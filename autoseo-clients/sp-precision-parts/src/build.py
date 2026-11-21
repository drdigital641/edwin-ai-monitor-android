#!/usr/bin/env python3
"""S & P Precision Parts (Monaer brake parts, Skudai) site builder. AutoSEO.my client, 21 Nov 2026.
EN at root, BM at /ms/, 中文 at /zh/. One template set for every page; facts in facts.json; copy in strings_en/ms/zh.py
(same keys, checked). ONE list GROUPS drives the product menu, hub, pages, footer, sitemap.xml and llms.txt.

ONE-SWITCH GO-LIVE: site.json is the only place a host lives (shared/golive.py). live_domain is empty for the preview.
Preview noindex is host-based (preview/.htaccess), so pages carry no robots meta.

Honesty gates (check.py): no prices, warranty, origin country, certificates or invented part numbers. The part list
(facts.json catalogue_samples) and the workshop list (facts.json workshops) hold only published / confirmed entries.

  python3 build.py [--fonts]  -> ../dist      python3 check.py -> pre-upload gate
Upload: Bridge sync_from_github, site autoseo, source autoseo-clients/sp-precision-parts/dist, base_path preview/sp-precision-parts."""
import hashlib, html, json, os, re, shutil, sys, urllib.parse, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'shared'))
sys.path.insert(0, HERE)
import autoseo_i18n as I18N
import golive as GL
import strings_en, strings_ms, strings_zh

STRINGS = {'en': strings_en, 'ms': strings_ms, 'zh': strings_zh}
S, L = strings_en, I18N.LANGS[0]
CFG = GL.load(os.path.join(HERE, 'site.json'))
F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
BASE = CFG.preview_path if not CFG.live else '/'


def _fill(v):
    # Phone lives ONLY in facts.json; strings carry {PHONE} / {PHONE_INTL} tokens.
    if isinstance(v, str):
        return v.replace('{PHONE}', F['phone']['display']).replace('{PHONE_INTL}', F['phone']['display_intl'])
    if isinstance(v, dict):
        return {k: _fill(x) for k, x in v.items()}
    if isinstance(v, list):
        return [_fill(x) for x in v]
    if isinstance(v, tuple):
        return tuple(_fill(x) for x in v)
    return v


for _m in STRINGS.values():
    for _k in [k for k in vars(_m) if k.isupper()]:
        setattr(_m, _k, _fill(getattr(_m, _k)))
OUT = os.path.join(HERE, '..', 'dist')
E = html.escape
LK = F['links']
NAME = F['name']
TODAY = '2026-11-21'
IMG = {'monaer-kit': (580, 440), 'monaer-pads': (430, 230), 'monaer-box': (310, 220), 'monaer-care': (270, 240), 'sp-banner': (1280, 753), 'sp-name-card': (1280, 731)}

# id, slug, photo
GROUPS = [('pads', 'brake-pads', 'monaer-pads'), ('discs', 'brake-discs', 'monaer-box'), ('care', 'brake-fluid-care', 'monaer-care')]
GP = {g[0]: {'slug': g[1], 'photo': g[2]} for g in GROUPS}


def gpath(g):
    return f"products/{GP[g]['slug']}/"


P_FINDER, P_LOC, P_JOIN = 'part-finder/', 'find-a-workshop/', 'become-authorised-workshop/'
PAGES = ['', 'products/'] + [gpath(g[0]) for g in GROUPS] + [P_FINDER, P_LOC, P_JOIN, 'faq/', 'contact/', 'articles/', 'privacy/']
NAV = [('products/', 'products'), (P_FINDER, 'finder'), (P_LOC, 'locator'), (P_JOIN, 'join'), ('faq/', 'faq'), ('contact/', 'contact')]


def u(p=''):
    return BASE + p


def pu(p=''):
    return u(I18N.page_path(L, p))


def canon(p=''):
    return CFG.canon(I18N.page_path(L, p))


def ver(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()[:8]


def wa_url(text):
    return f"{F['whatsapp']['url']}?text={urllib.parse.quote(text)}"


def icon(name):
    p = {
        'wa': '<path d="M4.6 19.4l1.1-3.5a7.9 7.9 0 1 1 2.9 2.7z"/><path d="M9.3 8.7c.3 2.5 2.3 4.7 5 5.2l.9-1.1 1.8.8-.3 1.5c-3.8.4-7.7-3.5-7.5-7.3l1.5-.3.8 1.7z"/>',
        'call': '<path d="M5.2 4h3.6l1.6 4-2.1 1.3a10.6 10.6 0 0 0 6.4 6.4l1.3-2.1 4 1.6v3.6a1.6 1.6 0 0 1-1.7 1.6C10.4 19.9 4.1 13.6 3.6 5.7A1.6 1.6 0 0 1 5.2 4z"/>',
        'pin': '<path d="M12 21s-6.4-5.5-6.4-10.9a6.4 6.4 0 0 1 12.8 0C18.4 15.5 12 21 12 21z"/><circle cx="12" cy="10.1" r="2.2"/>',
        'nav': '<path d="M20 4L3.5 10.6l7 2.6 2.6 7z"/>', 'mail': '<path d="M3.5 6h17v12h-17z"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
        'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>', 'x': '<path d="M6 6l12 12M18 6L6 18"/>',
        'go': '<path d="M5 12h13M13 6l6 6-6 6"/>', 'search': '<circle cx="10.5" cy="10.5" r="6"/><path d="M15 15l5 5"/>',
        'fb': '<path d="M14 8.5h2.5V5H14a3.5 3.5 0 0 0-3.5 3.5V11H8v3.5h2.5V21H14v-6.5h2.5L17 11h-3V8.5z"/>',
        'tick': '<path d="M5 12.5l4.5 4.5L19 7.5"/>', 'tool': '<path d="M14.5 5.5a4 4 0 0 0-5 5L4 16l4 4 5.500-5.5a4 4 0 0 0 5-5l-2.800 2.800-2.200-2.200z"/>',
        'car': '<path d="M4 16v-4l2-5h12l2 5v4"/><path d="M3 16h18v2H3z"/><circle cx="7.500" cy="14" r="1"/><circle cx="16.500" cy="14" r="1"/>',
    }[name]
    return f'<svg class="ic" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{p}</svg>'


def cta(kind, place, href, label, cls=None, ic=None, blank=True):
    c = f' class="{cls}"' if cls else ''
    t = ' target="_blank" rel="noopener"' if blank else ''
    return (f'<a{c} href="{E(href)}"{t} data-cta="{kind}_{place}" data-ref="{kind}_{place}">'
            f'{icon(ic) if ic else ""}<span>{E(label)}</span></a>')


def wa(place, text=None, label=None, cls='b-wa'):
    return cta('whatsapp', place, wa_url(text or S.PREFILL['default']), label or S.UI['wa_btn'], cls, 'wa')


def call(place, label=None, cls='b-call'):
    return cta('call', place, F['phone']['tel'], label or S.UI['call_btn'], cls, 'call', blank=False)


def pic(stem, eager=False, cls=None):
    w, h = IMG[stem]
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return (f'<picture><source type="image/webp" srcset="{u(f"media/{stem}.webp")}">'
            f'<img{c} src="{u(f"media/{stem}.jpg")}" width="{w}" height="{h}" alt="{E(S.ALT[stem])}"{load} decoding="async"></picture>')


def logo():
    return f'<img class="logo" src="{u("media/logo.webp")}" width="450" height="170" alt="Monaer 摩纳尔">'


def disc(cls='disc'):
    """The one drawn graphic: a drilled, slotted brake disc with the red Monaer dot. CSS turns it once and it stops."""
    holes = ''.join(f'<circle cx="{100 + 62 * __import__("math").cos(i * 0.5236):.1f}" cy="{100 + 62 * __import__("math").sin(i * 0.5236):.1f}" r="3.2"/>' for i in range(12))
    slots = ''.join(f'<path d="M100 100m0-84a84 84 0 0 1 30 6" transform="rotate({i * 60} 100 100)"/>' for i in range(6))
    lugs = ''.join(f'<circle cx="{100 + 20 * __import__("math").cos(i * 1.2566):.1f}" cy="{100 + 20 * __import__("math").sin(i * 1.2566):.1f}" r="3.6"/>' for i in range(5))
    return (f'<svg class="{cls}" viewBox="0 0 200 200" role="img" aria-label="{E(S.HOME["stop_label"])}"><g class="disc-spin">'
            f'<circle cx="100" cy="100" r="96" class="d-face"/><circle cx="100" cy="100" r="96" class="d-rim"/><g class="d-slot">{slots}</g><g class="d-hole">{holes}</g>'
            f'<circle cx="100" cy="100" r="38" class="d-hat"/><g class="d-lug">{lugs}</g><circle cx="100" cy="100" r="9" class="d-dot"/></g>'
            '<path class="d-cal" d="M150 28a96 96 0 0 1 38 44l-22 12a70 70 0 0 0-28-34z"/></svg>')


def head(path, title, meta, ld):
    css = os.path.join(HERE, 'assets', 'site.css')
    zh = L['code'] == 'zh'
    font = f'<link rel="preload" href="{u("assets/fonts/saira-700.woff2")}" as="font" type="font/woff2" crossorigin>'
    font += f'<link rel="preload" href="{u("assets/fonts/notosanssc-700.woff2" if zh else "assets/fonts/publicsans.woff2")}" as="font" type="font/woff2" crossorigin>'
    hero = f'<link rel="preload" as="image" type="image/webp" href="{u("media/monaer-kit.webp")}" fetchpriority="high">' if path == '' else ''
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
<meta property="og:image:alt" content="{E(S.ALT['monaer-kit'])}">
{I18N.og_locale_tags(L)}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(meta)}">
<meta name="twitter:image:alt" content="{E(S.ALT['monaer-kit'])}">
<meta name="theme-color" content="#0E1A22">
<link rel="icon" href="{u('media/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="icon" href="{u('media/icon-192.png')}" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="{u('media/apple-touch-icon.png')}">
{font}{hero}
<link rel="stylesheet" href="{u('assets/site.css')}?v={ver(css)}">
{ldj}
</head>'''


def header(path):
    def cur(p):
        return ' aria-current="page"' if path == p or (p == 'products/' and path.startswith('products/')) else ''
    nav = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in NAV)
    sheet = ''.join(f'<a href="{pu(p)}"{cur(p)}>{E(S.UI[k])}</a>' for p, k in [('', 'home')] + NAV)
    return f'''<body class="lang-{L['code']}{' is-home' if path == '' else ''}">
<a class="skip" href="#main">{E(S.UI['skip'])}</a>
<header class="top"><div class="wrap top-in">
<a class="brand" href="{pu('')}" aria-label="{E(NAME)}">{logo()}</a>
<nav class="topnav" aria-label="{E(S.UI['menu'])}">{nav}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='langs')}
<button class="burger" type="button" aria-expanded="false" aria-controls="sheet" aria-label="{E(S.UI['menu'])}">{icon('menu')}</button>
</div></header>
<div class="sheet" id="sheet" hidden><div class="sheet-in" role="dialog" aria-modal="true" aria-label="{E(S.UI['menu'])}">
<div class="sheet-top">{logo()}<button class="sheet-x" type="button" aria-label="{E(S.UI['close'])}">{icon('x')}</button></div>
<nav class="sheet-nav" aria-label="{E(S.UI['menu'])}">{sheet}</nav>
{I18N.switcher(u, path, L, S.UI['lang'], cls='langs')}
<div class="sheet-cta">{wa('menu')}{call('menu')}</div>
</div></div>
<main id="main">'''


def footer():
    a = F['address']
    prod = ''.join(f'<li><a href="{pu(gpath(g[0]))}">{E(S.PG[g[0]]["name"])}</a></li>' for g in GROUPS)
    nav = ''.join(f'<li><a href="{pu(p)}">{E(S.UI[k])}</a></li>' for p, k in NAV[1:] + [('articles/', 'articles')])
    return f'''</main>
<footer class="foot"><div class="wrap">
<div class="foot-g">
<div class="foot-id"><a class="brand" href="{pu('')}" aria-label="{E(NAME)}">{logo()}</a>
<p class="foot-n">{E(F['legal_name'])}</p><p class="foot-tag">{E(S.UI['tagline'])}</p>
<address>{'<br>'.join(E(x) for x in a['lines'])}</address>
<p class="foot-co">{E(S.UI['company'])} {E(F['company_no'])}</p></div>
<div><h2>{E(S.UI['contact_h'])}</h2><ul class="foot-l">
<li>{wa('footer', label='WhatsApp ' + F['phone']['display'], cls='fl')}</li>
<li>{call('footer', label=S.UI['call_short'] + ' ' + F['phone']['display'], cls='fl')}</li>
<li>{cta('email', 'footer', 'mailto:' + F['email'], F['email'], 'fl', 'mail', blank=False)}</li>
<li>{cta('map', 'footer', LK['maps'], S.UI['maps'], 'fl', 'pin')}</li>
<li>{cta('facebook', 'footer', LK['facebook'], S.UI['facebook'], 'fl', 'fb')}</li>
</ul></div>
<div><h2>{E(S.UI['products'])}</h2><ul class="foot-p">{prod}</ul><ul class="foot-p">{nav}</ul></div>
</div>
<p class="foot-safe">{E(S.UI['safety'])}</p>
<div class="foot-b"><span>&copy; 2026 {E(F['legal_name'])}</span><a href="{pu('privacy/')}">{E(S.UI['privacy'])}</a><a href="https://autoseo.my/">Website by AutoSEO.my</a></div>
</div></footer>
<div class="dock">{wa('mobile_bar', label=S.UI['wa_short'])}{call('mobile_bar', label=S.UI['call_short'])}</div>
<script src="{u('assets/site.js')}?v={ver(os.path.join(HERE, 'assets', 'site.js'))}" defer></script>
<script src="{u('p1-cta.js')}?v={ver(os.path.join(HERE, 'p1-cta.js'))}" defer></script>
</body>
</html>
'''


# ---------- schema (no rating, no review, no price, no hours: none confirmed) ----------
def org_ld():
    a = F['address']
    return {'@context': 'https://schema.org', '@type': 'AutoPartsStore', '@id': GL.jsonld_id(CFG), 'name': NAME, 'legalName': F['legal_name'],
            'description': S.LLMS['intro'], 'url': canon(''), 'inLanguage': L['hreflang'], 'telephone': F['phone']['e164'], 'email': F['email'],
            'image': CFG.og_image(), 'slogan': F['tagline'],
            'address': {'@type': 'PostalAddress', 'streetAddress': a['street'] + ', ' + a['area'], 'addressLocality': a['city'], 'postalCode': a['postcode'],
                        'addressRegion': a['region'], 'addressCountry': a['country']},
            'hasMap': LK['maps'], 'brand': {'@type': 'Brand', 'name': F['brand'], 'alternateName': F['brand_zh']},
            'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'sales', 'telephone': F['phone']['e164'], 'url': F['whatsapp']['url'], 'availableLanguage': ['en', 'ms', 'zh']}],
            'areaServed': [{'@type': 'State', 'name': 'Johor'}, {'@type': 'Country', 'name': 'Malaysia'}]}


def site_ld():
    return {'@context': 'https://schema.org', '@type': 'WebSite', '@id': GL.jsonld_id(CFG, 'website'), 'name': NAME, 'url': canon(''),
            'inLanguage': L['hreflang'], 'publisher': {'@id': GL.jsonld_id(CFG)}}


def crumb_ld(trail):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': canon(p)} for i, (p, n) in enumerate(trail)]}


def faq_ld(items):
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def product_ld(g, path):
    d = S.PG[g]
    return {'@context': 'https://schema.org', '@type': 'Product', 'name': f"{F['brand']} {d['name']}", 'description': d['meta'], 'url': canon(path),
            'image': CFG.share_base + f"media/{GP[g]['photo']}.jpg" if hasattr(CFG, 'share_base') else CFG.og_image(),
            'brand': {'@type': 'Brand', 'name': F['brand']}, 'category': d['name']}


# ---------- shared blocks ----------
def crumb_html(trail):
    li = ''.join(f'<li><a href="{pu(p)}"{" aria-current=\"page\"" if i == len(trail) - 1 else ""}>{E(n)}</a></li>' for i, (p, n) in enumerate(trail))
    return f'<nav class="crumb" aria-label="{E(S.UI["breadcrumb"])}"><ol>{li}</ol></nav>'


def qa(items):
    return '<div class="qa">' + ''.join(f'<details><summary><span>{E(q)}</span><i aria-hidden="true"></i></summary><p>{E(a)}</p></details>' for q, a in items) + '</div>'


def faq_band(items, tone='steel'):
    return f'<section class="band {tone}"><div class="wrap narrow"><h2>{E(S.UI["faq_h"])}</h2>{qa(items)}</div></section>'


def steps():
    st = ''.join(f'<li><span class="n" aria-hidden="true">{i + 1}</span><div><h3>{E(h)}</h3><p>{E(p)}</p></div></li>' for i, (h, p) in enumerate(S.UI['steps']))
    return f'<section class="band ink"><div class="wrap"><h2>{E(S.UI["steps_h"])}</h2><ol class="steps">{st}</ol><div class="btns">{wa("steps")}</div></div></section>'


def page_head(trail, h1, lead, btns, photo=None):
    ph = f'<figure class="ph-ph">{pic(photo, eager=True)}</figure>' if photo else f'<div class="ph-disc" aria-hidden="true">{disc("disc still")}</div>'
    return f'''<section class="ph"><div class="wrap ph-g"><div class="ph-t">{crumb_html(trail)}<h1>{E(h1)}</h1><p class="lead">{E(lead)}</p>
<div class="btns">{btns}</div></div>{ph}</div></section>'''


def field(name, label, kind='text', opts=None, ph='', req=False, im=None):
    r = ' required' if req else ''
    if opts is not None:
        o = f'<option value="">{E(S.FINDER["choose"])}</option>' + ''.join(f'<option>{E(x)}</option>' for x in opts)
        return f'<label class="fld"><span>{E(label)}</span><select name="{name}"{r}>{o}</select></label>'
    if kind == 'area':
        return f'<label class="fld wide"><span>{E(label)}</span><textarea name="{name}" rows="2"></textarea></label>'
    m = f' inputmode="{im}"' if im else ''
    return f'<label class="fld"><span>{E(label)}</span><input type="{kind}" name="{name}" placeholder="{E(ph)}"{m}{r} autocomplete="off"></label>'


def finder_form(place):
    P, X = S.FINDER, S.PREFILL
    labels = {'make': X['f_make'], 'model': X['f_model'], 'year': X['f_year'], 'axle': X['f_axle'], 'part': X['f_part']}
    return f'''<form class="wa-form" data-wa="{E(F['whatsapp']['url'])}" data-intro="{E(X['f_intro'])}" data-labels="{E(json.dumps(labels, ensure_ascii=False))}" data-cta="whatsapp_{place}_form" data-ref="whatsapp_{place}_form">
{field('make', P['f_make'], opts=F['makes'], req=True)}{field('model', P['f_model'], ph=P['f_model_ph'], req=True)}
{field('year', P['f_year'], ph=P['f_year_ph'], im='numeric')}{field('axle', P['f_axle'], opts=P['f_axle_opts'])}
{field('part', P['f_part'])}
<button type="submit" class="b-wa">{icon('wa')}<span>{E(P['f_send'])}</span></button>
<p class="fine">{E(S.UI['opens_wa'])} {E(S.UI['privacy_line'])}</p></form>'''


def join_form(place):
    P, X = S.JOIN, S.PREFILL
    labels = {'name': X['j_name'], 'person': X['j_person'], 'town': X['j_town'], 'state': X['j_state'], 'phone': X['j_phone'], 'bays': X['j_bays'], 'note': X['j_note']}
    return f'''<form class="wa-form" data-wa="{E(F['whatsapp']['url'])}" data-intro="{E(X['j_intro'])}" data-labels="{E(json.dumps(labels, ensure_ascii=False))}" data-cta="whatsapp_{place}_form" data-ref="whatsapp_{place}_form">
{field('name', P['f_name'], req=True)}{field('person', P['f_person'], req=True)}
{field('town', P['f_town'], req=True)}{field('state', P['f_state'], opts=F['states'], req=True)}
{field('phone', P['f_phone'], kind='tel', im='tel')}{field('bays', P['f_bays'], opts=P['f_bays_opts'])}
{field('note', P['f_note'], kind='area')}
<button type="submit" class="b-wa">{icon('wa')}<span>{E(P['f_send'])}</span></button>
<p class="fine">{E(S.UI['opens_wa'])} {E(S.UI['privacy_line'])}</p></form>'''


def part_rows():
    P = S.FINDER
    rows = ''
    for c in F['catalogue_samples']:
        fits = ''.join(f'<li>{E(x)}</li>' for x in c['fits'])
        txt = S.PREFILL['pads'] + c['m']
        rows += f'''<li class="part" data-q="{E((c['m'] + ' ' + ' '.join(c['fits'])).lower())}">
<div class="part-no"><b>{E(c['m'])}</b><span>{E(P['type_pad'])}</span><small>{E(P['pack_4'])}</small></div>
<div class="part-fit"><h3>{E(P['cols'][2])}</h3><ul>{fits}</ul></div>
{wa('finder_part', txt, S.UI['wa_short'], 'b-wa sm')}</li>'''
    return rows


def finder_block(place, with_list=True):
    P = S.FINDER
    lst = ''
    if with_list:
        lst = f'''<div class="lookup"><label class="search"><span class="vh">{E(P['search_label'])}</span>{icon('search')}<input type="search" id="part-q" placeholder="{E(P['search_ph'])}" aria-label="{E(P['search_label'])}" autocomplete="off"></label>
<p class="tag">{E(S.UI['sample'])}</p><ul class="parts" id="parts">{part_rows()}</ul>
<p class="none" id="part-none" hidden>{E(P['none'])} {wa('finder_none', label=S.UI['wa_short'], cls='b-wa sm')}</p>
<p class="fine">{E(P['list_note'])}</p></div>'''
    return lst + f'<div class="send-card"><h3>{E(P["form_h"])}</h3><p>{E(P["form_p"])}</p>{finder_form(place)}</div>'


def workshop_cards():
    """Only confirmed authorised workshops from facts.json. The distributor's own counter is always the first card."""
    R = S.LOCATOR
    a = F['address']
    me = f'''<li class="ws" data-state="Johor"><div><span class="ws-tag">{E(R['dist_tag'])}</span><h3>{E(F['legal_name'])}</h3>
<address>{E(a['one_line'])}</address><p>{E(R['dist_line'])}</p></div>
<div class="ws-b">{wa('locator_distributor', S.PREFILL['locator'], R['card_wa'], 'b-wa sm')}{call('locator_distributor', R['card_call'], 'b-call sm')}{cta('map', 'locator_distributor', LK['maps'], R['card_map'], 'chip', 'pin')}</div></li>'''
    rest = ''
    for i, w in enumerate(F['workshops']):
        rest += f'''<li class="ws" data-state="{E(w['state'])}"><div><h3>{E(w['name'])}</h3><address>{E(w['address'])}</address></div>
<div class="ws-b">{cta('call', f'locator_ws{i}', 'tel:' + w['tel'], R['card_call'], 'b-call sm', 'call', blank=False)}{cta('map', f'locator_ws{i}', w['maps'], R['card_map'], 'chip', 'pin')}</div></li>'''
    return me + rest


def locator_block(place, tag='p'):
    R = S.LOCATOR
    chips = f'<button type="button" class="st on" data-state="">{E(R["all"])}</button>' + ''.join(f'<button type="button" class="st" data-state="{E(s)}">{E(s)}</button>' for s in F['states'])
    return f'''<div class="loc"><{tag} class="loc-h">{E(R["state_h"])}</{tag}><div class="states" role="group" aria-label="{E(R['state_h'])}">{chips}</div>
<ul class="wss" id="wss">{workshop_cards()}</ul>
<div class="loc-empty" id="ws-none"><h3>{E(R['empty_h'])}</h3><p>{E(R['empty_p'])}</p>
<div class="btns">{wa(place + '_ask', S.PREFILL['locator'], R['ask_btn'])}</div></div></div>'''


def join_teaser(place):
    R = S.LOCATOR
    return f'''<section class="band blue"><div class="wrap join-t"><div><h2>{E(R['own_h'])}</h2><p>{E(R['own_p'])}</p></div>
<a class="b-solid" href="{pu(P_JOIN)}" data-cta="join_{place}" data-ref="join_{place}"><span>{E(S.UI['join_btn'])}</span>{icon('go')}</a></div></section>'''


# ---------- pages ----------
def home():
    H = S.HOME
    hero = f'''<section class="hero"><div class="hero-ph">{pic('monaer-kit', eager=True)}</div>
<div class="hero-disc" aria-hidden="true">{disc()}</div>
<div class="wrap hero-in"><h1>{E(H['h1'])}</h1><p class="hero-l">{E(H['line'])}</p>
<div class="btns">{wa('home_hero')}<a class="b-ghost" href="{pu(P_LOC)}" data-cta="locator_home_hero" data-ref="locator_home_hero">{icon('pin')}<span>{E(S.UI['locator_btn'])}</span></a></div>
</div></section>'''
    two = ''
    for (h, p, k), ic in zip(H['two'], ('car', 'tool')):
        href, lab = (pu(P_FINDER), S.UI['finder_btn']) if k == 'finder' else (pu(P_JOIN), S.UI['join_btn'])
        two += f'<li class="door door-{k}"><span class="door-ic">{icon(ic)}</span><h3>{E(h)}</h3><p>{E(p)}</p><a class="more" href="{href}" data-cta="{k}_home_doors" data-ref="{k}_home_doors"><span>{E(lab)}</span>{icon("go")}</a></li>'
    doors = f'<section class="band steel lift"><div class="wrap"><h2>{E(H["two_h"])}</h2><ul class="doors">{two}</ul></div></section>'
    why = ''.join(f'<li><h3>{E(h)}</h3><p>{E(p)}</p></li>' for h, p in H['why'])
    feel = ''.join(f'<li>{icon("tick")}<span>{E(x)}</span></li>' for x in H['feel'])
    whyb = f'''<section class="band ink lift"><div class="wrap"><h2>{E(H['why_h'])}</h2><p class="sub">{E(H['why_p'])}</p>
<ul class="why">{why}</ul>
<div class="feel"><figure>{pic('monaer-pads')}</figure><div><h3>{E(H['feel_h'])}</h3><ul class="ticks">{feel}</ul><p class="fine">{E(H['feel_note'])}</p></div></div>
</div></section>'''
    c = H['compare_cols']
    rows = ''.join(f'<tr><th scope="row">{E(a)}</th><td class="us">{E(b)}</td><td>{E(d)}</td></tr>' for a, b, d in H['compare_rows'])
    comp = f'''<section class="band steel lift"><div class="wrap narrow"><h2>{E(H['compare_h'])}</h2><p class="sub">{E(H['compare_p'])}</p>
<div class="cmp"><table><thead><tr><td></td><th scope="col" class="us">{E(c[1])}</th><th scope="col">{E(c[2])}</th></tr></thead><tbody>{rows}</tbody></table></div></div></section>'''
    cards = ''.join(f'''<li class="pc"><a href="{pu(gpath(g))}"><figure>{pic(GP[g]['photo'])}</figure><h3>{E(S.PG[g]['name'])}</h3><p>{E(S.PG[g]['line'])}</p><span class="more"><span>{E(S.UI['see_more'])}</span>{icon('go')}</span></a></li>''' for g in GP)
    rng = f'<section class="band paper lift"><div class="wrap"><h2>{E(H["range_h"])}</h2><ul class="pcs">{cards}</ul></div></section>'
    fnd = f'''<section class="band steel lift" id="finder"><div class="wrap"><h2>{E(H['finder_h'])}</h2><p class="sub">{E(H['finder_p'])}</p>
<div class="finder-g">{finder_block('home_finder')}</div>
<p class="more-row"><a class="more" href="{pu(P_FINDER)}"><span>{E(S.UI['finder_btn'])}</span>{icon('go')}</a></p></div></section>'''
    loc = f'''<section class="band paper lift"><div class="wrap"><h2>{E(H['locator_h'])}</h2><p class="sub">{E(H['locator_p'])}</p>{locator_block('home_locator')}</div></section>'''
    return hero + doors + whyb + rng + fnd + comp + loc + join_teaser('home') + steps() + faq_band(H['faq'])


def products_page(path):
    P = S.PRODUCTS
    trail = [('', S.UI['home']), (path, S.UI['products'])]
    secs = ''
    for i, (g, _, photo) in enumerate(GROUPS):
        d = S.PG[g]
        pts = ''.join(f'<li>{icon("tick")}<span>{E(x)}</span></li>' for x in d['points'][:4])
        secs += f'''<article class="row{' flip' if i % 2 else ''}"><figure>{pic(photo)}</figure><div><h2>{E(d['name'])}</h2><p>{E(d['line'])}</p><ul class="ticks">{pts}</ul>
<div class="btns">{wa('product_' + g, S.PREFILL[g])}<a class="more" href="{pu(gpath(g))}"><span>{E(S.UI['see_more'])}</span>{icon('go')}</a></div></div></article>'''
    body = (page_head(trail, P['h1'], P['lead'], wa('products'), 'monaer-kit') + f'<section class="band paper"><div class="wrap">{secs}<p class="fine">{E(S.UI["maker_note"])}</p></div></section>' +
            steps() + join_teaser('products'))
    return body, [org_ld(), crumb_ld(trail)]


def group_page(g):
    path = gpath(g)
    d = S.PG[g]
    trail = [('', S.UI['home']), ('products/', S.UI['products']), (path, d['name'])]
    pts = ''.join(f'<li>{icon("tick")}<span>{E(x)}</span></li>' for x in d['points'])
    bod = ''.join(f'<li>{E(x)}</li>' for x in d['body'])
    others = ''.join(f'<li><a class="chip" href="{pu(gpath(o))}">{E(S.PG[o]["name"])}</a></li>' for o in GP if o != g)
    extra = f'<section class="band steel"><div class="wrap"><h2>{E(S.HOME["finder_h"])}</h2><div class="finder-g">{finder_block("product_" + g)}</div></div></section>' if g != 'care' else ''
    body = (page_head(trail, d['h1'], d['lead'], wa('product_' + g, S.PREFILL[g]) + call('product_' + g, cls='b-ghost'), GP[g]['photo']) +
            f'''<section class="band paper"><div class="wrap two"><div><h2>{E(d['name'])}</h2><ul class="ticks big">{pts}</ul><p class="fine">{E(S.UI['maker_note'])}</p></div>
<div class="note-card"><h2>{E(d['body_h'])}</h2><ul class="dots">{bod}</ul><p class="fine">{E(S.UI['safety'])}</p><div class="btns">{wa('product_' + g + '_signs', S.PREFILL[g], S.UI['wa_short'], 'b-wa sm')}</div></div></div></section>''' +
            extra + steps() + f'<section class="band steel"><div class="wrap narrow"><h2>{E(S.UI["faq_h"])}</h2>{qa(d["faqs"])}<ul class="others">{others}</ul></div></section>' + join_teaser('product_' + g))
    return body, [org_ld(), product_ld(g, path), crumb_ld(trail), faq_ld(d['faqs'])]


def finder_page(path):
    P = S.FINDER
    trail = [('', S.UI['home']), (path, S.UI['finder'])]
    rd = ''.join(f'<li><h3>{E(h)}</h3><p>{E(p)}</p></li>' for h, p in P['read'])
    body = (page_head(trail, P['h1'], P['lead'], wa('finder')) +
            f'<section class="band steel"><div class="wrap"><h2>{E(P["search_h"])}</h2><div class="finder-g">{finder_block("finder")}</div><p class="fine">{E(S.UI["safety"])}</p></div></section>' +
            f'<section class="band paper"><div class="wrap two"><div><h2>{E(P["read_h"])}</h2><ul class="read">{rd}</ul></div><figure class="read-ph">{pic("monaer-pads")}</figure></div></section>' +
            steps() + faq_band(P['faqs']))
    return body, [org_ld(), crumb_ld(trail), faq_ld(P['faqs'])]


def locator_page(path):
    R = S.LOCATOR
    trail = [('', S.UI['home']), (path, S.UI['locator'])]
    body = (page_head(trail, R['h1'], R['lead'], wa('locator', S.PREFILL['locator'], R['ask_btn'])) +
            f'<section class="band paper"><div class="wrap">{locator_block("locator", "h2")}</div></section>' + join_teaser('locator') + faq_band(R['faqs']))
    return body, [org_ld(), crumb_ld(trail), faq_ld(R['faqs'])]


def join_page(path):
    J = S.JOIN
    trail = [('', S.UI['home']), (path, S.UI['join'])]
    get = ''.join(f'<li><span class="n" aria-hidden="true">{icon("tick")}</span><div><h3>{E(h)}</h3><p>{E(p)}</p></div></li>' for h, p in J['get'])
    body = (page_head(trail, J['h1'], J['lead'], f'<a class="b-wa" href="#apply">{icon("go")}<span>{E(S.UI["join_btn"])}</span></a>' + call('join', cls='b-ghost'), 'monaer-kit') +
            f'''<section class="band paper"><div class="wrap two"><div><h2>{E(J['get_h'])}</h2><ul class="get">{get}</ul></div>
<div class="send-card" id="apply"><h2>{E(J['form_h'])}</h2><p>{E(J['form_p'])}</p>{join_form('join')}</div></div></section>''' + faq_band(J['faqs']))
    return body, [org_ld(), crumb_ld(trail), faq_ld(J['faqs'])]


def faq_page(path):
    Q = S.FAQ_PAGE
    trail = [('', S.UI['home']), (path, S.UI['faq'])]
    body = page_head(trail, Q['h1'], Q['lead'], wa('faq', S.PREFILL['contact'], S.UI['wa_short'])) + f'<section class="band paper"><div class="wrap narrow">{qa(Q["items"])}<p class="fine">{E(S.UI["maker_note"])}</p></div></section>' + steps()
    return body, [org_ld(), crumb_ld(trail), faq_ld(Q['items'])]


def contact_page(path):
    C = S.CONTACT
    a = F['address']
    trail = [('', S.UI['home']), (path, S.UI['contact'])]
    body = page_head(trail, C['h1'], C['lead'], wa('contact', S.PREFILL['contact'], 'WhatsApp ' + F['phone']['display']) + call('contact', cls='b-ghost'), 'sp-name-card') + f'''<section class="band paper"><div class="wrap two">
<div class="note-card"><h2>{E(S.UI['address_h'])}</h2><address>{E(F['legal_name'])}<br>{'<br>'.join(E(x) for x in a['lines'])}<br>Malaysia</address>
<p class="fine">{E(S.UI['company'])} {E(F['company_no'])}</p>
<div class="chips">{cta('map', 'contact', LK['maps'], S.UI['maps'], 'chip', 'pin')}{cta('waze', 'contact', LK['waze'], S.UI['waze'], 'chip', 'nav')}
{cta('email', 'contact', 'mailto:' + F['email'], S.UI['email'], 'chip', 'mail', blank=False)}{cta('facebook', 'contact', LK['facebook'], S.UI['facebook'], 'chip', 'fb')}</div></div>
<div class="map"><iframe src="{E(LK['maps_embed'])}" title="{E(S.UI['maps'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
</div></section>
<section class="band ink"><div class="wrap narrow"><h2>{E(C['about_h'])}</h2><p class="about">{E(C['about_p'])}</p></div></section>''' + join_teaser('contact')
    return body, [org_ld(), crumb_ld(trail)]


def articles_page(path):
    A = S.ARTICLES
    trail = [('', S.UI['home']), (path, S.UI['articles'])]
    body = page_head(trail, A['h1'], A['empty'], wa('articles')) + '<section class="band paper"><div class="wrap"><ul class="art-list"></ul></div></section>'
    return body, [org_ld(), crumb_ld(trail)]


def privacy_page(path):
    P = S.PRIVACY
    trail = [('', S.UI['home']), (path, S.UI['privacy'])]
    rows = ''.join(f'<h2>{E(h)}</h2><p>{E(t)}</p>' for h, t in P['body'])
    body = page_head(trail, P['h1'], P['lead'], wa('privacy', S.PREFILL['contact'], S.UI['wa_short'])) + f'<section class="band paper"><div class="wrap narrow prose">{rows}</div></section>'
    return body, [org_ld(), crumb_ld(trail)]


def render(path):
    if path == '':
        H = S.HOME
        return head(path, H['title'], H['meta'], [org_ld(), site_ld(), faq_ld(H['faq'])]) + header(path) + home() + footer()
    if path.startswith('products/') and path != 'products/':
        g = next(x for x in GP if gpath(x) == path)
        b, ld = group_page(g)
        D = S.PG[g]
    else:
        fn, D = {'products/': (products_page, S.PRODUCTS), P_FINDER: (finder_page, S.FINDER), P_LOC: (locator_page, S.LOCATOR), P_JOIN: (join_page, S.JOIN),
                 'faq/': (faq_page, S.FAQ_PAGE), 'contact/': (contact_page, S.CONTACT), 'articles/': (articles_page, S.ARTICLES), 'privacy/': (privacy_page, S.PRIVACY)}[path]
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
        elif isinstance(a, (list, tuple)):
            if len(a) != len(b):
                raise SystemExit(f'strings length mismatch at {at}')
            for i, (x, y) in enumerate(zip(a, b)):
                walk(x, y, f'{at}[{i}]')
    for code in ('ms', 'zh'):
        for n in [n for n in dir(strings_en) if n.isupper()]:
            walk(getattr(strings_en, n), getattr(STRINGS[code], n), f'{code}.{n}')


def fonts():
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'
    t = set('中文摩纳尔')
    for mod in STRINGS.values():
        for n in dir(mod):
            if n.isupper():
                t |= set(str(getattr(mod, n)))
    chars = ''.join(sorted(c for c in t if ord(c) > 0x2E80))
    for wt in (400, 700):
        q = urllib.parse.urlencode({'family': f'Noto Sans SC:wght@{wt}', 'text': chars, 'display': 'swap'})
        css = urllib.request.urlopen(urllib.request.Request('https://fonts.googleapis.com/css2?' + q, headers={'User-Agent': ua})).read().decode()
        open(os.path.join(HERE, 'assets', 'fonts', f'notosanssc-{wt}.woff2'), 'wb').write(urllib.request.urlopen(re.search(r'url\((https://[^)]+)\)', css).group(1)).read())


def main():
    global S, L
    check_keys()
    if '--fonts' in sys.argv:
        fonts()
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'))
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
    lines = [GL.llms_header(CFG, NAME, S.LLMS['intro']).rstrip(), '', f'- Address: {a["one_line"]}',
             f'- WhatsApp and phone: {F["phone"]["display_intl"]} ({F["whatsapp"]["url"]})', f'- Email: {F["email"]}',
             f'- Company: {F["legal_name"]} ({F["company_no"]})', f'- Brand: {F["brand"]} ({F["brand_zh"]})', '', '## Products']
    lines += [f'- [{S.PG[g]["name"]}]({CFG.canon(gpath(g))}): {S.PG[g]["line"]}' for g in GP]
    lines += ['', '## For drivers', f'- [{S.FINDER["h1"]}]({CFG.canon(P_FINDER)})', f'- [{S.LOCATOR["h1"]}]({CFG.canon(P_LOC)})',
              '', '## For workshops', f'- [{S.JOIN["h1"]}]({CFG.canon(P_JOIN)})', '', '## Pages']
    for LL in I18N.LANGS:
        for p in PAGES:
            lines.append(f'- [{LL["label"]}] {CFG.canon(I18N.page_path(LL, p))}')
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf8').write('\n'.join(lines) + '\n')
    print(f'built {len(built)} pages for {CFG.canonical_base} (live={CFG.live})')


if __name__ == '__main__':
    main()
