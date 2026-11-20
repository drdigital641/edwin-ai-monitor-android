#!/usr/bin/env python3
"""Overseas Tyre site builder (AutoSEO.my client preview, 20 Nov 2026).
One template set for every page: head, header, menu sheet, footer, mobile bar, CTA links, photo blocks and schema live here
once, so one edit updates every page in every language. Facts: facts.json. Copy: strings_en/ms/zh.py (same keys).
Language plumbing (switcher, hreflang, og:locale, sitemap) comes from the shared template autoseo-template/autoseo_i18n.py.
Blocks follow autoseo-template/blocks (photo hero, soft cards, colour bands), restyled for this site.

  python3 build.py                 -> preview build, canonical/hreflang/OG/schema/sitemap on https://autoseo.my/preview/overseas-tyre/
  python3 build.py --live DOMAIN   -> same files with https://DOMAIN/ as the absolute base (unified go-live: the domain points
                                      at this same folder). Internal links are page-relative, so they work on both hosts.
No per-page robots meta: the preview host is noindexed by autoseo.my/preview/.htaccess (X-Robots-Tag), so nothing needs
stripping at go-live. Then python3 check.py before any Bridge upload (sync_from_github, site autoseo, base_path preview/overseas-tyre).
Photos are not in the repo: they live on the server in preview/overseas-tyre/images/ (Bridge drop 6affca5baa2556abf3139687)."""
import hashlib, html, json, os, re, shutil, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'autoseo-template'))
import autoseo_i18n as I18N
import strings_en, strings_ms, strings_zh
STRINGS = {'en': strings_en, 'ms': strings_ms, 'zh': strings_zh}
S, L = strings_en, I18N.LANGS[0]
CUR = ''   # site path of the page being rendered (with language prefix), for page-relative links

F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
if '--live' in sys.argv:
    SITE = 'https://' + sys.argv[sys.argv.index('--live') + 1].strip('/') + '/'
else:
    SITE = F['preview']['origin'] + F['preview']['base']
OUT = os.path.join(HERE, '..', 'dist')
E = html.escape
LK, WA, PH = F['links'], F['whatsapp'], F['photos']
TODAY = '2026-11-20'

SVC_PATH = {'tyres': 'services/tyres/', 'alignment': 'services/wheel-alignment/', 'servicing': 'services/car-servicing/',
            'brakes': 'services/brakes-suspension/', 'battery': 'services/battery-aircond/', 'diagnostics': 'services/diagnostics/'}
PAGES = ['', 'services/'] + [SVC_PATH[k] for k in strings_en.SVC_ORDER] + ['about/', 'contact/', 'articles/', 'privacy/']
NAV = [('services/', 'services'), ('about/', 'about'), ('contact/', 'contact'), ('articles/', 'articles')]
SVC_PHOTO = {'tyres': 'michelin-primacy-job', 'alignment': 'bay-alignment', 'servicing': 'harrier-tyres', 'brakes': 'brakes-suspension',
             'battery': 'vellfire-bay', 'diagnostics': 'bmw-x5-wheel-off'}
SVC_STRIP = {'tyres': ['michelin-ps5-job', 'michelin-ps5-fitted', 'hunter-fitting', 'hrv-tyres', 'sport-rim'],
             'alignment': ['mercedes-wheel', 'hunter-fitting', 'sport-rim'],
             'servicing': ['bay-alignment', 'vellfire-bay', 'hrv-tyres'],
             'brakes': ['bmw-x5-wheel-off', 'harrier-tyres', 'bay-alignment'],
             'battery': ['bay-alignment', 'harrier-tyres'],
             'diagnostics': ['brakes-suspension', 'bay-alignment']}
# home service bands: (strings BANDS key, photo, service page it links to, band colour)
BANDS = [('tyres', 'michelin-primacy-job', 'tyres', 'paper'), ('fitting', 'hunter-fitting', 'tyres', 'royal'),
         ('alignment', 'bay-alignment', 'alignment', 'concrete'), ('servicing', 'harrier-tyres', 'servicing', 'paper'),
         ('brakes', 'brakes-suspension', 'brakes', 'royal')]


# ---------- paths ----------
def rel(target=''):
    """Page-relative href from the page being rendered to site path `target` (no leading slash)."""
    depth = len([x for x in CUR.split('/') if x])
    r = '../' * depth + target
    return r or './'


def pu(p=''):
    return rel(I18N.page_path(L, p))


def absu(p=''):
    return SITE + p


def pabs(p=''):
    return absu(I18N.page_path(L, p))


def ver(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]


def icon(name):
    p = {
        'wa': '<path d="M12 3.2a8.7 8.7 0 0 0-7.5 13.1L3.3 20.8l4.6-1.2A8.7 8.7 0 1 0 12 3.2z" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M9.1 7.9c.2-.4.4-.4.7-.4h.5c.2 0 .4 0 .6.5l.8 1.9c.1.2.1.4 0 .6l-.5.7c-.1.2-.2.3 0 .6.5.9 1.2 1.6 2.1 2.1.3.1.4.1.6-.1l.7-.8c.2-.2.3-.2.6-.1l1.8.9c.3.1.4.2.4.4 0 .4-.1 1.1-.6 1.5-.5.5-1.3.7-2 .6-1.1-.2-2.6-.8-3.9-2-1.5-1.4-2.3-2.9-2.5-3.9-.1-.9.3-1.7.7-2z" fill="currentColor"/>',
        'call': '<path d="M5.2 4h3.6l1.6 4-2.1 1.3a10.6 10.6 0 0 0 6.4 6.4l1.3-2.1 4 1.6v3.6a1.6 1.6 0 0 1-1.7 1.6C10.4 19.9 4.1 13.6 3.6 5.7A1.6 1.6 0 0 1 5.2 4z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
        'pin': '<path d="M12 21s-6.4-5.5-6.4-10.9a6.4 6.4 0 0 1 12.8 0C18.4 15.5 12 21 12 21z" fill="none" stroke="currentColor" stroke-width="1.7"/><circle cx="12" cy="10.1" r="2.2" fill="none" stroke="currentColor" stroke-width="1.7"/>',
        'nav': '<path d="M4 11.4L20 4l-7.4 16-1.7-6.9z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
        'mail': '<rect x="3.5" y="6" width="17" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.7"/>',
        'fb': '<path d="M14 8h2.5V4.5H14A3.5 3.5 0 0 0 10.5 8v2.2H8v3.4h2.5V20h3.4v-6.4h2.4l.5-3.4h-2.9V8.6c0-.4.2-.6.6-.6z" fill="currentColor"/>',
        'menu': '<path d="M4 7h16M4 12h16M4 17h11" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        'x': '<path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        'prev': '<path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        'next': '<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        'go': '<path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        'star': '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8-4.3-4.1 5.9-.8z" fill="currentColor"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'


# ---------- CTA links (data-cta = data-ref = placement; the Controller reads the whatsapp_/call_/... prefix) ----------
def wa_url(key='default'):
    return f"{WA['url']}?text={urllib.parse.quote(S.PREFILL[key])}"


def wa(place, key='default', label=None, cls='b-wa'):
    return (f'<a class="{cls}" href="{E(wa_url(key))}" target="_blank" rel="noopener" data-cta="whatsapp_{place}" data-ref="whatsapp_{place}">'
            f'{icon("wa")}<span>{E(label or S.UI["wa_btn"])}</span></a>')


def call(place, label=None, cls='b-call', who='main'):
    """who: main = office mobile 018 (same number as WhatsApp), manager = In-Charge Manager, landline = GBP workshop line."""
    tel = {'main': WA['tel'], 'manager': F['manager']['tel'], 'landline': F['landline']['tel']}[who]
    kind = {'main': 'call', 'manager': 'call_manager', 'landline': 'call_landline'}[who]
    return (f'<a class="{cls}" href="{tel}" data-cta="{kind}_{place}" data-ref="{kind}_{place}">'
            f'{icon("call")}<span>{E(label or S.UI["call_btn"])}</span></a>')


def ext(kind, place, href, label, cls=None, ic=None):
    c = f' class="{cls}"' if cls else ''
    i = icon(ic) if ic else ''
    return f'<a{c} href="{E(href)}" target="_blank" rel="noopener" data-cta="{kind}_{place}" data-ref="{kind}_{place}">{i}<span>{E(label)}</span></a>'


def mail(place, cls=None):
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="mailto:{F["email"]}" data-cta="email_{place}" data-ref="email_{place}">{icon("mail")}<span>{E(F["email"])}</span></a>'


# ---------- media ----------
def pic(stem, alt=None, cls=None, eager=False, pos=True):
    m = PH[stem]
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager == 'high' else ('' if eager else ' loading="lazy"')
    st = f' style="object-position:{m["pos"]}"' if pos and 'pos' in m else ''
    a = S.CAPS.get(stem, '') if alt is None else alt
    return (f'<picture{c}><source type="image/webp" srcset="{rel("images/" + stem + ".webp")}">'
            f'<img src="{rel("images/" + stem + ".jpg")}" width="{m["w"]}" height="{m["h"]}" alt="{E(a)}"{load} decoding="async"{st}></picture>')


# ---------- shared page parts ----------
def head(path, title, meta, ld):
    css = os.path.join(HERE, 'assets', 'site.css')
    zh = L['code'] == 'zh'
    zh_font = f'<link rel="preload" href="{rel("assets/fonts/notosanssc-sub.woff2")}" as="font" type="font/woff2" crossorigin>' if zh else ''
    ldj = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="{L['hreflang']}"{' class="zh"' if zh else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(meta)}">
<link rel="canonical" href="{pabs(path)}">
{I18N.hreflang_links(absu, path)}
<meta name="theme-color" content="#1E3F7A">
<link rel="icon" href="{rel('assets/favicon.svg')}" type="image/svg+xml">
<link rel="apple-touch-icon" href="{rel('assets/touch-icon.png')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(F['short'])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta)}">
<meta property="og:url" content="{pabs(path)}">
<meta property="og:image" content="{absu('images/og.jpg')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(S.CAPS['cover'])}">
{I18N.og_locale_tags(L)}
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{rel('assets/fonts/plusjakarta-var.woff2')}" as="font" type="font/woff2" crossorigin>
{zh_font}
<link rel="stylesheet" href="{rel('assets/site.css')}?v={ver(css)}">
{ldj}
</head>'''


def wordmark():
    return '<span class="wm-a">Overseas</span> <span class="wm-b">Tyre</span>'


def header(path, over_photo):
    nav = ''.join(f'<a href="{pu(p)}"{" aria-current=\"page\"" if path == p or (p == "services/" and path.startswith(p)) else ""}>{E(S.UI[k])}</a>' for p, k in NAV)
    sheet = ''.join(f'<a href="{pu(p)}">{E(S.UI[k])}</a>' for p, k in [('', 'home')] + NAV + [('privacy/', 'privacy')])
    return f'''<body class="{'over' if over_photo else 'plain'}">
<a class="skip" href="#main">{E(S.UI['skip'])}</a>
<header class="top"><div class="wrap top-in">
<a class="wm" href="{pu('')}" aria-label="{E(F['short'])}">{wordmark()}</a>
<nav class="nav" aria-label="{E(S.UI['menu'])}">{nav}</nav>
{I18N.switcher(rel, path, L, S.UI['lang'], cls='lang')}
{wa('header', cls='b-wa b-sm hd-wa')}
<button class="mb" type="button" aria-expanded="false" aria-controls="sheet" aria-label="{E(S.UI['menu'])}">{icon('menu')}</button>
</div></header>
<div class="sheet" id="sheet" hidden><div class="sheet-in" role="dialog" aria-modal="true" aria-label="{E(S.UI['menu'])}">
<button class="sheet-x" type="button" aria-label="{E(S.UI['close'])}">{icon('x')}</button>
<nav aria-label="{E(S.UI['menu'])}">{sheet}</nav>
{I18N.switcher(rel, path, L, S.UI['lang'], cls='lang')}
<div class="btns">{wa('menu')}{call('menu')}</div>
</div></div>
<main id="main">'''


def hours_table(cls='hrs'):
    return (f'<table class="{cls}"><tbody><tr><th>{E(S.UI["open_days"])}</th><td class="num">{E(S.UI["hours_time"])}</td></tr>'
            f'<tr class="off"><th>{E(S.UI["wed"])}</th><td>{E(S.UI["closed"])}</td></tr></tbody></table>')


def footer():
    a = F['address']
    return f'''</main>
<footer class="ft"><div class="wrap">
<div class="ft-g">
<div class="ft-id">
<a class="wm" href="{pu('')}" aria-label="{E(F['short'])}">{wordmark()}</a>
<p class="ft-sign">{E(F['signboard_malay'])}</p>
<address>{E(S.UI['legal'])}<br>{'<br>'.join(E(x) for x in a['lines'])}</address>
<p class="ft-hrs">{E(S.UI['hours_line'])}</p>
</div>
<div><h2>{E(S.UI['contact_h'])}</h2><ul>
<li>{wa('footer', label=S.UI['wa_label'] + ' ' + WA['display'], cls='fl')}</li>
<li>{call('footer', label=S.UI['call_short'] + ' ' + WA['display'], cls='fl')}</li>
<li>{call('footer', label=S.UI['manager'] + ' ' + F['manager']['display'], cls='fl', who='manager')}</li>
<li>{call('footer', label=S.UI['landline'] + ' ' + F['landline']['display'], cls='fl', who='landline')}</li>
<li>{mail('footer', cls='fl')}</li>
<li>{ext('facebook', 'footer', LK['facebook'], S.UI['facebook'], cls='fl', ic='fb')}</li>
</ul></div>
<div><h2>{E(S.UI['find_h'])}</h2><ul>
<li>{ext('map', 'footer', LK['maps'], S.UI['maps'], cls='fl', ic='pin')}</li>
<li>{ext('waze', 'footer', LK['waze'], S.UI['waze'], cls='fl', ic='nav')}</li>
<li>{ext('michelin', 'footer', LK['michelin'], S.UI['michelin_link'], cls='fl')}</li>
<li>{ext('reviews', 'footer', LK['maps'], S.UI['reviews_link'], cls='fl')}</li>
</ul></div>
</div>
<div class="ft-b"><span>&copy; 2026 {E(S.UI['legal'])}</span><a href="{pu('privacy/')}">{E(S.UI['privacy'])}</a><a href="https://autoseo.my/">Website by AutoSEO.my</a></div>
</div></footer>
<div class="mbar">{wa('mobile_bar')}{call('mobile_bar', label=S.UI['call_short'])}</div>
<script src="{rel('assets/site.js')}?v={ver(os.path.join(HERE, 'assets', 'site.js'))}" defer></script>
<script src="{rel('p1-cta.js')}?v={ver(os.path.join(HERE, 'p1-cta.js'))}" defer></script>
</body>
</html>
'''


# ---------- schema (one facts file) ----------
def org_ld():
    a = F['address']
    return {
        '@context': 'https://schema.org', '@type': ['TireShop', 'AutoRepair'], '@id': SITE + '#business',
        'name': F['legal_name'], 'alternateName': [F['short'], F['signboard_malay']],
        'description': S.SCHEMA['description'], 'url': pabs(''), 'image': absu('images/og.jpg'),
        'telephone': F['landline']['e164'], 'email': F['email'],
        'address': {'@type': 'PostalAddress', 'streetAddress': a['street'], 'addressLocality': a['city'], 'addressRegion': a['region'],
                    'postalCode': a['postcode'], 'addressCountry': a['country']},
        'geo': {'@type': 'GeoCoordinates', 'latitude': F['geo']['lat'], 'longitude': F['geo']['lng']},
        'hasMap': LK['maps'],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': h['days'], 'opens': h['opens'], 'closes': h['closes']} for h in F['hours']],
        'contactPoint': [
            {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': WA['e164'], 'url': WA['url'], 'availableLanguage': ['en', 'ms', 'zh']},
            {'@type': 'ContactPoint', 'contactType': 'In-Charge Manager', 'telephone': F['manager']['e164']},
        ],
        'brand': {'@type': 'Brand', 'name': 'Michelin'},
        'sameAs': [LK['maps_cid'], LK['facebook']],
        'areaServed': [{'@type': 'Place', 'name': 'Taman Bukit Indah'}, {'@type': 'City', 'name': 'Johor Bahru'}],
        'knowsAbout': S.SCHEMA['knows'],
        'inLanguage': L['hreflang'],
    }


def crumb_ld(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': pabs(p)} for i, (p, n) in enumerate(trail)]}


def faq_ld(qs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qs]}


def service_ld(k, path):
    V = S.SERVICES[k]
    return {'@context': 'https://schema.org', '@type': 'Service', 'name': V['name'], 'serviceType': V['name'], 'description': V['meta'],
            'url': pabs(path), 'provider': {'@id': SITE + '#business'}, 'areaServed': {'@type': 'City', 'name': 'Johor Bahru'}}


def crumb_html(trail):
    li = ''.join(f'<li><a href="{pu(p)}"{" aria-current=\"page\"" if i == len(trail) - 1 else ""}>{E(n)}</a></li>' for i, (p, n) in enumerate(trail))
    return f'<nav class="crumb" aria-label="{E(S.UI["breadcrumb"])}"><ol>{li}</ol></nav>'


# ---------- blocks ----------
def hero():
    """Photo hero (autoseo-template/blocks photo_hero, restyled): full-bleed 4:3 shopfront under the transparent header,
    fascia kept in frame (object-position from facts), white H1 + WhatsApp on the photo's fade into deep blue."""
    H = S.HOME
    R = F['reviews']
    return f'''<section class="hero">
<div class="hero-ph">{pic('cover', eager='high')}</div>
<div class="wrap hero-in">
<h1>{E(H['h1'])}</h1>
<p class="hero-line">{E(H['line'])}</p>
<div class="hero-cta">{wa('home_hero', label=S.UI['wa_hero'])}{call('home_hero', label=S.UI['call_short'], cls='b-ghost')}</div>
{ext('reviews', 'home_hero', LK['maps'], f"{R['rating']} {S.UI['rating_of']} {R['count']} {S.UI['rating_reviews']}", cls='hero-rate', ic='star')}
</div></section>'''


def promise():
    H = S.HOME
    pts = ''.join(f'<li><h3>{E(a)}</h3><p>{E(b)}</p></li>' for a, b in H['promise_pts'])
    return f'''<section class="sec paper promise"><div class="wrap">
<div class="pr-t"><h2>{E(H['promise_h'])}</h2><p>{E(H['promise'])}</p></div>
<ul class="pr-pts">{pts}</ul>
</div></section>'''


def band(key, photo, svc, colour, i):
    h, p = S.BANDS[key]
    flip = ' flip' if i % 2 else ''
    return f'''<section class="band {colour}{flip}"><div class="wrap band-in">
<figure class="band-ph">{pic(photo)}<figcaption>{E(S.CAPS[photo])}</figcaption></figure>
<div class="band-t"><h2>{E(h)}</h2><p>{E(p)}</p>
<div class="btns">{wa('home_band_' + key, svc, cls='b-wa b-sm')}<a class="b-more" href="{pu(SVC_PATH[svc])}">{E(S.UI['see_service'])}</a></div></div>
</div></section>'''


def process(cls='concrete'):
    P = S.PROCESS
    steps = ''.join(f'<li><h3>{E(a)}</h3><p>{E(b)}</p></li>' for a, b in P['steps'])
    # tyre ring: tread notches + 4 step positions round the wheel
    notches = ''.join(f'<rect x="99" y="8" width="2" height="12" rx="1" transform="rotate({d} 100 100)"/>' for d in range(0, 360, 15))
    nums = ''.join(f'<g class="wn wn{i + 1}"><circle cx="{x}" cy="{y}" r="15"/><text x="{x}" y="{y + 5.5}">{i + 1}</text></g>'
                   for i, (x, y) in enumerate([(100, 26), (174, 100), (100, 174), (26, 100)]))
    wheel = (f'<svg class="wheel" viewBox="0 0 200 200" aria-hidden="true" focusable="false"><g class="tread">{notches}</g>'
             f'<circle class="tyre" cx="100" cy="100" r="74"/><circle class="rim" cx="100" cy="100" r="46"/>'
             f'<g class="spokes"><path d="M100 58v84M58 100h84M70 70l60 60M130 70l-60 60"/></g><circle class="hub" cx="100" cy="100" r="11"/>{nums}</svg>')
    return f'''<section class="sec {cls} proc"><div class="wrap proc-in">
<div class="proc-w">{wheel}</div>
<div><h2>{E(P['h2'])}</h2><p class="lead">{E(P['lead'])}</p><ol class="steps">{steps}</ol></div>
</div></section>'''


def rating(place):
    R, P = F['reviews'], S.PROOF
    stars = ''.join(icon('star') for _ in range(5))
    return f'''<section class="sec royal rate"><div class="wrap rate-in">
<div class="rate-n"><b class="num">{R['rating']}</b><span class="stars" aria-hidden="true">{stars}</span></div>
<div><h2>{E(P['h2'])}</h2><p>{E(R['rating'])} {E(S.UI['rating_of'])} {R['count']} {E(S.UI['rating_reviews'])}{E(S.UI['sep'])}{E(P['lead'])}</p>
{ext('reviews', place, LK['maps'], S.UI['reviews_link'], cls='b-line')}</div>
</div></section>'''


def rail(stems, h2=None, lead=None, cls='paper'):
    """4:5 work carousel. Behaviour copies Wrapstar ws.js glide (site.js): native drag, rAF autoplay with cloned children,
    hold or sideways drag pauses, resumes 1.5 s after release, reduced motion = no autoplay."""
    figs = ''.join(f'<figure class="card">{pic(s)}<figcaption>{E(S.CAPS[s])}</figcaption></figure>' for s in stems)
    hd = f'<div class="sec-h"><h2>{E(h2)}</h2>{f"<p>{E(lead)}</p>" if lead else ""}</div>' if h2 else ''
    return f'''<section class="sec {cls} work"><div class="wrap">{hd}
<div class="glide" tabindex="0" aria-label="{E(h2 or S.PROOF['rail_h'])}">{figs}</div>
<div class="rail-c"><button type="button" class="arr" data-dir="-1" aria-label="{E(S.UI['prev'])}">{icon('prev')}</button><button type="button" class="arr" data-dir="1" aria-label="{E(S.UI['next'])}">{icon('next')}</button></div>
</div></section>'''


def michelin_proof():
    H = S.HOME
    return f'''<section class="sec concrete mich"><div class="wrap mich-in">
<div class="mich-t"><h2>{E(H['michelin_h'])}</h2><p>{E(H['michelin_p'])}</p>
<div class="btns">{wa('home_michelin', 'tyres')}{ext('michelin', 'home_michelin', LK['michelin'], S.UI['michelin_link'], cls='b-more')}</div></div>
<div class="mich-ph"><figure>{pic('michelin-ps5-close')}<figcaption>{E(S.CAPS['michelin-ps5-close'])}</figcaption></figure>
<figure>{pic('michelin-primacy-close')}<figcaption>{E(S.CAPS['michelin-primacy-close'])}</figcaption></figure></div>
</div></section>'''


def identity(h, paras, link=True, cls='paper'):
    body = ''.join(f'<p>{E(p)}</p>' for p in paras)
    more = f'<a class="b-more" href="{pu("about/")}">{E(S.UI["see_about"])}</a>' if link else ''
    return f'''<section class="sec {cls} ident"><div class="wrap ident-in">
<figure class="sign">{pic('signboard', pos=False)}</figure>
<div><p class="sign-line" lang="ms">{E(F['signboard_malay'])}</p><h2>{E(h)}</h2>{body}{more}</div>
</div></section>'''


def visit(place, cls='paper'):
    a = F['address']
    return f'''<section class="sec {cls} visit"><div class="wrap visit-in">
<div class="card-s"><h2>{E(S.UI['hours_h'])}</h2>{hours_table()}<p class="note">{E(S.UI['wed_closed'])}</p></div>
<div class="card-s"><h2>{E(S.UI['address_h'])}</h2><address>{'<br>'.join(E(x) for x in a['lines'])}</address>
<div class="btns">{ext('map', place, LK['maps'], S.UI['maps'], cls='b-line', ic='pin')}{ext('waze', place, LK['waze'], S.UI['waze'], cls='b-line', ic='nav')}</div></div>
</div></section>'''


def faq(qs, cls='paper'):
    items = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in qs)
    return f'<section class="sec {cls}"><div class="wrap narrow"><h2>{E(S.UI["faq_h"])}</h2><div class="faq">{items}</div></div></section>'


def ask(place, key='default'):
    H = S.HOME
    return f'''<section class="ask"><div class="wrap ask-in">
<h2>{E(H['final_h'])}</h2><p>{E(H['final_line'])}</p>
<div class="btns">{wa(place + '_band', key)}{call(place + '_band', cls='b-ghost')}</div></div></section>'''


def page_head(path, trail, h1, lead, key, photo):
    ph = f'<figure class="ph-ph">{pic(photo)}</figure>' if photo else ''
    return f'''<section class="ph"><div class="wrap ph-in">
<div class="ph-t">{crumb_html(trail)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>
<div class="btns">{wa(slug(path) + '_head', key)}{call(slug(path) + '_head', cls='b-ghost-d')}</div></div>{ph}
</div></section>'''


def slug(path):
    p = path.strip('/').split('/')[-1] if path else 'home'
    return {'wheel-alignment': 'alignment', 'car-servicing': 'servicing', 'brakes-suspension': 'brakes', 'battery-aircond': 'battery'}.get(p, p.replace('-', '_'))


def svc_cards():
    return '<ul class="svl">' + ''.join(
        f'<li><a href="{pu(SVC_PATH[k])}">{pic(SVC_PHOTO[k], alt="")}<span class="svl-t"><b>{E(S.SERVICES[k]["name"])}</b><span>{E(S.SERVICES[k]["card"])}</span></span><i>{icon("go")}</i></a></li>'
        for k in strings_en.SVC_ORDER) + '</ul>'


# ---------- pages ----------
def home():
    H = S.HOME
    bands = ''.join(band(k, ph, svc, c, i) for i, (k, ph, svc, c) in enumerate(BANDS))
    also = ''.join(f'<a href="{pu(SVC_PATH[k])}">{E(S.SERVICES[k]["name"])}</a>' for k in ('battery', 'diagnostics'))
    body = f'''{hero()}
{promise()}
<div class="bands">{bands}</div>
<section class="sec paper also"><div class="wrap"><p><b>{E(S.UI['also_h'])}:</b> {also}</p></div></section>
{process()}
{rating('home_proof')}
{rail(F['work_strip'], S.PROOF['rail_h'], S.PROOF['rail_lead'])}
{michelin_proof()}
{identity(H['id_h'], [H['id_p']])}
{visit('home_visit', 'concrete')}
{faq(H['faq'])}
{ask('home')}'''
    return body, [org_ld(), faq_ld(H['faq'])], H['title'], H['meta']


def services_page(path):
    P = S.SERVICES_PAGE
    trail = [('', S.UI['home']), (path, S.UI['services'])]
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'default', 'hunter-fitting')}
<section class="sec paper"><div class="wrap">{svc_cards()}</div></section>
{process()}
{rail(F['work_strip'][:8], S.PROOF['rail_h'], None)}
{ask('services')}'''
    return body, [org_ld(), crumb_ld(trail)], P['title'], P['meta']


def service_page(k, path):
    V = S.SERVICES[k]
    trail = [('', S.UI['home']), ('services/', S.UI['services']), (path, V['name'])]
    lst = ''.join(f'<li>{E(x)}</li>' for x in V['list'])
    others = ''.join(f'<li><a href="{pu(SVC_PATH[o])}">{E(S.SERVICES[o]["name"])}</a></li>' for o in strings_en.SVC_ORDER if o != k)
    extra = ''
    if k == 'tyres':
        extra = f'<p class="note">{ext("michelin", "service_tyres", LK["michelin"], S.UI["michelin_link"], cls="b-more")}</p>'
    body = f'''{page_head(path, trail, V['h1'], V['lead'], k, SVC_PHOTO[k])}
<section class="sec paper"><div class="wrap two">
<div class="prose">{''.join(f'<p>{E(p)}</p>' for p in V['body'])}{extra}</div>
<aside class="card-s"><h2>{E(V['list_h'])}</h2><ul class="ticks">{lst}</ul></aside>
</div></section>
{rail(SVC_STRIP[k], S.PROOF['rail_h'], None, 'concrete')}
{process('paper')}
{faq(V['faq'], 'concrete')}
<section class="sec paper"><div class="wrap"><h2 class="sm">{E(S.UI['all_services'])}</h2><ul class="chips">{others}</ul></div></section>
{ask('service_' + slug(path), k)}'''
    return body, [org_ld(), service_ld(k, path), crumb_ld(trail), faq_ld(V['faq'])], V['title'], V['meta']


def about_page(path):
    P = S.ABOUT
    trail = [('', S.UI['home']), (path, S.UI['about'])]
    vals = ''.join(f'<li><h3>{E(a)}</h3><p>{E(b)}</p></li>' for a, b in P['vals'])
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'default', None)}
{identity(P['lead'], P['body'], link=False)}
<section class="sec concrete"><div class="wrap"><h2>{E(P['vals_h'])}</h2><ul class="pr-pts four">{vals}</ul></div></section>
{rating('about_proof')}
{rail(F['work_strip'], S.PROOF['rail_h'], S.PROOF['rail_lead'])}
{ask('about')}'''
    return body, [org_ld(), crumb_ld(trail)], P['title'], P['meta']


def contact_page(path):
    P = S.CONTACT
    trail = [('', S.UI['home']), (path, S.UI['contact'])]
    a = F['address']
    rows = f'''<ul class="cl">
<li>{wa('contact', label=S.UI['wa_label'] + ' ' + WA['display'], cls='cl-a cl-wa')}<span>{E(P['wa_note'])}</span></li>
<li>{call('contact', label=S.UI['call_short'] + ' ' + WA['display'], cls='cl-a')}<span>{E(P['wa_note'])}</span></li>
<li>{call('contact', label=S.UI['manager'] + ' ' + F['manager']['display'], cls='cl-a', who='manager')}<span>{E(P['manager_note'])}</span></li>
<li>{call('contact', label=S.UI['landline'] + ' ' + F['landline']['display'], cls='cl-a', who='landline')}<span>{E(P['landline_note'])}</span></li>
<li>{mail('contact', cls='cl-a')}</li>
<li>{ext('facebook', 'contact', LK['facebook'], F['facebook_name'], cls='cl-a', ic='fb')}</li>
</ul>'''
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'default', None)}
<section class="sec paper"><div class="wrap two">
<div class="card-s"><h2>{E(S.UI['contact_h'])}</h2>{rows}</div>
<div class="card-s"><h2>{E(S.UI['hours_h'])}</h2>{hours_table()}<p class="note">{E(S.UI['wed_closed'])}</p>
<h2 class="mt">{E(S.UI['address_h'])}</h2><address>{E(S.UI['legal'])}<br>{'<br>'.join(E(x) for x in a['lines'])}</address></div>
</div></section>
<section class="sec concrete"><div class="wrap">
<h2>{E(P['dir_h'])}</h2><p>{E(P['dir_p'])}</p>
<div class="map"><iframe src="{E(LK['map_embed'])}" title="{E(S.UI['map_title'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<div class="btns">{ext('map', 'contact', LK['maps'], S.UI['maps'], cls='b-line', ic='pin')}{ext('waze', 'contact', LK['waze'], S.UI['waze'], cls='b-line', ic='nav')}{ext('michelin', 'contact', LK['michelin'], S.UI['michelin_link'], cls='b-more')}</div>
</div></section>
{identity(S.HOME['id_h'], [S.HOME['id_p']], link=False)}
{ask('contact')}'''
    return body, [org_ld(), crumb_ld(trail)], P['title'], P['meta']


def articles_page(path):
    P = S.ARTICLES
    trail = [('', S.UI['home']), (path, S.UI['articles'])]
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'default', None)}
<section class="sec paper"><div class="wrap">{svc_cards()}</div></section>
{ask('articles')}'''
    return body, [org_ld(), crumb_ld(trail)], P['title'], P['meta']


def privacy_page(path):
    P = S.PRIVACY
    trail = [('', S.UI['home']), (path, S.UI['privacy'])]
    rows = ''.join(f'<h2>{E(h)}</h2><p>{E(t)}</p>' for h, t in P['body'])
    body = f'''<section class="ph"><div class="wrap"><div class="ph-t">{crumb_html(trail)}<h1>{E(P['h1'])}</h1></div></div></section>
<section class="sec paper"><div class="wrap narrow prose">{rows}</div></section>'''
    return body, [crumb_ld(trail)], P['title'], P['meta']


def render(path):
    if path == '':
        b, ld, t, m = home()
    elif path == 'services/':
        b, ld, t, m = services_page(path)
    elif path.startswith('services/'):
        k = [x for x, p in SVC_PATH.items() if p == path][0]
        b, ld, t, m = service_page(k, path)
    else:
        b, ld, t, m = {'about/': about_page, 'contact/': contact_page, 'articles/': articles_page, 'privacy/': privacy_page}[path](path)
    return head(path, t, m, ld) + header(path, path == '') + b + footer()


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


def zh_font_subset(src):
    """Subset Noto Sans SC to the characters the 中文 pages use: python3 build.py --fonts /path/NotoSansSC[wght].ttf"""
    import subprocess
    text = set()
    for n in dir(strings_zh):
        if n.isupper():
            text |= set(str(getattr(strings_zh, n)))
    cjk = ''.join(sorted(c for c in text if ord(c) > 0x2E7F))
    dst = os.path.join(HERE, 'assets', 'fonts', 'notosanssc-sub.woff2')
    tmp = '/tmp/ot-zh.ttf'
    subprocess.run(['fonttools', 'varLib.instancer', src, 'wght=400:700', '-o', tmp, '-q'], check=True)
    subprocess.run(['pyftsubset', tmp, f'--text={cjk}，。、：；！？（）《》“”', '--layout-features=*', '--flavor=woff2', f'--output-file={dst}'], check=True)


def main():
    global S, L, CUR
    check_keys()
    if '--fonts' in sys.argv:
        zh_font_subset(sys.argv[sys.argv.index('--fonts') + 1])
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'))
    shutil.copy(os.path.join(HERE, 'p1-cta.js'), os.path.join(OUT, 'p1-cta.js'))
    built = set()
    for LL in I18N.LANGS:
        L, S = LL, STRINGS[LL['code']]
        for p in PAGES:
            sp = I18N.page_path(L, p)
            CUR = sp
            d = os.path.join(OUT, sp)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf8').write(render(p))
            built.add(sp)
    bad = I18N.check_twins(built)
    if bad:
        raise SystemExit('\n'.join(bad))
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf8').write(I18N.sitemap_xml(absu, PAGES, TODAY))
    L, S = I18N.LANGS[0], strings_en
    a = F['address']
    lines = [f'# {F["name"]}', '', f'> {S.LLMS["intro"]}', '',
             f'- Address: {a["one_line"]}', f'- WhatsApp: {WA["intl"]} ({WA["url"]})', f'- In-Charge Manager: {F["manager"]["intl"]}',
             f'- Workshop line: {F["landline"]["intl"]}', f'- Email: {F["email"]}',
             '- Hours: Monday, Tuesday and Thursday to Sunday 9:30am to 7:30pm; closed on Wednesdays',
             f'- Google Maps: {LK["maps"]}', f'- Michelin dealer locator: {LK["michelin"]}', f'- Facebook: {LK["facebook"]}',
             '- Languages: English, Bahasa Melayu, 简体中文', '', '## Services']
    for k in strings_en.SVC_ORDER:
        lines.append(f'- {S.SERVICES[k]["name"]}: {S.SERVICES[k]["card"]} {absu(SVC_PATH[k])}')
    lines += ['', '## Pages']
    for LL in I18N.LANGS:
        for p in PAGES:
            lines.append(f'- [{LL["label"]}] {absu(I18N.page_path(LL, p))}')
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf8').write('\n'.join(lines) + '\n')
    print(f'built {len(built)} pages -> {os.path.normpath(OUT)} (base {SITE})')


if __name__ == '__main__':
    main()
