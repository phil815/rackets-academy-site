"""Rebuilds ski-and-padel.html (EN/FR/DE): dates, online booking (SumUp via Shop Apps Script),
minimum levels and accommodation note. Reviews section is kept as is.
Weekends are listed in CAMPS below (dates from the 'Events - Salgesch' calendar).
Run from the repo root: python3 tools/build_camps.py"""
import re

SCRIPT = 'https://script.google.com/macros/s/AKfycbwLWTwsILcSkAHe9FSKjicU1pUk5s3nxSnS4PQ2Tws2RVejiHjBltJJ8gKpmIe3JLRe/exec'
WA = 'https://wa.me/41772780115?text='
IMG = 'https://www.racketsacademy.ch/images/wix/'
SP = 'https://www.racketsacademy.ch/uploads/ski-padel/'
def imgsrc(i): return SP + i[3:].replace('_DSC', 'ski-padel-') + '.jpg' if i.startswith('SP:') else IMG + i + '.jpg'
GALLERY = ['crew','_DSC7791','_DSC8084','_DSC8386','_DSC7651','_DSC8709','_DSC8531','_DSC7952','_DSC9129','_DSC8416','_DSC8045',
           '_DSC7983','_DSC9403','_DSC8224','_DSC8829','_DSC8015','_DSC8329','_DSC9256','_DSC8618','_DSC8438','_DSC7739',
           '_DSC9170','_DSC8781','_DSC9278','_DSC8250','_DSC9023','_DSC9314']
GAL_T = {'en': ('The weekend in pictures', 'Powder in the morning, padel in the afternoon, spa at night. Tap a photo to enlarge.'),
         'fr': ('Le week-end en images', 'Poudreuse le matin, padel l’après-midi, spa le soir. Touche une photo pour l’agrandir.'),
         'de': ('Das Wochenende in Bildern', 'Pulverschnee am Morgen, Padel am Nachmittag, Spa am Abend. Tippe auf ein Foto zum Vergrössern.')}
GAL_ASSETS = r'''<div class="gal-box" hidden><button class="gal-x" aria-label="Close">&times;</button><button class="gal-prev" aria-label="Previous">&#8249;</button><img alt=""><button class="gal-next" aria-label="Next">&#8250;</button></div>
<style>
.gal{columns:3 260px;column-gap:12px}
.gal-item{display:block;break-inside:avoid;margin-bottom:12px;border-radius:14px;overflow:hidden;cursor:zoom-in}
.gal-item img{width:100%;display:block;transition:transform .3s}
.gal-item:hover img{transform:scale(1.04)}
.gal-box{position:fixed;inset:0;background:rgba(5,15,28,.94);z-index:1000;display:flex;align-items:center;justify-content:center}
.gal-box[hidden]{display:none}
.gal-box img{max-width:94vw;max-height:88vh;border-radius:10px}
.gal-box button{position:absolute;background:rgba(255,255,255,.12);color:#fff;border:0;font-size:2.4rem;line-height:1;width:52px;height:52px;border-radius:50%;cursor:pointer}
.gal-x{top:16px;right:16px}.gal-prev{left:12px}.gal-next{right:12px}
@media(max-width:600px){.gal{columns:2 140px;column-gap:8px}.gal-item{margin-bottom:8px;border-radius:10px}.gal-prev,.gal-next{bottom:20px;top:auto}}
</style>
<script>
(function(){var a=[].slice.call(document.querySelectorAll('.gal-item')),b=document.querySelector('.gal-box'),im=b.querySelector('img'),i=0;
function show(n){i=(n+a.length)%a.length;im.src=a[i].href;b.hidden=false;document.body.style.overflow='hidden';}
function hide(){b.hidden=true;document.body.style.overflow='';}
a.forEach(function(x,n){x.addEventListener('click',function(e){e.preventDefault();show(n);if(window.gtag)gtag('event','gallery_open');});});
b.querySelector('.gal-x').onclick=hide;b.querySelector('.gal-prev').onclick=function(e){e.stopPropagation();show(i-1);};
b.querySelector('.gal-next').onclick=function(e){e.stopPropagation();show(i+1);};
b.addEventListener('click',function(e){if(e.target===b)hide();});
document.addEventListener('keydown',function(e){if(b.hidden)return;if(e.key==='Escape')hide();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1);});
var x0=null;b.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
b.addEventListener('touchend',function(e){if(x0===null)return;var d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>40)show(i+(d<0?1:-1));x0=null;});})();
</script>
'''
CREW_T = {'en': ('Small group, real community', 'Twelve players per weekend, mixed levels and nationalities. You ski together in the morning, play together in the afternoon and share dinner in the evening — most guests leave with new padel partners.', 'Book your place'),
          'fr': ('Petit groupe, vraie communauté', 'Douze joueurs par week-end, niveaux et nationalités mélangés. On skie ensemble le matin, on joue ensemble l’après-midi et on dîne ensemble le soir — la plupart repartent avec de nouveaux partenaires de padel.', 'Réserve ta place'),
          'de': ('Kleine Gruppe, echte Community', 'Zwölf Spieler pro Wochenende, gemischte Levels und Nationalitäten. Morgens gemeinsam auf der Piste, nachmittags auf dem Court, abends am selben Tisch — die meisten fahren mit neuen Padel-Partnern nach Hause.', 'Platz buchen')}
CREW_CSS = r'''<style>.crew-grid{display:grid;grid-template-columns:1.3fr 1fr;gap:32px;align-items:center}.crew-img{width:100%;border-radius:24px;box-shadow:0 12px 30px rgba(11,26,43,.15);transform:rotate(-1.5deg)}@media(max-width:760px){.crew-grid{grid-template-columns:1fr;gap:18px}.crew-img{transform:none}}</style>'''
def crew(lang):
    h, p, c = CREW_T[lang]
    return f'''
<section class="section-tight crew-block">
  <div class="wrap crew-grid">
    <img src="{SP}ski-padel-crew.jpg" alt="Ski &amp;Padel group on the padel court at Rackets Academy" class="crew-img">
    <div><h2>{h}</h2><p class="section-lede">{p}</p><a class="btn btn-green" href="#camp-book">{c}</a></div>
  </div>
</section>
'''+CREW_CSS+'''
'''
def gname(g): return 'ski-padel-' + g.replace('_DSC', '')
def gallery(lang):
    h, p = GAL_T[lang]
    items = ''.join(f'<a href="{SP}{gname(g)}.jpg" class="gal-item"><img src="{SP}{gname(g)}.jpg" alt="Ski &Padel weekend at Rackets Academy" loading="lazy"></a>' for g in GALLERY)
    return f'''
<section class="section-tight" id="gallery">
  <div class="wrap">
    <h2>{h}</h2>
    <p class="section-lede">{p}</p>
    <div class="gal">{items}</div>
  </div>
</section>
'''+GAL_ASSETS+''''''

# id, day numbers, month index (for labels)
CAMPS = [('ski-padel-2027-02-18', 18, 21), ('ski-padel-2027-02-25', 25, 28)]

T = {
'en': dict(
  faq_h='Good to know',
  faq=[('Where does the Ski &Padel weekend take place?', 'At Rackets Academy in Salgesch, Valais (Switzerland). Padel, spa and lodging are in the same building; we ski where the conditions are best: Crans-Montana, Leukerbad, Grimentz-Zinal or the 4 Vallées, all within reach by car. Transport to the slopes is included.'),
       ('How do I get there from London, Paris or Berlin?', 'Fly to Geneva or Zurich. From Geneva Airport the train takes about 2.5 hours, from Zurich Airport about 3 hours. Salgesch station is a 15-minute walk from the Academy, and there is free parking if you come by car.'),
       ('Can I join on my own?', 'Yes. An individual place costs 1\'199 CHF. Rooms are for two, so we pair you with another guest. Groups of 4 pay 999 CHF per person.'),
       ('What level do I need?', 'Skiing: confident parallel turns on all pistes, including red runs — there are no beginner lessons. Padel: Playtomic level 1.5 or higher, so you know the rules and can keep a rally going.'),
       ('What is included and what is not?', 'Included: 3-day ski pass for the resort of the day (Crans-Montana, Leukerbad, Grimentz-Zinal or 4 Vallées), rental skis, poles and boots, daily transport, padel sessions with a coach and a tournament, rental rackets, unlimited spa, 3 nights of lodging, breakfast and dinner. Not included: lunch on the slopes, drinks at the bar and travel to Salgesch.'),
       ('Is the lodging a hotel?', 'No. You stay in simple, sporty shared rooms for two at WYN Skillpark, right next to the courts and the spa. No hotel service, but an unbeatable location.')],
  title='Ski &amp;Padel Weekends Switzerland · Feb 2027 | Rackets Academy',
  desc='Ski &amp;Padel weekends in Valais, 18–21 and 25–28 February 2027: 3 days skiing in the best Valais resorts, padel, spa, lodging and meals. 1199 CHF, groups of 4: 999 CHF per person.',
  h1='Ski &amp;Padel weekends in the Swiss Alps', lede='Skiing wherever the snow is best every morning, padel every afternoon, spa every evening. Two long weekends in February 2027 — 12 places each.',
  chips=['Thu–Sun · 3 nights', '12 places per weekend', 'From 999 CHF'], cta='Choose your weekend',
  mon='Feb', dlabel='Thu {a} – Sun {b} Feb 2027', dsub='Thursday to Sunday · 3 nights · 3 ski days',
  book_h='Book your place', s1='1. Pick your weekend', s2='2. Individual place or with your crew?',
  solo='Individual', solo_note='One place. Rooms are for two — we pair you with another guest.',
  grp='Group of 4', grp_note='Four places, two rooms for your group. Paid in one go.', grp_total='3\'996 CHF total', save='Save 800 CHF',
  pp='per person', go='Book &amp; pay', vat='Prices in CHF, VAT included. Secure card payment via SumUp — confirmation by email.',
  rules_h='Before you book: minimum level', rules_p='The weekend only works if everyone can keep up — on the slopes and on court. Please check honestly.',
  ski_h='Ski', ski_lvl='Intermediate to advanced', ski_p='You ski parallel turns confidently on all pistes, including red runs. There are no beginner lessons — the group skis together.',
  pad_h='Padel', pad_lvl='Playtomic level 1.5 or higher', pad_p='You know the basic rules and can keep a rally going. Afternoon sessions are games and drills with tips from our coach, not a first lesson.',
  stay_h='Sports lodge, not a hotel', stay_p='You sleep in simple, sporty rooms for two at WYN Skillpark, in the same building as our courts and spa. No room service, no minibar — but a location that is hard to beat:',
  stay=['20 seconds from the padel courts and the spa — no cold walks after the sauna', '20 minutes to Crans-Montana and Leukerbad, Zinal and the 4 Vallées within easy reach — transport included', '15 minutes on foot to Salgesch station, free parking on site'],
  inc_h="What's included", inc_p='One price, everything sorted — you just bring your ski clothes.',
  cards=[('SP:_DSC8084', '3 days of skiing', 'We go where the weather takes us: Crans-Montana, Leukerbad, Grimentz-Zinal or the 4 Vallées. 3-day ski pass included.'),
         ('SP:_DSC8709', '3 days of padel', 'Afternoon sessions with tips from an M3 Assistant coach and a tournament on Sunday.'),
         ('SP:_DSC9170', 'Ski equipment', 'Free rental skis, poles and boots from our sponsor Decathlon — travel light.'),
         ('SP:_DSC9314', 'Padel equipment', 'Test different rackets for free, courtesy of our sponsor Wilson.'),
         ('SP:_DSC9403', 'Unlimited spa', 'Finnish sauna, bio-sauna, hammam, jacuzzi, foot baths and relax zone, every evening.'),
         ('98c88169a3e4', 'Lodging', '3 nights in simple shared rooms for two at WYN Skillpark, right next to the courts.'),
         ('cc07951f3023', 'Transport', 'Transport to the ski resort and back is included each day.'),
         ('6af4057e8e3f', 'Meals', 'Breakfast and dinner included, lunch on the slopes is on you. Free water and coffee all day.'),
         ('b66024f48ebe', 'Gym', 'Functional training area for warm-ups, stretching and yoga after a day of sport.')],
  it_h='The long weekend', it=[('Thursday', '18:00 Get-to-know<br>19:30 Dinner'),
       ('Friday &amp; Saturday', '7:00 Breakfast<br>7:45 Leave for the slopes<br>8:45 Skiing<br>15:30 Back at the Academy<br>17:00 Padel<br>20:30 Dinner<br>21:00 Spa &amp; unwind'),
       ('Sunday', '7:00 Breakfast<br>7:45 Leave for the slopes<br>8:45 Skiing<br>15:30 Back at the Academy<br>16:30 Padel tournament<br>18:00 Departure')],
  final_h='12 places per weekend.', final_p='Questions about levels, rooms or groups? Message Mario on WhatsApp.', wa_cta='Ask on WhatsApp',
  wa_msg='Hola! I have a question about the Ski &Padel weekends.',
  m_name='Your name', m_email='Your email <span style="font-weight:400; opacity:.7;">(confirmation is sent here)</span>', m_phone='Mobile number <span style="font-weight:400; opacity:.7;">(for last-minute updates)</span>',
  m_group='Names of the other 3 participants', m_notes='Anything we should know? <span style="font-weight:400; opacity:.7;">(optional — diet, arrival time)</span>',
  m_lvl='Everyone in my booking meets the minimum ski and padel level.', m_stay='I understand the rooms are simple shared sports lodging, not a hotel.',
  m_btn='Continue to payment'),
'fr': dict(
  faq_h='Bon à savoir',
  faq=[('Où a lieu le week-end Ski &Padel ?', 'À la Rackets Academy à Salgesch, en Valais (Suisse). Padel, spa et logement sont dans le même bâtiment ; on skie là où les conditions sont les meilleures : Crans-Montana, Loèche-les-Bains, Grimentz-Zinal ou les 4 Vallées, toutes accessibles en voiture. Le transport aux pistes est inclus.'),
       ('Comment venir depuis Paris, Londres ou Berlin ?', 'En avion jusqu\'à Genève ou Zurich. Depuis l\'aéroport de Genève, le train met environ 2h30, depuis l\'aéroport de Zurich environ 3 heures. La gare de Salgesch est à 15 minutes à pied de l\'Academy, parking gratuit si tu viens en voiture.'),
       ('Puis-je venir seul·e ?', 'Oui. Une place individuelle coûte 1\'199 CHF. Les chambres sont pour deux, on te met avec un autre participant. Les groupes de 4 paient 999 CHF par personne.'),
       ('Quel niveau faut-il ?', 'Ski : virages parallèles sûrs sur toutes les pistes, y compris les rouges — pas de cours débutant. Padel : niveau Playtomic 1.5 ou plus, tu connais les règles et tu tiens un échange.'),
       ('Qu\'est-ce qui est inclus ou non ?', 'Inclus : forfait 3 jours pour la station du jour (Crans-Montana, Loèche-les-Bains, Grimentz-Zinal ou 4 Vallées), skis, bâtons et chaussures de location, transport quotidien, sessions de padel avec coach et tournoi, raquettes, spa illimité, 3 nuits, petit-déjeuner et souper. Non inclus : le dîner sur les pistes, les boissons au bar et le voyage jusqu\'à Salgesch.'),
       ('Le logement est-il un hôtel ?', 'Non. Tu dors dans des chambres simples et sportives pour deux au WYN Skillpark, juste à côté des terrains et du spa. Pas de service hôtelier, mais un emplacement imbattable.')],
  title='Week-end Ski &amp;Padel en Suisse · février 2027 | Rackets Academy',
  desc='Week-ends Ski &amp;Padel en Valais, 18–21 et 25–28 février 2027 : 3 jours de ski dans les meilleures stations du Valais, padel, spa, logement et repas. 1199 CHF, groupe de 4 : 999 CHF par personne.',
  h1='Week-ends Ski &amp;Padel dans les Alpes suisses', lede='Ski le matin là où la neige est la meilleure, padel l\'après-midi, spa le soir. Deux longs week-ends en février 2027 — 12 places chacun.',
  chips=['Jeu–dim · 3 nuits', '12 places par week-end', 'Dès 999 CHF'], cta='Choisir mon week-end',
  mon='fév', dlabel='Jeu {a} – dim {b} février 2027', dsub='Du jeudi au dimanche · 3 nuits · 3 jours de ski',
  book_h='Réserve ta place', s1='1. Choisis ton week-end', s2='2. Place individuelle ou avec ta bande ?',
  solo='Individuel', solo_note='Une place. Les chambres sont pour deux — on te met avec un autre participant.',
  grp='Groupe de 4', grp_note='Quatre places, deux chambres pour ton groupe. Payé en une fois.', grp_total='3\'996 CHF au total', save='800 CHF d\'économie',
  pp='par personne', go='Réserver &amp; payer', vat='Prix en CHF, TVA incluse. Paiement sécurisé par carte via SumUp — confirmation par e-mail.',
  rules_h='Avant de réserver : niveau minimum', rules_p='Le week-end ne fonctionne que si tout le monde suit — sur les pistes comme sur le terrain. Merci de vérifier honnêtement.',
  ski_h='Ski', ski_lvl='Intermédiaire à avancé', ski_p='Tu skies en virages parallèles avec aisance sur toutes les pistes, y compris les rouges. Pas de cours débutant — le groupe skie ensemble.',
  pad_h='Padel', pad_lvl='Niveau Playtomic 1.5 ou plus', pad_p='Tu connais les règles de base et tu tiens un échange. Les sessions de l\'après-midi sont des matchs et exercices avec les conseils de notre coach, pas une première leçon.',
  stay_h='Un lodge sportif, pas un hôtel', stay_p='Tu dors dans des chambres simples et sportives pour deux au WYN Skillpark, dans le même bâtiment que nos terrains et le spa. Pas de room service, pas de minibar — mais un emplacement imbattable :',
  stay=['20 secondes des terrains de padel et du spa — pas de marche dans le froid après le sauna', '20 minutes de Crans-Montana et Loèche-les-Bains, Zinal et les 4 Vallées à portée — transport inclus', '15 minutes à pied de la gare de Salgesch, parking gratuit sur place'],
  inc_h='Ce qui est inclus', inc_p='Un prix, tout est organisé — tu n\'apportes que tes habits de ski.',
  cards=[('SP:_DSC8084', '3 jours de ski', 'On va là où la météo nous emmène : Crans-Montana, Loèche-les-Bains, Grimentz-Zinal ou les 4 Vallées. Forfait 3 jours inclus.'),
         ('SP:_DSC8709', '3 jours de padel', 'Sessions l\'après-midi avec les conseils d\'un coach M3 Assistant et un tournoi le dimanche.'),
         ('SP:_DSC9170', 'Matériel de ski', 'Skis, bâtons et chaussures de location offerts par notre sponsor Decathlon — voyage léger.'),
         ('SP:_DSC9314', 'Matériel de padel', 'Teste différentes raquettes gratuitement, grâce à notre sponsor Wilson.'),
         ('SP:_DSC9403', 'Spa illimité', 'Sauna finlandais, bio-sauna, hammam, jacuzzi, bains de pieds et espace détente, chaque soir.'),
         ('98c88169a3e4', 'Logement', '3 nuits en chambres simples pour deux au WYN Skillpark, juste à côté des terrains.'),
         ('cc07951f3023', 'Transport', 'Le trajet aller-retour vers la station est inclus chaque jour.'),
         ('6af4057e8e3f', 'Repas', 'Petit-déjeuner et souper inclus, le dîner sur les pistes est à ta charge. Eau et café offerts toute la journée.'),
         ('b66024f48ebe', 'Gym', 'Espace de training fonctionnel pour l\'échauffement, les étirements et le yoga après le sport.')],
  it_h='Le long week-end', it=[('Jeudi', '18h00 Apéro de bienvenue<br>19h30 Souper'),
       ('Vendredi &amp; samedi', '7h00 Petit-déjeuner<br>7h45 Départ pour les pistes<br>8h45 Ski<br>15h30 Retour à l\'Academy<br>17h00 Padel<br>20h30 Souper<br>21h00 Spa &amp; détente'),
       ('Dimanche', '7h00 Petit-déjeuner<br>7h45 Départ pour les pistes<br>8h45 Ski<br>15h30 Retour à l\'Academy<br>16h30 Tournoi de padel<br>18h00 Départ')],
  final_h='12 places par week-end.', final_p='Des questions sur le niveau, les chambres ou les groupes ? Écris à Mario sur WhatsApp.', wa_cta='Demander sur WhatsApp',
  wa_msg='Hola ! J\'ai une question sur les week-ends Ski &Padel.',
  m_name='Ton nom', m_email='Ton e-mail <span style="font-weight:400; opacity:.7;">(la confirmation sera envoyée ici)</span>', m_phone='Numéro de mobile <span style="font-weight:400; opacity:.7;">(pour les infos de dernière minute)</span>',
  m_group='Noms des 3 autres participants', m_notes='Quelque chose à savoir ? <span style="font-weight:400; opacity:.7;">(facultatif — alimentation, heure d\'arrivée)</span>',
  m_lvl='Toutes les personnes de ma réservation ont le niveau minimum en ski et en padel.', m_stay='J\'ai compris que les chambres sont un logement sportif simple et partagé, pas un hôtel.',
  m_btn='Continuer vers le paiement'),
'de': dict(
  faq_h='Gut zu wissen',
  faq=[('Wo findet das Ski &Padel Wochenende statt?', 'In der Rackets Academy in Salgesch, Wallis (Schweiz). Padel, Spa und Unterkunft sind im selben Gebäude; Skifahren dort, wo die Bedingungen am besten sind: Crans-Montana, Leukerbad, Grimentz-Zinal oder 4 Vallées, alles gut mit dem Auto erreichbar. Der Transport zur Piste ist inklusive.'),
       ('Wie komme ich aus Berlin, London oder Paris hin?', 'Flug nach Genf oder Zürich. Ab Flughafen Genf dauert die Zugfahrt rund 2,5 Stunden, ab Flughafen Zürich rund 3 Stunden. Der Bahnhof Salgesch liegt 15 Gehminuten von der Academy, mit dem Auto gibt es gratis Parkplätze.'),
       ('Kann ich alleine mitkommen?', 'Ja. Ein Einzelplatz kostet 1\'199 CHF. Die Zimmer sind für zwei, wir teilen dich mit einem anderen Gast ein. 4er-Gruppen zahlen 999 CHF pro Person.'),
       ('Welches Niveau brauche ich?', 'Ski: sicher parallel auf allen Pisten, auch auf roten — es gibt keinen Anfängerkurs. Padel: Playtomic-Level 1.5 oder höher, du kennst die Regeln und kannst einen Ballwechsel halten.'),
       ('Was ist inklusive, was nicht?', 'Inklusive: 3-Tages-Skipass für das jeweilige Skigebiet (Crans-Montana, Leukerbad, Grimentz-Zinal oder 4 Vallées), Mietski, Stöcke und Schuhe, täglicher Transport, Padel-Sessions mit Coach und Turnier, Rackets, unbegrenzt Spa, 3 Nächte, Frühstück und Abendessen. Nicht inklusive: Mittagessen auf der Piste, Getränke an der Bar und die Anreise nach Salgesch.'),
       ('Ist die Unterkunft ein Hotel?', 'Nein. Du schläfst in einfachen, sportlichen Zimmern für zwei im WYN Skillpark, direkt neben den Courts und dem Spa. Kein Hotelservice, dafür eine unschlagbare Lage.')],
  title='Ski &amp;Padel Wochenende Schweiz · Feb. 2027 | Rackets Academy',
  desc='Ski &amp;Padel Wochenenden im Wallis, 18.–21. und 25.–28. Februar 2027: 3 Tage Skifahren in den besten Walliser Skigebieten, Padel, Spa, Unterkunft und Essen. 1199 CHF, 4er-Gruppe: 999 CHF pro Person.',
  h1='Ski &amp;Padel Wochenenden in den Schweizer Alpen', lede='Morgens Skifahren, wo der Schnee am besten ist, nachmittags Padel, abends Spa. Zwei lange Wochenenden im Februar 2027 — je 12 Plätze.',
  chips=['Do–So · 3 Nächte', '12 Plätze pro Wochenende', 'Ab 999 CHF'], cta='Wochenende wählen',
  mon='Feb', dlabel='Do {a}. – So {b}. Februar 2027', dsub='Donnerstag bis Sonntag · 3 Nächte · 3 Skitage',
  book_h='Platz buchen', s1='1. Wochenende wählen', s2='2. Einzelplatz oder mit deiner Crew?',
  solo='Einzelplatz', solo_note='Ein Platz. Die Zimmer sind für zwei — wir teilen dich mit einem anderen Gast ein.',
  grp='4er-Gruppe', grp_note='Vier Plätze, zwei Zimmer für eure Gruppe. In einem Mal bezahlt.', grp_total='3\'996 CHF total', save='800 CHF gespart',
  pp='pro Person', go='Buchen &amp; bezahlen', vat='Preise in CHF inkl. MWST. Sichere Kartenzahlung über SumUp — Bestätigung per E-Mail.',
  rules_h='Vor dem Buchen: Mindestniveau', rules_p='Das Wochenende funktioniert nur, wenn alle mithalten — auf der Piste und auf dem Court. Bitte ehrlich prüfen.',
  ski_h='Ski', ski_lvl='Mittel bis fortgeschritten', ski_p='Du fährst sicher parallel auf allen Pisten, auch auf roten. Es gibt keinen Anfängerkurs — die Gruppe fährt zusammen.',
  pad_h='Padel', pad_lvl='Playtomic-Level 1.5 oder höher', pad_p='Du kennst die Grundregeln und kannst einen Ballwechsel halten. Nachmittags gibt es Spiele und Drills mit Tipps vom Coach, keine erste Lektion.',
  stay_h='Sport-Lodge, kein Hotel', stay_p='Du schläfst in einfachen, sportlichen Zimmern für zwei im WYN Skillpark, im selben Gebäude wie unsere Courts und das Spa. Kein Zimmerservice, keine Minibar — dafür eine Lage, die kaum zu schlagen ist:',
  stay=['20 Sekunden zu den Padel-Courts und zum Spa — kein kalter Weg nach der Sauna', '20 Minuten nach Crans-Montana und Leukerbad, Zinal und die 4 Vallées in Reichweite — Transport inklusive', '15 Minuten zu Fuss zum Bahnhof Salgesch, gratis Parkplätze vor Ort'],
  inc_h='Was inklusive ist', inc_p='Ein Preis, alles organisiert — du bringst nur deine Skikleider mit.',
  cards=[('SP:_DSC8084', '3 Tage Skifahren', 'Wir fahren dorthin, wo das Wetter am besten ist: Crans-Montana, Leukerbad, Grimentz-Zinal oder 4 Vallées. 3-Tages-Skipass inklusive.'),
         ('SP:_DSC8709', '3 Tage Padel', 'Nachmittags Sessions mit Tipps von einem M3-Assistant-Coach und ein Turnier am Sonntag.'),
         ('SP:_DSC9170', 'Skiausrüstung', 'Gratis Mietski, Stöcke und Schuhe von unserem Sponsor Decathlon — reise mit leichtem Gepäck.'),
         ('SP:_DSC9314', 'Padelausrüstung', 'Teste verschiedene Rackets gratis, dank unserem Sponsor Wilson.'),
         ('SP:_DSC9403', 'Unbegrenzt Spa', 'Finnische Sauna, Bio-Sauna, Hammam, Jacuzzi, Fussbäder und Ruhezone, jeden Abend.'),
         ('98c88169a3e4', 'Unterkunft', '3 Nächte in einfachen Zimmern für zwei im WYN Skillpark, direkt neben den Courts.'),
         ('cc07951f3023', 'Transport', 'Fahrt ins Skigebiet und zurück ist jeden Tag inklusive.'),
         ('6af4057e8e3f', 'Essen', 'Frühstück und Abendessen inklusive, das Mittagessen auf der Piste zahlst du selbst. Wasser und Kaffee gratis.'),
         ('b66024f48ebe', 'Gym', 'Functional-Training-Bereich zum Aufwärmen, Dehnen und für Yoga nach dem Sport.')],
  it_h='Das lange Wochenende', it=[('Donnerstag', '18:00 Kennenlernen<br>19:30 Abendessen'),
       ('Freitag &amp; Samstag', '7:00 Frühstück<br>7:45 Abfahrt zur Piste<br>8:45 Skifahren<br>15:30 Zurück in der Academy<br>17:00 Padel<br>20:30 Abendessen<br>21:00 Spa &amp; Entspannen'),
       ('Sonntag', '7:00 Frühstück<br>7:45 Abfahrt zur Piste<br>8:45 Skifahren<br>15:30 Zurück in der Academy<br>16:30 Padel-Turnier<br>18:00 Abreise')],
  final_h='12 Plätze pro Wochenende.', final_p='Fragen zu Niveau, Zimmern oder Gruppen? Schreib Mario auf WhatsApp.', wa_cta='Auf WhatsApp fragen',
  wa_msg='Hola! Ich habe eine Frage zu den Ski &Padel Wochenenden.',
  m_name='Dein Name', m_email='Deine E-Mail <span style="font-weight:400; opacity:.7;">(Bestätigung geht hierhin)</span>', m_phone='Handynummer <span style="font-weight:400; opacity:.7;">(für kurzfristige Infos)</span>',
  m_group='Namen der anderen 3 Teilnehmenden', m_notes='Sollen wir etwas wissen? <span style="font-weight:400; opacity:.7;">(optional — Ernährung, Ankunftszeit)</span>',
  m_lvl='Alle Personen meiner Buchung erfüllen das Mindestniveau in Ski und Padel.', m_stay='Mir ist klar, dass die Zimmer eine einfache, geteilte Sport-Unterkunft sind und kein Hotel.',
  m_btn='Weiter zur Zahlung'),
}


def body(t, pre):
    from urllib.parse import quote
    dates = ''.join(f'''
        <label class="camp-opt">
          <input type="radio" name="camp" value="{cid}" data-label="{t['dlabel'].format(a=a, b=b)}"{' checked' if i == 0 else ''}>
          <span class="camp-tile camp-ticket">
            <span class="camp-day"><b>{a}</b><small>{t['mon']}</small></span>
            <strong>{t['dlabel'].format(a=a, b=b)}</strong>
            <span class="camp-spots">{t['dsub']}</span>
          </span>
        </label>''' for i, (cid, a, b) in enumerate(CAMPS))
    cards = ''.join(f'''
      <div class="card">
        <img src="{imgsrc(img)}" alt="{h}" loading="lazy" style="width:100%; height:140px; object-fit:cover; border-radius:12px; margin-bottom:14px;">
        <h3>{h}</h3>
        <p>{p}</p>
      </div>''' for img, h, p in t['cards'])
    it = ''.join(f'''
      <div class="card">
        <h3>{d}</h3>
        <p>{p}</p>
      </div>''' for d, p in t['it'])
    stay = ''.join(f'<li>{x}</li>' for x in t['stay'])
    chips = ''.join(f'<span>{c}</span>' for c in t['chips'])
    wa = WA + quote(t['wa_msg'])
    return f'''
<section class="hero" style="background-image:linear-gradient(160deg, rgba(0,119,222,.82), rgba(4,91,171,.88)), url('https://www.racketsacademy.ch/uploads/ski-padel/ski-padel-7791.jpg'); background-size:cover; background-position:center;">
  <span class="ball b1"></span><span class="ball b2"></span><span class="ball b3"></span>
  <div class="wrap hero-inner">
    <h1>{t['h1']}</h1>
    <p class="lede">{t['lede']}</p>
    <div class="camp-chips">{chips}</div>
    <div class="hero-actions"><a class="btn btn-green" href="#camp-book">{t['cta']}</a></div>
  </div>
</section>

{crew(next(k for k, v in T.items() if v is t))}
<section class="section-tight camp-book" id="camp-book">
  <div class="wrap">
    <h2>{t['book_h']}</h2>
    <p class="camp-step">{t['s1']}</p>
    <div class="camp-dates">{dates}
    </div>
    <p class="camp-step">{t['s2']}</p>
    <div class="camp-packs">
      <label class="camp-opt">
        <input type="radio" name="pack" value="single" checked>
        <span class="camp-tile">
          <span class="camp-pack-name">{t['solo']}</span>
          <span class="camp-pack-price">1'199 CHF <small>{t['pp']}</small></span>
          <span class="camp-pack-note">{t['solo_note']}</span>
        </span>
      </label>
      <label class="camp-opt">
        <input type="radio" name="pack" value="group4">
        <span class="camp-tile">
          <span class="camp-pack-name">{t['grp']}</span>
          <span class="camp-pack-price">999 CHF <small>{t['pp']}</small></span>
          <span class="camp-pack-note">{t['grp_note']} {t['grp_total']}.</span>
          <span class="camp-save">{t['save']}</span>
        </span>
      </label>
    </div>
    <div class="camp-summary">
      <div><p id="camp-sum-what"></p><p class="camp-total" id="camp-sum-total"></p></div>
      <button type="button" class="btn btn-green" id="camp-go" onclick="openCampModal()">{t['go']}</button>
    </div>
    <p style="margin:12px 0 0; font-size:.88rem; color:#045bab;">{t['vat']}</p>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['rules_h']}</h2>
    <p class="section-lede">{t['rules_p']}</p>
    <div class="camp-rules">
      <div class="camp-rule"><h3>⛷️ {t['ski_h']}</h3><span class="camp-level">{t['ski_lvl']}</span><p>{t['ski_p']}</p></div>
      <div class="camp-rule"><h3>🎾 {t['pad_h']}</h3><span class="camp-level">{t['pad_lvl']}</span><p>{t['pad_p']}</p></div>
    </div>
    <div class="camp-stay">
      <h3>🛏️ {t['stay_h']}</h3>
      <p>{t['stay_p']}</p>
      <ul>{stay}</ul>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>{t['inc_h']}</h2>
    <p class="section-lede">{t['inc_p']}</p>
    <div class="grid-3">{cards}
    </div>
  </div>
</section>

{gallery(next(k for k, v in T.items() if v is t))}
<section class="section-tight" style="background:var(--paper);">
  <div class="wrap">
    <h2>{t['it_h']}</h2>
    <div class="grid-3">{it}
    </div>
  </div>
</section>
'''


def final(t):
    from urllib.parse import quote
    faq = ''.join(f'<details class="card" style="margin-bottom:12px;"><summary style="font-weight:700; color:var(--blue-dark); cursor:pointer;">{q}</summary><p style="margin-top:10px;">{a}</p></details>' for q, a in t['faq'])
    return f'''<section class="section-tight">
  <div class="wrap" style="max-width:760px;">
    <h2>{t['faq_h']}</h2>
    {faq}
  </div>
</section>

<section class="section-tight" style="text-align:center;">
  <div class="wrap">
    <h2>{t['final_h']}</h2>
    <p class="section-lede" style="margin-left:auto; margin-right:auto;">{t['final_p']}</p>
    <div class="hero-actions" style="justify-content:center;">
      <a class="btn btn-green" href="#camp-book">{t['go']}</a>
      <a class="btn" style="background:var(--blue); color:#fff;" href="{WA + quote(t['wa_msg'])}" target="_blank" rel="noopener">{t['wa_cta']}</a>
    </div>
  </div>
</section>

<div class="buy-modal-overlay" id="buy-modal-overlay">
  <div class="buy-modal">
    <button type="button" class="buy-modal-close" id="buy-modal-close" aria-label="Close">&times;</button>
    <h3 id="buy-modal-title"></h3>
    <div class="buy-modal-price" id="buy-modal-price"></div>
    <form id="buy-modal-form" class="shop-form" method="POST" action="{SCRIPT}" target="_blank">
      <input type="hidden" name="formType" value="camp">
      <input type="hidden" name="campId" id="modal-campId">
      <input type="hidden" name="campPackage" id="modal-campPackage">
      <input type="hidden" name="price" id="modal-price">
      <label class="shop-field">{t['m_name']}<input type="text" name="buyerName" required autocomplete="name"></label>
      <label class="shop-field">{t['m_email']}<input type="email" name="buyerEmail" required autocomplete="email"></label>
      <label class="shop-field">{t['m_phone']}<input type="tel" name="phone" required autocomplete="tel"></label>
      <label class="shop-field" id="modal-group-wrap" style="display:none;">{t['m_group']}<textarea name="participants" rows="3" maxlength="300"></textarea></label>
      <label class="shop-field">{t['m_notes']}<textarea name="notes" rows="2" maxlength="300"></textarea></label>
      <label class="camp-check"><input type="checkbox" name="levelOk" value="yes" required><span>{t['m_lvl']}</span></label>
      <label class="camp-check"><input type="checkbox" name="lodgingOk" value="yes" required><span>{t['m_stay']}</span></label>
      <button type="submit" class="btn btn-green" style="width:100%; text-align:center;">{t['m_btn']}</button>
    </form>
  </div>
</div>

'''


for lang, t in T.items():
    f = ('' if lang == 'en' else lang + '/') + 'ski-and-padel.html'
    pre = '' if lang == 'en' else '../'
    s = open(f).read()
    # main block: after header .. up to the reviews section
    a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
    rev = s.index('<div class="wrap" style="max-width:700px; text-align:center;">')
    b = s.rindex('<section', 0, rev)
    s = s[:a] + body(t, pre) + '\n' + s[b:]
    # tail: everything between the end of the reviews section and the footer
    endrev = s.index('</section>', s.index('max-width:700px; text-align:center;')) + len('</section>')
    foot = s.index('<footer')
    s = s[:endrev] + '\n\n' + final(t) + s[foot:]
    s = re.sub(r'<title>.*?</title>', '<title>' + t['title'] + '</title>', s, count=1, flags=re.S)
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + t['desc'] + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + t['title'] + '"', s)
    s = re.sub(r'styles\.css\?v=\d+', 'styles.css?v=35', s)
    s = re.sub(r'<script src="(\.\./)?camps\.js[^"]*"></script>\n', '', s)
    s = re.sub(r'(<script src="(?:\.\./)?nav\.js\?v=)\d+("></script>)', r'\g<1>22\2', s)
    s = s.replace('</body>', f'<script src="{pre}camps.js?v=2"></script>\n</body>', 1)
    import json
    url = 'https://www.racketsacademy.ch/' + ('' if lang == 'en' else lang + '/') + 'ski-and-padel.html'
    ev = [{'@type': 'Event', 'name': 'Ski &Padel — ' + t['dlabel'].format(a=a2, b=b2),
           'startDate': '2027-02-%02dT18:00:00+01:00' % a2, 'endDate': '2027-02-%02dT18:00:00+01:00' % b2,
           'eventStatus': 'https://schema.org/EventScheduled', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
           'maximumAttendeeCapacity': 12, 'image': IMG + '96f05bf2d108.jpg', 'description': t['desc'].replace('&amp;', '&'),
           'location': {'@type': 'Place', 'name': 'Rackets Academy Salgesch', 'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressRegion': 'VS', 'addressCountry': 'CH'}},
           'organizer': {'@type': 'Organization', 'name': 'Rackets Academy', 'url': 'https://www.racketsacademy.ch/'},
           'offers': [{'@type': 'Offer', 'price': '1199', 'priceCurrency': 'CHF', 'url': url + '#camp-book', 'availability': 'https://schema.org/InStock', 'validFrom': '2026-10-01'},
                      {'@type': 'Offer', 'name': 'Group of 4 (per person)', 'price': '999', 'priceCurrency': 'CHF', 'url': url + '#camp-book', 'availability': 'https://schema.org/InStock', 'validFrom': '2026-10-01'}]}
          for cid, a2, b2 in CAMPS]
    ev.append({'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]})
    ev.append({'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Rackets Academy', 'item': 'https://www.racketsacademy.ch/' + ('' if lang == 'en' else lang + '/')}, {'@type': 'ListItem', 'position': 2, 'name': 'Ski &Padel', 'item': url}]})
    s = re.sub(r'<script type="application/ld\+json" id="ld-camps">.*?</script>\n', '', s, flags=re.S)
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-camps">' + json.dumps({'@context': 'https://schema.org', '@graph': ev}, ensure_ascii=False) + '</script>\n</head>', 1)
    open(f, 'w').write(s)
    print(f, 'ok')
