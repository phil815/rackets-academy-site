"""24h tournament page (P424): EN source = padel4ever/index.html.
Builds de/padel4ever/index.html and fr/padel4ever/index.html by replacing every
English text (static + simulator JS). Also adds hreflang + EN/DE/FR switch to all three.
Edit the EN page, then run: python3 tools/build_p424.py  (fails loudly if a string is missing)."""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'padel4ever', 'index.html')
BASE = 'https://www.racketsacademy.ch'
URL = {'en': '/padel4ever/', 'de': '/de/padel4ever/', 'fr': '/fr/padel4ever/'}

HEAD_TAG = '<!-- p424-i18n -->'
CSS = '.lsw{display:flex; gap:8px}.lsw a{color:#7f8ea0; text-decoration:none; font-size:13px; font-weight:800}.lsw a.on,.lsw a:hover{color:var(--green)}\n'

def i18n_head():
    links = ''.join(f'<link rel="alternate" hreflang="{l}" href="{BASE}{u}">\n' for l, u in URL.items())
    links += f'<link rel="alternate" hreflang="x-default" href="{BASE}{URL["en"]}">\n'
    return HEAD_TAG + '\n' + links

def switch(lang):
    on = ' class="on" aria-current="page"'
    return '<span class="lsw">' + ''.join(
        '<a href="%s" lang="%s"%s>%s</a>' % (URL[l], l, on if l == lang else '', l.upper())
        for l in ('en', 'de', 'fr')) + '</span>'

# (english, deutsch, français) — exact substrings of the EN page
T = [
 ('<html lang="en">', '<html lang="de">', '<html lang="fr">'),
 ('<title>P424 · 24h non-stop padel · Salgesch, 13–14 Mar 2027</title>',
  '<title>P424 · 24 Stunden Padel nonstop · Salgesch, 13.–14. März 2027</title>',
  '<title>P424 · 24 h de padel non-stop · Salgesch, 13–14 mars 2027</title>'),
 ('content="P424: 24 hours of non-stop padel. 6 crews of 8, 3 courts, one live table. Rackets Academy Salgesch, 13–14 Mar 2027."',
  'content="P424: 24 Stunden Padel nonstop. 6 Crews à 8, 3 Plätze, eine Live-Tabelle. Rackets Academy Salgesch, 13.–14. März 2027."',
  'content="P424 : 24 heures de padel non-stop. 6 équipes de 8, 3 terrains, un classement en direct. Rackets Academy Salgesch, 13–14 mars 2027."'),
 ('aria-label="P424 home"', 'aria-label="P424 Start"', 'aria-label="P424 accueil"'),
 ('<a class="l" href="#how">How it works</a>', '<a class="l" href="#how">So funktioniert’s</a>', '<a class="l" href="#how">Le principe</a>'),
 ('<a class="l" href="#play">Play it</a>', '<a class="l" href="#play">Selbst spielen</a>', '<a class="l" href="#play">À toi de jouer</a>'),
 ('<a class="l" href="#included">What\'s in</a>', '<a class="l" href="#included">Inklusive</a>', '<a class="l" href="#included">Inclus</a>'),
 ('<a class="pill" href="#register">Register a crew</a>', '<a class="pill" href="#register">Crew anmelden</a>', '<a class="pill" href="#register">Inscrire une équipe</a>'),
 ('Salgesch · Sat 13 Mar 13:00 to Sun 14 Mar 13:00', 'Salgesch · Sa 13. März 13:00 bis So 14. März 13:00', 'Salgesch · sam 13 mars 13:00 au dim 14 mars 13:00'),
 ('Padel for 24 hours. Your crew holds the court all day and all night.',
  '24 Stunden Padel. Deine Crew hält den Platz den ganzen Tag und die ganze Nacht.',
  '24 heures de padel. Ton équipe tient le terrain toute la journée et toute la nuit.'),
 ('Six crews of eight. Three courts. Two of you are always playing. Every game you win goes on one live table. Highest score at 13:00 on Sunday takes it.',
  'Sechs Crews à acht. Drei Plätze. Zwei von euch spielen immer. Jedes gewonnene Game kommt auf eine Live-Tabelle. Wer am Sonntag um 13:00 vorne liegt, gewinnt.',
  'Six équipes de huit. Trois terrains. Deux d’entre vous jouent toujours. Chaque jeu gagné compte au classement en direct. Le meilleur score dimanche à 13:00 l’emporte.'),
 ('<a class="pill" href="#play">Play a round yourself</a>', '<a class="pill" href="#play">Selbst eine Runde spielen</a>', '<a class="pill" href="#play">Joue une partie</a>'),
 ('<a class="pill ghost" href="#how">How it works</a>', '<a class="pill ghost" href="#how">So funktioniert’s</a>', '<a class="pill ghost" href="#how">Le principe</a>'),
 ('<span>Sat 13:00</span><span>Graveyard shift 01:30–04:50</span><span>Final · Sun 13:00</span>',
  '<span>Sa 13:00</span><span>Nachtschicht 01:30–04:50</span><span>Finale · So 13:00</span>',
  '<span>sam 13:00</span><span>Service de nuit 01:30–04:50</span><span>Finale · dim 13:00</span>'),
 ('<div class="l">crews</div>', '<div class="l">Crews</div>', '<div class="l">équipes</div>'),
 ('<div class="l">players each</div>', '<div class="l">Spieler pro Crew</div>', '<div class="l">joueurs chacune</div>'),
 ('<div class="l">courts</div>', '<div class="l">Plätze</div>', '<div class="l">terrains</div>'),
 ('<div class="l">rounds</div>', '<div class="l">Runden</div>', '<div class="l">tours</div>'),
 ('<div class="l">padel per player</div>', '<div class="l">Padel pro Person</div>', '<div class="l">de padel par joueur</div>'),
 ('<h2>How it works</h2>', '<h2>So funktioniert’s</h2>', '<h2>Le principe</h2>'),
 ('Read this once. Then play it below, and it clicks.', 'Einmal lesen. Dann unten selbst spielen, und es macht Klick.', 'Lis ceci une fois. Puis joue en dessous, et tout devient clair.'),
 ('<h3>Build a crew of eight</h3><p>One captain, seven teammates. Mixed levels are fine. Depth matters more than one star.</p>',
  '<h3>Stell eine Crew aus acht zusammen</h3><p>Ein Captain, sieben Teammates. Gemischte Levels sind kein Problem. Breite zählt mehr als ein Star.</p>',
  '<h3>Forme une équipe de huit</h3><p>Un capitaine, sept coéquipiers. Les niveaux mixtes sont les bienvenus. La profondeur compte plus qu’une star.</p>'),
 ('<h3>Two of you are always on court</h3><p>All six crews play at the same time on three courts. Each round lasts 45 minutes plus a 5-minute change. You face a different crew every round.</p>',
  '<h3>Zwei von euch stehen immer auf dem Platz</h3><p>Alle sechs Crews spielen gleichzeitig auf drei Plätzen. Jede Runde dauert 45 Minuten plus 5 Minuten Wechsel. Jede Runde gegen eine andere Crew.</p>',
  '<h3>Deux d’entre vous sont toujours sur le terrain</h3><p>Les six équipes jouent en même temps sur trois terrains. Chaque tour dure 45 minutes, plus 5 minutes de changement. À chaque tour, une autre équipe en face.</p>'),
 ('<h3>The captain picks the duo</h3><p>Before each round the captain sends two players. Rule one: every possible duo of your eight plays exactly once (that\'s 28 rounds). Rule two: nobody plays two rounds in a row.</p>',
  '<h3>Der Captain wählt das Duo</h3><p>Vor jeder Runde schickt der Captain zwei Spieler. Regel eins: Jedes mögliche Duo aus euren acht spielt genau einmal (das sind 28 Runden). Regel zwei: Niemand spielt zwei Runden hintereinander.</p>',
  '<h3>Le capitaine choisit le duo</h3><p>Avant chaque tour, le capitaine envoie deux joueurs. Règle un : chaque duo possible parmi vos huit joue exactement une fois (soit 28 tours). Règle deux : personne ne joue deux tours de suite.</p>'),
 ('<h3>Every game counts</h3><p>No sets to protect, no knockouts. Every game your duo wins is a point on the live table. Lose 6–4? You still bank 4.</p>',
  '<h3>Jedes Game zählt</h3><p>Keine Sätze, kein K.-o. Jedes Game, das euer Duo gewinnt, ist ein Punkt auf der Live-Tabelle. 4–6 verloren? Die 4 gehören trotzdem euch.</p>',
  '<h3>Chaque jeu compte</h3><p>Pas de sets à défendre, pas d’élimination. Chaque jeu gagné par ton duo vaut un point au classement en direct. Perdu 4–6 ? Tu encaisses quand même 4.</p>'),
 ('<h3>Graveyard shift</h3><p>Rounds 16 to 19, from 01:30 to 04:50. Every game counts double for everyone. Whoever saves energy for the night wins the tournament.</p>',
  '<h3>Nachtschicht</h3><p>Runden 16 bis 19, von 01:30 bis 04:50. Jedes Game zählt für alle doppelt. Wer Energie für die Nacht spart, gewinnt das Turnier.</p>',
  '<h3>Service de nuit</h3><p>Tours 16 à 19, de 01:30 à 04:50. Chaque jeu compte double pour tout le monde. Qui garde de l’énergie pour la nuit gagne le tournoi.</p>'),
 ('<h3>Joker</h3><p>Once per tournament the captain can double one round for their crew only. Not in the graveyard shift. Timing is everything.</p>',
  '<h3>Joker</h3><p>Einmal pro Turnier kann der Captain eine Runde nur für seine Crew verdoppeln. Nicht in der Nachtschicht. Das Timing entscheidet.</p>',
  '<h3>Joker</h3><p>Une fois par tournoi, le capitaine peut doubler un tour pour son équipe seulement. Pas pendant le service de nuit. Tout est dans le timing.</p>'),
 ('<h3>Final round</h3><p>Sunday 12:20 to 13:00. Captain\'s pick, any duo, double points. The table can still flip in the last 40 minutes.</p>',
  '<h3>Finalrunde</h3><p>Sonntag 12:20 bis 13:00. Der Captain wählt ein beliebiges Duo, doppelte Punkte. In den letzten 40 Minuten kann die Tabelle noch kippen.</p>',
  '<h3>Tour final</h3><p>Dimanche de 12:20 à 13:00. Le capitaine choisit n’importe quel duo, points doublés. Le classement peut encore basculer dans les 40 dernières minutes.</p>'),
 ("<h2>You're the captain. Play it.</h2>", '<h2>Du bist Captain. Spiel’s durch.</h2>', '<h2>Tu es le capitaine. À toi de jouer.</h2>'),
 ('Enter your crew, then pick the duo for every round. Watch energy, save players for the graveyard shift, and use your joker. The other five crews are run by the computer.',
  'Gib deine Crew ein und wähl für jede Runde das Duo. Achte auf die Energie, spar Spieler für die Nachtschicht und setz deinen Joker. Die anderen fünf Crews spielt der Computer.',
  'Entre ton équipe, puis choisis le duo de chaque tour. Surveille l’énergie, garde des joueurs pour le service de nuit et place ton joker. Les cinq autres équipes sont jouées par l’ordinateur.'),
 ('<label for="crew">Crew name</label>', '<label for="crew">Name der Crew</label>', '<label for="crew">Nom de l’équipe</label>'),
 ('value="The Grinders"', 'value="Die Unermüdlichen"', 'value="Les Increvables"'),
 ('>Start at Sat 13:00</button>', '>Start am Sa um 13:00</button>', '>Départ sam à 13:00</button>'),
 ('<div class="rnum" id="rnum">Round 1</div>', '<div class="rnum" id="rnum">Runde 1</div>', '<div class="rnum" id="rnum">Tour 1</div>'),
 ('<p class="hint" id="hint">Tap two players to send them on court.</p>', '<p class="hint" id="hint">Tipp zwei Spieler an, um sie auf den Platz zu schicken.</p>', '<p class="hint" id="hint">Touche deux joueurs pour les envoyer sur le terrain.</p>'),
 ('disabled>Play round</button>', 'disabled>Runde spielen</button>', 'disabled>Jouer le tour</button>'),
 ('<input type="checkbox" id="joker"> Use joker (×2)', '<input type="checkbox" id="joker"> Joker setzen (×2)', '<input type="checkbox" id="joker"> Utiliser le joker (×2)'),
 ('>Auto-play to the end</button>', '>Automatisch zu Ende spielen</button>', '>Jouer automatiquement jusqu’au bout</button>'),
 ('<h3 style="color:#fff">Live table</h3>', '<h3 style="color:#fff">Live-Tabelle</h3>', '<h3 style="color:#fff">Classement en direct</h3>'),
 ('aria-label="Live table"', 'aria-label="Live-Tabelle"', 'aria-label="Classement en direct"'),
 ('<th>Crew</th><th style="text-align:right">Games</th><th style="text-align:right">Points</th>',
  '<th>Crew</th><th style="text-align:right">Games</th><th style="text-align:right">Punkte</th>',
  '<th>Équipe</th><th style="text-align:right">Jeux</th><th style="text-align:right">Points</th>'),
 ('Points = games won × multiplier. On the night, this table runs on screens in the hall and on Instagram.',
  'Punkte = gewonnene Games × Multiplikator. In der Turniernacht läuft diese Tabelle auf Bildschirmen in der Halle und auf Instagram.',
  'Points = jeux gagnés × multiplicateur. Le jour J, ce classement s’affiche sur les écrans de la halle et sur Instagram.'),
 ('Simulation only. Results depend on player energy and a bit of luck. On the day, captains make the same decisions you just made.',
  'Nur eine Simulation. Die Resultate hängen von der Energie der Spieler und etwas Glück ab. Am Turnier treffen die Captains genau dieselben Entscheidungen wie du gerade.',
  'Simple simulation. Les résultats dépendent de l’énergie des joueurs et d’un peu de chance. Le jour J, les capitaines prennent les mêmes décisions que toi.'),
 ("<h2>What's included</h2>", '<h2>Was inklusive ist</h2>', '<h2>Ce qui est inclus</h2>'),
 ('One price. Everything for 24 hours under one roof.', 'Ein Preis. Alles für 24 Stunden unter einem Dach.', 'Un seul prix. Tout pour 24 heures sous un même toit.'),
 ("<small>per player<br>CHF 1'992 per crew of 8</small>", "<small>pro Person<br>CHF 1'992 pro 8er-Crew</small>", "<small>par joueur<br>CHF 1'992 par équipe de 8</small>"),
 ('<li>~6 hours of match padel<span>7 matches with 7 different partners, plus the final</span></li>',
  '<li>~6 Stunden Match-Padel<span>7 Matches mit 7 verschiedenen Partnern, plus Finale</span></li>',
  '<li>~6 heures de padel en match<span>7 matchs avec 7 partenaires différents, plus la finale</span></li>'),
 ('<li>Two rooms per crew<span>Sleep in shifts while your duo plays</span></li>',
  '<li>Zwei Zimmer pro Crew<span>Schlafen im Schichtbetrieb, während euer Duo spielt</span></li>',
  '<li>Deux chambres par équipe<span>Dormir à tour de rôle pendant que ton duo joue</span></li>'),
 ('<li>Sat lunch: lasagne</li>', '<li>Sa Mittag: Lasagne</li>', '<li>Sam midi : lasagnes</li>'),
 ('<li>Sat dinner: roast with mashed potatoes</li>', '<li>Sa Abend: Braten mit Kartoffelstock</li>', '<li>Sam soir : rôti et purée</li>'),
 ('<li>Night fuel<span>Bananas and snacks, all night</span></li>', '<li>Energie für die Nacht<span>Bananen und Snacks, die ganze Nacht</span></li>', '<li>Carburant de nuit<span>Bananes et snacks, toute la nuit</span></li>'),
 ('<li>Sun breakfast buffet</li>', '<li>So Frühstücksbuffet</li>', '<li>Dim buffet petit-déjeuner</li>'),
 ('<li>Sun lunch: pizza</li>', '<li>So Mittag: Pizza</li>', '<li>Dim midi : pizza</li>'),
 ('<li>Spa, sauna and gym</li>', '<li>Spa, Sauna und Gym</li>', '<li>Spa, sauna et salle de fitness</li>'),
 ('<li>Physio on call</li>', '<li>Physio auf Abruf</li>', '<li>Physio sur appel</li>'),
 ('<li>DJ through the night</li>', '<li>DJ die ganze Nacht</li>', '<li>DJ toute la nuit</li>'),
 ('<li>Finisher shirt and goodie bag</li>', '<li>Finisher-Shirt und Goodie-Bag</li>', '<li>T-shirt finisher et goodie bag</li>'),
 ('<li>Water, free and unlimited<span>Other drinks at the bar</span></li>', '<li>Wasser, gratis und unbegrenzt<span>Andere Getränke an der Bar</span></li>', '<li>Eau gratuite et à volonté<span>Autres boissons au bar</span></li>'),
 ('<h3>The rest zone is the venue</h3>', '<h3>Die Ruhezone ist gleich hier</h3>', '<h3>La zone de repos, c’est sur place</h3>'),
 ('Between your matches you have about two and a half hours. Sauna, spa, gym, physio, bar and beds are all in the same building, a few steps from the court. No car, no hotel transfer. Recover, sleep, come back sharp.',
  'Zwischen deinen Matches hast du rund zweieinhalb Stunden. Sauna, Spa, Gym, Physio, Bar und Betten sind alle im selben Gebäude, ein paar Schritte vom Platz. Kein Auto, kein Hoteltransfer. Erholen, schlafen, frisch zurückkommen.',
  'Entre tes matchs, tu as environ deux heures et demie. Sauna, spa, fitness, physio, bar et lits sont dans le même bâtiment, à quelques pas du terrain. Pas de voiture, pas de transfert à l’hôtel. Récupère, dors, reviens affûté.'),
 ('<small>matches per player</small>', '<small>Matches pro Person</small>', '<small>matchs par joueur</small>'),
 ('<small>different partners</small>', '<small>verschiedene Partner</small>', '<small>partenaires différents</small>'),
 ('<small>on court</small>', '<small>auf dem Platz</small>', '<small>sur le terrain</small>'),
 ("<small>night you'll talk about</small>", '<small>Nacht, von der du noch lange erzählst</small>', '<small>nuit dont tu parleras longtemps</small>'),
 ('<h2>Schedule</h2>', '<h2>Ablauf</h2>', '<h2>Programme</h2>'),
 ('<span class="t">Sat 12:00</span><span>Check-in, shirts, lunch</span>', '<span class="t">Sa 12:00</span><span>Check-in, Shirts, Mittagessen</span>', '<span class="t">sam 12:00</span><span>Check-in, t-shirts, repas de midi</span>'),
 ('<span class="t">Sat 13:00</span><span>Clock starts. Round 1 on all three courts</span>', '<span class="t">Sa 13:00</span><span>Die Uhr läuft. Runde 1 auf allen drei Plätzen</span>', '<span class="t">sam 13:00</span><span>Le chrono démarre. Tour 1 sur les trois terrains</span>'),
 ('<span class="t">Sat 19:00–21:00</span><span>Dinner in shifts. Courts keep running</span>', '<span class="t">Sa 19:00–21:00</span><span>Abendessen in Schichten. Auf den Plätzen geht’s weiter</span>', '<span class="t">sam 19:00–21:00</span><span>Souper à tour de rôle. Les terrains continuent</span>'),
 ('<span class="t">Sat 22:00</span><span>DJ on. Lights down</span>', '<span class="t">Sa 22:00</span><span>DJ legt los. Licht runter</span>', '<span class="t">sam 22:00</span><span>DJ aux platines. Lumières tamisées</span>'),
 ('<span class="t">Sun 01:30–04:50</span><span>Graveyard shift. Rounds 16 to 19 count double</span>', '<span class="t">So 01:30–04:50</span><span>Nachtschicht. Runden 16 bis 19 zählen doppelt</span>', '<span class="t">dim 01:30–04:50</span><span>Service de nuit. Les tours 16 à 19 comptent double</span>'),
 ('<span class="t">Sun 07:00–09:00</span><span>Breakfast buffet in shifts</span>', '<span class="t">So 07:00–09:00</span><span>Frühstücksbuffet in Schichten</span>', '<span class="t">dim 07:00–09:00</span><span>Buffet petit-déjeuner à tour de rôle</span>'),
 ('<span class="t">Sun 12:20–13:00</span><span>Final round. Captain\'s pick, double points</span>', '<span class="t">So 12:20–13:00</span><span>Finalrunde. Der Captain wählt, doppelte Punkte</span>', '<span class="t">dim 12:20–13:00</span><span>Tour final. Choix du capitaine, points doublés</span>'),
 ('<span class="t">Sun 13:00</span><span>Clock stops. Podium, pizza</span>', '<span class="t">So 13:00</span><span>Die Uhr stoppt. Podest, Pizza</span>', '<span class="t">dim 13:00</span><span>Fin du chrono. Podium, pizza</span>'),
 ('<h2>Questions</h2>', '<h2>Fragen</h2>', '<h2>Questions</h2>'),
 ('<summary>Do I have to stay awake for 24 hours?</summary><p>No. You play about every fourth round. Most players sleep 3 to 4 hours in shifts. Your captain plans who rests when.</p>',
  '<summary>Muss ich 24 Stunden wach bleiben?</summary><p>Nein. Du spielst etwa jede vierte Runde. Die meisten schlafen 3 bis 4 Stunden im Schichtbetrieb. Dein Captain plant, wer wann Pause macht.</p>',
  '<summary>Dois-je rester éveillé 24 heures ?</summary><p>Non. Tu joues environ un tour sur quatre. La plupart dorment 3 à 4 heures à tour de rôle. Ton capitaine planifie qui se repose quand.</p>'),
 ('<summary>What level do I need?</summary><p>You should be comfortable in a match. Crews of mixed levels work well, because every duo plays once and the captain decides when.</p>',
  '<summary>Welches Level brauche ich?</summary><p>Du solltest dich im Match wohlfühlen. Crews mit gemischten Levels funktionieren gut, weil jedes Duo einmal spielt und der Captain entscheidet, wann.</p>',
  '<summary>Quel niveau faut-il ?</summary><p>Tu dois être à l’aise en match. Les équipes de niveaux mixtes fonctionnent bien, car chaque duo joue une fois et le capitaine décide quand.</p>'),
 ('<summary>What if a player gets injured or drops out?</summary><p>A crew needs at least five fit players to continue. With fewer, the crew stops and keeps the points it has.</p>',
  '<summary>Was, wenn sich jemand verletzt oder ausfällt?</summary><p>Eine Crew braucht mindestens fünf fitte Spieler, um weiterzuspielen. Mit weniger hört die Crew auf und behält ihre Punkte.</p>',
  '<summary>Et si un joueur se blesse ou abandonne ?</summary><p>Une équipe a besoin d’au moins cinq joueurs en forme pour continuer. En dessous, elle s’arrête et garde ses points.</p>'),
 ('<summary>How is the score counted?</summary><p>Each round is 45 minutes of play. Every game your duo wins is one point, two in the graveyard shift, the final round or your joker round. Ties are broken by total games won.</p>',
  '<summary>Wie wird gezählt?</summary><p>Jede Runde dauert 45 Minuten Spielzeit. Jedes Game, das euer Duo gewinnt, gibt einen Punkt, in der Nachtschicht, der Finalrunde oder eurer Joker-Runde zwei. Bei Gleichstand entscheidet die Gesamtzahl gewonnener Games.</p>',
  '<summary>Comment sont comptés les points ?</summary><p>Chaque tour dure 45 minutes de jeu. Chaque jeu gagné par ton duo vaut un point, deux pendant le service de nuit, le tour final ou ton tour joker. En cas d’égalité, le total de jeux gagnés départage.</p>'),
 ('<summary>Can I register alone?</summary><p>Yes. Message us and we put you in a crew.</p>',
  '<summary>Kann ich mich allein anmelden?</summary><p>Ja. Schreib uns, und wir teilen dich einer Crew zu.</p>',
  '<summary>Puis-je m’inscrire seul ?</summary><p>Oui. Écris-nous et on te place dans une équipe.</p>'),
 ("<h2>Six crews. That's it.</h2>", '<h2>Sechs Crews. Mehr nicht.</h2>', '<h2>Six équipes. Pas une de plus.</h2>'),
 ('<p>Get your eight together. Spots go to the first crews that commit.</p>', '<p>Trommle deine acht zusammen. Die Plätze gehen an die ersten Crews, die zusagen.</p>', '<p>Réunis tes huit. Les places vont aux premières équipes qui s’engagent.</p>'),
 ('?text=Hi%2C%20we%20want%20to%20register%20a%20crew%20for%20P424', '?text=Hallo%2C%20wir%20m%C3%B6chten%20eine%20Crew%20f%C3%BCr%20P424%20anmelden', '?text=Salut%2C%20nous%20voulons%20inscrire%20une%20%C3%A9quipe%20pour%20P424'),
 ('>Register on WhatsApp</a>', '>Per WhatsApp anmelden</a>', '>S’inscrire sur WhatsApp</a>'),
 ('P424 · working title, trademark check pending · A Rackets Academy production, Salgesch', 'P424 · Arbeitstitel, Markenprüfung läuft · Eine Produktion der Rackets Academy, Salgesch', 'P424 · titre provisoire, vérification de marque en cours · Une production Rackets Academy, Salgesch'),
 # --- simulator (JS) ---
 ("return (d?'Sun ':'Sat ')", "return (d?'So ':'Sa ')", "return (d?'dim ':'sam ')"),
 ("var defaults = ['Marco','Luca','Nico','Sam','Jonas','Dario','Tim','Alex'];", "var defaults = ['Marco','Luca','Nico','Sam','Jonas','Dario','Tim','Alex'];", "var defaults = ['Marco','Luca','Nico','Sam','Jonas','Dario','Théo','Alex'];"),
 ("'\">Player '+(i+1)+'</label>", "'\">Spieler '+(i+1)+'</label>", "'\">Joueur '+(i+1)+'</label>"),
 ("names.push(v||('Player '+(i+1)));", "names.push(v||('Spieler '+(i+1)));", "names.push(v||('Joueur '+(i+1)));"),
 ("||'Your crew';", "||'Deine Crew';", "||'Ton équipe';"),
 ("status:'Fresh'}", "status:'Frisch'}", "status:'En forme'}"),
 ("r===FINAL ? 'Final round' : 'Round '+r+' of 28'", "r===FINAL ? 'Finalrunde' : 'Runde '+r+' von 28'", "r===FINAL ? 'Tour final' : 'Tour '+r+' sur 28'"),
 ("'<span class=\"tag gy\">Graveyard ×2</span> '", "'<span class=\"tag gy\">Nachtschicht ×2</span> '", "'<span class=\"tag gy\">Service de nuit ×2</span> '"),
 ("'<span class=\"tag fn\">Final ×2 · any duo</span> '", "'<span class=\"tag fn\">Finale ×2 · freies Duo</span> '", "'<span class=\"tag fn\">Finale ×2 · duo libre</span> '"),
 ("'<span class=\"tag jk\">Joker available</span>'", "'<span class=\"tag jk\">Joker verfügbar</span>'", "'<span class=\"tag jk\">Joker disponible</span>'"),
 ("? 'Just played' : p.status", "? 'Gerade gespielt' : p.status", "? 'Vient de jouer' : p.status"),
 ("+why+' · energy '+e+'%</span>'", "+why+' · Energie '+e+'%</span>'", "+why+' · énergie '+e+'%</span>'"),
 ("h='Final: send any two, as long as they did not play round 28.';", "h='Finale: Schick zwei beliebige, solange sie nicht in Runde 28 gespielt haben.';", "h='Finale : envoie deux joueurs au choix, s’ils n’ont pas joué le tour 28.';"),
 ("h='Tap two players. Greyed out = not allowed this round.';", "h='Tipp zwei Spieler an. Ausgegraut = in dieser Runde nicht erlaubt.';", "h='Touche deux joueurs. Grisé = pas autorisé ce tour.';"),
 ("h='Now pick a partner for '+", "h='Jetzt einen Partner wählen für '+", "h='Choisis maintenant un partenaire pour '+"),
 ("+' are ready.';", "+' sind bereit.';", "+' sont prêts.';"),
 ("p.status='Recovering';", "p.status='Erholt sich';", "p.status='Récupère';"),
 ("p.status = p.energy>85?'Fresh':(Math.random()<.5?'Sauna':(Math.random()<.5?'Sleeping':'Physio'));",
  "p.status = p.energy>85?'Frisch':(Math.random()<.5?'Sauna':(Math.random()<.5?'Schläft':'Physio'));",
  "p.status = p.energy>85?'En forme':(Math.random()<.5?'Sauna':(Math.random()<.5?'Dort':'Physio'));"),
 ("+(r===FINAL?'Final':'Round '+r)+' results</div>'", "+(r===FINAL?'Finale':'Runde '+r)+': Resultate</div>'", "+(r===FINAL?'Finale':'Tour '+r)+' : résultats</div>'"),
 ("'<span class=\"c\">Court '+x.c+'</span>", "'<span class=\"c\">Platz '+x.c+'</span>", "'<span class=\"c\">Terrain '+x.c+'</span>"),
 ("?' Points doubled this round.':''", "?' Punkte in dieser Runde verdoppelt.':''", "?' Points doublés ce tour.':''"),
 ("(r===FINAL?'Final played.':'Round '+r+' done.')", "(r===FINAL?'Finale gespielt.':'Runde '+r+' fertig.')", "(r===FINAL?'Finale jouée.':'Tour '+r+' terminé.')"),
 ("pos===1?'You won P424.':(pos<=3?'Podium. Place '+pos+'.':'Place '+pos+' of 6.')",
  "pos===1?'Du hast P424 gewonnen.':(pos<=3?'Podest. Platz '+pos+'.':'Platz '+pos+' von 6.')",
  "pos===1?'Tu as gagné P424.':(pos<=3?'Podium. '+pos+'e place.':pos+'e place sur 6.')"),
 ("' finished with '+me.pts+' points from '+me.games+' games.</p><ul><li>Every one of your 8 players played 7 matches with 7 different partners.</li><li>That is about 5 hours 15 minutes of match play each, plus the final.</li><li>Most tired at the end: '",
  "' beendet das Turnier mit '+me.pts+' Punkten aus '+me.games+' Games.</p><ul><li>Jeder deiner 8 Spieler hat 7 Matches mit 7 verschiedenen Partnern gespielt.</li><li>Das sind rund 5 Stunden 15 Minuten Spielzeit pro Person, plus Finale.</li><li>Am Ende am müdesten: '",
  "' termine avec '+me.pts+' points pour '+me.games+' jeux.</p><ul><li>Chacun de tes 8 joueurs a disputé 7 matchs avec 7 partenaires différents.</li><li>Soit environ 5 heures 15 de jeu chacun, plus la finale.</li><li>Le plus fatigué à la fin : '"),
 ("+'% energy).</li></ul>", "+'% Energie).</li></ul>", "+'% d’énergie).</li></ul>"),
 ("href=\"#register\">Register a real crew</a>", "href=\"#register\">Echte Crew anmelden</a>", "href=\"#register\">Inscrire une vraie équipe</a>"),
 ("id=\"againBtn\">Play again</button>", "id=\"againBtn\">Nochmals spielen</button>", "id=\"againBtn\">Rejouer</button>"),
 ("$('hint').textContent='Final results below.';", "$('hint').textContent='Schlussresultate unten.';", "$('hint').textContent='Résultats finaux ci-dessous.';"),
 ("$('rnum').textContent='Clock stopped'; $('rtime').textContent='Sun 13:00';", "$('rnum').textContent='Uhr gestoppt'; $('rtime').textContent='So 13:00';", "$('rnum').textContent='Chrono arrêté'; $('rtime').textContent='dim 13:00';"),
 ("$('msg').textContent='That duo is not allowed this round.';", "$('msg').textContent='Dieses Duo ist in dieser Runde nicht erlaubt.';", "$('msg').textContent='Ce duo n’est pas autorisé ce tour.';"),
]

def prepare_en(s):
    """Idempotent: hreflang, switch CSS/markup, language-safe clock() for the EN source."""
    if HEAD_TAG not in s:
        s = s.replace('<link rel="icon"', i18n_head() + '<link rel="icon"', 1)
        s = s.replace('</style>', CSS + '</style>', 1)
        s = s.replace('<nav class="hnav">', '<nav class="hnav">\n      ' + switch('en'), 1)
    s = s.replace("if(a.slice(0,3)===b.slice(0,3)) b=b.slice(4);", "if(a.split(' ')[0]===b.split(' ')[0]) b=b.split(' ')[1];")
    return s

def main():
    en = prepare_en(open(SRC, encoding='utf-8').read())
    open(SRC, 'w', encoding='utf-8').write(en)
    for idx, lang in ((1, 'de'), (2, 'fr')):
        out = en.replace(switch('en'), switch(lang))
        for row in T:
            src, dst = row[0], row[idx]
            n = out.count(src)
            assert n >= 1, f'{lang}: not found: {src[:70]}'
            out = out.replace(src, dst)
        os.makedirs(os.path.join(ROOT, lang, 'padel4ever'), exist_ok=True)
        open(os.path.join(ROOT, lang, 'padel4ever', 'index.html'), 'w', encoding='utf-8').write(out)
        print(lang, 'ok', len(out))

if __name__ == '__main__':
    main()
