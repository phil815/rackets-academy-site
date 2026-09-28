"""Generates one product page per racket (EN/FR/DE) from the racket cards in shop.html.
Run from repo root:  python3 tools/build_rackets.py
Pages: rackets/<model>.html, fr/rackets/<model>.html, de/rackets/<model>.html"""
import re, os, json, html, glob, urllib.parse, datetime

BASE = 'https://www.racketsacademy.ch/'
WA = '41772780115'
T = {
 'en': dict(test_h='Test it first', test_p='Rent this racket for 10 CHF and play a real match with it. If you buy it, we credit the 10 CHF to the price — completely risk-free.',
            facts=['Official {brand} reseller', 'Pick up at the academy in Salgesch or Sion', 'Test for 10 CHF — credited when you buy'],
            test_btn='Book a test on WhatsApp', back='← Back to shop', wa="Hola! I'd like to test the {label}.",
            suffix=' – test & buy', similar='You might also like', brand_suffix=' | Rackets Academy', pickup='Pick up in Salgesch or Sion',
            meta='{label} for {price} CHF at Rackets Academy in Valais. Test it for 10 CHF first — credited when you buy. Pick up in Salgesch or Sion.'),
 'fr': dict(test_h="Teste-la d'abord", test_p="Loue cette raquette pour 10 CHF et joue un vrai match avec. Si tu l'achètes, on déduit les 10 CHF du prix — sans aucun risque.",
            facts=['Revendeur officiel {brand}', "Retrait à l'academy à Salgesch ou Sion", 'Test à 10 CHF — déduit si tu achètes'],
            test_btn='Réserver un test sur WhatsApp', back='← Retour à la boutique', wa="Hola ! J'aimerais tester la {label}.",
            suffix=' – tester & acheter', similar='Tu aimeras aussi', brand_suffix=' | Rackets Academy', pickup='Retrait à Salgesch ou Sion',
            meta="{label} à {price} CHF à la Rackets Academy en Valais. Teste-la d'abord pour 10 CHF, déduits si tu achètes. Retrait à Salgesch ou Sion."),
 'de': dict(test_h='Erst testen', test_p='Miete dieses Racket für 10 CHF und spiel damit ein echtes Match. Kaufst du es, schreiben wir dir die 10 CHF gut — ganz ohne Risiko.',
            facts=['Offizieller {brand}-Händler', 'Abholung in der Academy in Salgesch oder Sion', 'Test für 10 CHF — beim Kauf angerechnet'],
            test_btn='Test per WhatsApp buchen', back='← Zurück zum Shop', wa='Hola! Ich möchte das {label} testen.',
            suffix=' – testen & kaufen', similar='Das könnte dir auch gefallen', brand_suffix=' | Rackets Academy', pickup='Abholung in Salgesch oder Sion',
            meta='{label} für {price} CHF bei der Rackets Academy im Wallis. Erst für 10 CHF testen, beim Kauf angerechnet. Abholung in Salgesch oder Sion.'),
}
CARD_RE = re.compile(r'<div class="racket-card[^"]*">\n.*?\n      </div>\n', re.S)

def cards(shop):
    out = []
    for m in CARD_RE.finditer(shop):
        c = m.group(0)
        src = re.search(r"(?:onclick|data-onclick)=\"(openBuyModal\([^\"]+\))\"", c)
        if not src: continue
        call = src.group(1)
        model = re.search(r"racketModel:'([^']+)'", call).group(1)
        label = re.search(r"racketLabel:'([^']+)'", call).group(1)
        price = re.search(r'<span class="racket-price">(\d+)', c).group(1)
        img = re.search(r'<img class="racket-photo" src="([^"]+)"', c).group(1)
        btn = re.search(r'<button type="button" class="buy-btn"[^>]*>[^<]*</button>', c).group(0)
        out.append(dict(model=model, label=label, price=price, img=img, btn=btn, sold='sold-out' in c.split('\n')[0]))
    return out

def build(lang):
    pre = '' if lang == 'en' else lang + '/'
    shop = open(pre + 'shop.html').read()
    t = T[lang]
    head_end = shop.index('</header>') + len('</header>')
    modal_start = shop.index('<div class="buy-modal-overlay"')
    top, bottom = shop[:head_end], shop[modal_start:]
    items = cards(shop)
    os.makedirs(pre + 'rackets', exist_ok=True)
    urls = []
    for it in items:
        slug, label, price = it['model'], it['label'].replace(' — ', ' '), it['price']
        brand = label.split(' ')[0]
        url = BASE + pre + 'rackets/' + slug + '.html'
        title = label + t['suffix']
        if len(title + t['brand_suffix']) <= 60: title += t['brand_suffix']
        meta = t['meta'].format(label=label, price=price)
        img_rel = it['img']                                   # relative to the shop page dir (base href)
        img_abs = BASE + ('' if lang == 'en' else '') + re.sub(r'^(\.\./)+', '', img_rel).split('?')[0]
        page_top = top
        page_top = re.sub(r'<title>.*?</title>', '<title>' + html.escape(title, quote=False) + '</title>', page_top, flags=re.S)
        page_top = re.sub(r'<meta name="description" content="[^"]*"', '<meta name="description" content="' + html.escape(meta) + '"', page_top)
        page_top = re.sub(r'<link rel="canonical" href="[^"]*"', '<link rel="canonical" href="' + url + '"', page_top)
        page_top = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + html.escape(title) + '"', page_top)
        page_top = re.sub(r'<meta property="og:description" content="[^"]*"', '<meta property="og:description" content="' + html.escape(meta) + '"', page_top)
        page_top = re.sub(r'<meta property="og:url" content="[^"]*"', '<meta property="og:url" content="' + url + '"', page_top)
        page_top = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="' + img_abs + '"', page_top)
        page_top = re.sub(r'<meta property="og:type" content="[^"]*"', '<meta property="og:type" content="product"', page_top)
        for l in ['en', 'fr', 'de', 'x-default']:
            lp = '' if l in ('en', 'x-default') else l + '/'
            page_top = re.sub(r'<link rel="alternate" hreflang="' + l + '" href="[^"]*"', '<link rel="alternate" hreflang="' + l + '" href="' + BASE + lp + 'rackets/' + slug + '.html"', page_top)
        # base href so all relative links behave like on the shop page
        page_top = page_top.replace('<head>\n', '<head>\n<base href="../">\n', 1)
        page_top = page_top.replace("location.replace(n+'/'+p", "location.replace(n+'/rackets/'+p")
        # language switcher -> same racket in other languages
        page_top = re.sub(r'(<div class="lang-menu">)(.*?)(</div>)',
                          lambda m: m.group(1) + m.group(2).replace('href="#"', 'href="rackets/' + slug + '.html"').replace('shop.html', 'rackets/' + slug + '.html') + m.group(3),
                          page_top, flags=re.S)
        ld = {'@context': 'https://schema.org', '@type': 'Product', 'name': label, 'sku': slug,
              'brand': {'@type': 'Brand', 'name': brand}, 'image': img_abs, 'description': meta,
              'offers': {'@type': 'Offer', 'price': price, 'priceCurrency': 'CHF', 'url': url,
                         'availability': 'https://schema.org/' + ('OutOfStock' if it['sold'] else 'InStock'),
                         'itemCondition': 'https://schema.org/NewCondition',
                         'seller': {'@type': 'Organization', 'name': 'Rackets Academy'}}}
        page_top = page_top.replace('</head>', '<script type="application/ld+json" id="ld-product">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
        wa = 'https://wa.me/' + WA + '?text=' + urllib.parse.quote(t['wa'].format(label=label))
        same = [x for x in items if x['model'] != slug and x['model'].split('-')[0] == slug.split('-')[0] and not x['sold']]
        other = [x for x in items if x['model'] != slug and x not in same and not x['sold']]
        pick = (same + other)[:4]
        similar = ''.join('<a class="similar-card" href="rackets/' + x['model'] + '.html"><img src="' + x['img'] + '" alt="' + html.escape(x['label'].replace(' — ', ' ')) + '" loading="lazy"><span>' + html.escape(x['label'].replace(' — ', ' ')) + '</span><strong>' + x['price'] + ' CHF</strong></a>' for x in pick)
        facts = ''.join('<li>' + html.escape(f.format(brand=brand), quote=False) + '</li>' for f in t['facts'])
        body = f'''
<section class="product-page" data-product="{slug}">
  <div class="wrap">
    <a class="product-back" href="shop.html#rackets">{t['back']}</a>
    <div class="product-grid">
      <div class="racket-card product-card{' sold-out' if it['sold'] else ''}">
        <img class="racket-photo" src="{img_rel}" alt="{html.escape(label)}">
      </div>
      <div class="product-info">
        <p class="product-brand">{html.escape(brand)}</p>
        <h1>{html.escape(label)}</h1>
        <div class="racket-card product-buy{' sold-out' if it['sold'] else ''}">
          <span class="racket-price">{price} CHF</span>
          <span class="product-pickup">{t['pickup']}</span>
          {it['btn']}
        </div>
        <div class="product-test">
          <h2>{t['test_h']}</h2>
          <p>{t['test_p']}</p>
          <a class="btn product-test-btn" href="{wa}" target="_blank" rel="noopener">{t['test_btn']}</a>
        </div>
        <ul class="product-facts">{facts}</ul>
      </div>
    </div>
    <h2 class="similar-title">{t['similar']}</h2>
    <div class="similar-grid">{similar}</div>
  </div>
</section>

'''
        open(pre + 'rackets/' + slug + '.html', 'w').write(page_top + body + bottom)
        urls.append(url)
    return urls, items

if __name__ == '__main__':
    all_urls = []
    for lang in ['en', 'fr', 'de']:
        u, items = build(lang)
        all_urls += u
        print(lang, len(u), 'pages')
    # sitemap: keep existing, add product pages
    sm = open('sitemap.xml').read()
    d = datetime.date.today().isoformat()
    sm = re.sub(r'\s*<url><loc>[^<]*/rackets/[^<]*</loc>.*?</url>', '', sm)
    add = ''.join(f'\n  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>' for u in all_urls)
    sm = sm.replace('\n</urlset>', add + '\n</urlset>')
    open('sitemap.xml', 'w').write(sm)
