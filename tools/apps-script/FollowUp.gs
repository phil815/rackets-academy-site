/**
 * FollowUp.gs — Mail an NOTIFY_EMAIL, wenn eine Zahlung NICHT zustande kam (FAILED / EXPIRED),
 * damit Phil die Person persönlich nachfassen kann (Mail- und WhatsApp-Link mit fertigem Text).
 *
 * - Hängt sich an checkPendingOrders (5-Min-Trigger) – keine Änderung an Code.gs/Events.gs/Camps.gs.
 * - Wartet 2 Std. ab Bestellversuch (so lange kann die Person es noch erneut versuchen).
 * - Keine Mail, wenn dieselbe E-Mail-Adresse danach doch bezahlt hat (z.B. 3 Versuche, 4. klappt).
 * - Mehrere Fehlversuche derselben Person = EINE Mail.
 * - Interne Tests (@racketsacademy.ch, p.junggutierrez@…) und Google-Shopping-Bots werden ignoriert.
 * - Markiert erledigte Zeilen in Spalte M («FollowUp»), damit nie doppelt gemailt wird.
 * - Nur Bestellungen ab Installation (ältere Fehlversuche lösen keine Mail aus).
 *
 * WICHTIG: Diese Datei muss UNTER Code.gs stehen (neue Dateien landen automatisch unten). Nur speichern –
 * kein neues Deployment nötig, der Zeit-Trigger nutzt immer den gespeicherten Code.
 */
var FU_WAIT_HOURS_ = 2;
var FU_COL_ = 13; // Spalte M
var FU_SKIP_ = /@racketsacademy\.ch$|^p\.junggutierrez@|storebotmail|@example\./i;

var FU_BASE_CHECK_ = typeof checkPendingOrders === 'function' ? checkPendingOrders : null;
if (FU_BASE_CHECK_) {
  checkPendingOrders = function () {
    FU_BASE_CHECK_();
    try { followUpUnpaid_(); } catch (err) { Logger.log('followUpUnpaid_ ERROR: ' + err.message); }
  };
}

function followUpUnpaid_() {
  var props = PropertiesService.getScriptProperties();
  var since = Number(props.getProperty('FU_SINCE') || 0);
  if (!since) { since = Date.now(); props.setProperty('FU_SINCE', String(since)); }

  var sheet = getSheet_('Orders');
  if (sheet.getRange(1, FU_COL_).getValue() === '') sheet.getRange(1, FU_COL_).setValue('FollowUp');
  var data = sheet.getDataRange().getValues();
  var now = Date.now();

  // bezahlte E-Mails mit Zeitpunkt (für «hat danach doch bezahlt?»)
  var paid = {};
  for (var i = 1; i < data.length; i++) {
    if (data[i][8] !== 'PAID') continue;
    var pe = String(data[i][5]).toLowerCase().trim();
    var pt = new Date(data[i][0]).getTime();
    if (!paid[pe] || pt > paid[pe]) paid[pe] = pt;
  }

  // offene Fehlversuche je E-Mail sammeln
  var groups = {};
  for (var r = 1; r < data.length; r++) {
    var row = data[r], st = row[8];
    if (st !== 'FAILED' && st !== 'EXPIRED') continue;
    if (row[FU_COL_ - 1]) continue;                    // schon erledigt
    var t = new Date(row[0]).getTime();
    if (!t || t < since) continue;                     // vor Installation
    var email = String(row[5]).toLowerCase().trim();
    if (!email || FU_SKIP_.test(email)) { sheet.getRange(r + 1, FU_COL_).setValue('–'); continue; }
    (groups[email] = groups[email] || []).push({ r: r + 1, t: t, row: row });
  }

  Object.keys(groups).forEach(function (email) {
    var g = groups[email];
    var last = g[g.length - 1];
    if (now - last.t < FU_WAIT_HOURS_ * 3600000) return;          // Person kann es noch versuchen
    var stamp = Utilities.formatDate(new Date(), 'Europe/Zurich', 'dd.MM. HH:mm');
    if (paid[email] && paid[email] >= g[0].t) {                   // hat doch bezahlt
      g.forEach(function (x) { sheet.getRange(x.r, FU_COL_).setValue('bezahlt später – keine Mail'); });
      return;
    }
    sendFollowUpMail_(email, g);
    g.forEach(function (x) { sheet.getRange(x.r, FU_COL_).setValue('Follow-up-Mail ' + stamp); });
  });
}

function sendFollowUpMail_(email, g) {
  var notify = getProp_('NOTIFY_EMAIL') || 'phil@racketsacademy.ch';
  var last = g[g.length - 1].row;
  var type = last[3], name = String(last[4] || '').trim(), amount = last[7];
  var d = {}; try { d = JSON.parse(last[6]); } catch (e) {}
  var lang = String(d.lang || 'fr').slice(0, 2);
  var anyFailed = g.some(function (x) { return x.row[8] === 'FAILED'; });
  var what = fuLabel_(type, d);
  var first = name.split(/\s+/)[0] || '';

  var reason = anyFailed
    ? 'Zahlung von SumUp abgelehnt (FAILED) – meist Karte/3D-Secure abgelehnt oder Limit.'
    : 'Zahlung nicht abgeschlossen (EXPIRED) – Bezahlseite geöffnet, aber nicht bezahlt bzw. abgebrochen.';

  var msg = {
    fr: 'Bonjour ' + first + ', ici Phil de la Rackets Academy 👋 J’ai vu que ta commande « ' + what + ' » n’a pas pu être finalisée (paiement non abouti). Je peux t’aider ? Je peux aussi t’envoyer un lien de paiement TWINT ou une facture.',
    de: 'Hallo ' + first + ', hier ist Phil von der Rackets Academy 👋 Ich habe gesehen, dass deine Bestellung «' + what + '» nicht abgeschlossen wurde (Zahlung nicht durchgegangen). Kann ich dir helfen? Gerne schicke ich dir auch einen TWINT-Link oder eine Rechnung.',
    en: 'Hi ' + first + ', Phil from Rackets Academy here 👋 I saw your order "' + what + '" didn’t go through (payment not completed). Can I help? I can also send you a TWINT payment link or an invoice.'
  }[lang] || '';

  var phone = String(d.phone || '').replace(/[^\d+]/g, '');
  if (/^0\d{9}$/.test(phone)) phone = '41' + phone.slice(1);
  phone = phone.replace(/^\+/, '').replace(/^00/, '');
  var wa = phone ? 'https://wa.me/' + phone + '?text=' + encodeURIComponent(msg) : '';
  var subj = { fr: 'Ta commande Rackets Academy', de: 'Deine Bestellung bei der Rackets Academy', en: 'Your Rackets Academy order' }[lang] || 'Rackets Academy';
  var mailto = 'mailto:' + email + '?subject=' + encodeURIComponent(subj) + '&body=' + encodeURIComponent(msg);

  var details = [];
  if (d.participants) details.push('Teilnehmende: ' + d.participants);
  if (d.qty) details.push('Anzahl: ' + d.qty);
  if (d.pickupLocation || d.location) details.push('Standort: ' + (d.pickupLocation || d.location));
  if (d.notes) details.push('Notiz: ' + d.notes);
  if (d.giftMessage) details.push('Geschenktext: ' + d.giftMessage);

  var when = g.map(function (x) {
    return Utilities.formatDate(new Date(x.t), 'Europe/Zurich', 'dd.MM. HH:mm') + ' (' + x.row[8] + ')';
  }).join(', ');

  var esc = function (s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); };
  var html =
    '<p><b>' + esc(name || email) + '</b> wollte <b>' + esc(what) + '</b> für <b>' + esc(amount) + ' CHF</b> kaufen – die Zahlung kam nicht zustande.</p>' +
    '<p>' + esc(reason) + '<br>Versuche: ' + g.length + ' · ' + esc(when) + '</p>' +
    '<p>E-Mail: ' + esc(email) + (d.phone ? '<br>Telefon: ' + esc(d.phone) : '') +
    '<br>Sprache: ' + lang.toUpperCase() + (details.length ? '<br>' + details.map(esc).join('<br>') : '') + '</p>' +
    '<p>' + (wa ? '<a href="' + wa + '" style="display:inline-block;background:#25D366;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:600">WhatsApp mit Text öffnen</a> &nbsp; ' : '') +
    '<a href="' + mailto + '" style="display:inline-block;background:#0b2545;color:#fff;padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:600">Mail mit Text öffnen</a></p>' +
    '<p style="color:#666">Vorgeschlagener Text (' + lang.toUpperCase() + '):<br><i>' + esc(msg) + '</i></p>' +
    '<p style="color:#666;font-size:12px">Shop-Sheet, Tab Orders, Spalte M = «Follow-up-Mail». Bezahlt die Person später doch, kommt die normale Bestellmail.</p>';

  MailApp.sendEmail(notify, '💬 Follow-up: ' + (name || email) + ' – ' + what + ' ' + amount + ' CHF nicht bezahlt', '',
    { htmlBody: html, name: 'Rackets Academy Shop', replyTo: email });
}

function fuLabel_(type, d) {
  if (type === 'racket') return d.racketLabel || 'Schläger';
  if (type === 'ticket') return /padel-dine/.test(d.eventId || '') ? 'Padel +Dine' + (d.ticket === 'dinner' ? ' (Dinner)' : ' (Turnier + Dinner)') : (d.eventId || 'Event-Ticket');
  if (type === 'camp') return 'Ski & Padel ' + String(d.campId || '').replace('ski-padel-', '');
  if (type === 'voucher') return 'Gutschein';
  if (type === 'lesson') return 'Trainerstunden-Gutschein';
  return type || 'Bestellung';
}

// Test im Editor: zeigt, was gemailt würde (ohne zu senden, ohne Spalte M zu ändern).
function testFollowUp() {
  var data = getSheet_('Orders').getDataRange().getValues();
  for (var i = data.length - 1; i > 0; i--) {
    if (data[i][8] === 'FAILED' || data[i][8] === 'EXPIRED') {
      var d = {}; try { d = JSON.parse(data[i][6]); } catch (e) {}
      Logger.log('Letzter Fehlversuch: ' + data[i][4] + ' · ' + fuLabel_(data[i][3], d) + ' · ' + data[i][7] + ' CHF · ' + data[i][8]);
      break;
    }
  }
  Logger.log(checkPendingOrders === FU_BASE_CHECK_ ? 'NICHT aktiv – FollowUp.gs muss unter Code.gs stehen' : 'Follow-up-Hook aktiv ✔');
}
