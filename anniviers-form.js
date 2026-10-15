/* Val d'Anniviers guest-card discount sign-up.
   ENDPOINT = eigenes Apps Script (eigenes Sheet «Anniviers»). Solange leer: Absenden öffnet WhatsApp mit allen Angaben. */
(function () {
  var ENDPOINT = 'https://script.google.com/macros/s/AKfycbxM5AiA2PHESx3liCIpsYV8AJOriaMsnnE1TFnmCBW7LVgX7hUicCFAh0qZvHoTBn2hNA/exec';
  var WA = '41762914369';
  var f = document.getElementById('anniviers-form');
  if (!f) return;
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var msg = {
    en: { sending: 'Sending…', fail: 'Something went wrong — please try again or write to us on WhatsApp.', wa: 'Val d’Anniviers guest card – 15% discount' },
    fr: { sending: 'Envoi…', fail: 'Oups, ça n’a pas marché — réessaie ou écris-nous sur WhatsApp.', wa: 'Carte d’hôte Val d’Anniviers – réduction 15%' },
    de: { sending: 'Wird gesendet…', fail: 'Das hat nicht geklappt — bitte nochmals versuchen oder schreib uns auf WhatsApp.', wa: 'Gästekarte Val d’Anniviers – 15% Rabatt' }
  }[lang] || {};
  var qs = new URLSearchParams(location.search), src = qs.get('src') || qs.get('utm_source') || '';
  try { if (src) sessionStorage.setItem('ra_src', src); else src = sessionStorage.getItem('ra_src') || ''; } catch (e) {}
  f.elements.source.value = src || (document.referrer ? 'web:' + new URL(document.referrer).hostname : 'direct');
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!f.reportValidity()) return;
    if (f.elements.website.value) return; // Spam-Falle
    var data = new URLSearchParams(new FormData(f));
    data.set('lang', lang);
    data.set('program', 'anniviers');
    var btn = f.querySelector('button[type=submit]'), label = btn.textContent;
    var done = function () {
      f.hidden = true;
      document.getElementById('anniviers-form-ok').hidden = false;
      if (window.gtag) gtag('event', 'generate_lead', { form: 'anniviers_guest_card', lead_source: data.get('source') });
    };
    if (!ENDPOINT) {
      var t = [msg.wa, data.get('first_name') + ' ' + data.get('last_name'), data.get('email'), data.get('phone'), 'Carte: ' + data.get('card_number'), data.get('location')].join('\n');
      window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(t), '_blank');
      done();
      return;
    }
    btn.disabled = true; btn.textContent = msg.sending;
    fetch(ENDPOINT, { method: 'POST', mode: 'no-cors', body: data })
      .then(done)
      .catch(function () { btn.disabled = false; btn.textContent = label; alert(msg.fail); });
  });
})();
