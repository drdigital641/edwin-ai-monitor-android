/* Design-review demo only (?demo=1). Made-up rows, never real clients. Not used by the real dashboard. */
window.AUTOSEO_DEMO = (function () {
  var now = new Date().toISOString();
  var rows = [
    { id: "d1", name: "Demo Workshop A Sdn Bhd (Air-Cond, ADAS & Electrical Specialist)", url: "demo-workshop-a.example", step: "live", open_url: "https://example.com/", health: "ok", taps: { wa: 14, call: 3 }, articles: 6, memo: "Owner prefers WhatsApp after 6pm.", memo_updated_at: now, payment: { plan: "", status: "notset" } },
    { id: "d2", name: "Demo Motor B", url: "demomotorb.example", step: "preview", open_url: "https://example.com/", health: "warn", taps: { wa: 0, call: 0 }, articles: 2, memo: "", memo_updated_at: "" },
    { id: "d3", name: "Demo Tyre C", url: "demotyrec.example", step: "pending", open_url: "", health: "none", taps: {}, articles: 0, memo: "", memo_updated_at: "", new_followup: true }
  ];
  return function (action, b) {
    return new Promise(function (ok) { setTimeout(function () {
      if (action === "me") return ok({ ok: true, user: { email: "demo@example.com" }, group_link: "https://example.com/group" });
      if (action === "clients") return ok({ ok: true, clients: rows.slice() });
      if (action === "save_memo") return ok({ ok: true, memo_updated_at: new Date().toISOString() });
      if (action === "create_client") { rows.unshift({ id: "d" + Date.now(), name: b.company, url: b.url, step: "pending", taps: {}, articles: 0, memo: "", new_followup: true }); return ok({ ok: true, submitted_by: "demo@example.com" }); }
      ok({ ok: false, code: "unknown" });
    }, 250); });
  };
})();
