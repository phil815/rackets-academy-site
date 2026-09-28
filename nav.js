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

  var modal = document.createElement('div');
  modal.className = 'book-modal-overlay';
  modal.innerHTML = `
    <div class="book-modal">
      <button class="book-modal-close" aria-label="Close">×</button>
      <h3>Good to know before you book</h3>
      <ul>
        <li><strong>Forgot your racket?</strong> Rent one at the club for 3, 5 or 10 CHF (beginner / intermediate / pro) — pay directly with Twint.</li>
        <li><strong>Need balls?</strong> Available to buy on-site too.</li>
        <li><strong>Plans change?</strong> No problem — cancel free up to 24h before your booking, right in the app.</li>
      </ul>
      <a href="#" class="btn btn-green book-modal-continue" target="_blank" rel="noopener">Continue to Playtomic</a>
    </div>`;
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
  document.querySelectorAll('.shop-panel').forEach(function (panel) {
    panel.classList.toggle('active', panel.id === id);
  });
  document.querySelectorAll('.shop-bubble').forEach(function (bubble) {
    bubble.classList.toggle('active', bubble.id === 'bubble-' + id);
  });
  var target = document.getElementById(id);
  if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Shared "Buy Now" modal for both vouchers and rackets.
function openBuyModal(type, opts) {
  document.getElementById('modal-formType').value = type;
  document.getElementById('buy-modal-title').textContent = opts.title || '';
  document.getElementById('buy-modal-price').textContent = (opts.price || '') + ' CHF';
  document.getElementById('modal-price').value = opts.price || '';
  document.getElementById('modal-qty').value = opts.qty || '';
  document.getElementById('modal-racketModel').value = opts.racketModel || '';
  document.getElementById('modal-racketLabel').value = opts.racketLabel || '';

  var locationSelect = document.getElementById('modal-location');
  locationSelect.name = type === 'voucher' ? 'location' : 'pickupLocation';

  var giftWrap = document.getElementById('modal-gift-wrap');
  if (giftWrap) giftWrap.style.display = type === 'voucher' ? '' : 'none';

  var emailNote = document.getElementById('modal-email-note');
  if (emailNote) {
    emailNote.textContent = type === 'voucher'
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
  openBuyModal('voucher', {
    title: qty + '× Gift Voucher',
    price: price,
    qty: qty
  });
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

// "Next event" badges — reads live from the public Google Calendars
// (Events - Salgesch / Events - Sion). Needs a restricted Google Calendar
// API key filled in below (see instructions). Matches badges by keyword
// against event titles, e.g. <span data-next-event="Racketero"></span>.
(function () {
  function formatFullDate(d) {
    var days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    var months = ['January','February','March','April','May','June','July','August','September','October','November','December'];
    var day = d.getDate();
    var suffix = 'th';
    if (day % 10 === 1 && day !== 11) suffix = 'st';
    else if (day % 10 === 2 && day !== 12) suffix = 'nd';
    else if (day % 10 === 3 && day !== 13) suffix = 'rd';
    return days[d.getDay()] + ', ' + months[d.getMonth()] + ' ' + day + suffix;
  }
  var API_KEY = 'AIzaSyDm1T-ofSLpJVzfpMOzhp7LLzMK1Pg9vpM';
  var CALENDARS = [
    'c_06fae67e3da9afefbea72735459e8b237c81650b84fff9332d50ddaa66509191@group.calendar.google.com', // Events - Salgesch
    'c_3ef252ff359c72bd0187f71d11f948958588fceca659a6d89ae3888ee6710d68@group.calendar.google.com'  // Events - Sion
  ];

  document.addEventListener('DOMContentLoaded', function () {
    var badges = document.querySelectorAll('[data-next-event]');
    if (!badges.length || !API_KEY) return;

    var now = new Date().toISOString();
    var future = new Date(Date.now() + 1000 * 60 * 60 * 24 * 120).toISOString(); // 120-day window

    var timeout = new Promise(function (resolve) {
      setTimeout(function () { resolve([]); }, 6000); // never leave badges stuck
    });

    Promise.race([
      Promise.all(CALENDARS.map(function (calId) {
        var url = 'https://www.googleapis.com/calendar/v3/calendars/' + encodeURIComponent(calId) +
          '/events?key=' + API_KEY + '&timeMin=' + now + '&timeMax=' + future +
          '&singleEvents=true&orderBy=startTime&maxResults=100';
        return fetch(url).then(function (r) {
          if (!r.ok) { console.warn('Calendar fetch failed for', calId, r.status); return { items: [] }; }
          return r.json();
        }).catch(function (err) { console.warn('Calendar fetch error for', calId, err); return { items: [] }; });
      })),
      timeout
    ]).then(function (results) {
      var allEvents = results.flatMap(function (r) { return r.items || []; });

      badges.forEach(function (el) {
        var keywords = el.getAttribute('data-next-event').toLowerCase().split(',').map(function (k) { return k.trim(); });
        var match = allEvents
          .filter(function (ev) {
            var title = (ev.summary || '').toLowerCase();
            return keywords.some(function (k) { return title.includes(k); });
          })
          .sort(function (a, b) {
            var da = new Date(a.start.dateTime || a.start.date);
            var db = new Date(b.start.dateTime || b.start.date);
            return da - db;
          })[0];

        if (match) {
          var d = new Date(match.start.dateTime || match.start.date);
          var formatted = formatFullDate(d);
          el.textContent = 'Next: ' + formatted;
          el.classList.add('next-event-badge');
        } else {
          el.textContent = 'Ask us for the next date';
          el.classList.add('next-event-badge', 'next-event-badge--empty');
        }
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
    en: { title: 'Where do you want to play?', court: 'Book a court', course: 'Courses', sub: 'Pick your location', close: 'Close', sa: 'Padel · Pickleball · Tennis', si: 'Padel' },
    fr: { title: 'Où veux-tu jouer ?', court: 'Réserver', course: 'Cours', sub: 'Choisis ton lieu', close: 'Fermer', sa: 'Padel · Pickleball · Tennis', si: 'Padel' },
    de: { title: 'Wo möchtest du spielen?', court: 'Platz buchen', course: 'Kurse', sub: 'Wähle deinen Standort', close: 'Schliessen', sa: 'Padel · Pickleball · Tennis', si: 'Padel' }
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
    document.body.appendChild(bar);
    document.body.classList.add('has-sticky-book');
  });
})();

// ------------------------------------------------------------------
// Cookie consent — "Your serve" (Google Consent Mode v2)
// ------------------------------------------------------------------
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var T = {
    en: { t: 'Your serve', p: 'We use cookies for anonymous visitor stats — no ads, no tracking across sites. The ball is in your court.', yes: 'In · accept', no: 'Out · decline', more: 'Privacy', set: 'Cookie settings' },
    fr: { t: 'À toi de servir', p: 'On utilise des cookies pour des statistiques anonymes — pas de pub, pas de pistage. La balle est dans ton camp.', yes: 'In · accepter', no: 'Out · refuser', more: 'Confidentialité', set: 'Paramètres cookies' },
    de: { t: 'Dein Aufschlag', p: 'Wir nutzen Cookies für anonyme Besucherstatistiken — keine Werbung, kein Tracking. Der Ball liegt bei dir.', yes: 'In · annehmen', no: 'Out · ablehnen', more: 'Datenschutz', set: 'Cookie-Einstellungen' }
  }[L] || null;
  if (!T) return;
  function get() { try { return localStorage.getItem('ra_consent'); } catch (e) { return null; } }
  function choose(v) {
    try { localStorage.setItem('ra_consent', v); } catch (e) {}
    if (typeof gtag === 'function') gtag('consent', 'update', { analytics_storage: v });
    var el = document.getElementById('serve-banner');
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
        '<p class="sv-text">' + T.p + ' <a href="privacy-policy.html">' + T.more + '</a></p>' +
        '<div class="sv-btns">' +
          '<button type="button" class="sv-no">' + T.no + '</button>' +
          '<button type="button" class="sv-yes">' + T.yes + '</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(el);
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
// Shop checkout via fetch → Apps Script returns JSON {ok,url} → redirect
// to SumUp in the same tab. (Apps Script HTML pages run in a sandboxed
// iframe that can't auto-redirect — that caused the white screen.)
// ------------------------------------------------------------------
(function () {
  var L = (document.documentElement.lang || 'en').slice(0, 2);
  var MSG = {
    en: { wait: 'Preparing secure payment…', err: 'Something went wrong. Please try again or message us on WhatsApp.' },
    fr: { wait: 'Préparation du paiement sécurisé…', err: "Un problème est survenu. Réessaie ou écris-nous sur WhatsApp." },
    de: { wait: 'Sichere Zahlung wird vorbereitet…', err: 'Da ist etwas schiefgelaufen. Bitte versuch es nochmal oder schreib uns auf WhatsApp.' }
  }[L] || { wait: '…', err: 'Error' };

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (!form || form.id !== 'buy-modal-form' || form.dataset.fallback === '1') return;
    e.preventDefault();
    var btn = form.querySelector('button[type="submit"]');
    var label = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = MSG.wait; }
    var err = form.querySelector('.checkout-error');
    if (err) err.remove();

    var data = new URLSearchParams(new FormData(form));
    data.set('mode', 'json');
    fetch(form.action, { method: 'POST', body: data })
      .then(function (r) { return r.text(); })
      .then(function (txt) {
        var url = null;
        try { var j = JSON.parse(txt); if (j.ok && j.url) url = j.url; else if (j.error) throw new Error(j.error); }
        catch (x) {
          var m = txt.match(/https:(?:\\?\/){2}[^"'\s<\\]*sumup[^"'\s<\\]*/i);
          if (m) url = m[0].replace(/\\\//g, '/');
          else if (x && x.message && txt.charAt(0) === '{') throw x;
        }
        if (!url) throw new Error('no checkout url');
        window.location.href = url;
      })
      .catch(function (x) {
        if (x instanceof TypeError) { form.dataset.fallback = '1'; form.target = '_self'; form.submit(); return; }
        if (btn) { btn.disabled = false; btn.textContent = label; }
        var p = document.createElement('p');
        p.className = 'checkout-error';
        p.style.cssText = 'color:#c0392b; font-size:.9rem; margin:10px 0 0;';
        p.textContent = MSG.err + (x && x.message && x.message !== 'no checkout url' && !/fetch|network/i.test(x.message) ? ' (' + x.message + ')' : '');
        form.appendChild(p);
        if (window.console) console.error('checkout', x);
      });
  });
})();
