"""Shared partials for the Sheng Heng Auto Service Centre site (template-first, rule 18).

Every page is rendered from these pieces; one edit here changes every page in EN, BM and 中文.
  facts.json  -> F (single data source)      site.json -> CFG (one-switch go-live config, rule 15)
  content_<lang>.json -> C[lang] (EN written once; BM/中文 from the cheap translation step, rule 6)
Pieces: head(), header(), lang_switch(), nav_sheet(), footer(), mobile_bar(), cta_row(), wa_url(),
service template + area template (build.py), faq_block(), ticket(), slider(), rail(), video_tile(), figure(),
schema builder (ld_business/ld_service/ld_faq/ld_crumbs), i18n strings (content_*.json).
"""
import json, os, sys, hashlib
from html import escape as E
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/mnt/project-files/autoseo-template/')
sys.path.insert(0, '/mnt/project-files/autoseo-template/golive/')
import golive as GL  # shared one-switch go-live module

F = json.load(open(os.path.join(HERE, 'facts.json')))
CFG = GL.load(os.path.join(HERE, 'site.json'))
SITE = json.load(open(os.path.join(HERE, 'site.json')))
LANGS = [
    {'code': 'en', 'prefix': '', 'hreflang': 'en', 'label': 'EN', 'og': 'en_MY'},
    {'code': 'ms', 'prefix': 'ms/', 'hreflang': 'ms', 'label': 'BM', 'og': 'ms_MY'},
    {'code': 'zh', 'prefix': 'zh/', 'hreflang': 'zh-Hans', 'label': '中文', 'og': 'zh_CN'},
]
C = {L['code']: json.load(open(os.path.join(HERE, f"content_{L['code']}.json"))) for L in LANGS}
P = CFG.base_path  # '/preview/sheng-heng-auto' on the preview host, '' when live
NOINDEX = (not CFG.live) and bool(SITE.get('noindex', True))
REVIEW_HELPER = 'review.html'


def u(path=''):
    return P + '/' + path.lstrip('/')


def lp(L, path=''):
    return u(L['prefix'] + path)


def vh(rel):
    with open(os.path.join(HERE, 'assets', rel), 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]


def asset(rel):
    return u('assets/' + rel) + '?v=' + vh(rel)


def ui(L, k):
    return C[L['code']]['ui'][k]


# ---------------------------------------------------------------- icons (one set, 1.75px stroke)
def _svg(d, extra=''):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{d}</svg>'

ICON = {
    'wa': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>',
    'call': _svg('<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>'),
    'mail': _svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
    'pin': _svg('<path d="M12 22s7-6.1 7-12a7 7 0 1 0-14 0c0 5.9 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/>'),
    'nav': _svg('<path d="m3 11 18-8-8 18-2-8-8-2z"/>'),
    'fb': _svg('<path d="M15 3h-2.5A3.5 3.5 0 0 0 9 6.5V9H7v3h2v9h3v-9h2.6l.4-3h-3V6.8c0-.5.4-.8.9-.8H15z"/>'),
    'menu': _svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    'close': _svg('<path d="M6 6l12 12M18 6 6 18"/>'),
    'arrow': _svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    'tick': _svg('<path d="M20 6 9 17l-5-5"/>'),
    'play': '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 4.5v15l12.5-7.5z"/></svg>',
    'card': _svg('<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M2.5 10h19M6.5 15h4"/>'),
    'clock': _svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
    'star': _svg('<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>'),
    # service icons
    'continental-car-specialist-skudai': _svg('<path d="M3 15.5V13l2-4.5A2 2 0 0 1 6.8 7h10.4a2 2 0 0 1 1.8 1.5L21 13v2.5a1 1 0 0 1-1 1h-1.5"/><path d="M5.5 16.5H4a1 1 0 0 1-1-1M9 16.5h6"/><circle cx="7.2" cy="16.5" r="1.8"/><circle cx="16.8" cy="16.5" r="1.8"/><path d="M4 12.5h16"/>'),
    'adas-calibration-skudai': _svg('<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/><path d="M12 1.5v3M12 19.5v3M1.5 12h3M19.5 12h3"/>'),
    'ecu-repair-programming-skudai': _svg('<rect x="6" y="6" width="12" height="12" rx="1.5"/><rect x="9.5" y="9.5" width="5" height="5" rx=".5"/><path d="M9 2.5V6M15 2.5V6M9 18v3.5M15 18v3.5M2.5 9H6M2.5 15H6M18 9h3.5M18 15h3.5"/>'),
    'car-key-immobilizer-skudai': _svg('<circle cx="8" cy="15.5" r="4.5"/><path d="m11.2 12.3 8.3-8.3M16 7.5l2.5 2.5M18.5 5l2 2"/>'),
    'car-coding-instrument-cluster-skudai': _svg('<path d="M3.5 17a8.5 8.5 0 1 1 17 0"/><path d="m12 17 4-5.5"/><circle cx="12" cy="17" r="1.3"/><path d="M6.5 13.5l1 .6M12 8.5v1.2M17.5 13.5l-1 .6"/>'),
    'gearbox-overhaul-skudai': _svg('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>'),
    'car-diagnostic-skudai': _svg('<path d="M2.5 12h4l2.5-6 4 12 2.5-6h6"/>'),
    'car-service-skudai': _svg('<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9z"/>'),
    # dashboard lamps (process)
    'lamp-check': _svg('<path d="M5 15.5V9.5L7.5 7h2l1-1.5H15l1 1.5h2v3h1.5v-1H21v5.5h-1.5v-1H18v3h-3.5L13 18H7.5L5 15.5z"/><path d="M2.5 11v4M5 13H2.5"/>'),
    'lamp-scan': _svg('<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M6 11h2l1.5-3 3 6 1.5-3h4M8 20h8"/>'),
    'lamp-quote': _svg('<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>'),
    'lamp-road': _svg('<path d="M8 3 5 21M16 3l3 18M12 4v2.5M12 10v3M12 17v3"/>'),
}


def icon(k):
    return ICON[k]


# ---------------------------------------------------------------- media (real client photos, manifest sizes)
M = {
    'h01': ('hero/h01-storefront-hang-lekir', [(480, 300), (800, 500)], 'r1610', '50% 55%'),
    'g01': ('gallery/g01-adas-calibration-bay', [(480, 600), (726, 908)], 'r45', '50% 50%'),
    'g02': ('gallery/g02-bmw-on-lift', [(480, 600), (688, 860)], 'r45', '50% 50%'),
    'g03': ('gallery/g03-b48-valve-seal', [(480, 600), (739, 924)], 'r45', '50% 50%'),
    'g04': ('gallery/g04-m-steering-wheel', [(480, 600), (800, 1000)], 'r45', '50% 50%'),
    'g05': ('gallery/g05-bmw-steering-wheel-before', [(480, 600), (800, 1000)], 'r45', '50% 50%'),
    'g06': ('gallery/g06-gearbox-oem-vs-ori-plates', [(480, 600), (800, 1000)], 'r45', '50% 50%'),
    'g07': ('gallery/g07-gearbox-final-gear-bearings', [(480, 600), (800, 1000)], 'r45', '50% 50%'),
    'w01': ('wide/w01-pre-collision-warning', [(800, 450), (1280, 720)], 'r169', '50% 50%'),
    'w02': ('wide/w02-alphard-full-service', [(800, 450), (1280, 720)], 'r169', '50% 50%'),
    'w03': ('wide/w03-steering-before-after', [(800, 500), (1240, 775)], 'r1610', '50% 50%'),
    'w04': ('wide/w04-turbo-pair', [(480, 360), (880, 660)], 'r43', '50% 50%'),
    'w05': ('wide/w05-gearbox-clutch-plate', [(640, 480), (1080, 810)], 'r43', '50% 50%'),
    'p01b': ('pairs/p01-mercedes-meter-before', [(480, 360), (700, 525)], 'r43', '50% 50%'),
    'p01a': ('pairs/p01-mercedes-meter-after', [(480, 360), (700, 525)], 'r43', '50% 50%'),
    'p02b': ('pairs/p02-bmw3-cluster-before', [(480, 480), (700, 700)], 'r11', '50% 50%'),
    'p02a': ('pairs/p02-bmw3-cluster-after', [(480, 480), (700, 700)], 'r11', '50% 50%'),
}
ORDER = ['continental-car-specialist-skudai', 'adas-calibration-skudai', 'ecu-repair-programming-skudai', 'car-key-immobilizer-skudai',
         'car-coding-instrument-cluster-skudai', 'gearbox-overhaul-skudai', 'car-diagnostic-skudai', 'car-service-skudai']
THUMB = {'continental-car-specialist-skudai': 'g02', 'adas-calibration-skudai': 'g01', 'ecu-repair-programming-skudai': 'p02a',
         'car-key-immobilizer-skudai': 'g05', 'car-coding-instrument-cluster-skudai': 'g04', 'gearbox-overhaul-skudai': 'g06',
         'car-diagnostic-skudai': 'w01', 'car-service-skudai': 'w02'}
SHORT = {'continental-car-specialist-skudai': 'continental', 'adas-calibration-skudai': 'adas', 'ecu-repair-programming-skudai': 'ecu',
         'car-key-immobilizer-skudai': 'key', 'car-coding-instrument-cluster-skudai': 'coding', 'gearbox-overhaul-skudai': 'gearbox',
         'car-diagnostic-skudai': 'diagnostic', 'car-service-skudai': 'service'}


def img_url(mid, w):
    base, sizes, _, _ = M[mid]
    return u(f'images/{base}-{w}.webp')


def img(L, mid, sizes='(min-width:900px) 560px, 100vw', eager=False, cls=''):
    base, sz, ratio, pos = M[mid]
    alt = C[L['code']]['img'][mid]['alt']
    srcset = ', '.join(f'{u("images/%s-%d.webp" % (base, w))} {w}w' for w, h in sz)
    w, h = sz[0]
    load = 'fetchpriority="high" loading="eager"' if eager else 'loading="lazy" decoding="async"'
    style = f' style="object-position:{pos}"' if pos != '50% 50%' else ''
    c = f' class="{cls}"' if cls else ''
    return f'<img src="{u("images/%s-%d.webp" % (base, w))}" srcset="{srcset}" sizes="{sizes}" width="{w}" height="{h}" alt="{E(alt)}" {load}{style}{c}>'


def figure(L, mid, sizes='(min-width:900px) 560px, 100vw', eager=False, caption=True, extra_cls=''):
    ratio = M[mid][2]
    cap = f'<figcaption>{E(C[L["code"]]["img"][mid]["caption"])}</figcaption>' if caption else ''
    return f'<figure class="fig {ratio} {extra_cls}">{img(L, mid, sizes, eager)}{cap}</figure>'


def slider(L, pair, cap_key=None):
    """Before/after drag slider (range input: finger, mouse, keyboard). Both images share the pair's own frame."""
    b, a = pair + 'b', pair + 'a'
    ratio = M[b][2]
    lab = ui(L, 'slider_label')
    cap = C[L['code']]['home'].get(cap_key) if cap_key else C[L['code']]['img'][a]['caption']
    return (f'<div class="ba {ratio}">{img(L, a, "(min-width:900px) 560px, 100vw")}'
            f'{img(L, b, "(min-width:900px) 560px, 100vw", cls="b4")}'
            f'<span class="lbl l">{E(ui(L, "before"))}</span><span class="lbl r">{E(ui(L, "after"))}</span>'
            f'<input type="range" min="0" max="100" value="50" aria-label="{E(lab)}"><span class="hdl"></span>'
            f'<span class="cap">{E(cap)}</span></div>')


def w03(L):
    return (f'<figure class="fig r1610 w03">{img(L, "w03", "(min-width:900px) 1100px, 100vw")}'
            f'<span class="lbl l">{E(ui(L, "before"))}</span><span class="lbl r">{E(ui(L, "after"))}</span>'
            f'<figcaption>{E(C[L["code"]]["img"]["w03"]["caption"])}</figcaption></figure>')


def video_tile(L, ref='video_adas_fbreel', dark=False):
    """9:16 tile, poster + play icon from first paint, never an empty player. Self-hosted mp4 when it returns 200,
    otherwise a tap opens the Facebook reel in a new tab."""
    c = C[L['code']]
    poster = u('images/video/v01-bmw-adas-calibration-poster-720.webp')
    pimg = f'<img src="{poster}" width="720" height="1280" alt="{E(c["img"]["v01"]["alt"])}" loading="lazy" decoding="async">'
    pl = f'<span class="pl">{icon("play")}</span>'
    if SITE.get('video_mp4_live'):
        el = f'<button class="vf" type="button" data-src="{u(SITE["video_mp4"])}" aria-label="{E(ui(L, "play"))}" data-cta="video" data-ref="video_adas_play">{pimg}{pl}</button>'
        extra = ''
    else:
        el = f'<a class="vf" href="{E(F["fb_reel"])}" target="_blank" rel="noopener" aria-label="{E(ui(L, "play"))}" data-cta="facebook" data-ref="{ref}">{pimg}{pl}</a>'
        extra = ''
    return f'<figure class="vt">{el}<figcaption>{E(c["img"]["v01"]["caption"])}</figcaption>{extra}</figure>'


# ---------------------------------------------------------------- CTAs
def wa_url(text):
    return f'https://wa.me/{F["whatsapp"]["wa"]}?text={quote(text)}'


def wa_a(L, text, ref, label=None, cls='btn btn-wa'):
    lab = label or ui(L, 'wa')
    return f'<a class="{cls}" href="{E(wa_url(text))}" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="{ref}">{icon("wa")}<span>{E(lab)}</span></a>'


def call_a(L, ref, label=None, cls='btn btn-call', second=False):
    num = F['phone2'] if second else F['phone']
    lab = label or ui(L, 'call')
    return f'<a class="{cls}" href="tel:{num["e164"]}" data-cta="call" data-ref="{ref}">{icon("call")}<span>{E(lab)}</span></a>'


def cta_row(L, text, place, extra=''):
    return f'<div class="ctas">{wa_a(L, text, "whatsapp_" + place)}{call_a(L, "call_" + place)}{extra}</div>'


def review_href(L):
    q = '?business=sheng-heng-auto' + ('' if L['code'] == 'en' else '&lang=' + L['code'])
    return u(REVIEW_HELPER) + q


def review_btn(L, ref, cls='btn btn-call btn-sm'):
    return f'<a class="{cls}" href="{E(review_href(L))}" target="_blank" rel="noopener" data-cta="review" data-ref="{ref}">{icon("star")}<span>{E(ui(L, "review_btn"))}</span></a>'


# ---------------------------------------------------------------- schema builder
def _abs(path):
    return CFG.canon(path)


def ld_business(L):
    c = C[L['code']]
    areas = [{'@type': 'Place', 'name': n} for a in F['areas'] for n, _ in a['places']] + [{'@type': 'Place', 'name': 'Skudai, Johor'}]
    return {
        '@type': 'AutoRepair', '@id': GL.jsonld_id(CFG), 'name': F['name'], 'alternateName': F['alternate_name'],
        'legalName': F['legal_name'], 'foundingDate': F['founded'], 'slogan': F['tagline'],
        'url': _abs(L['prefix']), 'telephone': F['phone']['e164'], 'email': F['email'],
        'image': [CFG.og_image(), _abs('images/hero/h01-storefront-hang-lekir-800.webp')],
        'logo': _abs('images/brand/logo-sheng-heng-auto-960.png'),
        'address': {'@type': 'PostalAddress', 'streetAddress': F['address']['street'], 'addressLocality': F['address']['locality'],
                    'addressRegion': F['address']['region'], 'postalCode': F['address']['postcode'], 'addressCountry': 'MY'},
        'geo': {'@type': 'GeoCoordinates', 'latitude': F['geo']['lat'], 'longitude': F['geo']['lng']},
        'hasMap': F['maps_url'],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': F['hours']['days'],
                                       'opens': F['hours']['opens'], 'closes': F['hours']['closes']}],
        'contactPoint': [{'@type': 'ContactPoint', 'telephone': F['phone']['e164'], 'contactType': 'customer service', 'availableLanguage': ['en', 'ms', 'zh']},
                         {'@type': 'ContactPoint', 'telephone': F['phone2']['e164'], 'contactType': 'customer service'}],
        'areaServed': areas, 'sameAs': [F['cid_url'], F['facebook']], 'knowsLanguage': ['en', 'ms', 'zh'],
        'paymentAccepted': 'AhaPay instalment',
    }


def ld_crumbs(L, items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': _abs(L['prefix'] + p)} for i, (n, p) in enumerate(items)]}


def ld_faq(faqs):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': q['a']}} for q in faqs]}


def ld_service(L, slug, path):
    s = C[L['code']]['services'][slug]
    return {'@type': 'Service', 'name': s['schema_name'], 'description': s['schema_desc'], 'serviceType': s['schema_name'],
            'url': _abs(L['prefix'] + path), 'provider': {'@id': GL.jsonld_id(CFG)},
            'areaServed': [{'@type': 'Place', 'name': 'Skudai, Johor'}]}


def ld(L, *nodes):
    g = {'@context': 'https://schema.org', '@graph': [n for n in nodes if n]}
    return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False).replace('</', '<\\/') + '</script>'


# ---------------------------------------------------------------- head
def head(L, path, title, meta, ldjson, preload_hero=False):
    c = C[L['code']]
    robots = '<meta name="robots" content="noindex, nofollow">\n' if NOINDEX else ''
    alt_loc = ''.join(f'\n<meta property="og:locale:alternate" content="{o["og"]}">' for o in LANGS if o is not L)
    pre = ''
    if preload_hero:
        pre = (f'<link rel="preload" as="image" href="{img_url("h01", 480)}" imagesrcset="{img_url("h01", 480)} 480w, {img_url("h01", 800)} 800w" '
               f'imagesizes="(min-width:1024px) 640px, 100vw" fetchpriority="high">\n')
    return f'''<!doctype html>
<html lang="{L["hreflang"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(meta)}">
{robots}{GL.head_tags(CFG, path, L["code"])}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(F["name"])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta)}">
<meta property="og:image:alt" content="{E(c["ui"]["share_alt"])}">
<meta property="og:locale" content="{L["og"]}">{alt_loc}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(meta)}">
<meta name="twitter:image:alt" content="{E(c["ui"]["share_alt"])}">
<meta name="theme-color" content="#1F4FA8">
<link rel="icon" type="image/png" sizes="32x32" href="{u("images/brand/icon-sh-32.png")}">
<link rel="apple-touch-icon" href="{u("images/brand/icon-sh-192.png")}">
<link rel="manifest" href="{u("site.webmanifest")}">
<link rel="preload" as="font" type="font/woff2" href="{u("assets/fonts/saira.woff2")}" crossorigin>
{pre}<link rel="stylesheet" href="{asset("site.css")}">
{ldjson}
</head>
'''


# ---------------------------------------------------------------- header, language switch, nav sheet
def lang_switch(L, path):
    out = []
    for o in LANGS:
        cur = ' aria-current="true"' if o is L else ''
        out.append(f'<a href="{lp(o, path)}" hreflang="{o["hreflang"]}" lang="{o["hreflang"]}"{cur}>{o["label"]}</a>')
    return f'<nav class="lsw" aria-label="{E(ui(L, "lang_label"))}">{"".join(out)}</nav>'


def nav_items(L):
    c = C[L['code']]
    return [(ui(L, 'nav_home'), ''), (ui(L, 'nav_services'), ORDER[0] + '/'), (ui(L, 'nav_areas'), 'areas/' + F['areas'][0]['slug'] + '/'),
            (ui(L, 'nav_about'), 'about/'), (ui(L, 'nav_contact'), 'contact/'), (ui(L, 'nav_articles'), 'articles/')]


def logo_img(L, h=46):
    return f'<img src="{u("images/brand/logo-sheng-heng-auto-480.webp")}" width="480" height="372" alt="{E(C[L["code"]]["img"]["logo"]["alt"])}">'


def header(L, path):
    c = C[L['code']]
    desk = ''.join(f'<a href="{lp(L, p)}"{" aria-current=\"page\"" if p == path else ""}>{E(n)}</a>' for n, p in nav_items(L) if p not in ('', 'articles/'))
    return f'''<a class="skip" href="#main">{E(ui(L, "skip"))}</a>
<header class="hd"><div class="wrap">
<a class="logo" href="{lp(L, "")}">{logo_img(L)}</a>
<nav class="nav" aria-label="Main">{desk}</nav>
{wa_a(L, c["wa_generic"], "whatsapp_header", label=ui(L, "wa"), cls="btn btn-wa btn-sm hd-wa")}
{lang_switch(L, path)}
<button class="mbtn" id="mopen" type="button" aria-controls="sheet" aria-expanded="false" aria-label="{E(ui(L, "menu"))}">{icon("menu")}</button>
</div></header>
{nav_sheet(L, path)}'''


def nav_sheet(L, path):
    c = C[L['code']]
    sv = ''.join(f'<a class="sl" href="{lp(L, s + "/")}"><span>{E(c["services"][s]["nav"])}</span>{icon("arrow")}</a>' for s in ORDER)
    ar = ''.join(f'<a class="sl" href="{lp(L, "areas/" + a["slug"] + "/")}"><span>{E(c["areas"][a["slug"]]["nav"])}</span>{icon("arrow")}</a>' for a in F['areas'])
    main = ''.join(f'<a class="sl" href="{lp(L, p)}"><span>{E(n)}</span>{icon("arrow")}</a>' for n, p in nav_items(L) if p in ('', 'about/', 'contact/', 'articles/'))
    return f'''<div class="sheet" id="sheet" aria-hidden="true" role="dialog" aria-modal="true" aria-label="{E(ui(L, "menu"))}">
<div class="sheet-top"><a href="{lp(L, "")}">{logo_img(L)}</a><button class="mbtn" id="mclose" type="button" aria-label="{E(ui(L, "close"))}">{icon("close")}</button></div>
<div class="sheet-body">{main}<h3>{E(ui(L, "nav_services"))}</h3>{sv}<h3>{E(ui(L, "nav_areas"))}</h3>{ar}
<div class="sheet-cta">{wa_a(L, c["wa_generic"], "whatsapp_menu", label=ui(L, "wa_long"))}{call_a(L, "call_menu", label=ui(L, "call_long"))}</div></div></div>'''


# ---------------------------------------------------------------- footer + sticky bar
def hours_rows(L):
    return (f'<tr><th scope="row">{E(ui(L, "hours_week"))}</th><td>{E(ui(L, "hours_time"))}</td></tr>'
            f'<tr><th scope="row">{E(ui(L, "hours_sun"))}</th><td>{E(ui(L, "hours_closed"))}</td></tr>')


def footer(L, path):
    c = C[L['code']]
    svc = ''.join(f'<li><a href="{lp(L, s + "/")}">{E(c["services"][s]["nav"])}</a></li>' for s in ORDER)
    ar = ''.join(f'<li><a href="{lp(L, "areas/" + a["slug"] + "/")}">{E(c["areas"][a["slug"]]["nav"])}</a></li>' for a in F['areas'])
    cr = F['footer_credit']
    return f'''<footer class="ft"><div class="wrap">
<span class="badge">{logo_img(L)}</span>
<div class="fcols">
<div><h3>{E(ui(L, "visit_h"))}</h3><ul>
<li>{E(F["address"]["display"])}</li>
<li>{E(ui(L, "hours_week"))}: {E(ui(L, "hours_time"))}<br><small>{E(ui(L, "hours_sun"))}: {E(ui(L, "hours_closed"))} ({E(ui(L, "hours_tz"))})</small></li>
<li><a href="{E(F["maps_url"])}" target="_blank" rel="noopener" data-cta="map" data-ref="map_footer">{E(ui(L, "open_maps"))}</a></li>
<li><a href="{E(F["directions_url"])}" target="_blank" rel="noopener" data-cta="directions" data-ref="directions_footer">{E(ui(L, "directions"))}</a></li>
</ul></div>
<div><h3>{E(ui(L, "talk_h"))}</h3><ul>
<li><a href="{E(wa_url(c["wa_generic"]))}" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="whatsapp_footer">WhatsApp {E(F["whatsapp"]["display"])}</a> <small>({E(F["contact_person"])})</small></li>
<li><a href="tel:{F["phone"]["e164"]}" data-cta="call" data-ref="call_footer">{E(ui(L, "call"))} {E(F["phone"]["display"])}</a></li>
<li><a href="tel:{F["phone2"]["e164"]}" data-cta="call" data-ref="call_second_line_footer">{E(ui(L, "second_line"))} {E(F["phone2"]["display"])}</a></li>
<li><a href="mailto:{F["email"]}" data-cta="email" data-ref="email_footer">{E(F["email"])}</a></li>
<li><a href="{E(F["facebook"])}" target="_blank" rel="noopener" data-cta="facebook" data-ref="facebook_footer">{E(ui(L, "facebook"))}</a></li>
<li><small>{E(ui(L, "ahapay"))}</small></li>
</ul></div>
<div><h3>{E(ui(L, "services_h"))}</h3><ul class="svc">{svc}</ul>
<h3 style="margin-top:18px">{E(ui(L, "areas_h"))}</h3><ul class="svc">{ar}</ul></div>
</div>
<a class="frev" href="{E(review_href(L))}" target="_blank" rel="noopener" data-cta="review" data-ref="review_footer"><img src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png" alt="Google" height="24" width="71" loading="lazy">{E(ui(L, "review_footer"))}</a>
<div class="fbot"><span>{E(ui(L, "legal"))} · {E(ui(L, "est"))}</span>
<span><a href="{lp(L, "privacy/")}">{E(ui(L, "privacy"))}</a> · <a href="{E(cr["url"])}" target="_blank" rel="noopener">{E(cr["text"])}</a></span></div>
</div></footer>
<div class="mbar">{wa_a(L, c["wa_generic"], "whatsapp_mobile_bar", label=ui(L, "wa"))}{call_a(L, "call_mobile_bar")}</div>
<script src="{asset("site.js")}" defer></script>
<script src="{asset("p1-cta.js")}" defer></script>
</body>
</html>
'''


# ---------------------------------------------------------------- blocks
def faq_block(L, faqs):
    if not faqs:
        return ''
    items = ''.join(f'<details><summary>{E(q["q"])}</summary><div class="a"><p>{E(q["a"])}</p></div></details>' for q in faqs)
    return f'<section class="sec faq" id="faq"><div class="wrap"><h2>{E(ui(L, "faq_h"))}</h2>{items}</div></section>'


def ticket(L, r, i):
    tag = C[L['code']].get('review_tags', {}).get(str(i)) if r.get('tag') else None
    t = f'<span class="tag">{E(tag)}</span>' if tag else ''
    return (f'<li class="tk">{t}<blockquote lang="en"><p>“{E(r["text"])}”</p></blockquote>'
            f'<div class="who">{E(r["name"])}<span>Google</span></div></li>')


def tickets(L, idx=None):
    rs = F['reviews']
    pick = idx if idx is not None else range(len(rs))
    return '<ul class="tickets">' + ''.join(ticket(L, rs[i], i + 1) for i in pick) + '</ul>'


def rail(L, ids=('g01', 'g02', 'g03', 'g04', 'g05', 'g06', 'g07')):
    lis = ''.join(f'<li>{figure(L, m, "(min-width:900px) 270px, 62vw")}</li>' for m in ids)
    return f'<ul class="rail" data-auto aria-label="{E(ui(L, "carousel_label"))}">{lis}</ul>'


def crumbs(L, items):
    lis = ''.join((f'<li><a href="{lp(L, p)}">{E(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{E(n)}</li>') for i, (n, p) in enumerate(items))
    return f'<ol class="crumbs">{lis}</ol>'


def visit_block(L, ref='findus'):
    c = C[L['code']]
    return f'''<div class="visit">
<div><div class="map"><iframe src="{E(F["embed_url"])}" title="{E(ui(L, "map_title"))}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<p class="map-fb"><a href="{E(F["maps_url"])}" target="_blank" rel="noopener" data-cta="map" data-ref="map_{ref}">{E(ui(L, "map_fallback"))}</a></p></div>
<div class="card info"><h3>{E(ui(L, "address_h"))}</h3><address>{E(F["address"]["display"])}</address>
<table class="hrs"><caption class="sr">{E(ui(L, "hours_h"))}</caption>{hours_rows(L)}</table>
<p class="aha">{icon("card")}{E(ui(L, "ahapay"))}</p>
<div class="ctas three">{wa_a(L, c["wa_generic"], "whatsapp_" + ref, label=ui(L, "wa"))}{call_a(L, "call_" + ref)}<a class="btn btn-red" href="{E(F["directions_url"])}" target="_blank" rel="noopener" data-cta="directions" data-ref="directions_{ref}">{icon("nav")}<span>{E(ui(L, "directions"))}</span></a></div>
</div></div>'''


def svc_list(L, current=None, two=True):
    c = C[L['code']]
    lis = ''.join(f'<li><a href="{lp(L, s + "/")}"{" aria-current=\"page\"" if s == current else ""}>{icon(s)}<span>{E(c["services"][s]["nav"])}</span></a></li>' for s in ORDER)
    return f'<ul class="svlist{" two" if two else ""}">{lis}</ul>'


def area_chips(L, current=None):
    c = C[L['code']]
    out = []
    for a in F['areas']:
        on = ' on' if a['slug'] == current else ''
        km = ui(L, 'about_km').format(km=a['chip_km'])
        out.append(f'<li><a class="chip{on}" href="{lp(L, "areas/" + a["slug"] + "/")}">{E(c["areas"][a["slug"]]["nav"])} <small>{E(km)}</small></a></li>')
    return '<ul class="chips">' + ''.join(out) + '</ul>'


def mid_cta(L, text, ref):
    return f'''<section class="midcta"><div class="wrap"><div class="card stripe"><h2>{E(ui(L, "cta_mid_h"))}</h2><p>{E(ui(L, "cta_mid_p"))}</p>
<div class="ctas">{wa_a(L, text, "whatsapp_" + ref)}{call_a(L, "call_" + ref)}</div></div></div></section>'''


def end_cta(L, text, ref):
    return f'''<section class="band ice"><div class="wrap"><h2>{E(ui(L, "cta_end_h"))}</h2><p class="sub">{E(ui(L, "cta_end_p"))}</p>
<div class="ctas">{wa_a(L, text, "whatsapp_" + ref)}{call_a(L, "call_" + ref)}</div></div></section>'''
