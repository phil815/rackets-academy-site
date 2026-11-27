"""Padel racket buying guide (EN/FR/DE): padel-racket-guide.html, built from the spa page shell (like build_tennis.py).
Goal (Guti 25.11.2026): answer the question people ask Google and AI assistants ("which padel racket suits me?")
with our own rackets. Nothing is invented: rackets, prices and stock come from shop.html, the specs from
tools/racket_specs.json (Shop sheet, tab RacketSpecs). Sold-out and not-yet-available rackets are left out.
Rerun after every shop change: python3 tools/build_racket_guide.py (from repo root), then tools/ux_nav.py."""
import re, json, html, urllib.parse
SLUG = 'padel-racket-guide.html'
BASE = 'https://www.racketsacademy.ch/'
WA = '41772780115'
IMG = 'images/photos/shop-winners.jpg'
PER = 4                                   # rackets shown per profile
BRANDS = ['Wilson', 'Babolat', 'Siux']    # Wilson first: main sponsor

T = {
'en': dict(title='Which padel racket suits me? Buying guide | Rackets Academy',
  desc='Padel racket buying guide from Valais: shape, hardness and weight explained simply, with picks for beginners, control, all-round and power. Test any racket for 10 CHF.',
  kicker='Padel racket guide', h1='Which padel racket suits me?',
  lede='Three things decide: shape, hardness and weight. Here is how to choose, with the rackets we have in the shop right now. And you can test every one before you buy.',
  chips=['Test for 10 CHF', 'Credited when you buy', 'Pick up in Salgesch or Sion', 'Free shipping'],
  cta='See all rackets', cta2='Ask us on WhatsApp', wa='Hola! I need help choosing a padel racket.',
  fd=dict(h='Find your racket', p='Three taps and you see the rackets that suit you.',
     q=[('How often do you play?', [('new', 'I am new'), ('reg', 'Regularly'), ('pro', 'Tournaments')]),
        ('How do you play?', [('ctl', 'Safe and controlled'), ('all', 'A bit of everything'), ('pow', 'Attack')]),
        ('Sensitive arm?', [('yes', 'Yes'), ('no', 'No')])],
     res='These suit you', view='View', test='Book a test', wa="Hola! I'd like to test the {label}."),
  flow_h='Three questions to the right racket',
  flow=[('1', 'Which shape?', 'Round gives control and forgives off-centre hits. Diamond gives power but needs clean technique. Teardrop sits in between.'),
        ('2', 'How hard?', 'A soft racket is comfortable, easy on the arm and helps the ball out. A hard racket gives more pressure and precision once you hit cleanly.'),
        ('3', 'How heavy?', 'Lighter and balanced towards the handle is easy to move at the net. Heavier and head-heavy puts more weight behind smashes.')],
  prof=[('beg', 'For beginners', 'Easy to play and forgiving. These rackets are soft or made for amateur level, so you get the ball over the net while you learn.'),
        ('ctl', 'For control', 'Round shape, large sweet spot. For players who build the point, defend well and rarely give a ball away.'),
        ('all', 'All-round', 'Teardrop shape: a mix of control and power. A good choice if you play a bit of everything or do not know your style yet.'),
        ('pow', 'For power', 'Diamond shape, more weight in the head. For players who attack, smash and already hit the ball cleanly.')],
  spec=dict(Rund='Round', Träne='Teardrop', Diamant='Diamond', Weich='soft', Mittel='medium', Hart='hard'),
  facts_h='Test first, then buy',
  facts=[('🎾', 'Test for 10 CHF', 'Rent the racket and play a real match with it. If you buy it, we credit the 10 CHF to the price.'),
         ('✅', 'Official reseller', 'We are an official reseller of Wilson, Babolat and Siux. Every racket is new and original.'),
         ('📦', 'Pick up or shipping', 'Pick up in Salgesch or Sion, or free shipping by post. Returns within 30 days if new and in original packaging.')],
  faq_h='Racket questions',
  faq=[('Which padel racket is best for beginners?', 'A round or teardrop racket that is soft to medium and not too heavy. It forgives off-centre hits and is easy on the arm. In our shop these are for example {beg}.'),
       ('Round, teardrop or diamond: what is the difference?', 'Round means control and a large sweet spot. Diamond means power, with the weight in the head. Teardrop is the middle: some of both.'),
       ('How much does a good padel racket cost?', 'The rackets in our shop currently cost between {lo} and {hi} CHF. For a beginner a racket around {lo}–200 CHF is enough.'),
       ('Can I test a racket before I buy it?', 'Yes. You rent any racket for 10 CHF and play a real match with it in Salgesch or Sion. If you buy it, the 10 CHF are credited.'),
       ('Where can I buy a padel racket in Valais?', 'At Rackets Academy in Salgesch (Littenstrasse 30) and Sion (Route de Préjeux 16), or online with pick-up or free shipping in Switzerland.'),
       ('I come from tennis. Which racket should I choose?', 'Tennis players often bring power from their swing, so many feel comfortable with a teardrop racket of medium hardness. The best way is to test two shapes in a match.')],
  final_h='Not sure yet? Test two.', final_p='10 CHF per test · credited when you buy · Salgesch and Sion'),
'fr': dict(title='Quelle raquette de padel choisir ? Guide | Rackets Academy',
  desc='Guide pour choisir ta raquette de padel en Valais : forme, dureté et poids expliqués simplement, avec nos choix pour débutants, contrôle, polyvalence et puissance. Test à 10 CHF.',
  kicker='Guide raquettes de padel', h1='Quelle raquette de padel choisir ?',
  lede="Trois choses comptent : la forme, la dureté et le poids. Voici comment choisir, avec les raquettes que nous avons en ce moment à la boutique. Et tu peux tester chacune avant d'acheter.",
  chips=['Test à 10 CHF', 'Déduit si tu achètes', 'Retrait à Salgesch ou Sion', 'Envoi gratuit'],
  cta='Voir toutes les raquettes', cta2='Demande-nous sur WhatsApp', wa="Hola ! J'ai besoin d'aide pour choisir une raquette de padel.",
  fd=dict(h='Trouve ta raquette', p='Trois réponses et tu vois les raquettes qui te conviennent.',
     q=[('Tu joues souvent ?', [('new', 'Je débute'), ('reg', 'Régulièrement'), ('pro', 'En tournoi')]),
        ('Comment joues-tu ?', [('ctl', 'Sûr et contrôlé'), ('all', 'Un peu de tout'), ('pow', 'Attaque')]),
        ('Bras sensible ?', [('yes', 'Oui'), ('no', 'Non')])],
     res='Celles qui te conviennent', view='Voir', test='Réserver un test', wa="Hola ! J'aimerais tester la {label}."),
  flow_h='Trois questions pour trouver ta raquette',
  flow=[('1', 'Quelle forme ?', 'La forme ronde donne du contrôle et pardonne les frappes décentrées. Le diamant donne de la puissance mais demande une technique propre. La goutte d’eau est entre les deux.'),
        ('2', 'Quelle dureté ?', 'Une raquette souple est confortable, ménage le bras et aide la balle à sortir. Une raquette dure donne plus de pression et de précision quand tu frappes proprement.'),
        ('3', 'Quel poids ?', 'Plus légère et équilibrée vers le manche, elle est facile à manier au filet. Plus lourde avec le poids en tête, elle met plus de force dans les smashs.')],
  prof=[('beg', 'Pour débuter', 'Faciles à jouer et tolérantes. Ces raquettes sont souples ou prévues pour le niveau amateur : la balle passe le filet pendant que tu apprends.'),
        ('ctl', 'Pour le contrôle', 'Forme ronde, grande zone de frappe. Pour celles et ceux qui construisent le point, défendent bien et donnent peu de balles.'),
        ('all', 'Polyvalentes', 'Forme goutte d’eau : un mélange de contrôle et de puissance. Un bon choix si tu joues un peu de tout ou si tu ne connais pas encore ton style.'),
        ('pow', 'Pour la puissance', 'Forme diamant, plus de poids en tête. Pour celles et ceux qui attaquent, smashent et frappent déjà proprement.')],
  spec=dict(Rund='Ronde', Träne='Goutte d’eau', Diamant='Diamant', Weich='souple', Mittel='moyenne', Hart='dure'),
  facts_h="Teste d'abord, achète ensuite",
  facts=[('🎾', 'Test à 10 CHF', "Loue la raquette et joue un vrai match avec. Si tu l'achètes, on déduit les 10 CHF du prix."),
         ('✅', 'Revendeur officiel', 'Nous sommes revendeur officiel de Wilson, Babolat et Siux. Chaque raquette est neuve et originale.'),
         ('📦', 'Retrait ou envoi', "Retrait à Salgesch ou Sion, ou envoi gratuit par la Poste. Retour sous 30 jours si neuve et dans l'emballage d'origine.")],
  faq_h='Questions sur les raquettes',
  faq=[('Quelle raquette de padel pour débuter ?', 'Une raquette ronde ou goutte d’eau, souple à moyenne et pas trop lourde. Elle pardonne les frappes décentrées et ménage le bras. Dans notre boutique, par exemple {beg}.'),
       ('Ronde, goutte d’eau ou diamant : quelle différence ?', 'Ronde : contrôle et grande zone de frappe. Diamant : puissance, avec le poids en tête. Goutte d’eau : le milieu, un peu des deux.'),
       ('Combien coûte une bonne raquette de padel ?', 'Les raquettes de notre boutique coûtent actuellement entre {lo} et {hi} CHF. Pour débuter, une raquette autour de {lo}–200 CHF suffit.'),
       ("Puis-je tester une raquette avant de l'acheter ?", "Oui. Tu loues n'importe quelle raquette pour 10 CHF et tu joues un vrai match avec, à Salgesch ou à Sion. Si tu l'achètes, les 10 CHF sont déduits."),
       ('Où acheter une raquette de padel en Valais ?', 'À la Rackets Academy à Salgesch (Littenstrasse 30) et à Sion (Route de Préjeux 16), ou en ligne avec retrait ou envoi gratuit en Suisse.'),
       ('Je viens du tennis. Quelle raquette choisir ?', 'Les joueurs de tennis apportent souvent de la puissance avec leur geste ; beaucoup se sentent bien avec une goutte d’eau de dureté moyenne. Le mieux est de tester deux formes en match.')],
  final_h='Pas encore sûr ? Testes-en deux.', final_p='10 CHF par test · déduits si tu achètes · Salgesch et Sion'),
'de': dict(title='Welcher Padelschläger passt zu mir? Kaufberatung | Rackets Academy',
  desc='Kaufberatung Padelschläger aus dem Wallis: Form, Härte und Gewicht einfach erklärt, mit Empfehlungen für Einsteiger, Kontrolle, Allround und Power. Jeden Schläger für 10 CHF testen.',
  kicker='Kaufberatung Padelschläger', h1='Welcher Padelschläger passt zu mir?',
  lede='Drei Dinge entscheiden: Form, Härte und Gewicht. So wählst du, mit den Schlägern, die wir gerade im Shop haben. Und du kannst jeden vor dem Kauf testen.',
  chips=['Test für 10 CHF', 'Beim Kauf angerechnet', 'Abholung in Salgesch oder Sion', 'Versand gratis'],
  cta='Alle Schläger ansehen', cta2='Frag uns per WhatsApp', wa='Hola! Ich brauche Hilfe bei der Wahl eines Padelschlägers.',
  fd=dict(h='Finde deinen Schläger', p='Drei Antworten antippen, und du siehst die Schläger, die zu dir passen.',
     q=[('Wie oft spielst du?', [('new', 'Neu dabei'), ('reg', 'Regelmässig'), ('pro', 'Turniere')]),
        ('Wie spielst du?', [('ctl', 'Sicher und kontrolliert'), ('all', 'Von allem etwas'), ('pow', 'Angriff')]),
        ('Empfindlicher Arm?', [('yes', 'Ja'), ('no', 'Nein')])],
     res='Diese passen zu dir', view='Ansehen', test='Test buchen', wa='Hola! Ich möchte das {label} testen.'),
  flow_h='In drei Fragen zum richtigen Schläger',
  flow=[('1', 'Welche Form?', 'Rund gibt Kontrolle und verzeiht Bälle, die du nicht mittig triffst. Diamant gibt Power, braucht aber saubere Technik. Die Tränenform liegt dazwischen.'),
        ('2', 'Wie hart?', 'Ein weicher Schläger ist angenehm, schont den Arm und hilft dem Ball hinaus. Ein harter Schläger gibt mehr Druck und Präzision, sobald du sauber triffst.'),
        ('3', 'Wie schwer?', 'Leichter und grifflastig ist am Netz wendig. Schwerer und kopflastig bringt mehr Wucht in den Smash.')],
  prof=[('beg', 'Für Einsteiger', 'Leicht zu spielen und fehlerverzeihend. Diese Schläger sind weich oder für Amateur-Niveau gebaut: Der Ball kommt übers Netz, während du lernst.'),
        ('ctl', 'Für Kontrolle', 'Runde Form, grosse Trefferfläche. Für alle, die den Punkt aufbauen, gut verteidigen und kaum einen Ball verschenken.'),
        ('all', 'Allround', 'Tränenform: eine Mischung aus Kontrolle und Power. Eine gute Wahl, wenn du von allem etwas spielst oder deinen Stil noch nicht kennst.'),
        ('pow', 'Für Power', 'Diamantform, mehr Gewicht im Kopf. Für alle, die angreifen, smashen und den Ball schon sauber treffen.')],
  spec=dict(Rund='Rund', Träne='Träne', Diamant='Diamant', Weich='weich', Mittel='mittel', Hart='hart'),
  facts_h='Erst testen, dann kaufen',
  facts=[('🎾', 'Test für 10 CHF', 'Miete den Schläger und spiel damit ein echtes Match. Kaufst du ihn, schreiben wir dir die 10 CHF gut.'),
         ('✅', 'Offizieller Händler', 'Wir sind offizieller Händler von Wilson, Babolat und Siux. Jeder Schläger ist neu und original.'),
         ('📦', 'Abholung oder Versand', 'Abholung in Salgesch oder Sion, oder Gratis-Versand per Post. Rückgabe innert 30 Tagen, wenn neu und originalverpackt.')],
  faq_h='Fragen zu Schlägern',
  faq=[('Welcher Padelschläger ist gut für Anfänger?', 'Ein runder oder tränenförmiger Schläger, weich bis mittel und nicht zu schwer. Er verzeiht Bälle neben der Mitte und schont den Arm. Bei uns im Shop zum Beispiel {beg}.'),
       ('Rund, Träne oder Diamant: was ist der Unterschied?', 'Rund heisst Kontrolle und grosse Trefferfläche. Diamant heisst Power, mit dem Gewicht im Kopf. Die Träne ist die Mitte: etwas von beidem.'),
       ('Was kostet ein guter Padelschläger?', 'Die Schläger in unserem Shop kosten aktuell zwischen {lo} und {hi} CHF. Für den Einstieg reicht ein Schläger um {lo}–200 CHF.'),
       ('Kann ich einen Schläger vor dem Kauf testen?', 'Ja. Du mietest jeden Schläger für 10 CHF und spielst damit ein echtes Match in Salgesch oder Sion. Kaufst du ihn, werden die 10 CHF angerechnet.'),
       ('Wo kann ich im Wallis einen Padelschläger kaufen?', 'In der Rackets Academy in Salgesch (Littenstrasse 30) und in Sion (Route de Préjeux 16), oder online mit Abholung oder Gratis-Versand in der Schweiz.'),
       ('Ich komme vom Tennis. Welchen Schläger soll ich nehmen?', 'Tennisspieler bringen oft Power aus dem Schwung mit; viele fühlen sich mit einer Tränenform mittlerer Härte wohl. Am besten testest du zwei Formen im Match.')],
  final_h='Noch unsicher? Teste zwei.', final_p='10 CHF pro Test · beim Kauf angerechnet · Salgesch und Sion'),
}

CARD_RE = re.compile(r'<div class="racket-card([^"]*)">\n(.*?)\n      </div>\n', re.S)
SPECS = {r[0]: dict(zip(['shape', 'weight', 'face', 'core', 'hard', 'level', 'balance'], r[2:] + [''] * 7))
         for r in json.load(open('tools/racket_specs.json'))[1:]}

def stock_url(shop):
    m = re.search(r'<form id="buy-modal-form"[^>]*action="([^"]+)"', shop)
    return m.group(1) + '?action=stock' if m else ''

_STOCK = {}
def live_stock(shop):
    """Live price and quantity from the shop app (same call as nav.js on the shop page). Empty dict if it cannot be reached:
    then the static shop.html decides, and the page corrects itself in the browser."""
    url = stock_url(shop)
    if url and url not in _STOCK:
        try:
            import urllib.request
            j = json.loads(urllib.request.urlopen(url, timeout=40).read().decode('utf-8'))
            _STOCK[url] = j.get('rackets', {}) if j.get('ok') else {}
        except Exception as e:
            print('  Lagerabfrage nicht erreichbar, nehme shop.html:', e); _STOCK[url] = {}
    return _STOCK.get(url, {})

def rackets(shop):
    """All rackets that can be bought today, with price, photo and specs."""
    out = []; live = live_stock(shop)
    for m in CARD_RE.finditer(shop):
        cls, c = m.group(1), m.group(2)
        mo = re.search(r"racketModel:'([^']+)'", c)
        if not mo or mo.group(1) not in SPECS: continue
        if mo.group(1) not in live_stock(shop) and ('sold-out' in cls or 'coming' in cls): continue
        slug = mo.group(1)
        if slug in live and not live[slug].get('qty'): continue      # Lager 0: nicht empfehlen
        label = re.search(r"racketLabel:'([^']+)'", c).group(1).replace(' — ', ' ')
        out.append(dict(slug=slug, label=label, brand=label.split(' ')[0], price=int(live.get(slug, {}).get('price') or re.search(r'racket-price">(\d+)', c).group(1)),
                        img=re.search(r'<img class="racket-photo" src="([^"]+)"', c).group(1), **SPECS[slug]))
    return out

def picks(rs):
    """Profile -> rackets. Rules only use the spec sheet; each racket appears once; brands in turn starting with Wilson, cheapest first."""
    order = lambda r: (BRANDS.index(r['brand']) if r['brand'] in BRANDS else 9, r['price'])
    used, res = set(), {}
    rules = [('beg', lambda r: r['level'] == 'Amateur' or r['hard'] == 'Weich'),
             ('ctl', lambda r: r['shape'] == 'Rund'),
             ('all', lambda r: r['shape'] == 'Träne'),
             ('pow', lambda r: r['shape'] == 'Diamant')]
    for key, rule in rules:
        pool = [r for r in sorted(rs, key=order) if rule(r) and r['slug'] not in used]
        mixed = []                                    # brands in turn (Wilson, Babolat, Siux, Wilson, ...), so no profile shows one brand only
        while pool and len(mixed) < PER:
            for b in BRANDS:
                nxt = next((r for r in pool if r['brand'] == b), None)
                if nxt and len(mixed) < PER: mixed.append(nxt); pool.remove(nxt)
        res[key] = mixed
        used |= {r['slug'] for r in res[key]}
    return res

FINDER_CSS = """<style id="rg-finder-css">
.rg-finder{padding:0; position:relative; z-index:3;}
.rg-card{margin-top:-56px; background:#fff; border-radius:28px; padding:26px 28px; box-shadow:0 18px 44px rgba(11,26,43,.2);}
.rg-card h2{margin:0 0 4px; color:#0077de; letter-spacing:-.02em;}
.rg-card > p{margin:0 0 18px; color:#0b1a2b;}
.rg-qs{display:flex; gap:18px 28px; flex-wrap:wrap;}
.rg-group{display:flex; flex-direction:column; gap:8px; min-width:0;}
.rg-label{margin:0; font-size:.95rem; font-weight:700; color:#4c5d70;}
.rg-pills{display:flex; gap:8px; flex-wrap:wrap;}
.rg-pill{font:inherit; font-size:1rem; font-weight:700; color:#0b1a2b; background:#fff; border:2px solid #c9d3de; border-radius:999px; padding:11px 18px; min-height:48px; cursor:pointer; transition:background .15s, border-color .15s, color .15s;}
.rg-pill:hover{border-color:#0077de;}
.rg-pill[aria-pressed="true"]{background:#0077de; border-color:#0077de; color:#fff;}
.rg-pill:focus-visible{outline:3px solid #0077de; outline-offset:3px;}
.rg-res-h{margin:24px 0 12px; font-size:1.15rem; color:#0b1a2b;}
.rg-res{display:grid; grid-template-columns:repeat(3,1fr); gap:14px;}
.rg-item{display:flex; flex-direction:column; gap:6px; background:#eef4fa; border-radius:20px; padding:14px; color:#0b1a2b;}
.rg-item img{width:100%; aspect-ratio:1/1; object-fit:contain; background:#fff; border-radius:14px;}
.rg-item b{font-size:1.05rem; line-height:1.25;}
.rg-item span{font-size:.95rem; color:#4c5d70;}
.rg-item strong{font-size:1.15rem;}
.rg-acts{display:flex; gap:8px; flex-wrap:wrap; margin-top:auto; padding-top:6px;}
.rg-acts a{flex:1 1 auto; text-align:center; font-weight:700; font-size:1rem; border-radius:999px; padding:11px 14px; min-height:48px; box-sizing:border-box; text-decoration:none; display:flex; align-items:center; justify-content:center;}
.rg-acts .rg-test{background:#6ffd1d; color:#0b1a2b;}
.rg-acts .rg-view{background:#fff; color:#0077de; border:2px solid #0077de;}
@media (max-width:760px){
  .rg-card{margin-top:-28px; padding:20px 16px; border-radius:22px;}
  .rg-qs{flex-direction:column;}
  .rg-pill{flex:1 1 auto; padding:11px 12px;}
  .rg-res{grid-template-columns:1fr;}
  .rg-item{display:grid; grid-template-columns:96px 1fr; column-gap:12px; align-items:start;}
  .rg-item img{grid-row:1 / span 4;}
  .rg-acts{grid-column:1 / -1;}
}
@media (prefers-reduced-motion:reduce){ .rg-pill{transition:none;} }
</style>
"""

FINDER_JS = """<script id="rg-finder-js">
(function(){
  var box=document.querySelector('[data-rg-finder]'); if(!box) return;
  var D=JSON.parse(document.getElementById('rg-data').textContent), R=D.rackets, T=D.t, out=box.querySelector('.rg-res');
  var BR=['Wilson','Babolat','Siux'];
  function score(r,a){
    var s=0, near={ctl:{Rund:4,'Träne':1},all:{'Träne':4,Rund:1,Diamant:1},pow:{Diamant:4,'Träne':1}}[a.style];
    s+=near[r.shape]||0;
    if(a.level==='new'){ s+=(r.level==='Amateur'?3:0)+(r.hard==='Weich'?2:0)-(r.hard==='Hart'?3:0)-(r.level==='Profi'?2:0); }
    if(a.level==='reg'){ s+=(r.level==='Fortgeschritten'?2:0)+(r.level==='Amateur'?1:0); }
    if(a.level==='pro'){ s+=(r.level==='Profi'?3:0)+(r.level==='Fortgeschritten'?1:0)+(r.hard==='Hart'?1:0); }
    if(a.arm==='yes'){ s+=(r.hard==='Weich'?2:0)+(r.hard==='Mittel'?1:0)-(r.hard==='Hart'?4:0); }
    return s;
  }
  function esc(x){return String(x).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
  function draw(){
    var a={}; box.querySelectorAll('.rg-pill[aria-pressed="true"]').forEach(function(b){a[b.dataset.k]=b.dataset.v;});
    var list=R.map(function(r){return {r:r,s:score(r,a)};}).sort(function(x,y){
      return y.s-x.s || BR.indexOf(x.r.brand)-BR.indexOf(y.r.brand) || x.r.price-y.r.price;});
    var seen={}, per={}, pick=[];   // no colour twins, at most two per brand
    list.forEach(function(x){var r=x.r, k=[r.brand,r.shape,r.hard,r.level,r.price].join('|');
      if(pick.length<3 && !seen[k] && (per[r.brand]||0)<2){seen[k]=1; per[r.brand]=(per[r.brand]||0)+1; pick.push(x);}});
    list=pick;
    out.innerHTML=list.map(function(x){var r=x.r;
      return '<div class="rg-item"><img src="'+esc(r.img)+'" alt="'+esc(r.label)+'" loading="lazy"><b>'+esc(r.label)+'</b><span>'+esc(T.spec[r.shape])+' · '+esc(T.spec[r.hard])+' · '+esc(r.weight)+' g</span><strong>'+r.price+' CHF</strong>'+
        '<div class="rg-acts"><a class="rg-test" target="_blank" rel="noopener" href="https://wa.me/'+D.wa+'?text='+encodeURIComponent(T.wa.replace('{label}',r.label))+'">'+esc(T.test)+'</a><a class="rg-view" href="rackets/'+esc(r.slug)+'.html">'+esc(T.view)+'</a></div></div>';}).join('');
  }
  box.addEventListener('click',function(e){var b=e.target.closest('.rg-pill'); if(!b) return;
    b.parentNode.querySelectorAll('.rg-pill').forEach(function(x){x.setAttribute('aria-pressed', x===b?'true':'false');}); draw();});
  draw();
  // Live-Bestand wie im Shop: ausverkaufte Schläger verschwinden, Preise werden nachgezogen
  if(D.stock) fetch(D.stock).then(function(r){return r.json();}).then(function(j){
    if(!j||!j.ok||!j.rackets) return;
    R=R.filter(function(r){var i=j.rackets[r.slug]; if(i&&i.price) r.price=i.price; return !i||i.qty>0;});
    draw();
    document.querySelectorAll('.similar-card[data-rg]').forEach(function(a){var i=j.rackets[a.dataset.rg]; if(!i) return;
      if(!(i.qty>0)){var g=a.parentNode; a.remove(); if(!g.children.length){var sec=g.closest('section'); if(sec) sec.hidden=true;}}
      else if(i.price){var p=a.querySelector('strong'); if(p) p.textContent=i.price+' CHF';}});
  }).catch(function(){});
})();
</script>
"""

def finder(t, rs, stock=''):
    """Interactive picker (Guti 25.11.2026): three questions as pills like the booking block on the home page, three rackets as result.
    The static sections below stay for Google and AI assistants, which read text, not buttons."""
    f = t['fd']; keys = ['level', 'style', 'arm']; first = {'level': 'new', 'style': 'all', 'arm': 'no'}
    groups = ''.join(
        f'<div class="rg-group"><p class="rg-label" id="rg-{k}">{q}</p><div class="rg-pills" role="group" aria-labelledby="rg-{k}">'
        + ''.join(f'<button type="button" class="rg-pill" aria-pressed="{"true" if v == first[k] else "false"}" data-k="{k}" data-v="{v}">{lab}</button>' for v, lab in opts)
        + '</div></div>' for k, (q, opts) in zip(keys, f['q']))
    data = dict(wa=WA, stock=stock, t=dict(spec=t['spec'], view=f['view'], test=f['test'], wa=f['wa']),
                rackets=[{k: r[k] for k in ('slug', 'label', 'brand', 'price', 'img', 'shape', 'hard', 'level', 'weight')} for r in rs])
    return f'''
<section class="rg-finder" id="finder">
  <div class="wrap">
    <div class="rg-card" data-rg-finder>
      <h2>{f['h']}</h2>
      <p>{f['p']}</p>
      <div class="rg-qs">{groups}</div>
      <h3 class="rg-res-h">{f['res']}</h3>
      <div class="rg-res" aria-live="polite"></div>
    </div>
  </div>
</section>
<script type="application/json" id="rg-data">{json.dumps(data, ensure_ascii=False).replace('</', '<\\\\/')}</script>
'''

def body(t, pre, rs, stock=''):
    wa = 'https://wa.me/' + WA + '?text=' + urllib.parse.quote(t['wa'])
    pk = picks(rs)
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in t['chips'])
    flow = ''.join(f'<div class="kb-step"><span class="kb-badge">{a}</span><h3>{h}</h3><p>{p}</p></div>' for a, h, p in t['flow'])
    facts = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['facts'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    card = lambda r: (f'<a class="similar-card" data-rg="{r["slug"]}" href="rackets/{r["slug"]}.html"><img src="{r["img"]}" alt="{html.escape(r["label"])}" loading="lazy">'
                      f'<span>{html.escape(r["label"])}</span><span>{t["spec"][r["shape"]]} · {t["spec"][r["hard"]]} · {r["weight"]} g</span><strong>{r["price"]} CHF</strong></a>')
    profs = ''.join(f'''
<section class="co2-sec" id="{key}">
  <div class="wrap">
    <h2 class="co2-h">{h}</h2>
    <p class="pb-intro">{p}</p>
    <div class="similar-grid">{''.join(card(r) for r in pk[key])}</div>
  </div>
</section>
''' for key, h, p in t['prof'] if pk[key])
    return f'''
<section class="spa-hero co-hero kb-hero" style="background-image:url('{BASE + IMG}'); background-position:center 35%;">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="spa-chips">{chips}</div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="shop.html#rackets">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="{wa}" target="_blank" rel="noopener">{t['cta2']}</a>
    </div>
  </div>
</section>
{finder(t, rs, stock)}
<section class="co2-sec kb-flow-sec" id="how">
  <div class="wrap">
    <h2 class="co2-h">{t['flow_h']}</h2>
    <div class="kb-flow">{flow}</div>
  </div>
</section>
{profs}
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
      <a class="btn btn-green spa-cta" href="shop.html#rackets">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>

'''

for lang, t in T.items():
    pre = '' if lang == 'en' else '../'
    d = '' if lang == 'en' else lang + '/'
    url = BASE + d + SLUG
    rs = rackets(open(d + 'shop.html').read())
    pk = picks(rs)
    lo, hi = min(r['price'] for r in rs), max(r['price'] for r in rs)
    beg = ', '.join(r['label'] for r in pk['beg'][:2])
    t['faq'] = [(q, a.format(lo=lo, hi=hi, beg=beg)) for q, a in t['faq']]
    s = open(d + 'spa-and-sauna.html').read()
    a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
    b = s.index('<footer')
    head, tail = s[:a], s[b:]
    head = head.replace('spa-and-sauna.html', SLUG).replace(f'href="{SLUG}" class="active"', 'href="spa-and-sauna.html"')   # canonical/hreflang/lang menu -> this page; nav Spa link stays
    s = head + body(t, pre, rs, stock_url(open(d + 'shop.html').read())) + tail
    s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>' + t['title'] + '</title>', s, count=1, flags=re.S)
    esc = lambda x: x.replace('"', '&quot;')
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + esc(t['desc']) + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + esc(t['title']) + '"', s)
    s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="' + BASE + IMG + '"', s)
    ld = {'@context': 'https://schema.org', '@graph': [
      {'@type': 'ItemList', 'name': t['h1'], 'url': url,
       'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': r['label'], 'url': BASE + d + 'rackets/' + r['slug'] + '.html'}
                           for i, r in enumerate(x for key, _, _ in t['prof'] for x in pk[key])]},
      {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}]}
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-rg">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
    s = s.replace('class="active"', '')
    s = s.replace('</head>', FINDER_CSS + '</head>', 1).replace('</body>', FINDER_JS + '</body>', 1)
    open(d + SLUG, 'w').write(s)
    print(d + SLUG, len(t['title']), len(t['desc']), {k: [r['slug'] for r in v] for k, v in pk.items()} if lang == 'en' else '')
