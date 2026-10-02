"""Events hub (events.html, EN/FR/DE): live agenda from Google Calendar + event cards.
Edits only the hero lede, the main section, meta description and an inline style block.
Dates come live from the calendars via nav.js (data-next-event / data-agenda)."""
import re, urllib.parse
WA = 'https://wa.me/41772780115?text='
MSG = {'en': 'Hola! I am interested in {e}. Please keep me posted.',
       'fr': 'Hola ! Je suis intéressé·e par {e}. Tenez-moi au courant.',
       'de': 'Hola! Ich interessiere mich für {e}. Haltet mich auf dem Laufenden.'}
# (key, title, href or None=WhatsApp, calendar keywords, is_new)
CARDS = [
 ('nto24', 'NTO24 · 24h', None, '24h', True),
 ('dine', 'Padel+Dine feat. Instinct Amazonia', None, 'amazonia,dine', True),
 ('ski', 'Ski &amp;Padel', 'ski-and-padel.html', 'ski', False),
 ('racketero', 'Racketero', 'racketero.html', 'racketero', False),
 ('rackemix', 'Rackemix', None, 'rackemix', True),
 ('pickle', 'Pickleball Mix &amp; Match', None, 'pickleball', True),
 ('paella', 'Padel+Paella', 'padel-paella.html', 'paella', False),
 ('wine', 'Padel+Wine', 'padel-wine.html', 'wine', False),
 ('beer', 'Padel+Beer', None, 'beer', True),
 ('fitness', 'Padel+Fitness', 'padel-fitness.html', 'fitness', False),
 ('swiss', None, 'swiss-tennis.html', 'swisstennis,p20,p50,p100,p200,hyundai', False),
 ('rivella', 'Rivella League', 'rivella-league.html', 'rivella', False),
]
T = {
'en': dict(desc='Rackets Academy events in Valais: NTO24 24h tournament, Padel+Dine, Ski &Padel weekends, Racketero, Rackemix, Pickleball Mix & Match, Padel+Paella/Wine/Beer/Fitness, Swiss Tennis and Rivella League.',
  lede='Social nights, weekly tournaments, a 24-hour marathon, ski weekends and official Swiss Tennis competitions. Dates update live from our calendar.',
  agenda_h='Coming up', all_h='All our events', new='New', loading='Loading dates…', wait='Next date loading…',
  more='Learn more →', ask='Ask on WhatsApp →', camps='See the camps →', standings='See standings →', tourn='See tournaments →',
  own='Planning your own event? <a href="company-events.html">Company events</a> · <a href="kids-birthday.html">Kids’ birthdays</a> · <a href="https://www.instagram.com/racketsacademy.ch" target="_blank" rel="noopener">Instagram</a>',
  t={'swiss': 'Swiss Tennis Tournaments'},
  p={'nto24': '24 hours of non-stop padel: teams of 6 rotate so their team never leaves the court. Last team standing wins.',
     'dine': 'Padel first, then dinner by Instinct Amazonia, the restaurant from Granges.',
     'ski': 'Ski by day, padel by night. 4-day weekends in February, small group, simple sporty rooms in Salgesch.',
     'racketero': 'Our friendly tournament for beginners and intermediates — new opponents, your level.',
     'rackemix': 'Our monthly mix night on court — new partners, good vibes, a drink after.',
     'pickle': 'Every Sunday: mix partners, match levels, play pickleball. Newcomers welcome.',
     'paella': '2 hours of padel, then fresh paella and a drink. Max 16 spots.',
     'wine': 'Play, then unwind with a glass of local Valais wine.',
     'beer': 'Play, then a cold beer at the bar with everyone from the courts.',
     'fitness': 'On-court padel combined with a fitness session for a full workout morning.',
     'swiss': 'The Rackets Hyundai Cup and official Swiss Tennis Padel competitions (P20 to P200).',
     'rivella': '32 teams, 8 groups, April–November. The final decides the Academy champion.'}),
'fr': dict(desc="Événements Rackets Academy en Valais : tournoi 24 h NTO24, Padel+Dine, week-ends Ski &Padel, Racketero, Rackemix, Pickleball Mix & Match, Padel+Paella/Wine/Beer/Fitness, Swiss Tennis et Rivella League.",
  lede="Soirées conviviales, tournois réguliers, un marathon de 24 heures, des week-ends de ski et des compétitions officielles Swiss Tennis. Les dates se mettent à jour en direct depuis notre calendrier.",
  agenda_h='À venir', all_h='Tous nos événements', new='Nouveau', loading='Chargement des dates…', wait='Prochaine date en chargement…',
  more='En savoir plus →', ask='Demander sur WhatsApp →', camps='Voir les camps →', standings='Voir le classement →', tourn='Voir les tournois →',
  own="Tu organises ton propre événement ? <a href=\"company-events.html\">Événements d'entreprise</a> · <a href=\"kids-birthday.html\">Anniversaires enfants</a> · <a href=\"https://www.instagram.com/racketsacademy.ch\" target=\"_blank\" rel=\"noopener\">Instagram</a>",
  t={'swiss': 'Tournois Swiss Tennis'},
  p={'nto24': "24 heures de padel non-stop : des équipes de 6 tournent pour ne jamais quitter le terrain. La dernière équipe debout gagne.",
     'dine': "D'abord le padel, ensuite le dîner par Instinct Amazonia, le restaurant de Granges.",
     'ski': "Ski le jour, padel le soir. Week-ends de 4 jours en février, petit groupe, chambres simples et sportives à Salgesch.",
     'racketero': "Notre tournoi convivial pour débutants et intermédiaires — nouveaux adversaires, ton niveau.",
     'rackemix': "Notre soirée mix mensuelle sur le terrain — nouveaux partenaires, bonne ambiance, un verre après.",
     'pickle': "Chaque dimanche : on mélange les partenaires, on équilibre les niveaux, on joue au pickleball. Débutants bienvenus.",
     'paella': "2 heures de padel, puis une paella fraîche et une boisson. Max. 16 places.",
     'wine': "Joue, puis détends-toi avec un verre de vin valaisan.",
     'beer': "Joue, puis une bière fraîche au bar avec tout le monde.",
     'fitness': "Padel sur le terrain et séance de fitness pour une matinée d'entraînement complète.",
     'swiss': "La Rackets Hyundai Cup et les compétitions officielles Swiss Tennis Padel (P20 à P200).",
     'rivella': "32 équipes, 8 groupes, d'avril à novembre. La finale désigne le champion de l'Academy."}),
'de': dict(desc='Rackets Academy Events im Wallis: NTO24 24-Std.-Turnier, Padel+Dine, Ski &Padel Wochenenden, Racketero, Rackemix, Pickleball Mix & Match, Padel+Paella/Wine/Beer/Fitness, Swiss Tennis und Rivella League.',
  lede='Gesellige Abende, regelmässige Turniere, ein 24-Stunden-Marathon, Ski-Wochenenden und offizielle Swiss Tennis Wettkämpfe. Die Daten kommen live aus unserem Kalender.',
  agenda_h='Demnächst', all_h='Alle unsere Events', new='Neu', loading='Daten werden geladen…', wait='Nächstes Datum wird geladen…',
  more='Mehr erfahren →', ask='Per WhatsApp fragen →', camps='Zu den Camps →', standings='Zur Tabelle →', tourn='Zu den Turnieren →',
  own='Du planst deinen eigenen Anlass? <a href="company-events.html">Firmenevents</a> · <a href="kids-birthday.html">Kindergeburtstage</a> · <a href="https://www.instagram.com/racketsacademy.ch" target="_blank" rel="noopener">Instagram</a>',
  t={'swiss': 'Swiss Tennis Turniere'},
  p={'nto24': '24 Stunden Padel nonstop: 6er-Teams wechseln sich ab, damit ihr Team nie vom Platz geht. Das letzte Team gewinnt.',
     'dine': 'Zuerst Padel, dann Abendessen von Instinct Amazonia, dem Restaurant aus Granges.',
     'ski': 'Tagsüber Ski, abends Padel. 4-tägige Wochenenden im Februar, kleine Gruppe, einfache sportliche Zimmer in Salgesch.',
     'racketero': 'Unser Freundschaftsturnier für Einsteiger und Fortgeschrittene — neue Gegner, dein Level.',
     'rackemix': 'Unser monatlicher Mix-Abend auf dem Platz — neue Partner, gute Stimmung, ein Drink danach.',
     'pickle': 'Jeden Sonntag: Partner mischen, Niveaus ausgleichen, Pickleball spielen. Neue sind willkommen.',
     'paella': '2 Stunden Padel, dann frische Paella und ein Drink. Max. 16 Plätze.',
     'wine': 'Spiel, dann entspann dich bei einem Glas Walliser Wein.',
     'beer': 'Spiel, dann ein kühles Bier an der Bar mit allen vom Platz.',
     'fitness': 'Padel auf dem Platz kombiniert mit einer Fitness-Einheit für einen vollen Workout-Morgen.',
     'swiss': 'Der Rackets Hyundai Cup und offizielle Swiss Tennis Padel-Wettkämpfe (P20 bis P200).',
     'rivella': '32 Teams, 8 Gruppen, April–November. Das Finale kürt den Academy-Champion.'}),
}
CSS = '''<style id="ev-hub-css">
.ev-agenda-sec{padding-bottom:0}
.ev-agenda{display:grid;gap:8px;max-width:760px}
.ev-row{display:grid;grid-template-columns:minmax(150px,auto) 1fr auto;gap:14px;align-items:center;padding:12px 16px;border-radius:12px;background:var(--paper,#f4f7fb);text-decoration:none;color:inherit;transition:transform .15s}
.ev-row:hover{transform:translateX(3px)}
.ev-when{font-weight:800;color:var(--blue-dark,#045bab);font-size:.9rem;white-space:nowrap}
.ev-what{font-weight:600}
.ev-go{opacity:.6}
.ev-empty,.ev-agenda-loading{opacity:.7;margin:0}
.ev-new{display:inline-block;background:var(--green,#c6f432);color:var(--blue-dark,#045bab);font-size:.68rem;font-weight:800;text-transform:uppercase;letter-spacing:.04em;padding:3px 8px;border-radius:999px;margin-bottom:8px}
.ev-own{margin-top:22px;text-align:center;opacity:.9}
@media (max-width:560px){.ev-row{grid-template-columns:1fr auto}.ev-when{grid-column:1/-1;white-space:normal}}
</style>
'''
def section(lang, t):
    cards = []
    for key, title, href, kw, new in CARDS:
        title = title or t['t'][key]
        plain = re.sub('<[^>]+>', '', title).replace('&amp;', '&')
        if href:
            link = f'href="{href}"'
            cta = {'ski': t['camps'], 'rivella': t['standings'], 'swiss': t['tourn']}.get(key, t['more'])
        else:
            link = 'href="' + WA + urllib.parse.quote(MSG[lang].format(e=plain)) + '" target="_blank" rel="noopener"'
            cta = t['ask']
        tag = f'<span class="ev-new">{t["new"]}</span>' if new else ''
        cards.append(f'''      <a class="card card-link" {link}>
        {tag}<h3>{title}</h3>
        <p>{t['p'][key]}</p>
        <span data-next-event="{kw}">{t['wait']}</span>
        <span class="card-cta">{cta}</span>
      </a>''')
    return f'''<section class="ev-agenda-sec">
  <div class="wrap">
    <h2>{t['agenda_h']}</h2>
    <div class="ev-agenda" data-agenda="8"><p class="ev-agenda-loading">{t['loading']}</p></div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{t['all_h']}</h2>
    <div class="grid-3">
{chr(10).join(cards)}
    </div>
    <p class="ev-own">{t['own']}</p>
  </div>
</section>

'''
for lang, t in T.items():
    path = 'events.html' if lang == 'en' else lang + '/events.html'
    s = open(path).read()
    a = s.index('</section>', s.index('<section class="hero"')) + len('</section>\n\n')
    b = s.index('<footer>')
    s = s[:a] + section(lang, t) + s[b:]
    s = re.sub(r'(<section class="hero".*?<p class="lede">).*?(</p>)', lambda m: m.group(1) + t['lede'] + m.group(2), s, count=1, flags=re.S)
    esc = t['desc'].replace('&', '&amp;').replace('"', '&quot;')
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + esc + '"', s)
    s = re.sub(r'<style id="ev-hub-css">.*?</style>\n', '', s, flags=re.S)
    s = s.replace('</head>', CSS + '</head>', 1)
    s = re.sub(r'nav\.js\?v=\d+', 'nav.js?v=22', s)
    open(path, 'w').write(s)
    print(path, len(t['desc']))
