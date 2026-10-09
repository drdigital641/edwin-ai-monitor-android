const PLAN_PRICE = 20;
const BOOST_PRICE = 10;

// Pricing calculator
const calc = document.getElementById("calc");
if (calc) {
  const total = document.getElementById("calc-total");
  const breakdown = document.getElementById("calc-break");
  const update = () => {
    const runs = Number(calc.querySelector('input[name="runs"]:checked')?.value || 0);
    total.textContent = "S$" + (PLAN_PRICE + runs * BOOST_PRICE);
    breakdown.textContent = runs
      ? "S$" + PLAN_PRICE + " Get Found + " + runs + " × S$" + BOOST_PRICE + " Boost" + (runs > 1 ? "s" : "")
      : "S$" + PLAN_PRICE + " Get Found only";
  };
  calc.addEventListener("change", update);
  update();
}

// Page One backend (Base44): chat assistant, website checker, sign-up and contact form.
const API = "https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions";
const trackCta = (type) => { try { if (window.p1Track) window.p1Track(type); } catch (e) { /* ignore */ } };

async function callApi(name, payload) {
  const res = await fetch(API + "/" + name, {
    method: "POST", credentials: "omit",
    headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
  });
  let data = {};
  try { data = await res.json(); } catch (e) { /* ignore */ }
  return { ok: res.ok, status: res.status, data };
}

function el(tag, cls, text) {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (text != null) n.textContent = text;
  return n;
}

function storageGet(key, store) {
  try { return (store || localStorage).getItem(key); } catch (e) { return null; }
}
function storageSet(key, value, store) {
  try { (store || localStorage).setItem(key, value); } catch (e) { /* private mode */ }
}

// ---------- AI chat assistant (bottom right) ----------
const SUGGESTIONS = ["How much does it cost?", "What do I get for S$20?", "Do you have proof it works?", "How do I sign up?"];
const SAFE_LINK = /^\/(signup\/|pricing\/|get-found\/|seo-boost\/|results\/|report\.html|faq\/|#check|about\/|contact\/|privacy\/|terms\/)$/;

function startChatHelper() {
  const float = document.getElementById("wa-float");
  const root = el("div", "chat-helper");
  root.innerHTML =
    '<div class="chat-teaser" id="chat-teaser" hidden>' +
      '<button class="chat-teaser-close" type="button" aria-label="Dismiss">×</button>' +
      '<p>Questions about getting found on Google? Ask me 👋</p>' +
    '</div>' +
    '<section class="chat-panel" id="chat-panel" role="dialog" aria-label="Chat with Page One Singapore" hidden>' +
      '<header class="chat-head">' +
        '<span class="chat-avatar" aria-hidden="true">1</span>' +
        '<div><b>Page One assistant</b><small>AI · answers instantly, 24/7</small></div>' +
        '<button class="chat-close" type="button" aria-label="Close chat">×</button>' +
      '</header>' +
      '<div class="chat-body" id="chat-body" aria-live="polite"></div>' +
      '<form class="chat-form" id="chat-form">' +
        '<label class="sr-only" for="chat-input">Your message</label>' +
        '<input id="chat-input" type="text" maxlength="600" autocomplete="off" placeholder="Ask a question…">' +
        '<button type="submit" aria-label="Send"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M3 20.5 21 12 3 3.5l.01 6.6L15 12 3.01 13.9z"/></svg></button>' +
      '</form>' +
      '<p class="chat-note">AI assistant, may make mistakes. Need a person? <a href="/contact/">Leave a message</a>.</p>' +
    '</section>' +
    '<button class="chat-launcher" id="chat-launcher" type="button" aria-expanded="false" aria-controls="chat-panel" aria-label="Open chat">' +
      '<span class="chat-ring" aria-hidden="true"></span>' +
      '<svg class="chat-icon" viewBox="0 0 24 24" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-5 4v-4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm3 6.5a1.5 1.5 0 1 0 0 .01zm5 0a1.5 1.5 0 1 0 0 .01zm5 0a1.5 1.5 0 1 0 0 .01z"/></svg>' +
      '<span class="chat-badge" id="chat-badge" aria-hidden="true">1</span>' +
    '</button>';
  document.body.appendChild(root);
  if (float) float.remove();

  const teaser = root.querySelector("#chat-teaser");
  const panel = root.querySelector("#chat-panel");
  const body = root.querySelector("#chat-body");
  const launcher = root.querySelector("#chat-launcher");
  const badge = root.querySelector("#chat-badge");
  const form = root.querySelector("#chat-form");
  const input = root.querySelector("#chat-input");
  let history = [];
  try { history = JSON.parse(storageGet("p1-chat", sessionStorage) || "[]"); } catch (e) { history = []; }
  let busy = false;
  let started = false;

  const scroll = () => { body.scrollTop = body.scrollHeight; };
  const save = () => storageSet("p1-chat", JSON.stringify(history.slice(-20)), sessionStorage);

  const render = (m) => {
    const p = el("p", "chat-msg" + (m.role === "user" ? " chat-me" : ""), m.content);
    body.appendChild(p);
    if (m.links && m.links.length) {
      const list = el("div", "chat-replies");
      for (const l of m.links) {
        if (!SAFE_LINK.test(l.href)) continue;
        const a = el("a", "chat-reply", l.label);
        a.href = l.href;
        list.appendChild(a);
      }
      if (list.childNodes.length) body.appendChild(list);
    }
  };

  const chips = () => {
    const list = el("div", "chat-replies chat-suggest");
    for (const q of SUGGESTIONS) {
      const b = el("button", "chat-reply", q);
      b.type = "button";
      b.addEventListener("click", () => { list.remove(); send(q); });
      list.appendChild(b);
    }
    body.appendChild(list);
  };

  const greet = () => {
    if (started) return;
    started = true;
    if (history.length) { history.forEach(render); scroll(); return; }
    render({ role: "assistant", content: "Hi! 👋 I'm Page One's assistant. Ask me anything about getting found on Google and AI search, our S$20 introductory plan, or signing up." });
    chips();
  };

  async function send(text) {
    text = String(text || "").trim().slice(0, 600);
    if (!text || busy) return;
    busy = true;
    const suggest = body.querySelector(".chat-suggest");
    if (suggest) suggest.remove();
    const mine = { role: "user", content: text };
    history.push(mine);
    render(mine);
    const typing = el("p", "chat-msg chat-typing");
    typing.setAttribute("aria-label", "Typing");
    typing.innerHTML = "<span></span><span></span><span></span>";
    body.appendChild(typing);
    scroll();
    trackCta("chat_message");
    let reply;
    try {
      const r = await callApi("siteChat", {
        messages: history.slice(-8).map((m) => ({ role: m.role, content: m.content })),
        page: location.pathname, session: storageGet("p1-sid", sessionStorage) || "",
      });
      reply = { role: "assistant", content: r.data.reply || "Sorry, I couldn't answer that just now.", links: r.data.links || [] };
    } catch (e) {
      reply = { role: "assistant", content: "Sorry, I can't connect right now. Please try again, or leave a message on our contact page.", links: [{ label: "Contact", href: "/contact/" }] };
    }
    typing.remove();
    history.push(reply);
    save();
    render(reply);
    scroll();
    busy = false;
    input.focus();
  }

  const hideTeaser = () => { teaser.hidden = true; };
  const open = () => {
    panel.hidden = false;
    launcher.setAttribute("aria-expanded", "true");
    launcher.classList.add("is-open");
    badge.hidden = true;
    hideTeaser();
    storageSet("p1-chat-seen", "1");
    greet();
    scroll();
    if (window.matchMedia("(min-width: 768px)").matches) input.focus();
    trackCta("chat_open");
  };
  const close = () => {
    panel.hidden = true;
    launcher.setAttribute("aria-expanded", "false");
    launcher.classList.remove("is-open");
    launcher.focus();
  };
  window.p1OpenChat = open;

  form.addEventListener("submit", (e) => { e.preventDefault(); const t = input.value; input.value = ""; send(t); });
  launcher.addEventListener("click", () => (panel.hidden ? open() : close()));
  root.querySelector(".chat-close").addEventListener("click", close);
  teaser.querySelector("p").addEventListener("click", open);
  teaser.querySelector(".chat-teaser-close").addEventListener("click", () => { hideTeaser(); storageSet("p1-chat-seen", "1"); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !panel.hidden) close(); });
  document.querySelectorAll("[data-open-chat]").forEach((b) => b.addEventListener("click", open));

  // Pop the teaser bubble once, on larger screens only, so it never covers content on phones
  const roomy = window.matchMedia("(min-width: 768px)").matches;
  if (storageGet("p1-chat-seen")) {
    badge.hidden = true;
  } else if (roomy) {
    setTimeout(() => {
      if (!panel.hidden) return;
      teaser.hidden = false;
      setTimeout(hideTeaser, 12000);
      window.addEventListener("scroll", hideTeaser, { once: true, passive: true });
    }, 8000);
  }
}

startChatHelper();

// ---------- Website checker (homepage) ----------
const checker = document.getElementById("checker-form");
if (checker) {
  const out = document.getElementById("checker-result");
  const err = document.getElementById("checker-error");
  const btn = checker.querySelector("button");
  const ICON = { pass: "✓", warn: "!", fail: "✕" };
  const showError = (msg) => { err.textContent = msg; err.hidden = false; };

  const renderBasics = (r) => {
    out.textContent = "";
    const head = el("div", "checker-head");
    const ring = el("div", "score-ring " + (r.score >= 85 ? "good" : r.score >= 60 ? "ok" : "bad"));
    ring.style.setProperty("--p", r.score);
    ring.appendChild(el("b", null, String(r.score)));
    ring.appendChild(el("small", null, "/100"));
    head.appendChild(ring);
    const t = el("div");
    t.appendChild(el("h3", null, r.host));
    const fails = r.checks.filter((c) => c.status === "fail").length;
    const warns = r.checks.filter((c) => c.status === "warn").length;
    t.appendChild(el("p", null, fails + warns === 0 ? "Excellent. Your website covers all the basics we check."
      : `${fails} problem${fails === 1 ? "" : "s"} and ${warns} thing${warns === 1 ? "" : "s"} to improve.`));
    head.appendChild(t);
    out.appendChild(head);

    const groups = {};
    r.checks.forEach((c) => (groups[c.group] = groups[c.group] || []).push(c));
    const order = { fail: 0, warn: 1, pass: 2 };
    const grid = el("div", "checker-groups");
    for (const g of Object.keys(groups)) {
      const box = el("div", "checker-group");
      box.appendChild(el("h4", null, g));
      const ul = el("ul");
      for (const c of groups[g].sort((a, b) => order[a.status] - order[b.status])) {
        const li = el("li", "chk " + c.status);
        li.appendChild(el("span", "chk-icon", ICON[c.status]));
        const d = el("div");
        d.appendChild(el("b", null, c.label));
        d.appendChild(el("p", null, c.detail));
        li.appendChild(d);
        ul.appendChild(li);
      }
      box.appendChild(ul);
      grid.appendChild(box);
    }
    out.appendChild(grid);

    const speed = el("div", "checker-speed");
    speed.appendChild(el("h4", null, "Mobile speed (Google PageSpeed)"));
    const sp = el("p", "fine", "Measuring with Google… this can take up to 30 seconds.");
    speed.appendChild(sp);
    out.appendChild(speed);

    const ctaBox = el("div", "checker-cta");
    ctaBox.appendChild(el("p", null, fails + warns ? "Want us to fix these for you? Our Get Found plan covers all of this, from S$20 a month (introductory price)." : "Great foundations. Want more customers from Google and AI search? See what we do for S$20 a month."));
    const row = el("div", "cta-row");
    const s1 = el("a", "btn", "Sign up from S$20/month"); s1.href = "/signup/";
    const s2 = el("button", "btn btn-ghost", "Ask our assistant"); s2.type = "button";
    s2.addEventListener("click", () => window.p1OpenChat && window.p1OpenChat());
    row.appendChild(s1); row.appendChild(s2);
    ctaBox.appendChild(row);
    out.appendChild(ctaBox);
    return sp;
  };

  const renderSpeed = (sp, r, url) => {
    if (!r || !r.ok || r.score == null) {
      sp.textContent = "";
      sp.append("Google's speed test is busy right now. ");
      const a = el("a", "link", "Run it on PageSpeed Insights ↗");
      a.href = "https://pagespeed.web.dev/analysis?url=" + encodeURIComponent(url);
      a.target = "_blank"; a.rel = "noopener";
      sp.appendChild(a);
      return;
    }
    sp.className = "speed-line";
    sp.textContent = "";
    const score = el("b", r.score >= 90 ? "good" : r.score >= 50 ? "ok" : "bad", r.score + "/100");
    sp.appendChild(score);
    const bits = [];
    if (r.lab && r.lab.lcp) bits.push("Main content shows in " + r.lab.lcp);
    if (r.lab && r.lab.cls) bits.push("layout shift " + r.lab.cls);
    if (r.field_overall) bits.push("real-user Core Web Vitals: " + r.field_overall.toLowerCase());
    sp.append(" " + bits.join(" · "));
  };

  checker.addEventListener("submit", async (e) => {
    e.preventDefault();
    const url = checker.url.value.trim();
    err.hidden = true;
    if (!url) { showError("Enter your website address, like yourbusiness.com.sg"); return; }
    btn.disabled = true;
    btn.textContent = "Checking…";
    out.hidden = false;
    out.textContent = "";
    out.appendChild(el("p", "checker-loading", "Checking " + url + " … this takes about 10 seconds."));
    trackCta("checker_run");
    try {
      const r = await callApi("siteCheck", { url, mode: "basics" });
      if (!r.data || !r.data.ok) { out.hidden = true; showError((r.data && r.data.error) || "We couldn't check that website. Please try again."); return; }
      storageSet("p1-site", r.data.url, sessionStorage);
      const sp = renderBasics(r.data);
      out.scrollIntoView({ behavior: "smooth", block: "start" });
      callApi("siteCheck", { url: r.data.url, mode: "speed" }).then((s) => renderSpeed(sp, s.data, r.data.url)).catch(() => renderSpeed(sp, null, r.data.url));
    } catch (e2) {
      out.hidden = true;
      showError("We couldn't reach our checker. Please try again in a moment.");
    } finally {
      btn.disabled = false;
      btn.textContent = "Check my website";
    }
  });
}

// ---------- Sign up (Stripe Checkout) ----------
const signup = document.getElementById("signup-form");
if (signup) {
  const params = new URLSearchParams(location.search);
  const err = signup.querySelector(".form-error");
  const btn = signup.querySelector('button[type="submit"]');
  const total = document.getElementById("signup-total");
  const boostsWanted = params.get("boosts");
  if (boostsWanted && signup.querySelector('input[name="boosts"][value="' + boostsWanted + '"]')) {
    signup.querySelector('input[name="boosts"][value="' + boostsWanted + '"]').checked = true;
  }
  const site = storageGet("p1-site", sessionStorage);
  if (site && !signup.website.value) signup.website.value = site;
  if (params.get("cancelled")) document.getElementById("signup-cancelled").hidden = false;
  const update = () => {
    const n = Number(signup.querySelector('input[name="boosts"]:checked').value || 0);
    total.textContent = "S$" + (PLAN_PRICE + n * BOOST_PRICE);
  };
  signup.addEventListener("change", update);
  update();
  signup.addEventListener("submit", async (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(signup).entries());
    err.hidden = true;
    if (!String(d.business || "").trim() || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(d.email || "").trim())) {
      err.textContent = "Please enter your business name and a valid email.";
      err.hidden = false;
      return;
    }
    btn.disabled = true;
    btn.textContent = "Opening secure payment…";
    trackCta("signup_start");
    try {
      const r = await callApi("createCheckout", { business: d.business, email: d.email, website: d.website, boosts: Number(d.boosts || 0) });
      if (r.data && r.data.url) { location.href = r.data.url; return; }
      err.textContent = (r.data && r.data.error) || "We couldn't start checkout. Please try again.";
    } catch (e2) {
      err.textContent = "We couldn't reach the payment page. Please check your connection and try again.";
    }
    err.hidden = false;
    btn.disabled = false;
    btn.textContent = "Continue to secure payment";
  });
}

// Pricing calculator -> sign-up link keeps the chosen number of Boosts
const calcSignup = document.getElementById("calc-signup");
if (calcSignup && calc) {
  const sync = () => { calcSignup.href = "/signup/?boosts=" + (calc.querySelector('input[name="runs"]:checked')?.value || 0); };
  calc.addEventListener("change", sync);
  sync();
}

// ---------- SEO Boost top-up ----------
const topup = document.getElementById("topup-form");
if (topup) {
  const err = topup.querySelector(".form-error");
  const btn = topup.querySelector('button[type="submit"]');
  topup.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = topup.email.value.trim();
    err.hidden = true;
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { err.textContent = "Please enter the email you subscribed with."; err.hidden = false; return; }
    btn.disabled = true;
    btn.textContent = "Opening secure payment…";
    trackCta("boost_topup_start");
    try {
      const r = await callApi("createCheckout", { kind: "boosts", email, boosts: Number(topup.boosts.value) });
      if (r.data && r.data.url) { location.href = r.data.url; return; }
      err.textContent = (r.data && r.data.error) || "We couldn't start checkout. Please try again.";
    } catch (e2) {
      err.textContent = "We couldn't reach the payment page. Please try again.";
    }
    err.hidden = false;
    btn.disabled = false;
    btn.textContent = "Pay securely with Stripe";
  });
}

// ---------- Contact form ----------
const lead = document.getElementById("lead-form");
if (lead) {
  const err = lead.querySelector(".form-error");
  const btn = lead.querySelector('button[type="submit"]');
  const site = storageGet("p1-site", sessionStorage);
  if (site && !lead.website.value) lead.website.value = site;
  lead.addEventListener("submit", async (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(lead).entries());
    err.hidden = true;
    const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(d.email || "").trim());
    if (!String(d.name || "").trim() || (!emailOk && String(d.phone || "").replace(/\D/g, "").length < 7)) {
      err.textContent = "Please add your name and an email or phone number so we can reply.";
      err.hidden = false;
      return;
    }
    btn.disabled = true;
    btn.textContent = "Sending…";
    try {
      const r = await callApi("siteLead", { ...d, source: "contact_form", page: location.pathname });
      if (r.data && r.data.ok) {
        lead.hidden = true;
        document.getElementById("lead-done").hidden = false;
        trackCta("lead_submit");
        return;
      }
      err.textContent = (r.data && r.data.error) || "Something went wrong. Please try again.";
    } catch (e2) {
      err.textContent = "We couldn't send your message. Please check your connection and try again.";
    }
    err.hidden = false;
    btn.disabled = false;
    btn.textContent = "Send message";
  });
}

const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Hero search bar: types a few real-world searches in a loop
const typed = document.getElementById("typed");
if (typed && !reducedMotion) {
  const queries = ["aircon servicing near me", "sofa cleaning singapore", "car workshop ang mo kio", "best tuition centre tampines"];
  let q = 0;
  let i = queries[0].length;
  let deleting = true;
  const tick = () => {
    const text = queries[q];
    if (deleting) {
      i--;
      if (i <= 0) { deleting = false; q = (q + 1) % queries.length; }
    } else {
      i++;
      if (i >= queries[q].length) { deleting = true; typed.textContent = queries[q]; return setTimeout(tick, 2200); }
    }
    typed.textContent = (deleting ? text : queries[q]).slice(0, Math.max(i, 0));
    setTimeout(tick, deleting ? 35 : 70);
  };
  setTimeout(tick, 2500);
}

// Fade sections in as they scroll into view
const revealEls = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window && !reducedMotion) {
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
    }
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
  revealEls.forEach((el) => io.observe(el));
} else {
  revealEls.forEach((el) => el.classList.add("in"));
}

// Client stories carousel: auto-rotates, pauses on hover/focus, swipeable
const track = document.getElementById("carousel-track");
if (track) {
  const slides = [...track.children];
  const dotsWrap = document.getElementById("carousel-dots");
  const carousel = document.getElementById("carousel");
  let current = 0;
  let timer = null;

  const dots = slides.map((_, n) => {
    const b = document.createElement("button");
    b.type = "button";
    b.setAttribute("aria-label", "Show story " + (n + 1));
    b.addEventListener("click", () => { go(n); restart(); });
    dotsWrap.appendChild(b);
    return b;
  });

  const mark = (n) => {
    current = n;
    dots.forEach((d, k) => d.setAttribute("aria-current", k === n ? "true" : "false"));
  };
  const go = (n) => {
    const target = (n + slides.length) % slides.length;
    track.scrollTo({ left: slides[target].offsetLeft - track.offsetLeft, behavior: reducedMotion ? "auto" : "smooth" });
    mark(target);
  };
  const stop = () => { clearInterval(timer); timer = null; };
  const start = () => { if (!reducedMotion && !timer) timer = setInterval(() => go(current + 1), 6000); };
  const restart = () => { stop(); start(); };

  document.getElementById("carousel-prev").addEventListener("click", () => { go(current - 1); restart(); });
  document.getElementById("carousel-next").addEventListener("click", () => { go(current + 1); restart(); });
  carousel.addEventListener("mouseenter", stop);
  carousel.addEventListener("mouseleave", start);
  carousel.addEventListener("focusin", stop);
  carousel.addEventListener("focusout", start);
  track.addEventListener("pointerdown", stop);

  // Keep the dots in sync when people swipe
  let scrollTimer;
  track.addEventListener("scroll", () => {
    clearTimeout(scrollTimer);
    scrollTimer = setTimeout(() => {
      const n = Math.round(track.scrollLeft / track.clientWidth);
      if (n !== current) mark(Math.min(Math.max(n, 0), slides.length - 1));
    }, 120);
  }, { passive: true });

  mark(0);
  start();
}

// Mobile menu
const menuBtn = document.getElementById("menu-btn");
const nav = document.getElementById("nav");
if (menuBtn && nav) {
  menuBtn.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    menuBtn.textContent = open ? "✕" : "☰";
  });
  nav.addEventListener("click", (e) => {
    if (e.target.closest("a")) {
      nav.classList.remove("open");
      menuBtn.setAttribute("aria-expanded", "false");
      menuBtn.textContent = "☰";
    }
  });
}

// Anonymous visit and button-click counts for the Page One controller (Base44).
// No cookies and no personal details: page, referrer type, device and a random id only.
// Skipped when the browser sends Do Not Track or is automated.
(() => {
  const APP = "6ac7f2548a9c3877449e2772";
  if (navigator.doNotTrack === "1" || window.doNotTrack === "1" || navigator.webdriver) return;
  if (!/(^|\.)pageonesingapore\.com$/.test(location.hostname)) return;
  const rid = () => Math.random().toString(36).slice(2) + Date.now().toString(36);
  const keep = (store, key) => {
    try { let v = store.getItem(key); if (!v) { v = rid(); store.setItem(key, v); } return v; } catch (e) { return rid(); }
  };
  const visitor = keep(localStorage, "p1-vid");
  const session = keep(sessionStorage, "p1-sid");
  const params = new URLSearchParams(location.search);
  const ref = document.referrer && !document.referrer.includes(location.hostname) ? document.referrer : "";
  const source = (() => {
    const r = ref.toLowerCase(), u = (params.get("utm_source") || "").toLowerCase();
    if (/chatgpt|openai/.test(r + u)) return "chatgpt";
    if (/perplexity/.test(r + u)) return "perplexity";
    if (/gemini|bard/.test(r + u)) return "gemini";
    if (/google\./.test(r) || u === "google") return params.get("gclid") ? "google_ads" : "google";
    if (/bing\./.test(r)) return "bing";
    if (/facebook|instagram|tiktok|linkedin|t\.co|twitter|x\.com/.test(r + u)) return "social";
    if (u) return u;
    return r ? "referral" : "direct";
  })();
  const ua = navigator.userAgent;
  const base = {
    session_id: session, visitor_id: visitor, page_path: location.pathname,
    referrer: ref.slice(0, 300), utm_source: params.get("utm_source") || "", utm_medium: params.get("utm_medium") || "",
    utm_campaign: params.get("utm_campaign") || "", traffic_source: source,
    device_type: /Mobi|Android|iPhone/i.test(ua) ? "mobile" : /iPad|Tablet/i.test(ua) ? "tablet" : "desktop",
    browser: /Edg\//.test(ua) ? "edge" : /Chrome\//.test(ua) ? "chrome" : /Safari\//.test(ua) ? "safari" : /Firefox\//.test(ua) ? "firefox" : "other",
  };
  const send = (entity, extra) => {
    try {
      fetch("https://base44.app/api/apps/" + APP + "/entities/" + entity, {
        method: "POST", credentials: "omit", keepalive: true,
        headers: { "Content-Type": "application/json" }, body: JSON.stringify({ ...base, ...extra }),
      }).catch(() => {});
    } catch (e) { /* tracking must never break the page */ }
  };
  send("PageView", {});
  document.addEventListener("click", (e) => {
    const a = e.target.closest && e.target.closest('a[href*="wa.me/"]');
    if (!a) return;
    const type = a.classList.contains("chat-reply") ? "chat_reply" : a.classList.contains("footer-wa") ? "footer_whatsapp"
      : a.closest(".article-cta") ? "article_cta" : a.classList.contains("btn") ? "whatsapp_button" : "whatsapp_link";
    send("CtaClick", { cta_type: type });
  }, true);
  window.p1Track = (type) => send("CtaClick", { cta_type: type });
  document.addEventListener("click", (e) => {
    const a = e.target.closest && e.target.closest('a[href^="/signup/"]');
    if (a) send("CtaClick", { cta_type: "signup_link" });
  }, true);
})();
