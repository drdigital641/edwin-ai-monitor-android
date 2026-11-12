/* AutoSEO client dashboard. All screens are built from the small templates below
   (header/menu, KPI tiles, client card, form), so one edit changes every screen.
   Every number shown comes from the server; the page never filters other accounts' data itself. */
(function () {
  "use strict";
  var T = window.T, CFG = window.AUTOSEO_ADMIN_CONFIG || {};
  var DEMO = /[?&]demo=1\b/.test(location.search);
  var state = { token: null, me: null, clients: null, error: null, last: null };
  var $app = document.getElementById("app"), $hdr = document.getElementById("hdr");

  /* ---------- helpers ---------- */
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function bi(k, cls) { var v = T[k]; return '<span class="bi ' + (cls || "") + '">' + esc(v[0]) + '<span class="zh" lang="zh-Hans">' + esc(v[1]) + "</span></span>"; }
  function biText(k) { return T[k][0] + " " + T[k][1]; }
  function when(iso) { if (!iso) return ""; var d = new Date(iso); if (isNaN(d)) return ""; return d.toLocaleString("en-GB", { day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit" }); }
  function store(k, v) { try { if (v == null) sessionStorage.removeItem(k); else sessionStorage.setItem(k, v); } catch (e) {} }
  function load(k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } }
  function safeUrl(u) { u = String(u || "").trim(); if (!u) return ""; if (!/^https?:\/\//i.test(u)) u = "https://" + u; try { var x = new URL(u); return /^https?:$/.test(x.protocol) ? x.href : ""; } catch (e) { return ""; } }
  function route() { return (location.hash.replace(/^#\/?/, "") || "clients").split("/")[0]; }

  /* ---------- server ---------- */
  function api(action, body) {
    if (DEMO) return window.AUTOSEO_DEMO(action, body || {});
    if (!CFG.api_url) return Promise.reject({ code: "not_set" });
    return fetch(CFG.api_url, {
      method: "POST", headers: { "Content-Type": "application/json" }, credentials: "omit",
      body: JSON.stringify(Object.assign({ action: action, id_token: state.token }, body || {}))
    }).then(function (r) { return r.json().catch(function () { return { ok: false, code: "bad_reply" }; }).then(function (j) { if (!j.ok) throw j; return j; }); },
      function () { throw { code: "network" }; });
  }
  function errText(e) {
    var c = e && e.code;
    var k = c === "not_allowed" ? "err_denied" : c === "email_not_verified" ? "err_unverified" : c === "network" ? "err_network" : c === "token_expired" || c === "bad_token" ? "err_session" : c === "not_set" ? "signin_not_set" : "err_generic";
    return bi(k);
  }

  /* ---------- template: header + labelled drop-down menu ---------- */
  var NAV = [["clients", "nav_clients"], ["new", "nav_new"]];
  function header() {
    if (!state.me) { $hdr.innerHTML = '<div class="hdr-in"><span class="logo" aria-hidden="true">AS</span><span class="menu-label">' + bi("app_title") + "</span></div>"; return; }
    var r = route(), cur = NAV.filter(function (n) { return n[0] === r; })[0] || NAV[0];
    $hdr.innerHTML = '<div class="hdr-in" style="position:relative">' +
      '<button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="menu"><span class="logo" aria-hidden="true">AS</span>' +
      '<span class="menu-label">' + bi(cur[1]) + "</span>" +
      '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>' +
      '<span class="hdr-who">' + esc(state.me.email) + "</span>" +
      '<nav class="menu" id="menu" hidden aria-label="Menu 菜单">' +
      NAV.map(function (n) { return '<a href="#/' + n[0] + '"' + (n[0] === r ? ' aria-current="page"' : "") + ">" + bi(n[1]) + "</a>"; }).join("") +
      '<hr><button type="button" id="signOut">' + bi("nav_signout") + "</button></nav></div>";
    var btn = document.getElementById("menuBtn"), menu = document.getElementById("menu");
    btn.onclick = function (ev) { ev.stopPropagation(); var o = menu.hidden; menu.hidden = !o; btn.setAttribute("aria-expanded", String(o)); };
    document.addEventListener("click", function close(ev) { if (!menu.contains(ev.target)) { menu.hidden = true; btn.setAttribute("aria-expanded", "false"); } }, { once: true });
    menu.querySelectorAll("a").forEach(function (a) { a.onclick = function () { menu.hidden = true; }; });
    document.getElementById("signOut").onclick = signOut;
  }

  /* ---------- template: pieces of a client card ---------- */
  var STEPS = ["pending", "preview", "live"];
  function steps(step) {
    var i = STEPS.indexOf(step); if (i < 0) i = 0;
    return '<ol class="steps" aria-label="' + esc(biText("status")) + '">' + STEPS.map(function (s, j) {
      var c = j < i ? "done" : j === i ? "now" : "";
      return '<li class="' + c + '"' + (j === i ? ' aria-current="step"' : "") + '><span class="dot" aria-hidden="true"></span>' + bi("st_" + s) + "</li>";
    }).join("") + "</ol>";
  }
  function pill(kind, key) { return '<span class="pill p-' + kind + '">' + esc(T[key][0]) + '<span class="zh" lang="zh-Hans">' + esc(T[key][1]) + "</span></span>"; }
  function healthPill(h) { return h === "ok" ? pill("ok", "h_ok") : h === "warn" ? pill("warn", "h_warn") : h === "down" ? pill("down", "h_down") : pill("none", "h_none"); }
  function fact(lblKey, valHtml, wide) { return '<div class="fact' + (wide ? " wide" : "") + '"><div class="lbl">' + bi(lblKey) + '</div><div class="val">' + valHtml + "</div></div>"; }
  function payment(c) {
    if (c.step !== "live") return ""; /* Payment section shows on Live clients only */
    var p = c.payment || {};
    var st = p.status === "paid" ? pill("ok", "pay_paid") : p.status === "due" ? pill("warn", "pay_due") : pill("none", "pay_notset");
    return '<section class="pay"><h3>' + bi("pay_title") + '</h3><div class="facts">' +
      fact("pay_plan", p.plan ? esc(p.plan) : bi("pay_notset")) + fact("pay_status", st) +
      '</div><button class="btn btn-line btn-block" type="button" disabled style="margin-top:10px" title="' + esc(biText("pay_soon")) + '">' + bi("pay_link") + "</button>" +
      '<div class="memo-meta" style="text-align:center">' + bi("pay_soon", "bi-inline") + "</div></section>";
  }
  function card(c) {
    var open = safeUrl(c.open_url);
    var link = open ? '<a class="btn btn-line" href="' + esc(open) + '" target="_blank" rel="noopener noreferrer">' + bi(c.step === "live" ? "open_site" : "open_preview") + "</a>" : "";
    var taps = c.taps || {};
    return '<article class="card" data-id="' + esc(c.id) + '">' +
      '<div class="card-top"><div style="min-width:0"><h2 class="card-name">' + esc(c.name) + "</h2>" + (c.url ? '<div class="card-url">' + esc(c.url) + "</div>" : "") + "</div>" +
      (c.new_followup ? '<span class="flag">' + esc(T.new_followup[0]) + '<span class="zh" lang="zh-Hans">' + esc(T.new_followup[1]) + "</span></span>" : "") + "</div>" +
      steps(c.step) +
      '<div class="facts">' +
        fact("health", healthPill(c.step === "pending" ? "none" : c.health)) +
        fact("articles", esc(c.articles == null ? 0 : c.articles)) +
        fact("taps", esc(T.taps_wa[0]) + " " + esc(taps.wa || 0) + " &nbsp;·&nbsp; " + esc(T.taps_call[0]) + " " + esc(T.taps_call[1]) + " " + esc(taps.call || 0), true) +
      "</div>" +
      (link ? '<div class="card-links">' + link + "</div>" : "") +
      '<div class="memo"><label for="memo-' + esc(c.id) + '">' + bi("memo") + '</label><textarea id="memo-' + esc(c.id) + '" data-memo="' + esc(c.id) + '" placeholder="' + esc(T.memo_ph[0] + " · " + T.memo_ph[1]) + '">' + esc(c.memo || "") + "</textarea>" +
      '<div class="memo-meta" id="mm-' + esc(c.id) + '">' + memoMeta(c.memo_updated_at) + "</div></div>" +
      payment(c) + "</article>";
  }
  function memoMeta(at) { return at ? esc(T.memo_edited[0]) + " " + esc(T.memo_edited[1]) + ": " + esc(when(at)) : esc(T.memo_never[0]) + " · " + esc(T.memo_never[1]); }
  function kpi(n, k) { return '<div class="kpi"><b>' + esc(n) + "</b><span>" + bi(k) + "</span></div>"; }

  /* ---------- screens ---------- */
  function demoNote() { return DEMO ? '<div class="demo">' + bi("demo_note") + "</div>" : ""; }
  function screenSignIn(errHtml) {
    $app.innerHTML = '<div class="center"><h1 class="h1">' + bi("signin_title") + "</h1><p>" + bi("signin_text") + "</p>" +
      (errHtml ? '<div class="banner-err">' + errHtml + "</div>" : "") +
      (CFG.google_client_id || DEMO ? '<div id="gsi"></div>' : '<div class="banner-err">' + bi("signin_not_set") + "</div>") + "</div>";
    if (DEMO) { var b = document.createElement("button"); b.className = "btn btn-main"; b.innerHTML = bi("signin_title"); b.onclick = function () { onToken("demo"); }; document.getElementById("gsi").appendChild(b); return; }
    if (!CFG.google_client_id) return;
    gsiReady(function () {
      google.accounts.id.initialize({ client_id: CFG.google_client_id, callback: function (r) { onToken(r.credential); }, auto_select: false, ux_mode: "popup", itp_support: true });
      google.accounts.id.renderButton(document.getElementById("gsi"), { theme: "outline", size: "large", shape: "pill", text: "signin_with", width: 280 });
    });
  }
  function screenLoading() { $app.innerHTML = '<div class="center"><p>' + bi("loading") + "</p></div>"; }
  function screenError(e) { $app.innerHTML = '<div class="center"><div class="banner-err">' + errText(e) + '</div><button class="btn btn-main" id="retry">' + bi("retry") + "</button></div>"; document.getElementById("retry").onclick = refresh; }

  function screenClients() {
    var cs = state.clients || [];
    var live = cs.filter(function (c) { return c.step === "live"; }).length;
    var taps = cs.reduce(function (a, c) { return a + ((c.taps && c.taps.wa) || 0) + ((c.taps && c.taps.call) || 0); }, 0);
    $app.innerHTML = demoNote() + '<h1 class="h1">' + bi("nav_clients") + "</h1>" +
      '<div class="kpis">' + kpi(cs.length, "k_clients") + kpi(live, "k_live") + kpi(cs.length - live, "k_building") + kpi(taps, "k_taps") + "</div>" +
      '<div class="add-row"><a class="btn btn-ochre btn-block" href="#/new">+ ' + bi("nav_new") + "</a></div>" +
      (cs.length ? '<div class="cards">' + cs.map(card).join("") + "</div>"
        : '<div class="center"><h2 class="h1" style="font-size:18px">' + bi("empty_title") + "</h2><p>" + bi("empty_text") + "</p></div>");
    $app.querySelectorAll("textarea[data-memo]").forEach(wireMemo);
  }

  /* memo autosave: saves 1.2s after typing stops and when the box loses focus */
  function wireMemo(ta) {
    var id = ta.getAttribute("data-memo"), meta = document.getElementById("mm-" + id), timer = null, saved = ta.value;
    function save() {
      clearTimeout(timer); var v = ta.value; if (v === saved) return;
      meta.className = "memo-meta"; meta.innerHTML = esc(T.memo_saving[0]) + " " + esc(T.memo_saving[1]);
      api("save_memo", { client_id: id, memo: v }).then(function (r) {
        saved = v; var c = (state.clients || []).filter(function (x) { return x.id === id; })[0]; if (c) { c.memo = v; c.memo_updated_at = r.memo_updated_at; }
        meta.innerHTML = esc(T.memo_saved[0]) + " " + esc(T.memo_saved[1]) + " · " + memoMeta(r.memo_updated_at);
      }, function (e) {
        meta.className = "memo-meta err"; meta.innerHTML = esc(T.memo_err[0]) + " " + esc(T.memo_err[1]);
        if (e && (e.code === "token_expired" || e.code === "bad_token")) return signOut(e);
        timer = setTimeout(save, 5000);
      });
    }
    ta.addEventListener("input", function () { clearTimeout(timer); timer = setTimeout(save, 1200); });
    ta.addEventListener("blur", save);
  }

  function screenNew() {
    $app.innerHTML = demoNote() + '<h1 class="h1">' + bi("f_title") + '</h1><form class="form" id="nf" novalidate>' +
      '<div class="field"><label for="f-company">1. ' + bi("f_company", "bi-inline") + ' <span class="req">(' + esc(T.f_required[0]) + " " + esc(T.f_required[1]) + ')</span></label><input type="text" id="f-company" name="company" maxlength="120" autocomplete="organization" required placeholder="' + esc(T.f_company_ph[0]) + '"><div class="err-msg" id="e-company" hidden>' + bi("f_err_company") + "</div></div>" +
      '<div class="field"><label for="f-url">2. ' + bi("f_url", "bi-inline") + ' <span class="req">(' + esc(T.f_required[0]) + " " + esc(T.f_required[1]) + ')</span></label><input type="text" id="f-url" name="url" maxlength="200" inputmode="url" autocapitalize="off" autocorrect="off" spellcheck="false" required placeholder="' + esc(T.f_url_ph[0]) + '"><div class="err-msg" id="e-url" hidden>' + bi("f_err_url") + "</div></div>" +
      '<fieldset class="field" style="border:0;padding:0;margin:0 0 18px"><legend class="lbl" style="padding:0;margin-bottom:8px;font-weight:650">3. ' + bi("f_urltype", "bi-inline") + ' <span class="req">(' + esc(T.f_required[0]) + " " + esc(T.f_required[1]) + ')</span></legend><div class="choice">' +
        '<label><input type="radio" name="url_type" value="new">' + bi("f_new_url") + "</label>" +
        '<label><input type="radio" name="url_type" value="existing">' + bi("f_existing_url") + "</label>" +
      '</div><div class="err-msg" id="e-type" hidden>' + bi("f_err_urltype") + "</div></fieldset>" +
      '<div class="field"><label for="f-notes">4. ' + bi("f_notes", "bi-inline") + ' <span class="opt">(' + esc(T.f_optional[0]) + " " + esc(T.f_optional[1]) + ')</span></label><textarea id="f-notes" name="notes" class="notes-big" maxlength="5000" placeholder="' + esc(T.f_notes_ph[0] + "\n" + T.f_notes_ph[1]) + '"></textarea></div>' +
      '<div class="banner-err" id="e-save" hidden></div>' +
      '<div class="form-actions"><button class="btn btn-main btn-block save" type="submit" id="saveBtn">' + bi("f_save") + '</button><a class="btn btn-line btn-block" href="#/clients">' + bi("f_cancel") + "</a></div></form>";
    var f = document.getElementById("nf");
    f.onsubmit = function (ev) {
      ev.preventDefault();
      var company = f.company.value.trim(), url = f.url.value.trim(), type = (f.querySelector("input[name=url_type]:checked") || {}).value, notes = f.notes.value;
      document.getElementById("e-company").hidden = !!company; document.getElementById("e-url").hidden = !!url; document.getElementById("e-type").hidden = !!type;
      if (!company || !url || !type) { (company ? url ? f.querySelector("input[name=url_type]") : f.url : f.company).focus(); return; }
      var btn = document.getElementById("saveBtn"); btn.disabled = true; btn.innerHTML = bi("f_saving");
      api("create_client", { company: company, url: url, url_type: type, notes: notes }).then(function (r) {
        state.clients = null; state.last = { company: company, url: url, type: type, notes: notes, user: r.submitted_by || state.me.email };
        location.hash = "#/done";
      }, function (e) { btn.disabled = false; btn.innerHTML = bi("f_save"); var b = document.getElementById("e-save"); b.hidden = false; b.innerHTML = errText(e); });
    };
  }

  function summaryText(x) {
    var type = x.type === "existing" ? T.sum_existing : T.sum_new, notes = x.notes.trim();
    function fill(tpl, i) { return tpl.replace("{company}", x.company).replace("{url}", x.url).replace("{type}", type[i]).replace("{notes}", notes || T.sum_no_notes[i]).replace("{user}", x.user); }
    return fill(T.sum_en, 0) + "\n" + fill(T.sum_zh, 1);
  }
  function screenDone() {
    var x = state.last; if (!x) { location.hash = "#/clients"; return; }
    var text = summaryText(x), group = safeUrl(state.me.group_link);
    $app.innerHTML = '<div class="form"><div class="ok-tick" aria-hidden="true">✓</div><h1 class="h1">' + bi("done_title") + "</h1><p>" + bi("done_text") + "</p>" +
      '<div class="summary" id="sum"></div><div class="form-actions">' +
      '<button class="btn btn-main btn-block save" type="button" id="copyBtn">' + bi("copy") + "</button>" +
      (group ? '<a class="btn btn-ochre btn-block" href="' + esc(group) + '" target="_blank" rel="noopener noreferrer">' + bi("open_group") + "</a>"
             : '<button class="btn btn-line btn-block" type="button" disabled>' + bi("group_not_set") + "</button>") +
      '<a class="btn btn-line btn-block" href="#/clients">' + bi("back_clients") + "</a></div></div>";
    document.getElementById("sum").textContent = text;
    document.getElementById("copyBtn").onclick = function () {
      var b = this; function ok() { b.innerHTML = bi("copied"); setTimeout(function () { b.innerHTML = bi("copy"); }, 2000); }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(ok, fallback); else fallback();
      function fallback() { var r = document.createRange(); r.selectNodeContents(document.getElementById("sum")); var s = getSelection(); s.removeAllRanges(); s.addRange(r); try { document.execCommand("copy"); ok(); } catch (e) {} }
    };
  }

  /* ---------- flow ---------- */
  function gsiReady(cb) {
    if (window.google && google.accounts && google.accounts.id) return cb();
    var s = document.createElement("script"); s.src = "https://accounts.google.com/gsi/client"; s.async = true; s.onload = cb; document.head.appendChild(s);
  }
  function onToken(tok) { state.token = tok; store("as_tok", tok); refresh(); }
  function signOut(e) {
    state.token = null; state.me = null; state.clients = null; store("as_tok", null);
    try { if (window.google && google.accounts) google.accounts.id.disableAutoSelect(); } catch (x) {}
    header(); screenSignIn(e && e.code ? errText(e) : "");
  }
  function refresh() {
    header(); screenLoading();
    api("me").then(function (r) { state.me = r.user; state.me.group_link = r.group_link || ""; return api("clients"); })
      .then(function (r) { state.clients = r.clients || []; render(); },
        function (e) { if (e && /^(not_allowed|email_not_verified|token_expired|bad_token|not_set)$/.test(e.code)) signOut(e); else screenError(e); });
  }
  function render() {
    header();
    var r = route();
    if (r === "new") return screenNew();
    if (r === "done") return screenDone();
    if (!state.clients) return refresh();
    screenClients();
    window.scrollTo(0, 0);
  }
  window.addEventListener("hashchange", function () { if (state.me) render(); });
  var saved = load("as_tok");
  if (saved && (!DEMO || saved === "demo")) onToken(saved); else { header(); screenSignIn(""); }
})();
