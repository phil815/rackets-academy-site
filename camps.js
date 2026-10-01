// Ski & Padel camp booking: weekend + package picker, live spots from the
// Shop Apps Script (?action=camps), and the shared SumUp pop-up modal
// (payment itself is handled by the checkout block in nav.js).
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var S = {
    en: { left: function (n) { return n === 1 ? 'Last spot!' : n + ' of 12 spots left'; }, sold: 'Sold out', total: 'Total', pp: 'per person', people: function (n) { return n === 1 ? '1 person' : n + ' people'; }, solo: 'Solo', group: 'Group of 4' },
    fr: { left: function (n) { return n === 1 ? 'Dernière place !' : n + ' places sur 12'; }, sold: 'Complet', total: 'Total', pp: 'par personne', people: function (n) { return n === 1 ? '1 personne' : n + ' personnes'; }, solo: 'Solo', group: 'Groupe de 4' },
    de: { left: function (n) { return n === 1 ? 'Letzter Platz!' : 'Noch ' + n + ' von 12 Plätzen'; }, sold: 'Ausgebucht', total: 'Total', pp: 'pro Person', people: function (n) { return n === 1 ? '1 Person' : n + ' Personen'; }, solo: 'Solo', group: '4er-Gruppe' }
  }[L] || null;
  if (!S) return;
  var PACKS = { single: { people: 1, pp: 1199 }, group4: { people: 4, pp: 999 } };
  var fmt = function (n) { return n.toLocaleString('de-CH').replace(/[,\u2019]/g, "'"); };

  document.addEventListener('DOMContentLoaded', function () {
    var box = document.getElementById('camp-book');
    var form = document.getElementById('buy-modal-form');
    if (!box || !form) return;
    var spots = {};

    function sel(name) { return box.querySelector('input[name="' + name + '"]:checked'); }

    function refresh() {
      box.querySelectorAll('input[name="camp"]').forEach(function (r) {
        var n = spots[r.value], el = r.parentNode.querySelector('.camp-spots');
        if (n === undefined || !el) return;
        el.textContent = n > 0 ? S.left(n) : S.sold;
        el.classList.toggle('low', n <= 4);
        r.disabled = n <= 0;
        if (r.disabled && r.checked) r.checked = false;
      });
      var c = sel('camp');
      if (!c) { var firstOpen = box.querySelector('input[name="camp"]:not(:disabled)'); if (firstOpen) firstOpen.checked = true; c = firstOpen; }
      var g = box.querySelector('input[name="pack"][value="group4"]');
      if (c && g) {
        var n = spots[c.value];
        g.disabled = n !== undefined && n < 4;
        if (g.disabled && g.checked) box.querySelector('input[name="pack"][value="single"]').checked = true;
      }
      var p = sel('pack'), pk = PACKS[p ? p.value : 'single'];
      var btn = document.getElementById('camp-go');
      document.getElementById('camp-sum-what').textContent = c ? c.getAttribute('data-label') + ' · ' + S.people(pk.people) : S.sold;
      document.getElementById('camp-sum-total').textContent = S.total + ' ' + fmt(pk.people * pk.pp) + ' CHF';
      if (btn) btn.disabled = !c;
    }

    box.addEventListener('change', refresh);
    refresh();

    fetch(form.action + '?action=camps')
      .then(function (r) { return r.json(); })
      .then(function (j) { if (j && j.ok && j.camps) { spots = j.camps; refresh(); } })
      .catch(function () {});

    window.openCampModal = function () {
      var c = sel('camp'), p = sel('pack');
      if (!c || !p) return;
      var pk = PACKS[p.value];
      var oldPane = document.querySelector('#buy-modal-overlay .pay-pane');
      if (oldPane) oldPane.remove();
      form.style.display = '';
      var b = form.querySelector('button[type="submit"]');
      if (b && b.dataset.label) { b.disabled = false; b.textContent = b.dataset.label; }
      var old = form.querySelector('.checkout-error'); if (old) old.remove();
      document.getElementById('modal-campId').value = c.value;
      document.getElementById('modal-campPackage').value = p.value;
      document.getElementById('modal-price').value = pk.people * pk.pp;
      document.getElementById('buy-modal-title').textContent = c.getAttribute('data-label') + ' · ' + (p.value === 'group4' ? S.group : S.solo);
      document.getElementById('buy-modal-price').textContent = fmt(pk.people * pk.pp) + ' CHF' + (pk.people > 1 ? ' (' + pk.people + ' × ' + pk.pp + ')' : '');
      var grp = document.getElementById('modal-group-wrap'), ta = grp.querySelector('textarea');
      grp.style.display = pk.people > 1 ? '' : 'none';
      ta.required = pk.people > 1;
      document.getElementById('buy-modal-overlay').classList.add('open');
    };
  });
})();
