/* Autotex staff catalogue dashboard (demo). Vanilla ES2018, no dependencies. */
(function () {
  'use strict';
  var AT = window.AT || { brands: [], models: [], cats: [], parts: [], products: [] };
  var root = document.getElementById('staff-app');
  if (!root) return;
  var KEY = 'at_catalog_v1', AKEY = 'at_audit_v1', SKEY = 'at_staff', PIN = '1995', PAGE = 50;
  var STOCK = { '': 'Unknown', 'in': 'In stock', 'order': 'Order from Korea', 'out': 'Out of stock' };
  var mem = { ov: null, audit: null, who: null };

  /* ---------- helpers ---------- */
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function money(n) {
    if (n == null || n === '' || isNaN(n)) return 'Ask for price';
    n = Number(n);
    var s = (Math.round(n * 100) % 100 === 0) ? String(Math.round(n)) : n.toFixed(2);
    var p = s.split('.');
    p[0] = p[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return 'S$' + p.join('.');
  }
  function lsGet(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function lsSet(k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function byId(list) { var o = {}; list.forEach(function (x) { o[x.id] = x; }); return o; }
  function $(sel, el) { return (el || root).querySelector(sel); }
  var BR = byId(AT.brands || []), MO = byId(AT.models || []), CA = byId(AT.cats || []), PA = byId(AT.parts || []);

  function loadOv() {
    if (mem.ov) return mem.ov;
    var o = null;
    try { o = JSON.parse(lsGet(KEY) || 'null'); } catch (e) { o = null; }
    if (!o || typeof o !== 'object') o = {};
    if (!o.products || typeof o.products !== 'object') o.products = {};
    if (!Array.isArray(o.added)) o.added = [];
    mem.ov = o;
    return o;
  }
  function saveOv() {
    var o = loadOv();
    o.updated = new Date().toISOString();
    lsSet(KEY, JSON.stringify(o));
  }
  function loadAudit() {
    if (mem.audit) return mem.audit;
    var a = null;
    try { a = JSON.parse(lsGet(AKEY) || '[]'); } catch (e) { a = []; }
    mem.audit = Array.isArray(a) ? a : [];
    return mem.audit;
  }
  function who() {
    var w = null;
    try { w = sessionStorage.getItem(SKEY); } catch (e) { w = mem.who; }
    return w || mem.who || '';
  }
  function log(what) {
    var a = loadAudit();
    a.push({ t: new Date().toISOString(), who: who() || 'unknown', what: what });
    if (a.length > 300) a.splice(0, a.length - 300);
    lsSet(AKEY, JSON.stringify(a));
  }

  /* ---------- merged catalogue ---------- */
  var FIELDS = ['price', 'sample', 'oem', 'stock', 'status', 'note'];
  function baseList() { return (AT.products || []).concat(loadOv().added); }
  function baseOf(id) {
    var i, p = AT.products || [];
    for (i = 0; i < p.length; i++) if (p[i].id === id) return p[i];
    var ad = loadOv().added;
    for (i = 0; i < ad.length; i++) if (ad[i].id === id) return ad[i];
    return null;
  }
  function merge(b) {
    var o = loadOv().products[b.id], m = {}, k;
    for (k in b) m[k] = b[k];
    if (o) for (k in o) m[k] = o[k];
    if (m.price === undefined) m.price = null;
    return m;
  }
  function partOf(p) {
    var pt = PA[p.p];
    if (pt) return { name: pt.name, cat: pt.cat, alias: pt.alias || [] };
    return { name: p.pn || 'Custom part', cat: p.pc || '', alias: [] };
  }
  function modelLabel(p) {
    var m = MO[p.m]; if (!m) return p.m || '';
    var b = BR[m.b];
    return (b ? b.name + ' ' : '') + m.name + (m.code ? ' (' + m.code + ')' : '');
  }
  function isEdited(id) {
    var o = loadOv().products[id];
    if (o && Object.keys(o).length) return true;
    return loadOv().added.some(function (a) { return a.id === id; });
  }
  function allMerged() {
    return baseList().map(function (b) {
      var m = merge(b);
      m._part = partOf(m);
      m._label = modelLabel(m);
      m._b = MO[m.m] ? MO[m.m].b : '';
      return m;
    });
  }
  function sortList(l) {
    l.sort(function (a, b) {
      return a._label.localeCompare(b._label) || a._part.name.localeCompare(b._part.name);
    });
    return l;
  }
  function haystack(m) {
    var mo = MO[m.m] || {}, br = BR[mo.b] || {};
    return [br.name, mo.name, mo.code, (mo.alias || []).join(' '), m._part.name, m._part.alias.join(' '), m.oem]
      .join(' ').toLowerCase();
  }

  /* ---------- change application ---------- */
  function same(a, b) {
    if (a == null && b == null) return true;
    if (a == null || b == null) return false;
    return a === b;
  }
  function norm(k, v) { if (k === 'price') return v == null ? null : v; if (k === 'sample') return v ? 1 : 0; if (k === 'status') return v || 'published'; return v == null ? '' : v; }
  /* patch: partial {field:value}; stores only differences from base. returns list of changed field names */
  function applyPatch(id, patch) {
    var b = baseOf(id); if (!b) return [];
    var ovs = loadOv().products, cur = merge(b), changed = [];
    Object.keys(patch).forEach(function (k) {
      if (FIELDS.indexOf(k) < 0) return;
      var v = patch[k];
      if (k === 'price') v = (v === '' || v == null) ? null : Number(v);
      if (k === 'sample') v = v ? 1 : 0;
      if (same(norm(k, cur[k]), v)) return;
      changed.push(k);
      ovs[id] = ovs[id] || {};
      if (same(norm(k, b[k]), v)) delete ovs[id][k]; else ovs[id][k] = v;
    });
    if (ovs[id] && !Object.keys(ovs[id]).length) delete ovs[id];
    return changed;
  }
  function describe(id) { var b = baseOf(id); if (!b) return id; var m = merge(b); return modelLabel(m) + ' ' + partOf(m).name; }

  /* ---------- state ---------- */
  var S = { tab: 'products', F: { brand: '', model: '', cat: '', flag: '', q: '' }, shown: PAGE, sel: {}, edit: null, imp: null, toast: '' };
  var filtered = [];

  /* ---------- views ---------- */
  function render() {
    if (!who()) { renderLogin(); return; }
    var tabs = [['products', 'Products'], ['add', 'Add product'], ['io', 'Import/Export'], ['activity', 'Activity']];
    root.innerHTML =
      '<div class="st-top"><div><h1 class="st-h1">Staff catalogue</h1><p class="st-sub">Signed in as <strong>' + esc(who()) + '</strong> (demo)</p></div>' +
      '<button type="button" class="btn ghost" data-act="signout">Sign out</button></div>' +
      '<div class="st-info"><strong>How publishing works.</strong> In this preview your changes are saved only in this browser. On the live site, Save publishes to the shop and Google within minutes.</div>' +
      '<div class="st-tabs" role="tablist">' + tabs.map(function (t) {
        return '<button type="button" role="tab" class="st-tab" id="st-tab-' + t[0] + '" data-act="tab" data-tab="' + t[0] + '" aria-selected="' + (S.tab === t[0]) + '">' + t[1] + '</button>';
      }).join('') + '</div><div id="st-panel" role="tabpanel"></div><div id="st-toast" class="st-toast" role="status" aria-live="polite"></div>';
    renderPanel();
    if (S.edit) openEdit(S.edit);
  }
  function renderPanel() {
    var p = $('#st-panel'); if (!p) return;
    if (S.tab === 'products') renderProducts(p);
    else if (S.tab === 'add') renderAdd(p);
    else if (S.tab === 'io') renderIO(p);
    else renderActivity(p);
  }
  function renderLogin() {
    root.innerHTML = '<div class="st-login"><form class="st-card" data-form="login" autocomplete="off"><h1 class="st-h1">Staff sign-in (demo)</h1>' +
      '<p class="st-note">Demo only. The real dashboard will use proper staff accounts.</p>' +
      '<label class="st-lbl" for="st-name">Your name</label><input id="st-name" class="st-in" name="name" type="text" required autocomplete="off">' +
      '<label class="st-lbl" for="st-pin">PIN</label><input id="st-pin" class="st-in" name="pin" type="password" inputmode="numeric" required autocomplete="off">' +
      '<p class="st-err" id="st-lerr" role="alert"></p>' +
      '<button type="submit" class="btn primary st-full">Sign in</button></form></div>';
  }
  function opts(list, sel, blank) {
    return (blank != null ? '<option value="">' + esc(blank) + '</option>' : '') + list.map(function (x) {
      return '<option value="' + esc(x[0]) + '"' + (String(x[0]) === String(sel) ? ' selected' : '') + '>' + esc(x[1]) + '</option>';
    }).join('');
  }
  function renderProducts(p) {
    var F = S.F;
    var models = (AT.models || []).filter(function (m) { return !F.brand || m.b === F.brand; })
      .map(function (m) { return [m.id, (BR[m.b] ? BR[m.b].name + ' ' : '') + m.name + (m.code ? ' ' + m.code : '') + ' ' + (m.years || '')]; });
    var flags = [['sample', 'Sample price'], ['nopart', 'No part number'], ['hidden', 'Hidden'], ['edited', 'Edited'], ['instock', 'In stock']];
    p.innerHTML = '<div id="st-sum" class="st-sum"></div>' +
      '<div class="st-filters">' +
      '<div class="st-f st-f-q"><label class="st-lbl" for="st-q">Search</label><input id="st-q" class="st-in" type="search" data-f="q" placeholder="Model, part, alias or part number" value="' + esc(F.q) + '"></div>' +
      '<div class="st-f"><label class="st-lbl" for="st-fb">Brand</label><select id="st-fb" class="st-in" data-f="brand">' + opts((AT.brands || []).map(function (b) { return [b.id, b.name]; }), F.brand, 'All brands') + '</select></div>' +
      '<div class="st-f"><label class="st-lbl" for="st-fm">Model</label><select id="st-fm" class="st-in" data-f="model">' + opts(models, F.model, 'All models') + '</select></div>' +
      '<div class="st-f"><label class="st-lbl" for="st-fc">Category</label><select id="st-fc" class="st-in" data-f="cat">' + opts((AT.cats || []).map(function (c) { return [c.id, c.name]; }), F.cat, 'All categories') + '</select></div>' +
      '<div class="st-f"><label class="st-lbl" for="st-ff">Show</label><select id="st-ff" class="st-in" data-f="flag">' + opts(flags, F.flag, 'All products') + '</select></div>' +
      '</div><div id="st-bulk"></div><div id="st-list"></div>';
    refreshList();
  }
  function refreshList() {
    var all = sortList(allMerged()), F = S.F, q = F.q.trim().toLowerCase(), toks = q ? q.split(/\s+/) : [];
    var c = { total: all.length, sample: 0, hidden: 0, instock: 0, nopart: 0 };
    all.forEach(function (m) {
      if (m.sample && m.price != null) c.sample++;
      if (m.status === 'hidden') c.hidden++;
      if (m.stock === 'in') c.instock++;
      if (!m.oem) c.nopart++;
    });
    filtered = all.filter(function (m) {
      if (F.brand && m._b !== F.brand) return false;
      if (F.model && m.m !== F.model) return false;
      if (F.cat && m._part.cat !== F.cat) return false;
      if (F.flag === 'sample' && !(m.sample && m.price != null)) return false;
      if (F.flag === 'nopart' && m.oem) return false;
      if (F.flag === 'hidden' && m.status !== 'hidden') return false;
      if (F.flag === 'instock' && m.stock !== 'in') return false;
      if (F.flag === 'edited' && !isEdited(m.id)) return false;
      if (toks.length) { var h = haystack(m); for (var i = 0; i < toks.length; i++) if (h.indexOf(toks[i]) < 0) return false; }
      return true;
    });
    var sum = $('#st-sum'), list = $('#st-list'); if (!sum || !list) return;
    function chip(flag, n, label, on) {
      return '<button type="button" class="st-chip' + (on ? ' on' : '') + '" data-act="sum" data-flag="' + flag + '" aria-pressed="' + !!on + '"><span class="st-chip-n">' + n + '</span><span class="st-chip-l">' + label + '</span></button>';
    }
    sum.innerHTML = chip('', c.total, 'Products', !F.flag) + chip('sample', c.sample, 'Sample prices to confirm', F.flag === 'sample') +
      chip('hidden', c.hidden, 'Hidden', F.flag === 'hidden') + chip('instock', c.instock, 'In stock', F.flag === 'instock') +
      chip('nopart', c.nopart, 'Missing part number', F.flag === 'nopart');
    var vis = filtered.slice(0, S.shown);
    list.innerHTML = '<p class="st-count" aria-live="polite">Showing ' + vis.length + ' of ' + filtered.length + ' matching products</p>' +
      (filtered.length ? '<div class="st-rows"><div class="st-row st-head" aria-hidden="true"><span></span><span class="st-rowmain"><span>Model</span><span>Part</span><span>Price</span><span>Stock</span><span>Part no.</span><span>Status</span></span></div>' +
        vis.map(rowHtml).join('') + '</div>' : '<div class="st-empty">No products match these filters.</div>') +
      (filtered.length > vis.length ? '<button type="button" class="btn st-more" data-act="more">Show more (' + (filtered.length - vis.length) + ' left)</button>' : '');
    refreshBulk();
  }
  function rowHtml(m) {
    var ed = isEdited(m.id);
    return '<div class="st-row' + (m.status === 'hidden' ? ' is-hidden' : '') + '">' +
      '<label class="st-chk"><input type="checkbox" data-sel="' + esc(m.id) + '"' + (S.sel[m.id] ? ' checked' : '') + ' aria-label="Select ' + esc(m._label + ' ' + m._part.name) + '"></label>' +
      '<button type="button" class="st-rowmain" data-act="edit" data-id="' + esc(m.id) + '">' +
      '<span class="st-c-model">' + esc(m._label) + '</span>' +
      '<span class="st-c-part">' + esc(m._part.name) + (ed ? ' <em class="st-badge b-edit">edited</em>' : '') + '</span>' +
      '<span class="st-c-price">' + esc(money(m.price)) + (m.price != null && m.sample ? ' <em class="st-badge b-sample">sample</em>' : '') + '</span>' +
      '<span class="st-c-stock"><em class="st-badge s-' + (m.stock || 'unk') + '">' + esc(STOCK[m.stock] || 'Unknown') + '</em></span>' +
      '<span class="st-c-oem">' + (m.oem ? esc(m.oem) : '<span class="st-dim">none</span>') + '</span>' +
      '<span class="st-c-status"><em class="st-badge ' + (m.status === 'hidden' ? 'b-hidden' : 'b-pub') + '">' + (m.status === 'hidden' ? 'Hidden' : 'Published') + '</em></span>' +
      '</button></div>';
  }
  function selIds() { return Object.keys(S.sel).filter(function (k) { return S.sel[k]; }); }
  function refreshBulk() {
    var b = $('#st-bulk'); if (!b) return;
    var n = selIds().length, allSel = filtered.length && filtered.every(function (m) { return S.sel[m.id]; });
    var kb = b.querySelector('details'), open = kb && kb.open;
    b.innerHTML = '<div class="st-bulkbar"><label class="st-chk st-selall"><input type="checkbox" data-act="selall"' + (allSel ? ' checked' : '') + '> <span>Select all ' + filtered.length + ' filtered</span></label>' +
      '<span class="st-selcount">' + n + ' selected</span>' +
      (n ? '<button type="button" class="btn ghost st-sm" data-act="selclear">Clear</button>' : '') + '</div>' +
      '<details class="st-bulk"' + (open ? ' open' : '') + '><summary>Bulk actions' + (n ? ' (' + n + ' selected)' : '') + '</summary><div class="st-bulkbody">' +
      '<div class="st-bulkrow"><label class="st-lbl" for="st-pct">Price change %</label><div class="st-inline"><input id="st-pct" class="st-in" type="number" step="0.1" placeholder="e.g. 5 or -10"><button type="button" class="btn" data-act="bulk-pct">Apply</button></div></div>' +
      '<div class="st-bulkrow st-btns"><button type="button" class="btn" data-act="bulk-confirm">Mark confirmed</button><button type="button" class="btn" data-act="bulk-hide">Hide</button><button type="button" class="btn" data-act="bulk-pub">Publish</button></div>' +
      '<p class="st-note">Bulk actions apply to the ticked products only.</p></div></details>';
  }

  /* ---------- edit sheet ---------- */
  function stockSel(id, v) { return '<select id="' + id + '" name="stock" class="st-in">' + opts(Object.keys(STOCK).map(function (k) { return [k, STOCK[k]]; }), v) + '</select>'; }
  function openEdit(id) {
    var b = baseOf(id); if (!b) return;
    var m = merge(b), pa = partOf(m); S.edit = id;
    closeModal(true);
    var d = document.createElement('div');
    d.className = 'st-modal'; d.id = 'st-modal';
    d.innerHTML = '<div class="st-sheet" role="dialog" aria-modal="true" aria-labelledby="st-mt"><form data-form="edit" data-id="' + esc(id) + '">' +
      '<div class="st-sheet-h"><div><h2 id="st-mt" class="st-h2">' + esc(pa.name) + '</h2><p class="st-sub">' + esc(modelLabel(m)) + (MO[m.m] && MO[m.m].years ? ' &middot; ' + esc(MO[m.m].years) : '') + '</p></div>' +
      '<button type="button" class="st-x" data-act="close" aria-label="Close">&times;</button></div>' +
      '<label class="st-lbl" for="e-price">Price (S$) &ndash; leave blank for "Ask for price"</label><input id="e-price" name="price" class="st-in" type="number" min="0" step="0.01" inputmode="decimal" value="' + (m.price == null ? '' : esc(m.price)) + '">' +
      '<label class="st-check"><input type="checkbox" name="confirmed"' + (!m.sample ? ' checked' : '') + '> <span>Price confirmed (real price)</span></label>' +
      '<p class="st-hint">Original: ' + esc(money(b.price)) + (b.sample ? ' (sample)' : '') + '</p>' +
      '<label class="st-lbl" for="e-oem">Part number (OEM)</label><input id="e-oem" name="oem" class="st-in" type="text" value="' + esc(m.oem) + '" autocomplete="off">' +
      '<label class="st-lbl" for="e-stock">Stock</label>' + stockSel('e-stock', m.stock || '') +
      '<label class="st-lbl" for="e-note">Note shown on the product page</label><textarea id="e-note" name="note" class="st-in" rows="3">' + esc(m.note) + '</textarea>' +
      '<label class="st-check"><input type="checkbox" name="published"' + (m.status !== 'hidden' ? ' checked' : '') + '> <span>Published (untick to hide from the shop)</span></label>' +
      '<p class="st-err" id="e-err" role="alert"></p>' +
      '<div class="st-actions"><button type="submit" class="btn primary">Save</button><button type="button" class="btn ghost" data-act="close">Cancel</button>' +
      '<button type="button" class="btn ghost st-danger" data-act="reset" data-id="' + esc(id) + '">' + (loadOv().added.some(function (a) { return a.id === id; }) ? 'Delete product' : 'Reset to original') + '</button></div>' +
      (b.url ? '<p class="st-view"><a href="../' + esc(b.url) + '" target="_blank" rel="noopener">View on shop</a></p>' : '') +
      '</form></div>';
    root.appendChild(d);
    document.body.classList.add('st-lock');
    var f = $('#e-price', d); if (f) f.focus();
  }
  function closeModal(keep) {
    var d = $('#st-modal'); if (d) d.parentNode.removeChild(d);
    document.body.classList.remove('st-lock');
    if (!keep) S.edit = null;
  }
  function saveEdit(form) {
    var id = form.getAttribute('data-id'), fd = form.elements, err = $('#e-err');
    var pr = fd.price.value.trim(), price = null;
    if (pr !== '') { price = Number(pr); if (isNaN(price) || price < 0) { err.textContent = 'Enter a valid price, or leave it blank.'; return; } price = Math.round(price * 100) / 100; }
    var patch = { price: price, sample: fd.confirmed.checked ? 0 : 1, oem: fd.oem.value.trim(), stock: fd.stock.value, status: fd.published.checked ? 'published' : 'hidden', note: fd.note.value.trim() };
    var ch = applyPatch(id, patch);
    if (ch.length) { saveOv(); log('Edited ' + describe(id) + ': ' + ch.join(', ')); toast('Saved ' + ch.length + ' change' + (ch.length > 1 ? 's' : '')); }
    else toast('No changes to save');
    closeModal(); refreshList();
  }

  /* ---------- add product ---------- */
  function renderAdd(p) {
    var models = (AT.models || []).map(function (m) { return [m.id, (BR[m.b] ? BR[m.b].name + ' ' : '') + m.name + (m.code ? ' ' + m.code : '') + ' ' + (m.years || '')]; });
    var parts = (AT.parts || []).map(function (x) { return [x.id, x.name]; }).concat([['__custom', 'Other (type a custom part name)']]);
    p.innerHTML = '<form class="st-card" data-form="add"><h2 class="st-h2">Add product</h2>' +
      '<label class="st-lbl" for="a-m">Model</label><select id="a-m" name="m" class="st-in">' + opts(models, '') + '</select>' +
      '<label class="st-lbl" for="a-p">Part type</label><select id="a-p" name="p" class="st-in" data-act="addpart">' + opts(parts, '') + '</select>' +
      '<div id="a-custom" hidden><label class="st-lbl" for="a-pn">Custom part name</label><input id="a-pn" name="pn" class="st-in" type="text">' +
      '<label class="st-lbl" for="a-pc">Category</label><select id="a-pc" name="pc" class="st-in">' + opts((AT.cats || []).map(function (c) { return [c.id, c.name]; }), '', 'No category') + '</select></div>' +
      '<label class="st-lbl" for="a-price">Price (S$, blank = Ask for price)</label><input id="a-price" name="price" class="st-in" type="number" min="0" step="0.01" inputmode="decimal">' +
      '<label class="st-check"><input type="checkbox" name="confirmed" checked> <span>Price confirmed (real price)</span></label>' +
      '<label class="st-lbl" for="a-oem">Part number (OEM)</label><input id="a-oem" name="oem" class="st-in" type="text">' +
      '<label class="st-lbl" for="a-stock">Stock</label>' + stockSel('a-stock', '') +
      '<label class="st-lbl" for="a-note">Note</label><textarea id="a-note" name="note" class="st-in" rows="3"></textarea>' +
      '<p class="st-err" id="a-err" role="alert"></p><button type="submit" class="btn primary st-full">Add product</button></form>';
  }
  function addProduct(form) {
    var f = form.elements, err = $('#a-err'), custom = f.p.value === '__custom', pn = f.pn.value.trim();
    var m = f.m.value;
    if (custom && !pn) { err.textContent = 'Type a part name.'; return; }
    var pr = f.price.value.trim(), price = pr === '' ? null : Math.round(Number(pr) * 100) / 100;
    if (price != null && (isNaN(price) || price < 0)) { err.textContent = 'Enter a valid price.'; return; }
    var dup = allMerged().filter(function (x) {
      return x.m === m && (custom ? (!x.p && x._part.name.toLowerCase() === pn.toLowerCase()) || x._part.name.toLowerCase() === pn.toLowerCase() : x.p === f.p.value);
    })[0];
    if (dup) { toast('That model and part already exist. Opening it.'); S.tab = 'products'; S.edit = dup.id; render(); return; }
    var prod = { id: 'custom-' + Date.now(), m: m, p: custom ? '' : f.p.value, url: '', price: price, sample: f.confirmed.checked ? 0 : 1,
      oem: f.oem.value.trim(), stock: f.stock.value, status: 'published', note: f.note.value.trim() };
    if (custom) { prod.pn = pn; prod.pc = f.pc.value; }
    loadOv().added.push(prod); saveOv();
    log('Added ' + describe(prod.id));
    toast('Product added');
    S.tab = 'products'; S.F = { brand: '', model: '', cat: '', flag: 'edited', q: '' }; render();
  }

  /* ---------- import / export ---------- */
  function renderIO(p) {
    p.innerHTML = '<div class="st-card"><h2 class="st-h2">Export</h2>' +
      '<p class="st-note">Download the full catalogue including your changes.</p>' +
      '<div class="st-btns"><button type="button" class="btn" data-act="exp-csv">Export CSV</button><button type="button" class="btn" data-act="exp-json">Export changes (JSON)</button></div>' +
      '<p class="st-note"><strong>Send the JSON file to Page One to publish the changes to the live site.</strong></p></div>' +
      '<div class="st-card"><h2 class="st-h2">Import CSV</h2>' +
      '<p class="st-note">Use a CSV exported from here. Rows are matched by <code>id</code>. Editable columns: price, sample, oem, stock, status, note. Unknown ids are reported, not added.</p>' +
      '<label class="st-lbl" for="i-file">CSV file</label><input id="i-file" class="st-in" type="file" accept=".csv,text/csv" data-act="csvfile">' +
      '<label class="st-lbl" for="i-text">Or paste CSV text</label><textarea id="i-text" class="st-in" rows="4"></textarea>' +
      '<button type="button" class="btn" data-act="imp-preview">Preview changes</button><div id="i-prev"></div></div>' +
      '<div class="st-card"><h2 class="st-h2">Start over</h2><p class="st-note">Remove every change saved in this browser.</p><button type="button" class="btn ghost st-danger" data-act="reset-all">Reset all changes</button></div>';
  }
  function csvCell(v) { v = v == null ? '' : String(v); return /[",\r\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }
  function download(name, text, type) {
    try {
      var a = document.createElement('a'), u = URL.createObjectURL(new Blob([text], { type: type }));
      a.href = u; a.download = name; document.body.appendChild(a); a.click();
      setTimeout(function () { document.body.removeChild(a); URL.revokeObjectURL(u); }, 500);
    } catch (e) { toast('Download not supported in this browser'); }
  }
  function today() { var d = new Date(); return d.getFullYear() + '-' + ('0' + (d.getMonth() + 1)).slice(-2) + '-' + ('0' + d.getDate()).slice(-2); }
  function exportCsv() {
    var head = ['id', 'brand', 'model', 'code', 'years', 'category', 'part', 'price', 'sample', 'oem', 'stock', 'status', 'note', 'url'];
    var rows = [head.join(',')];
    sortList(allMerged()).forEach(function (m) {
      var mo = MO[m.m] || {}, br = BR[mo.b] || {}, ca = CA[m._part.cat] || {};
      rows.push([m.id, br.name, mo.name, mo.code, mo.years, ca.name, m._part.name, m.price == null ? '' : m.price, m.sample ? 1 : 0, m.oem, m.stock, m.status, m.note, m.url].map(csvCell).join(','));
    });
    download('autotex-catalogue-' + today() + '.csv', '﻿' + rows.join('\r\n') + '\r\n', 'text/csv');
    log('Exported CSV'); toast('CSV downloaded');
  }
  function exportJson() {
    var o = loadOv();
    download('autotex-catalogue-changes-' + today() + '.json', JSON.stringify({ products: o.products, added: o.added, updated: o.updated || new Date().toISOString() }, null, 2), 'application/json');
    log('Exported changes JSON'); toast('JSON downloaded');
  }
  function parseCsv(t) {
    var rows = [], row = [], f = '', q = false, i, c;
    t = t.replace(/^﻿/, '');
    for (i = 0; i < t.length; i++) {
      c = t[i];
      if (q) {
        if (c === '"') { if (t[i + 1] === '"') { f += '"'; i++; } else q = false; } else f += c;
      } else if (c === '"') q = true;
      else if (c === ',') { row.push(f); f = ''; }
      else if (c === '\n' || c === '\r') { if (c === '\r' && t[i + 1] === '\n') i++; row.push(f); f = ''; rows.push(row); row = []; }
      else f += c;
    }
    if (f !== '' || row.length) { row.push(f); rows.push(row); }
    return rows.filter(function (r) { return r.length > 1 || (r.length === 1 && r[0].trim() !== ''); });
  }
  function previewImport() {
    var box = $('#i-prev'), text = $('#i-text').value;
    if (!text.trim()) { box.innerHTML = '<p class="st-err">Choose a CSV file or paste CSV text first.</p>'; return; }
    var rows = parseCsv(text);
    if (rows.length < 2) { box.innerHTML = '<p class="st-err">No data rows found.</p>'; return; }
    var head = rows[0].map(function (h) { return h.trim().toLowerCase(); }), ix = head.indexOf('id');
    if (ix < 0) { box.innerHTML = '<p class="st-err">The CSV needs an "id" column.</p>'; return; }
    var changes = [], unknown = [], bad = [], unchanged = 0;
    rows.slice(1).forEach(function (r, n) {
      var id = (r[ix] || '').trim(), b = baseOf(id);
      if (!id) return;
      if (!b) { unknown.push(id); return; }
      var cur = merge(b), patch = {}, diffs = [];
      FIELDS.forEach(function (k) {
        var col = head.indexOf(k); if (col < 0) return;
        var v = (r[col] || '').trim(), nv;
        if (k === 'price') { if (v === '') nv = null; else { nv = Number(v.replace(/^S\$/i, '').replace(/,/g, '')); if (isNaN(nv) || nv < 0) { bad.push('Row ' + (n + 2) + ': bad price "' + v + '"'); return; } } }
        else if (k === 'sample') { nv = /^(1|true|yes|y)$/i.test(v) ? 1 : (/^(0|false|no|n)$/i.test(v) ? 0 : null); if (nv === null) { bad.push('Row ' + (n + 2) + ': bad sample "' + v + '"'); return; } }
        else if (k === 'stock') { if (!(v in STOCK)) { bad.push('Row ' + (n + 2) + ': bad stock "' + v + '"'); return; } nv = v; }
        else if (k === 'status') { if (v !== 'published' && v !== 'hidden') { bad.push('Row ' + (n + 2) + ': bad status "' + v + '"'); return; } nv = v; }
        else nv = v;
        var cv = cur[k] === undefined ? (k === 'price' ? null : '') : cur[k];
        if (!same(cv, nv)) { patch[k] = nv; diffs.push(k + ': ' + (k === 'price' ? money(cv) : String(cv === '' ? '(blank)' : cv)) + ' → ' + (k === 'price' ? money(nv) : String(nv === '' ? '(blank)' : nv))); }
      });
      if (diffs.length) changes.push({ id: id, patch: patch, diffs: diffs }); else unchanged++;
    });
    S.imp = changes;
    box.innerHTML = '<div class="st-prev"><p><strong>' + changes.length + '</strong> row' + (changes.length === 1 ? '' : 's') + ' will change, ' + unchanged + ' unchanged, ' + unknown.length + ' unknown id' + (unknown.length === 1 ? '' : 's') + (bad.length ? ', ' + bad.length + ' invalid value' + (bad.length === 1 ? '' : 's') + ' skipped' : '') + '.</p>' +
      (changes.length ? '<ul class="st-list">' + changes.slice(0, 10).map(function (c) { return '<li><strong>' + esc(describe(c.id)) + '</strong><br>' + esc(c.diffs.join('; ')) + '</li>'; }).join('') + '</ul>' + (changes.length > 10 ? '<p class="st-note">...and ' + (changes.length - 10) + ' more.</p>' : '') +
        '<button type="button" class="btn primary" data-act="imp-apply">Apply ' + changes.length + ' change' + (changes.length === 1 ? '' : 's') + '</button>' : '') +
      (unknown.length ? '<p class="st-err">Unknown ids (not added): ' + esc(unknown.slice(0, 8).join(', ')) + (unknown.length > 8 ? ' and ' + (unknown.length - 8) + ' more' : '') + '</p>' : '') +
      (bad.length ? '<p class="st-err">' + esc(bad.slice(0, 5).join('; ')) + (bad.length > 5 ? '...' : '') + '</p>' : '') + '</div>';
  }
  function applyImport() {
    var ch = S.imp || [], n = 0;
    ch.forEach(function (c) { if (applyPatch(c.id, c.patch).length) n++; });
    if (n) { saveOv(); log('Imported CSV: ' + n + ' products changed'); }
    S.imp = null; toast('Imported ' + n + ' change' + (n === 1 ? '' : 's'));
    var b = $('#i-prev'); if (b) b.innerHTML = '<p class="st-ok">Applied ' + n + ' change' + (n === 1 ? '' : 's') + '.</p>';
  }

  /* ---------- activity ---------- */
  function renderActivity(p) {
    var a = loadAudit().slice().reverse();
    p.innerHTML = '<div class="st-card"><h2 class="st-h2">Activity</h2>' + (a.length ? '<ul class="st-log">' + a.map(function (e) {
      var d = new Date(e.t), ts = isNaN(d) ? esc(e.t) : esc(d.toLocaleString('en-SG', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }));
      return '<li><span class="st-log-t">' + ts + '</span> <strong>' + esc(e.who) + '</strong> ' + esc(e.what) + '</li>';
    }).join('') + '</ul>' : '<p class="st-note">No activity yet.</p>') + '</div>';
  }

  /* ---------- bulk ---------- */
  function bulk(kind) {
    var ids = selIds();
    if (!ids.length) { toast('Tick some products first'); return; }
    var patchFor, label;
    if (kind === 'pct') {
      var v = parseFloat(($('#st-pct') || {}).value);
      if (isNaN(v) || v === 0) { toast('Enter a percentage, e.g. 5 or -10'); return; }
      label = 'Change prices by ' + (v > 0 ? '+' : '') + v + '%';
      patchFor = function (m) { return m.price == null ? null : { price: Math.max(0, Math.round(m.price * (1 + v / 100) * 100) / 100) }; };
    } else if (kind === 'confirm') { label = 'Mark as confirmed'; patchFor = function () { return { sample: 0 }; }; }
    else if (kind === 'hide') { label = 'Hide'; patchFor = function () { return { status: 'hidden' }; }; }
    else { label = 'Publish'; patchFor = function () { return { status: 'published' }; }; }
    var ok = true;
    try { ok = window.confirm(label + ' for ' + ids.length + ' selected product' + (ids.length === 1 ? '' : 's') + '?'); } catch (e) { ok = true; }
    if (!ok) return;
    var n = 0;
    ids.forEach(function (id) {
      var b = baseOf(id); if (!b) return;
      var p = patchFor(merge(b)); if (p && applyPatch(id, p).length) n++;
    });
    if (n) { saveOv(); log('Bulk: ' + label + ' on ' + n + ' product' + (n === 1 ? '' : 's')); }
    toast(label + ': ' + n + ' updated');
    refreshList();
  }

  /* ---------- misc ---------- */
  var tt;
  function toast(msg) {
    var t = $('#st-toast'); if (!t) return;
    t.textContent = msg; t.classList.add('on');
    clearTimeout(tt); tt = setTimeout(function () { t.classList.remove('on'); }, 3500);
  }

  /* ---------- events ---------- */
  root.addEventListener('click', function (e) {
    var el = e.target.closest('[data-act]'); if (!el || !root.contains(el)) return;
    var act = el.getAttribute('data-act');
    if (el.tagName === 'SELECT' || el.tagName === 'INPUT' && act !== 'selall') return;
    if (act === 'tab') { S.tab = el.getAttribute('data-tab'); render(); }
    else if (act === 'signout') { try { sessionStorage.removeItem(SKEY); } catch (x) {} mem.who = null; closeModal(); render(); }
    else if (act === 'sum') { S.F = { brand: '', model: '', cat: '', flag: el.getAttribute('data-flag'), q: '' }; S.shown = PAGE; renderPanel(); }
    else if (act === 'more') { S.shown += PAGE; refreshList(); }
    else if (act === 'edit') openEdit(el.getAttribute('data-id'));
    else if (act === 'close') closeModal();
    else if (act === 'reset') {
      var id = el.getAttribute('data-id'), ov = loadOv(), isAdded = ov.added.some(function (a) { return a.id === id; });
      var nm = describe(id), ok = true;
      try { ok = window.confirm((isAdded ? 'Delete ' : 'Reset to original: ') + nm + '?'); } catch (x) {}
      if (!ok) return;
      if (isAdded) { ov.added = ov.added.filter(function (a) { return a.id !== id; }); }
      delete ov.products[id]; delete S.sel[id];
      saveOv(); log((isAdded ? 'Deleted ' : 'Reset to original: ') + nm);
      toast(isAdded ? 'Product deleted' : 'Reset to original'); closeModal(); refreshList();
    }
    else if (act === 'selall') { var on = el.checked; filtered.forEach(function (m) { if (on) S.sel[m.id] = true; else delete S.sel[m.id]; }); refreshList(); }
    else if (act === 'selclear') { S.sel = {}; refreshList(); }
    else if (act === 'bulk-pct') bulk('pct');
    else if (act === 'bulk-confirm') bulk('confirm');
    else if (act === 'bulk-hide') bulk('hide');
    else if (act === 'bulk-pub') bulk('pub');
    else if (act === 'exp-csv') exportCsv();
    else if (act === 'exp-json') exportJson();
    else if (act === 'imp-preview') previewImport();
    else if (act === 'imp-apply') applyImport();
    else if (act === 'reset-all') {
      var ok2 = true; try { ok2 = window.confirm('Remove ALL changes saved in this browser?'); } catch (x) {}
      if (!ok2) return;
      mem.ov = { products: {}, added: [] }; saveOv(); log('Reset all changes'); S.sel = {}; toast('All changes removed');
    }
  });
  root.addEventListener('input', function (e) {
    var t = e.target;
    if (t.getAttribute('data-f') === 'q') { S.F.q = t.value; S.shown = PAGE; refreshList(); }
  });
  root.addEventListener('change', function (e) {
    var t = e.target, f = t.getAttribute('data-f'), sid = t.getAttribute('data-sel');
    if (f && f !== 'q') {
      S.F[f] = t.value; if (f === 'brand') S.F.model = '';
      S.shown = PAGE; renderPanel();
    } else if (sid) { if (t.checked) S.sel[sid] = true; else delete S.sel[sid]; refreshBulk(); }
    else if (t.getAttribute('data-act') === 'selall') { /* handled in click */ }
    else if (t.getAttribute('data-act') === 'addpart') { var c = $('#a-custom'); if (c) c.hidden = t.value !== '__custom'; }
    else if (t.getAttribute('data-act') === 'csvfile' && t.files && t.files[0]) {
      var r = new FileReader();
      r.onload = function () { $('#i-text').value = String(r.result || ''); previewImport(); };
      r.readAsText(t.files[0]);
    }
  });
  root.addEventListener('submit', function (e) {
    var f = e.target.getAttribute('data-form'); if (!f) return;
    e.preventDefault();
    if (f === 'login') {
      var n = e.target.elements.name.value.trim(), pin = e.target.elements.pin.value.trim();
      if (!n) { $('#st-lerr').textContent = 'Enter your name.'; return; }
      if (pin !== PIN) { $('#st-lerr').textContent = 'Wrong PIN.'; return; }
      mem.who = n; try { sessionStorage.setItem(SKEY, n); } catch (x) {}
      log('Signed in'); render();
    } else if (f === 'edit') saveEdit(e.target);
    else if (f === 'add') addProduct(e.target);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && $('#st-modal')) closeModal();
  });
  root.addEventListener('mousedown', function (e) { if (e.target.id === 'st-modal') closeModal(); });

  render();
})();
