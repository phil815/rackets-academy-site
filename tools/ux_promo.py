"""Laufband oben auf allen Seiten in normaler Schreibweise, ohne Emoji (Markenregel: keine Grossbuchstaben-Texte).
Gleicher Wortlaut wie bisher, nur die Schreibweise aendert sich. Idempotent. Vom Repo-Wurzelordner: python3 tools/ux_promo.py"""
import glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAIRS = [('🎾 PLÄTZE JETZT OFFEN — ', 'Plätze jetzt offen — '),
         ('🎾 COURTS OPEN NOW — ', 'Courts open now — '), ('>Book Now on Playtomic →<', '>Book now on Playtomic →<'),
         ('🎾 COURTS OUVERTS — ', 'Courts ouverts — ')]
n = 0
for path in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True):
    s = open(path, encoding='utf-8').read()
    if 'promo-track' not in s: continue
    o = s
    for a, b in PAIRS: s = s.replace(a, b)
    if s != o:
        open(path, 'w', encoding='utf-8').write(s); n += 1
print('pages changed:', n)
