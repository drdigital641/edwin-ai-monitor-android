import json, html, pathlib

SLUG = "car-stalls-at-traffic-lights-singapore"
URL = f"https://www.sggarage.com/articles/{SLUG}.html"
TITLE = "Car Stalls at Traffic Lights: Causes and What to Do"
H1 = "Car Stalling at Traffic Lights or When Slowing Down? Causes and What to Do"
DESC = ("Engine dies at traffic lights or when you slow down? What to do in the moment, common causes "
        "(idle control, vacuum leak, sensors, fuel, battery) and what to tell the workshop.")
PUB = "2026-11-11T01:30:00+08:00"
BYLINE_DATE = "November 11, 2026"
SECTION = "Engine"
IMG = "https://i.ibb.co/qM3ZKCDy/edwin-garage-og-image.jpg"
KEYWORDS = "car stalls at traffic lights Singapore, engine stalls when slowing down, car dies at idle, engine cuts out when stopping, car stalling causes"

FAQ = [
 ("Why does my car stall when I stop at traffic lights?",
  "At idle the engine runs on a small, carefully controlled amount of air and fuel. If something upsets that, such as a dirty throttle body, a vacuum leak, a faulty sensor, weak spark or a fuel supply problem, the engine can die when you lift off the accelerator. Heavy electrical or aircon load can tip a weak engine over the edge. The cause needs checking, not guessing."),
 ("Is it dangerous if my car stalls in traffic?",
  "It can be. When the engine stops, the power steering and brake assist reduce, so the steering and brake pedal feel heavier, but they still work. Keep calm, press the brake firmly, steer to a safe spot and switch on your hazard lights. If the car keeps stalling, stop driving it and arrange an inspection."),
 ("Can a weak battery or alternator make a car stall?",
  "Yes. If the alternator is not charging properly, the car runs down the battery and can stall at low engine speed when electrical load is high. Our alternator and starting guides explain the signs. A workshop can test the charging system."),
 ("Should I keep restarting the engine if it stalls?",
  "Restart it once or twice to move to a safe place. If it will not stay running, or you smell fuel, stop. Repeated cranking can drain the battery and, if there is a fuel problem, make it worse. Arrange recovery instead."),
 ("Does a stalling car mean the gearbox is faulty?",
  "Sometimes. In an automatic, the car stalling when you brake to a stop or select Drive can point to a gearbox or torque converter fault, but engine causes are more common. A diagnostic scan and road test separate the two."),
 ("What should I tell the workshop about the stalling?",
  "Tell them when it happens: cold or hot engine, when slowing, at a standstill, with the aircon on, or when turning the steering. Note any warning lights, rough idle or fuel smell, and whether it began after refuelling, a battery change or other work."),
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
<p><strong>A car that stalls at traffic lights or when slowing down usually has a problem at idle: a dirty throttle body, a vacuum leak, a faulty sensor, weak spark, a fuel supply fault or a weak charging system. In the moment, keep calm, brake firmly, steer to a safe place and switch on your hazard lights. A car that stalls repeatedly, or stalls with a fuel smell or warning lights, should not be driven. Arrange an inspection or recovery.</strong></p>
<p>We are Edwin Garage, a car workshop in Ang Mo Kio. This guide covers what to do the moment the engine dies, what usually causes it, and what to tell the workshop so the cause is found quickly.</p>

<h2>What should you do the moment the engine stalls?</h2>
<ol>
<li><strong>Keep calm and brake firmly.</strong> The steering and brake pedal feel heavier without engine assistance, but they still work. Press the brake pedal harder than usual.</li>
<li><strong>Switch on your hazard lights</strong> so drivers behind you see you.</li>
<li><strong>Steer to a safe place</strong> if the car is still rolling.</li>
<li><strong>Restart once or twice.</strong> In an automatic, put the selector in Neutral or Park first. In a manual, press the clutch.</li>
<li><strong>If it will not stay running,</strong> stop trying and arrange recovery. Repeated cranking drains the battery.</li>
</ol>
<p>Stop driving and call for recovery if the stalling comes with a <strong>fuel smell</strong>, <strong>smoke</strong>, a <strong>red warning light</strong> or a burning smell. See <a href="/articles/car-fuel-smell-singapore.html">car fuel smell</a> and <a href="/articles/breakdown-accident-towing-singapore.html">breakdown and towing</a>. In case of fire, get everyone out and call SCDF 995.</p>

<h2>What usually causes a car to stall at idle?</h2>
<p>When it happens and what else you notice points to where to look. The table is a guide to the usual causes, not a diagnosis.</p>
<div class="tbl"><table class="art-tbl"><thead><tr><th>What you notice</th><th>What it usually means</th><th>How urgent</th></tr></thead><tbody>
<tr><td>Stalls when you stop, with a rough or hunting idle beforehand</td><td>Dirty throttle body or idle air passage, or a vacuum leak</td><td>Book an inspection soon. See <a href="/articles/car-vibrates-at-idle-singapore.html">car vibrates at idle</a>.</td></tr>
<tr><td>Stalls with the check engine light on, or a jerk before it dies</td><td>Faulty sensor or misfire, such as spark plugs or ignition parts</td><td>Book a scan. See <a href="/articles/engine-misfiring-car-jerking-causes-diagnosis-repair.html">engine misfiring and jerking</a>.</td></tr>
<tr><td>Stalls and is slow to restart, or loses power when accelerating</td><td>Fuel supply problem, such as a weak pump or a blocked filter</td><td>Do not delay. A car that cuts out while driving is a safety risk.</td></tr>
<tr><td>Stalls with the lights dimming, a battery light or slow cranking</td><td>Weak battery or alternator not charging</td><td>Book a charging test. See <a href="/articles/alternator-failure-signs-car-battery-dying.html">alternator failure signs</a>.</td></tr>
<tr><td>Stalls only when the aircon is on or when turning the steering fully</td><td>Idle not compensating for the extra load</td><td>Book an inspection soon.</td></tr>
<tr><td>Automatic stalls as you brake to a stop or select Drive</td><td>Possible gearbox or torque converter fault</td><td>Book a scan and road test promptly.</td></tr>
</tbody></table></div>

<h3>Idle control and air leaks</h3>
<p>At idle the engine computer controls a small amount of air through the throttle. Carbon build-up in the throttle body, a cracked vacuum hose or a leaking intake gasket upsets that air. The engine then idles unevenly and can stall when you lift off the accelerator.</p>

<h3>Sensors, spark and fuel</h3>
<p>Sensors tell the computer how much air is coming in and how fast the engine is turning. If one gives a wrong reading, the fuel and spark can be wrong and the engine dies. Worn spark plugs and ignition parts cause misfires that can become a stall; see <a href="/articles/spark-plug-replacement-singapore.html">spark plug replacement</a>. A weak fuel pump or blocked filter can starve the engine, usually with loss of power first.</p>

<h3>Battery and charging</h3>
<p>If the alternator is not charging well, the battery runs down and the engine can stall at low speed, especially with the lights, aircon and wipers on. A battery or charging warning light, dimming lights or slow starting are clues. Our <a href="/articles/car-wont-start-morning-battery-alternator-starter-singapore.html">guide to starting problems</a> explains the difference between battery, alternator and starter.</p>

<h2>What a workshop checks</h2>
<ul>
<li>Scan for stored fault codes, then check live sensor data.</li>
<li>Inspect the throttle body, intake and vacuum hoses for dirt and leaks.</li>
<li>Check the spark plugs and ignition parts.</li>
<li>Test fuel pressure and look at the fuel filter where one is fitted.</li>
<li>Test the battery and the alternator output.</li>
<li>Road test to see when the stall happens, including with the aircon on.</li>
</ul>
<p>The fix depends on what is found, so ask for the cause and a quote before you approve any work. Our guide to <a href="/articles/car-diagnostic-fee-singapore.html">what a diagnostic fee covers</a> explains how this works at Edwin Garage. If a warning light is on, see <a href="/articles/dashboard-warning-lights-meaning-singapore.html">what dashboard warning lights mean</a>.</p>

<section aria-labelledby="edwin-assessment" style="padding:24px;margin:32px 0;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px">
<h2 id="edwin-assessment" style="margin-top:0">Book a stalling check</h2>
<p>Inspections and repairs at Edwin Garage in Ang Mo Kio are by appointment, booked online. WhatsApp 9785 6612 is for enquiries. Open 10am to 8pm, Monday to Saturday; closed Sundays. If the car keeps stalling, arrange recovery rather than driving it to your booking.</p>
<p><a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book an inspection online</a></p>
</section>

<h2>Frequently asked questions</h2>
""" + "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(a)}</p>" for q, a in FAQ) + """

<div class="takeaways-box"><h3>Key Takeaways</h3><ul>
<li>Brake firmly, switch on the hazard lights and steer to a safe spot if the engine dies.</li>
<li>Common causes are a dirty throttle body, a vacuum leak, a faulty sensor, weak spark, a fuel fault or a weak charging system.</li>
<li>A fuel smell, smoke or a red warning light means stop and arrange recovery.</li>
<li>Tell the workshop when it stalls, whether the engine is hot or cold, and if the aircon is on.</li>
</ul></div>

<div class="cta-block">
  <h3>Car stalling?</h3>
  <p>Edwin Garage is in Ang Mo Kio, serving Hougang, Yio Chu Kang, Serangoon and nearby areas. Inspections and repairs are by online appointment. WhatsApp 9785 6612 is for enquiries.</p>
  <a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a>
</div>
<div class="cluster-box"><h3>Related guides</h3><ul>
<li><a href="/articles/car-vibrates-at-idle-singapore.html">Car Vibrates at Idle</a></li>
<li><a href="/articles/engine-misfiring-car-jerking-causes-diagnosis-repair.html">Engine Misfiring and Car Jerking</a></li>
<li><a href="/articles/spark-plug-replacement-singapore.html">Spark Plug Replacement</a></li>
<li><a href="/articles/alternator-failure-signs-car-battery-dying.html">Alternator Failure Signs</a></li>
<li><a href="/articles/car-fuel-smell-singapore.html">Car Fuel Smell</a></li>
<li><a href="/articles/dashboard-warning-lights-meaning-singapore.html">Dashboard Warning Lights Meaning</a></li>
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
