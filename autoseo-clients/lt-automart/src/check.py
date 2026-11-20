#!/usr/bin/env python3
"""Pre-upload gate for LT Automart. Exit 1 on any problem. Run after build.py, before any Bridge upload.
Fails on: brief grep list (lorem, TODO, other-agency name, aggregateRating, ratingValue, RM + digit, staff numbers,
gmail, Taman Abad), stars/score, warranty/dealer claims, a robots meta (noindex is host-based), H1 count != 1, missing
tracker, wrong footer credit, CTA without data-cta/data-ref, wrong WhatsApp/tel/social/map links, bad JSON-LD, canonical/
hreflang/og:url/og:image not from site.json, missing twins, missing files, CJK glyphs missing from the font subset,
sitemap not matching the page list. Em dashes are allowed only inside the verbatim Google review quote."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, '..', 'dist')
sys.path.insert(0, HERE)
import build
CFG = build.CFG
BANNED = [r'lorem', r'\bTODO\b', r'\bTBD\b', r'\bXXX\b', 'pa' + r'ge[\s-]*o' + 'ne', 'pageo' + 'nesingapore',
          'aggregate' + 'Rating', 'rating' + 'Value', 'review' + 'Count', 'best' + 'Rating', r'"@type": "Review"', '[★☆⭐]', r'\b4\.3\b',
          r'\bRM\s?\d', r'012[\s-]?995', r'011[\s-]?2620', r'018[\s-]?242', r'60129957670', r'601126202426', r'60182426566', 'gm' + 'ail', 'Taman ' + 'Abad',
          r'warrant', r'guarante', r'authori[sz]ed dealer', r'\bLTA\b', r'\bJPJ\b', r'LTautomark', r'11\.11', r'10pm', r'10 malam',
          r'unsplash', r'pexels', r'shutterstock', r'istock']
WA = 'https://wa.me/60127166110?text='
SITE = CFG.canonical_base
OG = CFG.og_image()
LK = build.LK
OK_HREF = {LK['maps'], LK['waze'], LK['facebook'], LK['tiktok'], LK['reviews']} | set(build.REEL_URL.values())
bad = 0


def fail(f, m):
    global bad
    bad += 1
    print(f'FAIL {os.path.relpath(f, DIST)}: {m}')


chars = set(open(os.path.join(HERE, 'assets', 'fonts', 'zh-chars.txt'), encoding='utf8').read())
files = [os.path.join(dp, f) for dp, _, fs in os.walk(DIST) for f in fs if f.endswith(('.html', '.txt', '.xml', '.js', '.css'))]
pages = set()
quote = build.F['reviews'][1]['text']
for f in files:
    t = open(f, encoding='utf8').read()
    for b in BANNED:
        m = re.search(b, t, re.I)
        if m:
            fail(f, f'banned "{m.group(0)}"')
    if '—' in t.replace(build.E(quote), '').replace(quote, ''):
        fail(f, 'em dash outside the verbatim review')
    if not f.endswith('.html'):
        continue
    rel = os.path.relpath(os.path.dirname(f), DIST).replace('\\', '/')
    p = '' if rel == '.' else rel + '/'
    pages.add(p)
    if re.search(r'<meta name="robots"', t):
        fail(f, 'robots meta found (preview noindex is host-based)')
    if len(re.findall(r'<h1\b', t)) != 1:
        fail(f, 'H1 count != 1')
    if 'p1-cta.js' not in t:
        fail(f, 'no tracker')
    if t.count('Website by AutoSEO.my') != 1 or '<a href="https://autoseo.my/">Website by AutoSEO.my</a>' not in t:
        fail(f, 'footer credit')
    can = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    if not can or can.group(1) != SITE + p:
        fail(f, f'canonical {can.group(1) if can else None} != {SITE + p}')
    hl = re.findall(r'hreflang="(en|ms|zh-Hans|x-default)" href="([^"]+)"', t)
    if len(hl) != 4 or any(not h.startswith(SITE) for _, h in hl):
        fail(f, 'hreflang block')
    if t.count('<nav class="tabs"') != 2:
        fail(f, 'language switcher (header + menu)')
    for k in ('og:image', 'og:image:secure_url', 'twitter:image'):
        if not re.search(r'(?:property|name)="' + k + '" content="' + re.escape(OG) + '"', t):
            fail(f, k + ' != ' + OG)
    if not all(x in t for x in ('og:image:type" content="image/jpeg"', 'og:image:width" content="1200"', 'og:image:height" content="630"', 'og:image:alt')):
        fail(f, 'og:image type/width/height/alt')
    if f'og:url" content="{SITE + p}"' not in t:
        fail(f, 'og:url')
    for a in re.findall(r'<a\b[^>]*>', t):
        h = re.search(r'href="([^"]*)"', a)
        h = (h.group(1) if h else '').replace('&amp;', '&')
        if h.startswith('http') and 'autoseo.my' not in h or h.startswith('tel:'):
            if 'data-cta=' not in a or 'data-ref=' not in a:
                fail(f, 'external link without data-cta/data-ref: ' + a[:90])
        if 'wa.me' in h and not h.startswith(WA):
            fail(f, 'wrong WhatsApp link ' + h[:60])
        if h.startswith('tel:') and h != 'tel:+60127166110':
            fail(f, 'wrong tel ' + h)
        if h.startswith('http') and 'wa.me' not in h and 'autoseo.my' not in h and h not in OK_HREF:
            fail(f, 'unexpected external link ' + h)
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            d = json.loads(j)
        except Exception as e:
            fail(f, f'bad JSON-LD {e}')
            continue
        if d.get('@type') == ['AutoPartsStore', 'AutoRepair']:
            oh = d['openingHoursSpecification']
            if len(oh) != 1 or oh[0]['opens'] != '10:00' or oh[0]['closes'] != '20:30' or len(oh[0]['dayOfWeek']) != 7:
                fail(f, 'hours')
            if d['address']['postalCode'] != '80250' or '183, Jalan Dato Sulaiman' not in d['address']['streetAddress'] or d['telephone'] != '+60127166110':
                fail(f, 'NAP')
            if d['sameAs'] != [LK['facebook'], LK['tiktok']] or d['legalName'] != 'LT AUTOMART TRADING SDN. BHD.':
                fail(f, 'sameAs / legalName')
            if not d['url'].startswith(SITE) or not d['@id'].startswith(SITE):
                fail(f, 'schema url/@id not from site.json')
    if p in ('', 'ms/', 'zh/') and '"FAQPage"' not in t:
        fail(f, 'FAQPage missing on home')
    if p not in ('', 'ms/', 'zh/') and '"BreadcrumbList"' not in t:
        fail(f, 'BreadcrumbList missing')
    for src in re.findall(r'(?:src|srcset|href)="' + re.escape(build.BASE) + r'((?:media|assets)/[^"?\s]+)', t) + re.findall(r', ' + re.escape(build.BASE) + r'((?:media|assets)/[^"?\s,]+)', t):
        stem = os.path.basename(src).rsplit('.', 1)[0]
        if not os.path.exists(os.path.join(DIST, src)) and stem not in build.M and stem not in ('og', 'favicon'):
            fail(f, 'missing file ' + src)
    body = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    miss = {c for c in body if ord(c) > 0x2E80 and not (0xFE00 <= ord(c) <= 0xFE0F) and not (0x1F300 <= ord(c))} - chars
    if miss:
        fail(f, 'CJK glyphs missing from font subset: ' + ''.join(sorted(miss))[:40])
if len(pages) != len(build.PAGES) * 3:
    fail(DIST, f'{len(pages)} pages built, expected {len(build.PAGES) * 3}')
sm = open(os.path.join(DIST, 'sitemap.xml'), encoding='utf8').read()
if sm.count('<loc>') != len(pages) or any(not x.startswith(SITE) for x in re.findall(r'<loc>([^<]+)', sm)):
    fail(os.path.join(DIST, 'sitemap.xml'), 'sitemap does not match pages')
tmp = tempfile.mkdtemp()
shutil.copytree(DIST, os.path.join(tmp, 'preview', 'lt-automart'))
r = subprocess.run([sys.executable, '/mnt/project-files/tracking/cta_check.py', '--dir', tmp], capture_output=True, text=True)
shutil.rmtree(tmp)
print(r.stdout.strip()[-400:])
if r.returncode:
    bad += 1
print(f'check: {len(files)} files, {len(pages)} pages, {bad} problem(s)')
sys.exit(1 if bad else 0)
