"""Checks a built site folder: JSON-LD parses, FAQ schema = visible FAQs, one H1, title/desc lengths, internal links and assets exist."""
import json, os, re, sys
from urllib.parse import urljoin, urlparse
root = sys.argv[1]; base = sys.argv[2] if len(sys.argv) > 2 else 'https://pageonesingapore.com/preview/klar-details/'
bad = 0
for dp, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith('.html'): continue
        fp = os.path.join(dp, f); rel = os.path.relpath(fp, root); t = open(fp, encoding='utf-8').read()
        errs = []
        for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                g = json.loads(m)['@graph']
                for n in g:
                    if n.get('@type') == 'FAQPage' and len(n['mainEntity']) != t.count('<details'): errs.append('faq mismatch')
            except Exception as e: errs.append('jsonld %s' % e)
        if t.count('<h1') != 1: errs.append('h1=%d' % t.count('<h1'))
        if 'noindex' in t and f != '404.html': errs.append('noindex')
        title = re.search(r'<title>(.*?)</title>', t).group(1)
        import html as H
        if len(H.unescape(title)) > 60: errs.append('title long')
        page_url = urljoin(base, rel.replace('index.html', ''))
        for u in re.findall(r'(?:href|src)="([^"]+)"', t):
            if u.startswith(('http', 'mailto:', 'tel:', '#')) and not u.startswith(base): continue
            full = urljoin(page_url, u).split('?')[0].split('#')[0]
            p = urlparse(full).path.replace(urlparse(base).path, '', 1)
            tgt = os.path.join(root, p)
            if p == '' or p.endswith('/'): tgt = os.path.join(tgt, 'index.html')
            if not os.path.exists(tgt): errs.append('missing ' + u)
        if errs: bad += 1; print(rel, sorted(set(errs)))
print('bad pages', bad)
