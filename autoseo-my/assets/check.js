// Free website check in the homepage hero. Text comes from the page (#site-check-text, built from
// strings/<lang>.json), so the same file serves EN, BM and 中文. Loaded with defer; nothing runs until the form is used.
(() => {
  const form = document.getElementById("site-check");
  const dataEl = document.getElementById("site-check-text");
  if (!form || !dataEl) return;
  let T;
  try { T = JSON.parse(dataEl.textContent); } catch { return; }
  const endpoint = form.dataset.endpoint;
  const lang = form.dataset.lang || "en";
  const input = form.querySelector("input");
  const errEl = document.getElementById("site-check-error");
  const prog = document.getElementById("site-check-progress");
  const out = document.getElementById("site-check-result");
  const btn = form.querySelector("button[type=submit]");
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  // Group names the checker sends, mapped to the keys used in strings/<lang>.json (check.groups).
  const GROUPS = { "Google basics": "google", Mobile: "mobile", "AI search": "ai", Customers: "customers" };
  const fill = (s, v) => String(s || "").replace(/\{(\w+)\}/g, (m, k) => (k in v ? v[k] : m));

  function waLink(key, vars) {
    return "https://wa.me/" + T.wa + "?text=" + encodeURIComponent(fill(T.prefills[key], vars));
  }

  function siteOf(raw) {
    const s = String(raw || "").trim().replace(/^https?:\/\//i, "").replace(/\/.*$/, "").replace(/^www\./i, "").toLowerCase();
    return /^[a-z0-9.-]+\.[a-z]{2,}$/.test(s) ? s : "";
  }

  function ctx() {
    const q = new URLSearchParams(location.search);
    return {
      page: location.pathname, trigger: "hero", lang, referrer: document.referrer || "",
      utm_source: q.get("utm_source") || "", utm_medium: q.get("utm_medium") || "", utm_campaign: q.get("utm_campaign") || "",
      automated: navigator.webdriver === true, test: /(^|[?&])qa=1\b/.test(location.search),
    };
  }

  async function call(path, body) {
    const r = await fetch(endpoint + "/" + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ...body, brand: "autoseo" }) });
    let j = {};
    try { j = await r.json(); } catch { /* not JSON */ }
    return { status: r.status, j };
  }

  let timer = 0;
  function progress(on) {
    clearInterval(timer);
    prog.hidden = !on;
    if (!on) return;
    const bar = prog.querySelector(".bar i"), step = prog.querySelector(".step");
    let i = 0;
    const tick = () => {
      step.textContent = T.c.progress[Math.min(i, T.c.progress.length - 1)];
      bar.style.width = Math.min(92, 10 + i * 24) + "%";
      i++;
    };
    tick();
    timer = setInterval(tick, 4000);
  }

  function showError(msg) { errEl.textContent = msg; errEl.hidden = !msg; }

  function waBlock(href, text) {
    return `<div class="checker-cta"><h4 class="hero-check-cta-h">${esc(T.c.wa_heading)}</h4><p>${esc(text)}</p>` +
      `<a class="btn btn-wa-cta" href="${esc(href)}" target="_blank" rel="noopener" data-cta="whatsapp_check_result">${esc(T.c.wa_button)}</a></div>`;
  }

  function failed(site, msg) {
    out.hidden = false;
    out.innerHTML = `<div class="checker-result"><p class="form-error">${esc(msg)}</p>` +
      waBlock(waLink("check_failed", { site: site || input.value.trim() }), T.c.wa_failed_text) +
      `<p class="checker-hint"><button type="button" class="checker-try" data-again>${esc(T.c.again)}</button></p></div>`;
  }

  function item(c) {
    const s = T.c.items[c.id] || { label: c.label, pass: c.detail, fix: c.detail };
    const st = c.status === "pass" ? "pass" : c.status === "warn" ? "warn" : "fail";
    const icon = st === "pass" ? "✓" : st === "warn" ? "!" : "✕";
    return `<li class="chk ${st}"><span class="chk-icon" aria-hidden="true">${icon}</span><div><b>${esc(s.label)}</b> <span class="chk-tag">${esc(T.c.status[st])}</span><p>${esc(st === "pass" ? s.pass : s.fix)}</p></div></li>`;
  }

  function render(site, r, log) {
    const checks = Array.isArray(r.checks) ? r.checks : [];
    const n = (st) => checks.filter((c) => c.status === st).length;
    const score = typeof r.score === "number" ? r.score : 0;
    const tone = score >= 80 ? "" : score >= 50 ? " ok" : " bad";
    const verdict = score >= 80 ? T.c.verdict_good : score >= 50 ? T.c.verdict_ok : T.c.verdict_poor;
    const groups = Object.keys(T.c.groups).map((g) => {
      const todo = checks.filter((c) => GROUPS[c.group] === g && c.status !== "pass");
      const good = checks.filter((c) => GROUPS[c.group] === g && c.status === "pass");
      if (!todo.length && !good.length) return "";
      return `<div class="checker-group"><h4>${esc(T.c.groups[g])}</h4><ul>${todo.map(item).join("")}</ul>` +
        (good.length ? `<details class="hero-check-good"><summary>${esc(T.c.show_good)} (${good.length})</summary><ul>${good.map(item).join("")}</ul></details>` : "") + `</div>`;
    }).join("");
    out.hidden = false;
    out.innerHTML = `<div class="checker-result">` +
      `<div class="checker-head"><div class="score-ring${tone}" style="--p:${score}"><b>${score}</b><small>/100</small></div>` +
      `<div><h3>${esc(fill(T.c.result_for, { site }))}</h3><p>${esc(verdict)}</p>` +
      `<p class="hero-check-counts">${esc(fill(T.c.counts, { fails: n("fail"), warns: n("warn"), passes: n("pass") }))}</p></div></div>` +
      waBlock(waLink("check", { site, score }), T.c.wa_text) +
      `<div class="checker-groups">${groups}</div>` +
      `<div class="checker-speed"><h4>${esc(T.c.speed_label)}</h4><p class="speed-line" id="site-check-speed">${esc(T.c.speed_wait)}</p></div>` +
      `<p class="checker-hint">${esc(T.c.disclaimer)}</p>` +
      `<p class="checker-hint"><button type="button" class="checker-try" data-again>${esc(T.c.again)}</button></p></div>`;
    out.querySelectorAll("[data-cta=whatsapp_check_result]").forEach((a) => a.addEventListener("click", () => tap(log)));
    speedCheck(r.url || input.value, r.share_id);
  }

  // Marks the result row as a WhatsApp lead. text/plain keeps it a simple request (no preflight); fire and forget.
  function tap(log) {
    if (!log || !log.log_id || !log.log_token) return;
    try {
      fetch(endpoint + "/siteCheckContact", { method: "POST", keepalive: true, headers: { "Content-Type": "text/plain" },
        body: JSON.stringify({ event: "whatsapp", log_id: log.log_id, log_token: log.log_token, brand: "autoseo" }) }).catch(() => {});
    } catch { /* ignore */ }
  }

  async function speedCheck(url, shareId) {
    const el = document.getElementById("site-check-speed");
    try {
      const { j } = await call("siteCheck", { url, mode: "speed", share_id: shareId || "" });
      if (!el) return;
      if (!j.ok || typeof j.score !== "number") { el.textContent = T.c.speed_na; return; }
      const cls = j.score >= 90 ? "good" : j.score >= 50 ? "ok" : "bad";
      el.innerHTML = `<b class="${cls}">${j.score}</b>/100`;
    } catch { if (el) el.textContent = T.c.speed_na; }
  }

  out.addEventListener("click", (e) => {
    if (!e.target.closest("[data-again]")) return;
    out.hidden = true; out.innerHTML = "";
    input.value = ""; input.focus();
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const raw = input.value.trim();
    const site = siteOf(raw);
    if (!site) { showError(T.c.err_empty); input.focus(); return; }
    showError(""); out.hidden = true; out.innerHTML = "";
    btn.disabled = true; progress(true);
    try {
      const { status, j } = await call("siteCheck", { url: raw, mode: "basics", ctx: ctx() });
      progress(false);
      if (j && j.ok) render(site, j, { log_id: j.log_id, log_token: j.log_token });
      else failed(site, status === 429 ? T.c.err_rate : j && j.blocked ? T.c.err_blocked : T.c.err_failed);
    } catch {
      progress(false);
      failed(site, T.c.err_network);
    } finally {
      btn.disabled = false;
    }
    out.scrollIntoView({ behavior: "smooth", block: "start" });
  });
})();
