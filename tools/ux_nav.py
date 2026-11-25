"""Menü, Menüknopf und Footer-Links für alle Seiten (UX W2, Phil 19.11.2026).
Menü: Buchen · Training · Events · Camps · Firmen · Spa · Mitgliedschaft · Shop + Knopf «Platz buchen».
Über uns, FAQ und Team-Login stehen im Footer. Der Menüknopf am Handy trägt das Wort «Menü» (auch für 60+ verständlich).
Idempotent. Nach jedem build_*.py laufen lassen:  python3 tools/ux_nav.py   (vom Repo-Wurzelordner)"""
import re, glob, os
T = {
 'de': dict(book='Buchen', camps='Camps', co='Firmen', cta='Platz buchen', member='Mitgliedschaft', sponsor='Sponsor werden', menu='Menü', close='Schliessen', about='Über uns', faq='FAQ', login='Team-Login'),
 'fr': dict(book='Réserver', camps='Camps', co='Entreprises', cta='Réserver un terrain', member='Membres', sponsor='Devenir sponsor', menu='Menu', close='Fermer', about='À propos', faq='FAQ', login='Login équipe'),
 'en': dict(book='Book', camps='Camps', co='Companies', cta='Book a court', member='Membership', sponsor='Become a sponsor', menu='Menu', close='Close', about='About', faq='FAQ', login='Team login'),
}
V2_PAGES = {'tennis.html', 'pickleball.html', 'padel-valais.html',
            'training.html', 'camps.html', 'spa-and-sauna.html',
            'company.html', 'company-events.html', 'sponsoring.html', 'rackets-plus.html', 'kids-birthday.html',
            'kids-camp.html', 'kids-camp-winter.html', 'kids-camp-easter.html', 'kids-camp-summer.html'}   # events.html: eigener Stil (evw), schon in Hauptblau
V2_SPORT = {'tennis.html': 'TENNIS', 'pickleball.html': 'PICKLEBALL'}
def fix(path):
    s = open(path, encoding='utf-8').read()
    if '<nav class="navlinks">' not in s: return False
    m = re.search(r'<html[^>]*lang="(\w\w)', s); L = m.group(1) if m else 'en'
    if L not in T: L = 'en'
    t = T[L]; o = s
    a, b = s.index('<nav class="navlinks">'), s.index('</nav>', s.index('<nav class="navlinks">'))
    nav = s[a:b]
    def link(href):
        m = re.search(r'<a href="%s"( class="active")?\s*>([^<]*)</a>' % re.escape(href), nav)
        return (m.group(1) or '', m.group(2)) if m else ('', None)
    name = os.path.basename(path)
    login = re.search(r'<a class="nav-login" href="([^"]+)"', s)
    items = [('book.html', t['book']), ('training.html', None), ('events.html', None), ('camps.html', t['camps']),
             ('company.html', t['co']), ('spa-and-sauna.html', 'Spa'), ('rackets-plus.html', t['member']), ('shop.html', None)]
    out = ['<nav class="navlinks">']
    for href, label in items:
        act, old = link(href)
        if href == 'company.html' and name in ('company-events.html', 'company.html', 'sponsoring.html'): act = ' class="active"'
        if href == 'camps.html' and (name.startswith('kids-') or name == 'ski-and-padel.html'): act = ' class="active"'
        out.append('      <a href="%s"%s>%s</a>' % (href, act, label or old or href))
    ls = re.search(r'\n(\s*<div class="lang-switch">.*?</div>\s*</div>)', nav, flags=re.S)
    if ls: out.append(ls.group(1).strip('\n'))
    mob = re.search(r'\n(\s*<a class="nav-cta-mobile" href="(?!book\.html)[^>]*>[^<]*</a>)', nav)   # Sonder-Knopf (z. B. Tickets) bleibt
    if mob: out.append(mob.group(1).strip('\n'))
    s = s[:a] + '\n'.join(out) + '\n    ' + s[b:]
    s = re.sub(r'<a class="nav-cta" href="book\.html"(?: data-pick="court")?>[^<]*</a>', '<a class="nav-cta" href="book.html" data-pick="court">%s</a>' % t['cta'], s)
    s = re.sub(r'<button class="nav-toggle[^>]*>.*?</button>',
               '<button class="nav-toggle nav-toggle-word" aria-label="%s" aria-expanded="false"><i class="nt-bars"><b></b><b></b><b></b></i><em class="nt-open">%s</em><em class="nt-close">%s</em></button>' % (t['menu'], t['menu'], t['close']), s, flags=re.S)
    m = re.search(r'<span class="foot-more">.*?href="([^"]*intern\.html)".*?</span>\n\s*', s, flags=re.S)
    lg = login.group(1) if login else (m.group(1) if m else None)
    if lg:
        # FAQ steht schon unter «Schnellzugriff»; in der unteren Zeile nicht doppelt (UX-Check 23.11.2026)
        more = '<span class="foot-more"><a href="about.html">%s</a> · <a href="sponsoring.html">%s</a> · <a href="%s" rel="nofollow">%s</a></span>\n      ' % (t['about'], t['sponsor'], lg, t['login'])
        if m: s = s[:m.start()] + more + s[m.end():]
        else: s = re.sub(r'(<div class="footer-bottom">\s*)', lambda x: x.group(1) + more, s, count=1)
    # Footer Salgesch: Pickleball und Tennis als Links (Wochenlauf 23.11.2026, interne Links zu den Prio-Produkten)
    s = s.replace('<p>Padel · Pickleball · Tennis · Spa</p>', '<p>Padel · <a class="foot-sport" href="pickleball.html">Pickleball</a> · <a class="foot-sport" href="tennis.html">Tennis</a> · Spa</p>')
    # Vorschaubilder (og:image, JSON-LD) bleiben JPG/PNG: nicht jede Plattform zeigt WebP
    def orig(m):
        base = m.group(2)
        for ext in ('.jpg', '.jpeg', '.png'):
            if os.path.exists(base + ext): return m.group(1) + base + ext
        return m.group(0)
    lines = s.split('\n')
    for i, l in enumerate(lines):
        if '.webp' in l and ('og:image' in l or 'twitter:image' in l or 'application/ld+json' in l):
            lines[i] = re.sub(r'(https://www\.racketsacademy\.ch/)((?:images|uploads)/[^"\s]+?)\.webp', orig, l)
    s = '\n'.join(lines)
    # Design v2 (Rollout Nov 2026): diese Seiten bekommen die Klasse «v2» (Stil dazu am Ende von styles.css).
    # Steht hier, weil ux_nav.py nach jedem build_*.py laeuft: so bleibt die Klasse auch nach einem Neubau erhalten.
    if name in V2_PAGES:
        s = re.sub(r'<body(?: class="([^"]*)")?>', lambda m: '<body class="%s">' % ' '.join(dict.fromkeys(((m.group(1) or '').split() + ['v2']))), s, count=1)
        sport = V2_SPORT.get(name)
        if sport:   # Knopf fuehrt direkt zu den freien Zeiten dieser Sportart
            s = s.replace('href="https://playtomic.com/clubs/rackets-academy-salgesch"', 'href="https://playtomic.com/clubs/rackets-academy-salgesch?sport=%s"' % sport)
    if s != o: open(path, 'w', encoding='utf-8').write(s)
    return s != o
if __name__ == '__main__':
    n = 0
    for f in glob.glob('*.html') + glob.glob('*/*.html') + glob.glob('*/*/*.html'):
        if f.startswith(('miatuya', 'uploads', 'padel4ever', 'fr/padel4ever', 'de/padel4ever')): continue
        n += fix(f)
    print('pages changed:', n)
