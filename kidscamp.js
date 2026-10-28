// Kids padel camps: live spots per week from the Shop Apps Script (?action=camps)
// and the shared SumUp pop-up modal (payment is handled by the checkout block in nav.js).
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var box = document.getElementById('kc-book');
    var form = document.getElementById('buy-modal-form');
    if (!box || !form) return;
    var fmt = function (n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, "'"); };
    var spots = {};

    function paint() {
      box.querySelectorAll('.kc-week').forEach(function (row) {
        var n = spots[row.getAttribute('data-camp')], el = row.querySelector('.kc-left'), btn = row.querySelector('.kc-book');
        if (n === undefined) return;
        el.textContent = n <= 0 ? box.dataset.sold : (n === 1 ? box.dataset.last : box.dataset.left.replace('{n}', n));
        el.classList.toggle('low', n <= 5);
        btn.disabled = n <= 0;
      });
    }

    fetch(form.action + '?action=camps')
      .then(function (r) { return r.json(); })
      .then(function (j) { if (j && j.ok && j.camps) { spots = j.camps; paint(); } })
      .catch(function () {});

    var sel = document.getElementById('kc-n'), wrap = document.getElementById('kc-kids-wrap'),
        list = document.getElementById('kc-kids'), hid = wrap.querySelector('input[name="participants"]'), pp = 0;

    function sync() {
      var names = list.querySelectorAll('.pp-name'), ages = list.querySelectorAll('.pp-age'), out = [];
      for (var k = 0; k < names.length; k++) out.push((k + 1) + '. ' + names[k].value.trim() + ' (' + ages[k].value + ')');
      hid.value = out.join('; ');
    }

    function render() {
      var n = Number(sel.value), old = [];
      list.querySelectorAll('.pp-row').forEach(function (r) { old.push([r.querySelector('.pp-name').value, r.querySelector('.pp-age').value]); });
      list.innerHTML = '';
      for (var i = 1; i <= n; i++) {
        var row = document.createElement('div'); row.className = 'pp-row';
        row.innerHTML = '<input type="text" class="pp-name" required maxlength="60" autocomplete="off" placeholder="' + wrap.dataset.kid + ' ' + i + '">' +
                        '<input type="number" class="pp-age" required min="5" max="15" inputmode="numeric" placeholder="' + wrap.dataset.age + '">';
        if (old[i - 1]) { row.children[0].value = old[i - 1][0]; row.children[1].value = old[i - 1][1]; }
        list.appendChild(row);
      }
      document.getElementById('modal-campPackage').value = 'kid' + n;
      document.getElementById('modal-price').value = n * pp;
      document.getElementById('buy-modal-price').textContent = box.dataset.total + ' ' + fmt(n * pp) + ' CHF' + (n > 1 ? ' (' + n + ' × ' + pp + ')' : '');
      sync();
    }
    sel.addEventListener('change', render);
    list.addEventListener('input', sync);

    box.addEventListener('click', function (e) {
      var b = e.target.closest('.kc-book');
      if (!b || b.disabled) return;
      var oldPane = document.querySelector('#buy-modal-overlay .pay-pane');
      if (oldPane) oldPane.remove();
      form.style.display = '';
      var sb = form.querySelector('button[type="submit"]');
      if (sb && sb.dataset.label) { sb.disabled = false; sb.textContent = sb.dataset.label; }
      var err = form.querySelector('.checkout-error'); if (err) err.remove();
      pp = Number(b.dataset.pp);
      var left = spots[b.dataset.camp];
      sel.querySelectorAll('option').forEach(function (o) { o.disabled = left !== undefined && Number(o.value) > left; });
      if (sel.selectedOptions[0] && sel.selectedOptions[0].disabled) sel.value = '1';
      document.getElementById('modal-campId').value = b.dataset.camp;
      document.getElementById('buy-modal-title').textContent = b.dataset.label;
      render();
      document.getElementById('buy-modal-overlay').classList.add('open');
    });
  });
})();
