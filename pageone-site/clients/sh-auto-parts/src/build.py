#!/usr/bin/env python3
"""SH Auto Parts - hidden preview website (Page One Singapore, 29 Oct 2026).

Run:  python3 build.py site
Facts: FACTS.md only. Catalogue = SAMPLE entries (no real list yet). Contact details = to confirm (WA / PHONE empty).
Preview URL: https://pageonesingapore.com/preview/sh-auto-parts/ (hidden by a server header; no noindex in pages).
"""
import html, json, sys, re, datetime, hashlib, shutil
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE / "site")
if not OUT.is_absolute():
    OUT = Path.cwd() / OUT

# ------------------------------------------------------------------ constants
BASE = "https://pageonesingapore.com/preview/sh-auto-parts"   # single BASE constant; change at go-live
WA = "6583680055"   # ASSUMED WhatsApp = first shopfront number (Edwin to confirm). Empty = enquiry form.
PHONES = ["+65 8368 0055", "+65 8368 1155"]   # shopfront sign, photo Edwin sent 29 Oct 2026
PHONE = PHONES[0]
EMAIL = "shautopartspl@gmail.com"   # shopfront sign
TODAY = datetime.date.today().isoformat()
BRAND = "SH Auto Parts"
LEGAL = "SH AUTO PARTS PTE. LTD."
UEN = "202418610M"
ADDR_STREET = "61 Woodlands Industrial Park E9, #01-08, E9 Premium"
ADDR_POST = "757047"
ADDR = f"{ADDR_STREET}, Singapore {ADDR_POST}"
TAG = "China Car Parts Supplier"
KEY = "7b3e9a1c5d0f48e2a6c1b94d8e03f5a7"   # IndexNow key
e = lambda s: html.escape(str(s), quote=True)
EMBLEM = (HERE / "assets" / "emblem.svg").read_text().strip()
CRED = "Stock photos: Unsplash"

# ------------------------------------------------------------------ photos (Unsplash, hotlinked, mood only)
PH = {
    "hero": "1642268565002-729f4e3dad5b", "matte": "1620891549027-942fdc95d3f5", "white": "1560958089-b8a1929cea89",
    "tail": "1725745096249-f6e7c160c4be", "taillit": "1518438223361-dde09dbeed6a", "head": "1531843256863-af93f4edfcfb",
    "charge": "1593941707874-ef25b8b4a92b", "showroom": "1666919643134-d97687c1826c", "wheel": "1572191267783-5618f992aff5",
    "door": "1615903214534-582a77a2a85e", "m3": "1648866892162-9336ef9182e2",
}
def purl(k, w): return f"https://images.unsplash.com/photo-{PH[k]}?auto=format&fit=crop&w={w}&q=70"
def pic(k, alt, w, h, sizes="100vw", eager=False, cls=""):
    ss = ", ".join(f"{purl(k, x)} {x}w" for x in (800, 1400, 2000))
    return (f'<img src="{purl(k, 1400)}" srcset="{ss}" sizes="{sizes}" alt="{e(alt)}" width="{w}" height="{h}" '
            f'{"" if eager else "loading=\"lazy\" "}decoding="async"{" fetchpriority=\"high\"" if eager else ""}{f" class=\"{cls}\"" if cls else ""} onerror="this.remove()">')

SHOP_IMG = '<img src="{{R}}shopfront.jpg" alt="SH Auto Parts shopfront at 61 Woodlands Industrial Park E9, #01-08, E9 Premium" width="720" height="960" loading="lazy" decoding="async">'

# ------------------------------------------------------------------ catalogue model
PARTS = [  # slug, name, category, synonyms (owner language)
    ("front-bumper", "Front Bumper", "bumpers", ["front bumper", "bumper front", "fbumper", "f bumper"]),
    ("rear-bumper", "Rear Bumper", "bumpers", ["rear bumper", "back bumper", "bumper rear", "bumper back", "r bumper"]),
    ("bumper-trim", "Bumper Trim", "bumpers", ["bumper trim", "bumper lip", "bumper strip", "bumper garnish", "sticker bumper", "bumper sticker", "bumper moulding", "bumper molding"]),
    ("headlamp", "Headlamp", "lamps-lights", ["headlamp", "headlight", "head lamp", "head light", "front light", "front lamp"]),
    ("tail-lamp", "Tail Lamp", "lamps-lights", ["tail lamp", "taillamp", "tail light", "taillight", "rear lamp", "rear light", "back light", "back lamp", "brake light", "tail"]),
    ("rear-reflector", "Rear Reflector", "lamps-lights", ["rear reflector", "reflector", "bumper reflector", "rear bumper reflector"]),
    ("fog-lamp", "Fog Lamp", "lamps-lights", ["fog lamp", "fog light", "foglamp", "foglight", "fog"]),
    ("side-mirror", "Side Mirror", "mirrors", ["side mirror", "wing mirror", "mirror cover", "mirror glass", "door mirror", "mirror"]),
    ("bonnet", "Bonnet", "body-panels", ["bonnet", "hood"]),
    ("fender", "Fender", "body-panels", ["fender", "front fender", "wing", "mudguard"]),
    ("door-panel", "Door Panel", "body-panels", ["door panel", "door shell", "door"]),
    ("tailgate", "Tailgate", "body-panels", ["tailgate", "boot", "boot lid", "trunk lid", "trunk", "liftgate"]),
    ("grille", "Grille", "grilles-trims", ["grille", "grill", "front grille", "front grill"]),
    ("wheel-arch", "Wheel Arch", "grilles-trims", ["wheel arch", "arch lining", "arch liner", "fender liner", "wheel arch liner"]),
    ("other", "Other Part", "other-parts", ["wiper", "cabin filter", "other part"]),
]
PART = {p[0]: p for p in PARTS}
GENERIC = [  # generic words owners type: slug -> weight
    ("bumper", {"front-bumper": .8, "rear-bumper": .8, "bumper-trim": .4}),
    ("lamp", {"headlamp": .6, "tail-lamp": .6, "fog-lamp": .4, "rear-reflector": .3}),
    ("light", {"headlamp": .6, "tail-lamp": .6, "fog-lamp": .4, "rear-reflector": .3}),
    ("body panel", {"bonnet": .5, "fender": .5, "door-panel": .5, "tailgate": .5}),
    ("panel", {"bonnet": .5, "fender": .5, "door-panel": .5, "tailgate": .5}),
]
CATS = [  # slug, name, line, part slugs, icon, title, desc
    ("bumpers", "Bumpers", "Front bumpers, rear bumpers and bumper trim", ["front-bumper", "rear-bumper", "bumper-trim"], "front-bumper"),
    ("lamps-lights", "Lamps & Lights", "Headlamps, tail lamps, rear reflectors and fog lamps", ["headlamp", "tail-lamp", "rear-reflector", "fog-lamp"], "tail-lamp"),
    ("mirrors", "Mirrors", "Side mirrors, covers and mirror glass", ["side-mirror"], "side-mirror"),
    ("body-panels", "Body Panels", "Bonnets, fenders, door panels and tailgates", ["bonnet", "fender", "door-panel", "tailgate"], "bonnet"),
    ("grilles-trims", "Grilles & Trims", "Front grilles, bumper trim and wheel arch linings", ["grille", "bumper-trim", "wheel-arch"], "grille"),
    ("other-parts", "Other Parts", "Wipers, cabin filters and other small parts", ["other"], "other"),
]
CAT = {c[0]: c for c in CATS}

def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# brand slug, name, brand aliases, models: (name, extra aliases, needs-brand aliases)
BRANDS = [
    ("tesla", "Tesla", ["tesla"], [("Model 3", ["model 3", "model3", "m3"], ["3"]), ("Model Y", ["model y", "modely"], ["y", "my"])]),
    ("byd", "BYD", ["byd"], [("Atto 3", ["atto 3", "atto3", "atto"], []), ("Dolphin", ["dolphin"], []), ("Seal", ["seal", "seal u"], []), ("Sealion 7", ["sealion 7", "sealion7", "sea lion 7", "sealion"], []), ("M6", ["m6", "byd m6"], [])]),
    ("denza", "Denza", ["denza"], [("D9", ["d9", "d 9", "d09"], ["09", "9"])]),
    ("mg", "MG", ["mg"], [("MG4", ["mg4", "mg 4"], ["4"]), ("ZS EV", ["zs ev", "zsev", "zs"], []), ("MG5", ["mg5", "mg 5"], ["5"]), ("HS", ["mg hs"], ["hs"])]),
    ("maxus", "Maxus", ["maxus"], [("MIFA 9", ["mifa 9", "mifa9", "mifa"], []), ("eDeliver 3", ["edeliver 3", "e deliver 3", "edeliver3", "edeliver"], [])]),
    ("chery", "Chery", ["chery"], []),
    ("omoda", "Omoda", ["omoda"], [("Omoda E5", ["omoda e5", "omoda5", "e5"], [])]),
    ("jaecoo", "Jaecoo", ["jaecoo"], [("J7", ["jaecoo j7", "j7"], [])]),
    ("gac", "GAC", ["gac", "gac motor", "aion"], [("Aion Y", ["aion y", "aiony"], []), ("Aion V", ["aion v", "aionv"], ["v"])]),
    ("xpeng", "XPeng", ["xpeng", "xiaopeng", "x peng"], [("G6", ["g6", "xpeng g6"], []), ("X9", ["x9", "xpeng x9"], [])]),
    ("foton", "Foton", ["foton"], []),
    ("geely", "Geely", ["geely"], []),
    ("zeekr", "Zeekr", ["zeekr", "zeker"], [("001", ["zeekr 001"], ["001", "1"]), ("X", ["zeekr x"], ["x"]), ("009", ["zeekr 009"], ["009"])]),
    ("deepal", "Deepal", ["deepal"], [("S07", ["deepal s07", "s07"], []), ("L07", ["deepal l07", "l07"], [])]),
    ("avatr", "Avatr", ["avatr", "avatar"], [("11", ["avatr 11"], ["11"]), ("12", ["avatr 12"], ["12"])]),
    ("ora", "Ora", ["ora"], [("Good Cat", ["good cat", "goodcat", "ora good cat"], [])]),
]
BASE5 = ["headlamp", "tail-lamp", "front-bumper", "rear-bumper", "side-mirror"]
EXTRA = {
    ("tesla", "Model 3"): ["rear-reflector", "bonnet"],
    ("tesla", "Model Y"): ["bumper-trim", "rear-reflector", "bonnet", "fender", "door-panel", "tailgate", "other"],
    ("byd", "Atto 3"): ["rear-reflector", "bonnet", "bumper-trim"], ("byd", "Dolphin"): ["fog-lamp"],
    ("byd", "Seal"): ["rear-reflector", "bonnet"], ("byd", "Sealion 7"): ["fender"],
    ("denza", "D9"): ["rear-reflector", "bumper-trim", "grille"],
    ("mg", "MG4"): ["rear-reflector", "bonnet"], ("mg", "ZS EV"): ["grille"], ("mg", "MG5"): ["grille"], ("mg", "HS"): ["grille"],
    ("maxus", "MIFA 9"): ["door-panel", "tailgate"], ("zeekr", "001"): ["bonnet", "rear-reflector"],
    ("xpeng", "G6"): ["rear-reflector"], ("gac", "Aion Y"): ["bonnet"], ("deepal", "S07"): ["rear-reflector"],
}
NOMODEL = ["front-bumper", "headlamp", "tail-lamp", "grille"]
SIDE_PARTS = {"headlamp", "tail-lamp", "rear-reflector", "fog-lamp", "side-mirror", "fender", "door-panel"}
STATUS = {"ask": "Ask for availability", "stock": "In stock", "order": "Can order"}

ENTRIES = []
for bslug, bname, _, models in BRANDS:
    if models:
        for mname, _, _ in models:
            for ps in BASE5 + EXTRA.get((bslug, mname), []):
                ENTRIES.append((bslug, bname, mname, ps))
    else:
        for ps in NOMODEL:
            ENTRIES.append((bslug, bname, "", ps))
ENTRIES = [dict(id=f"sh-{i + 1:04d}", brand=b, brandName=bn, model=m, modelSlug=slugify(m), part=ps, partName=PART[ps][1],
                title=(f"{bn} {m} {PART[ps][1]}" if m else f"{bn} {PART[ps][1]}"),
                side="Left or right - tell us" if ps in SIDE_PARTS else "", status="ask", sample=True, photo="", note="", price="", pub=True)
           for i, (b, bn, m, ps) in enumerate(ENTRIES)]
def find_entry(b, m, p):
    return next(x for x in ENTRIES if x["brand"] == b and x["model"] == m and x["part"] == p)

# ------------------------------------------------------------------ icons (line icons for part types; no stock photos on product cards)
IC = {
    "front-bumper": '<path d="M3 21h26v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM6.5 21l1.6-6.2A3 3 0 0 1 11 12.6h10a3 3 0 0 1 2.9 2.2L25.5 21M10 24h12M9 16.5h3M20 16.5h3"/>',
    "rear-bumper": '<path d="M3 21h26v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM5 21v-4.5a3 3 0 0 1 3-3h16a3 3 0 0 1 3 3V21M5.5 17h5M21.5 17h5M13 24h6"/>',
    "bumper-trim": '<path d="M3 17c8-5 18-5 26 0M3 22c8-5 18-5 26 0M8 14.6v9M24 14.6v9" />',
    "headlamp": '<path d="M5 9c6-3 12-1 15 4 1.6 3 .6 6.4-3 7.2-5.2 1.2-10-1.4-12-6-1-2.2-.6-4 0-5.2Z"/><circle cx="14" cy="14.5" r="3"/><path d="M24 11h5M25 15h4M24 19h5"/>',
    "tail-lamp": '<path d="M3 12 25 8c2.6-.4 4 1.2 4 3.4V15c0 2-1.2 3.4-3.2 3.7L5 22c-2 .3-3-.9-3-2.8Z"/><path d="M9 12.4v7M14 11.6v7M19 10.8v7"/>',
    "rear-reflector": '<rect x="4" y="10" width="24" height="12" rx="3"/><path d="M9 22 15 10M15 22l6-12M21 22l5-9"/>',
    "fog-lamp": '<circle cx="12" cy="16" r="6"/><circle cx="12" cy="16" r="2"/><path d="M21 11h8M22 16h7M21 21h8"/>',
    "side-mirror": '<path d="M12 8c8-2.5 16 1 16 7s-8 8.5-16 5.5Z"/><path d="M12 20 5.5 27M12 14.5H5"/>',
    "bonnet": '<path d="M4 23 8 11h16l4 12zM13 11l-2 12M19 11l2 12M8 23h16"/><path d="M4 26h24" opacity=".5"/>',
    "fender": '<path d="M3 25v-5.5c0-2.6 1.8-4.3 4.4-4.5l5-.4 4-4.6h5.6c3.5 0 7 2.4 7 6.5V25"/><path d="M8.5 25a5.7 5.7 0 0 1 11.4 0"/>',
    "door-panel": '<path d="M5 27V13l6-7h14a2 2 0 0 1 2 2v19zM5 13h17V6M18 19h6"/>',
    "tailgate": '<path d="M5 27V14c0-4 2-7 6-7h10c4 0 6 3 6 7v13zM9 12h14v7H9zM12 23h8"/>',
    "grille": '<rect x="4" y="9" width="24" height="14" rx="4"/><path d="M8 13h16M8 16h16M8 19h16M12 9v14M20 9v14" opacity=".6"/>',
    "wheel-arch": '<path d="M3 25a13 13 0 0 1 26 0"/><path d="M8 25a8 8 0 0 1 16 0M3 25h26"/>',
    "other": '<path d="M20 5a6 6 0 0 0-5.6 8.2L5 22.6a2.6 2.6 0 0 0 3.7 3.7l9.4-9.4A6 6 0 0 0 26.5 11l-3.5 3.5-3.4-1-1-3.4L22 6.6A6 6 0 0 0 20 5Z"/>',
}
def ico(k, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[k]}</svg>'
UI = {
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3a.4.4 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>',
    "send": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12 20 4l-5 16-3.5-6.5Z"/><path d="m11.5 13.5 4-5"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "wrench": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M20 5a6 6 0 0 0-5.6 8.2L5 22.6a2.6 2.6 0 0 0 3.7 3.7l9.4-9.4A6 6 0 0 0 26.5 11l-3.5 3.5-3.4-1-1-3.4L22 6.6A6 6 0 0 0 20 5Z"/></svg>',
    "car": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 21H3.5v-5L6 9.5h14L25 16h3.5v5H27M10 21h10"/><circle cx="8" cy="21.5" r="2.6"/><circle cx="24" cy="21.5" r="2.6"/><path d="M6 16h19"/></svg>',
    "photo": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="8" width="24" height="17" rx="3"/><circle cx="16" cy="16.5" r="4.5"/><path d="M11 8l1.6-3h6.8L21 8"/></svg>',
    "check": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="16" cy="16" r="12"/><path d="m10.5 16.5 3.8 3.8 7.2-8"/></svg>',
    "pin": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M16 29s9-8.5 9-15a9 9 0 0 0-18 0c0 6.5 9 15 9 15Z"/><circle cx="16" cy="14" r="3.2"/></svg>',
    "doc": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M8 3h11l6 6v20H8z"/><path d="M19 3v6h6M12 15h9M12 19h9M12 23h6"/></svg>',
}

# ------------------------------------------------------------------ links to enquiry / WhatsApp
def enq(text, r="{{R}}", vehicle=""):
    """Enquiry href. WA empty -> on-site enquiry form prefilled. WA set -> wa.me with the prefilled message."""
    if WA:
        msg = f"Hi SH Auto Parts, I'm looking for: {text}" + (f" for {vehicle}" if vehicle else "") + ". (from website)"
        return f"https://wa.me/{WA}?text={quote(msg)}"
    return f"{r}enquiry/?q={quote(text + (' for ' + vehicle if vehicle else ''))}"
PVN = '' if WA else '<span class="pvn">Preview note: WhatsApp number pending. Enquire buttons open the enquiry form for now.</span>'

# ------------------------------------------------------------------ page shell
VER = {}
def asset(name):
    if name not in VER:
        VER[name] = hashlib.sha1((HERE / name).read_bytes()).hexdigest()[:8]
    return f"{name}?v={VER[name]}"

pages = []  # (url path, priority)
def logo_html(r):
    return (f'<a class="logo" href="{r}" aria-label="SH Auto Parts home"><img class="em" src="{r}logo-96.png" alt="" width="48" height="48">'
            f'<span class="wm"><b>SH AUTO</b><b>PARTS</b><small>{TAG}</small></span></a>')

ORG = {"@type": ["AutoPartsStore", "Organization"], "@id": BASE + "/#org", "name": BRAND, "legalName": LEGAL, "url": BASE + "/",
       "identifier": {"@type": "PropertyValue", "propertyID": "UEN", "value": UEN},
       "foundingDate": "2024-05-09", "slogan": TAG, "logo": BASE + "/icon-512.png", "image": BASE + "/og.jpg",
       "description": "Singapore seller of China and EV car body parts for workshops and car owners.",
       "address": {"@type": "PostalAddress", "streetAddress": ADDR_STREET, "addressLocality": "Singapore", "postalCode": ADDR_POST, "addressCountry": "SG"},
       "areaServed": {"@type": "Country", "name": "Singapore"}}
if PHONE: ORG["telephone"] = PHONE
ORG["email"] = EMAIL
SITE = {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": BRAND, "publisher": {"@id": BASE + "/#org"},
        "potentialAction": {"@type": "SearchAction", "target": BASE + "/catalogue/?q={search_term_string}", "query-input": "required name=search_term_string"}}

NAV = [("catalogue/", "Catalogue", "cat"), ("parts/", "Parts", "parts"), ("brands/", "Brands", "brands"),
       ("for-workshops/", "Workshops", "ws"), ("for-car-owners/", "Car owners", "own"), ("about/", "About", "about"), ("contact/", "Contact", "contact")]

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details class="rv"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items) + "</div>"
def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def shell(path, title, desc, body, active="", crumbs=None, schema=None, og_type="website", index=True, faq=None, img=None, pri=0.7, preload=None):
    assert len(title) < 60, (path, len(title), title)
    assert len(desc) < 160, (path, len(desc), desc)
    depth = path.count("/")
    r = "../" * depth
    url = BASE + "/" + ("" if path == "index.html" else path.replace("index.html", ""))
    ld = [dict(ORG), dict(SITE)] if path == "index.html" else [{"@id": BASE + "/#org"} if False else dict(ORG)]
    if crumbs:
        ld.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u}
                                                                     for i, (n, u) in enumerate([("Home", "")] + crumbs)]})
    if faq: ld.append(faq_ld(faq))
    if schema: ld.extend(schema)
    ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False).replace("</", "<\\/")
    nav = "".join(f'<a href="{r}{u}"{" aria-current=\"page\"" if k == active else ""}>{n}</a>' for u, n, k in NAV)
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Breadcrumb"><a href="' + r + '">Home</a>' + "".join(
            (f'<span>/</span><a href="{r}{u}">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span>/</span><span aria-current="page">{e(n)}</span>')
            for i, (n, u) in enumerate(crumbs)) + "</nav>"
    body = body.replace("{{CRUMBS}}", cr).replace("{{R}}", r)
    ogi = img or BASE + "/og.jpg"
    brands_ft = "".join(f'<li><a href="{r}brands/{b[0]}/">{e(b[1])}</a></li>' for b in BRANDS[:8])
    brands_ft2 = "".join(f'<li><a href="{r}brands/{b[0]}/">{e(b[1])}</a></li>' for b in BRANDS[8:])
    parts_ft = "".join(f'<li><a href="{r}parts/{c[0]}/">{e(c[1])}</a></li>' for c in CATS)
    doc = f"""<!doctype html>
<html lang="en-SG" class="no-js" data-root="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="en_SG"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{ogi}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="SH Auto Parts - China and EV car parts in Singapore">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{ogi}">
<link rel="icon" href="{r}favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="{r}icon-192.png"><link rel="apple-touch-icon" href="{r}apple-touch-icon.png"><link rel="manifest" href="{r}site.webmanifest">
<meta name="theme-color" content="#0A0A0C">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Saira:ital,wght@0,500;0,600;0,700;0,800;1,600;1,700;1,800&display=swap">
{f'<link rel="preconnect" href="https://images.unsplash.com">' if preload else ''}
<link rel="stylesheet" href="{r}{asset('sh.css')}">
<script>document.documentElement.classList.remove('no-js');document.documentElement.classList.add('js');window.SH_ROOT="{r}";</script>
<script type="application/ld+json">{ldj}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="pv" role="note">Preview for SH Auto Parts - not live. Staff demo: <a href="{r}staff/">/staff/</a></div>
<header class="hd"><div class="wrap">
{logo_html(r)}
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="nav-cta" href="{enq('a part', r)}">Enquire</a></nav>
<button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
</div></header>
<main id="main">
{body}
</main>
<footer class="ft"><div class="wrap">
<div class="ft-g">
<div class="ft-about">{logo_html(r)}<p>{LEGAL}<br>UEN {UEN}<br>Shop: {e(ADDR)}<br>Call {" / ".join(f'<a href="tel:{x.replace(" ","")}">{x}</a>' for x in PHONES)}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p><p class="mu">Brand names are used only to describe which vehicles a part is for.</p></div>
<div><h4>Parts</h4><ul>{parts_ft}<li><a href="{r}catalogue/">Full catalogue</a></li></ul></div>
<div><h4>Brands</h4><ul>{brands_ft}</ul></div>
<div><h4>&nbsp;</h4><ul>{brands_ft2}</ul></div>
<div><h4>Company</h4><ul><li><a href="{r}for-workshops/">For workshops</a></li><li><a href="{r}for-car-owners/">For car owners</a></li><li><a href="{r}articles/">Guides</a></li><li><a href="{r}about/">About</a></li><li><a href="{r}contact/">Contact</a></li><li><a href="{r}enquiry/">Enquiry</a></li><li><a href="{r}privacy/">Privacy</a></li></ul></div>
</div>
<div class="ft-b"><span>&copy; {datetime.date.today().year} {LEGAL}</span><span>Stock photos are mood imagery only. <a href="{r}staff/">Staff</a></span></div>
</div></footer>
<nav class="mbar" aria-label="Quick actions"><a href="{r}catalogue/">{UI['search']}<span>Search</span></a><a href="{enq('a part', r)}">{UI['send']}<span>Enquire</span></a><a class="wa" href="{enq('a part', r)}">{UI['wa']}<span>WhatsApp</span></a></nav>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="{r}{asset('data.js')}" defer></script><script src="{r}{asset('sh.js')}" defer></script><script src="{r}{asset('wa.js')}" defer></script>
</body>
</html>
"""
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc)
    if index:
        pages.append(("/" + ("" if path == "index.html" else path.replace("index.html", "")), pri))

def btn(href, label, kind="p", extra=""):
    return f'<a class="btn btn-{kind}" href="{href}"{extra}>{label}</a>'

def card_static(x, r="{{R}}"):
    veh = f"{x['brandName']} {x['model']}".strip()
    return (f'<article class="rc rv"><div class="rc-ic">{ico(x["part"])}</div><div class="rc-b"><span class="chip">{e(veh)}</span>'
            f'<h3>{e(x["title"])}</h3><div class="rc-m"><span class="pill">Ask for availability</span><span class="smp">Sample listing - staff to confirm</span></div>'
            f'<div class="rc-a"><a class="btn btn-p btn-s" href="{enq(x["title"], r, "")}">Enquire</a>'
            f'<a class="btn btn-g btn-s" href="{r}catalogue/?brand={x["brand"]}&amp;model={x["modelSlug"]}&amp;part={x["part"]}">Details</a></div></div></article>')

TRY = ["Tesla Model Y tail lamp", "Denza D9 rear reflector", "atto3 headlight", "MG4 side mirror", "zeekr 001 bonnet", "sticker bumper model y"]
def search_box(idp, ph="Brand, model and part, e.g. Tesla Model Y tail lamp", action="{{R}}catalogue/", live=True, tries=TRY, big=True):
    ch = "".join(f'<button type="button" data-try="{e(t)}">{e(t)}</button>' for t in tries)
    return f'''<form class="sbox{" big" if big else ""}" role="search" action="{action}" method="get" data-search="{idp}">
<label class="sr" for="{idp}-q">Search the catalogue</label>
<div class="srow">{UI["search"]}<input id="{idp}-q" class="sin" name="q" type="search" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search" placeholder="{e(ph)}"><button class="btn btn-p" type="submit">Search</button></div>
<p class="try"><span>Try:</span>{ch}</p>
<div class="sres" id="{idp}-res" aria-live="polite"></div></form>'''

def brandchips(r="{{R}}", marquee=True):
    one = "".join(f'<a class="bchip" href="{r}brands/{b[0]}/">{e(b[1])}</a>' for b in BRANDS)
    two = one.replace("<a ", '<a tabindex="-1" aria-hidden="true" ', ) if marquee else ""
    return f'<div class="bstrip" aria-label="Brands"><div class="btrack">{one}{two}</div></div>'

# ------------------------------------------------------------------ pages
HOME_FAQ = [
    ("Do you have the part for my car, for example a Tesla Model Y tail lamp?",
     "Search by brand, model and part. The listings on this preview are samples, so we never promise stock from a search result. Send the car and the part and we confirm fitment and availability, then reply."),
    ("Who do you sell to?", "SH Auto Parts sells in Singapore to workshops and car owners. We do not export."),
    ("Which car brands do you cover?",
     "Our brand board lists MG, Tesla, Maxus, Chery, BYD, GAC, XPeng, Foton, Geely, Zeekr, Omoda, Jaecoo, Denza, Deepal, Avatr and Ora, mainly for body parts. If your model is not listed, send it to us and ask."),
    ("How do I get the right part?",
     "Tell us the brand, model and the part, and add a photo of the old part if you can. We check fitment against your car before anything is confirmed. Prices and availability are given on enquiry."),
]

def home():
    cats = "".join(f'''<a class="cc rv" href="{{{{R}}}}parts/{c[0]}/"><span class="cc-ic">{ico(c[4])}</span><h3>{e(c[1])}</h3><p>{e(c[2])}</p><span class="more">More details {UI["arrow"]}</span></a>''' for c in CATS)
    feat = [find_entry("tesla", "Model Y", "tail-lamp"), find_entry("tesla", "Model Y", "front-bumper"), find_entry("denza", "D9", "rear-reflector"),
            find_entry("byd", "Atto 3", "headlamp"), find_entry("mg", "MG4", "side-mirror"), find_entry("zeekr", "001", "bonnet")]
    steps = [("Search", "Type the brand, model and part in plain words, the way you would say it to us."),
             ("Send car and part", "Open the enquiry form or WhatsApp with your car details. A photo of the old part helps."),
             ("We confirm and reply", "We check fitment against your car and reply with availability.")]
    st = "".join(f'<li class="rv"><span class="n">{i + 1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(steps))
    body = f'''<section class="hero">
<div class="hero-bg" aria-hidden="true">{pic("hero", "Car tail light in the dark (mood image)", 2000, 1333, "100vw", True, "kb")}</div>
<div class="wrap hero-in">
<p class="eyebrow">China &amp; EV car parts &middot; Singapore</p>
<h1>Body parts for China &amp; EV cars, <em>found by car and part.</em></h1>
<p class="lead">Search the way you talk, like &ldquo;Tesla Model Y tail lamp&rdquo;. Then send us your car and the part. For workshops and car owners in Singapore.</p>
{search_box("hq")}
{PVN}
</div></section>
<section class="strip"><div class="wrap">{brandchips()}</div></section>
<section class="sec"><div class="wrap">
<div class="sec-t rv"><p class="kick">Parts</p><h2>Browse by part type</h2><p>Mainly body parts, plus some other parts. Pick a type to see what each part is and which cars it is listed for.</p></div>
<div class="cgrid">{cats}</div>
</div></section>
<section class="sec alt"><div class="wrap">
<div class="sec-t rv"><p class="kick">Featured listings</p><h2>Sample listings from the catalogue</h2><p>Example entries to show how the catalogue works. We confirm availability and fitment on enquiry.</p></div>
<div class="rgrid">{"".join(card_static(x) for x in feat)}</div>
<p class="center rv" style="margin-top:28px"><a class="btn btn-g" href="{{{{R}}}}catalogue/">See the full catalogue {UI["arrow"]}</a></p>
</div></section>
<section class="sec"><div class="wrap">
<div class="two">
<a class="tc rv" href="{{{{R}}}}for-workshops/"><div class="tc-ph">{pic("door", "Red and black car door, mood image", 900, 600, "(min-width:900px) 45vw, 100vw")}</div><div class="tc-b"><p class="kick">For workshops</p><h3>Parts for the job on your bay</h3><p>Send the car and the parts you need. We check fitment and reply.</p><span class="more">More details {UI["arrow"]}</span></div></a>
<a class="tc rv" href="{{{{R}}}}for-car-owners/"><div class="tc-ph">{pic("matte", "Matte black electric car under a warm sky, mood image", 900, 600, "(min-width:900px) 45vw, 100vw")}</div><div class="tc-b"><p class="kick">For car owners</p><h3>Not sure which part it is?</h3><p>Tell us your car and what is damaged. We help you find the right part name.</p><span class="more">More details {UI["arrow"]}</span></div></a>
</div></div></section>
<section class="sec alt"><div class="wrap">
<div class="sec-t rv"><p class="kick">How it works</p><h2>Three steps</h2></div>
<ol class="steps">{st}</ol>
</div></section>
<section class="sec"><div class="wrap shop">
<div class="shop-ph rv">{SHOP_IMG}</div>
<div class="shop-b rv"><p class="kick">Visit or call</p><h2>Our shop in Woodlands</h2><p>{e(ADDR)}</p>
<p>Call <a href="tel:{PHONES[0].replace(" ","")}">{PHONES[0]}</a> or <a href="tel:{PHONES[1].replace(" ","")}">{PHONES[1]}</a><br>Email <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p class="mu">Opening hours: to confirm.</p>
<div class="btns">{btn(enq("a part"), "WhatsApp us " + UI["arrow"])}{btn("tel:" + PHONES[0].replace(" ",""), "Call now", "g")}</div></div>
</div></section>
<section class="sec"><div class="wrap narrow">
<div class="sec-t rv"><p class="kick">FAQ</p><h2>Quick answers</h2></div>
{faq_html(HOME_FAQ)}
</div></section>
<section class="cta"><div class="wrap center rv"><h2>Tell us the car and the part.</h2><p>We confirm fitment and reply. {PVN.replace("pvn", "pvn")}</p><div class="btns">{btn(enq("a part"), "Send an enquiry " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div></div></section>'''
    shell("index.html", "SH Auto Parts | China & EV Body Parts in Singapore",
          "Search body parts for Tesla, BYD, Denza, MG, Zeekr and more China and EV cars. SH Auto Parts serves workshops and car owners in Singapore.",
          body, "", faq=HOME_FAQ, pri=1.0, preload=True)

def catalogue():
    brandopts = "".join(f'<option value="{b[0]}">{e(b[1])}</option>' for b in BRANDS)
    partopts = "".join(f'<option value="{p[0]}">{e(p[1])}</option>' for p in PARTS)
    links = "".join(f'<li><a href="{{{{R}}}}brands/{b[0]}/">{e(b[1])} parts</a></li>' for b in BRANDS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Catalogue</p><h1>Search the catalogue</h1>
<p class="lead">Type the brand, model and part, or use the filters. Listings are samples until staff confirm them.</p></div></section>
<section class="sec tight"><div class="wrap">
<form class="sbox" id="cat-form" role="search" action="" method="get" data-search="cq">
<label class="sr" for="cq-q">Search</label>
<div class="srow">{UI["search"]}<input id="cq-q" class="sin" name="q" type="search" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="Brand, model and part, e.g. Tesla Model Y tail lamp"><button class="btn btn-p" type="submit">Search</button></div>
<div class="filters"><label>Brand<select name="brand" id="f-brand"><option value="">All brands</option>{brandopts}</select></label>
<label>Model<select name="model" id="f-model"><option value="">All models</option></select></label>
<label>Part<select name="part" id="f-part"><option value="">All parts</option>{partopts}</select></label>
<button class="btn btn-g btn-s" type="button" id="f-clear">Clear</button></div>
<p class="try"><span>Try:</span>{"".join(f'<button type="button" data-try="{e(t)}">{e(t)}</button>' for t in TRY)}</p>
</form>
{PVN}
<div class="count" id="cat-count" aria-live="polite"></div>
<div class="sres full" id="cat-res"></div>
<noscript><p class="note">The search needs JavaScript. You can still browse by brand:</p><ul class="plain">{links}</ul></noscript>
</div></section>'''
    ld = [{"@type": "ItemList", "name": "Brands in the SH Auto Parts catalogue", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": f"{b[1]} body parts", "url": f"{BASE}/brands/{b[0]}/"} for i, b in enumerate(BRANDS)]}]
    shell("catalogue/index.html", "Catalogue | SH Auto Parts Singapore",
          "Search China and EV car body parts by brand, model and part, like Tesla Model Y tail lamp. Sample listings; send us your car to confirm.",
          body, "cat", [("Catalogue", "catalogue/")], ld, pri=0.9)

def parts_hub():
    cards = "".join(f'''<a class="cc rv" href="{{{{R}}}}parts/{c[0]}/"><span class="cc-ic">{ico(c[4])}</span><h3>{e(c[1])}</h3><p>{e(c[2])}</p><span class="more">More details {UI["arrow"]}</span></a>''' for c in CATS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Parts</p><h1>Parts for China &amp; EV cars</h1><p class="lead">Mainly body parts, with some other parts. Choose a type, or go straight to the search.</p></div></section>
<section class="sec tight"><div class="wrap"><div class="cgrid">{cards}</div><div class="center" style="margin-top:32px">{btn("{{R}}catalogue/", "Search the catalogue " + UI["arrow"])}</div></div></section>'''
    shell("parts/index.html", "Car Body Parts by Type | SH Auto Parts",
          "Bumpers, lamps and lights, mirrors, body panels, grilles and trims for China and EV cars in Singapore. Choose a part type.",
          body, "parts", [("Parts", "parts/")], pri=0.8)

PART_COPY = {
    "bumpers": ("Bumpers for China & EV cars", "Front bumpers, rear bumpers and bumper trim for China and EV cars sold in Singapore. Tell us the model and we confirm fitment.",
        ["A bumper is more than one piece. There is usually the outer bumper cover, and separate trim pieces such as the lower lip, strips and garnish. Tell us which piece you mean, and say front or rear.",
         "If your car has parking sensors or a camera near the bumper, mention it and send a photo. It helps us match the right part.",
         "Not sure what the piece is called? Send a photo of the damage and the car model."]),
    "lamps-lights": ("Lamps & lights for China & EV cars", "Headlamps, tail lamps, rear reflectors and fog lamps for China and EV cars in Singapore. Send your model and we confirm fitment.",
        ["Lamps are listed by position: headlamp at the front, tail lamp at the rear, rear reflector low on the rear bumper, and fog lamp. People also say headlight, taillight or brake light, and the search understands those words.",
         "Say which side you need. Left and right are as seen from the driver's seat. A photo of the old lamp, front and back, is the quickest way for us to match it."]),
    "mirrors": ("Side mirrors for China & EV cars", "Side mirrors, mirror covers and mirror glass for China and EV cars in Singapore. Tell us your model and which side you need.",
        ["Owners ask for the whole mirror, only the cover, or only the glass. Tell us which one, and which side. Left and right are as seen from the driver's seat.",
         "A photo of the broken mirror from the outside and, if possible, the back helps us confirm the right part."]),
    "body-panels": ("Body panels for China & EV cars", "Bonnets, fenders, door panels and tailgates for China and EV cars in Singapore. Send the model and we confirm fitment.",
        ["Body panels are the big pieces: the bonnet (hood), the front fender (wing), door panels and the tailgate (boot lid). Panels are specific to the model, so we always check against your car.",
         "Tell us the model and the damage. A few photos from different angles are enough to start."]),
    "grilles-trims": ("Grilles & trims for China & EV cars", "Front grilles, bumper trim and wheel arch linings for China and EV cars in Singapore. Send your model and we confirm fitment.",
        ["Grilles and trim pieces are small but easy to get wrong, because the shape changes between models. Send a photo of the piece, or of the place where it was fitted.",
         "Bumper trim also appears under Bumpers. Wheel arch lining is the liner inside the wheel arch."]),
    "other-parts": ("Other parts for China & EV cars", "Wipers, cabin filters and other small parts for China and EV cars in Singapore. Tell us the car and what you need.",
        ["Our focus is body parts, but some owners and workshops also need other small parts such as wipers or a cabin filter. Ask us with the car model and we check.",
         "If the part you want is not in the catalogue, send an enquiry. Not being listed does not mean we cannot help."]),
}
def part_pages():
    for c in CATS:
        slug, name, line, ps, icon = c
        h1, desc, paras = PART_COPY[slug]
        title = f"{name} for China & EV Cars | SH Auto Parts"
        sub = "".join(f'<li id="{p}"><span class="ic-s">{ico(p)}</span><div><h3>{e(PART[p][1])}</h3><p class="mu">Also searched as: {e(", ".join(PART[p][3][:4]))}.</p>'
                      f'<a class="more" href="{{{{R}}}}catalogue/?part={p}">See {e(PART[p][1].lower())} listings {UI["arrow"]}</a></div></li>' for p in ps)
        others = "".join(f'<a class="bchip" href="{{{{R}}}}parts/{o[0]}/">{e(o[1])}</a>' for o in CATS if o[0] != slug)
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Parts</p><h1>{h1.replace("&", "&amp;")}</h1><p class="lead">{e(line)}.</p></div></section>
<section class="sec tight"><div class="wrap two-c">
<div class="prose">{"".join(f"<p>{e(t)}</p>" for t in paras)}
<h2>Part types in this group</h2><ul class="plist">{sub}</ul>
<div class="btns">{btn(enq(name), "Enquire about " + e(name.lower()) + " " + UI["arrow"])}{btn("{{R}}catalogue/?" + "part=" + ps[0], "Search these parts", "g")}</div>{PVN}</div>
<aside class="side"><div class="panel"><h3>Search by car</h3>{search_box("pq", "Brand, model and part", tries=[f"Tesla Model Y {PART[ps[0]][1].lower()}", f"BYD Atto 3 {PART[ps[0]][1].lower()}"], big=False)}</div></aside>
</div></section>
<section class="sec alt tight"><div class="wrap"><div class="sec-t"><h2>Listed cars</h2><p>Sample listings in this group. Staff confirm availability and fitment on enquiry.</p></div>
<div class="sres full" data-list="parts:{','.join(ps)}" data-limit="9"></div>
<noscript><p class="note">Open the <a href="{{{{R}}}}catalogue/">catalogue</a> to see listings.</p></noscript></div></section>
<section class="sec tight"><div class="wrap"><div class="sec-t"><h2>Other part types</h2></div><div class="bchips">{others}</div></div></section>'''
        shell(f"parts/{slug}/index.html", title, desc, body, "parts", [("Parts", "parts/"), (name, f"parts/{slug}/")], pri=0.8)

def brands_hub():
    cards = "".join(f'<a class="cc rv" href="{{{{R}}}}brands/{b[0]}/"><span class="cc-ic bn">{e(b[1][:2].upper())}</span><h3>{e(b[1])}</h3><p>{e(", ".join(m[0] for m in b[3]) if b[3] else "Ask us for your model")}</p><span class="more">More details {UI["arrow"]}</span></a>' for b in BRANDS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Brands</p><h1>Car brands we list parts for</h1><p class="lead">The 16 brands on our brand board. Brand names only describe which vehicle a part is for.</p></div></section>
<section class="sec tight"><div class="wrap"><div class="cgrid">{cards}</div></div></section>'''
    shell("brands/index.html", "Car Brands | SH Auto Parts Singapore",
          "China and EV car brands we list body parts for: Tesla, BYD, Denza, MG, Maxus, Chery, Zeekr and more. Choose your brand.",
          body, "brands", [("Brands", "brands/")], pri=0.8)

def brand_pages():
    for slug, name, _, models in BRANDS:
        if models:
            mnames = [m[0] for m in models]
            ml = mnames[0] if len(mnames) == 1 else ", ".join(mnames[:-1]) + " and " + mnames[-1]
            intro = f"SH Auto Parts lists body and lamp parts for {name} {ml}. Search by model and part, then send us your car so we can confirm fitment. The listings on this preview are samples until staff confirm the real list."
            desc = f"{name} body parts in Singapore: sample listings for {ml}. Send your car and part and we confirm fitment."
            rows = ""
            for m in models:
                ps = [x["part"] for x in ENTRIES if x["brand"] == slug and x["model"] == m[0]]
                links = " &middot; ".join(f'<a href="{{{{R}}}}catalogue/?brand={slug}&amp;model={slugify(m[0])}&amp;part={p}">{e(PART[p][1])}</a>' for p in ps)
                rows += f'<li><h3>{e(name)} {e(m[0])}</h3><p>{links}</p></li>'
            modelsec = f'<h2>{e(name)} models</h2><ul class="mlist">{rows}</ul>'
        else:
            intro = f"{name} is on our brand board, but no {name} model is listed here yet. Tell us your model and the part, with a photo if you can, and we check what we can find."
            desc = f"{name} body parts in Singapore: tell us your model and part and SH Auto Parts checks. Sample listings only."
            ps = [x["part"] for x in ENTRIES if x["brand"] == slug]
            links = " &middot; ".join(f'<a href="{{{{R}}}}catalogue/?brand={slug}&amp;part={p}">{e(PART[p][1])}</a>' for p in ps)
            modelsec = f'<h2>Parts we are asked about</h2><p class="mu">Model: ask us. These are sample part types for {e(name)}.</p><p>{links}</p>'
        title = f"{name} Body Parts in Singapore | SH Auto Parts"
        others = "".join(f'<a class="bchip" href="{{{{R}}}}brands/{b[0]}/">{e(b[1])}</a>' for b in BRANDS if b[0] != slug)
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Brand</p><h1>{e(name)} body parts in Singapore</h1><p class="lead">{e(intro)}</p></div></section>
<section class="sec tight"><div class="wrap two-c">
<div class="prose">{modelsec}<p>Not sure which part you need? Read <a href="{{{{R}}}}articles/which-part-is-it/">which part is it</a>, or <a href="{enq(name + " part")}">send us your {e(name)} and the part</a>.</p>{PVN}</div>
<aside class="side"><div class="panel"><h3>Search {e(name)} parts</h3>{search_box("bq", f"{name} model and part", tries=[f"{name} tail lamp", f"{name} front bumper"], big=False)}</div></aside>
</div></section>
<section class="sec alt tight"><div class="wrap"><div class="sec-t"><h2>{e(name)} listings</h2><p>Sample listings. Staff confirm availability and fitment on enquiry.</p></div>
<div class="sres full" data-list="brand:{slug}" data-limit="9"></div></div></section>
<section class="sec tight"><div class="wrap"><div class="sec-t"><h2>Other brands</h2></div><div class="bchips">{others}</div></div></section>'''
        shell(f"brands/{slug}/index.html", title, desc, body, "brands", [("Brands", "brands/"), (name, f"brands/{slug}/")], pri=0.7)

WS_FAQ = [("What should a workshop send us?", "The car brand and model, the part, left or right if it matters, and a photo of the old part or the damage. A list of several parts is fine."),
          ("Do you give workshop prices?", "Prices are not listed on this preview. Ask in your enquiry and we reply. Any trade terms are to confirm."),
          ("Can I ask for a part that is not in the catalogue?", "Yes. The catalogue is a sample, so send the car and part and we check.")]
OWN_FAQ = [("I do not know what the part is called. What do I do?", "Send a photo of the damage and your car model. Our guide on part names also helps. We reply with the part name and what we can find."),
           ("Do I need to know the car year?", "It helps. Send the model and, if you can, the year shown on your car documents. We confirm fitment before anything else."),
           ("Can I buy online here?", "Not on this preview. You search, send an enquiry, and we reply. Prices and availability are given on enquiry.")]
def audience_pages():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">For workshops</p><h1>Parts for China &amp; EV cars, for Singapore workshops</h1>
<p class="lead">Search by car and part, send us your list, and we check fitment before we reply. We sell in Singapore to workshops and car owners.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div class="prose">
<h2>How a workshop uses this site</h2>
<ul class="ticks"><li>Search the catalogue by brand, model and part, in the words you already use.</li><li>Send the car and the part from the enquiry form. A list of several parts is fine.</li><li>Add a photo of the old part or the damage, front and back for lamps.</li><li>We confirm fitment against the car and reply.</li></ul>
<h2>What we focus on</h2><p>Mainly body parts: bumpers, lamps, mirrors, panels, grilles and trims, plus some other parts, for China and EV brands such as Tesla, BYD, Denza, MG, Zeekr and more. See all <a href="{{{{R}}}}brands/">brands</a>.</p>
<h2>To confirm</h2><p class="mu">Trade pricing, stock, delivery and warranty are not stated on this preview. They are to confirm with SH Auto Parts.</p>
<div class="btns">{btn(enq("parts for our workshop"), "Send a parts list " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div>{PVN}</div>
<aside class="side"><div class="panel photo">{pic("door", "Car door panel, mood image", 700, 520, "(min-width:900px) 30vw, 100vw")}</div></aside></div></section>
<section class="sec alt"><div class="wrap narrow"><div class="sec-t"><h2>Workshop FAQ</h2></div>{faq_html(WS_FAQ)}</div></section>'''
    shell("for-workshops/index.html", "Parts for Workshops | SH Auto Parts Singapore",
          "China and EV car body parts for Singapore workshops. Search by car and part, send your list, and SH Auto Parts confirms fitment.",
          body, "ws", [("For workshops", "for-workshops/")], faq=WS_FAQ, pri=0.8)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">For car owners</p><h1>Find the right part for your China or EV car</h1>
<p class="lead">Not sure what the part is called? Tell us the car and what is damaged, and we help you find it.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div class="prose">
<h2>What to tell us</h2>
<ul class="ticks"><li>Your car brand and model, for example Tesla Model Y or BYD Atto 3.</li><li>The part, or a photo of the damage if you do not know its name.</li><li>Left or right, if the part comes in pairs. Left and right are as seen from the driver's seat.</li></ul>
<h2>Useful guides</h2><p><a href="{{{{R}}}}articles/tesla-model-y-tail-lamp-what-to-send/">Tesla Model Y tail lamp: what to send us</a><br><a href="{{{{R}}}}articles/china-ev-body-parts-what-to-check/">What to check before you buy body parts</a><br><a href="{{{{R}}}}articles/which-part-is-it/">Which part is it? Names explained</a></p>
<h2>To confirm</h2><p class="mu">Prices, stock, fitting and warranty are not stated on this preview. They are to confirm with SH Auto Parts.</p>
<div class="btns">{btn(enq("a part for my car"), "Send an enquiry " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div>{PVN}</div>
<aside class="side"><div class="panel photo">{pic("matte", "Matte black electric car, mood image", 700, 520, "(min-width:900px) 30vw, 100vw")}</div></aside></div></section>
<section class="sec alt"><div class="wrap narrow"><div class="sec-t"><h2>Car owner FAQ</h2></div>{faq_html(OWN_FAQ)}</div></section>'''
    shell("for-car-owners/index.html", "Parts for Car Owners | SH Auto Parts Singapore",
          "Find body parts for your China or EV car in Singapore. Tell SH Auto Parts the car and the part and we confirm fitment.",
          body, "own", [("For car owners", "for-car-owners/")], faq=OWN_FAQ, pri=0.8)

def about():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">About</p><h1>About SH Auto Parts</h1><p class="lead">A Singapore company selling China and EV car parts, mainly body parts, to workshops and car owners.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div class="prose">
<h2>Company details</h2>
<dl class="facts"><div><dt>Legal name</dt><dd>{LEGAL}</dd></div><div><dt>UEN</dt><dd>{UEN}</dd></div><div><dt>Registered</dt><dd>9 May 2024</dd></div><div><dt>Status</dt><dd>Live company</dd></div>
<div><dt>Registered address</dt><dd>{e(ADDR)}</dd></div><div><dt>Activity</dt><dd>Retail sale of spare parts and accessories for motor vehicles (SSIC 47314)</dd></div><div><dt>Tagline</dt><dd>{TAG}</dd></div></dl>
<p class="mu">Company details are as shown in public ACRA records. Phone numbers and email are from our shopfront sign. Opening hours are to confirm.</p>
<h2>What we do</h2><p>We sell mainly body parts, and some other parts, for China and EV cars. We sell in Singapore to workshops and car owners. We do not export.</p>
<h2>Brands</h2><p>Our brand board shows MG, Tesla, Maxus, Chery, BYD, GAC, XPeng, Foton, Geely, Zeekr, Omoda, Jaecoo, Denza, Deepal, Avatr and Ora. Brand names are used only to describe which vehicles a part is for. See <a href="{{{{R}}}}brands/">all brands</a>.</p>
<h2>Photos</h2><p class="mu">The shop photo is ours. Other car photos are {CRED.lower().replace("stock photos: ","stock photos from ")}: mood images, not photos of SH Auto Parts stock. The catalogue entries on this preview are samples.</p>
<div class="btns">{btn(enq("a part"), "Send an enquiry " + UI["arrow"])}{btn("{{R}}contact/", "Contact", "g")}</div>{PVN}</div>
<aside class="side"><div class="panel photo">{SHOP_IMG}</div><p class="mu">Our shop at E9 Premium, Woodlands.</p></aside></div></section>'''
    shell("about/index.html", "About SH Auto Parts | Singapore Car Parts Supplier",
          "SH AUTO PARTS PTE. LTD., UEN 202418610M, Singapore. China and EV car body parts for workshops and car owners.",
          body, "about", [("About", "about/")], pri=0.6)

def contact():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Contact</p><h1>Contact SH Auto Parts</h1><p class="lead">The quickest way is to send us your car and the part.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div class="prose">
<h2>Send an enquiry</h2><p>Use the enquiry form with your car and part, and add a photo if you can. We reply after we confirm fitment.</p>
<div class="btns">{btn(enq("a part"), "Open the enquiry form " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div>{PVN}
<h2>Details</h2>
<dl class="facts"><div><dt>Company</dt><dd>{LEGAL} (UEN {UEN})</dd></div><div><dt>Registered address</dt><dd>{e(ADDR)}</dd></div>
<div><dt>Phone</dt><dd>{"<br>".join(f'<a href="tel:{x.replace(" ","")}">{x}</a>' for x in PHONES)}</dd></div><div><dt>WhatsApp</dt><dd><a href="https://wa.me/{WA}">+65 8368 0055</a></dd></div><div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div><div><dt>Shop</dt><dd>{e(ADDR)}</dd></div><div><dt>Opening hours</dt><dd><span class="pvn">To confirm</span></dd></div></dl>
</div><aside class="side"><div class="panel photo">{SHOP_IMG}</div><p class="mu">Our shopfront at 61 Woodlands Industrial Park E9.</p></aside></div></section>'''
    shell("contact/index.html", "Contact | SH Auto Parts Singapore",
          "Contact SH Auto Parts, Singapore: send your car and part through the enquiry form. Registered address and company details.",
          body, "contact", [("Contact", "contact/")], pri=0.6)

def enquiry():
    brandopts = "".join(f'<option value="{b[0]}">{e(b[1])}</option>' for b in BRANDS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Enquiry</p><h1>Tell us the car and the part</h1><p class="lead">We confirm fitment against your car and reply.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div>
<div class="demo-note" role="note"><b>Preview note.</b> This form is a demo. Your message is saved in this browser only and is not sent anywhere yet. For a faster reply, WhatsApp us on +65 8368 0055 or call +65 8368 1155.</div>
<form class="form" id="enq-form" novalidate>
<div class="g2"><label>I am a<select name="as"><option value="workshop">Workshop</option><option value="owner">Car owner</option></select></label>
<label>Your name<input name="name" required autocomplete="name"></label></div>
<label>Phone or WhatsApp<input name="contact" required inputmode="tel" autocomplete="tel"></label>
<div class="g2"><label>Car brand<select name="brand" id="e-brand"><option value="">Choose</option>{brandopts}<option value="other">Other</option></select></label>
<label>Car model<input name="model" id="e-model" placeholder="e.g. Model Y" autocomplete="off"></label></div>
<label>Part you need<input name="part" id="e-part" required placeholder="e.g. tail lamp, left side" autocomplete="off"></label>
<label>Anything else <span class="mu">(year, damage, photo link)</span><textarea name="note" rows="4"></textarea></label>
<label class="chk"><input type="checkbox" name="consent" required><span>I agree that SH Auto Parts may use these details to reply to this enquiry. See the <a href="{{{{R}}}}privacy/">privacy notice</a>.</span></label>
<div class="err" id="enq-err" hidden>Please fill in your name, contact, the part, and tick the box.</div>
<button class="btn btn-p btn-l" type="submit">{UI["send"]} Send enquiry</button>
</form>
<div class="ok" id="enq-ok" hidden><h2>Thank you. Saved in this browser (demo).</h2><p>In the live site this goes to SH Auto Parts. For now, no message has been sent.</p><p><a class="btn btn-g" href="{{{{R}}}}catalogue/">Back to the catalogue</a></p></div>
</div><aside class="side"><div class="panel"><h3>A photo helps</h3><p class="mu">A photo of the old part, front and back for lamps, helps us match it. In the live site you can send it by WhatsApp.</p></div></aside></div></section>'''
    shell("enquiry/index.html", "Send an Enquiry | SH Auto Parts Singapore",
          "Send your car and the part you need. SH Auto Parts confirms fitment for China and EV cars and replies.",
          body, "", [("Enquiry", "enquiry/")], pri=0.6)

def privacy():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Privacy</p><h1>Privacy notice (PDPA)</h1><p class="lead">How {LEGAL} handles personal data collected on this website.</p></div></section>
<section class="sec tight"><div class="wrap narrow prose">
<h2>What we collect</h2><p>When you send an enquiry we ask for your name, a phone number or WhatsApp number, your car brand and model, the part you need and any note you add.</p>
<h2>Why we use it</h2><p>To reply to your enquiry, confirm fitment and tell you about availability. We do not use it for anything else without asking you.</p>
<h2>Preview note</h2><p>This is a preview. The enquiry form saves your message in your own browser only and does not send it to us. Staff and retention details below are to confirm before go-live.</p>
<h2>Keeping and sharing</h2><p>Retention period and any sharing with service providers: <span class="pvn">to confirm</span>.</p>
<h2>Your rights</h2><p>Under Singapore's Personal Data Protection Act you can ask to see or correct your personal data, or withdraw your consent. Send requests to <a href="mailto:shautopartspl@gmail.com">shautopartspl@gmail.com</a>. Data protection officer: <span class="pvn">to confirm</span>.</p>
<h2>Cookies and analytics</h2><p>This site stores your preferences and any staff changes in your browser. It also counts taps on WhatsApp buttons once a WhatsApp number is added. Anything further is to confirm.</p>
<p class="mu">Company: {LEGAL}, UEN {UEN}, {e(ADDR)}.</p>
</div></section>'''
    shell("privacy/index.html", "Privacy Notice | SH Auto Parts Singapore",
          "How SH AUTO PARTS PTE. LTD. handles personal data from enquiries on this website, under Singapore's PDPA.",
          body, "", [("Privacy", "privacy/")], pri=0.3)

ARTICLES = [
 ("tesla-model-y-tail-lamp-what-to-send", "Tesla Model Y tail lamp: what to send us", "Tesla Model Y Tail Lamp: What to Send | SH Auto Parts",
  "Which photos and details help us match a Tesla Model Y tail lamp, and how to describe left or right. A short checklist.", "tail",
  [("The short version", "Send the brand and model, which side you need, and two photos of the old lamp. That is usually enough for us to start checking."),
   ("1. Say left or right", "Left and right are as seen from the driver's seat, not from outside the car. If you are not sure, say where the damage is, for example &ldquo;the lamp on the side next to the fuel-side kerb&rdquo; is too vague, so a photo of the whole rear of the car is better."),
   ("2. Photograph the lamp", "Take one photo from outside the car showing the whole lamp and the area around it. If the lamp is already off the car, take a second photo of the back, where any markings or numbers are."),
   ("3. Tell us the car", "Brand, model and, if you can, the year shown on your car documents. Say if the car has been modified, repainted or has had earlier repairs to the rear."),
   ("4. Mention what else is damaged", "A broken lamp often comes with bumper or reflector damage. Tell us, so we can check the right pieces together."),
   ("What happens next", "We compare your photos with the part and confirm fitment before we reply. Lamps for the same model can differ, so we do not guess from the model name alone.")]),
 ("china-ev-body-parts-what-to-check", "Body parts for China EVs in Singapore: what to check before you buy", "China EV Body Parts: What to Check Before You Buy",
  "A buyer's checklist for body parts on China and EV cars in Singapore: model, side, sensors, paint, and what is included.", "charge",
  [("Why a checklist helps", "Body parts look similar across models, but small differences decide whether a part fits. A few checks before you pay save a return trip."),
   ("Match the exact model", "Give the brand and the model name as written on the car. Parts for two models from the same brand are often different, even when they look alike."),
   ("Check the side", "Lamps, mirrors, fenders and doors come left and right. Left and right are as seen from the driver's seat."),
   ("Sensors, cameras and holes", "If your bumper has parking sensors, a camera or other fittings, tell the seller. Ask whether the part you are buying has the same openings."),
   ("Paint and finish", "Ask whether the part is bare, primed or painted, and who matches the colour. Never assume."),
   ("What is included", "Ask whether brackets, clips, bulbs or fixings come with the part, and whether the part is new. Ask any seller about returns and warranty, and get the answer in writing. For SH Auto Parts these terms are to confirm."),
   ("Send photos", "Photos of the old part and the damaged area let the seller compare before you commit.")]),
 ("which-part-is-it", "Which part is it? Bumper, fender, reflector and trim names explained", "Car Part Names Explained: Bumper, Fender, Reflector",
  "Plain-English names for car body parts: bumper, bumper trim, fender, bonnet, tailgate, reflector, grille and more.", "head",
  [("Why names matter", "The same part can have several names. If you search or enquire with a name we also recognise, we can find it faster. Here are the common ones."),
   ("Bumper and bumper trim", "The bumper is the large piece at the front or rear of the car. Bumper trim covers the strips, lip and garnish attached to or around it. People also say bumper lip or sticker bumper."),
   ("Rear reflector", "A reflector is the red, lamp-like panel low on the rear bumper. It is not the tail lamp."),
   ("Fender and bonnet", "The fender (also called the wing) is the panel beside the front wheel. The bonnet, called the hood in some countries, is the lid over the front of the car."),
   ("Tailgate", "The tailgate is the rear lid of a hatchback or SUV. Some people say boot, trunk lid or liftgate."),
   ("Lamps", "Headlamp or headlight is at the front. Tail lamp or taillight is at the rear, and some people also say brake light. A fog lamp is a small extra lamp, usually low at the front."),
   ("Mirror, grille and arch", "The side mirror is also called a wing mirror. The grille is the vented panel at the front. The wheel arch lining is the liner inside the wheel arch."),
   ("Still not sure?", "Send a photo and the car model. We tell you the part name and check what we can find.")]),
]
def articles():
    cards = ""
    for slug, h1, title, desc, ph, secs in ARTICLES:
        cards += f'<a class="tc rv" href="{{{{R}}}}articles/{slug}/"><div class="tc-ph">{pic(ph, "Mood image", 900, 600, "(min-width:900px) 30vw, 100vw")}</div><div class="tc-b"><p class="kick">Guide</p><h3>{h1.replace("&", "&amp;")}</h3><p>{e(desc)}</p><span class="more">Read the guide {UI["arrow"]}</span></div></a>'
        paras = "".join(f"<h2>{a}</h2><p>{b}</p>" for a, b in secs)
        sch = [{"@type": "Article", "headline": h1, "description": desc, "datePublished": "2026-10-29", "dateModified": "2026-10-29",
                "author": {"@id": BASE + "/#org"}, "publisher": {"@id": BASE + "/#org"}, "image": BASE + "/og.jpg", "mainEntityOfPage": f"{BASE}/articles/{slug}/"}]
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Guide</p><h1>{h1.replace("&", "&amp;")}</h1><p class="lead">{e(desc)}</p></div></section>
<section class="sec tight"><div class="wrap two-c"><article class="prose">{paras}
<div class="btns">{btn(enq("a part"), "Send us your car and part " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div>{PVN}</article>
<aside class="side"><div class="panel photo">{pic(ph, "Mood image, not SH Auto Parts stock", 700, 520, "(min-width:900px) 30vw, 100vw")}</div></aside></div></section>'''
        shell(f"articles/{slug}/index.html", title, desc, body, "", [("Guides", "articles/"), (h1, f"articles/{slug}/")], sch, og_type="article", pri=0.6)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Guides</p><h1>Guides for buyers</h1><p class="lead">Short, practical notes on getting the right body part.</p></div></section>
<section class="sec tight"><div class="wrap"><div class="two three">{cards}</div></div></section>'''
    shell("articles/index.html", "Guides | SH Auto Parts Singapore",
          "Short guides on getting the right body part for China and EV cars in Singapore: what to send, what to check, part names.",
          body, "", [("Guides", "articles/")], pri=0.6)

def staff_page():
    r = "../"
    doc = f"""<!doctype html>
<html lang="en-SG" data-root="{r}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Staff dashboard | SH Auto Parts (demo)</title><meta name="description" content="Demo staff dashboard for SH Auto Parts.">
<meta name="robots" content="index,follow"><link rel="canonical" href="{BASE}/staff/">
<link rel="icon" href="{r}favicon.ico" sizes="48x48"><link rel="apple-touch-icon" href="{r}apple-touch-icon.png"><meta name="theme-color" content="#0A0A0C">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Saira:ital,wght@0,600;0,700;0,800;1,700;1,800&display=swap">
<link rel="stylesheet" href="{r}{asset('sh.css')}"><link rel="stylesheet" href="{r}{asset('staff.css')}">
<script>window.SH_ROOT="{r}";</script></head>
<body class="st"><div id="app"><p style="padding:40px;color:#A6A6B0">Loading staff dashboard...</p></div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="{r}{asset('data.js')}"></script><script src="{r}{asset('sh.js')}"></script><script src="{r}{asset('staff.js')}"></script>
</body></html>"""
    (OUT / "staff").mkdir(parents=True, exist_ok=True)
    (OUT / "staff/index.html").write_text(doc)

def notfound():
    body = f'''<section class="ph-hd"><div class="wrap"><p class="kick">404</p><h1>Page not found</h1><p class="lead">The page may have moved. Search the catalogue, or go to the homepage.</p></div></section>
<section class="sec tight"><div class="wrap">{search_box("nq", big=False, action="/catalogue/")}<p style="margin-top:24px"><a class="btn btn-g" href="/">Back to the homepage</a></p></div></section>'''
    shell("404.html", "Page Not Found | SH Auto Parts", "Page not found. Search the SH Auto Parts catalogue or go to the homepage.", body, index=False)

# ------------------------------------------------------------------ data.js
def datajs():
    brands = []
    for slug, name, al, models in BRANDS:
        brands.append({"slug": slug, "name": name, "aliases": al,
                       "models": [{"slug": slugify(m[0]), "name": m[0], "aka": m[1], "nb": m[2]} for m in models]})
    data = {"read": "29 Oct 2026", "base": BASE, "wa": WA, "phone": PHONE, "status": STATUS,
            "brands": brands,
            "parts": [{"slug": p[0], "name": p[1], "cat": p[2], "syn": p[3]} for p in PARTS],
            "generic": [{"w": g[0], "map": g[1]} for g in GENERIC],
            "cats": [{"slug": c[0], "name": c[1], "parts": c[3]} for c in CATS],
            "icons": IC, "entries": ENTRIES}
    (OUT / "data.js").write_text("window.SH_DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
    (HERE / "data.js").write_text((OUT / "data.js").read_text())

def statics():
    for f in ("favicon.ico", "favicon-48.png", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "og.jpg"):
        shutil.copy(HERE / "assets" / f, OUT / f)
    for f in ("sh.css", "sh.js", "staff.js", "staff.css", "wa.js"):
        shutil.copy(HERE / f, OUT / f)
    for f in ("emblem.svg", "logo.png", "logo-96.png", "shopfront.jpg"): shutil.copy(HERE / "assets" / f, OUT / f)
    (OUT / "site.webmanifest").write_text(json.dumps({"name": BRAND, "short_name": BRAND, "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#0A0A0C", "background_color": "#0A0A0C", "display": "standalone", "start_url": "./"}, indent=1))
    (OUT / f"{KEY}.txt").write_text(KEY)
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nDisallow: /staff/\n\n" + "".join(f"User-agent: {b}\nAllow: /\nDisallow: /staff/\n\n" for b in bots) + f"Sitemap: {BASE}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n" for u, pr in pages) + "</urlset>\n")
    L = [f"# {BRAND}", "", f"> {LEGAL}, Singapore (UEN {UEN}). Sells China and EV car parts, mainly body parts, to workshops and car owners in Singapore. No export. Tagline: {TAG}.", "",
         "## Facts", f"- Legal name: {LEGAL}", f"- UEN: {UEN}", "- Registered: 9 May 2024 (live company)", f"- Registered address: {ADDR}",
         "- Activity: retail sale of spare parts and accessories for motor vehicles (SSIC 47314)",
         f"- Phone: {', '.join(PHONES)} (WhatsApp {PHONES[0]})", f"- Email: {EMAIL}", "- Opening hours, prices, stock, warranty: to confirm (not published)", "",
         "## Brands (names used only to describe fitment)"] + [f"- {b[1]}: {BASE}/brands/{b[0]}/" for b in BRANDS] + \
        ["", "## Part types"] + [f"- {c[1]}: {BASE}/parts/{c[0]}/" for c in CATS] + \
        ["", "## Pages", f"- Catalogue search: {BASE}/catalogue/", f"- For workshops: {BASE}/for-workshops/", f"- For car owners: {BASE}/for-car-owners/",
         f"- Guides: {BASE}/articles/", f"- Enquiry: {BASE}/enquiry/", "", "Catalogue entries on the preview are samples. Availability and fitment are confirmed by staff on enquiry."]
    (OUT / "llms.txt").write_text("\n".join(L) + "\n")
    (OUT / "htaccess.txt").write_text(f"""# SH Auto Parts - go-live notes only (do NOT upload as .htaccess in the preview).
# Preview URL: {BASE}/ - hidden by a server header on the parent /preview/ folder; pages carry no noindex.
# At go-live:
#  1. Change BASE in build.py to the real domain and rebuild; set WA (digits with country code) and PHONE.
#  2. Add a Controller Client row for site id 'sh-auto-parts' (wa.js counter) when WA is set.
#  3. Force https + one host:
RewriteEngine On
RewriteCond %{{HTTPS}} off
RewriteRule ^ https://%{{HTTP_HOST}}%{{REQUEST_URI}} [L,R=301]
ErrorDocument 404 /404.html
<IfModule mod_headers.c>
<If "%{{REQUEST_URI}} =~ m#^/staff/#">
Header always set X-Robots-Tag "noindex, nofollow"
</If>
</IfModule>
# 4. Replace the demo staff login (PIN 2468) with a real login before any real data is entered.
# 5. Submit {BASE}/sitemap.xml to Search Console; IndexNow key file: /{KEY}.txt
""")

if __name__ == "__main__":
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    datajs()
    home(); catalogue(); parts_hub(); part_pages(); brands_hub(); brand_pages(); audience_pages(); about(); contact(); enquiry(); privacy(); articles()
    staff_page(); notfound(); statics()
    print(f"pages in sitemap {len(pages)}, entries {len(ENTRIES)}, files {sum(1 for _ in OUT.rglob('*') if _.is_file())}")
