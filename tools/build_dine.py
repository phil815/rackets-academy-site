"""Padel+Dine feat. Instinct Amazonia (padel-dine.html, EN/FR/DE), built from the spa page shell.
Tickets: Tournament + Dinner Party 79 CHF pp (teams of 2, 48 places), Dinner Party 59 CHF (52 places).
Booking via dine.js -> Shop Apps Script (Events.gs, formType=ticket) -> SumUp pop-up."""
import re, json
SLUG = 'padel-dine.html'
ACTION = 'https://script.google.com/macros/s/AKfycbwLWTwsILcSkAHe9FSKjicU1pUk5s3nxSnS4PQ2Tws2RVejiHjBltJJ8gKpmIe3JLRe/exec'
WIX = 'https://static.wixstatic.com/media/'
def wix(mid, name, w=800, h=1000):
    return f'{WIX}{mid}/v1/fill/w_{w},h_{h},al_c,q_80/{name}'
FOOD = [wix('a3a56a_3d44b71bb78e4869aba5342b2dd60454~mv2.webp', 'amazonia-1.webp'),
        wix('a3a56a_44ff6cea50334f278473bf61bc80cc1c~mv2.webp', 'amazonia-2.webp'),
        wix('a3a56a_e69ddbcf49a54732849652269a652a49~mv2.webp', 'amazonia-3.webp'),
        wix('a3a56a_b164d8caf46c4237835f7359454cc681~mv2.webp', 'amazonia-4.webp'),
        wix('a3a56a_aca03e7661334ba591f0fb2fd96f9050~mv2.webp', 'amazonia-5.webp'),
        wix('a3a56a_777febb127754a2092bc5caebadbc802~mv2.webp', 'amazonia-6.webp')]
COCKTAIL = wix('a3a56a_df0072226b254c45aa0b4cb9b11f866d~mv2.webp', 'cocktail.webp', 900, 900)
LEAVES = wix('a3a56a_52c8e9bfce6440ab90806a235307620e~mv2.webp', 'leaves.webp', 1600, 600)

T = {
'fr': dict(
  title='Padel+Dine feat. Instinct Amazonia · 7 novembre | Rackets Academy',
  desc="Samedi 7 novembre 2026 à Salgesch : tournoi de padel en équipe de 2, buffet signature nikkei d'Instinct Amazonia et soirée DJ jusqu'à 2h. Tournoi + Dinner Party 79 CHF, Dinner Party 59 CHF.",
  kicker='Rackets Academy × Instinct Amazonia', h1='Padel+Dine', h1b='feat. Instinct Amazonia',
  lede="Tournoi de padel le jour, Dinner Party le soir. Buffet signature nikkei, DJ et ambiance jungle jusqu'à 2h du matin.",
  chips=['Samedi 7 novembre 2026', '10h – 2h', 'Salgesch'], cta='Prendre mes billets', cta2='Le programme',
  concept_h='Un nouveau concept : jouer, manger, danser.',
  concept_p="On réunit le padel et la cuisine d'Instinct Amazonia, le restaurant nikkei de Granges, pour une journée qui ne s'arrête pas au dernier point. Tu joues le tournoi avec ton ou ta partenaire, puis tout le monde se retrouve pour la Dinner Party.",
  tk_h='Deux billets, une seule soirée',
  t1_name='Tournoi + Dinner Party', t1_price='79 CHF', t1_unit='par personne', t1_note="Inscription en équipe de 2 · 158 CHF par équipe · 48 places",
  t1_inc=['Tournoi : qualifications puis tableau final', 'Balles incluses', 'Buffet signature Instinct Amazonia', '1 boisson incluse', 'Soirée DJ jusqu’à 2h'],
  t2_name='Dinner Party', t2_price='59 CHF', t2_unit='par personne', t2_note='Pour celles et ceux qui viennent pour la soirée · 52 places',
  t2_inc=['Buffet signature Instinct Amazonia', '1 boisson incluse', 'Soirée DJ jusqu’à 2h'],
  extra='Raquettes à louer sur place. Autres boissons au bar.',
  prog_h='Le programme', prog=[('10h', 'Accueil et qualifications du tournoi'), ('Après-midi', 'Tableau final et remise des prix'), ('Soir', 'Dinner Party : buffet signature Instinct Amazonia'), ('Jusqu’à 2h', 'Soirée DJ')],
  food_h='Le buffet signature', food_p='Une sélection généreuse aux influences nikkei : finger food à partager et plats chauds à savourer en assiette.',
  food=[('Côté froid', 'Sushis, salades, bouchées aux saveurs nikkei et autres créations froides'), ('À partager', 'Karaage croustillant, baos et autres spécialités de la maison'), ('Côté chaud', 'Ribs de porc cuits à basse température, curry de poulet, poulet satay, viandes grillées'), ('Accompagnements', 'Riz sauté, légumes sautés et autres accompagnements')],
  food_cap='Sélection indicative, la composition finale dépend des produits de saison. Photos : Instinct Amazonia.',
  bar_h='Le bar', bar_p='Une boisson est incluse dans ton billet. Ensuite, le bar est tenu par l’équipe d’Instinct Amazonia :',
  bar=[('Sangria au verre', '8 CHF'), ('Pichet de sangria à partager', '29 CHF'), ('Apéritifs et cocktails : Spritz, Suze…', '10 CHF'), ('Vodka–Red Bull, whisky–coca, rhum–coca…', '12 CHF')],
  bar_cap='Bières, vins et boissons sans alcool également disponibles. Prix indicatifs.',
  book_h='Réserve tes billets', step1='1. Choisis ton billet', qty_l='Nombre de billets', go='Réserver & payer',
  pay_note='Prix en CHF, TVA incluse. Paiement sécurisé par carte via SumUp, confirmation par e-mail. Remboursement possible jusqu’au dimanche 1er novembre 2026.',
  partner_h='Instinct Amazonia', partner_p='Cuisine nikkei, food & party : le restaurant de Granges marie les saveurs japonaises et péruviennes, avec cocktails créatifs et ambiance festive. Pour Padel+Dine, toute l’équipe vient cuisiner chez nous.', partner_a='Découvrir le restaurant',
  faq_h='Bon à savoir',
  faq=[('Comment fonctionne le tournoi ?', 'Tu t’inscris en équipe de 2. Le matin, on joue les qualifications, puis les équipes passent dans le tableau final. Les balles sont fournies.'),
       ('Je n’ai pas de raquette, c’est grave ?', 'Pas du tout : tu peux louer une raquette sur place.'),
       ('Je peux venir seulement pour la soirée ?', 'Oui, avec le billet Dinner Party à 59 CHF : buffet signature, une boisson et la soirée DJ.'),
       ('Et si j’ai une allergie ?', 'Indique-la dans le formulaire de réservation, on la transmet à la cuisine.'),
       ('Puis-je annuler ?', 'Oui, remboursement possible jusqu’au dimanche 1er novembre 2026. Écris-nous sur WhatsApp ou par e-mail. Après cette date, les billets ne sont plus remboursés.'),
       ('Où cela se passe-t-il ?', 'À la Rackets Academy de Salgesch, Littenstrasse 30, 3970 Salgesch (5 min de Sierre). Parking gratuit.')],
  final_h='Samedi 7 novembre. On joue, on mange, on danse.', final_p='Tournoi + Dinner Party 79 CHF · Dinner Party 59 CHF · Salgesch',
  m_name='Ton nom', m_mail='Ton e-mail', m_mail2='(la confirmation arrive ici)', m_tel='Numéro de mobile', m_tel2='(pour les infos du jour J)',
  m_people='Noms des participant·es', m_notes='Allergies ou remarques ?', m_notes2='(facultatif)', m_ok='J’ai lu les conditions : remboursement possible jusqu’au dimanche 1er novembre 2026.', m_go='Continuer vers le paiement',
  cap1='48 places', cap2='52 places', t1_sub='Équipe de 2', t2_sub='Billet individuel'),
'de': dict(
  title='Padel+Dine feat. Instinct Amazonia · 7. November | Rackets Academy',
  desc='Samstag, 7. November 2026 in Salgesch: Padelturnier im 2er-Team, Nikkei-Signature-Buffet von Instinct Amazonia und DJ-Party bis 2 Uhr. Turnier + Dinner Party 79 CHF, Dinner Party 59 CHF.',
  kicker='Rackets Academy × Instinct Amazonia', h1='Padel+Dine', h1b='feat. Instinct Amazonia',
  lede='Tagsüber Padelturnier, abends Dinner Party. Nikkei-Signature-Buffet, DJ und Jungle-Vibes bis 2 Uhr morgens.',
  chips=['Samstag, 7. November 2026', '10 – 2 Uhr', 'Salgesch'], cta='Tickets sichern', cta2='Zum Programm',
  concept_h='Ein neues Konzept: spielen, essen, tanzen.',
  concept_p='Wir bringen Padel und die Küche von Instinct Amazonia zusammen, dem Nikkei-Restaurant aus Granges. Ein Tag, der nicht mit dem letzten Punkt endet: Du spielst das Turnier mit deinem Partner oder deiner Partnerin, danach treffen sich alle zur Dinner Party.',
  tk_h='Zwei Tickets, ein Abend',
  t1_name='Turnier + Dinner Party', t1_price='79 CHF', t1_unit='pro Person', t1_note='Anmeldung als 2er-Team · 158 CHF pro Team · 48 Plätze',
  t1_inc=['Turnier: Qualifikation, dann Haupttableau', 'Bälle inklusive', 'Signature-Buffet von Instinct Amazonia', '1 Getränk inklusive', 'DJ-Party bis 2 Uhr'],
  t2_name='Dinner Party', t2_price='59 CHF', t2_unit='pro Person', t2_note='Für alle, die nur zur Party kommen · 52 Plätze',
  t2_inc=['Signature-Buffet von Instinct Amazonia', '1 Getränk inklusive', 'DJ-Party bis 2 Uhr'],
  extra='Schläger können vor Ort gemietet werden. Weitere Getränke an der Bar.',
  prog_h='Das Programm', prog=[('10 Uhr', 'Empfang und Qualifikationsrunde'), ('Nachmittag', 'Haupttableau und Siegerehrung'), ('Abend', 'Dinner Party: Signature-Buffet von Instinct Amazonia'), ('Bis 2 Uhr', 'DJ-Party')],
  food_h='Das Signature-Buffet', food_p='Eine grosszügige Auswahl mit Nikkei-Einflüssen: Fingerfood zum Teilen und warme Gerichte auf dem Teller.',
  food=[('Kalt', 'Sushi, Salate, Nikkei-Häppchen und weitere kalte Kreationen'), ('Zum Teilen', 'Knuspriges Karaage, Baos und weitere Spezialitäten des Hauses'), ('Warm', 'Niedergegarte Schweinerippchen, Hähnchen-Curry, Saté-Spiesse, Grilliertes'), ('Beilagen', 'Gebratener Reis, Wokgemüse und weitere Beilagen')],
  food_cap='Auswahl unverbindlich, die finale Zusammenstellung richtet sich nach den Saisonprodukten. Fotos: Instinct Amazonia.',
  bar_h='Die Bar', bar_p='Ein Getränk ist im Ticket inbegriffen. Danach führt das Team von Instinct Amazonia die Bar:',
  bar=[('Sangria im Glas', '8 CHF'), ('Sangria-Krug zum Teilen', '29 CHF'), ('Apéritifs und Cocktails: Spritz, Suze…', '10 CHF'), ('Vodka–Red Bull, Whisky–Cola, Rum–Cola…', '12 CHF')],
  bar_cap='Bier, Wein und alkoholfreie Getränke ebenfalls erhältlich. Preise unverbindlich.',
  book_h='Tickets sichern', step1='1. Wähl dein Ticket', qty_l='Anzahl Tickets', go='Buchen & bezahlen',
  pay_note='Preise in CHF, inkl. MWST. Sichere Kartenzahlung über SumUp, Bestätigung per E-Mail. Rückerstattung bis Sonntag, 1. November 2026 möglich.',
  partner_h='Instinct Amazonia', partner_p='Nikkei-Küche, Food & Party: Das Restaurant in Granges verbindet japanische und peruanische Aromen, dazu kreative Cocktails und Party-Stimmung. Für Padel+Dine kocht das ganze Team bei uns.', partner_a='Zum Restaurant',
  faq_h='Gut zu wissen',
  faq=[('Wie läuft das Turnier ab?', 'Du meldest dich als 2er-Team an. Am Morgen wird die Qualifikation gespielt, danach geht es ins Haupttableau. Bälle sind inklusive.'),
       ('Ich habe keinen Schläger, ist das ein Problem?', 'Nein, du kannst vor Ort einen Schläger mieten.'),
       ('Kann ich nur an die Party kommen?', 'Ja, mit dem Dinner-Party-Ticket für 59 CHF: Signature-Buffet, ein Getränk und die DJ-Party.'),
       ('Was ist mit Allergien?', 'Gib sie im Buchungsformular an, wir leiten sie an die Küche weiter.'),
       ('Kann ich stornieren?', 'Ja, Rückerstattung bis Sonntag, 1. November 2026. Schreib uns per WhatsApp oder E-Mail. Danach werden Tickets nicht mehr zurückerstattet.'),
       ('Wo findet es statt?', 'In der Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch (5 Min. von Siders). Gratis-Parkplätze.')],
  final_h='Samstag, 7. November. Spielen, essen, tanzen.', final_p='Turnier + Dinner Party 79 CHF · Dinner Party 59 CHF · Salgesch',
  m_name='Dein Name', m_mail='Deine E-Mail', m_mail2='(hierhin kommt die Bestätigung)', m_tel='Handynummer', m_tel2='(für Infos am Eventtag)',
  m_people='Namen der Teilnehmenden', m_notes='Allergien oder Bemerkungen?', m_notes2='(optional)', m_ok='Ich habe die Bedingungen gelesen: Rückerstattung bis Sonntag, 1. November 2026 möglich.', m_go='Weiter zur Zahlung',
  cap1='48 Plätze', cap2='52 Plätze', t1_sub='2er-Team', t2_sub='Einzelticket'),
'en': dict(
  title='Padel+Dine feat. Instinct Amazonia · 7 November | Rackets Academy',
  desc='Saturday 7 November 2026 in Salgesch: padel tournament in teams of 2, Instinct Amazonia’s nikkei signature buffet and a DJ party until 2am. Tournament + Dinner Party 79 CHF, Dinner Party 59 CHF.',
  kicker='Rackets Academy × Instinct Amazonia', h1='Padel+Dine', h1b='feat. Instinct Amazonia',
  lede='Padel tournament by day, Dinner Party by night. Nikkei signature buffet, DJ and jungle vibes until 2am.',
  chips=['Saturday 7 November 2026', '10am – 2am', 'Salgesch'], cta='Get your tickets', cta2='See the programme',
  concept_h='A new concept: play, eat, dance.',
  concept_p='We bring together padel and the cooking of Instinct Amazonia, the nikkei restaurant from Granges, for a day that doesn’t end with the last point. Play the tournament with your partner, then everyone meets for the Dinner Party.',
  tk_h='Two tickets, one night',
  t1_name='Tournament + Dinner Party', t1_price='79 CHF', t1_unit='per person', t1_note='Sign up as a team of 2 · 158 CHF per team · 48 places',
  t1_inc=['Tournament: qualifying round, then main draw', 'Balls included', 'Instinct Amazonia signature buffet', '1 drink included', 'DJ party until 2am'],
  t2_name='Dinner Party', t2_price='59 CHF', t2_unit='per person', t2_note='For everyone coming just for the night · 52 places',
  t2_inc=['Instinct Amazonia signature buffet', '1 drink included', 'DJ party until 2am'],
  extra='Rental rackets available on site. Other drinks at the bar.',
  prog_h='The programme', prog=[('10am', 'Welcome and qualifying round'), ('Afternoon', 'Main draw and prize-giving'), ('Evening', 'Dinner Party: Instinct Amazonia signature buffet'), ('Until 2am', 'DJ party')],
  food_h='The signature buffet', food_p='A generous spread with nikkei influences: finger food to share and hot dishes served on the plate.',
  food=[('Cold', 'Sushi, salads, nikkei bites and more cold creations'), ('To share', 'Crispy karaage, baos and other house specialities'), ('Hot', 'Slow-cooked pork ribs, chicken curry, chicken satay, grilled meats'), ('Sides', 'Fried rice, sautéed vegetables and more')],
  food_cap='Indicative selection; the final menu depends on seasonal produce. Photos: Instinct Amazonia.',
  bar_h='The bar', bar_p='One drink is included in your ticket. After that, the Instinct Amazonia team runs the bar:',
  bar=[('Sangria by the glass', '8 CHF'), ('Sangria jug to share', '29 CHF'), ('Apéritifs and cocktails: Spritz, Suze…', '10 CHF'), ('Vodka–Red Bull, whisky–coke, rum–coke…', '12 CHF')],
  bar_cap='Beer, wine and soft drinks also available. Prices indicative.',
  book_h='Get your tickets', step1='1. Pick your ticket', qty_l='Number of tickets', go='Book & pay',
  pay_note='Prices in CHF, VAT included. Secure card payment via SumUp, confirmation by email. Refunds possible until Sunday 1 November 2026.',
  partner_h='Instinct Amazonia', partner_p='Nikkei cooking, food & party: the Granges restaurant blends Japanese and Peruvian flavours with creative cocktails and a party atmosphere. For Padel+Dine, the whole team comes to cook at our place.', partner_a='Visit the restaurant',
  faq_h='Good to know',
  faq=[('How does the tournament work?', 'You sign up as a team of 2. The qualifying round is played in the morning, then teams move into the main draw. Balls are provided.'),
       ('I don’t have a racket — is that a problem?', 'Not at all, you can rent one on site.'),
       ('Can I come just for the party?', 'Yes, with the Dinner Party ticket for 59 CHF: signature buffet, one drink and the DJ party.'),
       ('What about allergies?', 'Let us know in the booking form and we’ll pass it on to the kitchen.'),
       ('Can I cancel?', 'Yes, refunds are possible until Sunday 1 November 2026. Message us on WhatsApp or by email. After that date, tickets are non-refundable.'),
       ('Where is it?', 'At Rackets Academy Salgesch, Littenstrasse 30, 3970 Salgesch (5 min from Sierre). Free parking.')],
  final_h='Saturday 7 November. Play, eat, dance.', final_p='Tournament + Dinner Party 79 CHF · Dinner Party 59 CHF · Salgesch',
  m_name='Your name', m_mail='Your email', m_mail2='(confirmation is sent here)', m_tel='Mobile number', m_tel2='(for updates on the day)',
  m_people='Participant names', m_notes='Allergies or comments?', m_notes2='(optional)', m_ok='I have read the terms: refunds possible until Sunday 1 November 2026.', m_go='Continue to payment',
  cap1='48 places', cap2='52 places', t1_sub='Team of 2', t2_sub='Single ticket'),
}

CSS = '''<style id="dine-css">
:root{--jungle:#0f2e27;--jungle2:#173f35;--gold:#c6a460;--cream:#f7f2e7}
.dn-hero{position:relative;min-height:86vh;display:flex;align-items:flex-end;padding:120px 0 56px;color:#fff;background:var(--jungle) center/cover no-repeat;overflow:hidden}
.dn-hero:before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,46,39,.55) 0%,rgba(15,46,39,.92) 75%)}
.dn-hero-in{position:relative;z-index:1;display:grid;grid-template-columns:1.4fr .8fr;gap:40px;align-items:end}
.dn-kicker{color:var(--gold);font-weight:800;letter-spacing:.12em;text-transform:uppercase;font-size:.82rem;margin:0 0 12px}
.dn-hero h1{color:#fff;font-size:clamp(2.6rem,8vw,5rem);line-height:.95;margin:0}
.dn-hero h1 span{display:block;color:var(--gold);font-size:.45em;letter-spacing:.02em;margin-top:10px}
.dn-hero .lede{color:#fff;max-width:560px;font-size:1.15rem;opacity:.95;margin:18px 0}
.dn-hero .spa-chip{border-color:rgba(198,164,96,.6)}
.dn-logo{width:100%;height:auto;max-width:260px;justify-self:end;filter:drop-shadow(0 4px 18px rgba(0,0,0,.35))}
.dn-btn-gold{background:var(--gold)!important;color:var(--jungle)!important}
.dn-sec{padding:64px 0}
.dn-dark{background:var(--jungle);color:#fff}
.dn-dark h2,.dn-dark h3{color:#fff}
.dn-cream{background:var(--cream)}
.dn-h{font-size:clamp(1.8rem,4.5vw,2.6rem);line-height:1.1;margin:0 0 18px;color:var(--jungle)}
.dn-dark .dn-h{color:#fff}
.dn-sec p,.dn-sec li,.dn-menu div,.dn-book p{color:var(--jungle)}.dn-dark p,.dn-dark li,.dn-dark span{color:#fff}
.dn-concept{max-width:760px;font-size:1.15rem;line-height:1.55}
.dn-tks{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:8px}
.dn-tk{background:#fff;border-radius:22px;padding:28px;border:2px solid #e7dcc4;position:relative}
.dn-tk.main{border-color:var(--gold);box-shadow:0 12px 32px rgba(15,46,39,.12)}
.dn-tk h3{margin:0;color:var(--jungle);font-size:1.4rem}
.dn-tk .pr{font-size:2.6rem;font-weight:800;color:var(--jungle);margin:8px 0 0;line-height:1}
.dn-tk .pr small{font-size:.95rem;font-weight:700;opacity:.7}
.dn-tk .nt{color:#8a6d33;font-weight:700;font-size:.92rem;margin:8px 0 16px}
.dn-tk ul{list-style:none;padding:0;margin:0}
.dn-tk li{padding:8px 0 8px 28px;border-top:1px solid #efe6d3;position:relative}
.dn-tk li:before{content:"✓";position:absolute;left:4px;color:var(--gold);font-weight:800}
.dn-extra{margin:16px 0 0;font-size:.95rem;opacity:.8}
.dn-prog{list-style:none;padding:0;margin:0;max-width:720px}
.dn-prog li{display:grid;grid-template-columns:130px 1fr;gap:16px;padding:16px 0;border-bottom:1px solid rgba(198,164,96,.35);font-size:1.1rem}
.dn-prog b{color:var(--gold)}
.dn-food{display:grid;grid-template-columns:1fr 1.1fr;gap:40px;align-items:start}
.dn-gal{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.dn-gal img{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:14px;display:block;background:var(--jungle2)}
.dn-menu{margin:18px 0 0}
.dn-menu div{padding:12px 0;border-top:1px solid #e7dcc4}
.dn-menu b{display:block;color:var(--jungle)}
.dn-cap{font-size:.85rem;opacity:.7;margin:14px 0 0}
.dn-bar{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:center}
.dn-bar img{width:100%;border-radius:22px;aspect-ratio:1;object-fit:cover}
.dn-bar-l div{display:flex;justify-content:space-between;gap:16px;padding:12px 0;border-bottom:1px solid rgba(198,164,96,.35)}
.dn-bar-l b{color:var(--gold);white-space:nowrap}
.dn-book .camp-step{color:var(--jungle)}
.dn-book .camp-opt input:checked + .camp-tile{border-color:var(--gold);box-shadow:0 0 0 3px rgba(198,164,96,.3)}
.dn-book .camp-pack-name,.dn-book .camp-pack-price{color:var(--jungle)}
.dn-book .camp-summary{background:var(--jungle)}
.dn-book .camp-summary p{color:#fff}
.dn-book .camp-summary .btn{background:var(--gold);color:var(--jungle)}
.dn-qty{display:flex;align-items:center;gap:10px;margin:-14px 0 26px}
.dn-qty button{width:40px;height:40px;border-radius:50%;border:2px solid var(--gold);background:#fff;font-size:1.3rem;font-weight:800;cursor:pointer;color:var(--jungle)}
.dn-qty input{width:64px;height:40px;text-align:center;border:2px solid #e7dcc4;border-radius:10px;font:inherit;font-weight:800}
.dn-soon{background:var(--gold);color:var(--jungle);font-weight:800;border-radius:12px;padding:12px 16px;margin:0 0 14px}
.dn-partner{display:grid;grid-template-columns:200px 1fr;gap:36px;align-items:center;max-width:860px}
.dn-partner img{width:100%;height:auto}
.dn-final{background:var(--jungle) center/cover;position:relative;padding:90px 0;text-align:center;color:#fff}
.dn-final:before{content:"";position:absolute;inset:0;background:rgba(15,46,39,.82)}
.dn-final .wrap{position:relative}
.dn-final h2{color:#fff;font-size:clamp(1.8rem,5vw,2.6rem);margin:0 0 8px}
.pp-row.pp-one{grid-template-columns:1fr!important}
#modal-people{display:grid;gap:8px;margin-top:6px}.pp-row{display:grid;grid-template-columns:1fr 120px;gap:8px}.pp-row input{width:100%}.pp-lbl{font-size:.78rem;font-weight:700;color:#7a8ea3;margin-bottom:-4px}
@media(max-width:820px){.dn-hero-in,.dn-tks,.dn-food,.dn-bar,.dn-partner{grid-template-columns:1fr}.dn-logo{justify-self:start;max-width:150px;order:-1}.dn-prog li{grid-template-columns:100px 1fr}.dn-partner img{max-width:160px}}
</style>
'''

def body(L, t, pre):
    chips = ''.join(f'<span class="spa-chip">{c}</span>' for c in t['chips'])
    inc = lambda xs: ''.join(f'<li>{x}</li>' for x in xs)
    prog = ''.join(f'<li><b>{a}</b><span>{b}</span></li>' for a, b in t['prog'])
    gal = ''.join(f'<img src="{u}" alt="Instinct Amazonia" loading="lazy" onerror="this.remove()">' for u in FOOD)
    menu = ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in t['food'])
    bar = ''.join(f'<div><span>{a}</span><b>{b}</b></div>' for a, b in t['bar'])
    faq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in t['faq'])
    hero_img = pre + 'images/coaching/coaching-hero.jpg'
    return f'''
<section class="dn-hero" style="background-image:url('{hero_img}')">
  <div class="wrap dn-hero-in">
    <div>
      <p class="dn-kicker">{t['kicker']}</p>
      <h1>{t['h1']}<span>{t['h1b']}</span></h1>
      <p class="lede">{t['lede']}</p>
      <div class="spa-chips">{chips}</div>
      <div class="hero-actions">
        <a class="btn dn-btn-gold" href="#tk-book">{t['cta']}</a>
        <a class="btn spa-cta-ghost" href="#programme">{t['cta2']}</a>
      </div>
    </div>
    <img class="dn-logo" src="{pre}images/dine/instinct-amazonia-logo-gold.webp" alt="Instinct Amazonia" width="360" height="466">
  </div>
</section>

<section class="dn-sec">
  <div class="wrap">
    <h2 class="dn-h">{t['concept_h']}</h2>
    <p class="dn-concept">{t['concept_p']}</p>
  </div>
</section>

<section class="dn-sec dn-cream">
  <div class="wrap">
    <h2 class="dn-h">{t['tk_h']}</h2>
    <div class="dn-tks">
      <div class="dn-tk main"><h3>{t['t1_name']}</h3><p class="pr">{t['t1_price']} <small>{t['t1_unit']}</small></p><p class="nt">{t['t1_note']}</p><ul>{inc(t['t1_inc'])}</ul></div>
      <div class="dn-tk"><h3>{t['t2_name']}</h3><p class="pr">{t['t2_price']} <small>{t['t2_unit']}</small></p><p class="nt">{t['t2_note']}</p><ul>{inc(t['t2_inc'])}</ul></div>
    </div>
    <p class="dn-extra">{t['extra']}</p>
  </div>
</section>

<section class="dn-sec dn-dark" id="programme">
  <div class="wrap">
    <h2 class="dn-h">{t['prog_h']}</h2>
    <ul class="dn-prog">{prog}</ul>
  </div>
</section>

<section class="dn-sec">
  <div class="wrap dn-food">
    <div>
      <h2 class="dn-h">{t['food_h']}</h2>
      <p>{t['food_p']}</p>
      <div class="dn-menu">{menu}</div>
      <p class="dn-cap">{t['food_cap']}</p>
    </div>
    <div class="dn-gal">{gal}</div>
  </div>
</section>

<section class="dn-sec dn-dark">
  <div class="wrap dn-bar">
    <div>
      <h2 class="dn-h">{t['bar_h']}</h2>
      <p>{t['bar_p']}</p>
      <div class="dn-bar-l">{bar}</div>
      <p class="dn-cap">{t['bar_cap']}</p>
    </div>
    <img src="{COCKTAIL}" alt="Cocktail Instinct Amazonia" loading="lazy">
  </div>
</section>

<section class="section-tight camp-book dn-book" id="tk-book">
  <div class="wrap">
    <h2 class="dn-h">{t['book_h']}</h2>
    <p class="camp-step">{t['step1']}</p>
    <div class="camp-dates">
      <label class="camp-opt">
        <input type="radio" name="tk" value="team" checked>
        <span class="camp-tile">
          <span class="camp-pack-name">{t['t1_name']}</span>
          <span class="camp-pack-price">158 CHF <small>· {t['t1_sub']} (2 × 79)</small></span>
          <span class="camp-spots">{t['cap1']}</span>
        </span>
      </label>
      <label class="camp-opt">
        <input type="radio" name="tk" value="dinner">
        <span class="camp-tile">
          <span class="camp-pack-name">{t['t2_name']}</span>
          <span class="camp-pack-price">59 CHF <small>· {t['t2_sub']}</small></span>
          <span class="camp-spots">{t['cap2']}</span>
        </span>
      </label>
    </div>
    <div class="dn-qty" id="tk-qty-wrap" style="display:none"><span>{t['qty_l']}</span><button type="button" data-step="-1" aria-label="−">−</button><input id="tk-qty" type="number" min="1" max="10" value="1" inputmode="numeric"><button type="button" data-step="1" aria-label="+">+</button></div>
    <p class="dn-soon" id="tk-note" style="display:none"></p>
    <div class="camp-summary">
      <div><p id="tk-sum-what"></p><p class="camp-total" id="tk-sum-total"></p></div>
      <button type="button" class="btn" id="tk-go" onclick="openTicketModal()">{t['go']}</button>
    </div>
    <p style="margin:12px 0 0; font-size:.88rem; color:var(--jungle);">{t['pay_note']}</p>
  </div>
</section>

<section class="dn-sec dn-dark">
  <div class="wrap dn-partner">
    <img src="{pre}images/dine/instinct-amazonia-logo-gold.webp" alt="Instinct Amazonia" width="360" height="466" loading="lazy">
    <div>
      <h2 class="dn-h">{t['partner_h']}</h2>
      <p>{t['partner_p']}</p>
      <a class="btn dn-btn-gold" href="https://www.amazoniarestaurant.ch/" target="_blank" rel="noopener">{t['partner_a']}</a>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="wrap">
    <h2>{t['faq_h']}</h2>
    <div class="spa-faq">{faq}</div>
  </div>
</section>

<section class="dn-final" style="background-image:url('{LEAVES}')">
  <div class="wrap">
    <h2>{t['final_h']}</h2>
    <p>{t['final_p']}</p>
    <a class="btn dn-btn-gold" href="#tk-book">{t['cta']}</a>
  </div>
</section>

<div class="buy-modal-overlay" id="buy-modal-overlay">
  <div class="buy-modal">
    <button type="button" class="buy-modal-close" id="buy-modal-close" aria-label="Close">&times;</button>
    <h3 id="buy-modal-title"></h3>
    <div class="buy-modal-price" id="buy-modal-price"></div>
    <form id="buy-modal-form" class="shop-form" method="POST" action="{ACTION}" target="_blank">
      <input type="hidden" name="formType" value="ticket">
      <input type="hidden" name="eventId" id="modal-eventId">
      <input type="hidden" name="ticket" id="modal-ticket">
      <input type="hidden" name="qty" id="modal-qty">
      <input type="hidden" name="price" id="modal-price">
      <label class="shop-field">{t['m_name']}<input type="text" name="buyerName" required autocomplete="name"></label>
      <label class="shop-field">{t['m_mail']} <span style="font-weight:400; opacity:.7;">{t['m_mail2']}</span><input type="email" name="buyerEmail" required autocomplete="email"></label>
      <label class="shop-field">{t['m_tel']} <span style="font-weight:400; opacity:.7;">{t['m_tel2']}</span><input type="tel" name="phone" required autocomplete="tel"></label>
      <div class="shop-field">{t['m_people']}<div id="modal-people"></div><input type="hidden" name="participants"></div>
      <label class="shop-field">{t['m_notes']} <span style="font-weight:400; opacity:.7;">{t['m_notes2']}</span><textarea name="notes" rows="2" maxlength="300"></textarea></label>
      <label class="camp-check"><input type="checkbox" name="termsOk" value="yes" required><span>{t['m_ok']}</span></label>
      <button type="submit" class="btn btn-green" style="width:100%; text-align:center;">{t['m_go']}</button>
    </form>
  </div>
</div>

'''

def ld(L, t, url):
    base = 'https://www.racketsacademy.ch/'
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Event', 'name': 'Padel+Dine feat. Instinct Amazonia', 'description': t['desc'],
         'startDate': '2026-11-07T10:00:00+01:00', 'endDate': '2026-11-08T02:00:00+01:00',
         'eventStatus': 'https://schema.org/EventScheduled', 'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
         'maximumAttendeeCapacity': 100, 'image': FOOD[0], 'inLanguage': L,
         'location': {'@type': 'Place', 'name': 'Rackets Academy Salgesch', 'address': {'@type': 'PostalAddress', 'streetAddress': 'Littenstrasse 30', 'postalCode': '3970', 'addressLocality': 'Salgesch', 'addressRegion': 'VS', 'addressCountry': 'CH'}},
         'organizer': [{'@type': 'Organization', 'name': 'Rackets Academy', 'url': base}, {'@type': 'Restaurant', 'name': 'Instinct Amazonia', 'url': 'https://www.amazoniarestaurant.ch/'}],
         'offers': [{'@type': 'Offer', 'name': t['t1_name'], 'price': '79', 'priceCurrency': 'CHF', 'url': url + '#tk-book', 'availability': 'https://schema.org/InStock', 'validFrom': '2026-10-03T00:00:00+02:00'},
                    {'@type': 'Offer', 'name': t['t2_name'], 'price': '59', 'priceCurrency': 'CHF', 'url': url + '#tk-book', 'availability': 'https://schema.org/InStock', 'validFrom': '2026-10-03T00:00:00+02:00'}]},
        {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in t['faq']]}]}

for L, t in T.items():
    pre = '' if L == 'en' else '../'
    d = '' if L == 'en' else L + '/'
    s = open(d + 'spa-and-sauna.html').read()
    a = s.index('</header>'); a = s.index('\n', s.index('</div>', a)) + 1
    b = s.index('<footer')
    s = s[:a] + body(L, t, pre) + s[b:]
    s = s.replace('spa-and-sauna.html', SLUG)
    s = re.sub(r'<script type="application/ld\+json" id="ld-spa">.*?</script>\n', '', s, flags=re.S)
    s = re.sub(r'<title>.*?</title>', '<title>' + t['title'] + '</title>', s, count=1, flags=re.S)
    esc = lambda x: x.replace('&', '&amp;').replace('"', '&quot;')
    for k in ['name="description"', 'property="og:description"']:
        s = re.sub(r'<meta ' + k + ' content="[^"]*"', '<meta ' + k + ' content="' + esc(t['desc']) + '"', s)
    s = re.sub(r'<meta property="og:title" content="[^"]*"', '<meta property="og:title" content="' + esc(t['title']) + '"', s)
    s = re.sub(r'<meta property="og:image" content="[^"]*"', '<meta property="og:image" content="' + FOOD[0] + '"', s)
    url = 'https://www.racketsacademy.ch/' + d + SLUG
    s = s.replace('</head>', '<script type="application/ld+json" id="ld-dine">' + json.dumps(ld(L, t, url), ensure_ascii=False) + '</script>\n' + CSS + '</head>', 1)
    s = s.replace('class="active"', '')
    s = re.sub(r'<script src="(?:\.\./)?nav\.js\?v=\d+"></script>', lambda m: m.group(0) + '\n<script src="' + pre + 'dine.js?v=2"></script>', s, count=1)
    open(d + SLUG, 'w').write(s)
    print(d + SLUG, len(t['title']), len(t['desc']))
