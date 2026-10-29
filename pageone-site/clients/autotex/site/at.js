/* Autotex shop: catalogue merge, search, finder, cart -> WhatsApp. No libraries. */
(function () {
  "use strict";
  var AT = window.AT; if (!AT) return;
  var R = window.AT_ROOT || "";
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  function load(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  /* ---- catalogue (+ staff changes saved in this browser by /staff/) ---- */
  var ov = load("at_catalog_v1", {}) || {};
  (ov.models || []).forEach(function (m) { if (m && m.id && m.b && !AT.models.some(function (o) { return o.id === m.id; })) AT.models.push(m); });
  var BR = {}, M = {}, P = {}, C = {};
  AT.brands.forEach(function (b) { BR[b.id] = b; });
  AT.models.forEach(function (m) { M[m.id] = m; });
  AT.parts.forEach(function (p) { P[p.id] = p; });
  AT.cats.forEach(function (c) { C[c.id] = c; });
  var list = AT.products.concat(ov.added || []).map(function (x) {
    var o = (ov.products || {})[x.id]; var y = {}; for (var k in x) y[k] = x[k];
    if (o) for (var j in o) y[j] = o[j];
    return y;
  });
  function href(x) { return x.url ? R + x.url : R + "search/?id=" + encodeURIComponent(x.id); }
  function mhref(m) { return m.custom ? R + "search/?m=" + encodeURIComponent(m.id) : R + m.b + "/" + m.id + "/"; }
  var SIDE = { L: "Left", R: "Right", pair: "Pair" };
  var PR = {};
  list.forEach(function (x) {
    x.model = M[x.m]; x.part = P[x.p] || { id: "", name: x.pn || "Part", alias: [], side: false, unit: "piece", cat: x.pc || "" };
    x.cat = C[x.part.cat] || { name: "" };
    x.title = x.part.name + " for " + (x.model ? BR[x.model.b].name + " " + x.model.name + " (" + x.model.code + ")" : "");
    PR[x.id] = x;
  });
  var live = list.filter(function (x) { return x.status !== "hidden" && x.model; });
  AT.PR = PR;

  function money(v) { v = +v; return "S$" + (v % 1 ? v.toFixed(2) : v.toLocaleString("en-SG")); }
  function showPrice(x) { return x.price != null && x.price !== "" && !(AT.live && x.sample); }
  function priceHtml(x) {
    if (!showPrice(x)) return '<span class="price ask">Ask for price</span>';
    return '<span class="price">' + money(x.price) + "</span>" + (x.sample ? '<span class="badge sample">Sample price</span>' : "");
  }
  function years(m) { return m.years.replace("-now", " onwards"); }

  // refresh prices printed in the static HTML if staff changed them in this browser
  if (ov.products) $$("[data-price]").forEach(function (el) {
    var x = PR[el.getAttribute("data-price")]; if (!x || !ov.products[x.id]) return;
    var w = document.createElement("span"); w.innerHTML = priceHtml(x);
    var b = el.nextElementSibling; if (b && b.classList.contains("sample")) b.remove();
    el.replaceWith.apply(el, Array.prototype.slice.call(w.childNodes));
  });

  /* ---- cart ---- */
  var CK = "at_cart_v1";
  function cart() { return load(CK, []) || []; }
  function setCart(c) { save(CK, c); count(); }
  function count() { var n = cart().reduce(function (a, i) { return a + (+i.q || 0); }, 0); $$("[data-cart-count]").forEach(function (b) { b.textContent = n; b.classList.toggle("on", n > 0); }); }
  function add(id, q, side) {
    var c = cart(), key = id + "|" + (side || ""), f = c.filter(function (i) { return i.k === key; })[0];
    if (f) f.q = Math.min(20, f.q + q); else c.push({ k: key, id: id, q: q, side: side || "" });
    setCart(c); toast(PR[id], q, side);
  }
  var tEl;
  function toast(x, q, side) {
    if (!tEl) { tEl = document.createElement("div"); tEl.className = "toast"; tEl.setAttribute("role", "status"); document.body.appendChild(tEl); }
    tEl.innerHTML = "<span>Added " + q + " × " + esc(x.part.name) + (side ? " (" + esc(side) + ")" : "") + "</span><a href=\"" + R + "cart/\">View cart</a>";
    tEl.classList.add("on"); clearTimeout(tEl._t); tEl._t = setTimeout(function () { tEl.classList.remove("on"); }, 3200);
  }
  count();

  // side picker for quick "Add" buttons on lamps / mirrors / suspension
  function pickSide(x, cb) {
    var d = document.createElement("div"); d.className = "sheet-bg";
    d.innerHTML = '<div class="sheet" role="dialog" aria-modal="true" aria-label="Choose side"><h3>' + esc(x.title) + '</h3><p>Which side?</p><div class="sheet-b">' +
      '<button class="btn primary" data-s="Left">Left (passenger)</button><button class="btn primary" data-s="Right">Right (driver)</button><button class="btn ghost" data-s="Both">Both sides</button></div><button class="btn ghost sm" data-s="">Cancel</button></div>';
    document.body.appendChild(d);
    d.addEventListener("click", function (e) {
      var b = e.target.closest("[data-s]"); if (!b && e.target !== d) return;
      var s = b ? b.getAttribute("data-s") : ""; d.remove();
      if (s === "Both") { cb("Left"); cb("Right"); } else if (s) cb(s);
    });
    var f = $("button", d); if (f) f.focus();
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest("[data-add]"); if (!b) return;
    e.preventDefault(); var x = PR[b.getAttribute("data-add")]; if (!x) return;
    if (x.side) add(x.id, 1, SIDE[x.side] || ""); else if (x.part.side) pickSide(x, function (s) { add(x.id, 1, s); }); else add(x.id, 1, "");
  });

  // product page form
  $$("[data-buy]").forEach(function (f) {
    var id = f.getAttribute("data-buy"), q = $("input[name=qty]", f);
    f.addEventListener("click", function (e) { var b = e.target.closest("[data-q]"); if (!b) return; q.value = Math.max(1, Math.min(20, (+q.value || 1) + +b.getAttribute("data-q"))); });
    f.addEventListener("submit", function (e) {
      e.preventDefault(); var s = f.querySelector("input[name=side]:checked");
      if (f.querySelector("input[name=side]") && !s) { var fs = $(".side", f); fs.classList.add("need"); fs.querySelector("input").focus(); return; }
      add(id, Math.max(1, Math.min(20, +q.value || 1)), s ? s.value : "");
    });
  });

  /* ---- cart page ---- */
  var cEl = $("[data-cart]");
  function renderCart() {
    var c = cart().filter(function (i) { return PR[i.id]; });
    if (!c.length) { cEl.innerHTML = '<div class="empty"><p>Your cart is empty.</p><p><a class="btn primary" href="' + R + '">Find a part</a></p></div>'; return; }
    var tot = 0, ask = 0, sample = 0;
    var rows = c.map(function (i, n) {
      var x = PR[i.id], has = showPrice(x); if (has) tot += x.price * i.q; else ask++; if (has && x.sample) sample++;
      return '<li class="ci"><div><a href="' + esc(href(x)) + '"><b>' + esc(x.part.name) + (i.side ? " (" + esc(i.side) + ")" : "") + "</b></a><span>" + esc(BR[x.model.b].name + " " + x.model.name + " " + x.model.code + ", " + years(x.model)) + "</span>" +
        '<span class="ci-p">' + priceHtml(x) + "</span></div>" +
        '<div class="ci-q"><button type="button" data-cq="' + n + '" data-d="-1" aria-label="Less">−</button><b>' + i.q + '</b><button type="button" data-cq="' + n + '" data-d="1" aria-label="More">+</button>' +
        '<button type="button" class="rm" data-rm="' + n + '" aria-label="Remove">Remove</button></div></li>';
    }).join("");
    cEl.innerHTML = '<ul class="cl">' + rows + '</ul><div class="ctot"><span>Total' + (ask ? " (plus " + ask + " item" + (ask > 1 ? "s" : "") + " priced on WhatsApp)" : "") + "</span><b>" + money(tot) + "</b></div>" +
      (sample ? '<p class="small muted">Preview: sample prices, not Autotex\'s real prices.</p>' : "") +
      '<p class="small">We confirm stock and the exact fit for your car before you pay.</p>';
    cEl._c = c;
  }
  if (cEl) {
    renderCart();
    cEl.addEventListener("click", function (e) {
      var b = e.target.closest("[data-cq],[data-rm]"); if (!b) return; var c = cEl._c;
      if (b.hasAttribute("data-rm")) c.splice(+b.getAttribute("data-rm"), 1);
      else { var i = c[+b.getAttribute("data-cq")]; i.q = Math.max(1, Math.min(20, i.q + +b.getAttribute("data-d"))); }
      setCart(c); renderCart();
    });
    var co = $("[data-checkout]");
    co.addEventListener("submit", function (e) {
      e.preventDefault(); var c = cart().filter(function (i) { return PR[i.id]; }), msg = $("[data-co-msg]");
      if (!c.length) { msg.textContent = "Your cart is empty."; return; }
      var fd = new FormData(co), tot = 0, L = ["Hi Autotex, I'd like to order:", ""];
      c.forEach(function (i, n) {
        var x = PR[i.id], has = showPrice(x); if (has) tot += x.price * i.q;
        L.push((n + 1) + ". " + x.part.name + (i.side ? " (" + i.side + ")" : "") + " - " + BR[x.model.b].name + " " + x.model.name + " " + x.model.code + " (" + x.model.years + ")");
        L.push("   Qty " + i.q + " x " + (has ? money(x.price) + (x.sample ? " (sample price)" : "") : "price please") + (x.oem ? " · Part no. " + x.oem : "") + " · Ref " + x.id);
      });
      L.push("", "Total: " + money(tot) + " (to confirm)", "", "Name: " + (fd.get("name") || ""), "Car plate / chassis: " + (fd.get("car") || "-"), "Collection: " + fd.get("collect"));
      if (fd.get("note")) L.push("Notes: " + fd.get("note"));
      var url = "https://wa.me/" + AT.wa + "?text=" + encodeURIComponent(L.join("\n"));
      if (window.p1WaTap) window.p1WaTap($("button[type=submit]", co));
      msg.textContent = "Opening WhatsApp… Your cart stays here until you clear it.";
      window.location.href = url;
    });
  }

  /* ---- search ---- */
  function norm(s) { return " " + String(s || "").toLowerCase().replace(/[()]/g, " ").replace(/[^a-z0-9\-+ ]/g, " ").replace(/-/g, " ").replace(/\s+/g, " ").trim() + " "; }
  function lev(a, b) { if (Math.abs(a.length - b.length) > 1) return 9; var d = [], i, j; for (i = 0; i <= a.length; i++) d[i] = [i]; for (j = 0; j <= b.length; j++) d[0][j] = j;
    for (i = 1; i <= a.length; i++) for (j = 1; j <= b.length; j++) d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)); return d[a.length][b.length]; }
  var MK = AT.models.map(function (m) {
    var keys = [m.name].concat(m.alias).map(function (k) { return norm(k).trim(); });
    norm(m.name).trim().split(" ").forEach(function (w) { if (w.length > 2 && keys.indexOf(w) < 0) keys.push(w); });
    return { m: m, keys: keys };
  });
  function parse(q) {
    var s = norm(q), words = s.trim().split(" "), r = { brands: [], models: [], parts: [], year: 0 };
    AT.brands.forEach(function (b) { if (s.indexOf(" " + b.name.toLowerCase() + " ") >= 0) r.brands.push(b.id); });
    var y = s.match(/ (19|20)\d\d /); if (y) r.year = +y[0];
    var hits = [];
    MK.forEach(function (o) {
      var best = 0;
      o.keys.forEach(function (k) {
        if (s.indexOf(" " + k + " ") >= 0) best = Math.max(best, k.length + 1);
        else if (k.length >= 5 && k.indexOf(" ") < 0) words.forEach(function (w) { if (w.length >= 4 && (lev(w, k) <= 1 || (w.length >= 5 && k.indexOf(w) === 0))) best = Math.max(best, k.length - 1); });
      });
      if (best) hits.push({ m: o.m, s: best });
    });
    if (hits.length) {
      var top = Math.max.apply(null, hits.map(function (h) { return h.s; }));
      r.models = hits.filter(function (h) { return h.s >= top - 1; }).map(function (h) { return h.m; });
    }
    if (r.brands.length) r.models = r.models.filter(function (m) { return r.brands.indexOf(m.b) >= 0; });
    var coded = r.models.filter(function (m) { return s.indexOf(" " + m.code.toLowerCase() + " ") >= 0; });
    if (coded.length) r.models = coded;
    if (r.year) { var yr = r.models.filter(function (m) { var p = m.years.split("-"), a = +p[0], b = p[1] === "now" ? 2100 : +p[1]; return r.year >= a && r.year <= b; }); if (yr.length) r.models = yr; }
    var ph = [];
    AT.parts.forEach(function (p) {
      var best = 0; [p.name].concat(p.alias).forEach(function (a) { var k = norm(a).trim(); if (s.indexOf(" " + k + " ") >= 0) best = Math.max(best, k.length);
        else if (k.length >= 5 && k.indexOf(" ") < 0) words.forEach(function (w) { if (w.length >= 5 && lev(w, k) <= 1) best = Math.max(best, k.length - 1); }); });
      if (best) ph.push({ p: p, s: best });
    });
    if (ph.length) { var t = Math.max.apply(null, ph.map(function (h) { return h.s; })); r.parts = ph.filter(function (h) { return h.s >= t; }).map(function (h) { return h.p; }); }
    if (s.indexOf(" rear ") >= 0 || s.indexOf(" back ") >= 0) { var rr = r.parts.filter(function (p) { return !/^front/.test(p.id); }); if (rr.length) r.parts = rr; }
    if (s.indexOf(" front ") >= 0) { var ff = r.parts.filter(function (p) { return !/^rear/.test(p.id); }); if (ff.length) r.parts = ff; }
    // category words ("brakes", "suspension", "body parts", "lamps")
    if (!r.parts.length) AT.cats.forEach(function (c) { var w = norm(c.name).trim().split(" ")[0].replace(/s$/, ""); if (w.length > 3 && s.indexOf(" " + w) >= 0) AT.parts.forEach(function (p) { if (p.cat === c.id) r.parts.push(p); }); });
    return r;
  }
  function pcard(x, showModel) {
    return '<article class="pc" data-pid="' + esc(x.id) + '"><a class="pc-a" href="' + esc(href(x)) + '"><div class="art" data-cat="' + esc(x.part.cat) + '">' + (x.cat.svg || "") + "<span>Photo coming</span></div>" +
      "<h3>" + esc(showModel ? x.title : x.part.name) + '</h3><p class="pc-sub">' + esc(showModel ? years(x.model) : x.part.unit) + "</p></a>" +
      '<div class="pc-f"><div class="pc-p">' + priceHtml(x) + '</div><button class="btn add sm" type="button" data-add="' + esc(x.id) + '">Add</button></div></article>';
  }
  function search(q) {
    var r = parse(q), out = live;
    if (r.brands.length) out = out.filter(function (x) { return r.brands.indexOf(x.model.b) >= 0; });
    if (r.models.length) { var ids = r.models.map(function (m) { return m.id; }); out = out.filter(function (x) { return ids.indexOf(x.m) >= 0; }); }
    if (r.parts.length) { var pids = r.parts.map(function (p) { return p.id; }); out = out.filter(function (x) { return pids.indexOf(x.p) >= 0; }); }
    if (!r.brands.length && !r.models.length && !r.parts.length) {
      var s = norm(q).trim(); out = s.length > 2 ? live.filter(function (x) { return (x.oem && norm(x.oem).indexOf(s) >= 0) || norm(x.title).indexOf(s) >= 0 || (x.pn && norm(x.pn).indexOf(s) >= 0); }) : [];
    }
    return { r: r, items: out };
  }
  AT.search = search;

  var res = $("[data-results]");
  if (res) {
    var qs = new URLSearchParams(location.search), q = qs.get("q") || "", fb = qs.get("b"), fm = qs.get("m"), fp = qs.get("p");
    if (fm && fp) { var hit = live.filter(function (x) { return x.m === fm && x.p === fp; })[0]; if (hit) { location.replace(href(hit)); return; } }
    if (fm && !fp && M[fm] && !M[fm].custom) { location.replace(mhref(M[fm])); return; }
    var fid = qs.get("id");
    if (fid && PR[fid]) { detail(PR[fid]); }
    else if (fm && M[fm]) { var mm = M[fm], its = live.filter(function (x) { return x.m === fm; });
      var t0 = $("[data-sr-title]"); if (t0) t0.textContent = BR[mm.b].name + " " + mm.name + (mm.code ? " (" + mm.code + ")" : "") + " parts";
      res.innerHTML = "<p class=\"lead\">" + esc(years(mm)) + " · " + esc(mm.fuel || "") + "</p>" + (its.length ? '<div class="pgrid">' + its.map(function (x) { return pcard(x, false); }).join("") + "</div>" : '<p class="muted">No parts listed for this car yet. <a href="https://wa.me/' + AT.wa + '">Ask us on WhatsApp</a>.</p>');
      photos(); }
    var items = [], head = "";
    if (q) { var o = search(q); items = o.items; var inp = $(".finder input[name=q]"); if (inp) inp.value = q;
      var hq = $("#hq"); if (hq) hq.value = q;
      head = "<h2>" + items.length + " result" + (items.length === 1 ? "" : "s") + " for “" + esc(q) + "”</h2>";
      if (o.r.models.length === 1 && !o.r.parts.length) head += '<p><a class="btn ghost" href="' + R + o.r.models[0].b + "/" + o.r.models[0].id + '/">All parts for the ' + esc(BR[o.r.models[0].b].name + " " + o.r.models[0].name + " " + o.r.models[0].code) + "</a></p>";
      else if (o.r.models.length > 1) head += '<p class="chips">' + o.r.models.map(function (m) { return '<a class="chip" href="?q=' + encodeURIComponent(q + " " + m.code) + '">' + esc(m.name + " " + m.code + " (" + years(m) + ")") + "</a>"; }).join("") + "</p><p class=\"small muted\">Tap your generation to narrow it down.</p>";
    } else if (fb || fp) {
      items = live.filter(function (x) { return (!fb || x.model.b === fb) && (!fp || x.p === fp); });
      head = "<h2>" + items.length + " parts</h2>";
    }
    if (!fid && !fm && (q || fb || fp)) {
      res.innerHTML = head + (items.length ? '<div class="pgrid">' + items.slice(0, 60).map(function (x) { return pcard(x, true); }).join("") + "</div>" + (items.length > 60 ? '<p class="small">Showing 60. Add your model to narrow it down.</p>' : "") :
        '<div class="empty"><p>No match yet. Try the car model and the part, like “Sportage brake pads”, or ask us.</p><p><a class="btn wa" href="https://wa.me/' + AT.wa + "?text=" + encodeURIComponent("Hi Autotex, I'm looking for: " + q + ". My car plate / chassis: ") + '">WhatsApp us</a></p></div>');
      var t = $("[data-sr-title]"); if (t && q) t.textContent = "Search: " + q;
      photos();
    }
  }

  function detail(x) {
    var m = x.model, t = $("[data-sr-title]"); if (t) t.textContent = x.part.name + " for " + BR[m.b].name + " " + m.name + (m.code ? " (" + m.code + ")" : "");
    document.title = x.title + " | Autotex";
    var f = $(".hero-f.slim"); if (f) f.hidden = true;
    var side = x.side ? '<p><b>Side:</b> ' + esc(SIDE[x.side] || "") + "</p>" : (x.part.side ? '<fieldset class="side"><legend>Side</legend><label><input type="radio" name="side" value="Left"> Left (passenger)</label><label><input type="radio" name="side" value="Right"> Right (driver)</label></fieldset>' : "");
    res.innerHTML = '<section class="prod" data-product="' + esc(x.id) + '"><div class="prod-art"><div class="art big" data-cat="' + esc(x.part.cat) + '">' + (x.cat.svg || "") + '<span>Photo coming</span></div><div class="thumbs"></div></div><div class="prod-i">' +
      '<p class="fits">Fits ' + esc(BR[m.b].name + " " + m.name + " " + (m.code || "") + ", " + years(m)) + "</p>" +
      '<div class="buy"><div class="buy-p">' + priceHtml(x) + '<span class="unit">per ' + esc(x.part.unit) + "</span></div>" +
      '<form class="buy-f" data-buy2>' + side + '<div class="qty"><label>Qty</label><input name="qty" type="number" min="1" max="20" value="1" inputmode="numeric"></div><button class="btn primary big" type="submit">Add to cart</button></form></div>' +
      (x.note ? '<p class="note">' + esc(x.note) + "</p>" : "") + (x.oem ? '<p><b>Part number:</b> <span class="mono">' + esc(x.oem) + "</span></p>" : "") + "</div></section>";
    $("[data-buy2]", res).addEventListener("submit", function (e) { e.preventDefault(); var s = res.querySelector("input[name=side]:checked");
      if (res.querySelector("input[name=side]") && !s) { $(".side", res).classList.add("need"); return; }
      add(x.id, Math.max(1, +$("input[name=qty]", res).value || 1), s ? s.value : (SIDE[x.side] || "")); });
    photos();
  }
  /* photos added by staff in this browser (IndexedDB at_media/photos, key "<id>:<i>") */
  var dbp;
  function db() { if (!dbp) dbp = new Promise(function (ok, no) { try { var r = indexedDB.open("at_media", 1); r.onupgradeneeded = function () { r.result.createObjectStore("photos"); }; r.onsuccess = function () { ok(r.result); }; r.onerror = no; } catch (e) { no(e); } }); return dbp; }
  function getPhoto(key) { return db().then(function (d) { return new Promise(function (ok) { try { var q = d.transaction("photos").objectStore("photos").get(key); q.onsuccess = function () { ok(q.result || null); }; q.onerror = function () { ok(null); }; } catch (e) { ok(null); } }); }); }
  function photos() {
    $$("[data-pid] .art, [data-product] .art").forEach(function (a) {
      var host = a.closest("[data-pid]") || a.closest("[data-product]"), id = host.getAttribute("data-pid") || host.getAttribute("data-product"), x = PR[id];
      if (!x || !x.photos || a._ph) return; a._ph = 1;
      getPhoto(id + ":0").then(function (u) { if (!u) return; a.classList.add("has-ph"); a.innerHTML = '<img src="' + u + '" alt="' + esc(x.title) + '" loading="lazy">'; }).catch(function () {});
      var th = host.querySelector(".thumbs");
      if (th && x.photos > 1) for (var i = 0; i < x.photos; i++) (function (i) { getPhoto(id + ":" + i).then(function (u) { if (!u) return; var b = document.createElement("button"); b.type = "button"; b.innerHTML = '<img src="' + u + '" alt="">';
        b.onclick = function () { a.innerHTML = '<img src="' + u + '" alt="' + esc(x.title) + '">'; }; th.appendChild(b); }); })(i);
    });
  }
  if (list.some(function (x) { return x.photos; })) photos();
  // staff-added cars: add their tiles to brand pages and the home page tabs
  AT.models.filter(function (m) { return m.custom; }).forEach(function (m) {
    var n = live.filter(function (x) { return x.m === m.id; }).length;
    var tile = '<a class="mt" href="' + esc(mhref(m)) + '"><span class="mt-b">' + esc(BR[m.b].name) + "</span><b>" + esc(m.name) + (m.code ? " <i>" + esc(m.code) + "</i>" : "") + "</b><span>" + esc(years(m)) + " · " + n + " parts</span></a>";
    var g = location.pathname.match(new RegExp("/" + m.b + "/$")) ? $(".mgrid") : $('[data-pane="' + (m.b === "kia" ? "ki" : "hy") + '"]');
    if (g) g.insertAdjacentHTML("beforeend", tile);
  });
  // staff-added products for this car on the static model page (preview: this browser only)
  var mp = location.pathname.match(/\/(hyundai|kia)\/([a-z0-9-]+)\/$/);
  if (mp && M[mp[2]]) { var extra = live.filter(function (x) { return x.m === mp[2] && !x.url; });
    if (extra.length) { var w = $(".msecs"); if (w) { var s = document.createElement("section"); s.className = "msec"; s.innerHTML = "<h2>Newly added</h2><div class=\"pgrid\">" + extra.map(function (x) { return pcard(x, false); }).join("") + "</div>"; w.insertBefore(s, w.firstChild); photos(); } } }

  /* ---- header search suggestions ---- */
  $$(".hd-search input, .finder input[name=q]").forEach(function (inp) {
    var box = document.createElement("div"); box.className = "sugg"; box.hidden = true; inp.parentNode.appendChild(box);
    inp.addEventListener("input", function () {
      var v = inp.value.trim(); if (v.length < 3) { box.hidden = true; return; }
      var o = search(v), it = o.items.slice(0, 6);
      if (!it.length) { box.hidden = true; return; }
      box.innerHTML = it.map(function (x) { return '<a href="' + esc(href(x)) + '"><b>' + esc(x.title) + "</b><span>" + (showPrice(x) ? money(x.price) : "Ask") + "</span></a>"; }).join("") +
        (o.items.length > 6 ? '<a class="all" href="' + R + "search/?q=" + encodeURIComponent(v) + '">See all ' + o.items.length + " results</a>" : "");
      box.hidden = false;
    });
    inp.addEventListener("blur", function () { setTimeout(function () { box.hidden = true; }, 200); });
  });

  /* ---- finder: brand -> model -> part ---- */
  $$("[data-finder]").forEach(function (f) {
    var sb = $("[data-f=b]", f), sm = $("[data-f=m]", f), sp = $("[data-f=p]", f);
    function models() {
      var b = sb.value, want = sm.getAttribute("data-sel");
      sm.innerHTML = '<option value="">' + (b ? "Choose model" : "Choose brand first") + "</option>" + AT.models.filter(function (m) { return m.b === b; }).map(function (m) {
        return '<option value="' + m.id + '"' + (m.id === want ? " selected" : "") + ">" + esc(m.name + " " + m.code + " (" + years(m) + ")") + "</option>"; }).join("");
      sm.disabled = !b; parts();
    }
    function parts() {
      var m = sm.value, have = live.filter(function (x) { return x.m === m; });
      sp.innerHTML = '<option value="">' + (m ? "All parts for this car" : "Choose model first") + "</option>" + AT.cats.map(function (c) {
        var o = have.filter(function (x) { return x.part.cat === c.id && x.p; }); if (!o.length) return "";
        return '<optgroup label="' + esc(c.name) + '">' + o.map(function (x) { return '<option value="' + x.p + '">' + esc(x.part.name) + "</option>"; }).join("") + "</optgroup>"; }).join("");
      sp.disabled = !m;
    }
    sb.addEventListener("change", function () { sm.removeAttribute("data-sel"); models(); });
    sm.addEventListener("change", parts);
    models();
    f.addEventListener("submit", function (e) {
      var q = $("input[name=q]", f).value.trim();
      if (document.activeElement && document.activeElement.closest(".f-q") || (q && !sm.value)) { // typed search
        e.preventDefault(); location.href = R + "search/?q=" + encodeURIComponent(q); return; }
      if (sm.value) { e.preventDefault(); var hit = sp.value && live.filter(function (x) { return x.m === sm.value && x.p === sp.value; })[0];
        location.href = hit ? href(hit) : mhref(M[sm.value]); return; }
      if (!sb.value && !q) { e.preventDefault(); sb.focus(); }
      else if (sb.value && !q) { e.preventDefault(); location.href = R + sb.value + "/"; }
    });
  });

  /* ---- small UI ---- */
  var bg = $(".burger"), nav = $("#nav");
  if (bg) bg.addEventListener("click", function () { var o = nav.classList.toggle("open"); bg.setAttribute("aria-expanded", o); });
  $$(".tabs [data-tab]").forEach(function (t) {
    t.addEventListener("click", function () {
      $$(".tabs [data-tab]").forEach(function (o) { o.setAttribute("aria-selected", o === t); });
      $$("[data-pane]").forEach(function (p) { p.hidden = p.getAttribute("data-pane") !== t.getAttribute("data-tab"); });
    });
  });
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } }); }, { rootMargin: "0px 0px -8% 0px" });
    $$(".reveal, .pc, .mt, .ct").forEach(function (el) { el.classList.add("rv"); io.observe(el); });
  }
})();
