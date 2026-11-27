"""Shop v3 (Guti 27.11.2026): the shop shows rackets only; gift vouchers and Floky get their own pages.
Reason: on a phone the old page was 15 screens long and the first racket came after almost four.

What it does, for EN/FR/DE:
- shop.html: new lede, promise chips, three category pills (rackets / vouchers / Floky), racket section first,
  the box "never buy blind" moves below the rackets. Sections #vouchers and #floky move out.
- gift-vouchers.html and floky.html: built from the shop shell (header, buy window, footer) with the moved section.
- Page-only CSS and JS (prefix sv3-), no change to styles.css or nav.js, so no version numbers to bump.
- The racket cards stay in the HTML grouped by brand (build_rackets.py, build_racket_guide.py and build_siux.py read
  them there). The script in the browser puts them into one list: new and in stock first, sold out folded away,
  with filters by player type and brand and a sort order.
Run once from repo root: python3 tools/ux_shop_v3.py, then tools/ux_nav.py. Running it again changes nothing."""
import re, json, html
BASE = 'https://www.racketsacademy.ch/'
MARK = '<!-- shop-v3 -->'
V = 'gift-vouchers.html'
F = 'floky.html'

T = {
'en': dict(lede='Padel rackets from Wilson, Babolat and Siux: with you in 1–2 working days, or ready to pick up in Salgesch and Sion. You can test every racket first.',
  chips=['Delivery in 1–2 working days', 'In CHF, no customs', 'Test for 10 CHF', '30-day returns'],
  cats=['Rackets', 'Gift vouchers', 'Floky sleeves'],
  v_title='Padel gift vouchers | Rackets Academy', v_desc='Give padel: gift vouchers from 20 CHF for a game at Rackets Academy in Salgesch or Sion, plus course and racket vouchers. Sent by e-mail right after payment.',
  v_h1='Gift vouchers', v_lede='Give a game of padel, a course or a racket. You get the voucher by e-mail right after payment.',
  f_title='Floky arm sleeve for padel | Rackets Academy', f_desc='Floky No-Strain, the biomechanical arm sleeve for padel: dampens vibrations and supports elbow and forearm. Available at Rackets Academy in Valais.',
  f_h1='Floky sleeves', f_lede='The arm sleeve for padel from our partner Floky.',
  js=dict(type='Player type', brand='Brand', sort='Sort by', all='All', beg='Beginner', ctl='Control', allr='All-round', pow='Power',
          rec='Recommended', up='Price: low to high', down='Price: high to low', out='Sold out at the moment', none='No racket matches these filters.',
          test='Test it · 10 CHF', count='{n} rackets')),
'fr': dict(lede="Raquettes de padel Wilson, Babolat et Siux : chez toi en 1–2 jours ouvrables, ou à retirer à Salgesch et Sion. Tu peux tester chaque raquette avant.",
  chips=['Livraison en 1–2 jours ouvrables', 'En CHF, sans douane', 'Test à 10 CHF', 'Retour sous 30 jours'],
  cats=['Raquettes', 'Bons cadeaux', 'Manchons Floky'],
  v_title='Bons cadeaux padel | Rackets Academy', v_desc="Offre du padel : bons cadeaux dès 20 CHF pour une partie à la Rackets Academy à Salgesch ou Sion, et bons pour cours et raquettes. Envoyés par e-mail juste après le paiement.",
  v_h1='Bons cadeaux', v_lede="Offre une partie de padel, un cours ou une raquette. Tu reçois le bon par e-mail juste après le paiement.",
  f_title='Manchon Floky pour le padel | Rackets Academy', f_desc="Floky No-Strain, le manchon biomécanique pour le padel : amortit les vibrations et soutient le coude et l'avant-bras. Disponible à la Rackets Academy en Valais.",
  f_h1='Manchons Floky', f_lede='Le manchon pour le padel de notre partenaire Floky.',
  js=dict(type='Type de joueur', brand='Marque', sort='Trier par', all='Tous', beg='Débutant', ctl='Contrôle', allr='Polyvalent', pow='Puissance',
          rec='Recommandé', up='Prix croissant', down='Prix décroissant', out='Épuisées pour le moment', none='Aucune raquette ne correspond à ces filtres.',
          test='Teste-la · 10 CHF', count='{n} raquettes')),
'de': dict(lede='Padelschläger von Wilson, Babolat und Siux: in 1–2 Werktagen bei dir oder zur Abholung in Salgesch und Sion. Jeden Schläger kannst du vorher testen.',
  chips=['Lieferung in 1–2 Werktagen', 'In CHF, ohne Zoll', 'Test für 10 CHF', '30 Tage Rückgabe'],
  cats=['Schläger', 'Geschenkgutscheine', 'Floky Sleeves'],
  v_title='Padel-Geschenkgutscheine | Rackets Academy', v_desc='Verschenk Padel: Geschenkgutscheine ab 20 CHF für ein Spiel in der Rackets Academy in Salgesch oder Sion, dazu Kurs- und Racket-Gutscheine. Per E-Mail gleich nach der Zahlung.',
  v_h1='Geschenkgutscheine', v_lede='Verschenk ein Padel-Spiel, einen Kurs oder ein Racket. Den Gutschein bekommst du gleich nach der Zahlung per E-Mail.',
  f_title='Floky Arm-Sleeve für Padel | Rackets Academy', f_desc='Floky No-Strain, der biomechanische Arm-Sleeve für Padel: dämpft Vibrationen und stützt Ellbogen und Unterarm. Erhältlich in der Rackets Academy im Wallis.',
  f_h1='Floky Sleeves', f_lede='Der Arm-Sleeve für Padel von unserem Partner Floky.',
  js=dict(type='Spielertyp', brand='Marke', sort='Sortieren', all='Alle', beg='Einsteiger', ctl='Kontrolle', allr='Allround', pow='Power',
          rec='Empfohlen', up='Preis aufsteigend', down='Preis absteigend', out='Zurzeit ausverkauft', none='Kein Schläger passt zu diesen Filtern.',
          test='Testen · 10 CHF', count='{n} Schläger')),
}

CSS = """<style id="sv3-css">
.sv3-chips{display:flex; flex-wrap:wrap; gap:8px; margin:14px 0 0;}
.sv3-chips span{background:rgba(255,255,255,.16); backdrop-filter:blur(6px); border:1px solid rgba(255,255,255,.35); border-radius:999px; padding:6px 14px; font-weight:700; font-size:.9rem; color:#fff;}
.sv3-cats{display:flex; gap:8px; flex-wrap:wrap; padding:22px 0 6px;}
.sv3-cats a{font-weight:700; font-size:1rem; color:#0b1a2b; background:#fff; border:2px solid #c9d3de; border-radius:999px; padding:11px 18px; min-height:48px; box-sizing:border-box; display:inline-flex; align-items:center; text-decoration:none;}
.sv3-cats a:hover{border-color:#0077de;}
.sv3-cats a[aria-current="page"]{background:#0077de; border-color:#0077de; color:#fff;}
.sv3-cats a:focus-visible, .sv3-pill:focus-visible, .sv3-sort select:focus-visible{outline:3px solid #0077de; outline-offset:3px;}
.sv3-bar{background:#fff; border-radius:24px; padding:18px 20px; margin:0 0 20px; display:flex; gap:16px 28px; flex-wrap:wrap; align-items:flex-end; box-shadow:0 6px 20px rgba(11,26,43,.08);}
.sv3-group{display:flex; flex-direction:column; gap:8px; min-width:0;}
.sv3-label{margin:0; font-size:.95rem; font-weight:700; color:#4c5d70;}
.sv3-pills{display:flex; gap:8px; flex-wrap:wrap;}
.sv3-pill{font:inherit; font-size:1rem; font-weight:700; color:#0b1a2b; background:#fff; border:2px solid #c9d3de; border-radius:999px; padding:9px 16px; min-height:46px; cursor:pointer;}
.sv3-pill:hover{border-color:#0077de;}
.sv3-pill[aria-pressed="true"]{background:#0077de; border-color:#0077de; color:#fff;}
.sv3-sort select{font:inherit; font-size:1rem; font-weight:700; color:#0b1a2b; background:#fff; border:2px solid #c9d3de; border-radius:999px; padding:9px 14px; min-height:46px;}
.sv3-count{margin:0 0 12px; font-weight:700; color:#4c5d70;}
.sv3-brand{display:block; font-size:.78rem; font-weight:700; color:#4c5d70; margin-top:2px;}
.sv3-on .racket-brand-heading{display:none;}
.sv3-out{margin:28px 0 0;}
.sv3-out > summary{cursor:pointer; font-weight:700; font-size:1.05rem; color:#0b1a2b; padding:12px 0; min-height:48px; box-sizing:border-box;}
.sv3-out .racket-grid{margin-top:12px;}
.sv3-hide{display:none !important;}
.sv3-after{margin-top:36px;}
.hero h1{overflow-wrap:anywhere; hyphens:auto;}
@media (max-width:480px){ .hero h1{font-size:clamp(1.7rem,8.4vw,2.4rem); line-height:1.1;} }
@media (max-width:760px){
  .sv3-bar{padding:14px; border-radius:20px; gap:14px;}
  .sv3-group{width:100%;}
  .sv3-pills{flex-wrap:nowrap; overflow-x:auto; scrollbar-width:none; padding-bottom:2px;}
  .sv3-pills::-webkit-scrollbar{display:none;}
  .sv3-pill{flex:none;}
  .sv3-sort select{width:100%;}
  .sv3-cats a{flex:1 1 auto; justify-content:center; padding:11px 12px;}
}
</style>
"""

# moved sections keep their old anchors alive: shop.html#vouchers and #floky go to the new pages
REDIRECT = """<script id="sv3-redirect">(function(){function go(){var h=location.hash;if(h==='#vouchers'){location.replace('%s');}else if(h==='#floky'){location.replace('%s');}}go();addEventListener('hashchange',go);})();</script>
""" % (V, F)

JS = """<script id="sv3-js">
(function(){
  var sec=document.getElementById('rackets'); if(!sec) return;
  var T=JSON.parse(document.getElementById('sv3-data').textContent);
  var BR=['Wilson','Babolat','Siux'], state={type:'*',brand:'*',sort:'rec'}, order=0;
  var cards=[].slice.call(sec.querySelectorAll('.racket-card'));
  // brand per card from the heading above its grid, original position for "recommended"
  var brand='';
  sec.querySelectorAll('.racket-brand-heading, .racket-grid').forEach(function(el){
    if(el.classList.contains('racket-brand-heading')){brand=el.textContent.trim();return;}
    el.querySelectorAll('.racket-card').forEach(function(c){
      c.dataset.brand=brand; c.dataset.pos=order++;
      var a=c.querySelector('.racket-link');
      if(a&&!c.querySelector('.racket-test')){var t=document.createElement('a');t.className='racket-test';t.href=a.getAttribute('href');t.textContent=T.test;c.insertBefore(t,c.querySelector('.racket-model'));}
      if(!c.querySelector('.sv3-brand')){var b=document.createElement('span');b.className='sv3-brand';b.textContent=brand;c.insertBefore(b,c.querySelector('.racket-model'));}
    });
  });
  var first=sec.querySelector('.racket-brand-heading'); if(!first) return;
  var bar=document.createElement('div'); bar.className='sv3-bar';
  function group(key,label,opts){
    var g=document.createElement('div'); g.className='sv3-group';
    g.innerHTML='<p class="sv3-label">'+label+'</p><div class="sv3-pills" role="group" aria-label="'+label+'"></div>';
    opts.forEach(function(o,i){var b=document.createElement('button');b.type='button';b.className='sv3-pill';b.textContent=o[1];b.setAttribute('aria-pressed',i===0?'true':'false');
      b.addEventListener('click',function(){state[key]=o[0];g.querySelectorAll('.sv3-pill').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});draw();});
      g.lastChild.appendChild(b);});
    bar.appendChild(g);
  }
  group('type',T.type,[['*',T.all],['beg',T.beg],['ctl',T.ctl],['all',T.allr],['pow',T.pow]]);
  group('brand',T.brand,[['*',T.all]].concat(BR.map(function(b){return [b,b];})));
  var sg=document.createElement('div'); sg.className='sv3-group sv3-sort';
  sg.innerHTML='<label class="sv3-label" for="sv3-sort">'+T.sort+'</label><select id="sv3-sort"><option value="rec">'+T.rec+'</option><option value="up">'+T.up+'</option><option value="down">'+T.down+'</option></select>';
  sg.querySelector('select').addEventListener('change',function(e){state.sort=e.target.value;draw();});
  bar.appendChild(sg);
  var count=document.createElement('p'); count.className='sv3-count'; count.setAttribute('aria-live','polite');
  var grid=document.createElement('div'); grid.className='racket-grid';
  var empty=document.createElement('p'); empty.className='racket-empty'; empty.textContent=T.none; empty.hidden=true;
  var out=document.createElement('details'); out.className='sv3-out'; out.innerHTML='<summary></summary><div class="racket-grid"></div>';
  first.parentNode.insertBefore(bar,first); first.parentNode.insertBefore(count,first); first.parentNode.insertBefore(grid,first);
  first.parentNode.insertBefore(empty,first); first.parentNode.insertBefore(out,first);
  sec.querySelectorAll('.racket-grid').forEach(function(g){if(g!==grid&&g!==out.lastChild&&g.getAttribute('data-brand')===null){g.classList.add('sv3-hide');}});
  sec.classList.add('sv3-on');
  function price(c){return parseInt((c.querySelector('.racket-price')||{}).textContent,10)||0;}
  function isType(c,t){var s=c.dataset;
    if(t==='beg') return s.level==='Amateur'||s.hard==='Weich';
    if(t==='ctl') return s.shape==='Rund';
    if(t==='all') return s.shape==='Träne';
    if(t==='pow') return s.shape==='Diamant';
    return true;}
  var busy=false;
  function draw(){
    busy=true;
    var list=cards.filter(function(c){return (state.brand==='*'||c.dataset.brand===state.brand)&&isType(c,state.type);});
    list.sort(function(a,b){
      if(state.sort==='up') return price(a)-price(b)||a.dataset.pos-b.dataset.pos;
      if(state.sort==='down') return price(b)-price(a)||a.dataset.pos-b.dataset.pos;
      function rank(c){return c.classList.contains('coming')?2:(c.querySelector('.racket-badge')?0:1);}   // new and in stock, in stock, announced
      return rank(a)-rank(b)||BR.indexOf(a.dataset.brand)-BR.indexOf(b.dataset.brand)||a.dataset.pos-b.dataset.pos;});   // Wilson first: main sponsor
    var avail=list.filter(function(c){return !c.classList.contains('sold-out')||c.classList.contains('coming');});
    var gone=list.filter(function(c){return c.classList.contains('sold-out')&&!c.classList.contains('coming');});
    cards.forEach(function(c){if(list.indexOf(c)<0&&c.parentNode){c.parentNode.removeChild(c);}});
    avail.forEach(function(c){grid.appendChild(c);});
    gone.forEach(function(c){out.lastChild.appendChild(c);});
    out.firstChild.textContent=T.out+' ('+gone.length+')';
    out.hidden=!gone.length; empty.hidden=avail.length>0||gone.length>0;
    count.textContent=T.count.replace('{n}',avail.length);
    setTimeout(function(){busy=false;},0);
  }
  draw();
  // nav.js sets sold-out / coming / specs after its live stock call: arrange again when that happens
  var timer; new MutationObserver(function(){if(busy) return; clearTimeout(timer); timer=setTimeout(draw,60);})
    .observe(sec,{subtree:true,attributes:true,attributeFilter:['class','data-shape']});
})();
</script>
"""

def panel(h, sid):
    a = h.index('<section id="%s"' % sid); b = h.index('</section>', a) + len('</section>')
    return a, b

def cats(t, active):
    links = [('shop.html', t['cats'][0]), (V, t['cats'][1]), (F, t['cats'][2])]
    return ('<section class="section-tight" style="padding-top:0; padding-bottom:0;">\n  <div class="wrap">\n    <nav class="sv3-cats" aria-label="Shop">'
            + ''.join('<a href="%s"%s>%s</a>' % (u, ' aria-current="page"' if i == active else '', n) for i, (u, n) in enumerate(links))
            + '</nav>\n  </div>\n</section>\n\n')

def head_for(h, slug, title, desc, lang):
    """Shop head for another page: own title, description, canonical, hreflang, language switch."""
    d = '' if lang == 'en' else lang + '/'
    esc = lambda x: html.escape(x, quote=True)
    h = re.sub(r'<title>.*?</title>', '<title>' + html.escape(title, quote=False) + '</title>', h, count=1, flags=re.S)
    for k in ['name="description"', 'property="og:description"']:
        h = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + esc(desc) + '"', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + esc(title) + '"', h)
    h = re.sub(r'<meta property="og:url" content="[^"]*"', '<meta property="og:url" content="' + BASE + d + slug + '"', h)
    h = re.sub(r'<link rel="canonical" href="[^"]*"', '<link rel="canonical" href="' + BASE + d + slug + '"', h)
    for l in ['en', 'fr', 'de', 'x-default']:
        lp = '' if l in ('en', 'x-default') else l + '/'
        h = re.sub(r'<link rel="alternate" hreflang="' + l + '" href="[^"]*"', '<link rel="alternate" hreflang="' + l + '" href="' + BASE + lp + slug + '"', h)
    h = re.sub(r'(<div class="lang-menu">)(.*?)(</div>)', lambda m: m.group(1) + m.group(2).replace('shop.html', slug) + m.group(3), h, flags=re.S)
    h = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\n?', '', h, flags=re.S)      # shop schema belongs to the shop
    return h

for lang, t in T.items():
    d = '' if lang == 'en' else lang + '/'
    f = d + 'shop.html'
    h = open(f).read()
    if MARK in h:
        print(f, 'already v3'); continue
    hero_a = h.index('<section class="hero"'); hero_b = h.index('</section>', hero_a) + len('</section>')
    bub_a = h.index('<section', hero_b); bub_b = h.index('</section>', bub_a) + len('</section>')
    assert 'shop-bubbles' in h[bub_a:bub_b]
    va, vb = panel(h, 'vouchers'); fa, fb = panel(h, 'floky'); ra, rb = panel(h, 'rackets')
    vouchers, floky, rackets = h[va:vb], h[fa:fb], h[ra:rb]
    top, hero, bottom = h[:hero_a], h[hero_a:hero_b], h[fb:]
    assert va > bub_b and ra > vb and fa > rb, 'unexpected section order'

    def hero_with(h1, lede, chips=None):
        x = re.sub(r'<h1>.*?</h1>', '<h1>' + h1 + '</h1>', hero, count=1, flags=re.S)
        x = re.sub(r'<p class="lede">.*?</p>', '<p class="lede">' + lede + '</p>'
                   + ('\n    <div class="sv3-chips">' + ''.join('<span>%s</span>' % c for c in chips) + '</div>' if chips else ''), x, count=1, flags=re.S)
        return x

    # --- shop: rackets only -------------------------------------------------
    r = rackets.replace('class="shop-panel"', 'class="shop-panel active"', 1)
    box_a = r.index('<div class="highlight-box"'); box_b = r.index('</div>', r.index('</p>', box_a)) + len('</div>')
    box = r[box_a:box_b]
    r = r[:box_a].rstrip() + '\n\n    ' + r[box_b:].lstrip()
    end = r.rindex('</div>', 0, r.rindex('</section>'))                 # closing tag of .wrap
    r = r[:end] + '  <div class="sv3-after">\n    ' + box.replace(' style="margin-bottom:32px;"', '') + '\n    </div>\n  ' + r[end:]
    h1 = re.search(r'<h1>(.*?)</h1>', hero, re.S).group(1)
    data = '<script type="application/json" id="sv3-data">' + json.dumps(t['js'], ensure_ascii=False) + '</script>\n'
    # Titelbild Shop (Guti 27.11.2026: «besseres Titelbild»): Spielerin mit Wilson-Schläger in unserer Halle statt Siegerfoto
    shop_hero = hero_with(h1, t['lede'], t['chips'])
    shop_hero = re.sub(r"url\('[^']*shop-winners[^']*'\)", "url('" + BASE + "images/photos/visp-player.webp')", shop_hero)
    shop_hero = shop_hero.replace('background-position:center 35%', 'background-position:center 47%')
    assert 'visp-player.webp' in shop_hero
    shop = (top.replace('</head>', MARK + '\n' + REDIRECT + CSS + '</head>', 1)
            + shop_hero + '\n\n' + cats(t, 0) + r + '\n\n'
            + bottom.replace('</body>', data + JS + '</body>', 1))
    open(f, 'w').write(shop)

    # --- own pages for vouchers and Floky ------------------------------------
    for slug, sec, title, desc, h1x, ledex, idx in [(V, vouchers, t['v_title'], t['v_desc'], t['v_h1'], t['v_lede'], 1),
                                                   (F, floky, t['f_title'], t['f_desc'], t['f_h1'], t['f_lede'], 2)]:
        page = (head_for(top, slug, title, desc, lang).replace('</head>', MARK + '\n' + CSS + '</head>', 1)
                + hero_with(h1x, ledex) + '\n\n' + cats(t, idx)
                + sec.replace('class="shop-panel"', 'class="shop-panel active"', 1) + '\n\n' + bottom)
        open(d + slug, 'w').write(page)
    print(f, 'rebuilt;', d + V, d + F)
