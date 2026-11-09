import json, html, pathlib

SLUG = "steering-wheel-shaking-at-speed-singapore"
URL = f"https://www.sggarage.com/articles/{SLUG}.html"
TITLE = "Steering Wheel Shaking at Speed: Common Causes"
H1 = "Steering Wheel Shaking at Speed? What Causes It and What to Check"
DESC = ("Steering wheel vibrating at higher speeds? Common causes (wheel balance, tyres, alignment, worn parts), "
        "when it is unsafe and what to tell the workshop.")
PUB = "2026-11-10T10:30:00+08:00"
BYLINE_DATE = "November 10, 2026"
SECTION = "Steering & Tyres"
IMG = "https://i.ibb.co/qM3ZKCDy/edwin-garage-og-image.jpg"
KEYWORDS = "steering wheel shaking at speed Singapore, steering wheel vibration, car shakes at highway speed, wheel balancing, steering vibration causes"

FAQ = [
 ("Why does my steering wheel shake only at higher speeds?",
  "The most common reason is a wheel that is out of balance. A small imbalance is barely felt at low speed but becomes a steady shake once the wheels spin faster. Tyre damage, a bent rim or worn suspension parts can cause the same feeling, so the cause needs to be checked rather than guessed."),
 ("Is it safe to drive with a shaking steering wheel?",
  "A light, steady vibration that has built up gradually can usually be driven carefully to a booked inspection, but do not ignore it. If the shake is violent, started suddenly after hitting a kerb or pothole, comes with a tyre bulge, a pulling steering or a noise from a wheel, slow down, pull over safely and arrange recovery."),
 ("Is it wheel balancing or wheel alignment?",
  "They fix different problems. Wheel balancing corrects uneven weight around the wheel and tyre, which usually shows up as a shake at certain speeds. Wheel alignment corrects the angles of the wheels, which usually shows up as the car pulling to one side or uneven tyre wear. A workshop can check both."),
 ("Why does the steering wheel shake only when I brake?",
  "A shake that appears only under braking usually points to the brakes, such as uneven brake discs, rather than wheel balance. Our brake wear guide explains what a workshop checks. Book an inspection if it happens every time."),
 ("Can worn suspension parts make the steering shake?",
  "Yes. Worn ball joints, tie rod ends, bushes or wheel bearings can let the wheel move more than it should, which you may feel as a shake, a loose steering feel or a knocking sound. These parts are safety-related, so have them inspected."),
 ("What should I tell the workshop about the steering shake?",
  "Tell them the speed range where it happens, whether it is in the steering wheel or the seat, whether it changes when you brake or accelerate, and whether it began after a new tyre, a kerb hit or a pothole. A short note on the date it started helps."),
]

ld_faq = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
biz = {"@type": ["AutoRepair", "LocalBusiness"], "@id": "https://www.sggarage.com/#business",
       "name": "Edwin Garage Aircon & Car Repair", "url": "https://www.sggarage.com", "telephone": "+6597856612",
       "address": {"@type": "PostalAddress", "streetAddress": "Blk 5032 Ang Mo Kio Industrial Park 2 #01-295",
                   "addressLocality": "Ang Mo Kio", "addressRegion": "Singapore", "postalCode": "569535", "addressCountry": "SG"},
       "geo": {"@type": "GeoCoordinates", "latitude": 1.3721, "longitude": 103.8458},
       "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                      "opens": "10:00", "closes": "20:00"}],
       "sameAs": ["https://share.google/hYkZhnKyoAEeERhWM", "https://www.facebook.com/edwingarageamk/", "https://www.facebook.com/sggarageedwin/"]}
ld_graph = {"@context": "https://schema.org", "@graph": [
    biz,
    {"@type": "Article", "@id": URL + "#article", "headline": H1, "description": DESC,
     "image": {"@type": "ImageObject", "url": IMG}, "datePublished": PUB, "dateModified": PUB,
     "author": {"@type": "Person", "name": "Edwin", "jobTitle": "Master Automotive Technician", "worksFor": {"@id": "https://www.sggarage.com/#business"}},
     "publisher": {"@id": "https://www.sggarage.com/#business"},
     "mainEntityOfPage": {"@type": "WebPage", "@id": URL}, "articleSection": SECTION, "inLanguage": "en-SG",
     "about": {"@id": "https://www.sggarage.com/#business"},
     "keywords": KEYWORDS},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.sggarage.com"},
        {"@type": "ListItem", "position": 2, "name": "Car Guides", "item": "https://www.sggarage.com/articles/"},
        {"@type": "ListItem", "position": 3, "name": H1, "item": URL}]},
    {"@type": "WebPage", "@id": URL, "url": URL, "name": TITLE, "datePublished": PUB, "dateModified": PUB,
     "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".article h2", ".article p"]}}]}

e = lambda s: html.escape(s, quote=True)
tpl = pathlib.Path(__file__).with_name("style.css").read_text()

body = f"""
<p><strong>A steering wheel that shakes at higher speeds is most often caused by a wheel that is out of balance, but damaged tyres, a bent rim, wheel alignment problems or worn suspension parts can feel the same. A light, steady shake can wait for a booked inspection. A violent shake, a shake that started suddenly after hitting a kerb or pothole, or a shake with a tyre bulge or a noise from a wheel means slow down, pull over safely and arrange recovery.</strong></p>
<p>We are Edwin Garage, a car workshop in Ang Mo Kio. This guide helps you work out what the shake is telling you, how urgent it is, and what to tell the workshop so the cause is found quickly.</p>

<h2>When should you stop driving straight away?</h2>
<p>Slow down, pull over somewhere safe and switch on your hazard lights if you notice the shake together with any of these:</p>
<ul>
<li><strong>A sudden, violent shake</strong> that started right after hitting a kerb, pothole or road debris.</li>
<li><strong>A bulge or cut</strong> on the side of a tyre. Our <a href="/articles/tyre-sidewall-bulge-singapore-safe-driving.html">tyre sidewall bulge guide</a> explains why this is not safe to drive on.</li>
<li><strong>The car pulling hard to one side</strong>, or the steering feeling loose or vague.</li>
<li><strong>A rumbling, grinding or knocking noise</strong> from one wheel. See <a href="/articles/wheel-bearing-noise-singapore.html">wheel bearing noise</a>.</li>
<li><strong>A red warning light</strong>, or a burning smell from the wheels after driving.</li>
</ul>
<p>If the car is not safe to drive, arrange recovery instead of driving it to the workshop. The <a href="/articles/breakdown-accident-towing-singapore.html">breakdown and towing guide</a> explains what to do next.</p>

<h2>What usually causes a steering wheel to shake?</h2>
<p>Where and when you feel the shake points to where to look. The table is a guide to the usual causes, not a diagnosis.</p>
<div class="tbl"><table class="art-tbl"><thead><tr><th>What you feel</th><th>What it usually means</th><th>How urgent</th></tr></thead><tbody>
<tr><td>Steering wheel shakes at a certain speed range and settles outside it</td><td>A front wheel is out of balance, often after a tyre change or a lost balancing weight</td><td>Book a wheel balance check soon.</td></tr>
<tr><td>Shake felt in the seat or floor rather than the steering wheel</td><td>Usually a rear wheel or tyre issue</td><td>Book an inspection soon.</td></tr>
<tr><td>Shake with the car pulling to one side or tyres wearing unevenly</td><td>Wheel alignment out of specification</td><td>Book an alignment check. See <a href="/articles/wheel-alignment-signs-what-checked-singapore.html">what is checked in an alignment</a>.</td></tr>
<tr><td>Sudden shake after hitting a kerb or pothole</td><td>Bent rim, damaged tyre or a bent suspension part</td><td>Slow down and have it inspected promptly. Stop if it is violent.</td></tr>
<tr><td>Shake with clunks, a loose steering feel or knocking over bumps</td><td>Worn ball joints, tie rod ends, bushes or wheel bearings</td><td>Safety related. Book an inspection soon.</td></tr>
<tr><td>Shake only when braking</td><td>Brake discs or pads, not wheel balance</td><td>Book a brake inspection. See <a href="/articles/brake-wear-replace-brake-pads-singapore.html">brake wear and pads</a>.</td></tr>
</tbody></table></div>

<h3>Wheel balance: the most common cause</h3>
<p>A tyre and wheel never weigh exactly the same all the way around. Small weights are fixed to the rim so the wheel spins evenly. If a weight falls off, or a tyre is fitted without being balanced properly, the wheel wobbles slightly as it spins. At low speed you will not feel it, but at higher speeds the wobble becomes a steady shake in the steering wheel. A workshop corrects this by spinning the wheel on a balancing machine and refitting the weights.</p>

<h3>Tyre and rim damage</h3>
<p>A tyre with an internal fault, a flat spot, uneven wear or a bulge can make the car shake. So can a rim that was bent by a pothole or kerb. Look at the tyres for bulges, cuts and uneven wear, and check the tyre pressure when the tyres are cold. Do not drive on a tyre with a bulge.</p>

<h3>Alignment and worn suspension parts</h3>
<p>Wheel alignment affects how evenly the tyres wear and how the car tracks on the road. Worn suspension and steering parts let the wheel move when it should be held firmly, and you may feel this as a shake or a loose steering feel. Our guide to <a href="/articles/car-suspension-noise-clunking-rattling-singapore.html">suspension noises</a> lists the usual signs. These parts affect control of the car, so do not leave them for weeks.</p>

<h2>What to do in the first few minutes</h2>
<ol>
<li><strong>Slow down</strong> and drive smoothly. Avoid hard braking and sharp turns.</li>
<li><strong>If any stop sign above applies,</strong> pull over safely, switch on your hazard lights and arrange recovery.</li>
<li><strong>Note when it happens:</strong> the speed range, whether it is in the steering wheel or the seat, and whether it changes when you brake.</li>
<li><strong>When the car is parked,</strong> look at each tyre for bulges, cuts and uneven wear, and check the pressures when cold.</li>
<li><strong>Tell the workshop</strong> if it began after a new tyre, a kerb hit or a pothole.</li>
</ol>

<h2>What a workshop checks</h2>
<p>To find the cause, a mechanic will usually:</p>
<ul>
<li>Test drive the car to feel where and at what speed the shake appears.</li>
<li>Inspect the tyres and rims for bulges, damage and uneven wear.</li>
<li>Check wheel balance on a balancing machine and look for missing weights.</li>
<li>Check wheel alignment.</li>
<li>Inspect ball joints, tie rod ends, bushes and wheel bearings for play.</li>
<li>Check the brake discs and pads if the shake happens when braking.</li>
</ul>
<p>The fix depends on what is found, so ask for the cause and a quote before you approve any work. Our guide to <a href="/articles/car-diagnostic-fee-singapore.html">what a diagnostic fee covers</a> explains how this works at Edwin Garage.</p>

<section aria-labelledby="edwin-assessment" style="padding:24px;margin:32px 0;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px">
<h2 id="edwin-assessment" style="margin-top:0">Book a steering shake check</h2>
<p>Inspections and repairs at Edwin Garage in Ang Mo Kio are by appointment, booked online. WhatsApp 9785 6612 is for enquiries. Open 10am to 8pm, Monday to Saturday; closed Sundays. If the car is not safe to drive, arrange recovery rather than driving it to your booking.</p>
<p><a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book an inspection online</a></p>
</section>

<h2>Frequently asked questions</h2>
""" + "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(a)}</p>" for q, a in FAQ) + """

<div class="takeaways-box"><h3>Key Takeaways</h3><ul>
<li>A shake at higher speeds is most often a wheel out of balance.</li>
<li>Tyre damage, a bent rim, alignment or worn suspension parts can feel the same.</li>
<li>A shake only when braking points to the brakes.</li>
<li>A sudden violent shake, a tyre bulge or a noise from a wheel means slow down, stop safely and arrange recovery.</li>
<li>Tell the workshop the speed range and whether it began after a kerb hit, pothole or new tyre.</li>
</ul></div>

<div class="cta-block">
  <h3>Steering wheel shaking?</h3>
  <p>Edwin Garage is in Ang Mo Kio, serving Hougang, Yio Chu Kang, Serangoon and nearby areas. Inspections and repairs are by online appointment. WhatsApp 9785 6612 is for enquiries.</p>
  <a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a>
</div>
<div class="cluster-box"><h3>Related guides</h3><ul>
<li><a href="/articles/wheel-alignment-signs-what-checked-singapore.html">Wheel Alignment: Signs and What Is Checked</a></li>
<li><a href="/articles/tyre-sidewall-bulge-singapore-safe-driving.html">Tyre Sidewall Bulge: Is It Safe to Drive?</a></li>
<li><a href="/articles/car-suspension-noise-clunking-rattling-singapore.html">Car Suspension Noise: Clunking and Rattling</a></li>
<li><a href="/articles/wheel-bearing-noise-singapore.html">Wheel Bearing Noise in Singapore</a></li>
<li><a href="/articles/brake-wear-replace-brake-pads-singapore.html">Brake Wear and Replacing Brake Pads</a></li>
<li><a href="/articles/car-vibrates-at-idle-singapore.html">Car Vibrates at Idle</a></li>
</ul></div>
"""

page = f"""<!DOCTYPE html>
<html lang="en-SG">
<head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:image" content="{IMG}"><meta property="og:type" content="article">
<meta property="og:url" content="{URL}">
<meta property="og:locale" content="en_SG"><meta property="og:site_name" content="Edwin Garage Singapore">
<meta property="article:published_time" content="{PUB}"><meta property="article:modified_time" content="{PUB}">
<meta property="article:section" content="{e(SECTION)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(TITLE)}">
<meta name="twitter:description" content="{e(DESC)}"><meta name="twitter:image" content="{IMG}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{URL}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_graph, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
<style>
{tpl}</style>
</head>
<body>
<header class="site-header">
  <a class="logo" href="/"><span>Edwin</span> Garage</a>
  <button class="hamburger" aria-label="Menu" onclick="document.getElementById('hnav').classList.toggle('open')"><span></span><span></span><span></span></button>
  <nav class="hnav" id="hnav">
    <a class="nl" href="/">Home</a>
    <a class="nl" href="/car-servicing-repair/">Servicing</a>
    <a class="nl" href="/car-aircon-repair/">Aircon</a>
    <a class="nl" href="/accident-claim-repair/">Accident</a>
    <a class="nl active" href="/articles/">Articles</a>
    <a class="btn-book-sm" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Now</a>
  </nav>
</header>
<div class="art-header"><div class="art-header-inner">
  <nav class="breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span class="sep">›</span><a href="/articles/">Articles</a><span class="sep">›</span><span>{e(H1)}</span></nav>
  <div class="art-category">{e(SECTION)}</div>
  <h1>{e(H1)}</h1>
  <div class="art-byline"><strong>Edwin</strong><span class="sep">·</span><span>Master Automotive Technician</span><span class="sep">·</span><span>{BYLINE_DATE}</span><span class="sep">·</span><span>Edwin Garage, Ang Mo Kio</span></div>
</div></div>
<div class="article-wrap"><article class="article">
{body}</article></div>
<footer class="footer"><div class="footer-inner">
  <div class="footer-brand"><a class="logo" href="/"><span>Edwin</span> Garage</a><p>Car workshop in Ang Mo Kio since 2010. Servicing, repairs, aircon and accident claims.</p></div>
  <div class="footer-links"><h4>Services</h4><ul><li><a href="/car-servicing-repair/">Car Servicing &amp; Repair</a></li><li><a href="/car-aircon-repair/">Car Aircon Repair</a></li><li><a href="/accident-claim-repair/">Accident &amp; Dent Repair</a></li><li><a href="/prices/">Starting prices</a></li></ul></div>
  <div class="footer-links"><h4>Visit Us</h4><ul><li>Blk 5032 Ang Mo Kio Industrial Park 2 #01-295, Singapore 569535</li><li>Mon–Sat: 10am – 8pm · Closed Sundays</li><li><a href="https://wa.me/6597856612" target="_blank" rel="noopener">WhatsApp: 9785 6612</a> (enquiries)</li></ul></div>
  <div class="footer-links"><h4>Quick Links</h4><ul><li><a href="/articles/">Car Guides &amp; Articles</a></li><li><a href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a></li><li><a href="/about/">About Edwin Garage</a></li></ul></div>
</div><div class="footer-bottom"><p>© 2026 Edwin Garage Automotive Services Pte. Ltd. (UEN 201828727D) · Blk 5032 Ang Mo Kio Industrial Park 2 #01-295 · Singapore 569535</p></div><p style="text-align:center;font-size:.82rem;margin:12px 0 0"><a href="/privacy-policy/">Privacy Policy</a></p></footer>
<script src="/p1-cta.js" defer></script>
</body>
</html>
"""
out = pathlib.Path(__file__).with_name(SLUG + ".html")
out.write_text(page)
print(out, len(page.encode()))
