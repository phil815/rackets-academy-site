"""UX v1 (Oct 2026): prices, FAQ, trust strip, gift banner, location info on index/book (EN/FR/DE).
Idempotent: blocks are wrapped in <!-- ux:NAME --> ... <!-- /ux:NAME --> markers and replaced on rerun."""
import re, json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SA = 'https://playtomic.com/tenant/f89dfa07-4283-453e-8be3-316f9bd060d3'
T = {
 'en': dict(
  trust='<span class="ts-stars">★★★★★</span> <b>4.9</b> · 77 Google reviews · 2 clubs in Valais · daily 7am–11:30pm',
  bb_h='Intro course every Saturday at 10:00 in Sion', bb_k='New to padel?',
  pr_h='Court prices', pr_lede='Pay per player, split automatically in Playtomic.',
  pad='Padel indoor', pad_d='90 min', p1='17 CHF', p1d='per person · Mon–Fri before 5pm', p2='20 CHF', p2d='per person · from 5pm & weekends',
  ten='Tennis', ten_p='from 15 CHF', ten_d='per person', pic='Pickleball', pic_p='Live prices', pic_d='on Playtomic',
  pr_notes=['Racket rental 3, 5 or 10 CHF', 'Balls for sale on site', 'Free cancellation up to 24 h before', 'Changing rooms & showers at both clubs'],
  pr_cta='See free slots', pr_cta2='Course prices',
  gift_k='Gift idea', gift_h='Give padel.', gift_p='Gift vouchers from 20 CHF, sent by e-mail and valid at both clubs.', gift_cta='Buy a gift voucher', shop='shop.html#vouchers',
  faq_h='First time? Good to know', faq_all='All questions →',
  q=[('How much does a court cost?','Padel indoor (90 min): 17 CHF per person Mon–Fri before 5pm, 20 CHF per person from 5pm and at weekends. Tennis from 15 CHF per person. Pickleball prices are live on Playtomic.'),
     ("I don't have a racket.",'Rent one at the club for 3, 5 or 10 CHF (beginner / intermediate / pro), pay with Twint. Balls are on sale on site.'),
     ("I've never played.",'Join the intro course every Saturday at 10:00 in Sion. No experience needed, rackets to rent on site. <a href="https://tinyurl.com/Academy-Sion" target="_blank" rel="noopener">Sign up on Playtomic</a>.'),
     ('How do I cancel?','Free cancellation up to 24 hours before your booking, directly in the Playtomic app.'),
     ('When are you open?','Every day 7am–11:30pm at both clubs.'),
     ('Changing rooms and showers?','Yes, at both clubs.'),
     ('Where do I park?','Salgesch: free parking on site, the station is a 15-minute walk. Sion: Route de Préjeux 16, see the directions under “Locations”.'),
     ('Can we split the payment?','Yes. Playtomic splits the court price automatically between the players.')],
  sa_extra='🅿️ Free parking · 🚆 15 min walk from Salgesch station', showers='Changing rooms &amp; showers'),
 'fr': dict(
  trust='<span class="ts-stars">★★★★★</span> <b>4.9</b> · 77 avis Google · 2 sites en Valais · tous les jours 7h–23h30',
  bb_h="Cours d'initiation chaque samedi à 10h à Sion", bb_k='Nouveau au padel ?',
  pr_h='Tarifs des courts', pr_lede='Prix par joueur, réparti automatiquement dans Playtomic.',
  pad='Padel indoor', pad_d='90 min', p1='17 CHF', p1d='par personne · lun–ven avant 17h', p2='20 CHF', p2d='par personne · dès 17h et le week-end',
  ten='Tennis', ten_p='dès 15 CHF', ten_d='par personne', pic='Pickleball', pic_p='Prix en direct', pic_d='sur Playtomic',
  pr_notes=['Location de raquette 3, 5 ou 10 CHF', 'Balles en vente sur place', "Annulation gratuite jusqu'à 24 h avant", 'Vestiaires et douches sur les deux sites'],
  pr_cta='Voir les créneaux libres', pr_cta2='Tarifs des cours',
  gift_k='Idée cadeau', gift_h='Offre du padel.', gift_p='Bons cadeaux dès 20 CHF, envoyés par e-mail et valables sur les deux sites.', gift_cta='Acheter un bon cadeau', shop='shop.html#vouchers',
  faq_h='Première fois ? Bon à savoir', faq_all='Toutes les questions →',
  q=[('Combien coûte un court ?',"Padel indoor (90 min) : 17 CHF par personne du lundi au vendredi avant 17h, 20 CHF par personne dès 17h et le week-end. Tennis dès 15 CHF par personne. Les prix du pickleball sont en direct sur Playtomic."),
     ("Je n'ai pas de raquette.","Loue-la au club pour 3, 5 ou 10 CHF (débutant / intermédiaire / pro), paiement par Twint. Balles en vente sur place."),
     ("Je n'ai jamais joué.","Viens au cours d'initiation, chaque samedi à 10h à Sion. Aucune expérience nécessaire, raquette à louer sur place. <a href=\"https://tinyurl.com/Academy-Sion\" target=\"_blank\" rel=\"noopener\">S'inscrire sur Playtomic</a>."),
     ('Comment annuler ?',"Annulation gratuite jusqu'à 24 h avant ta réservation, directement dans l'app Playtomic."),
     ('Quels sont les horaires ?','Tous les jours de 7h à 23h30, sur les deux sites.'),
     ('Y a-t-il des vestiaires et des douches ?','Oui, sur les deux sites.'),
     ('Où se garer ?',"Salgesch : parking gratuit sur place, la gare est à 15 min à pied. Sion : Route de Préjeux 16, voir l'itinéraire sous « Sites & horaires »."),
     ('Peut-on partager le paiement ?','Oui. Playtomic répartit automatiquement le prix du court entre les joueurs.')],
  sa_extra='🅿️ Parking gratuit · 🚆 15 min à pied de la gare de Salgesch', showers='Vestiaires &amp; douches'),
 'de': dict(
  trust='<span class="ts-stars">★★★★★</span> <b>4.9</b> · 77 Google-Bewertungen · 2 Standorte im Wallis · täglich 7–23:30 Uhr',
  bb_h='Einführungskurs jeden Samstag um 10 Uhr in Sion', bb_k='Neu im Padel?',
  pr_h='Platzpreise', pr_lede='Preis pro Person, in Playtomic automatisch aufgeteilt.',
  pad='Padel indoor', pad_d='90 Min.', p1='17 CHF', p1d='pro Person · Mo–Fr vor 17 Uhr', p2='20 CHF', p2d='pro Person · ab 17 Uhr & am Wochenende',
  ten='Tennis', ten_p='ab 15 CHF', ten_d='pro Person', pic='Pickleball', pic_p='Live-Preise', pic_d='auf Playtomic',
  pr_notes=['Schlägermiete 3, 5 oder 10 CHF', 'Bälle vor Ort erhältlich', 'Kostenlos stornieren bis 24 h vorher', 'Garderoben & Duschen an beiden Standorten'],
  pr_cta='Freie Zeiten ansehen', pr_cta2='Kurspreise',
  gift_k='Geschenkidee', gift_h='Schenk Padel.', gift_p='Geschenkgutscheine ab 20 CHF, per E-Mail verschickt und an beiden Standorten gültig.', gift_cta='Gutschein kaufen', shop='shop.html#vouchers',
  faq_h='Zum ersten Mal hier? Gut zu wissen', faq_all='Alle Fragen →',
  q=[('Was kostet ein Platz?','Padel indoor (90 Min.): 17 CHF pro Person Mo–Fr vor 17 Uhr, 20 CHF pro Person ab 17 Uhr und am Wochenende. Tennis ab 15 CHF pro Person. Die Pickleball-Preise siehst du live auf Playtomic.'),
     ('Ich habe keinen Schläger.','Miete einen im Club für 3, 5 oder 10 CHF (Einsteiger / Fortgeschritten / Pro), bezahlt wird mit Twint. Bälle gibt es vor Ort.'),
     ('Ich habe noch nie gespielt.','Komm in den Einführungskurs, jeden Samstag um 10 Uhr in Sion. Keine Vorkenntnisse nötig, Schläger kannst du vor Ort mieten. <a href="https://tinyurl.com/Academy-Sion" target="_blank" rel="noopener">Auf Playtomic anmelden</a>.'),
     ('Wie storniere ich?','Kostenlos bis 24 Stunden vor deiner Buchung, direkt in der Playtomic-App.'),
     ('Wann habt ihr offen?','Täglich von 7 bis 23:30 Uhr, an beiden Standorten.'),
     ('Gibt es Garderoben und Duschen?','Ja, an beiden Standorten.'),
     ('Wo kann ich parken?','Salgesch: Gratis-Parkplätze vor Ort, der Bahnhof ist 15 Gehminuten entfernt. Sion: Route de Préjeux 16, siehe Wegbeschreibung unter «Standorte».'),
     ('Kann man die Zahlung teilen?','Ja. Playtomic teilt den Platzpreis automatisch unter den Spielern auf.')],
  sa_extra='🅿️ Gratis-Parkplätze · 🚆 15 Gehminuten vom Bahnhof Salgesch', showers='Garderoben &amp; Duschen'),
}

def mark(name, html): return f'<!-- ux:{name} -->\n{html}\n<!-- /ux:{name} -->'
def put(s, name, html, anchor_re, where='after'):
    blk = mark(name, html)
    pat = re.compile(rf'<!-- ux:{name} -->.*?<!-- /ux:{name} -->', re.S)
    if pat.search(s): return pat.sub(lambda m: blk, s)
    m = re.search(anchor_re, s, re.S)
    assert m, (name, anchor_re)
    i = m.end() if where == 'after' else m.start()
    return s[:i] + '\n' + blk + '\n' + s[i:]

def prices(t):
    notes = ''.join(f'<li>{n}</li>' for n in t['pr_notes'])
    return f'''<section class="section-tight ux-prices" id="prices">
  <div class="wrap">
    <h2>{t['pr_h']}</h2>
    <p class="section-lede">{t['pr_lede']}</p>
    <div class="price-grid">
      <div class="price-card main"><p class="pc-sport">{t['pad']} <span>{t['pad_d']}</span></p>
        <div class="pc-row"><b>{t['p1']}</b><span>{t['p1d']}</span></div>
        <div class="pc-row"><b>{t['p2']}</b><span>{t['p2d']}</span></div></div>
      <div class="price-card"><p class="pc-sport">{t['ten']}</p><div class="pc-row"><b>{t['ten_p']}</b><span>{t['ten_d']}</span></div></div>
      <div class="price-card"><p class="pc-sport">{t['pic']}</p><div class="pc-row"><b class="pc-soft">{t['pic_p']}</b><span>{t['pic_d']}</span></div></div>
    </div>
    <ul class="price-notes">{notes}</ul>
    <div class="hero-actions">
      <a class="btn btn-green" href="{SA}" target="_blank" rel="noopener" data-pick="court">{t['pr_cta']}</a>
      <a class="btn btn-outline-blue" href="training.html">{t['pr_cta2']}</a>
    </div>
  </div>
</section>'''

def faq(t, n=None, more=True):
    qs = t['q'] if n is None else [t['q'][i] for i in n]
    items = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in qs)
    link = f'<p class="faq-more"><a href="book.html#faq">{t["faq_all"]}</a></p>' if more else ''
    return f'''<section class="section-tight ux-faq" id="faq">
  <div class="wrap">
    <h2>{t['faq_h']}</h2>
    <div class="faq-list">{items}</div>{link}
  </div>
</section>'''

def faq_schema(t):
    data = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in t['q']]}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>'

def gift(t):
    return f'''<section class="section-tight ux-gift">
  <div class="wrap">
    <a class="gift-banner" href="{t['shop']}">
      <span class="gb-icon" aria-hidden="true">🎁</span>
      <span class="gb-txt"><small>{t['gift_k']}</small><b>{t['gift_h']}</b><span>{t['gift_p']}</span></span>
      <span class="btn btn-green gb-btn">{t['gift_cta']}</span>
    </a>
  </div>
</section>'''

for lang, pre in (('en', ''), ('fr', 'fr/'), ('de', 'de/')):
    t = T[lang]
    # ---------- index ----------
    p = os.path.join(ROOT, pre, 'index.html'); s = open(p).read()
    # F9 trust strip inside hero, after hero-actions
    s = put(s, 'trust', f'<p class="trust-strip">{t["trust"]}</p>', r'<section class="hero hero-video".*?<div class="hero-actions">.*?</div>')
    # F7 naming: beginner banner -> intro course
    s = re.sub(r'(<section class="beginner-banner">.*?<p class="bb-kicker">).*?(</p>\s*<h2>).*?(</h2>)', lambda m: m.group(1) + t['bb_k'] + m.group(2) + t['bb_h'] + m.group(3), s, count=1, flags=re.S)
    # F1 prices: replace old prices section (the section-tight with training.html link and Playtomic price button)
    if '<!-- ux:prices -->' not in s:
        secs = list(re.finditer(r'<section class="section-tight">\s*<div class="wrap" style="text-align:center;">.*?</section>', s, re.S))
        old = [m for m in secs if 'href="training.html"' in m.group(0)]
        assert len(old) == 1, (lang, len(old))
        s = s[:old[0].start()] + mark('prices', prices(t)) + s[old[0].end():]
    else:
        s = put(s, 'prices', prices(t), '')
    # F6 gift banner right after prices
    s = put(s, 'gift', gift(t), r'<!-- /ux:prices -->')
    # F3 short FAQ before locations
    s = put(s, 'faq', faq(t, [0, 1, 2, 3, 6]).replace('id="faq"', 'id="faq-home"'), r'<section id="locations"', 'before')
    # F17 location extras (Salgesch parking/train, showers both)
    s = re.sub(r'\n?<!-- ux:sa-extra -->.*?<!-- /ux:sa-extra -->', '', s, flags=re.S)
    s = s.replace('<p class="location-address">Littenstrasse 30, 3970 Salgesch</p>', '<p class="location-address">Littenstrasse 30, 3970 Salgesch</p>' + mark('sa-extra', f'<p class="loc-extra">{t["sa_extra"]}</p>'), 1)
    s = re.sub(r'<span class="amenity-pill ux-sh">[^<]*</span>', '', s)
    s = re.sub(r'(<div class="amenity-row">(?:(?!</div>).)*?)(\s*</div>)', lambda m: m.group(1) + '\n            <span class="amenity-pill ux-sh">' + t['showers'] + '</span>' + m.group(2), s, flags=re.S)
    # F19 tu-form
    if lang == 'fr':
        s = s.replace('Réservez sur Playtomic →', 'Réserve sur Playtomic →').replace('Rejoignez la communauté WhatsApp', 'Rejoins la communauté WhatsApp')
    open(p, 'w').write(s)
    # ---------- book ----------
    p = os.path.join(ROOT, pre, 'book.html'); s = open(p).read()
    s = put(s, 'prices', prices(t), r'<section class="section-tight" style="text-align:center;">.*?</section>')
    s = put(s, 'faq', faq(t, more=False), r'<!-- /ux:prices -->')
    s = put(s, 'faq-schema', faq_schema(t), r'</head>', 'before')
    if lang == 'fr':
        s = s.replace('Réservez sur Playtomic →', 'Réserve sur Playtomic →')
    open(p, 'w').write(s)
print('ok')
