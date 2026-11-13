import json, html, pathlib

SLUG = "car-engine-knocking-noise-singapore"
URL = f"https://www.sggarage.com/articles/{SLUG}.html"
TITLE = "Car Engine Knocking Noise: Causes and What to Do"
H1 = "Why Is My Car Engine Knocking, and Is It Safe to Keep Driving?"
DESC = ("Engine knocking or tapping? What the sound can mean (low oil, fuel, ignition, worn parts), "
        "when to stop driving and what to tell the workshop.")
PUB = "2026-11-14T01:30:00+08:00"
BYLINE_DATE = "November 14, 2026"
SECTION = "Engine"
IMG = "https://i.ibb.co/qM3ZKCDy/edwin-garage-og-image.jpg"
KEYWORDS = "car engine knocking noise Singapore, engine knock causes, engine tapping noise, engine pinging when accelerating, car engine rattle"

FAQ = [
 ("What causes an engine knocking noise?",
  "A knocking or tapping sound can come from low or wrong engine oil, fuel burning unevenly (often heard as pinging when you accelerate), carbon build-up, a weak ignition spark, a worn belt tensioner or accessory, or worn internal parts such as bearings. The sound alone is not enough to tell which, so it needs a proper check."),
 ("Is it safe to drive with an engine knocking?",
  "Not if the knock is deep, loud or comes with the oil warning light, a burning smell or loss of power. Stop safely, switch off and arrange recovery. A light tapping that fades once the engine is warm is less urgent, but still book a check soon."),
 ("What is the difference between knocking and pinging?",
  "Pinging is a light, metallic rattle heard mainly when you accelerate or climb a slope, and is linked to how the fuel burns. A deep knock that follows engine speed, and gets worse as revs rise, is more serious and can point to worn internal parts."),
 ("Can low engine oil cause a knocking noise?",
  "Yes. Oil keeps moving parts apart. When the level is low or the oil is old, parts can tap or knock. Check the dipstick on level ground with the engine off, and do not drive far if the oil light is on. See our guide to the engine oil pressure warning light."),
 ("Will a spark plug change fix an engine knock?",
  "Sometimes, if worn plugs cause misfiring or pinging. It will not fix a knock from worn internal parts. A diagnosis should come before replacing anything."),
 ("What should I tell the workshop about the noise?",
  "Say when it happens (cold start, warm engine, accelerating, idle), whether it follows engine speed, whether any warning light is on, and when the oil was last changed. Ask for the cause and a quote before you approve any work."),
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
<p><strong>An engine knocking or tapping noise can be as minor as pinging under load, or as serious as worn internal parts. Common causes are low or old oil, fuel burning unevenly, carbon build-up, weak ignition, a loose belt component, or worn bearings. If the knock is deep and loud, or comes with the oil warning light, stop safely, switch off and arrange recovery.</strong></p>
<p>We are Edwin Garage, a car workshop in Ang Mo Kio. This guide helps you describe the sound, decide whether to keep driving, and know what the workshop should check. It is a guide, not a diagnosis: the same sound can have different causes.</p>

<h2>Is it safe to keep driving with an engine knock?</h2>
<p>Stop and switch off if any of these happen:</p>
<ul>
<li>A deep, heavy knock that gets faster as the revs rise.</li>
<li>The oil pressure warning light is on.</li>
<li>Burning smell, smoke, or the temperature gauge climbing.</li>
<li>Sudden loss of power.</li>
</ul>
<p>Arrange recovery rather than driving on. If there is smoke or fire, get everyone out and call SCDF on 995. For a light tapping that fades once the engine is warm, you can usually drive to a workshop, but do not leave it for weeks. See also <a href="/articles/engine-oil-pressure-warning-light-singapore.html">the engine oil pressure warning light</a>.</p>

<h2>What does the sound tell you?</h2>
<p>Use the table to match what you hear. It narrows the possibilities, it does not confirm them.</p>
<div class="tbl"><table class="art-tbl"><thead><tr><th>What you notice</th><th>What it can point to</th><th>What to do</th></tr></thead><tbody>
<tr><td>Light metallic rattle when accelerating or on a slope</td><td>Pinging: fuel burning unevenly, carbon build-up or worn spark plugs</td><td>See <a href="/articles/spark-plug-replacement-singapore.html">spark plug replacement</a></td></tr>
<tr><td>Tapping on a cold start that fades when warm</td><td>Oil slow to reach parts, old or wrong oil</td><td>Check the oil level and when it was last changed</td></tr>
<tr><td>Tapping with the oil light on</td><td>Low oil or low oil pressure</td><td>Stop. See <a href="/articles/engine-oil-pressure-warning-light-singapore.html">oil pressure warning light</a></td></tr>
<tr><td>Knocking with shaking or jerking</td><td>Misfire</td><td>See <a href="/articles/engine-misfiring-car-jerking-causes-diagnosis-repair.html">engine misfiring and jerking</a></td></tr>
<tr><td>Deep knock that follows engine speed</td><td>Worn internal parts such as bearings</td><td>Stop driving and arrange recovery</td></tr>
<tr><td>Knock with temperature rising</td><td>Overheating damage risk</td><td>Stop. See <a href="/articles/car-engine-overheating-causes-singapore.html">engine overheating causes</a></td></tr>
</tbody></table></div>

<h3>Check the oil first</h3>
<p>With the car on level ground and the engine off for a few minutes, check the dipstick. A low level is a common and fixable cause. Skipping oil changes also adds wear over time; see <a href="/articles/what-happens-skip-engine-oil-change-singapore.html">what happens if you skip an engine oil change</a>.</p>

<h3>Cold start or warm engine?</h3>
<p>Note when the noise happens. A sound only on a cold start points in a different direction from one that appears when the engine is hot or under load. This detail helps the workshop a lot.</p>

<h2>What should the workshop check?</h2>
<ul>
<li>Engine oil level, condition and pressure.</li>
<li>A scan for stored fault codes, including misfire.</li>
<li>Spark plugs and ignition parts.</li>
<li>Belts, tensioner and accessories that can tap or rattle.</li>
<li>Listening at the engine to locate where the sound comes from.</li>
</ul>
<p>Ask for the cause and a quote before you approve any work. Our guide to <a href="/articles/car-diagnostic-fee-singapore.html">what a diagnostic fee covers</a> explains how this works at Edwin Garage.</p>

<section aria-labelledby="edwin-assessment" style="padding:24px;margin:32px 0;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px">
<h2 id="edwin-assessment" style="margin-top:0">Book an engine check</h2>
<p>Inspections and repairs at Edwin Garage in Ang Mo Kio are by appointment, booked online. WhatsApp 9785 6612 is for enquiries. Open 10am to 8pm, Monday to Saturday; closed Sundays. See our <a href="/car-servicing-repair/">car servicing and repair</a> page.</p>
<p><a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book an inspection online</a></p>
</section>

<h2>Frequently asked questions</h2>
""" + "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(a)}</p>" for q, a in FAQ) + """

<div class="takeaways-box"><h3>Key Takeaways</h3><ul>
<li>A deep knock, the oil light or a burning smell means stop and arrange recovery.</li>
<li>Check the oil level first; low or old oil is a common cause.</li>
<li>Note when the noise happens: cold start, warm, accelerating or idle.</li>
<li>Get a diagnosis before replacing parts.</li>
</ul></div>

<div class="cta-block">
  <h3>Engine making a noise?</h3>
  <p>Edwin Garage is in Ang Mo Kio, serving Hougang, Yio Chu Kang, Serangoon and nearby areas. Inspections and repairs are by online appointment. WhatsApp 9785 6612 is for enquiries.</p>
  <a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a>
</div>
<div class="cluster-box"><h3>Related guides</h3><ul>
<li><a href="/articles/engine-oil-pressure-warning-light-singapore.html">Engine Oil Pressure Warning Light</a></li>
<li><a href="/articles/engine-misfiring-car-jerking-causes-diagnosis-repair.html">Engine Misfiring and Jerking</a></li>
<li><a href="/articles/spark-plug-replacement-singapore.html">Spark Plug Replacement</a></li>
<li><a href="/articles/car-engine-overheating-causes-singapore.html">Car Engine Overheating Causes</a></li>
<li><a href="/articles/what-happens-skip-engine-oil-change-singapore.html">What Happens If You Skip an Oil Change</a></li>
<li><a href="/articles/car-diagnostic-fee-singapore.html">Car Diagnostic Fee</a></li>
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
