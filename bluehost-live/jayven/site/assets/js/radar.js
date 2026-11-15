(function () {
  "use strict";
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // Hub filters: region chips (hash-synced) + type chips + district select; month groups hide when empty
  var board = document.querySelector("[data-board]");
  if (board) {
    var cards = $$("[data-card]", board);
    var empty = board.querySelector("[data-empty]");
    var dsel = document.querySelector("[data-f-district]");
    var area = "all", type = "", dist = "";
    var areas = ["all", "central", "north", "north-east", "east", "west"];
    var match = function (c) {
      var okA = area === "all" || c.getAttribute("data-area") === area;
      var okT = !type || (" " + c.getAttribute("data-types") + " ").indexOf(" " + type + " ") > -1;
      var okD = !dist || c.getAttribute("data-district") === dist;
      return okA && okT && okD;
    };
    var apply = function () {
      var total = 0;
      cards.forEach(function (c) { var ok = match(c); if (ok) total++; c.hidden = !ok; });
      $$(".rd-group", board).forEach(function (g) {
        g.hidden = !$$("[data-card]", g).some(function (c) { return !c.hidden; });
      });
      empty.hidden = total > 0;
      $$("[data-f-area]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-f-area") === area)); });
      var moods = $$("[data-mood]");
      var hasMood = moods.some(function (m) { return m.getAttribute("data-mood") === area; });
      moods.forEach(function (m) { m.hidden = m.getAttribute("data-mood") !== (hasMood ? area : "all"); });
      $$("[data-f-type]").forEach(function (b) { b.setAttribute("aria-pressed", String(b.getAttribute("data-f-type") === type)); });
    };
    $$("[data-f-area]").forEach(function (b) {
      b.addEventListener("click", function () {
        area = b.getAttribute("data-f-area"); dist = ""; if (dsel) dsel.value = "";
        history.replaceState(null, "", area === "all" ? location.pathname : "#" + area);
        apply();
      });
    });
    $$("[data-f-type]").forEach(function (b) {
      b.addEventListener("click", function () { var t = b.getAttribute("data-f-type"); type = type === t ? "" : t; apply(); });
    });
    if (dsel) dsel.addEventListener("change", function () {
      dist = dsel.value; if (dist) { area = "all"; history.replaceState(null, "", location.pathname); } apply();
    });
    var fromHash = function () {
      var h = location.hash.replace("#", "");
      if (areas.indexOf(h) > -1) area = h;
      apply();
    };
    window.addEventListener("hashchange", fromHash);
    fromHash();
  }

  // Sticky WhatsApp bar hides while the form is on screen
  var bar = document.querySelector("[data-bar]");
  var watch = $$("#register,[data-primary]");
  if (bar && watch.length && "IntersectionObserver" in window) {
    var seen = {};
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { seen[watch.indexOf(e.target)] = e.isIntersecting; });
      bar.classList.toggle("is-off", Object.keys(seen).some(function (k) { return seen[k]; }));
    }, { threshold: 0.15 });
    watch.forEach(function (el) { io.observe(el); });
  }

  // Form -> WhatsApp with PDPA consent
  $$("[data-wa-form]").forEach(function (f) {
    f.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var err = f.querySelector("[data-form-error]");
      var v = function (n) { var el = f.querySelector("[name=" + n + "]"); return el ? String(el.value || "").trim() : ""; };
      var msg = "";
      if (!v("name")) msg = "Please add your name.";
      else if (!v("phone")) msg = "Please add your phone number.";
      else if (!f.querySelector("[name=consent]").checked) msg = "Please tick the consent box first.";
      if (msg) { err.textContent = msg; err.hidden = false; return; }
      err.hidden = true;
      var p = v("project");
      var text = "Hi Jayven, please send me " + (p ? "updates on " + p : "new-launch updates") + ". Name: " + v("name") + ". Phone: " + v("phone") + ".";
      window.location.href = "https://wa.me/" + f.getAttribute("data-wa-digits") + "?text=" + encodeURIComponent(text);
    });
  });
})();
