"""Build two static SG Garage aircon pages (3 Nov 2026).

Output: site/car-aircon-specialist-singapore/index.html
        site/car-aircon-compressor-replacement/index.html
Facts used are owner-confirmed only (see README.md). Run: python3 build.py
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")
TODAY = "2026-11-03"
BASE = "https://www.sggarage.com"
BOOK = "https://sggarageedwin.as.me/"
WA = "https://wa.me/6597856612"
OG = "https://i.ibb.co/qM3ZKCDy/edwin-garage-og-image.jpg"
OG_COMP = "https://i.ibb.co/Jjzw9Hw6/aircon-compressor-ready-stock.jpg"
UNIT = "Blk 5032 Ang Mo Kio Industrial Park 2 #01-309, Singapore 569535"

CSS = """*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:Inter,"Segoe UI","Helvetica Neue",Arial,sans-serif;color:#374151;line-height:1.65;background:#fff}h1,h2,h3{color:#111827;line-height:1.2;margin-top:0}h1{font-size:clamp(2rem,5vw,3.3rem);letter-spacing:-.04em;margin-bottom:20px}h2{font-size:clamp(1.55rem,3vw,2.2rem);letter-spacing:-.025em;margin-bottom:16px}h3{font-size:1.12rem;margin-bottom:8px}a{color:#2563EB}.site-header{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid #e5e7eb;box-shadow:0 1px 3px rgba(0,0,0,.08)}.nav-inner{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;align-items:center;height:64px;gap:32px}.nav-logo{font-weight:700;font-size:1.1rem;color:#111827;text-decoration:none}.nav-links{display:flex;list-style:none;gap:24px;margin:0;padding:0;flex:1}.nav-links a{color:#374151;text-decoration:none;font-size:.95rem;font-weight:500;transition:color .2s}.nav-links a:hover{color:#2563EB}.nav-cta{background:#2563EB;color:#fff;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:600;font-size:.9rem;white-space:nowrap}.nav-cta:hover,.btn:hover{background:#1d4ed8}.wrap{max-width:1100px;margin:auto;padding:0 24px}.crumbs{font-size:.85rem;color:#64748b;margin-bottom:14px}.crumbs a{color:#64748b;text-decoration:none}.hero{background:linear-gradient(135deg,#eff6ff,#fff 62%);padding:72px 0 60px}.hero .wrap>*{animation:rise .6s ease both}.hero .wrap>*:nth-child(2){animation-delay:.05s}.hero .wrap>*:nth-child(3){animation-delay:.1s}.hero .wrap>*:nth-child(4){animation-delay:.15s}.hero .wrap>*:nth-child(5){animation-delay:.2s}@keyframes rise{from{opacity:.001;transform:translateY(12px)}to{opacity:1;transform:none}}.eyebrow{font-weight:700;color:#2563EB;font-size:.9rem;text-transform:uppercase;letter-spacing:.08em}.lead{font-size:1.15rem;max-width:760px;margin:0 0 26px}.answer{background:#fff;border-left:4px solid #2563EB;border-radius:8px;padding:18px 22px;max-width:820px;box-shadow:0 2px 6px rgba(0,0,0,.05);margin:0 0 26px}.answer p{margin:0}.actions{display:flex;gap:12px;flex-wrap:wrap}.btn{display:inline-block;background:#2563EB;color:#fff;border-radius:8px;padding:13px 22px;text-decoration:none;font-weight:700;transition:background .2s,transform .2s}.btn:hover{transform:translateY(-1px)}.btn.alt{background:#fff;color:#1d4ed8;border:1px solid #2563EB}.btn.alt:hover{background:#eff6ff}.section{padding:60px 0}.alt{background:#f8fafc}.intro{max-width:780px;margin-bottom:26px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:22px;box-shadow:0 2px 5px rgba(0,0,0,.035);transition:transform .2s,box-shadow .2s}.card:hover{transform:translateY(-3px);box-shadow:0 8px 20px rgba(37,99,235,.10)}.card p{margin:0;font-size:.96rem}.card .price{display:inline-block;margin-top:10px;font-weight:700;color:#1d4ed8}.tbl{overflow-x:auto}.facts{width:100%;border-collapse:collapse;font-size:.97rem;background:#fff;border:1px solid #e5e7eb}.facts th,.facts td{padding:12px 16px;text-align:left;border-bottom:1px solid #e5e7eb;vertical-align:top}.facts thead th{background:#2563EB;color:#fff}.note{font-size:.88rem;color:#64748b;margin-top:12px}ol.steps{padding-left:22px;max-width:820px}ol.steps li{margin-bottom:10px}.faq{max-width:860px}.faq details{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:17px 20px;margin-bottom:12px}.faq summary{cursor:pointer;color:#111827;font-weight:700}.faq details p{margin:12px 0 0}.links{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px}.links a{display:block;padding:14px 16px;border:1px solid #e5e7eb;border-radius:10px;text-decoration:none;font-weight:600;transition:border-color .2s,background .2s}.links a:hover{border-color:#2563EB;background:#eff6ff}.cta-band{background:#1d4ed8;color:#fff;padding:52px 0}.cta-band h2,.cta-band p{color:#fff}.cta-band .btn{background:#fff;color:#1d4ed8}.cta-band .btn.alt{border-color:#bfdbfe;background:transparent;color:#fff}.footer{background:#111827;color:#9ca3af;padding:48px 24px 24px}.footer-inner{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;margin-bottom:32px}.footer-col strong{color:#fff;display:block;margin-bottom:12px;font-size:.95rem}.footer-col p,.footer-col li{font-size:.88rem;margin-bottom:8px}.footer-col ul{list-style:none;padding:0;margin:0}.footer-col a{color:#9ca3af;text-decoration:none}.footer-col a:hover{color:#fff}.footer-bottom{max-width:1200px;margin:0 auto;padding-top:24px;border-top:1px solid #374151;font-size:.82rem;text-align:center}@media(max-width:768px){.nav-links{display:none}.nav-inner{justify-content:space-between;padding:0 16px}.wrap{padding:0 16px}.hero{padding:52px 0 44px}.section{padding:46px 0}.grid{grid-template-columns:1fr}}@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important;scroll-behavior:auto!important}}"""

NAV = """<header class="site-header"><nav class="nav-inner"><a href="/" class="nav-logo">Edwin Garage</a><ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/car-servicing-repair/">Servicing &amp; Repair</a></li><li><a href="/car-aircon-repair/">Car Aircon</a></li><li><a href="/accident-claim-repair/">Accident Claim</a></li><li><a href="/prices/">Prices</a></li><li><a href="/about/">About</a></li><li><a href="/articles/">Articles</a></li></ul><a href="https://sggarageedwin.as.me/" class="nav-cta" target="_blank" rel="noopener">Book Now</a></nav></header>"""

FOOTER = """<footer class="footer"><div class="footer-inner"><div class="footer-col"><strong>Edwin Garage</strong><p>Main workshop: Blk 5032 Ang Mo Kio Industrial Park 2 #01-295, Singapore 569535</p><p>Aircon unit (SG Garage): #01-309, same address</p><p>Mon–Sat 10am–8pm | Closed Sundays</p></div><div class="footer-col"><strong>Aircon</strong><ul><li><a href="/car-aircon-specialist-singapore/">Car Aircon Specialist</a></li><li><a href="/car-aircon-compressor-replacement/">Compressor Replacement</a></li><li><a href="/car-aircon-repair/">Car Aircon Repair</a></li><li><a href="/prices/">Starting prices</a></li></ul></div><div class="footer-col"><strong>Contact</strong><p>By appointment only</p><p>Book: <a href="https://sggarageedwin.as.me/">sggarageedwin.as.me</a></p><p><a href="/about/">About Edwin Garage</a></p></div></div><div class="footer-bottom">© 2026 Edwin Garage Automotive Services Pte. Ltd. (UEN 201828727D). All rights reserved.</div></footer><script src="/p1-cta.js" defer></script>"""


def esc(s):
    return html.escape(s, quote=True)


def strip_tags(s):
    import re
    return re.sub(r"<[^>]+>", "", s)


def business_node():
    return {
        "@type": ["AutoRepair", "LocalBusiness"],
        "@id": BASE + "/#business",
        "name": "Edwin Garage Aircon & Car Repair",
        "legalName": "Edwin Garage Automotive Services Pte. Ltd.",
        "alternateName": ["SG Garage", "SGGarage", "Edwin Garage"],
        "url": BASE + "/",
        "telephone": "+6597856612",
        "foundingDate": "2010",
        "address": {"@type": "PostalAddress", "streetAddress": "Blk 5032 Ang Mo Kio Industrial Park 2 #01-295",
                    "addressLocality": "Ang Mo Kio", "addressRegion": "Singapore", "postalCode": "569535", "addressCountry": "SG"},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                                       "opens": "10:00", "closes": "20:00"}],
        "sameAs": ["https://share.google/hYkZhnKyoAEeERhWM", "https://www.facebook.com/edwingarageamk/",
                   "https://www.facebook.com/sggarageedwin/"],
    }


def offer(name, price, url):
    return {"@type": "Offer", "itemOffered": {"@type": "Service", "name": name, "url": url},
            "priceSpecification": {"@type": "PriceSpecification", "minPrice": price, "priceCurrency": "SGD",
                                   "valueAddedTaxIncluded": True}}


def page(p):
    url = BASE + p["path"]
    faq_ld = {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}} for q, a in p["faqs"]]}
    graph = [business_node(),
             {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["h1"], "description": p["desc"],
              "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "en-SG",
              "primaryImageOfPage": {"@type": "ImageObject", "url": p["og"]},
              "about": {"@id": BASE + "/#business"}},
             p["service_ld"],
             {"@type": "BreadcrumbList", "itemListElement": [
                 {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
                 {"@type": "ListItem", "position": 2, "name": "Car Aircon", "item": BASE + "/car-aircon-repair/"},
                 {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": url}]},
             faq_ld]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    faq_html = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in p["faqs"])
    head = (
        '<!doctype html><html lang="en-SG"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{esc(p["title"])}</title><meta name="description" content="{esc(p["desc"])}">'
        '<meta name="robots" content="index,follow,max-image-preview:large">'
        f'<link rel="canonical" href="{url}">'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="Edwin Garage">'
        f'<meta property="og:title" content="{esc(p["title"])}"><meta property="og:description" content="{esc(p["desc"])}">'
        f'<meta property="og:url" content="{url}"><meta property="og:image" content="{p["og"]}">'
        f'<meta property="og:image:alt" content="{esc(p["og_alt"])}"><meta property="og:locale" content="en_SG">'
        f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(p["title"])}">'
        f'<meta name="twitter:description" content="{esc(p["desc"])}"><meta name="twitter:image" content="{p["og"]}">'
        '<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">'
        '<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
        f'<style>{CSS}</style><script type="application/ld+json">{ld}</script></head>'
    )
    body = (
        f'<body>{NAV}<main><section class="hero"><div class="wrap">'
        f'<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › <a href="/car-aircon-repair/">Car Aircon</a> › {esc(p["crumb"])}</nav>'
        f'<p class="eyebrow">{p["eyebrow"]}</p><h1>{p["h1"]}</h1>'
        f'<div class="answer"><p><strong>Quick answer:</strong> {p["answer"]}</p></div>'
        f'<div class="actions"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book Online</a>'
        '</div><p class="note">By appointment only. Book your slot through the booking link above.</p>'
        f'</div></section>{p["body"]}'
        f'<section class="section alt"><div class="wrap"><h2>Frequently asked questions</h2><div class="faq">{faq_html}</div></div></section>'
        f'<section class="section"><div class="wrap"><h2>Related aircon pages and guides</h2><ul class="links">'
        + "".join(f'<li><a href="{h}">{esc(t)} →</a></li>' for h, t in p["related"]) +
        '</ul></div></section>'
        '<section class="cta-band"><div class="wrap"><h2>Book your aircon check</h2>'
        '<p>By appointment only, Monday to Saturday, 10am to 8pm. Book your slot through the link at sggarageedwin.as.me.</p>'
        f'<div class="actions"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book an appointment</a></div></div></section>'
        f'</main>{FOOTER}</body></html>\n'
    )
    return head + body


PRICE_NOTE = ("Starting prices include parts, labour and GST. The final price is confirmed after we inspect the car at your "
              "booked appointment, and no work starts until you approve it. Diagnosis is $30 if you don't go ahead with the repair.")

# ---------------------------------------------------------------- page 1
SPEC_FAQS = [
    ("Where is the SG Garage aircon unit?",
     "At Blk 5032 Ang Mo Kio Industrial Park 2 #01-309, Singapore 569535, on the ground floor of the same block as the Edwin Garage "
     "main workshop (#01-295). It is about 5 to 10 minutes from Ang Mo Kio MRT."),
    ("Does the #01-309 unit do other car repairs?",
     "No. The #01-309 unit does car aircon work only: gas top-up after a leak check, leak checks, compressor, cooling coil, condenser "
     "and aircon odour. Servicing, mechanical repair and accident claims are handled at the main workshop, #01-295."),
    ("How much is a car aircon gas top-up?",
     "From $20, after a leak check, including parts, labour and GST. If the system is leaking, we show you where and quote the repair "
     "before topping up, because gas added to a leaking system escapes again."),
    ("How much does a car aircon compressor or cooling coil cost?",
     'Compressor replacement starts from $550 and cooling coil replacement from $600, including parts, labour and GST. The final price '
     'depends on the car and is confirmed after inspection. See <a href="/car-aircon-compressor-replacement/">compressor replacement</a>.'),
    ("Do I need an appointment for aircon repair?",
     'Yes. Aircon work is by appointment only, booked through the link at <a href="https://sggarageedwin.as.me/">sggarageedwin.as.me</a>. '
     "We are open Monday to Saturday, 10am to 8pm, and closed on Sundays."),
    ("What makes a car aircon specialist different from a general workshop?",
     "A specialist tests the whole aircon system before changing parts: pressures on both sides, leak tracing, compressor clutch and "
     "electrical checks, and airflow. That finds the real cause, so you are not paying for repeated gas top-ups or the wrong part."),
]

SPEC_BODY = f"""
<section class="section"><div class="wrap"><h2>What is a car aircon specialist?</h2>
<p class="intro">A car aircon specialist is a workshop that diagnoses and repairs only car air-conditioning: refrigerant leaks, compressors, cooling coils (evaporators), condensers, fans and smells. The work starts with tests rather than a quick gas top-up, so the quote fixes the cause. SG Garage, our aircon unit at #01-309 in Ang Mo Kio Industrial Park 2, does aircon work only.</p>
<div class="grid">
<article class="card"><h3>Gas top-up</h3><p>Done after a leak check, so the gas stays in the system.</p><span class="price">From $20</span></article>
<article class="card"><h3>Leak check</h3><p>We trace where the refrigerant is escaping before recommending any repair.</p><span class="price">Part of the inspection</span></article>
<article class="card"><h3>Compressor</h3><p>Repair or replacement once tests confirm the compressor is the fault. <a href="/car-aircon-compressor-replacement/">Compressor replacement</a></p><span class="price">From $550</span></article>
<article class="card"><h3>Cooling coil</h3><p>Repair or replacement of a leaking or failed cooling coil behind the dashboard.</p><span class="price">From $600</span></article>
<article class="card"><h3>Condenser</h3><p>Condenser repair or replacement when it leaks or cannot release heat.</p><span class="price">Quoted after inspection</span></article>
<article class="card"><h3>Aircon odour</h3><p>Treatment for a musty or bad smell from the vents.</p><span class="price">Quoted after inspection</span></article>
</div><p class="note">{PRICE_NOTE}</p></div></section>

<section class="section alt"><div class="wrap"><h2>How do we diagnose a car aircon problem?</h2>
<p class="intro">We test before we quote. Most aircon complaints in Singapore (not cold, cold only when driving, warm at idle, a smell or a noise) can come from more than one part, so each check rules causes in or out.</p>
<ol class="steps">
<li><strong>Vent temperature and pressure check:</strong> gauges on the high and low sides show whether the system is low on gas, overcharged, blocked or not compressing.</li>
<li><strong>Leak tracing:</strong> if the pressure is low, we find where the gas escapes. Common points are hose joints, the compressor seal, the condenser and the cooling coil.</li>
<li><strong>Compressor and electrical check:</strong> clutch engagement, fuses, relays and pressure switches. An electrical fault can stop the compressor and look like a gas problem.</li>
<li><strong>Airflow check:</strong> blower, cabin filter, condenser fan and cooling coil, for weak airflow, poor cooling at idle or smells.</li>
<li><strong>Clear quote:</strong> we explain what we found and what to fix first. Nothing is done until you approve the price.</li>
</ol>
<p>More on this: <a href="/articles/car-aircon-pressure-test-mechanics-check-singapore.html">what a car aircon pressure test checks</a> and <a href="/articles/car-aircon-gas-leak-signs-causes-what-to-do.html">signs of an aircon gas leak</a>.</p>
</div></section>

<section class="section"><div class="wrap"><h2>How much does car aircon repair cost at SG Garage?</h2>
<p class="intro">These are starting prices from the owner, Edwin. They include parts, labour and GST.</p>
<div class="tbl"><table class="facts"><thead><tr><th>Aircon job</th><th>Starting price (SGD)</th></tr></thead><tbody>
<tr><td>Aircon gas top-up (after a leak check)</td><td><strong>From $20</strong></td></tr>
<tr><td>Cooling coil replacement</td><td><strong>From $600</strong></td></tr>
<tr><td><a href="/car-aircon-compressor-replacement/">Compressor replacement</a></td><td><strong>From $550</strong></td></tr>
<tr><td>Condenser, leak repair, odour treatment</td><td><strong>Quoted after inspection</strong></td></tr>
<tr><td>Diagnosis, if you don't go ahead with the repair</td><td><strong>$30</strong></td></tr>
</tbody></table></div>
<p class="note">{PRICE_NOTE} Full list: <a href="/prices/">Edwin Garage prices</a>.</p></div></section>

<section class="section alt"><div class="wrap"><h2>How to choose a car aircon specialist in Singapore</h2>
<p class="intro">Whichever workshop you use, these questions help you avoid paying twice for the same fault.</p>
<div class="grid">
<article class="card"><h3>Do they check for leaks first?</h3><p>A top-up without a leak check often means the cooling fades again within weeks.</p></article>
<article class="card"><h3>Do they show you the cause?</h3><p>Ask to see the gauge readings or the leak point before you approve a part.</p></article>
<article class="card"><h3>Are prices clear?</h3><p>Look for starting prices that include parts, labour and GST, with the final price agreed before work starts.</p></article>
<article class="card"><h3>New or remanufactured?</h3><p>For compressors, ask which option suits your car and why. <a href="/articles/remanufactured-vs-new-car-aircon-compressor-singapore.html">Remanufactured vs new</a></p></article>
<article class="card"><h3>Is the repair tested?</h3><p>The system should be pressure and vent-temperature tested again before you collect the car.</p></article>
<article class="card"><h3>Can you book a slot?</h3><p>An appointment means your car gets proper time for the checks.</p></article>
</div></div></section>

<section class="section"><div class="wrap"><h2>Where is SG Garage and when is it open?</h2>
<p class="intro">SG Garage, the aircon unit, is at <strong>{UNIT}</strong>, on the ground floor of the same block as the Edwin Garage main workshop (#01-295), about 5 to 10 minutes from Ang Mo Kio MRT. Open Monday to Saturday, 10am to 8pm; closed on Sundays. By appointment only: book your slot through the link at sggarageedwin.as.me. We serve drivers from Ang Mo Kio, Hougang, Yio Chu Kang, Serangoon, Bishan, Toa Payoh and the rest of Singapore.</p>
<p><a href="https://www.google.com/maps/search/?api=1&amp;query=5032%20Ang%20Mo%20Kio%20Industrial%20Park%202%20%2301-309%20Singapore%20569535" target="_blank" rel="noopener">Open in Google Maps</a> · <a href="/about/">About Edwin Garage</a></p>
</div></section>
"""

SPEC = dict(
    path="/car-aircon-specialist-singapore/",
    title="Car Aircon Specialist Singapore | SG Garage, Ang Mo Kio",
    desc="Aircon-only unit at #01-309 Ang Mo Kio: leak check, gas top-up from $20, compressor from $550, cooling coil, condenser, odour. By appointment only.",
    h1="Car aircon specialist in Singapore: aircon-only unit in Ang Mo Kio",
    crumb="Car Aircon Specialist",
    eyebrow="SG Garage · #01-309 Ang Mo Kio · Aircon only",
    answer=("SG Garage is the aircon-only unit of Edwin Garage, at #01-309 Ang Mo Kio Industrial Park 2. We check for leaks before "
            "any top-up, then repair the cause: gas top-up from $20, cooling coil from $600 and compressor from $550, including "
            "parts, labour and GST. The final price is confirmed after inspection. By appointment only, booked online."),
    og=OG, og_alt="Edwin Garage car aircon and repair workshop, Ang Mo Kio, Singapore",
    wa_text="Hi%20Edwin%2C%20I%27d%20like%20to%20ask%20about%20car%20aircon%20repair.",
    body=SPEC_BODY, faqs=SPEC_FAQS,
    service_ld={"@type": "Service", "@id": BASE + "/car-aircon-specialist-singapore/#service",
                "name": "Car aircon specialist repair", "serviceType": "Car air-conditioning repair",
                "description": "Car aircon diagnosis and repair at the SG Garage aircon unit, #01-309 Ang Mo Kio Industrial Park 2: gas top-up after a leak check, leak checks, compressor, cooling coil, condenser and odour.",
                "provider": {"@id": BASE + "/#business"}, "areaServed": {"@type": "Country", "name": "Singapore"},
                "url": BASE + "/car-aircon-specialist-singapore/",
                "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Car aircon starting prices", "itemListElement": [
                    offer("Car aircon gas top-up (after a leak check)", 20, BASE + "/car-aircon-specialist-singapore/"),
                    offer("Aircon cooling coil replacement", 600, BASE + "/car-aircon-specialist-singapore/"),
                    offer("Aircon compressor replacement", 550, BASE + "/car-aircon-compressor-replacement/")]}},
    related=[("/car-aircon-compressor-replacement/", "Car aircon compressor replacement"),
             ("/car-aircon-repair/", "Car aircon repair and servicing"),
             ("/articles/why-car-aircon-not-cold-singapore.html", "Why is my car aircon not cold?"),
             ("/articles/aircon-cooling-coil-replacement-singapore.html", "Cooling coil replacement"),
             ("/articles/car-aircon-condenser-what-it-does-cleaning-singapore.html", "What the aircon condenser does"),
             ("/articles/why-car-aircon-smells-and-how-to-fix-it.html", "Why car aircon smells")],
)

# ---------------------------------------------------------------- page 2
COMP_FAQS = [
    ("How much does car aircon compressor replacement cost in Singapore?",
     "At SG Garage, compressor replacement starts from $550, including parts, labour and GST. The final price depends on the car, the "
     "compressor type and what else the inspection finds, and is confirmed before any work starts."),
    ("How do I know if my aircon compressor is failing?",
     "Common signs are warm air from the vents, cooling that cuts in and out, a grinding or rattling noise when the aircon is on, and a "
     "compressor clutch that does not engage. A leak or an electrical fault can cause the same symptoms, so the system should be tested first."),
    ("Can a gas top-up fix a bad compressor?",
     "No. A top-up only replaces lost refrigerant. It does not repair a worn compressor, a faulty clutch or a wiring fault, and if the "
     "system leaks the gas escapes again."),
    ("Is a remanufactured compressor a good option?",
     'It can be, when the unit is the correct specification, properly rebuilt and tested. We remanufacture compressors in-house as a '
     'lower-cost option to new where it suits the car, and explain the choice before you decide. Read <a href="/articles/remanufactured-vs-new-car-aircon-compressor-singapore.html">remanufactured vs new compressors</a>.'),
    ("Can I keep driving with a noisy aircon compressor?",
     "Switch the aircon off and book an inspection soon. On many cars the compressor is driven by the engine belt, so a seizing "
     "compressor or pulley can damage the belt."),
    ("Is there a fee if I don't go ahead with the compressor replacement?",
     "Diagnosis is $30 if you decide not to go ahead with the repair. If you approve the work, you pay the agreed repair price."),
]

COMP_BODY = f"""
<section class="section"><div class="wrap"><h2>Signs your car aircon compressor is failing</h2>
<p class="intro">The compressor pumps refrigerant around the aircon system. When it weakens, cooling usually fades first in Singapore's stop-go traffic and midday heat.</p>
<div class="grid">
<article class="card"><h3>Warm air from the vents</h3><p>Cooling is weak or gone, even with the fan on high.</p></article>
<article class="card"><h3>Cooling cuts in and out</h3><p>Cold for a few minutes, then warm, then cold again.</p></article>
<article class="card"><h3>Noise when the aircon is on</h3><p>Grinding, rattling or squealing that stops when you switch the aircon off.</p></article>
<article class="card"><h3>Clutch not engaging</h3><p>On clutch-type compressors, the front plate does not spin when the aircon is switched on.</p></article>
<article class="card"><h3>Oil or leak marks</h3><p>Oily residue around the compressor body or its seals can point to a leak.</p></article>
<article class="card"><h3>Belt trouble</h3><p>A squealing or damaged drive belt can come from a compressor or pulley that is starting to seize.</p></article>
</div>
<p class="note">More detail: <a href="/articles/car-aircon-compressor-failure-warning-signs-repair-costs.html">compressor failure warning signs</a> and <a href="/articles/car-aircon-compressor-noise-singapore.html">compressor noise: repair or replace?</a></p>
</div></section>

<section class="section alt"><div class="wrap"><h2>Is it really the compressor?</h2>
<p class="intro">Several faults look like a dead compressor. We check these first, so you do not replace an $550 part when the cause is cheaper.</p>
<div class="tbl"><table class="facts"><thead><tr><th>Symptom</th><th>Could also be</th><th>What we check</th></tr></thead><tbody>
<tr><td>No cold air at all</td><td>Low gas from a leak, blown fuse or relay, faulty pressure switch</td><td>Pressures, leak trace, compressor power supply</td></tr>
<tr><td>Cold when driving, warm at idle</td><td>Weak condenser fan or blocked condenser</td><td>Fan operation, condenser airflow, pressures at idle</td></tr>
<tr><td>Noise with aircon on</td><td>Worn pulley bearing or drive belt</td><td>Pulley, belt and compressor with the aircon on and off</td></tr>
<tr><td>Cooling fades over weeks</td><td>Slow refrigerant leak (hoses, condenser, cooling coil)</td><td>Leak tracing before any top-up</td></tr>
</tbody></table></div></div></section>

<section class="section"><div class="wrap"><h2>How we replace a car aircon compressor</h2>
<ol class="steps">
<li><strong>Confirm the fault:</strong> pressure readings, clutch and electrical checks, and a leak trace, so the compressor is proven to be the cause.</li>
<li><strong>Agree the quote:</strong> we explain the options (new or remanufactured, where suitable) and the price. Nothing starts until you approve.</li>
<li><strong>Recover the refrigerant</strong> and remove the old compressor.</li>
<li><strong>Check for debris:</strong> a compressor that failed inside can send metal particles through the system, so we check whether other parts need cleaning or replacing and tell you before doing extra work.</li>
<li><strong>Fit the compressor</strong> with the correct oil, then vacuum the system and charge it with the correct refrigerant for your car (R134a or R1234yf).</li>
<li><strong>Test before handover:</strong> pressures, vent temperature and leak check, so you collect a car that cools properly.</li>
</ol></div></section>

<section class="section alt"><div class="wrap"><h2>New or remanufactured compressor?</h2>
<p class="intro">Both can be the right choice. A new compressor suits cars that need a specific updated unit or owners who plan to keep the car for many years. A remanufactured compressor is a used unit that has been stripped, rebuilt with worn parts replaced and tested, and is usually a lower-cost option. We remanufacture compressors in-house where it suits the car, and we tell you which option we recommend and why before you decide.</p>
<div class="tbl"><table class="facts"><thead><tr><th>Job</th><th>Starting price (SGD)</th></tr></thead><tbody>
<tr><td>Aircon compressor replacement</td><td><strong>From $550</strong></td></tr>
<tr><td>Aircon cooling coil replacement</td><td><strong>From $600</strong></td></tr>
<tr><td>Aircon gas top-up (after a leak check)</td><td><strong>From $20</strong></td></tr>
<tr><td>Diagnosis, if you don't go ahead with the repair</td><td><strong>$30</strong></td></tr>
</tbody></table></div>
<p class="note">{PRICE_NOTE}</p></div></section>

<section class="section"><div class="wrap"><h2>What changes the price of a compressor replacement?</h2>
<ul>
<li><strong>The car and compressor type:</strong> clutch, variable-displacement and electric compressors differ in part cost and fitting time.</li>
<li><strong>New or remanufactured:</strong> a remanufactured unit, where suitable, usually costs less than new.</li>
<li><strong>Access:</strong> some engine bays need more parts removed to reach the compressor.</li>
<li><strong>Damage elsewhere:</strong> if the old compressor sent debris through the system, other parts may need cleaning or replacing. We show you before quoting it.</li>
<li><strong>Refrigerant type:</strong> newer cars use R1234yf, older cars R134a.</li>
</ul>
<p>Compressor jobs are done at SG Garage, our aircon-only unit at {UNIT}. See <a href="/car-aircon-specialist-singapore/">car aircon specialist</a> for everything the unit handles.</p>
</div></section>
"""

COMP = dict(
    path="/car-aircon-compressor-replacement/",
    title="Car Aircon Compressor Replacement Singapore | SG Garage",
    desc="Car aircon compressor replacement in Ang Mo Kio from $550, incl. parts, labour and GST. Tested first, new or remanufactured. By appointment only.",
    h1="Car aircon compressor replacement in Singapore",
    crumb="Compressor Replacement",
    eyebrow="SG Garage · #01-309 Ang Mo Kio · Aircon only",
    answer=("Car aircon compressor replacement at SG Garage in Ang Mo Kio starts from $550, including parts, labour and GST. We "
            "first test pressures, the clutch and wiring, and trace leaks to confirm the compressor is the cause, then quote a new or "
            "remanufactured unit. By appointment only. The final price is confirmed after inspection; diagnosis is $30 if you don't go ahead."),
    og=OG_COMP, og_alt="Car aircon compressors at Edwin Garage, Ang Mo Kio, Singapore",
    wa_text="Hi%20Edwin%2C%20I%27d%20like%20to%20ask%20about%20aircon%20compressor%20replacement.",
    body=COMP_BODY, faqs=COMP_FAQS,
    service_ld={"@type": "Service", "@id": BASE + "/car-aircon-compressor-replacement/#service",
                "name": "Car aircon compressor replacement", "serviceType": "Car air-conditioning compressor replacement",
                "description": "Aircon compressor diagnosis and replacement (new or remanufactured where suitable) at the SG Garage aircon unit, #01-309 Ang Mo Kio Industrial Park 2.",
                "provider": {"@id": BASE + "/#business"}, "areaServed": {"@type": "Country", "name": "Singapore"},
                "url": BASE + "/car-aircon-compressor-replacement/",
                "offers": offer("Aircon compressor replacement", 550, BASE + "/car-aircon-compressor-replacement/")},
    related=[("/car-aircon-specialist-singapore/", "Car aircon specialist (SG Garage)"),
             ("/car-aircon-repair/", "Car aircon repair and servicing"),
             ("/articles/car-aircon-compressor-failure-warning-signs-repair-costs.html", "Compressor failure warning signs"),
             ("/articles/car-aircon-compressor-noise-singapore.html", "Compressor noise: repair or replace?"),
             ("/articles/remanufactured-vs-new-car-aircon-compressor-singapore.html", "Remanufactured vs new compressor"),
             ("/articles/car-aircon-pressure-test-mechanics-check-singapore.html", "Car aircon pressure test")],
)

if __name__ == "__main__":
    for p in (SPEC, COMP):
        d = os.path.join(OUT, p["path"].strip("/"))
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(p))
        print("built", p["path"])
