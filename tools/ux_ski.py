"""Ski & Padel: Reihenfolge und Länge der Seite (UX W6, Phil 19.11.2026). Texte, Titel, FAQ, Preise und Buchungslogik bleiben.
Reihenfolge: Hero (Preis sichtbar, Hinweis Sport-Lodge) → Was inklusive ist (kompakt) → Programm → Gruppe → Gästestimmen
→ Buchung → Mindestniveau + Sport-Lodge (offen) → Fotos (12, Rest per Knopf) → Storno (eingeklappt) → FAQ → Schluss.
Buchungsfenster: ein Häkchen statt drei (die drei Felder gehen weiter an den Server).
Arbeitet auf dem fertigen HTML, idempotent. Nach build_camps.py:  python3 tools/ux_ski.py && python3 tools/ux_nav.py"""
import re
T = {'de': ('Ich bestätige:', 'Alle {n} Fotos zeigen'), 'fr': ('Je confirme :', 'Voir les {n} photos'), 'en': ('I confirm:', 'Show all {n} photos')}
for L, p in [('en', 'ski-and-padel.html'), ('fr', 'fr/ski-and-padel.html'), ('de', 'de/ski-and-padel.html')]:
    s = open(p, encoding='utf-8').read()
    if 'inc-compact' in s: print(p, 'schon umgestellt'); continue
    a = s.index('<section class="section-tight crew-block">'); b = s.index('<div class="buy-modal-overlay"')
    mid = s[a:b]
    def cut(marker, end='</section>'):
        global mid
        i = mid.index(marker); j = mid.index(end, i) + len(end); x = mid[i:j]; mid = mid[:i] + mid[j:]; return x
    crew = cut('<section class="section-tight crew-block">')
    testi = cut('<section class="section-tight" style="background:var(--paper);">')
    book = cut('<section class="section-tight camp-book" id="camp-book">')
    level = cut('<section class="section-tight">')
    canc = cut('<section class="section-tight" id="cancellation">')
    inc = cut('<section>')
    gal = cut('<section class="section-tight" id="gallery">')
    prog = cut('<section class="section-tight" style="background:var(--paper);">')
    faq = cut('<section class="section-tight">')
    final = cut('<section class="section-tight" style="text-align:center;">')
    rest = mid   # Lightbox (gal-box) samt Style/Script: muss nach der Galerie stehen
    assert 'camp-rules' in level and 'grid-3' in inc and 'gal-item' in gal and 'gal-box' in rest, p
    inc = inc.replace('<section>', '<section class="inc-compact">', 1)
    inc = re.sub(r' style="width:100%; height:140px; object-fit:cover; border-radius:12px; margin-bottom:14px;"', '', inc)
    h = re.search(r'<h2>(.*?)</h2>', canc).group(1); canc = canc.replace('<h2>' + h + '</h2>', '', 1)
    i = canc.index('>', canc.index('<div class="wrap"')) + 1; j = canc.rindex('</div>')
    canc = canc[:i] + '\n<details class="ski-acc"><summary>' + h + '</summary>' + canc[i:j] + '</details>\n' + canc[j:]
    n = gal.count('class="gal-item"'); gal = gal.replace('<div class="gal">', '<div class="gal gal-short">', 1); i = gal.rindex('</div>')
    gal = gal[:i] + '<p style="text-align:center;margin-top:16px;"><button type="button" class="btn btn-outline" onclick="this.closest(\'section\').querySelector(\'.gal\').classList.remove(\'gal-short\');this.parentNode.remove()">%s</button></p>\n  ' % T[L][1].format(n=n) + gal[i:]
    s = s[:a] + '\n'.join([inc, prog, crew, testi, book, level, gal, rest, canc, faq, final]) + '\n' + s[b:]
    # Hero: Preis gross beim Knopf, Hinweis Sport-Lodge als Chip
    chips = re.search(r'<div class="camp-chips">(.*?)</div>', s).group(1)
    cl = re.findall(r'<span>(.*?)</span>', chips); price = next(c for c in cl if 'CHF' in c)
    pp = re.search(r'<span class="camp-pack-price">[^<]*<small>(.*?)</small>', s).group(1)
    lodge = re.sub(r'^\W+\s*', '', re.search(r'<div class="camp-stay">\s*<h3>(.*?)</h3>', s, flags=re.S).group(1))
    newchips = ''.join('<span>%s</span>' % c for c in cl if c != price) + '<span>%s</span>' % lodge
    s = s.replace('<div class="camp-chips">' + chips + '</div>', '<div class="camp-chips">' + newchips + '</div>', 1)
    s = s.replace('<div class="hero-actions"><a class="btn btn-green" href="#camp-book">', '<p class="ski-price">%s <small>%s</small></p>\n    <div class="hero-actions"><a class="btn btn-green" href="#camp-book">' % (price, pp), 1)
    # ein Häkchen statt drei
    m = re.search(r'<label class="camp-check"><input type="checkbox" name="levelOk" value="yes" required><span>(.*?)</span></label>\s*<label class="camp-check"><input type="checkbox" name="lodgingOk" value="yes" required><span>(.*?)</span></label>\s*<label class="camp-check"><input type="checkbox" name="cancelOk" value="yes" required><span>(.*?)</span></label>', s, flags=re.S)
    one = ('<label class="camp-check camp-check-one"><input type="checkbox" name="allOk" value="yes" required><span><b>%s</b><br>· %s<br>· %s<br>· %s</span></label>'
           '<input type="hidden" name="levelOk" value="yes"><input type="hidden" name="lodgingOk" value="yes"><input type="hidden" name="cancelOk" value="yes">') % (T[L][0], m.group(1), m.group(2), m.group(3))
    s = s[:m.start()] + one + s[m.end():]
    open(p, 'w', encoding='utf-8').write(s); print(p, 'ok', price, pp, '|', lodge, '|', n)
