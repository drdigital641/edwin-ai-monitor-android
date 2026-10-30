/* Autotex staff dashboard (live). Vanilla JS, talks to the Base44 API on the same origin. */
(function () {
  'use strict';
  var APP = '6ae3683191b1a44205dbf5ec';
  var BASE = '/api/apps/' + APP;
  var D = window.AT_DEFS || { brands: [], cats: [], parts: [] };
  var root = document.getElementById('app');
  var TOKEN_KEY = 'base44_access_token';
  var PAGE = 50, MAXPH = 6;
  var STOCK = { '': 'Not set', 'in': 'In stock', 'order': 'Order from Korea', 'out': 'Out of stock' };
  var SIDES = { '': 'None', 'L': 'Left', 'R': 'Right', 'pair': 'Pair' };
  var FUELS = ['petrol', 'diesel', 'hybrid', 'electric', 'petrol / hybrid', 'petrol / diesel'];

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function byId(list) { var o = {}; list.forEach(function (x) { o[x.id] = x; }); return o; }
  var BR = byId(D.brands), CA = byId(D.cats), PA = byId(D.parts);
  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* ignore */ } }
  function lsDel(k) { try { localStorage.removeItem(k); } catch (e) { /* ignore */ } }
  function slug(s) { return String(s || '').toLowerCase().replace(/&/g, ' and ').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, ''); }
  function money(n) {
    if (n == null || n === '' || isNaN(n)) return 'Ask for price';
    n = Number(n);
    var s = (Math.round(n * 100) % 100 === 0) ? String(Math.round(n)) : n.toFixed(2);
    var p = s.split('.');
    p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return 'S$' + p.join('.');
  }
  function parsePrice(v) {
    if (v == null) return null;
    var s = String(v).replace(/s\$|\$|,|\s/gi, '');
    if (s === '') return null;
    var n = Number(s);
    return isNaN(n) || n < 0 ? NaN : n;
  }
  function uid() { return 'p' + Date.now().toString(36) + Math.random().toString(36).slice(2, 7); }
  function $(sel, el) { return (el || document).querySelector(sel); }
  var toastT;
  function toast(msg, ms) {
    var t = document.getElementById('toast'); if (!t) return;
    t.textContent = msg; t.className = 'st-toast on';
    clearTimeout(toastT); toastT = setTimeout(function () { t.className = 'st-toast'; }, ms || 3000);
  }
  function safeSrc(u) {
    u = String(u || '');
    return /^(https?:\/\/|data:image\/|blob:|\/)/i.test(u) ? u : '';
  }

  /* ---------- API ---------- */
  var token = lsGet(TOKEN_KEY) || '';
  var user = null;
  function headers(extra) {
    var h = { 'X-App-Id': APP, 'Content-Type': 'application/json' };
    if (token) h.Authorization = 'Bearer ' + token;
    if (extra) for (var k in extra) h[k] = extra[k];
    return h;
  }
  function signOutExpired() {
    lsDel(TOKEN_KEY); lsDel('token'); token = ''; user = null; renderSignIn('Your session ended. Please sign in again.');
  }
  function api(method, path, body) {
    return fetch(BASE + path, { method: method, headers: headers(), body: body === undefined ? undefined : JSON.stringify(body) })
      .catch(function () { throw new Error('No connection. Check your internet and try again.'); })
      .then(function (res) {
        if (res.status === 401) { signOutExpired(); throw new Error('Signed out'); }
        if (!res.ok) {
          return res.text().then(function (t) {
            var m = ''; try { var j = JSON.parse(t); m = j.message || j.detail || j.error || ''; } catch (e) { m = ''; }
            throw new Error((m && typeof m === 'string' ? m : 'Server error') + ' (' + res.status + ')');
          });
        }
        if (res.status === 204) return null;
        return res.text().then(function (t) { try { return t ? JSON.parse(t) : null; } catch (e) { return null; } });
      });
  }
  function listAll(entity, sort, q) {
    var out = [];
    function page(skip) {
      var p = '/entities/' + entity + '?limit=500&skip=' + skip + '&sort=' + encodeURIComponent(sort || '-updated_date');
      if (q) p += '&q=' + encodeURIComponent(JSON.stringify(q));
      return api('GET', p).then(function (r) {
        r = Array.isArray(r) ? r : [];
        out = out.concat(r);
        return r.length >= 500 ? page(skip + 500) : out;
      });
    }
    return page(0);
  }
  function logAct(what) {
    api('POST', '/entities/AtLog', { who: user ? user.email : '', what: what }).catch(function () { /* log is best effort */ });
  }
  function runPool(items, n, fn) {
    var i = 0, ok = 0, fail = 0, errs = [];
    function next() {
      if (i >= items.length) return Promise.resolve();
      var it = items[i++];
      return fn(it).then(function () { ok++; }, function (e) { fail++; errs.push(e && e.message); }).then(next);
    }
    var w = []; for (var k = 0; k < Math.min(n, items.length); k++) w.push(next());
    return Promise.all(w).then(function () { return { ok: ok, fail: fail, errs: errs }; });
  }

  /* ---------- state ---------- */
  var cars = [], products = [], CM = {}, PM = {};
  var S = { tab: 'quick', shown: PAGE, sel: {}, F: { q: '', brand: '', car: '', status: '', nophoto: false, noprice: false } };
  var Q, E = null, importState = null, logs = null;
  function newQ(keep) {
    Q = { brand: keep ? Q.brand : '', car: keep ? Q.car : '', part: '', pn: '', pc: '', psearch: '', side: '', price: '', stock: '', oem: '', note: '', photos: [], addCar: false, ac: { name: '', code: '', years: '', fuel: 'petrol' }, err: '', saving: false, done: null };
  }
  newQ(false);
  function reindex() {
    CM = {}; PM = {};
    cars.forEach(function (c) { CM[c.key] = c; });
    products.forEach(function (p) { PM[p.id] = p; });
  }
  function carLabel(key) {
    var c = CM[key]; if (!c) return key || '';
    return (BR[c.b] ? BR[c.b].name + ' ' : '') + c.name + (c.code ? ' (' + c.code + ')' : '');
  }
  function carShort(c) { return c.name + (c.code ? ' ' + c.code : ''); }
  function partName(p) { var d = PA[p.p]; return d ? d.name : (p.pn || 'Other part'); }
  function partCat(p) { var d = PA[p.p]; return d ? d.cat : (p.pc || ''); }
  function brandOfProduct(p) { var c = CM[p.m]; return c ? c.b : ''; }

  /* ---------- photos ---------- */
  var b44cache = {};
  function photoImg(val, cls) {
    val = String(val || '');
    if (val.indexOf('b44photo:') === 0) {
      var id = val.slice(9);
      if (b44cache[id]) return '<img alt="" ' + (cls ? 'class="' + cls + '" ' : '') + 'src="' + esc(safeSrc(b44cache[id])) + '">';
      return '<img alt="" ' + (cls ? 'class="' + cls + '" ' : '') + 'data-b44="' + esc(id) + '" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==">';
    }
    var s = safeSrc(val);
    return s ? '<img alt="" loading="lazy" ' + (cls ? 'class="' + cls + '" ' : '') + 'src="' + esc(s) + '">' : '';
  }
  function hydrate() {
    var imgs = document.querySelectorAll('img[data-b44]');
    Array.prototype.forEach.call(imgs, function (img) {
      var id = img.getAttribute('data-b44'); img.removeAttribute('data-b44');
      if (b44cache[id]) { img.src = b44cache[id]; return; }
      api('GET', '/entities/AtPhoto/' + encodeURIComponent(id)).then(function (r) {
        if (r && r.data) { b44cache[id] = r.data; img.src = safeSrc(r.data); }
      }).catch(function () { /* ignore */ });
    });
  }
  function readImage(file) {
    if (window.createImageBitmap) {
      return createImageBitmap(file, { imageOrientation: 'from-image' }).catch(function () { return viaImg(file); });
    }
    return viaImg(file);
  }
  function viaImg(file) {
    return new Promise(function (res, rej) {
      var u = URL.createObjectURL(file), im = new Image();
      im.onload = function () { URL.revokeObjectURL(u); res(im); };
      im.onerror = function () { URL.revokeObjectURL(u); rej(new Error('Could not read this photo')); };
      im.src = u;
    });
  }
  function compress(file, max, q) {
    return readImage(file).then(function (img) {
      var w = img.width || img.naturalWidth, h = img.height || img.naturalHeight;
      var sc = Math.min(1, max / Math.max(w, h));
      var cw = Math.max(1, Math.round(w * sc)), ch = Math.max(1, Math.round(h * sc));
      var cv = document.createElement('canvas'); cv.width = cw; cv.height = ch;
      var cx = cv.getContext('2d'); cx.fillStyle = '#fff'; cx.fillRect(0, 0, cw, ch); cx.drawImage(img, 0, 0, cw, ch);
      if (img.close) img.close();
      return new Promise(function (res, rej) {
        cv.toBlob(function (b) { b ? res(b) : rej(new Error('Could not compress this photo')); }, 'image/jpeg', q);
      });
    });
  }
  function blobToDataUrl(b) {
    return new Promise(function (res, rej) {
      var r = new FileReader(); r.onload = function () { res(r.result); }; r.onerror = function () { rej(new Error('read failed')); };
      r.readAsDataURL(b);
    });
  }
  function uploadBlob(blob, onPct) {
    return new Promise(function (res, rej) {
      var x = new XMLHttpRequest(), fd = new FormData();
      fd.append('file', blob, 'photo.jpg');
      x.open('POST', BASE + '/integration-endpoints/Core/UploadFile');
      x.setRequestHeader('X-App-Id', APP);
      if (token) x.setRequestHeader('Authorization', 'Bearer ' + token);
      x.upload.onprogress = function (e) { if (e.lengthComputable) onPct(Math.round(e.loaded / e.total * 100)); };
      x.onerror = function () { rej(new Error('network')); };
      x.onload = function () {
        if (x.status < 200 || x.status >= 300) return rej(new Error('upload ' + x.status));
        try { var j = JSON.parse(x.responseText); if (j && j.file_url) return res(j.file_url); } catch (e) { /* fall through */ }
        rej(new Error('bad upload reply'));
      };
      x.send(fd);
    });
  }
  function ctxOf(name) { return name === 'q' ? Q : (E ? E.d : null); }
  function photoKey(name) {
    if (name === 'e' && E) return E.rec.key;
    return quickKey() || ('draft-' + Date.now());
  }
  function addPhotos(name, files) {
    var ctx = ctxOf(name); if (!ctx) return;
    var room = MAXPH - ctx.photos.length;
    files = Array.prototype.slice.call(files).filter(function (f) { return /^image\//.test(f.type) || !f.type; });
    if (files.length > room) toast('Max ' + MAXPH + ' photos. Extra ones skipped.');
    files.slice(0, Math.max(0, room)).forEach(function (f) {
      var it = { id: uid(), val: null, prev: null, state: 'busy', pct: 0, file: f, msg: '' };
      ctx.photos.push(it);
      processPhoto(name, it);
    });
    refreshPhotos(name);
  }
  function processPhoto(name, it) {
    var ctx = ctxOf(name);
    it.state = 'busy'; it.pct = 0; it.msg = '';
    compress(it.file, 1280, 0.78).then(function (blob) {
      it.blob = blob; if (!it.prev) it.prev = URL.createObjectURL(blob);
      refreshPhotos(name);
      return uploadBlob(blob, function (p) { it.pct = p; refreshPhotos(name); }).then(function (url) {
        it.val = url; it.state = 'ok';
      }, function (e1) {
        /* fallback (e.g. Base44 upload credits used up): store a smaller copy as an AtPhoto record */
        var sizes = [[900, 0.7], [720, 0.62], [560, 0.55], [420, 0.5]];
        function shrink(i) {
          return compress(it.file, sizes[i][0], sizes[i][1]).then(blobToDataUrl).then(function (data) {
            return (data.length > 110000 && i < sizes.length - 1) ? shrink(i + 1) : data;
          });
        }
        return shrink(0).then(function (data) {
          return api('POST', '/entities/AtPhoto', { data: data, product: photoKey(name) });
        }).then(function (rec) {
          if (!rec || !rec.id) throw new Error('no id');
          it.val = 'b44photo:' + rec.id; it.state = 'ok';
        }, function (e2) {
          var m = 'upload: ' + ((e1 && e1.message) || 'failed') + '; backup: ' + ((e2 && e2.message) || 'failed');
          try { api('POST', '/entities/AtLog', { who: (user && user.email) || '', what: 'Photo failed (' + m + ')' }); } catch (x) { /* ignore */ }
          throw new Error(m);
        });
      });
    }).catch(function (e) {
      it.state = 'err'; it.msg = e && e.message ? e.message : 'failed';
    }).then(function () {
      if (ctxOf(name) === ctx) refreshPhotos(name);
    });
  }
  function photoErr(ctx) {
    var f = (ctx.photos || []).filter(function (p) { return p.state === 'err' && p.msg; })[0];
    return f ? ' (' + f.msg + ')' : '';
  }
  function photosHTML(name) {
    var ctx = ctxOf(name), h = '';
    h += '<div class="st-thumbs">';
    ctx.photos.forEach(function (it, i) {
      var img = it.prev ? '<img alt="" src="' + esc(it.prev) + '">' : photoImg(it.val);
      h += '<div class="st-thumb">' + img;
      if (i === 0) h += '<span class="st-tag">Main</span>';
      if (it.state === 'busy') h += '<div class="st-prog">' + (it.pct ? it.pct + '%' : 'Working...') + '</div>';
      if (it.state === 'err') h += '<div class="st-prog bad" data-a="retry" data-c="' + name + '" data-i="' + esc(it.id) + '">Failed. Tap to retry</div>';
      h += '<button type="button" class="st-tx" aria-label="Remove photo" data-a="rmph" data-c="' + name + '" data-i="' + esc(it.id) + '">&times;</button>';
      if (i > 0) h += '<button type="button" class="st-tl" aria-label="Move earlier" title="Move earlier" data-a="mvph" data-c="' + name + '" data-i="' + esc(it.id) + '">&lsaquo;</button>';
      h += '</div>';
    });
    h += '</div>';
    if (!ctx.photos.length) h = '';
    var full = ctx.photos.length >= MAXPH;
    h += '<div class="st-photobtns">' +
      '<label class="btn primary" for="cam-' + name + '"' + (full ? ' aria-disabled="true"' : '') + '>&#128247; Take photo</label>' +
      '<label class="btn" for="gal-' + name + '">Gallery</label></div>' +
      '<input class="st-hiddenin" id="cam-' + name + '" type="file" accept="image/*" capture="environment" multiple data-ph="' + name + '">' +
      '<input class="st-hiddenin" id="gal-' + name + '" type="file" accept="image/*" multiple data-ph="' + name + '">' +
      '<p class="st-hint">' + ctx.photos.length + ' of ' + MAXPH + ' photos. The first photo is the main one. Use &lsaquo; to move a photo earlier.</p>';
    return h;
  }
  function refreshPhotos(name) {
    var el = document.getElementById('ph-' + name);
    if (el) { el.innerHTML = photosHTML(name); hydrate(); }
  }
  function photosBusy(ctx) { return ctx.photos.some(function (p) { return p.state === 'busy'; }); }
  function photosBad(ctx) { return ctx.photos.some(function (p) { return p.state === 'err'; }); }
  function photoVals(ctx) { return ctx.photos.filter(function (p) { return p.state === 'ok' && p.val; }).map(function (p) { return p.val; }); }

  /* ---------- keys ---------- */
  function takenKey(k) { return products.some(function (p) { return p.key === k; }); }
  function uniqueKey(base) {
    var k = base, n = 2;
    while (takenKey(k)) { k = base + '-' + n; n++; }
    return k;
  }
  function quickKey() {
    if (!Q.car) return '';
    var c = CM[Q.car]; if (!c) return '';
    var part = Q.part && Q.part !== 'other' ? Q.part : (slug(Q.pn) || '');
    if (!part) return '';
    return c.b + '-' + c.key + '-' + part;
  }

  /* ---------- top-level screens ---------- */
  function headerHTML(withTabs) {
    var h = '<header class="st-header"><div class="st-header-in"><div class="st-top"><div class="st-brand"><img src="https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@a8f2a915254fc2ff888ae3dcbaefc0f9919c51d8/pageone-site/clients/autotex/staff-app/logo.svg" alt="Autotex"><b>Staff</b></div><div class="st-links">' +
      '<a class="st-link" href="https://autotexautoparts.com.sg/" target="_blank" rel="noopener">View shop</a>' +
      (user ? '<button type="button" class="st-link" data-a="signout">Sign out</button>' : '') + '</div></div>';
    if (user) h += '<div class="st-who">' + esc(user.full_name || '') + ' ' + esc(user.email) + '</div>';
    if (withTabs) {
      var tabs = [['quick', 'Quick add'], ['products', 'Products'], ['cars', 'Cars'], ['io', 'Import / Export'], ['log', 'Activity']];
      h += '<div class="st-tabs" role="tablist">' + tabs.map(function (t) {
        return '<button type="button" class="st-tab" role="tab" aria-selected="' + (S.tab === t[0]) + '" data-a="tab" data-v="' + t[0] + '">' + t[1] + '</button>';
      }).join('') + '</div>';
    }
    return h + '</div></header>';
  }
  function renderSignIn(msg) {
    root.innerHTML = headerHTML(false) + '<div class="st-center"><img src="https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@a8f2a915254fc2ff888ae3dcbaefc0f9919c51d8/pageone-site/clients/autotex/staff-app/logo.svg" alt="">' +
      '<h1 class="st-h1">Autotex Staff</h1><p class="st-note">Sign in to add and edit products. Changes go live on the website straight away.</p>' +
      (msg ? '<p class="st-err">' + esc(msg) + '</p>' : '') +
      '<button type="button" class="btn primary full" style="min-height:56px" data-a="signin">Sign in</button></div>';
  }
  function renderNotStaff() {
    root.innerHTML = headerHTML(false) + '<div class="st-center"><div class="st-card"><p>Your account (' + esc(user.email) + ') is not on the Autotex staff list yet. Ask Page One to add you.</p>' +
      '<button type="button" class="btn full" data-a="signout">Sign out</button></div></div>';
  }
  function renderLoading(msg) {
    root.innerHTML = headerHTML(false) + '<p class="st-boot">' + esc(msg || 'Loading...') + '</p>';
  }
  function renderError(msg) {
    root.innerHTML = headerHTML(false) + '<div class="st-center"><p class="st-err">' + esc(msg) + '</p><button type="button" class="btn primary" data-a="reload">Try again</button></div>';
  }
  function boot() {
    var m = /[?&]access_token=([^&#]+)/.exec(location.search);
    if (m) {
      lsSet(TOKEN_KEY, decodeURIComponent(m[1])); token = decodeURIComponent(m[1]);
      var u = new URL(location.href); u.searchParams.delete('access_token'); u.searchParams.delete('from_url');
      try { history.replaceState(null, '', u.pathname + (u.search || '') + u.hash); } catch (e) { /* ignore */ }
    }
    if (!token) return renderSignIn();
    renderLoading();
    api('GET', '/entities/User/me').then(function (me) {
      user = me || {};
      if (user.role !== 'admin') return renderNotStaff();
      renderLoading('Loading your catalogue...');
      return Promise.all([listAll('AtCar', 'name'), listAll('AtProduct', '-updated_date')]).then(function (r) {
        cars = r[0]; products = r[1]; reindex(); renderMain();
      });
    }).catch(function (e) {
      if (!token) return;
      renderError(e.message || 'Could not load.');
    });
  }
  function renderMain() {
    root.innerHTML = headerHTML(true) + '<main class="st-wrap" id="view"></main>';
    renderView();
  }
  function renderView() {
    var v = document.getElementById('view'); if (!v) return;
    var y = window.scrollY;
    v.innerHTML = S.tab === 'quick' ? quickHTML() : S.tab === 'products' ? productsHTML() : S.tab === 'cars' ? carsHTML() : S.tab === 'io' ? ioHTML() : logHTML();
    Array.prototype.forEach.call(root.querySelectorAll('.st-tab'), function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-v') === S.tab)); });
    if (S.tab === 'products') renderList();
    hydrate();
    window.scrollTo(0, y);
  }
  function setTab(t) {
    S.tab = t; window.scrollTo(0, 0);
    if (t === 'log') { logs = null; loadLogs(); }
    renderView();
  }

  /* ---------- Quick add ---------- */
  function pillsHTML(items, cur, field, ctx) {
    return '<div class="st-pills">' + items.map(function (i) {
      return '<button type="button" class="st-pill' + (cur === i[0] ? ' on' : '') + '" data-a="set" data-c="' + ctx + '" data-f="' + field + '" data-v="' + esc(i[0]) + '">' + esc(i[1]) + (i[2] ? '<small>' + esc(i[2]) + '</small>' : '') + '</button>';
    }).join('') + '</div>';
  }
  function carFormHTML(c, nameKey) {
    return '<div class="st-mini"><b>Add a car' + (Q.brand ? ' (' + esc(BR[Q.brand].name) + ')' : '') + '</b>' +
      '<label class="st-lbl" for="ac-name">Car name</label><input class="st-in" id="ac-name" data-f="ac.name" placeholder="e.g. Avante" value="' + esc(c.name) + '" autocomplete="off">' +
      '<div class="st-2col"><div><label class="st-lbl" for="ac-code">Generation code (optional)</label><input class="st-in" id="ac-code" data-f="ac.code" placeholder="e.g. CN7" value="' + esc(c.code) + '" autocomplete="off"></div>' +
      '<div><label class="st-lbl" for="ac-years">Years (optional)</label><input class="st-in" id="ac-years" data-f="ac.years" placeholder="2020-now" value="' + esc(c.years) + '" autocomplete="off"></div></div>' +
      '<label class="st-lbl" for="ac-fuel">Fuel</label><select class="st-in" id="ac-fuel" data-f="ac.fuel">' + FUELS.map(function (f) { return '<option' + (c.fuel === f ? ' selected' : '') + '>' + f + '</option>'; }).join('') + '</select>' +
      '<p class="st-err" id="ac-err"></p><div class="btns"><button type="button" class="btn primary" data-a="savecar">Save car</button><button type="button" class="btn" data-a="cancelcar">Cancel</button></div></div>';
  }
  function partPickerHTML(ctxName, cur, search) {
    var s = (search || '').toLowerCase().trim(), h = '';
    D.cats.forEach(function (cat) {
      var ps = D.parts.filter(function (p) {
        return p.cat === cat.id && (!s || (p.name + ' ' + (p.alias || []).join(' ')).toLowerCase().indexOf(s) >= 0);
      });
      if (!ps.length) return;
      h += '<div class="st-catl">' + esc(cat.name) + '</div>' + pillsHTML(ps.map(function (p) { return [p.id, p.name]; }), cur, 'part', ctxName);
    });
    if (!h) h = '<p class="st-note">No part matches. Use "Other part" below.</p>';
    h += '<div class="st-catl">Not in the list</div>' + pillsHTML([['other', 'Other part']], cur, 'part', ctxName);
    return h;
  }
  function quickHTML() {
    var h = '';
    if (Q.done) {
      h += '<div class="st-success"><b>Saved. Live on the website now.</b><p class="st-note" style="margin:4px 0 8px">' + esc(Q.done) + '</p>' +
        '<div class="btns"><button type="button" class="btn primary" data-a="another">Add another (same car)</button><button type="button" class="btn" data-a="anothercar">Different car</button></div></div>';
    }
    h += '<div class="st-card"><h2 class="st-step"><span>1</span> Photo</h2><div id="ph-q">' + photosHTML('q') + '</div>';
    h += '<h2 class="st-step"><span>2</span> Brand</h2>' + pillsHTML(D.brands.map(function (b) { return [b.id, b.name]; }), Q.brand, 'brand', 'q');
    if (Q.brand) {
      var cl = cars.filter(function (c) { return c.b === Q.brand && c.status !== 'hidden'; }).sort(function (a, b) { return carShort(a).localeCompare(carShort(b)); });
      h += '<h2 class="st-step"><span>3</span> Car</h2><div class="st-pills">' + cl.map(function (c) {
        return '<button type="button" class="st-pill' + (Q.car === c.key ? ' on' : '') + '" data-a="set" data-c="q" data-f="car" data-v="' + esc(c.key) + '">' + esc(c.name) + (c.code ? ' ' + esc(c.code) : '') + (c.years ? '<small>' + esc(c.years) + '</small>' : '') + '</button>';
      }).join('') + '<button type="button" class="st-pill add" data-a="addcar">+ Add a car</button></div>';
      if (!cl.length) h += '<p class="st-hint">No cars for ' + esc(BR[Q.brand].name) + ' yet. Tap "+ Add a car".</p>';
      if (Q.addCar) h += carFormHTML(Q.ac);
    }
    if (Q.car) {
      h += '<h2 class="st-step"><span>4</span> Part</h2><input class="st-in" type="search" placeholder="Search parts, e.g. bumper" data-f="psearch" value="' + esc(Q.psearch) + '" aria-label="Search parts" autocomplete="off">' +
        '<div id="parts-q">' + partPickerHTML('q', Q.part, Q.psearch) + '</div>';
      if (Q.part === 'other') {
        h += '<div class="st-mini"><label class="st-lbl" for="q-pn">Part name</label><input class="st-in" id="q-pn" data-f="pn" value="' + esc(Q.pn) + '" placeholder="e.g. Radiator" autocomplete="off">' +
          '<label class="st-lbl" for="q-pc">Category</label><select class="st-in" id="q-pc" data-f="pc"><option value="">Choose a category</option>' + D.cats.map(function (c) { return '<option value="' + esc(c.id) + '"' + (Q.pc === c.id ? ' selected' : '') + '>' + esc(c.name) + '</option>'; }).join('') + '</select></div>';
      }
    }
    var pd = PA[Q.part];
    if (Q.car && Q.part) {
      var n = 5;
      if ((pd && pd.side) || Q.part === 'other') {
        h += '<h2 class="st-step"><span>' + (n++) + '</span> Side</h2>' + pillsHTML([['', 'Not needed'], ['L', 'Left'], ['R', 'Right'], ['pair', 'Pair']], Q.side, 'side', 'q');
      }
      h += '<h2 class="st-step"><span>' + (n++) + '</span> Price and stock</h2>' +
        '<label class="st-lbl" for="q-price">Price in S$ (leave empty for "Ask for price")</label><input class="st-in st-bigin" id="q-price" inputmode="decimal" data-f="price" value="' + esc(Q.price) + '" placeholder="e.g. 180" autocomplete="off">' +
        '<label class="st-lbl">Stock</label>' + pillsHTML(Object.keys(STOCK).map(function (k) { return [k, STOCK[k]]; }), Q.stock, 'stock', 'q') +
        '<label class="st-lbl" for="q-oem">OEM part number (optional)</label><input class="st-in" id="q-oem" data-f="oem" value="' + esc(Q.oem) + '" autocomplete="off" autocapitalize="characters">' +
        '<label class="st-lbl" for="q-note">Note (optional)</label><textarea class="st-in" id="q-note" data-f="note" rows="2">' + esc(Q.note) + '</textarea>' +
        '<p class="st-warn">The note is visible to customers on the website.</p>';
    }
    h += '</div>';
    var ready = Q.car && Q.part;
    h += '<div class="st-savebar">' + (ready ? '<div class="st-sum" id="q-sum">' + quickSummary() + '</div>' : '') +
      '<p class="st-err" id="q-err">' + esc(Q.err) + '</p>' +
      '<button type="button" class="btn primary" id="q-save" data-a="qsave">' + (Q.saving ? 'Saving...' : 'Save product') + '</button></div>';
    return h;
  }
  function quickSummary() {
    var pd = PA[Q.part], nm = pd ? pd.name : (Q.pn || 'Other part');
    return esc(carLabel(Q.car) + ' · ' + nm + (Q.side ? ' (' + SIDES[Q.side] + ')' : '') + ' · ' + (Q.price ? money(parsePrice(Q.price)) : 'Ask for price'));
  }
  function validateDraft(d, needCar) {
    if (needCar && !d.m) return 'Choose a car first.';
    if (!d.p) return 'Choose the part.';
    if (d.p === 'other') {
      if (!String(d.pn || '').trim()) return 'Type the part name.';
      if (!d.pc) return 'Choose a category for the part.';
    }
    var pr = parsePrice(d.price);
    if (pr !== null && isNaN(pr)) return 'Price must be a number, like 180 or 45.50.';
    return '';
  }
  function recordFrom(d, key, status) {
    var r = { key: key, m: d.m, p: d.p, stock: d.stock || '', side: d.side || '', oem: String(d.oem || '').trim(), note: String(d.note || '').trim(), photos: d.photos || [], status: status || 'published' };
    if (d.p === 'other') { r.pn = String(d.pn).trim(); r.pc = d.pc; }
    var pr = parsePrice(d.price); if (pr !== null) r.price = pr;
    return r;
  }
  function quickSave() {
    if (Q.saving) return;
    var d = { m: Q.car, p: Q.part, pn: Q.pn, pc: Q.pc, price: Q.price, oem: Q.oem, stock: Q.stock, side: Q.side, note: Q.note };
    var err = !Q.brand ? 'Choose a brand first.' : validateDraft(d, true);
    if (!err && photosBusy(Q)) err = 'Photos are still uploading. Wait a moment.';
    if (!err && photosBad(Q)) err = 'A photo failed. Tap it to retry, or remove it.' + photoErr(Q);
    if (err) { Q.err = err; setText('q-err', err); return; }
    Q.err = ''; Q.saving = true; setText('q-err', ''); setText('q-save', 'Saving...');
    d.photos = photoVals(Q);
    var key = uniqueKey(quickKey());
    var rec = recordFrom(d, key, 'published');
    api('POST', '/entities/AtProduct', rec).then(function (saved) {
      saved = saved && saved.id ? saved : Object.assign({ id: 'tmp-' + key }, rec);
      products.unshift(saved); reindex();
      logAct('Added ' + carLabel(rec.m) + ' ' + (PA[rec.p] ? PA[rec.p].name : rec.pn) + ' (' + key + ')');
      var label = carLabel(rec.m) + ' · ' + (PA[rec.p] ? PA[rec.p].name : rec.pn);
      var keepB = Q.brand, keepC = Q.car;
      newQ(false); Q.brand = keepB; Q.car = keepC; Q.done = label;
      toast('Saved. Live on the website now.', 4000);
      window.scrollTo(0, 0); renderView();
    }).catch(function (e) {
      Q.saving = false; Q.err = 'Not saved: ' + (e.message || 'error') + '. Your form is still filled in. Try again.';
      setText('q-err', Q.err); setText('q-save', 'Save product');
    });
  }
  function setText(id, t) { var el = document.getElementById(id); if (el) el.textContent = t; }

  function saveCarFromForm() {
    var c = Q.ac, name = c.name.trim();
    if (!Q.brand) return setText('ac-err', 'Choose a brand first.');
    if (!name) return setText('ac-err', 'Type the car name.');
    var dupe = cars.some(function (x) { return x.b === Q.brand && x.name.toLowerCase() === name.toLowerCase() && (x.code || '').toLowerCase() === c.code.trim().toLowerCase(); });
    if (dupe) return setText('ac-err', 'That car is already in the list.');
    setText('ac-err', 'Saving...');
    createCar(Q.brand, c).then(function (rec) {
      Q.car = rec.key; Q.addCar = false; Q.ac = { name: '', code: '', years: '', fuel: 'petrol' };
      toast('Car added'); renderView();
    }).catch(function (e) { setText('ac-err', 'Could not save the car: ' + e.message); });
  }
  function createCar(brand, c) {
    var base = slug(c.name + ' ' + (c.code || '')), key = base, n = 2;
    while (CM[key]) { key = base + '-' + n; n++; }
    var nm = c.name.trim(), alias = [nm.toLowerCase()];
    if (c.code && c.code.trim()) alias.push((nm + ' ' + c.code.trim()).toLowerCase());
    var rec = { key: key, b: brand, name: nm, code: (c.code || '').trim(), years: (c.years || '').trim(), alias: alias, fuel: c.fuel || 'petrol', status: 'published' };
    return api('POST', '/entities/AtCar', rec).then(function (saved) {
      saved = saved && saved.id ? saved : Object.assign({ id: 'tmp-' + key }, rec);
      cars.push(saved); reindex(); logAct('Added car ' + carLabel(key)); return saved;
    });
  }

  /* ---------- Products ---------- */
  function filtered() {
    var F = S.F, q = F.q.toLowerCase().trim();
    return products.filter(function (p) {
      if (F.brand && brandOfProduct(p) !== F.brand) return false;
      if (F.car && p.m !== F.car) return false;
      if (F.status && (p.status || 'published') !== F.status) return false;
      if (F.nophoto && p.photos && p.photos.length) return false;
      if (F.noprice && p.price != null && p.price !== '') return false;
      if (q) {
        var c = CM[p.m] || {};
        var hay = [carLabel(p.m), (c.alias || []).join(' '), partName(p), p.oem, p.key, p.note].join(' ').toLowerCase();
        return q.split(/\s+/).every(function (w) { return hay.indexOf(w) >= 0; });
      }
      return true;
    });
  }
  function productsHTML() {
    var F = S.F;
    var cl = cars.filter(function (c) { return !F.brand || c.b === F.brand; });
    var h = '<div class="st-filters"><input class="st-in full" type="search" id="f-q" data-flt="q" placeholder="Search car, part or OEM no." value="' + esc(F.q) + '" aria-label="Search products" autocomplete="off">' +
      '<select class="st-in" data-flt="brand" aria-label="Brand"><option value="">All brands</option>' + D.brands.map(function (b) { return '<option value="' + b.id + '"' + (F.brand === b.id ? ' selected' : '') + '>' + esc(b.name) + '</option>'; }).join('') + '</select>' +
      '<select class="st-in" data-flt="car" aria-label="Car"><option value="">All cars</option>' + cl.map(function (c) { return '<option value="' + esc(c.key) + '"' + (F.car === c.key ? ' selected' : '') + '>' + esc(carShort(c)) + '</option>'; }).join('') + '</select>' +
      '<select class="st-in" data-flt="status" aria-label="Status"><option value="">Any status</option><option value="published"' + (F.status === 'published' ? ' selected' : '') + '>Published</option><option value="hidden"' + (F.status === 'hidden' ? ' selected' : '') + '>Hidden</option></select></div>' +
      '<div class="st-flags"><button type="button" class="st-pill' + (F.nophoto ? ' on' : '') + '" data-a="flag" data-v="nophoto">No photo</button><button type="button" class="st-pill' + (F.noprice ? ' on' : '') + '" data-a="flag" data-v="noprice">No price</button></div>' +
      '<div id="plist"></div>';
    return h;
  }
  function renderList() {
    var el = document.getElementById('plist'); if (!el) return;
    var list = filtered(), n = list.length, selN = Object.keys(S.sel).length;
    var h = '<div class="st-count">' + n + ' of ' + products.length + ' products</div>';
    if (!products.length) {
      el.innerHTML = '<div class="st-empty">No products yet.<br><button type="button" class="btn primary" style="margin-top:12px" data-a="tab" data-v="quick">Add the first product</button></div>'; return;
    }
    if (!n) { el.innerHTML = h + '<div class="st-empty">Nothing matches these filters.</div>'; return; }
    h += '<div class="st-bulkbar"><label class="st-chk"><input type="checkbox" data-a="selall"' + (list.every(function (p) { return S.sel[p.id]; }) ? ' checked' : '') + '> All</label><span class="st-note" style="margin:0">' + selN + ' selected</span>';
    if (selN) {
      h += '<button type="button" class="btn" data-a="bulk" data-v="hidden">Hide</button><button type="button" class="btn" data-a="bulk" data-v="published">Publish</button>' +
        '<select class="st-in" style="width:auto" id="bulk-stock" aria-label="Set stock"><option value="">Set stock...</option>' + Object.keys(STOCK).map(function (k) { return '<option value="s:' + k + '">' + STOCK[k] + '</option>'; }).join('') + '</select>' +
        '<button type="button" class="btn danger" data-a="bulk" data-v="delete">Delete</button>';
    }
    h += '</div><div class="st-rows">' + list.slice(0, S.shown).map(rowHTML).join('') + '</div>';
    if (n > S.shown) h += '<button type="button" class="btn full" style="margin-top:12px" data-a="more">Show more (' + (n - S.shown) + ')</button>';
    el.innerHTML = h; hydrate();
  }
  function rowHTML(p) {
    var hid = (p.status || 'published') === 'hidden';
    var ph = p.photos && p.photos.length ? photoImg(p.photos[0]) : 'No photo';
    return '<div class="st-row' + (hid ? ' is-hidden' : '') + '"><label class="st-chk"><input type="checkbox" data-a="sel" data-id="' + esc(p.id) + '"' + (S.sel[p.id] ? ' checked' : '') + ' aria-label="Select"></label>' +
      '<button type="button" class="st-rowmain" data-a="edit" data-id="' + esc(p.id) + '"><span class="st-rowthumb">' + ph + '</span><span class="st-rowtxt"><b>' + esc(partName(p)) + (p.side ? ' (' + esc(SIDES[p.side] || p.side) + ')' : '') + '</b><small>' + esc(carLabel(p.m)) + '</small>' +
      '<span>' + (hid ? '<i class="st-badge b-hidden">Hidden</i>' : '') + (p.stock ? '<i class="st-badge s-' + esc(p.stock) + '">' + esc(STOCK[p.stock] || p.stock) + '</i>' : '') + '</span></span><span class="st-price">' + esc(money(p.price)) + '</span></button></div>';
  }

  /* ---------- Edit sheet ---------- */
  function openEdit(id) {
    var p = PM[id]; if (!p) return;
    E = { rec: p, err: '', saving: false, d: {
      m: p.m, p: p.p, pn: p.pn || '', pc: p.pc || '', price: p.price == null ? '' : String(p.price), oem: p.oem || '', stock: p.stock || '', side: p.side || '', note: p.note || '', status: p.status || 'published',
      photos: (p.photos || []).map(function (v) { return { id: uid(), val: v, prev: null, state: 'ok', pct: 0 }; }) } };
    renderSheet(); document.body.classList.add('st-lock');
  }
  function closeSheet() {
    var m = document.getElementById('sheet'); if (m) m.remove();
    document.body.classList.remove('st-lock'); E = null;
  }
  function renderSheet() {
    var d = E.d, p = E.rec, pd = PA[d.p];
    var old = document.getElementById('sheet'), st = old ? old.querySelector('.st-sheet').scrollTop : 0;
    var h = '<div class="st-modal" id="sheet" role="dialog" aria-modal="true"><div class="st-sheet"><div class="st-sheet-h"><div><h2 class="st-h2" style="margin:0">' + esc(pd ? pd.name : (d.pn || 'Other part')) + '</h2><div class="st-note" style="margin:0">' + esc(carLabel(d.m)) + '</div></div><button type="button" class="st-x" data-a="closesheet" aria-label="Close">&times;</button></div>';
    h += '<label class="st-lbl" for="e-m">Car</label><select class="st-in" id="e-m" data-c="e" data-f="m">' + cars.map(function (c) { return '<option value="' + esc(c.key) + '"' + (d.m === c.key ? ' selected' : '') + '>' + esc(carLabel(c.key)) + '</option>'; }).join('') + (CM[d.m] ? '' : '<option value="' + esc(d.m) + '" selected>' + esc(d.m) + '</option>') + '</select>';
    if (d.p === 'other') {
      h += '<label class="st-lbl" for="e-pn">Part name</label><input class="st-in" id="e-pn" data-c="e" data-f="pn" value="' + esc(d.pn) + '"><label class="st-lbl" for="e-pc">Category</label><select class="st-in" id="e-pc" data-c="e" data-f="pc">' + D.cats.map(function (c) { return '<option value="' + esc(c.id) + '"' + (d.pc === c.id ? ' selected' : '') + '>' + esc(c.name) + '</option>'; }).join('') + '</select>';
    }
    if ((pd && pd.side) || d.p === 'other' || d.side) h += '<label class="st-lbl">Side</label>' + pillsHTML([['', 'Not needed'], ['L', 'Left'], ['R', 'Right'], ['pair', 'Pair']], d.side, 'side', 'e');
    h += '<label class="st-lbl" for="e-price">Price in S$ (empty = Ask for price)</label><input class="st-in" id="e-price" inputmode="decimal" data-c="e" data-f="price" value="' + esc(d.price) + '">' +
      '<label class="st-lbl">Stock</label>' + pillsHTML(Object.keys(STOCK).map(function (k) { return [k, STOCK[k]]; }), d.stock, 'stock', 'e') +
      '<label class="st-lbl" for="e-oem">OEM part number</label><input class="st-in" id="e-oem" data-c="e" data-f="oem" value="' + esc(d.oem) + '" autocapitalize="characters">' +
      '<label class="st-lbl" for="e-note">Note</label><textarea class="st-in" id="e-note" data-c="e" data-f="note" rows="2">' + esc(d.note) + '</textarea><p class="st-warn">The note is visible to customers on the website.</p>' +
      '<label class="st-lbl">Photos</label><div id="ph-e">' + photosHTML('e') + '</div>' +
      '<label class="st-lbl">Status</label>' + pillsHTML([['published', 'Published'], ['hidden', 'Hidden']], d.status, 'status', 'e') +
      '<p class="st-err" id="e-err">' + esc(E.err) + '</p><div class="btns"><button type="button" class="btn primary" style="flex:1 1 140px;min-height:52px" id="e-save" data-a="esave">' + (E.saving ? 'Saving...' : 'Save changes') + '</button><button type="button" class="btn danger" data-a="edel">Delete</button></div>' +
      '<p class="st-hint">Key: ' + esc(p.key) + '</p></div></div>';
    if (old) old.remove();
    document.body.insertAdjacentHTML('beforeend', h);
    document.querySelector('#sheet .st-sheet').scrollTop = st;
    hydrate();
  }
  function editSave() {
    if (E.saving) return;
    var d = E.d, p = E.rec;
    var err = validateDraft(d, true);
    if (!err && photosBusy(d)) err = 'Photos are still uploading. Wait a moment.';
    if (!err && photosBad(d)) err = 'A photo failed. Tap it to retry, or remove it.' + photoErr(d);
    if (err) { E.err = err; setText('e-err', err); return; }
    var next = recordFrom(d, p.key, d.status), patch = {};
    ['m', 'pn', 'pc', 'oem', 'stock', 'side', 'note', 'status'].forEach(function (k) {
      if (d.p !== 'other' && (k === 'pn' || k === 'pc')) return;
      if ((next[k] || '') !== (p[k] || '')) patch[k] = next[k] === undefined ? '' : next[k];
    });
    if (JSON.stringify(next.photos) !== JSON.stringify(p.photos || [])) patch.photos = next.photos;
    var np = next.price === undefined ? null : next.price, op = p.price == null || p.price === '' ? null : Number(p.price);
    if (np !== op) patch.price = np;
    if (!Object.keys(patch).length) { toast('Nothing changed'); return closeSheet(); }
    E.saving = true; setText('e-err', ''); setText('e-save', 'Saving...');
    api('PUT', '/entities/AtProduct/' + encodeURIComponent(p.id), patch).then(function (r) {
      Object.assign(p, patch, r && r.id ? r : {}); reindex();
      logAct('Edited ' + carLabel(p.m) + ' ' + partName(p) + ' (' + Object.keys(patch).join(', ') + ')');
      toast('Saved. Live on the website now.'); closeSheet(); renderView();
    }).catch(function (e) {
      E.saving = false; E.err = 'Not saved: ' + e.message; setText('e-err', E.err); setText('e-save', 'Save changes');
    });
  }
  function editDelete() {
    var p = E.rec;
    if (!window.confirm('Delete ' + partName(p) + ' for ' + carLabel(p.m) + '? This cannot be undone.')) return;
    api('DELETE', '/entities/AtProduct/' + encodeURIComponent(p.id)).then(function () {
      products = products.filter(function (x) { return x.id !== p.id; }); reindex(); delete S.sel[p.id];
      logAct('Deleted ' + carLabel(p.m) + ' ' + partName(p) + ' (' + p.key + ')');
      toast('Deleted'); closeSheet(); renderView();
    }).catch(function (e) { E.err = 'Not deleted: ' + e.message; setText('e-err', E.err); });
  }

  /* ---------- Bulk ---------- */
  function bulk(action) {
    var ids = Object.keys(S.sel).filter(function (id) { return PM[id]; });
    if (!ids.length) return;
    var patch, label;
    if (action === 'delete') {
      if (!window.confirm('Delete ' + ids.length + ' products? This cannot be undone.')) return;
      label = 'Deleted';
    } else if (action.indexOf('s:') === 0) { patch = { stock: action.slice(2) }; label = 'Set stock to "' + (STOCK[patch.stock] || 'Not set') + '" on'; }
    else { patch = { status: action }; label = action === 'hidden' ? 'Hid' : 'Published'; }
    toast('Working on ' + ids.length + '...', 8000);
    runPool(ids, 4, function (id) {
      var p = PM[id];
      if (action === 'delete') return api('DELETE', '/entities/AtProduct/' + encodeURIComponent(id)).then(function () { products = products.filter(function (x) { return x.id !== id; }); });
      return api('PUT', '/entities/AtProduct/' + encodeURIComponent(id), patch).then(function () { Object.assign(p, patch); });
    }).then(function (r) {
      reindex(); S.sel = {};
      logAct(label + ' ' + r.ok + ' products' + (r.fail ? ' (' + r.fail + ' failed)' : ''));
      toast(r.fail ? r.ok + ' done, ' + r.fail + ' failed: ' + r.errs[0] : label + ' ' + r.ok + ' products.', 4000);
      renderView();
    });
  }

  /* ---------- Cars ---------- */
  var carUi = { open: false, brand: 'hyundai', c: { name: '', code: '', years: '', fuel: 'petrol' }, edit: null };
  function carsHTML() {
    var h = '<div class="btns"><button type="button" class="btn primary full" style="min-height:52px" data-a="newcar">+ Add a car</button></div>';
    if (carUi.open) {
      h += '<div class="st-mini"><b>Add a car</b><label class="st-lbl">Brand</label>' + pillsHTML(D.brands.map(function (b) { return [b.id, b.name]; }), carUi.brand, 'cbrand', 'cu') +
        '<label class="st-lbl" for="cu-name">Car name</label><input class="st-in" id="cu-name" data-f="cu.name" value="' + esc(carUi.c.name) + '" placeholder="e.g. Avante" autocomplete="off">' +
        '<div class="st-2col"><div><label class="st-lbl" for="cu-code">Generation code</label><input class="st-in" id="cu-code" data-f="cu.code" value="' + esc(carUi.c.code) + '" autocomplete="off"></div><div><label class="st-lbl" for="cu-years">Years</label><input class="st-in" id="cu-years" data-f="cu.years" value="' + esc(carUi.c.years) + '" placeholder="2020-now" autocomplete="off"></div></div>' +
        '<label class="st-lbl" for="cu-fuel">Fuel</label><select class="st-in" id="cu-fuel" data-f="cu.fuel">' + FUELS.map(function (f) { return '<option' + (carUi.c.fuel === f ? ' selected' : '') + '>' + f + '</option>'; }).join('') + '</select>' +
        '<p class="st-err" id="cu-err"></p><div class="btns"><button type="button" class="btn primary" data-a="cusave">Save car</button><button type="button" class="btn" data-a="cucancel">Cancel</button></div></div>';
    }
    D.brands.forEach(function (b) {
      var cl = cars.filter(function (c) { return c.b === b.id; }).sort(function (x, y) { return carShort(x).localeCompare(carShort(y)); });
      h += '<h2 class="st-h2" style="margin-top:18px">' + esc(b.name) + ' (' + cl.length + ')</h2><div class="st-rows">' + cl.map(function (c) {
        var n = products.filter(function (p) { return p.m === c.key; }).length, hid = c.status === 'hidden';
        return '<div class="st-row' + (hid ? ' is-hidden' : '') + '"><div class="st-rowmain" style="cursor:default"><span class="st-rowtxt"><b>' + esc(carShort(c)) + '</b><small>' + esc([c.years, c.fuel].filter(Boolean).join(' · ')) + ' · ' + n + ' products</small>' + (hid ? '<i class="st-badge b-hidden">Hidden</i>' : '') + '</span>' +
          '<button type="button" class="btn" data-a="cartoggle" data-id="' + esc(c.id) + '">' + (hid ? 'Show' : 'Hide') + '</button><button type="button" class="btn" data-a="caredit" data-id="' + esc(c.id) + '">Edit</button></div></div>';
      }).join('') + (cl.length ? '' : '<div class="st-empty">No cars yet.</div>') + '</div>';
    });
    return h;
  }
  function openCarEdit(id, keepD) {
    var c = cars.filter(function (x) { return x.id === id; })[0]; if (!c) return;
    carUi.edit = { rec: c, d: { name: c.name || '', code: c.code || '', years: c.years || '', fuel: c.fuel || 'petrol', alias: (c.alias || []).join(', '), status: c.status || 'published' } };
    if (keepD) carUi.edit.d = keepD;
    var d = carUi.edit.d;
    var h = '<div class="st-modal" id="sheet" role="dialog" aria-modal="true"><div class="st-sheet"><div class="st-sheet-h"><h2 class="st-h2" style="margin:0">Edit car</h2><button type="button" class="st-x" data-a="closesheet" aria-label="Close">&times;</button></div>' +
      '<label class="st-lbl" for="ce-name">Name</label><input class="st-in" id="ce-name" data-f="ce.name" value="' + esc(d.name) + '">' +
      '<div class="st-2col"><div><label class="st-lbl" for="ce-code">Code</label><input class="st-in" id="ce-code" data-f="ce.code" value="' + esc(d.code) + '"></div><div><label class="st-lbl" for="ce-years">Years</label><input class="st-in" id="ce-years" data-f="ce.years" value="' + esc(d.years) + '"></div></div>' +
      '<label class="st-lbl" for="ce-fuel">Fuel</label><input class="st-in" id="ce-fuel" data-f="ce.fuel" value="' + esc(d.fuel) + '">' +
      '<label class="st-lbl" for="ce-alias">Other names owners type (comma separated)</label><input class="st-in" id="ce-alias" data-f="ce.alias" value="' + esc(d.alias) + '">' +
      '<label class="st-lbl">Status</label>' + pillsHTML([['published', 'Published'], ['hidden', 'Hidden']], d.status, 'cestatus', 'ce') +
      '<p class="st-err" id="ce-err"></p><div class="btns"><button type="button" class="btn primary" style="flex:1 1 140px" data-a="cesave">Save changes</button></div></div></div>';
    document.body.insertAdjacentHTML('beforeend', h); document.body.classList.add('st-lock');
  }
  function carEditSave() {
    var c = carUi.edit.rec, d = carUi.edit.d;
    if (!d.name.trim()) return setText('ce-err', 'Name is required.');
    var patch = { name: d.name.trim(), code: d.code.trim(), years: d.years.trim(), fuel: d.fuel.trim(), status: d.status, alias: d.alias.split(',').map(function (s) { return s.trim(); }).filter(Boolean) };
    api('PUT', '/entities/AtCar/' + encodeURIComponent(c.id), patch).then(function () {
      Object.assign(c, patch); reindex(); logAct('Edited car ' + carLabel(c.key)); closeSheet(); carUi.edit = null; toast('Car saved'); renderView();
    }).catch(function (e) { setText('ce-err', 'Not saved: ' + e.message); });
  }

  /* ---------- CSV import / export ---------- */
  var CSV_COLS = ['key', 'brand', 'car key', 'car name', 'part', 'price', 'oem', 'stock', 'side', 'status', 'note', 'photos', 'category'];
  function csvCell(v) { v = String(v == null ? '' : v); return /[",\n\r]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
  function toCSV(rows) { return rows.map(function (r) { return r.map(csvCell).join(','); }).join('\r\n') + '\r\n'; }
  function parseCSV(t) {
    t = String(t).replace(/^﻿/, '');
    var rows = [], row = [], cell = '', q = false, i, c;
    for (i = 0; i < t.length; i++) {
      c = t[i];
      if (q) { if (c === '"') { if (t[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += c; }
      else if (c === '"') q = true;
      else if (c === ',') { row.push(cell); cell = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && t[i + 1] === '\n') i++; row.push(cell); cell = ''; rows.push(row); row = []; }
      else cell += c;
    }
    if (cell !== '' || row.length) { row.push(cell); rows.push(row); }
    return rows.filter(function (r) { return r.some(function (x) { return x.trim() !== ''; }); });
  }
  function download(name, text, type) {
    var b = new Blob([text], { type: type || 'text/csv;charset=utf-8' }), a = document.createElement('a');
    a.href = URL.createObjectURL(b); a.download = name; document.body.appendChild(a); a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }
  function exportCSV() {
    var rows = [CSV_COLS].concat(products.map(function (p) {
      var c = CM[p.m] || {};
      return [p.key, c.b || '', p.m, c.name ? carShort(c) : '', PA[p.p] ? p.p : (p.pn || ''), p.price == null ? '' : p.price, p.oem || '', p.stock || '', p.side || '', p.status || 'published', p.note || '', (p.photos || []).join('|'), PA[p.p] ? '' : (p.pc || '')];
    }));
    download('autotex-products-' + new Date().toISOString().slice(0, 10) + '.csv', toCSV(rows));
    toast('Exported ' + products.length + ' products');
  }
  function templateCSV() {
    var ex = cars[0] || { b: 'hyundai', key: 'avante-cn7', name: 'Avante', code: 'CN7' };
    download('autotex-template.csv', toCSV([CSV_COLS, ['', ex.b, ex.key, '', 'front-bumper', '180', '86511-AA000', 'in', '', 'published', '', '', '']]));
  }
  function ioHTML() {
    var h = '<div class="st-card"><h2 class="st-h2">Export</h2><p class="st-note">Download every product as a CSV file you can open in Excel or Google Sheets.</p><button type="button" class="btn full" data-a="export">Export ' + products.length + ' products (CSV)</button></div>' +
      '<div class="st-card"><h2 class="st-h2">Import</h2><p class="st-note">Rows are matched by the <b>key</b> column. A matching key updates that product; an empty or new key creates one.</p>' +
      '<div class="btns"><button type="button" class="btn" data-a="template">Download CSV template</button></div>' +
      '<label class="st-lbl" for="imp-file">Choose a CSV file</label><input class="st-in" id="imp-file" type="file" accept=".csv,text/csv">' +
      '<div id="imp-out">' + importHTML() + '</div></div>';
    return h;
  }
  function prepareImport(text) {
    var rows = parseCSV(text);
    if (rows.length < 2) return { err: 'No data rows found in this file.' };
    var head = rows[0].map(function (x) { return x.trim().toLowerCase(); });
    function col(n) { return head.indexOf(n); }
    if (col('car key') < 0 || col('part') < 0) return { err: 'The file needs at least the columns "car key" and "part". Use the template.' };
    var seen = {}, out = [];
    rows.slice(1).forEach(function (r, idx) {
      function g(n) { var i = col(n); return i < 0 ? undefined : (r[i] || '').trim(); }
      var o = { line: idx + 2, action: 'skip', why: '' };
      var m = g('car key'), part = g('part'), cat = g('category');
      if (!CM[m]) { o.why = 'Unknown car key "' + m + '"'; return out.push(o); }
      var pd = PA[part] || D.parts.filter(function (p) { return p.name.toLowerCase() === (part || '').toLowerCase(); })[0];
      var d = { m: m, p: pd ? pd.id : 'other', pn: pd ? '' : part, pc: pd ? '' : (cat && CA[cat] ? cat : (D.cats.filter(function (c) { return c.name.toLowerCase() === (cat || '').toLowerCase(); })[0] || {}).id || '') };
      if (!part) { o.why = 'Part is empty'; return out.push(o); }
      if (!pd && !d.pc) { o.why = 'Custom part needs a valid "category"'; return out.push(o); }
      var price = parsePrice(g('price'));
      if (price !== null && isNaN(price)) { o.why = 'Bad price'; return out.push(o); }
      var stock = g('stock') || '', side = g('side') || '', status = (g('status') || 'published').toLowerCase();
      if (['', 'in', 'order', 'out'].indexOf(stock) < 0) { o.why = 'Bad stock "' + stock + '"'; return out.push(o); }
      if (['', 'L', 'R', 'pair'].indexOf(side) < 0) { o.why = 'Bad side "' + side + '"'; return out.push(o); }
      if (['published', 'hidden'].indexOf(status) < 0) { o.why = 'Bad status "' + status + '"'; return out.push(o); }
      var photosStr = g('photos');
      d.price = price === null ? '' : String(price); d.oem = g('oem') || ''; d.stock = stock; d.side = side; d.note = g('note') || '';
      d.photos = photosStr ? photosStr.split('|').map(function (s) { return s.trim(); }).filter(Boolean).slice(0, MAXPH) : [];
      var key = g('key'), existing = key ? products.filter(function (p) { return p.key === key; })[0] : null;
      if (key && seen[key]) { o.why = 'Duplicate key in file'; return out.push(o); }
      if (key) seen[key] = 1;
      o.d = d; o.status = status; o.part = pd ? pd.name : part; o.price = price;
      if (existing) {
        var rec = recordFrom(d, key, status), patch = {};
        ['m', 'p', 'pn', 'pc', 'oem', 'stock', 'side', 'note', 'status'].forEach(function (k) { if (rec[k] !== undefined && (rec[k] || '') !== (existing[k] || '')) patch[k] = rec[k]; });
        if (JSON.stringify(rec.photos) !== JSON.stringify(existing.photos || [])) patch.photos = rec.photos;
        var ep = existing.price == null ? null : Number(existing.price);
        if ((rec.price === undefined ? null : rec.price) !== ep) patch.price = rec.price === undefined ? null : rec.price;
        o.key = key; o.id = existing.id; o.patch = patch;
        o.action = Object.keys(patch).length ? 'update' : 'same';
      } else { o.key = key; o.action = 'create'; }
      out.push(o);
    });
    return { rows: out };
  }
  function importHTML() {
    var s = importState; if (!s) return '';
    if (s.err) return '<p class="st-err">' + esc(s.err) + '</p>';
    var c = s.rows.filter(function (r) { return r.action === 'create'; }).length, u = s.rows.filter(function (r) { return r.action === 'update'; }).length, sk = s.rows.filter(function (r) { return r.action === 'skip'; }).length, same = s.rows.filter(function (r) { return r.action === 'same'; }).length;
    var h = '<p class="st-note"><b>' + c + '</b> to create, <b>' + u + '</b> to update, ' + same + ' unchanged, ' + sk + ' skipped.</p><div class="st-tablewrap"><table class="st-table"><thead><tr><th>Row</th><th>Action</th><th>Car</th><th>Part</th><th>Price</th><th>Note</th></tr></thead><tbody>' +
      s.rows.slice(0, 200).map(function (r) {
        return '<tr><td>' + r.line + '</td><td>' + esc(r.action) + '</td><td>' + esc(r.d ? carLabel(r.d.m) : '') + '</td><td>' + esc(r.part || '') + '</td><td>' + esc(r.price == null ? '' : r.price) + '</td><td>' + esc(r.why) + '</td></tr>';
      }).join('') + '</tbody></table></div>' + (s.rows.length > 200 ? '<p class="st-hint">Showing the first 200 rows.</p>' : '') +
      (s.busy ? '<p class="st-note">' + esc(s.busy) + '</p>' : '') + '<p class="st-err" id="imp-err">' + esc(s.msg || '') + '</p>';
    if (c + u) h += '<button type="button" class="btn primary full" data-a="doimport"' + (s.busy ? ' disabled' : '') + '>Create ' + c + ' / update ' + u + ' rows</button>';
    return h;
  }
  function doImport() {
    var s = importState; if (!s || s.busy) return;
    var creates = s.rows.filter(function (r) { return r.action === 'create'; }), updates = s.rows.filter(function (r) { return r.action === 'update'; });
    s.busy = 'Importing...'; refreshImport();
    var taken = {}; products.forEach(function (p) { taken[p.key] = 1; });
    var recs = creates.map(function (r) {
      var c = CM[r.d.m], base = r.key || (c.b + '-' + c.key + '-' + (r.d.p === 'other' ? slug(r.d.pn) : r.d.p)), k = base, n = 2;
      while (taken[k]) { k = base + '-' + n; n++; }
      taken[k] = 1;
      return recordFrom(r.d, k, r.status);
    });
    var failed = 0, firstErr = '';
    var chunks = []; for (var i = 0; i < recs.length; i += 50) chunks.push(recs.slice(i, i + 50));
    var p = Promise.resolve();
    chunks.forEach(function (ch) {
      p = p.then(function () {
        return api('POST', '/entities/AtProduct/bulk', ch).catch(function (e) {
          if (!token) throw e;
          return runPool(ch, 3, function (rec) { return api('POST', '/entities/AtProduct', rec); }).then(function (r) { failed += r.fail; if (r.fail) firstErr = r.errs[0]; });
        });
      });
    });
    p.then(function () {
      return runPool(updates, 4, function (r) { return api('PUT', '/entities/AtProduct/' + encodeURIComponent(r.id), r.patch); });
    }).then(function (r) {
      failed += r.fail; if (r.fail) firstErr = r.errs[0];
      logAct('CSV import: ' + recs.length + ' created, ' + updates.length + ' updated' + (failed ? ', ' + failed + ' failed' : ''));
      return listAll('AtProduct', '-updated_date');
    }).then(function (list) {
      products = list; reindex();
      importState = { rows: [], msg: '' };
      importState = null;
      toast(failed ? 'Import done with ' + failed + ' failures: ' + firstErr : 'Import finished', 5000);
      renderView();
    }).catch(function (e) { s.busy = ''; s.msg = 'Import stopped: ' + e.message; refreshImport(); });
  }
  function refreshImport() { var el = document.getElementById('imp-out'); if (el) el.innerHTML = importHTML(); }

  /* ---------- Activity ---------- */
  function loadLogs() {
    api('GET', '/entities/AtLog?limit=100&sort=' + encodeURIComponent('-created_date')).then(function (r) {
      logs = Array.isArray(r) ? r : []; if (S.tab === 'log') renderView();
    }).catch(function (e) { logs = { err: e.message }; if (S.tab === 'log') renderView(); });
  }
  function logHTML() {
    var h = '<div class="btns"><button type="button" class="btn" data-a="reloadlog">Refresh</button></div>';
    if (!logs) return h + '<p class="st-note">Loading...</p>';
    if (logs.err) return h + '<p class="st-err">' + esc(logs.err) + '</p>';
    if (!logs.length) return h + '<div class="st-empty">No activity yet.</div>';
    return h + '<ul class="st-log">' + logs.map(function (l) {
      var t = l.created_date ? new Date(l.created_date) : null;
      return '<li><b>' + esc(l.what) + '</b><small>' + esc(l.who || '') + (t && !isNaN(t) ? ' · ' + esc(t.toLocaleString('en-SG')) : '') + '</small></li>';
    }).join('') + '</ul>';
  }

  /* ---------- events ---------- */
  function setPath(obj, path, v) { var p = path.split('.'); if (p.length === 2) obj[p[0]][p[1]] = v; }
  function ctxByName(c) {
    return c === 'q' ? Q : c === 'e' ? (E && E.d) : c === 'cu' ? carUi.c : c === 'ce' ? (carUi.edit && carUi.edit.d) : null;
  }
  function setField(c, f, v) {
    if (c === 'q') {
      if (f === 'brand') { if (Q.brand !== v) { Q.brand = v; Q.car = ''; Q.part = ''; Q.addCar = false; } }
      else if (f === 'car') { Q.car = v; Q.done = null; }
      else if (f === 'part') { Q.part = v; Q.err = ''; if (v !== 'other') { Q.pn = ''; Q.pc = ''; } var pd = PA[v]; if (pd && !pd.side) Q.side = ''; }
      else Q[f] = v;
      renderView();
    } else if (c === 'e') {
      E.d[f] = v; if (f === 'part') return; renderSheet();
    } else if (c === 'cu') { carUi.brand = v; renderView(); }
    else if (c === 'ce') { carUi.edit.d.status = v; var s = document.getElementById('sheet'); if (s) { s.remove(); var keep = carUi.edit; openCarEdit(keep.rec.id, keep.d); } }
  }
  document.addEventListener('click', function (ev) {
    var t = ev.target.closest ? ev.target.closest('[data-a]') : null; if (!t) return;
    var a = t.getAttribute('data-a'), v = t.getAttribute('data-v'), id = t.getAttribute('data-id');
    if (a === 'selall' || a === 'sel') return; // handled on change
    switch (a) {
      case 'signin': if (window.__atLogin) window.__atLogin(); else location.href = '/login?from_url=' + encodeURIComponent(location.href); break;
      case 'signout': lsDel(TOKEN_KEY); lsDel('token'); token = ''; location.reload(); break;
      case 'reload': boot(); break;
      case 'tab': setTab(v); break;
      case 'set': { var c = t.getAttribute('data-c'), f = t.getAttribute('data-f'); if (f === 'cbrand') f = 'brand'; if (f === 'cestatus') f = 'status'; setField(c, f, v); break; }
      case 'addcar': Q.addCar = !Q.addCar; renderView(); if (Q.addCar) { var el = document.getElementById('ac-name'); if (el) el.focus(); } break;
      case 'cancelcar': Q.addCar = false; renderView(); break;
      case 'savecar': saveCarFromForm(); break;
      case 'qsave': quickSave(); break;
      case 'another': Q.done = null; renderView(); window.scrollTo(0, 0); break;
      case 'anothercar': Q.done = null; Q.car = ''; Q.brand = ''; renderView(); window.scrollTo(0, 0); break;
      case 'rmph': { var ctx = ctxOf(t.getAttribute('data-c')); ctx.photos = ctx.photos.filter(function (p) { return p.id !== t.getAttribute('data-i'); }); refreshPhotos(t.getAttribute('data-c')); break; }
      case 'mvph': { var nm = t.getAttribute('data-c'), cx = ctxOf(nm), ix = cx.photos.findIndex(function (p) { return p.id === t.getAttribute('data-i'); }); if (ix > 0) { var x = cx.photos.splice(ix, 1)[0]; cx.photos.splice(ix - 1, 0, x); refreshPhotos(nm); } break; }
      case 'retry': { var nm2 = t.getAttribute('data-c'), it = ctxOf(nm2).photos.filter(function (p) { return p.id === t.getAttribute('data-i'); })[0]; if (it) { processPhoto(nm2, it); refreshPhotos(nm2); } break; }
      case 'flag': S.F[v] = !S.F[v]; S.shown = PAGE; renderView(); break;
      case 'more': S.shown += PAGE; renderList(); break;
      case 'edit': openEdit(id); break;
      case 'closesheet': closeSheet(); break;
      case 'esave': editSave(); break;
      case 'edel': editDelete(); break;
      case 'bulk': bulk(v); break;
      case 'newcar': carUi.open = !carUi.open; renderView(); break;
      case 'cucancel': carUi.open = false; renderView(); break;
      case 'cusave': {
        var cc = carUi.c; if (!cc.name.trim()) return setText('cu-err', 'Type the car name.');
        createCar(carUi.brand, cc).then(function () { carUi.open = false; carUi.c = { name: '', code: '', years: '', fuel: 'petrol' }; toast('Car added'); renderView(); }).catch(function (e) { setText('cu-err', 'Could not save: ' + e.message); });
        break;
      }
      case 'cartoggle': {
        var car = cars.filter(function (x) { return x.id === id; })[0]; if (!car) break;
        var ns = car.status === 'hidden' ? 'published' : 'hidden';
        api('PUT', '/entities/AtCar/' + encodeURIComponent(id), { status: ns }).then(function () { car.status = ns; logAct((ns === 'hidden' ? 'Hid' : 'Showed') + ' car ' + carLabel(car.key)); renderView(); }).catch(function (e) { toast('Failed: ' + e.message); });
        break;
      }
      case 'caredit': openCarEdit(id); break;
      case 'cesave': carEditSave(); break;
      case 'export': exportCSV(); break;
      case 'template': templateCSV(); break;
      case 'doimport': doImport(); break;
      case 'reloadlog': logs = null; renderView(); loadLogs(); break;
    }
  });
  document.addEventListener('input', function (ev) {
    var t = ev.target;
    if (t.getAttribute && t.getAttribute('data-flt')) {
      S.F[t.getAttribute('data-flt')] = t.value; S.shown = PAGE;
      if (t.getAttribute('data-flt') === 'brand') { S.F.car = ''; return renderView(); }
      return renderList();
    }
    var f = t.getAttribute && t.getAttribute('data-f'); if (!f) return;
    var c = t.getAttribute('data-c');
    if (f.indexOf('.') > 0) {
      var p = f.split('.'), o = ctxByName(p[0] === 'ac' ? 'q' : p[0]);
      if (p[0] === 'ac') Q.ac[p[1]] = t.value; else if (o) o[p[1]] = t.value;
      return;
    }
    if (c === 'e') { E.d[f] = t.value; return; }
    Q[f] = t.value;
    if (f === 'psearch') { var pe = document.getElementById('parts-q'); if (pe) pe.innerHTML = partPickerHTML('q', Q.part, Q.psearch); }
    if (f === 'price' || f === 'pn') setHtml('q-sum', quickSummary());
  });
  function setHtml(id, h) { var el = document.getElementById(id); if (el) el.innerHTML = h; }
  document.addEventListener('change', function (ev) {
    var t = ev.target, a = t.getAttribute && t.getAttribute('data-a');
    if (t.getAttribute && t.getAttribute('data-ph')) { var nm = t.getAttribute('data-ph'); addPhotos(nm, t.files); t.value = ''; return; }
    if (a === 'sel') { if (t.checked) S.sel[t.getAttribute('data-id')] = 1; else delete S.sel[t.getAttribute('data-id')]; return renderList(); }
    if (a === 'selall') { filtered().forEach(function (p) { if (t.checked) S.sel[p.id] = 1; else delete S.sel[p.id]; }); return renderList(); }
    if (t.id === 'bulk-stock' && t.value) { var val = t.value; t.value = ''; return bulk(val); }
    if (t.id === 'imp-file') {
      var f = t.files && t.files[0]; if (!f) return;
      var r = new FileReader();
      r.onload = function () { importState = prepareImport(String(r.result)); refreshImport(); };
      r.readAsText(f); return;
    }
    if (t.tagName === 'SELECT' && t.getAttribute('data-flt')) return; // handled by input
    if (t.tagName === 'SELECT' && t.getAttribute('data-c') === 'e') { E.d[t.getAttribute('data-f')] = t.value; renderSheet(); }
    else if (t.tagName === 'SELECT' && t.id === 'q-pc') Q.pc = t.value;
  });

  boot();
})();
