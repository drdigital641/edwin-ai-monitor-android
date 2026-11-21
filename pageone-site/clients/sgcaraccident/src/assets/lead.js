/* SGCarAccident lead forms v1 (21 Nov 2026). Every enquiry goes to Edwin's WhatsApp for now.
   Each enquiry carries: reference (pathway code + date + 4 random digits), pathway category, the fields, a consent line
   with time, and the page. The same object shape (window.SCA_LEAD_SCHEMA below) is what a future lead API will store,
   so routing to workshops / reporting-centre referrals / partner fees can be added without changing the forms.
   Drafts are kept in sessionStorage for this visit only, so Back never loses what was typed. */
(function () {
  var d = document, UI = {};
  try { UI = JSON.parse(d.getElementById("ui").textContent); } catch (e) {}
  var LANG = d.body.getAttribute("data-lang") || "en";
  function ss(k, v) { try { if (v === undefined) return JSON.parse(sessionStorage.getItem(k) || "null"); sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) { return null; } }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  window.SCA_LEAD_SCHEMA = { v: 1, fields: ["ref", "pathway", "category", "lang", "page", "created_at", "consent", "consent_at", "data{}", "photos_via"] };

  [].slice.call(d.querySelectorAll("form.lead")).forEach(function (f) {
    var KEY = "sca_lead_" + f.id + "_" + LANG, saved = ss(KEY) || {};
    var els = [].slice.call(f.querySelectorAll("input,select,textarea")).filter(function (el) { return el.name && el.type !== "checkbox"; });
    els.forEach(function (el) {
      if (saved[el.name]) el.value = saved[el.name];
      ["input", "change"].forEach(function (t) { el.addEventListener(t, function () { saved[el.name] = el.value; ss(KEY, saved); el.closest(".field").classList.remove("bad"); }); });
    });
    var err = f.querySelector(".err"), sent = f.querySelector(".sent"), reopen = f.querySelector("[data-reopen]");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var miss = [];
      els.forEach(function (el) {
        var bad = el.required && !el.value.trim();
        if (el.type === "tel" && el.value.trim() && !/^[+\d][\d\s-]{6,}$/.test(el.value.trim())) bad = true;
        el.closest(".field").classList.toggle("bad", bad);
        if (bad) miss.push(f.querySelector('label[for="' + el.id + '"]').textContent.replace(/\s*\(.*\)$/, ""));
      });
      var c = f.querySelector("[name=consent]");
      if (miss.length) { err.textContent = (UI.req || "Please fill in: {f}").replace("{f}", miss.join(", ")); f.querySelector(".bad input,.bad textarea,.bad select").focus(); return; }
      if (!c.checked) { err.textContent = UI.consent || "Please tick the consent box."; c.focus(); return; }
      err.textContent = "";
      var now = new Date();
      var ref = f.getAttribute("data-code") + "-" + String(now.getFullYear()).slice(2) + pad(now.getMonth() + 1) + pad(now.getDate()) + "-" + (1000 + Math.floor(Math.random() * 9000));
      var stamp = pad(now.getDate()) + "/" + pad(now.getMonth() + 1) + "/" + now.getFullYear() + " " + pad(now.getHours()) + ":" + pad(now.getMinutes());
      var lines = ["SGCarAccident enquiry", "Ref: " + ref, "Category: " + f.getAttribute("data-cat"), ""];
      var data = {};
      els.forEach(function (el) {
        var v = el.value.trim(); if (!v) return;
        data[el.name] = v;
        lines.push(f.querySelector('label[for="' + el.id + '"]').textContent.replace(/\s*\(.*\)$/, "") + ": " + v);
      });
      if (f.querySelector(".photo-note")) lines.push("", f.querySelector(".photo-note").textContent);
      lines.push("", "Consent: " + c.parentNode.textContent.trim() + " [" + stamp + "]", "Page: " + location.href.split("#")[0]);
      var lead = { v: 1, ref: ref, pathway: f.getAttribute("data-lead"), category: f.getAttribute("data-cat"), lang: LANG, page: location.pathname,
                   created_at: now.toISOString(), consent: true, consent_at: now.toISOString(), data: data, photos_via: "whatsapp" };
      try { window.SCA_LAST_LEAD = lead; } catch (x) {}
      var u = "https://wa.me/" + f.getAttribute("data-wa") + "?text=" + encodeURIComponent(lines.join("\n"));
      reopen.href = u; reopen.target = "_blank"; reopen.rel = "noopener";
      sent.hidden = false;
      var w = null; try { w = window.open(u, "_blank"); if (w) w.opener = null; } catch (x) {}
      if (!w) { setTimeout(function () { location.href = u; }, 50); }
      sent.scrollIntoView({ behavior: "smooth", block: "center" });
    });
  });
})();
