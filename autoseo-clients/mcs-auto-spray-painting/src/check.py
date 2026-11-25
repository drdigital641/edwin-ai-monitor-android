#!/usr/bin/env python3
"""Pre-upload gate for the MCS Auto Spray Painting preview. Exit 1 on any problem. Run after build.py, before any Bridge upload.
Fails on: lorem / TODO / placeholder text, any trace of the other agency brand, aggregateRating or rating schema, warranty or
express-claim figures, prices, a company / SSM number, invented social accounts, a Singapore branch, the neighbours' names, review
quotes (blockquote), the rendered Supra, official brand logos used as images, em dashes, a hardcoded robots meta (noindex is
host-based on the preview), H1 count != 1, missing tracker, wrong footer credit, a CTA without data-cta, wrong WhatsApp / tel
links, bad JSON-LD, missing hreflang or switcher, missing media files, and pages without their /ms/ and /zh/ twins."""
import json, os, re, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, '..', 'dist')
sys.path.insert(0, HERE)
import build  # media table, server-only files
# Words are split so this file never trips a repo-wide grep.
# TikTok: only MCS's own profile link is allowed (Edwin, 25 Nov 2026: footer + contact list, data-cta tiktok_footer / tiktok_contact_list).
BANNED = [r'lorem', r'\bTODO\b', r'\bTBD\b', r'placeholder', r'\bXXX\b', 'pa' + r'ge[\s-]*o' + 'ne', 'pageo' + 'nesingapore',
          r'aggregate' + 'Rating', r'ratingValue', r'reviewCount', r'bestRating', '[★☆⭐]',
          r'warrant', r'jaminan', r'保修', r'保固', r'\b5 years?\b', r'5 tahun', r'5年', r'2[\s-]?hours?', r'2 jam', r'2小时', r'express claim',
          r'\bRM\s?\d', r'\bfrom RM\b', r'S\$\d', r'\bSSM\b', r'\d{6,}-[A-Z]\b', r'Sdn\.? Bhd', r'company no',
          r'instagram', r'tiktok(?!\.com/@mcsqianglong8792|_footer|_contact_list|</span>)', r'\bwaze\b', r'Singapore branch', r'cawangan Singapura', r'新加坡分行', r'新加坡分店',
          'Overseas ' + 'Tyre', 'HX ' + 'Auto', r'Supra', r'<blockquote', r'official (3M|Nippon|Glasurit|Aikka|HyperTint|HyperFilm)',
          r'authori[sz]ed dealer', r'official dealer', r'81200', r'Skudai', r'Glasurit', r'\bPPG\b', r'Standox', r'Spies\s*Hecker', r'RM\s?8,?500', r'RM\s?3,?000', r'\bhiring\b', r'jawatan kosong', r'招聘', r'Friday[^.<"]{0,30}7:00 ?pm', r'"Friday"[^}]*"19:00"', r'grayscale\(', r'mix-blend-mode']
LOGO_FILES = re.compile(r'(3m|nippon|glasurit|aikka|hypertint|hyperfilm)[^"/]*\.(png|webp|svg|jpg)', re.I)
BASE = build.BASE
WA = 'https://wa.me/60165562998?text='
bad = 0


def fail(f, m):
    global bad
    bad += 1
    print(f'FAIL {os.path.relpath(f, DIST)}: {m}')


files = [os.path.join(dp, f) for dp, _, fs in os.walk(DIST) for f in fs if f.endswith(('.html', '.txt', '.xml', '.js', '.css'))]
pages = set()
for f in files:
    t = open(f, encoding='utf8').read()
    for b in BANNED:
        m = re.search(b, t, re.I)
        if m and not (f.endswith(('.css', '.js')) and b in ('placeholder', r'2[\s-]?hours?', r'tiktok(?!\.com/@mcsqianglong8792|_footer|_contact_list|</span>)', r'instagram', r'\bwaze\b')):
            fail(f, f'banned "{m.group(0)}"')
    if '—' in t:
        fail(f, 'em dash')
    if not f.endswith('.html'):
        continue
    pages.add(os.path.relpath(os.path.dirname(f), DIST).replace('\\', '/').strip('.') + '/' if os.path.dirname(f) != DIST else '')
    if re.search(r'<meta name="robots"', t):
        fail(f, 'robots meta found (preview noindex is host-based; nothing to strip at go-live)')
    if len(re.findall(r'<h1\b', t)) != 1:
        fail(f, 'H1 count != 1')
    if 'p1-cta.js' not in t:
        fail(f, 'no tracker')
    if t.count('Website by AutoSEO.my') != 1 or '<a href="https://autoseo.my/">Website by AutoSEO.my</a>' not in t:
        fail(f, 'footer credit')
    if len(re.findall(r'hreflang="(en|ms|zh-Hans|x-default)" href=', t)) != 4:
        fail(f, 'hreflang block')
    if t.count('<nav class="lang"') != 2:
        fail(f, 'language switcher (header + menu) missing')
    for k in ('og:title', 'og:description', 'og:image', 'og:url'):
        if f'property="{k}"' not in t:
            fail(f, 'missing ' + k)
    if 'Pusat Kecantikan Kereta' not in t:
        fail(f, 'signboard line missing')
    for a in re.findall(r'<a\b[^>]*>', t):
        h = re.search(r'href="([^"]*)"', a)
        h = h.group(1) if h else ''
        if re.match(r'(https://wa\.me|tel:|mailto:|https://www\.google\.com/maps|https://maps\.google|https://www\.facebook\.com|https://www\.youtube\.com|https://www\.tiktok\.com)', h):
            if 'data-cta=' not in a or 'data-ref=' not in a:
                fail(f, 'CTA without data-cta/data-ref: ' + a[:90])
        if 'wa.me' in h and not h.startswith(WA):
            fail(f, 'wrong WhatsApp link ' + h[:60])
        if h.startswith('tel:') and h != 'tel:+60165562998':
            fail(f, 'wrong tel link')
        if h.startswith('mailto:') and h != 'mailto:mcs01092020@gmail.com':
            fail(f, 'wrong email')
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        try:
            json.loads(j)
        except Exception as e:
            fail(f, f'bad JSON-LD {e}')
    for src in re.findall(r'(?:src|srcset|href|poster)="' + re.escape(BASE) + r'((?:media|assets)/[^"?]+)', t):
        if LOGO_FILES.search(src):
            fail(f, 'brand logo used as an image: ' + src)
        if not os.path.exists(os.path.join(DIST, src)) and src not in build.SERVER_MEDIA:
            fail(f, 'missing file ' + src)
    for ph in re.findall(r'class="hero-ph"', t):
        pass
for p in [p for p in pages if not p.startswith(('ms/', 'zh/'))]:
    for pre in ('ms/', 'zh/'):
        if pre + p not in pages:
            fail(DIST, f'missing {pre} twin of /{p}')
sm = open(os.path.join(DIST, 'sitemap.xml'), encoding='utf8').read()
if sm.count('<loc>') != len(pages) or sm.count('hreflang="x-default"') != len(pages):
    fail(os.path.join(DIST, 'sitemap.xml'), f'sitemap has {sm.count("<loc>")} urls for {len(pages)} pages')

tmp = tempfile.mkdtemp()
shutil.copytree(DIST, os.path.join(tmp, 'preview', 'mcs-auto-spray-painting'))
r = subprocess.run([sys.executable, '/mnt/project-files/tracking/cta_check.py', '--dir', tmp], capture_output=True, text=True)
shutil.rmtree(tmp)
print(r.stdout.strip()[-500:])
if r.returncode:
    bad += 1
print(f'check: {len(files)} files, {len(pages)} pages, {bad} problem(s)')
sys.exit(1 if bad else 0)
