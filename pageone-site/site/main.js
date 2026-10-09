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

// Edwin's WhatsApp (country code, no + or spaces). Every enquiry goes here for now.
const WHATSAPP_NUMBER = "6597856612";
// Pre-filled WhatsApp message, ending with the page it came from so Edwin knows the context.
function waLink(text) {
  const from = "\n\n(From pageonesingapore.com" + location.pathname + ")";
  return "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text + from);
}
function openWhatsApp(text, type) {
  trackCta(type || "whatsapp_form");
  const url = waLink(text);
  const w = window.open(url, "_blank", "noopener");
  if (!w) location.href = url;
}
const trackCta = (type) => { try { if (window.p1Track) window.p1Track(type); } catch (e) { /* ignore */ } };

// Retries twice on network errors and temporary server errors (502/503/504), so a brief
// platform hiccup doesn't show visitors an error.
async function callApi(name, payload, attempt = 0) {
  let res;
  try {
    res = await fetch(API + "/" + name, {
      method: "POST", credentials: "omit",
      headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload),
    });
  } catch (e) {
    if (attempt < 2) { await new Promise((r) => setTimeout(r, 1500 * (attempt + 1))); return callApi(name, payload, attempt + 1); }
    throw e;
  }
  if ([502, 503, 504].includes(res.status) && attempt < 2) {
    await new Promise((r) => setTimeout(r, 1500 * (attempt + 1)));
    return callApi(name, payload, attempt + 1);
  }
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

// ---------- WhatsApp chat helper (bottom right) ----------
const QUICK_REPLIES = [
  { label: "I want to sign up (S$20/month)", text: "Hi Edwin, I'd like to sign up for the Get Found plan (S$20/month).\nMy business: \nWebsite (if any): " },
  { label: "I don't have a website yet", text: "Hi Edwin, I don't have a website yet. Can Page One build one for my business?\nMy business: " },
  { label: "I already have a website", text: "Hi Edwin, I already have a website. Can you add an SEO landing page and help it show up on Google?\nMy website: " },
  { label: "How much will it cost me?", text: "Hi Edwin, how much would the Get Found plan and SEO Boosts cost for my business?" },
];

function startChatHelper() {
  const float = document.getElementById("wa-float");
  const root = el("div", "chat-helper");
  root.innerHTML =
    '<div class="chat-teaser" id="chat-teaser" hidden>' +
      '<button class="chat-teaser-close" type="button" aria-label="Dismiss">×</button>' +
      '<p>Questions about getting found on Google? Chat with Edwin 👋</p>' +
    '</div>' +
    '<section class="chat-panel" id="chat-panel" role="dialog" aria-label="Chat with Page One Singapore on WhatsApp" hidden>' +
      '<header class="chat-head">' +
        '<span class="chat-avatar" aria-hidden="true">1</span>' +
        '<div><b>Edwin, Page One Singapore</b><small>Replies personally on WhatsApp</small></div>' +
        '<button class="chat-close" type="button" aria-label="Close chat">×</button>' +
      '</header>' +
      '<div class="chat-body" id="chat-body"></div>' +
      '<form class="chat-form" id="chat-form">' +
        '<label class="sr-only" for="chat-input">Your message</label>' +
        '<input id="chat-input" type="text" maxlength="600" autocomplete="off" placeholder="Type your question…">' +
        '<button type="submit" aria-label="Send on WhatsApp"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M3 20.5 21 12 3 3.5l.01 6.6L15 12 3.01 13.9z"/></svg></button>' +
      '</form>' +
      '<p class="chat-note">Opens WhatsApp with your message. No obligation.</p>' +
    '</section>' +
    '<button class="chat-launcher" id="chat-launcher" type="button" aria-expanded="false" aria-controls="chat-panel" aria-label="Open chat">' +
      '<span class="chat-ring" aria-hidden="true"></span>' +
      '<svg class="chat-icon" viewBox="0 0 24 24" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.8 2.3 1 2.5c.1.2 1.7 2.6 4.1 3.6 1.5.7 2.1.7 2.9.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>' +
      '<span class="chat-badge" id="chat-badge" data-n="1" aria-hidden="true"></span>' +
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
  let filled = false;

  const fill = () => {
    if (filled) return;
    filled = true;
    body.appendChild(el("p", "chat-msg", "Hi! 👋 I'm Edwin from Page One Singapore."));
    body.appendChild(el("p", "chat-msg", "We help Singapore businesses get found on Google, Google Maps and AI, from S$20 a month (introductory price). Pick a topic or type your question, and we'll continue on WhatsApp."));
    const list = el("div", "chat-replies");
    const checked = storageGet("p1-check", sessionStorage);
    const replies = checked ? [{ label: "Help me fix my website check results", text: "Hi Edwin, I ran the website checker:\n" + checked + "\nCan you help me fix these?" }, ...QUICK_REPLIES] : QUICK_REPLIES;
    for (const q of replies) {
      const a = el("a", "chat-reply", q.label);
      a.href = waLink(q.text);
      a.target = "_blank";
      a.rel = "noopener";
      list.appendChild(a);
    }
    body.appendChild(list);
  };

  const hideTeaser = () => { teaser.hidden = true; };
  const open = () => {
    panel.hidden = false;
    launcher.setAttribute("aria-expanded", "true");
    launcher.classList.add("is-open");
    badge.hidden = true;
    hideTeaser();
    storageSet("p1-chat-seen", "1");
    fill();
    trackCta("chat_open");
  };
  const close = () => {
    panel.hidden = true;
    launcher.setAttribute("aria-expanded", "false");
    launcher.classList.remove("is-open");
    launcher.focus();
  };
  window.p1OpenChat = open;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const t = input.value.trim();
    if (!t) { input.focus(); return; }
    input.value = "";
    openWhatsApp("Hi Edwin, " + t, "chat_typed");
  });
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
  const btn = checker.querySelector("button[type=\"submit\"]");
  const ICON = { pass: "✓", warn: "!", fail: "✕" };
  // Each check in plain words, with the industry term and why it matters to a business owner
  const PLAIN = {
    status: ["Your website opens", "HTTP status", "If the page doesn't open, customers leave and Google drops it."],
    https: ["Secure padlock", "HTTPS / SSL", "Without it, browsers show \"Not secure\", which puts customers off."],
    http_redirect: ["Always opens the secure version", "HTTP to HTTPS redirect", "Old links and typed addresses can still land on the unsafe version."],
    title: ["Headline shown on Google", "Title tag", "It's the blue headline people see in Google. A clear one gets more taps."],
    description: ["Short description on Google", "Meta description", "The lines under your headline in Google: your sales pitch in the results."],
    h1: ["Clear main heading", "H1", "Tells visitors and Google in one line what you do."],
    indexable: ["Allowed to appear on Google", "Indexability (noindex)", "If this is blocked, the page can't show up on Google at all."],
    canonical: ["Main address set", "Canonical tag", "Stops Google splitting the page into duplicate copies."],
    robots: ["Instructions for search engines", "robots.txt", "A small file that tells Google what it may read."],
    sitemap: ["List of your pages for Google", "XML sitemap", "Helps Google find every page, not just the homepage."],
    pages: ["Enough pages to be found", "Indexable pages", "Each service and area needs its own page to show up for those searches."],
    internal_links: ["Links between your pages", "Internal linking", "Helps visitors and Google discover your other pages."],
    viewport: ["Fits phone screens", "Mobile viewport", "Most customers search on their phone. A site that doesn't fit loses them."],
    response: ["Website responds quickly", "Server response time", "Slow sites lose impatient visitors and can rank lower."],
    weight: ["Page isn't too heavy", "HTML page weight", "Heavy pages load slowly on mobile data."],
    schema: ["Business details labelled for Google and AI", "Structured data (Schema.org)", "Lets Google and ChatGPT read your name, address, hours and services correctly."],
    ai_bots: ["ChatGPT and AI tools can read your site", "AI crawler access", "If AI tools are blocked, they can't recommend you."],
    content: ["Enough words to explain your business", "Indexable text content", "Google and AI read words. Too few, and they can't tell what you offer."],
    h2: ["Page split into clear sections", "H2 subheadings", "Makes the page easy to scan, for people and for AI."],
    llms: ["Summary for AI tools", "llms.txt", "A short plain-text summary that helps AI tools describe you (nice to have)."],
    og: ["Nice preview when shared on WhatsApp", "Open Graph tags", "Shared links show a picture and title instead of a bare address."],
    alt: ["Photos described in words", "Image alt text", "Google can't see photos. Descriptions help them appear in Google Images."],
    local: ["Phone number and location shown", "NAP: name, address, phone", "Google uses this to show you to customers nearby."],
    contact: ["One-tap call or WhatsApp", "Click-to-call / click-to-chat", "Ready customers can reach you instantly instead of hunting for your number."],
  };
  const GROUP = { "Google basics": "Showing up on Google", "Mobile": "Phones and speed", "AI search": "ChatGPT and AI assistants", "Customers": "Turning visitors into customers" };
  const plainLabel = (c) => (PLAIN[c.id] ? PLAIN[c.id][0] : c.label);
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
    const meaning = el("p", "score-meaning");
    meaning.append("What your score means: ");
    meaning.appendChild(el("b", "good", "85–100"));
    meaning.append(" in good shape · ");
    meaning.appendChild(el("b", "ok", "60–84"));
    meaning.append(" customers can find you, but you're missing some · ");
    meaning.appendChild(el("b", "bad", "below 60"));
    meaning.append(" many customers won't find you. Each item shows the plain-English meaning, with the technical name in grey. ");
    const gl = el("a", "link", "New to these terms? SEO explained simply →");
    gl.href = "/seo-explained/";
    meaning.appendChild(gl);
    out.appendChild(meaning);

    const groups = {};
    r.checks.forEach((c) => (groups[c.group] = groups[c.group] || []).push(c));
    const order = { fail: 0, warn: 1, pass: 2 };
    const grid = el("div", "checker-groups");
    for (const g of Object.keys(groups)) {
      const box = el("div", "checker-group");
      box.appendChild(el("h4", null, GROUP[g] || g));
      const ul = el("ul");
      for (const c of groups[g].sort((a, b) => order[a.status] - order[b.status])) {
        const li = el("li", "chk " + c.status);
        li.appendChild(el("span", "chk-icon", ICON[c.status]));
        const d = el("div");
        const name = el("b", null, plainLabel(c));
        if (PLAIN[c.id]) { name.append(" "); name.appendChild(el("span", "term", PLAIN[c.id][1])); }
        d.appendChild(name);
        d.appendChild(el("p", null, c.detail));
        if (c.status !== "pass" && PLAIN[c.id]) d.appendChild(el("p", "chk-why", "Why it matters: " + PLAIN[c.id][2]));
        li.appendChild(d);
        ul.appendChild(li);
      }
      box.appendChild(ul);
      grid.appendChild(box);
    }
    out.appendChild(grid);

    const speed = el("div", "checker-speed");
    speed.appendChild(el("h4", null, "How fast it loads on a phone (Google PageSpeed)"));
    const sp = el("p", "fine", "Measuring with Google… this can take up to 30 seconds.");
    speed.appendChild(sp);
    out.appendChild(speed);

    // Summary Edwin sees in the pre-filled WhatsApp message
    const issues = r.checks.filter((c) => c.status !== "pass").sort((a, b) => order[a.status] - order[b.status])
      .slice(0, 6).map((c) => "- " + plainLabel(c) + (c.status === "fail" ? " (problem)" : " (to improve)"));
    const summary = r.host + ": " + r.score + "/100" + (issues.length ? "\n" + issues.join("\n") : "");
    storageSet("p1-check", summary, sessionStorage);
    const ctaBox = el("div", "checker-cta");
    ctaBox.appendChild(el("p", null, fails + warns ? "Want help fixing these? Chat with Edwin on WhatsApp. Your results are sent with your message, so he can tell you what to fix first. Our Get Found plan covers all of this from S$20 a month (introductory price)." : "Great foundations. Want more customers from Google and AI search? Chat with Edwin about what we can do for S$20 a month."));
    const row = el("div", "cta-row");
    const s1 = el("a", "btn", "Chat with Edwin about my results");
    s1.href = waLink("Hi Edwin, I ran the website checker on pageonesingapore.com:\n" + summary + "\nCan you help me improve my website?");
    s1.target = "_blank"; s1.rel = "noopener";
    const s2 = el("a", "btn btn-ghost", "See plans from S$20/month"); s2.href = "/pricing/";
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
    if (r.lab && r.lab.lcp) bits.push("main content shows in " + r.lab.lcp + " (LCP)");
    if (r.lab && r.lab.cls) bits.push("page jumps around: " + r.lab.cls + " (CLS, lower is better)");
    if (r.field_overall) bits.push("real visitors' experience: " + r.field_overall.toLowerCase() + " (Core Web Vitals)");
    sp.append(" " + bits.join(" · "));
  };

  // Input helpers: clear button, example, "no website yet" link, and progress steps
  const input = checker.url;
  const clearBtn = document.getElementById("checker-clear");
  const progress = document.getElementById("checker-progress");
  const stepText = document.getElementById("checker-step");
  const bar = progress ? progress.querySelector(".bar i") : null;
  const syncClear = () => { if (clearBtn) clearBtn.hidden = !input.value; };
  input.addEventListener("input", syncClear);
  if (clearBtn) clearBtn.addEventListener("click", () => { input.value = ""; syncClear(); err.hidden = true; input.focus(); });
  const tryBtn = checker.querySelector("[data-try]");
  if (tryBtn) tryBtn.addEventListener("click", () => { input.value = tryBtn.dataset.try; syncClear(); checker.requestSubmit ? checker.requestSubmit() : checker.dispatchEvent(new Event("submit")); });
  const noSite = document.getElementById("checker-nosite");
  if (noSite) {
    noSite.href = waLink("Hi Edwin, I don't have a website yet. Can Page One build one for my business?\nMy business: ");
    noSite.target = "_blank"; noSite.rel = "noopener";
  }
  const STEPS = ["Opening your homepage…", "Checking how Google sees it…", "Checking it on a phone…", "Checking if ChatGPT and AI can read it…", "Working out your score…"];
  let stepTimer = null;
  const startProgress = () => {
    if (!progress) return;
    progress.hidden = false;
    let i = 0;
    stepText.textContent = STEPS[0];
    bar.style.width = "12%";
    stepTimer = setInterval(() => {
      i = Math.min(i + 1, STEPS.length - 1);
      stepText.textContent = STEPS[i];
      bar.style.width = Math.min(12 + i * 20, 92) + "%";
    }, 1600);
  };
  const stopProgress = () => { if (stepTimer) clearInterval(stepTimer); stepTimer = null; if (progress) progress.hidden = true; };

  // Social and marketplace pages aren't websites Google can rank like a business site
  const SOCIAL = [
    [/(^|\.)(facebook\.com|fb\.com|fb\.me)$/, "Facebook page"], [/(^|\.)instagram\.com$/, "Instagram profile"],
    [/(^|\.)tiktok\.com$/, "TikTok profile"], [/(^|\.)(shopee\.|lazada\.|carousell\.)/, "marketplace shop"],
    [/(^|\.)(linktr\.ee|beacons\.ai)$/, "link page"], [/(^|\.)(wa\.me|whatsapp\.com)$/, "WhatsApp link"],
    [/(^|\.)(maps\.app\.goo\.gl|goo\.gl)$|(^|\.)google\.[a-z.]+$/, "Google listing"],
  ];
  const socialKind = (value) => {
    let host = "";
    try { host = new URL(/^https?:\/\//.test(value) ? value : "https://" + value).hostname.replace(/^www\./, ""); } catch (e3) { return null; }
    for (const [re, kind] of SOCIAL) if (re.test(host)) return kind;
    return null;
  };
  const renderSocial = (value, kind) => {
    out.hidden = false;
    out.textContent = "";
    const box = el("div", "checker-social");
    box.appendChild(el("h3", null, "That's a " + kind + ", not a website"));
    box.appendChild(el("p", null, "A " + kind + " is a great start, but Google and AI assistants rank real websites for searches like \"hair salon near me\". Customers searching on Google may never see your " + kind + "."));
    box.appendChild(el("p", null, "Our Get Found plan builds you a proper website, connected to Google, Maps and AI search, from S$20 a month (introductory price)."));
    const row = el("div", "cta-row");
    const a = el("a", "btn", "Chat with Edwin about a website");
    a.href = waLink("Hi Edwin, my business is only on " + (/^[aeiou]/i.test(kind) ? "an " : "a ") + kind + " (" + value + "). Can Page One build me a proper website?");
    a.target = "_blank"; a.rel = "noopener";
    const p2 = el("a", "btn btn-ghost", "See what's included"); p2.href = "/get-found/";
    row.appendChild(a); row.appendChild(p2);
    const cta = el("div", "checker-cta"); cta.appendChild(row);
    box.appendChild(cta);
    out.appendChild(box);
    trackCta("checker_social");
  };

  checker.addEventListener("submit", async (e) => {
    e.preventDefault();
    const url = input.value.trim().replace(/\s+/g, "").replace(/[.,;]+$/, "").toLowerCase();
    input.value = url;
    syncClear();
    err.hidden = true;
    if (!url) { showError("Type your website address first, like yourbusiness.com.sg"); input.focus(); return; }
    if (!/\./.test(url)) { showError("That doesn't look like a website address. It should look like yourbusiness.com.sg. No website yet? Tap \"Chat with Edwin\" below."); input.focus(); return; }
    const kind = socialKind(url);
    if (kind) { renderSocial(url, kind); out.scrollIntoView({ behavior: "smooth", block: "start" }); return; }
    input.blur();
    btn.disabled = true;
    btn.textContent = "Checking…";
    out.hidden = true;
    out.textContent = "";
    startProgress();
    trackCta("checker_run");
    try {
      const r = await callApi("siteCheck", { url, mode: "basics" });
      if (!r.data || !r.data.ok) {
        const msg = (r.data && r.data.error) || "We couldn't check that website. Please try again.";
        showError(/doesn't return a web page|couldn't reach/i.test(msg) ? "We couldn't open " + url + ". Check the spelling, or try it with www. in front." : msg);
        return;
      }
      storageSet("p1-site", r.data.url, sessionStorage);
      stopProgress();
      out.hidden = false;
      const sp = renderBasics(r.data);
      out.scrollIntoView({ behavior: "smooth", block: "start" });
      callApi("siteCheck", { url: r.data.url, mode: "speed" }).then((s) => renderSpeed(sp, s.data, r.data.url)).catch(() => renderSpeed(sp, null, r.data.url));
    } catch (e2) {
      showError("We couldn't reach our checker. Please check your connection and try again.");
    } finally {
      stopProgress();
      btn.disabled = false;
      btn.textContent = "Check my website";
    }
  });
}

// ---------- Sign up (opens WhatsApp with the details filled in) ----------
const signup = document.getElementById("signup-form");
if (signup) {
  const params = new URLSearchParams(location.search);
  const err = signup.querySelector(".form-error");
  const total = document.getElementById("signup-total");
  const boostsWanted = params.get("boosts");
  if (boostsWanted && signup.querySelector('input[name="boosts"][value="' + boostsWanted + '"]')) {
    signup.querySelector('input[name="boosts"][value="' + boostsWanted + '"]').checked = true;
  }
  const site = storageGet("p1-site", sessionStorage);
  if (site && !signup.website.value) signup.website.value = site;
  const update = () => {
    const n = Number(signup.querySelector('input[name="boosts"]:checked').value || 0);
    total.textContent = "S$" + (PLAN_PRICE + n * BOOST_PRICE);
  };
  signup.addEventListener("change", update);
  update();
  signup.addEventListener("submit", (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(signup).entries());
    err.hidden = true;
    if (!String(d.business || "").trim() || !String(d.name || "").trim()) {
      err.textContent = "Please enter your name and business name.";
      err.hidden = false;
      return;
    }
    const n = Number(d.boosts || 0);
    const lines = [
      "Hi Edwin, I'd like to sign up for the Get Found plan (S$20/month, introductory price).",
      "Name: " + String(d.name).trim(),
      "Business: " + String(d.business).trim(),
      String(d.industry || "").trim() && "What we do: " + String(d.industry).trim(),
      "Website: " + (String(d.website || "").trim() || "none yet"),
      "SEO Boosts: " + (n ? n + " (S$" + n * BOOST_PRICE + ")" : "none for now"),
      "First month total: S$" + (PLAN_PRICE + n * BOOST_PRICE),
    ].filter(Boolean);
    const checked = storageGet("p1-check", sessionStorage);
    if (checked) lines.push("", "My website check: " + checked);
    openWhatsApp(lines.join("\n"), "signup_whatsapp");
  });
}

// Pricing calculator -> sign-up link keeps the chosen number of Boosts
const calcSignup = document.getElementById("calc-signup");
if (calcSignup && calc) {
  const sync = () => { calcSignup.href = "/signup/?boosts=" + (calc.querySelector('input[name="runs"]:checked')?.value || 0); };
  calc.addEventListener("change", sync);
  sync();
}

// ---------- SEO Boost top-up (WhatsApp) ----------
const topup = document.getElementById("topup-form");
if (topup) {
  const err = topup.querySelector(".form-error");
  topup.addEventListener("submit", (e) => {
    e.preventDefault();
    const business = topup.business.value.trim();
    err.hidden = true;
    if (!business) { err.textContent = "Please enter your business name."; err.hidden = false; return; }
    const n = Number(topup.boosts.value);
    openWhatsApp("Hi Edwin, I'd like to top up " + n + " SEO Boost" + (n > 1 ? "s" : "") + " (S$" + n * BOOST_PRICE + ").\nBusiness: " + business, "boost_topup_whatsapp");
  });
}

// ---------- Contact form (WhatsApp) ----------
const lead = document.getElementById("lead-form");
if (lead) {
  const err = lead.querySelector(".form-error");
  const site = storageGet("p1-site", sessionStorage);
  if (site && !lead.website.value) lead.website.value = site;
  lead.addEventListener("submit", (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(lead).entries());
    err.hidden = true;
    if (!String(d.name || "").trim()) { err.textContent = "Please add your name."; err.hidden = false; return; }
    const lines = [
      "Hi Edwin, I'm " + String(d.name).trim() + (String(d.business || "").trim() ? " from " + String(d.business).trim() : "") + ".",
      String(d.website || "").trim() && "Website: " + String(d.website).trim(),
      String(d.message || "").trim(),
    ].filter(Boolean);
    openWhatsApp(lines.join("\n"), "contact_whatsapp");
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
