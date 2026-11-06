"""Build /articles/car-wont-start-mobile-battery-replacement-singapore.html for sggarage.com (7 Nov 2026).

Edwin approved the angle: Edwin Garage recommends Battery Rescue SG (batteryrescue.sg, by Motoserv) as its
preferred mobile battery replacement service. Allowed Battery Rescue facts only: Motoserv, Delkor batteries,
islandwide, fastest in the North and North-East, from $169.90 fitted, transparent prices with a price searcher
by car model, send your location on WhatsApp for an ETA. No warranty lengths, no outlet counts.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "car-wont-start-mobile-battery-replacement-singapore"
URL = f"https://www.sggarage.com/articles/{SLUG}.html"
PUB = "2026-11-07T07:45:00+08:00"
TITLE = "Car Won't Start in Singapore? Mobile Battery Replacement"
H1 = "Car Won't Start in Singapore? When to Call a Mobile Battery Replacement"
DESC = ("Car won't start in Singapore? How to tell if it's the battery, why onsite replacement saves a tow, and why "
        "Edwin Garage recommends Battery Rescue by Motoserv.")
OG = "https://i.ibb.co/qM3ZKCDy/edwin-garage-og-image.jpg"
BR = "https://batteryrescue.sg/?utm_source=edwingarage"
BR_PRICES = "https://batteryrescue.sg/?utm_source=edwingarage#compare"
BR_WA = "https://wa.me/6581259169"
BR_WA_TEXT = BR_WA + "?text=" + "Hi%20Battery%20Rescue%2C%20my%20car%20won%27t%20start.%20I%27ll%20send%20my%20location%20for%20an%20ETA.%20(From%20Edwin%20Garage%20website)"
WA_SVG = ('<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>')

FAQS = [
    ("How do I know if my car battery is flat?",
     "Common signs are a clicking sound or a slow, weak crank when you turn the key, dim or flickering dashboard lights, "
     "and the car being fine yesterday but dead this morning. If the lights are bright and the engine cranks normally but "
     "won't fire, the battery is less likely to be the cause."),
    ("Can a battery be replaced where my car is parked?",
     "Yes. A mobile battery service brings the correct battery to your car, at home, at the office or in a car park, and "
     "fits it on the spot. You don't need a tow truck or a jump-start to get to a workshop first."),
    ("Who does Edwin Garage recommend for mobile battery replacement?",
     "Edwin Garage recommends Battery Rescue SG (batteryrescue.sg), backed by Motoserv. They fit Delkor batteries "
     "islandwide and are fastest in the North and North-East of Singapore."),
    ("How much does onsite battery replacement cost with Battery Rescue?",
     "Battery Rescue prices start from $169.90 fitted. The price depends on the battery your car needs, and you can "
     "check it before you call with the price searcher on batteryrescue.sg by entering your car model."),
    ("How do I get help from Battery Rescue quickly?",
     "Send your location to Battery Rescue on WhatsApp at 8125 9169 and they will tell you the ETA. Including your car "
     "model helps them bring the right battery."),
    ("Should I keep jump-starting a weak battery?",
     "A jump-start gets you moving once, but a battery that keeps going flat usually needs replacing, or there may be a "
     "charging fault or a power drain. Repeated jump-starts on a dying battery often end with the car stuck again."),
]

ART = f"""
<p><strong>If your car won't start in Singapore and you hear clicking or a slow crank, the battery is the most likely cause. You don't have to tow the car to a workshop: a mobile battery service can test and replace the battery where the car is parked. For this, Edwin Garage recommends <a href="{BR}">Battery Rescue SG</a>, backed by Motoserv.</strong></p>
<p>We are Edwin Garage, a car workshop in Ang Mo Kio. A dead battery is one of the most common reasons drivers message us, usually from a car park first thing in the morning. This guide explains what to do in plain steps, how to tell whether the battery is the problem, and when getting it changed on the spot makes more sense than coming to us.</p>

<h2>What should you do first when your car won't start?</h2>
<p>Stay calm and check the simple things before calling anyone. Most no-starts are a flat battery, but a few minutes of checks can save you a wasted call.</p>
<ol>
<li><strong>Make sure the car is in Park (P) or Neutral</strong> and your foot is firmly on the brake (or clutch in a manual).</li>
<li><strong>Check the key.</strong> A weak key fob battery can stop push-start cars from starting. Hold the fob right against the start button and try again.</li>
<li><strong>Turn off the aircon, lights and radio,</strong> then try once more. Don't keep cranking for a long time: it drains what little power is left.</li>
<li><strong>Listen and look.</strong> Note whether you hear clicking, a slow crank or nothing at all, and whether the dashboard lights are bright or dim. This tells you a lot (see below).</li>
<li><strong>If you are on a road or expressway,</strong> switch on your hazard lights, get yourself to a safe place away from traffic, and only then call for help.</li>
</ol>

<h2>How can you tell it's the battery?</h2>
<p>You don't need tools to make a good guess. Compare what you notice with this table.</p>
<div class="tbl"><table class="art-tbl"><thead><tr><th>What you notice</th><th>Most likely cause</th></tr></thead><tbody>
<tr><td>Rapid clicking when you turn the key or press start</td><td>Flat or weak battery</td></tr>
<tr><td>Engine turns over slowly, "rur... rur..."</td><td>Weak battery, often worse in the morning</td></tr>
<tr><td>Dashboard lights dim, flicker or go out when you try to start</td><td>Flat battery or a loose battery terminal</td></tr>
<tr><td>Nothing at all: no lights, no sound</td><td>Completely dead battery or a disconnected terminal</td></tr>
<tr><td>Lights bright, engine cranks normally, but won't fire up</td><td>Probably not the battery: fuel, ignition or another fault</td></tr>
<tr><td>Battery warning light came on while driving, then the car died</td><td>Charging problem (often the alternator), not only the battery</td></tr>
</tbody></table></div>
<p>A battery that is a few years old, a car that has been parked for a week, or lights left on overnight all make a flat battery more likely. In Singapore's heat and stop-start traffic, batteries also tend to wear out without much warning. Our guide to <a href="/articles/car-wont-start-morning-battery-alternator-starter-singapore.html">battery, alternator or starter problems</a> goes into the less common causes.</p>

<h2>Why onsite battery replacement makes sense</h2>
<p>When the battery is the problem, the quickest fix is usually to bring a new battery to the car, not the car to a workshop. Here is why:</p>
<ul>
<li><strong>No tow truck.</strong> A car with a flat battery can't be driven, so getting it to a workshop means a tow or a jump-start first.</li>
<li><strong>Less waiting around.</strong> You stay where you are (home, office, shopping centre car park) while the battery is changed.</li>
<li><strong>The right battery, fitted properly.</strong> A proper mobile service checks which battery your car takes and fits it on the spot, instead of you buying one and guessing.</li>
<li><strong>A jump-start is only temporary.</strong> It gets you going once, but a worn-out battery will usually leave you stuck again.</li>
</ul>
<p>If your car still starts and you can drive it in, you can also have the battery checked at a workshop. See our <a href="/articles/battery-service-walk-in-ang-mo-kio.html">car battery replacement guide</a> for how we do it at Edwin Garage in Ang Mo Kio.</p>

<h2>Who Edwin Garage recommends: Battery Rescue SG</h2>
<p>For drivers who are stuck with a flat battery, Edwin Garage recommends <a href="{BR}">Battery Rescue SG</a> as our preferred mobile battery replacement service. It is backed by Motoserv. Here is what you should know:</p>
<ul>
<li><strong>Delkor batteries</strong> are the batteries they fit.</li>
<li><strong>Islandwide service,</strong> and they are <strong>fastest in the North and North-East</strong> of Singapore.</li>
<li><strong>From $169.90 fitted.</strong> The price depends on the battery your car takes.</li>
<li><strong>Transparent prices:</strong> you can look up the price for your car before calling, with the <a href="{BR_PRICES}">price searcher by car model</a>.</li>
<li><strong>Quick ETA:</strong> send your location on WhatsApp and they'll tell you when they can reach you.</li>
</ul>
<div class="br-box">
<h3>Stuck with a flat battery right now?</h3>
<p>Send your location and car model to Battery Rescue on WhatsApp for an ETA.</p>
<a class="btn-wa btn-br" href="{BR_WA_TEXT}" target="_blank" rel="noopener" data-ref="battery-rescue">{WA_SVG} <span>WhatsApp Battery Rescue <span style="white-space:nowrap">· 8125 9169</span></span></a>
<p class="br-note">Check your price first with the <a href="{BR_PRICES}">Battery Rescue price searcher</a>.</p>
</div>

<h2>What to send when you ask for help</h2>
<p>A clear message gets you help faster. On WhatsApp, send:</p>
<ol>
<li><strong>Your location</strong> (use WhatsApp's "Location" option, plus the car park level or lot number if you have it).</li>
<li><strong>Your car make, model and year,</strong> for example "Honda Vezel 2016", so the right battery is brought.</li>
<li><strong>What happened:</strong> clicking, slow crank or nothing at all, and whether any warning light came on.</li>
</ol>

<h2>How to make your next battery last</h2>
<ul>
<li>If you mostly do short trips, take the car for a longer drive now and then so the battery can recharge.</li>
<li>Check that lights, the boot light and accessories are off when you leave the car.</li>
<li>If the car is going to sit for more than a week or two, ask a workshop about keeping the battery charged.</li>
<li>Have the battery and charging system tested at your regular servicing. Our <a href="/articles/car-battery-drains-overnight-singapore.html">battery draining overnight guide</a> covers what to check if it keeps going flat.</li>
</ul>

<h2>Frequently asked questions</h2>
""" + "".join(f"<h3>{html.escape(q)}</h3>\n<p>{html.escape(a)}</p>\n" for q, a in FAQS) + """
<div class="takeaways-box"><h3>Key Takeaways</h3><ul>
<li>Clicking, a slow crank or dim dashboard lights usually mean a flat or weak battery.</li>
<li>If the lights are bright and the engine cranks normally but won't fire, look beyond the battery.</li>
<li>Onsite battery replacement saves a tow: the new battery is fitted where the car is parked.</li>
<li>Edwin Garage recommends Battery Rescue SG, backed by Motoserv, for mobile battery replacement: Delkor batteries, islandwide, from $169.90 fitted.</li>
</ul></div>
"""

ld_faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}
ld_graph = {"@context": "https://schema.org", "@graph": [
    {"@type": ["AutoRepair", "LocalBusiness"], "@id": "https://www.sggarage.com/#business", "name": "Edwin Garage Aircon & Car Repair",
     "url": "https://www.sggarage.com", "telephone": "+6597856612",
     "address": {"@type": "PostalAddress", "streetAddress": "Blk 5032 Ang Mo Kio Industrial Park 2 #01-295", "addressLocality": "Ang Mo Kio",
                 "addressRegion": "Singapore", "postalCode": "569535", "addressCountry": "SG"},
     "geo": {"@type": "GeoCoordinates", "latitude": 1.3721, "longitude": 103.8458},
     "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "10:00", "closes": "20:00"}],
     "sameAs": ["https://share.google/hYkZhnKyoAEeERhWM", "https://www.facebook.com/edwingarageamk/", "https://www.facebook.com/sggarageedwin/"]},
    {"@type": "Article", "@id": URL + "#article", "headline": H1, "description": DESC,
     "image": {"@type": "ImageObject", "url": OG}, "datePublished": PUB, "dateModified": PUB,
     "author": {"@type": "Person", "name": "Edwin", "jobTitle": "Master Automotive Technician", "worksFor": {"@id": "https://www.sggarage.com/#business"}},
     "publisher": {"@id": "https://www.sggarage.com/#business"}, "mainEntityOfPage": {"@type": "WebPage", "@id": URL},
     "articleSection": "Battery", "inLanguage": "en-SG", "about": {"@id": "https://www.sggarage.com/#business"},
     "mentions": [{"@type": "Organization", "name": "Battery Rescue SG", "url": "https://batteryrescue.sg/"},
                  {"@type": "Organization", "name": "Motoserv"}],
     "keywords": "car won't start Singapore, mobile battery replacement Singapore, onsite car battery replacement, flat car battery, Battery Rescue SG, Motoserv"},
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.sggarage.com"},
        {"@type": "ListItem", "position": 2, "name": "Car Guides", "item": "https://www.sggarage.com/articles/"},
        {"@type": "ListItem", "position": 3, "name": H1, "item": URL}]},
    {"@type": "WebPage", "@id": URL, "url": URL, "name": TITLE, "datePublished": PUB, "dateModified": PUB,
     "speakable": {"@type": "SpeakableSpecification", "cssSelector": [".article h2", ".article p"]}}]}

CSS = """*{box-sizing:border-box;margin:0;padding:0}
:root{--accent:#2563EB;--hover:#1D4ED8;--bg:#FAFAF8;--text:#1A1A1A;--body:#374151;--muted:#6B7280;--border:#E5E7EB;--heading-font:'Playfair Display',Georgia,'Times New Roman',serif;--body-font:'Inter','Segoe UI','Helvetica Neue',sans-serif}
body{font-family:var(--body-font);background:var(--bg);color:var(--body);line-height:1.8;font-size:17px}
.site-header{background:#fff;border-bottom:1px solid var(--border);padding:0 20px;display:flex;align-items:center;justify-content:space-between;min-height:60px;position:sticky;top:0;z-index:900;flex-wrap:wrap}
.logo{color:var(--text);text-decoration:none;font-size:17px;font-weight:800;letter-spacing:-.3px;white-space:nowrap}.logo span{color:var(--accent)}
.hnav{display:flex;align-items:center;gap:8px}
.hnav .nl{color:var(--body);text-decoration:none;font-size:.85rem;font-weight:500;padding:6px 10px;border-radius:6px;transition:color .2s,background .2s;white-space:nowrap}
.hnav .nl:hover,.hnav .nl.active{color:var(--accent);background:#EFF6FF}
.btn-book-sm{background:var(--accent);color:#fff;text-decoration:none;padding:7px 14px;border-radius:20px;font-size:.8rem;font-weight:700;white-space:nowrap;transition:background .15s}.btn-book-sm:hover{background:var(--hover)}
.hamburger{display:none;flex-direction:column;justify-content:center;gap:5px;background:none;border:none;cursor:pointer;padding:8px}
.hamburger span{display:block;width:24px;height:2px;background:var(--accent);border-radius:2px}
@media(max-width:768px){.hamburger{display:flex}.hnav{display:none;flex-direction:column;align-items:stretch;width:100%;background:#fff;border-top:1px solid var(--border);padding:12px 0;gap:4px;order:3}.hnav.open{display:flex}.hnav .nl{font-size:.9rem;padding:10px 16px;border-radius:0;border-bottom:1px solid var(--border)}.btn-book-sm{margin:6px 16px;border-radius:8px;padding:10px 16px;font-size:.9rem}}
.art-header{background:#fff;border-bottom:1px solid var(--border);padding:40px 24px 36px}.art-header-inner{max-width:820px;margin:0 auto}
.breadcrumb{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font-size:13px;color:var(--muted);margin-bottom:20px}.breadcrumb a{color:var(--muted);text-decoration:none}.breadcrumb .sep{color:var(--border)}
.art-category{font-size:11px;font-weight:700;letter-spacing:2.5px;text-transform:uppercase;color:var(--accent);margin-bottom:18px}
.art-header h1{font-family:var(--heading-font);font-size:clamp(26px,5vw,44px);font-weight:800;color:var(--text);line-height:1.2;margin-bottom:20px}
.art-byline{font-size:13px;color:var(--muted);display:flex;flex-wrap:wrap;gap:6px;align-items:center}.art-byline .sep{color:var(--border)}.art-byline strong{color:var(--body)}
.article-wrap{max-width:820px;margin:0 auto;padding:44px 24px 60px}
.article h2{font-family:var(--heading-font);font-size:clamp(20px,3vw,26px);font-weight:700;color:var(--text);margin:48px 0 16px;line-height:1.3}
.article h3{font-size:17px;font-weight:700;color:var(--text);margin:28px 0 10px}
.article p{font-size:17px;line-height:1.8;margin-bottom:20px}
.article ul,.article ol{margin:4px 0 20px 24px}.article li{margin-bottom:8px;font-size:17px;line-height:1.7}
.article a{color:var(--accent);text-decoration:underline;text-underline-offset:3px}.article a:hover{color:var(--hover)}
.tbl{overflow-x:auto;margin:8px 0 24px}.art-tbl{width:100%;border-collapse:collapse;background:#fff;font-size:15px;border:1px solid var(--border)}.art-tbl th,.art-tbl td{padding:10px 14px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top}.art-tbl th{background:#EFF6FF;color:#1E3A8A}
.br-box{background:#F0FDF4;border:1px solid #BBF7D0;border-radius:14px;padding:26px 28px;margin:32px 0;text-align:center}
.br-box h3{font-family:var(--heading-font);font-size:21px;margin:0 0 8px}.br-box p{margin-bottom:16px}.br-box .br-note{font-size:14px;color:var(--muted);margin:14px 0 0}
.btn-wa{display:inline-flex;align-items:center;gap:8px;background:#25d366;color:#064e3b;text-decoration:none;padding:13px 24px;border-radius:30px;font-size:16px;font-weight:700;transition:background .2s,transform .2s}
.article .btn-wa{color:#064e3b;text-decoration:none}.btn-wa:hover{background:#1ebe5b;transform:translateY(-1px)}
.btn-book{display:inline-flex;align-items:center;background:var(--accent);color:#fff;text-decoration:none;padding:13px 26px;border-radius:30px;font-size:16px;font-weight:700;margin:6px}.article .btn-book{color:#fff;text-decoration:none}
.takeaways-box{background:#EFF6FF;border:1px solid #BFDBFE;border-radius:14px;padding:30px 34px;margin:52px 0 40px}
.takeaways-box h3{font-family:var(--heading-font);font-size:21px;color:#1E40AF;margin:0 0 18px}.takeaways-box ul{list-style:none;padding:0;margin:0}
.takeaways-box li{padding:7px 0 7px 26px;position:relative;color:#1E3A8A;font-size:16px;line-height:1.6}.takeaways-box li::before{content:'—';position:absolute;left:0;color:#3B82F6;font-weight:700}
.cluster-box{background:#fff;border:1px solid var(--border);border-radius:12px;padding:28px 32px;margin:44px 0}
.cluster-box h3{font-size:15px;font-weight:700;color:var(--text);margin:0 0 14px;text-transform:uppercase;letter-spacing:.5px}
.cluster-box ul{list-style:none;padding:0;margin:0}.cluster-box li{border-bottom:1px solid var(--border);padding:9px 0}.cluster-box li:last-child{border-bottom:none}
.cluster-box a{color:var(--accent);text-decoration:none;font-size:15px;font-weight:500}
.cta-block{background:#fff;border:1px solid var(--border);border-radius:14px;padding:32px;margin:44px 0;text-align:center}
.cta-block h3{font-family:var(--heading-font);font-size:22px;margin:0 0 10px}.cta-block p{color:var(--muted);font-size:16px;margin-bottom:18px}
.footer{background:#fff;border-top:1px solid var(--border);padding:40px 24px;margin-top:60px}
.footer-inner{max-width:1200px;margin:0 auto;display:flex;flex-wrap:wrap;gap:32px;justify-content:space-between}
.footer-brand p{color:var(--muted);font-size:14px;margin-top:8px;max-width:280px;line-height:1.6}
.footer-links h4{font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text);margin-bottom:12px}
.footer-links ul{list-style:none}.footer-links li{margin-bottom:8px;font-size:14px;color:var(--muted)}.footer-links a{color:var(--muted);text-decoration:none;font-size:14px}
.footer-bottom{border-top:1px solid var(--border);margin-top:32px;padding-top:20px;text-align:center;color:var(--muted);font-size:13px}
@media(max-width:480px){.article-wrap{padding:32px 16px 48px}.art-header{padding:32px 16px 28px}.br-box{padding:22px 16px}.btn-wa{padding:12px 16px;font-size:15px}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}"""


def build():
    e = html.escape
    head = f"""<!DOCTYPE html>
<html lang="en-SG">
<head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(TITLE)}</title>
<meta name="description" content="{e(DESC)}">
<meta property="og:title" content="{e(TITLE)}">
<meta property="og:description" content="{e(DESC)}">
<meta property="og:image" content="{OG}"><meta property="og:type" content="article">
<meta property="og:url" content="{URL}">
<meta property="og:locale" content="en_SG"><meta property="og:site_name" content="Edwin Garage Singapore">
<meta property="article:published_time" content="{PUB}"><meta property="article:modified_time" content="{PUB}">
<meta property="article:section" content="Battery">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(TITLE)}">
<meta name="twitter:description" content="{e(DESC)}"><meta name="twitter:image" content="{OG}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{URL}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_graph, ensure_ascii=False)}</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
<style>
{CSS}
</style>
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
  <div class="art-category">Battery</div>
  <h1>{e(H1)}</h1>
  <div class="art-byline"><strong>Edwin</strong><span class="sep">·</span><span>Master Automotive Technician</span><span class="sep">·</span><span>November 7, 2026</span><span class="sep">·</span><span>Edwin Garage, Ang Mo Kio</span></div>
</div></div>
<div class="article-wrap"><article class="article">
"""
    tail = """
<div class="cta-block">
  <h3>Car starts, but the battery feels weak?</h3>
  <p>Edwin Garage is in Ang Mo Kio, serving Hougang, Yio Chu Kang, Serangoon and nearby areas. Servicing and repairs are by appointment.</p>
  <a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a>
</div>
<div class="cluster-box"><h3>More on car batteries</h3><ul>
<li><a href="/articles/car-wont-start-morning-battery-alternator-starter-singapore.html">Car Won't Start in the Morning: Battery, Alternator or Starter?</a></li>
<li><a href="/articles/battery-service-walk-in-ang-mo-kio.html">Car Battery Replacement at Edwin Garage, Ang Mo Kio</a></li>
<li><a href="/articles/car-battery-drains-overnight-singapore.html">Car Battery Drains Overnight in Singapore: What to Check</a></li>
<li><a href="/articles/alternator-failure-signs-car-battery-dying.html">Alternator Failure Signs: Is It the Battery or the Alternator?</a></li>
</ul></div>
</article></div>
<footer class="footer"><div class="footer-inner">
  <div class="footer-brand"><a class="logo" href="/"><span>Edwin</span> Garage</a><p>Car workshop in Ang Mo Kio since 2010. Servicing, repairs, aircon and accident claims.</p></div>
  <div class="footer-links"><h4>Services</h4><ul><li><a href="/car-servicing-repair/">Car Servicing &amp; Repair</a></li><li><a href="/car-aircon-repair/">Car Aircon Repair</a></li><li><a href="/accident-claim-repair/">Accident &amp; Dent Repair</a></li><li><a href="/prices/">Starting prices</a></li></ul></div>
  <div class="footer-links"><h4>Visit Us</h4><ul><li>Blk 5032 Ang Mo Kio Industrial Park 2 #01-295, Singapore 569535</li><li>Mon–Sat: 10am – 8pm · Closed Sundays</li><li><a href="https://wa.me/6597856612" target="_blank" rel="noopener">WhatsApp: 9785 6612</a> (enquiries)</li></ul></div>
  <div class="footer-links"><h4>Quick Links</h4><ul><li><a href="/articles/">Car Guides &amp; Articles</a></li><li><a href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a></li><li><a href="/about/">About Edwin Garage</a></li></ul></div>
</div><div class="footer-bottom"><p>© 2026 Edwin Garage Automotive Services Pte. Ltd. (UEN 201828727D) · Blk 5032 Ang Mo Kio Industrial Park 2 #01-295 · Singapore 569535</p></div></footer>
<script src="/p1-cta.js" defer></script>
</body>
</html>
"""
    out = os.path.join(HERE, "site", "articles")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, SLUG + ".html"), "w", encoding="utf-8") as f:
        f.write(head + ART + tail)
    print("built", URL)


if __name__ == "__main__":
    build()
