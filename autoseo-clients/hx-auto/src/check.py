#!/usr/bin/env python3
"""Pre-upload gate for the HX Auto Service preview. Exit 1 on any problem. Run after build.py, before any Bridge upload.
Fails on: lorem / TODO / placeholder text, any Page One trace, the unpublished second number, an invented email, the negative
reviewers, the old domain, car wash as a service, staff-page claims, em dashes, missing noindex, H1 count != 1, missing tracker,
wrong footer credit, a CTA link without data-cta, wrong WhatsApp / tel number, bad JSON-LD, missing hreflang, brand logo files,
an image that is not in the drop list."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, '..', 'dist')
sys.path.insert(0, HERE)
from build import PHOTOS  # noqa: E402

OK_IMAGES = set(PHOTOS) | {'hx/' + s + x for s in ('shopfront-signboard', 'shopfront-forecourt', 'workshop-bays-overview', 'aircond-flushing-banner', 'mercedes-c-class-bay', 'bmw-5-series-engine', 'bmw-5-series-on-lift', 'land-rover-discovery-sport', 'mini-cooper-s-on-lift', 'kia-cerato-on-lift', 'toyota-alphard-white', 'toyota-vellfire-bay', 'mazda-3-engine', 'honda-jazz-engine') for x in ('-t', '-l', '-xl')} | {'hx/hero-960', 'hx/hero-1600', 'hx/hero-2400'} | {'hx/' + s for s in ('hero-merc-portrait', 'hero-merc-wide', 'bays-overview-wide', 'amg-matte-card', 'bmw-lift-card', 'mini-card', 'vios-red-card', 'qashqai-card', 'hrv-card', 'alphard-card')} | {s + '-full' for s in PHOTOS} | {'cover', 'og', 'logo-transparent', 'logo-on-black', 'favicon-512'}
# Words are split so this file never trips a repo-wide grep.
BANNED = [r'lorem', r'\bTODO\b', r'\bTBD\b', r'placeholder', r'\bXXX\b', 'pa' + r'ge[\s-]*o' + 'ne', 'pageo' + 'nesingapore',
          '019' + r'[\s-]*319[\s-]*9113', r'\+?60\s*19[\s-]*319[\s-]*9113', '6019' + '3199113',
          r'[a-z0-9._-]+@[a-z0-9-]+\.[a-z]{2,}', r'mailto:', r'\bIvan\b', r'\bVictor\b', 'hx' + r'auto\.my', 'hxauto' + r'\.',
          r'car ?wash', r'cuci kereta', r'洗车', r'\bReel \d', r'since\s+(19|20)\d\d', r'sejak\s+(19|20)\d\d', r'founded',
          r'authori[sz]ed dealer', r'official dealer', r'"latitude"', r'"geo"', r'Always open', r'24/7',
          r'logo-(bmw|mercedes|benz|toyota|honda|lexus|audi|porsche|alpine|vw|volkswagen)',
          # Fix round 1 (Edwin, 19 Nov 2026): no star ratings or rating numbers anywhere.
          r'aggregateRating', r'ratingValue', r'reviewRating', r'bestRating', r'out of 5', r'daripada 5', r'满分', '[\u2605\u2606\u2b50]',
          r'\b4\.0\b(?!\.)', r'Google rating', r'penilaian Google', r'评分',
          # Fix round 2 (Edwin, 19 Nov 2026): no June flyer promos, no review count, no photo grade.
          r'\bflyer\b', r'RM\s?30', r'percuma', r'免费', r'传单', r'\d+\s*reviews on Google', r'\d+\s*ulasan di Google', r'Google 上有\d',
          r'grayscale\(', r'mix-blend-mode', r'sepia\(']
bad = 0
FACTS = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
GOOGLE_TEXT = {s['text'] for s in FACTS['reviews']['snippets']}  # Google + Facebook snippets, word for word


def fail(f, m):
    global bad
    bad += 1
    print(f'FAIL {os.path.relpath(f, DIST)}: {m}')


files = [os.path.join(dp, f) for dp, _, fs in os.walk(DIST) for f in fs if f.endswith(('.html', '.txt', '.xml', '.js', '.css'))]
for f in files:
    t = open(f, encoding='utf8').read()
    for b in BANNED:
        m = re.search(b, t, re.I)
        if m and not (f.endswith(('.css', '.js')) and b in (r'placeholder', r'mailto:', r'[a-z0-9._-]+@[a-z0-9-]+\.[a-z]{2,}')):
            fail(f, f'banned "{m.group(0)}"')
    if '—' in t:
        fail(f, 'em dash')
    if not f.endswith('.html'):
        continue
    # every review quote must be a Google snippet from facts.json, word for word
    import html as _h
    for q in re.findall(r'<li class="qc[^"]*"><blockquote[^>]*><p>(.*?)</p>', t):
        if _h.unescape(q) not in GOOGLE_TEXT:
            fail(f, f'review text not verbatim from facts.json: {q[:60]}')
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
    if '--live' not in sys.argv and 'og:image" content="https://autoseo.my/preview/hx-auto/images/og.jpg?v=2"' not in t:
        fail(f, 'og:image')
    if not re.search(r'<nav class="ut"', t):
        fail(f, 'language switcher (underline tabs) missing')
    for a in re.findall(r'<a\b[^>]*>', t):
        if re.search(r'href="(https://wa\.me|tel:|https://g\.co|https://www\.google\.com/maps|https://waze\.com|https://www\.facebook\.com)', a) and 'data-cta=' not in a:
            fail(f, 'CTA without data-cta: ' + a[:90])
        if 'wa.me' in a and 'https://wa.me/601167761138?text=' not in a:
            fail(f, 'wrong WhatsApp link')
        if 'tel:' in a and 'href="tel:+601167761138"' not in a:
            fail(f, 'wrong tel link')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(j)
        except Exception as e:
            fail(f, f'bad JSON-LD {e}')
    for stem in re.findall(r'/images/([a-z0-9/-]+)\.(?:webp|png)', t):
        if stem not in OK_IMAGES:
            fail(f, f'image not in the drop: {stem}')

tmp = tempfile.mkdtemp()
shutil.copytree(DIST, os.path.join(tmp, 'preview', 'hx-auto'))
r = subprocess.run([sys.executable, '/mnt/project-files/tracking/cta_check.py', '--dir', tmp], capture_output=True, text=True)
shutil.rmtree(tmp)
print(r.stdout.strip()[-600:])
if r.returncode:
    bad += 1
print(f'check: {len(files)} files, {bad} problem(s)')
sys.exit(1 if bad else 0)
