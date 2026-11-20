#!/usr/bin/env python3
"""MCS Auto Spray Painting site builder (AutoSEO.my client preview, 20 Nov 2026).
One template set for every page: head, header, menu sheet, footer, mobile bar, CTA links and schema live here once,
so one edit updates every page in every language. Facts: facts.json. Copy: strings_en/ms/zh.py (same keys).
Language plumbing (switcher, hreflang, og:locale, sitemap) comes from the shared template ../../../autoseo-template/autoseo_i18n.py.
  python3 build.py               -> build for https://autoseo.my/preview/mcs-auto-spray-painting/
  python3 build.py --live DOMAIN -> same files for https://DOMAIN/ (unified go-live: the domain will point at the preview folder)
  python3 build.py --fonts       -> also re-subset the Chinese font from assets/fonts-src/NotoSansSC.ttf
No per-page robots meta: the preview host sends X-Robots-Tag noindex from preview/.htaccess (host-based), so nothing has to be
stripped at go-live. Then python3 check.py (pre-upload gate) before the Bridge upload
(sync_from_github, site autoseo, base_path preview/mcs-auto-spray-painting, source dist/)."""
import hashlib, html, json, os, re, shutil, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'autoseo-template'))
import autoseo_i18n as I18N
import strings_en, strings_ms, strings_zh
STRINGS = {'en': strings_en, 'ms': strings_ms, 'zh': strings_zh}
S, L = strings_en, I18N.LANGS[0]

F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
if '--live' in sys.argv:
    ORIGIN, BASE = 'https://' + sys.argv[sys.argv.index('--live') + 1], '/'
else:
    ORIGIN, BASE = F['preview']['origin'], F['preview']['base_path']
SITE = ORIGIN + BASE
OUT = os.path.join(HERE, '..', 'dist')
E = html.escape
LK = F['links']
TODAY = '2026-11-20'
NAME = F['name']

# Media. 'repo' files ship from src/media (web sizes made from the drop); 'server' files were placed from Bridge drop
# 6affcf1fb3066edc1e6030f5 straight into the preview folder's media/ (sha256 kept so check.py can trust them).
MEDIA = {
    'cover':             ('cover-960.webp', 960, 540, '50% 45%'),
    'cover-xl':          ('cover.webp', 1600, 900, '50% 45%'),
    'og':                ('og.jpg', 1200, 630, ''),
    'logo':              ('logo-220.webp', 220, 168, ''),
    'logo-xl':           ('logo-transparent.png', 794, 606, ''),
    'favicon':           ('favicon-32.png', 32, 32, ''),
    'touch':             ('apple-touch-icon.png', 180, 180, ''),
    'favicon-512':       ('favicon-512.png', 512, 512, ''),
    'signboard':         ('signboard-760.webp', 760, 485, '50% 55%'),
    'shopfront-booth':   ('shopfront-booth-760.webp', 640, 760, '50% 28%'),
    'vellfire-front':    ('vellfire-front-760.webp', 570, 760, '50% 52%'),
    'vellfire-rear':     ('vellfire-rear-760.webp', 570, 760, '50% 55%'),
    'vellfire-unit-57':  ('vellfire-unit-57-760.webp', 570, 760, '50% 50%'),
    'vellfire-booth':    ('vellfire-booth-760.webp', 379, 760, '50% 42%'),
    'handover':          ('handover-760.webp', 760, 759, '50% 50%'),
    'mclaren-shopfront': ('mclaren-shopfront-760.webp', 760, 690, '62% 48%'),
    'lotus-booth':       ('lotus-booth-760.webp', 611, 760, '50% 60%'),
    'panels-booth':      ('panels-booth-760.webp', 760, 359, '50% 45%'),
    'motorbike':         ('motorbike-760.webp', 428, 760, '50% 50%'),
    'upholstery-bay':    ('upholstery-bay-760.webp', 428, 760, '50% 55%'),
    'door-panel':        ('door-panel-760.webp', 760, 428, '50% 45%'),
    'seats':             ('seats-760.webp', 428, 760, '50% 45%'),
}
SERVER_MEDIA = {  # placed by Bridge drop_publish 20 Nov 2026
    'media/cover.webp': 'd451b9b28fef0fbc87cfffafc3ab300bf34740a7fc1db4bfd601fd336f3c0bbb',
    'media/og.jpg': '2eea8d83edbee5c3d8efbba3d3a1ac30ebfa9311726ea95d03847cc9760d71b8',
    'media/logo-transparent.png': 'ed9b4a95881b99ff2b68164aaec3d5ce49bd4b826f50f1caf5452d84935b13f6',
    'media/favicon-512.png': '85bae8fe99f422e5791e5fa564365deea83774ea5b842088a4b638dab0299255',
}

SVC_PATH = {'spray-painting': 'services/spray-painting/', 'custom-colour': 'services/custom-colour/',
            'body-repair': 'services/accident-body-repair/', 'paint-protection': 'services/nippon-ai-pps-paint-protection/',
            'rims-calipers-engine': 'services/rims-calipers-engine-bay/', 'interior-repair': 'services/interior-repair-reupholstery/',
            'carbon-bodykits': 'services/carbon-fibre-body-kits/', 'insurance-windscreen': 'services/insurance-windscreen-claims/',
            'motorbike': 'services/motorbike-spray/'}
SVC_PHOTOS = {  # real photos per service (facts.json services[].photos); first = zone + page photo
    'spray-painting': ['panels-booth', 'shopfront-booth', 'vellfire-booth', 'mclaren-shopfront'],
    'custom-colour': ['vellfire-front', 'vellfire-rear', 'vellfire-booth', 'handover'],
    'body-repair': ['shopfront-booth', 'panels-booth', 'vellfire-booth'],
    'paint-protection': ['vellfire-rear', 'vellfire-front'],
    'rims-calipers-engine': ['mclaren-shopfront', 'vellfire-front'],
    'interior-repair': ['seats', 'door-panel', 'upholstery-bay'],
    'carbon-bodykits': ['lotus-booth', 'mclaren-shopfront'],
    'insurance-windscreen': ['vellfire-unit-57', 'shopfront-booth'],
    'motorbike': ['motorbike', 'upholstery-bay'],
}
SWATCH = ['#48A6CA', '#EC060E', '#C5C8CC']
GALLERY = ['vellfire-front', 'mclaren-shopfront', 'lotus-booth', 'vellfire-booth', 'vellfire-rear', 'panels-booth', 'handover', 'vellfire-unit-57']
PAGES = ['', 'services/'] + [SVC_PATH[k] for k in strings_en.SERVICE_ORDER] + ['about/', 'contact/', 'articles/', 'privacy/']
NAV = [('services/', 'services'), ('about/', 'about'), ('contact/', 'contact')]


def u(p=''):
    return BASE + p


def absu(p=''):
    return SITE + p


def pu(p=''):
    return u(I18N.page_path(L, p))


def pabs(p=''):
    return absu(I18N.page_path(L, p))


def ver(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]


def murl(stem):
    return u('media/' + MEDIA[stem][0])


def mabs(stem):
    return absu('media/' + MEDIA[stem][0])


def wa_url(key='default'):
    return f"{F['whatsapp']['url']}?text={urllib.parse.quote(S.PREFILL[key])}"


def icon(name):
    p = {
        'wa': '<path d="M4.6 19.4l1.1-3.5a7.9 7.9 0 1 1 2.9 2.7z"/><path d="M9.3 8.7c.3 2.5 2.3 4.7 5 5.2l.9-1.1 1.8.8-.3 1.5c-3.8.4-7.7-3.5-7.5-7.3l1.5-.3.8 1.7z"/>',
        'call': '<path d="M5.2 4h3.6l1.6 4-2.1 1.3a10.6 10.6 0 0 0 6.4 6.4l1.3-2.1 4 1.6v3.6a1.6 1.6 0 0 1-1.7 1.6C10.4 19.9 4.1 13.6 3.6 5.7A1.6 1.6 0 0 1 5.2 4z"/>',
        'pin': '<path d="M12 21s-6.4-5.5-6.4-10.9a6.4 6.4 0 0 1 12.8 0C18.4 15.5 12 21 12 21z"/><circle cx="12" cy="10.1" r="2.2"/>',
        'mail': '<rect x="3.5" y="6" width="17" height="12" rx="2"/><path d="M4 7.5l8 5.5 8-5.5"/>',
        'menu': '<path d="M4 8h16M4 16h16"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
        'prev': '<path d="M15 5l-7 7 7 7"/>', 'next': '<path d="M9 5l7 7-7 7"/>', 'go': '<path d="M5 12h13M13 6l6 6-6 6"/>',
        'tick': '<path d="M5 12.5l4.2 4.2L19 7"/>', 'ext': '<path d="M14 5h5v5M19 5l-8 8"/><path d="M18 14v4.5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 4 18.5v-11A1.5 1.5 0 0 1 5.5 6H10"/>', 'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'


# ---------- CTA links (data-cta = data-ref = placement; the Controller reads the whatsapp_/call_/email_/map_/facebook_ prefix) ----------
def wa(place, key='default', label=None, cls='go-wa'):
    return (f'<a class="{cls}" href="{E(wa_url(key))}" target="_blank" rel="noopener" data-cta="whatsapp_{place}" data-ref="whatsapp_{place}">'
            f'{icon("wa")}<span>{E(label or S.UI["wa_btn"])}</span></a>')


def call(place, label=None, cls='go-call'):
    return (f'<a class="{cls}" href="{F["phone"]["tel"]}" data-cta="call_{place}" data-ref="call_{place}">'
            f'{icon("call")}<span>{E(label or S.UI["call_btn"])}</span></a>')


def ext(kind, place, href, label, cls=None, ic=None):
    c = f' class="{cls}"' if cls else ''
    return (f'<a{c} href="{E(href)}" target="_blank" rel="noopener" data-cta="{kind}_{place}" data-ref="{kind}_{place}">'
            f'{icon(ic) if ic else ""}<span>{E(label)}</span></a>')


def mail(place, cls=None):
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="mailto:{F["email"]}" data-cta="email_{place}" data-ref="email_{place}">{icon("mail")}<span>{E(F["email"])}</span></a>'


def img(stem, alt, eager=False, cls=None, sizes=None):
    f, w, h, pos = MEDIA[stem]
    c = f' class="{cls}"' if cls else ''
    st = f' style="object-position:{pos}"' if pos else ''
    load = ' fetchpriority="high"' if eager == 'high' else ('' if eager else ' loading="lazy"')
    return f'<img{c} src="{murl(stem)}" width="{w}" height="{h}" alt="{E(alt)}"{st}{load} decoding="async">'


def logo():
    return (f'<img class="shield" src="{murl("logo")}" width="220" height="168" alt="" decoding="async">'
            f'<span class="wm-t">MCS <b>Auto Spray Painting</b></span>')


# ---------- head / header / footer ----------
def head(path, title, meta, ld):
    css = os.path.join(HERE, 'assets', 'site.css')
    zh = L['code'] == 'zh'
    font = (f'<link rel="preload" href="{u("assets/fonts/notosanssc-sub.woff2")}" as="font" type="font/woff2" crossorigin>' if zh else
            f'<link rel="preload" href="{u("assets/fonts/urbanist.woff2")}" as="font" type="font/woff2" crossorigin>')
    hero = ''
    if path == '':
        hero = (f'<link rel="preload" as="image" href="{murl("cover")}" media="(max-width: 759px)" fetchpriority="high">'
                f'<link rel="preload" as="image" href="{murl("cover-xl")}" media="(min-width: 760px)" fetchpriority="high">')
    ldj = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="{L['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(meta)}">
<link rel="canonical" href="{pabs(path)}">
{I18N.hreflang_links(absu, path)}
<meta name="theme-color" content="#0D0E10">
<link rel="icon" href="{murl('favicon')}" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{murl('touch')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(NAME)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta)}">
<meta property="og:url" content="{pabs(path)}">
<meta property="og:image" content="{mabs('og')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(S.PHOTOS['cover'])}">
{I18N.og_locale_tags(L)}
<meta name="twitter:card" content="summary_large_image">
{font}{hero}
<link rel="stylesheet" href="{u('assets/site.css')}?v={ver(css)}">
{ldj}
</head>'''


def header(path):
    def cur(p):
        return ' aria-current="page"' if (path == p or (p == 'services/' and path.startswith('services/'))) else ''
    nav = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in NAV)
    sheet = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in [('', 'home')] + NAV + [('articles/', 'articles')])
    svc = ''.join(f'<a href="{pu(SVC_PATH[k])}">{E(S.SERVICES[k]["zone"])}</a>' for k in S.SERVICE_ORDER)
    return f'''<body class="lang-{L['code']}">
<a class="skip" href="#main">{E(S.UI['skip'])}</a>
<header class="top"><div class="wrap">
<a class="brand" href="{pu('')}" aria-label="{E(NAME)}">{logo()}</a>
<nav class="nav" aria-label="{E(S.UI['menu'])}">{nav}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='lang')}
{wa('header', label=S.UI['wa_short'], cls='go-wa sm hdr-wa')}
<button class="mb" type="button" aria-expanded="false" aria-controls="sheet" aria-label="{E(S.UI['menu'])}">{icon('menu')}</button>
</div></header>
<div class="sheet" id="sheet" hidden><div class="sheet-in" role="dialog" aria-modal="true" aria-label="{E(S.UI['menu'])}">
<button class="sheet-x" type="button" aria-label="{E(S.UI['close'])}">{icon('x')}</button>
<nav class="sheet-nav" aria-label="{E(S.UI['menu'])}">{sheet}</nav>
<nav class="sheet-svc" aria-label="{E(S.UI['services'])}">{svc}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='lang')}
<div class="sheet-cta">{wa('menu')}{call('menu')}</div>
</div></div>
<main id="main">'''


def hours_table(cls='hrs'):
    rows = ''.join(f'<tr{" class=\"off\"" if v == S.UI["closed"] else ""}><th scope="row">{E(d)}</th><td class="num">{E(v)}</td></tr>' for d, v in S.HOURS)
    return f'<table class="{cls}"><tbody>{rows}</tbody></table>'


def footer():
    a = F['address']
    lines = '<br>'.join(E(x) for x in a['lines'])
    svc = ''.join(f'<li><a href="{pu(SVC_PATH[k])}">{E(S.SERVICES[k]["zone"])}</a></li>' for k in S.SERVICE_ORDER)
    return f'''</main>
<footer class="ft"><div class="wrap">
<div class="ft-g">
<div class="ft-id">
<a class="brand" href="{pu('')}" aria-label="{E(NAME)}">{logo()}</a>
<p class="ft-tag">{E(S.UI['tagline'])}</p>
<address>{lines}</address>
</div>
<div><h2>{E(S.UI['hours_h'])}</h2>{hours_table('hrs ft-hrs')}</div>
<div><h2>{E(S.UI['contact_h'])}</h2><ul class="ft-l">
<li>{wa('footer', label='WhatsApp ' + F['whatsapp']['display'], cls='fl')}</li>
<li>{call('footer', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='fl')}</li>
<li>{mail('footer', cls='fl')}</li>
<li>{ext('facebook', 'footer', LK['facebook'], S.UI['facebook'], cls='fl', ic='ext')}</li>
<li>{ext('map', 'footer', LK['maps'], S.UI['maps'], cls='fl', ic='pin')}</li>
<li>{ext('youtube', 'footer', LK['youtube'], S.UI['youtube'], cls='fl', ic='ext')}</li>
</ul></div>
<div><h2>{E(S.UI['services'])}</h2><ul class="ft-s">{svc}</ul></div>
</div>
<div class="ft-b"><span>&copy; 2026 {E(NAME)}</span><a href="{pu('about/')}">{E(S.UI['about'])}</a><a href="{pu('articles/')}">{E(S.UI['articles'])}</a><a href="{pu('privacy/')}">{E(S.UI['privacy'])}</a><a href="https://autoseo.my/">Website by AutoSEO.my</a></div>
</div></footer>
<div class="mbar">{wa('mobile_bar', label=S.UI['wa_short'])}{call('mobile_bar', label=S.UI['call_short'])}</div>
<script src="{u('assets/site.js')}?v={ver(os.path.join(HERE, 'assets', 'site.js'))}" defer></script>
<script src="{u('p1-cta.js')}?v={ver(os.path.join(HERE, 'p1-cta.js'))}" defer></script>
</body>
</html>
'''


# ---------- schema (one facts file; no aggregateRating) ----------
def org_ld():
    a = F['address']
    d = {
        '@context': 'https://schema.org', '@type': ['AutoRepair', 'AutoBodyShop'], '@id': SITE + '#business',
        'name': NAME, 'alternateName': ['MCS Body & Paint', 'MCS Auto Spray Painting (' + F['signboard_malay'] + ')'],
        'description': S.SCHEMA['description'], 'url': pabs(''), 'inLanguage': L['hreflang'],
        'telephone': F['phone']['e164'], 'email': F['email'],
        'image': mabs('og'), 'logo': absu('media/' + MEDIA['logo-xl'][0]),
        'address': {'@type': 'PostalAddress', 'streetAddress': a['street'], 'addressLocality': a['city'], 'postalCode': a['postcode'],
                    'addressRegion': a['region'], 'addressCountry': a['country']},
        'geo': {'@type': 'GeoCoordinates', 'latitude': F['geo']['lat'], 'longitude': F['geo']['lng']},
        'hasMap': LK['maps'],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': h['days'], 'opens': h['opens'], 'closes': h['closes']} for h in F['hours']],
        'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': F['whatsapp']['e164'], 'url': F['whatsapp']['url'],
                          'availableLanguage': ['en', 'ms', 'zh']}],
        'sameAs': [LK['facebook'], LK['youtube'], LK['maps_cid']],
        'areaServed': [{'@type': 'Place', 'name': n} for n in F['areas']],
        'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': S.SERVICES[k]['h1'], 'url': pabs(SVC_PATH[k])}} for k in S.SERVICE_ORDER],
    }
    return d


def crumb_ld(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': pabs(p)} for i, (p, n) in enumerate(trail)]}


def service_ld(k):
    s = S.SERVICES[k]
    return {'@context': 'https://schema.org', '@type': 'Service', 'name': s['h1'], 'description': s['meta'], 'url': pabs(SVC_PATH[k]),
            'provider': {'@id': SITE + '#business'}, 'areaServed': [{'@type': 'Place', 'name': n} for n in F['areas']],
            'image': absu('media/' + MEDIA[SVC_PHOTOS[k][0]][0])}


def crumb_html(trail):
    li = ''.join(f'<li><a href="{pu(p)}"{" aria-current=\"page\"" if i == len(trail) - 1 else ""}>{E(n)}</a></li>' for i, (p, n) in enumerate(trail))
    return f'<nav class="crumb" aria-label="{E(S.UI["breadcrumb"])}"><ol>{li}</ol></nav>'


# ---------- blocks ----------
def hero():
    H = S.HOME
    cx, cw, ch, pos = MEDIA['cover-xl']
    chips = ''.join(f'<li><i style="--c:{c["hex"]}"></i>{E(S.CHIPS[c["key"]])}</li>' for c in F['chips'])
    return f'''<section class="hero">
<picture class="hero-ph"><source media="(min-width: 760px)" srcset="{murl('cover-xl')}" width="{cw}" height="{ch}">{img('cover', S.PHOTOS['cover'], eager='high')}</picture>
<div class="wrap hero-in">
<h1>{E(H['h1'])}</h1>
<ul class="chips" aria-label="{E(H['chips_label'])}">{chips}</ul>
<div class="hero-cta">{wa('home_hero')}{call('home_hero', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='go-line')}</div>
</div></section>'''


def promise():
    H = S.HOME
    return f'''<section class="band lt curve" id="studio"><div class="wrap split">
<div class="prose"><h2>{E(H['promise_h'])}</h2>{''.join(f'<p>{E(p)}</p>' for p in H['promise'])}
<p class="tag-line"><span>{E(S.UI['tagline'])}</span></p></div>
<figure class="frame tall">{img('vellfire-booth', S.PHOTOS['vellfire-booth'])}<figcaption>{E(S.PHOTOS['vellfire-booth'])}</figcaption></figure>
</div></section>'''


def zones(place, heading=True):
    tabs, panels = [], []
    for i, k in enumerate(S.SERVICE_ORDER):
        s = S.SERVICES[k]
        on = i == 0
        tabs.append(f'<button type="button" role="tab" id="zt-{k}" aria-controls="zp-{k}" aria-selected="{"true" if on else "false"}"{"" if on else " tabindex=\"-1\""}>'
                    f'<i style="--c:{SWATCH[i % 3]}"></i>{E(s["zone"])}</button>')
        ph = SVC_PHOTOS[k][0]
        panels.append(f'''<article class="zp{' on' if on else ''}" id="zp-{k}" role="tabpanel" aria-labelledby="zt-{k}">
<figure class="zp-ph">{img(ph, S.PHOTOS[ph])}</figure>
<div class="zp-tx"><h3>{E(s['h1'])}</h3><p>{E(s['short'])}</p><p class="zp-l">{E(s['lead'])}</p>
<div class="zp-a"><a class="more" href="{pu(SVC_PATH[k])}">{E(S.UI['see_service'])}</a>{wa(f'{place}_zone_{k}', k, label=S.UI['wa_short'], cls='go-wa sm')}</div></div>
</article>''')
    h = f'<div class="sec-h"><h2>{E(S.HOME["zones_h"])}</h2><p>{E(S.HOME["zones_p"])}</p></div>' if heading else ''
    return f'''<section class="band dk" id="zones"><div class="wrap">{h}
<div class="zones"><div class="zt" role="tablist" aria-label="{E(S.UI['zones_label'])}">{''.join(tabs)}</div>
<div class="zps">{''.join(panels)}</div></div>
</div></section>'''


def booth(compact=False):
    st = ''.join(f'<li><span class="tape" aria-hidden="true">{i + 1}</span><h3>{E(a)}</h3><p>{E(b)}</p></li>' for i, (a, b) in enumerate(S.STEPS))
    h = f'<div class="sec-h"><h2>{E(S.HOME["process_h"])}</h2><p>{E(S.HOME["process_p"])}</p></div>'
    return f'''<section class="band sv curve{' cp' if compact else ''}" id="process"><div class="wrap">{h}
<ol class="booth">{st}</ol></div></section>'''


def gallery(place):
    figs = ''.join(f'<li><figure>{img(s, S.PHOTOS[s])}<figcaption>{E(S.PHOTOS[s])}</figcaption></figure></li>' for s in GALLERY)
    G = S.HOME
    return f'''<section class="band dk" id="finished"><div class="wrap">
<div class="sec-h"><h2>{E(G['proof_h'])}</h2></div>
<div class="proof"><p class="rate"><b class="num">{F['reviews']['google_rating']}</b><span>{E(G['proof_line'])}</span></p>
<p class="themes">{E(G['proof_themes'])}</p>{ext('reviews', place, LK['maps'], S.UI['reviews'], cls='more')}</div>
</div>
<div class="gl" aria-label="{E(S.UI['gallery_label'])}" role="region"><ul class="glide" data-speed="0.035">{figs}</ul>
<div class="wrap gl-c"><button type="button" class="arr" data-dir="-1" aria-label="{E(S.UI['prev'])}">{icon('prev')}</button><button type="button" class="arr" data-dir="1" aria-label="{E(S.UI['next'])}">{icon('next')}</button></div></div>
</section>'''


def visit(place):
    H = S.HOME
    a = F['address']
    return f'''<section class="band lt curve" id="visit"><div class="wrap split rev">
<figure class="frame tall">{img('shopfront-booth', S.PHOTOS['shopfront-booth'])}</figure>
<div><h2>{E(H['hours_h'])}</h2><p class="addr">{icon('pin')}<span>{E(a['one_line'])}</span></p>
{hours_table()}<p class="note">{E(H['hours_p'])}</p>
<div class="btns">{wa(place + '_visit')}{ext('map', place + '_visit', LK['maps'], S.UI['maps'], cls='go-line', ic='pin')}</div></div>
</div></section>'''


def band(place, key='default'):
    H = S.HOME
    return f'''<section class="band cta"><div class="wrap">
<h2>{E(H['band_h'])}</h2><p>{E(H['band_p'])}</p>
<div class="btns">{wa(place + '_band', key)}{call(place + '_band', cls='go-line')}</div></div></section>'''


def page_head(trail, h1, lead, photo=None, place=None, key='default'):
    ph = f'<figure class="ph-ph">{img(photo, S.PHOTOS[photo], eager="high")}</figure>' if photo else ''
    cta = f'<div class="btns">{wa(place + "_top", key)}{call(place + "_top", label=S.UI["call_short"], cls="go-line")}</div>' if place else ''
    return f'''<section class="ph{' has-ph' if photo else ''}"><div class="wrap ph-in">
<div class="ph-tx">{crumb_html(trail)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>{cta}</div>{ph}
</div></section>'''


# ---------- pages ----------
def home():
    return hero() + promise() + zones('home') + booth() + gallery('home') + visit('home') + band('home')


def services_page(path):
    P = S.SERVICES_PAGE
    trail = [('', S.UI['home']), (path, S.UI['services'])]
    cards = []
    for k in S.SERVICE_ORDER:
        s, ph = S.SERVICES[k], SVC_PHOTOS[k][0]
        cards.append(f'<li><a href="{pu(SVC_PATH[k])}"><figure>{img(ph, S.PHOTOS[ph])}</figure><span class="sc-t"><b>{E(s["h1"])}</b><span>{E(s["short"])}</span></span></a></li>')
    body = page_head(trail, P['h1'], P['lead'], None, 'services') + f'''<section class="band lt curve"><div class="wrap">
<ul class="scards">{''.join(cards)}</ul>
<div class="onestop"><h2>{E(P['one_stop_h'])}</h2><p>{E(P['one_stop'])}</p></div>
</div></section>''' + booth(True) + band('services')
    return body, [org_ld(), crumb_ld(trail)]


def service_page(k, path):
    s = S.SERVICES[k]
    trail = [('', S.UI['home']), ('services/', S.UI['services']), (path, s['zone'])]
    photos = SVC_PHOTOS[k]
    more = ''.join(f'<figure class="frame">{img(p, S.PHOTOS[p])}<figcaption>{E(S.PHOTOS[p])}</figcaption></figure>' for p in photos[1:])
    pts = ''.join(f'<li>{icon("tick")}<span>{E(x)}</span></li>' for x in s['points'])
    posted = ''
    if k == 'custom-colour':
        posted = (f'<div class="posted"><p>{E(s["posted"])}</p><ul><li>{ext("facebook", "service_video_aikka", LK["fb_video_aikka"], s["posted_aikka"], cls="more")}</li>'
                  f'<li>{ext("facebook", "service_video_glasurit", LK["fb_video_glasurit"], s["posted_glasurit"], cls="more")}</li></ul></div>')
    others = ''.join(f'<li><a href="{pu(SVC_PATH[o])}"><i style="--c:{SWATCH[i % 3]}"></i>{E(S.SERVICES[o]["zone"])}</a></li>'
                     for i, o in enumerate(S.SERVICE_ORDER) if o != k)
    body = page_head(trail, s['h1'], s['lead'], photos[0], f'service_{k}', k) + f'''<section class="band lt curve"><div class="wrap split">
<div class="prose">{''.join(f'<p>{E(p)}</p>' for p in s['paras'])}<ul class="ticks">{pts}</ul>{posted}</div>
<div class="stack">{more}</div>
</div></section>''' + booth(True) + f'''<section class="band lt"><div class="wrap"><h2>{E(S.UI['other_services'])}</h2><ul class="others">{others}</ul></div></section>''' + band(f'service_{k}', k)
    return body, [org_ld(), service_ld(k), crumb_ld(trail)]


def about_page(path):
    A = S.ABOUT
    trail = [('', S.UI['home']), (path, S.UI['about'])]
    body = page_head(trail, A['h1'], A['lead'], 'signboard', 'about') + f'''<section class="band lt curve"><div class="wrap split">
<div class="prose"><h2>{E(A['sign_h'])}</h2><p>{E(A['sign_p'])}</p><h2>{E(A['unit_h'])}</h2><p>{E(A['unit_p'])}</p></div>
<figure class="frame tall">{img('vellfire-unit-57', S.PHOTOS['vellfire-unit-57'])}<figcaption>{E(S.PHOTOS['vellfire-unit-57'])}</figcaption></figure>
</div></section>
<section class="band dk"><div class="wrap split rev">
<figure class="frame">{img('mclaren-shopfront', S.PHOTOS['mclaren-shopfront'])}<figcaption>{E(S.PHOTOS['mclaren-shopfront'])}</figcaption></figure>
<div class="prose"><h2>{E(A['contact_h'])}</h2><p>{E(A['contact_p'])}</p><p>{E(A['area_p'])}</p>
<div class="btns">{wa('about_contact')}{call('about_contact', cls='go-line')}</div></div>
</div></section>''' + visit('about')
    return body, [org_ld(), crumb_ld(trail)]


def contact_page(path):
    C = S.CONTACT
    trail = [('', S.UI['home']), (path, S.UI['contact'])]
    a = F['address']
    body = page_head(trail, C['h1'], C['lead'], None, 'contact') + f'''<section class="band lt curve"><div class="wrap split">
<div class="card-c">
<h2>{E(S.UI['address_h'])}</h2><p class="addr">{icon('pin')}<span>{E(a['one_line'])}</span></p>
<h2>{E(S.UI['hours_h'])}</h2>{hours_table()}
<h2>{E(S.UI['contact_h'])}</h2><ul class="cl">
<li>{wa('contact_list', label='WhatsApp ' + F['whatsapp']['display'], cls='fl')}</li>
<li>{call('contact_list', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='fl')}</li>
<li>{mail('contact_list', cls='fl')}</li>
<li>{ext('facebook', 'contact_list', LK['facebook'], S.UI['facebook'], cls='fl', ic='ext')}</li>
<li>{ext('youtube', 'contact_list', LK['youtube'], S.UI['youtube'], cls='fl', ic='ext')}</li>
</ul><p class="note">{E(C['ask_for'])}</p></div>
<div class="mapw"><h2>{E(C['map_h'])}</h2>
<div class="map"><iframe src="{E(LK['maps_embed'])}" title="{E(S.UI['map_title'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<div class="btns">{ext('map', 'contact', LK['maps'], S.UI['maps'], cls='go-line', ic='pin')}{ext('directions', 'contact', LK['directions'], S.UI['directions'], cls='more')}</div></div>
</div></section>''' + band('contact')
    return body, [org_ld(), crumb_ld(trail)]


def articles_page(path):
    A = S.ARTICLES
    trail = [('', S.UI['home']), (path, S.UI['articles'])]
    body = page_head(trail, A['h1'], A['empty'], None, 'articles') + '<section class="band lt curve"><div class="wrap"><ul class="art-list"></ul></div></section>'
    return body, [org_ld(), crumb_ld(trail)]


def privacy_page(path):
    P = S.PRIVACY
    trail = [('', S.UI['home']), (path, S.UI['privacy'])]
    rows = ''.join(f'<h2>{E(h)}</h2><p>{E(t)}</p>' for h, t in P['body'])
    body = page_head(trail, P['h1'], P['meta']) + f'<section class="band lt curve"><div class="wrap prose narrow">{rows}</div></section>'
    return body, [org_ld(), crumb_ld(trail)]


def render(path):
    if path == '':
        H = S.HOME
        return head(path, H['title'], H['meta'], [org_ld()]) + header(path) + home() + footer()
    if path == 'services/':
        b, ld = services_page(path); t, m = S.SERVICES_PAGE['title'], S.SERVICES_PAGE['meta']
    elif path.startswith('services/'):
        k = [x for x, p in SVC_PATH.items() if p == path][0]
        b, ld = service_page(k, path); t, m = S.SERVICES[k]['title'], S.SERVICES[k]['meta']
    elif path == 'about/':
        b, ld = about_page(path); t, m = S.ABOUT['title'], S.ABOUT['meta']
    elif path == 'contact/':
        b, ld = contact_page(path); t, m = S.CONTACT['title'], S.CONTACT['meta']
    elif path == 'articles/':
        b, ld = articles_page(path); t, m = S.ARTICLES['title'], S.ARTICLES['meta']
    else:
        b, ld = privacy_page(path); t, m = S.PRIVACY['title'], S.PRIVACY['meta']
    return head(path, t, m, ld) + header(path) + b + footer()


def check_keys():
    def walk(a, b, at):
        if type(a) is not type(b):
            raise SystemExit(f'strings type mismatch at {at}')
        if isinstance(a, dict):
            if set(a) != set(b):
                raise SystemExit(f'strings key mismatch at {at}: {set(a) ^ set(b)}')
            for k in a:
                walk(a[k], b[k], f'{at}.{k}')
        elif isinstance(a, (list, tuple)):
            if len(a) != len(b):
                raise SystemExit(f'strings length mismatch at {at}')
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, f'{at}[{i}]')
    for code in ('ms', 'zh'):
        for n in [n for n in dir(strings_en) if n.isupper()]:
            if not hasattr(STRINGS[code], n):
                raise SystemExit(f'{code} missing {n}')
            walk(getattr(strings_en, n), getattr(STRINGS[code], n), f'{code}.{n}')
    if strings_ms.SERVICE_ORDER != strings_en.SERVICE_ORDER or strings_zh.SERVICE_ORDER != strings_en.SERVICE_ORDER:
        raise SystemExit('SERVICE_ORDER differs')


def zh_font_subset():
    """Subset Noto Sans SC to the characters the 中文 pages use (source assets/fonts-src/NotoSansSC.ttf, not shipped)."""
    import subprocess
    src = os.path.join(HERE, 'assets', 'fonts-src', 'NotoSansSC.ttf')
    dst = os.path.join(HERE, 'assets', 'fonts', 'notosanssc-sub.woff2')
    text = set()
    for n in dir(strings_zh):
        if n.isupper():
            text |= set(str(getattr(strings_zh, n)))
    chars = ''.join(sorted(c for c in text if ord(c) > 0x2E80)) + '中文'
    tf = os.path.join(HERE, 'assets', 'fonts-src', 'zh-chars.txt')
    open(tf, 'w', encoding='utf8').write(chars)
    tmp = dst + '.ttf'
    subprocess.run(['fonttools', 'varLib.instancer', src, 'wght=400:700', '-o', tmp, '-q'], check=True)
    subprocess.run(['pyftsubset', tmp, f'--text-file={tf}', '--layout-features=*', '--flavor=woff2', f'--output-file={dst}'], check=True)
    os.remove(tmp)


def main():
    global S, L
    check_keys()
    if '--fonts' in sys.argv:
        zh_font_subset()
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'), ignore=shutil.ignore_patterns('fonts-src'))
    shutil.copytree(os.path.join(HERE, 'media'), os.path.join(OUT, 'media'))
    shutil.copy(os.path.join(HERE, 'p1-cta.js'), os.path.join(OUT, 'p1-cta.js'))
    built = set()
    for LL in I18N.LANGS:
        L, S = LL, STRINGS[LL['code']]
        for p in PAGES:
            sp = I18N.page_path(L, p)
            os.makedirs(os.path.join(OUT, sp), exist_ok=True)
            open(os.path.join(OUT, sp, 'index.html'), 'w', encoding='utf8').write(render(p))
            built.add(sp)
    bad = I18N.check_twins(built)
    if bad:
        raise SystemExit('\n'.join(bad))
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf8').write(I18N.sitemap_xml(absu, PAGES, TODAY))
    L, S = I18N.LANGS[0], strings_en
    a = F['address']
    lines = [f'# {NAME}', '', f'> {S.LLMS["intro"]}', '',
             f'- Address: {a["one_line"]}', f'- WhatsApp and phone: {F["whatsapp"]["intl"]} ({F["whatsapp"]["url"]})',
             f'- Email: {F["email"]}', f'- Hours: {S.HOURS_SHORT}', f'- Google Maps: {LK["maps"]}', f'- Facebook: {LK["facebook"]}',
             '', '## Services']
    lines += [f'- {S.SERVICES[k]["h1"]}: {absu(SVC_PATH[k])}' for k in S.SERVICE_ORDER]
    lines += ['', '## Pages']
    for LL in I18N.LANGS:
        for p in PAGES:
            lines.append(f'- [{LL["label"]}] {absu(I18N.page_path(LL, p))}')
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf8').write('\n'.join(lines) + '\n')
    print(f'built {len(built)} pages')


if __name__ == '__main__':
    main()
