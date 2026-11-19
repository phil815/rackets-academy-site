#!/usr/bin/env python3
"""Firmen-Seite (company.html, 3 Sprachen) als Einstieg mit drei Wegen: Firmenevent, Sponsor werden, Firmenvorteile.
Der Partnerrabatt mit Formular bleibt darunter. Idempotent; nach jedem Neubau der Seite laufen lassen."""
import pathlib, re
ROOT = pathlib.Path(__file__).resolve().parent.parent
T = {
    '': dict(lede='Company events for your team, sponsoring for your brand and benefits for your employees. In Salgesch and Sion.', h='Three ways to work with us', ev='Company event', evp='Team building on the court: tournament with coaches, meeting room, food and apéro. 2 to 6 hours, in Salgesch or Sion.', evb='See event packages',
             sp='Become a sponsor', spp='Put your brand on the courts and in front of our community. A partnership that pays off for both sides and moves the sport forward.', spb='How sponsoring works',
             alt1='Company event at Rackets Academy', alt2='Winners on court at Rackets Academy', alt3='Players on court at Rackets Academy',
             be='Company benefits', bep='15% off court bookings before 17:30 for your employees, on every weekday. Free for the company, active from sign-up.', beb='Activate the discount'),
    'de/': dict(lede='Firmenevents für dein Team, Sponsoring für deine Marke und Vorteile für deine Mitarbeitenden. In Salgesch und Sion.', h='Drei Wege, mit uns zu arbeiten', ev='Firmenevent', evp='Teambuilding auf dem Platz: Turnier mit Coaches, Sitzungsraum, Essen und Apéro. 2 bis 6 Stunden, in Salgesch oder Sion.', evb='Event-Pakete ansehen',
                sp='Sponsor werden', spp='Deine Marke auf den Plätzen und vor unserer Community. Eine Partnerschaft, die sich für beide Seiten lohnt und den Sport voranbringt.', spb='So funktioniert Sponsoring',
                alt1='Firmenevent in der Rackets Academy', alt2='Turniersieger auf dem Platz der Rackets Academy', alt3='Spieler auf dem Platz der Rackets Academy',
                be='Firmenvorteile', bep='15% Rabatt auf Platzbuchungen vor 17:30 Uhr für deine Mitarbeitenden, an jedem Werktag. Für die Firma kostenlos, gültig ab der Anmeldung.', beb='Rabatt aktivieren'),
    'fr/': dict(lede='Des événements pour ton équipe, du sponsoring pour ta marque et des avantages pour tes employés. À Salgesch et Sion.', h='Trois façons de travailler avec nous', ev='Événement d’entreprise', evp='Team building sur le court : tournoi avec coachs, salle de réunion, repas et apéro. De 2 à 6 heures, à Salgesch ou Sion.', evb='Voir les formules',
                sp='Devenir sponsor', spp='Ta marque sur les courts et devant notre communauté. Un partenariat gagnant pour les deux côtés, qui fait avancer le sport.', spb='Comment ça marche',
                alt1='Événement d’entreprise à la Rackets Academy', alt2='Vainqueurs sur le court de la Rackets Academy', alt3='Joueurs sur le court de la Rackets Academy',
                be='Avantages entreprise', bep='15% de rabais sur les réservations avant 17h30 pour tes employés, chaque jour ouvrable. Gratuit pour l’entreprise, valable dès l’inscription.', beb='Activer le rabais'),
}
for lang, t in T.items():
    p = ROOT / lang / 'company.html'
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'\s*<section id="co-ways"[\s\S]*?</section>', '', s)                                   # idempotent
    s = re.sub(r'\s*<section id="events" class="section-tight">[\s\S]*?</section>', '', s)            # old one-line event teaser
    s = re.sub(r'\s*<section class="section-tight" style="padding-top:0;"><div class="wrap"><p class="offer-more sp-cross"[\s\S]*?</section>', '', s)
    card = lambda href, img, alt, h, txt, btn: f'''
      <a class="card card-link offer co-way" href="{href}">
        <img src="{img}" alt="{alt}" loading="lazy">
        <div class="offer-text"><h3>{h}</h3><p>{txt}</p><span class="co-go">{btn} →</span></div>
      </a>'''
    block = f'''
<section id="co-ways">
  <div class="wrap">
    <h2>{t['h']}</h2>
    <div class="grid-3 co-ways">{card('company-events.html', 'https://www.racketsacademy.ch/images/photos/cards/company-events.jpg', t['alt1'], t['ev'], t['evp'], t['evb'])}{card('sponsoring.html', 'https://www.racketsacademy.ch/images/photos/events-winners.webp', t['alt2'], t['sp'], t['spp'], t['spb'])}{card('#discount', 'https://www.racketsacademy.ch/images/photos/events-group.webp', t['alt3'], t['be'], t['bep'], t['beb'])}
    </div>
  </div>
</section>
'''
    s = re.sub(r'(<h1>[^<]*</h1>\s*<p class="lede">)[^<]*(</p>)', lambda m: m.group(1) + t['lede'] + m.group(2), s, count=1)
    i = s.index('<section id="discount">')
    s = s[:i] + block.lstrip('\n') + '\n' + s[i:]
    p.write_text(s, encoding='utf-8')
    print('ok', p.relative_to(ROOT))
