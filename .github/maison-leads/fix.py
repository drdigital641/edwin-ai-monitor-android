# GET-only crawl of maisoninteriordesign.sg (17 Nov 2026, thread "Fix Maison WhatsApp lead tracking").
# Writes maison-leads/sync/ = live pages with ONLY the /p1-cta.js?v= and /mid.js?v= cache-bust values changed, the new
# p1-cta.js (v4.2), mid.js with the old #cform -> WhatsApp handler removed (the tracker's enquiry form replaces it), and a
# new privacy/index.html built from the live contact page shell. maison-leads/sync.base.json = {site path: live sha256}.
import json, re, hashlib, os, shutil, urllib.request, urllib.parse, concurrent.futures as cf, time
O = 'https://maisoninteriordesign.sg'; BASE = 'preview/maison-interior-design'; OUT = 'maison-leads/sync'
UA = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36 PageOneCrawl'
def get(u):
    for i in range(3):
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': UA, 'Cache-Control': 'no-cache'}), timeout=30)
            return r.status, r.read(), r.geturl(), r.headers.get('content-type', '')
        except urllib.error.HTTPError as e:
            return e.code, b'', u, ''
        except Exception:
            time.sleep(2)
    return 0, b'', u, ''
sha = lambda b: hashlib.sha256(b).hexdigest()
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
rep = {'base': {}, 'pages': [], 'no_tag': [], 'skipped': [], 'problems': []}
# 1. JS files
P1 = open('maison-leads/js/p1-cta.js', 'rb').read()
st, live_p1, _, _ = get(O + '/p1-cta.js?nocache=' + str(time.time()))
rep['p1_live_sha'] = sha(live_p1)
if not rep['p1_live_sha'].startswith('999757bb'): rep['problems'].append('p1-cta.js live is not 999757bb')
open(f'{OUT}/p1-cta.js', 'wb').write(P1); rep['base'][f'{BASE}/p1-cta.js'] = sha(live_p1)
st, mid, _, _ = get(O + '/mid.js?nocache=' + str(time.time()))
rep['mid_live_sha'] = sha(mid)
if not rep['mid_live_sha'].startswith('5461159d'): rep['problems'].append('mid.js live is not 5461159d')
m = re.search(rb"/\* contact form -> WhatsApp with details filled in \*/\n[\s\S]*?window\.open\('https://wa\.me/6593391185\?text='\+encodeURIComponent\(t\),'_blank','noopener'\)\}\);\n", mid)
if not m: rep['problems'].append('cform block not found in mid.js'); newmid = mid
else: newmid = mid.replace(m.group(0), b"/* contact form: replaced 17 Nov 2026 by the enquiry form in /p1-cta.js (saved to the Controller) */\n", 1)
open(f'{OUT}/mid.js', 'wb').write(newmid); rep['base'][f'{BASE}/mid.js'] = sha(mid)
V1, V2 = sha(P1)[:8], sha(newmid)[:8]; rep['p1_v'], rep['mid_v'] = V1, V2
# 2. crawl pages
seen, q = set(), []
def add(u):
    try:
        x = urllib.parse.urlsplit(urllib.parse.urljoin(O + '/', u))
        if (x.hostname or '').lower().removeprefix('www.') != 'maisoninteriordesign.sg': return
        p = x.path or '/'
        if re.search(r'\.(jpe?g|png|webp|gif|svg|pdf|mp4|css|js|xml|txt|ico|zip|json|woff2?)$', p, re.I): return
        if p in seen or len(seen) > 3000: return
        seen.add(p); q.append(p)
    except Exception: pass
for p in ['/', '/404.html', '/review.html', '/logos/']: add(p)
for l in re.findall(r'<loc>\s*([^<\s]+)\s*</loc>', get(O + '/sitemap.xml')[1].decode('utf8', 'ignore')): add(l)
pages = []
def one(p):
    st, b, fu, ct = get(O + p)
    if st != 200 or 'html' not in ct: return {'p': p, 'skip': f'status {st} {ct}'}
    for mm in re.finditer(rb'<a\b[^>]*href=["\']([^"\'#][^"\']*)["\']', b, re.I): add(mm.group(1).decode('utf8', 'ignore').replace('&amp;', '&'))
    if urllib.parse.urlsplit(fu).path != p: return {'p': p, 'skip': 'redirect ' + fu}
    return {'p': p, 'b': b}
done = 0
with cf.ThreadPoolExecutor(8) as ex:
    while done < len(q):
        batch = q[done:]; done = len(q)
        for r in ex.map(one, batch): pages.append(r)
for r in sorted(pages, key=lambda r: r['p']):
    if 'b' not in r: rep['skipped'].append(f"{r['p']}: {r['skip']}"); continue
    b = r['b']; p = r['p']
    f = (p.lstrip('/') + 'index.html') if p.endswith('/') else p.lstrip('/')
    nb = re.sub(rb'(/p1-cta\.js\?v=)[0-9a-f]{6,64}', b'\\g<1>' + V1.encode(), b)
    nb = re.sub(rb'(/mid\.js\?v=)[0-9a-f]{6,64}', b'\\g<1>' + V2.encode(), nb)
    if b'/p1-cta.js' not in b: rep['no_tag'].append(p)
    if nb == b: continue
    if not re.search(r'\.html?$', f): rep['problems'].append('extensionless ' + p); continue
    os.makedirs(os.path.dirname(f'{OUT}/{f}') or OUT, exist_ok=True); open(f'{OUT}/{f}', 'wb').write(nb)
    rep['base'][f'{BASE}/{f}'] = sha(b); rep['pages'].append(p)
# 3. privacy page from the live contact page shell
st, c, _, _ = get(O + '/contact/')
c = c.decode('utf-8'); i, j = c.find('<main id="main">'), c.find('</main>')
if i < 0 or j < 0: rep['problems'].append('contact shell not found')
else:
    head, foot = c[:i], c[j:]
    head = re.sub(r'<script type="application/ld\+json">[\s\S]*?</script>', '', head)
    head = re.sub(r'<title>[\s\S]*?</title>', '<title>Privacy Policy | Maison Interior Design</title>', head, 1)
    for k, v in [('description', 'How Maison Interior Design uses the name and mobile number you send through the enquiry form on this website.')]:
        head = re.sub(r'(<meta name="%s" content=")[^"]*(")' % k, lambda mm: mm.group(1) + v + mm.group(2), head)
        head = re.sub(r'(<meta (?:property|name)="(?:og|twitter):%s" content=")[^"]*(")' % k, lambda mm: mm.group(1) + v + mm.group(2), head)
    head = re.sub(r'(<meta (?:property|name)="(?:og|twitter):title" content=")[^"]*(")', lambda mm: mm.group(1) + 'Privacy Policy | Maison Interior Design' + mm.group(2), head)
    head = head.replace('https://maisoninteriordesign.sg/contact/', 'https://maisoninteriordesign.sg/privacy/')
    main = '''<main id="main">
<section class="phead"><div class="wrap narrow"><h1 class="display">Privacy policy</h1>
<p class="lead">How Maison Interior Design handles the details you send us through this website.</p></div></section>
<section class="sec tight"><div class="wrap narrow">
<h2>What we collect</h2>
<p>When you send the enquiry form we receive your name, your mobile number, the project or interest you typed, the page you sent it from and the time. When you tap a WhatsApp or call button we count the tap (page, time and device type) without your name or number.</p>
<h2>Why we use it</h2>
<p>To reply to your enquiry about interior design and renovation, usually by WhatsApp, and to see which pages help visitors find what they need.</p>
<h2>Who sees it</h2>
<p>Maison Interior Design and the team that runs this website for us, only to handle your enquiry. We do not sell or rent your details.</p>
<h2>How long we keep it</h2>
<p>Only as long as we need it to answer your enquiry and follow up on your project.</p>
<h2>Your choices</h2>
<p>You can ask to see, correct or delete your details, or tell us to stop contacting you, at any time: WhatsApp <a href="https://wa.me/6593391185?text=Hi%20Maison%2C%20I%20have%20a%20question%20about%20my%20personal%20data." data-cta="whatsapp" target="_blank" rel="noopener">+65 9339 1185</a> or email <a href="mailto:maisoninteriordesignsg@gmail.com">maisoninteriordesignsg@gmail.com</a>.</p>
<p><small>Last updated 17 November 2026.</small></p>
</div></section>
'''
    page = (head + main + foot).encode('utf-8')
    page = re.sub(rb'(/p1-cta\.js\?v=)[0-9a-f]{6,64}', b'\\g<1>' + V1.encode(), page)
    page = re.sub(rb'(/mid\.js\?v=)[0-9a-f]{6,64}', b'\\g<1>' + V2.encode(), page)
    os.makedirs(f'{OUT}/privacy', exist_ok=True); open(f'{OUT}/privacy/index.html', 'wb').write(page)
    st2 = get(O + '/privacy/')[0]; rep['privacy_live_status'] = st2
json.dump(rep['base'], open('maison-leads/sync.base.json', 'w'), indent=0, sort_keys=True)
rep.pop('base'); rep['n_pages'] = len(rep['pages']); rep['n_seen'] = len(seen)
json.dump(rep, open('maison-leads/REPORT.json', 'w'), indent=1)
print(json.dumps({k: v for k, v in rep.items() if k != 'pages'}, indent=1))
