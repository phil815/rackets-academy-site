// Padel+Dine ticket booking: ticket picker, live places from the Shop Apps
// Script (?action=tickets&event=…), sales start date, and the shared SumUp
// pop-up modal (payment itself is handled by the checkout block in nav.js).
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var EVENT = 'padel-dine-2026-11-07';
  var OPEN = new Date('2026-10-03T00:00:00+02:00').getTime();
  var EVENT_START = new Date('2026-11-07T10:00:00+01:00').getTime();
  var S = {
    en: { left: function (n, c) { return n === 1 ? 'Last place!' : n + ' of ' + c + ' places left'; }, sold: 'Sold out', total: 'Total', soon: 'Ticket sales open on Monday 5 October', over: 'Ticket sales are closed', team: 'Tournament + Dinner Party · team of 2', dinner: function (q) { return 'Dinner Party · ' + q + (q === 1 ? ' ticket' : ' tickets'); }, p: 'Player', g: 'Guest', you: 'you', name: 'First and last name', lvl: 'Playtomic level', booked: function (a, b) { return '✓ Already booked: ' + a + ' tournament ' + (a === 1 ? 'place' : 'places') + ' · ' + b + ' dinner ' + (b === 1 ? 'place' : 'places'); } },
    fr: { left: function (n, c) { return n === 1 ? 'Dernière place !' : n + ' places sur ' + c; }, sold: 'Complet', total: 'Total', soon: 'Billetterie ouverte dès le lundi 5 octobre', over: 'La billetterie est fermée', team: 'Tournoi + Dinner Party · équipe de 2', dinner: function (q) { return 'Dinner Party · ' + q + (q === 1 ? ' billet' : ' billets'); }, p: 'Joueur·se', g: 'Invité·e', you: 'toi', name: 'Prénom et nom', lvl: 'Niveau Playtomic', booked: function (a, b) { return '✓ Déjà réservé : ' + a + (a === 1 ? ' place' : ' places') + ' tournoi · ' + b + (b === 1 ? ' place' : ' places') + ' dîner'; } },
    de: { left: function (n, c) { return n === 1 ? 'Letzter Platz!' : 'Noch ' + n + ' von ' + c + ' Plätzen'; }, sold: 'Ausverkauft', total: 'Total', soon: 'Ticketverkauf ab Montag, 5. Oktober', over: 'Der Ticketverkauf ist geschlossen', team: 'Turnier + Dinner Party · 2er-Team', dinner: function (q) { return 'Dinner Party · ' + q + (q === 1 ? ' Ticket' : ' Tickets'); }, p: 'Spieler·in', g: 'Gast', you: 'du', name: 'Vor- und Nachname', lvl: 'Playtomic-Level', booked: function (a, b) { return '✓ Bereits vergeben: ' + a + (a === 1 ? ' Turnierplatz' : ' Turnierplätze') + ' · ' + b + (b === 1 ? ' Dinner-Platz' : ' Dinner-Plätze'); } }
  }[L] || null;
  if (!S) return;
  var TICKETS = { team: { people: 2, pp: 79, cap: 48 }, dinner: { pp: 59, cap: 52 } };

  document.addEventListener('DOMContentLoaded', function () {
    var box = document.getElementById('tk-book');
    var form = document.getElementById('buy-modal-form');
    if (!box || !form) return;
    var left = {}, qtyEl = document.getElementById('tk-qty');
    var btn = document.getElementById('tk-go'), note = document.getElementById('tk-note');

    function sel() { return box.querySelector('input[name="tk"]:checked'); }
    function qty() { return Math.max(1, Math.min(10, parseInt(qtyEl.value, 10) || 1)); }
    function people(t) { return t === 'team' ? 2 : qty(); }

    function refresh() {
      box.querySelectorAll('input[name="tk"]').forEach(function (r) {
        var n = left[r.value], el = r.parentNode.querySelector('.camp-spots');
        if (n === undefined || !el) return;
        el.textContent = n > 0 ? S.left(n, TICKETS[r.value].cap) : S.sold;
        el.classList.toggle('low', n <= 8);
        r.disabled = n < (r.value === 'team' ? 2 : 1);
        if (r.disabled && r.checked) r.checked = false;
      });
      var c = sel();
      if (!c) { c = box.querySelector('input[name="tk"]:not(:disabled)'); if (c) c.checked = true; }
      if (c && c.value === 'dinner' && left.dinner !== undefined && qty() > left.dinner) qtyEl.value = Math.max(1, left.dinner);
      document.getElementById('tk-qty-wrap').style.display = c && c.value === 'dinner' ? '' : 'none';
      var t = c ? c.value : null, amount = t ? people(t) * TICKETS[t].pp : 0;
      document.getElementById('tk-sum-what').textContent = t ? (t === 'team' ? S.team : S.dinner(qty())) : S.sold;
      document.getElementById('tk-sum-total').textContent = t ? S.total + ' ' + amount + ' CHF' : '';
      var now = Date.now(), closed = now < OPEN || now > EVENT_START;
      btn.disabled = !c || closed;
      note.textContent = now < OPEN ? S.soon : (now > EVENT_START ? S.over : '');
      note.style.display = note.textContent ? '' : 'none';
    }

    box.addEventListener('change', refresh);
    box.addEventListener('input', refresh);
    box.querySelectorAll('[data-step]').forEach(function (b) {
      b.addEventListener('click', function () { qtyEl.value = qty() + Number(b.getAttribute('data-step')); refresh(); });
    });
    refresh();

    fetch(form.action + '?action=tickets&event=' + EVENT)
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!(j && j.ok && j.tickets)) return;
        left = j.tickets; refresh();
        // social proof: places already taken (live: capacity minus places left)
        var el = document.getElementById('dn-booked');
        if (!el || left.team === undefined || left.dinner === undefined || Date.now() > EVENT_START) return;
        var a = Math.max(0, TICKETS.team.cap - left.team), b = Math.max(0, TICKETS.dinner.cap - left.dinner);
        if (a + b > 0) { el.textContent = S.booked(a, b); el.hidden = false; }
      })
      .catch(function () {});

    window.openTicketModal = function () {
      var c = sel();
      if (!c || btn.disabled) return;
      var t = c.value, n = people(t), amount = n * TICKETS[t].pp;
      var oldPane = document.querySelector('#buy-modal-overlay .pay-pane');
      if (oldPane) oldPane.remove();
      form.style.display = '';
      var b = form.querySelector('button[type="submit"]');
      if (b && b.dataset.label) { b.disabled = false; b.textContent = b.dataset.label; }
      var old = form.querySelector('.checkout-error'); if (old) old.remove();
      document.getElementById('modal-eventId').value = EVENT;
      document.getElementById('modal-ticket').value = t;
      document.getElementById('modal-qty').value = n;
      document.getElementById('modal-price').value = amount;
      document.getElementById('buy-modal-title').textContent = t === 'team' ? S.team : S.dinner(n);
      document.getElementById('buy-modal-price').textContent = amount + ' CHF' + (n > 1 ? ' (' + n + ' × ' + TICKETS[t].pp + ')' : '');
      var list = document.getElementById('modal-people'), hid = form.querySelector('input[name="participants"]');
      list.innerHTML = '';
      for (var i = 1; i <= n; i++) {
        var lbl = document.createElement('div'); lbl.className = 'pp-lbl';
        lbl.textContent = (t === 'team' ? S.p : S.g) + ' ' + i + (i === 1 ? ' (' + S.you + ')' : '');
        var row = document.createElement('div'); row.className = 'pp-row' + (t === 'team' ? '' : ' pp-one');
        row.innerHTML = '<input type="text" class="pp-name" required maxlength="60" autocomplete="' + (i === 1 ? 'name' : 'off') + '" placeholder="' + S.name + '">' +
          (t === 'team' ? '<input type="text" class="pp-lvl" maxlength="5" inputmode="decimal" placeholder="' + S.lvl + '">' : '');
        list.appendChild(lbl); list.appendChild(row);
      }
      var sync = function () {
        var names = list.querySelectorAll('.pp-name'), lv = list.querySelectorAll('.pp-lvl'), out = [];
        for (var k = 0; k < names.length; k++) out.push((k + 1) + '. ' + names[k].value.trim() + (lv[k] && lv[k].value ? ' (' + lv[k].value.trim() + ')' : ''));
        hid.value = out.join('; ');
      };
      list.oninput = sync; sync();
      var nameField = form.querySelector('input[name="buyerName"]');
      if (nameField) nameField.oninput = function () { var f1 = list.querySelector('.pp-name'); if (f1 && (!f1.value || f1.dataset.auto)) { f1.value = nameField.value; f1.dataset.auto = 1; sync(); } };
      document.getElementById('buy-modal-overlay').classList.add('open');
    };
  });
})();
