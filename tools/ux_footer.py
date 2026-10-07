"""UX v1 (Oct 2026): rich footer (hours, WhatsApp, links) on every page with .footer-grid. Idempotent."""
import os, re, glob
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WA = '41772780115'
F = {
 'en': dict(h='Daily 7am–11:30pm', dir='Directions', links='Quick links', L=[('book.html','Book a court'),('training.html','Courses'),('book.html#faq','FAQ'),('shop.html#vouchers','Gift vouchers'),('shop.html','Shop'),('events.html','Events')],
            c='Contact', wa='Message us on WhatsApp', wan='Quick reply · +41 77 278 01 15', txt='Hola! I have a question about Rackets Academy.'),
 'fr': dict(h='Tous les jours 7h–23h30', dir='Itinéraire', links='Liens rapides', L=[('book.html','Réserver un court'),('training.html','Cours'),('book.html#faq','FAQ'),('shop.html#vouchers','Bons cadeaux'),('shop.html','Shop'),('events.html','Événements')],
            c='Contact', wa='Écris-nous sur WhatsApp', wan='Réponse rapide · +41 77 278 01 15', txt="Hola ! J'ai une question sur la Rackets Academy."),
 'de': dict(h='Täglich 7–23:30 Uhr', dir='Route', links='Schnellzugriff', L=[('book.html','Platz buchen'),('training.html','Kurse'),('book.html#faq','FAQ'),('shop.html#vouchers','Geschenkgutscheine'),('shop.html','Shop'),('events.html','Events')],
            c='Kontakt', wa='Schreib uns auf WhatsApp', wan='Schnelle Antwort · +41 77 278 01 15', txt='Hola! Ich habe eine Frage zur Rackets Academy.'),
}
from urllib.parse import quote
def grid(t, pre):
    links = ''.join(f'<a href="{pre}{h}">{n}</a>' for h, n in t['L'])
    return (f'<div class="footer-grid ux-foot">'
      f'<div><h4>Salgesch</h4><a href="https://www.google.com/maps/search/?api=1&query=Littenstrasse+30+3970+Salgesch" target="_blank" rel="noopener">Littenstrasse 30, 3970 Salgesch</a><p>Padel · Pickleball · Tennis · Spa</p><p>{t["h"]}</p></div>'
      f'<div><h4>Sion</h4><a href="https://www.google.com/maps/search/?api=1&query=Route+de+Pr%C3%A9jeux+16+1950+Sion" target="_blank" rel="noopener">Route de Préjeux 16, 1950 Sion</a><p>Padel</p><p>{t["h"]}</p></div>'
      f'<div class="foot-links"><h4>{t["links"]}</h4>{links}</div>'
      f'<div class="footer-contact"><h4>{t["c"]}</h4><a class="foot-wa" href="https://wa.me/{WA}?text={quote(t["txt"])}" target="_blank" rel="noopener">{t["wa"]}</a><p>{t["wan"]}</p><a href="mailto:phil@racketsacademy.ch">phil@racketsacademy.ch</a></div>'
      f'</div>')
n = 0
for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    rel = os.path.relpath(p, ROOT)
    if rel.startswith(('tools', 'uploads', '.git')): continue
    s = open(p).read()
    if 'class="footer-grid' not in s: continue
    lang = (re.search(r'<html[^>]*lang="(..)', s) or [None, 'en'])[1]
    if lang not in F: lang = 'en'
    langroot = {'en': '', 'fr': 'fr', 'de': 'de'}[lang]
    d = os.path.dirname(rel)
    b = re.search(r'<base href="([^"]+)"', s)
    if b: d = os.path.normpath(os.path.join(d, b.group(1)))
    d = '' if d in ('.', '') else d
    pre = os.path.relpath(langroot or '.', d or '.')
    pre = '' if pre == '.' else pre + '/'
    s2 = re.sub(r'<div class="footer-grid[^"]*">.*?</div>\s*</div>(?=\s*<div class="sponsor-row")', grid(F[lang], pre), s, count=1, flags=re.S)
    if s2 == s:
        s2 = re.sub(r'<div class="footer-grid[^"]*">(?:(?!<div class="sponsor-row").)*?</div>\s*</div>\s*(?=\n\s*<div class="sponsor-row"|\n\s*<div class="footer-bottom")', grid(F[lang], pre), s, count=1, flags=re.S)
    if s2 != s: n += 1; open(p, 'w').write(s2)
    else: print('NOT REPLACED', rel)
print('footers updated:', n)
