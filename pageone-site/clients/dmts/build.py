#!/usr/bin/env python3
"""Build the Dynamic Motoring (DMTS) site published at pageonesingapore.com/dmts/.

    python3 build.py            # writes the HTML pages into ./site

Content comes from source/content.md and source/prices.json (captured from dmts.com.sg).
Shared assets (dmts.css, dmts.js, favicon.svg, img/) live in ./site and are edited by hand.
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')
BASE = '/dmts/'
ORIGIN = 'https://pageonesingapore.com'
ASSET_V = '1'

# Until DMTS approves this site and it replaces dmts.com.sg, keep it out of Google
# so it never competes with the client's own domain.
NOINDEX = True

BIZ = {
    'name': 'Dynamic Motoring',
    'short': 'DMTS',
    'tel': '+6563528832', 'tel_disp': '6352 8832',
    'mobile': '+6584309665', 'mobile_disp': '8430 9665',
    'wa': '6584309665',
    'fax_disp': '6352 8831',
    'email': 'sales@dmts.com.sg',
    'hq': {'street': '71 Woodlands Industrial Park E9, #01-25 Wave 9', 'postal': '757048',
           'map': '71 Woodlands Industrial Park E9 Wave 9 Singapore'},
    'branch': {'street': '60 Jalan Lam Huat, #05-48', 'postal': '737869',
               'map': '60 Jalan Lam Huat Singapore 737869'},
}
WA_TEXT = 'Hi Dynamic Motoring, I would like a quote for my gearbox.'

NAV = [('', 'Home'), ('services/', 'Services'), ('cost-estimator/', 'Cost Estimator'),
       ('gallery/', 'Gallery'), ('about/', 'About'), ('contact/', 'Contact')]

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
    return BASE + path


def wa_link(text=WA_TEXT):
    from urllib.parse import quote
    return f'https://wa.me/{BIZ["wa"]}?text={quote(text)}'


def cta_buttons(extra=''):
    return (f'<div class="btns">'
            f'<a class="btn btn-red" href="tel:{BIZ["tel"]}">{ICON["phone"]}Call {BIZ["tel_disp"]}</a>'
            f'<a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp us</a>'
            f'{extra}</div>')


def schema():
    def place(key, label):
        a = BIZ[key]
        return {
            '@type': 'AutoRepair', '@id': f'{ORIGIN}{BASE}#{key}',
            'name': f'Dynamic Motoring ({label})',
            'parentOrganization': {'@id': f'{ORIGIN}{BASE}#org'},
            'telephone': BIZ['tel'], 'email': BIZ['email'],
            'image': f'{ORIGIN}{BASE}img/shopfront.webp',
            'priceRange': 'S$300 - S$2,800',
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
         'url': f'{ORIGIN}{BASE}', 'logo': f'{ORIGIN}{BASE}img/logo.webp',
         'email': BIZ['email'], 'telephone': BIZ['tel'], 'sameAs': ['https://dmts.com.sg/'],
         'description': 'Gearbox and automatic transmission repair, overhaul, upgrade and servicing specialist in Singapore.'},
        place('hq', 'Woodlands HQ'), place('branch', 'Jalan Lam Huat branch')]}


def page(path, title, desc, body, active='', extra_head='', ld=None, scripts=''):
    canonical = ORIGIN + u(path)
    nav = ''.join(f'<a href="{u(p)}"{" aria-current=\"page\"" if p == active else ""}>{e(n)}</a>' for p, n in NAV)
    mnav = ''.join(f'<a href="{u(p)}">{e(n)}</a>' for p, n in NAV)
    lds = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ([schema()] + (ld or [])))
    robots = 'noindex, follow' if NOINDEX else 'index, follow, max-image-preview:large'
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Dynamic Motoring">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ORIGIN}{BASE}img/hero-workshop.webp">
<meta property="og:locale" content="en_SG">
<meta name="theme-color" content="#0b1e33">
<link rel="icon" href="{u("favicon.svg")}" type="image/svg+xml">
<link rel="stylesheet" href="{u("dmts.css")}?v={ASSET_V}">
{extra_head}{lds}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="topbar"><div class="wrap">
<span>Gearbox &amp; auto transmission specialist <span class="hide-sm">· Mon–Fri 9am–6pm · Sat 9am–3pm</span></span>
<span><a href="tel:{BIZ["tel"]}">{BIZ["tel_disp"]}</a> <span class="hide-sm">· After hours <a href="tel:{BIZ["mobile"]}">{BIZ["mobile_disp"]}</a></span></span>
</div></div>
<header class="site"><div class="wrap">
<a class="logo" href="{u()}"><img src="{u("img/logo.webp")}" width="360" height="127" alt="Dynamic Motoring"></a>
<nav class="main" aria-label="Main">{nav}</nav>
<a class="btn btn-red hdr-cta" href="tel:{BIZ["tel"]}">{ICON["phone"]}{BIZ["tel_disp"]}</a>
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
<p>Gearbox repair, overhaul, upgrade and servicing for continental, Japanese, Korean and other makes. Free diagnostic test and free towing to our workshop during office hours.</p>
<p><a href="tel:{BIZ["tel"]}">Tel {BIZ["tel_disp"]}</a><br><a href="tel:{BIZ["mobile"]}">After hours {BIZ["mobile_disp"]}</a><br>Fax {BIZ["fax_disp"]}<br><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></p>
</div>
<div>
<h3>Workshops</h3>
<p><strong>HQ</strong><br>{e(BIZ["hq"]["street"])}<br>Singapore {BIZ["hq"]["postal"]}</p>
<p><strong>Branch</strong><br>{e(BIZ["branch"]["street"])}<br>Singapore {BIZ["branch"]["postal"]}</p>
</div>
<div>
<h3>Pages</h3>
<ul>{''.join(f'<li><a href="{u(p)}">{e(n)}</a></li>' for p, n in NAV)}</ul>
<p style="margin-top:1em">Mon–Fri 9:00–18:00<br>Sat 9:00–15:00</p>
</div>
</div>
<div class="fine"><span>© 2026 Dynamic Motoring. All rights reserved.</span><a href="https://pageonesingapore.com/">Website &amp; SEO by Page One Singapore</a></div>
</div></footer>
<div class="dock">
<a class="btn btn-red" href="tel:{BIZ["tel"]}">{ICON["phone"]}Call</a>
<a class="btn btn-wa" href="{wa_link()}" target="_blank" rel="noopener">{ICON["wa"]}WhatsApp</a>
</div>
<script src="{u("dmts.js")}?v={ASSET_V}" defer></script>
{scripts}
</body>
</html>
'''


def img(name, alt, w=720, h=540, lazy=True, cls=''):
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

SYMPTOMS = [
    ('Transmission check light on', 'Engine or transmission check light on the dashboard while driving.'),
    ('Lack of response', 'Car hesitates or refuses to go into gear when you accelerate.'),
    ('Can’t change gear', 'Stuck in first gear, or only upshifts to third, when moving off or in motion.'),
    ('Jerking or gears slipping', 'Car jerks when shifting up or down, or slips in and out of gear (or pops into neutral) while driving.'),
    ('Vibration', 'Car vibrates at high speed on low RPM, or when accelerating hard from a standstill.'),
    ('ATF leaking or low', 'Bright red oil (ATF) stains on the floor after the car has been parked for a while.'),
    ('Gearbox noise', 'Loud noise from the gearbox once the engine starts or while the car is moving.'),
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
    ('teardown-bench', 'Dedicated gearbox teardown station'),
    ('gearbox-removal', 'Removing a gearbox with a transmission jack'),
    ('gearbox-jack', 'Gearbox lowered on a transmission jack'),
    ('transmission-cutaway', 'Automatic transmission cutaway display in the lounge'),
    ('atf-fluids', 'Fuchs Titan ATF used for gearbox servicing'),
    ('customer-lounge', 'Air-conditioned customer waiting lounge'),
]

FAQ = [
    ('How much does a gearbox repair cost in Singapore?',
     f'It depends on the car and the fault. As a guide, our estimator starts from S$300 for an ATF leak repair on Japanese and Korean cars, and a full transmission overhaul is S$1,800 for Japanese and Korean cars, S$2,500 for continental cars and S$2,800 for other makes. <a href="{BASE}cost-estimator/">Try the cost estimator</a>, then call us for a firm quote after the diagnostic test.'),
    ('Do you charge for diagnosis?',
     'The computer diagnostic test to read the transmission fault code is free (S$0 in our estimator).'),
    ('My car can’t move. Can you tow it?',
     f'Yes. We provide free pick-up to our workshop for gearbox repair during office hours, and if the car can’t move because of transmission failure we send a tow truck, free of charge. Call <a href="tel:{BIZ["tel"]}">{BIZ["tel_disp"]}</a>, or <a href="tel:{BIZ["mobile"]}">{BIZ["mobile_disp"]}</a> after office hours.'),
    ('Which car brands do you work on?',
     'All types of vehicles: continental (Audi, BMW, Mercedes-Benz, Volkswagen, Mini), Japanese (Toyota, Lexus, Honda, Mazda, Mitsubishi, Nissan, Subaru, Suzuki), Korean (Hyundai, Kia) and other makes such as Land Rover, Jaguar, Volvo, Ford, Renault, Peugeot, Citroën, Chevrolet and Opel.'),
    ('Is there a warranty after repair?',
     'Yes, every gearbox repair comes with a warranty for peace of mind. Ask us for the warranty terms for your repair when we quote.'),
    ('What are the signs my gearbox needs attention?',
     'A transmission check light, hesitation or refusing to go into gear, being stuck in one gear, jerking or slipping between gears, vibration at low RPM, red ATF stains under the car, or a loud noise from the gearbox. Any of these is worth a free diagnostic test before it gets worse.'),
    ('Where are your workshops and when are you open?',
     f'Our HQ is at {BIZ["hq"]["street"]}, Singapore {BIZ["hq"]["postal"]}, and our branch is at {BIZ["branch"]["street"]}, Singapore {BIZ["branch"]["postal"]}. We are open Monday to Friday 9am–6pm and Saturday 9am–3pm.'),
]


def faq_ld():
    import re
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': re.sub('<[^>]+>', '', a)}} for q, a in FAQ]}


def crumbs_ld(name, path):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': ORIGIN + BASE},
        {'@type': 'ListItem', 'position': 2, 'name': name, 'item': ORIGIN + BASE + path}]}


def page_hero(name, h1, sub):
    return (f'<div class="page-hero"><div class="wrap"><div class="crumbs"><a href="{u()}">Home</a> › {e(name)}</div>'
            f'<h1>{h1}</h1><p>{sub}</p></div></div>')


def band(h, p):
    return (f'<section><div class="wrap"><div class="band"><div><h2>{h}</h2><p>{p}</p></div>'
            f'{cta_buttons()}</div></div></section>')


WHY = [
    ('gear', 'Specialist', 'Auto transmission repair and overhaul for all types of vehicles.'),
    ('tag', 'Direct pricing', 'Competitive, direct pricing for transmission issues. You pay only for what is needed.'),
    ('drop', 'Quality parts &amp; ATF', 'High quality parts and the correct Automatic Transmission Fluid for your gearbox.'),
    ('users', 'Experienced team', 'Experienced, well-trained mechanics with over 15 years of combined gearbox experience.'),
    ('shield', 'Warranty', 'Warranty after repair, for peace of mind.'),
    ('truck', 'Free towing', 'Free pick-up or tow to our workshop during office hours.'),
]


def why_cards():
    return ''.join(f'<div class="card"><div class="ico">{ICON[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i, t, d in WHY)


def testimonials():
    return ''.join(f'<blockquote class="card quote"><div class="stars" aria-label="5 stars">★★★★★</div><p>“{e(q)}”</p>'
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
         '<dt>Sun &amp; PH</dt><dd>After-hours line <a href="tel:+6584309665">8430 9665</a></dd></dl>')


# ---------- pages ----------
def home():
    svc = ''.join(f'<a class="card img" href="{u("services/")}#{sid}" style="text-decoration:none;color:inherit">{img(im, alt)}'
                  f'<div class="body"><h3>{t}</h3><p class="muted">{d[:118].rsplit(" ", 1)[0]}…</p></div></a>'
                  for sid, t, im, alt, d in SERVICES)
    sym = ''.join(f'<div class="card"><h3>{e(t)}</h3><p class="muted">{e(d)}</p></div>' for t, d in SYMPTOMS[:6])
    gal = ''.join(f'<figure>{img(n, a)}<figcaption>{e(a)}</figcaption></figure>' for n, a in GALLERY[:6])
    body = f'''
<section class="hero" style="padding:0">
{img("hero-workshop", "Dynamic Motoring gearbox workshop in Woodlands", 1200, 900, lazy=False, cls="bg")}
<div class="wrap">
<span class="eyebrow">Gearbox specialist · Singapore</span>
<h1>Gearbox Repair &amp; Auto Transmission Specialist in Singapore</h1>
<p class="lead">Dynamic Motoring repairs, overhauls, upgrades and services automatic gearboxes for all car makes. Free diagnostic test, free towing to our workshop, and direct pricing you can check before you call.</p>
<ul class="chips"><li>Free diagnostic test</li><li>Free towing / pick-up</li><li>Warranty after repair</li><li>15+ years combined experience</li></ul>
{cta_buttons(f'<a class="btn btn-ghost" href="{u("cost-estimator/")}">Estimate my repair cost</a>')}
</div>
</section>

<section><div class="wrap">
<div class="sec-head"><h2>Why drivers bring their gearbox to DMTS</h2><p>We only do transmissions, so we find the real fault faster and recommend only the repair you need.</p></div>
<div class="grid g3">{why_cards()}</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="sec-head"><h2>Our gearbox services</h2><p>From a quick ATF service to a full transmission overhaul or performance upgrade.</p></div>
<div class="grid g4">{svc}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>Gearbox problems we fix</h2><p>Noticed one of these? Book a free diagnostic test before a small fault becomes a full overhaul.</p></div>
<div class="sym">{sym}</div>
<p style="margin-top:22px"><a class="btn btn-blue" href="{u("cost-estimator/")}">See prices for these problems</a></p>
</div></section>

<section class="alt"><div class="wrap split">
<div>
<h2>Know the cost before you come in</h2>
<p>Pick your car brand and the symptoms, and our estimator shows the typical repair price for continental, Japanese, Korean and other makes. Customers tell us the final quote often comes in <em>below</em> the estimate.</p>
<ul class="ticks"><li>Diagnostic test: free</li><li>ATF leak repair: from S$300</li><li>Full overhaul: from S$1,800</li></ul>
<a class="btn btn-blue" href="{u("cost-estimator/")}">Open the cost estimator</a>
</div>
<div>{img("diagnostics", "Laptop running a transmission diagnostic test on a BMW")}</div>
</div></section>

<section><div class="wrap">
<div class="sec-head"><h2>What our customers say</h2></div>
<div class="grid g3">{testimonials()}</div>
</div></section>

<section class="alt"><div class="wrap">
<div class="sec-head"><h2>Inside our workshop</h2><p>Dedicated gearbox teardown stations, diagnostic equipment and an air-conditioned lounge where you can watch your car being worked on.</p></div>
<div class="gallery">{gal}</div>
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

{band("Gearbox acting up?", "Call or WhatsApp us for a free quote. If the car can’t move, we’ll tow it in for free.")}
'''
    return page('', 'Gearbox Repair & Auto Transmission Specialist Singapore | Dynamic Motoring',
                'Gearbox repair, overhaul and servicing for all car makes in Woodlands, Singapore. Free diagnostic test, free towing, warranty and direct pricing. Call 6352 8832.',
                body, active='', ld=[faq_ld()])


def services():
    blocks = []
    for i, (sid, t, im, alt, d) in enumerate(SERVICES):
        pic = f'<div>{img(im, alt)}</div>'
        txt = f'<div><h2>{t}</h2><p>{d}</p>{cta_buttons()}</div>'
        blocks.append(f'<section id="{sid}"{" class=\"alt\"" if i % 2 else ""}><div class="wrap split">'
                      f'{txt + pic if i % 2 else pic + txt}</div></section>')
    body = (page_hero('Services', 'Gearbox Repair, Overhaul, Upgrade &amp; Servicing',
                      'Everything we do is about your transmission: diagnosis, repair, overhaul, strengthening upgrades and ATF servicing, for all car makes.')
            + ''.join(blocks)
            + f'<section><div class="wrap"><div class="sec-head"><h2>Signs your gearbox needs a check</h2></div><div class="sym">'
            + ''.join(f'<div class="card"><h3>{e(t)}</h3><p class="muted">{e(d)}</p></div>' for t, d in SYMPTOMS)
            + '</div></div></section>'
            + band('Not sure what’s wrong?', 'The diagnostic test is free. We’ll tell you the fault and the price before any work starts.'))
    ld = [crumbs_ld('Services', 'services/'), {
        '@context': 'https://schema.org', '@type': 'ItemList', 'itemListElement': [
            {'@type': 'ListItem', 'position': i + 1, 'item': {'@type': 'Service', 'name': html.unescape(t), 'description': d,
                                                               'provider': {'@id': f'{ORIGIN}{BASE}#org'}, 'areaServed': 'Singapore',
                                                               'url': f'{ORIGIN}{BASE}services/#{sid}'}}
            for i, (sid, t, im, alt, d) in enumerate(SERVICES)]}]
    return page('services/', 'Gearbox Repair, Overhaul & ATF Servicing Singapore | Dynamic Motoring',
                'Automatic gearbox repair and overhaul, transmission strengthening upgrades, ATF servicing and free towing in Singapore. All car makes. Free diagnostic test.',
                body, active='services/', ld=ld)


def estimator():
    data = json.load(open(os.path.join(HERE, 'source', 'prices.json'), encoding='utf-8'))
    body = page_hero('Cost Estimator', 'Gearbox Repair Cost Estimator',
                     'Choose your car type and brand, tick the repair for each symptom you notice, and see the estimated price. Then send it to us for a firm quote.') + f'''
<section><div class="wrap">
<div class="est">
<div>
<div class="tabs" role="tablist" id="cats"></div>
<label class="f" for="brand">Car brand</label>
<select id="brand"></select>
<h2 style="font-size:1.3rem;margin:24px 0 12px">Symptoms &amp; possible repairs</h2>
<div id="syms"></div>
</div>
<aside class="card total" aria-live="polite">
<div class="muted">Estimated total</div>
<div class="sum" id="sum">S$0</div>
<ul id="picked"><li>Tick a repair to add it.</li></ul>
<div class="btns" style="flex-direction:column">
<a class="btn btn-wa" id="send-wa" href="#" target="_blank" rel="noopener">{ICON["wa"]}Send estimate on WhatsApp</a>
<a class="btn btn-line" id="send-mail" href="#">Email estimate</a>
<a class="btn btn-red" href="tel:{BIZ["tel"]}">{ICON["phone"]}Call {BIZ["tel_disp"]}</a>
</div>
<p class="note" style="margin-top:14px">Estimates are a guide only. The final price is confirmed after the free diagnostic test, and is often lower.</p>
</aside>
</div>
</div></section>
''' + band('Prefer to talk it through?', 'Describe the symptoms and your car model, and we’ll tell you what it’s likely to be.')
    scripts = (f'<script>window.DMTS_PRICES={json.dumps(data["categories"], ensure_ascii=False)};'
               f'window.DMTS_WA="{BIZ["wa"]}";window.DMTS_EMAIL="{BIZ["email"]}";</script>')
    return page('cost-estimator/', 'Gearbox Repair Cost Estimator Singapore | Dynamic Motoring',
                'Estimate your gearbox repair cost in Singapore by car brand and symptom: valve body service, torque converter, mechatronic, ATF leak or full transmission overhaul.',
                body, active='cost-estimator/', ld=[crumbs_ld('Cost Estimator', 'cost-estimator/')], scripts=scripts)


def gallery():
    gal = ''.join(f'<figure>{img(n, a)}<figcaption>{e(a)}</figcaption></figure>' for n, a in GALLERY)
    body = (page_hero('Gallery', 'Our Gearbox Workshop',
                      'A look inside Dynamic Motoring: diagnostic equipment, gearbox teardown benches, transmission jacks and our customer lounge.')
            + f'<section><div class="wrap"><div class="gallery">{gal}</div></div></section>'
            + band('Come and see us', 'Visit our Woodlands HQ or Jalan Lam Huat branch, or let us pick your car up for free.'))
    return page('gallery/', 'Workshop Photos | Dynamic Motoring Gearbox Specialist',
                'Photos of the Dynamic Motoring gearbox workshop in Woodlands, Singapore: diagnostics, gearbox overhaul benches, car lifts and customer lounge.',
                body, active='gallery/', ld=[crumbs_ld('Gallery', 'gallery/')])


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
<li>Warranty after repair for peace of mind</li>
<li>High quality parts and Automatic Transmission Fluid (ATF)</li>
<li>Comfortable waiting lounge with a clear view of your car</li>
</ul>
</div>
</div></section>
<section><div class="wrap"><div class="sec-head"><h2>What our customers say</h2></div><div class="grid g3">{testimonials()}</div></div></section>
''' + band('Talk to a gearbox specialist', 'Call, WhatsApp or drop by either workshop.')
    return page('about/', 'About Dynamic Motoring | Gearbox Specialist Singapore',
                'Dynamic Motoring (DMTS) is a Singapore gearbox and auto transmission specialist with over 15 years of combined experience in gearbox repair and overhaul.',
                body, active='about/', ld=[crumbs_ld('About', 'about/')])


def contact():
    body = page_hero('Contact', 'Contact Dynamic Motoring',
                     'Call, WhatsApp or email us for a free gearbox quote. If your car can’t move, we’ll arrange free towing during office hours.') + f'''
<section><div class="wrap">
<div class="grid g2">
<div class="card">
<h2 style="font-size:1.4rem">Get in touch</h2>
<p><strong>Office:</strong> <a href="tel:{BIZ["tel"]}">{BIZ["tel_disp"]}</a><br>
<strong>After office hours:</strong> <a href="tel:{BIZ["mobile"]}">{BIZ["mobile_disp"]}</a><br>
<strong>Fax:</strong> {BIZ["fax_disp"]}<br>
<strong>Email:</strong> <a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></p>
{HOURS}
<div style="margin-top:18px">{cta_buttons()}</div>
</div>
<form class="card" id="qform">
<h2 style="font-size:1.4rem">Ask for a quote</h2>
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
'''
    return page('contact/', 'Contact | Dynamic Motoring Gearbox Specialist Singapore',
                'Contact Dynamic Motoring for gearbox repair in Singapore. Call 6352 8832, after hours 8430 9665. Workshops at Wave 9 Woodlands and Jalan Lam Huat.',
                body, active='contact/', ld=[crumbs_ld('Contact', 'contact/')])


def write(rel, text):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)
    print('wrote', rel, len(text.encode()), 'bytes')


if __name__ == '__main__':
    write('index.html', home())
    write('services/index.html', services())
    write('cost-estimator/index.html', estimator())
    write('gallery/index.html', gallery())
    write('about/index.html', about())
    write('contact/index.html', contact())
