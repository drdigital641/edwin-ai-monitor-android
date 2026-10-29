/* SH Auto Parts staff dashboard - DEMO. Data lives in this browser (localStorage, sh_*_v1). Go-live: real login, server database, audit log, backups. */
(function () {
  'use strict';
  var S = window.SH, D = S.D, esc = S.esc, ROOT = S.ROOT;
  var SES = 'sh_staff_v1', PIN = '2468';
  var app = document.getElementById('app');
  var state = { tab: 'overview', q: '', brand: '', part: '', status: '', shown: 40 };

  function $(s, el) { return (el || document).querySelector(s); }
  function $$(s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); }
  function sget() { try { return JSON.parse(sessionStorage.getItem(SES) || 'null'); } catch (e) { return null; } }
  function sset(v) { try { if (v) sessionStorage.setItem(SES, JSON.stringify(v)); else sessionStorage.removeItem(SES); } catch (e) { } }
  var user = sget();
  var EMB = '<svg class="em" viewBox="0 0 64 64" aria-hidden="true"><path d="M52.6 21.5A22 22 0 1 1 41.2 11.4" fill="none" stroke="#D7262E" stroke-width="7"/><path d="M38.5 7.8C47 3.6 58 5.6 62.5 12.5 55.5 9.8 48.5 10.6 43.6 15.2Z" fill="#D7262E"/><path d="M41.5 24.5C38 20.5 31 20.2 26.5 22.6 22.3 24.9 22.6 29.5 27.5 31.5L36.5 34.6C41.4 36.3 41.8 41 37.2 43.6 32.6 46.2 25 46 21.2 41.8" fill="none" stroke="#D7262E" stroke-width="6.4" stroke-linejoin="round"/></svg>';
  var LOGO = '<a class="logo" href="' + ROOT + '">' + EMB + '<span class="wm"><b>SH AUTO</b><b>PARTS</b><small>Staff</small></span></a>';

  /* ---------- login ---------- */
  function login() {
    app.innerHTML = '<div class="lg"><div class="lg-box">' + LOGO +
      '<h1>Staff login</h1><p class="mu">Demo only. Any name works. The demo PIN is <b class="pin">2468</b>. Real login is added at go-live.</p>' +
      '<form id="lf" class="form" novalidate><label>Your name<input name="n" autocomplete="name" required></label><label>PIN<input name="p" inputmode="numeric" autocomplete="off" required placeholder="demo PIN 2468"></label>' +
      '<div class="err" id="le" hidden>Enter your name and the demo PIN 2468.</div><button class="btn btn-p btn-l" type="submit">Log in</button></form>' +
      '<p class="mu small"><a href="' + ROOT + '">Back to the site</a></p></div></div>';
    $('#lf').addEventListener('submit', function (ev) {
      ev.preventDefault(); var f = ev.target;
      if (f.n.value.trim() && f.p.value.trim() === PIN) { user = { name: f.n.value.trim() }; sset(user); render(); } else $('#le').hidden = false;
    });
  }

  /* ---------- helpers ---------- */
  function fmt(t) { try { var d = new Date(t); return d.toLocaleDateString('en-SG', { day: 'numeric', month: 'short' }) + ' ' + d.toLocaleTimeString('en-SG', { hour: '2-digit', minute: '2-digit' }); } catch (e) { return t; } }
  function enqs() { return S.lsGet(S.K.enq, []); }
  function brandOpts(sel) { return D.brands.map(function (b) { return '<option value="' + b.slug + '"' + (sel === b.slug ? ' selected' : '') + '>' + esc(b.name) + '</option>'; }).join(''); }
  function partOpts(sel) { return D.parts.map(function (p) { return '<option value="' + p.slug + '"' + (sel === p.slug ? ' selected' : '') + '>' + esc(p.name) + '</option>'; }).join(''); }
  function isAdded(id) { return S.overlay().add.some(function (x) { return x.id === id; }); }
  function upsert(e) {
    var o = S.overlay();
    if (isAdded(e.id)) o.add = o.add.map(function (x) { return x.id === e.id ? e : x; });
    else if (D.entries.some(function (x) { return x.id === e.id; })) o.ov[e.id] = e;
    else o.add.push(e);
    if (!S.saveOverlay(o)) S.toast('Browser storage is full or blocked. Change not saved.');
  }
  function remove(id) {
    var o = S.overlay();
    if (isAdded(id)) o.add = o.add.filter(function (x) { return x.id !== id; });
    else { delete o.ov[id]; if (o.del.indexOf(id) < 0) o.del.push(id); }
    S.saveOverlay(o);
  }
  function titleOf(e) { var b = S.brandName(e.brand) || e.brandName, m = e.model; return (b + ' ' + (m || '') + ' ' + S.partName(e.part)).replace(/\s+/g, ' ').trim(); }

  /* ---------- shell ---------- */
  function render() {
    if (!user) return login();
    var tabs = [['overview', 'Overview'], ['catalogue', 'Catalogue'], ['enquiries', 'Enquiries'], ['data', 'Data & settings']];
    var newEnq = enqs().filter(function (x) { return !x.done; }).length;
    app.innerHTML = '<div class="st-top">' + LOGO + '<span class="sp"></span><span class="who">' + esc(user.name) + '</span><a class="btn btn-g btn-s" href="' + ROOT + '">View site</a><button class="btn btn-g btn-s" id="lo" type="button">Log out</button></div>' +
      '<div class="st-demo">Demo dashboard. Changes are saved in this browser only and show on the public pages of this preview. Real login is added at go-live.</div>' +
      '<nav class="st-tabs" role="tablist" aria-label="Dashboard">' + tabs.map(function (t) { return '<button role="tab" type="button" data-tab="' + t[0] + '" aria-selected="' + (state.tab === t[0]) + '">' + t[1] + (t[0] === 'enquiries' && newEnq ? ' <b class="dot">' + newEnq + '</b>' : '') + '</button>'; }).join('') + '</nav>' +
      '<main class="st-main" id="view"></main>';
    $('#lo').addEventListener('click', function () { user = null; sset(null); render(); });
    $$('[data-tab]').forEach(function (b) { b.addEventListener('click', function () { state.tab = b.getAttribute('data-tab'); render(); window.scrollTo(0, 0); }); });
    ({ overview: overview, catalogue: catalogue, enquiries: enquiriesView, data: dataView })[state.tab]();
  }

  /* ---------- overview ---------- */
  function overview() {
    var all = S.allEntries(true), pub = all.filter(function (e) { return e.pub !== false; }).length, smp = all.filter(function (e) { return e.sample; }).length;
    var stock = all.filter(function (e) { return e.status === 'stock'; }).length, ord = all.filter(function (e) { return e.status === 'order'; }).length;
    var ne = enqs().filter(function (x) { return !x.done; }).length;
    var tile = function (n, l, t) { return '<button class="tile" type="button" data-go="' + t + '"><b>' + n + '</b><span>' + l + '</span></button>'; };
    $('#view').innerHTML = '<h1 class="st-h">Welcome, ' + esc(user.name) + '</h1><p class="mu">This is how staff keep the catalogue up to date.</p>' +
      '<div class="tiles">' + tile(all.length, 'Catalogue entries', 'catalogue') + tile(pub, 'Published on the site', 'catalogue') + tile(smp, 'Still sample entries', 'catalogue') + tile(stock + ord, 'Marked in stock / can order', 'catalogue') + tile(ne, 'New enquiries', 'enquiries') + '</div>' +
      '<div class="cards2"><section class="card"><h2>Quick actions</h2><div class="btns"><button class="btn btn-p" data-act="add" type="button">Add an entry</button><button class="btn btn-g" data-go="enquiries" type="button">Open enquiries</button><a class="btn btn-g" href="' + ROOT + 'catalogue/">See the public catalogue</a></div></section>' +
      '<section class="card"><h2>How it works</h2><ol class="ol"><li>Search the list, then Edit an entry to set status (In stock / Can order), a photo link and an optional price.</li><li>When an entry is checked, untick &ldquo;Still a sample&rdquo;. Or confirm all samples at once.</li><li>Entries with Published off are hidden from the public site.</li></ol></section></div>' +
      '<section class="card"><h2>To confirm with the client</h2>' + todo() + '</section>';
    $$('[data-go]').forEach(function (b) { b.addEventListener('click', function () { state.tab = b.getAttribute('data-go'); render(); }); });
    $('[data-act=add]').addEventListener('click', function () { state.tab = 'catalogue'; render(); editor(null); });
  }
  function todo() {
    var items = ['WhatsApp number and phone number (set WA / PHONE in build.py; buttons then open WhatsApp with the part prefilled)', 'Email for enquiries and opening hours', 'Shop address, if different from the registered address', 'Whether parts are described as OEM, original or aftermarket (no such wording is used yet)', 'Prices: shown only when staff fill the price field', 'Stock, warranty and delivery wording', 'The real parts list (replaces the sample entries)', 'The extra brand logo shown as &ldquo;//.&rdquo; on the brand board', 'Final domain, then change BASE in build.py'];
    return '<ul class="ticks">' + items.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>';
  }

  /* ---------- catalogue ---------- */
  function filtered() {
    var all = S.allEntries(true);
    if (state.brand) all = all.filter(function (e) { return e.brand === state.brand; });
    if (state.part) all = all.filter(function (e) { return e.part === state.part; });
    if (state.status === 'hidden') all = all.filter(function (e) { return e.pub === false; });
    else if (state.status === 'sample') all = all.filter(function (e) { return e.sample; });
    else if (state.status) all = all.filter(function (e) { return (e.status || 'ask') === state.status; });
    if (state.q.trim()) {
      var r = S.search(state.q, { pool: all }); all = r.results.map(function (x) { return x.e; });
    }
    return all;
  }
  function catalogue() {
    $('#view').innerHTML = '<div class="st-bar"><h1 class="st-h">Catalogue</h1><div class="grow"></div><button class="btn btn-p" id="add" type="button">Add entry</button></div>' +
      '<div class="tool"><input class="sin2" id="sq" type="search" placeholder="Search, e.g. Tesla Model Y tail lamp" value="' + esc(state.q) + '"><select id="sb"><option value="">All brands</option>' + brandOpts(state.brand) + '</select><select id="sp"><option value="">All parts</option>' + partOpts(state.part) + '</select>' +
      '<select id="ss"><option value="">Any status</option><option value="ask"' + (state.status === 'ask' ? ' selected' : '') + '>Ask for availability</option><option value="stock"' + (state.status === 'stock' ? ' selected' : '') + '>In stock</option><option value="order"' + (state.status === 'order' ? ' selected' : '') + '>Can order</option><option value="sample"' + (state.status === 'sample' ? ' selected' : '') + '>Still sample</option><option value="hidden"' + (state.status === 'hidden' ? ' selected' : '') + '>Hidden</option></select></div>' +
      '<div id="list"></div>';
    function list() {
      var f = filtered(), sh = f.slice(0, state.shown);
      $('#list').innerHTML = '<div class="st-bar sm"><span class="mu">' + f.length + ' entries</span><div class="grow"></div><button class="btn btn-g btn-s" id="conf" type="button">Mark all samples as confirmed</button></div>' +
        (sh.length ? '<div class="rows">' + sh.map(row).join('') + '</div>' : '<p class="empty">No entries match.</p>') +
        (f.length > sh.length ? '<p class="seeall"><button class="btn btn-g" id="more" type="button">Show more (' + (f.length - sh.length) + ')</button></p>' : '');
      $('#conf').addEventListener('click', confirmAll);
      var m = $('#more'); if (m) m.addEventListener('click', function () { state.shown += 40; list(); });
    }
    list();
    var deb; $('#sq').addEventListener('input', function (ev) { state.q = ev.target.value; state.shown = 40; clearTimeout(deb); deb = setTimeout(list, 120); });
    $('#sb').addEventListener('change', function (ev) { state.brand = ev.target.value; state.shown = 40; list(); });
    $('#sp').addEventListener('change', function (ev) { state.part = ev.target.value; state.shown = 40; list(); });
    $('#ss').addEventListener('change', function (ev) { state.status = ev.target.value; state.shown = 40; list(); });
    $('#add').addEventListener('click', function () { editor(null); });
    $('#view').addEventListener('click', function (ev) {
      var b = ev.target.closest('[data-ed],[data-del],[data-pub]'); if (!b) return;
      var id = b.getAttribute('data-ed') || b.getAttribute('data-del') || b.getAttribute('data-pub');
      var e = S.allEntries(true).filter(function (x) { return x.id === id; })[0]; if (!e) return;
      if (b.hasAttribute('data-ed')) editor(e);
      else if (b.hasAttribute('data-del')) { if (window.confirm('Delete "' + e.title + '"?')) { remove(id); S.toast('Deleted.'); list(); } }
      else { e = Object.assign({}, e, { pub: e.pub === false }); upsert(e); S.toast(e.pub ? 'Published.' : 'Hidden from the public site.'); list(); }
    });
  }
  function row(e) {
    var st = e.status || 'ask';
    return '<div class="row' + (e.pub === false ? ' off' : '') + '"><div class="row-ic"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">' + (D.icons[e.part] || D.icons.other) + '</svg></div>' +
      '<div class="row-b"><b>' + esc(e.title) + '</b><span class="mu">' + esc(e.partName) + (e.side ? ' &middot; ' + esc(e.side) : '') + (e.price ? ' &middot; ' + esc(e.price) : '') + '</span>' +
      '<span class="tags"><span class="pill st-' + st + '">' + esc(D.status[st]) + '</span>' + (e.sample ? '<span class="tag">Sample</span>' : '<span class="tag ok">Confirmed</span>') + (e.pub === false ? '<span class="tag off">Hidden</span>' : '') + (e.photo ? '<span class="tag">Photo</span>' : '') + '</span></div>' +
      '<div class="row-a"><button class="btn btn-g btn-s" data-ed="' + esc(e.id) + '" type="button">Edit</button><button class="btn btn-g btn-s" data-pub="' + esc(e.id) + '" type="button">' + (e.pub === false ? 'Publish' : 'Hide') + '</button><button class="btn btn-g btn-s dng" data-del="' + esc(e.id) + '" type="button">Delete</button></div></div>';
  }
  function confirmAll() {
    var all = S.allEntries(true).filter(function (e) { return e.sample; });
    if (!all.length) return S.toast('No sample entries left.');
    if (!window.confirm('Mark ' + all.length + ' sample entries as confirmed? Only do this once staff have checked them.')) return;
    all.forEach(function (e) { upsert(Object.assign({}, e, { sample: false })); });
    S.toast(all.length + ' entries marked as confirmed.'); render();
  }

  /* ---------- editor modal ---------- */
  function editor(e) {
    var isNew = !e; e = e || { id: 'sx-' + Date.now().toString(36), brand: state.brand || 'tesla', model: '', part: state.part || 'tail-lamp', status: 'ask', sample: true, pub: true, side: '', note: '', photo: '', price: '', title: '' };
    var old = $('#ed'); if (old) old.remove();
    var m = document.createElement('div'); m.id = 'ed'; m.className = 'modal'; m.setAttribute('role', 'dialog'); m.setAttribute('aria-modal', 'true');
    m.innerHTML = '<form class="m-box form" novalidate><button class="m-x" type="button" aria-label="Close">&times;</button><h2>' + (isNew ? 'Add entry' : 'Edit entry') + '</h2>' +
      '<div class="g2"><label>Brand<select name="brand">' + brandOpts(e.brand) + '</select></label><label>Model<select name="modelsel"></select></label></div>' +
      '<label>Model, if not in the list<input name="modeltxt" placeholder="leave empty to use the list"></label>' +
      '<div class="g2"><label>Part type<select name="part">' + partOpts(e.part) + '</select></label><label>Side<input name="side" value="' + esc(e.side) + '" placeholder="e.g. Left or right - tell us"></label></div>' +
      '<label>Title <span class="mu">(empty = made from brand, model and part)</span><input name="title" value="' + esc(e.title) + '"></label>' +
      '<div class="g2"><label>Status<select name="status"><option value="ask">Ask for availability</option><option value="stock">In stock</option><option value="order">Can order</option></select></label><label>Price text <span class="mu">(shown only if filled)</span><input name="price" value="' + esc(e.price) + '" placeholder="staff choice"></label></div>' +
      '<label>Photo URL <span class="mu">(optional)</span><input name="photo" value="' + esc(e.photo) + '" placeholder="https://..."></label>' +
      '<label>Note<textarea name="note" rows="3">' + esc(e.note) + '</textarea></label>' +
      '<label class="chk"><input type="checkbox" name="pub"' + (e.pub !== false ? ' checked' : '') + '><span>Published on the public site</span></label>' +
      '<label class="chk"><input type="checkbox" name="sample"' + (e.sample ? ' checked' : '') + '><span>Still a sample (shows &ldquo;Sample listing - staff to confirm&rdquo;)</span></label>' +
      '<div class="btns"><button class="btn btn-p" type="submit">Save</button><button class="btn btn-g" type="button" data-c="1">Cancel</button></div></form>';
    document.body.appendChild(m); document.body.classList.add('noscroll');
    var f = $('form', m);
    function models() {
      var b = D.brands.filter(function (x) { return x.slug === f.brand.value; })[0], cur = e.model;
      f.modelsel.innerHTML = '<option value="">(none / ask us)</option>' + (b ? b.models.map(function (x) { return '<option value="' + esc(x.name) + '"' + (x.name === cur ? ' selected' : '') + '>' + esc(x.name) + '</option>'; }).join('') : '');
      if (cur && b && !b.models.some(function (x) { return x.name === cur; })) f.modeltxt.value = cur;
    }
    models(); f.status.value = e.status || 'ask';
    f.brand.addEventListener('change', function () { e.model = ''; models(); });
    function close() { m.remove(); document.body.classList.remove('noscroll'); }
    m.addEventListener('click', function (ev) { if (ev.target === m || ev.target.closest('.m-x,[data-c]')) close(); });
    f.addEventListener('submit', function (ev) {
      ev.preventDefault();
      var model = f.modeltxt.value.trim() || f.modelsel.value;
      var n = Object.assign({}, e, { brand: f.brand.value, brandName: S.brandName(f.brand.value), model: model, modelSlug: S.slug(model), part: f.part.value, partName: S.partName(f.part.value),
        side: f.side.value.trim(), status: f.status.value, price: f.price.value.trim(), photo: f.photo.value.trim(), note: f.note.value.trim(), pub: f.pub.checked, sample: f.sample.checked });
      n.title = f.title.value.trim() || titleOf(n);
      upsert(n); close(); S.toast('Saved.'); state.tab = 'catalogue'; render();
    });
  }

  /* ---------- enquiries ---------- */
  function enquiriesView() {
    var list = enqs();
    $('#view').innerHTML = '<h1 class="st-h">Enquiries</h1><p class="mu">From the enquiry form on this preview. Saved in this browser only.</p>' +
      (list.length ? '<div class="rows">' + list.map(function (q) {
        return '<div class="row' + (q.done ? ' off' : '') + '"><div class="row-b"><b>' + esc(q.part) + '</b><span>' + esc(q.name) + ' &middot; ' + esc(q.contact) + ' &middot; ' + (q.as === 'workshop' ? 'Workshop' : 'Car owner') + '</span>' +
          '<span class="mu">' + esc(((S.brandName(q.brand) || q.brand || '') + ' ' + (q.model || '')).trim() || 'Car not stated') + ' &middot; ' + esc(fmt(q.t)) + '</span>' + (q.note ? '<span class="mu">' + esc(q.note) + '</span>' : '') +
          '<span class="tags">' + (q.done ? '<span class="tag ok">Handled</span>' : '<span class="tag">New</span>') + '</span></div>' +
          '<div class="row-a"><button class="btn btn-g btn-s" data-done="' + esc(q.id) + '" type="button">' + (q.done ? 'Reopen' : 'Mark handled') + '</button><button class="btn btn-g btn-s dng" data-rm="' + esc(q.id) + '" type="button">Delete</button></div></div>';
      }).join('') + '</div>' : '<p class="empty">No enquiries yet. Send one from <a href="' + ROOT + 'enquiry/">the enquiry form</a> to see it here.</p>');
    $$('[data-done],[data-rm]').forEach(function (b) {
      b.addEventListener('click', function () {
        var id = b.getAttribute('data-done') || b.getAttribute('data-rm'), l = enqs();
        if (b.hasAttribute('data-done')) l = l.map(function (x) { return x.id === id ? Object.assign({}, x, { done: !x.done }) : x; });
        else l = l.filter(function (x) { return x.id !== id; });
        S.lsSet(S.K.enq, l); render();
      });
    });
  }

  /* ---------- data & settings ---------- */
  function dataView() {
    $('#view').innerHTML = '<h1 class="st-h">Data &amp; settings</h1>' +
      '<section class="card"><h2>Export / import</h2><p class="mu">Export saves your catalogue changes and enquiries as a JSON file. Import loads one back (replaces what is here).</p>' +
      '<div class="btns"><button class="btn btn-p" id="ex" type="button">Export JSON</button><label class="btn btn-g" style="cursor:pointer">Import JSON<input id="im" type="file" accept="application/json,.json" hidden></label></div></section>' +
      '<section class="card"><h2>Reset demo</h2><p class="mu">Removes all staff changes and enquiries from this browser. The public site goes back to the sample catalogue.</p><button class="btn btn-g dng" id="rs" type="button">Reset the demo</button></section>' +
      '<section class="card"><h2>Settings to confirm</h2>' + todo() + '</section>';
    $('#ex').addEventListener('click', function () {
      var blob = new Blob([JSON.stringify({ site: 'sh-auto-parts', exported: new Date().toISOString(), entries: S.overlay(), enquiries: enqs() }, null, 1)], { type: 'application/json' });
      var a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = 'sh-auto-parts-data.json'; document.body.appendChild(a); a.click(); a.remove(); S.toast('Exported.');
    });
    $('#im').addEventListener('change', function (ev) {
      var fl = ev.target.files[0]; if (!fl) return; var rd = new FileReader();
      rd.onload = function () { try { var j = JSON.parse(rd.result); if (!j || j.site !== 'sh-auto-parts') throw 0; S.saveOverlay({ ov: (j.entries && j.entries.ov) || {}, add: (j.entries && j.entries.add) || [], del: (j.entries && j.entries.del) || [] }); S.lsSet(S.K.enq, j.enquiries || []); S.toast('Imported.'); render(); } catch (e) { S.toast('That file is not an SH Auto Parts export.'); } };
      rd.readAsText(fl);
    });
    $('#rs').addEventListener('click', function () { if (window.confirm('Remove all staff changes and enquiries in this browser?')) { S.saveOverlay({ ov: {}, add: [], del: [] }); S.lsSet(S.K.enq, []); S.toast('Demo reset.'); render(); } });
  }

  render();
})();
