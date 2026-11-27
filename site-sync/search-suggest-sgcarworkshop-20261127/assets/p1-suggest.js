/*! p1-suggest 1.0.0 (shared-modules/search-suggest) | live search suggestions for client sites.
 * Master copy: Bluehost Bridge master folder modules/search-suggest/ (outside public_html).
 * Change the master first, bump module.json + CHANGELOG, then copy to sites. Never edit a site copy alone.
 *
 * Hook-up (two lines, no other markup changes):
 *   <link rel="stylesheet" href="./assets/p1-suggest.css?v=1.0.0">
 *   <script src="./assets/p1-suggest.js?v=1.0.0" defer data-index="./assets/search-index.json"></script>
 * It attaches to every input/textarea with [data-p1-suggest]; when none is marked, to the site's own
 * search boxes (type=search, inputs/textareas inside form[role=search], or name q/s/search/query/keyword).
 * Data: a static JSON index (data-index) OR a live endpoint (data-endpoint, "q=" is appended).
 *   item {t:"product|service|page|article|category|brand", n:name, u:url, i:thumb, p:price label, c:sub line, k:keywords}
 *   An endpoint may return the same items or Eunice-style {u,i,n,p,s}.
 * Options (script tag, overridable per box): data-min (2), data-delay (160 ms), data-max (6),
 *   data-base (prefix for root-relative item URLs, e.g. "/preview/x"), data-all-label, data-all-url,
 *   data-empty (text when nothing matches; empty string = hide the list), data-label-page (group label).
 */
(function () {
  'use strict';
  var d = document, w = window;
  var me = d.currentScript || d.querySelector('script[src*="p1-suggest"]');
  var CFG = me ? me.dataset : {};
  var CACHE = {}, UID = 0;
  var STOP = { a: 1, an: 1, the: 1, my: 1, me: 1, i: 1, is: 1, it: 1, of: 1, to: 1, in: 1, at: 1, on: 1, for: 1, and: 1, or: 1, near: 1, not: 1, no: 1, can: 1, do: 1, does: 1, how: 1, what: 1, where: 1, who: 1, need: 1, want: 1, get: 1, with: 1, from: 1, any: 1, some: 1, please: 1, best: 1 };

  function norm(s) {
    s = String(s || '').toLowerCase();
    try { s = s.normalize('NFD').replace(/[̀-ͯ]/g, ''); } catch (e) {}
    return s.replace(/[^a-z0-9㐀-鿿\s]+/g, ' ').replace(/\s+/g, ' ').trim();
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function hl(text, toks) {
    var out = esc(text);
    toks.forEach(function (t) {
      if (t.length < 2) return;
      var re = new RegExp('(' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'ig');
      out = out.replace(/(<[^>]*>|&[a-z#0-9]+;)|([^<&]+)/g, function (m, tag, txt) { return tag || txt.replace(re, '<mark>$1</mark>'); });
    });
    return out;
  }
  // One edit allowed for words of 5+ letters (typo tolerance, e.g. "gearbx" ~ "gearbox").
  function near(a, b) {
    if (Math.abs(a.length - b.length) > 1) return false;
    var i = 0, j = 0, e = 0;
    while (i < a.length && j < b.length) {
      if (a[i] === b[j]) { i++; j++; continue; }
      if (++e > 1) return false;
      if (a.length > b.length) i++; else if (b.length > a.length) j++; else { i++; j++; }
    }
    return e + (a.length - i) + (b.length - j) <= 1;
  }
  function tokScore(it, t) {
    var name = it._n, hay = it._h;
    if (name.indexOf(t) === 0) return 60;
    if ((' ' + name).indexOf(' ' + t) >= 0) return 45;
    if (t.length >= 3 && name.indexOf(t) >= 0) return 30;
    if ((' ' + hay).indexOf(' ' + t) >= 0) return 20;
    if (t.length >= 4 && hay.indexOf(t) >= 0) return 12;
    if (t.length >= 5) for (var x = 0; x < it._w.length; x++) { var wd = it._w[x]; if (near(t, wd) || near(t, wd.slice(0, t.length))) return 8; }
    return 0;
  }
  // Short queries must match every word. Longer, sentence-style queries ("my vezel aircon not cold near ubi")
  // drop filler words and need at least half the remaining words, so a typed question still gets suggestions.
  // Category and brand chips need one word that starts a word of their name ("ubi" -> Ubi, Ubi Road 1).
  // A typo match (score 8) only shows when nothing matches exactly.
  function score(it, toks) {
    var s = 0, hit = 0, fz = 0, strong = 0;
    for (var k = 0; k < toks.length; k++) {
      var v = tokScore(it, toks[k]);
      if (v) { hit++; s += v; if (v === 8) fz++; if (v >= 45) strong++; }
    }
    var chip = it.t === 'category' || it.t === 'brand';
    var need = chip ? 1 : (toks.length <= 2 ? toks.length : Math.ceil(toks.length / 2));
    if (!hit || hit < need || (chip && toks.length > 1 && !strong)) return 0;
    it._fz = fz > 0;
    if (it.t === 'product') s += 4;
    return s * (hit / toks.length) - Math.min(10, it._n.length / 12);
  }
  function prep(list) {
    return (list || []).filter(function (x) { return x && x.n && x.u; }).map(function (x) {
      x.t = x.t || 'page';
      x._n = norm(x.n);
      x._h = norm([x.n, x.c, x.b, x.k].join(' '));
      x._w = x._h.split(' ');
      return x;
    });
  }
  function load(url) {
    var c = CACHE[url];
    if (c) return c.then ? c : Promise.resolve(c);
    var key = 'p1s:' + url;
    try { var s = sessionStorage.getItem(key); if (s) return Promise.resolve(CACHE[url] = prep(JSON.parse(s))); } catch (e) {}
    CACHE[url] = fetch(url, { credentials: 'same-origin' }).then(function (r) {
      if (!r.ok) throw new Error('index ' + r.status);
      return r.json();
    }).then(function (j) {
      var items = Array.isArray(j) ? j : (j.items || []);
      try { sessionStorage.setItem(key, JSON.stringify(items)); } catch (e) {}
      return (CACHE[url] = prep(items));
    }).catch(function () { delete CACHE[url]; return []; });
    return CACHE[url];
  }
  function fromEndpoint(url, q) {
    return fetch(url + (url.indexOf('?') >= 0 ? '&' : '?') + 'q=' + encodeURIComponent(q), { credentials: 'same-origin', headers: { Accept: 'application/json' } })
      .then(function (r) { return r.ok ? r.json() : []; })
      .then(function (j) { return prep((Array.isArray(j) ? j : (j.items || [])).map(function (x) { if (x.s && x.n) x.n += ' (sold out)'; return x; })); })
      .catch(function () { return []; });
  }

  var LABEL = { product: 'Products', service: 'Services', page: 'Pages', article: 'Articles', category: 'Categories', brand: 'Brands' };
  var ORDER = ['product', 'service', 'page', 'article'];

  function attach(inp) {
    if (inp.dataset.p1sBound) return;
    inp.dataset.p1sBound = '1';
    var o = function (k, def) { return inp.dataset[k] != null ? inp.dataset[k] : (CFG[k] != null ? CFG[k] : def); };
    var MIN = +o('min', 2), DELAY = +o('delay', 160), MAX = +o('max', 6);
    var indexUrl = o('index', ''), endpoint = o('endpoint', ''), BASE = o('base', '').replace(/\/$/, '');
    var labels = {};
    Object.keys(LABEL).forEach(function (t) { labels[t] = o('label' + t.charAt(0).toUpperCase() + t.slice(1), LABEL[t]); });
    var form = inp.form || inp.closest('form');
    var id = 'p1s-' + (++UID), timer = 0, seq = 0, sel = -1, opts = [], lastQ = null;

    var box = d.createElement('div');
    box.className = 'p1s-box';
    box.id = id;
    box.setAttribute('role', 'listbox');
    box.setAttribute('aria-label', 'Search suggestions');
    box.hidden = true;
    var live = d.createElement('div');
    live.className = 'p1s-sr';
    live.setAttribute('aria-live', 'polite');
    d.body.appendChild(box);
    d.body.appendChild(live);

    inp.setAttribute('role', 'combobox');
    inp.setAttribute('aria-autocomplete', 'list');
    inp.setAttribute('aria-expanded', 'false');
    inp.setAttribute('aria-controls', id);
    inp.setAttribute('autocomplete', 'off');

    function url(u) { return BASE && u.charAt(0) === '/' && u.charAt(1) !== '/' ? BASE + u : u; }
    // Fixed under the box, so no parent overflow can clip it. Phones: full width with a 12px gutter.
    function place() {
      var r = inp.getBoundingClientRect(), vw = d.documentElement.clientWidth;
      var vh = w.visualViewport ? w.visualViewport.height : w.innerHeight;
      if (r.bottom < 0 || r.top > vh) { close(); return; }
      box.style.top = Math.round(r.bottom + 6) + 'px';
      box.style.maxHeight = Math.max(180, vh - r.bottom - 18) + 'px';
      if (vw <= 560) { box.style.left = '12px'; box.style.width = (vw - 24) + 'px'; }
      else {
        var width = Math.min(Math.max(r.width, 380), vw - 24), left = r.left;
        if (left + width > vw - 12) left = vw - 12 - width;
        box.style.left = Math.round(left) + 'px';
        box.style.width = Math.round(width) + 'px';
      }
    }
    function close() {
      box.hidden = true; sel = -1;
      inp.setAttribute('aria-expanded', 'false');
      inp.removeAttribute('aria-activedescendant');
    }
    function mark(i) {
      opts.forEach(function (a, k) { a.classList.toggle('on', k === i); a.setAttribute('aria-selected', k === i ? 'true' : 'false'); });
      sel = i;
      if (i >= 0) { inp.setAttribute('aria-activedescendant', opts[i].id); opts[i].scrollIntoView({ block: 'nearest' }); }
      else inp.removeAttribute('aria-activedescendant');
    }
    function allUrl(q) {
      var base = o('allUrl', '') || (form && form.getAttribute('action')) || '';
      if (!base) return '';
      return base + (base.indexOf('?') >= 0 ? '&' : '?') + encodeURIComponent(inp.name || 'q') + '=' + encodeURIComponent(q);
    }
    function render(q, list) {
      var toks = norm(q).split(' ').filter(function (t) { return t && !STOP[t]; });
      if (!toks.length) { close(); return; }
      var scored = list.map(function (it) { return { it: it, s: score(it, toks) }; }).filter(function (x) { return x.s > 0; })
        .sort(function (a, b) { return b.s - a.s; });
      if (scored.some(function (x) { return !x.it._fz; })) scored = scored.filter(function (x) { return !x.it._fz; });
      var main = [], cats = [], brands = [];
      scored.forEach(function (x) {
        if (x.it.t === 'category') { if (cats.length < 4) cats.push(x.it); }
        else if (x.it.t === 'brand') { if (brands.length < 4) brands.push(x.it); }
        else if (main.length < MAX) main.push(x.it);
      });
      main.sort(function (a, b) { return ORDER.indexOf(a.t) - ORDER.indexOf(b.t); });
      var html = '', n = 0, grp = '';
      function opt(cls, inner, href, extra) { return '<a class="' + cls + '" id="' + id + '-' + (n++) + '" role="option" aria-selected="false" href="' + esc(href) + '"' + (extra || '') + '>' + inner + '</a>'; }
      main.forEach(function (it) {
        var g = labels[it.t] || labels.page;
        if (g !== grp) { html += '<div class="p1s-h" role="presentation">' + esc(g) + '</div>'; grp = g; }
        var img = it.i ? '<img src="' + esc(url(it.i)) + '" alt="" width="48" height="48" loading="lazy" decoding="async">' : '<span class="p1s-ph" aria-hidden="true">' + esc((it.n || '?').replace(/^[^A-Za-z0-9]+/, '').charAt(0).toUpperCase()) + '</span>';
        var sub = it.c ? '<small>' + esc(it.c) + '</small>' : '';
        html += opt('p1s-o', img + '<span class="p1s-t"><span class="p1s-n">' + hl(it.n, toks) + '</span>' + sub + '</span>' + (it.p ? '<b class="p1s-p">' + esc(it.p) + '</b>' : ''), url(it.u));
      });
      [['category', cats], ['brand', brands]].forEach(function (pair) {
        if (!pair[1].length) return;
        html += '<div class="p1s-h" role="presentation">' + esc(labels[pair[0]]) + '</div><div class="p1s-chips" role="presentation">';
        pair[1].forEach(function (it) { html += opt('p1s-chip', '<span>' + hl(it.n, toks) + '</span>', url(it.u)); });
        html += '</div>';
      });
      var emptyTxt = o('empty', 'No matches yet. Try another word.');
      if (!n && !emptyTxt) { close(); live.textContent = ''; return; }
      if (!n) html += '<p class="p1s-empty">' + esc(emptyTxt) + '</p>';
      var au = allUrl(q), label = esc(o('allLabel', 'See all results')) + ' for &ldquo;' + esc(q.length > 40 ? q.slice(0, 40) + '…' : q) + '&rdquo;';
      if (au) html += opt('p1s-all', label, au);
      else if (form) html += opt('p1s-all', label, '#', ' data-p1s-submit="1"');
      box.innerHTML = html;
      opts = [].slice.call(box.querySelectorAll('[role=option]'));
      live.textContent = n ? (n + ' suggestions') : 'No suggestions';
      sel = -1;
      box.hidden = false;
      place();
      inp.setAttribute('aria-expanded', 'true');
    }
    function submitForm() {
      close();
      if (typeof form.requestSubmit === 'function') form.requestSubmit();
      else form.dispatchEvent(new Event('submit', { cancelable: true, bubbles: true }));
    }
    function go(a) {
      if (a.hasAttribute('data-p1s-submit')) submitForm();
      else location.href = a.href;
    }
    function run() {
      var q = inp.value.trim();
      if (q.length < MIN) { close(); lastQ = null; return; }
      if (q === lastQ && !box.hidden) return;
      lastQ = q;
      var my = ++seq;
      var p = endpoint ? fromEndpoint(endpoint, q) : load(indexUrl);
      p.then(function (list) { if (my === seq && inp.value.trim() === q && d.activeElement === inp) render(q, list); });
    }
    inp.addEventListener('input', function () { clearTimeout(timer); timer = setTimeout(run, DELAY); });
    inp.addEventListener('focus', function () { if (!endpoint && indexUrl) load(indexUrl); if (inp.value.trim().length >= MIN) { lastQ = null; run(); } });
    inp.addEventListener('blur', function () { setTimeout(function () { if (d.activeElement !== inp) close(); }, 150); });
    // Keys are taken in the capture phase, so a site's own Enter handler (e.g. "Enter = search")
    // does not fire when the visitor is choosing a suggestion.
    d.addEventListener('keydown', function (e) {
      if (e.target !== inp) return;
      var k = e.key;
      if (box.hidden || !opts.length) {
        if (k === 'ArrowDown' && inp.tagName !== 'TEXTAREA' && inp.value.trim().length >= MIN) { e.preventDefault(); lastQ = null; run(); }
        return;
      }
      if (k === 'ArrowDown' || k === 'ArrowUp') {
        e.preventDefault(); e.stopPropagation();
        var len = opts.length;
        // Down past the last row, or Up from the first, goes back to the typed text.
        mark(k === 'ArrowDown' ? (sel + 1 >= len ? -1 : sel + 1) : (sel <= -1 ? len - 1 : sel - 1));
      } else if (k === 'Enter' && sel >= 0) { e.preventDefault(); e.stopPropagation(); go(opts[sel]); }
      else if (k === 'Enter') close();
      else if (k === 'Escape') { e.preventDefault(); e.stopPropagation(); close(); }
      else if (k === 'Tab') close();
    }, true);
    // Tap support: keep focus while the finger or mouse is on the list, so the tap lands on the link.
    box.addEventListener('pointerdown', function (e) { if (e.pointerType === 'mouse') e.preventDefault(); });
    box.addEventListener('mousedown', function (e) { e.preventDefault(); });
    box.addEventListener('click', function (e) { var a = e.target.closest('[role=option]'); if (a && a.hasAttribute('data-p1s-submit')) { e.preventDefault(); submitForm(); } });
    box.addEventListener('mousemove', function (e) { var a = e.target.closest('[role=option]'); if (a && opts.indexOf(a) !== sel) mark(opts.indexOf(a)); });
    d.addEventListener('pointerdown', function (e) { if (!box.contains(e.target) && e.target !== inp) close(); });
    w.addEventListener('resize', function () { if (!box.hidden) place(); });
    if (w.visualViewport) w.visualViewport.addEventListener('resize', function () { if (!box.hidden) place(); });
    w.addEventListener('scroll', function () { if (!box.hidden) place(); }, { passive: true });
  }

  function targets() {
    var marked = d.querySelectorAll('input[data-p1-suggest], textarea[data-p1-suggest]');
    if (marked.length) return [].slice.call(marked);
    return [].slice.call(d.querySelectorAll('input[type=search], form[role=search] input[type=text], form[role=search] textarea, input[name=q], input[name=s], input[name=search], input[name=query], input[name=keyword]'))
      .filter(function (x) { return x.type !== 'hidden' && !x.closest('[data-p1-suggest-off]'); });
  }
  function init() { targets().forEach(attach); }
  w.P1Suggest = { version: '1.0.0', attach: attach, init: init };
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', init); else init();
})();
