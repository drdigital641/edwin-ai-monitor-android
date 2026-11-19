#!/usr/bin/env python3
"""Pre-upload gate for the Rasa Sayang Automotive preview. Exit 1 on any problem. Run after build.py, before any Bridge upload.
Fails on: lorem / TODO / placeholder text, any Page One trace, a founding-year claim, the old-site business-name wording,
the unresolved Facebook domain, ratings / reviews / hours, em dashes in visible copy, missing noindex, H1 count != 1,
missing tracker, wrong footer credit, a CTA link without data-cta, wrong WhatsApp / tel number, bad JSON-LD, missing hreflang,
an image that is not in the drop list."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, '..', 'dist')
sys.path.insert(0, HERE)
from build import PHOTOS  # noqa: E402  (importing build does not run it)

OK_IMAGES = set(PHOTOS) | {s + '-full' for s in PHOTOS} | {'cover', 'og', 'logo-transparent', 'logo-on-black', 'favicon-512'}
# Words are split so this file itself never trips a repo-wide grep.
BANNED = [r'lorem', r'\bTODO\b', r'\bTBD\b', r'placeholder', r'\bXXX\b', 'pa' + r'ge[\s-]*o' + 'ne', 'pageo' + 'nesingapore',
          r'since\s+(19|20)\d\d', r'sejak\s+(19|20)\d\d', r'(19|20)\d\d\s*年(成立|创立|起)', r'\b1991\b', r'founded', r'established in',
          'Automo' + 'bile', 'rasasayang' + r'auto\.com', 'rasasayang' + r'automotive\.com',
          r'aggregateRating', r'ratingValue', r'reviewCount', r'openingHours', r'"review"', r'testimonial', r'\bstars?\b',
          r'\bMon(day)?\s*[-–]\s*(Fri|Sat|Sun)', r'\b\d{1,2}(:\d\d)?\s?(am|pm)\b', r'\bopen daily\b', r'\b24/7\b',
          r'\bRM\s?\d', r'authori[sz]ed dealer', r'official (dealer|service)', r'warrant(y|ies)', r'guarantee', r'@[a-z0-9-]+\.(com|my)\b',
          r'grand opening', r'spray paint', r'windscreen', r'wheel alignment', r'body ?kit', r'welding']
bad = 0


def fail(f, m):
    global bad
    bad += 1
    print(f'FAIL {os.path.relpath(f, DIST)}: {m}')


files = [os.path.join(dp, f) for dp, _, fs in os.walk(DIST) for f in fs if f.endswith(('.html', '.txt', '.xml', '.js', '.css'))]
for f in files:
    t = open(f, encoding='utf8').read()
    for b in BANNED:
        m = re.search(b, t, re.I)
        if m and not (f.endswith(('.css', '.js')) and b in (r'\bstars?\b', r'placeholder')):
            fail(f, f'banned "{m.group(0)}"')
    if '—' in t:
        fail(f, 'em dash in copy (the client slogan is escaped inside JSON-LD only)')
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
    if 'og:image" content="https://autoseo.my/preview/rasa-sayang/images/og.webp"' not in t and '--live' not in sys.argv:
        fail(f, 'og:image')
    for a in re.findall(r'<a\b[^>]*>', t):
        if re.search(r'href="(https://wa\.me|tel:|https://www\.google\.com/maps|https://waze\.com|https://www\.facebook\.com)', a) and 'data-cta=' not in a:
            fail(f, 'CTA without data-cta: ' + a[:90])
        if 'wa.me' in a and 'https://wa.me/60166641686?text=' not in a:
            fail(f, 'wrong WhatsApp link')
        if 'tel:' in a and 'href="tel:+60166641686"' not in a:
            fail(f, 'wrong tel link')
        if 'mailto:' in a:
            fail(f, 'email link (no email is published)')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(j)
        except Exception as e:
            fail(f, f'bad JSON-LD {e}')
    for stem in re.findall(r'/images/([a-z0-9-]+)\.(?:webp|png)', t):
        if stem not in OK_IMAGES:
            fail(f, f'image not in the drop: {stem}')

tmp = tempfile.mkdtemp()
shutil.copytree(DIST, os.path.join(tmp, 'preview', 'rasa-sayang'))
r = subprocess.run([sys.executable, '/mnt/project-files/tracking/cta_check.py', '--dir', tmp], capture_output=True, text=True)
shutil.rmtree(tmp)
print(r.stdout.strip())
if r.returncode:
    bad += 1
print(f'check: {len(files)} files, {bad} problem(s)')
sys.exit(1 if bad else 0)
