"""Landing pages in EN/FR/DE, built from the spa-and-sauna.html shell (like build_visp.py):
padel-valais.html (pillar page «padel Valais / padel Wallis»), rackemix.html, padel-beer.html.
Run from repo root: python3 tools/build_landing.py"""
import re, json, urllib.parse

BASE = 'https://www.racketsacademy.ch/'
PT_SAL = 'https://playtomic.com/tenant/f89dfa07-4283-453e-8be3-316f9bd060d3'
PT_SION = 'https://playtomic.com/tenant/c2ce2a9e-ab52-4191-bf7f-0c0aa70a2701'
WA_NUM = '41772780115'
MAPS_SAL = 'https://www.google.com/maps/dir/?api=1&destination=Littenstrasse+30+3970+Salgesch'
MAPS_SION = 'https://www.google.com/maps/dir/?api=1&destination=Route+de+Pr%C3%A9jeux+16+1950+Sion'
LANGS = ['en', 'fr', 'de']
PRE = {'en': '', 'fr': '../', 'de': '../'}
DIR = {'en': '', 'fr': 'fr/', 'de': 'de/'}


def wa(text):
    return f'https://wa.me/{WA_NUM}?text=' + urllib.parse.quote(text)


def btn(href, label, green=True):
    ext = ' target="_blank" rel="noopener"' if href.startswith('http') else ''
    cls = 'btn btn-green spa-cta' if green else 'btn spa-cta-ghost'
    return f'<a class="{cls}" href="{href}"{ext}>{label}</a>'


def hero(img, pos, kicker, h1, lede, chips, b1, b2):
    ch = ''.join(f'<span class="spa-chip">{c}</span>' for c in chips)
    return f'''
<section class="spa-hero co-hero" style="background-image:url('{img}'); background-position:{pos};">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{kicker}</p>
    <h1>{h1}</h1>
    <p class="lede">{lede}</p>
    <div class="spa-chips">{ch}</div>
    <div class="hero-actions">{b1}{b2}</div>
  </div>
</section>
'''


def sec(h, inner, cls='co2-sec'):
    return f'''
<section class="{cls}">
  <div class="wrap">
    <h2 class="co2-h">{h}</h2>
    {inner}
  </div>
</section>
'''


def facs(items):
    return '<div class="ow-facs">' + ''.join(
        f'<div class="ow-fac"><span class="co2-ic">{e}</span><div><h3>{h}</h3><p>{a}</p><p class="ow-time">{b}</p></div></div>'
        for e, h, a, b in items) + '</div>'


def mores(items):
    return '<div class="co2-bens ow-mores">' + ''.join(
        f'<a class="co2-b ow-more" href="{l}"><span class="co2-ic">{e}</span><h3>{h} →</h3><p>{p}</p></a>'
        for e, h, p, l in items) + '</div>'


def near(items):
    return '<div class="spa-near">' + ''.join(
        f'<div class="spa-near-item"><strong>{a}</strong><span>{b}</span></div>' for a, b in items) + '</div>'


def faq(items, h):
    q = ''.join(f'<details><summary>{a}</summary><p>{b}</p></details>' for a, b in items)
    return f'''
<section class="section-tight">
  <div class="wrap">
    <h2>{h}</h2>
    <div class="spa-faq">{q}</div>
  </div>
</section>
'''


def final(img, pos, h, p, b1, b2):
    return f'''
<section class="spa-final" style="background-image:url('{img}'); background-position:{pos};">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-final-inner">
    <h2>{h}</h2>
    <p>{p}</p>
    <div class="hero-actions" style="justify-content:center;">{b1}{b2}</div>
  </div>
</section>
'''


# ---------------------------------------------------------------- padel-valais
def valais(L):
    pre = PRE[L]
    img = pre + 'images/photos/'
    T = {
     'en': dict(
        title='Padel in Valais – Sion & Salgesch near Sierre | Rackets Academy',
        desc='Padel in Valais: two clubs in Sion and Salgesch (near Sierre), indoor courts all year, open daily 7:00–23:30, from 17 CHF per person. Courses, tournaments, spa and bar.',
        kicker='Padel Valais · Sion &amp; Salgesch',
        h1='Padel in Valais — two clubs, open every day.',
        lede='Rackets Academy is padel in the heart of Valais: Sion and Salgesch near Sierre, indoor courts for every weather, coaches, weekly tournaments and the friendliest padel community in the canton.',
        chips=['Open daily 7:00–23:30', 'From 17 CHF per person', 'Indoor all year'],
        b1='Book in Salgesch', b2='Book in Sion',
        locs_h='Our two padel clubs in Valais',
        sal=('📍', 'Salgesch (near Sierre)', '4 indoor + 2 outdoor padel courts · pickleball · tennis · spa · bar · shop · Littenstrasse 30, 3970 Salgesch', 'Daily 7:00–23:30'),
        sion=('📍', 'Sion', '3 indoor padel courts · bar · shop · Route de Préjeux 16, 1950 Sion', 'Daily 7:00–23:30'),
        price_k='Prices', price_h='Padel from 17 CHF per person.',
        price_p='90 minutes indoor: 17 CHF per person Monday to Friday before 5 pm, 20 CHF per person from 5 pm and at weekends. Same price in Sion and Salgesch. Racket rental on site.',
        price_b='All prices',
        start_h='New to padel? Start here',
        more=[('🎓', 'Beginner session in Sion', 'Every Saturday 10–11, 25 CHF. No experience needed.', 'training.html'),
              ('📈', 'Playtomic level session', 'Every Saturday 11–12 in Sion: a coach sets your Playtomic level.', 'training.html'),
              ('🏆', 'Racketero', 'Our weekly tournament: matches against players at your level.', 'racketero.html'),
              ('🔀', 'Rackemix', 'Monthly mix tournament on Sunday morning, new partner every round.', 'rackemix.html'),
              ('🧒', 'Kids camps', 'Holiday padel camps in Salgesch for kids aged 6–14.', 'kids-camp.html'),
              ('🏢', 'Company events', 'Team events with padel, food and apéro in Sion or Salgesch.', 'company-events.html')],
        near_h='How far is your nearest court?',
        near=[('Sierre', '≈ 5 min to Salgesch'), ('Sion', 'in town'), ('Crans-Montana', '≈ 25 min to Salgesch'), ('Martigny', '≈ 25 min to Sion'), ('Nendaz', '≈ 20 min to Sion'), ('Visp', '≈ 20 min to Salgesch'), ('Leukerbad', '≈ 25 min to Salgesch'), ('Val d’Anniviers', '≈ 20 min to Salgesch')],
        faq_h='Padel in Valais: good to know',
        faq=[('Where can I play padel in Valais?', 'Rackets Academy has two padel clubs in Valais: in Sion (3 indoor courts) and in Salgesch near Sierre (4 indoor and 2 outdoor courts). Both are open every day from 7:00 to 23:30 and bookable on Playtomic.'),
             ('How much does padel cost in Valais?', 'At Rackets Academy a 90-minute indoor game costs 17 CHF per person on weekdays before 5 pm and 20 CHF per person from 5 pm and at weekends, the same in Sion and Salgesch.'),
             ('Can I play padel indoors in winter?', 'Yes. Our courts in Sion and four of the courts in Salgesch are indoors, so you can play all year, whatever the weather.'),
             ('I have never played. Where do I start?', 'Join the beginner session in Sion every Saturday from 10 to 11 (25 CHF), or book a court with friends and rent rackets on site. Our coaches also give private and group lessons.'),
             ('Is there padel near Sierre and Crans-Montana?', 'Yes: our Salgesch club is 5 minutes from Sierre and about 25 minutes from Crans-Montana, with parking in front of the hall.'),
             ('Do you have tournaments?', 'Every week: Racketero, plus the monthly Rackemix, Swiss Tennis padel tournaments and special events such as the 24-hour tournament.')],
        fin_h='See you on court.', fin_p='Book on Playtomic in 1 minute — Sion or Salgesch.'),
     'fr': dict(
        title='Padel Valais – Sion & Salgesch près de Sierre | Rackets Academy',
        desc='Padel en Valais : deux centres à Sion et Salgesch (près de Sierre), terrains indoor toute l’année, ouverts tous les jours 7h–23h30, dès 17 CHF par personne. Cours, tournois, spa et bar.',
        kicker='Padel Valais · Sion &amp; Salgesch',
        h1='Le padel en Valais — deux centres, ouverts tous les jours.',
        lede='La Rackets Academy, c’est le padel au cœur du Valais : Sion et Salgesch près de Sierre, des terrains indoor par tous les temps, des coachs, des tournois chaque semaine et la communauté padel la plus sympa du canton.',
        chips=['Ouvert tous les jours 7h–23h30', 'Dès 17 CHF par personne', 'Indoor toute l’année'],
        b1='Réserver à Salgesch', b2='Réserver à Sion',
        locs_h='Nos deux centres de padel en Valais',
        sal=('📍', 'Salgesch (près de Sierre)', '4 terrains de padel indoor + 2 outdoor · pickleball · tennis · spa · bar · shop · Littenstrasse 30, 3970 Salgesch', 'Tous les jours 7h–23h30'),
        sion=('📍', 'Sion', '3 terrains de padel indoor · bar · shop · Route de Préjeux 16, 1950 Sion', 'Tous les jours 7h–23h30'),
        price_k='Tarifs', price_h='Le padel dès 17 CHF par personne.',
        price_p='90 minutes en indoor : 17 CHF par personne du lundi au vendredi avant 17h, 20 CHF par personne dès 17h et le week-end. Même prix à Sion et à Salgesch. Location de raquettes sur place.',
        price_b='Tous les tarifs',
        start_h='Débutant ? Commence ici',
        more=[('🎓', 'Séance d’initiation à Sion', 'Chaque samedi de 10h à 11h, 25 CHF. Aucune expérience nécessaire.', 'training.html'),
              ('📈', 'Séance de niveau Playtomic', 'Chaque samedi de 11h à 12h à Sion : un coach détermine ton niveau Playtomic.', 'training.html'),
              ('🏆', 'Racketero', 'Notre tournoi hebdomadaire : des matchs contre des joueurs de ton niveau.', 'racketero.html'),
              ('🔀', 'Rackemix', 'Tournoi mix mensuel le dimanche matin, nouveau partenaire à chaque tour.', 'rackemix.html'),
              ('🧒', 'Camps enfants', 'Camps de padel pendant les vacances à Salgesch, 6–14 ans.', 'kids-camp.html'),
              ('🏢', 'Événements d’entreprise', 'Sorties d’équipe avec padel, repas et apéro à Sion ou Salgesch.', 'company-events.html')],
        near_h='À quelle distance est ton terrain ?',
        near=[('Sierre', '≈ 5 min de Salgesch'), ('Sion', 'en ville'), ('Crans-Montana', '≈ 25 min de Salgesch'), ('Martigny', '≈ 25 min de Sion'), ('Nendaz', '≈ 20 min de Sion'), ('Viège', '≈ 20 min de Salgesch'), ('Loèche-les-Bains', '≈ 25 min de Salgesch'), ('Val d’Anniviers', '≈ 20 min de Salgesch')],
        faq_h='Le padel en Valais : bon à savoir',
        faq=[('Où jouer au padel en Valais ?', 'La Rackets Academy a deux centres de padel en Valais : à Sion (3 terrains indoor) et à Salgesch près de Sierre (4 terrains indoor et 2 outdoor). Les deux sont ouverts tous les jours de 7h à 23h30 et se réservent sur Playtomic.'),
             ('Combien coûte le padel en Valais ?', 'À la Rackets Academy, une partie de 90 minutes en indoor coûte 17 CHF par personne en semaine avant 17h et 20 CHF par personne dès 17h et le week-end, au même prix à Sion et à Salgesch.'),
             ('Peut-on jouer au padel en indoor en hiver ?', 'Oui. Nos terrains de Sion et quatre terrains de Salgesch sont couverts : tu joues toute l’année, quelle que soit la météo.'),
             ('Je n’ai jamais joué. Par où commencer ?', 'Viens à la séance d’initiation à Sion chaque samedi de 10h à 11h (25 CHF), ou réserve un terrain entre amis et loue des raquettes sur place. Nos coachs donnent aussi des cours privés et en groupe.'),
             ('Y a-t-il du padel près de Sierre et Crans-Montana ?', 'Oui : notre centre de Salgesch est à 5 minutes de Sierre et à environ 25 minutes de Crans-Montana, avec parking devant la halle.'),
             ('Organisez-vous des tournois ?', 'Chaque semaine : le Racketero, plus le Rackemix mensuel, des tournois Swiss Tennis de padel et des événements spéciaux comme le tournoi de 24 heures.')],
        fin_h='On se voit sur le terrain.', fin_p='Réserve sur Playtomic en 1 minute — Sion ou Salgesch.'),
     'de': dict(
        title='Padel Wallis – Sitten & Salgesch bei Siders | Rackets Academy',
        desc='Padel im Wallis: zwei Zentren in Sitten und Salgesch (bei Siders), Indoor-Plätze das ganze Jahr, täglich 07:00–23:30 geöffnet, ab 17 CHF pro Person. Kurse, Turniere, Spa und Bar.',
        kicker='Padel Wallis · Sitten &amp; Salgesch',
        h1='Padel im Wallis — zwei Zentren, jeden Tag offen.',
        lede='Die Rackets Academy ist Padel mitten im Wallis: Sitten und Salgesch bei Siders, Indoor-Plätze bei jedem Wetter, Coaches, Turniere jede Woche und die herzlichste Padel-Community im Kanton.',
        chips=['Täglich 07:00–23:30', 'Ab 17 CHF pro Person', 'Indoor das ganze Jahr'],
        b1='In Salgesch buchen', b2='In Sitten buchen',
        locs_h='Unsere zwei Padelzentren im Wallis',
        sal=('📍', 'Salgesch (bei Siders)', '4 Padelplätze indoor + 2 outdoor · Pickleball · Tennis · Spa · Bar · Shop · Littenstrasse 30, 3970 Salgesch', 'Täglich 07:00–23:30'),
        sion=('📍', 'Sitten (Sion)', '3 Padelplätze indoor · Bar · Shop · Route de Préjeux 16, 1950 Sion', 'Täglich 07:00–23:30'),
        price_k='Preise', price_h='Padel ab 17 CHF pro Person.',
        price_p='90 Minuten indoor: 17 CHF pro Person Montag bis Freitag vor 17 Uhr, 20 CHF pro Person ab 17 Uhr und am Wochenende. Gleicher Preis in Sitten und Salgesch. Schlägermiete vor Ort.',
        price_b='Alle Preise',
        start_h='Neu beim Padel? Hier anfangen',
        more=[('🎓', 'Einsteiger-Session in Sitten', 'Jeden Samstag 10–11 Uhr, 25 CHF. Keine Erfahrung nötig.', 'training.html'),
              ('📈', 'Playtomic-Level-Session', 'Jeden Samstag 11–12 Uhr in Sitten: Ein Coach bestimmt dein Playtomic-Level.', 'training.html'),
              ('🏆', 'Racketero', 'Unser Wochenturnier: Spiele gegen Leute auf deinem Niveau.', 'racketero.html'),
              ('🔀', 'Rackemix', 'Monatliches Mix-Turnier am Sonntagmorgen, jede Runde ein neuer Partner.', 'rackemix.html'),
              ('🧒', 'Kindercamps', 'Padel-Feriencamps in Salgesch für Kinder von 6–14 Jahren.', 'kids-camp.html'),
              ('🏔️', 'Padel im Oberwallis', 'Alles für Leuk, Visp, Brig und Umgebung.', 'padel-oberwallis.html')],
        near_h='Wie weit ist dein nächster Platz?',
        near=[('Siders', '≈ 5 Min. nach Salgesch'), ('Sitten', 'in der Stadt'), ('Leuk', '≈ 10 Min. nach Salgesch'), ('Visp', '≈ 20 Min. nach Salgesch'), ('Brig', '≈ 30 Min. nach Salgesch'), ('Leukerbad', '≈ 25 Min. nach Salgesch'), ('Crans-Montana', '≈ 25 Min. nach Salgesch'), ('Martinach', '≈ 25 Min. nach Sitten')],
        faq_h='Padel im Wallis: gut zu wissen',
        faq=[('Wo kann man im Wallis Padel spielen?', 'Die Rackets Academy hat zwei Padelzentren im Wallis: in Sitten (3 Indoor-Plätze) und in Salgesch bei Siders (4 Indoor- und 2 Outdoor-Plätze). Beide sind täglich von 07:00 bis 23:30 offen und auf Playtomic buchbar.'),
             ('Was kostet Padel im Wallis?', 'Bei der Rackets Academy kostet ein 90-Minuten-Spiel indoor 17 CHF pro Person werktags vor 17 Uhr und 20 CHF pro Person ab 17 Uhr und am Wochenende, gleich in Sitten und Salgesch.'),
             ('Kann man im Winter indoor Padel spielen?', 'Ja. Unsere Plätze in Sitten und vier Plätze in Salgesch sind in der Halle: Du spielst das ganze Jahr, bei jedem Wetter.'),
             ('Ich habe noch nie gespielt. Wo fange ich an?', 'Komm zur Einsteiger-Session in Sitten jeden Samstag von 10 bis 11 Uhr (25 CHF), oder buch mit Freunden einen Platz und miete Schläger vor Ort. Unsere Coaches geben auch Einzel- und Gruppentrainings, in Salgesch auch auf Deutsch.'),
             ('Gibt es Padel im Oberwallis?', 'Unser Zentrum in Salgesch liegt an der Sprachgrenze: 10 Minuten ab Leuk, 20 Minuten ab Visp und 30 Minuten ab Brig, mit Parkplätzen vor der Halle.'),
             ('Gibt es Turniere?', 'Jede Woche: Racketero, dazu das monatliche Rackemix, Swiss-Tennis-Padelturniere und Spezialevents wie das 24-Stunden-Turnier.')],
        fin_h='Wir sehen uns auf dem Platz.', fin_p='Buch auf Playtomic in 1 Minute — Sitten oder Salgesch.'),
    }[L]
    body = hero(img + 'outdoor-salgesch.jpg', 'center 60%', T['kicker'], T['h1'], T['lede'], T['chips'],
                btn(PT_SAL, T['b1']), btn(PT_SION, T['b2'], False))
    body += sec(T['locs_h'], facs([T['sal'], T['sion']]) +
                f'<p class="ow-addr"><a href="{MAPS_SAL}" target="_blank" rel="noopener">Salgesch →</a> · <a href="{MAPS_SION}" target="_blank" rel="noopener">Sion →</a></p>')
    body += f'''
<section class="co2-sec ow-day">
  <div class="wrap co2-price">
    <p class="spa-kicker" style="color:var(--blue);">{T['price_k']}</p>
    <h2 class="co2-h">{T['price_h']}</h2>
    <p>{T['price_p']}</p>
    {btn('book.html#prices', T['price_b'])}
  </div>
</section>
'''
    body += sec(T['start_h'], mores(T['more']))
    body += sec(T['near_h'], near(T['near']), 'co2-sec co2-proof')
    body += faq(T['faq'], T['faq_h'])
    body += final(img + 'training-match.jpg', 'center 55%', T['fin_h'], T['fin_p'], btn(PT_SAL, T['b1']), btn(PT_SION, T['b2'], False))
    ld = [{'@type': 'SportsActivityLocation', 'name': 'Rackets Academy Salgesch', 'url': BASE + DIR[L] + 'padel-valais.html',
           'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressRegion': 'VS', 'addressCountry': 'CH'},
           'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'opens': '07:00', 'closes': '23:30'}]},
          {'@type': 'SportsActivityLocation', 'name': 'Rackets Academy Sion', 'url': BASE + DIR[L] + 'padel-valais.html',
           'address': {'@type': 'PostalAddress', 'streetAddress': 'Route de Préjeux 16', 'postalCode': '1950', 'addressLocality': 'Sion', 'addressRegion': 'VS', 'addressCountry': 'CH'},
           'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'opens': '07:00', 'closes': '23:30'}]}]
    return T, body, ld, img + 'outdoor-salgesch.jpg'


# ---------------------------------------------------------------- rackemix
RACKEMIX_DATES = ['2026-11-29', '2026-12-27', '2027-01-24', '2027-02-21', '2027-03-21']   # Events - Salgesch calendar, Sundays 10–12
MON = {'en': 'January February March April May June July August September October November December'.split(),
       'fr': 'janvier février mars avril mai juin juillet août septembre octobre novembre décembre'.split(),
       'de': 'Januar Februar März April Mai Juni Juli August September Oktober November Dezember'.split()}


def fdate(d, L):
    y, m, dd = map(int, d.split('-'))
    return {'en': f'Sun {dd} {MON[L][m-1]} {y}', 'fr': f'Dim. {dd} {MON[L][m-1]} {y}', 'de': f'So. {dd}. {MON[L][m-1]} {y}'}[L]


def rackemix(L):
    img = PRE[L] + 'images/photos/'
    T = {
     'en': dict(title='Rackemix – monthly padel mix tournament in Salgesch | Rackets Academy',
        desc='Rackemix: our monthly padel mix tournament in Salgesch near Sierre. Sunday 10–12, new partner every round, a drink after, 30 CHF per person. Sign up on Playtomic.',
        kicker='Monthly · Salgesch', h1='Rackemix — new partner every round.',
        lede='Our monthly mix tournament on Sunday morning: you sign up alone or with friends, we mix the teams every round. Good matches, good vibes, and a drink together after.',
        chips=['Sunday 10:00–12:00', '30 CHF per person', 'All levels welcome'], b1='Sign up on Playtomic', b2='See all events',
        how_h='How it works',
        how=[('📝', 'Sign up', 'On Playtomic, alone or with friends.', 'Salgesch'), ('🔀', 'Play', 'Short matches, a new partner every round.', '10:00–12:00'), ('🍻', 'Drink after', 'Meet everyone at the bar. The winner gets a 20 CHF voucher.', 'After the games')],
        dates_h='Next dates', dates_note='Sign-up for each date opens on Playtomic.',
        faq_h='Good to know',
        faq=[('Do I need a partner?', 'No. Rackemix is made for signing up alone: partners change every round.'),
             ('What level do I need?', 'You should know the basic rules and be able to keep a rally going. Beginners can start with our Saturday beginner session in Sion.'),
             ('What does it cost?', '30 CHF per person, court included. Racket rental on site if needed.'),
             ('Where is it?', 'At Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch, 5 minutes from Sierre.')],
        fin_h='See you on Sunday.', fin_p='30 CHF · Sunday 10–12 · Salgesch'),
     'fr': dict(title='Rackemix – tournoi de padel mix mensuel à Salgesch | Rackets Academy',
        desc='Rackemix : notre tournoi de padel mix mensuel à Salgesch près de Sierre. Dimanche 10h–12h, nouveau partenaire à chaque tour, un verre après, 30 CHF par personne. Inscription sur Playtomic.',
        kicker='Chaque mois · Salgesch', h1='Rackemix — un nouveau partenaire à chaque tour.',
        lede='Notre tournoi mix mensuel le dimanche matin : tu t’inscris seul ou entre amis, on mélange les équipes à chaque tour. De beaux matchs, une bonne ambiance et un verre ensemble après.',
        chips=['Dimanche 10h–12h', '30 CHF par personne', 'Tous niveaux'], b1='S’inscrire sur Playtomic', b2='Tous les événements',
        how_h='Comment ça marche',
        how=[('📝', 'Inscription', 'Sur Playtomic, seul ou entre amis.', 'Salgesch'), ('🔀', 'Jeu', 'Des matchs courts, un nouveau partenaire à chaque tour.', '10h–12h'), ('🍻', 'Un verre après', 'On se retrouve au bar. Le gagnant reçoit un bon de 20 CHF.', 'Après les matchs')],
        dates_h='Prochaines dates', dates_note='Les inscriptions ouvrent sur Playtomic pour chaque date.',
        faq_h='Bon à savoir',
        faq=[('Faut-il un partenaire ?', 'Non. Le Rackemix est fait pour s’inscrire seul : les partenaires changent à chaque tour.'),
             ('Quel niveau faut-il ?', 'Tu connais les règles de base et tu tiens un échange. Les débutants peuvent commencer par la séance d’initiation du samedi à Sion.'),
             ('Combien ça coûte ?', '30 CHF par personne, terrain compris. Location de raquettes sur place si besoin.'),
             ('Où ça se passe ?', 'À la Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch, à 5 minutes de Sierre.')],
        fin_h='On se voit dimanche.', fin_p='30 CHF · dimanche 10h–12h · Salgesch'),
     'de': dict(title='Rackemix – monatliches Padel-Mixturnier in Salgesch | Rackets Academy',
        desc='Rackemix: unser monatliches Padel-Mixturnier in Salgesch bei Siders. Sonntag 10–12 Uhr, jede Runde ein neuer Partner, danach ein Drink, 30 CHF pro Person. Anmeldung auf Playtomic.',
        kicker='Monatlich · Salgesch', h1='Rackemix — jede Runde ein neuer Partner.',
        lede='Unser monatliches Mixturnier am Sonntagmorgen: Du meldest dich allein oder mit Freunden an, wir mischen die Teams jede Runde neu. Gute Matches, gute Stimmung und danach ein Drink zusammen.',
        chips=['Sonntag 10:00–12:00', '30 CHF pro Person', 'Alle Niveaus'], b1='Auf Playtomic anmelden', b2='Alle Events',
        how_h='So läuft es',
        how=[('📝', 'Anmelden', 'Auf Playtomic, allein oder mit Freunden.', 'Salgesch'), ('🔀', 'Spielen', 'Kurze Matches, jede Runde ein neuer Partner.', '10:00–12:00'), ('🍻', 'Drink danach', 'Alle treffen sich an der Bar. Der Sieger bekommt einen 20-CHF-Gutschein.', 'Nach den Spielen')],
        dates_h='Nächste Daten', dates_note='Die Anmeldung für jedes Datum öffnet auf Playtomic.',
        faq_h='Gut zu wissen',
        faq=[('Brauche ich einen Partner?', 'Nein. Rackemix ist zum Alleine-Anmelden gemacht: Die Partner wechseln jede Runde.'),
             ('Welches Niveau brauche ich?', 'Du kennst die Grundregeln und kannst einen Ballwechsel halten. Einsteiger beginnen am besten mit der Samstags-Session in Sitten.'),
             ('Was kostet es?', '30 CHF pro Person, Platz inklusive. Schlägermiete vor Ort, falls nötig.'),
             ('Wo findet es statt?', 'In der Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch, 5 Minuten von Siders.')],
        fin_h='Wir sehen uns am Sonntag.', fin_p='30 CHF · Sonntag 10–12 Uhr · Salgesch'),
    }[L]
    body = hero(img + 'events-group.jpg', 'center 45%', T['kicker'], T['h1'], T['lede'], T['chips'],
                btn(PT_SAL, T['b1']), btn('events.html', T['b2'], False))
    body += sec(T['how_h'], facs(T['how']))
    dates = near([(fdate(d, L), '10:00–12:00') for d in RACKEMIX_DATES])
    body += sec(T['dates_h'], dates + f'<p class="ow-addr">{T["dates_note"]}</p>', 'co2-sec co2-proof')
    body += faq(T['faq'], T['faq_h'])
    body += final(img + 'events-friends.jpg', 'center 30%', T['fin_h'], T['fin_p'], btn(PT_SAL, T['b1']), btn('events.html', T['b2'], False))
    ld = [{'@type': 'Event', 'name': 'Rackemix', 'startDate': d + 'T10:00:00+01:00', 'endDate': d + 'T12:00:00+01:00',
           'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode', 'eventStatus': 'https://schema.org/EventScheduled',
           'location': {'@type': 'Place', 'name': 'Rackets Academy Salgesch', 'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressCountry': 'CH'}},
           'offers': {'@type': 'Offer', 'price': '30', 'priceCurrency': 'CHF', 'url': PT_SAL},
           'organizer': {'@type': 'Organization', 'name': 'Rackets Academy', 'url': BASE}, 'image': BASE + 'images/photos/events-group.jpg'}
          for d in RACKEMIX_DATES]
    return T, body, ld, img + 'events-group.jpg'


# ---------------------------------------------------------------- padel-beer
BEER_DATE = '2026-11-08'   # Events - Salgesch calendar


def beer(L):
    img = PRE[L] + 'images/photos/'
    w = wa({'en': 'Hola! I want to join Padel+Beer on 8 November.', 'fr': 'Hola ! Je veux m’inscrire au Padel+Beer du 8 novembre.', 'de': 'Hola! Ich möchte beim Padel+Beer am 8. November mitmachen.'}[L])
    T = {
     'en': dict(title='Padel+Beer – padel and a cold beer in Salgesch | Rackets Academy',
        desc='Padel+Beer in Salgesch near Sierre: play padel, then a cold beer at the bar with everyone from the courts. Next date Sunday 8 November 2026, 50 CHF per person.',
        kicker='Sunday · Salgesch', h1='Padel+Beer — play, then cheers.',
        lede='The relaxed Sunday in Salgesch: padel with players at your level, then a cold beer at the bar with everyone from the courts.',
        chips=['Sun 8 November 2026', '50 CHF per person', 'Salgesch'], b1='Sign up on WhatsApp', b2='See all events',
        how_h='What you get',
        how=[('🎾', 'Padel', 'Games with players at your level, court included.', 'Salgesch'), ('🍺', 'Beer', 'A cold beer at the bar after playing.', 'After the games'), ('🤝', 'People', 'Meet the Rackets community in a relaxed setting.', 'All levels')],
        faq_h='Good to know',
        faq=[('Can I come alone?', 'Yes. Sign up alone or with friends, we make the games.'),
             ('What does it cost?', '50 CHF per person.'),
             ('Do I need my own racket?', 'No, you can rent one on site.'),
             ('Where is it?', 'At Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch, 5 minutes from Sierre.')],
        fin_h='Cheers on Sunday.', fin_p='50 CHF · Sun 8 November 2026 · Salgesch'),
     'fr': dict(title='Padel+Beer – padel et bière fraîche à Salgesch | Rackets Academy',
        desc='Padel+Beer à Salgesch près de Sierre : joue au padel, puis une bière bien fraîche au bar avec tout le monde. Prochaine date dimanche 8 novembre 2026, 50 CHF par personne.',
        kicker='Dimanche · Salgesch', h1='Padel+Beer — on joue, puis santé !',
        lede='Le dimanche détente à Salgesch : du padel avec des joueurs de ton niveau, puis une bière fraîche au bar avec tout le monde.',
        chips=['Dim. 8 novembre 2026', '50 CHF par personne', 'Salgesch'], b1='S’inscrire sur WhatsApp', b2='Tous les événements',
        how_h='Au programme',
        how=[('🎾', 'Padel', 'Des matchs avec des joueurs de ton niveau, terrain compris.', 'Salgesch'), ('🍺', 'Bière', 'Une bière fraîche au bar après le jeu.', 'Après les matchs'), ('🤝', 'Rencontres', 'La communauté Rackets dans une ambiance détendue.', 'Tous niveaux')],
        faq_h='Bon à savoir',
        faq=[('Je peux venir seul ?', 'Oui. Inscris-toi seul ou entre amis, on organise les matchs.'),
             ('Combien ça coûte ?', '50 CHF par personne.'),
             ('Faut-il ma propre raquette ?', 'Non, tu peux en louer une sur place.'),
             ('Où ça se passe ?', 'À la Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch, à 5 minutes de Sierre.')],
        fin_h='Santé dimanche !', fin_p='50 CHF · dim. 8 novembre 2026 · Salgesch'),
     'de': dict(title='Padel+Beer – Padel und ein kühles Bier in Salgesch | Rackets Academy',
        desc='Padel+Beer in Salgesch bei Siders: Padel spielen, danach ein kühles Bier an der Bar mit allen vom Platz. Nächstes Datum Sonntag, 8. November 2026, 50 CHF pro Person.',
        kicker='Sonntag · Salgesch', h1='Padel+Beer — erst spielen, dann Prost.',
        lede='Der entspannte Sonntag in Salgesch: Padel mit Leuten auf deinem Niveau, danach ein kühles Bier an der Bar mit allen vom Platz.',
        chips=['So. 8. November 2026', '50 CHF pro Person', 'Salgesch'], b1='Per WhatsApp anmelden', b2='Alle Events',
        how_h='Das bekommst du',
        how=[('🎾', 'Padel', 'Spiele mit Leuten auf deinem Niveau, Platz inklusive.', 'Salgesch'), ('🍺', 'Bier', 'Ein kühles Bier an der Bar nach dem Spielen.', 'Nach den Spielen'), ('🤝', 'Leute', 'Die Rackets-Community in entspannter Runde.', 'Alle Niveaus')],
        faq_h='Gut zu wissen',
        faq=[('Kann ich allein kommen?', 'Ja. Melde dich allein oder mit Freunden an, wir stellen die Spiele zusammen.'),
             ('Was kostet es?', '50 CHF pro Person.'),
             ('Brauche ich einen eigenen Schläger?', 'Nein, du kannst vor Ort einen mieten.'),
             ('Wo findet es statt?', 'In der Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch, 5 Minuten von Siders.')],
        fin_h='Prost am Sonntag.', fin_p='50 CHF · So. 8. November 2026 · Salgesch'),
    }[L]
    body = hero(img + 'events-friends.jpg', 'center 30%', T['kicker'], T['h1'], T['lede'], T['chips'],
                btn(w, T['b1']), btn('events.html', T['b2'], False))
    body += sec(T['how_h'], facs(T['how']))
    body += faq(T['faq'], T['faq_h'])
    body += final(img + 'events-group.jpg', 'center 45%', T['fin_h'], T['fin_p'], btn(w, T['b1']), btn('events.html', T['b2'], False))
    ld = [{'@type': 'Event', 'name': 'Padel+Beer', 'startDate': BEER_DATE, 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
           'eventStatus': 'https://schema.org/EventScheduled',
           'location': {'@type': 'Place', 'name': 'Rackets Academy Salgesch', 'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressCountry': 'CH'}},
           'offers': {'@type': 'Offer', 'price': '50', 'priceCurrency': 'CHF'},
           'organizer': {'@type': 'Organization', 'name': 'Rackets Academy', 'url': BASE}, 'image': BASE + 'images/photos/events-friends.jpg'}]
    return T, body, ld, img + 'events-friends.jpg'


# ---------------------------------------------------------------- shell
LANG_NAME = {'en': 'English', 'de': 'Deutsch', 'fr': 'Français'}


def write(slug, L, T, body, ld, ogimg):
    d = DIR[L]
    s = open(d + 'spa-and-sauna.html').read()
    a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
    b = s.index('<footer')
    s = s[:a] + body + s[b:]
    url = BASE + d + slug
    alt = ''.join(f'<link rel="alternate" hreflang="{x}" href="{BASE + DIR[x] + slug}">\n' for x in LANGS) + f'<link rel="alternate" hreflang="x-default" href="{BASE + slug}">\n'
    s = re.sub(r'(<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n)+', alt, s, count=1)
    s = re.sub(r'<link rel="canonical" href="[^"]*"', f'<link rel="canonical" href="{url}"', s)
    s = re.sub(r'<meta property="og:url" content="[^"]*"', f'<meta property="og:url" content="{url}"', s)
    s = re.sub(r'<div class="lang-menu">.*?</div>', lambda m: m.group(0).replace('spa-and-sauna.html', slug), s, count=1, flags=re.S)
    s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>' + T['title'] + '</title>', s, count=1, flags=re.S)
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + T['desc'].replace('"', '&quot;') + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + T['title'] + '"', s)
    s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="' + BASE + ogimg.replace('../', '') + '"', s)
    faqs = {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': x}} for q, x in T['faq']]}
    graph = {'@context': 'https://schema.org', '@graph': ld + [faqs]}
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-landing">' + json.dumps(graph, ensure_ascii=False) + '</script>\n</head>', 1)
    s = s.replace('class="active"', '')
    open(d + slug, 'w').write(s)
    print(d + slug, len(T['title']), len(T['desc']))


for L in LANGS:
    for slug, fn in [('padel-valais.html', valais), ('rackemix.html', rackemix), ('padel-beer.html', beer)]:
        T, body, ld, og = fn(L)
        write(slug, L, T, body, ld, og)
