#!/usr/bin/env python3
"""Carku Singapore preview builder (pageonesingapore.com/preview/carku/).

Template-first: every page renders head, header, footer, sticky bar, CTA links and
schema from the functions below. Articles come from data/articles/*.json and use the
same templates (night writer: add one JSON, run this, upload the changed files).

    python3 build.py          -> writes ./site
Facts live in data/models.py and FACTS below. Never add a claim that is not there.
"""
import hashlib, html, json, os, shutil, sys, urllib.parse, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "data"))
from models import MODELS, MEDIA, DIMS, APP_IOS, APP_ANDROID  # noqa: E402

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
BASE = "https://pageonesingapore.com/preview/carku/"
HYPER = "https://pageonesingapore.com/preview/hyper-power/"
KOHDEN = "https://www.kohden.com.sg/"
WA_NUM = "6586030355"
TEL = "+6569666565"
TEL_TXT = "+65 6966 6565"
ADDR = "7 Kaki Bukit Road 1 #01-15 Eunos Technolink, Singapore 415937"
HOURS = "Monday to Friday, 9am to 5pm. Closed on Saturday and Sunday."
TODAY = datetime.date(2026, 11, 15).isoformat()

e = html.escape


def wa(msg):
    return "https://wa.me/%s?text=%s" % (WA_NUM, urllib.parse.quote(msg, safe=""))


WA_GENERAL = wa("Hi Kohden, I'd like advice on a Carku smart battery for my car.\nCar model: \nCurrent battery size (from the label): ")
WA_WORKSHOP = wa("Hi Kohden, our workshop would like to stock and fit Carku batteries.\nWorkshop name: \nArea: \nContact person: ")


def wa_model(m):
    return wa("Hi Kohden, I'm interested in the Carku %s (%s).\nCar model: " % (m["code"], m["size_long"]))


# ---------- icons (one authored set, 1.6 stroke) ----------
P = {
    "bt": '<path d="m7 7 10 10-5 4V3l5 4L7 17"/>',
    "bolt": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    "shield": '<path d="M12 3 5 5.8v5.4c0 4.5 3 8 7 9.8 4-1.8 7-5.3 7-9.8V5.8L12 3z"/><path d="m9 12 2.2 2.2L15.5 10"/>',
    "ring": '<circle cx="12" cy="12" r="8.5"/><path d="M12 3.5a8.5 8.5 0 0 1 8.2 10.7"/>',
    "thermo": '<path d="M10 14.5V5a2 2 0 0 1 4 0v9.5a4 4 0 1 1-4 0z"/><path d="M12 9v7"/>',
    "cycle": '<path d="M20 12a8 8 0 0 1-14 5.3M4 12a8 8 0 0 1 14-5.3"/><path d="M18 3v4h-4M6 21v-4h4"/>',
    "feather": '<path d="M5 19 19 5M8 16h6l4-4M8 16V10l6-6"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "van": '<path d="M3 7h11v9H3zM14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    "swap": '<path d="M4 8h13l-3-3M20 16H7l3 3"/>',
    "wrench": '<path d="M14.5 6.5a4 4 0 0 0 5 5l-8.8 8.8a2 2 0 0 1-2.9-2.9L16.6 8.6"/><path d="M14.5 6.5 17 4"/>',
    "phone": '<rect x="7" y="2.5" width="10" height="19" rx="2.5"/><path d="M11 18.5h2"/>',
    "alert": '<path d="M12 3 2.5 20h19L12 3z"/><path d="M12 10v4.5M12 17.5v.01"/>',
    "volt": '<rect x="3" y="7" width="16" height="11" rx="2"/><path d="M19 10.5h2v4h-2M8 12.5h6M11 9.5v6"/>',
    "health": '<path d="M3 12h4l2-5 4 10 2-5h6"/>',
    "current": '<path d="M3 12c2.5-5 5.5-5 8 0s5.5 5 8 0"/><path d="M19 8v8"/>',
    "check": '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
    "left": '<path d="M15 5 8 12l7 7"/>',
    "right": '<path d="m9 5 7 7-7 7"/>',
    "pin": '<path d="M12 21s6.5-5.6 6.5-11a6.5 6.5 0 0 0-13 0c0 5.4 6.5 11 6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "flake": '<path d="M12 2v20M3.5 7l17 10M20.5 7l-17 10"/><path d="m9.5 3.5 2.5 2 2.5-2M9.5 20.5l2.5-2 2.5 2"/>',
    "store": '<path d="M4 9.5V20h16V9.5M3 9.5 5 4h14l2 5.5"/><path d="M10 20v-5h4v5"/>',
    "qr": '<path d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h2v2h-2zM18 18h2v2h-2zM14 18h2M18 14h2"/>',
}
WA_PATH = '<path fill="currentColor" d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21h.01c5.46 0 9.91-4.45 9.91-9.91A9.85 9.85 0 0 0 12.04 2zm0 18.15h-.01a8.23 8.23 0 0 1-4.2-1.15l-.3-.18-3.12.82.83-3.04-.2-.31a8.22 8.22 0 0 1-1.26-4.38c0-4.54 3.7-8.24 8.25-8.24a8.2 8.2 0 0 1 8.24 8.25c0 4.54-3.7 8.23-8.23 8.23zm4.52-6.16c-.25-.12-1.47-.72-1.69-.81-.23-.08-.39-.12-.56.13-.16.25-.64.81-.78.97-.14.17-.29.19-.54.06a6.7 6.7 0 0 1-1.99-1.23 7.5 7.5 0 0 1-1.38-1.72c-.14-.25-.02-.38.11-.51.11-.11.25-.29.37-.43.13-.15.17-.25.25-.42.08-.17.04-.31-.02-.43-.06-.13-.56-1.35-.77-1.85-.2-.48-.41-.42-.56-.43h-.48a.92.92 0 0 0-.66.31c-.23.25-.87.85-.87 2.07 0 1.22.89 2.4 1.02 2.57.12.16 1.75 2.67 4.23 3.74.59.26 1.05.41 1.41.52.59.19 1.13.16 1.56.1.48-.07 1.47-.6 1.67-1.18.21-.58.21-1.08.15-1.18-.06-.11-.23-.17-.48-.29z"/>'


def ico(name):
    if name == "wa":
        return '<svg class="ico" viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">%s</svg>' % WA_PATH
    return ('<svg class="ico" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" '
            'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>' % P[name])


def btn_wa(label, cta, href=WA_GENERAL, cls="", anchor=False):
    return ('<a class="btn btn-wa %s" href="%s" data-cta="%s" target="_blank" rel="noopener"%s>%s<span>%s</span></a>'
            % (cls, e(href), cta, ' data-sticky-anchor' if anchor else "", ico("wa"), e(label)))


IMG = "assets/img/carku/"


def frame(r, name, alt, fb, key="product", cls="", eager=False):
    """Official Carku image in a frame at its true aspect ratio, object-fit: contain (never cover)."""
    w, h = DIMS[key]
    load = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy"'
    return ('<span class="frame %s" style="aspect-ratio:%d/%d"><span class="fb" aria-hidden="true">%s</span>'
            '<img src="%s%s%s" alt="%s" %s decoding="async" width="%d" height="%d"></span>'
            % (cls, w, h, e(fb), r, IMG, e(name), e(alt), load, w, h))


def tbc(v, suffix=""):
    return ('<span class="tbc">To be confirmed</span>' if v is None else e(str(v)) + suffix)


# ---------- navigation ----------
NAV = [("smart-app/", "Smart app"), ("jump-start/", "Jump-start"), ("models/", "Models"),
       ("fitment/", "Find your size"), ("warranty/", "Warranty"), ("for-workshops/", "Workshops")]
MENU = [("Drivers", [("smart-app/", "Smart battery app"), ("jump-start/", "One-touch jump start"),
                     ("models/", "All 7 models"), ("fitment/", "Find your size"),
                     ("why-sodium-ion/", "Why sodium-ion"), ("warranty/", "5-year warranty and service"),
                     ("faq/", "FAQ"), ("contact/", "Contact Kohden")]),
        ("Workshops", [("for-workshops/", "Stock and fit Carku")])]


def head(path, title, desc, schema, og_alt="Carku smart sodium-ion car battery, Singapore"):
    r = "../" * path.count("/")
    url = BASE + path
    t, dsc = e(title), e(desc)
    return f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t}</title>
<meta name="description" content="{dsc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B2350">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Carku Singapore">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{dsc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/img/og-1200x630.jpg">
<meta property="og:image:secure_url" content="{BASE}assets/img/og-1200x630.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(og_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t}">
<meta name="twitter:description" content="{dsc}">
<meta name="twitter:image" content="{BASE}assets/img/og-1200x630.jpg">
<link rel="preload" href="{r}assets/fonts/archivo-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{r}assets/css/site.css?v={VER['css']}">
<link rel="icon" type="image/webp" href="{r}assets/img/carku/carku-app-icon.webp">
<link rel="apple-touch-icon" href="{r}assets/img/apple-touch-icon.png">
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(path)}
<main id="main">
"""


def header(path):
    r = "../" * path.count("/")
    nav = "".join('<a href="%s%s"%s>%s</a>' % (r, h, ' aria-current="page"' if path.startswith(h) else "", e(l)) for h, l in NAV)
    cols = ""
    for lab, items in MENU:
        cols += '<p class="menu-h">%s</p><ul>%s</ul>' % (e(lab), "".join('<li><a href="%s%s">%s</a></li>' % (r, h, e(l)) for h, l in items))
    return f"""<header class="hd">
  <div class="wrap hd-in">
    <a class="hd-logo" href="{r or './'}"><img src="{r}{IMG}{MEDIA['logo']}" alt="Carku" width="300" height="100"><span class="sg">Singapore</span></a>
    <nav class="hd-nav" aria-label="Main">{nav}</nav>
    {btn_wa("WhatsApp", "header-whatsapp")}
    <details class="menu" data-menu>
      <summary aria-label="Menu"><span class="burger" aria-hidden="true"><i></i><i></i></span></summary>
      <div class="menu-panel">{cols}{btn_wa("WhatsApp Kohden", "menu-whatsapp", cls="btn-full")}</div>
    </details>
  </div>
</header>"""


def footer(path):
    r = "../" * path.count("/")
    drv = "".join('<li><a href="%s%s">%s</a></li>' % (r, h, e(l)) for h, l in MENU[0][1])
    return f"""</main>
<footer class="ft">
  <div class="wrap">
    <div class="ft-grid">
      <div class="ft-brand">
        <span class="ft-logo"><img src="{r}{IMG}{MEDIA['logo']}" alt="Carku" width="300" height="100" loading="lazy"></span>
        <p style="margin-top:14px">Smart sodium-ion car batteries with app monitoring, one-touch jump start and a 5-year warranty.</p>
        {btn_wa("WhatsApp Kohden", "footer-whatsapp")}
      </div>
      <div>
        <h2>Singapore distributor</h2>
        <p><a href="{KOHDEN}" target="_blank" rel="noopener">KohDen International Pte Ltd</a></p>
        <address>{e(ADDR)}</address>
        <ul style="margin-top:8px"><li><a href="tel:{TEL}" data-cta="footer-call">Call {TEL_TXT}</a></li><li><a href="{e(WA_GENERAL)}" data-cta="footer-wa-number" target="_blank" rel="noopener">WhatsApp +65 8603 0355</a></li></ul>
        <p style="margin-top:8px">{e(HOURS)}</p>
      </div>
      <nav aria-label="Footer"><h2>Drivers</h2><ul>{drv}</ul></nav>
      <div>
        <h2>Workshops</h2><ul><li><a href="{r}for-workshops/">Stock and fit Carku</a></li></ul>
        <h2 style="margin-top:18px">Also from Kohden</h2>
        <ul><li><a href="{HYPER}" data-cta="footer-hyper-power">Hyper Power sodium-ion and lithium batteries</a></li><li><a href="{KOHDEN}" target="_blank" rel="noopener">kohden.com.sg</a></li></ul>
        <h2 style="margin-top:18px">More</h2>
        <ul><li><a href="{r}articles/">Guides</a></li><li><a href="{r}privacy/">Privacy</a></li></ul>
      </div>
    </div>
    <div class="ft-legal">
      <p>Carku is a brand of Shenzhen Carku Technology Co., Ltd. Distributed in Singapore by <a href="{KOHDEN}" target="_blank" rel="noopener">KohDen International Pte Ltd</a>. Specifications from carkubattery.com product pages. Warranty, replacement, 24-hour support and on-site service are Kohden's Singapore terms. Prices on request.</p>
      <p>© 2026 Carku Singapore. Preview site.</p>
    </div>
  </div>
</footer>
<div class="sticky" data-sticky aria-hidden="true">{btn_wa("WhatsApp Kohden", "sticky-whatsapp")}<a class="btn call" href="tel:{TEL}" data-cta="sticky-call">Call</a></div>
<script src="{r}assets/js/site.js?v={VER['js']}" defer></script>
</body>
</html>
"""


# ---------- schema ----------
ORG = {"@type": "Organization", "@id": BASE + "#kohden", "name": "KohDen International Pte Ltd", "url": KOHDEN,
       "telephone": TEL_TXT,
       "address": {"@type": "PostalAddress", "streetAddress": "7 Kaki Bukit Road 1 #01-15 Eunos Technolink",
                   "addressLocality": "Singapore", "postalCode": "415937", "addressCountry": "SG"},
       "contactPoint": [{"@type": "ContactPoint", "contactType": "customer service", "telephone": TEL_TXT, "areaServed": "SG",
                         "availableLanguage": "en", "hoursAvailable": {"@type": "OpeningHoursSpecification",
                         "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "17:00"}}],
       "brand": {"@id": BASE + "#brand"}}
BRAND = {"@type": "Brand", "@id": BASE + "#brand", "name": "Carku", "url": "https://www.carkubattery.com/"}


def graph(*nodes):
    return {"@context": "https://schema.org", "@graph": [BRAND, ORG] + list(nodes)}


def crumbs_schema(trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + p} for i, (p, n) in enumerate(trail)]}


def crumbs_html(path, trail):
    r = "../" * path.count("/")
    li = []
    for i, (p, n) in enumerate(trail):
        li.append('<li>%s</li>' % (e(n) if i == len(trail) - 1 else '<a href="%s%s">%s</a>' % (r, p, e(n))))
    return '<nav class="crumbs" aria-label="Breadcrumb"><ol>%s</ol></nav>' % "".join(li)


def page_head(path, trail, h1, lead, cta_label="WhatsApp Kohden", cta_href=WA_GENERAL, cta="page-whatsapp", h1_html=None):
    return f"""<section class="ph"><div class="wrap">{crumbs_html(path, trail)}<h1>{h1_html or e(h1)}</h1><p class="lead">{e(lead)}</p>{btn_wa(cta_label, cta, cta_href, anchor=True)}</div></section>"""


def cta_band(path, h="Not sure which Carku fits your car?", p="Send Kohden your car model and the size code on your current battery. They reply on WhatsApp during office hours."):
    return f"""<section class="sec"><div class="wrap"><div class="cta-band"><div><h2>{e(h)}</h2><p>{e(p)}</p></div><div>{btn_wa("Ask Kohden on WhatsApp", "band-whatsapp", cls="btn-full")}</div></div></div></section>"""


def sister(path):
    return f"""<section class="sec"><div class="wrap"><div class="sister"><div><h2>Two Kohden battery brands</h2><p>Carku is the smart one, with the app and one-touch jump start. Want lithium LiFePO4, or a JIS size such as N55 or S95? Kohden's other brand, Hyper Power, covers those.</p></div><div class="sister-links"><a class="btn btn-line" href="{HYPER}" data-cta="sister-hyper-power">See Hyper Power</a><a class="txt-link" href="{KOHDEN}" target="_blank" rel="noopener">kohden.com.sg</a></div></div></div></section>"""


# ---------- pages ----------
PAGES = {}  # path -> html
SITEMAP = []  # (path, priority)


def add(path, html_, prio="0.6", sitemap=True):
    PAGES[path] = html_
    if sitemap:
        SITEMAP.append((path, prio))


def rail_items(r):
    out = []
    for m in MODELS:
        out.append('<a class="rail-item" href="%smodels/%s/">%s<span class="rail-cap"><b>%s</b><span>%s, %sAh, %sA peak</span></span></a>'
                   % (r, m["slug"], frame(r, m["img"][0], "Carku %s sodium-ion 12V starting battery, official front product photo" % m["code"], m["code"]),
                      e(m["code"]), e(m["size_long"]), m["ah"], m["peak"]))
    return "".join(out)


def phone_illustration(r):
    return ('<figure class="shot">%s<figcaption class="ph-cap">Carku-Battery app, Activate Device screen. Official App Store screenshot.</figcaption></figure>'
            % frame(r, MEDIA["shot_activate"], "Official Carku-Battery iOS App Store screenshot of the Activate Device screen", "Carku-Battery app", "shot_activate"))


def stores(r):
    i = f'<img src="{r}{IMG}{MEDIA["icon"]}" alt="" width="512" height="512" loading="lazy">'
    return (f'<div class="stores"><a class="store" href="{APP_IOS}" target="_blank" rel="noopener" data-cta="app-ios">{i}Carku Battery on the App Store</a>'
            f'<a class="store" href="{e(APP_ANDROID)}" target="_blank" rel="noopener" data-cta="app-android">{i}Carku Battery on Google Play</a></div>')


def steps():
    return """<ol class="steps">
<li><span><b>Download the Carku Battery app</b><span>Free on the App Store and Google Play. Register with a username and password.</span></span></li>
<li><span><b>Pair your battery over Bluetooth</b><span>Turn on Bluetooth, follow the app's prompts and pick your battery from the list. The app can also read the QR code on the battery.</span></span></li>
<li><span><b>Check your battery any time</b><span>Tap your battery's ID to open its dashboard: state of charge, health, voltage, temperature, current and alerts.</span></span></li>
</ol>"""


def build_home():
    p = ""
    r = ""
    h6 = MODELS[2]
    schema = graph({"@type": "WebSite", "@id": BASE + "#site", "name": "Carku Singapore", "url": BASE, "publisher": {"@id": BASE + "#kohden"}},
                   {"@type": "WebPage", "@id": BASE + "#home", "url": BASE, "name": "Smart Car Battery Singapore | Carku app, jump-start, 5-year warranty",
                    "about": {"@id": BASE + "#brand"}, "isPartOf": {"@id": BASE + "#site"}})
    body = head(p, "Smart Car Battery Singapore | Carku app, jump-start, 5-year warranty",
                "Carku smart car batteries in Singapore: check charge and health in the app over Bluetooth, one-touch jump start even when the battery is flat, 5-year warranty. WhatsApp Kohden.",
                schema)
    body += f"""<section class="hero" aria-labelledby="hero-h">
  <div class="wrap hero-in">
    <div class="hero-vis">
      <div class="gauge">
        <svg viewBox="0 0 200 200" aria-hidden="true" focusable="false">
          <circle class="g-wave" cx="100" cy="100" r="96"/><circle class="g-wave w2" cx="100" cy="100" r="96"/>
          <circle class="g-track" cx="100" cy="100" r="88"/>
          <circle class="g-fill" cx="100" cy="100" r="88" pathLength="100" transform="rotate(-90 100 100)"/>
        </svg>
        <div class="gauge-img"><img src="{IMG}{h6['img'][0]}" alt="Carku CBN30-L3/H6 sodium-ion battery with the Carku-Battery app and Bluetooth marks, official product photo" width="1600" height="1310" loading="eager" fetchpriority="high" decoding="async"></div>
      </div>
      <ul class="chips" aria-label="Key facts"><li>{ico("bt")}Bluetooth app</li><li>{ico("thermo")}−40 to 80 °C</li><li>{ico("cycle")}3000 cycles</li></ul>
    </div>
    <div class="hero-copy">
      <h1 id="hero-h">Smart car battery for Singapore</h1>
      <p class="hero-line">Check it on your phone. Start a flat car with one touch. 5-year warranty.</p>
      <div class="hero-cta">{btn_wa("WhatsApp Kohden", "hero-whatsapp", cls="btn-full", anchor=True)}<a class="txt-link" href="models/" data-cta="hero-models">See the 7 models</a></div>
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="why-h">
  <div class="wrap">
    <div class="sec-h"><h2 id="why-h">Three things a normal battery can't do</h2></div>
    <div class="screens">
      <a class="screen" href="smart-app/" data-cta="home-screen-app"><span class="s-ico">{ico("bt")}</span><h3>It reports to your phone</h3><p>The Carku Battery app connects over Bluetooth and shows charge, health, voltage, temperature, current and alerts.</p><span class="go">How the app works</span></a>
      <a class="screen screen-hi" href="jump-start/" data-cta="home-screen-jump"><span class="s-ico">{ico("bolt")}</span><h3>It starts a flat car</h3><p>One-touch jump start in the app, even when the battery is flat. No cables, no second car.</p><span class="go">About one-touch jump start</span></a>
      <a class="screen" href="warranty/" data-cta="home-screen-warranty"><span class="s-ico">{ico("shield")}</span><h3>5-year warranty</h3><p>On every Carku passenger model, with Kohden's 1-to-1 replacement for defects and 24-hour support.</p><span class="go">Warranty and service</span></a>
    </div>
  </div>
</section>

<section class="sec sec-white" aria-labelledby="rail-h">
  <div class="wrap">
    <div class="sec-h"><h2 id="rail-h">Seven models, D23 and H5 to H9</h2><p>All seven passenger models are stocked by Kohden in Singapore.</p></div>
    <div class="rail-wrap" data-rail>
      <div class="rail" role="region" aria-label="Carku models" tabindex="0">{rail_items(r)}</div>
      <div class="rail-ctrl"><div class="dots" role="group" aria-label="Choose a model"></div><div class="arrows"><button type="button" data-prev aria-label="Previous model">{ico("left")}</button><button type="button" data-next aria-label="Next model">{ico("right")}</button></div></div>
    </div>
    <p style="margin-top:18px"><a class="txt-link" href="fitment/">Find your size code</a></p>
  </div>
</section>

<section class="sec on-night" aria-labelledby="app-h">
  <div class="wrap app-grid">
    {phone_illustration(r)}
    <div>
      <div class="sec-h"><h2 id="app-h">Set up in three steps</h2><p>No dongle and no workshop visit. The Bluetooth module is built into the battery.</p></div>
      {steps()}
      {stores(r)}
    </div>
  </div>
</section>

<section class="sec" aria-labelledby="na-h">
  <div class="wrap">
    <div class="sec-h"><h2 id="na-h">Sodium-ion inside</h2><p>The chemistry behind the smart features, from Carku's published figures.</p></div>
    <ul class="facts">
      <li><b class="num">3000</b><span>rated charge cycles</span></li>
      <li><b class="num">−40 to 80 °C</b><span>working range</span></li>
      <li><b class="num">Half</b><span>the weight of lead-acid, per Carku</span></li>
      <li><b class="num">Sealed</b><span>maintenance-free, no topping up</span></li>
    </ul>
    <p style="margin-top:16px"><a class="txt-link" href="why-sodium-ion/">Why sodium-ion beats lead-acid</a></p>
  </div>
</section>

<section class="sec sec-white" aria-labelledby="svc-h">
  <div class="wrap split">
    {frame(r, MEDIA['workshop'], "Official Carku lifestyle photo of a CBN30-L3/H6 sodium-ion battery carried in a workshop beside a passenger car", "Carku", "workshop")}
    <div>
      <div class="sec-h"><h2 id="svc-h">Backed by Kohden in Singapore</h2></div>
      <ul class="svc">
        <li>{ico("clock")}<span><b>24-hour support</b><span>A support team for any battery issue.</span></span></li>
        <li>{ico("van")}<span><b>Free on-site service</b><span>Service comes to you. Workshops are welcome to partner.</span></span></li>
        <li>{ico("swap")}<span><b>1-to-1 replacement</b><span>A defective battery is replaced one for one.</span></span></li>
      </ul>
      <p style="margin-top:16px"><a class="txt-link" href="for-workshops/">For workshops: stock and fit Carku</a></p>
    </div>
  </div>
</section>
{sister(p)}
{cta_band(p)}
"""
    body += footer(p)
    add(p, body, "1.0")


def build_smart_app():
    p = "smart-app/"
    r = "../"
    trail = [("", "Home"), (p, "Smart battery app")]
    faq = [("Is the Carku Battery app free?", "Yes. It is a free download on the App Store and Google Play."),
           ("How does the app connect to the battery?", "Over Bluetooth. Turn on Bluetooth on your phone, open the app and follow its prompts to pick your battery. The app can also read the QR code on the battery to get its details."),
           ("Does the app need mobile data?", "You need an internet connection to download the app and register. Pairing with the battery uses Bluetooth."),
           ("Can I add more than one battery?", "Yes. The app's settings let you bind additional devices.")]
    schema = graph(crumbs_schema(trail), faq_schema(faq))
    body = head(p, "Car Battery with App and Bluetooth | Carku Battery app Singapore",
                "The Carku Battery app reads your car battery over Bluetooth: state of charge, state of health, voltage, temperature, current and alerts. Free on iOS and Android.", schema)
    body += page_head(p, trail, "A car battery with an app", "Pair your Carku battery with your phone over Bluetooth and see how it is doing, before it lets you down.")
    body += f"""<section class="sec on-night"><div class="wrap app-grid">{phone_illustration(r)}<div><div class="sec-h"><h2>What the app shows</h2><p>Carku lists these readings for its passenger batteries.</p></div>
<ul class="svc">
<li>{ico("ring")}<span><b>State of charge</b><span>How full the battery is right now.</span></span></li>
<li>{ico("health")}<span><b>State of health</b><span>How the battery is ageing, with early warnings for potential issues.</span></span></li>
<li>{ico("volt")}<span><b>Voltage</b><span>A real-time reading of the battery's charge level.</span></span></li>
<li>{ico("thermo")}<span><b>Temperature</b><span>So you know it is working in a safe range.</span></span></li>
<li>{ico("current")}<span><b>Current</b><span>What is flowing in and out of the battery.</span></span></li>
<li>{ico("alert")}<span><b>Alerts</b><span>Wireless alerts and diagnostic guidance.</span></span></li>
</ul></div></div></section>
<section class="sec"><div class="wrap app-grid" style="align-items:start"><div class="sec-h"><h2>Pair it in three steps</h2><p>From Carku's own setup guide.</p>{stores(r)}</div><div class="on-night" style="border-radius:28px;padding:18px">{steps()}</div></div></section>
<section class="sec sec-white"><div class="wrap split split-rev">{frame("../", MEDIA['appguide'], "Official Carku-Battery app installation guide: account, sign-in, Bluetooth pairing, real-time status and settings", "Carku Battery app", "appguide")}<div class="prose"><h2 style="margin-top:0">Why it matters in Singapore</h2><p>Short trips, idling in traffic and cars parked for days drain a battery slowly. A normal battery gives no warning until the car will not start. With Carku you can open the app and see the charge and health before you set off.</p><p>And if the charge does run out, the same app has <a href="../jump-start/">one-touch jump start</a>.</p></div></div></section>
<section class="sec"><div class="wrap"><h2 class="faq-group" style="margin-top:0">App questions</h2>{faq_html(faq)}</div></section>
{cta_band(p, "Want a battery that talks to your phone?")}"""
    body += footer(p)
    add(p, body, "0.9")


def build_jump():
    p = "jump-start/"
    r = "../"
    trail = [("", "Home"), (p, "One-touch jump start")]
    faq = [("Can a Carku battery start the car when it is flat?", "Yes. Kohden confirms that through the Carku app the battery can start the car even when it has gone flat. Carku calls this one-touch jump start."),
           ("Do I still need jumper cables or a power bank?", "The one-touch jump start is built to rescue you without a second car. Kohden can explain how it works on your model."),
           ("Which Carku models have it?", "Kohden supplies all seven Carku passenger models in Singapore. Ask Kohden on WhatsApp to confirm the feature for the model that fits your car.")]
    schema = graph(crumbs_schema(trail), faq_schema(faq))
    body = head(p, "Jump-Start Battery Singapore | Carku one-touch jump start",
                "Carku smart car battery with one-touch jump start in the app, even when the battery is flat. Sold and supported in Singapore by Kohden. WhatsApp to ask.", schema)
    body += page_head(p, trail, "One-touch jump start, even when the battery is flat", "Battery gone flat in the car park? Open the Carku app and use one-touch jump start. No cables, no second car.")
    body += f"""<section class="sec"><div class="wrap split">{frame("../", MODELS[3]['img'][1], "Carku CBN30-L3H sodium-ion starting battery in an official lifestyle scene with a passenger car", "Carku smart battery")}<div class="prose">
<h2 style="margin-top:0">A battery that rescues itself</h2>
<p>Carku lists one-touch jump start capability on its smart starting batteries. Kohden confirms what that means for drivers here: through the app, the battery can start the car even when it has gone flat.</p>
<h3>When it helps</h3>
<ul><li>Lights or a dashcam left on overnight</li><li>A car parked for a long time</li></ul>
<h3>What you need</h3>
<ul><li>A Carku smart battery fitted in your car</li><li>The free Carku Battery app, paired over Bluetooth</li></ul>
<p class="fine">Exact steps and limits depend on the model. Kohden can walk you through it.</p>
</div></div></section>
<section class="sec on-night"><div class="wrap"><div class="sec-h"><h2>It starts with the app</h2><p>Pair once and the same app shows charge, health and alerts, so a flat battery is less of a surprise.</p></div>{steps()}{stores(r)}</div></section>
<section class="sec"><div class="wrap"><h2 class="faq-group" style="margin-top:0">Jump-start questions</h2>{faq_html(faq)}</div></section>
{cta_band(p, "Never wait for a jump again", "Tell Kohden your car model and they will match the right Carku battery.")}"""
    body += footer(p)
    add(p, body, "0.9")


def build_why():
    p = "why-sodium-ion/"
    trail = [("", "Home"), (p, "Why sodium-ion")]
    schema = graph(crumbs_schema(trail))
    body = head(p, "Sodium-ion vs Lead-Acid Car Battery | Why Carku",
                "Why a Carku sodium-ion starting battery: 3000 cycles, works from −40 °C to 80 °C, sealed and maintenance-free, about half the weight of lead-acid, plus app monitoring.", schema)
    body += page_head(p, trail, "Why sodium-ion beats lead-acid", "Carku builds its smart car batteries on sodium-ion cells. Here is what that changes for a driver.")
    rows = [("Rated cycles", "3000", "Far fewer, varies by type"),
            ("Working temperature", "−40 °C to 80 °C", "Loses power in heat and cold"),
            ("Weight", "About half of lead-acid, per Carku", "Heavier"),
            ("Maintenance", "Sealed, no topping up", "May need checks"),
            ("Monitoring", "Bluetooth app: charge, health, alerts", "None"),
            ("Flat-battery rescue", "One-touch jump start in the app", "Needs cables or a second car")]
    tr = "".join('<tr><th scope="row">%s</th><td>%s</td><td style="font-weight:500;color:var(--ink-2)">%s</td></tr>' % tuple(map(e, r_)) for r_ in rows)
    hg = frame("../", MEDIA["hero_graphic"], "Official Carku photo of CBN30-L3H and CBN30-L3 sodium-ion starting batteries on a highway with passenger cars, headline The Next-Gen Lead-Acid Replacement", "Carku", "hero_graphic", cls="band-img")
    body += f"""<section class="sec"><div class="wrap">{hg}
<div style="overflow-x:auto;margin-top:26px"><table class="spec" style="min-width:560px"><caption>Carku sodium-ion vs a typical lead-acid battery</caption><thead><tr><th scope="col">What matters</th><th scope="col" style="color:var(--night)">Carku sodium-ion</th><th scope="col">Typical lead-acid</th></tr></thead><tbody>{tr}</tbody></table></div>
<p class="fine" style="margin-top:10px">Carku figures from carkubattery.com product pages. Lead-acid column is a general description, not a specific product.</p>
</div></section>
<section class="sec sec-white"><div class="wrap split">{frame("../", MEDIA['features'], "Official Carku graphic of sodium-ion starting batteries with feature icons and passenger-car scenes", "Carku sodium-ion", "features")}<div class="prose">
<h2 style="margin-top:0">Built for heat as well as cold</h2>
<p>Carku rates its sodium-ion starting batteries from −40 °C to 80 °C. In Singapore the challenge is heat: a car parked in the sun all day. Carku says its sodium-ion chemistry stays stable across that range, and lists self-heating on most models.</p>
<h2>Light and sealed</h2>
<p>Carku says its sodium-ion starting battery is about half the weight of lead-acid. The case is sealed and maintenance-free, so there is no acid to top up.</p>
<h2>Cleaner chemistry</h2>
<p>Sodium is an abundant material. Carku describes the chemistry as cleaner, safer and fully recyclable.</p>
<p>Looking for a sodium-ion battery with on-site fitting across many JIS sizes? See Kohden's other brand, <a href="{HYPER}">Hyper Power</a>.</p>
</div></div></section>
{cta_band(p)}"""
    body += footer(p)
    add(p, body, "0.7")


def model_card(m, r):
    return ('<a class="mcard" href="%smodels/%s/">%s<span><b>%s</b><span class="m-size">%s</span><span class="m-k">%sAh, %sA peak, %s</span></span></a>'
            % (r, m["slug"], frame(r, m["img"][0], "Carku %s sodium-ion starting battery, official front product photo" % m["code"], m["code"]),
               e(m["code"]), e(m["size_long"]), m["ah"], m["peak"], e(m["volt"])))


def build_models():
    p = "models/"
    trail = [("", "Home"), (p, "Models")]
    il = {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": BASE + "models/%s/" % m["slug"], "name": "Carku " + m["code"]} for i, m in enumerate(MODELS)]}
    schema = graph(crumbs_schema(trail), il)
    body = head(p, "Carku Battery Singapore | All 7 smart sodium-ion car battery models",
                "All 7 Carku smart sodium-ion car batteries in Singapore: CBN30-D23, H5, H6, L3H, H7, H8 and CBN50-H9. Bluetooth app, 3000 cycles, 5-year warranty. In stock at Kohden.", schema)
    body += page_head(p, trail, "Carku battery models in Singapore", "Seven 12V smart sodium-ion batteries for passenger cars. All stocked by Kohden.")
    cards = "".join(model_card(m, "../") for m in MODELS)
    rows = "".join('<tr><th scope="row"><a href="%s/">%s</a></th><td>%s</td><td>%sAh</td><td>%sA</td><td>%s</td></tr>'
                   % (m["slug"], e(m["code"]), e(m["size"]), m["ah"], m["peak"], tbc(m["wh"], " Wh")) for m in MODELS)
    lineup = frame("../", MEDIA["lineup"], "Official Carku sodium-ion starting battery lineup with four passenger-car batteries and the Carku-Battery app on a phone", "Carku lineup", "lineup", cls="band-img")
    body += f"""<section class="sec"><div class="wrap">{lineup}<div class="mgrid" style="margin-top:22px">{cards}</div></div></section>
<section class="sec sec-white"><div class="wrap"><div style="overflow-x:auto"><table class="spec" style="min-width:560px"><caption>Compare at a glance</caption><thead><tr><th scope="col">Model</th><th scope="col">Size</th><th scope="col">Capacity</th><th scope="col">Peak current</th><th scope="col">Energy</th></tr></thead><tbody>{rows}</tbody></table></div>
<p class="fine" style="margin-top:10px">All models: 3000 cycles, −40 °C to 80 °C, Bluetooth app, 5-year warranty. Carku publishes peak current, not CCA.</p></div></section>
{cta_band(p)}"""
    body += footer(p)
    add(p, body, "0.9")


def build_model(m):
    p = "models/%s/" % m["slug"]
    trail = [("", "Home"), ("models/", "Models"), (p, m["code"])]
    props = [("Capacity", "%s Ah" % m["ah"]), ("Voltage", m["volt"]), ("Peak current", "%s A" % m["peak"]),
             ("Cycle life", "3000 cycles"), ("Operating temperature", "-40 to 80 °C"), ("Bluetooth", "Yes")]
    if m["wh"]:
        props.append(("Energy", "%s Wh" % m["wh"]))
    if m["dims"] and not m["dims_tbc"]:
        props.append(("Dimensions", m["dims"]))
    if m["kg"]:
        props.append(("Weight", m["kg"]))
    prod = {"@type": "Product", "@id": BASE + p + "#product", "name": "Carku %s sodium-ion car starting battery" % m["code"],
            "model": m["code"], "sku": m["code"], "brand": {"@id": BASE + "#brand"}, "image": [BASE + IMG + f for f in m["img"]],
            "description": "12V smart sodium-ion starting battery for passenger cars, %s. %sAh, %sA peak current, Bluetooth app monitoring, 5-year warranty in Singapore through Kohden." % (m["size_long"], m["ah"], m["peak"]),
            "category": "Car starting battery",
            "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in props]}
    schema = graph(crumbs_schema(trail), prod)
    title = "Carku %s Smart Battery | %s, %sAh, %sA | Singapore" % (m["code"], m["size"], m["ah"], m["peak"])
    desc = "Carku %s smart sodium-ion car battery, %s: %sAh, %sA peak, 3000 cycles, Bluetooth app and one-touch jump start. 5-year warranty via Kohden Singapore." % (m["code"], m["size_long"], m["ah"], m["peak"])
    body = head(p, title, desc, schema, og_alt="Carku %s smart sodium-ion car battery" % m["code"])
    body += page_head(p, trail, "", m["line"], "Ask about the %s" % m["code"], wa_model(m), "model-whatsapp", h1_html='Carku <span style="white-space:nowrap">%s</span> smart battery' % e(m["code"]))
    dims = tbc(m["dims"]) + (' <span class="tbc">Size to be confirmed</span>' if m["dims_tbc"] else "")
    spec = [("Size", e(m["size_long"])), ("Voltage", e(m["volt"])), ("Capacity", "%s Ah" % m["ah"]),
            ("Peak current", "%s A <span class=\"fine\">(peak, not CCA)</span>" % m["peak"]), ("Energy", tbc(m["wh"], " Wh")),
            ("Dimensions (L × W × H)", dims), ("Weight", tbc(m["kg"])), ("Cycle life", "3000 cycles"),
            ("Operating temperature", "−40 °C to 80 °C"), ("Self-heating", "<span class=\"tbc\">To be confirmed for this model</span>"),
            ("Bluetooth app", "Yes, Carku Battery app"), ("One-touch jump start", "Yes, through the app"),
            ("Terminal layout", "<span class=\"tbc\">To be confirmed</span>"), ("Warranty", "5 years, terms by Kohden"),
            ("Availability", "In stock at Kohden, Singapore")]
    tr = "".join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (e(k), v) for k, v in spec)
    views = {"angle": "three-quarter product photo", "angle-right": "three-quarter product photo from the right", "angle-high": "three-quarter product photo from above",
             "back": "back and label photo", "top": "top view showing the terminals", "scene": "official lifestyle scene with a passenger car",
             "certificates": "photographed with certificate documents, official gallery image"}
    gallery = "".join(frame("../../", f, "Carku %s sodium-ion starting battery, %s" % (m["code"], views[f.split("-", 3)[3][:-5]] if f.split("-", 3)[3][:-5] in views else "official product photo"), m["code"]) for f in m["img"][1:])
    off = "".join('<li>%s<span>%s</span></li>' % (ico("check"), e(x)) for x in m["official"])
    others = "".join(model_card(o, "../../") for o in MODELS if o is not m and o["size"] in (m["size"],)) or ""
    body += f"""<section class="sec"><div class="wrap mp">
  <div class="mp-media">{frame("../../", m['img'][0], "Carku %s sodium-ion 12V starting battery, official front product photo" % m['code'], m['code'], eager=True)}<div class="mp-thumbs">{gallery}</div></div>
  <div>
    <table class="spec"><caption>Specifications</caption><tbody>{tr}</tbody></table>
    <p class="fine" style="margin-top:10px">Source: <a href="{e(m['src'])}" target="_blank" rel="noopener">Carku product page</a>. Carku publishes peak current, not CCA.</p>
    <h2 style="font-size:1.6rem;margin:28px 0 12px">From Carku</h2>
    <ul class="ticks">{off}</ul>
    <h2 style="font-size:1.6rem;margin:28px 0 12px">With every Carku from Kohden</h2>
    <ul class="ticks"><li>{ico("check")}<span>5-year warranty and 1-to-1 replacement for defects</span></li><li>{ico("check")}<span>24-hour support and free on-site service</span></li><li>{ico("check")}<span>Free Carku Battery app with one-touch jump start</span></li></ul>
    <p style="margin-top:22px">{btn_wa("Ask about the %s" % m['code'], "model-whatsapp-2", wa_model(m), cls="btn-full")}</p>
    <p><a class="txt-link" href="../../fitment/#size-{m['size'].lower()}">Check it fits: size {e(m['size'])}</a></p>
  </div>
</div></section>
{('<section class="sec sec-white"><div class="wrap"><h2 style="margin-bottom:18px">Also in size ' + e(m['size']) + '</h2><div class="mgrid">' + others + '</div></div></section>') if others else ''}
{sister(p)}"""
    body += footer(p)
    add(p, body, "0.8")


def build_fitment():
    p = "fitment/"
    trail = [("", "Home"), (p, "Find your size")]
    schema = graph(crumbs_schema(trail))
    body = head(p, "Carku Battery Size Finder | D23, H5, H6, H7, H8, H9 Singapore",
                "Find the Carku smart battery for your car by battery size code: JIS D23 or DIN H5 (L2), H6 (L3), H7 (L4), H8 (L5) and H9 (L6). Dimensions and models side by side.", schema)
    body += page_head(p, trail, "Find your Carku by battery size", "Look at the label on your current battery for its size code, then tap it below.")
    sizes = []
    for m in MODELS:
        if m["size"] not in sizes:
            sizes.append(m["size"])
    chips = "".join('<li><a href="#size-%s">%s</a></li>' % (s.lower(), s) for s in sizes)
    blocks = ""
    for s in sizes:
        ms = [m for m in MODELS if m["size"] == s]
        rows = "".join('<div class="fit-row">%s<div><b><a href="../models/%s/">%s</a></b><br><span class="fine">%sAh, %sA peak. Size: %s. Weight: %s.</span></div></div>'
                       % (frame("../", m["img"][0], "Carku %s, official product photo" % m["code"], m["code"]), m["slug"], e(m["code"]), m["ah"], m["peak"],
                          tbc(m["dims"]) + (" (to be confirmed)" if m["dims_tbc"] else ""), tbc(m["kg"])) for m in ms)
        lab = ms[0]["size_long"].replace(" case", " size")
        blocks += '<section class="fit" id="size-%s" aria-labelledby="h-%s"><h2 id="h-%s">%s <small>%s</small></h2>%s</section>' % (s.lower(), s.lower(), s.lower(), s, e(lab), rows)
    body += f"""<section class="sec"><div class="wrap"><ul class="sizes" aria-label="Battery sizes">{chips}</ul>{blocks}
<div class="prose" style="margin-top:30px"><h2>Not sure of your size?</h2><p>Send Kohden a photo of your current battery's label and your car model on WhatsApp. Terminal layout for each Carku model is still being confirmed, so Kohden checks the fit before you buy.</p><p>Your car takes a JIS size such as N55, Q85, S95 or T110? Kohden's <a href="{HYPER}">Hyper Power</a> range covers those sizes.</p></div></div></section>
{cta_band(p, "Send a photo of your battery label", "Kohden will tell you which Carku fits.")}"""
    body += footer(p)
    add(p, body, "0.8")


def build_warranty():
    p = "warranty/"
    trail = [("", "Home"), (p, "Warranty and service")]
    faq = [("How long is the Carku warranty in Singapore?", "5 years on every Carku passenger model, with terms by Kohden."),
           ("What happens if my battery is defective?", "Kohden replaces a defective battery one for one."),
           ("Is there support outside office hours?", "Yes. Kohden runs 24-hour support for battery issues. The office itself is open Monday to Friday, 9am to 5pm.")]
    schema = graph(crumbs_schema(trail), faq_schema(faq))
    body = head(p, "5-Year Warranty Car Battery Singapore | Carku via Kohden",
                "Every Carku passenger car battery has a 5-year warranty in Singapore, plus 1-to-1 replacement for defects, 24-hour support and free on-site service from Kohden.", schema)
    body += page_head(p, trail, "5-year warranty on every Carku", "Terms by Kohden, Carku's Singapore distributor. Plus the service that comes with it.")
    body += f"""<section class="sec"><div class="wrap split"><div><ul class="facts" style="grid-template-columns:1fr 1fr"><li><b class="num">5 years</b><span>warranty on every passenger model</span></li><li><b class="num">1 to 1</b><span>replacement for a defect</span></li><li><b class="num">24 h</b><span>support for battery issues</span></li><li><b class="num">Free</b><span>on-site service</span></li></ul></div>
<div class="prose"><h2 style="margin-top:0">What you get</h2>
<ul class="svc"><li>{ico("shield")}<span><b>5-year warranty</b><span>On all seven Carku passenger models sold by Kohden.</span></span></li><li>{ico("swap")}<span><b>1-to-1 replacement</b><span>If a defect is found, the battery is replaced one for one.</span></span></li><li>{ico("clock")}<span><b>24-hour support</b><span>A support team for any battery issue, around the clock.</span></span></li><li>{ico("van")}<span><b>Free on-site service</b><span>Service comes to you. Workshops are welcome to partner.</span></span></li></ul>
<p class="fine" style="margin-top:14px">Full warranty terms: <span class="tbc">To be confirmed</span> Kohden will publish the Singapore terms. The warranty and service terms inside the Carku app also apply. Ask Kohden on WhatsApp for a copy.</p></div></div></section>
<section class="sec sec-white"><div class="wrap"><h2 class="faq-group" style="margin-top:0">Warranty questions</h2>{faq_html(faq)}</div></section>
{cta_band(p, "Questions about a claim?", "WhatsApp Kohden with your battery's serial number from the app.")}"""
    body += footer(p)
    add(p, body, "0.8")


def build_workshops():
    p = "for-workshops/"
    trail = [("", "Home"), (p, "For workshops")]
    schema = graph(crumbs_schema(trail))
    body = head(p, "Stock and Fit Carku Smart Batteries | Workshops Singapore",
                "Workshops in Singapore: stock and fit Carku smart sodium-ion batteries through Kohden. Seven passenger sizes, app monitoring, 5-year warranty and 1-to-1 replacement.", schema)
    body += page_head(p, trail, "Stock and fit Carku in your workshop", "A battery your customers can see working on their phone. Supplied and supported by Kohden.", "Workshop enquiry on WhatsApp", WA_WORKSHOP, "workshop-whatsapp")
    body += f"""<section class="sec"><div class="wrap split">{frame("../", MEDIA['factory'], "Official Carku factory exterior with the CARKU wordmark on the building", "Carku", "factory")}<div>
<div class="sec-h"><h2>Why workshops add Carku</h2></div>
<ul class="svc">
<li>{ico("bt")}<span><b>Something to show the customer</b><span>Pair the battery with their phone at handover and they see it working.</span></span></li>
<li>{ico("store")}<span><b>Seven passenger sizes</b><span>JIS D23 and DIN H5 to H9, all stocked by Kohden.</span></span></li>
<li>{ico("shield")}<span><b>5-year warranty</b><span>With 1-to-1 replacement for defects, so fewer comebacks.</span></span></li>
<li>{ico("van")}<span><b>Kohden behind you</b><span>24-hour support and on-site service. Workshops are welcome to partner.</span></span></li>
<li>{ico("wrench")}<span><b>Plug-and-play fit</b><span>Carku describes the H6 as a direct replacement for the original AGM battery.</span></span></li>
</ul>
<p style="margin-top:20px">{btn_wa("Workshop enquiry on WhatsApp", "workshop-whatsapp-2", WA_WORKSHOP, cls="btn-full")}</p>
<p class="fine">Trade terms on request. Kohden also distributes DENSO, EXN, MOON and Hyper Power.</p>
</div></div></section>
{sister(p)}"""
    body += footer(p)
    add(p, body, "0.7")


FAQ_ALL = [
    ("The app", [
        ("What does the Carku app show?", "State of charge, state of health, voltage, temperature, current and alerts, over Bluetooth."),
        ("Is the app free?", "Yes. Search for Carku Battery on the App Store or Google Play."),
        ("How do I pair the battery?", "Turn on Bluetooth, open the app and follow its prompts to pick your battery. The app can also read the QR code on the battery.")]),
    ("Jump-start", [
        ("Can it start my car when the battery is flat?", "Yes. Through the app, a Carku battery can start the car even when it has gone flat. Carku calls it one-touch jump start."),
        ("Do I need a second car or cables?", "No second car is needed for the one-touch jump start. Kohden can walk you through it for your model.")]),
    ("Fit and specs", [
        ("Which sizes are there?", "JIS D23 and DIN H5 (L2), H6 (L3), H7 (L4), H8 (L5) and H9 (L6). Seven models in total."),
        ("Why do you show peak current and not CCA?", "Carku publishes peak current for these batteries. It is not the same test as CCA, so we do not label it CCA."),
        ("Is the terminal layout the same as my old battery?", "Terminal layout for each model is still being confirmed. Send Kohden a photo of your current battery and they will check."),
        ("How long does it last?", "Carku rates the sodium-ion cells for 3000 charge cycles.")]),
    ("Warranty and buying", [
        ("How long is the warranty?", "5 years on every Carku passenger model, terms by Kohden."),
        ("How much does it cost?", "Prices are on request. WhatsApp Kohden with your car model."),
        ("Where can I buy Carku in Singapore?", "From Kohden, 7 Kaki Bukit Road 1 #01-15. WhatsApp +65 8603 0355 or call +65 6966 6565, Monday to Friday, 9am to 5pm."),
        ("Carku or Hyper Power?", "Both come from Kohden. Carku leads with the smart app, one-touch jump start and a 5-year warranty. Hyper Power adds lithium LiFePO4 and more JIS sizes.")]),
]


def faq_schema(qs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}


def faq_html(qs):
    return '<div class="faq">%s</div>' % "".join('<details><summary>%s</summary><div class="a"><p>%s</p></div></details>' % (e(q), e(a)) for q, a in qs)


def build_faq():
    p = "faq/"
    trail = [("", "Home"), (p, "FAQ")]
    allq = [q for _, qs in FAQ_ALL for q in qs]
    schema = graph(crumbs_schema(trail), faq_schema(allq))
    body = head(p, "Carku Battery FAQ Singapore | App, jump-start, warranty, sizes",
                "Answers about Carku smart car batteries in Singapore: the Bluetooth app, one-touch jump start, sizes, peak current, the 5-year warranty and where to buy.", schema)
    body += page_head(p, trail, "Carku questions, answered", "The app, jump-start, sizes and warranty. Anything else, ask Kohden on WhatsApp.")
    inner = "".join('<h2 class="faq-group">%s</h2>%s' % (e(g), faq_html(qs)) for g, qs in FAQ_ALL)
    body += f'<section class="sec"><div class="wrap">{inner}</div></section>{cta_band(p)}'
    body += footer(p)
    add(p, body, "0.7")


def build_contact():
    p = "contact/"
    trail = [("", "Home"), (p, "Contact")]
    schema = graph(crumbs_schema(trail))
    body = head(p, "Buy Carku Battery Singapore | Contact Kohden, Kaki Bukit",
                "Buy a Carku smart car battery in Singapore from Kohden, 7 Kaki Bukit Road 1 #01-15. WhatsApp +65 8603 0355, call +65 6966 6565. Monday to Friday, 9am to 5pm.", schema)
    body += page_head(p, trail, "Contact Kohden for Carku", "WhatsApp is fastest. Send your car model and battery size.")
    maps = "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote("KohDen International Pte Ltd, 7 Kaki Bukit Road 1, Singapore 415937")
    body += f"""<section class="sec"><div class="wrap cgrid">
<div class="cbox"><h2>WhatsApp or call</h2><p>{btn_wa("WhatsApp +65 8603 0355", "contact-whatsapp", cls="btn-full")}</p><p><a class="btn btn-line btn-full" href="tel:{TEL}" data-cta="contact-call">Call {TEL_TXT}</a></p><p class="fine">{e(HOURS)}</p></div>
<div class="cbox"><h2>Visit</h2><p><b>KohDen International Pte Ltd</b></p><address>{e(ADDR)}</address><p style="margin-top:12px"><a class="txt-link" href="{e(maps)}" target="_blank" rel="noopener" data-cta="contact-map">{ico("pin")} Open in Google Maps</a></p><p class="fine">Office hours: {e(HOURS)} Website: <a href="{KOHDEN}" target="_blank" rel="noopener">kohden.com.sg</a></p></div>
</div></section>{sister(p)}"""
    body += footer(p)
    add(p, body, "0.6")


def build_privacy():
    p = "privacy/"
    trail = [("", "Home"), (p, "Privacy")]
    body = head(p, "Privacy | Carku Singapore", "How this Carku Singapore site handles your information.", graph(crumbs_schema(trail)))
    body += page_head(p, trail, "Privacy", "Short and plain.")
    body += """<section class="sec"><div class="wrap prose">
<p>This site has no forms and does not ask you for personal data. When you tap a WhatsApp or call button, you contact KohDen International Pte Ltd directly through WhatsApp or your phone, and their terms apply to that conversation.</p>
<p>Product photos and app screenshots are Carku's official images, used with the permission of Carku's authorised Singapore dealer.</p>
<p>We count taps on buttons without storing who you are. Kohden handles any personal data you send them under Singapore's Personal Data Protection Act (PDPA).</p>
<p>Questions: WhatsApp +65 8603 0355 or call +65 6966 6565.</p>
</div></section>"""
    body += footer(p)
    add(p, body, "0.2")


def build_404():
    p = "404/"
    body = head(p, "Page not found | Carku Singapore", "This page does not exist.", graph())
    body += """<section class="ph"><div class="wrap"><h1>Page not found</h1><p class="lead">Try the models or WhatsApp Kohden.</p><a class="btn btn-line" href="/preview/carku/models/" style="color:#fff">See all models</a></div></section>"""
    body += footer(p)
    add("404.html", body.replace('href="../', 'href="/preview/carku/').replace('src="../', 'src="/preview/carku/'), sitemap=False)


# ---------- articles (night writer) ----------
def load_articles():
    d = os.path.join(ROOT, "data", "articles")
    arts = []
    for f in sorted(os.listdir(d)):
        if f.endswith(".json"):
            a = json.load(open(os.path.join(d, f)))
            arts.append(a)
    arts.sort(key=lambda a: a["date"], reverse=True)
    return arts


def build_articles():
    arts = load_articles()
    hub = "articles/"
    trail = [("", "Home"), (hub, "Guides")]
    for a in arts:
        p = "articles/%s/" % a["slug"]
        t = [("", "Home"), (hub, "Guides"), (p, a["title"])]
        art = {"@type": "Article", "headline": a["title"], "datePublished": a["date"], "dateModified": a.get("modified", a["date"]),
               "author": {"@id": BASE + "#kohden"}, "publisher": {"@id": BASE + "#kohden"}, "mainEntityOfPage": BASE + p,
               "about": {"@id": BASE + "#brand"}}
        if a.get("hero"):
            art["image"] = a["hero"]
        nodes = [crumbs_schema(t), art] + ([faq_schema([(q["q"], q["a"]) for q in a["faq"]])] if a.get("faq") else [])
        body = head(p, a["seo_title"], a["description"], graph(*nodes))
        body += page_head(p, t, a["title"], a["standfirst"])
        hero = ('<span class="frame frame-photo art-hero"><img src="%s" alt="%s" width="1536" height="1024" loading="eager" decoding="async"></span>' % (e(a["hero"]), e(a.get("hero_alt", "")))) if a.get("hero") else ""
        faqh = ('<h2>Questions</h2>' + faq_html([(q["q"], q["a"]) for q in a["faq"]])) if a.get("faq") else ""
        body += f'<section class="sec"><div class="wrap prose"><p class="fine"><time datetime="{a["date"]}">{a["date"]}</time></p>{hero}{a["body_html"]}{faqh}</div></section>{cta_band(p)}'
        body += footer(p)
        add(p, body, "0.6")
    cards = "".join('<a class="acard" href="%s/">%s<span class="ac-t"><b>%s</b><time datetime="%s">%s</time></span></a>'
                    % (a["slug"], ('<span class="frame frame-photo"><img src="%s" alt="%s" width="1536" height="1024" loading="lazy" decoding="async"></span>' % (e(a["hero"]), e(a.get("hero_alt", "")))) if a.get("hero") else "",
                       e(a["title"]), a["date"], a["date"]) for a in arts)
    body = head(hub, "Smart Car Battery Guides | Carku Singapore", "Guides from Kohden on smart car batteries, battery health apps and jump-starting in Singapore.", graph(crumbs_schema(trail)))
    body += page_head(hub, trail, "Smart battery guides", "Practical guides for Singapore drivers, from Kohden.")
    body += '<section class="sec"><div class="wrap"><div class="acards"><!--ARTICLE-CARDS-->%s</div>%s</div></section>' % (cards, "" if arts else '<p>The first guide is on the way.</p>')
    body += footer(hub)
    add(hub, body, "0.5", sitemap=bool(arts))


def write_meta():
    urls = [BASE + p for p, _ in SITEMAP]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p, pr in SITEMAP:
        sm.append("  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>" % (BASE + p, TODAY, pr))
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(OUT, "sitemap.txt"), "w").write("\n".join(urls) + "\n")
    models = "\n".join("- [Carku %s](%smodels/%s/): %s, %sAh, %s, %sA peak current%s%s" % (
        m["code"], BASE, m["slug"], m["size_long"], m["ah"], m["volt"], m["peak"],
        (", %s Wh" % m["wh"]) if m["wh"] else "", (", %s" % m["kg"]) if m["kg"] else "") for m in MODELS)
    arts = load_articles()
    guides = ("## Guides\n" + "\n".join("- [%s](%sarticles/%s/): %s" % (a["title"], BASE, a["slug"], a["description"]) for a in arts) + "\n\n") if arts else ""
    llms = f"""# Carku Singapore

> Carku smart sodium-ion car batteries for passenger cars in Singapore, distributed by KohDen International Pte Ltd. Each battery pairs with the free Carku Battery app over Bluetooth to show state of charge, state of health, voltage, temperature, current and alerts, offers one-touch jump start through the app even when the battery is flat, and carries a 5-year warranty (terms by Kohden).

## Key facts
- Seven 12V sodium-ion passenger models: CBN30-D23 (JIS D23), CBN30-L2/H5, CBN30-L3/H6, CBN30-L3H, CBN40-L4/H7, CBN40-L5/H8, CBN50-L6/H9. All stocked by Kohden.
- 3000 rated cycles, operating range -40 °C to 80 °C, sealed and maintenance-free.
- Carku publishes peak current (1000A to 1500A), not CCA.
- Service through Kohden: 5-year warranty, 1-to-1 replacement for defects, 24-hour support, free on-site service. Workshops are welcome to partner.
- Prices on request.

## Contact
- KohDen International Pte Ltd, {ADDR}
- WhatsApp +65 8603 0355, phone {TEL_TXT}, {HOURS}
- Distributor website: {KOHDEN}

## Pages
- [Smart battery app]({BASE}smart-app/)
- [One-touch jump start]({BASE}jump-start/)
- [All models]({BASE}models/)
- [Find your size]({BASE}fitment/)
- [Why sodium-ion]({BASE}why-sodium-ion/)
- [5-year warranty and service]({BASE}warranty/)
- [For workshops]({BASE}for-workshops/)
- [FAQ]({BASE}faq/)
- [Contact]({BASE}contact/)

## Models
{models}

{guides}## Related
- Hyper Power sodium-ion and lithium car batteries, also from Kohden: {HYPER}
"""
    open(os.path.join(OUT, "llms.txt"), "w").write(llms)


def main():
    global VER
    css = open(os.path.join(ROOT, "static/assets/css/site.css"), "rb").read()
    js = open(os.path.join(ROOT, "static/assets/js/site.js"), "rb").read()
    VER = {"css": hashlib.sha1(css).hexdigest()[:8], "js": hashlib.sha1(js).hexdigest()[:8]}
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "static"), OUT)
    build_home(); build_smart_app(); build_jump(); build_why(); build_models()
    for m in MODELS:
        build_model(m)
    build_fitment(); build_warranty(); build_workshops(); build_faq(); build_contact(); build_privacy(); build_articles(); build_404()
    for path, h in PAGES.items():
        fp = os.path.join(OUT, path if path.endswith(".html") else os.path.join(path, "index.html"))
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, "w").write(h)
    write_meta()
    print("pages:", len(PAGES), "sitemap:", len(SITEMAP))


VER = {}
if __name__ == "__main__":
    main()
