#!/usr/bin/env python3
"""Pre-upload gate for the KH Diesel preview (Edwin brief 23 Nov 2026). Exit 1 on any failure."""
import re, sys, os, glob, json
D = sys.argv[1]
BAN = [r'lorem', r'\bTODO\b', r'placeholder', r'Page One', r'pageonesingapore', r'Eastern Gateway', r'014-893 5358', r'0148935358',
       r'aggregateRating', r'Warehouse', r'authori[sz]ed Bosch', r'authori[sz]ed Denso', r'since 2017', r'two workshops', r'\bbest\b',
       r'No\.\s?1', r'guarantee', r'\bRM\s?\d', r'BAS PERSIA', r'Harvest Holidays', r'<video', r'\.mp4', r'terbaik', r'jaminan', r'最好', r'保证',
       r'photo of our (workshop|building)', r'real (customer )?jobs? (we|done)', r'noindex', r'—']
fail = []
files = [f for f in glob.glob(D + '/**/*', recursive=True) if f.endswith(('.html', '.js', '.css', '.xml', '.txt', '.json')) and '.build.json' not in f]
for f in files:
    t = open(f, encoding='utf-8').read()
    for b in BAN:
        for m in re.finditer(b, t, re.I):
            fail.append(f'{f[len(D):]}: banned "{m.group(0)}" …{t[max(0,m.start()-40):m.end()+30]!r}')
    for n in re.findall(r'wa\.me/(\d+)', t):
        if n != '60198545433': fail.append(f'{f}: wa.me {n}')
titles, descs = {}, {}
for f in glob.glob(D + '/**/index.html', recursive=True):
    t = open(f, encoding='utf-8').read(); p = f[len(D):]
    if len(re.findall(r'<h1[\s>]', t)) != 1: fail.append(f'{p}: h1 count')
    ti = re.search(r'<title>(.*?)</title>', t).group(1); de = re.search(r'name="description" content="(.*?)"', t).group(1)
    if ti in titles: fail.append(f'{p}: duplicate title with {titles[ti]}')
    if de in descs: fail.append(f'{p}: duplicate description with {descs[de]}')
    titles[ti] = p; descs[de] = p
    if not p.startswith(('/zh/',)) and len(__import__('html').unescape(ti)) > 60: fail.append(f'{p}: title {len(ti)} chars')
    for need in ['rel="canonical"', 'hreflang="x-default"', 'og:image:width', 'og:image:alt', 'p1-cta.js', '60198545433', 'Website by AutoSEO.my', 'privacy/"', 'application/ld+json']:
        if need not in t: fail.append(f'{p}: missing {need}')
    for img in re.findall(r'<img [^>]*>', t):
        alt = re.search(r'alt="([^"]*)"', img).group(1)
        if 'images/' in img and 'brand/' not in img and alt and not re.search(r'AI-generated|[Ii]llustrat', alt): fail.append(f'{p}: img alt without AI credit')
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        json.loads(m.group(1).replace('<\\/', '</'))
print('files', len(files), 'pages', len(titles))
print('\n'.join(fail[:60]) or 'GATE PASS')
sys.exit(1 if fail else 0)
