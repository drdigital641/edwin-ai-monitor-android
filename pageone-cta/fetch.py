# GET-only: download the listed pageonesingapore.com files exactly as served, into pageone-cta/live/<path>.
import urllib.request, os, hashlib, json
UA = 'Mozilla/5.0 (compatible; PageOneCtaFetch/1.0)'
out = {}
for p in [l.strip() for l in open('pageone-cta/pages.txt') if l.strip()]:
    url = 'https://pageonesingapore.com/' + (p[:-10] if p.endswith('index.html') else p)
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'}), timeout=30)
        b = r.read(); st = r.status; fu = r.geturl()
    except Exception as e:
        out[p] = {'error': str(e)[:200]}; continue
    dst = 'pageone-cta/live/' + p
    os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'wb').write(b)
    out[p] = {'status': st, 'final': fu, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
json.dump(out, open('pageone-cta/live-manifest.json', 'w'), indent=1)
print(sum(1 for v in out.values() if 'sha256' in v), 'fetched,', sum(1 for v in out.values() if 'error' in v), 'errors')
