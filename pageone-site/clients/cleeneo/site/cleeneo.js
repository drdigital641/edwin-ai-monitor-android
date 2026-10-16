(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('mnav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  var WA_NUM = '6580604977', EMAIL = 'sales@cleeneo.co';
  var wa = function (text) { return 'https://wa.me/' + WA_NUM + '?text=' + encodeURIComponent(text); };

  // WhatsApp tap counter for the Page One dashboard: same data and endpoint as the other
  // managed client sites (site key "cleeneo"). Off while this is a preview on pageonesingapore.com,
  // so it only counts once the site runs on the client's own domain.
  var track = function () {};
  (function () {
    if (window.__p1cta || location.hostname.replace(/^www\./, '') === 'pageonesingapore.com') return;
    window.__p1cta = 1;
    var WA = /^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i, last = 0;
    var sid = function () {
      try {
        var k = 'p1cta_sid', v = sessionStorage.getItem(k);
        if (!v) { v = Math.random().toString(36).slice(2) + Date.now().toString(36); sessionStorage.setItem(k, v); }
        return v;
      } catch (e) { return 'na'; }
    };
    track = function () {
      var n = Date.now(); if (n - last < 1500) return; last = n;
      try {
        fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/entities/CtaClick', {
          method: 'POST', credentials: 'omit', keepalive: true, headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ site: 'cleeneo', cta_type: 'whatsapp', session_id: sid(), page_path: location.pathname.slice(0, 200),
            device_type: /Mobi|Android|iPhone/i.test(navigator.userAgent) ? 'mobile' : 'desktop',
            referrer: (document.referrer || '').slice(0, 200) })
        }).catch(function () {});
      } catch (e) { /* tracking must never break the page */ }
    };
    document.addEventListener('click', function (e) {
      var a = e.target && e.target.closest ? e.target.closest('a[href]') : null;
      if (a && WA.test(String(a.href || ''))) track();
    }, true);
  })();

  var v = function (id) { var el = document.getElementById(id); return el ? el.value.trim() : ''; };

  // Order form (kits page) -> WhatsApp with the order typed out
  var o = document.getElementById('oform');
  if (o) {
    var kits = window.CLEENEO_KITS || {};
    if (location.hash && kits[location.hash.slice(1)]) document.getElementById('o-kit').value = location.hash.slice(1);
    o.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var k = kits[v('o-kit')] || {}, q = parseInt(v('o-qty'), 10) || 1;
      var total = k.price ? ' (S$' + (parseFloat(k.price) * q).toFixed(2) + ')' : '';
      var msg = 'Hi Cleeneo, I would like to order:\n' + q + ' x ' + k.name + ', ' + k.strips + ' strips' + total +
        '\nName: ' + v('o-name') + '\nDelivery address: ' + v('o-addr') + '\nPostal code: ' + v('o-postal');
      track(); window.open(wa(msg), '_blank', 'noopener');
    });
  }

  // Contact form -> WhatsApp (preferred) or email
  var f = document.getElementById('qform');
  if (f) {
    var msg = function () {
      return 'Hi Cleeneo,\n' + v('q-msg') + '\n\nName: ' + v('q-name') + '\nContact: ' + v('q-contact');
    };
    f.addEventListener('submit', function (ev) { ev.preventDefault(); track(); window.open(wa(msg()), '_blank', 'noopener'); });
    document.getElementById('q-mail').addEventListener('click', function () {
      if (!f.reportValidity()) return;
      location.href = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent('Message from cleeneo.co') + '&body=' + encodeURIComponent(msg());
    });
  }
})();
