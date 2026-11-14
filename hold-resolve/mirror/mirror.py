#!/usr/bin/env python3
"""Read-only HTTP mirror of live client sites (HOLD resolve, 14 Nov 2026; Edwin OK 9:24am SGT). GET requests only.
Seeds: current source paths (client-source-shas.txt), live sitemap.xml URLs, fixed extras; then every
same-host link/asset found in fetched HTML/CSS/XML. Saves bytes exactly as served to hold-resolve/live/<site>/ plus a
manifest (path, sha256, bytes) and a misses list. Redirects and errors are recorded, never followed."""
import json, hashlib, os, re, sys, time, urllib.request, urllib.error, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SITES = json.load(open(os.path.join(HERE, 'sites.json')))
only = sys.argv[1:] or list(SITES)
UA = 'Mozilla/5.0 (compatible; PageOneLiveSnapshot/1.0; read-only)'
class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None
opener = urllib.request.build_opener(NoRedirect)
EXTRAS = ['robots.txt', 'llms.txt', 'llms-full.txt', 'sitemap.xml', 'sitemap.txt', 'review.html', 'favicon.ico', 'favicon.svg',
          'site.webmanifest', '404.html', 'apple-touch-icon.png', 'index.html']
def get(url):
    for t in range(3):
        try:
            r = opener.open(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=40)
            return r.status, r.read()
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308, 403, 404, 410): return e.code, b''
        except Exception: pass
        time.sleep(3)
    return 0, b''
def url_of(base, rel):
    if rel == 'index.html': return base + '/'
    if rel.endswith('/index.html'): return base + '/' + urllib.parse.quote(rel[:-10])
    return base + '/' + urllib.parse.quote(rel)
def rel_of(base, href, cur):
    u = urllib.parse.urljoin(url_of(base, cur), href.strip())
    p = urllib.parse.urlparse(u)
    host = lambda h: h.lower().removeprefix('www.')
    if p.scheme not in ('http', 'https') or host(p.netloc) != host(urllib.parse.urlparse(base).netloc): return None
    path = urllib.parse.unquote(p.path).lstrip('/')
    if path == '' or path.endswith('/'): path += 'index.html'
    if '..' in path.split('/'): return None
    return path
for site in only:
    base = SITES[site]; out = os.path.join(ROOT, 'live', site); os.makedirs(out, exist_ok=True)
    seeds = [l.split()[2] for l in open(os.path.join(ROOT, 'client-source-shas.txt')) if l.split()[0] == site]
    st, sm = get(base + '/sitemap.xml')
    for loc in re.findall(rb'<loc>([^<]+)</loc>', sm):
        r = rel_of(base, loc.decode().strip(), 'index.html')
        if r: seeds.append(r)
    queue = list(dict.fromkeys(seeds + EXTRAS)); seen = set(queue); manifest = []; misses = []
    while queue:
        rel = queue.pop(0); code, body = get(url_of(base, rel))
        if code != 200: misses.append((rel, code)); continue
        dst = os.path.join(out, rel); os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, 'wb').write(body)
        manifest.append((rel, hashlib.sha256(body).hexdigest(), len(body)))
        if rel.endswith(('.html', '.htm', '.css', '.xml')):
            text = body.decode('utf-8', 'replace')
            refs = re.findall(r'''(?:href|src)\s*=\s*["']([^"'#]+)''', text) + re.findall(r'''url\(\s*["']?([^"')]+)''', text)
            refs += [s.strip().split(' ')[0] for ss in re.findall(r'''srcset\s*=\s*["']([^"']+)''', text) for s in ss.split(',')]
            refs += re.findall(r'<loc>([^<]+)</loc>', text)
            for h in refs:
                r = rel_of(base, h.split('?')[0], rel)
                if r and r not in seen and len(seen) < 3000: seen.add(r); queue.append(r)
        time.sleep(0.2)
    with open(os.path.join(ROOT, 'live', site + '.manifest.tsv'), 'w') as f:
        for m in sorted(manifest): f.write('%s\t%s\t%d\n' % m)
    with open(os.path.join(ROOT, 'live', site + '.misses.tsv'), 'w') as f:
        for m in sorted(misses): f.write('%s\t%s\n' % m)
    print(site, len(manifest), 'files', len(misses), 'misses')
