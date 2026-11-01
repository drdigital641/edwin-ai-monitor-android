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
import areas  # noqa: E402
from data import ENTRIES, CATEGORIES, PAGE_ONE_WA, PAGE_ONE_WA_SHOW, TIERS, PRICE_NOTE, FREE_EXAMPLE  # noqa: E402
from PIL import Image  # noqa: E402

SITE_NAME = 'SG Car Workshop'   # placeholder brand
DOMAIN = 'sgcarworkshop.sg'     # not bought yet
LIVE = False
# Browser key (Edwin, 1 Nov 2026): restricted to pageonesingapore.com referrers and Places API (New) only, so safe to ship in page source.
GOOGLE_MAPS_KEY = 'AIzaSyAkMQs46QK9N2fiAqc1dmZch39hPHMzsnU'
PREVIEW_BASE = 'https://pageonesingapore.com/preview/sgcarworkshop/'
BASE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW_BASE
PATH_BASE = '/' if LIVE else '/preview/sgcarworkshop/'
UPDATED = '2026-11-01'
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'site'))
E = html.escape
CAT = {c['slug']: c for c in CATEGORIES}
ENT = {e['slug']: e for e in ENTRIES}
PAID = [e for e in ENTRIES if e['tier'] != 'free']
CAT_LIST = [c for c in CATEGORIES if any(e['category'] == c['slug'] for e in ENTRIES)]
RN = areas.REGION_NAMES
ESTATES = areas.ESTATES
areas.annotate(ENTRIES)
PUB_REGIONS = PUB_ESTATES = PUB_PAIRS = None   # filled by setup_areas()


def setup_areas():
    """Decide which area pages exist: a region with a listing, an estate with 1+ listings, a service x estate pair with 2+."""
    global PUB_REGIONS, PUB_ESTATES, PUB_PAIRS
    PUB_REGIONS, PUB_ESTATES, PUB_PAIRS = areas.published(ENTRIES)


setup_areas()

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
    reg = ''.join('<li><a href="%sareas/%s/">%s</a></li>' % (p, k, E(RN[k])) for k in PUB_REGIONS)
    est = ''.join('<li><a href="%sareas/%s/">%s</a></li>' % (p, k, E(ESTATES[k]['name'])) for k in PUB_ESTATES)
    return ('<a class="skip" href="#main">Skip to content</a><header class="top"><div class="w bar"><a class="brand" href="%s" aria-label="%s home">%s<span class="wm"><span><b>SG</b> Car Workshop</span><small>Singapore car workshop directory</small></span></a>'
            '<details class="menu"><summary aria-label="Menu">%s<span>Menu</span></summary><nav class="mpanel" aria-label="Main">'
            '<a class="mfind" href="%s#find">%s Find a workshop</a>'
            '<div class="mcols"><div class="svc-col"><h3>Services</h3><ul>%s</ul></div><div><h3>Regions</h3><ul>%s</ul></div><div><h3>Estates</h3><ul>%s</ul></div></div>'
            '<a class="mabout" href="%sabout/">About</a></nav></details></div></header>') % (p, E(SITE_NAME), LOGO, ic('menu'), p, ic('search'), svc, reg, est, p)


def footer(depth):
    p = pre(depth)
    cats = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (p, c['slug'], E(c['short'])) for c in CAT_LIST)
    reg = ''.join('<li><a href="%sareas/%s/">%s</a></li>' % (p, k, E(RN[k])) for k in PUB_REGIONS)
    est = ''.join('<li><a href="%sareas/%s/">%s</a></li>' % (p, k, E(ESTATES[k]['name'])) for k in PUB_ESTATES)
    return ('<footer class="ft"><div class="w cols"><div><h3>%s</h3><p>A directory of car workshops and car services in Singapore, run by '
            '<a href="https://pageonesingapore.com/" rel="noopener">Page One Singapore</a>.</p><p class="fine">'
            'WhatsApp taps are counted and reported to the business. This is a preview and the brand name is a placeholder.</p></div>'
            '<div><h3>Services</h3><ul>%s</ul></div><div><h3>Regions</h3><ul>%s</ul><h3 class="h3b">Estates</h3><ul>%s</ul></div>'
            '<div><h3>Directory</h3><ul><li><a href="%sabout/">About</a></li><li><a href="%slist-your-workshop/">List your workshop</a></li>'
            '<li><a href="%slist-your-workshop/#remove">Remove my listing</a></li><li><a href="%sllms.txt">llms.txt</a></li></ul></div></div></footer>') % (E(SITE_NAME), cats, reg, est, p, p, p, p)


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
        ('What is %s?' % SITE_NAME, 'A directory of car workshops and car services in Singapore. Each entry shows what the business does, where it is and how to contact it, using details from the business or its public listing.'),
        ('How do I contact a workshop?', 'Tap WhatsApp or Call on a card. The WhatsApp message is prefilled with the workshop name and says you found them on %s, so you only need to add your car and what you need.' % SITE_NAME),
        ('Do you rank or review workshops?', 'No. Entries are not ranked and we do not write reviews. Profile pages may show a rating line from a source people can open, with its link and the date we checked.'),
        ('How can I browse by area?', 'Pick a region (North, North-East, East, West, Central, or Mobile for services that come to you) in the search panel, or open an estate page such as Kaki Bukit or Yishun to see the workshops in that industrial area, a map and nearby areas.'),
    ]
    faq_html = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in faqs)
    svc_opts = '<label class="opt"><input type="radio" name="svc" value="" checked><span>Any service</span></label>' + ''.join(
        '<label class="opt"><input type="radio" name="svc" value="%s"><span>%s</span></label>' % (c['slug'], E(c['short'])) for c in CAT_LIST)
    reg_opts = ''.join('<label class="opt"><input type="checkbox" name="reg" value="%s"><span>%s</span></label>' % (k, E('Mobile' if k == 'mobile' else RN[k])) for k in PUB_REGIONS)
    svc_tiles = ''.join('<li><a href="services/%s/"><span class="ti">%s</span><span><b>%s</b><small>%d listing%s</small></span></a></li>' % (
        c['slug'], ic(c['icon']), E(c['short']), n, '' if n == 1 else 's') for c in CAT_LIST for n in [sum(1 for e in ENTRIES if e['category'] == c['slug'])])
    reg_tiles = ''.join('<li><a href="areas/%s/"><span class="ti">%s</span><span><b>%s</b><small>%d listing%s</small></span></a></li>' % (
        k, ic('pin'), E(RN[k]), n, '' if n == 1 else 's') for k in PUB_REGIONS for n in [sum(1 for e in ENTRIES if e['region'] == k)])
    est_tiles = ''.join('<li><a href="areas/%s/"><span class="ti">%s</span><span><b>%s</b><small>%s &middot; %d listing%s</small></span></a></li>' % (
        k, ic('pin'), E(ESTATES[k]['name']), E(RN[ESTATES[k]['region']]), len(v), '' if len(v) == 1 else 's') for k, v in PUB_ESTATES.items())
    tiers = tiers_strip()
    body = f'''<section class="finder" id="find"><div class="w"><div class="hero-t"><h1>Find a car workshop in Singapore</h1>
<p>Search by service and area, then message the workshop directly on WhatsApp.</p></div>
<p class="nojs">Browse by <a href="#services">service</a> or <a href="#regions">area</a> below.</p>
<form class="panel" id="finder" role="search" aria-label="Find a workshop" onsubmit="return false">
<p class="shint" id="shint"><span class="pt" aria-hidden="true">&#128070;</span> Tap and type what you need and where, in any order</p>
<label class="q"><span class="skip">Search workshops by service, area or name</span>{ic('search')}<input id="q" type="search" placeholder="e.g. gearbox repair Woodlands" autocomplete="off" autocapitalize="off" enterkeyhint="search"></label>
<div class="frow"><span class="lab" id="lab-s">Service <small>optional</small></span><div class="opts" role="radiogroup" aria-labelledby="lab-s">{svc_opts}</div></div>
<div class="frow"><span class="lab" id="lab-r">Region <small>optional, choose one or more</small></span><div class="opts" role="group" aria-labelledby="lab-r">{reg_opts}</div></div>
<div class="fbar"><p id="count" aria-live="polite"><b>{len(ENTRIES)}</b> workshops</p><button type="button" class="linkbtn" id="reset">Clear</button></div>
</form></div></section>
<section class="feat" aria-roledescription="carousel" aria-label="Featured Premium workshops"><div class="w"><div class="sec-h"><h2>Featured Premium workshops <span class="spons">Sponsored</span></h2>
<div class="car-nav"><button type="button" id="cprev" aria-label="Previous">{ic('chev-l')}</button><button type="button" id="cnext" aria-label="Next">{ic('chev-r')}</button></div></div>
<div class="marq" id="marq"><ul class="track" id="track" aria-label="Featured workshops">{slides}</ul></div></div></section>
<section id="workshops" class="lst"><div class="w"><div class="sec-h"><h2>All workshops</h2><a class="sec-link" href="#services">Browse by service</a></div><p class="fine adnote">Premium and Verified listings are paid and shown first (sponsored). Basic listings are free and compiled from public Google data.</p><div class="grid" id="results">{cards}</div>
<div class="empty" id="empty"><b>No workshops match.</b> Try fewer filters, or <a href="list-your-workshop/">list your workshop</a>.</div></div></section>
<section class="alt" id="services"><div class="w"><h2>Browse by service</h2><ul class="tiles">{svc_tiles}</ul></div></section>
<section id="regions"><div class="w"><h2>Browse by area</h2><ul class="tiles rg">{reg_tiles}</ul><h3 class="sub-h">Estates and industrial areas</h3><ul class="tiles est">{est_tiles}</ul></div></section>
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
    page('services/%s/' % c['slug'], '%s in Singapore | %s' % (c['name'], SITE_NAME), c['blurb'] + ' Browse Singapore listings by area.',
         body, [itemlist, dict(crld, **{'@context': 'https://schema.org'})], h1=c['name'])


def cap(t, n):
    t = ' '.join(t.split())
    if len(t) <= n:
        return t
    return t[:n - 1].rsplit(' ', 1)[0].rstrip(',;:.') + '.'


def and_list(items):
    items = list(items)
    return items[0] if len(items) == 1 else ', '.join(items[:-1]) + ' and ' + items[-1]


def fit_title(*options):
    for o in options:
        if len(o) <= 60:
            return o
    return options[-1][:60]


def itemlist_ld(name, es):
    return {'@context': 'https://schema.org', '@type': 'ItemList', 'name': name, 'numberOfItems': len(es),
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': abs_url('workshops/%s/' % e['slug']), 'name': e['name']} for i, e in enumerate(es)]}


def area_tile(depth, k, sub):
    return '<li><a href="%sareas/%s/"><span class="ti">%s</span><span><b>%s</b><small>%s</small></span></a></li>' % (pre(depth), k, ic('pin'), E(sub[0]), E(sub[1]))


def region(slug):
    """Level 1: /areas/<region>/"""
    depth = 2
    name = RN[slug]
    es = [e for e in ENTRIES if e['region'] == slug]
    mobile = slug == 'mobile'
    h1 = 'Mobile car services across Singapore' if mobile else 'Car workshops in the %s region' % name
    cr, crld = crumbs(depth, [(name, None)])
    est = [(k, v) for k, v in PUB_ESTATES.items() if ESTATES[k]['region'] == slug and any(e['region'] == slug for e in v)]
    tiles = ''.join(area_tile(depth, k, (ESTATES[k]['name'], '%d listing%s' % (len(v), '' if len(v) == 1 else 's'))) for k, v in est)
    est_html = '<section class="alt"><div class="w"><h2>Estates and industrial areas</h2><ul class="tiles est">%s</ul></div></section>' % tiles if tiles else ''
    mob_note = ''
    if not mobile and 'mobile' in PUB_REGIONS:
        mob_note = '<p class="fine" style="margin-top:14px">Looking for a service that comes to you? See <a href="%sareas/mobile/">mobile car services across Singapore</a>.</p>' % pre(depth)
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:14px"><div class="w"><h1>{E(h1)}</h1><p class="lede">{E(areas.REGION_INTRO[slug])}</p></div></section>
{est_html}
<section><div class="w"><h2>{'Mobile listings' if mobile else 'All workshops in the %s region' % E(name)}</h2><div class="grid">{''.join(card(e, depth, 'areas/%s/' % slug) for e in es)}{list_card(depth, 'car workshop' if mobile else 'car workshop in the ' + name + ' region')}</div>{mob_note}</div></section>'''
    title = fit_title('Mobile Car Services in Singapore | %s' % SITE_NAME) if mobile else fit_title('Car Workshops in %s Singapore | %s' % (name, SITE_NAME), 'Car Workshops in %s | %s' % (name, SITE_NAME))
    desc = ('Mobile car services that come to your car anywhere in Singapore, such as onsite batteries and mobile detailing. Message them directly.' if mobile else
            'Car workshops and car services in the %s region of Singapore, with estate pages and direct WhatsApp or call contact.' % name)
    page('areas/%s/' % slug, title, cap(desc, 160), body, [itemlist_ld(h1, es), dict(crld, **{'@context': 'https://schema.org'})], h1=h1)


def estate(slug, es):
    """Level 2: /areas/<estate>/  (main local SEO page)"""
    depth = 2
    a = ESTATES[slug]
    rname = RN[a['region']]
    cr, crld = crumbs(depth, [(rname, 'areas/%s/' % a['region']), (a['name'], None)])
    n = len(es)
    intro = '%s %s lists %d workshop%s here: %s.' % (a['intro'], SITE_NAME, n, '' if n == 1 else 's', and_list(e['name'] for e in es))
    svc_pairs = [(c, v) for (s_, c), v in PUB_PAIRS.items() if s_ == slug]
    chips = ''
    if svc_pairs:
        chips = '<ul class="chips" aria-label="Browse by service in %s">%s</ul>' % (E(a['name']), ''.join(
            '<li><a href="%s/">%s%s (%d)</a></li>' % (c, ic(CAT[c]['icon']), E(CAT[c]['short']), len(v)) for c, v in svc_pairs))
    lat, lon = a['lat'], a['lon']
    bbox = '%.4f,%.4f,%.4f,%.4f' % (lon - 0.011, lat - 0.007, lon + 0.011, lat + 0.007)
    map_src = 'https://www.openstreetmap.org/export/embed.html?bbox=%s&layer=mapnik&marker=%.4f%%2C%.4f' % (bbox, lat, lon)
    map_big = 'https://www.openstreetmap.org/?mlat=%.4f&mlon=%.4f#map=15/%.4f/%.4f' % (lat, lon, lat, lon)
    near = [k for k in a['nearby'] if k in PUB_ESTATES]
    near_tiles = ''.join(area_tile(depth, k, (ESTATES[k]['name'], '%s \u00b7 %d listing%s' % (RN[ESTATES[k]['region']], len(PUB_ESTATES[k]), '' if len(PUB_ESTATES[k]) == 1 else 's'))) for k in near)
    near_tiles += area_tile(depth, a['region'], ('All of the %s region' % rname, 'Region page'))
    cats = and_list(dict.fromkeys(CAT[e['category']]['name'] for e in es))
    faqs = [
        ('Which car workshops are in %s?' % a['name'], '%s currently lists %d workshop%s in %s: %s. Each has its own page with services, address and contact details.' % (SITE_NAME, n, '' if n == 1 else 's', a['name'], and_list(e['name'] for e in es))),
        ('What car services can I find in %s?' % a['name'], 'Listings here cover %s. Open a workshop page to see the services it lists.' % cats.lower()),
        ('How do I contact a workshop in %s?' % a['name'], 'Tap WhatsApp or Call on a workshop card or page. WhatsApp messages are prefilled with the workshop name and say you found them on %s, so you only need to add your car and what you need. Some listings show Call only.' % SITE_NAME),
        ('Which region is %s in?' % a['name'], '%s is in the %s region of Singapore.%s Browse the <a href="%sareas/%s/">%s region page</a> for more workshops.' % (
            a['name'], rname, (' Nearby areas on %s: %s.' % (SITE_NAME, and_list(ESTATES[k]['name'] for k in near))) if near else '', pre(depth), a['region'], E(rname))),
    ]
    faq_html = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), t if '<a ' in t else E(t)) for q, t in faqs)
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:14px"><div class="w"><h1>Car workshops in {E(a['name'])}</h1><p class="lede">{E(intro)}</p>{chips}</div></section>
<section><div class="w"><h2>Workshops in {E(a['name'])}</h2><div class="grid">{''.join(card(e, depth, 'areas/%s/' % slug) for e in es)}{list_card(depth, 'car workshop in ' + a['name'])}</div></div></section>
<section class="alt"><div class="w"><h2>Map of {E(a['name'])}</h2>
<div class="mapbox"><iframe src="{E(map_src)}" title="Map of {E(a['name'], True)}" loading="lazy" referrerpolicy="no-referrer"></iframe></div>
<p class="fine">Approximate area map from OpenStreetMap. <a href="{E(map_big)}" target="_blank" rel="noopener">View a larger map</a>. Use the Directions button on a workshop for its exact address.</p></div></section>
<section><div class="w"><h2>Nearby areas</h2><ul class="tiles est">{near_tiles}</ul></div></section>
<section class="alt"><div class="w nar"><h2>Questions about {E(a['name'])}</h2>{faq_html}</div></section>'''
    title = fit_title('Car Workshops in %s | %s' % (a['name'], SITE_NAME), '%s Car Workshops | %s' % (a['name'], SITE_NAME), 'Car Workshops in %s' % a['name'])
    desc = 'Find car workshops in %s, %s region, Singapore: %s. Map, nearby areas and direct WhatsApp or call contact.' % (a['name'], rname, cats.lower())
    ld = [itemlist_ld('Car workshops in %s' % a['name'], es), dict(crld, **{'@context': 'https://schema.org'})]
    page('areas/%s/' % slug, title, cap(desc, 160), body, ld, h1='Car workshops in %s' % a['name'])


def estate_service(slug, cat, es):
    """Level 3: /areas/<estate>/<service>/  (only built when 2 or more workshops match)"""
    depth = 3
    a = ESTATES[slug]
    c = CAT[cat]
    rname = RN[a['region']]
    cr, crld = crumbs(depth, [(rname, 'areas/%s/' % a['region']), (a['name'], 'areas/%s/' % slug), (c['name'], None)])
    n = len(es)
    h1 = '%s in %s' % (c['name'], a['name'])
    intro = '%d workshops in %s are listed for %s: %s. Each page shows the address, hours and how to contact the workshop.' % (n, a['name'], c['name'].lower(), and_list(e['name'] for e in es))
    body = f'''<div class="w">{cr}</div>
<section class="hero" style="padding-top:14px"><div class="w"><h1>{E(h1)}</h1><p class="lede">{E(intro)}</p></div></section>
<section><div class="w"><div class="grid">{''.join(card(e, depth, 'areas/%s/%s/' % (slug, cat)) for e in es)}</div>
<p class="fine" style="margin-top:14px">More in this area: <a href="../">all workshops in {E(a['name'])}</a>, or <a href="{pre(depth)}services/{cat}/">{E(c['name'].lower())} across Singapore</a>.</p></div></section>'''
    title = fit_title('%s in %s | %s' % (c['name'], a['name'], SITE_NAME), '%s in %s' % (c['name'], a['name']))
    desc = '%s in %s, %s region: %s. Compare listings and contact a workshop directly.' % (c['name'], a['name'], rname, and_list(e['name'] for e in es))
    page('areas/%s/%s/' % (slug, cat), title, cap(desc, 160), body, [itemlist_ld(h1, es), dict(crld, **{'@context': 'https://schema.org'})], h1=h1)


def tier_badge(e_or_tier, cls=''):
    t = e_or_tier if isinstance(e_or_tier, str) else e_or_tier['tier']
    return '<span class="tier t-%s%s">%s</span>' % (t, (' ' + cls) if cls else '', E(TIERS[t]['badge']))


ASK = {'sonic-auto-garage': 'servicing or repair for my car', 'allen-motor-workshop': 'servicing or repair for my car', 'jss-motorworkz': 'servicing or repair for my car', 'everest-garage': 'servicing or repair for my car', 'hup-soon-lee-motor-service': 'servicing or repair for my car', 'cys-automobile-services': 'servicing or repair for my car', 'sg-garage': 'my car', 'cleanic-detailing': 'cleaning or fumigation for my car', 'autotex': 'a part for my car',
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


def live_contact(e, page_path, cls=''):
    """Basic contact button. The phone number is NOT stored: dir.js loads it live from Google Places and turns this into WhatsApp (mobile) or Call.
    Until then (or if Places fails) it is a plain link to the Google listing."""
    msg = "Hi %s, I found you on %s (%s). I'd like to ask about %s." % (e['name'], SITE_NAME, page_label(page_path), ASK.get(e['slug'], 'my car'))
    return ('<a class="btn wa live%s" href="%s" target="_blank" rel="noopener" data-live="contact" data-wa-msg="%s" data-cta="contact_dir_%s" data-tier="free" data-page="%s">'
            '<span class="ic-wa" hidden>%s</span><span class="ic-call">%s</span> <span class="lbl">Contact on Google</span></a>') % (
        (' ' + cls) if cls else '', E(maps_url(e)), E(msg, True), e['slug'], E(page_label(page_path)), WA_SVG, ic('phone'))


def photo_img(p, depth, lazy=True, cls=''):
    if p.get('f'):
        return img_tag(p['f'], p['alt'], depth, lazy=lazy, cls=cls)
    return '<img src="%s" alt="%s"%s decoding="async" referrerpolicy="no-referrer"%s>' % (
        E(p['u'], True), E(p['alt'], True), ' loading="lazy"' if lazy else '', (' class="%s"' % cls) if cls else '')


def tile(e):
    return '<div class="tile" aria-hidden="true">%s<b>%s</b><span>%s</span></div>' % (ic(CAT[e['category']]['icon']), E(e['name']), E(e.get('tile_text', CAT[e['category']]['short'])))


def region_label(e):
    if e['region'] == 'mobile':
        return 'Mobile \u00b7 island-wide'
    return '%s \u00b7 %s' % (e['area_label'], RN[e['region']])


def area_link_html(e, up):
    """' or workshops in <Estate>' / ' or mobile services' link for the foot of a workshop page."""
    if e['region'] == 'mobile':
        return ' or <a href="%sareas/mobile/">other mobile services</a>' % up
    k = e['estates'][0]
    return ' or <a href="%sareas/%s/">workshops in %s</a>' % (up, k, E(ESTATES[k]['name']))


def workshop_trail(e):
    """Home > Region > Estate > Workshop (mobile services: Home > Mobile > Workshop)."""
    t = [(RN[e['region']], 'areas/%s/' % e['region'])]
    if e['estates']:
        k = e['estates'][0]
        t.append((ESTATES[k]['name'], 'areas/%s/' % k))
    return t + [(e['name'], None)]


def call_icon(e, page_path):
    return '<a class="btn sm ico" href="tel:%s" aria-label="Call %s" %s>%s</a>' % (e['phone'], E(e['name'], True), track_attrs('call', e, page_path), ic('phone'))


def owner_note(e, depth, page_path, cls='owner-note'):
    """Small grey line for business owners. Links to the owner section of the listing page, never to a WhatsApp,
    so customers only ever see the workshop's own WhatsApp on a listing."""
    rm = (' <span class="sep">&middot;</span> <a class="rm" href="%slist-your-workshop/?w=%s#remove" data-cta="remove_%s" data-page="%s">Remove my listing</a>'
          % (pre(depth), e['slug'], e['slug'], E(page_label(page_path)))) if e['tier'] == 'free' else ''
    return ('<p class="%s">For business owners: Is this your workshop? <a href="%slist-your-workshop/?w=%s#claim" data-cta="claim_%s" data-page="%s">Manage this listing &rarr;</a>%s</p>'
            % (cls, pre(depth), e['slug'], e['slug'], E(page_label(page_path)), rm))


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


def gph_attrs(e):
    """Basic photos load live from Google Places (New) in the browser; nothing is self-hosted. Listings without a stored place_id are found by name + address."""
    ad = (e.get('addresses') or [{}])[0]
    q = '%s %s Singapore %s' % (e['name'], ad.get('street', ''), ad.get('postal', ''))
    return 'data-place="%s" data-q="%s" data-name="%s" data-maps="%s"' % (E(e.get('place_id', '')), E(q, True), E(e['name'], True), E(maps_url(e), True))


def gph_tile(e):
    return '<div class="tile ini" aria-hidden="true"><b>%s</b></div>' % E(e['name'][0])


def maps_url(e):
    """Google Maps link for a Basic listing: by cid when we have it, else by place_id."""
    if e.get('cid'):
        return 'https://www.google.com/maps?cid=%s' % e['cid']
    return 'https://www.google.com/maps/search/?api=1&query=%s&query_place_id=%s' % (quote(e['name']), e['place_id'])


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
        acts = live_contact(e, page_path, 'sm')
        acts += '<span class="minor"><a class="btn sm ghost" href="%s" target="_blank" rel="noopener" data-cta="directions_%s">Directions</a>' % (E(maps_url(e)), e['slug'])
        acts += '<a class="btn sm ghost" href="%sworkshops/%s/" data-cta="view_%s">View</a></span>' % (pre(depth), e['slug'], e['slug'])
        return ('<article class="card basic" %s><div class="ph gph" %s>%s%s</div><div class="bd"><span class="tag">%s</span>'
                '<h3><a href="%sworkshops/%s/">%s</a></h3>%s<p class="tx full">%s</p><div class="acts">%s</div>'
                '%s</div></article>') % (
            attrs, gph_attrs(e), gph_tile(e), tier_badge(e, 'on-ph'), E(c['short']), pre(depth), e['slug'], E(e['name']), rg, E(e['desc']), acts, owner_note(e, depth, page_path, 'claim'))
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
    if e['region'] == 'mobile':
        ld['areaServed'] = {'@type': 'Country', 'name': 'Singapore'}
    else:
        ld['areaServed'] = [{'@type': 'Place', 'name': ESTATES[k]['name'] + ', Singapore'} for k in e['estates']]
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
    cr, crld = crumbs(depth, workshop_trail(e))
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
    area_links = area_link_html(e, '../../')
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
<p class="fine">Last updated {UPDATED}. Browse more <a href="../../services/{c['slug']}/">{E(c['name'].lower())}</a> listings{area_links}.</p>
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
    cr, crld = crumbs(depth, workshop_trail(e))
    gurl = maps_url(e)
    contact_btn = live_contact(e, path, 'big')
    photo = '<div class="hero-ph gph" %s>%s</div>' % (gph_attrs(e), gph_tile(e))
    svcs = ''.join('<li>%s</li>' % E(s) for s in e['services_public'])
    hours = '<p class="fine" data-live="hours">See opening hours on the <a href="%s" target="_blank" rel="noopener">Google listing</a>.</p>' % E(gurl)
    reviews = '<p class="reviews-line" data-live="rating">%s <a href="%s" target="_blank" rel="noopener" data-cta="reviews_%s" data-tier="free" data-page="%s">See the Google rating and reviews</a></p>' % (
        ic('shield'), E(gurl), e['slug'], E(page_label(path)))
    claim = owner_note(e, depth, path)
    area_links = area_link_html(e, '../../')
    site_btn = ' <a class="btn ghost" href="#" hidden target="_blank" rel="noopener" data-live="site" data-cta="website_%s" data-tier="free">%s <span class="lbl">Website</span></a>' % (e['slug'], ic('out'))
    body = f'''<div class="w nar basicpg">{cr}
<div class="badges" style="margin-top:14px">{tier_badge(e)}<span class="tag">{E(c['short'])}</span></div>
<h1 style="margin-top:8px">{E(e['name'])}</h1>
<p class="meta rg">{ic('pin')}<span>{E(region_label(e))}</span></p>
{photo}
<p class="lede" style="font-size:1rem">{E(e['lede'])}</p>
<p>{E(e['area_ctx'])}</p>
<div class="acts main-acts">{contact_btn}</div>
<p class="fine">The button opens a chat that you start, using the number the business publishes on its Google listing. We never message workshops.</p>
<h2>Services</h2>
<ul class="tick svc-plain">{svcs}</ul>
<p class="fine">From the workshop's Google listing.</p>
<section id="find" class="findus"><h2>Find us</h2>
<ul class="facts"><li data-addr>{ic('pin')}<span>{E(e['address_public'])}</span></li><li data-live="phoneline">{ic('phone')}<span>Phone number on the <a href="{E(gurl)}" target="_blank" rel="noopener">Google listing</a></span></li></ul>
<p style="margin:10px 0"><a class="btn" href="{gurl}" target="_blank" rel="noopener" data-cta="directions_{e['slug']}" data-tier="free" data-page="{E(page_label(path))}" data-map>{ic('pin')} Directions</a>{site_btn}</p>
<h3>Opening hours</h3>{hours}
</section>
{reviews}
<p class="fine">Phone, opening hours and rating are shown live from Google. More <a href="../../services/{c['slug']}/">{E(c['name'].lower())}</a>{area_links}.</p>
{claim}
</div>'''
    _m = re.search(r'^(.*?)[, ]+(?:Singapore\s+)?(\d{6})\s*$', e['address_public'])
    street, postal = (_m.group(1), _m.group(2)) if _m else (e['address_public'], '')
    ld = {'@context': 'https://schema.org', '@type': 'AutoRepair', 'name': e['name'], 'url': url,
          'address': {'@type': 'PostalAddress', 'streetAddress': street, 'postalCode': postal, 'addressLocality': 'Singapore', 'addressCountry': 'SG'},
          }
    bar = wabar([live_contact(e, path),
                 '<a class="btn" href="%s" target="_blank" rel="noopener" data-cta="directions_%s" data-tier="free" data-page="%s">%s Directions</a>' % (E(gurl), e['slug'], E(page_label(path)), ic('pin'))])
    desc = next(d for d in ('%s: car workshop in %s, %s region. Address, directions, and phone, hours and Google rating shown live from Google.' % (e['name'], e['area_label'], RN[e['region']]), '%s, car workshop in %s. Address, directions, phone, hours and Google rating.' % (e['name'], e['area_label']), '%s, car workshop in %s.' % (e['name'], e['area_label'])) if len(d) <= 160)
    page(path, fit_title('%s | %s Car Workshop' % (e['name'], e['area_label']), '%s | %s' % (e['name'], e['area_label']), e['name']), desc, body, [ld, dict(crld, **{'@context': 'https://schema.org'})], bar=bar, h1=e['name'])


def tier_features():
    return [
        ('Basic card and short profile page: name, short description, category, area, one Google photo', 'yes', 'yes', 'yes'),
        ('Link to your website', 'yes', 'yes', 'yes (shown as a secondary button)'),
        ('WhatsApp (or Call) button with the source tagged', 'yes', 'yes', 'yes'),
        ('Tap counts (WhatsApp and call) reported to you', 'yes', 'yes', 'yes'),
        ('Your own photos and a completed-job gallery', 'no', 'yes', 'yes'),
        ('Detailed services with short descriptions', 'no', 'yes', 'yes'),
        ('Address, Directions link and opening hours', 'yes', 'yes', 'yes'),
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
    remove_generic = E(wa_link(PAGE_ONE_WA, "Hi Page One, please remove my workshop listing from %s. Business name: \n\n(From %s)" % (SITE_NAME, BASE + 'list-your-workshop/')))
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
<p>We do not rank workshops, use rating or review markup, or list car dealers or insurers. A rating line is shown only when it comes from a source people can open, with its link and the date we checked.</p>
<section id="claim" class="claim-sec"><h2>Already listed? Manage your listing</h2>
<p>If your workshop is already on {E(SITE_NAME)}, message Page One to correct a detail, add your own photos, upgrade to Verified, or remove the listing. We check that you run the business before changing anything.</p>
<p class="claim-for" id="claim-for" hidden>Listing: <b></b></p>
<a class="btn amber big" id="claim-wa" href="{claim_generic}" data-names="{claim_names}" data-wa="{PAGE_ONE_WA}" data-site="{E(SITE_NAME)}" target="_blank" rel="noopener" data-cta="claim_owner_page">{WA_SVG} WhatsApp Page One</a>
<p class="fine">This WhatsApp is for workshop owners only. Customers, please use the WhatsApp button on the workshop's own listing.</p></section>
<section id="remove" class="claim-sec"><h2>Remove my listing</h2>
<p>Basic listings are compiled from public Google data and are not endorsed by or arranged with the business. If you run a workshop and want your listing taken down, send us a message and we will remove it. We check that you run the business first.</p>
<p class="claim-for" id="remove-for" hidden>Listing: <b></b></p>
<a class="btn big" id="remove-wa" href="{remove_generic}" data-names="{claim_names}" data-wa="{PAGE_ONE_WA}" data-site="{E(SITE_NAME)}" target="_blank" rel="noopener" data-cta="remove_owner_page">{WA_SVG} WhatsApp to remove my listing</a>
<p class="fine">This WhatsApp is for workshop owners only. You start the chat; we never message workshops first.</p></section>
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
<h2>Where the details come from</h2>
<p>Every fact on a page comes from the business or from its public records. If a detail cannot be verified, such as a price or opening hours, we leave it out. We never copy a business's website text. We do not rank workshops or use rating markup; a rating line appears only with a source link and the date we checked.</p>
<h2>Unclaimed listings</h2>
<p>Basic listings that the business has not claimed are compiled from public Google data. They are free, they are not endorsed by or arranged with the business, and they can be removed on request: use <a href="../list-your-workshop/#remove">Remove my listing</a>. Phone, opening hours and rating on these listings load live from Google. Verified and Premium listings are paid, signed-up businesses and are labelled as such.</p>
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
         'SG Car Workshop is a Singapore car workshop directory run by Page One Singapore. Contact us on WhatsApp.',
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
    for k in PUB_REGIONS:
        region(k)
    for k, v in PUB_ESTATES.items():
        estate(k, v)
    for (k, cat), v in PUB_PAIRS.items():
        estate_service(k, cat, v)
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
    write_redirects()
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
    lines = ['# %s' % SITE_NAME, '', '> A directory of car workshops and car services in Singapore, run by Page One Singapore. Entries use details from the business or its public listing. No rankings and no rating or review markup.', '',
             'Last updated: %s' % UPDATED, '', '## Services']
    lines += ['- [%s](%sservices/%s/): %s' % (c['name'], BASE, c['slug'], c['blurb']) for c in CATEGORIES]
    lines += ['', '## Areas (regions)']
    lines += ['- [%s](%sareas/%s/): %s' % (RN[k], BASE, k, areas.REGION_INTRO[k]) for k in PUB_REGIONS]
    lines += ['', '## Estates and industrial areas']
    lines += ['- [%s](%sareas/%s/): %s %d listing%s.' % (ESTATES[k]['name'], BASE, k, ESTATES[k]['intro'], len(v), '' if len(v) == 1 else 's') for k, v in PUB_ESTATES.items()]
    lines += ['', '## Listings']
    for e in ENTRIES:
        lines.append('- [%s](%sworkshops/%s/): %s, %s%s' % (e['name'], BASE, e['slug'], CAT[e['category']]['name'] + ', ' + TIERS[e['tier']]['label'], e['area_label'], (' (own website: %s)' % e['url']) if e['tier'] == 'premium_leadgen' else ''))
    lines += ['', '## More', '- [List your workshop](%slist-your-workshop/)' % BASE, '- [About](%sabout/)' % BASE, '']
    open(OUT + '/llms.txt', 'w').write('\n'.join(lines))
    print('built %d pages + 404 into %s (LIVE=%s, v=%s)' % (len(PAGES), OUT, LIVE, V))


OLD_REGIONS = ['north', 'north-east', 'east', 'west', 'central']


def write_redirects():
    """/regions/<r>/ moved to /areas/<r>/. The bridge cannot upload .htaccess, so the preview gets soft redirect pages
    (meta refresh + canonical). redirects.htaccess holds the real 301 rules for Edwin to add on the live domain."""
    for r in OLD_REGIONS:
        d = os.path.join(OUT, 'regions', r)
        os.makedirs(d, exist_ok=True)
        new = '../../areas/%s/' % r
        open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(
            '<!doctype html>\n<html lang="en-SG"><head><meta charset="utf-8"><title>Moved | %s</title>'
            '<link rel="canonical" href="%s"><meta http-equiv="refresh" content="0; url=%s"></head>'
            '<body><p>This page has moved to <a href="%s">%s</a>.</p></body></html>\n' % (E(SITE_NAME), E(abs_url('areas/%s/' % r)), new, new, E(RN[r] + ' region')))
    rules = ['# 301 redirects for the SG Car Workshop area restructure (1 Nov 2026). Add to the .htaccess at the root of the live domain.',
             '# The upload bridge cannot send .htaccess files, so this file is not part of the synced site folder.']
    rules += ['Redirect 301 /regions/%s/ /areas/%s/' % (r, r) for r in OLD_REGIONS]
    rules += ['Redirect 301 /regions/ /']
    open(os.path.join(HERE, '..', 'redirects.htaccess'), 'w').write('\n'.join(rules) + '\n')


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
