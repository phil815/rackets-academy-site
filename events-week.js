// Events page (Guti 09.11.2026): next 30 days from the Sion + Salgesch Google calendars, grouped by week,
// cards like the weekly Instagram visuals. Each card links straight to the event's Playtomic sign-up.
//
// Optional block at the end of the calendar description, after a line "---" (never shown on the page):
//   playtomic: https://...   direct sign-up link (missing → Academy link of the site)
//   places: 8/16             booked/total → pill "8 VON 16 GEBUCHT"; booked ≥ total = full (greyed, not clickable)
//   style: hero | dark | white   (default white)
//   icon: 🍕
//   accent: +YOGA            highlighted part of the hero title
//   photo: https://...       hero photo (yoga / paella have a default photo and are hero by default)
//   price: 35 CHF
//   updated: 2026-11-09      when the places were last updated
//   title: Padel +Yoga       display title (optional; title_fr / title_de / title_en per language)
//   fr: … / de: … / en: …    short text per language (fallback: first sentence above "---")
// Shown: events with this block, plus those the old page showed (keyword list KEYS). Short text = first sentence above "---".
(function () {
  var API_KEY = 'AIzaSyDm1T-ofSLpJVzfpMOzhp7LLzMK1Pg9vpM';
  var CALENDARS = [
    { id: 'c_06fae67e3da9afefbea72735459e8b237c81650b84fff9332d50ddaa66509191@group.calendar.google.com', loc: 'Salgesch' },
    { id: 'c_3ef252ff359c72bd0187f71d11f948958588fceca659a6d89ae3888ee6710d68@group.calendar.google.com', loc: 'Sion' }
  ];
  var ACADEMY = { Sion: 'https://tinyurl.com/Academy-Sion', Salgesch: 'https://tinyurl.com/Academy-Salgesch' };
  // keywords of the public events the previous page already showed (everything else without a block stays hidden)
  var KEYS = ['padel+', 'padel +', 'dine', 'amazonia', 'wine', 'paella', 'beer', 'fitness', 'yoga', 'pizza', 'bifana', 'swisstennis', 'hyundai',
    'veyras', 'rivella', 'initiation', 'leveling', 'levelling', 'level', 'racketero', 'pickleball', '24h', 'p424', 'ski', 'rackemix'];
  var DAYS = 30;
  // default hero photos (site root), used when a hero has no photo: line
  var PHOTOS = [[/yoga/i, '/images/events/padel-yoga.jpg', 'center'], [/paella/i, '/images/padel-paella-2.jpg', 'center 85%']];

  var L = (document.documentElement.lang || 'en').slice(0, 2);
  if (['en', 'de', 'fr'].indexOf(L) < 0) L = 'en';
  var TX = {
    fr: { days: ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam'], time: function (h, m) { return h + 'h' + m; }, date: function (d, mo) { return d + '.' + mo; },
          week: function (a, b) { return 'Semaine du ' + a + ' au ' + b; }, wd: function (d, mo, same) { return same ? String(d) : d + '.' + mo; }, we: function (d, mo) { return d + '.' + mo; },
          booked: function (a, b) { return a + ' sur ' + b + ' inscrits'; },
          go: 'S’inscrire', btn: 'Je m’inscris', cta: { schedule: 'Voir le programme', whatsapp: 'Inscription par WhatsApp' }, upd: 'Places mises à jour le ', all: 'Tous',
          empty: 'Aucun événement dans les 30 prochains jours pour ce filtre.', fail: 'Les événements n’ont pas pu être chargés.',
          pt: 'Voir tous nos événements sur Playtomic', full: 'complet' },
    de: { days: ['So', 'Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa'], time: function (h, m) { return h + ':' + m; }, date: function (d, mo) { return d + '.' + mo + '.'; },
          week: function (a, b) { return 'Woche vom ' + a + ' bis ' + b; }, wd: function (d, mo, same) { return same ? d + '.' : d + '.' + mo + '.'; }, we: function (d, mo) { return d + '.' + mo + '.'; },
          booked: function (a, b) { return a + ' von ' + b + ' gebucht'; },
          go: 'Anmelden', btn: 'Anmelden', cta: { schedule: 'Spielplan ansehen', whatsapp: 'Anmelden per WhatsApp' }, upd: 'Plätze aktualisiert am ', all: 'Alle',
          empty: 'In den nächsten 30 Tagen keine Events für diesen Filter.', fail: 'Die Events konnten nicht geladen werden.',
          pt: 'Alle Events auf Playtomic', full: 'ausgebucht' },
    en: { days: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], time: function (h, m) { return h + ':' + m; }, date: function (d, mo) { return d + '.' + mo; },
          week: function (a, b) { return 'Week of ' + a + ' to ' + b; }, wd: function (d, mo, same) { return same ? String(d) : d + '.' + mo; }, we: function (d, mo) { return d + '.' + mo; },
          booked: function (a, b) { return a + ' of ' + b + ' booked'; },
          go: 'Sign up', btn: 'Sign up', cta: { schedule: 'Check schedule', whatsapp: 'Sign up on WhatsApp' }, upd: 'Spots updated on ', all: 'All',
          empty: 'No events in the next 30 days for this filter.', fail: 'The events could not be loaded.',
          pt: 'See all our events on Playtomic', full: 'full' }
  }[L];
  var FILTERS = [['all', TX.all], ['Sion', 'Sion'], ['Salgesch', 'Salgesch'], ['padel', 'Padel'], ['pickleball', 'Pickleball']];
  var filter = 'all', events = [], failed = false;

  function esc(x) { return String(x == null ? '' : x).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function sod(d) { var x = new Date(d); x.setHours(0, 0, 0, 0); return x; }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function monday(d) { return addDays(sod(d), -((d.getDay() + 6) % 7)); }
  function safeUrl(u) { u = String(u || '').trim(); return /^https:\/\/[^\s"'<>]+$/i.test(u) ? u : ''; }

  // calendar description → { text, meta } ; descriptions may contain HTML from the calendar editor
  function parseDesc(raw) {
    var t = String(raw || '').replace(/<br\s*\/?>/gi, '\n').replace(/<\/(p|div|li)>/gi, '\n').replace(/<a [^>]*href="([^"]+)"[^>]*>[^<]*<\/a>/gi, '$1').replace(/<[^>]+>/g, '');
    var ta = document.createElement('textarea'); ta.innerHTML = t; t = ta.value.replace(/\r/g, '');
    var meta = {}, text = t, m = /(^|\n)\s*-{3,}\s*(\n|$)/.exec(t);
    if (m) {
      text = t.slice(0, m.index);
      t.slice(m.index + m[0].length).split('\n').forEach(function (line) {
        var kv = /^\s*([a-z_]+)\s*:\s*(.+?)\s*$/i.exec(line);
        if (kv) meta[kv[1].toLowerCase()] = kv[2];
      });
    }
    text = text.replace(/\s+/g, ' ').trim();
    var first = (/^(.+?[.!?])(\s|$)/.exec(text) || [null, text])[1];
    return { short: first, meta: m ? meta : null };
  }
  function places(meta) {
    var p = /^\s*(\d+)\s*\/\s*(\d+)\s*$/.exec((meta && meta.places) || '');
    return p && +p[2] > 0 ? { taken: Math.min(+p[1], +p[2]), total: +p[2] } : null;
  }

  function toEvent(ev, cal) {
    var title = (ev.summary || '').trim();
    var d = parseDesc(ev.description), meta = d.meta;
    var low = title.toLowerCase();
    if (meta) title = meta['title_' + L] || meta.title || title;
    if (!meta && !KEYS.some(function (k) { return low.indexOf(k) > -1; })) return null;   // internal entry (school groups, ETA, private)
    meta = meta || {};
    var allDay = !ev.start.dateTime;
    var start = allDay ? new Date(ev.start.date + 'T12:00:00') : new Date(ev.start.dateTime);
    var deflt = PHOTOS.filter(function (x) { return x[0].test(title); })[0];
    var style = (meta.style || (deflt ? 'hero' : 'white')).toLowerCase();
    if (['hero', 'dark', 'white'].indexOf(style) < 0) style = 'white';
    return { title: title, start: start, allDay: allDay, loc: cal.loc, style: style, short: (meta[L] || d.short),
      cta: (TX.cta[meta.cta] || ''), href: safeUrl(meta.playtomic) || safeUrl(meta.link) || sitePath(meta.link) || (/swiss ?tennis/i.test(title) ? 'https://www.swisstennis.ch' : ACADEMY[cal.loc]), pl: places(meta), icon: meta.icon || '', accent: meta.accent || '',
      photo: safeUrl(meta.photo) || (deflt ? deflt[1] : ''), photoPos: safeUrl(meta.photo) || !deflt ? '' : deflt[2], price: meta.price || '', updated: meta.updated || '', pickle: /pickleball/i.test(title) };
  }

  // site-relative link, e.g. /{lang}/rivella-league.html (English pages live at the root)
  function sitePath(u) { return u && /^\/[\w{}\/.-]*$/.test(u) ? u.replace('/{lang}', L === 'en' ? '' : '/' + L) : ''; }

  function whenLine(e, withLoc) {
    var d = e.start, s = TX.days[d.getDay()] + ' ' + TX.date(pad(d.getDate()), pad(d.getMonth() + 1));
    if (!e.allDay) s += ' · ' + TX.time(d.getHours(), pad(d.getMinutes()));
    if (withLoc) s += ' · ' + e.loc;
    return s;
  }
  function descHtml(s) { return esc(s).replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>'); }
  function titleHtml(e) {
    var t = esc(e.title), a = e.accent && esc(e.accent);
    if (!a) return t;
    var i = t.toLowerCase().indexOf(a.toLowerCase());
    return i > -1 ? t.slice(0, i) + '<em>' + t.slice(i, i + a.length) + '</em>' + t.slice(i + a.length) : t;
  }
  function pillHtml(e) { return e.pl ? '<span class="evw-pill">' + esc(TX.booked(e.pl.taken, e.pl.total)) + '</span>' : ''; }

  function card(e) {
    var full = !!e.pl && e.pl.taken >= e.pl.total, cls = 'evw-card ' + e.style + (full ? ' full' : '') + (e.photo ? ' has-photo' : '');
    var open = full ? '<div class="' + cls + '" aria-disabled="true">' : '<a class="' + cls + '" href="' + esc(e.href) + '" target="_blank" rel="noopener">';
    var close = full ? '</div>' : '</a>';
    var label = esc(e.title) + (full ? ' (' + TX.full + ')' : '');
    if (e.style === 'hero') {
      return open.replace('>', ' aria-label="' + label + '">') +
        '<div class="evw-hero-photo"' + (e.photo ? ' role="img" aria-label="' + esc(e.title) + '" style="background-image:url(\'' + esc(e.photo) + '\')' + (e.photoPos ? ';background-position:' + e.photoPos : '') + '"' : '') + '></div>' +
        '<div class="evw-hero-body"><span class="evw-when">' + esc(whenLine(e, true)) + '</span>' +
        '<h3 class="evw-name">' + titleHtml(e) + '</h3>' + (e.short ? '<p class="evw-desc">' + descHtml(e.short) + '</p>' : '') + pillHtml(e) +
        '<div class="evw-foot"><span class="evw-price">' + esc(e.price) + '</span><span class="evw-btn">' + esc(e.cta || TX.btn) + '</span></div></div>' + close;
    }
    return open.replace('>', ' aria-label="' + label + '">') +
      '<span class="evw-when">' + esc(whenLine(e, false)) + '</span>' + (e.icon ? '<span class="evw-icon" aria-hidden="true">' + esc(e.icon) + '</span>' : '') +
      '<h3 class="evw-name">' + esc(e.title) + '</h3>' + (e.short ? '<p class="evw-desc">' + descHtml(e.short) + '</p>' : '') + pillHtml(e) +
      '<div class="evw-foot"><span class="evw-where">' + esc(e.loc) + (e.price ? ' · <b>' + esc(e.price) + '</b>' : '') + '</span>' +
      '<span class="evw-go">→ ' + esc(e.cta || TX.go) + '</span></div>' + close;
  }

  function keep(e) {
    if (filter === 'Sion' || filter === 'Salgesch') return e.loc === filter;
    if (filter === 'pickleball') return e.pickle;
    if (filter === 'padel') return !e.pickle;
    return true;
  }

  function render() {
    var root = document.getElementById('evw-list');
    if (!root) return;
    var chips = document.getElementById('evw-chips');
    chips.innerHTML = FILTERS.map(function (f) {
      return '<button type="button" class="evw-chip" data-f="' + f[0] + '" aria-pressed="' + (f[0] === filter) + '">' + esc(f[1]) + '</button>';
    }).join('');
    chips.querySelectorAll('.evw-chip').forEach(function (b) { b.onclick = function () { filter = b.getAttribute('data-f'); render(); }; });
    var fail = '<p class="evw-msg">' + esc(TX.fail) + ' <a href="' + ACADEMY.Sion + '" target="_blank" rel="noopener">' + esc(TX.pt) + ' →</a></p>';
    if (failed && !events.length) { root.innerHTML = fail; return; }
    var list = events.filter(keep);
    if (!list.length) { root.innerHTML = '<p class="evw-msg">' + esc(TX.empty) + ' <a href="' + ACADEMY.Sion + '" target="_blank" rel="noopener">' + esc(TX.pt) + ' →</a></p>'; return; }
    var weeks = {}, order = [];
    list.forEach(function (e) { var k = monday(e.start).getTime(); if (!weeks[k]) { weeks[k] = []; order.push(k); } weeks[k].push(e); });
    var rank = { hero: 0, dark: 1, white: 2 };
    var html = order.sort(function (a, b) { return a - b; }).map(function (k) {
      var a = new Date(+k), b = addDays(a, 6), same = a.getMonth() === b.getMonth();
      var head = TX.week(TX.wd(String(a.getDate()), pad(a.getMonth() + 1), same), TX.we(pad(b.getDate()), pad(b.getMonth() + 1)));
      var items = weeks[k].slice().sort(function (x, y) { return rank[x.style] - rank[y.style] || x.start - y.start; });
      return '<div class="evw-week"><h2>' + esc(head) + '</h2><div class="evw-grid">' + items.map(card).join('') + '</div></div>';
    }).join('');
    var upd = list.map(function (e) { return e.updated; }).filter(Boolean).sort().pop();
    if (upd) {
      var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(upd);
      html += '<p class="evw-note">' + esc(TX.upd + (m ? m[3] + '.' + m[2] + '.' + m[1] : upd)) + '</p>';
    }
    root.innerHTML = html;
  }

  function load(cb) {
    var from = new Date(), to = addDays(sod(from), DAYS + 1);
    if (/[?&]demo=1/.test(location.search)) return cb(demo(), false);
    var timeout = new Promise(function (res) { setTimeout(function () { res(null); }, 8000); });
    var calls = CALENDARS.map(function (cal) {
      var url = 'https://www.googleapis.com/calendar/v3/calendars/' + encodeURIComponent(cal.id) + '/events?key=' + API_KEY +
        '&timeMin=' + from.toISOString() + '&timeMax=' + to.toISOString() + '&singleEvents=true&orderBy=startTime&maxResults=250';
      return fetch(url).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (j) { return { ok: true, items: (j.items || []).map(function (ev) { return { ev: ev, cal: cal }; }) }; })
        .catch(function () { return { ok: false, items: [] }; });
    });
    Promise.race([Promise.all(calls), timeout]).then(function (res) {
      if (!res) return cb([], true);
      var raw = [], ok = false;
      res.forEach(function (r) { ok = ok || r.ok; raw = raw.concat(r.items); });
      cb(raw, !ok);
    });
  }

  // ?demo=1: example data from the brief (13.–21.11.2026), to check the layout
  function demo() {
    var S = CALENDARS[1], G = CALENDARS[0];
    function ev(t, s, desc, cal) { return { ev: { summary: t, start: s.length > 10 ? { dateTime: s } : { date: s }, description: desc }, cal: cal || S }; }
    function blk(o) { return 'Interner Text.\n---\n' + Object.keys(o).map(function (k) { return k + ': ' + o[k]; }).join('\n'); }
    var up = '2026-11-09';
    return [
      ev('Padel+Yoga (Patricia + Coach)', '2026-11-21T09:30:00+01:00', blk({ title: 'Padel +Yoga', style: 'hero', accent: '+Yoga', icon: '🧘', price: '35 CHF', places: '3/8', updated: up,
        fr: '45 minutes de yoga avec Patricia sur le court, puis 45 minutes de padel avec un coach. Tous niveaux, 8 personnes max.',
        de: '45 Minuten Yoga mit Patricia auf dem Court, danach 45 Minuten Padel mit Coach. Alle Levels, max. 8 Personen.',
        en: '45 minutes of yoga with Patricia on court, then 45 minutes of padel with a coach. All levels, max. 8 people.' })),
      ev('Padel Paella', '2026-11-15T09:00:00+01:00', blk({ title: 'Padel +Paella', style: 'hero', accent: '+Paella', icon: '🥘', price: '35 CHF', places: '11/16', updated: up,
        fr: '2 heures de padel à ton niveau, puis une paella fraîche cuisinée à l’Academy et une boisson. 16 places max.',
        de: '2 Stunden Padel auf deinem Level, danach frische Paella aus der Academy-Küche und ein Drink. Max. 16 Plätze.' }), G),
      ev('Swisstennis P50', '2026-11-13T16:00:00+01:00', blk({ title: 'Swiss Tennis P50', style: 'dark', icon: '🏆',
        fr: 'Tournoi officiel Swiss Tennis à Salgesch : gagne des points de classement. Inscription via Swiss Tennis.',
        de: 'Offizielles Swiss-Tennis-Turnier in Salgesch: Sammle Ranking-Punkte. Anmeldung über Swiss Tennis.' }), G),
      ev('Padel +Pizza', '2026-11-13T11:00:00+01:00', blk({ icon: '🍕', price: '35 CHF', places: '2/8', updated: up,
        fr: 'Une pause de midi différente : 90 minutes de padel, puis pizza et boisson avec tout le monde.',
        de: 'Mittagspause mal anders: 90 Minuten Padel, danach Pizza und ein Getränk mit allen vom Platz.' }), G),
      ev('Racketero - Intermediate', '2026-11-13T20:30:00+01:00', blk({ title: 'Racketero Intermediate', icon: '🔥', price: '30 CHF', places: '16/16', updated: up,
        fr: 'Tournoi amical : 2 heures, 5 matchs par équipe, uniquement contre ton niveau. Seul ou à deux, boisson incluse.',
        de: 'Freundschaftsturnier: 2 Stunden, 5 Matches pro Team, nur gegen dein Level. Allein oder zu zweit, inkl. Getränk.' }), G),
      ev('Padel Initiation', '2026-11-14T10:00:00+01:00', blk({ title_fr: 'Initiation au padel', title_de: 'Padel-Einsteigerkurs', icon: '🎾', places: '4/8', updated: up,
        fr: 'Jamais joué ? Découvre le padel avec nos coachs certifiés, raquette à louer sur place.',
        de: 'Noch nie gespielt? Lerne Padel mit unseren zertifizierten Coaches, Schläger kannst du vor Ort mieten.' })),
      ev('Coaching: Playtomic Level-Session Padel', '2026-11-14T11:00:00+01:00', blk({ title: 'Padel Leveling', icon: '🎯',
        fr: 'Un coach évalue ton jeu et fixe ton niveau Playtomic, pour jouer des matchs à ton niveau.',
        de: 'Ein Coach bewertet dein Spiel und setzt dein Playtomic-Level, damit du passende Matches findest.' })),
      ev('Pickleball Mix & Match', '2026-11-15T10:00:00+01:00', blk({ icon: '🥒', price: '10 CHF', places: '6/16', updated: up,
        fr: 'Tous niveaux : on mélange les équipes, nouveaux partenaires à chaque tour. Location de raquette +2 CHF.',
        de: 'Für alle Levels: Wir mischen die Teams, jede Runde neue Mitspieler. Schlägermiete +2 CHF.' }), G),
      ev('ETA Sion groupe école', '2026-11-17T14:00:00+01:00', 'Interne.')
    ];
  }

  document.addEventListener('DOMContentLoaded', function () {
    var root = document.getElementById('evw-list');
    if (!root) return;
    load(function (raw, fail) {
      var now = new Date(), seen = {};
      failed = fail;
      events = [];
      raw.forEach(function (x) {
        if (!x.ev || x.ev.status === 'cancelled' || !x.ev.start) return;
        var e = toEvent(x.ev, x.cal);
        if (!e) return;
        var endOk = e.allDay ? sod(e.start) >= sod(now) : e.start >= addDays(now, -1 / 24);
        var k = e.title + '|' + e.loc + '|' + e.start.toISOString();
        if (!endOk || seen[k]) return;
        seen[k] = true;
        events.push(e);
      });
      events.sort(function (a, b) { return a.start - b.start; });
      render();
    });
  });
})();
