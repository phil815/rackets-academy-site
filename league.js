/* Rackets Rivella League — live widget. Reads the public Google Sheet (CSV export) in the browser.
   Sheet: Groupes (gid 0) + Tableaux (gid 1880528437). No API key needed (sheet is "anyone with link"). */
(function () {
  var root = document.getElementById('league');
  if (!root) return;
  var SHEET = '1NjDd0YZtWGeiAPa5kK63ijzxMfuoaksbag3G8s3uxbo';
  var GID_GROUPS = '0', GID_BRACKET = '1880528437';
  var lang = (document.documentElement.lang || 'fr').slice(0, 2);
  var T = {
    fr: { finals: 'Phase finale', groups: 'Groupes', top: 'Top 16 (rangs 1–16)', low: 'Rangs 17–32', search: 'Trouve ton équipe…',
          team: 'Équipe', w: 'V', l: 'D', diff: '+/−', matches: 'Matchs', loading: 'Chargement du classement…',
          error: 'Le classement n\u2019a pas pu être chargé.', open: 'Ouvrir le Google Sheet', live: 'En direct depuis le Google Sheet',
          group: 'Groupe', tbd: 'à jouer', none: 'Aucune équipe trouvée.' },
    de: { finals: 'Finalphase', groups: 'Gruppen', top: 'Top 16 (Rang 1–16)', low: 'Rang 17–32', search: 'Finde dein Team…',
          team: 'Team', w: 'S', l: 'N', diff: '+/−', matches: 'Spiele', loading: 'Rangliste wird geladen…',
          error: 'Die Rangliste konnte nicht geladen werden.', open: 'Google Sheet öffnen', live: 'Live aus dem Google Sheet',
          group: 'Gruppe', tbd: 'offen', none: 'Kein Team gefunden.' },
    en: { finals: 'Final phase', groups: 'Groups', top: 'Top 16 (ranks 1–16)', low: 'Ranks 17–32', search: 'Find your team…',
          team: 'Team', w: 'W', l: 'L', diff: '+/−', matches: 'Matches', loading: 'Loading standings…',
          error: 'The standings could not be loaded.', open: 'Open the Google Sheet', live: 'Live from the Google Sheet',
          group: 'Group', tbd: 'to play', none: 'No team found.' }
  };
  T = T[lang] || T.fr;
  var SHEET_URL = 'https://docs.google.com/spreadsheets/d/' + SHEET + '/edit?usp=sharing';

  function csvUrl(gid) { return 'https://docs.google.com/spreadsheets/d/' + SHEET + '/export?format=csv&gid=' + gid + '&t=' + Date.now(); }
  function parseCSV(text) {
    var rows = [], row = [], f = '', q = false;
    for (var i = 0; i < text.length; i++) {
      var c = text[i];
      if (q) { if (c === '"') { if (text[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c; }
      else if (c === '"') q = true;
      else if (c === ',') { row.push(f); f = ''; }
      else if (c === '\n') { row.push(f); rows.push(row); row = []; f = ''; }
      else if (c !== '\r') f += c;
    }
    row.push(f); rows.push(row);
    return rows.map(function (r) { return r.map(function (x) { return x.trim(); }); });
  }
  function cell(r, i) { return (r && r[i]) || ''; }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function isPlaceholder(t) { return !t || /^(winner|loser|vainqueur|perdant|sieger|verlierer)\b/i.test(t) || t === 'WO' || t === 'TBD'; }
  function num(s) { var n = parseInt(s, 10); return isNaN(n) ? null : n; }
  function setsWon(a, b) { var w = 0; for (var i = 0; i < 3; i++) { var x = num(a[i]), y = num(b[i]); if (x !== null && y !== null && x !== y) { if (x > y) w++; } } return w; }
  function played(a, b) { for (var i = 0; i < 3; i++) if (num(a[i]) !== null || num(b[i]) !== null || a[i] === 'DNF' || b[i] === 'DNF') return true; return false; }

  /* ---------- Tableaux (bracket) ---------- */
  function parseBracket(rows) {
    var halves = [[0], [7]].map(function (h) {
      var o = h[0], title = '', sections = [], cur = null, pending = null;
      rows.forEach(function (r) {
        var a = cell(r, o), b = cell(r, o + 1), t = cell(r, o + 2), s = [cell(r, o + 3), cell(r, o + 4), cell(r, o + 5)];
        if (!title && a && !/^match/i.test(a) && !s[0]) { title = a; return; }
        if (a && !/^match/i.test(a)) { cur = { name: a, matches: [] }; sections.push(cur); pending = null; return; }
        if (/^match/i.test(a)) { pending = { label: a, A: { seed: b, team: t, sets: s } }; return; }
        if (pending && (t || b)) { pending.B = { seed: b, team: t, sets: s }; if (cur) cur.matches.push(pending); pending = null; }
      });
      return { title: title, sections: sections };
    });
    return halves;
  }

  /* ---------- Groupes ---------- */
  function parseGroups(rows) {
    var groups = [], g = null, rounds = [12, 17, 22];
    rows.forEach(function (r) {
      var e = cell(r, 4);
      if (/^(group|groupe|gruppe)\s*\d+/i.test(e)) { g = { name: e.replace(/^\D+/, ''), teams: [], rounds: rounds.map(function () { return { name: '', lines: [] }; }), _last: null }; groups.push(g); return; }
      if (!g) return;
      if (/^ranking$/i.test(e)) { rounds.forEach(function (c, k) { g.rounds[k].name = cell(r, c); }); return; }
      var name = cell(r, 6);
      if (name) {
        if (cell(r, 4)) { g._last = { seed: e, players: [name], w: num(cell(r, 7)) || 0, l: num(cell(r, 8)) || 0, gw: num(cell(r, 9)) || 0, gl: num(cell(r, 10)) || 0 }; g.teams.push(g._last); }
        else if (g._last) g._last.players.push(name);
      }
      rounds.forEach(function (c, k) {
        var team = cell(r, c);
        if (team && !/tour|round|runde/i.test(team)) g.rounds[k].lines.push({ team: team, sets: [cell(r, c + 1), cell(r, c + 2), cell(r, c + 3)] });
      });
    });
    groups.forEach(function (g) {
      g.teams.forEach(function (t) { t.name = t.players.join(' + '); });
      g.teams.sort(function (a, b) { return (b.w - a.w) || ((b.gw - b.gl) - (a.gw - a.gl)) || (b.gw - a.gw); });
      g.rounds.forEach(function (rd) { rd.matches = []; for (var i = 0; i + 1 < rd.lines.length; i += 2) rd.matches.push({ A: rd.lines[i], B: rd.lines[i + 1] }); });
    });
    return groups;
  }

  /* ---------- Render ---------- */
  function sideHTML(side, win, done) {
    var ph = isPlaceholder(side.team);
    return '<div class="lg-side' + (win ? ' win' : '') + (ph ? ' ph' : '') + '" data-team="' + esc(side.team.toLowerCase()) + '">' +
      '<span class="lg-team">' + esc(side.team || '—') + (side.seed ? ' <small>' + esc(side.seed) + '</small>' : '') + '</span>' +
      '<span class="lg-sets">' + side.sets.map(function (x) { return x ? '<b>' + esc(x) + '</b>' : ''; }).join('') + (done ? '' : '<em>' + T.tbd + '</em>') + '</span></div>';
  }
  function matchHTML(m) {
    var done = played(m.A.sets, m.B.sets), wa = setsWon(m.A.sets, m.B.sets), wb = setsWon(m.B.sets, m.A.sets);
    return '<div class="lg-match' + (done ? ' done' : '') + '">' + (m.label ? '<div class="lg-label">' + esc(m.label) + '</div>' : '') +
      sideHTML(m.A, done && wa > wb, done) + sideHTML(m.B, done && wb > wa, done) + '</div>';
  }
  function bracketHTML(half) {
    return half.sections.map(function (s) {
      if (!s.matches.length) return '';
      return '<h3 class="lg-round">' + esc(s.name) + '</h3><div class="lg-grid">' + s.matches.map(matchHTML).join('') + '</div>';
    }).join('');
  }
  function groupHTML(g) {
    var rows = g.teams.map(function (t, i) {
      var d = t.gw - t.gl;
      return '<tr data-team="' + esc(t.name.toLowerCase()) + '"><td class="pos">' + (i + 1) + '</td><td class="tn">' + esc(t.name) + '</td><td>' + t.w + '</td><td>' + t.l + '</td><td class="' + (d > 0 ? 'pos-d' : d < 0 ? 'neg-d' : '') + '">' + (d > 0 ? '+' : '') + d + '</td></tr>';
    }).join('');
    var ms = g.rounds.map(function (rd) {
      if (!rd.matches.length) return '';
      return '<div class="lg-rd"><h4>' + esc(rd.name) + '</h4><div class="lg-grid sm">' + rd.matches.map(matchHTML).join('') + '</div></div>';
    }).join('');
    return '<div class="lg-group"><h3>' + T.group + ' ' + esc(g.name) + '</h3>' +
      '<table class="lg-table"><thead><tr><th></th><th>' + T.team + '</th><th>' + T.w + '</th><th>' + T.l + '</th><th>' + T.diff + '</th></tr></thead><tbody>' + rows + '</tbody></table>' +
      (ms ? '<details><summary>' + T.matches + '</summary>' + ms + '</details>' : '') + '</div>';
  }

  function render(groups, bracket) {
    var hasBracket = bracket.some(function (h) { return h.sections.some(function (s) { return s.matches.some(function (m) { return !isPlaceholder(m.A.team) || played(m.A.sets, m.B.sets); }); }); });
    var tab = hasBracket ? 'finals' : 'groups', half = 0;
    root.innerHTML =
      '<div class="lg-bar"><div class="lg-tabs" role="tablist">' +
      (hasBracket ? '<button data-tab="finals">' + T.finals + '</button>' : '') + '<button data-tab="groups">' + T.groups + '</button></div>' +
      '<input class="lg-search" type="search" placeholder="' + T.search + '" aria-label="' + T.search + '"></div>' +
      '<div class="lg-halves"><button data-half="0">' + T.top + '</button><button data-half="1">' + T.low + '</button></div>' +
      '<div class="lg-body"></div><p class="lg-empty" hidden>' + T.none + '</p>' +
      '<p class="lg-foot"><span class="dot"></span>' + T.live + ' · <a href="' + SHEET_URL + '" target="_blank" rel="noopener">' + T.open + '</a></p>';
    var body = root.querySelector('.lg-body'), halvesBar = root.querySelector('.lg-halves'), search = root.querySelector('.lg-search');
    function draw() {
      root.querySelectorAll('[data-tab]').forEach(function (b) { b.classList.toggle('on', b.dataset.tab === tab); });
      root.querySelectorAll('[data-half]').forEach(function (b) { b.classList.toggle('on', +b.dataset.half === half); });
      halvesBar.hidden = tab !== 'finals';
      body.innerHTML = tab === 'finals' ? bracketHTML(bracket[half]) : '<div class="lg-groups">' + groups.map(groupHTML).join('') + '</div>';
      filter();
    }
    function filter() {
      var q = search.value.trim().toLowerCase(), any = false;
      body.querySelectorAll('[data-team]').forEach(function (el) { var hit = q && el.dataset.team.indexOf(q) > -1; el.classList.toggle('hit', !!hit); if (hit) any = true; });
      if (tab === 'groups') body.querySelectorAll('.lg-group').forEach(function (g) { g.hidden = !!q && !g.querySelector('.hit'); });
      else body.querySelectorAll('.lg-match').forEach(function (m) { m.hidden = !!q && !m.querySelector('.hit'); });
      if (tab === 'finals') body.querySelectorAll('.lg-round').forEach(function (h) { var grid = h.nextElementSibling; var vis = grid && [].some.call(grid.children, function (c) { return !c.hidden; }); h.hidden = !vis; grid.hidden = !vis; });
      root.querySelector('.lg-empty').hidden = !q || any;
    }
    root.addEventListener('click', function (e) {
      var b = e.target.closest('button'); if (!b) return;
      if (b.dataset.tab) { tab = b.dataset.tab; draw(); }
      if (b.dataset.half) { half = +b.dataset.half; draw(); }
    });
    search.addEventListener('input', function () {
      if (tab === 'finals' && search.value.trim()) {
        // jump to the half that contains the team
        var q = search.value.trim().toLowerCase();
        for (var h = 0; h < 2; h++) if (JSON.stringify(bracket[h]).toLowerCase().indexOf(q) > -1) { if (h !== half) { half = h; draw(); } break; }
      }
      filter();
    });
    draw();
  }

  root.innerHTML = '<p class="lg-loading">' + T.loading + '</p>';
  Promise.all([GID_GROUPS, GID_BRACKET].map(function (g) { return fetch(csvUrl(g), { credentials: 'omit' }).then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); }); }))
    .then(function (res) { render(parseGroups(parseCSV(res[0])), parseBracket(parseCSV(res[1]))); })
    .catch(function () { root.innerHTML = '<p class="lg-loading">' + T.error + ' <a href="' + SHEET_URL + '" target="_blank" rel="noopener">' + T.open + '</a></p>'; });
})();
