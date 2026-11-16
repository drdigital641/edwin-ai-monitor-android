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

16 Nov 2026 (Edwin): converted to a SINGAPORE site. Kohden (kohden.com.sg) is the distributor; main CTA WhatsApp Kohden.
No Malaysian phone/address/"Malaysia" wording. Cross-linked with Hyper Power + Carku previews. noindex,nofollow on every page.
"""
import html, json, os, re, shutil, hashlib, glob
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")
OG_IMG = "https://pageonesingapore.com/preview/exn-lube/og-image.jpg"   # 1200x630 JPG, same file on every page (WhatsApp needs jpg/png, own host)
SITE = "https://pageonesingapore.com/preview/exn-lube/"   # Singapore preview (16 Nov 2026): canonical = preview URL until Edwin names the SG domain
TODAY = "2026-11-16"

BRAND = "EXN Lube Singapore"
LEGAL = "EXN Lube Marketing Sdn. Bhd."     # brand owner, named once in the footer legal line only
# Singapore distributor: facts read live on kohden.com.sg home + contact-us, 16 Nov 2026
KOHDEN = "https://www.kohden.com.sg/"
KOHDEN_EXN = "https://www.kohden.com.sg/product-category/exn/"
KNAME = "KohDen International Pte Ltd"
PHONE, TEL = "+65 6966 6565", "+6569666565"
EMAIL = "kohden2019@yahoo.com"
STREET = "7 Kaki Bukit Road 1, #01-15 Eunos Technolink"
POST = "415937"
ADDR = f"{STREET}, Singapore {POST}"
HOURS = "Monday to Friday, 9am to 5pm. Saturday and Sunday closed."
# WhatsApp: not shown on kohden.com.sg; +65 8603 0355 is the Kohden WhatsApp Edwin confirmed on 15 Nov 2026 (Carku, Hyper Power use it). Edwin to confirm for EXN.
WA = "6586030355"
WA_DISP = "+65 8603 0355"   # Kohden WhatsApp widget number; WhatsApp only, never for calls
HYPER = "https://pageonesingapore.com/preview/hyper-power/"
CARKU = "https://pageonesingapore.com/preview/carku/"
MAPS = "https://www.google.com/maps/search/?api=1&query=" + quote("KohDen International 7 Kaki Bukit Road 1 Eunos Technolink Singapore 415937")
SOCIAL = {
    "YouTube": "https://www.youtube.com/@exnlube.official",
    "Instagram": "https://www.instagram.com/exnlube.official/",
    "TikTok": "https://www.tiktok.com/@exnlube.official",
}
def wa(msg): return f"https://wa.me/{WA}?text=" + quote(msg, safe="")
WA_GENERAL = wa("Hi Kohden, I'd like advice on EXN engine oil for my car.\nCar model: \nOil grade in my manual (e.g. 0W-20): ")
WA_WORKSHOP = wa("Hi Kohden, our workshop would like to stock EXN oils.\nWorkshop name: \nArea: \nContact person: ")

# Official EXN images, copied from exnlube.com/static/media and served from the preview (Edwin 16 Nov: no exnlube.com links).
E = "images/brand/"
def ex(name): return SITE + E + re.sub(r"[^a-z0-9.]+", "-", name.lower())
K = "https://www.kohden.com.sg/wp-content/uploads/"
def kd(p): return K + quote(p)

LOGO = ex("EXN LOGO BLACK-01-01.4e598f95512d0f60bfa9.png")
LOGO_W = ex("EXN LOGO WHITE-01-01.331823519af95aae4b41.webp")   # 300x83
HERO = ex("EXN WEBSITE - BANNER 01.212cd9602db2172415cd.webp")   # 1280x537
MOLY = ex("molytech_big.288c9403d1bc153587ff.webp")   # 640x512
COMPANY = ex("company_photo.b91fadc2cefd1cfe51cf.webp")   # 451x297
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

def esc(s): return html.escape(str(s), quote=True)

# ------------------------------------------------------------------ products (labels as listed by KohDen SG)
# id, category, name, grade, spec, base, pack, image  (packs as listed on the Kohden store, 16 Nov 2026)
PRODUCTS = [
 ("hyb", "passenger-car-engine-oil", "Extentios Hybrid", "0W-16", "API SP", "Fully synthetic", "4L", kd("2026/04/E2001-0W16P-4000-4L.jpg")),
 ("mr0w20", "passenger-car-engine-oil", "Extentios Molyracing", "0W-20", "API SN/CF, ACEA A5/B5", "Fully synthetic (PAO and ester)", "4L or 1L", kd("2026/04/0W20P-4L.jpg")),
 ("mr5w30", "passenger-car-engine-oil", "Extentios Molyracing", "5W-30", "API SN/CF, ACEA A3/B4, C3", "Fully synthetic (PAO and ester)", "4L or 1L", kd("2026/04/5W30P-4L.jpg")),
 ("mr5w40", "passenger-car-engine-oil", "Extentios Molyracing", "5W-40", "API SN/CF, ACEA A3/B4, C3", "Fully synthetic (PAO and ester)", "4L or 1L", kd("2026/04/5W40P-4L.jpg")),
 ("mr5w50", "passenger-car-engine-oil", "Extentios Molyracing", "5W-50", "API SN/CF, ACEA A3/B4, C3", "Fully synthetic (PAO and ester)", "4L or 1L", kd("2026/04/5W50N-1L.jpg")),
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
  title="Car Engine Oil Singapore | 0W-16 to 5W-50 | EXN",
  desc="EXN car engine oils: Extentios Hybrid 0W-16 (API SP), Extentios Molyracing 0W-20 to 5W-50 and Carios Molytech Nano. Grades, specs and pack sizes.",
  card="Fully synthetic and Molytech oils for daily cars, hybrids, diesels and performance engines.",
  answer="EXN makes three passenger car engine oil families: Extentios Hybrid 0W-16 (fully synthetic, API SP) for hybrids, Extentios Molyracing in 0W-20, 5W-30, 5W-40 and 5W-50 (fully synthetic PAO and ester) for modern and performance engines, and Carios Molytech Nano in 5W-30 and 10W-40 with EXN's Molytech nano technology.",
  body="<p>EXN describes its car range like this: \"Our range of engine lubricants has been meticulously formulated to withstand even the most arduous conditions, ensuring peak performance. We take pride in offering an array of engine oil solutions tailored to various form of car types, from commercial cars, diesel cars to high-performance racing engines.\"</p>"
       "<p>Every oil carries a dual API rating (SN/CF) or the latest API SP, plus ACEA sequences where listed, so a workshop can match it to the owner's manual.</p>",
  faq=[("Which EXN oil is for a hybrid car?", "Extentios Hybrid 0W-16, a fully synthetic oil rated API SP and sold in 4L. Use it where your owner's manual calls for 0W-16."),
       ("Which EXN oil suits a turbo or performance car?", "Extentios Molyracing, a fully synthetic PAO and ester oil in 0W-20, 5W-30, 5W-40 and 5W-50. The 5W-30 and 5W-40 also carry ACEA C3. Pick the grade in your owner's manual."),
       ("What does API SN/CF mean on EXN oils?", "SN is an API petrol engine category and CF a diesel category, so the oil is rated for both. See our <a href=\"{r}articles/how-to-read-an-engine-oil-label/\">guide to reading an oil label</a>.")]),
 dict(slug="motorcycle-oil", name="Motorcycle oil (Motios)", short="Motorcycle oil",
  title="Motorcycle Engine Oil Singapore | Motios | EXN Lube",
  desc="EXN Motios motorcycle oils for high-output, high-temperature engines: clutch engagement, engine protection and extreme pressure protection.",
  card="Motios oils for high-output, high-temperature bike engines and wet clutches.",
  answer="EXN's motorcycle range is the Motios series, launched between 2019 and 2021. EXN says these oils are made for high-output, high-temperature motorcycle engines by blending synthetic and petroleum-based oils, with good clutch engagement, engine protection and extreme pressure protection for all types of transmissions.",
  body="<p>In EXN's words: \"specifically designed for high output and high temperature motorcycle engines which are created through blending synthetic and petroleum-based oils. Our products excels when comes to clutch engagement, superior engine protection and capable to withstand extreme pressure protection for all types of transmissions.\"</p>"
       "<p>Kohden's Singapore store does not list Motios yet. Ask Kohden on WhatsApp whether they can supply the grade your bike needs.</p>",
  faq=[("Is Motios oil safe for wet clutches?", "EXN states the Motios series excels at clutch engagement. Check the JASO grade on the bottle against your bike's manual before use."),
       ("Which Motios grade do I need?", "Follow the viscosity in your motorcycle's owner's manual, then ask Kohden, EXN's Singapore distributor, whether that Motios grade is available.")]),
 dict(slug="heavy-duty-diesel-engine-oil", name="Heavy duty diesel engine oil (HDDEO)", short="Heavy duty diesel",
  title="Heavy Duty Diesel Engine Oil Singapore | HDDEO | EXN",
  desc="EXN heavy duty diesel engine oil for trucks, commercial and farm engines: wear protection, soot control and bearing corrosion protection.",
  card="HDDEO for trucks, buses, commercial and farm diesel engines.",
  answer="EXN Heavy Duty Diesel Engine Oil (HDDEO) is made for the diesel engines of heavy trucks, commercial vehicles and farm machinery. EXN says it is blended to meet and exceed major truck and engine makers' requirements, with advanced additives for wear protection, soot control and bearing corrosion protection.",
  body="<p>EXN's tagline for the range is \"Built To Endure, Designed To Excel\". The company describes it as \"specialized for the Heavy Duty diesel engines of vehicles blended design for Heavy Truck, Commercial and Farm lubricants\".</p>"
       "<p>Kohden's Singapore store does not list HDDEO grades yet. Fleet operators can ask Kohden about supply and the specification sheet of each grade.</p>",
  faq=[("Who is EXN HDDEO for?", "Owners and fleets running heavy trucks, buses, commercial diesels and farm machinery. Ask Kohden, EXN's Singapore distributor, about the grades and approvals for your engines."),
       ("How do I order EXN diesel oil in Singapore?", f"WhatsApp Kohden on {WA_DISP} or call {PHONE} with your engines and volumes. Ask for the technical data sheet of the grade you need.")]),
 dict(slug="industrial-lubricants", name="Industrial lubricants", short="Industrial oils",
  title="Industrial Lubricants Singapore | Hydraulic, Turbine | EXN",
  desc="EXN industrial lubricants for hydraulic systems, turbines, compressors, bearings, open and closed gears and pneumatic tools, up to power plants.",
  card="Hydraulic, turbine, compressor, bearing and gear oils for plants and factories.",
  answer="EXN supplies industrial lubricants for hydraulic systems, turbines, compressors, bearings, open and closed gears and pneumatic tools. EXN says the range serves the industrial sector from small plants to mega power plants. Kohden's Singapore store does not list industrial grades yet, so send Kohden your equipment list and ask what they can supply.",
  body="<p>In EXN's words, the range is used \"in a diverse range of equipment, including hydraulic systems, turbines, compressors, bearings, open and close gears, pneumatic tools and industrial sector... from small to mega power plants.\"</p>",
  faq=[("Which industrial oils does EXN make?", "Lubricants for hydraulic systems, turbines, compressors, bearings, open and closed gears and pneumatic tools. Ask EXN for the data sheet of each grade."),
       ("How do I order industrial lubricants from EXN?", f"WhatsApp Kohden, EXN's Singapore distributor, on {WA_DISP} or call {PHONE} with your equipment and volumes.")]),
 dict(slug="marine-lubricants", name="Marine lubricants", short="Marine oils",
  title="Marine Lubricants Singapore | Marine Diesel Oil | EXN",
  desc="EXN marine lubricants for fast and stationary diesel engines, with detergent and dispersant properties, oxidation resistance and anti-wear.",
  card="Marine diesel engine oils for fast and stationary diesel engines.",
  answer="EXN marine lubricants are made for fast and stationary diesel engines. EXN says they are formulated with detergent and dispersant properties, resist oxidation, protect against wear and have favourable alkalinity (TBN) to neutralise acids from combustion.",
  body="<p>EXN: \"Specially formulated with detergent and dispersant properties, these marine lubricants are designed to cater to the needs of fast and stationary diesel engines. They exhibit excellent resistance to oxidation, anti-wear capabilities, and possess favorable alkalinity properties.\"</p>",
  faq=[("What engines are EXN marine oils for?", "Fast and stationary marine diesel engines. Ask Kohden, EXN's Singapore distributor, with your engine maker and model."),
       ("Why does alkalinity matter in marine oil?", "Alkalinity, shown as TBN, neutralises acids formed when diesel fuel burns, which helps protect engine metal.")]),
 dict(slug="grease", name="Grease", short="Grease",
  title="Lithium Grease Singapore | Lithium Complex | EXN Lube",
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
  body="<p>EXN launched the MolyRacing series for premium cars between 2019 and 2021. Kohden's Singapore store lists every Molyracing grade in 4L and 1L bottles. The name comes from EXN's <a href=\"../../technology/molytech/\">Molytech technology</a>.</p>",
  faq=[("Which Molyracing grade should I use?", "The one in your owner's manual. 0W-20 suits many modern Japanese petrol engines; 5W-30 and 5W-40 with ACEA C3 suit many European cars; 5W-50 is for engines that call for a thicker hot grade."),
       ("What does ACEA C3 mean?", "C3 is a European low-ash (mid-SAPS) category for engines with diesel particulate filters and catalytic converters.")]),
 dict(slug="carios-molytech-nano", ids=["cm5w30", "cm10w40"], name="Carios Molytech Nano",
  title="Carios Molytech Nano 5W-30 and 10W-40 | EXN Lube",
  desc="EXN Carios Molytech Nano engine oil in 5W-30 and 10W-40, API SN/CF and ACEA A3/B4, 4L. Molytech nano technology explained.",
  tag="Enhanced Lubrication, Unmatched Efficiency",
  answer="Carios Molytech Nano is EXN's everyday engine oil with Molytech nano technology, in 5W-30 and 10W-40. Both grades are rated API SN/CF and ACEA A3/B4 and come in 4L. In 2020 EXN used Carios Molytech in a 100 km \"without engine oil\" demonstration.",
  body="<p>Molytech, in EXN's words, works like \"billions of ball bearings\" that fill gaps between metal surfaces and turn sliding friction into rolling. See <a href=\"../../technology/molytech/\">how Molytech works</a>.</p>",
  faq=[("5W-30 or 10W-40?", "5W-30 flows faster at start-up and suits most modern engines. 10W-40 is thicker when hot and is often used in older or higher-mileage engines. Follow your owner's manual."),
       ("Is Carios Molytech Nano for petrol or diesel?", "Its API SN/CF rating covers both petrol (SN) and diesel (CF) engines that call for these categories.")]),
]

# ------------------------------------------------------------------ html helpers
CSS_V = JS_V = ""

def rel(depth): return "../" * depth

def nav(r):
    items = [("products/", "Products"), ("technology/molytech/", "Molytech"), ("workshops/", "For workshops"),
             ("where-to-buy/", "Where to buy"), ("articles/", "Articles"), ("contact/", "Contact Kohden")]
    return "".join(f'<a href="{r}{h}">{t}</a>' for h, t in items)

def cta_buttons(r, ref="page", label="WhatsApp Kohden", href=None):
    href = href or WA_GENERAL
    return (f'<div class="ctas"><a class="btn wa" href="{esc(href)}" data-cta="{ref}-whatsapp" target="_blank" rel="noopener">{WA_ICON}<span>{esc(label)}</span></a>'
            f'<a class="btn ghost" href="tel:{TEL}" data-cta="{ref}-call">Call {PHONE}</a></div>')

WA_ICON = '<svg class="ico" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path fill="currentColor" d="M12.04 2A9.9 9.9 0 0 0 3.45 16.86L2.05 22l5.25-1.38A9.9 9.9 0 1 0 12.04 2zm0 18.15a8.2 8.2 0 0 1-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.24 8.24 0 1 1 7 3.86zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.78.97-.14.17-.29.19-.54.06a6.7 6.7 0 0 1-3.37-2.95c-.14-.25-.02-.38.11-.51l.37-.43c.13-.15.17-.25.25-.42.08-.17.04-.31-.02-.43l-.77-1.85c-.2-.48-.41-.42-.56-.43h-.48a.92.92 0 0 0-.66.31c-.23.25-.87.85-.87 2.07s.89 2.4 1.02 2.57c.12.16 1.75 2.67 4.23 3.74 1.48.64 2.06.69 2.8.58.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.08.15-1.18-.06-.11-.23-.17-.48-.29z"/></svg>'

def kohden_block(r, ref="kohden"):
    """The 'Distributed in Singapore by Kohden' section (home, where-to-buy, contact, workshops)."""
    return f"""<section class="kohden reveal" aria-labelledby="kd-{ref}"><div class="kd-in">
<div><h2 id="kd-{ref}">Distributed in Singapore by Kohden</h2>
<p><a href="{KOHDEN}" target="_blank" rel="noopener">{KNAME}</a> is an authorised distributor of EXN lubricants in Singapore, alongside DENSO, MOON and Hyper Power.</p>
<dl class="kd-facts"><dt>Address</dt><dd>{esc(ADDR)}</dd><dt>Phone</dt><dd><a href="tel:{TEL}" data-cta="{ref}-call">{PHONE}</a></dd><dt>Email</dt><dd><a href="mailto:{EMAIL}" data-cta="{ref}-email">{EMAIL}</a></dd><dt>Hours</dt><dd>{HOURS}</dd></dl>
<p class="kd-links"><a href="{KOHDEN_EXN}" target="_blank" rel="noopener" data-cta="{ref}-exn-category">EXN range on kohden.com.sg</a><a href="{KOHDEN}" target="_blank" rel="noopener" data-cta="{ref}-site">kohden.com.sg</a><a href="{MAPS}" target="_blank" rel="noopener" data-cta="{ref}-map">Open in Google Maps</a></p></div>
{cta_buttons(r, ref)}</div></section>"""

def sister_block(r, ref="sister"):
    return f"""<section class="sister reveal" aria-labelledby="sis-{ref}"><h2 id="sis-{ref}">Also from Kohden</h2>
<ul><li><a href="{HYPER}" data-cta="{ref}-hyper-power"><b>Hyper Power</b><span>Sodium-ion and lithium LiFePO4 car batteries, 3-year warranty</span></a></li>
<li><a href="{CARKU}" data-cta="{ref}-carku"><b>Carku</b><span>Smart car battery with a Bluetooth app and one-touch jump start</span></a></li>
<li><a href="{KOHDEN}" target="_blank" rel="noopener" data-cta="{ref}-kohden"><b>kohden.com.sg</b><span>All Kohden brands: DENSO, EXN, MOON, Hyper Power</span></a></li></ul></section>"""

ORG_ID = SITE + "#kohden"
BRAND_ID = SITE + "#brand"
def org_schema():
    return {"@type": "Organization", "@id": ORG_ID, "name": KNAME, "url": KOHDEN,
            "description": "Authorised distributor of DENSO, EXN, MOON and Hyper Power in Singapore.",
            "telephone": PHONE, "email": EMAIL,
            "address": {"@type": "PostalAddress", "streetAddress": STREET, "addressLocality": "Singapore",
                        "postalCode": POST, "addressCountry": "SG"},
            "areaServed": {"@type": "Country", "name": "Singapore"},
            "brand": {"@id": BRAND_ID},
            "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "telephone": PHONE, "email": EMAIL,
                              "areaServed": "SG", "availableLanguage": "en",
                              "hoursAvailable": {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}}]}

def brand_schema():
    return {"@type": "Brand", "@id": BRAND_ID, "name": "EXN Lube", "slogan": "The Lubricant Expert", "logo": LOGO, "sameAs": list(SOCIAL.values())}

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
    graph = [brand_schema(), org_schema(), {"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": BRAND, "inLanguage": "en-SG", "publisher": {"@id": ORG_ID}}]
    if trail: graph.append(crumbs(trail))
    graph += schema or []
    # night-run articles carry their own Base44 hero (images/articles/<slug>.*): it is also og:image + twitter:image (HARD IMAGE GATE)
    own = isinstance(image, str) and image.startswith(SITE + "images/articles/")
    og, og_w, og_h = (image, 1200, 675) if own else (OG_IMG, 1200, 630)
    og_type = ("webp" if og.endswith(".webp") else "png" if og.endswith(".png") else "jpeg")
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    doc = f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#111214">
<link rel="preload" href="{r}fonts/barlow-condensed-800.woff2" as="font" type="font/woff2" crossorigin>
<link rel="icon" href="{r}favicon.ico" sizes="48x48">
<link rel="icon" href="{r}favicon.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{r}favicon.png">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="image/{og_type}">
<meta property="og:image:width" content="{og_w}">
<meta property="og:image:height" content="{og_h}">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og}">
<link rel="stylesheet" href="{r}exn.css?v={CSS_V}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar">
<a class="logo" href="{r}" aria-label="EXN Lube Singapore home"><img src="{LOGO_W}" alt="EXN Lube logo" width="150" height="42"></a>
<button class="menu" aria-label="Menu" aria-expanded="false">Menu</button>
<nav class="nav" aria-label="Main">{nav(r)}</nav>
<a class="btn wa hd-wa" href="{esc(WA_GENERAL)}" data-cta="header-whatsapp" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp</span></a>
</div></header>
<main id="main">
{crumb_html(trail or [], r)}
{body}
</main>
<footer class="foot"><div class="wrap cols">
<div><img src="{LOGO_W}" alt="EXN Lube" width="120" height="33" loading="lazy">
<p class="ft-lab">Singapore distributor</p><p><a href="{KOHDEN}" target="_blank" rel="noopener"><b>{KNAME}</b></a><br>{esc(ADDR)}</p>
<p><a href="tel:{TEL}" data-cta="footer-call">Call {PHONE}</a><br><a href="mailto:{EMAIL}" data-cta="footer-email">{EMAIL}</a><br>{HOURS}</p>
<a class="btn wa" href="{esc(WA_GENERAL)}" data-cta="footer-whatsapp" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp Kohden</span></a></div>
<div><p class="ft-lab">Products</p>{"".join(f'<a href="{r}products/{c["slug"]}/">{esc(c["short"])}</a>' for c in CATS)}</div>
<div><p class="ft-lab">EXN in Singapore</p><a href="{r}technology/molytech/">Molytech technology</a><a href="{r}workshops/">For workshops</a><a href="{r}where-to-buy/">Where to buy</a><a href="{r}about/">About EXN</a><a href="{r}articles/">Articles</a><a href="{r}contact/">Contact Kohden</a><a href="{r}privacy/">Privacy</a></div>
<div><p class="ft-lab">Also from Kohden</p><a href="{HYPER}" data-cta="footer-hyper-power">Hyper Power batteries</a><a href="{CARKU}" data-cta="footer-carku">Carku smart batteries</a><a href="{KOHDEN_EXN}" target="_blank" rel="noopener" data-cta="footer-exn-category">EXN on kohden.com.sg</a><a href="{KOHDEN}" target="_blank" rel="noopener">kohden.com.sg</a></div>
</div><p class="wrap small">EXN is a brand of {LEGAL[:-1] if LEGAL.endswith(".") else LEGAL}. Distributed in Singapore by <a href="{KOHDEN}" target="_blank" rel="noopener">{KNAME}</a>. Grades and specs as printed on EXN labels and listed by Kohden. Prices on request. &copy; 2026 EXN Lube Singapore. Preview site.</p></footer>
<div class="sticky" data-sticky><a class="btn wa" href="{esc(WA_GENERAL)}" data-cta="sticky-whatsapp" target="_blank" rel="noopener">{WA_ICON}<span>WhatsApp Kohden</span></a><a class="btn ghost" href="tel:{TEL}" data-cta="sticky-call">Call</a></div>
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
             f'<h3>{esc(label)}</h3><p>{esc(spec)}{(", " + esc(base[0].lower() + base[1:])) if base else ""}. Pack: {esc(pack)}</p>')
    if link: return f'<a class="pcard reveal" href="{link}">{inner}</a>'
    return f'<div class="pcard reveal">{inner}</div>'

def product_link(pid, r):
    for pp in PPAGES:
        if pid in pp["ids"]: return f'{r}products/{pp["slug"]}/'
    return None

# ------------------------------------------------------------------ pages
def home():
    r = ""
    cards = "".join(f'<a class="ccard reveal" href="products/{c["slug"]}/"><img src="{CAT_ICON[c["slug"]]}" alt="" width="56" height="56" loading="lazy"><h3>{esc(c["name"])}</h3><p>{esc(c["card"])}</p><span>See the range</span></a>' for c in CATS)
    feat = "".join(pcard(p, r, product_link(p[0], r)) for p in PRODUCTS if p[0] in ("hyb", "mr5w30", "mr0w20", "cm10w40", "cvtf", "dot4"))
    arts = article_cards(r, 3)
    faq = [("Where can I buy EXN engine oil in Singapore?", f"From {KNAME}, EXN's authorised distributor in Singapore, at {ADDR}. WhatsApp {WA_DISP} or call {PHONE}, Monday to Friday, 9am to 5pm."),
           ("Which EXN oils does Kohden list in Singapore?", "Extentios Hybrid 0W-16, Extentios Molyracing 0W-20, 5W-30, 5W-40 and 5W-50, Carios Molytech Nano 5W-30 and 10W-40, Atfios ATF and CVTF, and the +Care brake fluids, treatments, cleaners and X40 spray."),
           ("Can my workshop stock EXN?", "Yes. Kohden supplies workshops in Singapore. Send your workshop name and area on WhatsApp. See <a href=\"workshops/\">EXN for workshops</a>."),
           ("What is EXN Molytech?", "EXN's friction technology: nano particles that act like tiny ball bearings between metal surfaces to cut heat, wear and engine drag. See <a href=\"technology/molytech/\">how Molytech works</a>.")]
    body = f"""
<section class="hero"><img class="hero-img" src="{HERO}" alt="EXN Lube engine oil bottles" width="1280" height="537" fetchpriority="high">
<div class="wrap hero-txt"><h1>EXN engine oil in Singapore</h1>
<p class="lead">Fully synthetic and Molytech oils, sold here by Kohden.</p>
{cta_buttons(r, "hero")}
<p class="links"><a href="products/">See all EXN products</a></p></div></section>
<section class="wrap grades" aria-labelledby="gr-h"><h2 id="gr-h">Find your grade</h2>
<p>Your owner's manual names the grade. Match it to the EXN bottle.</p>
<ul class="glist">
<li><a href="products/extentios-hybrid-0w-16/"><b>0W-16</b><span>Extentios Hybrid, API SP, for hybrids</span></a></li>
<li><a href="products/extentios-molyracing/"><b>0W-20</b><span>Extentios Molyracing, ACEA A5/B5</span></a></li>
<li><a href="products/extentios-molyracing/"><b>5W-30</b><span>Molyracing (ACEA C3) or Carios Molytech Nano</span></a></li>
<li><a href="products/extentios-molyracing/"><b>5W-40</b><span>Extentios Molyracing, ACEA A3/B4, C3</span></a></li>
<li><a href="products/extentios-molyracing/"><b>5W-50</b><span>Extentios Molyracing, ACEA A3/B4, C3</span></a></li>
<li><a href="products/carios-molytech-nano/"><b>10W-40</b><span>Carios Molytech Nano, ACEA A3/B4</span></a></li>
</ul></section>
<div class="wrap">{kohden_block(r, "home-kohden")}</div>
<section class="wrap"><h2>Popular EXN oils in Singapore</h2><div class="pgrid">{feat}</div></section>
<section class="band"><div class="wrap split"><div class="reveal"><h2>Molytech: less friction, less heat, less drag</h2><p>Molytech is EXN's nano technology. Its particles act, in EXN's words, \"like billions of ball bearings\" between metal surfaces, turning sliding friction into rolling.</p><a class="btn ghost" href="technology/molytech/">How Molytech works</a></div><img class="reveal" src="{MOLY}" alt="EXN Molytech nano technology illustration" width="640" height="512" loading="lazy"></div></section>
<section class="wrap"><h2>The full EXN range</h2><div class="cgrid">{cards}</div></section>
<section class="wrap wband reveal"><h2>For Singapore workshops</h2><p>Stock EXN oils, gearbox fluids and +Care treatments, supplied by Kohden.</p>{cta_buttons(r, "home-workshop", "Workshop enquiry on WhatsApp", WA_WORKSHOP)}<p><a href="workshops/">EXN for workshops</a></p></section>
<section class="wrap"><h2>Oil questions, answered</h2><div class="agrid">{arts}</div></section>
<div class="wrap">{sister_block(r, "home-sister")}</div>
<div class="wrap">{faq_html(faq, r)}</div>
"""
    shell("", "EXN Engine Oil Singapore | Distributed by Kohden", "EXN engine oil in Singapore: Extentios Hybrid 0W-16, Molyracing 0W-20 to 5W-50, Carios Molytech Nano, ATF, CVTF and +Care. WhatsApp Kohden.",
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
<p class="small">Grades, specs and packs as printed on EXN labels and listed on the Kohden store. Kohden's Singapore store lists car engine oils, gearbox fluids and +Care. For motorcycle, diesel, industrial, marine and grease grades, ask Kohden what they can supply.</p>
{cta_buttons(r, "products")}</section>"""
    il = {"@type": "ItemList", "name": "EXN Lube product groups", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": c["name"], "url": SITE + f'products/{c["slug"]}/'} for i, c in enumerate(CATS)]}
    shell("products/", "EXN Products Singapore | Engine Oil, ATF, +Care", "All EXN products for Singapore: car engine oils, ATF, CVT fluid and +Care from Kohden, plus motorcycle, diesel, industrial, marine oils and grease.", body, [il], trail=trail)

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
    body = f"""<section class="wrap page"><h1>EXN {esc(pp["name"])}</h1><p class="tagline">{esc(pp["tag"])}</p>
<p class="answer">{esc(pp["answer"])}</p>
<div class="pgrid">{"".join(pcard(p, r) for p in ps)}</div>
<h2>Specifications</h2><div class="tbl"><table><thead><tr><th>Grade</th><th>Specification</th><th>Base oil</th><th>Pack</th></tr></thead><tbody>{rows}</tbody></table></div>
{pp["body"]}
<h2>Where to buy {esc(pp["name"])} in Singapore</h2><p>From Kohden, EXN\'s authorised Singapore distributor, at {esc(ADDR)}. See <a href="{r}where-to-buy/">where to buy EXN</a> or <a href="{KOHDEN_EXN}" target="_blank" rel="noopener">the EXN range on kohden.com.sg</a>.</p>
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
           ("Did EXN really drive 100 km without engine oil?", "EXN ran a demonstration in 2020: Carios Molytech was added to a Toyota Vios engine, the oil was flushed out and the car was driven about 100 km. EXN reports no scratches or damage. The video is on EXN's YouTube channel.")]
    benefits = ["Cleans out deposits in the piston", "Prevents sludge from clumping in the oil tank", "Forms a film layer that stops metal-to-metal friction and wear",
                "Works as an anti-foaming agent", "Holds the oil's viscosity across temperatures, lowering shear and extending the drain interval",
                "Nano particles spread into curved surfaces", "A tackifier helps the oil stick to metal while the engine runs",
                "Raises TBN to fight corrosion from combustion acids"]
    body = f"""<section class="wrap page"><h1>Molytech: how EXN's nano technology works</h1>
<p class="answer">Molytech is EXN's friction technology. It is based on a 60-atom sphere called a buckyball that looks like a soccer ball at atomic level. The nano particles act like billions of ball bearings that fill gaps in metal surfaces, turning sliding friction into rolling, which EXN says lowers heat, wear and engine drag.</p>
<img class="wide reveal" src="{MOLY}" alt="Molytech nano particles acting as ball bearings between metal surfaces" width="640" height="512" loading="lazy">
<h2>What Molytech does, step by step</h2>
<ol><li>Nano particles spread through the oil and settle into the tiny peaks and valleys of metal surfaces.</li><li>They make the surface more even at atomic level.</li><li>Moving parts roll over the particles instead of grinding against each other.</li><li>Less friction means less heat, which helps the oil last longer, and less engine drag, which helps fuel mileage.</li></ol>
<h2>The eight benefits EXN lists</h2><ul class="ticks">{"".join(f"<li>{esc(b)}</li>" for b in benefits)}</ul>
<h2>The 100 km "without engine oil" test</h2>
<p>In 2020 EXN added Carios Molytech to a Toyota Vios engine, flushed it out and drove about 100 km. EXN reports that the engine \"remained in excellent condition, with no scratches or damage\". <a href="https://www.youtube.com/watch?v=SZzY5Y4k5sw" rel="noopener">Watch the video on YouTube</a>. This is a demonstration of film strength, not advice: never drive without oil.</p>
<h2>Oils with Molytech in Singapore</h2><ul class="ticks"><li><a href="{r}products/carios-molytech-nano/">Carios Molytech Nano 5W-30 and 10W-40</a></li><li><a href="{r}products/extentios-molyracing/">Extentios Molyracing 0W-20 to 5W-50</a></li></ul><p>Both are listed by Kohden in Singapore.</p>
{cta_buttons(r, "molytech")}
{faq_html(faq, r)}</section>"""
    vid = {"@type": "VideoObject", "name": "EXN Lube: 100 km without engine oil (Carios Molytech)", "description": "EXN's 2020 demonstration driving a Toyota Vios about 100 km after flushing out the engine oil.",
           "thumbnailUrl": "https://i.ytimg.com/vi/SZzY5Y4k5sw/hqdefault.jpg", "contentUrl": "https://www.youtube.com/watch?v=SZzY5Y4k5sw", "uploadDate": "2020-01-01"}
    # OPEN: real upload date of the video; VideoObject left out until confirmed (uploadDate must be true)
    shell(path, "Molytech Nano Technology Explained | EXN Singapore", "How EXN Molytech works: buckyball nano particles act like ball bearings to cut friction, heat and drag. Benefits and the 100 km test.", body, [faq_schema(faq)], image=MOLY, trail=trail)

def about():
    path = "about/"
    r = "../"
    trail = [("Home", ""), ("About EXN", path)]
    body = f"""<section class="wrap page"><h1>About EXN Lube in Singapore</h1>
<p class="answer">EXN Lube makes engine oils, gearbox fluids, grease and the +Care car care series under the slogan \"The Lubricant Expert\". In Singapore, EXN is distributed by {KNAME} in Kaki Bukit, an authorised distributor of DENSO, EXN, MOON and Hyper Power.</p>
<img class="wide reveal" src="{COMPANY}" alt="EXN Lube company photo" width="451" height="297" style="width:auto;max-width:100%" loading="lazy">
<h2>EXN in Singapore</h2>
<div class="tbl"><table><tbody>
<tr><th>Brand</th><td>EXN Lube</td></tr><tr><th>Brand owner</th><td>{LEGAL}, Malaysia</td></tr><tr><th>Singapore distributor</th><td><a href="{KOHDEN}" target="_blank" rel="noopener">{KNAME}</a></td></tr>
<tr><th>Address</th><td>{esc(ADDR)}</td></tr><tr><th>Phone</th><td><a href="tel:{TEL}" data-cta="about-kohden-call">{PHONE}</a></td></tr><tr><th>Email</th><td><a href="mailto:{EMAIL}" data-cta="about-kohden-email">{EMAIL}</a></td></tr>
<tr><th>Hours</th><td>{HOURS}</td></tr><tr><th>Range in Singapore</th><td>Car engine oils, Atfios ATF and CVTF, +Care fluids and treatments, X40 spray (as listed on the Kohden store)</td></tr></tbody></table></div>
<h2>Where EXN comes from</h2>
<p>EXN is a Malaysian lubricant brand, owned by {LEGAL} and founded in 2015 in Petaling Jaya by Marc Ee. EXN says it now supplies more than 10 export markets. Singapore is one of them, served by {KNAME}.</p>
<h2>What EXN stands for</h2>
<ul class="ticks"><li><b>Lubricants.</b> \"Our focus is on lubricants and we provide solutions for all issues and applications in this field.\"</li><li><b>Value.</b> Technically advanced products that generate added value.</li><li><b>Technology.</b> <a href="{r}technology/molytech/">Molytech</a>, EXN's nano friction technology.</li></ul>
<blockquote>\"It's an honor to collaborate with a diverse range of industries, from automotive and heavy-duty to marine and industrial sectors... prioritizing the highest standards of quality, safety, and environmental responsibility.\"<cite>Marc Ee, Founder and CEO, EXN Lube</cite></blockquote>
{cta_buttons(r, "about")}
{sister_block(r, "about-sister")}</section>"""
    sch = [{"@type": "AboutPage", "url": SITE + path, "about": {"@id": BRAND_ID}}]
    shell(path, "About EXN Lube Singapore | Distributed by Kohden", f"EXN Lube in Singapore: engine oils, ATF and +Care from {KNAME}, EXN's authorised distributor in Kaki Bukit.", body, sch, image=COMPANY, trail=trail)

def redirect_stub(path, target, title):
    """Old Malaysia-version URL kept on the server (the Bridge cannot delete): sends visitors to the Singapore page."""
    depth = path.count("/")
    r = rel(depth)
    doc = f"""<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><title>{esc(title)}</title>
<meta name="robots" content="noindex, nofollow"><link rel="canonical" href="{SITE}{target}">
<meta http-equiv="refresh" content="0; url={r}{target}"><meta name="viewport" content="width=device-width, initial-scale=1"></head>
<body><p><a href="{r}{target}">{esc(title)}</a></p></body></html>
"""
    out = os.path.join(OUT, path, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: f.write(doc)

def motorsport():
    redirect_stub("motorsport/", "", "EXN Lube Singapore")

def distributors():
    redirect_stub("distributors/", "workshops/", "EXN for Singapore workshops")

def workshops():
    path = "workshops/"
    r = "../"
    trail = [("Home", ""), ("For workshops", path)]
    faq = [("How does a Singapore workshop stock EXN?", f"Through {KNAME}, EXN's authorised distributor in Singapore. Send your workshop name, area and contact person on WhatsApp {WA_DISP}, or call {PHONE}."),
           ("Which EXN products can a workshop get in Singapore?", "Kohden's store lists the car engine oils (Extentios Hybrid, Extentios Molyracing, Carios Molytech Nano), Atfios ATF and CVTF, and the +Care fluids, treatments, cleaners and X40 spray."),
           ("What about trade prices?", "Trade terms are on request from Kohden.")]
    body = f"""<section class="wrap page"><h1>EXN oils for Singapore workshops</h1>
<p class="answer">Workshops in Singapore can stock EXN engine oils, gearbox fluids and +Care treatments through {KNAME}, EXN's authorised distributor. Every EXN label prints the viscosity and the API and ACEA ratings, so your team can match the owner's manual at the counter.</p>
<ul class="ticks"><li><b>Grades for most cars on the road</b>: 0W-16, 0W-20, 5W-30, 5W-40, 5W-50 and 10W-40.</li><li><b>Gearbox fluids</b>: Atfios ATF and CVTF, both fully synthetic, 4L.</li><li><b>+Care add-ons</b>: DOT 4 and DOT 5.1 brake fluid, power steering fluid, ATF and CVT treatments, injector cleaners, engine flush.</li><li><b>One supplier</b>: Kohden also distributes DENSO, MOON and Hyper Power.</li></ul>
{cta_buttons(r, "workshops", "Workshop enquiry on WhatsApp", WA_WORKSHOP)}
<p class="small">Trade terms on request.</p>
{kohden_block(r, "workshops-kohden")}
{faq_html(faq, r)}
{sister_block(r, "workshops-sister")}</section>"""
    shell(path, "Stock EXN Oil in Your Workshop | Singapore", "Singapore workshops can stock EXN engine oils, Atfios ATF and CVTF and +Care treatments through Kohden, EXN's authorised distributor.", body, [faq_schema(faq)], trail=trail)

def where_to_buy():
    path = "where-to-buy/"
    r = "../"
    trail = [("Home", ""), ("Where to buy", path)]
    faq = [("Where can I buy EXN oil in Singapore?", f"From {KNAME}, {ADDR}. Kohden lists itself as an authorised distributor of EXN. Phone {PHONE}."),
           ("Can I see the EXN range online?", f"Yes, Kohden lists the EXN range on its own website at kohden.com.sg."),
           ("Is there a list of workshops that use EXN?", "Not yet. Ask Kohden on WhatsApp which workshop near you can do the oil change.")]
    body = f"""<section class="wrap page"><h1>Where to buy EXN oil in Singapore</h1>
<p class="answer">In Singapore, EXN Lube is sold by {KNAME}, an authorised EXN distributor at {esc(ADDR)}. WhatsApp {WA_DISP} or call {PHONE}. Office hours: {HOURS}</p>
{kohden_block(r, "wtb-kohden")}
<h2>Workshops</h2><p>A list of Singapore workshops that use EXN is not published yet. Kohden can tell you which workshop near you stocks your grade. Workshop owners: see <a href="{r}workshops/">EXN for workshops</a>.</p>
{faq_html(faq, r)}</section>"""
    shell(path, "Where to Buy EXN Oil in Singapore | Kohden", f"Buy EXN engine oil, ATF and +Care in Singapore from Kohden, the authorised EXN distributor at 7 Kaki Bukit Road 1. Call {PHONE}.", body, [faq_schema(faq)], trail=trail)

def contact():
    path = "contact/"
    r = "../"
    trail = [("Home", ""), ("Contact Kohden", path)]
    body = f"""<section class="wrap page"><h1>Contact Kohden for EXN in Singapore</h1>
<p class="answer">For EXN oils in Singapore, contact {KNAME} at {esc(ADDR)}. WhatsApp {WA_DISP}, call {PHONE} or email {EMAIL}. {HOURS}</p>
{kohden_block(r, "contact-kohden")}
<p class="small">For EXN brand questions outside Singapore, see EXN's own channels: {", ".join(f'<a href="{u}" rel="noopener">{n}</a>' for n, u in SOCIAL.items())}.</p></section>"""
    sch = [{"@type": "ContactPage", "url": SITE + path, "about": {"@id": ORG_ID}}]
    shell(path, "Contact Kohden | EXN Lube Singapore", f"Contact Kohden for EXN oil in Singapore: 7 Kaki Bukit Road 1, Eunos Technolink. Call {PHONE}. Monday to Friday, 9am to 5pm.", body, sch, trail=trail)

def privacy():
    path = "privacy/"
    trail = [("Home", ""), ("Privacy", path)]
    body = f"""<section class="wrap page"><h1>Privacy notice</h1>
<p>This notice explains how personal data is handled on this website, in line with Singapore's Personal Data Protection Act 2012 (PDPA).</p>
<h2>What we collect</h2><p>This website has no forms and does not ask for personal data. If you WhatsApp, call or email Kohden, Kohden keeps what you send so they can reply.</p>
<h2>Button taps</h2><p>When you tap a call, email or WhatsApp button, we count the tap with the page name, device type and the site that referred you. We do not record your IP address or contact details.</p>
<h2>Contact</h2><p>Questions about your data: <a href="mailto:{EMAIL}" data-cta="privacy-email">{EMAIL}</a>, or call <a href="tel:{TEL}" data-cta="privacy-call">{PHONE}</a>.</p></section>"""
    shell(path, "Privacy Notice | EXN Lube Singapore", "How personal data is handled on the EXN Lube Singapore website under Singapore's PDPA 2012.", body, [], trail=trail)

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
        a["img"] = (SITE + a["hero"]) if a.get("hero") else imgs.get(a["slug"], HERO)
        out += f'<a class="acard reveal" href="{r}articles/{a["slug"]}/"><img src="{a["img"]}" alt="" width="300" height="200" loading="lazy"><h3>{esc(a["h1"])}</h3><p>{esc(a["desc"])}</p></a>'
    return out

def human_date(d):
    import datetime
    x = datetime.date.fromisoformat(d)
    return f"{x.day} {x.strftime('%B %Y')}"

def articles():
    r = "../"
    trail = [("Home", ""), ("Articles", "articles/")]
    body = f"""<section class="wrap page"><h1>Engine oil and lubricant articles</h1>
<p class="answer">Plain answers to the oil questions Singapore drivers and workshops ask most: which grade a hybrid needs, how to read an oil label, ATF vs CVT fluid, fully synthetic vs semi-synthetic, and DOT 4 vs DOT 5.1 brake fluid.</p>
<div class="agrid">{article_cards(r)}</div></section>"""
    shell("articles/", "Engine Oil Guides | EXN Lube Singapore", "EXN Lube guides: hybrid engine oil, reading oil labels, ATF vs CVT fluid, synthetic vs semi-synthetic oil and brake fluid types.", body, [], trail=trail)
    for a in ARTS:
        path = f'articles/{a["slug"]}/'
        rr = "../../"
        t2 = trail + [(a["h1"], path)]
        owner = a["owner"].strip("/") + "/"
        oname = next((c["short"] for c in CATS if owner.endswith(c["slug"] + "/")), None) or next((p["name"] for p in PPAGES if owner.endswith(p["slug"] + "/")), "EXN products")
        body = f"""<article class="wrap page post"><h1>{esc(a["h1"])}</h1>
<p class="meta">EXN Lube Singapore. Updated <time datetime="{a.get("updated", a["date"])}">{human_date(a.get("updated", a["date"]))}</time></p>
<img class="wide" src="{a["img"]}" alt="{esc(a.get("hero_alt") or a["h1"])}" width="{1200 if a.get("hero") else 800}" height="{675 if a.get("hero") else 500}" fetchpriority="high">
{a["body_html"].replace("<table", "<div class=\"tbl\"><table").replace("</table>", "</table></div>")}
<div class="ctaband"><p>Looking for the right EXN product? See <a href="{rr}{owner}">{esc(oname)}</a> or ask Kohden, EXN\'s Singapore distributor.</p>{cta_buttons(rr, "article-" + a["slug"])}</div>
{faq_html(a["faq"], rr)}</article>"""
        art = {"@type": "Article", "headline": a["h1"], "description": a["desc"], "datePublished": a["date"], "dateModified": a.get("updated", a["date"]), "inLanguage": "en-SG",
               "image": a["img"], "author": {"@type": "Organization", "name": "EXN Lube Singapore", "url": SITE + "about/"},
               "publisher": {"@id": ORG_ID}, "mainEntityOfPage": SITE + path}
        shell(path, a["title"], a["desc"], body, [art, faq_schema(a["faq"])], image=a["img"], trail=t2, ogtype="article")

def notfound():
    body = f'<section class="wrap page"><h1>Page not found</h1><p>The page you asked for is not here. Try <a href="{SITE}">the EXN Lube Singapore home page</a>, <a href="{SITE}products/">all products</a> or <a href="{SITE}contact/">contact Kohden</a>.</p></section>'
    shell("404.html", "Page not found | EXN Lube Singapore", "This page could not be found.", body, [])

# ------------------------------------------------------------------ assets + crawl files
CSS = """
@font-face{font-family:"Barlow Condensed";src:url(fonts/barlow-condensed-700.woff2) format("woff2");font-weight:700;font-display:swap}
@font-face{font-family:"Barlow Condensed";src:url(fonts/barlow-condensed-800.woff2) format("woff2");font-weight:800;font-display:swap}
@font-face{font-family:"Public Sans";src:url(fonts/public-sans-var.woff2) format("woff2");font-weight:100 900;font-display:swap}
:root{--ink:#111214;--bg:#ffffff;--label:#f2f2f0;--line:#dcdcd8;--red:#d71920;--red2:#a80f15;--mute:#55585e;--wa:#1a8d4a;--wa2:#14703a;--disp:"Barlow Condensed","Arial Narrow",sans-serif}
*{box-sizing:border-box}html,body{overflow-x:clip}
body{margin:0;background:var(--bg);color:var(--ink);font-family:"Public Sans",sans-serif;line-height:1.6;font-size:17px;-webkit-tap-highlight-color:rgba(215,25,32,.18);caret-color:var(--red)}
::selection{background:var(--red);color:#fff}
img{max-width:100%;height:auto}a{color:var(--red2);text-underline-offset:3px}
:focus-visible{outline:3px solid var(--red);outline-offset:2px}
.skip{position:absolute;left:-999px;top:0;background:#fff;padding:8px 12px;z-index:50}.skip:focus{left:8px}
.wrap{max-width:1140px;margin:0 auto;padding:0 16px}
h1,h2,h3{font-family:var(--disp);font-weight:800;line-height:1.05;letter-spacing:-.01em;text-wrap:balance}
p{text-wrap:pretty}
.top{background:var(--ink);position:sticky;top:0;z-index:20;border-bottom:4px solid var(--red)}.bar{display:flex;align-items:center;gap:14px;min-height:60px}
.logo{margin-right:auto}.logo img{height:32px;width:auto;display:block}.nav{display:flex;gap:18px}.nav a{color:#fff;text-decoration:none;font-weight:600;font-size:15px}.nav a:hover,.nav a:focus-visible{color:#ff6b70}
.menu{display:none;background:none;border:1px solid #555;color:#fff;border-radius:6px;padding:0 14px;min-height:44px;font:inherit;touch-action:manipulation}
.hd-wa{padding:0 14px;min-height:40px;font-size:15px}
@media(max-width:900px){.menu{display:block;order:3}.hd-wa{order:2}.nav{display:none;position:absolute;left:0;right:0;top:64px;background:var(--ink);flex-direction:column;padding:8px 16px 18px}.nav.open{display:flex}.nav a{padding:12px 0;font-size:19px;border-bottom:1px solid #2a2b2e}}
@media(max-width:380px){.hd-wa span{display:none}}
.crumbs{max-width:1140px;margin:14px auto 0;padding:0 16px;font-size:14px;color:var(--mute)}.crumbs a{color:var(--mute)}
.hero{position:relative;background:var(--ink);color:#fff;overflow:hidden;min-height:min(78svh,620px);display:flex;align-items:flex-end}
.hero-img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.5;animation:pour 1.1s ease-out both}
@keyframes pour{from{opacity:0;transform:scale(1.06)}to{opacity:.5;transform:none}}
.hero:after{content:"";position:absolute;inset:auto 0 0 0;height:60%;background:linear-gradient(transparent,rgba(17,18,20,.92))}
.hero-txt{position:relative;z-index:1;padding:40px 16px 34px;width:100%}.hero h1{font-size:clamp(46px,9vw,92px);margin:0 0 .15em;max-width:12ch;text-transform:uppercase;line-height:.95}
.lead{font-size:19px;max-width:34ch;color:#f0f0f0;margin:0}.hero .links a{color:#fff}
.ctas{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:48px;background:var(--red);color:#fff;text-decoration:none;font-weight:700;padding:0 20px;border-radius:6px;touch-action:manipulation;transition:background .15s,transform .15s}
.btn:active{transform:scale(.97)}.btn.wa{background:var(--wa)}.btn.wa:hover{background:var(--wa2)}.btn.ghost{background:transparent;border:2px solid currentColor;color:inherit}
.page .btn.ghost,.wband .btn.ghost,.kohden .btn.ghost{color:var(--ink)}
@media(max-width:600px){.ctas .btn{flex:1 1 100%}}
.ico{flex:none}
h2{font-size:clamp(30px,4.4vw,44px);margin:1.5em 0 .45em}h3{font-size:22px}
.grades h2{margin-top:1.2em}.glist{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));border-top:2px solid var(--ink)}
.glist a{display:flex;align-items:baseline;gap:14px;padding:14px 4px;border-bottom:1px solid var(--line);text-decoration:none;color:var(--ink);min-height:56px}
.glist b{font-family:var(--disp);font-weight:800;font-size:34px;color:var(--red);min-width:3.2em;white-space:nowrap;font-variant-numeric:tabular-nums}.glist span{color:var(--mute);font-size:15px}
.cgrid,.pgrid,.agrid{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}
.ccard,.pcard,.acard{display:block;background:#fff;border:1px solid var(--line);border-radius:4px;padding:16px;color:inherit;text-decoration:none;transition:border-color .15s}
.ccard:hover,.pcard:hover,.acard:hover,.ccard:focus-visible,.pcard:focus-visible,.acard:focus-visible{border-color:var(--red)}
.ccard h3,.pcard h3,.acard h3{margin:.4em 0 .2em}.ccard p,.pcard p,.acard p{margin:0;color:var(--mute);font-size:15px}.ccard span{display:inline-block;margin-top:10px;color:var(--red2);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.pcard img{aspect-ratio:1;object-fit:contain;width:100%;background:var(--label);border-radius:2px}.acard img{aspect-ratio:3/2;object-fit:contain;width:100%;background:var(--label);border-radius:2px}
.band{background:var(--label);margin:40px 0;padding:6px 0 30px}.split{display:grid;grid-template-columns:1.1fr .9fr;gap:28px;align-items:center}.split img{width:100%}.split>*,.cgrid>*,.pgrid>*,.agrid>*{min-width:0}@media(max-width:800px){.split{grid-template-columns:1fr}}
.kohden{background:var(--ink);color:#fff;border-radius:6px;padding:22px 20px;margin:36px 0}.kohden h2{margin:0 0 .3em;color:#fff}.kohden a{color:#fff}
.kd-in{display:grid;gap:10px}@media(min-width:900px){.kd-in{grid-template-columns:1.6fr 1fr;align-items:end}}
.kd-facts{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;margin:14px 0}.kd-facts dt{font-family:var(--disp);font-weight:700;font-size:18px;color:#ff8a8e}.kd-facts dd{margin:0}
.kd-links{display:flex;flex-wrap:wrap;gap:6px 18px}.kd-links a{display:inline-flex;align-items:center;min-height:44px}
.kohden .btn.ghost{color:#fff}
.wband{border:2px solid var(--ink);border-radius:6px;padding:4px 20px 14px;margin:40px auto}
.sister{margin:36px 0}.sister h2{margin-bottom:.3em}.sister ul{list-style:none;padding:0;margin:0;display:grid;gap:10px;grid-template-columns:repeat(auto-fill,minmax(260px,1fr))}
.sister a{display:block;padding:14px 16px;border:1px solid var(--line);border-top:4px solid var(--ink);border-radius:4px;text-decoration:none;color:var(--ink);min-height:44px}.sister b{display:block;font-family:var(--disp);font-size:24px}.sister span{color:var(--mute);font-size:15px}
.page{padding-bottom:40px}.page h1{font-size:clamp(38px,6vw,64px);margin:.4em 0 .3em}
.tagline{font-family:var(--disp);font-weight:700;font-size:22px;color:var(--red2);margin:0}
.answer{font-size:19px;background:var(--label);border-top:2px solid var(--ink);padding:14px 18px;margin:0 0 18px}
.phead{display:flex;align-items:center;gap:14px}.wide{width:100%;border-radius:4px;margin:12px 0;background:var(--label);object-fit:contain;max-height:460px}
.tbl{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:15px;margin:8px 0;font-variant-numeric:tabular-nums}th,td{border-bottom:1px solid var(--line);padding:10px 8px;text-align:left;vertical-align:top}thead th{background:var(--ink);color:#fff;font-family:var(--disp);font-size:18px;letter-spacing:.02em}
tbody th{width:32%;color:var(--mute);font-weight:600}
.ticks{padding-left:0;list-style:none}.ticks li{padding-left:28px;position:relative;margin:8px 0}.ticks li:before{content:"";position:absolute;left:4px;top:.55em;width:12px;height:7px;border-left:3px solid var(--red);border-bottom:3px solid var(--red);transform:rotate(-45deg)}
blockquote{margin:24px 0;padding:18px 22px;background:var(--label);font-size:18px}cite{display:block;margin-top:8px;font-style:normal;color:var(--mute);font-size:15px}
.faq details{border-bottom:1px solid var(--line);padding:12px 2px}.faq summary{cursor:pointer;font-weight:700;min-height:32px}.faq p{margin:.6em 0 0}
.ctaband{background:var(--ink);color:#fff;border-radius:6px;padding:20px 22px;margin:36px auto}.ctaband a{color:#fff}.ctaband .btn.ghost{color:#fff}
.more a{margin-right:12px;display:inline-block;min-height:32px}.meta{color:var(--mute);font-size:14px}
.foot{background:var(--ink);color:#d4d4d6;margin-top:40px;padding:34px 0 96px;font-size:15px}.foot .cols{display:grid;grid-template-columns:1.4fr 1fr 1fr 1fr;gap:22px}.foot a{color:#fff;display:block;padding:5px 0;text-decoration:none}.foot p a{display:inline}.foot .btn{display:inline-flex;margin-top:4px}
.ft-lab{font-family:var(--disp);font-weight:700;font-size:19px;color:#ff8a8e;margin:14px 0 4px}
@media(max-width:800px){.foot .cols{grid-template-columns:1fr 1fr}.foot .cols>div:first-child{grid-column:1/-1}}.small{font-size:13px;color:var(--mute)}.foot .small{color:#a5a5aa;margin-top:22px}.foot .small a{display:inline;color:#d4d4d6;text-decoration:underline}
.sticky{position:fixed;left:0;right:0;bottom:0;z-index:30;display:flex;gap:8px;padding:8px 12px calc(8px + env(safe-area-inset-bottom));background:rgba(17,18,20,.96);transform:translateY(110%);transition:transform .25s ease-out}
.sticky.on{transform:none}.sticky .btn{flex:1}.sticky .btn.ghost{flex:0 0 96px;color:#fff}
@media(min-width:900px){.sticky{display:none}.foot{padding-bottom:18px}}
.reveal{opacity:1;transform:none}.js .reveal{opacity:0;transform:translateY(12px);transition:opacity .4s ease-out,transform .4s ease-out}.js .reveal.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.js .reveal{opacity:1;transform:none}.hero-img{opacity:.5}}
"""

JS = """(function(){var d=document.documentElement;
if(!window.matchMedia('(prefers-reduced-motion: reduce)').matches&&'IntersectionObserver' in window){d.classList.add('js');
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});
document.querySelectorAll('.reveal').forEach(function(el){io.observe(el)});setTimeout(function(){document.querySelectorAll('.reveal').forEach(function(el){el.classList.add('in')})},2500)}
var st=document.querySelector('[data-sticky]'),hc=document.querySelector('.hero .ctas,.page .ctas');if(st){if(hc&&'IntersectionObserver' in window){new IntersectionObserver(function(es){st.classList.toggle('on',!es[0].isIntersecting)}).observe(hc)}else st.classList.add('on')}
var m=document.querySelector('.menu'),n=document.querySelector('.nav');if(m&&n)m.addEventListener('click',function(){var o=n.classList.toggle('open');m.setAttribute('aria-expanded',o)});
/* carousel standard: auto-slides, keeps sliding on scroll, pauses only while held/dragged, restarts ~2s after release */
document.querySelectorAll('.carousel[data-auto]').forEach(function(c){var held=false,t=null;
function step(){if(held)return;var w=c.firstElementChild?c.firstElementChild.getBoundingClientRect().width+12:300;
if(c.scrollLeft+c.clientWidth>=c.scrollWidth-4)c.scrollTo({left:0,behavior:'smooth'});else c.scrollBy({left:w,behavior:'smooth'})}
var iv=setInterval(step,3200);function down(){held=true;clearTimeout(t)}function up(){clearTimeout(t);t=setTimeout(function(){held=false},2000)}
c.addEventListener('pointerdown',down);c.addEventListener('touchstart',down,{passive:true});c.addEventListener('pointerup',up);c.addEventListener('touchend',up);c.addEventListener('pointercancel',up)})})();
"""

ROBOTS = f"""# Singapore preview: pages carry noindex. Real domain rules go in at go-live.
User-agent: *
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
             f"> EXN Lube engine oils, gearbox fluids and +Care car care products for Singapore drivers and workshops, distributed in Singapore by {KNAME} "
             "(authorised distributor of DENSO, EXN, MOON and Hyper Power). Preview site.", "",
             "## Key facts",
             f"- Singapore distributor: {KNAME}, {ADDR}", f"- Phone: {PHONE}; email {EMAIL}; WhatsApp +65 8603 0355",
             f"- Hours: {HOURS}", f"- EXN range on Kohden: {KOHDEN_EXN}",
             "- Technology: Molytech (buckyball nano particles that act like ball bearings to cut friction, heat and drag)",
             f"- Sister Kohden brands: Hyper Power {HYPER} ; Carku {CARKU}", "",
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
    if os.path.exists(os.path.join(HERE, "og-image.jpg")): shutil.copy(os.path.join(HERE, "og-image.jpg"), os.path.join(OUT, "og-image.jpg"))
    if os.path.exists(os.path.join(HERE, "favicon.png")):
        for fn in ("favicon.png", "favicon.ico"): shutil.copy(os.path.join(HERE, fn), os.path.join(OUT, fn))
    shutil.copytree(os.path.join(HERE, "images", "brand"), os.path.join(OUT, "images", "brand"))
    os.makedirs(os.path.join(OUT, "fonts"))
    for fn in ("barlow-condensed-700.woff2", "barlow-condensed-800.woff2", "public-sans-var.woff2"):
        shutil.copy(os.path.join(HERE, "fonts", fn), os.path.join(OUT, "fonts", fn))
    load_articles()
    home(); products_index()
    for c in CATS: cat_page(c)
    for pp in PPAGES: ppage(pp)
    molytech(); about(); motorsport(); distributors(); workshops(); where_to_buy(); contact(); articles(); privacy(); notfound()
    open(os.path.join(OUT, "robots.txt"), "w").write(ROBOTS)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(sitemap())
    open(os.path.join(OUT, "llms.txt"), "w").write(llms())
    open(os.path.join(HERE, "htaccess-golive.txt"), "w").write(HTACCESS)
    print(f"built {len(PAGES)} pages -> {OUT}")

if __name__ == "__main__":
    main()
