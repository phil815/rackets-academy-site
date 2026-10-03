/**
 * EVENT TICKETS – Events.gs (Datei im Shop-Apps-Script, UNTER Code.gs und Camps.gs)
 * =============================================================================
 * Website (padel-dine.html) -> SumUp-Pop-up -> Zahlung -> Bestätigungsmail
 * + KLARA-Rechnungsentwurf + Info an NOTIFY_EMAIL. Plätze werden live aus dem
 * Orders-Sheet gezählt (PAID + PENDING der letzten 2 h), getrennt pro Ticketart.
 *
 * Padel+Dine feat. Instinct Amazonia, Sa 7.11.2026:
 *   team   = Turnier + Dinner Party, 2er-Team, 2 × 79 CHF, 48 Plätze (24 Teams)
 *   dinner = Dinner Party, 59 CHF pro Person, 1–10 Tickets, 52 Plätze
 *   Verkauf ab Mo 5.10.2026 00:00, Rückerstattung bis So 1.11.2026.
 *
 * Script Properties:
 *   KLARA_DINE_ARTICLE = Artikelnummer in KLARA (fehlt sie, wird die Buchung
 *                        trotzdem angenommen; Notiz im Sheet: Rechnung manuell)
 * Weitere Events: einfach einen Eintrag in EVENTS_ ergänzen.
 *
 * KEINE Änderung an Code.gs/Camps.gs nötig: diese Datei hängt sich selbst ein.
 * Prüfen: testEventSetup ausführen.
 */

var EVENTS_ = {
  'padel-dine-2026-11-07': {
    start: '2026-11-07T10:00:00+01:00', salesOpen: '2026-10-03T00:00:00+02:00', articleProp: 'KLARA_DINE_ARTICLE',
    name: { de: 'Padel+Dine feat. Instinct Amazonia', fr: 'Padel+Dine feat. Instinct Amazonia', en: 'Padel+Dine feat. Instinct Amazonia' },
    date: { de: 'Samstag, 7. November 2026, 10 – 2 Uhr', fr: 'samedi 7 novembre 2026, de 10h à 2h', en: 'Saturday 7 November 2026, 10am – 2am' },
    refund: { de: 'Sonntag, 1. November 2026', fr: 'dimanche 1er novembre 2026', en: 'Sunday 1 November 2026' },
    tickets: {
      team:   { cap: 48, pp: 79, fixed: 2, name: { de: 'Turnier + Dinner Party (2er-Team)', fr: 'Tournoi + Dinner Party (équipe de 2)', en: 'Tournament + Dinner Party (team of 2)' },
                incl: { de: 'Turnier (Qualifikation + Haupttableau), Bälle, Signature-Buffet von Instinct Amazonia, 1 Getränk, DJ-Party bis 2 Uhr. Schläger können vor Ort gemietet werden.',
                        fr: 'Tournoi (qualifications + tableau final), balles, buffet signature Instinct Amazonia, 1 boisson, soirée DJ jusqu’à 2h. Raquettes à louer sur place.',
                        en: 'Tournament (qualifying round + main draw), balls, Instinct Amazonia signature buffet, 1 drink, DJ party until 2am. Rental rackets on site.' } },
      dinner: { cap: 52, pp: 59, max: 10, name: { de: 'Dinner Party', fr: 'Dinner Party', en: 'Dinner Party' },
                incl: { de: 'Signature-Buffet von Instinct Amazonia, 1 Getränk, DJ-Party bis 2 Uhr.',
                        fr: 'Buffet signature Instinct Amazonia, 1 boisson, soirée DJ jusqu’à 2h.',
                        en: 'Instinct Amazonia signature buffet, 1 drink, DJ party until 2am.' } }
    }
  }
};

var EV_T_ = {
  de: { subject: 'Deine Tickets für {e} 🎾🍣', hi: 'Hola', thanks: 'Danke für deine Buchung! Wir freuen uns auf dich.', booked: 'Gebucht', when: 'Wann', where: 'Wo', incl: 'Inklusive', paid: 'Bezahlt', people: 'Teilnehmende',
        refund: 'Rückerstattung möglich bis {d}: einfach auf diese Mail antworten oder uns auf WhatsApp schreiben.', fwd: 'Bitte leite diese Mail an alle Personen deiner Buchung weiter.',
        questions: 'Fragen? WhatsApp: +41 77 278 01 15.', bye: 'Bis bald auf dem Court!', team: 'Dein Rackets Academy Team', order: 'Buchung',
        soldOut: 'Diese Tickets sind ausverkauft.', onlyLeft: function (n) { return 'Nur noch ' + n + ' Platz/Plätze frei.'; }, notOpen: 'Der Ticketverkauf startet am Montag, 5. Oktober.', past: 'Der Ticketverkauf ist geschlossen.' },
  fr: { subject: 'Tes billets pour {e} 🎾🍣', hi: 'Hola', thanks: 'Merci pour ta réservation ! On se réjouit de te voir.', booked: 'Réservé', when: 'Quand', where: 'Où', incl: 'Inclus', paid: 'Payé', people: 'Participant·es',
        refund: 'Remboursement possible jusqu’au {d} : réponds simplement à cet e-mail ou écris-nous sur WhatsApp.', fwd: 'Merci de transférer cet e-mail à toutes les personnes de ta réservation.',
        questions: 'Des questions ? WhatsApp : +41 77 278 01 15.', bye: 'À bientôt sur le terrain !', team: 'Ton équipe Rackets Academy', order: 'Réservation',
        soldOut: 'Ces billets sont complets.', onlyLeft: function (n) { return 'Plus que ' + n + ' place(s) disponible(s).'; }, notOpen: 'La billetterie ouvre le lundi 5 octobre.', past: 'La billetterie est fermée.' },
  en: { subject: 'Your tickets for {e} 🎾🍣', hi: 'Hola', thanks: 'Thanks for your booking! We can\'t wait to see you.', booked: 'Booked', when: 'When', where: 'Where', incl: 'Included', paid: 'Paid', people: 'Participants',
        refund: 'Refunds possible until {d}: just reply to this email or message us on WhatsApp.', fwd: 'Please forward this email to everyone in your booking.',
        questions: 'Questions? WhatsApp: +41 77 278 01 15.', bye: 'See you on court!', team: 'Your Rackets Academy team', order: 'Booking',
        soldOut: 'These tickets are sold out.', onlyLeft: function (n) { return 'Only ' + n + ' place(s) left.'; }, notOpen: 'Ticket sales open on Monday 5 October.', past: 'Ticket sales are closed.' }
};

// ---------- availability (GET ...exec?action=tickets&event=…) ----------
function ticketAvailability_(eventId) {
  var ev = EVENTS_[eventId];
  if (!ev) return { ok: false, error: 'unknown event' };
  var data = getSheet_('Orders').getDataRange().getValues(), taken = {}, now = Date.now();
  for (var i = 1; i < data.length; i++) {
    if (data[i][3] !== 'ticket') continue;
    var st = data[i][8];
    var live = st === 'PAID' || (st === 'PENDING' && now - new Date(data[i][0]).getTime() < 2 * 3600000);
    if (!live) continue;
    try { var d = JSON.parse(data[i][6]); if (d.eventId === eventId) taken[d.ticket] = (taken[d.ticket] || 0) + (Number(d.qty) || 1); } catch (e) {}
  }
  var out = {};
  Object.keys(ev.tickets).forEach(function (k) { out[k] = Math.max(0, ev.tickets[k].cap - (taken[k] || 0)); });
  return { ok: true, tickets: out };
}

// ---------- order (called from doPost) ----------
function ticketOrder_(p, lang) {
  var t = EV_T_[lang] || EV_T_.en, ev = EVENTS_[p.eventId], tk = ev && ev.tickets[p.ticket];
  if (!ev || !tk) return { error: 'Unknown event or ticket.' };
  var now = Date.now();
  if (now < new Date(ev.salesOpen).getTime()) return { error: t.notOpen };
  if (now > new Date(ev.start).getTime()) return { error: t.past };
  var qty = tk.fixed || Math.max(1, Math.min(tk.max || 10, parseInt(p.qty, 10) || 1));
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    var left = ticketAvailability_(p.eventId).tickets[p.ticket];
    if (left < qty) return { error: left > 0 ? t.onlyLeft(left) : t.soldOut };
  } finally { lock.releaseLock(); }
  var amount = qty * tk.pp;
  return {
    amount: amount,
    description: 'Rackets Academy ' + ev.name.en + ' - ' + tk.name.en + ' - ' + qty + 'x ' + tk.pp + ' CHF',
    detail: JSON.stringify({ eventId: p.eventId, ticket: p.ticket, qty: qty, pricePP: tk.pp, phone: p.phone || '',
      participants: String(p.participants || '').slice(0, 600), notes: p.notes || '', lang: lang })
  };
}

// ---------- fulfilment (called from fulfillOrder_ once SumUp says PAID) ----------
function fulfillTicket_(sheet, rowIndex, row) {
  var buyerName = row[4], buyerEmail = row[5], detail = JSON.parse(row[6]), ref = row[1], amount = Number(row[7]);
  var lang = lang_(detail.lang), notes = [];
  if (!row[10]) {
    try {
      var invId = createTicketInvoice_(detail, buyerName, buyerEmail, amount, ref);
      if (invId) sheet.getRange(rowIndex, 11).setValue(invId);
      else notes.push('KLARA: Property ' + EVENTS_[detail.eventId].articleProp + ' fehlt - Rechnung manuell erstellen');
    } catch (err) { Logger.log('KLARA ticket ERROR: ' + err.message); notes.push('KLARA: ' + err.message); }
  }
  try {
    sendTicketEmail_(lang, buyerName, buyerEmail, detail, ref, amount);
    notes.push('Mail gesendet ' + Utilities.formatDate(new Date(), 'Europe/Zurich', 'dd.MM. HH:mm'));
  } catch (err) { notes.push('FEHLER Mail: ' + err.message); }
  sheet.getRange(rowIndex, 12).setValue(notes.join(' | '));
  try { notifyTeam_('ticket', buyerName, buyerEmail, detail, amount, notes.filter(function (n) { return n.indexOf('Mail gesendet') !== 0; })); }
  catch (err) { Logger.log('notifyTeam_ ticket ERROR: ' + err.message); }
}

function createTicketInvoice_(detail, buyerName, buyerEmail, amount, ref) {
  var ev = EVENTS_[detail.eventId], tk = ev.tickets[detail.ticket];
  var article = getProp_(ev.articleProp);
  if (!article) return null;
  var customerId = klaraCustomerId_(), today = klaraDate_(new Date());
  var item = {
    position: 1, itemNumer: article,
    description: ev.name.de + ' 7.11.2026 – ' + tk.name.de +
      (detail.participants ? ' (' + String(detail.participants).replace(/\s+/g, ' ').slice(0, 200) + ')' : ''),
    quantity: Number(detail.qty), unit: 'Ticket', price: Number(detail.pricePP), discount: 0, amount: amount,
    vat: VAT_NORMAL_, vatCase: 'TAXABLE_SUPPLY'
  };
  var body = {
    invoiceCode: 'WEB-' + shortRef_(ref), status: 'DRAFT',
    documentDate: today, paymentDate: today, issuedDate: today, amount: amount, usingVAT: true,
    subject: 'Online-Shop ' + ev.name.de + ' – ' + buyerName,
    ourReference: 'Online-Shop', yourReference: buyerName + ' <' + buyerEmail + '>',
    companyCityAndDate: 'Salgesch', postMethod: 'PRINT_AND_MANUAL_SEND',
    ibanNumberCHF: KLARA_IBAN_, qrInvoice: false,
    closeAndSignature: 'Bereits bezahlt via SumUp (Online-Shop).\nReferenz: ' + ref + '\n\nThe Rackets Academy AG',
    order: { orderNumber: klaraOrderNumber_(), orderName: 'Online-Shop', customer: { id: customerId } },
    documentAddress: { customerId: customerId },
    orderItems: [item]
  };
  var created = JSON.parse(klara_('post', '/core/v1/invoices', body).getContentText());
  Logger.log('KLARA ticket draft created id=' + created.id);
  return created.id;
}

function sendTicketEmail_(lang, name, email, detail, ref, amount) {
  var t = EV_T_[lang] || EV_T_.en, ev = EVENTS_[detail.eventId], tk = ev.tickets[detail.ticket];
  var evName = ev.name[lang] || ev.name.en;
  var people = detail.participants ? String(detail.participants).split(/;\s*/).map(esc_).join('<br>') : '';
  var html = '<p>' + t.hi + ' ' + esc_(name) + '!</p><p>' + t.thanks + '</p>' +
    '<p style="background:#f7f2e7;border-radius:10px;padding:14px 16px;"><b>' + t.booked + ':</b> ' + esc_(evName) + ' · ' + esc_(tk.name[lang] || tk.name.en) +
    ' · ' + detail.qty + ' × ' + tk.pp + ' CHF · ' + t.paid + ': ' + amount + ' CHF<br>' +
    '<b>' + t.when + ':</b> ' + (ev.date[lang] || ev.date.en) + '<br>' +
    '<b>' + t.where + ':</b> Rackets Academy, Littenstrasse 30, 3970 Salgesch' +
    (people ? '<br><br><b>' + t.people + ':</b><br>' + people : '') + '</p>' +
    '<p><b>' + t.incl + ':</b> ' + (tk.incl[lang] || tk.incl.en) + '</p>' +
    '<p>' + t.refund.replace('{d}', ev.refund[lang] || ev.refund.en) + '</p>' +
    (detail.qty > 1 ? '<p>' + t.fwd + '</p>' : '') +
    '<p>' + t.questions + '</p>' +
    '<p>' + t.bye + '<br>' + t.team + '<br><span style="color:#667;">Littenstrasse 30, 3970 Salgesch</span></p>' +
    '<p style="color:#99a;font-size:12px;">' + t.order + ' ' + shortRef_(ref) + '</p>';
  MailApp.sendEmail(email, t.subject.replace('{e}', evName) + ' (' + t.order + ' ' + shortRef_(ref) + ')', '',
    { htmlBody: mailShell_(html), name: 'Rackets Academy', replyTo: getProp_('NOTIFY_EMAIL') || 'phil@racketsacademy.ch' });
}

// ---------- Hooks (chain onto whatever Code.gs/Camps.gs defined) ----------
var EV_BASE_DOGET_ = typeof doGet === 'function' ? doGet : null;
var EV_BASE_DOPOST_ = typeof doPost === 'function' ? doPost : null;
var EV_BASE_FULFILL_ = typeof fulfillOrder_ === 'function' ? fulfillOrder_ : null;

if (EV_BASE_DOGET_ && EV_BASE_DOPOST_ && EV_BASE_FULFILL_) {
  doGet = function (e) {
    if (e && e.parameter && e.parameter.action === 'tickets') return json_(ticketAvailability_(e.parameter.event));
    return EV_BASE_DOGET_(e);
  };

  doPost = function (e) {
    if (!(e && e.parameter && e.parameter.formType === 'ticket')) return EV_BASE_DOPOST_(e);
    JSON_MODE_ = e.parameter.mode === 'json';
    Logger.log('doPost TICKET (json=' + JSON_MODE_ + '). Params: ' + JSON.stringify(e.parameter));
    try {
      var p = e.parameter, lang = lang_(p.lang), ref = Utilities.getUuid();
      var co = ticketOrder_(p, lang);
      if (co.error) return htmlError_(co.error);
      var checkout = createSumUpCheckout_(ref, co.amount, co.description);
      getSheet_('Orders').appendRow([new Date(), ref, checkout.id, 'ticket', p.buyerName, p.buyerEmail,
        co.detail, co.amount, 'PENDING', '', '', '']);
      if (JSON_MODE_) return json_({ ok: true, id: checkout.id, url: checkout.hosted_checkout_url, amount: co.amount, description: co.description });
      return HtmlService.createHtmlOutput(
        '<p style="font-family:sans-serif;font-size:18px;padding:40px;text-align:center;">' +
        '<a href="' + checkout.hosted_checkout_url + '" target="_top" style="display:inline-block;background:#6ffd1d;color:#045bab;padding:14px 28px;border-radius:999px;text-decoration:none;font-weight:bold;">Continue to payment</a></p>');
    } catch (err) {
      Logger.log('doPost TICKET ERROR: ' + err.message + ' | ' + err.stack);
      return htmlError_('Error: ' + err.message);
    }
  };

  fulfillOrder_ = function (sheet, rowIndex, row) {
    if (row[3] === 'ticket') return fulfillTicket_(sheet, rowIndex, row);
    return EV_BASE_FULFILL_(sheet, rowIndex, row);
  };
}

// Test from the editor: hooks active? free places per ticket type?
function testEventSetup() {
  Logger.log(doPost === EV_BASE_DOPOST_ || !EV_BASE_DOPOST_ ? 'NICHT aktiv - Events.gs muss unter Code.gs und Camps.gs stehen' : 'Hooks aktiv ✔');
  Logger.log('KLARA_DINE_ARTICLE: ' + (getProp_('KLARA_DINE_ARTICLE') || 'fehlt noch'));
  Logger.log(JSON.stringify(ticketAvailability_('padel-dine-2026-11-07')));
}
