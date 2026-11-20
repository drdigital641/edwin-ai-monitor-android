#!/usr/bin/env python3
"""Hock Chuan Hiong 福荃香 site builder (AutoSEO.my client preview, 20 Nov 2026).
One template set for every page: head, header, menu sheet, footer, mobile bar, CTA links and schema live here once, so one
edit updates every page in every language. Facts: facts.json. Copy: strings_en/ms/zh.py (same keys, checked).
Language plumbing (switcher, hreflang, og:locale, sitemap) comes from the shared ../../../autoseo-template/autoseo_i18n.py;
look v2 tokens/blocks adapted from ../../../autoseo-template/blocks/.

BASE URL: facts.json site_base is the ONE value for canonical, hreflang, og:url, schema, sitemap.xml and llms.txt.
Go-live = change site_base to https://<domain>/ and rebuild (the domain will point at this same folder). share_base
(og:image / twitter:image) stays on the preview host until the domain answers 200 over SSL.
No per-page robots meta: preview/.htaccess sends X-Robots-Tag noindex for the preview host.
  python3 build.py            -> dist/
  python3 build.py --fonts    -> also refresh the Chinese font subsets from Google Fonts (text= subset)
  python3 check.py            -> pre-upload gate
Upload: Bridge sync_from_github, site autoseo, source autoseo-clients/hock-chuan-hiong/dist, base_path preview/hock-chuan-hiong."""
import hashlib, html, json, os, re, shutil, sys, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'autoseo-template'))
import autoseo_i18n as I18N
import strings_en, strings_ms, strings_zh
STRINGS = {'en': strings_en, 'ms': strings_ms, 'zh': strings_zh}
S, L = strings_en, I18N.LANGS[0]

F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
SITE = F['site_base']
SHARE = F['share_base']
BASE = urllib.parse.urlparse(SITE).path  # '/preview/hock-chuan-hiong/' now, '/' after go-live
OUT = os.path.join(HERE, '..', 'dist')
E = html.escape
LK = F['links']
TODAY = '2026-11-20'
NAME = F['name']

# Photos placed on the server by Bridge drop_publish (drops 6afff0a4 + 6afff2c9, 20 Nov 2026) into media/ as WebP + JPG pairs.
# stem: (w, h, object-position). Smaller -600/-800 WebP copies are made by this build from the same photos (src/media).
PH = {
    'bakkwa-closeup-hero': (1600, 2000, '50% 45%'),
    'bakkwa-closeup-wide': (1600, 900, '50% 50%'),
    'bakkwa-closeup-card': (1080, 1350, '50% 40%'),
    'bakkwa-grilled-pile-hero': (1280, 720, '50% 50%'),
    'bakkwa-grilled-pile-card': (768, 960, '50% 50%'),
    'vacuum-packed-bakkwa-slices': (1080, 1350, '50% 50%'),
    'wholesale-carton-packed-bakkwa': (1080, 1350, '50% 45%'),
    'wholesale-cartons-loading-van': (1080, 1350, '50% 55%'),
    'pork-floss-jars': (1080, 1350, '50% 30%'),
    'red-carry-bag': (1080, 1350, '50% 60%'),
    'counter-signage-red-band': (1600, 720, '50% 50%'),
    'packaging-emblem': (640, 640, '50% 50%'),
    'festive-display-gift-packs': (1080, 1350, '50% 50%'),
    'display-cart-red-packs': (1080, 1350, '50% 50%'),
    'popup-stall-canopy': (768, 960, '50% 50%'),
    'mobile-stall-truck': (640, 800, '50% 50%'),
    'bakkwa-display-case': (576, 720, '50% 50%'),
}
SMALL = {k: 600 for k in PH if PH[k][0] >= 760 and PH[k][1] > PH[k][0]}  # 4:5 cards get a 600w copy
SMALL['bakkwa-closeup-hero'] = 800
SERVER_MEDIA = json.load(open(os.path.join(HERE, 'server_media.json'), encoding='utf8'))  # path -> sha256 as placed
CAROUSEL = ['bakkwa-grilled-pile-card', 'bakkwa-closeup-card', 'vacuum-packed-bakkwa-slices', 'pork-floss-jars',
            'display-cart-red-packs', 'festive-display-gift-packs', 'red-carry-bag']
PRODUCT_PHOTO = {'pork': 'bakkwa-closeup-card', 'porkfloss': 'pork-floss-jars'}
ZH_NAME = {k: strings_zh.PRODUCTS[k]['name'] for k in strings_zh.PRODUCT_ORDER}
REEL_POSTERS = ['bakkwa-grilled-pile-card', 'festive-display-gift-packs', 'popup-stall-canopy', 'wholesale-carton-packed-bakkwa']
PAGES = ['', 'products/', 'festive-gifts/', 'wholesale/', 'visit/', 'our-story/', 'articles/', 'privacy/']
NAV = [('products/', 'products'), ('festive-gifts/', 'festive'), ('wholesale/', 'wholesale'), ('visit/', 'visit'), ('our-story/', 'story')]
ACCENT = '1996年老字号福荃香肉乾至尊新春中秋批发自取'  # Ma Shan Zheng brush accents only (small)


def u(p=''):
    return BASE + p


def absu(p=''):
    return SITE + p


def share(p=''):
    return SHARE + p


def pu(p=''):
    return u(I18N.page_path(L, p))


def pabs(p=''):
    return absu(I18N.page_path(L, p))


def ver(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]


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
        'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
        'ext': '<path d="M14 5h5v5M19 5l-8 8"/><path d="M18 14v4.5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 4 18.5v-11A1.5 1.5 0 0 1 5.5 6H10"/>',
        'play': '<path d="M8 5.2v13.6L19 12z"/>',
        'star': '<path d="M12 3.6l2.5 5.3 5.8.7-4.3 4 1.1 5.7L12 16.5l-5.1 2.8 1.1-5.7-4.3-4 5.8-.7z"/>',
        'box': '<path d="M3.5 7.5L12 3.5l8.5 4v9L12 20.5l-8.5-4z"/><path d="M3.5 7.5L12 11.5l8.5-4M12 11.5v9"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'


# ---------- CTA links (data-cta = data-ref = placement; the Controller reads the whatsapp_/call_/email_/map_/facebook_ prefix) ----------
def wa(place, key='default', label=None, cls='go-wa'):
    return (f'<a class="{cls}" href="{E(wa_url(key))}" target="_blank" rel="noopener" data-cta="whatsapp_{place}" data-ref="whatsapp_{place}">'
            f'{icon("wa")}<span>{E(label or S.UI["wa_btn"])}</span></a>')


def call(place, label=None, cls='go-call'):
    return (f'<a class="{cls}" href="{F["phone"]["tel"]}" data-cta="call_{place}" data-ref="call_{place}">'
            f'{icon("call")}<span>{E(label or S.UI["call_btn"])}</span></a>')


def ext(kind, place, href, label, cls=None, ic='ext'):
    c = f' class="{cls}"' if cls else ''
    return (f'<a{c} href="{E(href)}" target="_blank" rel="noopener" data-cta="{kind}_{place}" data-ref="{kind}_{place}">'
            f'{icon(ic) if ic else ""}<span>{E(label)}</span></a>')


def mail(place, cls=None):
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="mailto:{F["email"]}" data-cta="email_{place}" data-ref="email_{place}">{icon("mail")}<span>{E(F["email"])}</span></a>'


def pic(stem, eager=False, cls=None, sizes='(min-width: 900px) 30vw, 80vw', alt=None):
    """WebP (small + full) with JPG fallback; alt = what the photo shows."""
    w, h, pos = PH[stem]
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager == 'high' else ('' if eager else ' loading="lazy"')
    sw = SMALL.get(stem)
    srcset = (f'{u("media/" + stem + "-" + str(sw) + ".webp")} {sw}w, {u("media/" + stem + ".webp")} {w}w' if sw else u('media/' + stem + '.webp'))
    sz = f' sizes="{sizes}"' if sw else ''
    a = S.PHOTOS[stem] if alt is None else alt
    return (f'<picture><source type="image/webp" srcset="{srcset}"{sz}>'
            f'<img{c} src="{u("media/" + stem + ".jpg")}" width="{w}" height="{h}" alt="{E(a)}" style="object-position:{pos}"{load} decoding="async"></picture>')


def logo(cls='logo'):
    return (f'<picture><source type="image/webp" srcset="{u("media/logo-on-maroon.webp")}">'
            f'<img class="{cls}" src="{u("media/logo-on-maroon.png")}" width="420" height="180" alt="{E(S.PHOTOS["logo"])}" decoding="async"></picture>')


def seal(txt):
    return f'<span class="seal" lang="zh-Hans">{E(txt)}</span>'


def halal_note(cls='nh'):
    return f'<p class="{cls}"><b>{E(S.UI["non_halal_short"])}</b><span>{E(S.UI["non_halal"])}</span></p>'


def embers(n=12):
    return '<div class="embers" aria-hidden="true">' + '<i></i>' * n + '</div>'


# ---------- head / header / footer ----------
def head(path, title, meta, ld):
    css = os.path.join(HERE, 'assets', 'site.css')
    zh = L['code'] == 'zh'
    font = (f'<link rel="preload" href="{u("assets/fonts/fraunces.woff2")}" as="font" type="font/woff2" crossorigin>' +
            (f'<link rel="preload" href="{u("assets/fonts/notoserifsc-400.woff2")}" as="font" type="font/woff2" crossorigin>' if zh else
             f'<link rel="preload" href="{u("assets/fonts/hanken.woff2")}" as="font" type="font/woff2" crossorigin>'))
    hero = ''
    if path == '':
        hero = (f'<link rel="preload" as="image" href="{u("media/bakkwa-grilled-pile-card.webp")}" media="(max-width: 759px)" fetchpriority="high">'
                f'<link rel="preload" as="image" href="{u("media/bakkwa-grilled-pile-hero.webp")}" media="(min-width: 760px)" fetchpriority="high">')
    ldj = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    og = share('media/og.jpg')
    return f'''<!doctype html>
<html lang="{L['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(meta)}">
<link rel="canonical" href="{pabs(path)}">
{I18N.hreflang_links(absu, path)}
<meta name="theme-color" content="#59171B">
<link rel="icon" href="{u('media/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="icon" href="{u('media/favicon.png')}" sizes="512x512" type="image/png">
<link rel="apple-touch-icon" href="{u('media/apple-touch-icon.png')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(NAME)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta)}">
<meta property="og:url" content="{pabs(path)}">
<meta property="og:image" content="{og}">
<meta property="og:image:secure_url" content="{og}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(S.PHOTOS['og'])}">
{I18N.og_locale_tags(L)}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(meta)}">
<meta name="twitter:image" content="{og}">
<meta name="twitter:image:alt" content="{E(S.PHOTOS['og'])}">
{font}{hero}
<link rel="stylesheet" href="{u('assets/site.css')}?v={ver(css)}">
{ldj}
</head>'''


def header(path):
    def cur(p):
        return ' aria-current="page"' if path == p else ''
    nav = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in NAV)
    sheet = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in [('', 'home')] + NAV + [('articles/', 'articles')])
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
{I18N.switcher(u, path, L, S.UI['lang'], cls='lang')}
<div class="sheet-cta">{wa('menu')}{call('menu')}</div>
{halal_note('nh nh-sheet')}
</div></div>
<main id="main">'''


def hours_line():
    return f'<p class="hrs">{icon("clock")}<span>{E(S.UI["hours_short"])}</span></p>'


def follow(place):
    return (f'<div class="follow">{ext("facebook", place, LK["facebook"], S.UI["facebook"], cls="chip")}'
            f'{ext("instagram", place, LK["instagram"], S.UI["instagram"], cls="chip")}'
            f'{ext("threads", place, LK["threads"], S.UI["threads"], cls="chip")}</div>')


def footer():
    a = F['address']
    lines = '<br>'.join(E(x) for x in a['lines'])
    nav = ''.join(f'<li><a href="{pu(p)}">{E(S.UI[k])}</a></li>' for p, k in NAV + [('articles/', 'articles')])
    return f'''</main>
<footer class="ft"><svg class="ft-arc" viewBox="0 0 1440 60" preserveAspectRatio="none" aria-hidden="true"><path d="M0 60V30C360 -10 1080 -10 1440 30v30z"/></svg><div class="wrap">
<div class="ft-g">
<div class="ft-id">
<a class="brand" href="{pu('')}" aria-label="{E(NAME)}">{logo()}</a>
<p class="ft-tag">{E(S.UI['tagline'])} {seal(S.UI['since'])}</p>
<address>{lines}</address>
{halal_note('nh nh-ft')}
</div>
<div><h2>{E(S.UI['hours_h'])}</h2><p class="ft-h"><span>{E(S.UI['daily'])}</span><b class="num">9am - 8pm</b></p>
<h2>{E(S.UI['contact_h'])}</h2><ul class="ft-l">
<li>{wa('footer', label='WhatsApp ' + F['whatsapp']['display'], cls='fl')}</li>
<li>{call('footer', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='fl')}</li>
<li>{mail('footer', cls='fl')}</li>
<li>{ext('map', 'footer', LK['gbp'], S.UI['maps'], cls='fl', ic='pin')}</li>
</ul></div>
<div><h2>{E(S.UI['follow_h'])}</h2>{follow('footer')}
<ul class="ft-n">{nav}</ul></div>
</div>
<div class="ft-b"><span>&copy; 2026 {E(NAME)}</span><a href="{pu('privacy/')}">{E(S.UI['privacy'])}</a><a href="https://autoseo.my/">Website by AutoSEO.my</a></div>
</div></footer>
<div class="mbar">{wa('mobile_bar', label=S.UI['wa_short'])}{call('mobile_bar', label=S.UI['call_short'])}</div>
<script src="{u('assets/site.js')}?v={ver(os.path.join(HERE, 'assets', 'site.js'))}" defer></script>
<script src="{u('p1-cta.js')}?v={ver(os.path.join(HERE, 'p1-cta.js'))}" defer></script>
</body>
</html>
'''


# ---------- schema (GBP NAP; no aggregateRating) ----------
def org_ld():
    a = F['address']
    return {
        '@context': 'https://schema.org', '@type': 'FoodEstablishment', '@id': SITE + '#business',
        'name': NAME, 'alternateName': [F['name_en'], F['name_zh'], F['name_zh_full']],
        'description': S.SCHEMA['description'], 'url': pabs(''), 'inLanguage': L['hreflang'],
        'telephone': F['phone']['e164'], 'email': F['email'],
        'image': share('media/og.jpg'), 'logo': absu('media/logo-on-maroon.png'),
        'address': {'@type': 'PostalAddress', 'streetAddress': a['street'] + ', ' + a['locality'], 'addressLocality': a['city'],
                    'postalCode': a['postcode'], 'addressRegion': a['region'], 'addressCountry': a['country']},
        'geo': {'@type': 'GeoCoordinates', 'latitude': F['geo']['lat'], 'longitude': F['geo']['lng']},
        'hasMap': LK['gbp'],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': h['days'], 'opens': h['opens'], 'closes': h['closes']} for h in F['hours']],
        'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': F['phone']['e164'], 'url': F['whatsapp']['url'],
                          'availableLanguage': ['en', 'ms', 'zh']}],
        'sameAs': [LK['facebook'], LK['instagram']],
        'areaServed': {'@type': 'City', 'name': 'Klang'},
    }


def site_ld():
    return {'@context': 'https://schema.org', '@type': 'WebSite', '@id': SITE + '#website', 'name': NAME, 'url': pabs(''),
            'inLanguage': L['hreflang'], 'publisher': {'@id': SITE + '#business'}}


def crumb_ld(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': pabs(p)} for i, (p, n) in enumerate(trail)]}


def crumb_html(trail):
    li = ''.join(f'<li><a href="{pu(p)}"{" aria-current=\"page\"" if i == len(trail) - 1 else ""}>{E(n)}</a></li>' for i, (p, n) in enumerate(trail))
    return f'<nav class="crumb" aria-label="{E(S.UI["breadcrumb"])}"><ol>{li}</ol></nav>'


# ---------- blocks ----------
def hero():
    H = S.HOME
    w, h, _ = PH['bakkwa-grilled-pile-hero']
    return f'''<section class="hero">
<picture class="hero-ph"><source media="(min-width: 760px)" type="image/webp" srcset="{u('media/bakkwa-grilled-pile-hero.webp')}" width="{w}" height="{h}">
<source media="(min-width: 760px)" srcset="{u('media/bakkwa-grilled-pile-hero.jpg')}" width="{w}" height="{h}">
<source type="image/webp" srcset="{u('media/bakkwa-grilled-pile-card.webp')}">
<img src="{u('media/bakkwa-grilled-pile-card.jpg')}" width="768" height="960" alt="{E(S.PHOTOS['bakkwa-grilled-pile-hero'])}" fetchpriority="high" decoding="async"></picture>
<div class="glow" aria-hidden="true"></div>{embers()}
<div class="wrap hero-in">
{seal(S.UI['since'])}
<h1>{E(H['h1'])}</h1>
<p class="hero-line">{E(H['line'])}</p>
<div class="hero-cta">{wa('home_hero')}{call('home_hero', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='go-line')}</div>
</div>
<svg class="hero-arc" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 80V40C400 -8 1040 -8 1440 40v40z"/></svg>
</section>'''


def carousel(place):
    cards = ''.join(f'<li class="pc"><figure>{pic(s, sizes="(min-width: 900px) 300px, 72vw")}<figcaption>{E(S.CAPS[s])}</figcaption></figure></li>' for s in CAROUSEL)
    return f'''<div class="gl" role="region" aria-label="{E(S.UI['carousel'])}"><ul class="glide" data-speed="0.035">{cards}</ul>
<div class="gl-c"><button type="button" class="arr" data-dir="-1" aria-label="{E(S.UI['prev'])}">{icon('prev')}</button><button type="button" class="arr" data-dir="1" aria-label="{E(S.UI['next'])}">{icon('next')}</button></div></div>'''


def product_card(k, place):
    p = S.PRODUCTS[k]
    zh = ZH_NAME[k]
    if k in PRODUCT_PHOTO:
        media = f'<div class="pr-m">{pic(PRODUCT_PHOTO[k], sizes="(min-width: 900px) 25vw, 46vw")}</div>'
    else:
        media = f'<div class="pr-m pr-t" aria-hidden="true"><span lang="zh-Hans">{E(zh)}</span></div>'
    sub = '' if L['code'] == 'zh' else f'<span class="pr-zh" lang="zh-Hans">{E(zh)}</span>'
    return f'<li class="pr">{media}<div class="pr-b"><h3>{E(p["name"])}{sub}</h3><p>{E(p["line"])}</p></div></li>'


def products_grid(place):
    return f'<ul class="prs">{"".join(product_card(k, place) for k in S.PRODUCT_ORDER)}</ul>'


def sec_h(h, p=None, tag='h2'):
    pp = f'<p>{E(p)}</p>' if p else ''
    return f'<div class="sec-h"><{tag}>{E(h)}</{tag}>{pp}</div>'


def home():
    H = S.HOME
    reels = ''.join(
        f'<li><a class="rl" href="https://www.facebook.com/reel/{rid}/" target="_blank" rel="noopener" data-cta="facebook_reel_{i + 1}" data-ref="facebook_reel_{i + 1}" aria-label="{E(S.UI["play"])} {i + 1}">'
        f'{pic(REEL_POSTERS[i], alt="", sizes="(min-width: 900px) 25vw, 46vw")}<span class="rl-p">{icon("play")}</span><span class="rl-t">{E(S.UI["reel"])} {i + 1}</span></a></li>'
        for i, rid in enumerate(LK['reels']))
    return hero() + f'''
<section class="band cream" id="products"><div class="wrap">
{sec_h(H['products_h'], H['products_p'])}
</div>{carousel('home')}
<div class="wrap row-cta">{wa('home_products', label=S.UI['wa_price'])}<a class="more" href="{pu('products/')}">{E(S.UI['all_products'])}{icon('go')}</a></div>
<div class="wrap">{halal_note()}</div>
</section>

<section class="band maroon curve" id="festive">{embers(8)}<div class="wrap fest">
<div class="fest-tx">{sec_h(H['festive_h'], H['festive_p'])}
<ul class="fest-t"><li><span lang="zh-Hans">新春</span><b>{E(H['festive_cny'])}</b></li><li><span lang="zh-Hans">中秋</span><b>{E(H['festive_moon'])}</b></li></ul>
<div class="btns">{wa('home_festive', 'festive', label=S.UI['wa_festive'], cls='go-wa gold')}<a class="more lt" href="{pu('festive-gifts/')}">{E(S.UI['more_festive'])}{icon('go')}</a></div></div>
<figure class="fest-ph">{pic('festive-display-gift-packs', sizes="(min-width: 900px) 40vw, 90vw")}</figure>
</div></section>

<section class="band cream curve" id="wholesale"><div class="wrap lap">
<div class="lap-ph"><figure class="a">{pic('wholesale-carton-packed-bakkwa', sizes="(min-width: 900px) 30vw, 62vw")}</figure><figure class="b">{pic('wholesale-cartons-loading-van', sizes="(min-width: 900px) 22vw, 46vw")}</figure></div>
<div class="lap-card">{seal('批发')}<h2>{E(H['wholesale_h'])}</h2><p>{E(H['wholesale_p'])}</p>
<div class="btns">{wa('home_wholesale', 'wholesale', label=S.UI['wa_wholesale'])}<a class="more" href="{pu('wholesale/')}">{E(S.UI['more_wholesale'])}{icon('go')}</a></div></div>
</div></section>

<section class="band rice curve" id="visit"><div class="wrap visit">
<figure class="v-ph">{pic('red-carry-bag', sizes="(min-width: 900px) 30vw, 80vw")}</figure>
<div class="v-tx">{seal('自取')}<h2>{E(H['visit_h'])}</h2><p>{E(H['visit_p'])}</p>
<p class="addr">{icon('pin')}<span>{E(F['address']['one_line'])}</span></p>{hours_line()}
<div class="btns">{wa('home_visit', 'pickup', label=S.UI['wa_pickup'])}{call('home_visit', cls='go-line')}</div>
<p class="sub">{ext('map', 'home_visit', LK['gbp'], S.UI['maps'], cls='more', ic='pin')}</p></div>
</div></section>

<section class="band char curve" id="popups"><div class="wrap">
{sec_h(H['popup_h'], H['popup_p'])}
<div class="mos"><figure class="m1">{pic('popup-stall-canopy', sizes="(min-width: 900px) 40vw, 90vw")}</figure>
<figure class="m2">{pic('display-cart-red-packs', sizes="(min-width: 900px) 25vw, 44vw")}</figure>
<figure class="m3">{pic('mobile-stall-truck', sizes="(min-width: 900px) 25vw, 44vw")}</figure></div>
{follow('home_popups')}
</div></section>

<section class="band story curve" id="story"><div class="story-bg" aria-hidden="true">{pic('counter-signage-red-band', alt='', sizes='100vw')}</div><div class="wrap">
<div class="story-card"><h2>{E(H['story_h'])}</h2><p>{E(H['story_p'])}</p>
<a class="more" href="{pu('our-story/')}">{E(S.UI['more_story'])}{icon('go')}</a></div>
</div></section>

<section class="band cream curve" id="reels"><div class="wrap">
{sec_h(H['reels_h'], H['reels_p'])}
<ul class="reels">{reels}</ul>
<div class="proof"><p class="rate"><b class="num">{F['rating']['value']}</b>{icon('star')}<span>{E(H['proof_line'].format(n=F['rating']['count']))}</span></p>
{ext('reviews', 'home', LK['gbp'], S.UI['reviews'], cls='more')}</div>
</div></section>'''


def page_head(trail, h1, lead, place=None, key='default', label=None):
    cta = f'<div class="btns">{wa(place + "_head", key, label=label)}{call(place + "_head", cls="go-line lt")}</div>' if place else ''
    return f'''<section class="ph">{embers(7)}<div class="wrap">{crumb_html(trail)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>{cta}</div>
<svg class="hero-arc" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0 80V40C400 -8 1040 -8 1440 40v40z"/></svg></section>'''


def products_page(path):
    P = S.PRODUCTS_PAGE
    trail = [('', S.UI['home']), (path, S.UI['products'])]
    body = page_head(trail, P['h1'], P['lead'], 'products', label=S.UI['wa_price']) + f'''
<section class="band cream"><div class="wrap">{products_grid('products')}{halal_note()}</div></section>
<section class="band rice curve"><div class="wrap lap">
<div class="lap-ph one"><figure class="a">{pic('vacuum-packed-bakkwa-slices', sizes="(min-width: 900px) 34vw, 80vw")}</figure></div>
<div class="lap-card"><h2>{E(P['packed_h'])}</h2><p>{E(P['packed_p'])}</p>
<div class="btns">{wa('products_packed', label=S.UI['wa_price'])}<a class="more" href="{pu('festive-gifts/')}">{E(S.UI['more_festive'])}{icon('go')}</a></div></div>
</div></section>
<section class="band cream curve"><div class="wrap">{sec_h(S.HOME['products_h'])}</div>{carousel('products')}</section>'''
    return body, [org_ld(), crumb_ld(trail)]


def festive_page(path):
    P = S.FESTIVE
    H = S.HOME
    trail = [('', S.UI['home']), (path, S.UI['festive'])]
    how = ''.join(f'<li><span class="n num">{i + 1}</span><p>{E(x)}</p></li>' for i, x in enumerate(P['how']))
    body = page_head(trail, P['h1'], P['lead'], 'festive', 'festive', S.UI['wa_festive']) + f'''
<section class="band cream"><div class="wrap">
<ul class="fest-big"><li><span lang="zh-Hans">新春</span><h2>{E(H['festive_cny'])}</h2><p>{E(P['cny_p'])}</p></li>
<li><span lang="zh-Hans">中秋</span><h2>{E(H['festive_moon'])}</h2><p>{E(P['moon_p'])}</p></li></ul>
</div></section>
<section class="band maroon curve">{embers(8)}<div class="wrap fest">
<div class="fest-tx"><h2>{E(P['how_h'])}</h2><ol class="how">{how}</ol>
<div class="btns">{wa('festive_how', 'festive', label=S.UI['wa_festive'], cls='go-wa gold')}</div>
<p class="sub"><a class="more lt" href="{pu('wholesale/')}">{E(P['corporate_p'])}{icon('go')}</a></p></div>
<figure class="fest-ph">{pic('festive-display-gift-packs', sizes="(min-width: 900px) 40vw, 90vw")}</figure>
</div></section>
<section class="band cream curve"><div class="wrap"><div class="duo">
<figure>{pic('display-cart-red-packs', sizes="(min-width: 900px) 30vw, 46vw")}<figcaption>{E(S.CAPS['display-cart-red-packs'])}</figcaption></figure>
<figure>{pic('red-carry-bag', sizes="(min-width: 900px) 30vw, 46vw")}<figcaption>{E(S.CAPS['red-carry-bag'])}</figcaption></figure></div>
{halal_note()}</div></section>'''
    return body, [org_ld(), crumb_ld(trail)]


def wholesale_page(path):
    P = S.WHOLESALE
    trail = [('', S.UI['home']), (path, S.UI['wholesale'])]
    send = ''.join(f'<li>{icon("box")}<span>{E(x)}</span></li>' for x in P['send'])
    body = page_head(trail, P['h1'], P['lead'], 'wholesale', 'wholesale', S.UI['wa_wholesale']) + f'''
<section class="band cream"><div class="wrap lap">
<div class="lap-ph"><figure class="a">{pic('wholesale-carton-packed-bakkwa', sizes="(min-width: 900px) 30vw, 62vw")}</figure><figure class="b">{pic('vacuum-packed-bakkwa-slices', sizes="(min-width: 900px) 22vw, 46vw")}</figure></div>
<div class="lap-card"><h2>{E(P['send_h'])}</h2><ul class="send">{send}</ul>
<div class="btns">{wa('wholesale_send', 'wholesale', label=S.UI['wa_wholesale'])}</div></div>
</div></section>
<section class="band rice curve"><div class="wrap duo">
<figure>{pic('wholesale-carton-packed-bakkwa', sizes="(min-width: 900px) 30vw, 46vw")}<figcaption>{E(P['carton_p'])}</figcaption></figure>
<figure>{pic('wholesale-cartons-loading-van', sizes="(min-width: 900px) 30vw, 46vw")}<figcaption>{E(P['van_p'])}</figcaption></figure>
</div><div class="wrap">{halal_note()}</div></section>
<section class="band cream curve"><div class="wrap">{sec_h(S.HOME['products_h'])}{products_grid('wholesale')}</div></section>'''
    return body, [org_ld(), crumb_ld(trail)]


def visit_page(path):
    P = S.VISIT
    trail = [('', S.UI['home']), (path, S.UI['visit'])]
    steps = ''.join(f'<li><span class="n num">{i + 1}</span><p>{E(x)}</p></li>' for i, x in enumerate(P['pickup']))
    body = page_head(trail, P['h1'], P['lead'], 'visit', 'pickup', S.UI['wa_pickup']) + f'''
<section class="band cream"><div class="wrap split">
<div class="card-c">
<h2>{E(S.UI['address_h'])}</h2><p class="addr">{icon('pin')}<span>{E(F['address']['one_line'])}</span></p>
<h2>{E(S.UI['hours_h'])}</h2><p class="ft-h dk"><span>{E(S.UI['daily'])}</span><b class="num">9am - 8pm</b></p>
<h2>{E(S.UI['contact_h'])}</h2><ul class="cl">
<li>{wa('visit_list', 'pickup', label='WhatsApp ' + F['whatsapp']['display'], cls='fl')}</li>
<li>{call('visit_list', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='fl')}</li>
<li>{mail('visit_list', cls='fl')}</li>
</ul>{halal_note()}</div>
<div class="mapw"><h2>{E(P['map_h'])}</h2>
<div class="map"><iframe src="{E(LK['map_embed'])}" title="{E(S.UI['map_title'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<div class="btns">{ext('map', 'visit', LK['gbp'], S.UI['maps'], cls='go-line', ic='pin')}</div></div>
</div></section>
<section class="band rice curve"><div class="wrap visit">
<figure class="v-ph">{pic('red-carry-bag', sizes="(min-width: 900px) 30vw, 80vw")}</figure>
<div class="v-tx"><h2>{E(P['pickup_h'])}</h2><ol class="how dk">{steps}</ol>
<div class="btns">{wa('visit_pickup', 'pickup', label=S.UI['wa_pickup'])}</div></div>
</div></section>
<section class="band char curve"><div class="wrap">{sec_h(S.HOME['popup_h'], S.HOME['popup_p'])}
<div class="mos"><figure class="m1">{pic('popup-stall-canopy', sizes="(min-width: 900px) 40vw, 90vw")}</figure>
<figure class="m2">{pic('bakkwa-display-case', sizes="(min-width: 900px) 25vw, 44vw")}</figure>
<figure class="m3">{pic('mobile-stall-truck', sizes="(min-width: 900px) 25vw, 44vw")}</figure></div>
{follow('visit_popups')}</div></section>'''
    return body, [org_ld(), crumb_ld(trail)]


def story_page(path):
    P = S.STORY
    trail = [('', S.UI['home']), (path, S.UI['story'])]
    body = page_head(trail, P['h1'], P['lead']) + f'''
<section class="band cream"><div class="wrap split st">
<div class="prose"><p class="big">{E(P['p1'])}</p><p>{E(P['p2'])}</p><p>{E(P['p3'])}</p>
<div class="btns">{wa('story')}<a class="more" href="{pu('visit/')}">{E(S.UI['more_visit'])}{icon('go')}</a></div></div>
<figure class="st-sign"><span lang="zh-Hans">1996年<br>老字号</span></figure>
</div></section>
<section class="band story curve"><div class="story-bg" aria-hidden="true">{pic('counter-signage-red-band', alt='', sizes='100vw')}</div><div class="wrap">
<div class="story-card"><h2>{E(P['ben_h'])}</h2><p>{E(P['ben_p'])}</p>
{ext('facebook', 'story_series', LK['facebook'], P['ben_link'], cls='more')}</div>
</div></section>
<section class="band cream curve"><div class="wrap emb">
<figure class="badge">{pic('packaging-emblem', sizes='160px')}</figure><p>{E(P['emblem_p'])}</p>{halal_note()}
</div></section>'''
    return body, [org_ld(), crumb_ld(trail)]


def articles_page(path):
    A = S.ARTICLES
    trail = [('', S.UI['home']), (path, S.UI['articles'])]
    body = page_head(trail, A['h1'], A['empty'], 'articles') + f'<section class="band cream"><div class="wrap"><ul class="art-list"></ul>{halal_note()}</div></section>'
    return body, [org_ld(), crumb_ld(trail)]


def privacy_page(path):
    P = S.PRIVACY
    trail = [('', S.UI['home']), (path, S.UI['privacy'])]
    rows = ''.join(f'<h2>{E(h)}</h2><p>{E(t)}</p>' for h, t in P['body'])
    body = page_head(trail, P['h1'], P['meta']) + f'<section class="band cream"><div class="wrap prose narrow">{rows}{halal_note()}</div></section>'
    return body, [org_ld(), crumb_ld(trail)]


PAGE_FN = {'products/': (products_page, 'PRODUCTS_PAGE'), 'festive-gifts/': (festive_page, 'FESTIVE'), 'wholesale/': (wholesale_page, 'WHOLESALE'),
           'visit/': (visit_page, 'VISIT'), 'our-story/': (story_page, 'STORY'), 'articles/': (articles_page, 'ARTICLES'), 'privacy/': (privacy_page, 'PRIVACY')}


def render(path):
    if path == '':
        H = S.HOME
        return head(path, H['title'], H['meta'], [org_ld(), site_ld()]) + header(path) + home() + footer()
    fn, key = PAGE_FN[path]
    b, ld = fn(path)
    D = getattr(S, key)
    return head(path, D['title'], D['meta'], ld) + header(path) + b + footer()


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


def cjk_text():
    t = set()
    for mod in STRINGS.values():
        for n in dir(mod):
            if n.isupper():
                t |= set(str(getattr(mod, n)))
    t |= set(NAME + ACCENT + '中文' + '新春中秋' + '1996年老字号')
    return ''.join(sorted(c for c in t if ord(c) > 0x2E80))


def fonts():
    """Chinese subsets straight from Google Fonts (text= returns one woff2 holding only these glyphs)."""
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    chars = cjk_text()
    open(os.path.join(HERE, 'assets', 'fonts', 'zh-chars.txt'), 'w', encoding='utf8').write(chars)
    for fam, wt, out, txt in [('Noto Serif SC', 400, 'notoserifsc-400.woff2', chars), ('Noto Serif SC', 700, 'notoserifsc-700.woff2', chars),
                              ('Ma Shan Zheng', 400, 'mashanzheng.woff2', ''.join(sorted(set(ACCENT))))]:
        q = urllib.parse.urlencode({'family': f'{fam}:wght@{wt}', 'text': txt, 'display': 'swap'})
        css = urllib.request.urlopen(urllib.request.Request('https://fonts.googleapis.com/css2?' + q, headers={'User-Agent': ua})).read().decode()
        url = re.search(r'url\((https://[^)]+)\)', css).group(1)
        open(os.path.join(HERE, 'assets', 'fonts', out), 'wb').write(urllib.request.urlopen(url).read())


def small_media():
    """600w/800w WebP copies of the drop photos (from the full JPGs in ../media-src, which are not shipped)."""
    from PIL import Image
    src = os.path.join(HERE, '..', 'media-src')
    os.makedirs(os.path.join(HERE, 'media'), exist_ok=True)
    for stem, w in SMALL.items():
        dst = os.path.join(HERE, 'media', f'{stem}-{w}.webp')
        if os.path.exists(dst):
            continue
        im = Image.open(os.path.join(src, stem + '.jpg')).convert('RGB')
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        im.save(dst, 'WEBP', quality=78, method=6)


def main():
    global S, L
    check_keys()
    if '--fonts' in sys.argv:
        fonts()
    if '--media' in sys.argv:
        small_media()
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'), ignore=shutil.ignore_patterns('zh-chars.txt'))
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
             f'- Address: {a["one_line"]}', f'- WhatsApp and phone: {F["phone"]["display"]} ({F["whatsapp"]["url"]})',
             f'- Email: {F["email"]}', '- Hours: Monday to Sunday, 9am to 8pm', f'- Google Maps: {LK["gbp"]}',
             f'- Google rating: {F["rating"]["value"]} from {F["rating"]["count"]} reviews (Google Business Profile, 20 Nov 2026)',
             f'- Facebook: {LK["facebook"]}', f'- Instagram: {LK["instagram"]}', f'- Threads: {LK["threads"]}',
             '- Non-Halal: pork products.', '', '## Products']
    lines += [f'- {S.PRODUCTS[k]["name"]} ({ZH_NAME[k]})' for k in S.PRODUCT_ORDER]
    lines += ['', '## Pages']
    for LL in I18N.LANGS:
        for p in PAGES:
            lines.append(f'- [{LL["label"]}] {absu(I18N.page_path(LL, p))}')
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf8').write('\n'.join(lines) + '\n')
    print(f'built {len(built)} pages for {SITE}')


if __name__ == '__main__':
    main()
