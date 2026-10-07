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
- 07.10.2026 · Meta Pixel: InitiateCheckout jetzt mit Betrag (Feld `price`) + Paket; Purchase mit eventID (SumUp-ID); Klick auf «Pay on the SumUp page instead» = AddPaymentInfo; Rückkehr von SumUp mit `?paid=<ref>&amount=<CHF>` zählt als Purchase (1× pro ref). **Offen:** im Shop-Apps-Script beim SumUp-Checkout `redirect_url` = `https://www.racketsacademy.ch/ski-and-padel.html?paid=<ref>&amount=<CHF>` (bzw. Seite des Produkts) setzen. nav.js v29. Live-Kampagne «Ski & Padel 2027 – Sales» optimiert auf InitiateCheckout.
- 06.10.2026 · Meta Pixel 1826093361488124 in nav.js (loads only after cookie consent; events: PageView, PlaytomicClick, Contact, Lead, InitiateCheckout, Purchase). Cookie banner text + privacy policy (EN/FR/DE) updated.
- 2026-10-04 · Phil · COWORK.md angelegt, Felix als Collaborator, Drive-Ordner pro Seite
- 2026-10-03 · Phil · Padel+Dine live inkl. Ticketverkauf, Video-Hero
- 07.10.2026 · Ski & Padel: Sticky-Button mobil «Choose your weekend» → #camp-book. Event-Seiten (Padel +Dine, Ski & Padel): Top-Leiste zeigt Event statt «Courts open now». hero-mobile.mp4 komprimiert (2,7 → 1,1 MB). nav.js v26.
- 07.10.2026 · UX v1 (Branch ux-v1): Preise + FAQ auf Startseite/Book, Trust-Zeile, Gutschein-Banner, neuer Footer (Zeiten, WhatsApp, Links), Shop als Filter-Shop, Racket-Filter + «Teste-la 10 CHF», Kursseite-Weiche («Cours d'initiation»), Anfrageformulare Kids/Firmen → WhatsApp, Ski-Seite leichter (uploads/ski-padel/sm) + Bewertungen nach oben, Popup/Cookie-Banner übersetzt bzw. kompakt. Scripts: tools/ux_*.py (nach Generator-Läufen erneut ausführen).
- 07.10.2026 · Schläger-Specs (Form, Gewicht, Härte, Niveau, Balance) aus Shop-Sheet Tab «RacketSpecs» → tools/racket_specs.json → python3 tools/build_racket_specs.py → racket-specs.js. Shop-Filter Forme/Dureté/Niveau + Specs auf Produktseiten. Event-Preise im Events-Hub, NTO24 verlinkt auf /padel4ever/.
