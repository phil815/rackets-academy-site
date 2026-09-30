"""Kids birthday landing page (EN/FR/DE): kids-birthday.html, built from the spa page shell."""
import re, json, urllib.parse
WA_SA = '41772780115'
SLUG = 'kids-birthday.html'
T = {
'en': dict(title="Kids' birthday party with padel, Valais | Rackets Academy",
  desc="Padel birthday party in Salgesch (5 min from Sierre): 1 h with a coach, 1 h mini tournament, then pizza or cake. Up to 12 kids, 20 CHF per child.",
  kicker="Kids' birthday · Salgesch", h1='The birthday party everyone talks about.',
  lede='Two hours of padel with a coach, a mini tournament and pizza or cake to finish — indoors, whatever the weather.',
  chips=['20 CHF per child', '2 hours', 'Up to 12 kids'],
  cta='Book a birthday', cta2='How it works',
  wa="Hola! I'd like to book a kids' birthday party. Date: … · Number of kids: … · Age: …",
  flow_h='How the party works',
  flow=[('1 h', 'Training with a coach', 'Fun games and first shots — no experience needed.'),
        ('1 h', 'Mini tournament', 'Teams, matches and a winner. Everyone plays.'),
        ('🍕', 'Pizza or cake', 'Time to celebrate the birthday kid together.')],
  facts_h='Good to know',
  facts=[('📍', 'Where', 'Rackets Academy Salgesch — 5 min from Sierre.'),
         ('🕒', 'When', 'Weekdays before 17:00. Weekends on request.'),
         ('👧', 'Group size', 'Up to 12 kids. 20 CHF per child from 8 kids.')],
  faq=[('How long is a padel birthday party?', '2 hours: 1 hour of training with a coach, then 1 hour mini tournament, followed by pizza or cake.'),
       ('How much does it cost?', '20 CHF per child from 8 kids, up to 12 kids.'),
       ('When can we book?', 'Weekdays before 17:00. Weekends on request — just ask us on WhatsApp.'),
       ('Where does it take place?', 'At Rackets Academy in Salgesch, 5 minutes from Sierre. Indoor, so the party happens rain or shine.')],
  faq_h='Questions from parents',
  final_h='Pick a date — we handle the fun.', final_p='Salgesch · weekdays before 17:00 · weekends on request'),
'fr': dict(title='Anniversaire enfant avec padel en Valais | Rackets Academy',
  desc="Anniversaire padel à Salgesch (5 min de Sierre) : 1 h avec un coach, 1 h de mini-tournoi, puis pizza ou gâteau. Jusqu'à 12 enfants, 20 CHF par enfant.",
  kicker='Anniversaire enfant · Salgesch', h1="L'anniversaire dont tout le monde parle.",
  lede='Deux heures de padel avec un coach, un mini-tournoi et pizza ou gâteau pour finir — en salle, quelle que soit la météo.',
  chips=['20 CHF par enfant', '2 heures', "Jusqu'à 12 enfants"],
  cta='Réserver un anniversaire', cta2='Le déroulement',
  wa="Hola ! J'aimerais réserver un anniversaire enfant. Date : … · Nombre d'enfants : … · Âge : …",
  flow_h="Comment se passe la fête",
  flow=[('1 h', 'Entraînement avec un coach', 'Jeux fun et premiers coups — aucune expérience nécessaire.'),
        ('1 h', 'Mini-tournoi', 'Équipes, matchs et un gagnant. Tout le monde joue.'),
        ('🍕', 'Pizza ou gâteau', "Place à la fête autour de l'enfant du jour."),],
  facts_h='Bon à savoir',
  facts=[('📍', 'Où', 'Rackets Academy Salgesch — à 5 min de Sierre.'),
         ('🕒', 'Quand', 'En semaine avant 17h. Le week-end sur demande.'),
         ('👧', 'Taille du groupe', "Jusqu'à 12 enfants. 20 CHF par enfant dès 8 enfants.")],
  faq=[("Combien de temps dure un anniversaire padel ?", "2 heures : 1 heure d'entraînement avec un coach, puis 1 heure de mini-tournoi, suivies de pizza ou gâteau."),
       ('Combien ça coûte ?', "20 CHF par enfant dès 8 enfants, jusqu'à 12 enfants."),
       ('Quand peut-on réserver ?', 'En semaine avant 17h. Le week-end sur demande — écris-nous sur WhatsApp.'),
       ('Où cela se passe-t-il ?', 'À la Rackets Academy à Salgesch, à 5 minutes de Sierre. En salle, la fête a lieu par tous les temps.')],
  faq_h='Questions des parents',
  final_h='Choisis une date — on s’occupe du fun.', final_p='Salgesch · en semaine avant 17h · week-end sur demande'),
'de': dict(title='Kindergeburtstag im Wallis mit Padel | Rackets Academy',
  desc='Padel-Kindergeburtstag in Salgesch (5 Min. von Siders): 1 Std. mit Coach, 1 Std. Mini-Turnier, danach Pizza oder Kuchen. Bis 12 Kinder, 20 CHF pro Kind.',
  kicker='Kindergeburtstag · Salgesch', h1='Der Geburtstag, von dem alle reden.',
  lede='Zwei Stunden Padel mit Coach, ein Mini-Turnier und zum Schluss Pizza oder Kuchen — drinnen, bei jedem Wetter.',
  chips=['20 CHF pro Kind', '2 Stunden', 'Bis 12 Kinder'],
  cta='Geburtstag buchen', cta2='So läuft es ab',
  wa='Hola! Ich möchte einen Kindergeburtstag buchen. Datum: … · Anzahl Kinder: … · Alter: …',
  flow_h='So läuft die Party ab',
  flow=[('1 Std.', 'Training mit Coach', 'Lustige Spiele und erste Schläge — keine Erfahrung nötig.'),
        ('1 Std.', 'Mini-Turnier', 'Teams, Matches und ein Sieger. Alle spielen mit.'),
        ('🍕', 'Pizza oder Kuchen', 'Jetzt wird das Geburtstagskind gefeiert.')],
  facts_h='Gut zu wissen',
  facts=[('📍', 'Wo', 'Rackets Academy Salgesch — 5 Min. von Siders.'),
         ('🕒', 'Wann', 'Unter der Woche vor 17 Uhr. Wochenende auf Anfrage.'),
         ('👧', 'Gruppengrösse', 'Bis 12 Kinder. 20 CHF pro Kind ab 8 Kindern.')],
  faq=[('Wie lange dauert ein Padel-Kindergeburtstag?', '2 Stunden: 1 Stunde Training mit Coach, dann 1 Stunde Mini-Turnier, danach Pizza oder Kuchen.'),
       ('Was kostet es?', '20 CHF pro Kind ab 8 Kindern, bis maximal 12 Kinder.'),
       ('Wann kann man buchen?', 'Unter der Woche vor 17 Uhr. Wochenende auf Anfrage — schreib uns einfach auf WhatsApp.'),
       ('Wo findet er statt?', 'In der Rackets Academy in Salgesch, 5 Minuten von Siders. Drinnen — die Party findet bei jedem Wetter statt.')],
  faq_h='Fragen von Eltern',
  final_h='Wähl ein Datum — für den Spass sorgen wir.', final_p='Salgesch · unter der Woche vor 17 Uhr · Wochenende auf Anfrage'),
}

def body(t, pre):
    img = lambda p: pre + p
    wa = 'https://wa.me/' + WA_SA + '?text=' + urllib.parse.quote(t['wa'])
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in t['chips'])
    flow = ''.join(f'<div class="kb-step"><span class="kb-badge">{a}</span><h3>{h}</h3><p>{p}</p></div>' for a, h, p in t['flow'])
    facts = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in t['facts'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    return f'''
<section class="spa-hero co-hero kb-hero" style="background-image:url('{img("images/coaching/coaching-2.jpg")}');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="spa-chips">{chips}</div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="{wa}" target="_blank" rel="noopener">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="#flow">{t['cta2']}</a>
    </div>
  </div>
</section>

<section class="co2-sec kb-flow-sec" id="flow">
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

<section class="spa-final kb-final" style="background-image:url('{img("images/coaching/coaching-6.jpg")}');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-final-inner">
    <h2>{t['final_h']}</h2>
    <p>{t['final_p']}</p>
    <a class="btn btn-green spa-cta" href="{wa}" target="_blank" rel="noopener">{t['cta']}</a>
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
    s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="https://www.racketsacademy.ch/images/coaching/coaching-2.jpg"', s)
    ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-kb">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
    s = s.replace('class="active"', '')
    open(d + SLUG, 'w').write(s)
    print(d + SLUG, len(t['title']), len(t['desc']))
