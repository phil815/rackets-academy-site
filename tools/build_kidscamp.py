"""Kids holiday padel camps Salgesch (EN/FR/DE): hub kids-camp.html + kids-camp-winter/easter/summer.html.
Built from the spa page shell (like build_birthday.py). Half day 09:00-12:00, 6-14 years, CHF 250 per 5-day week.
Change weeks/prices here and rerun: python3 tools/build_kidscamp.py (from repo root)."""
import re, json, urllib.parse, datetime as dt
WA_SA = '41772780115'
BASE = 'https://www.racketsacademy.ch/'
PRICE_DAY = 50          # 5 mornings = 250 CHF, 4 mornings = 200 CHF
D = dt.date
WEEKS = {
  'winter': [(D(2026, 12, 28), D(2026, 12, 31)), (D(2027, 1, 4), D(2027, 1, 8)), (D(2027, 2, 8), D(2027, 2, 12))],
  'easter': [(D(2027, 3, 30), D(2027, 4, 2))],
  'summer': [(D(2027, 6, 28), D(2027, 7, 2)), (D(2027, 7, 5), D(2027, 7, 9)), (D(2027, 7, 12), D(2027, 7, 16)),
             (D(2027, 7, 19), D(2027, 7, 23)), (D(2027, 7, 26), D(2027, 7, 30)), (D(2027, 8, 2), D(2027, 8, 6)),
             (D(2027, 8, 9), D(2027, 8, 13))],
}
SEASONS = ['winter', 'easter', 'summer']
SLUG = {'hub': 'kids-camp.html', 'winter': 'kids-camp-winter.html', 'easter': 'kids-camp-easter.html', 'summer': 'kids-camp-summer.html'}
IMG = {'hub': 'images/coaching/coaching-2.jpg', 'winter': 'images/coaching/coaching-3.jpg', 'easter': 'images/coaching/coaching-4.jpg', 'summer': 'images/coaching/coaching-5.jpg'}
MON = {'en': 'January February March April May June July August September October November December'.split(),
       'fr': 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'.split(),
       'de': 'Januar Februar März April Mai Juni Juli August September Oktober November Dezember'.split()}

def drange(a, b, L):
    m = MON[L]
    if L == 'en':
        return (f'{a.day} – {b.day} {m[a.month-1]} {b.year}' if a.month == b.month else f'{a.day} {m[a.month-1]} – {b.day} {m[b.month-1]} {b.year}')
    if L == 'fr':
        return (f'{a.day} – {b.day} {m[a.month-1]} {b.year}' if a.month == b.month else f'{a.day} {m[a.month-1]} – {b.day} {m[b.month-1]} {b.year}')
    return (f'{a.day}. – {b.day}. {m[a.month-1]} {b.year}' if a.month == b.month else f'{a.day}. {m[a.month-1]} – {b.day}. {m[b.month-1]} {b.year}')

def ndays(a, b):
    return (b - a).days + 1

T = {
'en': dict(
  name={'hub': 'Kids padel holiday camps', 'winter': 'Winter holiday camp', 'easter': 'Easter holiday camp', 'summer': 'Summer camp'},
  title={'hub': 'Padel holiday camps for kids in Valais | Rackets Academy',
         'winter': 'Kids padel camp, Christmas & carnival holidays | Rackets Academy',
         'easter': 'Kids padel camp, Easter holidays 2027, Valais | Rackets Academy',
         'summer': 'Kids padel summer camp 2027, Valais | Rackets Academy'},
  desc={'hub': 'Padel camps for kids aged 6–14 in the Valais school holidays: winter, Easter and summer 2027 in Salgesch (5 min from Sierre). Mornings 9–12, CHF 250 per week.',
        'winter': 'Padel camp for kids aged 6–14 in the Christmas and carnival holidays 2026/27 in Salgesch, 5 min from Sierre. Mornings 9–12, indoors, CHF 250 per week.',
        'easter': 'Padel camp for kids aged 6–14 in the Easter holidays 2027 in Salgesch, 5 min from Sierre. 4 mornings 9–12, indoors, rackets included, CHF 200.',
        'summer': 'Padel summer camp 2027 for kids aged 6–14 in Salgesch, 5 min from Sierre: 7 weeks from 28 June, mornings 9–12, indoors, CHF 250 per week.'},
  kicker={'hub': 'Kids camps · Salgesch', 'winter': 'Winter holidays 2026/27 · Salgesch', 'easter': 'Easter holidays 2027 · Salgesch', 'summer': 'Summer holidays 2027 · Salgesch'},
  h1={'hub': 'Holidays? Padel camp!', 'winter': 'Padel instead of the sofa — all winter.', 'easter': 'Easter holidays on the padel court.', 'summer': 'The summer camp kids ask for again.'},
  lede={'hub': 'Mornings full of padel, games and new friends for kids aged 6–14 — in every school holiday, indoors in Salgesch.',
        'winter': 'Christmas and carnival holidays: five mornings of padel, games and matches. Indoors and warm, whatever the weather.',
        'easter': 'Four mornings of padel, games and a mini tournament in the Easter holidays — indoors in Salgesch.',
        'summer': 'Seven summer weeks to choose from: padel, games and matches every morning, indoors and in the shade.'},
  chips=['Age 6–14', 'Mon–Fri 9:00–12:00', 'CHF 250 per week', 'Rackets included'],
  cta='Reserve a spot', cta2='See the dates',
  wa='Hola! I would like to reserve a spot in the kids padel camp: {w}. Child: … · Age: …',
  flow_h='A camp morning',
  flow=[('9:00', 'Warm-up & technique', 'Coordination games, then the basics: forehand, backhand, volley, the walls.'),
        ('10:15', 'Break & games', 'Short snack break, then team games on court.'),
        ('11:00', 'Matches', 'Real points and a mini tournament on the last day. Pick-up at 12:00.')],
  weeks_h='Dates & booking', week_lbl='Week', days_lbl='{n} mornings',
  facts_h='Good to know',
  facts=[('📍', 'Where', 'Rackets Academy Salgesch, Littenstrasse 30 — 5 min from Sierre, 20 min from Visp.'),
         ('👧', 'Who', 'Kids aged 6–14, beginners and players. Groups by age and level.'),
         ('🎒', 'What to bring', 'Indoor sports shoes, sportswear, a water bottle and a snack. Rackets and balls are provided.')],
  faq_h='Questions from parents',
  faq=[('How much does the kids padel camp cost?', 'CHF 250 per week (5 mornings, Monday to Friday, 9:00–12:00). Short weeks with 4 mornings cost CHF 200. Rackets and balls are included.'),
       ('Does my child need to know how to play padel?', 'No. Kids are grouped by age and level, so beginners and players both get the right coaching.'),
       ('Which age group is the camp for?', 'For kids and teens aged 6 to 14.'),
       ('Do the camp weeks match our school holidays?', 'The weeks follow the Valais school holidays. If your holidays fall on other dates, write us on WhatsApp and we will find a solution.'),
       ('How do I book a spot?', 'Tap “Reserve a spot” next to the week you want and send us the WhatsApp message with your child’s name and age. We confirm your spot and send the payment details.')],
  more_h='All holiday camps', season_lbl={'winter': 'Winter 2026/27', 'easter': 'Easter 2027', 'summer': 'Summer 2027'},
  season_sub={'winter': 'Christmas & carnival', 'easter': 'Easter holidays', 'summer': '7 weeks from 28 June'},
  final_h='Places are limited — reserve early.', final_p='Salgesch · Mon–Fri 9:00–12:00 · age 6–14'),
'fr': dict(
  name={'hub': 'Camps de padel pour enfants', 'winter': "Camp des vacances d'hiver", 'easter': 'Camp des vacances de Pâques', 'summer': "Camp d'été"},
  title={'hub': 'Camps de padel enfants vacances scolaires Valais | Rackets Academy',
         'winter': 'Camp padel enfants vacances de Noël et Carnaval | Rackets Academy',
         'easter': 'Camp padel enfants vacances de Pâques 2027, Valais | Rackets Academy',
         'summer': "Camp d'été padel enfants 2027, Sierre Valais | Rackets Academy"},
  desc={'hub': "Camps de padel pour enfants de 6 à 14 ans pendant les vacances scolaires valaisannes : hiver, Pâques et été 2027 à Salgesch (5 min de Sierre). Matins 9h–12h, CHF 250 la semaine.",
        'winter': "Camp de padel pour enfants de 6 à 14 ans pendant les vacances de Noël et de Carnaval 2026/27 à Salgesch, 5 min de Sierre. Matins 9h–12h, en salle, CHF 250 la semaine.",
        'easter': "Camp de padel pour enfants de 6 à 14 ans pendant les vacances de Pâques 2027 à Salgesch, 5 min de Sierre. 4 matins 9h–12h, en salle, raquettes incluses, CHF 200.",
        'summer': "Camp d'été de padel 2027 pour enfants de 6 à 14 ans à Salgesch, 5 min de Sierre : 7 semaines dès le 28 juin, matins 9h–12h, en salle, CHF 250 la semaine."},
  kicker={'hub': 'Camps enfants · Salgesch', 'winter': "Vacances d'hiver 2026/27 · Salgesch", 'easter': 'Vacances de Pâques 2027 · Salgesch', 'summer': "Vacances d'été 2027 · Salgesch"},
  h1={'hub': 'Les vacances ? Camp de padel !', 'winter': "Du padel plutôt que le canapé, tout l'hiver.", 'easter': 'Les vacances de Pâques sur le terrain de padel.', 'summer': "Le camp d'été que les enfants redemandent."},
  lede={'hub': "Des matinées de padel, de jeux et de nouveaux copains pour les 6–14 ans — à chaque vacances scolaires, en salle à Salgesch.",
        'winter': "Vacances de Noël et de Carnaval : cinq matinées de padel, de jeux et de matchs. Au chaud, quelle que soit la météo.",
        'easter': "Quatre matinées de padel, de jeux et un mini-tournoi pendant les vacances de Pâques — en salle à Salgesch.",
        'summer': "Sept semaines d'été au choix : padel, jeux et matchs chaque matin, en salle et à l'ombre."},
  chips=['6–14 ans', 'Lu–ve 9h–12h', 'CHF 250 la semaine', 'Raquettes fournies'],
  cta='Réserver une place', cta2='Voir les dates',
  wa="Hola ! J'aimerais réserver une place au camp de padel enfants : {w}. Enfant : … · Âge : …",
  flow_h='Une matinée de camp',
  flow=[('9h00', 'Échauffement & technique', 'Jeux de coordination, puis les bases : coup droit, revers, volée, les vitres.'),
        ('10h15', 'Pause & jeux', "Petite pause goûter, puis jeux d'équipe sur le terrain."),
        ('11h00', 'Matchs', 'De vrais points et un mini-tournoi le dernier jour. Fin à 12h00.')],
  weeks_h='Dates & réservation', week_lbl='Semaine', days_lbl='{n} matinées',
  facts_h='Bon à savoir',
  facts=[('📍', 'Où', 'Rackets Academy Salgesch, Littenstrasse 30 — à 5 min de Sierre, 20 min de Sion.'),
         ('👧', 'Pour qui', "Enfants de 6 à 14 ans, débutants ou joueurs. Groupes par âge et niveau."),
         ('🎒', 'À prendre', "Chaussures de sport pour la salle, tenue de sport, gourde et goûter. Raquettes et balles fournies.")],
  faq_h='Questions des parents',
  faq=[('Combien coûte le camp de padel pour enfants ?', 'CHF 250 la semaine (5 matinées, du lundi au vendredi, 9h–12h). Les semaines de 4 matinées coûtent CHF 200. Raquettes et balles incluses.'),
       ("Mon enfant doit-il déjà savoir jouer au padel ?", "Non. Les enfants sont répartis par âge et par niveau : débutants comme joueurs reçoivent le bon entraînement."),
       ("Pour quel âge est le camp ?", "Pour les enfants et ados de 6 à 14 ans."),
       ('Les semaines correspondent-elles à nos vacances scolaires ?', "Les semaines suivent les vacances scolaires valaisannes. Si vos vacances tombent à d'autres dates, écrivez-nous sur WhatsApp, on trouvera une solution."),
       ('Comment réserver une place ?', "Touchez « Réserver une place » à côté de la semaine choisie et envoyez-nous le message WhatsApp avec le prénom et l'âge de votre enfant. Nous confirmons la place et envoyons les infos de paiement.")],
  more_h='Tous les camps de vacances', season_lbl={'winter': 'Hiver 2026/27', 'easter': 'Pâques 2027', 'summer': 'Été 2027'},
  season_sub={'winter': 'Noël & Carnaval', 'easter': 'Vacances de Pâques', 'summer': '7 semaines dès le 28 juin'},
  final_h='Places limitées — réservez tôt.', final_p='Salgesch · lu–ve 9h–12h · 6–14 ans'),
'de': dict(
  name={'hub': 'Padel-Feriencamps für Kinder', 'winter': 'Wintercamp', 'easter': 'Ostercamp', 'summer': 'Sommercamp'},
  title={'hub': 'Padel-Feriencamp für Kinder im Wallis | Rackets Academy',
         'winter': 'Kinder-Padelcamp Weihnachts- & Fasnachtsferien | Rackets Academy',
         'easter': 'Kinder-Padelcamp Osterferien 2027, Oberwallis | Rackets Academy',
         'summer': 'Padel-Sommercamp für Kinder 2027, Wallis | Rackets Academy'},
  desc={'hub': 'Padel-Camps für Kinder von 6 bis 14 Jahren in den Walliser Schulferien: Winter, Ostern und Sommer 2027 in Salgesch (20 Min. ab Visp). Vormittags 9–12 Uhr, CHF 250 pro Woche.',
        'winter': 'Padel-Camp für Kinder von 6 bis 14 Jahren in den Weihnachts- und Fasnachtsferien 2026/27 in Salgesch, 20 Min. ab Visp. Vormittags 9–12 Uhr, drinnen, CHF 250 pro Woche.',
        'easter': 'Padel-Camp für Kinder von 6 bis 14 Jahren in den Osterferien 2027 in Salgesch, 20 Min. ab Visp. 4 Vormittage 9–12 Uhr, drinnen, Schläger inklusive, CHF 200.',
        'summer': 'Padel-Sommercamp 2027 für Kinder von 6 bis 14 Jahren in Salgesch, 20 Min. ab Visp: 7 Wochen ab 28. Juni, vormittags 9–12 Uhr, drinnen, CHF 250 pro Woche.'},
  kicker={'hub': 'Kindercamps · Salgesch', 'winter': 'Winterferien 2026/27 · Salgesch', 'easter': 'Osterferien 2027 · Salgesch', 'summer': 'Sommerferien 2027 · Salgesch'},
  h1={'hub': 'Ferien? Padel-Camp!', 'winter': 'Padel statt Sofa — den ganzen Winter.', 'easter': 'Osterferien auf dem Padelplatz.', 'summer': 'Das Sommercamp, das Kinder nochmals wollen.'},
  lede={'hub': 'Vormittage voller Padel, Spiele und neuer Freunde für Kinder von 6 bis 14 — in allen Schulferien, drinnen in Salgesch.',
        'winter': 'Weihnachts- und Fasnachtsferien: fünf Vormittage Padel, Spiele und Matches. Drinnen und warm, bei jedem Wetter.',
        'easter': 'Vier Vormittage Padel, Spiele und ein Mini-Turnier in den Osterferien — drinnen in Salgesch.',
        'summer': 'Sieben Sommerwochen zur Wahl: jeden Vormittag Padel, Spiele und Matches, drinnen und im Schatten.'},
  chips=['6–14 Jahre', 'Mo–Fr 9–12 Uhr', 'CHF 250 pro Woche', 'Schläger inklusive'],
  cta='Platz reservieren', cta2='Daten ansehen',
  wa='Hola! Ich möchte einen Platz im Kinder-Padelcamp reservieren: {w}. Kind: … · Alter: …',
  flow_h='Ein Camp-Vormittag',
  flow=[('9:00', 'Aufwärmen & Technik', 'Koordinationsspiele, dann die Basics: Vorhand, Rückhand, Volley, die Wände.'),
        ('10:15', 'Pause & Spiele', 'Kurze Znüni-Pause, dann Teamspiele auf dem Platz.'),
        ('11:00', 'Matches', 'Echte Punkte und am letzten Tag ein Mini-Turnier. Abholen um 12:00.')],
  weeks_h='Daten & Buchung', week_lbl='Woche', days_lbl='{n} Vormittage',
  facts_h='Gut zu wissen',
  facts=[('📍', 'Wo', 'Rackets Academy Salgesch, Littenstrasse 30 — 5 Min. ab Siders, 20 Min. ab Visp, 30 Min. ab Brig.'),
         ('👧', 'Für wen', 'Kinder von 6 bis 14 Jahren, Anfänger und Spieler. Gruppen nach Alter und Niveau.'),
         ('🎒', 'Mitnehmen', 'Hallenschuhe, Sportkleider, Trinkflasche und Znüni. Schläger und Bälle stellen wir.')],
  faq_h='Fragen von Eltern',
  faq=[('Was kostet das Kinder-Padelcamp?', 'CHF 250 pro Woche (5 Vormittage, Montag bis Freitag, 9–12 Uhr). Kurze Wochen mit 4 Vormittagen kosten CHF 200. Schläger und Bälle sind inklusive.'),
       ('Muss mein Kind schon Padel spielen können?', 'Nein. Die Kinder spielen in Gruppen nach Alter und Niveau — Anfänger wie Fortgeschrittene bekommen das passende Training.'),
       ('Für welches Alter ist das Camp?', 'Für Kinder und Jugendliche von 6 bis 14 Jahren.'),
       ('Passen die Camp-Wochen zu unseren Schulferien?', 'Die Wochen richten sich nach den Walliser Schulferien. Liegen eure Ferien anders, schreibt uns auf WhatsApp — wir finden eine Lösung.'),
       ('Wie reserviere ich einen Platz?', 'Tippe bei der gewünschten Woche auf «Platz reservieren» und schick uns die WhatsApp-Nachricht mit Name und Alter deines Kindes. Wir bestätigen den Platz und schicken die Zahlungsinfos.')],
  more_h='Alle Feriencamps', season_lbl={'winter': 'Winter 2026/27', 'easter': 'Ostern 2027', 'summer': 'Sommer 2027'},
  season_sub={'winter': 'Weihnachten & Fasnacht', 'easter': 'Osterferien', 'summer': '7 Wochen ab 28. Juni'},
  final_h='Plätze begrenzt — früh reservieren.', final_p='Salgesch · Mo–Fr 9–12 Uhr · 6–14 Jahre'),
}

def wa_link(t, label):
    return 'https://wa.me/' + WA_SA + '?text=' + urllib.parse.quote(t['wa'].format(w=label))

def week_rows(t, L, season, with_season=False):
    rows = ''
    for a, b in WEEKS[season]:
        lab = drange(a, b, L)
        n = ndays(a, b)
        price = n * PRICE_DAY
        head = (t['season_lbl'][season] + ' · ' if with_season else '') + lab
        rows += (f'<div class="kc-week"><div><strong>{head}</strong><span>{t["days_lbl"].format(n=n)} · 9:00–12:00 · CHF {price}</span></div>'
                 f'<a class="btn btn-green kc-book" href="{wa_link(t, head)}" target="_blank" rel="noopener">{t["cta"]}</a></div>')
    return rows

def body(t, L, page, pre):
    img = lambda p: pre + p
    seasons = SEASONS if page == 'hub' else [page]
    first = WEEKS[seasons[0]][0]
    wa = wa_link(t, t['name'][page])
    chips = list(t['chips'])
    if page == 'easter':
        chips[1] = {'en': 'Tue–Fri 9:00–12:00', 'fr': 'Ma–ve 9h–12h', 'de': 'Di–Fr 9–12 Uhr'}[L]
        chips[2] = 'CHF 200'
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in chips)
    flow = ''.join(f'<div class="kb-step"><span class="kb-badge">{a}</span><h3>{h}</h3><p>{p}</p></div>' for a, h, p in t['flow'])
    weeks = ''
    for s in seasons:
        weeks += (f'<h3 class="kc-season">{t["season_lbl"][s]} <span>· {t["season_sub"][s]}</span></h3>' if page == 'hub' else '') + '<div class="kc-weeks">' + week_rows(t, L, s) + '</div>'
    facts = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['facts'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    more = ''.join(f'<a class="co2-b ow-more" href="{SLUG[s]}"><span class="co2-ic">{ {"winter": "❄️", "easter": "🐣", "summer": "☀️"}[s] }</span><h3>{t["season_lbl"][s]} →</h3><p>{t["season_sub"][s]}</p></a>'
                   for s in SEASONS if s != page)
    if page != 'hub':
        more = f'<a class="co2-b ow-more" href="{SLUG["hub"]}"><span class="co2-ic">🎾</span><h3>{t["name"]["hub"]} →</h3><p>{t["more_h"]}</p></a>' + more
    return f'''
<section class="spa-hero co-hero kb-hero" style="background-image:url('{img(IMG[page])}');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker'][page]}</p>
    <h1>{t['h1'][page]}</h1>
    <p class="lede">{t['lede'][page]}</p>
    <div class="spa-chips">{chips}</div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="#dates">{t['cta2']}</a>
      <a class="btn spa-cta-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>

<section class="co2-sec" id="dates">
  <div class="wrap">
    <h2 class="co2-h">{t['weeks_h']}</h2>
    {weeks}
  </div>
</section>

<section class="co2-sec kb-flow-sec">
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

<section class="spa-final kb-final" style="background-image:url('{img("images/coaching/coaching-6.jpg")}');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-final-inner">
    <h2>{t['final_h']}</h2>
    <p>{t['final_p']}</p>
    <a class="btn btn-green spa-cta" href="#dates">{t['cta2']}</a>
  </div>
</section>

'''

def ld_for(t, L, page, url):
    seasons = SEASONS if page == 'hub' else [page]
    loc = {'@type': 'Place', 'name': 'Rackets Academy Salgesch',
           'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressRegion': 'VS', 'addressCountry': 'CH'}}
    org = {'@type': 'Organization', 'name': 'Rackets Academy', 'url': BASE}
    events = []
    for s in seasons:
        for a, b in WEEKS[s]:
            events.append({'@type': 'Event', 'name': t['name'][s] + ' · ' + drange(a, b, L) + ' · Rackets Academy',
                           'description': t['desc'][s], 'startDate': a.isoformat() + 'T09:00:00+01:00' if a.month not in (4, 5, 6, 7, 8, 9, 10) else a.isoformat() + 'T09:00:00+02:00',
                           'endDate': b.isoformat() + ('T12:00:00+02:00' if b.month in (4, 5, 6, 7, 8, 9, 10) else 'T12:00:00+01:00'),
                           'eventStatus': 'https://schema.org/EventScheduled', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
                           'location': loc, 'organizer': org, 'image': BASE + IMG[s], 'url': url,
                           'typicalAgeRange': '6-14',
                           'offers': {'@type': 'Offer', 'price': str(ndays(a, b) * PRICE_DAY), 'priceCurrency': 'CHF', 'availability': 'https://schema.org/InStock', 'url': url}})
    faq = {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}
    return {'@context': 'https://schema.org', '@graph': events + [faq]}

out = []
for L, t in T.items():
    pre = '' if L == 'en' else '../'
    d = '' if L == 'en' else L + '/'
    for page in ['hub'] + SEASONS:
        slug = SLUG[page]
        url = BASE + d + slug
        s = open(d + 'spa-and-sauna.html').read()
        a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
        b = s.index('<footer')
        s = s[:a] + body(t, L, page, pre) + s[b:]
        s = s.replace('spa-and-sauna.html', slug)
        s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
        s = re.sub(r'<title>.*?</title>', '<title>' + t['title'][page] + '</title>', s, count=1, flags=re.S)
        esc = lambda x: x.replace('"', '&quot;')
        for k in ['name="description"', 'property="og:description"']:
            s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + esc(t['desc'][page]) + '"', s)
        s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + esc(t['title'][page]) + '"', s)
        s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="' + BASE + IMG[page] + '"', s)
        s = s.replace('</head>', '<script type="application/ld+json" id="ld-kc">' + json.dumps(ld_for(t, L, page, url), ensure_ascii=False) + '</script>\n</head>', 1)
        s = s.replace('class="active"', '')
        open(d + slug, 'w').write(s)
        out.append((d + slug, len(t['title'][page]), len(t['desc'][page])))
for o in out:
    print(*o)
