/* SGCarAccident private settlement: fill (Driver A) -> sign -> secure link; Driver B checks + signs; PDF for both.
   Data goes only to the private Base44 API (POST body). The share token lives in the URL fragment (#t=...),
   which browsers never send to any server. No personal data is ever put in a URL. */
(function () {
  var d = document, root = d.getElementById("settle");
  if (!root) return;
  var API = root.getAttribute("data-api"), LANG = root.getAttribute("data-lang"), SIGN_URL = root.getAttribute("data-sign");
  var S = JSON.parse(d.getElementById("settle-strings").textContent);
  var $ = function (q, el) { return (el || d).querySelector(q); }, $$ = function (q, el) { return [].slice.call((el || d).querySelectorAll(q)); };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function api(body) {
    return fetch(API, { method: "POST", headers: { "Content-Type": "application/json" }, credentials: "omit", body: JSON.stringify(body) })
      .then(function (r) { return r.json().then(function (j) { j._status = r.status; return j; }); });
  }

  // ---------- signature pad ----------
  function pad(box) {
    var c = $("canvas", box), ctx = c.getContext("2d"), drawn = false, last = null;
    function size() { var r = c.getBoundingClientRect(), k = window.devicePixelRatio || 1; c.width = r.width * k; c.height = r.height * k; ctx.setTransform(k, 0, 0, k, 0, 0); ctx.lineWidth = 2.6; ctx.lineCap = "round"; ctx.lineJoin = "round"; ctx.strokeStyle = "#0F2A3D"; drawn = false; }
    function pt(e) { var r = c.getBoundingClientRect(); return [e.clientX - r.left, e.clientY - r.top]; }
    c.addEventListener("pointerdown", function (e) { c.setPointerCapture(e.pointerId); last = pt(e); ctx.beginPath(); ctx.arc(last[0], last[1], 1.2, 0, 7); ctx.fillStyle = "#0F2A3D"; ctx.fill(); drawn = true; e.preventDefault(); });
    c.addEventListener("pointermove", function (e) { if (!last) return; var p = pt(e); ctx.beginPath(); ctx.moveTo(last[0], last[1]); ctx.lineTo(p[0], p[1]); ctx.stroke(); last = p; drawn = true; e.preventDefault(); });
    ["pointerup", "pointercancel", "pointerleave"].forEach(function (t) { c.addEventListener(t, function () { last = null; }); });
    $(".clr", box).addEventListener("click", size);
    return {
      init: size, empty: function () { return !drawn; },
      png: function () { var o = d.createElement("canvas"); o.width = 600; o.height = 200; var x = o.getContext("2d"); x.fillStyle = "#fff"; x.fillRect(0, 0, 600, 200); x.drawImage(c, 0, 0, 600, 200); return o.toDataURL("image/png"); }
    };
  }

  // ---------- photos ----------
  function shrink(file) {
    return new Promise(function (ok, no) {
      var img = new Image(), url = URL.createObjectURL(file);
      img.onload = function () {
        var m = 1280, w = img.naturalWidth, h = img.naturalHeight, k = Math.min(1, m / Math.max(w, h));
        var c = d.createElement("canvas"); c.width = Math.round(w * k); c.height = Math.round(h * k);
        c.getContext("2d").drawImage(img, 0, 0, c.width, c.height); URL.revokeObjectURL(url);
        var q = 0.72, out = c.toDataURL("image/jpeg", q);
        while (out.length > 440000 && q > 0.35) { q -= 0.1; out = c.toDataURL("image/jpeg", q); }
        ok(out);
      };
      img.onerror = no; img.src = url;
    });
  }

  // ---------- PDF (drawn on canvas so Chinese text and signatures render, then wrapped by jsPDF) ----------
  function wrapLines(ctx, text, maxW) {
    var out = [], words = String(text || "").split(/(\s+)/), line = "";
    var cjk = /[　-鿿＀-￯]/;
    var tokens = [];
    words.forEach(function (w) { if (cjk.test(w)) tokens = tokens.concat(w.split("")); else tokens.push(w); });
    tokens.forEach(function (t) { var test = line + t; if (ctx.measureText(test).width > maxW && line.trim()) { out.push(line.trim()); line = t.trim() ? t : ""; } else line = test; });
    if (line.trim()) out.push(line.trim());
    return out.length ? out : [""];
  }
  function loadImg(src) { return new Promise(function (ok) { if (!src) return ok(null); var i = new Image(); i.onload = function () { ok(i); }; i.onerror = function () { ok(null); }; i.src = src; }); }
  function makePdf(r) {
    var W = 1240, H = 1754, M = 90, font = getComputedStyle(d.body).fontFamily;
    function page() { var c = d.createElement("canvas"); c.width = W; c.height = H; var x = c.getContext("2d"); x.fillStyle = "#fff"; x.fillRect(0, 0, W, H); x.textBaseline = "top"; return [c, x]; }
    return Promise.all([loadImg(r.a_signature), loadImg(r.b_signature)].concat((r.photos || []).map(loadImg))).then(function (imgs) {
      var p1 = page(), c = p1[0], x = p1[1], y = M;
      x.fillStyle = "#083F63"; x.fillRect(M, y, W - 2 * M, 84); x.fillStyle = "#fff"; x.font = "700 34px " + font; x.fillText(S.pdf_title, M + 24, y + 24); y += 110;
      function row(label, val) {
        x.font = "400 21px " + font; x.fillStyle = "#3C5466";
        var lb = wrapLines(x, label, 270); lb.forEach(function (l, i) { x.fillText(l, M, y + i * 28); });
        x.font = "700 24px " + font; x.fillStyle = "#0F2A3D";
        var ls = wrapLines(x, val || "-", W - 2 * M - 300); ls.forEach(function (l, i) { x.fillText(l, M + 300, y + i * 34); });
        y += Math.max(ls.length * 34, lb.length * 28) + 12; x.fillStyle = "#D5DEE5"; x.fillRect(M, y - 6, W - 2 * M, 1);
      }
      function head(t) { y += 14; x.fillStyle = "#0B5A8C"; x.fillRect(M, y, W - 2 * M, 44); x.fillStyle = "#fff"; x.font = "700 24px " + font; x.fillText(t, M + 16, y + 10); y += 62; }
      head(S.s_accident);
      row(S.date + " / " + S.time, (r.accident_date || "") + (r.accident_time ? "  " + r.accident_time : ""));
      row(S.location, r.location); if (r.description) row(S.description, r.description);
      head(S.option);
      var payer = r.payer === "a" ? (r.party_a.name || S.driver_a) : (r.party_b.name || S.driver_b);
      var payee = r.payer === "a" ? (r.party_b.name || S.driver_b) : (r.party_a.name || S.driver_a);
      row(r.settlement_option === "A" ? "(A)" : "(B)", r.settlement_option === "A" ? S.opt_a.replace(/^\(A\)\s*/, "") : S.opt_b.replace(/^\(B\)\s*/, "") + "  " + payer + " -> " + payee + ": S$" + (r.amount || ""));
      [["a", S.driver_a, 0], ["b", S.driver_b, 1]].forEach(function (pp) {
        var P = r["party_" + pp[0]] || {}; head(pp[1]);
        row(S.name, P.name); row(S.nric, P.nric_last4); row(S.phone, P.phone); row(S.vehicle_no, P.vehicle_no); row(S.vehicle_make, P.vehicle_make); row(S.insurer, P.insurer);
        var sig = imgs[pp[2]], at = r[pp[0] + "_signed_at"];
        x.font = "400 22px " + font; x.fillStyle = "#3C5466"; wrapLines(x, at ? S.pdf_signed + " " + new Date(at).toLocaleString(LANG === "zh" ? "zh-SG" : "en-SG", { timeZone: "Asia/Singapore" }) : S.pdf_waiting, 270).forEach(function (l, i) { x.fillText(l, M, y + i * 28); });
        if (sig) x.drawImage(sig, M + 300, y - 20, 330, 110); x.fillStyle = "#0F2A3D"; x.fillRect(M + 300, y + 92, 330, 2); y += 118;
      });
      x.font = "400 19px " + font; x.fillStyle = "#3C5466";
      wrapLines(x, S.pdf_footer, W - 2 * M).forEach(function (l, i) { x.fillText(l, M, H - M - 40 + i * 26); });
      var pages = [c];
      var ph = imgs.slice(2).filter(Boolean);
      if (ph.length) {
        var p2 = page(), c2 = p2[0], x2 = p2[1]; x2.fillStyle = "#083F63"; x2.font = "700 32px " + font; x2.fillText(S.pdf_photos, M, M);
        var cw = (W - 2 * M - 30) / 2, chh = 640;
        ph.forEach(function (im, i) { var cx = M + (i % 2) * (cw + 30), cy = M + 70 + Math.floor(i / 2) * (chh + 30), k = Math.min(cw / im.width, chh / im.height); x2.drawImage(im, cx, cy, im.width * k, im.height * k); });
        pages.push(c2);
      }
      var pdf = new window.jspdf.jsPDF({ unit: "mm", format: "a4" });
      pages.forEach(function (pg, i) { if (i) pdf.addPage(); pdf.addImage(pg.toDataURL("image/jpeg", 0.9), "JPEG", 0, 0, 210, 297); });
      pdf.save("private-settlement-" + (r.accident_date || "form") + (r.status === "signed" ? "-signed" : "") + ".pdf");
    });
  }

  function reviewHtml(r) {
    function dl(rows) { return "<dl>" + rows.filter(function (q) { return q[1]; }).map(function (q) { return "<dt>" + esc(q[0]) + "</dt><dd>" + esc(q[1]) + "</dd>"; }).join("") + "</dl>"; }
    function party(P, t) { P = P || {}; return "<h3>" + esc(t) + "</h3>" + dl([[S.name, P.name], [S.nric, P.nric_last4], [S.phone, P.phone], [S.vehicle_no, P.vehicle_no], [S.vehicle_make, P.vehicle_make], [S.insurer, P.insurer]]); }
    var opt = r.settlement_option === "A" ? S.opt_a : S.opt_b + " " + (r.payer === "a" ? S.payer_a : S.payer_b) + ": S$" + r.amount;
    return "<h3>" + esc(S.s_accident) + "</h3>" + dl([[S.date, r.accident_date], [S.time, r.accident_time], [S.location, r.location], [S.description, r.description]]) +
      "<h3>" + esc(S.option) + "</h3><p>" + esc(opt) + "</p>" + party(r.party_a, S.driver_a) + party(r.party_b, S.driver_b);
  }

  // ---------- Driver A: fill ----------
  var form = $("#settle-form");
  if (form) {
    var steps = $$(".step", form), i = 0, bar = $(".prog i"), lab = $(".prog-l"), tpl = lab.getAttribute("data-tpl");
    var photos = [], sigA = pad($("#padA")), intro = $("#settle-intro");
    $("[name=accident_date]", form).value = new Date(Date.now() + 8 * 36e5).toISOString().slice(0, 10);
    $("[name=accident_time]", form).value = new Date(Date.now() + 8 * 36e5).toISOString().slice(11, 16);
    function show(k) {
      i = k; steps.forEach(function (s, j) { s.classList.toggle("on", j === i); });
      bar.style.width = ((i + 1) / steps.length * 100) + "%"; lab.textContent = tpl.replace("{n}", i + 1).replace("{t}", steps.length);
      $("[data-back]", form).disabled = i === 0; $("[data-next]", form).hidden = i === steps.length - 1; $("[data-save]", form).hidden = i !== steps.length - 1;
      if (steps[i].querySelector("#padA")) setTimeout(sigA.init, 30);
      if (steps[i].hasAttribute("data-review")) $("#reviewA").innerHTML = reviewHtml(collect());
      window.scrollTo({ top: form.getBoundingClientRect().top + window.scrollY - 70, behavior: "smooth" });
    }
    function val(n) { var e = form.elements[n]; return e ? (e.type === "checkbox" ? e.checked : String(e.value || "").trim()) : ""; }
    function party(p) { return { name: val(p + "_name"), nric_last4: val(p + "_nric").toUpperCase(), phone: val(p + "_phone"), vehicle_no: val(p + "_vehicle_no").toUpperCase().replace(/\s+/g, ""), vehicle_make: val(p + "_vehicle_make"), insurer: val(p + "_insurer") }; }
    function collect() {
      var opt = (form.querySelector("[name=settlement_option]:checked") || {}).value || "", payer = (form.querySelector("[name=payer]:checked") || {}).value || "";
      return { lang: LANG, accident_date: val("accident_date"), accident_time: val("accident_time"), location: val("location"), description: val("description"), settlement_option: opt, amount: opt === "B" ? val("amount") : "", payer: opt === "B" ? payer : "", party_a: party("a"), party_b: party("b") };
    }
    function check(step) {
      var bad = [];
      $$("[data-req]", step).forEach(function (f) {
        var box = f.closest(".field"), ok;
        if (f.matches(".opts")) ok = !!f.querySelector("input:checked"); else ok = String(f.value || "").trim().length > 0 && (!f.pattern || new RegExp("^(?:" + f.pattern + ")$").test(f.value.trim()));
        if (f.closest("[data-if-b]") && (form.querySelector("[name=settlement_option]:checked") || {}).value !== "B") ok = true;
        box.classList.toggle("bad", !ok); if (!ok) bad.push(f);
      });
      $(".err", form).textContent = bad.length ? S.err_required : "";
      if (bad.length) bad[0].focus && bad[0].focus();
      return !bad.length;
    }
    $("[data-start]").addEventListener("click", function () { intro.hidden = true; form.hidden = false; d.documentElement.classList.add("js"); show(0); });
    $("[data-next]", form).addEventListener("click", function () { if (check(steps[i])) show(i + 1); });
    $("[data-back]", form).addEventListener("click", function () { $(".err", form).textContent = ""; if (i > 0) show(i - 1); });
    form.addEventListener("change", function (e) {
      if (e.target.name === "settlement_option") $("[data-if-b]", form).hidden = e.target.value !== "B";
    });
    $("#photoIn").addEventListener("change", function (e) {
      var files = [].slice.call(e.target.files || []).slice(0, 4 - photos.length);
      Promise.all(files.map(shrink)).then(function (urls) { photos = photos.concat(urls).slice(0, 4); thumbs(); });
      e.target.value = "";
    });
    function thumbs() {
      var t = $("#thumbs"); t.innerHTML = "";
      photos.forEach(function (u, k) { var f = d.createElement("figure"); f.innerHTML = '<img alt="" src="' + u + '"><button type="button" aria-label="' + esc(S.remove) + '">×</button>'; f.querySelector("button").onclick = function () { photos.splice(k, 1); thumbs(); }; t.appendChild(f); });
    }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var err = $(".err", form);
      if (sigA.empty()) { err.textContent = S.err_sign; return; }
      if (!val("consent")) { err.textContent = S.err_consent; return; }
      var body = collect(); body.action = "create"; body.a_signature = sigA.png(); body.consent = true; body.photos = photos;
      var btn = $("[data-save]", form); btn.disabled = true; btn.lastChild.textContent = S.saving; err.textContent = "";
      api(body).then(function (j) {
        btn.disabled = false; btn.lastChild.textContent = S.save;
        if (!j.ok) { err.textContent = j._status === 422 ? S.err_required : S.err_net; return; }
        var rec = Object.assign({}, body, { status: "awaiting_other_party", a_signed_at: new Date().toISOString(), b_signature: "", photos: photos });
        done(j.token, rec);
      }).catch(function () { btn.disabled = false; btn.lastChild.textContent = S.save; err.textContent = S.err_net; });
    });
    function done(token, rec) {
      form.hidden = true; var box = $("#settle-done"); box.hidden = false;
      var link = location.origin + SIGN_URL + "#t=" + token;
      $("[data-pdf]", box).onclick = function () { makePdf(rec); };
      $("[data-share]", box).onclick = function () {
        if (navigator.share) navigator.share({ title: S.pdf_title, text: S.share_text, url: link }).catch(function () {});
        else if (navigator.clipboard) navigator.clipboard.writeText(link).then(function () { $("[data-copied]", box).textContent = S.copied; });
      };
      $("#shareLink").value = link;
      box.scrollIntoView({ behavior: "smooth" });
    }
  }

  // ---------- Driver B: check and sign ----------
  var signBox = $("#sign-view");
  if (signBox) {
    var m = /[#&]t=([A-Za-z0-9_-]{40,64})/.exec(location.hash), token = m && m[1], rec = null, sigB = null;
    var msg = $("#sign-msg");
    if (!token) { msg.textContent = S.bad_link; return; }
    msg.textContent = S.loading;
    api({ action: "get", token: token }).then(function (j) {
      if (!j.ok) { msg.textContent = S.bad_link; return; }
      rec = j.settlement; msg.textContent = ""; render();
    }).catch(function () { msg.textContent = S.err_net; });
    function render() {
      $("#reviewB").innerHTML = reviewHtml(rec) + (rec.photos && rec.photos.length ? '<div class="thumbs">' + rec.photos.map(function (u) { return '<figure><img alt="" src="' + u + '"></figure>'; }).join("") + "</div>" : "");
      signBox.hidden = false;
      var signed = rec.status === "signed";
      $("#sign-form").hidden = signed; $("#signed").hidden = !signed;
      if (!signed && !sigB) { sigB = pad($("#padB")); setTimeout(sigB.init, 30); }
    }
    $("#signed [data-pdf]").onclick = function () { makePdf(rec); };
    $("#sign-form").addEventListener("submit", function (e) {
      e.preventDefault(); var err = $("#sign-form .err");
      if (sigB.empty()) { err.textContent = S.err_sign; return; }
      if (!$("#sign-form [name=consent]").checked) { err.textContent = S.err_consent; return; }
      var btn = $("#sign-form [type=submit]"); btn.disabled = true;
      api({ action: "sign", token: token, b_signature: sigB.png(), consent: true }).then(function (j) {
        btn.disabled = false;
        if (j.ok) { rec = j.settlement; render(); $("#signed").scrollIntoView({ behavior: "smooth" }); }
        else if (j.error === "already_signed") api({ action: "get", token: token }).then(function (g) { if (g.ok) { rec = g.settlement; render(); } });
        else err.textContent = S.err_net;
      }).catch(function () { btn.disabled = false; err.textContent = S.err_net; });
    });
  }
})();
