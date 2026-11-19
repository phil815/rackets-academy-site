#!/usr/bin/env python3
"""Mitgliedschafts-Seite rackets-plus.html (EN/DE/FR) neu: Nutzen zuerst, 3 Schritte, Status-Tabelle, Prämien, FAQ mit Schema.
Fakten aus ra-crm docs/wissen/MARIA.md (Level ab 4/7/10 Besuchstagen im Vormonat, Goodies, Punkte verfallen nicht, STOP/START).
Idempotent: ersetzt Kopfzeilen (title, description, og) und alles zwischen Hero und Footer."""
import pathlib, re, json, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
WA = 'https://tinyurl.com/RA-Plus'
IMG = 'https://www.racketsacademy.ch/images/'

T = {
 '': dict(
  title='Padel membership in Valais – free, with rewards | RACKETS+',
  desc='RACKETS+ is the free membership of Rackets Academy in Salgesch and Sion: collect points with every booking, get free water, balls and tournaments, and redeem rackets or lessons. All on WhatsApp.',
  h1='Padel membership in Valais: free, with rewards', lede='Play at Rackets Academy and get something back every time. Play 4 days in a month and you get free water at every visit, a drinking bottle and a can of balls every month.',
  cta='Join free on WhatsApp', facts=['Free', 'No app, no account', 'Start in 1 minute'],
  top_h='Play. Collect. Treat yourself.', top=[('Racket', 'Worth 200 CHF. You pick the model.'), ('Private lesson', 'One hour with one of our coaches.'), ('Spa session', 'Sauna and jacuzzi after the match.')],
  how_h='How it works', how=[('Say «Hola» to María', 'Write to our WhatsApp bot. She signs you up in a minute and sends your member card.'), ('Play as usual', 'Every booking in Playtomic gives you points, automatically. Nothing to scan.'), ('Collect your rewards', 'Send María the number of the reward you want and pick it up at the bar.')],
  st_h='Benefits by status', st_p='The more often you play, the better your goodies.', entry='the start', from_='from {n} visit days', entry_s='start', from_s='{n}+ days',
  rows=['Collect points with every booking', 'Redeem points', 'Free water at every visit', 'RACKETS+ drinking bottle (once)', '1 can of balls per month', '2 overgrips per month', '1 free tournament per month'],
  st_note='<strong>Your status follows the days you played in a month</strong> and stays with you for the whole next month. So a quiet month costs you nothing.',
  yes='included', no='not included',
  card_h='Your card, in your wallet', card_p='Every member gets a digital member card for Apple Wallet or Google Wallet. It shows your points and status live and is always on your phone.',
  card_alt='Digital RACKETS+ member cards for Apple Wallet and Google Wallet in the four status levels',
  earn_h='How you collect points', earn=['Every booking with us: court, class, tournament, spa', 'First class and first tournament: <strong>+25</strong> each (once)', 'Your birthday: <strong>+25</strong>', 'Bring a friend: <strong>+50</strong> for both of you'],
  rew_h='What your points get you', rew_p='Send María the number of the reward you want.', rew_th=('Reward', 'Points'), swipe='↔ Swipe for all rewards',
  rew=[('Sticker', '', '5'), ('Drink', '', '20'), ('Spa session', '', '80'), ('Playtomic tournament entry', '', '100'), ('Swiss Tennis tournament', '(worth 45 CHF)', '150'), ('Spot in a group class', '', '200'), ('T-shirt', '', '250'), ('Shorts', '', '350'), ('Private lesson before 5 pm', '', '750'), ('Racket', '(worth 200 CHF)', '1’250')],
  faq_h='Questions about the membership', faq=[
   ('What does RACKETS+ cost?', 'Nothing. The membership is free. All you need is WhatsApp.'),
   ('Do I need an app?', 'No. Everything runs in WhatsApp with María, our bot. Your member card sits in Apple Wallet or Google Wallet.'),
   ('How do I collect points?', 'Automatically with every booking you make with us in Playtomic: court, class, tournament or spa. On top there are bonus points for your first class, your first tournament, your birthday and for friends you bring.'),
   ('Do my points expire?', 'No. Your points stay as long as you are a member.'),
   ('How is my status calculated?', 'By the number of days you played in a calendar month: from 4 days Challenger, from 7 Master, from 10 Legend. The status then applies for the whole following month.'),
   ('How do I leave?', 'Send STOP to María and you get no more messages. With START you are back, and your points are still there.')],
  end_h='Ready? Say «Hola» to María', end_p='She takes care of the rest.', end_cta='Write on WhatsApp'),
 'de/': dict(
  title='Padel-Mitgliedschaft im Wallis – gratis, mit Prämien | RACKETS+',
  desc='RACKETS+ ist die kostenlose Mitgliedschaft der Rackets Academy in Salgesch und Sion: Punkte bei jeder Buchung, gratis Wasser, Bälle und Turniere, Rackets oder Lektionen als Prämie. Alles über WhatsApp.',
  h1='Padel-Mitgliedschaft im Wallis: gratis, mit Prämien', lede='Spiel bei der Rackets Academy und bekomm jedes Mal etwas zurück. Spielst du an 4 Tagen im Monat, gibt es gratis Wasser bei jedem Besuch, eine Trinkflasche und jeden Monat eine Dose Bälle.',
  cta='Gratis per WhatsApp beitreten', facts=['Kostenlos', 'Keine App, kein Konto', 'In 1 Minute dabei'],
  top_h='Spielen. Sammeln. Gönnen.', top=[('Racket', 'Im Wert von 200 CHF. Du wählst das Modell.'), ('Privatstunde', 'Eine Stunde mit einem unserer Coaches.'), ('Spa-Session', 'Sauna und Jacuzzi nach dem Match.')],
  how_h='So funktioniert es', how=[('Sag «Hola» zu María', 'Schreib unserem WhatsApp-Bot. Sie meldet dich in einer Minute an und schickt dir deine Mitgliedskarte.'), ('Spiel wie immer', 'Jede Buchung in Playtomic bringt dir automatisch Punkte. Du musst nichts scannen.'), ('Hol dir deine Prämien', 'Schick María die Nummer der Prämie und hol sie an der Bar ab.')],
  st_h='Vorteile nach Status', st_p='Je öfter du spielst, desto besser deine Goodies.', entry='der Einstieg', from_='ab {n} Besuchstagen', entry_s='Start', from_s='{n}+ Tage',
  rows=['Punkte sammeln bei jeder Buchung', 'Punkte einlösen', 'Wasser gratis bei jedem Besuch', 'RACKETS+ Trinkflasche (einmalig)', '1 Dose Bälle pro Monat', '2 Griffbänder pro Monat', '1 Gratis-Turnier pro Monat'],
  st_note='<strong>Dein Status richtet sich nach deinen Besuchstagen im Monat</strong> und bleibt dir den ganzen Folgemonat erhalten. Ein ruhiger Monat kostet dich also nichts.',
  yes='inbegriffen', no='nicht inbegriffen',
  card_h='Deine Karte, in deinem Wallet', card_p='Jedes Mitglied bekommt eine digitale Mitgliedskarte für Apple Wallet oder Google Wallet. Sie zeigt Punkte und Status live und ist immer auf deinem Handy.',
  card_alt='Digitale RACKETS+ Mitgliedskarten für Apple Wallet und Google Wallet in den vier Status-Stufen',
  earn_h='So sammelst du Punkte', earn=['Jede Buchung bei uns: Platz, Kurs, Turnier, Spa', 'Erster Kurs und erstes Turnier: je <strong>+25</strong> (einmalig)', 'Dein Geburtstag: <strong>+25</strong>', 'Freunde werben: <strong>+50</strong> für euch beide'],
  rew_h='Das bekommst du für deine Punkte', rew_p='Schick María die Nummer der Prämie, die du willst.', rew_th=('Prämie', 'Punkte'), swipe='↔ Wischen für alle Prämien',
  rew=[('Sticker', '', '5'), ('Getränk', '', '20'), ('Spa-Session', '', '80'), ('Playtomic-Turnier-Teilnahme', '', '100'), ('Swiss Tennis Turnier', '(Wert 45 CHF)', '150'), ('Platz im Gruppenkurs', '', '200'), ('T-Shirt', '', '250'), ('Hose', '', '350'), ('Privatstunde vor 17 Uhr', '', '750'), ('Racket', '(Wert 200 CHF)', '1’250')],
  faq_h='Fragen zur Mitgliedschaft', faq=[
   ('Was kostet RACKETS+?', 'Nichts. Die Mitgliedschaft ist kostenlos. Du brauchst nur WhatsApp.'),
   ('Brauche ich eine App?', 'Nein. Alles läuft in WhatsApp mit María, unserem Bot. Deine Mitgliedskarte liegt im Apple Wallet oder Google Wallet.'),
   ('Wie sammle ich Punkte?', 'Automatisch mit jeder Buchung bei uns in Playtomic: Platz, Kurs, Turnier oder Spa. Dazu kommen Bonuspunkte für den ersten Kurs, das erste Turnier, deinen Geburtstag und für geworbene Freunde.'),
   ('Verfallen meine Punkte?', 'Nein. Deine Punkte bleiben, solange du Mitglied bist.'),
   ('Wie wird mein Status berechnet?', 'Nach der Zahl der Tage, an denen du in einem Kalendermonat gespielt hast: ab 4 Tagen Challenger, ab 7 Master, ab 10 Legend. Der Status gilt dann den ganzen folgenden Monat.'),
   ('Wie melde ich mich ab?', 'Schick María das Wort STOP, dann bekommst du keine Nachrichten mehr. Mit START bist du wieder dabei, deine Punkte bleiben.')],
  end_h='Bereit? Sag «Hola» zu María', end_p='Den Rest übernimmt sie.', end_cta='Auf WhatsApp schreiben'),
 'fr/': dict(
  title='Carte membre padel en Valais – gratuite, avec récompenses | RACKETS+',
  desc='RACKETS+ est la carte membre gratuite de la Rackets Academy à Salgesch et Sion : des points à chaque réservation, de l’eau, des balles et des tournois offerts, raquettes ou cours en récompense. Tout sur WhatsApp.',
  h1='Carte membre padel en Valais : gratuite, avec récompenses', lede='Joue à la Rackets Academy et reçois quelque chose à chaque fois. Joue 4 jours dans le mois et tu as de l’eau gratuite à chaque visite, une gourde et une boîte de balles chaque mois.',
  cta='Rejoindre gratuitement sur WhatsApp', facts=['Gratuit', 'Pas d’app, pas de compte', 'Inscrit en 1 minute'],
  top_h='Joue. Cumule. Fais-toi plaisir.', top=[('Raquette', 'D’une valeur de 200 CHF. Tu choisis le modèle.'), ('Cours privé', 'Une heure avec un de nos coachs.'), ('Session spa', 'Sauna et jacuzzi après le match.')],
  how_h='Comment ça marche', how=[('Dis «Hola» à María', 'Écris à notre bot WhatsApp. Elle t’inscrit en une minute et t’envoie ta carte membre.'), ('Joue comme d’habitude', 'Chaque réservation sur Playtomic te donne des points, automatiquement. Rien à scanner.'), ('Récupère tes récompenses', 'Envoie à María le numéro de la récompense et passe la prendre au bar.')],
  st_h='Avantages par statut', st_p='Plus tu joues, meilleurs sont tes goodies.', entry='le début', from_='dès {n} jours de visite', entry_s='début', from_s='{n}+ jours',
  rows=['Des points à chaque réservation', 'Échanger ses points', 'Eau gratuite à chaque visite', 'Gourde RACKETS+ (une fois)', '1 boîte de balles par mois', '2 surgrips par mois', '1 tournoi gratuit par mois'],
  st_note='<strong>Ton statut dépend de tes jours de visite dans le mois</strong> et tu le gardes tout le mois suivant. Un mois calme ne te coûte donc rien.',
  yes='inclus', no='non inclus',
  card_h='Ta carte, dans ton wallet', card_p='Chaque membre reçoit une carte membre numérique pour Apple Wallet ou Google Wallet. Elle affiche tes points et ton statut en direct, toujours sur ton téléphone.',
  card_alt='Cartes membre numériques RACKETS+ pour Apple Wallet et Google Wallet dans les quatre statuts',
  earn_h='Comment gagner des points', earn=['Chaque réservation chez nous : court, cours, tournoi, spa', 'Premier cours et premier tournoi : <strong>+25</strong> chacun (une fois)', 'Ton anniversaire : <strong>+25</strong>', 'Parraine un ami : <strong>+50</strong> pour vous deux'],
  rew_h='Ce que valent tes points', rew_p='Envoie à María le numéro de la récompense que tu veux.', rew_th=('Récompense', 'Points'), swipe='↔ Glisse pour tout voir',
  rew=[('Sticker', '', '5'), ('Boisson', '', '20'), ('Session spa', '', '80'), ('Participation à un tournoi Playtomic', '', '100'), ('Tournoi Swiss Tennis', '(valeur 45 CHF)', '150'), ('Place en cours collectif', '', '200'), ('T-shirt', '', '250'), ('Short', '', '350'), ('Cours privé avant 17 h', '', '750'), ('Raquette', '(valeur 200 CHF)', '1’250')],
  faq_h='Questions sur la carte membre', faq=[
   ('Combien coûte RACKETS+ ?', 'Rien. La carte membre est gratuite. Il te faut seulement WhatsApp.'),
   ('Faut-il une application ?', 'Non. Tout se passe sur WhatsApp avec María, notre bot. Ta carte membre est dans Apple Wallet ou Google Wallet.'),
   ('Comment gagner des points ?', 'Automatiquement à chaque réservation chez nous sur Playtomic : court, cours, tournoi ou spa. S’y ajoutent des points bonus pour ton premier cours, ton premier tournoi, ton anniversaire et les amis que tu parraines.'),
   ('Mes points expirent-ils ?', 'Non. Tes points restent tant que tu es membre.'),
   ('Comment est calculé mon statut ?', 'Selon le nombre de jours où tu as joué dans un mois civil : dès 4 jours Challenger, dès 7 Master, dès 10 Legend. Le statut vaut ensuite pour tout le mois suivant.'),
   ('Comment me désinscrire ?', 'Envoie STOP à María et tu ne reçois plus de messages. Avec START tu reviens, et tes points sont toujours là.')],
  end_h='Prêt ? Dis «Hola» à María', end_p='Elle s’occupe du reste.', end_cta='Écrire sur WhatsApp'),
}
TIERS = [('Member', 0, 'mb', 0), ('Challenger', 1, 'ch', 4), ('Master', 2, 'ms', 7), ('Legend', 3, 'lg', 10)]
FROM = [0, 0, 1, 1, 1, 2, 3]   # row i is included from tier index FROM[i]
TOPIMG = [IMG + 'rackets/wilson-bela-v3.jpg', IMG + 'photos/training-player.webp', IMG + 'spa/spa-jacuzzi.webp']
PTS = ['1’250', '750', '80']
HERO = IMG + 'photos/events-group.webp'

def body(t, rel):
    e = html.escape
    head = ''.join(f'<div class="pt-h pt-{c}" role="columnheader"><b>{n}</b><span class="pt-stars" aria-hidden="true">{"★" * s}</span><small><span class="pt-full">{t["entry"] if not d else t["from_"].format(n=d)}</span><span class="pt-short">{t["entry_s"] if not d else t["from_s"].format(n=d)}</span></small></div>' for n, s, c, d in TIERS)
    rows = ''
    for i, r in enumerate(t['rows']):
        cells = ''.join(f'<div class="pt-c" role="cell"><i class="pt-dot pt-{c}{"" if s >= FROM[i] else " off"}" role="img" aria-label="{t["yes"] if s >= FROM[i] else t["no"]}"></i></div>' for n, s, c, d in TIERS)
        rows += f'<div class="pt-r" role="row"><div class="pt-l" role="rowheader">{r}</div>{cells}</div>'
    top = ''.join(f'<div class="plus-tile{" plus-tile-prod" if i == 0 else ""}"><img src="{TOPIMG[i].format(rel=rel)}" alt="{e(h)}" loading="lazy"><span class="plus-pts">{PTS[i]} {t["rew_th"][1]}</span><div class="plus-tile-t"><h3>{h}</h3><p>{p}</p></div></div>' for i, (h, p) in enumerate(t['top']))
    how = ''.join(f'<li><b>{h}</b><span>{p}</span></li>' for h, p in t['how'])
    rew = ''.join(f'<tr><td class="lead">{i + 1}. {n}{" <span class=sub>" + s + "</span>" if s else ""}</td><td>{p} 🟢</td></tr>' for i, (n, s, p) in enumerate(t['rew'])).replace('class=sub', 'class="sub"')
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    ld = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}, ensure_ascii=False)
    return f'''<section class="hero plus-hero" style="background-image:linear-gradient(100deg, rgba(4,60,130,.94) 0%, rgba(0,105,205,.86) 45%, rgba(0,119,222,.45) 100%), url('{HERO}'); background-size:cover; background-position:center 35%;">
  <div class="wrap hero-inner">
    <h1><span class="plus-brand">Rackets<i>+</i></span><span class="plus-h1sub">{t['h1']}</span></h1>
    <p class="lede">{t['lede']}</p>
    <div class="hero-actions">
      <a class="btn btn-green" href="{WA}" target="_blank" rel="noopener">{t['cta']}</a>
    </div>
    <ul class="plus-facts">{''.join(f'<li>{x}</li>' for x in t['facts'])}</ul>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['top_h']}</h2>
    <div class="plus-tiles">{top}</div>
  </div>
</section>

<section class="section-tight" style="background:var(--paper);">
  <div class="wrap">
    <h2>{t['how_h']}</h2>
    <ol class="plus-steps">{how}</ol>
  </div>
</section>

<section class="section-tight" id="status">
  <div class="wrap">
    <h2>{t['st_h']}</h2>
    <p class="section-lede">{t['st_p']}</p>
    <div class="pt" role="table" aria-label="{e(t['st_h'])}">
      <div class="pt-r pt-head" role="row"><div class="pt-l" role="columnheader"></div>{head}</div>
      {rows}
    </div>
    <p class="pt-note">{t['st_note']}</p>
  </div>
</section>

<section class="section-tight" style="background:var(--paper);">
  <div class="wrap grid-2" style="align-items:center;">
    <div>
      <h2>{t['card_h']}</h2>
      <p class="section-lede" style="margin-left:0;">{t['card_p']}</p>
      <h3 style="margin-top:22px;">{t['earn_h']}</h3>
      <ul>{''.join(f'<li>{x}</li>' for x in t['earn'])}</ul>
    </div>
    <div style="text-align:center;">
      <img src="{rel}images/rackets-plus-cards.jpg" alt="{e(t['card_alt'])}" loading="lazy" style="max-width:320px; width:100%; border-radius:var(--radius-md); box-shadow:0 12px 30px rgba(11,26,43,.15);">
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['rew_h']}</h2>
    <p class="section-lede">{t['rew_p']}</p>
    <div class="pill-box">
      <div class="price-table-wrap">
      <table class="price-table">
        <tr><th>{t['rew_th'][0]}</th><th>{t['rew_th'][1]}</th></tr>
        {rew}
      </table>
      </div>
    </div>
  </div>
</section>

<section class="section-tight" style="background:var(--paper);">
  <div class="wrap">
    <h2>{t['faq_h']}</h2>
    <div class="faq-list">{faq}</div>
  </div>
</section>
<script type="application/ld+json">{ld}</script>

<section class="section-tight" style="text-align:center;">
  <div class="wrap">
    <div class="pill-box">
      <h2 style="margin-top:0;">{t['end_h']}</h2>
      <p class="section-lede" style="margin-left:auto; margin-right:auto;">{t['end_p']}</p>
      <div class="hero-actions" style="justify-content:center; display:flex; gap:14px;">
        <a class="btn btn-green" href="{WA}" target="_blank" rel="noopener">{t['end_cta']}</a>
      </div>
    </div>
  </div>
</section>

'''

for lang, t in T.items():
    p = ROOT / lang / 'rackets-plus.html'
    s = p.read_text(encoding='utf-8')
    a = html.escape
    s = re.sub(r'<title>[^<]*</title>', lambda m: f'<title>{a(t["title"], quote=False)}</title>', s, count=1)
    for pat in (r'(<meta name="description" content=")[^"]*(")', r'(<meta property="og:description" content=")[^"]*(")'):
        s = re.sub(pat, lambda m: m.group(1) + a(t['desc']) + m.group(2), s, count=1)
    s = re.sub(r'(<meta property="og:title" content=")[^"]*(")', lambda m: m.group(1) + a(t['title']) + m.group(2), s, count=1)
    i = s.index('<section class="hero'); j = s.index('<footer')
    s = s[:i] + body(t, '../' if lang else '') + s[j:]
    p.write_text(s, encoding='utf-8')
    print('ok', p.relative_to(ROOT), len(s))
