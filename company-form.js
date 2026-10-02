/* Company discount sign-up → Apps Script web app (sheet + email to Phil + confirmation to applicant).
   Until ENDPOINT is set, submitting opens WhatsApp prefilled with the form data. */
(function () {
  var ENDPOINT = 'https://script.google.com/macros/s/AKfycbzfVMFLKr8rg6Dmcz4JnA009tllWbZBAot5kcqf_gUVP0wu2tS4eDk6BTr_9Ut93uiXQw/exec';
  var WA = '41762914369';
  var f = document.getElementById('company-form');
  if (!f) return;
  var lang = (document.documentElement.lang || 'en').slice(0, 2);
  var msg = {
    en: { sending: 'Sending…', fail: 'Something went wrong — please try again or write to us on WhatsApp.' },
    fr: { sending: 'Envoi…', fail: 'Oups, ça n’a pas marché — réessaie ou écris-nous sur WhatsApp.' },
    de: { sending: 'Wird gesendet…', fail: 'Das hat nicht geklappt — bitte nochmals versuchen oder schreib uns auf WhatsApp.' }
  }[lang] || {};
  // Quelle merken (z.B. ?src=foire-du-valais vom QR-Code am Stand)
  var qs = new URLSearchParams(location.search), src = qs.get('src') || qs.get('utm_source') || '';
  try { if (src) sessionStorage.setItem('ra_src', src); else src = sessionStorage.getItem('ra_src') || ''; } catch (e) {}
  f.elements.source.value = src || (document.referrer ? 'web:' + new URL(document.referrer).hostname : 'direct');
  var sel = f.elements.company, others = f.querySelectorAll('.co-other');
  sel.addEventListener('change', function () {
    var o = sel.value === '__other';
    others.forEach(function (el) { el.hidden = !o; });
    f.elements.company_other.required = o;
  });
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    if (!f.reportValidity()) return;
    var data = new URLSearchParams(new FormData(f));
    data.set('lang', lang);
    var btn = f.querySelector('button[type=submit]'), label = btn.textContent;
    if (!ENDPOINT) {
      var t = ['Company discount', data.get('company') === '__other' ? data.get('company_other') : data.get('company'), data.get('first_name') + ' ' + data.get('last_name'), data.get('email'), data.get('phone'), data.get('location')].filter(Boolean).join('\n');
      window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(t), '_blank');
      return;
    }
    btn.disabled = true; btn.textContent = msg.sending;
    fetch(ENDPOINT, { method: 'POST', mode: 'no-cors', body: data })
      .then(function () {
        f.hidden = true;
        document.getElementById('company-form-ok').hidden = false;
        if (window.gtag) gtag('event', 'generate_lead', { form: 'company_discount', company: data.get('company') === '__other' ? 'new:' + data.get('company_other') : data.get('company'), lead_source: data.get('source'), new_company: data.get('company') === '__other' });
      })
      .catch(function () { btn.disabled = false; btn.textContent = label; alert(msg.fail); });
  });
})();
