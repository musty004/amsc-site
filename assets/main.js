/* AMSC — shared behaviour
   1. Mobile navigation
   2. Prayer times for Kaduna (AlAdhan API, cached for the day, offline fallback)
   3. Share and print buttons (Freshers' guide)
   4. Clearance checklist that remembers ticks on this device
*/

/* ---------- 1. navigation ---------- */
(function () {
  var btn = document.querySelector('.navtoggle');
  var nav = document.getElementById('primary-nav');
  if (!btn || !nav) return;
  function set(open) {
    nav.classList.toggle('is-open', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  btn.addEventListener('click', function () { set(!nav.classList.contains('is-open')); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-open')) { set(false); btn.focus(); }
  });
})();

/* ---------- 2. prayer times ---------- */
(function () {
  var ORDER = ['Fajr', 'Dhuhr', 'Asr', 'Maghrib', 'Isha'];

  /* Offline fallback: approximate Kaduna times. Replace with the mosque's
     printed timetable if it differs. */
  var FALLBACK = { Fajr: '05:20', Dhuhr: '13:20', Asr: '16:35', Maghrib: '18:45', Isha: '19:55' };

  /* Jama'ah: 15 minutes after each prayer time, except Dhuhr, which is
     fixed at 1:15pm. Change JAMAAH_GAP or JAMAAH_FIXED if the arrangement changes. */
  var JAMAAH_GAP = 15;
  var JAMAAH_FIXED = { Dhuhr: '13:15' };

  var list = document.getElementById('salah-list');
  var nextEl = document.getElementById('salah-next');
  var grid = document.getElementById('salah-grid');
  if (!list && !grid) return;

  var current = FALLBACK;

  function todayKey() {
    var d = new Date();
    return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
  }
  function minutes(hhmm) {
    var p = String(hhmm).split(':');
    return parseInt(p[0], 10) * 60 + parseInt(p[1], 10);
  }
  function fmt(hhmm) {
    var m = minutes(hhmm), h = Math.floor(m / 60), mm = m % 60;
    var ap = h >= 12 ? 'pm' : 'am', h12 = h % 12 || 12;
    return h12 + ':' + (mm < 10 ? '0' + mm : mm) + ap;
  }
  function jamaah(t, name) {
    if (JAMAAH_FIXED[name]) return JAMAAH_FIXED[name];
    var m = (minutes(t[name]) + JAMAAH_GAP) % 1440;
    var h = Math.floor(m / 60), mm = m % 60;
    return (h < 10 ? '0' + h : h) + ':' + (mm < 10 ? '0' + mm : mm);
  }
  function nowMin() { var d = new Date(); return d.getHours() * 60 + d.getMinutes(); }
  function nextPrayer(t) {
    var n = nowMin();
    for (var i = 0; i < ORDER.length; i++) if (minutes(t[ORDER[i]]) > n) return ORDER[i];
    return 'Fajr';
  }
  function countdown(t, name) {
    var d = minutes(t[name]) - nowMin();
    if (d < 0) d += 1440;
    var h = Math.floor(d / 60), m = d % 60;
    return (h ? h + 'h ' : '') + m + 'm';
  }
  function render() {
    var t = current, next = nextPrayer(t);
    if (list) {
      list.innerHTML = ORDER.map(function (n) {
        return '<li' + (n === next ? ' class="is-next"' : '') + '>' + n + ' <b>' + fmt(t[n]) + '</b></li>';
      }).join('');
    }
    if (nextEl) nextEl.textContent = next + ' in ' + countdown(t, next);
    if (grid) {
      grid.innerHTML = ORDER.map(function (n) {
        return '<div class="salah-cell' + (n === next ? ' is-next' : '') + '">' +
          '<div class="n">' + n + '</div><div class="t">' + fmt(t[n]) + '</div>' +
          '<div class="j">Jama’ah ' + fmt(jamaah(t, n)) + '</div></div>';
      }).join('');
    }
  }

  var cached = null;
  try { cached = JSON.parse(localStorage.getItem('amsc.salah') || 'null'); } catch (e) {}
  if (cached && cached.key === todayKey() && cached.times) current = cached.times;
  render();
  setInterval(render, 60000);

  if (current === FALLBACK) {
    fetch('https://api.aladhan.com/v1/timingsByCity?city=Kaduna&country=Nigeria&method=3')
      .then(function (r) { return r.json(); })
      .then(function (d) {
        var t = d.data.timings, out = {};
        ORDER.forEach(function (n) { out[n] = t[n].slice(0, 5); });
        current = out;
        try { localStorage.setItem('amsc.salah', JSON.stringify({ key: todayKey(), times: out })); } catch (e) {}
        render();
      })
      .catch(function () { /* offline: the fallback is already on screen */ });
  }
})();

/* ---------- 3. share and print ---------- */
(function () {
  var status = document.getElementById('share-status');
  function say(msg) { if (status) status.textContent = msg; }

  document.querySelectorAll('[data-share]').forEach(function (b) {
    b.addEventListener('click', function () {
      var data = { title: document.title, text: b.getAttribute('data-share'), url: location.href };
      if (navigator.share) {
        navigator.share(data).catch(function () {});
      } else if (navigator.clipboard) {
        navigator.clipboard.writeText(location.href).then(
          function () { say('Link copied. Paste it into your class group.'); },
          function () { say('Copy this link: ' + location.href); });
      } else {
        say('Copy this link: ' + location.href);
      }
    });
  });
  document.querySelectorAll('[data-print]').forEach(function (b) {
    b.addEventListener('click', function () { window.print(); });
  });
})();

/* ---------- 4. checklist ---------- */
(function () {
  var boxes = document.querySelectorAll('.checklist input[type="checkbox"]');
  if (!boxes.length) return;
  var KEY = 'amsc.freshers.checklist';
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) {}
  var count = document.getElementById('checklist-count');
  function update() {
    var done = 0;
    boxes.forEach(function (b) { if (b.checked) done++; });
    if (count) count.textContent = done + ' of ' + boxes.length + ' ready';
  }
  boxes.forEach(function (b) {
    if (saved[b.id]) b.checked = true;
    b.addEventListener('change', function () {
      saved[b.id] = b.checked;
      try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch (e) {}
      update();
    });
  });
  update();
})();

/* ---------- 5. full-page thank-you message ---------- */
function amscDone(title, text) {
  var o = document.createElement('div');
  o.className = 'done';
  o.setAttribute('role', 'dialog');
  o.setAttribute('aria-modal', 'true');
  o.setAttribute('aria-labelledby', 'done-title');
  o.innerHTML = '<div class="done__inner"><div class="done__icon" aria-hidden="true">' +
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12.5 4.5 4.5L19 7.5"/></svg></div>' +
    '<h2 id="done-title"></h2><p></p><div class="actions">' +
    '<button type="button" class="btn btn--yellow" data-done-close>Back to the website</button>' +
    '<a class="btn btn--line-light" href="index.html">Go to the home page</a></div></div>';
  o.querySelector('h2').textContent = title;
  o.querySelector('p').textContent = text;
  document.body.appendChild(o);
  document.body.classList.add('has-done');
  var btn = o.querySelector('[data-done-close]');
  btn.focus();
  function close() {
    o.remove();
    document.body.classList.remove('has-done');
    document.removeEventListener('keydown', esc);
  }
  function esc(e) { if (e.key === 'Escape') close(); }
  btn.addEventListener('click', close);
  document.addEventListener('keydown', esc);
}

/* ---------- 6. Formspree forms (contact, volunteer, alumni) ---------- */
(function () {
  document.querySelectorAll('form[data-formspree]').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = f.querySelector('[type="submit"]');
      var err = f.querySelector('.form-error');
      var label = btn.textContent;
      btn.disabled = true;
      btn.textContent = 'Sending…';
      if (err) err.hidden = true;
      fetch(f.action, { method: 'POST', body: new FormData(f), headers: { Accept: 'application/json' } })
        .then(function (r) {
          if (!r.ok) throw new Error('status ' + r.status);
          f.reset();
          amscDone(f.getAttribute('data-success-title'), f.getAttribute('data-success-text'));
        })
        .catch(function () {
          if (err) {
            err.textContent = 'Your message could not be sent. Check your connection and try again, or email Afitmssn@gmail.com.';
            err.hidden = false;
          }
        })
        .then(function () { btn.disabled = false; btn.textContent = label; });
    });
  });
})();

/* ---------- 7. embedded Google registration form ---------- */
(function () {
  document.querySelectorAll('[data-gform]').forEach(function (box) {
    var frame = box.querySelector('iframe');
    var loads = 0;
    /* The listener is attached before the form starts loading, so the first
       load is the form itself and the second is Google's confirmation page. */
    frame.addEventListener('load', function () {
      loads++;
      if (loads === 2) {
        box.scrollIntoView({ block: 'start' });
        amscDone('Registration received',
          'JazakAllahu khayran. Your details have reached AMSC, and you will be added to the AMSC WhatsApp Community soon. A copy of your answers has been sent to your email.');
      }
    });
    frame.src = box.getAttribute('data-gform');
  });
})();
