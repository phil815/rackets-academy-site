/**
 * RA Website-Daten — gratis Ersatz für Supermetrics.
 * Holt täglich Google Analytics 4 (Property 556163205) und Google Search Console
 * (sc-domain:racketsacademy.ch) und schreibt alles in das Sheet «RA Website-Daten».
 * Claude liest dieses Sheet für Auswertungen.
 *
 * Einrichtung (einmalig): Funktion «setup» ausführen → Zugriff erlauben.
 * Danach läuft «refreshAll» jeden Morgen um ca. 6 Uhr automatisch.
 * Jeder Lauf schreibt die Tabs komplett neu ab START_ (kein Doppeltes, Korrekturen von Google werden übernommen).
 */
var GA_PROPERTY_ = 'properties/556163205';
var GSC_SITE_ = 'sc-domain:racketsacademy.ch';
var START_ = '2026-09-27';
var TZ_ = 'Europe/Zurich';
var KEY_EVENTS_ = ['book_court', 'whatsapp_click', 'begin_checkout', 'purchase', 'generate_lead', 'form_start', 'form_submit', 'gallery_open', 'view_item'];

function setup() {
  var props = PropertiesService.getScriptProperties();
  var id = props.getProperty('SHEET_ID');
  var ss = id ? SpreadsheetApp.openById(id) : SpreadsheetApp.create('RA Website-Daten');
  props.setProperty('SHEET_ID', ss.getId());
  ScriptApp.getProjectTriggers().forEach(function (t) {
    if (t.getHandlerFunction() === 'refreshAll') ScriptApp.deleteTrigger(t);
  });
  ScriptApp.newTrigger('refreshAll').timeBased().everyDays(1).atHour(6).inTimezone(TZ_).create();
  refreshAll();
  Logger.log('Sheet: ' + ss.getUrl());
}

function refreshAll() {
  var ss = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID'));
  var end = Utilities.formatDate(new Date(), TZ_, 'yyyy-MM-dd');
  var log = [];
  var jobs = [
    ['GA Tage', function () { return ga_(['date'], ['sessions', 'engagedSessions', 'bounceRate', 'totalUsers', 'newUsers', 'screenPageViews', 'averageSessionDuration'], end); }],
    ['GA Quellen', function () { return ga_(['date', 'sessionSourceMedium', 'sessionCampaignName'], ['sessions', 'engagedSessions', 'userEngagementDuration'], end); }],
    ['GA Einstiegsseiten', function () { return ga_(['date', 'landingPage', 'sessionSourceMedium', 'deviceCategory'], ['sessions', 'engagedSessions', 'userEngagementDuration'], end); }],
    ['GA Seiten', function () { return ga_(['date', 'pagePath'], ['screenPageViews', 'totalUsers', 'sessions', 'userEngagementDuration'], end); }],
    ['GA Ereignisse', function () { return ga_(['date', 'eventName', 'pagePath'], ['eventCount', 'totalUsers'], end, { filter: { fieldName: 'eventName', inListFilter: { values: KEY_EVENTS_ } } }); }],
    ['GA Länder & Geräte', function () { return ga_(['date', 'country', 'city', 'deviceCategory'], ['sessions', 'engagedSessions'], end); }],
    ['GSC Tage', function () { return gsc_(['date'], end); }],
    ['GSC Seiten', function () { return gsc_(['date', 'page'], end); }],
    ['GSC Suchbegriffe', function () { return gsc_(['date', 'query', 'page'], end); }]
  ];
  jobs.forEach(function (j) {
    try {
      var rows = j[1]();
      write_(ss, j[0], rows);
      log.push([j[0], rows.length - 1, 'OK']);
    } catch (err) {
      log.push([j[0], '', 'FEHLER: ' + err.message]);
    }
  });
  var info = [['Stand', Utilities.formatDate(new Date(), TZ_, 'dd.MM.yyyy HH:mm')], ['Zeitraum', START_ + ' bis ' + end], [], ['Tab', 'Zeilen', 'Status']].concat(log);
  write_(ss, 'Info', info);
  var first = ss.getSheetByName('Sheet1') || ss.getSheetByName('Tabelle1') || ss.getSheetByName('Feuille 1');
  if (first && ss.getSheets().length > 1) ss.deleteSheet(first);
}

// ---- Google Analytics 4 (Erweiterter Dienst «Google Analytics Data API») ----
function ga_(dims, mets, end, dimFilter) {
  var out = [dims.concat(mets)], offset = 0, limit = 100000;
  while (true) {
    var req = {
      dateRanges: [{ startDate: START_, endDate: end }],
      dimensions: dims.map(function (d) { return { name: d }; }),
      metrics: mets.map(function (m) { return { name: m }; }),
      limit: limit, offset: offset, keepEmptyRows: false
    };
    if (dimFilter) req.dimensionFilter = dimFilter;
    var res = AnalyticsData.Properties.runReport(req, GA_PROPERTY_);
    (res.rows || []).forEach(function (r) {
      var row = r.dimensionValues.map(function (v, i) {
        return dims[i] === 'date' ? v.value.slice(0, 4) + '-' + v.value.slice(4, 6) + '-' + v.value.slice(6, 8) : v.value;
      });
      r.metricValues.forEach(function (v) { row.push(Number(v.value)); });
      out.push(row);
    });
    offset += limit;
    if (!res.rowCount || offset >= res.rowCount) break;
  }
  if (dims[0] === 'date') { var head = out.shift(); out.sort(function (a, b) { return a[0] < b[0] ? 1 : a[0] > b[0] ? -1 : 0; }); out.unshift(head); }
  return out;
}

// ---- Google Search Console (Search Analytics API) ----
function gsc_(dims, end) {
  var url = 'https://searchconsole.googleapis.com/webmasters/v3/sites/' + encodeURIComponent(GSC_SITE_) + '/searchAnalytics/query';
  var out = [dims.concat(['clicks', 'impressions', 'ctr', 'position'])], startRow = 0;
  while (true) {
    var res = UrlFetchApp.fetch(url, {
      method: 'post', contentType: 'application/json', muteHttpExceptions: true,
      headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() },
      payload: JSON.stringify({ startDate: START_, endDate: end, dimensions: dims, rowLimit: 25000, startRow: startRow, dataState: 'all' })
    });
    if (res.getResponseCode() !== 200) throw new Error('Search Console HTTP ' + res.getResponseCode() + ': ' + res.getContentText().slice(0, 300));
    var rows = JSON.parse(res.getContentText()).rows || [];
    rows.forEach(function (r) {
      out.push(r.keys.concat([r.clicks, r.impressions, Math.round(r.ctr * 10000) / 10000, Math.round(r.position * 10) / 10]));
    });
    if (rows.length < 25000) break;
    startRow += 25000;
  }
  if (dims[0] === 'date') { var head = out.shift(); out.sort(function (a, b) { return a[0] < b[0] ? 1 : a[0] > b[0] ? -1 : 0; }); out.unshift(head); }
  return out;
}

function write_(ss, name, rows) {
  var sh = ss.getSheetByName(name) || ss.insertSheet(name);
  sh.clearContents();
  if (!rows.length) return;
  var width = rows.reduce(function (m, r) { return Math.max(m, r.length); }, 1);
  rows = rows.map(function (r) { while (r.length < width) r.push(''); return r; });
  sh.getRange(1, 1, rows.length, width).setValues(rows);
  sh.getRange(1, 1, 1, width).setFontWeight('bold');
  sh.setFrozenRows(1);
}
