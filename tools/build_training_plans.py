"""Rebuilds the plans part of training.html (from #plans up to the 'questions' section) – EN/FR/DE."""
import urllib.parse, re
PT_SA, PT_SI = 'https://tinyurl.com/Academy-Salgesch', 'https://tinyurl.com/Academy-Sion'
WA = {'sa': '41772780115', 'si': '41762914369'}
ADULT = [('60', 40, (130, 33), (375, 29), (1000, 26)), ('90', 50, (160, 40), (475, 37), (1250, 32))]
KIDS = [('60', 30, (95, 24), (280, 22), (750, 19)), ('90', 40, (130, 33), (375, 29), (1000, 26))]
PRIV = [('60', 1, 90, 100), ('60', 2, 60, 70), ('90', 3, 65, 75), ('90', 4, 55, 65)]
L = {
 'en': dict(ids=('adults', 'kids', 'private'), plans_h='Choose your plan', jump=('Adults', 'Kids', 'Private lessons'),
   season='Season 2026/27 · 24.08.2026 – 21.06.2027 · 39 weeks',
   cols=('Drop-in', 'Month', 'Quarter', 'Year'), sess=('1 session', '4 sessions', '13 sessions', '39 sessions'), per='/session', best='Best price', total='total',
   ad_h='Adults', ad_p='Groups of 2–4 players by level (min. 2 before 17:00, min. 3 after 17:00).',
   ki_h='Kids', ki_p='Groups of 3–4 kids by level and age. 2nd child −20 % on the subscription.',
   ki_sched='Mon · Wed · Fri (60 min): 13:30 · 14:30 · 15:30 · 16:30<br>Tue · Thu (90 min): 13:00 · 14:30 · 16:00',
   sub='Subscription incl. training plan &amp; feedback', drop='Drop-in on Playtomic',
   wa_ad="Hola! I'm interested in an adult padel course (subscription). Could you tell me more?",
   wa_ki="Hola! I'm interested in a kids padel course (subscription). Could you tell me more?",
   wa_pr="Hola! I'd like to book a private padel lesson.",
   pr_h='Private lessons', pr_p='Your own plan, your own pace. Price per person — coach, court, racket and balls included.',
   pr_cols=('Duration', 'Players', 'Before 17:00', 'After 17:00'), pr_book='Book a private lesson',
   loc=('Salgesch · Mario', 'Sion · Phil'), book=('Salgesch', 'Sion'),
   good_h='Good to know',
   good=['No classes during school holidays: 19–25.10.26 · 28.12.26–10.01.27 · 08–14.02.27 · 29.03–04.04.27',
         'Missed sessions: a make-up in another group is offered where possible, but not guaranteed. Refund with a medical certificate.',
         'Payment: drop-in via Playtomic, subscriptions in advance at the club.']),
 'fr': dict(ids=('adultes', 'enfants', 'prive'), plans_h='Choisis ton abonnement', jump=('Adultes', 'Enfants', 'Cours privés'),
   season='Saison 2026/27 · 24.08.2026 – 21.06.2027 · 39 semaines',
   cols=('Drop-in', 'Mois', 'Trimestre', 'Année'), sess=('1 séance', '4 séances', '13 séances', '39 séances'), per='/séance', best='Meilleur prix', total='total',
   ad_h='Adultes', ad_p='Groupes de 2 à 4 joueurs par niveau (min. 2 avant 17h, min. 3 après 17h).',
   ki_h='Enfants', ki_p='Groupes de 3 à 4 enfants par niveau et par âge. 2e enfant −20 % sur l’abonnement.',
   ki_sched='Lun · Mer · Ven (60 min) : 13h30 · 14h30 · 15h30 · 16h30<br>Mar · Jeu (90 min) : 13h00 · 14h30 · 16h00',
   sub='Abonnement avec plan &amp; retour après chaque séance', drop='Drop-in sur Playtomic',
   wa_ad="Hola ! Je suis intéressé(e) par un cours de padel adulte (abonnement). Tu peux m'en dire plus ?",
   wa_ki="Hola ! Je suis intéressé(e) par un cours de padel enfant (abonnement). Tu peux m'en dire plus ?",
   wa_pr="Hola ! J'aimerais réserver un cours privé de padel.",
   pr_h='Cours privés', pr_p='Ton plan, ton rythme. Prix par personne — coach, court, raquette et balles inclus.',
   pr_cols=('Durée', 'Joueurs', 'Avant 17h', 'Après 17h'), pr_book='Réserver un cours privé',
   loc=('Salgesch · Mario', 'Sion · Phil'), book=('Salgesch', 'Sion'),
   good_h='Bon à savoir',
   good=['Pas de cours pendant les vacances scolaires : 19–25.10.26 · 28.12.26–10.01.27 · 08–14.02.27 · 29.03–04.04.27',
         'Séances manquées : un rattrapage dans un autre groupe est proposé si possible, sans garantie. Remboursement sur certificat médical.',
         'Paiement : drop-in via Playtomic, abonnements à l’avance au club.']),
 'de': dict(ids=('erwachsene', 'kids', 'privat'), plans_h='Wähle dein Abo', jump=('Erwachsene', 'Kinder', 'Privatlektionen'),
   season='Saison 2026/27 · 24.08.2026 – 21.06.2027 · 39 Wochen',
   cols=('Drop-in', 'Monat', 'Quartal', 'Jahr'), sess=('1 Lektion', '4 Lektionen', '13 Lektionen', '39 Lektionen'), per='/Lektion', best='Bester Preis', total='total',
   ad_h='Erwachsene', ad_p='Gruppen von 2–4 Spielern nach Niveau (min. 2 vor 17 Uhr, min. 3 nach 17 Uhr).',
   ki_h='Kinder', ki_p='Gruppen von 3–4 Kindern nach Niveau und Alter. 2. Kind −20 % aufs Abo.',
   ki_sched='Mo · Mi · Fr (60 Min.): 13:30 · 14:30 · 15:30 · 16:30<br>Di · Do (90 Min.): 13:00 · 14:30 · 16:00',
   sub='Abo inkl. Trainingsplan &amp; Feedback', drop='Drop-in auf Playtomic',
   wa_ad='Hola! Ich interessiere mich für einen Padelkurs für Erwachsene (Abo). Kannst du mir mehr erzählen?',
   wa_ki='Hola! Ich interessiere mich für einen Kinder-Padelkurs (Abo). Kannst du mir mehr erzählen?',
   wa_pr='Hola! Ich möchte eine Padel-Privatlektion buchen.',
   pr_h='Privatlektionen', pr_p='Dein Plan, dein Tempo. Preis pro Person — Coach, Platz, Racket und Bälle inklusive.',
   pr_cols=('Dauer', 'Spieler', 'Vor 17 Uhr', 'Nach 17 Uhr'), pr_book='Privatlektion buchen',
   loc=('Salgesch · Mario', 'Sion · Phil'), book=('Salgesch', 'Sion'),
   good_h='Gut zu wissen',
   good=['Kein Training in den Schulferien: 19.–25.10.26 · 28.12.26–10.01.27 · 08.–14.02.27 · 29.03.–04.04.27',
         'Verpasste Lektionen: Wo möglich bieten wir eine Ersatzlektion in einer anderen Gruppe an, ohne Garantie. Rückerstattung mit Arztzeugnis.',
         'Zahlung: Drop-in über Playtomic, Abos im Voraus im Club.']),
}
wa = lambda n, txt: 'https://wa.me/' + n + '?text=' + urllib.parse.quote(txt)
chf = lambda v: ("{:,}".format(v)).replace(',', "'") + '.–'

def table(t, rows):
    head = ''.join(f'<th{" class=\"best\"" if i == 3 else ""}>{c}<small>{s}</small>{"<em>" + t["best"] + "</em>" if i == 3 else ""}</th>' for i, (c, s) in enumerate(zip(t['cols'], t['sess'])))
    body = ''
    for dur, drop, m, q, y in rows:
        cells = f'<td><b>{chf(drop)}</b></td>' + ''.join(f'<td{" class=\"best\"" if i == 2 else ""}><b>{chf(p)}</b><span class="co3-u">{t["per"]}</span><small>{chf(tot)} {t["total"]}</small></td>' for i, (tot, p) in enumerate([m, q, y]))
        body += f'<tr><th>{dur} min</th>{cells}</tr>'
    return f'<div class="co3-tw"><table class="co3-t"><thead><tr><th></th>{head}</tr></thead><tbody>{body}</tbody></table></div>'

def block(t, sid, img, h, p, rows, wa_txt, extra=''):
    return f'''
<section class="co3-sec" id="{sid}">
  <div class="wrap co3-card">
    <img class="co3-img" src="{img}" alt="" loading="lazy">
    <div class="co3-body">
      <h2>{h}</h2>
      <p class="co3-lead">{p}</p>
      {extra}
      {table(t, rows)}
      <p class="co3-lbl">{t['sub']}</p>
      <div class="co3-btns">
        <a class="btn btn-green" href="{wa(WA['sa'], wa_txt)}" target="_blank" rel="noopener">{t['loc'][0]}</a>
        <a class="btn btn-green" href="{wa(WA['si'], wa_txt)}" target="_blank" rel="noopener">{t['loc'][1]}</a>
      </div>
      <p class="co3-lbl co3-lbl2">{t['drop']}</p>
      <div class="co3-btns">
        <a class="btn co3-ghost" href="{PT_SA}" target="_blank" rel="noopener">{t['book'][0]}</a>
        <a class="btn co3-ghost" href="{PT_SI}" target="_blank" rel="noopener">{t['book'][1]}</a>
      </div>
    </div>
  </div>
</section>'''

def build(lang, pre):
    t = L[lang]
    img = lambda n: pre + 'images/coaching/' + n + '.jpg'
    jump = ''.join(f'<a href="#{i}">{l}</a>' for i, l in zip(t['ids'], t['jump']))
    prow = ''.join(f'<tr><th>{d} min</th><td>{n}</td><td><b>{a} CHF</b></td><td><b>{b} CHF</b></td></tr>' for d, n, a, b in PRIV)
    good = ''.join(f'<li>{g}</li>' for g in t['good'])
    html = f'''<section class="co3-head" id="plans">
  <div class="wrap">
    <h2 class="co2-h">{t['plans_h']}</h2>
    <nav class="jump-nav co3-jump">{jump}</nav>
    <p class="co-season">{t['season']}</p>
  </div>
</section>
{block(t, t['ids'][0], img('coaching-2'), t['ad_h'], t['ad_p'], ADULT, t['wa_ad'])}
{block(t, t['ids'][1], img('coaching-4'), t['ki_h'], t['ki_p'], KIDS, t['wa_ki'], '<p class="co3-sched">' + t['ki_sched'] + '</p>')}
<section class="co3-sec" id="{t['ids'][2]}">
  <div class="wrap co3-card">
    <img class="co3-img" src="{img('coaching-5')}" alt="" loading="lazy">
    <div class="co3-body">
      <h2>{t['pr_h']}</h2>
      <p class="co3-lead">{t['pr_p']}</p>
      <div class="co3-tw"><table class="co3-t co3-tp"><thead><tr>{''.join('<th>' + c + '</th>' for c in t['pr_cols'])}</tr></thead><tbody>{prow}</tbody></table></div>
      <p class="co3-lbl">{t['pr_book']}</p>
      <div class="co3-btns">
        <a class="btn btn-green" href="{wa(WA['sa'], t['wa_pr'])}" target="_blank" rel="noopener">{t['loc'][0]}</a>
        <a class="btn btn-green" href="{wa(WA['si'], t['wa_pr'])}" target="_blank" rel="noopener">{t['loc'][1]}</a>
      </div>
    </div>
  </div>
</section>

<section class="co3-sec co3-good">
  <div class="wrap">
    <h3>{t['good_h']}</h3>
    <ul>{good}</ul>
  </div>
</section>

'''
    return html

for lang in ['en', 'fr', 'de']:
    pre = '' if lang == 'en' else '../'
    f = ('' if lang == 'en' else lang + '/') + 'training.html'
    s = open(f).read()
    a = s.index('<section class="section-tight" id="plans">') if '<section class="section-tight" id="plans">' in s else s.index('<section class="co3-head" id="plans">')
    b = s.index('<section class="section-tight" style="text-align:center;">', a)
    s = s[:a] + build(lang, pre) + s[b:]
    open(f, 'w').write(s)
    print(f, 'ok')
