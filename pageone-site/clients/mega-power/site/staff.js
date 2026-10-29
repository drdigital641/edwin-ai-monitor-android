/* Mega Power staff dashboard - DEMO. Data lives in this browser (localStorage). Production: real logins, server-side permissions, database, audit log, backups. */
(function () {
  'use strict';
  var M = window.MP, D = M.D, LS = M.LS, esc = M.esc, ROOT = M.ROOT;
  var AUD = 'mp_audit_v1', ROLE = 'mp_role_v1', APPR = 'mp_approvals_v1';
  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  var app = $('#app');
  var role = LS.get(ROLE, 'admin');
  var ROLES = { admin: 'Admin', editor: 'Catalogue editor', sales: 'Sales' };
  var CAN = {
    overview: ['admin', 'editor', 'sales'], products: ['admin', 'editor', 'sales'], edit: ['admin', 'editor'], import: ['admin', 'editor'],
    leads: ['admin', 'sales'], migration: ['admin', 'editor'], settings: ['admin'], guide: ['admin', 'editor', 'sales']
  };
  function can(k) { return CAN[k].indexOf(role) >= 0; }
  var IC = {
    home: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 11 12 4l9 7v9H3z"/><path d="M9 20v-6h6v6"/></svg>',
    box: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/></svg>',
    plus: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v8M8 12h8"/></svg>',
    up: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 16V4M7 9l5-5 5 5M4 20h16"/></svg>',
    inbox: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 13l3-8h12l3 8v6H3z"/><path d="M3 13h5l1 3h6l1-3h5"/></svg>',
    route: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.5"/></svg>',
    cog: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/></svg>',
    book: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4zM20 4h-6"/><path d="M20 4v14h-6"/></svg>'
  };
  function now() { return new Date().toISOString(); }
  function fmt(t) { try { var d = new Date(t); return d.toLocaleDateString('en-SG', { day: 'numeric', month: 'short' }) + ' ' + d.toLocaleTimeString('en-SG', { hour: '2-digit', minute: '2-digit' }); } catch (e) { return t; } }
  function audit(msg, id) { var a = LS.get(AUD, []); a.unshift({ t: now(), who: ROLES[role], msg: msg, id: id || '' }); LS.set(AUD, a.slice(0, 200)); }
  function prods() { return M.allProducts(); }
  function save(items) { items.forEach(function (p) { delete p._ix; }); if (!M.saveProducts(items)) { M.toast('Browser storage is full. Remove some demo photos or reset the demo.'); return false; } return true; }
  function leads() { return M.leads(); }
  function saveLeads(l) { LS.set(M.K.leads, l); }
  function srcTag(p) { return p.src === 'public' ? '<span class="tag tag-t">Public site import</span>' : '<span class="tag tag-r">DEMO / NOT VERIFIED</span>'; }
  function stTag(s) { return '<span class="tag ' + ({ published: 'tag-t', draft: 'tag-a', archived: 'tag-g' }[s] || 'tag-g') + '">' + esc(s) + '</span>'; }
  var LT = { EXPORT: ['tag-n', 'EXPORT'], SUPPLIER: ['tag-t', 'SUPPLIER'], LOCAL: ['tag-o', 'LOCAL'] };
  function ltag(t) { return '<span class="tag ' + (LT[t] || ['tag-g'])[0] + '">' + esc(t) + '</span>'; }
  function pendingFit(l) { return l.status === 'New' && l.type !== 'SUPPLIER' && (l.sub === 'VIN_MATCH' || (l.fields && (l.fields.vin || l.fields.oem)) || (l.items || []).some(function (i) { return i.src !== 'public'; }) || (l.items || []).length > 0); }

  /* ---------- shell ---------- */
  function shell(route, inner) {
    var L = leads(), newL = L.filter(function (l) { return l.status === 'New'; }).length;
    var nav = [
      ['overview', '#overview', 'Overview', IC.home], ['products', '#products', 'Products', IC.box], ['edit', '#new', 'Add product', IC.plus], ['import', '#import', 'Bulk import', IC.up],
      ['leads', '#leads', 'Enquiries', IC.inbox, newL], ['migration', '#migration', 'Old site migration', IC.route], ['settings', '#settings', 'Settings & approvals', IC.cog], ['guide', '#guide', 'How-to for staff', IC.book]
    ].filter(function (n) { return can(n[0]); });
    app.innerHTML = '<header class="st-top"><a class="brand" href="#overview"><i>MP</i><span>Mega Power<small>Staff dashboard · demo</small></span></a><span class="sp"></span>' +
      '<label class="sr" for="role">Role</label><select id="role" aria-label="Signed in as (demo role)">' + Object.keys(ROLES).map(function (k) { return '<option value="' + k + '"' + (k === role ? ' selected' : '') + '>Demo role: ' + ROLES[k] + '</option>'; }).join('') + '</select>' +
      '<a href="' + ROOT + '" target="_blank" rel="noopener">View website ↗</a><button class="lnk" id="reset">Reset demo</button></header>' +
      '<div class="st-demo">Demo back office. Everything here is saved in this browser only, and roles are simulated. Production needs real logins, server-side permissions and a database.</div>' +
      '<div class="st-l"><nav class="st-nav" aria-label="Dashboard"><span class="grp">Catalogue</span>' + nav.map(function (n) { return (n[0] === 'leads' ? '<span class="grp">Sales</span>' : n[0] === 'migration' ? '<span class="grp">Launch</span>' : '') + '<a href="' + n[1] + '"' + (route === n[0] ? ' aria-current="page"' : '') + '>' + n[3] + n[2] + (n[4] ? '<b>' + n[4] + '</b>' : '') + '</a>'; }).join('') + '</nav>' +
      '<main class="st-main" id="main">' + inner + '</main></div>';
    $('#role').addEventListener('change', function () { role = this.value; LS.set(ROLE, role); M.toast('Now viewing as ' + ROLES[role] + ' (demo).'); router(); });
    $('#reset').addEventListener('click', function () { if (!confirm('Clear all demo products, enquiries and history in this browser?')) return; [M.K.prod, M.K.rfq, M.K.leads, M.K.ev, AUD, APPR].forEach(LS.del); M.toast('Demo reset to the 13 public listings.'); router(); });
    window.scrollTo(0, 0);
  }
  function locked(name) { return '<div class="locked"><b>' + esc(ROLES[role]) + ' cannot open ' + esc(name) + '.</b><br>Switch the demo role at the top to see how permissions work.</div>'; }

  /* ---------- overview ---------- */
  function overview() {
    var P = prods(), L = leads(), ev = LS.get(M.K.ev, []);
    var pub = P.filter(function (p) { return p.status === 'published'; }), dr = P.filter(function (p) { return p.status === 'draft'; });
    var cnt = function (t) { return L.filter(function (l) { return l.type === t; }).length; };
    var pend = L.filter(pendingFit).length;
    var searches = ev.filter(function (e) { return e.e === 'search_started'; }), nm = {};
    ev.filter(function (e) { return e.e === 'no_match'; }).forEach(function (e) { var q = (e.d.q || '').toLowerCase(); nm[q] = (nm[q] || 0) + 1; });
    var nmList = Object.keys(nm).sort(function (a, b) { return nm[b] - nm[a]; }).slice(0, 6);
    var pubN = P.filter(function (p) { return p.src === 'public'; }).length, demoN = P.length - pubN;
    var recent = P.slice().sort(function (a, b) { return (b.created || '').localeCompare(a.created || ''); }).slice(0, 5);
    var aud = LS.get(AUD, []).slice(0, 6);
    var h = '<h1>Overview</h1><p class="st-sub">Catalogue and enquiries at a glance. Figures below are demo data in this browser.</p>' +
      '<div class="kpis">' +
      '<a class="kpi" href="#products"><small>Published products</small><b>' + pub.length + '</b><i>' + dr.length + ' draft · ' + P.filter(function (p) { return p.status === 'archived'; }).length + ' archived</i><div class="bar"><span style="width:' + Math.round(pub.length / Math.max(1, P.length) * 100) + '%"></span></div></a>' +
      '<a class="kpi k-ex" href="#leads/EXPORT"><small>Export RFQs</small><b>' + cnt('EXPORT') + '</b><i>overseas buyers</i></a>' +
      '<a class="kpi k-su" href="#leads/SUPPLIER"><small>Supplier enquiries</small><b>' + cnt('SUPPLIER') + '</b><i>import / new brands</i></a>' +
      '<a class="kpi k-lo" href="#leads/LOCAL"><small>Local workshop</small><b>' + cnt('LOCAL') + '</b><i>Singapore</i></a>' +
      '<a class="kpi k-pe" href="#leads"><small>Pending fitment checks</small><b>' + pend + '</b><i>new enquiries with VIN, OEM or parts</i></a>' +
      '</div><div class="cols"><div>' +
      '<div class="pan"><h2>Catalogue source</h2><p style="margin:0 0 8px"><b>' + pubN + '</b> records imported from the public megapower.com.sg pages (read ' + esc(D.read) + '). <b>' + demoN + '</b> demo records added here.</p><p class="note" style="margin:0">This is not the full catalogue. Hidden, unpublished and other products need an official export from the current Magento admin. See <a href="#migration">Old site migration</a>.</p></div>' +
      '<div class="pan"><h2>Recently added products</h2>' + (recent.filter(function (p) { return p.created; }).length ? '<ul class="feed">' + recent.filter(function (p) { return p.created; }).map(function (p) { return '<li><a href="#edit/' + esc(p.id) + '">' + esc(p.name) + '</a> ' + srcTag(p) + '<time>' + fmt(p.created) + '</time></li>'; }).join('') + '</ul>' : '<p class="empty">No products added yet. <a href="#new">Add one</a> to see it appear in the website search.</p>') + '</div>' +
      '<div class="pan"><h2>Change history</h2>' + (aud.length ? '<ul class="feed">' + aud.map(function (a) { return '<li><span>' + esc(a.msg) + ' <span class="note">by ' + esc(a.who) + '</span></span><time>' + fmt(a.t) + '</time></li>'; }).join('') + '</ul>' : '<p class="empty">No changes yet.</p>') + '</div>' +
      '</div><div>' +
      '<div class="pan"><h2>Latest enquiries<span class="sp"></span>' + (can('leads') ? '<a class="btn btn-g btn-s" href="#leads">Open inbox</a>' : '') + '</h2>' + (L.length ? '<ul class="feed">' + L.slice(0, 6).map(function (l) { return '<li>' + ltag(l.type) + ' <span>' + (can('leads') ? '<a href="#lead/' + esc(l.id) + '">' : '') + esc(l.id) + (can('leads') ? '</a>' : '') + ' · ' + esc(l.fields.company || l.fields.name || '') + (l.fields.country ? ', ' + esc(l.fields.country) : '') + '</span><time>' + fmt(l.created) + '</time></li>'; }).join('') + '</ul>' : '<p class="empty">No enquiries yet. Send one from the <a href="' + ROOT + 'export/" target="_blank">export page</a>.</p>') + '</div>' +
      '<div class="pan"><h2>Search insights</h2><p style="margin:0 0 8px">' + searches.length + ' searches in this browser. Searches with no match show demand you could source:</p>' + (nmList.length ? '<ul class="feed">' + nmList.map(function (q) { return '<li><span class="mono">' + esc(q) + '</span><time>' + nm[q] + '×</time></li>'; }).join('') + '</ul>' : '<p class="note">None yet. Try “Mercedes W210 compressor” on the website.</p>') + '</div>' +
      '</div></div>';
    shell('overview', h);
  }

  /* ---------- product list ---------- */
  var PF = { q: '', cat: '', st: '', src: '' };
  function products() {
    var P = prods();
    var h = '<h1>Products</h1><p class="st-sub">' + P.length + ' records. Edits show on the website straight away in this browser.</p>' +
      '<div class="toolbar"><input class="in" id="pq" placeholder="Search name, OEM, make…" value="' + esc(PF.q) + '"><select class="in" id="pc"><option value="">All categories</option>' + D.cats.map(function (c) { return '<option value="' + c.slug + '"' + (PF.cat === c.slug ? ' selected' : '') + '>' + esc(c.name) + '</option>'; }).join('') + '</select>' +
      '<select class="in" id="ps"><option value="">Any status</option><option' + (PF.st === 'published' ? ' selected' : '') + '>published</option><option' + (PF.st === 'draft' ? ' selected' : '') + '>draft</option><option' + (PF.st === 'archived' ? ' selected' : '') + '>archived</option></select>' +
      '<select class="in" id="pr"><option value="">Any source</option><option value="public"' + (PF.src === 'public' ? ' selected' : '') + '>Public site import</option><option value="demo"' + (PF.src === 'demo' ? ' selected' : '') + '>Demo records</option></select>' +
      (can('edit') ? '<a class="btn btn-o btn-s" href="#new">+ Add product</a>' : '') + '</div><div class="pan" style="padding:6px 12px"><div class="tw"><table class="tbl rsp"><thead><tr><th></th><th>Product</th><th>References</th><th>Category</th><th>Source</th><th>Status</th><th></th></tr></thead><tbody id="pt"></tbody></table></div></div>';
    shell('products', h);
    function draw() {
      var q = M.norm(PF.q), qq = PF.q.toLowerCase();
      var rows = P.filter(function (p) {
        if (PF.cat && p.cat !== PF.cat) return false; if (PF.st && p.status !== PF.st) return false;
        if (PF.src === 'public' && p.src !== 'public') return false; if (PF.src === 'demo' && p.src === 'public') return false;
        if (!qq) return true;
        return (p.name + ' ' + p.make + ' ' + p.model + ' ' + (p.sku || '')).toLowerCase().indexOf(qq) >= 0 || (p.refs || []).some(function (r) { return M.norm(r.n).indexOf(q) >= 0; });
      });
      $('#pt').innerHTML = rows.length ? rows.map(function (p) {
        return '<tr><td><img src="' + esc(M.pimg(p)) + '" alt="" onerror="this.onerror=null;this.src=\'' + M.ph(p) + '\'"></td><td><div class="t">' + esc(p.name) + '</div><span class="note">' + esc(p.sku ? 'SKU ' + p.sku : 'No SKU yet') + '</span></td>' +
          '<td data-h="Refs" class="mono" style="font-size:.82rem">' + ((p.refs || []).map(function (r) { return esc(r.n); }).join('<br>') || '<span class="note">none</span>') + '</td><td data-h="Category">' + esc(M.catName(p.cat)) + '</td><td>' + srcTag(p) + '</td><td>' + stTag(p.status) + '</td>' +
          '<td><div class="acts">' + (can('edit') ? '<a class="btn btn-g btn-s" href="#edit/' + esc(p.id) + '">Edit</a><button class="btn btn-g btn-s" data-dup="' + esc(p.id) + '">Duplicate</button><button class="btn btn-g btn-s" data-arc="' + esc(p.id) + '">' + (p.status === 'archived' ? 'Restore' : 'Archive') + '</button>' : '') + '<a class="btn btn-g btn-s" href="' + M.purl(p) + '" target="_blank" rel="noopener">View</a></div></td></tr>';
      }).join('') : '<tr><td colspan="7" class="empty">No products match.</td></tr>';
    }
    draw();
    $('#pq').addEventListener('input', function () { PF.q = this.value; draw(); });
    $('#pc').addEventListener('change', function () { PF.cat = this.value; draw(); });
    $('#ps').addEventListener('change', function () { PF.st = this.value; draw(); });
    $('#pr').addEventListener('change', function () { PF.src = this.value; draw(); });
    $('#pt').addEventListener('click', function (e) {
      var d = e.target.closest('[data-dup]'), a = e.target.closest('[data-arc]');
      if (d) { var src = M.byId(d.getAttribute('data-dup')), c = JSON.parse(JSON.stringify(src)); c.id = newId(); c.name += ' (copy)'; c.sku = ''; c.status = 'draft'; c.src = 'staff-demo'; c.verified = false; c.created = now(); delete c.url; delete c.old; P.push(c); if (save(P)) { audit('Duplicated ' + src.name + ' as a draft', c.id); location.hash = '#edit/' + c.id; } }
      if (a) { var p = P.filter(function (x) { return x.id === a.getAttribute('data-arc'); })[0]; p.status = p.status === 'archived' ? 'published' : 'archived'; if (p.status === 'published' && p.src !== 'public') p.status = 'draft'; save(P); audit((p.status === 'archived' ? 'Archived ' : 'Restored ') + p.name, p.id); M.toast(p.name + ' is now ' + p.status + '.'); products(); }
    });
  }
  function newId() { var P = prods(), n = P.length + 1, id; do { id = 'mp-d' + String(n++).padStart(4, '0'); } while (P.some(function (p) { return p.id === id; })); return id; }

  /* ---------- product form ---------- */
  function editor(id) {
    if (!can('edit')) { shell('edit', locked('the product editor')); return; }
    var P = prods(), orig = id ? P.filter(function (p) { return p.id === id; })[0] : null;
    if (id && !orig) { shell('products', '<p class="empty">Product not found.</p>'); return; }
    var p = orig ? JSON.parse(JSON.stringify(orig)) : { id: newId(), src: 'staff-demo', status: 'draft', verified: false, refs: [{ n: '', t: 'Original OEM number', v: false }], codes: [], images: [], specs: [], tags: [], related: [], stock: 'hidden', cat: '' };
    if (!p.images) p.images = p.image ? [p.image] : [];
    var isPub = p.src === 'public';
    var cats = D.cats.map(function (c) { return '<option value="' + c.slug + '"' + (p.cat === c.slug ? ' selected' : '') + '>' + esc(c.name) + '</option>'; }).join('');
    var h = '<h1>' + (orig ? 'Edit product' : 'Add new product') + '</h1><p class="st-sub">' + (orig ? srcTag(p) + ' ' + stTag(p.status) + ' · ID ' + esc(p.id) : 'New records are marked DEMO / NOT VERIFIED until a staff member verifies the fitment.') + '</p>' +
      (isPub ? '<div class="demo-flag" style="margin-top:0"><span>This record was copied from the public page <a href="' + esc(p.old) + '" target="_blank" rel="noopener">' + esc(p.old.replace('https://www.', '')) + '</a>. Its URL stays the same after launch.' + (p.staff_note ? ' <b>Check:</b> ' + esc(p.staff_note) : '') + '</span></div>' : '') +
      '<form id="pf" class="pf" novalidate><div>' +
      '<div class="pan"><h2>Photos</h2><label class="drop big" data-img><input type="file" accept="image/*" multiple><b>Drag photos here or tap to choose</b>First photo is the main image. Resized in the browser before saving.</label><div class="gal" id="gal"></div>' +
      '<div style="margin-top:12px"><label class="f" for="f-alt">Alt text for the main photo</label><input class="in" id="f-alt" name="alt" value="' + esc(p.alt || '') + '" placeholder="e.g. Sanden compressor for BMW 2 Series F45"></div></div>' +
      '<div class="pan"><h2>Basics</h2><div class="fgrid">' +
      '<div class="full"><label class="f" for="f-name">Product title</label><input class="in" id="f-name" name="name" value="' + esc(p.name || '') + '" placeholder="e.g. Toyota Hiace A/C Compressor - Denso" required></div>' +
      '<div><label class="f" for="f-cat">Category</label><select class="in" id="f-cat" name="cat" required><option value="">Choose</option>' + cats + '</select></div>' +
      '<div><label class="f" for="f-sku">Internal SKU</label><input class="in mono" id="f-sku" name="sku" value="' + esc(p.sku || '') + '"></div>' +
      '<div><label class="f" for="f-brand">Part / component brand</label><input class="in" id="f-brand" name="brand" value="' + esc(p.brand || '') + '" placeholder="e.g. Denso"></div>' +
      '<div><label class="f" for="f-country">Country of manufacture</label><input class="in" id="f-country" name="country" value="' + esc(p.country || '') + '"></div>' +
      '<div class="full"><label class="f" for="f-desc">Description</label><textarea class="in" id="f-desc" name="desc">' + esc(p.desc || '') + '</textarea></div></div></div>' +
      '<div class="pan"><h2>Reference numbers</h2><p class="note" style="margin-top:-4px">Keep the number exactly as printed. Search ignores spaces and dashes. Tick “verified” only when staff have confirmed it.</p><div class="rows" id="refs"></div><button type="button" class="btn btn-g btn-s" id="addref">+ Add alternate / cross-reference</button></div>' +
      '<div class="pan"><h2>Vehicle application</h2><div class="fgrid">' +
      '<div><label class="f" for="f-make">Make</label><input class="in" id="f-make" name="make" value="' + esc(p.make || '') + '" list="makes"></div>' +
      '<div><label class="f" for="f-model">Model</label><input class="in" id="f-model" name="model" value="' + esc(p.model || '') + '"></div>' +
      '<div><label class="f" for="f-codes">Series / chassis codes <i>(comma separated)</i></label><input class="in mono" id="f-codes" name="codes" value="' + esc((p.codes || []).join(', ')) + '" placeholder="e.g. F45, F46"></div>' +
      '<div class="grid2"><div><label class="f" for="f-yf">Year from</label><input class="in" id="f-yf" name="yearFrom" inputmode="numeric" value="' + esc(p.yearFrom || (p.years && p.years[0]) || '') + '"></div><div><label class="f" for="f-yt">Year to</label><input class="in" id="f-yt" name="yearTo" inputmode="numeric" value="' + esc(p.yearTo || (p.years && p.years[p.years.length - 1]) || '') + '"></div></div>' +
      '<div><label class="f" for="f-mk">Market</label><input class="in" id="f-mk" name="market" value="' + esc(p.market || '') + '" placeholder="e.g. Europe, Japan, Asia"></div>' +
      '<div><label class="f" for="f-st">Steering side</label><select class="in" id="f-st" name="steering"><option value="">Not applicable / unknown</option><option' + (p.steering === 'Right-hand drive' ? ' selected' : '') + '>Right-hand drive</option><option' + (p.steering === 'Left-hand drive' ? ' selected' : '') + '>Left-hand drive</option><option' + (p.steering === 'Both' ? ' selected' : '') + '>Both</option></select></div>' +
      '<div><label class="f" for="f-gas">Refrigerant</label><input class="in" id="f-gas" name="gas" value="' + esc(p.gas || '') + '"></div><div><label class="f" for="f-oil">Compressor oil</label><input class="in" id="f-oil" name="oil" value="' + esc(p.oil || '') + '"></div>' +
      '</div><datalist id="makes">' + Object.keys(prods().reduce(function (a, x) { if (x.make) a[x.make] = 1; return a; }, {})).map(function (m) { return '<option value="' + esc(m) + '">'; }).join('') + '</datalist></div>' +
      '<div class="pan"><h2>Technical specifications</h2><div class="rows" id="specs"></div><button type="button" class="btn btn-g btn-s" id="addspec">+ Add specification</button></div>' +
      '<div class="pan"><h2>Search &amp; SEO</h2><div class="fgrid">' +
      '<div class="full"><label class="f" for="f-tags">Search tags <i>(comma separated, e.g. other spellings)</i></label><input class="in" id="f-tags" name="tags" value="' + esc((p.tags || []).join(', ')) + '"></div>' +
      '<div class="full"><label class="f" for="f-mt">Meta title <span class="cnt-hint" data-cnt="60"></span></label><input class="in" id="f-mt" name="metaTitle" value="' + esc(p.metaTitle || '') + '"></div>' +
      '<div class="full"><label class="f" for="f-md">Meta description <span class="cnt-hint" data-cnt="160"></span></label><textarea class="in" id="f-md" name="metaDesc" style="min-height:70px">' + esc(p.metaDesc || '') + '</textarea></div>' +
      '<div class="full"><label class="f">Google preview</label><div class="serp" id="serp"></div></div></div></div>' +
      '</div><div>' +
      '<div class="pan"><h2>Publishing</h2><label class="f" for="f-status">Status</label><select class="in" id="f-status" name="status"><option value="draft"' + (p.status === 'draft' ? ' selected' : '') + '>Draft (hidden)</option><option value="published"' + (p.status === 'published' ? ' selected' : '') + '>Published</option><option value="archived"' + (p.status === 'archived' ? ' selected' : '') + '>Archived</option></select>' +
      '<label class="f" for="f-stock" style="margin-top:12px">Stock display on website</label><select class="in" id="f-stock" name="stock"><option value="hidden"' + (p.stock !== 'on-request' && p.stock !== 'in-stock' ? ' selected' : '') + '>Hidden (default)</option><option value="on-request"' + (p.stock === 'on-request' ? ' selected' : '') + '>“Available on request”</option><option value="in-stock"' + (p.stock === 'in-stock' ? ' selected' : '') + '>“In stock” (needs owner approval)</option></select>' +
      '<label class="chk" style="margin-top:14px;color:var(--ink)"><input type="checkbox" name="verified"' + (p.verified ? ' checked' : '') + '> Fitment and references verified by staff</label>' +
      '<h3 style="font-size:.92rem;margin:16px 0 6px">Checks before publishing</h3><ul class="checks" id="checks"></ul></div>' +
      '<div class="pan"><h2>Related products</h2><select class="in" id="f-rel" multiple size="6" style="min-height:140px">' + prods().filter(function (x) { return x.id !== p.id; }).map(function (x) { return '<option value="' + esc(x.id) + '"' + ((p.related || []).indexOf(x.id) >= 0 ? ' selected' : '') + '>' + esc(x.name) + '</option>'; }).join('') + '</select><p class="note">Hold Ctrl / Cmd to pick several.</p></div>' +
      (orig ? '<div class="pan"><h2>History</h2><ul class="feed">' + (LS.get(AUD, []).filter(function (a) { return a.id === p.id; }).slice(0, 8).map(function (a) { return '<li><span>' + esc(a.msg) + '</span><time>' + fmt(a.t) + '</time></li>'; }).join('') || '<li class="note">No changes in this demo yet.' + (isPub ? ' Source: public page, ' + esc(D.read) + '.' : '') + '</li>') + '</ul></div>' : '') +
      '</div><div class="sticky-act" style="grid-column:1/-1"><button class="btn btn-o" type="submit">Save product</button><button class="btn btn-g" type="button" id="saveview">Save and view on website</button><a class="btn btn-g" href="#products">Cancel</a></div></form>';
    shell('edit', h);
    var f = $('#pf');
    // photos
    function drawGal() {
      $('#gal').innerHTML = p.images.map(function (src, i) { return '<div><img src="' + esc(src) + '" alt="" onerror="this.onerror=null;this.src=\'' + M.ph(p) + '\'">' + (i === 0 ? '<span class="main">Main</span>' : '') + '<button type="button" data-rmimg="' + i + '" aria-label="Remove photo">×</button></div>'; }).join('');
      checks();
    }
    $('#gal').addEventListener('click', function (e) { var b = e.target.closest('[data-rmimg]'); if (b) { p.images.splice(+b.getAttribute('data-rmimg'), 1); drawGal(); } });
    var dz = $('[data-img]'), fi = $('input', dz);
    function addFiles(files) {
      Array.prototype.forEach.call(files, function (file) {
        if (!/^image\//.test(file.type)) { M.toast(file.name + ' is not an image.'); return; }
        if (file.size > 8 * 1024 * 1024) { M.toast(file.name + ' is over 8 MB.'); return; }
        var rd = new FileReader();
        rd.onload = function () {
          var im = new Image(); im.onload = function () {
            var s = Math.min(1, 900 / Math.max(im.width, im.height)), c = document.createElement('canvas'); c.width = Math.round(im.width * s); c.height = Math.round(im.height * s);
            var g = c.getContext('2d'); g.fillStyle = '#fff'; g.fillRect(0, 0, c.width, c.height); g.drawImage(im, 0, 0, c.width, c.height);
            p.images.push(c.toDataURL('image/jpeg', 0.8)); drawGal();
          }; im.src = rd.result;
        };
        rd.readAsDataURL(file);
      });
    }
    fi.addEventListener('change', function () { addFiles(fi.files); fi.value = ''; });
    ['dragenter', 'dragover'].forEach(function (t) { dz.addEventListener(t, function (e) { e.preventDefault(); dz.classList.add('over'); }); });
    ['dragleave', 'drop'].forEach(function (t) { dz.addEventListener(t, function (e) { e.preventDefault(); dz.classList.remove('over'); }); });
    dz.addEventListener('drop', function (e) { addFiles(e.dataTransfer.files); });
    // refs
    function refRow(r) { return '<div class="row"><input class="in mono" data-rn value="' + esc(r.n) + '" placeholder="Number as printed"><select class="in" data-rt>' + ['Original OEM number', 'OEM number (as listed)', 'Manufacturer part number', 'Cross-reference', 'Reseller SKU'].map(function (t) { return '<option' + (r.t === t ? ' selected' : '') + '>' + t + '</option>'; }).join('') + '</select><label><input type="checkbox" data-rv' + (r.v ? ' checked' : '') + '> verified</label><button type="button" class="x" data-rmrow aria-label="Remove">×</button></div>'; }
    function specRow(s) { return '<div class="row kv"><input class="in" data-sk value="' + esc(s.k) + '" placeholder="e.g. Voltage"><input class="in" data-sv value="' + esc(s.v) + '" placeholder="e.g. 12V"><button type="button" class="x" data-rmrow aria-label="Remove">×</button></div>'; }
    $('#refs').innerHTML = (p.refs.length ? p.refs : [{ n: '', t: 'Original OEM number', v: false }]).map(refRow).join('');
    $('#specs').innerHTML = (p.specs || []).map(specRow).join('');
    $('#addref').addEventListener('click', function () { $('#refs').insertAdjacentHTML('beforeend', refRow({ n: '', t: 'Cross-reference', v: false })); });
    $('#addspec').addEventListener('click', function () { $('#specs').insertAdjacentHTML('beforeend', specRow({ k: '', v: '' })); });
    f.addEventListener('click', function (e) { var b = e.target.closest('[data-rmrow]'); if (b) { b.closest('.row').remove(); checks(); } });
    function collect() {
      var v = function (n) { return (f.elements[n] && f.elements[n].value || '').trim(); };
      p.name = v('name'); p.cat = v('cat'); p.sku = v('sku'); p.brand = v('brand'); p.country = v('country'); p.desc = v('desc'); p.make = v('make'); p.model = v('model');
      p.codes = v('codes').split(',').map(function (s) { return s.trim(); }).filter(Boolean); p.yearFrom = v('yearFrom'); p.yearTo = v('yearTo'); p.market = v('market'); p.steering = v('steering');
      p.gas = v('gas'); p.oil = v('oil'); p.tags = v('tags').split(',').map(function (s) { return s.trim(); }).filter(Boolean); p.metaTitle = v('metaTitle'); p.metaDesc = v('metaDesc'); p.alt = v('alt');
      p.status = v('status'); p.stock = v('stock'); p.verified = f.elements.verified.checked;
      p.refs = $$('#refs .row').map(function (r) { return { n: $('[data-rn]', r).value.trim(), t: $('[data-rt]', r).value, v: $('[data-rv]', r).checked }; }).filter(function (r) { return r.n; });
      p.specs = $$('#specs .row').map(function (r) { return { k: $('[data-sk]', r).value.trim(), v: $('[data-sv]', r).value.trim() }; }).filter(function (s) { return s.k && s.v; });
      p.related = $$('#f-rel option').filter(function (o) { return o.selected; }).map(function (o) { return o.value; });
      var yf = +p.yearFrom, yt = +p.yearTo || yf; p.years = []; if (yf && yt >= yf && yt - yf < 40) for (var y = yf; y <= yt; y++) p.years.push(y);
      p.image = p.images[0] || '';
    }
    function conflicts() {
      var others = prods().filter(function (x) { return x.id !== p.id; }), out = { sku: null, refs: [] };
      if (p.sku) out.sku = others.filter(function (x) { return x.sku && x.sku.toUpperCase() === p.sku.toUpperCase(); })[0] || null;
      p.refs.forEach(function (r) { var n = M.norm(r.n); others.forEach(function (x) { (x.refs || []).forEach(function (xr) { if (M.norm(xr.n) === n && n) out.refs.push({ n: r.n, p: x }); }); }); });
      return out;
    }
    var ackRef = false;
    function checks() {
      collect();
      var c = conflicts(), L = [
        [p.images.length > 0, 'Main photo added'], [!!p.name, 'Product title'], [!!p.cat, 'Category chosen'], [p.refs.length > 0 || (p.make && p.model), 'At least one reference number, or make and model'],
        [!!p.alt || !p.images.length, 'Alt text for the main photo'], [p.metaTitle.length <= 60, 'Meta title 60 characters or less'], [p.metaDesc.length <= 160, 'Meta description 160 characters or less'],
        [!c.sku, c.sku ? 'SKU already used by “' + c.sku.name + '”' : 'SKU is unique']
      ];
      var h = L.map(function (x) { return '<li class="' + (x[0] ? 'ok' : '') + '">' + esc(x[1]) + '</li>'; }).join('');
      if (c.refs.length) h += '<li class="warn"><span>Reference <b class="mono">' + esc(c.refs[0].n) + '</b> is also on “' + esc(c.refs[0].p.name) + '”. One number can be ambiguous across markets. <label class="chk" style="margin-top:6px;color:var(--ink)"><input type="checkbox" id="ackref"' + (ackRef ? ' checked' : '') + '> I checked this is correct</label></span></li>';
      if (!p.verified) h += '<li class="warn">Not verified yet: shown with a DEMO / NOT VERIFIED label</li>';
      $('#checks').innerHTML = h;
      var a = $('#ackref'); if (a) a.addEventListener('change', function () { ackRef = a.checked; });
      // counters + serp
      $$('[data-cnt]').forEach(function (s) { var inp = s.closest('div').querySelector('.in'), n = inp.value.length, mx = +s.getAttribute('data-cnt'); s.textContent = n + '/' + mx; s.classList.toggle('over', n > mx); });
      var cn = M.catName(p.cat || ''), ttl = p.metaTitle || ((p.name || 'Product title') + ' | Mega Power');
      $('#serp').innerHTML = '<div class="u">www.megapower.com.sg › our-products › ' + esc(p.cat || 'category') + '</div><div class="h">' + esc(ttl.length > 62 ? ttl.slice(0, 60) + '…' : ttl) + '</div><div class="d">' + esc((p.metaDesc || p.desc || 'Add a meta description so Google shows a useful summary.').slice(0, 160)) + '</div>';
      return { ok: L.every(function (x) { return x[0]; }) && (!c.refs.length || ackRef), list: L, c: c };
    }
    f.addEventListener('input', checks); f.addEventListener('change', checks);
    drawGal();
    function doSave(view) {
      var r = checks();
      if (p.status === 'published' && !r.ok) { M.toast('Fix the checks on the right before publishing, or save as a draft.'); $('#checks').scrollIntoView({ behavior: 'smooth', block: 'center' }); return; }
      if (!p.name || !p.cat) { M.toast('A title and category are needed even for a draft.'); return; }
      if (r.c.sku) { M.toast('That SKU is already used. Change it before saving.'); return; }
      if (!p.created) p.created = now();
      p.updated = now();
      var all = prods(), i = all.findIndex(function (x) { return x.id === p.id; });
      if (i >= 0) all[i] = p; else all.push(p);
      if (!save(all)) return;
      audit((i >= 0 ? 'Edited ' : 'Added ') + p.name + ' (' + p.status + ')', p.id);
      M.toast('Saved. ' + (p.status === 'published' ? 'It is now in the website search. <a href="' + ROOT + 'our-products.html?q=' + encodeURIComponent((p.refs[0] || {}).n || p.name) + '" target="_blank">Search for it</a>' : 'Saved as ' + p.status + '.'), 5000);
      if (view) window.open(M.purl(p), '_blank'); else location.hash = '#edit/' + p.id;
    }
    f.addEventListener('submit', function (e) { e.preventDefault(); doSave(false); });
    $('#saveview').addEventListener('click', function () { doSave(true); });
  }

  /* ---------- CSV import ---------- */
  var SAMPLE = 'sku,title,category,make,model,oem_number,alt_numbers,brand,country,refrigerant,image_url,status\n' +
    'DEMO-CMP-001,Toyota Hiace A/C Compressor (DEMO),compressors,Toyota,Hiace,DEMO-447260-0001,,Denso,Japan,R134a,,published\n' +
    'DEMO-CMP-001,Toyota Hiace A/C Compressor second row (DEMO),compressors,Toyota,Hiace,DEMO-447260-0002,,Denso,Japan,R134a,,draft\n' +
    'DEMO-CND-002,"BMW 2 Series F45 Condenser (DEMO)",condenser,BMW,2 Series F45,8730R,,Valeo,,,,draft\n' +
    'DEMO-FAN-003,Blower motor without category (DEMO),,Honda,Civic,DEMO-79310-0003,,,,,,draft\n' +
    'DEMO-COL-004,Isuzu D-Max Cooling Coil (DEMO),cooling-coil,Isuzu,D-Max,DEMO-8980-0004,DEMO-ALT-0004,,Thailand,R134a,,draft\n';
  var FIELDS = { '': '(ignore)', sku: 'SKU', name: 'Title', cat: 'Category', make: 'Make', model: 'Model', ref: 'OEM number', alt: 'Alternate numbers', brand: 'Brand', country: 'Country', gas: 'Refrigerant', oil: 'Oil', image: 'Image URL', status: 'Status', desc: 'Description' };
  var GUESS = { sku: 'sku', title: 'name', name: 'name', product: 'name', category: 'cat', cat: 'cat', make: 'make', model: 'model', oem: 'ref', oem_number: 'ref', oemno: 'ref', part_number: 'ref', alt_numbers: 'alt', alternate: 'alt', brand: 'brand', country: 'country', refrigerant: 'gas', gas: 'gas', oil: 'oil', image: 'image', image_url: 'image', status: 'status', description: 'desc' };
  function parseCSV(t) {
    var rows = [], row = [], cell = '', q = false;
    for (var i = 0; i < t.length; i++) {
      var ch = t[i];
      if (q) { if (ch === '"') { if (t[i + 1] === '"') { cell += '"'; i++; } else q = false; } else cell += ch; }
      else if (ch === '"') q = true; else if (ch === ',') { row.push(cell); cell = ''; } else if (ch === '\n' || ch === '\r') { if (ch === '\r' && t[i + 1] === '\n') i++; row.push(cell); rows.push(row); row = []; cell = ''; } else cell += ch;
    }
    if (cell || row.length) { row.push(cell); rows.push(row); }
    return rows.filter(function (r) { return r.some(function (c) { return c.trim(); }); });
  }
  var IMP = { rows: null, head: null, map: null };
  function importer() {
    if (!can('import')) { shell('import', locked('bulk import')); return; }
    var h = '<h1>Bulk import</h1><p class="st-sub">Upload a CSV (for example the export from the current Magento admin). Nothing is overwritten: duplicates and ambiguous references wait for your approval.</p>' +
      '<div class="pan"><h2>1. Choose a file</h2><div class="toolbar"><label class="btn btn-n btn-s" style="cursor:pointer">Upload CSV<input type="file" id="csvf" accept=".csv,text/csv" hidden></label><button class="btn btn-g btn-s" id="sample">Load sample CSV (demo rows)</button></div>' +
      '<textarea class="in mono" id="csvt" style="min-height:120px;font-size:.8rem" placeholder="…or paste CSV text here">' + esc(IMP.text || '') + '</textarea><div style="margin-top:8px"><button class="btn btn-o btn-s" id="parse">Read the file</button></div></div><div id="imp2"></div>';
    shell('import', h);
    $('#sample').addEventListener('click', function () { $('#csvt').value = SAMPLE; run(); });
    $('#csvf').addEventListener('change', function () { var fl = this.files[0]; if (!fl) return; var rd = new FileReader(); rd.onload = function () { $('#csvt').value = rd.result; run(); }; rd.readAsText(fl); });
    $('#parse').addEventListener('click', run);
    function run() {
      IMP.text = $('#csvt').value;
      var rows = parseCSV(IMP.text);
      if (rows.length < 2) { M.toast('Need a header row and at least one product row.'); return; }
      IMP.head = rows[0].map(function (h) { return h.trim(); }); IMP.rows = rows.slice(1);
      IMP.map = IMP.head.map(function (h) { return GUESS[h.toLowerCase().replace(/[^a-z_]/g, '')] || ''; });
      review();
    }
    function review() {
      var catBy = {}; D.cats.forEach(function (c) { catBy[c.slug] = c.slug; catBy[c.name.toLowerCase()] = c.slug; });
      var existing = prods(), seenSku = {};
      var items = IMP.rows.map(function (r, idx) {
        var o = {}; IMP.map.forEach(function (f, i) { if (f) o[f] = (r[i] || '').trim(); });
        var issues = [], kind = 'new';
        var cat = catBy[(o.cat || '').toLowerCase()];
        if (!o.name) issues.push('No title');
        if (!cat) issues.push(o.cat ? 'Unknown category “' + o.cat + '”' : 'No category');
        if (issues.length) kind = 'invalid';
        var skuU = (o.sku || '').toUpperCase();
        if (kind !== 'invalid' && skuU) {
          if (seenSku[skuU]) { kind = 'dup'; issues.push('SKU ' + o.sku + ' repeats row ' + seenSku[skuU]); }
          else if (existing.some(function (p) { return (p.sku || '').toUpperCase() === skuU; })) { kind = 'dup'; issues.push('SKU ' + o.sku + ' already in the catalogue'); }
          seenSku[skuU] = seenSku[skuU] || idx + 2;
        }
        if (kind === 'new' && o.ref) {
          var n = M.norm(o.ref), hit = existing.filter(function (p) { return (p.refs || []).some(function (x) { return M.norm(x.n) === n; }); })[0];
          if (hit) { kind = 'ref'; issues.push('Reference ' + o.ref + ' is already on “' + hit.name + '”'); }
        }
        return { row: idx + 2, o: o, cat: cat, kind: kind, issues: issues, ok: kind === 'new' };
      });
      IMP.items = items;
      var K2 = { new: ['tag-t', 'New'], dup: ['tag-r', 'Duplicate SKU'], ref: ['tag-a', 'Reference ambiguity'], invalid: ['tag-r', 'Invalid'] };
      var counts = {}; items.forEach(function (i) { counts[i.kind] = (counts[i.kind] || 0) + 1; });
      $('#imp2').innerHTML = '<div class="pan"><h2>2. Match the columns</h2><div class="map">' + IMP.head.map(function (h, i) { return '<div><label>' + esc(h) + '</label><select class="in" data-map="' + i + '">' + Object.keys(FIELDS).map(function (k) { return '<option value="' + k + '"' + (IMP.map[i] === k ? ' selected' : '') + '>' + FIELDS[k] + '</option>'; }).join('') + '</select></div>'; }).join('') + '</div></div>' +
        '<div class="pan"><h2>3. Review ' + items.length + ' rows<span class="sp"></span>' + Object.keys(counts).map(function (k) { return '<span class="tag ' + K2[k][0] + '">' + counts[k] + ' ' + K2[k][1].toLowerCase() + '</span>'; }).join(' ') + '</h2>' +
        '<p class="note" style="margin-top:0">New rows are ticked. Rows with a duplicate SKU or a reference already in use are not ticked: tick one only after checking it. Imported rows arrive as drafts marked DEMO / NOT VERIFIED.</p>' +
        '<div class="tw"><table class="tbl"><thead><tr><th>Import</th><th>Row</th><th>Title</th><th>Category</th><th>OEM</th><th>Check</th></tr></thead><tbody>' + items.map(function (it, i) {
          return '<tr><td><input type="checkbox" data-ok="' + i + '"' + (it.ok ? ' checked' : '') + (it.kind === 'invalid' ? ' disabled' : '') + ' aria-label="Import row ' + it.row + '"></td><td class="mono">' + it.row + '</td><td>' + esc(it.o.name || '—') + '</td><td>' + esc(it.cat ? M.catName(it.cat) : it.o.cat || '—') + '</td><td class="mono">' + esc(it.o.ref || '') + '</td><td><span class="tag ' + K2[it.kind][0] + '">' + K2[it.kind][1] + '</span>' + (it.issues.length ? '<div class="note">' + esc(it.issues.join('; ')) + '</div>' : '') + (it.kind === 'dup' ? '<div class="note">If ticked, it is added as a separate draft with “-COPY” on the SKU. Nothing is overwritten.</div>' : '') + '</td></tr>';
        }).join('') + '</tbody></table></div><div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap"><button class="btn btn-o" id="doimp">Import ticked rows as drafts</button><button class="btn btn-g" id="cancelimp">Cancel</button></div></div>';
      $$('[data-map]').forEach(function (s) { s.addEventListener('change', function () { IMP.map[+s.getAttribute('data-map')] = s.value; review(); }); });
      $$('[data-ok]').forEach(function (c) { c.addEventListener('change', function () { items[+c.getAttribute('data-ok')].ok = c.checked; }); });
      $('#cancelimp').addEventListener('click', function () { IMP = { rows: null }; importer(); });
      $('#doimp').addEventListener('click', function () {
        var all = prods(), n = 0;
        items.forEach(function (it) {
          if (!it.ok || it.kind === 'invalid') return;
          var o = it.o, refs = [];
          if (o.ref) refs.push({ n: o.ref, t: 'Original OEM number', v: false });
          (o.alt || '').split(/[;|]/).map(function (s) { return s.trim(); }).filter(Boolean).forEach(function (a) { refs.push({ n: a, t: 'Cross-reference', v: false }); });
          var id = newId(); all.push({ id: id, src: 'import-demo', status: 'draft', verified: false, created: now(), name: o.name, cat: it.cat, sku: it.kind === 'dup' ? o.sku + '-COPY' : o.sku || '', make: o.make || '', model: o.model || '', codes: [], brand: o.brand || '', country: o.country || '', gas: o.gas || '', oil: o.oil || '', refs: refs, images: o.image ? [o.image] : [], image: o.image || '', desc: o.desc || '', alt: o.name, years: [], specs: [], tags: [], related: [], stock: 'hidden' });
          n++;
        });
        if (save(all)) { audit('Imported ' + n + ' row' + (n === 1 ? '' : 's') + ' from CSV as drafts'); M.toast(n + ' row' + (n === 1 ? '' : 's') + ' imported as drafts. Review and publish them from Products.', 5000); PF.st = 'draft'; PF.src = 'demo'; location.hash = '#products'; }
      });
    }
    if (IMP.rows) review();
  }

  /* ---------- leads ---------- */
  var LF = { q: '' };
  function inbox(type) {
    if (!can('leads')) { shell('leads', locked('the enquiry inbox')); return; }
    var L = leads(), c = function (t) { return L.filter(function (l) { return !t || l.type === t; }).length; };
    var tabs = [['', 'All'], ['EXPORT', 'Export'], ['SUPPLIER', 'Supplier'], ['LOCAL', 'Local workshop']];
    var h = '<h1>Enquiries</h1><p class="st-sub">Every form on the website lands here with its lead type, source page and products.</p>' +
      '<div class="pill-tabs">' + tabs.map(function (t) { return '<a href="#leads' + (t[0] ? '/' + t[0] : '') + '"' + ((type || '') === t[0] ? ' aria-current="page"' : '') + '>' + t[1] + '<b>' + c(t[0]) + '</b></a>'; }).join('') + '</div>' +
      '<div class="toolbar"><input class="in" id="lq" placeholder="Search name, company, country, part…" value="' + esc(LF.q) + '">' + (L.length ? '' : '<button class="btn btn-g btn-s" id="seed">Add 3 sample enquiries (fictional)</button>') + '</div>' +
      '<div class="pan" style="padding:6px 12px"><div class="tw"><table class="tbl rsp"><thead><tr><th>Type</th><th>Enquiry</th><th>From</th><th>Parts / need</th><th>Status</th><th>Received</th></tr></thead><tbody id="lt"></tbody></table></div></div>';
    shell('leads', h);
    function draw() {
      var q = LF.q.toLowerCase();
      var rows = L.filter(function (l) { return (!type || l.type === type) && (!q || JSON.stringify(l).toLowerCase().indexOf(q) >= 0); });
      $('#lt').innerHTML = rows.length ? rows.map(function (l) {
        var need = (l.items || []).map(function (i) { return i.name + ' × ' + i.qty; }).join(', ') || l.fields.part || l.fields.category || l.fields.categories || l.source.need || l.fields.vehicle || '';
        return '<tr><td>' + ltag(l.type) + (l.sub === 'VIN_MATCH' ? ' <span class="tag tag-a">VIN</span>' : '') + (l.sample ? ' <span class="tag tag-g">sample</span>' : '') + '</td><td><a class="t" href="#lead/' + esc(l.id) + '">' + esc(l.id) + '</a></td><td data-h="From">' + esc([l.fields.company, l.fields.name].filter(Boolean).join(' · ')) + (l.fields.country ? '<br><span class="note">' + esc(l.fields.country) + '</span>' : '') + '</td><td data-h="Need" style="max-width:280px">' + esc(need) + '</td><td>' + esc(l.status) + '</td><td data-h="Received"><span class="note">' + fmt(l.created) + '</span></td></tr>';
      }).join('') : '<tr><td colspan="6" class="empty">No enquiries yet. Send one from the website (export, supplier or workshop page) and it appears here.</td></tr>';
    }
    draw();
    $('#lq').addEventListener('input', function () { LF.q = this.value; draw(); });
    var s = $('#seed'); if (s) s.addEventListener('click', function () {
      var t = Date.now(), mk = function (id, type, f, items, mins, sub) { return { id: id, type: type, sub: sub || '', created: new Date(t - mins * 60000).toISOString(), status: 'New', fields: f, files: [], items: items, source: { page: '/export/', url: '', referrer: '', product: '', utm: '', need: '' }, tag: type, notes: [], sample: true }; };
      var b = M.byId('mp-0008');
      saveLeads([
        mk('MP-EX-S001', 'EXPORT', { name: 'Sample Buyer', company: 'Sample Parts Trading (fictional)', country: 'Malaysia', email: 'buyer@example.com', quantity: '10 pcs', destination: 'Port Klang', channel: 'Email' }, b ? [{ id: b.id, name: b.name, ref: '8730R', qty: 10, url: '/' + b.url, src: 'public' }] : [], 30),
        mk('MP-SU-S001', 'SUPPLIER', { company: 'Sample Cooling Parts Factory (fictional)', country: 'China', name: 'Sample Contact', email: 'sales@example.com', categories: 'Compressors, Condensers', moq: '100 pcs' }, [], 90),
        mk('MP-LO-S001', 'LOCAL', { company: 'Sample Motor Workshop (fictional)', name: 'Sample Mechanic', mobile: '9000 0000', vehicle: 'Mercedes C200 W205 2017', part: 'compressor', branch: 'Kaki Bukit' }, [], 150)
      ].concat(leads()));
      inbox(type);
    });
  }
  function leadView(id) {
    if (!can('leads')) { shell('leads', locked('enquiries')); return; }
    var L = leads(), l = L.filter(function (x) { return x.id === id; })[0];
    if (!l) { shell('leads', '<p class="empty">Enquiry ' + esc(id) + ' was not found in this browser. Enquiries are saved per browser in the demo.</p><a class="btn btn-g" href="#leads">Back to inbox</a>'); return; }
    var F = l.fields, lab = { name: 'Name', company: 'Company / workshop', country: 'Country', email: 'Email', mobile: 'Mobile / WhatsApp', contact: 'Email or WhatsApp', wechat: 'WeChat', category: 'Part category', categories: 'Categories offered', vehicle: 'Vehicle', vin: 'VIN / chassis', oem: 'OEM number', quantity: 'Quantity', destination: 'Destination', part: 'Part needed', branch: 'Nearest branch', supplier_type: 'Supplier type', brands: 'Brands', moq: 'MOQ', certifications: 'Certifications', markets: 'Markets', channel: 'Preferred channel', message: 'Message' };
    var dl = Object.keys(lab).filter(function (k) { return F[k]; }).map(function (k) { return '<dt>' + lab[k] + '</dt><dd' + (k === 'vin' || k === 'oem' ? ' class="mono"' : '') + '>' + esc(F[k]) + '</dd>'; }).join('');
    var mail = F.email || (F.contact && F.contact.indexOf('@') > 0 ? F.contact : '');
    var h = '<a href="#leads' + '/' + l.type + '" class="note">← ' + { EXPORT: 'Export', SUPPLIER: 'Supplier', LOCAL: 'Local workshop' }[l.type] + ' enquiries</a><h1 style="margin-top:6px">' + esc(l.id) + ' ' + ltag(l.type) + (l.sub === 'VIN_MATCH' ? ' <span class="tag tag-a">VIN match request</span>' : '') + (l.sample ? ' <span class="tag tag-g">fictional sample</span>' : '') + '</h1><p class="st-sub">Received ' + fmt(l.created) + ' · tag <span class="mono">' + esc(l.tag) + '</span></p>' +
      '<div class="ld"><div>' +
      '<div class="pan"><h2>Details</h2><dl class="kv">' + dl + (F.consent ? '<dt>Consent</dt><dd>Agreed to privacy notice</dd>' : '') + '</dl></div>' +
      '<div class="pan"><h2>Parts requested</h2>' + ((l.items || []).length ? '<table class="tbl"><thead><tr><th>Product</th><th>Ref</th><th>Qty</th><th></th></tr></thead><tbody>' + l.items.map(function (i) { var p = M.byId(i.id); return '<tr><td><span class="t">' + esc(i.name) + '</span> ' + (i.src !== 'public' ? '<span class="tag tag-r">DEMO</span>' : '') + '</td><td class="mono">' + esc(i.ref) + '</td><td>' + esc(i.qty) + '</td><td>' + (p ? '<a href="#edit/' + esc(p.id) + '">Product record</a>' : '<span class="note">record removed</span>') + '</td></tr>'; }).join('') + '</tbody></table>' : '<p class="note" style="margin:0">No catalogue items attached' + (l.source.need ? '. Sourcing request for: <b>' + esc(l.source.need) + '</b>' : '') + '.</p>') + '</div>' +
      '<div class="pan"><h2>Source</h2><dl class="kv"><dt>Page</dt><dd class="mono" style="font-size:.85rem">' + esc(l.source.page) + '</dd>' + (l.source.product ? '<dt>Product page</dt><dd>' + esc(l.source.product) + '</dd>' : '') + (l.source.need ? '<dt>No-match search</dt><dd>' + esc(l.source.need) + '</dd>' : '') + '<dt>Referrer</dt><dd>' + esc(l.source.referrer || 'direct') + '</dd>' + (l.source.utm ? '<dt>Campaign</dt><dd>' + esc(l.source.utm) + '</dd>' : '') + (l.files && l.files.length ? '<dt>Files</dt><dd>' + esc(l.files.join(', ')) + ' <span class="note">(names only in the demo)</span></dd>' : '') + '</dl></div>' +
      '</div><div>' +
      '<div class="pan"><h2>Status</h2><select class="in" id="lst">' + ['New', 'Fitment check', 'Quoted', 'Won', 'Lost', 'Spam'].map(function (s) { return '<option' + (l.status === s ? ' selected' : '') + '>' + s + '</option>'; }).join('') + '</select>' +
      (mail ? '<a class="btn btn-n btn-s" style="margin-top:12px;width:100%" href="mailto:' + esc(mail) + '?subject=' + encodeURIComponent('Mega Power enquiry ' + l.id) + '">Reply by email</a>' : '') +
      '<p class="note" style="margin-top:10px">Live site: new enquiries also email the right team and can alert sales on WhatsApp once Mega Power confirms the addresses.</p></div>' +
      '<div class="pan"><h2>Internal notes</h2><ul class="feed">' + (l.notes || []).map(function (n) { return '<li><span>' + esc(n.text) + ' <span class="note">by ' + esc(n.who) + '</span></span><time>' + fmt(n.t) + '</time></li>'; }).join('') + '</ul><textarea class="in" id="lnote" placeholder="e.g. Checked chassis, part matches" style="min-height:70px"></textarea><button class="btn btn-g btn-s" id="addnote" style="margin-top:8px">Add note</button></div>' +
      '</div></div>';
    shell('leads', h);
    $('#lst').addEventListener('change', function () { var all = leads(); all.forEach(function (x) { if (x.id === id) x.status = $('#lst').value; }); saveLeads(all); audit('Enquiry ' + id + ' set to ' + $('#lst').value, id); M.toast('Status saved.'); });
    $('#addnote').addEventListener('click', function () { var t = $('#lnote').value.trim(); if (!t) return; var all = leads(); all.forEach(function (x) { if (x.id === id) (x.notes = x.notes || []).push({ t: now(), who: ROLES[role], text: t }); }); saveLeads(all); leadView(id); });
  }

  /* ---------- migration ---------- */
  function migration() {
    if (!can('migration')) { shell('migration', locked('the migration plan')); return; }
    var O = D.old, P = prods().filter(function (p) { return p.src === 'public'; });
    var rows = P.map(function (p) { return [p.old.replace(O, '/'), '/' + p.url, 'Same URL kept', 'Built in mockup']; })
      .concat(D.cats.map(function (c) { return ['/our-products/' + c.slug + '.html', '/our-products/' + c.slug + '.html', 'Same URL kept', 'Built in mockup']; }))
      .concat([['/our-products.html', '/our-products.html', 'Same URL kept (now the search page)', 'Built in mockup'], ['/about-us/', '/about-us/', 'Same URL kept', 'Built in mockup'], ['/contact-us/', '/contact-us/', 'Same URL kept', 'Built in mockup'],
        ['/about-who-we-are/', '/about-us/', '301 redirect', 'Planned, not live'], ['/about-quality-service/', '/about-us/', '301 redirect', 'Planned, not live'], ['/our-services/', '/singapore-workshops/', '301 redirect', 'Planned, not live'],
        ['/catalogsearch/advanced/', '/our-products.html', '301 redirect', 'Planned, not live'], ['/checkout/cart/', '/rfq/', '301 redirect', 'Planned, not live'], ['/wishlist/', '/rfq/', '301 redirect', 'Planned, not live'],
        ['/customer/account/…', '/rfq/', '301 redirect (no customer data moved)', 'Planned, not live'], ['/career-opportunities/', '/contact-us/', '301 redirect (or keep page if hiring)', 'Ask owner'],
        ['/terms-conditions', '/terms-conditions/', '301 to folder URL', 'Planned, not live'], ['/privacy-policy', '/privacy-policy/', '301 to folder URL', 'Planned, not live']]);
    var steps = [['Read-only audit of the current Magento site (version, admin users, hosting, product counts)', 'Needs admin access'], ['Owner approval to move product data and photos', 'Needs owner'], ['Official product export with images, categories, attributes, SEO URLs', 'Needs admin access'],
      ['Read-only archive of the original export, with URL-to-product mapping', 'Ready to run'], ['Field mapping: make, model, years, OEM and alternate numbers kept as printed', 'Designed (see Add product)'], ['De-duplicate without losing aliases; staff approve doubtful matches', 'Designed (see Bulk import)'],
      ['Pilot import of the 13 public listings', 'Done in this mockup'], ['Full import, then counts and missing-photo report against the source', 'After export'], ['Search Console check of indexed URLs; redirects live only at launch', 'At launch']];
    var h = '<h1>Old site migration</h1><p class="st-sub">How megapower.com.sg moves over without losing products or Google rankings. Nothing on this page is live: the current website has not been touched.</p>' +
      '<div class="cols"><div class="pan"><h2>Catalogue migration steps</h2><ol style="padding-left:20px;margin:0">' + steps.map(function (s) { return '<li style="margin-bottom:8px">' + esc(s[0]) + ' <span class="tag ' + (/Done|Designed|Ready/.test(s[1]) ? 'tag-t' : 'tag-a') + '">' + esc(s[1]) + '</span></li>'; }).join('') + '</ol></div>' +
      '<div class="pan"><h2>What we know today</h2><dl class="kv"><dt>Current platform</dt><dd>Looks like Magento (URL patterns). To confirm with admin access.</dd><dt>Public listings found</dt><dd>13 (9 compressors, 2 condensers, 1 fan/motor, 1 refrigerant), read ' + esc(D.read) + '</dd><dt>Other categories</dt><dd>8 categories show no public listings; hidden products may exist</dd><dt>Customer accounts</dt><dd>Not moved unless the owner asks</dd></dl></div></div>' +
      '<div class="pan"><h2>URL map (' + rows.length + ' URLs)</h2><div class="tw"><table class="tbl"><thead><tr><th>Current URL</th><th>New URL</th><th>Action</th><th>Status</th></tr></thead><tbody>' + rows.map(function (r) { return '<tr><td class="mono" style="font-size:.8rem">' + esc(r[0]) + '</td><td class="mono" style="font-size:.8rem">' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td><td><span class="tag ' + (r[3] === 'Built in mockup' ? 'tag-t' : 'tag-a') + '">' + esc(r[3]) + '</span></td></tr>'; }).join('') + '</tbody></table></div></div>';
    shell('migration', h);
  }

  /* ---------- settings ---------- */
  var APPROVALS = ['Legal name and branding to show (Mega Power Engineering & Trading, or a Pte Ltd name)', 'Priority export countries and buyer types; Chinese language?', 'WhatsApp number(s), WeChat ID/QR, and one email per enquiry type',
    'Magento admin and hosting access, total products, hidden or archived items, photo rights', 'Show prices or stock publicly? (mockup: no prices, stock hidden)', 'VIN decoder / EPC data source, or staff-assisted matching only',
    'Exact product range (radiators, cooling, commercial and industrial vehicles?)', 'Supplier intake: MOQ, certifications, regions, purchasing email', 'Branch list, phone numbers and opening hours to show (current site and directories differ)',
    'Promote the YUKI house brand, brand logos or exhibition history?', 'Hosting, launch date, ERP or stock integration', 'Hero line “Sourced in Singapore, supplied worldwide” and other draft copy'];
  function settings() {
    if (!can('settings')) { shell('settings', locked('settings')); return; }
    var ap = LS.get(APPR, {});
    var ch = [['WhatsApp (local workshops)', 'Pending confirmation', 'Button hidden; message preview shown'], ['WhatsApp / WeChat (export)', 'Pending confirmation', 'Not shown on the website'], ['Export enquiries email', 'Pending confirmation', 'Demo inbox only'],
      ['Supplier enquiries email', 'Pending confirmation', 'Demo inbox only'], ['Main line', D.tel, 'Live on website'], ['General email', D.email, 'Live on website']];
    var R = ['View products', 'Add / edit products', 'Bulk import', 'See enquiries', 'Change settings'], rm = { admin: [1, 1, 1, 1, 1], editor: [1, 1, 1, 0, 0], sales: [1, 0, 0, 1, 0] };
    var h = '<h1>Settings &amp; approvals</h1><p class="st-sub">Contact channels, staff roles and the owner decisions needed before launch.</p>' +
      '<div class="pan"><h2>Contact channels</h2><div class="tw"><table class="tbl"><thead><tr><th>Channel</th><th>Value</th><th>On the website</th></tr></thead><tbody>' + ch.map(function (c) { return '<tr><td>' + esc(c[0]) + '</td><td>' + (/Pending/.test(c[1]) ? '<span class="tag tag-a">' + esc(c[1]) + '</span>' : esc(c[1])) + '</td><td>' + esc(c[2]) + '</td></tr>'; }).join('') + '</tbody></table></div></div>' +
      '<div class="cols"><div class="pan"><h2>Staff roles</h2><table class="tbl role-m"><thead><tr><th></th><th>Admin</th><th>Editor</th><th>Sales</th></tr></thead><tbody>' + R.map(function (r, i) { return '<tr><td>' + r + '</td>' + ['admin', 'editor', 'sales'].map(function (k) { return '<td class="' + (rm[k][i] ? 'yes">✓' : 'no">–') + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody></table><p class="note">Demo: roles switch at the top. Production: each staff member signs in, and the server checks permissions on every action, with an audit log and daily backups.</p></div>' +
      '<div class="pan"><h2>Owner approvals before launch</h2><ul class="checks" id="ap">' + APPROVALS.map(function (a, i) { return '<li class="' + (ap[i] ? 'ok' : '') + '"><label class="chk" style="color:var(--ink)"><input type="checkbox" data-ap="' + i + '"' + (ap[i] ? ' checked' : '') + '> ' + esc(a) + '</label></li>'; }).join('') + '</ul></div></div>';
    shell('settings', h);
    $$('[data-ap]').forEach(function (c) { c.addEventListener('change', function () { var a = LS.get(APPR, {}); a[c.getAttribute('data-ap')] = c.checked; LS.set(APPR, a); c.closest('li').classList.toggle('ok', c.checked); }); });
  }

  /* ---------- guide ---------- */
  function guide() {
    var h = '<h1>How-to for staff</h1><p class="st-sub">Short steps for the parts counter, on a phone or a computer.</p><div class="cols guide">' +
      '<div class="pan"><h2>Add a new product</h2><ol><li>Tap <b>Add product</b>.</li><li>Take or choose a clear photo of the part on a plain background. The first photo is the main one.</li><li>Type the title as: <i>Make Model Part - Brand</i>, for example “Toyota Hiace A/C Compressor - Denso”.</li><li>Pick the category and type the OEM number exactly as printed on the label. Add other numbers as alternates.</li><li>Fill in make, model, chassis code and years if you know them. Leave blank if unsure: never guess.</li><li>Leave it as <b>Draft</b> and save. A senior staff member checks the fitment, ticks <b>verified</b> and sets it to <b>Published</b>.</li></ol></div>' +
      '<div class="pan"><h2>Answer an enquiry</h2><ol><li>Open <b>Enquiries</b>. New ones are at the top, with a count in the menu.</li><li>Check the parts and any VIN or chassis number. Set status to <b>Fitment check</b> while you confirm.</li><li>Reply by email or the customer\'s preferred channel, then set <b>Quoted</b>.</li><li>Set <b>Won</b> or <b>Lost</b> when you know, so the sales report stays correct.</li></ol></div>' +
      '<div class="pan"><h2>Import many products</h2><ol><li>Export a CSV from the old system or a spreadsheet.</li><li>Open <b>Bulk import</b> and upload it.</li><li>Check the column matching.</li><li>Rows with a duplicate SKU or a number already in use stay unticked until you check them.</li><li>Imported rows arrive as drafts.</li></ol></div>' +
      '<div class="pan"><h2>Retire a product</h2><ol><li>In <b>Products</b>, tap <b>Archive</b>. It leaves the website but stays in the system with its history.</li><li>Tap <b>Restore</b> to bring it back.</li></ol></div></div>';
    shell('guide', h);
  }

  function router() {
    var h = (location.hash || '#overview').slice(1).split('/');
    var r = h[0];
    if (r === 'overview' || !r) overview();
    else if (r === 'products') products();
    else if (r === 'new') editor(null);
    else if (r === 'edit') editor(decodeURIComponent(h[1] || ''));
    else if (r === 'import') importer();
    else if (r === 'leads') inbox(h[1] || '');
    else if (r === 'lead') leadView(decodeURIComponent(h[1] || ''));
    else if (r === 'migration') migration();
    else if (r === 'settings') settings();
    else if (r === 'guide') guide();
    else overview();
    var m = $('#main'); if (m) m.focus && m.setAttribute('tabindex', '-1');
  }
  window.addEventListener('hashchange', router);
  router();
})();
