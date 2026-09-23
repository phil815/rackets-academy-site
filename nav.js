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
