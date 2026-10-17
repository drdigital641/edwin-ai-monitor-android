(function () {
  var btn = document.querySelector('.menu-btn'), nav = document.getElementById('mnav');
  if (btn && nav) btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  var WA_NUM = '6584309665';
  var wa = function (text) { return 'https://wa.me/' + WA_NUM + '?text=' + encodeURIComponent(text); };

  // WhatsApp tap counter for the Page One dashboard: same data and endpoint as the other
  // managed client sites (Page One site key for this client). Off while this is a preview on pageonesingapore.com,
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
          body: JSON.stringify({ site: 'dmts', cta_type: 'whatsapp', session_id: sid(), page_path: location.pathname.slice(0, 200),
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

  // Contact form -> WhatsApp
  var f = document.getElementById('qform');
  if (f) {
    var msg = function () {
      var v = function (id) { return document.getElementById(id).value.trim(); };
      return 'Hi Jacky, I\'m enquiring from your website (Page: Contact, Button: Book a diagnostic form). ' +
        'I would like to book a gearbox diagnostic.\nName: ' + v('q-name') + '\nContact: ' + v('q-phone') +
        (v('q-car') ? '\nCar: ' + v('q-car') : '') + (v('q-msg') ? '\nProblem: ' + v('q-msg') : '');
    };
    f.addEventListener('submit', function (ev) { ev.preventDefault(); track(); window.open(wa(msg()), '_blank', 'noopener'); });
  }
})();

// Gearbox motion: meshing gears that turn and speed up while you scroll, cogs on the headings that turn
// with the page, scroll reveals, the process line, counters. Content stays visible without JS, and
// everything sits still for visitors who ask for reduced motion.
(function () {
  var root = document.documentElement, still = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hdr = document.querySelector('header.site');
  var onScroll = function () {
    var y = window.pageYOffset || 0;
    root.style.setProperty('--rot', (y * 0.25).toFixed(1) + 'deg');
    if (hdr) hdr.classList.toggle('scrolled', y > 10);
    proc();
  };

  // process line: fills as the steps scroll through the middle of the screen
  var procs = [].slice.call(document.querySelectorAll('.process'));
  var proc = function () {
    procs.forEach(function (ol) {
      var r = ol.getBoundingClientRect(), vh = window.innerHeight;
      var p = still ? 1 : Math.max(0, Math.min(1, (vh * 0.75 - r.top) / (r.height || 1)));
      ol.style.setProperty('--p', p.toFixed(3));
      var steps = ol.querySelectorAll('.step');
      for (var i = 0; i < steps.length; i++) steps[i].classList.toggle('on', p >= i / Math.max(1, steps.length - 1) - 0.02);
    });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', proc);
  onScroll();
  if (still) return;

  // meshing gears: rotation = k * driver angle + c (k and c are worked out at build time)
  var sets = [].slice.call(document.querySelectorAll('svg.gears')).map(function (svg) {
    return { svg: svg, vis: true, gears: [].slice.call(svg.querySelectorAll('.gr')).map(function (g) {
      return { g: g, k: +g.getAttribute('data-k'), c: +g.getAttribute('data-c') };
    }) };
  });
  var a = 0, boost = 0, lastY = window.pageYOffset || 0, lastT = 0;
  window.addEventListener('scroll', function () {
    var y = window.pageYOffset || 0; boost += Math.min(40, Math.abs(y - lastY) * 0.35); lastY = y;
  }, { passive: true });
  var frame = function (t) {
    var dt = lastT ? Math.min(50, t - lastT) : 16; lastT = t;
    a += dt * 0.012 + boost * 0.12; boost *= 0.9;
    sets.forEach(function (s) {
      if (!s.vis) return;
      s.gears.forEach(function (x) { x.g.setAttribute('transform', 'rotate(' + (x.k * a + x.c).toFixed(2) + ')'); });
    });
    requestAnimationFrame(frame);
  };
  if ('IntersectionObserver' in window) {
    var gio = new IntersectionObserver(function (es) { es.forEach(function (en) {
      sets.forEach(function (s) { if (s.svg === en.target) s.vis = en.isIntersecting; });
    }); });
    sets.forEach(function (s) { gio.observe(s.svg); });
  }
  if (sets.length) requestAnimationFrame(frame);

  // scroll reveal, staggered within each group
  if (!('IntersectionObserver' in window)) return;
  var counted = function (el) {
    var n = +el.getAttribute('data-n'), t0 = 0;
    var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / 1100);
      el.textContent = Math.round(n * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) {
      if (!en.isIntersecting) return;
      var el = en.target; el.classList.add('in'); io.unobserve(el);
      setTimeout(function () { el.classList.remove('rv', 'in'); el.style.removeProperty('--d'); }, 1400); // hand hover effects back
      [].forEach.call(el.querySelectorAll('.n[data-n]'), counted);
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  var sel = 'main section .sec-head, main .card, main .stat, main .split > *, main .band, main details, main .gallery figure, main .step, main section > .wrap > h2, main .ticks';
  var seen = [];
  [].forEach.call(document.querySelectorAll(sel), function (el) {
    if (el.closest('.hero') || seen.some(function (p) { return p.contains(el); })) return;
    var r = el.getBoundingClientRect();
    if (r.top < window.innerHeight && r.bottom > 0) return; // already on screen: leave it as is
    var sib = el.parentNode ? [].indexOf.call(el.parentNode.children, el) : 0;
    el.style.setProperty('--d', (Math.min(sib, 5) * 0.08) + 's');
    el.classList.add('rv'); seen.push(el); io.observe(el);
  });
  root.classList.add('js');
})();
