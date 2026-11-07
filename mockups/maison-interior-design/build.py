#!/usr/bin/env python3
"""Maison Interior Design - Page One redesign mockup.

Builds a static multi-page site into ./site from the client's own photos and wording
(maisoninteriordesign.sg, read 3 Nov 2026). Images are linked from their current WordPress
uploads folder so nothing is copied or altered.

Run: python3 build.py
"""
import hashlib, html, json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site")
U = "https://maisoninteriordesign.sg/wp-content/uploads/"
BASE = "/preview/maison-interior-design/"   # preview path on pageonesingapore.com
DOMAIN = "https://maisoninteriordesign.sg"
WA = "6593391185"
PHONE = "+65 9339 1185"
EMAIL = "maisoninteriordesignsg@gmail.com"
IG = "https://www.instagram.com/maison_interiordesign/"
FB = "https://www.facebook.com/MaisonInteriorDesignSG"

# ---------------------------------------------------------------- projects
L = BASE + "img/landed/"   # landed build photos sent by the client (house number removed)
LDIM = {"landed-front.jpg": (1600, 760), "landed-volumes.jpg": (1095, 937), "landed-canopy.jpg": (1475, 700),
        "landed-gate.jpg": (1300, 470), "landed-angle.jpg": (1600, 900), "landed-side.jpg": (900, 1600), "landed-street.jpg": (1600, 900)}
P = [
 dict(slug="landed-home-holland", name="Landed Home", place="Holland", kind="Landed", type="Landed house",
      status="Completed", hero=L+"landed-front.jpg", heroL=L+"landed-front.jpg",
      gal=[L+"landed-volumes.jpg", L+"landed-canopy.jpg", L+"landed-angle.jpg", L+"landed-gate.jpg"],
      lede="A landed home built as a stack of offset grey volumes, with a deep cantilevered canopy over the car porch and a roof terrace above.",
      story=[("Layered volumes","The upper floors are set as offset boxes in two tones of grey, each stepping back to open a roof terrace. Full-height glazing in black frames brings light deep into the rooms."),
             ("A canopy that shelters","A deep cantilevered roof reaches over the car porch, so arriving in the rain stays dry. Its warm timber-look soffit softens the grey and leads you to the front door."),
             ("A calm street face","Slatted aluminium gates, louvred service doors and a stone-look boundary wall keep the frontage quiet and private, while still letting air and light through.")]),
 dict(slug="jimmy-monkey-one-north", name="Jimmy Monkey", place="One-North", kind="Commercial", type="Café",
      status="Completed", hero="Jimmy-Monkey-Completed-6-1024x775.jpg", heroL="Jimmy-Monkey-Completed-6.jpg",
      gal=["Jimmy-Monkey-Completed-7-1024x775.jpg","Jimmy-Monkey-Completed-9-1024x775.jpg",
           "Jimmy-Monkey-Completed-8-775x1024.jpg","Jimmy-Monkey-Completed-5-775x1024.jpg","Jimmy-Monkey-Completed-4-775x1024.jpg",
           "Jimmy-Monkey-Completed-3-775x1024.jpg","Jimmy-Monkey-Completed-2-775x1024.jpg","Jimmy-Monkey-Completed-1-775x1024.jpg"],
      lede="A café among the greenery of a conserved former army barracks, reworked for more seats, more light and a calmer kitchen.",
      story=[("The lounge","Long bench seating replaced the old loose tables, adding seats and turning every guest towards the greenery outside. A floor-to-window dark tinted mirror wall doubles the sense of space, while the barracks' original toilet bowl and lighting were kept as features."),
             ("Greens and pastry","To keep a small room from feeling crowded, the herb-plant drawer hides behind a tinted mirror door on the electrical box. The large coffee roaster moved elsewhere, freeing a dedicated, warmly lit pastry display on a walnut wood-grain counter."),
             ("The enclosed kitchen","A black painted headboard gives the chefs a place for daily specials. Graphite subway tiles run at varying heights, an L-shaped food pass with heat lamps speeds service, and reclaimed crate slabs keep cost down and durability up.")],
      materials=["Hafary Artisan Graphite tiles","Nippon Paint Matte Black","Admira Deep Mode Walnut laminate"]),
 dict(slug="62-havelock-road-river-place", name="River Place", place="62 Havelock Road", kind="Residential", type="Condominium",
      status="Completed", hero="62-Havelock-Road-Living-Dining-1-small-1024x683.jpg", heroL="62-Havelock-Road-Living-Dining-1-small-scaled.jpg",
      gal=["62-Havelock-Road-Living-1-small-1024x683.jpg","62-Havelock-Road-Kichen-2-small-775x1024.jpg","62-Havelock-Road-Kichen-1-small-1024x683.jpg",
           "62-Havelock-Road-Living-2-small-775x1024.jpg","62-Havelock-Road-Dining-1-small-1024x683.jpg","62-Havelock-Road-Dining-2-small-775x1024.jpg",
           "62-Havelock-Road-Toilet-1-small-775x1024.jpg","62-Havelock-Road-Toilet-2-small-775x1024.jpg"],
      lede="A riverside condominium: living, dining, kitchen and two bathrooms, completed."),
 dict(slug="teck-whye-crescent", name="Teck Whye Crescent", place="Blk 10", kind="Residential", type="HDB 3-bedroom",
      status="Completed", hero="Completed-Blk-10-Teck-Whye-1-1024x683.jpg", heroL="Completed-Blk-10-Teck-Whye-1.jpg",
      gal=["Completed-Blk-10-Teck-Whye-2-1-1024x683.jpg","Completed-Blk-10-Teck-Whye-6-775x1024.jpg","Completed-Blk-10-Teck-Whye-3-1024x683.jpg",
           "Completed-Blk-10-Teck-Whye-4-1024x683.jpg","Completed-Blk-10-Teck-Whye-5-1024x683.jpg"],
      lede="An HDB 3-bedroom flat at Teck Whye Crescent, designed and built."),
 dict(slug="yaowarat-thai-kway-chap", name="Yaowarat", place="Thai Kway Chap", kind="Commercial", type="Restaurant",
      status="Completed", hero="Yaowarat-Completed-2-1024x775.jpg", heroL="yaowarat-banner.jpg",
      gal=["Yaowarat-Completed-1-1024x775.jpg","Yaowarat-Completed-3-1024x775.jpg","Yaowarat-Completed-5-1024x775.jpg","Yaowarat-Completed-4-1024x775.jpg"],
      lede="A Thai kway chap eatery, completed."),
 dict(slug="jimmy-monkey-plq", name="Jimmy Monkey", place="Paya Lebar Quarter", kind="Commercial", type="Café",
      status="Completed", hero="JM-PLQ-Completed-Photo-3-copy-1024x682.jpg", heroL="JM-PLQ-Completed-Photo-3-copy.jpg",
      gal=["JM-PLQ-Completed-Photo-1-copy-1024x682.jpg","JM-PLQ-Completed-Photo-2-copy-1024x682.jpg","JM-PLQ-Completed-Photo-4-copy-1024x682.jpg",
           "JM-PLQ-Completed-Photo-5-copy-1024x682.jpg","JM-PLQ-Completed-Photo-6-copy-1024x682.jpg","JM-PLQ-Completed-Photo-7-copy-1024x682.jpg",
           "JM-PLQ-Completed-Photo-8-copy-1024x682.jpg"],
      lede="The second Jimmy Monkey café, at Paya Lebar Quarter, completed."),
 dict(slug="commonwealth-road", name="Commonwealth Road", place="Blk 52", kind="3D Design", type="Home, 3D visualisation",
      status="3D design", hero="52-commonwealth-3D-Living-Room-View-1-Final.jpg", heroL="52-commonwealth-3D-Master-Bedroom-View-1-Final.jpg",
      gal=["52-commonwealth-3D-Master-Bedroom-View-1-Final.jpg","52-commonwealth-3D-Kitchen-View-1-Final.jpg","52-commonwealth-3D-Master-Bedroom-View-2-Final.jpg",
           "52-commonwealth-3D-Toilet-View-1-Final.jpg","52-commonwealth-3D-Toilet-View-2-Final.jpg"],
      lede="Photo-real 3D views of the living room, kitchen, master bedroom and bathrooms, prepared before a single wall is touched."),
 dict(slug="tampines-street-22", name="Tampines Street 22", place="Blk 296", kind="3D Design", type="HDB, 3D visualisation",
      status="3D design", hero="3D-Visual-Blk-296-Tampines-St-22-3-1024x683.jpg", heroL="3D-Visual-Blk-296-Tampines-St-22-3-scaled.jpg",
      gal=["3D-Visual-Blk-296-Tampines-St-22-4-1024x683.jpg","3D-Visual-Blk-296-Tampines-St-22-2-1024x683.jpg","3D-Visual-Blk-296-Tampines-St-22-5-1024x683.jpg",
           "3D-Visual-Blk-296-Tampines-St-22-6-1-1024x683.jpg","3D-Visual-Blk-296-Tampines-St-22-1-1-1024x683.jpg"],
      lede="Six 3D visuals for an HDB home at Tampines Street 22."),
]
B = BASE + "img/bedok/"   # Bedok Reservoir photos and home-tour video sent by the client
BDIM = {'bedroom.jpg': (1600, 1066), 'bath-vanity.jpg': (1067, 1600), 'bath-niche.jpg': (1066, 1600), 'wardrobe.jpg': (1067, 1600), 'wc-niche.jpg': (1600, 899), 'garden-corner.jpg': (899, 1600), 'stone-niche.jpg': (1066, 1600), 'living-view.jpg': (1600, 899), 'flowers.jpg': (1067, 1600), 'living-doorway.jpg': (1600, 1067), 'tv-wall.jpg': (1600, 1066), 'tv-wall-angle.jpg': (1600, 1067), 'kitchen-doorway.jpg': (1066, 1600), 'entrance.jpg': (1600, 1067), 'living-bar.jpg': (1600, 1066), 'bath-cabinet.jpg': (1066, 1600), 'mirror-art.jpg': (1066, 1600), 'art-niche.jpg': (1066, 1600), 'kitchen-run.jpg': (1067, 1600), 'kitchen-sink.jpg': (1067, 1600), 'kitchen-window.jpg': (1600, 899), 'kitchen-wide.jpg': (1600, 1067), 'sofa-stone.jpg': (1600, 1067), 'dining-living.jpg': (1600, 1067), 'stone-wall.jpg': (1600, 1067), 'dining-window.jpg': (1600, 899)}
LDIM.update(BDIM)
BEDOK = dict(slug="bedok-reservoir-road", name="Bedok Reservoir", place="Blk 715", kind="Residential", type="HDB home",
      status="Completed", hero=B+"dining-living.jpg", heroL=B+"dining-living.jpg", video=B+"home-tour.mp4", poster=B+"home-tour-poster.jpg",
      gal=[B+"tv-wall-angle.jpg", B+"living-view.jpg", B+"bedroom.jpg", B+"kitchen-wide.jpg"],
      lede="A whole-home design and build at Bedok Reservoir Road: one calm palette of stone, oak and charcoal, lit so the textures do the talking.",
      story=[("A rock wall to dine by","The dining area is anchored by a full-height rock-textured feature wall, washed from above by a hidden light line. A veined stone island and table sit in front, softened by tan leather chairs."),
             ("Oak, stone and soft light","Oak-tone panelling wraps the living room and hides the doors. The TV sits on a stone-look panel framed by a warm glow, over a floating console, with herringbone flooring running through the home."),
             ("Light where you need it","Strip lights sit under every wall cabinet and inside each niche, so the kitchen, wardrobe and bathrooms read as quiet, evenly lit spaces rather than bright boxes.")],
      rooms=[("Arrival", "A lit oak niche greets you at the door, and a stone-backed console holds the first arrangement of the home.",
               ["entrance.jpg", "stone-niche.jpg", "flowers.jpg"]),
             ("Living", "Oak panelling, a framed stone-look TV wall and a planted corner by the windows, with the green view kept open.",
               ["living-doorway.jpg", "tv-wall.jpg", "living-view.jpg", "living-bar.jpg", "garden-corner.jpg"]),
             ("Dining", "A rock-textured wall, a veined stone island and a long table that links kitchen and living.",
               ["dining-living.jpg", "dining-window.jpg", "sofa-stone.jpg"]),
             ("Kitchen", "Charcoal matt base cabinets, walnut-tone uppers and a stone-look backsplash lit along its full length.",
               ["kitchen-wide.jpg", "kitchen-run.jpg", "kitchen-sink.jpg", "kitchen-window.jpg", "kitchen-doorway.jpg"]),
             ("Bedroom and wardrobe", "An oak headboard wall that doubles as a divider, a dressing area with tinted glass doors and lit shelves, and an art niche lit like a small gallery.",
               ["bedroom.jpg", "wardrobe.jpg", "art-niche.jpg"]),
             ("Bathrooms", "Slate-look tiles floor to ceiling, recessed niches with their own light, and art placed to be caught in the mirror.",
               ["wc-niche.jpg", "bath-vanity.jpg", "bath-niche.jpg", "bath-cabinet.jpg", "mirror-art.jpg"])])
P.insert(0, BEDOK)
BYSLUG = {p["slug"]: p for p in P}

STEPS = [
 ("Conceptualisation", ["Interior design and concept consultation","Space planning and layout proposal"], "52-commonwealth-3D-Master-Bedroom-View-1-Final-1280x400.jpg"),
 ("Quotation & proposal", ["Itemised renovation quotation","Perspective 3D drawing and colour proposal"], "3D-Visual-Blk-296-Tampines-St-22-2-1024x683.jpg"),
 ("Applications", ["Renovation loan application","HDB renovation permit application"], "Completed-Blk-10-Teck-Whye-3-1024x683.jpg"),
 ("Design & build", ["Additional alterations","Dedicated project management","Furnishing and decor"], "62-Havelock-Road-Kichen-1-small-1024x683.jpg"),
 ("Post project", ["2-year workmanship warranty","Post-sales service"], "Jimmy-Monkey-Completed-9-1024x775.jpg"),
]

QUOTES = [
 ("He did not over-promise and under-deliver.", "Isaac & Ee Xuan", "Denzy Gelato Café"),
 ("Always ensure the comfort of the house owner as their first priority.", "Michael", "Jimmy Monkey Café"),
]

FAQ = [
 ("Do you design HDB flats, condos, landed homes and commercial spaces?",
  "Yes. Maison Interior Design takes on residential projects, from HDB flats to condominiums, and commercial spaces such as cafés and restaurants. Our builder team also builds landed houses. Recent work includes an HDB 3-bedroom at Teck Whye, River Place condo at Havelock Road, and both Jimmy Monkey cafés."),
 ("Will I see my home before renovation starts?",
  "Yes. After the concept consultation and layout proposal, you receive an itemised quotation together with perspective 3D drawings and a colour proposal, so you can see each room before work begins."),
 ("Do you handle the HDB renovation permit and renovation loan?",
  "Yes. The team handles the HDB renovation permit application and helps with your renovation loan application as part of the process."),
 ("What happens after handover?",
  "Every project comes with a 2-year workmanship warranty and post-sales service, so you have one team to call if anything needs attention after you move in."),
]

e = html.escape

# Suppliers (Edwin approved 7 Nov 2026). Logos go in img/partners/<key>.webp|.svg|.png when available; until then the name is set in text.
SUPPLIERS = [("kdpanels", "KD Panels", "https://www.kdpanels.com/"), ("chroma", "Chroma Living", "https://chromafurnishing.com/chromaliving"),
             ("hafary", "Hafary", "https://www.hafary.com.sg/"), ("adoore", "ADOORE", "https://adoore.com.sg/"),
             ("woodorigins", "Wood Origins", "https://woodorigins.sg/"), ("stones", "Stones Selection", "https://www.stonesselection.com.sg/"),
             ("lambent", "Lambent", "https://www.lambent.sg/"), ("meerkat", "Meerkat Home", "https://www.meerkathome.sg/"),
             ("rigel", "RIGEL", "https://www.rigel-group.com/")]

def suppliers(eyebrow_cls="eyebrow"):
    from PIL import Image
    cells = []
    for k, name, url in SUPPLIERS:
        logo = ""
        for ext in ("svg", "webp", "png"):
            fp = os.path.join(HERE, "img", "partners", f"{k}.{ext}")
            if os.path.exists(fp):
                w, h = (169, 22)
                if ext != "svg":
                    with Image.open(fp) as im: w, h = im.size
                logo = f'<img src="{BASE}img/partners/{k}.{ext}" alt="{e(name)} logo" width="{w}" height="{h}" loading="lazy" decoding="async">'
                break
        inner = logo + (f'<span class="sup-n">{e(name)}</span>' if (not logo or k in ("stones", "rigel")) else "")
        cells.append(f'<li><a class="sup{" has-logo" if logo else ""} sup-{k}" href="{url}" target="_blank" rel="noopener">{inner}</a></li>')
    return (f'<section class="sec suppliers" aria-labelledby="sup-h"><div class="wrap"><p class="{eyebrow_cls} rv">Materials, flooring, lighting and furnishings</p>'
            f'<h2 class="display rv" id="sup-h">Our trusted <em>suppliers</em></h2><ul class="sup-g rv">{"".join(cells)}</ul>'
            f'<p class="sup-note rv">Maison works with these trusted Singapore suppliers for materials, flooring, lighting and furnishings.</p></div></section>')
VER = hashlib.md5(open(os.path.join(HERE, "mid.css"), "rb").read() + open(os.path.join(HERE, "mid.js"), "rb").read()).hexdigest()[:8]

def src(f):
    return f if f.startswith(("http", "/")) else U + f

def absu(f):
    return "https://pageonesingapore.com" + f if f.startswith("/") else src(f)

def img(f, alt, cls="", w=1024, h=683, lazy=True, sizes=None):
    return (f'<img src="{src(f)}" alt="{e(alt)}" width="{w}" height="{h}"'
            + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"')
            + ' referrerpolicy="no-referrer"' + (f' class="{cls}"' if cls else "") + '>')

def dims(f):
    for a, b in LDIM.items():
        if f.endswith(a): return b
    for a, b in (("775x1024", (775, 1024)), ("766x1024", (766, 1024)), ("1024x775", (1024, 775)), ("1024x682", (1024, 682))):
        if a in f: return b
    return (1024, 683)

LOGO = ('<a class="brand" href="{b}" aria-label="Maison Interior Design, home">'
        '<span class="bm">MAISON</span><span class="bs">Interior Design</span></a>').format(b=BASE)

NAV = [("portfolio/", "Portfolio"), ("services/", "Services"), ("new-launches/", "New launches"), ("about/", "About"), ("contact/", "Contact")]

def wa(text="Hi Maison Interior Design, I'd like to discuss my renovation."):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"

def head(title, desc, path, og_img, schema):
    url = DOMAIN + "/" + path
    return f"""<!doctype html><html lang="en-SG"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{('' if og_img.startswith('http') else 'https://pageonesingapore.com') + src(og_img) if og_img.startswith('/') else src(og_img)}"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f4efe8">
<link rel="icon" href="{BASE}favicon.svg" type="image/svg+xml"><link rel="icon" href="{BASE}brand/favicon-48.png" sizes="48x48" type="image/png"><link rel="apple-touch-icon" href="{BASE}brand/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400&family=Jost:wght@300;400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{BASE}mid.css?v={VER}">
<script>document.documentElement.classList.add('js')</script>
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>"""

SVC_SUB = [("bto-renovation", "BTO key collection"), ("new-condo-renovation", "New condo"), ("landed-renovation", "Landed renovation"),
           ("office-fit-out", "Office fit-out"), ("retail-shop-fit-out", "Retail shop fit-out"), ("commercial-fit-out", "Commercial fit-out")]

def header(cur, over=False):
    def nl(h, t):
        on = cur == h or (h == "portfolio/" and cur == "landed-homes/")
        a = f'<a href="{BASE}{h}"{" aria-current=page" if on else ""}>{t}</a>'
        if h == "services/":
            subs = "".join(f'<a href="{BASE}services/{sl}/">{st}</a>' for sl, st in SVC_SUB)
            return f'<span class="nav-g">{a}<span class="nav-sub"><a class="sub-all" href="{BASE}services/">All services</a>{subs}</span></span>'
        if h == "portfolio/":
            return (f'<span class="nav-g">{a}<span class="nav-sub"><a class="sub-all" href="{BASE}portfolio/">All projects</a>'
                    f'<a href="{BASE}portfolio/bedok-reservoir-road/">Bedok Reservoir</a><a href="{BASE}landed-homes/">Landed homes</a></span></span>')
        return a
    links = "".join(nl(h, t) for h, t in NAV)
    return f"""<body class="{'over' if over else 'solid'}"><a class="skip" href="#main">Skip to content</a>
<header class="hd" id="hd"><div class="wrap hd-in">{LOGO}
<nav class="nav" id="nav" aria-label="Main">{links}<a class="nav-cta" href="{wa()}" data-cta="whatsapp">Book a consultation</a></nav>
<button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span></button></div></header>
<main id="main">"""

def cta_block():
    return f"""<section class="cta dark"><div class="wrap cta-in rv">
<p class="eyebrow">Start your dream home with us</p>
<h2 class="display">So tell us,<br><em>what's your story?</em></h2>
<p class="cta-p">Send your floor plan and a few photos you love. Roland and the team will come back with ideas, a layout and an honest, itemised quote.</p>
<div class="btns"><a class="btn light" href="{wa()}" data-cta="whatsapp">WhatsApp {PHONE}</a><a class="btn ghost-l" href="{BASE}contact/">Send your floor plan</a></div>
</div></section>"""

def footer():
    links = "".join(f'<a href="{BASE}{h}">{t}</a>' for h, t in NAV[:1] + [("landed-homes/", "Landed Homes")] + NAV[1:])
    return f"""</main><footer class="ft"><div class="wrap ft-in">
<div class="ft-a">{LOGO}<p>Residential and commercial interior design, and landed house building, in Singapore since 2018.</p></div>
<div class="ft-b"><h3>Studio</h3>{links}</div>
<div class="ft-c"><h3>Talk to us</h3><p>Roland Ng, Managing Director</p><a href="tel:+{WA}">{PHONE}</a><a href="mailto:{EMAIL}">{EMAIL}</a>
<p class="soc"><a href="{IG}" rel="noopener">Instagram</a><a href="{FB}" rel="noopener">Facebook</a><a href="{wa()}">WhatsApp</a></p></div>
</div><div class="wrap ft-legal"><span>© 2026 Maison Interior Design</span><span>Redesign concept by Page One Singapore</span></div></footer>
<a class="fab" href="{wa()}" data-cta="whatsapp" aria-label="WhatsApp Maison Interior Design"><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg></a>
<div class="vm" id="vm" hidden role="dialog" aria-modal="true" aria-label="Home tour video"><button class="vm-x" aria-label="Close video">×</button><video controls playsinline preload="none"></video></div>
<script src="{BASE}mid.js?v={VER}" defer></script></body></html>"""

ORG = {"@type": "HomeAndConstructionBusiness", "@id": DOMAIN + "/#business", "name": "Maison Interior Design",
       "url": DOMAIN + "/", "telephone": PHONE, "email": EMAIL, "foundingDate": "2018",
       "areaServed": {"@type": "Country", "name": "Singapore"}, "image": U + "Jimmy-Monkey-Completed-6.jpg",
       "founder": {"@type": "Person", "name": "Roland Ng", "jobTitle": "Managing Director"},
       "sameAs": [IG, FB]}

def faq_schema():
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i+1, "name": n, "item": DOMAIN + "/" + u} for i, (n, u) in enumerate(items)]}

def faq_html():
    rows = "".join(f'<details class="qa rv"><summary><h3>{e(q)}</h3><span class="pm" aria-hidden="true"></span></summary><p>{e(a)}</p></details>' for q, a in FAQ)
    return f'<section class="sec faq"><div class="wrap narrow"><p class="eyebrow rv">Good to know</p><h2 class="display rv">Questions homeowners ask us</h2>{rows}</div></section>'

def card(p, cls="pc"):
    w, h = dims(p["hero"])
    return (f'<a class="{cls} rv" href="{BASE}portfolio/{p["slug"]}/" data-kind="{e(p["kind"])}">'
            f'<figure>{img(p["hero"], p["name"] + " " + p["place"] + ", " + p["type"].lower(), w=w, h=h)}</figure>'
            f'<div class="pc-t"><span class="tag">{e(p["kind"])} · {e(p["type"])}</span><h3>{e(p["name"])} <em>{e(p["place"])}</em></h3>'
            f'<span class="more">View project</span></div></a>')

def write(path, s):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f: f.write(s)

HOUSE = ('<svg class="house" viewBox="0 0 520 340" fill="none" stroke="currentColor" stroke-width="1.2" aria-hidden="true">'
 '<path d="M20 320h480"/><path d="M60 320V150h400v170"/><path d="M40 150h440"/><path d="M60 150l40-50h320l40 50"/>'
 '<path d="M90 100V60h200v40"/><path d="M80 60h220"/><path d="M110 75h160"/>'
 '<rect x="95" y="190" width="90" height="70"/><path d="M140 190v70M95 225h90"/>'
 '<rect x="215" y="190" width="90" height="130"/><path d="M260 190v130"/>'
 '<rect x="335" y="190" width="90" height="70"/><path d="M380 190v70M335 225h90"/>'
 '<rect x="120" y="70" width="40" height="22"/><rect x="220" y="70" width="40" height="22"/>'
 '<path d="M20 335h480" stroke-dasharray="3 6" opacity=".6"/><path d="M60 330v10M460 330v10" opacity=".6"/></svg>')

def landed_band():
    return f"""<section class="sec landed dark"><div class="wrap landed-in"><div class="landed-t">
<p class="eyebrow rv">Builder</p><h2 class="display rv">Building a <em>landed home?</em></h2>
<p class="rv">Beyond interiors, our builder team mainly builds landed houses. One team from the structure to the last cabinet, so the house and the interior are planned together from day one.</p>
<a class="btn light rv" href="{BASE}landed-homes/">Landed house building</a></div>
<a class="landed-art rv" href="{BASE}portfolio/landed-home-holland/"><figure class="la-main">{img(L+"landed-volumes.jpg", "Landed home by Maison: offset grey volumes and roof terrace", w=1095, h=937)}</figure>
<figure class="la-inset">{img(L+"landed-canopy.jpg", "Cantilevered canopy over the car porch", w=1475, h=700)}</figure>
<span class="la-cap">Featured build · Holland</span></a></div></section>"""

def landed():
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("Landed Homes", "landed-homes/")]),
              {"@type": "Service", "name": "Landed house building", "serviceType": "Landed house construction and interior design", "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "Country", "name": "Singapore"}}]}
    s = head("Landed House Builder Singapore | Design & Build | Maison Interior Design",
             "Maison Interior Design's builder team mainly builds landed houses in Singapore, with the interior planned together with the build by one team.",
             "landed-homes/", L+"landed-front.jpg", schema)
    s += header("landed-homes/", over=True)
    s += f"""<section class="phero lhero">{img(L+"landed-front.jpg", "Landed house with cantilevered canopy, built by Maison", "kb", 1600, 760, lazy=False)}<div class="hero-shade"></div>
<div class="wrap phero-in"><p class="eyebrow light">Landed homes · Design &amp; build</p><h1 class="display hero-h">House and interior, <em>built as one</em></h1>
<p class="hero-p">Alongside residential and commercial interiors, our builder team mainly builds landed houses in Singapore.</p>
<div class="btns"><a class="btn light" href="{wa("Hi Maison, I'd like to discuss building a landed house.")}" data-cta="whatsapp">Discuss your landed home</a><a class="btn ghost-l" href="#featured">See a recent build</a></div></div></section>
<section class="sec tight"><div class="wrap"><div class="why">
<div class="rv"><span class="sn">01</span><h3>One team, start to finish</h3><p>The people who build the house also design and fit out the interior, so nothing is lost between contractor and designer.</p></div>
<div class="rv"><span class="sn">02</span><h3>Interior planned early</h3><p>Layouts, storage and lighting are decided with the structure, not squeezed in after the walls are up.</p></div>
<div class="rv"><span class="sn">03</span><h3>See it first in 3D</h3><p>Perspective 3D drawings and a colour proposal let you walk through the house before work starts.</p></div>
<div class="rv"><span class="sn">04</span><h3>Dedicated project management</h3><p>One point of contact on site, an itemised quotation and post-sales service after handover.</p></div></div></div></section>
<section class="sec feat" id="featured"><div class="wrap">
<div class="sec-h"><div><p class="eyebrow rv">Featured build · Holland</p><h2 class="display rv">Three moves that <em>shape the house</em></h2></div>
<a class="link rv" href="{BASE}portfolio/landed-home-holland/">View the full project</a></div>
<div class="feat-g">
<figure class="fg-a rv">{img(L+"landed-volumes.jpg", "Offset grey volumes with full-height glazing and roof terrace", w=1095, h=937)}<figcaption><span class="sn">01</span><b>Layered volumes</b>Offset boxes in two greys step back to open a roof terrace.</figcaption></figure>
<figure class="fg-b rv">{img(L+"landed-canopy.jpg", "Deep cantilevered canopy with timber-look soffit", w=1475, h=700)}<figcaption><span class="sn">02</span><b>A canopy that shelters</b>A deep cantilever keeps the car porch dry; the warm soffit leads you in.</figcaption></figure>
<figure class="fg-c rv">{img(L+"landed-gate.jpg", "Slatted aluminium gate and stone-look boundary wall", w=1300, h=470)}<figcaption><span class="sn">03</span><b>A calm street face</b>Slatted gates and a stone-look wall: private, but never closed in.</figcaption></figure>
</div></div></section>
{cta_block()}"""
    s += footer()
    write("landed-homes/index.html", s)

# ---------------------------------------------------------------- home
def home():
    slides = [(B+"dining-living.jpg", "Stone and oak", "Bedok Reservoir, completed home", "bedok-reservoir-road"),
              ("Jimmy-Monkey-Completed-7.jpg", "Effortless style", "Jimmy Monkey, One-North", "jimmy-monkey-one-north"),
              ("62-Havelock-Road-Living-Dining-1-small-scaled.jpg", "Space consciousness", "River Place, Havelock Road", "62-havelock-road-river-place")]
    sl = "".join(f'<div class="slide{" on" if i==0 else ""}" data-cap="{e(c)}" data-href="{BASE}portfolio/{s}/">{img(f, c, "kb", 1600, 1067, lazy=i>0)}</div>' for i, (f, t, c, s) in enumerate(slides))
    dots = "".join(f'<button class="hdot{" on" if i==0 else ""}" aria-label="Show {e(c)}"><i></i></button>' for i, (f, t, c, s) in enumerate(slides))
    feat = [BYSLUG[s] for s in ("bedok-reservoir-road", "landed-home-holland", "62-havelock-road-river-place", "jimmy-monkey-one-north")]
    grid = "".join(card(p, "pc f%d" % i) for i, p in enumerate(feat))
    strip = []
    for p in P:
        for f in p["gal"][:3]:
            w, h = dims(f)
            strip.append(f'<li><a href="{BASE}portfolio/{p["slug"]}/" draggable="false">{img(f, p["name"] + " " + p["place"], w=w, h=h)}<span>{e(p["name"])} · {e(p["place"])}</span></a></li>')
    svc = [("Residential", "HDB flats and condominiums, planned around how you actually live: storage, light and flow first, then the finishes.", "62-Havelock-Road-Living-1-small-1024x683.jpg", "residential"),
           ("Commercial", "Cafés, restaurants and offices that work hard for the owner and feel easy for the customer, delivered to schedule.", "JM-PLQ-Completed-Photo-1-copy-1024x682.jpg", "commercial"),
           ("3D design", "Perspective 3D drawings and a colour proposal for every room, so you approve the look before work begins.", "3D-Visual-Blk-296-Tampines-St-22-5-1024x683.jpg", "3d-design")]
    svch = "".join(f'<a class="svc rv" href="{BASE}services/#{a}"><figure>{img(f, t + " interior design")}</figure><span class="num">0{i+1}</span><h3>{t}</h3><p>{d}</p><span class="more">More details</span></a>' for i, (t, d, f, a) in enumerate(svc))
    steps = "".join(f'<li class="rv"><span class="sn">0{i+1}</span><h3>{t}</h3><ul>{"".join("<li>"+e(x)+"</li>" for x in b)}</ul></li>' for i, (t, b, f) in enumerate(STEPS))
    qs = "".join(f'<figure class="q{" on" if i==0 else ""}"><blockquote>“{e(q)}”</blockquote><figcaption><b>{e(n)}</b>{e(c)}</figcaption></figure>' for i, (q, n, c) in enumerate(QUOTES))
    jm = BYSLUG["jimmy-monkey-one-north"]
    schema = {"@context": "https://schema.org", "@graph": [ORG, faq_schema()]}
    s = head("Interior Designer Singapore | HDB, Condo & Commercial | Maison Interior Design",
             "Maison Interior Design plans, designs and builds HDB flats, condos, cafés and offices in Singapore. 3D drawings before work starts, 2-year workmanship warranty. Since 2018.",
             "", "Jimmy-Monkey-Completed-6.jpg", schema)
    s += header("", over=True)
    s += f"""<section class="hero" id="hero"><div class="slides">{sl}</div><div class="hero-shade"></div>
<div class="wrap hero-in"><p class="eyebrow light">Interior design &amp; build · Singapore · Since 2018</p>
<h1 class="display hero-h">Interior design for homes and cafés in Singapore, <em>made to be lived in.</em></h1>
<p class="hero-p">HDB flats, condominiums and commercial spaces, designed in 3D and built by one dedicated team.</p>
<div class="btns"><a class="btn light" href="{BASE}portfolio/">View our work</a><a class="btn ghost-l" href="{wa()}" data-cta="whatsapp">WhatsApp us</a></div></div>
<div class="wrap hero-foot"><a class="cap" id="cap" href="{BASE}portfolio/{slides[0][3]}/">{e(slides[0][2])}</a><div class="hdots">{dots}</div></div></section>

<section class="sec intro"><div class="wrap intro-in">
<p class="eyebrow rv">The studio</p>
<p class="lead rv">Maison Interior Design was formed in 2018 to make a reality of the homes, commercial spaces and offices our clients picture. We seek out exclusive materials and textures, and we stay hands-on, on site, until the last detail is right.</p>
<ul class="facts rv"><li><b>2018</b><span>Founded</span></li><li><b>3D</b><span>Every room drawn before work starts</span></li><li><b>2 yrs</b><span>Workmanship warranty</span></li><li><b>HDB</b><span>Renovation permit handled for you</span></li></ul>
</div></section>

<section class="sec bedok"><div class="wrap bk-in">
<div class="bk-art rv"><a class="bk-main" href="{BASE}portfolio/bedok-reservoir-road/">{img(B+"stone-wall.jpg", "Rock-textured feature wall and veined stone dining table, Bedok Reservoir home", w=1600, h=1067)}</a>
<button class="bk-vid" type="button" data-video="{B}home-tour.mp4" data-poster="{B}home-tour-poster.jpg" aria-label="Play the Bedok Reservoir home tour video, 1 minute 22 seconds"><video muted loop playsinline autoplay preload="metadata" poster="{B}home-tour-poster.jpg" width="360" height="636"><source src="{B}tour-teaser.mp4" type="video/mp4"></video><span class="bk-play"><i></i>Tour · 1:22</span></button></div>
<div class="bk-t"><p class="eyebrow rv">Featured home · Bedok Reservoir</p><h2 class="display rv">Stone, oak and <em>quiet light</em></h2>
<p class="rv">A whole home built around one palette: a rock-textured dining wall, oak panelling, charcoal cabinetry and light tucked into every niche.</p>
<div class="bk-d rv"><a href="{BASE}portfolio/bedok-reservoir-road/#kitchen">{img(B+"kitchen-sink.jpg", "Lit stone-look backsplash and black sink", w=1067, h=1600)}<span>Kitchen</span></a><a href="{BASE}portfolio/bedok-reservoir-road/#bathrooms">{img(B+"bath-vanity.jpg", "Slate-look bathroom with lit niche", w=1067, h=1600)}<span>Bath</span></a><a href="{BASE}portfolio/bedok-reservoir-road/#bedroom">{img(B+"wardrobe.jpg", "Dressing area with tinted glass doors", w=1067, h=1600)}<span>Wardrobe</span></a></div>
<div class="bk-a rv"><a class="btn dark-b" href="{BASE}portfolio/bedok-reservoir-road/">See the home</a><button class="link" type="button" data-video="{B}home-tour.mp4" data-poster="{B}home-tour-poster.jpg">Watch the home tour</button></div></div></div></section>

<section class="sec works"><div class="wrap"><div class="sec-h"><div><p class="eyebrow rv">Selected works</p><h2 class="display rv">Spaces we have <em>shaped</em></h2></div>
<a class="link rv" href="{BASE}portfolio/">View all projects</a></div>
<div class="fgrid">{grid}</div></div></section>

<section class="sec reel" aria-label="Project photos"><div class="wrap"><p class="eyebrow rv">From site</p><h2 class="display rv">Details, <em>up close</em></h2></div>
<div class="marq" id="marq"><ul class="track" id="track">{"".join(strip)}</ul></div></section>

<section class="sec svcs"><div class="wrap"><div class="sec-h"><div><p class="eyebrow rv">What we do</p><h2 class="display rv">Design, then build. <em>One team.</em></h2></div></div>
<div class="svc-g">{svch}</div></div></section>

{landed_band()}
<section class="sec process dark"><div class="wrap"><div class="sec-h"><div><p class="eyebrow rv">How we work</p><h2 class="display rv">Five steps from <em>first idea</em> to keys in hand</h2></div>
<a class="link light rv" href="{BASE}services/">See the full process</a></div><ol class="steps">{steps}</ol></div></section>

<section class="sec story"><div class="wrap story-in">
<figure class="story-img rv">{img("Jimmy-Monkey-Completed-7-1024x775.jpg", "Jimmy Monkey One-North pastry counter and herb shelves", w=1024, h=775)}</figure>
<div class="story-t"><p class="eyebrow rv">Project story · Jimmy Monkey, One-North</p>
<h2 class="display rv">A barracks café, <em>opened up to the greenery</em></h2>
<p class="rv">{e(jm["story"][0][1])}</p>
<ul class="mat rv">{"".join("<li>"+e(m)+"</li>" for m in jm["materials"])}</ul>
<a class="btn dark-b rv" href="{BASE}portfolio/{jm["slug"]}/">Read the project</a></div></div></section>

<section class="sec quotes"><div class="wrap narrow"><p class="eyebrow rv">What clients say</p><div class="qs rv" id="qs">{qs}</div>
<div class="qnav"><button class="qb" id="qprev" aria-label="Previous review">←</button><button class="qb" id="qnext" aria-label="Next review">→</button></div></div></section>

{faq_html()}
<section class="sec tight nl-band"><div class="wrap nl-band-in"><div><p class="eyebrow">New launches · 2026 to 2027</p><h2 class="display">Collecting keys <em>soon?</em></h2>
<p>Guides for new BTO, condo, landed, office and shop projects: what to check at handover, the rules and a realistic timeline.</p></div>
<div class="btns"><a class="btn dark-b" href="{BASE}new-launches/">See new launches</a><a class="btn ghost-d" href="{BASE}services/bto-renovation/">BTO key collection guide</a></div></div></section>
{suppliers()}
{cta_block()}"""
    s += footer()
    write("index.html", s)

# ---------------------------------------------------------------- portfolio
def portfolio():
    chips = "".join(f'<button class="chip{" on" if k=="All" else ""}" data-f="{k}" aria-pressed="{"true" if k=="All" else "false"}">{k}</button>' for k in ("All", "Landed", "Residential", "Commercial", "3D Design"))
    grid = "".join(card(p) for p in P)
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("Portfolio", "portfolio/")]),
              {"@type": "CollectionPage", "name": "Interior design portfolio", "hasPart": [{"@type": "CreativeWork", "name": p["name"] + " " + p["place"], "url": DOMAIN + "/portfolio/" + p["slug"] + "/"} for p in P]}]}
    s = head("Interior Design Portfolio Singapore | HDB, Condo & Café Projects | Maison",
             "Completed HDB, condominium, café and restaurant interiors by Maison Interior Design, plus 3D design visuals. See Jimmy Monkey, River Place, Teck Whye and more.",
             "portfolio/", "Jimmy-Monkey-Completed-6.jpg", schema)
    s += header("portfolio/")
    s += f"""<section class="phead"><div class="wrap"><p class="eyebrow">Portfolio</p><h1 class="display">Homes, cafés <em>and everything between</em></h1>
<p class="ph-p">Completed residential and commercial projects, and the 3D designs that come before every build.</p>
<div class="chips" role="group" aria-label="Filter projects">{chips}</div>
<a class="ph-landed" href="{BASE}landed-homes/"><span class="eyebrow">Builder</span>Building a landed home? See how we design and build landed houses <b>→</b></a></div></section>
<section class="sec tight"><div class="wrap"><div class="pgrid" id="pgrid">{grid}</div></div></section>{cta_block()}"""
    s += footer()
    write("portfolio/index.html", s)

def project(i, p):
    nxt = P[(i + 1) % len(P)]
    gal = "".join(f'<a class="g rv" href="{src(f)}" data-lb>{img(f, p["name"] + " " + p["place"] + ", photo " + str(j+2), w=dims(f)[0], h=dims(f)[1])}</a>' for j, f in enumerate(p["gal"]))
    story = ""
    if p.get("story"):
        story = '<div class="pstory">' + "".join(f'<div class="ps rv"><span class="sn">0{k+1}</span><h2>{e(t)}</h2><p>{e(x)}</p></div>' for k, (t, x) in enumerate(p["story"])) + "</div>"
    rooms_html = ""
    if p.get("rooms"):
        n = 1
        parts = []
        for k, (t, x, fs) in enumerate(p["rooms"]):
            figs = []
            for j, f in enumerate(fs):
                w, h = dims(f)
                figs.append(f'<a class="g rv{" wide" if j == 0 and w > h else ""}{" tall" if h > w else ""}" href="{B+f}" data-lb>{img(B+f, p["name"] + " " + t.lower() + ", photo " + str(n), w=w, h=h)}</a>')
                n += 1
            parts.append(f'<section class="room" id="{t.split()[0].lower()}"><div class="room-h rv"><span class="sn">{k+1:02d}</span><h2 class="display">{e(t)}</h2><p>{e(x)}</p></div><div class="rgal n{len(fs)}">{"".join(figs)}</div></section>')
        idx = "".join(f'<a href="#{t.split()[0].lower()}">{e(t)}</a>' for t, x, fs in p["rooms"])
        rooms_html = f'<section class="sec tight rooms"><div class="wrap"><nav class="room-idx rv" aria-label="Rooms">{idx}</nav>{"".join(parts)}</div></section>'
    video_html = ""
    if p.get("video"):
        video_html = f'''<section class="sec tour dark" id="tour"><div class="wrap tour-in"><div class="tour-v rv"><video controls preload="none" playsinline poster="{p["poster"]}" width="480" height="848"><source src="{p["video"]}" type="video/mp4"></video></div>
<div class="tour-t"><p class="eyebrow rv">Home tour</p><h2 class="display rv">Walk through <em>the finished home</em></h2><p class="rv">A 1-minute 22-second tour, room by room, from the foyer to the bedroom, explaining what was changed and why.</p>
<a class="btn light rv" href="{wa("Hi Maison, I watched the Bedok Reservoir home tour and would like to discuss my home.")}" data-cta="whatsapp">Talk to us about your home</a></div></div></section>'''
    mats = f'<div class="pmeta-row"><dt>Materials</dt><dd>{"<br>".join(e(m) for m in p["materials"])}</dd></div>' if p.get("materials") else ""
    title = f'{p["name"]} {p["place"]}'
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("Portfolio", "portfolio/"), (title, "portfolio/" + p["slug"] + "/")]),
              {"@type": "CreativeWork", "name": title, "about": p["type"], "creator": {"@id": DOMAIN + "/#business"}, "image": [absu(p["heroL"])] + [absu(f) for f in p["gal"][:4]]}]
              + ([{"@type": "VideoObject", "name": title + " home tour", "description": "Room-by-room tour of the finished home by Maison Interior Design.", "thumbnailUrl": absu(p["poster"]), "contentUrl": absu(p["video"]), "uploadDate": "2026-11-03", "duration": "PT1M22S"}] if p.get("video") else [])}
    s = head(f'{title} | {p["type"]} Interior Design | Maison Interior Design',
             f'{p["lede"]} {p["kind"]} interior project by Maison Interior Design, Singapore.'[:158],
             f'portfolio/{p["slug"]}/', p["heroL"], schema)
    s += header("portfolio/", over=True)
    s += f"""<section class="phero">{img(p["heroL"], title, "kb", 1600, 1067, lazy=False)}<div class="hero-shade"></div>
<div class="wrap phero-in"><nav class="bc" aria-label="Breadcrumb"><a href="{BASE}">Home</a><span>/</span><a href="{BASE}portfolio/">Portfolio</a></nav>
<p class="eyebrow light">{e(p["kind"])} · {e(p["type"])}</p><h1 class="display hero-h">{e(p["name"])} <em>{e(p["place"])}</em></h1></div></section>
<section class="sec tight"><div class="wrap pintro">
<p class="lead rv">{e(p["lede"])}</p>
<dl class="pmeta rv"><div class="pmeta-row"><dt>Type</dt><dd>{e(p["type"])}</dd></div><div class="pmeta-row"><dt>Scope</dt><dd>{"Design &amp; build" if p["status"]=="Completed" else "3D design &amp; visualisation"}</dd></div>
<div class="pmeta-row"><dt>Status</dt><dd>{e(p["status"])}</dd></div>{mats}</dl></div>{('<div class="wrap">'+story+'</div>') if story else ''}</section>
{video_html}{rooms_html or f'<section class="sec tight"><div class="wrap"><div class="gal">{gal}</div></div></section>'}
<section class="next"><a href="{BASE}portfolio/{nxt["slug"]}/" class="next-a">{img(nxt["hero"], nxt["name"], w=dims(nxt["hero"])[0], h=dims(nxt["hero"])[1])}<span class="next-t"><span class="eyebrow light">Next project</span><b class="display">{e(nxt["name"])} <em>{e(nxt["place"])}</em></b></span></a></section>
{cta_block()}
<div class="lb" id="lb" hidden><button class="lb-x" aria-label="Close">×</button><button class="lb-p" aria-label="Previous">←</button><img alt=""><button class="lb-n" aria-label="Next">→</button></div>"""
    s += footer()
    write(f'portfolio/{p["slug"]}/index.html', s)

# ---------------------------------------------------------------- services
def services():
    svc = [("residential", "Residential interior design", "HDB flats and condominiums", "62-Havelock-Road-Living-1-small-1024x683.jpg",
            "From a 3-room HDB flat at Teck Whye to a riverside condo at Havelock Road, we plan every room around storage, light and the way your household moves, then carry the design through to build.",
            ["Concept consultation and space planning", "3D views of every room before work starts", "HDB renovation permit and renovation loan applications", "Carpentry, alterations, furnishing and decor"]),
           ("commercial", "Commercial interior design", "Cafés, restaurants and offices", "JM-PLQ-Completed-Photo-2-copy-1024x682.jpg",
            "Commercial spaces have to earn their keep. We design for seating counts, staff workflow and the customer's first impression, and we keep the build on schedule so you open on time.",
            ["Layouts for seating, counters and kitchen flow", "Feature walls, lighting and display design", "Dedicated project management to opening day", "No hidden costs in an itemised quotation"]),
           ("3d-design", "3D design and visualisation", "See it before it is built", "52-commonwealth-3D-Kitchen-View-1-Final.jpg",
            "Every proposal comes with perspective 3D drawings and a colour proposal, so you can change a cabinet, a tile or a colour on screen instead of on site.",
            ["Perspective 3D drawings room by room", "Colour and material proposal", "Revisions before quotation is final", "Drawings reused by the build team on site"]),
           ("landed", "Landed house building", "Our builder team", "62-Havelock-Road-Living-Dining-1-small-1024x683.jpg",
            "Our builder team mainly builds landed houses. Because the same team designs the interior, the house and the rooms inside it are planned together from the start.",
            ["House and interior by one team", "Interior planned alongside the structure", "3D drawings before work starts", "Dedicated project management"])]
    blocks = "".join(f"""<article class="sblock rv" id="{a}"><figure>{img(f, t)}</figure><div><p class="eyebrow">0{i+1} · {e(sub)}</p><h2 class="display">{e(t)}</h2><p>{e(d)}</p>
<ul class="ticks">{"".join("<li>"+e(x)+"</li>" for x in l)}</ul>{('<a class="link" href="'+BASE+'landed-homes/">More on landed homes</a>') if a=="landed" else ('<a class="link" href="'+wa("Hi Maison, I'd like to ask about " + t.lower() + ".")+'" data-cta="whatsapp">Ask about '+e(t.lower())+'</a>')}</div></article>""" for i, (a, t, sub, f, d, l) in enumerate(svc))
    steps = "".join(f'<li class="pstep rv"><figure>{img(f, t)}</figure><div><span class="sn">0{i+1}</span><h3>{e(t)}</h3><ul>{"".join("<li>"+e(x)+"</li>" for x in b)}</ul></div></li>' for i, (t, b, f) in enumerate(STEPS))
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("Services", "services/")]), faq_schema(),
              {"@type": "HowTo", "name": "How a renovation with Maison Interior Design works", "step": [{"@type": "HowToStep", "position": i+1, "name": t, "text": "; ".join(b)} for i, (t, b, f) in enumerate(STEPS)]}]}
    s = head("Interior Design Services Singapore | HDB, Condo, Commercial & 3D | Maison",
             "Residential and commercial interior design and build in Singapore: concept, 3D drawings, itemised quotation, HDB permit, project management and a 2-year workmanship warranty.",
             "services/", "52-commonwealth-3D-Kitchen-View-1-Final.jpg", schema)
    s += header("services/")
    s += f"""<section class="phead"><div class="wrap"><p class="eyebrow">Services</p><h1 class="display">Interior design and build, <em>start to finish</em></h1>
<p class="ph-p">One team takes your home or business from first sketch to handover, then stays on call for two years after.</p></div></section>
<section class="sec tight"><div class="wrap sblocks">{blocks}</div></section>
<section class="sec dark"><div class="wrap"><p class="eyebrow rv">The process</p><h2 class="display rv">Five steps, <em>no surprises</em></h2><ol class="psteps">{steps}</ol></div></section>
{faq_html()}{cta_block()}"""
    s += footer()
    write("services/index.html", s)

# ---------------------------------------------------------------- about
def about():
    qs = "".join(f'<figure class="aq rv"><blockquote>“{e(q)}”</blockquote><figcaption><b>{e(n)}</b>{e(c)}</figcaption></figure>' for q, n, c in QUOTES)
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("About", "about/")]), {"@type": "AboutPage", "about": {"@id": DOMAIN + "/#business"}}]}
    s = head("About Maison Interior Design | Singapore Interior Designers Since 2018",
             "Maison Interior Design was founded in 2018 by Managing Director Roland Ng to design and build homes, commercial spaces and offices across Singapore.",
             "about/", "Jimmy-Monkey-Completed-8-775x1024.jpg", schema)
    s += header("about/")
    s += f"""<section class="phead"><div class="wrap"><p class="eyebrow">About</p><h1 class="display">Never settle. <em>Ever improving.</em></h1></div></section>
<section class="sec tight"><div class="wrap about-in">
<figure class="rv">{img("Jimmy-Monkey-Completed-8-775x1024.jpg", "Jimmy Monkey café interior by Maison Interior Design", w=775, h=1024)}</figure>
<div><p class="lead rv">Maison Interior Design was formed in 2018 to make a reality of the house, commercial space or office you have in mind. We love designing, we are adventurous about it, and we take pride in every space we build.</p>
<p class="rv">Rooted in residential and commercial design and project management, we are bold enough to look for exclusive materials and textures, and practical enough to be on site, hands-on, until the job is done. Strategic brainstorming at the start, careful work on site, and an honest itemised quote throughout.</p>
<div class="person rv"><b>Roland Ng</b><span>Managing Director</span><a href="{wa("Hi Roland, I'd like to discuss my renovation.")}" data-cta="whatsapp">WhatsApp Roland</a></div></div></div></section>
<section class="sec values dark"><div class="wrap vals"><div class="rv"><span class="sn">01</span><h3>Effortless luxury</h3><p>Materials and textures chosen with care, so a space feels considered without feeling fussy.</p></div>
<div class="rv"><span class="sn">02</span><h3>Effortless style</h3><p>A clear concept, carried through from the first 3D view to the last fitting.</p></div>
<div class="rv"><span class="sn">03</span><h3>Space consciousness</h3><p>Every centimetre planned, from hidden storage to mirror walls that double a room.</p></div></div></section>
<section class="sec"><div class="wrap"><p class="eyebrow rv">In their words</p><div class="aqs">{qs}</div></div></section>{suppliers()}{cta_block()}"""
    s += footer()
    write("about/index.html", s)

# ---------------------------------------------------------------- contact
def contact():
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("Contact", "contact/")]), {"@type": "ContactPage", "about": {"@id": DOMAIN + "/#business"}}]}
    s = head("Contact Maison Interior Design | Book an Interior Design Consultation",
             "WhatsApp or call Roland Ng on +65 9339 1185, email the studio, or send your floor plan for an interior design consultation in Singapore.",
             "contact/", "62-Havelock-Road-Living-Dining-1-small-1024x683.jpg", schema)
    s += header("contact/")
    s += f"""<section class="phead"><div class="wrap"><p class="eyebrow">Contact</p><h1 class="display">Let's talk about <em>your space</em></h1>
<p class="ph-p">The fastest way is WhatsApp. Send your floor plan and a few photos you like, and we will reply with first ideas.</p></div></section>
<section class="sec tight"><div class="wrap contact-in">
<div class="cinfo rv"><a class="cbig" href="{wa()}" data-cta="whatsapp"><span class="eyebrow">WhatsApp</span><b>{PHONE}</b></a>
<a class="cbig" href="tel:+{WA}" data-cta="call"><span class="eyebrow">Call</span><b>{PHONE}</b></a>
<a class="cbig" href="mailto:{EMAIL}"><span class="eyebrow">Email</span><b class="sm">{EMAIL}</b></a>
<p class="person"><b>Roland Ng</b><span>Managing Director</span></p></div>
<form class="cform rv" id="cform"><h2 class="display">Send an enquiry</h2>
<label>Your name<input name="n" required autocomplete="name"></label>
<label>Phone<input name="p" type="tel" required autocomplete="tel"></label>
<label>Property<select name="t"><option>HDB flat</option><option>Condominium</option><option>Landed home</option><option>Café or restaurant</option><option>Office or shop</option><option>Other</option></select></label>
<label>Tell us about your project<textarea name="m" rows="4" placeholder="Rooms, timeline, styles you like"></textarea></label>
<button class="btn dark-b" type="submit">Continue on WhatsApp</button>
<p class="fnote">Opens WhatsApp with your details filled in. Attach your floor plan there.</p></form></div></section>"""
    s += footer()
    write("contact/index.html", s)

def notfound():
    s = head("Page not found | Maison Interior Design", "This page has moved. Browse our interior design portfolio or contact the studio.", "404", "Jimmy-Monkey-Completed-6.jpg", {"@context": "https://schema.org", **ORG})
    s += header("")
    s += f'<section class="phead"><div class="wrap"><p class="eyebrow">404</p><h1 class="display">This room <em>isn\'t here</em></h1><p class="ph-p">The page may have moved. Try the portfolio or get in touch.</p><div class="btns"><a class="btn dark-b" href="{BASE}portfolio/">View portfolio</a><a class="btn ghost-d" href="{BASE}contact/">Contact us</a></div></div></section>'
    s += footer()
    write("404.html", s)

def extras():
    urls = [""] + [h for h, _ in NAV] + ["landed-homes/"] + [f'portfolio/{p["slug"]}/' for p in P] + LAUNCH_URLS[1:]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{DOMAIN}/{u}</loc><lastmod>{'2026-11-07' if (u in LAUNCH_URLS or u == '') else '2026-11-03'}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    write("sitemap.xml", sm)
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    write("llms.txt", f"""# Maison Interior Design

> Residential and commercial interior design and build studio in Singapore, founded 2018; its builder team mainly builds landed houses. Managing Director: Roland Ng. WhatsApp/phone {PHONE}, email {EMAIL}.

## Services
- [Residential interior design]({DOMAIN}/services/#residential): HDB flats and condominiums, concept to handover.
- [Commercial interior design]({DOMAIN}/services/#commercial): cafes, restaurants, offices.
- [3D design]({DOMAIN}/services/#3d-design): perspective 3D drawings and colour proposal before work starts.
- [Landed house building]({DOMAIN}/landed-homes/): the builder team mainly builds landed houses, with the interior planned by the same team.

## Process
Conceptualisation; itemised quotation with 3D drawings; HDB renovation permit and renovation loan applications; design and build with dedicated project management; 2-year workmanship warranty and post-sales service.

## Suppliers
Maison works with these Singapore suppliers for materials, flooring, lighting and furnishings: """ + ", ".join(f"[{n}]({u})" for k, n, u in SUPPLIERS) + """.

## Service guides
""" + "".join(f'- [{g["short"]}]({DOMAIN}/services/{g["slug"]}/): {g["desc"]}\n' for g in GUIDES) + """
## New launches (renovation and fit-out guides; facts from public sources, Maison is not appointed by any developer or HDB)
- [New launches hub]({DOMAIN}/new-launches/)
""" + "".join(f'- [{p["name"]}, {p["place"]}]({DOMAIN}/new-launches/{p["slug"]}/): {p["label"]}. {p["date"][1].split(". ")[0]}.\n' for p in LAUNCHES) + """
## Projects
""" + "".join(f'- [{p["name"]} {p["place"]}]({DOMAIN}/portfolio/{p["slug"]}/): {p["kind"]}, {p["type"]}.\n' for p in P))
    write("favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#1f1c19"/><text x="32" y="44" font-family="Georgia,serif" font-size="36" fill="#c9a979" text-anchor="middle">M</text></svg>')
    shutil.copy(os.path.join(HERE, "mid.css"), os.path.join(OUT, "mid.css"))
    for d in ("brand", "logos", "img", "images"):
        if os.path.isdir(os.path.join(HERE, d)): shutil.copytree(os.path.join(HERE, d), os.path.join(OUT, d))
    shutil.copy(os.path.join(HERE, "mid.js"), os.path.join(OUT, "mid.js"))

exec(open(os.path.join(HERE, "launches.py"), encoding="utf-8").read())

if __name__ == "__main__":
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    home(); portfolio(); services(); landed(); about(); contact(); notfound()
    for i, p in enumerate(P): project(i, p)
    launches_build()
    extras()
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files")
