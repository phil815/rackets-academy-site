// Ski &Padel camp booking: weekend + package picker, live spots from the
// Shop Apps Script (?action=camps), and the shared SumUp pop-up modal
// (payment itself is handled by the checkout block in nav.js).
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var S = {
    en: { now: 'Pay now', dep: 'deposit', rest: 'rest by 15 Jan 2027', left: function (n) { return n === 1 ? 'Last spot!' : n + ' of 12 spots left'; }, sold: 'Sold out', total: 'Total', pp: 'per person', people: function (n) { return n === 1 ? '1 person' : n + ' people'; }, solo: 'Individual', duo: 'Duo', group: 'Crew of 4' },
    fr: { now: 'À payer maintenant', dep: 'acompte', rest: 'solde au 15.01.2027', left: function (n) { return n === 1 ? 'Dernière place !' : n + ' places sur 12'; }, sold: 'Complet', total: 'Total', pp: 'par personne', people: function (n) { return n === 1 ? '1 personne' : n + ' personnes'; }, solo: 'Individuel', duo: 'Duo', group: 'Bande de 4' },
    de: { now: 'Jetzt zahlen', dep: 'Anzahlung', rest: 'Rest bis 15.01.2027', left: function (n) { return n === 1 ? 'Letzter Platz!' : 'Noch ' + n + ' von 12 Plätzen'; }, sold: 'Ausgebucht', total: 'Total', pp: 'pro Person', people: function (n) { return n === 1 ? '1 Person' : n + ' Personen'; }, solo: 'Einzelplatz', duo: 'Duo', group: '4er-Crew' }
  }[L] || null;
  if (!S) return;
  // Early-bird until 30.11.2026, then +75 CHF p.p. (same rule as Camps.gs, which decides the real amount)
  var LATE = Date.now() >= new Date('2026-12-01T00:00:00+01:00').getTime() ? 75 : 0, DEPOSIT = 200;
  var PACKS = { single: { people: 1, pp: 1199 + LATE }, duo: { people: 2, pp: 1199 + LATE }, group4: { people: 4, pp: 999 + LATE } };
  var fmt = function (n) { return n.toLocaleString('de-CH').replace(/[,\u2019]/g, "'"); };

  document.addEventListener('DOMContentLoaded', function () {
    // Meta optimisation goal (Guti 02.11.2026): a visitor who stays at least 10 s with the page visible.
    // Fires once per page view; fbq exists only after cookie consent.
    (function () {
      var seen = 0, last = Date.now(), done = false;
      var t = setInterval(function () {
        var now = Date.now();
        if (document.visibilityState === 'visible') seen += now - last;
        last = now;
        if (!done && seen >= 10000) {
          done = true; clearInterval(t);
          if (window.fbq) window.fbq('trackCustom', 'SkiPadelEngaged10s');
          if (window.gtag) window.gtag('event', 'engaged_10s', { page_type: 'ski_padel' });
        }
      }, 1000);
    })();
    var box = document.getElementById('camp-book');
    var form = document.getElementById('buy-modal-form');
    if (!box || !form) return;
    var spots = {};

    function sel(name) { return box.querySelector('input[name="' + name + '"]:checked'); }
    function payNow(pk) { var m = sel('paymode'); return m && m.value === 'deposit' ? pk.people * DEPOSIT : pk.people * pk.pp; }
    if (LATE) {
      var eb = document.getElementById('camp-early'); if (eb) eb.style.display = 'none';
      box.querySelectorAll('input[name="pack"]').forEach(function (r) {
        var el = r.parentNode.querySelector('.camp-pack-price'); if (el) el.firstChild.nodeValue = fmt(PACKS[r.value].pp) + ' CHF ';
        var note = r.parentNode.querySelector('.camp-pack-note');
        if (note && PACKS[r.value].people > 1) note.textContent = note.textContent.replace(/[\d']{4,} CHF/, fmt(PACKS[r.value].people * PACKS[r.value].pp) + ' CHF');
      });
    }

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
      if (c) {
        var n = spots[c.value];
        box.querySelectorAll('input[name="pack"]').forEach(function (r) {
          var need = PACKS[r.value].people;
          r.disabled = n !== undefined && n < need;
          if (r.disabled && r.checked) box.querySelector('input[name="pack"][value="single"]').checked = true;
        });
      }
      var p = sel('pack'), pk = PACKS[p ? p.value : 'single'];
      var btn = document.getElementById('camp-go');
      document.getElementById('camp-sum-what').textContent = c ? c.getAttribute('data-label') + ' · ' + S.people(pk.people) : S.sold;
      var m = sel('paymode'), dep = m && m.value === 'deposit';
      document.getElementById('camp-sum-total').textContent = S.total + ' ' + fmt(pk.people * pk.pp) + ' CHF' +
        (dep ? ' · ' + S.now + ' ' + fmt(payNow(pk)) + ' CHF (' + S.dep + ', ' + S.rest + ')' : '');
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
      var m = sel('paymode'), dep = m && m.value === 'deposit';
      document.getElementById('modal-price').value = payNow(pk);
      var pm = document.getElementById('modal-payMode'); if (pm) pm.value = dep ? 'deposit' : 'full';
      document.getElementById('buy-modal-title').textContent = c.getAttribute('data-label') + ' · ' + ({ single: S.solo, duo: S.duo, group4: S.group }[p.value]);
      document.getElementById('buy-modal-price').textContent = dep
        ? S.now + ': ' + fmt(payNow(pk)) + ' CHF (' + S.dep + ') · ' + S.total + ' ' + fmt(pk.people * pk.pp) + ' CHF, ' + S.rest
        : fmt(pk.people * pk.pp) + ' CHF' + (pk.people > 1 ? ' (' + pk.people + ' × ' + fmt(pk.pp) + ')' : '');
      var grp = document.getElementById('modal-group-wrap'), list = document.getElementById('modal-people'), hid = grp.querySelector('input[name="participants"]');
      list.innerHTML = '';
      for (var i = 1; i <= pk.people; i++) {
        var lbl = document.createElement('div'); lbl.className = 'pp-lbl';
        lbl.textContent = grp.dataset.pers + ' ' + i + (i === 1 ? ' (' + grp.dataset.you + ')' : '');
        var row = document.createElement('div'); row.className = 'pp-row';
        row.innerHTML = '<input type="text" class="pp-name" required maxlength="60" autocomplete="' + (i === 1 ? 'name' : 'off') + '" placeholder="' + grp.dataset.name + '">' +
                        '<input type="number" class="pp-age" required min="10" max="99" inputmode="numeric" placeholder="' + grp.dataset.age + '">';
        list.appendChild(lbl); list.appendChild(row);
      }
      var sync = function () {
        var names = list.querySelectorAll('.pp-name'), ages = list.querySelectorAll('.pp-age'), out = [];
        for (var k = 0; k < names.length; k++) out.push((k + 1) + '. ' + names[k].value.trim() + ' (' + ages[k].value + ')');
        hid.value = out.join('; ');
      };
      list.oninput = sync; sync();
      var nameField = form.querySelector('input[name="buyerName"]');
      if (nameField) nameField.oninput = function () { var f1 = list.querySelector('.pp-name'); if (f1 && (!f1.value || f1.dataset.auto)) { f1.value = nameField.value; f1.dataset.auto = 1; sync(); } };
      document.getElementById('buy-modal-overlay').classList.add('open');
    };
  });
})();
