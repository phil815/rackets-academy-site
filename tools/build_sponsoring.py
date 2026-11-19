"""Seite «Sponsor werden» (sponsoring.html, EN/FR/DE). Phil 19.11.2026: keine Preise, kein Rabatt-Prozentsatz,
Kontakt nur per E-Mail an Phil; Ziel einer Partnerschaft ist Win-win und den Sport voranbringen;
lokal verankert, national agierend; Partnerlogos prominent als Beleg. Inhalte aus dem Sponsoring-Deck (Drive).
Hülle = company-events.html der jeweiligen Sprache. Danach:  python3 tools/ux_nav.py"""
import re, json
MAIL = 'mailto:phil@racketsacademy.ch?subject=Sponsoring%20Rackets%20Academy'
T = {
 'de': dict(pre='de/', title='Sponsor werden – Partner der Rackets Academy im Wallis', desc='Werde Partner der Rackets Academy: Sichtbarkeit auf den Plätzen in Salgesch und Sion, eigener Event, Vorteile für dein Team. Lokal verankert, national agierend. Schreib Phil eine E-Mail.',
   kicker='Partnerschaft · Salgesch &amp; Sion', h1='Werde Sponsor der Rackets Academy', lede='Padel wächst im Wallis rasant. Wir suchen Partner, die den Sport mit uns voranbringen wollen, und zwar so, dass beide Seiten gewinnen.',
   cta='Schreib Phil eine E-Mail', cta2='Was du bekommst', logos_h='Diese Marken sind schon Partner', why_h='Worum es uns geht',
   why=[('🤝','Win-win','Eine Partnerschaft muss sich für dich lohnen. Wir schauen gemeinsam, was zu deiner Firma passt, statt ein fixes Paket zu verkaufen.'),
        ('🎾','Den Sport voranbringen','Mit unseren Partnern machen wir Padel und Pickleball gross: Kurse für Kinder, Turniere, Events und Plätze für alle.'),
        ('📍','Lokal verankert, national agierend','Zuhause in Salgesch und Sion, mit dem Ziel, in der ganzen Schweiz zu wachsen. Lokale Firmen und globale Marken sind schon dabei.')],
   ben_h='Was Partner bei uns bekommen', ben_p='Je nach Partnerschaft, immer auf dich zugeschnitten.',
   ben=[('🏟️','Dein Name auf dem Platz','Dein Logo auf den Glaswänden, und der Platz trägt deinen Namen in der Buchungs-App.'),
        ('📺','Sichtbarkeit vor Ort und online','Logo auf unserem LED-Screen, auf der Website und auf den Turnierplakaten.'),
        ('🎉','Dein eigener Event','Ein Event pro Jahr unter deinem Namen, und unsere Anlage für deinen Firmenanlass: Plätze, Bar, Sitzungsraum, Terrasse.'),
        ('📱','Beiträge auf Social Media','Wir zeigen die Partnerschaft regelmässig auf unseren Kanälen.'),
        ('👥','Vorteile für dein Team','Rabatt für deine Mitarbeitenden auf Plätze, Kurse, Camps und Spa.')],
   end_h='Lass uns reden', end_p='Schreib Phil, was du dir vorstellst. Er meldet sich persönlich bei dir.'),
 'fr': dict(pre='fr/', title='Devenir sponsor – partenaire de la Rackets Academy en Valais', desc='Deviens partenaire de la Rackets Academy : visibilité sur les terrains de Salgesch et Sion, ton propre événement, avantages pour ton équipe. Ancrés localement, actifs au niveau national. Écris à Phil.',
   kicker='Partenariat · Salgesch &amp; Sion', h1='Deviens sponsor de la Rackets Academy', lede='Le padel grandit très vite en Valais. Nous cherchons des partenaires qui veulent faire avancer ce sport avec nous, de façon à ce que chacun y gagne.',
   cta='Écrire un e-mail à Phil', cta2='Ce que tu obtiens', logos_h='Ces marques sont déjà partenaires', why_h='Ce qui compte pour nous',
   why=[('🤝','Gagnant-gagnant','Un partenariat doit être intéressant pour toi. Nous regardons ensemble ce qui convient à ton entreprise, plutôt que de vendre un paquet fixe.'),
        ('🎾','Faire avancer le sport','Avec nos partenaires, nous développons le padel et le pickleball : cours pour enfants, tournois, événements et terrains pour tous.'),
        ('📍','Ancrés localement, actifs au niveau national','Chez nous à Salgesch et à Sion, avec l’objectif de grandir dans toute la Suisse. Des entreprises locales et des marques mondiales sont déjà de la partie.')],
   ben_h='Ce que nos partenaires obtiennent', ben_p='Selon le partenariat, toujours sur mesure.',
   ben=[('🏟️','Ton nom sur le terrain','Ton logo sur les vitres, et le terrain porte ton nom dans l’application de réservation.'),
        ('📺','Visibilité sur place et en ligne','Logo sur notre écran LED, sur le site web et sur les affiches des tournois.'),
        ('🎉','Ton propre événement','Un événement par an à ton nom, et nos installations pour ta sortie d’entreprise : terrains, bar, salle de conférence, terrasse.'),
        ('📱','Publications sur les réseaux','Nous montrons régulièrement le partenariat sur nos canaux.'),
        ('👥','Avantages pour ton équipe','Rabais pour tes collaborateurs sur les terrains, les cours, les camps et le spa.')],
   end_h='Parlons-en', end_p='Écris à Phil ce que tu imagines. Il te répond personnellement.'),
 'en': dict(pre='', title='Become a sponsor – partner of Rackets Academy in Valais', desc='Become a partner of Rackets Academy: visibility on the courts in Salgesch and Sion, your own event, benefits for your team. Locally rooted, active nationwide. Email Phil.',
   kicker='Partnership · Salgesch &amp; Sion', h1='Become a sponsor of Rackets Academy', lede='Padel is growing fast in Valais. We are looking for partners who want to move the sport forward with us, in a way that works for both sides.',
   cta='Email Phil', cta2='What you get', logos_h='These brands are already partners', why_h='What matters to us',
   why=[('🤝','Win-win','A partnership has to pay off for you. We work out together what fits your company instead of selling a fixed package.'),
        ('🎾','Moving the sport forward','With our partners we grow padel and pickleball: kids’ courses, tournaments, events and courts for everyone.'),
        ('📍','Locally rooted, active nationwide','At home in Salgesch and Sion, with the goal of growing across Switzerland. Local companies and global brands are already on board.')],
   ben_h='What partners get', ben_p='Depending on the partnership, always tailored to you.',
   ben=[('🏟️','Your name on the court','Your logo on the glass walls, and the court carries your name in the booking app.'),
        ('📺','Visibility on site and online','Logo on our LED screen, on the website and on tournament posters.'),
        ('🎉','Your own event','One event a year under your name, and our venue for your company day: courts, bar, meeting room, terrace.'),
        ('📱','Social media posts','We feature the partnership regularly on our channels.'),
        ('👥','Benefits for your team','A discount for your employees on courts, courses, camps and spa.')],
   end_h='Let’s talk', end_p='Tell Phil what you have in mind. He will get back to you personally.'),
}
def cards(items): return ''.join(f'<div class="co2-b"><span class="co2-ic">{i}</span><h3>{h}</h3><p>{p}</p></div>' for i, h, p in items)
for L, t in T.items():
    pre = t['pre']; up = '../' if pre else ''
    s = open(pre + 'company-events.html', encoding='utf-8').read()
    track = re.search(r'<div class="sponsor-track">(.*?)</div>', s, flags=re.S).group(1)
    logos, seen = [], set()
    for m in re.finditer(r'<a href="([^"]+)"[^>]*><img src="([^"]+)" alt="([^"]+)"[^>]*></a>', track):
        if m.group(3) not in seen:
            seen.add(m.group(3)); logos.append(f'<a href="{m.group(1)}" target="_blank" rel="noopener"><img src="{m.group(2)}" alt="{m.group(3)}" loading="lazy"></a>')
    # Red Bull: Logo-Datei fehlt noch im Repo (images/partners/red-bull-white.png) → bis dahin als Schriftzug
    logos.append('<a href="https://www.redbull.com/ch-de/" target="_blank" rel="noopener" class="sp-word">Red Bull</a>')
    body = f'''<section class="spa-hero co-hero" style="background-image:url('{up}images/photos/events-group.webp'); background-position:center 40%;">
  <div class="spa-hero-shade"></div>
  <div class="wrap spa-hero-inner">
    <p class="spa-kicker">{t['kicker']}</p>
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="hero-actions">
      <a class="btn btn-green spa-cta" href="{MAIL}">{t['cta']}</a>
      <a class="btn spa-cta-ghost" href="#benefits">{t['cta2']}</a>
    </div>
  </div>
</section>

<section class="sp-logos-sec">
  <div class="wrap">
    <h2 class="sp-logos-h">{t['logos_h']}</h2>
    <div class="sp-logos">{''.join(logos)}</div>
  </div>
</section>

<section class="co2-sec">
  <div class="wrap">
    <h2 class="co2-h">{t['why_h']}</h2>
    <div class="co2-bens ev-mods">{cards(t['why'])}</div>
  </div>
</section>

<section class="co2-sec co2-proof" id="benefits">
  <div class="wrap">
    <h2 class="co2-h">{t['ben_h']}</h2>
    <p class="kc-sub">{t['ben_p']}</p>
    <div class="co2-bens ev-mods">{cards(t['ben'])}</div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap" style="text-align:center;">
    <h2>{t['end_h']}</h2>
    <p class="section-lede" style="margin-left:auto; margin-right:auto;">{t['end_p']}</p>
    <p><a class="btn btn-green" href="{MAIL}">phil@racketsacademy.ch</a></p>
  </div>
</section>

'''
    a, b = s.index('<section class="spa-hero co-hero"'), s.index('<footer>')
    s = s[:a] + body + s[b:]
    s = s.replace('company-events.html', 'sponsoring.html')
    s = s.replace('<a href="sponsoring.html" class="active">', '<a href="company-events.html" class="active">').replace('<a href="sponsoring.html">', '<a href="company-events.html">')
    esc = lambda x: x.replace('&', '&amp;').replace('"', '&quot;')
    s = re.sub(r'<title>.*?</title>', '<title>' + t['title'] + ' | Rackets Academy</title>', s, count=1, flags=re.S)
    s = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + esc(t['desc']), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + esc(t['title']) + ' | Rackets Academy', s, count=1)
    s = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + esc(t['desc']), s, count=1)
    s = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\1https://www.racketsacademy.ch/images/photos/events-group.jpg', s, count=1)
    s = re.sub(r'<script type="application/ld\+json"[^>]*>.*?</script>\n?', '', s, flags=re.S)
    open(pre + 'sponsoring.html', 'w', encoding='utf-8').write(s)
    print(pre + 'sponsoring.html', len(s))
