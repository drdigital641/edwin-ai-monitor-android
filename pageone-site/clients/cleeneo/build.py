#!/usr/bin/env python3
"""Build the Cleeneo site (cleeneo.co).

Built once into pageonesingapore.com/preview/cleeneo/ and never moved: on activation, cleeneo.co's
document root is pointed at that same folder (see ../PLAYBOOK.md). Every internal link is relative so
the files work at both addresses, and canonical/structured-data URLs always name cleeneo.co.

    python3 build.py            # writes the pages into ./site, then the share images and icons

Content comes from source/content.md (captured from the old Base44 shop on 13 Oct 2026). Orders go
through WhatsApp (pre-filled per kit), which the CtaClick tracker in cleeneo.js counts.
Shared assets (cleeneo.css, cleeneo.js, img/) live in ./site and are edited by hand.
Share images and icons are drawn by share.mjs (headless Chromium) from the client's photo and logo.
"""
import html
import json
import os
import subprocess
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')
ORIGIN = 'https://cleeneo.co'
BASE = '/'
DEPTH = 0  # folder depth of the page being built; set by build() so u() can emit relative links
ABS = False  # root-relative links instead (404 page: Apache serves it at any depth)
ASSET_V = "3"
SLUG = 'cleeneo'
INDEXNOW_KEY = 'af35e347ce61461f81c1426315d06255'  # same key as the controller's Client record
# Until cleeneo.co points here, share images and icons are linked at the preview address.
LIVE = False
IMG_ORIGIN = ORIGIN if LIVE else 'https://pageonesingapore.com/preview/cleeneo'
SHARES = {}  # share-image slug -> (headline, kicker)

BIZ = {
    'name': 'Cleeneo',
    'wa': '6580604977', 'tel': '+6580604977', 'disp': '8060 4977',
    'email': 'sales@cleeneo.co',
}
WA_TEXT = 'Hi Cleeneo, I have a question about your nasal strips.'

KITS = [
    {'id': 'trial', 'name': 'Trial Kit', 'strips': 10, 'price': '9.90', 'was': None,
     'note': 'Try them for a week or two', 'badge': None},
    {'id': 'pack30', 'name': '30-Strip Pack', 'strips': 30, 'price': '21.90', 'was': '29.90',
     'note': 'A month of nights', 'badge': 'Popular'},
    {'id': 'bundle', 'name': 'Bundle: Buy 2 Get 1 Free', 'strips': 90, 'price': '43.80', 'was': '89.70',
     'note': 'Three packs of 30, best price per strip', 'badge': 'Best value'},
]

NAV = [('', 'Home'), ('nasal-strips/snoring/', 'Snoring'), ('nasal-strips/sports/', 'Sports'),
       ('nasal-strips/allergies/', 'Allergies'), ('how-to-use/', 'How to use'), ('kits/', 'Kits &amp; prices'),
       ('contact/', 'Contact')]
FOOT_MORE = [('about/', 'About Cleeneo'), ('shipping/', 'Shipping &amp; returns'), ('blog/', 'Blog')]

REVIEWS = [
    ('Wei Ming T.', 'First night in years I didn’t wake up gasping. The lift is immediate and the adhesive leaves zero residue.'),
    ('Priya N.', 'I’ve tried every strip on the pharmacy shelf. This is a different category entirely.'),
    ('Jun Hao L.', 'My sleep tracking showed a 22% drop in disturbances the first week. The tension bar is the real engineering feat here.'),
    ('Mei Ling C.', 'Genuinely changed my mornings. I breathe through my nose now without thinking about it. Worth every cent.'),
]
RATING = ('4.9', '48')

DOCTOR = ('Cleeneo strips are a drug-free breathing aid, not a treatment for sleep apnoea or any medical condition. '
          'If you snore loudly most nights, stop breathing or gasp in your sleep, or feel very tired during the day, please see a doctor.')

ICON = {
    'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8.2 8.2 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.4 3.4 0 0 0-1 2.5 5.9 5.9 0 0 0 1.2 3.1 13.5 13.5 0 0 0 5.2 4.6c1.9.8 2.7.9 3.6.7a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.2-.3-.3-.6-.4zM12 21.8a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.8 17.8L.1 24l6.3-1.7a11.8 11.8 0 0 0 5.6 1.4A11.8 11.8 0 0 0 20.4 3.6z"/></svg>',
    'moon': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>',
    'run': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="14" cy="4" r="2"/><path d="M6 21l4-6 3 2 2 4M9 11l3-3 3 3 3 1M10 15l-1-5"/></svg>',
    'leaf': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10z"/><path d="M2 21c0-3 1.9-5.4 5.1-6"/></svg>',
    'plane': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17.8 19.2L16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/></svg>',
    'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
    'truck': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
    'repeat': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 1l4 4-4 4"/><path d="M3 11V9a4 4 0 0 1 4-4h14M7 23l-4-4 4-4"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/><path d="M2 2l20 20"/></svg>',
    'layers': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l10 5-10 5L2 7z"/><path d="M2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
    'wind': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9.6 4.6A2 2 0 1 1 11 8H2M12.6 19.4A2 2 0 1 0 14 16H2M17.7 7.7A2.5 2.5 0 1 1 19.5 12H2"/></svg>',
    'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/></svg>',
    'star': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/></svg>',
}

# Client photos (source/photos, uploaded by Edwin 13 Oct 2026), resized into site/img by hand.
def photo(name, alt, w=900, h=900, lazy=True, cls='photo'):
    return (f'<img class="{cls}" src="{u("img/" + name + ".webp")}" srcset="{u("img/" + name + "-480.webp")} 480w, {u("img/" + name + ".webp")} 900w"'
            f' sizes="(max-width: 899px) 92vw, 540px" width="{w}" height="{h}" alt="{e(alt)}"{" loading=\"lazy\"" if lazy else ""} decoding="async">')


HAND_ALT = 'Hand holding a black Cleeneo silk nasal strip with the Cleeneo logo'
LAYERS_ALT = 'The layers of a Cleeneo strip: black silk weave, spring-tension bar, adhesive and release liner'
FLAT_ALT = 'Cleeneo nasal strip, top view'


def nose_svg():
    return '''<svg class="art nose" viewBox="0 0 300 260" role="img" aria-label="A nasal strip on the bridge of the nose gently lifting the sides of the nose to open the nasal valve">
<g fill="none" stroke="#0f2a2c" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
<path d="M132 20C130 80 118 130 102 162"/><path d="M168 20C170 80 182 130 198 162"/>
<path d="M102 162C84 178 90 204 112 206C126 208 136 200 150 204C164 200 174 208 188 206C210 204 216 178 198 162"/>
<ellipse cx="124" cy="192" rx="10" ry="5"/><ellipse cx="176" cy="192" rx="10" ry="5"/></g>
<g transform="translate(150 112) scale(.42) translate(-200 -80)"><path d="M30 40C30 18 60 10 100 22C150 38 250 38 300 22C340 10 370 18 370 40V120C370 142 340 150 300 138C250 122 150 122 100 138C60 150 30 142 30 120Z" fill="#1d1f20" stroke="#000" stroke-width="6"/>
<g fill="none" stroke="#6e7b7c" stroke-width="7" stroke-linecap="round"><path d="M62 60C150 74 250 74 338 60"/><path d="M60 80H340"/><path d="M62 100C150 86 250 86 338 100"/></g></g>
<g fill="none" stroke="#e07a3f" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">
<path d="M96 146H56"/><path d="M66 136L56 146L66 156"/><path d="M204 146H244"/><path d="M234 136L244 146L234 156"/></g>
<text x="150" y="250" text-anchor="middle" font-size="15" font-weight="600" fill="#004d53">The bar lifts, the nasal valve opens</text>
</svg>'''


def mark():
    return f'<img class="mark" src="{u("img/mark.webp")}" width="36" height="36" alt="">'


e = html.escape


def u(path=''):
    if ABS:
        return BASE + path
    return ('../' * DEPTH or './') + path


def wa_link(text=WA_TEXT):
    return f'https://wa.me/{BIZ["wa"]}?text={quote(text)}'


def kit_text(k):
    return (f'Hi Cleeneo, I would like to order the {k["name"]} ({k["strips"]} strips, S${k["price"]}).\n'
            'Name:\nDelivery address and postal code:')


ORDER_TEXT = 'Hi Cleeneo, I would like to order your nasal strips. Which kit do you recommend for me?'


def wa_btn(label, text=WA_TEXT, cls='btn btn-wa'):
    return f'<a class="{cls}" href="{wa_link(text)}" target="_blank" rel="noopener">{ICON["wa"]}{label}</a>'


def org_ld():
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': 'OnlineStore', '@id': f'{ORIGIN}/#org', 'name': 'Cleeneo', 'alternateName': 'Cleeneo Nasal Strips',
         'url': f'{ORIGIN}/', 'logo': {'@type': 'ImageObject', 'url': f'{IMG_ORIGIN}/img/logo.png'},
         'image': f'{IMG_ORIGIN}/img/share/home.jpg', 'email': BIZ['email'], 'telephone': BIZ['tel'],
         'areaServed': {'@type': 'Country', 'name': 'Singapore'},
         'description': 'Singapore brand of drug-free, latex-free silk nasal strips for snoring, sport and allergy congestion, delivered free across Singapore.',
         'contactPoint': {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': BIZ['tel'],
                          'email': BIZ['email'], 'areaServed': 'SG', 'availableLanguage': 'English'}},
        {'@type': 'WebSite', '@id': f'{ORIGIN}/#site', 'url': f'{ORIGIN}/', 'name': 'Cleeneo', 'publisher': {'@id': f'{ORIGIN}/#org'},
         'inLanguage': 'en-SG'}]}


def product_ld():
    ship = {'@type': 'OfferShippingDetails', 'shippingRate': {'@type': 'MonetaryAmount', 'value': 0, 'currency': 'SGD'},
            'shippingDestination': {'@type': 'DefinedRegion', 'addressCountry': 'SG'},
            'deliveryTime': {'@type': 'ShippingDeliveryTime',
                             'handlingTime': {'@type': 'QuantitativeValue', 'minValue': 1, 'maxValue': 2, 'unitCode': 'DAY'},
                             'transitTime': {'@type': 'QuantitativeValue', 'minValue': 2, 'maxValue': 4, 'unitCode': 'DAY'}}}
    return {'@context': 'https://schema.org', '@type': 'Product', '@id': f'{ORIGIN}/#product',
            'name': 'Cleeneo Silk Nasal Strips', 'brand': {'@type': 'Brand', 'name': 'Cleeneo'},
            'image': [f'{IMG_ORIGIN}/img/share/kits.jpg', f'{IMG_ORIGIN}/img/share/home.jpg'],
            'description': 'Drug-free, latex-free silk nasal strips with three PET spring-tension bars that lift the nasal valve for easier nose breathing.',
            'material': 'Silk, PET, hypoallergenic adhesive',
            'aggregateRating': {'@type': 'AggregateRating', 'ratingValue': RATING[0], 'reviewCount': RATING[1], 'bestRating': '5'},
            'offers': [{'@type': 'Offer', 'name': k['name'], 'price': k['price'], 'priceCurrency': 'SGD', 'url': f'{ORIGIN}/kits/#{k["id"]}',
                        'eligibleQuantity': {'@type': 'QuantitativeValue', 'value': k['strips'], 'unitText': 'strips'},
                        'seller': {'@id': f'{ORIGIN}/#org'}, 'shippingDetails': ship} for k in KITS]}


def crumbs_ld(items):
    """items: [(name, path)] after Home."""
    lst = [('Home', '')] + items
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': html.unescape(n), 'item': f'{ORIGIN}/{p}'} for i, (n, p) in enumerate(lst)]}


def faq_ld(items):
    import re
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in items]}


def page(path, title, desc, body, active='', ld=None, share=None, kicker='Drug-free silk nasal strips · Singapore'):
    canonical = ORIGIN + BASE + path
    slug = path.strip('/').replace('/', '-') or 'home'
    headline = share or title.split(' | ')[0]
    SHARES[slug] = (headline, kicker)
    og_img = f'{IMG_ORIGIN}/img/share/{slug}.jpg'
    ld = (ld or []) + [{'@context': 'https://schema.org', '@type': 'WebPage', '@id': canonical, 'url': canonical, 'name': title,
                        'description': desc, 'isPartOf': {'@id': f'{ORIGIN}/#site'}, 'inLanguage': 'en-SG',
                        'primaryImageOfPage': {'@type': 'ImageObject', 'url': og_img, 'width': 1200, 'height': 630}}]
    nav = ''.join(f'<a href="{u(p)}"{" aria-current=\"page\"" if p == active else ""}>{n}</a>' for p, n in NAV[1:])
    mnav = ''.join(f'<a href="{u(p)}">{n}</a>' for p, n in NAV + FOOT_MORE)
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in [org_ld()] + ld)
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="p1-site" content="{SLUG}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Cleeneo">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:secure_url" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(headline)} | Cleeneo">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#004d53">
<link rel="icon" href="{u("favicon.ico")}" sizes="48x48">
<link rel="icon" href="{u("icon-96.png")}" type="image/png" sizes="96x96">
<link rel="icon" href="{u("icon-192.png")}" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{u("apple-touch-icon.png")}">
<link rel="manifest" href="{u("site.webmanifest")}">
<link rel="stylesheet" href="{u("cleeneo.css")}?v={ASSET_V}">
{lds}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
<span>Free delivery across Singapore on every kit <span class="hide-sm">· No subscription</span></span>
<span><a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {BIZ["disp"]}</a></span>
</div></div>
<header class="site"><div class="wrap">
<a class="logo" href="{u()}" aria-label="Cleeneo home">{mark()}<span>Cleeneo</span></a>
<nav class="main" aria-label="Main">{nav}</nav>
{wa_btn("Order on WhatsApp", ORDER_TEXT, "btn btn-wa hdr-cta")}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
</div>
<nav class="mobile-nav" id="mnav" aria-label="Mobile">{mnav}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="site"><div class="wrap">
<div class="grid">
<div>
<p class="flogo">{mark()}<span>Cleeneo</span></p>
<p>Drug-free, latex-free silk nasal strips, designed and run from Singapore. Free delivery on every kit, Singapore only.</p>
<p><a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {BIZ["disp"]}</a><br><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></p>
</div>
<div>
<h3>Nasal strips for</h3>
<ul><li><a href="{u("nasal-strips/snoring/")}">Snoring &amp; better sleep</a></li><li><a href="{u("nasal-strips/sports/")}">Sports &amp; training</a></li><li><a href="{u("nasal-strips/allergies/")}">Allergies &amp; congestion</a></li></ul>
</div>
<div>
<h3>Shop</h3>
<ul><li><a href="{u("kits/")}">Kits &amp; prices</a></li><li><a href="{u("how-to-use/")}">How to use</a></li><li><a href="{u("shipping/")}">Shipping &amp; returns</a></li></ul>
</div>
<div>
<h3>Cleeneo</h3>
<ul><li><a href="{u("about/")}">About</a></li><li><a href="{u("blog/")}">Blog</a></li><li><a href="{u("contact/")}">Contact</a></li></ul>
</div>
</div>
<p class="fine-note">{DOCTOR}</p>
<div class="fine"><span>© 2026 Cleeneo. All rights reserved.</span><a href="https://pageonesingapore.com/">Website &amp; SEO by Page One Singapore</a></div>
</div></footer>
<div class="dock">{wa_btn("Order on WhatsApp", ORDER_TEXT)}</div>
<script src="{u("cleeneo.js")}?v={ASSET_V}" defer></script>
</body>
</html>
'''


# ---------- shared blocks ----------
def page_hero(crumbs, h1, sub):
    trail = '<a href="' + u() + '">Home</a>' + ''.join(
        f' / <a href="{u(p)}">{n}</a>' if i < len(crumbs) - 1 else f' / <span>{n}</span>' for i, (n, p) in enumerate(crumbs))
    return (f'<section class="page-hero"><div class="wrap"><p class="crumbs">{trail}</p><h1>{h1}</h1>'
            f'<p>{sub}</p></div></section>')


def stars():
    return f'<span class="stars" aria-hidden="true">{ICON["star"] * 5}</span>'


def rating_line():
    return f'<p class="rating">{stars()}<span><strong>{RATING[0]}/5</strong> from {RATING[1]} verified reviews</span></p>'


def kit_cards(head=True):
    cards = []
    for k in KITS:
        per = float(k['price']) / k['strips']
        was = f'<s>S${k["was"]}</s>' if k['was'] else ''
        badge = f'<span class="badge">{k["badge"]}</span>' if k['badge'] else ''
        cards.append(f'''<article class="kit card" id="{k["id"]}">{badge}
<h3>{e(k["name"])}</h3>
<p class="strips">{k["strips"]} strips</p>
<p class="price"><span>S${k["price"]}</span>{was}</p>
<p class="per">About {per * 100:.0f}¢ a strip · {e(k["note"])}</p>
<ul class="ticks sm"><li>Free delivery in Singapore</li><li>One-time order, no subscription</li></ul>
{wa_btn("Order on WhatsApp", kit_text(k), "btn btn-wa wide")}
</article>''')
    return '<div class="grid g3 kits">' + ''.join(cards) + '</div>'


def reviews_block():
    q = ''.join(f'<blockquote class="card quote">{stars()}<p>“{e(t)}”</p><cite>{e(n)}</cite> <span class="muted">· verified buyer</span></blockquote>'
                for n, t in REVIEWS)
    return (f'<section><div class="wrap"><div class="sec-head"><h2>What customers say</h2>{rating_line()}</div>'
            f'<div class="grid g4 reviews" tabindex="0" role="region" aria-label="Customer reviews">{q}</div></div></section>')


def faq_html(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{e(q)}</summary><div><p>{a}</p></div></details>' for q, a in items) + '</div>'


def faq_block(items, heading='Questions'):
    return f'<section class="alt"><div class="wrap narrow"><div class="sec-head"><h2>{heading}</h2></div>{faq_html(items)}</div></section>'


def band(h, p, text=ORDER_TEXT, label='Order on WhatsApp', second=True):
    more = f'<a class="btn btn-ghost" href="{u("kits/")}">See kits &amp; prices</a>' if second else ''
    return (f'<section><div class="wrap"><div class="band"><div><h2>{h}</h2><p>{p}</p></div>'
            f'<div class="btns">{wa_btn(label, text)}{more}</div></div></div></section>')


def why_cards():
    items = [('shield', 'Drug-free &amp; latex-free', 'Works mechanically, not chemically. No medicine, no drowsiness, nothing to interact with.'),
             ('layers', 'Four-layer silk build', 'Three PET spring-tension bars under a soft silk layer, with a hypoallergenic adhesive.'),
             ('truck', 'Free Singapore delivery', 'Tracked and insured. Usually dispatched in 1–2 business days.'),
             ('repeat', 'No subscription', 'Order a pack when you need one. No auto-renewal and nothing to cancel.')]
    return ''.join(f'<div class="card"><div class="ico">{ICON[i]}</div><h3>{t}</h3><p>{d}</p></div>' for i, t, d in items)


def use_cards(skip=None):
    items = [('nasal-strips/snoring/', 'moon', 'Snoring &amp; sleep', 'Keep breathing through your nose at night, for quieter nights and better mornings.'),
             ('nasal-strips/sports/', 'run', 'Sports &amp; training', 'More air through your nose while you run, ride or train.'),
             ('nasal-strips/allergies/', 'leaf', 'Allergies &amp; congestion', 'Drug-free relief for a blocked nose from dust mites, mould and haze.')]
    return '<div class="grid g3 uses">' + ''.join(
        f'<a class="card use" href="{u(p)}"><div class="ico">{ICON[i]}</div><h3>{t}</h3><p>{d}</p><span class="more">Learn more →</span></a>'
        for p, i, t, d in items if p != skip) + '</div>'


STEPS = [
    ('Clean and dry', 'Wash the bridge of your nose and dry it fully. Oil, lotion or moisturiser stops the adhesive from holding.'),
    ('Find the spot', 'Peel off the liner and centre the strip across the bridge of your nose, just above where your nostrils flare.'),
    ('Press it down', 'Press the ends onto the sides of your nose and rub along the strip for 10 to 15 seconds so it bonds.'),
    ('Peel off gently', 'In the morning, wet the strip and peel slowly from the ends. Use a fresh strip each time.'),
]


def steps_html():
    return '<ol class="steps">' + ''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in STEPS) + '</ol>'


def doctor_note():
    return f'<p class="note">{DOCTOR}</p>'


FAQ = [
    ('How do nasal strips work?',
     'A Cleeneo strip has three flexible PET spring-tension bars. Once it is on the bridge of your nose, the bars try to straighten, which gently lifts the sides of your nose and widens the nasal valve, the narrowest part of your nasal airway. More air can then flow through your nose without effort.'),
    ('Are Cleeneo strips drug-free and latex-free?',
     'Yes. They work mechanically, not chemically, and use a hypoallergenic, latex-free adhesive.'),
    ('Can I sleep with them on?',
     'Yes. The adhesive and tension bar are made to hold through a full night’s sleep. Put a fresh strip on just before bed.'),
    ('How long can I wear one strip?',
     'The adhesive is designed to hold for up to 12 hours. Use a new strip for each night or each session.'),
    ('How fast is delivery in Singapore?',
     'Orders are dispatched within 1–2 business days (orders before 2pm SGT usually go out the next business day) and typically arrive 2–4 business days after dispatch. Delivery is free, tracked and insured.'),
    ('Do I need a subscription?',
     'No. Order a one-time pack or bundle whenever you need one. There is no auto-renewal and nothing to cancel.'),
    ('How do I order?',
     f'Pick a kit and tap “Order on WhatsApp”. Your kit is filled in for you; just add your name and delivery address and we will confirm your order and payment details in the chat. You can also email <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a>.'),
    ('Do you ship outside Singapore?',
     'Not at the moment. Cleeneo delivers within Singapore only, to residential, commercial and PO box addresses.'),
]
FAQ_BY = dict(FAQ)


def pick(*qs):
    return [(q, FAQ_BY[q]) for q in qs]


# ---------- pages ----------
def home():
    body = f'''
<section class="hero"><div class="wrap hero-grid">
<div>
<span class="eyebrow">Singapore brand · Drug-free · Latex-free</span>
<h1>Drug-Free Silk Nasal Strips for Better Sleep and Breathing</h1>
<p class="lead">Cleeneo strips sit on the bridge of your nose and gently lift the nasal valve, so air flows through your nose more easily. For snoring, a blocked nose, or more air while you train.</p>
{rating_line()}
<ul class="chips"><li>Trial kit S$9.90</li><li>Free delivery in Singapore</li><li>No subscription</li></ul>
<div class="btns">{wa_btn("Order on WhatsApp", ORDER_TEXT)}<a class="btn btn-line" href="{u("kits/")}">See kits &amp; prices</a></div>
</div>
<div class="hero-art">{photo("strip-in-hand", HAND_ALT, lazy=False)}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>Why Cleeneo</h2><p>A simple, mechanical way to breathe through your nose, made for Singapore and delivered free.</p></div>
<div class="grid g4 why">{why_cards()}</div>
</div></section>

<section class="alt"><div class="wrap split">
<div>{photo("strip-flat", FLAT_ALT)}</div>
<div>
<h2>How a nasal strip works</h2>
<p>Just inside your nostrils is the nasal valve, the narrowest part of the airway in your nose. When it narrows, from a cold, allergies, the shape of your nose or simply lying down, breathing through your nose takes more effort and many people switch to breathing through the mouth.</p>
<p>A Cleeneo strip acts like a small spring. Its three PET bars gently lift the sides of your nose, widening the nasal valve the moment it goes on. No drugs, no sprays, nothing to wear off.</p>
<a class="btn btn-line" href="{u("how-to-use/")}">How to put one on</a>
</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>Made for the moments you need to breathe</h2></div>
{use_cards()}
</div></section>

<section class="alt"><div class="wrap split">
<div>
<h2>Four layers, one strip</h2>
<p>Each Cleeneo strip is built in four layers, so it lifts firmly but feels soft on your skin.</p>
<ul class="ticks"><li><strong>Silk contact layer</strong> for a soft, breathable finish</li><li><strong>Three PET spring-tension bars</strong> for an even lift</li><li><strong>Hypoallergenic, latex-free adhesive</strong> that holds overnight</li><li><strong>Release liner</strong> you peel off before use</li></ul>
</div>
<div>{photo("strip-layers", LAYERS_ALT)}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>On in under a minute</h2></div>
{steps_html()}
</div></section>

<section class="alt" id="buy"><div class="wrap">
<div class="sec-head"><h2>Choose your kit</h2><p>All prices in Singapore dollars. Free delivery on every kit, Singapore only.</p></div>
{kit_cards()}
</div></section>

{reviews_block()}

{faq_block(pick("How do nasal strips work?", "Are Cleeneo strips drug-free and latex-free?", "Can I sleep with them on?", "How fast is delivery in Singapore?", "Do I need a subscription?", "How do I order?"), "Nasal strip FAQ")}

{band("Ready to breathe easier tonight?", "Start with the S$9.90 trial kit. Free delivery across Singapore.", kit_text(KITS[0]), "Order the trial kit")}
'''
    return page('', 'Cleeneo Nasal Strips | Drug-Free Snoring Relief Singapore',
                'Drug-free, latex-free silk nasal strips for snoring, sport and a blocked nose. Rated 4.9/5. Trial kit S$9.90 with free delivery across Singapore.',
                body, active='', ld=[product_ld(), faq_ld(pick("How do nasal strips work?", "Are Cleeneo strips drug-free and latex-free?", "Can I sleep with them on?", "How fast is delivery in Singapore?", "Do I need a subscription?", "How do I order?"))],
                share='Drug-Free Silk Nasal Strips for Better Sleep and Breathing')


USES = {
    'snoring': {
        'title': 'Nasal Strips for Snoring Singapore | Cleeneo',
        'desc': 'Drug-free silk nasal strips that help you keep breathing through your nose at night for quieter sleep. Trial kit S$9.90, free delivery in Singapore.',
        'h1': 'Nasal Strips for Snoring and Better Sleep',
        'sub': 'When your nose is open, you are more likely to keep breathing through it at night. Cleeneo gently lifts the nasal valve so you can.',
        'icon': 'moon',
        'sections': [
            ('Why a blocked nose leads to snoring',
             '<p>When the airway in your nose is narrow, breathing through it takes effort, so many sleepers end up breathing through the mouth. Mouth breathing lets air rattle past the soft tissue at the back of the throat, which is what you hear as snoring. It also leaves you with a dry mouth and a groggy start to the day.</p>'
             '<p>A Cleeneo strip widens the nasal valve from the outside, making it easier to stay with nose breathing through the night. For snoring that starts in the nose, that can mean quieter nights for you and whoever sleeps next to you.</p>'),
            ('A strip that lasts the night',
             '<ul class="ticks"><li>Hypoallergenic, latex-free adhesive made to hold through a full night</li><li>Soft silk layer that is comfortable on your skin</li><li>Peels off in the morning without leaving residue</li><li>Drug-free, so it is fine to use every night</li></ul>'),
            ('When to see a doctor',
             f'<p>{DOCTOR}</p>'),
        ],
        'faq': ['How do nasal strips work?', 'Can I sleep with them on?', 'Are Cleeneo strips drug-free and latex-free?', 'Do I need a subscription?'],
        'wa': 'Hi Cleeneo, I would like to try your nasal strips for snoring.',
    },
    'sports': {
        'title': 'Sports Nasal Strips for Running & Training | Cleeneo SG',
        'desc': 'Silk nasal strips for runners, cyclists and gym-goers in Singapore. More air through your nose while you train. Trial kit S$9.90, free delivery.',
        'h1': 'Sports Nasal Strips for Running, Cycling and Training',
        'sub': 'Keep breathing through your nose for longer as the effort goes up. Cleeneo opens the nasal valve so more air gets through with each breath.',
        'icon': 'run',
        'sections': [
            ('Why athletes use nasal strips',
             '<p>Many runners, cyclists and gym-goers train to breathe through the nose: it warms and filters the air and helps keep breathing calm and steady. As the effort rises, a narrow nasal valve is often what forces you to switch to mouth breathing.</p>'
             '<p>A Cleeneo strip gently lifts the sides of your nose, so more air can flow through it per breath. Many people find nose breathing feels easier for longer.</p>'),
            ('Made to stay on',
             '<ul class="ticks"><li>Adhesive designed to stay in place through sweat and movement</li><li>Low-profile silk finish under a cap, helmet or goggles</li><li>Drug-free, with nothing to declare or wear off</li></ul>'),
            ('How to use it for training',
             '<p>Put a strip on clean, dry skin before your warm-up and press it down well, so it bonds before you start sweating. Breathe through your nose during your session, then peel it off gently after your cool-down. Use a fresh strip each session.</p>'),
        ],
        'faq': ['How do nasal strips work?', 'How long can I wear one strip?', 'Are Cleeneo strips drug-free and latex-free?', 'How do I order?'],
        'wa': 'Hi Cleeneo, I would like to try your nasal strips for sport.',
    },
    'allergies': {
        'title': 'Nasal Strips for Allergies & Blocked Nose | Cleeneo SG',
        'desc': 'Drug-free nasal strips for a blocked nose from dust mites, mould or haze in Singapore. No drowsiness. Trial kit S$9.90, free delivery.',
        'h1': 'Nasal Strips for Allergies and a Blocked Nose',
        'sub': 'Singapore’s humidity means dust mites and mould all year round. Cleeneo opens your nose mechanically, with no medicine and no drowsiness.',
        'icon': 'leaf',
        'sections': [
            ('Drug-free relief for a stuffy nose',
             '<p>Allergies make the lining of the nose swell, which narrows the nasal valve even further. A Cleeneo strip lifts the sides of your nose from the outside, giving air more room to pass the moment it goes on.</p>'
             '<p>Because it works mechanically, there is no drowsiness, no rebound effect and nothing to build a dependency on. If you take allergy medication, keep following your doctor’s or pharmacist’s advice; the strip contains no medicine of its own.</p>'),
            ('Day or night',
             '<ul class="ticks"><li>Wear it at night when a blocked nose keeps you awake</li><li>Or during the day at home, at work or while travelling</li><li>Adhesive designed to hold for up to 12 hours</li><li>Hypoallergenic, latex-free adhesive and a soft silk layer</li></ul>'),
            ('Allergies all year round',
             '<p>Singapore has no pollen season to wait out. Dust mites, mould and the occasional haze are around all year, which is why many allergy sufferers keep a pack of strips at the bedside.</p>'),
        ],
        'faq': ['Are Cleeneo strips drug-free and latex-free?', 'How long can I wear one strip?', 'Can I sleep with them on?', 'How fast is delivery in Singapore?'],
        'wa': 'Hi Cleeneo, I would like to try your nasal strips for my allergies.',
    },
}


def use_page(key):
    p = USES[key]
    path = f'nasal-strips/{key}/'
    secs = ''.join(f'<section{" class=\"alt\"" if i % 2 else ""}><div class="wrap narrow"><h2>{h}</h2>{b}</div></section>'
                   for i, (h, b) in enumerate(p['sections']))
    items = pick(*p['faq'])
    body = (page_hero([('Nasal strips', 'kits/'), (p['h1'].split(' for ')[-1].split(' and ')[0].capitalize(), path)], p['h1'], p['sub'])
            + f'<section><div class="wrap split"><div>{photo("strip-flat", FLAT_ALT)}</div><div><h2>Try Cleeneo for {key}</h2>'
              f'<p>Start with the 10-strip trial kit for S$9.90, or save with a 30-strip pack. Free delivery across Singapore and no subscription.</p>'
              f'{rating_line()}<div class="btns">{wa_btn("Order on WhatsApp", p["wa"])}<a class="btn btn-line" href="{u("kits/")}">See kits &amp; prices</a></div></div></div></section>'
            + secs
            + f'<section class="alt"><div class="wrap"><div class="sec-head"><h2>How to put it on</h2></div>{steps_html()}</div></section>'
            + reviews_block()
            + f'<section class="alt"><div class="wrap"><div class="sec-head"><h2>Choose your kit</h2></div>{kit_cards()}</div></section>'
            + faq_block(items, 'Questions')
            + f'<section><div class="wrap"><div class="sec-head"><h2>Other ways people use Cleeneo</h2></div>{use_cards(path)}</div></section>')
    crumb = p['h1'].replace('Nasal Strips for ', '').replace('Sports Nasal Strips for ', '')
    ld = [crumbs_ld([('Nasal strips', 'kits/'), (crumb, path)]), faq_ld(items), product_ld()]
    return page(path, p['title'], p['desc'], body, active=path, ld=ld, share=p['h1'])


def how_to():
    items = [('Can I reuse a strip?', 'No. Use a fresh strip each night or each session, so the adhesive and the lift work as they should.'),
             ('The strip keeps coming off. What should I do?',
              'Make sure the skin is clean and completely dry, with no moisturiser or sunscreen on the nose. Press along the whole strip for 10 to 15 seconds after putting it on, and place it on the bridge just above the flare of the nostrils.'),
             ('Does it hurt to take off?',
              'It should not. Wet the strip with warm water first, then peel slowly from each end towards the middle.'),
             FAQ[3]]
    body = (page_hero([('How to use', 'how-to-use/')], 'How to Apply Nasal Strips for the Best Lift',
                      'Four simple steps. Placement matters most: on the bridge, just above where the nostrils flare.')
            + f'<section><div class="wrap">{steps_html()}</div></section>'
            + f'<section class="alt"><div class="wrap split"><div>{photo("strip-flat", FLAT_ALT)}</div><div><h2>Getting the position right</h2>'
              '<p>The strip works by lifting the sides of your nose at the nasal valve. Too high up on the bony part of the bridge and it has nothing to lift; too low and it sits on the soft tip. Feel for where the hard bridge ends and the softer sides of the nose begin, and centre the strip just there.</p>'
              '<ul class="ticks"><li>Clean, dry, oil-free skin</li><li>Centred, with both ends sitting evenly on the sides of the nose</li><li>Pressed firmly for 10 to 15 seconds</li></ul></div></div></section>'
            + faq_block(items, 'Tips and questions')
            + band('Try it tonight', 'The S$9.90 trial kit has 10 strips, with free delivery across Singapore.', kit_text(KITS[0]), 'Order the trial kit'))
    return page('how-to-use/', 'How to Apply Nasal Strips: Step by Step | Cleeneo',
                'How to put on a nasal strip for the best lift: clean and dry, find the spot, press for 10 to 15 seconds, and peel off gently in the morning.',
                body, active='how-to-use/', ld=[crumbs_ld([('How to use', 'how-to-use/')]), faq_ld(items), {
                    '@context': 'https://schema.org', '@type': 'HowTo', 'name': 'How to apply a Cleeneo nasal strip',
                    'step': [{'@type': 'HowToStep', 'position': i + 1, 'name': t, 'text': d} for i, (t, d) in enumerate(STEPS)]}],
                share='How to Apply Nasal Strips for the Best Lift')


def kits():
    opts = ''.join(f'<option value="{k["id"]}">{e(k["name"])}: {k["strips"]} strips, S${k["price"]}</option>' for k in KITS)
    body = (page_hero([('Kits &amp; prices', 'kits/')], 'Cleeneo Nasal Strip Kits and Prices',
                      'Three simple options, all with free delivery across Singapore and no subscription.')
            + f'<section><div class="wrap">{kit_cards()}</div></section>'
            + f'''<section class="alt" id="order"><div class="wrap split top">
<div>
<h2>Order on WhatsApp</h2>
<p>Choose your kit and fill in your delivery details. Tapping the button opens WhatsApp with your order typed out, ready to send. We will confirm your order and payment details in the chat.</p>
<ul class="ticks"><li>Free delivery, tracked and insured</li><li>Orders before 2pm SGT usually go out the next business day</li><li>Typically arrives 2–4 business days after dispatch</li></ul>
<p class="muted">Prefer email? Send your order to <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a>.</p>
</div>
<form class="card form" id="oform">
<label class="f" for="o-kit">Kit</label><select id="o-kit" required>{opts}</select>
<label class="f" for="o-qty">Quantity</label><select id="o-qty">{''.join(f'<option>{n}</option>' for n in range(1, 6))}</select>
<label class="f" for="o-name">Name</label><input id="o-name" type="text" autocomplete="name" required>
<label class="f" for="o-addr">Delivery address</label><textarea id="o-addr" autocomplete="street-address" required></textarea>
<label class="f" for="o-postal">Postal code</label><input id="o-postal" type="text" inputmode="numeric" autocomplete="postal-code" pattern="[0-9]{{6}}" required>
<button class="btn btn-wa wide" type="submit">{ICON["wa"]}Send order on WhatsApp</button>
<p class="small muted">Singapore addresses only.</p>
</form>
</div></section>'''
            + reviews_block()
            + faq_block(pick('How do I order?', 'How fast is delivery in Singapore?', 'Do I need a subscription?', 'Do you ship outside Singapore?'), 'Ordering questions'))
    data = json.dumps({k['id']: {'name': k['name'], 'strips': k['strips'], 'price': k['price']} for k in KITS})
    body += f'<script>window.CLEENEO_KITS={data};</script>'
    return page('kits/', 'Buy Nasal Strips Online in Singapore: Kits & Prices | Cleeneo',
                'Cleeneo silk nasal strips: 10-strip trial kit S$9.90, 30-strip pack S$21.90, 90-strip bundle S$43.80. Free delivery in Singapore, no subscription.',
                body, active='kits/', ld=[crumbs_ld([('Kits & prices', 'kits/')]), product_ld(),
                                          faq_ld(pick('How do I order?', 'How fast is delivery in Singapore?', 'Do I need a subscription?', 'Do you ship outside Singapore?'))],
                share='Nasal Strip Kits from S$9.90 with Free Delivery')


def shipping():
    items = [('Is delivery really free?', 'Yes. Delivery is free on every kit, with no minimum order.'),
             FAQ[7],
             ('How do I track my order?', f'Your parcel is tracked. If you need an update, WhatsApp us on <a href="{wa_link("Hi Cleeneo, can I have an update on my order?")}" target="_blank" rel="noopener">{BIZ["disp"]}</a> or email <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a>.')]
    body = (page_hero([('Shipping &amp; returns', 'shipping/')], 'Shipping and Delivery Across Singapore',
                      'Free, tracked and insured delivery on every order. Singapore only.')
            + f'''<section><div class="wrap grid g3">
<div class="card"><div class="ico">{ICON["truck"]}</div><h3>Free delivery</h3><p>Free on every kit, with no minimum order. Tracked and insured.</p></div>
<div class="card"><div class="ico">{ICON["repeat"].replace('<path d="M2 2l20 20"/>', '')}</div><h3>Fast dispatch</h3><p>Orders before 2pm SGT are dispatched the next business day. Later or weekend orders go out within 1–2 business days.</p></div>
<div class="card"><div class="ico">{ICON["plane"]}</div><h3>Singapore only</h3><p>Arrives typically 2–4 business days after dispatch, to residential, commercial and PO box addresses. No international shipping.</p></div>
</div></section>
<section class="alt"><div class="wrap narrow">
<h2>Returns and problems with an order</h2>
<p>If your order arrives damaged, or there is a problem with your strips, email <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a> within 14 days of delivery and we will sort it out promptly.</p>
<p>For hygiene reasons, opened packs cannot be returned. Quality issues are always looked after.</p>
</div></section>'''
            + faq_block(items, 'Delivery questions')
            + band('Free delivery on every kit', 'Order on WhatsApp in a minute.'))
    return page('shipping/', 'Shipping & Delivery Across Singapore | Cleeneo',
                'Free, tracked and insured delivery across Singapore on every Cleeneo order. Dispatched in 1–2 business days, arriving in 2–4. Singapore only.',
                body, active='', ld=[crumbs_ld([('Shipping & returns', 'shipping/')]), faq_ld(items)],
                share='Free, Tracked Delivery Across Singapore')


def about():
    body = (page_hero([('About', 'about/')], 'About Cleeneo',
                      'A Singapore brand making premium silk nasal strips for effortless breathing.')
            + f'''<section><div class="wrap split">
<div>
<h2>Breathe easier, sleep deeper</h2>
<p>Cleeneo makes silk nasal strips that gently lift the nasal passages, so you can breathe through your nose more easily. They are made for nighttime congestion, mouth breathing and snoring, and for anyone who wants clearer airflow: sleepers, athletes, travellers and allergy sufferers.</p>
<p>Every strip uses the same four-layer build: three PET spring-tension bars, a soft silk layer and a hypoallergenic, latex-free adhesive. No drugs, no sprays.</p>
<p>Cleeneo is founded and run from Singapore, with one simple mission: help people wake up rested.</p>
</div>
<div>{photo("strip-layers", LAYERS_ALT)}</div>
</div></section>
<section class="alt"><div class="wrap grid g3">
<div class="card"><div class="ico">{ICON["wind"]}</div><h3>Effortless breathing</h3><p>A firm, even lift that opens the nasal valve without discomfort.</p></div>
<div class="card"><div class="ico">{ICON["plane"]}</div><h3>Who it’s for</h3><p>Sleepers, athletes, travellers and anyone who wants clearer airflow.</p></div>
<div class="card"><div class="ico">{ICON["shield"]}</div><h3>Singapore-based</h3><p>Designed and run locally, with free, fast delivery across Singapore.</p></div>
</div></section>'''
            + reviews_block()
            + band('Questions about Cleeneo?', 'WhatsApp or email us, including for wholesale orders and partnerships.', WA_TEXT, 'WhatsApp us', second=False))
    return page('about/', 'About Cleeneo | Silk Nasal Strips Designed in Singapore',
                'Cleeneo is a Singapore brand of drug-free, latex-free silk nasal strips for sleepers, athletes, travellers and allergy sufferers.',
                body, active='', ld=[crumbs_ld([('About', 'about/')])], share='Silk Nasal Strips, Designed and Run in Singapore')


def contact():
    body = (page_hero([('Contact', 'contact/')], 'Contact Cleeneo',
                      'Questions, orders, wholesale or partnerships. WhatsApp is the fastest way to reach us.')
            + f'''<section><div class="wrap split top">
<div class="grid">
<div class="card"><div class="ico">{ICON["wa"]}</div><h3>WhatsApp</h3><p><a href="{wa_link()}" target="_blank" rel="noopener">{BIZ["disp"]}</a></p>{wa_btn("Chat on WhatsApp")}</div>
<div class="card"><div class="ico">{ICON["mail"]}</div><h3>Email</h3><p><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a><br><span class="muted">For questions, wholesale orders and partnerships.</span></p></div>
<div class="card"><div class="ico">{ICON["truck"]}</div><h3>Delivery</h3><p>Singapore only. Free, tracked and insured. <a href="{u("shipping/")}">Shipping details</a></p></div>
</div>
<form class="card form" id="qform">
<h2 class="h3">Send us a message</h2>
<label class="f" for="q-name">Name</label><input id="q-name" type="text" autocomplete="name" required>
<label class="f" for="q-contact">Phone or email</label><input id="q-contact" type="text" autocomplete="email" required>
<label class="f" for="q-msg">Message</label><textarea id="q-msg" required></textarea>
<div class="btns"><button class="btn btn-wa" type="submit">{ICON["wa"]}Send on WhatsApp</button><button class="btn btn-line" type="button" id="q-mail">Send by email</button></div>
</form>
</div></section>'''
            + faq_block(pick('How do I order?', 'How fast is delivery in Singapore?', 'Do you ship outside Singapore?'), 'Before you message'))
    return page('contact/', 'Contact Cleeneo | WhatsApp 8060 4977',
                'Contact Cleeneo on WhatsApp 8060 4977 or sales@cleeneo.co for orders, questions, wholesale and partnerships. Singapore delivery only.',
                body, active='contact/', ld=[crumbs_ld([('Contact', 'contact/')]), faq_ld(pick('How do I order?', 'How fast is delivery in Singapore?', 'Do you ship outside Singapore?'))],
                share='Contact Cleeneo: WhatsApp 8060 4977')


POSTS = [{
    'slug': 'do-nasal-strips-really-help-with-snoring',
    'title': 'Do Nasal Strips Really Help With Snoring and Mouth Breathing?',
    'seo': 'Do Nasal Strips Help With Snoring? How They Work | Cleeneo',
    'desc': 'How nasal strips open the nasal valve, why nose breathing matters for sleep, what to look for in a good strip, and how to apply one properly.',
    'date': '2026-10-11', 'date_disp': '11 October 2026',
    'body': [
        ('', '<p>Waking up with a dry mouth, feeling groggy, or being told you snore are often signs of the same thing: breathing through your mouth at night because your nose is partly blocked. Nasal strips are a simple, non-invasive way to help. Here is how they work, when they help, and what makes a good one.</p>'),
        ('How nasal strips work', '<p>The narrowest part of the airway in your nose is the <strong>nasal valve</strong>, just inside the nostrils. Even a small narrowing here makes breathing through your nose noticeably harder. A nasal strip works like a flexible spring: once it is pressed onto the bridge of the nose, its bars try to straighten, gently lifting the side walls of the nose away from the middle. The valve widens and air flows in with less resistance.</p><p>Because the strip works purely through tension, there is no medicine involved, so nothing wears off and nothing interacts with other things you take.</p>'),
        ('Why nose breathing matters for sleep', '<p>Your nose warms, humidifies and filters the air before it reaches your lungs, and the sinuses add nitric oxide to the air you breathe in. When the nose is blocked and you switch to breathing through your mouth, air moves past the soft tissue at the back of the throat and can make it vibrate. That vibration is snoring.</p><p>So for snoring that starts with a blocked or narrow nose, keeping the nose open can make a real difference. Strips will not fix every kind of snoring, though. Snoring caused by the throat, the tongue or sleep apnoea needs a doctor’s advice.</p>'),
        ('What to look for in a good nasal strip', '<h3>1. More than one tension bar</h3><p>Several flexible bars lift more evenly than a single band, and hold the nasal passages open more consistently through the night.</p><h3>2. A breathable, soft material</h3><p>Soft materials such as silk sit comfortably on the skin and follow the shape of the nose. Rubbery or heavy plastic strips can trap sweat and oil and lift off.</p><h3>3. A skin-friendly adhesive</h3><p>The adhesive should hold all night but come off without red marks. Latex-free, hypoallergenic adhesives are kinder to sensitive skin.</p>'),
        ('How to apply a nasal strip properly', '<ol><li><strong>Clean your skin.</strong> Wash and fully dry your nose so there is no oil or moisturiser.</li><li><strong>Find the right position.</strong> Centre the strip on the bridge of your nose, just above where the nostrils flare.</li><li><strong>Press and secure.</strong> Rub along the strip for 10 to 15 seconds so the adhesive bonds.</li><li><strong>Remove it gently.</strong> In the morning, wet the strip and peel slowly from both ends.</li></ol>'),
        ('When to see a doctor', f'<p>{DOCTOR}</p>'),
        ('Try Cleeneo', '<p>Cleeneo strips have three PET spring-tension bars under a soft silk layer, with a hypoallergenic, latex-free adhesive. The 10-strip trial kit is S$9.90 with free delivery across Singapore, and there is no subscription.</p>'),
    ],
}]


def blog():
    cards = ''.join(f'<a class="card use" href="{u("blog/" + p["slug"] + "/")}"><p class="muted small">{p["date_disp"]}</p><h3>{e(p["title"])}</h3><p>{e(p["desc"])}</p><span class="more">Read more →</span></a>' for p in POSTS)
    body = (page_hero([('Blog', 'blog/')], 'The Cleeneo Blog', 'Plain guides to nose breathing, snoring and sleeping better.')
            + f'<section><div class="wrap grid g2">{cards}</div></section>')
    return page('blog/', 'Blog: Nose Breathing, Snoring & Sleep | Cleeneo',
                'Guides from Cleeneo on nasal strips, nose breathing, snoring and better sleep in Singapore.',
                body, active='', ld=[crumbs_ld([('Blog', 'blog/')])], share='Guides to Nose Breathing, Snoring and Better Sleep')


def post(p):
    path = f'blog/{p["slug"]}/'
    secs = ''.join((f'<h2>{h}</h2>' if h else '') + b for h, b in p['body'])
    body = (page_hero([('Blog', 'blog/'), ('Article', path)], e(p['title']), f'By Cleeneo · {p["date_disp"]}')
            + f'<section><div class="wrap narrow article">{secs}<div class="btns" style="margin-top:24px">{wa_btn("Order the trial kit", kit_text(KITS[0]))}'
              f'<a class="btn btn-line" href="{u("kits/")}">See kits &amp; prices</a></div></div></section>')
    ld = [crumbs_ld([('Blog', 'blog/'), (p['title'], path)]), {
        '@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': p['title'], 'description': p['desc'],
        'datePublished': p['date'], 'dateModified': '2026-10-13', 'author': {'@type': 'Organization', 'name': 'Cleeneo', 'url': f'{ORIGIN}/'},
        'publisher': {'@id': f'{ORIGIN}/#org'}, 'mainEntityOfPage': f'{ORIGIN}/{path}',
        'image': f'{IMG_ORIGIN}/img/share/blog-{p["slug"]}.jpg'}]
    return page(path, p['seo'], p['desc'], body, active='', ld=ld, share=p['title'])


def not_found():
    global ABS
    ABS = True
    try:
        body = (page_hero([('Page not found', '')], 'Sorry, that page isn’t here',
                          'It may have moved when the Cleeneo site was updated. These links will get you back on track.')
                + f'<section><div class="wrap">{use_cards()}<p style="margin-top:20px" class="btns"><a class="btn btn-line" href="{u()}">Home</a><a class="btn btn-line" href="{u("kits/")}">Kits &amp; prices</a>{wa_btn("WhatsApp us")}</p></div></section>')
        html_ = page('404.html', 'Page not found | Cleeneo', 'This page does not exist on cleeneo.co.', body)
    finally:
        ABS = False
        SHARES.pop('404.html', None)
    return html_.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex, follow">')


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)


PAGES = []


def build(rel, fn, *args):
    global DEPTH
    DEPTH = rel.count('/')
    write(rel, fn(*args))
    if rel.endswith('index.html'):
        PAGES.append(rel[:-len('index.html')])


def robots_txt():
    return f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n'


def sitemap():
    urls = ''.join(f'<url><loc>{ORIGIN}/{p}</loc><lastmod>2026-10-13</lastmod></url>' for p in PAGES)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


def llms_txt():
    kits = '\n'.join(f'- {k["name"]}: {k["strips"]} strips, S${k["price"]}' for k in KITS)
    return f'''# Cleeneo

> Singapore brand of drug-free, latex-free silk nasal strips. A spring-tension bar lifts the nasal valve for easier nose breathing, for snoring, sport and allergy congestion. Free delivery across Singapore (Singapore only), no subscription.

- Orders and questions: WhatsApp +65 {BIZ["disp"]} (https://wa.me/{BIZ["wa"]}), email {BIZ["email"]}
- Rated {RATING[0]}/5 from {RATING[1]} verified reviews

## Kits (SGD, free delivery)
{kits}

## Pages
- [Home]({ORIGIN}/)
- [Nasal strips for snoring]({ORIGIN}/nasal-strips/snoring/)
- [Sports nasal strips]({ORIGIN}/nasal-strips/sports/)
- [Nasal strips for allergies]({ORIGIN}/nasal-strips/allergies/)
- [How to use]({ORIGIN}/how-to-use/)
- [Kits and prices]({ORIGIN}/kits/)
- [Shipping and returns]({ORIGIN}/shipping/)
- [About]({ORIGIN}/about/)
- [Contact]({ORIGIN}/contact/)
- [Blog]({ORIGIN}/blog/)
'''


def manifest():
    return json.dumps({'name': 'Cleeneo', 'short_name': 'Cleeneo', 'start_url': './', 'display': 'browser',
                       'background_color': '#ffffff', 'theme_color': '#004d53',
                       'icons': [{'src': f'icon-{s}.png', 'sizes': f'{s}x{s}', 'type': 'image/png'} for s in (192, 512)]}, indent=1)


def main():
    build('index.html', home)
    for k in USES:
        build(f'nasal-strips/{k}/index.html', use_page, k)
    build('nasal-strips/index.html', lambda: redirect_page('../kits/'))
    PAGES.remove('nasal-strips/')
    build('how-to-use/index.html', how_to)
    build('kits/index.html', kits)
    build('shipping/index.html', shipping)
    build('about/index.html', about)
    build('contact/index.html', contact)
    build('blog/index.html', blog)
    for p in POSTS:
        build(f'blog/{p["slug"]}/index.html', post, p)
    build('404.html', not_found)
    build('robots.txt', robots_txt)
    build('sitemap.xml', sitemap)
    build('llms.txt', llms_txt)
    build('site.webmanifest', manifest)
    write(f'{INDEXNOW_KEY}.txt', INDEXNOW_KEY)
    for d in ('img', 'img/share'):
        write(f'{d}/index.html', '')
    print('pages', len(PAGES))
    cards = {s: {'headline': h, 'kicker': k} for s, (h, k) in SHARES.items()}
    with open(os.path.join(HERE, 'share-cards.json'), 'w') as f:
        json.dump({'cards': cards, 'photo': os.path.join(HERE, 'source', 'photos', 'strip-in-hand.png'),
                   'mark': os.path.join(HERE, 'source', 'photos', 'mark-512.png')}, f, ensure_ascii=False)
    if os.environ.get('SKIP_IMAGES') != '1':
        env = dict(os.environ)
        if 'NODE_PATH' not in env:
            env['NODE_PATH'] = subprocess.run(['npm', 'root', '-g'], capture_output=True, text=True).stdout.strip()
        subprocess.run(['node', os.path.join(HERE, 'share.mjs')], check=True, env=env)


def redirect_page(to):
    return (f'<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url={to}"><link rel="canonical" href="{ORIGIN}/kits/"><title>Cleeneo</title></head>'
            f'<body><p><a href="{to}">Cleeneo kits and prices</a></p></body></html>')


if __name__ == '__main__':
    main()
