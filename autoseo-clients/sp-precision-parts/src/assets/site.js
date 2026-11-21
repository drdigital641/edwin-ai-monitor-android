/* S & P Precision Parts (Monaer): menu sheet, header, dock, part search, state filter, WhatsApp forms. No libraries. */
(function () {
  var d = document, $ = function (s, r) { return (r || d).querySelector(s); }, $$ = function (s, r) { return [].slice.call((r || d).querySelectorAll(s)); };

  // menu sheet
  var sheet = $('#sheet'), burger = $('.burger');
  function setSheet(open) { if (!sheet) return; sheet.hidden = !open; burger.setAttribute('aria-expanded', open ? 'true' : 'false'); d.body.style.overflow = open ? 'hidden' : ''; if (open) $('.sheet-x').focus(); else burger.focus(); }
  if (burger) { burger.addEventListener('click', function () { setSheet(true); }); $('.sheet-x').addEventListener('click', function () { setSheet(false); }); d.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !sheet.hidden) setSheet(false); }); }

  // home header turns solid after 24px
  var top = $('.top');
  if (top && d.body.classList.contains('is-home')) { var onS = function () { top.classList.toggle('solid', window.scrollY > 24); }; onS(); window.addEventListener('scroll', onS, { passive: true }); }

  // dock hides while the hero buttons are on screen
  var dock = $('.dock'), heroBtns = $('.hero .btns');
  if (dock && heroBtns && 'IntersectionObserver' in window) { new IntersectionObserver(function (en) { dock.classList.toggle('hide', en[0].isIntersecting); }).observe(heroBtns); }

  // part search (filters the published list; empty result points to WhatsApp)
  var q = $('#part-q'), parts = $$('#parts .part'), none = $('#part-none');
  if (q) q.addEventListener('input', function () {
    var v = q.value.trim().toLowerCase(), n = 0;
    parts.forEach(function (p) { var ok = !v || p.getAttribute('data-q').indexOf(v) > -1; p.hidden = !ok; if (ok) n++; });
    if (none) none.hidden = n > 0;
  });

  // workshop state filter
  $$('.loc').forEach(function (loc) {
    var cards = $$('.ws', loc), empty = $('.loc-empty', loc);
    $$('.st', loc).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.st', loc).forEach(function (x) { x.classList.toggle('on', x === b); x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
        var s = b.getAttribute('data-state');
        cards.forEach(function (c) { c.hidden = !!s && c.getAttribute('data-state') !== s; });
      });
    });
  });

  // forms open WhatsApp with the filled fields; nothing is stored or posted
  $$('.wa-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var labels = {}; try { labels = JSON.parse(f.getAttribute('data-labels')); } catch (x) {}
      var lines = [f.getAttribute('data-intro')];
      $$('input,select,textarea', f).forEach(function (el) { var v = (el.value || '').trim(); if (v) lines.push((labels[el.name] || el.name) + ': ' + v); });
      var url = f.getAttribute('data-wa') + '?text=' + encodeURIComponent(lines.join('\n'));
      if (window.p1CtaTap) { try { window.p1CtaTap(f.getAttribute('data-cta'), f); } catch (x) {} }
      window.open(url, '_blank', 'noopener');
    });
  });
})();
