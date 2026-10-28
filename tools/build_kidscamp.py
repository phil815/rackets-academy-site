"""Kids holiday padel camps Salgesch (EN/FR/DE): hub kids-camp.html + kids-camp-winter/easter/summer.html,
plus the camps overview camps.html (kids camps + Ski &Padel).
Built from the spa page shell (like build_birthday.py). 6-14 years, 20 spots per week, CHF 50 per half day.
Online booking: kidscamp.js -> Shop Apps Script (Camps.gs, campId kids-YYYY-MM-DD) -> SumUp.
The week list must match KIDS_CAMPS_ in Camps.gs (rackets-pl-data). Rerun: python3 tools/build_kidscamp.py"""
import re, json, urllib.parse, datetime as dt
WA_SA = '41772780115'
BASE = 'https://www.racketsacademy.ch/'
SHOP = 'https://script.google.com/macros/s/AKfycbwLWTwsILcSkAHe9FSKjicU1pUk5s3nxSnS4PQ2Tws2RVejiHjBltJJ8gKpmIe3JLRe/exec'
PRICE_DAY = 50
CAP = 20
D = dt.date
WEEKS = {   # (start, end, slot)  am = 9-12, pm = 14-17 (after skiing)
  'winter': [(D(2027, 1, 4), D(2027, 1, 8), 'pm'), (D(2027, 2, 8), D(2027, 2, 12), 'pm')],
  'easter': [(D(2027, 3, 30), D(2027, 4, 2), 'am')],
  'summer': [(D(2027, 7, 12), D(2027, 7, 16), 'am'), (D(2027, 8, 9), D(2027, 8, 13), 'am')],
}
SEASONS = ['winter', 'easter', 'summer']
SLUG = {'hub': 'kids-camp.html', 'winter': 'kids-camp-winter.html', 'easter': 'kids-camp-easter.html', 'summer': 'kids-camp-summer.html'}
IMG = {'hub': 'images/coaching/coaching-2.jpg', 'winter': 'images/coaching/coaching-3.jpg', 'easter': 'images/coaching/coaching-4.jpg', 'summer': 'images/coaching/coaching-5.jpg'}
ICON = {'winter': '❄️', 'easter': '🐣', 'summer': '☀️'}
SLOT = {'am': ('09:00', '12:00'), 'pm': ('14:00', '17:00')}
MON = {'en': 'January February March April May June July August September October November December'.split(),
       'fr': 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'.split(),
       'de': 'Januar Februar März April Mai Juni Juli August September Oktober November Dezember'.split()}

def drange(a, b, L):
    m, d = MON[L], ('.' if L == 'de' else '')
    if a.month == b.month:
        return f'{a.day}{d} – {b.day}{d} {m[b.month-1]} {b.year}'
    return f'{a.day}{d} {m[a.month-1]} – {b.day}{d} {m[b.month-1]} {b.year}'

ndays = lambda a, b: (b - a).days + 1

T = {
'en': dict(
  time={'am': '9:00–12:00', 'pm': '14:00–17:00'},
  name={'hub': 'Kids padel holiday camps', 'winter': 'Winter camp', 'easter': 'Easter camp', 'summer': 'Summer camp'},
  title={'hub': 'Kids padel day camps, holidays 2027 – Sierre, Valais | Rackets Academy',
         'winter': 'Kids padel camp January & February 2027, Valais | Rackets Academy',
         'easter': 'Kids padel camp, Easter holidays 2027, Valais | Rackets Academy',
         'summer': 'Kids padel summer camp 2027, Valais | Rackets Academy'},
  desc={'hub': 'Padel camps for kids aged 6–14 in the Valais school holidays 2027: winter, Easter and summer in Salgesch, 5 min from Sierre. 20 spots per week, CHF 250, book online.',
        'winter': 'Afternoon padel camp after skiing for kids aged 6–14: January and carnival holidays 2027 in Salgesch, 5 min from Sierre. 14:00–17:00, CHF 250 per week.',
        'easter': 'Padel camp for kids aged 6–14 in the Easter holidays 2027 in Salgesch, 5 min from Sierre. 4 mornings 9:00–12:00, indoors, rackets included, CHF 200.',
        'summer': 'Padel summer camp 2027 for kids aged 6–14 in Salgesch, 5 min from Sierre: 12–16 July and 9–13 August, mornings 9–12, indoors, CHF 250 per week.'},
  kicker={'hub': 'Kids camps 2027 · Salgesch', 'winter': 'January & February 2027 · Salgesch', 'easter': 'Easter holidays 2027 · Salgesch', 'summer': 'Summer holidays 2027 · Salgesch'},
  h1={'hub': 'Holidays? Padel camp!', 'winter': 'Ski in the morning, padel in the afternoon.', 'easter': 'Easter holidays on the padel court.', 'summer': 'The summer camp kids ask for again.'},
  lede={'hub': 'Three hours a day of padel, games and new friends for kids aged 6–14 — in the winter, Easter and summer holidays, indoors in Salgesch.',
        'winter': 'Afternoon camp in the January and carnival holidays: after the slopes, five afternoons of padel, games and matches. Warm and indoors.',
        'easter': 'Four mornings of padel, games and a mini tournament in the Easter holidays — indoors in Salgesch.',
        'summer': 'Two summer weeks, when most families are back home: padel, games and matches every morning, indoors and out of the heat.'},
  chips=['Age 6–14', '20 spots per week', 'CHF 250 per week', 'Rackets included'],
  days={'mf': 'Mon–Fri', 'tf': 'Tue–Fri'},
  cta='Book online', cta2='See the dates',
  wa='Hola! I have a question about the kids padel camp: {w}.', wa_q='Questions? WhatsApp',
  left='{n} of 20 spots left', last='Last spot!', sold='Fully booked',
  flow_h={'hub': 'A camp day', 'am': 'A camp morning', 'pm': 'A camp afternoon'},
  flow=[('Warm-up & technique', 'Coordination games, then the basics: forehand, backhand, volley, the walls.'),
        ('Break & games', 'Short snack break, then team games on court.'),
        ('Matches', 'Real points and a mini tournament on the last day.')],
  weeks_h='Dates & booking', days_lbl='{n} days',
  facts_h='Good to know',
  facts=[('📍', 'Where', 'Rackets Academy Salgesch, Littenstrasse 30 — 5 min from Sierre, 15 min from Crans-Montana, 20 min from Sion and Visp.'),
         ('👧', 'Who', 'Kids aged 6–14, beginners and players. Groups by age and level, max. 20 kids per week.'),
         ('🎒', 'What to bring', 'Indoor sports shoes, sportswear, a water bottle and a snack. Rackets and balls are provided.')],
  faq_h='Questions from parents',
  faq=[('How much does the kids padel camp cost?', 'CHF 250 per week (5 days, 3 hours a day). The Easter camp has 4 days and costs CHF 200. Rackets and balls are included.'),
       ('Is it a day camp?', 'Yes — a sports day camp without overnight stay: 3 hours a day in Salgesch, 5 min from Sierre, 15 min from Crans-Montana, 20 min from Sion and Visp. Ideal alongside ski school or other holiday activities.'),
       ('When does the camp take place?', 'January and February: afternoons 14:00–17:00, so kids can ski in the morning. Easter and summer: mornings 9:00–12:00.'),
       ('Does my child need to know how to play padel?', 'No. Kids are grouped by age and level, so beginners and players both get the right coaching.'),
       ('How many kids are in a camp?', 'Maximum 20 kids per week, split into small groups by age and level.'),
       ('How do I book?', 'Online on this page: choose the week, enter your children’s names and ages and pay by card or TWINT. You get the confirmation by email right away.')],
  more_h='All kids camps', season_lbl={'winter': 'Winter 2027', 'easter': 'Easter 2027', 'summer': 'Summer 2027'},
  season_sub={'winter': 'January & February · afternoons', 'easter': 'Easter holidays · mornings', 'summer': 'July & August · mornings'},
  final_h='20 spots per week — book early.', final_p='Salgesch · age 6–14 · CHF 250 per week',
  m_name='Parent’s name', m_mail='Email', m_mail_n='(confirmation is sent here)', m_tel='Mobile number', m_tel_n='(for updates on the camp)',
  m_n='Number of children', m_kids='Name and age of each child', m_kid='Child', m_age='Age', m_notes='Anything we should know?', m_notes_n='(optional — allergies, health)',
  m_go='Continue to payment', m_total='Total',
  camps=dict(title='Camps for kids and adults in Valais | Rackets Academy',
             desc='All Rackets Academy camps in Salgesch: kids padel holiday camps 2027 (winter, Easter, summer) and Ski &Padel weekends for adults in February 2027.',
             kicker='Camps · Salgesch', h1='Camps for every age.', lede='Holiday camps for kids aged 6–14 and Ski &Padel weekends for adults — all in Salgesch, 5 min from Sierre.',
             kids_h='Kids holiday camps 2027', kids_p='Age 6–14 · 3 hours a day · CHF 250 per week · book online',
             ski_h='Ski &Padel weekends', ski_p='For adults · February 2027 · ski in the morning, padel in the afternoon, 3 nights in Salgesch.', ski_cta='Ski &Padel →')),
'fr': dict(
  time={'am': '9h–12h', 'pm': '14h–17h'},
  name={'hub': 'Camps de padel pour enfants', 'winter': "Camp d'hiver", 'easter': 'Camp de Pâques', 'summer': "Camp d'été"},
  title={'hub': 'Camp de vacances padel enfants Sierre & Valais 2027 | Rackets Academy',
         'winter': 'Camp padel enfants janvier et Carnaval 2027, Valais | Rackets Academy',
         'easter': 'Camp padel enfants vacances de Pâques 2027, Valais | Rackets Academy',
         'summer': "Camp d'été padel enfants 2027, Sierre Valais | Rackets Academy"},
  desc={'hub': "Camps de padel pour enfants de 6 à 14 ans pendant les vacances scolaires 2027 : hiver, Pâques et été à Salgesch, 5 min de Sierre. 20 places par semaine, CHF 250, réservation en ligne.",
        'winter': "Camp de padel l'après-midi, après le ski, pour les 6–14 ans : vacances de janvier et de Carnaval 2027 à Salgesch, 5 min de Sierre. 14h–17h, CHF 250 la semaine.",
        'easter': "Camp de padel pour enfants de 6 à 14 ans pendant les vacances de Pâques 2027 à Salgesch, 5 min de Sierre. 4 matins 9h–12h, en salle, raquettes incluses, CHF 200.",
        'summer': "Camp d'été de padel 2027 pour les 6–14 ans à Salgesch, 5 min de Sierre : 12–16 juillet et 9–13 août, matins 9h–12h, en salle, CHF 250 la semaine."},
  kicker={'hub': 'Camps enfants 2027 · Salgesch', 'winter': 'Janvier & février 2027 · Salgesch', 'easter': 'Vacances de Pâques 2027 · Salgesch', 'summer': "Vacances d'été 2027 · Salgesch"},
  h1={'hub': 'Les vacances ? Camp de padel !', 'winter': "Ski le matin, padel l'après-midi.", 'easter': 'Les vacances de Pâques sur le terrain de padel.', 'summer': "Le camp d'été que les enfants redemandent."},
  lede={'hub': "Trois heures par jour de padel, de jeux et de nouveaux copains pour les 6–14 ans — pendant les vacances d'hiver, de Pâques et d'été, en salle à Salgesch.",
        'winter': "Camp l'après-midi pendant les vacances de janvier et de Carnaval : après les pistes, cinq après-midis de padel, de jeux et de matchs. Au chaud, en salle.",
        'easter': "Quatre matinées de padel, de jeux et un mini-tournoi pendant les vacances de Pâques — en salle à Salgesch.",
        'summer': "Deux semaines d'été, quand la plupart des familles sont de retour : padel, jeux et matchs chaque matin, en salle et à l'abri de la chaleur."},
  chips=['6–14 ans', '20 places par semaine', 'CHF 250 la semaine', 'Raquettes fournies'],
  days={'mf': 'Lu–ve', 'tf': 'Ma–ve'},
  cta='Réserver en ligne', cta2='Voir les dates',
  wa="Hola ! J'ai une question sur le camp de padel enfants : {w}.", wa_q='Des questions ? WhatsApp',
  left='Plus que {n} places sur 20', last='Dernière place !', sold='Complet',
  flow_h={'hub': 'Une journée de camp', 'am': 'Une matinée de camp', 'pm': "Un après-midi de camp"},
  flow=[('Échauffement & technique', 'Jeux de coordination, puis les bases : coup droit, revers, volée, les vitres.'),
        ('Pause & jeux', "Petite pause goûter, puis jeux d'équipe sur le terrain."),
        ('Matchs', 'De vrais points et un mini-tournoi le dernier jour.')],
  weeks_h='Dates & réservation', days_lbl='{n} jours',
  facts_h='Bon à savoir',
  facts=[('📍', 'Où', 'Rackets Academy Salgesch, Littenstrasse 30 — à 5 min de Sierre, 15 min de Crans-Montana, 20 min de Sion.'),
         ('👧', 'Pour qui', "Enfants de 6 à 14 ans, débutants ou joueurs. Groupes par âge et niveau, 20 enfants max. par semaine."),
         ('🎒', 'À prendre', "Chaussures de salle, tenue de sport, gourde et goûter. Raquettes et balles fournies.")],
  faq_h='Questions des parents',
  faq=[('Combien coûte le camp de padel pour enfants ?', 'CHF 250 la semaine (5 jours, 3 heures par jour). Le camp de Pâques dure 4 jours et coûte CHF 200. Raquettes et balles incluses.'),
       ('Est-ce un camp de jour ?', 'Oui — un camp sportif de jour, sans nuitée : 3 heures par jour à Salgesch, à 5 min de Sierre, 15 min de Crans-Montana et 20 min de Sion. Idéal en complément de l’école de ski ou d’un centre aéré.'),
       ('À quelle heure a lieu le camp ?', "Janvier et février : l'après-midi de 14h à 17h, pour pouvoir skier le matin. Pâques et été : le matin de 9h à 12h."),
       ("Mon enfant doit-il déjà savoir jouer au padel ?", "Non. Les enfants sont répartis par âge et par niveau : débutants comme joueurs reçoivent le bon entraînement."),
       ("Combien d'enfants par camp ?", "20 enfants maximum par semaine, en petits groupes par âge et niveau."),
       ('Comment réserver ?', "En ligne sur cette page : choisissez la semaine, indiquez le prénom et l'âge de vos enfants et payez par carte ou TWINT. La confirmation arrive tout de suite par e-mail.")],
  more_h='Tous les camps enfants', season_lbl={'winter': 'Hiver 2027', 'easter': 'Pâques 2027', 'summer': 'Été 2027'},
  season_sub={'winter': "Janvier & février · après-midi", 'easter': 'Vacances de Pâques · matin', 'summer': 'Juillet & août · matin'},
  final_h='20 places par semaine — réservez tôt.', final_p='Salgesch · 6–14 ans · CHF 250 la semaine',
  m_name='Nom du parent', m_mail='E-mail', m_mail_n='(la confirmation est envoyée ici)', m_tel='Mobile', m_tel_n='(pour les infos sur le camp)',
  m_n="Nombre d'enfants", m_kids='Prénom et âge de chaque enfant', m_kid='Enfant', m_age='Âge', m_notes='Quelque chose à savoir ?', m_notes_n='(facultatif — allergies, santé)',
  m_go='Continuer vers le paiement', m_total='Total',
  camps=dict(title='Camps pour enfants et adultes en Valais | Rackets Academy',
             desc='Tous les camps de la Rackets Academy à Salgesch : camps de padel pour enfants 2027 (hiver, Pâques, été) et week-ends Ski &Padel pour adultes en février 2027.',
             kicker='Camps · Salgesch', h1='Des camps pour tous les âges.', lede="Camps de vacances pour les 6–14 ans et week-ends Ski &Padel pour adultes — à Salgesch, 5 min de Sierre.",
             kids_h='Camps de vacances enfants 2027', kids_p='6–14 ans · 3 heures par jour · CHF 250 la semaine · réservation en ligne',
             ski_h='Week-ends Ski &Padel', ski_p="Pour adultes · février 2027 · ski le matin, padel l'après-midi, 3 nuits à Salgesch.", ski_cta='Ski &Padel →')),
'de': dict(
  time={'am': '9–12 Uhr', 'pm': '14–17 Uhr'},
  name={'hub': 'Padel-Feriencamps für Kinder', 'winter': 'Wintercamp', 'easter': 'Ostercamp', 'summer': 'Sommercamp'},
  title={'hub': 'Sportcamp Padel für Kinder – Feriencamp Wallis 2027 | Rackets Academy',
         'winter': 'Kinder-Padelcamp Januar & Fasnacht 2027, Wallis | Rackets Academy',
         'easter': 'Kinder-Padelcamp Osterferien 2027, Oberwallis | Rackets Academy',
         'summer': 'Padel-Sommercamp für Kinder 2027, Wallis | Rackets Academy'},
  desc={'hub': 'Padel-Camps für Kinder von 6 bis 14 Jahren in den Schulferien 2027: Winter, Ostern und Sommer in Salgesch, 20 Min. ab Visp. 20 Plätze pro Woche, CHF 250, online buchen.',
        'winter': 'Padel-Camp am Nachmittag nach dem Skifahren für Kinder von 6 bis 14: Januar- und Fasnachtsferien 2027 in Salgesch, 20 Min. ab Visp. 14–17 Uhr, CHF 250 pro Woche.',
        'easter': 'Padel-Camp für Kinder von 6 bis 14 Jahren in den Osterferien 2027 in Salgesch, 20 Min. ab Visp. 4 Vormittage 9–12 Uhr, drinnen, Schläger inklusive, CHF 200.',
        'summer': 'Padel-Sommercamp 2027 für Kinder von 6 bis 14 in Salgesch, 20 Min. ab Visp: 12.–16. Juli und 9.–13. August, vormittags 9–12 Uhr, CHF 250 pro Woche.'},
  kicker={'hub': 'Kindercamps 2027 · Salgesch', 'winter': 'Januar & Februar 2027 · Salgesch', 'easter': 'Osterferien 2027 · Salgesch', 'summer': 'Sommerferien 2027 · Salgesch'},
  h1={'hub': 'Ferien? Padel-Camp!', 'winter': 'Morgens Ski, nachmittags Padel.', 'easter': 'Osterferien auf dem Padelplatz.', 'summer': 'Das Sommercamp, das Kinder nochmals wollen.'},
  lede={'hub': 'Drei Stunden pro Tag Padel, Spiele und neue Freunde für Kinder von 6 bis 14 — in den Winter-, Oster- und Sommerferien, drinnen in Salgesch.',
        'winter': 'Nachmittagscamp in den Januar- und Fasnachtsferien: nach der Piste fünf Nachmittage Padel, Spiele und Matches. Warm und drinnen.',
        'easter': 'Vier Vormittage Padel, Spiele und ein Mini-Turnier in den Osterferien — drinnen in Salgesch.',
        'summer': 'Zwei Sommerwochen, wenn die meisten Familien wieder zu Hause sind: jeden Vormittag Padel, Spiele und Matches, drinnen und ohne Hitze.'},
  chips=['6–14 Jahre', '20 Plätze pro Woche', 'CHF 250 pro Woche', 'Schläger inklusive'],
  days={'mf': 'Mo–Fr', 'tf': 'Di–Fr'},
  cta='Online buchen', cta2='Daten ansehen',
  wa='Hola! Ich habe eine Frage zum Kinder-Padelcamp: {w}.', wa_q='Fragen? WhatsApp',
  left='Noch {n} von 20 Plätzen', last='Letzter Platz!', sold='Ausgebucht',
  flow_h={'hub': 'Ein Camp-Tag', 'am': 'Ein Camp-Vormittag', 'pm': 'Ein Camp-Nachmittag'},
  flow=[('Aufwärmen & Technik', 'Koordinationsspiele, dann die Basics: Vorhand, Rückhand, Volley, die Wände.'),
        ('Pause & Spiele', 'Kurze Znüni- bzw. Zvieri-Pause, dann Teamspiele auf dem Platz.'),
        ('Matches', 'Echte Punkte und am letzten Tag ein Mini-Turnier.')],
  weeks_h='Daten & Buchung', days_lbl='{n} Tage',
  facts_h='Gut zu wissen',
  facts=[('📍', 'Wo', 'Rackets Academy Salgesch, Littenstrasse 30 — 5 Min. ab Siders und Leuk, 20 Min. ab Visp, 30 Min. ab Brig.'),
         ('👧', 'Für wen', 'Kinder von 6 bis 14 Jahren, Anfänger und Spieler. Gruppen nach Alter und Niveau, max. 20 Kinder pro Woche.'),
         ('🎒', 'Mitnehmen', 'Hallenschuhe, Sportkleider, Trinkflasche und Znüni/Zvieri. Schläger und Bälle stellen wir.')],
  faq_h='Fragen von Eltern',
  faq=[('Was kostet das Kinder-Padelcamp?', 'CHF 250 pro Woche (5 Tage, 3 Stunden pro Tag). Das Ostercamp hat 4 Tage und kostet CHF 200. Schläger und Bälle sind inklusive.'),
       ('Ist es ein Tagescamp?', 'Ja — ein Sportcamp ohne Übernachtung: 3 Stunden pro Tag in Salgesch, 5 Min. ab Siders und Leuk, 20 Min. ab Visp, 30 Min. ab Brig. Ideal neben Skischule, Ferienpass oder anderen Ferienangeboten.'),
       ('Wann findet das Camp statt?', 'Januar und Februar: nachmittags 14–17 Uhr, damit die Kinder morgens Ski fahren können. Ostern und Sommer: vormittags 9–12 Uhr.'),
       ('Muss mein Kind schon Padel spielen können?', 'Nein. Die Kinder spielen in Gruppen nach Alter und Niveau — Anfänger wie Fortgeschrittene bekommen das passende Training.'),
       ('Wie viele Kinder sind im Camp?', 'Maximal 20 Kinder pro Woche, in kleinen Gruppen nach Alter und Niveau.'),
       ('Wie buche ich?', 'Online auf dieser Seite: Woche wählen, Name und Alter der Kinder eintragen und mit Karte oder TWINT bezahlen. Die Bestätigung kommt sofort per Mail.')],
  more_h='Alle Kindercamps', season_lbl={'winter': 'Winter 2027', 'easter': 'Ostern 2027', 'summer': 'Sommer 2027'},
  season_sub={'winter': 'Januar & Februar · nachmittags', 'easter': 'Osterferien · vormittags', 'summer': 'Juli & August · vormittags'},
  final_h='20 Plätze pro Woche — früh buchen.', final_p='Salgesch · 6–14 Jahre · CHF 250 pro Woche',
  m_name='Name eines Elternteils', m_mail='E-Mail', m_mail_n='(dorthin geht die Bestätigung)', m_tel='Handynummer', m_tel_n='(für Infos zum Camp)',
  m_n='Anzahl Kinder', m_kids='Name und Alter jedes Kindes', m_kid='Kind', m_age='Alter', m_notes='Sollen wir etwas wissen?', m_notes_n='(optional — Allergien, Gesundheit)',
  m_go='Weiter zur Zahlung', m_total='Total',
  camps=dict(title='Camps für Kinder und Erwachsene im Wallis | Rackets Academy',
             desc='Alle Camps der Rackets Academy in Salgesch: Padel-Feriencamps für Kinder 2027 (Winter, Ostern, Sommer) und Ski &Padel Wochenenden für Erwachsene im Februar 2027.',
             kicker='Camps · Salgesch', h1='Camps für jedes Alter.', lede='Feriencamps für Kinder von 6 bis 14 und Ski &Padel Wochenenden für Erwachsene — in Salgesch, 20 Min. ab Visp.',
             kids_h='Kinder-Feriencamps 2027', kids_p='6–14 Jahre · 3 Stunden pro Tag · CHF 250 pro Woche · online buchen',
             ski_h='Ski &Padel Wochenenden', ski_p='Für Erwachsene · Februar 2027 · morgens Ski, nachmittags Padel, 3 Nächte in Salgesch.', ski_cta='Ski &Padel →')),
}

def camp_id(a):
    return 'kids-' + a.isoformat()

def week_label(t, L, a, b, slot):
    return drange(a, b, L) + ' · ' + t['time'][slot]

def week_rows(t, L, season):
    rows = ''
    for a, b, slot in WEEKS[season]:
        n = ndays(a, b)
        price = n * PRICE_DAY
        lab = week_label(t, L, a, b, slot)
        dd = t['days']['mf'] if n == 5 else t['days']['tf']
        rows += (f'<div class="kc-week" data-camp="{camp_id(a)}">'
                 f'<div><strong>{drange(a, b, L)}</strong><span>{dd} {t["time"][slot]} · CHF {price}</span><span class="kc-left"></span></div>'
                 f'<button type="button" class="btn btn-green kc-book" data-camp="{camp_id(a)}" data-pp="{price}" data-label="{t["season_lbl"][season]} · {lab}">{t["cta"]}</button></div>')
    return rows

def modal(t, L):
    return f'''
<div class="buy-modal-overlay" id="buy-modal-overlay">
  <div class="buy-modal">
    <button type="button" class="buy-modal-close" id="buy-modal-close" aria-label="Close">&times;</button>
    <h3 id="buy-modal-title"></h3>
    <div class="buy-modal-price" id="buy-modal-price"></div>
    <form id="buy-modal-form" class="shop-form" method="POST" action="{SHOP}" target="_blank">
      <input type="hidden" name="formType" value="camp">
      <input type="hidden" name="campId" id="modal-campId">
      <input type="hidden" name="campPackage" id="modal-campPackage" value="kid1">
      <input type="hidden" name="price" id="modal-price">
      <label class="shop-field">{t['m_n']}<select id="kc-n"><option value="1">1</option><option value="2">2</option><option value="3">3</option></select></label>
      <div class="shop-field" id="kc-kids-wrap" data-kid="{t['m_kid']}" data-age="{t['m_age']}">{t['m_kids']}<div id="kc-kids"></div><input type="hidden" name="participants"></div>
      <label class="shop-field">{t['m_name']}<input type="text" name="buyerName" required autocomplete="name"></label>
      <label class="shop-field">{t['m_mail']} <span style="font-weight:400; opacity:.7;">{t['m_mail_n']}</span><input type="email" name="buyerEmail" required autocomplete="email"></label>
      <label class="shop-field">{t['m_tel']} <span style="font-weight:400; opacity:.7;">{t['m_tel_n']}</span><input type="tel" name="phone" required autocomplete="tel"></label>
      <label class="shop-field">{t['m_notes']} <span style="font-weight:400; opacity:.7;">{t['m_notes_n']}</span><textarea name="notes" rows="2" maxlength="300"></textarea></label>
      <button type="submit" class="btn btn-green" style="width:100%; text-align:center;">{t['m_go']}</button>
    </form>
  </div>
</div>
'''

def flow_html(t, page):
    if page == 'hub':
        badges, key = ['1 h', '2 h', '3 h'], 'hub'
    else:
        slot = WEEKS[page][0][2]
        s = SLOT[slot][0]
        h = int(s[:2])
        badges = [f'{h}:00', f'{h + 1}:15', f'{h + 2}:00'] if L_ != 'fr' else [f'{h}h00', f'{h + 1}h15', f'{h + 2}h00']
        key = slot
    return t['flow_h'][key], ''.join(f'<div class="kb-step"><span class="kb-badge">{b}</span><h3>{h}</h3><p>{p}</p></div>' for b, (h, p) in zip(badges, t['flow']))

def hero(t, img, kicker, h1, lede, chips, cta_href, cta, wa):
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in chips)
    return f'''
<section class="spa-hero co-hero kb-hero" style="background-image:url('{img}');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{kicker}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="spa-chips">{chips}</div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="{cta_href}">{cta}</a>
      <a class="btn spa-cta-ghost" href="{wa}" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>
'''

def body(t, L, page, pre):
    seasons = SEASONS if page == 'hub' else [page]
    wa = 'https://wa.me/' + WA_SA + '?text=' + urllib.parse.quote(t['wa'].format(w=t['name'][page]))
    chips = list(t['chips'])
    if page == 'winter':
        chips[1] = t['days']['mf'] + ' ' + t['time']['pm']
    elif page == 'easter':
        chips[1], chips[2] = t['days']['tf'] + ' ' + t['time']['am'], 'CHF 200'
    elif page == 'summer':
        chips[1] = t['days']['mf'] + ' ' + t['time']['am']
    weeks = ''
    for s in seasons:
        weeks += (f'<h3 class="kc-season">{ICON[s]} {t["season_lbl"][s]} <span>· {t["season_sub"][s]}</span></h3>' if page == 'hub' else '') + '<div class="kc-weeks">' + week_rows(t, L, s) + '</div>'
    fh, flow = flow_html(t, page)
    facts = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['facts'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    more = ''.join(f'<a class="co2-b ow-more" href="{SLUG[s]}"><span class="co2-ic">{ICON[s]}</span><h3>{t["season_lbl"][s]} →</h3><p>{t["season_sub"][s]}</p></a>' for s in SEASONS if s != page)
    if page != 'hub':
        more = f'<a class="co2-b ow-more" href="{SLUG["hub"]}"><span class="co2-ic">🎾</span><h3>{t["name"]["hub"]} →</h3><p>{t["more_h"]}</p></a>' + more
    more += f'<a class="co2-b ow-more" href="ski-and-padel.html"><span class="co2-ic">⛷️</span><h3>{t["camps"]["ski_h"]} →</h3><p>{t["camps"]["ski_p"]}</p></a>'
    return hero(t, pre + IMG[page], t['kicker'][page], t['h1'][page], t['lede'][page], chips, '#dates', t['cta2'], wa) + f'''
<section class="co2-sec" id="dates">
  <div class="wrap" id="kc-book" data-left="{t['left']}" data-last="{t['last']}" data-sold="{t['sold']}" data-total="{t['m_total']}">
    <h2 class="co2-h">{t['weeks_h']}</h2>
    {weeks}
    <p class="kc-wa"><a href="{wa}" target="_blank" rel="noopener">{t['wa_q']} →</a></p>
  </div>
</section>

<section class="co2-sec kb-flow-sec">
  <div class="wrap">
    <h2 class="co2-h">{fh}</h2>
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

<section class="spa-final kb-final" style="background-image:url('{pre}images/coaching/coaching-6.jpg');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-final-inner">
    <h2>{t['final_h']}</h2>
    <p>{t['final_p']}</p>
    <a class="btn btn-green spa-cta" href="#dates">{t['cta2']}</a>
  </div>
</section>
''' + modal(t, L)

def camps_body(t, L, pre):
    c = t['camps']
    cards = ''.join(f'<a class="co2-b ow-more" href="{SLUG[s]}"><span class="co2-ic">{ICON[s]}</span><h3>{t["season_lbl"][s]} →</h3><p>{t["season_sub"][s]}</p></a>' for s in SEASONS)
    wa = 'https://wa.me/' + WA_SA + '?text=' + urllib.parse.quote(t['wa'].format(w='Camps'))
    return hero(t, pre + 'images/coaching/coaching-hero.jpg', c['kicker'], c['h1'], c['lede'], [t['chips'][0], 'Ski &Padel'], '#kids', t['cta2'], wa) + f'''
<section class="co2-sec" id="kids">
  <div class="wrap">
    <h2 class="co2-h">🎾 {c['kids_h']}</h2>
    <p class="kc-sub">{c['kids_p']}</p>
    <div class="co2-bens ow-mores kc-mores">{cards}</div>
    <p style="margin-top:16px;"><a class="btn btn-green" href="{SLUG['hub']}">{t['name']['hub']} →</a></p>
  </div>
</section>

<section class="co2-sec ow-day">
  <div class="wrap">
    <h2 class="co2-h">⛷️ {c['ski_h']}</h2>
    <p class="kc-sub">{c['ski_p']}</p>
    <p><a class="btn btn-green" href="ski-and-padel.html">{c['ski_cta']}</a></p>
  </div>
</section>
'''

def ld_for(t, L, page, url):
    seasons = SEASONS if page == 'hub' else [page]
    loc = {'@type': 'Place', 'name': 'Rackets Academy Salgesch',
           'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressRegion': 'VS', 'addressCountry': 'CH'}}
    org = {'@type': 'Organization', 'name': 'Rackets Academy', 'url': BASE}
    tz = lambda d: '+02:00' if D(d.year, 3, 28) <= d < D(d.year, 10, 31) else '+01:00'
    events = []
    for s in seasons:
        for a, b, slot in WEEKS[s]:
            events.append({'@type': 'Event', 'name': t['name'][s] + ' · ' + week_label(t, L, a, b, slot) + ' · Rackets Academy',
                           'description': t['desc'][s], 'startDate': f'{a.isoformat()}T{SLOT[slot][0]}:00{tz(a)}', 'endDate': f'{b.isoformat()}T{SLOT[slot][1]}:00{tz(b)}',
                           'eventStatus': 'https://schema.org/EventScheduled', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
                           'location': loc, 'organizer': org, 'image': BASE + IMG[s], 'url': url, 'typicalAgeRange': '6-14', 'maximumAttendeeCapacity': CAP,
                           'offers': {'@type': 'Offer', 'price': str(ndays(a, b) * PRICE_DAY), 'priceCurrency': 'CHF', 'availability': 'https://schema.org/InStock', 'url': url}})
    faq = {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}
    return {'@context': 'https://schema.org', '@graph': events + [faq]}

def shell(d, slug, html, title, desc, img, ld, scripts=''):
    s = open(d + 'spa-and-sauna.html').read()
    a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
    b = s.index('<footer')
    s = s[:a] + html + s[b:]
    s = s.replace('spa-and-sauna.html', slug)
    s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>' + title + '</title>', s, count=1, flags=re.S)
    esc = lambda x: x.replace('"', '&quot;')
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + esc(desc) + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + esc(title) + '"', s)
    s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="' + BASE + img + '"', s)
    if ld:
        s = s.replace('</head>', '<script type="application/ld+json" id="ld-kc">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
    s = s.replace('class="active"', '')
    if scripts:
        s = s.replace('</body>', scripts + '\n</body>', 1)
    open(d + slug, 'w').write(s)
    return d + slug

out = []
for L, t in T.items():
    L_ = L
    pre = '' if L == 'en' else '../'
    d = '' if L == 'en' else L + '/'
    for page in ['hub'] + SEASONS:
        url = BASE + d + SLUG[page]
        f = shell(d, SLUG[page], body(t, L, page, pre), t['title'][page], t['desc'][page], IMG[page], ld_for(t, L, page, url),
                  f'<script src="{pre}kidscamp.js?v=1"></script>')
        out.append((f, len(t['title'][page]), len(t['desc'][page])))
    c = t['camps']
    f = shell(d, 'camps.html', camps_body(t, L, pre), c['title'], c['desc'], 'images/coaching/coaching-hero.jpg', None)
    out.append((f, len(c['title']), len(c['desc'])))
for o in out:
    print(*o)
