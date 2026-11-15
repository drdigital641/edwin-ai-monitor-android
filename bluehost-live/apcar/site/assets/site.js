/* AP Car preview: small helpers only. Every word, link and schema is already in the HTML. */
(function () {
  var d = document, w = window;
  var reduced = w.matchMedia && w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var conn = navigator.connection || {};
  var slow = conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '');

  /* Menu drawer */
  var btn = d.getElementById('menu-btn'), dr = d.getElementById('drawer');
  if (btn && dr) {
    var set = function (o) { dr.classList.toggle('open', o); btn.setAttribute('aria-expanded', o ? 'true' : 'false'); btn.querySelector('.lbl').textContent = o ? btn.dataset.close : btn.dataset.open; };
    btn.addEventListener('click', function () { set(!dr.classList.contains('open')); });
    d.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  }

  /* Symptom picker (tabs). Without JS every panel shows. */
  var tabs = d.querySelectorAll('[data-pick]');
  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      tabs.forEach(function (o) { o.setAttribute('aria-selected', o === t ? 'true' : 'false'); var p = d.getElementById(o.getAttribute('aria-controls')); if (p) p.hidden = o !== t; });
    });
  });

  /* Vent read-out: digits settle on the real reading (5.9 °C, fb photo / TikTok 02). */
  var rd = d.querySelector('[data-read]');
  if (rd) {
    var target = parseFloat(rd.dataset.read), el = rd.querySelector('.n');
    if (reduced) el.textContent = target.toFixed(1); else {
      var t0 = null, dur = 1600;
      var step = function (ts) { if (!t0) t0 = ts; var k = (ts - t0) / dur;
        if (k < 1) { el.textContent = (Math.floor(Math.random() * 9) + 1) + '.' + Math.floor(Math.random() * 10); requestAnimationFrame(step); }
        else el.textContent = target.toFixed(1); };
      requestAnimationFrame(step);
    }
  }

  /* Self-hosted clips: muted loop, poster only for reduced motion / Save-Data; play only while on screen. */
  d.querySelectorAll('video[data-auto]').forEach(function (v) {
    var ctl = v.parentNode.querySelector('.vctl');
    var sync = function () { if (!ctl) return; var p = !v.paused; ctl.innerHTML = p ? ctl.dataset.ip : ctl.dataset.ipl; ctl.setAttribute('aria-label', p ? ctl.dataset.pause : ctl.dataset.play); };
    v.addEventListener('play', sync); v.addEventListener('pause', sync);
    if (ctl) ctl.addEventListener('click', function () { if (v.paused) { v.dataset.user = 'play'; v.play(); } else { v.dataset.user = 'pause'; v.pause(); } });
    if (reduced || slow) { sync(); return; }
    if ('IntersectionObserver' in w) {
      new IntersectionObserver(function (es) { es.forEach(function (e) {
        if (e.isIntersecting && v.dataset.user !== 'pause') { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else if (!e.isIntersecting) v.pause();
      }); }, { threshold: 0.25 }).observe(v);
    } else { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
  });

  /* Click-to-play clips: no autoplay; starting one pauses every other video on the page. */
  d.querySelectorAll('video[data-tap]').forEach(function (v) {
    var ctl = v.parentNode.querySelector('.vctl');
    var sync = function () { if (!ctl) return; var p = !v.paused; ctl.innerHTML = p ? ctl.dataset.ip : ctl.dataset.ipl; ctl.setAttribute('aria-label', p ? ctl.dataset.pause : ctl.dataset.play); };
    v.addEventListener('play', function () {
      d.querySelectorAll('video').forEach(function (o) { if (o !== v && !o.paused) { o.pause(); if (o.hasAttribute('data-auto')) o.dataset.user = 'pause'; } });
      sync();
    });
    v.addEventListener('pause', sync);
    var go = function (ev) { ev.preventDefault(); if (v.paused) v.play(); else v.pause(); };
    if (ctl) ctl.addEventListener('click', go);
    v.addEventListener('click', go);
    sync();
  });


  /* Reveal on scroll */
  var rv = d.querySelectorAll('.rv');
  if (!reduced && 'IntersectionObserver' in w) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (x) { io.observe(x); });
  } else rv.forEach(function (x) { x.classList.add('in'); });

  /* Click-to-load: nothing from TikTok or Google Maps loads until the visitor taps. */
  d.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a.reel[data-embed]');
    if (a) { e.preventDefault(); var box = d.createElement('div'); box.className = 'embed-frame';
      var f = d.createElement('iframe'); f.src = a.dataset.embed; f.title = a.dataset.title; f.loading = 'lazy';
      f.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen'; f.allowFullscreen = true; box.appendChild(f); a.replaceWith(box); return; }
    var m = e.target.closest && e.target.closest('button[data-map]');
    if (m) { var fr = d.createElement('iframe'); fr.src = m.dataset.map; fr.title = m.dataset.title; fr.loading = 'lazy';
      fr.referrerPolicy = 'no-referrer-when-downgrade'; m.parentNode.appendChild(fr); m.remove(); }
  });

  /* Tap counting for the owner's dashboard (WhatsApp, call, map, email). No cookies, no personal data.
     On the /preview/ copy it sends only when the page URL has ?p1test=1 (stored as a test tap). */
  (function () {
    if (w.__p1cta) return; w.__p1cta = 1;
    var site = 'apcar', test = /[?&]p1test=1/.test(location.search), last = 0;
    if (/^\/preview\//.test(location.pathname) && !test) return;
    if (location.protocol === 'file:') return;
    function kind(h) { if (/^(https?:\/\/(wa\.me|api\.whatsapp\.com)\/|whatsapp:)/i.test(h)) return 'whatsapp';
      if (/^tel:/i.test(h)) return 'call'; if (/^mailto:/i.test(h)) return 'email';
      if (/^https?:\/\/(www\.)?google\.[a-z.]+\/maps|^https?:\/\/maps\.app\.goo\.gl|^https?:\/\/goo\.gl\/maps|^https?:\/\/share\.google\/|^https?:\/\/search\.google\.com\/local\/writereview/i.test(h)) return 'map'; return ''; }
    function sid() { try { var k = 'p1cta_sid', v = sessionStorage.getItem(k); if (!v) { v = Math.random().toString(36).slice(2) + Date.now().toString(36); sessionStorage.setItem(k, v); } return v; } catch (e) { return 'na'; } }
    d.addEventListener('click', function (e) {
      var a = e.target && e.target.closest ? e.target.closest('a[href],button[data-map]') : null; if (!a) return;
      var t = a.dataset.cta ? a.dataset.cta.split('_')[0] : kind(String(a.href || '')); if (!/^(whatsapp|call|map|email)$/.test(t)) return;
      var now = Date.now(); if (now - last < 1500) return; last = now;
      try { fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track', { method: 'POST', credentials: 'omit', keepalive: true,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ entity: 'CtaClick', site: site, cta_type: t, cta_ref: a.dataset.ref || '', session_id: sid(),
          page_path: location.pathname.slice(0, 200), device_type: /Mobi|Android|iPhone/i.test(navigator.userAgent) ? 'mobile' : 'desktop',
          referrer: (d.referrer || '').slice(0, 200), flag: test ? 'test' : undefined }) }).catch(function () {}); } catch (err) {}
    }, true);
  })();
})();
