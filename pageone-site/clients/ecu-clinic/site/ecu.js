(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('mnav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // WhatsApp tap counter for the Page One dashboard: same data and endpoint as the other
  // managed client sites (site key "ecu-clinic"). Off while this is a preview on pageonesingapore.com,
  // so it only counts once the site runs on the client's own domain.
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
    var track = function () {
      var n = Date.now(); if (n - last < 1500) return; last = n;
      try {
        fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/entities/CtaClick', {
          method: 'POST', credentials: 'omit', keepalive: true, headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ site: 'ecu-clinic', cta_type: 'whatsapp', session_id: sid(), page_path: location.pathname.slice(0, 200),
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

})();
