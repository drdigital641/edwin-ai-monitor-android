#!/usr/bin/env python3
"""Pre-upload gate for the Hock Chuan Hiong preview. Exit 1 on any problem. Run after build.py, before any Bridge upload.
Fails on: lorem / TODO / placeholder text, any trace of the other agency brand, aggregateRating or rating schema, the
do-not-use landlines / old Bayu Tinggi listing / old IG handle / dead domain, RM prices, awards, 'best in Malaysia', online
shop / delivery claims, a computed age ('40 years'), em dashes, a hardcoded robots meta (noindex is host-based), H1 count != 1,
missing tracker, wrong footer credit, a CTA without data-cta, wrong WhatsApp / tel / social links, bad JSON-LD, canonicals /
hreflang not on site_base, og/twitter image not the resolving share JPG, a missing Non-Halal note, missing twins, missing
media or asset files, CJK glyphs missing from the font subset, and a sitemap that does not match the page list."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, '..', 'dist')
sys.path.insert(0, HERE)
import build
# Words are split so this file never trips a repo-wide grep.
BANNED = [r'lorem', r'\bTODO\b', r'\bTBD\b', r'placeholder', r'\bXXX\b', 'pa' + r'ge[\s-]*o' + 'ne', 'pageo' + 'nesingapore',
          r'aggregate' + 'Rating', r'ratingValue', r'reviewCount', r'bestRating', '[★☆⭐]',
          r'3318[\s-]?8091', r'333188091', r'3166[\s-]?2898', r'331662898', r'3323[\s-]?0531', r'Bayu Tinggi',
          r'instagram\.com/hchiongfood', r'hockchuanhiong\.com', r'\bRM\s?\d', r'RM\d', r'令吉', r'\baward', r'得奖', r'best in Malaysia',
          r'\bdeliver', r'送货', r'penghantaran', r'online shop', r'shopee', r'lazada', r'grabfood', r'foodpanda',
          r'40 years', r'40年', r'40 tahun', r'\bfounder\b', r'创办人', r'郑再兴', r'Hock Moon Hiong', r'福满香', r'Kota Kemuning', r'Setia Alam',
          r'unsplash', r'pexels', r'shutterstock', r'istock', r'gettyimages', r'ChIJ']
CSSJS_OK = {'placeholder'}
WA = 'https://wa.me/60102349328?text='
SITE = build.SITE
SHARE_OG = build.SHARE + 'media/og.jpg'
SOCIAL = {'facebook.com/hchiongfood': build.LK['facebook'], 'instagram.com': build.LK['instagram'], 'threads.com': build.LK['threads']}
bad = 0


def fail(f, m):
    global bad
    bad += 1
    print(f'FAIL {os.path.relpath(f, DIST)}: {m}')


chars = set(open(os.path.join(HERE, 'assets', 'fonts', 'zh-chars.txt'), encoding='utf8').read())
files = [os.path.join(dp, f) for dp, _, fs in os.walk(DIST) for f in fs if f.endswith(('.html', '.txt', '.xml', '.js', '.css'))]
pages = set()
for f in files:
    t = open(f, encoding='utf8').read()
    for b in BANNED:
        m = re.search(b, t, re.I)
        if m and not (f.endswith(('.css', '.js')) and b in CSSJS_OK):
            fail(f, f'banned "{m.group(0)}"')
    if '—' in t:
        fail(f, 'em dash')
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
    if t.count('class="nh') < 2 or not re.search(r'Non-Halal / |/ Non-Halal /|Tidak Halal / ', t):
        fail(f, 'Non-Halal note missing')
    can = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    if not can or can.group(1) != SITE + p:
        fail(f, f'canonical {can.group(1) if can else None} != {SITE + p}')
    hl = re.findall(r'hreflang="(en|ms|zh-Hans|x-default)" href="([^"]+)"', t)
    if len(hl) != 4 or any(not h.startswith(SITE) for _, h in hl):
        fail(f, 'hreflang block (en, ms, zh-Hans, x-default on site_base)')
    if t.count('<nav class="lang"') != 2:
        fail(f, 'language switcher (header + menu) missing')
    for k in ('og:image', 'og:image:secure_url', 'twitter:image'):
        if not re.search(r'(?:property|name)="' + k + '" content="' + re.escape(SHARE_OG) + '"', t):
            fail(f, k + ' is not the resolving share URL ' + SHARE_OG)
    if 'og:image:type" content="image/jpeg"' not in t or 'og:image:width" content="1200"' not in t or 'og:image:height" content="630"' not in t or 'og:image:alt' not in t:
        fail(f, 'og:image type/width/height/alt')
    if not re.search(r'og:url" content="' + re.escape(SITE + p) + '"', t):
        fail(f, 'og:url not on site_base')
    for a in re.findall(r'<a\b[^>]*>', t):
        h = re.search(r'href="([^"]*)"', a)
        h = h.group(1) if h else ''
        if re.match(r'(https://wa\.me|tel:|mailto:|https://www\.google\.com/maps|https://www\.facebook\.com|https://www\.instagram\.com|https://www\.threads\.com)', h):
            if 'data-cta=' not in a or 'data-ref=' not in a:
                fail(f, 'CTA without data-cta/data-ref: ' + a[:90])
        if 'wa.me' in h and not h.startswith(WA):
            fail(f, 'wrong WhatsApp link ' + h[:60])
        if h.startswith('tel:') and h != 'tel:+60102349328':
            fail(f, 'wrong tel link ' + h)
        if h.startswith('mailto:') and h != 'mailto:hchiongfood@gmail.com':
            fail(f, 'wrong email ' + h)
        if 'instagram.com' in h and h != build.LK['instagram']:
            fail(f, 'wrong Instagram link')
        if 'threads.com' in h and h != build.LK['threads']:
            fail(f, 'wrong Threads link')
        if 'facebook.com' in h and h != build.LK['facebook'] and not re.fullmatch(r'https://www\.facebook\.com/reel/(' + '|'.join(build.LK['reels']) + r')/', h):
            fail(f, 'wrong Facebook link ' + h)
        if 'google.com/maps' in h and h != build.LK['gbp']:
            fail(f, 'map link is not the GBP URL')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            d = json.loads(j)
        except Exception as e:
            fail(f, f'bad JSON-LD {e}')
            continue
        if d.get('@type') == 'FoodEstablishment':
            if d.get('sameAs') != [build.LK['facebook'], build.LK['instagram']]:
                fail(f, 'sameAs')
            oh = d['openingHoursSpecification']
            if len(oh) != 1 or oh[0]['opens'] != '09:00' or oh[0]['closes'] != '20:00' or len(oh[0]['dayOfWeek']) != 7:
                fail(f, 'hours')
            if d['address']['postalCode'] != '41200' or 'Lorong Batu Nilam 1D' not in d['address']['streetAddress'] or d['telephone'] != '+60102349328':
                fail(f, 'NAP')
            if not d['url'].startswith(SITE):
                fail(f, 'schema url not on site_base')
    for src in re.findall(r'(?:src|srcset|href)="' + re.escape(build.BASE) + r'((?:media|assets)/[^"?\s]+)', t) + \
            re.findall(r'(?:srcset="|, )' + re.escape(build.BASE) + r'((?:media|assets)/[^"?\s,]+)', t):
        if not os.path.exists(os.path.join(DIST, src)) and src not in build.SERVER_MEDIA:
            fail(f, 'missing file ' + src)
    body = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    miss = {c for c in body if ord(c) > 0x2E80 and not (0xFE00 <= ord(c) <= 0xFE0F)} - chars
    if miss:
        fail(f, 'CJK glyphs missing from font subset: ' + ''.join(sorted(miss))[:40])
for L in build.I18N.LANGS[1:]:
    for p in [p for p in pages if not p.startswith(('ms/', 'zh/'))]:
        if L['prefix'] + p not in pages:
            fail(DIST, f'missing {L["code"]} twin of /{p}')
if len(pages) != len(build.PAGES) * 3:
    fail(DIST, f'{len(pages)} pages built, expected {len(build.PAGES) * 3}')
sm = open(os.path.join(DIST, 'sitemap.xml'), encoding='utf8').read()
if sm.count('<loc>') != len(pages) or sm.count('hreflang="x-default"') != len(pages) or any(not x.startswith(SITE) for x in re.findall(r'<loc>([^<]+)', sm)):
    fail(os.path.join(DIST, 'sitemap.xml'), f'sitemap has {sm.count("<loc>")} urls for {len(pages)} pages')

tmp = tempfile.mkdtemp()
shutil.copytree(DIST, os.path.join(tmp, 'preview', 'hock-chuan-hiong'))
r = subprocess.run([sys.executable, '/mnt/project-files/tracking/cta_check.py', '--dir', tmp], capture_output=True, text=True)
shutil.rmtree(tmp)
print(r.stdout.strip()[-400:])
if r.returncode:
    bad += 1
print(f'check: {len(files)} files, {len(pages)} pages, {bad} problem(s)')
sys.exit(1 if bad else 0)
