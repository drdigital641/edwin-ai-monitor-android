#!/usr/bin/env python3
"""Advance Machinery Movers site builder (AutoSEO.my client preview, 20 Nov 2026).
One template set for every page: head, header, menu sheet, footer, mobile bar, CTA links, photo blocks and schema live here
once, so one edit updates every page in every language. Facts: facts.json (from Bridge drop 6affd43013dcc9b4e971be51).
Copy: strings_en/ms/zh.py (same keys). Language plumbing (switcher, hreflang, og:locale, sitemap) comes from the shared
template autoseo-template/autoseo_i18n.py. Blocks follow autoseo-template/blocks (photo hero, soft cards, overlap block,
colour bands, floating bar), restyled for this site.

  python3 build.py                 -> preview build, canonical/hreflang/OG/schema/sitemap on https://autoseo.my/preview/advance-machinery-movers/
  python3 build.py --live DOMAIN   -> same files with https://DOMAIN/ as the absolute base (unified go-live: the domain points
                                      at this same folder). Internal links are page-relative, so they work on both hosts.
  python3 build.py --zhfont        -> refresh the Noto Sans SC subset from Google Fonts for the characters in strings_zh.py
No per-page robots meta: the preview host is noindexed by autoseo.my/preview/.htaccess (X-Robots-Tag). Then python3 check.py
before any Bridge upload (sync_from_github, site autoseo, base_path preview/advance-machinery-movers).
Photos are not in the repo: they live on the server in preview/advance-machinery-movers/images/ (published from the drop)."""
import hashlib, html, json, os, shutil, sys, urllib.parse
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

SVC_PATH = {'rigging': 'services/rigging-millwright/', 'relocation': 'services/plant-relocation/',
            'stuffing': 'services/container-stuffing-unstuffing/', 'crating': 'services/wooden-crates-vacuum-packing/',
            'alignment': 'services/precision-alignment/', 'rental': 'services/heavy-forklift-side-loader-rental/'}
PAGES = ['', 'services/'] + [SVC_PATH[k] for k in strings_en.SVC_ORDER] + ['about/', 'contact/', 'articles/', 'privacy/']
NAV = [('services/', 'services'), ('about/', 'about'), ('contact/', 'contact'), ('articles/', 'articles')]
SVC_PHOTO = {'rigging': 'crane-lift', 'relocation': 'plant-relocation', 'stuffing': 'container-stuffing',
             'crating': 'wooden-crates', 'alignment': 'precision-install', 'rental': 'heavy-forklift'}
SVC_STRIP = {'rigging': ['crane-lift', 'dismantling', 'heavy-forklift', 'plant-relocation', 'precision-install'],
             'relocation': ['plant-relocation', 'crane-lift', 'container-lift', 'dismantling', 'precision-install'],
             'stuffing': ['container-stuffing', 'container-lift', 'wooden-crates'],
             'crating': ['wooden-crates', 'protective-packing', 'container-stuffing'],
             'alignment': ['precision-install', 'dismantling'],
             'rental': ['heavy-forklift', 'fleet', 'wooden-crates']}
SLUG = {'rigging': 'rigging', 'relocation': 'relocation', 'stuffing': 'stuffing', 'crating': 'crating', 'alignment': 'alignment', 'rental': 'rental'}


# ---------- paths ----------
def rel(target=''):
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
        'fax': '<path d="M7 9V4h10v5M6 19H4.5A1.5 1.5 0 0 1 3 17.5v-7A1.5 1.5 0 0 1 4.5 9h15a1.5 1.5 0 0 1 1.5 1.5v7a1.5 1.5 0 0 1-1.5 1.5H18M7 15h10v5H7z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/>',
        'menu': '<path d="M4 7h16M4 12h16M4 17h11" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        'x': '<path d="M6 6l12 12M18 6L6 18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
        'prev': '<path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        'next': '<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        'go': '<path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
        'cross': '<circle cx="12" cy="12" r="7" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 2v6M12 16v6M2 12h6M16 12h6" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="1.6" fill="currentColor"/>',
        'check': '<path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'


# ---------- CTA links (data-cta = data-ref = placement; the Controller reads the whatsapp_/call_/... prefix) ----------
def wa_url(key='default'):
    return f"{WA['url']}?text={urllib.parse.quote(S.PREFILL[key])}"


def wa(place, key='default', label=None, cls='b-wa'):
    return (f'<a class="{cls}" href="{E(wa_url(key))}" target="_blank" rel="noopener" data-cta="whatsapp_{place}" data-ref="whatsapp_{place}">'
            f'{icon("wa")}<span>{E(label or S.UI["wa_btn"])}</span></a>')


def call(place, label=None, cls='b-call'):
    return (f'<a class="{cls}" href="{F["landline"]["tel"]}" data-cta="call_{place}" data-ref="call_{place}">'
            f'{icon("call")}<span>{E(label or S.UI["call_btn"])}</span></a>')


def ext(kind, place, href, label, cls=None, ic=None):
    c = f' class="{cls}"' if cls else ''
    i = icon(ic) if ic else ''
    return f'<a{c} href="{E(href)}" target="_blank" rel="noopener" data-cta="{kind}_{place}" data-ref="{kind}_{place}">{i}<span>{E(label)}</span></a>'


def mail(place, who='general', cls=None):
    addr = F['email'] if who == 'general' else F['email_meiwan']
    kind = 'email' if who == 'general' else 'email_meiwan'
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="mailto:{addr}" data-cta="{kind}_{place}" data-ref="{kind}_{place}">{icon("mail")}<span>{E(addr)}</span></a>'


# ---------- media ----------
def pic(stem, alt=None, cls=None, eager=False, pos=True):
    m = PH[stem]
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager == 'high' else ('' if eager else ' loading="lazy"')
    st = f' style="object-position:{m["pos"]}"' if pos and 'pos' in m else ''
    a = S.CAPS.get(stem, '') if alt is None else alt
    return (f'<picture{c}><source type="image/webp" srcset="{rel("images/" + stem + ".webp")}">'
            f'<img src="{rel("images/" + stem + ".jpg")}" width="{m["w"]}" height="{m["h"]}" alt="{E(a)}"{load} decoding="async"{st}></picture>')


def logo(kind='color', cls='lg', eager=True):
    stem = F['logo'][kind]
    load = '' if eager else ' loading="lazy"'
    return (f'<picture class="{cls}"><source type="image/webp" srcset="{rel("images/" + stem + ".webp")}">'
            f'<img src="{rel("images/" + stem + ".png")}" width="{F["logo"]["w"]}" height="{F["logo"]["h"]}" alt="{E(S.CAPS["logo"])}"{load} decoding="async"></picture>')


# ---------- shared page parts ----------
def head(path, title, meta, ld):
    css = os.path.join(HERE, 'assets', 'site.css')
    zh = L['code'] == 'zh'
    zh_font = f'<link rel="preload" href="{rel("assets/fonts/notosanssc-sub-400.woff2")}" as="font" type="font/woff2" crossorigin>' if zh else ''
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
<meta name="theme-color" content="#111318">
<link rel="icon" href="{rel('assets/favicon-48.png')}" type="image/png" sizes="48x48">
<link rel="icon" href="{rel('assets/icon-192.png')}" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{rel('assets/touch-icon.png')}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(F['short'])}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta)}">
<meta property="og:url" content="{pabs(path)}">
<meta property="og:image" content="{absu('images/og.jpg')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(S.CAPS['og'])}">
{I18N.og_locale_tags(L)}
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{rel('assets/fonts/rajdhani-700.woff2')}" as="font" type="font/woff2" crossorigin>
{zh_font}
<link rel="stylesheet" href="{rel('assets/site.css')}?v={ver(css)}">
{ldj}
</head>'''


def header(path, over_photo):
    nav = ''.join(f'<a href="{pu(p)}"{" aria-current=\"page\"" if path == p or (p == "services/" and path.startswith(p)) else ""}>{E(S.UI[k])}</a>' for p, k in NAV)
    sheet = ''.join(f'<a href="{pu(p)}">{E(S.UI[k])}</a>' for p, k in [('', 'home')] + NAV + [('privacy/', 'privacy')])
    return f'''<body class="{'over' if over_photo else 'plain'}">
<a class="skip" href="#main">{E(S.UI['skip'])}</a>
<header class="top"><div class="wrap top-in">
<a class="brand" href="{pu('')}" aria-label="{E(F['short'])}">{logo('inverse', 'lg lg-inv')}{logo('color', 'lg lg-col')}</a>
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
            f'<tr class="off"><th>{E(S.UI["sun"])}</th><td>{E(S.UI["closed"])}</td></tr></tbody></table>')


def footer():
    return f'''</main>
<footer class="ft"><div class="wrap">
<div class="ft-g">
<div class="ft-id">
<a class="brand" href="{pu('')}" aria-label="{E(F['short'])}">{logo('inverse', 'lg', eager=False)}</a>
<p class="ft-legal">{E(F['name'])} <span class="num">({E(F['company_no'])})</span><br><span lang="zh-Hant">{E(F['chinese_name'])}</span></p>
<p class="ft-sign" lang="ms">{E(F['malay_signboard'])}</p>
<address>{'<br>'.join(E(x) for x in F['address']['lines'])}</address>
<p class="ft-hrs">{E(S.UI['hours_line'])}</p>
</div>
<div><h2>{E(S.UI['contact_h'])}</h2><ul>
<li>{wa('footer', label=S.UI['wa_label'] + ' ' + WA['display'], cls='fl')}<small>{E(S.UI['wa_who'])}</small></li>
<li>{call('footer', label=S.UI['landline'] + ' ' + F['landline']['display'], cls='fl')}</li>
<li class="fl fx">{icon('fax')}<span>{E(S.UI['fax'])} <span class="num">{E(F['fax']['display'])}</span></span></li>
<li>{mail('footer', cls='fl')}</li>
<li>{mail('footer', who='meiwan', cls='fl')}</li>
</ul></div>
<div><h2>{E(S.UI['find_h'])}</h2><ul>
<li>{ext('map', 'footer', LK['maps'], S.UI['maps'], cls='fl', ic='pin')}</li>
<li>{ext('waze', 'footer', LK['waze'], S.UI['waze'], cls='fl', ic='nav')}</li>
</ul>
<h2 class="mt">{E(S.UI['services'])}</h2><ul class="ft-sv">{''.join(f'<li><a href="{pu(SVC_PATH[k])}">{E(S.SERVICES[k]["name"])}</a></li>' for k in strings_en.SVC_ORDER)}</ul></div>
</div>
<div class="ft-b"><span>&copy; 2026 {E(F['name'])}</span><a href="{pu('privacy/')}">{E(S.UI['privacy'])}</a><a href="https://autoseo.my/">Website by AutoSEO.my</a></div>
</div></footer>
<div class="mbar">{wa('mobile_bar', label=S.UI['wa_label'])}{call('mobile_bar', label=S.UI['call_short'], cls='b-call')}</div>
<script src="{rel('assets/site.js')}?v={ver(os.path.join(HERE, 'assets', 'site.js'))}" defer></script>
<script src="{rel('p1-cta.js')}?v={ver(os.path.join(HERE, 'p1-cta.js'))}" defer></script>
</body>
</html>
'''


# ---------- schema (one facts file) ----------
def org_ld():
    a = F['address']
    return {
        '@context': 'https://schema.org', '@type': 'LocalBusiness', '@id': SITE + '#business',
        'name': F['name'], 'alternateName': [F['short'], F['chinese_name'], F['malay_signboard']],
        'legalName': F['name'], 'identifier': {'@type': 'PropertyValue', 'propertyID': 'SSM company no.', 'value': F['company_no']},
        'foundingDate': str(F['incorporated']),
        'description': S.SCHEMA['description'], 'url': pabs(''), 'image': absu('images/og.jpg'), 'logo': absu('images/logo.png'),
        'telephone': F['landline']['e164'], 'faxNumber': F['fax']['e164'], 'email': F['email'],
        'address': {'@type': 'PostalAddress', 'streetAddress': a['street'], 'addressLocality': a['city'], 'addressRegion': a['region'],
                    'postalCode': a['postcode'], 'addressCountry': a['country']},
        'geo': {'@type': 'GeoCoordinates', 'latitude': F['geo']['lat'], 'longitude': F['geo']['lng']},
        'hasMap': LK['maps'],
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': h['days'], 'opens': h['opens'], 'closes': h['closes']} for h in F['hours']],
        'contactPoint': [
            {'@type': 'ContactPoint', 'contactType': 'sales', 'name': WA['name'], 'telephone': WA['e164'], 'url': WA['url'],
             'email': F['email_meiwan'], 'availableLanguage': ['en', 'ms', 'zh']},
            {'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': F['landline']['e164'], 'email': F['email']},
        ],
        'areaServed': [{'@type': 'Country', 'name': 'Malaysia'}, {'@type': 'Country', 'name': 'Singapore'}],
        'knowsAbout': S.SCHEMA['knows'],
        'makesOffer': [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': S.SERVICES[k]['name'], 'url': pabs(SVC_PATH[k])}} for k in strings_en.SVC_ORDER],
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
            'url': pabs(path), 'image': absu('images/' + SVC_PHOTO[k] + '.jpg'), 'provider': {'@id': SITE + '#business'},
            'areaServed': [{'@type': 'Country', 'name': 'Malaysia'}, {'@type': 'Country', 'name': 'Singapore'}]}


def crumb_html(trail):
    li = ''.join(f'<li><a href="{pu(p)}"{" aria-current=\"page\"" if i == len(trail) - 1 else ""}>{E(n)}</a></li>' for i, (p, n) in enumerate(trail))
    return f'<nav class="crumb" aria-label="{E(S.UI["breadcrumb"])}"><ol>{li}</ol></nav>'


# ---------- blocks ----------
def authority():
    return (f'<p class="auth"><b>{E(S.UI["authority"])}</b>'
            f'<span>{E(S.UI["company_no"])} <span class="num">{E(F["company_no"])}</span></span><span>{E(S.UI["where"])}</span></p>')


def hero():
    """Photo hero (autoseo-template/blocks photo_hero, restyled): the 4:5 crew-and-signboard photo stays whole on phones
    (signboard + all four crew), fading into charcoal; on desktop it stands at the right with the type on charcoal."""
    H = S.HOME
    return f'''<section class="hero">
<div class="hero-ph">{pic('cover', eager='high')}</div>
<div class="wrap hero-in">
<div class="hero-t">
<h1>{E(H['h1'])}</h1>
{authority()}
<div class="hero-cta">{wa('home_hero', label=S.UI['wa_hero'])}{call('home_hero', label=S.UI['call_short'], cls='b-ghost')}</div>
</div></div></section>'''


def promise():
    H = S.HOME
    pts = ''.join(f'<li>{icon("cross")}<div><h3>{E(a)}</h3><p>{E(b)}</p></div></li>' for a, b in H['promise_pts'])
    return f'''<section class="sec paper promise"><div class="wrap pr-in">
<div class="pr-t"><h2>{E(H['promise_h'])}</h2><p>{E(H['promise'])}</p></div>
<ul class="pr-pts">{pts}</ul>
</div></section>'''


def journey():
    """Services pattern: one machine's path (lift, crate, container, install/align), a vertical alignment line with a
    crosshair at every stop and a real job photo per stop."""
    H = S.HOME
    stops = ''
    for i, (k, photo, h, p) in enumerate(H['journey']):
        stops += f'''<li class="jst{' flip' if i % 2 else ''}">
<span class="jst-pin" aria-hidden="true">{icon('cross')}</span>
<figure class="jst-ph">{pic(photo)}<figcaption>{E(S.CAPS[photo])}</figcaption></figure>
<div class="jst-t"><p class="jst-n num">{E(S.UI['stop'])} {i + 1}</p><h3>{E(h)}</h3><p>{E(p)}</p>
<a class="b-more" href="{pu(SVC_PATH[k])}">{E(S.SERVICES[k]['name'])}{icon('go')}</a></div></li>'''
    return f'''<section class="sec steel journey"><div class="wrap">
<div class="sec-h"><h2>{E(H['journey_h'])}</h2><p>{E(H['journey_lead'])}</p></div>
<ol class="jr">{stops}</ol>
</div></section>'''


def more_cards(keys, h=None, cls='paper'):
    cards = ''.join(f'''<li class="sc"><a href="{pu(SVC_PATH[k])}">{pic(SVC_PHOTO[k], alt='')}
<span class="sc-t"><b>{E(S.SERVICES[k]['name'])}</b><span>{E(S.SERVICES[k]['card'])}</span></span><i>{icon('go')}</i></a></li>''' for k in keys)
    hd = f'<div class="sec-h"><h2>{E(h)}</h2></div>' if h else ''
    return f'<section class="sec {cls}"><div class="wrap">{hd}<ul class="scs">{cards}</ul></div></section>'


def timeline(cls='paper', place='home_timeline'):
    """Process pattern: six-stop plant-relocation timeline on a steel rule, crosshair pins, brown/green trim only."""
    items = ''.join(f'<li><span class="tl-pin" aria-hidden="true"></span><p class="tl-n num">{i + 1:02d}</p><h3>{E(a)}</h3><p>{E(b)}</p></li>'
                    for i, (a, b) in enumerate(S.TIMELINE))
    return f'''<section class="sec {cls} tline"><div class="wrap">
<div class="sec-h"><h2>{E(S.HOME['timeline_h'])}</h2><p>{E(S.HOME['timeline_lead'])}</p></div>
<ol class="tl">{items}</ol>
<div class="btns">{wa(place, 'relocation', cls='b-wa b-sm')}<a class="b-more" href="{pu(SVC_PATH['relocation'])}">{E(S.SERVICES['relocation']['name'])}{icon('go')}</a></div>
</div></section>'''


def rail(stems, h2=None, lead=None, cls='paper'):
    """4:5 work carousel. Behaviour copies Wrapstar ws.js glide (site.js): native drag, rAF autoplay with cloned children,
    hold or sideways drag pauses, resumes 1.5 s after release, reduced motion = no autoplay. No touch-action on the rail."""
    figs = ''.join(f'<figure class="card">{pic(s)}<figcaption>{E(S.CAPS[s])}</figcaption></figure>' for s in stems)
    hd = f'<div class="sec-h"><h2>{E(h2)}</h2>{f"<p>{E(lead)}</p>" if lead else ""}</div>' if h2 else ''
    return f'''<section class="sec {cls} work"><div class="wrap">{hd}
<div class="glide" tabindex="0" aria-label="{E(h2 or S.HOME['rail_h'])}">{figs}</div>
<div class="rail-c"><button type="button" class="arr" data-dir="-1" aria-label="{E(S.UI['prev'])}">{icon('prev')}</button><button type="button" class="arr" data-dir="1" aria-label="{E(S.UI['next'])}">{icon('next')}</button></div>
</div></section>'''


def fleet():
    """Proof: fleet strip (wide photo) + CNY team photo, overlapping (blocks lap_block idea)."""
    H = S.HOME
    return f'''<section class="sec steel fleet"><div class="wrap fl-in">
<figure class="fl-wide">{pic('fleet')}<figcaption>{E(S.CAPS['fleet'])}</figcaption></figure>
<div class="fl-card"><h2>{E(H['fleet_h'])}</h2><p>{E(H['fleet_p'])}</p>
<div class="btns">{wa('home_fleet', 'rental', cls='b-wa b-sm')}<a class="b-more" href="{pu(SVC_PATH['rental'])}">{E(S.SERVICES['rental']['name'])}{icon('go')}</a></div></div>
<figure class="fl-team">{pic('team-cny')}<figcaption>{E(H['team_p'])}</figcaption></figure>
</div></section>'''


def signboard():
    return (f'<div class="sign" aria-label="{E(S.ABOUT["sign_h"])}"><span lang="ms">{E(F["malay_signboard"])}</span>'
            f'<span lang="zh-Hant">{E(F["chinese_name"])}</span><span>{E(F["name"].upper())} <small class="num">({E(F["company_no"])})</small></span></div>')


def visit(place, cls='paper'):
    return f'''<section class="sec {cls} visit"><div class="wrap visit-in">
<div class="card-s"><h2>{E(S.UI['hours_h'])}</h2>{hours_table()}</div>
<div class="card-s"><h2>{E(S.UI['address_h'])}</h2><address>{E(F['name'])}<br>{'<br>'.join(E(x) for x in F['address']['lines'])}</address>
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
    ph = f'<figure class="ph-ph">{pic(photo, eager="high")}</figure>' if photo else ''
    return f'''<section class="ph{' has-ph' if photo else ''}"><div class="wrap ph-in">
<div class="ph-t">{crumb_html(trail)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>
<div class="btns">{wa(slug(path) + '_head', key)}{call(slug(path) + '_head', cls='b-ghost-d')}</div></div>{ph}
</div></section>'''


def slug(path):
    p = path.strip('/').split('/')[-1] if path else 'home'
    inv = {v.strip('/').split('/')[-1]: k for k, v in SVC_PATH.items()}
    return 'service_' + inv[p] if p in inv else p.replace('-', '_')


# ---------- pages ----------
def home():
    H = S.HOME
    body = f'''{hero()}
{promise()}
{journey()}
{more_cards(['relocation', 'rental'], H['more_h'])}
{timeline('steel', 'home_timeline')}
{rail(F['work_strip'], H['rail_h'], H['rail_lead'])}
{fleet()}
{visit('home_visit', 'paper')}
{faq(H['faq'], 'steel')}
{ask('home')}'''
    return body, [org_ld(), faq_ld(H['faq'])], H['title'], H['meta']


def services_page(path):
    P = S.SERVICES_PAGE
    trail = [('', S.UI['home']), (path, S.UI['services'])]
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'default', 'dismantling')}
{more_cards(strings_en.SVC_ORDER, None, 'paper')}
{timeline('steel', 'services_timeline')}
{rail(F['work_strip'], S.HOME['rail_h'], None)}
{ask('services')}'''
    return body, [org_ld(), crumb_ld(trail)], P['title'], P['meta']


def service_page(k, path):
    V = S.SERVICES[k]
    trail = [('', S.UI['home']), ('services/', S.UI['services']), (path, V['name'])]
    lst = ''.join(f'<li>{icon("check")}<span>{E(x)}</span></li>' for x in V['list'])
    others = ''.join(f'<li><a href="{pu(SVC_PATH[o])}">{E(S.SERVICES[o]["name"])}</a></li>' for o in strings_en.SVC_ORDER if o != k)
    tl = timeline('steel', 'service_' + k + '_timeline') if k in ('rigging', 'relocation', 'alignment') else ''
    body = f'''{page_head(path, trail, V['h1'], V['lead'], k, SVC_PHOTO[k])}
<section class="sec paper"><div class="wrap two">
<div class="prose">{''.join(f'<p>{E(p)}</p>' for p in V['body'])}</div>
<aside class="card-s"><h2>{E(V['list_h'])}</h2><ul class="ticks">{lst}</ul></aside>
</div></section>
{rail(SVC_STRIP[k], S.HOME['rail_h'], None, 'steel' if not tl else 'paper')}
{tl}
{faq(V['faq'], 'paper' if tl else 'steel')}
<section class="sec paper"><div class="wrap"><h2 class="sm">{E(S.UI['all_services'])}</h2><ul class="chips">{others}</ul></div></section>
{ask('service_' + k, k)}'''
    return body, [org_ld(), service_ld(k, path), crumb_ld(trail), faq_ld(V['faq'])], V['title'], V['meta']


def about_page(path):
    P = S.ABOUT
    trail = [('', S.UI['home']), (path, S.UI['about'])]
    safety = ''.join(f'<li>{icon("cross")}<div><h3>{E(a)}</h3><p>{E(b)}</p></div></li>' for a, b in P['safety'])
    vis = ''.join(f'<li>{E(x)}</li>' for x in P['vision'])
    mis = ''.join(f'<li>{E(x)}</li>' for x in P['mission'])
    cust = ''.join(f'<li>{E(c)}</li>' for c in F['customers'])
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'default', None)}
<section class="sec paper"><div class="wrap lap">
<figure class="lap-img">{pic('unit-14')}<figcaption>{E(S.CAPS['unit-14'])}</figcaption></figure>
<div class="lap-card"><h2>{E(P['story_h'])}</h2>{''.join(f'<p>{E(p)}</p>' for p in P['story'])}{authority()}</div>
</div></section>
<section class="sec steel"><div class="wrap narrow"><h2>{E(P['sign_h'])}</h2><p>{E(P['sign_p'])}</p>{signboard()}</div></section>
<section class="sec paper"><div class="wrap two">
<div><h2>{E(P['safety_h'])}</h2><ul class="pr-pts one">{safety}</ul></div>
<figure class="ph-side">{pic('training')}<figcaption>{E(S.CAPS['training'])}</figcaption></figure>
</div></section>
<section class="sec steel"><div class="wrap"><h2>{E(P['vm_h'])}</h2><div class="vm">
<div class="card-s"><h3>{E(P['vision_h'])}</h3><ul class="ticks plain">{vis}</ul></div>
<div class="card-s"><h3>{E(P['mission_h'])}</h3><ul class="ticks plain">{mis}</ul></div></div></div></section>
<section class="sec paper"><div class="wrap"><h2>{E(S.UI['served_h'])}</h2><p class="note">{E(P['served_p'])}</p><ul class="cust">{cust}</ul></div></section>
<section class="sec steel"><div class="wrap two">
<figure class="ph-side">{pic('team-cny')}<figcaption>{E(S.CAPS['team-cny'])}</figcaption></figure>
<div><h2>{E(P['team_h'])}</h2><p>{E(S.HOME['team_p'])}</p>{ext('map', 'about', LK['maps'], S.UI['listing'], cls='b-line', ic='pin')}</div>
</div></section>
{ask('about')}'''
    return body, [org_ld(), crumb_ld(trail)], P['title'], P['meta']


def contact_page(path):
    P = S.CONTACT
    trail = [('', S.UI['home']), (path, S.UI['contact'])]
    rows = f'''<ul class="cl">
<li>{wa('contact', label=S.UI['wa_label'] + ' ' + WA['display'], cls='cl-a cl-wa')}<span>{E(S.UI['wa_who'])}. {E(P['wa_note'])}</span></li>
<li>{call('contact', label=S.UI['landline'] + ' ' + F['landline']['display'], cls='cl-a')}<span>{E(P['office_note'])}</span></li>
<li><span class="cl-a cl-x">{icon('fax')}<span>{E(S.UI['fax'])} <span class="num">{E(F['fax']['display'])}</span></span></span></li>
<li>{mail('contact', cls='cl-a')}<span>{E(S.UI['email_general'])}</span></li>
<li>{mail('contact', who='meiwan', cls='cl-a')}<span>{E(S.UI['email_meiwan'])}</span></li>
</ul>'''
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'default', None)}
<section class="sec paper"><div class="wrap two">
<div class="card-s"><h2>{E(S.UI['contact_h'])}</h2>{rows}</div>
<div class="card-s"><h2>{E(S.UI['hours_h'])}</h2>{hours_table()}
<h2 class="mt">{E(S.UI['address_h'])}</h2><address>{E(F['name'])}<br><span lang="zh-Hant">{E(F['chinese_name'])}</span><br>{'<br>'.join(E(x) for x in F['address']['lines'])}</address></div>
</div></section>
<section class="sec steel"><div class="wrap">
<h2>{E(P['dir_h'])}</h2><p>{E(P['dir_p'])}</p>
<div class="map"><iframe src="{E(LK['map_embed'])}" title="{E(S.UI['map_title'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
<div class="btns">{ext('map', 'contact', LK['maps'], S.UI['maps'], cls='b-line', ic='pin')}{ext('waze', 'contact', LK['waze'], S.UI['waze'], cls='b-line', ic='nav')}</div>
</div></section>
<section class="sec paper"><div class="wrap two">
<figure class="ph-side">{pic('unit-14')}<figcaption>{E(S.CAPS['unit-14'])}</figcaption></figure>
<div>{signboard()}</div></div></section>
{ask('contact')}'''
    return body, [org_ld(), crumb_ld(trail)], P['title'], P['meta']


def articles_page(path):
    P = S.ARTICLES
    trail = [('', S.UI['home']), (path, S.UI['articles'])]
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'default', None)}
{more_cards(strings_en.SVC_ORDER, None, 'paper')}
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


def zh_font_subset():
    """Download a Noto Sans SC subset (400 + 700) holding only the characters the 中文 pages use, from Google Fonts' text= API."""
    import re, urllib.request
    text = set()
    for n in dir(strings_zh):
        if n.isupper():
            text |= set(str(getattr(strings_zh, n)))
    text |= set(F['chinese_name']) | set(F['whatsapp']['name_zh'])
    cjk = ''.join(sorted(c for c in text if ord(c) > 0x2E7F)) + '，。、：；！？（）《》“”'
    ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36'}
    for w in (400, 700):
        u = 'https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@%d&text=%s' % (w, urllib.parse.quote(cjk))
        css = urllib.request.urlopen(urllib.request.Request(u, headers=ua)).read().decode()
        src = re.search(r'url\((https://[^)]+)\)', css).group(1)
        data = urllib.request.urlopen(urllib.request.Request(src, headers=ua)).read()
        open(os.path.join(HERE, 'assets', 'fonts', f'notosanssc-sub-{w}.woff2'), 'wb').write(data)
        print(f'zh font {w}: {len(cjk)} chars, {len(data)} bytes')


def main():
    global S, L, CUR
    check_keys()
    if '--zhfont' in sys.argv:
        zh_font_subset()
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
             f'- Company no.: {F["company_no"]}', f'- Chinese name: {F["chinese_name"]}', f'- Signboard (Malay): {F["malay_signboard"]}',
             f'- Incorporated: {F["incorporated"]} in Johor Bahru ({F["years"]} years in operation in 2026; 30th anniversary in {F["anniversary_30th"]})',
             f'- Address: {a["one_line"]}',
             f'- WhatsApp: {WA["intl"]} ({WA["url"]}), {WA["name"]}, {WA["title"]}', f'- Office: {F["landline"]["intl"]}', f'- Fax: {F["fax"]["intl"]}',
             f'- Email: {F["email"]} (general), {F["email_meiwan"]} ({WA["name"]})',
             '- Hours: Monday to Saturday 8:00am to 5:00pm; Sunday closed', '- Service area: Malaysia and Singapore',
             f'- Google Maps: {LK["maps"]}', f'- Waze: {LK["waze"]}',
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
