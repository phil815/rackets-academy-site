// Startseite v2 und Seite «Platz buchen»: Buchungsblock. Die Logik (Playtomic-Link aus Standort, Sport und Tag,
// freie Padel-Plätze) liegt in nav.js (raBookCard), damit das Buchungsfenster auf allen Seiten dieselbe benutzt.
// Ohne JavaScript führt der Knopf zur Clubseite Salgesch.
(function () {
  var card = document.querySelector('[data-hv2-book]');
  if (card && window.raBookCard) window.raBookCard(card);
})();
