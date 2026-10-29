/* Mega Power mockup - public site logic: catalogue store, part search, enquiry list, lead forms (demo storage in this browser). */
(function () {
  'use strict';
  var D = window.MP_DATA || { products: [], cats: [] };
  var ROOT = window.MP_ROOT || document.documentElement.getAttribute('data-root') || '';
  var LS = {
    get: function (k, d) { try { var v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } },
    del: function (k) { try { localStorage.removeItem(k); } catch (e) {} }
  };
  var K = { prod: 'mp_products_v1', rfq: 'mp_rfq_v1', leads: 'mp_leads_v1', ev: 'mp_events_v1' };
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  var CATS = {}; D.cats.forEach(function (c) { CATS[c.slug] = c; });

  /* ---------- catalogue store (public data + staff changes saved in this browser) ---------- */
  function allProducts() {
    var saved = LS.get(K.prod, null);
    if (saved && saved.read === D.read && Array.isArray(saved.items)) return saved.items;
    return D.products.map(function (p) { return JSON.parse(JSON.stringify(p)); });
  }
  function saveProducts(items) { return LS.set(K.prod, { read: D.read, items: items }); }
  function published() { return allProducts().filter(function (p) { return p.status === 'published'; }); }
  function byId(id) { return allProducts().filter(function (p) { return p.id === id; })[0]; }
  function purl(p) { return p.src === 'public' && p.url ? ROOT + p.url : ROOT + 'our-products/item.html?id=' + encodeURIComponent(p.id); }
  function catName(s) { return CATS[s] ? CATS[s].name : s; }
  function ph(p) { return ROOT + 'img/ph-' + ((CATS[p.cat] || {}).icon || 'comp') + '.svg'; }
  function pimg(p) { return (p.images && p.images[0]) || p.image || ph(p); }

  /* ---------- tracking (demo: kept in this browser for the staff "search insights") ---------- */
  function track(name, data) {
    var ev = LS.get(K.ev, []); ev.push({ e: name, d: data || {}, t: Date.now(), p: location.pathname });
    if (ev.length > 400) ev = ev.slice(-400);
    LS.set(K.ev, ev);
    try { (window.dataLayer = window.dataLayer || []).push({ event: name, mp: data || {} }); } catch (e) {}
  }

  /* ---------- search ---------- */
  function norm(s) { return String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, ''); }
  var STOP = {};
  'A AN THE FOR OF AND TO WITH CAR CARS AUTO AUTOMOTIVE AIRCON AIRCOND AC AIR CON CONDITIONING CONDITIONER PART PARTS SPARE SPARES OEM NO NUMBER REF PN SG SINGAPORE LAND NEED WANT PRICE'.split(' ').forEach(function (w) { STOP[w] = 1; });
  var SYN = { VW: 'VOLKSWAGEN', VOLKS: 'VOLKSWAGEN', MERC: 'MERCEDES', MERCEDESBENZ: 'MERCEDES', BENZ: 'MERCEDES', MB: 'MERCEDES', MERCEDEZ: 'MERCEDES',
    LANDROVER: 'ROVER', RANGEROVER: 'ROVER', CONDENSOR: 'CONDENSER', CONDENSERS: 'CONDENSER', COMPRESSORS: 'COMPRESSOR', COMPRESOR: 'COMPRESSOR', COMP: 'COMPRESSOR',
    FANS: 'FAN', MOTORS: 'MOTOR', BLOWERS: 'BLOWER', COILS: 'COIL', EVAPORATORS: 'EVAPORATOR', FILTERS: 'FILTER', VALVES: 'VALVE', DRIERS: 'DRIER', DRYERS: 'DRIER', DRYER: 'DRIER',
    MACHINES: 'MACHINE', REFRIGERANTS: 'REFRIGERANT', FREON: 'REFRIGERANT', R134A: 'R134', HFO1234YF: 'R1234YF', '1234YF': 'R1234YF', ACCESSORIES: 'ACCESSORY' };
  var CATKW = { COMPRESSOR: 'compressors', CONDENSER: 'condenser', COIL: 'cooling-coil', EVAPORATOR: 'cooling-coil', FAN: 'fans-and-motors', BLOWER: 'fans-and-motors', MOTOR: 'fans-and-motors',
    FILTER: 'filters', VALVE: 'valves', DRIER: 'driers', RECEIVER: 'driers', ACCESSORY: 'accessories', EQUIPMENT: 'equipment', MACHINE: 'machines', OIL: 'compressor-oil', REFRIGERANT: 'refrigerant', GAS: 'refrigerant' };
  var MAKES = {};
  'VOLKSWAGEN MERCEDES ROVER RANGE BMW PORSCHE AUDI TOYOTA HONDA NISSAN MAZDA MITSUBISHI SUBARU SUZUKI DAIHATSU LEXUS INFINITI HYUNDAI KIA VOLVO FORD CHEVROLET OPEL PEUGEOT CITROEN RENAULT FIAT ALFA JAGUAR MINI SKODA SEAT TESLA BYD ISUZU HINO SCANIA MAN IVECO PROTON PERODUA'.split(' ').forEach(function (m) { MAKES[m] = 1; });
  function canon(t) { return SYN[t] || t; }
  function isYear(t) { return /^(19[89]\d|20[0-4]\d)$/.test(t); }
  function isCode(t) { return /\d/.test(t) && /[A-Z]/.test(t) || /^\d{3,}$/.test(t); }
  function lev(a, b) {
    if (Math.abs(a.length - b.length) > 2) return 9;
    var m = [], i, j; for (i = 0; i <= b.length; i++) m[i] = [i];
    for (j = 0; j <= a.length; j++) m[0][j] = j;
    for (i = 1; i <= b.length; i++) for (j = 1; j <= a.length; j++) m[i][j] = Math.min(m[i - 1][j] + 1, m[i][j - 1] + 1, m[i - 1][j - 1] + (b[i - 1] === a[j - 1] ? 0 : 1));
    return m[b.length][a.length];
  }
  function words(s) { return String(s || '').toUpperCase().split(/[^A-Z0-9]+/).filter(Boolean); }
  function index(p) {
    if (p._ix) return p._ix;
    var T = {}, add = function (list, w) { list.forEach(function (x) { x = canon(x); if (!x || STOP[x]) return; if (!T[x] || T[x] < w) T[x] = w; }); };
    add(words(p.name), 1); add(words(p.orig), 1); add(words(p.brand), 2); add(words(p.gas), 1); add(words(p.oil), 1); add(words((p.tags || []).join(' ')), 2);
    add(words(p.model), 4); add((p.codes || []).map(norm), 5); add(words(p.make), 3);
    if (p.make) add([norm(p.make)], 3);
    add(words(catName(p.cat)), 3);
    Object.keys(CATKW).forEach(function (k) { if (CATKW[k] === p.cat) T[k] = 3; });
    var refs = (p.refs || []).map(function (r) { return norm(r.n); }).filter(Boolean);
    var mk = {}; words(p.make).map(canon).forEach(function (w) { mk[w] = 1; }); if (p.make) mk[canon(norm(p.make))] = 1;
    var digits = (p.codes || []).concat(words(p.model)).map(function (c) { return norm(c).replace(/\D/g, ''); }).filter(function (d) { return d.length >= 3; });
    p._ix = { T: T, refs: refs, mk: mk, digits: digits };
    return p._ix;
  }
  function search(q, opt) {
    opt = opt || {};
    var list = (opt.items || published()).filter(function (p) { return !opt.cat || p.cat === opt.cat; });
    var qn = norm(q), raw = String(q || '').toUpperCase().split(/[\s,;/|]+/).map(norm).filter(Boolean);
    var toks = raw.map(canon).filter(function (t) { return !STOP[t]; });
    var cats = {}, year = opt.year && isYear(String(opt.year)) ? +opt.year : null, qmake = null;
    toks.forEach(function (t) { if (CATKW[t]) cats[CATKW[t]] = 1; if (isYear(t)) year = +t; if (MAKES[t]) qmake = t; });
    if (cats['compressor-oil'] && cats.compressors) delete cats.compressors;
    var res = [], related = [];
    list.forEach(function (p) {
      var ix = index(p), kind = null, score = 0, why = '';
      // 1) reference numbers
      ix.refs.forEach(function (r) {
        if (kind === 'exact') return;
        if (r && (r === qn || raw.indexOf(r) >= 0 && r.length >= 4)) { kind = 'exact'; score = 1000; why = 'ref'; }
        else if (qn.length >= 5 && r.length >= 5 && (r.indexOf(qn) >= 0 || qn.indexOf(r) >= 0)) { if (!kind) { kind = 'possible'; score = 400; why = 'partial-ref'; } }
      });
      if (kind !== 'exact' && toks.length) {
        var hits = 0, soft = 0, fail = false, unknown = 0, catHit = false;
        toks.forEach(function (t) {
          if (fail) return;
          if (isYear(t)) return;
          if (CATKW[t]) { if (cats[p.cat]) { hits += 3; catHit = true; } return; }
          if (MAKES[t]) { if (ix.mk[t]) hits += 3; else fail = true; return; }
          if (ix.T[t]) { hits += ix.T[t]; return; }
          if (isCode(t)) {
            var d = t.replace(/\D/g, '');
            if (d.length >= 3 && ix.digits.indexOf(d) >= 0) { soft++; hits += 1; return; }
            if (ix.refs.some(function (r) { return t.length >= 4 && r.indexOf(t) >= 0; })) { soft++; hits += 2; return; }
            fail = true; return;
          }
          if (t.length >= 4) {
            var lim = t.length >= 8 ? 2 : 1, ok = false;
            Object.keys(ix.T).some(function (w) { if (w.length >= 4 && lev(t, w) <= lim) { ok = true; return true; } });
            if (ok) { hits += 1; return; }
          }
          if (t.length >= 3) unknown++;
        });
        if (Object.keys(cats).length && !cats[p.cat]) fail = true;
        if (!fail && hits > 0 && (hits >= unknown * 2 || catHit)) {
          var k2 = soft || unknown ? 'possible' : 'match';
          if (!kind || k2 === 'match') { kind = k2; score = Math.max(score, 100 + hits * 10 - unknown * 5); why = 'tokens'; }
        } else if (fail && !kind) {
          // related: same make and part type, shown only as "not verified for your vehicle"
          var mkOk = !qmake || ix.mk[qmake], catOk = !Object.keys(cats).length || cats[p.cat];
          if (qmake && mkOk && catOk) related.push(p);
        }
      }
      if (!toks.length && !qn) { kind = 'all'; score = 1; }
      if (kind) {
        var yr = null;
        if (year) yr = (p.years && p.years.length) ? (p.years.indexOf(year) >= 0 ? 'listed' : 'differs') : 'unknown';
        if (yr === 'differs' && kind === 'match') kind = 'possible';
        res.push({ p: p, kind: kind, score: score, year: yr, why: why });
      }
    });
    res.sort(function (a, b) { return b.score - a.score || a.p.name.localeCompare(b.p.name); });
    return { q: q, results: res, related: related, year: year, exact: res.some(function (r) { return r.kind === 'exact'; }) };
  }

  /* ---------- UI helpers ---------- */
  function toast(html, ms) {
    var t = $('#toast'); if (!t) return; t.innerHTML = html; t.classList.add('on');
    clearTimeout(t._h); t._h = setTimeout(function () { t.classList.remove('on'); }, ms || 3200);
  }
  var KIND = { exact: ['tag-t', 'Exact reference match'], match: ['tag-n', 'Matches your search'], possible: ['tag-a', 'Possible match, please verify'] };
  function badge(p) { return p.src !== 'public' ? '<span class="tag tag-r">DEMO / NOT VERIFIED</span>' : ''; }
  function cardHTML(p, kind) {
    var refs = (p.refs || []).slice(0, 2).map(function (r) { return '<span>' + esc(r.n) + '</span>'; }).join('');
    var meta = [((p.make || '') + ' ' + (p.model || '')).trim(), p.brand].filter(Boolean).join(' · ');
    var k = kind && KIND[kind] ? '<span class="tag ' + KIND[kind][0] + '" style="align-self:flex-start">' + KIND[kind][1] + '</span>' : '<span class="tag tag-n" style="align-self:flex-start">' + esc(catName(p.cat)) + '</span>';
    return '<article class="card"><div class="im">' + badge(p) + '<img src="' + esc(pimg(p)) + '" alt="' + esc(p.alt || p.name) + '" width="400" height="300" loading="lazy" onerror="this.onerror=null;this.src=\'' + ph(p) + '\'"></div><div class="bd">' + k +
      '<h3><a href="' + purl(p) + '">' + esc(p.name) + '</a></h3><div class="meta">' + esc(meta) + '</div>' + (refs ? '<div class="refs">' + refs + '</div>' : '') +
      '<div class="ft"><a class="btn btn-g btn-s" href="' + purl(p) + '">View details</a><button class="btn btn-o btn-s" data-add="' + esc(p.id) + '">Add to RFQ</button></div></div></article>';
  }

  /* ---------- enquiry list (RFQ basket) ---------- */
  function rfq() { return LS.get(K.rfq, []); }
  function setRfq(v) { LS.set(K.rfq, v); renderCount(true); }
  function addRfq(id, qty) {
    var l = rfq(), it = l.filter(function (x) { return x.id === id; })[0];
    if (it) it.qty = (+it.qty || 1) + (qty || 1); else l.push({ id: id, qty: qty || 1 });
    setRfq(l); var p = byId(id);
    track('add_to_rfq', { id: id, qty: qty || 1 });
    toast('Added to your enquiry list: <b>' + esc(p ? p.name : id) + '</b>. <a href="' + ROOT + 'rfq/">View list</a>');
  }
  function renderCount(bump) {
    var n = rfq().reduce(function (a, x) { return a + 1; }, 0);
    $$('[data-rfq-count]').forEach(function (b) { b.textContent = n; if (bump) { b.classList.remove('bump'); void b.offsetWidth; b.classList.add('bump'); } });
    $$('[data-rfq-count2]').forEach(function (b) { b.textContent = n ? '(' + n + ')' : ''; });
  }

  /* ---------- leads ---------- */
  function leads() { return LS.get(K.leads, []); }
  function saveLead(l) { var all = leads(); all.unshift(l); return LS.set(K.leads, all); }
  function nextId(type) {
    var pre = { EXPORT: 'EX', SUPPLIER: 'SU', LOCAL: 'LO' }[type] || 'GE';
    var n = leads().filter(function (l) { return l.type === type; }).length + 1;
    return 'MP-' + pre + '-' + String(n).padStart(4, '0');
  }

  /* ---------- page setup ---------- */
  function navSetup() {
    var b = $('.burger'), n = $('#nav');
    if (b && n) b.addEventListener('click', function () { var o = n.classList.toggle('open'); b.setAttribute('aria-expanded', o); });
    renderCount();
    document.addEventListener('click', function (ev) {
      var a = ev.target.closest && ev.target.closest('[data-add]');
      if (a) { ev.preventDefault(); var q = 1; if (a.hasAttribute('data-withqty')) { var qi = $('[data-qty]'); q = Math.max(1, +(qi && qi.value) || 1); } addRfq(a.getAttribute('data-add'), q); }
      var r = ev.target.closest && ev.target.closest('[data-reset-demo]');
      if (r) { Object.keys(K).forEach(function (k) { LS.del(K[k]); }); renderCount(); toast('Demo data cleared in this browser.'); }
    });
  }
  function reveal() {
    var els = $$('.rv');
    if (!('IntersectionObserver' in window) || navigator.webdriver) { els.forEach(function (e) { e.classList.add('vis'); }); return; }
    var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('vis'); io.unobserve(x.target); } }); }, { rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (e, i) { e.style.transitionDelay = Math.min(i % 6, 5) * 60 + 'ms'; io.observe(e); });
  }

  /* tabs on the finder */
  function tabs() {
    $$('.finder .tabs').forEach(function (tl) {
      var bs = $$('[role=tab]', tl);
      function sel(b) {
        bs.forEach(function (x) { var on = x === b; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; var p = document.getElementById(x.getAttribute('aria-controls')); if (p) p.hidden = !on; });
      }
      bs.forEach(function (b, i) {
        b.addEventListener('click', function () { sel(b); });
        b.addEventListener('keydown', function (e) { var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0; if (d) { var nb = bs[(i + d + bs.length) % bs.length]; sel(nb); nb.focus(); } });
      });
    });
    // vehicle selects
    var mk = $('#s-make'), md = $('#s-model');
    if (mk && md) mk.addEventListener('change', function () {
      var v = mk.value;
      if (!v || v === '__other') { md.innerHTML = '<option value="">' + (v ? 'Type the model in the box above' : 'Choose a make first') + '</option>'; md.disabled = true; return; }
      var ms = {}; published().forEach(function (p) { if (p.make === v && p.model) ms[p.model] = 1; });
      md.innerHTML = '<option value="">Any model</option>' + Object.keys(ms).sort().map(function (m) { return '<option>' + esc(m) + '</option>'; }).join('');
      md.disabled = false;
    });
  }

  function goSearch(form) {
    var q = (form.q && form.q.value || '').trim();
    var p = new URLSearchParams();
    if (form.getAttribute('data-finder') === 'vehicle') {
      var mk = form.make && form.make.value, md = form.model && form.model.value, ct = form.cat && form.cat.value, yr = form.year && form.year.value.trim();
      var parts = [q]; if (mk && mk !== '__other' && q.toUpperCase().indexOf(mk.toUpperCase()) < 0) parts.unshift(mk); if (md) parts.push(md);
      q = parts.filter(Boolean).join(' ').trim();
      if (ct) p.set('cat', ct); if (yr) p.set('year', yr);
    }
    if (q) p.set('q', q);
    var scope = form.getAttribute('data-scope');
    if (scope && form.closest('[data-finder]') && location.pathname.indexOf('/our-products/') >= 0 && $('[data-results]')) { renderCatalogue(q, { cat: scope }); history.replaceState(null, '', '?' + p.toString()); return; }
    if ($('[data-results]') && !scope && form.getAttribute('data-finder') === 'main') { renderCatalogue(q, { cat: p.get('cat'), year: p.get('year') }); history.replaceState(null, '', '?' + p.toString()); return; }
    location.href = ROOT + 'our-products.html' + (p.toString() ? '?' + p.toString() : '');
  }

  function liveSearch() {
    $$('input[data-live]').forEach(function (inp) {
      var box = inp.closest('.qbox'), live = box && $('.live', box), form = inp.form, t, act = -1;
      if (!live) return;
      function close() { live.classList.remove('on'); act = -1; }
      function draw() {
        var q = inp.value.trim(); if (q.length < 2) { close(); return; }
        var r = search(q, { cat: form && form.getAttribute('data-scope') });
        var list = r.results.slice(0, 6);
        live.innerHTML = list.length ? list.map(function (x) {
          return '<a role="option" href="' + purl(x.p) + '"><img src="' + esc(pimg(x.p)) + '" alt="" onerror="this.onerror=null;this.src=\'' + ph(x.p) + '\'"><span><span class="t">' + esc(x.p.name) + '</span><br><span class="s">' + (KIND[x.kind] ? KIND[x.kind][1] : '') + ((x.p.refs || [])[0] ? ' · ' + esc(x.p.refs[0].n) : '') + '</span></span></a>';
        }).join('') + '<a href="#" data-all><span class="t" style="padding-left:4px">See all results for “' + esc(q) + '”</span></a>'
          : '<div class="none">No verified match yet for “' + esc(q) + '”. Press Search for sourcing options.</div>';
        live.classList.add('on');
      }
      inp.addEventListener('input', function () { clearTimeout(t); t = setTimeout(draw, 110); });
      inp.addEventListener('focus', function () { if (inp.value.trim().length >= 2) draw(); });
      inp.addEventListener('keydown', function (e) {
        var as = $$('a', live); if (!live.classList.contains('on') || !as.length) return;
        if (e.key === 'ArrowDown' || e.key === 'ArrowUp') { e.preventDefault(); act = (act + (e.key === 'ArrowDown' ? 1 : -1) + as.length) % as.length; as.forEach(function (a, i) { a.classList.toggle('act', i === act); }); }
        else if (e.key === 'Enter' && act >= 0) { e.preventDefault(); as[act].click(); }
        else if (e.key === 'Escape') close();
      });
      live.addEventListener('click', function (e) { var a = e.target.closest('[data-all]'); if (a) { e.preventDefault(); close(); goSearch(form); } });
      document.addEventListener('click', function (e) { if (!box.contains(e.target)) close(); });
    });
    $$('form[data-finder]').forEach(function (f) {
      f.addEventListener('submit', function (e) { e.preventDefault(); $$('.live', f).forEach(function (l) { l.classList.remove('on'); }); goSearch(f); });
    });
    $$('[data-try]').forEach(function (b) {
      b.addEventListener('click', function () {
        var f = b.closest('form'), i = f && $('input[data-live]', f); if (!i) return; i.value = b.getAttribute('data-try');
        if (f.make) { f.make.value = ''; f.make.dispatchEvent(new Event('change')); } if (f.cat) f.cat.value = '';
        goSearch(f);
      });
    });
  }

  /* ---------- catalogue page ---------- */
  var CAT_STATE = { page: 1, per: 12, filt: { cat: {}, make: {}, brand: {} } };
  function renderCatalogue(q, opt) {
    var grid = $('[data-results]'); if (!grid) return;
    opt = opt || {};
    var scope = grid.getAttribute('data-cat') || opt.cat || '';
    var r = search(q || '', { cat: scope, year: opt.year });
    if (q) track('search_started', { q: q });
    var res = r.results;
    // filters (main catalogue only)
    var fl = $('#filters');
    if (fl) {
      var F = CAT_STATE.filt, groups = { cat: {}, make: {}, brand: {} };
      res.forEach(function (x) { groups.cat[x.p.cat] = (groups.cat[x.p.cat] || 0) + 1; if (x.p.make) groups.make[x.p.make] = (groups.make[x.p.make] || 0) + 1; if (x.p.brand) groups.brand[x.p.brand] = (groups.brand[x.p.brand] || 0) + 1; });
      ['cat', 'make', 'brand'].forEach(function (g) {
        var box = $('[data-fl="' + g + '"]', fl);
        box.innerHTML = Object.keys(groups[g]).sort().map(function (k) { return '<label><input type="checkbox" value="' + esc(k) + '"' + (F[g][k] ? ' checked' : '') + '> ' + esc(g === 'cat' ? catName(k) : k) + '<small>' + groups[g][k] + '</small></label>'; }).join('') || '<small class="note">None</small>';
        $$('input', box).forEach(function (c) { c.addEventListener('change', function () { if (c.checked) F[g][c.value] = 1; else delete F[g][c.value]; CAT_STATE.page = 1; renderCatalogue(q, opt); }); });
      });
      res = res.filter(function (x) { return (!Object.keys(F.cat).length || F.cat[x.p.cat]) && (!Object.keys(F.make).length || F.make[x.p.make]) && (!Object.keys(F.brand).length || F.brand[x.p.brand]); });
    }
    if (opt.cat && !scope) res = res.filter(function (x) { return x.p.cat === opt.cat; });
    var note = $('[data-note]'), cnt = $('[data-count]'), empty = $('[data-empty]');
    if (empty) empty.style.display = res.length ? 'none' : '';
    cnt.textContent = res.length + (res.length === 1 ? ' product' : ' products') + (q ? ' for “' + q + '”' : '');
    var nh = '';
    if (q && res.length) {
      track('search_results', { q: q, n: res.length, exact: r.exact });
      var kinds = {}; res.forEach(function (x) { kinds[x.kind] = 1; });
      if (kinds.exact) nh = '<div class="match-note mn-ok"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.5 2.5L16 9.5"/></svg><div><b>Exact reference match for “' + esc(q) + '”.</b> Our team still confirms fitment with your chassis number before quoting.</div></div>';
      else if (kinds.match) nh = '<div class="match-note mn-ok"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.5 2.5L16 9.5"/></svg><div><b>' + res.length + ' listing' + (res.length > 1 ? 's' : '') + ' match your vehicle and part.</b> Fitment is confirmed by our team before quoting.</div></div>';
      if (kinds.possible) nh += '<div class="match-note mn-warn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 3 2 20h20L12 3Z"/><path d="M12 10v4M12 17v.5"/></svg><div><b>Some results are possible matches only.</b> They share part of the number or chassis code but are not confirmed alternates. Please verify with our team.</div></div>';
      if (r.year && res.some(function (x) { return x.year === 'unknown'; })) nh += '<div class="match-note mn-warn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><path d="M12 7v6M12 16v.5"/></svg><div><b>Fitment requires confirmation for ' + r.year + '.</b> These listings do not state a model year. <a href="' + ROOT + 'rfq/#vin">Send your chassis number</a> and we check.</div></div>';
    }
    note.innerHTML = nh;
    var pages = Math.max(1, Math.ceil(res.length / CAT_STATE.per)); if (CAT_STATE.page > pages) CAT_STATE.page = 1;
    var slice = res.slice((CAT_STATE.page - 1) * CAT_STATE.per, CAT_STATE.page * CAT_STATE.per);
    if (!res.length && q) {
      track('no_match', { q: q });
      var rel = r.related.slice(0, 3);
      grid.innerHTML = '<div class="nores" style="grid-column:1/-1"><span class="tag tag-g">No verified match</span><h3 style="margin-top:12px">We don\'t list a part for “' + esc(q) + '” yet</h3><p>We won\'t guess a fitment. Send the request and our team checks whether we can source it, usually starting from the chassis number.</p>' +
        '<div class="pd-cta"><a class="btn btn-o" href="' + ROOT + 'rfq/?need=' + encodeURIComponent(q) + '" data-src>Request sourcing</a><a class="btn btn-g" href="' + ROOT + 'rfq/#vin">Send a chassis number</a></div>' +
        (rel.length ? '<p class="note" style="margin-top:18px"><b>Other listings for this make and part type.</b> Shown for reference only: they are <b>not</b> verified for your vehicle.</p><div class="pgrid">' + rel.map(function (p) { return cardHTML(p, null); }).join('') + '</div>' : '') + '</div>';
    } else if (!res.length) {
      grid.innerHTML = '';
    } else grid.innerHTML = slice.map(function (x) { return cardHTML(x.p, q ? x.kind : null); }).join('');
    var pg = $('[data-pager]');
    if (pg) {
      pg.innerHTML = pages > 1 ? Array.apply(null, Array(pages)).map(function (_, i) { return '<button type="button"' + (i + 1 === CAT_STATE.page ? ' aria-current="page"' : '') + ' data-pg="' + (i + 1) + '">' + (i + 1) + '</button>'; }).join('') : '';
      $$('[data-pg]', pg).forEach(function (b) { b.addEventListener('click', function () { CAT_STATE.page = +b.getAttribute('data-pg'); renderCatalogue(q, opt); grid.scrollIntoView({ behavior: 'smooth' }); }); });
    }
  }
  function catalogueInit() {
    var grid = $('[data-results]'); if (!grid) return;
    var u = new URLSearchParams(location.search), q = u.get('q') || '';
    $$('form[data-finder="main"] input[data-live]').forEach(function (i) { i.value = q; });
    renderCatalogue(q, { cat: u.get('cat'), year: u.get('year') });
    var ft = $('[data-ftoggle]'); if (ft) ft.addEventListener('click', function () { $('#filters').classList.toggle('open'); });
    var cl = $('[data-clear]'); if (cl) cl.addEventListener('click', function () { CAT_STATE.filt = { cat: {}, make: {}, brand: {} }; renderCatalogue(q, { year: u.get('year') }); });
  }

  /* ---------- product + dynamic item page ---------- */
  function productInit() {
    $$('[data-q]').forEach(function (b) { b.addEventListener('click', function () { var i = $('[data-qty]'); i.value = Math.max(1, (+i.value || 1) + +b.getAttribute('data-q')); }); });
    var pd = $('[data-product]'); if (pd) track('view_product', { id: pd.getAttribute('data-product') });
    var host = $('[data-item-page]'); if (!host) return;
    var id = new URLSearchParams(location.search).get('id'), p = byId(id);
    if (!p || p.status === 'archived') { host.innerHTML = '<div class="nores"><h3>Product not found</h3><p>It may have been archived in the staff dashboard.</p><a class="btn btn-o" href="' + ROOT + 'our-products.html">Search products</a></div>'; return; }
    track('view_product', { id: id });
    document.title = p.name + ' | Mega Power';
    var c = $('[data-crumb]'); if (c) c.textContent = p.name;
    var rows = [['Part type', catName(p.cat)], ['Car make', p.make], ['Model', p.model], ['Chassis / series', (p.codes || []).join(', ')], ['Years', p.yearFrom || p.yearTo ? (p.yearFrom || '?') + ' to ' + (p.yearTo || '?') : ''], ['Market', p.market], ['Steering', p.steering],
      ['Component brand', p.brand], ['Country of manufacture', p.country], ['Refrigerant gas', p.gas], ['Compressor oil', p.oil]].concat((p.specs || []).map(function (s) { return [s.k, s.v]; }));
    host.className = 'wrap pd';
    host.innerHTML = '<div class="pd-img">' + badge(p) + '<img src="' + esc(pimg(p)) + '" alt="' + esc(p.alt || p.name) + '" onerror="this.onerror=null;this.src=\'' + ph(p) + '\'"></div><div><span class="tag tag-n">' + esc(catName(p.cat)) + '</span> ' + (p.status === 'draft' ? '<span class="tag tag-a">Draft: staff preview</span>' : '') +
      '<h1 style="margin-top:10px">' + esc(p.name) + '</h1><p>' + esc(p.desc || '') + '</p>' +
      '<table class="spec">' + ((p.refs || []).map(function (r) { return '<tr><th>' + esc(r.t || 'Reference') + (r.v ? '' : ' <span class="tag tag-a">unverified</span>') + '</th><td class="mono">' + esc(r.n) + '</td></tr>'; }).join('') || '<tr><th>Reference</th><td>None given</td></tr>') + '</table>' +
      '<div class="fit"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg><div><b>Fitment is confirmed by our team.</b> ' + (p.src !== 'public' ? 'This is a DEMO record added in the staff dashboard, not real stock. ' : '') + 'Send your VIN or chassis number with the enquiry.</div></div>' +
      '<div class="pd-cta"><div class="qty"><button type="button" data-q="-1" aria-label="Less">−</button><input type="number" min="1" value="1" aria-label="Quantity" data-qty><button type="button" data-q="1" aria-label="More">+</button></div><button class="btn btn-o" data-add="' + esc(p.id) + '" data-withqty>Add to RFQ</button><a class="btn btn-n" href="' + ROOT + 'rfq/?add=' + esc(p.id) + '&type=EXPORT">Request export quote</a></div>' +
      '<h2 style="font-size:1.15rem;margin-top:24px">Specifications</h2><table class="spec">' + rows.filter(function (r) { return r[1]; }).map(function (r) { return '<tr><th>' + esc(r[0]) + '</th><td>' + esc(r[1]) + '</td></tr>'; }).join('') + '</table></div>';
    $$('[data-q]', host).forEach(function (b) { b.addEventListener('click', function () { var i = $('[data-qty]', host); i.value = Math.max(1, (+i.value || 1) + +b.getAttribute('data-q')); }); });
  }

  /* ---------- forms ---------- */
  function validate(f) {
    var ok = true, first = null;
    $$('input,select,textarea', f).forEach(function (el) {
      if (el.type === 'file') return;
      var bad = false, v = (el.value || '').trim();
      if (el.type === 'checkbox') { if (el.required && !el.checked) bad = true; var er = el.closest('div') && el.closest('div').querySelector('.err'); if (er) er.classList.toggle('on', bad); }
      else {
        if (el.required && !v) bad = true;
        if (!bad && v && el.type === 'email' && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) bad = true;
        if (!bad && v && el.minLength > 0 && v.length < el.minLength) bad = true;
        el.classList.toggle('bad', bad); el.setAttribute('aria-invalid', bad ? 'true' : 'false');
      }
      if (bad) { ok = false; if (!first) first = el; }
    });
    if (first) first.focus();
    return ok;
  }
  function formData(f) {
    var o = {}, files = [];
    $$('input,select,textarea', f).forEach(function (el) {
      if (!el.name) return;
      if (el.type === 'file') { Array.prototype.forEach.call(el.files || [], function (x) { files.push(x.name + ' (' + Math.round(x.size / 1024) + ' KB)'); }); return; }
      if (el.type === 'checkbox') { if (el.name === 'consent') { o.consent = el.checked; return; } if (el.checked) o[el.name] = (o[el.name] ? o[el.name] + ', ' : '') + el.value; return; }
      if (el.value.trim()) o[el.name] = el.value.trim();
    });
    return { fields: o, files: files };
  }
  function itemsFor(f) {
    if (f.hasAttribute('data-sub')) return [];
    var ctx = f.getAttribute('data-ctx-items');
    var list = ctx ? JSON.parse(ctx) : ($('[data-items]', f) ? rfq() : []);
    return list.map(function (x) { var p = byId(x.id); return p ? { id: p.id, name: p.name, ref: (p.refs || [])[0] ? p.refs[0].n : '', qty: x.qty, url: purl(p).replace(ROOT, '/'), src: p.src } : null; }).filter(Boolean);
  }
  function modal(html) {
    var m = $('#mp-mod'); if (!m) { m = document.createElement('div'); m.id = 'mp-mod'; m.className = 'mod'; m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true'); document.body.appendChild(m); m.addEventListener('click', function (e) { if (e.target === m || e.target.closest('[data-close]')) m.classList.remove('on'); }); }
    m.innerHTML = '<div class="box">' + html + '</div>'; m.classList.add('on'); var b = $('button,a', m); if (b) b.focus();
  }
  function formsInit() {
    $$('form[data-lead]').forEach(function (f) {
      $$('input,select,textarea', f).forEach(function (el) { el.addEventListener('input', function () { if (el.classList.contains('bad')) { el.classList.remove('bad'); } }); });
      $$('[data-drop]', f).forEach(function (d) {
        var inp = $('input[type=file]', d), lab = d.childNodes[d.childNodes.length - 1];
        function show() { var n = Array.prototype.map.call(inp.files || [], function (x) { return x.name; }).join(', '); if (n) lab.textContent = 'Attached: ' + n; }
        inp.addEventListener('change', show);
        ['dragenter', 'dragover'].forEach(function (t) { d.addEventListener(t, function (e) { e.preventDefault(); d.classList.add('over'); }); });
        ['dragleave', 'drop'].forEach(function (t) { d.addEventListener(t, function (e) { e.preventDefault(); d.classList.remove('over'); }); });
        d.addEventListener('drop', function (e) { if (e.dataTransfer && e.dataTransfer.files.length) { try { inp.files = e.dataTransfer.files; } catch (x) {} show(); } });
      });
      f.addEventListener('submit', function (e) {
        e.preventDefault();
        if (!validate(f)) { toast('Please check the highlighted fields.'); return; }
        var type = f.getAttribute('data-lead'), fd = formData(f), items = itemsFor(f), u = new URLSearchParams(location.search);
        var lead = { id: nextId(type), type: type, sub: f.getAttribute('data-sub') || '', created: new Date().toISOString(), status: 'New', fields: fd.fields, files: fd.files, items: items,
          source: { page: location.pathname, url: location.href, referrer: document.referrer || '', product: ($('[data-product]') || {}).getAttribute ? $('[data-product]').getAttribute('data-product') : (u.get('p') || u.get('add') || ''),
            utm: ['utm_source', 'utm_medium', 'utm_campaign'].map(function (k) { return u.get(k) ? k + '=' + u.get(k) : ''; }).filter(Boolean).join('&'), need: u.get('need') || '' },
          tag: type === 'SUPPLIER' ? 'IMPORT_SUPPLIER' : type === 'LOCAL' ? 'SG_WORKSHOP' : (f.getAttribute('data-sub') || 'EXPORT_RFQ'), notes: [] };
        if (!saveLead(lead)) { toast('Could not save in this browser (private mode?).'); return; }
        track({ EXPORT: 'submit_export_rfq', SUPPLIER: 'submit_supplier_lead', LOCAL: 'submit_local_enquiry' }[type], { id: lead.id, items: items.length });
        if (items.length && !f.getAttribute('data-ctx-items')) { setRfq([]); renderBasket(); }
        f.reset(); $$('[data-drop]', f).forEach(function (d) { d.lastChild.textContent = 'File removed after sending'; });
        var label = { EXPORT: 'Export enquiries', SUPPLIER: 'Supplier enquiries', LOCAL: 'Local workshop enquiries' }[type];
        modal('<span class="tag tag-t">Enquiry ' + esc(lead.id) + ' recorded</span><h3 style="margin-top:12px">Thank you. Our team will reply.</h3>' +
          (items.length ? '<p>' + items.length + ' part' + (items.length > 1 ? 's' : '') + ' included: ' + items.map(function (i) { return esc(i.name) + ' × ' + esc(i.qty); }).join(', ') + '.</p>' : '') +
          '<div class="demo-flag"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg><span><b>Demo only:</b> saved to the staff inbox under <b>' + label + '</b> in this browser. No email or WhatsApp was sent. On the live site this goes to the sales inbox once Mega Power confirms the addresses.</span></div>' +
          '<div class="pd-cta" style="margin-bottom:0"><a class="btn btn-n" href="' + ROOT + 'staff/#lead/' + encodeURIComponent(lead.id) + '">See it in the staff inbox</a><button class="btn btn-g" data-close>Close</button></div>');
      });
    });
  }

  /* ---------- RFQ page ---------- */
  function renderBasket() {
    var l = rfq();
    $$('form[data-lead]:not([data-ctx-items]) [data-items]').forEach(function (d) { d.innerHTML = l.length ? '<p class="note" style="margin-top:-4px">' + l.length + ' part' + (l.length > 1 ? 's' : '') + ' from your <a href="' + ROOT + 'rfq/">enquiry list</a> will be included.</p>' : ''; });
    var b = $('[data-basket]'); if (!b) return;
    if (!l.length) { b.innerHTML = '<div class="nores"><b style="color:var(--navy)">Your enquiry list is empty.</b><p style="margin:6px 0 12px;color:var(--muted)">Add parts from the catalogue, or describe what you need in the form below.</p><a class="btn btn-g btn-s" href="' + ROOT + 'our-products.html">Search products</a></div>'; }
    else b.innerHTML = l.map(function (x) {
      var p = byId(x.id); if (!p) return '';
      return '<div class="bi"><img src="' + esc(pimg(p)) + '" alt="" onerror="this.onerror=null;this.src=\'' + ph(p) + '\'"><div><div class="t">' + esc(p.name) + '</div><div class="s">' + esc(((p.refs || [])[0] || {}).n || catName(p.cat)) + ' ' + badge(p) + '</div></div><div class="c"><label class="sr" for="q-' + esc(p.id) + '">Quantity</label><input class="in" id="q-' + esc(p.id) + '" type="number" min="1" value="' + esc(x.qty) + '" data-bq="' + esc(p.id) + '"><button class="x" data-brm="' + esc(p.id) + '" aria-label="Remove">×</button></div></div>';
    }).join('');
    $$('[data-bq]', b).forEach(function (i) { i.addEventListener('change', function () { var l2 = rfq(); l2.forEach(function (x) { if (x.id === i.getAttribute('data-bq')) x.qty = Math.max(1, +i.value || 1); }); LS.set(K.rfq, l2); }); });
    $$('[data-brm]', b).forEach(function (btn) { btn.addEventListener('click', function () { setRfq(rfq().filter(function (x) { return x.id !== btn.getAttribute('data-brm'); })); renderBasket(); }); });
  }
  function rfqInit() {
    if (!$('[data-basket]')) { renderBasket(); return; }
    var u = new URLSearchParams(location.search);
    if (u.get('add') && byId(u.get('add'))) { var l = rfq(); if (!l.some(function (x) { return x.id === u.get('add'); })) { l.push({ id: u.get('add'), qty: 1 }); setRfq(l); } }
    renderBasket();
    var tabs = $$('[data-rt]');
    function sel(t) { tabs.forEach(function (b) { b.setAttribute('aria-selected', b.getAttribute('data-rt') === t); }); $$('[data-rt-panel]').forEach(function (p) { p.hidden = p.getAttribute('data-rt-panel') !== t; }); }
    tabs.forEach(function (b) { b.addEventListener('click', function () { sel(b.getAttribute('data-rt')); }); });
    if (u.get('type') === 'LOCAL') sel('LOCAL');
    if (u.get('need')) { $$('textarea[name=message]').forEach(function (t) { t.value = 'Request sourcing: ' + u.get('need') + '. Not found in the catalogue.'; }); $$('input[name=vehicle]').forEach(function (i) { if (!i.value) i.value = u.get('need'); }); }
  }

  /* ---------- workshop page: product context + WhatsApp preview ---------- */
  function localInit() {
    var prev = $('[data-wa-preview]'); if (!prev) return;
    var u = new URLSearchParams(location.search), p = u.get('p') && byId(u.get('p')), f = $('#local-form');
    function txt() {
      var v = f && f.vehicle.value.trim(), part = f && f.part.value.trim();
      return 'Hello Mega Power, I am enquiring about ' + (p ? p.name + ((p.refs || [])[0] ? ' (ref ' + p.refs[0].n + ')' : '') : (part || 'a part')) + ' found on ' + (p ? D.base + '/' + (p.url || 'our-products/item.html?id=' + p.id) : D.base + '/singapore-workshops/') + '.\nMy vehicle details are: ' + (v || '…');
    }
    if (p && f) {
      f.setAttribute('data-ctx-items', JSON.stringify([{ id: p.id, qty: 1 }]));
      $('[data-items]', f).innerHTML = '<div class="bi" style="margin-bottom:14px"><img src="' + esc(pimg(p)) + '" alt="" onerror="this.onerror=null;this.src=\'' + ph(p) + '\'"><div><div class="t">' + esc(p.name) + '</div><div class="s">' + esc(((p.refs || [])[0] || {}).n || '') + '</div></div><span></span></div>';
      f.part.value = catName(p.cat).replace(/s$/, '') + (p.refs && p.refs[0] ? ' ' + p.refs[0].n : '');
      if (p.make) f.vehicle.placeholder = 'e.g. ' + p.make + ' ' + (p.model || '') + ' + year';
    }
    function upd() { prev.textContent = txt(); }
    if (f) ['input', 'change'].forEach(function (t) { f.addEventListener(t, upd); });
    upd();
    var cp = $('[data-copy-wa]'); if (cp) cp.addEventListener('click', function () {
      track('click_whatsapp', { configured: false });
      try { navigator.clipboard.writeText(prev.textContent); toast('Message copied. WhatsApp number still to be confirmed by Mega Power.'); } catch (e) { toast('Copy not available here.'); }
    });
  }

  window.MP = { D: D, LS: LS, K: K, ROOT: ROOT, esc: esc, norm: norm, search: search, allProducts: allProducts, saveProducts: saveProducts, byId: byId, purl: purl, pimg: pimg, ph: ph, catName: catName, CATS: CATS, leads: leads, track: track, toast: toast, cardHTML: cardHTML };
  function init() { if (document.body.classList.contains('st')) return; navSetup(); tabs(); liveSearch(); catalogueInit(); productInit(); formsInit(); rfqInit(); localInit(); reveal(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
