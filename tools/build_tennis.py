"""Tennis landing page (EN/FR/DE): tennis.html, built from the spa page shell (like build_pickleball.py).
Facts (Phil 21.11.2026): indoor tennis in Salgesch only (none in Sion), from 15 CHF p.p., 20 min from Sion, 20 min from Visp;
goal: be found for tennis everywhere between Sion and Brig. 2 indoor courts as in our Playtomic club text.
Rerun: python3 tools/build_tennis.py (from repo root), then tools/ux_nav.py."""
import re, json, urllib.parse
SLUG = 'tennis.html'
BASE = 'https://www.racketsacademy.ch/'
PT = 'https://playtomic.com/clubs/rackets-academy-salgesch'
WA_SA = '41772780115'
IMG = 'images/photos/tennis-lesson.jpg'
T = {
'en': dict(title='Indoor tennis Valais – courts between Sion and Brig | Rackets Academy',
  desc='Indoor tennis in Valais: 2 covered courts in Salgesch, 5 min from Sierre, 20 min from Sion and Visp, 30 min from Brig. From 15 CHF per person, book online, open daily 7:00–23:30.',
  kicker='Tennis Valais · Salgesch', h1='Indoor tennis in Valais — between Sion and Brig.',
  lede='Two covered courts in Salgesch, playable all year whatever the weather. 5 min from Sierre, 20 min from Sion, 20 min from Visp.',
  chips=['From 15 CHF p.p.', '2 indoor courts', 'Daily 7:00–23:30', 'Book online'],
  cta='Book a tennis court', cta2='How to get here', wa='Hola! I have a question about tennis in Salgesch.',
  near_h='Close to you, wherever you are in Valais', near_p='Salgesch sits right on the language border, easy to reach by road and by train (Salgesch station). That makes it the indoor tennis hall for the whole stretch from Sion to Brig.',
  near=[('Sierre', '5 min'), ('Leuk', '10 min'), ('Sion', '20 min'), ('Visp', '20 min'), ('Brig', '30 min')],
  flow_h='How it works', flow=[('1', 'Book on Playtomic', 'Choose «Rackets Academy Salgesch», pick tennis and your time. No membership needed.'),
     ('2', 'Come and play', 'Free parking at the door, changing rooms and showers on site.'),
     ('3', 'Stay a while', 'Bar with pizzas and snacks, and a spa with sauna, hammam and jacuzzi in the same building.')],
  facts_h='Good to know', facts=[('📍', 'Where', 'Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch. Tennis is only in Salgesch, not at our Sion site.'),
     ('💰', 'Prices', 'From 15 CHF per person. You pay online when you book. Free cancellation up to 24 h before.'),
     ('☔', 'All year, any weather', 'Both courts are indoors. Open every day from 7:00 to 23:30, Sundays included.')],
  faq_h='Tennis questions', faq=[('Where can I play indoor tennis in Valais?', 'At Rackets Academy in Salgesch: 2 indoor tennis courts, open daily 7:00–23:30, 5 minutes from Sierre, 20 from Sion and Visp, 30 from Brig. Book online on Playtomic.'),
     ('How much does a tennis court cost?', 'From 15 CHF per person. You see the exact price for your time slot when you book.'),
     ('Do I need to be a club member?', 'No. Anyone can book a court online, there is no membership or annual fee.'),
     ('Is there tennis at Rackets Academy in Sion?', 'No. Our Sion site has padel only. The tennis courts are in Salgesch, 20 minutes from Sion.'),
     ('Is there an indoor tennis hall near Visp or Brig?', 'Yes, Salgesch is 20 minutes from Visp and 30 minutes from Brig.'),
     ('Can I play in the evening or on Sunday?', 'Yes. The hall is open every day from 7:00 to 23:30.')],
  more_h='More at Rackets Academy', more=[('🎾', 'Padel', 'The biggest padel centre in Valais.', 'index.html'), ('🏓', 'Pickleball', '3 indoor courts in the same hall.', 'pickleball.html'), ('🧖', 'Spa & sauna', 'Sauna, hammam and jacuzzi after the match.', 'spa-and-sauna.html')],
  final_h='Fancy a set?', final_p='Salgesch · 2 indoor courts · daily 7:00–23:30'),
'fr': dict(title='Tennis indoor Valais – courts couverts entre Sion et Brigue | Rackets Academy',
  desc='Tennis indoor en Valais : 2 courts couverts à Salgesch, à 5 min de Sierre, 20 min de Sion et de Viège, 30 min de Brigue. Dès 15 CHF par personne, réservation en ligne, ouvert tous les jours de 7h à 23h30.',
  kicker='Tennis Valais · Salgesch', h1='Le tennis indoor en Valais — entre Sion et Brigue.',
  lede='Deux courts couverts à Salgesch, jouables toute l’année par tous les temps. À 5 min de Sierre, 20 min de Sion, 20 min de Viège.',
  chips=['Dès 15 CHF p.p.', '2 courts couverts', 'Tous les jours 7h–23h30', 'Réservation en ligne'],
  cta='Réserver un court de tennis', cta2='Comment venir', wa='Hola ! J’ai une question sur le tennis à Salgesch.',
  near_h='Près de chez toi, où que tu sois en Valais', near_p='Salgesch se trouve sur la frontière des langues, facile d’accès par la route et en train (gare de Salgesch). C’est la halle de tennis pour tout le tronçon de Sion à Brigue.',
  near=[('Sierre', '5 min'), ('Loèche', '10 min'), ('Sion', '20 min'), ('Viège', '20 min'), ('Brigue', '30 min')],
  flow_h='Comment ça marche', flow=[('1', 'Réserve sur Playtomic', 'Choisis «Rackets Academy Salgesch», puis tennis et ton horaire. Pas besoin d’être membre.'),
     ('2', 'Viens jouer', 'Parking gratuit devant la porte, vestiaires et douches sur place.'),
     ('3', 'Reste un moment', 'Bar avec pizzas et snacks, et spa avec sauna, hammam et jacuzzi dans le même bâtiment.')],
  facts_h='Bon à savoir', facts=[('📍', 'Où', 'Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch. Le tennis est seulement à Salgesch, pas sur notre site de Sion.'),
     ('💰', 'Tarifs', 'Dès 15 CHF par personne. Tu paies en ligne à la réservation. Annulation gratuite jusqu’à 24 h avant.'),
     ('☔', 'Toute l’année, par tous les temps', 'Les deux courts sont couverts. Ouvert tous les jours de 7h à 23h30, dimanche compris.')],
  faq_h='Questions sur le tennis', faq=[('Où jouer au tennis indoor en Valais ?', 'À la Rackets Academy de Salgesch : 2 courts de tennis couverts, ouverts tous les jours de 7h à 23h30, à 5 minutes de Sierre, 20 de Sion et de Viège, 30 de Brigue. Réservation en ligne sur Playtomic.'),
     ('Combien coûte un court de tennis ?', 'Dès 15 CHF par personne. Le prix exact de ton créneau s’affiche à la réservation.'),
     ('Faut-il être membre d’un club ?', 'Non. Tout le monde peut réserver un court en ligne, sans abonnement ni cotisation annuelle.'),
     ('Y a-t-il du tennis à la Rackets Academy de Sion ?', 'Non. Notre site de Sion propose uniquement du padel. Les courts de tennis sont à Salgesch, à 20 minutes de Sion.'),
     ('Y a-t-il une halle de tennis près de Viège ou de Brigue ?', 'Oui, Salgesch est à 20 minutes de Viège et à 30 minutes de Brigue.'),
     ('Peut-on jouer le soir ou le dimanche ?', 'Oui. La halle est ouverte tous les jours de 7h à 23h30.')],
  more_h='Aussi à la Rackets Academy', more=[('🎾', 'Padel', 'Le plus grand centre de padel du Valais.', 'index.html'), ('🏓', 'Pickleball', '3 courts indoor dans la même halle.', 'pickleball.html'), ('🧖', 'Spa & sauna', 'Sauna, hammam et jacuzzi après le match.', 'spa-and-sauna.html')],
  final_h='Envie d’un set ?', final_p='Salgesch · 2 courts couverts · tous les jours 7h–23h30'),
'de': dict(title='Tennishalle Wallis – Indoor-Tennis zwischen Sion und Brig | Rackets Academy',
  desc='Tennishalle im Wallis: 2 Hallenplätze in Salgesch, 5 Min. ab Siders, 20 Min. ab Sion und Visp, 30 Min. ab Brig. Ab 15 CHF pro Person, online buchen, täglich 07:00–23:30 offen.',
  kicker='Tennis Wallis · Salgesch', h1='Tennishalle im Wallis — zwischen Sion und Brig.',
  lede='Zwei Hallenplätze in Salgesch, das ganze Jahr und bei jedem Wetter bespielbar. 5 Min. ab Siders, 20 Min. ab Sion, 20 Min. ab Visp.',
  chips=['Ab 15 CHF p.P.', '2 Hallenplätze', 'Täglich 07:00–23:30', 'Online buchen'],
  cta='Tennisplatz buchen', cta2='So kommst du hin', wa='Hola! Ich habe eine Frage zu Tennis in Salgesch.',
  near_h='In deiner Nähe, egal wo im Wallis', near_p='Salgesch liegt an der Sprachgrenze und ist mit Auto und Zug (Bahnhof Salgesch) gut erreichbar. Damit ist es die Tennishalle für die ganze Strecke von Sion bis Brig.',
  near=[('Siders', '5 Min.'), ('Leuk', '10 Min.'), ('Sion', '20 Min.'), ('Visp', '20 Min.'), ('Brig', '30 Min.')],
  flow_h='So funktioniert es', flow=[('1', 'Auf Playtomic buchen', '«Rackets Academy Salgesch» wählen, dann Tennis und deine Zeit. Keine Mitgliedschaft nötig.'),
     ('2', 'Kommen und spielen', 'Gratis-Parkplätze vor der Tür, Garderoben und Duschen vor Ort.'),
     ('3', 'Noch etwas bleiben', 'Bar mit Pizzas und Snacks, Spa mit Sauna, Hammam und Whirlpool im gleichen Gebäude.')],
  facts_h='Gut zu wissen', facts=[('📍', 'Wo', 'Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch. Tennis gibt es nur in Salgesch, nicht an unserem Standort Sion.'),
     ('💰', 'Preise', 'Ab 15 CHF pro Person. Du bezahlst online bei der Buchung. Kostenlos stornieren bis 24 Std. vorher.'),
     ('☔', 'Ganzjährig, bei jedem Wetter', 'Beide Plätze sind in der Halle. Täglich von 07:00 bis 23:30 offen, auch am Sonntag.')],
  faq_h='Fragen zu Tennis', faq=[('Wo gibt es im Wallis eine Tennishalle?', 'In der Rackets Academy in Salgesch: 2 Hallenplätze, täglich 07:00–23:30, 5 Minuten ab Siders, 20 ab Sion und Visp, 30 ab Brig. Online buchen auf Playtomic.'),
     ('Was kostet ein Tennisplatz?', 'Ab 15 CHF pro Person. Den genauen Preis für deine Zeit siehst du bei der Buchung.'),
     ('Muss ich Clubmitglied sein?', 'Nein. Jeder kann online einen Platz buchen, ohne Mitgliedschaft und ohne Jahresbeitrag.'),
     ('Gibt es Tennis in der Rackets Academy in Sion?', 'Nein. An unserem Standort Sion gibt es nur Padel. Die Tennisplätze sind in Salgesch, 20 Minuten von Sion.'),
     ('Gibt es eine Tennishalle in der Nähe von Visp oder Brig?', 'Ja, Salgesch liegt 20 Minuten von Visp und 30 Minuten von Brig.'),
     ('Kann ich abends oder am Sonntag spielen?', 'Ja. Die Halle ist täglich von 07:00 bis 23:30 offen.')],
  more_h='Mehr in der Rackets Academy', more=[('🎾', 'Padel', 'Das grösste Padelzentrum im Wallis.', 'index.html'), ('🏓', 'Pickleball', '3 Indoor-Plätze in der gleichen Halle.', 'pickleball.html'), ('🧖', 'Spa & Sauna', 'Sauna, Hammam und Whirlpool nach dem Spiel.', 'spa-and-sauna.html')],
  final_h='Lust auf einen Satz?', final_p='Salgesch · 2 Hallenplätze · täglich 07:00–23:30'),
}

def body(t, pre):
    wa = 'https://wa.me/' + WA_SA + '?text=' + urllib.parse.quote(t['wa'])
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in t['chips'])
    near = ''.join(f'<div class="tn-near"><b>{m}</b><span>{p}</span></div>' for p, m in t['near'])
    flow = ''.join(f'<div class="kb-step"><span class="kb-badge">{a}</span><h3>{h}</h3><p>{p}</p></div>' for a, h, p in t['flow'])
    facts = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['facts'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    more = ''.join(f'<a class="co2-b ow-more" href="{l}"><span class="co2-ic">{e}</span><h3>{h} →</h3><p>{p}</p></a>' for e, h, p, l in t['more'])
    return f'''
<section class="spa-hero co-hero kb-hero" style="background-image:url('{BASE + IMG}'); background-position:center 35%;">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="spa-chips">{chips}</div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="{PT}" target="_blank" rel="noopener">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="#near">{t['cta2']}</a>
    </div>
  </div>
</section>

<section class="co2-sec" id="near">
  <div class="wrap">
    <h2 class="co2-h">{t['near_h']}</h2>
    <p class="pb-intro">{t['near_p']}</p>
    <div class="tn-nears">{near}</div>
  </div>
</section>

<section class="co2-sec kb-flow-sec" id="how">
  <div class="wrap">
    <h2 class="co2-h">{t['flow_h']}</h2>
    <div class="kb-flow">{flow}</div>
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

<section class="co2-sec">
  <div class="wrap">
    <h2 class="co2-h">{t['more_h']}</h2>
    <div class="co2-bens ow-mores kc-mores">{more}</div>
  </div>
</section>

<section class="spa-final kb-final" style="background-image:url('{pre}images/coaching/coaching-6.webp');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-final-inner">
    <h2>{t['final_h']}</h2>
    <p>{t['final_p']}</p>
    <div class="hero-actions" style="justify-content:center;">
      <a class="btn btn-green spa-cta" href="{PT}" target="_blank" rel="noopener">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>

'''

for lang, t in T.items():
    pre = '' if lang == 'en' else '../'
    d = '' if lang == 'en' else lang + '/'
    url = BASE + d + SLUG
    s = open(d + 'spa-and-sauna.html').read()
    a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
    b = s.index('<footer')
    head, tail = s[:a], s[b:]
    head = head.replace('spa-and-sauna.html', SLUG).replace(f'href="{SLUG}" class="active"', 'href="spa-and-sauna.html"')   # canonical/hreflang/lang menu -> this page; nav Spa link stays
    s = head + body(t, pre) + tail
    s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>' + t['title'] + '</title>', s, count=1, flags=re.S)
    esc = lambda x: x.replace('"', '&quot;')
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + esc(t['desc']) + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + esc(t['title']) + '"', s)
    s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="' + BASE + IMG + '"', s)
    ld = {'@context': 'https://schema.org', '@graph': [
      {'@type': 'SportsActivityLocation', 'name': 'Rackets Academy Salgesch – Tennis', 'url': url, 'telephone': '+41772780115', 'image': BASE + IMG, 'sport': 'Tennis',
       'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressRegion': 'VS', 'addressCountry': 'CH'},
       'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '07:00', 'closes': '23:30'}],
       'areaServed': ['Sierre', 'Siders', 'Sion', 'Sitten', 'Leuk', 'Loèche', 'Crans-Montana', 'Visp', 'Viège', 'Brig', 'Brigue', 'Valais', 'Wallis']},
      {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}]}
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-tn">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
    s = s.replace('class="active"', '')
    open(d + SLUG, 'w').write(s)
    print(d + SLUG, len(t['title']), len(t['desc']))
