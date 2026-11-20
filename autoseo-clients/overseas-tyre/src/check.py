#!/usr/bin/env python3
"""Pre-upload gate for the Overseas Tyre preview. Exit 1 on any problem. Run after build.py, before any Bridge upload.
Fails on: lorem / TODO / placeholder text, any trace of the other agency brand, aggregateRating or rating schema, the unconfirmed
fascia landline anywhere (it may not be published until Edwin confirms), label prices (RM + number), Michelin logo files used as
chrome, a per-page robots meta (noindex comes from the preview host header only), Continental captions, the neighbour workshop's
name, em dashes, H1 count != 1, missing tracker, wrong footer credit, a CTA without data-cta/data-ref, wrong WhatsApp / tel links,
map links not pinned to the listing, bad JSON-LD, missing hreflang, missing local files, and runs tracking/cta_check.py."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, '..', 'dist')
F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
# Words are split so this file never trips a repo-wide grep.
BANNED = [r'lorem', r'\bTODO\b', r'\bTBD\b', r'placeholder', r'\bXXX\b', 'pa' + r'ge[\s-]*o' + 'ne', 'pageo' + 'nesingapore',
          r'aggregate' + 'Rating', r'ratingValue', r'reviewCount', r'bestRating',
          '232[\\s-]*' + '4524', '72324' + '524',                 # unconfirmed fascia landline
          r'\bRM\s?\d', r'\bMYR\s?\d',                            # no label prices
          r'bibendum', r'michelin[-_]?logo', r'<meta name="robots"',
          r'\bHX\b', r'HX Auto', r'ChIJ', r'Singapore branch', r'cawangan Singapura', r'新加坡分行',
          r'mix-blend-mode', r'grayscale\(']
WA = F['whatsapp']['url'] + '?text='
TELS = {F['whatsapp']['tel'], F['manager']['tel'], F['landline']['tel']}
MAPS = {F['links']['maps'], F['links']['maps_cid'], F['links']['map_embed']}
bad = 0


def fail(f, m):
    global bad
    bad += 1
    print(f'FAIL {os.path.relpath(f, DIST)}: {m}')


files = [os.path.join(dp, f) for dp, _, fs in os.walk(DIST) for f in fs if f.endswith(('.html', '.txt', '.xml', '.js', '.css'))
         and '/images' not in dp]
html_n = 0
for f in files:
    t = open(f, encoding='utf8').read()
    for b in BANNED:
        m = re.search(b, t, re.I)
        if m and not (f.endswith(('.css', '.js')) and b == 'placeholder'):
            fail(f, f'banned "{m.group(0)}"')
    if '—' in t:
        fail(f, 'em dash')
    if not f.endswith('.html'):
        continue
    html_n += 1
    if len(re.findall(r'<h1\b', t)) != 1:
        fail(f, 'H1 count != 1')
    if 'p1-cta.js' not in t:
        fail(f, 'no tracker')
    if t.count('Website by AutoSEO.my') != 1 or '<a href="https://autoseo.my/">Website by AutoSEO.my</a>' not in t:
        fail(f, 'footer credit')
    if len(re.findall(r'hreflang="(en|ms|zh-Hans|x-default)" href=', t)) != 4:
        fail(f, 'hreflang block')
    if t.count('<nav class="lang"') != 2:
        fail(f, 'language switcher missing')
    for k in ('og:title', 'og:description', 'og:image', 'og:url'):
        if f'property="{k}"' not in t:
            fail(f, 'missing ' + k)
    for cap in re.findall(r'<figcaption>(.*?)</figcaption>', t, re.S):
        if re.search(r'continental', cap, re.I):
            fail(f, 'Continental in a photo caption')
    for a in re.findall(r'<a\b[^>]*>', t):
        h = re.search(r'href="([^"]*)"', a)
        h = (h.group(1) if h else '').replace('&amp;', '&')
        if re.match(r'(https://wa\.me|tel:|mailto:|https://(www\.)?google\.com/maps|https://maps\.google|https://www\.waze|https://www\.facebook\.com|https://www\.michelin)', h):
            if 'data-cta=' not in a or 'data-ref=' not in a:
                fail(f, 'CTA without data-cta/data-ref: ' + a[:90])
        if 'wa.me' in h and not h.startswith(WA):
            fail(f, 'wrong WhatsApp link ' + h[:60])
        if h.startswith('tel:') and h not in TELS:
            fail(f, 'tel link not in facts: ' + h)
        if re.match(r'https://(www\.google\.com/maps|maps\.google)', h) and h not in MAPS:
            fail(f, 'map link not pinned to the listing: ' + h[:80])
    for src in re.findall(r'<iframe[^>]*src="([^"]+)"', t):
        if src.replace('&amp;', '&') not in MAPS:
            fail(f, 'unknown iframe ' + src[:60])
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(j)
        except Exception as e:
            fail(f, f'bad JSON-LD {e}')
    d = os.path.dirname(f)
    for src in re.findall(r'(?:src|srcset|href)="((?:\.\./)*(?:assets|p1-cta)[^"?#]*)', t):
        if not os.path.exists(os.path.normpath(os.path.join(d, src))):
            fail(f, 'missing file ' + src)
    for src in re.findall(r'(?:src|srcset)="((?:\.\./)*images/[^"?#]+)', t):
        stem = os.path.basename(src).rsplit('.', 1)[0]
        if stem not in F['photos']:
            fail(f, 'image not in the drop: ' + src)

tmp = tempfile.mkdtemp()
shutil.copytree(DIST, os.path.join(tmp, 'preview', 'overseas-tyre'), ignore=shutil.ignore_patterns('images'))
r = subprocess.run([sys.executable, '/mnt/project-files/tracking/cta_check.py', '--dir', tmp], capture_output=True, text=True)
shutil.rmtree(tmp)
print(r.stdout.strip()[-500:])
if r.returncode:
    bad += 1
print(f'check: {len(files)} files ({html_n} pages), {bad} problem(s)')
sys.exit(1 if bad else 0)
