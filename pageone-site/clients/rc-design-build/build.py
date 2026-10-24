"""R&C - Retail & Commercial Design & Build: builds every page into site/ (python3 build.py).

New Edwin-owned brand, started 24 Oct 2026 from the brief in drdigital641/edwin-ai-context
(handoffs/2026-10-24-rc-design-build-project.md, copied to content/PROJECT-BRIEF.md).
Facts: there are none yet beyond the brand name, tagline and service scope in the brief. No address, UEN, team,
years, prices, reviews, warranties or completed projects exist, so none are published. Every image is an
AI design concept (generated 24 Oct 2026 with Base44 GenerateImage) and is labelled as such where shown.
Pending before LIVE (shown in dashed boxes on the preview): domain, operating entity + UEN, public contact
(WhatsApp number: Edwin chose "decide later" on 24 Oct 2026), who delivers the work, service area.

Env: RC_OUT (output dir), RC_IMG (image base URL, e.g. a local folder for screenshots).
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
sys.path.insert(0, os.path.join(HERE, 'content'))
import services as C_SVC  # noqa: E402
import avl as C_AVL  # noqa: E402
import spaces as C_SPC  # noqa: E402
import guides as C_GDE  # noqa: E402

OUT = os.environ.get('RC_OUT', os.path.join(HERE, 'site'))
SLUG = 'rc-design-build'
DOMAIN = ''            # final domain not chosen yet (brief section 13)
LIVE = False           # True only after Edwin's go-ahead and every PENDING item is confirmed
WA_NUMBER = ''         # digits only, e.g. '6591234567'; empty = honest "opening soon" state
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
BASE = ('https://%s/' % DOMAIN) if DOMAIN else PREVIEW
ASSET_SHA = '6958e99'
IMG = os.environ.get('RC_IMG') or ('https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@%s/site-assets/%s/' % (ASSET_SHA, SLUG))
TODAY = '2026-10-24'
INDEXNOW_KEY = '7d4c2a9e1f6b8035c4e2a7d9b1f60c38'
BRAND = 'R&C'
BRAND_FULL = 'R&C - Retail & Commercial Design & Build'
TAGLINE = 'Retail spaces. Commercial interiors. Built around your business.'

if LIVE:
    assert DOMAIN and WA_NUMBER, 'LIVE needs DOMAIN and WA_NUMBER confirmed'

PENDING = [
    ('Domain', 'Final website address not chosen yet.'),
    ('Operating company', 'Registered business name and UEN to be confirmed before launch.'),
    ('Enquiry line', 'WhatsApp number for R&C enquiries to be confirmed.'),
    ('Who delivers the work', 'Delivery arrangements to be confirmed before projects are taken on.'),
    ('Service area', 'Areas served to be confirmed.'),
]

# ---------- page registry ----------
SVC = {p['path']: p for p in C_SVC.PAGES}
AVLP = {p['path']: p for p in C_AVL.PAGES}
SPC = {p['path']: p for p in C_SPC.PAGES}
GDE = {p['path']: p for p in C_GDE.PAGES}
ALL_CONTENT = {}
for d in (SVC, AVLP, SPC, GDE):
    ALL_CONTENT.update(d)

SERVICE_ORDER = ['/retail-commercial-design-build/', '/services/commercial-carpentry/', '/services/commercial-renovation/',
                 '/services/commercial-electrical-works/', '/services/commercial-tiling-flooring/',
                 '/services/commercial-painting-finishing/']
SHORT = {
    '/retail-commercial-design-build/': 'Design & Build', '/services/commercial-carpentry/': 'Carpentry',
    '/services/commercial-renovation/': 'Renovation', '/services/commercial-electrical-works/': 'Electrical works',
    '/services/commercial-tiling-flooring/': 'Tiling & flooring', '/services/commercial-painting-finishing/': 'Painting & finishing',
    '/avl/': 'AVL overview', '/avl/commercial-audio-systems/': 'Audio systems', '/avl/display-visual-systems/': 'Displays & signage',
    '/avl/architectural-feature-lighting/': 'Feature lighting', '/spaces/retail-shops-boutiques/': 'Retail shops & boutiques',
    '/spaces/offices-showrooms/': 'Offices & showrooms', '/spaces/cafes-service-counters/': 'Cafes & service counters',
    '/spaces/salons-beauty-studios/': 'Salons & beauty studios', '/services/': 'Services', '/spaces/': 'Spaces',
    '/design-concepts/': 'Design concepts', '/guides/': 'Guides', '/about/': 'About', '/contact/': 'Contact',
    '/privacy-policy/': 'Privacy policy', '/': 'Home',
}
for p in GDE.values():
    SHORT[p['path']] = p['h1']

NAV = [('/retail-commercial-design-build/', 'Design & Build'), ('/services/', 'Services'), ('/avl/', 'AVL'),
       ('/spaces/', 'Spaces'), ('/design-concepts/', 'Concepts'), ('/guides/', 'Guides'), ('/about/', 'About'),
       ('/contact/', 'Contact')]

# ---------- helpers ----------
E = html.escape


def rel(frm, to):
    """Relative link from page path frm (a folder path) to path to, so the site works in /preview/<slug>/ and on a domain."""
    if to.startswith(('http', 'mailto:', 'tel:', '#')):
        return to
    depth = len([s for s in frm.strip('/').split('/') if s])
    r = '../' * depth + to.lstrip('/')
    return r or './'


def abs_url(path):
    return BASE + path.lstrip('/')


def fix_links(h, frm):
    return re.sub(r'href="(/[^"]*)"', lambda m: 'href="%s"' % rel(frm, m.group(1)), h)


def vhash(name):
    with open(os.path.join(HERE, name), 'rb') as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


def img_url(key, small=False):
    return IMG + key + ('-640' if small else '') + '.webp'


def pic(key, alt, cls='', eager=False, small=False, tag=True):
    w = 640 if small else 1024
    srcset = '%s 640w, %s 1024w' % (img_url(key, True), img_url(key))
    sizes = '(max-width: 700px) 92vw, 46vw' if not small else '(max-width: 600px) 92vw, 30vw'
    t = '<img src="%s" srcset="%s" sizes="%s" width="%d" height="%d" alt="%s"%s%s>' % (
        img_url(key, small), srcset, sizes, w, w, E(alt),
        ' loading="eager" fetchpriority="high"' if eager else ' loading="lazy"', ' decoding="async"')
    if tag:
        t += '<span class="tag">AI design concept</span>'
    return t


def wa_link(topic, frm):
    if not WA_NUMBER:
        return None
    msg = 'Hi R&C, I would like to discuss %s. (Page: %s, ref: website)' % (topic, frm)
    return 'https://wa.me/%s?text=%s' % (WA_NUMBER, quote(msg))


def cta(frm, topic='my space', label='Discuss Your Space', cls='btn btn-main'):
    w = wa_link(topic, frm)
    if w:
        return '<a class="%s" href="%s" rel="noopener">%s</a>' % (cls, E(w), label)
    return '<a class="%s" href="%s">%s</a>' % (cls, rel(frm, '/contact/'), label)


def pending_box(items=None, title='Pending before launch'):
    if LIVE:
        return ''
    items = items or PENDING
    return '<div class="pending"><b>%s (preview note)</b>%s</div>' % (
        E(title), '<br>'.join('%s: %s' % (E(a), E(b)) for a, b in items))


def faq_html(faqs):
    return '<div class="faq"><h2>Frequently asked questions</h2>%s</div>' % ''.join(
        '<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in faqs)


def faq_schema(faqs):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q,
            'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}


def org_schema():
    o = {'@type': 'Organization', '@id': BASE + '#org', 'name': BRAND_FULL, 'alternateName': BRAND, 'url': BASE,
         'logo': BASE + 'icon-512.png', 'slogan': TAGLINE,
         'description': 'Design and build for retail and commercial spaces in Singapore: carpentry, renovation, electrical works, '
                        'tiling and flooring, painting and finishing, and audio, visual and lighting (AVL).'}
    return o


def crumbs_html(frm, crumbs):
    li = ['<li><a href="%s">Home</a></li>' % rel(frm, '/')]
    for path, name in crumbs[:-1]:
        li.append('<li><a href="%s">%s</a></li>' % (rel(frm, path), E(name)))
    li.append('<li aria-current="page">%s</li>' % E(crumbs[-1][1]))
    return '<nav class="crumbs wrap" aria-label="Breadcrumb"><ol>%s</ol></nav>' % ''.join(li)


def crumbs_schema(crumbs):
    items = [('/', 'Home')] + list(crumbs)
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': abs_url(p)} for i, (p, n) in enumerate(items)]}


def card(frm, path, title, text, key, more='More details', small=True):
    return ('<a class="card rv" href="%s"><div class="ph">%s</div><div class="bd"><h3>%s</h3><p>%s</p>'
            '<span class="more">%s</span></div></a>') % (rel(frm, path), pic(key, title + ' (AI design concept)', small=small),
                                                        E(title), E(text), more)


def svc_tile(frm, path):
    p = ALL_CONTENT[path]
    return ('<a class="rv" href="%s"><img src="%s" width="92" height="92" alt="" loading="lazy" decoding="async">'
            '<div><h3>%s</h3><p>%s</p><span class="more">More details</span></div></a>') % (
        rel(frm, path), img_url(p['image'], True), E(SHORT.get(path, p['h1'])), E(p['card']))


# ---------- layout ----------
def head(path, title, desc, schema, og_img=None):
    can = abs_url(path)
    og = og_img or (IMG + 'og-rc.jpg')
    ld = json.dumps({'@context': 'https://schema.org', '@graph': schema}, ensure_ascii=False).replace('</', '<\\/')
    r = rel(path, '/')
    return '''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%s</title>
<meta name="description" content="%s">
<link rel="canonical" href="%s">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#2b2925">
<link rel="icon" href="%sfavicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="192x192" href="%sicon-192.png">
<link rel="apple-touch-icon" href="%sapple-touch-icon.png">
<link rel="manifest" href="%ssite.webmanifest">
<link rel="preload" href="%sfonts/fraunces-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="%src.css?v=%s">
<meta property="og:type" content="website">
<meta property="og:site_name" content="%s">
<meta property="og:title" content="%s">
<meta property="og:description" content="%s">
<meta property="og:url" content="%s">
<meta property="og:image" content="%s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Small shop interior with oak shelving and cream walls (AI design concept)">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">%s</script>
</head>
''' % (E(title), E(desc), can, r, r, r, r, r, r, vhash('rc.css'), E(BRAND_FULL), E(title), E(desc), can, og, ld)


def header(path):
    links = ''.join('<a href="%s"%s>%s</a>' % (rel(path, p), ' aria-current="page"' if path == p or (p != '/' and path.startswith(p) and p in ('/services/', '/avl/', '/spaces/', '/guides/')) else '', E(n))
                    for p, n in NAV)
    return '''<body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="brand" href="%s"><img src="%sicon-192.png" width="38" height="38" alt=""><span>R&amp;C<small>Retail &amp; Commercial Design &amp; Build</small></span></a>
<nav class="nav" id="nav" aria-label="Main">%s</nav>
%s
<button class="menu-btn" type="button" aria-controls="nav" aria-expanded="false">Menu</button>
</div></header>
<main id="main">
''' % (rel(path, '/'), rel(path, '/'), links, cta(path, 'my space', 'Discuss Your Space'))


def footer(path):
    col = lambda paths: ''.join('<li><a href="%s">%s</a></li>' % (rel(path, p), E(SHORT[p])) for p in paths)
    return '''</main>
<footer class="foot"><div class="wrap">
<div><h3>R&amp;C</h3><p>%s</p><p>Design &amp; build for retail and commercial spaces in Singapore: carpentry, renovation, electrical, flooring, finishing and AVL.</p>%s</div>
<div><h3>Services</h3><ul>%s</ul></div>
<div><h3>AVL &amp; spaces</h3><ul>%s</ul></div>
<div><h3>Plan</h3><ul>%s</ul></div>
<p class="small">Images on this site are AI design concepts for discussion, not completed projects. &copy; 2026 %s.</p>
</div></footer>
<script src="%src.js?v=%s" defer></script>
<script src="%swa-tap-counter.js?v=%s" defer></script>
</body>
</html>
''' % (E(TAGLINE), pending_box([('Operating company', 'name and UEN to be confirmed'), ('Contact', 'enquiry line to be confirmed')]),
       col(SERVICE_ORDER), col(['/avl/', '/avl/commercial-audio-systems/', '/avl/display-visual-systems/', '/avl/architectural-feature-lighting/', '/spaces/retail-shops-boutiques/', '/spaces/cafes-service-counters/']),
       col(['/design-concepts/', '/guides/', '/about/', '/contact/', '/privacy-policy/']), E(BRAND_FULL),
       rel(path, '/'), vhash('rc.js'), rel(path, '/'), vhash('wa-tap-counter.js'))


def cta_band(path, topic):
    return ('<div class="wrap"><div class="cta-band rv"><div><h2>Planning a shop, office, cafe or salon space?</h2>'
            '<p>Send your floor plan, unit photos, intended use and target opening date, and we\'ll discuss your scope.</p></div>'
            '<div>%s</div></div></div>') % cta(path, topic, 'Discuss Your Space', 'btn btn-light')


PAGES_OUT = []  # (path, lastmod)


def write(path, doc, lastmod=TODAY):
    d = os.path.join(OUT, path.strip('/'))
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(doc)
    PAGES_OUT.append((path, lastmod))


# ---------- content pages ----------
def related_html(path, rels):
    out = []
    for r in rels:
        if r in SHORT:
            out.append('<li><a href="%s">%s</a></li>' % (rel(path, r), E(SHORT[r])))
    return ''.join(out)


def content_page(p, crumbs, kind='service'):
    path = p['path']
    schema = [org_schema(), crumbs_schema(crumbs), faq_schema(p['faqs'])]
    main_entity = {'@type': 'Article' if kind == 'guide' else 'Service', 'name': p['h1'], 'description': p['desc'],
                   'url': abs_url(path), 'image': img_url(p['image'])}
    if kind == 'guide':
        main_entity.update({'headline': p['h1'], 'datePublished': p['date'], 'dateModified': p['date'],
                            'author': {'@id': BASE + '#org'}, 'publisher': {'@id': BASE + '#org'}})
    else:
        main_entity.update({'provider': {'@id': BASE + '#org'}, 'serviceType': p['kicker']})
    schema.append(main_entity)
    secs = ''.join('<h2>%s</h2>%s' % (E(s['h2']), fix_links(s['html'], path)) for s in p['sections'])
    meta = ''
    if kind == 'guide':
        meta = '<p class="meta">Planning guide · %s · Published 24 October 2026</p>' % E(p['reading'])
    side_rel = related_html(path, p['related'])
    owner = ''
    if kind == 'guide' and p.get('owner') in SHORT:
        owner = '<p><a class="btn btn-ghost" href="%s">%s</a></p>' % (rel(path, p['owner']), E('See ' + SHORT[p['owner']]))
    body = '''%s
<section class="phead"><div class="wrap">
<div><span class="eyebrow">%s</span><h1>%s</h1><p class="answer">%s</p>%s<div class="btns">%s</div></div>
<div class="pic">%s</div>
</div></section>
<div class="wrap layout">
<article class="prose">%s%s%s</article>
<aside class="side"><div class="panel"><h3>Related</h3><ul>%s</ul></div>
<div class="panel"><h3>Start with the basics</h3><p>A floor plan, a few unit photos, how you'll use the space and your target opening date.</p>%s</div></aside>
</div>
%s''' % (crumbs_html(path, crumbs), E(p['kicker']), E(p['h1']), E(p['answer']), meta,
         cta(path, p.get('wa_topic', 'my space')) + (' <a class="btn btn-ghost" href="%s">All services</a>' % rel(path, '/services/') if kind == 'service' else ''),
         pic(p['image'], p['image_alt'], eager=True), secs, owner, faq_html(p['faqs']), side_rel,
         cta(path, p.get('wa_topic', 'my space')), cta_band(path, p.get('wa_topic', 'my space')))
    write(path, head(path, p['title'], p['desc'], schema) + header(path) + body + footer(path), p.get('date', TODAY))


# ---------- hub pages ----------
def hub(path, title, desc, h1, kicker, intro, key, alt, inner, crumbs, extra_schema=None):
    schema = [org_schema(), crumbs_schema(crumbs), {'@type': 'CollectionPage', 'name': h1, 'url': abs_url(path), 'description': desc}]
    if extra_schema:
        schema += extra_schema
    body = '''%s
<section class="phead"><div class="wrap">
<div><span class="eyebrow">%s</span><h1>%s</h1><p class="answer">%s</p><div class="btns">%s</div></div>
<div class="pic">%s</div></div></section>
<section class="band sand"><div class="wrap">%s</div></section>
%s''' % (crumbs_html(path, crumbs), E(kicker), E(h1), E(intro), cta(path), pic(key, alt, eager=True), inner, cta_band(path, 'my space'))
    write(path, head(path, title, desc, schema) + header(path) + body + footer(path))


def build_hubs():
    # services
    inner = '<div class="head"><h2>Specialist services</h2><p>Each page explains scope, options, budget drivers and what to prepare.</p></div><div class="svc">%s</div>' % ''.join(
        svc_tile('/services/', s) for s in SERVICE_ORDER)
    inner += '<div class="head" style="margin-top:44px"><h2>Audio, visual and lighting</h2><p>Sound, screens and feature light planned with the fit-out.</p></div><div class="svc">%s</div>' % ''.join(
        svc_tile('/services/', s) for s in ['/avl/commercial-audio-systems/', '/avl/display-visual-systems/', '/avl/architectural-feature-lighting/'])
    hub('/services/', 'Retail & Commercial Renovation Services | R&C',
        'Commercial carpentry, renovation, electrical works, tiling, flooring, painting and AVL for shops, offices, cafes and salons in Singapore.',
        'Services for retail and commercial spaces', 'Services', C_SVC.SERVICES_INTRO, 'counter-joinery',
        'Custom oak shop counter with display niche (AI design concept)', inner, [('/services/', 'Services')])
    # spaces
    inner = '<div class="head"><h2>Choose your type of space</h2></div><div class="grid g4">%s</div>' % ''.join(
        card('/spaces/', p['path'], SHORT[p['path']], p['card'], p['image']) for p in C_SPC.PAGES)
    hub('/spaces/', 'Shop, Office, Cafe & Salon Interiors | R&C',
        'Plan a retail shop, office or showroom, cafe counter or salon interior: the needs, scope mix and materials for each type of business space.',
        'Interiors by type of business space', 'Spaces', C_SPC.SPACES_INTRO, 'hero-boutique',
        'Boutique shop unit with oak perimeter shelving (AI design concept)', inner, [('/spaces/', 'Spaces')])
    # guides
    inner = '<div class="head"><h2>Planning guides</h2><p>Practical reading before you speak to any contractor.</p></div><div class="grid g3">%s</div>' % ''.join(
        card('/guides/', p['path'], p['h1'], p['card'], p['image'], 'Read guide') for p in C_GDE.PAGES)
    hub('/guides/', 'Shop Fit-Out & Renovation Guides | R&C',
        'Original planning guides for Singapore shop and commercial fit-outs: briefing, shelving materials, counters, checklists, lighting and music.',
        'Planning guides for business spaces', 'Guides', C_GDE.GUIDES_INTRO, 'design-planning',
        'Shop floor plan with material samples on a table (AI design concept)', inner, [('/guides/', 'Guides')])


def build_concepts():
    path = '/design-concepts/'
    rows = []
    for c in C_SPC.CONCEPTS:
        chips = ''.join('<li><a href="%s">%s</a></li>' % (rel(path, s), E(SHORT.get(s, s))) for s in c['services'] if s in SHORT)
        rows.append('''<div class="concept rv" id="%s"><div class="pic">%s</div><div><span class="eyebrow">AI design concept · %s</span>
<h2>%s</h2><p>%s</p><ul>%s</ul><ul class="chips">%s</ul></div></div>''' % (
            E(c['slug']), pic(c['image'], c['title'] + ' (AI design concept)'), E(c['space'].title()), E(c['title']), E(c['summary']),
            ''.join('<li>%s</li>' % E(x) for x in c['elements']), chips))
    inner = '<div class="prose" style="max-width:none">%s</div>' % ''.join(rows)
    hub(path, 'Retail & Office Interior Design Concepts | R&C',
        'AI design concepts for small shops, office receptions, cafe counters, salons and showrooms: ideas to discuss, clearly labelled, not completed projects.',
        'Design concepts for retail and commercial spaces', 'Design concepts', C_SPC.CONCEPTS_INTRO, 'showroom',
        'Small showroom with oak display walls and a screen (AI design concept)', inner, [(path, 'Design concepts')],
        [{'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': c['title'],
                                                     'url': abs_url(path) + '#' + c['slug']} for i, c in enumerate(C_SPC.CONCEPTS)]}])


# ---------- home ----------
HOME_FAQ = [
    ('What does R&C do?', 'R&C is a design and build brand for retail and commercial spaces in Singapore. It covers integrated planning, '
     'custom carpentry, renovation, electrical works, tiling and flooring, painting and finishing, and audio, visual and lighting (AVL) '
     'for shops, offices, showrooms, cafes and salons.'),
    ('Are the photos on this site completed projects?', 'No. Every image on this site is an AI design concept, labelled as such, to help '
     'discuss ideas. Photographs of actual completed work will only be shown once real projects exist and the owners agree.'),
    ('What should I send to start?', 'A floor plan or unit layout, a few photos of the unit, how you plan to use the space, your landlord or '
     'mall fit-out guidelines if you have them, and your target opening date. That is enough for a first scope discussion.'),
    ('Can AVL be planned together with the renovation?', 'Yes, and it is usually easier that way. Speaker, screen and feature lighting '
     'positions affect ceilings, wall backing, power points and cable routes, so planning them during the fit-out avoids rework later.'),
]

PROCESS = [('Brief', 'Your business, how the space will be used, priorities and target opening date.'),
           ('Site assessment', 'Measure the unit, check existing services and landlord or mall requirements.'),
           ('Scope & quotation', 'A written scope that separates what is included from what is not.'),
           ('Design', 'Layout, carpentry details, finishes, lighting and AVL positions agreed before work starts.'),
           ('Installation', 'Trades sequenced on site within the building\'s working rules.'),
           ('Handover', 'Walk-through, defects list and the information you need to run the space.')]


def concept_line(c):
    s = [x.strip() for x in c['summary'].split('. ') if x.strip()]
    s = [x for x in s if not x.lower().startswith('an ai design concept')] or s
    return s[0].rstrip('.') + '.'


def build_home():
    path = '/'
    spaces = ''.join(card(path, p['path'], SHORT[p['path']], p['card'], p['image']) for p in C_SPC.PAGES)
    svcs = ''.join(svc_tile(path, s) for s in SERVICE_ORDER)
    concepts = ''.join('<a class="card" href="%s#%s"><div class="ph">%s</div><div class="bd"><h3>%s</h3><p>%s</p><span class="more">View concept</span></div></a>' % (
        rel(path, '/design-concepts/'), E(c['slug']), pic(c['image'], c['title'] + ' (AI design concept)', small=True), E(c['title']),
        E(concept_line(c))) for c in sorted(C_SPC.CONCEPTS, key=lambda c: c['image'] in ('hero-boutique', 'office-reception', 'cafe-counter', 'salon-stations'))[:5])
    steps = ''.join('<li class="rv"><strong>%s</strong><span>%s</span></li>' % (E(a), E(b)) for a, b in PROCESS)
    trio = ''.join('<div><b>%s</b><span>%s</span></div>' % (E(t['title']), E(t['text'])) for t in C_AVL.AVL_TRIO)
    guides = ''.join(card(path, p['path'], p['h1'], p['card'], p['image'], 'Read guide') for p in C_GDE.PAGES[:3])
    faqs = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in HOME_FAQ)
    body = '''<section class="hero"><div class="wrap">
<div><span class="eyebrow">Retail &amp; Commercial Design &amp; Build</span>
<h1>Design &amp; Build for Retail and Commercial Spaces</h1>
<p class="lede">From custom carpentry and renovation to electrical, flooring and integrated audio, visual and lighting.</p>
<div class="btns">%s<a class="btn btn-ghost" href="%s">Explore Our Services</a></div>
<ul class="facts"><li>Shops &amp; boutiques</li><li>Offices &amp; showrooms</li><li>Cafes &amp; counters</li><li>Salons &amp; studios</li></ul>
</div>
<div class="hero-img">%s</div>
</div></section>

<section class="band sand"><div class="wrap">
<div class="head rv"><h2>Spaces built around how your business works</h2><p>A boutique, a reception, a service counter and a salon station each ask different things of a layout.</p></div>
<div class="grid g4">%s</div></div></section>

<section class="band"><div class="wrap">
<div class="head rv"><h2>Services</h2><p>One coordinated scope, or the specialist trade you need. Each service has its own page with the details.</p></div>
<div class="svc">%s</div>
<p class="rv" style="margin-top:20px"><a href="%s">See all services and AVL &rarr;</a></p></div></section>

<section class="band olive"><div class="wrap">
<div class="head rv"><h2>Design concepts</h2><p>AI-generated design concepts to start a conversation. They are ideas, not completed projects.</p></div>
<div class="rail">%s</div></div></section>

<section class="band"><div class="wrap">
<div class="head rv"><h2>How an R&amp;C project is planned to run</h2><p>The intended process, from first brief to handover.</p></div>
<ol class="steps">%s</ol></div></section>

<section class="band dark"><div class="wrap avl">
<div class="pic rv">%s</div>
<div class="rv"><span class="eyebrow" style="color:var(--oak-l)">AVL: audio, visual and lighting</span>
<h2>Sound, screens and light, planned with the space</h2>
<p>Ceiling speakers, display screens and feature lighting all need backing, power and cable routes. Planning them with the fit-out keeps them neat and avoids rework.</p>
<div class="trio">%s</div>
<div class="btns"><a class="btn btn-light" href="%s">Explore AVL</a></div></div>
</div></section>

<section class="band sand"><div class="wrap">
<div class="head rv"><h2>Planning guides</h2><p>Practical reading for shop owners and tenants.</p></div>
<div class="grid g3">%s</div>
<p class="rv" style="margin-top:20px"><a href="%s">All guides &rarr;</a></p></div></section>

<section class="band" id="enquire"><div class="wrap enq">
<div class="rv"><h2>Discuss your space</h2><p>Start with what you already have. These four things are enough for a first conversation about scope:</p>
<ul class="check"><li>Floor plan or unit layout</li><li>A few photos of the unit as it is now</li><li>How you intend to use the space</li><li>Your target opening date</li></ul></div>
<div class="panel rv"><h3>Ready when you are</h3><p>Share your details and we'll discuss your scope.</p>%s<div class="btns">%s</div></div>
</div></section>

<section class="band sand"><div class="wrap"><div class="faq" style="max-width:820px"><h2>Questions</h2>%s</div></div></section>
''' % (cta(path), rel(path, '/services/'), pic('hero-boutique', 'Small Singapore boutique unit with oak shelving, cream walls and an olive accent behind the counter (AI design concept)', eager=True),
       spaces, svcs, rel(path, '/services/'), concepts, steps,
       pic('showroom', 'Showroom with a display screen, ceiling speakers and warm feature lighting (AI design concept)'), trio, rel(path, '/avl/'),
       guides, rel(path, '/guides/'), pending_box([('Enquiry line', 'WhatsApp number to be confirmed')]), cta(path), faqs)
    schema = [org_schema(), {'@type': 'WebSite', '@id': BASE + '#site', 'name': BRAND_FULL, 'url': BASE, 'publisher': {'@id': BASE + '#org'}},
              faq_schema(HOME_FAQ)]
    title = 'Retail & Commercial Design & Build Singapore | R&C'
    desc = 'Design and build for Singapore shops, offices, cafes and salons: custom carpentry, renovation, electrical, flooring, finishing and AVL.'
    write(path, head(path, title, desc, schema) + header(path) + body + footer(path))


# ---------- about / contact / privacy / 404 ----------
def simple(path, title, desc, h1, kicker, answer, prose, crumbs, key=None, alt='', schema_extra=None):
    schema = [org_schema(), crumbs_schema(crumbs)] + (schema_extra or [])
    picture = '<div class="pic">%s</div>' % pic(key, alt, eager=True) if key else ''
    body = '''%s
<section class="phead"><div class="wrap"%s>
<div><span class="eyebrow">%s</span><h1>%s</h1><p class="answer">%s</p></div>%s</div></section>
<div class="wrap" style="padding-bottom:30px"><article class="prose">%s</article></div>
%s''' % (crumbs_html(path, crumbs), '' if key else ' style="grid-template-columns:1fr"', E(kicker), E(h1), E(answer), picture,
         fix_links(prose, path), cta_band(path, 'my space') if path != '/contact/' else '')
    write(path, head(path, title, desc, schema) + header(path) + body + footer(path))


def build_static():
    about = '''<h2>What R&amp;C is for</h2>
<p>R&amp;C is a design and build brand for Singapore business owners and tenants who are opening, moving or refreshing a retail or commercial space. The focus is practical: shops and boutiques, offices and showrooms, cafes and service counters, and salons and beauty studios.</p>
<h2>What R&amp;C covers</h2>
<ul><li><a href="/retail-commercial-design-build/">Design &amp; build</a>: integrated planning and coordination from brief to handover.</li>
<li><a href="/services/commercial-carpentry/">Commercial carpentry</a>: counters, shelving, storage, display fixtures and reception joinery.</li>
<li><a href="/services/commercial-renovation/">Renovation</a>, <a href="/services/commercial-electrical-works/">electrical works</a>, <a href="/services/commercial-tiling-flooring/">tiling and flooring</a>, and <a href="/services/commercial-painting-finishing/">painting and finishing</a>.</li>
<li><a href="/avl/">AVL</a>: audio, visual and lighting planned with the space.</li></ul>
<h2>How this website handles evidence</h2>
<p>R&amp;C is a new brand. This site therefore shows no client list, reviews, project counts or years in business, because none can be verified yet. Every image is an AI design concept and is labelled as one. Photographs of actual completed work, and any credentials, will be added only when they are real and can be checked.</p>
<h2>Business details</h2>
<p>The operating company, contact details and delivery arrangements will be published here before R&amp;C takes on projects.</p>
%s''' % pending_box()
    simple('/about/', 'About R&C | Retail & Commercial Design & Build', 'About R&C, a Singapore design and build brand for shops, offices, cafes and salons: what it covers and how this site handles evidence.',
           'About R&C', 'About', 'R&C - Retail & Commercial Design & Build is a new Singapore brand for business owners and tenants planning shops, offices, showrooms, cafes and salons, covering design and build, carpentry, renovation, electrical, flooring, finishing and AVL.',
           about, [('/about/', 'About')], 'design-planning', 'Floor plan and material samples on a planning table (AI design concept)',
           [{'@type': 'AboutPage', 'name': 'About R&C', 'url': abs_url('/about/')}])
    w = wa_link('my space', '/contact/')
    contact_cta = ('<p><a class="btn btn-main" href="%s" rel="noopener">WhatsApp R&amp;C</a></p>' % E(w)) if w else pending_box(
        [('Enquiry line', 'The R&C WhatsApp number is being set up. Until then this page lists what to prepare.')], 'Enquiry line opening soon')
    contact = '''<h2>How to start</h2>
<p>The quickest way to a useful first conversation is to share what you already have about the unit and the business.</p>
%s
<h2>What to prepare</h2>
<ol><li><strong>Floor plan or unit layout</strong>, from the landlord, mall or previous tenant if you have one.</li>
<li><strong>Photos of the unit</strong> as it is now: shopfront, each wall, ceiling and floor.</li>
<li><strong>Intended use</strong>: what you sell or do there, how many staff, what customers do in the space.</li>
<li><strong>Target opening date</strong>, plus any handover or fit-out period in your lease.</li>
<li><strong>Landlord or mall fit-out guidelines</strong>, if you have them.</li>
<li><strong>Priorities</strong>: what must be right on day one, and what can wait.</li></ol>
<p class="note">Not sure where to begin? Read <a href="/guides/how-to-brief-a-shop-fit-out/">how to brief a shop fit-out</a> first.</p>''' % contact_cta
    simple('/contact/', 'Contact R&C | Discuss Your Retail or Office Space', 'Discuss your shop, office, cafe or salon space with R&C: what to send for a first scope conversation, including floor plan, photos and opening date.',
           'Discuss your space', 'Contact', 'Send a floor plan, a few photos of the unit, how you will use the space and your target opening date. That is enough for a first conversation about scope, options and next steps.',
           contact, [('/contact/', 'Contact')], 'office-reception', 'Office reception with a curved oak counter (AI design concept)',
           [{'@type': 'ContactPage', 'name': 'Contact R&C', 'url': abs_url('/contact/')}])
    privacy = '''<p>Last updated 24 October 2026.</p>
<h2>What this website collects</h2>
<p>This website has no forms and sets no advertising cookies. When you tap a WhatsApp button, an anonymous count is recorded (the page you were on, whether you used a phone or computer, and the referring site) so we can see which pages help visitors. It does not record your name, number or the message you send.</p>
<h2>Messages you send</h2>
<p>If you contact R&amp;C, the details you choose to share (such as your name, number, floor plan and photos) are used only to respond to your enquiry and discuss your project, in line with Singapore's Personal Data Protection Act. They are not sold or shared for marketing.</p>
<h2>Third-party services</h2>
<p>WhatsApp messages are handled by WhatsApp under its own privacy policy. Fonts and scripts on this site are served from this website.</p>
<h2>Access, correction and questions</h2>
<p>You may ask to see, correct or delete personal data you have shared with R&amp;C.</p>
%s''' % pending_box([('Data protection contact', 'to be published with the operating company details')])
    simple('/privacy-policy/', 'Privacy Policy | R&C', 'How the R&C website handles personal data: no forms, an anonymous WhatsApp tap count, and how enquiry details are used.',
           'Privacy policy', 'Privacy', 'This website has no forms and no advertising cookies. It records only an anonymous count of WhatsApp button taps. Details you send when you contact R&C are used only to answer your enquiry.',
           privacy, [('/privacy-policy/', 'Privacy policy')])


def build_404():
    path = '/404/'
    r = '/preview/%s/' % SLUG if not DOMAIN else '/'
    doc = head('/', 'Page not found | R&C', 'This page does not exist.', [org_schema()]).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large">', '<meta name="robots" content="noindex">')
    # 404 is served at any depth, so use root-absolute links
    doc = re.sub(r'(href|src)="(?:\./|(?:\.\./)*)((?:favicon|icon-|apple-|site\.web|fonts/|rc\.css)[^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), r, m.group(2)), doc)
    hdr = header('/').replace('href="./"', 'href="%s"' % r)
    hdr = re.sub(r'(href|src)="((?!https?:|#)[^"]+)"', lambda m: '%s="%s%s"' % (m.group(1), r, m.group(2).lstrip('./')) if not m.group(2).startswith('/') else m.group(0), hdr)
    body = '''<section class="phead"><div class="wrap" style="grid-template-columns:1fr"><div><span class="eyebrow">404</span><h1>That page isn't here</h1>
<p class="answer">The link may be old or mistyped. Try one of these instead.</p>
<div class="btns"><a class="btn btn-main" href="%s">Home</a><a class="btn btn-ghost" href="%sservices/">Services</a><a class="btn btn-ghost" href="%scontact/">Contact</a></div></div></div></section>''' % (r, r, r)
    ftr = footer('/')
    ftr = re.sub(r'(href|src)="((?!https?:|#)[^"]+)"', lambda m: '%s="%s%s"' % (m.group(1), r, m.group(2).lstrip('./')) if not m.group(2).startswith('/') else m.group(0), ftr)
    with open(os.path.join(OUT, '404.html'), 'w', encoding='utf-8') as f:
        f.write(doc + hdr + body + ftr)


# ---------- machine files ----------
def build_machine():
    urls = ''.join('<url><loc>%s</loc><lastmod>%s</lastmod></url>' % (E(abs_url(p)), m) for p, m in sorted(PAGES_OUT))
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls)
    bots = ['Googlebot', 'Googlebot-Image', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot',
            'Claude-SearchBot', 'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']
    rb = ''.join('User-agent: %s\nAllow: /\n\n' % b for b in bots)
    rb += 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % BASE
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write(rb)
    lines = ['# %s' % BRAND_FULL, '', '> %s' % TAGLINE, '',
             'R&C is a new Singapore design and build brand for retail and commercial spaces: shops and boutiques, offices and showrooms, '
             'cafes and service counters, salons and beauty studios. Services: integrated design and build, commercial carpentry, '
             'renovation, electrical works, tiling and flooring, painting and finishing, and audio, visual and lighting (AVL).',
             '', 'All images on the site are AI design concepts, not completed projects. No prices, reviews or project counts are published.', '']
    sections = [('Services', SERVICE_ORDER), ('AVL', [p['path'] for p in C_AVL.PAGES]), ('Spaces', [p['path'] for p in C_SPC.PAGES]),
                ('Guides', [p['path'] for p in C_GDE.PAGES])]
    for name, paths in sections:
        lines.append('## %s' % name)
        for pth in paths:
            p = ALL_CONTENT[pth]
            lines.append('- [%s](%s): %s' % (p['h1'], abs_url(pth), p['card']))
        lines.append('')
    lines += ['## Other', '- [Design concepts](%s): AI design concepts, clearly labelled.' % abs_url('/design-concepts/'),
              '- [About](%s)' % abs_url('/about/'), '- [Contact](%s)' % abs_url('/contact/'), '']
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write('\n'.join(lines))
    with open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w') as f:
        f.write(INDEXNOW_KEY)
    man = {'name': BRAND_FULL, 'short_name': 'R&C', 'start_url': './', 'display': 'browser', 'background_color': '#fbf8f2',
           'theme_color': '#2b2925', 'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                               {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}]}
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump(man, f)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    for name in ('rc.css', 'rc.js', 'wa-tap-counter.js'):
        shutil.copy(os.path.join(HERE, name), OUT)
    shutil.copytree(os.path.join(HERE, 'fonts'), os.path.join(OUT, 'fonts'))
    for name in ('favicon.ico', 'favicon-48.png', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png'):
        shutil.copy(os.path.join(HERE, 'icons', name), OUT)
    build_home()
    build_hubs()
    build_concepts()
    for p in C_SVC.PAGES:
        cr = [(p['path'], SHORT[p['path']])] if p['path'] == '/retail-commercial-design-build/' else [('/services/', 'Services'), (p['path'], SHORT[p['path']])]
        content_page(p, cr)
    for p in C_AVL.PAGES:
        cr = [('/avl/', 'AVL')] if p['path'] == '/avl/' else [('/avl/', 'AVL'), (p['path'], SHORT[p['path']])]
        content_page(p, cr)
    for p in C_SPC.PAGES:
        content_page(p, [('/spaces/', 'Spaces'), (p['path'], SHORT[p['path']])])
    for p in C_GDE.PAGES:
        content_page(p, [('/guides/', 'Guides'), (p['path'], p['h1'])], kind='guide')
    build_static()
    build_404()
    build_machine()
    print('built %d pages into %s' % (len(PAGES_OUT), OUT))


if __name__ == '__main__':
    main()
