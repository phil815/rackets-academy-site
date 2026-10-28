"""Pickleball landing page (EN/FR/DE): pickleball.html, built from the spa page shell (like build_birthday.py).
Facts (Phil 29.10.2026): 3 indoor courts in Salgesch only (none in Sion), from 5 CHF p.p. per hour, paddle rental 2 CHF.
Rerun: python3 tools/build_pickleball.py (from repo root)."""
import re, json, urllib.parse
SLUG = 'pickleball.html'
BASE = 'https://www.racketsacademy.ch/'
PT = 'https://playtomic.com/clubs/rackets-academy-salgesch'
WA_SA = '41772780115'
IMG = 'images/wix/6363169da8a0.jpg'
T = {
'en': dict(title='Pickleball Valais – 3 indoor courts near Sierre | Rackets Academy',
  desc='Pickleball in Valais: 3 indoor courts in Salgesch, 5 min from Sierre, 18 min from Sion. From 5 CHF per person per hour, paddle 2 CHF, Sunday Mix & Match.',
  kicker='Pickleball Valais · Salgesch', h1='Pickleball in Valais — 3 indoor courts in Salgesch.',
  lede='The easiest racket sport to learn: fun from the first rally, for all ages. 5 min from Sierre, 18 min from Sion, 20 min from Visp.',
  chips=['From 5 CHF p.p. / 1 h', 'Paddle rental 2 CHF', 'Daily 7:00–23:30', 'Indoor, all year'],
  cta='Book a court', cta2='What is pickleball?', wa='Hola! I have a question about pickleball in Salgesch.',
  flow_h='Your first game', flow=[('1', 'Book on Playtomic', 'Pick a court in Salgesch — 1 hour is perfect to start.'),
     ('2', 'Grab a paddle', 'No equipment? Rent a paddle for 2 CHF, balls are on site.'),
     ('3', 'Play doubles', 'Underhand serve, short rallies, lots of laughs. The rules take 5 minutes.')],
  facts_h='Good to know', facts=[('📍', 'Where', 'Rackets Academy Salgesch, Littenstrasse 30 — free parking. Pickleball is only in Salgesch, not in Sion.'),
     ('💰', 'Prices', 'From 5 CHF per person per hour. Paddle rental 2 CHF. Free cancellation up to 24 h before.'),
     ('🍕', 'After the game', 'Bar with pizzas and snacks, and a spa with sauna, hammam and jacuzzi in the same building.')],
  faq_h='Pickleball questions', faq=[('Where can I play pickleball in Valais?', 'At Rackets Academy in Salgesch: 3 indoor courts, open daily 7:00–23:30, 5 minutes from Sierre, 18 from Sion and 20 from Visp. Book on Playtomic.'),
     ('How much does pickleball cost?', 'From 5 CHF per person per hour. A rental paddle costs 2 CHF.'),
     ('Do I need my own paddle?', 'No. You can rent a paddle for 2 CHF on site.'),
     ('Is there pickleball in Sion?', 'At our Sion site we only have padel. Pickleball is in Salgesch, 18 minutes from Sion.'),
     ('Is pickleball hard to learn?', 'No — it is the easiest racket sport to start. Underhand serve, small court, light paddle: most people play real rallies within minutes.'),
     ('Pickleball or padel?', 'Both are played in doubles. Pickleball uses a solid paddle and a light plastic ball on a smaller court without walls; padel uses the glass walls. You can try both at Rackets Academy.')],
  more_h='More at Rackets Academy', more=[('🎾', 'Padel', 'The biggest padel centre in Valais.', 'index.html'), ('🧖', 'Spa & sauna', 'Sauna, hammam and jacuzzi after the game.', 'spa-and-sauna.html'), ('📅', 'Events', 'Rackemix, tournaments and more.', 'events.html')],
  final_h='Ready for your first rally?', final_p='Salgesch · 3 indoor courts · daily 7:00–23:30'),
'fr': dict(title='Pickleball Valais – 3 courts indoor près de Sierre | Rackets Academy',
  desc='Pickleball en Valais : 3 courts indoor à Salgesch, à 5 min de Sierre et 18 min de Sion. Dès 5 CHF par personne et par heure, raquette 2 CHF, Mix & Match le dimanche.',
  kicker='Pickleball Valais · Salgesch', h1='Le pickleball en Valais — 3 courts indoor à Salgesch.',
  lede='Le sport de raquette le plus facile à apprendre : on s’amuse dès le premier échange, à tout âge. À 5 min de Sierre, 18 min de Sion, 20 min de Viège.',
  chips=['Dès 5 CHF p.p. / 1 h', 'Location de raquette 2 CHF', 'Tous les jours 7h–23h30', 'Indoor, toute l’année'],
  cta='Réserver un court', cta2='C’est quoi ?', wa='Hola ! J’ai une question sur le pickleball à Salgesch.',
  flow_h='Ta première partie', flow=[('1', 'Réserve sur Playtomic', 'Choisis un court à Salgesch — 1 heure, c’est parfait pour commencer.'),
     ('2', 'Prends une raquette', 'Pas de matériel ? Location de raquette 2 CHF, balles sur place.'),
     ('3', 'Joue en double', 'Service par en dessous, échanges courts, beaucoup de rires. Les règles en 5 minutes.')],
  facts_h='Bon à savoir', facts=[('📍', 'Où', 'Rackets Academy Salgesch, Littenstrasse 30 — parking gratuit. Le pickleball est seulement à Salgesch, pas à Sion.'),
     ('💰', 'Tarifs', 'Dès 5 CHF par personne et par heure. Location de raquette 2 CHF. Annulation gratuite jusqu’à 24 h avant.'),
     ('🍕', 'Après le match', 'Bar avec pizzas et snacks, et spa avec sauna, hammam et jacuzzi dans le même bâtiment.')],
  faq_h='Questions sur le pickleball', faq=[('Où jouer au pickleball en Valais ?', 'À la Rackets Academy de Salgesch : 3 courts indoor, ouverts tous les jours de 7h à 23h30, à 5 minutes de Sierre, 18 de Sion et 20 de Viège. Réservation sur Playtomic.'),
     ('Combien coûte le pickleball ?', 'Dès 5 CHF par personne et par heure. La location d’une raquette coûte 2 CHF.'),
     ('Faut-il sa propre raquette ?', 'Non. Tu peux louer une raquette sur place pour 2 CHF.'),
     ('Y a-t-il du pickleball à Sion ?', 'Sur notre site de Sion, nous avons uniquement du padel. Le pickleball se joue à Salgesch, à 18 minutes de Sion.'),
     ('Le pickleball est-il difficile ?', 'Non — c’est le sport de raquette le plus simple pour débuter. Service par en dessous, petit terrain, raquette légère : on fait de vrais échanges en quelques minutes.'),
     ('Pickleball ou padel ?', 'Les deux se jouent en double. Le pickleball se joue avec une raquette pleine et une balle légère en plastique sur un terrain plus petit sans vitres ; le padel utilise les vitres. Tu peux essayer les deux à la Rackets Academy.')],
  more_h='Aussi à la Rackets Academy', more=[('🎾', 'Padel', 'Le plus grand centre de padel du Valais.', 'index.html'), ('🧖', 'Spa & sauna', 'Sauna, hammam et jacuzzi après le match.', 'spa-and-sauna.html'), ('📅', 'Événements', 'Rackemix, tournois et plus.', 'events.html')],
  final_h='Prêt pour ton premier échange ?', final_p='Salgesch · 3 courts indoor · tous les jours 7h–23h30'),
'de': dict(title='Pickleball Wallis – 3 Indoor-Plätze bei Siders | Rackets Academy',
  desc='Pickleball im Wallis: 3 Indoor-Plätze in Salgesch, 5 Min. ab Siders, 20 Min. ab Visp. Ab 5 CHF pro Person und Stunde, Schläger 2 CHF, Mix & Match am Sonntag.',
  kicker='Pickleball Wallis · Salgesch', h1='Pickleball im Wallis — 3 Indoor-Plätze in Salgesch.',
  lede='Der einfachste Racketsport: Spass ab dem ersten Ballwechsel, für jedes Alter. 5 Min. ab Siders, 20 Min. ab Visp, 30 Min. ab Brig.',
  chips=['Ab 5 CHF p.P. / 1 Std.', 'Schlägermiete 2 CHF', 'Täglich 07:00–23:30', 'Indoor, ganzjährig'],
  cta='Platz buchen', cta2='Was ist Pickleball?', wa='Hola! Ich habe eine Frage zu Pickleball in Salgesch.',
  flow_h='Dein erstes Spiel', flow=[('1', 'Auf Playtomic buchen', 'Platz in Salgesch wählen — 1 Stunde ist perfekt für den Start.'),
     ('2', 'Schläger mieten', 'Keine Ausrüstung? Schläger für 2 CHF mieten, Bälle gibt’s vor Ort.'),
     ('3', 'Doppel spielen', 'Aufschlag von unten, kurze Ballwechsel, viel Spass. Die Regeln in 5 Minuten.')],
  facts_h='Gut zu wissen', facts=[('📍', 'Wo', 'Rackets Academy Salgesch, Littenstrasse 30 — Gratis-Parkplätze. Pickleball gibt es nur in Salgesch, nicht in Sion.'),
     ('💰', 'Preise', 'Ab 5 CHF pro Person und Stunde. Schlägermiete 2 CHF. Kostenlos stornieren bis 24 Std. vorher.'),
     ('🍕', 'Nach dem Spiel', 'Bar mit Pizzas und Snacks, Spa mit Sauna, Hammam und Whirlpool im gleichen Gebäude.')],
  faq_h='Fragen zu Pickleball', faq=[('Wo kann man im Wallis Pickleball spielen?', 'In der Rackets Academy in Salgesch: 3 Indoor-Plätze, täglich 07:00–23:30, 5 Minuten ab Siders, 20 ab Visp und 30 ab Brig. Buchung über Playtomic.'),
     ('Was kostet Pickleball?', 'Ab 5 CHF pro Person und Stunde. Ein Mietschläger kostet 2 CHF.'),
     ('Brauche ich einen eigenen Schläger?', 'Nein. Vor Ort kannst du einen Schläger für 2 CHF mieten.'),
     ('Gibt es Pickleball in Sion?', 'In unserem Standort Sion gibt es nur Padel. Pickleball spielst du in Salgesch, 18 Minuten von Sion.'),
     ('Ist Pickleball schwer zu lernen?', 'Nein — es ist der einfachste Racketsport für den Einstieg. Aufschlag von unten, kleines Feld, leichter Schläger: nach wenigen Minuten spielst du echte Ballwechsel.'),
     ('Pickleball oder Padel?', 'Beides wird im Doppel gespielt. Pickleball spielt man mit einem festen Schläger und leichtem Plastikball auf einem kleineren Feld ohne Wände; beim Padel spielen die Glaswände mit. Bei uns kannst du beides ausprobieren.')],
  more_h='Mehr in der Rackets Academy', more=[('🎾', 'Padel', 'Das grösste Padelzentrum im Wallis.', 'index.html'), ('🧖', 'Spa & Sauna', 'Sauna, Hammam und Whirlpool nach dem Spiel.', 'spa-and-sauna.html'), ('📅', 'Events', 'Rackemix, Turniere und mehr.', 'events.html')],
  final_h='Bereit für deinen ersten Ballwechsel?', final_p='Salgesch · 3 Indoor-Plätze · täglich 07:00–23:30'),
}

EXTRA = {'en': {'what_h': 'What is pickleball?', 'what_p': 'Pickleball is a racket sport invented in 1965 in the USA and now one of the fastest-growing sports in the world. It mixes tennis, badminton and table tennis: you play with a solid paddle and a light perforated plastic ball on a small court — usually in doubles. Rallies are short and social, and beginners have fun from the very first game.', 'rules': [('📐', 'Small court', 'The size of a badminton court (13.4 × 6.1 m), net about 86 cm high.'), ('🏓', 'Paddle & ball', 'Solid paddle, light plastic ball with holes — easy on the arm.'), ('⬇️', 'Underhand serve', 'Serve diagonally and below the waist; the ball must bounce once on each side first.'), ('🚫', 'The kitchen', 'No volleys in the 2.13 m zone next to the net — that makes the game tactical.'), ('🔢', 'Scoring', 'Games to 11 points, win by 2. Only the serving team scores.'), ('❤️', 'Good for you', 'Low impact on joints, lots of movement and laughter — for all ages.')], 'mm_h': 'Mix & Match — every Sunday', 'mm_p': 'Drop-in pickleball for all levels: just come, we mix the teams so you play with and against new people every round.', 'mm_facts': ['Every Sunday 10:00–12:00', 'Drop-in, no registration', '10 CHF per person', 'Paddle rental +2 CHF', 'All levels welcome'], 'spa_h': 'Member of the Swiss Pickleball Association', 'spa_p': 'Rackets Academy Salgesch is a member of the Swiss Pickleball Association, the national federation that promotes pickleball in Switzerland — with clubs, tournaments and the Swiss Pickleball Tour.', 'spa_cta': 'Visit pickleballverband.ch', 'spa_url': 'https://pickleballverband.ch/en/', 'faq_add': [('What is pickleball?', 'A racket sport from the USA that mixes tennis, badminton and table tennis. It is played with a solid paddle and a light perforated plastic ball on a badminton-sized court, usually in doubles. Games go to 11 points.'), ('When is the pickleball Mix & Match?', 'Every Sunday from 10:00 to 12:00 in Salgesch. Drop-in, no registration needed, 10 CHF per person, paddle rental 2 CHF. All levels welcome.')]}, 'fr': {'what_h': "C'est quoi, le pickleball ?", 'what_p': "Le pickleball est un sport de raquette inventé en 1965 aux États-Unis et aujourd'hui l'un des sports qui grandissent le plus vite au monde. Il mélange tennis, badminton et ping-pong : on joue avec une raquette pleine et une balle en plastique perforée sur un petit terrain — le plus souvent en double. Les échanges sont courts et conviviaux, et les débutants s'amusent dès la première partie.", 'rules': [('📐', 'Petit terrain', 'La taille d’un terrain de badminton (13,4 × 6,1 m), filet à environ 86 cm.'), ('🏓', 'Raquette & balle', 'Raquette pleine, balle légère en plastique perforée — douce pour le bras.'), ('⬇️', 'Service par en dessous', 'En diagonale et sous la taille ; la balle doit d’abord rebondir une fois de chaque côté.'), ('🚫', 'La « kitchen »', 'Pas de volée dans la zone de 2,13 m près du filet — c’est ce qui rend le jeu tactique.'), ('🔢', 'Comptage', 'Parties en 11 points, avec 2 points d’écart. Seule l’équipe au service marque.'), ('❤️', 'Bon pour la santé', 'Peu d’impact sur les articulations, beaucoup de mouvement et de rires — à tout âge.')], 'mm_h': 'Mix & Match — chaque dimanche', 'mm_p': 'Pickleball libre pour tous les niveaux : viens simplement, on mélange les équipes pour que tu joues avec et contre de nouvelles personnes à chaque tour.', 'mm_facts': ['Chaque dimanche 10h–12h', 'Sans inscription', '10 CHF par personne', 'Location de raquette +2 CHF', 'Tous niveaux bienvenus'], 'spa_h': 'Membre de la Swiss Pickleball Association', 'spa_p': 'La Rackets Academy Salgesch est membre de la Swiss Pickleball Association, la fédération nationale qui développe le pickleball en Suisse — avec clubs, tournois et le Swiss Pickleball Tour.', 'spa_cta': 'Visiter pickleballverband.ch', 'spa_url': 'https://pickleballverband.ch/fr/', 'faq_add': [("C'est quoi, le pickleball ?", "Un sport de raquette venu des États-Unis qui mélange tennis, badminton et ping-pong. On joue avec une raquette pleine et une balle légère en plastique perforée sur un terrain de la taille d'un terrain de badminton, le plus souvent en double. Les parties se jouent en 11 points."), ('Quand a lieu le Mix & Match de pickleball ?', 'Chaque dimanche de 10h à 12h à Salgesch. Sans inscription, 10 CHF par personne, location de raquette 2 CHF. Tous niveaux bienvenus.')]}, 'de': {'what_h': 'Was ist Pickleball?', 'what_p': 'Pickleball ist ein Racketsport, 1965 in den USA erfunden und heute eine der am schnellsten wachsenden Sportarten der Welt. Er verbindet Tennis, Badminton und Tischtennis: Gespielt wird mit einem festen Schläger und einem leichten, gelochten Plastikball auf einem kleinen Feld — meist im Doppel. Die Ballwechsel sind kurz und gesellig, Einsteiger haben vom ersten Spiel an Spass.', 'rules': [('📐', 'Kleines Feld', 'So gross wie ein Badmintonfeld (13,4 × 6,1 m), Netz rund 86 cm hoch.'), ('🏓', 'Schläger & Ball', 'Fester Schläger, leichter Plastikball mit Löchern — schont den Arm.'), ('⬇️', 'Aufschlag von unten', 'Diagonal und unterhalb der Hüfte; der Ball muss zuerst auf jeder Seite einmal aufspringen.'), ('🚫', 'Die «Kitchen»', 'Kein Volley in der 2,13-m-Zone am Netz — das macht das Spiel taktisch.'), ('🔢', 'Zählweise', 'Gespielt wird auf 11 Punkte, mit 2 Punkten Vorsprung. Nur das aufschlagende Team punktet.'), ('❤️', 'Gesund', 'Gelenkschonend, viel Bewegung und viel Lachen — für jedes Alter.')], 'mm_h': 'Mix & Match — jeden Sonntag', 'mm_p': 'Pickleball für alle Niveaus, einfach vorbeikommen: Wir mischen die Teams, du spielst jede Runde mit und gegen neue Leute.', 'mm_facts': ['Jeden Sonntag 10:00–12:00', 'Ohne Anmeldung', '10 CHF pro Person', 'Schlägermiete +2 CHF', 'Alle Niveaus willkommen'], 'spa_h': 'Mitglied der Swiss Pickleball Association', 'spa_p': 'Die Rackets Academy Salgesch ist Mitglied der Swiss Pickleball Association, des nationalen Verbands, der Pickleball in der Schweiz fördert — mit Clubs, Turnieren und der Swiss Pickleball Tour.', 'spa_cta': 'Zu pickleballverband.ch', 'spa_url': 'https://pickleballverband.ch/', 'faq_add': [('Was ist Pickleball?', 'Ein Racketsport aus den USA, der Tennis, Badminton und Tischtennis verbindet. Gespielt wird mit einem festen Schläger und einem leichten, gelochten Plastikball auf einem Feld in Badmintongrösse, meist im Doppel. Gespielt wird auf 11 Punkte.'), ('Wann ist das Pickleball Mix & Match?', 'Jeden Sonntag von 10:00 bis 12:00 in Salgesch. Ohne Anmeldung, 10 CHF pro Person, Schlägermiete 2 CHF. Alle Niveaus willkommen.')]}}
SPA_LOGO = 'https://cdn.pickleballverband.ch/wp-content/uploads/2023/11/SPA-logo-onblack_512px.webp'
for _l in T:
    T[_l].update(EXTRA[_l])
    T[_l]['faq'] = T[_l]['faq_add'] + T[_l]['faq']

def body(t, pre):
    wa = 'https://wa.me/' + WA_SA + '?text=' + urllib.parse.quote(t['wa'])
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in t['chips'])
    flow = ''.join(f'<div class="kb-step"><span class="kb-badge">{a}</span><h3>{h}</h3><p>{p}</p></div>' for a, h, p in t['flow'])
    facts = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['facts'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    more = ''.join(f'<a class="co2-b ow-more" href="{l}"><span class="co2-ic">{e}</span><h3>{h} →</h3><p>{p}</p></a>' for e, h, p, l in t['more'])
    rules = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['rules'])
    mm = ''.join(f'<span class="spa-chip pb-chip">{c}</span>' for c in t['mm_facts'])
    return f'''
<section class="spa-hero co-hero kb-hero" style="background-image:url('{BASE + IMG}');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="spa-chips">{chips}</div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="{PT}" target="_blank" rel="noopener">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="#what">{t['cta2']}</a>
    </div>
  </div>
</section>

<section class="co2-sec" id="what">
  <div class="wrap">
    <h2 class="co2-h">{t['what_h']}</h2>
    <p class="pb-intro">{t['what_p']}</p>
    <div class="co2-bens ev-mods pb-rules">{rules}</div>
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

<section class="co2-sec ow-day" id="mix">
  <div class="wrap">
    <h2 class="co2-h">{t['mm_h']}</h2>
    <p class="pb-intro">{t['mm_p']}</p>
    <div class="spa-chips pb-chips">{mm}</div>
  </div>
</section>

<section class="co2-sec">
  <div class="wrap pb-spa">
    <a class="pb-spa-logo" href="{t['spa_url']}" target="_blank" rel="noopener"><img src="{SPA_LOGO}" alt="Swiss Pickleball Association" width="256" height="145" loading="lazy"></a>
    <div><h2 class="co2-h">{t['spa_h']}</h2><p>{t['spa_p']}</p><p><a class="pb-spa-link" href="{t['spa_url']}" target="_blank" rel="noopener">{t['spa_cta']} →</a></p></div>
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

<section class="spa-final kb-final" style="background-image:url('{pre}images/coaching/coaching-6.jpg');">
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
      {'@type': 'SportsActivityLocation', 'name': 'Rackets Academy Salgesch – Pickleball', 'url': url, 'telephone': '+41772780115', 'image': BASE + IMG,
       'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressRegion': 'VS', 'addressCountry': 'CH'},
       'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 'opens': '07:00', 'closes': '23:30'}],
       'areaServed': ['Sierre', 'Siders', 'Sion', 'Sitten', 'Crans-Montana', 'Leuk', 'Visp', 'Valais', 'Wallis']},
      {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}]}
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-pb">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
    s = s.replace('class="active"', '')
    open(d + SLUG, 'w').write(s)
    print(d + SLUG, len(t['title']), len(t['desc']))
