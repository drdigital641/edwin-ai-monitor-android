#!/usr/bin/env python3
"""Rasa Sayang Automotive site builder (AutoSEO.my client preview, 19 Nov 2026).
One template set for every page: head, header, menu sheet, footer, mobile bar, CTA links and schema live here once, so one
edit updates every page in every language.
Facts: facts.json. Copy: strings_en.py, strings_ms.py, strings_zh.py (same keys). Output: ../dist/ (English at the root,
Bahasa Melayu at ms/, Simplified Chinese at zh/). Switcher, hreflang, og:locale and sitemap language entries come from the
shared AutoSEO template ../../../autoseo-template/autoseo_i18n.py.
  python3 build.py   -> build from site.json (one switch: live_domain + live). LIVE since 20 Nov 2026 on
                        https://rasasayangautomotive.com/ (addon docroot = autoseo.my/preview/rasa-sayang, same files).
Then python3 check.py (pre-upload gate) before any upload through the Bridge (sync_from_github, base_path preview/rasa-sayang).
Photos are NOT in this repo: they were placed on the server from Bridge drops 6afef206... and 6afef249... into images/."""
import hashlib, html, json, os, shutil, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'autoseo-template'))
import autoseo_i18n as I18N
import strings_en, strings_ms, strings_zh
STRINGS = {'en': strings_en, 'ms': strings_ms, 'zh': strings_zh}
S, L = strings_en, I18N.LANGS[0]  # current language; build() switches both

F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
# ONE-SWITCH GO-LIVE (20 Nov 2026, autoseo-template/golive): host-dependent output comes from site.json only.
#   live_domain empty -> canonical etc. on the preview URL, meta noindex.
#   live_domain set   -> canonical / hreflang / JSON-LD / sitemap / robots / llms on https://<live_domain>/.
#   live true         -> og:url, og:image and twitter:image on the live domain too, and no meta noindex (the preview host still
#                        gets X-Robots-Tag noindex from autoseo.my/preview/.htaccess, Host-conditional).
# Links and assets are page-relative (@@B@@ is swapped per page depth at write time), so one set of files works at the domain
# root and under /preview/rasa-sayang/.
CFG = json.load(open(os.path.join(HERE, 'site.json'), encoding='utf8'))
LIVE_DOMAIN = (CFG.get('live_domain') or '').strip('/').lower()
LIVE = bool(CFG.get('live')) and bool(LIVE_DOMAIN)
PREVIEW = CFG['preview_url']
SITE = f'https://{LIVE_DOMAIN}/' if LIVE_DOMAIN else PREVIEW
SHARE = SITE if LIVE else PREVIEW
OG = CFG.get('og_image', 'images/og.jpg') + (f"?v={CFG['og_version']}" if CFG.get('og_version') else '')
BASE = '@@B@@/'
NOINDEX = not LIVE
OUT = os.path.join(HERE, '..', 'dist')
E = html.escape
HQ, SUB = F['locations'][0], F['locations'][1]


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


TEL = 'tel:' + F['whatsapp_e164']
FB = F['facebook']

# 4:5 work files (w, h) and their -full lightbox files (w, h), from manifest.json in the drop.
PHOTOS = {
    'porsche-taycan-ev-battery-lift': (594, 742, 1080, 742),
    'porsche-taycan-ev-diagnostics': (530, 662, 1280, 662),
    'volvo-xc90-t8-hybrid-battery-work': (790, 988, 810, 988),
    'volvo-xc90-t8-hybrid-battery-modules': (937, 1171, 960, 1171),
    'volvo-xc90-t8-coolant-pump-hoses': (901, 1126, 960, 1126),
    'volvo-xc90-t8-erad-parts': (704, 880, 1280, 880),
    'volvo-xc90-t8-erad-bay': (960, 1205, 960, 1205),
    'volvo-xc90-t8-hybrid-bdu': (960, 1200, 960, 1219),
    'volvo-xc60-t8-coolant-pumps': (720, 900, 1280, 900),
    'volvo-xc60-t8-obc-control-units': (960, 1205, 960, 1205),
    'volvo-xc60-t8-fuel-pump-module': (591, 739, 1080, 739),
    'ferrari-488-gear-knob-internals': (810, 1016, 810, 1016),
    'ferrari-488-gear-knob-panel': (810, 1016, 810, 1016),
    'bmw-x5-f15-gearbox-flywheel': (960, 1208, 960, 1208),
    'lamborghini-aventador-svj-service-lift': (713, 891, 1280, 891),
    'lamborghini-aventador-svj-rear': (713, 891, 1280, 891),
    'supercar-service-bay-shah-alam': (715, 894, 1280, 894),
    'lamborghini-aventador-svj-front-service': (708, 885, 1280, 885),
    'ev-hybrid-fender-cover-coolant-pumps': (960, 1193, 960, 1193),
    'rolls-royce-front-engine-service': (709, 886, 1280, 886),
    'rolls-royce-engine-overhaul-lift': (960, 1195, 960, 1195),
    'rolls-royce-engines-on-floor': (710, 887, 1280, 887),
    'volvo-xc90-t8-erad-motor': (689, 861, 1280, 861),
    'rolls-royce-air-suspension': (591, 739, 1080, 739),
    'volvo-xc90-t8-brake-fluid': (960, 1199, 960, 1199),
}
# Home carousel order: mix the three worlds (supercar, HV hybrid, engine) so the first frames show range.
CAROUSEL = ['lamborghini-aventador-svj-service-lift', 'volvo-xc90-t8-hybrid-battery-modules', 'rolls-royce-engine-overhaul-lift',
            'porsche-taycan-ev-battery-lift', 'ferrari-488-gear-knob-internals', 'volvo-xc90-t8-erad-motor', 'bmw-x5-f15-gearbox-flywheel',
            'lamborghini-aventador-svj-front-service', 'volvo-xc60-t8-obc-control-units', 'rolls-royce-air-suspension',
            'porsche-taycan-ev-diagnostics', 'volvo-xc90-t8-hybrid-bdu', 'rolls-royce-engines-on-floor', 'volvo-xc90-t8-erad-bay',
            'ferrari-488-gear-knob-panel', 'volvo-xc60-t8-coolant-pumps', 'lamborghini-aventador-svj-rear', 'volvo-xc90-t8-hybrid-battery-work',
            'rolls-royce-front-engine-service', 'volvo-xc60-t8-fuel-pump-module', 'volvo-xc90-t8-coolant-pump-hoses',
            'ev-hybrid-fender-cover-coolant-pumps', 'volvo-xc90-t8-erad-parts', 'volvo-xc90-t8-brake-fluid', 'supercar-service-bay-shah-alam']
assert sorted(CAROUSEL) == sorted(PHOTOS)


def img(stem):
    return u(f'images/{stem}.webp')


# ---------- icons: one authored set, 1.6 stroke, square caps (workshop line drawing) ----------
def icon(name):
    p = {
        'wa': '<path d="M4.5 19.5l1.2-3.6A8 8 0 1 1 8.6 18.6z"/><path d="M9.2 8.6c.3 2.6 2.4 4.9 5.2 5.4l1-1.2 1.8.8-.3 1.6c-3.9.4-8-3.6-7.7-7.5l1.6-.3.8 1.8z"/>',
        'call': '<path d="M5 4h4l1.5 4-2.2 1.4a11 11 0 0 0 6.3 6.3L16 13.5l4 1.5v4a1.5 1.5 0 0 1-1.6 1.5C10.6 20 4 13.4 3.5 5.6A1.5 1.5 0 0 1 5 4z"/>',
        'pin': '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
        'nav': '<path d="M4 11.5L20 4l-7.5 16-1.6-6.9z"/>',
        'fb': '<path d="M13.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4a21 21 0 0 0-2.3-.1c-2.3 0-3.8 1.4-3.8 3.9v2.3H8v3h2.5V21"/>',
        'play': '<path d="M8 5.5v13l10-6.5z"/>',
        'scan': '<path d="M4 8V4h4M16 4h4v4M20 16v4h-4M8 20H4v-4"/><path d="M7 12h3l1.5-3 2 6 1.5-3h2"/>',
        'wrench': '<path d="M14.5 4.5a4 4 0 0 0-4.8 5.3L4 15.5 6.5 18l5.7-5.7a4 4 0 0 0 5.3-4.8l-2.4 2.4-2.3-.6-.6-2.3z"/>',
        'key': '<circle cx="8" cy="15" r="3.5"/><path d="M10.5 12.5L19 4M16 7l2.5 2.5M14 9l1.8 1.8"/>',
        'bolt': '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z"/>',
        'prev': '<path d="M15 5l-7 7 7 7"/>', 'next': '<path d="M9 5l7 7-7 7"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
        'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>', 'go': '<path d="M5 12h13M13 6l6 6-6 6"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'


# ---------- CTA links (data-cta = placement; the Controller reads the whatsapp_/call_/facebook_/waze_/map_ prefix) ----------
def wa(place, label=None, cls='btn-wa'):
    return (f'<a class="{cls}" href="{E(wa_url())}" target="_blank" rel="noopener" data-cta="whatsapp_{place}" data-ref="whatsapp_{place}">'
            f'{icon("wa")}<span>{E(label or S.UI["wa_btn"])}</span></a>')


def call(place, label=None, cls='btn-call'):
    return f'<a class="{cls}" href="{TEL}" data-cta="call_{place}" data-ref="call_{place}">{icon("call")}<span>{E(label or S.UI["call_btn"])}</span></a>'


def fb(place, label=None, cls='lnk', href=None):
    return (f'<a class="{cls}" href="{E(href or FB)}" target="_blank" rel="noopener" data-cta="facebook_{place}" data-ref="facebook_{place}">'
            f'{icon("fb")}<span>{E(label or S.UI["fb_btn"])}</span></a>')


def waze(loc, place, cls='lnk'):
    return (f'<a class="{cls}" href="{E(loc["waze"])}" target="_blank" rel="noopener" data-cta="waze_{loc["id"]}_{place}" '
            f'data-ref="waze_{loc["id"]}_{place}">{icon("nav")}<span>{E(S.UI["waze_btn"])}</span></a>')


def gmap(loc, place, cls='lnk'):
    return (f'<a class="{cls}" href="{E(loc["maps_url"])}" target="_blank" rel="noopener" data-cta="map_{loc["id"]}_{place}" '
            f'data-ref="map_{loc["id"]}_{place}">{icon("pin")}<span>{E(S.UI["map_btn"])}</span></a>')


# ---------- schema ----------
BIZ_ID = absu('#business')
SUB_ID = absu('#subang-jaya')


def postal(loc):
    return {'@type': 'PostalAddress', 'streetAddress': loc['street'], 'addressLocality': loc['city'], 'addressRegion': loc['region'],
            'postalCode': loc['postcode'], 'addressCountry': loc['country']}


def business():
    return {
        '@type': ['AutoRepair', 'AutomotiveBusiness', 'LocalBusiness'], '@id': BIZ_ID,
        'name': F['name'], 'legalName': F['legal_name'], 'alternateName': F['short'], 'url': pabs(),
        'description': S.HOME['desc'], 'slogan': F['tagline_verbatim'],
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'Company registration number (Malaysia)', 'value': F['company_no']},
        'logo': absu('images/logo-transparent.png'), 'image': [absu('images/cover.webp'), shu(OG)],
        'telephone': F['whatsapp_e164'], 'address': postal(HQ), 'hasMap': HQ['waze'], 'sameAs': [FB],
        'areaServed': [{'@type': 'City', 'name': c} for c in F['service_area']] + [{'@type': 'AdministrativeArea', 'name': 'Selangor'}],
        'knowsAbout': [s['name'] for s in S.SERVICES] + F['brands_serviced'],
        'contactPoint': {'@type': 'ContactPoint', 'telephone': F['whatsapp_e164'], 'contactType': 'customer service',
                         'availableLanguage': ['en', 'ms', 'zh']},
        'department': {'@id': SUB_ID},
    }


def branch():
    return {'@type': ['AutoRepair', 'LocalBusiness'], '@id': SUB_ID, 'name': f"{F['short']} ({SUB['label']})",
            'url': pabs('contact/'), 'telephone': F['whatsapp_e164'], 'address': postal(SUB), 'hasMap': SUB['waze'],
            'parentOrganization': {'@id': BIZ_ID}, 'image': shu(OG)}


def crumbs(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': pabs(p)} for i, (n, p) in enumerate(items)]}


def faqld(faq):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]}


def ld(graph):
    j = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':'))
    j = j.replace('\u2014', '\\u2014').replace('</', '<\\/')  # client slogan keeps its exact dash, escaped
    return f'<script type="application/ld+json">{j}</script>'


# ---------- shared layout ----------
def nav():
    return [('services/', S.UI['nav_services']), ('about/', S.UI['nav_about']), ('articles/', S.UI['nav_articles']),
            ('contact/', S.UI['nav_contact'])]


def head(title, desc, path, graph, hero=False):
    css_v = ver(os.path.join(OUT, 'assets', 'site.css'))
    rob = '<meta name="robots" content="noindex, nofollow">' if NOINDEX else ''
    pre = f'<link rel="preload" as="image" href="{img("cover")}" type="image/webp" fetchpriority="high">' if hero else ''
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
<meta name="theme-color" content="#000000">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(F['short'])}">
{I18N.og_locale_tags(L)}
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{shu(I18N.page_path(L, path))}">
<meta property="og:image" content="{shu(OG)}">
<meta property="og:image:secure_url" content="{shu(OG)}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(S.CAPTIONS['og'])}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{shu(OG)}">
<link rel="icon" type="image/png" sizes="512x512" href="{u('images/favicon-512.png')}">
<link rel="apple-touch-icon" href="{u('images/favicon-512.png')}">
<link rel="preload" as="font" type="font/woff2" href="{u('assets/fonts/barlow-condensed-800.woff2')}" crossorigin>
{pre}
<link rel="stylesheet" href="{u('assets/site.css')}?v={css_v}">
{ld(graph)}
</head>
<body>
<a class="skip" href="#main">{E(S.UI['skip'])}</a>
'''


def header(active='', path=''):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{pu(p)}"{cur if active == p else ""}>{E(n)}</a>' for p, n in nav())
    sheet = ''.join(f'<a href="{pu(p)}">{E(n)}</a>' for p, n in [('', S.UI['nav_home'])] + nav())
    svc = ''.join(f'<a href="{pu("services/" + s["slug"] + "/")}">{E(s["name"])}</a>' for s in S.SERVICES)
    return f'''<header class="top">
<div class="top-in">
<a class="mark" href="{pu()}" aria-label="{E(S.UI['home_aria'])}"><img src="{u('images/logo-transparent.webp')}" width="2000" height="592" alt="{E(S.UI['logo_alt'])}"></a>
<nav class="nav" aria-label="{E(S.UI['aria_main'])}">{links}</nav>
{I18N.switcher(u, path, L, S.UI['lang_label'], 'pills')}
{wa('header', S.UI['wa_btn'], 'btn-wa sm hide-m')}
<button class="menu-b" type="button" aria-expanded="false" aria-controls="sheet" aria-label="{E(S.UI['menu'])}">{icon('menu')}</button>
</div>
</header>
<div class="sheet" id="sheet" hidden>
<div class="sheet-in">
<button class="sheet-x" type="button" aria-label="{E(S.UI['close'])}">{icon('x')}</button>
<nav class="sheet-nav" aria-label="{E(S.UI['aria_menu'])}">{sheet}</nav>
<nav class="sheet-svc" aria-label="{E(S.UI['nav_services'])}">{svc}</nav>
{I18N.switcher(u, path, L, S.UI['lang_label'], 'pills pills-lg')}
{wa('menu', S.UI['wa_btn_long'])}
</div>
</div>
'''


def loc_block(loc, tag, h, place):
    return (f'<div class="loc"><p class="loc-t"><span class="tag">{E(tag)}</span>{E(h)}</p><address>{E(loc["one_line"])}</address>'
            f'<p class="loc-l">{waze(loc, place)}{gmap(loc, place)}</p></div>')


def footer():
    js_v = ver(os.path.join(OUT, 'assets', 'site.js'))
    cta_v = ver(os.path.join(OUT, 'p1-cta.js'))
    pages = ''.join(f'<a href="{pu(p)}">{E(n)}</a>' for p, n in [('', S.UI['nav_home'])] + nav() + [('privacy/', S.UI['privacy'])])
    svc = ''.join(f'<a href="{pu("services/" + s["slug"] + "/")}">{E(s["name"])}</a>' for s in S.SERVICES)
    return f'''<footer class="foot">
<div class="foot-in">
<div class="foot-brand"><img src="{u('images/logo-transparent.webp')}" width="2000" height="592" alt="{E(S.UI['logo_alt'])}" loading="lazy">
<p class="foot-name">{E(F['name'])}</p><p class="foot-reg">{E(S.UI['reg_no'])} {E(F['company_no'])}</p></div>
<div class="foot-locs">{loc_block(HQ, S.UI['hq_tag'], S.UI['footer_hq'], 'footer')}{loc_block(SUB, S.UI['branch_tag'], S.UI['footer_subang'], 'footer')}</div>
<div class="foot-talk"><h2 class="foot-h">{E(S.UI['footer_talk'])}</h2>{wa('footer', S.UI['wa_btn_long'], 'lnk')}{call('footer', S.UI['call_btn_long'], 'lnk')}{fb('footer')}</div>
<div><h2 class="foot-h">{E(S.UI['nav_services'])}</h2><nav class="foot-nav" aria-label="{E(S.UI['nav_services'])}">{svc}</nav></div>
<div><h2 class="foot-h">{E(S.UI['footer_pages'])}</h2><nav class="foot-nav" aria-label="{E(S.UI['aria_pages'])}">{pages}</nav></div>
</div>
<div class="foot-base"><p>{E(S.UI['brands_note'])}</p><p class="credit"><a href="https://autoseo.my/">{S.UI['credit']}</a></p></div>
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
def frame(stem, cls='fr', eager=False, sizes='(min-width: 900px) 360px, 78vw'):
    w, h, fw, fh = PHOTOS[stem]
    cap = S.CAPTIONS[stem]
    lz = '' if eager else ' loading="lazy"'
    return (f'<figure class="{cls}"><button type="button" class="fr-b" data-full="{u("images/" + stem + "-full.webp")}" data-w="{fw}" data-h="{fh}" '
            f'data-cap="{E(cap)}" aria-label="{E(S.UI["photo_open"])}: {E(cap)}"><img src="{img(stem)}" width="{w}" height="{h}" '
            f'alt="{E(cap)}" decoding="async"{lz}></button><figcaption>{E(cap)}</figcaption></figure>')


def carousel(stems, label, place='work'):
    return (f'<div class="wr" data-place="{place}"><div class="wr-t" tabindex="0" role="region" aria-label="{E(label)}">'
            f'{"".join(frame(s, "fr wr-i") for s in stems)}</div>'
            f'<div class="wr-c"><button type="button" class="arr" data-dir="-1" aria-label="{E(S.UI["prev"])}">{icon("prev")}</button>'
            f'<div class="dots" aria-hidden="true">{"<i></i>" * len(stems)}</div>'
            f'<button type="button" class="arr" data-dir="1" aria-label="{E(S.UI["next"])}">{icon("next")}</button></div></div>')


def spec_strip(items, heading_level='h3'):
    rows = []
    for i, s in enumerate(items):
        w, h, _, _ = PHOTOS[s['photo']]
        rows.append(f'<li class="sp"><a href="{pu("services/" + s["slug"] + "/")}">'
                    f'<span class="sp-p"><img src="{img(s["photo"])}" width="{w}" height="{h}" alt="{E(S.CAPTIONS[s["photo"]])}" loading="lazy" decoding="async"></span>'
                    f'<span class="sp-x"><span class="sp-n">{i + 1:02d}</span><{heading_level} class="sp-h">{E(s["name"])}</{heading_level}>'
                    f'<span class="sp-l">{E(s["card_line"])}</span></span>{icon("go")}</a></li>')
    return f'<ol class="spec">{"".join(rows)}</ol>'


def circuit():
    ics = ['wa', 'scan', 'wrench', 'key']
    steps = ''.join(f'<li class="node"><span class="node-i">{icon(ics[i])}</span><div><h3>{E(t)}</h3><p>{E(d)}</p></div></li>'
                    for i, (t, d) in enumerate(S.HOME['process_steps']))
    return (f'<section class="sec circ"><div class="wrap"><h2>{E(S.HOME["process_h2"])}</h2>'
            f'<ol class="hv">{steps}</ol><p class="act">{wa("process", S.UI["wa_btn_long"])}</p></div></section>')


def reels():
    """Up to 6 Facebook reels in 9:16 embedded players (checked embeddable 19 Nov 2026), horizontal native scroll, lazy-loaded.
    Captions come from each reel's own Facebook caption (facts.json facebook_reels, strings REELS). No autoplay."""
    cards = []
    for i, r in enumerate(F['facebook_reels']['featured'][:6]):
        url = f'https://www.facebook.com/reel/{r["id"]}'
        cap = S.REELS[r['caption_key']]
        src = 'https://www.facebook.com/plugins/video.php?href=' + urllib.parse.quote(url, safe='') + '&show_text=false&width=270&height=480'
        cards.append(f'<li class="rl"><div class="rl-f"><iframe src="{E(src)}" title="{E(cap)}" loading="lazy" width="270" height="480" '
                     f'allow="encrypted-media; picture-in-picture; web-share" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe></div>'
                     f'<p class="rl-c">{E(cap)}</p><a class="rl-a" href="{E(url)}" target="_blank" rel="noopener" data-cta="facebook_reel_{i + 1}" '
                     f'data-ref="facebook_reel_{i + 1}">{icon("fb")}<span>{E(S.UI["watch_fb"])}</span></a></li>')
    return (f'<section class="sec reels"><div class="wrap"><h2>{E(S.HOME["reels_h2"])}</h2><p class="sub">{E(S.HOME["reels_line"])}</p></div>'
            f'<ul class="rls" aria-label="{E(S.HOME["reels_h2"])}">{"".join(cards)}</ul>'
            f'<div class="wrap"><p class="act">{fb("reels", S.UI["fb_btn"], "btn-line")}</p></div></section>')


def faq_block(faq, h2):
    items = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq)
    return f'<section class="sec faq"><div class="wrap narrow"><h2>{E(h2)}</h2>{items}</div></section>'


def ask_block(place):
    return (f'<section class="sec ask"><div class="wrap"><h2>{E(S.UI["ask_title"])}</h2><p>{E(S.UI["ask_line"])}</p>'
            f'<div class="act">{wa(place, S.UI["wa_btn_long"])}{call(place, S.UI["call_btn_long"])}</div></div></section>')


def page_head(h1, lead, trail):
    bc = ''.join(f'<a href="{pu(p)}">{E(n)}</a><span aria-hidden="true">/</span>' for n, p in trail[:-1]) + f'<span>{E(trail[-1][0])}</span>'
    return (f'<section class="ph"><div class="wrap"><nav class="bc" aria-label="{E(S.UI["aria_breadcrumb"])}">{bc}</nav>'
            f'<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p></div><span class="hvline" aria-hidden="true"></span></section>')


def visit_block(place):
    return (f'<section class="sec visit"><div class="wrap"><h2>{E(S.HOME["visit_h2"])}</h2><p class="sub">{E(S.HOME["visit_line"])}</p>'
            f'<div class="locs">{loc_block(HQ, S.UI["hq_tag"], S.UI["footer_hq"], place)}{loc_block(SUB, S.UI["branch_tag"], S.UI["footer_subang"], place)}</div>'
            f'<p class="areas"><span>{E(S.UI["areas_label"])}</span> {E(" / ".join(F["service_area"]))}</p>'
            f'<div class="act">{wa(place + "_visit", S.UI["wa_btn_long"])}</div></div></section>')


# ---------- pages ----------
def home():
    H = S.HOME
    hero = f'''<section class="bay">
<div class="bay-ph"><img src="{img('cover')}" width="1280" height="894" alt="{E(S.CAPTIONS['cover'])}" fetchpriority="high" decoding="async"></div>
<div class="bay-tx"><div class="wrap">
<h1>{E(H['h1'])}</h1>
<span class="hvline" aria-hidden="true"></span>
<p class="bay-l">{E(H['hero_line'])}</p>
<div class="bay-cta">{wa('home_hero', S.UI['wa_btn'])}{call('home_hero', S.UI['call_btn'], 'btn-call')}</div>
</div></div>
</section>'''
    brands = ''.join(f'<li>{E(b)}</li>' for b in F['brands_serviced'])
    intro = (f'<section class="sec intro"><div class="wrap split"><div><h2>{E(H["intro_h2"])}</h2>'
             + ''.join(f'<p>{E(p)}</p>' for p in H['intro_p'])
             + f'</div><div class="makes"><h3>{E(H["brands_label"])}</h3><ul>{brands}</ul></div></div></section>')
    spec = f'<section class="sec specs"><div class="wrap"><h2>{E(H["spec_h2"])}</h2>{spec_strip(S.SERVICES)}</div></section>'
    cars = ''.join(f'<li>{E(c)}</li>' for c in S.CARS)
    work = (f'<section class="sec work"><div class="wrap"><h2>{E(H["work_h2"])}</h2><p class="sub">{E(H["work_line"])}</p></div>'
            f'{carousel(CAROUSEL, H["work_h2"])}<div class="wrap"><h3 class="cars-h">{E(S.CARS_LABEL)}</h3><ul class="cars">{cars}</ul></div></section>')
    body = hero + intro + spec + circuit() + work + reels() + faq_block(S.FAQ_HOME, S.UI['faq_h2']) + visit_block('home')
    graph = [business(), branch(), {'@type': 'WebSite', 'name': F['short'], 'url': pabs(), 'inLanguage': L['hreflang']},
             {'@type': 'WebPage', 'name': H['title'], 'url': pabs(), 'inLanguage': L['hreflang'], 'about': {'@id': BIZ_ID}},
             faqld(S.FAQ_HOME)]
    return page('', H['title'], H['desc'], graph, body, '', True)


def service(s):
    path = f'services/{s["slug"]}/'
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_services'], 'services/'), (s['name'], path)]
    pid = s['id'].replace('-', '_')
    blocks = ''.join(f'<h2>{E(h)}</h2><p>{E(p)}</p>' for h, p in s['body'])
    cta = f'<div class="act">{wa("service_" + pid, S.UI["wa_btn_long"])}{call("service_" + pid, S.UI["call_btn"])}</div>'
    gal = f'<div class="gal">{"".join(frame(x, "fr", False, "(min-width: 900px) 280px, 44vw") for x in [s["photo"]] + s["photos"])}</div>'
    others = ''.join(f'<a href="{pu("services/" + o["slug"] + "/")}">{E(o["name"])}</a>' for o in S.SERVICES if o['id'] != s['id'])
    body = (page_head(s['h1'], s['lead'], trail)
            + f'<section class="sec"><div class="wrap split svc"><div class="prose">{blocks}{cta}</div><div class="media">{gal}</div></div></section>'
            + faq_block(s['faq'], S.UI['faq_h2'])
            + f'<section class="sec more"><div class="wrap"><h2>{E(S.UI["related"])}</h2><nav class="tabs" aria-label="{E(S.UI["related"])}">{others}</nav></div></section>'
            + ask_block('service_' + pid + '_end'))
    graph = [business(), crumbs(trail),
             {'@type': 'Service', 'name': s['name'], 'serviceType': s['name'], 'description': s['desc'], 'url': pabs(path),
              'provider': {'@id': BIZ_ID}, 'areaServed': [{'@type': 'City', 'name': c} for c in F['service_area']]},
             faqld(s['faq'])]
    return page(path, s['title'], s['desc'], graph, body, 'services/')


def services_index():
    X = S.SERVICES_INDEX
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_services'], 'services/')]
    jobs = ''.join(f'<li>{E(j)}</li>' for j in S.JOBS)
    body = (page_head(X['h1'], X['lead'], trail)
            + f'<section class="sec specs"><div class="wrap">{spec_strip(S.SERVICES, "h2")}</div></section>'
            + f'<section class="sec jobs"><div class="wrap narrow"><h2>{E(S.UI["jobs_h2"])}</h2><ul class="jl">{jobs}</ul></div></section>'
            + ask_block('services'))
    graph = [business(), crumbs(trail), {'@type': 'ItemList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': s['name'], 'url': pabs('services/' + s['slug'] + '/')} for i, s in enumerate(S.SERVICES)]}]
    return page('services/', X['title'], X['desc'], graph, body, 'services/')


def about():
    X = S.ABOUT
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_about'], 'about/')]
    blocks = ''.join(f'<h2>{E(h)}</h2><p>{E(p)}</p>' for h, p in X['body'])
    pts = ''.join(f'<li>{E(p)}</li>' for p in X['tag_points'])
    body = (page_head(X['h1'], X['lead'], trail)
            + f'<section class="sec motto"><div class="wrap"><h2 class="vh">{E(X["tag_h2"])}</h2><blockquote><p>{E(X["tag_main"])}</p><ul>{pts}</ul></blockquote></div></section>'
            + f'<section class="sec"><div class="wrap split"><div class="prose">{blocks}'
            + f'<p class="reg">{E(S.UI["reg_no"])} {E(F["company_no"])}</p></div>'
            + f'<div class="media"><div class="gal">{frame("supercar-service-bay-shah-alam")}{frame("volvo-xc90-t8-erad-bay")}</div></div></div></section>'
            + ask_block('about'))
    graph = [business(), branch(), crumbs(trail), {'@type': 'AboutPage', 'name': X['title'], 'url': pabs('about/'), 'about': {'@id': BIZ_ID}}]
    return page('about/', X['title'], X['desc'], graph, body, 'about/')


def contact():
    X = S.CONTACT
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_contact'], 'contact/')]
    body = (page_head(X['h1'], X['lead'], trail)
            + f'''<section class="sec"><div class="wrap split">
<div class="prose"><h2>{E(X['wa_h'])}</h2><p class="num"><a href="{TEL}" data-cta="call_contact_number" data-ref="call_contact_number">{E(F['whatsapp_display'])}</a></p>
<p>{E(X['wa_p'])}</p><div class="act">{wa('contact', S.UI['wa_btn_long'])}{call('contact', S.UI['call_btn'])}</div>
<p class="links">{fb('contact')}</p>
<h2>{E(X['hours_h'])}</h2><p>{E(X['hours_p'])}</p></div>
<div class="locs col">{loc_block(HQ, S.UI['hq_tag'], S.UI['footer_hq'], 'contact')}{loc_block(SUB, S.UI['branch_tag'], S.UI['footer_subang'], 'contact')}
<p class="areas"><span>{E(S.UI['areas_label'])}</span> {E(' / '.join(F['service_area']))}</p></div>
</div></section>''')
    graph = [business(), branch(), crumbs(trail), {'@type': 'ContactPage', 'name': X['title'], 'url': pabs('contact/'), 'about': {'@id': BIZ_ID}}]
    return page('contact/', X['title'], X['desc'], graph, body, 'contact/')


def privacy():
    X = S.PRIVACY
    trail = [(S.UI['nav_home'], ''), (S.UI['privacy'], 'privacy/')]
    blocks = ''.join(f'<h2>{E(h)}</h2><p>{E(p)}</p>' for h, p in X['body'])
    body = page_head(X['h1'], S.UI['last_updated'], trail) + f'<section class="sec"><div class="wrap narrow prose">{blocks}</div></section>'
    return page('privacy/', X['title'], X['desc'], [business(), crumbs(trail)], body)


def articles():
    X = S.ARTICLES
    trail = [(S.UI['nav_home'], ''), (S.UI['nav_articles'], 'articles/')]
    body = (page_head(X['h1'], X['lead'], trail)
            + '<section class="sec"><div class="wrap"><div class="art-list" id="articles"></div></div></section>' + ask_block('articles'))
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
    shutil.copy(os.path.join(HERE, 'p1-cta.js'), os.path.join(OUT, 'p1-cta.js'))
    os.makedirs(os.path.join(OUT, 'images'), exist_ok=True)
    shutil.copy(os.path.join(HERE, 'og.jpg'), os.path.join(OUT, 'images', 'og.jpg'))
    key = open(os.path.join(HERE, 'indexnow-key.txt')).read().strip()  # IndexNow key file at the docroot (public by design)
    open(os.path.join(OUT, key + '.txt'), 'w').write(key)  # share image (JPG 1200x630); other photos live on the server only
    names = [n for n in dir(strings_en) if n.isupper()]
    missing = [f'{c}: {n}' for c, mod in STRINGS.items() for n in names if not hasattr(mod, n)]
    for n in ('UI', 'CAPTIONS', 'HOME', 'REELS'):
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
    llms = f"""# {F['name']}

> {F['category']} in Shah Alam and Subang Jaya, Selangor, Malaysia. Company no. {F['company_no']}.

- Shah Alam HQ: {HQ['one_line']} (Waze {HQ['waze']})
- Subang Jaya branch: {SUB['one_line']} (Waze {SUB['waze']})
- WhatsApp and phone: {F['whatsapp_display_intl']} ({F['whatsapp_url']})
- Facebook: {FB}
- Makes serviced: {', '.join(F['brands_serviced'])}
- Areas: {', '.join(F['service_area'])}
- Opening hours: not published; WhatsApp to arrange a time

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
