"""ContiExpert / Volt Autocare site builder (Page One, 3 Nov 2026).
Usage: python3 build.py <out_dir>   (LIVE=False builds the pageonesingapore.com/preview/contiexpert/ copy)
Content: content/services.py (SERVICES, BRANDS), content/articles.py (ARTICLES); pages below.
Facts policy: only facts in BRIEF.md 'Verified'. Anything else goes in CONFIRM (CONFIRM.md is written on each build)."""
import os, sys, json, math, shutil, html, runpy, re, hashlib, subprocess

LIVE = True  # contiexpert.sg is live since 4 Nov 2026 (domain root = preview/contiexpert folder)
DOMAIN = 'https://contiexpert.sg'
BASE = '' if LIVE else '/preview/contiexpert'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'site')
TODAY = '2026-11-07'  # sitemap lastmod: every page re-published 7 Nov SGT (brand-name sweep)
INDEXNOW_KEY = '6f1c2e9a4b7d48c3a05e9d21b8f3c7e4'

BIZ = 'Volt Autocare'
SITE = 'ContiExpert'
LEGAL = 'Volt Autocare Pte. Ltd.'
BRAND = 'ContiExpert by Volt Autocare'  # one public name everywhere (Edwin, 6 Nov 2026); legal name only in footer + privacy + schema legalName
UEN = '202506592N'
ADDR1 = '143 Bukit Timah Road'
ADDR2 = 'Newton Circus, Singapore 229843'
ADDR_NOTE = 'inside the Shell station'
PHONE = '+65 8221 5502'
TEL = '+6582215502'
WA = '6582215502'
EMAIL = 'Newton@voltauto.sg'
LAT, LON = 1.3109645, 103.8421669
MAPS = ('https://www.google.com/maps/place/Volt+Autocare+@Bukit+Timah/@1.3109645,103.8421669,17z/data=!3m1!4b1!4m6!3m5'
        '!1s0x31da19a1ff4674a3:0x2cd1ca1effa4a97b!8m2!3d1.3109645!4d103.8421669!16s%2Fg%2F11x64r1zbq')
DIRECTIONS = 'https://www.google.com/maps/dir/?api=1&destination=Volt+Autocare+%40Bukit+Timah%2C+143+Bukit+Timah+Road%2C+Singapore+229843'
EMBED = 'https://www.google.com/maps?q=Volt+Autocare+%40Bukit+Timah,+143+Bukit+Timah+Road,+Singapore+229843&z=16&output=embed'
RATING = ('5.0', '22', '3 Nov 2026')
SOCIAL = ['https://www.facebook.com/voltautocare/', 'https://www.instagram.com/voltautocare/', 'https://www.tiktok.com/@volt.autocare']

CONFIRM = [
    'Shell station photo in the homepage hero (sent by Edwin): confirm we may use it, or swap for a photo the client takes',
    'Public brand: "ContiExpert by Volt Autocare" (used in this preview), "Volt Autocare" only, or something else? Google lists "Volt Autocare @Bukit Timah".',
    'WhatsApp and call number +65 8221 5502 for every button (the old site WhatsApp buttons used +65 6264 3832, which no other source shows).',
    'Opening hours for Mon-Fri, Saturday, Sunday and public holidays (Google, Sgcarmart, AutoKaki and your own posts all differ). Preview says "WhatsApp to check".',
    'Main focus: European cars, hybrid/EV, or both equally (website says European; Facebook/Instagram say Hybrid & EV specialist).',
    'Which makes and models you service in-house (Mercedes-Benz, BMW, Audi, Volkswagen, Porsche, MINI?) and which jobs you refer out.',
    'Visit process shown on the site: WhatsApp details, inspection, explain + quote, owner approves before work starts. Is that right? Diagnostic fee?',
    'Arrival: where exactly a first-time driver enters the Shell station and where to stop. Any parking while waiting?',
    'Prices you are happy to publish (e.g. servicing package, Standard PPI, aircon coil wash). Old social posts showed $118 servicing, $60 Standard PPI, $168 coil wash: still valid?',
    'Warranty on parts and labour (written terms), if any.',
    'Names, roles and photos of the owner / service adviser / technicians willing to appear, with real experience details.',
    'Real photos: frontage with Shell + Volt signage, workshop bay, team, 3 real repair cases (with customer consent). Logo file in high resolution.',
    'Permission to use your Instagram/TikTok graphics and videos on the site; original MP4 files if possible.',
    'Company details: Volt Autocare Pte. Ltd., UEN 202506592N (from a company-data site). Correct?',
    'Any authorisations or certifications you can show documents for (e.g. the Dongfeng EV service partner mention on Sgcarmart).',
]

c1 = runpy.run_path(os.path.join(HERE, 'content', 'services.py'))
c2 = runpy.run_path(os.path.join(HERE, 'content', 'articles.py'))
SERVICES, BRANDS, ARTICLES = c1['SERVICES'], c1['BRANDS'], c2['ARTICLES']
for p in SERVICES + BRANDS + ARTICLES:
    CONFIRM.extend('[%s] %s' % (p['slug'], x) for x in p.get('confirm', []))

E = html.escape
def u(path): return BASE + path
def ver(name):
    with open(os.path.join(HERE, name), 'rb') as f: return hashlib.sha1(f.read()).hexdigest()[:8]

ICONS = {
 'european-car-servicing': '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/>',
 'car-diagnostics-warning-lights': '<path d="M3 13a9 9 0 0 1 18 0"/><path d="M12 13l4-4"/><circle cx="12" cy="13" r="1.5"/><path d="M5 19h14"/>',
 'car-aircon-repair': '<path d="M12 2v20M4.9 6l14.2 12M19.1 6 4.9 18"/><path d="M9 4l3 2 3-2M9 20l3-2 3 2"/>',
 'brake-suspension-repair': '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3"/><path d="M12 4v2M20 12h-2M12 20v-2M4 12h2"/>',
 'gearbox-transmission-service': '<circle cx="6" cy="6" r="2"/><circle cx="12" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="6" cy="18" r="2"/><circle cx="12" cy="18" r="2"/><path d="M6 8v8M12 8v8M18 8v4H6"/>',
 'hybrid-ev-servicing': '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 'pre-purchase-inspection': '<path d="M9 11l2 2 4-4"/><path d="M5 4h14v16H5z"/><path d="M9 2h6v4H9z"/>',
 'car': '<path d="M5 16h14M3 13l2-5h14l2 5v4h-2M5 17H3v-4"/><circle cx="7.5" cy="17" r="1.8"/><circle cx="16.5" cy="17" r="1.8"/>',
 'pin': '<path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/>',
 'book': '<path d="M4 4h7a3 3 0 0 1 3 3v13a2 2 0 0 0-2-2H4z"/><path d="M20 4h-6a3 3 0 0 0-3 3"/><path d="M20 4v14h-6"/>',
}
def ico(k): return '<span class="ico" aria-hidden="true"><svg viewBox="0 0 24 24">%s</svg></span>' % ICONS.get(k, ICONS['car'])
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.1c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.8s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.6-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>'
CALL_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>'
DIR_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>'
LOGO_SVG = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#fff"/>'
            + ''.join('<rect x="%.1f" y="%.1f" width="6" height="6" transform="rotate(45 %.1f %.1f)" fill="%s"/>' % (x - 3, y - 3, x, y, c) for x, y, c in
                      ((8, 12, '#1e7bff'), (15, 12, '#5aa5ff'), (25, 12, '#5aa5ff'), (32, 12, '#1e7bff'), (11.5, 19, '#1e7bff'), (28.5, 19, '#1e7bff'), (15, 26, '#0b5fd6'), (25, 26, '#0b5fd6'), (20, 32, '#0b5fd6')))
            + '</svg>')

PHOTOS = {}
def img(key, alt, cls='', eager=False, sizes='(max-width:700px) 100vw, 600px'):
    w, h = PHOTOS.get(key, (800, 600))
    return '<img class="%s" src="/assets/photos/%s.webp" width="%d" height="%d" alt="%s"%s decoding="async">' % (cls, key, w, h, E(alt), '' if eager else ' loading="lazy"')
# Real Volt Autocare photos only (their Google listing photos, supplied by Edwin 3 Nov 2026)
SVC_IMG = {'european-car-servicing': ('ce-lexus-bmw', 'Lexus and BMW in for servicing at ContiExpert, Shell Newton'),
           'car-diagnostics-warning-lights': ('ce-battery-test', 'Battery and charging system tester reading on a car at ContiExpert'),
           'car-aircon-repair': ('ce-vellfire-aircon', 'Aircon gauges and R1234yf refrigerant connected to a Toyota Vellfire at ContiExpert'),
           'brake-suspension-repair': ('ce-porsche', 'Porsche 911 on the ramp at ContiExpert'),
           'gearbox-transmission-service': ('ce-audi-amg', 'Audi and Mercedes-AMG with bonnets open in the ContiExpert bays'),
           'hybrid-ev-servicing': ('real-mg4', 'Electric car raised on a lift at ContiExpert'),
           'pre-purchase-inspection': ('ce-cla-golf', 'Mercedes CLA and Volkswagen Golf in the ContiExpert bays'),
           'mercedes-benz': ('ce-sclass-eclass', 'Mercedes S-Class and E-Class at the ContiExpert bays, Shell Newton'),
           'bmw': ('real-bmw', 'BMW with the bonnet open and an aircon service machine at ContiExpert'),
           'audi-volkswagen': ('ce-alternators', 'Old and new alternator during a replacement at ContiExpert')}
SVC_IMG['hybrid-fan'] = ('real-mg4', 'Electric car raised on a lift at ContiExpert')
LOGOS = {'mercedes-benz': ['logo-mercedes'], 'bmw': ['logo-bmw'], 'audi-volkswagen': ['logo-audi', 'logo-vw']}

def wa_link(text):
    import urllib.parse
    return 'https://wa.me/%s?text=%s' % (WA, urllib.parse.quote(text))
def btn_wa(label='WhatsApp us', text='Hi ContiExpert, I would like to ask about my car.', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener" data-cta="whatsapp">%s %s</a>' % (cls, E(wa_link(text)), WA_SVG, E(label))
def btn_call(cls='btn btn-ghost'): return '<a class="%s" href="tel:%s" data-cta="call">%s Call %s</a>' % (cls, TEL, CALL_SVG, PHONE)
def btn_dir(cls='btn btn-ghost'): return '<a class="%s" href="%s" target="_blank" rel="noopener" data-cta="directions">%s Directions</a>' % (cls, DIRECTIONS, DIR_SVG)

def org_ld():
    return {'@context': 'https://schema.org', '@type': 'AutoRepair', '@id': DOMAIN + '/#business', 'name': BRAND,
            'alternateName': ['Volt Autocare @Bukit Timah'], 'legalName': LEGAL, 'url': DOMAIN + '/',
            'telephone': PHONE, 'email': EMAIL, 'image': DOMAIN + '/assets/og.jpg', 'logo': DOMAIN + '/assets/icon-512.png',
            'address': {'@type': 'PostalAddress', 'streetAddress': ADDR1 + ' (inside Shell station)', 'addressLocality': 'Singapore',
                        'postalCode': '229843', 'addressCountry': 'SG'},
            'geo': {'@type': 'GeoCoordinates', 'latitude': LAT, 'longitude': LON}, 'hasMap': MAPS, 'sameAs': SOCIAL,
            'areaServed': {'@type': 'GeoCircle', 'geoMidpoint': {'@type': 'GeoCoordinates', 'latitude': LAT, 'longitude': LON}, 'geoRadius': '10000'}}

def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': DOMAIN + p} for i, (n, p) in enumerate(items)]}
def faq_ld(faqs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in faqs]}

NAV = [('Services', '/services/'), ('Makes', '/brands/mercedes-benz/'), ('Near you', '/areas-we-serve/'), ('Guides', '/article/'), ('FAQs', '/faqs/'), ('Visit us', '/contact-us/')]

def fix_links(s):
    s = re.sub(r'(href|src|poster)="/(?!/)', lambda m: '%s="%s/' % (m.group(1), BASE), s)
    return s

def brand_title(t):
    t = re.sub(r'\s*[|\-]\s*(ContiExpert by Volt Autocare|Volt Autocare|ContiExpert)\s*$', '', t)
    return t + ' | ' + BRAND

def page(path, title, desc, body, lds=(), crumbs=None):
    title = brand_title(title)
    assert len(title) <= 80, (path, title)
    canon = DOMAIN + path
    ld = [org_ld()] + list(lds)
    if crumbs: ld.append(crumbs_ld(crumbs))
    navh = ''.join('<a href="%s"%s>%s</a>' % (p, ' aria-current="page"' if path.startswith(p) and p != '/' else '', n) for n, p in NAV)
    cr = ''
    head = f'''<!doctype html><html lang="en-SG" class="no-js"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}"><meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canon}"><meta property="og:image" content="{DOMAIN}/assets/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{BRAND}, European car servicing at Newton Circus">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#ffffff">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&display=swap">
<link rel="stylesheet" href="/ce.css?v={ver('ce.css')}">
{''.join('<script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld)}
</head><body><a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap"><a class="logo" href="/" aria-label="{BRAND} home">{LOGO_SVG}<span><b>{SITE}</b><small>by Volt Autocare</small></span></a>
<nav class="nav" id="nav" aria-label="Main">{navh}</nav>{btn_wa('WhatsApp', cls='btn btn-wa hide-sm')}
<button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button></div></header>
<main id="main">'''
    foot = f'''</main>
<section class="ctaband"><div class="wrap"><h2>Tell us what your car is doing</h2><p>Model, year and a photo of any warning light.</p>
<div class="btns">{btn_wa('WhatsApp ' + PHONE)}{btn_call()}{btn_dir()}</div></div></section>
<footer class="ftr"><div class="wrap"><div class="cols">
<div><h4>{BRAND}</h4><address class="nap">{ADDR1} ({ADDR_NOTE})<br>{ADDR2}<br><a href="tel:{TEL}" data-cta="call">{PHONE}</a> (call / WhatsApp)<br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
<p>Opening hours: please WhatsApp us to check before you come.</p></div>
<div><h4>Services</h4><ul>{''.join('<li><a href="/services/%s/">%s</a></li>' % (s['slug'], E(s['name'])) for s in SERVICES)}</ul></div>
<div><h4>Makes</h4><ul>{''.join('<li><a href="/brands/%s/">%s</a></li>' % (b['slug'], E(b['name'])) for b in BRANDS)}</ul><h4 style="margin-top:14px">Near you</h4><ul><li><a href="/areas-we-serve/">Drivers within 10 km</a></li><li><a href="/contact-us/">Directions</a></li></ul></div>
<div><h4>About</h4><ul><li><a href="/about/">About us</a></li><li><a href="/article/">Car care guides</a></li><li><a href="/faqs/">FAQs</a></li><li><a href="/privacy/">Privacy</a></li>
<li><a href="{SOCIAL[0]}" rel="noopener" target="_blank">Facebook</a> &middot; <a href="{SOCIAL[1]}" rel="noopener" target="_blank">Instagram</a> &middot; <a href="{SOCIAL[2]}" rel="noopener" target="_blank">TikTok</a></li></ul></div>
</div><div class="legal">&copy; 2026 {LEGAL} (UEN {UEN}). Brand names such as Mercedes-Benz, BMW, Audi and Volkswagen belong to their owners and are used only to describe the cars we work on.</div></div></footer>
<div class="stickycta">{btn_wa('WhatsApp')}<a class="btn btn-volt" href="tel:{TEL}" data-cta="call">{CALL_SVG} Call</a></div>
<script src="/ce.js?v={ver('ce.js')}" defer></script><script src="/wa-tap-counter.js?v={ver('wa-tap-counter.js')}" defer></script>
</body></html>'''
    out = head + body + foot
    out = fix_links(out)
    fp = os.path.join(OUT, path.strip('/'), 'index.html') if path != '/404' else os.path.join(OUT, '404.html')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, 'w', encoding='utf-8') as f: f.write(out)
    if path != '/404': SITEMAP.append(path)
    if path in MODIFIED: MOD[path] = MODIFIED[path]

SITEMAP = []
MODIFIED = {'/services/': '2026-11-05', '/brands/mercedes-benz/': '2026-11-05', '/european-car-service-schedule-singapore/': '2026-11-05',
            '/pre-purchase-car-inspection-singapore-your-ultimate-guide-to-buying-with-confidence/': '2026-11-05', '/dealer-vs-independent-workshop-singapore/': '2026-11-05'}  # true lastmod for pages changed after TODAY
MOD = {}

def crumbs_html(items):
    parts = []
    for i, (n, p) in enumerate(items):
        parts.append(E(n) if i == len(items) - 1 else '<a href="%s">%s</a>' % (p, E(n)))
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % '<span>/</span>'.join(parts)

def faq_html(faqs, h='Questions owners ask'):
    return '<section class="faq"><h2>%s</h2>%s</section>' % (E(h), ''.join(
        '<details><summary>%s</summary><p>%s</p></details>' % (E(f['q']), E(f['a'])) for f in faqs))

def card(href, icon, title, text, more='More details'):
    ph = SVC_IMG.get(icon)
    top = '<span class="cimg">%s</span>' % img(ph[0], ph[1]) if ph else ico(icon)
    return '<a class="card%s" href="%s" data-rv>%s<h3>%s</h3><p>%s</p><span class="more">%s &rarr;</span></a>' % (' pcard' if ph else '', href, top, E(title), E(text), more)

URLNAME = {}
def build_urlnames():
    URLNAME['/'] = 'Home'; URLNAME['/services/'] = 'All services'; URLNAME['/areas-we-serve/'] = 'Drivers within 10 km of Newton'
    URLNAME['/contact-us/'] = 'Visit the workshop'; URLNAME['/faqs/'] = 'FAQs'; URLNAME['/article/'] = 'Car care guides'
    for s in SERVICES: URLNAME['/services/%s/' % s['slug']] = s['name']
    for b in BRANDS: URLNAME['/brands/%s/' % b['slug']] = b['name']
    for a in ARTICLES: URLNAME['/%s/' % a['slug']] = a['h1']

def aside(extra=''):
    return f'''<aside class="aside"><div class="boxcta"><h3>Ask about your car</h3><p>WhatsApp your make, model, year and the problem. We reply with the next step.</p>
{btn_wa('WhatsApp ' + PHONE)}<a class="btn btn-ghost" href="{DIRECTIONS}" target="_blank" rel="noopener" data-cta="directions">{DIR_SVG} Directions</a></div>
<div class="card"><h3 style="margin-top:0">Where we are</h3><p>{ADDR1}, {ADDR_NOTE}, {ADDR2}.</p><p><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> {RATING[0]} from {RATING[1]} Google reviews <small>(checked {RATING[2]})</small><br><a href="{MAPS}" target="_blank" rel="noopener" data-cta="maps">See reviews on Google</a></p></div>{extra}</aside>'''

def related_html(urls):
    items = [x for x in urls if x in URLNAME]
    if not items: return ''
    return '<h2>Related</h2><div class="chips">%s</div>' % ''.join('<a class="chip" href="%s">%s</a>' % (x, E(URLNAME[x])) for x in items)

def detail_page(kind, p):
    if kind == 'service':
        path = '/services/%s/' % p['slug']; cr = [('Home', '/'), ('Services', '/services/'), (p['name'], path)]
    elif kind == 'brand':
        path = '/brands/%s/' % p['slug']; cr = [('Home', '/'), ('Makes', '/services/'), (p['name'], path)]
    else:
        path = '/%s/' % p['slug']; cr = [('Home', '/'), ('Guides', '/article/'), (p['h1'], path)]
    secs = ''.join('<section data-rv><h2>%s</h2>%s</section>' % (E(s['h2']), s['html'].replace('<table', '<div class="tablewrap"><table').replace('</table>', '</table></div>')) for s in p['sections'])
    meta = ''
    lds = [faq_ld(p['faqs'])]
    if kind == 'article':
        meta = '<p class="meta">Updated %s &middot; %s min read &middot; By the %s team, Newton Circus</p>' % (p.get('updated', '3 Nov 2026'), p.get('minutes', 6), BRAND)
        lds.append({'@context': 'https://schema.org', '@type': 'Article', 'headline': p['h1'], 'datePublished': p['date'], 'dateModified': p.get('modified', p['date']),
                    'author': {'@type': 'Organization', 'name': BRAND, 'url': DOMAIN + '/'}, 'publisher': {'@id': DOMAIN + '/#business'},
                    'image': DOMAIN + '/assets/og.jpg', 'mainEntityOfPage': DOMAIN + path})
        own = p.get('service')
        extra = ('<div class="card"><h3 style="margin-top:0">The service behind this guide</h3><p><a href="%s">%s</a></p></div>' % (own, E(URLNAME.get(own, 'Our services')))) if own else ''
    else:
        lds.append({'@context': 'https://schema.org', '@type': 'Service', 'name': p['h1'], 'serviceType': p['name'], 'provider': {'@id': DOMAIN + '/#business'},
                    'areaServed': 'Singapore', 'url': DOMAIN + path})
        extra = ''
    key = p['slug'] if kind != 'article' else (p.get('service') or '').strip('/').split('/')[-1]
    ph = SVC_IMG.get(key, ('real-front', 'ContiExpert by Volt Autocare workshop bays at the Shell station, Newton'))
    logos = ''.join(img(l, l.replace('logo-', '').upper() + ' logo', 'blogo') for l in LOGOS.get(p['slug'], [])) if kind == 'brand' else ''
    body = f'''<div class="phead ph2"><div class="wrap"><div>{crumbs_html(cr)}{('<div class="blogos">%s</div>' % logos) if logos else ''}<h1>{E(p['h1'])}</h1>{meta}<p class="answer">{E(p['answer'])}</p>
<div class="btns">{btn_wa('WhatsApp us about this', 'Hi ContiExpert, I am asking about: ' + p['name'] if 'name' in p else 'Hi ContiExpert, I read your guide: ' + p['h1'])}{btn_dir()}</div></div><div class="phimg">{img(ph[0], ph[1], eager=True)}</div></div></div>
<div class="sec"><div class="wrap layout"><article class="prose">{secs}
<div data-rv>{faq_html(p['faqs'])}</div><div data-rv>{related_html(p.get('related', []))}</div></article>{aside(extra)}</div></div>'''
    page(path, p['title'], p['desc'], body, lds, cr)

# ---------- 10 km catchment ----------
AREAS = [  # name, lat, lon, group  (centroids are approximate; distances shown as rounded straight-line km)
    ('Newton', 1.3138, 103.8380, 'core'), ('Novena', 1.3204, 103.8438, 'N'), ('Orchard', 1.3040, 103.8318, 'S'),
    ('Tanglin', 1.3065, 103.8185, 'W'), ('River Valley', 1.2940, 103.8350, 'S'), ('Farrer Park', 1.3124, 103.8543, 'E'),
    ('Balestier', 1.3250, 103.8500, 'N'), ('Toa Payoh', 1.3343, 103.8563, 'N'), ('Bukit Timah', 1.3310, 103.7970, 'W'),
    ('Holland Village', 1.3112, 103.7958, 'W'), ('Bugis', 1.3008, 103.8559, 'S'), ('Tiong Bahru', 1.2860, 103.8270, 'S'),
    ('Kallang', 1.3115, 103.8710, 'E'), ('Raffles Place', 1.2840, 103.8514, 'S'), ('Thomson', 1.3540, 103.8330, 'N'),
    ('Bishan', 1.3508, 103.8485, 'N'), ('Queenstown', 1.2942, 103.8060, 'W'), ('Geylang', 1.3180, 103.8870, 'E'),
    ('Serangoon', 1.3498, 103.8737, 'E'), ('Ang Mo Kio', 1.3700, 103.8496, 'N'), ('Beauty World', 1.3412, 103.7758, 'W'),
    ('Marine Parade', 1.3020, 103.9050, 'E'), ('HarbourFront', 1.2653, 103.8220, 'S'), ('Clementi', 1.3151, 103.7650, 'W'),
]
def km(lat, lon):
    R = 6371.0; p1, p2 = math.radians(LAT), math.radians(lat); dp = p2 - p1; dl = math.radians(lon - LON)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))
AREAS = sorted([(n, la, lo, g, km(la, lo)) for n, la, lo, g in AREAS], key=lambda x: x[4])
AREAS = [a for a in AREAS if a[4] <= 10]

LBL = {'Tanglin': ('end', -7, 4), 'Orchard': ('end', -7, 14), 'Farrer Park': ('middle', 0, -9), 'Kallang': ('start', 7, 10), 'Tiong Bahru': ('end', -7, 4), 'Thomson': ('end', -7, 4), 'River Valley': ('start', 7, 8), 'Bugis': ('start', 7, 2), 'Balestier': ('start', 7, -2), 'Novena': ('start', 7, 8), 'Bishan': ('start', 7, 4), 'Raffles Place': ('start', 7, 6)}
def catchment_svg(size=600, labels=True, cls=''):
    """Premium light catchment map (v9, 3 Nov 2026): labels placed with simple collision avoidance."""
    c = size / 2; pxkm = (size / 2 - 22) / 10.0
    fs = max(11, size // 46); FONT = 'Manrope,system-ui,sans-serif'
    def xy(la, lo): return (c + (lo - LON) * 111.32 * math.cos(math.radians(LAT)) * pxkm, c - (la - LAT) * 110.57 * pxkm)
    s = ['<svg viewBox="0 0 %d %d" role="img" aria-label="Map of the 10 km circle around the Newton Circus workshop with nearby neighbourhoods" class="%s">' % (size, size, cls)]
    s.append('<rect width="%d" height="%d" fill="#f4f4f1"/>' % (size, size))
    for r, col in ((10, '#ffffff'), (6, '#f7f7f5'), (3, '#ececea')):
        s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="#b9bab6" stroke-width="1.2" stroke-dasharray="4 5"/>' % (c, c, r * pxkm, col))
        s.append('<text x="%.1f" y="%.1f" fill="#6b6d70" font-size="%d" font-family="%s" text-anchor="middle">%d km</text>' % (c, c - r * pxkm + 16, fs, FONT, r))
    wf = max(12, size // 40)
    boxes = [(c - 13, c - 13, c + 13, c + 13)]  # the pin
    for r in (10, 6, 3):  # ring labels
        boxes.append((c - 22, c - r * pxkm + 4, c + 22, c - r * pxkm + 18))
    pts = [(n, ) + xy(la, lo) for n, la, lo, g, d in AREAS if n != 'Newton']
    for n, x, y in pts: boxes.append((x - 6, y - 6, x + 6, y + 6))
    def hit(bx): return any(not (bx[2] < o[0] or bx[0] > o[2] or bx[3] < o[1] or bx[1] > o[3]) for o in boxes)
    ww = 8 * wf * 0.66  # "Workshop" label: pick a free spot around the pin
    wpos = (c, c + 16 + wf)
    for tx, ty in ((c, c + 16 + wf), (c, c - 16), (c - 14 - ww / 2, c + wf * 0.35), (c + 14 + ww / 2, c + wf * 0.35), (c, c + 40 + wf), (c, c - 40)):
        bx = (tx - ww / 2, ty - wf, tx + ww / 2, ty + 3)
        if not hit(bx): wpos = (tx, ty); break
    boxes.append((wpos[0] - ww / 2, wpos[1] - wf, wpos[0] + ww / 2, wpos[1] + 3))
    for n, x, y in pts:
        s.append('<circle cx="%.1f" cy="%.1f" r="4" fill="#111316"/>' % (x, y))
        if not (labels is True or (labels and n in labels)): continue
        w = len(n) * fs * 0.62
        cands = [('start', x + 7, y + fs * 0.35), ('end', x - 7, y + fs * 0.35), ('middle', x, y - 8), ('middle', x, y + fs + 6),
                 ('start', x + 7, y - 6), ('end', x - 7, y - 6), ('start', x + 7, y + fs + 2), ('end', x - 7, y + fs + 2)]
        best = None
        for anc, tx, ty in cands:
            x0 = tx if anc == 'start' else tx - w if anc == 'end' else tx - w / 2
            bx = (x0, ty - fs, x0 + w, ty + 2)
            if bx[0] < 4 or bx[2] > size - 4: continue
            if not hit(bx): best = (anc, tx, ty, bx); break
        if not best:
            anc, tx, ty = cands[0]; best = (anc, tx, ty, (tx, ty - fs, tx + w, ty + 2))
        boxes.append(best[3])
        s.append('<text x="%.1f" y="%.1f" fill="#2b2d31" font-size="%d" font-weight="500" font-family="%s" text-anchor="%s">%s</text>' % (best[1], best[2], fs, FONT, best[0], E(n)))
    s.append('<circle class="pulse" cx="%.1f" cy="%.1f" r="10" fill="#111316" opacity=".25"/>' % (c, c))
    s.append('<circle cx="%.1f" cy="%.1f" r="8" fill="#111316" stroke="#fff" stroke-width="3"/>' % (c, c))
    s.append('<text x="%.1f" y="%.1f" fill="#111316" font-weight="800" font-size="%d" font-family="%s" text-anchor="middle">Workshop</text>' % (wpos[0], wpos[1], wf, FONT))
    s.append('</svg>')
    return ''.join(s)

GROUP = {
 'N': ('From the north: Novena, Balestier, Toa Payoh, Thomson, Bishan, Ang Mo Kio',
       'Most drivers from these estates come down the CTE or along Thomson Road, both of which lead towards Newton. Novena and Balestier are close enough that a drop-off and a short ride home or to the office is practical.'),
 'W': ('From the west: Tanglin, Bukit Timah, Holland Village, Beauty World, Queenstown, Clementi',
       'The Bukit Timah Road and Dunearn Road corridor runs straight towards Newton Circus, and the PIE is the other common way in. Owners along Bukit Timah often pass the workshop on the way into town.'),
 'S': ('From the south: Orchard, River Valley, Bugis, Tiong Bahru, Raffles Place, HarbourFront',
       'From Orchard, Scotts Road leads up to Newton Circus. From the city and River Valley, Clemenceau Avenue and the CTE are the usual ways north. Many owners in this band drop the car before work and collect it after.'),
 'E': ('From the east: Farrer Park, Kallang, Geylang, Serangoon, Marine Parade',
       'Drivers from the east usually take the PIE or CTE towards Bukit Timah Road. Farrer Park and Kallang are only a few kilometres away, so a visit fits into an ordinary weekday.'),
}

# Popular jobs with prices the business itself published (Instagram/TikTok/Facebook, Nov-Dec 2025). PREVIEW ONLY until the client confirms.
POPULAR = [
    ('Servicing packages', 'from $118', 'Oil and filter servicing packages for continental cars, with add-ons at the same visit.', '/services/european-car-servicing/', 'european-car-servicing'),
    ('Aircon cooling-coil wash', 'from $168', 'For weak cooling, warm air or a musty smell. The coil is cleaned, not just the gas topped up.', '/services/car-aircon-repair/', 'car-aircon-repair'),
    ('Standard pre-purchase inspection', '$60', 'A condition and safety check before you pay for a used car.', '/services/pre-purchase-inspection/', 'pre-purchase-inspection'),
    ('Hybrid and EV battery health check', 'Ask us', 'State-of-health reading for hybrid and EV batteries, with a hybrid or EV pre-purchase inspection.', '/services/hybrid-ev-servicing/', 'hybrid-ev-servicing'),
    ('Hybrid battery fan cleaning', 'Ask us', 'A clogged battery cooling fan makes a hybrid battery run hot. We clean it and check the airflow.', '/services/hybrid-ev-servicing/', 'hybrid-fan'),
    ('Gearbox oil (ATF) change', 'Ask us', 'Fresh transmission fluid for smoother shifts, timed to your gearbox and how you drive.', '/services/gearbox-transmission-service/', 'gearbox-transmission-service'),
]
CONFIRM.append('Prices on the homepage come from your own posts (Dec 2025 servicing packages from $118, TikTok aircon coil wash $168, Standard PPI $60). Are they still current, and what do the packages include? Prices for hybrid battery health check, battery fan cleaning and ATF change?')
CONFIRM.append('Is Volt Autocare part of the Volt Auto group (Dongfeng distributor)? If yes, may we say so?')

IG = [('ig-2025-12-15b', 'Car A/C blowing warm air? Common causes, a ContiExpert by Volt Autocare tip'), ('ig-2025-12-23b', 'Why brake pads wear out faster than you think'),
      ('ig-2025-12-23a', 'Top 4 causes of bad fuel efficiency'), ('ig-2025-11-19', 'Tyre pressure and engine efficiency'),
      ('ig-2025-12-15a', 'Service checklist for every car owner'), ('ig-2025-11-26', 'Prepping your EV for long drives')]
# Google reviews of Volt Autocare @Bukit Timah, pulled 3 Nov 2026 (short verbatim excerpts, name as shown on Google).
REVIEWS = [
    ('Ang Keng Yeow', 'Jul 2026', 'Aircon', 'They only changed my compressor saving me a lot of money.'),
    ('Ricky Shi', 'Oct 2026', 'Steering and suspension', 'He was honest, patient and genuinely helpful.'),
    ('Jeff C', 'Mar 2026', 'Aircon compressor', 'Diagnosed and explained the issue clearly.'),
    ('Cal Low', 'Mar 2026', 'Wheel bearing', 'Helped complete the job in under 2 hours.'),
    ('Yi Yi', 'Sep 2026', 'Battery', 'Friendly, efficient and professional.'),
    ('Adam Lim', 'Sep 2026', 'Pre-purchase inspection', 'The report was comprehensive and was generated on the same day.'),
    ('Ng Tim Peng', 'Jun 2025', 'Repairs', 'Advised not to change certain parts.'),
    ('Ken S', 'Sep 2025', 'Repairs', 'Provided a cost effective solution to fix the issue.'),
]
CONFIRM.append('Reviews: the homepage quotes short excerpts from your Google reviews (names as shown on Google). OK to show them? Customers name "Newt" and "An" - may we name them on the About page, with their roles?')
CONFIRM.append('Bring your own parts: a Google review says you fit customer-supplied parts for labour only. Is that offered for all jobs? Any warranty difference?')
CONFIRM.append('Car batteries: reviews mention battery replacement. Which brands do you stock, and from what price? Walk-in or appointment?')

# "What do you need today?" - problems drivers actually come in with (from reviews + their posts)
NEEDS = [
    ('car-diagnostics-warning-lights', 'A warning light is on', 'Send us a photo. We read the fault codes and tell you if it is safe to drive.', '/services/car-diagnostics-warning-lights/', ''),
    ('car-aircon-repair', 'Aircon blowing warm', 'We find the cause first, so you do not pay for a coil you do not need.', '/services/car-aircon-repair/', 'coil wash from $168'),
    ('battery', 'Battery flat or weak', 'Battery test and replacement, often while you fill up next door.', '/contact-us/', ''),
    ('pre-purchase-inspection', 'Buying a used car', 'A thorough check with a written report, usually the same day.', '/services/pre-purchase-inspection/', 'from $60'),
    ('european-car-servicing', 'Service is due', 'Oil, filters and checks for continental and everyday cars.', '/services/european-car-servicing/', 'from $118'),
    ('brake-suspension-repair', 'Noise when braking or on bumps', 'Brake pads, discs, bearings and suspension, explained before we start.', '/services/brake-suspension-repair/', ''),
    ('hybrid-ev-servicing', 'Hybrid or EV check', 'Battery health reading and hybrid battery fan cleaning.', '/services/hybrid-ev-servicing/', ''),
    ('parts', 'Have your own parts?', 'Customers bring their own parts and we fit them for labour only.', '/faqs/', ''),
]
ICONS['battery'] = '<rect x="3" y="7" width="16" height="11" rx="2"/><path d="M19 11h2v3h-2M7 12h4M9 10v4M14 12h2"/>'
ICONS['parts'] = '<path d="M21 8 12 3 3 8v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8"/>'
ICONS['quote'] = '<path d="M7 7h4v4c0 3-2 5-4 6M15 7h4v4c0 3-2 5-4 6"/>'

def home():
    tiles = ''.join('<a class="svl" href="/services/%s/" data-rv><small>0%d</small><b>%s</b><span>&rarr;</span></a>' % (
        s['slug'], i + 1, E(s['name'])) for i, s in enumerate(SERVICES))
    revs = ''.join('<li><figure class="rq"><blockquote>&ldquo;%s&rdquo;</blockquote><figcaption><b>%s</b><span>%s &middot; %s</span></figcaption></figure></li>' % (E(q), E(n), E(job), E(d)) for n, d, job, q in REVIEWS)
    prices = ''.join('<a class="prow" href="%s"><span>%s</span><b>%s</b></a>' % (h, E(t), E(p)) for t, p, x, h, i in POPULAR)
    _unused = ''.join('<a class="acard2" href="/%s/" data-rv><small>%s</small><h3>%s</h3><span>Read &rarr;</span></a>'
                        % (a['slug'], E(a.get('brand') or 'Car care'), E(a['h1'])) for a in ARTICLES[:3])
    logos = ''.join(img(l, l.replace('logo-', '').upper() + ' logo', 'blogo') for l in ['logo-mercedes', 'logo-bmw', 'logo-audi', 'logo-vw', 'logo-porsche', 'logo-mini'])
    faqs = [
        {'q': 'Will you replace parts I do not need?', 'a': 'No. We show you what we found and agree the price before any work.'},
        {'q': 'Which cars do you work on?', 'a': 'Mercedes-Benz, BMW, Audi and VW mainly, plus hybrids, EVs, Japanese and Korean cars.'},
        {'q': 'Can I bring my own parts?', 'a': 'Yes. Send us the part details first and we fit it for labour only.'},
    ]
    body = f'''<section class="lux-hero"><div class="lux-img">{img('real-bay', 'Mercedes-Benz and BMW in the ContiExpert by Volt Autocare bays, with an aircon service machine', eager=True, sizes='(max-width:820px) 100vw, 50vw')}
<figure class="pip"><video class="pipv" src="/assets/video/find-us-sm.mp4" poster="/assets/photos/poster-find-us.webp" muted loop playsinline autoplay preload="metadata" aria-label="Video: walking from the Shell station to the ContiExpert by Volt Autocare bays"></video>
<button class="vsnd" type="button">&#9654; Sound</button><figcaption>Find us &middot; 0:31</figcaption></figure>
<a class="shellpip" href="{MAPS}" target="_blank" rel="noopener" data-cta="maps">{img('real-shell', 'The Shell station at Newton Circus, 143 Bukit Timah Road, where ContiExpert by Volt Autocare is', sizes='240px')}<span>Look for this Shell &middot; Newton Circus</span></a></div>
<div class="wrap lux-copy"><span class="eyebrow">ContiExpert by Volt Autocare &middot; Newton</span>
<h1>Continental car specialists<span>at Newton Circus</span></h1>
<p>Mercedes, BMW, Audi, VW, hybrids and EVs. We fix only what your car needs.</p>
<div class="btns">{btn_wa('Book on WhatsApp', cls='btn btn-dark')}<a class="btn btn-outline" href="tel:{TEL}" data-cta="call">Call {PHONE}</a></div></div></section>

<section class="facts"><div class="wrap"><a href="{MAPS}" target="_blank" rel="noopener" data-cta="maps"><b>{RATING[0]} &#9733;</b><span>{RATING[1]} Google reviews</span></a>
<div><b>Inside Shell</b><span>143 Bukit Timah Road</span></div><div><b>Clear prices</b><span>before we start</span></div><div><b>Own parts</b><span>welcome</span></div></div></section>

<section class="sec5"><div class="wrap"><div class="head5"><span class="eyebrow">Continental</span><h2>The makes we know</h2></div>
<div class="logorow">{logos}</div>
<div class="chips5">{''.join('<a href="/brands/%s/">%s &rarr;</a>' % (b['slug'], E(b['name'])) for b in BRANDS)}</div></div></section>

<section class="sec5 grey svc5"><div class="wrap"><div class="head5"><span class="eyebrow">Services</span><h2>What we do</h2><a class="lnk" href="/services/">All services &rarr;</a></div>
<div class="svlist">{tiles}</div></div></section>

<section class="sec5"><div class="wrap split"><div class="splitimg" data-rv>{img('real-front', 'ContiExpert by Volt Autocare workshop bays under the awning at the Shell station, Newton', sizes='(max-width:820px) 100vw, 560px')}</div>
<div data-rv><span class="eyebrow">Our approach</span><h2>Honest advice first</h2>
<ol class="steps5"><li><b>We find the real fault</b>No parts you don't need.</li>
<li><b>We explain it plainly</b>Price agreed before we start.</li>
<li><b>We work quickly</b>Many jobs done the same visit.</li></ol></div></div></section>

<section class="sec5 grey revs"><div class="wrap"><div class="head5"><span class="eyebrow">{RATING[0]} &#9733; from {RATING[1]} Google reviews</span><h2>In our customers&rsquo; words</h2><a class="lnk" href="{MAPS}" target="_blank" rel="noopener" data-cta="maps">All reviews on Google &rarr;</a></div>
<div class="carwrap"><div class="marq"><ul class="track">{revs}</ul></div><div class="carbtns"><button class="cprev" aria-label="Previous">&larr;</button><button class="cnext" aria-label="Next">&rarr;</button></div></div></div></section>

<section class="sec5"><div class="wrap split rev"><div data-rv><span class="eyebrow">Starting prices</span><h2>Popular jobs</h2>
<div class="prices">{prices}</div><p class="note">Confirm for your model on WhatsApp.</p></div>
<div data-rv><span class="eyebrow">Hybrid &amp; EV</span><h2>Buying a used hybrid or EV?</h2><p>We check the battery&rsquo;s health with the Autel MS909EV before you pay, and clean hybrid battery fans.</p>
<figure class="vcard"><video src="/assets/video/ev-ppi-sm.mp4" poster="/assets/photos/poster-ev-ppi.webp" controls playsinline preload="none" aria-label="Video: ContiExpert by Volt Autocare EV and hybrid pre-purchase inspection"></video><figcaption>Our EV/hybrid PPI &middot; 1 min</figcaption></figure>
<p><a class="lnk" href="/services/hybrid-ev-servicing/">Hybrid and EV care &rarr;</a></p></div></div></section>

<section class="sec5 grey"><div class="wrap split"><div data-rv><span class="eyebrow">Visit us</span><h2>Inside Shell, Newton Circus</h2>
<address class="nap">{ADDR1}, {ADDR_NOTE}<br>{ADDR2}</address>
<p>Fill up while we check your car. <a href="/areas-we-serve/">Getting here &rarr;</a></p>
<div class="btns">{btn_dir('btn btn-dark')}{btn_wa('WhatsApp ' + PHONE, cls='btn btn-outline')}</div></div>
<div class="mapbox" data-rv><iframe src="{EMBED}" title="Map of {BRAND} at 143 Bukit Timah Road" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div></section>

<section class="sec5 faq5"><div class="wrap">{faq_html(faqs, 'Quick answers')}</div></section>'''
    page('/', 'Continental Car Specialist, Newton Circus',
         'Mercedes-Benz, BMW, Audi and VW servicing and repairs, plus hybrid and EV checks, inside Shell at 143 Bukit Timah Road, Newton. 5.0 from 22 Google reviews.',
         body, [faq_ld(faqs)])

def services_hub():
    cr = [('Home', '/'), ('Services', '/services/')]
    body = f'''<div class="phead"><div class="wrap">{crumbs_html(cr)}<h1>Car servicing and repair services</h1>
<p class="answer">{BRAND} services and repairs European cars, and checks hybrids and EVs, at our workshop inside the Shell station at 143 Bukit Timah Road, Newton Circus. Pick the service closest to your problem, or WhatsApp us what the car is doing and we will point you to the right one.</p></div></div>
<div class="sec"><div class="wrap"><div class="grid g3">{''.join(card('/services/%s/' % s['slug'], s['slug'], s['name'], s['card']) for s in SERVICES)}</div>
<h2>By make</h2><div class="grid g3">{''.join(card('/brands/%s/' % b['slug'], b['slug'], b['name'], b['card']) for b in BRANDS)}</div>
<section data-rv><h2>How do you choose a car repair workshop in Singapore?</h2>
<p>Repair cost depends on the model and what the inspection finds, so we give a quote after we look at the car and you approve it before work starts. Ask any workshop to explain the findings and separate urgent items from those that can wait. Our <a href="/dealer-vs-independent-workshop-singapore/">dealer vs independent workshop guide</a> lists the questions to ask.</p>
<p>For common issues, start with the guides on the <a href="/bmw-check-engine-light-singapore/">BMW check engine light</a>, <a href="/mercedes-engine-overheating-singapore/">Mercedes overheating</a> and <a href="/audi-aircon-not-cold-repair-singapore/">Audi aircon problems</a>, and use the <a href="/european-car-service-schedule-singapore/">car maintenance checklist</a> to keep servicing on schedule. Buying a used car? Read about the <a href="/pre-purchase-car-inspection-singapore-your-ultimate-guide-to-buying-with-confidence/">pre-purchase car inspection</a> first.</p></section></div></div>'''
    page('/services/', 'Car Repair Singapore: European Car Services | ContiExpert by Volt Autocare',
         'Car repair in Singapore for European cars: servicing, diagnostics, aircon, brakes, suspension, gearbox, hybrid and EV checks. Quote agreed before work.', body, (), cr)

def areas_page():
    cr = [('Home', '/'), ('Drivers within 10 km', '/areas-we-serve/')]
    rows = ''.join('<tr><td>%s</td><td>about %s km</td><td>%s</td></tr>' % (E(n), ('%.0f' % d) if d >= 1.5 else '1', {'core': 'Next door', 'N': 'North', 'S': 'South', 'E': 'East', 'W': 'West'}[g]) for n, la, lo, g, d in AREAS)
    groups = ''.join('<section data-rv><h2>%s</h2><p>%s</p><p>%s</p></section>' % (E(t), E(x),
              'Straight-line distance: ' + E(', '.join('%s about %s km' % (a[0], ('%.0f' % a[4]) if a[4] >= 1.5 else '1') for a in AREAS if a[3] == k)) + '.') for k, (t, x) in GROUP.items())
    faqs = [
        {'q': 'Is 10 km the driving distance?', 'a': 'No. The 10 km circle on this page is a straight line from the workshop. Driving distance and time depend on your route and the traffic, so use the Directions button to see your own route in Google Maps.'},
        {'q': 'Do you have other branches?', 'a': 'No. We have one workshop, inside the Shell station at 143 Bukit Timah Road, Newton Circus. The neighbourhoods on this page are where many of our customers drive in from, not separate outlets.'},
        {'q': 'Can I come from outside the 10 km circle?', 'a': 'Yes. The circle is simply where the workshop is most convenient. Owners from anywhere in Singapore are welcome; WhatsApp us first so we can plan the time you arrive.'},
        {'q': 'What is close by while my car is being checked?', 'a': 'Newton MRT station, on the North-South and Downtown lines, and Newton Food Centre are both close to Newton Circus, and Orchard and Novena are a short ride away.'},
    ]
    body = f'''<div class="phead"><div class="wrap">{crumbs_html(cr)}<h1>Car workshop for drivers within 10 km of Newton</h1>
<p class="answer">{BRAND} has one workshop, inside the Shell station at 143 Bukit Timah Road, Newton Circus. Because Newton is near the middle of Singapore, Novena, Orchard, Toa Payoh, Bukit Timah, Holland Village, Bishan, Kallang and the city are all within about 10 km in a straight line.</p>
<div class="btns">{btn_wa('WhatsApp ' + PHONE)}{btn_dir()}</div></div></div>
<div class="sec"><div class="wrap layout"><article class="prose">
<div class="catch" data-rv>{catchment_svg(640)}</div><p><small>Rings at 3, 6 and 10 km in a straight line from the workshop pin. Neighbourhood dots are approximate centres.</small></p>
<section data-rv><h2>Which neighbourhoods are within 10 km?</h2><div class="tablewrap"><table class="area-tbl"><thead><tr><th>Neighbourhood</th><th>Straight line</th><th>Direction</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>Larger districts stretch across the rings, so parts of Ang Mo Kio, Serangoon or Clementi may be just inside or just outside 10 km.</p></section>
{groups}
<section data-rv><h2>What is near the workshop while you wait?</h2><p>Newton Circus is a busy junction where Bukit Timah Road, Dunearn Road, Scotts Road, Newton Road and Clemenceau Avenue North meet. Newton MRT station (North-South and Downtown lines) and Newton Food Centre are both close by, and Orchard Road and Novena are a short ride away. If the job will take longer, many owners drop the car and head to work or home, and we message them when it is ready.</p></section>
<section data-rv><h2>How do I find the entrance?</h2><p>Set your navigation to <a href="{MAPS}" target="_blank" rel="noopener" data-cta="maps">Volt Autocare @Bukit Timah on Google Maps</a> or to 143 Bukit Timah Road, Singapore 229843. The workshop is inside the Shell station. If it is your first visit, WhatsApp us when you are a few minutes away and we will guide you in.</p></section>
<div data-rv>{faq_html(faqs)}</div>
<div data-rv>{related_html(['/contact-us/', '/services/european-car-servicing/', '/services/car-diagnostics-warning-lights/', '/services/pre-purchase-inspection/'])}</div>
</article>{aside()}</div></div>'''
    page('/areas-we-serve/', 'Car Workshop Near Newton, Novena & Orchard | ContiExpert by Volt Autocare',
         'One workshop at Newton Circus, inside Shell on Bukit Timah Road, within 10 km of Novena, Orchard, Toa Payoh, Bukit Timah, Bishan and the city.',
         body, [faq_ld(faqs)], cr)

def contact_page():
    cr = [('Home', '/'), ('Visit us', '/contact-us/')]
    body = f'''<div class="phead"><div class="wrap">{crumbs_html(cr)}<h1>Visit {BRAND} at Newton Circus</h1>
<p class="answer">Our workshop is inside the Shell station at 143 Bukit Timah Road, Newton Circus, Singapore 229843. WhatsApp or call {PHONE} before you come so we can check the car in quickly. Tap Directions for Google Maps from where you are.</p>
<div class="btns">{btn_wa('WhatsApp ' + PHONE)}{btn_call()}{btn_dir()}</div></div></div>
<div class="sec"><div class="wrap grid g2" style="align-items:start">
<div class="prose"><h2 style="margin-top:0">Contact details</h2>
<address class="nap"><strong>{BRAND}</strong> (Google Maps: Volt Autocare @Bukit Timah)<br>{ADDR1}, {ADDR_NOTE}<br>{ADDR2}<br>
Call / WhatsApp: <a href="tel:{TEL}" data-cta="call">{PHONE}</a><br>Email: <a href="mailto:{EMAIL}">{EMAIL}</a></address>
<h2>Opening hours</h2><p>Please WhatsApp us to check before you come, especially on weekends and public holidays.</p>
<h2>What to send us on WhatsApp</h2><ol><li>Make, model and year of the car</li><li>Mileage, roughly</li><li>What you noticed and when it happens (cold start, braking, at speed, with aircon on)</li><li>A photo of any warning light on the dashboard</li></ol>
<p>Please do not send your NRIC or full vehicle documents. We only need what helps us understand the car.</p>
<h2>Finding the entrance</h2><p>The workshop is inside the Shell station on Bukit Timah Road at Newton Circus. On your first visit, WhatsApp us when you are a few minutes away and we will guide you in.</p>
<p><a href="/areas-we-serve/">Coming from Novena, Orchard, Toa Payoh or Bukit Timah? See getting here from your area &rarr;</a></p>
<p><span class="stars">&#9733;&#9733;&#9733;&#9733;&#9733;</span> {RATING[0]} from {RATING[1]} Google reviews (checked {RATING[2]}). <a href="{MAPS}" target="_blank" rel="noopener" data-cta="maps">Read the reviews on Google</a></p>
<p>Follow us: <a href="{SOCIAL[0]}" target="_blank" rel="noopener">Facebook</a> &middot; <a href="{SOCIAL[1]}" target="_blank" rel="noopener">Instagram</a> &middot; <a href="{SOCIAL[2]}" target="_blank" rel="noopener">TikTok</a></p></div>
<div><div class="mapbox"><iframe src="{EMBED}" title="Map of {BRAND} at 143 Bukit Timah Road" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p style="margin-top:12px">{btn_dir('btn btn-line')}</p></div></div></div>'''
    page('/contact-us/', 'Contact & Directions, Newton Circus | ContiExpert by Volt Autocare',
         'ContiExpert by Volt Autocare, 143 Bukit Timah Road inside the Shell station, Newton Circus, Singapore 229843. Call or WhatsApp +65 8221 5502. Map and directions.', body, (), cr)

FAQS = [
 ('Visiting', [
  {'q': 'Where exactly is the workshop?', 'a': 'Inside the Shell station at 143 Bukit Timah Road, Newton Circus, Singapore 229843. Search "Volt Autocare @Bukit Timah" in Google Maps or tap Directions on any page.'},
  {'q': 'Do I need an appointment?', 'a': 'Please WhatsApp us first. It lets us plan the bay and tell you how long the car is likely to stay, and saves you a wasted trip.'},
  {'q': 'Is ContiExpert the same workshop as Volt Autocare @Bukit Timah on Google Maps?', 'a': 'Yes. ContiExpert by Volt Autocare is our workshop at Newton Circus, and contiexpert.sg is its website. Google Maps lists us as Volt Autocare @Bukit Timah.'},
 ]),
 ('Cars and services', [
  {'q': 'Which makes do you service?', 'a': 'European cars are our speciality, including Mercedes-Benz, BMW, Audi and Volkswagen. We also look after hybrids, EVs and Japanese and Korean cars, for example servicing, batteries, brakes, aircon and pre-purchase inspections. Send us the model and year first.'},
  {'q': 'Can you service my car without voiding the manufacturer warranty?', 'a': 'Warranty terms differ between brands and dealers, so read your warranty booklet or ask the dealer what records they need. Our guide on dealer versus independent workshops explains what to check.'},
  {'q': 'Do you do pre-purchase inspections?', 'a': 'Yes, we offer a standard pre-purchase inspection and a hybrid or EV inspection that also looks at the battery. Book before you pay a deposit on the car.'},
  {'q': 'My warning light is on. Can I still drive in?', 'a': 'A red warning light, overheating, or brakes that feel wrong mean you should stop safely and not drive on. An amber engine light usually allows a careful drive in, but send us a photo first.'},
 ]),
 ('Quotes and payment', [
  {'q': 'How much will my repair cost?', 'a': 'It depends on the fault, the model and the parts chosen. We check the car first, explain what we found and agree the cost with you before any work starts.'},
  {'q': 'Will you do work I have not agreed to?', 'a': 'No. If we find something else during the job, we message you with what it is and the cost, and wait for your answer.'},
  {'q': 'Do you publish prices?', 'a': 'Yes for our most popular jobs: servicing packages from $118, aircon cooling-coil wash from $168 and a standard pre-purchase inspection at $60. For anything else, WhatsApp us your model and we give you a clear quote.'},
  {'q': 'Can I bring my own parts?', 'a': 'Yes. Customers bring their own parts and we fit them for labour only. Send us the part details first so we can check it suits your car.'},
 ]),
]

def faqs_page():
    cr = [('Home', '/'), ('FAQs', '/faqs/')]
    allf = [f for _, fs in FAQS for f in fs]
    body = f'''<div class="phead"><div class="wrap">{crumbs_html(cr)}<h1>Questions about servicing your car with us</h1>
<p class="answer">Answers to what owners ask before they visit {BRAND} at Newton Circus: where we are, which cars we work on, how quotes work and what to do when a warning light comes on. Anything not covered here, WhatsApp us on {PHONE}.</p></div></div>
<div class="sec"><div class="wrap layout"><div>{''.join('<div data-rv>%s</div>' % faq_html(fs, t) for t, fs in FAQS)}</div>{aside()}</div></div>'''
    page('/faqs/', 'European Car Servicing FAQs Singapore | ContiExpert by Volt Autocare',
         'Answers on visiting our Newton Circus workshop, makes we service, pre-purchase inspections, warning lights, quotes and how work is agreed.', body, [faq_ld(allf)], cr)

def about_page():
    cr = [('Home', '/'), ('About us', '/about/')]
    body = f'''<div class="phead"><div class="wrap">{crumbs_html(cr)}<h1>About {BRAND} at Newton Circus</h1>
<p class="answer">{BRAND} is a car workshop inside the Shell station at 143 Bukit Timah Road, Newton Circus. We service and repair European cars such as Mercedes-Benz, BMW, Audi and Volkswagen, and we check hybrids and EVs. contiexpert.sg is our website.</p></div></div>
<div class="sec"><div class="wrap layout"><article class="prose">
<section><h2>Who we are</h2><p>{BRAND} is one workshop at Newton Circus. Google Maps lists us as Volt Autocare @Bukit Timah, and you can find us on <a href="{SOCIAL[0]}" target="_blank" rel="noopener">Facebook</a>, <a href="{SOCIAL[1]}" target="_blank" rel="noopener">Instagram</a> and <a href="{SOCIAL[2]}" target="_blank" rel="noopener">TikTok</a> as ContiExpert by Volt Autocare.</p></section>
<section><h2>Who you will meet</h2><div class="teamrow">{img('team-coilwash', 'ContiExpert by Volt Autocare team member explaining an aircon coil wash')}{img('team-atf', 'ContiExpert by Volt Autocare team member with transmission fluids')}{img('team-outdoor', 'ContiExpert by Volt Autocare team member with a fluid service machine')}</div>
<p>These photos are from our own TikTok and Instagram videos, filmed at the workshop. Our team explains each job on camera the same way we explain it to you at the counter. In our Google reviews, customers often mention Newt and An by name.</p></section>
<section><h2>How we work</h2><ol><li>You tell us what the car is doing, on WhatsApp or at the workshop.</li><li>We check the car and show you what we found.</li><li>We explain what is urgent and what can wait, and give you the cost.</li><li>We start only after you agree, and message you when the car is ready.</li></ol></section>
<section><h2>Why a workshop at Newton?</h2><p>Newton Circus is close to the middle of Singapore. Owners from Novena, Orchard, Toa Payoh, Bukit Timah and the city can drop the car on the way to work, and Newton MRT is close by. See <a href="/areas-we-serve/">drivers within 10 km</a>.</p></section>
<section><h2>What our customers say</h2><p>Our Google listing showed <strong>{RATING[0]} stars from {RATING[1]} reviews</strong> when we checked on {RATING[2]}. A few of them:</p>{''.join('<blockquote class="aq">&ldquo;%s&rdquo; <cite>%s, %s</cite></blockquote>' % (E(q), E(n), E(d)) for n, d, j, q in REVIEWS[:4])}<p><a href="{MAPS}" target="_blank" rel="noopener" data-cta="maps">Read every review on Google</a>.</p></section>
</article>{aside()}</div></div>'''
    page('/about/', 'About Us, Newton Circus Workshop', 'ContiExpert by Volt Autocare is a European car workshop inside the Shell station at 143 Bukit Timah Road, Newton Circus, also offering hybrid and EV checks.', body, (), cr)

def article_hub():
    cr = [('Home', '/'), ('Guides', '/article/')]
    cards = ''.join('<a class="card acard" href="/%s/" data-rv><div class="band-top"></div><span class="tag">%s</span><h3>%s</h3><p>%s</p><span class="more">Read &rarr;</span></a>'
                    % (a['slug'], E(a.get('brand') or 'Car care'), E(a['h1']), E(a['desc']), ) for a in sorted(ARTICLES, key=lambda a: a.get('date', ''), reverse=True))  # newest first
    body = f'''<div class="phead"><div class="wrap">{crumbs_html(cr)}<h1>European car care guides</h1>
<p class="answer">Plain answers for owners in Singapore: warning lights, overheating, aircon, service schedules, choosing a workshop and checking a used car before you buy. Written by the {BRAND} team at Newton Circus.</p></div></div>
<div class="sec"><div class="wrap"><div class="grid g3">{cards}</div></div></div>'''
    page('/article/', 'European Car Care Guides Singapore | ContiExpert by Volt Autocare', 'Guides for European car owners in Singapore: warning lights, overheating, aircon, service schedules, dealer vs independent and pre-purchase checks.', body, (), cr)

def privacy_page():
    cr = [('Home', '/'), ('Privacy', '/privacy/')]
    body = f'''<div class="phead"><div class="wrap">{crumbs_html(cr)}<h1>Privacy notice</h1><p class="answer">How {LEGAL} handles the personal data you share with us, in line with Singapore's Personal Data Protection Act (PDPA).</p></div></div>
<div class="sec"><div class="wrap prose"><h2>What we collect</h2><p>When you WhatsApp, call or email us, we receive your name, number or email and what you tell us about your car. When you visit, we record the vehicle details we need for the job.</p>
<h2>Why we use it</h2><p>To reply to you, quote, carry out and record the work, and contact you about your car. We do not sell your data.</p>
<h2>Website</h2><p>This website has no contact form. It counts taps on the WhatsApp button (page, device type and time, with a random visit id) so we know which pages help people reach us. It does not record your phone number or name.</p>
<h2>Your rights</h2><p>You can ask to see, correct or withdraw consent for your data by emailing <a href="mailto:{EMAIL}">{EMAIL}</a>.</p><p>Last updated 3 November 2026.</p></div></div>'''
    page('/privacy/', 'Privacy Notice | ContiExpert by Volt Autocare', 'How ContiExpert by Volt Autocare handles personal data under the PDPA when you contact or visit our Newton Circus workshop.', body, (), cr)

def notfound():
    body = f'''<div class="phead"><div class="wrap"><h1>Page not found</h1><p class="answer">This page may have moved. Try our services, guides or contact page, or WhatsApp us on {PHONE}.</p>
<div class="btns"><a class="btn btn-volt" href="/">Home</a><a class="btn btn-ghost" href="/services/">Services</a><a class="btn btn-ghost" href="/article/">Guides</a></div></div></div>'''
    page('/404', 'Page not found | ContiExpert by Volt Autocare', 'Page not found.', body)

def extras():
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for p in SITEMAP: f.write('<url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (DOMAIN, p, max(MOD.get(p, TODAY), TODAY)))
        f.write('</urlset>\n')
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write('User-agent: *\nAllow: /\n\n' + ''.join('User-agent: %s\nAllow: /\n\n' % b for b in
                ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'ChatGPT-User', 'GPTBot', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot'])
                + 'Sitemap: %s/sitemap.xml\n' % DOMAIN)
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write(f'''# {BRAND}

> {BRAND} is a car workshop inside the Shell station at {ADDR1}, {ADDR2}. It services and repairs European cars (Mercedes-Benz, BMW, Audi, Volkswagen) and checks hybrids and EVs. Call or WhatsApp {PHONE}. Google Maps: "Volt Autocare @Bukit Timah", {RATING[0]} stars from {RATING[1]} reviews (checked {RATING[2]}).

- Website: {DOMAIN}/
- Email: {EMAIL}
- Map: {MAPS}

## Services
''' + ''.join('- [%s](%s/services/%s/): %s\n' % (s['name'], DOMAIN, s['slug'], s['card']) for s in SERVICES)
          + '\n## Makes\n' + ''.join('- [%s](%s/brands/%s/): %s\n' % (b['name'], DOMAIN, b['slug'], b['card']) for b in BRANDS)
          + '\n## Local\n- [Drivers within 10 km of Newton](%s/areas-we-serve/)\n- [Visit and directions](%s/contact-us/)\n' % (DOMAIN, DOMAIN)
          + '\n## Guides\n' + ''.join('- [%s](%s/%s/)\n' % (a['h1'], DOMAIN, a['slug']) for a in ARTICLES))
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': BRAND, 'short_name': SITE, 'start_url': '/', 'display': 'standalone', 'background_color': '#0b1b2b', 'theme_color': '#0b1b2b',
                   'icons': [{'src': '/assets/icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': '/assets/icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}, f)
    with open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w') as f: f.write(INDEXNOW_KEY)
    for n in ('ce.css', 'ce.js'): shutil.copy(os.path.join(HERE, n), os.path.join(OUT, n))
    with open('/mnt/project-files/tracking/wa-tap-counter.js') as f: tc = f.read().replace("'SLUG'", "'contiexpert'")
    with open(os.path.join(HERE, 'wa-tap-counter.js'), 'w') as f: f.write(tc)
    shutil.copy(os.path.join(HERE, 'wa-tap-counter.js'), os.path.join(OUT, 'wa-tap-counter.js'))
    subprocess.check_call([sys.executable, os.path.join(HERE, 'make_assets.py'), os.path.join(OUT, 'assets')], stdout=subprocess.DEVNULL)
    shutil.move(os.path.join(OUT, 'assets', 'favicon.ico'), os.path.join(OUT, 'favicon.ico'))
    make_og()
    os.makedirs(os.path.join(OUT, 'assets', 'video'), exist_ok=True)  # self-hosted videos (no GitHub/jsDelivr media)
    for v in ('find-us', 'ev-ppi'): shutil.copy(os.path.join(HERE, 'real', 'video-web', v + '.mp4'), os.path.join(OUT, 'assets', 'video', v + '-sm.mp4'))  # new names: the Bridge cannot overwrite the old >1 MB files
    with open(os.path.join(HERE, 'CONFIRM.md'), 'w') as f:
        f.write('# ContiExpert / Volt Autocare: facts to confirm before go-live (auto-written by build.py)\n\n' + ''.join('%d. %s\n' % (i + 1, x) for i, x in enumerate(CONFIRM)))

RF = os.environ.get('CE_RESEARCH', '/home/user/edwin-ai-monitor-android/pageone-site/clients/contiexpert/src/research-fetch')
def photos():
    subprocess.check_call([sys.executable, os.path.join(HERE, 'make_photos.py'), RF, os.path.join(OUT, 'assets')], stdout=subprocess.DEVNULL)
    PHOTOS.update(json.load(open(os.path.join(OUT, 'assets', 'photos', 'dims.json'))))
    os.remove(os.path.join(OUT, 'assets', 'photos', 'dims.json'))
def make_og():
    from PIL import Image, ImageDraw, ImageFont
    F = '/usr/share/fonts/opentype/inter/Inter-%s.otf'
    im = Image.new('RGB', (1200, 630), (12, 15, 20)); d = ImageDraw.Draw(im)
    ph = Image.open(os.path.join(OUT, 'assets', 'photos', 'real-bay.webp')).convert('RGB'); ph = ph.resize((int(ph.size[0] * 630 / ph.size[1]), 630))
    im.paste(ph, (1200 - ph.size[0], 0))
    for x in range(1200 - ph.size[0], 1200 - ph.size[0] + 160):
        a = 1 - (x - (1200 - ph.size[0])) / 160
        for y in range(0, 630, 1): pass
    grad = Image.new('L', (160, 630)); gd = ImageDraw.Draw(grad)
    for x in range(160): gd.line([(x, 0), (x, 630)], fill=int(255 * (1 - x / 160)))
    im.paste((12, 15, 20), (1200 - ph.size[0], 0, 1200 - ph.size[0] + 160, 630), grad)
    d.text((64, 70), 'ContiExpert', font=ImageFont.truetype(F % 'Bold', 46), fill='white')
    d.text((66, 126), 'by Volt Autocare', font=ImageFont.truetype(F % 'Medium', 24), fill=(90, 165, 255))
    y = 220
    for line in ('Continental and hybrid', 'car specialist at', 'Newton Circus'):
        d.text((64, y), line, font=ImageFont.truetype(F % 'Bold', 54), fill='white'); y += 66
    d.text((64, 460), 'Inside Shell, 143 Bukit Timah Road', font=ImageFont.truetype(F % 'Medium', 27), fill=(170, 182, 196))
    d.text((64, 502), 'WhatsApp +65 8221 5502', font=ImageFont.truetype(F % 'SemiBold', 27), fill=(90, 165, 255))
    im.save(os.path.join(OUT, 'assets', 'og.jpg'), quality=84, optimize=True)

def brand_check():
    """Stop the build if any page breaks the one-brand rule (McAfee fix, 6 Nov 2026)."""
    import re, glob
    bad = []
    for f in glob.glob(os.path.join(OUT, '**', '*'), recursive=True):
        if not f.endswith(('.html', '.txt', '.xml', '.webmanifest', '.js', '.css')): continue
        t = open(f, encoding='utf-8', errors='ignore').read(); rel = os.path.relpath(f, OUT)
        if re.search(r'jsdelivr|githubusercontent|github\.com/drdigital', t): bad.append(rel + ': jsdelivr/GitHub link')
        if re.search(r'(?<!by )Volt Autocare(?! @| Pte)', t): bad.append(rel + ': bare "Volt Autocare"')
        if f.endswith('.html'):
            m = re.search(r'<title>(.*?)</title>', t, re.S)
            if m and not m.group(1).strip().endswith('| ' + BRAND) and rel != '404.html': bad.append(rel + ': title not ending "| ' + BRAND + '"')
            if '"@type":"Article"' in t.replace(' ', '') and BRAND not in t.split('"author"', 1)[-1][:200]: bad.append(rel + ': article author is not ' + BRAND)
            if '"@type":"Article"' in t.replace(' ', '') and 'By the ' + BRAND + ' team' not in t: bad.append(rel + ': article byline missing')
    if bad: sys.exit('BRAND CHECK FAILED, do not upload:\n  ' + '\n  '.join(bad))
    print('brand check OK: one brand, no jsdelivr/GitHub media')

if __name__ == '__main__':
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    # copy the tap counter first so ver() can hash it
    with open('/mnt/project-files/tracking/wa-tap-counter.js') as f: tc = f.read().replace("'SLUG'", "'contiexpert'")
    with open(os.path.join(HERE, 'wa-tap-counter.js'), 'w') as f: f.write(tc)
    photos()
    build_urlnames()
    home(); services_hub()
    for s in SERVICES: detail_page('service', s)
    for b in BRANDS: detail_page('brand', b)
    article_hub()
    for a in ARTICLES: detail_page('article', a)
    areas_page(); contact_page(); faqs_page(); about_page(); privacy_page(); notfound()
    extras()
    brand_check()
    print('built', len(SITEMAP), 'pages ->', OUT)
