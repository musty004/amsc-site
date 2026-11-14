/* AMSC Student Portal (Islamiyyah and Dawrah)
   One page app: sign-up and log-in, the student dashboard, Qur'an progress, library,
   classes and profile, plus teacher and admin tools.
   Data lives in Supabase. Who can see or change what is enforced by the database's
   security rules (see _source/portal/setup.sql), not by this file. */
(function () {
  'use strict';

  var CFG = window.AMSC_PORTAL || {};
  var DATA = window.AMSC_DATA;
  var root = document.getElementById('portal');
  if (!root) return;
  window.AMSC_PORTAL_STARTED = true;

  // ===================================================================== helpers
  function Safe(s) { this.s = s; }
  Safe.prototype.toString = function () { return this.s; };
  var raw = function (s) { return new Safe(String(s)); };
  var ESC = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  var esc = function (v) { return String(v == null ? '' : v).replace(/[&<>"']/g, function (c) { return ESC[c]; }); };
  function out(v) {
    if (v instanceof Safe) return v.s;
    if (Array.isArray(v)) return v.map(out).join('');
    if (v === false || v === null || v === undefined) return '';
    return esc(v);
  }
  // Tagged template: every value is escaped unless it is already safe HTML.
  function html(strings) {
    var s = strings[0];
    for (var i = 1; i < arguments.length; i++) s += out(arguments[i]) + strings[i];
    return new Safe(s);
  }
  var $ = function (sel, el) { return (el || document).querySelector(sel); };
  var $$ = function (sel, el) { return Array.prototype.slice.call((el || document).querySelectorAll(sel)); };
  var safeUrl = function (u) { return /^https?:\/\//i.test(u || '') ? u : '#'; };
  var firstName = function (n) { return String(n || '').trim().split(/\s+/)[0] || ''; };
  var initials = function (n) {
    var p = String(n || '').trim().split(/\s+/);
    return ((p[0] || '')[0] || '').toUpperCase() + ((p.length > 1 ? p[p.length - 1][0] : '') || '').toUpperCase();
  };
  var fmtNum = function (n) { return Number(n || 0).toLocaleString('en-NG'); };
  var plural = function (n, one, many) { return fmtNum(n) + ' ' + (n === 1 ? one : (many || one + 's')); };

  function toDate(s) { return /^\d{4}-\d{2}-\d{2}$/.test(s) ? new Date(s + 'T12:00:00Z') : new Date(s); }
  function fmtDate(s, withYear) {
    if (!s) return '';
    var o = { weekday: 'short', day: 'numeric', month: 'short', timeZone: 'Africa/Lagos' };
    if (withYear !== false) o.year = 'numeric';
    return toDate(s).toLocaleDateString('en-GB', o);
  }
  function todayISO() { return new Intl.DateTimeFormat('en-CA', { timeZone: 'Africa/Lagos' }).format(new Date()); }
  function lagosNow() { var d = new Date(); return new Date(d.getTime() + d.getTimezoneOffset() * 60000 + 3600000); }

  function waLink(phone, text) {
    var d = String(phone || '').replace(/\D/g, '');
    if (!d) return '';
    if (d.charAt(0) === '0') d = '234' + d.slice(1);
    return 'https://wa.me/' + d + (text ? '?text=' + encodeURIComponent(text) : '');
  }
  function fmtSize(b) {
    if (!b) return '';
    return b < 1048576 ? Math.max(1, Math.round(b / 1024)) + ' KB' : (b / 1048576).toFixed(1) + ' MB';
  }
  function friendly(e) {
    var m = (e && (e.message || e.msg || e.error_description)) || String(e || '');
    if (/Failed to fetch|NetworkError|Load failed|network/i.test(m)) return 'We could not reach the portal. Check your internet connection and try again.';
    if (/Invalid login credentials/i.test(m)) return 'The email or password is not correct.';
    if (/already registered|already exists/i.test(m)) return 'An account with this email already exists. Log in instead.';
    if (/Database error saving new user/i.test(m)) return 'We could not create your account just now. Please try again, or contact the Islamiyyah admin.';
    if (/same_password|different from the old/i.test(m)) return 'Choose a password different from your current one.';
    if (/weak|at least 6/i.test(m)) return 'Choose a longer password (at least 8 characters).';
    if (/rate limit|too many/i.test(m)) return 'Too many attempts. Wait a few minutes and try again.';
    if (/not authorized|Email address not authorized/i.test(m)) return 'Email resets are not switched on yet. Ask the Islamiyyah admin to reset your password.';
    if (e && e.code === '42501') return /Only an admin|cannot/.test(m) ? m : 'You do not have permission to do that.';
    if (/row-level security|violates row/i.test(m)) return 'You do not have permission to do that.';
    return m || 'Something went wrong. Please try again.';
  }
  async function run(p) {
    var r = await p;
    if (r.error) throw r.error;
    return r.data;
  }
  async function count(q) {
    var r = await q;
    if (r.error) throw r.error;
    return r.count || 0;
  }

  // ------------------------------------------------------------------ labels
  var LEVEL = { beginner: 'Beginner', intermediate: 'Intermediate', advanced: 'Advanced' };
  var QLEVEL = { beginner: 'Beginner', intermediate: 'Intermediate', advanced: 'Advanced / Hifz' };
  var TRACK = { quran: 'Qur’an', arabic: 'Arabic', books: 'Islamic book studies' };
  var KIND = { memorisation: 'Memorisation', revision: 'Revision (Muraja’ah)', recitation: 'Recitation (Tarteel)' };
  var ROLE = { student: 'Student', teacher: 'Teacher', admin: 'Admin' };
  var STATUS = { pending: 'Awaiting approval', active: 'Active', inactive: 'Inactive' };
  var WING = { brothers: 'Brothers', sisters: 'Sisters', mixed: 'Brothers and sisters' };
  var SUBJECT = { quran: 'Qur’an', tajweed: 'Tajweed', arabic: 'Arabic', aqeedah: 'Aqeedah and Tawheed', fiqh: 'Fiqh', seerah: 'Seerah', hadith: 'Hadith', general: 'General' };
  var AUDIENCE = { all: 'Everyone', brothers: 'Brothers', sisters: 'Sisters', group: 'Group' };
  var STUDY_LEVELS = ['100L', '200L', '300L', '400L', '500L', 'Postgraduate', 'Staff or other'];

  function opts(map, sel, blank) {
    var o = blank !== undefined ? html`<option value="">${blank}</option>` : '';
    return [o].concat(Object.keys(map).map(function (k) {
      return html`<option value="${k}"${raw(k === sel ? ' selected' : '')}>${map[k]}</option>`;
    }));
  }

  // ------------------------------------------------------------------ icons
  var P = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"';
  var ICONS = {
    quran: '<path d="M12 6.5S9.5 4 5 4v14c4.5 0 7 2 7 2s2.5-2 7-2V4c-4.5 0-7 2.5-7 2.5Z"/><path d="M12 6.5V20"/>',
    book: '<path d="M4 4.5A2.5 2.5 0 0 1 6.5 2H20v18H6.5A2.5 2.5 0 0 0 4 22z"/><path d="M8 7h8M8 11h6"/>',
    calendar: '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    users: '<circle cx="9" cy="8" r="3.2"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 5.5a3.2 3.2 0 0 1 0 6M17.5 14.4A6.5 6.5 0 0 1 21.5 20"/>',
    download: '<path d="M12 3v12M7.5 11 12 15.5 16.5 11"/><path d="M4 19h16"/>',
    external: '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>',
    check: '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    bell: '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
    star: '<path d="m12 3.5 2.6 5.4 5.9.8-4.3 4.2 1 5.9-5.2-2.8L6.8 19.8l1-5.9L3.5 9.7l5.9-.8Z"/>',
    shield: '<path d="M12 3 20 6v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6Z"/><path d="m9 12 2 2 4-4"/>',
    alert: '<path d="M12 3 2 20h20Z"/><path d="M12 10v4M12 17h.01"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    trash: '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/>',
    phone: '<path d="M6 3h3l1.5 4.5-2 1.5a12 12 0 0 0 6.5 6.5l1.5-2L21 15v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4 5.2 2 2 0 0 1 6 3Z"/>',
    file: '<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8Z"/><path d="M14 3v5h5"/>',
    link: '<path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/><path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/>',
    whatsapp: '<path d="M12 2a10 10 0 0 0-8.6 15L2 22l5.2-1.4A10 10 0 1 0 12 2Z"/><path d="M8.5 8.5c.5 2.8 2.7 5 5.5 5.5l1.2-1.2 2 1-.4 1.6c-3.8.4-8.6-4.4-8.2-8.2l1.6-.4 1 2Z"/>'
  };
  var icon = function (n, cls) { return raw('<svg class="' + (cls || 'ico') + '" ' + P + '>' + ICONS[n] + '</svg>'); };

  // ===================================================================== state
  var S = { sb: null, user: null, me: null, recovery: false, nav: 0 };
  var isStaff = function () { return S.me && S.me.status === 'active' && (S.me.role === 'teacher' || S.me.role === 'admin'); };
  var isAdmin = function () { return S.me && S.me.status === 'active' && S.me.role === 'admin'; };
  function token() { var t = ++S.nav; return function () { return t === S.nav; }; }
  function go(hash) { if (location.hash === hash) route(); else location.hash = hash; }

  // ------------------------------------------------------------------ notices
  var live = document.getElementById('portal-live');
  function announce(msg) { if (live) { live.textContent = ''; setTimeout(function () { live.textContent = msg; }, 30); } }
  function toast(msg, kind) {
    var t = document.createElement('div');
    t.className = 'pt-toast' + (kind === 'error' ? ' pt-toast--error' : '');
    t.textContent = msg;
    document.body.appendChild(t);
    announce(msg);
    setTimeout(function () { t.classList.add('is-out'); setTimeout(function () { t.remove(); }, 400); }, 3600);
  }
  function formError(form, msg) {
    var e = $('.form-error', form);
    if (!e) return;
    e.textContent = msg || '';
    e.hidden = !msg;
    if (msg) e.focus();
  }
  function busy(btn, on, label) {
    if (!btn) return;
    if (on) { btn._html = btn.innerHTML; btn.disabled = true; btn.setAttribute('aria-busy', 'true'); btn.textContent = label || 'Please wait…'; }
    else { btn.disabled = false; btn.removeAttribute('aria-busy'); if (btn._html !== undefined) { btn.innerHTML = btn._html; delete btn._html; } }
  }
  // Wire a form: validation by the browser, then fn(values, form). Errors land in the form.
  function onSubmit(form, fn) {
    if (!form) return;
    form.addEventListener('submit', async function (ev) {
      ev.preventDefault();
      formError(form, '');
      var btn = $('button[type=submit]', form);
      var vals = {};
      new FormData(form).forEach(function (v, k) { vals[k] = typeof v === 'string' ? v.trim() : v; });
      busy(btn, true);
      try { await fn(vals, form); }
      catch (e) { formError(form, friendly(e)); }
      finally { if (document.body.contains(btn)) busy(btn, false); }
    });
  }

  // ===================================================================== Qur'an maths
  var SURAHS = DATA ? DATA.surahs : [];
  var OFFSET = [0];
  SURAHS.forEach(function (s, i) { OFFSET[i + 1] = OFFSET[i] + s[4]; });
  var TOTAL = OFFSET[SURAHS.length] || 6236;
  var JUZ = DATA ? DATA.juz.map(function (j) { return OFFSET[j[0] - 1] + j[1] - 1; }) : [];
  JUZ.push(TOTAL);
  var surah = function (n) { return SURAHS[n - 1]; };
  var surahName = function (n) { var s = surah(n); return s ? s[1] : 'Surah ' + n; };
  var rangeText = function (l) {
    var s = surah(l.surah);
    var whole = s && l.from_ayah === 1 && l.to_ayah === s[4];
    return surahName(l.surah) + (whole ? ' (whole surah)' : ', ayah ' + l.from_ayah + (l.to_ayah !== l.from_ayah ? '–' + l.to_ayah : ''));
  };

  function progress(logs) {
    var mem = new Uint8Array(TOTAL), ver = new Uint8Array(TOTAL);
    var lastDate = null, revision30 = 0;
    var cutoff = new Date(Date.now() - 30 * 864e5).toISOString().slice(0, 10);
    logs.forEach(function (l) {
      if (!lastDate || l.log_date > lastDate) lastDate = l.log_date;
      if (l.kind === 'memorisation') {
        var a = OFFSET[l.surah - 1] + l.from_ayah - 1, b = OFFSET[l.surah - 1] + l.to_ayah - 1;
        for (var i = a; i <= b && i < TOTAL; i++) { mem[i] = 1; if (l.verified) ver[i] = 1; }
      }
      if (l.kind === 'revision' && l.log_date >= cutoff) revision30 += l.to_ayah - l.from_ayah + 1;
    });
    var memorised = 0, verified = 0, i;
    for (i = 0; i < TOTAL; i++) { memorised += mem[i]; verified += ver[i]; }
    var juz = [];
    for (var j = 0; j < 30; j++) {
      var c = 0;
      for (i = JUZ[j]; i < JUZ[j + 1]; i++) c += mem[i];
      juz.push(c / (JUZ[j + 1] - JUZ[j]));
    }
    var bySurah = [];
    SURAHS.forEach(function (s, k) {
      var c2 = 0;
      for (var x = OFFSET[k]; x < OFFSET[k + 1]; x++) c2 += mem[x];
      if (c2) bySurah.push({ n: s[0], done: c2, total: s[4] });
    });
    return {
      memorised: memorised, verified: verified, pct: memorised / TOTAL, juz: juz, bySurah: bySurah,
      juzDone: juz.filter(function (v) { return v >= 0.999; }).length,
      juzEquiv: memorised / TOTAL * 30, lastDate: lastDate, revision30: revision30
    };
  }
  // Ayahs logged as memorised in each of the last 12 weeks (weeks start on Monday).
  function weekly(logs) {
    var now = lagosNow();
    var monday = new Date(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()));
    monday.setUTCDate(monday.getUTCDate() - ((monday.getUTCDay() + 6) % 7));
    var weeks = [];
    for (var w = 11; w >= 0; w--) {
      var start = new Date(monday.getTime() - w * 7 * 864e5);
      weeks.push({ start: start.toISOString().slice(0, 10), end: new Date(start.getTime() + 6 * 864e5).toISOString().slice(0, 10), v: 0 });
    }
    logs.forEach(function (l) {
      if (l.kind !== 'memorisation') return;
      for (var k = 0; k < weeks.length; k++) {
        if (l.log_date >= weeks[k].start && l.log_date <= weeks[k].end) { weeks[k].v += l.to_ayah - l.from_ayah + 1; break; }
      }
    });
    return weeks;
  }

  function nextSession() {
    var tt = (DATA && DATA.timetable) || [];
    var now = lagosNow();
    var mins = now.getHours() * 60 + now.getMinutes();
    var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    var toMin = function (t) { var p = t.split(':'); return +p[0] * 60 + +p[1]; };
    for (var i = 0; i < 8; i++) {
      var day = (now.getDay() + i) % 7;
      var list = tt.filter(function (s) { return s.day === day && (i > 0 || toMin(s.end) > mins); })
        .sort(function (a, b) { return toMin(a.start) - toMin(b.start); });
      if (list.length) {
        var s = list[0];
        var when = i === 0 ? (toMin(s.start) <= mins ? 'Happening now' : 'Today') : i === 1 ? 'Tomorrow' : DAYS[day];
        return { when: when, s: s };
      }
    }
    return null;
  }
  var DAYNAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  var t12 = function (t) { var p = t.split(':'); var h = +p[0]; return (h % 12 || 12) + ':' + p[1] + (h < 12 ? ' AM' : ' PM'); };

  // ===================================================================== shared pieces
  function bar(value, label, cls) {
    var pct = Math.max(0, Math.min(100, Math.round(value * 1000) / 10));
    return html`<div class="pt-bar ${cls || ''}" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pct}" aria-label="${label}"><span style="width:${pct}%"></span></div>`;
  }
  function empty(title, text, action) {
    return html`<div class="pt-empty"><p class="pt-empty__t">${title}</p>${text ? html`<p>${text}</p>` : ''}${action || ''}</div>`;
  }
  function loading(label) {
    return html`<div class="pt-loading" role="status"><span class="pt-spin" aria-hidden="true"></span>${label || 'Loading…'}</div>`;
  }
  function errorBox(e, retry) {
    return html`<div class="pt-error" role="alert">${icon('alert')}<div><p><strong>That did not load.</strong> ${friendly(e)}</p>${retry ? html`<button type="button" class="btn btn--sm btn--line" data-retry>Try again</button>` : ''}</div></div>`;
  }
  function helpLink(text) {
    if (!DATA || !DATA.helpWa) return '';
    return html`<a class="pt-help" href="${DATA.helpWa}" target="_blank" rel="noopener">${icon('whatsapp')}${text || 'Message the Islamiyyah admin on WhatsApp'}<span class="sr-only"> (opens WhatsApp)</span></a>`;
  }
  function pill(text, kind) { return html`<span class="pt-pill${kind ? ' pt-pill--' + kind : ''}">${text}</span>`; }
  function statusPill(st) { return pill(STATUS[st] || st, st === 'active' ? 'green' : st === 'pending' ? 'yellow' : 'grey'); }

  function weeklyChart(weeks) {
    var max = Math.max.apply(null, weeks.map(function (w) { return w.v; }).concat([1]));
    var step = max <= 10 ? 5 : max <= 50 ? 10 : max <= 200 ? 50 : 100;
    var top = Math.ceil(max / step) * step;
    var W = 600, H = 240, padL = 46, padB = 40, padT = 14, gw = (W - padL) / weeks.length, bw = Math.min(30, gw - 8);
    var y = function (v) { return padT + (H - padT - padB) * (1 - v / top); };
    var grid = [], g;
    for (g = 0; g <= top; g += step) {
      grid.push('<line x1="' + padL + '" x2="' + W + '" y1="' + y(g) + '" y2="' + y(g) + '" class="pt-chart__grid"/>' +
        '<text x="' + (padL - 8) + '" y="' + (y(g) + 7) + '" class="pt-chart__tick" text-anchor="end">' + g + '</text>');
    }
    var bars = weeks.map(function (w, i) {
      var x = padL + i * gw + (gw - bw) / 2, h = Math.max(0, y(0) - y(w.v)), r = Math.min(4, h / 2);
      var label = 'Week of ' + fmtDate(w.start, false) + ': ' + plural(w.v, 'ayah') + ' memorised';
      var d = h > 0 ? 'M' + x + ',' + y(0) + 'V' + (y(w.v) + r) + 'q0,-' + r + ' ' + r + ',-' + r + 'H' + (x + bw - r) + 'q' + r + ',0 ' + r + ',' + r + 'V' + y(0) + 'Z' : '';
      var lab = (i % 3 === 2 || weeks.length < 8) ? '<text x="' + (x + bw / 2) + '" y="' + (H - 10) + '" class="pt-chart__tick" text-anchor="middle">' + esc(fmtDate(w.start, false).replace(/^\w+ /, '')) + '</text>' : '';
      return '<g class="pt-chart__col" tabindex="0" role="img" aria-label="' + esc(label) + '" data-tip="' + esc(label) + '">' +
        '<rect x="' + (padL + i * gw) + '" y="' + padT + '" width="' + gw + '" height="' + (H - padT - padB) + '" class="pt-chart__hit"/>' +
        (d ? '<path d="' + d + '" class="pt-chart__bar"/>' : '') + lab + '</g>';
    }).join('');
    var rows = weeks.map(function (w) { return html`<tr><td>${fmtDate(w.start, false)}</td><td>${fmtNum(w.v)}</td></tr>`; });
    return html`<figure class="pt-chart">
      <figcaption>Ayahs recorded as memorised each week, last 12 weeks</figcaption>
      <div class="pt-chart__wrap"><svg viewBox="0 0 ${W} ${H}" role="group" aria-label="Weekly memorisation chart">${raw(grid.join('') + bars)}</svg><div class="pt-chart__tip" hidden></div></div>
      <details class="pt-chart__table"><summary>Show as a table</summary>
        <table class="pt-table pt-table--plain"><thead><tr><th scope="col">Week starting</th><th scope="col">Ayahs memorised</th></tr></thead><tbody>${rows}</tbody></table>
      </details>
    </figure>`;
  }
  function wireChart(el) {
    $$('.pt-chart', el).forEach(function (fig) {
      var tip = $('.pt-chart__tip', fig), wrap = $('.pt-chart__wrap', fig);
      var show = function (g) {
        tip.textContent = g.dataset.tip; tip.hidden = false;
        var r = g.getBoundingClientRect(), w = wrap.getBoundingClientRect();
        var left = Math.max(0, Math.min(w.width - tip.offsetWidth, r.left - w.left + r.width / 2 - tip.offsetWidth / 2));
        tip.style.left = left + 'px'; tip.style.top = '0px';
        $$('.pt-chart__col', fig).forEach(function (c) { c.classList.toggle('is-on', c === g); });
      };
      var hide = function () { tip.hidden = true; $$('.pt-chart__col', fig).forEach(function (c) { c.classList.remove('is-on'); }); };
      $$('.pt-chart__col', fig).forEach(function (g) {
        g.addEventListener('mouseenter', function () { show(g); });
        g.addEventListener('focus', function () { show(g); });
        g.addEventListener('click', function () { show(g); });
        g.addEventListener('mouseleave', hide);
        g.addEventListener('blur', hide);
      });
    });
  }

  function quranSummary(pr, level, latestAssessment) {
    return html`<div class="pt-stats">
      <div class="pt-stat"><span class="pt-stat__k">Memorised</span><span class="pt-stat__v">${(pr.pct * 100).toFixed(pr.pct > 0 && pr.pct < 0.01 ? 2 : 1)}%</span><span class="pt-stat__s">${fmtNum(pr.memorised)} of ${fmtNum(TOTAL)} ayahs</span></div>
      <div class="pt-stat"><span class="pt-stat__k">About</span><span class="pt-stat__v">${pr.juzEquiv.toFixed(1)}</span><span class="pt-stat__s">juz memorised${pr.juzDone ? html` (${pr.juzDone} complete)` : ''}</span></div>
      <div class="pt-stat"><span class="pt-stat__k">Verified by a teacher</span><span class="pt-stat__v">${fmtNum(pr.verified)}</span><span class="pt-stat__s">ayahs</span></div>
      <div class="pt-stat"><span class="pt-stat__k">Revision, last 30 days</span><span class="pt-stat__v">${fmtNum(pr.revision30)}</span><span class="pt-stat__s">ayahs</span></div>
    </div>
    <div class="pt-overall">
      <div class="pt-overall__row"><span>Overall progress</span><span>${(pr.pct * 100).toFixed(1)}%</span></div>
      ${bar(pr.pct, 'Overall Qur’an memorisation progress')}
      <p class="pt-meta">Qur’an level: <strong>${level ? QLEVEL[level] : 'Not assigned yet'}</strong> · Last record: <strong>${pr.lastDate ? fmtDate(pr.lastDate) : 'None yet'}</strong> · Latest assessment: <strong>${latestAssessment ? fmtDate(latestAssessment.assessed_on) : 'None yet'}</strong></p>
    </div>`;
  }
  function juzGrid(pr) {
    return html`<div class="pt-juz" role="list" aria-label="Progress by juz">${pr.juz.map(function (v, i) {
      var pct = Math.round(v * 100);
      return html`<div class="pt-juz__cell${raw(pct >= 100 ? ' is-done' : pct > 0 ? ' is-part' : '')}" role="listitem" aria-label="Juz ${i + 1}: ${pct}% memorised"><span class="pt-juz__n" aria-hidden="true">${i + 1}</span><span class="pt-juz__fill" style="height:${pct}%" aria-hidden="true"></span></div>`;
    })}</div>
    <p class="pt-legend"><span class="pt-legend__sw is-done"></span>Complete <span class="pt-legend__sw is-part"></span>Started <span class="pt-legend__sw"></span>Not started</p>`;
  }
  function surahOptions(sel) {
    return SURAHS.map(function (s) { return html`<option value="${s[0]}"${raw(s[0] === sel ? ' selected' : '')}>${s[0]}. ${s[1]} (${s[4]} ayahs)</option>`; });
  }
  function logForm(id, staff) {
    var s = 114;
    return html`<form class="form form--plain pt-form" id="${id}" novalidate>
      <div class="field--2">
        <div class="field"><label for="${id}-kind">Type</label><select id="${id}-kind" name="kind" required>${opts(KIND, 'memorisation')}</select></div>
        <div class="field"><label for="${id}-date">Date</label><input id="${id}-date" name="log_date" type="date" required value="${todayISO()}" max="${todayISO()}"></div>
      </div>
      <div class="field"><label for="${id}-surah">Surah</label><select id="${id}-surah" name="surah" required data-surah>${surahOptions(s)}</select></div>
      <div class="field--2">
        <div class="field"><label for="${id}-from">From ayah</label><input id="${id}-from" name="from_ayah" type="number" inputmode="numeric" min="1" max="${surah(s)[4]}" value="1" required></div>
        <div class="field"><label for="${id}-to">To ayah</label><input id="${id}-to" name="to_ayah" type="number" inputmode="numeric" min="1" max="${surah(s)[4]}" value="${surah(s)[4]}" required></div>
      </div>
      <div class="field"><label for="${id}-note">Note <span class="opt">(optional)</span></label><textarea id="${id}-note" name="note" maxlength="500" rows="2" placeholder="${staff ? 'For example: strong recitation, revise the madd rules' : 'For example: revised with my study partner'}"></textarea></div>
      <p class="form-error" role="alert" tabindex="-1" hidden></p>
      <button class="btn btn--blue" type="submit">${staff ? 'Save verified record' : 'Save record'}</button>
    </form>`;
  }
  function wireLogForm(form) {
    var sel = $('[data-surah]', form), from = $('[name=from_ayah]', form), to = $('[name=to_ayah]', form);
    sel.addEventListener('change', function () {
      var n = surah(+sel.value)[4];
      from.max = to.max = n; from.value = 1; to.value = n;
    });
  }
  function readLog(v) {
    var s = surah(+v.surah), f = parseInt(v.from_ayah, 10), t = parseInt(v.to_ayah, 10);
    if (!s) throw new Error('Choose a surah.');
    if (!(f >= 1) || !(t >= 1)) throw new Error('Enter the ayah numbers.');
    if (f > t) throw new Error('“From ayah” must be the same as or before “to ayah”.');
    if (t > s[4]) throw new Error(s[1] + ' has ' + s[4] + ' ayahs.');
    if (!v.log_date || v.log_date > todayISO()) throw new Error('Choose a date that is not in the future.');
    return { kind: v.kind, surah: s[0], from_ayah: f, to_ayah: t, log_date: v.log_date, note: v.note || null };
  }
  function logList(logs, opts2) {
    opts2 = opts2 || {};
    if (!logs.length) return empty('No records yet', opts2.emptyText || 'Records you save will appear here.');
    var limit = opts2.limit || 25;
    var items = logs.map(function (l, i) {
      var canDelete = opts2.staff || (l.student_id === S.me.id && !l.verified);
      return html`<li class="pt-log${raw(i >= limit ? ' is-more' : '')}"${raw(i >= limit ? ' hidden' : '')}>
        <div class="pt-log__main">
          <span class="pt-log__date">${fmtDate(l.log_date)}</span>
          <strong>${rangeText(l)}</strong>
          <span class="pt-log__tags">${pill(KIND[l.kind].split(' (')[0], l.kind === 'memorisation' ? 'blue' : 'mist')} ${l.verified ? pill('Verified by teacher', 'green') : pill('Self-recorded', 'grey')}</span>
          ${l.note ? html`<p class="pt-log__note">${l.note}</p>` : ''}
        </div>
        <div class="pt-log__act">
          ${opts2.staff && !l.verified ? html`<button type="button" class="btn btn--sm btn--blue" data-verify="${l.id}">${icon('check')}Verify</button>` : ''}
          ${canDelete ? html`<button type="button" class="pt-iconbtn" data-del-log="${l.id}" aria-label="Delete the record for ${rangeText(l)} on ${fmtDate(l.log_date)}">${icon('trash')}</button>` : ''}
        </div>
      </li>`;
    });
    return html`<ul class="pt-logs">${items}</ul>${logs.length > limit ? html`<button type="button" class="btn btn--sm btn--line" data-more>Show all ${logs.length} records</button>` : ''}`;
  }
  function wireLogList(el, reload) {
    var more = $('[data-more]', el);
    if (more) more.addEventListener('click', function () { $$('.pt-log.is-more', el).forEach(function (li) { li.hidden = false; }); more.remove(); });
    $$('[data-del-log]', el).forEach(function (b) {
      b.addEventListener('click', async function () {
        if (b.dataset.confirm !== '1') { b.dataset.confirm = '1'; b.classList.add('is-confirm'); b.setAttribute('aria-label', 'Press again to delete'); b.title = 'Press again to delete'; toast('Press the delete button again to confirm.'); return; }
        b.disabled = true;
        try {
          var rows = await run(S.sb.from('quran_logs').delete().eq('id', b.dataset.delLog).select('id'));
          if (!rows.length) throw new Error('That record could not be deleted.');
          toast('Record deleted.'); reload();
        } catch (e) { b.disabled = false; toast(friendly(e), 'error'); }
      });
    });
    $$('[data-verify]', el).forEach(function (b) {
      b.addEventListener('click', async function () {
        busy(b, true, 'Verifying…');
        try {
          var rows = await run(S.sb.from('quran_logs').update({ verified: true }).eq('id', b.dataset.verify).select('id'));
          if (!rows.length) throw new Error('That record could not be verified.');
          toast('Record verified.'); reload();
        } catch (e) { busy(b, false); toast(friendly(e), 'error'); }
      });
    });
  }
  function assessmentList(list, canDelete) {
    if (!list.length) return empty('No assessments yet', 'Your teachers’ assessments and comments will appear here.');
    return html`<ul class="pt-feedback">${list.map(function (a) {
      return html`<li class="pt-fb">
        <div class="pt-fb__head"><strong>${a.title}</strong>${a.score !== null && a.score !== undefined ? html`<span class="pt-fb__score">${Number(a.score)}%</span>` : ''}</div>
        <p class="pt-meta">${TRACK[a.track]} · ${fmtDate(a.assessed_on)}${a.teacher_name ? html` · ${a.teacher_name}` : ''}</p>
        ${a.comment ? html`<p class="pt-fb__c">${a.comment}</p>` : ''}
        ${canDelete && (isAdmin() || a.teacher_id === S.me.id) ? html`<button type="button" class="pt-textbtn" data-del-assess="${a.id}">Delete</button>` : ''}
      </li>`;
    })}</ul>`;
  }
  function noticeList(list, manage) {
    if (!list.length) return empty('No announcements', 'Notices from the Islamiyyah committee and your teachers will appear here.');
    return html`<ul class="pt-notices">${list.map(function (n) {
      return html`<li class="pt-notice${raw(n.pinned ? ' is-pinned' : '')}">
        <div class="pt-notice__head"><strong>${n.title}</strong>${n.pinned ? pill('Pinned', 'yellow') : ''}</div>
        <p class="pt-notice__body">${n.body}</p>
        <p class="pt-meta">${n.author_name || 'Islamiyyah committee'} · ${fmtDate(n.created_at)}${manage ? html` · For: ${n.audience === 'group' ? (manage.groups[n.group_id] || 'a group') : AUDIENCE[n.audience]}` : ''}</p>
        ${manage && (isAdmin() || n.author_id === S.me.id) ? html`<button type="button" class="pt-textbtn" data-del-notice="${n.id}">Delete</button>` : ''}
      </li>`;
    })}</ul>`;
  }

  // ===================================================================== rendering frame
  function setRoot(content) { root.innerHTML = out(content); root.setAttribute('aria-busy', 'false'); }
  function authFrame(title, lede, body) {
    setRoot(html`<div class="pt-auth">
      <div class="pt-auth__card">
        <p class="pt-auth__kicker">AMSC Student Portal</p>
        <h2 id="pt-h" tabindex="-1">${title}</h2>
        ${lede ? html`<p class="pt-auth__lede">${lede}</p>` : ''}
        ${body}
      </div>
    </div>`);
    var h = $('#pt-h'); if (h && S.focusNext) h.focus();
    S.focusNext = true;
  }
  // ------------------------------------------------------------------ who sees what
  // Each person sees only their own workspace: an Islamiyyah student, teacher or admin, and/or a
  // Dawrah student or admin. People in both programmes switch between them at the top.
  var inIslamiyyah = function () { return !!(S.me && S.me.status === 'active'); };
  var dawrahAccess = function () { var d = S.dawrah; return !!(d && d.term && (d.student || d.admin)); };
  var dawrahOnly = function () { return dawrahAccess() && !inIslamiyyah(); };
  function homeHash() {
    if (inIslamiyyah()) return isAdmin() ? '#/admin' : isStaff() ? '#/teach' : '#/dashboard';
    return dawrahAccess() ? '#/dawrah' : '#/dashboard';
  }
  function tabsFor(prog) {
    if (prog === 'dawrah') {
      if (!S.dawrah.admin) return [];
      return [['dawrah', 'Students'], ['dawrah/classes', 'Classes'], ['dawrah/exam-setup', 'Exam'], ['dawrah/settings', 'Settings']]
        .concat(S.dawrah.student ? [['dawrah/mine', 'My classes']] : []);
    }
    if (isAdmin()) return [['admin', 'Overview'], ['members', 'Members'], ['groups', 'Groups'], ['notices', 'Notices'], ['library', 'Library']]
      .concat(S.teaches ? [['teach', 'My teaching']] : []);
    if (isStaff()) return [['teach', 'My students'], ['notices', 'Notices'], ['library', 'Library']];
    return [['dashboard', 'Home'], ['quran', 'Qur’an'], ['arabic', 'Arabic'], ['classes', 'My class'], ['library', 'Library']];
  }
  function roleLabel(prog) {
    if (prog === 'dawrah') return S.dawrah.admin ? 'Dawrah admin' : 'Dawrah student';
    var r = { student: 'Islamiyyah student', teacher: 'Islamiyyah teacher', admin: 'Islamiyyah admin' }[S.me.role];
    return r + (S.me.role === 'student' && S.me.wing ? ' · ' + WING[S.me.wing] : '');
  }
  // prog: 'islamiyyah' or 'dawrah'; cur: the tab to mark ('' for none, such as the profile page).
  function shell(prog, cur) {
    var tabs = tabsFor(prog), both = inIslamiyyah() && dawrahAccess();
    var islHome = homeHash().slice(2);
    setRoot(html`<div class="pt-shell">
      <div class="pt-top">
        <div class="pt-who"><span class="pt-mono" aria-hidden="true">${initials(S.me.full_name)}</span>
          <div><strong>${S.me.full_name}</strong><span>${roleLabel(prog)}</span></div></div>
        <div class="pt-top__act">
          <a class="btn btn--sm btn--line" href="#/profile"${raw(cur === 'profile' ? ' aria-current="page"' : '')}>Profile</a>
          <button type="button" class="btn btn--sm btn--line" data-logout>Log out</button>
        </div>
      </div>
      ${both ? html`<nav class="pt-prog" aria-label="Programme"><a href="#/${islHome}"${raw(prog === 'islamiyyah' ? ' aria-current="page"' : '')}>Islamiyyah</a><a href="#/dawrah"${raw(prog === 'dawrah' ? ' aria-current="page"' : '')}>Dawrah</a></nav>` : ''}
      ${tabs.length ? html`<nav class="pt-tabs" aria-label="${prog === 'dawrah' ? 'Dawrah' : 'Islamiyyah'} sections"><ul>${tabs.map(function (t) {
        return html`<li><a href="#/${t[0]}"${raw(t[0] === cur ? ' aria-current="page"' : '')}>${t[1]}</a></li>`;
      })}</ul></nav>` : ''}
      <div class="pt-view" id="pt-view"></div>
    </div>`);
    var hdr = document.querySelector('.site-header');
    if (hdr) document.documentElement.style.setProperty('--pt-head', hdr.offsetHeight + 'px');
    var cur_ = $('.pt-tabs [aria-current]');
    if (cur_) { var nav = $('.pt-tabs ul'); nav.scrollLeft = cur_.offsetLeft - 16; }
    return $('#pt-view');
  }
  function view(el, content, focus) {
    el.innerHTML = out(content);
    if (focus !== false) { var h = $('h2', el); if (h && S.focusNext) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); } }
    S.focusNext = true;
    var r = $('[data-retry]', el); if (r) r.addEventListener('click', route);
  }
  function subnav(base, items, cur, label) {
    return html`<nav class="pt-subnav" aria-label="${label}"><ul>${items.map(function (i) {
      return html`<li><a href="#/${base}${i[0] ? '/' + i[0] : ''}"${raw(i[0] === cur ? ' aria-current="page"' : '')}>${i[1]}</a></li>`;
    })}</ul></nav>`;
  }

  // ===================================================================== router
  var STUDENT_VIEWS = ['dashboard', 'quran', 'arabic', 'classes'];
  var STAFF_VIEWS = ['teach', 'student', 'notices'];
  var ADMIN_VIEWS = ['admin', 'members', 'member', 'groups'];
  async function route() {
    var h = location.hash || '';
    if (h && h.indexOf('#/') !== 0) return;              // a sign-in link fragment being read
    var parts = h.replace(/^#\/?/, '').split(/[?#]/)[0].split('/').filter(Boolean);
    var name = parts[0] || '';
    if (!S.sb) return;
    if (!S.user) {
      if (name === 'signup') return viewSignup(parts[1]);
      if (name === 'forgot') return viewForgot();
      return viewLogin();
    }
    if (S.recovery) return viewSetPassword('reset');
    if (!S.me) return viewNoProfile();
    if (S.me.must_change_password) return viewSetPassword('forced');
    if (S.me.status === 'inactive' && !dawrahAccess()) return viewInactive();
    if (!inIslamiyyah() && !dawrahAccess()) return viewPending();

    var el;
    if (name === 'profile') {
      var prog = S.prog === 'dawrah' && dawrahAccess() ? 'dawrah' : inIslamiyyah() ? 'islamiyyah' : 'dawrah';
      el = shell(prog, 'profile');
      try { viewProfile(el); } catch (e) { view(el, errorBox(e, true)); }
      return;
    }
    if (name === 'dawrah') {
      if (!dawrahAccess()) return go(homeHash());
      S.prog = 'dawrah';
      var sub = parts[1] || '', d = S.dawrah;
      var cur = !d.admin ? '' : sub === '' || sub === 'student' ? 'dawrah'
        : sub === 'classes' || sub === 'new' || sub === 'edit' || (sub === 'class' && !d.student) ? 'dawrah/classes'
        : sub === 'exam-setup' ? 'dawrah/exam-setup' : sub === 'settings' ? 'dawrah/settings' : 'dawrah/mine';
      el = shell('dawrah', cur);
      try { await viewDawrah(el, parts.slice(1)); } catch (e) { view(el, errorBox(e, true)); }
      return;
    }
    // Islamiyyah
    if (!inIslamiyyah()) return go('#/dawrah');
    var views = {
      dashboard: viewDashboard, quran: viewQuran, arabic: viewArabic, classes: viewClasses, library: viewLibrary,
      teach: viewTeach, student: viewStudent, notices: viewNotices,
      admin: viewAdmin, members: viewMembers, member: viewMember, groups: viewGroups
    };
    var ok = views[name] &&
      (STUDENT_VIEWS.indexOf(name) < 0 || S.me.role === 'student') &&
      (STAFF_VIEWS.indexOf(name) < 0 || isStaff()) &&
      (ADMIN_VIEWS.indexOf(name) < 0 || isAdmin());
    if (!ok) return go(homeHash());
    S.prog = 'islamiyyah';
    var tab = name === 'member' ? 'members'
      : name === 'student' ? (isAdmin() && h.indexOf('from=admin') > 0 ? 'members' : 'teach') : name;
    el = shell('islamiyyah', tab);
    try { await views[name](el, parts.slice(1)); } catch (e) { view(el, errorBox(e, true)); }
  }

  root.addEventListener('click', async function (ev) {
    var b = ev.target.closest('[data-logout]');
    if (!b) return;
    busy(b, true, 'Logging out…');
    try { await S.sb.auth.signOut(); } catch (e) { /* signed out locally anyway */ }
    S.user = null; S.me = null; S.dawrah = null; S.recovery = false;
    go('#/login');
  });

  async function loadMe() {
    S.me = await run(S.sb.from('profiles').select('*').eq('id', S.user.id).maybeSingle());
    // Dawrah access; if the Dawrah part of the database is not set up yet, carry on without it.
    try { S.dawrah = S.me ? await run(S.sb.rpc('dawrah_me')) : null; } catch (e) { S.dawrah = null; }
    S.teaches = 0;
    if (isStaff()) { try { S.teaches = await count(S.sb.from('group_teachers').select('group_id', { count: 'exact', head: true }).eq('teacher_id', S.me.id)); } catch (e) { S.teaches = 0; } }
    return S.me;
  }

  // ===================================================================== sign-in screens
  function passwordField(id, label, name, auto, minlen) {
    return html`<div class="field"><label for="${id}">${label}</label>
      <div class="pt-pw"><input id="${id}" name="${name}" type="password" autocomplete="${auto}" required${raw(minlen ? ' minlength="' + minlen + '"' : '')}>
      <button type="button" class="pt-pw__toggle" data-pw="${id}" aria-pressed="false">Show<span class="sr-only"> password</span></button></div></div>`;
  }
  function wirePw(el) {
    $$('[data-pw]', el).forEach(function (b) {
      b.addEventListener('click', function () {
        var inp = document.getElementById(b.dataset.pw), show = inp.type === 'password';
        inp.type = show ? 'text' : 'password';
        b.setAttribute('aria-pressed', String(show));
        b.firstChild.textContent = show ? 'Hide' : 'Show';
      });
    });
  }

  function viewLogin() {
    authFrame('Log in', 'For Islamiyyah and Dawrah students, teachers and admins.', html`
      <form class="form form--plain pt-form" id="f-login" novalidate>
        <div class="field"><label for="li-email">Email</label><input id="li-email" name="email" type="email" autocomplete="email" required></div>
        ${passwordField('li-pw', 'Password', 'password', 'current-password')}
        <p class="form-error" role="alert" tabindex="-1" hidden></p>
        <button class="btn btn--blue pt-wide" type="submit">Log in</button>
      </form>
      <p class="pt-auth__links"><a href="#/forgot">Forgot your password?</a></p>
      <div class="pt-auth__alt"><p>New to the portal?</p><a class="btn btn--line pt-wide" href="#/signup">Create a student account</a></div>`);
    var f = $('#f-login'); wirePw(f);
    onSubmit(f, async function (v) {
      if (!v.email || !v.password) throw new Error('Enter your email and password.');
      var d = await run(S.sb.auth.signInWithPassword({ email: v.email, password: v.password }));
      S.user = d.user;
      await loadMe();
      go(homeHash());
    });
  }

  function viewSignup(preset) {
    var pre = preset === 'dawrah' ? 'dawrah' : preset === 'islamiyyah' ? 'islamiyyah' : '';
    var ck = function (v) { return raw(pre === v ? ' checked' : ''); };
    authFrame('Create your account', 'One account for the AMSC Islamiyyah and the Dawrah.', html`
      <form class="form form--plain pt-form" id="f-signup" novalidate>
        <fieldset class="field pt-choice pt-choice--list"><legend>What are you signing up for?</legend>
          <label><input type="radio" name="programme" value="islamiyyah" required${ck('islamiyyah')}> Islamiyyah classes <span class="pt-meta">(weekends)</span></label>
          <label><input type="radio" name="programme" value="dawrah"${ck('dawrah')}> Dawrah <span class="pt-meta">(${DW.title || 'Dawratul-Hadith'})</span></label>
          <label><input type="radio" name="programme" value="both"> Both</label>
        </fieldset>
        <div class="field"><label for="su-name">Full name</label><input id="su-name" name="full_name" autocomplete="name" required minlength="2" maxlength="120"></div>
        <div class="field"><label for="su-email">Email</label><input id="su-email" name="email" type="email" autocomplete="email" required aria-describedby="su-email-h">
          <p class="pt-meta" id="su-email-h">For the Dawrah, use the same email you put on the registration form.</p></div>
        <fieldset class="field pt-choice"><legend>Are you a brother or a sister?</legend>
          <label><input type="radio" name="wing" value="brothers" required> Brother</label>
          <label><input type="radio" name="wing" value="sisters"> Sister</label>
        </fieldset>
        <div class="field"><label for="su-phone">WhatsApp number <span class="opt">(optional)</span></label><input id="su-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel" maxlength="20" placeholder="0803 000 0000"></div>
        <div class="field--2">
          <div class="field"><label for="su-dept">Department <span class="opt">(optional)</span></label><input id="su-dept" name="department" maxlength="120"></div>
          <div class="field"><label for="su-level">Level <span class="opt">(optional)</span></label><select id="su-level" name="level"><option value="">Choose</option>${STUDY_LEVELS.map(function (l) { return html`<option>${l}</option>`; })}</select></div>
        </div>
        ${passwordField('su-pw', 'Password (at least 8 characters)', 'password', 'new-password', 8)}
        ${passwordField('su-pw2', 'Confirm password', 'password2', 'new-password', 8)}
        <label class="pt-consent"><input type="checkbox" name="consent" value="yes" required>
          <span>I agree that AMSC may keep my details and learning records to run its programmes. Only I, my teachers and the portal admins can see them, and I can ask for my account to be deleted at any time.</span></label>
        <p class="form-error" role="alert" tabindex="-1" hidden></p>
        <button class="btn btn--blue pt-wide" type="submit">Create account</button>
      </form>
      <p class="pt-auth__links">Already have an account? <a href="#/login">Log in</a></p>`);
    var f = $('#f-signup'); wirePw(f);
    onSubmit(f, async function (v) {
      if (['islamiyyah', 'dawrah', 'both'].indexOf(v.programme) < 0) throw new Error('Choose what you are signing up for.');
      if (!v.full_name || v.full_name.length < 2) throw new Error('Enter your full name.');
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email || '')) throw new Error('Enter a valid email address.');
      if (v.wing !== 'brothers' && v.wing !== 'sisters') throw new Error('Choose brother or sister.');
      if ((v.password || '').length < 8) throw new Error('Your password must be at least 8 characters.');
      if (v.password !== v.password2) throw new Error('The two passwords do not match.');
      if (v.consent !== 'yes') throw new Error('Tick the box to agree to how your details are used.');
      var d = await run(S.sb.auth.signUp({
        email: v.email, password: v.password,
        options: { data: { portal: 'islamiyyah', programme: v.programme, full_name: v.full_name, wing: v.wing, phone: v.phone || '', department: v.department || '', level: v.level || '', consent: true } }
      }));
      if (d.user && d.user.identities && d.user.identities.length === 0) throw new Error('An account with this email already exists. Log in instead.');
      if (!d.session) {
        authFrame('Check your email', null, html`<p>We sent a confirmation link to <strong>${v.email}</strong>. Open it, then come back and log in.</p><a class="btn btn--blue pt-wide" href="#/login">Go to log in</a>`);
        return;
      }
      S.user = d.user;
      await loadMe();
      go(homeHash());
    });
  }

  function viewForgot() {
    var emailOn = !!CFG.emailReset;
    authFrame('Forgot your password?', emailOn ? 'Enter your email and we will send you a link to set a new password.' : 'The Islamiyyah admin can set a temporary password for you.', html`
      ${emailOn ? html`<form class="form form--plain pt-form" id="f-forgot" novalidate>
        <div class="field"><label for="fg-email">Email</label><input id="fg-email" name="email" type="email" autocomplete="email" required></div>
        <p class="form-error" role="alert" tabindex="-1" hidden></p>
        <button class="btn btn--blue pt-wide" type="submit">Send reset link</button>
      </form><p class="pt-or"><span>or</span></p>` : ''}
      <p>Message the admin on WhatsApp with your full name and the email you signed up with. You will get a temporary password, and the portal will ask you to choose a new one when you log in.</p>
      ${helpLink('Ask for a temporary password on WhatsApp')}
      <p class="pt-auth__links"><a href="#/login">Back to log in</a></p>`);
    var f = $('#f-forgot');
    onSubmit(f, async function (v) {
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email || '')) throw new Error('Enter a valid email address.');
      await run(S.sb.auth.resetPasswordForEmail(v.email, { redirectTo: location.origin + location.pathname }));
      f.outerHTML = html`<div class="pt-done" role="status">${icon('check')}<p>If an account uses <strong>${v.email}</strong>, a reset link is on its way. Check your inbox and spam folder.</p></div>`.s;
    });
  }

  function viewSetPassword(mode) {
    var forced = mode === 'forced';
    authFrame(forced ? 'Choose a new password' : 'Set a new password',
      forced ? 'You logged in with a temporary password. Choose your own password to continue.' : 'Choose a new password for your account.', html`
      <form class="form form--plain pt-form" id="f-newpw" novalidate>
        ${passwordField('np-pw', 'New password (at least 8 characters)', 'password', 'new-password', 8)}
        ${passwordField('np-pw2', 'Confirm new password', 'password2', 'new-password', 8)}
        <p class="form-error" role="alert" tabindex="-1" hidden></p>
        <button class="btn btn--blue pt-wide" type="submit">Save password</button>
      </form>
      <p class="pt-auth__links"><button type="button" class="pt-textbtn" data-logout>Log out</button></p>`);
    var f = $('#f-newpw'); wirePw(f);
    onSubmit(f, async function (v) {
      if ((v.password || '').length < 8) throw new Error('Your password must be at least 8 characters.');
      if (v.password !== v.password2) throw new Error('The two passwords do not match.');
      await run(S.sb.auth.updateUser({ password: v.password }));
      S.recovery = false;
      if (S.me && S.me.must_change_password) {
        await run(S.sb.from('profiles').update({ must_change_password: false }).eq('id', S.me.id).select('id'));
      }
      await loadMe();
      toast('Your new password is saved.');
      go(homeHash());
    });
  }

  function viewPending() {
    var m = S.me, dawrahSide = !m.joins_islamiyyah;
    authFrame(dawrahSide ? 'You are signed up for the Dawrah' : 'Your account is waiting for approval', null, html`
      ${dawrahSide
        ? html`<p>Jazakallahu khairan, ${firstName(m.full_name)}. Your Dawrah page opens as soon as the Dawrah team adds the registration list.</p>
            <p>Make sure <strong>${m.email}</strong> is the same email you put on the Dawrah registration form.</p>`
        : html`<p>Jazakallahu khairan for signing up, ${firstName(m.full_name)}. The Islamiyyah committee will approve your account and place you in your classes, usually at the next weekend class.</p>
            <p class="pt-meta">Also registered for the Dawrah? Your Dawrah page opens once the Dawrah team adds the registrations.</p>`}
      <dl class="pt-dl">
        <div><dt>Name</dt><dd>${m.full_name}</dd></div>
        <div><dt>Email</dt><dd>${m.email}</dd></div>
        <div><dt>Brother or sister</dt><dd>${m.wing === 'sisters' ? 'Sister' : m.wing === 'brothers' ? 'Brother' : 'Not chosen'}</dd></div>
      </dl>
      <button type="button" class="btn btn--blue pt-wide" data-refresh>Check again</button>
      ${dawrahSide ? dwHelp() : helpLink('Ask the admin to approve you on WhatsApp')}
      ${dawrahSide ? html`<p class="pt-auth__links"><button type="button" class="pt-textbtn" data-join>I also want to join the Islamiyyah classes</button></p>` : ''}
      <p class="pt-auth__links"><button type="button" class="pt-textbtn" data-logout>Log out</button></p>`);
    $('[data-refresh]').addEventListener('click', async function (ev) {
      busy(ev.currentTarget, true, 'Checking…');
      try {
        await loadMe();
        if (S.me && !inIslamiyyah() && !dawrahAccess()) { busy(ev.currentTarget, false); toast('Not open yet. Please check again later.'); }
        else go(homeHash());
      } catch (e) { busy(ev.currentTarget, false); toast(friendly(e), 'error'); }
    });
    var j = $('[data-join]');
    if (j) j.addEventListener('click', async function () {
      busy(j, true, 'Sending…');
      try {
        var rows = await run(S.sb.from('profiles').update({ joins_islamiyyah: true }).eq('id', S.me.id).select('*'));
        S.me = rows[0]; toast('Done. The Islamiyyah committee will review your sign-up.'); route();
      } catch (e) { busy(j, false); toast(friendly(e), 'error'); }
    });
  }
  function viewInactive() {
    authFrame('Your account is inactive', 'Contact the Islamiyyah admin if you think this is a mistake.', html`
      ${helpLink()}<p class="pt-auth__links"><button type="button" class="pt-textbtn" data-logout>Log out</button></p>`);
  }
  function viewNoProfile() {
    authFrame('We could not find your portal profile', 'Your login works, but your student record is missing. The Islamiyyah admin can fix this.', html`
      ${helpLink()}<p class="pt-auth__links"><button type="button" class="pt-textbtn" data-logout>Log out</button></p>`);
  }
  function viewNotReady() {
    root.innerHTML = out(html`<div class="pt-auth"><div class="pt-auth__card">
      <p class="pt-auth__kicker">AMSC Student Portal</p>
      <h2>The portal is opening soon</h2>
      <p class="pt-auth__lede">The Islamiyyah committee is setting up student accounts. In the meantime, classes run every Saturday and Sunday at the AFIT Mosque.</p>
      <a class="btn btn--blue pt-wide" href="islamiyyah.html">About the Islamiyyah programme</a>
      ${helpLink('Ask the Islamiyyah admin a question')}
    </div></div>`);
    root.setAttribute('aria-busy', 'false');
  }

  // ===================================================================== student: home
  async function myGroups() {
    var ids = [S.me.quran_group, S.me.arabic_group].filter(Boolean);
    if (!ids.length) return {};
    var gs = await run(S.sb.from('groups').select('*').in('id', ids));
    var m = {}; gs.forEach(function (g) { m[g.id] = g; }); return m;
  }
  // Arabic class progress, recorded by the class's teacher as lessons completed in the textbook.
  function arabicProgress(g) {
    if (!g) return empty('Not placed in an Arabic class yet', 'The Islamiyyah committee will place you after your level check.');
    if (g.current_lesson == null) return html`<p>Your teacher will record your class’s progress here.</p>`;
    var tot = g.total_lessons, cur = g.current_lesson;
    return html`<div class="pt-hero"><span class="pt-hero__v">${cur}${tot ? html`<small>/${tot}</small>` : ''}</span><span class="pt-hero__s">${plural(cur, 'lesson')} completed${g.book ? ' · ' + g.book : ''}</span></div>
      ${tot ? bar(cur / tot, 'Arabic class progress') : ''}
      <p class="pt-meta">Updated by your teacher on ${fmtDate(g.progress_at)}</p>`;
  }

  async function viewDashboard(el) {
    var mine = token();
    view(el, loading('Loading…'), false);
    var res = await Promise.all([
      myGroups(),
      run(S.sb.from('announcements').select('*').order('pinned', { ascending: false }).order('created_at', { ascending: false }).limit(4)),
      run(S.sb.from('quran_logs').select('kind,surah,from_ayah,to_ayah,log_date,verified').eq('student_id', S.me.id).limit(3000))
    ]);
    if (!mine()) return;
    var groups = res[0], notices = res[1], pr = progress(res[2]), nx = nextSession();
    var ag = S.me.arabic_group && groups[S.me.arabic_group];
    view(el, html`
      <h2 class="pt-h">Assalamu alaykum, ${firstName(S.me.full_name)}</h2>
      <section class="pt-card pt-card--blue" aria-labelledby="d-next">
        <h3 id="d-next">${icon('clock')}Next class</h3>
        ${nx ? html`<p class="pt-next__when">${nx.when}, ${t12(nx.s.start)} to ${t12(nx.s.end)}</p><p class="pt-next__what">${nx.s.title}</p><p class="pt-next__where">${DATA.venue}</p>` : html`<p>No classes scheduled.</p>`}
        <a class="pt-cardlink" href="#/classes">Timetable, teachers and classmates</a>
      </section>
      <div class="pt-grid">
        <section class="pt-card" aria-labelledby="d-q">
          <h3 id="d-q">${icon('quran')}Qur’an</h3>
          <div class="pt-hero"><span class="pt-hero__v">${(pr.pct * 100).toFixed(1)}%</span><span class="pt-hero__s">memorised · about ${pr.juzEquiv.toFixed(1)} juz</span></div>
          ${bar(pr.pct, 'Qur’an memorised')}
          <p class="pt-meta">Last record: ${pr.lastDate ? fmtDate(pr.lastDate) : 'none yet'}</p>
          <a class="pt-cardlink" href="#/quran">My Qur’an record</a>
        </section>
        <section class="pt-card" aria-labelledby="d-a">
          <h3 id="d-a">${icon('book')}Arabic</h3>
          ${arabicProgress(ag)}
          <a class="pt-cardlink" href="#/arabic">My Arabic studies</a>
        </section>
      </div>
      <section class="pt-card" aria-labelledby="d-notices">
        <h3 id="d-notices">${icon('bell')}Announcements</h3>
        ${noticeList(notices)}
      </section>`);
  }

  // ===================================================================== student: Qur'an
  async function viewQuran(el, args) {
    var tab = (args && args[0]) || '', mine = token();
    view(el, loading('Loading your Qur’an record…'), false);
    var res = await Promise.all([
      run(S.sb.from('quran_logs').select('*').eq('student_id', S.me.id).order('log_date', { ascending: false }).order('created_at', { ascending: false }).limit(3000)),
      run(S.sb.from('assessments').select('*').eq('student_id', S.me.id).eq('track', 'quran').order('assessed_on', { ascending: false }))
    ]);
    if (!mine()) return;
    var logs = res[0], qa = res[1], pr = progress(logs);
    var body;
    if (tab === 'history') body = html`<section class="pt-card" aria-labelledby="q-hist"><h3 id="q-hist">History</h3>
        ${logList(logs, { emptyText: 'Press “Record progress” to add what you memorised or revised.' })}</section>`;
    else if (tab === 'feedback') body = html`<section class="pt-card" aria-labelledby="q-fb"><h3 id="q-fb">${icon('star')}Teacher feedback</h3>${assessmentList(qa)}</section>`;
    else body = html`<div class="pt-grid">
        <section class="pt-card" aria-labelledby="q-juz"><h3 id="q-juz">Progress by juz</h3>${juzGrid(pr)}</section>
        <section class="pt-card" aria-labelledby="q-surahs"><h3 id="q-surahs">Surahs memorised</h3>
          ${pr.bySurah.length ? html`<ul class="pt-surahs">${pr.bySurah.map(function (x) {
            return html`<li><span class="pt-surahs__n">${x.n}. ${surahName(x.n)}</span><span class="pt-surahs__c">${x.done}/${x.total}</span>${bar(x.done / x.total, surahName(x.n) + ' progress', 'pt-bar--thin')}</li>`;
          })}</ul>` : empty('None yet', 'Surahs appear here as you record them.')}</section>
      </div>
      <section class="pt-card" aria-labelledby="q-chart"><h3 id="q-chart">Progress over time</h3>${weeklyChart(weekly(logs))}</section>`;
    view(el, html`
      <div class="pt-headrow"><h2 class="pt-h">My Qur’an</h2><button type="button" class="btn btn--sm btn--blue" data-add aria-expanded="false" aria-controls="q-add">${icon('plus')}Record progress</button></div>
      <section class="pt-card" id="q-add" hidden aria-labelledby="q-add-h">
        <h3 id="q-add-h">Record your progress</h3>
        <p class="pt-meta">Record what you memorised or revised. Your teacher verifies it at class.</p>
        ${logForm('f-log', false)}
      </section>
      <section class="pt-card" aria-label="Summary">${quranSummary(pr, S.me.quran_level, qa[0])}</section>
      ${subnav('quran', [['', 'Overview'], ['history', 'History (' + logs.length + ')'], ['feedback', 'Teacher feedback (' + qa.length + ')']], tab, 'Qur’an record')}
      ${body}`);
    var addBtn = $('[data-add]', el), panel = $('#q-add', el);
    addBtn.addEventListener('click', function () {
      panel.hidden = !panel.hidden; addBtn.setAttribute('aria-expanded', String(!panel.hidden));
      if (!panel.hidden) $('#f-log-kind', el).focus();
    });
    var f = $('#f-log', el); wireLogForm(f);
    onSubmit(f, async function (v) {
      var row = readLog(v); row.student_id = S.me.id; row.verified = false;
      await run(S.sb.from('quran_logs').insert(row));
      toast('Saved: ' + rangeText(row) + '.');
      S.focusNext = false; viewQuran(el, args);
    });
    wireLogList(el, function () { S.focusNext = false; viewQuran(el, args); });
    wireChart(el);
  }

  // ===================================================================== student: Arabic
  async function viewArabic(el) {
    var mine = token();
    view(el, loading('Loading your Arabic studies…'), false);
    var res = await Promise.all([
      myGroups(), run(S.sb.rpc('my_teachers')),
      run(S.sb.from('assessments').select('*').eq('student_id', S.me.id).eq('track', 'arabic').order('assessed_on', { ascending: false }))
    ]);
    if (!mine()) return;
    var g = S.me.arabic_group && res[0][S.me.arabic_group], aa = res[2];
    var ts = g ? (res[1] || []).filter(function (t) { return t.group_id === g.id; }).map(function (t) { return t.full_name; }) : [];
    var bk = DATA.arabicText;
    view(el, html`
      <h2 class="pt-h">My Arabic studies</h2>
      <section class="pt-card" aria-labelledby="ar-p">
        <h3 id="ar-p">${icon('star')}Class progress</h3>
        ${g ? html`<p class="pt-ar-class"><strong>${g.name}</strong> · ${LEVEL[S.me.arabic_level || g.level]} · ${ts.length ? 'Teacher: ' + ts.join(', ') : 'Teacher to be assigned'}</p>` : ''}
        ${arabicProgress(g)}
      </section>
      <div class="pt-grid">
        <section class="pt-card" aria-labelledby="ar-b">
          <h3 id="ar-b">${icon('book')}Textbook</h3>
          ${bk && bk.file ? html`<p><span lang="ar" dir="rtl" class="pt-ar">${bk.ar}</span><br>${bk.en}, Book 1${bk.pages ? ' · ' + bk.pages + ' pages' : ''}</p>
            <a class="btn btn--sm btn--blue" href="${bk.file}" download>${icon('download')}Download the PDF<span class="sr-only"> of ${bk.en}</span></a>` : html`<p>Your teacher will share the textbook.</p>`}
        </section>
        <section class="pt-card" aria-labelledby="ar-w">
          <h3 id="ar-w">${icon('calendar')}When</h3>
          ${DATA.timetable.filter(function (x) { return /arabic/i.test(x.title); }).map(function (x) {
            return html`<p><strong>${DAYNAMES[x.day]}s, ${t12(x.start)} to ${t12(x.end)}</strong></p>`;
          })}
          <p class="pt-meta">At the ${DATA.venue}, grouped by Arabic level.</p>
        </section>
      </div>
      <section class="pt-card" aria-labelledby="ar-fb">
        <h3 id="ar-fb">Teacher feedback</h3>
        ${assessmentList(aa)}
      </section>`);
  }

  // ===================================================================== library
  async function viewLibrary(el) {
    var mine = token();
    view(el, loading('Loading the library…'), false);
    var items = await run(S.sb.from('resources').select('*').order('created_at', { ascending: false }));
    if (!mine()) return;
    var staff = isStaff();
    view(el, html`
      <div class="pt-headrow"><h2 class="pt-h">Library</h2>${staff ? html`<button type="button" class="btn btn--sm btn--blue" data-add aria-expanded="false" aria-controls="lib-add">${icon('plus')}Add material</button>` : ''}</div>
      ${staff ? html`<section class="pt-card" id="lib-add" hidden aria-labelledby="lib-add-h">
        <h3 id="lib-add-h">Add material</h3>
        <form class="form form--plain pt-form" id="f-res" novalidate>
          <div class="field"><label for="r-title">Title</label><input id="r-title" name="title" required maxlength="160"></div>
          <div class="field--2">
            <div class="field"><label for="r-author">Author <span class="opt">(optional)</span></label><input id="r-author" name="author" maxlength="120"></div>
            <div class="field"><label for="r-subject">Subject</label><select id="r-subject" name="subject" required>${opts(SUBJECT, 'quran')}</select></div>
          </div>
          <div class="field"><label for="r-level">Level</label><select id="r-level" name="level"><option value="all">All levels</option>${opts(LEVEL)}</select></div>
          <div class="field"><label for="r-desc">Description <span class="opt">(optional)</span></label><textarea id="r-desc" name="description" maxlength="600" rows="2"></textarea></div>
          <fieldset class="field pt-choice"><legend>Source</legend>
            <label><input type="radio" name="source" value="file" checked> Upload a file</label>
            <label><input type="radio" name="source" value="url"> Paste a link</label>
          </fieldset>
          <div class="field" data-src="file"><label for="r-file">File (PDF, audio, video, Word or PowerPoint, up to 50 MB)</label><input id="r-file" name="file" type="file" accept=".pdf,.mp3,.m4a,.mp4,.doc,.docx,.ppt,.pptx,.epub,.jpg,.jpeg,.png"></div>
          <div class="field" data-src="url" hidden><label for="r-url">Link (for example a Google Drive or YouTube link)</label><input id="r-url" name="url" type="url" inputmode="url" placeholder="https://"></div>
          <p class="form-error" role="alert" tabindex="-1" hidden></p>
          <div class="pt-upload" hidden role="status"></div>
          <button class="btn btn--blue" type="submit">Add to library</button>
        </form>
      </section>` : ''}
      <div class="pt-filters" role="search">
        <div class="field"><label for="lib-q">Search</label><input id="lib-q" type="search" placeholder="Title, author or topic"></div>
        <div class="field"><label for="lib-s">Subject</label><select id="lib-s"><option value="">All subjects</option>${opts(SUBJECT)}</select></div>
        <div class="field"><label for="lib-l">Level</label><select id="lib-l"><option value="">All levels</option>${opts(LEVEL)}</select></div>
      </div>
      <p class="pt-meta" id="lib-count" aria-live="polite"></p>
      <div id="lib-list"></div>`);

    var list = $('#lib-list', el), q = $('#lib-q', el), fs = $('#lib-s', el), fl = $('#lib-l', el);
    function card(r) {
      var file = !!r.file_path;
      var canDel = isAdmin() || (staff && r.added_by === S.me.id);
      return html`<li class="pt-res">
        <span class="pt-res__icon" aria-hidden="true">${icon(file ? 'file' : 'link')}</span>
        <div class="pt-res__body">
          <strong class="pt-res__t">${r.title}</strong>
          <span class="pt-meta">${r.author ? r.author + ' · ' : ''}${SUBJECT[r.subject]} · ${r.level === 'all' ? 'All levels' : LEVEL[r.level]}${r.file_type ? ' · ' + r.file_type : ''}${r.file_size ? ' · ' + fmtSize(r.file_size) : ''}</span>
          ${r.description ? html`<p>${r.description}</p>` : ''}
        </div>
        <div class="pt-res__act">
          ${file ? html`<button type="button" class="btn btn--sm btn--blue" data-dl="${r.id}">${icon('download')}Download<span class="sr-only"> ${r.title}</span></button>`
                 : html`<a class="btn btn--sm btn--line" href="${safeUrl(r.url)}" target="_blank" rel="noopener">${icon('external')}Open<span class="sr-only"> ${r.title} (opens in a new tab)</span></a>`}
          ${canDel ? html`<button type="button" class="pt-textbtn" data-del-res="${r.id}">Remove</button>` : ''}
        </div>
      </li>`;
    }
    function draw() {
      var term = q.value.trim().toLowerCase(), s = fs.value, l = fl.value;
      var shown = items.filter(function (r) {
        if (s && r.subject !== s) return false;
        if (l && r.level !== l && r.level !== 'all') return false;
        if (term && (r.title + ' ' + (r.author || '') + ' ' + (r.description || '')).toLowerCase().indexOf(term) < 0) return false;
        return true;
      });
      $('#lib-count', el).textContent = items.length ? 'Showing ' + shown.length + ' of ' + plural(items.length, 'item') + '.' : '';
      list.innerHTML = out(!items.length ? empty('The library is empty for now', staff ? 'Use “Add material” to upload the first book or notes.' : 'Your teachers will add books, notes and audio here.')
        : !shown.length ? empty('Nothing matches your search', 'Try another word, or clear the filters.')
        : html`<ul class="pt-resources">${shown.map(card)}</ul>`);
    }
    [q, fs, fl].forEach(function (c) { c.addEventListener('input', draw); });
    draw();

    list.addEventListener('click', async function (ev) {
      var dl = ev.target.closest('[data-dl]'), del = ev.target.closest('[data-del-res]');
      if (dl) {
        var r = items.find(function (x) { return x.id === dl.dataset.dl; });
        busy(dl, true, 'Preparing…');
        try {
          var d = await run(S.sb.storage.from('materials').createSignedUrl(r.file_path, 600, { download: r.file_path.split('/').pop() }));
          window.location.href = d.signedUrl;
        } catch (e) { toast(friendly(e), 'error'); }
        finally { busy(dl, false); }
      }
      if (del) {
        if (del.dataset.confirm !== '1') { del.dataset.confirm = '1'; del.textContent = 'Press again to remove'; return; }
        var it = items.find(function (x) { return x.id === del.dataset.delRes; });
        del.disabled = true;
        try {
          var rows = await run(S.sb.from('resources').delete().eq('id', it.id).select('id'));
          if (!rows.length) throw new Error('That item could not be removed.');
          if (it.file_path) await S.sb.storage.from('materials').remove([it.file_path]);
          items = items.filter(function (x) { return x.id !== it.id; });
          toast('Removed from the library.'); draw();
        } catch (e) { del.disabled = false; toast(friendly(e), 'error'); }
      }
    });

    if (!staff) return;
    var addBtn = $('[data-add]', el), panel = $('#lib-add', el), f = $('#f-res', el);
    addBtn.addEventListener('click', function () {
      panel.hidden = !panel.hidden; addBtn.setAttribute('aria-expanded', String(!panel.hidden));
      if (!panel.hidden) $('#r-title', el).focus();
    });
    $$('[name=source]', f).forEach(function (rb) {
      rb.addEventListener('change', function () {
        $$('[data-src]', f).forEach(function (d) { d.hidden = d.dataset.src !== rb.value || !rb.checked; });
      });
    });
    onSubmit(f, async function (v) {
      if (!v.title || v.title.length < 2) throw new Error('Enter a title.');
      var row = { title: v.title, author: v.author || null, subject: v.subject, level: v.level || 'all', description: v.description || null };
      var up = $('.pt-upload', f), path = null;
      if (v.source === 'url') {
        if (!/^https?:\/\/\S+\.\S+/i.test(v.url || '')) throw new Error('Paste a full link that starts with https://');
        row.url = v.url; row.file_type = 'Link';
      } else {
        var file = $('#r-file', f).files[0];
        if (!file) throw new Error('Choose a file to upload.');
        if (file.size > 50 * 1048576) throw new Error('That file is larger than 50 MB. Upload it to Google Drive and paste the link instead.');
        var ext = (file.name.split('.').pop() || '').toLowerCase();
        var clean = file.name.replace(/[^\w.\-]+/g, '-').replace(/-+/g, '-').slice(-80);
        path = (window.crypto && crypto.randomUUID ? crypto.randomUUID() : String(Date.now())) + '/' + clean;
        up.hidden = false; up.textContent = 'Uploading ' + file.name + ' (' + fmtSize(file.size) + ')…';
        await run(S.sb.storage.from('materials').upload(path, file, { contentType: file.type || undefined, upsert: false }));
        row.file_path = path; row.file_size = file.size;
        row.file_type = ({ pdf: 'PDF', mp3: 'Audio', m4a: 'Audio', mp4: 'Video', doc: 'Word', docx: 'Word', ppt: 'Slides', pptx: 'Slides', epub: 'eBook', jpg: 'Image', jpeg: 'Image', png: 'Image' })[ext] || ext.toUpperCase();
      }
      try {
        await run(S.sb.from('resources').insert(row));
      } catch (e) {
        if (path) await S.sb.storage.from('materials').remove([path]);
        up.hidden = true;
        throw e;
      }
      toast('Added to the library.');
      S.focusNext = false; viewLibrary(el);
    });
  }

  // ===================================================================== student: my class
  async function viewClasses(el) {
    var mine = token();
    view(el, loading('Loading your class…'), false);
    var res = await Promise.all([myGroups(), run(S.sb.rpc('my_teachers')), run(S.sb.rpc('my_classmates'))]);
    if (!mine()) return;
    var groups = res[0], teachers = res[1] || [], mates = res[2] || [];
    var today = lagosNow().getDay();
    var groupCard = function (track, label, gid, level, levels) {
      var g = gid && groups[gid], id = 'c-' + track;
      if (!g) return html`<section class="pt-card" aria-labelledby="${id}"><h3 id="${id}">${icon(track === 'quran' ? 'quran' : 'book')}${label} class</h3>
        ${empty('Not placed yet', 'The Islamiyyah committee will place you in a ' + label + ' class soon.')}</section>`;
      var ts = teachers.filter(function (t) { return t.group_id === g.id; });
      var ms = mates.filter(function (m) { return m.group_name === g.name && m.track === track; });
      return html`<section class="pt-card" aria-labelledby="${id}">
        <h3 id="${id}">${icon(track === 'quran' ? 'quran' : 'book')}${label} class</h3>
        <p class="pt-classname"><strong>${g.name}</strong><span class="pt-meta">${levels[level || g.level]} · ${WING[g.wing]}</span></p>
        <h4 class="pt-sub">${ts.length > 1 ? 'Teachers' : 'Teacher'}</h4>
        ${ts.length ? html`<ul class="pt-people">${ts.map(function (t) {
          return html`<li><span class="pt-mono" aria-hidden="true">${initials(t.full_name)}</span><div><strong>${t.full_name}</strong>
            ${t.subjects ? html`<span class="pt-meta">${t.subjects}</span>` : ''}${t.bio ? html`<p>${t.bio}</p>` : ''}</div></li>`;
        })}</ul>` : html`<p class="pt-meta">To be assigned.</p>`}
        <details class="pt-details pt-mates"><summary>Classmates (${ms.length})</summary>
          ${ms.length ? html`<ul class="pt-chips">${ms.map(function (m) { return html`<li>${m.full_name}</li>`; })}</ul>` : html`<p class="pt-meta">No classmates listed yet.</p>`}
        </details>
      </section>`;
    };
    view(el, html`
      <h2 class="pt-h">My class</h2>
      <div class="pt-grid">
        ${groupCard('quran', 'Qur’an', S.me.quran_group, S.me.quran_level, QLEVEL)}
        ${groupCard('arabic', 'Arabic', S.me.arabic_group, S.me.arabic_level, LEVEL)}
      </div>
      <section class="pt-card" aria-labelledby="c-tt">
        <h3 id="c-tt">${icon('calendar')}Weekend timetable</h3>
        <table class="pt-table"><caption class="sr-only">Islamiyyah weekend timetable</caption>
          <thead><tr><th scope="col">Day</th><th scope="col">Time</th><th scope="col">Session</th></tr></thead>
          <tbody>${DATA.timetable.map(function (x) {
            return html`<tr${raw(x.day === today ? ' class="is-today"' : '')}><td data-label="Day"><span class="pt-td">${DAYNAMES[x.day]}${x.day === today ? html` ${pill('Today', 'yellow')}` : ''}</span></td><td data-label="Time"><span class="pt-td">${t12(x.start)} to ${t12(x.end)}</span></td><td data-label="Session"><span class="pt-td">${x.title}<span class="pt-meta"> ${x.note}</span></span></td></tr>`;
          })}</tbody></table>
        <p class="pt-meta">All classes hold at the ${DATA.venue}. Classmates are shown by name only.</p>
      </section>
      <section class="pt-card" aria-labelledby="c-books">
        <h3 id="c-books">${icon('book')}Sunday book studies</h3>
        <p class="pt-meta">All students study these books together on Sundays.</p>
        <ul class="pt-booklist">${DATA.books.map(function (b) {
          return html`<li><div><span lang="ar" dir="rtl" class="pt-ar">${b.ar}</span><strong>${b.en}${b.note && b.note.indexOf('Part') === 0 ? ', ' + b.note : ''}</strong><span class="pt-meta">${b.subject}${b.pages ? ' · ' + b.pages + ' pages' : ''}</span></div>
            ${b.file ? html`<a class="btn btn--sm btn--line" href="${b.file}" download>${icon('download')}PDF<span class="sr-only"> of ${b.en}</span></a>` : ''}</li>`;
        })}</ul>
      </section>`);
  }

  // ===================================================================== profile
  function viewProfile(el) {
    var m = S.me, staff = inIslamiyyah() && m.role !== 'student', dOnly = dawrahOnly();
    view(el, html`
      <h2 class="pt-h">My profile</h2>
      <div class="pt-grid">
        <section class="pt-card" aria-labelledby="p-acc">
          <h3 id="p-acc">Account</h3>
          <dl class="pt-dl">
            <div><dt>Email</dt><dd>${m.email}</dd></div>
            ${dOnly ? html`<div><dt>Programme</dt><dd>${S.dawrah.term.title}</dd></div>` : html`<div><dt>Role</dt><dd>${roleLabel('islamiyyah').split(' · ')[0]}</dd></div>`}
            ${dawrahAccess() && !dOnly ? html`<div><dt>Dawrah</dt><dd>${S.dawrah.admin ? 'Admin' : 'Student'}, ${S.dawrah.term.title}</dd></div>` : ''}
            <div><dt>${dOnly ? 'Brother or sister' : 'Class'}</dt><dd>${m.wing ? (dOnly ? (m.wing === 'sisters' ? 'Sister' : 'Brother') : WING[m.wing]) : 'Not set'}</dd></div>
            ${dOnly || staff ? '' : html`<div><dt>Qur’an level</dt><dd>${m.quran_level ? QLEVEL[m.quran_level] : 'Not assigned'}</dd></div>
            <div><dt>Arabic level</dt><dd>${m.arabic_level ? LEVEL[m.arabic_level] : 'Not assigned'}</dd></div>`}
            <div><dt>Member since</dt><dd>${fmtDate(m.created_at)}</dd></div>
          </dl>
          <p class="pt-meta">${dOnly ? 'To change your email, message the Dawrah team.' : 'To change your class, level or email, ask the Islamiyyah admin.'}</p>
        </section>
        <section class="pt-card" aria-labelledby="p-edit">
          <h3 id="p-edit">Your details</h3>
          <form class="form form--plain pt-form" id="f-prof" novalidate>
            <div class="field"><label for="p-name">Full name</label><input id="p-name" name="full_name" required minlength="2" maxlength="120" value="${m.full_name}"></div>
            <div class="field"><label for="p-phone">WhatsApp number</label><input id="p-phone" name="phone" type="tel" inputmode="tel" maxlength="20" value="${m.phone || ''}"></div>
            <div class="field--2">
              <div class="field"><label for="p-dept">Department</label><input id="p-dept" name="department" maxlength="120" value="${m.department || ''}"></div>
              <div class="field"><label for="p-level">Level</label><select id="p-level" name="level"><option value="">Choose</option>${STUDY_LEVELS.map(function (l) { return html`<option${raw(l === m.level ? ' selected' : '')}>${l}</option>`; })}</select></div>
            </div>
            ${staff ? html`<div class="field"><label for="p-subj">Subjects you teach</label><input id="p-subj" name="subjects" maxlength="200" value="${m.subjects || ''}" placeholder="For example: Tajweed and Hifz"></div>
            <div class="field"><label for="p-bio">Short introduction <span class="opt">(students see this)</span></label><textarea id="p-bio" name="bio" maxlength="500" rows="3">${m.bio || ''}</textarea></div>` : ''}
            <p class="form-error" role="alert" tabindex="-1" hidden></p>
            <button class="btn btn--blue" type="submit">Save details</button>
          </form>
        </section>
        <section class="pt-card" aria-labelledby="p-pw">
          <h3 id="p-pw">Change password</h3>
          <form class="form form--plain pt-form" id="f-pw" novalidate>
            ${passwordField('cp-pw', 'New password (at least 8 characters)', 'password', 'new-password', 8)}
            ${passwordField('cp-pw2', 'Confirm new password', 'password2', 'new-password', 8)}
            <p class="form-error" role="alert" tabindex="-1" hidden></p>
            <button class="btn btn--blue" type="submit">Change password</button>
          </form>
        </section>
        <section class="pt-card" aria-labelledby="p-priv">
          <h3 id="p-priv">${icon('shield')}Your privacy</h3>
          <p>Your details and records are visible only to you, your teachers and the portal admins. Classmates see your name only. To delete your account and records, message ${dOnly ? 'the Dawrah team' : 'the Islamiyyah admin'}.</p>
          ${dOnly ? dwHelp() : helpLink()}
        </section>
        ${dOnly ? html`<section class="pt-card" aria-labelledby="p-isl">
          <h3 id="p-isl">${icon('quran')}Islamiyyah classes</h3>
          ${m.joins_islamiyyah ? html`<p>Your Islamiyyah sign-up is waiting for the committee’s approval.</p>`
            : html`<p>The weekend Islamiyyah classes cover Qur’an, Arabic and Islamic books. Want to join?</p>
              <button type="button" class="btn btn--sm btn--blue" data-join>I want to join the Islamiyyah</button>`}
        </section>` : ''}
      </div>`);
    var jb = $('[data-join]', el);
    if (jb) jb.addEventListener('click', async function () {
      busy(jb, true, 'Sending…');
      try {
        var rows = await run(S.sb.from('profiles').update({ joins_islamiyyah: true }).eq('id', m.id).select('*'));
        S.me = rows[0]; toast('Done. The Islamiyyah committee will review your sign-up.'); S.focusNext = false; viewProfile(el);
      } catch (e) { busy(jb, false); toast(friendly(e), 'error'); }
    });
    onSubmit($('#f-prof', el), async function (v) {
      if (!v.full_name || v.full_name.length < 2) throw new Error('Enter your full name.');
      var row = { full_name: v.full_name, phone: v.phone || null, department: v.department || null, level: v.level || null };
      if (staff) { row.subjects = v.subjects || null; row.bio = v.bio || null; }
      var rows = await run(S.sb.from('profiles').update(row).eq('id', m.id).select('*'));
      S.me = rows[0];
      toast('Your details are saved.');
      $('.pt-who strong').textContent = S.me.full_name;
    });
    var fp = $('#f-pw', el); wirePw(fp);
    onSubmit(fp, async function (v, form) {
      if ((v.password || '').length < 8) throw new Error('Your password must be at least 8 characters.');
      if (v.password !== v.password2) throw new Error('The two passwords do not match.');
      await run(S.sb.auth.updateUser({ password: v.password }));
      form.reset();
      toast('Your password is changed.');
    });
  }

  // ===================================================================== teaching
  async function teachingData() {
    var gt = await run(S.sb.from('group_teachers').select('group_id').eq('teacher_id', S.me.id));
    var ids = gt.map(function (r) { return r.group_id; });
    if (!ids.length) return { groups: [], students: [], logs: [] };
    var res = await Promise.all([
      run(S.sb.from('groups').select('*').in('id', ids).order('name')),
      run(S.sb.from('profiles').select('*').in('quran_group', ids).eq('status', 'active').order('full_name')),
      run(S.sb.from('profiles').select('*').in('arabic_group', ids).eq('status', 'active').order('full_name'))
    ]);
    var seen = {}, students = [];
    res[1].concat(res[2]).forEach(function (p) { if (!seen[p.id] && p.id !== S.me.id) { seen[p.id] = 1; students.push(p); } });
    var logs = students.length ? await run(S.sb.from('quran_logs').select('*').in('student_id', students.map(function (s) { return s.id; })).order('log_date', { ascending: false }).limit(3000)) : [];
    return { groups: res[0], students: students, logs: logs };
  }

  async function viewTeach(el) {
    var mine = token();
    view(el, loading('Loading your groups…'), false);
    var d = await teachingData();
    if (!mine()) return;
    var names = {}; d.students.forEach(function (s) { names[s.id] = s.full_name; });
    var unverified = d.logs.filter(function (l) { return !l.verified; });
    var logsBy = {}; d.logs.forEach(function (l) { (logsBy[l.student_id] = logsBy[l.student_id] || []).push(l); });
    view(el, html`
      <h2 class="pt-h">${isAdmin() ? 'My teaching' : 'My students'}</h2>
      ${!d.groups.length ? empty('You have not been assigned a group yet', 'An admin assigns teachers to groups in Groups.', isAdmin() ? html`<a class="btn btn--sm btn--blue" href="#/groups">Manage groups</a>` : '') : ''}
      ${unverified.length ? html`<section class="pt-card" aria-labelledby="t-ver">
        <h3 id="t-ver">${icon('check')}Records to verify (${unverified.length})</h3>
        <p class="pt-meta">Students recorded these themselves. Verify them after you listen at class.</p>
        <ul class="pt-logs">${unverified.slice(0, 30).map(function (l) {
          return html`<li class="pt-log"><div class="pt-log__main"><span class="pt-log__date">${fmtDate(l.log_date)}</span>
            <strong><a href="#/student/${l.student_id}">${names[l.student_id]}</a>: ${rangeText(l)}</strong>
            <span class="pt-log__tags">${pill(KIND[l.kind].split(' (')[0], 'mist')}</span>${l.note ? html`<p class="pt-log__note">${l.note}</p>` : ''}</div>
            <div class="pt-log__act"><button type="button" class="btn btn--sm btn--blue" data-verify="${l.id}">${icon('check')}Verify</button></div></li>`;
        })}</ul></section>` : ''}
      ${d.groups.map(function (g) {
        var members = d.students.filter(function (s) { return s.quran_group === g.id || s.arabic_group === g.id; });
        return html`<section class="pt-card" aria-labelledby="g-${g.id}">
          <div class="pt-headrow"><h3 id="g-${g.id}">${g.name}</h3><span class="pt-meta">${TRACK[g.track]} · ${(g.track === 'quran' ? QLEVEL : LEVEL)[g.level]} · ${WING[g.wing]}</span></div>
          ${g.track === 'arabic' ? html`<details class="pt-details pt-progbox"><summary>Class progress: ${g.current_lesson == null ? 'not recorded yet' : (g.total_lessons ? g.current_lesson + ' of ' + g.total_lessons + ' lessons' : plural(g.current_lesson, 'lesson')) + ' completed'}</summary>
            <form class="form form--plain pt-form" data-prog="${g.id}" novalidate>
              <p class="pt-meta">Students see this on their Arabic page. Update it after each class.</p>
              <div class="field--2">
                <div class="field"><label for="pl-${g.id}">Lessons completed</label><input id="pl-${g.id}" name="lesson" type="number" inputmode="numeric" min="0" max="200" required value="${g.current_lesson == null ? '' : g.current_lesson}"></div>
                <div class="field"><label for="pn-${g.id}">Lessons in the book <span class="opt">(optional)</span></label><input id="pn-${g.id}" name="total" type="number" inputmode="numeric" min="1" max="200" value="${g.total_lessons || ''}"></div>
              </div>
              <div class="field"><label for="pb-${g.id}">Book <span class="opt">(optional)</span></label><input id="pb-${g.id}" name="book" maxlength="120" value="${g.book || ''}" placeholder="For example: Durus al-Lughah, Book 1"></div>
              <p class="form-error" role="alert" tabindex="-1" hidden></p>
              <button class="btn btn--sm btn--blue" type="submit">Save progress</button>
            </form></details>` : ''}
          ${members.length ? html`<table class="pt-table"><caption class="sr-only">Students in ${g.name}</caption>
            <thead><tr><th scope="col">Student</th>${g.track === 'quran' ? html`<th scope="col">Memorised</th><th scope="col">Last record</th>` : html`<th scope="col">Department</th>`}<th scope="col"><span class="sr-only">Open</span></th></tr></thead>
            <tbody>${members.map(function (s) {
              var pr = g.track === 'quran' ? progress(logsBy[s.id] || []) : null;
              return html`<tr><td data-label="Student"><span class="pt-td"><strong>${s.full_name}</strong></span></td>
                ${pr ? html`<td data-label="Memorised"><span class="pt-td">${fmtNum(pr.memorised)} ayahs (${(pr.pct * 100).toFixed(1)}%)</span></td><td data-label="Last record"><span class="pt-td">${pr.lastDate ? fmtDate(pr.lastDate) : 'None'}</span></td>` : html`<td data-label="Department"><span class="pt-td">${s.department || '—'}${s.level ? ', ' + s.level : ''}</span></td>`}
                <td><a class="btn btn--sm btn--line" href="#/student/${s.id}">Open<span class="sr-only"> ${s.full_name}</span></a></td></tr>`;
            })}</tbody></table>` : empty('No students in this group yet', 'An admin places students in groups.')}
          <details class="pt-details"><summary>Post a notice to ${g.name}</summary>
            <form class="form form--plain pt-form" data-notice="${g.id}" novalidate>
              <div class="field"><label for="n-t-${g.id}">Title</label><input id="n-t-${g.id}" name="title" required maxlength="140"></div>
              <div class="field"><label for="n-b-${g.id}">Message</label><textarea id="n-b-${g.id}" name="body" required maxlength="2000" rows="3"></textarea></div>
              <p class="form-error" role="alert" tabindex="-1" hidden></p>
              <button class="btn btn--blue btn--sm" type="submit">Post notice</button>
            </form></details>
        </section>`;
      })}`);
    wireLogList(el, function () { S.focusNext = false; viewTeach(el); });
    $$('[data-prog]', el).forEach(function (f) {
      onSubmit(f, async function (v, form) {
        var lesson = parseInt(v.lesson, 10), total = v.total === '' ? null : parseInt(v.total, 10);
        if (!(lesson >= 0 && lesson <= 200)) throw new Error('Enter how many lessons the class has completed.');
        if (total !== null && !(total >= 1 && total <= 200)) throw new Error('Enter how many lessons the book has, or leave it empty.');
        if (total !== null && lesson > total) throw new Error('Lessons completed cannot be more than the lessons in the book.');
        await run(S.sb.rpc('set_group_progress', { g: form.dataset.prog, lesson: lesson, total: total, book_name: v.book || '' }));
        toast('Class progress saved.'); S.focusNext = false; viewTeach(el);
      });
    });
    $$('[data-notice]', el).forEach(function (f) {
      onSubmit(f, async function (v, form) {
        if (!v.title || !v.body) throw new Error('Enter a title and a message.');
        await run(S.sb.from('announcements').insert({ title: v.title, body: v.body, audience: 'group', group_id: form.dataset.notice }));
        form.reset(); form.closest('details').open = false;
        toast('Notice posted to the group.');
      });
    });
  }

  async function viewStudent(el, args) {
    var id = args[0], mine = token();
    view(el, loading('Loading the student record…'), false);
    var res = await Promise.all([
      run(S.sb.from('profiles').select('*').eq('id', id).maybeSingle()),
      run(S.sb.from('quran_logs').select('*').eq('student_id', id).order('log_date', { ascending: false }).order('created_at', { ascending: false }).limit(2000)),
      run(S.sb.from('assessments').select('*').eq('student_id', id).order('assessed_on', { ascending: false }))
    ]);
    if (!mine()) return;
    var p = res[0], logs = res[1], assess = res[2];
    if (!p) return view(el, html`<h2 class="pt-h">Student not found</h2>${empty('This student is not in your groups', 'You can open the records of students in the groups you teach.', html`<a class="btn btn--sm btn--blue" href="#/teach">Back to Teaching</a>`)}`);
    var pr = progress(logs);
    var wa = waLink(p.phone, 'Assalamu alaykum ' + firstName(p.full_name) + ', ');
    view(el, html`
      <p class="pt-back"><a href="${isAdmin() && location.hash.indexOf('from=admin') > 0 ? '#/member/' + p.id : '#/teach'}">← Back</a></p>
      <div class="pt-headrow"><h2 class="pt-h">${p.full_name}</h2>${isAdmin() ? html`<a class="btn btn--sm btn--line" href="#/member/${p.id}">Edit account</a>` : ''}</div>
      <p class="pt-meta">${p.wing ? WING[p.wing] : ''}${p.department ? ' · ' + p.department : ''}${p.level ? ', ' + p.level : ''}${p.phone ? html` · <a href="tel:${p.phone.replace(/[^\d+]/g, '')}">${p.phone}</a>` : ''}${wa ? html` · <a href="${wa}" target="_blank" rel="noopener">WhatsApp<span class="sr-only"> (opens WhatsApp)</span></a>` : ''}</p>
      <section class="pt-card" aria-label="Qur’an summary">${quranSummary(pr, p.quran_level, assess.filter(function (a) { return a.track === 'quran'; })[0])}</section>
      <div class="pt-grid">
        <section class="pt-card" aria-labelledby="s-add"><h3 id="s-add">${icon('plus')}Add a verified record</h3>${logForm('f-tlog', true)}</section>
        <section class="pt-card" aria-labelledby="s-as"><h3 id="s-as">${icon('star')}Add an assessment</h3>
          <form class="form form--plain pt-form" id="f-assess" novalidate>
            <div class="field--2">
              <div class="field"><label for="a-track">Area</label><select id="a-track" name="track">${opts(TRACK, 'quran')}</select></div>
              <div class="field"><label for="a-date">Date</label><input id="a-date" name="assessed_on" type="date" value="${todayISO()}" max="${todayISO()}" required></div>
            </div>
            <div class="field"><label for="a-title">Title</label><input id="a-title" name="title" required maxlength="120" placeholder="For example: Juz Amma test, or Weekly recitation"></div>
            <div class="field"><label for="a-score">Score out of 100 <span class="opt">(optional)</span></label><input id="a-score" name="score" type="number" inputmode="decimal" min="0" max="100" step="0.5"></div>
            <div class="field"><label for="a-comment">Comment for the student</label><textarea id="a-comment" name="comment" maxlength="1000" rows="3"></textarea></div>
            <p class="form-error" role="alert" tabindex="-1" hidden></p>
            <button class="btn btn--blue" type="submit">Save assessment</button>
          </form></section>
        <section class="pt-card" aria-labelledby="s-juz"><h3 id="s-juz">Progress by juz</h3>${juzGrid(pr)}</section>
        <section class="pt-card" aria-labelledby="s-ch"><h3 id="s-ch">Progress over time</h3>${weeklyChart(weekly(logs))}</section>
        <section class="pt-card pt-card--wide" aria-labelledby="s-hist"><h3 id="s-hist">Qur’an records</h3>${logList(logs, { staff: true, emptyText: 'No records yet. Add the first one above.' })}</section>
        <section class="pt-card pt-card--wide" aria-labelledby="s-fb"><h3 id="s-fb">Assessments</h3><div id="s-fb-list">${assessmentList(assess, true)}</div></section>
      </div>`);
    var reload = function () { S.focusNext = false; viewStudent(el, args); };
    var f = $('#f-tlog', el); wireLogForm(f);
    onSubmit(f, async function (v) {
      var row = readLog(v); row.student_id = p.id; row.verified = true;
      await run(S.sb.from('quran_logs').insert(row));
      toast('Saved for ' + firstName(p.full_name) + ': ' + rangeText(row) + '.'); reload();
    });
    onSubmit($('#f-assess', el), async function (v) {
      if (!v.title || v.title.length < 2) throw new Error('Enter a title for the assessment.');
      var score = v.score === '' ? null : Number(v.score);
      if (score !== null && !(score >= 0 && score <= 100)) throw new Error('The score must be between 0 and 100.');
      if (!v.assessed_on || v.assessed_on > todayISO()) throw new Error('Choose a date that is not in the future.');
      await run(S.sb.from('assessments').insert({ student_id: p.id, track: v.track, title: v.title, assessed_on: v.assessed_on, score: score, comment: v.comment || null }));
      toast('Assessment saved.'); reload();
    });
    wireLogList(el, reload);
    wireChart(el);
    $$('[data-del-assess]', el).forEach(function (b) {
      b.addEventListener('click', async function () {
        if (b.dataset.confirm !== '1') { b.dataset.confirm = '1'; b.textContent = 'Press again to delete'; return; }
        try {
          var rows = await run(S.sb.from('assessments').delete().eq('id', b.dataset.delAssess).select('id'));
          if (!rows.length) throw new Error('That assessment could not be deleted.');
          toast('Assessment deleted.'); reload();
        } catch (e) { toast(friendly(e), 'error'); }
      });
    });
  }

  // ===================================================================== notices
  async function viewNotices(el) {
    var mine = token();
    view(el, loading('Loading announcements…'), false);
    var res = await Promise.all([
      run(S.sb.from('announcements').select('*').order('pinned', { ascending: false }).order('created_at', { ascending: false }).limit(100)),
      run(S.sb.from('groups').select('*').order('name')),
      isAdmin() ? Promise.resolve(null) : run(S.sb.from('group_teachers').select('group_id').eq('teacher_id', S.me.id))
    ]);
    if (!mine()) return;
    var list = res[0], groups = res[1], gnames = {};
    groups.forEach(function (g) { gnames[g.id] = g.name + ' (' + TRACK[g.track] + ')'; });
    var mineG = res[2] ? res[2].map(function (r) { return r.group_id; }) : groups.map(function (g) { return g.id; });
    var audOpts = (isAdmin() ? [html`<option value="all">Everyone</option><option value="brothers">Brothers only</option><option value="sisters">Sisters only</option>`] : [])
      .concat(groups.filter(function (g) { return mineG.indexOf(g.id) >= 0; }).map(function (g) { return html`<option value="g:${g.id}">${gnames[g.id]}</option>`; }));
    view(el, html`
      <h2 class="pt-h">Announcements</h2>
      <section class="pt-card" aria-labelledby="n-new"><h3 id="n-new">${icon('bell')}Post an announcement</h3>
        ${audOpts.length ? html`<form class="form form--plain pt-form" id="f-notice" novalidate>
          <div class="field"><label for="n-aud">Who should see it?</label><select id="n-aud" name="aud" required>${audOpts}</select></div>
          <div class="field"><label for="n-title">Title</label><input id="n-title" name="title" required maxlength="140"></div>
          <div class="field"><label for="n-body">Message</label><textarea id="n-body" name="body" required maxlength="2000" rows="4"></textarea></div>
          ${isAdmin() ? html`<label class="pt-consent"><input type="checkbox" name="pinned" value="yes"><span>Pin to the top of everyone’s home page</span></label>` : ''}
          <p class="form-error" role="alert" tabindex="-1" hidden></p>
          <button class="btn btn--blue" type="submit">Post</button>
        </form>` : empty('You can post once you are assigned a group', '')}
      </section>
      <section class="pt-card" aria-labelledby="n-all"><h3 id="n-all">All announcements</h3><div id="n-list">${noticeList(list, { groups: gnames })}</div></section>`);
    onSubmit($('#f-notice', el), async function (v) {
      if (!v.title || !v.body) throw new Error('Enter a title and a message.');
      var row = { title: v.title, body: v.body, pinned: v.pinned === 'yes' };
      if (v.aud.indexOf('g:') === 0) { row.audience = 'group'; row.group_id = v.aud.slice(2); } else row.audience = v.aud;
      await run(S.sb.from('announcements').insert(row));
      toast('Announcement posted.'); S.focusNext = false; viewNotices(el);
    });
    $$('[data-del-notice]', el).forEach(function (b) {
      b.addEventListener('click', async function () {
        if (b.dataset.confirm !== '1') { b.dataset.confirm = '1'; b.textContent = 'Press again to delete'; return; }
        try {
          var rows = await run(S.sb.from('announcements').delete().eq('id', b.dataset.delNotice).select('id'));
          if (!rows.length) throw new Error('That announcement could not be deleted.');
          toast('Announcement deleted.'); S.focusNext = false; viewNotices(el);
        } catch (e) { toast(friendly(e), 'error'); }
      });
    });
  }

  // ===================================================================== Dawrah
  // Students: the latest class (recording + two questions), all classes, progress, book and exam.
  // Dawrah admins: follow-up table, classes, exam, registrations and settings.
  var DW = (DATA && DATA.dawrah) || { coordinators: [] };
  var LETTERS = 'ABCDEF';
  var dTerm = function () { return S.dawrah && S.dawrah.term; };
  var portalUrl = function () { return location.origin + location.pathname; };

  function dwHead(cur) {
    var t = dTerm();
    return html`<h2 class="pt-h">${t.title}</h2>
      <p class="pt-dw-lede">${[t.schedule, t.venue].filter(Boolean).join(' · ')}</p>`;
  }
  function dwHelp() {
    if (!DW.coordinators.length) return '';
    return html`<p class="pt-dw-help">${icon('whatsapp')}<span>Questions about the Dawrah? WhatsApp ${DW.coordinators.map(function (c, i) {
      return html`${i ? (i === DW.coordinators.length - 1 ? ' or ' : ', ') : ''}<a href="${c[2]}" target="_blank" rel="noopener">${c[0]}<span class="sr-only"> (opens WhatsApp)</span></a>`;
    })}.</span></p>`;
  }
  function dayLabel(c) { return 'Day ' + c.day_number; }

  async function viewDawrah(el, args) {
    args = args || [];
    var sub = args[0] || '', d = S.dawrah;
    if (d.admin) {
      if (sub === '') return dwTracker(el);
      if (sub === 'classes') return dwClasses(el);
      if (sub === 'new') return dwEditClass(el, null);
      if (sub === 'edit') return dwEditClass(el, args[1]);
      if (sub === 'student') return dwStudent(el, decodeURIComponent(args[1] || ''));
      if (sub === 'exam-setup') return dwExamSetup(el);
      if (sub === 'settings') return dwSettings(el);
      if (!d.student && sub === 'class') return dwEditClass(el, args[1]);
    }
    if (d.student) {
      if (sub === 'class') return dwClass(el, args[1]);
      if (sub === 'exam') return dwExam(el);
      return dwHome(el);
    }
    return dwTracker(el);
  }

  // ------------------------------------------------------------------ student: home
  async function dwHome(el) {
    var mine = token(), t = dTerm();
    view(el, loading('Loading the Dawrah…'), false);
    var res = await Promise.all([
      run(S.sb.rpc('dawrah_my_classes')),
      run(S.sb.from('dawrah_attempts').select('score,total').eq('user_id', S.me.id).eq('term_id', t.id).is('lesson_id', null)),
      run(S.sb.from('dawrah_roster').select('written_score').eq('term_id', t.id).eq('email', String(S.me.email).toLowerCase()))
    ]);
    if (!mine()) return;
    var classes = res[0] || [], exam = res[1][0], written = res[2][0] && res[2][0].written_score;
    var withQ = classes.filter(function (c) { return c.questions > 0; });
    var done = withQ.filter(function (c) { return c.score != null; });
    var right = done.reduce(function (a, c) { return a + c.score; }, 0), asked = done.reduce(function (a, c) { return a + c.total; }, 0);
    var next = classes.find(function (c) { return c.questions > 0 && c.score == null; }) ||
               classes.find(function (c) { return !c.questions && !c.opened; });
    var status = function (c) {
      if (c.questions) return c.score != null ? pill('Done · ' + c.score + '/' + c.total, 'green') : pill('To do', 'yellow');
      return c.opened ? pill('Listened', 'green') : pill('New', 'blue');
    };
    var examLine = exam ? html`<p><strong>${t.exam_title}:</strong> ${exam.score} of ${exam.total}${written != null ? html` · written part: ${Number(written)}` : ''}</p>`
      : t.exam_open ? html`<a class="btn btn--sm btn--blue" href="#/dawrah/exam">Take the ${t.exam_title.toLowerCase()}</a>`
      : html`<p class="pt-meta">The ${t.exam_title.toLowerCase()} opens at the end of the Dawrah.</p>`;
    view(el, html`
      ${dwHead('mine')}
      <section class="pt-card pt-card--blue" aria-labelledby="dw-next">
        <h3 id="dw-next">${icon('clock')}${next ? 'Your next step' : 'You are up to date'}</h3>
        ${next ? html`<p class="pt-next__when">${dayLabel(next)} · ${fmtDate(next.lesson_date, false)}</p>
            <p class="pt-next__what">${next.title}</p>
            <p class="pt-next__where">${next.questions ? 'Listen to the class, then answer ' + plural(next.questions, 'short question') + '.' : 'Listen to the class.'}</p>
            <a class="pt-cardlink" href="#/dawrah/class/${next.id}">Open the class</a>`
          : classes.length ? html`<p class="pt-next__where">You have done every class so far. The next class appears here after it holds.</p>`
          : html`<p class="pt-next__what">The first class is coming soon.</p><p class="pt-next__where">After each class, its recording and two short questions appear here.</p>`}
      </section>
      <div class="pt-grid">
        <section class="pt-card" aria-labelledby="dw-prog">
          <h3 id="dw-prog">${icon('star')}Your progress</h3>
          <div class="pt-hero"><span class="pt-hero__v">${done.length}</span><span class="pt-hero__s">of ${plural(withQ.length, 'class', 'classes')} done</span></div>
          ${bar(withQ.length ? done.length / withQ.length : 0, 'Dawrah classes done')}
          <p class="pt-meta">${asked ? 'Questions right: ' + right + ' of ' + asked : 'Your scores appear here after you answer.'}</p>
          ${examLine}
        </section>
        <section class="pt-card" aria-labelledby="dw-book">
          <h3 id="dw-book">${icon('book')}The book</h3>
          ${t.book_url ? html`<p>Download the book we are studying, to read along and revise.</p>
              <a class="btn btn--sm btn--blue" href="${/^assets\//.test(t.book_url) ? t.book_url : safeUrl(t.book_url)}" target="_blank" rel="noopener">${icon('download')}Download the book (PDF)</a>`
            : html`<p>The book (PDF) is coming soon, in sha Allah.</p>`}
        </section>
      </div>
      <section class="pt-card" aria-labelledby="dw-all">
        <h3 id="dw-all">${icon('calendar')}Classes</h3>
        ${classes.length ? html`<ul class="pt-dw-list">${classes.map(function (c) {
          return html`<li><a href="#/dawrah/class/${c.id}"><span class="pt-dw-day">${c.day_number}</span>
            <span class="pt-dw-t"><strong>${c.title}</strong><span class="pt-meta">${fmtDate(c.lesson_date, false)}</span></span>${status(c)}</a></li>`;
        })}</ul>` : empty('No classes yet', 'Each class appears here on the day it holds.')}
      </section>
      ${dwHelp()}`);
  }

  // ------------------------------------------------------------------ student: one class
  function dwPlayer(url, title) {
    if (!url) return html`<p class="pt-meta">The recording will be added soon.</p>`;
    var m, link = html`<p><a href="${safeUrl(url)}" target="_blank" rel="noopener">Not playing? Open the recording in a new tab<span class="sr-only"> (opens in a new tab)</span></a></p>`;
    if ((m = url.match(/drive\.google\.com\/(?:file\/d\/|open\?id=|uc\?(?:export=\w+&)?id=)([\w-]{10,})/)))
      return html`<div class="pt-dw-player"><iframe src="https://drive.google.com/file/d/${m[1]}/preview" title="Recording: ${title}" allow="autoplay" loading="lazy"></iframe></div>${link}`;
    if ((m = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/))([\w-]{11})/)))
      return html`<div class="pt-dw-player pt-dw-player--video"><iframe src="https://www.youtube-nocookie.com/embed/${m[1]}" title="Recording: ${title}" allow="encrypted-media; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>${link}`;
    if (/\.(mp3|m4a|aac|ogg|oga|opus|wav)(\?|#|$)/i.test(url))
      return html`<audio class="pt-dw-audio" controls preload="none" src="${safeUrl(url)}"></audio>${link}`;
    return html`<a class="btn btn--blue" href="${safeUrl(url)}" target="_blank" rel="noopener">${icon('external')}Listen to the recording<span class="sr-only"> (opens in a new tab)</span></a>`;
  }
  function dwQuiz(qs, label, note) {
    return html`<form class="pt-dw-quiz" id="dw-quiz" novalidate>
      ${qs.map(function (q, n) {
        return html`<fieldset class="pt-dw-q"><legend><span class="pt-dw-qn">Question ${n + 1}${qs.length > 1 ? ' of ' + qs.length : ''}</span>${q.prompt}</legend>
          ${q.options.map(function (o, k) {
            return html`<label class="pt-dw-opt"><input type="radio" name="${q.id}" value="${k}"><span><b>${LETTERS[k]}</b>${o}</span></label>`;
          })}</fieldset>`;
      })}
      <p class="pt-meta">${note}</p>
      <p class="form-error" role="alert" tabindex="-1" hidden></p>
      <button class="btn btn--blue" type="submit">${label}</button>
    </form>`;
  }
  function dwAnswers(form, qs) {
    var a = {}, missing = 0;
    qs.forEach(function (q) {
      var c = $('input[name="' + q.id + '"]:checked', form);
      if (c) a[q.id] = Number(c.value); else missing++;
    });
    return { answers: a, missing: missing };
  }
  function dwReview(list) {
    var score = list.filter(function (q) { return q.chosen === q.correct; }).length;
    return html`<p class="pt-dw-score${raw(score === list.length ? ' is-full' : '')}" tabindex="-1">${icon(score === list.length ? 'check' : 'star')}<span>You got <strong>${score} of ${list.length}</strong> right.${score === list.length ? ' Masha Allah!' : ' The right answers are marked below.'}</span></p>
      ${list.map(function (q, n) {
        return html`<div class="pt-dw-q"><p class="pt-dw-qp"><span class="pt-dw-qn">Question ${n + 1}</span>${q.prompt}</p>
          <ul class="pt-dw-ans">${q.options.map(function (o, k) {
            var ok = k === q.correct, me = k === q.chosen;
            return html`<li class="${ok ? 'is-right' : me ? 'is-wrong' : ''}"><b>${LETTERS[k]}</b><span>${o}${ok ? html` <span class="pt-dw-tag">Right answer</span>` : ''}${me ? html` <span class="pt-dw-tag pt-dw-tag--you">Your answer</span>` : ''}</span></li>`;
          })}</ul></div>`;
      })}`;
  }

  async function dwClass(el, id) {
    var mine = token();
    view(el, loading('Opening the class…'), false);
    var classes = await run(S.sb.rpc('dawrah_my_classes'));
    if (!mine()) return;
    var i = classes.findIndex(function (c) { return c.id === id; });
    var back = html`<p class="pt-back"><a href="#/dawrah${S.dawrah.admin ? '/mine' : ''}">← All classes</a></p>`;
    if (i < 0) return view(el, html`${back}${empty('This class is not open yet', 'Classes appear on the day they hold.')}`);
    var c = classes[i], prev = classes[i - 1], next = classes[i + 1], qs = [], review = null;
    if (c.questions) {
      if (c.score != null) review = await run(S.sb.rpc('dawrah_review', { lesson: id }));
      else qs = await run(S.sb.rpc('dawrah_questions_for', { lesson: id }));
    }
    if (!mine()) return;
    S.sb.rpc('dawrah_opened', { lesson: id }).then(function () {}, function () {});
    view(el, html`${back}
      <h2 class="pt-h">${dayLabel(c)}: ${c.title}</h2>
      <p class="pt-dw-lede">${fmtDate(c.lesson_date)}</p>
      <section class="pt-card" aria-labelledby="dw-l">
        <h3 id="dw-l"><span class="pt-dw-step" aria-hidden="true">1</span>Listen to the class</h3>
        ${dwPlayer(c.audio_url, c.title)}
        ${c.notes ? html`<p class="pt-dw-notes">${c.notes}</p>` : ''}
      </section>
      ${c.questions ? html`<section class="pt-card" aria-labelledby="dw-a">
        <h3 id="dw-a"><span class="pt-dw-step" aria-hidden="true">2</span>Answer the questions</h3>
        <div id="dw-qbox">${review ? dwReview(review) : dwQuiz(qs, 'Submit my answers', 'You have one try. After you submit, you will see the right answers.')}</div>
      </section>` : ''}
      <nav class="pt-dw-pager" aria-label="Other classes">
        ${prev ? html`<a href="#/dawrah/class/${prev.id}">← ${dayLabel(prev)}</a>` : html`<span></span>`}
        ${next ? html`<a href="#/dawrah/class/${next.id}">${dayLabel(next)} →</a>` : ''}
      </nav>`);
    onSubmit($('#dw-quiz', el), async function (v, form) {
      var a = dwAnswers(form, qs);
      if (a.missing) throw new Error(a.missing === qs.length ? 'Choose an answer for each question.' : 'Answer every question before you submit.');
      var r = await run(S.sb.rpc('dawrah_submit', { lesson: id, answers: a.answers }));
      var byId = {};
      (r.results || []).forEach(function (x) { byId[x.id] = x; });
      var box = $('#dw-qbox', el);
      box.innerHTML = out(dwReview(qs.map(function (q) { return Object.assign({}, q, byId[q.id] || {}); })));
      var s = $('.pt-dw-score', box); if (s) s.focus();
      toast('Your answers are saved.');
    });
  }

  // ------------------------------------------------------------------ student: exam
  async function dwExam(el) {
    var mine = token();
    view(el, loading('Opening the exam…'), false);
    S.dawrah = await run(S.sb.rpc('dawrah_me'));
    var t = dTerm();
    var att = await run(S.sb.from('dawrah_attempts').select('score,total').eq('user_id', S.me.id).eq('term_id', t.id).is('lesson_id', null));
    var qs = !att.length && t.exam_open ? await run(S.sb.rpc('dawrah_questions_for', { lesson: null })) : [];
    if (!mine()) return;
    var back = html`<p class="pt-back"><a href="#/dawrah${S.dawrah.admin ? '/mine' : ''}">← Back to the Dawrah</a></p>`;
    var body = att.length ? html`<section class="pt-card"><p class="pt-dw-score is-full">${icon('check')}<span>You have taken the exam. Your score: <strong>${att[0].score} of ${att[0].total}</strong>.</span></p><p class="pt-meta">If there is a written part, its score is added by the Dawrah team.</p></section>`
      : !t.exam_open ? empty('The exam is not open yet', 'It opens at the end of the Dawrah. You will be told when.')
      : !qs.length ? empty('The exam questions are not ready yet', 'Check back soon.')
      : html`<section class="pt-card">${dwQuiz(qs, 'Submit the exam', 'You have one try, and you cannot change your answers after you submit. Your score shows straight away.')}</section>`;
    view(el, html`${back}<h2 class="pt-h">${t.exam_title}</h2>${body}`);
    onSubmit($('#dw-quiz', el), async function (v, form) {
      var a = dwAnswers(form, qs), btn = $('button[type=submit]', form);
      if (form.dataset.ready !== '1') {
        form.dataset.ready = '1';
        setTimeout(function () { btn.textContent = 'Yes, submit the exam'; }, 0);
        throw new Error(a.missing ? 'You have not answered ' + plural(a.missing, 'question') + '. Press the button again to submit anyway.' : 'Check your answers, then press the button again to submit.');
      }
      var r = await run(S.sb.rpc('dawrah_submit', { lesson: null, answers: a.answers }));
      toast('Your exam is submitted.');
      view(el, html`${back}<h2 class="pt-h">${t.exam_title}</h2><section class="pt-card"><p class="pt-dw-score is-full" tabindex="-1">${icon('check')}<span>Your score: <strong>${r.score} of ${r.total}</strong>. Jazakallahu khairan.</span></p></section>`);
    });
  }

  // ------------------------------------------------------------------ admin: follow-up table
  function dwFollowText(r, missed) {
    var hi = 'Assalamu alaykum ' + (firstName(r.full_name) || '') + ', this is the AMSC Dawrah team. ';
    if (!r.signed_up) return hi + 'You registered for ' + dTerm().title + '. Please create your login on the Student Portal with the same email you registered with (' + r.email + '): ' + portalUrl() + '#/signup/dawrah';
    if (missed) return hi + 'We noticed ' + (missed === 1 ? 'one class has' : missed + ' classes have') + ' not been done on the portal yet. The recordings and questions are here: ' + portalUrl() + '#/dawrah. May Allah make it easy for you.';
    return hi;
  }
  async function dwTracker(el) {
    var mine = token(), t = dTerm();
    view(el, loading('Loading Dawrah students…'), false);
    var res = await Promise.all([run(S.sb.rpc('dawrah_tracker')), run(S.sb.rpc('dawrah_my_classes'))]);
    if (!mine()) return;
    var rows = res[0] || [], today = todayISO();
    var due = (res[1] || []).filter(function (c) { return c.questions > 0 && c.lesson_date <= today; }).length;
    rows.forEach(function (r) {
      r.missed = r.signed_up ? Math.max(0, due - r.classes_done) : due;
      r.state = !r.signed_up ? 'nologin' : r.missed >= 2 ? 'behind' : 'ok';
      r.follow = (!r.signed_up && due > 0) || r.missed >= 2;
    });
    var n = function (f) { return rows.filter(f).length; };
    view(el, html`${dwHead('')}
      <div class="pt-stats">
        <div class="pt-stat"><span class="pt-stat__k">Registered</span><span class="pt-stat__v">${rows.length}</span></div>
        <div class="pt-stat"><span class="pt-stat__k">Have logged in</span><span class="pt-stat__v">${n(function (r) { return r.signed_up; })}</span></div>
        <div class="pt-stat"><span class="pt-stat__k">Up to date</span><span class="pt-stat__v">${n(function (r) { return r.signed_up && !r.missed; })}</span></div>
        <div class="pt-stat"><span class="pt-stat__k">Need follow-up</span><span class="pt-stat__v">${n(function (r) { return r.follow; })}</span></div>
      </div>
      ${rows.length ? html`<div class="pt-filters pt-filters--2" role="search">
          <div class="field"><label for="dw-q">Search</label><input id="dw-q" type="search" placeholder="Name, email or number"></div>
          <div class="field"><label for="dw-f">Show</label><select id="dw-f"><option value="">Everyone</option><option value="follow">Need follow-up</option><option value="nologin">No login yet</option><option value="ok">Up to date</option></select></div>
        </div>
        <div class="pt-headrow"><p class="pt-meta" id="dw-count" aria-live="polite"></p><button type="button" class="pt-textbtn" id="dw-csv">${icon('download')}Download as a spreadsheet (CSV)</button></div>
        <div id="dw-list"></div>`
      : html`<section class="pt-card">${empty('No students yet', 'Copy the registrations from the Google Sheet and paste them in Settings.', html`<a class="btn btn--sm btn--blue" href="#/dawrah/settings">Add registered students</a>`)}</section>`}
      <p class="pt-meta">${due ? plural(due, 'class', 'classes') + ' with questions so far.' : 'No classes with questions yet.'} “Need follow-up” means no login yet, or 2 or more classes not done.</p>`);
    if (!rows.length) return;
    var q = $('#dw-q', el), f = $('#dw-f', el);
    function shown() {
      var s = q.value.trim().toLowerCase();
      return rows.filter(function (r) {
        if (f.value === 'follow' && !r.follow) return false;
        if (f.value && f.value !== 'follow' && r.state !== f.value) return false;
        return !s || ((r.full_name || '') + ' ' + r.email + ' ' + (r.phone || '')).toLowerCase().indexOf(s) >= 0;
      });
    }
    function draw() {
      var list = shown();
      $('#dw-count', el).textContent = 'Showing ' + list.length + ' of ' + plural(rows.length, 'student') + '.';
      $('#dw-list', el).innerHTML = out(list.length ? html`<table class="pt-table"><caption class="sr-only">Dawrah students</caption>
        <thead><tr><th scope="col">Student</th><th scope="col">Classes done</th><th scope="col">Questions right</th><th scope="col">Exam</th><th scope="col">Last active</th><th scope="col"><span class="sr-only">Follow up</span></th></tr></thead>
        <tbody>${list.map(function (r) {
          var wa = waLink(r.phone, dwFollowText(r, r.missed));
          return html`<tr><td data-label="Student"><span class="pt-td"><a href="#/dawrah/student/${encodeURIComponent(r.email)}"><strong>${r.full_name || r.email}</strong></a>
              <span class="pt-meta">${r.email}</span>${r.state === 'nologin' ? pill('No login yet', 'grey') : r.follow ? pill('Follow up', 'yellow') : ''}</span></td>
            <td data-label="Classes done"><span class="pt-td">${r.signed_up ? r.classes_done + ' of ' + due : '—'}</span></td>
            <td data-label="Questions right"><span class="pt-td">${r.quiz_total ? r.quiz_score + ' of ' + r.quiz_total : '—'}</span></td>
            <td data-label="Exam"><span class="pt-td">${r.exam_total != null ? r.exam_score + ' of ' + r.exam_total : '—'}</span></td>
            <td data-label="Last active"><span class="pt-td">${r.last_active ? fmtDate(r.last_active, false) : '—'}</span></td>
            <td><span class="pt-td">${wa ? html`<a class="btn btn--sm btn--line" href="${wa}" target="_blank" rel="noopener">${icon('whatsapp')}WhatsApp<span class="sr-only"> ${r.full_name || r.email}</span></a>` : ''}</span></td></tr>`;
        })}</tbody></table>` : empty('Nobody matches', 'Change the search or the filter.'));
    }
    [q, f].forEach(function (c) { c.addEventListener('input', draw); c.addEventListener('change', draw); });
    draw();
    $('#dw-csv', el).addEventListener('click', function () {
      var cell = function (v) { v = v == null ? '' : String(v); return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
      var lines = [['Name', 'Email', 'WhatsApp', 'Logged in', 'Classes done', 'Classes so far', 'Questions right', 'Questions answered', 'Exam score', 'Exam out of', 'Written score', 'Last active']]
        .concat(shown().map(function (r) {
          return [r.full_name, r.email, r.phone, r.signed_up ? 'Yes' : 'No', r.classes_done, due, r.quiz_score, r.quiz_total, r.exam_score, r.exam_total, r.written_score == null ? '' : Number(r.written_score), r.last_active ? String(r.last_active).slice(0, 10) : ''];
        }));
      var blob = new Blob(['﻿' + lines.map(function (l) { return l.map(cell).join(','); }).join('\r\n')], { type: 'text/csv;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob); a.download = 'dawrah-students-' + todayISO() + '.csv';
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
    });
  }

  // ------------------------------------------------------------------ admin: one student
  async function dwStudent(el, email) {
    var mine = token(), t = dTerm();
    view(el, loading('Loading the student…'), false);
    var res = await Promise.all([run(S.sb.rpc('dawrah_tracker')), run(S.sb.rpc('dawrah_my_classes'))]);
    if (!mine()) return;
    var r = (res[0] || []).find(function (x) { return x.email === email; }), classes = res[1] || [];
    var back = html`<p class="pt-back"><a href="#/dawrah">← All students</a></p>`;
    if (!r) return view(el, html`${back}${empty('Student not found', 'They may have been removed from this Dawrah.')}`);
    var att = [], seen = [];
    if (r.user_id) {
      var more = await Promise.all([
        run(S.sb.from('dawrah_attempts').select('id,lesson_id,score,total,submitted_at').eq('user_id', r.user_id).eq('term_id', t.id)),
        run(S.sb.from('dawrah_views').select('lesson_id,last_at').eq('user_id', r.user_id))
      ]);
      if (!mine()) return;
      att = more[0]; seen = more[1];
    }
    var attFor = function (lid) { return att.find(function (a) { return a.lesson_id === lid; }); };
    var exam = attFor(null);
    var wa = waLink(r.phone, dwFollowText(r, 0));
    view(el, html`${back}
      <h2 class="pt-h">${r.full_name || r.email}</h2>
      <p class="pt-dw-lede">${r.email}${r.phone ? ' · ' + r.phone : ''} ${r.signed_up ? '' : pill('No login yet', 'grey')}</p>
      <div class="pt-actions pt-dw-gap">
        ${wa ? html`<a class="btn btn--sm btn--blue" href="${wa}" target="_blank" rel="noopener">${icon('whatsapp')}WhatsApp</a>` : ''}
        <a class="btn btn--sm btn--line" href="mailto:${r.email}">Email</a>
      </div>
      <div class="pt-grid">
        <section class="pt-card" aria-labelledby="ds-sc">
          <h3 id="ds-sc">${icon('star')}Scores</h3>
          <dl class="pt-dl">
            <div><dt>Classes done</dt><dd>${r.classes_done}</dd></div>
            <div><dt>Questions right</dt><dd>${r.quiz_total ? r.quiz_score + ' of ' + r.quiz_total : '—'}</dd></div>
            <div><dt>${t.exam_title}</dt><dd>${exam ? exam.score + ' of ' + exam.total : 'Not taken'}${exam ? html` <button type="button" class="pt-textbtn" data-reset="${exam.id}">Let them retake it</button>` : ''}</dd></div>
          </dl>
          <form class="form form--plain pt-form" id="ds-w" novalidate>
            <div class="field"><label for="ds-ws">Written exam score <span class="opt">(out of 100, optional)</span></label>
              <input id="ds-ws" name="w" type="number" inputmode="decimal" min="0" max="100" step="0.5" value="${r.written_score == null ? '' : Number(r.written_score)}"></div>
            <p class="form-error" role="alert" tabindex="-1" hidden></p>
            <button class="btn btn--sm btn--blue" type="submit">Save score</button>
          </form>
        </section>
        <section class="pt-card" aria-labelledby="ds-cl">
          <h3 id="ds-cl">${icon('calendar')}Classes</h3>
          ${classes.length ? html`<ul class="pt-rows">${classes.map(function (c) {
            var a = attFor(c.id), v = seen.find(function (x) { return x.lesson_id === c.id; });
            return html`<li><div><strong>${dayLabel(c)}</strong> <span class="pt-meta">${c.title}</span></div>
              <div class="pt-dw-rowend">${a ? pill(a.score + '/' + a.total, 'green') : c.questions ? pill(v ? 'Opened' : 'Not done', v ? 'blue' : 'grey') : pill(v ? 'Listened' : 'Not opened', v ? 'green' : 'grey')}
              ${a ? html`<button type="button" class="pt-textbtn" data-reset="${a.id}">Reset<span class="sr-only"> ${dayLabel(c)}</span></button>` : ''}</div></li>`;
          })}</ul>` : empty('No classes yet', '')}
        </section>
      </div>
      <section class="pt-card pt-danger" aria-labelledby="ds-rm">
        <h3 id="ds-rm">Remove from this Dawrah</h3>
        <p>They will no longer see the Dawrah. Their portal account stays.</p>
        <button type="button" class="btn btn--sm pt-btn-danger" id="ds-remove">Remove ${firstName(r.full_name) || 'student'}</button>
      </section>`);
    onSubmit($('#ds-w', el), async function (v) {
      var w = v.w === '' ? null : Number(v.w);
      if (w !== null && !(w >= 0 && w <= 100)) throw new Error('Enter a score from 0 to 100, or leave it empty.');
      var rows = await run(S.sb.from('dawrah_roster').update({ written_score: w }).eq('term_id', t.id).eq('email', r.email).select('email'));
      if (!rows.length) throw new Error('That score could not be saved.');
      toast('Written score saved.');
    });
    $$('[data-reset]', el).forEach(function (b) {
      b.addEventListener('click', async function () {
        if (b.dataset.confirm !== '1') { b.dataset.confirm = '1'; b.textContent = 'Press again to reset'; return; }
        try {
          var rows = await run(S.sb.from('dawrah_attempts').delete().eq('id', b.dataset.reset).select('id'));
          if (!rows.length) throw new Error('That could not be reset.');
          toast('Reset. They can answer again.'); S.focusNext = false; dwStudent(el, email);
        } catch (e) { toast(friendly(e), 'error'); }
      });
    });
    var rm = $('#ds-remove', el);
    rm.addEventListener('click', async function () {
      if (rm.dataset.confirm !== '1') { rm.dataset.confirm = '1'; rm.textContent = 'Press again to remove'; return; }
      busy(rm, true, 'Removing…');
      try {
        await run(S.sb.from('dawrah_roster').delete().eq('term_id', t.id).eq('email', r.email));
        toast('Removed from the Dawrah.'); go('#/dawrah');
      } catch (e) { busy(rm, false); toast(friendly(e), 'error'); }
    });
  }

  // ------------------------------------------------------------------ admin: classes
  async function dwClasses(el) {
    var mine = token(), t = dTerm();
    view(el, loading('Loading classes…'), false);
    var res = await Promise.all([run(S.sb.rpc('dawrah_my_classes')), run(S.sb.from('dawrah_attempts').select('lesson_id').eq('term_id', t.id))]);
    if (!mine()) return;
    var classes = res[0] || [], answered = {}, today = todayISO();
    res[1].forEach(function (a) { if (a.lesson_id) answered[a.lesson_id] = (answered[a.lesson_id] || 0) + 1; });
    view(el, html`${dwHead('classes')}
      <section class="pt-card" aria-labelledby="dc-h">
        <div class="pt-headrow"><h3 id="dc-h">${icon('calendar')}Classes</h3><a class="btn btn--sm btn--blue" href="#/dawrah/new">${icon('plus')}Add a class</a></div>
        ${classes.length ? html`<ul class="pt-dw-list">${classes.slice().reverse().map(function (c) {
          return html`<li><a href="#/dawrah/edit/${c.id}"><span class="pt-dw-day">${c.day_number}</span>
            <span class="pt-dw-t"><strong>${c.title}</strong><span class="pt-meta">${fmtDate(c.lesson_date, false)} · ${plural(answered[c.id] || 0, 'student')} answered</span></span>
            <span class="pt-dw-pills">${c.lesson_date > today ? pill('Shows ' + fmtDate(c.lesson_date, false), 'grey') : ''}${!c.audio_url ? pill('No recording', 'yellow') : ''}${!c.questions ? pill('No questions', 'yellow') : ''}</span></a></li>`;
        })}</ul>` : empty('No classes yet', 'After each class, add its recording link and two questions here. Students see it straight away.')}
      </section>
      <section class="pt-card" aria-labelledby="dc-how"><h3 id="dc-how">How to add a recording</h3>
        <ol class="pt-steps">
          <li>Upload the audio to Google Drive.</li>
          <li>Right-click it (or tap the three dots), choose <strong>Share</strong>, and set General access to <strong>Anyone with the link</strong>.</li>
          <li>Press <strong>Copy link</strong>, then paste it in the class form here. YouTube links work too.</li>
        </ol>
      </section>`);
  }

  function dwQuestionFields(n, q, locked, label) {
    var o = (q && q.options) || [], pre = 'q' + n;
    if (locked) return html`<div class="pt-dw-q"><p class="pt-dw-qp"><span class="pt-dw-qn">Question ${n}</span>${q.prompt}</p>
      <ul class="pt-dw-ans">${o.map(function (x, k) { return html`<li class="${k === q.correct ? 'is-right' : ''}"><b>${LETTERS[k]}</b><span>${x}${k === q.correct ? html` <span class="pt-dw-tag">Right answer</span>` : ''}</span></li>`; })}</ul></div>`;
    return html`<fieldset class="pt-dw-qedit"><legend>${label || 'Question ' + n}${!label && n > 1 ? html` <span class="opt">(optional)</span>` : ''}</legend>
      <div class="field"><label for="${pre}">Question</label><textarea id="${pre}" name="${pre}" rows="2" maxlength="500">${q ? q.prompt : ''}</textarea></div>
      <p class="pt-meta" id="${pre}-h">Type the answers, then tick the right one. C and D are optional.</p>
      ${[0, 1, 2, 3].map(function (k) {
        return html`<div class="pt-dw-optedit"><label class="pt-dw-right"><input type="radio" name="${pre}c" value="${k}"${raw(q && q.correct === k ? ' checked' : '')} aria-describedby="${pre}-h"><span class="sr-only">Answer ${LETTERS[k]} is the right one</span></label>
          <label for="${pre}o${k}" class="pt-dw-letter"><span class="sr-only">Answer </span>${LETTERS[k]}</label><input id="${pre}o${k}" name="${pre}o${k}" maxlength="200" value="${o[k] || ''}"></div>`;
      })}
    </fieldset>`;
  }
  function dwReadQuestion(v, n) {
    var pre = 'q' + n, prompt = v[pre] || '', opts2 = [], correct = -1;
    [0, 1, 2, 3].forEach(function (k) {
      var x = v[pre + 'o' + k] || '';
      if (x) { if (String(k) === v[pre + 'c']) correct = opts2.length; opts2.push(x); }
    });
    if (!prompt && !opts2.length) return null;
    if (prompt.length < 2) throw new Error('Type question ' + n + '.');
    if (opts2.length < 2) throw new Error('Question ' + n + ' needs at least two answers.');
    if (correct < 0) throw new Error('Tick the right answer for question ' + n + '.');
    return { prompt: prompt, options: opts2, correct: correct };
  }

  async function dwEditClass(el, id) {
    var mine = token(), t = dTerm();
    view(el, loading('Loading…'), false);
    var classes = await run(S.sb.rpc('dawrah_my_classes'));
    var c = id ? classes.find(function (x) { return x.id === id; }) : null, qs = [], answered = 0;
    if (c) {
      var more = await Promise.all([
        run(S.sb.from('dawrah_questions').select('*').eq('lesson_id', id).order('position')),
        count(S.sb.from('dawrah_attempts').select('id', { count: 'exact', head: true }).eq('lesson_id', id))
      ]);
      qs = more[0]; answered = more[1];
    }
    if (!mine()) return;
    var back = html`<p class="pt-back"><a href="#/dawrah/classes">← All classes</a></p>`;
    if (id && !c) return view(el, html`${back}${empty('Class not found', 'It may have been deleted.')}`);
    var locked = answered > 0;
    var nextDay = classes.reduce(function (m, x) { return Math.max(m, x.day_number); }, 0) + 1;
    view(el, html`${back}
      <h2 class="pt-h">${c ? dayLabel(c) + ': ' + c.title : 'Add a class'}</h2>
      <form class="form form--plain pt-form" id="dw-cf" novalidate>
        <section class="pt-card">
          <h3>The class</h3>
          <div class="field--2">
            <div class="field"><label for="cf-day">Day number</label><input id="cf-day" name="day" type="number" min="1" max="300" required value="${c ? c.day_number : nextDay}"></div>
            <div class="field"><label for="cf-date">Date</label><input id="cf-date" name="date" type="date" required value="${c ? c.lesson_date : todayISO()}" aria-describedby="cf-date-h"></div>
          </div>
          <p class="pt-meta" id="cf-date-h">Students see the class from this date.</p>
          <div class="field"><label for="cf-title">What was taught</label><input id="cf-title" name="title" required maxlength="160" value="${c ? c.title : ''}" placeholder="For example: Hadith 1, Actions are by intentions"></div>
          <div class="field"><label for="cf-audio">Recording link <span class="opt">(Google Drive or YouTube)</span></label><input id="cf-audio" name="audio" type="url" inputmode="url" maxlength="500" value="${c && c.audio_url ? c.audio_url : ''}" placeholder="https://drive.google.com/file/d/…"></div>
          <div class="field"><label for="cf-notes">Short note for students <span class="opt">(optional)</span></label><textarea id="cf-notes" name="notes" rows="2" maxlength="600">${c && c.notes ? c.notes : ''}</textarea></div>
        </section>
        <section class="pt-card">
          <h3>Two short questions</h3>
          ${locked ? html`<p class="pt-meta">${plural(answered, 'student has', 'students have')} answered, so these questions are locked to keep scores fair.</p>` : html`<p class="pt-meta">Students answer once and see the right answers after.</p>`}
          ${locked ? qs.map(function (q, i) { return dwQuestionFields(i + 1, q, true); }) : [dwQuestionFields(1, qs[0], false), dwQuestionFields(2, qs[1], false)]}
        </section>
        <p class="form-error" role="alert" tabindex="-1" hidden></p>
        <button class="btn btn--blue" type="submit">${c ? 'Save changes' : 'Add the class'}</button>
      </form>
      ${c ? html`<details class="pt-details pt-dw-gap"><summary>Delete this class</summary>
        <p>This also deletes its questions and every student’s answers to them.</p>
        <button type="button" class="btn btn--sm pt-btn-danger" id="cf-del">Delete ${dayLabel(c)}</button></details>` : ''}`);
    onSubmit($('#dw-cf', el), async function (v) {
      var day = parseInt(v.day, 10);
      if (!(day >= 1 && day <= 300)) throw new Error('Enter the day number (1, 2, 3…).');
      if (!/^\d{4}-\d{2}-\d{2}$/.test(v.date || '')) throw new Error('Choose the date of the class.');
      if ((v.title || '').length < 2) throw new Error('Type what was taught.');
      if (v.audio && !/^https?:\/\//i.test(v.audio)) throw new Error('The recording link must start with https://');
      var newQs = [];
      if (!locked) [1, 2].forEach(function (n) { var q = dwReadQuestion(v, n); if (q) newQs.push(q); });
      var row = { term_id: t.id, day_number: day, lesson_date: v.date, title: v.title, audio_url: v.audio || null, notes: v.notes || null };
      var saved = c ? await run(S.sb.from('dawrah_lessons').update(row).eq('id', c.id).select('id'))
                    : await run(S.sb.from('dawrah_lessons').insert(row).select('id'));
      if (!saved.length) throw new Error('The class could not be saved.');
      var lid = saved[0].id;
      if (!locked) {
        if (c) await run(S.sb.from('dawrah_questions').delete().eq('lesson_id', lid));
        if (newQs.length) await run(S.sb.from('dawrah_questions').insert(newQs.map(function (q, i) {
          return { term_id: t.id, lesson_id: lid, position: i + 1, prompt: q.prompt, options: q.options, correct: q.correct };
        })));
      }
      toast(c ? 'Class saved.' : 'Class added. Students can see it' + (v.date > todayISO() ? ' from ' + fmtDate(v.date, false) + '.' : ' now.'));
      go('#/dawrah/classes');
    });
    var del = $('#cf-del', el);
    if (del) del.addEventListener('click', async function () {
      if (del.dataset.confirm !== '1') { del.dataset.confirm = '1'; del.textContent = 'Press again to delete'; return; }
      busy(del, true, 'Deleting…');
      try {
        var rows = await run(S.sb.from('dawrah_lessons').delete().eq('id', c.id).select('id'));
        if (!rows.length) throw new Error('That class could not be deleted.');
        toast('Class deleted.'); go('#/dawrah/classes');
      } catch (e) { busy(del, false); toast(friendly(e), 'error'); }
    });
  }

  // ------------------------------------------------------------------ admin: exam
  async function dwExamSetup(el) {
    var mine = token(), t0 = dTerm();
    view(el, loading('Loading the exam…'), false);
    var res = await Promise.all([
      run(S.sb.from('dawrah_terms').select('*').eq('id', t0.id)),
      run(S.sb.from('dawrah_questions').select('*').eq('term_id', t0.id).is('lesson_id', null).order('position')),
      count(S.sb.from('dawrah_attempts').select('id', { count: 'exact', head: true }).eq('term_id', t0.id).is('lesson_id', null))
    ]);
    if (!mine()) return;
    var t = res[0][0] || t0, qs = res[1], taken = res[2];
    S.dawrah.term = t;
    view(el, html`${dwHead('exam-setup')}
      <section class="pt-card" aria-labelledby="de-st">
        <div class="pt-headrow"><h3 id="de-st">${icon('shield')}${t.exam_title}</h3>${t.exam_open ? pill('Open', 'green') : pill('Closed', 'grey')}</div>
        <p>${t.exam_open ? 'Students can take the exam now. Each student has one try, and it is marked straight away.' : 'Students cannot see the exam until you open it. Open it at the end of the Dawrah.'}</p>
        <p class="pt-meta">${plural(qs.length, 'question')} · ${plural(taken, 'student has', 'students have')} taken it. Scores show on the Students page.</p>
        <button type="button" class="btn btn--sm ${t.exam_open ? 'btn--line' : 'btn--blue'}" id="de-toggle"${raw(!t.exam_open && !qs.length ? ' disabled' : '')}>${t.exam_open ? 'Close the exam' : 'Open the exam'}</button>
        ${!t.exam_open && !qs.length ? html`<p class="pt-meta">Add questions first.</p>` : ''}
      </section>
      <section class="pt-card" aria-labelledby="de-q">
        <h3 id="de-q">Exam questions</h3>
        ${qs.length ? html`<ol class="pt-dw-examqs">${qs.map(function (q) {
          return html`<li><p class="pt-dw-qp">${q.prompt}</p><ul class="pt-dw-ans">${q.options.map(function (x, k) {
            return html`<li class="${k === q.correct ? 'is-right' : ''}"><b>${LETTERS[k]}</b><span>${x}${k === q.correct ? html` <span class="pt-dw-tag">Right answer</span>` : ''}</span></li>`;
          })}</ul>${taken ? '' : html`<button type="button" class="pt-textbtn pt-textbtn--danger" data-delq="${q.id}">Delete<span class="sr-only"> this question</span></button>`}</li>`;
        })}</ol>` : empty('No exam questions yet', 'Add them below, one at a time.')}
        ${taken ? html`<p class="pt-meta">Students have taken the exam, so questions can no longer be changed.</p>` : html`
        <form class="form form--plain pt-form pt-dw-gap" id="de-add" novalidate>
          ${dwQuestionFields(1, null, false, 'New question')}
          <p class="form-error" role="alert" tabindex="-1" hidden></p>
          <button class="btn btn--sm btn--blue" type="submit">${icon('plus')}Add this question</button>
        </form>`}
      </section>
      <p class="pt-meta">Written part: mark it on paper, then type each student’s score on their page (Students → open a student).</p>`);
    $('#de-toggle', el).addEventListener('click', async function (ev) {
      var b = ev.currentTarget; busy(b, true);
      try {
        await run(S.sb.from('dawrah_terms').update({ exam_open: !t.exam_open }).eq('id', t.id).select('id'));
        toast(t.exam_open ? 'The exam is closed.' : 'The exam is open. Students can take it now.');
        S.focusNext = false; dwExamSetup(el);
      } catch (e) { busy(b, false); toast(friendly(e), 'error'); }
    });
    onSubmit($('#de-add', el), async function (v) {
      var q = dwReadQuestion(v, 1);
      if (!q) throw new Error('Type the question and its answers.');
      var pos = qs.reduce(function (m, x) { return Math.max(m, x.position); }, 0) + 1;
      await run(S.sb.from('dawrah_questions').insert({ term_id: t.id, lesson_id: null, position: pos, prompt: q.prompt, options: q.options, correct: q.correct }));
      toast('Question added.'); S.focusNext = false; dwExamSetup(el);
    });
    $$('[data-delq]', el).forEach(function (b) {
      b.addEventListener('click', async function () {
        if (b.dataset.confirm !== '1') { b.dataset.confirm = '1'; b.textContent = 'Press again to delete'; return; }
        try {
          await run(S.sb.from('dawrah_questions').delete().eq('id', b.dataset.delq));
          toast('Question deleted.'); S.focusNext = false; dwExamSetup(el);
        } catch (e) { toast(friendly(e), 'error'); }
      });
    });
  }

  // ------------------------------------------------------------------ admin: settings
  function parseRoster(text) {
    var EM = /^[^@\s]+@[^@\s]+\.[^@\s]+$/, PH = /^\+?[\d\s()-]{7,}$/, TS = /^\d{1,4}[\/.-]\d{1,2}[\/.-]\d{1,4}/;
    var split = function (l) {
      if (l.indexOf('\t') >= 0) return l.split('\t').map(function (c) { return c.trim(); });
      var cells = [], cur = '', q = false;
      for (var i = 0; i < l.length; i++) {
        var ch = l[i];
        if (q) { if (ch === '"') { if (l[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += ch; }
        else if (ch === '"') q = true; else if (ch === ',') { cells.push(cur.trim()); cur = ''; } else cur += ch;
      }
      cells.push(cur.trim());
      return cells;
    };
    var rows = String(text || '').split(/\r?\n/).filter(function (l) { return l.trim(); }).map(split);
    var iEmail = -1, iNames = [], iPhone = -1, skipped = 0, byEmail = {};
    if (rows.length && !rows[0].some(function (c) { return EM.test(c); })) {
      var head = rows.shift().map(function (h) { return h.toLowerCase(); });
      head.forEach(function (h, i) {
        if (/e-?mail/.test(h)) { if (iEmail < 0) iEmail = i; return; }
        if (/name/.test(h) && !/user ?name|nick/.test(h)) iNames.push(i);
      });
      [/whats/, /phone|tel/, /number/].some(function (re) {
        iPhone = head.findIndex(function (h) { return re.test(h) && !/matric|reg|room|level|e-?mail/.test(h); });
        return iPhone >= 0;
      });
    }
    rows.forEach(function (r) {
      var email = (iEmail >= 0 && EM.test(r[iEmail] || '') ? r[iEmail] : r.find(function (c) { return EM.test(c); }) || '').toLowerCase();
      if (!email) { skipped++; return; }
      var name = iNames.length ? iNames.map(function (i) { return r[i] || ''; }).join(' ').replace(/\s+/g, ' ').trim()
        : (r.find(function (c) { return c && !EM.test(c) && !PH.test(c) && !TS.test(c) && /[a-z]/i.test(c); }) || '');
      var phone = iPhone >= 0 ? r[iPhone] || '' : (r.find(function (c) { return PH.test(c) && !TS.test(c); }) || '');
      byEmail[email] = { email: email, full_name: name.slice(0, 120) || null, phone: phone.slice(0, 30) || null };
    });
    var list = Object.keys(byEmail).map(function (k) { return byEmail[k]; });
    return { list: list, skipped: skipped };
  }

  async function dwSettings(el) {
    var mine = token(), t0 = dTerm();
    view(el, loading('Loading settings…'), false);
    var res = await Promise.all([
      run(S.sb.from('dawrah_terms').select('*').eq('id', t0.id)),
      run(S.sb.from('dawrah_admins').select('*').order('added_at')),
      count(S.sb.from('dawrah_roster').select('email', { count: 'exact', head: true }).eq('term_id', t0.id))
    ]);
    if (!mine()) return;
    var t = res[0][0] || t0, admins = res[1], registered = res[2];
    S.dawrah.term = t;
    view(el, html`${dwHead('settings')}
      <section class="pt-card" aria-labelledby="dst-reg">
        <h3 id="dst-reg">${icon('users')}Add registered students</h3>
        <p><strong>${plural(registered, 'student')}</strong> registered so far.</p>
        <ol class="pt-steps">
          <li>Open the Google Sheet of the registration form’s responses.</li>
          <li>Select the rows, including the top (header) row, and copy them.</li>
          <li>Paste them below and press <strong>Add students</strong>. Pasting the same people again is safe.</li>
        </ol>
        <form class="form form--plain pt-form" id="dst-paste" novalidate>
          <div class="field"><label for="dst-rows">Paste here</label><textarea id="dst-rows" name="rows" rows="5" placeholder="Or type one per line: email, full name, WhatsApp number"></textarea></div>
          <p class="form-error" role="alert" tabindex="-1" hidden></p>
          <button class="btn btn--blue" type="submit">Add students</button>
        </form>
        <p class="pt-meta">Each student then creates a portal login with the same email they registered with, and the Dawrah opens for them.</p>
      </section>
      <div class="pt-grid">
        <section class="pt-card" aria-labelledby="dst-det">
          <h3 id="dst-det">Dawrah details</h3>
          <form class="form form--plain pt-form" id="dst-term" novalidate>
            <div class="field"><label for="dt-title">Name</label><input id="dt-title" name="title" required maxlength="160" value="${t.title}"></div>
            <div class="field"><label for="dt-sch">Days and time</label><input id="dt-sch" name="schedule" maxlength="200" value="${t.schedule || ''}" placeholder="For example: Mon, Wed and Fri, between Maghrib and Isha"></div>
            <div class="field"><label for="dt-ven">Venue</label><input id="dt-ven" name="venue" maxlength="120" value="${t.venue || ''}"></div>
            <div class="field"><label for="dt-book">Book link <span class="opt">(PDF; leave empty for “coming soon”)</span></label><input id="dt-book" name="book_url" maxlength="500" value="${t.book_url || ''}" placeholder="https://drive.google.com/…"></div>
            <div class="field"><label for="dt-exam">Exam name</label><input id="dt-exam" name="exam_title" required maxlength="120" value="${t.exam_title}"></div>
            <p class="form-error" role="alert" tabindex="-1" hidden></p>
            <button class="btn btn--blue" type="submit">Save details</button>
          </form>
        </section>
        <section class="pt-card" aria-labelledby="dst-adm">
          <h3 id="dst-adm">${icon('shield')}Dawrah admins</h3>
          <p class="pt-meta">They can add classes, see every student and follow up. Portal admins are always included.</p>
          ${admins.length ? html`<ul class="pt-rows">${admins.map(function (a) {
            return html`<li><div><strong>${a.full_name || a.email || 'Admin'}</strong><span class="pt-meta">${a.email || ''}</span></div>
              <button type="button" class="pt-textbtn pt-textbtn--danger" data-deladm="${a.user_id}">Remove<span class="sr-only"> ${a.full_name || ''}</span></button></li>`;
          })}</ul>` : html`<p>No extra admins yet.</p>`}
          <form class="form form--plain pt-form" id="dst-addadm" novalidate>
            <div class="field"><label for="da-email">Add an admin by email</label><input id="da-email" name="email" type="email" required autocomplete="off" aria-describedby="da-h"></div>
            <p class="pt-meta" id="da-h">They must create a portal account with this email first.</p>
            <p class="form-error" role="alert" tabindex="-1" hidden></p>
            <button class="btn btn--sm btn--blue" type="submit">Add admin</button>
          </form>
        </section>
      </div>
      <details class="pt-details"><summary>Start the next Dawrah</summary>
        <p>When this Dawrah is over, start the next one here. This Dawrah’s students, classes and scores are kept, but students will no longer see them. You will then add the new registrations.</p>
        <form class="form form--plain pt-form" id="dst-new" novalidate>
          <div class="field"><label for="dn-title">Name of the next Dawrah</label><input id="dn-title" name="title" required maxlength="160"></div>
          <p class="form-error" role="alert" tabindex="-1" hidden></p>
          <button class="btn btn--sm pt-btn-danger" type="submit">Start the next Dawrah</button>
        </form>
      </details>`);
    onSubmit($('#dst-paste', el), async function (v, form) {
      var p = parseRoster(v.rows);
      if (!p.list.length) throw new Error('No email addresses found. Copy the rows from the sheet, including the email column.');
      await run(S.sb.from('dawrah_roster').upsert(p.list.map(function (r) {
        return { term_id: t.id, email: r.email, full_name: r.full_name, phone: r.phone };
      }), { onConflict: 'term_id,email' }));
      form.reset();
      toast(plural(p.list.length, 'student') + ' added or updated.' + (p.skipped ? ' ' + plural(p.skipped, 'line') + ' without an email skipped.' : ''));
      S.focusNext = false; dwSettings(el);
    });
    onSubmit($('#dst-term', el), async function (v) {
      if ((v.title || '').length < 2) throw new Error('Enter the name of the Dawrah.');
      if ((v.exam_title || '').length < 2) throw new Error('Enter the exam name.');
      if (v.book_url && !/^(https?:\/\/|assets\/)/i.test(v.book_url)) throw new Error('The book link must start with https://');
      var rows = await run(S.sb.from('dawrah_terms').update({ title: v.title, schedule: v.schedule || null, venue: v.venue || null, book_url: v.book_url || null, exam_title: v.exam_title }).eq('id', t.id).select('*'));
      if (!rows.length) throw new Error('The details could not be saved.');
      S.dawrah.term = rows[0];
      toast('Dawrah details saved.'); S.focusNext = false; dwSettings(el);
    });
    onSubmit($('#dst-addadm', el), async function (v) {
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email || '')) throw new Error('Enter a valid email address.');
      var name = await run(S.sb.rpc('dawrah_add_admin', { admin_email: v.email }));
      toast((name || v.email) + ' is now a Dawrah admin.'); S.focusNext = false; dwSettings(el);
    });
    $$('[data-deladm]', el).forEach(function (b) {
      b.addEventListener('click', async function () {
        if (b.dataset.confirm !== '1') { b.dataset.confirm = '1'; b.textContent = 'Press again to remove'; return; }
        try {
          await run(S.sb.from('dawrah_admins').delete().eq('user_id', b.dataset.deladm));
          toast('Admin removed.');
          if (b.dataset.deladm === S.me.id) { S.dawrah = await run(S.sb.rpc('dawrah_me')); return route(); }
          S.focusNext = false; dwSettings(el);
        } catch (e) { toast(friendly(e), 'error'); }
      });
    });
    onSubmit($('#dst-new', el), async function (v, form) {
      if ((v.title || '').length < 2) throw new Error('Enter the name of the next Dawrah.');
      if (form.dataset.ready !== '1') { form.dataset.ready = '1'; throw new Error('Are you sure? Press “Start the next Dawrah” again to confirm.'); }
      await run(S.sb.from('dawrah_terms').update({ is_current: false }).eq('id', t.id).select('id'));
      try {
        await run(S.sb.from('dawrah_terms').insert({ title: v.title, schedule: t.schedule, venue: t.venue, exam_title: 'Final exam', is_current: true }));
      } catch (e) {
        await S.sb.from('dawrah_terms').update({ is_current: true }).eq('id', t.id);
        throw e;
      }
      S.dawrah = await run(S.sb.rpc('dawrah_me'));
      toast('The next Dawrah has started. Add its registrations now.');
      go('#/dawrah/settings');
    });
  }

  // ===================================================================== admin
  async function viewAdmin(el) {
    var mine = token();
    view(el, loading('Loading the overview…'), false);
    var c = function (q) { return count(q); };
    var res = await Promise.all([
      run(S.sb.from('profiles').select('*').eq('status', 'pending').eq('joins_islamiyyah', true).order('created_at')),
      c(S.sb.from('profiles').select('id', { count: 'exact', head: true }).eq('status', 'active').eq('role', 'student')),
      c(S.sb.from('profiles').select('id', { count: 'exact', head: true }).eq('status', 'active').eq('role', 'teacher')),
      c(S.sb.from('profiles').select('id', { count: 'exact', head: true }).eq('status', 'active').eq('role', 'student').or('quran_group.is.null,arabic_group.is.null'))
    ]);
    if (!mine()) return;
    var pend = res[0];
    var stat = function (k, v, href) { return html`<a class="pt-stat pt-stat--link" href="${href}"><span class="pt-stat__k">${k}</span><span class="pt-stat__v">${fmtNum(v)}</span></a>`; };
    view(el, html`
      <h2 class="pt-h">Islamiyyah overview</h2>
      <div class="pt-stats">
        ${stat('Waiting for approval', pend.length, '#/members?status=pending')}
        ${stat('Active students', res[1], '#/members?status=active')}
        ${stat('Teachers', res[2], '#/members?role=teacher')}
        ${stat('Not yet in a class', res[3], '#/members?nogroup=1')}
      </div>
      <section class="pt-card" aria-labelledby="a-pend"><h3 id="a-pend">${icon('bell')}Waiting for approval</h3>
        ${pend.length ? html`<ul class="pt-rows">${pend.map(function (p) {
          return html`<li><div><strong>${p.full_name}</strong><span class="pt-meta">${p.email} · ${p.wing ? WING[p.wing] : 'Class not chosen'}${p.department ? ' · ' + p.department : ''}${p.level ? ', ' + p.level : ''} · signed up ${fmtDate(p.created_at, false)}</span></div>
            <a class="btn btn--sm btn--blue" href="#/member/${p.id}">Review<span class="sr-only"> ${p.full_name}</span></a></li>`;
        })}</ul>` : empty('Nobody is waiting', 'New Islamiyyah sign-ups appear here. Dawrah sign-ups go to the Dawrah list instead.')}
      </section>
      <details class="pt-details pt-card"><summary>How the Islamiyyah portal runs</summary>
        <ol class="pt-steps">
          <li>Students create their own accounts at <strong>${location.host}${location.pathname}</strong>.</li>
          <li>You approve each one and set their Qur’an and Arabic levels and classes.</li>
          <li>Create classes in <a href="#/groups">Groups</a> and assign teachers. To make someone a teacher, open their account in Members and set the role to Teacher.</li>
          <li>Teachers verify Qur’an records, add assessments and update Arabic class progress.</li>
          <li>If someone forgets their password, open their account and set a temporary password.</li>
        </ol></details>`);
  }

  async function viewMembers(el) {
    var mine = token();
    view(el, loading('Loading members…'), false);
    var res = await Promise.all([run(S.sb.from('profiles').select('*').order('created_at', { ascending: false })), run(S.sb.from('groups').select('id,name,track'))]);
    if (!mine()) return;
    var all = res[0], gname = {};
    res[1].forEach(function (g) { gname[g.id] = g.name; });
    var qs = new URLSearchParams((location.hash.split('?')[1]) || '');
    view(el, html`
      <h2 class="pt-h">Members</h2>
      <div class="pt-filters" role="search">
        <div class="field"><label for="m-q">Search</label><input id="m-q" type="search" placeholder="Name, email or department"></div>
        <div class="field"><label for="m-st">Status</label><select id="m-st"><option value="">Any status</option>${opts(STATUS, qs.get('status') || '')}</select></div>
        <div class="field"><label for="m-ro">Role</label><select id="m-ro"><option value="">Any role</option>${opts(ROLE, qs.get('role') || '')}<option value="staff"${raw(qs.get('role') === 'staff' ? ' selected' : '')}>Teachers and admins</option></select></div>
        <div class="field"><label for="m-wi">Class</label><select id="m-wi"><option value="">Brothers and sisters</option><option value="brothers">Brothers</option><option value="sisters">Sisters</option></select></div>
      </div>
      <label class="pt-consent pt-consent--inline"><input type="checkbox" id="m-ng"${raw(qs.get('nogroup') ? ' checked' : '')}><span>Only students not yet in a class</span></label>
      <label class="pt-consent pt-consent--inline"><input type="checkbox" id="m-dw"><span>Include Dawrah-only accounts</span></label>
      <p class="pt-meta" id="m-count" aria-live="polite"></p>
      <div id="m-list"></div>`);
    var q = $('#m-q', el), st = $('#m-st', el), ro = $('#m-ro', el), wi = $('#m-wi', el), ng = $('#m-ng', el), dw = $('#m-dw', el);
    var dawrahSide = function (p) { return !p.joins_islamiyyah && p.status === 'pending'; };
    function draw() {
      var t = q.value.trim().toLowerCase();
      var shown = all.filter(function (p) {
        if (st.value && p.status !== st.value) return false;
        if (ro.value === 'staff' ? p.role === 'student' : ro.value && p.role !== ro.value) return false;
        if (wi.value && p.wing !== wi.value) return false;
        if (ng.checked && ((p.quran_group && p.arabic_group) || p.role !== 'student' || p.status !== 'active')) return false;
        if (!dw.checked && dawrahSide(p)) return false;
        if (t && (p.full_name + ' ' + p.email + ' ' + (p.department || '')).toLowerCase().indexOf(t) < 0) return false;
        return true;
      });
      var total = dw.checked ? all.length : all.filter(function (p) { return !dawrahSide(p); }).length;
      $('#m-count', el).textContent = 'Showing ' + shown.length + ' of ' + plural(total, 'member') + '.';
      $('#m-list', el).innerHTML = out(shown.length ? html`<table class="pt-table"><caption class="sr-only">Portal members</caption>
        <thead><tr><th scope="col">Name</th><th scope="col">Status</th><th scope="col">Role</th><th scope="col">Qur’an group</th><th scope="col">Arabic group</th><th scope="col"><span class="sr-only">Open</span></th></tr></thead>
        <tbody>${shown.map(function (p) {
          return html`<tr><td data-label="Name"><span class="pt-td"><strong>${p.full_name}</strong><span class="pt-meta">${p.email}${p.wing ? ' · ' + WING[p.wing] : ''}</span>${dawrahSide(p) ? pill('Dawrah only', 'blue') : ''}</span></td>
            <td data-label="Status"><span class="pt-td">${statusPill(p.status)}</span></td><td data-label="Role"><span class="pt-td">${ROLE[p.role]}</span></td>
            <td data-label="Qur’an group"><span class="pt-td">${p.quran_group ? gname[p.quran_group] : '—'}</span></td><td data-label="Arabic group"><span class="pt-td">${p.arabic_group ? gname[p.arabic_group] : '—'}</span></td>
            <td><a class="btn btn--sm btn--line" href="#/member/${p.id}">Open<span class="sr-only"> ${p.full_name}</span></a></td></tr>`;
        })}</tbody></table>` : empty('No members match', 'Change the search or filters.'));
    }
    [q, st, ro, wi, ng, dw].forEach(function (c2) { c2.addEventListener('input', draw); c2.addEventListener('change', draw); });
    draw();
  }

  function tempPassword() {
    var words = ['Iqra', 'Noor', 'Sabr', 'Huda', 'Ilm', 'Taqwa', 'Barakah', 'Ihsan'];
    var a = new Uint32Array(2);
    (window.crypto || {}).getRandomValues ? crypto.getRandomValues(a) : (a[0] = Date.now(), a[1] = Math.random() * 1e9);
    return words[a[0] % words.length] + '-' + String(1000 + (a[1] % 9000));
  }

  async function viewMember(el, args) {
    var id = args[0], mine = token();
    view(el, loading('Loading the account…'), false);
    var res = await Promise.all([run(S.sb.from('profiles').select('*').eq('id', id).maybeSingle()), run(S.sb.from('groups').select('*').order('name'))]);
    if (!mine()) return;
    var p = res[0], groups = res[1];
    if (!p) return view(el, html`<h2 class="pt-h">Account not found</h2>${empty('This account no longer exists', '', html`<a class="btn btn--sm btn--blue" href="#/members">Back to members</a>`)}`);
    var self = p.id === S.me.id;
    var gOpts = function (track, sel) {
      return [html`<option value="">Not placed</option>`].concat(groups.filter(function (g) { return g.track === track; }).map(function (g) {
        return html`<option value="${g.id}"${raw(g.id === sel ? ' selected' : '')}>${g.name} (${(track === 'quran' ? QLEVEL : LEVEL)[g.level]}, ${WING[g.wing]})</option>`;
      }));
    };
    view(el, html`
      <p class="pt-back"><a href="#/members">← All members</a></p>
      <div class="pt-headrow"><h2 class="pt-h">${p.full_name}</h2>${statusPill(p.status)}</div>
      <p class="pt-meta">${p.email}${p.phone ? ' · ' + p.phone : ''}${p.department ? ' · ' + p.department : ''}${p.level ? ', ' + p.level : ''} · joined ${fmtDate(p.created_at)}${p.consent_at ? ' · consent given' : ' · no consent recorded'}</p>
      ${!p.joins_islamiyyah && p.status === 'pending' ? html`<p class="pt-alert pt-alert--info">${icon('alert')}<span>${firstName(p.full_name)} signed up for the Dawrah only. Approving them here also adds them to the Islamiyyah.</span></p>` : ''}
      <div class="pt-grid">
        <section class="pt-card pt-card--wide" aria-labelledby="m-edit"><h3 id="m-edit">Approval, class and role</h3>
          <form class="form form--plain pt-form" id="f-member" novalidate>
            <div class="field--2">
              <div class="field"><label for="mm-status">Status</label><select id="mm-status" name="status"${raw(self ? ' disabled' : '')}>${opts(STATUS, p.status)}</select></div>
              <div class="field"><label for="mm-role">Role</label><select id="mm-role" name="role"${raw(self ? ' disabled' : '')}>${opts(ROLE, p.role)}</select></div>
            </div>
            <div class="field"><label for="mm-wing">Class</label><select id="mm-wing" name="wing"><option value="">Not set</option>${opts({ brothers: 'Brothers', sisters: 'Sisters' }, p.wing)}</select></div>
            <div class="field--2">
              <div class="field"><label for="mm-ql">Qur’an level</label><select id="mm-ql" name="quran_level">${opts(QLEVEL, p.quran_level, 'Not assigned')}</select></div>
              <div class="field"><label for="mm-qg">Qur’an group</label><select id="mm-qg" name="quran_group">${gOpts('quran', p.quran_group)}</select></div>
            </div>
            <div class="field--2">
              <div class="field"><label for="mm-al">Arabic level</label><select id="mm-al" name="arabic_level">${opts(LEVEL, p.arabic_level, 'Not assigned')}</select></div>
              <div class="field"><label for="mm-ag">Arabic group</label><select id="mm-ag" name="arabic_group">${gOpts('arabic', p.arabic_group)}</select></div>
            </div>
            <div class="field"><label for="mm-subj">Subjects taught <span class="opt">(teachers)</span></label><input id="mm-subj" name="subjects" maxlength="200" value="${p.subjects || ''}"></div>
            ${self ? html`<p class="pt-meta">You cannot change your own status or role. Another admin can.</p>` : ''}
            <p class="form-error" role="alert" tabindex="-1" hidden></p>
            <div class="pt-actions"><button class="btn btn--blue" type="submit">${p.status === 'pending' ? 'Save and approve' : 'Save changes'}</button>
              <a class="btn btn--line" href="#/student/${p.id}?from=admin">Qur’an record</a></div>
          </form></section>
        <section class="pt-card" aria-labelledby="m-pw"><h3 id="m-pw">${icon('shield')}Forgotten password</h3>
          <p>Set a temporary password and send it to ${firstName(p.full_name)}. The portal will ask them to choose a new one when they log in.</p>
          <form class="form form--plain pt-form" id="f-temp" novalidate>
            <div class="field"><label for="tp">Temporary password</label><input id="tp" name="pw" required minlength="8" value="${tempPassword()}" autocomplete="off"></div>
            <p class="form-error" role="alert" tabindex="-1" hidden></p>
            <button class="btn btn--blue" type="submit">Set temporary password</button>
          </form>
          <div id="tp-done"></div></section>
        ${self ? '' : html`<section class="pt-card pt-danger" aria-labelledby="m-del"><h3 id="m-del">${icon('trash')}Delete account</h3>
          <p>This permanently deletes ${firstName(p.full_name)}’s account, Qur’an records and assessments. To keep the records, set the status to Inactive instead.</p>
          <form class="form form--plain pt-form" id="f-del" novalidate>
            <div class="field"><label for="del-name">Type <strong>${p.full_name}</strong> to confirm</label><input id="del-name" name="name" autocomplete="off" required></div>
            <p class="form-error" role="alert" tabindex="-1" hidden></p>
            <button class="btn pt-btn-danger" type="submit">Delete permanently</button>
          </form></section>`}
      </div>`);
    onSubmit($('#f-member', el), async function (v) {
      var row = {
        wing: v.wing || null, quran_level: v.quran_level || null, quran_group: v.quran_group || null,
        arabic_level: v.arabic_level || null, arabic_group: v.arabic_group || null, subjects: v.subjects || null
      };
      if (!self) { row.status = v.status === 'pending' && p.status === 'pending' ? 'active' : v.status; row.role = v.role; }
      if (row.status === 'active') row.joins_islamiyyah = true;
      var rows = await run(S.sb.from('profiles').update(row).eq('id', p.id).select('*'));
      if (!rows.length) throw new Error('The account could not be updated.');
      toast(p.status === 'pending' && rows[0].status === 'active' ? firstName(p.full_name) + ' is approved.' : 'Changes saved.');
      if (self) await loadMe();
      S.focusNext = false; viewMember(el, args);
    });
    onSubmit($('#f-temp', el), async function (v) {
      if ((v.pw || '').length < 8) throw new Error('The temporary password must be at least 8 characters.');
      await run(S.sb.rpc('admin_set_password', { target: p.id, new_password: v.pw }));
      var msg = 'Assalamu alaykum ' + firstName(p.full_name) + '. Your AMSC Islamiyyah portal temporary password is: ' + v.pw + '\nLog in at ' + location.origin + location.pathname + ' and you will be asked to choose a new password.';
      var wa = waLink(p.phone, msg);
      $('#tp-done', el).innerHTML = out(html`<div class="pt-done" role="status">${icon('check')}<div><p>Temporary password set: <strong class="pt-code">${v.pw}</strong></p>
        ${wa ? html`<a class="btn btn--sm btn--blue" href="${wa}" target="_blank" rel="noopener">${icon('whatsapp')}Send on WhatsApp<span class="sr-only"> (opens WhatsApp)</span></a>` : html`<p class="pt-meta">No phone number on this account. Send the password to them privately.</p>`}</div></div>`);
      announce('Temporary password set.');
    });
    var fd = $('#f-del', el);
    if (fd) onSubmit(fd, async function (v) {
      if (v.name !== p.full_name) throw new Error('Type the full name exactly as shown to confirm.');
      await run(S.sb.rpc('admin_delete_user', { target: p.id }));
      toast('Account deleted.'); go('#/members');
    });
  }

  async function viewGroups(el) {
    var mine = token();
    view(el, loading('Loading groups…'), false);
    var res = await Promise.all([
      run(S.sb.from('groups').select('*').order('track').order('level').order('name')),
      run(S.sb.from('group_teachers').select('*')),
      run(S.sb.from('profiles').select('id,full_name,role,status,wing,quran_group,arabic_group').order('full_name'))
    ]);
    if (!mine()) return;
    var groups = res[0], links = res[1], people = res[2];
    var staff = people.filter(function (p) { return p.status === 'active' && p.role !== 'student'; });
    var nameOf = {}; people.forEach(function (p) { nameOf[p.id] = p.full_name; });
    var teachersOf = function (gid) { return links.filter(function (l) { return l.group_id === gid; }).map(function (l) { return l.teacher_id; }); };
    var size = function (g) { return people.filter(function (p) { return p.status === 'active' && (p.quran_group === g.id || p.arabic_group === g.id); }).length; };
    var groupForm = function (g) {
      var id = g ? g.id : 'new', tids = g ? teachersOf(g.id) : [];
      return html`<form class="form form--plain pt-form" data-group="${id}" novalidate>
        <div class="field"><label for="gn-${id}">Group name</label><input id="gn-${id}" name="name" required maxlength="80" value="${g ? g.name : ''}" placeholder="For example: Qur’an Beginners (Brothers)"></div>
        <div class="field--2">
          <div class="field"><label for="gt-${id}">Area</label><select id="gt-${id}" name="track"${raw(g ? ' disabled' : '')}>${opts({ quran: 'Qur’an', arabic: 'Arabic' }, g ? g.track : 'quran')}</select></div>
          <div class="field"><label for="gl-${id}">Level</label><select id="gl-${id}" name="level">${opts(g && g.track === 'arabic' ? LEVEL : QLEVEL, g ? g.level : 'beginner')}</select></div>
        </div>
        <div class="field"><label for="gw-${id}">Who attends</label><select id="gw-${id}" name="wing">${opts(WING, g ? g.wing : 'brothers')}</select></div>
        ${g && g.track === 'arabic' ? html`<fieldset class="field pt-fieldset"><legend>Class progress <span class="opt">(teachers can also update this)</span></legend>
          <div class="field"><label for="gb-${id}">Book</label><input id="gb-${id}" name="book" maxlength="120" value="${g.book || ''}" placeholder="For example: Durus al-Lughah, Book 1"></div>
          <div class="field--2">
            <div class="field"><label for="gc-${id}">Lessons completed</label><input id="gc-${id}" name="current_lesson" type="number" inputmode="numeric" min="0" max="200" value="${g.current_lesson == null ? '' : g.current_lesson}"></div>
            <div class="field"><label for="gtl-${id}">Lessons in the book</label><input id="gtl-${id}" name="total_lessons" type="number" inputmode="numeric" min="1" max="200" value="${g.total_lessons || ''}"></div>
          </div></fieldset>` : ''}
        ${g ? html`<fieldset class="field pt-choice pt-choice--list"><legend>Teachers</legend>${staff.length ? staff.map(function (t) {
          return html`<label><input type="checkbox" name="t" value="${t.id}"${raw(tids.indexOf(t.id) >= 0 ? ' checked' : '')}> ${t.full_name} <span class="pt-meta">(${ROLE[t.role]}${t.wing ? ', ' + WING[t.wing] : ''})</span></label>`;
        }) : html`<p class="pt-meta">No teachers yet. Open a member in Members and set their role to Teacher.</p>`}</fieldset>` : ''}
        <p class="form-error" role="alert" tabindex="-1" hidden></p>
        <div class="pt-actions"><button class="btn btn--blue btn--sm" type="submit">${g ? 'Save group' : 'Create group'}</button>
        ${g ? html`<button type="button" class="pt-textbtn pt-textbtn--danger" data-del-group="${g.id}">Delete group</button>` : ''}</div>
      </form>`;
    };
    var section = function (track, title) {
      var gs = groups.filter(function (g) { return g.track === track; });
      return html`<section class="pt-card pt-card--wide" aria-labelledby="gs-${track}"><h3 id="gs-${track}">${title}</h3>
        ${gs.length ? html`<ul class="pt-groups">${gs.map(function (g) {
          var t = teachersOf(g.id).map(function (x) { return nameOf[x]; }).filter(Boolean);
          return html`<li class="pt-groupitem"><details><summary><span><strong>${g.name}</strong><span class="pt-meta">${(track === 'quran' ? QLEVEL : LEVEL)[g.level]} · ${WING[g.wing]} · ${plural(size(g), 'student')} · ${t.length ? t.join(', ') : 'no teacher yet'}</span></span><span class="pt-edit">Edit</span></summary>
            ${groupForm(g)}</details></li>`;
        })}</ul>` : empty('No ' + title.toLowerCase() + ' yet', 'Create one with the form above.')}
      </section>`;
    };
    view(el, html`
      <h2 class="pt-h">Groups and teachers</h2>
      <section class="pt-card" aria-labelledby="g-new"><h3 id="g-new">${icon('plus')}Create a group</h3>
        <p class="pt-meta">The committee document sets three levels for each area: Beginner, Intermediate and Advanced (Hifz for Qur’an).</p>
        ${groupForm(null)}</section>
      ${section('quran', 'Qur’an groups')}
      ${section('arabic', 'Arabic groups')}`);
    var reload = function () { S.focusNext = false; viewGroups(el); };
    $$('[data-group]', el).forEach(function (f) {
      onSubmit(f, async function (v, form) {
        if (!v.name || v.name.length < 2) throw new Error('Enter a group name.');
        var gid = form.dataset.group;
        if (gid === 'new') {
          await run(S.sb.from('groups').insert({ name: v.name, track: v.track, level: v.level, wing: v.wing }));
          toast('Group created.'); return reload();
        }
        var upd = { name: v.name, level: v.level, wing: v.wing };
        if ('current_lesson' in v) {
          var cl = v.current_lesson === '' ? null : parseInt(v.current_lesson, 10), tl = v.total_lessons === '' ? null : parseInt(v.total_lessons, 10);
          if (cl !== null && !(cl >= 0 && cl <= 200)) throw new Error('Lessons completed must be a number from 0 to 200.');
          if (tl !== null && !(tl >= 1 && tl <= 200)) throw new Error('Lessons in the book must be a number from 1 to 200.');
          if (cl !== null && tl !== null && cl > tl) throw new Error('Lessons completed cannot be more than the lessons in the book.');
          var g0 = groups.find(function (x) { return x.id === gid; });
          upd.book = v.book || null; upd.total_lessons = tl; upd.current_lesson = cl;
          if (cl !== g0.current_lesson || tl !== g0.total_lessons || (v.book || null) !== (g0.book || null)) upd.progress_at = new Date().toISOString();
        }
        var rows = await run(S.sb.from('groups').update(upd).eq('id', gid).select('id'));
        if (!rows.length) throw new Error('The group could not be saved.');
        var want = $$('[name=t]:checked', form).map(function (c) { return c.value; });
        var have = teachersOf(gid);
        var add = want.filter(function (x) { return have.indexOf(x) < 0; });
        var drop = have.filter(function (x) { return want.indexOf(x) < 0; });
        if (add.length) await run(S.sb.from('group_teachers').insert(add.map(function (t) { return { group_id: gid, teacher_id: t }; })));
        if (drop.length) await run(S.sb.from('group_teachers').delete().eq('group_id', gid).in('teacher_id', drop));
        toast('Group saved.'); reload();
      });
    });
    $$('[data-del-group]', el).forEach(function (b) {
      b.addEventListener('click', async function () {
        if (b.dataset.confirm !== '1') { b.dataset.confirm = '1'; b.textContent = 'Press again to delete. Students stay, but leave the group.'; return; }
        try {
          var rows = await run(S.sb.from('groups').delete().eq('id', b.dataset.delGroup).select('id'));
          if (!rows.length) throw new Error('The group could not be deleted.');
          toast('Group deleted.'); reload();
        } catch (e) { toast(friendly(e), 'error'); }
      });
    });
  }

  // ===================================================================== start
  function bootFailed(e) {
    root.innerHTML = out(html`<div class="pt-auth"><div class="pt-auth__card"><p class="pt-auth__kicker">AMSC Student Portal</p>
      <h2>The portal did not open</h2>${errorBox(e)}<a class="btn btn--blue pt-wide" href="">Refresh the page</a>${helpLink('Tell the Islamiyyah admin on WhatsApp')}</div></div>`);
    root.setAttribute('aria-busy', 'false');
    if (window.console) console.error('[portal]', e);
  }
  async function boot() {
    if (!DATA) return bootFailed(new Error('A portal file did not load. Check your connection and refresh the page.'));
    if (!CFG.supabaseUrl || !CFG.supabaseKey) return viewNotReady();
    if (!window.supabase || !window.supabase.createClient) return bootFailed(new Error('A portal file did not load. Check your connection and refresh the page.'));
    S.sb = window.supabase.createClient(CFG.supabaseUrl.trim(), CFG.supabaseKey.trim(), {
      auth: {
        persistSession: true, autoRefreshToken: true, detectSessionInUrl: true, storageKey: 'amsc-portal-auth',
        // Run auth steps directly instead of through the browser's cross-tab lock, which can
        // stall on some browsers and leave the page loading forever.
        lock: function (name, acquireTimeout, fn) { return fn(); }
      }
    });
    S.sb.auth.onAuthStateChange(function (event, session) {
      if (event === 'PASSWORD_RECOVERY') {
        S.recovery = true;
        setTimeout(async function () { S.user = session && session.user; if (S.user) { try { await loadMe(); } catch (e) { /* shown later */ } } go('#/reset'); }, 0);
      } else if (event === 'SIGNED_OUT' && S.user) {
        S.user = null; S.me = null;
        setTimeout(function () { go('#/login'); }, 0);
      }
    });
    window.addEventListener('hashchange', function () { route(); });
    try {
      // A saved session is read from this browser; if that ever stalls, start signed out.
      var s = await Promise.race([
        run(S.sb.auth.getSession()),
        new Promise(function (resolve) { setTimeout(function () { resolve({ session: null }); }, 8000); })
      ]);
      S.user = s.session ? s.session.user : null;
      if (S.user) await loadMe();
    } catch (e) {
      return bootFailed(e);
    }
    S.focusNext = false;
    route();
  }
  // Nothing on screen after 20 seconds means something is stuck: say so instead of spinning.
  setTimeout(function () {
    if (root.getAttribute('aria-busy') === 'true') bootFailed(new Error('The portal is taking too long to start. Check your internet connection and refresh the page.'));
  }, 20000);
  boot().catch(bootFailed);
})();
