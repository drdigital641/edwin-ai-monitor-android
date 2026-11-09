import json, html, pathlib

SLUG = "car-burning-smell-singapore"
URL = f"https://www.sggarage.com/articles/{SLUG}.html"
TITLE = "Car Burning Smell in Singapore: What Each Smell Means"
H1 = "Burning Smell from Your Car in Singapore? What Each Smell Means and When to Stop"
DESC = ("Burning smell from your car in Singapore? How to tell burnt oil, coolant, brakes, rubber and "
        "electrical smells apart, which ones mean stop now, and what a workshop checks.")
PUB = "2026-11-08T07:30:00+08:00"
SECTION = "Engine & Safety"
IMG = "https://i.ibb.co/qM3ZKCDy/edwin-garage-og-image.jpg"

FAQ = [
 ("Is it safe to drive with a burning smell from my car?",
  "Not always. If you also see smoke, the temperature gauge is rising, a red warning light is on, or the smell is like burning plastic or wiring, pull over safely and switch off the engine. A faint smell that goes away, such as new brake pads bedding in or a little oil spilled during servicing, is usually not urgent, but have it checked if it lasts more than a few drives."),
 ("Why does my car smell like burning oil after driving?",
  "The most common reason is engine oil leaking onto the hot exhaust, often from a worn valve cover gasket or another seal. It can also be oil that was spilled during a recent oil change burning off. If the smell keeps coming back or you see oil spots under the car, have the leak traced."),
 ("What does a sweet burning smell mean?",
  "A sweet, syrupy smell usually means coolant is leaking onto a hot part of the engine. Watch the temperature gauge and stop driving if it climbs, because running low on coolant can overheat and damage the engine."),
 ("Why do my brakes smell after driving down a car park ramp?",
  "Long downhill ramps in multi-storey car parks make the brakes work hard, and hot brakes can give off a sharp smell. If it fades after the car cools, it is usually heat. If one wheel is much hotter than the others or the car pulls to one side, a brake may be sticking and should be checked."),
 ("Is a burning smell after servicing normal?",
  "A light smell for a short time after servicing can happen if a little oil was spilled on the engine and is burning off. It should fade within a day or two of driving. If it gets stronger, or you see smoke or drips, go back to the workshop and ask them to check."),
 ("What should I tell the workshop about a burning smell?",
  "Tell them what the smell is like (oil, sweet, rubber, plastic, sharp brakes), when it happens (cold start, after a long drive, after braking, with the aircon on), where it seems to come from, and whether any warning light or smoke appeared. Photos of drips under the car also help."),
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
     "keywords": "car burning smell Singapore, burning oil smell car, sweet smell car coolant, brake burning smell, burning plastic smell car, car smells after servicing"},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.sggarage.com"},
        {"@type": "ListItem", "position": 2, "name": "Car Guides", "item": "https://www.sggarage.com/articles/"},
        {"@type": "ListItem", "position": 3, "name": H1, "item": URL}]},
    {"@type": "WebPage", "@id": URL, "url": URL, "name": TITLE, "datePublished": PUB, "dateModified": PUB,
     "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".article h2", ".article p"]}}]}

e = lambda s: html.escape(s, quote=True)
tpl = pathlib.Path(__file__).with_name("style.css").read_text()

body = f"""
<p><strong>A burning smell from your car usually comes from one of five things: oil, coolant, brakes, a belt or hose, or wiring. Smoke, a rising temperature gauge, a red warning light or a smell of burning plastic means pull over and switch off. Most other smells can wait for a booked inspection, as long as they don't get worse.</strong></p>
<p>We are Edwin Garage, a car workshop in Ang Mo Kio. This guide helps you work out what the smell probably is, how urgent it is, and what to tell the workshop so the cause can be found quickly.</p>

<h2>When should you stop driving straight away?</h2>
<p>Pull over somewhere safe, switch off the engine and get everyone out of the car if you notice any of these with the smell:</p>
<ul>
<li><strong>Smoke</strong> from under the bonnet, from a wheel or from inside the cabin.</li>
<li><strong>The temperature gauge climbing</strong> towards hot, or a coolant warning light.</li>
<li><strong>A red warning light</strong> such as oil pressure, brake or battery. Our guide to <a href="/articles/dashboard-warning-lights-meaning-singapore.html">dashboard warning lights</a> explains each one.</li>
<li><strong>A smell of burning plastic or hot wiring</strong>, especially from the dashboard or fuse box area.</li>
<li><strong>A strong fuel smell</strong>. See <a href="/articles/car-fuel-smell-singapore.html">car fuel smell: when to stop driving</a>.</li>
</ul>
<p>If there is heavy smoke or steam, don't open the bonnet straight away: hot coolant and oil can burn you. Wait for it to cool, and call for a tow if you aren't sure the car is safe. Our <a href="/articles/breakdown-accident-towing-singapore.html">breakdown and towing guide</a> covers what to do next.</p>

<h2>What does each burning smell mean?</h2>
<p>Different faults smell different. Match what you notice with this table, then check the notes below it.</p>
<div class="tbl"><table class="art-tbl"><thead><tr><th>What it smells like</th><th>Likely cause</th><th>How urgent</th></tr></thead><tbody>
<tr><td>Burnt oil, sharp and smoky, often after a drive</td><td>Engine oil leaking onto the hot exhaust, or oil spilled during a recent oil change</td><td>Book a check soon. Stop if there is smoke or the oil warning light comes on.</td></tr>
<tr><td>Sweet and syrupy</td><td>Coolant leaking onto hot engine parts, or from the heater core inside the cabin</td><td>Watch the temperature gauge. Stop if it rises.</td></tr>
<tr><td>Hot, sharp, metallic, near one or more wheels</td><td>Hot brakes after a long ramp, a sticking brake caliper, or the handbrake left on</td><td>If one wheel is much hotter or the car pulls, get it checked before driving far.</td></tr>
<tr><td>Burning rubber</td><td>A slipping drive belt, or a hose or loose plastic touching the exhaust</td><td>Book a check. Stop if you also hear loud squealing and lose aircon or power steering.</td></tr>
<tr><td>Burning plastic or hot electrical smell</td><td>A wiring fault, an overheating fan motor or resistor, or something melted on the exhaust</td><td>Stop and switch off. Electrical smells can be a fire risk.</td></tr>
<tr><td>Rotten eggs (sulphur)</td><td>Catalytic converter problem, or a battery being overcharged</td><td>Book a check. Stop if the battery area is hot or hissing.</td></tr>
</tbody></table></div>

<h3>Burnt oil</h3>
<p>Oil that drips or seeps onto the exhaust burns with a sharp, smoky smell, often strongest when you stop at a traffic light or park after a drive. Common sources are a worn valve cover gasket or another engine seal. Look for dark spots on the ground where you park. Our articles on <a href="/articles/mercedes-e200-engine-oil-leak.html">Mercedes E200 oil leaks</a> and <a href="/articles/bmw-n20-engine-oil-leak-valve-cover-timing-chain-singapore.html">BMW N20 oil leaks</a> show what this looks like on two common cars.</p>

<h3>Sweet smell (coolant)</h3>
<p>Coolant has a sweet smell when it is hot. If you smell it from the engine bay, there may be a leaking hose, radiator or water pump. If you smell it inside the car, often with a misty windscreen, the heater core may be leaking. Low coolant can lead to overheating, so read <a href="/articles/car-coolant-leak-signs-risks-diagnosis.html">coolant leak signs</a> and <a href="/articles/car-engine-overheating-causes-singapore.html">engine overheating causes</a> before you drive far.</p>

<h3>Brakes</h3>
<p>Singapore drivers go down a lot of multi-storey car park ramps, and riding the brakes all the way down makes them hot. A smell that fades once the car cools is usually just heat. New brake pads can also smell for the first few drives while they bed in. A smell from one wheel only, a wheel that is much hotter than the others, or a car that pulls to one side can mean a brake is sticking. See <a href="/articles/brake-wear-replace-brake-pads-singapore.html">brake wear and when to replace brake pads</a>.</p>

<h3>Burning rubber</h3>
<p>A drive belt that slips on its pulleys can smell like hot rubber, often with a squeal. A hose or a loose plastic undertray touching the exhaust can smell the same. Our guide to <a href="/articles/car-belt-squeal-startup-singapore.html">belt squeal at startup</a> explains the belt side.</p>

<h3>Burning plastic or electrical smell</h3>
<p>This is the one not to ignore. A wiring fault, a blower fan motor or resistor running hot, or an aftermarket accessory wired in badly can all smell like hot plastic. Switch off the engine and don't keep driving until it has been checked. If the smell only comes through the aircon vents and is musty rather than burnt, it is more likely a dirty cabin filter or evaporator: see <a href="/articles/why-car-aircon-smells-and-how-to-fix-it.html">why car aircon smells</a>.</p>

<h2>What to do in the first few minutes</h2>
<ol>
<li><strong>Find a safe place to stop,</strong> switch on your hazard lights and switch off the engine.</li>
<li><strong>Look before you touch.</strong> Check for smoke, steam or drips under the car. Don't touch the wheels, exhaust or engine: they can be very hot.</li>
<li><strong>Check the dashboard.</strong> Note any warning lights and where the temperature gauge was before you stopped.</li>
<li><strong>Note when it happens.</strong> Cold start, after a long drive, after braking, only with the aircon on, or only when parked.</li>
<li><strong>Decide whether to drive on.</strong> If any of the stop signs above apply, don't. Call for a tow instead.</li>
</ol>

<h2>Burning smell after servicing or repairs</h2>
<p>A light smell for a short time after an oil change can be a little oil spilled on the engine or exhaust that is burning off. It should fade within a day or two of normal driving. New brake pads can smell for the first few drives too. If the smell gets stronger, you see smoke, or there are fresh drips under the car, go back to the workshop and ask them to look again. A good workshop will want to know.</p>

<h2>What a workshop checks</h2>
<p>To find the cause, a mechanic will usually:</p>
<ul>
<li>Look for oil and coolant leaks around the engine, hoses, radiator and exhaust.</li>
<li>Check the coolant and oil levels and the condition of the drive belt.</li>
<li>Compare wheel temperatures and check whether any brake is dragging.</li>
<li>Look for loose undertrays, plastic or debris touching the exhaust.</li>
<li>Check for signs of hot or damaged wiring, and test the fan and charging system if needed.</li>
</ul>
<p>The fix and its cost depend on what is found, so ask for the cause and a quote before approving any work. Our guide to <a href="/articles/car-diagnostic-fee-singapore.html">what a diagnostic fee covers</a> explains how this works at Edwin Garage.</p>

<h2>Frequently asked questions</h2>
""" + "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(a)}</p>" for q, a in FAQ) + """

<div class="takeaways-box"><h3>Key Takeaways</h3><ul>
<li>Smoke, a rising temperature gauge, a red warning light or a burning plastic smell means stop and switch off.</li>
<li>Burnt oil usually means a leak onto the exhaust; a sweet smell usually means coolant.</li>
<li>Hot brakes after a long ramp often fade; a smell from one wheel only can mean a sticking brake.</li>
<li>A light smell after servicing should fade within a day or two. If it doesn't, go back and ask.</li>
<li>Tell the workshop what it smells like, when it happens and whether any light came on.</li>
</ul></div>

<div class="cta-block">
  <h3>Still smelling something burning?</h3>
  <p>Edwin Garage is in Ang Mo Kio, serving Hougang, Yio Chu Kang, Serangoon and nearby areas. Inspections and repairs are by online appointment. WhatsApp 9785 6612 is for enquiries.</p>
  <a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a>
</div>
<div class="cluster-box"><h3>Related guides</h3><ul>
<li><a href="/articles/car-fuel-smell-singapore.html">Car Fuel Smell in Singapore: When to Stop Driving</a></li>
<li><a href="/articles/car-coolant-leak-signs-risks-diagnosis.html">Car Coolant Leak: Signs, Risks and Diagnosis</a></li>
<li><a href="/articles/car-engine-overheating-causes-singapore.html">Car Engine Overheating: Causes in Singapore</a></li>
<li><a href="/articles/brake-wear-replace-brake-pads-singapore.html">Brake Wear: When to Replace Brake Pads</a></li>
<li><a href="/articles/car-belt-squeal-startup-singapore.html">Car Belt Squeal at Startup in Singapore: What to Check</a></li>
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
  <div class="art-byline"><strong>Edwin</strong><span class="sep">·</span><span>Master Automotive Technician</span><span class="sep">·</span><span>November 8, 2026</span><span class="sep">·</span><span>Edwin Garage, Ang Mo Kio</span></div>
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
