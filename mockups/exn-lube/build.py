#!/usr/bin/env python3
"""EXN Lube - Page One rebuild of exnlube.com (preview).

Why: the current exnlube.com is a Create React App shell. Google, Bing and AI fetchers get a
267-character page titled "Exnlube" for every URL, no sitemap, no text, no schema.
This build is plain static HTML: every page has its own title, answer-first text, schema and
is listed in the sitemap.

Facts only from: EXN corporate deck (Messe Frankfurt download, 2025), EXN exhibitor listing
(Automechanika Dubai), EXN YouTube "about", exnlube.com meta + asset list, and the product
labels/specs listed by EXN's Singapore distributor KohDen (kohden.com.sg, read 3 Nov 2026).
Nothing invented. Open items are in OPEN below and in /mnt/project-files/exn-lube/README.md.

Header, nav and footer live ONLY in shell() (MASTER-RULES 2.11): one edit changes every page.

Run: python3 build.py   -> ./site   (preview: pageonesingapore.com/preview/exn-lube/)
"""
import html, json, os, shutil, hashlib, glob
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")
SITE = "https://exnlube.com/"          # canonical = the real domain (go-live edits nothing)
TODAY = "2026-11-08"

BRAND = "EXN Lube"
LEGAL = "EXN Lube Marketing Sdn. Bhd."
REG = "201201003247 (976772-K)"
PHONE, TEL = "+60 3-7733 8313", "+60377338313"
FAX = "+60 3-7733 6208"
EMAIL = "marketing@exnlube.com"
STREET = "Lot W3A06-A07, Level 3A, Metropolitan Square, Jalan PJU 8/1, Damansara Perdana"
CITY, POST, REGION = "Petaling Jaya", "47820", "Selangor"
ADDR = f"{STREET}, {POST} {CITY}, {REGION}, Malaysia"
WA = ""   # OPEN: EXN's WhatsApp number (their site shows a WhatsApp icon). Empty = call/email CTAs only.
MAPS = "https://www.google.com/maps/search/?api=1&query=" + quote("EXN Lube Marketing Sdn Bhd Metropolitan Square Damansara Perdana")
SOCIAL = {
    "YouTube": "https://www.youtube.com/@exnlube.official",
    "Instagram": "https://www.instagram.com/exnlube.official/",
    "TikTok": "https://www.tiktok.com/@exnlube.official",
}

E = "https://exnlube.com/static/media/"
def ex(name): return E + quote(name)
K = "https://www.kohden.com.sg/wp-content/uploads/"
def kd(p): return K + quote(p)

LOGO = ex("EXN LOGO BLACK-01-01.4e598f95512d0f60bfa9.png")
LOGO_W = ex("EXN LOGO WHITE-01-01.331823519af95aae4b41.png")
ICON = "https://exnlube.com/exnlube192.png"
HERO = ex("EXN WEBSITE - BANNER 01.212cd9602db2172415cd.jpg")
HERO2 = ex("EXN WEBSITE - BANNER 02.4dfaa53332de7778530f.jpg")
HERO3 = ex("EXN WEBSITE - BANNER 03.e46cbc3446d631e26be5.jpg")
MOLY = ex("molytech_big.288c9403d1bc153587ff.png")
COMPANY = ex("company_photo.b91fadc2cefd1cfe51cf.png")
COMM = [ex(f"Community-2024-(o)-0{i}.{h}.jpg") for i, h in
        [(2, "dd165d0358a437484f95"), (3, "e59deb3bdd278c463bdd"), (4, "bdacb6930c0ef95873fa"),
         (5, "e6cb68078de1c951ae51"), (6, "1d9c123fc7ee4c7afbc7")]]
CAT_ICON = {
    "passenger-car-engine-oil": ex("1. CAR-10.54891bf785959f4abede140c2f565971.svg"),
    "motorcycle-oil": ex("2. MOTORCYCLE-10.3d85983d8440bcde80694e485b2a653c.svg"),
    "heavy-duty-diesel-engine-oil": ex("4. HEAVY DUTY OILS-10.d1d2479d1c74eb4be559465f45ec8321.svg"),
    "industrial-lubricants": ex("5. INDUSTRIAL OILS-10.20e725a1f87db21a6970e75ec317d258.svg"),
    "marine-lubricants": ex("6. MARINE OILS-10.26ebfdbbff1a412135a0dbea9df639b4.svg"),
    "grease": ex("7. GREASE-10.6f420152bd01742fabd48287c159c434.svg"),
    "transmission-and-gear-oil": ex("3. LCV-10.81dc621a2e21d81402f9164fe857dd14.svg"),
    "car-care": ex("1. CAR-10.54891bf785959f4abede140c2f565971.svg"),
}
MARKETS = ["Malaysia (home market)", "South Korea", "Brunei", "Vietnam", "China", "Hong Kong", "Macau",
           "Tonga", "Cambodia", "Singapore", "Thailand", "Laos", "United Arab Emirates"]

def esc(s): return html.escape(str(s), quote=True)

# ------------------------------------------------------------------ products (labels as listed by KohDen SG)
# id, category, name, grade, spec, base, pack, image
PRODUCTS = [
 ("hyb", "passenger-car-engine-oil", "Extentios Hybrid", "0W-16", "API SP", "Fully synthetic", "4L", kd("2026/04/E2001-0W16P-4000-4L.jpg")),
 ("mr0w20", "passenger-car-engine-oil", "Extentios Molyracing", "0W-20", "API SN/CF, ACEA A5/B5", "Fully synthetic (PAO and ester)", "4L", kd("2026/04/0W20P-4L.jpg")),
 ("mr5w30", "passenger-car-engine-oil", "Extentios Molyracing", "5W-30", "API SN/CF, ACEA A3/B4, C3", "Fully synthetic (PAO and ester)", "4L", kd("2026/04/5W30P-4L.jpg")),
 ("mr5w40", "passenger-car-engine-oil", "Extentios Molyracing", "5W-40", "API SN/CF, ACEA A3/B4, C3", "Fully synthetic (PAO and ester)", "4L", kd("2026/04/5W40P-4L.jpg")),
 ("mr5w50", "passenger-car-engine-oil", "Extentios Molyracing", "5W-50", "API SN/CF, ACEA A3/B4, C3", "Fully synthetic (PAO and ester)", "1L", kd("2026/04/5W50N-1L.jpg")),
 ("cm5w30", "passenger-car-engine-oil", "Carios Molytech Nano", "5W-30", "API SN/CF, ACEA A3/B4", "Molytech nano formula", "4L", kd("2026/04/E3001-5W30P-4000.jpg")),
 ("cm10w40", "passenger-car-engine-oil", "Carios Molytech Nano", "10W-40", "API SN/CF, ACEA A3/B4", "Molytech nano formula", "4L", kd("2026/03/E3002-10W40P-4000.jpg")),
 ("atf", "transmission-and-gear-oil", "ATFIOS ATF", "", "Automatic transmission fluid", "Fully synthetic", "4L", kd("2026/04/EXN-–-ATFIOS-ATF-–-FULLY-SYN-4L-E4001-ATMF-4000.jpg")),
 ("cvtf", "transmission-and-gear-oil", "ATFIOS CVTF", "", "CVT fluid", "Fully synthetic", "4L", kd("2026/04/E4002-CVTF-4000-4L.jpg")),
 ("dot4", "car-care", "+Care Brake Fluid", "DOT 4", "Brake fluid", "", "1L", kd("2026/04/E5001-DOT4-1000-1L.jpg")),
 ("dot51", "car-care", "+Care Brake Fluid", "DOT 5.1", "Brake fluid", "", "1L", kd("2026/04/E5002-DOT5-1000-1L.jpg")),
 ("psf", "car-care", "+Care Power Steering Fluid", "", "Power steering fluid", "", "1L", kd("2026/04/E5011-C_CARE-1000-1L.jpg")),
 ("atfb", "car-care", "+Care ATF Stop Leak + Treatment (blue)", "", "Automatic gearbox treatment", "", "450ml", kd("2026/04/EXN-–-ATF-STOP-LEAK-TREATMENT-BLUE-450ML-E4011-C.jpg")),
 ("atfy", "car-care", "+Care ATF Stop Leak, High Mileage (yellow)", "", "Automatic gearbox treatment", "", "450ml", kd("2026/04/EXN-–-ATF-STOP-LEAK-TREATMENT-HIGH-MILEAGE-YELLOW-450ML-E4012-C.jpg")),
 ("cvtt", "car-care", "+Care CVT Treatment", "", "CVT gearbox treatment", "", "450ml", kd("2026/04/E4013-C_CARE-0450-0.45L.jpg")),
 ("pic", "car-care", "+Care Petrol Injector Cleaner", "", "Fuel system cleaner", "", "350ml", kd("2026/04/E6011-C_CARE-0350-0.35L.jpg")),
 ("dic", "car-care", "+Care Diesel Injector Cleaner", "", "Fuel system cleaner", "", "350ml", kd("2026/04/E6012-C_CARE-0350-0.35L.jpg")),
 ("eop", "car-care", "+Care Engine Optimizer Pro", "", "Engine oil treatment", "", "350ml", kd("2026/04/E6013-C_CARE-0350-0.35L.jpg")),
 ("eb", "car-care", "+Care Engine Booster", "", "Engine oil treatment", "", "350ml", kd("2026/04/E6014-C_CARE-350-0.35L.jpg")),
 ("ef", "car-care", "+Care Super Engine Flush", "", "Engine flush", "", "450ml", kd("2026/04/E6015-C_CARE-0450-0.45L.jpg")),
 ("x40", "car-care", "X40 Ultra Lube Spray", "", "Lubricant spray", "", "400ml", kd("2026/04/E7011-C_CARE-0400-0.4L.jpg")),
]
def prods(cat): return [p for p in PRODUCTS if p[1] == cat]

# ------------------------------------------------------------------ categories
CATS = [
 dict(slug="passenger-car-engine-oil", name="Passenger car engine oil", short="Car engine oil",
  title="Car Engine Oil Malaysia | 0W-16 to 5W-50 | EXN Lube",
  desc="EXN car engine oils: Extentios Hybrid 0W-16 (API SP), Extentios Molyracing 0W-20 to 5W-50 and Carios Molytech Nano. Grades, specs and pack sizes.",
  card="Fully synthetic and Molytech oils for daily cars, hybrids, diesels and performance engines.",
  answer="EXN makes three passenger car engine oil families: Extentios Hybrid 0W-16 (fully synthetic, API SP) for hybrids, Extentios Molyracing in 0W-20, 5W-30, 5W-40 and 5W-50 (fully synthetic PAO and ester) for modern and performance engines, and Carios Molytech Nano in 5W-30 and 10W-40 with EXN's Molytech nano technology.",
  body="<p>EXN describes its car range like this: \"Our range of engine lubricants has been meticulously formulated to withstand even the most arduous conditions, ensuring peak performance. We take pride in offering an array of engine oil solutions tailored to various form of car types, from commercial cars, diesel cars to high-performance racing engines.\"</p>"
       "<p>Every oil carries a dual API rating (SN/CF) or the latest API SP, plus ACEA sequences where listed, so a workshop can match it to the owner's manual.</p>",
  faq=[("Which EXN oil is for a hybrid car?", "Extentios Hybrid 0W-16, a fully synthetic oil rated API SP and sold in 4L. Use it where your owner's manual calls for 0W-16."),
       ("Which EXN oil suits a turbo or performance car?", "Extentios Molyracing, a fully synthetic PAO and ester oil in 0W-20, 5W-30, 5W-40 and 5W-50. The 5W-30 and 5W-40 also carry ACEA C3. Pick the grade in your owner's manual."),
       ("What does API SN/CF mean on EXN oils?", "SN is an API petrol engine category and CF a diesel category, so the oil is rated for both. See our <a href=\"{r}articles/how-to-read-an-engine-oil-label/\">guide to reading an oil label</a>.")]),
 dict(slug="motorcycle-oil", name="Motorcycle oil (Motios)", short="Motorcycle oil",
  title="Motorcycle Engine Oil Malaysia | Motios Series | EXN Lube",
  desc="EXN Motios motorcycle oils for high-output, high-temperature engines: clutch engagement, engine protection and extreme pressure protection.",
  card="Motios oils for high-output, high-temperature bike engines and wet clutches.",
  answer="EXN's motorcycle range is the Motios series, launched between 2019 and 2021. EXN says these oils are made for high-output, high-temperature motorcycle engines by blending synthetic and petroleum-based oils, with good clutch engagement, engine protection and extreme pressure protection for all types of transmissions.",
  body="<p>In EXN's words: \"specifically designed for high output and high temperature motorcycle engines which are created through blending synthetic and petroleum-based oils. Our products excels when comes to clutch engagement, superior engine protection and capable to withstand extreme pressure protection for all types of transmissions.\"</p>"
       "<p>EXN has supported motorcycle events such as PortBike Motoday Kedah and the Malaysia Cub Prix, and holds a Certificate of Achievement from the Malaysian Motorcycle Association for its \"Zero Engine Oil Run\".</p>",
  faq=[("Is Motios oil safe for wet clutches?", "EXN states the Motios series excels at clutch engagement. Check the JASO grade on the bottle against your bike's manual before use."),
       ("Which Motios grade do I need?", "Follow the viscosity in your motorcycle's owner's manual, then ask an EXN stockist for the matching Motios bottle.")]),
 dict(slug="heavy-duty-diesel-engine-oil", name="Heavy duty diesel engine oil (HDDEO)", short="Heavy duty diesel",
  title="Heavy Duty Diesel Engine Oil Malaysia | HDDEO | EXN Lube",
  desc="EXN heavy duty diesel engine oil for trucks, commercial and farm engines: wear protection, soot control and bearing corrosion protection.",
  card="HDDEO for trucks, buses, commercial and farm diesel engines.",
  answer="EXN Heavy Duty Diesel Engine Oil (HDDEO) is made for the diesel engines of heavy trucks, commercial vehicles and farm machinery. EXN says it is blended to meet and exceed major truck and engine makers' requirements, with advanced additives for wear protection, soot control and bearing corrosion protection.",
  body="<p>EXN's tagline for the range is \"Built To Endure, Designed To Excel\". The company describes it as \"specialized for the Heavy Duty diesel engines of vehicles blended design for Heavy Truck, Commercial and Farm lubricants\".</p>"
       "<p>Fleet operators can contact EXN for drum and bulk supply and for the specification sheet of each grade.</p>",
  faq=[("Who is EXN HDDEO for?", "Owners and fleets running heavy trucks, buses, commercial diesels and farm machinery. Contact EXN for the grade and approvals that match your engines."),
       ("Can I buy EXN diesel oil in bulk?", "Yes, contact EXN's marketing team for fleet and bulk supply. Ask for the technical data sheet of the grade you need.")]),
 dict(slug="industrial-lubricants", name="Industrial lubricants", short="Industrial oils",
  title="Industrial Lubricants Malaysia | Hydraulic, Turbine | EXN",
  desc="EXN industrial lubricants for hydraulic systems, turbines, compressors, bearings, open and closed gears and pneumatic tools, up to power plants.",
  card="Hydraulic, turbine, compressor, bearing and gear oils for plants and factories.",
  answer="EXN supplies industrial lubricants for hydraulic systems, turbines, compressors, bearings, open and closed gears and pneumatic tools. EXN says the range serves the industrial sector from small plants to mega power plants. Contact EXN with your equipment list to get the matching grades.",
  body="<p>In EXN's words, the range is used \"in a diverse range of equipment, including hydraulic systems, turbines, compressors, bearings, open and close gears, pneumatic tools and industrial sector... from small to mega power plants.\"</p>",
  faq=[("Which industrial oils does EXN make?", "Lubricants for hydraulic systems, turbines, compressors, bearings, open and closed gears and pneumatic tools. Ask EXN for the data sheet of each grade."),
       ("How do I order industrial lubricants from EXN?", "Email or call EXN's head office in Petaling Jaya with your equipment and volumes, and the team will advise the grades.")]),
 dict(slug="marine-lubricants", name="Marine lubricants", short="Marine oils",
  title="Marine Lubricants Malaysia | Marine Diesel Engine Oil | EXN",
  desc="EXN marine lubricants for fast and stationary diesel engines, with detergent and dispersant properties, oxidation resistance and anti-wear.",
  card="Marine diesel engine oils for fast and stationary diesel engines.",
  answer="EXN marine lubricants are made for fast and stationary diesel engines. EXN says they are formulated with detergent and dispersant properties, resist oxidation, protect against wear and have favourable alkalinity (TBN) to neutralise acids from combustion.",
  body="<p>EXN: \"Specially formulated with detergent and dispersant properties, these marine lubricants are designed to cater to the needs of fast and stationary diesel engines. They exhibit excellent resistance to oxidation, anti-wear capabilities, and possess favorable alkalinity properties.\"</p>",
  faq=[("What engines are EXN marine oils for?", "Fast and stationary marine diesel engines. Contact EXN with your engine maker and model for the right grade."),
       ("Why does alkalinity matter in marine oil?", "Alkalinity, shown as TBN, neutralises acids formed when diesel fuel burns, which helps protect engine metal.")]),
 dict(slug="grease", name="Grease", short="Grease",
  title="Lithium Grease Malaysia | Lithium Complex Grease | EXN Lube",
  desc="EXN lithium and lithium complex greases on mineral or synthetic base oil, for automotive and industrial bearings, gears and sliding surfaces.",
  card="Lithium and lithium complex greases for bearings, gears and sliding parts.",
  answer="EXN grease is made with lithium and lithium complex thickeners on a mineral or synthetic base oil. EXN says it gives rust prevention, anti-wear and extreme pressure protection for automotive and industrial bearings, gears and sliding surfaces.",
  body="<p>EXN describes its greases as having a \"base oil composed of mineral or synthetic\" and being \"comprised of Lithium &amp; Lithium Complex\", used for \"rust prevention, anti-wear purposes, and as an extreme pressure agent\".</p>",
  faq=[("What is the difference between lithium and lithium complex grease?", "Lithium complex grease generally handles higher temperatures than simple lithium grease. Choose the type your equipment maker specifies."),
       ("Where is EXN grease used?", "On automotive and industrial bearings, gears and sliding surfaces, according to EXN.")]),
 dict(slug="transmission-and-gear-oil", name="Transmission and gear oil (Atfios, Garios)", short="Gearbox oils",
  title="ATF, CVT Fluid and Gear Oil | Atfios and Garios | EXN Lube",
  desc="EXN Atfios fully synthetic ATF and CVT fluid (4L) and Garios gear oil. Which fluid fits which gearbox, and why never to mix them.",
  card="Atfios ATF and CVT fluid, and Garios gear oil.",
  answer="EXN's gearbox range has two families: Atfios transmission fluids, which include a fully synthetic ATF for conventional automatic gearboxes and a fully synthetic CVTF for CVT gearboxes (both 4L), and Garios gear oils for manual gearboxes and differentials. EXN's tagline: \"Shift Into Excellence, Powering Your Drive With Precision\".",
  body="<p>ATF and CVT fluid are not interchangeable. A CVT needs a fluid with the right friction for its belt and pulleys, while a conventional automatic uses ATF. Read our <a href=\"{r}articles/atf-vs-cvt-fluid/\">guide to ATF vs CVT fluid</a> before changing either.</p>",
  faq=[("Can I use ATF in a CVT gearbox?", "No. A CVT needs CVT fluid such as Atfios CVTF. Using ATF can make the belt slip and damage the gearbox."),
       ("Is Atfios fully synthetic?", "Yes. Both Atfios ATF and Atfios CVTF are listed as fully synthetic, in 4L bottles.")]),
 dict(slug="car-care", name="+Care car care series", short="+Care car care",
  title="Brake Fluid, Engine Flush and Treatments | +Care | EXN Lube",
  desc="EXN +Care: DOT 4 and DOT 5.1 brake fluid, power steering fluid, ATF and CVT treatments, injector cleaners, engine flush and X40 spray.",
  card="Brake fluid, power steering fluid, flushes, injector cleaners and treatments.",
  answer="EXN's +Care series covers the fluids and treatments a car needs between oil changes: DOT 4 and DOT 5.1 brake fluid, power steering fluid, ATF Stop Leak treatments, CVT Treatment, petrol and diesel injector cleaners, Engine Optimizer Pro, Engine Booster, Super Engine Flush and the X40 Ultra Lube Spray.",
  body="<p>EXN's tagline for the series is \"Engineered For Excellence\". Brake fluid absorbs moisture over time, so replace it at the interval in your car's service schedule. See <a href=\"{r}articles/dot-4-vs-dot-5-1-brake-fluid/\">DOT 4 vs DOT 5.1 brake fluid</a>.</p>",
  faq=[("Can I mix DOT 4 and DOT 5.1 brake fluid?", "Both are glycol-based and compatible, but it is best to flush and fill with one type. Never mix them with silicone DOT 5."),
       ("What does Super Engine Flush do?", "An engine flush is added before an oil change to help loosen deposits so they drain out with the old oil. Follow the label's instructions.")]),
]
CAT = {c["slug"]: c for c in CATS}

# product detail pages (engine oils with real specs)
PPAGES = [
 dict(slug="extentios-hybrid-0w-16", ids=["hyb"], name="Extentios Hybrid 0W-16",
  title="Extentios Hybrid 0W-16 Fully Synthetic Oil | API SP | EXN",
  desc="EXN Extentios Hybrid 0W-16: fully synthetic engine oil rated API SP for hybrid cars, in 4L. Specs, who it is for and where to buy.",
  tag="Efficiency In Silence, Long-Term Brilliance",
  answer="Extentios Hybrid 0W-16 is EXN's fully synthetic engine oil for hybrid cars. It is rated API SP, the current API petrol category, and comes in a 4L bottle. Use it where your owner's manual calls for SAE 0W-16.",
  body="<p>Hybrid engines stop and start many times on every trip and often run cooler than a normal engine, so makers specify very thin oils such as 0W-16 that flow at once and cut friction. Read <a href=\"../../articles/which-engine-oil-for-hybrid-cars/\">which engine oil a hybrid car needs</a>.</p>",
  faq=[("Is Extentios Hybrid 0W-16 only for hybrids?", "It is made for hybrids, but any engine whose manual specifies 0W-16 and API SP can use it."),
       ("Can I use 0W-20 instead of 0W-16?", "Follow your owner's manual. Many hybrids accept 0W-20 as an alternative, but some do not.")]),
 dict(slug="extentios-molyracing", ids=["mr0w20", "mr5w30", "mr5w40", "mr5w50"], name="Extentios Molyracing",
  title="Extentios Molyracing 0W-20 to 5W-50 | Fully Synthetic | EXN",
  desc="EXN Extentios Molyracing fully synthetic PAO and ester engine oil in 0W-20, 5W-30, 5W-40 and 5W-50. API SN/CF, ACEA A3/B4, C3 and A5/B5.",
  tag="The MolyRacing series for premium cars",
  answer="Extentios Molyracing is EXN's top passenger car oil: fully synthetic, made with PAO and ester base oils, in four grades. 0W-20 is rated API SN/CF and ACEA A5/B5. 5W-30, 5W-40 and 5W-50 are rated API SN/CF, ACEA A3/B4 and C3.",
  body="<p>EXN launched the MolyRacing series for premium cars between 2019 and 2021 and has run it in the Malaysia Speed Festival, which EXN has sponsored since 2017. The name comes from EXN's <a href=\"../../technology/molytech/\">Molytech technology</a>.</p>",
  faq=[("Which Molyracing grade should I use?", "The one in your owner's manual. 0W-20 suits many modern Japanese petrol engines; 5W-30 and 5W-40 with ACEA C3 suit many European cars; 5W-50 is for engines that call for a thicker hot grade."),
       ("What does ACEA C3 mean?", "C3 is a European low-ash (mid-SAPS) category for engines with diesel particulate filters and catalytic converters.")]),
 dict(slug="carios-molytech-nano", ids=["cm5w30", "cm10w40"], name="Carios Molytech Nano",
  title="Carios Molytech Nano 5W-30 and 10W-40 | EXN Lube",
  desc="EXN Carios Molytech Nano engine oil in 5W-30 and 10W-40, API SN/CF and ACEA A3/B4, 4L. Molytech nano technology explained.",
  tag="Enhanced Lubrication, Unmatched Efficiency",
  answer="Carios Molytech Nano is EXN's everyday engine oil with Molytech nano technology, in 5W-30 and 10W-40. Both grades are rated API SN/CF and ACEA A3/B4 and come in 4L. In 2020 EXN used Carios Molytech in its 100 km \"without engine oil\" demonstration.",
  body="<p>Molytech, in EXN's words, works like \"billions of ball bearings\" that fill gaps between metal surfaces and turn sliding friction into rolling. See <a href=\"../../technology/molytech/\">how Molytech works</a>.</p>",
  faq=[("5W-30 or 10W-40?", "5W-30 flows faster at start-up and suits most modern engines. 10W-40 is thicker when hot and is often used in older or higher-mileage engines. Follow your owner's manual."),
       ("Is Carios Molytech Nano for petrol or diesel?", "Its API SN/CF rating covers both petrol (SN) and diesel (CF) engines that call for these categories.")]),
]

# ------------------------------------------------------------------ html helpers
CSS_V = JS_V = ""

def rel(depth): return "../" * depth

def nav(r):
    items = [("products/", "Products"), ("technology/molytech/", "Molytech"), ("where-to-buy/", "Where to buy"),
             ("articles/", "Articles"), ("about/", "About"), ("contact/", "Contact")]
    return "".join(f'<a href="{r}{h}">{t}</a>' for h, t in items)

def cta_buttons(r, ref="page"):
    b = []
    if WA:
        b.append(f'<a class="btn wa" data-ref="{ref}" href="https://wa.me/{WA}?text={quote("Hi EXN Lube, I would like to ask about ")}">WhatsApp EXN</a>')
    b.append(f'<a class="btn" href="tel:{TEL}" data-ref="{ref}">Call {PHONE}</a>')
    b.append(f'<a class="btn ghost" href="mailto:{EMAIL}" data-ref="{ref}">Email us</a>')
    return '<div class="ctas">' + "".join(b) + "</div>"

ORG_ID = SITE + "#org"
def org_schema():
    return {"@type": "Organization", "@id": ORG_ID, "name": BRAND, "legalName": LEGAL, "url": SITE,
            "logo": LOGO, "image": HERO, "slogan": "The Lubricant Expert", "foundingDate": "2015",
            "founder": {"@type": "Person", "name": "Marc Ee", "jobTitle": "Founder and CEO"},
            "telephone": PHONE, "faxNumber": FAX, "email": EMAIL,
            "identifier": {"@type": "PropertyValue", "propertyID": "SSM company registration", "value": REG},
            "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": CITY,
                        "postalCode": POST, "addressRegion": REGION, "addressCountry": "MY"},
            "areaServed": [m.split(" (")[0] for m in MARKETS],
            "brand": [{"@type": "Brand", "name": "EXN Lube"}, {"@type": "Brand", "name": "Sachi Lubricant"}],
            "sameAs": list(SOCIAL.values())}

def faq_html(faq, r):
    if not faq: return ""
    out = '<section class="faq reveal"><h2>Questions and answers</h2>'
    for q, a in faq:
        out += f'<details><summary>{esc(q)}</summary><p>{a.replace("{r}", r)}</p></details>'
    return out + "</section>"

def faq_schema(faq):
    import re
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]}

def crumbs(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(trail)]}

def crumb_html(trail, r):
    if len(trail) < 2: return ""
    parts = [f'<a href="{r}{p}">{esc(n)}</a>' for n, p in trail[:-1]] + [f"<span>{esc(trail[-1][0])}</span>"]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"

PAGES = []   # (path, lastmod)

def shell(path, title, desc, body, schema=None, image=HERO, trail=None, ogtype="website"):
    depth = path.count("/")
    r = rel(depth)
    url = SITE + path
    graph = [org_schema(), {"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": BRAND, "publisher": {"@id": ORG_ID}}]
    if trail: graph.append(crumbs(trail))
    graph += schema or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    social = "".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOCIAL.items())
    doc = f"""<!doctype html>
<html lang="en-MY">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#0b0b0c">
<link rel="icon" href="{r}favicon.ico" sizes="48x48">
<link rel="icon" href="{r}favicon.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{r}favicon.png">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="{r}exn.css?v={CSS_V}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<header class="top"><div class="wrap bar">
<a class="logo" href="{r}" aria-label="EXN Lube home"><img src="{LOGO_W}" alt="EXN Lube logo" width="150" height="40"></a>
<button class="menu" aria-label="Menu" aria-expanded="false">Menu</button>
<nav class="nav">{nav(r)}</nav>
</div></header>
<main>
{crumb_html(trail or [], r)}
{body}
</main>
<footer class="foot"><div class="wrap cols">
<div><img src="{LOGO_W}" alt="EXN Lube" width="120" height="32" loading="lazy"><p><b>{LEGAL}</b><br>Reg. no. {REG}<br>{esc(ADDR)}</p>
<p><a href="tel:{TEL}">{PHONE}</a> &middot; Fax {FAX}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><b>Products</b>{"".join(f'<a href="{r}products/{c["slug"]}/">{esc(c["short"])}</a>' for c in CATS)}</div>
<div><b>EXN Lube</b><a href="{r}about/">About EXN</a><a href="{r}technology/molytech/">Molytech technology</a><a href="{r}motorsport/">Motorsport and community</a><a href="{r}distributors/">Export and distributors</a><a href="{r}where-to-buy/">Where to buy</a><a href="{r}articles/">Articles</a><a href="{r}contact/">Contact</a><a href="{r}privacy/">Privacy</a></div>
<div><b>Follow EXN</b>{social}</div>
</div><p class="wrap small">&copy; 2026 {LEGAL} EXN - The Lubricant Expert.</p></footer>
<script src="{r}exn.js?v={JS_V}" defer></script>
<script src="{r}wa-tap-counter.js?v={JS_V}" defer></script>
</body>
</html>
"""
    out = os.path.join(OUT, path, "index.html") if path.endswith("/") or path == "" else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: f.write(doc)
    if not path.startswith("404"):
        PAGES.append((path, TODAY))

def pcard(p, r, link=None):
    _, cat, name, grade, spec, base, pack, im = p
    label = f"{name} {grade}".strip()
    inner = (f'<img src="{im}" alt="EXN {esc(label)} {esc(pack)} bottle" width="300" height="300" loading="lazy">'
             f'<h3>{esc(label)}</h3><p>{esc(spec)}{(" &middot; " + esc(base)) if base else ""} &middot; {esc(pack)}</p>')
    if link: return f'<a class="pcard reveal" href="{link}">{inner}</a>'
    return f'<div class="pcard reveal">{inner}</div>'

def product_link(pid, r):
    for pp in PPAGES:
        if pid in pp["ids"]: return f'{r}products/{pp["slug"]}/'
    return None

# ------------------------------------------------------------------ pages
def home():
    r = ""
    cards = "".join(f'<a class="ccard reveal" href="products/{c["slug"]}/"><img src="{CAT_ICON[c["slug"]]}" alt="" width="56" height="56" loading="lazy"><h3>{esc(c["name"])}</h3><p>{esc(c["card"])}</p><span>More details</span></a>' for c in CATS)
    feat = "".join(pcard(p, r, product_link(p[0], r)) for p in PRODUCTS if p[0] in ("hyb", "mr5w30", "mr0w20", "cm10w40", "cvtf", "dot4"))
    arts = article_cards(r, 3)
    faq = [("Who makes EXN Lube?", f"{LEGAL}, a Malaysian lubricant company founded in 2015 and based in Damansara Perdana, Petaling Jaya, Selangor. Its founder and CEO is Marc Ee."),
           ("What does EXN Lube make?", "Engine oils for cars, motorcycles and heavy duty diesels, industrial and marine lubricants, grease, gearbox fluids and the +Care car care series."),
           ("Where can I buy EXN oil?", "From more than 700 workshops, spare parts shops and retailers in Malaysia, and from EXN's distributors in its export markets. See <a href=\"where-to-buy/\">where to buy</a>."),
           ("What is EXN Molytech?", "EXN's friction technology: nano particles that act like tiny ball bearings between metal surfaces to cut heat, wear and engine drag. See <a href=\"technology/molytech/\">how Molytech works</a>.")]
    body = f"""
<section class="hero"><img class="hero-img" src="{HERO}" alt="EXN Lube engine oil range" width="1600" height="700" fetchpriority="high">
<div class="wrap hero-txt"><p class="eyebrow">EXN &middot; The Lubricant Expert</p>
<h1>Engine oils and lubricants made in Malaysia, trusted in 12 export markets</h1>
<p class="lead">EXN Lube is a Malaysian lubricant brand from Petaling Jaya, founded in 2015. We make engine oils for cars, motorcycles and heavy duty diesels, plus industrial, marine, grease, gearbox and car care products, sold through more than 700 workshops and retailers in Malaysia.</p>
{cta_buttons(r, "home-hero")}
<p class="links"><a href="products/">See all products</a> &middot; <a href="where-to-buy/">Find a stockist</a></p></div></section>
<section class="stats wrap"><div class="stat reveal"><b>2015</b><span>founded in Petaling Jaya</span></div><div class="stat reveal"><b>700+</b><span>workshops and retailers in Malaysia</span></div><div class="stat reveal"><b>12</b><span>export markets, mostly in Asia</span></div><div class="stat reveal"><b>2017</b><span>Malaysia Speed Festival partner since</span></div></section>
<section class="wrap"><h2>Our product range</h2><div class="cgrid">{cards}</div></section>
<section class="band"><div class="wrap split"><div class="reveal"><h2>Molytech: less friction, less heat, less drag</h2><p>Molytech is EXN's nano technology. Its particles act, in EXN's words, \"like billions of ball bearings\" between metal surfaces, turning sliding friction into rolling. Lower heat helps the oil last longer and less drag helps fuel mileage.</p><a class="btn ghost" href="technology/molytech/">How Molytech works</a></div><img class="reveal" src="{MOLY}" alt="EXN Molytech nano technology illustration" width="560" height="420" loading="lazy"></div></section>
<section class="wrap"><h2>Popular EXN oils</h2><div class="pgrid">{feat}</div></section>
<section class="wrap"><h2>On track and in the community</h2><div class="carousel" data-auto>{"".join(f'<img src="{u}" alt="EXN Lube community and motorsport event" width="600" height="400" loading="lazy">' for u in COMM)}</div><p>EXN has backed the Malaysia Speed Festival every year since 2017, plus drift, Cub Prix and badminton events. <a href="motorsport/">See EXN in motorsport</a>.</p></section>
<section class="wrap"><h2>Oil questions, answered</h2><div class="agrid">{arts}</div></section>
<div class="wrap">{faq_html(faq, r)}</div>
<section class="wrap ctaband reveal"><h2>Stock EXN or ask about a grade</h2><p>Workshops, retailers and importers: talk to the EXN team in Petaling Jaya.</p>{cta_buttons(r, "home-bottom")}</section>
"""
    shell("", "EXN Lube | Engine Oil and Lubricants Malaysia", "EXN Lube is a Malaysian lubricant brand since 2015: car, motorcycle and diesel engine oils, industrial, marine, grease, ATF and +Care. 700+ stockists.",
          body, [faq_schema(faq)])

def products_index():
    r = "../"
    trail = [("Home", ""), ("Products", "products/")]
    cards = "".join(f'<a class="ccard reveal" href="{c["slug"]}/"><img src="{CAT_ICON[c["slug"]]}" alt="" width="56" height="56" loading="lazy"><h3>{esc(c["name"])}</h3><p>{esc(c["card"])}</p><span>More details</span></a>' for c in CATS)
    rows = "".join(f'<tr><td>{esc(p[2])}</td><td>{esc(p[3]) or "-"}</td><td>{esc(p[4])}</td><td>{esc(p[6])}</td></tr>' for p in PRODUCTS)
    body = f"""<section class="wrap page"><h1>EXN Lube products</h1>
<p class="answer">EXN makes lubricants in eight groups: passenger car engine oil, motorcycle oil (Motios), heavy duty diesel engine oil, industrial lubricants, marine lubricants, grease, transmission and gear oil (Atfios and Garios) and the +Care car care series. Each group has its own page below.</p>
<div class="cgrid">{cards}</div>
<h2>EXN product list with grades and specs</h2>
<div class="tbl"><table><thead><tr><th>Product</th><th>Grade</th><th>Spec / type</th><th>Pack</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="small">Grades and specs as printed on EXN labels. Motorcycle, diesel, industrial, marine and grease grades: ask EXN for the data sheet.</p>
{cta_buttons(r, "products")}</section>"""
    il = {"@type": "ItemList", "name": "EXN Lube product groups", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": c["name"], "url": SITE + f'products/{c["slug"]}/'} for i, c in enumerate(CATS)]}
    shell("products/", "EXN Lube Products | Engine Oil, Grease, ATF, +Care", "All EXN Lube products: car and motorcycle engine oil, heavy duty diesel, industrial and marine oils, grease, ATF, CVT fluid and +Care treatments.", body, [il], trail=trail)

def cat_page(c):
    path = f'products/{c["slug"]}/'
    r = "../../"
    trail = [("Home", ""), ("Products", "products/"), (c["short"], path)]
    ps = prods(c["slug"])
    grid = f'<div class="pgrid">{"".join(pcard(p, r, product_link(p[0], r)) for p in ps)}</div>' if ps else ""
    others = "".join(f'<a href="{r}products/{o["slug"]}/">{esc(o["short"])}</a>' for o in CATS if o is not c)
    body = f"""<section class="wrap page"><div class="phead"><img src="{CAT_ICON[c["slug"]]}" alt="" width="64" height="64"><h1>{esc(c["name"])}</h1></div>
<p class="answer">{esc(c["answer"])}</p>
{grid}
{c["body"].replace("{r}", r)}
{cta_buttons(r, c["slug"])}
{faq_html(c["faq"], r)}
<p class="more"><b>Other EXN products:</b> {others}</p></section>"""
    sch = [faq_schema([(q, a.replace("{r}", r)) for q, a in c["faq"]])]
    if ps:
        sch.append({"@type": "ItemList", "name": c["name"], "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": f"EXN {p[2]} {p[3]}".strip()} for i, p in enumerate(ps)]})
    shell(path, c["title"], c["desc"], body, sch, image=(ps[0][7] if ps else HERO), trail=trail)

def ppage(pp):
    path = f'products/{pp["slug"]}/'
    r = "../../"
    cat = CAT["passenger-car-engine-oil"]
    trail = [("Home", ""), ("Products", "products/"), (cat["short"], f'products/{cat["slug"]}/'), (pp["name"], path)]
    ps = [p for p in PRODUCTS if p[0] in pp["ids"]]
    rows = "".join(f'<tr><td>SAE {esc(p[3])}</td><td>{esc(p[4])}</td><td>{esc(p[5])}</td><td>{esc(p[6])}</td></tr>' for p in ps)
    body = f"""<section class="wrap page"><h1>EXN {esc(pp["name"])}</h1><p class="eyebrow">{esc(pp["tag"])}</p>
<p class="answer">{esc(pp["answer"])}</p>
<div class="pgrid">{"".join(pcard(p, r) for p in ps)}</div>
<h2>Specifications</h2><div class="tbl"><table><thead><tr><th>Grade</th><th>Specification</th><th>Base oil</th><th>Pack</th></tr></thead><tbody>{rows}</tbody></table></div>
{pp["body"]}
<h2>Where to buy {esc(pp["name"])}</h2><p>Ask any EXN stockist in Malaysia, or an EXN distributor in your country. See <a href="{r}where-to-buy/">where to buy EXN</a>.</p>
{cta_buttons(r, pp["slug"])}
{faq_html(pp["faq"], r)}</section>"""
    # Product schema without offers is invalid for rich results (MASTER-RULES 4.5 / CSKA lesson): use ProductGroup-free ItemList + brand info
    sch = [faq_schema(pp["faq"]), {"@type": "ItemList", "name": f"EXN {pp['name']} grades", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": f"EXN {p[2]} {p[3]} {p[6]}", "image": p[7]} for i, p in enumerate(ps)]}]
    shell(path, pp["title"], pp["desc"], body, sch, image=ps[0][7], trail=trail)

def molytech():
    path = "technology/molytech/"
    r = "../../"
    trail = [("Home", ""), ("Molytech technology", path)]
    faq = [("What is Molytech?", "EXN's nano technology based on a 60-atom sphere called a buckyball. Its nano particles act like tiny ball bearings between metal parts to reduce friction, heat, wear and engine drag."),
           ("Which EXN oils use Molytech?", "The Carios Molytech Nano range and the Extentios Molyracing range carry the Molytech name."),
           ("Did EXN really drive 100 km without engine oil?", "EXN ran a demonstration in 2020: Carios Molytech was added to a Toyota Vios engine, the oil was flushed out and the car was driven from Klang to Rawang via Damansara and back. EXN reports no scratches or damage. The video is on EXN's YouTube channel.")]
    benefits = ["Cleans out deposits in the piston", "Prevents sludge from clumping in the oil tank", "Forms a film layer that stops metal-to-metal friction and wear",
                "Works as an anti-foaming agent", "Holds the oil's viscosity across temperatures, lowering shear and extending the drain interval",
                "Nano particles spread into curved surfaces", "A tackifier helps the oil stick to metal while the engine runs",
                "Raises TBN to fight corrosion from combustion acids"]
    body = f"""<section class="wrap page"><h1>Molytech: how EXN's nano technology works</h1>
<p class="answer">Molytech is EXN's friction technology. It is based on a 60-atom sphere called a buckyball that looks like a soccer ball at atomic level. The nano particles act like billions of ball bearings that fill gaps in metal surfaces, turning sliding friction into rolling, which EXN says lowers heat, wear and engine drag.</p>
<img class="wide reveal" src="{MOLY}" alt="Molytech nano particles acting as ball bearings between metal surfaces" width="1000" height="560" loading="lazy">
<h2>What Molytech does, step by step</h2>
<ol><li>Nano particles spread through the oil and settle into the tiny peaks and valleys of metal surfaces.</li><li>They make the surface more even at atomic level.</li><li>Moving parts roll over the particles instead of grinding against each other.</li><li>Less friction means less heat, which helps the oil last longer, and less engine drag, which helps fuel mileage.</li></ol>
<h2>The eight benefits EXN lists</h2><ul class="ticks">{"".join(f"<li>{esc(b)}</li>" for b in benefits)}</ul>
<h2>The 100 km "without engine oil" test</h2>
<p>In 2020 EXN added Carios Molytech to a Toyota Vios engine, flushed it out and drove from Klang to Rawang via Damansara and back. EXN reports that the engine \"remained in excellent condition, with no scratches or damage\". <a href="https://www.youtube.com/watch?v=SZzY5Y4k5sw" rel="noopener">Watch the video on YouTube</a>. This is a demonstration of film strength, not advice: never drive without oil.</p>
<p>EXN also holds a Certificate of Achievement from the Malaysian Motorcycle Association for its \"Zero Engine Oil Run\".</p>
<h2>Oils with Molytech</h2><p><a href="{r}products/carios-molytech-nano/">Carios Molytech Nano 5W-30 and 10W-40</a> &middot; <a href="{r}products/extentios-molyracing/">Extentios Molyracing 0W-20 to 5W-50</a></p>
{cta_buttons(r, "molytech")}
{faq_html(faq, r)}</section>"""
    vid = {"@type": "VideoObject", "name": "EXN Lube: 100 km without engine oil (Carios Molytech)", "description": "EXN's 2020 demonstration driving a Toyota Vios from Klang to Rawang and back after flushing out the engine oil.",
           "thumbnailUrl": "https://i.ytimg.com/vi/SZzY5Y4k5sw/hqdefault.jpg", "contentUrl": "https://www.youtube.com/watch?v=SZzY5Y4k5sw", "uploadDate": "2020-01-01"}
    # OPEN: real upload date of the video; VideoObject left out until confirmed (uploadDate must be true)
    shell(path, "Molytech Nano Technology Explained | EXN Lube", "How EXN Molytech works: buckyball nano particles act like ball bearings to cut friction, heat and drag. Benefits and the 100 km test.", body, [faq_schema(faq)], image=MOLY, trail=trail)

def about():
    path = "about/"
    r = "../"
    trail = [("Home", ""), ("About", path)]
    tl = [("2015", "First headquarters opens in Petaling Jaya."), ("2016 to 2018", "Expands to Sabah and Sarawak, first export to China, sponsors the Kepong FC badminton team. Certificate of Achievement from the Malaysian Motorcycle Association for the \"Zero Engine Oil Run\"."),
          ("2019 to 2021", "Launches the Motios motorcycle series and the MolyRacing series for premium cars, sponsors the Malaysia Speed Festival and rebrands with a new logo."),
          ("2022 to 2023", "Debut at the TAPA 2023 expo and a fifth straight year with the Malaysia Speed Festival."),
          ("2024 to 2025", "Exhibits at trade shows including Automechanika Dubai and Automechanika Shanghai; 50 EXN-wrapped cars drive across Klang Valley from December 2024.")]
    body = f"""<section class="wrap page"><h1>About EXN Lube</h1>
<p class="answer">EXN Lube is a Malaysian lubricant brand owned by {LEGAL} (registration {REG}). Founded in 2015 and based at Metropolitan Square, Damansara Perdana, Petaling Jaya, EXN supplies engine oils and lubricants to more than 700 workshops, spare parts shops and retailers in Malaysia and to over 10 export markets.</p>
<img class="wide reveal" src="{COMPANY}" alt="EXN Lube company photo" width="1000" height="560" loading="lazy">
<h2>Company facts</h2>
<div class="tbl"><table><tbody>
<tr><th>Brand</th><td>EXN Lube (also Sachi Lubricant)</td></tr><tr><th>Company</th><td>{LEGAL}</td></tr><tr><th>Registration</th><td>{REG}</td></tr>
<tr><th>Founded</th><td>2015</td></tr><tr><th>Founder and CEO</th><td>Marc Ee</td></tr><tr><th>Head office</th><td>{esc(ADDR)}</td></tr>
<tr><th>Phone</th><td><a href="tel:{TEL}">{PHONE}</a> (fax {FAX})</td></tr><tr><th>Email</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
<tr><th>Network</th><td>700+ workshops, spare parts shops and retailers in Malaysia; 12 export markets</td></tr>
<tr><th>Cover</th><td>AmAssurance product liability insurance</td></tr></tbody></table></div>
<h2>What EXN stands for</h2>
<ul class="ticks"><li><b>Lubricants.</b> \"Our focus is on lubricants and we provide solutions for all issues and applications in this field.\"</li><li><b>Value.</b> Technically advanced products that generate added value.</li><li><b>People.</b> \"Our dedicated corporate culture, along with our loyal and motivated workforce, is the strategic key to our success.\"</li></ul>
<blockquote>\"It's an honor to collaborate with a diverse range of industries, from automotive and heavy-duty to marine and industrial sectors... prioritizing the highest standards of quality, safety, and environmental responsibility.\"<cite>Marc Ee, Founder and CEO</cite></blockquote>
<h2>EXN timeline</h2><ol class="timeline">{"".join(f"<li class='reveal'><b>{y}</b> {esc(t)}</li>" for y, t in tl)}</ol>
<p><a href="{r}motorsport/">Motorsport and community</a> &middot; <a href="{r}distributors/">Export markets</a> &middot; <a href="{r}contact/">Contact EXN</a></p></section>"""
    sch = [{"@type": "AboutPage", "url": SITE + path, "about": {"@id": ORG_ID}}]
    shell(path, "About EXN Lube | Malaysian Lubricant Maker Since 2015", f"EXN Lube ({LEGAL}, reg. {REG}): Petaling Jaya lubricant brand founded 2015 by Marc Ee. 700+ stockists, 12 export markets.", body, sch, image=COMPANY, trail=trail)

def motorsport():
    path = "motorsport/"
    r = "../"
    trail = [("Home", ""), ("Motorsport and community", path)]
    msf = [("2017", "Max Impact"), ("2018", "MSF Fap Master"), ("2019", "Official Partner, MSF Series"), ("2020 to 2024", "MSF Superturismo, Cyberturismo, Supermoto, Touge, Merdeka Race and SuciMuci Motorsports")]
    body = f"""<section class="wrap page"><h1>EXN Lube in motorsport and the community</h1>
<p class="answer">EXN Lube has sponsored the Malaysia Speed Festival (MSF), a MAM and FIA-sanctioned racing championship, every year since 2017. EXN also backs drift, motorcycle, car show and badminton events and runs the EXN Lube Racing Team.</p>
<div class="carousel" data-auto>{"".join(f'<img src="{u}" alt="EXN Lube at a community or motorsport event" width="600" height="400" loading="lazy">' for u in COMM)}</div>
<h2>Malaysia Speed Festival partnership</h2><div class="tbl"><table><thead><tr><th>Year</th><th>EXN-backed series</th></tr></thead><tbody>{"".join(f"<tr><td>{y}</td><td>{esc(s)}</td></tr>" for y, s in msf)}</tbody></table></div>
<p>MSF, in EXN's words, \"aims to promote grass roots as well as the general motorsport scene in Malaysia\".</p>
<h2>Other events EXN has supported</h2><ul class="ticks"><li>Tawau Drift and PortBike Motoday Kedah</li><li>Malaysia Cub Prix and Retro Havoc</li><li>EXN GT Circuit and the EXN X50 Series</li><li>Velocity Motor Show, Malaysia Autoshow and Razer Racing Autoshow</li><li>SBC Young International Juniors Badminton Championship 2019 and the Kepong FC badminton team</li><li>Traditional Boat Race at the 32nd SEA Games, Cambodia</li></ul>
{cta_buttons(r, "motorsport")}</section>"""
    shell(path, "EXN Lube Motorsport | Malaysia Speed Festival Partner", "EXN Lube has backed the Malaysia Speed Festival since 2017, plus drift, Cub Prix, car shows and badminton. Events and series EXN supports.", body, [], image=COMM[0], trail=trail)

def distributors():
    path = "distributors/"
    r = "../"
    trail = [("Home", ""), ("Export and distributors", path)]
    faq = [("Which countries sell EXN Lube?", "Malaysia, plus South Korea, Brunei, Vietnam, China, Hong Kong, Macau, Tonga, Cambodia, Singapore, Thailand, Laos and the United Arab Emirates."),
           ("How do I become an EXN distributor?", f"Email {EMAIL} or call {PHONE} with your company, country and the product groups you want to carry."),
           ("Where does EXN exhibit?", "EXN has exhibited at trade shows including Automechanika Dubai, Automechanika Shanghai, MIAPEX, Taipei AMPA and MIMS Automobility Moscow.")]
    body = f"""<section class="wrap page"><h1>EXN Lube export markets and distributors</h1>
<p class="answer">EXN Lube is sold in Malaysia and exported to 12 markets, mostly in Asia: South Korea, Brunei, Vietnam, China, Hong Kong, Macau, Tonga, Cambodia, Singapore, Thailand, Laos and the United Arab Emirates. Importers and distributors in new markets can contact EXN's head office in Petaling Jaya.</p>
<ul class="markets">{"".join(f"<li class='reveal'>{esc(m)}</li>" for m in MARKETS)}</ul>
<h2>Why distributors carry EXN</h2><ul class="ticks"><li>A full range from one maker: car, motorcycle, diesel, industrial, marine, grease, gearbox and +Care</li><li>Labels with API and ACEA specs that workshops can check</li><li>A brand seen at the Malaysia Speed Festival since 2017 and at international trade shows</li><li>Product liability insurance from AmAssurance</li></ul>
{cta_buttons(r, "distributors")}
{faq_html(faq, r)}</section>"""
    shell(path, "EXN Lube Export Markets | Become a Distributor", "EXN Lube is exported to 12 markets including Singapore, Brunei, Vietnam, Thailand, China and the UAE. How to become an EXN distributor.", body, [faq_schema(faq)], trail=trail)

def where_to_buy():
    path = "where-to-buy/"
    r = "../"
    trail = [("Home", ""), ("Where to buy", path)]
    faq = [("Where can I buy EXN oil in Malaysia?", "At more than 700 workshops, spare parts shops and retailers across Malaysia, with most in Ipoh, Johor Bahru, Klang Valley and Kota Kinabalu. Call EXN for the nearest one."),
           ("Where can I buy EXN oil in Singapore?", "KohDen International Pte Ltd, 7 Kaki Bukit Road 1, #01-15 Eunos Technolink, Singapore 415937, lists itself as an authorised EXN distributor. Phone +65 6966 6565.")]
    body = f"""<section class="wrap page"><h1>Where to buy EXN Lube</h1>
<p class="answer">In Malaysia, EXN Lube is sold through more than 700 workshops, spare parts shops and retailers, mainly in Klang Valley, Ipoh, Johor Bahru and Kota Kinabalu. Outside Malaysia, buy from EXN's distributor in your country. Call {PHONE} for the stockist nearest you.</p>
<h2>Malaysia</h2><p>Tell us your town and we will point you to the nearest EXN workshop or shop.</p>{cta_buttons(r, "where-to-buy-my")}
<h2>Singapore</h2><p><b>KohDen International Pte Ltd</b><br>7 Kaki Bukit Road 1, #01-15 Eunos Technolink, Singapore 415937<br><a href="tel:+6569666565">+65 6966 6565</a> &middot; Mon to Fri, 9am to 5pm</p>
<h2>Other countries</h2><p>EXN is exported to {len(MARKETS) - 1} markets. See <a href="{r}distributors/">export markets</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
{faq_html(faq, r)}</section>"""
    shell(path, "Where to Buy EXN Lube | 700+ Stockists in Malaysia", "Buy EXN engine oil at 700+ workshops and shops in Malaysia, from KohDen in Singapore, or from EXN distributors in 12 export markets.", body, [faq_schema(faq)], trail=trail)

def contact():
    path = "contact/"
    r = "../"
    trail = [("Home", ""), ("Contact", path)]
    body = f"""<section class="wrap page"><h1>Contact EXN Lube</h1>
<p class="answer">EXN Lube's head office is at {esc(ADDR)}. Call {PHONE} or email {EMAIL} for products, stockists, fleet and industrial supply, or distribution.</p>
{cta_buttons(r, "contact")}
<div class="tbl"><table><tbody><tr><th>Company</th><td>{LEGAL}</td></tr><tr><th>Address</th><td>{esc(ADDR)} &middot; <a href="{MAPS}" rel="noopener">Open in Google Maps</a></td></tr>
<tr><th>Phone</th><td><a href="tel:{TEL}">{PHONE}</a></td></tr><tr><th>Fax</th><td>{FAX}</td></tr><tr><th>Email</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr>
<tr><th>Social</th><td>{" &middot; ".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOCIAL.items())}</td></tr></tbody></table></div></section>"""
    sch = [{"@type": "ContactPage", "url": SITE + path, "about": {"@id": ORG_ID}}]
    shell(path, "Contact EXN Lube | Petaling Jaya Head Office", f"Contact EXN Lube, Metropolitan Square, Damansara Perdana, Petaling Jaya. Phone {PHONE}, email {EMAIL}.", body, sch, trail=trail)

def privacy():
    path = "privacy/"
    trail = [("Home", ""), ("Privacy", path)]
    body = f"""<section class="wrap page"><h1>Privacy notice</h1>
<p>This notice explains how {LEGAL} handles personal data on this website, in line with Malaysia's Personal Data Protection Act 2010.</p>
<h2>What we collect</h2><p>We do not ask for personal data on this website. If you call, email or message us, we keep what you send so we can reply.</p>
<h2>Button taps</h2><p>When you tap a call, email or WhatsApp button, we count the tap with the page name, device type and the site that referred you. We do not record your IP address or contact details.</p>
<h2>Contact</h2><p>Questions about your data: <a href="mailto:{EMAIL}">{EMAIL}</a>, {PHONE}.</p></section>"""
    shell(path, "Privacy Notice | EXN Lube", "How EXN Lube handles personal data on exnlube.com under Malaysia's PDPA 2010.", body, [], trail=trail)

# ------------------------------------------------------------------ articles
ARTS = []
def load_articles():
    for f in sorted(glob.glob(os.path.join(HERE, "articles", "*.json"))):
        ARTS.append(json.load(open(f)))

def article_cards(r, n=None):
    imgs = {"which-engine-oil-for-hybrid-cars": kd("2026/04/E2001-0W16P-4000-4L.jpg"), "how-to-read-an-engine-oil-label": kd("2026/04/5W30P-4L.jpg"),
            "atf-vs-cvt-fluid": kd("2026/04/E4002-CVTF-4000-4L.jpg"), "fully-synthetic-vs-semi-synthetic-engine-oil": kd("2026/04/0W20P-4L.jpg"),
            "dot-4-vs-dot-5-1-brake-fluid": kd("2026/04/E5002-DOT5-1000-1L.jpg")}
    out = ""
    for a in ARTS[:n] if n else ARTS:
        a["img"] = imgs.get(a["slug"], HERO)
        out += f'<a class="acard reveal" href="{r}articles/{a["slug"]}/"><img src="{a["img"]}" alt="" width="300" height="200" loading="lazy"><h3>{esc(a["h1"])}</h3><p>{esc(a["desc"])}</p></a>'
    return out

def articles():
    r = "../"
    trail = [("Home", ""), ("Articles", "articles/")]
    body = f"""<section class="wrap page"><h1>Engine oil and lubricant articles</h1>
<p class="answer">Plain answers to the oil questions drivers and workshops ask most: which grade a hybrid needs, how to read an oil label, ATF vs CVT fluid, fully synthetic vs semi-synthetic, and DOT 4 vs DOT 5.1 brake fluid.</p>
<div class="agrid">{article_cards(r)}</div></section>"""
    shell("articles/", "Engine Oil Guides and Articles | EXN Lube", "EXN Lube guides: hybrid engine oil, reading oil labels, ATF vs CVT fluid, synthetic vs semi-synthetic oil and brake fluid types.", body, [], trail=trail)
    for a in ARTS:
        path = f'articles/{a["slug"]}/'
        rr = "../../"
        t2 = trail + [(a["h1"], path)]
        owner = a["owner"].strip("/") + "/"
        oname = next((c["short"] for c in CATS if owner.endswith(c["slug"] + "/")), None) or next((p["name"] for p in PPAGES if owner.endswith(p["slug"] + "/")), "EXN products")
        body = f"""<article class="wrap page post"><h1>{esc(a["h1"])}</h1>
<p class="meta">By the EXN Lube technical team &middot; <time datetime="{a["date"]}">8 November 2026</time></p>
<img class="wide" src="{a["img"]}" alt="{esc(a["h1"])}" width="800" height="500">
{a["body_html"].replace("<table", "<div class=\"tbl\"><table").replace("</table>", "</table></div>")}
<div class="ctaband"><p>Looking for the right EXN product? See <a href="{rr}{owner}">{esc(oname)}</a> or ask the EXN team.</p>{cta_buttons(rr, "article-" + a["slug"])}</div>
{faq_html(a["faq"], rr)}</article>"""
        art = {"@type": "Article", "headline": a["h1"], "description": a["desc"], "datePublished": a["date"], "dateModified": a["date"],
               "image": a["img"], "author": {"@type": "Organization", "name": "EXN Lube technical team", "url": SITE + "about/"},
               "publisher": {"@id": ORG_ID}, "mainEntityOfPage": SITE + path}
        shell(path, a["title"], a["desc"], body, [art, faq_schema(a["faq"])], image=a["img"], trail=t2, ogtype="article")

def notfound():
    body = f'<section class="wrap page"><h1>Page not found</h1><p>The page you asked for is not here. Try <a href="/">the EXN Lube home page</a>, <a href="/products/">all products</a> or <a href="/contact/">contact us</a>.</p></section>'
    shell("404.html", "Page not found | EXN Lube", "This page could not be found.", body, [])

# ------------------------------------------------------------------ assets + crawl files
CSS = """
:root{--ink:#111214;--bg:#ffffff;--soft:#f4f4f5;--line:#e4e4e7;--red:#d71920;--red2:#a80f15;--mute:#5b5f66;--dark:#0b0b0c}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;line-height:1.6;font-size:17px}
img{max-width:100%;height:auto}a{color:var(--red2)}
.wrap{max-width:1140px;margin:0 auto;padding:0 16px}
.top{background:var(--dark);position:sticky;top:0;z-index:20}.bar{display:flex;align-items:center;justify-content:space-between;min-height:62px}
.logo img{height:34px;width:auto;display:block}.nav{display:flex;gap:18px}.nav a{color:#fff;text-decoration:none;font-weight:600;font-size:15px;opacity:.9;transition:opacity .2s}.nav a:hover{opacity:1;color:#ff4d52}
.menu{display:none;background:none;border:1px solid #444;color:#fff;border-radius:8px;padding:6px 12px;font:inherit}
@media(max-width:860px){.menu{display:block}.nav{display:none;position:absolute;left:0;right:0;top:62px;background:var(--dark);flex-direction:column;padding:12px 16px 18px}.nav.open{display:flex}}
.crumbs{max-width:1140px;margin:14px auto 0;padding:0 16px;font-size:14px;color:var(--mute)}.crumbs a{color:var(--mute)}
.hero{position:relative;background:var(--dark);color:#fff;overflow:hidden}
.hero-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.42;animation:drift 18s ease-in-out infinite alternate}
@keyframes drift{from{transform:scale(1)}to{transform:scale(1.06)}}
.hero-txt{position:relative;padding:72px 16px 64px}.hero h1{font-size:clamp(30px,5vw,50px);line-height:1.12;margin:.2em 0;max-width:800px}
.lead{font-size:19px;max-width:720px;color:#ececec}.eyebrow{color:var(--red);font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:13px;margin:0}
.hero .eyebrow{color:#ff5a5f}.hero .links a{color:#fff}
.ctas{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}
.btn{display:inline-block;background:var(--red);color:#fff;text-decoration:none;font-weight:700;padding:13px 20px;border-radius:10px;transition:transform .2s,background .2s}
.btn:hover{background:var(--red2);transform:translateY(-2px)}.btn.ghost{background:transparent;border:2px solid currentColor;color:inherit}.btn.wa{background:#1fa855}
.page .btn.ghost{color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:-34px;position:relative}
.stat{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px;box-shadow:0 8px 24px rgba(0,0,0,.06)}.stat b{display:block;font-size:30px;color:var(--red)}.stat span{font-size:14px;color:var(--mute)}
@media(max-width:700px){.stats{grid-template-columns:1fr 1fr;margin-top:16px}}
h2{font-size:clamp(23px,3vw,30px);line-height:1.2;margin:1.6em 0 .6em}
.cgrid,.pgrid,.agrid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(240px,1fr))}
.ccard,.pcard,.acard{display:block;background:#fff;border:1px solid var(--line);border-radius:16px;padding:18px;color:inherit;text-decoration:none;transition:transform .25s,box-shadow .25s,border-color .25s}
.ccard:hover,.pcard:hover,.acard:hover{transform:translateY(-4px);box-shadow:0 12px 28px rgba(0,0,0,.09);border-color:var(--red)}
.ccard h3,.pcard h3,.acard h3{margin:.4em 0 .2em;font-size:18px}.ccard p,.pcard p,.acard p{margin:0;color:var(--mute);font-size:15px}.ccard span{display:inline-block;margin-top:10px;color:var(--red2);font-weight:700}
.pcard img{aspect-ratio:1;object-fit:contain;width:100%;background:var(--soft);border-radius:12px}.acard img{aspect-ratio:3/2;object-fit:contain;width:100%;background:var(--soft);border-radius:12px}
.band{background:var(--soft);margin:40px 0;padding:10px 0 34px}.split{display:grid;grid-template-columns:1.1fr .9fr;gap:28px;align-items:center}.split img{width:100%}.split>*,.cgrid>*,.pgrid>*,.agrid>*{min-width:0}@media(max-width:800px){.split{grid-template-columns:1fr}}
.carousel{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;scrollbar-width:none;padding-bottom:6px}.carousel::-webkit-scrollbar{display:none}
.carousel img{flex:0 0 min(78%,420px);scroll-snap-align:start;border-radius:14px;aspect-ratio:3/2;object-fit:cover}
.page{padding-bottom:40px}.page h1{font-size:clamp(28px,4vw,42px);line-height:1.15;margin:.5em 0 .3em}
.answer{font-size:19px;background:var(--soft);border-left:4px solid var(--red);padding:14px 18px;border-radius:0 12px 12px 0}
.phead{display:flex;align-items:center;gap:14px}.wide{width:100%;border-radius:16px;margin:12px 0;background:var(--soft);object-fit:contain;max-height:460px}
.tbl{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:15px;margin:8px 0}th,td{border-bottom:1px solid var(--line);padding:10px 8px;text-align:left;vertical-align:top}thead th{background:var(--dark);color:#fff}
tbody th{width:32%;color:var(--mute);font-weight:600}
.ticks{padding-left:0;list-style:none}.ticks li{padding-left:28px;position:relative;margin:8px 0}.ticks li:before{content:"";position:absolute;left:4px;top:.55em;width:12px;height:7px;border-left:3px solid var(--red);border-bottom:3px solid var(--red);transform:rotate(-45deg)}
.timeline{list-style:none;padding:0;border-left:3px solid var(--red);margin-left:6px}.timeline li{padding:6px 0 12px 18px}.timeline b{display:block;color:var(--red2)}
.markets{display:flex;flex-wrap:wrap;gap:8px;list-style:none;padding:0}.markets li{background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-weight:600}
blockquote{margin:24px 0;padding:18px 22px;background:var(--soft);border-radius:14px;font-size:18px}cite{display:block;margin-top:8px;font-style:normal;color:var(--mute);font-size:15px}
.faq details{border:1px solid var(--line);border-radius:12px;padding:12px 16px;margin:10px 0;background:#fff}.faq summary{cursor:pointer;font-weight:700}.faq p{margin:.6em 0 0}
.ctaband{background:var(--dark);color:#fff;border-radius:18px;padding:22px 24px;margin:36px auto}.ctaband a{color:#fff}.ctaband .btn.ghost{color:#fff}
.more a{margin-right:12px}.meta{color:var(--mute);font-size:14px}.post table{font-size:15px}
.foot{background:var(--dark);color:#cfcfd2;margin-top:40px;padding:34px 0 18px;font-size:15px}.foot .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:22px}.foot a{color:#fff;display:block;margin:4px 0;text-decoration:none}.foot p a{display:inline}
@media(max-width:800px){.foot .cols{grid-template-columns:1fr 1fr}}.small{font-size:13px;color:var(--mute)}.foot .small{color:#9a9aa0}
.reveal{opacity:1;transform:none}.js .reveal{opacity:0;transform:translateY(16px);transition:opacity .5s ease,transform .5s ease}.js .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.js .reveal{opacity:1;transform:none}}
"""

JS = """(function(){var d=document.documentElement;
if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver' in window){d.classList.add('js');
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});setTimeout(function(){document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')})},2500)}
var m=document.querySelector('.menu'),n=document.querySelector('.nav');if(m&&n)m.addEventListener('click',function(){var o=n.classList.toggle('open');m.setAttribute('aria-expanded',o)});
/* carousel standard: auto-slides, keeps sliding on scroll, pauses only while held/dragged, restarts ~2s after release */
document.querySelectorAll('.carousel[data-auto]').forEach(function(c){var held=false,t=null;
function step(){if(held)return;var w=c.firstElementChild?c.firstElementChild.getBoundingClientRect().width+12:300;
if(c.scrollLeft+c.clientWidth>=c.scrollWidth-4)c.scrollTo({left:0,behavior:'smooth'});else c.scrollBy({left:w,behavior:'smooth'})}
var iv=setInterval(step,3200);function down(){held=true;clearTimeout(t)}function up(){clearTimeout(t);t=setTimeout(function(){held=false},2000)}
c.addEventListener('pointerdown',down);c.addEventListener('touchstart',down,{passive:true});c.addEventListener('pointerup',up);c.addEventListener('touchend',up);c.addEventListener('pointercancel',up)})})();
"""

ROBOTS = f"""User-agent: *
Allow: /

User-agent: Googlebot
Allow: /

User-agent: Bingbot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: DuckAssistBot
Allow: /

Sitemap: {SITE}sitemap.xml
"""

def llms():
    lines = [f"# {BRAND}", "",
             f"> EXN Lube is a Malaysian lubricant brand owned by {LEGAL} (reg. {REG}), founded in 2015 in Petaling Jaya, Selangor. "
             "It makes engine oils for cars, motorcycles and heavy duty diesels, industrial and marine lubricants, grease, ATF/CVT fluids and the +Care car care series, "
             "sold through 700+ workshops and retailers in Malaysia and exported to 12 markets. Slogan: The Lubricant Expert.", "",
             "## Key facts",
             f"- Company: {LEGAL}, registration {REG}", f"- Founded: 2015; Founder and CEO: Marc Ee", f"- Head office: {ADDR}",
             f"- Phone: {PHONE}; fax {FAX}; email {EMAIL}", "- Network: 700+ workshops, spare parts shops and retailers in Malaysia",
             "- Export markets: " + ", ".join(MARKETS[1:]), "- Motorsport: Malaysia Speed Festival partner every year since 2017",
             "- Technology: Molytech (buckyball nano particles that act like ball bearings to cut friction, heat and drag)",
             "- Singapore distributor: KohDen International Pte Ltd, 7 Kaki Bukit Road 1 #01-15, Singapore 415937, +65 6966 6565", "",
             "## Engine oils"]
    for p in PRODUCTS:
        if p[1] == "passenger-car-engine-oil":
            lines.append(f"- EXN {p[2]} {p[3]}: {p[4]}; {p[5]}; {p[6]}")
    lines += ["", "## Pages"]
    for path, _ in PAGES:
        lines.append(f"- {SITE}{path}")
    return "\n".join(lines) + "\n"

def sitemap():
    urls = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{m}</lastmod></url>\n" for p, m in PAGES)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n'

HTACCESS = """# EXN Lube (exnlube.com) - apply at go-live via cPanel (the Bridge cannot write .htaccess)
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\\. [NC]
RewriteRule ^ https://exnlube.com%{REQUEST_URI} [L,R=301]
<IfModule mod_headers.c>
<FilesMatch "\\.(html)$">
Header set Cache-Control "max-age=3600"
</FilesMatch>
Header always set X-Content-Type-Options "nosniff"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
</IfModule>
"""

def main():
    global CSS_V, JS_V
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    CSS_V = hashlib.md5(CSS.encode()).hexdigest()[:8]
    tracker = open(os.path.join(HERE, "wa-tap-counter.js")).read()
    JS_V = hashlib.md5((JS + tracker).encode()).hexdigest()[:8]
    open(os.path.join(OUT, "exn.css"), "w").write(CSS)
    open(os.path.join(OUT, "exn.js"), "w").write(JS)
    open(os.path.join(OUT, "wa-tap-counter.js"), "w").write(tracker)
    if os.path.exists(os.path.join(HERE, "favicon.png")):
        for fn in ("favicon.png", "favicon.ico"): shutil.copy(os.path.join(HERE, fn), os.path.join(OUT, fn))
    load_articles()
    home(); products_index()
    for c in CATS: cat_page(c)
    for pp in PPAGES: ppage(pp)
    molytech(); about(); motorsport(); distributors(); where_to_buy(); contact(); articles(); privacy(); notfound()
    open(os.path.join(OUT, "robots.txt"), "w").write(ROBOTS)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sitemap())
    open(os.path.join(OUT, "llms.txt"), "w").write(llms())
    open(os.path.join(HERE, "htaccess-golive.txt"), "w").write(HTACCESS)
    print(f"built {len(PAGES)} pages -> {OUT}")

if __name__ == "__main__":
    main()
