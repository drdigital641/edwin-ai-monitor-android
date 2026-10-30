#!/usr/bin/env python3
"""Partware Auto Pte. Ltd. - Honda parts shop preview (Page One Singapore, built 30 Oct 2026).

Run:  python3 build.py OUT_DIR        (default ./site)
Facts: FACTS.md only (ACRA via recordowl.com, Yellow Pages, Facebook page). No prices, ratings, export countries,
shipping terms or "authorised dealer" claims. Honda is written as text only, never a logo.
Catalogue: catalog.py (+ optional catalogue.json = staff changes exported from /staff/). Prices are SAMPLES until
confirmed; with LIVE = True, sample prices are hidden from pages and schema and shown as "Ask for price".
Preview: BASE below (the parent preview folder's .htaccess hides it; pages carry no noindex).
"""
import html, json, sys, datetime, hashlib, shutil, re
from pathlib import Path
from urllib.parse import quote
from catalog import BRANDS, MODELS, CATS, PARTS, GRADES, fits, sample_price

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE / "site")
LIVE = False  # True at go-live: sample prices are not published
BASE = "https://pageonesingapore.com/preview/partware-auto"  # ONE constant: swap for the client's own domain at go-live
TODAY = datetime.date.today().isoformat()
BRAND = "Partware Auto"
LEGAL = "Partware Auto Pte. Ltd."
UEN = "201540164H"
INC = "11 November 2015"
# ACRA lists the registered address as #01-24; Yellow Pages and the Facebook listing title say #01-21.
# CLIENT MUST CONFIRM the shop unit number. Change it here only.
UNIT = "#01-21"
ADDR1 = f"10 Kaki Bukit Road 1, {UNIT}"
ADDR2 = "KB Industrial Building, Singapore 416175"
TEL = "6747 5028"; TEL_H = "+6567475028"
WA = "6587977581"; WA_SHOW = "+65 8797 7581"
FB = "https://www.facebook.com/partwareauto"
GMAP = "https://www.google.com/maps/search/?api=1&query=" + quote("Partware Auto 10 Kaki Bukit Road 1 KB Industrial Building Singapore 416175")
INDEXNOW = hashlib.sha1(b"partware-auto-indexnow").hexdigest()[:32]
e = lambda s: html.escape(str(s), quote=True)
SUFFIX = " | Partware Auto"
HOURS = [("Monday to Friday", "9am to 6pm"), ("Saturday", "9am to 3pm"), ("Sunday and public holidays", "Closed (Sunday is not listed on Facebook; to be confirmed)")]


def T(*cands):
    """First candidate title under 60 characters."""
    for c in cands:
        if len(c) < 60:
            return c
    return cands[-1][:59]


def D(s):
    assert len(s) < 160, (len(s), s)
    return s


# ---------------- catalogue ----------------
BR = {b: n for b, n in BRANDS}
M = {m[0]: dict(id=m[0], b=m[1], name=m[2], code=m[3], years=m[4], alias=m[5], fuel=m[6]) for m in MODELS}
C = {c[0]: dict(id=c[0], name=c[1], line=c[2], icon=c[3]) for c in CATS}
P = {p[0]: dict(id=p[0], cat=p[1], name=p[2], alias=p[3], side=p[4], unit=p[5]) for p in PARTS}


def mlabel(m): return f"{BR[m['b']]} {m['name']} ({m['code']})"
def yrs(m): return m["years"].replace("-now", " onwards")


PNOTE = {"drive-belt": "Some Honda engines use a timing chain instead of a timing belt. Tell us your engine and we will confirm which part applies."}
PRODUCTS = []
for mt in MODELS:
    m = M[mt[0]]
    for pt in PARTS:
        if not fits(mt, pt):
            continue
        p = P[pt[0]]
        PRODUCTS.append(dict(id=f"{m['b']}-{m['id']}-{p['id']}", m=m["id"], p=p["id"], url=f"{m['b']}/{m['id']}/{p['id']}/",
                             price=sample_price(mt, pt), sample=1, oem="", stock="", status="published", note=PNOTE.get(p["id"], "")))

# staff changes exported from the dashboard (Import/Export > JSON) are applied here at build time
cj = HERE / "catalogue.json"
if cj.exists():
    ch = json.loads(cj.read_text())
    by = {x["id"]: x for x in PRODUCTS}
    for pid, d in (ch.get("products") or {}).items():
        if pid in by: by[pid].update({k: v for k, v in d.items() if k in ("price", "sample", "oem", "stock", "status", "note")})
PRODUCTS = [x for x in PRODUCTS if x["status"] == "published"]
for x in PRODUCTS:
    x["model"] = M[x["m"]]; x["part"] = P[x["p"]]; x["cat"] = C[x["part"]["cat"]]
    x["title"] = f"{x['part']['name']} for {mlabel(x['model'])}"


def show_price(x):
    return x["price"] is not None and not (LIVE and x["sample"])


def money(v):
    return f"S${v:,.0f}" if float(v).is_integer() else f"S${v:,.2f}"


def price_html(x, big=False):
    if not show_price(x):
        return f'<span class="price ask" data-price="{x["id"]}">Ask for price</span>'
    b = '<span class="badge sample" title="Demo price for the preview, not Partware Auto\'s real price">Sample price</span>' if x["sample"] else ""
    return f'<span class="price{" big" if big else ""}" data-price="{x["id"]}">{money(x["price"])}</span>{b}'


STOCK = {"in": ("In stock", "ok"), "order": ("Order in", "warn"), "out": ("Out of stock", "out")}

# ---------------- icons ----------------
SV = lambda body, vb="0 0 48 48": f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'
ICON = {
 "service": SV('<rect x="14" y="14" width="20" height="26" rx="3"/><path d="M18 14v-4h12v4M14 22h20M14 30h20" opacity=".7"/><path d="M24 4v6"/>'),
 "engine": SV('<path d="M8 18h6v-4h12v4h6l4 4h4v12h-4l-4 4H14l-6-6Z"/><path d="M4 22v8M17 10h6"/><circle cx="24" cy="27" r="4" opacity=".6"/>'),
 "body": SV('<path d="M5 30v-6l5-2 6-8h15l8 8 5 2v6h-4"/><path d="M13 30h22"/><circle cx="12" cy="31" r="4"/><circle cx="36" cy="31" r="4"/><path d="M17 22h20M24 14v8"/>'),
 "under": SV('<circle cx="24" cy="24" r="17"/><circle cx="24" cy="24" r="6"/><circle cx="24" cy="24" r="12" opacity=".5"/><path d="M24 15v2M31 20l-2 1M31 28l-2-1M17 20l2 1M17 28l2-1M24 31v2"/>'),
 "interior": SV('<path d="M12 40V18c0-5 3-8 8-8h8c5 0 8 3 8 8v22"/><path d="M12 28h24M16 40v-6M32 40v-6"/><circle cx="24" cy="20" r="2.5"/>'),
 "cart": SV('<path d="M3 5h4l3 18h17l3-12H9"/><circle cx="13" cy="28" r="2"/><circle cx="25" cy="28" r="2"/>', "0 0 34 34"),
 "search": SV('<circle cx="14" cy="14" r="9"/><path d="m21 21 7 7"/>', "0 0 32 32"),
 "phone": SV('<path d="M7 4h6l3 7-4 2a16 16 0 0 0 8 8l2-4 7 3v6a3 3 0 0 1-3 3C14 29 4 19 4 7a3 3 0 0 1 3-3Z"/>', "0 0 34 34"),
 "pin": SV('<path d="M17 31s10-9 10-17a10 10 0 0 0-20 0c0 8 10 17 10 17Z"/><circle cx="17" cy="14" r="3.5"/>', "0 0 34 34"),
 "check": SV('<circle cx="17" cy="17" r="13"/><path d="m11 17 4 4 8-8"/>', "0 0 34 34"),
 "driver": SV('<path d="M5 30v-7l4-9h22l4 9v7"/><path d="M5 23h30"/><circle cx="12" cy="31" r="3.5"/><circle cx="28" cy="31" r="3.5"/><path d="M12 17h16" opacity=".6"/>', "0 0 40 40"),
 "wrench": SV('<path d="M27 6a8 8 0 0 0-7 11L6 31l3 3 14-14a8 8 0 0 0 11-7l-5 4-4-1-1-4Z"/>', "0 0 40 40"),
 "globe": SV('<circle cx="20" cy="20" r="15"/><path d="M5 20h30M20 5c-6 7-6 23 0 30M20 5c6 7 6 23 0 30"/>', "0 0 40 40"),
}
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3a.4.4 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>'


def wa_link(text):
    return f"https://wa.me/{WA}?text={quote(text)}"


def part_art(x, cls="art"):
    return f'<div class="{cls}" data-cat="{x["cat"]["id"]}">{ICON[x["cat"]["icon"]]}<span>Photo coming</span></div>'


# ---------------- page shell ----------------
NAV = [("parts/", "Parts", "parts"), ("honda/", "Honda models", "honda"), ("workshops/", "Workshops &amp; trade", "workshops"),
       ("export/", "Export", "export"), ("articles/", "Guides", "articles"), ("contact/", "Contact", "contact")]

ORG = {"@type": ["AutoPartsStore", "LocalBusiness"], "@id": BASE + "/#store", "name": BRAND, "legalName": LEGAL,
       "url": BASE + "/", "logo": BASE + "/icon-512.png", "image": BASE + "/og.jpg", "telephone": "+65 " + TEL,
       "foundingDate": "2015", "identifier": {"@type": "PropertyValue", "propertyID": "UEN", "value": UEN},
       "slogan": "Your Honda Parts Specialist", "sameAs": [FB],
       "address": {"@type": "PostalAddress", "streetAddress": f"{ADDR1}, KB Industrial Building", "postalCode": "416175",
                   "addressLocality": "Singapore", "addressCountry": "SG"},
       "openingHoursSpecification": [
           {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "18:00"},
           {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "09:00", "closes": "15:00"}],
       "contactPoint": [{"@type": "ContactPoint", "telephone": "+65 8797 7581", "contactType": "sales",
                         "contactOption": "WhatsApp", "areaServed": "SG", "availableLanguage": ["English"]}],
       "areaServed": "SG", "hasMap": GMAP}

VER = {}
def asset(name):
    if name not in VER:
        VER[name] = hashlib.sha1((HERE / name).read_bytes()).hexdigest()[:8]
    return f"{name}?v={VER[name]}"


SITEMAP = []
def write(path, text):
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text)


def shell(path, title, desc, body, active="", crumbs=None, schema=None, js=("data.js", "pw.js", "wa.js"),
          css=("pw.css",), index=True, prio="0.6", og_type="website"):
    assert len(title) < 60, (len(title), title)
    D(desc)
    depth = path.count("/")
    r = "../" * depth
    url = BASE + "/" + path.replace("index.html", "")
    ld = [dict(ORG)]
    if crumbs:
        ld.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u}
            for i, (n, u) in enumerate([("Home", "")] + crumbs)]})
    if schema: ld.extend(schema)
    ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False).replace("</", "<\\/")
    nav = "".join(f'<a href="{r}{u}"{" aria-current=\"page\"" if k == active else ""}>{n}</a>' for u, n, k in NAV)
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Breadcrumb"><a href="' + r + '">Home</a>' + "".join(
            (f'<span>/</span><a href="{r}{u}">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span>/</span><b>{e(n)}</b>')
            for i, (n, u) in enumerate(crumbs)) + "</nav>"
    body = body.replace("{{CRUMBS}}", cr).replace("{{R}}", r)
    scripts = "".join(f'<script src="{r}{asset(j)}" defer></script>' for j in js)
    styles = "".join(f'<link rel="stylesheet" href="{r}{asset(c)}">' for c in css)
    pv = f'<div class="pv" role="note">Preview for Partware Auto, not live yet. <b>Prices shown are samples.</b> <a href="{r}staff/">Staff dashboard</a></div>' if not LIVE else ""
    doc = f"""<!doctype html>
<html lang="en-SG" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Partware Auto, your Honda parts specialist in Singapore">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{r}favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="{r}icon-192.png"><link rel="apple-touch-icon" href="{r}apple-touch-icon.png"><link rel="manifest" href="{r}site.webmanifest">
<meta name="theme-color" content="#12161C">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Inter:wght@400;500;600;700&display=swap">
{styles}
<script>document.documentElement.classList.remove('no-js');window.PW_ROOT="{r}";</script>
<script type="application/ld+json">{ldj}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{pv}
<header class="hd"><div class="wrap hd-in">
<a class="logo" href="{r}" aria-label="Partware Auto home"><img class="mark" src="{r}mark.png" width="38" height="38" alt=""><span class="wm">PARTWARE AUTO<small>Your Honda parts specialist</small></span></a>
<form class="hd-search" action="{r}search/" role="search"><label class="sr" for="hq">Search parts</label><input id="hq" name="q" type="search" placeholder="e.g. civic brake pads" autocomplete="off">{ICON['search']}</form>
<a class="cartb" href="{r}cart/" aria-label="Cart">{ICON['cart']}<b data-cart-count>0</b></a>
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
</div><nav class="nav" id="nav" aria-label="Main"><div class="wrap">{nav}</div></nav></header>
<main id="main">
{body}
</main>
<footer class="ft"><div class="wrap ft-g">
<div><p class="ft-brand">PARTWARE AUTO</p><p>{e(LEGAL)} · UEN {UEN}<br>Retailer, wholesaler and exporter of Honda parts since 2015.</p></div>
<div><h4>Visit</h4><p>{e(ADDR1)}<br>{e(ADDR2)}<br><a href="{GMAP}" rel="noopener">Directions</a></p></div>
<div><h4>Talk to us</h4><p><a href="tel:{TEL_H}">Call {TEL}</a><br><a href="https://wa.me/{WA}" rel="noopener">WhatsApp {WA_SHOW}</a><br><a href="{FB}" rel="noopener">Facebook</a></p></div>
<div><h4>Explore</h4><p><a href="{r}parts/">Parts</a><br><a href="{r}honda/">Honda models</a><br><a href="{r}workshops/">Workshops &amp; trade</a><br><a href="{r}export/">Export</a><br><a href="{r}articles/">Guides</a><br><a href="{r}about/">About</a><br><a href="{r}privacy/">Privacy</a></p></div>
</div><div class="wrap ft-b">© {datetime.date.today().year} {e(LEGAL)}. Honda is a trademark of Honda Motor Co., Ltd., used here as text to describe the cars our parts are for.</div></footer>
<a class="wa-fab" href="https://wa.me/{WA}?text={quote('Hi Partware Auto, I need a Honda part.')}" aria-label="WhatsApp Partware Auto" rel="noopener">{WA_SVG}</a>
{scripts}
</body>
</html>
"""
    write(path, doc)
    if index:
        SITEMAP.append((url, prio))


def card(x, r, show_model=True):
    t = x["title"] if show_model else x["part"]["name"]
    sub = yrs(x["model"]) if show_model else x["part"]["unit"]
    return (f'<article class="pc" data-pid="{x["id"]}"><a class="pc-a" href="{r}{x["url"]}">{part_art(x)}'
            f'<h3>{e(t)}</h3><p class="pc-sub">{e(sub)}</p></a>'
            f'<div class="pc-f"><div class="pc-p">{price_html(x)}</div>'
            f'<button class="btn add sm" type="button" data-add="{x["id"]}"{" data-side=\"1\"" if x["part"]["side"] else ""}>Add</button></div></article>')


def faq_block(qs):
    h = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in qs)
    sch = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
           "acceptedAnswer": {"@type": "Answer", "text": html.unescape(re.sub("<[^>]+>", "", a))}} for q, a in qs]}
    return h, sch


def finder(r, m=None):
    return f'''<form class="finder" data-finder action="{r}search/">
<div class="f-row"><label><span>1. Your Honda model</span><select name="m" data-f="m" data-sel="{e(m or "")}"><option value="">Choose your Honda model</option></select></label>
<label><span>2. Part</span><select name="p" data-f="p"><option value="">Choose model first</option></select></label>
<button class="btn primary" type="submit">Show part</button></div>
<div class="f-or"><span>or type it</span></div>
<div class="f-q"><input name="q" type="search" placeholder="Try: civic brake pads, vezel headlamp" aria-label="Search parts" autocomplete="off"><button class="btn dark" type="submit">{ICON['search']}<span>Search</span></button></div>
<noscript><p class="small">Search needs JavaScript. Browse by <a href="{r}honda/">Honda model</a> or <a href="{r}parts/">part group</a>.</p></noscript>
</form>'''


def model_tile(m, r):
    n = sum(1 for x in PRODUCTS if x["m"] == m["id"])
    return (f'<a class="mt" href="{r}{m["b"]}/{m["id"]}/"><span class="mt-b">{e(BR[m["b"]])}</span>'
            f'<b>{e(m["name"])} <i>{e(m["code"])}</i></b><span>{e(yrs(m))} · {n} parts</span></a>')


def cat_tile(c, r):
    return f'<a class="ct" href="{r}parts/{c["id"]}/">{ICON[c["icon"]]}<b>{e(c["name"])}</b><span>{e(c["line"])}</span></a>'


def grade_box():
    chips = "".join(f'<span class="badge">{g}</span>' for g in GRADES)
    return (f'<div class="grade-box"><p class="small"><b>Grade options to ask about</b></p><div class="grades">{chips}</div>'
            f'<p class="small muted">Partware Auto offers Genuine, OEM and Aftermarket parts for Honda. Which grade is available for a part, and the price of each, is confirmed on WhatsApp.</p></div>')


# ---------------- home ----------------
def build_home():
    r = ""
    faqs = [
        ("Do you sell Genuine, OEM and Aftermarket Honda parts?", "Partware Auto offers Genuine, OEM and Aftermarket parts for Honda. What is available differs by part, so send us your list and ask which grades we can offer for your car."),
        ("Do I need a part number to order?", "No. Pick your Honda model and the part, or send your car plate or chassis number on WhatsApp. If you do have a part number, include it."),
        ("Do you supply workshops and overseas buyers?", "Yes. Partware Auto is a retailer, wholesaler and exporter of Honda parts. Use the Workshops page for wholesale enquiries and the Export page to send a parts list with your destination country."),
        ("Are the prices on this site final?" if not LIVE else "How do I get a price?",
         "Not yet. This preview shows sample prices only; Partware Auto will put in its own prices and confirm stock on WhatsApp." if not LIVE else "Add parts to your cart and send it on WhatsApp, or ask about one part. We reply with stock, grade options and price."),
    ]
    fh, fs = faq_block(faqs)
    cats = "".join(cat_tile(C[c[0]], r) for c in CATS)
    tiles = "".join(model_tile(M[m[0]], r) for m in MODELS)
    pop_ids = ["honda-civic-fc-front-brake-pads", "honda-vezel-ru-headlamp", "honda-jazz-gk-spark-plugs", "honda-crv-rw-front-shock-absorber"]
    pop = "".join(card(x, r) for x in PRODUCTS if x["id"] in pop_ids)
    body = f'''
<section class="hero"><div class="wrap hero-in">
<div class="hero-t reveal"><p class="eyebrow">Kaki Bukit, Singapore · Since 2015</p>
<h1>Your Honda Parts Specialist</h1>
<p class="lead">Retail, wholesale and export of Honda parts. Pick your model and part, or type what you need, then send your list on WhatsApp.</p></div>
<div class="hero-f reveal">{finder(r)}</div>
</div>
<div class="wrap"><ul class="strip"><li>{ICON['check']}Genuine, OEM and Aftermarket grades to ask about</li><li>{ICON['check']}Retail, wholesale and export</li><li>{ICON['check']}Stock, grade and price confirmed on WhatsApp</li></ul></div></section>

<section class="sec"><div class="wrap">
<div class="sec-h"><h2>Who we help</h2><p>Three ways to buy Honda parts from Partware Auto.</p></div>
<div class="aud">
<a class="reveal" href="parts/">{ICON['driver']}<b>Drivers</b><span>Find the part for your Honda by model, then send it to us on WhatsApp for stock and price.</span><em>Find a part</em></a>
<a class="reveal" href="workshops/">{ICON['wrench']}<b>Workshops &amp; trade</b><span>Wholesale supply for workshops. Tell us the Honda models you service and the parts you buy often.</span><em>Ask about wholesale</em></a>
<a class="reveal" href="export/">{ICON['globe']}<b>Overseas export</b><span>Buying Honda parts for another country? Paste your parts list and tell us the destination.</span><em>Send an export list</em></a>
</div></div></section>

<section class="sec alt"><div class="wrap">
<div class="sec-h"><h2>Five product groups</h2><p>The same groups as our Facebook page. Each lists parts for every Honda model we cover.</p></div>
<div class="cgrid">{cats}</div>
</div></section>

<section class="sec"><div class="wrap">
<div class="sec-h"><h2>Shop by Honda model</h2><p>Choose your model and generation code. Every part for it is on one page.</p></div>
<div class="mgrid">{tiles}</div>
</div></section>

<section class="sec alt"><div class="wrap">
<div class="sec-h"><h2>Popular searches</h2><p>Examples of what drivers look for. <a href="parts/">Browse all parts</a>.</p></div>
<div class="pgrid">{pop}</div>
</div></section>

<section class="sec"><div class="wrap two">
<div class="reveal"><h2>Why Partware Auto</h2>
<p>Partware Auto Pte. Ltd. was established in 2015 as a retailer, wholesaler and exporter of automobile parts for the Honda make. We offer Genuine, OEM and Aftermarket grades, so you can ask which one suits your car and budget.</p>
<p>Our shop is at {e(ADDR1)}, {e(ADDR2)}. <a href="about/">About us</a></p></div>
<div class="proofbar reveal"><div><b>2015</b><span>Established</span></div><div><b>{UEN}</b><span>UEN, registered in Singapore</span></div><div><b>Kaki Bukit</b><span>Singapore 416175</span></div></div>
</div></section>

<section class="sec alt"><div class="wrap narrow">
<h2>Questions</h2>{fh}
</div></section>
<section class="cta"><div class="wrap"><h2>Not sure which part you need?</h2><p>Send your car plate or chassis number and what you need. We reply with the part, grade options and price.</p>
<a class="btn wa" href="{wa_link("Hi Partware Auto, I need a Honda part. My car plate / chassis number is: ")}" rel="noopener">{WA_SVG}WhatsApp {WA_SHOW}</a></div></section>
'''
    shell("index.html", "Honda Parts Singapore | Partware Auto",
          "Honda parts specialist in Kaki Bukit, Singapore. Retail, wholesale and export. Find parts by model, then send your list on WhatsApp.",
          body, active="", schema=[fs, {"@type": "WebSite", "@id": BASE + "/#web", "url": BASE + "/", "name": BRAND,
          "potentialAction": {"@type": "SearchAction", "target": BASE + "/search/?q={q}", "query-input": "required name=q"}}], prio="1.0")


# ---------------- honda + model pages ----------------
def build_brands():
    path = "honda/index.html"; r = "../"
    tiles = "".join(model_tile(M[m[0]], r) for m in MODELS)
    n = len(PRODUCTS)
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}
<h1>Honda parts in Singapore by model</h1>
<p class="lead">{n} listings across {len(MODELS)} Honda models and generations, from servicing parts to body, undercarriage and interior parts. Choose your model and generation code.</p>
<div class="hero-f slim">{finder(r)}</div></div></section>
<section class="sec"><div class="wrap"><h2>Honda models</h2><div class="mgrid">{tiles}</div>
<p class="small">Your model is not here? <a href="{wa_link("Hi Partware Auto, do you have parts for my Honda? Model and year: ")}" rel="noopener">Ask us on WhatsApp</a>.</p></div></section>'''
    shell(path, "Honda Parts by Model | Partware Auto", D("Honda parts for the Civic, Jazz, City, Vezel, CR-V, Odyssey, Shuttle, Freed, Stepwgn, Accord, Insight and Stream. Find yours by model."),
          body, active="honda", crumbs=[("Honda models", "honda/")], prio="0.9")


def build_models():
    for mt in MODELS:
        m = M[mt[0]]; bn = BR[m["b"]]
        path = f"{m['b']}/{m['id']}/index.html"; r = "../../"
        items = [x for x in PRODUCTS if x["m"] == m["id"]]
        secs, jump = [], []
        for c in CATS:
            xs = [x for x in items if x["cat"]["id"] == c[0]]
            if not xs: continue
            jump.append(f'<a class="chip" href="#{c[0]}">{e(c[1])}</a>')
            secs.append(f'<section class="msec" id="{c[0]}"><h2>{ICON[c[3]]}{e(c[1])}</h2><div class="pgrid">{"".join(card(x, r, show_model=False) for x in xs)}</div>'
                        f'<p class="small"><a href="{r}parts/{c[0]}/">{e(c[1])} for other Honda models</a></p></section>')
        sibs = "".join(model_tile(M[o[0]], r) for o in MODELS if o[0] != m["id"] and o[2].split()[0] == m["name"].split()[0])
        others = "".join(f'<a class="chip" href="{r}{o[1]}/{o[0]}/">{e(o[2])} {e(o[3])}</a>' for o in MODELS if o[0] != m["id"])
        hy = " This model is a hybrid. Hybrid battery and drive-system parts are not listed here; ask us." if m["fuel"] == "hybrid" else ""
        body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}
<h1>{e(bn)} {e(m["name"])} ({e(m["code"])}) parts</h1>
<p class="lead">Parts for the {e(bn)} {e(m["name"])}, {e(m["code"])} generation, {e(yrs(m))} ({e(m["fuel"])}).{e(hy)} Add what you need and send the list on WhatsApp.</p>
<p class="fitnote">{ICON['check']}<span>Not sure if your car is the {e(m["code"])}? Send your car plate or chassis number and we will check before you order.</span></p>
<div class="chips jump">{"".join(jump)}</div></div></section>
<div class="wrap msecs">{"".join(secs)}</div>
<section class="sec"><div class="wrap">{grade_box()}</div></section>
{f'<section class="sec alt"><div class="wrap"><h2>Other {e(m["name"].split()[0])} generations</h2><div class="mgrid">{sibs}</div></div></section>' if sibs else ""}
<section class="sec"><div class="wrap"><h2>Other Honda models</h2><div class="chips">{others}</div></div></section>'''
        sch = {"@type": "ItemList", "name": f"{bn} {m['name']} ({m['code']}) parts", "numberOfItems": len(items),
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + "/" + x["url"], "name": x["title"]} for i, x in enumerate(items)]}
        title = T(f"{bn} {m['name']} {m['code']} Parts Singapore{SUFFIX}", f"{bn} {m['name']} {m['code']} Parts{SUFFIX}")
        shell(path, title, D(f"{bn} {m['name']} ({m['code']}, {m['years'].replace('-now', '+')}) parts in Singapore: servicing, engine, body, undercarriage and interior parts. Order on WhatsApp."),
              body, active="honda", crumbs=[("Honda models", "honda/"), (f"{m['name']} ({m['code']})", f"{m['b']}/{m['id']}/")], schema=[sch], prio="0.8")


# ---------------- product pages ----------------
def build_products():
    for x in PRODUCTS:
        m, p, c = x["model"], x["part"], x["cat"]; bn = BR[m["b"]]
        r = "../../../"; path = x["url"] + "index.html"
        same_car = [y for y in PRODUCTS if y["m"] == m["id"] and y["id"] != x["id"]]
        same_cat = [y for y in same_car if y["cat"]["id"] == c["id"]]
        rest = [y for y in same_car if y["cat"]["id"] != c["id"]]
        related = (same_cat + rest)[:8]
        other_models = [y for y in PRODUCTS if y["p"] == p["id"] and y["m"] != m["id"]]
        om = "".join(f'<a class="chip" href="{r}{y["url"]}">{e(y["model"]["name"])} {e(y["model"]["code"])}</a>' for y in other_models)
        stock = STOCK.get(x["stock"])
        stock_h = f'<span class="stock {stock[1]}">{stock[0]}</span>' if stock else '<span class="stock">Stock confirmed on WhatsApp</span>'
        oem = f'<div><dt>Part number</dt><dd class="mono">{e(x["oem"])}</dd></div>' if x["oem"] else '<div><dt>Part number</dt><dd>We match it to your car plate or chassis number</dd></div>'
        side = ('<fieldset class="side"><legend>Side</legend><label><input type="radio" name="side" value="Left" required> Left (passenger)</label>'
                '<label><input type="radio" name="side" value="Right"> Right (driver)</label></fieldset>') if p["side"] else ""
        msg = f"Hi Partware Auto, I'm asking about: {x['title']} {m['years']}. Which grades (Genuine / OEM / Aftermarket) can you offer, and the price of each? My car plate / chassis number is: "
        note = f'<p class="note">{e(x["note"])}</p>' if x["note"] else ""
        sample_note = '<p class="small muted">Preview: this is a sample price for the demo. Partware Auto will put in its own price.</p>' if x["sample"] and show_price(x) else ""
        desc_t = f"{p['name']} for the {bn} {m['name']} ({m['code']}, {m['years'].replace('-now', ' onwards')})"
        body = f'''<div class="wrap">{{{{CRUMBS}}}}</div>
<section class="prod wrap" data-product="{x["id"]}">
<div class="prod-art">{part_art(x, "art big")}<div class="thumbs"></div></div>
<div class="prod-i">
<p class="eyebrow"><a href="{r}parts/{c["id"]}/">{e(c["name"])}</a> · <a href="{r}{m["b"]}/{m["id"]}/">{e(bn)} {e(m["name"])} {e(m["code"])}</a></p>
<h1>{e(p["name"])} for {e(bn)} {e(m["name"])} ({e(m["code"])})</h1>
<p class="fits">Fits {e(bn)} {e(m["name"])} {e(m["code"])}, {e(yrs(m))}</p>
<div class="buy">
<div class="buy-p">{price_html(x, big=True)}<span class="unit">per {e(p["unit"])}</span></div>
{stock_h}
<form class="buy-f" data-buy="{x["id"]}">{side}
<div class="qty"><label for="q-{x["id"]}">Qty</label><button type="button" data-q="-1" aria-label="Less">−</button><input id="q-{x["id"]}" name="qty" type="number" min="1" max="20" value="1" inputmode="numeric"><button type="button" data-q="1" aria-label="More">+</button></div>
<button class="btn primary big" type="submit">{ICON['cart']}Add to cart</button>
</form>
<a class="btn wa ghost" href="{wa_link(msg)}" rel="noopener">{WA_SVG}Ask about this part</a>
{sample_note}
</div>
{grade_box()}
{note}
<dl class="spec">
<div><dt>Car</dt><dd>{e(bn)} {e(m["name"])}</dd></div>
<div><dt>Generation</dt><dd>{e(m["code"])}, {e(yrs(m))}</dd></div>
<div><dt>Engine type</dt><dd>{e(m["fuel"])}</dd></div>
<div><dt>Sold as</dt><dd>{e(p["unit"])}{" (left or right)" if p["side"] else ""}</dd></div>
{oem}
<div><dt>Visit</dt><dd>Kaki Bukit (KB Industrial Building)</dd></div>
</dl>
<p class="fitnote">{ICON['check']}<span>Facelift and engine versions can differ. Send your car plate or chassis number with your order so we can confirm this part fits your exact car.</span></p>
</div></section>
<section class="sec"><div class="wrap"><h2>More parts for your {e(m["name"])} {e(m["code"])}</h2><div class="pgrid">{"".join(card(y, r, show_model=False) for y in related)}</div>
<p><a class="btn ghost" href="{r}{m["b"]}/{m["id"]}/">All {e(bn)} {e(m["name"])} {e(m["code"])} parts</a></p></div></section>
<section class="sec alt"><div class="wrap"><h2>{e(p["name"])} for other models</h2><div class="chips">{om}</div>
<p class="small"><a href="{r}parts/{c["id"]}/">All {e(c["name"].lower())}</a></p></div></section>'''
        prod = {"@type": "Product", "@id": BASE + "/" + x["url"] + "#product", "name": f"{p['name']} for {bn} {m['name']} ({m['code']})",
                "sku": x["id"], "category": c["name"], "image": BASE + "/og.jpg",
                "description": desc_t + ". Sold by Partware Auto, a Honda parts specialist in Singapore. Genuine, OEM and Aftermarket grades are available to ask about.",
                "isAccessoryOrSparePartFor": {"@type": "Car", "name": f"{bn} {m['name']} {m['code']}", "brand": {"@type": "Brand", "name": bn}}}
        if x["oem"]: prod["mpn"] = x["oem"]
        if show_price(x):
            off = {"@type": "Offer", "url": BASE + "/" + x["url"], "priceCurrency": "SGD", "price": f'{x["price"]:.2f}',
                   "seller": {"@id": BASE + "/#store"}, "areaServed": "SG"}
            if stock: off["availability"] = {"in": "https://schema.org/InStock", "order": "https://schema.org/PreOrder", "out": "https://schema.org/OutOfStock"}[x["stock"]]
            prod["offers"] = off
        short = m["name"].split(" / ")[0]
        title = T(f"{p['name']} {bn} {m['name']} {m['code']}{SUFFIX}", f"{p['name']} {bn} {short} {m['code']}{SUFFIX}", f"{p['name']} {bn} {short} {m['code']}")
        shell(path, title, D(next(s for s in (f"{desc_t}. Honda parts specialist in Kaki Bukit. Ask about Genuine, OEM and Aftermarket grades.", f"{desc_t}. Ask Partware Auto about Genuine, OEM and Aftermarket grades.") if len(s) < 160)),
              body, active="honda", crumbs=[("Honda models", "honda/"), (f"{m['name']} ({m['code']})", f"{m['b']}/{m['id']}/"), (p["name"], x["url"])],
              schema=[prod], prio="0.7", og_type="product")


# ---------------- catalogue + group pages ----------------
def build_cats():
    tiles = "".join(cat_tile(C[c[0]], "../") for c in CATS)
    mt = "".join(model_tile(M[m[0]], "../") for m in MODELS)
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Honda parts catalogue</h1>
<p class="lead">Search by Honda model and part, or open one of our five product groups. Each lists the part for every Honda model we cover.</p>
<div class="hero-f slim">{finder("../")}</div></div></section>
<section class="sec"><div class="wrap"><h2>Product groups</h2><div class="cgrid">{tiles}</div></div></section>
<section class="sec alt"><div class="wrap"><h2>Or start from your model</h2><div class="mgrid">{mt}</div></div></section>'''
    shell("parts/index.html", "Honda Parts Catalogue | Partware Auto", D("Search Honda parts by model and part: servicing essentials, engine, body, undercarriage and interior parts. Order on WhatsApp."),
          body, active="parts", crumbs=[("Parts", "parts/")], prio="0.9")
    order = [p[2] for p in PARTS]
    for ct in CATS:
        c = C[ct[0]]; r = "../../"
        xs = [x for x in PRODUCTS if x["cat"]["id"] == c["id"]]
        pnames = sorted({x["part"]["name"] for x in xs}, key=order.index)
        blocks = []
        for pname in pnames:
            sub = [x for x in xs if x["part"]["name"] == pname]
            rows = "".join(f'<tr><td><a href="{r}{x["url"]}">{e(x["model"]["name"])} <i>{e(x["model"]["code"])}</i></a><small>{e(yrs(x["model"]))}</small></td>'
                           f'<td class="r">{price_html(x)}</td><td class="r"><button class="btn add sm" type="button" data-add="{x["id"]}"{" data-side=\"1\"" if x["part"]["side"] else ""}>Add</button></td></tr>'
                           for x in sub)
            blocks.append(f'<details class="pl" id="{sub[0]["p"]}"><summary><b>{e(pname)}</b> <span>{len(sub)} Honda models</span></summary><div class="tbl"><table><thead><tr><th>Model</th><th class="r">Price</th><th></th></tr></thead><tbody>{rows}</tbody></table></div></details>')
        others = "".join(f'<a class="chip" href="{r}parts/{o[0]}/">{e(o[1])}</a>' for o in CATS if o[0] != c["id"])
        body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Honda {e(c["name"].lower())}</h1>
<p class="lead">{e(c["line"])} for {len({x["m"] for x in xs})} Honda models and generations. Open a part to see every model, or add straight to your cart.</p></div></section>
<section class="sec"><div class="wrap narrow">{"".join(blocks)}{grade_box()}</div></section>
<section class="sec alt"><div class="wrap"><h2>Other product groups</h2><div class="chips">{others}</div></div></section>'''
        sch = {"@type": "ItemList", "name": f"Honda {c['name']}", "numberOfItems": len(pnames),
               "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n} for i, n in enumerate(pnames)]}
        shell(f"parts/{c['id']}/index.html", T(f"Honda {c['name']} Singapore{SUFFIX}", f"Honda {c['name']}{SUFFIX}"),
              D(f"Honda {c['name'].lower()} in Singapore: {c['line'].lower()}. Find your model, then order on WhatsApp."),
              body, active="parts", crumbs=[("Parts", "parts/"), (c["name"], f"parts/{c['id']}/")], schema=[sch], prio="0.8")


# ---------------- workshops, export ----------------
def parts_box(label="Parts list"):
    return f'''<fieldset><legend>{label}</legend>
<label>Paste one part per line<small>Part number or description, then quantity. Example: Civic FC front brake pads, 4</small>
<textarea name="parts" rows="6" placeholder="Civic FC front brake pads, 4&#10;Vezel RU headlamp left, 2&#10;Jazz GK cabin filter x 10"></textarea></label>
<label>Or upload a .csv or .txt file<small>Read in your browser only. It is not uploaded anywhere.</small><input type="file" accept=".csv,.txt,text/csv,text/plain" aria-label="Upload a parts list file"></label>
<div class="btns"><button class="btn dark" type="button" data-parts-go>Check list</button><button class="btn ghost" type="button" data-parts-ex>Fill an example</button></div>
<div data-parts-out aria-live="polite"></div></fieldset>'''


def build_trade():
    qs = [("Do you offer trade or wholesale pricing?", "Partware Auto describes itself as a retailer, wholesaler and exporter of Honda parts. Trade prices and terms are not published on this site, so ask in your enquiry and we will reply on WhatsApp."),
          ("Which parts can a workshop order?", "Servicing essentials, engine parts, body parts, undercarriage parts and interior parts for Honda. Genuine, OEM and Aftermarket grades are available to ask about."),
          ("Can I send a long list?", "Yes. Paste it or upload a .csv or .txt file. Lines we can match to our catalogue are listed; the rest go into your message for our team to check.")]
    fh, fs = faq_block(qs)
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Honda parts for workshops and trade</h1>
<p class="lead">Wholesale supply of Honda parts from Kaki Bukit. Tell us what your workshop services and what you buy often, and send your parts list.</p></div></section>
<section class="sec"><div class="wrap cart-g">
<div><h2>How a trade enquiry works</h2>
<ol class="howto"><li><h3>Send your details and list</h3><p>Fill in the form. A parts list is optional but helps us reply faster.</p></li>
<li><h3>We check stock and grades</h3><p>We confirm what we can supply in Genuine, OEM or Aftermarket grade and the price for each.</p></li>
<li><h3>Agree supply terms</h3><p>Trade terms are agreed with you directly on WhatsApp. None are published here.</p></li></ol>
<h2>Questions</h2>{fh}</div>
<form class="frm" data-lead="TRADE" id="trade-form"><h2>Workshop or trade enquiry</h2>
<div class="row2"><label>Business name<input name="company" autocomplete="organization" required></label>
<label>Your name<input name="name" autocomplete="name" required></label></div>
<div class="row2"><label>WhatsApp or phone<input name="contact" type="tel" autocomplete="tel" inputmode="tel" required></label>
<label>Business type<select name="business"><option>Workshop</option><option>Parts trader</option><option>Fleet or company</option><option>Other</option></select></label></div>
<label>Honda models you service<small>For example Civic FC, Vezel RU, Freed GB5</small><input name="vehicle"></label>
{parts_box()}
<label>Notes<textarea name="note" rows="3" placeholder="Grade you prefer, how often you order"></textarea></label>
<button class="btn wa big" type="submit">{WA_SVG}Send on WhatsApp</button>
<div data-lead-done hidden aria-live="polite"></div>
<p class="small muted">Tapping send saves the enquiry in this browser and opens WhatsApp with a summary to {WA_SHOW}. Nothing is sent until you tap send in WhatsApp.</p>
</form></div></section>'''
    shell("workshops/index.html", "Honda Parts for Workshops & Trade | Partware Auto", D("Wholesale Honda parts for Singapore workshops and trade buyers. Send your parts list and models serviced; we reply on WhatsApp."),
          body, active="workshops", crumbs=[("Workshops & trade", "workshops/")], schema=[fs], prio="0.8")


def build_export():
    qs = [("What should I send for an export quote?", "Your destination country, the Honda model and chassis number (VIN) for each car, and your parts list with quantities. A photo of the old part helps. Our guide on parts lists explains the details."),
          ("Which countries do you export to?", "We have not published a country list. Tell us your destination in the enquiry and we will reply on WhatsApp."),
          ("What are your shipping and payment terms?", "Shipping and payment terms are not published on this site. They are discussed per enquiry, so ask when you send your list.")]
    fh, fs = faq_block(qs)
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Export Honda parts from Singapore</h1>
<p class="lead">Partware Auto is an exporter of Honda parts. Paste your parts list, tell us the destination country, and we reply on WhatsApp.</p></div></section>
<section class="sec"><div class="wrap cart-g">
<div><h2>How an export enquiry works</h2>
<ol class="howto"><li><h3>Paste or upload your list</h3><p>One line per part: part number or description, then quantity. We match what we can to our catalogue.</p></li>
<li><h3>Add destination and contact</h3><p>Tell us the country and how to reach you. Add chassis numbers (VIN) if you have them.</p></li>
<li><h3>Send it on WhatsApp</h3><p>The form opens WhatsApp with a ready summary. We reply with stock, grade options and a quote.</p></li></ol>
<p>New to this? Read <a href="../articles/parts-list-chassis-vin-export-quote/">how to give a parts list with chassis or VIN for an export quote</a>.</p>
<h2>Questions</h2>{fh}</div>
<form class="frm" data-lead="EXPORT" id="export-form"><h2>Export enquiry</h2>
<div class="row2"><label>Your name<input name="name" autocomplete="name" required></label>
<label>Company<input name="company" autocomplete="organization"></label></div>
<div class="row2"><label>Destination country<input name="country" autocomplete="country-name" required></label>
<label>WhatsApp or phone<input name="contact" type="tel" autocomplete="tel" inputmode="tel" required></label></div>
<label>Email (optional)<input name="email" type="email" autocomplete="email"></label>
<label>Vehicle and chassis number (VIN)<small>For example Honda Vezel RU, chassis RU1-1234567</small><input name="vehicle"></label>
{parts_box()}
<label>Notes<textarea name="note" rows="3" placeholder="Grade you prefer, shipping questions"></textarea></label>
<button class="btn wa big" type="submit">{WA_SVG}Send on WhatsApp</button>
<div data-lead-done hidden aria-live="polite"></div>
<p class="small muted">Tapping send saves the enquiry in this browser and opens WhatsApp with a summary to {WA_SHOW}. Nothing is sent until you tap send in WhatsApp.</p>
</form></div></section>'''
    shell("export/index.html", "Export Honda Parts from Singapore | Partware Auto", D("Overseas buyers: send your Honda parts list and destination to Partware Auto in Singapore. Paste or upload a list; we reply on WhatsApp."),
          body, active="export", crumbs=[("Export", "export/")], schema=[fs], prio="0.8")


# ---------------- simple pages ----------------
def build_pages():
    # search
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1 data-sr-title>Search Honda parts</h1>
<div class="hero-f slim">{finder("../")}</div></div></section>
<section class="sec"><div class="wrap"><div data-results aria-live="polite"><p class="muted">Type your Honda and the part, for example “civic brake pads” or “vezel headlamp”.</p></div></div></section>'''
    shell("search/index.html", "Search Honda Parts | Partware Auto", "Search Honda parts by model and part name.", body, crumbs=[("Search", "search/")], index=False)
    # cart
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Your cart</h1></div></section>
<section class="sec"><div class="wrap cart-g">
<div data-cart><p class="muted">Loading your cart…</p></div>
<form class="co" data-checkout>
<h2>Send your order</h2>
<p class="small">Your cart opens in WhatsApp as a message to Partware Auto ({WA_SHOW}). Nothing is paid here. We reply to confirm stock, grade, price and collection.</p>
<label>Your name<input name="name" autocomplete="name" required></label>
<label>Car plate or chassis number<input name="car" placeholder="e.g. SMA1234X" autocapitalize="characters"><small>Helps us check the exact part for your car.</small></label>
<label>Grade to ask about<select name="grade"><option value="">Not sure, please advise</option><option>Genuine</option><option>OEM</option><option>Aftermarket</option></select></label>
<label>Collection<select name="collect"><option>Self-collect at Kaki Bukit</option><option>Please tell me about delivery</option></select></label>
<label>Notes<textarea name="note" rows="3" placeholder="Anything else we should know"></textarea></label>
<button class="btn wa big" type="submit">{WA_SVG}Send order on WhatsApp</button>
<p class="small muted" data-co-msg></p>
</form>
</div></section>'''
    shell("cart/index.html", "Your Cart | Partware Auto", "Your Partware Auto parts cart.", body, crumbs=[("Cart", "cart/")], index=False)
    # about: every fact from FACTS.md with its source
    unit_note = f'<p class="small muted">Preview note: the shop unit shows {UNIT} (Yellow Pages and the Facebook listing). ACRA lists the registered address as #01-24. Partware Auto to confirm.</p>' if not LIVE else ""
    rows = [("Registered name", LEGAL, "ACRA via recordowl.com"), ("UEN", f'<span class="mono">{UEN}</span>', "ACRA via recordowl.com, Yellow Pages"),
            ("Incorporated", f"{INC} (the Facebook page says established in 2015)", "ACRA via recordowl.com; Facebook"),
            ("Business activities", "Wholesale of motor vehicle parts (SSIC 46563, primary) and retail of motor vehicle parts (SSIC 47314)", "ACRA"),
            ("Address", f"{e(ADDR1)}, {e(ADDR2)}", "Yellow Pages and Facebook listing (unit); ACRA (building)"),
            ("Phone", f'<a href="tel:{TEL_H}">{TEL}</a>', "Yellow Pages"),
            ("WhatsApp", f'<a href="https://wa.me/{WA}" rel="noopener">{WA_SHOW}</a>', "Yellow Pages WhatsApp link (to be confirmed)"),
            ("Services", "Retail, wholesale and export", "Facebook page"),
            ("Product groups", "Servicing Essentials, Engine Parts, Body Parts, Undercarriage Parts, Interior Parts", "Facebook page"),
            ("Parts grades", "Genuine, OEM and Aftermarket parts for the Honda make", "Facebook page"),
            ("Opening hours", "Mon to Fri 9am to 6pm, Sat 9am to 3pm, Sunday and public holidays closed (to be confirmed)", "Facebook page, via autoyas.com"),
            ("Category", "Automotive parts store", "Facebook page"),
            ("Facebook", f'<a href="{FB}" rel="noopener">facebook.com/partwareauto</a>', "Facebook")]
    trs = "".join(f"<tr><th scope='row'>{k}</th><td>{v}</td><td class='src'>{s}</td></tr>" for k, v, s in rows)
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>About Partware Auto</h1>
<p class="lead">Partware Auto Pte. Ltd. was established in 2015 as a retailer, wholesaler and exporter of automobile parts for the Honda make. Our tagline is “Your Honda Parts Specialist”.</p></div></section>
<section class="sec"><div class="wrap narrow">
<h2>What we do</h2><p>We offer Genuine, OEM and Aftermarket parts across five product groups: Servicing Essentials, Engine Parts, Body Parts, Undercarriage Parts and Interior Parts. We serve drivers at retail, workshops through wholesale, and overseas buyers through export.</p>
<h2>Business details and sources</h2>
<div class="tbl"><table class="facts-t"><thead><tr><th>Item</th><th>Detail</th><th>Source</th></tr></thead><tbody>{trs}</tbody></table></div>
{unit_note}
<p>Questions? <a href="../contact/">Contact us</a> or see <a href="../workshops/">workshops and trade</a> and <a href="../export/">export</a>.</p>
</div></section>'''
    org = {"@type": "AboutPage", "url": BASE + "/about/", "name": "About Partware Auto", "about": {"@id": BASE + "/#store"}}
    shell("about/index.html", "About Partware Auto, Honda Parts Singapore", D(f"Partware Auto Pte. Ltd. (UEN {UEN}), established 2015: retailer, wholesaler and exporter of Honda parts in Kaki Bukit, Singapore."),
          body, crumbs=[("About", "about/")], schema=[org], prio="0.6")
    # contact
    hrs = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in HOURS)
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Contact Partware Auto</h1>
<p class="lead">WhatsApp is the fastest way. Send your car plate or chassis number and the part you need.</p></div></section>
<section class="sec"><div class="wrap cgrid3">
<a class="cc" href="{wa_link("Hi Partware Auto, I need a Honda part. Car plate / chassis: ")}" rel="noopener">{WA_SVG}<b>WhatsApp</b><span>{WA_SHOW}</span></a>
<a class="cc" href="tel:{TEL_H}">{ICON['phone']}<b>Call</b><span>{TEL}</span></a>
<a class="cc" href="{GMAP}" rel="noopener">{ICON['pin']}<b>Visit</b><span>{e(ADDR1)}<br>{e(ADDR2)}</span></a>
</div><div class="wrap"><h2>Opening hours</h2><div class="tbl" style="max-width:520px"><table class="hours"><tbody>{hrs}</tbody></table></div>
<p class="small muted">These hours come from the Partware Auto Facebook page and are being confirmed with the shop. Please WhatsApp before you visit so we can check stock.</p>
<p><a href="{FB}" rel="noopener">Partware Auto on Facebook</a></p></div></section>'''
    shell("contact/index.html", "Contact Partware Auto | Honda Parts Kaki Bukit", D(f"WhatsApp {WA_SHOW} or call {TEL}. Partware Auto, 10 Kaki Bukit Road 1, KB Industrial Building, Singapore 416175."),
          body, active="contact", crumbs=[("Contact", "contact/")], prio="0.6")
    # privacy
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Privacy</h1><p class="lead">What this website stores and what it sends.</p></div></section>
<section class="sec"><div class="wrap narrow art-b">
<h2>Stored in your browser</h2><p>Your cart and any export or workshop enquiry you create are saved in your own browser (local storage) on your device. This website has no server database in this preview, so nothing you type in the forms is sent to us until you tap send in WhatsApp.</p>
<h2>Sent through WhatsApp</h2><p>When you tap a WhatsApp button, WhatsApp opens with a message that you can read and edit. What you send is then handled by WhatsApp and by Partware Auto, which replies to you.</p>
<h2>Button taps</h2><p>We count taps on WhatsApp buttons to see which pages help customers. The count records the page, where the visit came from, the button text, screen size, time zone, language and time on site, with random visit ids. It does not record your IP address and does not use advertising identifiers.</p>
<h2>Fonts</h2><p>Page fonts load from Google Fonts, which receives your browser's standard request.</p>
<h2>Questions</h2><p>Contact {e(LEGAL)} on WhatsApp {WA_SHOW} or call {TEL}.</p>
</div></section>'''
    shell("privacy/index.html", "Privacy | Partware Auto", "What the Partware Auto website stores in your browser, what WhatsApp enquiries send, and how button taps are counted.", body, crumbs=[("Privacy", "privacy/")], prio="0.3")
    # staff
    body = '<div id="staff-app" class="wrap"><h1 class="sr">Staff dashboard</h1><p class="muted">Loading the staff dashboard…</p><noscript>The staff dashboard needs JavaScript.</noscript></div>'
    shell("staff/index.html", "Staff Dashboard | Partware Auto", "Partware Auto staff dashboard (demo): products, enquiries and export.", body, js=("data.js", "staff.js"),
          css=("pw.css", "staff.css"), index=False)
    # 404
    body = f'''<section class="ph"><div class="wrap"><h1>Page not found</h1><p class="lead">That page has moved or never existed. Search for your part instead.</p>
<div class="hero-f slim">{finder("{{R}}")}</div></div></section>'''
    shell("404.html", "Page not found | Partware Auto", "Page not found.", body, index=False)


# ---------------- articles (DRAFTS for client review; general knowledge only, no figures) ----------------
ARTS = [
 ("genuine-oem-aftermarket-honda-parts", "Genuine vs OEM vs aftermarket Honda parts: what to ask",
  "What the three grades usually mean, how they differ and the questions to ask a parts seller before you buy.",
  [("What do the three grades mean?", "<ul><li><b>Genuine</b> parts come in the carmaker's own branding and are supplied through its parts channel.</li><li><b>OEM</b> parts are made by a manufacturer that supplies the carmaker, but are sold under the manufacturer's own brand.</li><li><b>Aftermarket</b> parts are made by other companies to fit the car. Quality, materials and price vary a lot between brands.</li></ul>"),
   ("How do you choose between them?", "Think about the part and the car. A part that affects braking or steering deserves the most care, whatever the grade. On an older car you plan to keep only a short time, a lower-cost grade may make sense for parts that do not affect safety. For a newer car, many owners prefer Genuine or OEM. Your workshop's advice is worth asking for."),
   ("What should you ask the seller?", "<ol><li>Which grades can you supply for my exact car (send your chassis number)?</li><li>What brand is the OEM or aftermarket option?</li><li>Is there a warranty, and what does it cover?</li><li>Is the part new, and does it come in its original packaging?</li></ol>"),
   ("What does Partware Auto offer?", "Partware Auto's Facebook page says it offers Genuine, OEM and Aftermarket parts for Honda. Which grade is available depends on the part, so send your list on WhatsApp and ask for the options and the price of each.")],
  "undercarriage-parts"),
 ("parts-list-chassis-vin-export-quote", "How to give a parts list with chassis or VIN for an export quote",
  "What overseas buyers should send so a Honda parts exporter can check fitment and quote without back and forth.",
  [("Why send a chassis number or VIN?", "Honda models change within a generation. A facelift, engine option or market version can change a lamp, bumper, filter or sensor. The chassis number (or VIN) identifies the exact car, so the seller can confirm the right part instead of guessing from the model name."),
   ("Where do you find it?", "It is on the vehicle registration or log card, on a plate in the engine bay or at the base of the windscreen, and often on the driver's door pillar. Older Japanese-market cars use a shorter frame number, such as a model code followed by digits. Send whatever is printed."),
   ("What should each line of the list contain?", "<ul><li>Part number if you have it, otherwise a clear description.</li><li>Quantity.</li><li>Left or right, for lamps, mirrors and suspension parts.</li><li>Front or rear, where it applies.</li><li>The car it is for: model, generation code, year and chassis number.</li></ul>"),
   ("What else helps?", "Tell us the destination country, whether the car is left-hand or right-hand drive, the grade you prefer (Genuine, OEM or Aftermarket), and add a photo of the old part when you can. A simple CSV or text file with one part per line and the quantity after a comma works well."),
   ("Where do you send it?", "Use the export enquiry form. You can paste your list or upload a .csv or .txt file; lines that match our catalogue are listed and the rest go into your message. Shipping and payment terms are not set on the website, so ask in your enquiry.")],
  "servicing-essentials"),
 ("honda-vezel-common-service-parts", "Honda Vezel (HR-V) common service parts",
  "The service and wear parts owners of the Honda Vezel RU and RV usually need to plan for.",
  [("Which Vezel do you have?", "The Vezel sold in Singapore is also called the HR-V. The first generation is the RU (2014-2021) and the newer one is the RV (2021 onwards). Both are hybrids in our catalogue. Check your chassis number or log card before ordering, because parts differ between the two."),
   ("What are the regular servicing parts?", "<ul><li>Engine oil filter.</li><li>Engine air filter.</li><li>Cabin filter for the air-conditioning.</li><li>Spark plugs.</li><li>Wiper blades.</li></ul><p>Follow the owner's manual and service book for intervals. We do not give mileage figures here because they depend on your car and driving.</p>"),
   ("Which parts wear with use?", "<ul><li>Front and rear brake pads and brake discs. A hybrid uses its motor to slow the car, so pad wear can differ from a normal car; have them checked at each service.</li><li>Shock absorbers and stabiliser links, which can cause knocks over bumps as they wear.</li><li>CV joints, where a torn boot or a clicking sound when turning needs attention.</li><li>Engine mountings, if you feel more vibration.</li></ul>"),
   ("What about hybrid parts?", "The hybrid battery and drive system are specialist items and are not listed in our online catalogue. Ask us on WhatsApp if you need something that is not shown."),
   ("How do you order?", "Open the Vezel pages, add the parts to your cart and send the cart on WhatsApp. Ask about Genuine, OEM and Aftermarket options for each part.")],
  "servicing-essentials"),
]


def build_articles():
    cards = []
    for slug, t, d, qa, cat in ARTS:
        r = "../../"
        c = C[cat]
        xs = [x for x in PRODUCTS if x["cat"]["id"] == cat][:4]
        if slug == "honda-vezel-common-service-parts":
            xs = [x for x in PRODUCTS if x["m"] == "vezel-ru" and x["p"] in ("oil-filter", "cabin-filter", "front-brake-pads", "spark-plugs")]
        sec = "".join(f'<h2>{e(q)}</h2>{a if a.startswith("<") else f"<p>{a}</p>"}' for q, a in qa)
        extra = {"honda-vezel-common-service-parts": f'<a href="{r}honda/vezel-ru/">Honda Vezel RU parts</a> or <a href="{r}honda/vezel-rv/">Vezel RV parts</a>',
                 "parts-list-chassis-vin-export-quote": f'<a href="{r}export/">send an export parts list</a>',
                 "genuine-oem-aftermarket-honda-parts": f'<a href="{r}parts/{cat}/">{e(c["name"].lower())}</a>'}[slug]
        body = f'''<section class="ph"><div class="wrap narrow">{{{{CRUMBS}}}}<h1>{e(t)}</h1><p class="lead">{e(d)}</p>
<p class="small muted"><span class="draft">Draft for client review</span> By Partware Auto · 30 Oct 2026</p></div></section>
<article class="sec art-b"><div class="wrap narrow">{sec}
<div class="callout"><b>Need the part?</b> See {extra}, or <a href="{wa_link("Hi Partware Auto, I read your guide and need a part. Car plate / chassis: ")}" rel="noopener">WhatsApp us your car plate</a>.</div>
</div></article>
<section class="sec alt"><div class="wrap"><h2>Parts to ask about</h2><div class="pgrid">{"".join(card(x, r) for x in xs)}</div></div></section>'''
        art = {"@type": "Article", "headline": t, "description": d, "datePublished": "2026-10-30", "dateModified": TODAY,
               "author": {"@id": BASE + "/#store"}, "publisher": {"@id": BASE + "/#store"}, "image": BASE + "/og.jpg",
               "mainEntityOfPage": BASE + f"/articles/{slug}/"}
        shell(f"articles/{slug}/index.html", T(t + SUFFIX, t), d if len(d) < 160 else d[:157] + "...", body,
              active="articles", crumbs=[("Guides", "articles/"), (t, f"articles/{slug}/")], schema=[art], og_type="article", prio="0.6")
        cards.append(f'<a class="ac" href="{slug}/"><span class="ac-i">{ICON[c["icon"]]}</span><b>{e(t)}</b><span>{e(d)}</span></a>')
    body = f'''<section class="ph"><div class="wrap">{{{{CRUMBS}}}}<h1>Honda parts guides</h1>
<p class="lead">Short, practical answers to questions buyers ask: grades, export lists and common service parts.</p></div></section>
<section class="sec"><div class="wrap agrid">{"".join(cards)}</div></section>'''
    shell("articles/index.html", "Honda Parts Guides | Partware Auto", "Practical guides for Honda owners, workshops and overseas buyers: Genuine vs OEM vs aftermarket, export parts lists and Vezel service parts.",
          body, active="articles", crumbs=[("Guides", "articles/")], prio="0.6")


# ---------------- data.js, static files ----------------
def build_data():
    d = {"wa": WA, "live": LIVE,
         "brands": [{"id": b, "name": n} for b, n in BRANDS],
         "models": [{"id": m["id"], "b": m["b"], "name": m["name"], "code": m["code"], "years": m["years"], "alias": m["alias"], "fuel": m["fuel"]} for m in M.values()],
         "cats": [{"id": c["id"], "name": c["name"], "line": c["line"], "svg": ICON[c["icon"]]} for c in C.values()],
         "parts": [{"id": p["id"], "cat": p["cat"], "name": p["name"], "alias": p["alias"], "side": p["side"], "unit": p["unit"]} for p in P.values()],
         "products": [{k: x[k] for k in ("id", "m", "p", "url", "price", "sample", "oem", "stock", "status", "note")} for x in PRODUCTS]}
    (HERE / "data.js").write_text("/* Partware Auto catalogue, generated by build.py " + TODAY + ". Prices with sample:1 are demo prices. */\nwindow.PW=" + json.dumps(d, separators=(",", ":"), ensure_ascii=False) + ";\n")


def build_static():
    for f in ("pw.css", "pw.js", "wa.js", "data.js", "staff.js", "staff.css"):
        shutil.copy(HERE / f, OUT / f)
    for f in (HERE / "assets").iterdir():
        shutil.copy(f, OUT / f.name)
    write("robots.txt", "User-agent: *\nAllow: /\nDisallow: /staff/\nDisallow: /cart/\nDisallow: /search/\n\n" +
          "".join(f"User-agent: {b}\nAllow: /\n\n" for b in ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "ChatGPT-User", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Applebot-Extended", "DuckAssistBot"]) +
          f"Sitemap: {BASE}/sitemap.xml\n")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n" for u, p in SITEMAP) + "</urlset>\n")
    write(f"{INDEXNOW}.txt", INDEXNOW)
    write("site.webmanifest", json.dumps({"name": "Partware Auto Honda Parts", "short_name": "Partware Auto", "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#12161C", "background_color": "#ffffff", "display": "standalone"}))
    cats = "\n".join(f"- {c[1]}: {BASE}/parts/{c[0]}/" for c in CATS)
    models = "\n".join(f"- {BR[m[1]]} {m[2]} ({m[3]}, {m[4]}): {BASE}/{m[1]}/{m[0]}/" for m in MODELS)
    arts = "\n".join(f"- {a[1]}: {BASE}/articles/{a[0]}/" for a in ARTS)
    write("llms.txt", f"""# Partware Auto ({LEGAL})

> Honda parts specialist in Kaki Bukit, Singapore. Retailer, wholesaler and exporter of parts for the Honda make since 2015. Search by Honda model and part, then send your list on WhatsApp.

- Registered name: {LEGAL}, UEN {UEN}, incorporated {INC}
- Address: {ADDR1}, {ADDR2}
- Phone: {TEL}. WhatsApp: {WA_SHOW}
- Hours (from the Facebook page, to be confirmed): Mon-Fri 9am-6pm, Sat 9am-3pm, Sun and public holidays closed
- Services: retail, wholesale, export
- Grades offered: Genuine, OEM and Aftermarket (availability confirmed per part on WhatsApp)
- Product groups: Servicing Essentials, Engine Parts, Body Parts, Undercarriage Parts, Interior Parts
- Workshops and trade: {BASE}/workshops/
- Export enquiries: {BASE}/export/
- Preview note: prices in this preview are samples, not real prices.

## Product groups
{cats}

## Models
{models}

## Guides
{arts}
""")
    write("htaccess.txt", """# Go-live .htaccess for Partware Auto's own domain (paste via cPanel; edit DOMAIN)
ErrorDocument 404 /404.html
RewriteEngine On
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} ^www\\. [NC]
RewriteRule ^ https://DOMAIN%{REQUEST_URI} [L,R=301]
<FilesMatch "\\.(html)$">
Header set Cache-Control "max-age=3600"
</FilesMatch>
<IfModule mod_headers.c>
Header set X-Content-Type-Options "nosniff"
</IfModule>
""")


if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    build_data()
    build_home(); build_brands(); build_models(); build_products(); build_cats(); build_trade(); build_export(); build_pages(); build_articles()
    build_static()
    print(f"built {len(SITEMAP)} indexed pages, {len(PRODUCTS)} products -> {OUT}")
