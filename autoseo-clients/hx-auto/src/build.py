#!/usr/bin/env python3
"""HX Auto Service site builder (AutoSEO.my client preview, 19 Nov 2026).
One template set for every page: head, header, menu sheet, footer, mobile bar, CTA links and schema live here once, so one
edit updates every page in every language. Facts: facts.json. Copy: strings_en.py / strings_ms.py / strings_zh.py (same keys).
Language plumbing (switcher, hreflang, og:locale, sitemap) comes from the shared template ../../../autoseo-template/autoseo_i18n.py.
  python3 build.py                 -> preview build for https://autoseo.my/preview/hx-auto/ (noindex, nofollow)
  python3 build.py --live DOMAIN   -> build for https://DOMAIN/ (still noindex until Edwin approves go-live)
Then python3 check.py (pre-upload gate) before any Bridge upload (sync_from_github, site autoseo, base_path preview/hx-auto).
Photos are NOT in this repo: they were placed on the server from Bridge drops 6afefb47... and 6afefb93... into images/."""
import hashlib, html, json, os, shutil, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'autoseo-template'))
import autoseo_i18n as I18N
import strings_en, strings_ms, strings_zh
STRINGS = {'en': strings_en, 'ms': strings_ms, 'zh': strings_zh}
S, L = strings_en, I18N.LANGS[0]

F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
# GO-LIVE (20 Nov 2026): one set of files serves both hosts. Links are page-relative (placeholder swapped at write time),
# canonical / hreflang / schema / sitemap / robots / llms are on the live domain, og:image + twitter:image + og:url stay on the
# working preview-host URLs until https://hxautoservice.com.my/ answers 200 over SSL (then set SHARE_LIVE = True).
LIVE_DOMAIN = 'hxautoservice.com.my'
SHARE_LIVE = True
ORIGIN, BASE = 'https://' + LIVE_DOMAIN, '@@B@@/'
NOINDEX = False   # preview noindex = Host-conditional X-Robots-Tag in autoseo.my/preview/.htaccess, never a meta tag
SITE = ORIGIN + '/'
SHARE = SITE if SHARE_LIVE else 'https://autoseo.my' + F['preview']['base_path']
OUT = os.path.join(HERE, '..', 'dist')
E = html.escape
LOC = F['locations'][0]
TEL = 'tel:' + F['whatsapp_e164']
FB = F['facebook']
R = F['reviews']


def u(p=''):
    return BASE + p


def absu(p=''):
    return SITE + p


def shu(p=''):
    return SHARE + p


def pu(p=''):
    return u(I18N.page_path(L, p))


def pabs(p=''):
    return absu(I18N.page_path(L, p))


def ver(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]


def wa_url():
    return f"{F['whatsapp_url']}?text={urllib.parse.quote(S.PREFILL)}"


# 4:5 work files (w, h) and -full lightbox files (w, h), from manifest.json in the drop.
PHOTOS = {
    'shopfront-signboard': (960, 1200, 1600, 1200), 'shopfront-forecourt': (864, 1080, 1440, 1080),
    'honda-hrv-front': (1229, 1536, 1600, 1200), 'kia-cerato-on-lift': (1229, 1536, 1600, 1200),
    'mercedes-c-class-bay': (1229, 1536, 1600, 1200), 'mercedes-amg-matte': (1229, 1536, 1600, 1200),
    'bmw-5-series-engine': (1229, 1536, 1600, 1200), 'land-rover-discovery-sport': (1229, 1536, 1600, 1200),
    'toyota-vios-red-lift': (1229, 1536, 1600, 1200), 'nissan-gt-r-on-lift': (1229, 1536, 1600, 1200),
    'toyota-alphard-white': (1229, 1536, 1600, 1200), 'mini-cooper-s-on-lift': (1229, 1536, 1600, 1200),
    'honda-jazz-engine': (1229, 1536, 1600, 1200), 'nissan-qashqai-on-lift': (1229, 1536, 1600, 1200),
    'mazda-3-engine': (1229, 1536, 1600, 1200), 'bmw-5-series-on-lift': (1229, 1536, 1600, 1200),
    'toyota-vellfire-bay': (1229, 1536, 1600, 1200), 'mercedes-van-two-post': (576, 720, 960, 720),
    'mercedes-oil-belt-parts': (576, 720, 960, 720), 'vellfire-on-lift-side': (576, 720, 960, 720),
    'workshop-bays-overview': (864, 1080, 1440, 1080), 'nissan-coils-and-oil': (576, 720, 960, 720),
    'bmw-oil-and-filter': (576, 720, 960, 720), 'subaru-coilover-service': (576, 720, 960, 720),
    'aircond-flushing-banner': (960, 1200, 1600, 1200),
}
CAROUSEL = ['workshop-bays-overview', 'mercedes-amg-matte', 'nissan-gt-r-on-lift', 'toyota-alphard-white', 'bmw-5-series-on-lift',
            'subaru-coilover-service', 'mini-cooper-s-on-lift', 'land-rover-discovery-sport', 'aircond-flushing-banner', 'kia-cerato-on-lift',
            'mercedes-c-class-bay', 'nissan-coils-and-oil', 'toyota-vellfire-bay', 'honda-jazz-engine', 'nissan-qashqai-on-lift',
            'bmw-5-series-engine', 'mercedes-van-two-post', 'toyota-vios-red-lift', 'mazda-3-engine', 'mercedes-oil-belt-parts',
            'vellfire-on-lift-side', 'honda-hrv-front', 'bmw-oil-and-filter', 'shopfront-forecourt', 'shopfront-signboard']
assert sorted(CAROUSEL) == sorted(PHOTOS)
DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
DAY_SCHEMA = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


# Enhanced full-colour set (Bridge drop hx-auto-enhanced-2026-11-19): originals in images/hd/, web sizes in images/hx/.
# <stem>-t.webp 720x900 (4:5 tile), <stem>-l.webp 1000x750 and <stem>-xl.webp 1600x1200 (4:3 full frame). No grade or tint.
ENH = {'shopfront-signboard', 'shopfront-forecourt', 'workshop-bays-overview', 'aircond-flushing-banner', 'mercedes-c-class-bay',
       'bmw-5-series-engine', 'bmw-5-series-on-lift', 'land-rover-discovery-sport', 'mini-cooper-s-on-lift', 'kia-cerato-on-lift',
       'toyota-alphard-white', 'toyota-vellfire-bay', 'mazda-3-engine', 'honda-jazz-engine'}
for _s in ENH:
    PHOTOS[_s] = (720, 900, 1600, 1200)
HERO_SET = [(960, 540), (1600, 900), (2400, 1350)]


def img(stem):
    return u(f'images/hx/{stem}-t.webp') if stem in ENH else u(f'images/{stem}.webp')


def img_full(stem):
    return u(f'images/hx/{stem}-xl.webp') if stem in ENH else u(f'images/{stem}-full.webp')


def hero_srcset():
    return ', '.join(f'{u(f"images/hx/hero-{w}.webp")} {w}w' for w, _ in HERO_SET)


HERO_SIZES = '(max-width: 899px) 170vh, 100vw'


def icon(name):
    p = {
        'wa': '<path d="M4.6 19.4l1.1-3.5a7.9 7.9 0 1 1 2.9 2.7z"/><path d="M9.3 8.7c.3 2.5 2.3 4.7 5 5.2l.9-1.1 1.8.8-.3 1.5c-3.8.4-7.7-3.5-7.5-7.3l1.5-.3.8 1.7z"/>',
        'call': '<path d="M5.2 4h3.6l1.6 4-2.1 1.3a10.6 10.6 0 0 0 6.4 6.4l1.3-2.1 4 1.6v3.6a1.6 1.6 0 0 1-1.7 1.6C10.4 19.9 4.1 13.6 3.6 5.7A1.6 1.6 0 0 1 5.2 4z"/>',
        'pin': '<path d="M12 21s-6.4-5.5-6.4-10.9a6.4 6.4 0 0 1 12.8 0C18.4 15.5 12 21 12 21z"/><circle cx="12" cy="10.1" r="2.2"/>',
        'nav': '<path d="M4 11.4L20 4l-7.4 16-1.7-6.9z"/>',
        'fb': '<path d="M13.4 21v-7.4h2.5l.4-3h-2.9V8.7c0-.9.3-1.5 1.5-1.5h1.6V4.5a20 20 0 0 0-2.3-.1c-2.3 0-3.8 1.4-3.8 3.9v2.3H8v3h2.4V21"/>',
        'scan': '<rect x="3.5" y="5" width="17" height="11" rx="1.5"/><path d="M8 20h8M12 16v4M6.5 11.5h2l1.3-2.6 2 5 1.4-2.4h4.3"/>',
        'wrench': '<path d="M14.6 4.4a4 4 0 0 0-4.9 5.3L4 15.4 6.6 18l5.7-5.7a4 4 0 0 0 5.3-4.9l-2.4 2.4-2.3-.6-.6-2.3z"/>',
        'key': '<circle cx="8" cy="15" r="3.4"/><path d="M10.4 12.6L19 4M16 7l2.4 2.4M14 9l1.8 1.8"/>',
        'car': '<path d="M4 15.5V12l2-4.5h12l2 4.5v3.5zM4 12h16"/><circle cx="7.5" cy="16.5" r="1.6"/><circle cx="16.5" cy="16.5" r="1.6"/>',
        'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
        'prev': '<path d="M15 5l-7 7 7 7"/>', 'next': '<path d="M9 5l7 7-7 7"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
        'menu': '<path d="M4 7h16M4 12h16M4 17h11"/>', 'go': '<path d="M5 12h13M13 6l6 6-6 6"/>',
        'tow': '<path d="M3 16h9V9h4l3 4v3h-2"/><circle cx="7" cy="17" r="2"/><circle cx="16" cy="17" r="2"/><path d="M12 9L6 4"/>',
        'engine': '<path d="M4 10h2V8h3V6h6v2h2l2 3h1v5h-1l-2 2H9l-2-2H6v-2H4z"/><path d="M11 6V4h2v2"/>',
        'snow': '<path d="M12 3v18M4.2 7.5l15.6 9M19.8 7.5l-15.6 9"/><path d="M9.5 4.5L12 7l2.5-2.5M9.5 19.5L12 17l2.5 2.5"/>',
        'disc': '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="2.5"/><path d="M12 3.5v3M20.5 12h-3M12 20.5v-3M3.5 12h3"/>',
        'battery': '<rect x="3.5" y="7" width="17" height="12" rx="1.5"/><path d="M7 7V5h3v2M14 7V5h3v2M7 13h3M15.5 11.5v3M14 13h3"/>',
        'lift': '<path d="M5 21V4M19 21V4M5 13h14"/><path d="M7.5 13l1.2-3h6.6l1.2 3"/><circle cx="9" cy="16" r="1.4"/><circle cx="15" cy="16" r="1.4"/>',
        'quote': '<path d="M5 18v-4.5C5 9.5 7 7 10 6M14 18v-4.5c0-4 2-6.5 5-7.5"/><path d="M5 14h4v4H5zM14 14h4v4h-4z"/>',
        'oil': '<path d="M5 9h9l3-2 3 1-4 4H5zM5 9v8h11v-5"/><path d="M20 14c0 1-1 2-1 2s-1-1-1-2 1-2 1-2 1 1 1 2z"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'


# ---------- CTA links (data-cta = placement; the Controller reads the whatsapp_/call_/facebook_/waze_/map_ prefix) ----------
def wa(place, label=None, cls='btn-wa'):
    return (f'<a class="{cls}" href="{E(wa_url())}" target="_blank" rel="noopener" data-cta="whatsapp_{place}" data-ref="whatsapp_{place}">'
            f'{icon("wa")}<span>{E(label or S.UI["wa_btn"])}</span></a>')


def call(place, label=None, cls='btn-call'):
    return f'<a class="{cls}" href="{TEL}" data-cta="call_{place}" data-ref="call_{place}">{icon("call")}<span>{E(label or S.UI["call_btn"])}</span></a>'


def fb(place, label=None, cls='lk'):
    return (f'<a class="{cls}" href="{E(FB)}" target="_blank" rel="noopener" data-cta="facebook_{place}" data-ref="facebook_{place}">'
            f'{icon("fb")}<span>{E(label or S.UI["fb_btn"])}</span></a>')


def waze(place, cls='lk'):
    return (f'<a class="{cls}" href="{E(LOC["waze"])}" target="_blank" rel="noopener" data-cta="waze_{place}" data-ref="waze_{place}">'
            f'{icon("nav")}<span>{E(S.UI["waze_btn"])}</span></a>')


def gmap(place, cls='lk'):
    return (f'<a class="{cls}" href="{E(LOC["maps_url"])}" target="_blank" rel="noopener" data-cta="map_{place}" data-ref="map_{place}">'
            f'{icon("pin")}<span>{E(S.UI["map_btn"])}</span></a>')


# ---------- schema ----------
BIZ_ID = absu('#business')


def opening_spec():
    out = []
    for d, n in zip(DAYS, DAY_SCHEMA):
        v = F['hours'][d]
        if v == 'closed':
            continue
        o, c = v.split('-')
        out.append({'@type': 'OpeningHoursSpecification', 'dayOfWeek': f'https://schema.org/{n}', 'opens': o, 'closes': c})
    return out


def opening_hours():
    ab = {'monday': 'Mo', 'tuesday': 'Tu', 'wednesday': 'We', 'thursday': 'Th', 'friday': 'Fr', 'saturday': 'Sa'}
    return [f"{ab[d]} {F['hours'][d]}" for d in DAYS if F['hours'][d] != 'closed']


def business():
    return {
        '@type': ['AutoRepair', 'AutomotiveBusiness', 'LocalBusiness'], '@id': BIZ_ID,
        'name': F['name'], 'legalName': F['legal_name'], 'url': pabs(), 'description': S.HOME['desc'],
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'Company registration number (Malaysia)', 'value': F['company_no']},
        'logo': absu('images/logo-transparent.png'), 'image': [absu('images/cover.webp'), shu('images/og.jpg') + '?v=3'],
        'telephone': F['whatsapp_e164'],
        'address': {'@type': 'PostalAddress', 'streetAddress': LOC['street'], 'addressLocality': LOC['city'], 'addressRegion': LOC['region'],
                    'postalCode': LOC['postcode'], 'addressCountry': LOC['country']},
        'hasMap': LOC['maps_url'], 'sameAs': [FB],
        'openingHours': opening_hours(), 'openingHoursSpecification': opening_spec(),
        'areaServed': [{'@type': 'Place', 'name': c} for c in F['service_area']],
        'knowsAbout': [s['name'] for s in S.SERVICES],
        'contactPoint': {'@type': 'ContactPoint', 'telephone': F['whatsapp_e164'], 'contactType': 'customer service', 'availableLanguage': ['en', 'ms', 'zh']},
    }


def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': pabs(p)} for i, (n, p) in enumerate(items)]}


def faqld(faq):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}


def ld(graph):
    j = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
    return f'<script type="application/ld+json">{j}</script>'


# ---------- shared layout ----------
def nav():
    return [('services/', S.UI['nav_services']), ('about/', S.UI['nav_about']), ('articles/', S.UI['nav_articles']), ('contact/', S.UI['nav_contact'])]


def shield(cls, lazy=False):
    lz = ' loading="lazy"' if lazy else ''
    return f'<img class="{cls}" src="{u("images/logo-transparent.webp")}" width="488" height="412" alt="{E(S.UI["logo_alt"])}" decoding="async"{lz}>'


def head(title, desc, path, graph, hero=False):
    css_v = ver(os.path.join(OUT, 'assets', 'site.css'))
    rob = '<meta name="robots" content="noindex, nofollow">' if NOINDEX else ''
    pre = ''.join(f'<link rel="preload" as="image" href="{u("images/hx/sq-" + s + ".webp")}" type="image/webp" fetchpriority="high">\n' for s in HERO_TILES[:2]) if hero is True else ''
    if isinstance(hero, str) and hero in ENH:
        pre = (f'<link rel="preload" as="image" href="{u("images/hx/" + hero + "-l.webp")}" imagesrcset="{u("images/hx/" + hero + "-l.webp")} 1000w, '
               f'{img_full(hero)} 1600w" imagesizes="(max-width: 899px) 140vh, 100vw" type="image/webp" fetchpriority="high">')
    return f'''<!DOCTYPE html>
<html lang="{L['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{rob}
<link rel="canonical" href="{pabs(path)}">
{I18N.hreflang_links(absu, path)}
<meta name="theme-color" content="#111111">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(F['short'])}">
{I18N.og_locale_tags(L)}
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{shu(I18N.page_path(L, path))}">
<meta property="og:image" content="{shu('images/og.jpg') + '?v=3'}">
<meta property="og:image:secure_url" content="{shu('images/og.jpg') + '?v=3'}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(S.CAPTIONS['og'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{shu('images/og.jpg') + '?v=3'}">
<link rel="icon" type="image/png" sizes="512x512" href="{u('images/favicon-512.png')}">
<link rel="apple-touch-icon" href="{u('images/favicon-512.png')}">
<link rel="preload" as="font" type="font/woff2" href="{u('assets/fonts/oswald-var.woff2')}" crossorigin>
{pre}
<link rel="stylesheet" href="{u('assets/site.css')}?v={css_v}">
{ld(graph)}
</head>
<body class="l-{L['code']}">
<a class="skip" href="#main">{E(S.UI['skip'])}</a>
'''


def header(active='', path=''):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{pu(p)}"{cur if active == p else ""}>{E(n)}</a>' for p, n in nav())
    sheet = ''.join(f'<a href="{pu(p)}">{E(n)}</a>' for p, n in [('', S.UI['nav_home'])] + nav())
    svc = ''.join(f'<a href="{pu("services/" + s["slug"] + "/")}">{E(s["name"])}</a>' for s in S.SERVICES)
    return f'''<header class="hb">
<div class="hb-in">
<a class="hb-mark" href="{pu()}" aria-label="{E(S.UI['home_aria'])}">{shield('hb-shield')}<span class="hb-name">HX AUTO SERVICE<small>{E(S.UI['brand_line'])}</small></span></a>
<nav class="hb-nav" aria-label="{E(S.UI['aria_main'])}">{links}</nav>
{I18N.switcher(u, path, L, S.UI['lang_label'], 'ut')}
{wa('header', S.UI['wa_btn'], 'btn-wa sm hb-wa')}
<button class="hb-menu" type="button" aria-expanded="false" aria-controls="sheet" aria-label="{E(S.UI['menu'])}">{icon('menu')}</button>
</div>
</header>
<div class="sheet" id="sheet" hidden>
<div class="sheet-in">
<button class="sheet-x" type="button" aria-label="{E(S.UI['close'])}">{icon('x')}</button>
<nav class="sheet-nav" aria-label="{E(S.UI['aria_menu'])}">{sheet}</nav>
<nav class="sheet-svc" aria-label="{E(S.UI['nav_services'])}">{svc}</nav>
{I18N.switcher(u, path, L, S.UI['lang_label'], 'ut ut-lg')}
{wa('menu', S.UI['wa_btn_long'])}
</div>
</div>
'''


def hfmt(hm):
    h, m = map(int, hm.split(':'))
    h12 = h % 12 or 12
    if L['code'] == 'zh':
        return ('上午' if h < 12 else '下午' if h < 18 else '晚上') + f'{h12}:{m:02d}'
    if L['code'] == 'ms':
        return f'{h12}:{m:02d} ' + ('pagi' if h < 12 else 'petang' if h < 19 else 'malam')
    return f'{h12}:{m:02d}' + ('am' if h < 12 else 'pm')


def hours_table(cls='hrs'):
    rows = []
    for d, name in zip(DAYS, S.UI['days']):
        v = F['hours'][d]
        if v == 'closed':
            t = S.UI['closed']
        else:
            o, c = v.split('-')
            t = hfmt(o) + {'en': ' to ', 'ms': ' hingga ', 'zh': ' 至 '}[L['code']] + hfmt(c)
        hi = ' class="hi"' if d == 'thursday' else (' class="off"' if v == 'closed' else '')
        rows.append(f'<tr{hi}><th scope="row">{E(name)}</th><td>{E(t)}</td></tr>')
    return f'<table class="{cls}"><tbody>{"".join(rows)}</tbody></table>'


def footer():
    js_v = ver(os.path.join(OUT, 'assets', 'site.js'))
    cta_v = ver(os.path.join(OUT, 'p1-cta.js'))
    pages = ''.join(f'<a href="{pu(p)}">{E(n)}</a>' for p, n in [('', S.UI['nav_home'])] + nav() + [('privacy/', S.UI['privacy'])])
    svc = ''.join(f'<a href="{pu("services/" + s["slug"] + "/")}">{E(s["name"])}</a>' for s in S.SERVICES)
    return f'''<footer class="fb">
<div class="fb-in">
<div class="fb-brand">{shield('fb-shield', True)}<p class="fb-name">HX AUTO SERVICE <span>({E(F['company_no'])})</span></p><p class="fb-sub">{E(S.UI['brand_line'])}</p>
<address>{E(LOC['one_line'])}</address><p class="fb-hrs">{icon('clock')}<span>{E(S.UI['hours_short'])}</span></p></div>
<div class="fb-talk"><h2 class="fb-h">{E(S.UI['footer_talk'])}</h2>{wa('footer', S.UI['wa_btn_long'], 'lk')}{call('footer', S.UI['call_btn_long'], 'lk')}{fb('footer')}</div>
<div><h2 class="fb-h">{E(S.UI['nav_services'])}</h2><nav class="fb-nav" aria-label="{E(S.UI['nav_services'])}">{svc}</nav></div>
<div><h2 class="fb-h">{E(S.UI['footer_pages'])}</h2><nav class="fb-nav" aria-label="{E(S.UI['aria_pages'])}">{pages}</nav></div>
</div>
<div class="fb-base"><p>{E(S.UI['brands_note'])}</p><p class="credit"><a href="https://autoseo.my/">{S.UI['credit']}</a></p></div>
</footer>
<nav class="dock" aria-label="{E(S.UI['aria_contact'])}">{wa('mobile_bar', S.UI['wa_btn'])}{call('mobile_bar', S.UI['call_btn'])}</nav>
<dialog class="lb" id="lb" aria-label="{E(S.UI['aria_photo'])}"><button class="lb-x" type="button" aria-label="{E(S.UI['close'])}">{icon('x')}</button><img alt="" decoding="async"><p class="lb-c"></p></dialog>
<script src="{u('assets/site.js')}?v={js_v}" defer></script>
<script src="{u('p1-cta.js')}?v={cta_v}" defer></script>
</body>
</html>
'''


def page(path, title, desc, graph, body, active='', hero=False):
    return head(title, desc, path, graph, hero) + header(active, path) + f'<main id="main">{body}</main>\n' + footer()


# ---------- blocks ----------
def frame(stem, cls='ph', eager=False):
    w, h, fw, fh = PHOTOS[stem]
    cap = S.CAPTIONS[stem]
    lz = '' if eager else ' loading="lazy"'
    return (f'<figure class="{cls}"><button type="button" class="ph-b" data-full="{img_full(stem)}" data-w="{fw}" data-h="{fh}" '
            f'data-cap="{E(cap)}" aria-label="{E(S.UI["photo_open"])}: {E(cap)}"><img src="{img(stem)}" width="{w}" height="{h}" '
            f'alt="{E(cap)}" decoding="async"{lz}></button><figcaption>{E(cap)}</figcaption></figure>')


def carousel(stems, label):
    return (f'<div class="wr"><div class="wr-t" tabindex="0" role="region" aria-label="{E(label)}">'
            f'{"".join(frame(s, "ph wr-i") for s in stems)}</div>'
            f'<div class="wr-c"><button type="button" class="arr" data-dir="-1" aria-label="{E(S.UI["prev"])}">{icon("prev")}</button>'
            f'<div class="dots" aria-hidden="true">{"<i></i>" * len(stems)}</div>'
            f'<button type="button" class="arr" data-dir="1" aria-label="{E(S.UI["next"])}">{icon("next")}</button></div></div>')


# Car side view: front at the right. Zone markers sit on the part they name.
ZONE_XY = {'engine': (506, 116), 'battery': (548, 142), 'diagnostics': (404, 126), 'aircond': (338, 92),
           'brakes': (456, 172), 'tyres': (146, 172), 'suspension': (146, 120), 'undercarriage': (300, 192)}


def car_svg():
    marks = ''.join(f'<g class="zm" data-z="{z["id"]}" transform="translate({ZONE_XY[z["id"]][0]} {ZONE_XY[z["id"]][1]})">'
                    f'<circle class="zm-r" r="15"/><circle class="zm-d" r="5"/></g>' for z in S.ZONES)
    return f'''<svg class="car" viewBox="0 0 600 230" aria-hidden="true" focusable="false">
<line class="car-g" x1="20" y1="208" x2="580" y2="208"/>
<path class="car-b" d="M36 170V148Q38 128 64 122L160 110Q205 70 262 64H372Q420 66 462 104L534 116Q562 122 564 148V170H502A46 46 0 0 0 410 170H192A46 46 0 0 0 100 170Z"/>
<path class="car-w" d="M180 108Q212 80 262 75H306V108ZM318 75H368Q406 77 436 106L318 108Z"/>
<path class="car-l" d="M312 112V166M470 128H520M38 150H60"/>
<circle class="car-t" cx="146" cy="172" r="34"/><circle class="car-h" cx="146" cy="172" r="14"/>
<circle class="car-t" cx="456" cy="172" r="34"/><circle class="car-h" cx="456" cy="172" r="14"/>
{marks}
</svg>'''


def diagram():
    tabs = ''.join(f'<button type="button" class="zt" role="tab" id="zt-{z["id"]}" aria-controls="zp-{z["id"]}" aria-selected="{"true" if i == 0 else "false"}" data-z="{z["id"]}">{E(z["name"])}</button>'
                   for i, z in enumerate(S.ZONES))
    names = {s['slug']: s['name'] for s in S.SERVICES}
    panels = ''.join(f'<div class="zp" role="tabpanel" id="zp-{z["id"]}" aria-labelledby="zt-{z["id"]}" data-z="{z["id"]}"><h3>{E(z["name"])}</h3><p>{E(z["line"])}</p>'
                     f'<a class="zp-go" href="{pu("services/" + z["svc"] + "/")}">{E(names[z["svc"]])}{icon("go")}</a></div>' for z in S.ZONES)
    also = ''.join(f'<a href="{pu("services/" + s["slug"] + "/")}">{icon("oil" if s["id"] == "service-oil" else "tow")}<span>{E(s["name"])}</span></a>'
                   for s in S.SERVICES if s['id'] in ('service-oil', 'towing'))
    return (f'<div class="dg" data-zone="{S.ZONES[0]["id"]}"><div class="dg-car">{car_svg()}</div>'
            f'<div class="dg-ctl"><p class="dg-lab" id="zl">{E(S.UI["zones_label"])}</p><div class="zts" role="tablist" aria-labelledby="zl">{tabs}</div>'
            f'<div class="zps">{panels}</div><div class="dg-also"><p>{E(S.UI["also_label"])}</p>{also}</div></div></div>')


SVC_ICON = {'diagnostics': 'scan', 'service-oil': 'oil', 'engine-transmission': 'engine', 'aircond': 'snow',
            'brakes-suspension-tyres': 'disc', 'battery-electrical': 'battery', 'undercarriage': 'lift', 'towing': 'tow'}
# Home bento mosaic: 5 large 4:3 frames (the drop's suggested big tiles) and 8 4:5 tiles, all full colour.
MOSAIC = [('honda-jazz-engine', 'L'), ('bmw-5-series-engine', 's'), ('kia-cerato-on-lift', 's'),
          ('shopfront-forecourt', 'L'), ('mini-cooper-s-on-lift', 's'), ('land-rover-discovery-sport', 's'),
          ('mercedes-c-class-bay', 'L'), ('bmw-5-series-on-lift', 's'), ('mazda-3-engine', 's'),
          ('toyota-alphard-white', 'L'), ('toyota-vellfire-bay', 's'), ('amg-matte-card', 's'),
          ('aircond-flushing-banner', 'L')]
# Reviews: Google and Facebook snippets from facts.json, shown exactly as captured. No stars, no rating, never translated.
REVIEWS = R['snippets']


def services_grid():
    cards = ''.join(f'<li class="rv" style="--d:{i % 4}"><a class="sg" href="{pu("services/" + s["slug"] + "/")}"><span class="sg-i">{icon(SVC_ICON[s["id"]])}</span>'
                    f'<h3>{E(s["name"])}</h3><p>{E(s["home_line"])}</p><span class="sg-go"><span>{E(S.HOME["view"])}</span>{icon("go")}</span></a></li>'
                    for i, s in enumerate(S.SERVICES))
    return (f'<section class="sec lt"><div class="wrap"><div class="sec-h rv"><h2>{E(S.HOME["svc_h2"])}</h2><p>{E(S.HOME["svc_p"])}</p></div>'
            f'<ul class="sgs">{cards}</ul></div></section>')


def mosaic():
    tiles = []
    for i, (s, k) in enumerate(MOSAIC):
        cap = S.CAPTIONS.get(s) or S.CAPTIONS['mercedes-amg-matte']
        if s == 'amg-matte-card':
            src = u('images/hx/amg-matte-card.webp')
            tiles.append(f'<figure class="mt mt-s rv" style="--d:{i % 3}"><button type="button" class="ph-b" data-full="{src}" data-w="960" data-h="1200" '
                         f'data-cap="{E(cap)}" aria-label="{E(S.UI["photo_open"])}: {E(cap)}"><img src="{src}" width="960" height="1200" alt="{E(cap)}" loading="lazy" decoding="async"></button>'
                         f'<figcaption><span>{E(cap)}</span></figcaption></figure>')
            continue
        if k == 'L':
            pic = (f'<img src="{u("images/hx/" + s + "-l.webp")}" srcset="{u("images/hx/" + s + "-l.webp")} 1000w, {img_full(s)} 1600w" '
                   f'sizes="(min-width: 900px) 50vw, 100vw" width="1000" height="750" alt="{E(cap)}" loading="lazy" decoding="async">')
        else:
            pic = f'<img src="{img(s)}" width="720" height="900" alt="{E(cap)}" loading="lazy" decoding="async">'
        tiles.append(f'<figure class="mt mt-{k} rv" style="--d:{i % 3}"><button type="button" class="ph-b" data-full="{img_full(s)}" data-w="1600" data-h="1200" '
                     f'data-cap="{E(cap)}" aria-label="{E(S.UI["photo_open"])}: {E(cap)}">{pic}</button><figcaption><span>{E(cap)}</span></figcaption></figure>')
    brands = ''.join(f'<li>{E(b)}</li>' for b in F['brands_seen'])
    return (f'<section class="sec dk"><div class="wrap"><div class="sec-h rv"><h2>{E(S.HOME["mosaic_h2"])}</h2><p>{E(S.HOME["mosaic_p"])}</p></div>'
            f'<div class="bento">{"".join(tiles)}</div>'
            f'<h3 class="mk-h">{E(S.HOME["brands_label"])}</h3><ul class="mk">{brands}</ul></div></section>')


def steps_strip():
    ics = ['wa', 'scan', 'wrench']
    li = ''.join(f'<li class="st rv" style="--d:{i}"><span class="st-n">{i + 1}</span><span class="st-i">{icon(ics[i])}</span>'
                 f'<h3>{E(t)}</h3><p>{E(d)}</p></li>' for i, (t, d) in enumerate(S.HOME['steps']))
    return f'<section class="sec dk"><div class="wrap"><h2 class="rv">{E(S.HOME["steps_h2"])}</h2><ol class="sts">{li}</ol></div></section>'


def reviews_block(first_n=4):
    lang = '' if L['code'] == 'en' else ' lang="en"'
    src = lambda r: S.UI['review_src_google'] if r['src'] == 'google' else S.UI['review_src_facebook']
    card = lambda r, i: (f'<li class="qc rv" style="--d:{i % 2}"><blockquote{lang}><p>{E(r["text"])}</p></blockquote>'
                         f'<p class="qc-by"><span>{E(r["name"])}</span>{E(src(r))}</p></li>')
    first = ''.join(card(r, i) for i, r in enumerate(REVIEWS[:first_n]))
    rest = ''.join(card(r, i) for i, r in enumerate(REVIEWS[first_n:]))
    return (f'<section class="sec lt rvw"><div class="wrap"><h2 class="rv">{E(S.HOME["reviews_h2"])}</h2>'
            f'<ul class="qcs">{first}</ul><details class="more"><summary>{E(S.UI["more_reviews"])} ({len(REVIEWS) - first_n})</summary><ul class="qcs">{rest}</ul></details>'
            f'<p class="note">{E(S.UI["reviews_note"])}</p></div></section>')


def wa_band():
    return (f'<section class="band"><div class="wrap band-in"><div class="rv"><h2>{E(S.HOME["band_h2"])}</h2><p>{E(S.HOME["band_p"])}</p></div>'
            f'<p class="act rv">{wa("band", S.UI["wa_btn_long"])}</p></div></section>')


def faq_block(faq, h2, cls='sec dk chev'):
    items = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)
    return f'<section class="{cls}"><div class="wrap narrow"><h2>{E(h2)}</h2><div class="faq">{items}</div></div></section>'


def ask_block(place):
    return (f'<section class="sec dk ask"><div class="wrap"><h2>{E(S.UI["ask_title"])}</h2><p>{E(S.UI["ask_line"])}</p>'
            f'<div class="act">{wa(place, S.UI["wa_btn_long"])}{call(place, S.UI["call_btn_long"])}</div></div></section>')


def page_head(h1, lead, trail):
    bc = ''.join(f'<a href="{pu(p)}">{E(n)}</a><span aria-hidden="true">/</span>' for n, p in trail[:-1]) + f'<span>{E(trail[-1][0])}</span>'
    return (f'<section class="phd chev"><div class="wrap"><nav class="bc" aria-label="{E(S.UI["aria_breadcrumb"])}">{bc}</nav>'
            f'<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p></div></section>')


def find_block():
    """Find us: the one place on the home page with the opening hours, plus a lazy Google Maps embed (address search, no coordinates)."""
    return (f'<section class="sec lt"><div class="wrap find"><div class="find-x"><h2>{E(S.HOME["find_h2"])}</h2><p>{E(S.HOME["find_p"])}</p>'
            f'<figure class="shop"><img src="{sq("shopfront-signboard")}" width="480" height="480" alt="{E(S.HOME["shop_cap"])}" loading="lazy" decoding="async"></figure>'
            f'<address>{E(LOC["one_line"])}</address><p class="vlinks">{waze("home", "lk on-lt")}{gmap("home", "lk on-lt")}</p>'
            f'<div class="hbox"><h3>{icon("clock")}{E(S.HOME["hours_h"])}</h3>{hours_table()}</div></div>'
            f'<div class="map find-m"><iframe src="{E(LOC["maps_embed"])}" title="{E(S.UI["map_title"])}" loading="lazy" '
            f'referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></section>')


# ---------- pages ----------
HOME_TILES = {'diagnostics': 'bmw-5-series-on-lift', 'service-oil': 'honda-jazz-engine', 'engine-transmission': 'mazda-3-engine',
              'aircond': 'aircond-flushing-banner', 'brakes-suspension-tyres': 'mini-cooper-s-on-lift', 'battery-electrical': 'bmw-5-series-engine',
              'undercarriage': 'kia-cerato-on-lift', 'towing': 'toyota-vellfire-bay'}
# Round 3 (20 Nov): HX's camera is soft at the source, so no photo is ever shown large on the homepage.
# Everything is a 480x480 square thumbnail (sq-*), shown at 200 CSS px or less on a phone, 320px or less on desktop.
HERO_TILES = ['mercedes-c-class-bay', 'toyota-alphard-white', 'mazda-3-engine', 'shopfront-signboard', 'bmw-5-series-on-lift', 'mini-cooper-s-on-lift',
              'honda-jazz-engine', 'toyota-vellfire-bay', 'kia-cerato-on-lift']
SQ_ALL = ['mercedes-c-class-bay', 'toyota-alphard-white', 'mazda-3-engine', 'honda-jazz-engine', 'shopfront-signboard', 'aircond-flushing-banner',
          'bmw-5-series-on-lift', 'mini-cooper-s-on-lift', 'workshop-bays-overview', 'toyota-vellfire-bay', 'kia-cerato-on-lift',
          'land-rover-discovery-sport', 'bmw-5-series-engine', 'shopfront-forecourt']
BAY_GRID = ['mercedes-c-class-bay', 'toyota-alphard-white', 'mazda-3-engine', 'honda-jazz-engine', 'shopfront-forecourt', 'bmw-5-series-on-lift',
            'mini-cooper-s-on-lift', 'workshop-bays-overview', 'toyota-vellfire-bay', 'kia-cerato-on-lift', 'land-rover-discovery-sport', 'bmw-5-series-engine']
TRUST_IC = ['pin', 'clock', 'car', 'nav']


def sq(stem):
    return u(f'images/hx/sq-{stem}.webp')


def trust_strip():
    li = ''.join(f'<li>{icon(TRUST_IC[i])}<span>{E(x)}</span></li>' for i, x in enumerate(S.HOME['trust']))
    return f'<section class="trust" aria-label="{E(S.HOME["trust_label"])}"><ul class="wrap trust-in">{li}</ul></section>'


def service_tiles():
    T = S.HOME['tiles']
    tiles = []
    for i, s in enumerate(S.SERVICES):
        name, line = T[s['id']]
        tiles.append(f'<li class="tl"><a href="{pu("services/" + s["slug"] + "/")}"><img src="{sq(HOME_TILES[s["id"]])}" width="480" height="480" '
                     f'alt="" loading="lazy" decoding="async"><span class="tl-x"><span class="tl-i">{icon(SVC_ICON[s["id"]])}</span>'
                     f'<strong>{E(name)}</strong><span>{E(line)}</span></span></a></li>')
    an, al = S.HOME['all_tile']
    return (f'<section class="sec dk svs"><div class="wrap"><div class="sec-h rv"><h2>{E(S.HOME["svc_h2"])}</h2></div>'
            f'<ul class="tls">{"".join(tiles)}</ul>'
            f'<p class="tls-all"><a class="lk" href="{pu("services/")}"><span>{E(an)}</span>{icon("go")}</a></p></div></section>')


def bay_grid():
    tiles = []
    for s in BAY_GRID:
        cap = S.CAPTIONS[s]
        tiles.append(f'<li><button type="button" class="ph-b" data-full="{u("images/hx/" + s + "-l.webp")}" data-w="1000" data-h="750" '
                     f'data-cap="{E(cap)}" aria-label="{E(S.UI["photo_open"])}: {E(cap)}"><img src="{sq(s)}" width="480" height="480" alt="{E(cap)}" '
                     f'loading="lazy" decoding="async"></button></li>')
    brands = ''.join(f'<li>{E(b)}</li>' for b in F['brands_seen'])
    return (f'<section class="sec dk"><div class="wrap"><div class="sec-h rv"><h2>{E(S.HOME["mosaic_h2"])}</h2><p>{E(S.HOME["mosaic_p"])}</p></div>'
            f'<ul class="bay-g">{"".join(tiles)}</ul>'
            f'<h3 class="mk-h">{E(S.HOME["brands_label"])}</h3><ul class="mk">{brands}</ul></div></section>')


def hero_mosaic():
    tiles = ''.join(f'<li><img src="{sq(s)}" width="480" height="480" alt="{E(S.CAPTIONS[s])}" '
                    f'{"fetchpriority=\"high\" " if i < 2 else "loading=\"lazy\" "}decoding="async"></li>' for i, s in enumerate(HERO_TILES))
    pool = json.dumps([[sq(s), S.CAPTIONS[s]] for s in SQ_ALL], ensure_ascii=False)
    return f'<ul class="mz" data-pool="{E(pool)}">{tiles}</ul>'


def home():
    H = S.HOME
    logo = (f'<img class="hero-shield" src="{u("images/logo-transparent.webp")}" width="488" height="412" alt="{E(F["short"])}" decoding="async">')
    hero = f'''<section class="hero3">
<div class="wrap hero3-in">
{hero_mosaic()}
<div class="hero3-t">
{logo}
<h1>{E(H['h1'])}</h1>
<p class="hero-l">{E(H['hero_line'])}</p>
<div class="hero-cta">{wa('home_hero', S.UI['wa_btn'], 'btn-wa btn-red')}{call('home_hero', S.UI['call_btn'])}</div>
</div>
</div>
</section>'''
    body = (hero + trust_strip() + service_tiles() + bay_grid() + reviews_block() + steps_strip() + wa_band()
            + faq_block(S.FAQ_HOME, S.UI['faq_h2'], 'sec dk') + find_block())
    graph = [business(), {'@type': 'WebSite', 'name': F['short'], 'url': pabs(), 'inLanguage': L['hreflang']},
             {'@type': 'WebPage', 'name': H['title'], 'url': pabs(), 'inLanguage': L['hreflang'], 'about': {'@id': BIZ_ID}},
             faqld(S.FAQ_HOME)]
    return page('', H['title'], H['desc'], graph, body, '', True)


# Round 3: per-service media. Hero + strip use enhanced photos where we have them; makes come only from the cars in those photos.
SVC_MEDIA = {
    'diagnostics': ('bmw-5-series-engine', ['mini-cooper-s-on-lift', 'mercedes-c-class-bay', 'land-rover-discovery-sport', 'mazda-3-engine']),
    'service-oil': ('mercedes-c-class-bay', ['bmw-oil-and-filter', 'mercedes-oil-belt-parts', 'honda-jazz-engine', 'toyota-vellfire-bay']),
    'engine-transmission': ('mazda-3-engine', ['honda-jazz-engine', 'bmw-5-series-engine', 'nissan-coils-and-oil', 'toyota-alphard-white']),
    'aircond': ('aircond-flushing-banner', ['toyota-alphard-white', 'toyota-vellfire-bay', 'workshop-bays-overview', 'mercedes-c-class-bay']),
    'brakes-suspension-tyres': ('bmw-5-series-on-lift', ['kia-cerato-on-lift', 'subaru-coilover-service', 'mini-cooper-s-on-lift', 'land-rover-discovery-sport']),
    'battery-electrical': ('mini-cooper-s-on-lift', ['toyota-vellfire-bay', 'honda-jazz-engine', 'bmw-5-series-engine', 'toyota-alphard-white']),
    'undercarriage': ('land-rover-discovery-sport', ['kia-cerato-on-lift', 'nissan-qashqai-on-lift', 'mercedes-van-two-post', 'bmw-5-series-on-lift']),
    'towing': ('shopfront-forecourt', ['workshop-bays-overview', 'kia-cerato-on-lift', 'vellfire-on-lift-side', 'shopfront-signboard']),
}
STEM_MAKE = [('mercedes', 'Mercedes-Benz'), ('bmw', 'BMW'), ('alphard', 'Toyota Alphard'), ('vellfire', 'Toyota Vellfire'), ('honda', 'Honda'),
             ('kia', 'Kia'), ('mazda', 'Mazda'), ('mini', 'Mini'), ('subaru', 'Subaru'), ('nissan', 'Nissan'), ('land-rover', 'Land Rover')]
_COPY = {}


def svc_copy(sid):
    c = L['code']
    if c not in _COPY:
        _COPY[c] = json.load(open(os.path.join(HERE, 'copy', f'services_{c}.json'), encoding='utf8'))
    return _COPY[c][sid]


def svc_makes(stems):
    out = []
    for st in stems:
        for k, m in STEM_MAKE:
            if k in st and m not in out and m in F['brands_seen']:
                out.append(m)
    return out


def svc_hero_img(stem, eager=True):
    cap = S.CAPTIONS[stem]
    if stem in ENH:
        return (f'<img class="hero-img" src="{u("images/hx/" + stem + "-l.webp")}" srcset="{u("images/hx/" + stem + "-l.webp")} 1000w, {img_full(stem)} 1600w" '
                f'sizes="(max-width: 899px) 140vh, 100vw" width="1600" height="1200" alt="{E(cap)}" fetchpriority="high" decoding="async">')
    return f'<img class="hero-img" src="{img_full(stem)}" width="1600" height="1200" alt="{E(cap)}" fetchpriority="high" decoding="async">'


def service(s):
    C = svc_copy(s['id'])
    V = S.SVC_UI
    path = f'services/{s["slug"]}/'
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_services'], 'services/'), (s['name'], path)]
    pid = s['id'].replace('-', '_')
    hero_stem, strip = SVC_MEDIA[s['id']]
    bc = ''.join(f'<a href="{pu(p)}">{E(n)}</a><span aria-hidden="true">/</span>' for n, p in trail[:-1]) + f'<span>{E(trail[-1][0])}</span>'
    hero = (f'<section class="hero shero">{svc_hero_img(hero_stem)}<div class="wrap hero-in">'
            f'<nav class="bc" aria-label="{E(S.UI["aria_breadcrumb"])}">{bc}</nav>'
            f'<p class="hero-k">{E(s["name"])}</p><h1>{E(s["h1"])}</h1><p class="hero-l">{E(C["lead"])}</p>'
            f'<div class="hero-cta">{wa("service_" + pid, S.UI["wa_btn"])}{call("service_" + pid, S.UI["call_btn"])}</div></div></section>')
    signs = ''.join(f'<li class="rv" style="--d:{i % 3}">{E(x)}</li>' for i, x in enumerate(C['signs']))
    intro = (f'<section class="sec lt"><div class="wrap s2"><div class="rv"><h2>{E(V["intro_h2"])}</h2><p class="big">{E(C["intro"])}</p></div>'
             f'<div class="sbox rv"><h2>{E(V["signs_h2"])}</h2><ul class="signs">{signs}</ul></div></div></section>')
    steps = ''.join(f'<li class="pr rv" style="--d:{i % 3}"><span class="pr-n" aria-hidden="true">{i + 1:02d}</span><div><h3>{E(h)}</h3><p>{E(d)}</p></div></li>'
                    for i, (h, d) in enumerate(C['steps']))
    steps = f'<section class="sec dk"><div class="wrap"><h2 class="rv">{E(V["steps_h2"])}</h2><ol class="prs">{steps}</ol></div></section>'
    makes = svc_makes([hero_stem] + strip)
    checks = ''.join(f'<li>{E(x)}</li>' for x in C['checks'])
    mk = ''.join(f'<li>{E(m)}</li>' for m in makes)
    checks = (f'<section class="sec lt"><div class="wrap s2"><div class="rv"><h2>{E(V["checks_h2"])}</h2><ul class="cks">{checks}</ul></div>'
              f'<div class="rv"><h2>{E(V["makes_h2"])}</h2><ul class="mk mk-lt">{mk}</ul><p class="note">{E(V["makes_note"])}</p></div></div></section>')
    photos = (f'<section class="sec dk"><div class="wrap"><h2 class="rv">{E(V["photos_h2"])}</h2>'
              f'<div class="strip">{"".join(frame(x, "ph st4 rv") for x in strip)}</div></div></section>')
    band = (f'<section class="band"><div class="wrap band-in"><div class="rv"><h2>{E(V["band_h2"])}</h2><p>{E(V["band_p"])}</p></div>'
            f'<p class="act rv">{wa("service_" + pid + "_band", S.UI["wa_btn_long"])}</p></div></section>')
    faq = faq_block(C['faq'], S.UI['faq_h2'], 'sec lt')
    others = ''.join(f'<a href="{pu("services/" + o["slug"] + "/")}">{E(o["name"])}</a>' for o in S.SERVICES if o['id'] != s['id'])
    tail = (f'<section class="sec lt silver"><div class="wrap s2"><div><h2>{E(S.UI["related"])}</h2><nav class="rel" aria-label="{E(S.UI["related"])}">{others}</nav></div>'
            f'<div class="loc"><h2>{E(V["local_h2"])}</h2><p>{icon("pin")}<span>{E(V["local"])}</span></p>'
            f'<p class="vlinks">{waze("service_" + pid, "lk on-lt")}{gmap("service_" + pid, "lk on-lt")}</p></div></div></section>')
    body = hero + intro + steps + checks + photos + band + faq + tail
    graph = [business(), crumbs(trail),
             {'@type': 'Service', 'name': s['name'], 'serviceType': s['name'], 'description': s['desc'], 'url': pabs(path),
              'provider': {'@id': BIZ_ID}, 'areaServed': [{'@type': 'Place', 'name': c} for c in F['service_area']]},
             faqld(C['faq'])]
    return page(path, s['title'], s['desc'], graph, body, 'services/', hero_stem)


def services_index():
    X = S.SERVICES_INDEX
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_services'], 'services/')]
    cards = []
    for i, s in enumerate(S.SERVICES):
        st = SVC_MEDIA[s['id']][0]
        pic = (f'<img src="{u("images/hx/" + st + "-l.webp")}" width="1000" height="750" alt="{E(S.CAPTIONS[st])}" loading="lazy" decoding="async">'
               if st in ENH else f'<img src="{img(st)}" alt="{E(S.CAPTIONS[st])}" loading="lazy" decoding="async">')
        cards.append(f'<li class="rv" style="--d:{i % 2}"><a class="sx" href="{pu("services/" + s["slug"] + "/")}"><span class="sx-p">{pic}</span>'
                     f'<span class="sx-x"><span class="sx-i">{icon(SVC_ICON[s["id"]])}</span><h2>{E(s["name"])}</h2><p>{E(svc_copy(s["id"])["card"])}</p>'
                     f'<span class="sg-go"><span>{E(S.SVC_UI["index_more"])}</span>{icon("go")}</span></span></a></li>')
    body = (page_head(X['h1'], X['lead'], trail)
            + f'<section class="sec lt"><div class="wrap"><ul class="sxs">{"".join(cards)}</ul></div></section>'
            + f'<section class="sec lt silver"><div class="wrap">{diagram()}</div></section>'
            + ask_block('services'))
    graph = [business(), crumbs(trail), {'@type': 'ItemList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': s['name'], 'url': pabs('services/' + s['slug'] + '/')} for i, s in enumerate(S.SERVICES)]}]
    return page('services/', X['title'], X['desc'], graph, body, 'services/')


def about():
    X = S.ABOUT
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_about'], 'about/')]
    blocks = ''.join(f'<h2>{E(h)}</h2><p>{E(p)}</p>' for h, p in X['body'])
    sign = (f'<section class="sec dk chev"><div class="wrap"><h2 class="vh">{E(X["sign_h2"])}</h2><div class="sign"><p class="sign-a">HX AUTO SERVICE</p>'
            f'<p class="sign-b">PUSAT SERVIS KERETA</p><p class="sign-c">DIMILIKI OLEH: HX AUTO SERVICE ({E(F["company_no"])})</p></div></div></section>')
    body = (page_head(X['h1'], X['lead'], trail) + sign
            + f'<section class="sec lt"><div class="wrap split"><div class="prose">{blocks}</div>'
            + f'<div class="media"><div class="gal">{frame("shopfront-forecourt")}{frame("workshop-bays-overview")}</div></div></div></section>'
            + reviews_block() + ask_block('about'))
    graph = [business(), crumbs(trail), {'@type': 'AboutPage', 'name': X['title'], 'url': pabs('about/'), 'about': {'@id': BIZ_ID}}]
    return page('about/', X['title'], X['desc'], graph, body, 'about/')


def contact():
    X = S.CONTACT
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_contact'], 'contact/')]
    body = (page_head(X['h1'], X['lead'], trail)
            + f'''<section class="sec lt"><div class="wrap split">
<div class="prose"><h2>{E(X['wa_h'])}</h2><p class="num"><a href="{TEL}" data-cta="call_contact_number" data-ref="call_contact_number">{E(F['whatsapp_display'])}</a></p>
<p>{E(X['wa_p'])}</p><div class="act">{wa('contact', S.UI['wa_btn_long'], 'btn-wa on-lt')}{call('contact', S.UI['call_btn'], 'btn-call on-lt')}</div>
<p class="vlinks">{fb('contact', None, 'lk on-lt')}</p>
<h2>{E(X['addr_h'])}</h2><address>{E(LOC['one_line'])}</address><p class="vlinks">{waze('contact', 'lk on-lt')}{gmap('contact', 'lk on-lt')}</p></div>
<div class="hbox"><h2>{E(X['hours_h'])}</h2>{hours_table()}<p class="note">{E(X['hours_p'])}</p></div>
</div></section>
<section class="sec dk"><div class="wrap"><h2>{E(X['map_h'])}</h2><div class="map"><iframe src="{E(LOC['maps_embed'])}" title="{E(S.UI['map_title'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
<p class="vlinks">{gmap('contact_map')}{waze('contact_map')}</p></div></section>''')
    graph = [business(), crumbs(trail), {'@type': 'ContactPage', 'name': X['title'], 'url': pabs('contact/'), 'about': {'@id': BIZ_ID}}]
    return page('contact/', X['title'], X['desc'], graph, body, 'contact/')


def privacy():
    X = S.PRIVACY
    trail = [(S.UI['nav_home'], ''), (S.UI['privacy'], 'privacy/')]
    blocks = ''.join(f'<h2>{E(h)}</h2><p>{E(p)}</p>' for h, p in X['body'])
    body = page_head(X['h1'], S.UI['last_updated'], trail) + f'<section class="sec lt"><div class="wrap narrow prose">{blocks}</div></section>'
    return page('privacy/', X['title'], X['desc'], [business(), crumbs(trail)], body)


def articles():
    X = S.ARTICLES
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_articles'], 'articles/')]
    body = (page_head(X['h1'], X['lead'], trail)
            + '<section class="sec lt"><div class="wrap"><div class="art-list" id="articles"></div></div></section>' + ask_block('articles'))
    graph = [business(), crumbs(trail), {'@type': 'CollectionPage', 'name': X['title'], 'url': pabs('articles/'), 'inLanguage': L['hreflang']}]
    return page('articles/', X['title'], X['desc'], graph, body, 'articles/')


def build():
    global S, L
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, 'assets', 'fonts'))
    for f in ('site.css', 'site.js'):
        shutil.copy(os.path.join(HERE, 'assets', f), os.path.join(OUT, 'assets', f))
    for f in os.listdir(os.path.join(HERE, 'assets', 'fonts')):
        shutil.copy(os.path.join(HERE, 'assets', 'fonts', f), os.path.join(OUT, 'assets', 'fonts', f))
    # Web sizes of the enhanced photo set (made from the drop originals in images/hd/ on the server; see ENH).
    shutil.copytree(os.path.join(HERE, 'images', 'hx'), os.path.join(OUT, 'images', 'hx'))
    shutil.copy(os.path.join(HERE, 'images', 'og.jpg'), os.path.join(OUT, 'images', 'og.jpg'))
    shutil.copy(os.path.join(HERE, 'p1-cta.js'), os.path.join(OUT, 'p1-cta.js'))
    names = [n for n in dir(strings_en) if n.isupper()]
    missing = [f'{c}: {n}' for c, mod in STRINGS.items() for n in names if not hasattr(mod, n)]
    for n in ('UI', 'CAPTIONS', 'HOME'):
        missing += [f'{c}: {n}.{k}' for c, mod in STRINGS.items() for k in getattr(strings_en, n) if k not in getattr(mod, n, {})]
    if missing:
        sys.exit('strings files are missing keys: ' + ', '.join(missing))
    built, en_paths = [], []
    for L in I18N.LANGS:
        S = STRINGS[L['code']]
        pages = {'': home(), 'services/': services_index(), 'about/': about(), 'contact/': contact(), 'privacy/': privacy(), 'articles/': articles()}
        for s in S.SERVICES:
            pages[f'services/{s["slug"]}/'] = service(s)
        for p, h in pages.items():
            d = os.path.join(OUT, I18N.page_path(L, p))
            os.makedirs(d, exist_ok=True)
            depth = I18N.page_path(L, p).count('/')
            h = h.replace('@@B@@/', '../' * depth if depth else './')
            open(os.path.join(d, 'index.html'), 'w', encoding='utf8').write(h)
            built.append(I18N.page_path(L, p))
        if L is I18N.DEFAULT:
            en_paths = list(pages)
    S, L = strings_en, I18N.DEFAULT
    twins = I18N.check_twins(set(built))
    if twins:
        sys.exit('language twins missing: ' + ', '.join(twins))
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf8').write(I18N.sitemap_xml(absu, en_paths, F['updated']))
    svc = '\n'.join(f'- [{s["name"]}]({absu("services/" + s["slug"] + "/")}): {s["card_line"]}' for s in S.SERVICES)
    hrs = '; '.join(f"{d.title()} {F['hours'][d]}" for d in DAYS)
    llms = f"""# {F['name']}

> {F['category']} (Pusat Servis Kereta) in Taman Bukit Indah, Iskandar Puteri, Johor Bahru, Malaysia, close to the Second Link. Company no. {F['company_no']}.

- Address: {LOC['one_line']}
- WhatsApp and phone: {F['whatsapp_display_intl']} ({F['whatsapp_url']})
- Opening hours (Google): {hrs}
- Facebook: {FB}
- Waze: {LOC['waze']} / Google Maps: {LOC['maps_url']}
- Makes seen in the workshop: {', '.join(F['brands_seen'])}
- Areas: {', '.join(F['service_area'])}

## Services
{svc}

## Languages
English at the site root, Bahasa Melayu at /ms/, Simplified Chinese at /zh/. Every page exists in all three.

## Pages
""" + '\n'.join(f'- {absu(p)} (BM: {absu("ms/" + p)}, 中文: {absu("zh/" + p)})' for p in en_paths) + '\n'
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf8').write(llms)
    open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {absu("sitemap.xml")}\n')
    print(f'built {len(built)} pages ({len(en_paths)} x {len(I18N.LANGS)} languages) -> {os.path.abspath(OUT)} (base {SITE})')


if __name__ == '__main__':
    build()
