#!/usr/bin/env python3
"""Pre-upload gate for CCH Automotive. Fails (exit 1) on any banned word, wrong number, missing noindex, H1 count != 1,
missing tracker, rating/hours schema, wrong footer credit, or a CTA link without data-cta. Run after build.py."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import strings_en, strings_ms, strings_zh
CREDIT = {'en': strings_en.UI['credit'], 'ms': strings_ms.UI['credit'], 'zh': strings_zh.UI['credit']}
HTML_LANG = {'en': 'en', 'ms': 'ms', 'zh': 'zh-Hans'}
DIST = os.path.join(HERE, '..', 'dist')
BANNED = [r'lorem', r'\bTODO\b', 'pa'+r'ge\s*o'+'ne', 'pageo'+'nesingapore', r'012[-\s]?820[-\s]?1559', r'12[-\s]?820[-\s]?1559', r'018[-\s]?789[-\s]?3055',
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
    if f.endswith('sitemap.xml'):
        n_loc, n_alt = t.count('<loc>'), t.count('<xhtml:link')
        if n_loc != 39 or n_alt != n_loc * 4: fail(f, f'sitemap {n_loc} locs / {n_alt} hreflang links (want 39 / 156)')
    if not f.endswith('.html'):
        continue
    if '<meta name="robots" content="noindex, nofollow">' not in t: fail(f, 'no noindex')
    if len(re.findall(r'<h1\b', t)) != 1: fail(f, 'H1 count != 1')
    if 'p1-cta.js' not in t: fail(f, 'no tracker')
    rel = os.path.relpath(f, DIST).replace(os.sep, '/')
    lc = rel.split('/')[0] if rel.split('/')[0] in ('ms', 'zh') else 'en'
    if t.count(CREDIT[lc]) != 1 or f'<a href="https://autoseo.my/">{CREDIT[lc]}</a>' not in t: fail(f, 'footer credit')
    if f'<html lang="{HTML_LANG[lc]}">' not in t: fail(f, 'html lang')
    for code in ('en', 'ms', 'zh-Hans', 'x-default'):
        if f'hreflang="{code}" href=' not in t: fail(f, f'hreflang {code} missing')
    if len(re.findall(r'<nav class="lang-sw', t)) != 2 or '>BM</a>' not in t or '>中文</a>' not in t: fail(f, 'language switcher')
    if lc != 'en' and re.search(r'wa\.me/[^"]*\?text=Hi%20CCH%20Automotive%2C%20I%27d', t): fail(f, 'English WhatsApp prefill on ' + lc)
    if lc != 'en':
        tw = os.path.join(DIST, rel[3:])
        if not os.path.exists(tw): fail(f, 'no English twin')
    else:
        for o in ('ms', 'zh'):
            if not os.path.exists(os.path.join(DIST, o, rel)): fail(f, f'no {o} twin')
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
