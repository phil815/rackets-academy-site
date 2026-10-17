/**
 * RA Website-Daten — gratis Ersatz für Supermetrics.
 * Holt täglich Google Analytics 4 (Property 556163205), Meta Ads (act_870675094567241) und Instagram
 * (@racketsacademy.ch) und schreibt alles in das Sheet «RA Website-Daten».
 * Search Console über die API (GCP-Projekt «RA Analytics», ra-analytics-511909), Tab «GSC Tage».
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
    ['Instagram Posts', function () { return igPosts_(); }],
    ['GSC Tage', function () { return gscDays_(end); }]
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
  try { igDays_(ss); log.push(['Instagram Tage', '', 'OK']); } catch (err) { log.push(['Instagram Tage', '', 'FEHLER: ' + err.message]); }
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
var SHOP_SHEET_ = '1meJ2CES_u2nFlpBLHcV0RKROFMkShiQHHVqIhA9kaoI';
var COMPANY_SHEET_ = '1-QqAHXZ9V4hoWr3UIm5W3D5YBA2z0Z4soyyRVrk00S8';
var ANNIV_SHEET_ = '1BdUSojPlZofdEi9PDIapuNF_DnxaPLui8_qp4JeKxYI';
var INTERNAL_ = /@racketsacademy\.ch$|^p\.junggutierrez@|storebotmail|@example\./i;

// Datum aus Sheet-Zelle (Date oder Text dd/MM/yyyy bzw. M/d/yyyy) → 'yyyy-MM-dd'
function day_(v, us) {
  if (v instanceof Date) return Utilities.formatDate(v, TZ_, 'yyyy-MM-dd');
  var m = String(v).match(/^(\d{1,2})[\/.](\d{1,2})[\/.](\d{4})/);
  if (!m) return '';
  var dd = us ? m[2] : m[1], mm = us ? m[1] : m[2];
  return m[3] + '-' + ('0' + mm).slice(-2) + '-' + ('0' + dd).slice(-2);
}
function countSignups_(id, tab, from, to, us) {
  var sh = SpreadsheetApp.openById(id).getSheetByName(tab);
  if (!sh || sh.getLastRow() < 2) return 0;
  return sh.getRange(2, 1, sh.getLastRow() - 1, 4).getValues().filter(function (r) {
    var d = day_(r[0], us); return r[3] && d >= from && d <= to;
  }).length;
}
// Kanal aus Quelle/Medium + Kampagne
function chan_(sm, camp) {
  sm = String(sm).toLowerCase(); camp = String(camp || '').toLowerCase();
  if (sm === 'google / maps') return 'Google Maps (Unternehmensprofil)';
  if (sm === 'google / organic' || /bing|duckduckgo|yahoo|ecosia/.test(sm)) return 'Google-Suche (gratis)';
  if (sm === 'google / cpc') return 'Google Ads';
  if (sm === 'instagram / paid' || /facebook.*paid|meta/.test(sm)) return 'Instagram/Meta Ads';
  if (/instagram|^ig \/|facebook|l\.instagram/.test(sm)) return 'Instagram/Facebook (gratis)';
  if (/_clubs/.test(camp)) return 'Mails an Clubs (Ski & Padel)';
  if (/company|partner|acor|foire|flyer/.test(sm + ' ' + camp)) return 'Firmenpartner & Flyer';
  if (/chatgpt|perplexity|claude|gemini|copilot/.test(sm)) return 'KI-Assistenten (ChatGPT & Co.)';
  if (/oppwa|sumup/.test(sm)) return 'Rückkehr von der Zahlungsseite';
  if (/l\.wl\.co|whatsapp/.test(sm)) return 'WhatsApp';
  if (sm === '(direct) / (none)') return 'Direkt (Link getippt, Lesezeichen, Apps)';
  return 'Andere';
}
function mmss_(sec) { sec = Math.round(sec || 0); return Math.floor(sec / 60) + ':' + ('0' + (sec % 60)).slice(-2); }

function weeklyReport(opts) {
  var tz = TZ_, d = function (n) { var x = new Date(); x.setDate(x.getDate() - n); return Utilities.formatDate(x, tz, 'yyyy-MM-dd'); };
  var cur = [d(7), d(1)], prev = [d(14), d(8)];
  var sum = function (rows, from, to, col) { return rows.filter(function (r) { return r[0] >= from && r[0] <= to; }).reduce(function (a, r) { return a + (Number(r[col]) || 0); }, 0); };
  var pct = function (a, b) { return b ? (a >= b ? '+' : '') + Math.round((a - b) / b * 100) + '%' : (a ? 'neu' : '–'); };
  var fmt = function (n, dec) { return Number(n).toFixed(dec || 0).replace(/\B(?=(\d{3})+(?!\d))/g, "'"); };
  var esc = function (s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); };
  var tbl = function (head, rows) {
    return '<table cellpadding="4" style="border-collapse:collapse;font-size:13px;margin:6px 0 14px"><tr style="background:#eef3f8">' + head.map(function (h, i) { return '<th align="' + (i ? 'right' : 'left') + '">' + h + '</th>'; }).join('') + '</tr>' +
      rows.map(function (r) { return '<tr>' + r.map(function (c, i) { return '<td' + (i ? ' align="right"' : '') + ' style="border-bottom:1px solid #eee">' + c + '</td>'; }).join('') + '</tr>'; }).join('') + '</table>';
  };
  var lines = [];

  // ---- Website (GA4) ----
  try {
    var tot = function (a, b) { var r = gaR_([], ['sessions', 'engagedSessions', 'totalUsers', 'userEngagementDuration'], a, b)[0] || [0, 0, 0, 0]; return r; };
    var t1 = tot(cur[0], cur[1]), t0 = tot(prev[0], prev[1]);
    var bounce = function (t) { return t[0] ? Math.round((1 - t[1] / t[0]) * 100) : 0; };
    var evNames = { book_court: 'Klick «Court buchen» (Playtomic)', whatsapp_click: 'WhatsApp-Klicks', begin_checkout: 'Bezahlvorgang gestartet' };
    var evMap = function (a, b) { var o = {}; gaR_(['eventName'], ['eventCount'], a, b, { filter: { fieldName: 'eventName', inListFilter: { values: Object.keys(evNames) } } }).forEach(function (r) { o[r[0]] = r[1]; }); return o; };
    var e1 = evMap(cur[0], cur[1]), e0 = evMap(prev[0], prev[1]);
    var evRows = Object.keys(evNames).map(function (k) { return [evNames[k], e1[k] || 0, pct(e1[k] || 0, e0[k] || 0)]; });
    var c1 = countSignups_(COMPANY_SHEET_, 'Anmeldungen', cur[0], cur[1], true), c0 = countSignups_(COMPANY_SHEET_, 'Anmeldungen', prev[0], prev[1], true);
    var a1 = countSignups_(ANNIV_SHEET_, 'Anmeldungen', cur[0], cur[1]), a0 = countSignups_(ANNIV_SHEET_, 'Anmeldungen', prev[0], prev[1]);
    evRows.push(['Anmeldungen Firmenrabatt', c1, pct(c1, c0)], ['Anmeldungen Carte d\'hôte Anniviers', a1, pct(a1, a0)]);
    // Kanäle
    var ch = {};
    gaR_(['sessionSourceMedium', 'sessionCampaignName'], ['sessions', 'engagedSessions', 'userEngagementDuration'], cur[0], cur[1]).forEach(function (r) {
      var k = chan_(r[0], r[1]); ch[k] = ch[k] || [0, 0, 0]; ch[k][0] += r[2]; ch[k][1] += r[3]; ch[k][2] += r[4];
    });
    var chRows = Object.keys(ch).sort(function (a, b) { return ch[b][0] - ch[a][0]; }).map(function (k) {
      var v = ch[k]; return [k, fmt(v[0]), v[0] ? Math.round((1 - v[1] / v[0]) * 100) + '%' : '–', mmss_(v[0] ? v[2] / v[0] : 0)];
    });
    var pages = gaR_(['pagePath'], ['screenPageViews', 'totalUsers', 'userEngagementDuration'], cur[0], cur[1]).slice(0, 8)
      .map(function (r) { return [esc(r[0]), fmt(r[1]), fmt(r[2]), mmss_(r[2] ? r[3] / r[2] : 0)]; });
    lines.push('<h3>Website</h3><p>Besuche: <b>' + fmt(t1[0]) + '</b> (' + pct(t1[0], t0[0]) + ' vs. Vorwoche) · Personen: ' + fmt(t1[2]) +
      ' · Absprungrate: <b>' + bounce(t1) + '%</b> (Vorwoche ' + bounce(t0) + '%) · Ø Zeit pro Besuch: <b>' + mmss_(t1[0] ? t1[3] / t1[0] : 0) + '</b> (Vorwoche ' + mmss_(t0[0] ? t0[3] / t0[0] : 0) + ')</p>' +
      '<p style="font-size:12px;color:#777;margin-top:-6px">Absprungrate = Besuche unter 10 Sek. mit nur 1 Seite und ohne Aktion (tiefer = besser). Ø Zeit = aktive Zeit auf der Seite.</p>' +
      '<p style="margin:10px 0 0"><b>Was die Leute gemacht haben</b></p>' + tbl(['Aktion', 'Anzahl', 'vs. Vorwoche'], evRows) +
      '<p style="margin:10px 0 0"><b>Woher sie kamen</b></p>' + tbl(['Kanal', 'Besuche', 'Absprungrate', 'Ø Zeit'], chRows) +
      '<p style="margin:10px 0 0"><b>Meistbesuchte Seiten</b></p>' + tbl(['Seite', 'Aufrufe', 'Personen', 'Ø Zeit/Person'], pages));
  } catch (e) { lines.push('<h3>Website</h3><p>Fehler: ' + esc(e.message) + '</p>'); }

  // ---- Shop & Bezahlungen (aus dem Shop-Sheet, zählt jeden Kauf – auch ohne Cookie-Zustimmung) ----
  try {
    var o = SpreadsheetApp.openById(SHOP_SHEET_).getSheetByName('Orders').getDataRange().getValues(); o.shift();
    var label = function (r) {
      var j = {}; try { j = JSON.parse(r[6]); } catch (x) {}
      if (r[3] === 'racket') return j.racketLabel || 'Schläger';
      if (r[3] === 'ticket') return /padel-dine/.test(j.eventId || '') ? 'Padel +Dine' : (j.eventId || 'Event-Ticket');
      if (r[3] === 'camp') return 'Ski & Padel ' + String(j.campId || '').replace('ski-padel-', '');
      if (r[3] === 'voucher') return 'Gutschein'; if (r[3] === 'lesson') return 'Trainerstunden-Gutschein';
      return r[3];
    };
    var rows = o.map(function (r) { return { day: day_(r[0]), name: String(r[4] || ''), email: String(r[5] || '').toLowerCase().trim(), what: label(r), amt: Number(r[7]) || 0, st: r[8], fu: r[12] || '' }; })
      .filter(function (r) { return r.email && !INTERNAL_.test(r.email); });
    var inW = function (r, w) { return r.day >= w[0] && r.day <= w[1]; };
    var paid = rows.filter(function (r) { return r.st === 'PAID' && inW(r, cur); });
    var paidPrev = rows.filter(function (r) { return r.st === 'PAID' && inW(r, prev); });
    var paidEver = {}; rows.forEach(function (r) { if (r.st === 'PAID') paidEver[r.email] = (paidEver[r.email] || '') < r.day ? r.day : paidEver[r.email]; });
    var failed = {}; rows.filter(function (r) { return (r.st === 'FAILED' || r.st === 'EXPIRED') && inW(r, cur); }).forEach(function (r) {
      if (paidEver[r.email] && paidEver[r.email] >= r.day) return; // hat danach doch bezahlt
      var f = failed[r.email] = failed[r.email] || { name: r.name, email: r.email, what: r.what, amt: r.amt, n: 0, fu: '' };
      f.n++; if (r.fu) f.fu = r.fu;
    });
    var revenue = paid.reduce(function (a, r) { return a + r.amt; }, 0), revPrev = paidPrev.reduce(function (a, r) { return a + r.amt; }, 0);
    var fl = Object.keys(failed).map(function (k) { return failed[k]; });
    lines.push('<h3>Shop & Bezahlungen</h3><p>Bezahlt: <b>' + paid.length + '</b> Kauf/Käufe · <b>CHF ' + fmt(revenue) + '</b> (Vorwoche ' + paidPrev.length + ' · CHF ' + fmt(revPrev) + ')</p>' +
      (paid.length ? tbl(['Bezahlt', 'Wer', 'CHF'], paid.map(function (r) { return [r.day.slice(8) + '.' + r.day.slice(5, 7) + '. · ' + esc(r.what), esc(r.name), fmt(r.amt)]; })) : '') +
      '<p style="margin:10px 0 0"><b>Nicht bezahlt – zum Nachfassen (' + fl.length + ')</b></p>' +
      (fl.length ? tbl(['Wer · was', 'CHF', 'Versuche', 'Follow-up'], fl.map(function (f) {
        return [esc(f.name) + ' · <a href="mailto:' + esc(f.email) + '">' + esc(f.email) + '</a><br><span style="color:#777">' + esc(f.what) + '</span>', fmt(f.amt), f.n, f.fu ? esc(String(f.fu)) : '<span style="color:#b00">offen</span>'];
      })) : '<p style="color:#777">Keine – alle Bezahlversuche gingen durch. 🎉</p>'));
  } catch (e) { lines.push('<h3>Shop & Bezahlungen</h3><p>Fehler: ' + esc(e.message) + '</p>'); }

  // ---- Meta Ads ----
  try {
    var m = metaAds_(d(1)); m.shift();
    var sp1 = sum(m, cur[0], cur[1], 4), sp0 = sum(m, prev[0], prev[1], 4), lc1 = sum(m, cur[0], cur[1], 7), lc0 = sum(m, prev[0], prev[1], 7), lp1 = sum(m, cur[0], cur[1], 8), im1 = sum(m, cur[0], cur[1], 5);
    var byAd = {};
    m.filter(function (r) { return r[0] >= cur[0] && r[0] <= cur[1]; }).forEach(function (r) {
      var k = r[1] + ' › ' + r[3]; byAd[k] = byAd[k] || [0, 0, 0]; byAd[k][0] += r[4]; byAd[k][1] += r[7]; byAd[k][2] += r[8];
    });
    var top = Object.keys(byAd).sort(function (a, b) { return byAd[b][0] - byAd[a][0]; }).slice(0, 6).map(function (k) {
      var v = byAd[k]; return [esc(k), fmt(v[0], 2), v[1], v[2], v[1] ? fmt(v[0] / v[1], 2) : '–'];
    });
    lines.push('<h3>Meta Ads</h3><p>Ausgaben: <b>CHF ' + fmt(sp1, 2) + '</b> (' + pct(sp1, sp0) + ') · Impressionen: ' + fmt(im1) + ' · Link-Klicks: <b>' + lc1 + '</b> (' + pct(lc1, lc0) + ') · Seite geladen: <b>' + lp1 + '</b>' + (lc1 ? ' (' + Math.round(lp1 / lc1 * 100) + '% der Klicks)' : '') + ' · CHF/Klick: ' + (lc1 ? fmt(sp1 / lc1, 2) : '–') + '</p>' +
      (top.length ? tbl(['Kampagne › Anzeige', 'CHF', 'Klicks', 'Seite geladen', 'CHF/Klick'], top) : '<p>Keine aktiven Anzeigen.</p>'));
  } catch (e) { lines.push('<h3>Meta Ads</h3><p>Fehler: ' + esc(e.message) + '</p>'); }

  // ---- Instagram ----
  try {
    var ss = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID'));
    var f = ss.getSheetByName('Instagram Follower').getDataRange().getDisplayValues(); f.shift();
    var now = f.length ? Number(f[f.length - 1][1]) : 0;
    var ago = f.filter(function (r) { return r[0] <= cur[0]; }).pop();
    var posts = (ss.getSheetByName('Instagram Posts').getDataRange().getValues()).slice(1).filter(function (r) { var dd = r[0] instanceof Date ? Utilities.formatDate(r[0], TZ_, 'yyyy-MM-dd') : String(r[0]); return dd >= cur[0] && dd <= cur[1]; });
    lines.push('<h3>Instagram</h3><p>Follower: <b>' + fmt(now) + '</b>' + (ago ? ' (' + ((now - Number(ago[1])) >= 0 ? '+' : '') + (now - Number(ago[1])) + ' in 7 Tagen)' : ' (Verlauf startet 16.10.)') + ' · Posts diese Woche: ' + posts.length + '</p>' +
      (posts.length ? tbl(['Post', 'Reichweite', 'Likes', 'Views'], posts.map(function (r) { return ['<a href="' + r[9] + '">' + esc(String(r[2]).slice(0, 50)) + '…</a>', fmt(r[5] || 0), r[3], fmt(r[8] || 0)]; })) : ''));
  } catch (e) { lines.push('<h3>Instagram</h3><p>Fehler: ' + esc(e.message) + '</p>'); }

  var url = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID')).getUrl();
  var body = '<div style="font-family:Arial,sans-serif;max-width:680px">' + lines.join('') +
    '<p style="color:#888;font-size:12px">Alle Details im Sheet <a href="' + url + '">RA Website-Daten</a>.</p></div>';
  saveReport_(cur, body);
  if (!(opts && opts.noMail)) MailApp.sendEmail(REPORT_TO_, '📊 Wochenbericht ' + cur[0].slice(8) + '.' + cur[0].slice(5, 7) + '.–' + cur[1].slice(8) + '.' + cur[1].slice(5, 7) + '.', '',
    { htmlBody: body, name: 'Rackets Academy Daten' });
}

// Bericht im Tab «Reports» ablegen (eine Zeile pro Woche, gleiche Woche wird überschrieben).
// Die interne Web App «RA P&L» zeigt diese Berichte im Reiter Marketing.
function saveReport_(cur, html) {
  var ss = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID'));
  var sh = ss.getSheetByName('Reports');
  if (!sh) {
    sh = ss.insertSheet('Reports');
    sh.getRange('A:B').setNumberFormat('@');
    sh.appendRow(['Woche von', 'Woche bis', 'Erstellt', 'HTML']);
  }
  if (html.length > 49000) html = html.slice(0, 49000) + '<p>… gekürzt</p>';  // Zellenlimit 50'000 Zeichen
  var weeks = sh.getLastRow() > 1 ? sh.getRange(2, 1, sh.getLastRow() - 1, 1).getDisplayValues().map(function (r) { return r[0]; }) : [];
  var i = weeks.indexOf(cur[0]), row = [cur[0], cur[1], new Date(), html];
  if (i >= 0) sh.getRange(i + 2, 1, 1, 4).setValues([row]); else sh.appendRow(row);
}

// Einmalig von Hand: Bericht ablegen, ohne Mail
function saveReportOnly() { weeklyReport({ noMail: true }); }

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
    return (r.dimensionValues || []).map(function (v) { return v.value; }).concat(r.metricValues.map(function (v) { return Number(v.value); }));
  }).sort(function (a, b) { return b[dims.length] - a[dims.length]; });
}

// ===================== Neu: Search Console, Instagram-Tageswerte, Wix-Basis =====================

var WIX_PROPERTY_ = 'properties/465019666';   // alte Wix-Website (Betrachter-Zugriff phil@)
var WIX_END_ = '2026-09-26';                   // letzter Tag mit Wix

// Search Console pro Tag (in refreshAll als Job «GSC Tage»)
function gsc_(from, to, dims) {
  var r = UrlFetchApp.fetch('https://searchconsole.googleapis.com/webmasters/v3/sites/' + encodeURIComponent(GSC_SITE_) + '/searchAnalytics/query', {
    method: 'post', contentType: 'application/json', muteHttpExceptions: true,
    headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() },
    payload: JSON.stringify({ startDate: from, endDate: to, dimensions: dims || ['date'], rowLimit: 25000 })
  });
  var body = JSON.parse(r.getContentText());
  if (body.error) throw new Error('Search Console: ' + body.error.message);
  return body.rows || [];
}
function gscDays_(end) {
  var rows = [['date', 'clicks', 'impressions', 'ctr_%', 'position']];
  gsc_(START_, end).forEach(function (r) {
    rows.push([r.keys[0], r.clicks, r.impressions, Math.round(r.ctr * 1000) / 10, Math.round(r.position * 10) / 10]);
  });
  var head = rows.shift(); rows.sort(function (a, b) { return a[0] < b[0] ? 1 : -1; }); rows.unshift(head);
  return rows;
}

// Instagram pro Tag: letzte 30 Tage neu holen, ältere Tage bleiben im Tab stehen
function igDays_(ss) {
  var sh = ss.getSheetByName('Instagram Tage') || ss.insertSheet('Instagram Tage');
  var head = ['date', 'reach', 'new_followers', 'profile_views', 'website_clicks', 'accounts_engaged', 'total_interactions', 'views'];
  var keep = {};
  if (sh.getLastRow() > 1) sh.getRange(2, 1, sh.getLastRow() - 1, head.length).getDisplayValues().forEach(function (r) { keep[r[0]] = r; });
  var now = Math.floor(Date.now() / 1000), day = 86400;
  var series = {};
  ['reach', 'follower_count'].forEach(function (m) {
    try {
      graph_(IG_ID_ + '/insights', { metric: m, period: 'day', since: now - 30 * day, until: now }).data[0].values.forEach(function (v) {
        var d = Utilities.formatDate(new Date(new Date(v.end_time).getTime() - day * 1000), TZ_, 'yyyy-MM-dd');
        (series[d] = series[d] || {})[m] = v.value;
      });
    } catch (e) {}
  });
  for (var i = 1; i <= 30; i++) {
    var since = now - (i + 1) * day, d = Utilities.formatDate(new Date(since * 1000 + day * 500), TZ_, 'yyyy-MM-dd');
    try {
      graph_(IG_ID_ + '/insights', { metric: 'profile_views,website_clicks,accounts_engaged,total_interactions,views', period: 'day', metric_type: 'total_value', since: since, until: since + day })
        .data.forEach(function (x) { (series[d] = series[d] || {})[x.name] = x.total_value ? x.total_value.value : ''; });
    } catch (e) {}
  }
  Object.keys(series).forEach(function (d) {
    var s = series[d];
    keep[d] = [d, s.reach || '', s.follower_count || 0, s.profile_views || '', s.website_clicks || '', s.accounts_engaged || '', s.total_interactions || '', s.views || ''];
  });
  var rows = Object.keys(keep).sort().reverse().map(function (k) { return keep[k]; });
  write_(ss, 'Instagram Tage', [head].concat(rows));
}

// Einmalig von Hand: Wochendurchschnitt der alten Wix-Website → Tab «Wix Basis»
function wixBaseline() {
  var ss = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID'));
  function rep(dims, mets, filter) {
    var req = { dateRanges: [{ startDate: '2023-01-01', endDate: WIX_END_ }], dimensions: dims.map(function (d) { return { name: d }; }), metrics: mets.map(function (m) { return { name: m }; }), limit: 100000 };
    if (filter) req.dimensionFilter = filter;
    return (AnalyticsData.Properties.runReport(req, WIX_PROPERTY_).rows || []).map(function (r) {
      return (r.dimensionValues || []).map(function (d) { return d.value; }).concat(r.metricValues.map(function (m) { return Number(m.value); }));
    });
  }
  var days = rep(['date'], ['sessions', 'engagedSessions', 'averageSessionDuration']).sort(function (a, b) { return a[0] < b[0] ? -1 : 1; });
  var first = days[0][0], start = first.slice(0, 4) + '-' + first.slice(4, 6) + '-' + first.slice(6, 8);
  var weeks = days.length / 7;
  var ses = 0, eng = 0, dur = 0; days.forEach(function (r) { ses += r[1]; eng += r[2]; dur += r[3] * r[1]; });
  var ch = { Google: 0, 'Instagram / Meta': 0, Direkt: 0, Andere: 0 };
  rep(['sessionSourceMedium'], ['sessions']).forEach(function (r) {
    var sm = String(r[0]).toLowerCase();
    var k = /^google|^bing/.test(sm) ? 'Google' : /instagram|^ig |^fb |facebook|^meta/.test(sm) ? 'Instagram / Meta' : /^\(direct\)/.test(sm) ? 'Direkt' : 'Andere';
    ch[k] += r[1];
  });
  var clicks = rep(['linkDomain'], ['eventCount'], { filter: { fieldName: 'eventName', stringFilter: { value: 'click' } } });
  var sumDom = function (re) { var n = 0; clicks.forEach(function (r) { if (re.test(r[0])) n += r[1]; }); return n; };
  var w = function (n) { return Math.round(n / weeks * 10) / 10; };
  var rows = [['Kennzahl', 'Ø pro Woche'],
    ['Besuche', w(ses)], ['Absprungrate %', Math.round((1 - eng / ses) * 100)], ['Besuchsdauer Sek.', Math.round(dur / ses)],
    ['Kanal Google', w(ch.Google)], ['Kanal Instagram / Meta', w(ch['Instagram / Meta'])], ['Kanal Direkt', w(ch.Direkt)], ['Kanal Andere', w(ch.Andere)],
    ['Court buchen (Klicks auf Playtomic)', w(sumDom(/playtomic/))], ['WhatsApp (Klicks auf wa.me)', w(sumDom(/^wa\.me$/))]];
  try {
    var g16 = Utilities.formatDate(new Date(Date.now() - 480 * 864e5), TZ_, 'yyyy-MM-dd');
    var g = gsc_(start > g16 ? start : g16, WIX_END_), gc = 0, gi = 0;            // Search Console hat max. 16 Monate Verlauf
    g.forEach(function (r) { gc += r.clicks; gi += r.impressions; });
    if (g.length) {
      rows.push(['Google-Suche Klicks', Math.round(gc / g.length * 7 * 10) / 10]);
      rows.push(['Google-Suche Impressionen', Math.round(gi / g.length * 7)]);
      rows.push(['Google-Suche Zeitraum', g.map(function (r) { return r.keys[0]; }).sort()[0] + ' bis ' + WIX_END_]);
    }
  } catch (e) { rows.push(['Google-Suche', 'noch nicht verfügbar: ' + e.message.slice(0, 80)]); }
  rows.push([], ['Zeitraum', start + ' bis ' + WIX_END_ + ' (' + days.length + ' Tage)']);
  write_(ss, 'Wix Basis', rows);
}

// Einmalig von Hand (bei Bedarf mehrmals): Instagram-Tageswerte rückwärts auffüllen, max. 2 Jahre (Instagram-Limit).
// Holt pro Tag Reichweite, Profilaufrufe, Link-Klicks, Interaktionen, Views. Neue Follower liefert Instagram nur 30 Tage zurück.
// Stoppt nach ca. 4.5 Minuten; nochmals ausführen, bis im Protokoll «fertig» steht.
function igBackfill() {
  var ss = SpreadsheetApp.openById(PropertiesService.getScriptProperties().getProperty('SHEET_ID'));
  var sh = ss.getSheetByName('Instagram Tage');
  var head = ['date', 'reach', 'new_followers', 'profile_views', 'website_clicks', 'accounts_engaged', 'total_interactions', 'views'];
  var keep = {};
  if (sh && sh.getLastRow() > 1) sh.getRange(2, 1, sh.getLastRow() - 1, head.length).getDisplayValues().forEach(function (r) { keep[r[0]] = r; });
  var dates = Object.keys(keep).sort();
  var d = dates.length ? dates[0] : Utilities.formatDate(new Date(), TZ_, 'yyyy-MM-dd');
  var limit = Utilities.formatDate(new Date(Date.now() - 729 * 864e5), TZ_, 'yyyy-MM-dd');
  var t0 = Date.now(), added = 0, empty = 0, done = '';
  while (Date.now() - t0 < 270000) {
    var prev = new Date(Utilities.parseDate(d, TZ_, 'yyyy-MM-dd').getTime() - 864e5 / 2);
    d = Utilities.formatDate(prev, TZ_, 'yyyy-MM-dd');
    if (d < limit) { done = 'fertig (2-Jahres-Limit)'; break; }
    var since = Math.floor(Utilities.parseDate(d, TZ_, 'yyyy-MM-dd').getTime() / 1000), v = {};
    try {
      graph_(IG_ID_ + '/insights', { metric: 'reach,profile_views,website_clicks,accounts_engaged,total_interactions,views', period: 'day', metric_type: 'total_value', since: since, until: since + 86400 })
        .data.forEach(function (x) { v[x.name] = x.total_value ? x.total_value.value : ''; });
    } catch (e) { done = 'fertig (Instagram: ' + e.message.slice(0, 80) + ')'; break; }
    if (!v.reach && !v.total_interactions) { if (++empty >= 21) { done = 'fertig (keine älteren Daten)'; break; } } else empty = 0;
    keep[d] = [d, v.reach || '', '', v.profile_views || '', v.website_clicks || '', v.accounts_engaged || '', v.total_interactions || '', v.views || ''];
    added++;
  }
  var rows = Object.keys(keep).sort().reverse().map(function (k) { return keep[k]; });
  write_(ss, 'Instagram Tage', [head].concat(rows));
  Logger.log(added + ' Tage ergänzt, ältester Tag ' + rows[rows.length - 1][0] + '. ' + (done || 'Noch nicht fertig: igBackfill nochmals ausführen.'));
}
