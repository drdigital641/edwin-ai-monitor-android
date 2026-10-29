#!/usr/bin/env python3
"""Mega Power Engineering & Trading - interactive website mockup (Page One Singapore, 29 Oct 2026).

Run:  python3 build.py OUT_DIR
Brief: drdigital641/edwin-ai-context handoffs/2026-10-29-mega-power-website-mockup.md
Facts: megapower.com.sg public pages read 29 Oct 2026 (FACTS.md). 13 public catalogue listings only; nothing invented.
Preview: pageonesingapore.com/preview/mega-power/ (hidden by the parent preview/.htaccess header; no noindex in pages).
Product and category URLs keep the current site's paths (/our-products/<cat>/<slug>.html) so old links keep working.
"""
import html, json, sys, re, datetime, hashlib, shutil
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE / "site")
BASE = "https://www.megapower.com.sg"
TODAY = datetime.date.today().isoformat()
READ = "29 Oct 2026"
BRAND = "Mega Power"
LEGAL = "Mega Power Engineering & Trading"
TEL_MAIN = "+65 6842 3389"; TEL_MAIN_H = "+6568423389"
EMAIL = "enquiry@megapower.com.sg"
LOGO = "https://www.megapower.com.sg/pub/media/logo/stores/1/Megapower_logo.png"
IMG = "https://www.megapower.com.sg/pub/media/catalog/product/cache/c30325cf7a1fe493f9dba056550e5705/"
OLD = "https://www.megapower.com.sg/"
e = lambda s: html.escape(str(s), quote=True)

BRANCHES = [
 ("Ang Mo Kio", "5025 Ang Mo Kio Industrial Park 2, #01-55/57, Singapore 569528", "6482 3389", "6481 1187"),
 ("Toh Guan", "21 Toh Guan Road East, #01-33 Toh Guan Centre, Singapore 608609", "6766 3389", "6316 2464"),
 ("Kaki Bukit", "13 Kaki Bukit Road 4, #01-27 Bartley Biz Centre, Singapore 417807", "6385 3389", "6385 3329"),
 ("Soon Lee", "5 Soon Lee Street, #01-26 Pioneer Point, Singapore 627607", "6252 3389", "6275 3389"),
]

# slug, name, short line, icon (existing megapower.com.sg categories; slugs = current URLs)
CATS = [
 ("compressors", "Compressors", "The pump that drives the A/C system", "comp"),
 ("condenser", "Condensers", "Releases heat at the front of the car", "cond"),
 ("cooling-coil", "Cooling Coils", "Evaporators inside the dashboard", "coil"),
 ("fans-and-motors", "Fans & Motors", "Blower motors and cooling fans", "fan"),
 ("filters", "Filters", "Filters for the A/C system", "filt"),
 ("valves", "Valves", "Expansion and control valves", "valve"),
 ("driers", "Driers", "Receiver driers and desiccant", "drier"),
 ("accessories", "Accessories", "Fittings and small parts", "acc"),
 ("equipment", "Equipment", "Workshop A/C tools", "equip"),
 ("machines", "Machines", "A/C service machines", "mach"),
 ("compressor-oil", "Compressor Oil", "PAG and other A/C oils", "oil"),
 ("refrigerant", "Refrigerant", "R134a and R1234YF gas", "gas"),
]
CAT = {c[0]: c for c in CATS}

def R(n, t, v=True): return {"n": n, "t": t, "v": v}
# Every value below is copied from the public product page (29 Oct 2026). "refs" type = label used on the current site.
PRODUCTS = [
 dict(id="mp-0001", cat="compressors", slug="volkswagen-golf-5-y13-compressor", orig="VOLKSWAGEN GOLF 5 Y13 COMPRESSOR",
      name="Volkswagen Golf 5 (Y13) A/C Compressor - Denso Europe", make="Volkswagen", model="Golf 5", codes=["Y13"], brand="Denso Europe",
      country="Germany", gas="R134", oil="PAG-46", refs=[R("DCP32060", "OEM number (as listed)")], img="c/m/cmvlgo-03a-n1-eu_1_test.jpg", years=[]),
 dict(id="mp-0002", cat="compressors", slug="volkswagen-golf-5-compressor", orig="VOLKSWAGEN GOLF 5 COMPRESSOR",
      name="Volkswagen Golf 5 A/C Compressor - Denso Japan", make="Volkswagen", model="Golf 5", codes=[], brand="Denso Japan",
      country="Japan", gas="R134", oil="PAG-46", refs=[R("437100-8011", "OEM number (as listed)")], img="c/m/cmvlgo-01e-n1-jp_2_wm.jpg", years=[]),
 dict(id="mp-0003", cat="compressors", slug="mercedes-benz-246-compressor", orig="MERCEDES-BENZ 246 COMPRESSOR",
      name="Mercedes-Benz 246 A/C Compressor - Sanden Europe", make="Mercedes-Benz", model="246", codes=["MB246", "246"], brand="Sanden Europe",
      country="France", gas="R1234YF", oil="PAG-46", refs=[R("8835U", "OEM number (as listed)")], img="c/m/cmmb246-01a-s3-eu_1_wm.jpg", years=[]),
 dict(id="mp-0004", cat="compressors", slug="mercedes-benz-w205-compressor", orig="MERCEDES BENZ W205 COMPRESSOR",
      name="Mercedes-Benz W205 A/C Compressor - Sanden Europe", make="Mercedes-Benz", model="W205", codes=["W205"], brand="Sanden Europe",
      country="France", gas="R1234YF", oil="PAG-46", refs=[R("1787", "OEM number (as listed)")], img="c/m/cmmb205-04e-s3-eu_1_wm.jpg", years=[]),
 dict(id="mp-0005", cat="compressors", slug="range-rover-evoque-2-2-d-compressor", orig="RANGE ROVER EVOQUE 2.2 (D) COMPRESSOR",
      name="Range Rover Evoque 2.2 (D) A/C Compressor - Behr Europe", make="Range Rover", model="Evoque 2.2 (D)", codes=["EVOQUE"], brand="Behr Europe",
      country="Hungary", gas="R134", oil="Premium PAG", refs=[R("8FK 351 339-441", "OEM number (as listed)")], img="c/m/cmlaro-14a-b1-eu_2_wm.jpg", years=[]),
 dict(id="mp-0006", cat="compressors", slug="range-rover-evoque-compressor", orig="RANGE ROVER EVOQUE COMPRESSOR",
      name="Range Rover Evoque A/C Compressor - Behr Europe", make="Range Rover", model="Evoque", codes=["EVOQUE"], brand="Behr Europe",
      country="Hungary", gas="R134", oil="Premium PAG", refs=[R("8FK 351 334-431", "OEM number (as listed)")], img="c/m/cmlaro-10a-b1-eu_2_-_wm_1.jpg", years=[]),
 dict(id="mp-0007", cat="compressors", slug="bmw-x5-f15-hybrid-compressor", orig="BMW X5 F15 HYBRID COMPRESSOR",
      name="BMW X5 F15 Hybrid A/C Compressor - Sanden Europe", make="BMW", model="X5 F15 Hybrid", codes=["X5", "F15"], brand="Sanden Europe",
      country="France", gas="R134 and R1234YF", oil="PAG-46", refs=[R("SHS-33H4167", "OEM number (as listed)")], img="c/m/cmbmx5-06a-s3-eu_1_wm.jpg", years=[]),
 dict(id="mp-0008", cat="compressors", slug="bmw-2-series-f45-46-compressor", orig="BMW 2 SERIES F45/46 COMPRESSOR",
      name="BMW 2 Series F45/F46 A/C Compressor - Sanden Europe", make="BMW", model="2 Series F45/F46", codes=["F45", "F46"], brand="Sanden Europe",
      country="France", gas="R1234YF", oil="PAG-46", refs=[R("8730R", "OEM number (as listed)")], img="c/m/cmbm218-01a-s3-eu_1_wm.jpg", years=[]),
 dict(id="mp-0009", cat="compressors", slug="porsche-boxster-718-compressor-sanden-europe", orig="PORSCHE BOXSTER 718 COMPRESSOR",
      name="Porsche Boxster 718 A/C Compressor - Sanden Europe", make="Porsche", model="Boxster 718", codes=["718"], brand="Sanden Europe",
      country="France", gas="R134a and R1234YF", oil="PAG-46", refs=[R("9P1 820 803B", "OEM number (as listed)")], img="c/o/comp_sample_-_1.jpg", years=[],
      staff_note="Current photo file is named 'comp_sample': check it shows this exact compressor."),
 dict(id="mp-0010", cat="condenser", slug="audi-q7-y2015-original-condenser-with-desiccant", orig="AUDI Q7 Y2015 ORIGINAL CONDENSER WITH DESICCANT",
      name="Audi Q7 (2015) Original A/C Condenser with Desiccant", make="Audi", model="Q7", codes=["Q7"], brand="Original (OE)",
      country="", gas="", oil="", refs=[R("4M0 816 421B", "OEM number (as listed)")], img="c/d/cdauq7-02a-o1_1_wm.jpg", years=[2015]),
 dict(id="mp-0011", cat="condenser", slug="audi-a4-y15-condenser-with-desiccant-and-valve", orig="AUDI A4 Y15 CONDENSER WITH DESICCANT AND VALVE",
      name="Audi A4 (2015) A/C Condenser with Desiccant and Valve - Valeo", make="Audi", model="A4", codes=["A4"], brand="Valeo",
      country="", gas="", oil="", refs=[R("8W0 816 421", "OEM number (as listed)")], img="c/d/cdaua4-05a-v1-tw_1_wm.jpg", years=[2015]),
 dict(id="mp-0012", cat="fans-and-motors", slug="mercedes-benz-205-blower-motor-with-wheel-and-regulator", orig="MERCEDES-BENZ 205 BLOWER MOTOR WITH WHEEL AND REGULATOR",
      name="Mercedes-Benz 205 Blower Motor with Wheel and Regulator - Valeo Europe", make="Mercedes-Benz", model="205", codes=["MB205", "205"], brand="Valeo Europe",
      country="Hungary", gas="", oil="", refs=[R("099 906 0412", "OEM number (as listed)")], img="b/l/blmb205-01c-v1-eu_4_wm.jpg", years=[]),
 dict(id="mp-0013", cat="refrigerant", slug="opteontm-r1234yf-refrigerant", orig="Opteon™ R1234YF Refrigerant",
      name="Opteon™ R1234YF Refrigerant, 10 lb (4.54 kg)", make="", model="", codes=["R1234YF", "1234YF"], brand="Opteon",
      country="United States of America", gas="R1234YF", oil="", refs=[], img="g/a/gascy1234-01a-l1_1_wm.jpg", years=[], weight="10lb (4.54KG)"),
]
for p in PRODUCTS:
    p["url"] = f"our-products/{p['cat']}/{p['slug']}.html"
    p["old"] = OLD + p["url"]
    p["image"] = IMG + p["img"]
    p["src"] = "public"
    p["status"] = "published"
    p["verified"] = True  # values copied from the public listing; fitment itself still confirmed per enquiry
    p["alt"] = p["name"].replace(" - ", ", ")
    d = []
    if p["make"]: d.append(f"Listed for the {p['make']} {p['model']}.")
    if p["brand"] and p["brand"] != "Original (OE)": d.append(f"Made by {p['brand']}" + (f" in {p['country']}." if p["country"] else "."))
    elif p["country"]: d.append(f"Made in {p['country']}.")
    if p.get("weight"): d.append(f"Pack size {p['weight']}.")
    if p["gas"] and p["cat"] != "refrigerant": d.append(f"Refrigerant: {p['gas']}." + (f" Compressor oil: {p['oil']}." if p["oil"] else ""))
    if p["refs"]: d.append(f"OEM number {p['refs'][0]['n']}.")
    p["desc"] = " ".join(d)

def ccount(slug): return sum(1 for p in PRODUCTS if p["cat"] == slug)

# ---------------- icons ----------------
I = {
 "comp": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="9" width="17" height="14" rx="4"/><circle cx="24.5" cy="16" r="4.5"/><circle cx="24.5" cy="16" r="1.4"/><path d="M8 9V6h4v3M9 23v3M15 23v3"/></svg>',
 "cond": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="4" y="6" width="24" height="20" rx="2.5"/><path d="M4 11h24M4 16h24M4 21h24M10 6v20M16 6v20M22 6v20" opacity=".55"/></svg>',
 "coil": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="6" y="5" width="20" height="22" rx="3"/><path d="M10 10c4 0 4 3 6 3s2-3 6-3M10 16c4 0 4 3 6 3s2-3 6-3M10 22c4 0 4-3 6-3"/></svg>',
 "fan": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="16" cy="16" r="12"/><circle cx="16" cy="16" r="2.2"/><path d="M16 13.8c-1-4 0-7 3-7.5 2 3 0 6-3 7.5ZM18.2 16c4-1 7 0 7.5 3-3 2-6 0-7.5-3ZM16 18.2c1 4 0 7-3 7.5-2-3 0-6 3-7.5ZM13.8 16c-4 1-7 0-7.5-3 3-2 6 0 7.5 3Z"/></svg>',
 "filt": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 6h22l-8 10v8l-6 3V16Z"/></svg>',
 "valve": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 13h7v6H4M28 13h-7v6h7M11 11l10 10M21 11 11 21M16 11V5M12 5h8"/></svg>',
 "drier": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="10" y="6" width="12" height="22" rx="6"/><path d="M14 6V3h4v3M13 14h6M13 18h6"/></svg>',
 "acc": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 4a6 6 0 0 0-5.6 8.2L4.5 22.1a2.5 2.5 0 0 0 3.5 3.5l9.9-9.9A6 6 0 0 0 26 10l-3.5 3.5-3.5-1-1-3.5L21.5 5.5A6 6 0 0 0 20 4Z"/></svg>',
 "equip": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="16" cy="16" r="11"/><path d="M16 16l5-5M9 20h14" /><path d="M8 13a9 9 0 0 1 3-4" opacity=".6"/></svg>',
 "mach": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="6" y="4" width="20" height="22" rx="3"/><circle cx="12" cy="11" r="3"/><circle cx="20" cy="11" r="3"/><path d="M10 19h12M10 22h8M9 26v2M23 26v2"/></svg>',
 "oil": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M16 4s8 9 8 15a8 8 0 0 1-16 0c0-6 8-15 8-15Z"/><path d="M12 20a4 4 0 0 0 4 4"/></svg>',
 "gas": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="9" y="8" width="14" height="20" rx="5"/><path d="M13 8V4h6v4M16 13v10M12 15l8 6M20 15l-8 6"/></svg>',
 "car": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 16H3v-4l2-5h12l3 5h1v4h-2"/><circle cx="7.5" cy="16.5" r="2"/><circle cx="16.5" cy="16.5" r="2"/><path d="M9.5 16.5h5M5 12h15"/></svg>',
 "vin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 9v6M10 9v6M13 9v6M16 9v6M18 9v6"/></svg>',
 "hash": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M9 4 7 20M17 4l-2 16M4 9h16M3 15h16"/></svg>',
 "globe": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="16" cy="16" r="12"/><path d="M4 16h24M16 4c4 4 4 20 0 24M16 4c-4 4-4 20 0 24"/></svg>',
 "factory": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M3 27V14l7 4v-4l7 4v-4l7 4V5h5v22Z"/><path d="M8 22h3M14 22h3M20 22h3"/></svg>',
 "wrench": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M20 4a6 6 0 0 0-5.6 8.2L4.5 22.1a2.5 2.5 0 0 0 3.5 3.5l9.9-9.9A6 6 0 0 0 26 10l-3.5 3.5-3.5-1-1-3.5L21.5 5.5A6 6 0 0 0 20 4Z"/></svg>',
 "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2Z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
 "list": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M9 6h11M9 12h11M9 18h11"/><circle cx="4.5" cy="6" r="1"/><circle cx="4.5" cy="12" r="1"/><circle cx="4.5" cy="18" r="1"/></svg>',
 "grid": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5"/></svg>',
 "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
 "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.5v.5"/></svg>',
 "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="m8 12.5 2.5 2.5L16 9.5"/></svg>',
 "calendar": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="5" y="7" width="22" height="20" rx="3"/><path d="M5 13h22M11 4v6M21 4v6"/></svg>',
 "pin": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M16 29s9-8.5 9-15a9 9 0 0 0-18 0c0 6.5 9 15 9 15Z"/><circle cx="16" cy="14" r="3.2"/></svg>',
 "truck": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M3 8h16v14H3zM19 13h6l4 5v4H19z"/><circle cx="9" cy="23.5" r="2.5" fill="#fff"/><circle cx="23" cy="23.5" r="2.5" fill="#fff"/></svg>',
 "tag": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M4 4h11l13 13-11 11L4 15Z"/><circle cx="10" cy="10" r="2"/></svg>',
 "doc": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M8 3h11l6 6v20H8z"/><path d="M19 3v6h6M12 15h9M12 19h9M12 23h6"/></svg>',
}
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3a.4.4 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>'

PLACEHOLDER = lambda ic: f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300"><rect width="400" height="300" fill="#F3F0E9"/><g transform="translate(150 100) scale(3.1)" color="#B9B2A3">{I[ic].replace("currentColor","#B9B2A3").replace("<svg ", "<svg width=\"32\" height=\"32\" ")}</g><text x="200" y="262" text-anchor="middle" font-family="Arial" font-size="15" fill="#9C9483">Photo to come from catalogue</text></svg>'

# ---------------- shared page shell ----------------
NAV = [("our-products.html", "Catalogue", "products"), ("singapore-workshops/", "SG Workshops", "local"), ("export/", "Export / Buyers", "export"),
       ("become-a-supplier/", "Suppliers", "supplier"),
       ("about-us/", "About", "about"), ("contact-us/", "Contact", "contact")]

ORG = {"@type": "Organization", "@id": BASE + "/#org", "name": LEGAL, "alternateName": BRAND, "url": BASE + "/",
       "logo": LOGO, "image": BASE + "/og.jpg", "foundingDate": "1989", "email": EMAIL, "telephone": TEL_MAIN,
       "contactPoint": [{"@type": "ContactPoint", "telephone": TEL_MAIN, "email": EMAIL, "contactType": "sales", "areaServed": "Worldwide", "availableLanguage": ["English"]}],
       "location": [{"@type": "Place", "name": f"{LEGAL} ({n})", "telephone": "+65 " + t, "address": {"@type": "PostalAddress", "streetAddress": a.rsplit(", Singapore", 1)[0], "addressCountry": "SG", "postalCode": a[-6:]}} for n, a, t, f in BRANCHES]}

VER = {}
def asset(name):
    if name not in VER:
        VER[name] = hashlib.sha1((HERE / name).read_bytes()).hexdigest()[:8]
    return f"{name}?v={VER[name]}"

pages = []  # (path, priority) for sitemap

def shell(path, title, desc, body, active="", crumbs=None, schema=None, js=("data.js", "mp.js", "chat.js", "wa.js"), og_type="website", index=True, img=None):
    depth = path.count("/") if not path.endswith("/") else path.count("/")
    if path.endswith(".html"):
        depth = path.count("/")
    r = "../" * depth
    url = BASE + "/" + (path.replace("index.html", "") if path != "index.html" else "")
    if path == "index.html": url = BASE + "/"
    ld = [dict(ORG)]
    if crumbs:
        ld.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u} for i, (n, u) in enumerate([("Home", "")] + crumbs)]})
    if schema: ld.extend(schema)
    ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False).replace("</", "<\\/")
    nav = "".join(f'<a href="{r}{u}"{" aria-current=\"page\"" if k == active else ""}{" data-catpanel aria-controls=\"catpanel\" aria-expanded=\"false\"" if k == "products" else ""}>{e(n)}{" <svg class=\"chev\" viewBox=\"0 0 12 12\" width=\"12\" height=\"12\"><path d=\"M2.5 4.5 6 8l3.5-3.5\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"1.8\"/></svg>" if k == "products" else ""}</a>' for u, n, k in NAV)
    cp_tiles = "".join(f'<a class="cp-t" href="{r}our-products/{c[0]}.html"><span class="ic">{I[c[3]]}</span><span><b>{e(c[1])}</b><small>{ccount(c[0]) or "to import"}{" listed" if ccount(c[0]) else ""}</small></span></a>' for c in CATS)
    catpanel = f'''<div class="catpanel" id="catpanel" hidden><div class="wrap">
<form class="qbox" data-finder="main" action="{r}our-products.html" role="search"><label class="f" for="q-cp">Search the catalogue</label><div class="qrow"><input class="in" id="q-cp" name="q" autocomplete="off" placeholder="Part no. or car, e.g. 8730R" data-live><button class="btn btn-o" type="submit">{I['search']}<span class="sr">Search</span></button></div><div class="live" role="listbox"></div></form>
<div class="cp-grid">{cp_tiles}<a class="cp-t all" href="{r}our-products.html"><span class="ic">{I['list']}</span><span><b>All products</b><small>Search &amp; filter</small></span></a></div>
<div class="cp-foot"><a href="{r}rfq/#vin">Don't know the part? Send a chassis number</a><a href="{r}rfq/#bulk">Have a parts list? Check it in one go</a><a href="{r}rfq/?need=">Can't find it? Request sourcing</a></div>
</div></div>'''
    sheet = "".join(f'<a class="brc" href="tel:+65{t.replace(" ","")}"><span><b>{e(n)}</b><small>{e(a)}</small></span><span class="btn btn-o btn-s">{I["phone"]} {t}</span></a>' for n, a, t, f in BRANCHES)
    ogi = img or (BASE + "/og.jpg")
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Breadcrumb"><a href="' + r + '">Home</a>' + "".join(
            (f'<span>/</span><a href="{r}{u}">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span>/</span>{e(n)}') for i, (n, u) in enumerate(crumbs)) + "</nav>"
    body = body.replace("{{CRUMBS}}", cr).replace("{{R}}", r)
    scripts = "".join(f'<script src="{r}{asset(j)}" defer></script>' for j in js)
    doc = f"""<!doctype html>
<html lang="en-SG" class="no-js" data-root="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{ogi}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(title)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="{r}icon-192.png"><link rel="apple-touch-icon" href="{r}apple-touch-icon.png"><link rel="manifest" href="{r}site.webmanifest">
<meta name="theme-color" content="#0A1F35">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{r}{asset('mp.css')}">
<script>document.documentElement.classList.remove('no-js');window.MP_ROOT="{r}";</script>
<script type="application/ld+json">{ldj}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="pv" role="note"><span class="pv-l">Preview mockup for Mega Power, not the live website. Enquiries here are demo only. </span><span class="pv-s">Preview mockup · </span><a href="{r}demo-guide/">Demo tour</a> · <a href="{r}staff/">Staff dashboard</a></div>
<header class="hd"><div class="wrap">
<a class="logo" href="{r}" aria-label="Mega Power home"><img src="{LOGO}" alt="Mega Power" width="160" height="38" onerror="this.parentNode.classList.add('noimg')"><span class="wm">MEGA POWER<small>Engineering &amp; Trading</small></span></a>
<nav class="nav" id="nav" aria-label="Main">{nav}</nav>
<div class="hd-act"><button class="catb" type="button" data-catpanel aria-controls="catpanel" aria-expanded="false">{I['grid']}<span>Catalogue</span></button><a class="rfqb" href="{r}rfq/" aria-label="Enquiry list">{I['list']}<span>Enquiry list</span><b data-rfq-count>0</b></a>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button></div>
</div>{catpanel}</header>
<main id="main">
{body}
</main>
<footer class="ft-main"><div class="wrap">
<div class="ft-g">
<div><h4>{LEGAL}</h4><p>Automotive air-conditioning and cooling parts for the trade, serving workshops since 1989.</p><p><a href="tel:{TEL_MAIN_H}">{TEL_MAIN}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<div><h4>Products</h4><ul>{"".join(f'<li><a href="{r}our-products/{c[0]}.html">{e(c[1])}</a></li>' for c in CATS[:6])}<li><a href="{r}our-products.html">All products</a></li></ul></div>
<div><h4>Work with us</h4><ul><li><a href="{r}export/">Export enquiries</a></li><li><a href="{r}become-a-supplier/">Become a supplier</a></li><li><a href="{r}singapore-workshops/">Singapore workshops</a></li><li><a href="{r}rfq/#vin">Send a chassis number</a></li><li><a href="{r}articles/">Guides</a></li></ul></div>
<div><h4>Branches</h4><ul>{"".join(f'<li>{e(n)}: <a href="tel:+65{t.replace(" ","")}">{t}</a></li>' for n, a, t, f in BRANCHES)}</ul></div>
</div>
<div class="ft-b"><span>&copy; {datetime.date.today().year} {LEGAL}</span><span><a href="{r}privacy-policy/">Privacy</a> · <a href="{r}terms-conditions/">Terms</a> · <a href="{r}staff/">Staff</a></span></div>
</div></footer>
<nav class="mbar" aria-label="Quick actions"><a href="{r}our-products.html" data-catpanel aria-controls="catpanel">{I['grid']}Catalogue</a><a class="hot" href="{r}rfq/">{I['list']}Enquiry <span data-rfq-count2></span></a><a href="{r}contact-us/" data-branches>{I['phone']}Call a branch</a></nav>
<div class="mod" id="branch-sheet" role="dialog" aria-modal="true" aria-labelledby="bs-h"><div class="box"><h3 id="bs-h">Call a Mega Power branch</h3><p class="note" style="margin-top:-4px">Opening hours to be confirmed. Main line <a href="tel:{TEL_MAIN_H}">{TEL_MAIN}</a>.</p><div class="brcs">{sheet}</div><button class="btn btn-g" type="button" data-close style="width:100%;margin-top:12px">Close</button></div></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
{scripts}
</body>
</html>
"""
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc)
    if index:
        pages.append(("/" + path.replace("index.html", "") if path != "index.html" else "/", 1.0 if path == "index.html" else 0.7))

def img_tag(p, cls="", lazy=True, w=400, h=300):
    ic = CAT[p["cat"]][3]
    return f'<img src="{e(p["image"])}" alt="{e(p["alt"])}" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else ""} decoding="async" onerror="this.onerror=null;this.src=(window.MP_ROOT||\'\')+\'img/ph-{ic}.svg\'">'

def card(p, r):
    refs = "".join(f'<span>{e(x["n"])}</span>' for x in p["refs"][:2])
    meta = " · ".join(x for x in [p["make"] + (" " + p["model"] if p["model"] else ""), p["brand"]] if x.strip())
    return f'''<article class="card rv"><div class="im">{img_tag(p)}</div><div class="bd">
<span class="tag tag-n" style="align-self:flex-start">{e(CAT[p["cat"]][1])}</span>
<h3><a href="{r}{p["url"]}">{e(p["name"])}</a></h3><div class="meta">{e(meta)}</div>{f'<div class="refs">{refs}</div>' if refs else ''}
<div class="ft"><a class="btn btn-g btn-s" href="{r}{p["url"]}">View details</a><button class="btn btn-o btn-s" data-add="{p["id"]}">Add to RFQ</button></div></div></article>'''

def finder(r, compact=False):
    makes = sorted({p["make"] for p in PRODUCTS if p["make"]})
    return f'''<div class="finder" id="finder">
<div class="tabs" role="tablist" aria-label="Find a part">
<button role="tab" id="t-veh" aria-controls="p-veh" aria-selected="true">{I['car']}By vehicle</button>
<button role="tab" id="t-vin" aria-controls="p-vin" aria-selected="false" tabindex="-1">{I['vin']}VIN / chassis</button>
<button role="tab" id="t-ref" aria-controls="p-ref" aria-selected="false" tabindex="-1">{I['hash']}OEM / part no.</button>
</div>
<form class="tabp" id="p-veh" role="tabpanel" aria-labelledby="t-veh" data-finder="vehicle" action="{r}our-products.html">
<div class="qbox"><label class="f" for="q-veh">Describe the part <i>(e.g. BMW F45 compressor)</i></label>
<div class="qrow"><input class="in" id="q-veh" name="q" autocomplete="off" placeholder="Make, model, chassis code, part" data-live><button class="btn btn-o" type="submit">{I['search']}<span class="sr">Search</span></button></div>
<div class="live" role="listbox"></div></div>
{"<details class=\"moref\"><summary>Filter by make, model, year</summary>" if compact else ""}<div class="grid2" style="margin-top:12px">
<div><label class="f" for="s-make">Make</label><select class="in" id="s-make" name="make"><option value="">Any make</option>{"".join(f'<option>{e(m)}</option>' for m in makes)}<option value="__other">Other make</option></select></div>
<div><label class="f" for="s-model">Model</label><select class="in" id="s-model" name="model" disabled><option value="">Choose a make first</option></select></div>
<div><label class="f" for="s-year">Model year <i>(optional)</i></label><input class="in" id="s-year" name="year" inputmode="numeric" maxlength="4" placeholder="e.g. 2015"></div>
<div><label class="f" for="s-cat">Part type</label><select class="in" id="s-cat" name="cat"><option value="">Any part</option>{"".join(f'<option value="{c[0]}">{e(c[1])}</option>' for c in CATS)}</select></div>
</div>{"</details>" if compact else ""}
<p class="ex">Try: <button type="button" data-try="BMW F45 compressor">BMW F45 compressor</button><button type="button" data-try="Mercedes W205 compressor">Mercedes W205 compressor</button><button type="button" data-try="Mercedes W210 compressor">Mercedes W210 compressor</button></p>
</form>
<form class="tabp" id="p-vin" role="tabpanel" aria-labelledby="t-vin" hidden data-lead="EXPORT" data-sub="VIN_MATCH" novalidate>
<p style="margin:0 0 12px;font-size:.93rem">Not sure which part fits? Send the VIN or chassis number. Our team identifies the part and replies. We do not decode VINs automatically.</p>
<div class="grid2">
<div><label class="f" for="v-vin">VIN / chassis number</label><input class="in" id="v-vin" name="vin" required minlength="6" autocomplete="off" style="text-transform:uppercase"><div class="err">Enter at least 6 characters.</div></div>
<div><label class="f" for="v-part">Part needed</label><select class="in" id="v-part" name="part" required><option value="">Choose</option>{"".join(f'<option>{e(c[1])}</option>' for c in CATS)}<option>Not sure</option></select><div class="err">Choose a part.</div></div>
<div><label class="f" for="v-name">Your name</label><input class="in" id="v-name" name="name" required autocomplete="name"><div class="err">Please add your name.</div></div>
<div><label class="f" for="v-contact">Email or WhatsApp</label><input class="in" id="v-contact" name="contact" required><div class="err">We need a way to reply.</div></div>
<div><label class="f" for="v-country">Country</label><input class="in" id="v-country" name="country" placeholder="e.g. Malaysia" autocomplete="country-name"></div>
<div><label class="f">Photo of old part label <i>(optional)</i></label><label class="drop" data-drop><input type="file" name="file" accept="image/*,.pdf">Tap to add a photo</label></div>
</div>
<label class="chk" style="margin-top:12px"><input type="checkbox" name="consent" required> <span>I agree that Mega Power may use these details to reply to this enquiry (<a href="{r}privacy-policy/">privacy</a>).</span></label>
<button class="btn btn-o" type="submit" style="margin-top:14px;width:100%">Send chassis number to our team</button>
</form>
<form class="tabp" id="p-ref" role="tabpanel" aria-labelledby="t-ref" hidden data-finder="ref" action="{r}our-products.html">
<div class="qbox"><label class="f" for="q-ref">OEM or part number</label>
<div class="qrow"><input class="in mono" id="q-ref" name="q" autocomplete="off" placeholder="e.g. 4M0 816 421B" data-live><button class="btn btn-o" type="submit">{I['search']}<span class="sr">Search</span></button></div>
<div class="live" role="listbox"></div></div>
<p class="hint">Spaces, dashes and capitals don't matter. Numbers differ by market, so we show exact matches and possible alternates separately.</p>
<p class="ex">Try: <button type="button" data-try="8730R">8730R</button><button type="button" data-try="4M0816421B">4M0816421B</button><button type="button" data-try="437100 8011">437100 8011</button></p>
</form>
</div>'''

# ---------------- home ----------------
def home():
    r = ""
    feat = [p for p in PRODUCTS if p["id"] in ("mp-0008", "mp-0004", "mp-0010", "mp-0012", "mp-0007", "mp-0013")]
    catgrid = "".join(f'<a class="cat rv" href="our-products/{s}.html"><span class="n{" z" if not ccount(s) else ""}">{ccount(s) if ccount(s) else "to import"}</span><span class="ic">{I[ic]}</span><b>{e(n)}</b><small>{e(d)}</small></a>' for s, n, d, ic in CATS)
    from hero_art import world, aircon, singapore
    BR_XY = [("Ang Mo Kio", 103.862, 1.373), ("Toh Guan", 103.745, 1.333), ("Kaki Bukit", 103.906, 1.336), ("Soon Lee", 103.703, 1.330)]
    strip_items = "".join(f'<a class="fs-i" href="{p["url"]}"><span class="fs-im">{img_tag(p, w=240, h=180)}</span><span class="fs-t"><small>{e(CAT[p["cat"]][1])}</small><b>{e(p["name"])}</b><span class="mono">{e(p["refs"][0]["n"]) if p["refs"] else ""}</span></span></a>' for p in PRODUCTS)
    cat_t = "".join(f'<a class="ct rv" href="our-products/{s_}.html"><span class="ic">{I[ic]}</span><b>{e(n)}</b><small>{(str(ccount(s_)) + " listed") if ccount(s_) else "Ask us"}</small></a>' for s_, n, d, ic in CATS)
    slides = [
        ("Singapore · Since 1989", '<h1 class="hx-h">Automotive air-con parts, <em>supplied from Singapore to the world.</em></h1>',
         "Compressors, condensers, blower motors and cooling parts for workshops and buyers in Singapore and overseas.",
         f'<a class="btn btn-o" href="our-products.html">{I["grid"]} Browse the catalogue</a><a class="btn btn-ghost" href="export/">Export enquiry</a>', world()),
        ("Find the right part", '<p class="hx-h">Search by car, chassis or <em>OEM number.</em></p>',
         "Every result says whether the reference is an exact match or needs checking. Our team confirms fitment before quoting.",
         f'<a class="btn btn-o" href="#finder">{I["search"]} Search parts</a><a class="btn btn-ghost" href="rfq/#vin">Send a chassis number</a>', aircon()),
        ("4 branches in Singapore", '<p class="hx-h">Need it for a job today? <em>Call your nearest branch.</em></p>',
         "Ang Mo Kio, Toh Guan, Kaki Bukit and Soon Lee, serving workshops and garages across the island.",
         f'<a class="btn btn-o" href="#" data-branches>{I["phone"]} Call a branch</a><a class="btn btn-ghost" href="singapore-workshops/">Workshop enquiry</a>', singapore(BR_XY)),
    ]
    sl = ""
    for i, (k, h, t, c, art) in enumerate(slides):
        on = " is-on" if i == 0 else ""
        hid = "" if i == 0 else ' aria-hidden="true"'
        sl += f'<div class="hx-s{on}" role="group" aria-roledescription="slide" aria-label="{i+1} of {len(slides)}"{hid}><div class="hx-art">{art}</div><div class="wrap hx-c"><span class="eyebrow">{k}</span>{h}<p class="hx-p">{t}</p><div class="hx-cta">{c}</div></div></div>'
    dots = "".join('<button type="button" aria-label="Show slide %d"%s></button>' % (i + 1, ' aria-current="true"' if i == 0 else "") for i in range(len(slides)))
    body = f'''<section class="hx" aria-roledescription="carousel" aria-label="Mega Power at a glance"><div class="hx-track">{sl}</div>
<div class="wrap hx-nav"><div class="hx-dots">{dots}</div><button type="button" class="hx-pp" aria-label="Pause slides"><span></span></button></div><div class="hx-bar"><i></i></div></section>
<section class="hx-find"><div class="wrap">{finder(r, compact=True)}</div></section>
<section class="sec-c"><div class="wrap">
<div class="who">
<a class="wh rv" href="singapore-workshops/"><span class="ic">{I['wrench']}</span><span><b>Singapore workshop</b><small>Check a part, call your branch</small></span><i>&rarr;</i></a>
<a class="wh dark rv" href="export/"><span class="ic">{I['globe']}</span><span><b>Overseas buyer</b><small>Request an export quotation</small></span><i>&rarr;</i></a>
<a class="wh rv" href="become-a-supplier/"><span class="ic">{I['factory']}</span><span><b>Parts supplier</b><small>Propose your range to us</small></span><i>&rarr;</i></a>
</div></div></section>
<section class="sec-c"><div class="wrap">
<div class="hd2 rv"><div><span class="kick">Product range</span><h2>Shop by part type</h2></div><a class="lk" href="our-products.html">All products &rarr;</a></div>
<div class="cts">{cat_t}</div>
</div></section>
<section class="sec-c bg-n"><div class="wrap">
<div class="hd2 rv"><div><span class="kick">From the catalogue</span><h2>Parts on the shelf</h2></div><a class="lk" href="our-products.html">See all &rarr;</a></div></div>
<div class="fs" aria-label="Featured parts"><div class="fs-tr">{strip_items}<span class="fs-dup" aria-hidden="true">{strip_items}</span></div></div>
</section>
<section class="sec-c"><div class="wrap">
<ul class="stats">
<li class="rv"><b data-cu="1989" data-from="1960">1989</b><span>Serving the trade since</span></li>
<li class="rv"><b data-cu="4">4</b><span>Branches in Singapore</span></li>
<li class="rv"><b data-cu="12">12</b><span>Part types in the catalogue</span></li>
</ul>
<ol class="stp">
<li class="rv"><span>1</span><b>Search</b><small>Car, chassis or OEM no.</small></li>
<li class="rv"><span>2</span><b>Check fitment</b><small>Exact or needs checking</small></li>
<li class="rv"><span>3</span><b>Send one enquiry</b><small>Add parts and quantities</small></li>
<li class="rv"><span>4</span><b>Get a quote</b><small>Our team confirms and replies</small></li>
</ol>
</div></section>
<section class="sec-c bg-w"><div class="wrap two2">
<div class="rv"><span class="kick">About</span><h2>A Singapore A/C parts specialist since 1989</h2><p>{LEGAL} supplies automotive air-conditioning parts to workshops and garages, for passenger cars, commercial vehicles, trucks and excavators.</p>
<p class="bl">Component brands in our current listings: <span>DENSO</span><span>SANDEN</span><span>BEHR</span><span>VALEO</span><span>OPTEON</span></p>
<a class="lk" href="about-us/">More about us &rarr;</a></div>
<div class="faq rv"><h3>Common questions</h3>
<details><summary>Do you show prices online?</summary><p>No. Prices depend on the exact part, quantity and destination, so we quote each enquiry.</p></details>
<details><summary>I don't know the part number. Can you still help?</summary><p>Yes. Send the make, model and year, or the VIN or chassis number, and our team identifies the part.</p></details>
<details><summary>Do you supply buyers outside Singapore?</summary><p>Send an export enquiry with the country and quantity and our team replies with what we can supply.</p></details>
<details><summary>How do I offer my products to Mega Power?</summary><p>Use the supplier form to send your company details, range, catalogue and MOQ.</p></details>
</div></div></section>'''

    faq = [("Do you show prices online?", "No. Prices depend on the exact part, quantity and destination, so we quote each enquiry."),
           ("I don't know the part number. Can you still help?", "Yes. Send the make, model and year, or the VIN or chassis number, and our team identifies the part."),
           ("Do you supply buyers outside Singapore?", "Send an export enquiry with the country and quantity and our team replies with what we can supply."),
           ("How do I offer my products to Mega Power?", "Use the supplier form to send your company details, range, catalogue and MOQ.")]
    sch = [{"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": BRAND, "publisher": {"@id": BASE + "/#org"},
            "potentialAction": {"@type": "SearchAction", "target": BASE + "/our-products.html?q={search_term_string}", "query-input": "required name=search_term_string"}},
           {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    shell("index.html", "Automotive Air-Con Parts Supplier Singapore | Mega Power",
          "Automotive A/C compressors, condensers and cooling parts from Singapore since 1989. Search by vehicle, chassis or OEM number and request a quote.",
          body, schema=sch)

# ---------------- catalogue ----------------
def filters_html():
    return f'''<aside class="filters" id="filters" aria-label="Filters">
<fieldset><legend>Part type</legend><div data-fl="cat"></div></fieldset>
<fieldset><legend>Vehicle make</legend><div data-fl="make"></div></fieldset>
<fieldset><legend>Component brand</legend><div data-fl="brand"></div></fieldset>
<button class="btn btn-g btn-s" type="button" data-clear style="width:100%">Clear filters</button>
</aside>'''

def catalogue():
    r = ""
    nojs = "".join(card(p, r) for p in PRODUCTS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Products &amp; part search</h1><p>Search the catalogue by vehicle, chassis code or OEM number. Results say clearly whether a reference matches exactly or needs checking by our team.</p></div></section>
<section class="sec" style="padding-top:28px"><div class="wrap">
<form class="qbox" data-finder="main" action="" style="margin-bottom:20px" role="search">
<label class="f" for="q-main">Search all products</label>
<div class="qrow"><input class="in" id="q-main" name="q" autocomplete="off" placeholder="Try 8730R, BMW F45 compressor, 4M0 816 421B" data-live><button class="btn btn-o" type="submit">{I['search']} Search</button></div>
<div class="live" role="listbox"></div>
<p class="ex">Try: <button type="button" data-try="8730R">8730R</button><button type="button" data-try="BMW F45 compressor">BMW F45 compressor</button><button type="button" data-try="4M0 816 421B">4M0 816 421B</button><button type="button" data-try="Mercedes W205 compressor">Mercedes W205 compressor</button><button type="button" data-try="Mercedes W210 compressor">Mercedes W210 compressor</button></p>
</form>
<div class="cat-l">{filters_html()}
<div><div class="res-hd"><span class="cnt" data-count>{len(PRODUCTS)} products</span><button class="btn btn-g btn-s ftoggle" type="button" data-ftoggle aria-controls="filters">Filters</button></div>
<div data-note></div>
<div class="pgrid" data-results>{nojs}</div><div class="pager" data-pager></div></div>
</div></div></section>'''
    sch = [{"@type": "CollectionPage", "name": "Mega Power products", "url": BASE + "/our-products.html", "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + "/" + p["url"], "name": p["name"]} for i, p in enumerate(PRODUCTS)]}}]
    shell("our-products.html", "Car A/C Parts Catalogue & OEM Search | Mega Power",
          "Search automotive A/C compressors, condensers, blower motors and refrigerant by vehicle, chassis code or OEM number. Enquiry-based, no checkout.",
          body, active="products", crumbs=[("Products", "our-products.html")], schema=sch)
    for s, n, d, ic in CATS:
        items = [p for p in PRODUCTS if p["cat"] == s]
        if items:
            grid = f'<div class="pgrid" data-results data-cat="{s}">{"".join(card(p, "../") for p in items)}</div>'
        else:
            grid = f'''<div class="pgrid" data-results data-cat="{s}"></div><div class="nores rv" data-empty><span class="tag tag-g">Moving over from the current catalogue</span><h3 style="margin-top:12px">{e(n)} listings are being moved over</h3><p>The current website lists this category. Its products will appear here once the full catalogue is imported. Need one now? Send the vehicle details or part number.</p><div class="pd-cta"><a class="btn btn-o" href="../rfq/?need={e(n)}">Request {e(n.lower())}</a><a class="btn btn-g" href="../rfq/#vin">Send a chassis number</a></div></div>'''
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>{e(n)}</h1><p>{e(d)}. {len(items) if items else "No"} listing{"" if len(items) == 1 else "s"} shown in this preview. Search by make, model or reference number.</p></div></section>
<section class="sec" style="padding-top:28px"><div class="wrap">
<form class="qbox" data-finder="main" data-scope="{s}" action="" style="margin-bottom:20px" role="search"><label class="f" for="q-c">Search {e(n.lower())}</label><div class="qrow"><input class="in" id="q-c" name="q" autocomplete="off" placeholder="Make, model or OEM number" data-live><button class="btn btn-o" type="submit">{I['search']} Search</button></div><div class="live" role="listbox"></div></form>
<div class="res-hd"><span class="cnt" data-count>{len(items)} products</span><a class="btn btn-g btn-s" href="../our-products.html">All categories</a></div><div data-note></div>
{grid}
</div></section>'''
        sch = [{"@type": "CollectionPage", "name": n, "url": BASE + f"/our-products/{s}.html", "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + "/" + p["url"], "name": p["name"]} for i, p in enumerate(items)]}}]
        title = f"Car A/C {n} Supplier Singapore | Mega Power"
        if len(title) > 60: title = f"Car A/C {n} | Mega Power"
        shell(f"our-products/{s}.html", title, f"{n} for automotive air-conditioning from {LEGAL}, Singapore. Search by vehicle or OEM number and send an enquiry.",
              body, active="products", crumbs=[("Products", "our-products.html"), (n, f"our-products/{s}.html")], schema=sch)

def product(p):
    r = "../../"
    c = CAT[p["cat"]]
    rows = [("Part type", c[1]), ("Car make", p["make"]), ("Model (as listed)", p["model"]), ("Component brand", p["brand"]),
            ("Country of manufacture", p["country"]), ("Refrigerant gas", p["gas"]), ("Compressor oil", p["oil"]), ("Weight", p.get("weight", "")),
            ("Year (as listed)", ", ".join(map(str, p["years"])))]
    spec = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in rows if b)
    refs = "".join(f'<tr><th>{e(x["t"])}</th><td class="mono">{e(x["n"])}</td></tr>' for x in p["refs"])
    related = [q for q in PRODUCTS if q["id"] != p["id"] and (q["make"] == p["make"] and q["make"] or q["cat"] == p["cat"])][:3]
    yrnote = "The year shown is the one on our listing. " if p["years"] else ""
    body = f'''<section class="ph-hd" style="padding:28px 0 30px"><div class="wrap">{{{{CRUMBS}}}}</div></section>
<section class="sec" style="padding-top:34px"><div class="wrap pd" data-product="{p["id"]}">
<div class="pd-img">{img_tag(p, lazy=False, w=800, h=800)}</div>
<div>
<span class="tag tag-n">{e(c[1])}</span>
<h1 style="margin-top:10px">{e(p["name"])}</h1>
<p>{e(p["desc"])}</p>
<table class="spec"><caption class="sr">Reference numbers</caption>{refs or '<tr><th>Reference</th><td>Not shown on the current listing</td></tr>'}</table>
<div class="fit">{I['info']}<div><b>Fitment is confirmed by our team.</b> {yrnote}OEM numbers can differ by market, engine and year. Send your VIN or chassis number with the enquiry and we check it before quoting.</div></div>
<div class="pd-cta"><div class="qty"><button type="button" data-q="-1" aria-label="Less">−</button><input type="number" min="1" value="1" aria-label="Quantity" data-qty><button type="button" data-q="1" aria-label="More">+</button></div>
<button class="btn btn-o" data-add="{p["id"]}" data-withqty>Add to enquiry list</button></div>
<div class="split">
<div><b>{I['wrench']} Singapore workshop</b><span>Call a branch to check the part, or send the car details.</span><div class="brmini">{"".join(f'<a href="tel:+65{t.replace(" ","")}">{e(n)}</a>' for n, a, t, f in BRANCHES)}</div><a class="btn btn-g btn-s" href="{r}singapore-workshops/?p={p["id"]}">Workshop enquiry</a></div>
<div><b>{I['globe']} Overseas buyer</b><span>Quoted by quantity and destination. Shipping and payment terms are agreed in the quotation.</span><a class="btn btn-n btn-s" href="{r}rfq/?add={p["id"]}&amp;type=EXPORT">Request export quote</a></div>
</div>
<h2 style="font-size:1.15rem;margin-top:24px">Specifications</h2>
<table class="spec">{spec}</table>
<p class="note">Details as listed on the current Mega Power catalogue page. Stock and prices are given on enquiry.</p>
</div></div></section>
{f'<section class="sec bg-w" style="padding:52px 0"><div class="wrap"><h2>Related parts</h2><div class="pgrid">{"".join(card(q, r) for q in related)}</div></div></section>' if related else ''}'''
    title = p["name"].split(" - ")[0]
    ref = p["refs"][0]["n"] if p["refs"] else ""
    SHORT = {"mp-0010": "Audi Q7 2015 A/C Condenser", "mp-0011": "Audi A4 2015 A/C Condenser", "mp-0012": "Mercedes-Benz 205 Blower Motor"}
    if p["id"] in SHORT: title = SHORT[p["id"]]
    t = f"{title} {ref} | Mega Power" if ref else f"{title} | Mega Power"
    if len(t) > 60: t = f"{title} | Mega Power"
    if len(t) > 60: t = (title[:47] + "…") + " | Mega Power"
    desc = (p["desc"] + " Ask Mega Power Singapore for a quote.")[:158]
    sch = [{"@type": "WebPage", "url": BASE + "/" + p["url"], "name": p["name"], "primaryImageOfPage": {"@type": "ImageObject", "url": p["image"]},
            "about": {"@type": "Thing", "name": p["name"], "identifier": [x["n"] for x in p["refs"]] or None}}]
    shell(p["url"], t, desc, body, active="products", img=p["image"],
          crumbs=[("Products", "our-products.html"), (c[1], f"our-products/{c[0]}.html"), (title, p["url"])], schema=sch)

def item_page():
    body = '''<section class="ph-hd" style="padding:28px 0 30px"><div class="wrap"><nav class="crumbs"><a href="../">Home</a><span>/</span><a href="../our-products.html">Products</a><span>/</span><span data-crumb>Product</span></nav></div></section>
<section class="sec" style="padding-top:34px"><div class="wrap" data-item-page><p>Loading product…</p></div></section>'''
    shell("our-products/item.html", "Product | Mega Power", "Product added in the Mega Power staff dashboard (demo).", body, active="products", index=False)

# ---------------- funnels ----------------
def lead_form(kind, r, prefill_note=""):
    cats = "".join(f'<option>{e(c[1])}</option>' for c in CATS)
    if kind == "EXPORT":
        return f'''<form class="form-card" data-lead="EXPORT" novalidate id="rfq-form">
<h2>Export quotation request</h2>{prefill_note}<div data-items></div>
<div class="fgrid">
<div><label class="f" for="x-name">Name</label><input class="in" id="x-name" name="name" required autocomplete="name"><div class="err">Please add your name.</div></div>
<div><label class="f" for="x-co">Company</label><input class="in" id="x-co" name="company" required autocomplete="organization"><div class="err">Please add your company.</div></div>
<div><label class="f" for="x-country">Country</label><input class="in" id="x-country" name="country" required autocomplete="country-name"><div class="err">Which country is this for?</div></div>
<div><label class="f" for="x-email">Work email</label><input class="in" id="x-email" name="email" type="email" required autocomplete="email"><div class="err">Enter a valid email.</div></div>
<div><label class="f" for="x-mob">Mobile / WhatsApp <i>(optional)</i></label><input class="in" id="x-mob" name="mobile" type="tel" autocomplete="tel"></div>
<div><label class="f" for="x-wc">WeChat ID <i>(optional)</i></label><input class="in" id="x-wc" name="wechat"></div>
<div><label class="f" for="x-cat">Part category</label><select class="in" id="x-cat" name="category"><option value="">From my list / not sure</option>{cats}</select></div>
<div><label class="f" for="x-veh">Vehicle make, model, year</label><input class="in" id="x-veh" name="vehicle" placeholder="e.g. BMW 218i F45 2016"></div>
<div><label class="f" for="x-vin">VIN / chassis <i>(optional)</i></label><input class="in mono" id="x-vin" name="vin"></div>
<div><label class="f" for="x-oem">OEM number <i>(optional)</i></label><input class="in mono" id="x-oem" name="oem"></div>
<div><label class="f" for="x-qty">Quantity</label><input class="in" id="x-qty" name="quantity" inputmode="numeric" placeholder="e.g. 20 pcs" required><div class="err">How many do you need?</div></div>
<div><label class="f" for="x-dest">Destination port / city</label><input class="in" id="x-dest" name="destination" placeholder="e.g. Port Klang"></div>
<div class="full"><label class="f">Photo or parts list <i>(optional)</i></label><label class="drop" data-drop><input type="file" name="file" accept="image/*,.pdf,.xlsx,.csv">Drop a file or tap to choose</label></div>
<div class="full"><label class="f" for="x-msg">Message</label><textarea class="in" id="x-msg" name="message" placeholder="Shipping requirements, timing, anything else"></textarea></div>
<div class="full"><label class="f" for="x-pref">Preferred reply channel</label><select class="in" id="x-pref" name="channel"><option>Email</option><option>WhatsApp</option><option>WeChat</option><option>Phone</option></select></div>
<div class="full"><label class="chk"><input type="checkbox" name="consent" required> <span>I agree that Mega Power may use these details to reply to this enquiry (<a href="{r}privacy-policy/">privacy</a>).</span></label><div class="err">Please tick to continue.</div></div>
</div>
<div class="demo-flag">{I['info']}<span>Demo: the enquiry is saved to the staff inbox in this browser. No email or WhatsApp is sent until Mega Power confirms the addresses.</span></div>
<button class="btn btn-o" type="submit" style="width:100%">Send export enquiry</button></form>'''
    if kind == "LOCAL":
        return f'''<form class="form-card" data-lead="LOCAL" novalidate id="local-form">
<h2>Workshop enquiry</h2>{prefill_note}<div data-items></div>
<div class="fgrid">
<div><label class="f" for="l-garage">Workshop name</label><input class="in" id="l-garage" name="company" required><div class="err">Please add the workshop name.</div></div>
<div><label class="f" for="l-name">Your name</label><input class="in" id="l-name" name="name" required autocomplete="name"><div class="err">Please add your name.</div></div>
<div><label class="f" for="l-tel">Phone / WhatsApp</label><input class="in" id="l-tel" name="mobile" type="tel" required autocomplete="tel" placeholder="8 digits"><div class="err">Enter a phone number.</div></div>
<div><label class="f" for="l-branch">Nearest branch</label><select class="in" id="l-branch" name="branch">{"".join(f'<option>{e(b[0])}</option>' for b in BRANCHES)}</select></div>
<div><label class="f" for="l-veh">Vehicle make, model, year</label><input class="in" id="l-veh" name="vehicle" required placeholder="e.g. Mercedes C200 W205 2017"><div class="err">Which vehicle is it for?</div></div>
<div><label class="f" for="l-part">Part needed</label><input class="in" id="l-part" name="part" required placeholder="e.g. compressor"><div class="err">Which part?</div></div>
<div><label class="f" for="l-oem">OEM / chassis <i>(optional)</i></label><input class="in mono" id="l-oem" name="oem"></div>
<div><label class="f">Photo <i>(optional)</i></label><label class="drop" data-drop><input type="file" name="file" accept="image/*">Tap to add a photo</label></div>
<div class="full"><label class="f" for="l-msg">Note</label><textarea class="in" id="l-msg" name="message" placeholder="When do you need it?"></textarea></div>
<div class="full"><label class="chk"><input type="checkbox" name="consent" required> <span>I agree that Mega Power may use these details to reply (<a href="{r}privacy-policy/">privacy</a>).</span></label><div class="err">Please tick to continue.</div></div>
</div>
<div class="demo-flag">{I['info']}<span>Demo: saved to the staff inbox in this browser only.</span></div>
<button class="btn btn-o" type="submit" style="width:100%">Send workshop enquiry</button></form>'''
    if kind == "SUPPLIER":
        return f'''<form class="form-card" data-lead="SUPPLIER" novalidate id="sup-form">
<h2>Supplier introduction</h2>
<div class="fgrid">
<div><label class="f" for="s-co">Company / manufacturer</label><input class="in" id="s-co" name="company" required autocomplete="organization"><div class="err">Please add your company.</div></div>
<div><label class="f" for="s-country">Country</label><input class="in" id="s-country" name="country" required><div class="err">Where are you based?</div></div>
<div><label class="f" for="s-name">Contact person</label><input class="in" id="s-name" name="name" required autocomplete="name"><div class="err">Please add a contact name.</div></div>
<div><label class="f" for="s-email">Work email</label><input class="in" id="s-email" name="email" type="email" required autocomplete="email"><div class="err">Enter a valid email.</div></div>
<div><label class="f" for="s-type">You are a</label><select class="in" id="s-type" name="supplier_type"><option>Manufacturer / factory</option><option>Brand owner</option><option>Distributor</option><option>Other</option></select></div>
<div><label class="f" for="s-brand">Brand(s)</label><input class="in" id="s-brand" name="brands"></div>
<div class="full"><label class="f">Part categories you supply</label><div style="display:flex;flex-wrap:wrap;gap:8px 16px">{"".join(f'<label class="chk" style="color:var(--ink)"><input type="checkbox" name="categories" value="{e(c[1])}"> {e(c[1])}</label>' for c in CATS)}</div></div>
<div><label class="f" for="s-moq">Typical MOQ</label><input class="in" id="s-moq" name="moq" placeholder="e.g. 50 pcs per model"></div>
<div><label class="f" for="s-cert">Certifications <i>(optional)</i></label><input class="in" id="s-cert" name="certifications" placeholder="e.g. IATF 16949"></div>
<div class="full"><label class="f" for="s-mk">Markets you already supply</label><input class="in" id="s-mk" name="markets"></div>
<div class="full"><label class="f">Catalogue, price list or photos</label><label class="drop" data-drop><input type="file" name="file" accept=".pdf,.xlsx,.csv,image/*" multiple>Drop PDF, Excel or images, or tap to choose</label></div>
<div class="full"><label class="f" for="s-msg">Message</label><textarea class="in" id="s-msg" name="message"></textarea></div>
<div class="full"><label class="chk"><input type="checkbox" name="consent" required> <span>I agree that Mega Power may use these details to review this offer (<a href="{r}privacy-policy/">privacy</a>).</span></label><div class="err">Please tick to continue.</div></div>
</div>
<div class="demo-flag">{I['info']}<span>Demo: saved to the staff inbox in this browser. Files are not uploaded in the demo, only their names are kept.</span></div>
<button class="btn btn-o" type="submit" style="width:100%">Send supplier introduction</button></form>'''


def bulk_tool(r, hid="bulk"):
    return f'''<div class="form-card bulk" id="{hid}" data-bulk style="margin-bottom:22px">
<h2 style="font-size:1.2rem">{I['list']} Have a parts list? Check it in one go</h2>
<p class="note" style="margin-top:-4px">Paste OEM or part numbers, one per line, with an optional quantity after a comma (for example <span class="mono">8730R, 10</span>). We match each line against the catalogue.</p>
<label class="sr" for="{hid}-t">Parts list</label><textarea class="in mono" id="{hid}-t" data-bulk-in style="min-height:110px" placeholder="8730R, 10&#10;4M0 816 421B, 4&#10;1787, 6"></textarea>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:10px"><button class="btn btn-n btn-s" type="button" data-bulk-go>Check my list</button><button class="btn btn-g btn-s" type="button" data-bulk-ex>Use an example</button></div>
<div data-bulk-out></div></div>'''

def export_page():
    r = "../"
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">Export / global buyers</span><h1>Source automotive A/C parts from Singapore</h1><p>For distributors, workshops and parts buyers outside Singapore. Tell us the vehicle, chassis or OEM number, the quantity and where it ships, and our team replies with what we can supply.</p></div></section>
<section class="sec"><div class="wrap two">
<div>{bulk_tool(r)}{lead_form("EXPORT", r)}</div>
<div style="display:flex;flex-direction:column;gap:18px">
<div class="side rv"><h3>How an export enquiry works</h3><ol class="steps-s"><li><b>Send your list</b>Part numbers, vehicles or chassis numbers, with quantities and destination.</li><li><b>We identify the parts</b>Our team checks each reference and fitment.</li><li><b>You get one quotation</b>Covering the parts we can supply, with shipping and payment terms.</li><li><b>Confirm and ship</b>Packing and shipping as agreed in the quotation.</li></ol></div>
<div class="side rv"><h3>What to send for a fast quote</h3><ul class="ticks"><li>Make, model and year, or the VIN / chassis number</li><li>OEM or part number, if you have it</li><li>Quantity per part</li><li>Destination country and port or city</li><li>A photo of the old part's label helps</li></ul></div>
<div class="side rv"><h3>Parts we list</h3><p style="font-size:.93rem">Compressors, condensers, cooling coils, fans and blower motors, filters, valves, driers, compressor oil and refrigerant, for passenger cars, commercial vehicles, trucks and excavators.</p><a href="{r}our-products.html">Search the catalogue</a></div>
<div class="side rv"><h3>Why buyers source from Mega Power</h3><ul class="ticks"><li>In the automotive A/C parts trade since 1989</li><li>Parts from makers such as Denso, Sanden, Behr and Valeo in our listings</li><li>Passenger cars, commercial vehicles, trucks and excavators</li><li>Each reference checked by staff before quoting</li></ul></div>
<div class="side rv"><h3>Contact</h3><p style="font-size:.93rem;margin:0"><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="tel:{TEL_MAIN_H}">{TEL_MAIN}</a><br><span class="note">WhatsApp and WeChat for export: to be added once confirmed.</span></p></div>
</div></div></section>'''
    shell("export/index.html", "Car A/C Parts Exporter Singapore | Mega Power",
          "Overseas distributors and workshops: request a quotation for automotive A/C compressors, condensers and cooling parts from Mega Power, Singapore.",
          body, active="export", crumbs=[("Export", "export/")])

def supplier_page():
    r = "../"
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">Supply to Mega Power</span><h1>Supply automotive A/C parts to Mega Power</h1><p>Manufacturers, brand owners and distributors of automotive A/C and cooling parts: introduce your range to our purchasing team in Singapore. Takes about 3 minutes.</p></div></section>
<section class="sec"><div class="wrap two">
<div>{lead_form("SUPPLIER", r)}</div>
<div style="display:flex;flex-direction:column;gap:18px">
<div class="side rv"><h3>Ranges we source</h3><div class="brands" style="gap:6px">{"".join(f'<span style="font-size:.8rem;padding:5px 10px;letter-spacing:0">{e(c[1])}</span>' for c in CATS[:7] + CATS[10:])}</div><p style="font-size:.9rem;margin:12px 0 0">For passenger cars, commercial vehicles, trucks and excavators. Makers in our current listings include Denso, Sanden, Behr and Valeo.</p></div>
<div class="side rv"><h3>What helps us review your offer</h3><ul class="ticks"><li>Product range by category, with OEM references</li><li>Catalogue or price list (PDF or Excel)</li><li>Minimum order quantity</li><li>Certifications and factory details</li><li>Markets you already supply</li></ul></div>
<div class="side rv"><h3>What happens next</h3><ol style="padding-left:18px;margin:0;font-size:.93rem"><li>Our purchasing team reviews the range.</li><li>If it fits, we ask for samples or more detail.</li><li>We reply either way.</li></ol><p class="note" style="margin-top:10px">Reply timing to be confirmed by Mega Power.</p></div>
</div></div></section>'''
    shell("become-a-supplier/index.html", "Supply Car A/C Parts to Mega Power Singapore",
          "Manufacturers and distributors of automotive A/C and cooling parts: send your range, catalogue and MOQ to Mega Power's purchasing team.",
          body, active="supplier", crumbs=[("Become a supplier", "become-a-supplier/")])

def local_page():
    r = "../"
    br = "".join(f'<div class="br rv"><b>{e(n)}</b><p>{e(a)}</p><a class="btn btn-g btn-s" href="tel:+65{t.replace(" ","")}">{I["phone"]} {t}</a></div>' for n, a, t, f in BRANCHES)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<span class="eyebrow">Singapore workshops</span><h1>Parts for the job, from your nearest branch</h1><p>Search the catalogue, then call a branch or send the car details. Our team checks fitment before you collect.</p></div></section>
<section class="sec" style="padding-bottom:0"><div class="wrap">
<div class="callstrip rv"><b>{I['phone']} Need it today? Call your nearest branch</b><div>{"".join(f'<a class="btn btn-g btn-s" href="tel:+65{t.replace(" ","")}"><span>{e(n)}</span> {t}</a>' for n, a, t, f in BRANCHES)}</div></div>
<form class="qbox form-card" data-finder="main" action="{r}our-products.html" role="search" style="margin-top:18px"><label class="f" for="q-ws">Check the part first</label><div class="qrow"><input class="in" id="q-ws" name="q" autocomplete="off" placeholder="e.g. W205 compressor or 1787" data-live><button class="btn btn-o" type="submit">{I['search']} Search</button></div><div class="live" role="listbox"></div></form>
</div></section>
<section class="sec" style="padding-top:28px"><div class="wrap two">
<div>{lead_form("LOCAL", r)}</div>
<div style="display:flex;flex-direction:column;gap:18px">
<div class="side rv"><h3>WhatsApp message (preview)</h3><p class="note" style="margin-top:0">This message is ready to send once Mega Power confirms its WhatsApp number.</p><div class="wa-prev" data-wa-preview>Hello Mega Power, I am enquiring about a part found on your website. My vehicle details are …</div>
<div style="display:flex;gap:8px;margin-top:10px;flex-wrap:wrap"><button class="btn btn-g btn-s" type="button" data-copy-wa>Copy message</button><span class="tag tag-a" style="align-self:center">WhatsApp number pending confirmation</span></div></div>
<div class="side rv"><h3>Branches</h3><div class="branches" style="grid-template-columns:1fr">{br}</div></div>
</div></div></section>'''
    shell("singapore-workshops/index.html", "Car A/C Parts for Singapore Workshops | Mega Power",
          "Singapore workshops: find car A/C parts by make, model or OEM number and enquire at Mega Power's Ang Mo Kio, Toh Guan, Kaki Bukit or Soon Lee branch.",
          body, active="local", crumbs=[("Singapore workshops", "singapore-workshops/")])

def rfq_page():
    r = "../"
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Your enquiry list</h1><p>Parts you add while browsing are kept here. Choose whether you are an overseas buyer or a Singapore workshop, then send one enquiry for the whole list.</p></div></section>
<section class="sec" style="padding-top:34px"><div class="wrap two">
<div>
<div class="basket" data-basket></div>
{bulk_tool(r)}
<div class="tabs" role="tablist" style="border-radius:12px 12px 0 0;overflow:hidden;border:1px solid var(--line);border-bottom:0;grid-template-columns:1fr 1fr" data-rfq-tabs>
<button role="tab" aria-selected="true" data-rt="EXPORT">{I['globe']}Overseas buyer</button><button role="tab" aria-selected="false" data-rt="LOCAL">{I['wrench']}Singapore workshop</button></div>
<div data-rt-panel="EXPORT">{lead_form("EXPORT", r)}</div>
<div data-rt-panel="LOCAL" hidden>{lead_form("LOCAL", r)}</div>
</div>
<div style="display:flex;flex-direction:column;gap:18px">
<div class="side" id="vin"><h3>Don't know the part? Send the chassis number</h3>{vin_form(r)}</div>
<div class="side"><h3>Prefer to talk?</h3><p style="font-size:.93rem;margin:0"><a href="tel:{TEL_MAIN_H}">{TEL_MAIN}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
</div></div></section>'''
    shell("rfq/index.html", "Request a Quote | Mega Power", "Send one enquiry for the automotive A/C parts on your list. Mega Power confirms fitment and replies with a quotation.",
          body, crumbs=[("Enquiry list", "rfq/")])

def vin_form(r):
    return f'''<form data-lead="EXPORT" data-sub="VIN_MATCH" novalidate>
<div class="fgrid">
<div class="full"><label class="f" for="v2-vin">VIN / chassis number</label><input class="in mono" id="v2-vin" name="vin" required minlength="6" style="text-transform:uppercase"><div class="err">Enter at least 6 characters.</div></div>
<div><label class="f" for="v2-make">Make <i>(optional)</i></label><input class="in" id="v2-make" name="vehicle"></div>
<div><label class="f" for="v2-part">Part needed</label><input class="in" id="v2-part" name="part" required><div class="err">Which part?</div></div>
<div><label class="f" for="v2-name">Name</label><input class="in" id="v2-name" name="name" required><div class="err">Please add your name.</div></div>
<div><label class="f" for="v2-c">Email or WhatsApp</label><input class="in" id="v2-c" name="contact" required><div class="err">We need a way to reply.</div></div>
<div class="full"><label class="f" for="v2-country">Country</label><input class="in" id="v2-country" name="country"></div>
<div class="full"><label class="chk"><input type="checkbox" name="consent" required> <span>I agree to the <a href="{r}privacy-policy/">privacy notice</a>.</span></label><div class="err">Please tick to continue.</div></div>
</div>
<p class="note" style="margin:10px 0">Chassis numbers are only seen by Mega Power staff and are never shown on the website.</p>
<button class="btn btn-n" type="submit" style="width:100%">Send to our team</button></form>'''

def about_page():
    r = "../"
    br = "".join(f'<div class="br rv"><b>{e(n)}</b><p>{e(a)}<br>Tel {t} · Fax {f}</p><a class="btn btn-g btn-s" href="tel:+65{t.replace(" ","")}">{I["phone"]} Call {e(n)}</a></div>' for n, a, t, f in BRANCHES)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>About Mega Power</h1><p>{LEGAL} has supplied automotive air-conditioning parts in Singapore since 1989.</p></div></section>
<section class="sec"><div class="wrap two">
<div class="rv"><h2>A one-stop A/C parts supplier for the trade</h2>
<p>Since 1989, Mega Power has supplied automotive air-con parts to workshops and car garages across Singapore. The range covers passenger vehicles, commercial vehicles, trucks and excavators.</p>
<p>The catalogue is organised into twelve part types, from compressors, condensers and cooling coils to valves, driers, compressor oil and refrigerant, plus workshop equipment and A/C machines.</p>
<h3 style="margin-top:28px">Component brands in our current listings</h3>
<div class="brands"><span>DENSO</span><span>SANDEN</span><span>BEHR</span><span>VALEO</span><span>OPTEON</span></div>
<p class="note" style="margin-top:12px">Brand names identify the maker of each listed part. They do not mean Mega Power is an appointed distributor.</p>
</div>
<div class="side rv"><h3>Company facts</h3><table class="spec" style="margin:0"><tr><th>Name</th><td>{LEGAL}</td></tr><tr><th>Serving the trade since</th><td>1989</td></tr><tr><th>Branches</th><td>4 in Singapore</td></tr><tr><th>Main line</th><td><a href="tel:{TEL_MAIN_H}">{TEL_MAIN}</a></td></tr><tr><th>Email</th><td><a href="mailto:{EMAIL}">{EMAIL}</a></td></tr><tr><th>Vehicles</th><td>Passenger, commercial, trucks, excavators</td></tr></table></div>
</div></section>
<section class="sec bg-w"><div class="wrap"><h2>Our branches</h2><div class="branches">{br}</div></div></section>'''
    shell("about-us/index.html", "About Mega Power | Car A/C Parts Since 1989",
          "Mega Power: automotive air-con parts supplier in Singapore since 1989, with branches in Ang Mo Kio, Toh Guan, Kaki Bukit and Soon Lee.",
          body, active="about", crumbs=[("About", "about-us/")])

def contact_page():
    r = "../"
    br = "".join(f'<div class="br rv"><b>{e(n)}</b><p>{e(a)}<br>Tel {t} · Fax {f}</p><a class="btn btn-g btn-s" href="tel:+65{t.replace(" ","")}">{I["phone"]} {t}</a></div>' for n, a, t, f in BRANCHES)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Contact Mega Power</h1><p>Main line <a style="color:#fff" href="tel:{TEL_MAIN_H}">{TEL_MAIN}</a> · <a style="color:#fff" href="mailto:{EMAIL}">{EMAIL}</a></p></div></section>
<section class="sec"><div class="wrap">
<div class="funnels" style="margin-bottom:40px">
<a class="fn dark" href="{r}export/" style="text-decoration:none"><span class="ic">{I['globe']}</span><h3>Export enquiry</h3><p>Overseas buyers: quotation by quantity and destination.</p></a>
<a class="fn" href="{r}become-a-supplier/" style="text-decoration:none;color:inherit"><span class="ic">{I['factory']}</span><h3>Supplier offer</h3><p>Introduce your products to our purchasing team.</p></a>
<a class="fn" href="{r}singapore-workshops/" style="text-decoration:none;color:inherit"><span class="ic">{I['wrench']}</span><h3>Workshop enquiry</h3><p>Local parts enquiry with your car details.</p></a>
</div>
<h2>Branches</h2><div class="branches">{br}</div>
<p class="note" style="margin-top:16px">Opening hours and the WhatsApp number will be added once Mega Power confirms them.</p>
</div></section>'''
    shell("contact-us/index.html", "Contact Mega Power | Car A/C Parts Singapore",
          "Contact Mega Power Engineering & Trading: main line +65 6842 3389, enquiry@megapower.com.sg, and four branches in Singapore.",
          body, active="contact", crumbs=[("Contact", "contact-us/")])

# ---------------- articles (drafts for technical review) ----------------
ARTS = [
 ("how-to-identify-a-car-aircon-compressor", "How to identify a car A/C compressor before ordering", "comp",
  "Read the label on the compressor body first. It usually carries the maker (for example Denso, Sanden or Valeo) and a part number. Then note the car's make, model, year and engine, and the refrigerant type shown on the label under the bonnet. Send all of these with your enquiry.",
  [("Where to find the part number", "<p>Most compressors carry a sticker or stamped plate on the body with the manufacturer's name and part number. A vehicle maker (OEM) number may also appear. Clean the label gently before taking a photo; do not scrape it.</p>"),
   ("What else identifies the compressor", "<ul><li>Refrigerant type: most cars use R134a or R1234yf. The type is on a label under the bonnet.</li><li>The make, model, year and engine of the car.</li><li>The VIN or chassis number, which pins down the exact build.</li><li>A photo of the whole compressor, including the pulley, the pipe connections and the electrical plug.</li></ul>"),
   ("Why the same model can use different compressors", "<p>One model can be built with different compressors for different engines, markets or years. Our own listings show this: the Volkswagen Golf 5 appears twice, once with a Denso Europe compressor (<a href=\"../../our-products/compressors/volkswagen-golf-5-y13-compressor.html\">DCP32060</a>) and once with a Denso Japan compressor (<a href=\"../../our-products/compressors/volkswagen-golf-5-compressor.html\">437100-8011</a>). That is why we check the chassis number before quoting.</p>"),
   ("Sending the enquiry", "<ol><li>Search the catalogue by the part number on the label.</li><li>If there is no exact match, search by vehicle.</li><li>Add the part to your enquiry list, or send the chassis number if you are unsure.</li></ol>")]),
 ("why-oem-numbers-differ-by-market", "Why A/C part OEM numbers differ between markets", "hash",
  "A part can carry several numbers: the vehicle maker's OEM number, the part maker's own number and cross-references used by resellers. The same car model sold in different markets may also be built with different suppliers' parts, so one model can map to more than one number.",
  [("The three kinds of number", "<ul><li><b>OEM number:</b> the vehicle maker's number for the part.</li><li><b>Manufacturer part number:</b> the part maker's own number, such as a Denso or Sanden reference.</li><li><b>Cross-reference:</b> another number said to fit the same application. These need checking before you rely on them.</li></ul>"),
   ("Why numbers change by market", "<p>Car makers may source a part from different suppliers for different factories or regions, and specifications change between model years. Refrigerant is one example: the European Union's mobile air-conditioning directive (2006/40/EC) moved new cars to lower-impact refrigerants such as R1234yf, so parts for the same model may differ by year and market.</p>"),
   ("How our search handles it", "<p>Our search ignores spaces, dashes and capitals, so <span class=\"mono\">4M0 816 421B</span> and <span class=\"mono\">4M0816421B</span> find the same part. It labels results as an exact reference match or a possible match, and never treats an unchecked cross-reference as interchangeable. Our team confirms fitment before quoting.</p>")]),
 ("how-to-send-vehicle-details-for-overseas-sourcing", "How to send vehicle details for overseas parts sourcing", "globe",
  "Send the VIN or chassis number, the make, model, year and engine, the market the car was sold in, the part needed with any number on its label, a clear photo, the quantity and the destination. With these, our team can identify the part and quote in one reply.",
  [("Checklist", "<ol><li>VIN or chassis number.</li><li>Make, model, year and engine size.</li><li>The market the car was sold in, and left- or right-hand drive.</li><li>Part needed, with any OEM or part number from the label.</li><li>A photo of the old part and its label.</li><li>Quantity per part.</li><li>Destination country and port or city.</li></ol>"),
   ("Why the chassis number matters", "<p>The chassis number identifies the exact build of the car, which is how parts are matched when the model name alone is not enough. Chassis numbers you send are only seen by Mega Power staff.</p>"),
   ("Where to send it", "<p>Use the <a href=\"../../export/\">export enquiry form</a> or the <a href=\"../../rfq/#vin\">chassis number form</a>. You can attach a photo or a parts list.</p>")]),
]

def articles():
    r = "../"
    cards = "".join(f'<a class="acard rv" href="{s}/"><div class="im">{I[ic]}</div><div class="bd"><b>{e(t)}</b><small>Guide · draft for technical review</small></div></a>' for s, t, ic, a, secs in ARTS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Guides for parts buyers</h1><p>Short guides on identifying automotive A/C parts and sending enquiries.</p></div></section>
<section class="sec"><div class="wrap"><div class="acards">{cards}</div></div></section>'''
    shell("articles/index.html", "A/C Parts Buyer Guides | Mega Power", "Guides on identifying automotive A/C compressors, reading OEM numbers and sending vehicle details for parts sourcing.",
          body, crumbs=[("Guides", "articles/")])
    for s, t, ic, ans, secs in ARTS:
        r = "../../"
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>{e(t)}</h1><p>Mega Power · draft for review by Mega Power's technical team · {READ}</p></div></section>
<section class="sec"><div class="wrap art">
<p class="ans">{e(ans)}</p>
{"".join(f"<h2>{e(h)}</h2>{b}" for h, b in secs)}
<div class="side" style="margin-top:32px"><h3>Need a part identified?</h3><p style="font-size:.93rem">Send the chassis number or a photo of the label.</p><a class="btn btn-o" href="{r}rfq/#vin">Send chassis number</a> <a class="btn btn-g" href="{r}our-products.html">Search the catalogue</a></div>
</div></section>'''
        sch = [{"@type": "Article", "headline": t, "datePublished": TODAY, "dateModified": TODAY, "author": {"@id": BASE + "/#org"}, "publisher": {"@id": BASE + "/#org"}, "image": BASE + "/og.jpg", "mainEntityOfPage": BASE + f"/articles/{s}/"}]
        tt = t if len(t + " | Mega Power") > 60 else t + " | Mega Power"
        shell(f"articles/{s}/index.html", tt[:60], ans[:157] + ("…" if len(ans) > 157 else ""), body, crumbs=[("Guides", "articles/"), (t, f"articles/{s}/")], schema=sch, og_type="article")

def legal():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Privacy policy</h1><p>Draft for Mega Power to review before launch.</p></div></section>
<section class="sec"><div class="wrap art">
<p>{LEGAL} collects the details you send in enquiry forms (name, company, contact details, vehicle and part details, VIN or chassis number, and files you attach) only to reply to your enquiry and supply parts.</p>
<h2>How we use your details</h2><ul><li>To identify parts and send quotations.</li><li>To contact you about your enquiry by the channel you choose.</li><li>We do not sell your details. VIN and chassis numbers are seen only by Mega Power staff and never shown on the website.</li></ul>
<h2>Keeping and deleting data</h2><p>Enquiries are kept for as long as needed to handle the enquiry and any order, then deleted. You can ask us to see, correct or delete your details.</p>
<h2>Contact</h2><p>Data protection contact: <a href="mailto:{EMAIL}">{EMAIL}</a> (Data Protection Officer to be named by Mega Power).</p>
</div></section>'''
    shell("privacy-policy/index.html", "Privacy Policy | Mega Power", "How Mega Power Engineering & Trading handles details sent through enquiry forms.", body, crumbs=[("Privacy", "privacy-policy/")])
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Terms of use</h1><p>Draft for Mega Power to review before launch.</p></div></section>
<section class="sec"><div class="wrap art">
<p>Product details on this website are given for identification. Fitment, availability and prices are confirmed by Mega Power in a written quotation before any order.</p>
<p>OEM and part numbers and brand names identify the parts listed. They belong to their owners and do not mean Mega Power is an appointed distributor unless stated.</p>
</div></section>'''
    shell("terms-conditions/index.html", "Terms of Use | Mega Power", "Terms for using the Mega Power website and product information.", body, crumbs=[("Terms", "terms-conditions/")])

def demo_guide():
    r = "../"
    steps = [
     ("Search a part number", "our-products.html?q=8730R", "Type 8730R. The BMW 2 Series F45/F46 compressor comes up as an exact reference match, with R1234YF and PAG-46."),
     ("Search like a buyer", "our-products.html?q=BMW%20F45%20compressor", "Type “BMW F45 compressor”: the same part, found by vehicle and part type."),
     ("Spaces and dashes don't matter", "our-products.html?q=4M0816421B", "4M0816421B finds the Audi Q7 condenser listed as 4M0 816 421B, with a fitment check note."),
     ("Chassis code search", "our-products.html?q=Mercedes%20W205%20compressor", "Mercedes W205 compressor finds the Sanden Europe compressor, reference 1787."),
     ("No made-up results", "our-products.html?q=Mercedes%20W210%20compressor", "Mercedes W210 compressor is not in the catalogue, so the search says so and offers “Request sourcing”."),
     ("Send an export RFQ", "our-products/compressors/bmw-2-series-f45-46-compressor.html", "Open the BMW part, set a quantity, tap Add to RFQ, then send the export form. It appears in the staff inbox under Export."),
     ("Supplier offer", "become-a-supplier/", "Fill in the supplier form with a demo catalogue file. It lands under Supplier enquiries."),
     ("Workshop enquiry", "singapore-workshops/?p=mp-0004", "The workshop form and WhatsApp message are pre-filled with the product. The WhatsApp number is marked as pending."),
     ("Staff: add a product", "staff/#new", "Add a DEMO product with a photo and part number, publish it, then search for it on the public site."),
     ("Staff: CSV import", "staff/#import", "Load the sample CSV. The importer flags a duplicate SKU and a reference already used, and waits for approval."),
     ("Staff: old URLs", "staff/#migration", "See how every current megapower.com.sg product URL is kept or redirected (planned, not live yet)."),
     ("Try it on a phone", "", "Open this page on a phone: search, enquiry list and forms fit the screen with a bottom action bar."),
    ]
    li = "".join(f'<li class="br rv" style="list-style:none"><b>{i+1}. {e(t)}</b><p>{e(d)}</p>{f"<a class=\"btn btn-o btn-s\" href=\"{r}{u}\">Try it</a>" if u else ""}</li>' for i, (t, u, d) in enumerate(steps))
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Demo tour</h1><p>Twelve things to try in this mockup. Everything you add or send stays in this browser; nothing reaches customers or the live website.</p></div></section>
<section class="sec"><div class="wrap"><ol class="branches" style="padding:0;margin:0">{li}</ol>
<p style="margin-top:24px"><button class="btn btn-g" type="button" data-reset-demo>Reset demo data in this browser</button></p></div></section>'''
    shell("demo-guide/index.html", "Demo Tour | Mega Power Preview", "Guided tour of the Mega Power website mockup.", body, crumbs=[("Demo tour", "demo-guide/")], index=False)

def staff():
    r = "../"
    doc = f"""<!doctype html>
<html lang="en-SG" data-root="{r}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Staff dashboard | Mega Power (demo)</title><meta name="robots" content="noindex,nofollow">
<link rel="icon" href="{r}favicon.ico" sizes="48x48"><link rel="apple-touch-icon" href="{r}apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{r}{asset('mp.css')}"><link rel="stylesheet" href="{r}{asset('staff.css')}">
<script>window.MP_ROOT="{r}";</script>
</head><body class="st">
<div id="app"><p style="padding:40px">Loading staff dashboard…</p></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="{r}{asset('data.js')}"></script><script src="{r}{asset('mp.js')}"></script><script src="{r}{asset('staff.js')}"></script>
</body></html>"""
    (OUT / "staff").mkdir(parents=True, exist_ok=True)
    (OUT / "staff/index.html").write_text(doc)

def notfound():
    body = f'''<section class="ph-hd"><div class="wrap"><h1>Page not found</h1><p>The page may have moved. Search the catalogue or go to the homepage.</p></div></section>
<section class="sec"><div class="wrap"><form class="qbox" data-finder="main" action="/our-products.html"><label class="f" for="q-404">Search products</label><div class="qrow"><input class="in" id="q-404" name="q" placeholder="Part number or vehicle"><button class="btn btn-o">Search</button></div></form></div></section>'''
    shell("404.html", "Page not found | Mega Power", "Page not found.", body, index=False)

def datajs():
    keep = ["id", "cat", "slug", "orig", "name", "make", "model", "codes", "brand", "country", "gas", "oil", "refs", "image", "years", "url", "old", "src", "status", "verified", "alt", "desc", "weight", "staff_note"]
    data = {"read": READ, "cats": [{"slug": s, "name": n, "line": d, "icon": ic} for s, n, d, ic in CATS],
            "products": [{k: p[k] for k in keep if k in p} for p in PRODUCTS],
            "branches": [{"name": n, "address": a, "tel": t, "fax": f} for n, a, t, f in BRANCHES],
            "tel": TEL_MAIN, "email": EMAIL, "base": BASE, "old": OLD}
    (OUT / "data.js").write_text("window.MP_DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    (HERE / "data.js").write_text((OUT / "data.js").read_text())

def statics():
    for f in ("favicon.ico", "favicon-48.png", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "og.jpg"):
        shutil.copy(HERE / "assets" / f, OUT / f)
    (OUT / "img").mkdir(exist_ok=True)
    for s, n, d, ic in CATS:
        (OUT / "img" / f"ph-{ic}.svg").write_text(PLACEHOLDER(ic))
    for f in ("mp.css", "mp.js", "staff.js", "staff.css", "wa.js", "chat.js"):
        shutil.copy(HERE / f, OUT / f)
    (OUT / "site.webmanifest").write_text(json.dumps({"name": LEGAL, "short_name": BRAND, "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}], "theme_color": "#0A1F35", "background_color": "#F7F5F0", "display": "standalone", "start_url": "./"}))
    key = "c4f2a8e61b9d47f0a3e5d8c2b7f1e690"
    (OUT / f"{key}.txt").write_text(key)
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Applebot-Extended", "DuckAssistBot"]
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /staff/\nDisallow: /demo-guide/\nDisallow: /our-products/item.html\n\n" +
        "".join(f"User-agent: {b}\nAllow: /\nDisallow: /staff/\n" for b in bots) + f"\nSitemap: {BASE}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u, pr in pages) + "</urlset>\n")
    llms = [f"# {LEGAL}", "", f"> Singapore supplier of automotive air-conditioning and cooling parts since 1989, for workshops, overseas buyers and parts suppliers. Four branches in Singapore. Main line {TEL_MAIN}, {EMAIL}. Enquiry-based: no public prices.", "",
            "## Branches"] + [f"- {n}: {a}. Tel +65 {t}" for n, a, t, f in BRANCHES] + ["", "## Product categories"] + [f"- {n}: {BASE}/our-products/{s}.html" for s, n, d, ic in CATS] + \
           ["", "## Listed products (reference numbers as listed)"] + [f"- {p['name']}" + (f" (OEM {p['refs'][0]['n']})" if p["refs"] else "") + f": {BASE}/{p['url']}" for p in PRODUCTS] + \
           ["", "## Enquiries", f"- Export quotation: {BASE}/export/", f"- Become a supplier: {BASE}/become-a-supplier/", f"- Singapore workshops: {BASE}/singapore-workshops/", "", "Fitment is confirmed by Mega Power staff for each enquiry, using the VIN or chassis number."]
    (OUT / "llms.txt").write_text("\n".join(llms) + "\n")
    (OUT / "htaccess.txt").write_text("""# Mega Power (www.megapower.com.sg) - for go-live only. Preview is hidden by the parent preview/.htaccess header.
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^ https://www.megapower.com.sg%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTP_HOST} ^megapower\\.com\\.sg$ [NC]
RewriteRule ^ https://www.megapower.com.sg%{REQUEST_URI} [L,R=301]
# Old Magento paths -> new pages (product and category URLs are unchanged)
Redirect 301 /about-who-we-are/ /about-us/
Redirect 301 /about-quality-service/ /about-us/
Redirect 301 /our-services/ /singapore-workshops/
Redirect 301 /catalogsearch/advanced/ /our-products.html
Redirect 301 /checkout/cart/ /rfq/
Redirect 301 /wishlist/ /rfq/
Redirect 301 /customer/account/ /rfq/
Redirect 301 /career-opportunities/ /contact-us/
Redirect 301 /terms-conditions /terms-conditions/
Redirect 301 /privacy-policy /privacy-policy/
ErrorDocument 404 /404.html
<IfModule mod_headers.c>
<FilesMatch "\\.(html)$">
Header set Cache-Control "max-age=3600, public"
</FilesMatch>
</IfModule>
<If "%{REQUEST_URI} =~ m#^/staff/#">
Header always set X-Robots-Tag "noindex, nofollow"
</If>
""")

if __name__ == "__main__":
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    datajs(); home(); catalogue(); [product(p) for p in PRODUCTS]; item_page()
    export_page(); supplier_page(); local_page(); rfq_page(); about_page(); contact_page(); articles(); legal(); demo_guide(); staff(); notfound()
    datajs(); statics()
    print(f"pages in sitemap {len(pages)}, products {len(PRODUCTS)}, files {sum(1 for _ in OUT.rglob('*') if _.is_file())}")
