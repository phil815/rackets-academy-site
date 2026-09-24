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

  var langSwitch = document.querySelector('.lang-switch');
  if (langSwitch) {
    var langBtn = langSwitch.querySelector('button');
    langBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      langSwitch.classList.toggle('open');
    });
    document.addEventListener('click', function () {
      langSwitch.classList.remove('open');
    });
  }
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
document.addEventListener('DOMContentLoaded', function () {
  var voucherForm = document.getElementById('voucher-form');
  if (voucherForm) {
    var priceField = document.getElementById('voucher-price');
    var qtyField = document.getElementById('voucher-qty');
    var syncBundle = function () {
      var checked = voucherForm.querySelector('input[name="bundle"]:checked');
      if (checked) {
        priceField.value = checked.getAttribute('data-price');
        qtyField.value = checked.getAttribute('data-qty');
      }
    };
    voucherForm.querySelectorAll('input[name="bundle"]').forEach(function (r) {
      r.addEventListener('change', syncBundle);
    });
    syncBundle(); // set initial values from the pre-checked option
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
