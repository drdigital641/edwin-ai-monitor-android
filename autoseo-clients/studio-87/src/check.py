#!/usr/bin/env python3
"""Pre-upload gate for the Studio 87 preview. Exit 1 on any problem. Run after build.py, before any Bridge upload.
Fails on: lorem / TODO / placeholder text, any trace of the other agency brand, aggregateRating or rating schema, the
Facebook-directory landline published as a tel: link (or anywhere), prices, a company / SSM number, an email, invented
social accounts (TikTok, Xiaohongshu, Waze), the rejected promo flyers or any fb-NN file used as an image, Western stock
or generated-image hints, review quotes (blockquote outside the official vision), em dashes, a hardcoded robots meta
(noindex is host-based on the preview), H1 count != 1, missing tracker, wrong footer credit, a CTA without data-cta,
wrong WhatsApp / tel / Instagram / Facebook links, bad JSON-LD, canonicals or hreflang not on https://studio87.com.my/,
a /ms/ page (this site is EN + 中文 only), missing /zh/ twins, missing media or asset files, CJK glyphs missing from the
font subset, and a sitemap that does not match the page list."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, '..', 'dist')
sys.path.insert(0, HERE)
import build
# Words are split so this file never trips a repo-wide grep.
BANNED = [r'lorem', r'\bTODO\b', r'\bTBD\b', r'placeholder', r'\bXXX\b', 'pa' + r'ge[\s-]*o' + 'ne', 'pageo' + 'nesingapore',
          r'aggregate' + 'Rating', r'ratingValue', r'reviewCount', r'bestRating', '[★☆⭐]',
          r'09[\s-]?509[\s-]?3717', r'6095093717', r'\+60\s?9[\s-]?509',
          r'\bRM\s?\d', r'\bfrom RM\b', r'RM\d', r'令吉', r'\bSSM\b', r'Sdn\.? Bhd', r'company no', r'@gmail', r'mailto:',
          r'tiktok', r'xiaohongshu', r'xhslink', r'\bwaze\b', r'\bfb-\d\d', r'unsplash', r'pexels', r'shutterstock', r'istock', r'gettyimages',
          r'\bowner\b', r'\bfounder\b', r'creative director', r'创办人', r'老板', r'official dealer', r'authori[sz]ed', r'经销商',
          r'Setia Alam', r'Batley', r'29 years', r'30 years', r'\bB-70\b', r'cid=', r'ChIJ', r'0x[0-9a-f]{6,}:0x']
CSSJS_OK = {'placeholder', r'mailto:', r'tiktok'}  # the shared tracker's link-type regexes
WA = 'https://wa.me/60179773168?text='
CANON = 'https://studio87.com.my/'
bad = 0


def fail(f, m):
    global bad
    bad += 1
    print(f'FAIL {os.path.relpath(f, DIST)}: {m}')


chars = set(open(os.path.join(HERE, 'assets', 'fonts-src', 'zh-chars.txt'), encoding='utf8').read())
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
    if p.startswith('ms/'):
        fail(f, 'Malay page found: this site is EN + 中文 only')
    if re.search(r'<meta name="robots"', t):
        fail(f, 'robots meta found (preview noindex is host-based)')
    if len(re.findall(r'<h1\b', t)) != 1:
        fail(f, 'H1 count != 1')
    if 'p1-cta.js' not in t:
        fail(f, 'no tracker')
    if t.count('Website by AutoSEO.my') != 1 or '<a href="https://autoseo.my/">Website by AutoSEO.my</a>' not in t:
        fail(f, 'footer credit')
    can = re.search(r'<link rel="canonical" href="([^"]+)"', t)
    if not can or can.group(1) != CANON + p:
        fail(f, f'canonical {can.group(1) if can else None} != {CANON + p}')
    hl = re.findall(r'hreflang="(en|zh-Hans|x-default)" href="([^"]+)"', t)
    if len(hl) != 3 or any(not h.startswith(CANON) for _, h in hl) or re.search(r'hreflang="ms"', t):
        fail(f, 'hreflang block (en, zh-Hans, x-default on studio87.com.my only)')
    if t.count('<nav class="lang"') != 2:
        fail(f, 'language switcher (header + menu) missing')
    if re.search(r'>BM<', t):
        fail(f, 'BM label in switcher')
    for k in ('og:title', 'og:description', 'og:image', 'og:url'):
        if f'property="{k}"' not in t:
            fail(f, 'missing ' + k)
    want = (build.F['preview']['origin'] + build.F['preview']['base_path'] if not build.LIVE else CANON) + 'media/og.jpg'
    for k in ('og:image', 'og:image:secure_url', 'twitter:image'):
        if not re.search(r'(?:property|name)="' + k + '" content="' + re.escape(want) + '"', t):
            fail(f, k + ' is not the resolving share URL ' + want)
    if 'og:image:type" content="image/jpeg"' not in t or 'og:image:width" content="1200"' not in t or 'og:image:height" content="630"' not in t:
        fail(f, 'og:image type/width/height')
    if not re.search(r'og:url" content="' + re.escape(CANON + p) + '"', t):
        fail(f, 'og:url not on the live domain')
    for bq in re.findall(r'<blockquote[^>]*>(.*?)</blockquote>', t, re.S):
        if "That&#x27;s our vision" not in bq and "That's our vision" not in bq:
            fail(f, 'blockquote that is not the official vision')
    for a in re.findall(r'<a\b[^>]*>', t):
        h = re.search(r'href="([^"]*)"', a)
        h = h.group(1) if h else ''
        if re.match(r'(https://wa\.me|tel:|https://www\.google\.com/maps|https://www\.facebook\.com|https://www\.instagram\.com)', h):
            if 'data-cta=' not in a or 'data-ref=' not in a:
                fail(f, 'CTA without data-cta/data-ref: ' + a[:90])
        if 'wa.me' in h and not h.startswith(WA):
            fail(f, 'wrong WhatsApp link ' + h[:60])
        if h.startswith('tel:') and h != 'tel:+60179773168':
            fail(f, 'wrong tel link ' + h)
        if 'instagram.com' in h and h != 'https://www.instagram.com/studio870407/':
            fail(f, 'wrong Instagram link')
        if 'facebook.com' in h and h != 'https://www.facebook.com/studio87hairstudio':
            fail(f, 'wrong Facebook link')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            d = json.loads(j)
        except Exception as e:
            fail(f, f'bad JSON-LD {e}')
            continue
        if d.get('@type') == 'HairSalon':
            if d.get('sameAs') != ['https://www.facebook.com/studio87hairstudio', 'https://www.instagram.com/studio870407/']:
                fail(f, 'HairSalon sameAs')
            if [h['opens'] for h in d['openingHoursSpecification']] != ['10:00', '11:00'] or d['openingHoursSpecification'][1]['dayOfWeek'] != ['Sunday']:
                fail(f, 'HairSalon hours')
            if not d['url'].startswith(CANON):
                fail(f, 'schema url not on live domain')
    for src in re.findall(r'(?:src|srcset|href)="' + re.escape(build.BASE) + r'((?:media|assets)/[^"?]+)', t):
        if not os.path.exists(os.path.join(DIST, src)) and src not in build.SERVER_MEDIA:
            fail(f, 'missing file ' + src)
    body = re.sub(r'<script.*?</script>', '', t, flags=re.S)
    miss = {c for c in body if ord(c) > 0x2E80 and not (0xFE00 <= ord(c) <= 0xFE0F)} - chars
    if miss:
        fail(f, 'CJK glyphs missing from font subset: ' + ''.join(sorted(miss))[:40])
    wk = re.findall(r'<figure class="wk">', t)
    if wk and len(re.findall(r'<figure class="wk"><picture>', t)) != len(wk):
        fail(f, 'work card without a photo')
for p in [p for p in pages if not p.startswith('zh/')]:
    if 'zh/' + p not in pages:
        fail(DIST, f'missing zh twin of /{p}')
if len(pages) != len(build.PAGES) * 2:
    fail(DIST, f'{len(pages)} pages built, expected {len(build.PAGES) * 2}')
sm = open(os.path.join(DIST, 'sitemap.xml'), encoding='utf8').read()
if sm.count('<loc>') != len(pages) or sm.count('hreflang="x-default"') != len(pages) or 'autoseo.my' in sm or 'hreflang="ms"' in sm:
    fail(os.path.join(DIST, 'sitemap.xml'), f'sitemap has {sm.count("<loc>")} urls for {len(pages)} pages')
if 'autoseo.my/preview' in open(os.path.join(DIST, 'llms.txt'), encoding='utf8').read():
    fail(os.path.join(DIST, 'llms.txt'), 'preview URL in llms.txt')

tmp = tempfile.mkdtemp()
shutil.copytree(DIST, os.path.join(tmp, 'preview', 'studio-87'))
r = subprocess.run([sys.executable, '/mnt/project-files/tracking/cta_check.py', '--dir', tmp], capture_output=True, text=True)
shutil.rmtree(tmp)
print(r.stdout.strip()[-400:])
if r.returncode:
    bad += 1
print(f'check: {len(files)} files, {len(pages)} pages, {bad} problem(s)')
sys.exit(1 if bad else 0)
