/* SGCarAccident: guided flows (one question per screen) + "Tell us what happened" matcher. Plain JS, no reload. */
(function () {
  var d = document;
  // ---- guided flow ----
  var flow = d.querySelector(".flow");
  if (flow) {
    var steps = [].slice.call(flow.querySelectorAll(".step")), n = steps.length, i = 0;
    var bar = d.querySelector(".prog i"), lab = d.querySelector(".prog-l");
    var back = d.querySelector("[data-back]"), next = d.querySelector("[data-next]"), navBox = d.querySelector(".nav");
    var tpl = lab ? lab.getAttribute("data-tpl") : "";
    function show(k, push) {
      i = Math.max(0, Math.min(n - 1, k));
      steps.forEach(function (s, j) { s.classList.toggle("on", j === i); });
      if (bar) bar.style.width = ((i + 1) / n * 100) + "%";
      if (lab) lab.textContent = tpl.replace("{n}", i + 1).replace("{t}", n);
      back.disabled = i === 0;
      navBox.style.display = steps[i].hasAttribute("data-end") ? "none" : "";
      if (push) { try { history.pushState({ s: i }, "", "#s" + (i + 1)); } catch (e) {} }
      var h = steps[i].querySelector("h2");
      if (push && h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
      if (push) window.scrollTo({ top: Math.max(0, flow.getBoundingClientRect().top + window.scrollY - 70), behavior: "smooth" });
    }
    next.addEventListener("click", function () { show(i + 1, true); });
    back.addEventListener("click", function () { if (history.state && history.state.s === i && i > 0) history.back(); else show(i - 1, true); });
    window.addEventListener("popstate", function (e) { show(e.state && typeof e.state.s === "number" ? e.state.s : 0, false); });
    flow.addEventListener("click", function (e) {
      var b = e.target.closest(".choice"); if (!b) return;
      var step = b.closest(".step");
      step.querySelectorAll(".choice").forEach(function (c) { c.setAttribute("aria-pressed", c === b ? "true" : "false"); });
      step.querySelectorAll(".note").forEach(function (nt) { nt.hidden = nt.getAttribute("data-k") !== b.getAttribute("data-k"); });
      var act = step.querySelector(".acts");
      if (act) act.hidden = !(b.getAttribute("data-k") === "hurt" || b.getAttribute("data-k") === "stuck");
    });
    steps.forEach(function (s) { s.querySelectorAll(".note").forEach(function (nt) { nt.hidden = true; }); var a = s.querySelector(".acts[data-opt]"); if (a) a.hidden = true; });
    var m = /^#s(\d+)$/.exec(location.hash);
    var start = m ? +m[1] - 1 : 0;
    try { history.replaceState({ s: start }, "", location.hash || location.pathname + location.search); } catch (e) {}
    show(start, false);
    var all = d.querySelector("[data-all]");
    if (all) all.addEventListener("click", function (e) { e.preventDefault(); d.documentElement.classList.remove("js"); all.parentNode.style.display = "none"; });
  }
  // ---- triage matcher (simple keywords, no AI) ----
  var tri = d.querySelector(".triage");
  if (tri) {
    var rules = JSON.parse(tri.getAttribute("data-rules")), out = tri.querySelector(".out"), inp = tri.querySelector("input");
    tri.addEventListener("submit", function (e) {
      e.preventDefault();
      var t = " " + inp.value.toLowerCase().replace(/[^\p{L}\p{N}' ]+/gu, " ") + " ", hit = null, best = 0;
      rules.paths.forEach(function (r) {
        var sc = 0; r.k.forEach(function (w) { if (t.indexOf(w) > -1) sc += w.length; });
        if (sc > best) { best = sc; hit = r; }
      });
      var hurt = rules.hurt.some(function (w) { return t.indexOf(w) > -1; });
      out.innerHTML = "";
      if (hurt) { var p = d.createElement("p"); p.innerHTML = "<strong>" + rules.msg.hurt + "</strong>"; out.appendChild(p); }
      var q = d.createElement("p");
      if (hit) {
        q.textContent = rules.msg.hit + " ";
        var a = d.createElement("a"); a.href = hit.u; a.textContent = hit.l; q.appendChild(a);
      } else q.textContent = rules.msg.none;
      out.appendChild(q);
    });
  }
})();
