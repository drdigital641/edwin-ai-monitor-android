/* SH Auto Parts - public site script: owner-language search, catalogue UI, enquiry form, motion.
   Data = window.SH_DATA (data.js, SAMPLE entries) merged with staff changes in localStorage (sh_entries_v1). Works in node for tests. */
(function (root) {
  'use strict';
  var D = root.SH_DATA;
  var ROOT = root.SH_ROOT || '';
  var K = { ov: 'sh_entries_v1', enq: 'sh_enq_v1' };

  /* ---------- storage (every access guarded) ---------- */
  function lsGet(k, d) { try { var v = root.localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function lsSet(k, v) { try { root.localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function overlay() { var o = lsGet(K.ov, null) || {}; return { ov: o.ov || {}, add: o.add || [], del: o.del || [] }; }
  function saveOverlay(o) { return lsSet(K.ov, o); }
  function allEntries(includeHidden) {
    var o = overlay(), del = {}, out = [];
    o.del.forEach(function (i) { del[i] = 1; });
    D.entries.forEach(function (x) { if (!del[x.id]) out.push(o.ov[x.id] ? Object.assign({}, x, o.ov[x.id]) : x); });
    o.add.forEach(function (x) { out.push(x); });
    return includeHidden ? out : out.filter(function (x) { return x.pub !== false; });
  }

  /* ---------- text helpers ---------- */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function norm(s) { return String(s || '').toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, ' ').trim().replace(/\s+/g, ' '); }
  function stem(t) { return (t.length > 3 && t.slice(-1) === 's' && t.slice(-2) !== 'ss' && t !== 'lens') ? t.slice(0, -1) : t; }
  function toks(s) { var n = norm(s); return n ? n.split(' ').map(stem) : []; }
  function slug(s) { return norm(s).replace(/ /g, '-'); }
  var STOP = {}; 'for the a an my our car cars part parts spare new need needs looking want buy sell left right lh rh set pcs pc of and to with model please do you have got is any'.split(' ').forEach(function (w) { STOP[stem(w)] = 1; });

  /* ---------- index (built once) ---------- */
  var IDX = null;
  function seqOf(s) { return toks(s); }
  function build() {
    var I = { parts: [], brands: [], models: [], vocab: {} };
    function vocab(seq) { seq.forEach(function (t) { if (t.length >= 4 && !/^\d+$/.test(t)) I.vocab[t] = 1; }); }
    D.parts.forEach(function (p) {
      var all = p.syn.concat([p.name]);
      all.forEach(function (s) { var q = seqOf(s); if (q.length) { I.parts.push({ seq: q, map: (function () { var m = {}; m[p.slug] = 1; return m; })(), specific: 1 }); vocab(q); } });
    });
    D.generic.forEach(function (g) { var q = seqOf(g.w); I.parts.push({ seq: q, map: g.map, specific: 0 }); vocab(q); });
    I.parts.sort(function (a, b) { return b.seq.length - a.seq.length || b.specific - a.specific; });
    D.brands.forEach(function (b) {
      b.aliases.concat([b.name]).forEach(function (a) { var q = seqOf(a); if (q.length) { I.brands.push({ seq: q, brand: b.slug }); vocab(q); } });
      b.models.forEach(function (m) {
        var seen = {};
        function add(a, nb) { var q = seqOf(a); var key = q.join(' ') + '|' + nb; if (!q.length || seen[key]) return; seen[key] = 1; I.models.push({ seq: q, brand: b.slug, model: m.slug, nb: nb }); vocab(q); }
        add(m.name, /^[0-9a-z]{1,3}$/.test(norm(m.name)) || /^\d+$/.test(norm(m.name)) ? 1 : 0);
        m.aka.forEach(function (a) { add(a, 0); });
        m.nb.forEach(function (a) { add(a, 1); });
        add(b.name + ' ' + m.name, 0);
        add(b.name + m.name, 0);
      });
    });
    I.brands.sort(function (a, b) { return b.seq.length - a.seq.length; });
    I.models.sort(function (a, b) { return b.seq.length - a.seq.length; });
    return I;
  }
  function find(t, used, seq) {
    for (var i = 0; i + seq.length <= t.length; i++) {
      var ok = true;
      for (var j = 0; j < seq.length; j++) { if (used[i + j] || t[i + j] !== seq[j]) { ok = false; break; } }
      if (ok) return i;
    }
    return -1;
  }
  function lev(a, b, max) {
    if (Math.abs(a.length - b.length) > max) return max + 1;
    var p = [], i, j;
    for (j = 0; j <= b.length; j++) p[j] = j;
    for (i = 1; i <= a.length; i++) {
      var c = [i], min = i;
      for (j = 1; j <= b.length; j++) { c[j] = Math.min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); if (c[j] < min) min = c[j]; }
      if (min > max) return max + 1;
      p = c;
    }
    return p[b.length];
  }
  function fix(t) { /* one-typo tolerance on long words that are not known */
    return t.map(function (w) {
      if (w.length < 5 || IDX.vocab[w] || /\d/.test(w)) return w;
      var best = null, bd = w.length >= 8 ? 2 : 1;
      for (var v in IDX.vocab) { var d = lev(w, v, bd); if (d <= bd && (best === null || d < bd)) { best = v; bd = d; if (d === 0) break; } }
      return best || w;
    });
  }

  /* ---------- parse a query into brand / model / part ---------- */
  function parse(q) {
    if (!IDX) IDX = build();
    var t = fix(toks(q)), used = t.map(function () { return false; });
    var R = { tokens: t, brand: null, model: null, parts: {}, hasPart: false, left: [] };
    var i, k, hit;
    IDX.parts.forEach(function (p) {
      if (find(t, used, p.seq) >= 0) {
        var at = find(t, used, p.seq);
        for (k = 0; k < p.seq.length; k++) used[at + k] = true;
        for (var s in p.map) R.parts[s] = Math.max(R.parts[s] || 0, p.map[s]);
        R.hasPart = true;
      }
    });
    var brandHit = null, brandAt = null;
    for (i = 0; i < IDX.brands.length; i++) { hit = find(t, used, IDX.brands[i].seq); if (hit >= 0) { brandHit = IDX.brands[i].brand; brandAt = [hit, IDX.brands[i].seq.length]; break; } }
    var hasModelWord = t.indexOf('model') >= 0;
    for (i = 0; i < IDX.models.length; i++) {
      var m = IDX.models[i];
      if (m.nb && !(brandHit === m.brand)) continue;
      hit = find(t, used, m.seq);
      if (hit >= 0) { for (k = 0; k < m.seq.length; k++) used[hit + k] = true; R.model = m.model; R.brand = m.brand; break; }
    }
    if (!R.model && brandHit) { R.brand = brandHit; }
    if (brandAt && R.brand === brandHit) { for (k = 0; k < brandAt[1]; k++) used[brandAt[0] + k] = true; }
    t.forEach(function (w, j) { if (!used[j] && !STOP[w] && w !== 'model') R.left.push(w); });
    return R;
  }

  /* ---------- search ---------- */
  var DEF = { ask: 'Ask for availability', stock: 'In stock', order: 'Can order' };
  function words(e) { return toks([e.title, e.side, e.note, e.partName, e.brandName, e.model].join(' ')); }
  function search(q, opts) {
    opts = opts || {};
    var pool = opts.pool || allEntries();
    var P = parse(q), out = [], i;
    var anyKey = !!(P.brand || P.model || P.hasPart);
    if (!norm(q)) return { q: q, P: P, results: pool.map(function (e, n) { return { e: e, score: 0, n: n }; }), weak: false, empty: true };
    pool.forEach(function (e, n) {
      var s = 0;
      if (P.brand && e.brand !== P.brand) return;
      if (P.brand) s += 20;
      if (P.model) { if (e.modelSlug === P.model && e.brand === P.brand) s += 50; }
      if (P.hasPart) { var w = P.parts[e.part] || 0; if (!w) return; s += 40 * w; }
      if (anyKey) {
        if (P.left.length) { var ew = words(e); P.left.forEach(function (l) { if (ew.indexOf(l) >= 0) s += 6; }); }
        out.push({ e: e, score: s, n: n });
      } else {
        var ew2 = words(e), hits = 0;
        P.tokens.forEach(function (tk) { if (STOP[tk]) return; for (var j = 0; j < ew2.length; j++) { if (ew2[j] === tk || (tk.length >= 3 && ew2[j].indexOf(tk) === 0)) { hits++; break; } } });
        var need = P.tokens.filter(function (tk) { return !STOP[tk]; }).length;
        if (need && hits >= need) out.push({ e: e, score: 10 * hits, n: n });
      }
    });
    if (out.length) {
      var max = 0; out.forEach(function (r) { if (r.score > max) max = r.score; });
      var cut = anyKey ? Math.max(1, max * 0.55) : 1;
      out = out.filter(function (r) { return r.score >= cut || (!P.model && !P.hasPart); });
      out.sort(function (a, b) { return b.score - a.score || a.n - b.n; });
    }
    var unk = P.left.filter(function (l) { return l.length >= 4 && !out.some(function (r) { return words(r.e).indexOf(l) >= 0; }); });
    var weak = !out.length || !anyKey || (anyKey && unk.length > 0) || (!!P.model && !out.some(function (r) { return r.e.modelSlug === P.model; }));
    return { q: q, P: P, results: out, weak: weak, empty: false };
  }
  function brandName(slugv) { for (var i = 0; i < D.brands.length; i++) if (D.brands[i].slug === slugv) return D.brands[i].name; return ''; }
  function modelName(b, m) { for (var i = 0; i < D.brands.length; i++) if (D.brands[i].slug === b) for (var j = 0; j < D.brands[i].models.length; j++) if (D.brands[i].models[j].slug === m) return D.brands[i].models[j].name; return ''; }
  function partName(s) { for (var i = 0; i < D.parts.length; i++) if (D.parts[i].slug === s) return D.parts[i].name; return ''; }

  /* ---------- links ---------- */
  function enqHref(e) {
    var veh = ((e.brandName || '') + ' ' + (e.model || '')).trim();
    if (D.wa) return 'https://wa.me/' + D.wa + '?text=' + encodeURIComponent("Hi SH Auto Parts, I'm looking for: " + e.partName + (veh ? ' for ' + veh : '') + '. (from website)');
    return ROOT + 'enquiry/?q=' + encodeURIComponent(e.partName + (veh ? ' for ' + veh : '')) + '&brand=' + encodeURIComponent(e.brand) + '&model=' + encodeURIComponent(e.model || '') + '&part=' + encodeURIComponent(e.part);
  }
  function enqFree(text) {
    if (D.wa) return 'https://wa.me/' + D.wa + '?text=' + encodeURIComponent("Hi SH Auto Parts, I'm looking for: " + (text || 'a part') + '. (from website)');
    return ROOT + 'enquiry/?q=' + encodeURIComponent(text || '');
  }

  /* ---------- rendering ---------- */
  function iconSvg(p) { return '<svg class="ic" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (D.icons[p] || D.icons.other) + '</svg>'; }
  function hlTitle(e, P) {
    var set = {};
    function addw(s) { norm(s).split(' ').forEach(function (w) { if (w) set[w] = 1; set[stem(w)] = 1; }); }
    if (P) {
      if (P.brand && P.brand === e.brand) addw(e.brandName);
      if (P.model && P.model === e.modelSlug) addw(e.model);
      if (P.parts && P.parts[e.part]) addw(e.partName);
    }
    return String(e.title).split(' ').map(function (w) { var n = norm(w); return n && (set[n] || set[stem(n)]) ? '<mark>' + esc(w) + '</mark>' : esc(w); }).join(' ');
  }
  function card(e, P) {
    var veh = ((e.brandName || '') + ' ' + (e.model || '')).trim() || e.brandName;
    var st = e.status || 'ask';
    var media = e.photo ? '<img src="' + esc(e.photo) + '" alt="' + esc(e.title) + '" loading="lazy" onerror="this.remove()">' : '';
    return '<article class="rc"><div class="rc-ic">' + iconSvg(e.part) + media + '</div><div class="rc-b">' +
      '<span class="chip">' + esc(veh) + (e.model ? '' : ' &middot; ask us for the model') + '</span>' +
      '<h3>' + hlTitle(e, P) + '</h3>' +
      '<p class="rc-t">' + esc(e.partName) + (e.side ? ' &middot; ' + esc(e.side) : '') + '</p>' +
      '<div class="rc-m"><span class="pill st-' + esc(st) + '">' + esc(D.status[st] || DEF.ask) + '</span>' + (e.price ? '<span class="price">' + esc(e.price) + '</span>' : '') +
      (e.sample ? '<span class="smp">Sample listing - staff to confirm</span>' : '') + '</div>' +
      '<div class="rc-a"><a class="btn btn-p btn-s" href="' + esc(enqHref(e)) + '">Enquire</a><button type="button" class="btn btn-g btn-s" data-det="' + esc(e.id) + '">Details</button></div></div></article>';
  }
  function understood(P) {
    var c = [];
    if (P.brand) c.push(brandName(P.brand));
    if (P.model) c.push(modelName(P.brand, P.model));
    Object.keys(P.parts).filter(function (s) { return P.parts[s] >= 1; }).forEach(function (s) { c.push(partName(s)); });
    if (!c.length && P.hasPart) { var g = Object.keys(P.parts); g.slice(0, 1).forEach(function (s) { c.push('Lamps / bumpers'); }); }
    return c.length ? '<p class="und">Looking for: ' + c.map(function (x) { return '<b>' + esc(x) + '</b>'; }).join(' &middot; ') + '</p>' : '';
  }
  function notListed(q) {
    return '<div class="nl"><h3>We may still have it</h3><p>Not listed, or not sure? Send us your car and the part' + (q ? ' (&ldquo;' + esc(q) + '&rdquo;)' : '') + '. We confirm fitment and reply.</p>' +
      '<a class="btn btn-p" href="' + esc(enqFree(q)) + '">Send us your car and part</a>' + (D.wa ? '' : '<span class="pvn">Preview note: WhatsApp number pending. This opens the enquiry form.</span>') + '</div>';
  }
  function renderSearch(box, q, o) {
    o = o || {};
    var r = search(q, { pool: o.pool });
    var list = r.results, n = list.length, lim = o.limit || 24;
    var shown = list.slice(0, o.shown || lim);
    var h = '';
    if (!norm(q) && !o.showAll) { box.innerHTML = ''; box.classList.remove('on'); return r; }
    box.classList.add('on');
    if (norm(q)) h += understood(r.P);
    if (norm(q) && r.weak && n) h += '<p class="weak">No exact match for that car and part. Showing the nearest sample listings. We may still have it, so send us your car and part.</p>';
    if (norm(q) && !n) h += '<p class="weak">No sample listing matches that yet.</p>';
    if (n) {
      h += '<div class="rgrid">' + shown.map(function (x) { return card(x.e, r.P); }).join('') + '</div>';
      if (o.seeAll && n > shown.length) h += '<p class="seeall"><a class="btn btn-g" href="' + esc(o.seeAll + '?q=' + encodeURIComponent(q)) + '">See all ' + n + ' results</a></p>';
      if (o.more && n > shown.length) h += '<p class="seeall"><button type="button" class="btn btn-g" data-more="1">Show more (' + (n - shown.length) + ')</button></p>';
    }
    h += notListed(norm(q) ? q : '');
    box.innerHTML = h;
    return r;
  }

  /* ---------- UI wiring (browser only) ---------- */
  var toastT;
  function toast(m) { if (typeof document === 'undefined') return; var t = document.getElementById('toast'); if (!t) return; t.textContent = m; t.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(function () { t.classList.remove('on'); }, 2600); }
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function debounce(f, ms) { var t; return function () { var a = arguments; clearTimeout(t); t = setTimeout(function () { f.apply(null, a); }, ms); }; }

  function modal(e) {
    var m = $('#det'); if (m) m.remove();
    var veh = ((e.brandName || '') + ' ' + (e.model || '')).trim();
    m = document.createElement('div'); m.id = 'det'; m.className = 'modal'; m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true'); m.setAttribute('aria-label', e.title);
    m.innerHTML = '<div class="m-box"><button class="m-x" aria-label="Close" type="button">&times;</button><div class="m-ic">' + iconSvg(e.part) + '</div><p class="kick">' + esc(veh || e.brandName) + '</p><h2>' + esc(e.title) + '</h2>' +
      '<dl class="facts"><div><dt>Part type</dt><dd>' + esc(e.partName) + '</dd></div>' + (e.side ? '<div><dt>Side</dt><dd>' + esc(e.side) + '</dd></div>' : '') +
      '<div><dt>Status</dt><dd>' + esc(D.status[e.status || 'ask']) + '</dd></div>' + (e.price ? '<div><dt>Price</dt><dd>' + esc(e.price) + '</dd></div>' : '') +
      (e.note ? '<div><dt>Note</dt><dd>' + esc(e.note) + '</dd></div>' : '') + '</dl>' +
      (e.sample ? '<p class="smp big">Sample listing - staff to confirm. Fitment and availability are confirmed when you enquire.</p>' : '') +
      '<div class="btns"><a class="btn btn-p" href="' + esc(enqHref(e)) + '">Enquire about this part</a><button type="button" class="btn btn-g m-c">Close</button></div></div>';
    document.body.appendChild(m); document.body.classList.add('noscroll');
    function close() { m.remove(); document.body.classList.remove('noscroll'); document.removeEventListener('keydown', key); }
    function key(ev) { if (ev.key === 'Escape') close(); }
    m.addEventListener('click', function (ev) { if (ev.target === m || ev.target.closest('.m-x,.m-c')) close(); });
    document.addEventListener('keydown', key);
    var f = $('.m-x', m); if (f) f.focus();
  }

  function initSearchBox(form) {
    var id = form.getAttribute('data-search'), input = $('.sin', form), res = $('.sres', form) || document.getElementById(id.replace(/q$/, '') + '-res');
    var home = id === 'hq', cat = id === 'cq';
    if (cat) return;
    if (!res) return;
    var run = function () { renderSearch(res, input.value, { limit: home ? 6 : 6, seeAll: ROOT + 'catalogue/' }); };
    input.addEventListener('input', debounce(run, 120));
    $$('[data-try]', form).forEach(function (b) { b.addEventListener('click', function () { input.value = b.getAttribute('data-try'); run(); input.focus({ preventScroll: true }); if (res.scrollIntoView && home && window.innerWidth < 760) setTimeout(function () { res.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 60); }); });
    var u = new URLSearchParams(location.search); if (u.get('q') && home) { input.value = u.get('q'); run(); }
  }

  function initCatalogue() {
    var form = document.getElementById('cat-form'); if (!form) return;
    var input = $('#cq-q'), res = document.getElementById('cat-res'), count = document.getElementById('cat-count');
    var fb = $('#f-brand'), fm = $('#f-model'), fp = $('#f-part'), shown = 24;
    function fillModels() {
      var b = D.brands.filter(function (x) { return x.slug === fb.value; })[0];
      var cur = fm.value; fm.innerHTML = '<option value="">All models</option>';
      if (b) b.models.forEach(function (m) { fm.insertAdjacentHTML('beforeend', '<option value="' + m.slug + '">' + esc(m.name) + '</option>'); });
      fm.disabled = !b || !b.models.length; if (cur) fm.value = cur;
    }
    function pool() {
      return allEntries().filter(function (e) { return (!fb.value || e.brand === fb.value) && (!fm.value || e.modelSlug === fm.value) && (!fp.value || e.part === fp.value); });
    }
    function run(reset) {
      if (reset) shown = 24;
      var q = input.value, p = pool();
      var r = renderSearch(res, q, { pool: p, shown: shown, showAll: true, more: true, limit: 24 });
      var n = r.results.length;
      count.innerHTML = '<b>' + n + '</b> ' + (n === 1 ? 'listing' : 'listings') + (norm(q) ? ' for &ldquo;' + esc(q) + '&rdquo;' : '') + ' <span class="mu">(sample listings)</span>';
      var u = new URLSearchParams(); if (q) u.set('q', q); if (fb.value) u.set('brand', fb.value); if (fm.value) u.set('model', fm.value); if (fp.value) u.set('part', fp.value);
      try { history.replaceState(null, '', location.pathname + (u.toString() ? '?' + u.toString() : '')); } catch (e) { }
    }
    function match(sel, v) { if (!v) return ''; var s = slug(v); for (var i = 0; i < sel.options.length; i++) if (sel.options[i].value === v || slug(sel.options[i].text) === s) return sel.options[i].value; return ''; }
    var u = new URLSearchParams(location.search);
    fb.value = match(fb, u.get('brand')); fillModels(); fm.value = match(fm, u.get('model')); fp.value = match(fp, u.get('part')); input.value = u.get('q') || '';
    fb.addEventListener('change', function () { fm.value = ''; fillModels(); run(true); });
    fm.addEventListener('change', function () { run(true); }); fp.addEventListener('change', function () { run(true); });
    input.addEventListener('input', debounce(function () { run(true); }, 120));
    form.addEventListener('submit', function (ev) { ev.preventDefault(); run(true); });
    $('#f-clear').addEventListener('click', function () { input.value = ''; fb.value = ''; fm.value = ''; fp.value = ''; fillModels(); run(true); });
    $$('[data-try]', form).forEach(function (b) { b.addEventListener('click', function () { input.value = b.getAttribute('data-try'); fb.value = ''; fm.value = ''; fp.value = ''; fillModels(); run(true); }); });
    res.addEventListener('click', function (ev) { if (ev.target.closest('[data-more]')) { shown += 24; run(false); } });
    run(true);
  }

  function initLists() {
    $$('[data-list]').forEach(function (box) {
      var spec = box.getAttribute('data-list').split(':'), lim = +box.getAttribute('data-limit') || 9, all = allEntries(), list, href;
      if (spec[0] === 'brand') { list = all.filter(function (e) { return e.brand === spec[1]; }); href = ROOT + 'catalogue/?brand=' + spec[1]; }
      else { var ps = spec[1].split(','); list = all.filter(function (e) { return ps.indexOf(e.part) >= 0; }); href = ROOT + 'catalogue/?part=' + ps[0]; }
      /* spread across parts/models so the first screen is varied */
      box.innerHTML = '<div class="rgrid">' + list.slice(0, lim).map(function (e) { return card(e); }).join('') + '</div>' +
        '<p class="seeall"><a class="btn btn-g" href="' + esc(href) + '">See all ' + list.length + ' listings</a></p>';
    });
  }

  function initEnquiry() {
    var f = document.getElementById('enq-form'); if (!f) return;
    var u = new URLSearchParams(location.search), q = u.get('q') || '', b = u.get('brand') || '', m = u.get('model') || '';
    if (q) { var pt = q.split(' for ')[0]; f.part.value = pt; var br = f.brand; if (b) { for (var i = 0; i < br.options.length; i++) if (br.options[i].value === b) br.value = b; } if (m) { var mn = ''; D.brands.forEach(function (x) { x.models.forEach(function (y) { if (y.slug === m) mn = y.name; }); }); f.model.value = mn || m; } else if (q.indexOf(' for ') > 0) { var rest = q.split(' for ')[1]; f.model.value = rest; } }
    if (u.get('as') === 'owner' || u.get('as') === 'workshop') f.as.value = u.get('as');
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var ok = f.name.value.trim() && f.contact.value.trim() && f.part.value.trim() && f.consent.checked;
      document.getElementById('enq-err').hidden = !!ok; if (!ok) return;
      var list = lsGet(K.enq, []);
      list.unshift({ id: 'q' + Date.now().toString(36), t: new Date().toISOString(), as: f.as.value, name: f.name.value.trim(), contact: f.contact.value.trim(), brand: f.brand.value, model: f.model.value.trim(), part: f.part.value.trim(), note: f.note.value.trim(), done: false });
      lsSet(K.enq, list.slice(0, 200));
      f.hidden = true; document.getElementById('enq-ok').hidden = false; window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  function initChrome() {
    var bg = $('.burger'), nav = $('#nav');
    if (bg && nav) {
      bg.addEventListener('click', function () { var o = document.body.classList.toggle('menu'); bg.setAttribute('aria-expanded', o ? 'true' : 'false'); bg.setAttribute('aria-label', o ? 'Close menu' : 'Open menu'); });
      $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { document.body.classList.remove('menu'); bg.setAttribute('aria-expanded', 'false'); }); });
    }
    var hd = $('.hd'); if (hd) { var f = function () { hd.classList.toggle('scr', window.scrollY > 8); }; window.addEventListener('scroll', f, { passive: true }); f(); }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
      $$('.rv').forEach(function (el) { io.observe(el); });
    } else { $$('.rv').forEach(function (el) { el.classList.add('in'); }); }
    document.addEventListener('click', function (ev) {
      var d = ev.target.closest('[data-det]'); if (!d) return;
      var id = d.getAttribute('data-det'), e = allEntries(true).filter(function (x) { return x.id === id; })[0]; if (e) modal(e);
    });
    var wa = $$('a[href*="/enquiry/"]'); /* keep nothing special */
  }

  function init() {
    $$('[data-search]').forEach(initSearchBox);
    initCatalogue(); initLists(); initEnquiry(); initChrome();
  }

  root.SH = { D: D, K: K, ROOT: ROOT, lsGet: lsGet, lsSet: lsSet, overlay: overlay, saveOverlay: saveOverlay, allEntries: allEntries, search: search, parse: parse, norm: norm, esc: esc, slug: slug,
    brandName: brandName, modelName: modelName, partName: partName, enqHref: enqHref, toast: toast, card: card };
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  }
})(typeof window !== 'undefined' ? window : globalThis);
