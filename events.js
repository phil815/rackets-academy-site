// Events page: 30-day calendar + category sections, fed by the same Google Calendars as nav.js.
(function () {
  var API_KEY = 'AIzaSyDm1T-ofSLpJVzfpMOzhp7LLzMK1Pg9vpM';
  var CALENDARS = [
    { id: 'c_06fae67e3da9afefbea72735459e8b237c81650b84fff9332d50ddaa66509191@group.calendar.google.com', loc: 'Salgesch' },
    { id: 'c_3ef252ff359c72bd0187f71d11f948958588fceca659a6d89ae3888ee6710d68@group.calendar.google.com', loc: 'Sion' }
  ];
  var WA = 'https://wa.me/41772780115?text=';
  var WA_MSG = 'Hola! I am interested in {e}. Please keep me posted.';
  var WINDOW_DAYS = 30;     // calendar view
  var FETCH_DAYS = 120;     // category sections look a bit further ahead

  // Categories, in display order. First keyword match wins; keywords match the calendar event title.
  var CATS = [
    { id: 'padel-plus',  name: 'Padel+ events',                       color: '#0077de', k: ['padel+', 'padel +', 'dine', 'amazonia', 'wine', 'paella', 'beer', 'fitness', 'yoga'] },
    { id: 'tournaments', name: 'Swiss Tennis & padel tournaments',    color: '#7b4fd1', k: ['swisstennis', 'hyundai', 'veyras', 'rivella'] },
    { id: 'coaching',    name: 'Coaching',                            color: '#22a06b', k: ['initiation', 'leveling', 'levelling', 'playtomic'] },
    { id: 'racketeros',  name: 'Racketeros',                          color: '#e07a1f', k: ['racketero'] },
    { id: 'pickleball',  name: 'Pickleball',                          color: '#2e9e5b', k: ['pickleball'] },
    { id: 'camps',       name: 'One-off events & Camps',              color: '#c2185b', k: ['24h', 'ski'] },
    { id: 'other',       name: 'More events',                         color: '#5e6b7a', k: ['rackemix'] }
  ];
  // Label and target page per event (first match wins). Anything without h gets a WhatsApp "notify me" link.
  var LINKS = [
    { k: ['24h'], label: 'NTO24 · 24h padel tournament', h: '/padel4ever/' },
    { k: ['amazonia', 'dine'], label: 'Padel +Dine powered by Instinct Amazonia', h: 'padel-dine.html' },
    { k: ['ski'], label: 'Ski &Padel weekend', h: 'ski-and-padel.html' },
    { k: ['rackemix'], label: 'Rackemix', h: 'rackemix.html' },
    { k: ['racketero - beginner'], label: 'Racketero · Beginner', h: 'racketero.html' },
    { k: ['racketero - intermediate'], label: 'Racketero · Intermediate', h: 'racketero.html' },
    { k: ['racketero'], label: 'Racketero', h: 'racketero.html' },
    { k: ['pickleball'], label: 'Pickleball Mix & Match', h: 'pickleball.html' },
    { k: ['paella'], label: 'Padel+Paella', h: 'padel-paella.html' },
    { k: ['wine'], label: 'Padel+Wine', h: 'padel-wine.html' },
    { k: ['beer'], label: 'Padel+Beer', h: 'padel-beer.html' },
    { k: ['fitness'], label: 'Padel+Fitness', h: 'padel-fitness.html' },
    { k: ['rivella'], label: 'Rivella League Final', h: 'rivella-league.html' },
    { k: ['swisstennis', 'hyundai'], label: null, h: 'swiss-tennis.html' },
    { k: ['veyras'], label: 'TC Veyras · Tennis tournament', n: '41795885483' },
    { k: ['initiation'], label: 'Initiation · Saturday 10–11, Sion', h: 'training.html' },
    { k: ['leveling', 'levelling', 'level-session', 'level session', 'playtomic'], label: 'Playtomic leveling · Saturday 11–12, Sion', h: 'training.html' }
  ];
  var FALLBACK_HREF = { camps: 'ski-and-padel.html', tournaments: 'swiss-tennis.html', racketeros: 'racketero.html', 'padel-plus': 'events.html' };

  var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  var DAYNAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  var active = {}; // category id -> true when shown
  CATS.forEach(function (c) { active[c.id] = true; });
  var events = [];
  var from;

  function esc(x) { return String(x).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function startOfDay(d) { var x = new Date(d); x.setHours(0, 0, 0, 0); return x; }
  function addDays(d, n) { var x = new Date(d); x.setDate(x.getDate() + n); return x; }
  function keyOf(d) { return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0'); }
  function startOf(ev) { var s = ev.start.dateTime || ev.start.date; return s.length === 10 ? new Date(s + 'T12:00:00') : new Date(s); }
  function timeOf(ev) { return ev.start.dateTime ? startOf(ev).toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }) : 'All day'; }
  function classify(title) {
    var t = (title || '').toLowerCase();
    for (var i = 0; i < CATS.length; i++) if (CATS[i].k.some(function (k) { return t.indexOf(k) > -1; })) return CATS[i];
    return null;
  }
  function linkFor(title) {
    var t = (title || '').toLowerCase();
    for (var i = 0; i < LINKS.length; i++) if (LINKS[i].k.some(function (k) { return t.indexOf(k) > -1; })) return LINKS[i];
    return null;
  }
  function catById(id) { return CATS.filter(function (c) { return c.id === id; })[0]; }

  function toEvent(ev, cal) {
    var cat = classify(ev.summary);
    if (!cat) return null;
    var m = linkFor(ev.summary);
    var label = m && m.label ? m.label : (ev.summary || '');
    var href = m && m.h ? m.h : null;
    var wa = href ? null : (WA + encodeURIComponent(WA_MSG.replace('{e}', label + ' (' + cal.loc + ')')));
    if (m && m.n && !href) wa = 'https://wa.me/' + m.n + '?text=' + encodeURIComponent(WA_MSG.replace('{e}', label));
    return { title: label, cat: cat, loc: cal.loc, start: startOf(ev), time: timeOf(ev), href: href, wa: wa, key: keyOf(startOf(ev)) };
  }

  function itemHtml(e) {
    var href = e.href || e.wa;
    var ext = e.href ? '' : ' target="_blank" rel="noopener"';
    var d = e.start;
    return '<a class="ev-item" data-cat="' + e.cat.id + '" href="' + esc(href) + '"' + ext + '>' +
      '<span class="ev-date"><b>' + d.getDate() + '</b><small>' + MONTHS[d.getMonth()] + '</small></span>' +
      '<span class="ev-info"><strong>' + esc(e.title) + '</strong>' +
      '<span class="ev-meta">' + DAYNAMES[(d.getDay() + 6) % 7] + ' · ' + esc(e.time) + ' · ' + esc(e.loc) + '</span></span>' +
      '<span class="ev-go">' + (e.href ? 'Details' : 'Notify me') + ' →</span></a>';
  }

  function inView(e) { return active[e.cat.id]; }

  function renderCalendar() {
    var grid = document.getElementById('ev-grid');
    var list = document.getElementById('ev-daylist');
    if (!grid || !list) return;
    var end = addDays(from, WINDOW_DAYS - 1);
    var byDay = {};
    events.forEach(function (e) {
      if (e.start < from || e.start > addDays(end, 1)) return;
      (byDay[e.key] = byDay[e.key] || []).push(e);
    });
    // header label
    var label = document.getElementById('ev-range');
    if (label) label.textContent = from.getDate() + ' ' + MONTHS[from.getMonth()] + ' – ' + end.getDate() + ' ' + MONTHS[end.getMonth()] + ' ' + end.getFullYear();

    // desktop grid: Monday-aligned weeks covering the window
    var gridStart = addDays(from, -((from.getDay() + 6) % 7));
    var html = '<div class="ev-dow">' + DAYNAMES.map(function (d) { return '<span>' + d + '</span>'; }).join('') + '</div><div class="ev-weeks">';
    for (var i = 0; i < 35; i++) {
      var d = addDays(gridStart, i);
      if (i > 0 && i % 7 === 0 && d > end) break;
      var k = keyOf(d);
      var out = d < from || d > end;
      var evs = (byDay[k] || []).filter(inView);
      html += '<button type="button" class="ev-cell' + (out ? ' out' : '') + (k === keyOf(new Date()) ? ' today' : '') + '" data-day="' + k + '"' + (evs.length ? '' : ' tabindex="-1"') + '>' +
        '<span class="ev-num">' + d.getDate() + '</span>' +
        evs.slice(0, 2).map(function (e) { return '<span class="ev-pill" style="background:' + e.cat.color + '">' + esc(e.time.slice(0, 5) === 'All d' ? 'All day' : e.time.slice(0, 5)) + ' ' + esc(e.title) + '</span>'; }).join('') +
        (evs.length > 2 ? '<span class="ev-more">+' + (evs.length - 2) + ' more</span>' : '') +
        '</button>';
    }
    html += '</div>';
    grid.innerHTML = html;

    // day list (mobile, and the day panel on desktop)
    var days = Object.keys(byDay).sort();
    list.innerHTML = days.length ? days.map(function (k) {
      var evs = byDay[k].filter(inView);
      if (!evs.length) return '';
      var d = startOf({ start: { date: k } });
      return '<div class="ev-day"><h3>' + DAYNAMES[(d.getDay() + 6) % 7] + ' ' + d.getDate() + ' ' + MONTHS[d.getMonth()] + '</h3>' + evs.map(itemHtml).join('') + '</div>';
    }).join('') : '<p class="ev-empty">No public events in the next 30 days. New dates coming soon, follow us on Instagram.</p>';

    grid.querySelectorAll('.ev-cell[data-day]').forEach(function (cell) {
      cell.addEventListener('click', function () { showDay(cell.getAttribute('data-day')); });
    });
  }

  function showDay(k) {
    var panel = document.getElementById('ev-daypanel');
    if (!panel) return;
    var evs = events.filter(function (e) { return e.key === k && inView(e); });
    var d = startOf({ start: { date: k } });
    panel.innerHTML = '<h3>' + DAYNAMES[(d.getDay() + 6) % 7] + ' ' + d.getDate() + ' ' + MONTHS[d.getMonth()] + '</h3>' +
      (evs.length ? evs.map(itemHtml).join('') : '<p class="ev-empty">Nothing planned this day.</p>');
    panel.hidden = false;
    panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function renderSections() {
    var root = document.getElementById('ev-sections');
    if (!root) return;
    root.innerHTML = CATS.map(function (c) {
      var mine = events.filter(function (e) { return e.cat.id === c.id && e.start >= from; }).slice(0, 3);
      var body = mine.length ? mine.map(itemHtml).join('') :
        '<p class="ev-empty">Next dates announced soon. <a href="' + esc(FALLBACK_HREF[c.id] || WA) + '"' + (FALLBACK_HREF[c.id] ? '' : ' target="_blank" rel="noopener"') + '>' + (FALLBACK_HREF[c.id] ? 'See details' : 'Ask us on WhatsApp') + ' →</a></p>';
      return '<section class="ev-sec" id="sec-' + c.id + '" data-cat="' + c.id + '"' + (active[c.id] ? '' : ' hidden') + '>' +
        '<h2><span class="ev-dot" style="background:' + c.color + '"></span>' + esc(c.name) + '</h2>' +
        '<div class="ev-items">' + body + '</div></section>';
    }).join('');
  }

  function renderChips() {
    var bar = document.getElementById('ev-chips');
    if (!bar) return;
    bar.innerHTML = CATS.map(function (c) {
      return '<button type="button" class="ev-chip" data-cat="' + c.id + '" aria-pressed="' + active[c.id] + '" style="--c:' + c.color + '">' + esc(c.name) + '</button>';
    }).join('');
    bar.querySelectorAll('.ev-chip').forEach(function (b) {
      b.addEventListener('click', function () {
        var id = b.getAttribute('data-cat');
        active[id] = !active[id];
        b.setAttribute('aria-pressed', active[id]);
        renderSections();
        renderCalendar();
      });
    });
  }

  function setStatus(msg) { var s = document.getElementById('ev-status'); if (s) s.textContent = msg || ''; }

  document.addEventListener('DOMContentLoaded', function () {
    if (!document.getElementById('ev-grid')) return;
    from = startOfDay(new Date());
    var to = addDays(from, FETCH_DAYS);
    var timeout = new Promise(function (resolve) { setTimeout(function () { resolve(null); }, 8000); });
    var fetches = CALENDARS.map(function (cal) {
      var url = 'https://www.googleapis.com/calendar/v3/calendars/' + encodeURIComponent(cal.id) +
        '/events?key=' + API_KEY + '&timeMin=' + from.toISOString() + '&timeMax=' + to.toISOString() +
        '&singleEvents=true&orderBy=startTime&maxResults=250';
      return fetch(url).then(function (r) { return r.ok ? r.json() : { items: [] }; })
        .then(function (json) { return (json.items || []).map(function (ev) { return { ev: ev, cal: cal }; }); })
        .catch(function () { return []; });
    });
    Promise.race([Promise.all(fetches), timeout]).then(function (groups) {
      if (!groups) { setStatus('Dates could not be loaded. Follow us on Instagram for the latest.'); groups = []; }
      var seen = {};
      events = [];
      groups.forEach(function (g) {
        g.forEach(function (x) {
          if (!x.ev || x.ev.status === 'cancelled' || !x.ev.start) return;
          var e = toEvent(x.ev, x.cal);
          if (!e) return;
          var k = e.cat.id + '|' + e.title + '|' + e.loc + '|' + e.start.toISOString();
          if (seen[k]) return;
          seen[k] = true;
          events.push(e);
        });
      });
      events.sort(function (a, b) { return a.start - b.start; });
      renderChips();
      renderSections();
      renderCalendar();
      setStatus('');
    });
  });
})();
