document.addEventListener('DOMContentLoaded', function () {
  var btn = document.querySelector('.nav-toggle');
  var links = document.querySelector('.navlinks');
  if (btn && links) {
    btn.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        links.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  document.querySelectorAll('.lang-switch').forEach(function (langSwitch) {
    var langBtn = langSwitch.querySelector('button');
    langBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      langSwitch.classList.toggle('open');
    });
    document.addEventListener('click', function () {
      langSwitch.classList.remove('open');
    });
  });
});

// "Before you book" info modal — shown once per session on primary booking links
document.addEventListener('DOMContentLoaded', function () {
  var triggers = document.querySelectorAll('[data-book-modal]');
  if (!triggers.length) return;

  var BL = (document.documentElement.lang || 'en').slice(0, 2);
  var BM = {
    en: { h: 'Good to know before you book', r: '<strong>No racket?</strong> Rent one at the club for 3, 5 or 10 CHF (beginner / intermediate / pro), pay with Twint.', b: '<strong>Need balls?</strong> Available to buy on-site.', c: '<strong>Plans change?</strong> Free cancellation up to 24 h before, right in the app.', go: 'Continue to Playtomic', x: 'Close' },
    fr: { h: 'Bon à savoir avant de réserver', r: '<strong>Pas de raquette ?</strong> Loue-la au club pour 3, 5 ou 10 CHF (débutant / intermédiaire / pro), paiement par Twint.', b: '<strong>Besoin de balles ?</strong> En vente sur place.', c: '<strong>Un imprévu ?</strong> Annulation gratuite jusqu\'à 24 h avant, directement dans l\'app.', go: 'Continuer vers Playtomic', x: 'Fermer' },
    de: { h: 'Gut zu wissen vor dem Buchen', r: '<strong>Kein Schläger?</strong> Miete einen im Club für 3, 5 oder 10 CHF (Einsteiger / Fortgeschritten / Pro), bezahlt wird mit Twint.', b: '<strong>Bälle nötig?</strong> Gibt es vor Ort zu kaufen.', c: '<strong>Etwas dazwischengekommen?</strong> Kostenlos stornieren bis 24 h vorher, direkt in der App.', go: 'Weiter zu Playtomic', x: 'Schliessen' }
  }[BL] || null;
  if (!BM) return;
  var modal = document.createElement('div');
  modal.className = 'book-modal-overlay';
  modal.innerHTML =
    '<div class="book-modal">' +
      '<button class="book-modal-close" aria-label="' + BM.x + '">×</button>' +
      '<h3>' + BM.h + '</h3>' +
      '<ul><li>' + BM.r + '</li><li>' + BM.b + '</li><li>' + BM.c + '</li></ul>' +
      '<a href="#" class="btn btn-green book-modal-continue" target="_blank" rel="noopener">' + BM.go + '</a>' +
    '</div>';
  document.body.appendChild(modal);

  var continueBtn = modal.querySelector('.book-modal-continue');
  var closeBtn = modal.querySelector('.book-modal-close');
  var pendingHref = null;

  triggers.forEach(function (el) {
    el.addEventListener('click', function (e) {
      if (sessionStorage.getItem('ra_book_modal_seen')) return; // don't nag repeat visitors
      e.preventDefault();
      pendingHref = el.getAttribute('href');
      continueBtn.setAttribute('href', pendingHref);
      modal.classList.add('open');
    });
  });

  function closeModal(){ modal.classList.remove('open'); }
  closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', function(e){ if(e.target === modal) closeModal(); });
  continueBtn.addEventListener('click', function(){
    sessionStorage.setItem('ra_book_modal_seen', '1');
    closeModal();
  });
});

// Shop forms — real submission to the Apps Script backend (SumUp checkout,
// voucher code pull / racket stock, email fulfillment). The form POSTs
// directly (real page navigation, not fetch) so there's no CORS issue —
// the Apps Script response redirects the browser to SumUp's hosted payment page.

// Shop category bubbles: show only the chosen panel (Vouchers or Rackets).
function showShopPanel(id) {
  // Online-shop behaviour (UX F6): every category is visible by default,
  // the chips just filter. id === 'all' shows everything.
  document.querySelectorAll('.shop-panel').forEach(function (panel) {
    panel.classList.toggle('active', id === 'all' || panel.id === id);
  });
  document.querySelectorAll('.shop-bubble').forEach(function (bubble) {
    bubble.classList.toggle('active', bubble.id === 'bubble-' + id);
  });
  var bar = document.querySelector('.shop-bubbles');
  if (bar) bar.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

document.addEventListener('DOMContentLoaded', function () {
  var bar = document.querySelector('.shop-bubbles');
  if (!bar) return;
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var X = {
    en: { all: 'All products', allr: 'All', u200: 'Up to 200 CHF', test: 'Test it · 10 CHF' },
    fr: { all: 'Tout le shop', allr: 'Toutes', u200: "Jusqu'à 200 CHF", test: 'Teste-la · 10 CHF' },
    de: { all: 'Alle Produkte', allr: 'Alle', u200: 'Bis 200 CHF', test: 'Testen · 10 CHF' }
  }[L] || { all: 'All', allr: 'All', u200: '≤ 200 CHF', test: 'Test · 10 CHF' };
  bar.classList.add('as-chips');
  var all = document.createElement('button');
  all.type = 'button'; all.className = 'shop-bubble'; all.id = 'bubble-all'; all.textContent = X.all;
  all.addEventListener('click', function () { showShopPanel('all'); });
  bar.insertBefore(all, bar.firstChild);
  document.querySelectorAll('.shop-panel').forEach(function (p) { p.classList.add('active'); });
  all.classList.add('active');

  // Racket filters (brand / price) + "test it" badge (UX F16)
  var rk = document.getElementById('rackets');
  if (!rk) return;
  var brand = '';
  rk.querySelectorAll('.racket-brand-heading, .racket-grid').forEach(function (el) {
    if (el.classList.contains('racket-brand-heading')) { brand = el.textContent.trim(); return; }
    el.setAttribute('data-brand', brand);
    el.querySelectorAll('.racket-card').forEach(function (c) {
      c.setAttribute('data-brand', brand);
      var pr = parseInt((c.querySelector('.racket-price') || {}).textContent, 10) || 0;
      c.setAttribute('data-price', pr);
      var a = c.querySelector('.racket-link');
      if (a && !c.querySelector('.racket-test')) {
        var t = document.createElement('a'); t.className = 'racket-test'; t.href = a.getAttribute('href'); t.textContent = X.test;
        c.insertBefore(t, c.querySelector('.racket-model'));
      }
    });
  });
  var brands = [];
  rk.querySelectorAll('.racket-brand-heading').forEach(function (h) { var b = h.textContent.trim(); if (brands.indexOf(b) < 0) brands.push(b); });
  var f = document.createElement('div'); f.className = 'racket-filter';
  var opts = [['*', X.allr]].concat(brands.map(function (b) { return [b, b]; })).concat([['u200', X.u200]]);
  opts.forEach(function (o, i) {
    var b = document.createElement('button'); b.type = 'button'; b.textContent = o[1]; b.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
    b.addEventListener('click', function () {
      f.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
      rk.querySelectorAll('.racket-card').forEach(function (c) {
        var ok = o[0] === '*' || (o[0] === 'u200' ? +c.getAttribute('data-price') <= 200 : c.getAttribute('data-brand') === o[0]);
        c.style.display = ok ? '' : 'none';
      });
      rk.querySelectorAll('.racket-grid').forEach(function (g) {
        var any = [].some.call(g.querySelectorAll('.racket-card'), function (c) { return c.style.display !== 'none'; });
        g.style.display = any ? '' : 'none';
        var h = g.previousElementSibling;
        if (h && h.classList.contains('racket-brand-heading')) h.style.display = any ? '' : 'none';
      });
    });
    f.appendChild(b);
  });
  var first = rk.querySelector('.racket-brand-heading');
  if (first) first.parentNode.insertBefore(f, first);
});

// Shared "Buy Now" modal for both vouchers and rackets.
function openBuyModal(type, opts) {
  var oldPane = document.querySelector('#buy-modal-overlay .pay-pane');
  if (oldPane) oldPane.remove();
  var bf = document.getElementById('buy-modal-form');
  if (bf) { bf.style.display = ''; var bb = bf.querySelector('button[type="submit"]'); if (bb && bb.dataset.label) { bb.disabled = false; bb.textContent = bb.dataset.label; } }
  document.getElementById('modal-formType').value = type;
  document.getElementById('buy-modal-title').textContent = opts.title || '';
  document.getElementById('buy-modal-price').textContent = (opts.price || '') + ' CHF';
  document.getElementById('modal-price').value = opts.price || '';
  document.getElementById('modal-qty').value = opts.qty || '';
  document.getElementById('modal-racketModel').value = opts.racketModel || '';
  document.getElementById('modal-racketLabel').value = opts.racketLabel || '';

  var locationSelect = document.getElementById('modal-location');
  locationSelect.name = type === 'racket' ? 'pickupLocation' : 'location';
  var durEl = document.getElementById('modal-duration');
  if (durEl) durEl.value = opts.duration || '';

  var giftWrap = document.getElementById('modal-gift-wrap');
  if (giftWrap) giftWrap.style.display = type === 'racket' ? 'none' : '';

  var emailNote = document.getElementById('modal-email-note');
  if (emailNote) {
    emailNote.textContent = type !== 'racket'
      ? emailNote.getAttribute('data-voucher')
      : emailNote.getAttribute('data-racket');
  }

  document.getElementById('buy-modal-overlay').classList.add('open');
}

function openVoucherModal() {
  var checked = document.querySelector('#voucher-options input[name="bundle"]:checked');
  if (!checked) return;
  var qty = checked.getAttribute('data-qty');
  var price = checked.getAttribute('data-price');
  var VL = { en: 'Gift Voucher', fr: 'Bon cadeau', de: 'Geschenkgutschein' }[(document.documentElement.lang || 'en').slice(0, 2)] || 'Gift Voucher';
  openBuyModal('voucher', {
    title: qty + '× ' + VL,
    price: price,
    qty: qty
  });
}

function openLessonModal() {
  var checked = document.querySelector('#lesson-options input[name="lesson"]:checked');
  if (!checked) return;
  var qty = parseInt((document.getElementById('lesson-qty') || {}).value || '1', 10);
  var dur = checked.value, price = qty * Number(checked.getAttribute('data-price'));
  var LL = { en: 'Coaching Voucher', fr: 'Bon de cours', de: 'Kurs-Gutschein' }[(document.documentElement.lang || 'en').slice(0, 2)] || 'Coaching Voucher';
  openBuyModal('lesson', { title: qty + '× ' + LL + ' ' + dur + ' Min', price: price, qty: qty, duration: dur });
}

document.addEventListener('DOMContentLoaded', function () {
  var overlay = document.getElementById('buy-modal-overlay');
  if (overlay) {
    var closeBtn = document.getElementById('buy-modal-close');
    if (closeBtn) closeBtn.addEventListener('click', function () {
      overlay.classList.remove('open');
    });
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) overlay.classList.remove('open');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') overlay.classList.remove('open');
    });
  }

});

// "Next event" badges + events agenda — reads live from the public Google
// Calendars (Events - Salgesch / Events - Sion). Badges match keywords against
// event titles, e.g. <span data-next-event="Racketero"></span>.
// <div data-agenda="8"></div> renders the next public events; only titles that
// match AGENDA below are shown, so internal entries (team events, cleaning…)
// never appear on the site.
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var LOC = { en: 'en-GB', fr: 'fr-CH', de: 'de-CH' }[L] || 'en-GB';
  var TXT = {
    en: { next: 'Next: ', none: 'Next date announced soon', empty: 'New dates coming soon — follow us on Instagram.' },
    fr: { next: 'Prochaine date : ', none: 'Prochaine date annoncée bientôt', empty: 'Nouvelles dates bientôt — suis-nous sur Instagram.' },
    de: { next: 'Nächstes Datum: ', none: 'Nächstes Datum folgt bald', empty: 'Neue Daten folgen bald — folg uns auf Instagram.' }
  }[L] || {};
  var WA = 'https://wa.me/41772780115?text=';
  // keyword(s) in calendar title → label + link per language (first match wins)
  var AGENDA = [
    { k: ['24h'], l: { en: 'NTO24 · 24h padel tournament', fr: 'NTO24 · tournoi de padel 24 h', de: 'NTO24 · 24-Std.-Padelturnier' }, h: '/padel4ever/' },
    { k: ['amazonia', 'dine'], l: { en: 'Padel +Dine powered by Instinct Amazonia', fr: 'Padel +Dine powered by Instinct Amazonia', de: 'Padel +Dine powered by Instinct Amazonia' }, h: 'padel-dine.html' },
    { k: ['ski'], l: { en: 'Ski &Padel weekend', fr: 'Week-end Ski &Padel', de: 'Ski &Padel Wochenende' }, h: 'ski-and-padel.html' },
    { k: ['rackemix'], l: { en: 'Rackemix', fr: 'Rackemix', de: 'Rackemix' }, wa: 'Rackemix' },
    { k: ['racketero - beginner'], l: { en: 'Racketero · Beginner', fr: 'Racketero · Débutants', de: 'Racketero · Einsteiger' }, h: 'racketero.html' },
    { k: ['racketero - intermediate'], l: { en: 'Racketero · Intermediate', fr: 'Racketero · Intermédiaires', de: 'Racketero · Fortgeschrittene' }, h: 'racketero.html' },
    { k: ['racketero'], l: { en: 'Racketero', fr: 'Racketero', de: 'Racketero' }, h: 'racketero.html' },
    { k: ['pickleball'], l: { en: 'Pickleball Mix & Match', fr: 'Pickleball Mix & Match', de: 'Pickleball Mix & Match' }, wa: 'Pickleball Mix & Match' },
    { k: ['paella'], l: { en: 'Padel+Paella', fr: 'Padel+Paella', de: 'Padel+Paella' }, h: 'padel-paella.html' },
    { k: ['wine'], l: { en: 'Padel+Wine', fr: 'Padel+Wine', de: 'Padel+Wine' }, h: 'padel-wine.html' },
    { k: ['beer'], l: { en: 'Padel+Beer', fr: 'Padel+Beer', de: 'Padel+Beer' }, wa: 'Padel+Beer' },
    { k: ['fitness'], l: { en: 'Padel+Fitness', fr: 'Padel+Fitness', de: 'Padel+Fitness' }, h: 'padel-fitness.html' },
    { k: ['rivella'], l: { en: 'Rivella League Final', fr: 'Finale de la Rivella League', de: 'Rivella League Finale' }, h: 'rivella-league.html' },
    { k: ['swisstennis', 'hyundai'], l: null, h: 'swiss-tennis.html' },
    { k: ['veyras tennis tournament kids'], l: { en: 'TC Veyras · Kids tennis tournament', fr: 'TC Veyras · Tournoi de tennis enfants', de: 'TC Veyras · Kinder-Tennisturnier' }, wa: 'TC Veyras', n: '41795885483' },
    { k: ['veyras'], l: { en: 'TC Veyras · Doubles tennis tournament', fr: 'TC Veyras · Tournoi de tennis en double', de: 'TC Veyras · Doppel-Tennisturnier' }, wa: 'TC Veyras', n: '41795885483' }
  ];
  var WA_MSG = { en: 'Hola! I am interested in {e}. Please keep me posted.', fr: 'Hola ! Je suis intéressé·e par {e}. Tenez-moi au courant.', de: 'Hola! Ich interessiere mich für {e}. Haltet mich auf dem Laufenden.' };

  var API_KEY = 'AIzaSyDm1T-ofSLpJVzfpMOzhp7LLzMK1Pg9vpM';
  var CALENDARS = [
    'c_06fae67e3da9afefbea72735459e8b237c81650b84fff9332d50ddaa66509191@group.calendar.google.com', // Events - Salgesch
    'c_3ef252ff359c72bd0187f71d11f948958588fceca659a6d89ae3888ee6710d68@group.calendar.google.com'  // Events - Sion
  ];

  function start(ev) { var s = ev.start.dateTime || ev.start.date; return s.length === 10 ? new Date(s + 'T12:00:00') : new Date(s); }
  function end(ev) { if (!ev.end) return null; var s = ev.end.dateTime || ev.end.date; return s.length === 10 ? new Date(new Date(s + 'T12:00:00').getTime() - 864e5) : new Date(s); }
  function fullDate(d) { var t = d.toLocaleDateString(LOC, { weekday: 'long', day: 'numeric', month: 'long' }); return t.charAt(0).toUpperCase() + t.slice(1); }
  function shortDate(d) { return d.toLocaleDateString(LOC, { weekday: 'short', day: 'numeric', month: 'short' }); }
  function esc(x) { return String(x).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function find(title) {
    var t = (title || '').toLowerCase();
    for (var i = 0; i < AGENDA.length; i++) if (AGENDA[i].k.some(function (k) { return t.indexOf(k) > -1; })) return AGENDA[i];
    return null;
  }

  document.addEventListener('DOMContentLoaded', function () {
    var badges = document.querySelectorAll('[data-next-event]');
    var agendas = document.querySelectorAll('[data-agenda]');
    if ((!badges.length && !agendas.length) || !API_KEY) return;

    var now = new Date().toISOString();
    var future = new Date(Date.now() + 1000 * 60 * 60 * 24 * 300).toISOString(); // ~10-month window

    var timeout = new Promise(function (resolve) { setTimeout(function () { resolve([]); }, 6000); });

    Promise.race([
      Promise.all(CALENDARS.map(function (calId) {
        var url = 'https://www.googleapis.com/calendar/v3/calendars/' + encodeURIComponent(calId) +
          '/events?key=' + API_KEY + '&timeMin=' + now + '&timeMax=' + future +
          '&singleEvents=true&orderBy=startTime&maxResults=250';
        return fetch(url).then(function (r) {
          if (!r.ok) { console.warn('Calendar fetch failed for', calId, r.status); return { items: [] }; }
          return r.json();
        }).catch(function (err) { console.warn('Calendar fetch error for', calId, err); return { items: [] }; });
      })),
      timeout
    ]).then(function (results) {
      var all = (results || []).flatMap(function (r) { return r.items || []; })
        .filter(function (ev) { return ev.status !== 'cancelled' && ev.start; })
        .filter(function (ev, i, arr) { var k = (ev.summary || '') + '|' + (ev.start.dateTime || ev.start.date); return arr.findIndex(function (x) { return (x.summary || '') + '|' + (x.start.dateTime || x.start.date) === k; }) === i; })
        .sort(function (a, b) { return start(a) - start(b); });

      badges.forEach(function (el) {
        var keywords = el.getAttribute('data-next-event').toLowerCase().split(',').map(function (k) { return k.trim(); });
        var match = all.filter(function (ev) {
          var title = (ev.summary || '').toLowerCase();
          return keywords.some(function (k) { return title.indexOf(k) > -1; });
        })[0];
        if (match) {
          el.textContent = (TXT.next || 'Next: ') + fullDate(start(match));
          el.classList.add('next-event-badge');
        } else {
          el.textContent = TXT.none || 'Ask us for the next date';
          el.classList.add('next-event-badge', 'next-event-badge--empty');
        }
      });

      agendas.forEach(function (box) {
        var max = parseInt(box.getAttribute('data-agenda'), 10) || 8;
        var perSeries = {}, rows = [];
        all.forEach(function (ev) {
          if (rows.length >= max) return;
          var m = find(ev.summary); if (!m) return;
          var key = m.k[0]; perSeries[key] = (perSeries[key] || 0) + 1;
          if (perSeries[key] > 2) return; // keep weekly series from flooding the list
          var label = m.l ? (m.l[L] || m.l.en) : (ev.summary || '').replace(/swisstennis/i, 'Swiss Tennis');
          var href = m.h || ((m.n ? 'https://wa.me/' + m.n + '?text=' : WA) + encodeURIComponent((WA_MSG[L] || WA_MSG.en).replace('{e}', label)));
          var s = start(ev), e = end(ev);
          var when = shortDate(s) + (e && e.toDateString() !== s.toDateString() ? ' – ' + shortDate(e) : '');
          rows.push('<a class="ev-row" href="' + esc(href) + '"' + (m.h ? '' : ' target="_blank" rel="noopener"') + '><span class="ev-when">' + esc(when) + '</span><span class="ev-what">' + esc(label) + '</span><span class="ev-go">→</span></a>');
        });
        box.innerHTML = rows.length ? rows.join('') : '<p class="ev-empty">' + esc(TXT.empty || '') + '</p>';
      });
    });
  });
})();

// ------------------------------------------------------------------
// Location picker (Salgesch / Sion), sticky mobile booking bar,
// remembered language choice. Added Sep 2026.
// ------------------------------------------------------------------
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var T = {
    en: { title: 'Where do you want to play?', court: 'Book a court', course: 'Courses', sub: 'Pick your location', close: 'Close', sa: 'Padel · Pickleball · Tennis · Spa · free parking', si: 'Padel · parking on site', tip: 'Racket rental 3–10 CHF · free cancellation up to 24 h before' },
    fr: { title: 'Où veux-tu jouer ?', court: 'Réserver', course: 'Cours', sub: 'Choisis ton lieu', close: 'Fermer', sa: 'Padel · Pickleball · Tennis · Spa · parking gratuit', si: 'Padel · parking sur place', tip: "Location de raquette 3–10 CHF · annulation gratuite jusqu'à 24 h avant" },
    de: { title: 'Wo möchtest du spielen?', court: 'Platz buchen', course: 'Kurse', sub: 'Wähle deinen Standort', close: 'Schliessen', sa: 'Padel · Pickleball · Tennis · Spa · Gratis-Parkplätze', si: 'Padel · Parkplätze vor Ort', tip: 'Schlägermiete 3–10 CHF · kostenlos stornieren bis 24 h vorher' }
  }[L] || null;
  if (!T) return;
  var URLS = {
    court: { sa: 'https://playtomic.com/tenant/f89dfa07-4283-453e-8be3-316f9bd060d3', si: 'https://playtomic.com/tenant/c2ce2a9e-ab52-4191-bf7f-0c0aa70a2701' },
    academy: { sa: 'https://tinyurl.com/Academy-Salgesch', si: 'https://tinyurl.com/Academy-Sion' }
  };

  function openPicker(kind) {
    var u = URLS[kind] || URLS.court;
    var ov = document.getElementById('loc-picker');
    if (!ov) {
      ov = document.createElement('div');
      ov.id = 'loc-picker';
      ov.setAttribute('role', 'dialog');
      ov.setAttribute('aria-modal', 'true');
      ov.innerHTML =
        '<div class="loc-sheet">' +
          '<button type="button" class="loc-close" aria-label="' + T.close + '">×</button>' +
          '<p class="loc-sub">' + T.sub + '</p>' +
          '<h3>' + T.title + '</h3>' +
          '<a class="loc-btn" data-loc="sa" target="_blank" rel="noopener"><strong>Salgesch</strong><span>' + T.sa + '</span></a>' +
          '<a class="loc-btn" data-loc="si" target="_blank" rel="noopener"><strong>Sion</strong><span>' + T.si + '</span></a>' +
          '<p class="loc-tip">' + T.tip + '</p>' +
        '</div>';
      document.body.appendChild(ov);
      ov.addEventListener('click', function (e) {
        if (e.target === ov || e.target.closest('.loc-close')) ov.classList.remove('open');
        var b = e.target.closest('.loc-btn');
        if (b) {
          try { localStorage.setItem('ra_loc', b.getAttribute('data-loc')); } catch (err) {}
          setTimeout(function () { ov.classList.remove('open'); }, 300);
        }
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') ov.classList.remove('open'); });
    }
    ov.querySelector('[data-loc="sa"]').href = u.sa;
    ov.querySelector('[data-loc="si"]').href = u.si;
    var last = null;
    try { last = localStorage.getItem('ra_loc'); } catch (err) {}
    ov.querySelectorAll('.loc-btn').forEach(function (b) { b.classList.toggle('last', b.getAttribute('data-loc') === last); });
    ov.classList.add('open');
  }
  window.openLocationPicker = openPicker;

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('[data-pick]');
    if (!a) return;
    e.preventDefault();
    openPicker(a.getAttribute('data-pick'));
  });

  // remember explicit language choice (used by the auto-language redirect)
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('.lang-menu a');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    var lang = h === '#' ? L : (/(^|\/)fr\//.test(h) ? 'fr' : (/(^|\/)de\//.test(h) ? 'de' : 'en'));
    try { localStorage.setItem('ra_lang', lang); } catch (err) {}
  });

  // sticky booking bar (mobile only, via CSS)
  document.addEventListener('DOMContentLoaded', function () {
    if (document.querySelector('.sticky-book')) return;
    var bar = document.createElement('div');
    bar.className = 'sticky-book';
    bar.innerHTML =
      '<button type="button" class="sb-court" data-pick="court">' + T.court + '</button>' +
      '<a class="sb-course" href="training.html">' + T.course + '</a>';
    if (/padel-dine/.test(location.pathname)) {
      var TK = { en: 'Get your tickets', fr: 'Prendre mes billets', de: 'Tickets sichern' }[L] || 'Get your tickets';
      bar.innerHTML = '<a class="sb-court" href="#tk-book">' + TK + '</a>';
    } else if (/ski-and-padel/.test(location.pathname)) {
      var SK = { en: 'Choose your weekend', fr: 'Choisir mon week-end', de: 'Wochenende wählen' }[L] || 'Choose your weekend';
      bar.innerHTML = '<a class="sb-court" href="#camp-book">' + SK + '</a>';
    } else if (/\/rackets\//.test(location.pathname)) {
      var buy = document.querySelector('.buy-btn'), tst = document.querySelector('.product-test-btn');
      var pr = (buy && (buy.getAttribute('onclick') || '').match(/price:(\d+)/)) || null;
      var RB = { en: ['Buy', 'Test · 10 CHF'], fr: ['Acheter', 'Tester · 10 CHF'], de: ['Kaufen', 'Testen · 10 CHF'] }[L] || ['Buy', 'Test'];
      bar.innerHTML = '<button type="button" class="sb-court">' + RB[0] + (pr ? ' · ' + pr[1] + ' CHF' : '') + '</button>' +
        (tst ? '<a class="sb-course" href="' + tst.getAttribute('href') + '" target="_blank" rel="noopener">' + RB[1] + '</a>' : '');
      bar.firstChild.addEventListener('click', function () { if (buy) buy.click(); });
    } else if (/shop\.html/.test(location.pathname)) {
      var SH = { en: ['🎁 Gift vouchers', 'Rackets'], fr: ['🎁 Bons cadeaux', 'Raquettes'], de: ['🎁 Gutscheine', 'Schläger'] }[L] || ['Vouchers', 'Rackets'];
      bar.innerHTML = '<button type="button" class="sb-court">' + SH[0] + '</button><button type="button" class="sb-course">' + SH[1] + '</button>';
      bar.children[0].addEventListener('click', function () { if (window.showShopPanel) showShopPanel('vouchers'); });
      bar.children[1].addEventListener('click', function () { if (window.showShopPanel) showShopPanel('rackets'); });
    } else if (/kids-birthday/.test(location.pathname)) {
      bar.innerHTML = '<a class="sb-court" href="#inquiry">' + ({ en: 'Request a birthday', fr: 'Demander un anniversaire', de: 'Geburtstag anfragen' }[L] || 'Request') + '</a>';
    } else if (/company-events/.test(location.pathname)) {
      bar.innerHTML = '<a class="sb-court" href="#inquiry">' + ({ en: 'Request an offer', fr: 'Demander une offre', de: 'Offerte anfragen' }[L] || 'Request') + '</a>';
    } else if (/training\.html/.test(location.pathname)) {
      var TR = { en: ['Intro course', 'Memberships'], fr: ["Cours d'initiation", 'Abonnements'], de: ['Einführungskurs', 'Abos'] }[L] || ['Intro', 'Plans'];
      bar.innerHTML = '<a class="sb-court" href="https://tinyurl.com/Academy-Sion" target="_blank" rel="noopener">' + TR[0] + '</a><a class="sb-course" href="#plans">' + TR[1] + '</a>';
    } else if (/spa-and-sauna/.test(location.pathname)) {
      var SP = { en: 'Book spa', fr: 'Réserver le spa', de: 'Spa buchen' }[L] || 'Book spa';
      bar.innerHTML = '<a class="sb-court" href="https://playtomic.com/clubs/rackets-academy-salgesch" target="_blank" rel="noopener">' + SP + '</a>' +
        '<a class="sb-course" href="#private">' + ({ en: 'Private spa', fr: 'Spa privé', de: 'Privat-Spa' }[L] || 'Private spa') + '</a>';
    }
    document.body.appendChild(bar);
    document.body.classList.add('has-sticky-book');

    // event pages: top banner promotes the event instead of court booking
    var EV = null;
    if (/padel-dine/.test(location.pathname)) EV = {
      en: ['🍽️ PADEL +DINE · SAT 7 NOV · SALGESCH', 'Get your tickets →'],
      fr: ['🍽️ PADEL +DINE · SAMEDI 7 NOV · SALGESCH', 'Prendre mes billets →'],
      de: ['🍽️ PADEL +DINE · SA 7. NOV · SALGESCH', 'Tickets sichern →'], h: '#tk-book' };
    else if (/ski-and-padel/.test(location.pathname)) EV = {
      en: ['⛷️ SKI & PADEL · FEBRUARY 2027 · 12 PLACES PER WEEKEND', 'Choose your weekend →'],
      fr: ['⛷️ SKI & PADEL · FÉVRIER 2027 · 12 PLACES PAR WEEK-END', 'Choisir mon week-end →'],
      de: ['⛷️ SKI & PADEL · FEBRUAR 2027 · 12 PLÄTZE PRO WOCHENENDE', 'Wochenende wählen →'], h: '#camp-book' };
    var track = EV && document.querySelector('.promo-track');
    if (track) {
      var tx = EV[L] || EV.en, one = '<span>' + tx[0] + ' — <a href="' + EV.h + '">' + tx[1] + '</a></span>';
      track.innerHTML = one + one + one;
    }
  });
})();

// ------------------------------------------------------------------
// Meta Pixel — measures which Instagram/Facebook ads lead to bookings.
// Loads ONLY after cookie consent ("In · accept").
// ------------------------------------------------------------------
var RA_PIXEL_ID = '1826093361488124';
function raPixelLoad() {
  if (!RA_PIXEL_ID || window.fbq) return;
  try { if (localStorage.getItem('ra_consent') !== 'granted') return; } catch (e) { return; }
  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
  n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,
  document,'script','https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', RA_PIXEL_ID);
  fbq('track', 'PageView');
}
function raPixel(name, params, custom, eventId) {
  if (typeof window.fbq !== 'function') return;
  if (eventId) fbq(custom ? 'trackCustom' : 'track', name, params || {}, { eventID: String(eventId) });
  else fbq(custom ? 'trackCustom' : 'track', name, params || {});
}
raPixelLoad();
// Value + product of a checkout form (hidden "price" field; camp/shop/ticket forms).
function raCheckoutParams(f) {
  var p = { currency: 'CHF' };
  var price = f && f.querySelector('[name="price"]');
  var v = price ? parseFloat(String(price.value).replace(/[^0-9.]/g, '')) : NaN;
  if (v > 0) p.value = v;
  var id = f && (f.querySelector('[name="campId"]') || f.querySelector('[name="racketModel"]') || f.querySelector('[name="formType"]'));
  if (id && id.value) p.content_name = id.value;
  var pkg = f && f.querySelector('[name="campPackage"]');
  if (pkg && pkg.value) p.content_category = pkg.value;
  return p;
}
// Back from the SumUp hosted payment page: ...?paid=<ref>&amount=<CHF> -> Purchase (once per ref).
(function () {
  try {
    var q = new URLSearchParams(location.search), ref = q.get('paid');
    if (!ref) return;
    var key = 'ra_paid_' + ref;
    if (!localStorage.getItem(key)) {
      raPixel('Purchase', { value: parseFloat(q.get('amount')) || 0, currency: 'CHF' }, false, ref);
      if (typeof gtag === 'function') gtag('event', 'purchase', { value: parseFloat(q.get('amount')) || 0, currency: 'CHF', transaction_id: ref });
      localStorage.setItem(key, '1');
    }
    q.delete('paid'); q.delete('amount');
    history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q : '') + location.hash);
  } catch (e) {}
})();
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a[href]');
  if (!a) return;
  var h = a.href;
  if (/playtomic\.com/.test(h)) raPixel('PlaytomicClick', { link: h }, true);
  else if (/wa\.me|whatsapp\.com/.test(h)) raPixel('Contact', { method: 'whatsapp' });
  else if (/tinyurl\.com\/RA-Plus/i.test(h)) raPixel('Lead', { content_name: 'Rackets+' });
}, true);
document.addEventListener('submit', function (e) {
  var f = e.target;
  if (f && /script\.google/.test(f.action || '')) raPixel('InitiateCheckout', raCheckoutParams(f));
}, true);

// ------------------------------------------------------------------
// Cookie consent — "Your serve" (Google Consent Mode v2)
// ------------------------------------------------------------------
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var T = {
    en: { s: 'Cookies for our stats and Meta ads. We never sell your data.', t: 'Your serve', p: 'We use cookies for visitor stats and to measure our Instagram & Facebook ads (Meta). We never sell your data. The ball is in your court.', yes: 'In · accept', no: 'Out · decline', more: 'Privacy', set: 'Cookie settings' },
    fr: { s: 'Cookies pour nos stats et nos pubs Meta. On ne vend jamais tes données.', t: 'À toi de servir', p: 'On utilise des cookies pour nos statistiques et pour mesurer nos pubs Instagram & Facebook (Meta). On ne vend jamais tes données. La balle est dans ton camp.', yes: 'In · accepter', no: 'Out · refuser', more: 'Confidentialité', set: 'Paramètres cookies' },
    de: { s: 'Cookies für unsere Statistik und Meta-Werbung. Wir verkaufen deine Daten nie.', t: 'Dein Aufschlag', p: 'Wir nutzen Cookies für Besucherstatistiken und um unsere Instagram- & Facebook-Werbung (Meta) zu messen. Wir verkaufen deine Daten nie. Der Ball liegt bei dir.', yes: 'In · annehmen', no: 'Out · ablehnen', more: 'Datenschutz', set: 'Cookie-Einstellungen' }
  }[L] || null;
  if (!T) return;
  function get() { try { return localStorage.getItem('ra_consent'); } catch (e) { return null; } }
  function choose(v) {
    try { localStorage.setItem('ra_consent', v); } catch (e) {}
    if (typeof gtag === 'function') gtag('consent', 'update', { analytics_storage: v });
    if (v === 'granted') raPixelLoad();
    var el = document.getElementById('serve-banner');
    document.body.classList.remove('consent-open');
    if (el) { el.classList.add('hit-' + (v === 'granted' ? 'in' : 'out')); setTimeout(function () { el.remove(); }, 650); }
  }
  function show() {
    if (document.getElementById('serve-banner')) return;
    var el = document.createElement('div');
    el.id = 'serve-banner';
    el.setAttribute('role', 'dialog');
    el.setAttribute('aria-label', T.t);
    el.innerHTML =
      '<div class="sv-court" aria-hidden="true"><span class="sv-net"></span><span class="sv-ball"></span></div>' +
      '<div class="sv-body">' +
        '<p class="sv-title">' + T.t + ' <span aria-hidden="true">🎾</span></p>' +
        '<p class="sv-text"><span class="sv-long">' + T.p + '</span><span class="sv-short">' + T.s + '</span> <a href="privacy-policy.html">' + T.more + '</a></p>' +
        '<div class="sv-btns">' +
          '<button type="button" class="sv-no">' + T.no + '</button>' +
          '<button type="button" class="sv-yes">' + T.yes + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(el);
    document.body.classList.add('consent-open');
    el.querySelector('.sv-yes').addEventListener('click', function () { choose('granted'); });
    el.querySelector('.sv-no').addEventListener('click', function () { choose('denied'); });
  }
  window.openCookieSettings = show;
  document.addEventListener('DOMContentLoaded', function () {
    var fb = document.querySelector('.footer-bottom');
    if (fb && !fb.querySelector('.cookie-settings')) {
      var s = document.createElement('span');
      s.innerHTML = '<a href="#" class="cookie-settings">' + T.set + '</a>';
      fb.appendChild(s);
      s.firstChild.addEventListener('click', function (e) { e.preventDefault(); show(); });
    }
    if (!get()) setTimeout(show, 900);
  });
})();

// ------------------------------------------------------------------
// Shop checkout: Apps Script creates the SumUp checkout and returns JSON
// {ok,id,url}; payment then happens in the SumUp card widget inside our
// modal (pop-up). Fallback: SumUp hosted payment page.
// ------------------------------------------------------------------
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var M = {
    en: { wait: 'Preparing secure payment…', err: 'Something went wrong. Please try again or message us on WhatsApp.', secure: 'Secure payment via SumUp', alt: 'Pay on the SumUp page instead', ok: 'Payment successful! 🎾', okText: 'Thank you! You will receive a confirmation by email within a few minutes.', fail: 'The payment did not go through. Please check your details or try another card.', loc: 'en-GB' },
    fr: { wait: 'Préparation du paiement sécurisé…', err: 'Un problème est survenu. Réessaie ou écris-nous sur WhatsApp.', secure: 'Paiement sécurisé via SumUp', alt: 'Payer plutôt sur la page SumUp', ok: 'Paiement réussi ! 🎾', okText: 'Merci ! Tu recevras une confirmation par e-mail dans quelques minutes.', fail: "Le paiement n'a pas abouti. Vérifie tes données ou essaie une autre carte.", loc: 'fr-CH' },
    de: { wait: 'Sichere Zahlung wird vorbereitet…', err: 'Da ist etwas schiefgelaufen. Bitte versuch es nochmal oder schreib uns auf WhatsApp.', secure: 'Sichere Zahlung über SumUp', alt: 'Stattdessen auf der SumUp-Seite bezahlen', ok: 'Zahlung erfolgreich! 🎾', okText: 'Danke! Du bekommst in wenigen Minuten eine Bestätigung per E-Mail.', fail: 'Die Zahlung hat nicht geklappt. Bitte prüf deine Angaben oder versuch eine andere Karte.', loc: 'de-CH' }
  }[L] || null;
  if (!M) return;
  var SDK = 'https://gateway.sumup.com/gateway/ecom/card/v2/sdk.js';

  function loadSdk(cb, fail) {
    if (window.SumUpCard) return cb();
    var t = setTimeout(fail, 8000), sc = document.createElement('script');
    sc.src = SDK;
    sc.onload = function () { clearTimeout(t); window.SumUpCard ? cb() : fail(); };
    sc.onerror = function () { clearTimeout(t); fail(); };
    document.head.appendChild(sc);
  }

  function showPay(form, j) {
    form.style.display = 'none';
    var pane = document.createElement('div');
    pane.className = 'pay-pane';
    pane.innerHTML =
      '<div class="pay-secure"><span aria-hidden="true">🔒</span> ' + M.secure + '</div>' +
      '<div id="sumup-card"></div>' +
      '<a class="pay-alt" href="' + j.url + '">' + M.alt + '</a>';
    form.parentNode.appendChild(pane);
    // Leaving for the SumUp page: count it, so these checkouts are not invisible.
    var alt = pane.querySelector('.pay-alt');
    if (alt) alt.addEventListener('click', function () {
      raPixel('AddPaymentInfo', { value: Number(j.amount) || 0, currency: 'CHF', content_name: 'sumup_hosted' });
    });
    loadSdk(function () {
      try {
        window.SumUpCard.mount({
          id: 'sumup-card',
          checkoutId: j.id,
          locale: M.loc,
          currency: 'CHF',
          amount: j.amount ? String(j.amount) : undefined,
          onResponse: function (type, body) {
            if (type === 'success') {
              pane.innerHTML = '<div class="pay-done"><h3>' + M.ok + '</h3><p>' + M.okText + '</p></div>';
              var pref = j.ref || j.id; // same id as the ?paid=<ref> return from the SumUp page -> no double count
              if (typeof gtag === 'function') gtag('event', 'purchase', { value: Number(j.amount) || 0, currency: 'CHF', transaction_id: pref });
              raPixel('Purchase', { value: Number(j.amount) || 0, currency: 'CHF' }, false, pref);
              try { localStorage.setItem('ra_paid_' + pref, '1'); } catch (x) {}
            } else if (type === 'fail' || type === 'error') {
              var n = pane.querySelector('.pay-note') || document.createElement('p');
              n.className = 'pay-note'; n.textContent = M.fail;
              pane.insertBefore(n, pane.querySelector('#sumup-card'));
            }
          }
        });
      } catch (x) { window.location.href = j.url; }
    }, function () { window.location.href = j.url; });
  }

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || form.id !== 'buy-modal-form' || form.dataset.fallback === '1') return;
    e.preventDefault();
    var btn = form.querySelector('button[type="submit"]');
    if (btn) { if (!btn.dataset.label) btn.dataset.label = btn.textContent; btn.disabled = true; btn.textContent = M.wait; }
    var old = form.querySelector('.checkout-error'); if (old) old.remove();

    var data = new URLSearchParams(new FormData(form));
    data.set('mode', 'json');
    data.set('lang', L);
    fetch(form.action, { method: 'POST', body: data })
      .then(function (r) { return r.text(); })
      .then(function (txt) {
        var j;
        try { j = JSON.parse(txt); } catch (x) { throw new Error('bad response'); }
        if (!j.ok) throw new Error(j.error || 'error');
        if (j.id) showPay(form, j); else window.location.href = j.url;
      })
      .catch(function (x) {
        if (x instanceof TypeError) { form.dataset.fallback = '1'; form.target = '_self'; form.submit(); return; }
        if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
        var p = document.createElement('p');
        p.className = 'checkout-error';
        p.textContent = M.err + (x && x.message && x.message !== 'bad response' ? ' (' + x.message + ')' : '');
        form.appendChild(p);
      });
  });
})();

// ------------------------------------------------------------------
// Shop: live racket prices + stock from the RacketStock sheet
// (Apps Script doGet ?action=stock). Static HTML stays as fallback.
// ------------------------------------------------------------------
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var cards = document.querySelectorAll('.racket-card');
    var form = document.getElementById('buy-modal-form');
    if (!cards.length || !form || !form.action) return;
    var L = (document.documentElement.lang || 'en').slice(0, 2);
    var SOLD = { en: 'Sold out', fr: 'Épuisé', de: 'Ausverkauft' }[L] || 'Sold out';
    var BUY = { en: 'Buy Now', fr: 'Acheter', de: 'Jetzt kaufen' }[L] || 'Buy Now';
    fetch(form.action + '?action=stock')
      .then(function (r) { return r.json(); })
      .then(function (j) {
        if (!j || !j.ok || !j.rackets) return;
        cards.forEach(function (card) {
          var btn = card.querySelector('.buy-btn');
          var src = (btn && (btn.getAttribute('onclick') || btn.dataset.onclick)) || '';
          var m = src.match(/racketModel:'([^']+)'/);
          if (!m || !j.rackets[m[1]]) return;
          var info = j.rackets[m[1]];
          var priceEl = card.querySelector('.racket-price');
          if (priceEl && info.price) priceEl.textContent = info.price + ' CHF';
          var call = src.replace(/price:\d+(\.\d+)?/, 'price:' + info.price);
          if (info.qty > 0) {
            card.classList.remove('sold-out');
            btn.disabled = false;
            btn.textContent = BUY;
            btn.setAttribute('onclick', call);
          } else {
            card.classList.add('sold-out');
            btn.dataset.onclick = call;
            btn.removeAttribute('onclick');
            btn.disabled = true;
            btn.textContent = SOLD;
          }
        });
      })
      .catch(function () { /* keep static prices */ });
  });
})();

// ------------------------------------------------------------------
// Shop: Product structured data (Google free listings / rich results),
// built from the racket cards after live prices are applied.
// ------------------------------------------------------------------
(function () {
  function build() {
    var cards = document.querySelectorAll('.racket-card');
    if (!cards.length || document.getElementById('ld-products') || document.getElementById('ld-product')) return;
    var items = [];
    cards.forEach(function (card, i) {
      var btn = card.querySelector('.buy-btn');
      var src = (btn && (btn.getAttribute('onclick') || btn.dataset.onclick)) || '';
      var label = (src.match(/racketLabel:'([^']+)'/) || [])[1];
      var model = (src.match(/racketModel:'([^']+)'/) || [])[1];
      var price = ((card.querySelector('.racket-price') || {}).textContent || '').replace(/[^\d.]/g, '');
      var img = card.querySelector('img');
      if (!label || !price) return;
      items.push({
        '@type': 'ListItem', position: i + 1,
        item: {
          '@type': 'Product',
          name: label.replace(' — ', ' '),
          sku: model,
          brand: { '@type': 'Brand', name: label.split(' ')[0] },
          image: img ? img.src : undefined,
          description: label + ' – padel racket, test it at Rackets Academy (Salgesch / Sion) before you buy.',
          offers: {
            '@type': 'Offer', price: price, priceCurrency: 'CHF',
            availability: card.classList.contains('sold-out') ? 'https://schema.org/OutOfStock' : 'https://schema.org/InStock',
            url: location.href.split('#')[0] + '#rackets',
            itemCondition: 'https://schema.org/NewCondition',
            hasMerchantReturnPolicy: { '@type': 'MerchantReturnPolicy', applicableCountry: 'CH', returnPolicyCategory: 'https://schema.org/MerchantReturnNotPermitted' },
            shippingDetails: { '@type': 'OfferShippingDetails', doesNotShip: true, shippingDestination: { '@type': 'DefinedRegion', addressCountry: 'CH' } },
            seller: { '@type': 'Organization', name: 'Rackets Academy' }
          }
        }
      });
    });
    if (!items.length) return;
    var s = document.createElement('script');
    s.type = 'application/ld+json'; s.id = 'ld-products';
    s.textContent = JSON.stringify({ '@context': 'https://schema.org', '@type': 'ItemList', name: 'Padel rackets', itemListElement: items });
    document.head.appendChild(s);
  }
  // after live stock (or 4s fallback)
  document.addEventListener('DOMContentLoaded', function () { setTimeout(build, 4000); });
})();

// ------------------------------------------------------------------
// Racket detail: pop-up on the shop page (URL = real product page, so
// Google indexes it and a refresh/share opens the full page).
// ------------------------------------------------------------------
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var T = {
    en: { h: 'Test it first', p: 'Rent this racket for 10 CHF and play a real match with it. If you buy it, we credit the 10 CHF to the price — completely risk-free.', btn: 'Book a test on WhatsApp', wa: "Hola! I'd like to test the {l}.", pick: 'Pick up in Salgesch or Sion · ready the next day', close: 'Close' },
    fr: { h: "Teste-la d'abord", p: "Loue cette raquette pour 10 CHF et joue un vrai match avec. Si tu l'achètes, on déduit les 10 CHF du prix — sans aucun risque.", btn: 'Réserver un test sur WhatsApp', wa: "Hola ! J'aimerais tester la {l}.", pick: 'Retrait à Salgesch ou Sion · prête dès le lendemain', close: 'Fermer' },
    de: { h: 'Erst testen', p: 'Miete dieses Racket für 10 CHF und spiel damit ein echtes Match. Kaufst du es, schreiben wir dir die 10 CHF gut — ganz ohne Risiko.', btn: 'Test per WhatsApp buchen', wa: 'Hola! Ich möchte das {l} testen.', pick: 'Abholung in Salgesch oder Sion · abholbereit ab dem nächsten Tag', close: 'Schliessen' }
  }[L];
  if (!T) return;
  var shopUrl = null, ov = null;

  function close(fromPop) {
    if (!ov || !ov.classList.contains('open')) return;
    ov.classList.remove('open');
    document.body.style.overflow = '';
    if (!fromPop && shopUrl) history.back();
    shopUrl = null;
  }

  function open(link) {
    var card = link.closest('.racket-card');
    var btn = card.querySelector('.buy-btn');
    var call = (btn && (btn.getAttribute('onclick') || btn.dataset.onclick)) || '';
    var label = ((call.match(/racketLabel:'([^']+)'/) || [])[1] || '').replace(' — ', ' ');
    var img = card.querySelector('img').src;
    var price = (card.querySelector('.racket-price') || {}).textContent || '';
    if (!ov) {
      ov = document.createElement('div');
      ov.id = 'product-modal';
      ov.innerHTML = '<div class="pm-sheet" role="dialog" aria-modal="true"><button type="button" class="pm-close" aria-label="' + T.close + '">×</button><div class="pm-body"></div></div>';
      document.body.appendChild(ov);
      ov.addEventListener('click', function (e) { if (e.target === ov || e.target.closest('.pm-close')) close(false); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(false); });
      window.addEventListener('popstate', function () { close(true); });
    }
    var wa = 'https://wa.me/41772780115?text=' + encodeURIComponent(T.wa.replace('{l}', label));
    var sold = card.classList.contains('sold-out');
    ov.querySelector('.pm-body').innerHTML =
      '<div class="pm-grid"><img src="' + img + '" alt="">' +
      '<div><p class="product-brand">' + label.split(' ')[0] + '</p><h2 class="pm-title">' + label + '</h2>' +
      '<div class="pm-price">' + price + '</div><p class="product-pickup">' + T.pick + '</p>' +
      '<button type="button" class="buy-btn pm-buy"' + (sold ? ' disabled' : '') + '>' + btn.textContent + '</button>' +
      '<div class="product-test"><h3>' + T.h + '</h3><p>' + T.p + '</p><a class="btn product-test-btn" href="' + wa + '" target="_blank" rel="noopener">' + T.btn + '</a></div></div></div>';
    ov.querySelector('.pm-buy').addEventListener('click', function () {
      close(false);
      setTimeout(function () { if (!sold) new Function(call)(); }, 60);
    });
    ov.classList.add('open');
    document.body.style.overflow = 'hidden';
    shopUrl = location.href;
    history.pushState({ racket: true }, '', link.getAttribute('href'));
    if (typeof gtag === 'function') gtag('event', 'view_item', { item_name: label });
  }

  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.racket-link');
    if (!a || e.metaKey || e.ctrlKey) return;
    e.preventDefault();
    open(a);
  });

  // product pages: keep structured data in sync with live price / stock
  document.addEventListener('DOMContentLoaded', function () {
    var ld = document.getElementById('ld-product'), buy = document.querySelector('.product-buy');
    if (!ld || !buy) return;
    setTimeout(function () {
      try {
        var d = JSON.parse(ld.textContent);
        d.offers.price = (buy.querySelector('.racket-price').textContent || '').replace(/[^\d.]/g, '') || d.offers.price;
        d.offers.availability = 'https://schema.org/' + (buy.classList.contains('sold-out') ? 'OutOfStock' : 'InStock');
        ld.textContent = JSON.stringify(d);
      } catch (x) {}
    }, 4000);
  });
})();

// open the right shop panel from a #vouchers / #rackets link
document.addEventListener('DOMContentLoaded', function () {
  var h = (location.hash || '').slice(1);
  if ((h === 'rackets' || h === 'vouchers' || h === 'floky') && document.getElementById(h) && typeof showShopPanel === 'function') showShopPanel(h);
});

// ------------------------------------------------------------------
// Homepage hero video: pick size by screen, WebM + MP4 sources,
// retry on first interaction (iOS low-power / autoplay policies)
// ------------------------------------------------------------------
(function () {
  document.addEventListener('DOMContentLoaded', function () {
    var v = document.querySelector('video.hero-bg');
    if (!v) return;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var save = navigator.connection && navigator.connection.saveData;
    if (reduce || save) return; // poster image stays
    var base = (window.innerWidth <= 760 ? v.getAttribute('data-mobile') : v.getAttribute('data-desktop')).replace(/\.mp4$/, '');
    [['.mp4', 'video/mp4'], ['.webm', 'video/webm']].forEach(function (s) {
      var el = document.createElement('source'); el.src = base + s[0]; el.type = s[1]; v.appendChild(el);
    });
    v.muted = true; v.defaultMuted = true; v.setAttribute('muted', ''); v.controls = false; v.disablePictureInPicture = true;
    v.addEventListener('pause', function () { if (!document.hidden) setTimeout(go, 300); });
    v.load();
    function go() { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
    v.addEventListener('canplay', go, { once: true });
    go();
    ['touchstart', 'scroll', 'click', 'mousemove', 'keydown'].forEach(function (ev) {
      window.addEventListener(ev, function once() { if (v.paused) go(); window.removeEventListener(ev, once); }, { passive: true });
    });
  });
})();

// ------------------------------------------------------------------
// Inquiry forms (kids birthday, company events) -> prefilled WhatsApp (UX F11)
// ------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('form.wa-inquiry').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = [].filter.call(f.querySelectorAll('[required]'), function (i) { return !i.value.trim(); });
      f.querySelectorAll('.iq-bad').forEach(function (x) { x.classList.remove('iq-bad'); });
      if (bad.length) { bad.forEach(function (i) { i.classList.add('iq-bad'); }); bad[0].focus(); return; }
      var lines = [f.getAttribute('data-intro')];
      f.querySelectorAll('input[data-label], textarea[data-label]').forEach(function (i) {
        if (i.value.trim()) lines.push('• ' + i.getAttribute('data-label') + ': ' + i.value.trim());
      });
      f.querySelectorAll('fieldset').forEach(function (fs) {
        var v = [].filter.call(fs.querySelectorAll('input:checked'), function () { return true; }).map(function (i) { return i.value; });
        if (v.length) lines.push('• ' + fs.querySelector('legend').textContent + ': ' + v.join(', '));
      });
      var url = 'https://wa.me/41772780115?text=' + encodeURIComponent(lines.join('\n'));
      if (typeof gtag === 'function') gtag('event', 'generate_lead', { form_id: f.id, page_path: location.pathname });
      if (typeof raPixel === 'function') raPixel('Lead', { content_name: f.id });
      var w = window.open(url, '_blank', 'noopener');
      if (!w) location.href = url;
    });
  });
});

// ------------------------------------------------------------------
// Racket specs (shape, weight, hardness, level) on shop cards + product
// pages, with shop filters. Data: /racket-specs.js (from the Shop sheet).
// ------------------------------------------------------------------
document.addEventListener('DOMContentLoaded', function () {
  var shop = document.getElementById('rackets');
  var prod = document.querySelector('.product-page[data-product]');
  if (!shop && !prod) return;
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var TR = {
    en: { Rund: 'Round', 'Träne': 'Teardrop', Diamant: 'Diamond', Weich: 'Soft', Mittel: 'Medium', Hart: 'Hard', Amateur: 'Amateur', Fortgeschritten: 'Advanced', Profi: 'Pro', Kopflastig: 'Head-heavy', Grifflastig: 'Head-light',
          shape: 'Shape', hard: 'Hardness', level: 'Level', weight: 'Weight', face: 'Face', core: 'Core', balance: 'Balance', any: 'All', specs: 'Specs', none: 'No racket matches these filters.' },
    fr: { Rund: 'Ronde', 'Träne': 'Larme', Diamant: 'Diamant', Weich: 'Souple', Mittel: 'Medium', Hart: 'Dure', Amateur: 'Amateur', Fortgeschritten: 'Confirmé', Profi: 'Expert', Kopflastig: 'En tête', Grifflastig: 'Au manche',
          shape: 'Forme', hard: 'Dureté', level: 'Niveau', weight: 'Poids', face: 'Surface', core: 'Mousse', balance: 'Équilibre', any: 'Tous', specs: 'Caractéristiques', none: 'Aucune raquette ne correspond à ces filtres.' },
    de: { shape: 'Form', hard: 'Härte', level: 'Niveau', weight: 'Gewicht', face: 'Schlagfläche', core: 'Kern', balance: 'Balance', any: 'Alle', specs: 'Technische Daten', none: 'Kein Schläger passt zu diesen Filtern.' }
  }[L] || {};
  function tr(v) { return TR[v] || v; }
  var BAL = { Mittel: { en: 'Even', fr: 'Équilibré', de: 'Ausgewogen' } };
  function trBal(v) { return (BAL[v] && BAL[v][L]) || tr(v); }

  function run() {
    var S = window.RA_SPECS || {};
    if (prod) {
      var d = S[prod.getAttribute('data-product')], info = prod.querySelector('.product-info');
      if (d && info && !info.querySelector('.product-specs')) {
        var rows = [['shape', tr(d.shape)], ['weight', d.weight ? d.weight + ' g' : ''], ['hard', tr(d.hard)], ['level', tr(d.level)], ['balance', trBal(d.balance)], ['face', d.face], ['core', d.core]];
        var dl = document.createElement('div'); dl.className = 'product-specs';
        dl.innerHTML = '<h3>' + TR.specs + '</h3><dl>' + rows.filter(function (r) { return r[1]; }).map(function (r) { return '<dt>' + TR[r[0]] + '</dt><dd>' + r[1] + '</dd>'; }).join('') + '</dl>';
        var facts = info.querySelector('.product-facts');
        info.insertBefore(dl, facts || null);
      }
    }
    if (!shop) return;
    var cards = [].slice.call(shop.querySelectorAll('.racket-card'));
    cards.forEach(function (c) {
      var a = c.querySelector('.racket-link'), id = a && (a.getAttribute('href').match(/rackets\/([^/.]+)\.html/) || [])[1], d = S[id];
      if (!d) return;
      c.setAttribute('data-shape', d.shape); c.setAttribute('data-hard', d.hard); c.setAttribute('data-level', d.level);
      if (!c.querySelector('.racket-spec')) {
        var sp = document.createElement('span'); sp.className = 'racket-spec';
        sp.textContent = [tr(d.shape), d.weight ? d.weight + ' g' : '', tr(d.hard), tr(d.level)].filter(Boolean).join(' · ');
        var price = c.querySelector('.racket-price'); c.insertBefore(sp, price);
      }
    });
    var bar = shop.querySelector('.racket-filter');
    if (!bar || shop.querySelector('.racket-selects')) return;
    var groups = [['shape', ['Rund', 'Träne', 'Diamant']], ['hard', ['Weich', 'Mittel', 'Hart']], ['level', ['Amateur', 'Fortgeschritten', 'Profi']]];
    var box = document.createElement('div'); box.className = 'racket-selects';
    groups.forEach(function (g) {
      var lab = document.createElement('label');
      lab.innerHTML = '<span>' + TR[g[0]] + '</span><select data-k="' + g[0] + '"><option value="">' + TR.any + '</option>' +
        g[1].map(function (v) { return '<option value="' + v + '">' + tr(v) + '</option>'; }).join('') + '</select>';
      box.appendChild(lab);
    });
    var empty = document.createElement('p'); empty.className = 'racket-empty'; empty.textContent = TR.none; empty.hidden = true;
    bar.parentNode.insertBefore(box, bar.nextSibling);
    box.parentNode.insertBefore(empty, box.nextSibling);
    function apply() {
      var sel = {}; box.querySelectorAll('select').forEach(function (s) { if (s.value) sel[s.getAttribute('data-k')] = s.value; });
      var shown = 0;
      cards.forEach(function (c) {
        var ok = Object.keys(sel).every(function (k) { return c.getAttribute('data-' + k) === sel[k]; });
        c.classList.toggle('spec-hide', !ok);
        if (ok && c.style.display !== 'none') shown++;
      });
      shop.querySelectorAll('.racket-grid').forEach(function (g) {
        var any = [].some.call(g.querySelectorAll('.racket-card'), function (c) { return c.style.display !== 'none' && !c.classList.contains('spec-hide'); });
        g.classList.toggle('spec-hide', !any);
        var h = g.previousElementSibling;
        if (h && h.classList.contains('racket-brand-heading')) h.classList.toggle('spec-hide', !any);
      });
      empty.hidden = shown > 0;
    }
    box.addEventListener('change', apply);
    bar.addEventListener('click', function () { setTimeout(apply, 0); });
  }
  if (window.RA_SPECS) return run();
  var s = document.createElement('script'); s.src = '/racket-specs.js?v=1'; s.onload = run; document.head.appendChild(s);
});
