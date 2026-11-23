// Startseite v2: Buchungsblock. Baut aus Standort, Sport und Tag den Playtomic-Link,
// damit der Besucher direkt bei den freien Zeiten landet. Ohne JavaScript führt der Knopf zur Clubseite Salgesch.
(function () {
  var card = document.querySelector('[data-hv2-book]');
  if (!card) return;
  var CLUBS = {
    salgesch: 'https://playtomic.com/clubs/rackets-academy-salgesch',
    sion: 'https://playtomic.com/clubs/rackets-academy-sion'
  };
  var cta = card.querySelector('.hv2-cta');
  var note = card.querySelector('.hv2-note');
  var state = { club: 'salgesch', sport: 'PADEL', day: '0' };

  function pad(n) { return (n < 10 ? '0' : '') + n; }
  function dateFor(day) {
    var d = new Date();
    if (day === '1') d.setDate(d.getDate() + 1);
    if (day === 'we') {               // nächster Samstag; am Wochenende selbst: heute
      var w = d.getDay();             // 0 = Sonntag, 6 = Samstag
      if (w !== 0 && w !== 6) d.setDate(d.getDate() + (6 - w));
    }
    return d.getFullYear() + '-' + pad(d.getMonth() + 1) + '-' + pad(d.getDate());
  }
  function render() {
    var sionOnly = state.club === 'sion';
    if (sionOnly && state.sport !== 'PADEL') state.sport = 'PADEL';   // Pickleball und Tennis nur in Salgesch
    card.querySelectorAll('.hv2-pill').forEach(function (b) {
      var on = (b.dataset.club && b.dataset.club === state.club) ||
               (b.dataset.sport && b.dataset.sport === state.sport) ||
               (b.dataset.day && b.dataset.day === state.day);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (b.dataset.sport && b.dataset.sport !== 'PADEL') b.disabled = sionOnly;
    });
    cta.href = CLUBS[state.club] + '?date=' + dateFor(state.day) + '&sport=' + state.sport;
    if (note) note.textContent = sionOnly ? note.dataset.sion : note.dataset.std;
    loadFree();
  }

  // Freie Padel-Plätze nach Tagesabschnitt (Web-App «Free slots»). Ohne Adresse oder bei einem Fehler
  // bleibt der Bereich unsichtbar und der Knopf führt wie bisher zu Playtomic.
  var free = card.querySelector('.hv2-free');
  var FREE_URL = card.getAttribute('data-free-url') || '';
  var run = 0;
  function loadFree() {
    if (!free) return;
    var mine = ++run;
    free.hidden = true;                               // nie die Zahlen einer früheren Auswahl stehen lassen
    if (!FREE_URL || state.sport !== 'PADEL' || !window.fetch) { free.hidden = true; return; }
    fetch(FREE_URL + '?club=' + state.club + '&date=' + dateFor(state.day))
      .then(function (r) { return r.json(); })
      .then(function (d) {
        if (mine !== run) return;                       // inzwischen wurde etwas anderes gewählt
        if (!d || !d.ok || !d.parts) { free.hidden = true; return; }
        var names = free.dataset.parts.split('|');
        var keys = ['morning', 'afternoon', 'evening'];
        var html = '';
        d.parts.forEach(function (p) {
          var i = keys.indexOf(p.key);
          if (i < 0 || p.past) return;
          var n = Number(p.courts) || 0;
          var txt = n === 0 ? free.dataset.full : (n === 1 ? free.dataset.one : free.dataset.n.replace('{n}', n));
          html += '<span class="hv2-part' + (n === 0 ? ' hv2-part-full' : '') + '"><b>' + names[i] + '</b> ' + txt + '</span>';
        });
        if (!html) { free.hidden = true; return; }
        free.innerHTML = '<p class="hv2-free-lead">' + free.dataset.lead + '</p><div class="hv2-parts">' + html +
          '</div><p class="hv2-free-asof">' + free.dataset.asof.replace('{t}', String(d.updated || '').replace(/[^0-9:]/g, '')) + '</p>';
        free.hidden = false;
      })
      .catch(function () { if (mine === run) free.hidden = true; });
  }
  card.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.hv2-pill');
    if (!b || b.disabled) return;
    if (b.dataset.club) state.club = b.dataset.club;
    if (b.dataset.sport) state.sport = b.dataset.sport;
    if (b.dataset.day) state.day = b.dataset.day;
    render();
  });
  render();
})();
