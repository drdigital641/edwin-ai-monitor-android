import json, html, pathlib

SLUG = "car-windscreen-fogging-up-inside-singapore"
URL = f"https://www.sggarage.com/articles/{SLUG}.html"
TITLE = "Car Windscreen Fogging Up Inside: Causes and Fixes"
H1 = "Why Does My Car Windscreen Fog Up Inside, and How Do I Clear It?"
DESC = ("Windscreen misting up inside during rain or a humid morning? Common causes (wet mats, "
        "recirculation mode, dirty cabin filter, aircon not drying, a water leak) and how to clear it safely.")
PUB = "2026-11-13T01:30:00+08:00"
BYLINE_DATE = "November 13, 2026"
SECTION = "Aircon"
IMG = "https://i.ibb.co/qM3ZKCDy/edwin-garage-og-image.jpg"
KEYWORDS = "car windscreen fogging up inside Singapore, car window fog rain, how to demist windscreen, car aircon defog, windscreen mist cabin filter"

FAQ = [
 ("Why does my car windscreen fog up inside?",
  "Fog forms when warm, moist air inside the cabin meets cooler glass. In Singapore the usual causes are damp carpets or mats, breath and wet clothes after rain, the aircon on recirculation, a dirty cabin filter that limits airflow, or an aircon that is not drying the air well. A persistent damp smell or wet carpet can point to a water leak."),
 ("What is the fastest way to clear a fogged windscreen?",
  "Turn the aircon on, point the airflow at the windscreen, switch to fresh-air mode instead of recirculation, and set the temperature to a comfortable level. Many cars have a demist button that does this for you. Open a window slightly if it is slow, and wipe only as a last resort, because wiping with a cloth can leave streaks."),
 ("Is it safe to drive with a fogged windscreen?",
  "No. Pull over safely and clear the glass first. Driving with poor visibility, especially at night or in heavy rain, is dangerous."),
 ("Why does the fog return when I switch the aircon off?",
  "Moisture is still inside the cabin. The aircon removes humidity as it cools, so without it the damp air meets the cool glass again. Dry the carpets and mats, and look for the source of the moisture."),
 ("Could a dirty cabin filter cause a fogged windscreen?",
  "It can contribute. A blocked cabin filter reduces airflow, so the demisting is slower and weaker. Our guide to cabin filter replacement explains when to change it."),
 ("When should I see a workshop about a fogging windscreen?",
  "See a workshop if the fog keeps coming back after you dry the cabin, if the carpet or floor is wet without a spill, if there is a damp or musty smell, or if the aircon blows weak or warm air. These point to a leak, a blocked drain or an aircon fault."),
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
<p><strong>A windscreen fogs up inside when warm, damp air in the cabin meets cooler glass. In Singapore the usual causes are damp mats and clothes after rain, the aircon on recirculation, a dirty cabin filter, an aircon that is not drying the air, or a water leak. To clear it, switch the aircon on, choose fresh air, and aim the airflow at the glass. If you cannot see clearly, pull over safely first.</strong></p>
<p>We are Edwin Garage, a car workshop in Ang Mo Kio. This guide covers how to clear a fogged windscreen quickly, why it happens, and when it means something needs checking. If the fog is on the outside of the glass, the wipers clear it; this guide is about fog inside the car.</p>

<h2>How do you clear a fogged windscreen quickly?</h2>
<ol>
<li><strong>Pull over if you cannot see.</strong> Do not drive with poor visibility. Stop somewhere safe, use hazard lights if needed, and clear the glass first.</li>
<li><strong>Turn the aircon on.</strong> The aircon removes moisture from the air as it cools, so it clears fog faster than heat alone.</li>
<li><strong>Choose fresh-air mode.</strong> Recirculation keeps the damp cabin air going round. Fresh air brings in air that can take up the moisture.</li>
<li><strong>Aim the airflow at the windscreen</strong> and raise the fan speed. Many cars have a demist or defrost button that sets this up.</li>
<li><strong>Crack a window open</strong> for a moment if it is slow, to let humid air out.</li>
</ol>
<p>Avoid wiping with your hand or a cloth. It smears the film and can leave streaks that glare at night. If the glass is streaky even when clean, see our guide to <a href="/articles/car-wiper-streaks-singapore.html">car wiper streaks</a>.</p>

<h2>Why does the windscreen fog up inside?</h2>
<p>The cause is moisture in the cabin. Use the table to see which one fits your car. It is a guide, not a diagnosis.</p>
<div class="tbl"><table class="art-tbl"><thead><tr><th>What you notice</th><th>What it usually means</th><th>What to do</th></tr></thead><tbody>
<tr><td>Fog after rain, clears once the aircon runs</td><td>Wet clothes, umbrellas and damp mats adding moisture</td><td>Dry the mats, leave the aircon on fresh air for a few minutes</td></tr>
<tr><td>Fog stays and the air barely moves</td><td>Blocked cabin filter reducing airflow</td><td>See <a href="/articles/car-cabin-filter-replacement-singapore.html">cabin filter replacement</a></td></tr>
<tr><td>Fog clears slowly, air is not cold</td><td>Aircon not cooling or drying the air well</td><td>See <a href="/articles/car-aircon-not-cold-singapore-causes-repair-options.html">aircon not cold</a></td></tr>
<tr><td>Fog returns every time, damp or musty smell</td><td>Moisture stuck in the carpet or aircon box</td><td>See <a href="/articles/car-aircon-smell-solution-singapore.html">car aircon smell</a></td></tr>
<tr><td>Wet carpet or floor with no spill</td><td>A water leak, for example a blocked drain or a seal</td><td>See <a href="/articles/water-under-car-aircon-or-leak-singapore.html">water under the car, aircon or leak</a></td></tr>
<tr><td>Aircon blows warm air</td><td>Aircon fault, so it cannot dry the air</td><td>See <a href="/articles/car-aircon-blowing-warm-air-singapore.html">aircon blowing warm air</a></td></tr>
</tbody></table></div>

<h3>Recirculation mode</h3>
<p>Recirculation reuses the cabin air. With a few passengers breathing, or after rain, the humidity builds up and settles on the glass. Switching to fresh air is often all that is needed.</p>

<h3>Damp mats and carpet</h3>
<p>A wet floor mat acts like a slow humidifier. Take the mats out to dry after a rainy day, and check the carpet underneath. If the carpet is wet and nothing was spilled, look for the source of the water.</p>

<h3>Cabin filter and the aircon</h3>
<p>The cabin filter cleans the air before it reaches the vents. When it is clogged, less air flows and the windscreen clears more slowly. An aircon in good condition also dries the air as it cools. If the cooling is weak, the demisting is weak too.</p>

<h2>When should you see a workshop?</h2>
<ul>
<li>The fog keeps coming back after you dry the cabin.</li>
<li>The carpet or floor is wet and you cannot find why.</li>
<li>There is a damp or musty smell when the aircon starts.</li>
<li>The aircon blows weak or warm air.</li>
<li>The glass clears slowly even with the aircon on fresh air.</li>
</ul>
<p>A workshop can check the aircon, the cabin filter and the places water can enter. Ask for the cause and a quote before you approve any work. Our guide to <a href="/articles/car-diagnostic-fee-singapore.html">what a diagnostic fee covers</a> explains how this works at Edwin Garage.</p>

<section aria-labelledby="edwin-assessment" style="padding:24px;margin:32px 0;background:#EFF6FF;border:1px solid #BFDBFE;border-radius:12px">
<h2 id="edwin-assessment" style="margin-top:0">Book an aircon and cabin check</h2>
<p>Inspections and repairs at Edwin Garage in Ang Mo Kio are by appointment, booked online. WhatsApp 9785 6612 is for enquiries. Open 10am to 8pm, Monday to Saturday; closed Sundays. See our <a href="/car-aircon-repair/">car aircon repair</a> page for how aircon checks work.</p>
<p><a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book an inspection online</a></p>
</section>

<h2>Frequently asked questions</h2>
""" + "\n".join(f"<h3>{e(q)}</h3>\n<p>{e(a)}</p>" for q, a in FAQ) + """

<div class="takeaways-box"><h3>Key Takeaways</h3><ul>
<li>Fog inside the glass is moisture: use the aircon on fresh air, aimed at the windscreen.</li>
<li>Do not drive until you can see clearly. Pull over safely first.</li>
<li>Dry the mats and carpet; damp is the most common source after rain.</li>
<li>A fog that keeps returning, a wet floor or a musty smell means a workshop check.</li>
</ul></div>

<div class="cta-block">
  <h3>Windscreen keeps fogging up?</h3>
  <p>Edwin Garage is in Ang Mo Kio, serving Hougang, Yio Chu Kang, Serangoon and nearby areas. Inspections and repairs are by online appointment. WhatsApp 9785 6612 is for enquiries.</p>
  <a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a>
</div>
<div class="cluster-box"><h3>Related guides</h3><ul>
<li><a href="/articles/car-cabin-filter-replacement-singapore.html">Car Cabin Filter Replacement</a></li>
<li><a href="/articles/car-aircon-not-cold-singapore-causes-repair-options.html">Car Aircon Not Cold</a></li>
<li><a href="/articles/car-aircon-smell-solution-singapore.html">Car Aircon Smell</a></li>
<li><a href="/articles/water-under-car-aircon-or-leak-singapore.html">Water Under Car: Aircon or Leak</a></li>
<li><a href="/articles/car-wiper-streaks-singapore.html">Car Wiper Streaks</a></li>
<li><a href="/articles/car-aircon-blowing-warm-air-singapore.html">Car Aircon Blowing Warm Air</a></li>
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
