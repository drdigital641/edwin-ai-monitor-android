/* EV Body Parts - public site script: owner-language search, live Base44 catalogue, enquiry -> WhatsApp, motion.
   Data = window.EV_DATA (data.js: snapshot of the Base44 app at build time) refreshed LIVE from the app's public REST read
   (EvBrand / EvCar / EvProduct, status published; EvPhoto chunks for b44photo:<group>). If the live read fails the snapshot stays. Works in node for tests. */
(function (root) {
  'use strict';
  var D = root.EV_DATA;
  var ROOT = root.EV_ROOT || '';
  var K = { live: 'ev_live_v1' };
  var LIVE_TTL = 45000;

  /* ---------- storage (every access guarded) ---------- */
  function lsGet(k, d) { try { var v = root.localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch (e) { return d; } }
  function lsSet(k, v) { try { root.localStorage.setItem(k, JSON.stringify(v)); return true; } catch (e) { return false; } }
  function ssGet(k) { try { var v = root.sessionStorage.getItem(k); return v ? JSON.parse(v) : null; } catch (e) { return null; } }
  function ssSet(k, v) { try { root.sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { } }

  /* ---------- text helpers ---------- */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function norm(s) { return String(s || '').toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, ' ').trim().replace(/\s+/g, ' '); }
  function stem(t) { return (t.length > 3 && t.slice(-1) === 's' && t.slice(-2) !== 'ss' && t !== 'lens') ? t.slice(0, -1) : t; }
  function toks(s) { var n = norm(s); return n ? n.split(' ').map(stem) : []; }
  function slug(s) { return norm(s).replace(/ /g, '-'); }
  var STOP = {}; 'for the a an my our car cars part parts spare new need needs looking want buy sell left right lh rh set pcs pc of and to with model please do you have got is any'.split(' ').forEach(function (w) { STOP[stem(w)] = 1; });
  function money(v) { v = +v; return 'S$' + (v % 1 ? v.toFixed(2) : v.toLocaleString('en-SG')); }

  /* ---------- state: snapshot first, live data replaces it ---------- */
  var S = { brands: [], cars: [], products: [], live: false };
  var BRM = {}, CARM = {}, PARTM = {}, STATIC_URL = {}, ENTRIES = [], ALL = [], IDX = null;
  D.parts.forEach(function (p) { PARTM[p.slug] = p; });
  D.products.forEach(function (p) { if (p.url) STATIC_URL[p.key] = p.url; });
  function carSlug(c) { var pre = c.b + '-'; return c.slug || (c.key.indexOf(pre) === 0 && c.key.length > pre.length ? c.key.slice(pre.length) : c.key); }
  function setData(brands, cars, products) {
    S.brands = brands.slice().sort(function (a, b) { return (a.order || 999) - (b.order || 999) || String(a.name).localeCompare(b.name); });
    S.cars = cars; S.products = products;
    BRM = {}; CARM = {};
    S.brands.forEach(function (b) { BRM[b.key] = b; });
    S.cars = S.cars.filter(function (c) { return BRM[c.b]; });
    S.cars.forEach(function (c) { c.slug = carSlug(c); CARM[c.key] = c; });
    ENTRIES = [];
    products.forEach(function (p) { var e = mkEntry(p); if (e) ENTRIES.push(e); });
    ENTRIES.sort(function (a, b) { return String(b.created).localeCompare(String(a.created)); });
    /* the catalogue is every part we can source for every model (Edwin, 31 Oct 2026: not a warehouse, a sourcing catalogue);
       a model+part with its own listing shows that listing instead */
    var have = {}; ENTRIES.forEach(function (e) { have[e.modelSlug + '|' + e.part] = 1; });
    ALL = ENTRIES.slice();
    S.brands.forEach(function (b) { S.cars.forEach(function (car) { if (car.b !== b.key) return; D.parts.forEach(function (pt) {
      if (pt.slug === 'other' || have[car.key + '|' + pt.slug]) return;
      ALL.push({ ask: true, src: true, id: 'src-' + car.key + '-' + pt.slug, key: '', brand: b.key, brandName: b.name, model: car.name, modelSlug: car.key, carSlug: car.slug,
        part: pt.slug, partName: pt.name, title: b.name + ' ' + car.name + ' ' + pt.name, side: '', price: null, stock: '', photos: [], url: '' });
    }); }); });
    IDX = null;
  }
  var SIDE = { L: 'Left', R: 'Right', pair: 'Pair' };
  var SPECIAL = {}; (D.special || []).forEach(function (k) { SPECIAL[k] = 1; });
  /* part type for a product with a missing/unknown p: longest owner-language match in its name or title */
  var SYN = []; D.parts.forEach(function (p) { if (p.slug !== 'other') p.syn.concat([p.name]).forEach(function (w) { SYN.push([' ' + String(w).toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim() + ' ', p.slug]); }); });
  SYN.sort(function (a, b) { return b[0].length - a[0].length; });
  function classify(t) { t = ' ' + String(t || '').toLowerCase().replace(/[^a-z0-9]+/g, ' ') + ' '; for (var i = 0; i < SYN.length; i++) if (t.indexOf(SYN[i][0]) >= 0) return SYN[i][1]; return ''; }
  function mkEntry(p) {
    var car = CARM[p.m]; if (!car) return null;
    var b = BRM[car.b], part = PARTM[p.p] && p.p !== 'other' ? PARTM[p.p] : (PARTM[classify((p.pn || '') + ' ' + (p.title || ''))] || null);
    var named = part && !(PARTM[p.p] && p.p !== 'other');
    var partName = part && !named ? part.name : (p.pn || (part ? part.name : 'Other part'));
    var title = p.title || (b.name + ' ' + car.name + ' ' + partName + (SIDE[p.side] ? ' (' + SIDE[p.side] + ')' : ''));
    var price = (typeof p.price === 'number' && p.price > 0) ? p.price : null;
    return { id: p.key, key: p.key, brand: car.b, brandName: b.name, model: car.name, modelSlug: car.key, carSlug: car.slug, part: part ? part.slug : 'other', partName: partName,
      title: title, side: p.side || '', price: price, stock: p.stock || '', photos: p.photos || [], desc: p.desc || '', note: p.note || '', oem: p.oem || '', grade: p.grade || '',
      created: (p.created || p.created_date || '').slice(0, 10), url: STATIC_URL[p.key] || p.url || '' };
  }
  setData(D.brands, D.cars, D.products);

  /* ---------- live read of the Base44 app (public read, no login) ---------- */
  function timeout(ms) { return new Promise(function (_, rej) { setTimeout(function () { rej(new Error('timeout')); }, ms); }); }
  function apiGet(path) {
    var bases = D.api || [], i = 0;
    function next(err) {
      if (i >= bases.length) return Promise.reject(err || new Error('no api'));
      var url = bases[i++] + path;
      return Promise.race([root.fetch(url, { headers: { 'X-App-Id': D.appId, 'Accept': 'application/json' }, credentials: 'omit' }), timeout(7000)])
        .then(function (r) { if (!r.ok) throw new Error('http ' + r.status); return r.json(); })
        .then(function (j) { var a = Array.isArray(j) ? j : (j && (j.items || j.entities || j.data || j.results)); if (!Array.isArray(a)) throw new Error('shape'); return a; })
        .catch(next);
    }
    return next();
  }
  function fetchAll(entity, query, sort) {
    var out = [];
    function page(skip) {
      var p = '/entities/' + entity + '?q=' + encodeURIComponent(JSON.stringify(query || {})) + '&limit=500&skip=' + skip + (sort ? '&sort=' + encodeURIComponent(sort) : '');
      return apiGet(p).then(function (a) { out = out.concat(a); return a.length >= 500 && skip < 9500 ? page(skip + 500) : out; });
    }
    return page(0);
  }
  function pubOnly(a) { return a.filter(function (r) { return !r.status || r.status === 'published'; }); }
  var renderers = [];
  function refresh() { renderers.forEach(function (f) { try { f(); } catch (e) { if (root.console) console.warn(e); } }); }
  function applyLive(L) {
    var brands = L.brands && L.brands.length ? L.brands : S.brands;
    var cars = L.cars && L.cars.length ? L.cars : S.cars;
    setData(brands, cars, L.products || []);
    S.live = true;
    refresh();
  }
  function liveLoad() {
    if (!root.fetch || !D.api || !D.api.length) return Promise.resolve(false);
    var c = ssGet(K.live);
    if (c && c.fail && Date.now() - c.t < 60000) return Promise.resolve(false);
    if (c && c.d && c.t && Date.now() - c.t < LIVE_TTL) { applyLive(c.d); return Promise.resolve(true); }
    return Promise.all([
      fetchAll('EvBrand', { status: 'published' }, 'order').catch(function () { return null; }),
      fetchAll('EvCar', { status: 'published' }).catch(function () { return null; }),
      fetchAll('EvProduct', { status: 'published' }, '-created_date')
    ]).then(function (r) {
      var d = { brands: r[0] ? pubOnly(r[0]).map(function (b) { return { key: b.key, name: b.name, alias: b.alias || [], order: b.order || 0 }; }) : null,
        cars: r[1] ? pubOnly(r[1]).map(function (x) { return { key: x.key, b: x.b, name: x.name, alias: x.alias || [], years: x.years || '', photo: x.photo || '' }; }) : null,
        products: pubOnly(r[2]).map(function (p) { return { key: p.key, m: p.m, p: p.p, pn: p.pn, title: p.title, side: p.side, oem: p.oem, grade: p.grade, price: p.price, stock: p.stock, photos: p.photos || [], desc: p.desc, note: p.note, created: p.created_date } }) };
      ssSet(K.live, { t: Date.now(), d: d });
      applyLive(d); return true;
    }).catch(function () { ssSet(K.live, { t: Date.now(), fail: 1 }); return false; });   /* snapshot stays on screen */
  }
  /* photos stored as b44photo:<group>: EvPhoto chunks (data-URL pieces) joined by i */
  var PHOTO_MEM = {};
  function loadPhoto(g) {
    if (D.photoFiles && D.photoFiles[g]) return Promise.resolve(ROOT + D.photoFiles[g]);
    if (PHOTO_MEM[g]) return PHOTO_MEM[g];
    return (PHOTO_MEM[g] = fetchAll('EvPhoto', { group: g }, 'i').then(function (rows) {
      rows.sort(function (a, b) { return (a.i || 0) - (b.i || 0); });
      var s = rows.map(function (r) { return r.data || ''; }).join('');
      if (s.indexOf('data:image') !== 0) throw new Error('bad photo');
      return s;
    }));
  }
  function photoSrc(ref) {
    if (!ref) return { url: '' };
    if (ref.indexOf('b44photo:') === 0) { var g = ref.slice(9); return D.photoFiles && D.photoFiles[g] ? { url: ROOT + D.photoFiles[g] } : { g: g }; }
    return { url: ref };
  }
  function hydrate(el) {
    if (typeof document === 'undefined') return;
    Array.prototype.forEach.call((el || document).querySelectorAll('img[data-b44]'), function (img) {
      var g = img.getAttribute('data-b44'); img.removeAttribute('data-b44');
      loadPhoto(g).then(function (u) { img.onload = function () { img.classList.remove('ph0'); }; img.src = u; }).catch(function () { img.remove(); });
    });
  }

  /* ---------- index (rebuilt when data changes) ---------- */
  function isNb(a) { var n = norm(a); return /^[0-9a-z]{1,2}$/.test(n) || /^\d+$/.test(n); }
  function build() {
    var I = { parts: [], brands: [], models: [], vocab: {} };
    function vocab(seq) { seq.forEach(function (t) { if (t.length >= 4 && !/^\d+$/.test(t)) I.vocab[t] = 1; }); }
    D.parts.forEach(function (p) {
      p.syn.concat([p.name]).forEach(function (s) { var q = toks(s); if (q.length) { var m = {}; m[p.slug] = 1; I.parts.push({ seq: q, map: m, specific: 1 }); vocab(q); } });
    });
    D.generic.forEach(function (g) { var q = toks(g.w); I.parts.push({ seq: q, map: g.map, specific: 0 }); vocab(q); });
    I.parts.sort(function (a, b) { return b.seq.length - a.seq.length || b.specific - a.specific; });
    S.brands.forEach(function (b) {
      (b.alias || []).concat([b.name]).forEach(function (a) { var q = toks(a); if (q.length) { I.brands.push({ seq: q, brand: b.key }); vocab(q); } });
    });
    S.cars.forEach(function (m) {
      var b = BRM[m.b], seen = {};
      function add(a, nb) { var q = toks(a); var key = q.join(' ') + '|' + nb; if (!q.length || seen[key]) return; seen[key] = 1; I.models.push({ seq: q, brand: m.b, model: m.key, nb: nb }); vocab(q); }
      add(m.name, isNb(m.name) ? 1 : 0);
      (m.alias || []).forEach(function (a) { add(a, isNb(a) ? 1 : 0); });
      add(b.name + ' ' + m.name, 0); add(b.name + m.name, 0);
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
  function fix(t) {
    return t.map(function (w) {
      if (w.length < 5 || IDX.vocab[w] || /\d/.test(w)) return w;
      var best = null, bd = w.length >= 8 ? 2 : 1;
      for (var v in IDX.vocab) { var d = lev(w, v, bd); if (d <= bd && (best === null || d < bd)) { best = v; bd = d; if (d === 0) break; } }
      return best || w;
    });
  }
  function parse(q) {
    if (!IDX) IDX = build();
    var t = fix(toks(q)), used = t.map(function () { return false; });
    var R = { tokens: t, brand: null, model: null, parts: {}, hasPart: false, left: [] };
    var i, k, hit;
    IDX.parts.forEach(function (p) {
      var at = find(t, used, p.seq);
      if (at >= 0) {
        for (k = 0; k < p.seq.length; k++) used[at + k] = true;
        for (var s in p.map) R.parts[s] = Math.max(R.parts[s] || 0, p.map[s]);
        R.hasPart = true;
      }
    });
    var brandHit = null, brandAt = null;
    for (i = 0; i < IDX.brands.length; i++) { hit = find(t, used, IDX.brands[i].seq); if (hit >= 0) { brandHit = IDX.brands[i].brand; brandAt = [hit, IDX.brands[i].seq.length]; break; } }
    for (i = 0; i < IDX.models.length; i++) {
      var m = IDX.models[i];
      if (m.nb && !(brandHit === m.brand)) continue;
      hit = find(t, used, m.seq);
      if (hit >= 0) {
        for (k = 0; k < m.seq.length; k++) used[hit + k] = true; R.model = m.model; R.brand = m.brand;
        /* other generations of the same car (e.g. "model y" -> also Model Y Juniper) when the query did not name one */
        R.sibs = [];
        IDX.models.forEach(function (o) { if (o.brand === m.brand && o.model !== m.model && R.sibs.indexOf(o.model) < 0 && o.seq.length > m.seq.length && o.seq.slice(0, m.seq.length).join(' ') === m.seq.join(' ')) R.sibs.push(o.model); });
        break;
      }
    }
    if (!R.model && brandHit) { R.brand = brandHit; }
    if (brandAt && R.brand === brandHit) { for (k = 0; k < brandAt[1]; k++) used[brandAt[0] + k] = true; }
    t.forEach(function (w, j) { if (!used[j] && !STOP[w] && w !== 'model') R.left.push(w); });
    return R;
  }

  /* ---------- search ---------- */
  function words(e) { var o = e.oem || ''; return toks([e.title, e.side, e.note, e.partName, e.brandName, e.model, o, o.replace(/[^0-9a-z]/gi, '')].join(' ')); }
  function askEntries(P, out) {
    /* "Ask us" cards: no listing exists for what was understood, so offer an enquiry (never a fake listing) */
    var asks = [];
    if (!P.brand) return asks;
    var b = BRM[P.brand];
    var models = P.model ? [P.model].concat(P.sibs || []) : [null];
    models.forEach(function (mk0) {
      var car = mk0 ? CARM[mk0] : null, veh = b.name + (car ? ' ' + car.name : '');
      if (mk0 && !car) return;
      function mk(partSlug, partName, title) {
        return { ask: true, id: 'ask-' + (mk0 || P.brand) + '-' + partSlug, key: '', brand: P.brand, brandName: b.name, model: car ? car.name : '', modelSlug: car ? car.key : '', carSlug: car ? car.slug : '',
          part: partSlug, partName: partName, title: title, side: '', price: null, stock: '', photos: [], url: '' };
      }
      if (P.hasPart) {
        var max = 0, s; for (s in P.parts) max = Math.max(max, P.parts[s]);
        Object.keys(P.parts).filter(function (p) { return P.parts[p] >= Math.max(.5, max); }).forEach(function (p) {
          var has = out.some(function (r) { return r.e.part === p && (!mk0 || r.e.modelSlug === mk0) && r.e.brand === P.brand; });
          if (!has && PARTM[p]) asks.push(mk(p, PARTM[p].name, veh + ' ' + PARTM[p].name));
        });
      } else if (car) asks.push(mk('other', 'Parts', veh + ' parts'));
      else if (!out.length) asks.push(mk('other', 'Parts', veh + ' parts'));
    });
    return asks;
  }
  function search(q, opts) {
    opts = opts || {};
    var pool = opts.pool || ENTRIES;
    var P = parse(q), out = [];
    var anyKey = !!(P.brand || P.model || P.hasPart);
    if (!norm(q)) return { q: q, P: P, results: pool.map(function (e, n) { return { e: e, score: 0, n: n }; }), weak: false, empty: true, onlyAsk: false };
    pool.forEach(function (e, n) {
      var s = 0;
      if (P.brand && e.brand !== P.brand) return;
      if (P.brand) s += 20;
      if (P.model) { if (e.modelSlug === P.model && e.brand === P.brand) s += 50; else if (e.src && (P.sibs || []).indexOf(e.modelSlug) >= 0) s += 45; }
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
    var products = out.length;
    /* a named model (e.g. a newer generation) with no listing of its own: its Ask-us cards go first, other models' listings follow */
    var askFirst = P.model && !out.some(function (r) { return r.e.modelSlug === P.model; });
    if (!opts.pool) { var asks = askEntries(P, out).map(function (a) { return { e: a, score: -1, n: 9999 }; }); out = askFirst ? asks.concat(out) : out.concat(asks); }
    var unk = P.left.filter(function (l) { return l.length >= 4 && !out.some(function (r) { return words(r.e).indexOf(l) >= 0; }); });
    var weak = !out.length || !anyKey || unk.length > 0;
    return { q: q, P: P, results: out, weak: weak, empty: false, onlyAsk: !products && out.length > 0 };
  }
  function brandName(k) { return BRM[k] ? BRM[k].name : ''; }
  function modelName(k) { return CARM[k] ? CARM[k].name : ''; }
  function partName(s) { return PARTM[s] ? PARTM[s].name : ''; }

  /* ---------- links ---------- */
  function waLink(text) { return 'https://wa.me/' + D.wa + '?text=' + encodeURIComponent('Hi ' + D.brand + ', I am looking for: ' + text + '. (from website)'); }
  function enqHref(e, suf) {
    /* prefilled WhatsApp quote request; the VIN is never put in the link (buyer adds it in the chat if needed) */
    var veh = ((e.brandName || '') + ' ' + (e.model || '')).trim(), t = (e.ask ? (veh + ' ' + e.partName) : (e.title || e.partName)) + (suf || '');
    if (D.wa) {
      var L = ['Hi ' + D.brand + ', please check fitment and quote:', 'Part: ' + t];
      if (e.oem) L.push('OE no.: ' + e.oem);
      L.push('Side: ' + (SIDE[e.side] || 'left / right / pair?'), 'Build month/year: ', 'Market: Singapore', 'I can send photos here. (from website)');
      return 'https://wa.me/' + D.wa + '?text=' + encodeURIComponent(L.join('\n'));
    }
    return ROOT + 'contact/';
  }
  function enqFree(text) { return D.wa ? waLink(text || 'a part') : ROOT + 'contact/'; }

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
  function artHtml(e) {
    var u = D.art && D.art[e.part];
    return u ? '<img class="art" src="' + esc(u) + '" alt="Illustrative image" title="' + esc(D.illus || '') + '" width="88" height="88" loading="lazy" decoding="async" onerror="this.remove()"><span class="illus-t">Illustrative</span>' : '';
  }
  function mediaHtml(e) {
    var ph = photoSrc(e.photos && e.photos[0]);
    if (ph.url) return '<img src="' + esc(ph.url) + '" alt="' + esc(e.title) + '" width="88" height="88" loading="lazy" decoding="async" onerror="this.remove()">';
    if (ph.g) return '<img class="ph0" data-b44="' + esc(ph.g) + '" alt="' + esc(e.title) + '" width="88" height="88" decoding="async">';
    return artHtml(e);
  }
  function addBtn(e, cls, label) {
    /* enquiry-first: no cart, the button opens a prefilled WhatsApp quote request */
    return '<a class="' + cls + '" href="' + esc(enqHref(e, SPECIAL[e.part] ? ' (specialist check)' : '')) + '" data-wa="quote">' + (label || 'Get a quote') + '</a>';
    var key = e.ask ? 'ask:' + e.modelSlug + ':' + e.part : e.key;
    return '<button type="button" class="' + cls + '" data-add data-key="' + esc(key) + '" data-title="' + esc(e.title) + '" data-car="' + esc(((e.brandName || '') + ' ' + (e.model || '')).trim()) + '" data-part="' + esc(e.partName) + '" data-side="' + esc(e.side || '') + '"' + (e.price ? ' data-price="' + e.price + '"' : '') + (e.ask ? ' data-ask="1"' : '') + '>' + (label || 'Add to cart') + '</button>';
  }
  function card(e, P) {
    var veh = ((e.brandName || '') + ' ' + (e.model || '')).trim() || e.brandName;
    if (e.ask) {
      return '<article class="rc askc"><div class="rc-ic">' + iconSvg(e.part) + artHtml(e) + '</div><div class="rc-b"><span class="chip">' + esc(veh) + '</span><h3>' + hlTitle(e, P) + '</h3>' +
        '<p class="rc-t">' + (e.src ? 'We source this part. Fitment checked before we quote.' : 'Not listed yet. We check fitment and quote.') + '</p>' +
        '<div class="rc-a">' + addBtn(e, 'btn btn-p btn-s', SPECIAL[e.part] ? 'Check fitment' : 'Get a quote') + '</div></div></article>';
    }
    var det = e.url ? '<a class="btn btn-g btn-s" href="' + esc(ROOT + e.url) + '">Details</a>' : '<button type="button" class="btn btn-g btn-s" data-det="' + esc(e.id) + '">Details</button>';
    return '<article class="rc"><div class="rc-ic">' + iconSvg(e.part) + mediaHtml(e) + '</div><div class="rc-b">' +
      '<span class="chip">' + esc(veh) + '</span><h3>' + hlTitle(e, P) + '</h3>' +
      '<p class="rc-t">' + esc(e.partName) + (e.oem ? ' &middot; OE ' + esc(e.oem) : '') + '</p>' +
      '<div class="rc-m">' + (SIDE[e.side] ? '<span class="pill side">' + SIDE[e.side] + '</span>' : '') + '</div>' +
      '<div class="rc-a">' + addBtn(e, 'btn btn-p btn-s', SPECIAL[e.part] ? 'Check fitment' : 'Get a quote') + det + '</div></div></article>';
  }
  function understood(P) {
    var c = [];
    if (P.brand) c.push(brandName(P.brand));
    if (P.model) c.push(modelName(P.model));
    Object.keys(P.parts).filter(function (s) { return P.parts[s] >= 1; }).forEach(function (s) { c.push(partName(s)); });
    if (!c.length && P.hasPart) c.push('Lamps / bumpers');
    return c.length ? '<p class="und">Looking for: ' + c.map(function (x) { return '<b>' + esc(x) + '</b>'; }).join(' &middot; ') + '</p>' : '';
  }
  function notListed(q) {
    return '<div class="nl"><h3>Not listed?</h3><p>We may still have it. Ask us on WhatsApp.</p>' +
      '<a class="btn btn-p" href="' + esc(enqFree(q)) + '">Ask on WhatsApp</a></div>';
  }
  function emptyHtml(name) {
    var t = name ? name + ' ' : '';
    return '<div class="empty"><p>No ' + esc(t) + 'listings yet. Ask us on WhatsApp and we check.</p><a class="btn btn-p btn-s" href="' + esc(enqFree(t + 'part')) + '">Ask on WhatsApp</a></div>';
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
    if (norm(q) && r.onlyAsk) h += '<p class="weak">No listing for that yet. Tap Get a quote and we check.</p>';
    else if (norm(q) && r.weak && n) h += '<p class="weak">No exact match. Showing the nearest listings.</p>';
    if (norm(q) && !n) h += '<p class="weak">No listing matches that yet.</p>';
    if (n) {
      h += '<div class="rgrid">' + shown.map(function (x) { return card(x.e, r.P); }).join('') + '</div>';
      if (o.seeAll && n > shown.length) h += '<p class="seeall"><a class="btn btn-g" href="' + esc(o.seeAll + '?q=' + encodeURIComponent(q)) + '">See all ' + n + ' results</a></p>';
      if (o.more && n > shown.length) h += '<p class="seeall"><button type="button" class="btn btn-g" data-more="1">Show more (' + (n - shown.length) + ')</button></p>';
    } else if (!norm(q) && o.showAll) h += emptyHtml('');
    if (norm(q)) h += notListed(q);
    box.innerHTML = h; hydrate(box);
    return r;
  }

  /* ---------- UI wiring (browser only) ---------- */
  var toastT;
  function toast(m) { if (typeof document === 'undefined') return; var t = document.getElementById('toast'); if (!t) return; if (m.html) t.innerHTML = m.html; else t.textContent = m; t.classList.add('on'); clearTimeout(toastT); toastT = setTimeout(function () { t.classList.remove('on'); }, 3800); }
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function debounce(f, ms) { var t; return function () { var a = arguments; clearTimeout(t); t = setTimeout(function () { f.apply(null, a); }, ms); }; }

  function modal(e) {
    var m = $('#det'); if (m) m.remove();
    var veh = ((e.brandName || '') + ' ' + (e.model || '')).trim();
    m = document.createElement('div'); m.id = 'det'; m.className = 'modal'; m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true'); m.setAttribute('aria-label', e.title);
    m.innerHTML = '<div class="m-box"><button class="m-x" aria-label="Close" type="button">&times;</button><div class="m-ic">' + iconSvg(e.part) + '</div><p class="kick">' + esc(veh || e.brandName) + '</p><h2>' + esc(e.title) + '</h2>' +
      '<dl class="facts"><div><dt>Part type</dt><dd>' + esc(e.partName) + '</dd></div>' + (SIDE[e.side] ? '<div><dt>Side</dt><dd>' + SIDE[e.side] + '</dd></div>' : '') +
      (e.oem ? '<div><dt>OE no.</dt><dd>' + esc(e.oem) + '</dd></div>' : '') + (e.grade ? '<div><dt>Grade</dt><dd>' + esc(e.grade) + '</dd></div>' : '') +
      (e.desc ? '<div><dt>About</dt><dd>' + esc(e.desc) + '</dd></div>' : '') + (e.note ? '<div><dt>Note</dt><dd>' + esc(e.note) + '</dd></div>' : '') + '</dl>' +
            '<p class="mu small">We confirm fitment against your build date, market, trim and OE number before quoting.</p><div class="btns">' + addBtn(e, 'btn btn-p', 'Check fitment &amp; get a quote') + '</div></div>';
    document.body.appendChild(m); document.body.classList.add('noscroll');
    function close() { m.remove(); document.body.classList.remove('noscroll'); document.removeEventListener('keydown', key); }
    function key(ev) { if (ev.key === 'Escape') close(); }
    m.addEventListener('click', function (ev) { if (ev.target === m || ev.target.closest('.m-x,.m-c')) close(); });
    document.addEventListener('keydown', key);
    var f = $('.m-x', m); if (f) f.focus();
  }

  function initSearchBox(form) {
    var id = form.getAttribute('data-search'), input = $('.sin', form), res = $('.sres', form);
    if (id === 'cq' || !res || !input) return;
    var home = id === 'hq';
    var run = function () { renderSearch(res, input.value, { limit: 6, seeAll: ROOT + 'catalogue/' }); };
    input.addEventListener('input', debounce(run, 120));
    renderers.push(function () { if (norm(input.value)) run(); });
    $$('[data-try]', form).forEach(function (b) { b.addEventListener('click', function () { input.value = b.getAttribute('data-try'); run(); input.focus({ preventScroll: true }); if (res.scrollIntoView && home && window.innerWidth < 760) setTimeout(function () { res.scrollIntoView({ behavior: 'smooth', block: 'start' }); }, 60); }); });
    var u = new URLSearchParams(location.search); if (u.get('q') && home) { input.value = u.get('q'); run(); }
  }

  function initCatalogue() {
    var form = document.getElementById('cat-form'); if (!form) return;
    var input = $('#cq-q'), res = document.getElementById('cat-res'), count = document.getElementById('cat-count');
    var fb = $('#f-brand'), fm = $('#f-model'), fp = $('#f-part'), shown = 24;
    function fillBrands() {
      var cur = fb.value; fb.innerHTML = '<option value="">All brands</option>' + S.brands.map(function (b) { return '<option value="' + esc(b.key) + '">' + esc(b.name) + '</option>'; }).join(''); fb.value = cur;
    }
    function fillModels() {
      var cur = fm.value; fm.innerHTML = '<option value="">All models</option>';
      S.cars.filter(function (c) { return c.b === fb.value; }).forEach(function (m) { fm.insertAdjacentHTML('beforeend', '<option value="' + esc(m.slug) + '">' + esc(m.name) + '</option>'); });
      fm.disabled = !fb.value || fm.options.length < 2; if (cur) fm.value = cur;
    }
    function pool() { return ALL.filter(function (e) { return (!fb.value || e.brand === fb.value) && (!fm.value || e.carSlug === fm.value) && (!fp.value || e.part === fp.value); }); }
    function run(reset) {
      if (reset) shown = 24;
      var q = input.value, fq = [q, fb.value ? brandName(fb.value) : '', fm.value ? (S.cars.filter(function (c) { return c.b === fb.value && c.slug === fm.value; })[0] || {}).name || '' : '', fp.value ? partName(fp.value) : ''].filter(Boolean).join(' ').replace(/ — /g, ' ');
      /* every part we can source counts: listed parts and order-in parts alike */
      var r = renderSearch(res, q, { pool: pool(), shown: shown, showAll: true, more: true, limit: 24 }), n = r.results.length;
      count.innerHTML = '<b>' + n.toLocaleString('en-SG') + '</b> ' + (n === 1 ? 'part' : 'parts') + (fq ? ' for &ldquo;' + esc(fq) + '&rdquo;' : ' we can source');
      var u = new URLSearchParams(); if (q) u.set('q', q); if (fb.value) u.set('brand', fb.value); if (fm.value) u.set('model', fm.value); if (fp.value) u.set('part', fp.value);
      try { history.replaceState(null, '', location.pathname + (u.toString() ? '?' + u.toString() : '')); } catch (e) { }
    }
    function match(sel, v) { if (!v) return ''; var s = slug(v); for (var i = 0; i < sel.options.length; i++) if (sel.options[i].value === v || slug(sel.options[i].text) === s) return sel.options[i].value; return ''; }
    var u = new URLSearchParams(location.search);
    fillBrands(); fb.value = match(fb, u.get('brand')); fillModels(); fm.value = match(fm, u.get('model')); fp.value = match(fp, u.get('part')); input.value = u.get('q') || '';
    fb.addEventListener('change', function () { fm.value = ''; fillModels(); run(true); });
    fm.addEventListener('change', function () { run(true); }); fp.addEventListener('change', function () { run(true); });
    input.addEventListener('input', debounce(function () { run(true); }, 120));
    form.addEventListener('submit', function (ev) { ev.preventDefault(); run(true); });
    $('#f-clear').addEventListener('click', function () { input.value = ''; fb.value = ''; fm.value = ''; fp.value = ''; fillModels(); run(true); });
    $$('[data-try]', form).forEach(function (b) { b.addEventListener('click', function () { input.value = b.getAttribute('data-try'); fb.value = ''; fm.value = ''; fp.value = ''; fillModels(); run(true); }); });
    res.addEventListener('click', function (ev) { if (ev.target.closest('[data-more]')) { shown += 24; run(false); } });
    renderers.push(function () { var b = fb.value, m = fm.value; fillBrands(); fb.value = b; fillModels(); fm.value = m; run(false); });
    run(true);
  }

  function initLists() {
    var boxes = $$('[data-list]');
    function draw() {
      boxes.forEach(function (box) {
        var spec = box.getAttribute('data-list').split(':'), lim = +box.getAttribute('data-limit') || 9, name = box.getAttribute('data-name') || '', list, href = ROOT + 'catalogue/';
        if (spec[0] === 'brand') { list = ALL.filter(function (e) { return e.brand === spec[1]; }); href += '?brand=' + spec[1]; }
        else if (spec[0] === 'car') { list = ALL.filter(function (e) { return e.modelSlug === spec[1]; }); var c = CARM[spec[1]]; if (c) href += '?brand=' + c.b + '&model=' + c.slug; }
        else if (spec[0] === 'new') { list = ENTRIES.slice(); var sec = box.closest('[data-new-sec]'); if (sec) sec.hidden = !list.length; }
        else { var ps = spec[1].split(','); list = ALL.filter(function (e) { return ps.indexOf(e.part) >= 0; }); href += '?part=' + ps[0]; }
        if (!list.length) { box.innerHTML = spec[0] === 'new' ? '' : emptyHtml(name); return; }
        box.innerHTML = '<div class="rgrid">' + list.slice(0, lim).map(function (e) { return card(e); }).join('') + '</div>' +
          (list.length > lim ? '<p class="seeall"><a class="btn btn-g" href="' + esc(href) + '">See all ' + list.length + ' parts</a></p>' : '');
        hydrate(box);
      });
    }
    if (boxes.length) { renderers.push(draw); draw(); }
  }


  /* ---------- cart (localStorage ev_cart_v1) -> WhatsApp order ---------- */
  var CK = 'ev_cart_v1', drawer = null;
  function cartGet() { var c = lsGet(CK, null); return c && Array.isArray(c.items) ? c : { items: [], name: '', note: '', sent: false }; }
  function cartPut(c) { lsSet(CK, c); badge(); if (drawer && document.body.classList.contains('cart-open')) drawDrawer(); }
  function badge() {
    var n = cartGet().items.reduce(function (a, i) { return a + (+i.qty || 0); }, 0);
    $$('[data-cart-count]').forEach(function (b) { b.textContent = n; b.hidden = !n; });
  }
  function cartAdd(it) {
    var c = cartGet(), f = c.items.filter(function (x) { return x.id === it.id; })[0];
    if (f) f.qty = Math.min(99, f.qty + 1); else c.items.push({ id: it.id, title: it.title, car: it.car, part: it.part, side: it.side, price: it.price, ask: it.ask, qty: 1 });
    c.sent = false; cartPut(c);
    toast({ html: 'Added to cart <button type="button" data-cart-open>View cart</button>' });
  }
  function cartTotals(c) {
    var t = 0, ask = 0; c.items.forEach(function (i) { if (i.price) t += i.price * i.qty; else ask += i.qty; });
    return { total: t, ask: ask };
  }
  function orderText(c) {
    var L = ['Hi ' + D.brand + ', I would like to order:', ''], T = cartTotals(c);
    c.items.forEach(function (i, n) { L.push((n + 1) + '. ' + i.qty + ' x ' + i.title + ' - ' + (i.price ? money(i.price) + ' each' : 'price?')); });
    L.push('');
    L.push(T.total ? 'Total: ' + money(T.total) + (T.ask ? ' + ' + T.ask + ' item' + (T.ask > 1 ? 's' : '') + ' priced on request' : '') : 'Total: price on request');
    if (c.name) L.push('Name: ' + c.name);
    if (c.note) L.push('Note: ' + c.note);
    L.push('', 'Please confirm fitment. I can send the build year, VIN and photos of the old part here.', '(from website)');
    return L.join('\n');
  }
  function cartSet(o) {
    if (o && !drawer) buildDrawer();
    document.body.classList.toggle('cart-open', !!o);
    if (o) { document.body.classList.remove('menu'); drawDrawer(); var x = $('.cdr-x', drawer); if (x) x.focus({ preventScroll: true }); }
  }
  function buildDrawer() {
    drawer = document.createElement('aside'); drawer.className = 'cdr'; drawer.setAttribute('role', 'dialog'); drawer.setAttribute('aria-label', 'Your cart'); drawer.setAttribute('aria-modal', 'true');
    document.body.appendChild(drawer);
    drawer.addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-q],[data-rm],[data-send],[data-clear],.cdr-x'); if (!b) return; var c = cartGet();
      if (b.hasAttribute('data-q')) { var i = c.items[+b.getAttribute('data-i')]; if (i) { i.qty = Math.max(1, Math.min(99, i.qty + +b.getAttribute('data-q'))); cartPut(c); } }
      else if (b.hasAttribute('data-rm')) { c.items.splice(+b.getAttribute('data-rm'), 1); cartPut(c); }
      else if (b.hasAttribute('data-clear')) { c = { items: [], name: c.name, note: '', sent: false }; cartPut(c); }
      else if (b.hasAttribute('data-send')) {
        if (!c.items.length || !D.wa) return;
        var url = 'https://wa.me/' + D.wa + '?text=' + encodeURIComponent(orderText(c));
        if (root.p1WaTap) { try { root.p1WaTap(b); } catch (e) { } }
        c.sent = true; lsSet(CK, c);
        var w = root.open(url, '_blank', 'noopener'); if (!w) root.location.href = url;
        drawDrawer();
      } else cartSet(false);
    });
    drawer.addEventListener('input', function (ev) { var c = cartGet(); if (ev.target.name === 'name') c.name = ev.target.value; if (ev.target.name === 'note') c.note = ev.target.value; lsSet(CK, c); });
  }
  function drawDrawer() {
    if (!drawer) return; var c = cartGet(), T = cartTotals(c), h = '<div class="cdr-h"><h2>Your cart</h2><button type="button" class="cdr-x" aria-label="Close cart">&times;</button></div>';
    if (!c.items.length) {
      h += '<div class="cdr-b"><p class="cdr-e">Your cart is empty.</p><p class="mu">Find a part, tap Add to cart, then send the order on WhatsApp.</p><a class="btn btn-p" href="' + ROOT + 'catalogue/">Search the catalogue</a></div>';
    } else {
      h += '<div class="cdr-b"><ul class="cl">' + c.items.map(function (i, n) {
        return '<li><div class="cl-t"><b>' + esc(i.title) + '</b><span>' + (i.price ? money(i.price) + ' each' : 'Price on request') + '</span></div>' +
          '<div class="cl-q"><button type="button" data-q="-1" data-i="' + n + '" aria-label="Less">&minus;</button><b>' + i.qty + '</b><button type="button" data-q="1" data-i="' + n + '" aria-label="More">+</button>' +
          '<button type="button" class="cl-rm" data-rm="' + n + '" aria-label="Remove ' + esc(i.title) + '">Remove</button></div></li>';
      }).join('') + '</ul>' +
        '<div class="cdr-tot"><span>Total</span><b>' + (T.total ? money(T.total) : 'Price on request') + '</b></div>' + (T.total && T.ask ? '<p class="mu small">+ ' + T.ask + ' item' + (T.ask > 1 ? 's' : '') + ' priced on request</p>' : '') +
        '<label class="cdr-f">Your name (optional)<input name="name" autocomplete="name" value="' + esc(c.name || '') + '"></label>' +
        '<label class="cdr-f">Note (optional)<textarea name="note" rows="2" placeholder="Car year, left or right, photo to follow...">' + esc(c.note || '') + '</textarea></label></div>' +
        '<div class="cdr-ft">' + (c.sent ? '<p class="cdr-s">Order opened in WhatsApp. Send it there, then clear the cart.</p><button type="button" class="btn btn-g" data-clear>Clear cart</button>' : '') +
        '<button type="button" class="btn btn-p btn-l" data-send>' + (D.wa ? 'Send order on WhatsApp' : 'WhatsApp not set') + '</button></div>';
    }
    drawer.innerHTML = h;
  }
  function initCart() {
    /* enquiry-first (31 Oct 2026): the cart is retired; clear any cart saved by the old version */
    try { localStorage.removeItem(CK); } catch (x) {}
    return;
    badge();
    document.addEventListener('click', function (ev) {
      var a = ev.target.closest('[data-add]');
      if (a) { ev.preventDefault(); var pr = a.getAttribute('data-price'); cartAdd({ id: a.getAttribute('data-key'), title: a.getAttribute('data-title'), car: a.getAttribute('data-car'), part: a.getAttribute('data-part'), side: a.getAttribute('data-side') || '', price: pr ? +pr : null, ask: !!a.getAttribute('data-ask') }); return; }
      var o = ev.target.closest('[data-cart-open]'); if (o) { ev.preventDefault(); cartSet(true); }
    });
    root.addEventListener('storage', function (ev) { if (ev.key === CK) badge(); });
    if (location.hash === '#cart') cartSet(true);
  }

  function initChrome() {
    var bg = $('.burger'), nav = $('#nav');
    function menuSet(o) { document.body.classList.toggle('menu', o); if (bg) { bg.setAttribute('aria-expanded', o ? 'true' : 'false'); bg.setAttribute('aria-label', o ? 'Close menu' : 'Open menu'); } if (o) { var f = $('a', nav); if (f) f.focus({ preventScroll: true }); } }
    if (bg && nav) {
      bg.addEventListener('click', function () { cartSet(false); menuSet(!document.body.classList.contains('menu')); });
      $$('[data-menu-close],[data-scrim]').forEach(function (x) { x.addEventListener('click', function () { menuSet(false); cartSet(false); }); });
      $$('a', nav).forEach(function (a) { a.addEventListener('click', function () { menuSet(false); }); });
      document.addEventListener('keydown', function (ev) { if (ev.key === 'Escape') { menuSet(false); cartSet(false); } });
    }
    var hd = $('.hd'); if (hd) { var f = function () { hd.classList.toggle('scr', window.scrollY > 8); }; window.addEventListener('scroll', f, { passive: true }); f(); }
    if ('IntersectionObserver' in window) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add('in'); io.unobserve(x.target); } }); }, { rootMargin: '0px 0px -6% 0px', threshold: 0.05 });
      $$('.rv').forEach(function (el) { io.observe(el); });
    } else { $$('.rv').forEach(function (el) { el.classList.add('in'); }); }
    document.addEventListener('click', function (ev) {
      var d = ev.target.closest('[data-det]'); if (!d) return;
      var id = d.getAttribute('data-det'), e = ENTRIES.filter(function (x) { return x.id === id; })[0]; if (e) modal(e);
    });
  }

  function init() {
    $$('[data-search]').forEach(initSearchBox);
    initCatalogue(); initLists(); initChrome(); initCart();
    liveLoad();
  }

  root.EV = { D: D, K: K, ROOT: ROOT, search: search, parse: parse, norm: norm, esc: esc, slug: slug, setData: setData, state: S, entries: function () { return ENTRIES; },
    liveLoad: liveLoad, applyLive: applyLive, card: card, enqHref: enqHref, toast: toast, loadPhoto: loadPhoto, cartGet: function () { return cartGet(); }, brandName: brandName, modelName: modelName, partName: partName };
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
  }
})(typeof window !== 'undefined' ? window : globalThis);
