#!/usr/bin/env python3
"""Build the Dynamic Motoring (DMTS) site.

Built once into pageonesingapore.com/preview/dmts/ and never moved: on activation, dmts.com.sg's
document root is pointed at that same folder. Every internal link is relative so the files work at
both addresses, and canonical/structured-data URLs always name dmts.com.sg. Search engines are kept
off the preview copy by "Disallow: /preview/" in pageonesingapore.com/robots.txt; dmts.com.sg gets
its own robots.txt and sitemap.xml from this folder.

    python3 build.py            # writes the HTML pages into ./site

Content comes from source/content.md (captured from dmts.com.sg) and the client's answers at onboarding.
The old cost estimator (source/prices.json) is archived only: DMTS quotes after a paid pre-repair diagnostic.
Shared assets (dmts.css, dmts.js, favicon.svg, img/) live in ./site and are edited by hand.
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')
ORIGIN = 'https://dmts.com.sg'  # the client's domain: canonical URLs and structured data
BASE = '/'
DEPTH = 0  # folder depth of the page being built; set by build() so u() can emit relative links
ABS = False  # root-relative links instead (404 page: Apache serves it at any depth)
ASSET_V = '5'
SLUG = 'dmts'  # Page One client key: p1-site marker (go-live check) and WhatsApp tracker
INDEXNOW_KEY = '5792dfeef836aebd82a445c206294c95'  # same key as the controller's Client record
# Share images and icons must load before dmts.com.sg points here, so until go-live they are linked
# at the preview address (the same files). At go-live set LIVE = True, rebuild and republish.
LIVE = False
IMG_ORIGIN = ORIGIN if LIVE else 'https://pageonesingapore.com/preview/dmts'
SHARES = {}  # share-image slug -> (photo, headline), filled as pages are built


BIZ = {
    'name': 'Dynamic Motoring',
    'short': 'DMTS',
    'tel': '+6563528832', 'tel_disp': '6352 8832',
    'mobile': '+6584309665', 'mobile_disp': '8430 9665',
    'wa': '6584309665',
    'fax_disp': '6352 8831',
    'email': 'contact@dmts.com.sg',
    'google': 'https://share.google/ZXSk6rE3VdUNgZyKS',
    'facebook': 'https://www.facebook.com/DYNAMICMOTORINGTRANSMISSIONSPECIALIST/',
    'hq': {'street': '71 Woodlands Industrial Park E9, #01-25 Wave 9', 'postal': '757048',
           'map': '71 Woodlands Industrial Park E9 Wave 9 Singapore'},
    'branch': {'street': '60 Jalan Lam Huat, #05-48', 'postal': '737869',
               'map': '60 Jalan Lam Huat Singapore 737869'},
}
WA_TEXT = 'Hi Dynamic Motoring, I would like a quote for my gearbox.'

NAV = [('', 'Home'), ('services/', 'Services'), ('gearbox-problems/', 'Gearbox Problems'), ('gallery/', 'Gallery'),
       ('about/', 'About'), ('contact/', 'Contact')]

DIAG = 'Pre-repair diagnostic from S$30'
WARRANTY = 'All repairs come with a standard 6-month warranty unless otherwise stated.'

ICON = {
    'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
    'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8.2 8.2 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6a1.1 1.1 0 0 0-.8.4 3.4 3.4 0 0 0-1 2.5 5.9 5.9 0 0 0 1.2 3.1 13.5 13.5 0 0 0 5.2 4.6c1.9.8 2.7.9 3.6.7a3.1 3.1 0 0 0 2-1.4 2.5 2.5 0 0 0 .2-1.4c-.1-.2-.3-.3-.6-.4zM12 21.8a9.8 9.8 0 0 1-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4A9.8 9.8 0 1 1 12 21.8zm8.4-18.2A11.8 11.8 0 0 0 1.8 17.8L.1 24l6.3-1.7a11.8 11.8 0 0 0 5.6 1.4A11.8 11.8 0 0 0 20.4 3.6z"/></svg>',
    'gear': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/></svg>',
    'tag': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20.6 13.4l-7.2 7.2a2 2 0 0 1-2.8 0L2 12V2h10l8.6 8.6a2 2 0 0 1 0 2.8z"/><circle cx="7" cy="7" r="1.5"/></svg>',
    'shield': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>',
    'drop': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 2.7l5.7 5.6a8 8 0 1 1-11.3 0z"/></svg>',
    'users': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/></svg>',
    'truck': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M1 3h15v13H1zM16 8h4l3 3v5h-7z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
}

e = html.escape


def u(path=''):
    if ABS:
        return BASE + path
    return ('../' * DEPTH or './') + path


def wa_link(text=WA_TEXT):
    from urllib.parse import quote
    return f'https://wa.me/{BIZ["wa"]}?text={quote(text)}'


def cta_buttons(extra=''):
    return (f'<div class="btns">'
            f'<a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp us</a>'
            f'<a class="btn btn-red" href="tel:{BIZ["tel"]}">{ICON["phone"]}Call {BIZ["tel_disp"]}</a>'
            f'{extra}</div>')


def schema():
    def place(key, label):
        a = BIZ[key]
        return {
            '@type': 'AutoRepair', '@id': f'{ORIGIN}{BASE}#{key}',
            'name': f'Dynamic Motoring ({label})',
            'parentOrganization': {'@id': f'{ORIGIN}{BASE}#org'},
            'telephone': BIZ['tel'], 'email': BIZ['email'],
            'image': [f'{IMG_ORIGIN}/img/share/home.jpg', f'{IMG_ORIGIN}/img/share/contact.jpg'],
            'logo': f'{IMG_ORIGIN}/img/logo.png',
            'address': {'@type': 'PostalAddress', 'streetAddress': a['street'],
                        'addressLocality': 'Singapore', 'postalCode': a['postal'], 'addressCountry': 'SG'},
            'openingHoursSpecification': [
                {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], 'opens': '09:00', 'closes': '18:00'},
                {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Saturday', 'opens': '09:00', 'closes': '15:00'}],
            'areaServed': 'Singapore',
        }
    return {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Organization', '@id': f'{ORIGIN}{BASE}#org', 'name': 'Dynamic Motoring',
         'alternateName': ['DMTS', 'Dynamic Motoring Transmission Specialist'],
         'url': f'{ORIGIN}{BASE}', 'logo': {'@type': 'ImageObject', 'url': f'{IMG_ORIGIN}/img/logo.png'},
         'image': f'{IMG_ORIGIN}/img/share/home.jpg',
         'email': BIZ['email'], 'telephone': BIZ['tel'], 'sameAs': [BIZ['facebook'], BIZ['google']],
         'description': 'Gearbox and automatic transmission repair, overhaul, upgrade and servicing specialist in Singapore.'},
        place('hq', 'Woodlands HQ'), place('branch', 'Jalan Lam Huat branch')]}


def page(path, title, desc, body, active='', extra_head='', ld=None, scripts='', share=('hero-workshop', None)):
    canonical = ORIGIN + BASE + path
    slug = path.strip('/').replace('/', '-') or 'home'
    headline = share[1] or title.split(' | ')[0]
    SHARES[slug] = (share[0], headline)
    og_img = f'{IMG_ORIGIN}/img/share/{slug}.jpg'
    ld = (ld or []) + [{'@context': 'https://schema.org', '@type': 'WebPage', '@id': canonical, 'url': canonical, 'name': title,
                        'description': desc, 'isPartOf': {'@id': f'{ORIGIN}{BASE}#org'},
                        'primaryImageOfPage': {'@type': 'ImageObject', 'url': og_img, 'width': 1200, 'height': 630}}]
    nav = ''.join(f'<a href="{u(p)}"{" aria-current=\"page\"" if p == active else ""}>{e(n)}</a>' for p, n in NAV)
    mnav = ''.join(f'<a href="{u(p)}">{e(n)}</a>' for p, n in NAV)
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ([schema()] + (ld or [])))
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
<meta property="og:site_name" content="Dynamic Motoring">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_img}">
<meta property="og:image:secure_url" content="{og_img}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{e(headline)} | Dynamic Motoring">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{og_img}">
<meta name="theme-color" content="#0b1e33">
<link rel="icon" href="{u("favicon.ico")}" sizes="48x48">
<link rel="icon" href="{u("icon-96.png")}" type="image/png" sizes="96x96">
<link rel="icon" href="{u("icon-192.png")}" type="image/png" sizes="192x192">
<link rel="icon" href="{u("favicon.svg")}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{u("apple-touch-icon.png")}">
<link rel="manifest" href="{u("site.webmanifest")}">
<link rel="stylesheet" href="{u("dmts.css")}?v={ASSET_V}">
{extra_head}{lds}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
<span>Gearbox &amp; auto transmission specialist <span class="hide-sm">· Mon–Fri 9am–6pm · Sat 9am–3pm · Sun &amp; PH closed</span></span>
<span><a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {BIZ["mobile_disp"]}</a> <span class="hide-sm">· Tel <a href="tel:{BIZ["tel"]}">{BIZ["tel_disp"]}</a></span></span>
</div></div>
<header class="site"><div class="wrap">
<a class="logo" href="{u()}"><img src="{u("img/logo.webp")}" width="360" height="127" alt="Dynamic Motoring"></a>
<nav class="main" aria-label="Main">{nav}</nav>
<a class="btn btn-wa hdr-cta" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp {BIZ["mobile_disp"]}</a>
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
<h3>Dynamic Motoring</h3>
<p>Gearbox repair, overhaul, upgrade and servicing for continental, Japanese, Korean and other makes. {DIAG}, free towing to our workshop during office hours, and a 6-month warranty on repairs.</p>
<p><a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp {BIZ["mobile_disp"]}</a> (preferred)<br><a href="tel:{BIZ["tel"]}">Tel {BIZ["tel_disp"]}</a><br>Fax {BIZ["fax_disp"]}<br><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></p>
<p><a href="{BIZ["facebook"]}" target="_blank" rel="noopener">Facebook</a> · <a href="{BIZ["google"]}" target="_blank" rel="noopener">Google</a></p>
</div>
<div>
<h3>Workshops</h3>
<p><strong>HQ</strong><br>{e(BIZ["hq"]["street"])}<br>Singapore {BIZ["hq"]["postal"]}</p>
<p><strong>Branch</strong><br>{e(BIZ["branch"]["street"])}<br>Singapore {BIZ["branch"]["postal"]}</p>
</div>
<div>
<h3>Services</h3>
<ul>{''.join(f'<li><a href="{u("services/" + sid + "/")}">{t}</a></li>' for sid, t, *_ in SERVICES)}</ul>
<h3 style="margin-top:1em">Gearbox problems</h3>
<ul>{''.join(f'<li><a href="{u("gearbox-problems/" + p["slug"] + "/")}">{e(p["name"])}</a></li>' for p in PROBLEMS)}</ul>
</div>
<div>
<h3>Pages</h3>
<ul>{''.join(f'<li><a href="{u(p)}">{e(n)}</a></li>' for p, n in NAV)}</ul>
<p style="margin-top:1em">Mon–Fri 9:00–18:00<br>Sat 9:00–15:00<br>Sun &amp; PH closed</p>
</div>
</div>
<div class="fine"><span>© 2026 Dynamic Motoring. All rights reserved.</span><a href="https://pageonesingapore.com/">Website &amp; SEO by Page One Singapore</a></div>
</div></footer>
<div class="dock">
<a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp</a>
<a class="btn btn-red" href="tel:{BIZ["tel"]}">{ICON["phone"]}Call</a>
</div>
<script src="{u("dmts.js")}?v={ASSET_V}" defer></script>
{scripts}
</body>
</html>
'''


def img(name, alt, w=640, h=480, lazy=True, cls=''):
    return (f'<img src="{u("img/" + name + ".webp")}" width="{w}" height="{h}" alt="{e(alt)}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async"{f" class=\"{cls}\"" if cls else ""}>')


# ---------- shared content ----------
SERVICES = [
    ('gearbox-repair', 'Gearbox Repair &amp; Overhaul', 'gearbox-teardown', 'Technician rebuilding an automatic gearbox on the teardown bench',
     'We have a full range of diagnostic tools specialising in auto transmission to accurately identify the root cause. With the vast experience of our gearbox specialists, we can recommend a full range of repair or overhaul services for any type or brand of gearbox, on site. Our gearbox solutions are flexible and tailored to each transmission issue, so you only pay for what is needed.'),
    ('gearbox-upgrade', 'Gearbox Strengthening &amp; Upgrade', 'gearbox-parts', 'Gearbox clutch packs and gear sets laid out for inspection',
     'Our transmission specialists can take re-conditioning to the next level with upgrades that strengthen gearbox reliability and performance to match the vehicle’s power (bhp) and torque (Nm). After assessment and a complete diagnostic procedure, we design an upgrade of the clutch, valve body or torque converter. This can increase the gearbox’s output torque and extend the service life of the whole system, with lubrication of bearings and gears optimised for the new performance level.'),
    ('gearbox-servicing', 'Gearbox Maintenance &amp; Servicing', 'atf-fluids', 'Fuchs Titan automatic transmission fluid used for gearbox servicing',
     'Regular servicing of the auto transmission is as important as servicing the engine. We only use the manufacturer’s recommended or gearbox-specific brand of Automatic Transmission Fluid (ATF), in the right amount and in the right place, for longer life of bearings and gears with less wear. Good maintenance and periodic inspection prevent malfunctions and breakdowns.'),
    ('free-towing', 'Free Towing / Pick-Up', 'gearbox-removal', 'Gearbox being removed from a car on a transmission jack',
     'We provide free pick-up to our workshop for gearbox repair during office hours. If the vehicle cannot move at all because of transmission failure, we send a tow truck to pick it up, free of charge.'),
]


TESTIMONIALS = [
    ('Ulysses Wang', 'BMW 5 Series', 'I never knew that there are actually car workshops that specialised in gearbox related problems until I chanced upon Dynamic Motoring Transmission Specialist from the internet. I had an idea of the repair cost after going through the cost estimator on their website. Arranged an appointment with Jacky and drove my BMW 5 series to let him check. Workshop was impressive from the setup and was relieved to know from him that the actual repair cost was lower than the estimated quote.'),
    ('Alvin Lee', 'Audi A4', 'Great service experience with Dynamic Motoring Transmission Specialist. I was initially very worried about the repair cost when my Audi A4 gearbox was diagnosed to be faulty. But Jacky was very patient and professional in explaining to me the overhaul process and the quoted price was below what I have expected. My car was ready after 3 days and was given a 6 months warranty as well. I would definitely recommend my friends to them for any gearbox issues.'),
    ('Rhyce Chng', 'Free service', 'Bought a used car from Dynamic Motoring and was given a free service at their workshop, Transmission Specialist. Nice and cosy waiting lounge with a clear view of my car undergoing maintenance. Fantastic experience with them. Thumbs up.'),
]

GALLERY = [
    ('shopfront', 'Dynamic Motoring workshop at Wave 9, Woodlands'),
    ('workshop-lifts', 'Car lifts in the Dynamic Motoring workshop'),
    ('mechanics-under-car', 'Mechanics inspecting a gearbox from under the car'),
    ('engine-bay-check', 'Technicians checking an engine bay'),
    ('diagnostics', 'Computer diagnostic test reading transmission fault codes'),
    ('gearbox-teardown', 'Gearbox overhaul on the teardown bench'),
    ('gearbox-parts', 'Clutch packs and gear sets from an automatic gearbox'),
    ('gearbox-removal', 'Removing a gearbox with a transmission jack'),
    ('transmission-cutaway', 'Automatic transmission cutaway display in the lounge'),
    ('atf-fluids', 'Fuchs Titan ATF used for gearbox servicing'),
    ('customer-lounge', 'Air-conditioned customer waiting lounge'),
]

FAQ = [
    ('How much does a gearbox repair cost in Singapore?',
     f'It depends on the car and the fault, so we don’t quote blind. We start with a pre-repair diagnostic (from S$30) to find the actual cause, then give you a clear quote before any work starts. <a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp us</a> your car model and symptoms to get started.'),
    ('How much is the diagnostic?',
     'Our pre-repair diagnostic starts from S$30. We read the transmission fault codes and check the gearbox, then tell you the fault and the repair price before any work starts.'),
    ('My car can’t move. Can you tow it?',
     f'Yes. We provide free pick-up to our workshop for gearbox repair during office hours, and if the car can’t move because of transmission failure we send a tow truck, free of charge. WhatsApp <a href="{wa_link()}" target="_blank" rel="noopener">{BIZ["mobile_disp"]}</a> or call <a href="tel:{BIZ["tel"]}">{BIZ["tel_disp"]}</a>.'),
    ('Which car brands do you work on?',
     'All types of vehicles: continental (Audi, BMW, Mercedes-Benz, Volkswagen, Mini), Japanese (Toyota, Lexus, Honda, Mazda, Mitsubishi, Nissan, Subaru, Suzuki), Korean (Hyundai, Kia) and other makes such as Land Rover, Jaguar, Volvo, Ford, Renault, Peugeot, Citroën, Chevrolet and Opel.'),
    ('Is there a warranty after repair?',
     'Yes. ' + WARRANTY),
    ('What are the signs my gearbox needs attention?',
     'A transmission check light, hesitation or refusing to go into gear, being stuck in one gear, jerking or slipping between gears, vibration at low RPM, red ATF stains under the car, or a loud noise from the gearbox. Any of these is worth a diagnostic before it gets worse.'),
    ('Where are your workshops and when are you open?',
     f'Our HQ is at {BIZ["hq"]["street"]}, Singapore {BIZ["hq"]["postal"]}, and our branch is at {BIZ["branch"]["street"]}, Singapore {BIZ["branch"]["postal"]}. We are open Monday to Friday 9am–6pm and Saturday 9am–3pm, and closed on Sundays and public holidays.'),
]


FAQ_BY_Q = dict(FAQ)

# One page per service. Only DMTS's own facts (old site + onboarding) and general gearbox knowledge.
SERVICE_PAGES = {
    'gearbox-repair': {
        'title': 'Gearbox Repair & Overhaul Singapore | Dynamic Motoring',
        'desc': 'Automatic gearbox repair and full transmission overhaul in Singapore for all car makes. Diagnostic from S$30, quote before work, 6-month warranty.',
        'h1': 'Gearbox Repair &amp; Overhaul in Singapore',
        'sub': 'We find the real cause first, then repair only what is needed, or overhaul the whole transmission when that is the right fix.',
        'sections': [
            ('Repair or full overhaul?',
             '<p>Not every gearbox fault needs a full rebuild. Some problems come from one part, such as a solenoid, a sensor, the valve body or a leaking seal, and can be repaired on their own. Others, such as worn clutch packs or internal damage, mean the transmission has to come out, be stripped down and rebuilt. Our diagnostic tells us which one your car needs, so you only pay for what is needed.</p>'),
            ('Any type or brand of gearbox',
             '<p>We work on automatic transmissions for continental, Japanese, Korean and other makes, from everyday family cars to continental models. Our workshop has dedicated teardown benches, transmission jacks and diagnostic tools specialising in auto transmission, so the work is done on site.</p>'),
        ],
        'problems': ['car-jerks-when-changing-gear', 'car-stuck-in-gear', 'transmission-warning-light', 'gearbox-noise'],
        'faq': ['How much does a gearbox repair cost in Singapore?', 'How much is the diagnostic?', 'Is there a warranty after repair?', 'Which car brands do you work on?'],
    },
    'gearbox-upgrade': {
        'title': 'Gearbox Upgrade & Strengthening Singapore | DMTS',
        'desc': 'Gearbox strengthening upgrades in Singapore: clutch, valve body and torque converter upgrades matched to your engine’s power and torque.',
        'h1': 'Gearbox Strengthening &amp; Upgrade',
        'sub': 'For cars whose engine now makes more power or torque than the original gearbox was built for, or owners who want a more reliable transmission.',
        'sections': [
            ('When an upgrade makes sense',
             '<p>A gearbox is designed for a certain amount of power (bhp) and torque (Nm). If the engine has been tuned or modified, the original clutches and torque converter can be pushed past what they were built for. A strengthening upgrade matches the gearbox to the engine, so it can handle the extra load reliably.</p>'),
            ('What we upgrade',
             '<ul class="ticks"><li>Clutch packs</li><li>Valve body</li><li>Torque converter</li><li>Lubrication of bearings and gears, set up for the new performance level</li></ul>'
             '<p>Every upgrade starts with an assessment and a complete diagnostic of your current gearbox, so the upgrade is designed for your car and how you drive it.</p>'),
        ],
        'problems': ['car-jerks-when-changing-gear', 'car-vibrates-when-accelerating'],
        'faq': ['How much is the diagnostic?', 'Is there a warranty after repair?', 'Which car brands do you work on?'],
    },
    'gearbox-servicing': {
        'title': 'Gearbox Servicing & ATF Change Singapore | DMTS',
        'desc': 'Automatic gearbox servicing in Singapore with the manufacturer-recommended or gearbox-specific ATF, in the right amount. All car makes.',
        'h1': 'Gearbox Maintenance &amp; ATF Servicing',
        'sub': 'Servicing your automatic transmission is as important as servicing the engine. The right fluid, in the right amount, keeps bearings and gears lasting longer.',
        'sections': [
            ('Why the right ATF matters',
             '<p>Automatic Transmission Fluid (ATF) cools and lubricates the gearbox and carries the hydraulic pressure that makes it shift. Different gearboxes need different fluids. We only use the manufacturer’s recommended or gearbox-specific brand of ATF, filled to the correct level, for longer life of bearings and gears with less wear.</p>'),
            ('Servicing prevents breakdowns',
             '<p>Good maintenance and periodic inspection catch small issues, such as a slow leak or old, worn fluid, before they turn into slipping, harsh shifting or a full overhaul. Follow the transmission service interval in your car’s service schedule, or ask us to check it for you.</p>'),
        ],
        'problems': ['transmission-fluid-leak', 'car-hesitates-when-accelerating', 'gearbox-noise'],
        'faq': ['What are the signs my gearbox needs attention?', 'Which car brands do you work on?', 'Where are your workshops and when are you open?'],
    },
    'free-towing': {
        'title': 'Free Towing for Gearbox Repair Singapore | DMTS',
        'desc': 'Car stuck because of the gearbox? Dynamic Motoring provides free pick-up and towing to our workshop for gearbox repair during office hours.',
        'h1': 'Free Towing &amp; Pick-Up for Gearbox Repair in Singapore',
        'sub': 'If your car can’t move because of a transmission failure, we send a tow truck to bring it to our workshop, free of charge, during office hours.',
        'sections': [
            ('How it works',
             f'<ol class="steps"><li><strong>WhatsApp us</strong> at <a href="{wa_link()}" target="_blank" rel="noopener">{BIZ["mobile_disp"]}</a> or call <a href="tel:{BIZ["tel"]}">{BIZ["tel_disp"]}</a> with your location, car model and what happened.</li>'
             '<li><strong>We arrange the pick-up</strong> to our workshop during office hours (Mon–Fri 9am–6pm, Sat 9am–3pm).</li>'
             '<li><strong>We diagnose the gearbox</strong> (from S$30) and tell you the fault and the price before any repair starts.</li></ol>'),
            ('Free for gearbox repair',
             '<p>Pick-up and towing are free when the car comes to us for gearbox repair. If your car can still be driven safely, you are also welcome to drive in to either workshop.</p>'),
        ],
        'problems': ['car-stuck-in-gear', 'transmission-warning-light'],
        'faq': ['My car can’t move. Can you tow it?', 'Where are your workshops and when are you open?', 'How much is the diagnostic?'],
    },
}

# One page per common gearbox problem (the symptoms list on the old site), with general causes.
PROBLEMS = [
    {'slug': 'transmission-warning-light', 'name': 'Transmission check light on',
     'title': 'Transmission Warning Light On? Singapore Gearbox Help',
     'desc': 'Engine or transmission check light on while driving? What it can mean for your gearbox, what to do now, and how we find the fault in Singapore.',
     'h1': 'Transmission or Check Light On: What It Means (Singapore)',
     'seen': 'The engine or transmission check light comes on while driving. Some cars also hold one gear (often called “limp mode”) to protect the gearbox.',
     'causes': ['The gearbox control unit has stored a fault code', 'A faulty sensor or shift solenoid', 'Low or overheated transmission fluid (ATF)', 'Wiring or connector problems', 'Internal wear in the gearbox'],
     'now': ['Note when the light came on and how the car is behaving', 'Avoid hard acceleration and long trips until it is checked', 'If the car is stuck in one gear or won’t move, don’t force it: ask us to tow it in'],
     'img': ('diagnostics', 'Diagnostic computer reading transmission fault codes'),
     'services': ['gearbox-repair', 'free-towing'],
     'faq': [('Can I keep driving with the transmission light on?',
              'It depends on the fault. If the car drives normally, keep it gentle and get it checked soon. If it is stuck in one gear, jerks badly or won’t move, stop driving it and arrange a tow, because driving on can turn a small fault into a bigger repair.')]},
    {'slug': 'car-hesitates-when-accelerating', 'name': 'Lack of response',
     'title': 'Car Hesitates or Won’t Go Into Gear? Singapore | DMTS',
     'desc': 'Car hesitates or refuses to go into gear when you accelerate? Common gearbox causes, what to do, and how we diagnose it in Singapore.',
     'h1': 'Car Hesitates or Won’t Go Into Gear: Causes and Repair in Singapore',
     'seen': 'You press the accelerator and the car hesitates, or there is a delay before it goes into Drive or Reverse.',
     'causes': ['Low or old transmission fluid (ATF)', 'Faulty shift solenoids or valve body', 'Worn clutch packs inside the gearbox', 'Torque converter problems'],
     'now': ['Check for red fluid stains where you park', 'Avoid hard acceleration until it is checked', 'Book a diagnostic before the delay gets worse'],
     'img': ('mechanics-under-car', 'Mechanics inspecting a gearbox from under the car'),
     'services': ['gearbox-repair', 'gearbox-servicing'],
     'faq': [('Is a delay when shifting into Drive serious?',
              'A short delay can be an early sign of low fluid or wear. It is usually cheaper to fix when caught early, so it is worth a diagnostic rather than waiting until the car won’t move.')]},
    {'slug': 'car-stuck-in-gear', 'name': 'Can’t change gear',
     'title': 'Car Stuck in Gear or Won’t Upshift? Singapore | DMTS',
     'desc': 'Car stuck in first gear or only shifting up to third? Common gearbox causes, limp mode explained, and free towing to our Singapore workshop.',
     'h1': 'Car Stuck in Gear or Won’t Upshift: Help in Singapore',
     'seen': 'The car stays in first gear, or only shifts up to third, when moving off or while driving.',
     'causes': ['The gearbox has gone into limp mode after detecting a fault', 'A failed shift solenoid', 'Valve body problems', 'Low transmission fluid', 'Gearbox control unit or wiring faults'],
     'now': ['Drive slowly to a safe place and avoid highways', 'Don’t keep driving long distances in one gear', 'WhatsApp us: if the car can’t move, we tow it in free during office hours'],
     'img': ('gearbox-removal', 'Gearbox being removed with a transmission jack'),
     'services': ['gearbox-repair', 'free-towing'],
     'faq': [('What is limp mode?',
              'Many automatic gearboxes hold one gear when they detect a fault, to protect themselves from further damage. The car can still move slowly, but it needs a diagnostic to find out why.')]},
    {'slug': 'car-jerks-when-changing-gear', 'name': 'Jerking or gears slipping',
     'title': 'Car Jerks When Changing Gear? Singapore | DMTS',
     'desc': 'Car jerks when shifting, slips in and out of gear or pops into neutral? Common automatic gearbox causes and how we fix them in Singapore.',
     'h1': 'Car Jerks When Changing Gear or Slips Out of Gear: Singapore Repair',
     'seen': 'The car jerks when shifting up or down, slips in and out of gear, or pops into neutral while driving.',
     'causes': ['Worn clutch packs or bands inside the gearbox', 'Low or degraded transmission fluid (ATF)', 'Valve body or shift solenoid faults', 'Torque converter problems'],
     'now': ['Avoid hard acceleration and towing loads', 'Check for fluid leaks where you park', 'Book a diagnostic: slipping usually gets worse with time'],
     'img': ('gearbox-teardown', 'Automatic gearbox opened up on the teardown bench'),
     'services': ['gearbox-repair', 'gearbox-servicing'],
     'faq': [('Will changing the gearbox oil fix jerking?',
              'Sometimes, if the fluid is low or worn out. But jerking can also come from worn clutches or a faulty valve body, which fresh fluid won’t fix. A diagnostic tells you which it is before you spend money.')]},
    {'slug': 'car-vibrates-when-accelerating', 'name': 'Vibration',
     'title': 'Car Vibrates When Accelerating? Singapore | DMTS',
     'desc': 'Car vibrates at high speed on low RPM or when accelerating hard from a stop? Possible gearbox causes and how we check them in Singapore.',
     'h1': 'Car Vibrates When Accelerating: Gearbox Causes in Singapore',
     'seen': 'The car vibrates at high speed on low RPM, or when accelerating hard from a standstill.',
     'causes': ['Torque converter (lock-up clutch) problems', 'Worn engine or gearbox mounts', 'Low or degraded transmission fluid', 'Drivetrain parts such as drive shafts'],
     'now': ['Note the speed and RPM when it happens', 'Avoid hard acceleration until it is checked', 'Book a diagnostic to find out whether it is the gearbox or another part'],
     'img': ('workshop-lifts', 'Car on a lift in the Dynamic Motoring workshop'),
     'services': ['gearbox-repair', 'gearbox-upgrade'],
     'faq': [('Is vibration always a gearbox problem?',
              'No. Vibration can also come from mounts, tyres or drive shafts. Our diagnostic checks the gearbox first, and we will tell you if the cause is elsewhere.')]},
    {'slug': 'transmission-fluid-leak', 'name': 'ATF leaking or low',
     'title': 'Transmission Fluid Leak Repair Singapore | DMTS',
     'desc': 'Bright red oil stains under your parked car? It may be automatic transmission fluid. Common leak causes and why low ATF damages a gearbox.',
     'h1': 'Transmission Fluid Leak in Singapore: Red Oil Under the Car',
     'seen': 'Bright red oil (ATF) stains on the floor after the car has been parked for a while.',
     'causes': ['Worn or leaking gearbox seals', 'A leaking transmission pan gasket', 'Damaged transmission cooler lines', 'Loose or damaged drain or fill plugs'],
     'now': ['Don’t just keep topping up: find and fix the leak', 'Watch for slipping or harsh shifts, signs the fluid is already low', 'Book a check before low fluid overheats the gearbox'],
     'img': ('atf-fluids', 'Automatic transmission fluid used for gearbox servicing'),
     'services': ['gearbox-servicing', 'gearbox-repair'],
     'faq': [('Is it safe to drive with a transmission fluid leak?',
              'A small leak can be driven to a workshop, but low fluid makes a gearbox overheat and slip, which can lead to a much bigger repair. Get it checked soon, and don’t ignore it.')]},
    {'slug': 'gearbox-noise', 'name': 'Gearbox noise',
     'title': 'Gearbox Noise: Whining or Clunking? Singapore | DMTS',
     'desc': 'Loud noise from the gearbox when the engine starts or while driving? Common causes of whining, humming and clunking gearboxes in Singapore cars.',
     'h1': 'Gearbox Noise in Singapore: Whining, Humming or Clunking',
     'seen': 'A loud noise from the gearbox once the engine starts or while the car is moving.',
     'causes': ['Worn bearings inside the gearbox', 'Low transmission fluid', 'Torque converter problems', 'Worn gear sets'],
     'now': ['Note whether the noise happens in Park, in gear or only while moving', 'Check for fluid leaks', 'Book a diagnostic: noises rarely go away on their own'],
     'img': ('gearbox-parts', 'Clutch packs and gear sets from an automatic gearbox'),
     'services': ['gearbox-repair', 'gearbox-servicing'],
     'faq': [('Why does my gearbox whine?',
              'A whine that changes with speed often points to worn bearings or gears, or low fluid. A diagnostic can narrow it down before the wear causes more damage.')]},
]
PROBLEM_BY = {p['slug']: p for p in PROBLEMS}
SERVICE_NAME = {sid: t for sid, t, *_ in SERVICES}
SERVICE_ROW = {sid: (sid, t, im, alt, d) for sid, t, im, alt, d in SERVICES}


def faq_ld():
    import re
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in FAQ]}


def crumbs_ld(name, path, parent=None):
    trail = [('Home', '')] + ([parent] if parent else []) + [(name, path)]
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': html.unescape(n), 'item': ORIGIN + BASE + p} for i, (n, p) in enumerate(trail)]}


def page_hero(name, h1, sub, parent=None):
    mid = f'<a href="{u(parent[1])}">{e(parent[0])}</a> › ' if parent else ''
    return (f'<div class="page-hero"><div class="wrap"><div class="crumbs"><a href="{u()}">Home</a> › {mid}{e(html.unescape(name))}</div>'
            f'<h1>{h1}</h1><p>{sub}</p></div></div>')


def faq_ld_of(items):
    import re
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in items]}


def faq_block(items, heading):
    return (f'<section class="alt"><div class="wrap" style="max-width:860px"><div class="sec-head"><h2>{heading}</h2></div>'
            + ''.join(f'<details><summary>{e(q)}</summary><div class="a">{a}</div></details>' for q, a in items)
            + '</div></section>')


def band(h, p):
    return (f'<section><div class="wrap"><div class="band"><div><h2>{h}</h2><p>{p}</p></div>'
            f'{cta_buttons()}</div></div></section>')


WHY = [
    ('gear', 'Specialist', 'Auto transmission repair and overhaul for all types of vehicles.'),
    ('tag', 'Direct pricing', 'A clear quote after the diagnostic, before any work starts. You pay only for what is needed.'),
    ('drop', 'Quality parts &amp; ATF', 'High quality parts and the correct Automatic Transmission Fluid for your gearbox.'),
    ('users', 'Experienced team', 'Experienced, well-trained mechanics with over 15 years of combined gearbox experience.'),
    ('shield', '6-month warranty', WARRANTY),
    ('truck', 'Free towing', 'Free pick-up or tow to our workshop during office hours.'),
]


def why_cards():
    return ''.join(f'<div class="card"><div class="ico">{ICON[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i, t, d in WHY)


def testimonials():
    return ''.join(f'<blockquote class="card quote"><p>“{e(q)}”</p>'
                   f'<cite>{e(n)}</cite> <span class="muted">· {e(c)}</span></blockquote>' for n, c, q in TESTIMONIALS)


def faq_html():
    return ''.join(f'<details><summary>{e(q)}</summary><div class="a">{a}</div></details>' for q, a in FAQ)


def loc_cards(maps=False):
    out = []
    for key, tag, label in (('hq', 'Headquarters', 'Woodlands (Wave 9)'), ('branch', 'Branch', 'Jalan Lam Huat')):
        a = BIZ[key]
        from urllib.parse import quote
        q = quote(a['map'])
        m = (f'<iframe class="map" title="Map: Dynamic Motoring {e(label)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
             f'src="https://www.google.com/maps?q={q}&amp;output=embed"></iframe>') if maps else ''
        out.append(f'<div class="card loc"><span class="tag">{tag}</span><h3>{e(label)}</h3>'
                   f'<p>{e(a["street"])}<br>Singapore {a["postal"]}</p>'
                   f'<a class="btn btn-line" href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener">Directions</a>{m}</div>')
    return ''.join(out)


HOURS = ('<dl class="hours"><dt>Mon – Fri</dt><dd>9:00am – 6:00pm</dd><dt>Saturday</dt><dd>9:00am – 3:00pm</dd>'
         '<dt>Sun &amp; PH</dt><dd>Closed</dd></dl>')


# ---------- pages ----------
def home():
    svc = service_cards()
    sym = problem_cards()
    gal = ''.join(f'<figure>{img(n, a)}<figcaption>{e(a)}</figcaption></figure>' for n, a in GALLERY[:6])
    body = f'''
<section class="hero" style="padding:0">
{img("hero-workshop", "Dynamic Motoring gearbox workshop in Woodlands", 800, 600, lazy=False, cls="bg")}
<div class="wrap">
<span class="eyebrow">Gearbox specialist · Singapore</span>
<h1>Gearbox Repair &amp; Auto Transmission Specialist in Singapore</h1>
<p class="lead">Dynamic Motoring repairs, overhauls, upgrades and services automatic gearboxes for all car makes. Pre-repair diagnostic from S$30, free towing to our workshop, and a 6-month warranty on repairs.</p>
<ul class="chips"><li>Diagnostic from S$30</li><li>Free towing / pick-up</li><li>6-month warranty</li><li>15+ years combined experience</li></ul>
{cta_buttons()}
</div>
</section>

<section><div class="wrap">
<div class="sec-head"><h2>Why drivers bring their gearbox to DMTS</h2><p>We only do transmissions, so we find the real fault faster and recommend only the repair you need.</p></div>
<div class="grid g3 why">{why_cards()}</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="sec-head"><h2>Our gearbox services</h2><p>From a quick ATF service to a full transmission overhaul or performance upgrade.</p></div>
<div class="grid g4 svc">{svc}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>Gearbox problems we fix</h2><p>Noticed one of these? Book a diagnostic before a small fault becomes a full overhaul.</p></div>
<div class="sym compact">{sym}</div>
<p style="margin-top:22px"><a class="btn btn-wa" href="{wa_link("Hi Dynamic Motoring, my car has a gearbox problem. Car model: ")}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp us your symptoms</a>
<a class="btn btn-line" href="{u("gearbox-problems/")}">All gearbox problems</a></p>
</div></section>

<section class="alt"><div class="wrap split">
<div>
<h2>Know the fault before you pay for a repair</h2>
<p>Gearbox symptoms can have very different causes, from a worn solenoid to a failing torque converter. So we diagnose first, then quote. You decide before any repair work starts.</p>
<ul class="ticks"><li>{DIAG}</li><li>Clear quote before any work starts</li><li>Standard 6-month warranty on repairs</li></ul>
<a class="btn btn-wa" href="{wa_link("Hi Dynamic Motoring, I would like to book a gearbox diagnostic.")}" target="_blank" rel="noopener">{ICON["wa"]}Book a diagnostic</a>
</div>
<div>{img("diagnostics", "Laptop running a transmission diagnostic test on a BMW")}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>What our customers say</h2></div>
<div class="grid g3" tabindex="0" role="region" aria-label="Customer reviews">{testimonials()}</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="sec-head"><h2>Inside our workshop</h2><p>Dedicated gearbox teardown stations, diagnostic equipment and an air-conditioned lounge where you can watch your car being worked on.</p></div>
<div class="gallery home-gal">{gal}</div>
<p style="margin-top:20px"><a class="btn btn-line" href="{u("gallery/")}">View all photos</a></p>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>Two workshops in the north</h2></div>
<div class="grid g2">{loc_cards()}</div>
<div class="card" style="margin-top:18px">{HOURS}</div>
</div></section>

<section class="alt"><div class="wrap" style="max-width:860px">
<div class="sec-head"><h2>Gearbox repair FAQ</h2></div>
{faq_html()}
</div></section>

{band("Gearbox acting up?", "WhatsApp or call us. If the car can’t move, we’ll tow it in for free.")}
'''
    return page('', 'Gearbox Repair & Transmission Specialist Singapore | DMTS',
                'Gearbox repair, overhaul and servicing for all car makes in Woodlands, Singapore. Diagnostic from S$30, free towing and a 6-month warranty. WhatsApp 8430 9665.',
                body, active='', ld=[faq_ld()], share=('hero-workshop', 'Gearbox Repair & Auto Transmission Specialist in Singapore'))


def services():
    blocks = []
    for i, (sid, t, im, alt, d) in enumerate(SERVICES):
        pic = f'<div>{img(im, alt)}</div>'
        more = f'<a class="btn btn-line" href="{u("services/" + sid + "/")}">Full details</a>'
        txt = f'<div><h2>{t}</h2><p>{d}</p>{cta_buttons(more)}</div>'
        blocks.append(f'<section id="{sid}"{" class=\"alt\"" if i % 2 else ""}><div class="wrap split">'
                      f'{txt + pic if i % 2 else pic + txt}</div></section>')
    body = (page_hero('Services', 'Gearbox Repair, Overhaul, Upgrade &amp; Servicing',
                      'Everything we do is about your transmission: diagnosis, repair, overhaul, strengthening upgrades and ATF servicing, for all car makes.')
            + ''.join(blocks)
            + f'<section><div class="wrap"><div class="sec-head"><h2>Signs your gearbox needs a check</h2></div><div class="sym">'
            + problem_cards()
            + '</div></div></section>'
            + faq_block(FAQ[:5], 'Gearbox service questions')
            + trust_strip()
            + band('Not sure what’s wrong?', 'Our pre-repair diagnostic starts from S$30. We’ll tell you the fault and the price before any work starts.'))
    ld = [crumbs_ld('Services', 'services/'), faq_ld_of(FAQ[:5]), {
        '@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'Service', 'name': html.unescape(t), 'description': d,
                                                               'provider': {'@id': f'{ORIGIN}{BASE}#org'}, 'areaServed': 'Singapore',
                                                               'url': f'{ORIGIN}{BASE}services/{sid}/'}}
            for i, (sid, t, im, alt, d) in enumerate(SERVICES)]}]
    return page('services/', 'Gearbox Repair, Overhaul & Servicing Singapore | DMTS',
                'Automatic gearbox repair and overhaul, transmission strengthening upgrades, ATF servicing and free towing in Singapore. All car makes. Diagnostic from S$30.',
                body, active='services/', ld=ld, share=('gearbox-teardown', 'Gearbox Repair, Overhaul, Upgrade & Servicing'))


def problem_cards(slugs=None):
    ps = [PROBLEM_BY[s] for s in slugs] if slugs else PROBLEMS
    return ''.join(f'<a class="card" href="{u("gearbox-problems/" + p["slug"] + "/")}" style="text-decoration:none;color:inherit">'
                   f'<h3>{e(p["name"])}</h3><p class="muted">{e(p["seen"])}</p><span class="more">What it means →</span></a>' for p in ps)


def service_cards(sids=None):
    rows = [SERVICE_ROW[s] for s in sids] if sids else SERVICES
    return ''.join(f'<a class="card img" href="{u("services/" + sid + "/")}" style="text-decoration:none;color:inherit">{img(im, alt)}'
                   f'<div class="body"><h3>{t}</h3><p class="muted">{d[:118].rsplit(" ", 1)[0]}…</p><span class="more">Learn more →</span></div></a>'
                   for sid, t, im, alt, d in rows)


def trust_strip(reviews=True):
    rv = f'<section><div class="wrap"><div class="sec-head"><h2>What our customers say</h2></div><div class="grid g3" tabindex="0" role="region" aria-label="Customer reviews">{testimonials()}</div></div></section>'
    return ((rv if reviews else '') + f'<section class="alt"><div class="wrap"><div class="sec-head"><h2>Our workshops in Woodlands and Jalan Lam Huat</h2></div>'
            f'<div class="grid g2">{loc_cards()}</div><div class="card" style="margin-top:18px">{HOURS}</div></div></section>')


def service_page(sid):
    _, t, im, alt, d = SERVICE_ROW[sid]
    sp = SERVICE_PAGES[sid]
    faq = [(q, FAQ_BY_Q[q]) for q in sp['faq']]
    others = [s for s, *_ in SERVICES if s != sid]
    secs = ''.join(f'<section{" class=\"alt\"" if i % 2 == 0 else ""}><div class="wrap" style="max-width:860px"><h2>{h}</h2>{b}</div></section>'
                   for i, (h, b) in enumerate(sp['sections']))
    body = (page_hero(t, sp['h1'], sp['sub'], parent=('Services', 'services/'))
            + f'''<section><div class="wrap split">
<div><h2>{t} at Dynamic Motoring</h2><p>{d}</p>
<ul class="ticks"><li>{DIAG}</li><li>Clear quote before any work starts</li><li>{WARRANTY}</li><li>Free towing to our workshop during office hours</li></ul>
{cta_buttons()}</div>
<div>{img(im, alt)}</div>
</div></section>'''
            + secs
            + f'<section><div class="wrap"><div class="sec-head"><h2>Problems this fixes</h2></div><div class="sym">{problem_cards(sp["problems"])}</div></div></section>'
            + faq_block(faq, f'{t}: common questions')
            + trust_strip()
            + f'<section><div class="wrap"><div class="sec-head"><h2>Other gearbox services</h2></div><div class="grid g3">{service_cards(others)}</div></div></section>'
            + band('Talk to a gearbox specialist', 'WhatsApp us your car model and symptoms. If the car can’t move, we’ll tow it in for free.'))
    ld = [crumbs_ld(t, f'services/{sid}/', parent=('Services', 'services/')), faq_ld_of(faq),
          {'@context': 'https://schema.org', '@type': 'Service', 'name': html.unescape(t), 'description': d, 'serviceType': html.unescape(t),
           'provider': {'@id': f'{ORIGIN}{BASE}#org'}, 'areaServed': {'@type': 'Country', 'name': 'Singapore'}, 'url': f'{ORIGIN}{BASE}services/{sid}/',
           'image': f'{IMG_ORIGIN}/img/share/services-{sid}.jpg'}]
    return page(f'services/{sid}/', sp['title'], sp['desc'], body, active='services/', ld=ld, share=(im, html.unescape(sp['h1'])))


HUB_FAQ = [(q, FAQ_BY_Q[q]) for q in ['What are the signs my gearbox needs attention?', 'How much is the diagnostic?',
                                     'How much does a gearbox repair cost in Singapore?', 'My car can’t move. Can you tow it?',
                                     'Which car brands do you work on?']]


def problems_hub():
    body = (page_hero('Gearbox Problems', 'Common Gearbox Problems in Singapore and What They Mean',
                      'Noticed something wrong with your automatic gearbox? Find your symptom below to see the usual causes and what to do next.')
            + f'<section><div class="wrap"><div class="sec-head"><h2>Find your symptom</h2></div><div class="sym">{problem_cards()}</div></div></section>'
            + f'''<section class="alt"><div class="wrap split">
<div><h2>Not sure which one it is?</h2><p>Gearbox symptoms often overlap, and the same symptom can have very different causes. Our pre-repair diagnostic reads the transmission fault codes and checks the gearbox, then we tell you the fault and the price before any work starts.</p>
<ul class="ticks"><li>{DIAG}</li><li>Clear quote before any work starts</li><li>Free towing if the car can’t move</li></ul>{cta_buttons()}</div>
<div>{img("diagnostics", "Transmission diagnostic test running on a laptop")}</div></div></section>'''
            + faq_block(HUB_FAQ, 'Gearbox problem FAQ')
            + trust_strip()
            + band('Gearbox acting up?', 'WhatsApp or call us. If the car can’t move, we’ll tow it in for free.'))
    ld = [crumbs_ld('Gearbox Problems', 'gearbox-problems/'), faq_ld_of(HUB_FAQ),
          {'@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [
              {'@type': 'ListItem', 'position': i + 1, 'name': p['name'], 'url': f'{ORIGIN}{BASE}gearbox-problems/{p["slug"]}/'} for i, p in enumerate(PROBLEMS)]}]
    return page('gearbox-problems/', 'Common Gearbox Problems & Symptoms Singapore | DMTS',
                'Transmission light on, jerking, slipping, stuck in gear, leaks, vibration or noise? What each gearbox symptom can mean and what to do next.',
                body, active='gearbox-problems/', ld=ld, share=('diagnostics', 'Common Gearbox Problems and What They Mean'))


def problem_page(slug):
    p = PROBLEM_BY[slug]
    faq = p['faq'] + [('How much does it cost to fix?',
                       f'It depends on the cause, so we don’t quote blind. Our pre-repair diagnostic starts from S$30, and we give you a clear quote before any work starts. <a href="{wa_link()}" target="_blank" rel="noopener">WhatsApp us</a> your car model and symptoms.')]
    li = lambda xs: ''.join(f'<li>{e(x)}</li>' for x in xs)
    others = [q['slug'] for q in PROBLEMS if q['slug'] != slug][:3]
    body = (page_hero(p['name'], p['h1'], e(p['seen']), parent=('Gearbox Problems', 'gearbox-problems/'))
            + f'''<section><div class="wrap split">
<div><h2>Common causes</h2><p>These are the usual reasons for this symptom in an automatic gearbox. More than one can be involved, which is why we diagnose before quoting.</p>
<ul class="ticks">{li(p["causes"])}</ul></div>
<div>{img(*p["img"])}</div>
</div></section>
<section class="alt"><div class="wrap" style="max-width:860px">
<h2>What to do now</h2><ul class="ticks">{li(p["now"])}</ul>
<h3>Why it pays to check early</h3>
<p>An automatic gearbox rarely fixes itself. A fault that starts as a sensor, a solenoid or low fluid can, if the car keeps being driven, wear the clutches and other internal parts, and a simple repair can turn into a full overhaul. Finding the cause early usually means a smaller, cheaper fix, which is why we diagnose first and quote before any work starts.</p>
</div></section>
<section><div class="wrap" style="max-width:860px">
<h2>How we find and fix it</h2>
<ol class="steps"><li><strong>Tell us what’s happening.</strong> WhatsApp <a href="{wa_link("Hi Dynamic Motoring, my car has a gearbox problem. Car model: ")}" target="_blank" rel="noopener">{BIZ["mobile_disp"]}</a> with your car model and the symptom.</li>
<li><strong>Diagnostic from S$30.</strong> We read the transmission fault codes and check the gearbox to find the actual cause.</li>
<li><strong>Clear quote first.</strong> You know the fault and the price before any repair starts.</li>
<li><strong>Repair with warranty.</strong> {WARRANTY}</li></ol>
{cta_buttons()}
</div></section>'''
            + f'<section class="alt"><div class="wrap"><div class="sec-head"><h2>Related services</h2></div><div class="grid g3">{service_cards(p["services"])}</div></div></section>'
            + faq_block(faq, 'Questions about this problem')
            + trust_strip()
            + f'<section><div class="wrap"><div class="sec-head"><h2>Other gearbox problems</h2></div><div class="sym">{problem_cards(others)}</div></div></section>')
    ld = [crumbs_ld(p['name'], f'gearbox-problems/{slug}/', parent=('Gearbox Problems', 'gearbox-problems/')), faq_ld_of(faq)]
    return page(f'gearbox-problems/{slug}/', p['title'], p['desc'], body, active='gearbox-problems/', ld=ld, share=(p['img'][0], p['h1']))


def all_pages():
    return ([p for p, _ in NAV] + [f'services/{s}/' for s, *_ in SERVICES] + [f'gearbox-problems/{p["slug"]}/' for p in PROBLEMS])


def retired_estimator():
    # DMTS no longer publishes repair prices (they quote after a diagnostic), so the old
    # estimator URL just forwards to the home page.
    return f'''<!doctype html>
<html lang="en-SG"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<title>Dynamic Motoring</title><link rel="canonical" href="{ORIGIN}{BASE}">
<meta http-equiv="refresh" content="0; url={u()}"></head>
<body><p><a href="{u()}">Continue to Dynamic Motoring</a></p></body></html>
'''


def gallery():
    gal = ''.join(f'<figure>{img(n, a)}<figcaption>{e(a)}</figcaption></figure>' for n, a in GALLERY)
    body = (page_hero('Gallery', 'Our Gearbox Workshop in Woodlands, Singapore',
                      'A look inside Dynamic Motoring: diagnostic equipment, gearbox teardown benches, transmission jacks and our customer lounge.')
            + f'<section><div class="wrap"><div class="gallery">{gal}</div></div></section>'
            + f'''<section class="alt"><div class="wrap" style="max-width:860px">
<h2>Built for gearbox work</h2>
<p>Our workshop is set up for automatic transmissions: dedicated gearbox teardown benches, transmission jacks for removing and refitting gearboxes, car lifts, and diagnostic tools specialising in auto transmission. We use the manufacturer’s recommended or gearbox-specific brand of ATF, such as the Fuchs Titan fluids in our servicing bay.</p>
<h2>Wait in comfort</h2>
<p>Our air-conditioned customer lounge has a clear view of the workshop, so you can watch your car being worked on, and an automatic transmission cutaway on display that shows what is inside a gearbox.</p>
</div></section>'''
            + faq_block(FAQ[4:], 'Visiting us')
            + trust_strip()
            + band('Come and see us', 'Visit our Woodlands HQ or Jalan Lam Huat branch, or let us pick your car up for free.'))
    return page('gallery/', 'Gearbox Workshop Photos, Woodlands Singapore | DMTS',
                'Photos of the Dynamic Motoring gearbox workshop in Woodlands, Singapore: diagnostics, gearbox overhaul benches, car lifts and customer lounge.',
                body, active='gallery/', ld=[crumbs_ld('Gallery', 'gallery/'), faq_ld_of(FAQ[4:])], share=('customer-lounge', 'Inside Our Gearbox Workshop in Woodlands'))


def about():
    body = page_hero('About', 'About Dynamic Motoring (DMTS)',
                     '“15 years of combined industry experience working on gearbox repair and overhaul.”') + f'''
<section><div class="wrap split">
<div>
<h2>Transmission specialists, not general mechanics</h2>
<p>DMTS’ team of specialists have over 15 years of combined industry experience in gearbox repair and overhaul. With wide and in-depth knowledge of different transmission systems and models, we follow a rigorous, stringent process to solve any gearbox issue. Our transmission specialists are constantly trained and kept up to date on the latest developments in the auto transmission industry.</p>
<h3>What we believe</h3>
<p>We believe in giving every customer the most direct and accurate gearbox solution for their specific problem, to save them time and money. That is only possible with an experienced team of transmission specialists and an extensive range of special tools and equipment.</p>
<p>Our focus on customers’ needs, and meeting their expectations, is why drivers choose us as their trusted workshop for gearbox repair.</p>
</div>
<div>{img("mechanics-under-car", "Dynamic Motoring mechanics inspecting a car on a lift")}</div>
</div></section>
<section class="alt"><div class="wrap split">
<div>{img("transmission-cutaway", "Automatic transmission cutaway on display in the DMTS lounge")}</div>
<div>
<h2>Our strengths</h2>
<ul class="ticks">
<li>Specialist in auto transmission repair &amp; overhaul of all types of vehicles</li>
<li>Experienced &amp; well-trained mechanics in gearbox repair</li>
<li>Competitive and direct pricing for transmission issues</li>
<li>Standard 6-month warranty on repairs</li>
<li>High quality parts and Automatic Transmission Fluid (ATF)</li>
<li>Comfortable waiting lounge with a clear view of your car</li>
</ul>
</div>
</div></section>
<section><div class="wrap"><div class="sec-head"><h2>What our customers say</h2></div><div class="grid g3" tabindex="0" role="region" aria-label="Customer reviews">{testimonials()}</div></div></section>
''' + faq_block(FAQ, 'Frequently asked questions') + trust_strip(reviews=False) + band('Talk to a gearbox specialist', 'Call, WhatsApp or drop by either workshop.')
    return page('about/', 'About Dynamic Motoring | Gearbox Specialist Singapore',
                'Dynamic Motoring (DMTS) is a Singapore gearbox and auto transmission specialist with over 15 years of combined experience in gearbox repair and overhaul.',
                body, active='about/', ld=[crumbs_ld('About', 'about/'), faq_ld_of(FAQ)], share=('mechanics-under-car', 'Transmission Specialists with 15+ Years of Combined Experience'))


def contact():
    body = page_hero('Contact', 'Contact Dynamic Motoring',
                     'WhatsApp is the fastest way to reach us. If your car can’t move, we’ll arrange free towing during office hours.') + f'''
<section><div class="wrap">
<div class="grid g2">
<div class="card">
<h2 style="font-size:1.4rem">Get in touch</h2>
<p><strong>WhatsApp (preferred):</strong> <a href="{wa_link()}" target="_blank" rel="noopener">{BIZ["mobile_disp"]}</a><br>
<strong>Office:</strong> <a href="tel:{BIZ["tel"]}">{BIZ["tel_disp"]}</a><br>
<strong>Fax:</strong> {BIZ["fax_disp"]}<br>
<strong>Email:</strong> <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a><br>
<strong>Find us on:</strong> <a href="{BIZ["facebook"]}" target="_blank" rel="noopener">Facebook</a> · <a href="{BIZ["google"]}" target="_blank" rel="noopener">Google</a></p>
{HOURS}
<div style="margin-top:18px">{cta_buttons()}</div>
</div>
<form class="card" id="qform">
<h2 style="font-size:1.4rem">Book a diagnostic</h2>
<p class="muted">This opens WhatsApp with your message ready to send.</p>
<label class="f" for="q-name">Name</label><input id="q-name" type="text" autocomplete="name" required>
<label class="f" for="q-phone" style="margin-top:12px">Contact number</label><input id="q-phone" type="tel" autocomplete="tel" required>
<label class="f" for="q-car" style="margin-top:12px">Car make &amp; model</label><input id="q-car" type="text" placeholder="e.g. BMW 520i, 2016">
<label class="f" for="q-msg" style="margin-top:12px">What’s happening?</label><textarea id="q-msg" placeholder="e.g. jerks when shifting from 2nd to 3rd"></textarea>
<div class="btns" style="margin-top:14px"><button class="btn btn-wa" type="submit">{ICON["wa"]}Send on WhatsApp</button>
<button class="btn btn-line" type="button" id="q-mail">Send by email</button></div>
</form>
</div>
</div></section>
<section class="alt"><div class="wrap">
<div class="sec-head"><h2>Our workshops</h2></div>
<div class="grid g2">{loc_cards(maps=True)}</div>
</div></section>
<section><div class="wrap" style="max-width:860px">
<h2>Before you come in</h2>
<p>Tell us your car make and model and what the gearbox is doing, for example a warning light, jerking between gears, slipping or a noise. It helps us plan the diagnostic. If the car can still be driven safely, drive in to either workshop during opening hours. If it can’t move, we arrange free towing to our workshop during office hours.</p>
<h2>After the diagnostic</h2>
<p>Our pre-repair diagnostic starts from S$30. We tell you the fault and give you a clear quote before any work starts, and repairs come with a standard 6-month warranty unless otherwise stated.</p>
</div></section>
''' + faq_block(FAQ[:5], 'Common questions') + f'<section><div class="wrap"><div class="sec-head"><h2>What our customers say</h2></div><div class="grid g3" tabindex="0" role="region" aria-label="Customer reviews">{testimonials()}</div></div></section>'
    return page('contact/', 'Contact | Dynamic Motoring Gearbox Specialist Singapore',
                'Contact Dynamic Motoring for gearbox repair in Singapore. WhatsApp 8430 9665 or call 6352 8832. Workshops at Wave 9 Woodlands and Jalan Lam Huat.',
                body, active='contact/', ld=[crumbs_ld('Contact', 'contact/'), faq_ld_of(FAQ[:5])], share=('shopfront', 'Contact Dynamic Motoring: Woodlands & Jalan Lam Huat'),
                scripts=f'<script>window.DMTS_EMAIL="{BIZ["email"]}";</script>')


def not_found():
    # Served by Apache (ErrorDocument in .htaccess) at whatever URL was missing, so links are root-relative.
    global ABS
    ABS = True
    try:
        body = (page_hero('Page not found', 'Sorry, we can’t find that page',
                          'The page may have moved when we rebuilt our website. Try one of these, or WhatsApp us and we’ll help.')
                + f'''<section><div class="wrap">
<div class="sec-head"><h2>Our gearbox services</h2></div>
<div class="grid g4 svc">{service_cards()}</div>
<p style="margin-top:22px"><a class="btn btn-line" href="{u()}">Home</a> <a class="btn btn-line" href="{u("gearbox-problems/")}">Gearbox problems</a> <a class="btn btn-line" href="{u("contact/")}">Contact</a></p>
</div></section>'''
                + band('Gearbox acting up?', 'WhatsApp or call us. If the car can’t move, we’ll tow it in for free.'))
        html_ = page('404.html', 'Page not found | Dynamic Motoring', 'This page does not exist on dmts.com.sg.', body)
    finally:
        ABS = False
        SHARES.pop('404.html', None)
    html_ = html_.replace('<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex, follow">')
    return re.sub(r'<link rel="canonical"[^>]*>\n', '', html_)


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote', rel, len(text.encode()), 'bytes')


def robots_txt():
    return f'User-agent: *\nAllow: /\n\nSitemap: {ORIGIN}/sitemap.xml\n'


def sitemap():
    import datetime
    today = datetime.date.today().isoformat()
    urls = ''.join(f'<url><loc>{ORIGIN}{BASE}{p}</loc><lastmod>{today}</lastmod></url>' for p in all_pages())
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'


def llms_txt():
    import re
    txt = lambda h: html.unescape(re.sub(r'<[^>]+>', '', h))
    svc = '\n'.join(f'- {txt(name)}: {txt(body).split(". ")[0]}.' for _, name, _, _, body, *rest in SERVICES)
    faq = '\n'.join(f'- {txt(q)} {txt(a)}' for q, a in FAQ[:6])
    hq, br = BIZ['hq'], BIZ['branch']
    return f'''# {BIZ['name']} ({BIZ['short']})

> Gearbox and automatic transmission repair, overhaul, upgrade and servicing specialist in Singapore.

- WhatsApp: {BIZ['mobile_disp']} (preferred) · Tel: {BIZ['tel_disp']} · Email: {BIZ['email']}
- Woodlands HQ: {hq['street']}, Singapore {hq['postal']}
- Branch: {br['street']}, Singapore {br['postal']}
- Hours: Mon-Fri 9am-6pm, Sat 9am-3pm, closed Sundays and public holidays
- {DIAG}. {WARRANTY}

## Services
{svc}

## Pages
''' + '\n'.join(f'- [{n}]({ORIGIN}/{p})' for p, n in NAV) + '\n' + '\n'.join(
        f'- [{txt(t)}]({ORIGIN}/services/{sid}/)' for sid, t, *_ in SERVICES) + '\n' + '\n'.join(
        f'- [{p["name"]}]({ORIGIN}/gearbox-problems/{p["slug"]}/): {p["seen"]}' for p in PROBLEMS) + f'''

## Common questions
{faq}
'''


def build(rel, fn):
    global DEPTH
    DEPTH = rel.count('/')
    write(rel, fn())


if __name__ == '__main__':
    build('index.html', home)
    build('services/index.html', services)
    for sid, *_ in SERVICES:
        build(f'services/{sid}/index.html', lambda sid=sid: service_page(sid))
    build('gearbox-problems/index.html', problems_hub)
    for prob in PROBLEMS:
        build(f'gearbox-problems/{prob["slug"]}/index.html', lambda s=prob['slug']: problem_page(s))
    build('cost-estimator/index.html', retired_estimator)
    build('price-estimator/index.html', retired_estimator)  # the old WordPress estimator's real address
    build('404.html', not_found)
    build('gallery/index.html', gallery)
    build('about/index.html', about)
    build('contact/index.html', contact)
    # Only read when dmts.com.sg serves this folder; pageonesingapore.com uses its own root robots.txt.
    build('robots.txt', robots_txt)
    build('sitemap.xml', sitemap)
    build('llms.txt', llms_txt)
    build(f'{INDEXNOW_KEY}.txt', lambda: INDEXNOW_KEY)
    build('site.webmanifest', lambda: json.dumps({
        'name': 'Dynamic Motoring', 'short_name': 'DMTS', 'start_url': './', 'display': 'standalone',
        'background_color': '#ffffff', 'theme_color': '#0b1e33',
        'icons': [{'src': f'icon-{n}.png', 'sizes': f'{n}x{n}', 'type': 'image/png'} for n in (192, 512)]}, indent=1))
    import share
    share.icons()
    for slug, (photo, headline) in SHARES.items():
        share.card(slug, photo, headline)
    print('share images', len(SHARES))
