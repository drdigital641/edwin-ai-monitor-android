#!/usr/bin/env python3
"""Pre-upload gate for the JT Autoworks preview. Exit 1 on any problem. Run after build.py, before any Bridge upload.
Fails on: lorem / TODO / placeholder text, any trace of the other agency brand, the ACRA address, the landline as WhatsApp, star ratings or
aggregateRating, "Opening Promotion" (until Edwin confirms), "top rated", the owner name while the flag is off, previous-workshop
names, invented MRT/parking, em dashes, missing noindex, H1 count != 1, missing tracker, wrong footer credit, a CTA without
data-cta, wrong WhatsApp / tel links, bad JSON-LD, missing hreflang, map links not pinned to the Place ID, missing media files."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, '..', 'dist')
F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
# Words are split so this file never trips a repo-wide grep.
BANNED = [r'lorem', r'\bTODO\b', r'\bTBD\b', r'placeholder', r'\bXXX\b', 'pa' + r'ge[\s-]*o' + 'ne', 'pageo' + 'nesingapore',
          '10 Ubi' + r' Crescent', r'#01-36', 'wa.me/65' + '62223102', r'aggregate' + 'Rating', r'ratingValue', r'reviewCount', r'bestRating',
          '[★☆⭐]', r'top[\s-]rated', r'\b5\.0\b', r'Opening ' + r'Promotion', r'promosi pembukaan', r'开业优惠',
          'AMA ' + 'Automotive', 'Wah ' + 'Hong', r'\bMRT\b', r'\bparking\b', r'letak kereta', r'停车', r'Reel \d',
          r'servicing from S\$158', r'Honest car care, straight answers', r'quote before work starts', r'official dealer', r'authori[sz]ed dealer',
          r'\bJW Motoring\b', r'grayscale\(', r'mix-blend-mode']
if not F['flags']['show_owner_name']:
    BANNED += [r'Ah\s*Hao', r'阿豪']
bad = 0


def fail(f, m):
    global bad
    bad += 1
    print(f'FAIL {os.path.relpath(f, DIST)}: {m}')


WA = 'https://wa.me/6583584927?text='
files = [os.path.join(dp, f) for dp, _, fs in os.walk(DIST) for f in fs if f.endswith(('.html', '.txt', '.xml', '.js', '.css'))]
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
    if '<meta name="robots" content="noindex, nofollow">' not in t:
        fail(f, 'no noindex')
    if len(re.findall(r'<h1\b', t)) != 1:
        fail(f, 'H1 count != 1')
    if 'p1-cta.js' not in t:
        fail(f, 'no tracker')
    if t.count('Website by AutoSEO.my') != 1 or '<a href="https://autoseo.my/">Website by AutoSEO.my</a>' not in t:
        fail(f, 'footer credit')
    if len(re.findall(r'hreflang="(en|ms|zh-Hans|x-default)" href=', t)) != 4:
        fail(f, 'hreflang block')
    if not re.search(r'<nav class="tabs"', t):
        fail(f, 'language switcher (underline tabs) missing')
    for k in ('og:title', 'og:description', 'og:image', 'og:url'):
        if f'property="{k}"' not in t:
            fail(f, 'missing ' + k)
    for a in re.findall(r'<a\b[^>]*>', t):
        h = re.search(r'href="([^"]*)"', a)
        h = h.group(1) if h else ''
        if re.match(r'(https://wa\.me|tel:|mailto:|https://www\.google\.com/maps|https://maps\.google|https://search\.google|https://www\.facebook\.com|https://www\.instagram\.com)', h):
            if 'data-cta=' not in a or 'data-ref=' not in a:
                fail(f, 'CTA without data-cta/data-ref: ' + a[:90])
        if 'wa.me' in h and not h.startswith(WA):
            fail(f, 'wrong WhatsApp link ' + h[:60])
        if h.startswith('tel:') and h != 'tel:+6562223102':
            fail(f, 'wrong tel link')
        if re.match(r'https://(www\.google\.com/maps|search\.google\.com/local)', h) and F['place_id'] not in h:
            fail(f, 'map link not pinned to the Place ID: ' + h[:80])
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(j)
        except Exception as e:
            fail(f, f'bad JSON-LD {e}')
    for src in re.findall(r'(?:src|href|poster)="/preview/jt-autoworks/((?:media|assets)/[^"?]+)', t):
        if not os.path.exists(os.path.join(DIST, src)):
            fail(f, 'missing file ' + src)
    if '--need-media' in sys.argv:
        for need in ('media/og.jpg', 'media/logo'):
            if need not in t:
                fail(f, 'media not used: ' + need)

tmp = tempfile.mkdtemp()
shutil.copytree(DIST, os.path.join(tmp, 'preview', 'jt-autoworks'))
r = subprocess.run([sys.executable, '/mnt/project-files/tracking/cta_check.py', '--dir', tmp], capture_output=True, text=True)
shutil.rmtree(tmp)
print(r.stdout.strip()[-600:])
if r.returncode:
    bad += 1
print(f'check: {len(files)} files, {bad} problem(s)')
sys.exit(1 if bad else 0)
