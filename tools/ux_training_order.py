"""Trainingsseite (EN/FR/DE), UX W15 (Nov 2026): Plaene und Preise direkt nach dem Kopf und den drei Einstiegskarten.
Die drei erklaerenden Abschnitte (Abo-Vorteile, Beispiel-Feedback, Preis-Zeile mit Knopf) ruecken hinter die Plaene,
vor «Noch Fragen?». Es werden nur vorhandene Abschnitte verschoben, kein Text aendert sich.
Idempotent. Nach build_training.py / build_training_plans.py / ux_training.py laufen lassen, danach ux_nav.py.
Vom Repo-Wurzelordner:  python3 tools/ux_training_order.py"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A, Z = '<!-- ux:tr-after -->', '<!-- /ux:tr-after -->'
SEC = re.compile(r'<section class="co2-sec(?: co2-proof)?">.*?</section>\s*', re.S)

for pre in ('', 'fr', 'de'):
    path = os.path.join(ROOT, pre, 'training.html')
    s = open(path, encoding='utf-8').read()
    plans = s.index('<section class="co3-head" id="plans">')
    # erklaerende Abschnitte, die (noch) vor den Plaenen stehen
    top = [m for m in SEC.finditer(s, 0, plans) if any(k in m.group(0) for k in ('co2-bens', 'co2-proof', 'co2-price'))]
    old = re.search(re.escape(A) + r'(.*?)' + re.escape(Z) + r'\n*', s, re.S)
    if top:
        block = ''.join(m.group(0).rstrip() + '\n\n' for m in top).rstrip()
        for m in reversed(top):
            s = s[:m.start()] + s[m.end():]
        old = re.search(re.escape(A) + r'(.*?)' + re.escape(Z) + r'\n*', s, re.S)
        if old: s = s[:old.start()] + s[old.end():]
    elif old:
        block = old.group(1).strip()
        s = s[:old.start()] + s[old.end():]
    else:
        raise SystemExit('Abschnitte nicht gefunden: ' + path)
    q = s.rindex('<section class="section-tight" style="text-align:center;">')
    s = s[:q] + A + '\n' + block + '\n' + Z + '\n\n' + s[q:]
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', os.path.join(pre, 'training.html'))
