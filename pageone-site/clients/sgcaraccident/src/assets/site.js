/* SGCarAccident v2: guided steps (one screen at a time, answers kept for this visit), insurer reporting-centre picker,
   accident statement helper (stays on the phone), helpbox toggles. Plain JS, no libraries. */
(function () {
  var d = document, UI = {};
  try { UI = JSON.parse(d.getElementById("ui").textContent); } catch (e) {}
  var LANG = d.body.getAttribute("data-lang") || "en";
  function ss(k, v) { try { if (v === undefined) return JSON.parse(sessionStorage.getItem(k) || "null"); sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }
  function fmt(s, o) { return String(s || "").replace(/\{(\w+)\}/g, function (m, k) { return o[k] != null ? o[k] : m; }); }
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function $$(q, el) { return [].slice.call((el || d).querySelectorAll(q)); }

  // ---------- single choices (flows, windscreen cover, statement yes/no) ----------
  function pickChoice(b, save) {
    var box = b.closest(".step") || b.closest(".card") || b.parentNode.parentNode;
    var grp = b.parentNode;
    $$(".choice", grp).forEach(function (c) { c.setAttribute("aria-pressed", c === b ? "true" : "false"); });
    var k = b.getAttribute("data-k");
    $$(":scope > .note", box).forEach(function (nt) { if (!nt.closest(".chk")) nt.hidden = nt.getAttribute("data-k") !== k; });
    var act = box.querySelector(".acts[data-opt]");
    if (act) act.hidden = !(k === "hurt" || k === "stuck");
    if (save) save();
  }

  // ---------- guided flow ----------
  var flow = d.querySelector(".flow");
  var FKEY = flow ? "sca_flow_" + flow.getAttribute("data-flow") + "_" + LANG : "";
  var state = (flow && ss(FKEY)) || { s: 0, a: {} };
  function save() { if (flow) ss(FKEY, state); }
  if (flow) {
    var steps = $$(".step", flow), n = steps.length, i = 0;
    var bar = d.querySelector(".prog i"), lab = d.querySelector(".prog-l");
    var back = d.querySelector("[data-back]"), next = d.querySelector("[data-next]"), navBox = d.querySelector(".nav");
    var tpl = lab ? lab.getAttribute("data-tpl") : "", labels = [];
    try { labels = JSON.parse(lab.getAttribute("data-labels")); } catch (e) {}
    function show(k, push) {
      i = Math.max(0, Math.min(n - 1, k));
      steps.forEach(function (s, j) { s.classList.toggle("on", j === i); });
      if (bar) bar.style.width = ((i + 1) / n * 100) + "%";
      if (lab) lab.textContent = tpl.replace("{n}", i + 1).replace("{t}", n) + (labels[i] ? " · " + labels[i] : "");
      back.disabled = i === 0;
      next.hidden = !!steps[i].hasAttribute("data-end");
      navBox.classList.toggle("end", steps[i].hasAttribute("data-end"));
      state.s = i; save();
      if (steps[i].querySelector("[data-final-insurer]")) finalInsurer(steps[i].querySelector("[data-final-insurer]"));
      if (push) { try { history.pushState({ s: i }, "", "#s" + (i + 1)); } catch (e) {} }
      var h = steps[i].querySelector("h2");
      if (push && h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
      if (push) window.scrollTo({ top: Math.max(0, flow.getBoundingClientRect().top + window.scrollY - 64), behavior: "smooth" });
    }
    next.addEventListener("click", function () { show(i + 1, true); });
    back.addEventListener("click", function () { if (history.state && history.state.s === i && i > 0) history.back(); else show(i - 1, true); });
    window.addEventListener("popstate", function (e) { show(e.state && typeof e.state.s === "number" ? e.state.s : 0, false); });
    // initial: hide notes, restore answers
    steps.forEach(function (s) { $$(".note", s).forEach(function (nt) { nt.hidden = true; }); var a = s.querySelector(".acts[data-opt]"); if (a) a.hidden = true; });
    steps.forEach(function (s, j) {
      var a = state.a[j]; if (!a) return;
      if (a.c) { var b = s.querySelector('.choices .choice[data-k="' + a.c + '"]'); if (b) pickChoice(b); }
      if (a.f) { Object.keys(a.f).forEach(function (k) { var b = s.querySelector('.flag[data-k="' + k + '"]'); if (b) b.setAttribute("aria-pressed", "true"); }); if (a.none) s.querySelector("[data-none]").setAttribute("aria-pressed", "true"); flagNotes(s); }
      if (a.y) { Object.keys(a.y).forEach(function (k) { var r = s.querySelector('.chk[data-k="' + k + '"]'); if (r) setYN(r, a.y[k]); }); }
    });
    flow.addEventListener("click", function (e) {
      var j = steps.indexOf(e.target.closest(".step")); if (j < 0) return;
      var a = state.a[j] = state.a[j] || {};
      var b = e.target.closest(".choices .choice");
      if (b) { pickChoice(b); a.c = b.getAttribute("data-k"); save(); return; }
      var f = e.target.closest(".flag");
      if (f) { var on = f.getAttribute("aria-pressed") !== "true"; f.setAttribute("aria-pressed", on ? "true" : "false"); a.f = a.f || {}; if (on) a.f[f.getAttribute("data-k")] = 1; else delete a.f[f.getAttribute("data-k")]; a.none = false; steps[j].querySelector("[data-none]").setAttribute("aria-pressed", "false"); flagNotes(steps[j]); save(); return; }
      var nb = e.target.closest("[data-none]");
      if (nb) { $$(".flag", steps[j]).forEach(function (x) { x.setAttribute("aria-pressed", "false"); }); nb.setAttribute("aria-pressed", "true"); a.f = {}; a.none = true; flagNotes(steps[j]); save(); return; }
      var yn = e.target.closest(".yn button");
      if (yn) { var r = yn.closest(".chk"); setYN(r, yn.getAttribute("data-v")); a.y = a.y || {}; a.y[r.getAttribute("data-k")] = yn.getAttribute("data-v"); save(); }
    });
    var m = /^#s(\d+)$/.exec(location.hash);
    var start = m ? +m[1] - 1 : (state.s || 0);
    try { history.replaceState({ s: start }, "", "#s" + (start + 1)); } catch (e) {}
    show(start, false);
    var all = d.querySelector("[data-all]");
    if (all) all.addEventListener("click", function (e) { e.preventDefault(); d.documentElement.classList.remove("js"); all.parentNode.style.display = "none"; $$(".note").forEach(function (x) { x.hidden = false; }); });
  }
  function flagNotes(s) {
    var any = false, police = false;
    $$(".flag", s).forEach(function (f) {
      var on = f.getAttribute("aria-pressed") === "true";
      var nt = s.querySelector('.note[data-k="' + f.getAttribute("data-k") + '"]'); if (nt) nt.hidden = !on;
      if (on) { any = true; if (f.getAttribute("data-police")) police = true; }
    });
    s.querySelector('.note[data-k="_police"]').hidden = !police;
    s.querySelector('.note[data-k="_none"]').hidden = !(s.querySelector("[data-none]").getAttribute("aria-pressed") === "true");
    var act = s.querySelector(".acts"); if (act) act.classList.toggle("hot", any);
  }
  function setYN(r, v) {
    $$(".yn button", r).forEach(function (b) { b.setAttribute("aria-pressed", b.getAttribute("data-v") === v ? "true" : "false"); });
    var nt = r.querySelector(".note"); if (nt) nt.hidden = v !== "n";
  }
  // choices outside a flow (windscreen cover etc.)
  $$(".card .choices").forEach(function (g) { $$(".note", g.parentNode).forEach(function (nt) { nt.hidden = true; }); });
  d.addEventListener("click", function (e) {
    var b = e.target.closest(".card .choices .choice"); if (b && !flow) pickChoice(b);
  });

  // ---------- insurer picker -> reporting centres inline ----------
  var INS_KEY = "sca_insurer";
  function centreHtml(c) {
    return '<div class="ins"><h3>' + esc(c.n || c.a) + "</h3>" + (c.n ? "<p>" + esc(c.a) + "</p>" : "") +
      (c.h ? '<p class="meta">' + esc(UI.hours) + ": " + esc(c.h) + "</p>" : "") + (c.x ? '<p class="meta">' + esc(c.x) + "</p>" : "") +
      '<a class="map" href="' + esc(c.m) + '" target="_blank" rel="noopener">' + esc(UI.dir) + "</a></div>";
  }
  function render(box, j) {
    var out = box.querySelector(".pick-out");
    var regions = [];
    j.c.forEach(function (c) { if (c.r && regions.indexOf(c.r) < 0) regions.push(c.r); });
    var h = '<p class="count">' + esc(fmt(UI.places, { n: j.c.length, name: j.name })) + "</p>";
    if (j.hl) h += '<a class="btn btn-ghost block hlb" href="' + esc(j.hlt) + '">' + esc(j.name + " " + j.hl) + "</a>";
    if (regions.length > 1) h += '<div class="chips filt" role="group" aria-label="' + esc(UI.near_h) + '"><button type="button" aria-pressed="true" data-r="">' + esc(UI.all) + "</button>" +
      regions.map(function (r) { return '<button type="button" aria-pressed="false" data-r="' + esc(r) + '">' + esc(r) + "</button>"; }).join("") + "</div>";
    h += '<div class="ins-list">' + j.c.map(function (c) { return centreHtml(c).replace('<div class="ins">', '<div class="ins" data-r="' + esc(c.r) + '">'); }).join("") + "</div>";
    h += '<p class="src">' + esc(fmt(UI.src, { name: j.name, d: j.read })) + ' <a href="' + esc(j.src) + '" rel="noopener">' + esc(j.name) + "</a></p>";
    h += '<a class="btn btn-sign block" href="' + esc(j.url) + '">' + esc(fmt(UI.full, { name: j.name })) + "</a>";
    out.innerHTML = h;
    var f = out.querySelector(".filt");
    if (f) f.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      $$("button", f).forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
      var r = b.getAttribute("data-r");
      $$(".ins", out).forEach(function (x) { x.hidden = !!r && x.getAttribute("data-r") !== r; });
    });
  }
  function loadIns(box, slug) {
    var out = box.querySelector(".pick-out");
    if (!slug) { out.innerHTML = ""; return; }
    if (slug === "other") { out.innerHTML = '<p class="note">' + esc(UI.other) + "</p>"; if (box.hasAttribute("data-store")) ss(INS_KEY, { slug: "other" }); return; }
    out.innerHTML = '<p class="count">' + esc(UI.loading) + "</p>";
    fetch(box.getAttribute("data-json") + slug + "." + LANG + ".json").then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
      render(box, j);
      if (box.hasAttribute("data-store")) ss(INS_KEY, { slug: slug, name: j.name, url: j.url, hl: j.hl, hlt: j.hlt });
    }).catch(function () { out.innerHTML = '<p class="err">' + esc(UI.fail) + "</p>"; });
  }
  $$(".picker").forEach(function (box) {
    var sel = box.querySelector("select");
    sel.addEventListener("change", function () { loadIns(box, sel.value); });
    var saved = ss(INS_KEY);
    if (saved && saved.slug && box.hasAttribute("data-store")) { sel.value = saved.slug; loadIns(box, saved.slug); }
  });
  function finalInsurer(el) {
    var s = ss(INS_KEY);
    if (!s || !s.slug || s.slug === "other") return;
    el.innerHTML = '<p><strong>' + esc(fmt(UI.picked, { name: s.name })) + "</strong></p>" +
      '<a class="btn btn-sign block" href="' + esc(s.url) + '">' + esc(fmt(UI.full, { name: s.name })) + "</a>" +
      (s.hl ? '<a class="btn btn-ghost block" href="' + esc(s.hlt) + '">' + esc(s.name + " " + s.hl) + "</a>" : "");
  }

  // ---------- helpbox: Request a callback / Submit accident details ----------
  d.addEventListener("click", function (e) {
    var o = e.target.closest("[data-open]"); if (!o) return;
    e.preventDefault();
    var w = d.getElementById("wrap-" + o.getAttribute("data-open")); if (!w) return;
    $$(".lead-wrap", w.parentNode).forEach(function (x) { if (x !== w) x.hidden = true; });
    w.hidden = false;
    var f = w.querySelector("input,textarea,select"); if (f) f.focus({ preventScroll: true });
    w.scrollIntoView({ behavior: "smooth", block: "start" });
  });

  // ---------- statement helper (nothing leaves the phone unless the driver sends it) ----------
  $$("[data-stmt]").forEach(function (form) {
    var S = JSON.parse(form.querySelector(".stmt-strings").textContent);
    var KEY = "sca_stmt_" + LANG;
    var saved = ss(KEY) || {};
    $$("input,select,textarea", form).forEach(function (el) {
      if (saved[el.name]) el.value = saved[el.name];
      el.addEventListener("input", function () { saved[el.name] = el.value; ss(KEY, saved); });
      el.addEventListener("change", function () { saved[el.name] = el.value; ss(KEY, saved); });
    });
    var out = form.querySelector(".stmt-out"), pre = form.querySelector(".stmt-text");
    function text() {
      var lines = [S.title, ""];
      S.groups.forEach(function (g) {
        var rows = g[1].map(function (k) { var el = form.elements[k]; return el && el.value.trim() ? S.labels[k] + ": " + el.value.trim() : ""; }).filter(Boolean);
        if (rows.length) { lines.push(g[0].toUpperCase()); lines = lines.concat(rows); lines.push(""); }
      });
      lines.push(S.footer);
      return lines.join("\n");
    }
    form.querySelector("[data-make]").addEventListener("click", function () {
      var t = text(); pre.textContent = t; out.hidden = false;
      form.querySelector("[data-wa-stmt]").href = "https://wa.me/" + S.wa + "?text=" + encodeURIComponent(S.wa_pre + "\n\n" + t);
      out.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    form.querySelector("[data-copy]").addEventListener("click", function () {
      var t = pre.textContent, msg = form.querySelector("[data-copied]");
      (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { msg.textContent = S.copied; }, function () {
        var r = d.createRange(); r.selectNodeContents(pre); var sel = getSelection(); sel.removeAllRanges(); sel.addRange(r);
      });
    });
    form.querySelector("[data-print]").addEventListener("click", function () {
      d.body.classList.add("print-stmt"); window.print(); setTimeout(function () { d.body.classList.remove("print-stmt"); }, 500);
    });
  });
  // a statement opened from inside a flow step: keep its yes/no visible
})();
