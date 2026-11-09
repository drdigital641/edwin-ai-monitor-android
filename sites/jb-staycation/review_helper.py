"""JB Staycations Google Review Helper (Edwin's universal spec, 9 Nov 2026).
One self-contained review.html: no backend, no libraries, no tracking. Hidden from Google:
meta robots noindex + X-Robots-Tag header (htaccess), rel=nofollow footer link, never in sitemap/llms/IndexNow."""
import os

G_SVG = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>'
         '<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>'
         '<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>'
         '<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>')

REVIEW_HTML = r"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Leave a Google Review | __NAME__</title>
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet">
<meta name="description" content="Leave a Google review for __NAME__.">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<style>
*{box-sizing:border-box}
html,body{margin:0;background:#f8f5ef;color:#0a1f38;font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.5}
main{max-width:560px;margin:0 auto;padding:24px 16px 48px}
.top{display:flex;align-items:center;gap:8px;margin:0 0 16px;font-weight:700;color:#0a1f38;text-decoration:none}
.top b{color:#8a5a10}
h1{font-size:1.5rem;line-height:1.25;margin:8px 0 4px;display:flex;align-items:center;gap:10px;flex-wrap:wrap}
h1 img{width:28px;height:28px}
.sub{margin:0 0 20px;color:#45566b}
.card{background:#fff;border:1px solid #e6dccb;border-radius:16px;padding:18px;margin-bottom:16px}
.label{display:block;font-weight:700;margin:0 0 10px}
.stars{display:flex;gap:6px;flex-wrap:wrap}
.star{width:48px;height:48px;border:0;background:none;font-size:40px;line-height:1;cursor:pointer;color:#cfc6b6;padding:0}
.star.on{color:#b8740a}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{min-height:44px;padding:10px 16px;border-radius:999px;border:1px solid #cfc6b6;background:#fff;color:#0a1f38;font-size:1rem;cursor:pointer}
.chip[aria-pressed="true"]{background:#0a1f38;border-color:#0a1f38;color:#fff}
.chip:disabled{opacity:.45;cursor:not-allowed}
.hint{font-size:.9rem;color:#45566b;margin:8px 0 0}
input[type=text]{width:100%;min-height:48px;padding:12px;border:1px solid #cfc6b6;border-radius:12px;font-size:1rem;font-family:inherit}
.btn{display:flex;align-items:center;justify-content:center;width:100%;min-height:56px;border:0;border-radius:14px;font-size:1.1rem;font-weight:700;cursor:pointer;text-decoration:none;font-family:inherit}
.gen{background:#0a1f38;color:#fff}
.again{background:#fff;color:#0a1f38;border:1px solid #0a1f38;margin:10px 0 12px;min-height:48px;font-size:1rem}
.open{background:#1e7e34;color:#fff;font-size:1.2rem;min-height:64px}
#out{display:none;margin-top:16px}
.ok{color:#1e7e34;font-weight:700;margin:0 0 8px}
.text{white-space:pre-wrap;background:#f8f5ef;border:1px solid #e6dccb;border-radius:12px;padding:12px;margin:0;overflow-wrap:anywhere}
.back{display:inline-flex;align-items:center;min-height:44px;margin-top:8px;color:#0a1f38}
</style>
</head>
<body>
<main>
<a class="top" href="./">JB <b>Staycations</b></a>
<h1><img src="google-g.svg" alt="Google" width="28" height="28"><span>Leave a Google Review for <span id="biz">__NAME__</span></span></h1>
<p class="sub">Tap the stars and up to 3 things you liked. We write the review and copy it for you. You paste it on Google and post it yourself.</p>

<section class="card">
<p class="label" id="stars-l">Your rating</p>
<div class="stars" id="stars" role="radiogroup" aria-labelledby="stars-l"></div>
</section>

<section class="card">
<p class="label" id="chips-l">What did you like? (up to 3)</p>
<div class="chips" id="chips" role="group" aria-labelledby="chips-l"></div>
<p class="hint" id="count">0 of 3 picked</p>
</section>

<section class="card">
<label class="label" for="extra">Add one short sentence (optional)</label>
<input type="text" id="extra" maxlength="120" placeholder="You can leave this empty" autocomplete="off">
<p class="hint"><span id="left">120</span> characters left</p>
</section>

<button class="btn gen" id="gen" type="button">Generate my review</button>

<section class="card" id="out" aria-live="polite">
<p class="ok" id="ok">✓ Copied! Just paste it on Google.</p>
<p class="text" id="text"></p>
<button class="btn again" id="again" type="button">Copy again</button>
<a class="btn open" id="open" href="#" target="_blank" rel="nofollow noopener noreferrer">Open Google Review →</a>
<p class="hint" style="text-align:center">On Google, tap the stars, paste your review and post it.</p>
</section>

<a class="back" href="./">← Back to __NAME__</a>
</main>
<script>
// ONE place for business settings. Only JB Staycations on this site; pick with ?business=<key>.
var CONFIG = {
  jbstaycation: {
    name: "__NAME__",
    googleReviewUrl: "https://maps.app.goo.gl/oWWdqZMFiy926sS49",
    attributes: ["Very clean", "Spacious for groups", "Great for gatherings", "Fun games room", "Easy self check-in", "Helpful host", "Good value", "Near KSL City"]
  }
};
(function () {
  var key = new URLSearchParams(location.search).get("business") || "jbstaycation";
  var biz = CONFIG[key] || CONFIG.jbstaycation;
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
  // Wording varies each time. Phrases only restate what the chip says: no prices, no other claims.
  var PHRASES = {
    "Very clean": ["the house was very clean", "everything was very clean", "the place was spotless", "the house was clean and tidy"],
    "Spacious for groups": ["there was lots of space for our group", "the house was spacious for a big group", "plenty of room for everyone", "spacious enough for the whole group"],
    "Great for gatherings": ["it was great for our family gathering", "perfect for a gathering with friends", "a great place for a gathering", "good for getting everyone together"],
    "Fun games room": ["the games room was a lot of fun", "we had fun with the pool table and games", "the games kept everyone busy", "the games room was a hit"],
    "Easy self check-in": ["self check-in was easy", "check-in was simple and smooth", "getting in was easy with self check-in", "the self check-in was hassle-free"],
    "Helpful host": ["the host was very helpful", "Daniel was helpful and quick to reply", "the host replied fast and helped us", "the host was friendly and helpful"],
    "Good value": ["it was good value for our group", "good value for money", "worth the price", "great value for the size of the house"],
    "Near KSL City": ["it is near KSL City", "KSL City is close by", "close to KSL City for food and shopping", "handy for KSL City"]
  };
  var OPEN = ["", "Stayed at __NAME__ with family. ", "Good stay at __NAME__. ", "Booked __NAME__ for a weekend. ", "Very happy with our stay. "];
  var JOIN = [
    function (l) { return cap(list(l)) + "."; },
    function (l) { return "What we liked: " + list(l) + "."; },
    function (l) { return l.map(function (x) { return cap(x) + "."; }).join(" "); }
  ];
  var END5 = ["Highly recommended!", "Would stay again.", "Will recommend to friends.", "Will book again.", "Recommended!"];
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function cap(x) { return x.charAt(0).toUpperCase() + x.slice(1); }
  function list(l) { return l.length < 2 ? l.join("") : l.slice(0, -1).join(", ") + " and " + l[l.length - 1]; }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function build() {
    var s = extra.value.trim();
    if (!picked.length && !s) return stars >= 4 ? "Great service, highly recommended!" : "Good stay, thank you.";
    var parts = [];
    if (picked.length) {
      var phrases = shuffle(picked).map(function (c) { return pick(PHRASES[c] || [c.toLowerCase()]); });
      parts.push((pick(OPEN) + pick(JOIN)(phrases)).trim());
    }
    if (stars === 5) parts.push(pick(END5));
    if (s) parts.push(/[.!?]$/.test(s) ? s : s + ".");   // guest's own sentence always last
    return parts.join(" ");
  }
  // Copy inside the tap itself so it works on phones.
  function copyNow(t) {
    var ok = false;
    var ta = document.createElement("textarea");
    ta.value = t; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.top = "-1000px"; ta.style.fontSize = "16px";
    document.body.appendChild(ta); ta.select(); ta.setSelectionRange(0, t.length);
    try { ok = document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(ta);
    try { if (navigator.clipboard && window.isSecureContext) { navigator.clipboard.writeText(t).catch(function () {}); ok = true; } } catch (e) {}
    return ok;
  }
  var current = "";
  function show(ok) {
    var o = document.getElementById("out"); o.style.display = "block";
    document.getElementById("ok").textContent = ok ? "✓ Copied! Just paste it on Google." : "Copy did not work on this browser. Press and hold the text to copy it.";
  }
  document.getElementById("gen").onclick = function () {
    current = build();
    document.getElementById("text").textContent = current;
    show(copyNow(current));
    document.getElementById("out").scrollIntoView({ behavior: "smooth", block: "start" });
  };
  document.getElementById("again").onclick = function () { show(copyNow(current)); };
  drawStars(); drawChips();
})();
</script>
</body>
</html>
"""


def write_review(out, name):
    open(os.path.join(out, 'review.html'), 'w', encoding='utf-8').write(REVIEW_HTML.replace('__NAME__', name))
    open(os.path.join(out, 'google-g.svg'), 'w').write(G_SVG)


def footer_link(r):
    """Footer link: rel=nofollow so Google is not sent to the noindex page."""
    return ('<a class="frev" href="%sreview.html?business=jbstaycation" rel="nofollow">'
            '<img src="%sgoogle-g.svg" alt="" width="18" height="18" loading="lazy">Leave a Google Review</a>' % (r, r))
