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

// Shop forms — WhatsApp stopgap until the Apps Script checkout is live.
// TODO(shop-backend): replace the wa.me redirect below with a real submit
// to the Apps Script Web App endpoint once it's deployed (SumUp checkout,
// voucher code pull, PDF generation). Field names are already backend-ready.
document.addEventListener('DOMContentLoaded', function () {
  var voucherForm = document.getElementById('voucher-form');
  if (voucherForm) {
    voucherForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(voucherForm);
      var bundleInput = voucherForm.querySelector('input[name="bundle"]:checked');
      var qty = bundleInput.getAttribute('data-qty');
      var price = bundleInput.getAttribute('data-price');
      var msg = `Hi! I'd like to order a gift voucher bundle:\n` +
        `- Bundle: ${qty}x 20 CHF (${price} CHF total)\n` +
        `- Name: ${fd.get('buyerName')}\n` +
        `- Email: ${fd.get('buyerEmail')}\n` +
        (fd.get('giftMessage') ? `- Gift message: ${fd.get('giftMessage')}\n` : '');
      window.open('https://wa.me/41762914369?text=' + encodeURIComponent(msg), '_blank');
    });
  }

  var racketForm = document.getElementById('racket-form');
  if (racketForm) {
    racketForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(racketForm);
      var msg = `Hi! I'd like to order a racket:\n` +
        `- Model: ${fd.get('racketModel')}\n` +
        `- Pickup: ${fd.get('pickupLocation')}\n` +
        `- Name: ${fd.get('buyerName')}\n` +
        `- Email: ${fd.get('buyerEmail')}`;
      window.open('https://wa.me/41762914369?text=' + encodeURIComponent(msg), '_blank');
    });
  }
});

// "Next event" badges — reads live from the public Google Calendars
// (Events - Salgesch / Events - Sion). Needs a restricted Google Calendar
// API key filled in below (see instructions). Matches badges by keyword
// against event titles, e.g. <span data-next-event="Racketero"></span>.
(function () {
  var API_KEY = ''; // <-- fill in: Google Cloud API key restricted to Calendar API + this domain
  var CALENDARS = [
    'c_06fae67e3da9afefbea72735459e8b237c81650b84fff9332d50ddaa66509191@group.calendar.google.com', // Events - Salgesch
    'c_3ef252ff359c72bd0187f71d11f948958588fceca659a6d89ae3888ee6710d68@group.calendar.google.com'  // Events - Sion
  ];

  document.addEventListener('DOMContentLoaded', function () {
    var badges = document.querySelectorAll('[data-next-event]');
    if (!badges.length || !API_KEY) return;

    var now = new Date().toISOString();
    var future = new Date(Date.now() + 1000 * 60 * 60 * 24 * 120).toISOString(); // 120-day window

    Promise.all(CALENDARS.map(function (calId) {
      var url = 'https://www.googleapis.com/calendar/v3/calendars/' + encodeURIComponent(calId) +
        '/events?key=' + API_KEY + '&timeMin=' + now + '&timeMax=' + future +
        '&singleEvents=true&orderBy=startTime&maxResults=100';
      return fetch(url).then(function (r) { return r.ok ? r.json() : { items: [] }; })
        .catch(function () { return { items: [] }; });
    })).then(function (results) {
      var allEvents = results.flatMap(function (r) { return r.items || []; });

      badges.forEach(function (el) {
        var keyword = el.getAttribute('data-next-event').toLowerCase();
        var match = allEvents
          .filter(function (ev) { return (ev.summary || '').toLowerCase().includes(keyword); })
          .sort(function (a, b) {
            var da = new Date(a.start.dateTime || a.start.date);
            var db = new Date(b.start.dateTime || b.start.date);
            return da - db;
          })[0];

        if (match) {
          var d = new Date(match.start.dateTime || match.start.date);
          var formatted = d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
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
