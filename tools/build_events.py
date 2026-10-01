"""Company events landing page (EN/FR/DE): company-events.html, built from the spa page shell."""
import re, json, urllib.parse
WA_SA = '41772780115'
SLUG = 'company-events.html'
T = {
'en': dict(title='Company events & team building in Valais | Rackets Academy',
  desc='Team events in Salgesch & Sion: padel tournament with coaches, meeting room, paella or raclette, apéro. 2 to 6 hours, from 25 CHF per person.',
  kicker='Company events · Valais', h1='Team event with padel, food and apéro.',
  lede='From a 2-hour padel session to a full day with meeting room, lunch and apéro — in Salgesch and Sion, whatever the weather.',
  chips=['From 25 CHF per person', '2 to 6 hours', 'Indoor, all year'],
  cta='Request your event', cta2='See an example day',
  wa='Hola! We are planning a company event. Date: … · People: … · Duration: …',
  mail_sub='Company event request', mail_body='Hello,\n\nwe are planning a company event.\nDate:\nNumber of people:\nDuration (2–6 h):\nWishes (padel, meeting room, paella/raclette, apéro, overnight):\n\nThank you!',
  mods_h='Build your event',
  mods=[('🎾', 'Padel for everyone', 'Courts for your whole group, split by level, one coach per court. Mini tournament to finish.'),
        ('💼', 'Meeting room', 'Room for your workshop or presentation, before or after playing.'),
        ('☕', 'Coffee & breaks', 'Welcome coffee with pastries, coffee breaks with juice and water.'),
        ('🥘', 'Paella or raclette', 'Freshly cooked on site for your team — with soft drinks and coffee.'),
        ('🥂', 'Apéro at the bar', 'Toast on the outdoor bar — first round on the company, if you like.'),
        ('🛏️', 'Overnight stay', 'Staying longer? We organise accommodation on request.')],
  day_h='Example: team day for 30 people', day_tag='Example',
  day=[('09:00', 'Welcome coffee & pastries'), ('09:30', 'Meeting room for your team'), ('12:00', 'Paella lunch with soft drinks & coffee'),
       ('13:30', 'Padel: 5 courts, 1 coach per court, split by level'), ('15:30', 'Apéro at the outdoor bar')],
  day_price='≈ 75 CHF per person, all included',
  ref_h='They played with us', refs=['Raiffeisen', 'CSS', 'Decathlon', 'Goldavenue Genève'],
  faq_h='Good to know',
  faq=[('How long does an event last?', 'From 2 hours (padel only) up to 6 hours with meeting room, lunch and apéro. Overnight stays on request.'),
       ('Do participants need padel experience?', 'No. Our coaches split the group by level — beginners learn the basics, experienced players get a proper match.'),
       ('What does it cost?', 'From 25 CHF per person for padel. A full team day with meeting room, paella and apéro is around 75 CHF per person. We send you a tailored offer.'),
       ('Where does it take place?', 'In our padel centres in Salgesch (5 min from Sierre, 20 min from Crans-Montana) and Sion. Indoor, so the weather never cancels your event.')],
  final_h='Tell us your date — we plan the rest.', final_p='Salgesch & Sion · 2 to 6 hours · from 25 CHF per person', final_mail='Request by email'),
'fr': dict(title="Sortie d'entreprise & team building Valais | Rackets Academy",
  desc="Événements d'entreprise à Salgesch & Sion : tournoi de padel avec coachs, salle de réunion, paella ou raclette, apéro. De 2 à 6 h, dès 25 CHF par personne.",
  kicker="Événements d'entreprise · Valais", h1='Team event avec padel, repas et apéro.',
  lede="D'une séance de padel de 2 heures à une journée complète avec salle de réunion, repas et apéro — à Salgesch et Sion, quelle que soit la météo.",
  chips=['Dès 25 CHF par personne', 'De 2 à 6 heures', 'En salle, toute l’année'],
  cta='Demander une offre', cta2="Voir un exemple de journée",
  wa="Hola ! Nous préparons un événement d'entreprise. Date : … · Personnes : … · Durée : …",
  mail_sub="Demande événement d'entreprise", mail_body="Bonjour,\n\nnous préparons un événement d'entreprise.\nDate :\nNombre de personnes :\nDurée (2–6 h) :\nSouhaits (padel, salle de réunion, paella/raclette, apéro, nuitée) :\n\nMerci !",
  mods_h='Compose ton événement',
  mods=[('🎾', 'Du padel pour tous', 'Des terrains pour tout le groupe, répartis par niveau, un coach par terrain. Mini-tournoi pour finir.'),
        ('💼', 'Salle de réunion', 'Une salle pour ton atelier ou ta présentation, avant ou après le jeu.'),
        ('☕', 'Café & pauses', "Café d'accueil avec viennoiseries, pauses-café avec jus et eau."),
        ('🥘', 'Paella ou raclette', 'Cuisinée sur place pour ton équipe — avec boissons sans alcool et café.'),
        ('🥂', 'Apéro au bar', "Trinquer au bar extérieur — la première tournée offerte par l'entreprise, si tu veux."),
        ('🛏️', 'Nuitée', 'Tu restes plus longtemps ? On organise l’hébergement sur demande.')],
  day_h="Exemple : journée d'équipe pour 30 personnes", day_tag='Exemple',
  day=[('09:00', "Café d'accueil & viennoiseries"), ('09:30', 'Salle de réunion pour ton équipe'), ('12:00', 'Paella avec boissons sans alcool & café'),
       ('13:30', 'Padel : 5 terrains, 1 coach par terrain, par niveau'), ('15:30', 'Apéro au bar extérieur')],
  day_price='≈ 75 CHF par personne, tout compris',
  ref_h='Ils ont joué avec nous', refs=['Raiffeisen', 'CSS', 'Decathlon', 'Goldavenue Genève'],
  faq_h='Bon à savoir',
  faq=[('Combien de temps dure un événement ?', "De 2 heures (padel seul) jusqu'à 6 heures avec salle de réunion, repas et apéro. Nuitée sur demande."),
       ("Faut-il savoir jouer au padel ?", "Non. Nos coachs répartissent le groupe par niveau — les débutants apprennent les bases, les joueurs confirmés ont un vrai match."),
       ('Combien ça coûte ?', "Dès 25 CHF par personne pour le padel. Une journée complète avec salle, paella et apéro revient à environ 75 CHF par personne. On t’envoie une offre sur mesure."),
       ('Où cela se passe-t-il ?', 'Dans nos centres de padel à Salgesch (5 min de Sierre, 20 min de Crans-Montana) et à Sion. En salle, la météo ne gâche jamais ton événement.')],
  final_h='Donne-nous ta date — on s’occupe du reste.', final_p='Salgesch & Sion · de 2 à 6 heures · dès 25 CHF par personne', final_mail='Demande par e-mail'),
'de': dict(title='Firmenevent & Teambuilding im Wallis | Rackets Academy',
  desc='Firmenanlässe in Salgesch & Sion: Padelturnier mit Coaches, Sitzungsraum, Paella oder Raclette, Apéro. 2 bis 6 Stunden, ab 25 CHF pro Person.',
  kicker='Firmenevents · Wallis', h1='Teamevent mit Padel, Essen und Apéro.',
  lede='Vom 2-stündigen Padel-Plausch bis zum ganzen Tag mit Sitzungsraum, Mittagessen und Apéro — in Salgesch und Sion, bei jedem Wetter.',
  chips=['Ab 25 CHF pro Person', '2 bis 6 Stunden', 'Drinnen, das ganze Jahr'],
  cta='Event anfragen', cta2='Beispiel-Tag ansehen',
  wa='Hola! Wir planen einen Firmenanlass. Datum: … · Personen: … · Dauer: …',
  mail_sub='Anfrage Firmenevent', mail_body='Hallo,\n\nwir planen einen Firmenanlass.\nDatum:\nAnzahl Personen:\nDauer (2–6 Std.):\nWünsche (Padel, Sitzungsraum, Paella/Raclette, Apéro, Übernachtung):\n\nDanke!',
  mods_h='Stell dir deinen Event zusammen',
  mods=[('🎾', 'Padel für alle', 'Plätze für die ganze Gruppe, nach Niveau eingeteilt, ein Coach pro Platz. Zum Schluss ein Mini-Turnier.'),
        ('💼', 'Sitzungsraum', 'Ein Raum für euren Workshop oder eure Präsentation, vor oder nach dem Spiel.'),
        ('☕', 'Kaffee & Pausen', 'Willkommenskaffee mit Gipfeli, Kaffeepausen mit Saft und Wasser.'),
        ('🥘', 'Paella oder Raclette', 'Frisch vor Ort gekocht für euer Team — mit Softdrinks und Kaffee.'),
        ('🥂', 'Apéro an der Bar', 'Anstossen an der Aussenbar — die erste Runde auf die Firma, wenn ihr wollt.'),
        ('🛏️', 'Übernachtung', 'Länger bleiben? Wir organisieren die Unterkunft auf Wunsch.')],
  day_h='Beispiel: Teamtag für 30 Personen', day_tag='Beispiel',
  day=[('09:00', 'Willkommenskaffee & Gipfeli'), ('09:30', 'Sitzungsraum für euer Team'), ('12:00', 'Paella mit Softdrinks & Kaffee'),
       ('13:30', 'Padel: 5 Plätze, 1 Coach pro Platz, nach Niveau'), ('15:30', 'Apéro an der Aussenbar')],
  day_price='≈ 75 CHF pro Person, alles inklusive',
  ref_h='Sie haben bei uns gespielt', refs=['Raiffeisen', 'CSS', 'Decathlon', 'Goldavenue Genève'],
  faq_h='Gut zu wissen',
  faq=[('Wie lange dauert ein Event?', 'Von 2 Stunden (nur Padel) bis 6 Stunden mit Sitzungsraum, Essen und Apéro. Übernachtung auf Wunsch.'),
       ('Braucht man Padel-Erfahrung?', 'Nein. Unsere Coaches teilen die Gruppe nach Niveau ein — Anfänger lernen die Basics, Erfahrene spielen ein richtiges Match.'),
       ('Was kostet es?', 'Ab 25 CHF pro Person für Padel. Ein ganzer Teamtag mit Sitzungsraum, Paella und Apéro kostet rund 75 CHF pro Person. Du bekommst eine massgeschneiderte Offerte.'),
       ('Wo findet es statt?', 'In unseren Padelcentern in Salgesch (5 Min. von Siders, 20 Min. von Crans-Montana) und Sion. Drinnen — das Wetter sagt euren Event nie ab.')],
  final_h='Sag uns dein Datum — den Rest planen wir.', final_p='Salgesch & Sion · 2 bis 6 Stunden · ab 25 CHF pro Person', final_mail='Anfrage per E-Mail'),
}

def body(t, pre):
    img = lambda p: pre + p
    wa = 'https://wa.me/' + WA_SA + '?text=' + urllib.parse.quote(t['wa'])
    mail = 'mailto:phil@racketsacademy.ch?subject=' + urllib.parse.quote(t['mail_sub']) + '&body=' + urllib.parse.quote(t['mail_body'])
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in t['chips'])
    mods = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['mods'])
    day = ''.join(f'<li><span class="co-wk ev-time">{a}</span>{b}</li>' for a, b in t['day'])
    refs = ''.join(f'<span class="ev-ref">{r}</span>' for r in t['refs'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    return f'''
<section class="spa-hero co-hero" style="background-image:url('{img("images/padel-paella-2.jpg")}'); background-position:center 70%;">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="spa-chips">{chips}</div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="{wa}" target="_blank" rel="noopener">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="#example">{t['cta2']}</a>
    </div>
  </div>
</section>

<section class="co2-sec">
  <div class="wrap">
    <h2 class="co2-h">{t['mods_h']}</h2>
    <div class="co2-bens ev-mods">{mods}</div>
  </div>
</section>

<section class="co2-sec co2-proof" id="example">
  <div class="wrap co2-split">
    <img class="co2-photo" src="{img('images/padel-paella-3.jpg')}" alt="Paella" loading="lazy">
    <div>
      <h2 class="co2-h">{t['day_h']}</h2>
      <div class="co-plan ev-day">
        <span class="co-tag">{t['day_tag']}</span>
        <ol>{day}</ol>
        <p class="ev-price">{t['day_price']}</p>
      </div>
    </div>
  </div>
</section>

<section class="co2-sec ev-refs-sec">
  <div class="wrap" style="text-align:center;">
    <p class="ev-ref-h">{t['ref_h']}</p>
    <div class="ev-refs">{refs}</div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['faq_h']}</h2>
    <div class="spa-faq">{faq}</div>
  </div>
</section>

<section class="spa-final" style="background-image:url('{img("images/coaching/coaching-6.jpg")}');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-final-inner">
    <h2>{t['final_h']}</h2>
    <p>{t['final_p']}</p>
    <div class="hero-actions" style="justify-content:center;">
      <a class="btn btn-green spa-cta" href="{wa}" target="_blank" rel="noopener">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="{mail}">{t['final_mail']}</a>
    </div>
  </div>
</section>

'''

for lang, t in T.items():
    pre = '' if lang == 'en' else '../'
    d = '' if lang == 'en' else lang + '/'
    s = open(d + 'spa-and-sauna.html').read()
    a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
    b = s.index('<footer')
    s = s[:a] + body(t, pre) + s[b:]
    s = s.replace('spa-and-sauna.html', SLUG)
    s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>' + t['title'] + '</title>', s, count=1, flags=re.S)
    esc = lambda x: x.replace('"', '&quot;')
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + esc(t['desc']) + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + esc(t['title']) + '"', s)
    s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="https://www.racketsacademy.ch/images/padel-paella-2.jpg"', s)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-events">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
    # nav: no item active
    s = s.replace('class="active"', '')
    open(d + SLUG, 'w').write(s)
    print(d + SLUG, len(t['title']), len(t['desc']))
