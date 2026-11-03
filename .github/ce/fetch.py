"""ContiExpert research fetch (runs on GitHub runner): WordPress media library, key pages, social images -> contact sheets."""
import json, os, re, sys, io, urllib.request, hashlib
from PIL import Image, ImageDraw
OUT = 'pageone-site/clients/contiexpert/src/research-fetch'
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
os.makedirs(OUT + '/wp', exist_ok=True); os.makedirs(OUT + '/social', exist_ok=True); os.makedirs(OUT + '/pages', exist_ok=True)
def get(u, t=40):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read()
log = []
# pages
for name, u in [('contiexpert-home', 'https://contiexpert.sg/'), ('contiexpert-services', 'https://contiexpert.sg/services/'),
                ('voltauto-home', 'https://voltauto.sg/'), ('voltauto-www', 'https://www.voltauto.sg/'), ('voltautocare', 'https://voltautocare.sg/')]:
    try:
        b = get(u); open('%s/pages/%s.html' % (OUT, name), 'wb').write(b); log.append('page ok %s %d' % (u, len(b)))
    except Exception as e: log.append('page fail %s %s' % (u, e))
# wp media
media = []
for p in range(1, 8):
    try:
        b = get('https://contiexpert.sg/wp-json/wp/v2/media?per_page=100&page=%d' % p); d = json.loads(b)
        if not d: break
        media += d
    except Exception as e: log.append('media page %d stop %s' % (p, e)); break
man = []
seen = set()
for m in media:
    if m.get('media_type') != 'image': continue
    u = m.get('source_url'); 
    if not u or u in seen: continue
    seen.add(u)
    slug = re.sub(r'[^a-z0-9-]+', '-', os.path.splitext(os.path.basename(u))[0].lower())[:70]
    try:
        im = Image.open(io.BytesIO(get(u))); im.load()
        w, h = im.size
        if im.mode not in ('RGB', 'RGBA'): im = im.convert('RGBA')
        if w > 1600: im = im.resize((1600, int(h * 1600 / w)), Image.LANCZOS)
        fn = '%s/wp/%03d-%s.webp' % (OUT, len(man) + 1, slug)
        im.save(fn, 'WEBP', quality=80)
        man.append({'n': len(man) + 1, 'file': os.path.basename(fn), 'src': u, 'w': w, 'h': h, 'alt': m.get('alt_text', ''), 'title': (m.get('title') or {}).get('rendered', ''), 'date': m.get('date')})
    except Exception as e: log.append('img fail %s %s' % (u, e))
json.dump(man, open(OUT + '/wp-manifest.json', 'w'), indent=1)
# social
soc = [l.strip() for l in open('.github/ce/social-urls.txt') if l.strip() and not l.startswith('#')]
smf = []
for i, line in enumerate(soc):
    name, u = line.split(' ', 1)
    try:
        im = Image.open(io.BytesIO(get(u))); im.load(); im = im.convert('RGB')
        fn = '%s/social/%s.webp' % (OUT, name); im.save(fn, 'WEBP', quality=85); smf.append({'name': name, 'w': im.size[0], 'h': im.size[1]})
    except Exception as e: log.append('social fail %s %s' % (name, e))
json.dump(smf, open(OUT + '/social-manifest.json', 'w'), indent=1)
# contact sheets: 30 per sheet, numbered
def sheet(files, label, outname):
    T = 260; cols = 6
    for s in range(0, len(files), 30):
        chunk = files[s:s + 30]; rows = (len(chunk) + cols - 1) // cols
        sh = Image.new('RGB', (cols * T, rows * (T + 22)), 'white'); d = ImageDraw.Draw(sh)
        for k, (lab, f) in enumerate(chunk):
            try:
                im = Image.open(f).convert('RGB'); im.thumbnail((T - 6, T - 6))
                x, y = (k % cols) * T, (k // cols) * (T + 22)
                sh.paste(im, (x + 3 + (T - 6 - im.size[0]) // 2, y + 3 + (T - 6 - im.size[1]) // 2))
                d.text((x + 4, y + T + 4), lab[:40], fill='black')
            except Exception: pass
        sh.save('%s/%s-%d.jpg' % (OUT, outname, s // 30 + 1), quality=70)
sheet([('#%d %dx%d' % (m['n'], m['w'], m['h']), '%s/wp/%s' % (OUT, m['file'])) for m in man], 'wp', 'sheet-wp')
sheet([(m['name'], '%s/social/%s.webp' % (OUT, m['name'])) for m in smf], 'social', 'sheet-social')
open(OUT + '/log.txt', 'w').write('\n'.join(log) + '\nwp images: %d, social: %d\n' % (len(man), len(smf)))
print('\n'.join(log)); print(len(man), len(smf))
