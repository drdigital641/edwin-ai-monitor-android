#!/usr/bin/env python3
"""JT Autoworks site builder (AutoSEO.my client preview, 20 Nov 2026).
One template set for every page: head, header, menu sheet, footer, mobile bar, CTA links, package cards, video facade and schema
live here once, so one edit updates every page in every language. Facts: facts.json. Copy: strings_en/ms/zh.py (same keys).
Language plumbing (switcher, hreflang, og:locale, sitemap) comes from the shared template ../../../autoseo-template/autoseo_i18n.py.
  python3 build.py                 -> preview build for https://autoseo.my/preview/jt-autoworks/ (noindex, nofollow)
  python3 build.py --live DOMAIN   -> build for https://DOMAIN/ (still noindex until Edwin approves go-live)
Then python3 check.py (pre-upload gate) before any Bridge upload (sync_from_github, site autoseo, base_path preview/jt-autoworks).
Media: src/media/ (prepared by prep_media.py from the Bridge drop) with media/manifest.json; any image block whose file is
missing is left out, never shown empty."""
import hashlib, html, json, os, re, shutil, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'autoseo-template'))
import autoseo_i18n as I18N
import strings_en, strings_ms, strings_zh
STRINGS = {'en': strings_en, 'ms': strings_ms, 'zh': strings_zh}
S, L = strings_en, I18N.LANGS[0]

F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
LIVE = '--live' in sys.argv
if LIVE:
    DOMAIN = sys.argv[sys.argv.index('--live') + 1]
    ORIGIN, BASE = f'https://{DOMAIN}', '/'
else:
    ORIGIN, BASE = 'https://autoseo.my', F['preview']['base_path']
SITE = ORIGIN + BASE
OUT = os.path.join(HERE, '..', 'dist')
MEDIA_DIR = os.path.join(HERE, 'media')
E = html.escape
LK = F['links']
SHOW_OWNER = bool(F['flags']['show_owner_name'])
TODAY = '2026-11-20'

_mf = os.path.join(MEDIA_DIR, 'manifest.json')
MEDIA = json.load(open(_mf, encoding='utf8')) if os.path.exists(_mf) else {}   # stem -> {"file":..., "w":..., "h":...}


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


def has(stem):
    return stem in MEDIA


def murl(stem):
    return u('media/' + MEDIA[stem]['file'])


def mabs(stem):
    return absu('media/' + MEDIA[stem]['file'])


def T(s):
    """Fill {tech}: 'our technician' while the owner flag is off (Edwin has not OK'd the name yet)."""
    return s.replace('{tech}', F['owner_name'] if SHOW_OWNER else S.TECH)


def wa_url(key='default'):
    return f"{F['whatsapp']['url']}?text={urllib.parse.quote(S.PREFILL[key])}"


def icon(name):
    p = {
        'wa': '<path d="M4.6 19.4l1.1-3.5a7.9 7.9 0 1 1 2.9 2.7z"/><path d="M9.3 8.7c.3 2.5 2.3 4.7 5 5.2l.9-1.1 1.8.8-.3 1.5c-3.8.4-7.7-3.5-7.5-7.3l1.5-.3.8 1.7z"/>',
        'call': '<path d="M5.2 4h3.6l1.6 4-2.1 1.3a10.6 10.6 0 0 0 6.4 6.4l1.3-2.1 4 1.6v3.6a1.6 1.6 0 0 1-1.7 1.6C10.4 19.9 4.1 13.6 3.6 5.7A1.6 1.6 0 0 1 5.2 4z"/>',
        'pin': '<path d="M12 21s-6.4-5.5-6.4-10.9a6.4 6.4 0 0 1 12.8 0C18.4 15.5 12 21 12 21z"/><circle cx="12" cy="10.1" r="2.2"/>',
        'nav': '<path d="M4 11.4L20 4l-7.4 16-1.7-6.9z"/>',
        'star': '<path d="M5 19V5h9l-1.5 3.5L14 12H6.5"/>',
        'menu': '<path d="M4 7h16M4 12h16M4 17h11"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
        'go': '<path d="M5 12h13M13 6l6 6-6 6"/>', 'prev': '<path d="M15 5l-7 7 7 7"/>', 'next': '<path d="M9 5l7 7-7 7"/>',
        'mail': '<rect x="3.5" y="6" width="17" height="12" rx="1.5"/><path d="M4 7l8 6 8-6"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'


# ---------- CTA links (data-cta = data-ref = placement; the Controller reads the whatsapp_/call_/... prefix) ----------
def wa(place, key='default', label=None, cls='go-wa'):
    return (f'<a class="{cls}" href="{E(wa_url(key))}" target="_blank" rel="noopener" data-cta="whatsapp_{place}" data-ref="whatsapp_{place}">'
            f'{icon("wa")}<span>{E(label or S.UI["wa_btn"])}</span></a>')


def call(place, label=None, cls='go-call'):
    return (f'<a class="{cls}" href="{F["phone"]["tel"]}" data-cta="call_{place}" data-ref="call_{place}">'
            f'{icon("call")}<span>{E(label or S.UI["call_btn"])}</span></a>')


def ext(kind, place, href, label, cls=None, ic=None):
    c = f' class="{cls}"' if cls else ''
    i = icon(ic) if ic else ''
    return (f'<a{c} href="{E(href)}" target="_blank" rel="noopener" data-cta="{kind}_{place}" data-ref="{kind}_{place}">{i}<span>{E(label)}</span></a>')


def mail(place, cls=None):
    c = f' class="{cls}"' if cls else ''
    return f'<a{c} href="mailto:{F["email"]}" data-cta="email_{place}" data-ref="email_{place}">{E(F["email"])}</a>'


# ---------- pages ----------
SVC_PATH = {'diagnostics': 'services/diagnostics/', 'aircon': 'services/aircon/', 'battery': 'services/battery/', 'ev': 'services/ev/',
            'ppi': 'services/pre-purchase-inspection/', 'towing': 'services/towing/', 'german': 'services/german-luxury-cars/'}
PAGES = ['', 'packages/', 'services/'] + [SVC_PATH[k] for k in strings_en.SERVICE_ORDER] + ['find-us/', 'about/', 'areas/', 'articles/', 'privacy/']
NAV = [('packages/', 'packages'), ('services/', 'services'), ('find-us/', 'find_us'), ('about/', 'about')]
SVC_REEL = {'diagnostics': 'diagnostics', 'ppi': 'used_car', 'german': 'bmw5'}   # only reels with a real poster frame
REEL_BY_TOPIC = {r['topic']: r for r in F['reels']}
HOME_STRIP = ['new_chapter', 'bmw5', 'used_car', 'diagnostics']   # Edwin's order, 20 Nov; tiles without a poster frame are skipped


def logo(cls='wm'):
    if has('logo'):
        m = MEDIA['logo']
        return f'<img src="{murl("logo")}" width="{m["w"]}" height="{m["h"]}" alt="JT Autoworks">'
    return '<span class="wm-t">J<b>T</b> AUTOWORKS</span>'


def head(path, title, meta, ld):
    og = mabs('og') if has('og') else absu('media/og.jpg')
    css = os.path.join(HERE, 'assets', 'site.css')
    zh_font = ('<link rel="preload" href="' + u('assets/fonts/notosanssc-sub.woff2') + '" as="font" type="font/woff2" crossorigin>') if L['code'] == 'zh' else ''
    ldj = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="{L['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(meta)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{pabs(path)}">
{I18N.hreflang_links(absu, path)}
<meta name="theme-color" content="#0F2140">
<link rel="icon" href="{u('media/favicon-32.png') if has('favicon-32') else u('assets/favicon.svg')}">
{f'<link rel="apple-touch-icon" href="{murl("touch-icon")}">' if has('touch-icon') else ''}
<meta property="og:type" content="website">
<meta property="og:site_name" content="JT Autoworks">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta)}">
<meta property="og:url" content="{pabs(path)}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="JT AUTOWORKS signboard, Premier @ Kaki Bukit">
{I18N.og_locale_tags(L)}
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="{u('assets/fonts/sora-var.woff2')}" as="font" type="font/woff2" crossorigin>
{zh_font}
<link rel="stylesheet" href="{u('assets/site.css')}?v={ver(css)}">
{ldj}
</head>'''


def header(path):
    nav = ''.join(f'<a href="{pu(p)}"{" aria-current=\"page\"" if path == p or (p and path.startswith(p) and p == "services/") else ""}>{E(S.UI[k])}</a>' for p, k in NAV)
    sheet_nav = ''.join(f'<a href="{pu(p)}">{E(S.UI[k])}</a>' for p, k in [('', 'home')] + NAV + [('areas/', 'areas'), ('articles/', 'articles')])
    return f'''<body>
<a class="skip" href="#main">{E(S.UI['skip'])}</a>
<header class="top"><div class="wrap">
<a class="wm" href="{pu('')}" aria-label="JT Autoworks">{logo()}</a>
<nav class="nav" aria-label="{E(S.UI['menu'])}">{nav}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='tabs')}
{wa('header')}
<button class="mb" type="button" aria-expanded="false" aria-controls="sheet" aria-label="{E(S.UI['menu'])}">{icon('menu')}</button>
</div></header>
<div class="sheet" id="sheet" hidden><div class="sheet-in" role="dialog" aria-modal="true" aria-label="{E(S.UI['menu'])}">
<button class="sheet-x" type="button" aria-label="{E(S.UI['close'])}">{icon('x')}</button>
<nav aria-label="{E(S.UI['menu'])}">{sheet_nav}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='tabs')}
{wa('menu')}
{call('menu')}
</div></div>
<main id="main">'''


def hours_table():
    return (f'<table class="hrs"><tbody><tr><th>{E(S.UI["mon_fri"])}</th><td class="num">{E(S.UI["hours_mf"])}</td></tr>'
            f'<tr><th>{E(S.UI["sat"])}</th><td class="num">{E(S.UI["hours_sat"])}</td></tr>'
            f'<tr><th>{E(S.UI["sun"])}</th><td>{E(S.UI["closed"])}</td></tr></tbody></table>')


def footer():
    a = F['address']
    return f'''</main>
<footer class="ft"><div class="wrap">
<div class="ft-g">
<div>
<a class="ft-logo" href="{pu('')}" aria-label="JT Autoworks">{logo()}</a>
<address>{E(S.UI['legal'])}<br>8 Kaki Bukit Ave 4, {a['unit']}<br>{a['building']}, Singapore {a['postal']}<br>({a['gate']})</address>
<p>{E(S.UI['hours_short'])}</p>
</div>
<div><h2>{E(S.UI['contact_h'])}</h2><ul>
<li>{wa('footer', label='WhatsApp ' + F['whatsapp']['display'], cls='fl')}</li>
<li>{call('footer', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='fl')}</li>
<li>{mail('footer')}</li>
<li>{ext('facebook', 'footer', LK['facebook'], S.UI['facebook'])}</li>
<li>{ext('instagram', 'footer', LK['instagram'], S.UI['instagram'] + ' ' + LK['instagram_handle'])}</li>
</ul></div>
<div><h2>{E(S.UI['find_us'])}</h2><ul>
<li>{ext('map', 'footer', LK['maps'], S.UI['maps'])}</li>
<li>{ext('directions', 'footer', LK['directions'], S.UI['directions'])}</li>
<li>{ext('reviews', 'footer', LK['reviews'], S.UI['reviews'])}</li>
<li>{ext('review_write', 'footer', LK['write_review'], S.UI['write_review'])}</li>
<li><a href="{pu('areas/')}">{E(S.UI['areas'])}</a></li>
</ul></div>
</div>
<div class="ft-b"><span>&copy; 2026 {E(S.UI['legal'])}</span><a href="{pu('privacy/')}">{E(S.UI['privacy'])}</a><a href="https://autoseo.my/">Website by AutoSEO.my</a></div>
</div></footer>
<div class="mbar">{wa('mobile_bar')}{call('mobile_bar', label=S.UI['call_short'])}</div>
<script src="{u('assets/site.js')}?v={ver(os.path.join(HERE, 'assets', 'site.js'))}" defer></script>
<script src="{u('p1-cta.js')}?v={ver(os.path.join(HERE, 'p1-cta.js'))}" defer></script>
</body>
</html>
'''


# ---------- schema (one facts file) ----------
def org_ld():
    a = F['address']
    days = []
    for h in F['hours']:
        days.append({'@type': 'OpeningHoursSpecification', 'dayOfWeek': h['days'], 'opens': h['opens'], 'closes': h['closes']})
    d = {
        '@context': 'https://schema.org', '@type': 'AutoRepair', '@id': SITE + '#business',
        'name': F['legal_name'], 'alternateName': [F['name'], F['sign_name']],
        'description': S.SCHEMA['description'], 'url': pabs(''),
        'telephone': F['phone']['e164'], 'email': F['email'],
        'address': {'@type': 'PostalAddress', 'streetAddress': a['street'], 'addressLocality': a['locality'], 'postalCode': a['postal'], 'addressCountry': a['country']},
        'geo': {'@type': 'GeoCoordinates', 'latitude': F['geo']['lat'], 'longitude': F['geo']['lng']},
        'hasMap': LK['maps'],
        'openingHoursSpecification': days,
        'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'customer service', 'telephone': F['whatsapp']['e164'], 'url': F['whatsapp']['url'], 'availableLanguage': ['en', 'zh', 'ms']}],
        'sameAs': [LK['maps'], LK['cid'], LK['facebook'], LK['instagram']],
        'areaServed': [{'@type': 'Place', 'name': n} for n in F['area_names'].values()],
        'knowsAbout': ['Car diagnostics', 'Car aircon repair', 'Car battery replacement', 'EV servicing', 'Pre-purchase car inspection', 'European car repair'],
        'makesOffer': [{'@type': 'Offer', 'name': S.PKG['name'].replace('{L}', p['letter']), 'price': p['price'], 'priceCurrency': 'SGD',
                        'description': S.PKG['oil_line'].format(oil=p['oil'], litres=p['litres'])} for p in F['packages']['items']],
    }
    if has('og'):
        d['image'] = mabs('og')
    if has('logo'):
        d['logo'] = mabs('logo')
    return d


def crumb_ld(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': pabs(p)} for i, (p, n) in enumerate(trail)]}


def faq_ld(qs):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in qs]}


def crumb_html(trail):
    li = []
    for i, (p, n) in enumerate(trail):
        li.append(f'<li><a href="{pu(p)}"{" aria-current=\"page\"" if i == len(trail) - 1 else ""}>{E(n)}</a></li>')
    return f'<nav class="crumb" aria-label="{E(S.UI["breadcrumb"])}"><ol>{"".join(li)}</ol></nav>'


# ---------- shared blocks ----------
def img(stem, alt, cls=None, eager=False, sizes=None):
    """One <img> from the media manifest. Real photos use cover in CSS; designed posters always use contain (class poster-img)."""
    m = MEDIA[stem]
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager == 'high' else ('' if eager else ' loading="lazy"')
    return f'<img{c} src="{murl(stem)}" width="{m["w"]}" height="{m["h"]}" alt="{E(alt)}"{load} decoding="async">'


def poster_fig(stem, alt, cap=None, cls='poster'):
    if not has(stem):
        return ''
    fc = f'<figcaption>{E(cap)}</figcaption>' if cap else ''
    return f'<figure class="{cls}">{img(stem, alt)}{fc}</figure>'


def lap_block(photo, h, paras, link=None, cls='white', flip=False):
    """Overlapping photo-and-text block (shared template: autoseo-template/blocks/soft-cards). Photo = real photo only."""
    if not has(photo):
        return f'<section class="sec {cls}"><div class="wrap prose"><h2>{E(h)}</h2>{"".join(f"<p>{E(p)}</p>" for p in paras)}{link or ""}</div></section>'
    return f'''<section class="sec {cls}"><div class="wrap lap{' flip' if flip else ''}">
<figure class="lap-img">{img(photo, S.PHOTOS.get(photo, ''))}</figure>
<div class="lap-card"><h2>{E(h)}</h2>{''.join(f'<p>{E(p)}</p>' for p in paras)}{link or ''}</div>
</div></section>'''


def hero_block():
    """Full-bleed photo hero (shared template: autoseo-template/blocks/photo-hero): real photo behind a transparent header,
    white headline and WhatsApp on the photo, bottom fading into the next band."""
    H = S.HOME
    pic = ''
    if has('hero-tall'):
        wide = f'<source media="(min-width: 760px)" srcset="{murl("hero-wide")}" width="{MEDIA["hero-wide"]["w"]}" height="{MEDIA["hero-wide"]["h"]}">' if has('hero-wide') else ''
        pic = f'<picture class="hero-bg">{wide}{img("hero-tall", S.PHOTOS["hero"], eager="high")}</picture>'
    return f'''<section class="hero on-navy">{pic}<div class="wrap hero-in">
<p class="kicker">{E(S.LOOK['kicker'])}</p>
<h1>{E(H['h1'])}</h1><p class="hero-line">{E(H['line'])}</p>
<div class="hero-cta">{wa('home_hero', 'home')}{call('home_hero', label=S.UI['call_short'], cls='go-ghost')}</div>
</div></section>'''


def reel(topic, place, key=None, cap=None, with_wa=True, eager=False):
    """Video tile (shared template: autoseo-template/blocks/video-facade). Always shows the real 9:16 poster frame.
    Self-hosted MP4 when media has video-<topic>: <video poster=...>. Otherwise an <img> facade of the poster frame that swaps
    to the official Facebook embed on tap (no Facebook script before the tap). No poster frame = no tile (never an empty box)."""
    r = REEL_BY_TOPIC[topic]
    cap = cap or S.REELS[topic]
    thumb = f'reel-{r["id"]}'
    vid = f'video-{topic}'
    if not has(thumb) and not has(vid):
        return ''
    play = '<span class="vf-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.2v13.6L19 12z"/></svg></span>'
    if has(vid):
        m = MEDIA[vid]
        poster = f' poster="{murl(thumb)}"' if has(thumb) else ''
        box = (f'<div class="vf vf-own"><video muted playsinline loop preload="none"{poster} width="{m["w"]}" height="{m["h"]}" aria-label="{E(cap)}">'
               f'<source src="{murl(vid)}" type="video/mp4"></video><button class="vf-snd" type="button" aria-pressed="false">{E(S.UI["tap_sound"])}</button></div>')
    else:
        href = f'https://www.facebook.com/reel/{r["id"]}/'
        src = 'https://www.facebook.com/plugins/video.php?href=' + urllib.parse.quote(href, safe='') + '&show_text=false&width=360&height=640'
        box = (f'<div class="vf"><button class="vf-b" type="button" data-src="{E(src)}" aria-label="{E(S.UI["play"] + ": " + cap)}">'
               f'{img(thumb, "", eager=eager)}{play}<span class="vf-len num">{r["len"]}</span></button></div>')
    w = wa(place, key or f'reel_{topic}', label=S.UI['wa_short'], cls='wa-mini') if with_wa else ''
    return f'<figure class="reel">{box}<figcaption><span>{E(cap)}</span>{w}</figcaption></figure>'


def pkg_cards(place_prefix):
    """Package strip (shared template: autoseo-template/blocks/soft-cards): rounded card, real poster (contain), big price,
    WhatsApp button on every card. Swipe strip on phones, three columns on desktop."""
    out = []
    for p in F['packages']['items']:
        lines = []
        if p['flush_bundle']:
            lines.append(f'<li>{E(S.PKG["flush"])}</li>')
        if p['windshield']:
            lines.append(f'<li>{E(S.PKG["windshield"])}</li>')
        if not p['flush_bundle'] and not p['windshield']:
            lines.append(f'<li class="no">{E(S.PKG["no_flush"])}</li>')
        name = S.PKG['name'].replace('{L}', p['letter'])
        fig = f'<div class="pk-img">{img(p["poster"], S.PKG["poster_alt"].replace("{L}", p["letter"]))}</div>' if has(p['poster']) else ''
        out.append(f'''<li class="pk-c">{fig}<div class="pk-b">
<p class="pk-tag"><b>{p['letter']}</b>{E(name)}</p>
<h3 class="pk-oil">{E(S.PKG['oil_line'].format(oil=p['oil'], litres=p['litres']))}</h3>
<p class="pk-p num">${p['price']}<small>{E(S.UI['for3'])}</small></p>
<p class="pk-x num">{E(S.PKG['extra'].format(x=p['extra_per_litre']))}</p>
<ul>{''.join(lines)}</ul>
{wa(f"{place_prefix}_package_{p['id']}", f"pkg_{p['id']}", label=S.UI['pkg_wa'].replace('{L}', p['letter']))}
</div></li>''')
    return f'<ul class="pk">{"".join(out)}</ul>'


def inc_block():
    P = F['packages']
    items = ''.join(f'<li>{E(S.PKG["common"][k].format(n=n))}</li>' for k, n in P['common'])
    return (f'<div class="inc"><h3>{E(S.PKG["inc_h"])}</h3><ul class="ticks2">{items}</ul>'
            f'<p>{E(S.PKG["brake_fluid"])} {E(S.PKG["lifetime"])} {E(S.PKG["visc"].format(v=" / ".join(P["viscosities"])))}</p></div>')


def process_block():
    st = ''.join(f'<li><h3>{E(a)}</h3><p>{E(b)}</p></li>' for a, b in S.PROCESS['steps'])
    return f'''<section class="sec navy on-navy" id="process"><div class="wrap">
<div class="sec-h"><h2>{E(S.PROCESS['h2'])}</h2><p>{E(S.PROCESS['lead'])}</p></div>
<ol class="route rv">{st}</ol></div></section>'''


def proof_block(place):
    items = ''.join(f'<li><h3>{E(T(a))}</h3><p>{E(T(b))}</p></li>' for a, b in S.PROOF['items'])
    qs = ''.join(f'<figure class="q"><blockquote><p>{E(q)}</p></blockquote><figcaption>{E(S.LOOK["quote_src"])}</figcaption></figure>' for q in S.LOOK['quotes'])
    return f'''<section class="sec steel" id="proof"><div class="wrap">
<div class="sec-h"><h2>{E(S.PROOF['h2'])}</h2></div>
<ul class="pf">{items}</ul>
<h3 class="qs-h">{E(S.LOOK['quotes_h'])}</h3>
<div class="qs">{qs}</div>
<div class="pf-foot"><p>{E(S.PROOF['note'])}</p>{ext('reviews', place, LK['reviews'], S.UI['reviews'], cls='more')}</div>
</div></section>'''


def photo_rail():
    stems = [s for s in F['photos_real'] if has(s)]
    if len(stems) < 2:
        return ''
    figs = ''.join(f'<figure>{img(s, S.PHOTOS[s])}<figcaption>{E(S.PHOTOS[s])}</figcaption></figure>' for s in stems)
    dots = ''.join('<i></i>' for _ in stems)
    return f'''<section class="sec navy on-navy" id="photos"><div class="wrap">
<div class="sec-h"><h2>{E(S.PHOTOS['h2'])}</h2><p>{E(S.LOOK['gallery_lead'])}</p></div>
<div class="rail"><div class="rail-t">{figs}</div>
<div class="rail-c"><button type="button" class="arr" data-dir="-1" aria-label="{E(S.UI['prev'])}">{icon('prev')}</button><button type="button" class="arr" data-dir="1" aria-label="{E(S.UI['next'])}">{icon('next')}</button><span class="dots" aria-hidden="true">{dots}</span></div></div>
</div></section>'''


def way_sign():
    a = F['address']
    return f'''<div class="sign" role="img" aria-label="{E(a['building'] + ', ' + a['gate'] + ', ' + a['unit'])}">
<div><i>@</i><p style="margin:0"><b>{E(a['building'])}</b><span>8 Kaki Bukit Ave 4, Singapore {a['postal']}</span></p></div>
<div><i>1</i><p style="margin:0"><b>{E(a['gate'])}</b><span>{E(S.GATE['landmarks']['Gate 1'])}</span></p></div>
<div class="here"><i>02</i><p style="margin:0"><b>{a['unit']}</b><span>JT AUTOWORKS</span></p></div>
</div>'''


def faq_html(qs):
    return '<div class="faq">' + ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in qs) + '</div>'


def ask(place, key, h=None, line=None):
    return f'''<section class="ask on-navy"><div class="wrap">
<h2>{E(h or S.HOME['final_h'])}</h2><p>{E(line or S.HOME['final_line'])}</p>
<div class="btns">{wa(place + '_band', key)}{call(place + '_band')}</div></div></section>'''


def page_head(path, trail, h1, lead, key):
    return f'''<section class="ph on-navy"><div class="wrap">{crumb_html(trail)}
<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>
<div class="ph-cta">{wa(slug(path) + '_head', key)}{call(slug(path) + '_head', cls='go-ghost')}</div></div></section>'''


def slug(path):
    p = path.strip('/').split('/')[-1] if path else 'home'
    return {'': 'home', 'find-us': 'findus', 'pre-purchase-inspection': 'ppi', 'german-luxury-cars': 'german'}.get(p, p.replace('-', '_'))


# ---------- page bodies ----------
def home():
    H = S.HOME
    strip = ''.join(f'<li>{x}</li>' for x in (reel(t, 'home_reel_' + t, eager=True) for t in HOME_STRIP) if x)
    svcs = ''.join(f'<li><a href="{pu(SVC_PATH[k])}"><b>{E(S.SERVICES[k]["name"])}</b><span>{E(S.SERVICES[k]["card"])}</span><i class="go-i">{icon("go")}</i></a></li>' for k in strings_en.SERVICE_ORDER)
    oth = ''.join(f'<li><b>{E(a)}</b> <span>{E(b)}</span></li>' for a, b in S.OTHER_SERVICES['items'])
    poster = poster_fig('location-poster', S.GATE['poster_alt'])
    return f'''{hero_block()}
<section class="sec navy on-navy band-v" id="videos"><div class="wrap">
<div class="sec-h"><h2>{E(S.LOOK['reels_h'])}</h2><p>{E(S.LOOK['reels_lead'])}</p></div>
<ul class="reels">{strip}</ul>
<p class="sec-more">{ext('facebook', 'home_reels_more', LK['facebook_videos'], S.UI['watch_more'], cls='more')}</p>
</div></section>
<section class="sec paper" id="packages"><div class="wrap">
<div class="sec-h"><p class="eyebrow">{E(S.LOOK['pkg_kicker'])}</p><h2>{E(S.PKG['h2'])}</h2><p>{E(S.PKG['lead'])}</p></div>
{pkg_cards('home')}
{inc_block()}
<p class="sec-more"><a class="more" href="{pu('packages/')}">{E(S.UI['see_packages'])}</a></p>
</div></section>
{lap_block('mercedes-c-class-on-lift-4x5', H['intro_h'], [H['intro'], H['lounge']], f'<a class="more" href="{pu("about/")}">{E(S.LOOK["about_more"])}</a>')}
{process_block()}
{proof_block('home')}
<section class="sec white" id="services"><div class="wrap">
<div class="sec-h"><h2>{E(H['svc_h'])}</h2><p>{E(S.UI['all_makes'])}</p></div>
<ul class="svl">{svcs}</ul>
<ul class="oth">{oth}</ul>
<p class="sec-more"><a class="more" href="{pu('services/')}">{E(S.UI['see_services'])}</a></p>
</div></section>
{photo_rail()}
<section class="sec paper" id="gate1"><div class="wrap way">
<div><h2>{E(S.GATE['h2'])}</h2><p>{E(S.GATE['lead'])}</p>{way_sign()}
<div class="btns">{ext('directions', 'home_gate', LK['directions'], S.UI['directions'], cls='go-line', ic='nav')}<a class="more" href="{pu('find-us/')}">{E(S.UI['see_find'])}</a></div></div>
<div>{poster}<div class="hrs-card"><h3>{E(S.UI['hours_h'])}</h3>{hours_table()}</div></div>
</div></section>
<section class="sec white" id="faq"><div class="wrap"><h2>{E(S.UI['faq_h'])}</h2>{faq_html(H['faq'])}</div></section>
{ask('home', 'home')}'''


def packages_page(path):
    P = S.PACKAGES
    trail = [('', S.UI['home']), (path, S.UI['packages'])]
    chk = ''.join(f'<li>{E(S.CHECK_50[g])}</li>' for g in F['check_50_groups'])
    n50 = S.OTHER_SERVICES['items'][3][0]
    comb = poster_fig('package-all', S.PKG['combined_alt'], P['compare_h'], cls='poster poster-wide')
    p50 = poster_fig('poster-50', S.LOOK['poster_alt'].replace('{name}', n50))
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'packages')}
<section class="sec paper"><div class="wrap">{pkg_cards('packages')}{inc_block()}{comb}</div></section>
<section class="sec white"><div class="wrap two"><div><h2>{E(n50)}</h2><ul class="ticks2 cols">{chk}</ul>{p50}</div>
<div class="side"><h3>{E(S.UI['hours_h'])}</h3>{hours_table()}<div class="btns">{wa('packages_side', 'packages')}</div></div></div></section>
<section class="sec paper"><div class="wrap"><h2>{E(S.UI['faq_h'])}</h2>{faq_html(P['faq'])}</div></section>
{ask('packages', 'packages')}'''
    return body, [org_ld(), crumb_ld(trail), faq_ld(P['faq'])]


def services_page(path):
    P = S.SERVICES_PAGE
    trail = [('', S.UI['home']), (path, S.UI['services'])]
    svcs = ''.join(f'<li><a href="{pu(SVC_PATH[k])}"><b>{E(S.SERVICES[k]["name"])}</b><span>{E(S.SERVICES[k]["card"])}</span><i class="go-i">{icon("go")}</i></a></li>' for k in strings_en.SERVICE_ORDER)
    oth = ''.join(f'<li><b>{E(a)}</b> <span>{E(b)}</span></li>' for a, b in S.OTHER_SERVICES['items'])
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'services')}
<section class="sec paper"><div class="wrap"><ul class="svl">{svcs}</ul>
<h2 class="mt">{E(S.OTHER_SERVICES['h2'])}</h2><ul class="oth">{oth}</ul>
<p class="sec-more"><a class="more" href="{pu('packages/')}">{E(S.UI['see_packages'])}</a></p></div></section>
{process_block()}
{ask('services', 'services')}'''
    return body, [org_ld(), crumb_ld(trail)]


SVC_POSTER = {'ev': 'ev-graphic', 'ppi': 'poster-ppi', 'towing': 'poster-towing', 'german': 'poster-luxury'}


def service_page(k, path):
    V = S.SERVICES[k]
    trail = [('', S.UI['home']), ('services/', S.UI['services']), (path, V['name'])]
    key = k
    if k == 'german':
        lst = ''.join(f'<li>{E(m)}</li>' for m in F['makes'])
    else:
        lst = ''.join(f'<li>{E(x)}</li>' for x in V['list'])
    extra = f'<p class="note"><b>{E(S.UI["all_makes"])}</b></p>' if k == 'german' else ''
    poster = poster_fig(SVC_POSTER[k], S.LOOK['poster_alt'].replace('{name}', V['name'])) if k in SVC_POSTER else ''
    side_reel = ''
    if k in SVC_REEL:
        r = reel(SVC_REEL[k], 'service_' + slug(path) + '_reel', key)
        side_reel = f'<div class="svc-reel">{r}</div>' if r else ''
    links = f'<div class="btns"><a class="more" href="{pu("packages/")}">{E(S.UI["see_packages"])}</a><a class="more" href="{pu("find-us/")}">{E(S.UI["see_find"])}</a></div>'
    body = f'''{page_head(path, trail, V['h1'], V['lead'], key)}
<section class="sec paper"><div class="wrap two">
<div class="prose">{''.join(f'<p>{E(T(p))}</p>' for p in V['body'])}{links}{side_reel}</div>
<aside class="side"><h3>{E(V['list_h'])}</h3><ul class="ticks2">{lst}</ul>{extra}{poster}</aside>
</div></section>
{process_block()}
{ask('service_' + slug(path), key)}'''
    return body, [org_ld(), crumb_ld(trail)]


def find_page(path):
    P = S.FIND
    trail = [('', S.UI['home']), (path, S.UI['find_us'])]
    lm = ''.join(f'<li>{E(S.GATE["landmarks"][x])}</li>' for x in F['landmarks'])
    poster = poster_fig('location-poster', S.GATE['poster_alt'], S.GATE['poster_labels'])
    a = F['address']
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'find_us')}
<section class="sec paper"><div class="wrap way">
<div><h2>{E(S.UI['address_h'])}</h2><p>{E(a['display'])}</p>{way_sign()}
<div class="btns">{ext('directions', 'findus', LK['directions'], S.UI['directions'], cls='go-line', ic='nav')}{ext('map', 'findus', LK['maps'], S.UI['maps'], cls='go-line', ic='pin')}</div>
<p class="note">{E(S.GATE['lost'])}</p></div>
<div>{poster}</div>
</div>
<div class="wrap"><div class="map"><iframe src="{E(LK['map_embed_keyless'])}" title="{E(S.UI['map_title'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div>
</section>
<section class="sec white"><div class="wrap two">
<div><h2>{E(S.GATE['landmarks_h'])}</h2><ul class="ticks2">{lm}</ul></div>
<div class="side"><h3>{E(S.UI['hours_h'])}</h3>{hours_table()}
<div class="btns">{wa('findus', 'find_us')}{call('findus')}</div>
<div class="btns">{ext('reviews', 'findus', LK['reviews'], S.UI['reviews'], cls='more')}{ext('review_write', 'findus', LK['write_review'], S.UI['write_review'], cls='more')}</div></div>
</div></section>
{ask('findus', 'find_us')}'''
    return body, [org_ld(), crumb_ld(trail)]


def about_page(path):
    P = S.ABOUT
    trail = [('', S.UI['home']), (path, S.UI['about'])]
    vals = ''.join(f'<li><b>{E(a)}</b><span>{E(b)}</span></li>' for a, b in P['values'])
    body = f'''{page_head(path, trail, P['h1'], P['lead'], 'about')}
{lap_block('shopfront-corridor-tighter-4x5', P['h1'], [T(p) for p in P['body']] + [P['lounge']], cls='paper')}
<section class="sec white"><div class="wrap"><h2>{E(P['values_h'])}</h2><ul class="vals">{vals}</ul></div></section>
{photo_rail()}
{proof_block('about')}
{ask('about', 'about')}'''
    return body, [org_ld(), crumb_ld(trail)]


def areas_page(path):
    P = S.AREAS
    trail = [('', S.UI['home']), (path, S.UI['areas'])]
    jump = ''.join(f'<li><a href="#{a}">{E(F["area_names"][a])}</a></li>' for a in F['areas'])
    rows = []
    for a in F['areas']:
        n = F['area_names'][a]
        p = P['here_p'] if a == 'kaki-bukit' else P['area_p'].replace('{area}', n)
        rows.append(f'''<section class="area" id="{a}"><h2>{E(P['area_h'].replace('{area}', n))}</h2><p>{E(p)}</p>
<div class="area-links"><a class="more" href="{pu('packages/')}">{E(S.UI['packages'])}</a><a class="more" href="{pu('services/')}">{E(S.UI['services'])}</a><a class="more" href="{pu('find-us/')}">{E(S.UI['find_us'])}</a></div></section>''')
    body = f'''<section class="ph on-navy"><div class="wrap">{crumb_html(trail)}<h1>{E(P['h1'])}</h1><p class="lead">{E(P['lead'])}</p><ul class="jump">{jump}</ul></div></section>
<section class="sec paper"><div class="wrap prose">{''.join(rows)}</div></section>
{ask('areas', 'areas')}'''
    return body, [org_ld(), crumb_ld(trail)]


def articles_page(path):
    P = S.ARTICLES
    trail = [('', S.UI['home']), (path, S.UI['articles'])]
    body = f'''{page_head(path, trail, P['h1'], P['empty'], 'articles')}
<section class="sec paper"><div class="wrap"><p><a class="more" href="{pu('services/')}">{E(S.UI['see_services'])}</a></p></div></section>'''
    return body, [org_ld(), crumb_ld(trail)]


def privacy_page(path):
    P = S.PRIVACY
    trail = [('', S.UI['home']), (path, S.UI['privacy'])]
    rows = ''.join(f'<h2 style="font-size:1.3rem;margin-top:1.4em">{E(h)}</h2><p>{E(t)}</p>' for h, t in P['body'])
    body = f'''<section class="ph on-navy"><div class="wrap">{crumb_html(trail)}<h1>{E(P['h1'])}</h1></div></section>
<section class="sec paper"><div class="wrap prose">{rows}</div></section>'''
    return body, [org_ld(), crumb_ld(trail)]


def render(path):
    if path == '':
        H = S.HOME
        return head(path, H['title'], H['meta'], [org_ld(), faq_ld(H['faq'])]) + header(path) + home() + footer()
    if path == 'packages/':
        b, ld = packages_page(path); t, m = S.PACKAGES['title'], S.PACKAGES['meta']
    elif path == 'services/':
        b, ld = services_page(path); t, m = S.SERVICES_PAGE['title'], S.SERVICES_PAGE['meta']
    elif path.startswith('services/'):
        k = [x for x, p in SVC_PATH.items() if p == path][0]
        b, ld = service_page(k, path); t, m = S.SERVICES[k]['title'], S.SERVICES[k]['meta']
    elif path == 'find-us/':
        b, ld = find_page(path); t, m = S.FIND['title'], S.FIND['meta']
    elif path == 'about/':
        b, ld = about_page(path); t, m = S.ABOUT['title'], S.ABOUT['meta']
    elif path == 'areas/':
        b, ld = areas_page(path); t, m = S.AREAS['title'], S.AREAS['meta']
    elif path == 'articles/':
        b, ld = articles_page(path); t, m = S.ARTICLES['title'], S.ARTICLES['meta']
    elif path == 'privacy/':
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
        elif isinstance(a, str):
            if sorted(re.findall(r'\{\w+\}', a)) != sorted(re.findall(r'\{\w+\}', b)):
                raise SystemExit(f'placeholder mismatch at {at}')
    names = [n for n in dir(strings_en) if n.isupper()]
    for code in ('ms', 'zh'):
        for n in names:
            walk(getattr(strings_en, n), getattr(STRINGS[code], n), f'{code}.{n}')


def zh_font_subset():
    """Subset Noto Sans SC to the characters the 中文 pages use (source: assets/fonts-src/NotoSansSC[wght].ttf if present)."""
    src = os.path.join(HERE, 'assets', 'fonts-src', 'NotoSansSC.ttf')
    dst = os.path.join(HERE, 'assets', 'fonts', 'notosanssc-sub.woff2')
    if not os.path.exists(src):
        return
    text = set()
    for n in dir(strings_zh):
        if n.isupper():
            text |= set(repr(getattr(strings_zh, n)).encode().decode('unicode_escape', 'ignore') if False else str(getattr(strings_zh, n)))
    cjk = ''.join(sorted(c for c in text if ord(c) > 0x2E80))
    open(os.path.join(HERE, 'assets', 'fonts-src', 'zh-chars.txt'), 'w', encoding='utf8').write(cjk)
    import subprocess
    tmp = dst + '.ttf'
    subprocess.run(['pyftsubset', src, f'--text-file={os.path.join(HERE, "assets", "fonts-src", "zh-chars.txt")}', '--layout-features=*', f'--output-file={tmp}'], check=True)
    subprocess.run(['fonttools', 'varLib.instancer', tmp, 'wght=400:700', '-o', tmp + '2.ttf', '-q'], check=True)
    from fontTools.ttLib import TTFont
    f = TTFont(tmp + '2.ttf'); f.flavor = 'woff2'; f.save(dst)
    os.remove(tmp); os.remove(tmp + '2.ttf')


def main():
    global S, L
    check_keys()
    if '--fonts' in sys.argv:
        zh_font_subset()
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'), ignore=shutil.ignore_patterns('fonts-src'))
    shutil.copy(os.path.join(HERE, 'p1-cta.js'), os.path.join(OUT, 'p1-cta.js'))
    if os.path.isdir(MEDIA_DIR):
        shutil.copytree(MEDIA_DIR, os.path.join(OUT, 'media'), ignore=shutil.ignore_patterns('manifest.json', 'src'))
    built = set()
    for LL in I18N.LANGS:
        L, S = LL, STRINGS[LL['code']]
        for p in PAGES:
            sp = I18N.page_path(L, p)
            d = os.path.join(OUT, sp)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf8').write(render(p))
            built.add(sp)
    bad = I18N.check_twins(built)
    if bad:
        raise SystemExit('\n'.join(bad))
    open(os.path.join(OUT, 'sitemap.xml'), 'w', encoding='utf8').write(I18N.sitemap_xml(absu, PAGES, TODAY))
    L, S = I18N.LANGS[0], strings_en
    lines = [f'# {F["name"]}', '', f'> {S.LLMS["intro"]}', '',
             f'- Address: {F["address"]["display"]}', f'- WhatsApp: +65 {F["whatsapp"]["display"]} ({F["whatsapp"]["url"]})',
             f'- Phone (landline, call only): +65 {F["phone"]["display"]}', f'- Email: {F["email"]}',
             f'- Hours: {S.UI["hours_short"]}', f'- Google Maps: {LK["maps"]}', '', '## Service packages (3 services each)']
    for p in F['packages']['items']:
        lines.append(f'- Package {p["letter"]}: {p["oil"]} {p["litres"]}L, ${p["price"]}, extra oil ${p["extra_per_litre"]}/L')
    lines += ['', '## Pages']
    for LL in I18N.LANGS:
        for p in PAGES:
            lines.append(f'- [{LL["label"]}] {absu(I18N.page_path(LL, p))}')
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf8').write('\n'.join(lines) + '\n')
    print(f'built {len(built)} pages, media {len(MEDIA)}')


if __name__ == '__main__':
    main()
