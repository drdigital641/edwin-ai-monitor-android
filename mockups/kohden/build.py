#!/usr/bin/env python3
"""KohDen International - Page One brand-site mockup.

Brand site (like the XADO one): builds trust in DENSO, EXN, MOON and Hyper Power parts
and sends drivers to authorised workshops; workshops buy trade from KohDen.
Product names, specs, list prices and images come from kohden.com.sg (WooCommerce store API,
read 3 Nov 2026). Images are linked from their uploads folder, nothing copied or altered.

Run: python3 build.py   -> ./site
"""
import html, json, os, shutil, hashlib
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")
BASE = "https://pageonesingapore.com/preview/kohden/"
U = "https://www.kohden.com.sg/wp-content/uploads/"
PHONE, TEL = "+65 6966 6565", "+6569666565"
WA = "6569666565"          # CONFIRM: is 6966 6565 on WhatsApp?
EMAIL = "kohden2019@yahoo.com"
ADDR = "7 Kaki Bukit Road 1, #01-15 Eunos Technolink, Singapore 415937"
MAPS = "https://www.google.com/maps?cid=4791073054792752607"
HOURS = "Mon to Fri, 9am to 5pm"

def img(p): return U + quote(p)

LOGO = img("2026/10/kohden_logo-v2.webp")
ICON = img("2026/10/cropped-kohden_logo-v2.webp")
BRANDS = {
 "denso": dict(name="DENSO", logo=img("2026/10/partner-logo-new-07-denso.webp"), page="denso.html",
   line="Spark plugs, filters, coolant and wipers from the Japanese maker of original-fit parts.",
   title="DENSO Parts Singapore | Spark Plugs, Filters, Wipers",
   desc="Genuine DENSO iridium spark plugs, air, cabin and oil filters, coolant and wipers in Singapore. List prices, sizes and where to get them fitted.",
   h1="Genuine DENSO parts in Singapore",
   lead="DENSO is a Japanese maker of original-equipment parts for many car brands. KohDen is an authorised DENSO distributor in Singapore and supplies these parts to workshops.",
   faq=[("Where can I get DENSO spark plugs fitted in Singapore?","At any workshop on our <a href=\"find-a-workshop.html\">authorised workshop list</a>. They buy direct from KohDen, so the parts are genuine."),
        ("How much do DENSO iridium spark plugs cost?","KohDen's list price is S$24 per plug for the Iridium Power range, S$22 to S$42 for Iridium SR and S$26 to S$36 for Iridium TT. Fitting is charged by the workshop."),
        ("How do I know my DENSO plugs are genuine?","Buy them from an authorised workshop and ask for the invoice. See our <a href=\"genuine-denso-spark-plugs.html\">guide to spotting fake spark plugs</a>.")]),
 "exn": dict(name="EXN", logo=img("2026/10/partner-logo-new-07-exn.webp"), page="exn.html",
   line="Engine oils, ATF and CVT fluids, brake fluid and engine treatments.",
   title="EXN Engine Oil Singapore | ATF, CVT Fluid, Additives",
   desc="EXN engine oils from 0W-16 hybrid to 5W-50, ATF and CVT fluids, DOT 4 and DOT 5.1 brake fluid and +Care treatments. List prices and authorised workshops.",
   h1="EXN oils and fluids in Singapore",
   lead="EXN makes engine oils, transmission fluids and +Care treatments for passenger cars. KohDen distributes the range to workshops across Singapore.",
   faq=[("Which EXN oil suits a hybrid?","EXN lists Extentios Hybrid 0W-16 (API SP) for hybrids. Always follow the grade in your owner's manual."),
        ("Is there a CVT fluid?","Yes, ATFIOS CVTF, fully synthetic, 4L, list price S$80. Ask the workshop to confirm it matches your gearbox."),
        ("Where can I get an EXN oil change?","At any workshop on our <a href=\"find-a-workshop.html\">authorised workshop list</a>.")]),
 "moon": dict(name="MOON", logo=img("2026/10/partner-logo-new-07-moon.webp"), page="moon.html",
   line="Silicone flat, hybrid and rear wiper blades, plus washer additive.",
   title="MOON Wiper Blades Singapore | Silicone Flat and Hybrid",
   desc="MOON silicone flat, hybrid and rear wiper blades and MWW-30 washer additive in Singapore. Sizes, list prices and workshops that fit them.",
   h1="MOON wiper blades in Singapore",
   lead="MOON makes silicone wiper blades in flat, hybrid and rear types. Singapore's heavy rain and strong sun wear blades fast, so most drivers change them once or twice a year.",
   faq=[("How often should I change wiper blades in Singapore?","When they streak, chatter or leave patches, often every 6 to 12 months in our sun and rain."),
        ("Flat or hybrid blade?","Flat blades sit low on curved screens; hybrid blades add a spoiler shape against wind lift. The workshop will match the fitting to your car."),
        ("What does the MWW-30 washer additive do?","MOON states it removes oil, soot and road film and is safe for paint, chrome, rubber and plastics.")]),
 "hyper-power": dict(name="Hyper Power", logo=img("2026/10/partner-logo-new-07-hyper-power.webp"), page="hyper-power.html",
   line="12V sodium-ion car batteries in JIS and DIN sizes, B20 to L6.",
   title="Hyper Power Sodium-Ion Car Battery Singapore | Sizes",
   desc="Hyper Power 12V sodium-ion car batteries in Singapore: JIS B20 to D31 and DIN L2 to L6, with cold cranking amps and sizes. Ask an authorised workshop.",
   h1="Hyper Power sodium-ion car batteries",
   lead="Hyper Power makes 12V car batteries with sodium-ion cells instead of lead-acid. KohDen carries 15 models in common JIS and DIN sizes.",
   faq=[("What is a sodium-ion car battery?","A 12V battery that uses sodium-ion cells in place of lead plates and acid. It fits the same tray sizes as the battery it replaces."),
        ("Which size fits my car?","Match the size code on your current battery (for example B24, D26 or L3). The workshop will confirm the terminal layout."),
        ("How much is a Hyper Power battery?","Prices depend on size. WhatsApp KohDen or ask an authorised workshop for a quote.")]),
}

# id, brand, group, name, lo, hi, image, spec   (lo=None: price on request)
P = [
 ("ik","denso","Spark plugs","Iridium Power IK series",24,0,"2026/04/DENSO-Iridium-Power-Spark-Plug-IK-series.jpg","ISO type, 14mm thread, 19mm reach. IK22 and above suit tuned engines."),
 ("ikh","denso","Spark plugs","Iridium Power IKH series",24,0,"2026/04/DENSO-Iridium-Power-Spark-Plug-IKH-series.jpg","14mm thread, 26.5mm long reach."),
 ("it","denso","Spark plugs","Iridium Power IT series",24,0,"2026/04/DENSO-Iridium-Power-Spark-Plug-IT-series.jpg","14mm tapered seat, 17.5mm reach."),
 ("itv","denso","Spark plugs","Iridium Power ITV series",24,0,"2026/04/DENSO-Iridium-Power-Spark-Plug-IT-series.jpg","14mm tapered seat, 25mm long reach."),
 ("ixu","denso","Spark plugs","Iridium Power IXU series",24,0,"2026/04/DENSO-Iridium-Power-Spark-Plug-IXU-series.jpg","12mm fully threaded, 19mm reach, projected insulator."),
 ("ixuh","denso","Spark plugs","Iridium Power IXUH series",24,0,"2026/04/DENSO-Iridium-Power-Spark-Plug-IXUH-series.jpg","12mm fully threaded, 26.5mm reach."),
 ("sr","denso","Spark plugs","Iridium SR",22,42,"2026/03/DENSO-Iridium-SR-Spark-Plug.jpg","Original-fit iridium plug for many Japanese and European cars."),
 ("tt","denso","Spark plugs","Iridium TT",26,36,"2026/03/DENSO-Iridium-TT-Spark-Plug.jpg","Iridium centre and platinum ground electrode, twin-tip design."),
 ("af","denso","Filters","COOL GEAR Air Filter",17,21,"2026/03/denso-air-filter.jpg","Engine air filter that stops dust reaching the engine."),
 ("caf","denso","Filters","COOL GEAR Cabin Air Filter",11,14,"2026/03/DENSO-Cabin-Air-Filter-03.jpg","Blocks dust, pollen and mould from the aircon air. Made in Korea."),
 ("of","denso","Filters","COOL GEAR Oil Filter",7,11,"2026/03/denso-oil-filter-02.jpg","Keeps metal particles and carbon out of the engine oil."),
 ("llc","denso","Coolant","Coolant LLC (green)",20,0,"2026/03/1565151518_LLC_Green2-02.jpg","Long-life coolant against overheating and corrosion."),
 ("sllc","denso","Coolant","Coolant SLLC (pink)",30,0,"2026/03/DENSO-Coolant-SLLC-Pink.jpg","Super long-life coolant."),
 ("rc","denso","Coolant","Radiator Cap",12,0,"","Holds cooling-system pressure; a worn cap can cause overheating."),
 ("ddp","denso","Wipers","Wiper Blade DDP",25,76,"2026/03/DENSO-DDP.jpg","Front wiper blade."),
 ("dcp","denso","Wipers","Wiper Blade DCP",13,22,"2026/03/DENSO-DCP.jpg","Front wiper blade."),
 ("dcs","denso","Wipers","Wiper Blade DCS",6,10,"2026/03/DENSO-DCS.jpg","Front wiper blade."),
 ("dra","denso","Wipers","Rear Wiper Blade DRA",18,22,"2026/03/DENSO-Rear-Wiper-Blade-DRA.jpg","Rear wiper blade."),
 ("drb","denso","Wipers","Rear Wiper Blade DRB",18,24,"2026/03/DENSO-Rear-Wiper-Blade-DRB.jpg","Rear wiper blade."),
 ("hyb","exn","Engine oil","Extentios Hybrid 0W-16, 4L",80,0,"2026/04/E2001-0W16P-4000-4L.jpg","Fully synthetic, API SP, for hybrids."),
 ("0w20","exn","Engine oil","Extentios Molyracing 0W-20",40,120,"2026/04/0W20P-4L.jpg","Fully synthetic esters. API SN/CF, ACEA A5/B5."),
 ("5w30m","exn","Engine oil","Extentios Molyracing 5W-30",40,120,"2026/04/5W30P-4L.jpg","API SN/CF, ACEA A3/B4, C3."),
 ("5w40","exn","Engine oil","Extentios Molyracing 5W-40",40,120,"2026/04/5W40P-4L.jpg","Fully synthetic. API SN/CF, ACEA A3/B4, C3."),
 ("5w50","exn","Engine oil","Extentios Molyracing 5W-50",40,120,"2026/04/5W50N-1L.jpg","Fully synthetic. API SN/CF, ACEA A3/B4, C3."),
 ("c5w30","exn","Engine oil","Carios Molytech Nano 5W-30, 4L",80,0,"2026/04/E3001-5W30P-4000.jpg","Semi-synthetic. API SN/CF, ACEA A3/B4."),
 ("c10w40","exn","Engine oil","Carios Molytech Nano 10W-40, 4L",80,0,"2026/03/E3002-10W40P-4000.jpg","Semi-synthetic. API SN/CF, ACEA A3/B4."),
 ("atf","exn","Gearbox and brakes","ATFIOS ATF, 4L",80,0,"2026/04/EXN-–-ATFIOS-ATF-–-FULLY-SYN-4L-E4001-ATMF-4000.jpg","Fully synthetic automatic transmission fluid."),
 ("cvtf","exn","Gearbox and brakes","ATFIOS CVTF, 4L",80,0,"2026/04/E4002-CVTF-4000-4L.jpg","Fully synthetic CVT fluid."),
 ("dot4","exn","Gearbox and brakes","Brake Fluid DOT 4, 1L",24,0,"2026/04/E5001-DOT4-1000-1L.jpg","+Care series."),
 ("dot51","exn","Gearbox and brakes","Brake Fluid DOT 5.1, 1L",30,0,"2026/04/E5002-DOT5-1000-1L.jpg","+Care series."),
 ("psf","exn","Gearbox and brakes","Power Steering Fluid, 1L",20,0,"2026/04/E5011-C_CARE-1000-1L.jpg","+Care series."),
 ("atfb","exn","Treatments","ATF Stop Leak + Treatment (blue)",30,0,"2026/04/EXN-–-ATF-STOP-LEAK-TREATMENT-BLUE-450ML-E4011-C.jpg","450ml, +Care series."),
 ("atfy","exn","Treatments","ATF Stop Leak, High Mileage (yellow)",30,0,"2026/04/EXN-–-ATF-STOP-LEAK-TREATMENT-HIGH-MILEAGE-YELLOW-450ML-E4012-C.jpg","450ml, +Care series."),
 ("cvtt","exn","Treatments","CVT Treatment",30,0,"2026/04/E4013-C_CARE-0450-0.45L.jpg","450ml, +Care series."),
 ("pic","exn","Treatments","Petrol Injector Cleaner",20,0,"2026/04/E6011-C_CARE-0350-0.35L.jpg","350ml, +Care series."),
 ("dic","exn","Treatments","Diesel Injector Cleaner",20,0,"2026/04/E6012-C_CARE-0350-0.35L.jpg","350ml, +Care series."),
 ("eop","exn","Treatments","Engine Optimizer Pro",20,0,"2026/04/E6013-C_CARE-0350-0.35L.jpg","350ml, +Care series."),
 ("eb","exn","Treatments","Engine Booster",20,0,"2026/04/E6014-C_CARE-350-0.35L.jpg","350ml, +Care series."),
 ("ef","exn","Treatments","Super Engine Flush",20,0,"2026/04/E6015-C_CARE-0450-0.45L.jpg","450ml, +Care series."),
 ("x40","exn","Treatments","X40 Ultra Lube Spray",20,0,"2026/04/E7011-C_CARE-0400-0.4L.jpg","400ml lubricant spray."),
 ("m1001","moon","Front blades","Silicone Hybrid Blade M1001",30,80,"2026/03/Hybrid-wiper-blade-Model-code-M1001.jpg","Streamlined shape against wind lift; less chatter."),
 ("m102","moon","Front blades","Silicone Flat Blade M-102",30,80,"2026/03/Flat-wiper-blade-Model-code-M102.jpg","Long-lasting silicone; quieter wiping; corrosion resistant."),
 ("m105","moon","Front blades","Silicone Japan Flat Blade M-105",30,0,"2026/03/MOON-Silicone-Japan-Flat-Blades.jpg","Flat blade for Japanese cars."),
 ("mgra","moon","Rear blades","Rear A-type Blade M-GRA",20,0,"2026/03/Regular-Rear-wiper-blade-Model-code-MGR.jpg","Original-style resin frame; easy to fit."),
 ("mgrb","moon","Rear blades","Rear B-type Blade M-GRB",20,0,"2026/03/Regular-Rear-wiper-blade-Model-code-MGR.jpg","Original-style resin frame; easy to fit."),
 ("mfr","moon","Rear blades","Rear Conti Blade M-FR",22,0,"2026/03/Flat-Rear-wiper-blade-Model-code-MFR.jpg","Flat rear blade."),
 ("mww","moon","Washer","Windshield Washer MWW-30",2,0,"2026/04/MOON-Windshield-Washer-MWW-30.jpg","Removes oil, soot and road film."),
]
BAT = [  # model, size, CCA, dims mm, image
 ("M42-36-S","B20 (ISS)",700,"194 x 126 x 200","2026/05/Hyper-Power-Battery-M42-36-S.jpg"),
 ("N55-45-S","B24",720,"236 x 128 x 200","2026/04/Hyper-Power-Battery-N55-45-S.jpg"),
 ("N55R-45-S","B24 (R)",720,"236 x 128 x 200","2026/04/Hyper-Power-Battery-N55-45-S.jpg"),
 ("Q85-60-S","D23",850,"230 x 172 x 203","2026/04/Hyper-Power-Battery-Q85-60-S.jpg"),
 ("Q85R-60-S","D23 (R)",850,"230 x 172 x 203","2026/04/Hyper-Power-Battery-Q85-60-S.jpg"),
 ("S95-70-S","D26",1000,"259 x 172 x 203","2026/04/Hyper-Power-Battery-S95-70-S.jpg"),
 ("S95R-70-S","D26 (R)",1000,"259 x 172 x 203","2026/04/Hyper-Power-Battery-S95-70-S.jpg"),
 ("T110-80-S","D31",1100,"305 x 172 x 203","2026/04/D31-T110-黑壳.jpg"),
 ("T110R-80-S","D31 (R)",1100,"305 x 172 x 203","2026/04/D31-T110-黑壳.jpg"),
 ("H5-60-S","L2 (DIN)",750,"245 x 175 x 189","2026/05/Hyper-Power-Battery-H5-60-S.jpg"),
 ("H6-60-S","L3 (DIN)",850,"280 x 175 x 189","2026/03/H6（蓝色）.jpg"),
 ("H6-70-S","L3 (DIN)",850,"280 x 175 x 189","2026/04/Hyper-Power-Battery-H6-70-S.jpg"),
 ("H7-80-S","L4 (DIN)",950,"315 x 175 x 189","2026/04/Hyper-Power-Battery-H7-80-S.jpg"),
 ("H8-92-S","L5 (DIN)",1050,"352 x 175 x 189","2026/04/Hyper-Power-Battery-H8-92-S.jpg"),
 ("H9-105-S","L6 (DIN)",1200,"395 x 175 x 189","2026/04/Hyper-Power-Battery-H8-92-S.jpg"),
]
for m, size, cca, dim, im in BAT:
    grp = "DIN sizes" if "DIN" in size else "JIS sizes"
    P.append(("hp-"+m.lower(), "hyper-power", grp, "Battery "+m, None, 0, im, f"12V sodium-ion, size {size}, {cca} CCA, {dim} mm."))

# Workshops that carry KohDen products. CONFIRM: list to come from KohDen / Edwin. Never invent.
DEALERS = []

e = html.escape
def price(lo, hi):
    if lo is None: return "Price on request"
    return f"S${lo}" if not hi else f"S${lo} to S${hi}"

def wa_link(text): return f"https://wa.me/{WA}?text=" + quote(text)

NAV = [("find-a-workshop.html","Find a workshop"),("genuine-denso-spark-plugs.html","Spot fake parts"),("denso.html","DENSO"),("exn.html","EXN"),("moon.html","MOON"),("hyper-power.html","Hyper Power"),("for-workshops.html","For workshops")]

def schema_org():
    return {"@context":"https://schema.org","@type":["Organization","AutoPartsStore"],"@id":BASE+"#org","name":"KohDen International Pte Ltd",
            "url":BASE,"logo":LOGO,"image":LOGO,"telephone":TEL,"email":EMAIL,"foundingDate":"2019",
            "description":"Authorised Singapore distributor of DENSO, EXN, MOON and Hyper Power car parts, supplying workshops since 2019.",
            "address":{"@type":"PostalAddress","streetAddress":"7 Kaki Bukit Road 1, #01-15 Eunos Technolink","postalCode":"415937","addressLocality":"Singapore","addressCountry":"SG"},
            "geo":{"@type":"GeoCoordinates","latitude":1.3347057,"longitude":103.9009866},"hasMap":MAPS,
            "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"17:00"}],
            "brand":[{"@type":"Brand","name":b["name"]} for b in BRANDS.values()],"sameAs":[MAPS]}

def faq_schema(faq):
    import re
    return {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub("<[^>]+>","",a)}} for q,a in faq]}

def crumbs_schema(items):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(items)]}

def page(fn, title, desc, body, schemas=(), crumbs=None, active=""):
    if crumbs:
        schemas = list(schemas) + [crumbs_schema([("Home","")] + crumbs)]
    lds = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in schemas)
    nav = "".join(f'<a href="{u}"{" aria-current=page" if u==active else ""}>{t}</a>' for u,t in NAV)
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs wrap" aria-label="Breadcrumb"><a href="index.html">Home</a>' + "".join(f' › <span>{e(n)}</span>' for n,u in crumbs) + '</nav>'
    url = BASE + ("" if fn=="index.html" else fn)
    doc = f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8"><script>document.documentElement.classList.add("js")</script>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{img('2026/10/DENSO-ThermalMaintenance23_final-2-scaled-1.webp')}">
<meta name="theme-color" content="#0c1a2b"><meta name="robots" content="max-image-preview:large">
<link rel="icon" href="{ICON}"><link rel="apple-touch-icon" href="{ICON}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/kd.css?v={VER['css']}">
{lds}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar">
<a class="logo" href="index.html" aria-label="KohDen home"><img src="{LOGO}" alt="KohDen International" width="150" height="34" referrerpolicy="no-referrer"></a>
<button class="burger" id="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button>
<nav id="nav">{nav}</nav>
</div></header>
<main id="main">{cr}{body}</main>
<footer class="foot"><div class="wrap fgrid">
<div><img class="flogo" src="{LOGO}" alt="KohDen International" width="150" height="34" referrerpolicy="no-referrer"><p>Authorised Singapore distributor of DENSO, EXN, MOON and Hyper Power car parts since 2019. We supply workshops; workshops fit the parts.</p></div>
<div><h4>For drivers</h4><a href="find-a-workshop.html">Find an authorised workshop</a><a href="genuine-denso-spark-plugs.html">Spot fake spark plugs</a>{"".join(f'<a href="{b["page"]}">{b["name"]}</a>' for b in BRANDS.values())}</div>
<div><h4>For workshops</h4><a href="for-workshops.html">Trade account and listing</a><a href="about.html">About KohDen</a><a href="tel:{TEL}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
<div><h4>Trade counter</h4><p>{ADDR}<br>{HOURS}</p><a href="{MAPS}" rel="noopener">Open in Google Maps</a></div>
</div><div class="wrap fine">© 2026 KohDen International Pte Ltd. Product details are the manufacturers' published specifications. List prices are KohDen's; workshop fitting is extra.</div></footer>
<a class="wa-float" href="{wa_link('Hi KohDen, I found you on your website. ')}" aria-label="WhatsApp KohDen">{WA_SVG}</a>
<script src="assets/kd.js?v={VER['js']}" defer></script>
</body></html>'''
    with open(os.path.join(OUT, fn), "w") as f: f.write(doc)
    SITEMAP.append(url)

WA_SVG = '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16.04 3C9.4 3 4 8.4 4 15.04c0 2.12.56 4.2 1.62 6.02L4 29l8.13-1.58a12 12 0 0 0 3.9.65C22.68 28.07 28 22.67 28 16.03 28 9.4 22.68 3 16.04 3zm0 22.1c-1.24 0-2.45-.22-3.6-.65l-.58-.22-4.82.94.97-4.7-.25-.6a9.9 9.9 0 0 1-.83-3.97c0-5.5 4.47-9.97 9.1-9.97 5.5 0 9.97 4.47 9.97 9.97 0 5.5-4.47 9.2-9.96 9.2zm5.46-7.45c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.26-.46-2.4-1.48-.89-.79-1.49-1.77-1.66-2.07-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.6-.92-2.2-.24-.57-.49-.5-.67-.5h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48 0 1.46 1.07 2.88 1.21 3.08.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.23 1.36.2 1.87.12.57-.08 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35z"/></svg>'

def card(p, link=True):
    pid, b, grp, name, lo, hi, im, spec = p
    brand = BRANDS[b]["name"]
    pic = f'<img src="{img(im)}" alt="{e(brand+" "+name)}" loading="lazy" referrerpolicy="no-referrer">' if im else f'<img class="lg" src="{BRANDS[b]["logo"]}" alt="{e(brand)}" loading="lazy" referrerpolicy="no-referrer">'
    return f'''<li class="pc"><div class="pimg">{pic}</div><div class="pbody"><span class="pb">{e(brand)}</span><h3>{e(name)}</h3><p>{e(spec)}</p><p class="price">{price(lo,hi)}<small>{"KohDen list price" if lo is not None else "Ask a workshop"}</small></p></div></li>'''

def dealer_block():
    if DEALERS:
        return ""  # filled when the list arrives
    return f'''<div class="dgrid">
<article class="dealer"><span class="tier">KohDen trade counter</span><h3>KohDen International</h3><p class="area">Kaki Bukit · East</p><p>{ADDR}</p><p class="who">{HOURS}. Parts supply and advice; fitting is done by workshops.</p>
<div class="dbtn"><a class="btn sm wa" href="{wa_link('Hi KohDen, which workshop near me can fit ')}">WhatsApp</a><a class="btn sm ghost" href="tel:{TEL}">Call</a><a class="btn sm ghost" href="{MAPS}" rel="noopener">Map</a></div></article>
<article class="dealer join"><span class="tier gold">Workshop owners</span><h3>Your workshop here</h3><p>Stock DENSO, EXN, MOON or Hyper Power and get listed on this finder, so drivers who want genuine parts find you.</p><div class="dbtn"><a class="btn sm" href="for-workshops.html">Get listed</a></div></article>
</div>'''

def write_assets():
    os.makedirs(os.path.join(OUT,"assets"), exist_ok=True)
    for n in ("kd.css","kd.js"):
        shutil.copy(os.path.join(HERE,n), os.path.join(OUT,"assets",n))
    # tap counter appended to the site script
    tap = open(os.path.join(HERE,"wa-tap-counter.js")).read().replace("'SLUG'","'kohden'")
    with open(os.path.join(OUT,"assets","kd.js"),"a") as f: f.write("\n"+tap)

def h(path):
    return hashlib.md5(open(os.path.join(HERE,path),"rb").read()).hexdigest()[:8]

VER = {}
SITEMAP = []

def build():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    VER["css"] = h("kd.css"); VER["js"] = h("kd.js")[:4] + h("wa-tap-counter.js")[:4]
    write_assets()
    org = schema_org()
    pop = [p for p in P if p[0] in ("ik","tt","caf","af","hyb","5w30m","cvtf","m1001","m102","hp-n55-45-s","hp-s95-70-s","llc")]

    # ---------------- home
    brands = "".join(f'''<a class="bc" href="{b["page"]}"><img src="{b["logo"]}" alt="{b["name"]}" loading="lazy" referrerpolicy="no-referrer"><span>{e(b["line"])}</span><b>See the range →</b></a>''' for b in BRANDS.values())
    home_faq = [("Does KohDen sell to the public?","KohDen supplies workshops. To buy and fit a part, go to an authorised workshop on our finder, or WhatsApp us and we will point you to one."),
                ("Are the parts genuine?","Yes. KohDen is an authorised distributor for DENSO, EXN, MOON and Hyper Power, so every part comes straight from the brand."),
                ("Can my own workshop order from KohDen?","Yes. Ask your mechanic to open a trade account with us, or send them our <a href=\"for-workshops.html\">workshop page</a>.")]
    body = f'''
<section class="hero"><div class="wrap hgrid">
<div class="htxt"><p class="kicker">Authorised distributor · Singapore since 2019</p>
<h1>Genuine DENSO, EXN, MOON and Hyper Power parts, fitted at a workshop near you</h1>
<p class="lead">KohDen brings these brands into Singapore and supplies them straight to workshops. Ask for them by name at your next service.</p>
<div class="hbtn"><a class="btn" href="find-a-workshop.html">Find an authorised workshop</a><a class="btn ghost" href="genuine-denso-spark-plugs.html">How to spot fake plugs</a></div></div>
<div class="hpics" aria-hidden="true">
<img class="p1" src="{img('2026/04/DENSO-Iridium-Power-Spark-Plug-IK-series.jpg')}" alt="" referrerpolicy="no-referrer">
<img class="p2" src="{img('2026/04/5W30P-4L.jpg')}" alt="" referrerpolicy="no-referrer">
<img class="p3" src="{img('2026/03/Hybrid-wiper-blade-Model-code-M1001.jpg')}" alt="" referrerpolicy="no-referrer">
<img class="p4" src="{img('2026/04/Hyper-Power-Battery-S95-70-S.jpg')}" alt="" referrerpolicy="no-referrer"></div>
</div></section>
<section class="logos"><div class="wrap lrow">{"".join(f'<a href="{b["page"]}"><img src="{b["logo"]}" alt="{b["name"]}" referrerpolicy="no-referrer"></a>' for b in BRANDS.values())}</div></section>
<section class="wrap sec rv"><div class="sh"><h2>Popular parts</h2><a href="denso.html">All brands →</a></div>
<div class="marq" id="marq"><ul class="track" id="track">{"".join(card(p) for p in pop)}</ul></div></section>
<section class="steps-band"><div class="wrap sec rv"><h2>How to get genuine parts</h2><ol class="steps">
<li><b>1</b><h3>Pick the part</h3><p>Browse the brand pages for sizes and list prices.</p></li>
<li><b>2</b><h3>Choose a workshop</h3><p>Every workshop on our finder buys direct from KohDen.</p></li>
<li><b>3</b><h3>Ask for it by name</h3><p>Say "DENSO Iridium" or "EXN 0W-20" and ask for the invoice.</p></li></ol>
<a class="btn" href="find-a-workshop.html">Find a workshop</a></div></section>
<section class="wrap sec rv"><h2>Four brands, one distributor</h2><div class="bgrid">{brands}</div></section>
<section class="alert rv"><div class="wrap split"><div><p class="kicker">Buyer warning</p><h2>Fake spark plugs are sold online in Singapore</h2><p>They can look like the real thing. Five quick checks, and where to buy plugs you can trust.</p><a class="btn" href="genuine-denso-spark-plugs.html">Read the 2-minute guide</a></div>
<img src="{img('2026/03/DENSO-Iridium-TT-Spark-Plug.jpg')}" alt="Genuine DENSO Iridium TT spark plug" loading="lazy" referrerpolicy="no-referrer"></div></section>
<section class="dark"><div class="wrap split rv"><div><p class="kicker">For workshop owners</p><h2>Stock the brands drivers ask for</h2><p>Trade prices, fast supply from Kaki Bukit, and a free listing on this workshop finder.</p><a class="btn" href="for-workshops.html">Open a trade account</a></div>
<ul class="ticks"><li>Authorised stock with invoices</li><li>DENSO, EXN, MOON and Hyper Power in one order</li><li>Listed on the KohDen workshop finder</li></ul></div></section>
<section class="wrap sec rv"><h2>Questions</h2>{faq_html(home_faq)}</section>'''
    page("index.html","KohDen | Genuine DENSO, EXN, MOON Parts Singapore",
         "Authorised Singapore distributor of DENSO spark plugs and filters, EXN oils, MOON wipers and Hyper Power batteries. Find a workshop that fits genuine parts.",
         body, [org, faq_schema(home_faq)])

    # ---------------- workshop finder
    body = f'''<header class="phero"><div class="wrap"><p class="kicker">Workshop finder</p><h1>Find a workshop with genuine KohDen parts</h1>
<p class="lead">These workshops buy DENSO, EXN, MOON and Hyper Power parts direct from KohDen. WhatsApp them, name the part, and ask for the invoice.</p></div></header>
<section class="wrap sec"><div class="filters" role="group" aria-label="Filter by area"><button class="on" data-f="All">All</button><button data-f="North">North</button><button data-f="East">East</button><button data-f="West">West</button><button data-f="Central">Central</button></div>
{dealer_block()}
<p class="note">Workshop list from KohDen International (2026). Many workshops work by appointment, so message ahead.</p></section>
<section class="dark"><div class="wrap split"><div><h2>Own a workshop?</h2><p>Get listed here and receive drivers who are already asking for genuine parts.</p><a class="btn" href="for-workshops.html">Get listed</a></div><ul class="ticks"><li>Free listing for trade customers</li><li>WhatsApp, call and map buttons</li><li>Linked from every brand page</li></ul></div></section>'''
    page("find-a-workshop.html","Find a Workshop for Genuine DENSO and EXN Parts | KohDen",
         "Workshops in Singapore that buy DENSO, EXN, MOON and Hyper Power parts direct from KohDen, the authorised distributor. WhatsApp, call or map.",
         body, [org], [("Find a workshop","find-a-workshop.html")], "find-a-workshop.html")

    # ---------------- fake spark plug guide
    gfaq = [("Are cheap DENSO spark plugs on marketplaces fake?","Not always, but you cannot check where they came from. KohDen's list price for Iridium Power is S$24 a plug; far below that is a warning sign."),
            ("What happens if I fit a fake spark plug?","Copies can misfire, foul or wear out early. A misfiring engine wastes fuel and can damage the catalytic converter, which costs far more than a set of plugs."),
            ("Where can I buy genuine DENSO spark plugs in Singapore?","From a workshop on our <a href=\"find-a-workshop.html\">authorised list</a>. They buy direct from KohDen, the authorised DENSO distributor."),
            ("Can KohDen check a plug I already bought?","WhatsApp us clear photos of the box and the plug markings and we will tell you what we can see.")]
    checks = [("Buy from an authorised channel","The only sure way. Authorised workshops buy from KohDen and can show you the invoice."),
              ("Check the price","Iridium Power lists at S$24 a plug, Iridium TT from S$26. A set of four at a fraction of that is a red flag."),
              ("Look at the box","Genuine boxes have sharp print, correct spelling and a part number that matches the plug. Blurred printing or a loose, unsealed box is a warning."),
              ("Look at the plug","Markings on the metal shell and insulator should be crisp and match the box. DENSO's iridium plugs have a very fine centre electrode, 0.4mm on Iridium Power."),
              ("Match the part number","Check the number against DENSO's application chart for your engine. A workshop can do this in seconds.")]
    body = f'''<header class="phero"><div class="wrap"><p class="kicker">Buyer guide · 2 min read</p><h1>How to buy genuine DENSO spark plugs in Singapore</h1>
<p class="lead">Fake spark plugs can look almost identical to the real thing. Here is how to tell, and where to buy plugs you can trust.</p></div></header>
<article class="wrap sec prose">
<div class="split top"><div><h2>Why it matters</h2><p>A spark plug fires thousands of times a minute. A poor copy can misfire or wear out early, and a misfiring engine wastes fuel and can damage the catalytic converter.</p></div>
<img class="framed" src="{img('2026/04/DENSO-Iridium-Power-Spark-Plug-IK-series.jpg')}" alt="Genuine DENSO Iridium Power spark plug" loading="lazy" referrerpolicy="no-referrer"></div>
<h2>5 checks before you buy</h2><ol class="checks">{"".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t,d in checks)}</ol>
<div class="cta-box"><h2>The easy way: buy from an authorised workshop</h2><p>Every workshop on our finder buys DENSO plugs direct from KohDen, the authorised distributor.</p><div class="hbtn"><a class="btn" href="find-a-workshop.html">Find a workshop</a><a class="btn ghost" href="denso.html#spark-plugs">See DENSO plug range</a></div></div>
<h2>Questions</h2>{faq_html(gfaq)}</article>'''
    art = {"@context":"https://schema.org","@type":"Article","headline":"How to buy genuine DENSO spark plugs in Singapore","datePublished":"2026-11-03","author":{"@id":BASE+"#org"},"publisher":{"@id":BASE+"#org"},"image":img("2026/04/DENSO-Iridium-Power-Spark-Plug-IK-series.jpg")}
    page("genuine-denso-spark-plugs.html","How to Spot Fake DENSO Spark Plugs in Singapore | KohDen",
         "Five checks to spot counterfeit DENSO spark plugs, list prices to compare, and authorised workshops in Singapore that sell genuine plugs.",
         body, [org, art, faq_schema(gfaq)], [("Spot fake spark plugs","genuine-denso-spark-plugs.html")], "genuine-denso-spark-plugs.html")

    # ---------------- brand pages
    for key, b in BRANDS.items():
        items = [p for p in P if p[1]==key]
        groups = []
        for p in items:
            if p[2] not in groups: groups.append(p[2])
        jump = "".join(f'<a href="#{slug(g)}">{e(g)}</a>' for g in groups)
        secs = "".join(f'<section class="wrap sec" id="{slug(g)}"><h2>{e(g)}</h2><ul class="pgrid">{"".join(card(p) for p in items if p[2]==g)}</ul></section>' for g in groups)
        prods = {"@context":"https://schema.org","@type":"ItemList","name":b["h1"],"itemListElement":[
            {"@type":"ListItem","position":i+1,"item":{"@type":"Product","name":f'{b["name"]} {p[3]}',"brand":{"@type":"Brand","name":b["name"]},"description":p[7],
             **({"image":img(p[6])} if p[6] else {}),
             **({"offers":{"@type":"Offer","priceCurrency":"SGD","price":p[4],"seller":{"@id":BASE+"#org"}}} if p[4] is not None and not p[5] else {}),
             **({"offers":{"@type":"AggregateOffer","priceCurrency":"SGD","lowPrice":p[4],"highPrice":p[5],"seller":{"@id":BASE+"#org"}}} if p[4] is not None and p[5] else {})}}
            for i,p in enumerate(items)]}
        extra = ""
        if key=="denso":
            extra = f'<section class="alert"><div class="wrap split"><div><h2>Worried about fake plugs?</h2><p>Five checks, and where to buy genuine DENSO in Singapore.</p><a class="btn" href="genuine-denso-spark-plugs.html">Read the guide</a></div></div></section>'
        body = f'''<header class="phero brandhero"><div class="wrap"><img class="blogo" src="{b["logo"]}" alt="{b["name"]}" referrerpolicy="no-referrer"><h1>{e(b["h1"])}</h1><p class="lead">{e(b["lead"])}</p>
<div class="hbtn"><a class="btn" href="find-a-workshop.html">Find a workshop</a><a class="btn ghost" href="{wa_link('Hi KohDen, I have a question about '+b['name']+' parts: ')}">Ask KohDen</a></div><nav class="jump">{jump}</nav></div></header>
{secs}{extra}<section class="wrap sec"><h2>{e(b["name"])} questions</h2>{faq_html(b["faq"])}</section>'''
        page(b["page"], b["title"], b["desc"], body, [org, prods, faq_schema(b["faq"])], [(b["name"], b["page"])], b["page"])

    # ---------------- for workshops
    wfaq = [("Who can open a trade account?","Any registered motor workshop in Singapore. WhatsApp us your company name and UEN."),
            ("How fast is supply?","Collect from our Kaki Bukit counter on weekdays, or ask us about delivery to your workshop."),
            ("How do I get listed on the finder?","Trade customers are listed free. Send your address, WhatsApp number and opening hours.")]
    body = f'''<header class="phero"><div class="wrap"><p class="kicker">For workshops</p><h1>Stock genuine DENSO, EXN, MOON and Hyper Power</h1>
<p class="lead">Open a KohDen trade account for trade prices, one supplier for four brands, and a free listing that sends drivers to you.</p>
<div class="hbtn"><a class="btn wa" href="{wa_link('Hi KohDen, I run a workshop and would like a trade account. Workshop name: ')}">WhatsApp for a trade account</a><a class="btn ghost" href="tel:{TEL}">Call {PHONE}</a></div></div></header>
<section class="wrap sec"><ul class="perks">
<li><h3>Trade prices</h3><p>Workshop pricing on all four brands. Ask us for the current trade list.</p></li>
<li><h3>Authorised stock</h3><p>Every part comes from the brand with an invoice, so you can show customers it is genuine.</p></li>
<li><h3>Listed on the finder</h3><p>Drivers who search for genuine parts are sent to the workshops on our list.</p></li>
<li><h3>Kaki Bukit counter</h3><p>Collect at Eunos Technolink, {HOURS}.</p></li></ul></section>
<section class="wrap sec"><h2>Questions</h2>{faq_html(wfaq)}</section>'''
    page("for-workshops.html","Trade Account for Workshops | DENSO, EXN Supplier Singapore",
         "Workshops in Singapore: open a KohDen trade account for DENSO, EXN, MOON and Hyper Power parts at trade prices, and get listed on our workshop finder.",
         body, [org, faq_schema(wfaq)], [("For workshops","for-workshops.html")], "for-workshops.html")

    # ---------------- about
    body = f'''<header class="phero"><div class="wrap"><p class="kicker">About</p><h1>About KohDen International</h1>
<p class="lead">Since 2019, KohDen has been an authorised Singapore distributor of car parts from brands workshops trust.</p></div></header>
<section class="wrap sec split top"><div class="prose"><p>We bring in DENSO maintenance and thermal parts, EXN oils and fluids, MOON wiper blades and Hyper Power sodium-ion batteries, and supply them to motor workshops across Singapore.</p>
<p>Drivers get genuine parts at a workshop they choose. Workshops get one reliable supplier for four brands.</p>
<h2>Visit or contact us</h2><ul class="contact"><li><b>Trade counter</b>{ADDR}</li><li><b>Hours</b>{HOURS}. Closed weekends and public holidays.</li><li><b>Phone</b><a href="tel:{TEL}">{PHONE}</a></li><li><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
<div class="hbtn"><a class="btn" href="{MAPS}" rel="noopener">Open in Google Maps</a><a class="btn ghost" href="find-a-workshop.html">Find a workshop</a></div></div>
<img class="framed" src="{img('2026/10/DENSO-ThermalMaintenance23_final-2-scaled-1-2.webp')}" alt="DENSO thermal and maintenance parts" loading="lazy" referrerpolicy="no-referrer"></section>'''
    page("about.html","About KohDen International | Car Parts Distributor Singapore",
         "KohDen International, Kaki Bukit: authorised Singapore distributor of DENSO, EXN, MOON and Hyper Power car parts since 2019. Address, hours and contact.",
         body, [org], [("About","about.html")], "about.html")

    # ---------------- 404, robots, sitemap, llms
    page("404.html","Page not found | KohDen","Page not found.",'<header class="phero"><div class="wrap"><h1>Page not found</h1><p class="lead">Try the <a href="find-a-workshop.html">workshop finder</a> or the <a href="index.html">home page</a>.</p></div></header>')
    SITEMAP.remove(BASE+"404.html")
    with open(os.path.join(OUT,"sitemap.xml"),"w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc><lastmod>2026-11-03</lastmod></url>\n" for u in SITEMAP) + "</urlset>\n")
    with open(os.path.join(OUT,"robots.txt"),"w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
    lines = [f"# KohDen International Pte Ltd", "", "> Authorised Singapore distributor (since 2019) of DENSO, EXN, MOON and Hyper Power car parts. Supplies motor workshops; drivers buy and fit through authorised workshops.", "",
             f"- Trade counter: {ADDR}. {HOURS}. Phone {PHONE}.", "", "## Pages"]
    lines += [f"- [{n}]({BASE}{u})" for u,n in [("find-a-workshop.html","Find an authorised workshop"),("genuine-denso-spark-plugs.html","How to spot fake DENSO spark plugs"),("denso.html","DENSO parts and list prices"),("exn.html","EXN oils and fluids"),("moon.html","MOON wiper blades"),("hyper-power.html","Hyper Power sodium-ion batteries"),("for-workshops.html","Trade accounts for workshops"),("about.html","About and contact")]]
    lines += ["", "## Key facts", "- DENSO Iridium Power spark plugs: S$24 each (KohDen list price). Iridium TT S$26 to S$36. Iridium SR S$22 to S$42.", "- EXN engine oils 4L: S$80 (Carios, Extentios Hybrid); Molyracing S$40 to S$120 by size.", "- MOON silicone flat and hybrid blades: S$30 to S$80.", "- Hyper Power 12V sodium-ion batteries: B20 to D31 and L2 to L6, 700 to 1200 CCA; price on request."]
    with open(os.path.join(OUT,"llms.txt"),"w") as f: f.write("\n".join(lines)+"\n")

def slug(s): return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-").replace("--","-")

def faq_html(faq):
    return '<div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{a}</p></details>" for q,a in faq) + "</div>"

if __name__ == "__main__":
    build()
    print("built", len(SITEMAP), "pages into", OUT)
