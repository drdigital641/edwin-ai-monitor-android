/* Autotex shop: live catalogue (Base44 database, public read) over the static baseline, search, finder, cart -> WhatsApp. No libraries. */
(function () {
  "use strict";
  var AT = window.AT; if (!AT) return;
  var R = window.AT_ROOT || "";
  var $ = function (s, el) { return (el || document).querySelector(s); };
  var $$ = function (s, el) { return Array.prototype.slice.call((el || document).querySelectorAll(s)); };
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); };
  function load(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } }
  function save(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }

  /* ---- catalogue: static baseline (data.js), replaced by the live database once it loads ---- */
  var API = "https://autotex-catalogue-05dbf5ec.base44.app/api/apps/6ae3683191b1a44205dbf5ec/entities/";
  var CACHE = "at_db_v2", TTL = 5 * 60 * 1000;
  var SIDE = { L: "Left", R: "Right", pair: "Pair" };
  var BR = {}, P = {}, C = {}, M = {}, PR = {}, MK = [], live = [], dbState = "pending", STATIC = {}, STATIC_M = {};
  AT.brands.forEach(function (b) { BR[b.id] = b; });
  AT.parts.forEach(function (p) { P[p.id] = p; });
  AT.cats.forEach(function (c) { C[c.id] = c; });
  AT.products.forEach(function (x) { STATIC[x.id] = x; });
  AT.models.forEach(function (m) { STATIC_M[m.id] = m; });
  AT.PR = PR;

  function fits(m, p) {
    if (p.need === "any") return true;
    var f = m.fuel || "petrol"; if (f === "electric") return false;
    if (p.need === "petrol") return f.indexOf("petrol") >= 0 || f.indexOf("hybrid") >= 0;
    return true;
  }
  function pub(r) { return !r.status || r.status === "published"; }
  function mlabel(m) { return BR[m.b].name + " " + m.name + (m.code ? " (" + m.code + ")" : ""); }
  function years(m) { return String(m.years || "").replace("-now", " onwards"); }
  function href(x) { return x.url ? R + x.url : R + "search/?id=" + encodeURIComponent(x.id); }
  function mhref(m) { return STATIC_M[m.id] ? R + m.b + "/" + m.id + "/" : R + "search/?m=" + encodeURIComponent(m.id); }
  function waLink(t) { return "https://wa.me/" + AT.wa + "?text=" + encodeURIComponent(t); }
  function askLink(m, p) { return waLink("Hi Autotex, how much is the " + p.name + " for my " + mlabel(m) + " " + m.years + "? Stock and price please. My car plate / chassis number is: "); }

  function setData(cars, prods) {
    var models = cars ? cars.filter(function (c) { return pub(c) && c.key && BR[c.b]; }).map(function (c) {
      return { id: c.key, b: c.b, name: c.name || "", code: c.code || "", years: c.years || "", alias: c.alias || [], fuel: c.fuel || "petrol" }; }) : AT.models;
    models.sort(function (a, b) { var x = (a.b + " " + a.name + " " + a.code).toLowerCase(), y = (b.b + " " + b.name + " " + b.code).toLowerCase(); return x < y ? -1 : x > y ? 1 : 0; });
    M = {}; models.forEach(function (m) { M[m.id] = m; });
    AT.models = models;
    var src = prods ? prods.filter(function (r) { return pub(r) && r.key && M[r.m] && (P[r.p] || r.p === "other" || r.pn); }).map(function (r) {
      var st = STATIC[r.key], pr = r.price === "" || r.price == null ? null : +r.price;
      var x = { id: r.key, m: r.m, p: P[r.p] ? r.p : "other", pn: r.pn || "", pc: r.pc || "", price: pr > 0 ? pr : null, oem: r.oem || "", stock: r.stock || "", side: r.side || "",
        note: r.note || "", photos: (r.photos || []).filter(function (s) { return typeof s === "string"; }), updated: r.updated_date || "", created: r.created_date || "" };
      if (st && st.url && st.m === x.m && st.p === x.p) x.url = st.url;
      return x; }) : AT.products.map(function (x) { var y = {}; for (var k in x) y[k] = x[k]; y.photos = x.photos || []; return y; });
    PR = {}; AT.PR = PR;
    src.forEach(function (x) {
      x.model = M[x.m];
      x.part = P[x.p] || { id: "other", name: x.pn || "Part", alias: [], side: false, unit: "piece", cat: x.pc || "", need: "any" };
      x.cat = C[x.part.cat] || { id: "", name: "", svg: (C["engine-parts"] || {}).svg };
      x.title = x.part.name + (x.side ? " (" + SIDE[x.side] + ")" : "") + " for " + mlabel(x.model);
      PR[x.id] = x;
    });
    live = src;
    MK = AT.models.map(function (m) {
      var keys = [m.name].concat(m.alias || []).map(function (k) { return norm(k).trim(); });
      norm(m.name).trim().split(" ").forEach(function (w) { if (w.length > 2 && keys.indexOf(w) < 0) keys.push(w); });
      return { m: m, keys: keys };
    });
  }

  function money(v) { v = +v; return "S$" + (v % 1 ? v.toFixed(2) : v.toLocaleString("en-SG")); }
  function showPrice(x) { return x.price != null && x.price !== "" && +x.price > 0; }
  function priceHtml(x) { return showPrice(x) ? '<span class="price" data-price="' + esc(x.id) + '">' + money(x.price) + "</span>" : '<span class="price ask" data-price="' + esc(x.id) + '">Ask for price</span>'; }

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
    var tot = 0, ask = 0;
    var rows = c.map(function (i, n) {
      var x = PR[i.id], has = showPrice(x); if (has) tot += x.price * i.q; else ask++;
      return '<li class="ci"><div><a href="' + esc(href(x)) + '"><b>' + esc(x.part.name) + (i.side ? " (" + esc(i.side) + ")" : "") + "</b></a><span>" + esc(BR[x.model.b].name + " " + x.model.name + " " + x.model.code + ", " + years(x.model)) + "</span>" +
        '<span class="ci-p">' + priceHtml(x) + "</span></div>" +
        '<div class="ci-q"><button type="button" data-cq="' + n + '" data-d="-1" aria-label="Less">−</button><b>' + i.q + '</b><button type="button" data-cq="' + n + '" data-d="1" aria-label="More">+</button>' +
        '<button type="button" class="rm" data-rm="' + n + '" aria-label="Remove">Remove</button></div></li>';
    }).join("");
    cEl.innerHTML = '<ul class="cl">' + rows + '</ul><div class="ctot"><span>Total' + (ask ? " (plus " + ask + " item" + (ask > 1 ? "s" : "") + " priced on WhatsApp)" : "") + "</span><b>" + (tot ? money(tot) : "On WhatsApp") + "</b></div>" +
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
        L.push("   Qty " + i.q + " x " + (has ? money(x.price) + "" : "price please") + (x.oem ? " · Part no. " + x.oem : "") + " · Ref " + x.id);
      });
      L.push("", "Total: " + (tot ? money(tot) + " (to confirm)" : "please quote"), "", "Name: " + (fd.get("name") || ""), "Car plate / chassis: " + (fd.get("car") || "-"), "Collection: " + fd.get("collect"));
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
  // word forms: plural -> singular, common synonyms, so different wordings land on the same part
  var SYN = { headlight: "headlamp", taillight: "taillamp", light: "lamp", disk: "disc", rotor: "disc", grill: "grille", stabiliser: "stabilizer", mounting: "mount", tyre: "tire", aircond: "aircon", ac: "aircon", hood: "bonnet" };
  function stem(w) { if (w.length > 3 && /s$/.test(w) && !/ss$/.test(w)) w = w.slice(0, -1); return SYN[w] || w; }
  function toks(x) { var o = []; norm(x).trim().split(" ").forEach(function (w) { if (w) { w = stem(w); if (o.indexOf(w) < 0) o.push(w); } }); return o; }
  function hasTok(Q, t) { if (Q.indexOf(t) >= 0) return true; if (t.length < 5) return false; for (var i = 0; i < Q.length; i++) if (Q[i].length >= 5 && lev(Q[i], t) <= 1) return true; return false; }
  // short forms people type that are not full aliases (front/rear words then pick the side)
  var XA = { "front-brake-pads": ["pad", "brake"], "rear-brake-pads": ["pad", "brake"], "front-brake-discs": ["disc"], "rear-brake-discs": ["disc"],
    "front-shock-absorber": ["absorber"], "rear-shock-absorber": ["absorber", "shock"], "headlamp": ["head lamp"], "tail-lamp": ["tail lamp", "taillamp"] };
  var STOP = ["for", "my", "the", "a", "an", "of", "and", "car", "part", "spare", "price", "how", "much", "cost", "new", "original", "oem", "genuine", "set", "left", "right", "side", "front", "rear", "back", "pair", "kia", "hyundai", "sg", "singapore", "need", "want", "buy", "replace", "replacement", "to", "with", "in", "is"];
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
    // parts: every word of a part name or alias must appear in the query, in any order ("K3 front pad" = "pad front K3")
    var Q = toks(s), ph = [];
    AT.parts.forEach(function (p) {
      var best = 0, used = null;
      [p.name].concat(p.alias || [], XA[p.id] || []).forEach(function (a) {
        var at = toks(a), ok = at.length && at.every(function (t) { return hasTok(Q, t); });
        if (ok && (at.length > best)) { best = at.length; used = at; }
      });
      if (best) ph.push({ p: p, s: best, used: used });
    });
    if (ph.length) { var t = Math.max.apply(null, ph.map(function (h) { return h.s; })); ph = ph.filter(function (h) { return h.s >= t; }); r.parts = ph.map(function (h) { return h.p; }); }
    var isRear = hasTok(Q, "rear") || hasTok(Q, "back"), isFront = hasTok(Q, "front");
    if (isRear && !isFront) { var rr = r.parts.filter(function (p) { return !/^front/.test(p.id); }); if (rr.length) r.parts = rr; }
    if (isFront && !isRear) { var ff = r.parts.filter(function (p) { return !/^rear/.test(p.id); }); if (ff.length) r.parts = ff; }
    // words we could not place (not a brand, car, year, part or filler): used to avoid showing unrelated parts
    var known = {};
    STOP.forEach(function (w) { known[w] = 1; });
    AT.brands.forEach(function (b) { known[stem(b.name.toLowerCase())] = 1; });
    r.models.forEach(function (m) { toks([m.name, m.code].concat(m.alias || []).join(" ")).forEach(function (w) { known[w] = 1; }); });
    MK.forEach(function (o) { if (r.models.indexOf(o.m) >= 0) o.keys.forEach(function (k) { toks(k).forEach(function (w) { known[w] = 1; }); }); });
    ph.forEach(function (h) { h.used.forEach(function (w) { known[w] = 1; }); });
    r.unknown = Q.filter(function (w) { return !known[w] && !/^\d+$/.test(w) && w.length > 1 && !ph.some(function (h) { return h.used.some(function (u) { return u.length >= 5 && lev(u, w) <= 1; }); }); });
    // category words ("brakes", "suspension", "body parts", "lamps")
    if (!r.parts.length) AT.cats.forEach(function (c) { var w = norm(c.name).trim().split(" ")[0].replace(/s$/, ""); if (w.length > 3 && s.indexOf(" " + w) >= 0) AT.parts.forEach(function (p) { if (p.cat === c.id) r.parts.push(p); }); });
    return r;
  }

  function ilTag(pid, alt) {
    return '<img class="il" src="' + esc(R + "assets/parts/" + pid + ".svg") + '" alt="' + esc((alt || "") + " (illustration)") + '" width="400" height="300" loading="lazy" decoding="async">';
  }
  function artHtml(x, big) {
    return '<div class="art has-il' + (big ? " big" : "") + '" data-cat="' + esc(x.part.cat) + '">' + ilTag(x.part.id, x.title) + "<span>Illustration</span></div>";
  }
  function pcard(x, showModel) {
    var needSide = x.part.side && !x.side;
    return '<article class="pc" data-pid="' + esc(x.id) + '" data-live="1"><a class="pc-a" href="' + esc(href(x)) + '">' + artHtml(x) +
      "<h3>" + esc(showModel ? x.title : x.part.name + (x.side ? " (" + SIDE[x.side] + ")" : "")) + '</h3><p class="pc-sub">' + esc(showModel ? years(x.model) : x.part.unit) + "</p></a>" +
      '<div class="pc-f"><div class="pc-p">' + priceHtml(x) + '</div><button class="btn add sm" type="button" data-add="' + esc(x.id) + '"' + (needSide ? ' data-side="1"' : "") + ">Add</button></div></article>";
  }
  var WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>';
  function askCard(m, p) {
    return '<article class="pc ask" data-live="1"><div class="pc-a"><div class="art has-il" data-cat="' + esc(p.cat) + '">' + ilTag(p.id, p.name) + "<span>Illustration</span></div><h3>" + esc(p.name) + '</h3><p class="pc-sub">' + esc(p.unit) +
      '</p></div><div class="pc-f"><div class="pc-p"><span class="price ask">Ask for price</span></div><a class="btn wa sm" href="' + esc(askLink(m, p)) + '" rel="noopener">' + WA_SVG + "Ask on WhatsApp</a></div></article>";
  }
  // every part type for a car: product cards where listed, otherwise an "Ask on WhatsApp" card
  function carListing(m) {
    var its = live.filter(function (x) { return x.m === m.id; }), out = "";
    AT.cats.forEach(function (c) {
      var cards = [];
      AT.parts.filter(function (p) { return p.cat === c.id && fits(m, p); }).forEach(function (p) {
        var xs = its.filter(function (x) { return x.p === p.id; });
        if (xs.length) xs.forEach(function (x) { cards.push(pcard(x, false)); }); else cards.push(askCard(m, p));
      });
      its.filter(function (x) { return x.p === "other" && x.part.cat === c.id; }).forEach(function (x) { cards.push(pcard(x, false)); });
      if (cards.length) out += '<section class="msec"><h2>' + esc(c.name) + '</h2><div class="pgrid">' + cards.join("") + "</div></section>";
    });
    var misc = its.filter(function (x) { return x.p === "other" && !C[x.part.cat]; });
    if (misc.length) out += '<section class="msec"><h2>More parts</h2><div class="pgrid">' + misc.map(function (x) { return pcard(x, false); }).join("") + "</div></section>";
    return out;
  }
  function search(q) {
    var r = parse(q), out = live;
    if (r.brands.length) out = out.filter(function (x) { return r.brands.indexOf(x.model.b) >= 0; });
    if (r.models.length) { var ids = r.models.map(function (m) { return m.id; }); out = out.filter(function (x) { return ids.indexOf(x.m) >= 0; }); }
    if (r.parts.length) { var pids = r.parts.map(function (p) { return p.id; }); out = out.filter(function (x) { return pids.indexOf(x.p) >= 0; }); }
    else if ((r.models.length || r.brands.length) && r.unknown.length) {
      // e.g. "K3 xyz": a car was found but the part words were not understood. Try the words as text, never show every part of the car.
      out = out.filter(function (x) { var hay = toks(x.title + " " + (x.oem || "") + " " + (x.pn || "") + " " + (x.note || "")); return r.unknown.every(function (w) { return hasTok(hay, w); }); });
    }
    if (!r.brands.length && !r.models.length && !r.parts.length) {
      var s = norm(q).trim(); out = s.length > 2 ? live.filter(function (x) { return (x.oem && norm(x.oem).indexOf(s) >= 0) || norm(x.title).indexOf(s) >= 0 || (x.pn && norm(x.pn).indexOf(s) >= 0); }) : [];
    }
    return { r: r, items: out };
  }
  AT.search = search;

  /* ---- photos: http(s) url, "b44photo:<id>" (local file if pulled at build time, else the AtPhoto record) ---- */
  var PH = {};
  function resolvePhoto(e) {
    if (!e) return Promise.resolve(null);
    if (/^https?:\/\//.test(e)) return Promise.resolve(e);
    if (e.indexOf("b44photo:") !== 0) return Promise.resolve(null);
    var id = e.slice(9);
    if (AT.photoMap && AT.photoMap[id]) return Promise.resolve(R + AT.photoMap[id]);
    if (!PH[id]) PH[id] = fetch(API + "AtPhoto?limit=200&q=" + encodeURIComponent(JSON.stringify({ group: id })), { credentials: "omit" }).then(function (r) { return r.ok ? r.json() : []; })
      .then(function (rows) {
        if (Array.isArray(rows) && rows.length) return rows.sort(function (a, b) { return a.i - b.i; }).map(function (x) { return x.data || ""; }).join("");
        return fetch(API + "AtPhoto/" + encodeURIComponent(id), { credentials: "omit" }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) { return j && j.data ? j.data : null; });
      }).catch(function () { return null; });
    return PH[id];
  }
  function showPhotos(a, x) {
    var first = x.photos && x.photos[0]; if (!first || a.getAttribute("data-ph") === first) return;
    a.setAttribute("data-ph", first);
    var go = function () { resolvePhoto(first).then(function (u) { if (!u || a.getAttribute("data-ph") !== first) return; a.classList.add("has-ph"); a.classList.remove("has-il");
      a.innerHTML = '<img src="' + esc(u) + '" alt="' + esc(x.title) + '" width="800" height="600" loading="lazy" decoding="async">'; }); };
    if ("IntersectionObserver" in window) { var o = new IntersectionObserver(function (es) { if (es[0].isIntersecting) { o.disconnect(); go(); } }, { rootMargin: "300px" }); o.observe(a); } else go();
  }
  function showThumbs(host, x) {
    var th = host.querySelector(".thumbs"); if (!th) return;
    var sig = (x.photos || []).join("|"); if (th.getAttribute("data-sig") === sig) return; th.setAttribute("data-sig", sig); th.innerHTML = "";
    if ((x.photos || []).length < 2) return;
    x.photos.forEach(function (e, i) { resolvePhoto(e).then(function (u) { if (!u || th.getAttribute("data-sig") !== sig) return; var b = document.createElement("button");
      b.type = "button"; b.setAttribute("data-full", u); b.setAttribute("aria-label", "Photo " + (i + 1)); b.innerHTML = '<img src="' + esc(u) + '" alt="" width="64" height="64" loading="lazy">'; th.appendChild(b); }); });
  }
  document.addEventListener("click", function (e) {
    var b = e.target.closest(".thumbs button[data-full]"); if (!b) return;
    var a = b.closest(".prod-art").querySelector(".art"); if (!a) return;
    a.classList.add("has-ph"); a.classList.remove("has-il"); a.removeAttribute("data-ph"); a.innerHTML = '<img src="' + esc(b.getAttribute("data-full")) + '" alt="" width="800" height="600">';
  });

  /* ---- search / detail page ---- */
  var res = $("[data-results]");
  function renderSearch() {
    if (!res) return;
    var qs = new URLSearchParams(location.search), q = qs.get("q") || "", fb = qs.get("b"), fm = qs.get("m"), fp = qs.get("p"), fid = qs.get("id");
    if (fm && fp) { var hit = live.filter(function (x) { return x.m === fm && x.p === fp; })[0]; if (hit && href(hit).indexOf("search/") < 0) { location.replace(href(hit)); return; } }
    if (fm && !fp && M[fm] && STATIC_M[fm] && dbState !== "pending") { location.replace(mhref(M[fm])); return; }
    var t0 = $("[data-sr-title]");
    if (fid) {
      if (PR[fid]) { detail(PR[fid]); return; }
      res.innerHTML = dbState === "pending" ? '<p class="muted">Loading the part…</p>' : '<div class="empty"><p>This part is not listed (any more).</p><p><a class="btn wa" href="' + waLink("Hi Autotex, I was looking at a part on your website (ref " + fid + "). Is it available? My car plate / chassis: ") + '">Ask us on WhatsApp</a></p></div>';
      return;
    }
    if (fm) {
      if (!M[fm]) { res.innerHTML = dbState === "pending" ? '<p class="muted">Loading…</p>' : '<div class="empty"><p>We could not find that car. Choose your car above, or ask us.</p><p><a class="btn wa" href="' + waLink("Hi Autotex, I need a part for my car. Model and year: ") + '">WhatsApp us</a></p></div>'; return; }
      var mm = M[fm];
      if (t0) t0.textContent = BR[mm.b].name + " " + mm.name + (mm.code ? " (" + mm.code + ")" : "") + " parts";
      res.innerHTML = '<p class="lead">' + esc(years(mm)) + " · " + esc(mm.fuel || "") + '</p><p class="fitnote"><span>Tap Ask on WhatsApp for the price and stock of any part. We check the fit with your car plate or chassis number.</span></p><div class="msecs">' + carListing(mm) + "</div>";
      return;
    }
    var items = [], head = "", o = null;
    if (q) { o = search(q); items = o.items; var inp = $(".finder input[name=q]"); if (inp && !inp.value) inp.value = q;
      var hq = $("#hq"); if (hq && !hq.value) hq.value = q;
      head = "<h2>" + items.length + " result" + (items.length === 1 ? "" : "s") + " for “" + esc(q) + "”</h2>";
      if (o.r.models.length === 1 && !o.r.parts.length) head += '<p><a class="btn ghost" href="' + esc(mhref(o.r.models[0])) + '">All parts for the ' + esc(mlabel(o.r.models[0])) + "</a></p>";
      else if (o.r.models.length > 1) head += '<p class="chips">' + o.r.models.map(function (m) { return '<a class="chip" href="?q=' + encodeURIComponent(q + " " + m.code) + '">' + esc(m.name + (m.code ? " " + m.code : "") + " (" + years(m) + ")") + "</a>"; }).join("") + "</p><p class=\"small muted\">Tap your generation to narrow it down.</p>";
    } else if (fb || fp) {
      items = live.filter(function (x) { return (!fb || x.model.b === fb) && (!fp || x.p === fp); });
      head = "<h2>" + items.length + " listed part" + (items.length === 1 ? "" : "s") + "</h2>";
    } else return;
    var html = head + (items.length ? '<div class="pgrid">' + items.slice(0, 60).map(function (x) { return pcard(x, true); }).join("") + "</div>" + (items.length > 60 ? '<p class="small">Showing 60. Add your model to narrow it down.</p>' : "") : "");
    if (!items.length) {
      if (o && o.r.models.length === 1 && o.r.parts.length) {
        var m1 = o.r.models[0], asks = o.r.parts.filter(function (p) { return fits(m1, p); }).slice(0, 6);
        if (asks.length) html += '<p class="muted">No price listed yet. Ask us and we reply with the price and stock.</p><div class="pgrid">' + asks.map(function (p) { return askCard(m1, p); }).join("") + "</div>";
      }
      if (o && o.r.unknown && o.r.unknown.length && !o.r.parts.length && o.r.models.length === 1) html += '<p><a class="btn ghost" href="' + esc(mhref(o.r.models[0])) + '">See all parts for the ' + esc(mlabel(o.r.models[0])) + "</a></p>";
      if (html.indexOf("pgrid") < 0) html += '<div class="empty"><p>No match yet. Try the car model and the part, like “Sportage brake pads”, or ask us.</p><p><a class="btn wa" href="' + waLink("Hi Autotex, I'm looking for: " + (q || "a part") + ". My car plate / chassis: ") + '">WhatsApp us</a></p></div>';
    }
    res.innerHTML = html;
    if (t0 && q) t0.textContent = "Search: " + q;
    refreshStatic();
  }

  function detail(x) {
    var m = x.model, t = $("[data-sr-title]"); if (t) t.textContent = x.part.name + " for " + mlabel(m);
    document.title = x.title + " | Autotex";
    var f = $(".hero-f.slim"); if (f) f.hidden = true;
    var side = x.side ? '<p class="sidefix"><b>Side:</b> ' + esc(SIDE[x.side]) + "</p>" : (x.part.side ? '<fieldset class="side"><legend>Side</legend><label><input type="radio" name="side" value="Left"> Left (passenger)</label><label><input type="radio" name="side" value="Right"> Right (driver)</label></fieldset>' : "");
    var msg = "Hi Autotex, I'm asking about: " + x.title + " " + m.years + ". My car plate / chassis number is: ";
    var stock = x.stock === "in" ? '<span class="stock ok">In stock</span>' : x.stock === "order" ? '<span class="stock warn">Order from Korea</span>' : x.stock === "out" ? '<span class="stock out">Out of stock</span>' : '<span class="stock">Stock checked on WhatsApp</span>';
    res.innerHTML = '<section class="prod" data-product="' + esc(x.id) + '"><div class="prod-art">' + artHtml(x, true) + '<div class="thumbs"></div></div><div class="prod-i">' +
      '<p class="fits">Fits ' + esc(mlabel(m) + ", " + years(m)) + "</p>" +
      '<div class="buy"><div class="buy-p">' + priceHtml(x) + '<span class="unit">per ' + esc(x.part.unit) + "</span></div>" + stock +
      '<form class="buy-f" data-buy2>' + side + '<div class="qty"><label>Qty</label><input name="qty" type="number" min="1" max="20" value="1" inputmode="numeric"></div><button class="btn primary big" type="submit">Add to cart</button></form>' +
      '<a class="btn wa' + (showPrice(x) ? " ghost" : "") + '" href="' + esc(waLink(msg)) + '" rel="noopener">' + WA_SVG + (showPrice(x) ? "Ask about this part" : "Ask for price on WhatsApp") + "</a></div>" +
      (x.note ? '<p class="note">' + esc(x.note) + "</p>" : "") + (x.oem ? '<p><b>Part number:</b> <span class="mono">' + esc(x.oem) + "</span></p>" : "") + "</div></section>";
    $("[data-buy2]", res).addEventListener("submit", function (e) { e.preventDefault(); var s = res.querySelector("input[name=side]:checked");
      if (res.querySelector("input[name=side]") && !s) { $(".side", res).classList.add("need"); return; }
      add(x.id, Math.max(1, +$("input[name=qty]", res).value || 1), s ? s.value : (SIDE[x.side] || "")); });
    refreshStatic();
  }

  /* ---- bring the static HTML in line with the live database ---- */
  function refreshStatic() {
    $$("[data-live]").forEach(function (el) { if (!res || !res.contains(el)) el.remove(); });
    renderLatest();
    $$("[data-ask][hidden]").forEach(function (el) { el.hidden = false; });
    // prices, stock, visibility of products already printed in the page
    $$("[data-price]").forEach(function (el) {
      var x = PR[el.getAttribute("data-price")]; if (!x) return;
      var big = el.classList.contains("big");
      if (showPrice(x)) { el.className = "price" + (big ? " big" : ""); el.textContent = money(x.price); } else { el.className = "price ask" + (big ? " big" : ""); el.textContent = "Ask for price"; }
    });
    $$("[data-stock]").forEach(function (el) {
      var x = PR[el.getAttribute("data-stock")]; if (!x) return;
      var s = { in: ["In stock", "ok"], order: ["Order from Korea", "warn"], out: ["Out of stock", "out"] }[x.stock] || ["Stock checked on WhatsApp", ""];
      el.className = "stock " + s[1]; el.textContent = s[0];
    });
    if (dbState === "done") {
      $$("[data-pid]").forEach(function (el) { if (res && res.contains(el)) return; var gone = !PR[el.getAttribute("data-pid")] && !el.hasAttribute("data-live"); el.hidden = gone; });
      $$("[data-product]").forEach(function (el) { if (res && res.contains(el)) return; var g = $(".gone", el); if (g) g.hidden = !!PR[el.getAttribute("data-product")]; var f = $(".buy", el); if (f && !PR[el.getAttribute("data-product")]) f.hidden = true; else if (f) f.hidden = false; });
    }
    $$("[data-pid], [data-product]").forEach(function (host) {
      var x = PR[host.getAttribute("data-pid") || host.getAttribute("data-product")]; if (!x) return;
      var a = $(".art", host); if (a && x.photos && x.photos.length) showPhotos(a, x);
      if (host.hasAttribute("data-product")) showThumbs(host, x);
    });
    if (dbState !== "done") return;
    // listed products that have no static page yet, and part types now listed: model pages, part pages
    var used = {};
    live.filter(function (x) { return !x.url; }).forEach(function (x) {
      var k = x.m + "|" + x.p, ask = x.p !== "other" && !used[k] ? $('[data-ask="' + k + '"]') : null;
      if (ask) {
        used[k] = 1; ask.hidden = true;
        if (ask.tagName === "TR") ask.insertAdjacentHTML("afterend", '<tr data-live="1" data-pid="' + esc(x.id) + '"><td><a href="' + esc(href(x)) + '">' + esc(x.model.name) + " <i>" + esc(x.model.code) + "</i></a><small>" + esc(years(x.model)) + "</small></td><td>" + esc(x.part.name) + (x.side ? " (" + SIDE[x.side] + ")" : "") + '</td><td class="r">' + priceHtml(x) + '</td><td class="r"><button class="btn add sm" type="button" data-add="' + esc(x.id) + '"' + (x.part.side && !x.side ? ' data-side="1"' : "") + ">Add</button></td></tr>");
        else ask.insertAdjacentHTML("afterend", pcard(x, false));
      } else extra(x);
    });
    // new cars: tiles on the home page and brand pages
    AT.models.filter(function (m) { return !STATIC_M[m.id]; }).forEach(function (m) {
      var tile = '<a class="mt" data-live="1" href="' + esc(mhref(m)) + '"><span class="mt-b">' + esc(BR[m.b].name) + "</span><b>" + esc(m.name) + (m.code ? " <i>" + esc(m.code) + "</i>" : "") + "</b><span>" + esc(years(m)) + "</span></a>";
      var g = location.pathname.match(new RegExp("/" + m.b + "/$")) ? $(".mgrid") : $('[data-pane="' + (m.b === "kia" ? "ki" : "hy") + '"]');
      if (g) g.insertAdjacentHTML("beforeend", tile);
    });
    // cars removed or hidden in the database
    $$("a.mt, .chips a.chip").forEach(function (a) { var mt = (a.getAttribute("href") || "").match(/\/(hyundai|kia)\/([a-z0-9-]+)\/$/); if (mt && STATIC_M[mt[2]] && !M[mt[2]]) a.hidden = true; else if (mt) a.hidden = false; });
    if (cEl) renderCart();
    refreshFinders();
  }
  function extra(x) {
    var mp = location.pathname.match(/\/(hyundai|kia)\/([a-z0-9-]+)\/$/);
    if (!mp || mp[2] !== x.m) return;
    var w = $(".msecs"); if (!w) return;
    var s = $("#live-extra"); if (!s) { s = document.createElement("section"); s.id = "live-extra"; s.className = "msec"; s.setAttribute("data-live", "1"); s.innerHTML = '<h2>Newly added</h2><div class="pgrid"></div>'; w.insertBefore(s, w.firstChild); }
    $(".pgrid", s).insertAdjacentHTML("beforeend", pcard(x, false));
  }

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
  var finders = [];
  $$("[data-finder]").forEach(function (f) {
    var sb = $("[data-f=b]", f), sm = $("[data-f=m]", f), sp = $("[data-f=p]", f);
    function models(keepModel, keepPart) {
      var b = sb.value, want = keepModel || sm.getAttribute("data-sel");
      sm.innerHTML = '<option value="">' + (b ? "Choose model" : "Choose brand first") + "</option>" + AT.models.filter(function (m) { return m.b === b; }).map(function (m) {
        return '<option value="' + esc(m.id) + '"' + (m.id === want ? " selected" : "") + ">" + esc(m.name + (m.code ? " " + m.code : "") + " (" + years(m) + ")") + "</option>"; }).join("");
      sm.disabled = !b; parts(keepPart);
    }
    function parts(want) {
      var m = M[sm.value];
      sp.innerHTML = '<option value="">' + (m ? "All parts for this car" : "Choose model first") + "</option>" + (m ? AT.parts.filter(function (p) { return fits(m, p); }).sort(function (a, b) { return a.name.localeCompare(b.name); })
        .map(function (p) { return '<option value="' + esc(p.id) + '"' + (p.id === want ? " selected" : "") + ">" + esc(p.name) + "</option>"; }).join("") : "");
      sp.disabled = !m;
    }
    sb.addEventListener("change", function () { sm.removeAttribute("data-sel"); models(); });
    sm.addEventListener("change", function () { parts(); });
    models();
    finders.push(function () { models(sm.value, sp.value); });
    f.addEventListener("submit", function (e) {
      var q = $("input[name=q]", f).value.trim();
      if (document.activeElement && document.activeElement.closest(".f-q") || (q && !sm.value)) { // typed search
        e.preventDefault(); location.href = R + "search/?q=" + encodeURIComponent(q); return; }
      if (sm.value) { e.preventDefault(); var hit = sp.value && live.filter(function (x) { return x.m === sm.value && x.p === sp.value; })[0];
        location.href = hit ? href(hit) : (sp.value && STATIC_M[sm.value] ? mhref(M[sm.value]) + "#p-" + sp.value : mhref(M[sm.value])); return; }
      if (!sb.value && !q) { e.preventDefault(); sb.focus(); }
      else if (sb.value && !q) { e.preventDefault(); location.href = R + sb.value + "/"; }
    });
  });
  function refreshFinders() { finders.forEach(function (fn) { fn(); }); }

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

  /* ---- "Newly added" carousel on the home page: glides on its own and loops, pauses when held or swiped ---- */
  var RM = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches, glides = [], ticking = false;
  function renderLatest() {
    var rail = $("[data-latest]"); if (!rail) return;
    var sec = rail.closest("section"), alt = $("[data-noprod]");
    if (dbState === "done") {
      var xs = live.slice().sort(function (a, b) { var x = b.created || b.updated || "", y = a.created || a.updated || ""; return x < y ? -1 : x > y ? 1 : 0; }).slice(0, 12);
      rail.innerHTML = xs.map(function (x) { return pcard(x, true); }).join("");
      sec.hidden = !xs.length; if (alt) alt.hidden = !!xs.length;
    }
    if (!sec.hidden) setTimeout(function () { glide(rail); }, 0);
  }
  function gstate(rail) { return glides.filter(function (o) { return o.r === rail; })[0]; }
  function glide(rail) {
    glides = glides.filter(function (o) { return o.r !== rail; });
    $$("[data-clone]", rail).forEach(function (c) { c.remove(); });
    rail.classList.remove("auto"); rail.scrollLeft = 0;
    var head = rail.parentNode.querySelector(".rail-nav");
    if (!rail._ev) {
      rail._ev = 1;
      var hold = function (ms) { var o = gstate(rail); if (o) o.hold = ms === Infinity ? Infinity : Date.now() + (ms || 3000); };
      var sx = 0, sy = 0, touching = false, grab = false, tm = 0;
      rail.addEventListener("touchstart", function (e) { var t = e.touches[0]; sx = t.clientX; sy = t.clientY; touching = true; grab = false;
        clearTimeout(tm); tm = setTimeout(function () { if (touching) { grab = true; hold(Infinity); } }, 350); }, { passive: true });
      rail.addEventListener("touchmove", function (e) { var t = e.touches[0], dx = Math.abs(t.clientX - sx), dy = Math.abs(t.clientY - sy);
        if (grab) { if (dy > 12 && dy > dx * 1.5) { grab = false; hold(1); } return; }
        if (dx > 8 && dx > dy) { grab = true; hold(Infinity); clearTimeout(tm); } else if (dy > 8) clearTimeout(tm); }, { passive: true });
      var end = function () { touching = false; clearTimeout(tm); if (grab) { grab = false; hold(); } };
      rail.addEventListener("touchend", end, { passive: true }); rail.addEventListener("touchcancel", end, { passive: true });
      rail.addEventListener("mouseenter", function () { hold(Infinity); }); rail.addEventListener("mouseleave", function () { hold(800); });
      rail.addEventListener("wheel", function (e) { if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) hold(); }, { passive: true });
      rail.addEventListener("focusin", function () { hold(); });
      if (head) $$(".rail-btn", head).forEach(function (b) { b.addEventListener("click", function () { hold(4000); rail.scrollBy({ left: (+b.getAttribute("data-dir")) * rail.clientWidth * 0.85, behavior: RM ? "auto" : "smooth" }); }); });
      if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { rail._vis = es[0].isIntersecting; }, { threshold: 0 }).observe(rail); else rail._vis = true;
      addEventListener("resize", function () { var o = gstate(rail); if (o) o.measure(); });
    }
    var fits = rail.scrollWidth <= rail.clientWidth + 4;
    if (head) head.hidden = fits;
    if (RM || fits) return;
    var kids = [].slice.call(rail.children);
    kids.forEach(function (k) { var c = k.cloneNode(true); c.setAttribute("aria-hidden", "true"); c.setAttribute("data-clone", "1"); c.removeAttribute("id"); c.classList.remove("rv");
      $$("a,button", c).forEach(function (a) { a.setAttribute("tabindex", "-1"); }); rail.appendChild(c); });
    rail.classList.add("auto");
    var o = { r: rail, pos: 0, hold: 0, half: 0 };
    o.measure = function () { o.half = rail.children[kids.length].offsetLeft - rail.children[0].offsetLeft; }; o.measure();
    glides.push(o);
    if (!ticking) { ticking = true; var last = 0; requestAnimationFrame(function tick(t) { var dt = last ? Math.min(64, t - last) : 16; last = t;
      glides.forEach(function (g) { var r = g.r;
        if (!r._vis || document.hidden || Date.now() < g.hold) { g.pos = r.scrollLeft; return; }
        g.pos += dt * 0.035; /* about 35px a second */
        if (g.half && g.pos >= g.half) g.pos -= g.half;
        r.scrollLeft = g.pos; });
      requestAnimationFrame(tick); }); }
  }

  /* ---- go: static baseline first, then the live database (cached 5 minutes in sessionStorage) ---- */
  setData(null, null);
  var cached = null;
  try { cached = JSON.parse(sessionStorage.getItem(CACHE)); } catch (e) {}
  function fetchAll(entity) {
    var out = [];
    function page(skip) {
      return fetch(API + entity + "?limit=500&skip=" + skip, { credentials: "omit" }).then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (rows) {
        if (!Array.isArray(rows)) throw 0; out = out.concat(rows);
        return rows.length >= 500 && skip < 20000 ? page(skip + 500) : out; });
    }
    return page(0);
  }
  function apply(d) { setData(d.cars, d.prods); dbState = "done"; renderSearch(); refreshStatic(); }
  if (cached && cached.t && Date.now() - cached.t < TTL && Array.isArray(cached.cars) && Array.isArray(cached.prods)) apply(cached);
  else {
    renderSearch(); refreshStatic();
    if (window.fetch && window.Promise) Promise.all([fetchAll("AtCar"), fetchAll("AtProduct")]).then(function (v) {
      var d = { t: Date.now(), cars: v[0], prods: v[1] };
      try { sessionStorage.setItem(CACHE, JSON.stringify(d)); } catch (e) {}
      apply(d);
    }).catch(function () { dbState = "failed"; renderSearch(); });
    else dbState = "failed";
  }
})();
