#!/usr/bin/env python3
"""Pre-upload gate for CCH Automotive. Fails (exit 1) on any banned word, wrong number, missing noindex, H1 count != 1,
missing tracker, rating/hours schema, wrong footer credit, or a CTA link without data-cta. Run after build.py."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, '..', 'dist')
BANNED = [r'lorem', r'\bTODO\b', r'page\s*one', r'pageonesingapore', r'012[-\s]?820[-\s]?1559', r'12[-\s]?820[-\s]?1559', r'018[-\s]?789[-\s]?3055',
          r'melaka', r'malacca', r'aggregateRating', r'openingHours', r'ratingValue', r'reviewCount', r'placeholder', r'\bXXX', r'\bSLUG\b',
          r'\bMon(day)?\s*[-–]\s*(Fri|Sat|Sun)', r'\b\d{1,2}(:\d\d)?\s?(am|pm)\b', r'\bopen daily\b', r'\b24/7\b', r'authori[sz]ed dealer',
          r'official (dealer|alpine|mercedes|bmw|audi)', r'hybrid specialist', r'EV certif', r'bentley', r'audi-r8-dark', r'MORE THEN', r'Programing',
          r'—', r'\bstars?\b', r'testimonial', r'\bRM\s?\d', r'since (19|20)\d\d', r'founded']
bad = 0
def fail(f, m):
    global bad; bad += 1; print(f'FAIL {os.path.relpath(f, DIST)}: {m}')
files = [os.path.join(dp, f) for dp, _, fs in os.walk(DIST) for f in fs if f.endswith(('.html', '.txt', '.xml', '.js', '.css'))]
for f in files:
    t = open(f, encoding='utf8').read()
    for b in BANNED:
        m = re.search(b, t, re.I)
        if m and not (f.endswith('.css') and b == r'\bstars?\b'):
            fail(f, f'banned "{m.group(0)}"')
    if not f.endswith('.html'):
        continue
    if '<meta name="robots" content="noindex, nofollow">' not in t: fail(f, 'no noindex')
    if len(re.findall(r'<h1\b', t)) != 1: fail(f, 'H1 count != 1')
    if 'p1-cta.js' not in t: fail(f, 'no tracker')
    if t.count('Website by AutoSEO.my') != 1 or '<a href="https://autoseo.my/">Website by AutoSEO.my</a>' not in t: fail(f, 'footer credit')
    for a in re.findall(r'<a\b[^>]*>', t):
        if re.search(r'href="(https://wa\.me|tel:|mailto:|https://www\.google\.com/maps|https://www\.facebook\.com)', a) and 'data-cta=' not in a:
            fail(f, 'CTA without data-cta: ' + a[:90])
        if 'wa.me' in a and 'wa.me/60109359391?text=' not in a: fail(f, 'wrong WhatsApp link')
        if 'tel:' in a and 'tel:+60109359391' not in a: fail(f, 'wrong tel link')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try: json.loads(j)
        except Exception as e: fail(f, f'bad JSON-LD {e}')
    for src in re.findall(r'src="/preview/cch-automotive/images/([^"]+)"', t):
        if 'audi' in src: fail(f, 'audi image used')
import shutil, tempfile
tmp = tempfile.mkdtemp(); shutil.copytree(DIST, os.path.join(tmp, 'preview', 'cch-automotive'))  # cta_check resolves /preview/... from a site root
r = subprocess.run([sys.executable, '/mnt/project-files/tracking/cta_check.py', '--dir', tmp], capture_output=True, text=True)
shutil.rmtree(tmp)
print(r.stdout.strip())
if r.returncode: bad += 1
print(f'check: {len(files)} files, {bad} problem(s)')
sys.exit(1 if bad else 0)
