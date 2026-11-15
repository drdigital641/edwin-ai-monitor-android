# GET-only: crawl each site, find pages with WhatsApp/call links but no CTA tracker, write a copy with the
# p1-cta.js tag added before </body> to cta-fix/out/<slug>/<file path>, plus a manifest with the live sha256.
import json, re, hashlib, os, sys, urllib.request, urllib.parse, concurrent.futures as cf
UA = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36'
TRK = re.compile(rb'functions/track|p1WaTap|p1CtaTap|whatsapp_click')
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA}), timeout=25)
        return r.status, r.read(), r.geturl(), r.headers.get('content-type', '')
    except Exception as e:
        return 0, b'', u, ''
jsc = {}
def js(u):
    if u not in jsc: jsc[u] = get(u)[1]
    return jsc[u]
H = lambda h: h.lower().removeprefix('www.')
sites = json.load(open('.github/cta-fix/sites.json'))
only = sys.argv[1].split(',') if len(sys.argv) > 1 else None
report = []
for s in sites:
    if only and s['slug'] not in only: continue
    o = s['origin']; host = H(urllib.parse.urlsplit(o).hostname); pre = s['prefix']; ex = s.get('exclude', [])
    jsbody = open(f"cta-fix/js/{s['slug']}/p1-cta.js", 'rb').read() if s['src'] else b''
    tag = (f'<script src="{s["src"]}?v={hashlib.sha256(jsbody).hexdigest()[:8]}" defer></script>').encode() if s['src'] else None
    seen, q, pages = set(), [], []
    def add(u):
        try:
            x = urllib.parse.urlsplit(urllib.parse.urljoin(o + '/', u))
            if x.scheme not in ('http', 'https') or H(x.hostname or '') != host: return
            p = x.path or '/'
            if not p.startswith(pre) or any(p.startswith(e) for e in ex): return
            if re.search(r'\.(jpe?g|png|webp|gif|svg|pdf|mp4|css|js|xml|txt|ico|zip|json|woff2?)$', p, re.I): return
            if p in seen or len(seen) > 4000: return
            seen.add(p); q.append(p)
        except Exception: pass
    add(pre)
    sm = get(o + pre + 'sitemap.xml')[1].decode('utf8', 'ignore')
    for l in re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', sm):
        if re.search(r'sitemap.*\.xml$', l):
            for l2 in re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', get(l)[1].decode('utf8', 'ignore')): add(l2)
        else: add(l)
    def one(p):
        st, b, fu, ct = get(o + p)
        if st != 200 or 'html' not in ct: return None
        for m in re.finditer(rb'<a\b[^>]*href=["\']([^"\'#][^"\']*)["\']', b, re.I): add(m.group(1).decode('utf8', 'ignore').replace('&amp;', '&'))
        if H(urllib.parse.urlsplit(fu).hostname or '') != host or urllib.parse.urlsplit(fu).path != p: return {'p': p, 'skip': 'redirect ' + fu}
        wa = len(re.findall(rb'<a\b[^>]*href=["\'](https?://(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)|whatsapp:)', b, re.I))
        tel = len(re.findall(rb'<a\b[^>]*href=["\']tel:', b, re.I))
        if not wa and not tel: return {'p': p, 'skip': 'no cta'}
        inl = b''.join(re.findall(rb'<script\b(?![^>]*src=)[^>]*>([\s\S]*?)</script>', b, re.I))
        srcs = [urllib.parse.urljoin(fu, m.decode()) for m in re.findall(rb'<script\b[^>]*src=["\']([^"\']+)["\']', b, re.I)]
        srcs = [x for x in srcs if H(urllib.parse.urlsplit(x).hostname or '') == host]
        has = bool(TRK.search(inl)) or any(TRK.search(js(x)) for x in srcs) or b'p1-cta.js' in b
        return {'p': p, 'wa': wa, 'tel': tel, 'has': has, 'b': b}
    done = 0
    with cf.ThreadPoolExecutor(8) as ex_:
        while done < len(q):
            batch = q[done:]; done = len(q)
            for r in ex_.map(one, batch):
                if r: pages.append(r)
    if s.get('reuse_tag'):
        home = get(o + '/')[1]
        m = re.search(rb'<script\b[^>]*' + re.escape(s['reuse_tag'].encode()) + rb'[^>]*>\s*</script>', home)
        tag = m.group(0) if m else None
    out = []
    for r in pages:
        if 'b' not in r or r['has']: continue
        b = r['b']; i = b.lower().rfind(b'</body>')
        p = r['p'][len(pre) - 1:] if pre != '/' else r['p']
        f = (p.lstrip('/') + 'index.html') if p.endswith('/') else p.lstrip('/')
        ent = {'url': o + r['p'], 'file': f, 'live_sha256': hashlib.sha256(b).hexdigest(), 'wa': r['wa'], 'tel': r['tel']}
        if i < 0 or not tag: ent['problem'] = 'no </body>' if i < 0 else 'no tag'
        else:
            nb = b[:i] + tag + b'\n' + b[i:]
            dst = f"cta-fix/out/{s['slug']}/{f}"
            if not re.search(r'\.html?$', f): ent['problem'] = 'extensionless url, map by hand'; dst = f"cta-fix/odd/{s['slug']}/{f}.html"
            os.makedirs(os.path.dirname(dst), exist_ok=True); open(dst, 'wb').write(nb)
            ent['new_sha256'] = hashlib.sha256(nb).hexdigest()
        out.append(ent)
    os.makedirs('cta-fix/manifest', exist_ok=True)
    json.dump({'site': s, 'tag': tag.decode() if tag else None, 'pages_seen': len(pages), 'with_cta': sum(1 for r in pages if 'b' in r),
               'already_tracked': sum(1 for r in pages if r.get('has')), 'to_fix': out}, open(f"cta-fix/manifest/{s['slug']}.json", 'w'), indent=1)
    line = f"{s['slug']}: seen={len(pages)} cta={sum(1 for r in pages if 'b' in r)} tracked={sum(1 for r in pages if r.get('has'))} fix={len(out)} problems={sum(1 for e in out if 'problem' in e)}"
    print(line); report.append(line)
open('cta-fix/REPORT.txt', 'w').write('\n'.join(report) + '\n')
