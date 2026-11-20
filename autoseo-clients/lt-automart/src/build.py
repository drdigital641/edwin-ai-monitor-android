#!/usr/bin/env python3
"""LT Automart site builder (AutoSEO.my client, 20 Nov 2026). Full site, EN at root, BM at /ms/, 中文 at /zh/.

One template set for every page: head, header, menu sheet, footer, floating bar, CTA links and schema live here once,
so one edit updates every page in every language. Facts: facts.json. Photos: media.json (from the Bridge drop manifest).
Copy: strings_en/ms/zh.py (same keys, checked). Services: ONE list (SERVICES below + strings SV) drives the home
upgrade menu, the services hub, every service page, the footer, sitemap.xml and llms.txt.

ONE-SWITCH GO-LIVE: site.json is the only place a host lives. canonical, hreflang, og:url, og:image, twitter:image,
JSON-LD url/@id, sitemap.xml, robots.txt and llms.txt all come from shared/golive.py (copy of autoseo-template/golive).
While live_domain is empty, every URL is the preview URL. No domain is written into any page by hand.
Preview noindex is host-based (X-Robots-Tag from the preview host .htaccess), so pages carry no robots meta.

  python3 build.py            -> ../dist
  python3 build.py --fonts    -> also refresh the Noto Sans SC subset (Google Fonts text= subset)
  python3 check.py            -> pre-upload gate
Upload: Bridge sync_from_github, site autoseo, source autoseo-clients/lt-automart/dist, base_path preview/lt-automart.
Full-size photos are placed on the server from Bridge drops 6b004343 + 6b004381 (media/<stem>.webp|.jpg); this build
ships only the smaller -600/-800/-420 WebP copies made from them."""
import hashlib, html, json, os, re, shutil, sys, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'shared'))
sys.path.insert(0, HERE)
import autoseo_i18n as I18N
import golive as GL
import strings_en, strings_ms, strings_zh

STRINGS = {'en': strings_en, 'ms': strings_ms, 'zh': strings_zh}
LIDX = {'en': 3, 'ms': 4, 'zh': 5}  # alt text column in media.json
S, L = strings_en, I18N.LANGS[0]
CFG = GL.load(os.path.join(HERE, 'site.json'))
F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
M = json.load(open(os.path.join(HERE, 'media.json'), encoding='utf8'))
BASE = CFG.preview_path if not CFG.live else '/'  # root-relative hrefs: '/preview/lt-automart/' now, '/' once live
OUT = os.path.join(HERE, '..', 'dist')
E = html.escape
LK = F['links']
NAME = F['name']
TODAY = '2026-11-20'

# ---------- the one services list ----------
# id: (page slug or None for hub-only, main photo or None, gallery photos, reel posters)
SERVICES = [
    ('audio', 'car-audio', 'audio-wall-team', ['jbl-audio-display', 'soundproofing-door'], ['reel-jbl-display-poster']),
    ('android', 'android-player-360-camera', 'android-player-alphard', ['android-player-vellfire', 'alphard-cockpit-upgrade'], []),
    ('mpv', 'alphard-vellfire-upgrades', 'alphard-cockpit-upgrade', ['gr-steering-wheel', 'marble-flooring-panels', 'leather-interior-retrim', 'alphard-rear-lt-plate'],
     ['reel-pilot-seats-poster', 'reel-console-box-poster', 'reel-estima-console-poster']),
    ('bmw', 'bmw-conversions', None, ['boot-spoiler-fitting', 'alphard-rear-lt-plate'], []),
    ('bodykit', 'body-kits', 'alphard-rear-lt-plate', ['boot-spoiler-fitting', 'alphard-cockpit-upgrade'], []),
    ('lighting', 'car-lighting', 'ambient-light-install-card', ['ambient-light-install-wide'], []),
    ('tint', 'window-tint', 'shopfront-night-hero', ['shopfront-sign-wide'], []),
    ('soundproof', 'soundproofing', 'soundproofing-door', ['audio-wall-team', 'jbl-audio-display'], []),
    ('service', None, None, [], []),
]
SV = {s[0]: {'slug': s[1], 'photo': s[2], 'gallery': s[3], 'reels': s[4]} for s in SERVICES}
PAGE_SERVICES = [s[0] for s in SERVICES if s[1]]
MENU = ['audio', 'android', 'mpv', 'bodykit', 'lighting', 'tint', 'soundproof']  # home upgrade menu chips
BMW_MARK = 'F10 → G30'
REEL_URL = {r['stem']: r['url'] for r in F['reels']}
CAROUSEL = ['android-player-alphard', 'alphard-cockpit-upgrade', 'ambient-light-install-card', 'soundproofing-door', 'gr-steering-wheel',
            'boot-spoiler-fitting', 'jbl-audio-display', 'android-player-vellfire', 'marble-flooring-panels', 'alphard-rear-lt-plate', 'leather-interior-retrim']


def spath(sid):
    return f"services/{SV[sid]['slug']}/"


PAGES = ['', 'services/'] + [spath(s) for s in PAGE_SERVICES] + ['contact/', 'articles/', 'privacy/']
SMALL = {}
for f in os.listdir(os.path.join(HERE, 'media')):
    m = re.match(r'(.+)-(\d+)\.webp$', f)
    if m and m.group(1) in M:
        SMALL[m.group(1)] = int(m.group(2))


def u(p=''):
    return BASE + p


def pu(p=''):
    return u(I18N.page_path(L, p))


def canon(p=''):
    return CFG.canon(I18N.page_path(L, p))


def ver(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]


def alt(stem):
    return M[stem][LIDX[L['code']]]


def wa_url(text):
    return f"{F['whatsapp']['url']}?text={urllib.parse.quote(text)}"


def icon(name):
    p = {
        'wa': '<path d="M4.6 19.4l1.1-3.5a7.9 7.9 0 1 1 2.9 2.7z"/><path d="M9.3 8.7c.3 2.5 2.3 4.7 5 5.2l.9-1.1 1.8.8-.3 1.5c-3.8.4-7.7-3.5-7.5-7.3l1.5-.3.8 1.7z"/>',
        'call': '<path d="M5.2 4h3.6l1.6 4-2.1 1.3a10.6 10.6 0 0 0 6.4 6.4l1.3-2.1 4 1.6v3.6a1.6 1.6 0 0 1-1.7 1.6C10.4 19.9 4.1 13.6 3.6 5.7A1.6 1.6 0 0 1 5.2 4z"/>',
        'pin': '<path d="M12 21s-6.4-5.5-6.4-10.9a6.4 6.4 0 0 1 12.8 0C18.4 15.5 12 21 12 21z"/><circle cx="12" cy="10.1" r="2.2"/>',
        'nav': '<path d="M20 4L3.5 10.6l7 2.6 2.6 7z"/>',
        'menu': '<path d="M4 7h16M4 12h11M4 17h16"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
        'prev': '<path d="M15 5l-7 7 7 7"/>', 'next': '<path d="M9 5l7 7-7 7"/>', 'go': '<path d="M5 12h13M13 6l6 6-6 6"/>',
        'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
        'play': '<path d="M8 5.2v13.6L19 12z"/>',
        'fb': '<path d="M14 8.5h2.5V5H14a3.5 3.5 0 0 0-3.5 3.5V11H8v3.5h2.5V21H14v-6.5h2.5L17 11h-3V8.5z"/>',
        'tt': '<path d="M14 3.5v11a3.5 3.5 0 1 1-3.5-3.5"/><path d="M14 3.5c.5 2.6 2.4 4.4 5 4.6"/>',
        'quote': '<path d="M5 18v-5a6 6 0 0 1 4-5.7M14 18v-5a6 6 0 0 1 4-5.7"/>',
        'g': '<path d="M4.5 5.5h15v10h-8l-4.5 3.5v-3.5H4.5z"/><path d="M8.5 9.5h7M8.5 12h4"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'


# ---------- CTA links: data-cta = data-ref = placement (Controller reads the whatsapp_/call_/map_/facebook_/tiktok_/waze_/review_ prefix) ----------
def cta(kind, place, href, label, cls=None, ic=None, blank=True):
    c = f' class="{cls}"' if cls else ''
    t = ' target="_blank" rel="noopener"' if blank else ''
    return (f'<a{c} href="{E(href)}"{t} data-cta="{kind}_{place}" data-ref="{kind}_{place}">'
            f'{icon(ic) if ic else ""}<span>{E(label)}</span></a>')


def wa(place, text=None, label=None, cls='btn-wa'):
    return cta('whatsapp', place, wa_url(text or S.PREFILL['default']), label or S.UI['wa_btn'], cls, 'wa')


def call(place, label=None, cls='btn-call'):
    return cta('call', place, F['phone']['tel'], label or S.UI['call_btn'], cls, 'call', blank=False)


def pic(stem, eager=False, cls=None, sizes='(min-width: 900px) 30vw, 80vw', small=True):
    """WebP (small + full) with JPG fallback from the server media folder; alt from media.json in this language."""
    w, h, pos = M[stem][:3]
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager == 'high' else ('' if eager else ' loading="lazy"')
    sw = SMALL.get(stem) if small else None
    srcset = (f'{u(f"media/{stem}-{sw}.webp")} {sw}w, {u(f"media/{stem}.webp")} {w}w' if sw else u(f'media/{stem}.webp'))
    sz = f' sizes="{sizes}"' if sw else ''
    return (f'<picture><source type="image/webp" srcset="{srcset}"{sz}>'
            f'<img{c} src="{u(f"media/{stem}.jpg")}" width="{w}" height="{h}" alt="{E(alt(stem))}" style="object-position:{pos}"{load} decoding="async"></picture>')


def wordmark():
    return f'<span class="wm" aria-hidden="true"><span class="wm-t">LT AUTOMART</span><span class="wm-s"></span></span>'


# ---------- head / header / footer ----------
def head(path, title, meta, ld):
    css = os.path.join(HERE, 'assets', 'site.css')
    zh = L['code'] == 'zh'
    font = f'<link rel="preload" href="{u("assets/fonts/archivo-it.woff2")}" as="font" type="font/woff2" crossorigin>'
    font += (f'<link rel="preload" href="{u("assets/fonts/notosanssc-700.woff2")}" as="font" type="font/woff2" crossorigin>' if zh else
             f'<link rel="preload" href="{u("assets/fonts/schibsted.woff2")}" as="font" type="font/woff2" crossorigin>')
    hero = ''
    if path == '':
        hero = (f'<link rel="preload" as="image" type="image/webp" href="{u("media/shopfront-night-hero-800.webp")}" media="(max-width: 899px)" fetchpriority="high">'
                f'<link rel="preload" as="image" type="image/webp" href="{u("media/shopfront-sign-wide.webp")}" media="(min-width: 900px)" fetchpriority="high">')
    ldj = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="{L['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(meta)}">
{GL.head_tags(CFG, path, L['code'])}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(NAME)}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta)}">
<meta property="og:image:alt" content="{E(M['shopfront-sign-wide'][LIDX[L['code']]])}">
{I18N.og_locale_tags(L)}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(meta)}">
<meta name="twitter:image:alt" content="{E(M['shopfront-sign-wide'][LIDX[L['code']]])}">
<meta name="theme-color" content="#121214">
<link rel="icon" href="{u('media/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="icon" href="{u('media/favicon.png')}" sizes="512x512" type="image/png">
<link rel="apple-touch-icon" href="{u('media/apple-touch-icon.png')}">
{font}{hero}
<link rel="stylesheet" href="{u('assets/site.css')}?v={ver(css)}">
{ldj}
</head>'''


NAV = [('services/', 'services'), ('contact/', 'contact'), ('articles/', 'articles')]


def header(path):
    def cur(p):
        return ' aria-current="page"' if path == p else ''
    nav = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in NAV)
    svc = ''.join(f'<a href="{pu(spath(s))}"{cur(spath(s))}>{E(S.SV[s]["name"])}</a>' for s in PAGE_SERVICES)
    sheet = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in [('', 'home')] + NAV)
    return f'''<body class="lang-{L['code']}">
<a class="skip" href="#main">{E(S.UI['skip'])}</a>
<header class="sign-bar"><div class="wrap sign-in">
<a class="brand" href="{pu('')}" aria-label="{E(NAME)}">{wordmark()}</a>
<nav class="topnav" aria-label="{E(S.UI['menu'])}">{nav}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='tabs')}
{wa('header', label=S.UI['wa_short'], cls='btn-wa sm hdr-wa')}
<button class="burger" type="button" aria-expanded="false" aria-controls="sheet" aria-label="{E(S.UI['menu'])}">{icon('menu')}</button>
</div></header>
<div class="sheet" id="sheet" hidden><div class="sheet-in" role="dialog" aria-modal="true" aria-label="{E(S.UI['menu'])}">
<div class="sheet-top">{wordmark()}<button class="sheet-x" type="button" aria-label="{E(S.UI['close'])}">{icon('x')}</button></div>
<nav class="sheet-nav" aria-label="{E(S.UI['menu'])}">{sheet}</nav>
<nav class="sheet-svc" aria-label="{E(S.UI['services'])}">{svc}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='tabs')}
<div class="sheet-cta">{wa('menu')}{call('menu')}</div>
</div></div>
<main id="main">'''


def footer():
    a = F['address']
    lines = '<br>'.join(E(x) for x in a['lines'])
    svc = ''.join(f'<li><a href="{pu(spath(s))}">{E(S.SV[s]["name"])}</a></li>' for s in PAGE_SERVICES)
    nav = ''.join(f'<li><a href="{pu(p)}">{E(S.UI[k])}</a></li>' for p, k in [('services/', 'all_services')] + NAV[1:])
    return f'''</main>
<footer class="sign-foot"><div class="pin" aria-hidden="true"></div><div class="wrap">
<div class="foot-g">
<div class="foot-id">
<a class="brand" href="{pu('')}" aria-label="{E(NAME)}">{wordmark()}</a>
<p class="foot-tag">{E(S.UI['tagline'])}</p>
<address>{lines}</address>
<p class="foot-h">{icon('clock')}<span>{E(S.UI['hours_short'])}</span></p>
</div>
<div><h2>{E(S.UI['contact_h'])}</h2><ul class="foot-l">
<li>{wa('footer', label='WhatsApp ' + F['phone']['display'], cls='fl')}</li>
<li>{call('footer', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='fl')}</li>
<li>{cta('map', 'footer', LK['maps'], S.UI['maps'], 'fl', 'pin')}</li>
<li>{cta('waze', 'footer', LK['waze'], S.UI['waze'], 'fl', 'nav')}</li>
</ul>
<h2>{E(S.UI['follow_h'])}</h2><ul class="foot-l">
<li>{cta('facebook', 'footer', LK['facebook'], S.UI['facebook'], 'fl', 'fb')}</li>
<li>{cta('tiktok', 'footer', LK['tiktok'], S.UI['tiktok'], 'fl', 'tt')}</li>
</ul></div>
<div><h2>{E(S.UI['services'])}</h2><ul class="foot-n">{svc}</ul><ul class="foot-n">{nav}</ul></div>
</div>
<p class="legal">{E(S.UI['legal'])}</p>
<div class="foot-b"><span>&copy; 2026 {E(NAME)}</span><a href="{pu('privacy/')}">{E(S.UI['privacy'])}</a><a href="https://autoseo.my/">Website by AutoSEO.my</a></div>
</div></footer>
<div class="float-bar">{wa('mobile_bar', label=S.UI['wa_short'])}{call('mobile_bar', label=S.UI['call_short'])}</div>
<script src="{u('assets/site.js')}?v={ver(os.path.join(HERE, 'assets', 'site.js'))}" defer></script>
<script src="{u('p1-cta.js')}?v={ver(os.path.join(HERE, 'p1-cta.js'))}" defer></script>
</body>
</html>
'''


# ---------- schema (GBP NAP; no aggregateRating, no Review) ----------
def org_ld():
    a = F['address']
    h = F['hours']
    return {
        '@context': 'https://schema.org', '@type': ['AutoPartsStore', 'AutoRepair'], '@id': GL.jsonld_id(CFG),
        'name': NAME, 'legalName': F['legal_name'], 'alternateName': F['google_listing_name'],
        'description': S.LLMS['intro'], 'url': canon(''), 'inLanguage': L['hreflang'],
        'telephone': F['phone']['e164'], 'image': CFG.og_image(),
        'address': {'@type': 'PostalAddress', 'streetAddress': a['street'] + ', ' + a['area'], 'addressLocality': a['city'],
                    'postalCode': a['postcode'], 'addressRegion': a['region'], 'addressCountry': a['country']},
        'geo': {'@type': 'GeoCoordinates', 'latitude': F['geo']['lat'], 'longitude': F['geo']['lng']},
        'hasMap': LK['maps'],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': h['days'], 'opens': h['opens'], 'closes': h['closes']}],
        'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': F['phone']['e164'], 'url': F['whatsapp']['url'],
                          'availableLanguage': ['en', 'ms', 'zh']}],
        'sameAs': [LK['facebook'], LK['tiktok']],
        'areaServed': {'@type': 'City', 'name': 'Johor Bahru'},
        'foundingDate': F['since'],
    }


def site_ld():
    return {'@context': 'https://schema.org', '@type': 'WebSite', '@id': GL.jsonld_id(CFG, 'website'), 'name': NAME, 'url': canon(''),
            'inLanguage': L['hreflang'], 'publisher': {'@id': GL.jsonld_id(CFG)}}


def crumb_ld(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': canon(p)} for i, (p, n) in enumerate(trail)]}


def faq_ld(items):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def service_ld(sid, path):
    d = S.SV[sid]
    return {'@context': 'https://schema.org', '@type': 'Service', 'name': d['name'], 'serviceType': d['name'], 'description': d['meta'],
            'url': canon(path), 'provider': {'@id': GL.jsonld_id(CFG)}, 'areaServed': {'@type': 'City', 'name': 'Johor Bahru'}}


def crumb_html(trail):
    li = ''.join(f'<li><a href="{pu(p)}"{" aria-current=\"page\"" if i == len(trail) - 1 else ""}>{E(n)}</a></li>' for i, (p, n) in enumerate(trail))
    return f'<nav class="crumb" aria-label="{E(S.UI["breadcrumb"])}"><ol>{li}</ol></nav>'


# ---------- shared blocks ----------
def led(cls='led'):
    """Thin LED light sweep along a slanted edge (SVG stretches to any width; CSS animates the dash)."""
    return (f'<svg class="{cls}" viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
            '<line x1="0" y1="10" x2="100" y2="0" class="led-base"/><line x1="0" y1="10" x2="100" y2="0" class="led-run"/></svg>')


def hours_line():
    return f'<p class="hrs">{icon("clock")}<span>{E(S.UI["hours_short"])}</span></p>'


def steps():
    st = ''.join(f'<li><span class="n">{i + 1}</span><h3>{E(h)}</h3><p>{E(p)}</p></li>' for i, (h, p) in enumerate(S.UI['process']))
    return f'<section class="band dark slant steps-band"><div class="wrap"><h2 class="h2">{E(S.UI["process_h"])}</h2><ol class="steps">{st}</ol></div></section>'


def qa_list(items):
    return '<div class="qa">' + ''.join(f'<details><summary><span>{E(q)}</span><i aria-hidden="true"></i></summary><p>{E(a)}</p></details>' for q, a in items) + '</div>'


def reel_row(stems, place='reels'):
    tiles = ''.join(
        f'<li><a class="reel" href="{E(REEL_URL[s])}" target="_blank" rel="noopener" data-cta="tiktok_{place}" data-ref="tiktok_{place}" aria-label="{E(alt(s))}, {E(S.UI["watch"])}">'
        f'{pic(s, sizes="(min-width: 900px) 260px, 64vw")}<span class="play">{icon("play")}</span><span class="reel-cap">{E(alt(s))}</span></a></li>' for s in stems)
    return f'<ul class="reel-row">{tiles}</ul>'


def bay_rail(stems):
    cards = ''.join(f'<li class="card45"><figure>{pic(s, sizes="(min-width: 900px) 300px, 72vw")}<figcaption>{E(alt(s))}</figcaption></figure></li>' for s in stems)
    return f'''<div class="bay-rail" role="region" aria-label="{E(S.UI['carousel'])}"><ul class="rail" data-speed="0.035">{cards}</ul>
<div class="rail-c"><button type="button" class="rail-btn" data-dir="-1" aria-label="{E(S.UI['prev'])}">{icon('prev')}</button><button type="button" class="rail-btn" data-dir="1" aria-label="{E(S.UI['next'])}">{icon('next')}</button></div></div>'''


def visit_band(place):
    a = F['address']
    return f'''<section class="band dark slant visit"><div class="wrap visit-g">
<figure class="visit-ph">{pic('shopfront-sign-wide', sizes='(min-width: 900px) 560px, 92vw')}</figure>
<div class="visit-t">
<h2 class="h2">{E(S.HOME['visit_h'])}</h2>
<p>{E(S.HOME['visit_p'])}</p>
<address>{E(a['one_line'])}</address>
{hours_line()}
<div class="btns">{wa(place, S.PREFILL['contact'])}{call(place, cls='btn-call ghost')}</div>
<div class="go">{cta('map', place, LK['maps'], S.UI['maps'], 'chip', 'pin')}{cta('waze', place, LK['waze'], S.UI['waze'], 'chip', 'nav')}</div>
</div></div></section>'''


def page_head(trail, h1, lead, sid=None, photo=None, place='page'):
    text = S.SV[sid]['prefill'] if sid else S.PREFILL['default']
    pl = f'service_{sid}' if sid else place
    ph = ''
    if photo:
        ph = f'<figure class="ph-ph">{pic(photo, eager="high", sizes="(min-width: 900px) 420px, 88vw")}</figure>'
    elif sid == 'bmw':
        ph = f'<div class="ph-ph type-tile" aria-hidden="true"><span>BMW</span><b>{E(BMW_MARK)}</b></div>'
    return f'''<section class="band dark slant page-head{" has-ph" if ph else ""}"><div class="wrap ph-g">
<div class="ph-t">{crumb_html(trail)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>
<div class="btns">{wa(pl, text)}{call(pl, cls='btn-call ghost')}</div>{hours_line()}</div>
{ph}</div>{led()}</section>'''


# ---------- home ----------
def home():
    H = S.HOME
    w, h, _ = M['shopfront-sign-wide'][:3]
    hero = f'''<section class="night-hero">
<picture class="nh-ph"><source media="(min-width: 900px)" type="image/webp" srcset="{u('media/shopfront-sign-wide.webp')}" width="{w}" height="{h}">
<source media="(min-width: 900px)" srcset="{u('media/shopfront-sign-wide.jpg')}" width="{w}" height="{h}">
<source type="image/webp" srcset="{u('media/shopfront-night-hero-800.webp')} 800w, {u('media/shopfront-night-hero.webp')} 1200w" sizes="100vw">
<img src="{u('media/shopfront-night-hero.jpg')}" width="1200" height="1500" alt="{E(alt('shopfront-night-hero'))}" fetchpriority="high" decoding="async"></picture>
<a class="live-chip" href="#reels"><span class="lc-ph">{pic('reel-console-box-poster', eager=True, sizes='72px')}<i>{icon('play')}</i></span><span>{E(S.UI['live_chip'])}</span></a>
<div class="wrap nh-in"><div class="nh-t">
<h1>{E(H['h1'])}</h1>
<p class="nh-line">{E(H['line'])}</p>
<div class="btns nh-cta">{wa('home_hero')}{call('home_hero', label=S.UI['call_btn'], cls='btn-call ghost')}</div>
{hours_line()}
</div>
<a class="nh-reel reel" href="{E(REEL_URL['reel-console-box-poster'])}" target="_blank" rel="noopener" data-cta="tiktok_home_hero" data-ref="tiktok_home_hero" aria-label="{E(alt('reel-console-box-poster'))}, {E(S.UI['watch'])}">{pic('reel-console-box-poster', sizes='300px')}<span class="play">{icon('play')}</span><span class="reel-cap">{E(S.UI['live_chip'])}</span></a>
</div>{led()}</section>'''

    chips = ''.join(f'<button type="button" class="upg-chip" role="tab" id="tab-{s}" aria-controls="pane-{s}" aria-selected="{"true" if i == 0 else "false"}"><span>{E(S.SV[s]["chip"])}</span></button>' for i, s in enumerate(MENU))
    panes = ''.join(f'''<div class="upg-pane" role="tabpanel" id="pane-{s}" aria-labelledby="tab-{s}">
<figure class="upg-ph">{pic(SV[s]['photo'], sizes='(min-width: 900px) 400px, 86vw')}</figure>
<div class="upg-t"><h3>{E(S.SV[s]['name'])}</h3><p>{E(S.SV[s]['line'])}</p>
<div class="btns">{wa('service_' + s, S.SV[s]['prefill'])}<a class="more" href="{pu(spath(s))}">{E(S.UI['see_service'])}{icon('go')}</a></div></div></div>''' for s in MENU)
    allsvc = ''.join(f'<li><a href="{pu(spath(s))}">{E(S.SV[s]["name"])}</a></li>' for s in PAGE_SERVICES)
    menu = f'''<section class="band light upg"><div class="wrap">
<h2 class="h2">{E(H['menu_h'])}</h2><p class="sub">{E(H['menu_p'])}</p>
<div class="upg-chips" role="tablist" aria-label="{E(H['menu_h'])}">{chips}</div>
<div class="upg-panes">{panes}</div>
<nav class="svc-links" aria-label="{E(S.UI['all_services'])}"><h3>{E(S.UI['all_services'])}</h3><ul>{allsvc}</ul></nav>
</div></section>'''

    mpv_li = ''.join(f'<li>{E(x)}</li>' for x in H['mpv_list'])
    mpv = f'''<section class="band light mpv-spot"><div class="wrap mpv-g">
<div class="mpv-ph"><figure class="m1">{pic('alphard-cockpit-upgrade', sizes='(min-width: 900px) 420px, 70vw')}</figure>
<figure class="m2">{pic('marble-flooring-panels', sizes='180px')}</figure><figure class="m3">{pic('gr-steering-wheel', sizes='180px')}</figure></div>
<div class="mpv-t"><h2 class="h2">{E(H['mpv_h'])}</h2><p>{E(H['mpv_p'])}</p><ul class="ticks">{mpv_li}</ul>
<div class="btns">{wa('service_mpv', S.SV['mpv']['prefill'])}<a class="more" href="{pu(spath('mpv'))}">{E(H['mpv_btn'])}{icon('go')}</a></div></div>
</div></section>'''

    reels = f'''<section class="band dark slant reels" id="reels"><div class="wrap">
<h2 class="h2">{E(S.UI['reels_h'])}</h2><p class="sub">{E(S.UI['reels_p'])}</p>
{reel_row([r['stem'] for r in F['reels']])}
<p class="follow">{cta('tiktok', 'reels_follow', LK['tiktok'], S.UI['tiktok'], 'chip', 'tt')}</p>
</div></section>'''

    jobs = f'''<section class="band light jobs"><div class="wrap"><h2 class="h2">{E(H['jobs_h'])}</h2></div>{bay_rail(CAROUSEL)}</section>'''

    why = ''.join(f'<li><h3>{E(h)}</h3><p>{E(p)}</p></li>' for h, p in H['why'])
    brands = ''.join(f'<li>{E(b)}</li>' for b in F['brands'])
    whyb = f'''<section class="band dark slant why"><div class="wrap">
<h2 class="h2">{E(H['why_h'])}</h2><ul class="why-grid">{why}</ul>
<h3 class="brands-h">{E(S.UI['brands_h'])}</h3><ul class="brand-row">{brands}</ul>
<p class="legal-in">{E(S.UI['legal'])}</p>
</div></section>'''

    tr = S.REVIEW_TR
    qs = ''.join(f'''<li><figure class="voice"><blockquote lang="en"><p>{E(r['text'])}</p></blockquote>
{f'<p class="tr"><b>{E(S.UI["translation"])}:</b> {E(tr[i])}</p>' if tr[i] else ''}<figcaption><span>{E(r['author'])}</span><small>Google</small></figcaption></figure></li>''' for i, r in enumerate(F['reviews']))
    voices = f'''<section class="band light voices"><div class="wrap">
<h2 class="h2">{E(H['reviews_h'])}</h2><ul class="voice-row">{qs}</ul>
<p class="more-row">{cta('review', 'home', LK['reviews'], S.UI['reviews_link'], 'more', 'g')}</p>
</div></section>'''

    faq = f'''<section class="band light faq"><div class="wrap narrow"><h2 class="h2">{E(S.UI['faq_h'])}</h2>{qa_list(H['faq'])}
<div class="art-teaser"><h3>{E(H['art_h'])}</h3><p>{E(H['art_p'])}</p><a class="more" href="{pu('articles/')}">{E(H['art_btn'])}{icon('go')}</a></div></div></section>'''
    return hero + menu + steps() + mpv + reels + jobs + whyb + voices + visit_band('home') + faq


# ---------- services hub ----------
def services_page(path):
    P = S.SERVICES_PAGE
    trail = [('', S.UI['home']), (path, S.UI['services'])]
    chips = ''.join(f'<a class="chip" href="#{s}">{E(S.SV[s]["chip"])}</a>' for s in [x[0] for x in SERVICES])
    secs = ''
    for i, (sid, slug, photo, gal, _) in enumerate(SERVICES):
        d = S.SV[sid]
        if photo:
            ph = f'<figure class="svc-ph">{pic(photo, sizes="(min-width: 900px) 380px, 86vw")}</figure>'
        elif sid == 'bmw':
            ph = f'<div class="svc-ph type-tile" aria-hidden="true"><span>BMW</span><b>{E(BMW_MARK)}</b></div>'
        else:
            ph = ''
        name = d['name'] if sid != 'service' else P['more_h']
        pts = ''.join(f'<li>{E(x)}</li>' for x in d['points'][:3])
        link = f'<a class="more" href="{pu(spath(sid))}">{E(S.UI["see_service"])}{icon("go")}</a>' if slug else ''
        secs += f'''<article class="svc{' flip' if i % 2 else ''}{' no-ph' if not ph else ''}" id="{sid}">{ph}<div class="svc-t">
<h2>{E(name)}</h2><p>{E(d['line'])}</p>{f'<ul class="ticks">{pts}</ul>' if pts else ''}
<div class="btns">{wa('service_' + sid, d['prefill'])}{link}</div></div></article>'''
    body = (page_head(trail, P['h1'], P['lead'], place='services') +
            f'<section class="band light svc-hub"><div class="wrap"><nav class="jump" aria-label="{E(S.UI["services"])}">{chips}</nav>{secs}</div></section>' +
            steps() + f'<section class="band light faq"><div class="wrap narrow"><h2 class="h2">{E(S.UI["faq_h"])}</h2>{qa_list([S.UI["faq_price"], S.UI["faq_appt"]])}</div></section>' +
            visit_band('services'))
    return body, [org_ld(), crumb_ld(trail), faq_ld([S.UI['faq_price'], S.UI['faq_appt']])]


# ---------- one service page (generated from the list) ----------
def service_page(sid):
    path = spath(sid)
    d = S.SV[sid]
    v = SV[sid]
    trail = [('', S.UI['home']), ('services/', S.UI['services']), (path, d['name'])]
    pts = ''.join(f'<li>{E(x)}</li>' for x in d['points'])
    gal = ''.join(f'<li class="card45"><figure>{pic(s, sizes="(min-width: 900px) 300px, 64vw")}<figcaption>{E(alt(s))}</figcaption></figure></li>' for s in v['gallery'])
    reels = ''
    if v['reels']:
        reels = f'''<section class="band dark slant reels"><div class="wrap"><h2 class="h2">{E(S.UI['reels_h'])}</h2><p class="sub">{E(S.UI['reels_p'])}</p>{reel_row(v['reels'], 'reels_' + sid)}</div></section>'''
    faqs = d['faqs'] + [S.UI['faq_price'], S.UI['faq_appt']]
    others = ''.join(f'<li><a class="chip" href="{pu(spath(s))}">{E(S.SV[s]["name"])}</a></li>' for s in PAGE_SERVICES if s != sid)
    brands = ''
    if sid == 'audio':
        brands = f'<h3 class="brands-h">{E(S.UI["brands_h"])}</h3><ul class="brand-row on-light">' + ''.join(f'<li>{E(b)}</li>' for b in F['brands']) + '</ul>'
    body = (page_head(trail, d['h1'], d['lead'], sid=sid, photo=v['photo']) +
            f'''<section class="band light fit"><div class="wrap fit-g"><div><h2 class="h2">{E(d['name'])}</h2><ul class="ticks big">{pts}</ul>{brands}
<div class="btns">{wa('service_' + sid + '_list', d['prefill'])}</div></div>
<ul class="gal">{gal}</ul></div></section>''' +
            reels + steps() +
            f'<section class="band light faq"><div class="wrap narrow"><h2 class="h2">{E(S.UI["faq_h"])}</h2>{qa_list(faqs)}'
            f'<nav class="others" aria-label="{E(S.UI["other_services"])}"><h3>{E(S.UI["other_services"])}</h3><ul>{others}</ul></nav></div></section>' +
            visit_band('service_' + sid))
    return body, [org_ld(), service_ld(sid, path), crumb_ld(trail), faq_ld(faqs)]


# ---------- contact ----------
def contact_page(path):
    C = S.CONTACT
    a = F['address']
    trail = [('', S.UI['home']), (path, S.UI['contact'])]
    body = page_head(trail, C['h1'], C['lead'], photo='shopfront-night-hero', place='contact') + f'''<section class="band light contact"><div class="wrap ct-g">
<div class="ct-card">
<h2>{E(S.UI['address_h'])}</h2><address>{'<br>'.join(E(x) for x in a['lines'])}<br>Malaysia</address>
<h2>{E(S.UI['hours_h'])}</h2><p class="hrs-big"><span>{E(S.UI['daily'])}</span><b>10:00 – 20:30</b></p>
<h2>{E(S.UI['contact_h'])}</h2>
<div class="ct-btns">{wa('contact', S.PREFILL['contact'])}{call('contact', cls='btn-call ghost dark-ink')}</div>
<div class="go">{cta('map', 'contact', LK['maps'], S.UI['maps'], 'chip', 'pin')}{cta('waze', 'contact', LK['waze'], S.UI['waze'], 'chip', 'nav')}
{cta('facebook', 'contact', LK['facebook'], S.UI['facebook'], 'chip', 'fb')}{cta('tiktok', 'contact', LK['tiktok'], S.UI['tiktok'], 'chip', 'tt')}
{cta('review', 'contact', LK['reviews'], S.UI['reviews_link'], 'chip', 'g')}</div>
</div>
<div class="map"><iframe src="{E(LK['maps_embed'])}" title="{E(S.UI['map_title'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
</div></section>
<section class="band dark slant about"><div class="wrap about-g"><figure>{pic('shopfront-sign-wide', sizes='(min-width: 900px) 560px, 92vw')}</figure>
<div><h2 class="h2">{E(C['about_h'])}</h2><p>{E(C['about_p'])}</p><p class="quote-own">"{E(F['own_line'])}"</p><p class="legal-in">{E(S.UI['legal'])}</p></div></div></section>'''
    return body, [org_ld(), crumb_ld(trail)]


def articles_page(path):
    A = S.ARTICLES
    trail = [('', S.UI['home']), (path, S.UI['articles'])]
    body = page_head(trail, A['h1'], A['empty'], place='articles') + '<section class="band light"><div class="wrap"><ul class="art-list"></ul></div></section>'
    return body, [org_ld(), crumb_ld(trail)]


def privacy_page(path):
    P = S.PRIVACY
    trail = [('', S.UI['home']), (path, S.UI['privacy'])]
    rows = ''.join(f'<h2>{E(h)}</h2><p>{E(t)}</p>' for h, t in P['body'])
    body = page_head(trail, P['h1'], P['meta'], place='privacy') + f'<section class="band light"><div class="wrap prose narrow">{rows}<p class="legal-in">{E(S.UI["legal"])}</p></div></section>'
    return body, [org_ld(), crumb_ld(trail)]


def render(path):
    if path == '':
        H = S.HOME
        return head(path, H['title'], H['meta'], [org_ld(), site_ld(), faq_ld(H['faq'])]) + header(path) + home() + footer()
    if path == 'services/':
        b, ld = services_page(path)
        D = S.SERVICES_PAGE
    elif path.startswith('services/'):
        sid = next(s for s in PAGE_SERVICES if spath(s) == path)
        b, ld = service_page(sid)
        D = S.SV[sid]
    else:
        fn, D = {'contact/': (contact_page, S.CONTACT), 'articles/': (articles_page, S.ARTICLES), 'privacy/': (privacy_page, S.PRIVACY)}[path]
        b, ld = fn(path)
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
        elif isinstance(a, (list, tuple)) and at.split('.')[-1] not in ('REVIEW_TR',):
            if len(a) != len(b):
                raise SystemExit(f'strings length mismatch at {at}')
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, f'{at}[{i}]')
    for code in ('ms', 'zh'):
        for n in [n for n in dir(strings_en) if n.isupper()]:
            if not hasattr(STRINGS[code], n):
                raise SystemExit(f'{code} missing {n}')
            walk(getattr(strings_en, n), getattr(STRINGS[code], n), f'{code}.{n}')
    for s in [x[0] for x in SERVICES]:
        for code in STRINGS:
            if s not in STRINGS[code].SV:
                raise SystemExit(f'{code} SV missing {s}')


def cjk_text():
    t = set()
    for mod in STRINGS.values():
        for n in dir(mod):
            if n.isupper():
                t |= set(str(getattr(mod, n)))
    for v in M.values():
        t |= set(v[5])
    t |= set('中文')
    return ''.join(sorted(c for c in t if ord(c) > 0x2E80))


def fonts():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    chars = cjk_text()
    open(os.path.join(HERE, 'assets', 'fonts', 'zh-chars.txt'), 'w', encoding='utf8').write(chars)
    for wt in (400, 700):
        q = urllib.parse.urlencode({'family': f'Noto Sans SC:wght@{wt}', 'text': chars, 'display': 'swap'})
        css = urllib.request.urlopen(urllib.request.Request('https://fonts.googleapis.com/css2?' + q, headers={'User-Agent': ua})).read().decode()
        url = re.search(r'url\((https://[^)]+)\)', css).group(1)
        open(os.path.join(HERE, 'assets', 'fonts', f'notosanssc-{wt}.woff2'), 'wb').write(urllib.request.urlopen(url).read())


def main():
    global S, L
    check_keys()
    if '--fonts' in sys.argv:
        fonts()
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
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf8').write(GL.sitemap_xml(CFG, PAGES, TODAY))
    open(os.path.join(OUT, 'robots.txt'), 'w', encoding='utf8').write(GL.robots_txt(CFG))
    L, S = I18N.LANGS[0], strings_en
    a = F['address']
    lines = [GL.llms_header(CFG, NAME, S.LLMS['intro']).rstrip(), '',
             f'- Address: {a["one_line"]}', f'- WhatsApp and phone: {F["phone"]["display_intl"]} ({F["whatsapp"]["url"]})',
             '- Hours: open daily, 10:00 to 20:30', f'- Google Maps: {LK["maps"]}', f'- Waze: {LK["waze"]}',
             f'- Facebook: {LK["facebook"]}', f'- TikTok: {LK["tiktok"]}', f'- Company: {F["legal_name"]} ({F["company_no"]})', '',
             '## Services']
    lines += [f'- [{S.SV[s]["name"]}]({CFG.canon(spath(s))}): {S.SV[s]["line"]}' for s in PAGE_SERVICES]
    lines += [f'- {S.SV["service"]["name"]}: {S.SV["service"]["line"]}', '', f'Brands we fit: {", ".join(F["brands"])}', '', '## Pages']
    for LL in I18N.LANGS:
        for p in PAGES:
            lines.append(f'- [{LL["label"]}] {CFG.canon(I18N.page_path(LL, p))}')
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf8').write('\n'.join(lines) + '\n')
    print(f'built {len(built)} pages for {CFG.canonical_base} (live={CFG.live})')


if __name__ == '__main__':
    main()
