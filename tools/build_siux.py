"""Siux brand page (EN/FR/DE): siux-switzerland.html, built from the spa page shell (like build_racket_guide.py).
Goal (Guti 26.11.2026): be the place to buy Siux padel rackets in Switzerland. Siux is rare here, we are official reseller,
ship from Switzerland in 1-2 working days and let people test first.
Nothing is invented: models, prices and dates come from shop.html, stock and price live from the shop app, specs from
tools/racket_specs.json. Rerun when a model is added: python3 tools/build_siux.py (from repo root), then tools/ux_nav.py."""
import re, json, html, urllib.parse, urllib.request, datetime
SLUG = 'siux-switzerland.html'
BASE = 'https://www.racketsacademy.ch/'
WA = '41772780115'
IMG = 'images/photos/shop-winners.jpg'

T = {
'en': dict(title='Siux padel rackets Switzerland – buy & test | Rackets Academy',
  desc='Siux padel rackets in Switzerland: official reseller in Valais, prices in CHF with no customs, delivery in 1–2 working days. Test any racket for 10 CHF first.',
  kicker='Siux · official reseller', h1='Siux padel rackets in Switzerland',
  lede='Siux is hard to find in Switzerland. We have the rackets here in Valais: in Swiss francs, without customs, at your door in 1–2 working days. And you can test before you buy.',
  chips=['In CHF, no customs', 'Delivery in 1–2 working days', 'Test for 10 CHF', 'Official reseller'],
  cta='See the rackets', cta2='Ask us on WhatsApp', wa='Hola! I have a question about Siux rackets.',
  now_h='In stock now', now_p='Order today, pick up tomorrow in Salgesch or Sion, or have it sent by post for free.',
  new_h='New 2027 collection', new_p='In store from {day}. Have a look now and be among the first.',
  out_h='Sold out at the moment', out_p='Write to us on WhatsApp and we tell you when it is back.',
  lab=dict(now='In stock', new='From {day}', out='Sold out'),
  spec=dict(Rund='Round', Träne='Teardrop', Diamant='Diamond', Weich='soft', Mittel='medium', Hart='hard',
            Amateur='amateur', Fortgeschritten='advanced', Profi='pro', Kopflastig='head-heavy', Grifflastig='handle-heavy'),
  lvl='Level', bal='balance',
  find_h='Not sure which Siux suits you?', find_p='Three taps in our racket guide and you see what fits your game.', find_b='To the racket guide',
  facts_h='Why buy your Siux from us',
  facts=[('🇨🇭', 'From Switzerland', 'Prices in Swiss francs, no customs and no import fees. Returns within 30 days if new and in original packaging.'),
         ('📦', 'With you in 1–2 working days', 'We ship by post anywhere in Switzerland for free, or you pick up in Salgesch or Sion.'),
         ('🎾', 'Test first', 'Rent the racket for 10 CHF and play a real match with it. If you buy it, we credit the 10 CHF.')],
  faq_h='Siux questions',
  faq=[('Where can I buy Siux padel rackets in Switzerland?', 'At Rackets Academy, official Siux reseller in Valais: online with delivery anywhere in Switzerland in 1–2 working days, or in our clubs in Salgesch and Sion.'),
       ('Do I pay customs on a Siux racket?', 'No. We ship from Switzerland and the price is in Swiss francs. There are no customs or import fees.'),
       ('How fast is delivery?', '1–2 working days by post anywhere in Switzerland, free of charge. You can also pick up in Salgesch or Sion.'),
       ('Can I test a Siux racket before buying?', 'Yes. You rent any racket for 10 CHF and play a real match with it in Salgesch or Sion. If you buy it, the 10 CHF are credited.'),
       ('Which Siux models do you have?', 'Currently {models}. Stock and prices on this page are updated live.'),
       ('What does a Siux racket cost?', 'With us between {lo} and {hi} CHF, depending on the model.')],
  final_h='Your Siux, tomorrow or the day after.', final_p='In CHF · no customs · 1–2 working days · test for 10 CHF'),
'fr': dict(title='Raquettes Siux en Suisse – acheter & tester | Rackets Academy',
  desc='Raquettes de padel Siux en Suisse : revendeur officiel en Valais, prix en CHF sans douane, livraison en 1–2 jours ouvrables. Teste chaque raquette pour 10 CHF.',
  kicker='Siux · revendeur officiel', h1='Raquettes de padel Siux en Suisse',
  lede="Siux est difficile à trouver en Suisse. Nous avons les raquettes ici en Valais : en francs suisses, sans douane, chez toi en 1–2 jours ouvrables. Et tu peux tester avant d'acheter.",
  chips=['En CHF, sans douane', 'Livraison en 1–2 jours ouvrables', 'Test à 10 CHF', 'Revendeur officiel'],
  cta='Voir les raquettes', cta2='Demande-nous sur WhatsApp', wa="Hola ! J'ai une question sur les raquettes Siux.",
  now_h='Disponibles maintenant', now_p="Commande aujourd'hui, retire demain à Salgesch ou Sion, ou reçois-la gratuitement par la Poste.",
  new_h='Nouvelle collection 2027', new_p='En magasin dès le {day}. Regarde déjà et sois parmi les premiers.',
  out_h='Épuisées pour le moment', out_p='Écris-nous sur WhatsApp et on te dit quand elle revient.',
  lab=dict(now='En stock', new='Dès le {day}', out='Épuisé'),
  spec=dict(Rund='Ronde', Träne='Goutte d’eau', Diamant='Diamant', Weich='souple', Mittel='moyenne', Hart='dure',
            Amateur='amateur', Fortgeschritten='avancé', Profi='pro', Kopflastig='poids en tête', Grifflastig='poids vers le manche'),
  lvl='Niveau', bal='équilibre',
  find_h='Tu ne sais pas quelle Siux te convient ?', find_p='Trois réponses dans notre guide et tu vois ce qui va avec ton jeu.', find_b='Vers le guide des raquettes',
  facts_h='Pourquoi acheter ta Siux chez nous',
  facts=[('🇨🇭', 'Depuis la Suisse', "Prix en francs suisses, sans douane ni frais d'importation. Retour sous 30 jours si neuve et dans l'emballage d'origine."),
         ('📦', 'Chez toi en 1–2 jours ouvrables', 'Envoi gratuit par la Poste partout en Suisse, ou retrait à Salgesch ou Sion.'),
         ('🎾', "Teste d'abord", "Loue la raquette pour 10 CHF et joue un vrai match avec. Si tu l'achètes, on déduit les 10 CHF.")],
  faq_h='Questions sur Siux',
  faq=[('Où acheter une raquette de padel Siux en Suisse ?', 'À la Rackets Academy, revendeur officiel Siux en Valais : en ligne avec livraison partout en Suisse en 1–2 jours ouvrables, ou dans nos clubs à Salgesch et Sion.'),
       ('Est-ce que je paie la douane sur une raquette Siux ?', "Non. Nous envoyons depuis la Suisse et le prix est en francs suisses. Il n'y a ni douane ni frais d'importation."),
       ('Quel est le délai de livraison ?', '1–2 jours ouvrables par la Poste partout en Suisse, gratuitement. Le retrait à Salgesch ou Sion est aussi possible.'),
       ("Puis-je tester une raquette Siux avant d'acheter ?", "Oui. Tu loues n'importe quelle raquette pour 10 CHF et tu joues un vrai match avec, à Salgesch ou à Sion. Si tu l'achètes, les 10 CHF sont déduits."),
       ('Quels modèles Siux avez-vous ?', 'Actuellement {models}. Le stock et les prix sur cette page sont mis à jour en direct.'),
       ('Combien coûte une raquette Siux ?', 'Chez nous entre {lo} et {hi} CHF, selon le modèle.')],
  final_h='Ta Siux, demain ou après-demain.', final_p='En CHF · sans douane · 1–2 jours ouvrables · test à 10 CHF'),
'de': dict(title='Siux Padelschläger Schweiz – kaufen & testen | Rackets Academy',
  desc='Siux Padelschläger in der Schweiz: offizieller Händler im Wallis, Preise in CHF ohne Zoll, Lieferung in 1–2 Werktagen. Jeden Schläger erst für 10 CHF testen.',
  kicker='Siux · offizieller Händler', h1='Siux Padelschläger in der Schweiz',
  lede='Siux findest du in der Schweiz kaum. Wir haben die Schläger hier im Wallis: in Franken, ohne Zoll, in 1–2 Werktagen bei dir. Und du kannst vor dem Kauf testen.',
  chips=['In CHF, ohne Zoll', 'Lieferung in 1–2 Werktagen', 'Test für 10 CHF', 'Offizieller Händler'],
  cta='Zu den Schlägern', cta2='Frag uns per WhatsApp', wa='Hola! Ich habe eine Frage zu den Siux-Schlägern.',
  now_h='Jetzt lieferbar', now_p='Heute bestellen, morgen in Salgesch oder Sion abholen, oder gratis per Post schicken lassen.',
  new_h='Neue Kollektion 2027', new_p='Im Laden ab {day}. Schau sie dir jetzt schon an und sei bei den Ersten.',
  out_h='Zurzeit ausverkauft', out_p='Schreib uns per WhatsApp, wir sagen dir, wann er wieder da ist.',
  lab=dict(now='Lieferbar', new='Ab {day}', out='Ausverkauft'),
  spec=dict(Rund='Rund', Träne='Träne', Diamant='Diamant', Weich='weich', Mittel='mittel', Hart='hart',
            Amateur='Amateur', Fortgeschritten='Fortgeschritten', Profi='Profi', Kopflastig='kopflastig', Grifflastig='grifflastig'),
  lvl='Niveau', bal='Balance',
  find_h='Unsicher, welcher Siux zu dir passt?', find_p='Drei Antworten in unserer Kaufberatung, und du siehst, was zu deinem Spiel passt.', find_b='Zur Kaufberatung',
  facts_h='Warum du deinen Siux bei uns kaufst',
  facts=[('🇨🇭', 'Aus der Schweiz', 'Preise in Franken, ohne Zoll und ohne Einfuhrgebühren. Rückgabe innert 30 Tagen, wenn neu und originalverpackt.'),
         ('📦', 'In 1–2 Werktagen bei dir', 'Gratis-Versand per Post in die ganze Schweiz, oder Abholung in Salgesch oder Sion.'),
         ('🎾', 'Erst testen', 'Miete den Schläger für 10 CHF und spiel damit ein echtes Match. Kaufst du ihn, schreiben wir dir die 10 CHF gut.')],
  faq_h='Fragen zu Siux',
  faq=[('Wo kann ich Siux Padelschläger in der Schweiz kaufen?', 'Bei der Rackets Academy, offizieller Siux-Händler im Wallis: online mit Lieferung in die ganze Schweiz in 1–2 Werktagen, oder in unseren Clubs in Salgesch und Sion.'),
       ('Zahle ich Zoll auf einen Siux-Schläger?', 'Nein. Wir verschicken aus der Schweiz, der Preis ist in Franken. Es fallen weder Zoll noch Einfuhrgebühren an.'),
       ('Wie schnell ist die Lieferung?', '1–2 Werktage per Post in die ganze Schweiz, gratis. Abholen in Salgesch oder Sion geht auch.'),
       ('Kann ich einen Siux-Schläger vor dem Kauf testen?', 'Ja. Du mietest jeden Schläger für 10 CHF und spielst damit ein echtes Match in Salgesch oder Sion. Kaufst du ihn, werden die 10 CHF angerechnet.'),
       ('Welche Siux-Modelle habt ihr?', 'Aktuell {models}. Bestand und Preise auf dieser Seite werden live nachgeführt.'),
       ('Was kostet ein Siux-Schläger?', 'Bei uns zwischen {lo} und {hi} CHF, je nach Modell.')],
  final_h='Dein Siux, morgen oder übermorgen.', final_p='In CHF · ohne Zoll · 1–2 Werktage · Test für 10 CHF'),
}

CARD_RE = re.compile(r'<div class="racket-card([^"]*)">\n(.*?)\n      </div>\n', re.S)
SPECS = {r[0]: dict(zip(['shape', 'weight', 'face', 'core', 'hard', 'level', 'balance'], r[2:] + [''] * 7))
         for r in json.load(open('tools/racket_specs.json'))[1:]}

def stock_url(shop):
    m = re.search(r'<form id="buy-modal-form"[^>]*action="([^"]+)"', shop)
    return m.group(1) + '?action=stock' if m else ''

_STOCK = {}
def live_stock(shop):
    url = stock_url(shop)
    if url and url not in _STOCK:
        for attempt in range(3):                      # die Shop-App antwortet manchmal erst beim zweiten Mal
            try:
                j = json.loads(urllib.request.urlopen(url, timeout=60).read().decode('utf-8'))
                _STOCK[url] = j.get('rackets', {}) if j.get('ok') else {}
                break
            except Exception as e:
                print('  Lagerabfrage Versuch', attempt + 1, 'fehlgeschlagen:', e); _STOCK[url] = {}
    return _STOCK.get(url, {})

def day_txt(iso, lang):
    d = datetime.date.fromisoformat(iso)
    m = {'en': 'January February March April May June July August September October November December',
         'de': 'Januar Februar März April Mai Juni Juli August September Oktober November Dezember',
         'fr': 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'}[lang].split()
    return (f'{d.day}. ' if lang == 'de' else f'{d.day} ') + m[d.month - 1]

def siux(shop):
    """All Siux rackets of the shop with state: now (in stock), new (announced with date), out (sold out)."""
    out, live, today = [], live_stock(shop), datetime.date.today().isoformat()
    for m in CARD_RE.finditer(shop):
        cls, c = m.group(1), m.group(2)
        mo = re.search(r"racketModel:'(siux-[^']+)'", c)
        if not mo or mo.group(1) not in SPECS: continue
        slug = mo.group(1)
        av = re.search(r'data-available="([\d-]+)"', c)
        qty = live[slug].get('qty') if slug in live else (0 if 'sold-out' in cls else 1)
        state = 'now' if qty else ('new' if av and av.group(1) > today else 'out')
        label = re.search(r"racketLabel:'([^']+)'", c).group(1).replace(' — ', ' ')
        out.append(dict(slug=slug, label=label, state=state, avail=av.group(1) if av else '',
                        price=int(live.get(slug, {}).get('price') or re.search(r'racket-price">(\d+)', c).group(1)),
                        img=re.search(r'<img class="racket-photo" src="([^"]+)"', c).group(1), **SPECS[slug]))
    return out

CSS = """<style id="sx-css">
.sx-grid{display:grid; grid-template-columns:repeat(4,1fr); gap:14px;}
.sx-card{display:flex; flex-direction:column; gap:5px; background:#fff; border:2px solid #d7e0ea; border-radius:20px; padding:14px; text-decoration:none; color:#0b1a2b;}
.sx-card:hover{border-color:#0077de;}
.sx-card img{width:100%; aspect-ratio:1/1; object-fit:contain;}
.sx-card b{font-size:1.05rem; line-height:1.25;}
.sx-card span{font-size:.95rem; color:#4c5d70;}
.sx-card strong{font-size:1.15rem; margin-top:auto; padding-top:4px;}
.sx-tag{align-self:flex-start; font-size:.9rem; font-weight:700; border-radius:999px; padding:4px 12px; background:#6ffd1d; color:#0b1a2b;}
.sx-card[data-state="new"] .sx-tag{background:#0077de; color:#fff;}
.sx-card[data-state="out"] .sx-tag{background:#e3e9ef; color:#4c5d70;}
.sx-card[data-state="out"] img{opacity:.55;}
.sx-find{background:#eef4fa; border-radius:24px; padding:26px; display:flex; align-items:center; justify-content:space-between; gap:16px 24px; flex-wrap:wrap;}
.sx-find h2{margin:0 0 4px; color:#0077de;}
.sx-find p{margin:0; color:#0b1a2b;}
@media (max-width:980px){ .sx-grid{grid-template-columns:repeat(2,1fr);} }
@media (max-width:480px){ .sx-card{padding:10px;} .sx-card b{font-size:1rem;} .sx-find .btn{width:100%; text-align:center;} }
</style>
"""

JS = """<script id="sx-js">
(function(){
  var d=document.getElementById('sx-data'); if(!d) return; var D=JSON.parse(d.textContent); if(!D.stock) return;
  fetch(D.stock).then(function(r){return r.json();}).then(function(j){
    if(!j||!j.ok||!j.rackets) return;
    document.querySelectorAll('.sx-card[data-sx]').forEach(function(a){var i=j.rackets[a.dataset.sx]; if(!i) return;
      if(i.price){a.querySelector('strong').textContent=i.price+' CHF';}
      var st=i.qty>0?'now':(a.dataset.state==='new'?'new':'out');
      if(st!==a.dataset.state){a.dataset.state=st; a.querySelector('.sx-tag').textContent=D.lab[st];}
    });
  }).catch(function(){});
})();
</script>
"""

def body(t, pre, lang, rs, stock):
    wa = 'https://wa.me/' + WA + '?text=' + urllib.parse.quote(t['wa'])
    sp = t['spec']
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in t['chips'])
    facts = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['facts'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    def tag(r): return t['lab'][r['state']].format(day=day_txt(r['avail'], lang) if r['avail'] else '')
    def card(r):
        return (f'<a class="sx-card" data-sx="{r["slug"]}" data-state="{r["state"]}" href="rackets/{r["slug"]}.html"><span class="sx-tag">{tag(r)}</span>'
                f'<img src="{r["img"]}" alt="{html.escape(r["label"])}" loading="lazy"><b>{html.escape(r["label"])}</b>'
                f'<span>{sp[r["shape"]]} · {sp[r["hard"]]} · {r["weight"]} g</span><span>{t["lvl"]} {sp[r["level"]]} · {t["bal"]} {sp[r["balance"]]}</span><strong>{r["price"]} CHF</strong></a>')
    def sec(key, h, p):
        items = [r for r in rs if r['state'] == key]
        if not items: return ''
        day = day_txt(min(r['avail'] for r in items if r['avail']), lang) if key == 'new' else ''
        return f'''
<section class="co2-sec" id="{key}">
  <div class="wrap">
    <h2 class="co2-h">{h}</h2>
    <p class="pb-intro">{p.format(day=day)}</p>
    <div class="sx-grid">{''.join(card(r) for r in items)}</div>
  </div>
</section>
'''
    data = dict(stock=stock, lab={k: v.format(day='') .strip() for k, v in t['lab'].items() if k != 'new'})
    first = next((k for k in ('now', 'new', 'out') if any(r['state'] == k for r in rs)), 'now')
    return f'''
<section class="spa-hero co-hero kb-hero" style="background-image:url('{BASE + IMG}'); background-position:center 35%;">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="spa-chips">{chips}</div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="{SLUG}#{first}">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="{wa}" target="_blank" rel="noopener">{t['cta2']}</a>
    </div>
  </div>
</section>
{sec('now', t['now_h'], t['now_p'])}{sec('new', t['new_h'], t['new_p'])}{sec('out', t['out_h'], t['out_p'])}
<section class="co2-sec">
  <div class="wrap">
    <div class="sx-find">
      <div><h2>{t['find_h']}</h2><p>{t['find_p']}</p></div>
      <a class="btn btn-green" href="padel-racket-guide.html#finder">{t['find_b']}</a>
    </div>
  </div>
</section>

<section class="co2-sec">
  <div class="wrap">
    <h2 class="co2-h">{t['facts_h']}</h2>
    <div class="co2-bens ev-mods">{facts}</div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['faq_h']}</h2>
    <div class="spa-faq">{faq}</div>
  </div>
</section>

<section class="spa-final kb-final" style="background-image:url('{pre}images/coaching/coaching-6.webp');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-final-inner">
    <h2>{t['final_h']}</h2>
    <p>{t['final_p']}</p>
    <div class="hero-actions" style="justify-content:center;">
      <a class="btn btn-green spa-cta" href="{SLUG}#{first}">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>
<script type="application/json" id="sx-data">{json.dumps(data, ensure_ascii=False)}</script>

'''

for lang, t in T.items():
    pre = '' if lang == 'en' else '../'
    d = '' if lang == 'en' else lang + '/'
    url = BASE + d + SLUG
    shop = open(d + 'shop.html').read()
    rs = siux(shop)
    order = {'now': 0, 'new': 1, 'out': 2}
    rs.sort(key=lambda r: (order[r['state']], r['price'], r['label']))
    models = ', '.join(sorted({' '.join(r['label'].split(' ')[1:2]) for r in rs}))          # Diablo, Electra, Fenix, ...
    lo, hi = min(r['price'] for r in rs), max(r['price'] for r in rs)
    t['faq'] = [(q, a.format(models=models, lo=lo, hi=hi)) for q, a in t['faq']]
    s = open(d + 'spa-and-sauna.html').read()
    a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
    b = s.index('<footer')
    head, tail = s[:a], s[b:]
    head = head.replace('spa-and-sauna.html', SLUG).replace(f'href="{SLUG}" class="active"', 'href="spa-and-sauna.html"')   # canonical/hreflang/lang menu -> this page; nav Spa link stays
    s = head + body(t, pre, lang, rs, stock_url(shop)) + tail
    s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>' + t['title'].replace('&', '&amp;') + '</title>', s, count=1, flags=re.S)
    esc = lambda x: x.replace('&', '&amp;').replace('"', '&quot;')
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + esc(t['desc']) + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + esc(t['title']) + '"', s)
    s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="' + BASE + IMG + '"', s)
    ld = {'@context': 'https://schema.org', '@graph': [
      {'@type': 'ItemList', 'name': t['h1'], 'url': url,
       'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': r['label'], 'url': BASE + d + 'rackets/' + r['slug'] + '.html'} for i, r in enumerate(rs)]},
      {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}]}
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-sx">' + json.dumps(ld, ensure_ascii=False) + '</script>\n' + CSS + '</head>', 1)
    s = s.replace('</body>', JS + '</body>', 1)
    s = s.replace('class="active"', '')
    open(d + SLUG, 'w').write(s)
    print(d + SLUG, len(t['title']), len(t['desc']), [(r['slug'], r['state'], r['price']) for r in rs] if lang == 'en' else '')
