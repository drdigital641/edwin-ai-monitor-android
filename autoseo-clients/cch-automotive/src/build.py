#!/usr/bin/env python3
"""CCH Automotive site builder (AutoSEO.my client). One template set for every page: head, header, menu, footer,
mobile bar, CTA links and schema live here once, so one edit updates every page.
Facts: facts.json. Copy: strings_en.py. Output: ../dist/ (paths relative to the site root folder).
  python3 build.py            -> preview build for https://autoseo.my/preview/cch-automotive/ (noindex, nofollow)
  python3 build.py --live DOMAIN  -> live build at https://DOMAIN/ (still noindex until Edwin says go live; remove NOINDEX then)
Then: python3 check.py (banned words, CTA tracker, one H1, schema) before any upload through the Bridge."""
import hashlib, html, json, os, shutil, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import strings_en as S

F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
LIVE = '--live' in sys.argv
if LIVE:
    DOMAIN = sys.argv[sys.argv.index('--live') + 1]
    ORIGIN, BASE = f'https://{DOMAIN}', '/'
else:
    ORIGIN, BASE = 'https://autoseo.my', F['preview']['base_path']
NOINDEX = True  # preview: always. Live: set False only when Edwin approves go-live.
SITE = ORIGIN + BASE
OUT = os.path.join(HERE, '..', 'dist')
E = html.escape

def u(p=''):
    return BASE + p

def absu(p=''):
    return SITE + p

def ver(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]

WA_TEXT = urllib.parse.quote(F['whatsapp_prefill'])
WA = f"{F['whatsapp_url']}?text={WA_TEXT}"
TEL = 'tel:' + F['whatsapp_e164']
MAIL = 'mailto:' + F['email']
MAPS = F['maps_url']
FB = F['facebook']

# Photos: 4:5 web files (w, h) + matching -full lightbox files (w, h). Captions say only what the photo shows (README in the drop).
PHOTOS = {
    'alpine-fender-engine': (1280, 1600, (1200, 1600), 'Black BMW on a two-post lift, Alpine Germany fender cover on'),
    'bmw-x-lift': (1280, 1600, (1200, 1600), 'BMW X3 (F25) on the lift, new mounts on the floor'),
    'engine-bay-mini': (810, 1012, (810, 1080), 'MINI John Cooper Works on the lift, Motul oil ready'),
    'engine-bay-open-hood': (1280, 1600, (1200, 1600), 'Open engine bay, two bottles of Motul Multipower Plus'),
    'fj-cruiser-lift': (1280, 1600, (1200, 1600), 'Toyota FJ Cruiser on the scissor lift, Toyota AT fluid on the floor'),
    'fj-cruiser-yellow': (1229, 1536, (1600, 1200), 'Toyota FJ Cruiser in the bay'),
    'merc-engine-bay-2': (1280, 1600, (1200, 1600), 'White Mercedes-Benz on the lift with Alpine RS 0W-40'),
    'mercedes-c-white': (1229, 1536, (1600, 1200), 'Mercedes-Benz C-Class in the workshop'),
    'mercedes-ml-engine': (1280, 1600, (1200, 1600), 'Mercedes-Benz ML / GLE with Alpine RS 5W-40 C3'),
    'mercedes-white-engine-bay': (1280, 1600, (1200, 1600), 'Mercedes-Benz A-Class or CLA, Alpine Longlife III 5W-30 and DSG Fluid'),
    'mustang-lift': (1280, 1600, (1200, 1600), 'Ford Mustang transmission service, Motorcraft Mercon LV fluid'),
    'pickup-lift': (1280, 1600, (1200, 1600), 'Toyota Hilux GR Sport service with Alpine TSN 10W-40'),
    'subaru-engine-bay': (1280, 1600, (1200, 1600), 'Subaru WRX STI on the lift, new front control arms'),
    'oil-alpine-red': (1229, 1536, (1600, 1200), 'Alpine TSN 10W-40 and a Toyota oil filter'),
    'oil-jugs-red': (1280, 1600, (1200, 1600), 'Motorcraft Mercon LV, transmission pan, filter and gasket'),
    'alpine-yellow-oil': (1229, 1536, (1600, 1200), 'Alpine Longlife 12 FE 0W-30 and a Perodua oil filter'),
    'parts-engine-mounts': (736, 920, (736, 1000), 'Gearbox mounting for a BMW X3 F25'),
    'turbo-piping-parts': (1280, 1600, (1200, 1600), 'Old and new hoses on an Alpine fender cover'),
}
PRINTS = {  # contain only, true portrait ratio
    'poster-conti': (853, 1280, 'CCH Automotive services poster: Professional in Conti Car'),
    'flyer-service-repair': (763, 1080, 'CCH Automotive Car Service and Repair flyer'),
}
WORK_STRIP = ['mercedes-ml-engine', 'bmw-x-lift', 'fj-cruiser-lift', 'merc-engine-bay-2', 'mustang-lift', 'engine-bay-mini',
              'mercedes-c-white', 'pickup-lift', 'alpine-fender-engine', 'subaru-engine-bay', 'mercedes-white-engine-bay', 'fj-cruiser-yellow']

def img(stem):
    return u(f'images/{stem}.webp')

# ---------- icons (one authored set, 1.8 stroke) ----------
def icon(name):
    p = {
        'wa': '<path d="M4.5 19.5l1.2-3.6A8 8 0 1 1 8.6 18.6z"/><path d="M9.2 8.6c.3 2.6 2.4 4.9 5.2 5.4l1-1.2 1.8.8-.3 1.6c-3.9.4-8-3.6-7.7-7.5l1.6-.3.8 1.8z"/>',
        'call': '<path d="M5 4h4l1.5 4-2.2 1.4a11 11 0 0 0 6.3 6.3L16 13.5l4 1.5v4a1.5 1.5 0 0 1-1.6 1.5C10.6 20 4 13.4 3.5 5.6A1.5 1.5 0 0 1 5 4z"/>',
        'mail': '<rect x="3.5" y="5.5" width="17" height="13" rx="1"/><path d="M4 6.5l8 6 8-6"/>',
        'pin': '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
        'fb': '<rect x="3.5" y="3.5" width="17" height="17" rx="1.5"/><path d="M13.5 20.5v-7h2.3l.4-2.6h-2.7V9.4c0-.8.3-1.3 1.4-1.3h1.4V5.8a17 17 0 0 0-2.1-.1c-2 0-3.3 1.2-3.3 3.4v1.8H8.6v2.6h2.3v7"/>',
        'prev': '<path d="M15 5l-7 7 7 7"/>', 'next': '<path d="M9 5l7 7-7 7"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
        'menu': '<path d="M4 7h16M4 12h16M4 17h10"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'

# ---------- CTA links: data-cta = placement (Controller reads the whatsapp_/call_/email_ prefix as the tap type) ----------
def wa(place, label=None, cls='btn-wa'):
    label = label or S.UI['wa_btn']
    return (f'<a class="{cls}" href="{E(WA)}" target="_blank" rel="noopener" data-cta="whatsapp_{place}" data-ref="whatsapp_{place}">'
            f'{icon("wa")}<span>{E(label)}</span></a>')

def call(place, label=None, cls='btn-call'):
    label = label or S.UI['call_btn']
    return f'<a class="{cls}" href="{TEL}" data-cta="call_{place}" data-ref="call_{place}">{icon("call")}<span>{E(label)}</span></a>'

def mail(place, label=None, cls='lnk'):
    return f'<a class="{cls}" href="{MAIL}" data-cta="email_{place}" data-ref="email_{place}">{icon("mail")}<span>{E(label or F["email"])}</span></a>'

def maps(place, label=None, cls='lnk'):
    return (f'<a class="{cls}" href="{E(MAPS)}" target="_blank" rel="noopener" data-cta="map_{place}" data-ref="map_{place}">'
            f'{icon("pin")}<span>{E(label or S.UI["map_btn"])}</span></a>')

def fb(place, label=None, cls='lnk'):
    return (f'<a class="{cls}" href="{E(FB)}" target="_blank" rel="noopener" data-cta="facebook_{place}" data-ref="facebook_{place}">'
            f'{icon("fb")}<span>{E(label or S.UI["fb_btn"])}</span></a>')

# ---------- schema ----------
A = F['address']
BIZ_ID = absu('#business')
def business():
    return {
        '@type': ['AutoRepair', 'AutomotiveBusiness', 'LocalBusiness'], '@id': BIZ_ID,
        'name': F['name'], 'alternateName': [F['short'], F['also_called']], 'url': absu(),
        'description': S.HOME['desc'], 'slogan': F['tagline_verbatim'],
        'logo': absu('images/logo-transparent.png'), 'image': [absu('images/cover.webp'), absu('images/og.webp')],
        'telephone': F['whatsapp_e164'], 'email': F['email'],
        'address': {'@type': 'PostalAddress', 'streetAddress': A['street'], 'addressLocality': A['city'],
                    'addressRegion': A['region'], 'postalCode': A['postcode'], 'addressCountry': A['country']},
        'hasMap': MAPS, 'sameAs': [FB],
        'areaServed': [{'@type': 'City', 'name': 'Kota Kinabalu'}, {'@type': 'AdministrativeArea', 'name': 'Sabah'}],
        'knowsAbout': [s['name'] for s in S.SERVICES] + ['Continental cars', 'Mercedes-Benz', 'BMW', 'Audi', 'Volkswagen'],
        'contactPoint': {'@type': 'ContactPoint', 'telephone': F['whatsapp_e164'], 'contactType': 'customer service',
                         'availableLanguage': ['en', 'ms']},
    }

def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': absu(p)} for i, (n, p) in enumerate(items)]}

def faqld(faq):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}

def ld(graph):
    return '<script type="application/ld+json">' + json.dumps({'@context': 'https://schema.org', '@graph': graph},
                                                                ensure_ascii=False, separators=(',', ':')) + '</script>'

# ---------- shared layout ----------
NAV = [('services/', S.UI['nav_services']), ('about/', S.UI['nav_about']), ('articles/', S.UI['nav_articles']), ('contact/', S.UI['nav_contact'])]

def head(title, desc, path, graph, preload_hero=False):
    css_v = ver(os.path.join(OUT, 'assets', 'site.css'))
    rob = '<meta name="robots" content="noindex, nofollow">' if NOINDEX else ''
    pre = (f'<link rel="preload" as="image" href="{img("cover")}" type="image/webp" fetchpriority="high">' if preload_hero else '')
    return f'''<!DOCTYPE html>
<html lang="en-MY">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{rob}
<link rel="canonical" href="{absu(path)}">
<meta name="theme-color" content="#0B1220">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(F['short'])}">
<meta property="og:locale" content="en_MY">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{absu(path)}">
<meta property="og:image" content="{absu('images/og.webp')}">
<meta property="og:image:secure_url" content="{absu('images/og.webp')}">
<meta property="og:image:type" content="image/webp">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="CCH Automotive workshop bay in Likas, Kota Kinabalu">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{absu('images/og.webp')}">
<link rel="icon" type="image/webp" href="{img('favicon-512')}">
<link rel="apple-touch-icon" href="{u('images/logo-transparent.png')}">
<link rel="preload" as="font" type="font/woff2" href="{u('assets/fonts/league-spartan.woff2')}" crossorigin>
{pre}
<link rel="stylesheet" href="{u('assets/site.css')}?v={css_v}">
{ld(graph)}
</head>
<body>
<a class="skip" href="#main">{S.UI['skip']}</a>
'''

def header(active=''):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{u(p)}"{cur if active == p else ""}>{E(n)}</a>' for p, n in NAV)
    sheet = ''.join(f'<a href="{u(p)}">{E(n)}</a>' for p, n in [('', S.UI['nav_home'])] + NAV)
    svc = ''.join(f'<a href="{u("services/" + s["slug"] + "/")}">{E(s["name"])}</a>' for s in S.SERVICES)
    return f'''<header class="bar">
<div class="bar-in">
<a class="badge" href="{u()}" aria-label="CCH Automotive home"><img src="{img('favicon-512')}" width="44" height="44" alt="CCH Automotive logo"><span class="badge-t"><b>CCH</b> Automotive</span></a>
<nav class="nav" aria-label="Main">{links}</nav>
{wa('header', S.UI['wa_btn'], 'btn-wa sm hide-m')}
<button class="menu-b" type="button" aria-expanded="false" aria-controls="sheet">{icon('menu')}<span>{S.UI['menu']}</span></button>
</div>
</header>
<div class="sheet" id="sheet" hidden>
<div class="sheet-in">
<button class="sheet-x" type="button" aria-label="{S.UI['close']}">{icon('x')}</button>
<nav class="sheet-nav" aria-label="Menu">{sheet}</nav>
<nav class="sheet-svc" aria-label="Services">{svc}</nav>
{wa('menu', S.UI['wa_btn_long'])}
</div>
</div>
'''

def footer():
    js_v = ver(os.path.join(OUT, 'assets', 'site.js'))
    cta_v = ver(os.path.join(OUT, 'p1-cta.js'))
    pages = ''.join(f'<a href="{u(p)}">{E(n)}</a>' for p, n in [('', S.UI['nav_home'])] + NAV + [('privacy/', S.UI['privacy'])])
    svc = ''.join(f'<a href="{u("services/" + s["slug"] + "/")}">{E(s["name"])}</a>' for s in S.SERVICES)
    return f'''<footer class="foot">
<div class="foot-in">
<div class="foot-brand"><img src="{img('logo-transparent')}" width="120" height="120" alt="CCH Automotive logo" loading="lazy"><p class="foot-name">{E(F['name'])}</p><p class="foot-tag">{E(F['tagline_verbatim'])}</p></div>
<div><h2 class="foot-h">{S.UI['footer_find']}</h2><address>{E(A['one_line'])}</address>{maps('footer')}</div>
<div><h2 class="foot-h">{S.UI['footer_talk']}</h2>{wa('footer', S.UI['wa_btn_long'], 'lnk')}{call('footer', S.UI['call_btn_long'], 'lnk')}{mail('footer')}{fb('footer')}</div>
<div><h2 class="foot-h">{S.UI['nav_services']}</h2><nav class="foot-nav" aria-label="Services">{svc}</nav></div>
<div><h2 class="foot-h">{S.UI['footer_pages']}</h2><nav class="foot-nav" aria-label="Pages">{pages}</nav></div>
</div>
<div class="foot-base"><p>{E(S.UI['brands_note'])}</p><p class="credit"><a href="https://autoseo.my/">{S.UI['credit']}</a></p></div>
</footer>
<nav class="dock" aria-label="Contact">{wa('mobile_bar', S.UI['wa_btn'])}{call('mobile_bar', S.UI['call_btn'])}</nav>
<dialog class="lb" id="lb" aria-label="Photo"><button class="lb-x" type="button" aria-label="{S.UI['close']}">{icon('x')}</button><img alt="" decoding="async"><p class="lb-c"></p></dialog>
<script src="{u('assets/site.js')}?v={js_v}" defer></script>
<script src="{u('p1-cta.js')}?v={cta_v}" defer></script>
</body>
</html>
'''

def page(path, title, desc, graph, body, active='', hero=False):
    return head(title, desc, path, graph, hero) + header(active) + f'<main id="main">{body}</main>\n' + footer()

# ---------- blocks ----------
def stripe():
    return '<div class="stripe" aria-hidden="true"></div>'

def frame(stem, eager=False, cls='shot'):
    w, h, full, cap = PHOTOS[stem]
    load = '' if eager else ' loading="lazy"'
    return (f'<figure class="{cls}"><button type="button" class="shot-b" data-full="{u("images/" + stem + "-full.webp")}" '
            f'data-cap="{E(cap)}" aria-label="{S.UI["photo_open"]}: {E(cap)}"><img src="{img(stem)}" width="{w}" height="{h}" '
            f'alt="{E(cap)}" decoding="async"{load}></button><figcaption>{E(cap)}</figcaption></figure>')

def printed(stem):
    w, h, alt = PRINTS[stem]
    return f'<figure class="print"><img src="{img(stem)}" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy" decoding="async"><figcaption>{E(alt)}</figcaption></figure>'

def card(s):
    st = s['card']
    if st in PRINTS:
        w, h, alt = PRINTS[st]
        pic = f'<span class="card-p print-p"><img src="{img(st)}" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy" decoding="async"></span>'
    else:
        w, h, _, cap = PHOTOS[st]
        pic = f'<span class="card-p"><img src="{img(st)}" width="{w}" height="{h}" alt="{E(cap)}" loading="lazy" decoding="async"></span>'
    return (f'<a class="card" href="{u("services/" + s["slug"] + "/")}">{pic}<span class="card-t">{E(s["name"])}</span>'
            f'<span class="card-l">{E(s["card_line"])}</span></a>')

def scroller(items):
    return (f'<div class="snap-w"><div class="snap" tabindex="0" aria-label="{S.UI["nav_services"]}">{"".join(card(s) for s in items)}</div>'
            f'<div class="snap-ctl"><button type="button" class="arr" data-dir="-1" aria-label="{S.UI["prev"]}">{icon("prev")}</button>'
            f'<button type="button" class="arr" data-dir="1" aria-label="{S.UI["next"]}">{icon("next")}</button></div></div>')

def rail(stems, label):
    return (f'<div class="rail-w"><div class="rail" tabindex="0" aria-label="{E(label)}">{"".join(frame(s) for s in stems)}</div>'
            f'<div class="rail-ctl"><button type="button" class="arr" data-dir="-1" aria-label="{S.UI["prev"]}">{icon("prev")}</button>'
            f'<div class="dots" aria-hidden="true">{"<i></i>" * len(stems)}</div>'
            f'<button type="button" class="arr" data-dir="1" aria-label="{S.UI["next"]}">{icon("next")}</button></div></div>')

def lift_svg(i):
    # Two-post lift; the car sits higher at each step (i = 0..3).
    y = 58 - i * 13
    return (f'<svg class="lift" viewBox="0 0 120 80" aria-hidden="true" style="--rise:{i * 13}px">'
            f'<rect x="8" y="6" width="7" height="70" class="post"/><rect x="105" y="6" width="7" height="70" class="post"/>'
            f'<rect x="4" y="74" width="112" height="3" class="floor"/>'
            f'<g class="car"><rect x="15" y="{y + 8}" width="90" height="2.5" class="arm"/>'
            f'<path d="M22 {y + 8}h76l-4-8-14-2-9-6H46l-12 6-8 2z" class="body"/>'
            f'<circle cx="38" cy="{y + 8}" r="5" class="wheel"/><circle cx="82" cy="{y + 8}" r="5" class="wheel"/></g></svg>')

def process():
    steps = ''.join(f'<li class="step">{lift_svg(i)}<div><h3><span class="n">{i + 1}</span>{E(t)}</h3><p>{E(d)}</p></div></li>'
                    for i, (t, d) in enumerate(S.HOME['process_steps']))
    return (f'<section class="sec process"><div class="wrap"><h2>{E(S.HOME["process_h2"])}</h2>'
            f'<ol class="steps">{steps}</ol><p class="act">{wa("process", S.UI["wa_btn_long"])}</p></div></section>')

def faq_block(faq, h2):
    items = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)
    return f'<section class="sec faq"><div class="wrap narrow"><h2>{E(h2)}</h2>{items}</div></section>'

def ask_block(place):
    return (f'<section class="sec ask"><div class="wrap">{stripe()}<h2>{E(S.UI["ask_title"])}</h2><p>{E(S.UI["ask_line"])}</p>'
            f'<div class="act">{wa(place, S.UI["wa_btn_long"])}{call(place, S.UI["call_btn_long"])}</div></div></section>')

def page_head(h1, lead, trail):
    bc = ''.join(f'<a href="{u(p)}">{E(n)}</a><span aria-hidden="true">/</span>' for n, p in trail[:-1]) + f'<span>{E(trail[-1][0])}</span>'
    return (f'<section class="ph"><div class="wrap"><nav class="bc" aria-label="Breadcrumb">{bc}</nav>'
            f'<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p></div>{stripe()}</section>')

# ---------- pages ----------
def home():
    H = S.HOME
    hero = f'''<section class="bay">
<div class="bay-ph"><img src="{img('cover')}" width="1170" height="731" alt="CCH Automotive workshop bay with a black Ford Mustang, a yellow Porsche and a black Porsche on a two-post lift" fetchpriority="high" decoding="async"><span class="sweep" aria-hidden="true"></span><span class="tag">{E(H['hero_tag'])}</span></div>
<div class="bay-tx"><h1>{E(H['h1'])}</h1><div><p class="bay-l">{E(H['hero_line'])}</p><div class="bay-cta">{wa('home_hero', S.UI['wa_btn'])}{call('home_hero', S.UI['call_btn'], 'btn-call ghost')}</div></div></div>
{stripe()}
</section>'''
    svc = (f'<section class="sec svc"><div class="wrap"><h2>{E(H["services_h2"])}</h2><p class="sub">{E(H["services_line"])}</p></div>'
           f'{scroller(S.SERVICES)}</section>')
    brands = ''.join(f'<li>{E(b)}</li>' for b in F['brands_from_hashtags'])
    intro = (f'<section class="sec intro"><div class="wrap split"><div><h2>{E(H["intro_h2"])}</h2>'
             + ''.join(f'<p>{E(p)}</p>' for p in H['intro_p'])
             + f'</div><div class="brands"><h3>{E(H["brands_label"])}</h3><ul>{brands}</ul></div></div></section>')
    posts = ''.join(f'<li>{E(x)}</li>' for x in F['cars_worked_on']['from_posts'])
    work = (f'<section class="sec work"><div class="wrap"><h2>{E(H["work_h2"])}</h2><p class="sub">{E(H["work_line"])}</p></div>'
            f'{rail(WORK_STRIP, H["work_h2"])}<div class="wrap"><h3>{E(H["posts_h3"])}</h3><ul class="chips">{posts}</ul></div></section>')
    oil = (f'<section class="sec oil"><div class="wrap split"><figure class="wide"><img src="{img("oil-kit")}" width="1600" height="1200" '
           f'alt="Parts laid out for a service: Alpine RSL 5W-40, filters, fluids, suspension and steering parts" loading="lazy" decoding="async">'
           f'<figcaption>Parts laid out for a service: Alpine RSL 5W-40, filters, fluids, suspension and steering parts</figcaption></figure>'
           f'<div><h2>{E(H["oil_h2"])}</h2><p>{E(H["oil_p"])}</p><p><a class="more" href="{u("services/car-service-maintenance/")}">Car service and maintenance</a></p></div></div></section>')
    visit = (f'<section class="sec visit"><div class="wrap">{stripe()}<h2>{E(H["visit_h2"])}</h2><p>{E(H["visit_p"])}</p>'
             f'<div class="act">{wa("home_visit", S.UI["wa_btn_long"])}{maps("home_visit", None, "btn-line")}</div></div></section>')
    body = hero + svc + intro + process() + work + oil + faq_block(S.FAQ_HOME, H['faq_h2']) + visit
    graph = [business(), {'@type': 'WebSite', 'name': F['short'], 'url': absu(), 'inLanguage': 'en-MY'},
             {'@type': 'WebPage', 'name': H['title'], 'url': absu(), 'about': {'@id': BIZ_ID}}, faqld(S.FAQ_HOME)]
    return page('', H['title'], H['desc'], graph, body, '', True)

def service(s):
    path = f'services/{s["slug"]}/'
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_services'], 'services/'), (s['name'], path)]
    blocks = ''.join(f'<h2>{E(h)}</h2><p>{E(p)}</p>' for h, p in s['body'])
    cta = f'<div class="act">{wa("service_" + s["id"].replace("-", "_"), S.UI["wa_btn_long"])}{call("service_" + s["id"].replace("-", "_"), S.UI["call_btn"])}</div>'
    media = ''
    if s.get('photos'):
        media += f'<div class="gal">{"".join(frame(x) for x in s["photos"])}</div>'
    if s.get('wide'):
        media += (f'<figure class="wide"><img src="{img(s["wide"])}" width="1600" height="1200" alt="Parts laid out for a service: Alpine RSL 5W-40, filters, fluids, suspension and steering parts" '
                  f'loading="lazy" decoding="async"><figcaption>Parts laid out for a service: Alpine RSL 5W-40, filters, fluids, suspension and steering parts</figcaption></figure>')
    if s.get('poster'):
        media += f'<div class="prints one">{printed(s["poster"])}</div>'
    others = ''.join(f'<a href="{u("services/" + o["slug"] + "/")}">{E(o["name"])}</a>' for o in S.SERVICES if o['id'] != s['id'])
    body = (page_head(s['h1'], s['lead'], trail)
            + f'<section class="sec"><div class="wrap split svc-body"><div class="prose">{blocks}{cta}</div><div class="media">{media}</div></div></section>'
            + faq_block(s['faq'], 'Questions about ' + s['name'].lower())
            + f'<section class="sec more-s"><div class="wrap"><h2>{S.UI["related"]}</h2><nav class="pills" aria-label="{S.UI["related"]}">{others}</nav></div></section>'
            + ask_block('service_' + s['id'].replace('-', '_') + '_end'))
    graph = [business(), crumbs(trail),
             {'@type': 'Service', 'name': s['name'], 'serviceType': s['name'], 'description': s['desc'], 'url': absu(path),
              'provider': {'@id': BIZ_ID}, 'areaServed': {'@type': 'City', 'name': 'Kota Kinabalu'}},
             faqld(s['faq'])]
    return page(path, s['title'], s['desc'], graph, body, 'services/')

def services_index():
    X = S.SERVICES_INDEX
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_services'], 'services/')]
    grid = ''.join(card(s) for s in S.SERVICES)
    body = (page_head(X['h1'], X['lead'], trail) + f'<section class="sec"><div class="wrap"><div class="cards">{grid}</div></div></section>'
            + ask_block('services'))
    graph = [business(), crumbs(trail), {'@type': 'ItemList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': s['name'], 'url': absu('services/' + s['slug'] + '/')} for i, s in enumerate(S.SERVICES)]}]
    return page('services/', X['title'], X['desc'], graph, body, 'services/')

def about():
    X = S.ABOUT
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_about'], 'about/')]
    blocks = ''.join(f'<h2>{E(h)}</h2><p>{E(p)}</p>' for h, p in X['body'])
    body = (page_head(X['h1'], X['lead'], trail)
            + f'<section class="sec"><div class="wrap split"><div class="prose">{blocks}</div><div class="media"><div class="gal two">{frame("merc-engine-bay-2")}{frame("pickup-lift")}</div></div></div></section>'
            + f'<section class="sec"><div class="wrap"><h2>{E(X["media_h2"])}</h2><div class="prints">{printed("poster-conti")}{printed("flyer-service-repair")}</div></div></section>'
            + ask_block('about'))
    graph = [business(), crumbs(trail), {'@type': 'AboutPage', 'name': X['title'], 'url': absu('about/'), 'about': {'@id': BIZ_ID}}]
    return page('about/', X['title'], X['desc'], graph, body, 'about/')

def contact():
    X = S.CONTACT
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_contact'], 'contact/')]
    body = (page_head(X['h1'], X['lead'], trail)
            + f'''<section class="sec"><div class="wrap split">
<div class="prose"><h2>WhatsApp or call</h2><p class="big"><a href="{TEL}" data-cta="call_contact_number" data-ref="call_contact_number">{E(F['whatsapp_display'])}</a></p>
<div class="act">{wa('contact', S.UI['wa_btn_long'])}{call('contact', S.UI['call_btn'])}</div>
<h2>Email and Facebook</h2><p class="links">{mail('contact')}{fb('contact')}</p>
<h2>Opening hours</h2><p>{E(X['hours_note'])}</p></div>
<div class="prose"><h2>Address</h2><address class="big-a">{E(A['street'])}<br>{E(A['postcode'])} {E(A['city'])}, {E(A['region'])}<br>{E(A['country_name'])}</address>
<p>{E(A['area_note'])}.</p><p>{maps('contact', None, 'btn-line')}</p></div>
</div></section>''')
    graph = [business(), crumbs(trail), {'@type': 'ContactPage', 'name': X['title'], 'url': absu('contact/'), 'about': {'@id': BIZ_ID}}]
    return page('contact/', X['title'], X['desc'], graph, body, 'contact/')

def privacy():
    X = S.PRIVACY
    trail = [(S.UI['nav_home'], ''), (S.UI['privacy'], 'privacy/')]
    blocks = ''.join(f'<h2>{E(h)}</h2><p>{E(p)}</p>' for h, p in X['body'])
    body = page_head(X['h1'], 'Last updated ' + '18 November 2026' + '.', trail) + f'<section class="sec"><div class="wrap narrow prose">{blocks}</div></section>'
    return page('privacy/', X['title'], X['desc'], [business(), crumbs(trail)], body)

def articles():
    X = S.ARTICLES
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_articles'], 'articles/')]
    body = (page_head(X['h1'], X['lead'], trail)
            + '<section class="sec"><div class="wrap"><div class="art-list" id="articles"></div></div></section>' + ask_block('articles'))
    graph = [business(), crumbs(trail), {'@type': 'CollectionPage', 'name': X['title'], 'url': absu('articles/')}]
    return page('articles/', X['title'], X['desc'], graph, body, 'articles/')

def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets', 'fonts'))
    for f in ('site.css', 'site.js'):
        shutil.copy(os.path.join(HERE, 'assets', f), os.path.join(OUT, 'assets', f))
    for f in os.listdir(os.path.join(HERE, 'assets', 'fonts')):
        shutil.copy(os.path.join(HERE, 'assets', 'fonts', f), os.path.join(OUT, 'assets', 'fonts', f))
    shutil.copy(os.path.join(HERE, 'p1-cta.js'), os.path.join(OUT, 'p1-cta.js'))
    pages = {'': home(), 'services/': services_index(), 'about/': about(), 'contact/': contact(), 'privacy/': privacy(), 'articles/': articles()}
    for s in S.SERVICES:
        pages[f'services/{s["slug"]}/'] = service(s)
    for p, h in pages.items():
        d = os.path.join(OUT, p)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf8').write(h)
    # sitemap.xml + llms.txt from the page list (ready for a live domain; never linked from autoseo.my)
    sm = ''.join(f'<url><loc>{absu(p)}</loc><lastmod>{F["updated"]}</lastmod></url>\n' for p in pages)
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sm}</urlset>\n')
    svc = '\n'.join(f'- [{s["name"]}]({absu("services/" + s["slug"] + "/")}): {s["card_line"]}' for s in S.SERVICES)
    llms = f"""# {F['name']}

> {F['category']} in Likas Baharu, Kota Kinabalu, Sabah, Malaysia. "{F['tagline_verbatim']}", with {F['experience_verbatim']}.

- Address: {A['one_line']} ({A['area_note']})
- WhatsApp and phone: {F['whatsapp_display_intl']} ({F['whatsapp_url']})
- Email: {F['email']}
- Facebook: {FB}
- Map: {MAPS}
- Makes: {', '.join(F['brands_from_hashtags'])} and other makes shown in our work photos
- Engine oil: {F['oil']['brand']}
- Opening hours: not published; WhatsApp to arrange a time

## Services
{svc}

## Pages
""" + '\n'.join(f'- {absu(p)}' for p in pages) + '\n'
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf8').write(llms)
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {absu("sitemap.xml")}\n')
    print(f'built {len(pages)} pages -> {os.path.abspath(OUT)} (base {SITE})')

if __name__ == '__main__':
    build()
