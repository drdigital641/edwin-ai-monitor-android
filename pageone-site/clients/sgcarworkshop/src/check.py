#!/usr/bin/env python3
"""Link checker + JSON-LD parse + banned words.  python3 check.py [sitedir]"""
import json, os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin, unquote
root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'site'))
BAN = re.compile(r"\b(best|no\.? ?1|#1|guaranteed?|aggregaterating|ratingvalue)\b", re.I)
bad = 0
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links = []; s.ld = []; s.in_ld = False; s.text = []; s.skip = 0; s.noindex = False
    def handle_starttag(s, t, a):
        a = dict(a)
        if t in ('a', 'link') and a.get('href'): s.links.append(a['href'])
        if t in ('img', 'script') and a.get('src'): s.links.append(a['src'])
        if t == 'script' and a.get('type') == 'application/ld+json': s.in_ld = True; s.ld.append('')
        elif t in ('script', 'style'): s.skip += 1
        if t == 'meta' and a.get('name') == 'robots' and 'noindex' in a.get('content', ''): s.noindex = True
    def handle_endtag(s, t):
        if t == 'script' and s.in_ld: s.in_ld = False
        elif t in ('script', 'style'): s.skip -= 1
    def handle_data(s, d):
        if s.in_ld: s.ld[-1] += d
        elif not s.skip: s.text.append(d)
files = [os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs if f.endswith('.html')]
for f in sorted(files):
    rel = os.path.relpath(f, root)
    p = P(); src = open(f, encoding='utf-8').read(); p.feed(src)
    if p.noindex and rel != '404.html': print('NOINDEX in', rel); bad += 1
    for j in p.ld:
        try: json.loads(j)
        except Exception as e: print('BAD JSON-LD', rel, e); bad += 1
    txt = ' '.join(p.text)
    for m in BAN.finditer(txt + ' '.join(p.ld)): print('BANNED', rel, m.group(0)); bad += 1
    if '404.html' == rel: continue
    base = '/' + rel.replace('index.html', '')
    for l in p.links:
        u = urlparse(l)
        if u.scheme in ('http', 'https', 'mailto', 'tel') or l.startswith('#') or l.startswith('data:'): continue
        t = unquote(urljoin(base, u.path))
        fp = os.path.join(root, t.lstrip('/'))
        if os.path.isdir(fp): fp = os.path.join(fp, 'index.html')
        if not os.path.isfile(fp): print('BROKEN', rel, '->', l); bad += 1
    if rel == 'index.html': print('home visible words:', len(re.findall(r"\w+", txt)))
    if rel.startswith('workshops/wei'): print('wei visible words:', len(re.findall(r"\w+", txt)))

# ---- Tier audit (PLAN.md Tiers, permanent rule): a higher tier never has less info or fewer conversion options than a lower one.
# Basic (free) now has a SHORT own page. Feature columns must satisfy  Basic < Verified <= Premium  (strict between Basic and Verified).
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import ENTRIES, TIERS
FEAT = ['photos', 'services_detail', 'faqs', 'gallery']          # numeric counts: Basic < Verified (Wei) <= Premium
MINIMUM = {'photos': 3, 'services_detail': 3, 'faqs': 3, 'gallery': 1}
CONV = ['contact', 'address', 'map', 'hours', 'rating']          # Basic must have all; hours/rating shown for information
def audit(a):
    jobs = len(re.findall(r'<figure class="rv job">', a))
    illus = len(re.findall(r'<figure class="rv illus">', a))
    return {
        'photos': jobs + len(re.findall(r'class="hero-ph(?: gph)?"[^>]*>(?:<img|<div class="tile ini")', a)),
        'services_detail': len(re.findall(r'<li class="svc ', a)),
        'faqs': len(re.findall(r'<details class="faq">', a)),
        'gallery': jobs + illus,
        'contact': bool(re.search(r'href="tel:\+\d+"[^>]*data-cta="call_dir_', a)) or bool(re.search(r'href="https://wa\.me/\d+\?text=[^"]*"[^>]*data-cta="whatsapp_dir_', a)),
        'address': 'data-addr' in a,
        'map': 'data-map' in a,
        'hours': 'class="hours"' in a,
        'rating': 'class="reviews-line"' in a,
    }
def both_buttons(a):
    return bool(re.search(r'href="tel:\+\d+"[^>]*data-cta="call_dir_', a)) and bool(re.search(r'href="https://wa\.me/\d+\?text=[^"]*"[^>]*data-cta="whatsapp_dir_', a))
rows, wei = [], None
for e in ENTRIES:
    f = os.path.join(root, 'workshops', e['slug'], 'index.html')
    if not os.path.isfile(f):
        print('MISSING PAGE', e['slug'], e['tier']); bad += 1; continue
    h = open(f, encoding='utf-8').read()
    r = audit(h); r['both_buttons'] = both_buttons(h)
    if e['slug'].startswith('wei'): wei = r
    rows.append((e, r))
cols = FEAT + CONV + ['both_buttons']
print('\nTier audit  (rule: Basic < Verified <= Premium on ' + ', '.join(FEAT) + '; Basic keeps contact, address, map, hours)')
print('%-28s %-16s %s' % ('listing', 'tier', ' '.join('%-15s' % c for c in cols)))
for e, r in rows:
    v = lambda x: (str(x) if isinstance(x, int) and not isinstance(x, bool) else ('yes' if x else 'NO'))
    notes = []
    if e['tier'] == 'free':
        for c in CONV[:4]:
            if not r[c]: notes.append('Basic missing ' + c)
        for c in FEAT:
            if wei and not r[c] < wei[c]: notes.append('Basic %s %s not < Verified %s' % (c, r[c], wei[c]))
        if r['both_buttons']: notes.append('Basic must have one contact button, not both')
    elif e['tier'] == 'premium_leadgen' and wei:
        for c in FEAT:   # Premium must reach Verified's level (capped at the thresholds below: 3 photos, 3 services, 3 FAQs, 1 gallery item)
            need = min(wei[c], MINIMUM[c])
            if r[c] < need: notes.append('Premium %s %s < Verified minimum %s' % (c, r[c], need))
        for c in ('contact', 'address', 'map', 'rating', 'both_buttons'):
            if wei[c] and not r[c]: notes.append('Premium missing ' + c)
    elif e['tier'] == 'premium':
        for c in ('contact', 'address', 'map', 'rating', 'both_buttons'):
            if not r[c]: notes.append('Verified missing ' + c)
        for c in FEAT:
            if r[c] < MINIMUM[c]: notes.append('Verified %s %s < %s' % (c, r[c], MINIMUM[c]))
    if notes: bad += 1
    print('%-28s %-16s %s %s' % (e['name'], e['tier'], ' '.join('%-15s' % v(r[c]) for c in cols), ('FAIL: ' + '; '.join(notes)) if notes else 'ok'))
# Wei (Verified) hours now come from its Google listing (checked 1 Nov 2026), so every tier shows hours.
home_src = open(os.path.join(root, 'index.html'), encoding='utf-8').read()
for e in ENTRIES:
    if e['tier'] == 'free':
        m = re.search(r'<article class="card basic"[^>]*>(?:(?!</article>).)*data-cta="(?:whatsapp|call)_dir_%s"(?:(?!</article>).)*href="[^"]*workshops/%s/"' % (e['slug'], e['slug']), home_src, re.S)
        if not m or 'Claim or remove' not in home_src: print('BASIC card incomplete (needs contact + View link)', e['slug']); bad += 1
        pg = open(os.path.join(root, 'workshops', e['slug'], 'index.html'), encoding='utf-8').read()
        ld = [json.loads(j) for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', pg, re.S)]
        if len(ld) != 1 or set(ld[0]) - {'@context', '@type', 'name', 'url', 'address', 'telephone', 'openingHours', 'geo'}: print('BASIC schema not minimal', e['slug']); bad += 1
        for needle in ('data-cta="claim_%s"' % e['slug'], 'Is this your workshop?', 'From the workshop', 'Rated '):
            if needle not in pg: print('BASIC page missing', needle, e['slug']); bad += 1
        for banned in ('class="faq"', 'class="gal"', 'class="svc ', 'FAQPage', 'Review'):
            if banned in pg: print('BASIC page has Verified-only content', banned, e['slug']); bad += 1
sm = open(os.path.join(root, 'sitemap.xml')).read(); lt = open(os.path.join(root, 'llms.txt')).read()
for e in ENTRIES:
    if ('workshops/%s/' % e['slug']) not in sm or ('workshops/%s/' % e['slug']) not in lt: print('NOT in sitemap/llms.txt', e['slug']); bad += 1
print('pages checked:', len(files), 'problems:', bad)
sys.exit(1 if bad else 0)
