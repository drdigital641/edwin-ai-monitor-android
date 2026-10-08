// Page One Singapore WhatsApp number (country code, no + or spaces).
const WHATSAPP_NUMBER = "6589976612";

const PLAN_PRICE = 20;
const BOOST_PRICE = 10;

function waLink(text) {
  return "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(text);
}

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

// Free check form -> prefilled WhatsApp message
const form = document.getElementById("check-form");
if (form) {
  const error = document.getElementById("form-error");
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const d = Object.fromEntries(new FormData(form).entries());
    if (!d.business?.trim() || !d.industry?.trim() || !d.name?.trim()) {
      error.hidden = false;
      return;
    }
    error.hidden = true;
    const lines = [
      "Hi Page One Singapore, I'd like a free Google + AI visibility check.",
      "Business: " + d.business.trim(),
      "What we do: " + d.industry.trim(),
      d.area?.trim() && "Area: " + d.area.trim(),
      d.website?.trim() && "Website: " + d.website.trim(),
      "Name: " + d.name.trim(),
    ].filter(Boolean);
    window.open(waLink(lines.join("\n")), "_blank", "noopener");
  });
}

// Floating WhatsApp button (fallback if the chat helper can't start)
const float = document.getElementById("wa-float");
if (float) {
  float.href = waLink("Hi Page One Singapore, I'd like to know more about the S$20 Get Found plan.");
  float.target = "_blank";
  float.rel = "noopener";
}

// Animated chat helper: replaces the plain WhatsApp button
const QUICK_REPLIES = [
  { label: "Get a free Google + AI visibility check", text: "Hi Page One Singapore, I'd like a free Google + AI visibility check for my business." },
  { label: "How much will it cost me?", text: "Hi Page One Singapore, how much would the Get Found plan and SEO Boosts cost for my business?" },
  { label: "I already have a website", text: "Hi Page One Singapore, I already have a website. Can you add an SEO landing page for me?" },
  { label: "Something else", text: "Hi Page One Singapore, I have a question." },
];

function storageGet(key) {
  try { return sessionStorage.getItem(key); } catch (e) { return null; }
}
function storageSet(key, value) {
  try { sessionStorage.setItem(key, value); } catch (e) { /* private mode */ }
}

function startChatHelper() {
  const root = document.createElement("div");
  root.className = "chat-helper";
  root.innerHTML =
    '<div class="chat-teaser" id="chat-teaser" hidden>' +
      '<button class="chat-teaser-close" type="button" aria-label="Dismiss">×</button>' +
      '<p><b>Hi there 👋</b><br>Can customers find you on Google and ChatGPT? Ask us, it\'s free.</p>' +
    "</div>" +
    '<section class="chat-panel" id="chat-panel" role="dialog" aria-label="Chat with Page One Singapore" hidden>' +
      '<header class="chat-head">' +
        '<span class="chat-avatar" aria-hidden="true">1</span>' +
        '<div><b>Page One Singapore</b><small>WhatsApp 24/7 · no obligation</small></div>' +
        '<button class="chat-close" type="button" aria-label="Close chat">×</button>' +
      "</header>" +
      '<div class="chat-body" id="chat-body"></div>' +
    "</section>" +
    '<button class="chat-launcher" id="chat-launcher" type="button" aria-expanded="false" aria-controls="chat-panel" aria-label="Open chat">' +
      '<span class="chat-ring" aria-hidden="true"></span>' +
      '<svg class="chat-icon" viewBox="0 0 24 24" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-5 4v-4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm3 6.5a1.5 1.5 0 1 0 0 .01zm5 0a1.5 1.5 0 1 0 0 .01zm5 0a1.5 1.5 0 1 0 0 .01z"/></svg>' +
      '<span class="chat-badge" id="chat-badge" aria-hidden="true">1</span>' +
    "</button>";
  document.body.appendChild(root);
  if (float) float.hidden = true;

  const teaser = root.querySelector("#chat-teaser");
  const panel = root.querySelector("#chat-panel");
  const body = root.querySelector("#chat-body");
  const launcher = root.querySelector("#chat-launcher");
  const badge = root.querySelector("#chat-badge");
  let filled = false;

  const addBubble = (html) => {
    const p = document.createElement("p");
    p.className = "chat-msg";
    p.innerHTML = html;
    body.appendChild(p);
  };

  const fillConversation = () => {
    if (filled) return;
    filled = true;
    const typing = document.createElement("p");
    typing.className = "chat-msg chat-typing";
    typing.setAttribute("aria-label", "Typing");
    typing.innerHTML = "<span></span><span></span><span></span>";
    body.appendChild(typing);
    setTimeout(() => {
      typing.remove();
      addBubble("Hi! 👋 I'm with Page One Singapore.");
      addBubble("We help Singapore businesses get found on Google, Google Maps and AI. Plans start at <b>S$20/month</b>, no contract. What can we help with?");
      const list = document.createElement("div");
      list.className = "chat-replies";
      for (const q of QUICK_REPLIES) {
        const a = document.createElement("a");
        a.className = "chat-reply";
        a.href = waLink(q.text);
        a.target = "_blank";
        a.rel = "noopener";
        a.textContent = q.label;
        list.appendChild(a);
      }
      body.appendChild(list);
      const note = document.createElement("p");
      note.className = "chat-note";
      note.textContent = "Opens WhatsApp. We reply personally, 24/7. No obligation to discuss.";
      body.appendChild(note);
    }, 900);
  };

  const hideTeaser = () => { teaser.hidden = true; };
  const open = () => {
    panel.hidden = false;
    launcher.setAttribute("aria-expanded", "true");
    launcher.classList.add("is-open");
    badge.hidden = true;
    hideTeaser();
    storageSet("p1-chat-seen", "1");
    fillConversation();
  };
  const close = () => {
    panel.hidden = true;
    launcher.setAttribute("aria-expanded", "false");
    launcher.classList.remove("is-open");
    launcher.focus();
  };

  launcher.addEventListener("click", () => (panel.hidden ? open() : close()));
  root.querySelector(".chat-close").addEventListener("click", close);
  teaser.querySelector("p").addEventListener("click", open);
  teaser.querySelector(".chat-teaser-close").addEventListener("click", () => {
    hideTeaser();
    storageSet("p1-chat-seen", "1");
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !panel.hidden) close();
  });

  // Pop the teaser bubble once per visit, on larger screens only, so it never covers content on phones
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

// Anonymous visit and WhatsApp-click counts for the Page One controller (Base44).
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
  const checkForm = document.getElementById("check-form");
  if (checkForm) checkForm.addEventListener("submit", () => {
    if (checkForm.querySelector("#form-error") && !checkForm.querySelector("#form-error").hidden) return;
    setTimeout(() => { const err = document.getElementById("form-error"); if (!err || err.hidden) send("CtaClick", { cta_type: "free_check_form" }); }, 0);
  });
})();
