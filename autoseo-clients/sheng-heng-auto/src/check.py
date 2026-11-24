#!/usr/bin/env python3
"""Pre-upload gate for Sheng Heng Auto (Edwin brief 24 Nov 2026). Exit 1 on any hit."""
import os, re, sys, json
D = sys.argv[1]
BAN = [
 (r'seri\s+orkid', re.I), (r'\b4\.6\b(?=[^<]{0,40}(star|rating|review|out of|/5))', re.I), (r'(star|rating|rated)[^<]{0,20}\b4\.6\b', re.I),
 (r'\b20 reviews\b', re.I), (r'aggregateRating', re.I), (r'5-star workshop', re.I), (r'rated 5', re.I), (r'page\s?one', re.I), (r'pageonesingapore', re.I),
 (r'lorem', re.I), (r'\bTODO\b', re.I), (r'placeholder(?!=)', re.I), (r'\bbest\b', re.I), (r'No\.\s?1\b', re.I), (r'number one', re.I),
 (r'guarantee', re.I), (r'warranty', re.I), (r'authori[sz]ed', re.I), (r'official dealer', re.I), (r'dealer-level', re.I), (r'\bkorean\b', re.I),
 (r'\bRM\s?\d', 0), (r'from RM', re.I), (r'LAUNCH', 0), (r'shopee', re.I), (r'auto restoration', re.I), (r'9780882671158100569', 0),
 (r'sofacare', re.I), (r'contiexpert', re.I), (r'edwin garage', re.I), (r'batteryrescue', re.I), (r'commercialfitout', re.I),
]
hits = []
for r, _, fs in os.walk(D):
    if '/images' in r.replace(D, ''):
        continue
    for f in fs:
        if not f.endswith(('.html', '.js', '.json', '.xml', '.txt', '.webmanifest', '.css')):
            continue
        p = os.path.join(r, f); t = open(p, encoding='utf-8').read()
        # placeholder= attribute on the review helper input is an HTML attribute, not copy
        t2 = re.sub(r'\.placeholder=|placeholder="', '', t)
        for pat, fl in BAN:
            for m in re.finditer(pat, t2, fl):
                hits.append(f'{os.path.relpath(p, D)}: {pat} -> {t2[max(0,m.start()-30):m.end()+30]!r}')
        for m in re.finditer(r'wa\.me/(\d+)', t):
            if m.group(1) != '60163352124': hits.append(f'{p}: wa.me {m.group(1)}')
        for m in re.finditer(r'tel:(\+?\d+)', t):
            if m.group(1) not in ('+60163352124', '+60137236688'): hits.append(f'{p}: tel {m.group(1)}')
        for m in re.finditer(r'<video[^>]*src="([^"]+)"', t):
            if not m.group(1).endswith('/video/v01-bmw-adas-calibration-9x16-720.mp4'): hits.append(f'{p}: video {m.group(1)}')
        for m in re.finditer(r'Website by[^<"]*', t):
            if m.group(0).strip() != 'Website by AutoSEO.my': hits.append(f'{p}: credit {m.group(0)}')
        for m in re.finditer(r'<a [^>]*>\s*Website by AutoSEO\.my', t):
            if 'href="https://autoseo.my/"' not in m.group(0): hits.append(f'{p}: credit link target')
print('\n'.join(hits) if hits else 'PRE-UPLOAD GREP: 0 hits')
sys.exit(1 if hits else 0)
