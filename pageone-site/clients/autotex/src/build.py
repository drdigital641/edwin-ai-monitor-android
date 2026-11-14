#!/usr/bin/env python3
"""Autotex Aircon Enterprise - Kia & Hyundai parts shop, live on https://autotexautoparts.com.sg.

Run:  python3 build.py OUT_DIR        (default ../site)      then upload OUT_DIR
Catalogue = database (Base44 app 6ae3683191b1a44205dbf5ec, entities AtCar / AtProduct / AtPhoto), exported as raw API
arrays into src/db/cars.json, src/db/products.json and (optional) src/db/photos.json. See README.md.
catalog.py only defines BRANDS, CATS and PARTS (the part types Autotex supplies). No sample data, no sample prices.
Facts: ACRA (UEN 52353300D, registered 24 Feb 1995, retail of motor vehicle parts), Google Business Profile
(1 Kaki Bukit Ave 6 #01-42 AutoBay@Kaki Bukit S417883, 6747 9618, 5.0 from 4 reviews), Edwin (29 Oct 2026:
Kia and Hyundai stockist, stock direct from Korea, sells to Singapore drivers at distribution price,
WhatsApp +65 9731 9547, hours Mon-Fri 9:30am-5:30pm, Sat 9:30am-3:30pm, Sunday closed).
autotex.net is NOT theirs (an Indian textile company) - never link it.
"""
import html, json, sys, datetime, hashlib, shutil, re
from pathlib import Path
from urllib.parse import quote
from catalog import BRANDS, CATS, PARTS, fits, BUNDLES, SET_DISCOUNT
from specs import spec, GB_LABEL
from partinfo import I as PINFO

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent / "site")
LIVE = True
BASE = "https://autotexautoparts.com.sg"
TODAY = datetime.date.today().isoformat()
BRAND = "Autotex"
LEGAL = "Autotex Aircon Enterprise"
UEN = "52353300D"
REG = "24 February 1995"
ADDR1 = "1 Kaki Bukit Avenue 6, #01-42"
ADDR2 = "AutoBay@Kaki Bukit, Singapore 417883"
TEL = "6747 9618"; TEL_H = "+6567479618"
WA = "6597319547"; WA_SHOW = "+65 9731 9547"
HOURS = [("Monday to Friday", "9:30am to 5:30pm"), ("Saturday", "9:30am to 3:30pm"), ("Sunday", "closed")]
PRIVACY_UPDATED = "8 November 2026"
HOURS_LINE = "Mon-Fri 9:30am-5:30pm, Sat 9:30am-3:30pm, Sunday closed"
GMAP = "https://www.google.com/maps/search/?api=1&query=Autotex+Aircon+Enterprise+1+Kaki+Bukit+Ave+6+%2301-42+Singapore+417883"
INDEXNOW = "7d3e9a51c4b84f2e9a0c6b1d58e2f437"
DB_URL = "https://autotex-catalogue-05dbf5ec.base44.app/"
e = lambda s: html.escape(str(s), quote=True)

# ---------------- catalogue (database exports + catalog.py definitions) ----------------
def dbfile(name, default):
    f = HERE / "db" / name
    return json.loads(f.read_text()) if f.exists() else default

def is_pub(row):
    return (row.get("status") or "published") == "published"

BR = {b: n for b, n in BRANDS}
CARS = [c for c in dbfile("cars.json", []) if is_pub(c) and c.get("b") in BR and c.get("key")]
CARS.sort(key=lambda c: (c["b"], (c.get("name") or "").lower(), (c.get("code") or "").lower()))  # A-Z everywhere (Edwin, 30 Oct 2026)
M = {c["key"]: dict(id=c["key"], b=c["b"], name=c["name"], code=c.get("code") or "", years=c.get("years") or "",
                    alias=list(c.get("alias") or []), fuel=c.get("fuel") or "petrol") for c in CARS}
C = {c[0]: dict(id=c[0], name=c[1], line=c[2], icon=c[3]) for c in CATS}
P = {p[0]: dict(id=p[0], cat=p[1], name=p[2], alias=p[3], side=p[4], unit=p[5], need=p[6]) for p in PARTS}
PT = {p[0]: p for p in PARTS}

def mlabel(m): return f"{BR[m['b']]} {mpar(m)}" if m["code"] else f"{BR[m['b']]} {m['name']}"
def myears(m): return m["years"].replace("-now", " onwards")
# model name with generation code; cars like EV3 / Inster have no code, so never leave "()" or ", ," behind
def mn(m): return m["name"] + " " + m["code"] if m.get("code") else m["name"]
def mpar(m): return m["name"] + " (" + m["code"] + ")" if m.get("code") else m["name"]
def mcy(m, yrs): return "(" + m["code"] + ", " + yrs + ")" if m.get("code") else "(" + yrs + ")"
def car_parts(m): return [P[p[0]] for p in PARTS if fits(m["fuel"], p)]

# photos: AtPhoto rows exported to db/photos.json are written to assets/p/<id>.jpg by pull_photos.py
PHOTO_IDS = {r.get("group") or r["id"] for r in dbfile("photos.json", []) if r.get("id") and r.get("data")}  # chunked photos share a "group"
SEEN_URLS = set()

def photo_src(entry):
    """Return (path-or-url used in <img>, absolute url) for a photo entry, or None if it cannot be shown statically."""
    if not isinstance(entry, str): return None
    if re.match(r"https?://", entry): return entry, entry
    if entry.startswith("b44photo:") and entry[9:] in PHOTO_IDS:
        p = f"assets/p/{entry[9:]}.jpg"
        return p, f"{BASE}/{p}"
    return None

PRODUCTS = []
_rows = [x for x in dbfile("products.json", []) if is_pub(x) and x.get("key") and x.get("m") in M]
_rows.sort(key=lambda x: str(x.get("created_date") or ""))
_first = {}
for row in _rows:
    m = M[row["m"]]
    pid = row.get("p") or "other"
    if pid in P:
        part = P[pid]
    else:
        pid = "other"
        part = dict(id="other", cat=row.get("pc") if row.get("pc") in C else "", name=(row.get("pn") or "Part").strip() or "Part",
                    alias=[], side=False, unit="piece", need="any")
    price = row.get("price")
    try: price = float(price) if price not in (None, "") else None
    except (TypeError, ValueError): price = None
    if price is not None and price <= 0: price = None
    if price is not None and price.is_integer(): price = int(price)
    key = str(row["key"])
    if pid != "other" and (m["id"], pid) not in _first:
        _first[(m["id"], pid)] = key; url = f"{m['b']}/{m['id']}/{pid}/"
    else:
        url = f"{m['b']}/{m['id']}/{key}/"
    if url in SEEN_URLS: continue
    SEEN_URLS.add(url)
    photos = [x for x in (row.get("photos") or []) if isinstance(x, str)]
    PRODUCTS.append(dict(id=key, m=m["id"], p=pid, pn=part["name"], pc=part["cat"], url=url, price=price, oem=(row.get("oem") or "").strip(),
                         stock=row.get("stock") if row.get("stock") in ("in", "order", "out") else "", side=row.get("side") if row.get("side") in ("L", "R", "pair") else "",
                         note=(row.get("note") or "").strip(), raw_photos=photos, updated=str(row.get("updated_date") or ""), created=str(row.get("created_date") or ""),
                         model=m, part=part, cat=C.get(part["cat"], dict(id="", name="Other parts", line="", icon="engine"))))
SIDE_L = {"L": "Left", "R": "Right", "pair": "Pair (left and right)"}
for x in PRODUCTS:
    x["title"] = f"{x['part']['name']}{' (' + SIDE_L[x['side']].split(' (')[0] + ')' if x['side'] else ''} for {mlabel(x['model'])}"
    x["photos"] = [s for s in (photo_src(p) for p in x["raw_photos"]) if s]
    x["ph_entries"] = x["raw_photos"]

def show_price(x):
    return x["price"] is not None

def money(v):
    return f"S${v:,.0f}" if float(v).is_integer() else f"S${v:,.2f}"

def price_html(x, big=False):
    if not show_price(x):
        return f'<span class="price ask{" big" if big else ""}" data-price="{e(x["id"])}">Ask for price</span>'
    return f'<span class="price{" big" if big else ""}" data-price="{e(x["id"])}">{money(x["price"])}</span>'

STOCK = {"in": ("In stock", "ok"), "order": ("Order from Korea", "warn"), "out": ("Out of stock", "out")}
AVAIL = {"in": "https://schema.org/InStock", "order": "https://schema.org/BackOrder", "out": "https://schema.org/OutOfStock"}
# Return and delivery terms (Edwin, 31 Oct 2026): 7-day return in original packaging; collect or deliver in 1 day; S$10 delivery, free above S$80.
RETURN_POLICY = {"@type": "MerchantReturnPolicy", "applicableCountry": "SG", "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                 "merchantReturnDays": 7, "returnMethod": "https://schema.org/ReturnInStore"}
SHIPPING = {"@type": "OfferShippingDetails", "shippingRate": {"@type": "MonetaryAmount", "value": "10.00", "currency": "SGD"}, "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "SG"},
            "deliveryTime": {"@type": "ShippingDeliveryTime", "handlingTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"},
                             "transitTime": {"@type": "QuantitativeValue", "minValue": 0, "maxValue": 1, "unitCode": "DAY"}}}

# ---------------- icons ----------------
SV = lambda body, vb="0 0 48 48": f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
ICON = {
 "body": SV('<path d="M5 30v-6l5-2 6-8h15l8 8 5 2v6h-4"/><path d="M13 30h22"/><circle cx="12" cy="31" r="4"/><circle cx="36" cy="31" r="4"/><path d="M17 22h20M24 14v8"/>'),
 "lamp": SV('<path d="M8 16c8-6 22-6 30 4v8c-8 6-22 6-30 0Z"/><path d="M14 20h10M14 25h14" opacity=".6"/><path d="M41 18l4-2M42 24h4M41 30l4 2"/>'),
 "pad": SV('<path d="M8 30c2-10 10-17 22-18l6 4c-10 1-17 7-19 16Z"/><path d="M12 33c3-11 12-19 25-19"/><circle cx="31" cy="15" r="1.5"/>'),
 "disc": SV('<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="6"/><circle cx="24" cy="24" r="12" opacity=".5"/><path d="M24 15v2M31 20l-2 1M31 28l-2-1M17 20l2 1M17 28l2-1M24 31v2"/>'),
 "susp": SV('<path d="M24 4v6M24 38v6"/><path d="M16 10h16M16 38h16"/><path d="M17 14l14 3-14 4 14 3-14 4 14 3-14 4"/>'),
 "mount": SV('<rect x="10" y="14" width="28" height="14" rx="4"/><circle cx="24" cy="21" r="4"/><path d="M6 34h36M14 28v6M34 28v6M24 6v8"/>'),
 "plug": SV('<path d="M20 4h8v6h-8zM18 10h12v8H18zM21 18h6v12h-6zM24 30v6M24 36l-4 4M24 36l5 3"/><path d="M18 14h12" opacity=".5"/>'),
 "coil": SV('<rect x="16" y="4" width="16" height="10" rx="2"/><path d="M19 14h10v6H19zM21 20h6v18h-6zM24 38v6"/><path d="M21 25h6M21 30h6" opacity=".5"/>'),
 "engine": SV('<path d="M8 18h6v-4h12v4h6l4 4h4v12h-4l-4 4H14l-6-6Z"/><path d="M4 22v8M17 10h6"/><circle cx="24" cy="27" r="4" opacity=".6"/>'),
 "fan": SV('<circle cx="24" cy="24" r="4"/><path d="M24 20c-2-8 0-14 6-14 4 0 4 6-2 14M28 24c8-2 14 0 14 6 0 4-6 4-14-2M24 28c2 8 0 14-6 14-4 0-4-6 2-14M20 24c-8 2-14 0-14-6 0-4 6-4 14 2"/>'),
 "bolt": SV('<path d="M27 4 10 27h12l-3 17 19-25H26Z"/>'),
 "cart": SV('<path d="M3 5h4l3 18h17l3-12H9"/><circle cx="13" cy="28" r="2"/><circle cx="25" cy="28" r="2"/>', "0 0 34 34"),
 "search": SV('<circle cx="14" cy="14" r="9"/><path d="m21 21 7 7"/>', "0 0 32 32"),
 "phone": SV('<path d="M7 4h6l3 7-4 2a16 16 0 0 0 8 8l2-4 7 3v6a3 3 0 0 1-3 3C14 29 4 19 4 7a3 3 0 0 1 3-3Z"/>', "0 0 34 34"),
 "pin": SV('<path d="M17 31s10-9 10-17a10 10 0 0 0-20 0c0 8 10 17 10 17Z"/><circle cx="17" cy="14" r="3.5"/>', "0 0 34 34"),
 "check": SV('<circle cx="17" cy="17" r="13"/><path d="m11 17 4 4 8-8"/>', "0 0 34 34"),
 "ship": SV('<path d="M4 22h26l-3 7H8Z"/><path d="M8 22V12h12v10M20 15h6v7M12 12V6h4"/>', "0 0 34 34"),
 "tag": SV('<path d="M4 4h12l14 14-12 12L4 16Z"/><circle cx="11" cy="11" r="2.5"/>', "0 0 34 34"),
}
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3a.4.4 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>'

def wa_link(text):
    return f"https://wa.me/{WA}?text={quote(text)}"

def ask_link(m, part=None):
    if part: return wa_link(f"Hi Autotex, how much is the {part['name']} for my {mlabel(m)} {m['years']}? Stock and price please. My car plate / chassis number is: ")
    return wa_link(f"Hi Autotex, I need a part for my {mlabel(m)} {m['years']}. My car plate / chassis number is: ")

def img_tag(src, r, alt, big=False, w=800, h=600):
    s = src if src.startswith("http") else r + src
    return f'<img src="{e(s)}" alt="{e(alt)}" width="{w}" height="{h}"{" fetchpriority=\"high\"" if big else " loading=\"lazy\""} decoding="async">'

# Claude-drawn illustration per part type (assets/parts/<id>.svg); a real staff photo always wins
def il_tag(pid, r, alt):
    return f'<img class="il" src="{r}assets/parts/{e(pid)}.svg" alt="{e(alt)} (illustration)" width="400" height="300" loading="lazy" decoding="async">'

def part_art(x, r, cls="art"):
    ph = x["photos"]
    if ph:
        return (f'<div class="{cls} has-ph" data-cat="{x["cat"]["id"]}" data-ph="{e(x["ph_entries"][0])}">{img_tag(ph[0][0], r, x["title"], big=cls.endswith("big"))}</div>')
    return f'<div class="{cls} has-il" data-cat="{x["cat"]["id"]}">{il_tag(x["part"]["id"], r, x["title"])}<span>Illustration</span></div>'

# ---------------- page shell ----------------
NAV = [("hyundai/", "Hyundai", "hyundai"), ("kia/", "Kia", "kia"), ("parts/", "Parts", "parts"),
       ("prices/", "Price list", "prices"), ("how-to-order/", "How to order", "order"), ("contact/", "Contact", "contact")]

MARK = ('<svg class="mark" viewBox="-16 0 224 190" aria-hidden="true" focusable="false"><g transform="skewX(-10)"><rect x="18" width="190" height="190" rx="38" fill="#D42A1E"/>'
        '<path fill="#fff" fill-rule="evenodd" d="M113 34 178 158H146L133 131H93L80 158H48ZM101 107H125L113 80Z"/></g></svg>')

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
ORG = {"@type": ["AutoPartsStore", "LocalBusiness"], "@id": BASE + "/#store", "name": LEGAL, "alternateName": BRAND,
       "url": BASE + "/", "logo": {"@type": "ImageObject", "url": BASE + "/logo.png", "width": 600, "height": 243},
       "image": BASE + "/og.jpg", "telephone": "+65 " + TEL,
       "foundingDate": "1995-02-24", "identifier": {"@type": "PropertyValue", "propertyID": "UEN", "value": UEN},
       "address": {"@type": "PostalAddress", "streetAddress": ADDR1 + ", AutoBay@Kaki Bukit", "postalCode": "417883",
                   "addressLocality": "Singapore", "addressCountry": "SG"},
       "openingHoursSpecification": [
           {"@type": "OpeningHoursSpecification", "dayOfWeek": DAYS, "opens": "09:30", "closes": "17:30"},
           {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:30", "closes": "15:30"}],
       "contactPoint": [{"@type": "ContactPoint", "telephone": "+65 9731 9547", "contactType": "sales",
                         "contactOption": "WhatsApp", "areaServed": "SG", "availableLanguage": ["English"]}],
       "areaServed": "SG", "hasMap": GMAP}

def hours_html(cls="hours"):
    return f'<dl class="{cls}">' + "".join(f"<div><dt>{d}</dt><dd>{t}</dd></div>" for d, t in HOURS) + "</dl>"

VER = {}
def asset(name):
    if name not in VER:
        VER[name] = hashlib.sha1((HERE / name).read_bytes()).hexdigest()[:8]
    return f"{name}?v={VER[name]}"

UPDATED = TODAY
SITEMAP = []
LM_NEW = {}   # page url -> content hash of this build (asset ?v= hashes and the footer year ignored)
LM_FILE = HERE / "lastmod.json"   # url -> [hash, date it last changed]; committed, so sitemap lastmod stays true (only bumped when a page's content changes)
FEED = []  # Google Merchant Center feed rows (products with a price)
def write(path, text):
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)

def shell(path, title, desc, body, active="", crumbs=None, schema=None, js=("data.js", "at.js", "wa.js"),
          css=("at.css",), index=True, prio="0.6", og_type="website", og_image=None, og_alt=None, noindex=False):
    if path == "404.html":
        r = "/"   # served for any missing URL: root-absolute links
    else:
        r = "../" * path.count("/")
    url = BASE + "/" + path.replace("index.html", "")
    ld = [dict(ORG)]
    if crumbs:
        ld.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u}
            for i, (n, u) in enumerate([("Home", "")] + crumbs)]})
    if schema: ld.extend(schema)
    ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False).replace("</", "<\\/")
    nav = "".join(f'<a href="{r}{u}"{" aria-current=\"page\"" if k == active else ""}>{e(n)}</a>' for u, n, k in NAV)
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Breadcrumb"><a href="' + r + '">Home</a>' + "".join(
            (f'<span>/</span><a href="{r}{u}">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span>/</span><b>{e(n)}</b>')
            for i, (n, u) in enumerate(crumbs)) + "</nav>"
    body = body.replace("{{CRUMBS}}", cr).replace("{{R}}", r)
    scripts = "".join(f'<script src="{r}{asset(j)}" defer></script>' for j in js)
    styles = "".join(f'<link rel="stylesheet" href="{r}{asset(c)}">' for c in css)
    robots = "noindex,follow" if noindex else "index,follow,max-image-preview:large"
    # OG fix 14 Nov 2026: always the 1200x630 JPG (per-page product photos are not 1200x630; WhatsApp needs a fixed JPG)
    ogi = f'<meta property="og:image" content="{BASE}/og.jpg"><meta property="og:image:secure_url" content="{BASE}/og.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(og_alt or "Autotex, Kia and Hyundai parts in Singapore") if og_image else "Autotex, Kia and Hyundai parts in Singapore"}">'
    doc = f"""<!doctype html>
<html lang="en-SG" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
{ogi}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}/og.jpg">
<link rel="icon" href="{r}favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="{r}icon-192.png"><link rel="apple-touch-icon" href="{r}apple-touch-icon.png"><link rel="manifest" href="{r}site.webmanifest">
<meta name="theme-color" content="#12161C">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@400;500;600;700&display=swap">
{styles}
<script>document.documentElement.classList.remove('no-js');window.AT_ROOT="{r}";</script>
<script type="application/ld+json">{ldj}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hd"><div class="wrap hd-in">
<a class="logo" href="{r}" aria-label="Autotex home">{MARK}<span class="wm">AUTOTEX<small>Korean car part stockist</small></span></a>
<form class="hd-search" action="{r}search/" role="search"><label class="sr" for="hq">Search parts</label><input id="hq" name="q" type="search" placeholder="e.g. Avante brake pads" autocomplete="off">{ICON['search']}</form>
<a class="cartb" href="{r}cart/" aria-label="Cart">{ICON['cart']}<b data-cart-count>0</b></a>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
</div><nav class="nav" id="nav" aria-label="Main"><div class="wrap">{nav}</div></nav></header>
<main id="main">
{body}
</main>
<footer class="ft"><div class="wrap ft-g">
<div><p class="ft-brand"><img src="{r}logo-dark.png" alt="Autotex, Korean car part stockist" width="240" height="97" loading="lazy"></p><p>{e(LEGAL)} · UEN {UEN}<br>Kia and Hyundai parts stockist, stocking direct from Korea.</p></div>
<div><h4>Visit</h4><p>{e(ADDR1)}<br>{e(ADDR2)}<br><a href="{GMAP}" rel="noopener">Directions</a></p></div>
<div><h4>Opening hours</h4><p>Mon-Fri 9:30am-5:30pm<br>Sat 9:30am-3:30pm<br>Sunday closed</p></div>
<div><h4>Talk to us</h4><p><a href="tel:{TEL_H}">Call {TEL}</a><br><a href="https://wa.me/{WA}" rel="noopener">WhatsApp {WA_SHOW}</a></p><p class="ft-links"><a href="{r}hyundai/">Hyundai parts</a> · <a href="{r}kia/">Kia parts</a> · <a href="{r}prices/">Price list</a> · <a href="{r}articles/">Guides</a> · <a href="{r}about/">About</a></p></div>
</div><div class="wrap ft-b">© {datetime.date.today().year} {e(LEGAL)}. Hyundai and Kia are trademarks of their owners; Autotex is an independent parts stockist. <a href="{r}privacy-policy/">Privacy Policy</a></div></footer>
<a class="wa-fab" href="https://wa.me/{WA}?text={e(quote('Hi Autotex, I need a part for my car.'))}" aria-label="WhatsApp Autotex" rel="noopener">{WA_SVG}</a>
{scripts}
</body>
</html>
"""
    write(path, doc)
    LM_NEW[url] = hashlib.sha1(re.sub(r"\?v=[0-9a-f]{8}|© \d{4}", "", doc).encode()).hexdigest()[:16]
    if index:
        SITEMAP.append((url, prio))

def card(x, r, show_model=True, show_part=True):
    t = x["title"] if (show_model and show_part) else (x["part"]["name"] + (f" ({SIDE_L[x['side']].split(' (')[0]})" if x["side"] else "") if not show_model else mlabel(x["model"]))
    sub = myears(x["model"]) if show_model else x["part"]["unit"]
    need_side = x["part"]["side"] and not x["side"]
    return (f'<article class="pc" data-pid="{e(x["id"])}"><a class="pc-a" href="{r}{x["url"]}">{part_art(x, r)}'
            f'<h3>{e(t)}</h3><p class="pc-sub">{e(sub)}</p></a>'
            f'<div class="pc-f"><div class="pc-p">{price_html(x)}</div>'
            f'<button class="btn add sm" type="button" data-add="{e(x["id"])}"{" data-side=\"1\"" if need_side else ""}>Add</button></div></article>')

def ask_card(m, part, r):
    return (f'<article class="pc ask" id="p-{part["id"]}" data-ask="{m["id"]}|{part["id"]}"><div class="pc-a"><div class="art has-il" data-cat="{part["cat"]}">{il_tag(part["id"], r, part["name"])}<span>Illustration</span></div>'
            f'<h3>{e(part["name"])}</h3><p class="pc-sub">{e(part["unit"])}</p></div>'
            f'<div class="pc-f"><div class="pc-p"><span class="price ask">Ask for price</span></div>'
            f'<a class="btn wa sm" href="{ask_link(m, part)}" rel="noopener">{WA_SVG}Ask on WhatsApp</a></div></article>')

def faq_block(qs):
    h = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in qs)
    sch = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
           "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub("<[^>]+>", "", a))}} for q, a in qs]}
    return h, sch

def finder(r, b=None, m=None):
    sel = (f'''<div class="f-sel" hidden><label><span>1. Car brand</span><select name="b" data-f="b"><option value="">Choose brand</option>{"".join(f'<option value="{bid}"{" selected" if bid == b else ""}>{e(n)}</option>' for bid, n in BRANDS)}</select></label>
<label><span>2. Model</span><select name="m" data-f="m" data-sel="{e(m or "")}"><option value="">Choose model</option></select></label>
<label><span>3. Part</span><select name="p" data-f="p"><option value="">Choose part</option></select></label></div>''')
    return f'''<form class="finder" data-finder action="{r}search/">
{sel}
<p class="f-hint"><span class="pt" aria-hidden="true">&#128071;</span> Type it the way you would say it.</p>
<div class="f-q"><input name="q" type="search" placeholder="e.g. Kia Cerato front brake pads" aria-label="Search parts, for example Kia Cerato front brake pads" autocomplete="off"><button class="btn dark" type="submit">{ICON['search']}<span>Search</span></button></div>
<div class="fguide" data-guide aria-label="Suggestions"></div>
<noscript><p class="small">Search needs JavaScript. Browse by <a href="{r}hyundai/">Hyundai</a>, <a href="{r}kia/">Kia</a> or the <a href="{r}prices/">price list</a>.</p></noscript>
</form>'''

def model_tile(m, r):
    return (f'<a class="mt" href="{r}{m["b"]}/{m["id"]}/"><span class="mt-b">{e(BR[m["b"]])}</span>'
            f'<b>{e(m["name"])} <i>{e(m["code"])}</i></b><span>{e(myears(m))}</span></a>')

def cat_tile(c, r):
    return f'<a class="ct" href="{r}parts/{c["id"]}/">{ICON[c["icon"]]}<b>{e(c["name"])}</b><span>{e(c["line"])}</span></a>'

# ---------------- home ----------------
def build_home():
    r = ""
    faqs = [
        ("Do I need the part number to order?", "No. Pick your car model and the part, or send us your car plate or chassis number on WhatsApp. We check the exact part for your car before you pay."),
        ("Are the prices on this site the final price?", "Where a part has a price on this site, it is the price for the part listed. For every other part, tap Ask for price and we reply on WhatsApp with the price and stock. Either way we confirm stock and the exact fit for your car before you pay."),
        ("Where do I collect my parts?", f"At our shop at {ADDR1}, {ADDR2}. We are open {HOURS_LINE}. Please WhatsApp us first so we can check stock and get your parts ready."),
        ("Which cars do you have parts for?", "Hyundai and Kia only, for models sold in Singapore such as the Avante, Tucson, Kona, Ioniq, Cerato, Sportage, Sorento, Niro and Picanto. Ask us if your model is not listed."),
    ]
    fh, fs = faq_block(faqs)
    hy = "".join(model_tile(m, r) for m in M.values() if m["b"] == "hyundai")
    ki = "".join(model_tile(m, r) for m in M.values() if m["b"] == "kia")
    cats = "".join(cat_tile(c, r) for c in C.values())
    latest = sorted(PRODUCTS, key=lambda x: x["created"] or x["updated"], reverse=True)[:12]
    pop = (f'<section class="sec newrail"{"" if latest else " hidden"}><div class="wrap"><div class="rail-h"><div><h2>Newly added</h2><p>The latest parts in our shop. For anything else, <a href="prices/">ask us for the price</a>.</p></div>'
           f'<div class="rail-nav"><button class="rail-btn" type="button" data-dir="-1" aria-label="Scroll left">&#8592;</button><button class="rail-btn" type="button" data-dir="1" aria-label="Scroll right">&#8594;</button></div></div>'
           f'<div class="rail" data-latest>{"".join(card(x, r) for x in latest)}</div></div></section>')
    pop += (f'<section class="sec" data-noprod{" hidden" if latest else ""}><div class="wrap two"><div><h2>Prices on request</h2>'
               f'<p>We quote every part for your exact car, so you get the right part at the right price. Pick your model, tap the part you need, and ask for the price on WhatsApp. We reply with the price and whether it is in stock.</p>'
               f'<p><a class="btn primary" href="prices/">How prices work</a></p></div>'
               f'<div class="proof"><p><b>Fastest way</b></p><p>Send your car plate or chassis number and the part you need.</p>'
               f'<p><a class="btn wa" href="{wa_link("Hi Autotex, I need a part. My car plate / chassis number is: ")}" rel="noopener">{WA_SVG}WhatsApp {WA_SHOW}</a></p></div></div></section>')
    body = f'''
<section class="hero"><div class="wrap hero-in">
<div class="hero-t reveal"><p class="eyebrow">Kaki Bukit · Registered {REG[-4:]}</p>
<h1>Kia and Hyundai parts, <em>direct from Korea</em></h1>
<p class="lead">Autotex is a Kia and Hyundai parts stockist in Singapore. Pick your car and the part, then see the price or ask us on WhatsApp. No part number needed.</p>
<ul class="ticks"><li>{ICON['check']}Body, lamps, brakes, suspension, engine, aircon</li><li>{ICON['check']}Sold direct to Singapore drivers</li><li>{ICON['check']}We check the fit for your car before you pay</li></ul></div>
<div class="hero-f reveal">{finder(r)}</div>
</div></section>

{pop}

<section class="sec"><div class="wrap">
<div class="sec-h"><h2>Shop by car</h2><p>Choose your model. Every part type we supply for it is on one page.</p></div>
<div class="tabs" role="tablist"><button role="tab" aria-selected="true" data-tab="hy">Hyundai</button><button role="tab" aria-selected="false" data-tab="ki">Kia</button></div>
<div class="mgrid" data-pane="hy">{hy}</div><div class="mgrid" data-pane="ki" hidden>{ki}</div>
<noscript><style>[data-pane]{{display:grid!important}}</style></noscript>
</div></section>

<section class="sec alt"><div class="wrap">
<div class="sec-h"><h2>Shop by part</h2><p>Every part type, across all Hyundai and Kia models.</p></div>
<div class="cgrid">{cats}</div>
</div></section>

<section class="sec dark"><div class="wrap">
<div class="sec-h"><h2>How ordering works</h2></div>
<ol class="steps">
<li class="reveal"><b>1</b><h3>Find your part</h3><p>Choose your brand, model and part, or just type it, like “Tucson tail lamp”.</p></li>
<li class="reveal"><b>2</b><h3>Get the price</h3><p>See the price where it is listed, or tap Ask for price. Pick left or right where needed.</p></li>
<li class="reveal"><b>3</b><h3>Send on WhatsApp</h3><p>Your order or question goes to our WhatsApp. We confirm stock, fit and collection with you.</p></li>
</ol>
<p class="center"><a class="btn primary" href="how-to-order/">How to order</a></p>
</div></section>

<section class="sec"><div class="wrap two">
<div class="reveal"><h2>Why Autotex</h2>
<p>Autotex stocks Kia and Hyundai parts brought in direct from Korea and sells them direct to Singapore drivers at distribution price. Our range covers body parts, lamps, brake pads and discs, suspension and steering, engine mounting, spark plugs, ignition coils, engine service parts, cooling and aircon parts, alternators and starter motors.</p>
<p>{e(LEGAL)} has been registered in Singapore since {REG} (UEN {UEN}). <a href="about/">About us</a></p></div>
<div class="proof reveal"><p class="stars" aria-label="Rated 5.0 out of 5 on Google">★★★★★</p><p><b>5.0 on Google</b> from 4 reviews</p><p><a href="{GMAP}" rel="noopener">See us on Google Maps</a></p>
<p class="addr">{ICON['pin']}<span>{e(ADDR1)}<br>{e(ADDR2)}</span></p>
<p class="small muted">Open {HOURS_LINE}.</p></div>
</div></section>

<section class="sec alt"><div class="wrap narrow">
<h2>Questions</h2>{fh}
</div></section>
<section class="cta"><div class="wrap"><h2>Not sure which part you need?</h2><p>Send us your car plate or chassis number and what is wrong. We will tell you the part and the price.</p>
<a class="btn wa" href="{wa_link("Hi Autotex, I need a part. My car plate / chassis number is: ")}" rel="noopener">{WA_SVG}WhatsApp {WA_SHOW}</a></div></section>
'''
    shell("index.html", "Kia & Hyundai Parts Singapore | Autotex", "Kia and Hyundai parts stockist in Kaki Bukit. Choose your car and part, see the price or ask on WhatsApp. Stock direct from Korea.",
          body, active="", schema=[fs, {"@type": "WebSite", "@id": BASE + "/#web", "url": BASE + "/", "name": "Autotex"}], prio="1.0")

# ---------------- brand x part pages (e.g. /kia/front-brake-pads/) ----------------
def brandpart_data():
    out = {}
    byk = {}
    for x in PRODUCTS: byk.setdefault((x["m"], x["p"]), []).append(x)
    for bid, bn in BRANDS:
        for pt in PARTS:
            pid = pt[0]
            if pid == "other": continue
            ms = [m for m in M.values() if m["b"] == bid and fits(m["fuel"], pt)]
            if len(ms) < 3: continue
            assert pid not in M, pid
            rows = []
            for m in sorted(ms, key=lambda m: (m["name"], m["code"])):
                xs = byk.get((m["id"], pid), [])
                xs = [x for x in xs if x.get("url")]
                rows.append((m, xs[0] if xs else None))
            out[(bid, pid)] = rows
    return out

# A brand x part page is only indexable when it carries real, distinct data (Edwin, 2 Nov 2026 SEO pass):
# at least BP_MIN_MODELS listed models, each with a catalogue price. Otherwise noindex,follow and out of sitemap.xml / llms.txt.
BP_MIN_MODELS = 8
BP_INDEXED, BP_NOINDEX = [], []   # (url, title, summary) / url

def _y0(m):
    mt = re.match(r"(\d{4})", m["years"] or "")
    return int(mt.group(1)) if mt else 0

def _lower(n):
    return n.lower().replace("atf", "ATF").replace("(4 l)", "(4 L)").replace("evap", "EVAP")

def _join(items, last="and"):
    items = list(items)
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + f" {last} " + items[-1]

def _fam(rows):
    """Group (model, product) rows by model family name, oldest generation first."""
    fam = {}
    for m, x in rows: fam.setdefault(m["name"], []).append((m, x))
    return {k: sorted(v, key=lambda t: _y0(t[0])) for k, v in fam.items()}

def _fit_notes(bid, pt, rows):
    """Models of this brand that do NOT get the part, with the real reason (fuel rule in catalog.fits)."""
    have = {m["id"] for m, _ in rows}
    miss = [m for m in M.values() if m["b"] == bid and m["id"] not in have]
    if not miss: return ""
    need = pt[6]
    ev = [mn(m) for m in miss if m["fuel"] == "electric"]
    oth = [mn(m) for m in miss if m["fuel"] != "electric"]
    out = []
    if ev: out.append(f"{_join(ev)} {'is' if len(ev) == 1 else 'are'} electric, so {'it is' if len(ev) == 1 else 'they are'} not listed for this part.")
    if oth:
        why = "have no spark ignition" if need == "petrol" else "do not use it"
        out.append(f"{_join(oth)} {why}, so {'it is' if len(oth) == 1 else 'they are'} left out.")
    return " ".join(out)

def build_brandparts():
    data = brandpart_data()
    for (bid, pid), rows in data.items():
        bn = BR[bid]; part = P[pid]; c = C.get(part["cat"]); r = "../../"; pt = PT[pid]; info = PINFO[pid]
        pl = _lower(part["name"]); unit = part["unit"]
        plural = pl.endswith(("pads", "plugs", "discs", "blades")); need_v = "need" if plural else "needs"
        priced = [(m, x) for m, x in rows if x and show_price(x)]
        prices = [x["price"] for _, x in priced]
        low, high = (min(prices), max(prices)) if prices else (None, None)
        lowt = f", from {money(low)}" if prices else ""
        indexable = len(rows) >= BP_MIN_MODELS and len(priced) >= BP_MIN_MODELS
        url = f"{BASE}/{bid}/{pid}/"
        lis = "".join(
            f'<li><a href="{r}{x["url"]}"><b>{e(mpar(m))}</b> <span>{e(myears(m))}</span></a><em>{money(x["price"]) if show_price(x) else "Ask for price"}</em></li>'
            if x else f'<li><a href="{r}{m["b"]}/{m["id"]}/"><b>{e(mpar(m))}</b> <span>{e(myears(m))}</span></a><em>Ask for price</em></li>'
            for m, x in rows)
        sib = "".join(f'<a class="chip" href="{r}{b2}/{pid}/">{e(BR[b2])} {e(part["name"].lower())}</a>' for b2, _ in BRANDS if b2 != bid and (b2, pid) in data)
        rel = "".join(f'<a class="chip" href="{r}{bid}/{p2}/">{e(P[p2]["name"])}</a>' for (b2, p2) in data if b2 == bid and p2 != pid and P[p2]["cat"] == part["cat"])

        # ---- data-driven facts that differ on every page ----
        y0 = min(_y0(m) for m, _ in rows)
        newest = max((m for m, _ in rows), key=lambda m: (_y0(m), m["name"]))
        fam = _fam(rows)
        multi = {k: v for k, v in fam.items() if len(v) > 1}
        gen_bits = [f"{k} ({', '.join(m['code'] + ' ' + myears(m) for m, _ in v)})" for k, v in multi.items()]
        fuels = [t for t in ("petrol", "diesel", "hybrid", "electric") if any(t in m["fuel"] for m, _ in rows)]
        cheapest = min(priced, key=lambda t: (t[1]["price"], t[0]["name"])) if priced else None
        dearest = max(priced, key=lambda t: (t[1]["price"], t[0]["name"])) if priced else None
        n_prices = len(set(prices))
        if prices and low == high:
            price_txt = f"Every listed {bn} model is priced the same, {money(low)} per {unit}."
        elif prices:
            price_txt = (f"Prices run from {money(low)} ({mpar(cheapest[0])}) to {money(high)} ({mpar(dearest[0])}) per {unit}, "
                         f"with {n_prices} different price points across the {len(priced)} priced models. Check the row for your model.")
        else:
            price_txt = "No price is published yet for these models. Ask on WhatsApp for the price and stock."
        # direct answer, 40-60 words
        lead = (f"Autotex lists {pl} for {len(rows)} {bn} models sold in Singapore, from cars of {y0} to the newest, the {mn(newest)} ({myears(newest)}), "
                + (f"priced {money(low)} to {money(high)} per {unit}. " if prices and low != high else (f"at {money(low)} per {unit}. " if prices else f"sold per {unit}. "))
                + "Send your car plate or chassis number and we confirm the fit before you pay.")
        # spec table for the three parts where the catalogue holds per-model specs
        spec_html = ""
        if pid in ("engine-oil", "transmission-oil", "spark-plugs"):
            if pid == "engine-oil": head, f = ("Oil grade", "Engine oil needed"), lambda s: (s["grade"], f"{s['oil_l']:g} L")
            elif pid == "transmission-oil": head, f = ("Gearbox", "Fluid needed"), lambda s: (f"{s['gbtext']}, {GB_LABEL[s['gb']]}", f"{s['fluid_l']:g} L")
            else: head, f = ("Cylinders", "Plugs needed"), lambda s: (str(s["cyl"]), str(s["cyl"]))
            trs = ""
            for m, _ in rows:
                s = spec(m["id"])
                if s:
                    a, b = f(s); trs += f"<tr><td>{e(mpar(m))} <small>{e(myears(m))}</small></td><td>{e(a)}</td><td>{e(b)}</td></tr>"
            if trs:
                spec_html = (f'<h2>{e(bn)} {e(pl)} specs by model</h2><p>Indicative figures per model. We confirm the exact grade and amount against your chassis number before you pay.{" The listed price is per set of 4, so ask us about 3 and 6 cylinder engines." if pid == "spark-plugs" else ""}</p>'
                             f'<div class="tbl"><table><thead><tr><th>Model</th><th>{head[0]}</th><th>{head[1]}</th></tr></thead><tbody>{trs}</tbody></table></div>')
        signs = info["signs"]
        gen_p = (f" Several families have more than one generation on this list: {_join(gen_bits)}. The part for one generation does not fit the other." if gen_bits else
                 " Each family appears once, so the model name and years on your log card are enough to pick the right row.")
        side_p = " Because it is a left and right part, say which side you need." if part["side"] else ""
        fuel_p = f" Fuel types on this list: {_join(fuels)}." if len(fuels) > 1 else f" All listed models are {fuels[0]}."
        fit_notes = _fit_notes(bid, pt, rows)

        faqs = [
            (f"Which {bn} models {'do' if plural else 'does'} the {pl} fit?",
             f"Autotex lists it for {len(rows)} {bn} models: " + "; ".join(f"{mpar(m)} {myears(m)}" for m, _ in rows) + ". " + (fit_notes + " " if fit_notes else "") + "We confirm the fit against your chassis number before you pay."),
            (f"How much {'are' if plural else 'is a'} {bn} {pl} in Singapore?", price_txt + f" Sold per {unit}. Collect from our shop, or delivery is S$10 and free above S$80."),
            (f"How do I know when the {bn} {pl} {need_v} replacing?",
             f"Common signs: {_join(signs)}. A workshop can confirm. To order, send {info['send']}, plus your car plate or chassis number."),
        ]
        fh, fs = faq_block(faqs)
        oem_rows = [(m, x) for m, x in rows if x and x.get("oem")]
        oem_p = (f"We have OEM part numbers recorded for {len(oem_rows)} of these models: " + "; ".join(f"{mpar(m)} {x['oem']}" for m, x in oem_rows) + "." if oem_rows else
                 "OEM means made to the carmaker's own specification. Aftermarket means made by another maker to fit the same car, usually at a different price. Our catalogue does not label each listing as one or the other, so ask on WhatsApp and we tell you what we quote for your car before you pay.")
        fam_names = _join(list(fam.keys()))
        body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}
<h1>{e(bn)} {e(pl)} in Singapore</h1>
<p class="lead">{e(lead)}</p></div></section>
<section class="sec"><div class="wrap"><h2>{e(bn)} models with {e(pl)}</h2><ul class="bplist">{lis}</ul>
<p class="small">Your model is not listed? <a href="{wa_link(f"Hi Autotex, do you have {part['name'].lower()} for my {bn}? Model and year: ")}" rel="noopener">Ask us on WhatsApp</a>.</p></div></section>
<section class="sec alt"><div class="wrap narrow">
<h2>Fitment by {e(bn)} model and year</h2>
<p>The list covers {e(fam_names)}, with the oldest car from {y0} and the newest the {e(mn(newest))} ({e(myears(newest))}).{e(gen_p)}{e(fuel_p)} {e(fit_notes)}</p>
<h2>What decides the right {e(pl)}</h2>
<p>The {e(pl)} {e(info["what"])}. Which one fits depends on {e(info["fit"])}.{e(side_p)}</p>
{spec_html}
<h2>Price by model</h2><p>{e(price_txt)}</p>
<h2>Signs the {e(bn)} {e(pl)} {need_v} replacing</h2>
<ul>{"".join(f"<li>{e(s[0].upper() + s[1:])}.</li>" for s in signs)}</ul>
<p>These signs are general to this type of part. A workshop can confirm the cause before you order.</p>
<h2>OEM or aftermarket {e(pl)}</h2><p>{e(oem_p)}</p>
<h2>What to send us</h2>
<p>Send {e(info["send"])} on <a href="{wa_link(f"Hi Autotex, I need {part['name'].lower()} for my {bn}. Car plate / chassis number: ")}" rel="noopener">WhatsApp {e(WA_SHOW)}</a>. Your chassis number is printed on the vehicle log card. We match the part to it and reply with the price and stock.</p>
<p class="small">Collect from {e(ADDR1)}, {e(ADDR2)}, or ask for delivery within 1 day at S$10, free above S$80. Returns within 7 days in the original packaging.</p>
<h2>Questions about {e(bn)} {e(pl)}</h2>{fh}
</div></section>
{f'<section class="sec"><div class="wrap"><h2>More {e(bn)} {e(c["name"].lower())}</h2><div class="chips">{rel}</div></div></section>' if rel else ""}
{f'<section class="sec alt"><div class="wrap"><h2>{e(part["name"])} for other brands</h2><div class="chips">{sib}</div><p class="small"><a href="{r}parts/{part["cat"]}/">All {e(c["name"].lower())}</a></p></div></section>' if (sib and c) else ""}'''
        title = f"{bn} {part['name']} Singapore | Autotex"
        if len(title) > 60: title = f"{bn} {part['name']} Singapore"[:60]
        fl = list(fam.keys())
        desc = f"{bn} {pl} for {len(rows)} models ({_join(fl[:3])}{' and more' if len(fl) > 3 else ''}){lowt}. Fit checked by chassis number. Autotex, Kaki Bukit."
        if len(desc) > 160: desc = f"{bn} {pl} for {len(rows)} {bn} models{lowt}. Fit checked by chassis number. Autotex, Kaki Bukit."
        if len(desc) < 120: desc += " Ask on WhatsApp."
        items = [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Product", "name": x["title"], "url": f"{BASE}/{x['url']}",
                  "offers": {"@type": "Offer", "price": str(x["price"]), "priceCurrency": "SGD", "url": f"{BASE}/{x['url']}"}}}
                 for i, (m, x) in enumerate(priced)]
        sch = [fs] + ([{"@type": "ItemList", "name": f"{bn} {part['name']} by model", "numberOfItems": len(items), "itemListElement": items}] if items and indexable else [])
        shell(f"{bid}/{pid}/index.html", title, desc, body, active=bid, crumbs=[(f"{bn} parts", f"{bid}/"), (f"{part['name']}", f"{bid}/{pid}/")],
              schema=sch, prio="0.8", index=indexable, noindex=not indexable)
        if indexable:
            BP_INDEXED.append((url, f"{bn} {part['name']}", f"{len(rows)} models, {y0} to {myears(newest)}" + (f", {money(low)} to {money(high)}" if prices and low != high else (f", {money(low)}" if prices else ""))))
        else:
            BP_NOINDEX.append(url)


# ---------------- brand pages ----------------
def build_brands():
    for bid, bn in BRANDS:
        path = f"{bid}/index.html"; r = "../"
        ms = [m for m in M.values() if m["b"] == bid]
        tiles = "".join(model_tile(m, r) for m in ms)
        catlinks = "".join(f'<a class="chip" href="{r}parts/{c["id"]}/#{bid}">{e(bn)} {e(c["name"].lower() if c["id"] != "brake-discs" else "brake discs")}</a>' for c in C.values())
        fams = list(dict.fromkeys(m["name"] for m in ms))
        names = ", ".join(fams)[:90]
        bpd = brandpart_data()
        bplinks = "".join(f'<a class="chip" href="{r}{bid}/{pid}/">{e(P[pid]["name"])}</a>' for (b2, pid) in bpd if b2 == bid)
        n_bp = sum(1 for (b2, _) in bpd if b2 == bid)
        n_ev = sum(1 for m in ms if m["fuel"] == "electric")
        intro = (f"Autotex supplies {bn} parts for {len(ms)} {bn} models sold in Singapore, covering {len(fams)} model families from {_join(fams[:4])} to {fams[-1]}. "
                 f"Each model page lists every part type we supply for that car, from bumpers, headlamps and tail lamps to brake pads and discs, suspension, engine mounting, spark plugs, ignition coils, cooling and aircon parts. "
                 f"There are also {n_bp} pages that compare one part type across all {bn} models, with the fitment, years and price for each model. "
                 f"{'Electric models have no engine, so engine parts are left off their pages. ' if n_ev else ''}"
                 f"Generations matter: the same model name often has two or three body styles with different parts, so every page shows the generation code and years. "
                 f"If you are unsure, send your car plate or chassis number on WhatsApp and we check the fit before you pay.")
        faqs = [
            (f"Which {bn} models does Autotex supply parts for?", f"{len(ms)} models: " + "; ".join(f"{mpar(m)} {myears(m)}" for m in ms) + ". Ask on WhatsApp if your model is not listed."),
            (f"How do I find the right part for my {bn}?", "Choose your model on this page, then the part type, or type your car and the part into the search box. If you are not sure of the generation, send your car plate or chassis number, printed on the vehicle log card, and we match the part."),
            (f"Do you have {bn} parts for every model and year?", "Only for the models listed above. Each model page lists the part types we supply for that car, with the price where one is set or an Ask for price button. We confirm stock and fit before you pay."),
        ]
        fh, fs = faq_block(faqs)
        body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}
<h1>{e(bn)} parts in Singapore</h1>
<p class="lead">{e(intro)}</p>
<div class="hero-f slim">{finder(r, b=bid)}</div></div></section>
<section class="sec"><div class="wrap"><h2>{e(bn)} models</h2><div class="mgrid">{tiles}</div></div></section>
<section class="sec alt"><div class="wrap"><h2>{e(bn)} parts by type</h2><div class="chips">{catlinks}</div>
<h3 class="bph">All {e(bn)} part types</h3><div class="chips">{bplinks}</div>
<p class="small">Your model is not here? <a href="{wa_link(f"Hi Autotex, do you have parts for my {bn}? Model and year: ")}" rel="noopener">Ask us on WhatsApp</a>.</p></div></section>
<section class="sec"><div class="wrap narrow"><h2>Questions about {e(bn)} parts</h2>{fh}</div></section>'''
        d = f"{bn} spare parts in Singapore for {len(ms)} models incl. {', '.join(fams[:3])}. See the price or ask on WhatsApp. Autotex, Kaki Bukit."
        shell(path, f"{bn} Parts Singapore: Order by Model | Autotex", d,
              body, active=bid, crumbs=[(f"{bn} parts", f"{bid}/")], schema=[fs], prio="0.9")

# ---------------- service kits and repair sets ----------------
def spec_note(m, pid):
    sp = spec(m["id"])
    if not sp: return ""
    if pid == "engine-oil": return f'{sp["grade"]} for this engine, {sp["oil_l"]:g} L fill (sold per 4 L bottle)'
    if pid == "transmission-oil": return f'{GB_LABEL[sp["gb"]]} for the {sp["gbtext"]}, about {sp["fluid_l"]:g} L fill (sold per 4 L)'
    if pid == "spark-plugs": return f'{sp["cyl"]} plugs for this engine'
    return ""

def car_sets(m):
    """Sets that apply to this car, with its listed parts and prices. Items that do not fit the car are left out."""
    out = []
    mine = {}
    for x in PRODUCTS:
        if x["m"] == m["id"] and x["p"] != "other": mine.setdefault(x["p"], x)
    for bid, name, line, inc, opt in BUNDLES:
        def rows(lst):
            rs = []
            for pid, q in lst:
                pt = P.get(pid)
                if not pt or not fits(m["fuel"], next(pp for pp in PARTS if pp[0] == pid)): continue
                sp = spec(m["id"]); x = mine.get(pid); it = dict(part=pt, qty=q, x=x, unit=None, ql=str(q))
                if sp and pid == "engine-oil": it.update(qty=sp["oil_l"], unit="/L", ql=f'{sp["oil_l"]:g} L')
                elif sp and pid == "transmission-oil": it.update(qty=sp["fluid_l"], unit="/L", ql=f'{sp["fluid_l"]:g} L')
                elif sp and pid == "spark-plugs": it.update(qty=sp["cyl"], unit="/plug", ql=f'{sp["cyl"]} plugs')
                elif sp and pid == "ignition-coil": it.update(qty=sp["cyl"], ql=str(sp["cyl"]))
                if it["unit"] and x and show_price(x): it["each"] = x["price"] / 4   # oils are priced per 4 L pack
                elif x and show_price(x): it["each"] = x["price"]
                rs.append(it)
            return rs
        items, adds = rows(inc), rows(opt)
        if len(items) < 2: continue   # e.g. service kits on an electric car
        priced = all(it["x"] and show_price(it["x"]) for it in items)
        total = round(sum(it["each"] * it["qty"] for it in items)) if priced else None
        price = int(round(total * (1 - SET_DISCOUNT))) if priced else None
        out.append(dict(id=bid, name=name, line=line, items=items, adds=adds, total=total, price=price,
                        url=f"{m['b']}/{m['id']}/sets/{bid}/"))
    return out

def set_card(st, r):
    pr = (f'<span class="price">{money(st["price"])}</span><small class="save">Save {money(st["total"] - st["price"])}</small>'
          if st["price"] is not None else '<span class="price ask">Ask for set price</span>')
    return (f'<article class="pc set"><a class="pc-a" href="{r}{st["url"]}"><div class="art has-il set-art">'
            + "".join(il_tag(it["part"]["id"], r, it["part"]["name"]) for it in st["items"][:4]) +
            f'<span>Set of {len(st["items"])}</span></div><h3>{e(st["name"])}</h3><p class="pc-sub">{e(st["line"])}</p></a>'
            f'<div class="pc-f"><div class="pc-p">{pr}</div><a class="btn sm" href="{r}{st["url"]}">View set</a></div></article>')

def build_sets():
    for m in M.values():
        bn = BR[m["b"]]
        for st in car_sets(m):
            path = st["url"] + "index.html"; r = "../../../../"
            def li(it):
                x, pt = it["x"], it["part"]
                link = f'<a href="{r}{x["url"]}">{e(pt["name"])}</a>' if x else e(pt["name"])
                ok = x and show_price(x)
                each = (money(round(it["each"], 2)) + (it["unit"] or "")) if ok else "Ask"
                sub = money(round(it["each"] * it["qty"])) if ok else "Ask"
                return f'<tr><td>{link}<small>{e(spec_note(m, pt["id"]) or pt["unit"])}</small></td><td class="r">{it["ql"]}</td><td class="r">{each}</td><td class="r">{sub}</td></tr>'
            lines = "".join(li(it) for it in st["items"])
            adds = "".join(li(it) for it in st["adds"])
            names = ", ".join(f'{it["ql"]} {it["part"]["name"]}' if it["ql"] != "1" else it["part"]["name"] for it in st["items"])
            msg = (f"Hi Autotex, I'd like the {st['name']} for my {mlabel(m)} {m['years']}"
                   + (f" (set price {money(st['price'])})" if st["price"] is not None else "") + f": {names}."
                   + (" Add-ons I want (optional): " if st["adds"] else "") + " My car plate / chassis number is: ")
            if st["price"] is not None:
                buy = (f'<div class="buy-p"><span class="price big">{money(st["price"])}</span><span class="unit">set price</span></div>'
                       f'<p class="save-l">Bought one by one: {money(st["total"])}. You save {money(st["total"] - st["price"])} ({int(SET_DISCOUNT * 100)}% off).</p>')
            else:
                buy = '<div class="buy-p"><span class="price ask big">Ask for set price</span></div>'
            body = f'''<div class="wrap">{{{{CRUMBS}}}}</div>
<section class="prod wrap">
<div class="prod-art"><div class="art big has-il set-art">{"".join(il_tag(it["part"]["id"], r, it["part"]["name"]) for it in st["items"][:4])}<span>Illustration</span></div></div>
<div class="prod-i">
<p class="eyebrow"><a href="{r}{m["b"]}/{m["id"]}/">{e(bn)} {e(mn(m))}</a></p>
<h1>{e(st["name"])} for {e(bn)} {e(mpar(m))}</h1>
<p class="fits">Fits {e(bn)} {e(mn(m))}, {e(myears(m))}. {e(st["line"])}.</p>
<div class="buy">{buy}
<a class="btn wa big" href="{wa_link(msg)}" rel="noopener">{WA_SVG}Order this set on WhatsApp</a></div>
<p class="fitnote">{ICON['check']}<span>We check every part against your car plate or chassis number before you pay.{" Oil grade, litres and gearbox fluid are the standard fills for your model; we confirm them with your chassis number." if any(it["part"]["id"] in ("engine-oil", "transmission-oil") for it in st["items"]) else ""}</span></p>
</div></section>
<section class="sec"><div class="wrap"><h2>What is in the set</h2>
<div class="tbl"><table><thead><tr><th>Part</th><th class="r">Qty</th><th class="r">Each</th><th class="r">Subtotal</th></tr></thead><tbody>{lines}</tbody></table></div>
{f'<h2>Optional add-ons</h2><p>Not included in the set price. Tell us on WhatsApp if you want them{"; rear top mounts are only used on some models, so we confirm with your chassis number" if any(it["part"]["id"] == "rear-top-mount" for it in st["adds"]) else ""}.</p><div class="tbl"><table><thead><tr><th>Part</th><th class="r">Qty</th><th class="r">Each</th><th class="r">Subtotal</th></tr></thead><tbody>{adds}</tbody></table></div>' if adds else ""}
<p><a class="btn ghost" href="{r}{m["b"]}/{m["id"]}/">All parts for the {e(bn)} {e(mn(m))}</a></p></div></section>'''
            prod = {"@type": "Product", "@id": BASE + "/" + st["url"] + "#product", "name": f"{st['name']} for {bn} {mpar(m)}",
                    "sku": f"{m['b']}-{m['id']}-{st['id']}", "category": "Service kits and repair sets", "image": [BASE + "/assets/parts/" + it["part"]["id"] + ".jpg" for it in st["items"][:4]],
                    "brand": {"@type": "Brand", "name": bn}, "description": f"{st['line']}. Set for the {bn} {mn(m)} ({myears(m)}), sold by Autotex in Singapore.",
                    "isRelatedTo": {"@type": "Car", "name": f"{bn} {mn(m)}", "brand": {"@type": "Brand", "name": bn}}}
            if st["price"] is not None:
                prod["offers"] = {"@type": "Offer", "url": BASE + "/" + st["url"], "priceCurrency": "SGD", "price": f'{st["price"]:.2f}',
                                  "availability": AVAIL["in"], "seller": {"@id": BASE + "/#store"}, "areaServed": "SG",
                                  "hasMerchantReturnPolicy": RETURN_POLICY, "shippingDetails": SHIPPING}
            tp = f" {money(st['price'])}" if st["price"] is not None else ""
            title = f"{st['name']} {bn} {mn(m)}{tp} | Autotex"
            if len(title) > 60: title = f"{st['name']} {bn} {mn(m)}{tp}"
            shell(path, title, f"{st['name']} for the {bn} {mn(m)}: {st['line'].lower()}." + (f" Set price {money(st['price'])}, save {money(st['total'] - st['price'])}." if st["price"] is not None else "") + " Order on WhatsApp.",
                  body, active=m["b"], crumbs=[(f"{bn} parts", f"{m['b']}/"), (mpar(m), f"{m['b']}/{m['id']}/"), (st["name"], st["url"])],
                  schema=[prod], index=False, noindex=True, prio="0.7")

# ---------------- model pages ----------------
def build_models():
    for m in M.values():
        bn = BR[m["b"]]
        path = f"{m['b']}/{m['id']}/index.html"; r = "../../"
        items = [x for x in PRODUCTS if x["m"] == m["id"]]
        secs, jump = [], []
        fit = car_parts(m)
        for c in C.values():
            cards = []
            for pt in [p for p in fit if p["cat"] == c["id"]]:
                xs = [x for x in items if x["p"] == pt["id"]]
                cards.extend(card(x, r, show_model=False) for x in xs) if xs else cards.append(ask_card(m, pt, r))
            cards.extend(card(x, r, show_model=False) for x in items if x["p"] == "other" and x["cat"]["id"] == c["id"])
            if not cards: continue
            jump.append(f'<a class="chip" href="#{c["id"]}">{e(c["name"])}</a>')
            secs.append(f'<section class="msec" id="{c["id"]}"><h2>{ICON[c["icon"]]}{e(c["name"])}</h2><div class="pgrid">{"".join(cards)}</div>'
                        f'<p class="small"><a href="{r}parts/{c["id"]}/">{e(c["name"])} for other Hyundai and Kia models</a></p></section>')
        sts = car_sets(m)
        if sts:
            jump.insert(0, '<a class="chip" href="#sets">Service kits &amp; sets</a>')
            secs.insert(0, f'<section class="msec" id="sets"><h2>{ICON["engine"]}Service kits &amp; sets</h2><p class="small">Everything for the job in one order, {int(SET_DISCOUNT * 100)}% below the single-part prices.</p><div class="pgrid">{"".join(set_card(st, r) for st in sts)}</div></section>')
        misc = [x for x in items if x["p"] == "other" and not x["cat"]["id"]]
        if misc:
            jump.append('<a class="chip" href="#more">More parts</a>')
            secs.append(f'<section class="msec" id="more"><h2>More parts</h2><div class="pgrid">{"".join(card(x, r, show_model=False) for x in misc)}</div></section>')
        first = m["name"].split()[0]
        sibs = "".join(model_tile(o, r) for o in M.values() if o["b"] == m["b"] and o["id"] != m["id"] and o["name"].split()[0] == first)
        others = "".join(f'<a class="chip" href="{r}{o["b"]}/{o["id"]}/">{e(mn(o))}</a>' for o in M.values() if o["b"] == m["b"] and o["id"] != m["id"])
        al = [a for a in m["alias"][:2] if a.split()[0] != m["name"].lower().split()[0]]
        alias = f" Also called the {', '.join(a.title() for a in al)}." if al else ""
        ev = " As an electric car it has no engine parts, so this page lists body, lamp, brake and suspension parts." if m["fuel"] == "electric" else ""
        names = [p["name"].lower() for p in fit if p["id"] in ("front-brake-pads", "oil-filter", "headlamp", "front-bumper", "spark-plugs", "front-shock-absorber") ][:5]
        fitline = (f" Common parts for this car include {', '.join(names[:-1]) + ' and ' + names[-1] if len(names) > 1 else (names[0] if names else 'body and service parts')}."
                   f" Each part is checked against the {e(m['name'])} {e(m['code'] or '')} before you pay.") if fit else ""
        body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}
<h1>{e(bn)} {e(mpar(m))} parts</h1>
<p class="lead">Parts for the {e(bn)} {e(m["name"])}, {e(m["code"]) + " generation, " if m["code"] else ""}{e(myears(m))} ({e(m["fuel"])}).{e(alias)}{ev} Where a price is listed you can add the part to your cart. For the others, tap Ask on WhatsApp and we reply with the price and stock.{fitline}</p>
<p class="fitnote">{ICON['check']}<span>Not sure if your car is the {e(m["code"] or m["name"])}? Send us your car plate or chassis number and we will check before you pay.</span></p>
<div class="chips jump">{"".join(jump)}</div></div></section>
<div class="wrap msecs">{"".join(secs)}</div>
{f'<section class="sec alt"><div class="wrap"><h2>Other {e(first)} generations</h2><div class="mgrid">{sibs}</div></div></section>' if sibs else ""}
<section class="sec"><div class="wrap"><h2>Other {e(bn)} models</h2><div class="chips">{others}</div></div></section>'''
        sch = []
        if items:
            sch.append({"@type": "ItemList", "name": f"{bn} {mpar(m)} parts", "numberOfItems": len(items),
                        "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + "/" + x["url"], "name": x["title"]} for i, x in enumerate(items)]})
        shell(path, f"{bn} {mn(m)} Parts Singapore | Autotex"[:70], f"{bn} {m['name']} {mcy(m, m['years'].replace('-now', '+'))} parts in Singapore: bumpers, lamps, brake pads, discs, suspension and more. See the price or ask on WhatsApp.",
              body, active=m["b"], crumbs=[(f"{bn} parts", f"{m['b']}/"), (f"{mpar(m)}", f"{m['b']}/{m['id']}/")], schema=sch, prio="0.8")

# ---------------- product pages ----------------
def build_products():
    for x in PRODUCTS:
        m, p, c = x["model"], x["part"], x["cat"]; bn = BR[m["b"]]
        r = "../../../"; path = x["url"] + "index.html"
        same_car = [y for y in PRODUCTS if y["m"] == m["id"] and y["id"] != x["id"]]
        same_cat = [y for y in same_car if y["cat"]["id"] == c["id"]]
        rest = [y for y in same_car if y["cat"]["id"] != c["id"]]
        related = (same_cat + rest)[:8]
        other_models = [y for y in PRODUCTS if p["id"] != "other" and y["p"] == p["id"] and y["m"] != m["id"]]
        om = "".join(f'<a class="chip" href="{r}{y["url"]}">{e(BR[y["model"]["b"]])} {e(mn(y["model"]))}</a>' for y in other_models)
        stock = STOCK.get(x["stock"])
        stock_h = f'<span class="stock {stock[1]}" data-stock="{e(x["id"])}">{stock[0]}</span>' if stock else f'<span class="stock" data-stock="{e(x["id"])}">Stock checked on WhatsApp</span>'
        oem = f'<div><dt>Part number</dt><dd class="mono">{e(x["oem"])}</dd></div>' if x["oem"] else '<div><dt>Part number</dt><dd>We match it to your car plate or chassis number</dd></div>'
        if x["side"]:
            side = f'<p class="sidefix"><b>Side:</b> {e(SIDE_L[x["side"]])}</p>'
        elif p["side"]:
            side = ('<fieldset class="side"><legend>Side</legend><label><input type="radio" name="side" value="Left" required> Left (passenger)</label>'
                    '<label><input type="radio" name="side" value="Right"> Right (driver)</label></fieldset>')
        else:
            side = ""
        msg = f"Hi Autotex, I'm asking about: {x['title']} {m['years']}. My car plate / chassis number is: "
        note = (f'<p class="note">{e(x["note"])}</p>' if x["note"] else "") + (f'<p class="note"><b>For this model:</b> {e(spec_note(m, x["p"]))}. We confirm with your chassis number.</p>' if spec_note(m, x["p"]) else "")
        desc_t = f"{p['name']} for the {bn} {m['name']} {mcy(m, myears(m))}"
        ph = x["photos"]
        thumbs = ""
        if len(ph) > 1:
            thumbs = "".join(f'<button type="button" data-full="{e(s if s.startswith("http") else r + s)}" aria-label="Photo {i + 1}"><img src="{e(s if s.startswith("http") else r + s)}" alt="" width="64" height="64" loading="lazy"></button>' for i, (s, _) in enumerate(ph))
        askbtn = (f'<a class="btn wa{"" if not show_price(x) else " ghost"}" href="{wa_link(msg)}" rel="noopener">{WA_SVG}{"Ask about this part" if show_price(x) else "Ask for price on WhatsApp"}</a>')
        c_link = f'<a href="{r}parts/{c["id"]}/">{e(c["name"])}</a> · ' if c["id"] else ""
        rel_h = (f'<section class="sec"><div class="wrap"><h2>More parts for your {e(mn(m))}</h2><div class="pgrid">{"".join(card(y, r, show_model=False) for y in related)}</div>'
                 f'<p><a class="btn ghost" href="{r}{m["b"]}/{m["id"]}/">All {e(bn)} {e(mn(m))} parts</a></p></div></section>') if related else \
                (f'<section class="sec"><div class="wrap"><p><a class="btn ghost" href="{r}{m["b"]}/{m["id"]}/">All parts for the {e(bn)} {e(mn(m))}</a></p></div></section>')
        om_h = (f'<section class="sec alt"><div class="wrap"><h2>{e(p["name"])} for other models</h2><div class="chips">{om}</div>'
                + (f'<p class="small"><a href="{r}parts/{c["id"]}/">All {e(c["name"].lower())}</a></p>' if c["id"] else "") + '</div></section>') if om else ""
        body = f'''<div class="wrap">{{{{CRUMBS}}}}</div>
<section class="prod wrap" data-product="{e(x["id"])}">
<div class="prod-art">{part_art(x, r, "art big")}<div class="thumbs">{thumbs}</div></div>
<div class="prod-i">
<p class="eyebrow">{c_link}<a href="{r}{m["b"]}/{m["id"]}/">{e(bn)} {e(mn(m))}</a></p>
<h1>{e(p["name"])}{f' ({e(SIDE_L[x["side"]].split(" (")[0])})' if x["side"] else ""} for {e(bn)} {e(mpar(m))}</h1>
<p class="fits">Fits {e(bn)} {e(mn(m))}, {e(myears(m))}</p>
<p class="gone" hidden>This part is no longer listed. <a href="{wa_link(msg)}" rel="noopener">Ask us on WhatsApp</a> if you still need it.</p>
<div class="buy">
<div class="buy-p">{price_html(x, big=True)}<span class="unit">per {e(p["unit"])}</span></div>
{stock_h}
<form class="buy-f" data-buy="{e(x["id"])}">{side}
<div class="qty"><label for="q-{e(x["id"])}">Qty</label><button type="button" data-q="-1" aria-label="Less">−</button><input id="q-{e(x["id"])}" name="qty" type="number" min="1" max="20" value="1" inputmode="numeric"><button type="button" data-q="1" aria-label="More">+</button></div>
<button class="btn primary big" type="submit">{ICON['cart']}Add to cart</button>
</form>
{askbtn}
</div>
{note}
<dl class="spec">
<div><dt>Car</dt><dd>{e(bn)} {e(m["name"])}</dd></div>
<div><dt>Generation</dt><dd>{e(m["code"] + ", " if m["code"] else "")}{e(myears(m))}</dd></div>
<div><dt>Engine type</dt><dd>{e(m["fuel"])}</dd></div>
<div><dt>Sold as</dt><dd>{e(p["unit"])}{" (left or right)" if p["side"] and not x["side"] else ""}</dd></div>
{oem}
<div><dt>Collect at</dt><dd>Kaki Bukit (AutoBay)</dd></div>
</dl>
<p class="fitnote">{ICON['check']}<span>We check that this part fits your exact car before you pay. Facelift and engine versions can differ, so send us your car plate or chassis number with the order.</span></p>
</div></section>
{rel_h}
{om_h}'''
        prod = {"@type": "Product", "@id": BASE + "/" + x["url"] + "#product", "name": f"{x['title'].split(' for ')[0]} for {bn} {mpar(m)}",
                "sku": x["id"], "category": c["name"], "image": [u for _, u in ph] or [BASE + "/assets/parts/" + p["id"] + ".jpg"],
                "brand": {"@type": "Brand", "name": bn},
                "description": desc_t + (f". {x['note']}" if x["note"] else "") + ". Sold by Autotex, Kia and Hyundai parts stockist in Singapore.",
                "isRelatedTo": {"@type": "Car", "name": f"{bn} {mn(m)}", "brand": {"@type": "Brand", "name": bn}}}
        if x["oem"]: prod["mpn"] = x["oem"]
        if show_price(x):
            FEED.append({"id": x["id"], "title": prod["name"][:150], "description": prod["description"][:5000],
                         "link": BASE + "/" + x["url"], "image_link": prod["image"][0],
                         "availability": {"in": "in_stock", "order": "backorder", "out": "out_of_stock"}.get(x["stock"] or "in", "in_stock"),
                         "price": f'{x["price"]:.2f} SGD', "condition": "new", "brand": bn, "mpn": x["oem"] or "",
                         "identifier_exists": "yes" if x["oem"] else "no", "google_product_category": "5613",
                         "product_type": f"{bn} > {mn(m)} > {c['name']}", "shipping": "SG:::10.00 SGD"})
        if show_price(x):
            off = {"@type": "Offer", "url": BASE + "/" + x["url"], "priceCurrency": "SGD", "price": f'{x["price"]:.2f}',
                   "seller": {"@id": BASE + "/#store"}, "areaServed": "SG"}
            off["availability"] = AVAIL.get(x["stock"] or "in", AVAIL["in"])  # Edwin 31 Oct: parts are in stock
            off["hasMerchantReturnPolicy"] = RETURN_POLICY; off["shippingDetails"] = SHIPPING
            prod["offers"] = off
        tprice = f" {money(x['price'])}" if show_price(x) else ""
        title = f"{p['name']} {bn} {mn(m)}{tprice} | Autotex"
        if len(title) > 60: title = f"{p['name']} {bn} {mn(m)}{tprice}"
        shell(path, title, f"{desc_t}.{(' ' + money(x['price']) + ' per ' + p['unit'] + '.') if show_price(x) else ' Ask for the price on WhatsApp.'} Kia and Hyundai parts stockist in Kaki Bukit.",
              body, active=m["b"], crumbs=[(f"{bn} parts", f"{m['b']}/"), (f"{mpar(m)}", f"{m['b']}/{m['id']}/"), (p["name"], x["url"])],
              schema=[prod], index=False, noindex=True, prio="0.7", og_type="product", og_image=ph[0][1] if ph else None, og_alt=x["title"])

# ---------------- category pages ----------------
def build_cats():
    tiles = "".join(cat_tile(c, "../") for c in C.values())
    cnames = [c["name"].lower() for c in C.values()]
    intro = (f"Autotex supplies {len(PARTS)} types of Hyundai and Kia part for {len(M)} models sold in Singapore, grouped into {len(C)} categories: {_join(cnames)}. "
             f"Open a category to see every part in it for every Hyundai and Kia model, with the model, years and price side by side. Where a price is listed you can add the part to your cart. "
             f"For anything else, tap Ask and we reply on WhatsApp with the price and stock. Sold as a piece, a pair or a set depending on the part, and the unit is shown on each page. "
             f"Engine parts are left off electric models, which have no engine. If you do not know the generation of your car, send your car plate or chassis number and we check the fit before you pay.")
    faqs = [("What kinds of Hyundai and Kia parts does Autotex supply?", f"{len(PARTS)} part types in {len(C)} categories: {_join(cnames)}. All are for Hyundai and Kia models sold in Singapore."),
            ("How do I know which part fits my car?", "Pick your model and generation, shown with its years on every page. If you are not sure, send your car plate or chassis number, printed on the vehicle log card, and we match the part before you pay."),
            ("Can I pay on the website?", "No. Your cart is sent to us on WhatsApp. We confirm stock, the exact part and the total, then tell you how to pay and collect.")]
    fh, fs = faq_block(faqs)
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Hyundai and Kia parts by type</h1>
<p class="lead">{e(intro)}</p></div></section>
<section class="sec"><div class="wrap"><div class="cgrid">{tiles}</div></div></section>
<section class="sec alt"><div class="wrap narrow"><h2>Questions about Hyundai and Kia parts</h2>{fh}</div></section>'''
    shell("parts/index.html", "Hyundai & Kia Parts by Type | Autotex", "Body parts, headlamps, tail lamps, brake pads, brake discs, suspension, engine mounting, spark plugs and ignition coils for Hyundai and Kia in Singapore.",
          body, active="parts", crumbs=[("Parts", "parts/")], schema=[fs], prio="0.8")
    for c in C.values():
        r = "../../"
        pts = [p for p in P.values() if p["cat"] == c["id"]]
        xs = [x for x in PRODUCTS if x["cat"]["id"] == c["id"]]
        groups = []
        for bid, bn in BRANDS:
            rows = []
            for m in [m for m in M.values() if m["b"] == bid]:
                for pt in pts:
                    if not fits(m["fuel"], PT[pt["id"]]): continue
                    mine = [x for x in xs if x["m"] == m["id"] and x["p"] == pt["id"]]
                    mcell = f'<a href="{r}{bid}/{m["id"]}/#p-{pt["id"]}">{e(m["name"])} <i>{e(m["code"])}</i></a><small>{e(myears(m))}</small>'
                    if mine:
                        for x in mine:
                            need_side = x["part"]["side"] and not x["side"]
                            rows.append(f'<tr data-pid="{e(x["id"])}"><td><a href="{r}{x["url"]}">{e(m["name"])} <i>{e(m["code"])}</i></a><small>{e(myears(m))}</small></td>'
                                        f'<td>{e(x["part"]["name"])}{f" ({SIDE_L[x["side"]].split(" (")[0]})" if x["side"] else ""}</td><td class="r">{price_html(x)}</td><td class="r"><button class="btn add sm" type="button" data-add="{e(x["id"])}"{" data-side=\"1\"" if need_side else ""}>Add</button></td></tr>')
                    else:
                        rows.append(f'<tr data-ask="{m["id"]}|{pt["id"]}"><td>{mcell}</td><td>{e(pt["name"])}</td><td class="r"><span class="price ask">Ask for price</span></td>'
                                    f'<td class="r"><a class="btn wa sm" href="{ask_link(m, pt)}" rel="noopener">{WA_SVG}Ask</a></td></tr>')
            if rows:
                groups.append(f'<h2 id="{bid}">{e(bn)} {e(c["name"].lower())}</h2><div class="tbl"><table><thead><tr><th>Model</th><th>Part</th><th class="r">Price</th><th></th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>')
        others = "".join(f'<a class="chip" href="{r}parts/{o["id"]}/">{e(o["name"])}</a>' for o in C.values() if o["id"] != c["id"])
        units = ", ".join(sorted({p["unit"] for p in pts}))
        body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>{e(c["name"])} for Hyundai and Kia</h1>
<p class="lead">{e(c["line"])} for Hyundai and Kia models. Where a price is listed you can add the part to your cart. For the others, tap Ask and we reply on WhatsApp with the price and stock.</p></div></section>
<section class="sec"><div class="wrap">{"".join(groups)}<p class="small">Sold per {e(units)}. We confirm the exact fit for your car on WhatsApp before you pay.</p></div></section>
<section class="sec alt"><div class="wrap"><h2>Other part types</h2><div class="chips">{others}</div></div></section>'''
        sch = []
        if xs:
            sch.append({"@type": "ItemList", "name": f"{c['name']} for Hyundai and Kia", "numberOfItems": len(xs),
                        "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + "/" + x["url"], "name": x["title"]} for i, x in enumerate(xs)]})
        shell(f"parts/{c['id']}/index.html", f"Hyundai & Kia {c['name']} Singapore | Autotex"[:68], (lambda d: d + " Autotex, Kaki Bukit." if len(d) < 138 else d)(f"{c['name']} for Hyundai and Kia models in Singapore. {c['line']}. See the price or ask on WhatsApp."),
              body, active="parts", crumbs=[("Parts", "parts/"), (c["name"], f"parts/{c['id']}/")], schema=sch, prio="0.8")

# ---------------- price list ----------------
def build_prices():
    r = "../"
    blocks = []
    for bid, bn in BRANDS:
        for m in [m for m in M.values() if m["b"] == bid]:
            rows = "".join(f'<tr data-pid="{e(x["id"])}"><td><a href="{r}{x["url"]}">{e(x["part"]["name"])}{f" ({SIDE_L[x["side"]].split(" (")[0]})" if x["side"] else ""}</a></td><td>{e(x["part"]["unit"])}</td><td class="r">{price_html(x)}</td></tr>'
                           for x in PRODUCTS if x["m"] == m["id"])
            if rows:
                blocks.append(f'<details class="pl" id="{m["id"]}"><summary><b>{e(bn)} {e(m["name"])}</b> <i>{e(m["code"])}</i> <span>{e(myears(m))}</span></summary><div class="tbl"><table><thead><tr><th>Part</th><th>Sold as</th><th class="r">Price</th></tr></thead><tbody>{rows}</tbody></table></div></details>')
    tiles = "".join(f'<div class="pl-b"><h3>{e(bn)}</h3><div class="mgrid">{"".join(model_tile(m, r) for m in M.values() if m["b"] == bid)}</div></div>' for bid, bn in BRANDS)
    if blocks:
        listing = f'<h2>Listed prices</h2>{"".join(blocks)}<h2>Any other part</h2><p>If your part or car is not above, choose your model below and tap Ask on WhatsApp.</p>'
    else:
        listing = ('<h2>Prices on request</h2><p>We quote each part for your exact car instead of printing one list for every generation, facelift and engine. '
                   'Choose your model below, tap the part you need, and ask for the price on WhatsApp. We reply with the price and whether it is in stock.</p>')
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Hyundai and Kia parts prices</h1>
<p class="lead">Where a price is listed it is the price for the part as listed. For every other part, ask us on WhatsApp and we reply with the price and stock. We confirm the fit for your car before you pay.</p>
<p><a class="btn wa" href="{wa_link("Hi Autotex, I need a price for a part. My car plate / chassis number is: ")}" rel="noopener">{WA_SVG}Ask for a price on WhatsApp</a></p></div></section>
<section class="sec"><div class="wrap narrow">{listing}</div><div class="wrap">{tiles}</div></section>'''
    shell("prices/index.html", "Hyundai & Kia Parts Prices Singapore | Autotex", "Prices for Hyundai and Kia parts in Singapore. See listed prices by model, or ask Autotex for the price and stock of any part on WhatsApp.",
          body, active="prices", crumbs=[("Price list", "prices/")], prio="0.9")

# ---------------- simple pages ----------------
def build_pages():
    # search
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1 data-sr-title>Search parts</h1>
<div class="hero-f slim">{finder("../")}</div></div></section>
<section class="sec"><div class="wrap"><div data-results aria-live="polite"><p class="muted">Type your car and the part, for example “Avante brake pads” or “Sportage headlamp”.</p></div></div></section>'''
    shell("search/index.html", "Search Hyundai & Kia Parts | Autotex", "Search Hyundai and Kia parts by car model and part name.", body, crumbs=[("Search", "search/")], index=False, noindex=True)
    # cart
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Your cart</h1></div></section>
<section class="sec"><div class="wrap cart-g">
<div data-cart><p class="muted">Loading your cart…</p></div>
<form class="co" data-checkout>
<h2>Send your order</h2>
<p class="small">Your order opens in WhatsApp as a message to Autotex ({WA_SHOW}). Nothing is paid here. We reply to confirm price, stock, fit and collection.</p>
<label>Your name<input name="name" autocomplete="name" required></label>
<label>Car plate or chassis number<input name="car" placeholder="e.g. SMA1234X" autocapitalize="characters"><small>Helps us check the exact part for your car.</small></label>
<label>Collection<select name="collect"><option>Self-collect at Kaki Bukit</option><option>Please tell me about delivery</option></select></label>
<label>Notes<textarea name="note" rows="3" placeholder="Anything else we should know"></textarea></label>
<button class="btn wa big" type="submit">{WA_SVG}Send order on WhatsApp</button>
<p class="small muted" data-co-msg></p>
</form>
</div></section>'''
    shell("cart/index.html", "Your Cart | Autotex", "Your Autotex parts cart.", body, crumbs=[("Cart", "cart/")], index=False, noindex=True)
    # how to order
    qs = [("Do I pay online?", "No. Your cart is sent to us on WhatsApp. We confirm stock, the exact part for your car and the total, then tell you how to pay and collect."),
          ("What if I don't know my car's generation?", "Send your car plate or chassis number. The chassis number is printed on your vehicle log card. We use it to find the exact part."),
          ("Can I order parts for left and right sides?", "Yes. Lamps, mirrors and suspension parts ask you to pick left or right. Add both if you need a pair."),
          ("Can I change my order after sending it?", "Yes. Just reply in the same WhatsApp chat before we confirm.")]
    fh, fs = faq_block(qs)
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>How to order Hyundai and Kia parts from Autotex</h1>
<p class="lead">Find the part, add it to your cart, and send the cart to our WhatsApp. We check the fit before you pay.</p></div></section>
<section class="sec"><div class="wrap narrow">
<ol class="howto">
<li><h2>Find your part</h2><p>Use the three boxes on the home page (brand, model, part) or type your car and the part into search, for example “Kona spark plugs”. You can also browse by <a href="../hyundai/">Hyundai</a> or <a href="../kia/">Kia</a> model, or by <a href="../parts/">part type</a>.</p></li>
<li><h2>Check the model and years</h2><p>Each page shows the generation code and the years it fits, like Avante AD 2016-2020. If you are not sure, carry on: we check before you pay.</p></li>
<li><h2>Add to cart</h2><p>Pick left or right where asked, choose how many, and tap Add to cart. Your cart stays on your phone until you send it.</p></li>
<li><h2>Send the order on WhatsApp</h2><p>Open your <a href="../cart/">cart</a>, add your name and car plate or chassis number, and tap Send order on WhatsApp. The order arrives at {WA_SHOW} as a ready-made message.</p></li>
<li><h2>We confirm and you collect</h2><p>We reply with stock, the exact part and the total. Collect at {e(ADDR1)}, {e(ADDR2)}, or ask us about delivery.</p></li>
</ol>
<h2>Questions</h2>{fh}</div></section>'''
    howto = {"@type": "HowTo", "name": "How to order Hyundai and Kia parts from Autotex", "step": [
        {"@type": "HowToStep", "position": i + 1, "name": n} for i, n in enumerate(["Find your part", "Check the model and years", "Add to cart", "Send the order on WhatsApp", "We confirm and you collect"])]}
    shell("how-to-order/index.html", "How to Order Hyundai & Kia Parts | Autotex", "Find your Hyundai or Kia part, add it to the cart and send the order to Autotex on WhatsApp. We check the fit for your car before you pay.",
          body, active="order", crumbs=[("How to order", "how-to-order/")], schema=[fs, howto], prio="0.7")
    # about
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>About Autotex</h1>
<p class="lead">Autotex Aircon Enterprise is a Kia and Hyundai parts stockist in Kaki Bukit, Singapore. We bring parts in direct from Korea and sell them direct to Singapore drivers.</p></div></section>
<section class="sec"><div class="wrap two">
<div><h2>What we stock</h2><p>Hyundai and Kia body parts, headlamps and tail lamps, engine parts, suspension, engine mounting, brake pads, brake discs (rotors), cooling and aircon parts, alternators, starter motors, spark plugs and ignition coils.</p>
<h2>How we sell</h2><p>Owners rarely know a part number, so our shop is built around your car: choose the model, choose the part, and send us the order. We match the exact part to your car plate or chassis number before you pay.</p>
<h2>Panels and parts that need fitting</h2><p>A body panel such as a bumper, fender or bonnet usually needs fitting and painting after you buy it. If you need <a href="https://sgcarworkshop.sg/services/spray-painting-bodywork/">a bodywork and spray-painting workshop to fit this Kia or Hyundai panel</a>, SG Car Workshop is a directory of independent Singapore workshops that you can start from. Its listings are written in its own words from public Google Business Profile details, and its paid listings are labelled Featured.</p>
<p>To be clear about it: Autotex has a Featured (paid) listing on SG Car Workshop, and both this website and the directory are run by Page One Singapore. We do not endorse every workshop on that list, so check any workshop, including us, before you decide.</p></div>
<div class="facts"><h2>Business details</h2><dl class="spec">
<div><dt>Registered name</dt><dd>{e(LEGAL)}</dd></div>
<div><dt>UEN</dt><dd class="mono">{UEN}</dd></div>
<div><dt>Registered</dt><dd>{REG}</dd></div>
<div><dt>Business</dt><dd>Retail sale of motor vehicle parts and accessories</dd></div>
<div><dt>Address</dt><dd>{e(ADDR1)}, {e(ADDR2)}</dd></div>
<div><dt>Opening hours</dt><dd>{HOURS_LINE}</dd></div>
<div><dt>Phone</dt><dd><a href="tel:{TEL_H}">{TEL}</a></dd></div>
<div><dt>WhatsApp</dt><dd><a href="https://wa.me/{WA}" rel="noopener">{WA_SHOW}</a></dd></div>
<div><dt>Google rating</dt><dd>5.0 from 4 reviews (<a href="{GMAP}" rel="noopener">Google Maps</a>)</dd></div>
</dl></div></div></section>'''
    shell("about/index.html", "About Autotex, Kia & Hyundai Parts Stockist", f"Autotex Aircon Enterprise (UEN {UEN}), registered {REG}: Kia and Hyundai parts stockist in Kaki Bukit, Singapore, stocking direct from Korea.",
          body, active="", crumbs=[("About", "about/")], prio="0.6")
    # contact
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Contact Autotex</h1>
<p class="lead">WhatsApp is fastest. Send your car plate or chassis number and the part you need.</p></div></section>
<section class="sec"><div class="wrap cgrid3">
<a class="cc" href="{wa_link("Hi Autotex, I need a part for my car. Car plate / chassis: ")}" rel="noopener">{WA_SVG}<b>WhatsApp</b><span>{WA_SHOW}</span></a>
<a class="cc" href="tel:{TEL_H}">{ICON['phone']}<b>Call</b><span>{TEL}</span></a>
<a class="cc" href="{GMAP}" rel="noopener">{ICON['pin']}<b>Visit</b><span>{e(ADDR1)}<br>{e(ADDR2)}</span></a>
</div><div class="wrap"><h2>Opening hours</h2>{hours_html("spec hours")}<p class="small">Please WhatsApp before you come down so we can check stock and get your parts ready.</p></div></section>'''
    shell("contact/index.html", "Contact Autotex | Kia & Hyundai Parts Kaki Bukit", f"WhatsApp {WA_SHOW} or call {TEL}. Autotex, {ADDR1}, Kaki Bukit, Singapore 417883. Open Mon to Sat.",
          body, active="contact", crumbs=[("Contact", "contact/")], prio="0.6")
    # privacy policy (Singapore PDPA 2012), added 8 Nov 2026. Describes only what this site really collects (wa.js tap counter, at.js cart + live catalogue, Google Fonts, host logs).
    body = f'''<section class="ph"><div class="wrap narrow">{{{{CRUMBS}}}}<h1>Privacy Policy</h1>
<p class="lead">What we collect when you use this website or contact {e(LEGAL)}, and what we do with it.</p>
<p class="small muted">Last updated {PRIVACY_UPDATED}</p></div></section>
<article class="sec art-b"><div class="wrap narrow">
<h2>Who runs this site</h2>
<p>This website is run by {e(LEGAL)} (UEN {UEN}), {e(ADDR1)}, {e(ADDR2)}.</p>
<h2>When you contact us</h2>
<p>You can reach us by WhatsApp on {WA_SHOW} or by phone call on {TEL}. What you send us, such as your name, car plate or chassis number, the part you need and photos of the old part, is used only to reply to you, check the right part for your car and handle your order.</p>
<h2>Your cart and order</h2>
<p>Your cart is kept in your own browser on your device, not on our server. When you tap Send order on WhatsApp, the order form (your name, car plate or chassis number, collection choice and notes) is put into a WhatsApp message to us. Nothing is sent until you send that message in WhatsApp, and nothing is paid on this website. You can clear the cart at any time.</p>
<h2>Prices and stock shown on the site</h2>
<p>To show current prices, stock and photos, your browser loads our parts catalogue from our database provider. This only reads the catalogue; it does not send your details.</p>
<h2>Counting taps on our WhatsApp buttons</h2>
<p>We count how often visitors tap the WhatsApp buttons and send orders on WhatsApp, so we can see which pages help people get in touch. Each tap sends one small record to our dashboard: the page it was tapped on, the button text, whether the device is a phone or a computer, the site you came from and any campaign tag in the link, whether you came from an ad (not the ad click code), how many pages you viewed and how long you had been on the site, your screen size, time zone and browser language, and two random codes: one that lasts only while your browser tab is open, and one kept in your browser so repeat visits from the same browser can be counted. The record is stored with the time of the tap.</p>
<p>The tap counter does not send or store your name, phone number or message. The WhatsApp message itself goes through WhatsApp, not through this counter. The counter does not use cookies.</p>
<h2>Fonts and server logs</h2>
<p>The text fonts on this site are loaded from Google Fonts, so your browser connects to Google to fetch them. Our website host keeps standard server logs, such as IP address, browser type and the pages requested, to keep the site running and secure.</p>
<h2>No selling of data</h2>
<p>We do not sell your details or give them to advertisers.</p>
<h2>Your rights under the PDPA</h2>
<p>We handle personal data in line with Singapore's Personal Data Protection Act 2012. To ask for a copy of the details we hold about you, or to have them corrected or removed, WhatsApp us on <a href="{wa_link("Hi Autotex, I would like a copy of my details, or to have them corrected or removed.")}" rel="noopener">{WA_SHOW}</a> or call <a href="tel:{TEL_H}">{TEL}</a>.</p>
</div></article>'''
    shell("privacy-policy/index.html", "Privacy Policy | Autotex", f"How {LEGAL} handles your details: WhatsApp and phone enquiries, your cart, tap counting on our buttons, server logs and your rights under Singapore PDPA.",
          body, active="", crumbs=[("Privacy Policy", "privacy-policy/")], prio="0.3")
    # staff: tiny noindex redirect to the Base44 staff dashboard (not in sitemap)
    write("staff/index.html", f'''<!doctype html>
<html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Staff dashboard | Autotex</title><meta name="robots" content="noindex,nofollow">
<meta http-equiv="refresh" content="0;url={DB_URL}"><link rel="canonical" href="{DB_URL}">
<script>location.replace("{DB_URL}");</script></head>
<body style="font:16px/1.5 system-ui,sans-serif;padding:24px"><p>Opening the staff dashboard. <a href="{DB_URL}">Continue to the staff dashboard</a>.</p></body></html>
''')
    # 404
    body = f'''<section class="ph"><div class="wrap"><h1>Page not found</h1><p class="lead">That page has moved or never existed. Search for your part, or use one of the links below.</p>
<div class="hero-f slim">{finder("{{{{R}}}}")}</div></div></section>
<section class="sec"><div class="wrap"><h2>Where to go next</h2>
<div class="chips"><a class="chip" href="/hyundai/">Hyundai parts</a><a class="chip" href="/kia/">Kia parts</a><a class="chip" href="/parts/">Parts by type</a><a class="chip" href="/prices/">Price list</a><a class="chip" href="/articles/">Guides</a><a class="chip" href="/how-to-order/">How to order</a><a class="chip" href="/contact/">Contact and opening hours</a><a class="chip" href="/">Home</a></div>
<p>Or WhatsApp us on <a href="https://wa.me/{WA}" rel="noopener">{WA_SHOW}</a> or call <a href="tel:{TEL_H}">{TEL}</a> with your car plate or chassis number and the part you need.</p></div></section>'''
    shell("404.html", "Page not found | Autotex", "Page not found. Search for a Hyundai or Kia part, or go to the parts, guides or contact pages.", body, index=False, noindex=True)

# ---------------- articles ----------------
ARTS = [
 ("find-the-right-part-without-a-part-number", "How to find the right Hyundai or Kia part without a part number",
  "Most owners don't know their part numbers. Here is what to send so you get the right part the first time.",
  [("What do you need to find the right part?", "You need three things: the model, the generation (or year) and, for some parts, the engine. The fastest way to give all three is your chassis number, which is printed on your vehicle log card. Send it with the part you need and we match the exact part."),
   ("Why does the generation matter?", "The same model name covers different cars over the years. A Hyundai Avante AD (2016-2020) and an Avante CN7 (2020 onwards) use different bumpers, lamps and many other parts. That is why every page on our shop shows the generation code and years."),
   ("What about facelifts and engines?", "A facelift partway through a generation can change lamps, bumpers and grilles. Engines change spark plugs, ignition coils, filters and mounts. Your chassis number settles both."),
   ("What to send us on WhatsApp", "<ol><li>Your car plate or chassis number.</li><li>The part, and left or right if it is a lamp, mirror or suspension part.</li><li>A photo of the old part if you have it.</li></ol>")],
  "body-parts"),
 ("brake-pads-and-discs-when-to-change", "Brake pads and brake discs: when to change one or both",
  "Pads wear first, discs wear slower. How to tell what your car needs.",
  [("How do you know your brake pads are worn?", "Common signs are a squeal when braking (many pads have a metal wear indicator that makes this sound), a longer stopping distance, or a brake warning light on cars with pad sensors. A workshop can measure the pad thickness in minutes."),
   ("When should the discs be changed too?", "Every disc has a minimum thickness stamped on it. If it is worn below that, scored deeply, or warped (you feel a shudder in the pedal or steering when braking), change the discs. Fitting new pads on worn discs shortens the life of the new pads."),
   ("Should pads be changed in pairs?", "Yes. Pads are sold and changed per axle, both sides at once, so the car brakes evenly. Discs are also changed in pairs on the same axle."),
   ("Front or rear?", "Front pads usually wear faster because the front brakes do most of the work. Our shop lists front and rear pads separately for each model.")],
  "brake-pads"),
 ("signs-of-a-worn-engine-mounting", "Signs of a worn engine mounting on a Hyundai or Kia",
  "Vibration at idle and a knock when you change gear can both point to the engine mounts.",
  [("What does an engine mounting do?", "Engine and gearbox mountings hold the engine in the car and absorb its vibration. They are rubber (some are fluid-filled) bonded to metal brackets, and the rubber wears and cracks with age and heat."),
   ("What are the common signs of a worn mounting?", "<ul><li>More vibration in the cabin or steering wheel at idle, especially in Drive at a traffic light.</li><li>A knock or clunk when you pull away, change gear or go over a bump.</li><li>The engine visibly rocking when someone revs it with the bonnet open.</li></ul>"),
   ("Is it safe to keep driving?", "A worn mounting lets the engine move more than it should, which strains hoses, wiring and the exhaust. Have it checked by a workshop and change the worn mount before other parts get damaged."),
   ("Which mounting do I need?", "Most cars have several mounts: an engine mount, a gearbox mount and a lower torque mount. Tell us the noise and where it comes from, with your car plate, and we will tell you which mount it usually is.")],
  "engine-mounting"),
 ("signs-of-a-failing-ignition-coil", "Signs of a failing ignition coil on a Hyundai or Kia",
  "A rough idle, a flashing check-engine light and a car that shakes under load can point to a weak ignition coil.",
  [("What does an ignition coil do?", "The ignition coil turns the car battery's low voltage into the high voltage a spark plug needs to ignite the fuel and air in each cylinder. Many modern engines have one coil for each cylinder, mounted on top of the spark plug."),
   ("What are the common signs of a failing ignition coil?", "<ul><li>A rough or shaky idle, especially when the engine is warm.</li><li>The car hesitates or jerks when you accelerate, or feels weak going uphill.</li><li>The check-engine light comes on, or flashes while the engine is misfiring.</li><li>Higher fuel use and a smell of unburnt fuel from the exhaust.</li></ul>"),
   ("Is it the coil or the spark plug?", "Both cause a misfire, so a workshop usually reads the fault code first. It tells you which cylinder is misfiring. The mechanic can then swap that coil with a neighbouring cylinder to see if the misfire follows it. If it does, the coil is at fault. If not, check the spark plug."),
   ("Is it safe to keep driving with a misfire?", "A flashing check-engine light means the engine is misfiring badly. Unburnt fuel can reach the exhaust and damage the catalytic converter, so have the car checked soon and avoid hard driving until then."),
   ("Which coil do I need?", "Coils differ by model, generation and engine. Send us your car plate or chassis number and which cylinder is misfiring, and we will match the right coil. Many owners change the spark plugs at the same time, so ask us about both.")],
  "ignition-coils", "2026-11-02"),
 ("signs-of-worn-spark-plugs", "Signs your Hyundai or Kia needs new spark plugs",
  "Hard starts, a rough idle and poor fuel economy can all point to worn spark plugs. Common signs, and how to tell them from a bad coil.",
  [("What does a spark plug do?", "A spark plug creates the spark that ignites the fuel and air in each cylinder of a petrol engine. The electrodes wear down with use, so over time the spark gets weaker and the engine burns fuel less cleanly."),
   ("What are the common signs of worn spark plugs?", "<ul><li>The engine is slower to start, or cranks for longer than before.</li><li>A rough or uneven idle, or a slight shake when stopped at a traffic light.</li><li>Hesitation or a flat spot when you accelerate.</li><li>Higher fuel use than usual.</li><li>A check-engine light that comes on with a misfire code.</li></ul>"),
   ("When should spark plugs be changed?", "Follow the service schedule in your owner's manual, because the interval depends on the engine and the type of plug fitted. Your workshop can also pull the plugs, check the electrode wear and tell you whether they are due."),
   ("Is it the spark plug or the ignition coil?", "Both cause a misfire, and they sit together in most engines. A workshop reads the fault code to find the cylinder, then checks the plug and the coil on that cylinder. If you are changing plugs on an older car, ask the workshop to look at the coils at the same time."),
   ("Do all cars need spark plugs?", "No. Spark plugs are for petrol engines. Diesel engines do not use them and electric cars have no engine, so they are not listed for those models in our shop."),
   ("Which spark plugs do I need?", "Plugs differ by engine, not just by model. Send us your car plate or chassis number and we will match the right set. Plugs are sold as a set for the number of cylinders your engine has.")],
  "spark-plugs", "2026-11-04"),
 ("signs-of-a-failing-alternator", "Signs of a failing alternator on a Hyundai or Kia",
  "A battery warning light, dim lights and a car that stalls or will not restart can point to the alternator, not just the battery. Common signs, and how to tell them apart.",
  [("What does an alternator do?", "The alternator is driven by the engine and generates the electricity that runs the car's lights, wipers, infotainment and ignition while the engine is running. It also recharges the battery. When it weakens, the car starts to run on the battery alone until the battery goes flat."),
   ("What are the common signs of a failing alternator?", "<ul><li>The battery or charging warning light comes on while you are driving.</li><li>Headlights and dashboard lights dim or flicker, especially at idle or when the aircon and other electrics are on.</li><li>The car is slow to start, or the battery goes flat again soon after a jump start or a new battery.</li><li>A whining or grinding noise from the engine bay that changes with engine speed.</li><li>Electrical items such as windows, the audio system or the aircon blower behave weakly or erratically.</li></ul>"),
   ("Is it the alternator or the battery?", "Both give a car that will not start, so they are easy to confuse. A weak battery usually shows up when starting, while a failing alternator tends to show up while driving, with the warning light and dimming lights. A workshop can test the battery and the charging voltage in a few minutes. If you keep replacing batteries, have the alternator tested."),
   ("Can I keep driving with a failing alternator?", "Not for long. The car runs on battery power until it runs flat, and then it can stall without warning, including on an expressway. If the warning light comes on, switch off unnecessary electrics, head for a safe place and have the car checked."),
   ("Do all cars have an alternator?", "Petrol and diesel cars do. Fully electric cars have no engine-driven alternator, so it is not listed for those models in our shop."),
   ("Which alternator do I need?", "Alternators differ by model, generation and engine. Send us your car plate or chassis number and we will match the right one. Ask about the drive belt at the same time, because a worn or loose belt can also cause charging problems.")],
  "electrical", "2026-11-06"),
 ("hyundai-kia-aircon-not-cold-which-parts", "Hyundai or Kia aircon not cold: which parts usually cause it",
  'Aircon blowing warm on a Hyundai or Kia? The usual causes: low refrigerant, compressor, condenser, cooling fan and cabin filter, and what to check first.',
  [('Why is my Hyundai or Kia aircon not cold?', 'The aircon needs three things to cool: enough refrigerant, a compressor that pumps it, and a condenser with airflow to release the heat. If any of the three fails, the air from the vents turns lukewarm or warm. Weak airflow is a different problem and usually points to the cabin filter or the blower.'),
   ('What are the usual causes?', '<ul><li>Low refrigerant. The system is sealed, so low gas normally means a leak somewhere in the pipes, joints or condenser.</li><li>A compressor that does not engage, or that is noisy or worn.</li><li>A condenser that is blocked with dirt, or damaged by stones or a minor front impact.</li><li>A radiator or condenser fan that does not run, so the heat cannot escape, especially in slow traffic.</li><li>A choked cabin air filter, which cuts airflow rather than temperature.</li></ul>'),
   ('Is it warm air or weak airflow?', 'Note which one you have. If the fan is strong but the air is not cold, look at the refrigerant, compressor, condenser and cooling fans. If the air is cold but weak, the cabin filter is the first thing to check, then the blower. Cold at highway speed but warm at traffic lights often points to a cooling fan that is not working.'),
   ('Will a gas top-up fix it?', 'Only if the gas was low, and low gas means the leak is still there. A top-up without a leak test may last days or a few weeks before the aircon warms up again. Ask the workshop to find the leak, and replace the part that is leaking, often a condenser, a hose or a compressor seal.'),
   ('Which aircon parts does Autotex supply?', 'For Hyundai and Kia models sold in Singapore we list the aircon compressor, the aircon condenser and the cabin air filter. The radiator fan is listed for petrol and diesel models. Refrigerant, leak testing and fitting are done by an aircon workshop, not by Autotex as the parts stockist.'),
   ('Can I keep driving with the aircon off?', 'Usually yes, but get a noisy or seizing compressor checked soon. On belt-driven systems a failing compressor can load the drive belt that also turns other parts. If the engine temperature gauge rises as well, stop in a safe place: that is an engine cooling problem, not only an aircon one.'),
   ('What should I send Autotex to get the right part?', 'Send your car plate or chassis number and the part you think you need. Compressors, condensers and fans differ by model, generation and engine, so the chassis number settles the match. A photo of the old part or the label on the compressor helps. If you are not sure which part has failed, have the aircon tested first.')],
  "cooling-aircon", "2026-11-08"),
]

# 40-60 word direct answers shown under each article H1, and meta descriptions of 120-160 characters (2 Nov 2026 SEO pass)
ART_ANS = {
 "hyundai-kia-aircon-not-cold-which-parts": 'If a Hyundai or Kia aircon is not cold, the usual causes are low refrigerant from a leak, a compressor that is not engaging, a blocked or damaged condenser, a cooling fan that is not running, or a clogged cabin filter. A workshop checks gas pressure and the compressor first, then the parts around them.',
 "find-the-right-part-without-a-part-number": "To get the right Hyundai or Kia part first time, send three things: your car model with its generation or year, the part you need, and your chassis number from the vehicle log card. The chassis number settles the generation, facelift and engine, which decide the fit. A photo of the old part helps too.",
 "brake-pads-and-discs-when-to-change": "Change brake pads when they squeal, the car takes longer to stop or a warning light comes on. Change the discs too if they are worn below the minimum thickness stamped on them, deeply scored or warped. Pads and discs are changed in pairs on the same axle, so both sides brake evenly.",
 "signs-of-a-worn-engine-mounting": "A worn engine mounting usually shows as extra vibration at idle, a knock or clunk when you pull away or change gear, or an engine that visibly rocks when revved. The rubber wears with age and heat, so have a workshop check it and replace the worn mount before hoses and wiring are strained.",
 "signs-of-worn-spark-plugs": "Worn spark plugs usually show as a slow or hard start, a rough idle, hesitation when you accelerate and higher fuel use. A misfire code can also appear. Follow the interval in your owner's manual, and have a workshop check the plugs and coils together, as both cause similar symptoms.",
 "signs-of-a-failing-alternator": "A failing alternator usually shows as a battery or charging warning light, dim or flickering lights, a car that is slow to start or keeps flattening the battery, and sometimes a whine from the engine bay. A workshop can test the battery and charging voltage to tell the two apart quickly.",
 "signs-of-a-failing-ignition-coil": "A failing ignition coil usually shows as a rough idle, hesitation or jerking when you accelerate, or a check-engine light that comes on or flashes during a misfire. A workshop reads the fault code to find the cylinder, then swaps coils to confirm. Avoid hard driving while the light flashes.",
}
ART_DESC = {
 "hyundai-kia-aircon-not-cold-which-parts": 'Aircon blowing warm on a Hyundai or Kia? The usual causes: low refrigerant, compressor, condenser, cooling fan and cabin filter, and what to check first.',
 "find-the-right-part-without-a-part-number": "Most owners don't know their part numbers. Send your model, generation, chassis number and a photo of the old part and we match the right part.",
 "brake-pads-and-discs-when-to-change": "Pads wear first and discs wear slower. How to tell from the squeal, the pedal feel and the disc thickness whether your Hyundai or Kia needs pads, discs or both.",
 "signs-of-a-worn-engine-mounting": "Vibration at idle and a knock when you change gear can point to the engine mounts. Common signs of a worn engine mounting on a Hyundai or Kia.",
 "signs-of-worn-spark-plugs": "Hard starts, a rough idle and poor fuel economy can point to worn spark plugs. Common signs on a Hyundai or Kia, and how to tell them from a bad ignition coil.",
 "signs-of-a-failing-alternator": "Battery warning light, dim lights or a car that stalls can point to a failing alternator. Signs on a Hyundai or Kia, and how to tell it from a flat battery.",
 "signs-of-a-failing-ignition-coil": "A rough idle, a flashing check-engine light and a car that shakes under load can point to a weak ignition coil. Signs, and how to tell it from a spark plug.",
}

def build_articles():
    cards = []
    for slug, t, d, qa, cat, *_dt in ARTS:
        adate = _dt[0] if _dt else "2026-10-29"
        d = ART_DESC.get(slug, d)
        r = "../../"
        c = C[cat]
        xs = [x for x in PRODUCTS if x["cat"]["id"] == cat][:4]
        more = (f'<section class="sec alt"><div class="wrap"><h2>{e(c["name"])} we stock</h2><div class="pgrid">{"".join(card(x, r) for x in xs)}</div></div></section>' if xs else "")
        sec = "".join(f'<h2>{e(q)}</h2>{a if a.startswith("<") else f"<p>{a}</p>"}' for q, a in qa)
        nice = datetime.date.fromisoformat(adate).strftime("%-d %b %Y")
        body = f'''<section class="ph"><div class="wrap narrow">{{{{CRUMBS}}}}<h1>{e(t)}</h1><p class="lead">{e(ART_ANS[slug])}</p>
<p class="small muted">By Autotex · Published {nice} · Last updated {nice}</p></div></section>
<article class="sec art-b"><div class="wrap narrow">{sec}
<div class="callout"><b>Need the part?</b> See <a href="{r}parts/{cat}/">{e(c["name"].lower())} for every Hyundai and Kia model</a>, or <a href="{wa_link("Hi Autotex, I read your guide and need a part. Car plate / chassis: ")}" rel="noopener">WhatsApp us your car plate</a>.</div>
</div></article>
{more}'''
        art = {"@type": "Article", "headline": t, "description": d, "datePublished": adate, "dateModified": adate,
               "author": {"@id": BASE + "/#store"}, "publisher": {"@id": BASE + "/#store"}, "image": BASE + "/og.jpg",
               "mainEntityOfPage": BASE + f"/articles/{slug}/"}
        # FAQPage = the question-form headings of this article, with the same answer text that is visible below them
        fq = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", a))).strip()}}
              for q, a in qa if q.endswith("?")]
        sch = [art] + ([{"@type": "FAQPage", "mainEntity": fq}] if fq else [])
        shell(f"articles/{slug}/index.html", (t + " | Autotex") if len(t) < 50 else t, d, body, crumbs=[("Guides", "articles/"), (t, f"articles/{slug}/")],
              schema=sch, og_type="article", prio="0.6")
        cards.append(f'<a class="ac" href="{slug}/"><span class="ac-i">{ICON[c["icon"]]}</span><b>{e(t)}</b><span>{e(d)}</span></a>')
    topics = _join([a[1].rstrip(".").lower() if False else a[1] for a in ARTS])
    intro = (f"These {len(ARTS)} guides are short, practical notes for Hyundai and Kia owners in Singapore who need to work out which part their car needs before they order. "
             f"They cover {_join([a[1] for a in ARTS])}. Each guide explains how the part works, the common signs that it is worn or failing, and what to send Autotex so we match the right part to your car. "
             f"The signs are general mechanical knowledge, not a diagnosis: a workshop should confirm the cause before you buy. "
             f"When you are ready, the guides link to the matching parts for every Hyundai and Kia model we supply, and you can WhatsApp your car plate or chassis number for a fit check.")
    faqs = [("What do I need to send to get the right Hyundai or Kia part?", "Your car plate or chassis number, printed on the vehicle log card, and the part you need. For lamps, mirrors and suspension parts, say left or right. A photo of the old part helps."),
            ("Can these guides tell me what is wrong with my car?", "No. They describe common signs of wear for each part. The same sign can have more than one cause, so have a workshop confirm the fault before you order the part."),
            ("Where do I find the part once I know what I need?", "Each guide links to the part type for every Hyundai and Kia model we supply. You can also pick your model, search for the part, or ask on WhatsApp for the price and stock.")]
    fh, fs = faq_block(faqs)
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Guides for Hyundai and Kia owners</h1>
<p class="lead">{e(intro)}</p></div></section>
<section class="sec"><div class="wrap agrid">{"".join(cards)}</div></section>
<section class="sec alt"><div class="wrap narrow"><h2>Questions about these guides</h2>{fh}</div></section>'''
    shell("articles/index.html", "Hyundai & Kia Parts Guides | Autotex", "Practical guides for Hyundai and Kia owners in Singapore: finding the right part, brakes, engine mounting, ignition coils and more.",
          body, crumbs=[("Guides", "articles/")], schema=[fs], prio="0.6")

# ---------------- data.js, static files, images ----------------
def build_data():
    d = {"wa": WA, "live": LIVE,
         "brands": [{"id": b, "name": n} for b, n in BRANDS],
         "models": [dict(m) for m in M.values()],
         "cats": [{"id": c["id"], "name": c["name"], "line": c["line"], "svg": ICON[c["icon"]]} for c in C.values()],
         "parts": [{"id": p["id"], "cat": p["cat"], "name": p["name"], "alias": p["alias"], "side": p["side"], "unit": p["unit"], "need": p["need"]} for p in P.values()],
         "photoMap": {i: f"assets/p/{i}.jpg" for i in sorted(PHOTO_IDS)},
         "products": [dict({k: x[k] for k in ("id", "m", "p", "url", "price", "oem", "stock", "side", "note", "created")}, photos=x["ph_entries"]) for x in PRODUCTS]}
    (HERE / "data.js").write_text("/* Autotex catalogue baseline, generated by build.py " + TODAY + " from db/*.json. The live database overrides it in the browser. */\nwindow.AT=" + json.dumps(d, separators=(",", ":"), ensure_ascii=False) + ";\n")

def build_static():
    for f in ("at.css", "at.js", "wa.js", "data.js"):
        shutil.copy(HERE / f, OUT / f)
    for f in (HERE / "assets").iterdir():
        if f.is_dir(): shutil.copytree(f, OUT / "assets" / f.name, dirs_exist_ok=True)
        else: shutil.copy(f, OUT / f.name)
    bots = ["*", "Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Applebot-Extended", "DuckAssistBot"]
    write("robots.txt", "".join(f"User-agent: {b}\n" for b in bots) + "Allow: /\nDisallow: /staff/\nDisallow: /cart/\nDisallow: /search/\n\n" + f"Sitemap: {BASE}/sitemap.xml\n")
    # lastmod = the day a page's content last changed (hash manifest src/lastmod.json), never just today's build date
    prev = json.loads(LM_FILE.read_text()) if LM_FILE.exists() else {}
    lm = {}
    for u, hsh in LM_NEW.items():
        old = prev.get(u)
        lm[u] = [hsh, old[1] if old and old[0] == hsh else TODAY]
    LM_FILE.write_text(json.dumps(lm, indent=0, sort_keys=True) + "\n")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"<url><loc>{u}</loc><lastmod>{lm[u][1]}</lastmod><priority>{p}</priority></url>\n" for u, p in SITEMAP) + "</urlset>\n")
    global UPDATED
    UPDATED = max(lm[u][1] for u, _ in SITEMAP)
    write(f"{INDEXNOW}.txt", INDEXNOW)
    write("site.webmanifest", json.dumps({"name": "Autotex Kia & Hyundai Parts", "short_name": "Autotex", "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#12161C", "background_color": "#ffffff", "display": "standalone"}))
    cats = "\n".join(f"- {c['name']}: {c['line']}. {BASE}/parts/{c['id']}/" for c in C.values())
    models = "\n".join(f"- {BR[m['b']]} {m['name']} {mcy(m, m['years'])}: {BASE}/{m['b']}/{m['id']}/" for m in M.values())
    bps = "\n".join(f"- {t}, {sm}: {u}" for u, t, sm in BP_INDEXED)
    arts = "\n".join(f"- {a[1]}: {ART_DESC.get(a[0], a[2])} {BASE}/articles/{a[0]}/" for a in ARTS)
    write("llms.txt", f"""# Autotex (Autotex Aircon Enterprise)

> Kia and Hyundai parts stockist in Kaki Bukit, Singapore. Stocks parts direct from Korea and sells direct to Singapore drivers. Pick your car and part, see the price where listed or ask on WhatsApp.

Last updated: {UPDATED}

## Business details
- Registered name: {LEGAL}, UEN {UEN}, registered {REG}
- Address: {ADDR1}, {ADDR2}
- Opening hours: {HOURS_LINE}
- Phone: {TEL}. WhatsApp: {WA_SHOW}
- Google rating: 5.0 from 4 reviews
- Prices: listed on the product page where set; otherwise quoted on WhatsApp. Autotex confirms stock and fit (by car plate or chassis number) before payment
- Ordering: add parts to the cart and send the order on WhatsApp. Collect at the shop, or delivery within 1 day at S$10, free above S$80. Returns within 7 days in the original packaging

## Key pages
- Home: {BASE}/
- Hyundai parts ({sum(1 for m in M.values() if m['b'] == 'hyundai')} models): {BASE}/hyundai/
- Kia parts ({sum(1 for m in M.values() if m['b'] == 'kia')} models): {BASE}/kia/
- Parts by type: {BASE}/parts/
- Full price list (every car and part): {BASE}/prices/
- How to order: {BASE}/how-to-order/
- About Autotex (business details; also notes Autotex has a Featured (paid) listing on the SG Car Workshop directory, which Page One Singapore also runs): {BASE}/about/
- Contact and directions: {BASE}/contact/
- Privacy policy: {BASE}/privacy-policy/

## Parts by type
{cats}

## Guides
{arts}

## Part pages by brand ({len(BP_INDEXED)}): models covered, years and price range per part type
{bps}

## Models
{models}
""")
    write("htaccess.txt", f"""# .htaccess for https://autotexautoparts.com.sg (the Bridge cannot write .htaccess; paste via cPanel)
Options -Indexes
DirectoryIndex index.html
ErrorDocument 404 /404.html
RewriteEngine On
RewriteCond %{{HTTPS}} off [OR]
RewriteCond %{{HTTP_HOST}} ^www\\. [NC]
RewriteRule ^ https://autotexautoparts.com.sg%{{REQUEST_URI}} [L,R=301]
<IfModule mod_headers.c>
<FilesMatch "\\.(html)$">
Header set Cache-Control "max-age=3600"
</FilesMatch>
Header set X-Content-Type-Options "nosniff"
</IfModule>
""")

if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    build_data()
    build_home(); build_brandparts(); build_brands(); build_models(); build_products(); build_sets(); build_cats(); build_prices(); build_pages(); build_articles()
    build_static()
    import pull_photos; pull_photos.run(OUT)
    cols = ["id", "title", "description", "link", "image_link", "availability", "price", "condition", "brand", "mpn", "identifier_exists", "google_product_category", "product_type", "shipping"]
    write("merchant-feed.tsv", "\t".join(cols) + "\n" + "".join("\t".join(str(r[k]).replace("\t", " ").replace("\n", " ") for k in cols) + "\n" for r in FEED))
    print(f"built {len(SITEMAP)} indexed pages, {len(PRODUCTS)} products -> {OUT}")
