"""Free shipping (Guti 27.11.2026): every racket costs 10 CHF more, shipping by post is included.
Before: racket price + 9 CHF shipping. After: racket price + 10, shipping 0.

IMPORTANT, order at go-live:
1. Shop app (Apps Script): SHIPPING_CHF_ = 0, new version deployed by Guti. Until then the app still adds 9 CHF.
2. Shop sheet, tab RacketStock: every price + 10 (the shop takes the live price from there).
3. Run this tool, then tools/ux_nav.py, push.
Doing 2 or 3 before 1 would charge customers price + 10 + 9.

What this tool changes (EN/FR/DE), from repo root: python3 tools/ux_free_shipping.py
- all texts "shipping for 9 CHF" -> free shipping (racket pages, shop, guide, Siux page, terms, build tools)
- nav.js: RA_SHIP_CHF = 0 and "(free)" instead of "(+9 CHF)"; nav.js version +1 in every page
- product data: shippingRate 0
- static prices in shop.html and on the racket pages + 10 (fallback and what Google reads)
Running it twice changes nothing the second time (marker in nav.js)."""
import re, glob, sys

TEXT = [
 # English
 ('1–2 working days by post anywhere in Switzerland, for 9 CHF. Pick-up in Salgesch or Sion is free.', '1–2 working days by post anywhere in Switzerland, free of charge. You can also pick up in Salgesch or Sion.'),
 ('or shipping by post for 9 CHF', 'or free shipping by post'),
 ('or shipping for 9 CHF in 1–2 working days', 'or free shipping in 1–2 working days'),
 ('or shipping in Switzerland for 9 CHF', 'or free shipping in Switzerland'),
 ('Shipping 9 CHF', 'Free shipping'),
 ('have it shipped by post for 9 CHF', 'have it shipped by post for free'),
 ('by post for 9 CHF (dispatched', 'by post free of charge (dispatched'),
 ('have it sent by post for 9 CHF', 'have it sent by post for free'),
 ('We ship by post anywhere in Switzerland for 9 CHF, or', 'We ship by post anywhere in Switzerland for free, or'),
 # Deutsch
 ('1–2 Werktage per Post in die ganze Schweiz, für 9 CHF. Die Abholung in Salgesch oder Sion ist gratis.', '1–2 Werktage per Post in die ganze Schweiz, gratis. Abholen in Salgesch oder Sion geht auch.'),
 ('oder Versand per Post für 9 CHF', 'oder Gratis-Versand per Post'),
 ('oder Versand für 9 CHF in 1–2 Werktagen', 'oder Gratis-Versand in 1–2 Werktagen'),
 ('oder Versand in der Schweiz für 9 CHF', 'oder Gratis-Versand in der Schweiz'),
 ('Versand 9 CHF', 'Versand gratis'),
 ('lass es dir für 9 CHF per Post schicken', 'lass es dir gratis per Post schicken'),
 ('per Post für 9 CHF (Versand innert', 'gratis per Post (Versand innert'),
 ('oder für 9 CHF per Post schicken lassen', 'oder gratis per Post schicken lassen'),
 ('Versand per Post in die ganze Schweiz für 9 CHF, oder', 'Gratis-Versand per Post in die ganze Schweiz, oder'),
 # Français
 ('1–2 jours ouvrables par la Poste partout en Suisse, pour 9 CHF. Le retrait à Salgesch ou Sion est gratuit.', '1–2 jours ouvrables par la Poste partout en Suisse, gratuitement. Le retrait à Salgesch ou Sion est aussi possible.'),
 ('ou envoi par la Poste pour 9 CHF', 'ou envoi gratuit par la Poste'),
 ('ou envoi pour 9 CHF en 1–2 jours ouvrables', 'ou envoi gratuit en 1–2 jours ouvrables'),
 ('ou envoi en Suisse pour 9 CHF', 'ou envoi gratuit en Suisse'),
 ('Envoi 9 CHF', 'Envoi gratuit'),
 ('fais-la envoyer par la Poste pour 9 CHF', 'fais-la envoyer gratuitement par la Poste'),
 ('par la Poste pour 9 CHF (envoi sous', 'gratuitement par la Poste (envoi sous'),
 ('ou reçois-la par la Poste pour 9 CHF', 'ou reçois-la gratuitement par la Poste'),
 ('Envoi par la Poste partout en Suisse pour 9 CHF, ou', 'Envoi gratuit par la Poste partout en Suisse, ou'),
]
PLUS = 10
MARK = '// free shipping since 2026-11 (tools/ux_free_shipping.py)'

nav = open('nav.js', encoding='utf-8').read()
if MARK in nav:
    print('already done'); sys.exit(0)

# --- 1. current static prices per racket, from the EN shop --------------------------------
shop = open('shop.html', encoding='utf-8').read()
PRICE = {m.group(2): int(m.group(1)) for m in re.finditer(r"price:(\d+),racketModel:'([^']+)'", shop)}
assert len(PRICE) >= 25, len(PRICE)

def bump_card(block, slug):
    o, n = PRICE[slug], PRICE[slug] + PLUS
    assert block.count('racket-price">%d' % o) == 1 and block.count('price:%d' % o) == 1, (slug, o)
    return block.replace('racket-price">%d' % o, 'racket-price">%d' % n).replace('price:%d' % o, 'price:%d' % n)

changed = 0
html = sorted(glob.glob('**/*.html', recursive=True))
for f in html:
    s = o0 = open(f, encoding='utf-8').read()
    # texts
    for a, b in TEXT: s = s.replace(a, b)
    # nav.js version
    s = re.sub(r'nav\.js\?v=(\d+)', lambda m: 'nav.js?v=%d' % (int(m.group(1)) + 1), s)
    name = f.split('/')[-1]
    if name == 'shop.html':
        for slug in PRICE:
            i = s.index("racketModel:'%s'" % slug); a = s.rfind('<div class="racket-card', 0, i); b = s.index('</button>', i)
            s = s[:a] + bump_card(s[a:b], slug) + s[b:]
    if '/rackets/' in '/' + f:
        slug = name[:-5]
        keep = {}
        def stash(m):
            k = '\x00%d\x00' % len(keep); keep[k] = m.group(0); return k
        s = re.sub(r'<a class="similar-card".*?</a>', stash, s, flags=re.S)
        if slug in PRICE:
            o, n = PRICE[slug], PRICE[slug] + PLUS
            for a, b in [('%d CHF' % o, '%d CHF' % n), ('"price": "%d"' % o, '"price": "%d"' % n), ('price:%d' % o, 'price:%d' % n), ('racket-price">%d' % o, 'racket-price">%d' % n)]:
                s = s.replace(a, b)
            s = s.replace('"shippingRate": {"@type": "MonetaryAmount", "value": 9,', '"shippingRate": {"@type": "MonetaryAmount", "value": 0,')
        for k, v in keep.items():
            m = re.search(r'href="rackets/([^"]+)\.html"', v)
            if m and m.group(1) in PRICE:
                v = v.replace('<strong>%d CHF</strong>' % PRICE[m.group(1)], '<strong>%d CHF</strong>' % (PRICE[m.group(1)] + PLUS))
            s = s.replace(k, v)
    if s != o0:
        open(f, 'w', encoding='utf-8').write(s); changed += 1

# --- 2. build tools: same texts, shipping rate 0 -------------------------------------------
for f in ['tools/build_rackets.py', 'tools/build_siux.py', 'tools/build_racket_guide.py']:
    s = o0 = open(f, encoding='utf-8').read()
    for a, b in TEXT: s = s.replace(a, b)
    s = s.replace("'shippingRate': {'@type': 'MonetaryAmount', 'value': 9,", "'shippingRate': {'@type': 'MonetaryAmount', 'value': 0,")
    s = s.replace('# Guti 28.10.2026: Versand 9 CHF (CH), Rückgabe 30 Tage', '# Guti 27.11.2026: Versand gratis (CH, im Preis inbegriffen; vorher 9 CHF), Rückgabe 30 Tage')
    if s != o0: open(f, 'w', encoding='utf-8').write(s); changed += 1

# --- 3. nav.js -----------------------------------------------------------------------------
assert 'var RA_SHIP_CHF = 9;' in nav
nav = nav.replace('var RA_SHIP_CHF = 9;', MARK + '\nvar RA_SHIP_CHF = 0;')
for lang, word in [("ship: 'Versand per Post (+' + RA_SHIP_CHF + ' CHF)'", "ship: 'Versand per Post (gratis)'"),
                   ("ship: 'Envoi par la Poste (+' + RA_SHIP_CHF + ' CHF)'", "ship: 'Envoi par la Poste (gratuit)'"),
                   ("ship: 'Shipping by post (+' + RA_SHIP_CHF + ' CHF)'", "ship: 'Shipping by post (free)'")]:
    assert lang in nav, lang
    nav = nav.replace(lang, word)
nav = nav.replace('// Rackets: Abholung oder Versand per Post (+9 CHF).', '// Rackets: Abholung oder Versand per Post (gratis, seit 27.11.2026).')
open('nav.js', 'w', encoding='utf-8').write(nav)

left = [f for f in html + ['tools/build_rackets.py', 'tools/build_siux.py', 'tools/build_racket_guide.py', 'nav.js'] if re.search(r'\b9 CHF', open(f, encoding='utf-8').read())]
print(changed + 1, 'files changed; still mention "9 CHF":', left)
