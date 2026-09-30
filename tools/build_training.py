"""Conversion-focused top of training.html (EN/FR/DE). Replaces hero + jump nav; keeps price tables below."""
import re, os, urllib.parse
WA_SA, WA_SI = '41772780115', '41762914369'
T = {
'en': dict(
  title='Padel courses Salgesch & Sion | Rackets Academy',
  desc='Padel courses for adults and kids in Salgesch and Sion. Subscriptions include a 12-week training plan and coach feedback after every session.',
  kicker='Coaching · Salgesch & Sion', h1='Train with a plan. See your progress.',
  lede='Group courses for adults and kids — with a subscription you get a 12-week training plan and a personal rating from your coach after every session.',
  chips=['Certified coaches', '12-week training plan', 'Feedback after every session'],
  cta='Choose your plan', cta2='Ask our coach',
  wa='Hola! I am interested in a padel course subscription. Could you tell me more?',
  ben_h='What your subscription includes',
  ben=[('📋', 'Your training plan', 'Every 12-week cycle has a clear goal for each week — from base position to bandeja. You always know what you work on and why.'),
       ('📩', 'Feedback after every session', 'Your coach rates your shots on the Playtomic scale (0–7) and emails you a short summary. Your progress, in black and white.'),
       ('🎓', 'Certified coaches', 'Our coaches are trained by M3 Coaching (Assistant Level 1) or the Spanish Padel Federation.'),
       ('💸', 'Up to 35 % cheaper', 'Per session compared to drop-in — and a fixed spot in your group every week.')],
  ex_h='This is what it looks like', ex_tag='Example',
  mail=dict(sub='Your session · Thu 19:00 · Sion', focus="Today's focus: the lob — height, depth, timing",
            rows=[('Lob', '2.5', '3.0'), ('Back glass exit', '2.5', '2.75'), ('Bandeja', '2.0', '2.0')],
            note='“Great height today. Next week: taking the net after the lob.”', sig='— Your coach'),
  plan_h='Your 12-week plan (extract)',
  plan=[('1', 'Own the middle'), ('3', 'The transition to the net'), ('5', 'Back glass exit under pressure'),
        ('7', 'The lob: height, depth, timing'), ('9', 'Bandeja and víbora'), ('12', 'Match play and cycle review')],
  steps_h='Start in 3 steps',
  steps=[('Message us', 'Tell your coach on WhatsApp your level and when you can play.'),
         ('Get your group', 'We place you in a group that matches your level and schedule.'),
         ('Train with a plan', 'Week 1 starts with your plan — feedback lands in your inbox after every session.')],
  plans_h='Choose your plan', plans_p='Month, quarter or year — all subscriptions include the training plan and the feedback emails. Drop-in sessions are booked on Playtomic without them.',
  jump=[('#adults', 'Adults'), ('#kids', 'Kids'), ('#private', 'Private lessons')], ids=('kids','adults'),
  season='Season 2026/27: 24.08.2026 – 21.06.2027 · 39 weeks of training',
  sub_old='Month / Quarter / Year subscriptions — sign up with our coach:',
  sub_new='Month / Quarter / Year — incl. training plan &amp; feedback after every session. Sign up with our coach:'),
'fr': dict(
  title='Cours de padel Salgesch & Sion | Rackets Academy',
  desc="Cours de padel adultes et enfants à Salgesch et Sion. L'abonnement inclut un plan de 12 semaines et un retour du coach après chaque séance.",
  kicker='Coaching · Salgesch & Sion', h1='Entraîne-toi avec un plan. Vois tes progrès.',
  lede="Cours en groupe pour adultes et enfants — avec un abonnement, tu reçois un plan d'entraînement de 12 semaines et une évaluation personnelle de ton coach après chaque séance.",
  chips=['Coachs certifiés', 'Plan de 12 semaines', 'Retour après chaque séance'],
  cta='Choisir mon abonnement', cta2='Écrire au coach',
  wa="Hola ! Je suis intéressé(e) par un abonnement de cours de padel. Tu peux m'en dire plus ?",
  ben_h='Ce que ton abonnement inclut',
  ben=[('📋', "Ton plan d'entraînement", "Chaque cycle de 12 semaines a un objectif clair pour chaque semaine — de la position de base à la bandeja. Tu sais toujours sur quoi tu travailles et pourquoi."),
       ('📩', 'Un retour après chaque séance', "Ton coach évalue tes coups sur l'échelle Playtomic (0–7) et t'envoie un résumé par e-mail. Tes progrès, noir sur blanc."),
       ('🎓', 'Coachs certifiés', 'Nos coachs sont formés par M3 Coaching (Assistant Level 1) ou par la Fédération espagnole de padel.'),
       ('💸', "Jusqu'à 35 % moins cher", 'Par séance par rapport au drop-in — et une place fixe dans ton groupe chaque semaine.')],
  ex_h='Voilà à quoi ça ressemble', ex_tag='Exemple',
  mail=dict(sub='Ta séance · jeu 19:00 · Sion', focus='Objectif du jour : le lob — hauteur, profondeur, timing',
            rows=[('Lob', '2.5', '3.0'), ('Sortie de vitre de fond', '2.5', '2.75'), ('Bandeja', '2.0', '2.0')],
            note='« Super hauteur aujourd’hui. La semaine prochaine : monter au filet après le lob. »', sig='— Ton coach'),
  plan_h='Ton plan de 12 semaines (extrait)',
  plan=[('1', 'Maîtriser le milieu'), ('3', 'La transition vers le filet'), ('5', 'Sortie de vitre de fond sous pression'),
        ('7', 'Le lob : hauteur, profondeur, timing'), ('9', 'Bandeja et víbora'), ('12', 'Matchs et bilan du cycle')],
  steps_h='Commence en 3 étapes',
  steps=[('Écris-nous', 'Dis à ton coach sur WhatsApp ton niveau et quand tu peux jouer.'),
         ('Trouve ton groupe', 'On te place dans un groupe adapté à ton niveau et à ton horaire.'),
         ('Entraîne-toi avec un plan', 'La semaine 1 commence avec ton plan — le retour arrive dans ta boîte mail après chaque séance.')],
  plans_h='Choisis ton abonnement', plans_p='Mois, trimestre ou année — tous les abonnements incluent le plan et les e-mails de retour. Les séances drop-in se réservent sur Playtomic, sans ces avantages.',
  jump=[('#adultes', 'Adultes'), ('#enfants', 'Enfants'), ('#prive', 'Cours privés')], ids=('enfants','adultes'),
  season='Saison 2026/27 : 24.08.2026 – 21.06.2027 · 39 semaines de cours',
  sub_old='Abonnements mois / trimestre / année — inscris-toi avec notre coach :',
  sub_new="Mois / trimestre / année — plan d'entraînement &amp; retour après chaque séance inclus. Inscris-toi avec notre coach :"),
'de': dict(
  title='Padelkurse Salgesch & Sion | Rackets Academy',
  desc='Padelkurse für Erwachsene und Kinder in Salgesch und Sion. Mit Abo: 12-Wochen-Trainingsplan und Feedback vom Coach nach jedem Training.',
  kicker='Coaching · Salgesch & Sion', h1='Trainiere mit Plan. Sieh deinen Fortschritt.',
  lede='Gruppenkurse für Erwachsene und Kinder — mit einem Abo bekommst du einen 12-Wochen-Trainingsplan und nach jedem Training ein persönliches Rating von deinem Coach.',
  chips=['Zertifizierte Coaches', '12-Wochen-Trainingsplan', 'Feedback nach jedem Training'],
  cta='Abo wählen', cta2='Coach fragen',
  wa='Hola! Ich interessiere mich für ein Padelkurs-Abo. Kannst du mir mehr erzählen?',
  ben_h='Das ist in deinem Abo drin',
  ben=[('📋', 'Dein Trainingsplan', 'Jeder 12-Wochen-Zyklus hat pro Woche ein klares Ziel — von der Grundposition bis zur Bandeja. Du weisst immer, woran du arbeitest und warum.'),
       ('📩', 'Feedback nach jedem Training', 'Dein Coach bewertet deine Schläge auf der Playtomic-Skala (0–7) und schickt dir eine kurze Zusammenfassung per E-Mail. Dein Fortschritt, schwarz auf weiss.'),
       ('🎓', 'Zertifizierte Coaches', 'Unsere Coaches sind von M3 Coaching (Assistant Level 1) oder vom Spanischen Padelverband ausgebildet.'),
       ('💸', 'Bis zu 35 % günstiger', 'Pro Lektion im Vergleich zum Drop-in — und jede Woche ein fixer Platz in deiner Gruppe.')],
  ex_h='So sieht das aus', ex_tag='Beispiel',
  mail=dict(sub='Dein Training · Do 19:00 · Sion', focus='Fokus heute: der Lob — Höhe, Länge, Timing',
            rows=[('Lob', '2.5', '3.0'), ('Rückwand-Ausgang', '2.5', '2.75'), ('Bandeja', '2.0', '2.0')],
            note='«Super Höhe heute. Nächste Woche: nach dem Lob ans Netz.»', sig='— Dein Coach'),
  plan_h='Dein 12-Wochen-Plan (Auszug)',
  plan=[('1', 'Die Mitte beherrschen'), ('3', 'Der Weg ans Netz'), ('5', 'Rückwand-Ausgang unter Druck'),
        ('7', 'Der Lob: Höhe, Länge, Timing'), ('9', 'Bandeja und Víbora'), ('12', 'Matchplay und Zyklus-Rückblick')],
  steps_h='In 3 Schritten starten',
  steps=[('Schreib uns', 'Sag deinem Coach auf WhatsApp dein Niveau und wann du spielen kannst.'),
         ('Deine Gruppe', 'Wir teilen dich in eine Gruppe ein, die zu deinem Niveau und Zeitplan passt.'),
         ('Mit Plan trainieren', 'Woche 1 startet mit deinem Plan — das Feedback kommt nach jedem Training per E-Mail.')],
  plans_h='Wähle dein Abo', plans_p='Monat, Quartal oder Jahr — alle Abos enthalten den Trainingsplan und die Feedback-E-Mails. Drop-in-Lektionen buchst du auf Playtomic, ohne diese Extras.',
  jump=[('#erwachsene', 'Erwachsene'), ('#kids', 'Kinder'), ('#privat', 'Privatlektionen')], ids=('kids','erwachsene'),
  season='Saison 2026/27: 24.08.2026 – 21.06.2027 · 39 Trainingswochen',
  sub_old='Monats- / Quartals- / Jahresabo — meld dich bei unserem Coach:',
  sub_new='Monat / Quartal / Jahr — inkl. Trainingsplan &amp; Feedback nach jedem Training. Meld dich bei unserem Coach:'),
}

S = {
 'en': dict(lede='Group courses for adults and kids in Salgesch and Sion.',
   b=[('📋','A plan for every week','12-week cycle with one clear goal per session.'),
      ('📩','Your rating after every session','Your coach scores your shots (0–7) and emails you a summary.'),
      ('🎓','Certified coaches','Trained by M3 Coaching or the Spanish Padel Federation.')],
   proof_h='Your progress, in black and white', proof_cap='Example of a feedback email',
   price='From <b>19.–</b> per session with a subscription — up to 35 % less than drop-in.'),
 'fr': dict(lede='Cours en groupe pour adultes et enfants à Salgesch et Sion.',
   b=[('📋','Un plan pour chaque semaine','Cycle de 12 semaines, un objectif clair par séance.'),
      ('📩','Ton évaluation après chaque séance','Ton coach note tes coups (0–7) et t’envoie un résumé par e-mail.'),
      ('🎓','Coachs certifiés','Formés par M3 Coaching ou la Fédération espagnole de padel.')],
   proof_h='Tes progrès, noir sur blanc', proof_cap='Exemple d’e-mail de retour',
   price='Dès <b>19.–</b> la séance avec un abonnement — jusqu’à 35 % de moins qu’en drop-in.'),
 'de': dict(lede='Gruppenkurse für Erwachsene und Kinder in Salgesch und Sion.',
   b=[('📋','Ein Plan für jede Woche','12-Wochen-Zyklus mit einem klaren Ziel pro Training.'),
      ('📩','Dein Rating nach jedem Training','Dein Coach bewertet deine Schläge (0–7) und schickt dir die Zusammenfassung per E-Mail.'),
      ('🎓','Zertifizierte Coaches','Ausgebildet von M3 Coaching oder vom Spanischen Padelverband.')],
   proof_h='Dein Fortschritt, schwarz auf weiss', proof_cap='Beispiel einer Feedback-E-Mail',
   price='Ab <b>19.–</b> pro Lektion mit Abo — bis zu 35 % günstiger als Drop-in.'),
}

def top(t, pre, lang):
    x = S[lang]
    img = lambda n: pre + 'images/coaching/' + n + '.jpg'
    wa = lambda n: 'https://wa.me/' + n + '?text=' + urllib.parse.quote(t['wa'])
    ben = ''.join(f'<div class="co2-b"><span class="co2-ic">{e}</span><h3>{h}</h3><p>{p}</p></div>' for e, h, p in x['b'])
    m = t['mail']
    rows = ''.join(f'<div class="co-row"><span>{s}</span><span class="co-lvl">{(a + " → <b>" + b + " ↑</b>") if b != a else a}</span></div>' for s, a, b in m['rows'])
    jump = ''.join(f'<a href="{h}">{l}</a>' for h, l in t['jump'])
    return f'''
<section class="spa-hero co-hero" style="background-image:url('{img("coaching-hero")}'); background-position:center 60%;">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{x['lede']}</p>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="#plans">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="{wa(WA_SI)}" target="_blank" rel="noopener">{t['cta2']}</a>
    </div>
  </div>
</section>

<section class="co2-sec">
  <div class="wrap">
    <h2 class="co2-h">{t['ben_h']}</h2>
    <div class="co2-bens">{ben}</div>
  </div>
</section>

<section class="co2-sec co2-proof">
  <div class="wrap co2-split">
    <img class="co2-photo" src="{img('coaching-3')}" alt="" loading="lazy">
    <div>
      <h2 class="co2-h">{x['proof_h']}</h2>
      <div class="co-mail">
        <p class="co-mail-sub">📩 {m['sub']}</p>
        <p class="co-mail-focus">{m['focus']}</p>
        {rows}
        <p class="co-mail-note">{m['note']}<br><span>{m['sig']}</span></p>
      </div>
      <p class="co2-cap">{x['proof_cap']}</p>
    </div>
  </div>
</section>

<section class="co2-sec">
  <div class="wrap co2-price">
    <p>{x['price']}</p>
    <a class="btn btn-green spa-cta" href="#plans">{t['cta']}</a>
  </div>
</section>

<section class="section-tight" id="plans">
  <div class="wrap">
    <h2>{t['plans_h']}</h2>
    <p class="section-lede">{t['plans_p']}</p>
    <nav class="jump-nav">{jump}</nav>
    <p class="co-season">{t['season']}</p>
  </div>
</section>
'''

for lang, t in T.items():
    pre = '' if lang == 'en' else '../'
    f = pre.replace('../', lang + '/') + 'training.html' if lang != 'en' else 'training.html'
    s = open(f).read()
    a = s.index('<section class="hero"') if '<section class="hero"' in s else s.index('<section class="spa-hero co-hero"')
    # end: the section containing the holiday note-box (keep it) -> cut until that section
    b = s.index('<section class="section-tight">\n  <div class="wrap">\n    <div class="note-box">', a)
    s = s[:a] + top(t, pre, lang).lstrip('\n') + '\n' + s[b:]
    s = s.replace(t['sub_old'], t['sub_new'])
    # adults before kids
    ki = s.index('<section id="' + t['ids'][0] + '"'); ad = s.index('<section id="' + t['ids'][1] + '"')
    if ki < ad:
        kend = ad; aend = s.index('<section', ad + 10)
        kids = s[ki:kend]; adults = s[ad:aend]
        s = s[:ki] + adults + kids + s[aend:]
    s = re.sub(r'<title>.*?</title>', '<title>' + t['title'] + '</title>', s, count=1, flags=re.S)
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + t['desc'].replace('"', '&quot;') + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + t['title'] + '"', s)
    open(f, 'w').write(s)
    print(f, len(t['title']), len(t['desc']))
