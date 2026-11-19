"""Menü, Menüknopf und Footer-Links für alle Seiten (UX W2, Phil 19.11.2026).
Menü: Spielen & Preise · Training · Events · Kinder & Camps · Firmen · Spa · RACKETS+ · Shop + Knopf «Platz buchen».
Über uns, FAQ und Team-Login stehen im Footer. Der Menüknopf am Handy trägt das Wort «Menü» (auch für 60+ verständlich).
Idempotent. Nach jedem build_*.py laufen lassen:  python3 tools/ux_nav.py   (vom Repo-Wurzelordner)"""
import re, glob, os
T = {
 'de': dict(book='Spielen &amp; Preise', camps='Kinder &amp; Camps', co='Firmen', cta='Platz buchen', menu='Menü', close='Schliessen', about='Über uns', faq='FAQ', login='Team-Login'),
 'fr': dict(book='Jouer &amp; tarifs', camps='Enfants &amp; camps', co='Entreprises', cta='Réserver un terrain', menu='Menu', close='Fermer', about='À propos', faq='FAQ', login='Login équipe'),
 'en': dict(book='Play &amp; prices', camps='Kids &amp; camps', co='Companies', cta='Book a court', menu='Menu', close='Close', about='About', faq='FAQ', login='Team login'),
}
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
             ('company-events.html', t['co']), ('spa-and-sauna.html', 'Spa'), ('rackets-plus.html', 'RACKETS+'), ('shop.html', None)]
    out = ['<nav class="navlinks">']
    for href, label in items:
        act, old = link(href)
        if href == 'company-events.html' and name in ('company-events.html', 'company.html', 'sponsoring.html'): act = ' class="active"'
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
    if 'class="foot-more"' not in s and login:
        more = '<span class="foot-more"><a href="about.html">%s</a> · <a href="faq.html">%s</a> · <a href="%s" rel="nofollow">%s</a></span>\n      ' % (t['about'], t['faq'], login.group(1), t['login'])
        s = re.sub(r'(<div class="footer-bottom">\s*)', lambda m: m.group(1) + more, s, count=1)
    if s != o: open(path, 'w', encoding='utf-8').write(s)
    return s != o
if __name__ == '__main__':
    n = 0
    for f in glob.glob('*.html') + glob.glob('*/*.html') + glob.glob('*/*/*.html'):
        if f.startswith(('miatuya', 'uploads', 'padel4ever', 'fr/padel4ever', 'de/padel4ever')): continue
        n += fix(f)
    print('pages changed:', n)
