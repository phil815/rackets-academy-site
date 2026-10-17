# Cowork – racketsacademy.ch

Gemeinsame Arbeitsdatei für **Phil** und **Felix**. Kurz halten, aktuell halten.
Wer etwas Grösseres ändert, ergänzt hier eine Zeile unter «Log».

---

## Wer macht was

| | Phil | Felix |
|---|---|---|
| Fokus | Inhalte, Seiten, Code, Shop/Tickets, Scripts | **Bilder & Videos** für die Seiten finden, sichten, auf den Drive legen |
| Arbeitet in | Repo + Apps Script | Google Drive (`Website – Bilder & Videos`) + Repo bei Bedarf |

---

## Felix: Bilder & Videos

### Wohin
Drive-Ordner **[Website – Bilder & Videos](https://drive.google.com/drive/folders/13YWtdTgHb42Rqarv6KWEoW2nK0gim5oU)**, ein Unterordner pro Seite:

| Ordner | Seite(n) | Was gebraucht wird (Prio) |
|---|---|---|
| `home` | Startseite | Atmosphäre beider Standorte, Leute lachen/spielen, Bar/Lounge |
| `training` | Kurse | **Salgesch**-Trainings (bisher nur Sion), Kids-Training, Coach erklärt |
| `kids-birthday` | Kindergeburtstag | **Echte Geburtstage** (bisher Coaching-Fotos als Ersatz) – nur mit Einverständnis der Eltern |
| `company-events` | Firmenevents | Teambuilding-Gruppen, Apéro, Gruppenfoto am Netz |
| `events` | Events + Eventseiten | Padel+Wine, Padel+Paella, Rackemix, Racketero, Pickleball, 24h-Turnier |
| `spa-sauna` | Spa & Sauna | Sauna, Ruhebereich, Details (Holz, Dampf, Handtücher) |
| `camps` | Ski & Padel | Ski + Padel, Unterkunft WYN Skillpark, Gruppe |
| `about-team` | Über uns | Teamfotos, Coaches einzeln (Jesus, Mario …) |

Padel+Dine (Instinct Amazonia): `Brand – Rackets Academy / Social – 2026-11-07 Padel+Dine` – Food- und Party-Fotos fehlen noch.

### Anforderungen
- **Fotos:** Originale (JPG/HEIC), kein WhatsApp-Export (zu stark komprimiert). Mind. 2000 px an der langen Seite.
  - Hero/Banner: **quer** (16:9 oder 3:2), Motiv eher in der Mitte, oben Luft für Text.
  - Karten/Social: **hoch** (4:5 oder 3:4).
- **Videos:** MP4/MOV, 5–15 s, ruhige Kamera, Action in der Mitte. Ton egal (läuft stumm). Für Desktop quer, für Handy hoch – beides ideal.
- **Echte Leute, echte Halle.** Kein Stock. Standort beachten: Sion-Fotos nur auf Sion-Seiten.
- **Einverständnis**: Erkennbare Personen müssen OK sein (Kinder: Eltern fragen).
- **Dateiname:** `seite_motiv_ort_nr.jpg`, z. B. `training_kids-vorhand_salgesch_01.jpg`.
- Lieber 5 starke als 50 mittelmässige. Unscharf/Gegenlicht/leere Courts rausnehmen.

### Ablauf
1. Felix legt Dateien in den passenden Ordner.
2. Kurze Nachricht an Phil: «training: 6 neue Fotos».
3. Phil (oder Claude) holt sie per **DriveZuGitHub → `pushFolderToGitHub`** ins Repo (`uploads/<ordner>/`), komprimiert sie und baut sie in die Seite ein.

Ordner-IDs für `PUSH_JOBS_` im Script DriveZuGitHub:
```javascript
var PUSH_JOBS_ = [
  ['1PrxDjW5lAKbKon4d27w-8ffA40tEaSwH', 'home'],
  ['1ZgdPjG1TQ3EyOioYEs7z1w2TehtKuyBg', 'training'],
  ['1-HHHCmHVSD1rs_8JzHe6t_34Xve24kF8', 'kids-birthday'],
  ['1LEEVKPJU5UH76OXJPSpdQWbQj9B22qLj', 'company-events'],
  ['1zPeBJWjx3vdNsf0nOoCRTq72-DqzfoHh', 'events'],
  ['19L6ThD1kW-tX6xkaSEcXcwkkWxnx8RfZ', 'spa-sauna'],
  ['1w1Jesr6dBXJN7NKLVdb5oyQ4gWt14AC7', 'camps'],
  ['1Vi-PKHH5ECx1UFuLhCfDi9JUNLXTukvO', 'about-team']
];
```

---

## Aufbau der Website (Kurzfassung)

- **Hosting:** GitHub Pages aus `main`, Domain `racketsacademy.ch` (`CNAME`). Push → live in ca. 1–2 Min.
  Hängt es: GitHub → Actions → «pages build and deployment» prüfen, ggf. neu starten.
- **Sprachen:** EN im Root, `fr/`, `de/`. Jede Seite gibt es 3×.
- **Generierte Seiten – nicht von Hand ändern**, sondern das Script in `tools/` anpassen und neu bauen:
  `build_dine.py` (Padel+Dine), `build_camps.py`, `build_training.py`, `build_birthday.py`, `build_events.py`, `build_events_hub.py`, `build_spa.py`, `build_rackets.py`, `build_oberwallis.py`.
- **Gemeinsame Teile:** `styles.css`, `nav.js` (Menü, Footer, mobile Buchungsleiste). Bei Änderung an `nav.js` die Version `nav.js?v=N` in allen Seiten hochzählen.
- **Medien:** `images/` (fertig optimiert), `uploads/` (aus Drive gepusht), `videos/` (Hero-Videos).
- **Shop/Tickets:** Formulare → Shop-Apps-Script (Code.gs, Camps.gs, Events.gs) → SumUp → Orders-Sheet → Mail + KLARA-Entwurf. Kopie von Events.gs liegt in `tools/apps-script/`.
- **Versteckt:** `padel4ever/` (24h-Turnier, nicht verlinkt, noindex).

## Brand
- Schrift: **Galano Grotesque** (`fonts/`).
- Farben: Navy `#0b1a2b` (Footer), Blau `#0077de`, Grün `#6ffd1d` (Akzent). Himmelblau nur für Sport-Events.
- Eventseiten dürfen ein eigenes Thema haben (z. B. Padel+Dine: Dschungelgrün/Gold), Logo und Schrift bleiben RA.
- Assets: Drive `Brand – Rackets Academy` (Logos, Icons, Templates).

## Zusammenarbeiten im Repo
- Vor dem Arbeiten: `git pull`. Kleine Commits, klare Messages (`Training: Salgesch-Fotos im Hero`).
- Nie Passwörter/Tokens ins Repo.
- Grosse Videos vorher komprimieren (Ziel < 3 MB, H.264, ohne Ton).

---

## Offene Punkte (Stand 4.10.2026)
- [ ] Padel+Dine: Food-/Party-Fotos Instinct Amazonia → Website + Insta-Carousel
- [ ] Kindergeburtstag & Firmenevents: echte Event-Fotos statt Coaching-Fotos
- [ ] Training: Salgesch- und Kids-Fotos
- [ ] Eigene Seiten: 24h-Turnier (Name offen), Rackemix, Pickleball Mix & Match, Padel+Beer
- [ ] FAQ-Seite (Racket-Miete, Stornierung, Hausregeln)
- [ ] Wix-Bilder (`images/wix/`) durch eigene ersetzen, dann Wix kündigen
- [ ] Merchant Center: falsche Gratisversand-Richtlinie durch Abholrichtlinie ersetzen

## Log
- 07.10.2026 · Meta Pixel: InitiateCheckout jetzt mit Betrag (Feld `price`) + Paket; Purchase mit eventID (SumUp-ID); Klick auf «Pay on the SumUp page instead» = AddPaymentInfo; Rückkehr von SumUp mit `?paid=<ref>&amount=<CHF>` zählt als Purchase (1× pro ref). ~~**Offen:** im Shop-Apps-Script beim SumUp-Checkout `redirect_url` = `https://www.racketsacademy.ch/ski-and-padel.html?paid=<ref>&amount=<CHF>` (bzw. Seite des Produkts) setzen.~~ ✅ erledigt 07.10. (Return.gs) nav.js v29. Live-Kampagne «Ski & Padel 2027 – Sales» optimiert auf InitiateCheckout.
- 06.10.2026 · Meta Pixel 1826093361488124 in nav.js (loads only after cookie consent; events: PageView, PlaytomicClick, Contact, Lead, InitiateCheckout, Purchase). Cookie banner text + privacy policy (EN/FR/DE) updated.
- 2026-10-04 · Phil · COWORK.md angelegt, Felix als Collaborator, Drive-Ordner pro Seite
- 2026-10-03 · Phil · Padel+Dine live inkl. Ticketverkauf, Video-Hero
- 07.10.2026 · Ski & Padel: Sticky-Button mobil «Choose your weekend» → #camp-book. Event-Seiten (Padel +Dine, Ski & Padel): Top-Leiste zeigt Event statt «Courts open now». hero-mobile.mp4 komprimiert (2,7 → 1,1 MB). nav.js v26.
- 07.10.2026 · UX v1 (Branch ux-v1): Preise + FAQ auf Startseite/Book, Trust-Zeile, Gutschein-Banner, neuer Footer (Zeiten, WhatsApp, Links), Shop als Filter-Shop, Racket-Filter + «Teste-la 10 CHF», Kursseite-Weiche («Cours d'initiation»), Anfrageformulare Kids/Firmen → WhatsApp, Ski-Seite leichter (uploads/ski-padel/sm) + Bewertungen nach oben, Popup/Cookie-Banner übersetzt bzw. kompakt. Scripts: tools/ux_*.py (nach Generator-Läufen erneut ausführen).
- 07.10.2026 · Schläger-Specs (Form, Gewicht, Härte, Niveau, Balance) aus Shop-Sheet Tab «RacketSpecs» → tools/racket_specs.json → python3 tools/build_racket_specs.py → racket-specs.js. Shop-Filter Forme/Dureté/Niveau + Specs auf Produktseiten. Event-Preise im Events-Hub, NTO24 verlinkt auf /padel4ever/.
- 07.10.2026 · SumUp-Rückkehr: neues Apps-Script-File `tools/apps-script/Return.gs` (ganz unten im Shop-Projekt) setzt bei jedem Checkout `redirect_url` = Produktseite (fr/de je nach Sprache) `?paid=<ref>&amount=<CHF>` und gibt `ref` in der JSON-Antwort zurück. Shop → shop.html, Camp → ski-and-padel.html, Ticket → Eventseite, sonst Startseite. Code.gs/Camps.gs/Events.gs/Fulfilment unverändert. nav.js: Widget-Kauf nutzt eventID `j.ref || j.id` + setzt `ra_paid_<ref>` (kein Doppelzählen). nav.js v30.
- 10.10.2026 · Firmenrabatt: «Suva / CRR» im Dropdown auf company.html (EN/DE/FR), nach Renotec. Apps Script «Company Discount» hat eigene PARTNERS-Liste – dort ebenfalls ergänzen (sonst Anmeldung = «Neue Firma»). Neue Partnerfirmen immer an beiden Stellen eintragen.
- 12.10.2026 · Follow-up bei unbezahlten Bestellungen: neues Apps-Script-File `tools/apps-script/FollowUp.gs` (ganz unten im Shop-Projekt, nur gespeichert – kein Deployment nötig). Hängt an checkPendingOrders: 2 Std. nach einem FAILED/EXPIRED-Versuch Mail «💬 Follow-up: …» an NOTIFY_EMAIL mit WhatsApp-/Mail-Link + fertigem Text in Kundensprache. Keine Mail, wenn dieselbe E-Mail danach bezahlt hat; mehrere Versuche = 1 Mail; interne Tests/Bots ignoriert; Spalte M «FollowUp» im Orders-Tab markiert erledigt. Nur Bestellungen ab 12.10.
- 14.10.2026 · Eigene Besuche: alle Seiten setzen traffic_type=internal, wenn das Geraet einmal ?internal=1 aufgerufen hat (localStorage ra_internal; ?internal=0 hebt auf). In GA4 Datenfilter «Internal Traffic» aktivieren. Analytics-Script (tools/apps-script/Analytics.gs, Projekt «Analytics») schreibt GA4 taeglich 6 Uhr ins Sheet «RA Website-Daten» (1BXsiGc3M1ZAXaIbciHvAOzc9LRSKqhsCtBPaYV8uBtE); Search Console braucht noch API-Freischaltung. GA4 Key Events: begin_checkout, book_court, whatsapp_click, purchase, generate_lead.
- 2026-10-14: SEO – Titel/Beschreibung Ski & Padel (Keyword «Padel Camp») und Spa (Wallis/Valais, Visp) in EN/DE/FR; 18 Weiterleitungs-Stubs für alte Wix-URLs (playtomic, home, padel, players-camp, coaching, about-us …) mit canonical + meta refresh, damit Google die Rankings überträgt. Stubs NICHT in sitemap.xml aufnehmen.
- 15.10.2026 · ÖFFENTLICH (noindex entfernt, in sitemap), Hero-Bild images/anniviers/, Spa ausgeschlossen. Partnerschaft Val d'Anniviers (Anniviers Tourisme SA): nur Salgesch; Carte d'hôte Anniviers Liberté, Winter ab 1.11.2026 erstmals. Landingpage anniviers.html / fr/ / de/ (noindex, nicht verlinkt – Entwurf). 15% vor 17:30, 7 Tage inkl. Wochenende. Formular wie Firmenrabatt + Feld card_number (N° carte d'hôtes); anniviers-form.js, ENDPOINT noch leer → Fallback WhatsApp. TODO: eigenes Apps Script + Sheet «Anniviers», Playtomic-Gruppe «Val d'Anniviers», Logo-Dateien vom Tourismusbüro (aktuell hotlink static.valdanniviers.ch).
- 15.10.2026 · Anniviers Backend live: Apps Script «Anniviers» (Projekt 18GNhfI01ebKaN-Djlrd6krxqMlr4tNWnysCcokon8scWgux9Ecx3rZe5), Web-App AKfycbxM5AiA…hNA, Sheet «RA Anniviers – Carte d'hôte» (1BdUSojPlZofdEi9PDIapuNF_DnxaPLui8_qp4JeKxYI). Jede Anmeldung → Mail an Phil mit Playtomic-Import-CSV (category_name «Val d'Anniviers», kein Ablaufdatum) + Bestätigung an Person.
- 16.10.2026 · Analytics-Script erweitert: Meta Ads (act_870675094567241) + Instagram (Posts, Follower-Verlauf) täglich 6 Uhr ins Sheet «RA Website-Daten»; Montag 7 Uhr Wochenbericht-Mail. Token: Meta-App «RA Analytics», System User «Analytics», Skripteigenschaft META_TOKEN (läuft nie ab). Search Console via Windsor.ai (gratis). Supermetrics nicht mehr nötig.
- 16.10.2026 · Firmenrabatt: «Oiken» im Dropdown (EN/DE/FR) + PARTNERS im Apps Script.
- 16.10.2026 · Google Ads 196-238-1580: GA4-Property 556163205 verknüpft (alte Wix-Property 465019666 als Quelle abgewählt); GA4-Conversions importiert (purchase, begin_checkout, whatsapp_click=Contact, book_court=Book appointment, generate_lead=Lead), alle als Konto-Standardziele für alle 3 Kampagnen. Alte Wix-Conversions (Kauf, Shopping Cart, In den Einkaufswagen, Checkout) bleiben ohne Daten stehen. Oberwallis-Kampagne: Negativ-Keywords jobs, stelle, stellen, regeln, video, bauen.
- 16.10.2026 · Google Ads «Ski & Padel – London (EN)»: Standorte erweitert um Amsterdam, Dubai, Tel Aviv District (wie Instagram-Ads); 18 Negativ-Keywords auf Kampagnenebene: exakt [padel] [ski] [skiing] [padel tennis] [paddle tennis] [padel sport] [paddle sport] [padel game] [game of padel]; Phrase "how to" "how do i" "what is" "rules" "techniques" "lessons" "school" "beginners" "serve". Budget weiter 1 CHF/Tag.
- 16.10.2026 · Google Ads «Ski & Padel – London (EN)»: Budget 3 CHF/Tag; automatische Regel «Ski & Padel EN – Budget zurück auf 1 CHF (15.11.)» setzt es am 15.11.2026 einmalig auf 1 CHF zurück (Mail an phil@). Kampagne läuft bis 31.1.2027. Hinweis: Netzwerke = Suche + Suchpartner + Display.
- 16.10.2026 · Google Ads: alle 3 Kampagnen (Oberwallis, Ski & Padel London EN, Ski & Padel Berlin DE) nur noch Google-Suchnetzwerk – Suchpartner und Display-Netzwerk deaktiviert.
- 17.10.2026 · Team-Login im Menü (alle EN/DE/FR-Seiten, klein rechts) → racketsacademy.ch/intern (noindex) mit Kacheln P&L und Marketing-Report; beide führen in die Apps-Script-Web-App «RA P&L» (Login racketsacademy.ch + Allowlist phil@/bettina@). Analytics-Skript legt jeden Wochenbericht zusätzlich im Sheet «RA Website-Daten», Tab «Reports» ab (saveReport_; saveReportOnly() = ohne Mail).
- 17.10.2026 · Web App «RA P&L» v2 (gleiche /exec-URL): Reiter P&L | Marketing; Marketing zeigt Wochenberichte aus Tab «Reports» (letzte 12 Wochen). Backup des Codes in rackets-pl-data/apps-script/Code.gs.
- 17.10.2026 · Analytics-Skript: Search Console per API (Tab «GSC Tage», braucht GCP-Projekt «RA Analytics» ra-analytics-511909 / Nr. 152803810942, Search Console API + Analytics Data API aktiviert), Instagram-Tageswerte (Tab «Instagram Tage»: Reichweite, neue Follower, Profilaufrufe, Link-Klicks, Interaktionen; 30 Tage rückwirkend, Verlauf wächst), Wix-Basis (Tab «Wix Basis», Ø pro Woche der alten Wix-Property 465019666, 04.12.2024–26.09.2026). Scope webmasters.readonly ergänzt.
