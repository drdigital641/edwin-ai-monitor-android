(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('mnav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  // close the mobile menu once a link in it is tapped
  if (btn && nav) nav.addEventListener('click', function (e) {
    if (!e.target.closest('a')) return;
    nav.classList.remove('open'); btn.setAttribute('aria-expanded', 'false');
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

  // Motion: header shadow on scroll, reveal-on-scroll, count-up stats.
  // Nothing is hidden until this script runs, and only things below the fold get hidden,
  // so the page is never blank if the script is slow or blocked.
  var head = document.querySelector('header.site');
  var onScroll = function () { if (head) head.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;

  // reading progress bar + hero parallax, one rAF per scroll
  var bar = document.createElement('div'); bar.className = 'progress'; document.body.appendChild(bar);
  var heroImg = document.querySelector('.hero img.bg'), ticking = false;
  var paint = function () {
    ticking = false;
    var h = document.documentElement.scrollHeight - innerHeight, y = scrollY;
    bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(y / h, 1) : 0) + ')';
    if (heroImg && y < innerHeight * 1.2) heroImg.style.setProperty('--py', (y * 0.3).toFixed(1) + 'px');
  };
  window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(paint); } }, { passive: true });
  paint();

  // pointer spotlight on cards, gentle tilt on photo cards (mouse only)
  if (matchMedia('(hover: hover)').matches) {
    document.querySelectorAll('.card.img, .gallery figure').forEach(function (c) { c.classList.add('tilt'); });
    document.addEventListener('pointermove', function (ev) {
      var c = ev.target.closest && ev.target.closest('.card, .gallery figure'); if (!c) return;
      var r = c.getBoundingClientRect(), x = (ev.clientX - r.left) / r.width, y = (ev.clientY - r.top) / r.height;
      c.style.setProperty('--mx', (x * 100).toFixed(1) + '%'); c.style.setProperty('--my', (y * 100).toFixed(1) + '%');
      if (c.classList.contains('tilt')) { c.style.setProperty('--rx', ((0.5 - y) * 6).toFixed(2) + 'deg'); c.style.setProperty('--ry', ((x - 0.5) * 6).toFixed(2) + 'deg'); }
    }, { passive: true });
  }

  // tap ripple on buttons
  document.addEventListener('pointerdown', function (ev) {
    var b = ev.target.closest && ev.target.closest('.btn'); if (!b) return;
    var r = b.getBoundingClientRect(), d = Math.max(r.width, r.height), s = document.createElement('span');
    s.className = 'rip'; s.style.width = s.style.height = d + 'px';
    s.style.left = (ev.clientX - r.left - d / 2) + 'px'; s.style.top = (ev.clientY - r.top - d / 2) + 'px';
    b.appendChild(s); setTimeout(function () { s.remove(); }, 650);
  }, { passive: true });

  if (!('IntersectionObserver' in window)) return;

  var groups = [
    ['.sec-head', ''], ['.why .card', 'stagger'], ['.svc .card', 'stagger'], ['.split>div:first-child', 'from-l'],
    ['.split>div:last-child', 'from-r'], ['.makes li', 'stagger-fast'], ['.gallery figure', 'zoom stagger'],
    ['.loc-wrap>.card', 'stagger'], ['#faq details', 'stagger-fast'], ['.band', 'zoom'], ['.svc+p', ''], ['.stats li', 'stagger'],
    // service pages, articles and the fault-code list (16 Oct 2026)
    ['.sym .card', 'stagger'], ['.arts .card', 'zoom stagger'], ['.prose>h2,.prose>p,.prose>ul', ''], ['.models-list p', 'stagger-fast'],
    ['.split details', 'stagger-fast'], ['ul.ticks', ''], ['.split>div>h2', '']
  ];
  var vh = window.innerHeight, io = new IntersectionObserver(function (es) {
    es.forEach(function (en) { if (!en.isIntersecting) return;
      var t = en.target; t.classList.add('in'); io.unobserve(t); count(t);
      // once shown, drop the reveal classes so hover effects run without the stagger delay
      setTimeout(function () { t.classList.remove('rv', 'in', 'from-l', 'from-r', 'zoom'); t.style.removeProperty('--d'); }, 1600); });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  groups.forEach(function (g) {
    var els = document.querySelectorAll(g[0]), step = /stagger-fast/.test(g[1]) ? 0.04 : /stagger/.test(g[1]) ? 0.09 : 0;
    Array.prototype.forEach.call(els, function (el, i) {
      if (el.getBoundingClientRect().top < vh * 0.92) { count(el); return; }
      el.classList.add('rv');
      g[1].split(' ').forEach(function (c) { if (c && c.indexOf('stagger') < 0) el.classList.add(c); });
      if (step) el.style.setProperty('--d', Math.min(i % 8 * step, 0.5) + 's');
      io.observe(el);
    });
  });

  function count(el) {
    var b = el.querySelector && el.querySelector('b[data-count]'); if (!b || b.dataset.done) return; b.dataset.done = 1;
    var to = +b.dataset.count, tail = b.innerHTML.replace(/^[\d,]+/, ''), t0 = null, dur = 1400;
    var fmt = function (n) { return Math.round(n).toLocaleString('en-SG'); };
    var tick = function (t) {
      if (!t0) t0 = t; var p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 3);
      b.innerHTML = fmt(to * e) + tail; if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

})();
