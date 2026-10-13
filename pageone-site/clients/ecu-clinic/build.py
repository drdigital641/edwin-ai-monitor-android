#!/usr/bin/env python3
"""Build The ECU Clinic website (page 1: the home page).

Built once into pageonesingapore.com/preview/ecu-clinic/ and never moved: on activation the client's
domain is pointed at that same folder. Every internal link is relative so the files work at both
addresses. While MOCKUP is True the page is noindex, carries the yellow preview strip, and its
canonical/structured-data URLs name the preview address; at activation set MOCKUP = False and ORIGIN
to the confirmed domain.

    python3 prep.py    # web photos, logo and icons (only when source photos change)
    python3 build.py   # writes the pages into ./site and the share image

Facts come only from source/content.md (the client's logo, flyers and Edwin's notes).
ecu.css, ecu.js and img/ live in ./site.
"""
import html
import json
import os
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')
SLUG = 'ecu-clinic'  # Page One client key: p1-site marker (go-live check) and WhatsApp tracker
PREVIEW = 'https://pageonesingapore.com/preview/ecu-clinic'
MOCKUP = False  # live on theecuclinicsg.com since 13 Oct 2026 (Edwin's go-ahead)
ORIGIN = PREVIEW if MOCKUP else 'https://theecuclinicsg.com'  # domain chosen by Edwin, 13 Oct 2026
BASE = '/'
DEPTH = 0
ASSET_V = '6'
# Until go-live the share image and icons are linked at the preview address (the same files).
LIVE = False
IMG_ORIGIN = ORIGIN if LIVE else PREVIEW
# Photos (img/), the share image and icon-512 are served from jsDelivr, pinned to the commit that
# holds them, because the Bluehost Bridge only takes files pasted inline. To serve them from the
# client's own domain instead, upload site/img/ and icon-512.png via cPanel and set IMG_CDN = None.
IMG_COMMIT = '22da05f017c842c1dea6cdd32178b29a7d760a43'
IMG_CDN = f'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@{IMG_COMMIT}/pageone-site/clients/ecu-clinic/site/'
if IMG_CDN:
    IMG_ORIGIN = IMG_CDN.rstrip('/')
SHARES = {}
HERO = 'mercedes-esp-pumps'  # hero background photo (prep.py makes the -lg version)

BIZ = {
    'name': 'The ECU Clinic',
    'contact': 'Ching',
    'tel': '+6598931923', 'tel_disp': '9893 1923',
    'wa': '6598931923',
    'facebook': 'https://www.facebook.com/TheECUclinicSG',
    'building': 'Premier @ Kaki Bukit',
    'street': '8 Kaki Bukit Avenue 4, #06-43',
    'postal': '415875',
    'map': 'Premier @ Kaki Bukit, 8 Kaki Bukit Avenue 4, Singapore 415875',
}
WA_TEXT = 'Hi The ECU Clinic, I need help with my car. Car model: \nChassis no.: \nFault code: '
WARRANTY = '6-month warranty'
HOURS_TXT = 'Monday to Friday, 9am to 7pm. Saturday, 9am to 3pm. Closed on Sundays and public holidays. WhatsApp enquiries are welcome 24/7, and after-hours appointments can be arranged.'

ICON = {
    'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8.2 8.2 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.4 3.4 0 0 0-1 2.5 5.9 5.9 0 0 0 1.2 3.1 13.5 13.5 0 0 0 5.2 4.6c1.9.8 2.7.9 3.6.7a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.2-.3-.3-.6-.4zM12 21.8a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.8 17.8L.1 24l6.3-1.7a11.8 11.8 0 0 0 5.6 1.4A11.8 11.8 0 0 0 20.4 3.6z"/></svg>',
    'chip': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/></svg>',
    'swap': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M17 3l4 4-4 4M21 7H7M7 21l-4-4 4-4M3 17h14"/></svg>',
    'code': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M8 7l-5 5 5 5M16 7l5 5-5 5M14 4l-4 16"/></svg>',
    'brake': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v2M12 19v2M3 12h2M19 12h2"/></svg>',
    'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
    'users': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></svg>',
    'truck': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
}

# WhatsApp and phone icons repeat on every button: draw them once in a hidden sprite and reuse them.
SPRITE = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">'
          + ICON['wa'].replace('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">', '<symbol id="i-wa" viewBox="0 0 24 24">').replace('</svg>', '</symbol>')
          + ICON['phone'].replace('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">', '<symbol id="i-phone" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">').replace('</svg>', '</symbol>')
          + '</svg>')
ICON['wa'] = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><use href="#i-wa"/></svg>'
ICON['phone'] = '<svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-phone"/></svg>'

e = html.escape


def u(path=''):
    if IMG_CDN and (path.startswith('img/') or path == 'icon-512.png'):
        return IMG_CDN + path
    return ('../' * DEPTH or './') + path


def wa_link(text=WA_TEXT):
    return f'https://wa.me/{BIZ["wa"]}?text={quote(text)}'


def cta_buttons(dark=False):
    call = 'btn-ghost' if dark else 'btn-red'
    return (f'<div class="btns">'
            f'<a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}<span class="lg">WhatsApp {BIZ["tel_disp"]}</span><span class="sm">WhatsApp us</span></a>'
            f'<a class="btn {call}" href="tel:{BIZ["tel"]}">{ICON["phone"]}Call {BIZ["contact"]}</a></div>')


def img(name, alt, w=640, h=480, lazy=True, cls=''):
    return (f'<img src="{u("img/" + name + ".webp")}" width="{w}" height="{h}" alt="{e(alt)}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async"{f" class=\"{cls}\"" if cls else ""}>')


# ---------- content (facts from source/content.md only) ----------
# 13 Oct 2026 client amendments: lead with ABS pump repair and brake fault diagnosis; ECU work is not
# featured (the client is still learning it); add Mercedes 7G/9G TCU repair, Mercedes steering lock
# (ELV) repair and brand-new OEM hybrid batteries; no BMW or Mercedes key programming.
SERVICES = [
    ('abs', 'ABS Pump &amp; Module Repair', 'abs-esc-units-bench', 'ABS and ESC units on the repair bench',
     'ABS, ESP or ESC warning light? We repair the pump and module, or supply a used or reconditioned unit.',
     ['ABS, ESP and ESC module repair', 'Used and recon ABS pumps', 'Mercedes-Benz ESP units',
      'Hyundai and Kia ESC units', 'Toyota Voxy, Noah and Sienta: repair, replace, used or recon', 'Plug and play available']),
    ('tcu', 'Mercedes 7-Speed &amp; 9-Speed TCU Repair', 'mercedes-7g-conductor-plate',
     'Mercedes 7-speed gearbox conductor plate with new filter, gasket and gearbox oil',
     'Gearbox warning, harsh shifts or stuck in one gear? We diagnose and repair the transmission control unit (TCU) on Mercedes 7-speed and 9-speed automatics.',
     ['7G-Tronic (722.9) TCU and conductor plate', '9G-Tronic TCU', 'Fault code reading and diagnosis',
      'New filter, pan gasket and gearbox oil fitted on the same job']),
    ('elv', 'Mercedes Steering Lock (ELV) Repair', 'mercedes-elv', 'Mercedes-Benz electronic steering lock on the bench',
     'Key won’t turn, or the car won’t start because of the steering lock? We repair the electronic steering lock (ELV) on Mercedes-Benz.',
     ['Mercedes-Benz ELV diagnosis', 'Steering lock repair', 'WhatsApp us your model and the symptoms']),
    ('hybrid', 'Hybrid Battery Replacement', 'hybrid-battery-pack', 'Brand-new hybrid battery pack ready to fit',
     'Hybrid battery warning or a weak battery? We replace it with a brand-new OEM hybrid battery.',
     ['Brand-new OEM hybrid batteries', 'Warranty: 1 year or 100,000 km', 'Removal and fitting', 'WhatsApp us your car model and year to check availability']),
]

WHY = [
    ('brake', 'ABS and brake system focus', 'ABS pumps, modules and brake system faults are our main work.'),
    ('chip', 'Board-level repair', 'Where we can, we repair the unit itself, down to the circuit board.'),
    ('swap', 'Repair, recon, used or new', 'More than one way to fix it: repair, reconditioned, used or new units.'),
    ('users', 'Over a decade of experience', 'Our team has more than ten years of experience with car electronics.'),
    ('truck', 'Pick-up and delivery', 'Can’t come in? Pick-up and delivery service is available.'),
    ('shield', '6-month warranty', 'Our repairs come with a 6-month warranty.'),
]

MAKES = ['Audi', 'BMW', 'Chevrolet', 'Honda', 'Hyundai', 'Kia', 'Mercedes-Benz', 'Mini', 'Nissan', 'Skoda', 'Toyota',
         'Volkswagen', 'Volvo', 'and more']

BMW_MODELS = [
    ('1 Series', 'F20, F21, F40'), ('2 Series', 'F22, F23, F45, F46, G42'), ('3 Series', 'F30, F31, F34, G20, G21'),
    ('4 Series', 'F32, F33, F36, F82, G22, G23'), ('5 Series', 'F07 GT, F10, F11, G30, G31'), ('6 Series', 'F06, F12, F13, G32'),
    ('7 Series', 'F01, F02, G11, G12'), ('8 Series', 'G14, G15, G16'), ('X1', 'E84, F48, U11'), ('X2', 'F39, U10'),
    ('X3', 'F25, G01'), ('X4', 'F26, G02'), ('X5', 'E70, F15, G05'), ('X6', 'E71, F16, G06'), ('M2', 'F87, G87'), ('Z4', 'G29'),
]

GALLERY = [
    ('mercedes-esp-pumps', 'Mercedes-Benz ESP pumps on the bench'),
    ('hyundai-kia-esc', 'Hyundai / Kia ESC unit'),
    ('mercedes-7g-conductor-plate', 'Mercedes 7-speed TCU job'),
    ('hybrid-battery-modules', 'Hybrid battery with new modules'),
    ('abs-esc-units-bench', 'ABS and ESC units for repair'),
    ('abs-pump-in-car', 'ABS pump in the engine bay'),
    ('mercedes-elv', 'Mercedes steering lock (ELV)'),
    ('elv-units', 'Steering lock units'),
    ('hybrid-battery-side', 'Brand-new hybrid battery pack'),
    ('active-brake-assist-warning', 'Mercedes brake assist warning'),
    ('mini-fuse-box', 'Mini fuse box module'),
    ('control-board-bench', 'Control board on the repair bench'),
]

WARNINGS = ['ABS warning light', 'ESP or ESC warning', 'Brake system warning',
            '“Active Brake Assist functions limited” (Mercedes)', 'Gearbox warning or limp mode (Mercedes)',
            'Steering lock or no-start fault (Mercedes)', 'Hybrid system warning']

STEPS = [
    ('WhatsApp us the details', f'Send your car model, chassis number and the fault code to <a href="{wa_link()}" target="_blank" rel="noopener">{BIZ["tel_disp"]}</a>. A photo of the scan tool screen or warning light helps.'),
    ('We check and advise', 'We tell you what we can do: repair your unit, or supply a recon, used or new one.'),
    ('Drop off or pick-up', f'Bring the car or part to us at {BIZ["building"]}, or use our pick-up and delivery service.'),
    ('Fixed, with warranty', 'Your car is back on the road, and the repair comes with a 6-month warranty.'),
]

FAQ = [
    ('What should I send when I WhatsApp you?',
     f'Your car model, chassis number and the fault code. A photo of the scan tool screen or the warning light on the dashboard also helps. WhatsApp <a href="{wa_link()}" target="_blank" rel="noopener">{BIZ["tel_disp"]}</a>.'),
    ('Can you repair my ABS pump or module?',
     'Yes. We repair ABS, ESP and ESC modules and supply used and reconditioned ABS pumps for makes such as Toyota, Honda, Mercedes-Benz, Hyundai, Kia, Volkswagen, Audi, Nissan, Volvo and Chevrolet. For Toyota Voxy, Noah and Sienta we repair, replace or supply used and recon ABS pumps and modules, with plug and play available.'),
    ('My Mercedes says “Active Brake Assist functions limited”. Can you help?',
     'Yes. WhatsApp us a photo of the dashboard and the fault code. We diagnose brake system warnings like this one and tell you what is causing it before any part is changed.'),
    ('Do you repair Mercedes 7-speed and 9-speed gearboxes?',
     'We repair the transmission control unit (TCU) on Mercedes 7G-Tronic (722.9) and 9G-Tronic automatic gearboxes. Send us the car model, chassis number and fault code.'),
    ('Do you repair Mercedes steering locks?',
     'Yes. We repair the electronic steering lock (ELV) on Mercedes-Benz cars. WhatsApp us your model and what the car is doing.'),
    ('What hybrid batteries do you fit?',
     'Brand-new OEM hybrid batteries, with a warranty of 1 year or 100,000 km. WhatsApp us your car model and year and we will check availability and price.'),
    ('Which car brands do you work on?',
     'Continental and Asian cars, including Audi, BMW, Chevrolet, Honda, Hyundai, Kia, Mercedes-Benz, Mini, Nissan, Skoda, Toyota, Volkswagen and Volvo. If your car isn’t listed, WhatsApp us the model and we will tell you.'),
    ('Is there a warranty?',
     'Yes. Our repairs come with a 6-month warranty. Brand-new hybrid batteries come with a warranty of 1 year or 100,000 km.'),
    ('Can you collect my car or part?',
     'Yes. Pick-up and delivery service is available. WhatsApp us your location and what needs to be collected.'),
    ('Which BMWs can have temperature programming?',
     'Most BMW models from 2010 to 2018, including the 1 to 8 Series, X1 to X6, M2 and Z4. See the full list on this page, or WhatsApp us your model to check.'),
    ('Where are you and when are you open?',
     f'We are at {BIZ["building"]}, {BIZ["street"]}, Singapore {BIZ["postal"]}. {HOURS_TXT}'),
]

# '#x' links go to a section of the home page; 'x/' links go to a page (both relative, via href()).
NAV = [('#services', 'Services'), ('articles/', 'Articles'), ('#how', 'How it works'),
       ('#gallery', 'Our work'), ('#faq', 'FAQ'), ('#contact', 'Contact')]

from pages import SERVICE_PAGES, ARTICLES
SP = {sp['key']: sp for sp in SERVICE_PAGES}
ART = {a['slug']: a for a in ARTICLES}


def href(p):
    return u() + p if p.startswith('#') else u(p)


def schema():
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': 'AutoRepair', '@id': f'{ORIGIN}{BASE}#business', 'name': BIZ['name'],
         'description': 'ABS pump and module repair, brake system fault diagnosis, Mercedes 7-speed and 9-speed TCU repair, Mercedes steering lock repair and hybrid battery replacement in Kaki Bukit, Singapore.',
         'url': f'{ORIGIN}{BASE}', 'telephone': BIZ['tel'],
         'logo': f'{IMG_ORIGIN}/icon-512.png', 'image': f'{IMG_ORIGIN}/img/share/home.jpg',
         'sameAs': [BIZ['facebook']],
         'address': {'@type': 'PostalAddress', 'streetAddress': f'{BIZ["street"]}, {BIZ["building"]}',
                     'addressLocality': 'Singapore', 'postalCode': BIZ['postal'], 'addressCountry': 'SG'},
         'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification',
                                        'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                        'opens': '09:00', 'closes': '19:00'},
                                       {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Saturday'],
                                        'opens': '09:00', 'closes': '15:00'}],
         'areaServed': 'Singapore',
         'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Services', 'itemListElement': [
             {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': html.unescape(t)}} for _, t, *_ in SERVICES]
             + [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': 'BMW temperature programming'}}]}}]}


def faq_ld():
    import re
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in FAQ]}


def page(path, title, desc, body, ld=None, share=('module-circuit-board.jpg', None), og_type='website'):
    canonical = ORIGIN + BASE + path
    slug = path.strip('/').replace('/', '-') or 'home'
    headline = share[1] or title.split(' | ')[0]
    SHARES[slug] = (share[0], headline)
    og_img = f'{IMG_ORIGIN}/img/share/{slug}.jpg'
    ld = [schema()] + (ld or []) + [{'@context': 'https://schema.org', '@type': 'WebPage', '@id': canonical, 'url': canonical,
                                     'name': title, 'description': desc, 'about': {'@id': f'{ORIGIN}{BASE}#business'},
                                     'primaryImageOfPage': {'@type': 'ImageObject', 'url': og_img, 'width': 1200, 'height': 630}}]
    nav = ''.join(f'<a href="{href(p)}">{e(n)}</a>' for p, n in NAV)
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    robots = 'noindex, nofollow' if MOCKUP else 'index, follow, max-image-preview:large'
    strip = '<div class="preview-strip">Preview by Page One Singapore. This is a draft of your new website.</div>\n' if MOCKUP else ''
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<meta name="p1-site" content="{SLUG}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BIZ['name']}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:secure_url" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(headline)} | {BIZ['name']}">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#1f262b">
<link rel="icon" href="{u("favicon.ico")}" sizes="48x48">
<link rel="icon" href="{u("icon-96.png")}" type="image/png" sizes="96x96">
<link rel="icon" href="{u("icon-192.png")}" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{u("apple-touch-icon.png")}">
<link rel="manifest" href="{u("site.webmanifest")}">
{'<link rel="preconnect" href="https://cdn.jsdelivr.net">' if IMG_CDN else ''}
{f'<link rel="preload" as="image" href="{u(f"img/{HERO}.webp")}" media="(max-width:899px)">' + chr(10) + f'<link rel="preload" as="image" href="{u(f"img/{HERO}-lg.webp")}" media="(min-width:900px)">' if not path else ''}
<link rel="stylesheet" href="{u("ecu.css")}?v={ASSET_V}">
{lds}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{SPRITE}
{strip}<div class="topbar"><div class="wrap">
<span>ABS &amp; brake system repair <span class="hide-sm">· Mon–Fri 9am–7pm · Sat 9am–3pm · WhatsApp 24/7</span></span>
<span><a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {BIZ["tel_disp"]}</a> <span class="hide-sm">· {BIZ["building"]}</span></span>
</div></div>
<header class="site"><div class="wrap">
<a class="logo" href="{u()}"><img src="{u("img/logo.webp")}" width="538" height="100" alt="The ECU Clinic: ECU and ABS repair for cars"></a>
<nav class="main" aria-label="Main">{nav}</nav>
<a class="btn btn-wa hdr-cta" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp {BIZ["tel_disp"]}</a>
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
</div>
<nav class="mobile-nav" id="mnav" aria-label="Mobile">{nav}</nav>
</header>
<main id="main">
{body}
</main>
<footer class="site"><div class="wrap">
<div class="grid">
<div>
<h3>The ECU Clinic</h3>
<p>ABS pump and module repair and brake fault diagnosis in Kaki Bukit, Singapore. Also Mercedes 7-speed and 9-speed TCU repair, Mercedes steering lock repair and brand-new OEM hybrid batteries. Pick-up and delivery available, 6-month warranty.</p>
<p><a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {BIZ["tel_disp"]}</a> (preferred, ask for {BIZ["contact"]})<br><a href="tel:{BIZ["tel"]}">Call {BIZ["tel_disp"]}</a></p>
<p><a href="{BIZ["facebook"]}" target="_blank" rel="noopener">Facebook</a></p>
</div>
<div>
<h3>Workshop</h3>
<p>{BIZ["building"]}<br>{e(BIZ["street"])}<br>Singapore {BIZ["postal"]}</p>
<p>Mon–Fri 9am–7pm<br>Sat 9am–3pm<br>Sun &amp; PH closed<br>WhatsApp enquiries 24/7</p>
</div>
<div>
<h3>Services</h3>
<ul>{''.join(f'<li><a href="{u(f"services/{sp['slug']}/")}">{e(sp['name'])}</a></li>' for sp in SERVICE_PAGES)}</ul>
</div>
<div>
<h3>Articles</h3>
<ul>{''.join(f'<li><a href="{u(f"articles/{a['slug']}/")}">{e(a['h1'])}</a></li>' for a in ARTICLES[:4])}<li><a href="{u("articles/")}">All articles</a></li></ul>
</div>
</div>
<div class="fine"><span>© 2026 The ECU Clinic. All rights reserved.</span><a href="https://pageonesingapore.com/">Website &amp; SEO by Page One Singapore</a></div>
</div></footer>
<div class="dock">
<a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp</a>
<a class="btn btn-red" href="tel:{BIZ["tel"]}">{ICON["phone"]}Call</a>
</div>
<script src="{u("ecu.js")}?v={ASSET_V}" defer></script>
</body>
</html>
'''


def why_cards():
    return ''.join(f'<div class="card"><div class="ico">{ICON[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i, t, d in WHY)


def service_cards():
    return ''.join(
        f'<div class="card img" id="{sid}">{img(im, alt)}<div class="body"><h3>{t}</h3><p class="muted">{d}</p>'
        f'<ul class="ticks">{"".join(f"<li>{e(x)}</li>" for x in items)}</ul>'
        f'<p class="more"><a href="{u(f"services/{SP[sid]["slug"]}/")}">More about {t} →</a></p></div></div>'
        for sid, t, im, alt, d, items in SERVICES)


def home():
    gal = ''.join(f'<figure>{img(n, a)}<figcaption>{e(a)}</figcaption></figure>' for n, a in GALLERY)
    steps = ''.join(f'<li><strong>{t}.</strong> {d}</li>' for t, d in STEPS)
    models = ''.join(f'<p><strong>{s}</strong><br>{c}</p>' for s, c in BMW_MODELS)
    makes = ''.join(f'<li>{m}</li>' for m in MAKES)
    warns = ''.join(f'<li>{e(w)}</li>' for w in WARNINGS)
    faq = ''.join(f'<details><summary>{e(q)}</summary><div class="a">{a}</div></details>' for q, a in FAQ)
    body = f'''
<section class="hero" style="padding:0">
<picture><source media="(min-width:900px)" srcset="{u(f"img/{HERO}-lg.webp")}">{img(HERO, "Mercedes-Benz ESP pumps on the repair bench", lazy=False, cls="bg")}</picture>
<div class="wrap">
<span class="eyebrow">Brake system specialist · Kaki Bukit, Singapore</span>
<h1>ABS Pump Repair &amp; Brake Fault Diagnosis in Singapore</h1>
<p class="lead">ABS or ESP light on? We find the fault and repair the pump or module. We also repair Mercedes 7-speed and 9-speed gearbox control units and steering locks, and fit brand-new OEM hybrid batteries.</p>
<ul class="chips"><li>6-month warranty</li><li>Pick-up &amp; delivery</li><li>10+ years’ experience</li><li>WhatsApp enquiries 24/7</li></ul>
{cta_buttons(dark=True)}
</div>
</section>

<section class="stats" aria-label="At a glance"><div class="wrap"><ul>
<li><b data-count="10">10<small>+</small></b>years with car electronics</li>
<li><b data-count="6">6<small>months</small></b>warranty on repairs</li>
<li><b data-count="100000">100,000<small>km</small></b>or 1-year hybrid battery warranty</li>
<li><b>24/7</b>WhatsApp enquiries</li>
</ul></div></section>

<section><div class="wrap">
<div class="sec-head"><h2>Why drivers and workshops come to The ECU Clinic</h2><p>When a brake warning light won’t go away, the fault is often in the ABS pump or module. That is what we fix.</p></div>
<div class="grid g3 why">{why_cards()}</div>
<div class="card" style="margin-top:18px;border-left:4px solid #2fd3a8;background:var(--bg)"><h3 style="margin-bottom:.3em">The repairer behind many workshops</h3><p style="margin:0">Many car workshops send their ABS and module repairs to us. Come direct and deal with the technician who does the repair.</p></div>
</div></section>

<section class="alt" id="services"><div class="wrap">
<div class="sec-head"><h2>Our services</h2><p>ABS and brake system repair, plus Mercedes gearbox and steering lock repair and hybrid batteries.</p></div>
<div class="grid g2 svc">{service_cards()}</div>
<p style="margin-top:22px"><a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp us your fault code</a></p>
</div></section>

<section id="diagnosis"><div class="wrap split">
<div>
<span class="eyebrow" style="color:var(--blue)">Fault diagnosis</span>
<h2>Warning light on the dashboard?</h2>
<p>An ABS, ESP or brake warning can come from the pump, the module, a sensor or the wiring. We find the cause first, then tell you the options: repair, recon, used or new.</p>
<ul class="ticks">{warns}</ul>
<a class="btn btn-wa" href="{wa_link("Hi The ECU Clinic, I have a warning light on my car. Car model: \nChassis no.: \nFault code / warning: ")}" target="_blank" rel="noopener">{ICON["wa"]}Send us a photo of the warning</a>
</div>
<div>{img("active-brake-assist-warning", "Mercedes-Benz dashboard showing Active Brake Assist functions limited")}</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="sec-head"><h2>Car brands we work on</h2><p>Continental and Asian cars. Not sure about yours? WhatsApp us the model.</p></div>
<ul class="makes">{makes}</ul>
</div></section>

<section id="bmw-temperature"><div class="wrap split media-hide-sm">
<div>
<span class="eyebrow" style="color:var(--blue)">BMW temperature programming</span>
<h2>BMW running hot at 120°C or more?</h2>
<p>We reprogram your BMW to bring a high coolant temperature down to a stable 95°C or so, for steady performance and long-term engine protection.</p>
<ul class="ticks"><li>Reduces high coolant temperature to about 95°C</li><li>Keeps the engine at a stable operating temperature</li><li>No change to daily driving or other functions</li></ul>
<a class="btn btn-wa" href="{wa_link("Hi The ECU Clinic, I would like BMW temperature programming. Model and year: ")}" target="_blank" rel="noopener">{ICON["wa"]}Check my BMW</a>
<details class="models"><summary>BMW models we program (2010–2018)</summary><div class="a">{models}<p>Model not listed? WhatsApp us and we’ll advise on compatibility.</p></div></details>
<p class="more"><a href="{u("services/bmw-temperature-programming/")}">More about BMW temperature programming →</a></p>
</div>
<div>{img("bmw-fault-code-scan", "Scan tool reading BMW engine fault codes")}</div>
</div></section>

<section class="alt" id="how"><div class="wrap split media-hide-sm">
<div>
<h2>How it works</h2>
<ol class="steps">{steps}</ol>
{cta_buttons()}
</div>
<div>{img("hyundai-kia-esc", "Hyundai / Kia ESC unit on the bench")}</div>
</div></section>

<section id="gallery"><div class="wrap">
<div class="sec-head"><h2>Our work</h2><p>Real jobs from our workshop: ABS and ESP units, Mercedes gearbox and steering lock work, and hybrid batteries.</p></div>
<div class="gallery home-gal">{gal}</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="sec-head"><h2>Guides and articles</h2><p>Warning lights and common faults, explained in plain words.</p></div>
<div class="grid g3 arts">{article_cards(ARTICLES[:3])}</div>
<p style="margin-top:18px"><a class="btn btn-line" href="{u("articles/")}">All articles</a></p>
</div></section>

<section id="contact"><div class="wrap">
<div class="sec-head"><h2>Visit us in Kaki Bukit</h2><p>WhatsApp is the fastest way to reach us for enquiries and appointments.</p></div>
<div class="loc-wrap">
<div class="card loc"><span class="tag">Workshop</span><h3>{BIZ["building"]}</h3>
<p>{e(BIZ["street"])}<br>Singapore {BIZ["postal"]}</p>
<div class="btns"><a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp {BIZ["tel_disp"]}</a>
<a class="btn btn-line" href="https://www.google.com/maps/search/?api=1&amp;query={quote(BIZ["map"])}" target="_blank" rel="noopener">Directions</a></div></div>
<div class="card"><h3>Opening hours</h3><dl class="hours"><dt>Mon – Fri</dt><dd>9:00am – 7:00pm</dd><dt>Sat</dt><dd>9:00am – 3:00pm</dd><dt>Sun &amp; PH</dt><dd>Closed</dd></dl>
<p class="muted" style="margin-top:10px">WhatsApp enquiries are welcome 24/7. After-hours appointments can be arranged. Pick-up and delivery available.</p></div>
</div>
</div></section>

<section id="faq"><div class="wrap" style="max-width:860px">
<div class="sec-head"><h2>ABS &amp; brake repair FAQ</h2></div>
{faq}
</div></section>

<section><div class="wrap"><div class="band"><div><h2>ABS or brake light on?</h2><p>WhatsApp us the fault code, chassis number and car model. We’ll tell you what we can do.</p></div>{cta_buttons(dark=True)}</div></div></section>
'''
    return page('', 'ABS Pump Repair Singapore | The ECU Clinic, Kaki Bukit',
                'ABS pump and module repair, brake fault diagnosis, Mercedes 7G/9G TCU and steering lock repair, new OEM hybrid batteries. Kaki Bukit. WhatsApp 9893 1923.',
                body, ld=[faq_ld()], share=('mercedes-esp-pumps.jpg', 'ABS Pump Repair Specialist in Singapore'))


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote', rel, len(text.encode()), 'bytes')


def build(rel, fn):
    global DEPTH
    DEPTH = rel.count('/')
    write(rel, fn())


def robots_txt():
    return f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n'


def all_paths():
    return ([''] + [f'services/{sp["slug"]}/' for sp in SERVICE_PAGES] + ['articles/']
            + [f'articles/{a["slug"]}/' for a in ARTICLES])


def sitemap():
    urls = ''.join(f'<url><loc>{ORIGIN}{BASE}{p}</loc></url>' for p in all_paths())
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


def not_found():
    # Served for any missing address on theecuclinicsg.com (the parent .htaccess sets ErrorDocument
    # 404 /404.html, which resolves to this folder there), so links are root-absolute.
    return f'''<!doctype html>
<html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex"><title>Page not found | The ECU Clinic</title>
<link rel="stylesheet" href="/ecu.css?v={ASSET_V}"></head>
<body><main id="main"><section><div class="wrap" style="max-width:640px;text-align:center;padding:80px 16px">
<h1>Page not found</h1>
<p>This page doesn’t exist. Head back to the home page, or WhatsApp us your car model and fault code.</p>
<div class="btns" style="justify-content:center"><a class="btn btn-line" href="/">Home page</a>
<a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {BIZ["tel_disp"]}</a></div>
</div></section></main></body></html>
'''


# ---------- service pages and articles ----------
def crumbs_ld(items):
    # items: [(name, path)], home first
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': f'{ORIGIN}{BASE}{p}'} for i, (n, p) in enumerate(items)]}


def crumbs_html(items):
    parts = [f'<a href="{u(p) if p else u()}">{e(n)}</a>' for n, p in items[:-1]] + [e(items[-1][0])]
    return '<nav class="crumbs" aria-label="Breadcrumb">' + ' › '.join(parts) + '</nav>'


def faq_ld_of(qa):
    import re
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in qa]}


def sub_hero(crumbs, eyebrow, h1, lead, photo, alt, buttons=True):
    return f'''<section class="hero sub" style="padding:0">
{img(photo, alt, lazy=False, cls="bg")}
<div class="wrap">
{crumbs_html(crumbs)}
<span class="eyebrow">{e(eyebrow)}</span>
<h1>{e(h1)}</h1>
<p class="lead">{e(lead)}</p>
{cta_buttons(dark=True) if buttons else ''}
</div>
</section>'''


def article_cards(arts):
    return ''.join(
        f'<a class="card img art" href="{u(f"articles/{a["slug"]}/")}">{img(a["photo"], a["alt"])}'
        f'<div class="body"><h3>{e(a["h1"])}</h3><p class="muted">{e(a["lead"])}</p></div></a>' for a in arts)


def band(title='ABS or brake light on?', text='WhatsApp us the fault code, chassis number and car model. We’ll tell you what we can do.'):
    return f'<section><div class="wrap"><div class="band"><div><h2>{e(title)}</h2><p>{e(text)}</p></div>{cta_buttons(dark=True)}</div></div></section>'


def service_page(sp):
    path = f'services/{sp["slug"]}/'
    crumbs = [('Home', ''), ('Services', '#services'), (sp['name'], path)]
    crumbs_disp = [('Home', ''), (sp['name'], path)]
    what = ''.join(f'<li>{e(x)}</li>' for x in sp['what'])
    signs = ''.join(f'<div class="card"><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, d in sp['signs'])
    faq = ''.join(f'<details><summary>{e(q)}</summary><div class="a">{e(a)}</div></details>' for q, a in sp['faq'])
    intro = ''.join(f'<p>{e(x)}</p>' for x in sp['intro'])
    rel = [ART[s] for s in sp['related']]
    others = ''.join(f'<li><a href="{u(f"services/{o["slug"]}/")}">{e(o["name"])}</a></li>' for o in SERVICE_PAGES if o is not sp)
    extra = ''
    if sp['key'] == 'bmw':
        models = ''.join(f'<p><strong>{s}</strong><br>{c}</p>' for s, c in BMW_MODELS)
        extra = f'''<section class="alt"><div class="wrap">
<div class="sec-head"><h2>BMW models we program (2010–2018)</h2><p>Model not listed? WhatsApp us and we’ll advise on compatibility.</p></div>
<div class="models-list">{models}</div>
</div></section>'''
    body = sub_hero(crumbs_disp, 'Service · Kaki Bukit, Singapore', sp['h1'], sp['lead'], sp['photo'], sp['alt']) + f'''
<section><div class="wrap split">
<div>
<h2>About this service</h2>
{intro}
<h3>What we do</h3>
<ul class="ticks">{what}</ul>
</div>
<div>{img(sp["photo"], sp["alt"])}</div>
</div></section>
''' + (f'''<section class="alt"><div class="wrap">
<div class="sec-head"><h2>Signs you may need this</h2><p>Not sure? WhatsApp us the fault code and we’ll tell you.</p></div>
<div class="grid sym">{signs}</div>
</div></section>''' if signs else '') + extra + f'''
<section><div class="wrap split">
<div>
<h2>How it works</h2>
<ol class="steps">{''.join(f'<li><strong>{t}.</strong> {d}</li>' for t, d in STEPS)}</ol>
</div>
<div>
<h2>Questions</h2>
{faq}
</div>
</div></section>
''' + (f'''<section class="alt"><div class="wrap">
<div class="sec-head"><h2>Related articles</h2></div>
<div class="grid g3 arts">{article_cards(rel)}</div>
</div></section>''' if rel else '') + f'''
<section><div class="wrap"><div class="sec-head"><h2>Other services</h2></div><ul class="ticks">{others}</ul></div></section>
''' + band()
    svc_ld = {'@context': 'https://schema.org', '@type': 'Service', 'name': sp['name'], 'serviceType': sp['name'],
              'description': sp['desc'], 'provider': {'@id': f'{ORIGIN}{BASE}#business'}, 'areaServed': 'Singapore',
              'url': f'{ORIGIN}{BASE}{path}'}
    return page(path, sp['title'], sp['desc'], body, ld=[svc_ld, crumbs_ld(crumbs_disp), faq_ld_of(sp['faq'])],
                share=(sp['share'], sp['h1']))


def articles_index():
    path = 'articles/'
    crumbs = [('Home', ''), ('Articles', path)]
    body = sub_hero(crumbs, 'Guides', 'Car Electronics Guides and Articles',
                    'ABS and brake warnings, Mercedes gearbox and steering lock faults, and hybrid batteries, explained in plain words.',
                    'control-board-bench', 'Control board on the repair bench', buttons=False) + f'''
<section><div class="wrap">
<div class="grid g3 arts">{article_cards(ARTICLES)}</div>
</div></section>
''' + band()
    return page(path, 'ABS, Brake & Mercedes Repair Guides | The ECU Clinic Articles',
                'Plain-English guides to ABS warning lights, Mercedes Active Brake Assist, 7G-Tronic TCU faults, steering lock (ELV) failure and hybrid batteries.',
                body, ld=[crumbs_ld(crumbs)], share=('control-board-repair-bench.jpg', 'Car Electronics Guides'))


def article(a):
    path = f'articles/{a["slug"]}/'
    sp = next(s for s in SERVICE_PAGES if s['slug'] == a['service'])
    crumbs = [('Home', ''), ('Articles', 'articles/'), (a['h1'], path)]
    more = [x for x in ARTICLES if x is not a][:3]
    body = sub_hero(crumbs, 'Guide', a['h1'], a['lead'], a['photo'], a['alt'], buttons=False) + f'''
<section><div class="wrap prose">
<p class="meta">By The ECU Clinic · {a["date"][8:10].lstrip("0")} Oct 2026</p>
{a["body"].replace("{wa}", wa_link())}
<div class="btns" style="margin-top:22px"><a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp {BIZ["tel_disp"]}</a>
<a class="btn btn-line" href="{u(f"services/{sp['slug']}/")}">{e(sp["name"])}</a></div>
</div></section>
<section class="alt"><div class="wrap">
<div class="sec-head"><h2>More articles</h2></div>
<div class="grid g3 arts">{article_cards(more)}</div>
</div></section>
''' + band()
    art_ld = {'@context': 'https://schema.org', '@type': 'Article', 'headline': a['h1'], 'description': a['desc'],
              'datePublished': a['date'], 'dateModified': a['date'], 'mainEntityOfPage': f'{ORIGIN}{BASE}{path}',
              'image': f'{IMG_ORIGIN}/img/share/{path.strip("/").replace("/", "-")}.jpg',
              'author': {'@type': 'Organization', 'name': BIZ['name'], 'url': f'{ORIGIN}{BASE}'},
              'publisher': {'@id': f'{ORIGIN}{BASE}#business'}}
    return page(path, a['title'], a['desc'], body, ld=[art_ld, crumbs_ld(crumbs)], share=(a['share'], a['h1']), og_type='article')


if __name__ == '__main__':
    build('index.html', home)
    for sp in SERVICE_PAGES:
        build(f'services/{sp["slug"]}/index.html', lambda sp=sp: service_page(sp))
    build('articles/index.html', articles_index)
    for a in ARTICLES:
        build(f'articles/{a["slug"]}/index.html', lambda a=a: article(a))
    # Only read when theecuclinicsg.com serves this folder; pageonesingapore.com has its own root robots.txt.
    build('robots.txt', robots_txt)
    build('sitemap.xml', sitemap)
    build('404.html', not_found)
    build('site.webmanifest', lambda: json.dumps({
        'name': BIZ['name'], 'short_name': 'ECU Clinic', 'start_url': './', 'display': 'standalone',
        'background_color': '#ffffff', 'theme_color': '#1f262b',
        'icons': [{'src': u(f'icon-{n}.png').lstrip('./') if n == 192 else u(f'icon-{n}.png'), 'sizes': f'{n}x{n}', 'type': 'image/png'} for n in (192, 512)]}, indent=1))
    import share
    for slug, (photo, headline) in SHARES.items():
        share.card(slug, photo, headline)
    print('share images', len(SHARES))
