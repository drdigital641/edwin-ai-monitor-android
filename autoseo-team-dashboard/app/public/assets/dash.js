/* AutoSEO team dashboard (21 Nov 2026): Overview, Billing, Sales.
   ONE shared shell: header + 3-item nav, cards, step strip, pills, money format, loading / empty / error states.
   All data comes from this app's server function "admin" through window.AUTOSEO_API(action, body), which the React
   shell (src/pages/Admin.jsx) sets after Base44 sign-in. No keys, PINs, tokens or client data live in this file.
   Extension points for later (not built in v1): NEW_CLIENT, MEMO, LANG, SHARE in EXT below. */
(function () {
  "use strict";
  var EXT = { NEW_CLIENT: false, MEMO: false, LANG: false, SHARE: false };
  var CURRENCY = "MYR";   // AutoSEO's own Stripe bills its clients in RM (Edwin 20 Nov). Never Page One's SGD.
  var PAGES = [
    { path: "/", key: "overview", label: "Overview" },
    { path: "/billing", key: "billing", label: "Billing" },
    { path: "/sales", key: "sales", label: "Sales" }
  ];
  var STEPS = [["pending", "Pending"], ["preview", "Preview"], ["live", "Live"]];

  // ---------- tiny DOM helpers (textContent only: no data ever goes through innerHTML) ----------
  function el(tag, a, kids) {
    var e = document.createElement(tag);
    Object.keys(a || {}).forEach(function (k) {
      var v = a[k];
      if (v === null || v === undefined || v === false) return;
      if (k === "text") e.textContent = v;
      else if (k === "class") e.className = v;
      else if (k.slice(0, 2) === "on") e.addEventListener(k.slice(2), v);
      else e.setAttribute(k, v === true ? "" : v);
    });
    (kids || []).forEach(function (c) { if (c !== null && c !== undefined && c !== false) e.appendChild(typeof c === "string" ? document.createTextNode(c) : c); });
    return e;
  }
  var NS = "http://www.w3.org/2000/svg";
  var ICONS = {
    ext: "M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5",
    lock: "M7 11V8a5 5 0 0 1 10 0v3M6 11h12v9H6z",
    chev: "M9 5l7 7-7 7",
    gear: "M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM19.4 13a7.6 7.6 0 0 0 0-2l2-1.6-2-3.4-2.4 1a7.4 7.4 0 0 0-1.7-1L15 3.5h-4l-.4 2.5a7.4 7.4 0 0 0-1.7 1l-2.4-1-2 3.4L6.6 11a7.6 7.6 0 0 0 0 2l-2 1.6 2 3.4 2.4-1c.5.4 1.1.8 1.7 1l.4 2.5h4l.4-2.5c.6-.2 1.2-.6 1.7-1l2.4 1 2-3.4z",
    folder: "M3 6.5A1.5 1.5 0 0 1 4.5 5h4.6l2 2.2h8.4A1.5 1.5 0 0 1 21 8.7v9.8a1.5 1.5 0 0 1-1.5 1.5h-15A1.5 1.5 0 0 1 3 18.5z"
  };
  function icon(kind, cls) {
    var s = document.createElementNS(NS, "svg");
    s.setAttribute("viewBox", "0 0 24 24"); s.setAttribute("aria-hidden", "true"); if (cls) s.setAttribute("class", cls);
    var p = document.createElementNS(NS, "path"); p.setAttribute("d", ICONS[kind]);
    if (kind === "folder") p.setAttribute("fill", "currentColor");
    else { p.setAttribute("fill", "none"); p.setAttribute("stroke", "currentColor"); p.setAttribute("stroke-width", "2"); p.setAttribute("stroke-linecap", "round"); p.setAttribute("stroke-linejoin", "round"); }
    s.appendChild(p); return s;
  }
  function $(id) { return document.getElementById(id); }

  // ---------- shared formats ----------
  function money(n, cur) {
    if (n === null || n === undefined || n === "" || !isFinite(Number(n))) return "Not set";
    var c = cur || CURRENCY;
    var s = Number(n).toLocaleString("en-MY", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    return (c === "MYR" ? "RM " : c + " ") + s;
  }
  function day(iso) {
    if (!iso) return "";
    var d = new Date(iso.length === 10 ? iso + "T00:00:00" : iso);
    return isNaN(d) ? "" : d.toLocaleDateString("en-MY", { day: "numeric", month: "short", year: "numeric" });
  }
  function hostOf(u) { try { return new URL(u).host; } catch (e) { return u || ""; } }
  var today = function () { return new Date().toISOString().slice(0, 10); };

  // Billing state from OUR record only (no Stripe yet). One rule, used by Overview and Billing.
  // c.billing_hint comes from the Controller ("not_billed" for K Tech, Edwin's brief 21 Nov); our own record wins.
  function billOf(plan, c) {
    if (!plan || !plan.status) return c && c.billing_hint === "not_billed" ? { key: "notbilled", label: "Not billed" } : { key: "notset", label: "Not set" };
    if (plan.status === "not_billed") return { key: "notbilled", label: "Not billed" };
    if (plan.status === "failed") return { key: "failed", label: "Failed", alert: "failed" };
    if (plan.status === "paid") {
      if (plan.period_end && plan.period_end < today()) return { key: "due", label: "Due", alert: "lapsed" };
      return { key: "paid", label: "Paid" };
    }
    if (plan.status === "due") return { key: "due", label: "Due" };
    return { key: "notset", label: "Not set" };
  }
  function pill(key, label) { return el("span", { class: "pill p-" + key, text: label }); }

  // ---------- API ----------
  var cache = {};
  function api(action, body) {
    if (typeof window.AUTOSEO_API !== "function") return Promise.resolve({ ok: false, code: "network" });
    return Promise.resolve(window.AUTOSEO_API(action, body)).then(function (r) { return r || { ok: false, code: "server" }; }, function () { return { ok: false, code: "network" }; });
  }
  function errText(code) {
    return ({
      not_set: "Live data is not connected yet. Edwin switches the link on after the security check.",
      not_allowed: "This account is not on the AutoSEO team list. Ask Edwin to add it.",
      bad_token: "You are signed out. Sign in again.",
      network: "No connection. Check your signal and try again.",
      rate: "Too many changes at once. Wait a minute.",
      too_much: "Direct + referral can't be more than the customer price.",
      number: "Enter numbers only.",
      name: "Type a name.",
      parent: "That folder is gone. Reload the page.",
      full: "The list is full (500 people).",
      invalid: "That didn't look right. Check the fields."
    })[code] || "Something went wrong. Try again.";
  }
  function stateBox(code) {
    if (code === "not_set") return el("div", { class: "empty" }, [el("b", { text: "Not connected yet" }), errText(code)]);
    return el("div", { class: "note bad", role: "alert", text: errText(code) });
  }
  function loading(n) { var w = el("div", { class: "list", "aria-busy": "true" }); for (var i = 0; i < (n || 3); i++) w.appendChild(el("div", { class: "skel" })); return w; }

  // ---------- shell ----------
  var view = null;
  function pageOf(path) { for (var i = 0; i < PAGES.length; i++) if (PAGES[i].path === path) return PAGES[i]; return PAGES[0]; }
  function shell() {
    var hdr = $("hdr"); hdr.textContent = ""; hdr.className = "top";
    var nav = el("nav", { class: "nav", "aria-label": "Dashboard pages" }, PAGES.map(function (p) {
      return el("a", { href: p.path, "data-key": p.key, onclick: function (e) { e.preventDefault(); go(p.path); } }, [p.label]);
    }));
    hdr.appendChild(el("div", { class: "top-in" }, [
      el("div", { class: "bar" }, [
        el("p", { class: "brand" }, ["AutoSEO Team", el("small", { text: "All AutoSEO clients in one view" })]),
        el("button", { class: "out", type: "button", text: "Sign out", onclick: function () { if (window.AUTOSEO_SIGNOUT) window.AUTOSEO_SIGNOUT(); } })
      ]),
      nav
    ]));
  }
  function go(path, replace) {
    var p = pageOf(path);
    if (location.pathname !== p.path) history[replace ? "replaceState" : "pushState"]({}, "", p.path);
    document.querySelectorAll(".nav a").forEach(function (a) { if (a.getAttribute("data-key") === p.key) a.setAttribute("aria-current", "page"); else a.removeAttribute("aria-current"); });
    document.title = p.label + " | AutoSEO Team";
    view = p.key;
    var root = $("app"); root.textContent = "";
    ({ overview: overview, billing: billing, sales: sales })[p.key](root);
    window.scrollTo(0, 0);
  }
  window.addEventListener("popstate", function () { go(location.pathname, true); });

  // ---------- data ----------
  function loadClients(force) {
    if (cache.clients && !force) return Promise.resolve(cache.clients);
    return api("team_clients").then(function (r) { if (r.ok) cache.clients = r; return r; });
  }
  function loadPlans(force) {
    if (cache.plans && !force) return Promise.resolve(cache.plans);
    return api("billing_list").then(function (r) { if (r.ok) cache.plans = r; return r; });
  }
  function plansById(r) { var m = {}; ((r && r.ok && r.plans) || []).forEach(function (p) { m[p.client_id] = p; }); return m; }

  // ================= PAGE 1: Overview =================
  var f = { q: "", step: "all", bill: "all" };
  function overview(root) {
    root.appendChild(el("h1", { class: "h1", text: "Overview" }));
    root.appendChild(el("p", { class: "lede", text: "Every AutoSEO client, from new to live. Read only." }));
    var body = el("div"); body.appendChild(loading(3)); root.appendChild(body);
    Promise.all([loadClients(), loadPlans()]).then(function (res) {
      if (view !== "overview") return;
      body.textContent = "";
      var cr = res[0];
      if (!cr.ok) { body.appendChild(stateBox(cr.code)); return; }
      var plans = plansById(res[1]);
      var rows = (cr.clients || []).map(function (c) { return { c: c, b: billOf(plans[c.id], c) }; });
      body.appendChild(tilesOf(rows));
      var listBox = el("div");
      body.appendChild(toolsOf(function () { drawList(listBox, rows); }));
      body.appendChild(listBox);
      drawList(listBox, rows);
      if (cr.as_of) body.appendChild(el("p", { class: "count", text: "Numbers from the Controller, " + new Date(cr.as_of).toLocaleString("en-MY") + ". Taps are the last 30 days." }));
    });
  }
  function tilesOf(rows) {
    var n = { pending: 0, preview: 0, live: 0 }, alerts = 0;
    rows.forEach(function (r) { n[r.c.step] = (n[r.c.step] || 0) + 1; if (r.b.alert) alerts++; });
    function t(cls, v, label) { return el("div", { class: "tile" + (cls ? " " + cls : "") }, [el("b", { text: String(v) }), el("span", { text: label })]); }
    return el("div", { class: "tiles" }, [
      t("total", rows.length, rows.length === 1 ? "client" : "clients"),
      t("", n.pending, "Pending"), t("", n.preview, "Preview"), t("", n.live, "Live"),
      t(alerts ? "warn" : "", alerts, "Billing alerts")
    ]);
  }
  function chipGroup(label, opts, cur, set) {
    return el("div", { class: "chips", role: "group", "aria-label": label }, opts.map(function (o) {
      return el("button", { class: "chip", type: "button", "aria-pressed": String(cur() === o[0]), text: o[1], onclick: function (e) {
        set(o[0]); e.currentTarget.parentNode.querySelectorAll(".chip").forEach(function (b) { b.setAttribute("aria-pressed", String(b === e.currentTarget)); });
      } });
    }));
  }
  function toolsOf(redraw) {
    var s = el("input", { class: "search", type: "search", placeholder: "Search name or domain", "aria-label": "Search clients", value: f.q });
    s.addEventListener("input", function () { f.q = s.value; redraw(); });
    return el("div", { class: "tools" }, [
      s,
      chipGroup("Status", [["all", "All"], ["pending", "Pending"], ["preview", "Preview"], ["live", "Live"]], function () { return f.step; }, function (v) { f.step = v; redraw(); }),
      chipGroup("Billing", [["all", "Any billing"], ["paid", "Paid"], ["due", "Due"], ["notbilled", "Not billed"]], function () { return f.bill; }, function (v) { f.bill = v; redraw(); })
    ]);
  }
  function drawList(box, rows) {
    box.textContent = "";
    var q = f.q.trim().toLowerCase();
    var shown = rows.filter(function (r) {
      if (f.step !== "all" && r.c.step !== f.step) return false;
      if (f.bill !== "all" && r.b.key !== f.bill) return false;
      if (q && (r.c.name + " " + (r.c.golive_domain || "") + " " + hostOf(r.c.live_url) + " " + hostOf(r.c.preview_url)).toLowerCase().indexOf(q) < 0) return false;
      return true;
    });
    box.appendChild(el("p", { class: "count", role: "status", text: shown.length + " of " + rows.length + " shown" }));
    if (!shown.length) { box.appendChild(el("div", { class: "empty" }, [el("b", { text: rows.length ? "No match" : "No AutoSEO clients yet" }), rows.length ? "Try another search or filter." : "New clients appear here once they are added in the Controller."])); return; }
    box.appendChild(el("div", { class: "list" }, shown.map(function (r) { return clientCard(r.c, r.b); })));
  }
  function stepStrip(step) {
    var idx = STEPS.map(function (s) { return s[0]; }).indexOf(step);
    return el("div", { class: "steps s-" + step, role: "img", "aria-label": "Status: " + (STEPS[idx] ? STEPS[idx][1] : step) }, STEPS.map(function (s, i) {
      return el("span", { class: i <= idx ? "on" : "", text: s[1] });
    }));
  }
  var HEALTH = { ok: ["ok", "Up"], warn: ["warn", "Slow"], down: ["down", "Down"], none: ["none", "Not checked"] };
  function domainCheck(c) {
    var d = c.domain_check;
    if (!c.golive_domain) return c.step === "live" ? "No go-live domain on record" : "No domain yet";
    if (!d) return "Not checked yet";
    var a = [d.dns_ok ? "Points to our server" : "Not pointing to our server", d.https_ok ? "HTTPS OK" : "No valid HTTPS"];
    return a.join(", ") + (d.at ? " (" + day(d.at) + ")" : "");
  }
  function clientCard(c, b) {
    var h = HEALTH[c.health] || HEALTH.none;
    var t = c.taps || {};
    var links = [];
    if (c.preview_url) links.push(el("a", { class: "btn", href: c.preview_url, target: "_blank", rel: "noopener noreferrer" }, ["Preview", icon("ext")]));
    if (c.live_url) links.push(el("a", { class: "btn main", href: c.live_url, target: "_blank", rel: "noopener noreferrer" }, ["Live site", icon("ext")]));
    return el("article", { class: "card" }, [
      el("div", { class: "card-h" }, [el("h2", { class: "name", text: c.name }), pill(b.key, b.label)]),
      stepStrip(c.step),
      links.length ? el("div", { class: "links" }, links) : null,
      el("dl", { class: "facts" }, [
        el("div", { class: "wide" }, [el("dt", { text: "Go live domain" }), el("dd", { text: c.golive_domain || "Not set" })]),
        el("div", {}, [el("dt", { text: "Live switch" }), el("dd", {}, [el("span", { class: "ro", title: "Only Edwin can switch this" }, [c.golive ? "On" : "Off", icon("lock")])])]),
        el("div", {}, [el("dt", { text: "Health" }), el("dd", {}, [pill(h[0], h[1])])]),
        el("div", { class: "wide" }, [el("dt", { text: "Domain check" }), el("dd", { text: domainCheck(c) })]),
        el("div", {}, [el("dt", { text: "Taps, 30 days" }), el("dd", { class: "num", text: "WhatsApp " + (t.wa || 0) + ", Call " + (t.call || 0) + ", Other " + (t.other || 0) })]),
        el("div", {}, [el("dt", { text: "Articles" }), el("dd", { class: "num", text: String(c.articles || 0) })])
      ])
    ]);
  }

  // ================= PAGE 2: Billing (AutoSEO's own Stripe, RM) =================
  var editing = null;
  function billing(root) {
    root.appendChild(el("h1", { class: "h1", text: "Billing" }));
    root.appendChild(el("p", { class: "lede", text: "What AutoSEO bills its own clients, in RM." }));
    root.appendChild(el("p", { class: "note", text: "Stripe is not connected yet. Plans and Paid/Due below are AutoSEO's own records. Nothing here charges a card or writes to Stripe." }));
    var body = el("div"); body.appendChild(loading(2)); root.appendChild(body);
    Promise.all([loadClients(), loadPlans()]).then(function (res) { if (view === "billing") drawBilling(body, res[0], res[1]); });
  }
  function drawBilling(body, cr, pr) {
    body.textContent = "";
    if (!cr.ok) { body.appendChild(stateBox(cr.code)); return; }
    if (!pr.ok) { body.appendChild(stateBox(pr.code)); return; }
    var plans = plansById(pr);
    var rows = (cr.clients || []).filter(function (c) { return c.step === "live" || plans[c.id]; })
      .map(function (c) { return { c: c, p: plans[c.id] || null, b: billOf(plans[c.id], c) }; });
    var al = rows.filter(function (r) { return r.b.alert && !(r.p && r.p.handled_at && r.p.handled_for === (r.p.period_end || "")); });
    body.appendChild(el("h2", { class: "h2", text: "Alerts" }));
    if (!al.length) body.appendChild(el("p", { class: "count", text: "No failed or lapsed payments." }));
    else body.appendChild(el("div", { class: "alerts" }, al.map(function (r) {
      var msg = el("p", { class: "msg", role: "status" });
      return el("div", { class: "alert-row" }, [
        el("div", {}, [el("b", { text: r.c.name }), el("div", { class: "count", text: r.b.alert === "failed" ? "Payment failed" : "Paid period ended " + day(r.p.period_end) }), msg]),
        el("button", { class: "btn", type: "button", text: "Mark handled", onclick: function (e) {
          e.currentTarget.disabled = true;
          api("billing_handle", { client_id: r.c.id }).then(function (x) { if (x.ok) { cache.plans = null; reloadBilling(body); } else { msg.textContent = errText(x.code); e.target.disabled = false; } });
        } })
      ]);
    })));
    body.appendChild(el("h2", { class: "h2", text: "Live clients" }));
    if (!rows.length) { body.appendChild(el("div", { class: "empty" }, [el("b", { text: "No live clients yet" }), "Clients show here once they are Live."])); return; }
    body.appendChild(el("div", { class: "list" }, rows.map(function (r) { return planCard(r, body); })));
  }
  function reloadBilling(body) { Promise.all([loadClients(), loadPlans(true)]).then(function (res) { drawBilling(body, res[0], res[1]); }); }
  function planCard(r, body) {
    var p = r.p || {};
    var card = el("article", { class: "card" }, [
      el("div", { class: "card-h" }, [el("h2", { class: "name", text: r.c.name }), pill(r.b.key, r.b.label)]),
      el("dl", { class: "facts", style: "margin-top:10px" }, [
        el("div", {}, [el("dt", { text: "Plan" }), el("dd", { text: p.plan || "Not set" })]),
        el("div", {}, [el("dt", { text: "Amount" }), el("dd", {}, [r.b.key === "notbilled" ? "None" : (p.amount === null || p.amount === undefined || p.amount === "") ? "Not set" : el("span", { class: "money", text: money(p.amount, p.currency || CURRENCY) })])]),
        el("div", { class: "wide" }, [el("dt", { text: "Period" }), el("dd", { text: p.period_start || p.period_end ? (day(p.period_start) || "?") + " to " + (day(p.period_end) || "?") : "Not set" })])
      ]),
      el("div", { class: "acts" }, [
        el("button", { class: "btn main", type: "button", text: "Edit plan", onclick: function () { editing = r.c.id; reloadBilling(body); } }),
        el("button", { class: "btn", type: "button", disabled: true, text: "Create payment link" }),
        el("button", { class: "btn", type: "button", disabled: true, text: "See invoices" })
      ]),
      el("p", { class: "stripe-off", text: "Payment link and invoices wait for AutoSEO's Stripe connection." })
    ]);
    if (editing === r.c.id) card.appendChild(planForm(r, body));
    return card;
  }
  function planForm(r, body) {
    var p = r.p || {};
    var plan = el("input", { type: "text", maxlength: "60", value: p.plan || "", placeholder: "e.g. Monthly SEO" });
    var amt = el("input", { type: "number", inputmode: "decimal", min: "0", step: "0.01", value: p.amount === undefined || p.amount === null ? "" : String(p.amount) });
    var st = el("select", {}, [["", "Not set"], ["paid", "Paid"], ["due", "Due"], ["failed", "Failed"], ["not_billed", "Not billed"]].map(function (o) { return el("option", { value: o[0], selected: (p.status || "") === o[0], text: o[1] }); }));
    var ps = el("input", { type: "date", value: p.period_start || "" }), pe = el("input", { type: "date", value: p.period_end || "" });
    var msg = el("p", { class: "msg", role: "status" });
    var save = el("button", { class: "btn main", type: "button", text: "Save" });
    save.addEventListener("click", function () {
      var a = amt.value === "" ? null : Number(amt.value);
      if (a !== null && (!isFinite(a) || a < 0)) { msg.textContent = errText("number"); return; }
      if (ps.value && pe.value && pe.value < ps.value) { msg.textContent = "The period end is before its start."; return; }
      save.disabled = true; msg.textContent = "";
      api("billing_save", { client_id: r.c.id, plan: plan.value.trim(), amount: a, status: st.value, period_start: ps.value, period_end: pe.value }).then(function (x) {
        if (x.ok) { editing = null; cache.plans = null; reloadBilling(body); } else { save.disabled = false; msg.textContent = errText(x.code); }
      });
    });
    return el("div", { class: "form" }, [
      el("label", {}, ["Plan name", plan]),
      el("div", { class: "row2" }, [el("label", {}, ["Amount (RM)", amt]), el("label", {}, ["Status", st])]),
      el("div", { class: "row2" }, [el("label", {}, ["Period start", ps]), el("label", {}, ["Period end", pe])]),
      el("div", { class: "acts" }, [save, el("button", { class: "btn", type: "button", text: "Cancel", onclick: function () { editing = null; reloadBilling(body); } })]),
      msg
    ]);
  }

  // ================= PAGE 3: Sales network (same SalesNode data as autoseo.my/sales) =================
  var S = { nodes: [], split: { customer: 300, direct: 60, referral: 40 }, open: {}, ui: null, setOpen: false };
  function keep() { return S.split.customer - S.split.direct - S.split.referral; }
  function rm(n) { return money(n, "MYR").replace(".00", ""); }
  function byId(id) { for (var i = 0; i < S.nodes.length; i++) if (S.nodes[i].id === id) return S.nodes[i]; return null; }
  function centre() { for (var i = 0; i < S.nodes.length; i++) if (S.nodes[i].role === "centre") return S.nodes[i]; return S.nodes[0]; }
  function kids(id) { return S.nodes.filter(function (n) { return n.parentId === id; }); }
  // Every person under AutoSEO.my is one sale. Parent earns Direct, grandparent earns Referral, nothing above 2 levels;
  // any share with nobody to receive it stays with AutoSEO. Same rule as the standalone /sales page.
  function calc() {
    var c = centre(), per = {}, keeps = 0, p1 = 0, p2 = 0, n1 = 0, n2 = 0, people = 0, sp = S.split;
    S.nodes.forEach(function (n) { per[n.id] = { d: 0, g: 0, earns: 0 }; });
    S.nodes.forEach(function (n) {
      if (n.id === c.id) return;
      people++; keeps += keep();
      var par = byId(n.parentId);
      if (!par || par.id === c.id) { keeps += sp.direct + sp.referral; return; }
      per[par.id].d++; per[par.id].earns += sp.direct; p1 += sp.direct; n1++;
      var gp = byId(par.parentId);
      if (!gp || gp.id === c.id) { keeps += sp.referral; return; }
      per[gp.id].g++; per[gp.id].earns += sp.referral; p2 += sp.referral; n2++;
    });
    var r = function (x) { return Math.round(x * 100) / 100; };
    return { per: per, people: people, sales: r(people * sp.customer), p1: r(p1), p2: r(p2), n1: n1, n2: n2, paid: r(p1 + p2), keeps: r(keeps) };
  }
  function sales(root) {
    root.appendChild(el("h1", { class: "h1", text: "Sales network" }));
    root.appendChild(el("p", { class: "lede", text: "Who sold to whom, and what each person earns." }));
    var body = el("div"); body.appendChild(loading(1)); root.appendChild(body);
    loadSales(body);
  }
  function loadSales(body) {
    return api("sales_data").then(function (r) {
      if (view !== "sales") return;
      if (!r.ok) { body.textContent = ""; body.appendChild(stateBox(r.code)); return; }
      S.nodes = r.nodes || [];
      if (r.settings) S.split = { customer: Number(r.settings.customer), direct: Number(r.settings.direct), referral: Number(r.settings.referral) };
      drawSales(body);
    });
  }
  function drawSales(body) {
    body.textContent = "";
    var sp = S.split;
    body.appendChild(el("div", { class: "split" }, [
      el("p", {}, ["Customer pays ", el("b", { text: rm(sp.customer) }), ". Direct ", el("b", { text: rm(sp.direct) }), ", Referral ", el("b", { text: rm(sp.referral) }), ", AutoSEO keeps ", el("b", { text: rm(keep()) }), "."]),
      el("button", { class: "gear", type: "button", "aria-label": "Commission settings", "aria-expanded": String(S.setOpen), onclick: function () { S.setOpen = !S.setOpen; drawSales(body); } }, [icon("gear")])
    ]));
    if (S.setOpen) body.appendChild(settingsBox(body));
    if (!S.nodes.length) { body.appendChild(el("div", { class: "empty" }, [el("b", { text: "No network yet" }), "The AutoSEO.my folder appears once the sales data is connected."])); return; }
    var C = calc();
    var tree = el("ul", { class: "tree" }); tree.appendChild(item(centre(), 0, C, body));
    body.appendChild(tree);
    body.appendChild(summary(C));
  }
  function settingsBox(body) {
    var sp = S.split;
    var c = el("input", { type: "number", inputmode: "decimal", min: "0", step: "0.01", value: String(sp.customer) });
    var d = el("input", { type: "number", inputmode: "decimal", min: "0", step: "0.01", value: String(sp.direct) });
    var g = el("input", { type: "number", inputmode: "decimal", min: "0", step: "0.01", value: String(sp.referral) });
    var k = el("b", { class: "money", text: rm(keep()) });
    var msg = el("p", { class: "msg", role: "status" });
    function upd() { var v = Number(c.value) - Number(d.value) - Number(g.value); k.textContent = isFinite(v) ? rm(v) : "-"; k.style.color = v < 0 ? "var(--alert)" : ""; }
    [c, d, g].forEach(function (i) { i.addEventListener("input", upd); });
    var save = el("button", { class: "btn main", type: "button", text: "Save settings" });
    save.addEventListener("click", function () {
      var s = { customer: Number(c.value), direct: Number(d.value), referral: Number(g.value) };
      if (![s.customer, s.direct, s.referral].every(function (x) { return isFinite(x) && x >= 0; }) || s.customer <= 0) { msg.textContent = errText("number"); return; }
      if (s.direct + s.referral > s.customer) { msg.textContent = errText("too_much"); return; }
      save.disabled = true;
      api("sales_settings", { settings: s }).then(function (r) {
        if (r.ok) { S.split = r.settings || s; S.setOpen = false; drawSales(body); } else { save.disabled = false; msg.textContent = errText(r.code || r.error); }
      });
    });
    return el("div", { class: "card form", style: "margin:0 0 12px" }, [
      el("label", {}, ["Customer pays (RM)", c]),
      el("div", { class: "row2" }, [el("label", {}, ["Direct commission (RM)", d]), el("label", {}, ["Referral commission (RM)", g])]),
      el("p", { style: "margin:0" }, ["AutoSEO keeps ", k]),
      el("div", { class: "acts" }, [save, el("button", { class: "btn", type: "button", text: "Close", onclick: function () { S.setOpen = false; drawSales(body); } })]),
      msg
    ]);
  }
  function earnText(e) {
    var parts = [];
    if (e.d) parts.push(e.d + " direct x " + rm(S.split.direct));
    if (e.g) parts.push(e.g + " level-2 x " + rm(S.split.referral));
    return parts.length ? " (" + parts.join(", ") + ")" : "";
  }
  function item(n, d, C, body) {
    var top = n.role === "centre", k = kids(n.id), isOpen = top || !!S.open[n.id];
    var li = el("li");
    var row = el("div", { class: "trow", style: "--d:" + d });
    row.appendChild(el("button", { class: "tog", type: "button", "aria-expanded": String(isOpen), onclick: function () { if (!top) { S.open[n.id] = !S.open[n.id]; drawSales(body); } } }, [
      icon("chev", "chev" + (isOpen ? " open" : "") + (top ? " none" : "")), icon("folder", "fold"),
      el("span", { class: "pw" }, [
        el("span", { class: "pl1" }, [el("span", { class: "nm", text: n.name }), top ? null : el("span", { class: "tag" + (k.length ? " ref" : ""), text: k.length ? "Referrer" : "Direct" })]),
        top ? el("span", { class: "pl2" }, ["Keeps ", el("b", { text: rm(C.keeps) })])
            : el("span", { class: "pl2" }, ["Pays " + rm(S.split.customer) + ". Earns ", el("b", { text: rm(C.per[n.id].earns) }), earnText(C.per[n.id])])
      ])
    ]));
    if (k.length) row.appendChild(el("span", { class: "cnt", "aria-label": k.length + " referrals", text: String(k.length) }));
    if (!top) row.appendChild(el("button", { class: "rm", type: "button", "aria-label": "Remove " + n.name, text: "−", onclick: function () { S.ui = { kind: "rm", id: n.id }; drawSales(body); } }));
    li.appendChild(row);
    if (S.ui && S.ui.kind === "rm" && S.ui.id === n.id) li.appendChild(removeBox(n, d, body));
    if (isOpen) {
      var ul = el("ul");
      k.forEach(function (c) { ul.appendChild(item(c, d + 1, C, body)); });
      ul.appendChild(el("li", {}, [addBox(n, d + 1, body)]));
      li.appendChild(ul);
    }
    return li;
  }
  function addBox(parent, d, body) {
    var box = el("div", { class: "sub", style: "--d:" + d });
    if (!(S.ui && S.ui.kind === "add" && S.ui.id === parent.id)) {
      box.appendChild(el("button", { class: "btn", type: "button", text: "+ Add person", onclick: function () { S.ui = { kind: "add", id: parent.id }; drawSales(body); var i = $("add-name"); if (i) i.focus(); } }));
      return box;
    }
    var inp = el("input", { id: "add-name", type: "text", maxlength: "60", autocomplete: "off", placeholder: "Name", "aria-label": "Name of new person under " + parent.name });
    var msg = el("p", { class: "msg", role: "status" });
    var save = el("button", { class: "btn main", type: "button", text: "Add" });
    function add() {
      var v = inp.value.trim(); if (!v) { msg.textContent = errText("name"); return; }
      save.disabled = true;
      api("sales_add", { name: v, parentId: parent.id }).then(function (r) {
        if (r.ok) { S.open[parent.id] = true; return loadSales(body); }
        save.disabled = false; msg.textContent = errText(r.code || r.error);
      });
    }
    save.addEventListener("click", add);
    inp.addEventListener("keydown", function (e) { if (e.key === "Enter") add(); });
    box.appendChild(el("div", { class: "addrow" }, [inp, save, el("button", { class: "btn", type: "button", text: "Cancel", onclick: function () { S.ui = null; drawSales(body); } })]));
    box.appendChild(msg);
    return box;
  }
  function removeBox(n, d, body) {
    var k = kids(n.id), parent = byId(n.parentId);
    var msg = el("p", { class: "msg", role: "status" });
    var yes = el("button", { class: "btn danger", type: "button", text: "Remove" });
    yes.addEventListener("click", function () {
      yes.disabled = true;
      api("sales_remove", { id: n.id }).then(function (r) { if (r.ok) { S.ui = null; return loadSales(body); } yes.disabled = false; msg.textContent = errText(r.code || r.error); });
    });
    var text = "Remove " + n.name + "?" + (k.length ? " Their " + k.length + (k.length === 1 ? " referral moves" : " referrals move") + " up to " + (parent ? parent.name : "AutoSEO.my") + "." : "");
    return el("div", { class: "sub", style: "--d:" + (d + 1) }, [el("p", { text: text }), el("div", { class: "acts" }, [yes, el("button", { class: "btn", type: "button", text: "Cancel", onclick: function () { S.ui = null; drawSales(body); } })]), msg]);
  }
  function summary(C) {
    var box = el("section", { "aria-labelledby": "sum-h" });
    box.appendChild(el("h2", { class: "h2", id: "sum-h", text: "Summary" }));
    function t(label, v, sub) { return el("div", { class: "tile" }, [el("b", { class: "num", text: v }), el("span", { text: label + (sub ? " (" + sub + ")" : "") })]); }
    box.appendChild(el("div", { class: "tiles" }, [
      t("People", String(C.people)),
      t("Sales", rm(C.sales), C.people + " x " + rm(S.split.customer)),
      t("Commission paid", rm(C.paid), C.n1 + " direct, " + C.n2 + " level-2"),
      t("AutoSEO keeps", rm(C.keeps))
    ]));
    var ok = Math.abs(C.sales - (C.paid + C.keeps)) < 0.005;
    box.appendChild(el("p", { class: "check" + (ok ? "" : " bad"), role: ok ? null : "alert", text: ok
      ? "Check: " + rm(C.sales) + " sales = " + rm(C.paid) + " paid + " + rm(C.keeps) + " kept."
      : "Warning: sales " + rm(C.sales) + " do not equal paid " + rm(C.paid) + " + kept " + rm(C.keeps) + "." }));
    var rows = S.nodes.filter(function (n) { return n.role !== "centre"; }).map(function (n) { return { n: n, e: C.per[n.id] }; });
    if (!rows.length) return box;
    rows.sort(function (a, b) { return b.e.earns - a.e.earns || a.n.name.localeCompare(b.n.name); });
    box.appendChild(el("table", { class: "tbl" }, [
      el("thead", {}, [el("tr", {}, [el("th", { text: "Name" }), el("th", { class: "r", text: "Direct" }), el("th", { class: "r", text: "Level-2" }), el("th", { class: "r", text: "Earns" })])]),
      el("tbody", {}, rows.map(function (r) { return el("tr", {}, [el("td", { class: "n", text: r.n.name }), el("td", { class: "r", text: String(r.e.d) }), el("td", { class: "r", text: String(r.e.g) }), el("td", { class: "r", text: rm(r.e.earns) })]); }))
    ]));
    return box;
  }

  // ---------- start ----------
  window.AUTOSEO_DASH = { ext: EXT, go: go };
  shell();
  go(location.pathname, true);
})();
