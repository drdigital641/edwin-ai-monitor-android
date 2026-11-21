/* ktech.my Autel MS906 MAX promo: Checkout payment form (round 3, 22 Nov 2026). Built from promo.json + strings.py.
   Checks the form here for quick feedback; the server (K Tech Promo Orders, fn ktechOrder) checks everything again,
   stores the order first and decides the payment step. Price, product and the end date are fixed on the server.
   No key, payment link or order data lives in this file. */
(function () {
  var F = document.getElementById('pmco');
  if (!F) return;
  var C = JSON.parse(F.getAttribute('data-cfg'));
  var M = C.msg, t0 = Date.now(), busy = false;
  var $ = function (id) { return document.getElementById(id); };
  var q = $('f-qty'), tot = $('pm-total'), err = $('pm-err'), btn = F.querySelector('.pm-go');
  var REF = /^KT-MAX-\d{6}-[A-Z0-9]{5}$/;
  function rm(n) { return 'RM' + n.toLocaleString('en-MY'); }
  function qty() { var n = Number(q.value); return Number.isInteger(n) ? n : NaN; }
  function upd() { var n = qty(); tot.textContent = n >= 1 && n <= C.max ? rm(n * C.price) : '–'; }
  F.querySelectorAll('.pm-qb').forEach(function (b) {
    b.addEventListener('click', function () {
      var n = qty() || 1; n = Math.min(C.max, Math.max(1, n + Number(b.getAttribute('data-d')))); q.value = n; upd(); mark('qty', '');
    });
  });
  q.addEventListener('input', upd);
  function phone(v) {
    var d = String(v || '').replace(/[\s\-().]/g, '');
    if (d.charAt(0) === '+') d = d.slice(1);
    if (d.indexOf('60') === 0) d = d.slice(2); else if (d.charAt(0) === '0') d = d.slice(1); else return '';
    if (d.charAt(0) === '0') d = d.slice(1);
    return /^1\d{8,9}$/.test(d) ? '+60' + d : '';
  }
  function val(n) { var el = F.elements[n]; return el ? String(el.value || '').trim() : ''; }
  function mark(n, msg) {
    var box = F.querySelector('[data-f="' + n + '"]'), em = $('e-' + n), el = F.elements[n];
    if (!box || !em) return;
    box.classList.toggle('bad', !!msg); em.hidden = !msg; em.textContent = msg || '';
    if (el && el.setAttribute) { if (msg) { el.setAttribute('aria-invalid', 'true'); el.setAttribute('aria-errormessage', 'e-' + n); } else el.removeAttribute('aria-invalid'); }
  }
  function check() {
    var bad = [];
    var n = qty();
    var rules = {
      name: val('name').length >= 2, phone: !!phone(val('phone')),
      email: /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(val('email')), address_line1: val('address_line1').length >= 3,
      postcode: /^\d{5}$/.test(val('postcode')), city: val('city').length >= 2, state: !!val('state'),
      qty: n >= 1 && n <= C.max, consent: $('f-consent').checked
    };
    Object.keys(rules).forEach(function (k) { mark(k, rules[k] ? '' : M[k]); if (!rules[k]) bad.push(k); });
    return bad;
  }
  ['name', 'phone', 'email', 'address_line1', 'postcode', 'city', 'state'].forEach(function (n) {
    var el = F.elements[n]; el.addEventListener('blur', function () { if (F.querySelector('[data-f="' + n + '"]').classList.contains('bad')) check(); });
  });
  function say(msg) { err.textContent = msg; err.hidden = !msg; }
  function show(h, p, ref) {
    F.hidden = true; $('pmco-dh').textContent = h; $('pmco-dp').textContent = p; $('pmco-ref').textContent = ref || '';
    $('pmco-ref').parentNode.hidden = !ref; var d = $('pmco-done'); d.hidden = false; d.focus(); window.scrollTo(0, d.getBoundingClientRect().top + window.pageYOffset - 90);
  }
  function post(body) {
    return fetch(C.api, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), credentials: 'omit' })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { j._s = r.status; return j; }); });
  }
  F.addEventListener('submit', function (ev) {
    ev.preventDefault();
    if (busy) return;
    var bad = check();
    if (bad.length) { say(M.fix); var el = F.elements[bad[0]] || $('f-' + bad[0]); if (el && el.focus) el.focus(); return; }
    say(''); busy = true; btn.disabled = true; var lbl = btn.querySelector('span'), old = lbl.textContent; lbl.textContent = M.sending;
    post({ action: 'order', lang: C.lang, name: val('name'), phone: phone(val('phone')), email: val('email'),
      address_line1: val('address_line1'), address_line2: val('address_line2'), postcode: val('postcode'), city: val('city'),
      state: val('state'), qty: qty(), consent: $('f-consent').checked, company_website: val('company_website'),
      fill_ms: Date.now() - t0, page_path: location.pathname })
      .then(function (j) {
        if (j.ok && REF.test(j.ref || '')) {
          if (j.pay_url && /^https:\/\/(checkout|buy)\.stripe\.com\//.test(j.pay_url)) { lbl.textContent = M.redirect; location.href = j.pay_url; return; }
          show(M.soon_h, M.soon_p, j.ref); return;
        }
        if (j._s === 422 && j.fields) { j.fields.forEach(function (k) { mark(k, M[k] || M.fix); }); say(M.fix); }
        else say(j._s === 410 ? M.ended : j._s === 429 ? M.rate : M.server);
        busy = false; btn.disabled = false; lbl.textContent = old;
      })
      .catch(function () { say(M.server); busy = false; btn.disabled = false; lbl.textContent = old; });
  });
  // Back from Stripe: ?ref=...&session_id=... (paid?) or &cancelled=1. The server asks Stripe; the browser is not trusted.
  var u = new URLSearchParams(location.search), ref = u.get('ref') || '';
  if (REF.test(ref) && u.get('cancelled')) say(M.cancel);
  else if (REF.test(ref) && u.get('session_id')) {
    post({ action: 'status', ref: ref, session_id: u.get('session_id') }).then(function (j) {
      if (j.ok && j.status === 'paid') show(M.paid_h, M.paid_p, ref); else show(M.check_h, M.check_p, ref);
    }).catch(function () { show(M.check_h, M.check_p, ref); });
  }
  upd();
})();
