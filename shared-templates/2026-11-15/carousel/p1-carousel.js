/* Page One shared sliding carousel v1 (15 Nov 2026). One file for every client site.
   Behaviour (Edwin, 3 Nov + 14 Nov 2026, Wrapstar-style glide):
   - slides on its own, continuously, as a seamless loop;
   - vertical page scrolling never stops it (also when the finger starts on it);
   - ONLY a press-and-hold or a sideways drag pauses it; it resumes 1.5 s after release;
   - the user can slide it left/right 1:1 with a finger or mouse; touch is decided on the first 6 px
     (sideways = slide + preventDefault, vertical = left to the page);
   - visible arrows + dots; keyboard focus on a control pauses it until focus leaves;
   - prefers-reduced-motion: no auto-slide, a plain swipe row with the same arrows + dots.
   Markup: see carousel.html. Options on the .p1c element: data-speed (px per ms, default 0.04),
   data-resume (ms, default 1500), data-hover-pause="1" (opt-in, off by default). */
(function () {
  'use strict';
  if (window.__p1c) return; window.__p1c = 1;
  var d = document, RM = !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  var all = [], running = false, last = 0;
  function now() { return Date.now(); }
  // keyboard focus pauses; a tap or click that focuses a card link must not (it would never resume)
  var kb = false;
  d.addEventListener('keydown', function (e) { if (e.key === 'Tab' || e.key === 'Enter' || e.key === ' ') kb = true; }, true);
  ['mousedown', 'touchstart', 'pointerdown'].forEach(function (t) { d.addEventListener(t, function () { kb = false; }, { capture: true, passive: true }); });
  function ready(f) { d.readyState !== 'loading' ? f() : d.addEventListener('DOMContentLoaded', f); }
  function el(tag, cls, attrs) { var e = d.createElement(tag); if (cls) e.className = cls; for (var k in attrs || {}) e.setAttribute(k, attrs[k]); return e; }

  function setup(root) {
    if (root.__p1c) return; root.__p1c = 1;
    var rail = root.querySelector('.p1c-rail'), track = root.querySelector('.p1c-track');
    if (!rail || !track) return;
    var cards = [].slice.call(track.children), n = cards.length;
    if (n < 2) return;
    var o = {
      root: root, rail: rail, track: track, n: n, pos: 0, half: 0, step: 0,
      speed: +(root.getAttribute('data-speed') || 0.04), resume: +(root.getAttribute('data-resume') || 1500),
      held: false, until: 0, vis: true, tween: null, motion: !RM
    };
    // controls (built here so every site gets the same accessible arrows + dots)
    var ctrl = root.querySelector('.p1c-ctrl');
    if (!ctrl) {
      ctrl = el('div', 'p1c-ctrl');
      ctrl.appendChild(el('button', 'p1c-prev', { type: 'button', 'aria-label': 'Previous' }));
      ctrl.appendChild(el('div', 'p1c-dots', { role: 'group', 'aria-label': 'Choose slide' }));
      ctrl.appendChild(el('button', 'p1c-next', { type: 'button', 'aria-label': 'Next' }));
      root.appendChild(ctrl);
    }
    var dotsBox = ctrl.querySelector('.p1c-dots'), groups = Math.min(n, 8), per = Math.ceil(n / groups), dots = [];
    groups = Math.ceil(n / per);
    for (var g = 0; g < groups; g++) {
      var b = el('button', 'p1c-dot', { type: 'button', 'aria-label': 'Slide ' + (g * per + 1) + ' of ' + n });
      b.setAttribute('data-i', g * per); dotsBox.appendChild(b); dots.push(b);
    }
    o.dots = dots; o.per = per;

    if (o.motion) {
      cards.forEach(function (c) {
        var k = c.cloneNode(true);
        k.setAttribute('aria-hidden', 'true'); k.removeAttribute('id');
        [].forEach.call(k.querySelectorAll('[id]'), function (x) { x.removeAttribute('id'); });
        [].forEach.call(k.querySelectorAll('a,button,input,select,textarea,[tabindex]'), function (x) { x.setAttribute('tabindex', '-1'); });
        track.appendChild(k);
      });
      root.classList.add('p1c-run');
    }
    root.classList.add('p1c-ready');

    function measure() {
      var kids = track.children;
      o.step = kids[1].offsetLeft - kids[0].offsetLeft;
      o.half = o.motion ? kids[n].offsetLeft - kids[0].offsetLeft : 0;
      if (o.motion) setPos(o.pos);
    }
    function wrap(p) { if (!o.half) return p; p = p % o.half; return p < 0 ? p + o.half : p; }
    function setPos(p) { o.pos = wrap(p); track.style.transform = 'translate3d(' + (-o.pos) + 'px,0,0)'; mark(); }
    function current() {
      if (!o.step) return 0;
      var x = o.motion ? o.pos : rail.scrollLeft;
      return Math.round(x / o.step) % n;
    }
    function mark() {
      var c = Math.floor(current() / o.per);
      for (var i = 0; i < dots.length; i++) dots[i].setAttribute('aria-current', i === c ? 'true' : 'false');
    }
    function pauseFor() { o.until = now() + o.resume; }
    function go(index) {
      if (!o.step) measure();
      if (o.motion) {
        var cur = o.pos, target = index * o.step;
        // shortest way round the loop
        if (o.half) { var diff = ((target - cur) % o.half + o.half * 1.5) % o.half - o.half / 2; target = cur + diff; }
        o.tween = { from: cur, to: target, t0: performance.now(), dur: 380 };
        pauseFor(); o.until += 380; kick();
      } else {
        rail.scrollTo({ left: index * o.step, behavior: 'auto' });
      }
    }
    function nudge(dir) { var i = current() + dir; go(o.motion ? i : Math.max(0, Math.min(n - 1, i))); }
    ctrl.querySelector('.p1c-prev').addEventListener('click', function () { nudge(-1); });
    ctrl.querySelector('.p1c-next').addEventListener('click', function () { nudge(1); });
    dots.forEach(function (b) { b.addEventListener('click', function () { go(+b.getAttribute('data-i')); }); });
    if (!o.motion) rail.addEventListener('scroll', mark, { passive: true });

    // keyboard: focus on a control or a card link pauses until focus leaves (WCAG 2.2.2 stop mechanism)
    root.addEventListener('focusin', function () { if (kb) o.held = true; });
    root.addEventListener('focusout', function (e) { if (!root.contains(e.relatedTarget)) { o.held = false; pauseFor(); } });
    if (root.getAttribute('data-hover-pause') === '1') {
      root.addEventListener('mouseenter', function () { o.hover = true; });
      root.addEventListener('mouseleave', function () { o.hover = false; pauseFor(); });
    }

    addEventListener('resize', measure);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { o.vis = es[0].isIntersecting; if (o.vis) kick(); }, { threshold: 0 }).observe(root);
    measure();
    if (!o.motion) { all.push(o); return; }

    // ---- touch: 1:1 sideways slide, vertical goes to the page, hold pauses ----
    var sx = 0, sy = 0, sp = 0, mode = '', timer = 0, touching = false, lastTouch = 0;
    rail.addEventListener('touchstart', function (e) {
      if (e.touches.length > 1) return;
      var t = e.touches[0]; sx = t.clientX; sy = t.clientY; sp = o.pos; mode = ''; touching = true; o.tween = null; lastTouch = now();
      clearTimeout(timer);
      timer = setTimeout(function () { if (touching && mode !== 'y') o.held = true; }, 250);
    }, { passive: true });
    rail.addEventListener('touchmove', function (e) {
      if (!touching) return;
      var t = e.touches[0], dx = t.clientX - sx, dy = t.clientY - sy;
      if (!mode) {
        if (Math.abs(dx) < 6 && Math.abs(dy) < 6) { if (Math.abs(dx) > Math.abs(dy) && e.cancelable) e.preventDefault(); return; }
        mode = Math.abs(dx) > Math.abs(dy) ? 'x' : 'y';
        if (mode === 'y') { clearTimeout(timer); o.held = false; return; }
        o.held = true; clearTimeout(timer);
      }
      if (mode === 'x') { if (e.cancelable) e.preventDefault(); setPos(sp - dx); }
    }, { passive: false });
    function tend() {
      if (!touching) return; touching = false; clearTimeout(timer); lastTouch = now();
      if (o.held) { o.held = false; pauseFor(); }
      if (mode === 'x') o.dragged = now();
      mode = '';
    }
    rail.addEventListener('touchend', tend, { passive: true });
    rail.addEventListener('touchcancel', tend, { passive: true });

    // ---- mouse: press pauses, drag slides 1:1, release resumes after 1.5 s ----
    var mdown = false, mx = 0, moved = 0;
    rail.addEventListener('mousedown', function (e) {
      // ignore the mouse events a browser fakes after a tap
      if (e.button !== 0 || now() - lastTouch < 1000) return; mdown = true; mx = e.clientX; sp = o.pos; moved = 0; o.held = true; o.tween = null;
    });
    addEventListener('mousemove', function (e) {
      if (!mdown) return; var dx = e.clientX - mx; moved = Math.max(moved, Math.abs(dx));
      if (moved > 3) { setPos(sp - dx); e.preventDefault(); }
    });
    addEventListener('mouseup', function () {
      if (!mdown) return; mdown = false; o.held = false; pauseFor(); if (moved > 5) o.dragged = now();
    });
    rail.addEventListener('dragstart', function (e) { e.preventDefault(); });
    // a drag must not open the card link underneath it
    rail.addEventListener('click', function (e) { if (o.dragged && now() - o.dragged < 400) { e.preventDefault(); e.stopPropagation(); } }, true);
    // trackpad / shift-wheel sideways scroll slides it; vertical wheel is left to the page
    rail.addEventListener('wheel', function (e) {
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) { e.preventDefault(); o.tween = null; setPos(o.pos + e.deltaX); pauseFor(); }
    }, { passive: false });

    all.push(o); kick();
  }

  function tick(t) {
    var dt = last ? Math.min(64, t - last) : 16; last = t; var any = false, n_ = now();
    all.forEach(function (o) {
      if (!o.motion) return;
      if (o.tween) {
        var k = Math.min(1, (t - o.tween.t0) / o.tween.dur), e = 1 - Math.pow(1 - k, 3);
        o.pos = o.tween.from + (o.tween.to - o.tween.from) * e;
        o.track.style.transform = 'translate3d(' + (-((o.pos % o.half + o.half) % o.half)) + 'px,0,0)';
        if (k >= 1) { o.pos = ((o.tween.to % o.half) + o.half) % o.half; o.tween = null; }
        any = true; return;
      }
      if (!o.vis || d.hidden) return;
      any = true;
      if (o.held || o.hover || n_ < o.until) return;
      o.pos += dt * o.speed; if (o.half && o.pos >= o.half) o.pos -= o.half;
      o.track.style.transform = 'translate3d(' + (-o.pos) + 'px,0,0)';
      if (o.dots) { var c = Math.floor((Math.round(o.pos / o.step) % o.n) / o.per); for (var i = 0; i < o.dots.length; i++) { var on = i === c ? 'true' : 'false'; if (o.dots[i].getAttribute('aria-current') !== on) o.dots[i].setAttribute('aria-current', on); } }
    });
    if (any) requestAnimationFrame(tick); else { running = false; last = 0; }
  }
  function kick() { if (!running) { running = true; last = 0; requestAnimationFrame(tick); } }
  d.addEventListener('visibilitychange', function () { if (!d.hidden) kick(); });

  ready(function () { [].forEach.call(d.querySelectorAll('.p1c'), setup); });
  window.p1Carousel = setup;
})();
