#!/usr/bin/env python3
"""Pre-upload gate for S & P Precision Parts (Monaer). Exit 1 on any problem. Run after build.py, before any Bridge upload."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DIST = os.path.join(HERE, '..', 'dist')
F = json.load(open(os.path.join(HERE, 'facts.json'), encoding='utf8'))
bad = []
BAN = [r'RM\s?\d', r'warrant', r'jaminan', r'保修|质保|保固', r'IATF', r'\bCCC\b', r'ISO\s?9', r'(?-i:\bECE\b)', r'Hengshui', r'made in', r'British', r'London', r'英国', r'(?-i:\bUK\b)', r'European', r'欧洲|Eropah',
       r'Mr\.? ?Rover', r'Gelang Patah', r'Page One', r'lt-automart', r'TODO|lorem', r'—', r'noindex', r'exclusive|sole distributor|eksklusif|独家|总代理']
pages = []
for r, _, fs in os.walk(DIST):
    for f in fs:
        if f.endswith('.html'):
            pages.append(os.path.join(r, f))
for p in pages:
    h = open(p, encoding='utf8').read(); rel = os.path.relpath(p, DIST)
    txt = re.sub(r'<script[^>]*ld\+json[^>]*>.*?</script>', '', h, flags=re.S)
    for b in BAN:
        m = re.search(b, txt, flags=re.I)
        if m: bad.append(f'{rel}: banned "{m.group(0)}"')
    if len(re.findall(r'<h1[ >]', h)) != 1: bad.append(f'{rel}: h1 count')
    if 'p1-cta.js' not in h: bad.append(f'{rel}: tracker missing')
    for a in re.findall(r'<a [^>]*href="(?:https://wa\.me|tel:|mailto:)[^>]*>', h):
        if 'data-cta=' not in a: bad.append(f'{rel}: untracked CTA {a[:80]}')
    for n in re.findall(r'wa\.me/(\d+)', h):
        if n != '60168556611': bad.append(f'{rel}: wrong WA number {n}')
    for k in ('rel="canonical"', 'hreflang="x-default"', 'og:image', 'application/ld+json'):
        if k not in h: bad.append(f'{rel}: missing {k}')
    if h.count('hreflang="') < 4: bad.append(f'{rel}: hreflang')
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, flags=re.S):
        json.loads(m)
    t = re.search(r'<title>(.*?)</title>', h).group(1); d = re.search(r'name="description" content="(.*?)"', h).group(1)
    if len(d) > 175: bad.append(f'{rel}: meta {len(d)} chars')
    for src in re.findall(r'(?:src|srcset|href)="(/preview/sp-precision-parts/(?:media|assets)/[^"?]+)', h):
        if not os.path.exists(os.path.join(DIST, src.split('/preview/sp-precision-parts/')[1])): bad.append(f'{rel}: missing file {src}')
if len(pages) != 36: bad.append(f'page count {len(pages)}')
sm = open(os.path.join(DIST, 'sitemap.xml')).read()
if sm.count('<url>') != 36: bad.append('sitemap url count %d' % sm.count('<url>'))
from PIL import Image
if Image.open(os.path.join(DIST, 'media', 'og.jpg')).size != (1200, 630): bad.append('og size')
if F['workshops'] and not all(w.get('confirmed') for w in F['workshops']): bad.append('unconfirmed workshop in facts.json')
print('\n'.join(bad) or f'OK: {len(pages)} pages pass')
sys.exit(1 if bad else 0)
