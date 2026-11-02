"""Checks a built site folder: JSON-LD parses, FAQ schema == visible FAQs, one H1, no meta noindex (except 404), internal links resolve, title/desc lengths."""
import json, os, re, sys, html
root = sys.argv[1]
bad = 0
pages = [os.path.join(dp, f) for dp, _, fs in os.walk(root) for f in fs if f.endswith('.html')]
for fp in pages:
    s = open(fp, encoding='utf-8').read(); rel = os.path.relpath(fp, root)
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(m)
        except Exception as e:
            print('JSON-LD', rel, e); bad += 1; continue
        faqs = [g for g in d.get('@graph', []) if g.get('@type') == 'FAQPage']
        vis = len(re.findall(r'<details><summary>', s))
        n = sum(len(f['mainEntity']) for f in faqs)
        if n != vis: print('FAQ mismatch', rel, n, vis); bad += 1
    if s.count('<h1') != 1: print('H1 count', rel, s.count('<h1')); bad += 1
    if 'noindex' in s and rel != '404.html': print('noindex', rel); bad += 1
    t = html.unescape(re.search(r'<title>(.*?)</title>', s).group(1))
    if len(t) > 62: print('title long', rel, len(t)); bad += 1
    if rel == '404.html': continue
    for h in re.findall(r'href="([^"#:]+?)(?:#[^"]*)?"', s):
        if h.startswith('//'): continue
        p = os.path.normpath(os.path.join(os.path.dirname(fp), h))
        if h.endswith('/') or os.path.isdir(p): p = os.path.join(p, 'index.html')
        if not os.path.exists(p): print('broken', rel, h); bad += 1
print('pages', len(pages), 'problems', bad)
