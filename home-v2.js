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
