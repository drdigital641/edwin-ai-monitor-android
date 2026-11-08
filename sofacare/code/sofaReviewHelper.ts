// Google Review Helper (Edwin, 8 Nov 2026, "Try this for sofacaresg only").
// One self-contained page, /review.html?business=sofacare: stars (default 5), up to 3 chips,
// optional sentence (max 120), Generate copies the text, then the customer opens Google and posts
// it themselves. No tracking, no cookies, nothing sent anywhere. noindex, follow; not in sitemap or llms.
// Place ID ChIJvXUIw95NrUkRsJKrhuwH3Xg = GBP feature 0x49ad4ddec30875bd:0x78dd07ec86ab92b0
// (cid 8709125966857474736), checked with a free IDs-only Place Details call.

export const REVIEW_PAGE = 'review.html';
export const GOOGLE_G_PATH = 'images/google-g.svg';
export const GOOGLE_G_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="48" height="48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>\n';

export const REVIEW_HTML = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Leave a Google Review | Sofa Care Singapore</title>
<meta name="robots" content="noindex, follow">
<meta name="description" content="Leave a Google review for Sofa Care Singapore.">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>
*{box-sizing:border-box}
html,body{margin:0;background:#f7faff;color:#123b5e;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.5}
main{max-width:560px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:1.5rem;line-height:1.25;margin:8px 0 4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
h1 img{width:28px;height:28px}
.sub{margin:0 0 20px;color:#4b6178}
.card{background:#fff;border:1px solid #dfe8f0;border-radius:16px;padding:18px;margin-bottom:16px}
.label{font-weight:700;margin:0 0 10px}
.stars{display:flex;gap:6px}
.star{width:52px;height:52px;border:0;background:none;font-size:40px;line-height:1;cursor:pointer;color:#c9d3dd;padding:0}
.star.on{color:#f5b301}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{min-height:44px;padding:10px 16px;border-radius:999px;border:1px solid #c9d3dd;background:#fff;color:#123b5e;font-size:1rem;cursor:pointer}
.chip[aria-pressed="true"]{background:#123b5e;border-color:#123b5e;color:#fff}
.chip:disabled{opacity:.45;cursor:not-allowed}
.hint{font-size:.9rem;color:#4b6178;margin:8px 0 0}
input[type=text]{width:100%;min-height:48px;padding:12px;border:1px solid #c9d3dd;border-radius:12px;font-size:1rem}
.btn{display:flex;align-items:center;justify-content:center;width:100%;min-height:56px;border:0;border-radius:14px;font-size:1.1rem;font-weight:700;cursor:pointer;text-decoration:none}
.gen{background:#123b5e;color:#fff}
.again{background:#fff;color:#123b5e;border:1px solid #123b5e;margin-top:10px;min-height:48px;font-size:1rem}
.open{background:#1e8e3e;color:#fff;margin-top:12px;font-size:1.2rem}
#out{display:none}
.ok{color:#1e8e3e;font-weight:700;margin:0 0 8px}
.text{white-space:pre-wrap;background:#f7faff;border:1px solid #dfe8f0;border-radius:12px;padding:12px;margin:0}
.back{display:inline-block;margin-top:8px;color:#123b5e}
</style>
</head>
<body>
<main>
<h1><img src="/images/google-g.svg" alt="Google" width="28" height="28"><span>Leave a Google Review — <span id="biz"></span></span></h1>
<p class="sub">Tap the stars and up to 3 things you liked. We write the review and copy it for you. You paste it on Google and post it yourself.</p>

<section class="card">
<p class="label" id="stars-l">Your rating</p>
<div class="stars" id="stars" role="radiogroup" aria-labelledby="stars-l"></div>
</section>

<section class="card">
<p class="label" id="chips-l">What did you like? (up to 3)</p>
<div class="chips" id="chips" aria-labelledby="chips-l"></div>
<p class="hint" id="count">0 of 3 picked</p>
</section>

<section class="card">
<label class="label" for="extra">Add one short sentence (optional)</label>
<input type="text" id="extra" maxlength="120" placeholder="You can leave this empty" autocomplete="off">
<p class="hint"><span id="left">120</span> characters left</p>
</section>

<button class="btn gen" id="gen" type="button">Generate my review</button>

<section class="card" id="out" aria-live="polite" style="margin-top:16px">
<p class="ok" id="ok">✓ Copied! Just paste it on Google.</p>
<p class="text" id="text"></p>
<button class="btn again" id="again" type="button">Copy again</button>
<a class="btn open" id="open" target="_blank" rel="noopener">Open Google Review →</a>
</section>

<a class="back" href="/">← Back to Sofa Care Singapore</a>
</main>
<script>
// ONE place for business settings. Only Sofa Care on this site.
var CONFIG = {
  sofacare: {
    name: "Sofa Care Singapore",
    googleReviewUrl: "https://search.google.com/local/writereview?placeid=ChIJvXUIw95NrUkRsJKrhuwH3Xg",
    attributes: ["Good service", "Fair pricing", "Thorough cleaning", "On time", "Friendly team", "Sofa looks like new", "Same-day service"]
  }
};
(function () {
  var key = new URLSearchParams(location.search).get("business") || "sofacare";
  var biz = CONFIG[key] || CONFIG.sofacare;
  var stars = 5, picked = [];
  document.getElementById("biz").textContent = biz.name;
  document.getElementById("open").href = biz.googleReviewUrl;
  var starsEl = document.getElementById("stars");
  function drawStars() {
    starsEl.innerHTML = "";
    for (var i = 1; i <= 5; i++) (function (n) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "star" + (n <= stars ? " on" : ""); b.textContent = "★";
      b.setAttribute("role", "radio"); b.setAttribute("aria-checked", n === stars ? "true" : "false");
      b.setAttribute("aria-label", n + (n === 1 ? " star" : " stars"));
      b.onclick = function () { stars = n; drawStars(); };
      starsEl.appendChild(b);
    })(i);
  }
  var chipsEl = document.getElementById("chips");
  function drawChips() {
    chipsEl.innerHTML = "";
    biz.attributes.forEach(function (a) {
      var on = picked.indexOf(a) !== -1;
      var b = document.createElement("button");
      b.type = "button"; b.className = "chip"; b.textContent = a;
      b.setAttribute("aria-pressed", on ? "true" : "false");
      b.disabled = !on && picked.length >= 3;
      b.onclick = function () {
        if (on) picked.splice(picked.indexOf(a), 1); else if (picked.length < 3) picked.push(a);
        drawChips();
      };
      chipsEl.appendChild(b);
    });
    document.getElementById("count").textContent = picked.length + " of 3 picked";
  }
  var extra = document.getElementById("extra");
  extra.oninput = function () { document.getElementById("left").textContent = 120 - extra.value.length; };
  // Wording varies on every Generate (Edwin 8 Nov: "the generated sentence must varies").
  // Phrases only restate what the chip says. No prices, no other claims.
  var PHRASES = {
    "Good service": ["the service was good", "service was good from start to end", "service was really good", "they gave good service", "the service was very good overall"],
    "Fair pricing": ["the price was fair", "pricing was fair", "the price was fair for the job", "the charges were reasonable", "the price was very fair"],
    "Thorough cleaning": ["the cleaning was very thorough", "they cleaned everything properly", "they did a very thorough job", "they were thorough with the cleaning", "nothing was missed in the cleaning"],
    "On time": ["they came on time", "arrived on time", "they came at the time given", "they were on time", "came right on schedule"],
    "Friendly team": ["the team was friendly", "the team was friendly and polite", "the guys were very friendly", "the crew was friendly", "the cleaners were friendly"],
    "Sofa looks like new": ["my sofa looks like new now", "the sofa looks almost new", "sofa came out looking like new", "my sofa looks so much newer", "the sofa looks brand new again"],
    "Same-day service": ["they could come the same day", "I got same-day service", "I could book them for the same day", "came on the same day I asked", "they did it same day"]
  };
  var OPEN = ["", "Very happy with Sofa Care Singapore. ", "Booked Sofa Care Singapore for my sofa. ", "Good experience overall. ", "Used Sofa Care Singapore recently. ", "Satisfied with the job. "];
  var JOIN = [
    function (l) { return cap(list(l)) + "."; },
    function (l) { return "What I liked: " + list(l) + "."; },
    function (l) { return l.map(function (x) { return cap(x) + "."; }).join(" "); },
    function (l) { return "Honestly, " + list(l) + "."; }
  ];
  var END5 = ["Highly recommended!", "Would book again.", "Will recommend to friends.", "Will use them again.", "Recommended!"];
  var DEFAULTS = ["Great service, highly recommended!", "Good job overall, would book again.", "Very happy with the service. Recommended!", "Smooth experience from start to end. Will recommend to friends.", "Good service, will use them again."];
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function cap(x) { return x.charAt(0).toUpperCase() + x.slice(1); }
  function list(l) { return l.length < 2 ? l.join("") : l.slice(0, -1).join(", ") + " and " + l[l.length - 1]; }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  var last = "";
  function build() {
    for (var tries = 0; tries < 8; tries++) {
      var t = once();
      if (t !== last) { last = t; return t; }
    }
    return last = once();
  }
  function once() {
    var s = extra.value.trim();
    if (!picked.length && !s) return stars === 5 ? pick(DEFAULTS) : pick(["Good service.", "The job was done.", "Service was okay."]);
    var parts = [];
    if (picked.length) {
      var phrases = shuffle(picked).map(function (c) { return pick(PHRASES[c] || [c.toLowerCase()]); });
      parts.push((pick(OPEN) + pick(JOIN)(phrases)).trim());
    }
    if (s) parts.push(/[.!?]$/.test(s) ? s : s + ".");
    if (stars === 5) parts.push(pick(END5));
    return parts.join(" ");
  }
  function copy(t) {
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = t; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.top = "-1000px";
      document.body.appendChild(ta); ta.select(); ta.setSelectionRange(0, t.length);
      var ok = false; try { ok = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta); return ok;
    }
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(t).then(function () { return true; }, fallback);
    return Promise.resolve(fallback());
  }
  var current = "";
  function show(ok) {
    document.getElementById("out").style.display = "block";
    document.getElementById("ok").textContent = ok ? "✓ Copied! Just paste it on Google." : "Copy did not work on this browser. Press and hold the text to copy it.";
  }
  document.getElementById("gen").onclick = function () {
    current = build();
    document.getElementById("text").textContent = current;
    copy(current).then(show);
    document.getElementById("out").scrollIntoView({ behavior: "smooth", block: "start" });
  };
  document.getElementById("again").onclick = function () { copy(current).then(show); };
  drawStars(); drawChips();
})();
</script>
</body>
</html>
`;

// Footer link on every page, added once here (the site's pages are generated, so this is the shared footer step).
export const REVIEW_FOOTER_LINK = '<a class="hover:text-white sc-greview" href="/review.html?business=sofacare" style="display:inline-flex;align-items:center;gap:6px"><img src="/images/google-g.svg" alt="" width="16" height="16" loading="lazy" decoding="async" style="width:16px;height:16px">Leave a Google Review</a>';

export function addSofaReviewHelper(files: Record<string, string>): void {
  files[REVIEW_PAGE] = REVIEW_HTML;
  for (const p of Object.keys(files)) {
    if (!p.endsWith('.html') || p === REVIEW_PAGE || p === 'lead-log.html' || files[p].includes('sc-greview')) continue;
    const i = files[p].lastIndexOf('</nav></div></div></footer>');
    if (i === -1) { if (p === '404.html') continue; throw Error('Review helper: footer layout changed on ' + p); }
    files[p] = files[p].slice(0, i) + REVIEW_FOOTER_LINK + files[p].slice(i);
  }
}
