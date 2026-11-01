#!/usr/bin/env python3
"""SG Car Workshop: static directory preview.  python3 build.py [outdir]   (default ../site)

Preview mode (LIVE = False): pages are published at https://pageonesingapore.com/preview/sgcarworkshop/ ; canonical, sitemap and
llms.txt name that address, robots.txt says Disallow: / . Internal links and assets are RELATIVE, so the same files work at the
preview address and on the real domain. LIVE = True switches every absolute URL to https://sgcarworkshop.sg/ and opens robots.txt.
Pages never carry a noindex tag: hiding the preview is done by a server header outside the pages (MASTER-RULES 4.3).
"""
import hashlib
import html
import json
import os
import re
import shutil
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'builder'))
from data import ENTRIES, CATEGORIES, REGIONS, PAGE_ONE_WA, PAGE_ONE_WA_SHOW, TIERS, PRICE_NOTE, FREE_EXAMPLE  # noqa: E402
from PIL import Image  # noqa: E402

SITE_NAME = 'SG Car Workshop'   # placeholder brand
DOMAIN = 'sgcarworkshop.sg'     # not bought yet
LIVE = False
GOOGLE_MAPS_KEY = None  # Edwin adds a browser key (referrer-restricted, Places API (New) only) at go-live; None = placeholder photo slots on Basic cards
PREVIEW_BASE = 'https://pageonesingapore.com/preview/sgcarworkshop/'
BASE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW_BASE
PATH_BASE = '/' if LIVE else '/preview/sgcarworkshop/'
UPDATED = '2026-11-01'
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'site'))
E = html.escape
CAT = {c['slug']: c for c in CATEGORIES}
ENT = {e['slug']: e for e in ENTRIES}
PAID = [e for e in ENTRIES if e['tier'] != 'free']
REGION_LIST = [(k, r) for k, r in REGIONS.items() if any(k in e['regions'] for e in ENTRIES)]
CAT_LIST = [c for c in CATEGORIES if any(e['category'] == c['slug'] for e in ENTRIES)]
RN = {k: r['name'] for k, r in REGIONS.items()}

ICONS = {
    'spray': '<path d="M4 9h8v6H4z"/><path d="M12 11h3l2-2"/><path d="M8 15v5"/><path d="M19 5h.01M21 8h.01M21 3h.01M18 2h.01"/>',
    'gear': '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M19 5l-2 2M7 17l-2 2"/>',
    'chip': '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    'battery': '<rect x="2" y="8" width="18" height="10" rx="2"/><path d="M22 11v4M7 11v4M5 13h4"/>',
    'sparkle': '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"/><path d="M19 17l.8 2.2L22 20l-2.2.8L19 23l-.8-2.2L16 20l2.2-.8z"/>',
    'film': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M7 5v14M17 5v14M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    'parts': '<path d="M14.7 6.3a4 4 0 0 0 5 5L21 13l-8 8-3-3 8-8z"/><path d="M3 21l6-6"/>',
    'wrench': '<path d="M14.5 6a4.5 4.5 0 0 0-5.7 5.6L3 17.5 6.5 21l5.9-5.8A4.5 4.5 0 0 0 18 9.5l-2.6 2.6-2.5-.5-.5-2.5z"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/>',
    'pin': '<path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    'phone': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'chev-l': '<path d="M15 18l-6-6 6-6"/>',
    'chev-r': '<path d="M9 18l6-6-6-6"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'out': '<path d="M7 17L17 7M8 7h9v9"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/>',
}


def ic(k, cls=''):
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"%s>%s</svg>' % (
        (' class="%s"' % cls) if cls else '', ICONS[k])


WA_SVG = ('<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 '
          '8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 '
          '5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')
# Logo mark: navy tile, gold map pin holding a hex nut ("find a workshop"). Same shape drawn in make_icons().
MARK_PATH = ('M24 41.5L14.1 27.3A12 12 0 1 1 33.9 27.3Z'
             'M24 13.2L29.9 16.6L29.9 23.4L24 26.8L18.1 23.4L18.1 16.6Z'
             'M24 17.4A2.6 2.6 0 1 0 24 22.6A2.6 2.6 0 1 0 24 17.4Z')
MARK_SVG = ('<svg viewBox="0 0 48 48" aria-hidden="true"><rect width="48" height="48" rx="12" fill="#0f1c33"/>'
            '<path fill="#d4a64a" fill-rule="evenodd" d="%s"/></svg>' % MARK_PATH)
LOGO = MARK_SVG

_h = hashlib.sha1()
for _f in ('dir.css', 'dir.js'):
    _h.update(open(os.path.join(HERE, _f), 'rb').read())
V = _h.hexdigest()[:8]

PAGES = {}   # path ('' = home, 'a/b/' ...) -> html
META = {}    # path -> title (for llms/sitemap)
_imgsz = {}


def imgsize(rel):
    if rel not in _imgsz:
        _imgsz[rel] = Image.open(os.path.join(HERE, 'img', rel)).size
    return _imgsz[rel]


def img_tag(rel, alt, depth, lazy=True, cls=''):
    w, h = imgsize(rel)
    return '<img src="%sassets/img/%s" alt="%s" width="%d" height="%d"%s%s decoding="async">' % (
        pre(depth), rel, E(alt, True), w, h, ' loading="lazy"' if lazy else '', (' class="%s"' % cls) if cls else '')


def pre(depth):
    return '../' * depth or './'


def abs_url(path):
    return BASE + path


def wa_link(num, msg):
    return 'https://wa.me/%s?text=%s' % (num, quote(msg))


def list_wa(depth, what):
    """Page One WhatsApp link for the 'List your workshop' calls to action."""
    return wa_link(PAGE_ONE_WA, 'Hi Page One, I would like to list my workshop on %s (%s).\n\n(From %s)' % (SITE_NAME, what, BASE))


def words(s):
    return len(re.findall(r"[A-Za-z0-9$'-]+", re.sub(r'<[^>]+>', ' ', s)))


# ------------------------------------------------------------------ components
def chip_row(depth, active=None):
    li = ''.join('<li><a href="%sservices/%s/"%s>%s%s</a></li>' % (pre(depth), c['slug'], ' class="on"' if c['slug'] == active else '', ic(c['icon']), E(c['short'])) for c in CATEGORIES)
    return '<ul class="chips" aria-label="Browse by service">%s</ul>' % li


def list_card(depth, what):
    return ('<article class="card list rv"><div class="bd"><span class="ic">%s</span><h3>List your workshop</h3>'
            '<p class="tx">For business owners: run a %s business in Singapore? Basic listings are free.</p>'
            '<div class="acts"><a class="btn sm ghost" href="%slist-your-workshop/" data-cta="list_%s">How listing works</a></div></div></article>') % (
        ic('plus'), E(what), pre(depth), re.sub(r'[^a-z0-9]+', '-', what.lower()).strip('-'))


def crumbs(depth, trail):
    """trail = [(label, relpath or None)]; returns (html, jsonld)"""
    items = [('Home', '')] + trail
    parts, ld = [], []
    for i, (lab, p) in enumerate(items):
        last = i == len(items) - 1
        parts.append(E(lab) if last else '<a href="%s%s">%s</a>' % (pre(depth), p, E(lab)))
        ld.append({'@type': 'ListItem', 'position': i + 1, 'name': lab, 'item': abs_url(p if p is not None else '')} if not last else
                  {'@type': 'ListItem', 'position': i + 1, 'name': lab})
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts), {'@type': 'BreadcrumbList', 'itemListElement': ld}


def header(depth):
    p = pre(depth)
    svc = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (p, c['slug'], E(c['short'])) for c in CAT_LIST)
    reg = ''.join('<li><a href="%sregions/%s/">%s</a></li>' % (p, k, E(r['name'])) for k, r in REGION_LIST)
    return ('<a class="skip" href="#main">Skip to content</a><header class="top"><div class="w bar"><a class="brand" href="%s" aria-label="%s home">%s<span class="wm"><span><b>SG</b> Car Workshop</span><small>Singapore car workshop directory</small></span></a>'
            '<details class="menu"><summary aria-label="Menu">%s<span>Menu</span></summary><nav class="mpanel" aria-label="Main">'
            '<a class="mfind" href="%s#find">%s Find a workshop</a>'
            '<div class="mcols"><div class="svc-col"><h3>Services</h3><ul>%s</ul></div><div><h3>Regions</h3><ul>%s</ul></div></div>'
            '<a class="mabout" href="%sabout/">About</a></nav></details></div></header>') % (p, E(SITE_NAME), LOGO, ic('menu'), p, ic('search'), svc, reg, p)


def footer(depth):
    p = pre(depth)
    cats = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (p, c['slug'], E(c['short'])) for c in CAT_LIST)
    reg = ''.join('<li><a href="%sregions/%s/">%s</a></li>' % (p, k, E(r['name'])) for k, r in REGION_LIST)
    return ('<footer class="ft"><div class="w cols"><div><h3>%s</h3><p>A directory of car workshops and car services in Singapore, run by '
            '<a href="https://pageonesingapore.com/" rel="noopener">Page One Singapore</a>.</p><p class="fine">Listing details are confirmed with each business. '
            'WhatsApp taps are counted and reported to the business. This is a preview and the brand name is a placeholder.</p></div>'
            '<div><h3>Services</h3><ul>%s</ul></div><div><h3>Regions</h3><ul>%s</ul></div>'
            '<div><h3>Directory</h3><ul><li><a href="%sabout/">About</a></li><li><a href="%slist-your-workshop/">List your workshop</a></li>'
            '<li><a href="%sllms.txt">llms.txt</a></li></ul></div></div></footer>') % (E(SITE_NAME), cats, reg, p, p, p)


def wabar(items):
    return '<div class="wabar" role="region" aria-label="Contact">%s</div>' % ''.join(items)


def page(path, title, desc, body, schema=None, og=None, bar=None, h1=None):
    assert len(title) <= 60, (path, len(title), title)
    assert len(desc) <= 160, (path, len(desc))
    depth = path.count('/')
    url = abs_url(path)
    og_rel = og or 'og-default.jpg'
    remote = og_rel.startswith('http')
    og_url = og_rel if remote else BASE + 'assets/img/' + og_rel
    ow, oh = (1200, 630) if og_rel in ('og-default.jpg', 'wei/og.jpg') else (None, None) if remote else imgsize(og_rel)
    ld = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(s, ensure_ascii=False).replace('</', '<\\/') for s in (schema or []))
    p = pre(depth)
    gk = '<meta name="gmaps-key" content="%s">\n' % E(GOOGLE_MAPS_KEY) if GOOGLE_MAPS_KEY else ''
    out = f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc, True)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{E(url)}">
<link rel="icon" href="{p}assets/favicon.ico" sizes="48x48">
<link rel="icon" href="{p}assets/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{p}assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{E(SITE_NAME)}">
<meta property="og:title" content="{E(title, True)}">
<meta property="og:description" content="{E(desc, True)}">
<meta property="og:url" content="{E(url)}">
<meta property="og:image" content="{E(og_url)}">
{('<meta property="og:image:width" content="%d">' + chr(10) + '<meta property="og:image:height" content="%d">') % (ow, oh) if ow else ''}
<meta property="og:image:alt" content="{E(h1 or title, True)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{E(og_url)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap">
<link rel="stylesheet" href="{p}assets/dir.css?v={V}">
<script>document.documentElement.className+=' js'</script>
{gk}{ld}</head>
<body{' class="has-bar"' if bar else ''}>
{header(depth)}
<main id="main">
{body}
</main>
{footer(depth)}
{bar or ''}
<script src="{p}assets/dir.js?v={V}" defer></script>
</body>
</html>
'''
    PAGES[path] = out
    META[path] = title


# ------------------------------------------------------------------ pages
def home():
    depth = 0
    feats = [e for e in ENTRIES if e['tier'] == 'premium_leadgen']
    slides = ''.join(slide(e) for e in feats)
    cards = ''.join(card(e, 0, '') for e in ENTRIES)
    faqs = [
        ('What is %s?' % SITE_NAME, 'A directory of car workshops and car services in Singapore. Each entry shows what the business does, where it is and how to contact it, using details confirmed by the business or taken from its public listing.'),
        ('How do I contact a workshop?', 'Tap WhatsApp or Call on a card. The WhatsApp message is prefilled with the workshop name and says you found them on %s, so you only need to add your car and what you need.' % SITE_NAME),
        ('Do you rank or review workshops?', 'No. Entries are not ranked and we do not write reviews. Profile pages may show a rating line from a source people can open, with its link and the date we checked.'),
        ('Which regions can I search?', 'Singapore has five planning regions: North, North-East, East, West and Central. Pick one or more in the search panel to see workshops that serve them. Mobile services can cover several regions.'),
    ]
    faq_html = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in faqs)
    svc_opts = '<label class="opt"><input type="radio" name="svc" value="" checked><span>Any service</span></label>' + ''.join(
        '<label class="opt"><input type="radio" name="svc" value="%s"><span>%s</span></label>' % (c['slug'], E(c['short'])) for c in CAT_LIST)
    reg_opts = ''.join('<label class="opt"><input type="checkbox" name="reg" value="%s"><span>%s</span></label>' % (k, E(r['name'])) for k, r in REGION_LIST)
    svc_tiles = ''.join('<li><a href="services/%s/"><span class="ti">%s</span><span><b>%s</b><small>%d listing%s</small></span></a></li>' % (
        c['slug'], ic(c['icon']), E(c['short']), n, '' if n == 1 else 's') for c in CAT_LIST for n in [sum(1 for e in ENTRIES if e['category'] == c['slug'])])
    reg_tiles = ''.join('<li><a href="regions/%s/"><span class="ti">%s</span><span><b>%s</b><small>%d listing%s</small></span></a></li>' % (
        k, ic('pin'), E(r['name']), n, '' if n == 1 else 's') for k, r in REGION_LIST for n in [sum(1 for e in ENTRIES if k in e['regions'])])
    tiers = tiers_strip()
    body = f'''<section class="finder" id="find"><div class="w"><div class="hero-t"><h1>Find a car workshop in Singapore</h1>
<p>Search by service and area, then message the workshop directly on WhatsApp.</p></div>
<p class="nojs">Browse by <a href="#services">service</a> or <a href="#regions">region</a> below.</p>
<form class="panel" id="finder" role="search" aria-label="Find a workshop" onsubmit="return false">
<p class="shint" id="shint"><span class="pt" aria-hidden="true">&#128070;</span> Tap and type what you need and where, in any order</p>
<label class="q"><span class="skip">Search workshops by service, area or name</span>{ic('search')}<input id="q" type="search" placeholder="e.g. gearbox repair Woodlands" autocomplete="off" autocapitalize="off" enterkeyhint="search"></label>
<div class="frow"><span class="lab" id="lab-s">Service <small>optional</small></span><div class="opts" role="radiogroup" aria-labelledby="lab-s">{svc_opts}</div></div>
<div class="frow"><span class="lab" id="lab-r">Region <small>optional, choose one or more</small></span><div class="opts" role="group" aria-labelledby="lab-r">{reg_opts}</div></div>
<div class="fbar"><p id="count" aria-live="polite"><b>{len(ENTRIES)}</b> workshops</p><button type="button" class="linkbtn" id="reset">Clear</button></div>
</form></div></section>
<section class="feat" aria-roledescription="carousel" aria-label="Featured Premium workshops"><div class="w"><div class="sec-h"><h2>Featured Premium workshops</h2>
<div class="car-nav"><button type="button" id="cprev" aria-label="Previous">{ic('chev-l')}</button><button type="button" id="cnext" aria-label="Next">{ic('chev-r')}</button></div></div>
<div class="marq" id="marq"><ul class="track" id="track" aria-label="Featured workshops">{slides}</ul></div></div></section>
<section id="workshops" class="lst"><div class="w"><div class="sec-h"><h2>All workshops</h2><a class="sec-link" href="#services">Browse by service</a></div><div class="grid" id="results">{cards}</div>
<div class="empty" id="empty"><b>No workshops match.</b> Try fewer filters, or <a href="list-your-workshop/">list your workshop</a>.</div></div></section>
<section class="alt" id="services"><div class="w"><h2>Browse by service</h2><ul class="tiles">{svc_tiles}</ul></div></section>
<section id="regions"><div class="w"><h2>Browse by region</h2><ul class="tiles rg">{reg_tiles}</ul></div></section>
<section class="alt"><div class="w"><h2>How the listings work</h2>{tiers}</div></section>
<section><div class="w nar"><h2>Questions</h2>{faq_html}</div></section>
<section class="owner-sec"><div class="w"><p class="owner-note">For business owners: Own a car workshop? Basic listings are free. <a href="list-your-workshop/" data-cta="list_home">List or manage your workshop &rarr;</a></p></div></section>'''
    ld = [
        {'@context': 'https://schema.org', '@type': 'WebSite', 'name': SITE_NAME, 'url': abs_url(''), 'inLanguage': 'en-SG'},
        {'@context': 'https://schema.org', '@type': 'Organization', 'name': SITE_NAME, 'url': abs_url(''), 'parentOrganization': {'@type': 'Organization', 'name': 'Page One Singapore', 'url': 'https://pageonesingapore.com/'}},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]},
    ]
    page('', 'Car Workshops in Singapore | SG Car Workshop',
         'Find car workshops in Singapore by service and region: repair, gearbox, ABS and ECU, spray painting, batteries, detailing, wraps and parts.', body, ld)


def category(c):
    depth = 2
    es = [e for e in ENTRIES if e['category'] == c['slug']]
    n = words(c['intro'])
    assert 40 <= n <= 60, (c['slug'], n)
    cr, crld = crumbs(depth, [('Services', 'services/' + c['slug'] + '/'), (c['name'], None)][1:])
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:20px"><div class="w"><h1>{E(c['name'])} in Singapore</h1><p class="lede">{E(c['intro'])}</p>{chip_row(depth, c['slug'])}</div></section>
<section><div class="w"><h2 class="rv">Listings</h2><div class="grid">{''.join(card(e, depth, 'services/%s/' % c['slug']) for e in es)}{list_card(depth, c['short'].lower())}</div></div></section>'''
    itemlist = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': c['name'] + ' in Singapore', 'numberOfItems': len(es),
                'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': abs_url('workshops/%s/' % e['slug']), 'name': e['name']} for i, e in enumerate(es)]}
    page('services/%s/' % c['slug'], '%s in Singapore | %s' % (c['name'], SITE_NAME), c['blurb'] + ' Browse Singapore listings with details confirmed by each business.',
         body, [itemlist, dict(crld, **{'@context': 'https://schema.org'})], h1=c['name'])


def region(slug, a):
    depth = 2
    es = [e for e in ENTRIES if slug in e['regions']]
    cr, crld = crumbs(depth, [(a['name'] + ' region', None)])
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:14px"><div class="w"><h1>Car workshops in the {E(a['name'])} region</h1><p class="lede">{E(a['intro'])}</p></div></section>
<section><div class="w"><div class="grid">{''.join(card(e, depth, 'regions/%s/' % slug) for e in es)}{list_card(depth, 'car workshop in the ' + a['name'] + ' region')}</div></div></section>'''
    itemlist = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Car workshops in the %s region' % a['name'], 'numberOfItems': len(es),
                'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': abs_url('workshops/%s/' % e['slug']), 'name': e['name']} for i, e in enumerate(es)]}
    page('regions/%s/' % slug, 'Car Workshops in %s Singapore | %s' % (a['name'], SITE_NAME), 'Car workshops and car services in the %s region of Singapore, with details confirmed by each business.' % a['name'],
         body, [itemlist, dict(crld, **{'@context': 'https://schema.org'})], h1='Car workshops in the %s region' % a['name'])


def tier_badge(e_or_tier, cls=''):
    t = e_or_tier if isinstance(e_or_tier, str) else e_or_tier['tier']
    return '<span class="tier t-%s%s">%s</span>' % (t, (' ' + cls) if cls else '', E(TIERS[t]['badge']))


ASK = {'everest-garage': 'servicing or repair for my car', 'hup-soon-lee-motor-service': 'servicing or repair for my car', 'cys-automobile-services': 'servicing or repair for my car', 'sg-garage': 'my car', 'cleanic-detailing': 'cleaning or fumigation for my car', 'autotex': 'a part for my car',
       'battery-rescue-sg': 'a battery for my car', 'wei-car-spray-painting': 'a spray painting job'}


def page_label(page_path):
    return '/' + page_path


def wa_href(e, page_path):
    """Directory WhatsApp link: the prefilled message names the business, the directory and the page the lead came from."""
    msg = "Hi %s, I found you on %s (%s). I'd like to ask about %s." % (e['name'], SITE_NAME, page_label(page_path), ASK.get(e['slug'], 'my car'))
    return wa_link(e['whatsapp'], msg)


def track_attrs(kind, e, page_path):
    return 'data-cta="%s_dir_%s" data-tier="%s" data-page="%s"' % (kind, e['slug'], e['tier'], E(page_label(page_path)))


def wa_btn(e, page_path, cls='', label='WhatsApp'):
    return '<a class="btn wa%s" href="%s" target="_blank" rel="noopener" %s>%s %s</a>' % (
        (' ' + cls) if cls else '', E(wa_href(e, page_path)), track_attrs('whatsapp', e, page_path), WA_SVG, E(label))


def call_btn(e, page_path, cls='', label='Call'):
    return '<a class="btn%s" href="tel:%s" %s>%s %s</a>' % ((' ' + cls) if cls else '', e['phone'], track_attrs('call', e, page_path), ic('phone'), E(label))


def photo_img(p, depth, lazy=True, cls=''):
    if p.get('f'):
        return img_tag(p['f'], p['alt'], depth, lazy=lazy, cls=cls)
    return '<img src="%s" alt="%s"%s decoding="async" referrerpolicy="no-referrer"%s>' % (
        E(p['u'], True), E(p['alt'], True), ' loading="lazy"' if lazy else '', (' class="%s"' % cls) if cls else '')


def tile(e):
    return '<div class="tile" aria-hidden="true">%s<b>%s</b><span>%s</span></div>' % (ic(CAT[e['category']]['icon']), E(e['name']), E(e.get('tile_text', CAT[e['category']]['short'])))


def region_label(e):
    rs = e['regions']
    if len(rs) == 5:
        return 'All regions (mobile)'
    names = ', '.join(RN[r] for r in rs)
    return '%s \u00b7 %s' % (e['area_label'], names) if len(rs) == 1 else names


def call_icon(e, page_path):
    return '<a class="btn sm ico" href="tel:%s" aria-label="Call %s" %s>%s</a>' % (e['phone'], E(e['name'], True), track_attrs('call', e, page_path), ic('phone'))


def owner_note(e, depth, page_path, cls='owner-note'):
    """Small grey line for business owners. Links to the owner section of the listing page, never to a WhatsApp,
    so customers only ever see the workshop's own WhatsApp on a listing."""
    return ('<p class="%s">For business owners: Is this your workshop? <a href="%slist-your-workshop/?w=%s#claim" data-cta="claim_%s" data-page="%s">Manage this listing &rarr;</a></p>'
            % (cls, pre(depth), e['slug'], e['slug'], E(page_label(page_path))))


SYN = {   # extra words people type for each service (search only, never shown)
    'spray-painting-bodywork': 'spray paint painting respray resprayed colour color bodywork body dent scratch panel',
    'gearbox-repair': 'gearbox transmission auto automatic gear shift cvt dsg',
    'abs-ecu-module-repair': 'abs ecu module ecm tcm brake engine computer control unit electronics',
    'car-battery': 'battery batteries replace replacement jump start flat alternator',
    'car-detailing-coating': 'detailing detail coating ceramic polish polishing wash clean cleaning interior',
    'car-wrap-ppf': 'wrap wraps wrapping ppf film protection tint sticker',
    'car-parts': 'parts part spare accessories',
    'general-servicing-repair': 'servicing service repair maintenance aircon air con ac cooling oil brake workshop mechanic',
}


def card_search(e):
    c = CAT[e['category']]
    t = ' '.join([e['name'], c['name'], SYN.get(c['slug'], ''), e['area_label'], e.get('desc', ''), ' '.join(e.get('card_text', [])[:1]),
                  ' '.join(s['n'] for s in e['services']), ' '.join(e.get('services_public', [])), e.get('domain', ''), e.get('regions_note', ''), e.get('service_area', '')]).lower()
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()


def card(e, depth, page_path=''):
    c = CAT[e['category']]
    attrs = 'data-search="%s" data-cat="%s" data-regions="%s" data-tier="%s"' % (E(card_search(e), True), c['slug'], ' '.join(e['regions']), e['tier'])
    rg = '<p class="meta rg">%s<span>%s</span></p>' % (ic('pin'), E(region_label(e)))
    if e['tier'] == 'free':
        acts = wa_btn(e, page_path, 'sm') if e.get('whatsapp') else call_btn(e, page_path, 'sm wa', 'Call ' + e['phone_show'])
        acts += '<span class="minor"><a class="btn sm ghost" href="https://www.google.com/maps?cid=%s" target="_blank" rel="noopener" data-cta="directions_%s">Directions</a>' % (e['cid'], e['slug'])
        acts += '<a class="btn sm ghost" href="%sworkshops/%s/" data-cta="view_%s">View</a></span>' % (pre(depth), e['slug'], e['slug'])
        return ('<article class="card basic" %s><div class="ph gph" data-place="%s"><div class="tile ini" aria-hidden="true"><b>%s</b><span class="gph-note">Google photo</span></div>%s</div><div class="bd"><span class="tag">%s</span>'
                '<h3><a href="%sworkshops/%s/">%s</a></h3>%s<p class="tx full">%s</p><div class="acts">%s</div>'
                '%s</div></article>') % (
            attrs, E(e.get('place_id', '')), E(e['name'][0]), tier_badge(e, 'on-ph'), E(c['short']), pre(depth), e['slug'], E(e['name']), rg, E(e['desc']), acts, owner_note(e, depth, page_path, 'claim'))
    ci = e.get('card_img')
    ph = photo_img(dict(ci, alt=ci['alt']), depth, lazy=True) if ci else tile(e)
    acts = wa_btn(e, page_path, 'sm') + (call_icon(e, page_path) if e.get('phone') else '')
    return ('<article class="card" %s>'
            '<div class="ph">%s%s</div><div class="bd"><span class="tag">%s</span><h3><a href="%sworkshops/%s/">%s</a></h3>'
            '%s<p class="tx">%s</p><div class="acts">%s</div></div></article>') % (
        attrs, ph, tier_badge(e, 'on-ph'), E(c['short']), pre(depth), e['slug'], E(e['name']), rg, E(e['card_text'][0]), acts)


def slide(e):
    c = CAT[e['category']]
    ci = e.get('card_img')
    return ('<li><article class="card fc"><div class="ph">%s%s</div><div class="bd"><span class="tag">%s</span><h3><a href="workshops/%s/">%s</a></h3>'
            '<p class="meta rg">%s<span>%s</span></p><p class="tx">%s</p><div class="acts">%s<a class="btn sm" href="workshops/%s/">View</a></div></div></article></li>') % (
        photo_img(ci, 0, lazy=True) if ci else tile(e), tier_badge(e, 'on-ph'), E(c['short']), e['slug'], E(e['name']), ic('pin'), E(region_label(e)), E(e['card_text'][0]),
        wa_btn(e, '', 'sm'), e['slug'])


def free_card(depth, ex=FREE_EXAMPLE):
    """Free-tier card: plain. No photo, no phone. Shown only as a labelled example (made-up name)."""
    c = CAT[ex['category']]
    return ('<article class="card free-card"><div class="bd"><span class="ex-flag">Example only, not a real business</span>%s<span class="tag">%s</span>'
            '<h3>%s</h3><p class="meta">%s</p><p class="tx">%s</p><div class="acts">'
            '<span class="btn sm wa ex" aria-disabled="true">%s WhatsApp</span><span class="btn sm ex" aria-disabled="true">Website: %s</span></div></div></article>') % (
        tier_badge('free'), E(c['short']), E(ex['name']), E(ex['area_label']), E(ex['text']), WA_SVG, E(ex['site_label']))


def tiers_strip():
    """Short three-tier summary for the home page. No prices."""
    items = [
        ('free', 'A card plus a short profile page: one Google photo, address and Directions, opening hours, a Google rating line and a WhatsApp or Call button.'),
        ('premium', 'A full page with real photos, services, address, map, reviews line and FAQs.'),
        ('premium_leadgen', 'Everything in Verified, plus the business\'s own website and local search work. Premium workshops are featured at the top.'),
    ]
    li = ''.join('<li>%s<b>%s</b>%s</li>' % (tier_badge(t), E(TIERS[t]['tagline']), E(txt)) for t, txt in items)
    return '<ol class="steps tiers-strip">%s</ol><p class="fine" style="margin-top:10px"><a href="list-your-workshop/">Compare the three tiers</a></p>' % li


def ld_business(e, url):
    ld = {'@context': 'https://schema.org', '@type': 'AutoRepair', '@id': url + '#business', 'name': e['name'], 'url': url, 'mainEntityOfPage': url}
    first = e['photos'][0] if e.get('photos') else e.get('card_img')
    if first:
        ld['image'] = [BASE + 'assets/img/' + first['f'] if first.get('f') else first['u']]
    if e.get('phone'):
        ld['telephone'] = e['phone']
    adds = [a for a in e.get('addresses', []) if a.get('postal')]
    if e['slug'] == 'battery-rescue-sg':
        ld['location'] = [{'@type': 'Place', 'name': a['label'], 'address': {'@type': 'PostalAddress', 'streetAddress': a['street'], 'addressLocality': 'Singapore', 'addressCountry': 'SG'}} for a in e['addresses']]
    elif e.get('addresses'):
        a0 = e['addresses'][0]
        ld['address'] = {'@type': 'PostalAddress', 'streetAddress': a0['street'], 'postalCode': a0['postal'], 'addressLocality': 'Singapore', 'addressCountry': 'SG'}
        if len(e['addresses']) > 1:
            ld['location'] = [{'@type': 'Place', 'name': a['label'], 'address': {'@type': 'PostalAddress', 'streetAddress': a['street'], 'postalCode': a['postal'], 'addressLocality': 'Singapore', 'addressCountry': 'SG'}} for a in e['addresses'][1:]]
    ld['hasMap'] = e['map_url']
    if e.get('hours_ld'):
        ld['openingHoursSpecification'] = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': d, 'opens': o, 'closes': c} for d, o, c in e['hours_ld']]
    if len(e['regions']) == 5:
        ld['areaServed'] = {'@type': 'Country', 'name': 'Singapore'}
    else:
        ld['areaServed'] = [{'@type': 'Place', 'name': RN[r] + ' region, Singapore'} for r in e['regions']]
    ld['makesOffer'] = [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['n']}} for s in e['services']]
    same = list(e.get('social') or [])
    if e['tier'] == 'premium_leadgen':
        same.append(e['url'])
    if same:
        ld['sameAs'] = same
    if e.get('legal'):
        ld['legalName'] = e['legal']
        ld['taxID'] = e['uen']
    return ld


def listing(e):
    """Verified and Premium page. Same layout for both; the lead-gen tier adds the website button below WhatsApp and Call."""
    depth = 2
    c = CAT[e['category']]
    path = 'workshops/%s/' % e['slug']
    url = abs_url(path)
    cr, crld = crumbs(depth, [(c['name'], 'services/%s/' % c['slug']), (e['name'], None)])
    lead = e['tier'] == 'premium_leadgen'
    wa, call = wa_btn(e, path, 'big'), call_btn(e, path, 'big', 'Call ' + e['phone_show'])
    wa = wa.replace('WhatsApp</a>', 'WhatsApp %s</a>' % e.get('whatsapp_show', e['phone_show']))
    sec = []
    if lead:
        sec.append('<a class="btn amber" href="%s" target="_blank" rel="noopener" data-cta="visit_%s" data-tier="%s" data-page="%s">Visit %s for full details %s</a>' % (
            E(e['url']), e['slug'], e['tier'], E(page_label(path)), E(e['domain']), ic('out')))
    if e.get('book_url'):
        sec.append('<a class="btn" href="%s" target="_blank" rel="noopener" data-cta="book_%s">%s</a>' % (E(e['book_url']), e['slug'], E(e['book_label'])))
    sec.append('<a class="btn" href="%s" target="_blank" rel="noopener" data-cta="map_%s" data-map>%s %s</a>' % (E(e['map_url']), e['slug'], ic('pin'), E(e.get('map_label', 'Open in Google Maps'))))
    btns = '<div class="acts main-acts">%s%s</div><div class="acts sec-acts">%s</div>' % (wa, call, ''.join(sec))
    photos = e.get('photos') or []
    hero = '<div class="hero-ph">%s</div>' % (photo_img(photos[0], depth, lazy=False) if photos else tile(e))
    if photos and len(photos) > 1:
        gal = '<h2>Recent work</h2><div class="gal">%s</div>' % ''.join(
            '<figure class="rv job">%s<figcaption>%s</figcaption></figure>' % (photo_img(p, depth), E(p['cap'])) for p in photos[1:])
    else:
        gal = ''
    if e.get('illustrations'):
        gal += '<h2>Parts range</h2><div class="gal">%s</div>' % ''.join(
            '<figure class="rv illus">%s<figcaption>%s</figcaption></figure>' % (photo_img(p, depth), E(p['cap'])) for p in e['illustrations'])
    svcs = ''.join('<li class="svc rv"><b>%s</b><span>%s</span>%s</li>' % (E(s['n']), E(s['d']), ('<em class="pr">%s</em>' % E(s['p'])) if s.get('p') else '') for s in e['services'])
    extra = ''
    for h, kind, items in e.get('sections', []):
        extra += '<h2>%s</h2>' % E(h) + (('<ul class="tick">%s</ul>' % ''.join('<li>%s</li>' % E(i) for i in items)) if kind == 'ul' else ''.join('<p>%s</p>' % E(i) for i in items))
    adds = ''.join('<li data-addr>%s<span>%s%s%s</span></li>' % (
        ic('pin'), ('<b>%s</b><br>' % E(a['label'])) if a.get('label') else '', E(a['street']),
        (', Singapore ' + a['postal']) if a.get('postal') else ', Singapore') for a in e.get('addresses', []))
    if e.get('service_area') and not adds:
        adds = '<li data-addr>%s<span>%s</span></li>' % (ic('pin'), E(e['service_area']))
    elif e.get('service_area'):
        adds += '<li>%s<span>%s</span></li>' % (ic('pin'), E(e['service_area']))
    if e.get('addresses') and e['addresses'][0].get('note'):
        adds += '<li>%s<span>%s</span></li>' % (ic('shield'), E(e['addresses'][0]['note']))
    hours = ''
    if e.get('hours'):
        hours = '<h3>Opening hours</h3><dl class="hours">%s</dl>' % ''.join('<dt>%s</dt><dd>%s</dd>' % (E(a), E(b)) for a, b in e['hours'])
    if e.get('hours_note'):
        hours += '<p class="fine">%s</p>' % E(e['hours_note'])
    contact = '<li>%s<span>Call %s or WhatsApp %s</span></li>' % (ic('phone'), e['phone_show'], e.get('whatsapp_show', e['phone_show']))
    rv = e['reviews']
    reviews = '<p class="reviews-line">%s <span>%s</span> <a href="%s" target="_blank" rel="noopener" data-cta="reviews_%s">%s</a></p>' % (
        ic('shield'), E(rv['text']), E(rv['url']), e['slug'], E(rv['label']))
    faqs = ''.join('<details class="faq"><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in e['faqs'])
    price_note = '<p class="fine">%s</p>' % E(e['price_note']) if e.get('price_note') else ''
    note = '<p class="fine disclose">%s</p>' % E(e['note']) if e.get('note') else ''
    body = f'''<div class="w nar prem">{cr}
<div class="badges" style="margin-top:14px">{tier_badge(e)}<span class="tag">{E(c['short'])}</span></div>
<h1 style="margin-top:8px">{E(e['name'])}</h1>
<p class="meta">{E(e['area_label'])}</p>
<p class="lede" style="font-size:1rem">{E(e['lede'])}</p>
{btns}
{hero}
<h2>Services</h2>
<ul class="svcs">{svcs}</ul>
{price_note}
{gal}
{extra}
<section id="find" class="findus"><h2>{E(e.get('addr_heading', 'Find us'))}</h2>
<ul class="facts">{adds}{contact}</ul>
{hours}
</section>
<h2>Reviews</h2>
{reviews}
<h2>Questions</h2>
<div class="faqs">{faqs}</div>
<div class="cta rv" style="margin-top:26px"><div><h2>Ask {E(e['name'])}</h2><p>Message on WhatsApp or call. Say you found them on {E(SITE_NAME)}.</p></div><div class="acts">{wa}{call}</div></div>
{('<div class="acts sec-acts" style="margin-top:12px">%s</div>' % sec[0]) if lead else ''}
{note}
<p class="fine">Details are checked with the business before the directory goes live. Last updated {UPDATED}. Browse more <a href="../../services/{c['slug']}/">{E(c['name'].lower())}</a> listings{' or <a href="../../regions/%s/">workshops in the %s region</a>' % (e['regions'][0], E(RN[e['regions'][0]]))}.</p>
</div>'''
    bar = wabar([wa_btn(e, path), call_btn(e, path)])
    faq_ld = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in e['faqs']]}
    ld = [ld_business(e, url), faq_ld, dict(crld, **{'@context': 'https://schema.org'})]
    og = e.get('og_img') or (photos[0]['u'] if photos and photos[0].get('u') else None)
    page(path, e['title'], e['desc'], body, ld, og=og, bar=bar, h1=e['name'])


def basic_page(e):
    """Basic (free) profile page: deliberately short. One Google photo slot, short text, plain service names, address + Directions, hours,
    Google rating line (text only, no review schema), WhatsApp or Call, owner claim box. No gallery, FAQs, service descriptions or prices."""
    depth = 2
    c = CAT[e['category']]
    path = 'workshops/%s/' % e['slug']
    url = abs_url(path)
    cr, _ = crumbs(depth, [(c['name'], 'services/%s/' % c['slug']), (e['name'], None)])
    gurl = 'https://www.google.com/maps?cid=%s' % e['cid']
    if e.get('whatsapp'):
        contact_btn = wa_btn(e, path, 'big', 'WhatsApp ' + e['phone_show'])
        contact_line = 'WhatsApp %s' % e['phone_show']
    else:
        contact_btn = call_btn(e, path, 'big wa', 'Call ' + e['phone_show'])
        contact_line = 'Call %s' % e['phone_show']
    photo = ('<div class="hero-ph gph" data-place="%s"><div class="tile ini" aria-hidden="true"><b>%s</b><span class="gph-note">Google photo</span></div></div>'
             % (E(e['place_id']), E(e['name'][0])))
    svcs = ''.join('<li>%s</li>' % E(s) for s in e['services_public'])
    hours = ''.join('<dt>%s</dt><dd>%s</dd>' % (E(a), E(b)) for a, b in e['hours_rows'])
    rating = 'Rated %s from %d Google reviews (checked %s)' % (e['rating'], e['reviews'], e['checked'])
    reviews = '<p class="reviews-line">%s <a href="%s" target="_blank" rel="noopener" data-cta="reviews_%s" data-tier="free" data-page="%s">%s</a></p>' % (
        ic('shield'), E(gurl), e['slug'], E(page_label(path)), E(rating))
    claim = owner_note(e, depth, path)
    body = f'''<div class="w nar basicpg">{cr}
<div class="badges" style="margin-top:14px">{tier_badge(e)}<span class="tag">{E(c['short'])}</span></div>
<h1 style="margin-top:8px">{E(e['name'])}</h1>
<p class="meta rg">{ic('pin')}<span>{E(region_label(e))}</span></p>
{photo}
<p class="lede" style="font-size:1rem">{E(e['lede'])}</p>
<p>{E(e['area_ctx'])}</p>
<div class="acts main-acts">{contact_btn}</div>
<h2>Services</h2>
<ul class="tick svc-plain">{svcs}</ul>
<p class="fine">From the workshop's Google listing.</p>
<section id="find" class="findus"><h2>Find us</h2>
<ul class="facts"><li data-addr>{ic('pin')}<span>{E(e['address_public'])}</span></li><li>{ic('phone')}<span>{E(contact_line)}</span></li></ul>
<p style="margin:10px 0"><a class="btn" href="{gurl}" target="_blank" rel="noopener" data-cta="directions_{e['slug']}" data-tier="free" data-page="{E(page_label(path))}" data-map>{ic('pin')} Directions</a></p>
<h3>Opening hours</h3><dl class="hours">{hours}</dl>
</section>
{reviews}
<p class="fine">Checked on Google, 1 Nov 2026. More <a href="../../services/{c['slug']}/">{E(c['name'].lower())}</a> or <a href="../../regions/{e['regions'][0]}/">{E(RN[e['regions'][0]])} region</a> workshops.</p>
{claim}
</div>'''
    street, postal = e['address_public'].rsplit(', Singapore ', 1)
    ld = {'@context': 'https://schema.org', '@type': 'AutoRepair', 'name': e['name'], 'url': url,
          'address': {'@type': 'PostalAddress', 'streetAddress': street, 'postalCode': postal, 'addressLocality': 'Singapore', 'addressCountry': 'SG'},
          'telephone': e['phone'], 'openingHours': e['hours_ld']}
    bar = wabar([wa_btn(e, path) if e.get('whatsapp') else call_btn(e, path, 'wa'),
                 '<a class="btn" href="%s" target="_blank" rel="noopener" data-cta="directions_%s" data-tier="free" data-page="%s">%s Directions</a>' % (E(gurl), e['slug'], E(page_label(path)), ic('pin'))])
    desc = '%s: car workshop in %s, %s region. Address, directions, hours and Google rating. %s.' % (e['name'], e['area_label'], RN[e['regions'][0]], contact_line)
    page(path, '%s | %s Car Workshop' % (e['name'], e['area_label']), desc, body, [ld], bar=bar, h1=e['name'])


def tier_features():
    return [
        ('Basic card and short profile page: name, short description, category, area, one Google photo', 'yes', 'yes', 'yes'),
        ('Link to your website', 'yes', 'yes', 'yes (shown as a secondary button)'),
        ('WhatsApp (or Call) button with the source tagged', 'yes', 'yes', 'yes'),
        ('Tap counts (WhatsApp and call) reported to you', 'yes', 'yes', 'yes'),
        ('Your own photos and a completed-job gallery', 'no', 'yes', 'yes'),
        ('Detailed services with short descriptions', 'no', 'yes', 'yes'),
        ('Address, Directions link and opening hours (where confirmed)', 'yes', 'yes', 'yes'),
        ('Sticky contact bar on phones', 'yes', 'yes', 'yes'),
        ('Both WhatsApp and Call buttons', 'no', 'yes', 'yes'),
        ('Rating line from a source people can check, with link and date', 'yes', 'yes', 'yes'),
        ('3 to 5 local FAQs', 'no', 'yes', 'yes'),
        ('LocalBusiness structured data', 'yes', 'yes', 'yes'),
        ('Your own website, local SEO, AI search optimisation, regular content', 'no', 'no', 'yes'),
        ('Lead tracking and monthly reporting', 'no', 'no', 'yes'),
    ]


def tier_table():
    def cell(v):
        if v == 'yes':
            return '<td class="y"><span aria-label="Included">%s</span></td>' % ic('shield')
        if v == 'no':
            return '<td class="n"><span aria-label="Not included">&ndash;</span></td>'
        return '<td class="y">%s</td>' % E(v)
    heads = ''.join('<th scope="col">%s<span class="pr">%s</span><small>%s</small></th>' % (tier_badge(t), E(TIERS[t]['price_text']), E(TIERS[t]['tagline'])) for t in TIERS)
    rows = ''.join('<tr><th scope="row">%s</th>%s</tr>' % (E(f), cell(a) + cell(b) + cell(c)) for f, a, b, c in tier_features())
    table = '<div class="tier-table"><table><thead><tr><th></th>%s</tr></thead><tbody>%s</tbody></table></div>' % (heads, rows)
    cards = ''
    for i, t in enumerate(TIERS):
        li = ''.join('<li%s>%s</li>' % ('' if row[1 + i] != 'no' else ' class="no"', E(row[0])) for row in tier_features())
        cards += ('<article class="card tier-card rv"><div class="bd">%s<h3>%s</h3><p class="pr">%s</p><p class="meta">%s</p><ul class="tick">%s</ul>'
                  '<a class="btn amber" href="%s" target="_blank" rel="noopener" data-cta="whatsapp_list_tier_%s">%s Ask about %s</a></div></article>') % (
            tier_badge(t), E(TIERS[t]['label']), E(TIERS[t]['price_text']), E(TIERS[t]['tagline']), li, E(list_wa(1, TIERS[t]['label'])), t, WA_SVG, E(TIERS[t]['label']))
    return table + '<div class="tier-cards">%s</div>' % cards


def list_page():
    depth = 1
    cr, crld = crumbs(depth, [('List your workshop', None)])
    wa = E(list_wa(depth, 'general enquiry'))
    claim_generic = E(wa_link(PAGE_ONE_WA, "Hi Page One, I'm a workshop owner, about my %s listing.\n\n(From %s)" % (SITE_NAME, BASE + 'list-your-workshop/')))
    claim_names = E(json.dumps({e['slug']: e['name'] for e in ENTRIES}), True)
    body = f'''<div class="w">{cr}
<h1 style="margin-top:14px">List your workshop</h1>
<p class="lede" style="font-size:1rem;max-width:720px">{E(SITE_NAME)} lists car workshops and car services in Singapore: repair, gearbox, ABS and ECU modules, spray painting and bodywork, batteries, detailing and coating, wraps and PPF, and parts. Pick the tier that fits your business.</p>
<h2 style="margin-top:24px">Three tiers</h2>
{tier_table()}
<p class="fine">{E(PRICE_NOTE)} Every tier gets WhatsApp taps counted and reported to you, and no tier promises a number of enquiries or a ranking.</p>
<h2 style="margin-top:28px">What a free card looks like</h2>
<p>A Basic listing is a plain card with a short profile page. Here is a made-up example with a made-up name, so you can see the style.</p>
<div class="grid ex-grid">{free_card(depth)}</div>
<h2 style="margin-top:28px">What we need from you</h2>
<ul class="tick"><li>Your agreement in writing (WhatsApp is fine) and permission to use your photos</li><li>Business name, area, phone or WhatsApp, and the services you really offer</li><li>For Verified: your address, opening hours, a few photos of real jobs, and a review source we can link to</li></ul>
<h2>What we do not do</h2>
<p>We do not rank workshops, use rating or review markup, or list car dealers or insurers. A rating line is shown only when it comes from a source people can open, with its link and the date we checked. Anything we cannot confirm with you stays off the page.</p>
<section id="claim" class="claim-sec"><h2>Already listed? Manage your listing</h2>
<p>If your workshop is already on {E(SITE_NAME)}, message Page One to correct a detail, add your own photos, upgrade to Verified, or remove the listing. We check that you run the business before changing anything.</p>
<p class="claim-for" id="claim-for" hidden>Listing: <b></b></p>
<a class="btn amber big" id="claim-wa" href="{claim_generic}" data-names="{claim_names}" data-wa="{PAGE_ONE_WA}" data-site="{E(SITE_NAME)}" target="_blank" rel="noopener" data-cta="claim_owner_page">{WA_SVG} WhatsApp Page One</a>
<p class="fine">This WhatsApp is for workshop owners only. Customers, please use the WhatsApp button on the workshop's own listing.</p></section>
<div class="cta rv" style="margin-top:22px"><div><h2>Ask on WhatsApp</h2><p>Tell us what your workshop does and we will reply with the next step.</p></div>
<a class="btn amber big" href="{wa}" target="_blank" rel="noopener" data-cta="whatsapp_list_page">{WA_SVG} WhatsApp Page One</a></div>
</div>'''
    page('list-your-workshop/', 'List Your Car Workshop | SG Car Workshop',
         'Basic (free), Verified or Premium: compare the three ways to list your car workshop in Singapore.',
         body, [dict(crld, **{'@context': 'https://schema.org'})])


def about_page():
    depth = 1
    cr, crld = crumbs(depth, [('About', None)])
    body = f'''<div class="w nar">{cr}
<h1 style="margin-top:14px">About {E(SITE_NAME)}</h1>
<p class="lede" style="font-size:1rem">{E(SITE_NAME)} is a directory of car workshops and car services in Singapore, run by Page One Singapore, a web and SEO service for small businesses.</p>
<h2>How entries are checked</h2>
<p>Every fact on a page comes from the business or from its public records, and the business confirms it before the directory goes live. If a detail cannot be confirmed, such as a price or opening hours, we leave it out. We never copy a business's website text. We do not rank workshops or use rating markup; a rating line appears only with a source link and the date we checked.</p>
<h2>Who we list</h2>
<p>Car workshops and car services only: repair and servicing, gearbox, ABS and ECU modules, spray painting and bodywork, batteries, detailing and coating, wraps and PPF, and parts. Car dealers and insurance are not listed.</p>
<h2>A note on one listing</h2>
<p>SG Garage, a workshop in Ang Mo Kio, belongs to the founder of Page One Singapore. We list it like any other entry and say so here.</p>
<h2>Contact</h2>
<p>Page One Singapore is a project of Snap Commercial Pte. Ltd. (UEN 202209904W). To list a workshop or correct a page, WhatsApp {PAGE_ONE_WA_SHOW}.</p>
<div style="display:flex;flex-wrap:wrap;gap:10px"><a class="btn wa big" href="{E(list_wa(depth, 'general enquiry'))}" target="_blank" rel="noopener" data-cta="whatsapp_about">{WA_SVG} WhatsApp {PAGE_ONE_WA_SHOW}</a>
<a class="btn big" href="../list-your-workshop/">How listing works</a></div>
</div>'''
    page('about/', 'About SG Car Workshop | Run by Page One Singapore',
         'SG Car Workshop is a Singapore car workshop directory run by Page One Singapore. Details are confirmed by each business. Contact us on WhatsApp.',
         body, [dict(crld, **{'@context': 'https://schema.org'}), {'@context': 'https://schema.org', '@type': 'AboutPage', 'name': 'About ' + SITE_NAME, 'url': abs_url('about/')}])


def not_found():
    b = PATH_BASE
    cats = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (b, c['slug'], E(c['name'])) for c in CATEGORIES)
    out = f'''<!doctype html>
<html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Page not found | {E(SITE_NAME)}</title><meta name="robots" content="noindex">
<link rel="icon" href="{b}assets/favicon.ico" sizes="48x48"><link rel="stylesheet" href="{b}assets/dir.css?v={V}"></head>
<body><main class="w nar" style="padding:60px 16px"><h1>That page is not here</h1><p>The page may have moved. Try the <a href="{b}">home page</a> or pick a service.</p>
<ul class="tick">{cats}</ul><p><a class="btn amber" href="{b}">Back to {E(SITE_NAME)}</a></p></main></body></html>
'''
    return out


# ------------------------------------------------------------------ build
def build():
    home()
    for c in CAT_LIST:
        category(c)
    for k, r in REGION_LIST:
        region(k, r)
    for e in PAID:
        listing(e)
    for e in ENTRIES:
        if e['tier'] == 'free':
            basic_page(e)
    list_page()
    about_page()

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT + '/assets/img')
    for path, h in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(h)
    open(OUT + '/404.html', 'w', encoding='utf-8').write(not_found())
    for f in ('dir.css', 'dir.js'):
        shutil.copy(os.path.join(HERE, f), OUT + '/assets/' + f)
    shutil.copytree(os.path.join(HERE, 'img'), OUT + '/assets/img', dirs_exist_ok=True)
    make_icons()

    urls = sorted(PAGES)
    open(OUT + '/sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                                          ''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (abs_url(p), UPDATED) for p in urls) + '</urlset>\n')
    if LIVE:
        bots = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
        robots = ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots) + 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % BASE
    else:
        robots = 'User-agent: *\nDisallow: /\n'
    open(OUT + '/robots.txt', 'w').write(robots)
    lines = ['# %s' % SITE_NAME, '', '> A directory of car workshops and car services in Singapore, run by Page One Singapore. Entries use details confirmed by each business. No rankings and no rating or review markup.', '',
             'Last updated: %s' % UPDATED, '', '## Services']
    lines += ['- [%s](%sservices/%s/): %s' % (c['name'], BASE, c['slug'], c['blurb']) for c in CATEGORIES]
    lines += ['', '## Regions']
    lines += ['- [%s region](%sregions/%s/): %s' % (r['name'], BASE, k, r['intro']) for k, r in REGION_LIST]
    lines += ['', '## Listings']
    for e in ENTRIES:
        lines.append('- [%s](%sworkshops/%s/): %s, %s%s' % (e['name'], BASE, e['slug'], CAT[e['category']]['name'] + ', ' + TIERS[e['tier']]['label'], e['area_label'], (' (own website: %s)' % e['url']) if e['tier'] == 'premium_leadgen' else ''))
    lines += ['', '## More', '- [List your workshop](%slist-your-workshop/)' % BASE, '- [About](%sabout/)' % BASE, '']
    open(OUT + '/llms.txt', 'w').write('\n'.join(lines))
    print('built %d pages + 404 into %s (LIVE=%s, v=%s)' % (len(PAGES), OUT, LIVE, V))


def make_icons():
    """Favicon, app icons and default share image, drawn with Pillow (no external files)."""
    from PIL import ImageDraw, ImageFont

    def mark(sz, bg=True):
        """Pin + hex nut mark, drawn 8x large then scaled down for smooth edges."""
        S = 8
        k = sz * S / 48.0
        im = Image.new('RGBA', (sz * S, sz * S), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        if bg:
            d.rounded_rectangle([0, 0, sz * S - 1, sz * S - 1], radius=int(12 * k), fill='#0f1c33')
        gold, navy = '#d4a64a', '#0f1c33'
        d.ellipse([12 * k, 8 * k, 36 * k, 32 * k], fill=gold)
        d.polygon([(14.1 * k, 27.3 * k), (33.9 * k, 27.3 * k), (24 * k, 41.5 * k)], fill=gold)
        d.polygon([(24 * k, 13.2 * k), (29.9 * k, 16.6 * k), (29.9 * k, 23.4 * k), (24 * k, 26.8 * k), (18.1 * k, 23.4 * k), (18.1 * k, 16.6 * k)], fill=navy)
        d.ellipse([21.4 * k, 17.4 * k, 26.6 * k, 22.6 * k], fill=gold)
        im = im.resize((sz, sz), Image.LANCZOS)
        if bg:
            out = Image.new('RGB', (sz, sz), '#ffffff')
            out.paste(im, mask=im.split()[3])
            return out
        return im
    mark(192).save(OUT + '/assets/icon-192.png')
    mark(180).save(OUT + '/assets/apple-touch-icon.png')
    mark(48).save(OUT + '/assets/favicon.ico', sizes=[(48, 48)])
    W, H = 1200, 630
    im = Image.new('RGB', (W, H), '#0f1c33')
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(15 + 10 * t), int(28 + 20 * t), int(51 + 40 * t)))
    def font(bold, size):
        for f in (('/usr/share/fonts/opentype/inter/Inter-ExtraBold.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf') if bold else
                  ('/usr/share/fonts/opentype/inter/Inter-Regular.otf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')):
            try:
                return ImageFont.truetype(f, size)
            except OSError:
                pass
        return ImageFont.load_default()
    m = mark(150, bg=False)
    im.paste(m, (80, 150), m)
    fb, fs = font(True, 76), font(False, 34)
    d.text((260, 170), 'SG', font=fb, fill='#d4a64a')
    d.text((260 + d.textlength('SG ', font=fb), 170), 'Car Workshop', font=fb, fill='white')
    d.text((262, 270), 'Singapore car workshop directory', font=fs, fill='#cdd5e6')
    d.rounded_rectangle([80, 420, 1120, 422], radius=1, fill='#2a3c5f')
    d.text((80, 455), 'Find a workshop by service and area. WhatsApp them directly.', font=font(False, 30), fill='#d4a64a')
    im.save(OUT + '/assets/img/og-default.jpg', quality=85)


if __name__ == '__main__':
    build()
