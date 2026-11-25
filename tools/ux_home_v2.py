"""Startseite v2 (Nov 2026, Gutis OK 23.11.): Nachtfoto-Hero mit Video, Buchungsblock (Standort, Sport, Tag ->
Playtomic), neun Fotokacheln. Betrifft nur index.html in EN/FR/DE. Stil: home-v2.css, Logik: home-v2.js.
Idempotent: Bloecke stehen zwischen <!-- ux:hv2-NAME --> ... <!-- /ux:hv2-NAME --> und werden beim erneuten Lauf ersetzt.
Titel, H1, Meta und alle uebrigen Abschnitte bleiben unveraendert."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = '6'
# Web-App «Free slots» (Apps Script, deployt 23.11.2026; bei Änderungen neue Version auf DIESEM Deployment). Leer = Anzeige der freien Padel-Plätze bleibt aus, nur der Link zu Playtomic.
FREE_URL = 'https://script.google.com/macros/s/AKfycbyhaXT98MOSUwf7W7f09CfWK21OaJP3MDpi2dZMk09LLelhNF_Hp5gKe68cpekoxryCEA/exec'
SA = 'https://playtomic.com/tenant/f89dfa07-4283-453e-8be3-316f9bd060d3'

T = {
 'en': dict(file='index.html', p='',
  promo=('🎾 COURTS OPEN NOW — ', 'Courts open now — '), promo_a=('Book Now on Playtomic', 'Book now on Playtomic'),
  aria='Book a court', wo='Where', was='What', wann='When', today='Today', tomorrow='Tomorrow', weekend='Weekend',
  free_lead='Free padel courts', free_parts='Morning|Afternoon|Evening', free_one='1 court free', free_n='{n} courts free', free_full='Fully booked', free_asof='As of {t}',
  cta='See free slots', note='You book securely on Playtomic', note_sion='Pickleball and tennis are in Salgesch',
  more='Also here: <a href="company.html#discount">Company discount</a> · <a href="shop.html#vouchers">Gift vouchers</a>',
  tiles=[('Play', 'Padel, tennis and pickleball. Pick your court and book directly, from CHF 17 per person.'),
         ('Courses &amp; Training', 'Group courses for kids and adults from 19.– per session, plus private lessons.'),
         ('Events', 'Monthly events combining sport, food and social moments. Also bookable privately.'),
         ('Kids &amp; camps', 'Holiday camps, kids’ birthdays and Ski &amp; Padel weekends.'),
         ('Companies', 'Team events on request, company discount and sponsoring.'),
         ('Spa', 'Relax and recover in our wellness area with sauna, hammam and jacuzzi.'),
         ('Tennis', 'Two indoor courts in Salgesch, 20 min from Sion, from CHF 15 per person.'),
         ('Pickleball', 'Three indoor courts in Salgesch, 18 min from Sion, from CHF 5 per person.'),
         ('Shop', 'Rackets, gift vouchers and gift ideas.')]),
 'fr': dict(file='fr/index.html', p='../',
  promo=('🎾 COURTS OUVERTS — ', 'Courts ouverts — '), promo_a=None,
  aria='Réserver un court', wo='Où', was='Quoi', wann='Quand', today="Aujourd'hui", tomorrow='Demain', weekend='Week-end',
  free_lead='Courts de padel libres', free_parts='Matin|Après-midi|Soir', free_one='1 court libre', free_n='{n} courts libres', free_full='Complet', free_asof='État à {t}',
  cta='Voir les créneaux libres', note='Tu réserves en toute sécurité sur Playtomic', note_sion='Pickleball et tennis sont à Salgesch',
  more='Aussi chez nous : <a href="company.html#discount">Rabais entreprise</a> · <a href="shop.html#vouchers">Bons cadeaux</a>',
  tiles=[('Jouer', 'Padel, tennis et pickleball. Choisis ton terrain et réserve directement, dès 17 CHF par personne.'),
         ('Cours &amp; entraînement', 'Cours en groupe pour enfants et adultes dès 19.– la séance, et cours privés.'),
         ('Événements', 'Des événements chaque mois entre sport, bonne bouffe et ambiance conviviale. Réservable en privé aussi.'),
         ('Enfants &amp; camps', 'Camps de vacances, anniversaires et week-ends Ski &amp; Padel.'),
         ('Entreprises', 'Événements d’équipe sur demande, rabais entreprise et sponsoring.'),
         ('Spa', 'Détends-toi dans notre espace bien-être avec sauna, hammam et jacuzzi.'),
         ('Tennis', 'Deux courts couverts à Salgesch, à 20 min de Sion, dès 15 CHF par personne.'),
         ('Pickleball', 'Trois courts indoor à Salgesch, à 18 min de Sion, dès 5 CHF par personne.'),
         ('Shop', 'Raquettes, bons cadeaux et idées cadeaux.')]),
 'de': dict(file='de/index.html', p='../',
  promo=('🎾 PLÄTZE JETZT OFFEN — ', 'Plätze jetzt offen — '), promo_a=None,
  aria='Platz buchen', wo='Wo', was='Was', wann='Wann', today='Heute', tomorrow='Morgen', weekend='Wochenende',
  free_lead='Freie Padel-Plätze', free_parts='Vormittag|Nachmittag|Abend', free_one='1 Platz frei', free_n='{n} Plätze frei', free_full='Ausgebucht', free_asof='Stand {t}',
  cta='Freie Zeiten ansehen', note='Du buchst sicher über Playtomic', note_sion='Pickleball und Tennis gibt es in Salgesch',
  more='Auch bei uns: <a href="company.html#discount">Firmenrabatt</a> · <a href="shop.html#vouchers">Geschenkgutscheine</a>',
  tiles=[('Spielen', 'Padel, Tennis und Pickleball. Platz wählen und direkt buchen, ab 17 CHF pro Person.'),
         ('Kurse &amp; Training', 'Gruppenkurse für Kinder und Erwachsene ab 19.– pro Lektion, plus Privatstunden.'),
         ('Events', 'Monatliche Events mit Sport, Essen und geselligen Momenten. Auch privat buchbar.'),
         ('Kinder &amp; Camps', 'Feriencamps, Kindergeburtstag und Ski &amp; Padel-Wochenenden.'),
         ('Firmen', 'Teamevents auf Anfrage, Firmenrabatt und Sponsoring.'),
         ('Spa', 'Entspanne dich in unserem Wellnessbereich mit Sauna, Hammam und Jacuzzi.'),
         ('Tennis', 'Zwei Hallenplätze in Salgesch, 20 Min. ab Sion und Visp, ab 15 CHF pro Person.'),
         ('Pickleball', 'Drei Indoor-Plätze in Salgesch, 20 Min. ab Visp, ab 5 CHF pro Person.'),
         ('Shop', 'Schläger, Gutscheine und Geschenkideen.')]),
}
# (Bild, Ziel, Zusatzattribute, Zusatzklasse) in der Reihenfolge der Kacheln
TILES = [('play', SA, ' target="_blank" rel="noopener" data-pick="court"', ''),
         ('training', 'training.html', '', ''), ('events', 'events.html', '', ''), ('kids', 'camps.html', '', ''),
         ('company', 'company.html', '', ''), ('spa', 'spa-and-sauna.html', '', ''),
         ('tennis', 'tennis.html', '', ''), ('pickleball', 'pickleball.html', '', ''), ('shop', 'shop.html', '', ' hv2-top')]


def block(name, body):
    return '<!-- ux:hv2-%s -->\n%s\n<!-- /ux:hv2-%s -->' % (name, body, name)


def put(s, name, body, first_time):
    """Ersetzt einen vorhandenen Markerblock, sonst wendet es first_time(s, neuer_block) an."""
    new = block(name, body)
    pat = re.compile(r'<!-- ux:hv2-%s -->.*?<!-- /ux:hv2-%s -->' % (name, name), re.S)
    if pat.search(s):
        return pat.sub(lambda m: new, s, count=1)
    out = first_time(s, new)
    assert out != s, 'Anker fuer Block %s nicht gefunden' % name
    return out


def book_html(t):
    pill = lambda attr, label, on=False: '<button type="button" class="hv2-pill" aria-pressed="%s" %s>%s</button>' % ('true' if on else 'false', attr, label)
    return '''<section class="hv2-book" aria-label="%(aria)s">
  <div class="wrap">
    <div class="hv2-card" data-hv2-book data-free-url="%(free_url)s">
      <div class="hv2-group"><p class="hv2-label" id="hv2-wo">%(wo)s</p><div class="hv2-pills" role="group" aria-labelledby="hv2-wo">%(clubs)s</div></div>
      <div class="hv2-group"><p class="hv2-label" id="hv2-was">%(was)s</p><div class="hv2-pills" role="group" aria-labelledby="hv2-was">%(sports)s</div></div>
      <div class="hv2-group"><p class="hv2-label" id="hv2-wann">%(wann)s</p><div class="hv2-pills" role="group" aria-labelledby="hv2-wann">%(days)s</div></div>
      <div class="hv2-go"><a class="btn btn-green hv2-cta" href="https://playtomic.com/clubs/rackets-academy-salgesch?sport=PADEL" target="_blank" rel="noopener">%(cta)s</a><p class="hv2-note" data-std="%(note)s" data-sion="%(note_sion)s">%(note)s</p></div>
      <div class="hv2-free" hidden aria-live="polite" data-lead="%(free_lead)s" data-parts="%(free_parts)s" data-one="%(free_one)s" data-n="%(free_n)s" data-full="%(free_full)s" data-asof="%(free_asof)s"></div>
    </div>
  </div>
</section>''' % dict(t, free_url=FREE_URL,
        clubs=pill('data-club="salgesch"', 'Salgesch', True) + pill('data-club="sion"', 'Sion'),
        sports=pill('data-sport="PADEL"', 'Padel', True) + pill('data-sport="PICKLEBALL"', 'Pickleball') + pill('data-sport="TENNIS"', 'Tennis'),
        days=pill('data-day="0"', t['today'], True) + pill('data-day="1"', t['tomorrow']) + pill('data-day="we"', t['weekend']))


def tiles_html(t):
    rows = []
    for (img, href, extra, cls), (h, p) in zip(TILES, t['tiles']):
        rows.append('      <a class="hv2-tile%s" href="%s"%s><img src="%simages/home/tile-%s.webp" alt="" width="960" height="720" loading="lazy"><div class="hv2-tile-text"><h3>%s</h3><p>%s</p></div></a>'
                    % (cls, href, extra, t['p'], img, h, p))
    return '    <div class="hv2-tiles">\n' + '\n'.join(rows) + '\n    </div>\n    <p class="offer-more">' + t['more'] + '</p>'


for lang, t in T.items():
    path = os.path.join(ROOT, t['file'])
    s = open(path, encoding='utf-8').read()
    p = t['p']

    # body-Klasse, Stil und Logik
    s = s.replace('<body>', '<body class="home-v2">', 1)
    assert 'class="home-v2"' in s
    s = re.sub(r'\n<link rel="stylesheet" href="[^"]*home-v2\.css\?v=\d+">', '', s)
    s = re.sub(r'(<link rel="stylesheet" href="[^"]*styles\.css\?v=\d+">)', lambda m: m.group(1) + '\n<link rel="stylesheet" href="%shome-v2.css?v=%s">' % (p, VER), s, count=1)
    s = re.sub(r'<script src="[^"]*home-v2\.js\?v=\d+" defer></script>\n', '', s)
    s = s.replace('</body>', '<script src="%shome-v2.js?v=%s" defer></script>\n</body>' % (p, VER), 1)
    assert 'home-v2.css' in s and 'home-v2.js' in s

    # Laufband in normaler Schreibweise (Markenregel: keine Grossbuchstaben-Texte)
    s = s.replace(*t['promo'])
    if t['promo_a']:
        s = s.replace(*t['promo_a'])

    # Hero: der einzelne Knopf weicht dem Buchungsblock direkt darunter
    s = put(s, 'hero-cta', '', lambda x, new: re.sub(
        r'<div class="hero-actions">\s*<a class="btn btn-green"[^>]*>[^<]*</a>\s*</div>(?=\s*<!-- ux:trust -->)', lambda m: new, x, count=1, flags=re.S))

    # Buchungsblock nach dem Hero
    s = put(s, 'book', book_html(t), lambda x, new: x.replace('\n<section class="beginner-banner">', '\n' + new + '\n\n<section class="beginner-banner">', 1))

    # Neun Fotokacheln statt der sechs Karten samt Zeile «Auch bei uns»
    s = put(s, 'tiles', tiles_html(t), lambda x, new: re.sub(
        r'[ \t]*<div class="grid-3">\s*<a class="card card-link offer".*?<p class="offer-more">.*?</p>', lambda m: new, x, count=1, flags=re.S))

    open(path, 'w', encoding='utf-8').write(s)
    print('ok', t['file'])
