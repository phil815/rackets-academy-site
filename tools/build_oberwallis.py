"""German-only landing page de/padel-oberwallis.html (target: Upper Valais, Salgesch)."""
import re, json, urllib.parse
PT = 'https://playtomic.com/tenant/f89dfa07-4283-453e-8be3-316f9bd060d3'
WA = 'https://wa.me/41762914369?text=' + urllib.parse.quote('Hola Philip! Ich komme aus dem Oberwallis und möchte in Salgesch spielen.')
MAPS = 'https://www.google.com/maps/dir/?api=1&destination=Littenstrasse+30+3970+Salgesch'
URL = 'https://www.racketsacademy.ch/de/padel-oberwallis.html'
TITLE = 'Padel im Oberwallis – Salgesch | Rackets Academy'
DESC = 'Das grösste Padelzentrum im Wallis: 20 Min. ab Visp, 30 Min. ab Brig. Padel, Pickleball, Tennis, Spa und Bar in Salgesch, täglich 07:00–23:30.'
FAC = [('🎾', 'Padel', '4 Plätze indoor, 2 outdoor', 'Täglich 07:00–23:30'),
       ('🏓', 'Pickleball', '4 Plätze indoor', 'Täglich 07:00–23:30'),
       ('🎾', 'Tennis', '2 Plätze indoor', 'Täglich 07:00–23:30'),
       ('🧖', 'Spa', '2 Saunen, Hammam, Whirlpool', 'Mo–Fr 14:00–22:00 · Sa–So 10:00–22:00'),
       ('🍕', 'Bar', 'Pizzas, Empanadas, Snacks und mehr', 'Mo–Fr 10:00–22:00 · Sa–So 10:00–20:00')]
MORE = [('🏆', 'Racketero-Turniere', 'Jede Woche — spiel gegen neue Leute aus dem ganzen Wallis.', 'racketero.html'),
        ('🎓', 'Training auf Deutsch', 'Einzel- oder Gruppentrainings, mit deutschsprachigen Coaches in Salgesch.', 'training.html'),
        ('🎂', 'Kindergeburtstag', '2 Stunden Padel mit Coach und Mini-Turnier, bis 12 Kinder.', 'kids-birthday.html'),
        ('💼', 'Firmenevent', 'Teamevent mit Padel, Essen und Apéro — ab 25 CHF pro Person.', 'company-events.html')]
FAQ = [('Wo kann man im Oberwallis Padel spielen?', 'In der Rackets Academy in Salgesch — dem grössten Padelzentrum im Wallis, 20 Minuten von Visp und 30 Minuten von Brig. 4 Indoor- und 2 Outdoor-Plätze, täglich 07:00–23:30.'),
       ('Brauche ich einen eigenen Schläger?', 'Nein. Für dein erstes Spiel bekommst du einen Leihschläger gratis.'),
       ('Gibt es Training auf Deutsch?', 'Ja, in Salgesch trainieren dich auch deutschsprachige Coaches — einzeln oder in der Gruppe.'),
       ('Wann ist es am günstigsten?', 'Vor 17 Uhr spielst du günstiger — ideal bei Schichtarbeit, Teilzeit oder freien Nachmittagen.')]

def body():
    fac = ''.join(f'<div class="ow-fac"><span class="co2-ic">{e}</span><div><h3>{h}</h3><p>{a}</p><p class="ow-time">{b}</p></div></div>' for e, h, a, b in FAC)
    more = ''.join(f'<a class="co2-b ow-more" href="{l}"><span class="co2-ic">{e}</span><h3>{h} →</h3><p>{p}</p></a>' for e, h, p, l in MORE)
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in FAQ)
    return f'''
<section class="spa-hero co-hero" style="background-image:url('../images/hero-poster.jpg');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">Padel im Oberwallis · Salgesch</p>
    <h1>Das grösste Padelzentrum im Wallis.</h1>
    <p class="lede">Padel, Pickleball, Tennis, Spa und Bar — und die beste Community im Wallis. Gleich um die Ecke.</p>
    <div class="spa-chips"><span class="spa-chip">🚗 20 Min. ab Visp</span><span class="spa-chip">🚗 30 Min. ab Brig</span><span class="spa-chip">Gratis Leihschläger fürs erste Spiel</span></div>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="{PT}" target="_blank" rel="noopener">Platz in Salgesch buchen</a>
      <a class="btn spa-cta-ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp an Philip</a>
    </div>
  </div>
</section>

<section class="co2-sec">
  <div class="wrap">
    <h2 class="co2-h">Alles an einem Ort</h2>
    <div class="ow-facs">{fac}</div>
  </div>
</section>

<section class="co2-sec ow-day">
  <div class="wrap co2-price">
    <p class="spa-kicker" style="color:var(--blue);">Tagsüber spielen</p>
    <h2 class="co2-h">Vor 17 Uhr günstiger.</h2>
    <p>Schichtarbeit, Teilzeit oder freier Nachmittag? Vor 17 Uhr spielst du günstiger — und die Plätze sind frei.</p>
    <a class="btn btn-green spa-cta" href="{PT}" target="_blank" rel="noopener">Freie Plätze ansehen</a>
  </div>
</section>

<section class="co2-sec">
  <div class="wrap">
    <h2 class="co2-h">Mehr als nur spielen</h2>
    <div class="co2-bens ow-mores">{more}</div>
  </div>
</section>

<section class="co2-sec co2-proof">
  <div class="wrap">
    <h2 class="co2-h">So kommst du hin</h2>
    <div class="spa-near"><div class="spa-near-item"><strong>Visp</strong><span>≈ 20 Min.</span></div><div class="spa-near-item"><strong>Brig</strong><span>≈ 30 Min.</span></div><div class="spa-near-item"><strong>Siders</strong><span>≈ 5 Min.</span></div><div class="spa-near-item"><strong>Sitten</strong><span>≈ 18 Min.</span></div></div>
    <p class="ow-addr">📍 Littenstrasse 30, 3970 Salgesch · <a href="{MAPS}" target="_blank" rel="noopener">Route planen →</a></p>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>Gut zu wissen</h2>
    <div class="spa-faq">{faq}</div>
  </div>
</section>

<section class="spa-final" style="background-image:url('../images/coaching/coaching-6.jpg');">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-final-inner">
    <h2>Dein erstes Spiel? Der Schläger geht auf uns.</h2>
    <p>Buch auf Playtomic oder schreib Philip: +41 76 291 43 69</p>
    <div class="hero-actions" style="justify-content:center;">
      <a class="btn btn-green spa-cta" href="{PT}" target="_blank" rel="noopener">Platz buchen</a>
      <a class="btn spa-cta-ghost" href="{WA}" target="_blank" rel="noopener">WhatsApp an Philip</a>
    </div>
  </div>
</section>

'''

s = open('de/spa-and-sauna.html').read()
a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
b = s.index('<footer')
s = s[:a] + body() + s[b:]
s = re.sub(r'<link rel="alternate" hreflang="[^"]*" href="[^"]*">\n', '', s)
s = re.sub(r'<link rel="canonical" href="[^"]*"', '<link rel="canonical" href="' + URL + '"', s)
s = re.sub(r'<meta property="og:url" content="[^"]*"', '<meta property="og:url" content="' + URL + '"', s)
s = s.replace('<div class="lang-menu"><a href="../spa-and-sauna.html">English</a><a href="#">Deutsch</a><a href="../fr/spa-and-sauna.html">Français</a></div>',
              '<div class="lang-menu"><a href="../index.html">English</a><a href="#">Deutsch</a><a href="../fr/index.html">Français</a></div>')
s = s.replace("location.replace(n+'/'+p", "location.replace(n+'/'+'index.html'")
s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
s = re.sub(r'<title>.*?</title>', '<title>' + TITLE + '</title>', s, count=1, flags=re.S)
for k in ['name="description"', 'property="og:description"']:
    s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + DESC + '"', s)
s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + TITLE + '"', s)
s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="https://www.racketsacademy.ch/images/hero-poster.jpg"', s)
ld = {'@context': 'https://schema.org', '@graph': [
  {'@type': 'SportsActivityLocation', 'name': 'Rackets Academy Salgesch', 'url': URL, 'telephone': '+41762914369',
   'image': 'https://www.racketsacademy.ch/images/hero-poster.jpg',
   'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressRegion': 'VS', 'addressCountry': 'CH'},
   'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'], 'opens': '07:00', 'closes': '23:30'}],
   'areaServed': ['Oberwallis', 'Salgesch', 'Leuk', 'Susten', 'Turtmann', 'Gampel-Bratsch', 'Steg-Hohtenn', 'Raron', 'Visp', 'Brig-Glis', 'Naters', 'Leukerbad', 'Siders']},
  {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]}]}
s = s.replace('</head>', '<script type="application/ld+json" id="ld-ow">' + json.dumps(ld, ensure_ascii=False) + '</script>\n</head>', 1)
s = s.replace('class="active"', '')
s = s.replace('<html lang="de"', '<html lang="de-CH"') if False else s
open('de/padel-oberwallis.html', 'w').write(s)
print('ok', len(TITLE), len(DESC))
