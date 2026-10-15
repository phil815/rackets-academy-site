/**
 * Val d'Anniviers – Carte d'hôte (15% vor 17:30, 7 Tage, nur Salgesch, ohne Spa)
 * Projekt «Anniviers» (phil@racketsacademy.ch), als Web-App bereitgestellt (Ausführen als: ich, Zugriff: jeder).
 *
 * - doPost: Anmeldung von racketsacademy.ch/anniviers.html → Sheet «RA Anniviers – Carte d'hôte», Mail an Phil,
 *           Bestätigung an die Person (FR/DE/EN).
 * - Bei JEDER Anmeldung: Mail an Phil mit Playtomic-Import-CSV im Anhang (Kategorie «Val d'Anniviers», ohne Ablaufdatum).
 * - exportPending(): manuell alle noch nicht exportierten Zeilen als eine CSV mailen (Spalte J markiert Exportiertes).
 * - Einmalig: setup() ausführen.
 * - Playtomic: Kategorie muss exakt CATEGORY heissen und vorher in Playtomic Manager existieren.
 *   Import: Customers → Imports → Import new customers → CSV hochladen.
 */
var NOTIFY_ = 'phil@racketsacademy.ch';
var CATEGORY_ = "Val d'Anniviers";
var TZ_ = 'Europe/Zurich';
var HEAD_ = ['Zeitpunkt', 'Vorname', 'Nachname', 'E-Mail', 'Telefon', "Carte d'hôte Nr.", 'Standort', 'Sprache', 'Quelle', 'Playtomic-Import', 'In Playtomic ✔', 'Notiz'];

function setup() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('SHEET_ID');
  var ss = id ? SpreadsheetApp.openById(id) : SpreadsheetApp.create("RA Anniviers – Carte d'hôte");
  props.setProperty('SHEET_ID', ss.getId());
  var sh = ss.getSheets()[0];
  sh.setName('Anmeldungen');
  sh.getRange(1, 1, 1, HEAD_.length).setValues([HEAD_]).setFontWeight('bold').setBackground('#1e3a52').setFontColor('#ffffff');
  sh.setFrozenRows(1);
  sh.setColumnWidths(1, HEAD_.length, 140);
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  Logger.log('Sheet: ' + ss.getUrl());
}

function sheet_() {
  return SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID')).getSheetByName('Anmeldungen');
}

function doPost(e) {
  var p = (e && e.parameter) || {};
  if (p.website) return out_('ok'); // Spam-Falle
  if (!p.email || !p.first_name || !p.card_number) return out_('missing');
  var lock = LockService.getScriptLock(); lock.waitLock(20000);
  try {
    var sh = sheet_();
    var email = String(p.email).trim().toLowerCase();
    var card = String(p.card_number).trim();
    var data = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, HEAD_.length).getValues() : [];
    var dupe = data.some(function (r) { return String(r[3]).toLowerCase() === email; });
    var lang = String(p.lang || 'fr').slice(0, 2);
    var stamp = Utilities.formatDate(new Date(), TZ_, 'yyyy-MM-dd');
    sh.appendRow([new Date(), p.first_name, p.last_name || '', email, p.phone || '', card, p.location || 'Salgesch', lang.toUpperCase(), p.source || '', dupe ? 'Duplikat – kein Import' : 'CSV ' + stamp, false, '']);
    sh.getRange(sh.getLastRow(), 11).insertCheckboxes();
    notifyPhil_(p, email, card, dupe);
    if (!dupe) confirm_(p, email, lang);
  } finally { lock.releaseLock(); }
  return out_('ok');
}

function out_(s) { return ContentService.createTextOutput(s); }

function notifyPhil_(p, email, card, dupe) {
  var name = (p.first_name + ' ' + (p.last_name || '')).trim();
  MailApp.sendEmail(NOTIFY_, '🏔️ Anniviers: ' + name + (dupe ? ' (Duplikat)' : ''), '',
    { htmlBody: '<p><b>' + name + '</b> hat sich mit der Carte d\'hôte Val d\'Anniviers angemeldet.</p>' +
      '<p>E-Mail: ' + email + '<br>Telefon: ' + (p.phone || '–') + '<br>Carte d\'hôte Nr.: <b>' + card + '</b><br>Sprache: ' + String(p.lang || '').toUpperCase() + '<br>Quelle: ' + (p.source || '–') + '</p>' +
      (dupe ? '<p style="color:#b00">Diese E-Mail ist schon im Sheet – keine Import-Datei.</p>' : IMPORT_HOWTO_),
      attachments: dupe ? [] : [csvBlob_([[name, email, phone_(p.phone), '', '', CATEGORY_, '', '', '']], name)],
      name: 'Rackets Academy', replyTo: email });
}

function confirm_(p, email, lang) {
  var first = String(p.first_name).trim();
  var T = {
    fr: ['Ta réduction carte d\'hôte Val d\'Anniviers',
      'Bonjour ' + first + ',<br><br>Merci pour ton inscription ! On t\'ajoute au groupe « Val d\'Anniviers » dans Playtomic, en général sous 1 jour ouvrable. Ensuite tu as <b>-15% sur toutes tes réservations de court à Salgesch avant 17h30</b>, tous les jours, aussi le week-end (spa non inclus).<br><br>Important : réserve avec la même adresse e-mail ou le même numéro de téléphone que dans le formulaire, et garde ta carte d\'hôte sur toi.<br><br>À bientôt sur le court !<br>Phil & la team Rackets Academy<br>Littenstrasse 30, 3970 Salgesch'],
    de: ['Dein Gästekarten-Rabatt Val d\'Anniviers',
      'Hallo ' + first + ',<br><br>danke für deine Anmeldung! Wir nehmen dich in Playtomic in die Gruppe «Val d\'Anniviers» auf, meist innert 1 Arbeitstag. Danach hast du <b>15% Rabatt auf alle Court-Buchungen in Salgesch vor 17:30 Uhr</b>, jeden Tag, auch am Wochenende (ohne Spa).<br><br>Wichtig: Buch mit derselben E-Mail-Adresse oder Telefonnummer wie im Formular und nimm deine Gästekarte mit.<br><br>Bis bald auf dem Court!<br>Phil & das Rackets Academy Team<br>Littenstrasse 30, 3970 Salgesch'],
    en: ['Your Val d\'Anniviers guest card discount',
      'Hi ' + first + ',<br><br>thanks for signing up! We\'ll add you to the "Val d\'Anniviers" group in Playtomic, usually within 1 working day. From then on you get <b>15% off all court bookings in Salgesch before 5:30 pm</b>, every day, weekends included (spa not included).<br><br>Important: book with the same email or phone number you used in the form, and keep your guest card with you.<br><br>See you on court!<br>Phil & the Rackets Academy team<br>Littenstrasse 30, 3970 Salgesch']
  }[lang] || null;
  if (!T) return;
  MailApp.sendEmail(email, T[0], '', { htmlBody: T[1], name: 'Rackets Academy', replyTo: NOTIFY_ });
}

var IMPORT_HOWTO_ = '<p><b>Playtomic:</b> Customers → Imports → Import new customers → bestätigen → angehängte CSV hochladen → Next. ' +
  'Die Person landet direkt in der Gruppe «Val d\'Anniviers».</p>';

function csvBlob_(people, label) {
  var head = ['name', 'email', 'phone_number', 'gender', 'birthdate', 'category_name', 'category_expires', 'benefit_price_id', 'next_due_date'];
  var csv = [head].concat(people).map(function (r) { return r.map(csvCell_).join(','); }).join('\n');
  var slug = String(label).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  return Utilities.newBlob(csv, 'text/csv', 'playtomic-anniviers-' + slug + '.csv');
}

// Manuell: alle noch nicht exportierten Zeilen (Spalte J leer) in EINER CSV mailen
function exportPending() {
  var sh = sheet_();
  if (sh.getLastRow() < 2) return;
  var data = sh.getRange(2, 1, sh.getLastRow() - 1, HEAD_.length).getValues(), people = [], idx = [];
  data.forEach(function (r, i) {
    if (r[9]) return;
    people.push([(r[1] + ' ' + r[2]).trim(), r[3], phone_(r[4]), '', '', CATEGORY_, '', '', '']);
    idx.push(i + 2);
  });
  if (!idx.length) return;
  var stamp = Utilities.formatDate(new Date(), TZ_, 'yyyy-MM-dd');
  MailApp.sendEmail(NOTIFY_, '🏔️ Playtomic-Import Anniviers: ' + idx.length + ' Person(en)', '',
    { htmlBody: IMPORT_HOWTO_, attachments: [csvBlob_(people, 'sammel-' + stamp)], name: 'Rackets Academy' });
  idx.forEach(function (row) { sh.getRange(row, 10).setValue('CSV ' + stamp); });
}

function phone_(s) {
  var t = String(s || '').replace(/[^\d+]/g, '');
  if (!t) return '';
  if (/^00/.test(t)) t = '+' + t.slice(2);
  if (/^0\d{9}$/.test(t)) t = '+41' + t.slice(1);
  if (/^41\d{9}$/.test(t)) t = '+' + t;
  return t;
}

function csvCell_(v) {
  var s = String(v == null ? '' : v);
  return /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
}

// Test im Editor (schreibt eine Testzeile; danach im Sheet löschen)
function testPost() {
  doPost({ parameter: { first_name: 'Test', last_name: 'Anniviers', email: NOTIFY_, phone: '079 000 00 00', card_number: 'TEST-001', lang: 'fr', source: 'test' } });
}
