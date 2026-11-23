"""Buchungsseite v2 (Musterseite fuer den Rollout des Startseiten-Designs, Nov 2026). Betrifft book.html in EN/FR/DE.
Texte bleiben unveraendert. Es aendert sich nur Gestaltung und Reihenfolge:
  Hero (Foto, dunkel) -> Live-Verfuegbarkeit mit Buchungsblock der Startseite (statt der zwei Standort-Knoepfe)
  -> Platzpreise -> Plaetze / Offene Matches / Turniere -> Playtomic-App -> Fragen -> Nicht auf Playtomic?
Stil und Logik: home-v2.css / home-v2.js (gleiche Version wie die Startseite). Der Buchungsblock wird aus der
Startseite der jeweiligen Sprache uebernommen, also zuerst tools/ux_home_v2.py laufen lassen.
Idempotent: Markerbloecke <!-- ux:bv2-NAME --> werden beim erneuten Lauf ersetzt."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VER = re.search(r"^VER = '(\d+)'", open(os.path.join(ROOT, 'tools', 'ux_home_v2.py'), encoding='utf-8').read(), re.M).group(1)

for pre, p in [('', ''), ('fr', '../'), ('de', '../')]:
    path = os.path.join(ROOT, pre, 'book.html')
    s = open(path, encoding='utf-8').read()
    home = open(os.path.join(ROOT, pre, 'index.html'), encoding='utf-8').read()

    # body-Klasse, Stil und Logik
    s = re.sub(r'<body(?: class="[^"]*")?>', '<body class="home-v2 book-v2">', s, count=1)
    s = re.sub(r'\n<link rel="stylesheet" href="[^"]*home-v2\.css\?v=\d+">', '', s)
    s = re.sub(r'(<link rel="stylesheet" href="[^"]*styles\.css\?v=\d+">)', lambda m: m.group(1) + '\n<link rel="stylesheet" href="%shome-v2.css?v=%s">' % (p, VER), s, count=1)
    s = re.sub(r'<script src="[^"]*home-v2\.js\?v=\d+" defer></script>\n', '', s)
    s = s.replace('</body>', '<script src="%shome-v2.js?v=%s" defer></script>\n</body>' % (p, VER), 1)
    assert 'home-v2.css' in s and 'home-v2.js' in s

    # Buchungsblock der Startseite (nur die Karte) statt der zwei Standort-Knoepfe
    card = re.search(r'<div class="hv2-card".*?\n    </div>(?=\n  </div>\n</section>\n<!-- /ux:hv2-book -->)', home, re.S)
    assert card, 'Buchungsblock in index.html nicht gefunden'
    new = '<!-- ux:bv2-book -->\n    %s\n    <!-- /ux:bv2-book -->' % card.group(0)
    pat = re.compile(r'<!-- ux:bv2-book -->.*?<!-- /ux:bv2-book -->', re.S)
    if pat.search(s):
        s = pat.sub(lambda m: new, s, count=1)
    else:
        s, n = re.subn(r'<div class="hero-actions"[^>]*>\s*<a class="btn btn-green"[^>]*data-book-modal>[^<]*</a>\s*<a class="btn btn-green"[^>]*data-book-modal>[^<]*</a>\s*</div>', lambda m: new, s, count=1)
        assert n == 1, 'Standort-Knoepfe nicht gefunden'

    # Fragen hinter die Playtomic-App ruecken (vor «Nicht auf Playtomic?»)
    faq = re.search(r'<!-- ux:faq -->.*?<!-- /ux:faq -->\n', s, re.S)
    assert faq
    rest = s[:faq.start()] + s[faq.end():]
    last = [m.start() for m in re.finditer(r'<section class="section-tight" style="text-align:center;">', rest)][-1]
    if rest[:last].rstrip().endswith('</section>') and '<!-- /ux:faq -->' not in rest:
        s = rest[:last] + faq.group(0) + '\n' + rest[last:]

    open(path, 'w', encoding='utf-8').write(s)
    print('ok', os.path.join(pre, 'book.html'))
