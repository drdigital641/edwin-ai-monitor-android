import json, html, pathlib

SLUG = "car-exhaust-smoke-colour-singapore"
URL = f"https://www.sggarage.com/articles/{SLUG}.html"
TITLE = "Car Exhaust Smoke Colour: White, Blue or Black?"
H1 = "White, Blue or Black Smoke from Your Car Exhaust? What Each Colour Means"
DESC = ("Car exhaust smoking? How to tell normal morning vapour from white, blue-grey and black smoke, "
        "what each colour means and when to stop driving.")
PUB = "2026-11-09T10:45:00+08:00"
BYLINE_DATE = "November 9, 2026"
SECTION = "Engine & Safety"
IMG = "https://i.ibb.co/qM3ZKCDy/edwin-garage-og-image.jpg"
KEYWORDS = "car exhaust smoke Singapore, white smoke from exhaust, blue smoke from exhaust, black smoke from exhaust, exhaust smoke colour meaning, car smoking exhaust"

FAQ = [
 ("Is white smoke from the exhaust normal in the morning?",
  "A thin white vapour on a cold start that clears within a few minutes of driving is usually water condensation, and it is common in humid weather. Thick white smoke that keeps coming after the engine is warm, or smells sweet, is not normal and needs checking, because it can mean coolant is getting into the engine."),
 ("What does blue or grey smoke from the exhaust mean?",
  "Blue-grey smoke usually means the engine is burning oil. Worn valve stem seals, worn piston rings or a leaking turbo seal are common causes. Check the oil level on the dipstick, top up if it is low, and book an inspection. Stop driving if the oil pressure warning light comes on."),
 ("What causes black smoke from a petrol car exhaust?",
  "Black smoke means the engine is burning too much fuel for the air it gets. A blocked air filter, a leaking or sticking fuel injector or a faulty sensor are common causes. It wastes fuel and can damage the catalytic converter over time, so have it diagnosed rather than ignored."),
 ("Can I keep driving if my exhaust is smoking?",
  "Not if the smoke is thick and continuous, the temperature gauge is rising, a red warning light is on, the engine is losing power or you smell fuel. Pull over safely, switch off and arrange recovery. A short puff on start-up with no other symptoms can usually wait for a booked inspection, but don't leave it for weeks."),
 ("Will a smoking exhaust fail the vehicle inspection?",
  "Cars due for their periodic inspection have their exhaust emissions tested, so visible smoke is worth fixing before your inspection date. Fixing the cause also stops the problem from getting more expensive."),
 ("What should I tell the workshop about exhaust smoke?",
  "Tell them the colour, whether it happens only on a cold start or all the time, whether it gets worse when you accelerate, any smell (sweet, oily or fuel), and whether the oil or coolant level has been dropping. A short phone video of the smoke from behind the car helps a lot."),
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
# Shared footer (incl. the Google review button, 13 Nov 2026): edit footer.html once, every article builder reads it.
FOOTER = pathlib.Path(__file__).with_name("footer.html").read_text()

body = f"""
<p><strong>The colour of the smoke tells you where to look. Thin white vapour on a cold morning that clears in a few minutes is usually just condensation. Thick white smoke that keeps coming can mean coolant is burning, blue-grey smoke means oil is burning, and black smoke means too much fuel. Smoke with a rising temperature gauge, a red warning light, a fuel smell or loss of power means pull over and switch off.</strong></p>
<p>We are Edwin Garage, a car workshop in Ang Mo Kio. This guide helps you read what your exhaust is telling you, decide how urgent it is, and tell the workshop what it needs to know to find the cause quickly.</p>

<h2>When should you stop driving straight away?</h2>
<p>Pull over somewhere safe, switch off the engine and don't continue if you see exhaust smoke together with any of these:</p>
<ul>
<li><strong>Thick smoke that keeps pouring out</strong>, not just a puff when you start the car.</li>
<li><strong>The temperature gauge climbing</strong> towards hot, or a coolant warning light. See <a href="/articles/car-engine-overheating-causes-singapore.html">engine overheating causes</a>.</li>
<li><strong>A red warning light</strong>, especially oil pressure. Our <a href="/articles/engine-oil-pressure-warning-light-singapore.html">oil pressure warning light guide</a> explains why this one matters.</li>
<li><strong>A strong fuel smell</strong>. See <a href="/articles/car-fuel-smell-singapore.html">car fuel smell: when to stop driving</a>.</li>
<li><strong>Loss of power, heavy shaking or loud knocking</strong> from the engine.</li>
</ul>
<p>If smoke is coming from under the bonnet rather than the exhaust pipe, treat it as a possible fire: get everyone out and away from the car and traffic, don't open the bonnet, and call SCDF on 995. Our <a href="/articles/car-burning-smell-singapore.html">burning smell guide</a> covers this. For a car that is unsafe to drive, arrange recovery instead of driving it to a workshop; the <a href="/articles/breakdown-accident-towing-singapore.html">breakdown and towing guide</a> explains what to do next.</p>

<h2>What does each smoke colour mean?</h2>
<p>Look at the smoke from behind the car in daylight, with the engine idling and then with someone gently revving it. The table below is a guide to where the fault usually is, not a diagnosis.</p>
<div class="tbl"><table class="art-tbl"><thead><tr><th>What you see</th><th>What it usually means</th><th>How urgent</th></tr></thead><tbody>
<tr><td>Thin white vapour on a cold start that clears in a few minutes</td><td>Water condensation in the exhaust, common in humid weather</td><td>Normal. No action needed if it disappears once the engine is warm.</td></tr>
<tr><td>Thick white smoke that continues when the engine is warm, often smelling sweet</td><td>Coolant getting into the engine, for example from a failing head gasket</td><td>Check the coolant level when the engine is cold and book an inspection soon. Stop if the temperature gauge rises.</td></tr>
<tr><td>Blue or grey smoke, often with an oily smell</td><td>Engine oil being burnt: valve stem seals, piston rings, turbo seals or a breather fault</td><td>Check the dipstick and top up if low. Book an inspection. Stop if the oil pressure light comes on.</td></tr>
<tr><td>Black or dark grey smoke, worse when you accelerate</td><td>Too much fuel for the air: blocked air filter, faulty injector or sensor</td><td>Book a diagnosis. It wastes fuel and can damage the catalytic converter.</td></tr>
<tr><td>Smoke from under the bonnet, not the exhaust pipe</td><td>Oil or coolant on hot engine parts, or a possible fire</td><td>Stop, get everyone away from the car and call 995 if fire is possible.</td></tr>
</tbody></table></div>

<h3>White smoke: condensation or coolant?</h3>
<p>Every petrol engine makes water when it burns fuel. When the exhaust is cold, that water shows up as thin white vapour and sometimes drips from the tailpipe. In Singapore's humid mornings this is very common, and it disappears once the exhaust warms up. That is normal.</p>
<p>Thick white smoke that keeps coming after the engine is warm is different. It often smells sweet and may come with a falling coolant level, a misfire on start-up or overheating. These point to coolant leaking into the cylinders, often from a <a href="/articles/head-gasket-failure-warning-signs-singapore.html">failing head gasket</a>. Keep an eye on the temperature gauge and don't open the radiator or coolant cap while the engine is hot. On some Subaru engines this shows up together with coolant and oil mixing, which we explain in our <a href="/articles/subaru-xv-forester-impreza-coolant-mixing-oil-singapore.html">Subaru coolant and oil guide</a>.</p>

<h3>Blue or grey smoke: burning oil</h3>
<p>Blue-grey smoke means engine oil is reaching the combustion chamber and being burnt. A puff of blue smoke right after a cold start that then stops often points to worn valve stem seals. Smoke that continues while driving, especially when you accelerate, points more to worn piston rings. On turbo engines, a leaking turbo seal can do the same. A blocked breather (PCV) system can also push oil where it shouldn't go.</p>
<p>The practical sign is the oil level dropping between services. Check the dipstick on level ground with the engine off and cool, and top up with the right oil if it is low. Our guide to <a href="/articles/hyundai-tucson-engine-oil-consumption-singapore.html">engine oil consumption</a> explains how much oil use is worth worrying about, and <a href="/articles/what-happens-skip-engine-oil-change-singapore.html">what happens if you skip oil changes</a> explains why running low is risky.</p>

<h3>Black smoke: too much fuel</h3>
<p>Black smoke from a petrol car means the engine is getting more fuel than it can burn. Common causes are a blocked air filter, a fuel injector that leaks or sticks open, or a faulty sensor telling the engine computer the wrong thing. You may also notice poor fuel economy, rough idling or a check engine light. If the engine is also jerking or misfiring, see our guide to <a href="/articles/engine-misfiring-car-jerking-causes-diagnosis-repair.html">engine misfiring and jerking</a>.</p>
<p>On a diesel, a short puff of dark smoke under hard acceleration can be normal on older models, but continuous black smoke is not. Either way, have it diagnosed, because unburnt fuel can overheat and damage the catalytic converter.</p>

<h2>What to do in the first few minutes</h2>
<ol>
<li><strong>Check the dashboard.</strong> Look at the temperature gauge and any warning lights before deciding to drive on.</li>
<li><strong>If any stop sign above applies,</strong> pull over safely, switch on your hazard lights and switch off the engine.</li>
<li><strong>Note the colour and when it happens:</strong> cold start only, all the time, or only when you accelerate.</li>
<li><strong>Take a short video</strong> of the exhaust from a safe spot behind the car, away from traffic.</li>
<li><strong>Once the engine has cooled,</strong> check the oil and coolant levels. Don't open a hot coolant cap.</li>
</ol>

<h2>What a workshop checks</h2>
<p>To find the cause, a mechanic will usually:</p>
<ul>
<li>Look at the smoke at idle and when revving, and note the smell.</li>
<li>Check the oil and coolant levels and look for coolant or oil where it shouldn't be.</li>
<li>Read fault codes and live sensor data with a diagnostic scanner.</li>
<li>Check the air filter, breather system and, on turbo engines, the turbo for oil leaks.</li>
<li>If coolant loss is suspected, pressure-test the cooling system or check for exhaust gases in the coolant.</li>
<li>If oil burning is suspected, do a compression or leak-down test to check the piston rings and valves.</li>
</ul>
<p>The fix and its cost depend on what is found, so ask for the cause and a quote before you approve any work. Our guide to <a href="/articles/car-diagnostic-fee-singapore.html">what a diagnostic fee covers</a> explains how this works at Edwin Garage.</p>

<section aria-labelledby="edwin-assessment" style="padding:24px;margin:32px 0;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px">
<h2 id="edwin-assessment" style="margin-top:0">Book an exhaust smoke check</h2>
<p>Inspections and repairs at Edwin Garage in Ang Mo Kio are by appointment, booked online. WhatsApp 9785 6612 is for enquiries. Open 10am to 8pm, Monday to Saturday; closed Sundays. If the car is not safe to drive, arrange recovery rather than driving it to your booking.</p>
<p><a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book an inspection online</a></p>
</section>

<h2>Frequently asked questions</h2>
""" + "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(a)}</p>" for q, a in FAQ) + """

<div class="takeaways-box"><h3>Key Takeaways</h3><ul>
<li>Thin white vapour on a cold morning that clears in a few minutes is usually condensation.</li>
<li>Thick white smoke when warm, often sweet-smelling, can mean coolant is burning.</li>
<li>Blue-grey smoke means oil is burning; check the dipstick and book an inspection.</li>
<li>Black smoke means too much fuel; it wastes fuel and can damage the catalytic converter.</li>
<li>Smoke with a rising temperature gauge, a red warning light, a fuel smell or loss of power means stop and switch off.</li>
</ul></div>

<div class="cta-block">
  <h3>Smoke from your exhaust?</h3>
  <p>Edwin Garage is in Ang Mo Kio, serving Hougang, Yio Chu Kang, Serangoon and nearby areas. Inspections and repairs are by online appointment. WhatsApp 9785 6612 is for enquiries.</p>
  <a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a>
</div>
<div class="cluster-box"><h3>Related guides</h3><ul>
<li><a href="/articles/head-gasket-failure-warning-signs-singapore.html">Head Gasket Failure: Warning Signs</a></li>
<li><a href="/articles/car-burning-smell-singapore.html">Car Burning Smell in Singapore: What Each Smell Means</a></li>
<li><a href="/articles/engine-misfiring-car-jerking-causes-diagnosis-repair.html">Engine Misfiring and Car Jerking: Causes and Diagnosis</a></li>
<li><a href="/articles/car-engine-overheating-causes-singapore.html">Car Engine Overheating: Causes in Singapore</a></li>
<li><a href="/articles/engine-oil-pressure-warning-light-singapore.html">Engine Oil Pressure Warning Light</a></li>
<li><a href="/articles/car-diagnostic-fee-singapore.html">Car Diagnostic Fee in Singapore: What Does It Cover?</a></li>
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
{FOOTER}<script src="/p1-cta.js" defer></script>
</body>
</html>
"""
out = pathlib.Path(__file__).with_name(SLUG + ".html")
out.write_text(page)
print(out, len(page.encode()))
