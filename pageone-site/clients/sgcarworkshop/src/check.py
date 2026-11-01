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

# ---- Tier audit (PLAN.md Tiers, permanent rule): a premium page must never have less than Wei's page or than a free card.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import ENTRIES, TIERS
CRIT = ['photos>=3', 'phone', 'whatsapp', 'address', 'map', 'services>=3', 'faqs>=3', 'reviews']
def audit(html_src):
    a = html_src
    return {
        'photos>=3': len(re.findall(r'<figure class="rv job">', a)) + (1 if 'class="hero-ph"><img' in a else 0) >= 3,
        'phone': bool(re.search(r'href="tel:\+\d+"', a)),
        'whatsapp': bool(re.search(r'href="https://wa\.me/\d+\?text=', a)),
        'address': 'data-addr' in a,
        'map': 'data-map' in a,
        'services>=3': len(re.findall(r'<li class="svc ', a)) >= 3,
        'faqs>=3': len(re.findall(r'<details class="faq">', a)) >= 3,
        'reviews': 'class="reviews-line"' in a,
    }
FREE_CARD = {c: False for c in CRIT}   # a free card: name, description, categories, area, website link only
rows, wei = [], None
for e in ENTRIES:
    f = os.path.join(root, 'workshops', e['slug'], 'index.html')
    r = audit(open(f, encoding='utf-8').read()) if os.path.isfile(f) else {c: False for c in CRIT}
    if e['tier'] == 'premium' and e['slug'].startswith('wei'): wei = r
    rows.append((e, r))
baseline = {c: (wei or {}).get(c, True) for c in CRIT}
print('\nTier audit (columns: ' + ', '.join(CRIT) + ')')
print('%-24s %-18s %s  %s' % ('listing', 'tier', ' '.join('%-12s' % c for c in CRIT), 'score'))
for e, r in rows:
    miss = [c for c in CRIT if not r[c]]
    score = sum(r.values())
    fail = e['tier'] != 'free' and (score < sum(baseline.values()) or score <= sum(FREE_CARD.values()) or bool(miss))
    if fail: bad += 1
    print('%-24s %-18s %s  %d/8 %s' % (e['name'], e['tier'], ' '.join('%-12s' % ('yes' if r[c] else 'NO') for c in CRIT), score, ('FAIL: missing ' + ', '.join(miss)) if fail else 'ok'))
print('pages checked:', len(files), 'problems:', bad)
sys.exit(1 if bad else 0)
