/**
 * Return.gs — Rückkehr von der SumUp-Bezahlseite (hosted checkout) auf die Website.
 *
 * Setzt bei JEDEM SumUp-Checkout redirect_url = <Produktseite>?paid=<ref>&amount=<CHF>,
 * damit nav.js den Kauf als Meta-Purchase (eventID = ref) und GA4-purchase zählt.
 * Gibt in der JSON-Antwort zusätzlich `ref` zurück (nav.js nutzt ihn als eventID im Widget,
 * so zählen Widget-Kauf und spätere Rückkehr nur einmal).
 *
 * SumUp leitet nur nach ERFOLGREICHER Zahlung weiter (Button «zurück zur Website» auf der
 * Erfolgsseite), bei Abbruch/Fehler nicht. Deshalb kein Zwischenschritt nötig.
 *
 * KEINE Änderung an Code.gs / Camps.gs / Events.gs / Fulfilment.
 * WICHTIG: Diese Datei muss UNTER Code.gs, Camps.gs und Events.gs stehen (neue Dateien landen
 * automatisch unten). Danach: Bereitstellen → Bereitstellungen verwalten → Bearbeiten → Neue Version.
 */
var RT_SITE_ = 'https://www.racketsacademy.ch/';
// Event-ID (Events.gs) -> Seite auf der Website
var RT_EVENT_PAGES_ = { 'padel-dine-2026-11-07': 'padel-dine.html' };
// Seiten, die es auch unter /fr/ und /de/ gibt ('' = Startseite)
var RT_LANG_PAGES_ = { '': 1, 'shop.html': 1, 'ski-and-padel.html': 1, 'padel-dine.html': 1, 'events.html': 1 };
var RT_CTX_ = null;

function rtReturnUrl_(p) {
  var page = '';
  if (p.formType === 'camp') page = 'ski-and-padel.html';
  else if (p.formType === 'ticket') page = RT_EVENT_PAGES_[p.eventId] || 'events.html';
  else if (p.formType === 'voucher' || p.formType === 'lesson' || p.formType === 'racket') page = 'shop.html';
  var l = String(p.lang || '').slice(0, 2).toLowerCase();
  var pre = ((l === 'fr' || l === 'de') && RT_LANG_PAGES_[page]) ? l + '/' : '';
  return RT_SITE_ + pre + page;
}

// Gleiche Anfrage wie in Code.gs, plus redirect_url (nur wenn ein Website-Checkout läuft).
createSumUpCheckout_ = function (checkoutRef, amount, description) {
  var payload = {
    checkout_reference: checkoutRef, amount: amount, currency: 'CHF', description: description,
    merchant_code: getProp_('MERCHANT_CODE'), hosted_checkout: { enabled: true }
  };
  if (RT_CTX_ && RT_CTX_.url) {
    payload.redirect_url = RT_CTX_.url + '?paid=' + encodeURIComponent(checkoutRef) + '&amount=' + encodeURIComponent(amount);
    RT_CTX_.ref = checkoutRef;
  }
  var res = UrlFetchApp.fetch('https://api.sumup.com/v0.1/checkouts', {
    method: 'post', contentType: 'application/json',
    headers: { Authorization: 'Bearer ' + getProp_('SUMUP_API_KEY') },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });
  Logger.log('SumUp create: HTTP ' + res.getResponseCode() + ' ' + res.getContentText());
  if (res.getResponseCode() >= 300) throw new Error('SumUp: ' + res.getContentText());
  return JSON.parse(res.getContentText());
};

var RT_BASE_DOPOST_ = typeof doPost === 'function' ? doPost : null;
if (RT_BASE_DOPOST_) {
  doPost = function (e) {
    var p = (e && e.parameter) || {};
    RT_CTX_ = { url: rtReturnUrl_(p), ref: null };
    try {
      var out = RT_BASE_DOPOST_(e);
      if (RT_CTX_.ref && p.mode === 'json') {
        try {
          var o = JSON.parse(out.getContent());
          if (o && o.ok) { o.ref = RT_CTX_.ref; return json_(o); }
        } catch (x) {}
      }
      return out;
    } finally {
      RT_CTX_ = null;
    }
  };
}

// Test im Editor: zeigt, wohin SumUp zurückleitet (kein Checkout, keine Zahlung).
function testReturnUrls() {
  [{ formType: 'camp', lang: 'fr' }, { formType: 'ticket', eventId: 'padel-dine-2026-11-07', lang: 'de' },
   { formType: 'racket', lang: 'en' }, { formType: 'voucher', lang: 'fr' }, { formType: 'x' }]
    .forEach(function (p) { Logger.log(JSON.stringify(p) + ' -> ' + rtReturnUrl_(p) + '?paid=<ref>&amount=<CHF>'); });
  Logger.log(doPost === RT_BASE_DOPOST_ ? 'NICHT aktiv – Return.gs muss ganz unten stehen' : 'Return-Hook aktiv ✔');
}
