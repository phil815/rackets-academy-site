/**
 * RA Website-Daten — gratis Ersatz für Supermetrics.
 * Holt täglich Google Analytics 4 (Property 556163205), Meta Ads (act_870675094567241) und Instagram
 * (@racketsacademy.ch) und schreibt alles in das Sheet «RA Website-Daten».
 * Search Console läuft über Windsor.ai (gratis), nicht über dieses Script.
 * Meta/Instagram: Skripteigenschaft META_TOKEN = System-User-Token (ads_read, instagram_basic, instagram_manage_insights).
 * Montags 7 Uhr: Wochenbericht per Mail (Website + Meta Ads + Instagram).
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
var META_ACT_ = 'act_870675094567241';
var IG_ID_ = '17841465666000216';
var GRAPH_ = 'https://graph.facebook.com/v22.0/';
var REPORT_TO_ = 'phil@racketsacademy.ch';
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
  ScriptApp.getProjectTriggers().forEach(function (t) { if (t.getHandlerFunction() === 'weeklyReport') ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('weeklyReport').timeBased().onWeekDay(ScriptApp.WeekDay.MONDAY).atHour(7).inTimezone(TZ_).create();
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
    ['Meta Ads', function () { return metaAds_(end); }],
    ['Instagram Posts', function () { return igPosts_(); }]
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
  try { igFollowers_(ss); log.push(['Instagram Follower', '', 'OK']); } catch (err) { log.push(['Instagram Follower', '', 'FEHLER: ' + err.message]); }
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

// ---- Meta Graph API (Ads + Instagram) ----
function graph_(path, params) {
  var token = PropertiesService.getScriptProperties().getProperty('META_TOKEN');
  if (!token) throw new Error('META_TOKEN fehlt (Projekteinstellungen → Skripteigenschaften)');
  var q = Object.keys(params || {}).map(function (k) { return k + '=' + encodeURIComponent(params[k]); });
  q.push('access_token=' + encodeURIComponent(token));
  var url = (/^https:/.test(path) ? path : GRAPH_ + path) + (/\?/.test(path) ? '&' : '?') + q.join('&');
  var res = UrlFetchApp.fetch(url, { muteHttpExceptions: true });
  var body = JSON.parse(res.getContentText());
  if (body.error) throw new Error('Meta: ' + body.error.message);
  return body;
}
function graphAll_(path, params) {
  var out = [], body = graph_(path, params);
  while (true) {
    out = out.concat(body.data || []);
    if (!body.paging || !body.paging.next) break;
    body = JSON.parse(UrlFetchApp.fetch(body.paging.next).getContentText());
  }
  return out;
}
function action_(arr, type) {
  var v = 0; (arr || []).forEach(function (a) { if (a.action_type === type) v = Number(a.value); }); return v;
}

// Meta Ads: pro Tag und Anzeige
function metaAds_(end) {
  var rows = [['date', 'campaign', 'adset', 'ad', 'spend_chf', 'impressions', 'reach', 'link_clicks', 'landing_page_views', 'video_3s_views', 'ctr_link_%', 'cpc_link_chf']];
  graphAll_(META_ACT_ + '/insights', {
    level: 'ad', time_increment: 1, limit: 500,
    time_range: JSON.stringify({ since: START_, until: end }),
    fields: 'date_start,campaign_name,adset_name,ad_name,spend,impressions,reach,inline_link_clicks,actions'
  }).forEach(function (r) {
    var clicks = Number(r.inline_link_clicks || 0), spend = Number(r.spend || 0), imp = Number(r.impressions || 0);
    rows.push([r.date_start, r.campaign_name, r.adset_name, r.ad_name, spend, imp, Number(r.reach || 0), clicks,
      action_(r.actions, 'landing_page_view'), action_(r.actions, 'video_view'),
      imp ? Math.round(clicks / imp * 10000) / 100 : 0, clicks ? Math.round(spend / clicks * 100) / 100 : '']);
  });
  var head = rows.shift(); rows.sort(function (a, b) { return a[0] < b[0] ? 1 : a[0] > b[0] ? -1 : 0; }); rows.unshift(head);
  return rows;
}

// Instagram: letzte 50 Posts mit Reichweite/Interaktionen
function igPosts_() {
  var rows = [['date', 'type', 'caption', 'likes', 'comments', 'reach', 'saved', 'shares', 'views', 'link']];
  graph_(IG_ID_ + '/media', { fields: 'id,timestamp,media_type,caption,like_count,comments_count,permalink', limit: 50 }).data.forEach(function (m) {
    var ins = {};
    try {
      graph_(m.id + '/insights', { metric: 'reach,saved,shares,views' }).data.forEach(function (d) { ins[d.name] = d.values[0].value; });
    } catch (e) {}
    rows.push([String(m.timestamp).slice(0, 10), m.media_type, String(m.caption || '').replace(/\s+/g, ' ').slice(0, 80),
      m.like_count || 0, m.comments_count || 0, ins.reach || '', ins.saved || '', ins.shares || '', ins.views || '', m.permalink]);
  });
  return rows;
}

// Instagram: Followerzahl pro Tag (Verlauf wird angehängt, nicht überschrieben)
function igFollowers_(ss) {
  var me = graph_(IG_ID_, { fields: 'followers_count,media_count' });
  var sh = ss.getSheetByName('Instagram Follower') || ss.insertSheet('Instagram Follower');
  if (sh.getLastRow() === 0) { sh.appendRow(['date', 'followers', 'posts']); sh.getRange(1, 1, 1, 3).setFontWeight('bold'); sh.setFrozenRows(1); }
  var today = Utilities.formatDate(new Date(), TZ_, 'yyyy-MM-dd');
  var last = sh.getLastRow() > 1 ? sh.getRange(sh.getLastRow(), 1).getDisplayValue() : '';
  if (last === today) sh.getRange(sh.getLastRow(), 2, 1, 2).setValues([[me.followers_count, me.media_count]]);
  else sh.appendRow([today, me.followers_count, me.media_count]);
}

// ---- Wochenbericht (Montag 7 Uhr) ----
function weeklyReport() {
  var tz = TZ_, d = function (n) { var x = new Date(); x.setDate(x.getDate() - n); return Utilities.formatDate(x, tz, 'yyyy-MM-dd'); };
  var cur = [d(7), d(1)], prev = [d(14), d(8)];
  var sum = function (rows, from, to, col) { return rows.filter(function (r) { return r[0] >= from && r[0] <= to; }).reduce(function (a, r) { return a + (Number(r[col]) || 0); }, 0); };
  var pct = function (a, b) { return b ? (a >= b ? '+' : '') + Math.round((a - b) / b * 100) + '%' : '–'; };
  var fmt = function (n, dec) { return Number(n).toFixed(dec || 0).replace(/\B(?=(\d{3})+(?!\d))/g, "'"); };
  var lines = [];
  // Website (GA4)
  try {
    var ga = ga_(['date'], ['sessions', 'engagedSessions', 'totalUsers'], d(1));
    ga.shift();
    var s1 = sum(ga, cur[0], cur[1], 1), s0 = sum(ga, prev[0], prev[1], 1), e1 = sum(ga, cur[0], cur[1], 2), u1 = sum(ga, cur[0], cur[1], 3);
    var tbl = function (head, rows) {
      return '<table cellpadding="4" style="border-collapse:collapse;font-size:13px;margin:6px 0 12px"><tr style="background:#eef3f8">' + head.map(function (h, i) { return '<th align="' + (i ? 'right' : 'left') + '">' + h + '</th>'; }).join('') + '</tr>' +
        rows.map(function (r) { return '<tr>' + r.map(function (c, i) { return '<td' + (i ? ' align="right"' : '') + '>' + c + '</td>'; }).join('') + '</tr>'; }).join('') + '</table>';
    };
    var src = gaR_(['sessionSourceMedium'], ['sessions', 'engagedSessions'], cur[0], cur[1]).slice(0, 6)
      .map(function (r) { return [r[0], fmt(r[1]), r[1] ? Math.round(r[2] / r[1] * 100) + '%' : '–']; });
    var pages = gaR_(['pagePath'], ['screenPageViews', 'totalUsers'], cur[0], cur[1]).slice(0, 8)
      .map(function (r) { return [r[0], fmt(r[1]), fmt(r[2])]; });
    var evNames = { book_court: 'Klick «Court buchen» (Playtomic)', whatsapp_click: 'WhatsApp-Klicks', begin_checkout: 'Bezahlvorgang gestartet', purchase: 'Käufe', generate_lead: 'Anmeldungen (Firmen/Anniviers)' };
    var ev = gaR_(['eventName'], ['eventCount'], cur[0], cur[1], { filter: { fieldName: 'eventName', inListFilter: { values: Object.keys(evNames) } } });
    var evPrev = {}; gaR_(['eventName'], ['eventCount'], prev[0], prev[1], { filter: { fieldName: 'eventName', inListFilter: { values: Object.keys(evNames) } } }).forEach(function (r) { evPrev[r[0]] = r[1]; });
    var evRows = Object.keys(evNames).map(function (k) { var v = 0; ev.forEach(function (r) { if (r[0] === k) v = r[1]; }); return [evNames[k], v, pct(v, evPrev[k] || 0)]; });
    lines.push('<h3>Website</h3><p>Besuche: <b>' + fmt(s1) + '</b> (' + pct(s1, s0) + ' vs. Vorwoche) · Personen: ' + fmt(u1) + ' · engagiert: ' + (s1 ? Math.round(e1 / s1 * 100) : 0) + '%</p>' +
      '<p style="margin:10px 0 0"><b>Was die Leute gemacht haben</b></p>' + tbl(['Aktion', 'Anzahl', 'vs. Vorwoche'], evRows) +
      '<p style="margin:10px 0 0"><b>Woher sie kamen</b></p>' + tbl(['Quelle', 'Besuche', 'engagiert'], src) +
      '<p style="margin:10px 0 0"><b>Meistbesuchte Seiten</b></p>' + tbl(['Seite', 'Aufrufe', 'Personen'], pages));
  } catch (e) { lines.push('<p>Website: Fehler ' + e.message + '</p>'); }
  // Meta Ads
  try {
    var m = metaAds_(d(1)); m.shift();
    var sp1 = sum(m, cur[0], cur[1], 4), sp0 = sum(m, prev[0], prev[1], 4), lc1 = sum(m, cur[0], cur[1], 7), lc0 = sum(m, prev[0], prev[1], 7), lp1 = sum(m, cur[0], cur[1], 8), im1 = sum(m, cur[0], cur[1], 5);
    var byAd = {};
    m.filter(function (r) { return r[0] >= cur[0] && r[0] <= cur[1]; }).forEach(function (r) {
      var k = r[1] + ' › ' + r[3]; byAd[k] = byAd[k] || [0, 0, 0]; byAd[k][0] += r[4]; byAd[k][1] += r[7]; byAd[k][2] += r[8];
    });
    var top = Object.keys(byAd).sort(function (a, b) { return byAd[b][0] - byAd[a][0]; }).slice(0, 6).map(function (k) {
      var v = byAd[k]; return '<tr><td>' + k + '</td><td align="right">' + fmt(v[0], 2) + '</td><td align="right">' + v[1] + '</td><td align="right">' + v[2] + '</td><td align="right">' + (v[1] ? fmt(v[0] / v[1], 2) : '–') + '</td></tr>';
    }).join('');
    lines.push('<h3>Meta Ads</h3><p>Ausgaben: <b>CHF ' + fmt(sp1, 2) + '</b> (' + pct(sp1, sp0) + ') · Impressionen: ' + fmt(im1) + ' · Link-Klicks: <b>' + lc1 + '</b> (' + pct(lc1, lc0) + ') · Landingpage-Aufrufe: <b>' + lp1 + '</b> · CHF/Klick: ' + (lc1 ? fmt(sp1 / lc1, 2) : '–') + '</p>' +
      (top ? '<table cellpadding="4" style="border-collapse:collapse;font-size:13px"><tr style="background:#eef3f8"><th align="left">Kampagne › Anzeige</th><th>CHF</th><th>Klicks</th><th>LP-Aufrufe</th><th>CHF/Klick</th></tr>' + top + '</table>' : '<p>Keine aktiven Anzeigen.</p>'));
  } catch (e) { lines.push('<h3>Meta Ads</h3><p>Fehler: ' + e.message + '</p>'); }
  // Instagram
  try {
    var ss = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID'));
    var f = ss.getSheetByName('Instagram Follower').getDataRange().getDisplayValues(); f.shift();
    var now = f.length ? Number(f[f.length - 1][1]) : 0;
    var ago = f.filter(function (r) { return r[0] <= cur[0]; }).pop();
    lines.push('<h3>Instagram</h3><p>Follower: <b>' + fmt(now) + '</b>' + (ago ? ' (' + ((now - Number(ago[1])) >= 0 ? '+' : '') + (now - Number(ago[1])) + ' in 7 Tagen)' : '') + '</p>');
  } catch (e) { lines.push('<h3>Instagram</h3><p>Fehler: ' + e.message + '</p>'); }
  var url = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID')).getUrl();
  MailApp.sendEmail(REPORT_TO_, '📊 Wochenbericht ' + cur[0].slice(8) + '.' + cur[0].slice(5, 7) + '.–' + cur[1].slice(8) + '.' + cur[1].slice(5, 7) + '.', '',
    { htmlBody: '<div style="font-family:Arial,sans-serif;max-width:640px">' + lines.join('') + '<p style="color:#888;font-size:12px">Alle Details im Sheet <a href="' + url + '">RA Website-Daten</a>.</p></div>', name: 'Rackets Academy Daten' });
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

// GA4 für einen beliebigen Zeitraum, sortiert nach erster Kennzahl (absteigend)
function gaR_(dims, mets, from, to, dimFilter) {
  var req = { dateRanges: [{ startDate: from, endDate: to }], dimensions: dims.map(function (d) { return { name: d }; }), metrics: mets.map(function (m) { return { name: m }; }), limit: 1000 };
  if (dimFilter) req.dimensionFilter = dimFilter;
  var res = AnalyticsData.Properties.runReport(req, GA_PROPERTY_);
  return (res.rows || []).map(function (r) {
    return r.dimensionValues.map(function (v) { return v.value; }).concat(r.metricValues.map(function (v) { return Number(v.value); }));
  }).sort(function (a, b) { return b[dims.length] - a[dims.length]; });
}
