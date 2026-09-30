"""Rebuilds the main content of spa-and-sauna.html (EN/FR/DE)."""
import re, urllib.parse
PT = 'https://playtomic.com/clubs/rackets-academy-salgesch'
WA = 'https://wa.me/41772780115?text='
T = {
'en': dict(
  title='Spa & Sauna Salgesch · near Sierre, Sion, Crans-Montana',
  desc='Sauna, hammam & jacuzzi in Salgesch – 10 min from Sierre, 20 min from Crans-Montana, 25 min from Sion. From 25 CHF, daily 14:00–22:00.',
  kicker='Spa & Sauna · Salgesch', h1='Grey outside? Warm inside.',
  lede='Finnish sauna, bio-sauna, hammam and jacuzzi right next to our courts — your escape after the slopes, on foggy autumn days or after your match.',
  chips=['From 25 CHF', 'Daily 14:00–22:00', 'Book in 1 minute'],
  cta='Book your spa time', cta2='Private spa for your group',
  moments_h='Made for days like these',
  moments=[('⛷️','After the slopes','Heavy legs after skiing? 80 °C in the Finnish sauna and the bubbles of the jacuzzi loosen everything up.'),
           ('🌫️','Grey autumn days','When the fog sits in the valley, bring the warmth in: an evening of sweating, steaming and switching off.'),
           ('🎾','After your match','The spa is right next to the courts. Shower, sauna, jacuzzi — the best recovery there is.')],
  inside_h="What's waiting for you",
  gallery=[('spa-sauna','Finnish sauna · 80 °C'),('spa-area','Jacuzzi & spa area'),('spa-relax','Relaxation room'),('spa-shower','Hot & cold rain shower')],
  facilities=['Finnish sauna · 80 °C','Bio-sauna · 65 °C','Hammam (steam bath)','Jacuzzi','Two foot baths','Relaxation room','Hot & cold rain shower'],
  ritual_h='Your spa ritual', ritual_sub='Our tip for the perfect evening — repeat 2–3 rounds.',
  ritual=[('Warm up','Start gently in the bio-sauna at 65 °C or the hammam.'),('Heat','Move on to the Finnish sauna at 80 °C for 8–12 minutes.'),('Cool down','Cold rain shower and a warm foot bath.'),('Relax','Jacuzzi, then lie back in the relaxation room.')],
  private_h='Private spa for your group', private_p='Book the whole spa for 2 hours for up to 8 people — 120 CHF, that is from 15 CHF per person. Perfect for birthdays, team evenings or a girls’ night after skiing.',
  private_cta='Request private spa', private_wa='Hola! I would like to book the private spa (2h, max 8 people). Date: ',
  prices_h='Prices & memberships', scroll='↔ Scroll to see all prices',
  rows=[('1 entry','25 CHF'),('Private spa 2h (max 8 people)','120 CHF'),('10+1 entries','250 CHF'),('1 month','150 CHF'),('3 months','130 CHF / month'),('6 months','100 CHF / month'),('12 months','80 CHF / month')],
  prices_note='Single entries and 10+1 packs are booked on Playtomic. Monthly, quarterly and yearly memberships are set up at the club — message us on WhatsApp.',
  member_cta='Membership on WhatsApp', member_wa='Hola! I am interested in a spa membership.',
  near_h='Just around the corner', near_p='Our spa is in Salgesch, right between Sierre and the Leuk region — quick to reach after a ski day or from anywhere in Central Valais.',
  near=[('Sierre','≈ 10 min'),('Crans-Montana','≈ 20 min'),('Sion','≈ 25 min'),('Leuk','≈ 10 min')],
  faq_h='Good to know',
  faq=[('Is there a sauna near Crans-Montana?','Yes — our spa in Salgesch is about 20 minutes by car from Crans-Montana. Ideal after a day on the slopes: Finnish sauna, bio-sauna, hammam and jacuzzi from 25 CHF.'),
       ('Where can I go to the sauna near Sierre or Sion?','Rackets Academy Spa is in Salgesch, about 10 minutes from Sierre and 25 minutes from Sion. Open daily 14:00–22:00, book your entry on Playtomic.'),
       ('Can I book the spa privately?','Yes. You can privatise the whole spa for 2 hours for up to 8 people for 120 CHF — perfect for birthdays or team evenings.')],
  final_h='Your warm-up is waiting.', final_p='Open daily 14:00–22:00 · Littenstrasse 30, 3970 Salgesch'),
'fr': dict(
  title='Spa & sauna Salgesch · près de Sierre, Sion, Crans-Montana',
  desc='Sauna, hammam et jacuzzi à Salgesch – à 10 min de Sierre, 20 min de Crans-Montana, 25 min de Sion. Dès 25 CHF, tous les jours 14h–22h.',
  kicker='Spa & Sauna · Salgesch', h1='Gris dehors ? Chaud dedans.',
  lede='Sauna finlandais, bio-sauna, hammam et jacuzzi juste à côté de nos terrains — ton refuge après les pistes, les jours de brouillard ou après ton match.',
  chips=['Dès 25 CHF', 'Tous les jours 14h–22h', 'Réservé en 1 minute'],
  cta='Réserver mon spa', cta2='Spa privé pour ton groupe',
  moments_h='Fait pour des jours comme ça',
  moments=[('⛷️','Après les pistes','Les jambes lourdes après le ski ? 80 °C au sauna finlandais et les bulles du jacuzzi détendent tout.'),
           ('🌫️',"Journées grises d'automne","Quand le brouillard reste dans la vallée, fais entrer la chaleur : une soirée pour transpirer, se détendre et décrocher."),
           ('🎾','Après ton match','Le spa est juste à côté des terrains. Douche, sauna, jacuzzi — la meilleure récupération qui soit.')],
  inside_h="Ce qui t'attend",
  gallery=[('spa-sauna','Sauna finlandais · 80 °C'),('spa-area','Jacuzzi & espace spa'),('spa-relax','Salle de repos'),('spa-shower','Douche pluie chaude & froide')],
  facilities=['Sauna finlandais · 80 °C','Bio-sauna · 65 °C','Hammam (bain de vapeur)','Jacuzzi','Deux bains de pieds','Salle de repos','Douche pluie chaude & froide'],
  ritual_h='Ton rituel spa', ritual_sub='Notre conseil pour une soirée parfaite — à répéter 2–3 fois.',
  ritual=[('Se réchauffer','Commence en douceur au bio-sauna à 65 °C ou au hammam.'),('Transpirer','Passe au sauna finlandais à 80 °C pendant 8–12 minutes.'),('Se rafraîchir','Douche pluie froide et bain de pieds chaud.'),('Se détendre','Jacuzzi, puis repos dans la salle de relaxation.')],
  private_h='Spa privé pour ton groupe', private_p="Réserve tout le spa pendant 2 heures pour 8 personnes max — 120 CHF, soit dès 15 CHF par personne. Idéal pour un anniversaire, une soirée d'équipe ou entre amies après le ski.",
  private_cta='Demander le spa privé', private_wa="Hola ! J'aimerais réserver le spa privé (2h, 8 personnes max). Date : ",
  prices_h='Prix & abonnements', scroll='↔ Faire défiler pour voir tous les prix',
  rows=[('1 entrée','25 CHF'),('Spa privé 2h (8 pers. max)','120 CHF'),('10+1 entrées','250 CHF'),('1 mois','150 CHF'),('3 mois','130 CHF / mois'),('6 mois','100 CHF / mois'),('12 mois','80 CHF / mois')],
  prices_note="Les entrées simples et les packs 10+1 se réservent sur Playtomic. Les abonnements mensuels, trimestriels et annuels se font au club — écris-nous sur WhatsApp.",
  member_cta='Abonnement via WhatsApp', member_wa="Hola ! Je suis intéressé(e) par un abonnement spa.",
  near_h='Tout près de chez toi', near_p="Notre spa se trouve à Salgesch, entre Sierre et la région de Loèche — vite accessible après une journée de ski ou depuis tout le Valais central.",
  near=[('Sierre','≈ 10 min'),('Crans-Montana','≈ 20 min'),('Sion','≈ 25 min'),('Loèche','≈ 10 min')],
  faq_h='Bon à savoir',
  faq=[('Y a-t-il un sauna près de Crans-Montana ?',"Oui — notre spa à Salgesch est à environ 20 minutes en voiture de Crans-Montana. Idéal après les pistes : sauna finlandais, bio-sauna, hammam et jacuzzi dès 25 CHF."),
       ('Où aller au sauna près de Sierre ou de Sion ?',"Le spa de la Rackets Academy est à Salgesch, à environ 10 minutes de Sierre et 25 minutes de Sion. Ouvert tous les jours de 14h à 22h, réservation sur Playtomic."),
       ('Peut-on privatiser le spa ?',"Oui. Tu peux privatiser tout le spa pendant 2 heures pour 8 personnes max pour 120 CHF — idéal pour un anniversaire ou une soirée d'équipe.")],
  final_h="Ta pause chaleur t'attend.", final_p='Tous les jours 14h–22h · Littenstrasse 30, 3970 Salgesch'),
'de': dict(
  title='Spa & Sauna Salgesch · bei Siders, Sitten, Crans-Montana',
  desc='Sauna, Hammam & Jacuzzi in Salgesch – 10 Min. von Siders, 20 Min. von Crans-Montana, 25 Min. von Sitten. Ab 25 CHF, täglich 14–22 Uhr.',
  kicker='Spa & Sauna · Salgesch', h1='Grau draussen? Warm drinnen.',
  lede='Finnische Sauna, Bio-Sauna, Hammam und Jacuzzi direkt neben unseren Plätzen — dein Rückzugsort nach der Piste, an nebligen Herbsttagen oder nach dem Match.',
  chips=['Ab 25 CHF', 'Täglich 14–22 Uhr', 'In 1 Minute gebucht'],
  cta='Spa-Zeit buchen', cta2='Privat-Spa für deine Gruppe',
  moments_h='Gemacht für Tage wie diese',
  moments=[('⛷️','Nach der Piste','Schwere Beine vom Skifahren? 80 °C in der finnischen Sauna und die Blubberblasen im Jacuzzi lockern alles.'),
           ('🌫️','Graue Herbsttage','Wenn der Nebel im Tal hängt, hol dir die Wärme rein: ein Abend zum Schwitzen, Dampfen und Abschalten.'),
           ('🎾','Nach dem Match','Das Spa liegt direkt neben den Plätzen. Dusche, Sauna, Jacuzzi — bessere Regeneration gibt es nicht.')],
  inside_h='Das erwartet dich',
  gallery=[('spa-sauna','Finnische Sauna · 80 °C'),('spa-area','Jacuzzi & Spa-Bereich'),('spa-relax','Ruheraum'),('spa-shower','Warm-kalte Regendusche')],
  facilities=['Finnische Sauna · 80 °C','Bio-Sauna · 65 °C','Hammam (Dampfbad)','Jacuzzi','Zwei Fussbäder','Ruheraum','Warm-kalte Regendusche'],
  ritual_h='Dein Spa-Ritual', ritual_sub='Unser Tipp für den perfekten Abend — 2–3 Runden wiederholen.',
  ritual=[('Aufwärmen','Sanft starten in der Bio-Sauna bei 65 °C oder im Hammam.'),('Schwitzen','Weiter in die finnische Sauna bei 80 °C für 8–12 Minuten.'),('Abkühlen','Kalte Regendusche und ein warmes Fussbad.'),('Entspannen','Jacuzzi, danach zurücklehnen im Ruheraum.')],
  private_h='Privat-Spa für deine Gruppe', private_p='Buch das ganze Spa für 2 Stunden für bis zu 8 Personen — 120 CHF, also ab 15 CHF pro Person. Perfekt für Geburtstage, Team-Abende oder den Mädelsabend nach dem Skitag.',
  private_cta='Privat-Spa anfragen', private_wa='Hola! Ich möchte das Privat-Spa buchen (2 Std., max. 8 Personen). Datum: ',
  prices_h='Preise & Abos', scroll='↔ Wischen für alle Preise',
  rows=[('1 Eintritt','25 CHF'),('Privat-Spa 2 Std. (max. 8 Pers.)','120 CHF'),('10+1 Eintritte','250 CHF'),('1 Monat','150 CHF'),('3 Monate','130 CHF / Monat'),('6 Monate','100 CHF / Monat'),('12 Monate','80 CHF / Monat')],
  prices_note='Einzeleintritte und 10+1-Pakete bucht ihr auf Playtomic. Monats-, Quartals- und Jahresabos richten wir im Club ein — schreib uns auf WhatsApp.',
  member_cta='Abo per WhatsApp', member_wa='Hola! Ich interessiere mich für ein Spa-Abo.',
  near_h='Gleich um die Ecke', near_p='Unser Spa liegt in Salgesch, zwischen Siders und der Region Leuk — schnell erreichbar nach dem Skitag oder aus dem ganzen Mittelwallis.',
  near=[('Siders (Sierre)','≈ 10 Min.'),('Crans-Montana','≈ 20 Min.'),('Sitten (Sion)','≈ 25 Min.'),('Leuk','≈ 10 Min.')],
  faq_h='Gut zu wissen',
  faq=[('Gibt es eine Sauna in der Nähe von Crans-Montana?','Ja — unser Spa in Salgesch liegt rund 20 Autominuten von Crans-Montana entfernt. Ideal nach dem Skitag: finnische Sauna, Bio-Sauna, Hammam und Jacuzzi ab 25 CHF.'),
       ('Wo gibt es eine Sauna bei Siders oder Sitten?','Das Spa der Rackets Academy liegt in Salgesch, rund 10 Minuten von Siders und 25 Minuten von Sitten. Täglich 14–22 Uhr geöffnet, Eintritt auf Playtomic buchen.'),
       ('Kann man das Spa privat mieten?','Ja. Du kannst das ganze Spa für 2 Stunden für bis zu 8 Personen für 120 CHF mieten — perfekt für Geburtstage oder Team-Abende.')],
  final_h='Deine Aufwärmrunde wartet.', final_p='Täglich 14–22 Uhr · Littenstrasse 30, 3970 Salgesch'),
}
def body(t, pre):
    img = lambda n: pre + 'images/spa/' + n + '.jpg'
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in t['chips'])
    moments = ''.join(f'<div class="spa-moment"><span class="spa-emoji">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['moments'])
    gal = ''.join(f'<figure class="spa-shot"><img src="{img(n + "-sm")}" srcset="{img(n + "-sm")} 700w, {img(n)} 1400w" sizes="(max-width:760px) 100vw, 50vw" alt="{c}" loading="lazy"><figcaption>{c}</figcaption></figure>' for n, c in t['gallery'])
    fac = ''.join(f'<li>{x}</li>' for x in t['facilities'])
    rit = ''.join(f'<li><span class="spa-step">{i+1}</span><div><strong>{h}</strong><p>{p}</p></div></li>' for i, (h, p) in enumerate(t['ritual']))
    rows = ''.join(f'<tr><td class="lead">{a}</td><td>{b}</td></tr>' for a, b in t['rows'])
    near = ''.join(f'<div class="spa-near-item"><strong>{c}</strong><span>{d}</span></div>' for c, d in t['near'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    pwa = WA + urllib.parse.quote(t['private_wa']); mwa = WA + urllib.parse.quote(t['member_wa'])
    return f'''
<section class="spa-hero" style="background-image:url('{img("spa-jacuzzi")}');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="spa-chips">{chips}</div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="{PT}" target="_blank" rel="noopener">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="#private">{t['cta2']}</a>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['moments_h']}</h2>
    <div class="spa-moments">{moments}</div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['inside_h']}</h2>
    <div class="spa-gallery">{gal}</div>
    <ul class="spa-facilities">{fac}</ul>
  </div>
</section>

<section class="section-tight spa-ritual-wrap">
  <div class="wrap">
    <h2>{t['ritual_h']}</h2>
    <p class="section-lede">{t['ritual_sub']}</p>
    <ol class="spa-ritual">{rit}</ol>
  </div>
</section>

<section class="section-tight" id="private">
  <div class="wrap">
    <div class="spa-private">
      <img src="{img('spa-relax-sm')}" alt="{t['gallery'][2][1]}" loading="lazy">
      <div>
        <h2>{t['private_h']}</h2>
        <p>{t['private_p']}</p>
        <a class="btn btn-green" href="{pwa}" target="_blank" rel="noopener">{t['private_cta']}</a>
      </div>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['prices_h']}</h2>
    <div class="pill-box">
      <div class="scroll-hint">{t['scroll']}</div>
      <div class="price-table-wrap">
      <table class="price-table">{rows}</table>
      </div>
    </div>
    <p style="text-align:center; margin-top:20px; font-size:0.88rem; color:#045bab;">{t['prices_note']}</p>
    <div class="hero-actions" style="justify-content:center; margin-top:14px;">
      <a class="btn btn-green" href="{PT}" target="_blank" rel="noopener">{t['cta']}</a>
      <a class="btn" style="background:var(--blue); color:#fff;" href="{mwa}" target="_blank" rel="noopener">{t['member_cta']}</a>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['near_h']}</h2>
    <p class="section-lede">{t['near_p']}</p>
    <div class="spa-near">{near}</div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['faq_h']}</h2>
    <div class="spa-faq">{faq}</div>
  </div>
</section>

<section class="spa-final" style="background-image:url('{img("spa-sauna")}');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-final-inner">
    <h2>{t['final_h']}</h2>
    <p>{t['final_p']}</p>
    <a class="btn btn-green spa-cta" href="{PT}" target="_blank" rel="noopener">{t['cta']}</a>
  </div>
</section>

'''
for lang, t in T.items():
    f = ('' if lang == 'en' else lang + '/') + 'spa-and-sauna.html'
    pre = '' if lang == 'en' else '../'
    s = open(f).read()
    a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
    b = s.index('<footer')
    s = s[:a] + body(t, pre) + s[b:]
    s = re.sub(r'<title>.*?</title>', '<title>' + t['title'] + '</title>', s, count=1, flags=re.S)
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + t['desc'] + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + t['title'] + '"', s)
    s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="https://www.racketsacademy.ch/images/spa/spa-jacuzzi.jpg"', s)
    import json
    ld = {'@context': 'https://schema.org', '@graph': [
      {'@type': 'DaySpa', 'name': 'Rackets Academy Spa & Sauna', 'url': 'https://www.racketsacademy.ch/' + ('' if lang == 'en' else lang + '/') + 'spa-and-sauna.html',
       'image': 'https://www.racketsacademy.ch/images/spa/spa-jacuzzi.jpg', 'telephone': '+41772780115', 'priceRange': 'CHF 25–120',
       'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressRegion': 'VS', 'addressCountry': 'CH'},
       'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'opens': '14:00', 'closes': '22:00'}],
       'areaServed': ['Salgesch', 'Sierre', 'Siders', 'Sion', 'Sitten', 'Crans-Montana', 'Leuk', 'Valais', 'Wallis'],
       'amenityFeature': [{'@type': 'LocationFeatureSpecification', 'name': x, 'value': True} for x in t['facilities']]},
      {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}]}
    s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-spa">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
    open(f, 'w').write(s); print(f, len(t['title']), len(t['desc']))
