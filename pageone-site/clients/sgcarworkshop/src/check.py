#!/usr/bin/env python3
"""Link checker + JSON-LD parse + banned words.  python3 check.py [sitedir]"""
import json, os, re, sys
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin, unquote
root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'site'))
BAN = re.compile(r"\b(" + '|'.join(__import__('json').load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')))['wording']['ban']) + r")\b", re.I)
bad = 0
from html import unescape as html_unescape

# Edwin 3 Nov 2026 (PERMANENT): listings use the exact Google Business Profile name, so a workshop's own name
# (e.g. "Best Auto Service @ Toh Guan") is masked before the wording checks; our own copy is still checked.
class _NameMasked:
    def __init__(s, rx):
        import glob as _g, html as _h
        s.rx = rx; s.names = []
        for _f in _g.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'workshops', '*.json')):
            _r = json.load(open(_f)); _n = _r.get('name') or ''
            if rx.search(_n): s.names += [_n, _h.escape(_n), _h.escape(_n, quote=False), __import__('urllib.parse').parse.quote(_n), _r.get('slug') or os.path.basename(_f)[:-5]]
        s.names.sort(key=len, reverse=True)
    def _m(s, t):
        for _n in s.names: t = t.replace(_n, 'Workshop')
        return t
    def finditer(s, t): return s.rx.finditer(s._m(t))
    def findall(s, t): return s.rx.findall(s._m(t))
    def search(s, t): return s.rx.search(s._m(t))
HOTLINK = set()
SET_IMG = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')))['image_hosts_pending']
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
_BANM = _NameMasked(BAN)
files = [os.path.join(d, f) for d, _, fs in os.walk(root) for f in fs if f.endswith('.html')]
for f in sorted(files):
    rel = os.path.relpath(f, root)
    p = P(); src = open(f, encoding='utf-8').read(); p.feed(src)
    _mf = json.load(open(os.path.join(root, '..', 'build-manifest.json')))
    _raw = open(f, encoding='utf-8').read()
    _okni = rel == '404.html' or 'http-equiv="refresh"' in _raw or 'This folder is not a page' in _raw or (rel[:-10] if rel.endswith('index.html') else rel) in _mf['noindex']
    if p.noindex and not _okni: print('NOINDEX in', rel); bad += 1
    for j in p.ld:
        try: json.loads(j)
        except Exception as e: print('BAD JSON-LD', rel, e); bad += 1
    txt = ' '.join(p.text)
    _bt = txt + ' '.join(p.ld)
    if re.fullmatch(r'areas/[a-z-]+/index\.html', rel) and '<title>Best Car Workshops in ' in src:
        # Edwin 3 Nov 2026: estate titles may say "Best ... Top Rated" only when the page ranks workshops by the combined score (8+ comparable workshops) and says so
        if 'Ranked by a combined score of Google rating and number of ratings' not in src: print('BEST title without a ranking basis', rel); bad += 1
        _bt = _bt.replace('Best Car Workshops in', 'Car Workshops in', 1)
    for m in _BANM.finditer(_bt): print("BANNED", rel, m.group(0)); bad += 1
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
ENT_TIER = {_e['slug']: _e['tier'] for _e in ENTRIES}
FEAT = ['photos', 'services_detail', 'faqs', 'gallery']          # numeric counts: Basic < Verified (Wei) <= Premium
MINIMUM = {'photos': 3, 'services_detail': 3, 'faqs': 3, 'gallery': 1}
CONV = ['contact', 'address', 'map', 'hours', 'rating']          # Basic must have all; hours/rating shown for information
def audit(a):
    jobs = len(re.findall(r'<figure class="rv job">', a))
    illus = len(re.findall(r'<figure class="rv illus">', a))
    return {
        'photos': jobs + len(re.findall(r'class="hero-ph(?: gph)?(?: has-img)?"[^>]*>(?:<img|<div class="tile ini")', a)),
        'services_detail': len(re.findall(r'<li class="svc ', a)),
        'faqs': len(re.findall(r'<details class="faq">', a)),
        'gallery': jobs + illus,
        'contact': 'google.com/maps/search/?api=1&amp;query=' in a and 'query_place_id=' in a or bool(re.search(r'href="tel:\+\d+"[^>]*data-cta="call_dir_', a)) or bool(re.search(r'href="https://wa\.me/\d+\?text=[^"]*"[^>]*data-cta="whatsapp_dir_', a)),
        'address': 'data-addr' in a,
        'map': 'data-map' in a,
        'hours': 'class="hours"' in a or 'data-live="hours"' in a,
        'rating': 'class="reviews-line"' in a or 'class="rtg"' in a,
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
        for c in CONV[:3]:
            if not r[c]: notes.append('Basic missing ' + c)
        for c in FEAT:
            if wei and not r[c] < wei[c]: notes.append('Basic %s %s not < Verified %s' % (c, r[c], wei[c]))
        if not r['both_buttons']: notes.append('Basic needs WhatsApp + Call')
    elif e['tier'] in ('premium_leadgen', 'none') and wei:
        for c in (FEAT if e['tier'] != 'none' else []):   # founder-owned: no invented photos or FAQs; contact, address, map and buttons still required   # Premium must reach Verified's level (capped at the thresholds below: 3 photos, 3 services, 3 FAQs, 1 gallery item)
            need = min(wei[c], MINIMUM[c])
            have = r[c]
            if c == 'photos' and e.get('category') == 'car-parts': have = max(have, r['gallery'])   # parts shop: its catalogue part images count as pictures when no shop photos exist
            if have < need: notes.append('Premium %s %s < Verified minimum %s' % (c, r[c], need))
        for c in (('contact', 'address', 'map', 'rating', 'both_buttons') if e['tier'] != 'none' else ('contact', 'address', 'map', 'both_buttons')):
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
import urllib.parse as _up
import data as _data
ENDORSE = re.compile(r'\b(partner\w*|verified|recommended|recommends|trusted|confirmed|endorse\w*|official\w*|approved|authori[sz]ed|certified|best|top|leading|number one)\b', re.I)
ENDORSE = _NameMasked(ENDORSE)
CATPHRASE = {'general-servicing-repair': 'servicing or repair', 'spray-painting-bodywork': 'spray painting or bodywork', 'gearbox-repair': 'gearbox repair',
             'abs-ecu-module-repair': 'ABS or ECU repair', 'car-battery': 'a car battery', 'car-detailing-coating': 'detailing or coating', 'car-aircon-repair': 'car aircon repair',
             'car-wrap-ppf': 'a wrap or PPF', 'car-parts': 'car parts'}
CANON = 'https://sgcarworkshop.sg/'
def want_wa(e):
    return 'https://wa.me/%s?text=%s' % (e['whatsapp'], _up.quote('Hi, I found you on SG Car Workshop (sgcarworkshop.sg). I would like to ask about %s for my car' % CATPHRASE[e['category']]))
OSM = 'openstreetmap.org'
PILOT_SLUGS = set(f[:-5] for f in os.listdir(os.path.join(root, '..', 'data', 'pilot'))) if os.path.isdir(os.path.join(root, '..', 'data', 'pilot')) else set()
for e in ENTRIES:
    if e['slug'] in PILOT_SLUGS:
        # Basic PILOT (Edwin 2 Nov 2026): single fixed-content page, no photo, hours say "see Google Maps", no ratings/reviews/second phones.
        pg = open(os.path.join(root, 'workshops', e['slug'], 'index.html'), encoding='utf-8').read()
        body = re.sub(r'<(script|style).*?</\1>', '', pg, flags=re.S)
        _gs = re.findall(r'<section class="pl-sec pl-google".*?</section>', body, re.S)   # reviews, comparison and hours blocks
        gsec = re.search(r'.', '') if False else (_gs[0] if _gs else None)
        gj = os.path.join(root, '..', 'data', 'google_cache', e['slug'] + '.json')
        if gsec:
            body_g = ' '.join(_gs)
            for _s in _gs: body = body.replace(_s, '')
            gc = json.load(open(gj)) if os.path.exists(gj) else None
            gtxt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', body_g))
            if not gc or gc.get('source') != 'google_places' or not gc.get('fetched_at'): print('PILOT google section needs a google_places cache with fetched_at', e['slug']); bad += 1
            else:
                import datetime as _dt
                if (_dt.date.today() - _dt.date.fromisoformat(gc['fetched_at'])).days > 30: print('PILOT google cache older than 30 days', e['slug']); bad += 1
                if 'Google Maps' not in gtxt: print('PILOT google section lacks attribution', e['slug']); bad += 1
                _hero = re.search(r'<p class="rtg"><b>([0-9.]+)</b> \(([\d,]+)\+? Google rating', pg)
                if gc.get('rating') and gc.get('userRatingCount') and (not _hero or _hero.group(1) != '%.1f' % float(gc['rating']) or _hero.group(2) != format(gc['userRatingCount'], ',')): print('PILOT hero rating does not match cache', e['slug']); bad += 1
                for h in (gc.get('weekdayDescriptions') or []):
                    if h.replace('\u202f', ' ').replace('\u2009', ' ') not in gtxt: print('PILOT google hours do not match cache', e['slug']); bad += 1; break
            if re.search(r'[\u201c\u201d]|<q>|<blockquote', body_g): print('PILOT google section must not quote reviews', e['slug']); bad += 1
            if ENDORSE.search(gtxt): print('PILOT google section has endorsement wording', e['slug']); bad += 1
        # Round 2 (Edwin 3 Nov 2026): the FAQ section may state Google hours (checked below against the cache); it is audited on its own, then removed from the text checks.
        fsec = re.search(r'<section class="pl-sec" id="faqs">.*?</section>', body, re.S)
        faq_txt = ''
        if fsec:
            body = body.replace(fsec.group(0), '')
            faq_txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', fsec.group(0)))
            for _o in ENTRIES: faq_txt = faq_txt.replace(_o['name'], ' ')
            nq = fsec.group(0).count('<details')
            if not 5 <= nq <= 7: print('PILOT FAQ must have 5 to 7 questions, has', nq, e['slug']); bad += 1
            if re.search(r'\b(review|reviews|rated|stars?|rating|ratings)\b', faq_txt, re.I): print('PILOT FAQ mentions reviews/ratings', e['slug']); bad += 1
            if ENDORSE.search(faq_txt): print('PILOT FAQ has endorsement wording', e['slug']); bad += 1
            _gc = json.load(open(gj)) if os.path.exists(gj) else {}
            _hh = re.sub(r'\s+', ' ', ' '.join(_gc.get('weekdayDescriptions') or []).replace('\u202f', ' ').replace('\u2009', ' '))
            for _t in re.findall(r'\b\d{1,2}(?::\d{2})?\s?(?:AM|PM)\b', faq_txt):
                if _t not in _hh: print('PILOT FAQ states a time that is not in the Google hours', _t, e['slug']); bad += 1
        txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<p class="rtg">.*?</p>', ' ', body)))
        txt = txt.replace(e['name'], ' ')   # a workshop name such as 'Moon Star' must not trip the review/rating word check
        for _o in ENTRIES:                  # neighbours' names appear in the More-in block
            txt = txt.replace(_o['name'], ' ')
        for needle in ('see Google Maps for current hours', 'maps/dir/?api=1&amp;destination=', 'google.com/maps/embed/v1/place?key=', 'Is this your workshop?', 'data-cta="whatsapp_dir_%s"' % e['slug'], 'data-cta="call_dir_%s"' % e['slug'], 'id="faqs"', 'data-cta="maps_%s"' % e['slug']):
            if needle not in pg: print('PILOT page missing', needle, e['slug']); bad += 1
        if '<img' in body or 'class="hoursbox"' in pg or 'livephone.js' in pg: print('PILOT page must have no photo and no hours box', e['slug']); bad += 1
        for stored in ('"openingHours"', 'ratingValue', 'reviewCount', 'aggregateRating', '"review"'):
            if stored in pg: print('PILOT page has a forbidden field', stored, e['slug']); bad += 1
        if re.search(r'\b(review|reviews|rated|stars?|rating)\b', txt.replace('See photos, reviews & hours on Google Maps', '').replace('See photos, reviews &amp; hours on Google Maps', ''), re.I): print('PILOT page mentions reviews/ratings', e['slug']); bad += 1
        if re.search(r'\b(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\w*\s*[-:to]|\d{1,2}\s?(am|pm)\b', txt): print('PILOT page states opening hours', e['slug']); bad += 1
        if '<article class="story">' in pg:
            if pg.count('<article class="story">') > 2: print('PILOT page has more than 2 stories', e['slug']); bad += 1
            for su in re.findall(r'<article class="story">.*?href="([^"]+)"', pg, re.S):
                if not su.startswith('https://'): print('PILOT story must link to the original post', e['slug']); bad += 1
            fj = os.path.join(root, '..', 'data', 'facts', e['slug'] + '.json')
            fs = json.load(open(fj))['stories'] if os.path.exists(fj) else []
            import html as _h
            if sorted(_h.unescape(u) for u in re.findall(r'<article class="story">.*?href="([^"]+)"', pg, re.S)) != sorted(x['source_url'] for x in fs): print('PILOT stories must match the fact file source URLs', e['slug']); bad += 1
        wa = re.findall(r'wa\.me/(\d+)', pg)
        if not wa or set(wa) != {str(e['whatsapp'])}: print('PILOT WhatsApp must be the stored mobile only', e['slug']); bad += 1
        tels = set(re.findall(r'tel:(\+\d+)', pg))
        if tels != {'+' + str(e['whatsapp'])}: print('PILOT Call must be the stored mobile only', e['slug'], tels); bad += 1
        for w in ENDORSE.findall(txt): print('PILOT page has endorsement wording', w, e['slug']); bad += 1
        if want_wa(e) not in pg: print('PILOT WhatsApp prefill wrong', e['slug']); bad += 1
        continue
    # RULE 2: every live record has a stored SG mobile with WhatsApp; RULE 4 prefill
    if not re.match(r'^65[89]\d{7}$', str(e.get('whatsapp', ''))): print('LIVE RECORD WITHOUT STORED MOBILE', e['slug']); bad += 1
    if not e.get('phone') and not e.get('whatsapp'): print('NO PHONE', e['slug']); bad += 1
    if e['tier'] == 'free':
        pg = open(os.path.join(root, 'workshops', e['slug'], 'index.html'), encoding='utf-8').read()
        ld = [json.loads(j) for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', pg, re.S)]
        biz = [x for x in ld if x.get('@type') != 'BreadcrumbList']
        if len(biz) != 1 or biz[0].get('@type') != 'AutoRepair' or set(biz[0]) - {'@context', '@type', 'name', 'url', 'address', 'geo', 'telephone', 'sameAs', 'hasMap'} or not {'name', 'address', 'geo', 'telephone', 'hasMap'} <= set(biz[0]):
            print('BASIC schema must be AutoRepair with name, address, geo, telephone, hasMap (+ sameAs only)', e['slug']); bad += 1
        for needle in ('data-cta="claim_%s"' % e['slug'], 'Is this your workshop?', 'query_place_id=%s' % e['place_id'], 'See photos, reviews &amp; hours on Google Maps',
                       'maps/dir/?api=1&amp;destination=', 'destination_place_id=%s' % e['place_id'], ('Typical services for this type' if e['services_source'] == 'google_profile' else 'From the workshop\'s own website'), 'Show opening hours',
                       '<span translate="no">Google Maps</span>', 'google.com/maps/embed/v1/place?key=', 'loading="lazy"', 'referrerpolicy="strict-origin-when-cross-origin"', 'height="300"',
                       'class="hoursbox"', 'livephone.js'):
            if needle not in pg: print('BASIC page missing', needle, e['slug']); bad += 1
        if not re.search(r'embed/v1/place\?key=[^&"]+&amp;q=%s' % re.escape(_up.quote('%s %s Singapore' % (e['name'], e['address_public']))), pg): print('BASIC embed q is not name + address + Singapore', e['slug']); bad += 1
        if OSM in pg: print('BASIC page has an OSM map and Places content', e['slug']); bad += 1
        txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style).*?</\1>', '', pg, flags=re.S)))
        for w in ENDORSE.findall(txt): print('BASIC page has endorsement wording', w, e['slug']); bad += 1
        if 'Remove my listing' not in pg or 'list-your-workshop/?w=%s#remove' % e['slug'] not in pg or 'Manage this listing' not in pg: print('BASIC page missing Manage/Remove links', e['slug']); bad += 1
        for stored in ('openingHours', 'ratingValue', 'reviewCount', 'aggregateRating', '"review"', 'maps?cid', 'cid='): 
            if stored in pg: print('BASIC page has a forbidden Google-derived field', stored, e['slug']); bad += 1
        if want_wa(e) not in pg: print('BASIC WhatsApp prefill wrong', e['slug']); bad += 1
        for banned in ('class="faq"', 'class="gal"', 'class="svc ', 'FAQPage', 'Review'):
            if banned in pg: print('BASIC page has Verified-only content', banned, e['slug']); bad += 1
        # sticky bar on profiles has WhatsApp + Call
        if not re.search(r'<div class="wabar"[^>]*>.*wa\.me/.*tel:\+65.*</div>', pg, re.S): print('BASIC sticky bar needs WhatsApp + Call', e['slug']); bad += 1

# RULE 4: EVERY business card (home carousel and grid, area, service, search results) has WhatsApp + Call; the prefill is the one template
for dp, _, fs in os.walk(root):
    for fn in fs:
        if not fn.endswith('.html') or 'workshops' + os.sep + fn in dp: continue
        rel = os.path.relpath(os.path.join(dp, fn), root)
        t = open(os.path.join(dp, fn), encoding='utf-8').read()
        for m in re.finditer(r'<article class="card([^"]*)"[^>]*>(.*?)</article>', t, re.S):
            cls, inner = m.group(1), m.group(2)
            if 'free-card' in cls or 'list' in cls.split():
                continue
            slug = re.search(r'workshops/([a-z0-9-]+)/', inner)
            if not slug: continue
            s = slug.group(1)
            if 'data-cta="whatsapp_dir_%s"' % s not in inner or 'data-cta="call_dir_%s"' % s not in inner or 'href="tel:+65' not in inner or 'wa.me/65' not in inner:
                print('CARD WITHOUT WhatsApp + Call', rel, s); bad += 1
            ent = [x for x in ENTRIES if x['slug'] == s]
            if ent and want_wa(ent[0]) not in inner: print('CARD WhatsApp prefill wrong', rel, s); bad += 1
sm = open(os.path.join(root, 'sitemap.xml')).read(); lt = open(os.path.join(root, 'llms.txt')).read()
for e in ENTRIES:
    if ('workshops/%s/' % e['slug']) not in sm or ('workshops/%s/' % e['slug']) not in lt: print('NOT in sitemap/llms.txt', e['slug']); bad += 1
# (SG Garage shares Edwin's number, so match Page One's own prefill.)
# Customers must only see the workshop's own WhatsApp: Page One's number may appear only on owner pages.
from data import PAGE_ONE_WA
for dp, _, fs in os.walk(root):
    for fn in fs:
        if not fn.endswith('.html'): continue
        rel = os.path.relpath(os.path.join(dp, fn), root)
        if rel.startswith(('list-your-workshop', 'about')): continue
        if 'wa.me/%s?text=Hi%%20Page%%20One' % PAGE_ONE_WA in open(os.path.join(dp, fn), encoding='utf-8').read():
            print('Page One WhatsApp on a customer page:', rel); bad += 1
# ---- Area structure (Edwin, 1 Nov 2026): regions -> estates -> service x estate, breadcrumbs on every workshop page, no confirmation claims.
import areas as _ar
_ar.annotate(ENTRIES)
_regions, _est, _pairs = _ar.published(ENTRIES)
_pairs = {(s, k): v for (s, k), v in _pairs.items() if k != 'general-servicing-repair' and len(v) < len(_est[s])}   # same merge rule as build.py
def _ld(path):
    return [json.loads(j) for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', open(os.path.join(root, path, 'index.html'), encoding='utf-8').read(), re.S)]
_sitemap = open(os.path.join(root, 'sitemap.xml')).read()
for k in _regions:
    if not os.path.isfile(os.path.join(root, 'areas', k, 'index.html')): print('MISSING region page', k); bad += 1
for k in _ar.ESTATES:
    exists = os.path.isfile(os.path.join(root, 'areas', k, 'index.html'))
    if k in _est and not exists: print('MISSING estate page', k); bad += 1
    if k not in _est and (exists or '/areas/%s/' % k in _sitemap): print('EMPTY estate published or in sitemap', k); bad += 1
for k, v in _est.items():
    types = {x.get('@type') for x in _ld('areas/%s' % k)}
    if not {'ItemList', 'BreadcrumbList'} <= types: print('estate schema missing', k, types); bad += 1
    h = open(os.path.join(root, 'areas', k, 'index.html'), encoding='utf-8').read()
    if h.count('<details>') < 3 or 'openstreetmap.org/export/embed' not in h: print('estate needs 3+ FAQs and a map', k); bad += 1
    if len(re.findall(r'<article class="card', h)) - h.count('card list') < len(v): print('estate card count', k); bad += 1
for (k, c), v in _pairs.items():
    if len(v) < 2 or not os.path.isfile(os.path.join(root, 'areas', k, c, 'index.html')): print('L3 page missing or under 2 workshops', k, c); bad += 1
for dp, _, fs in os.walk(os.path.join(root, 'areas')):
    parts = os.path.relpath(dp, os.path.join(root, 'areas')).split(os.sep)
    if len(parts) == 2 and 'index.html' in fs and 'http-equiv="refresh"' not in open(os.path.join(dp, 'index.html'), encoding='utf-8').read() and (parts[0], parts[1]) not in _pairs: print('L3 page that should not exist', parts); bad += 1
for e in ENTRIES:
    t = [x for x in _ld('workshops/%s' % e['slug']) if x.get('@type') == 'BreadcrumbList']
    names = [i['name'] for i in t[0]['itemListElement']] if t else []
    want = ['Home', _ar.REGION_NAMES[e['region']]] + ([_ar.TOWNS[_ar.ESTATES[e['estates'][0]]['town']]['name'], _ar.ESTATES[e['estates'][0]]['name']] if e['estates'] else []) + [e['name']]
    if names != want: print('BREADCRUMB', e['slug'], names, 'want', want); bad += 1
for dp, _, fs in os.walk(root):
    for fn in fs:
        if fn.endswith(('.html', '.txt')) and re.search(r'confirmed (with|by) (each|the) business|business confirms|checked with the business', open(os.path.join(dp, fn), encoding='utf-8').read(), re.I):
            print('CONFIRMATION CLAIM in', os.path.relpath(os.path.join(dp, fn), root)); bad += 1
if os.path.isdir(os.path.join(root, 'regions')) is False: print('old /regions/ redirect pages missing'); bad += 1

# Compliance: footer + About + Featured (paid) labels + legal pages + canonical domain
for rel in ('index.html', 'about/index.html', 'list-your-workshop/index.html', 'terms/index.html', 'privacy/index.html'):
    t = open(os.path.join(root, rel), encoding='utf-8').read()
    if 'list-your-workshop/#remove' not in t and rel != 'list-your-workshop/index.html': print('footer Remove my listing link missing', rel); bad += 1
    if 'terms/' not in t or 'privacy/' not in t: print('footer Terms/Privacy links missing', rel); bad += 1
    if CANON not in t: print('canonical is not sgcarworkshop.sg', rel); bad += 1
about = open(os.path.join(root, 'about/index.html'), encoding='utf-8').read()
if "built from the workshop's public Google Business Profile" not in about or 'They are not endorsed by or arranged with the business.' not in about: print('About page missing Basic-listing note'); bad += 1
# TRUST (Edwin 3 Nov 2026): no page may say preview/placeholder, or give the old wrong source (website, Facebook, WhatsApp Business page)
for _r, _d, _fs in os.walk(root):
    for _fn in _fs:
        if _fn.endswith('.html'):
            _t = open(os.path.join(_r, _fn), encoding='utf-8').read()
            _vis = re.sub(r'<(script|style)\b.*?</\1>', '', _t, flags=re.S)
            _vis = re.sub(r'<[^>]+>', ' ', _vis)
            for _w in ('This is a preview', 'brand name is a placeholder', 'Facebook or WhatsApp Business page', 'publishes itself'):
                if _w.lower() in _vis.lower(): print('WRONG/PLACEHOLDER TEXT "%s" in' % _w, os.path.relpath(os.path.join(_r, _fn), root)); bad += 1
if 'https://maps.google.com/help/terms_maps/' not in open(os.path.join(root, 'terms/index.html'), encoding='utf-8').read(): print('Terms missing Google Maps terms link'); bad += 1
if 'https://policies.google.com/privacy' not in open(os.path.join(root, 'privacy/index.html'), encoding='utf-8').read(): print('Privacy missing Google privacy link'); bad += 1
if 'id="remove"' not in open(os.path.join(root, 'list-your-workshop/index.html'), encoding='utf-8').read(): print('list page missing #remove section'); bad += 1
if 'Featured (paid)' not in home_src or 'Sponsored' in home_src: print('home carousel must be labelled Featured (paid)'); bad += 1
for rel in ('sitemap.xml', 'llms.txt'):
    t = open(os.path.join(root, rel), encoding='utf-8').read()
    if CANON not in t or 'pageonesingapore.com/preview' in t: print('not on sgcarworkshop.sg:', rel); bad += 1
    for u in re.findall(r'<loc>([^<]+)</loc>', t):
        if not u.startswith(CANON): print('sitemap URL off-domain', u); bad += 1
if 'maps/dir' in open(os.path.join(root, 'index.html'), encoding='utf-8').read() and False: pass
# dir.js tracker
djs = open(os.path.join(root, 'assets', 'dir.js'), encoding='utf-8').read()
if "LIVE_HOST='sgcarworkshop.sg'" not in djs or not all(k in djs for k in ('maps', 'directions', 'hours')): print('dir.js must count maps_/directions_/hours_ taps on sgcarworkshop.sg'); bad += 1
# TAP COUNTER (Edwin 2 Nov 2026): every WhatsApp and Call link must carry the tracking hook (data-cta + data-tier) so dir.js counts it per workshop.
# Page One's own WhatsApp (owner boxes: claim/remove links) is the only exception and is counted by its own claim_/remove_ hook.
from data import PAGE_ONE_WA as _P1
for _root, _d, _fs in os.walk(sys.argv[1] if len(sys.argv) > 1 else '../site'):
    for _fn in _fs:
        if not _fn.endswith('.html'): continue
        _p = os.path.join(_root, _fn); _h = open(_p, encoding='utf-8').read()
        for _a in re.findall(r'<a\b[^>]*>', _h):
            _m = re.search(r'href="([^"]*)"', _a)
            if not _m: continue
            _u = _m.group(1)
            if _u.startswith('tel:'):
                if 'data-cta="call_dir_' not in _a or 'data-tier="' not in _a: print('tel: link without the tap hook', _p, _u); bad += 1
            elif 'wa.me/' in _u:
                if re.search(r'wa\.me/%s' % re.escape(str(_P1)), _u): continue
                if 'data-cta="whatsapp_dir_' not in _a or 'data-tier="' not in _a: print('wa.me link without the tap hook', _p, _u[:60]); bad += 1
if not all(k in djs for k in ("sgcarworkshop-test", "cta_label", "sendBeacon", "functions/track")) or 'visitor_id' in djs: print('dir.js tap counter must send site/sgcarworkshop(-test), cta_label slug, use sendBeacon and send no visitor_id'); bad += 1
# Sort: Premium, Verified, then Basic A to Z (never by rating)
order = [(0, '') if e['tier'] == 'premium_leadgen' else (1, e['name'].lower()) for e in ENTRIES]
if order != sorted(order): print('ENTRIES not sorted: paid Featured first, then everyone else A to Z'); bad += 1
# Every tel: link anywhere in the site must be an SG mobile (+65 8/9 + 7 digits), the same number as WhatsApp (Edwin 2 Nov 2026)
for _root, _d, _fs in os.walk(sys.argv[1] if len(sys.argv) > 1 else '../site'):
    for _fn in _fs:
        if _fn.endswith('.html'):
            for _t in re.findall(r'href="tel:([^"]*)"', open(os.path.join(_root, _fn), encoding='utf-8').read()):
                if not re.fullmatch(r'\+65[89]\d{7}', _t): print('tel: is not an SG mobile', _t, os.path.join(_root, _fn)); bad += 1
# DATA: every record file passes the schema; forbidden Google fields; removed/pending place_ids never live; snapshots stay private
import subprocess
live_pids = {e['place_id'] for e in ENTRIES if e.get('place_id')}
for f in _data.workshop_files():
    r = json.load(open(f))
    if _data.FORBIDDEN_KEYS & set(r): print('RECORD', os.path.basename(f), 'stores Google-only field(s)'); bad += 1
    for p in _data.record_problems(r): print('RECORD', os.path.basename(f), p); bad += 1
    if r['status'] != 'active' and r['place_id'] in live_pids: print('NON-ACTIVE record is live', r['slug']); bad += 1
# RIGID DATABASE RULES (Edwin, 3 Nov 2026): (1) no record without a confirmed SG mobile; (2) no duplicates, tracked by the permanent registry
import registry as _reg
_REG = _reg.load()
for f in _data.workshop_files():                       # every stored record, even pending, must hold a Google/own-site confirmed SG mobile and a passed screen
    r = json.load(open(f))
    if not any(p.get('kind') == 'mobile' and _reg.MOBILE_RE.match(p.get('e164', '')) and p.get('source') in ('google_profile', 'own_site') for p in r.get('phones', [])): print('RECORD', os.path.basename(f), 'has no confirmed SG mobile'); bad += 1
    if (r.get('google_screen') or {}).get('passed') is not True: print('RECORD', os.path.basename(f), 'has not passed the Google screen (unscreened or failed records must not be stored)'); bad += 1
for e in ENTRIES:
    if not _reg.MOBILE_RE.match(e.get('phone') or ''): print('LISTING without SG mobile', e['slug']); bad += 1
for _k in ('slug', 'place_id'):
    _c = {}
    for e in ENTRIES:
        if e.get(_k): _c.setdefault(e[_k], []).append(e['slug'])
    for _v, _l in _c.items():
        if len(_l) > 1: print('DUPLICATE', _k, _v, _l); bad += 1
_pc = {}
for e in ENTRIES: _pc.setdefault(e.get('phone'), []).append(e['slug'])
for _v, _l in _pc.items():
    if len(_l) > 1: print('WARNING (not a failure): shared mobile', _v, _l)
_seen = {}
for x in _REG:
    if x.get('status') not in _reg.STATUSES: print('registry bad status', x.get('slug')); bad += 1
    if set(x) != {'place_id', 'slug', 'name_norm', 'postal_code', 'mobile', 'status', 'date'}: print('registry entry has wrong fields', x.get('slug')); bad += 1
    if x.get('mobile') and not _reg.MOBILE_RE.match(x['mobile']): print('registry bad mobile', x.get('slug')); bad += 1
    for _k in ('place_id', 'slug'):
        if x.get(_k):
            if (_k, x[_k]) in _seen: print('registry DUPLICATE', _k, x[_k]); bad += 1
            _seen[(_k, x[_k])] = 1
    if x['status'] != 'built' and x.get('place_id') in live_pids: print('registry says not built but listing is live', x['slug']); bad += 1
_blt = {x['slug'] for x in _REG if x['status'] == 'built'}
for e in ENTRIES:
    if e['slug'] not in _blt: print('live listing missing from registry (run registry.py sync)', e['slug']); bad += 1
_ids = {x['place_id'] for x in _REG if x.get('place_id')}; _mob = {x['mobile'] for x in _REG if x.get('mobile')}
_cq = _data._jload('candidate_queue.json', [])
_qm = set(); _qp = set()
for c in _cq:
    if c['place_id'] in _ids or c['place_id'] in _qp or _reg.match(_REG, None, None, c['name_hint'], c['postal_code'])[0] or c['place_id'] in {r.get('place_id') for r in map(lambda f: json.load(open(f)), _data.workshop_files())}:
        print('QUEUE candidate duplicates the registry or itself', c['name_hint']); bad += 1
    _qp.add(c['place_id']); _qm.add(c['mobile_hint'])
    if set(c) != {'place_id', 'name_hint', 'address_hint', 'postal_code', 'mobile_hint', 'source', 'added'}: print('queue entry has wrong fields', c.get('name_hint')); bad += 1
if _data.REMOVED & live_pids: print('REMOVED place_id is live', _data.REMOVED & live_pids); bad += 1
_ign = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.gitignore')).read() if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.gitignore')) else ''
if 'snapshots/' not in _ign: print('.gitignore must list snapshots/'); bad += 1
# Google API: places.googleapis ONLY in assets/livephone.js (one URL, fields businessStatus,regularOpeningHours); the browser key ONLY on Basic profile pages
# (Maps Embed iframe URL + data-key of the hours box); pages with an OSM map carry no Places content at all.
for dp, dn, fns in os.walk(root):
    for fn in fns:
        if fn.endswith(('.html', '.js', '.css', '.txt', '.xml')):
            rel = os.path.relpath(os.path.join(dp, fn), root)
            t = open(os.path.join(dp, fn), encoding='utf-8').read()
            is_profile = re.match(r'workshops/[^/]+/index\.html$', rel) is not None
            keys = re.findall(r'AIza[0-9A-Za-z_-]{20,}', t)
            if 'maps?cid' in t or 'maps/place/?q=place_id' in t: print('OLD cid / place link in', rel); bad += 1
            if rel == 'assets/livephone.js':
                if keys or t.count('places.googleapis') != 1 or 'fields=businessStatus,regularOpeningHours&' not in t or re.search(r'nationalPhoneNumber|internationalPhoneNumber|photos|rating|reviews|websiteUri', t):
                    print('livephone.js must make exactly one Places URL with only businessStatus,regularOpeningHours'); bad += 1
                continue
            if 'places.googleapis' in t or 'gmaps-key' in t: print('GOOGLE API REFERENCE in', rel); bad += 1
            if keys:
                allowed = is_profile and len(set(keys)) == 1
                if not allowed: print('GOOGLE KEY outside a profile page in', rel); bad += 1
            if OSM in t and (keys or 'hoursbox' in t or 'livephone.js' in t or 'google.com/maps/embed' in t): print('OSM page carries Places content', rel); bad += 1
            if 'livephone.js' in t and not (is_profile and 'class="hoursbox"' in t): print('livephone.js loaded outside a profile hours box', rel); bad += 1
# robots guard (Edwin 2 Nov 2026): sgcarworkshop.sg and the preview serve the SAME folder. robots.txt (preview) must keep Disallow: /;
# robots-live.txt must be crawlable with the Sitemap line; htaccess/.htaccess must route /robots.txt to it on sgcarworkshop.sg only.
# A LIVE build (SGCW_LIVE=1 / site-live) must have a crawlable robots.txt itself.
_rd = lambda n: open(os.path.join(root, n)).read() if os.path.exists(os.path.join(root, n)) else ''
_dis = lambda t: [l for l in t.splitlines() if re.match(r'^\s*disallow\s*:\s*/\s*$', l, re.I)]
_live = os.path.basename(root) == 'site-live' or os.environ.get('SGCW_LIVE') == '1'
_okrobots = lambda t: not _dis(t) and re.search(r'^User-agent:\s*\*\s*\nAllow:\s*/\s*$', t, re.M) and 'Sitemap: https://sgcarworkshop.sg/sitemap.xml' in t
_rl = _rd('robots-live.txt')
if not _okrobots(_rl): print('robots-live.txt must be "User-agent: *" / "Allow: /" plus Sitemap: https://sgcarworkshop.sg/sitemap.xml and no Disallow: /'); bad += 1
if _live:
    if not _okrobots(_rd('robots.txt')): print('LIVE robots.txt disallows / or lacks Allow/Sitemap'); bad += 1
elif not _dis(_rd('robots.txt')): print('PREVIEW robots.txt must keep Disallow: / (it is what pageonesingapore.com serves)'); bad += 1
_ht = os.path.join(root, '..', 'htaccess', '.htaccess')
_h = open(_ht).read() if os.path.exists(_ht) else ''
if not (re.search(r'^RewriteCond %\{HTTP_HOST\} \^\(www\\\.\)\?sgcarworkshop\\\.sg\$ \[NC\]$', _h, re.M) and re.search(r'^RewriteRule \^robots\\\.txt\$ robots-live\.txt \[END\]$', _h, re.M) and 'RewriteOptions Inherit' in _h):
    print('htaccess/.htaccess must rewrite /robots.txt to robots-live.txt only for (www.)sgcarworkshop.sg, with RewriteOptions Inherit'); bad += 1

# GUIDES (Edwin 3 Nov 2026): 10 pages, in sitemap and llms.txt, no prices, no endorsement words, workshop links real
import guides as _gd
_bad0 = bad
_sm = open(os.path.join(root, 'sitemap.xml')).read(); _ll = open(os.path.join(root, 'llms.txt')).read()
if len(_gd.GUIDES) != 10: print('expected 10 guides'); bad += 1
for _g in _gd.GUIDES:
    _p = os.path.join(root, _gd.gpath(_g), 'index.html')
    if not os.path.exists(_p): print('guide page missing', _g['slug']); bad += 1; continue
    _t = open(_p, encoding='utf-8').read()
    _v = re.sub(r'<(script|style).*?</\1>', '', _t, flags=re.S); _v = re.sub(r'<[^>]+>', ' ', _v)
    if _gd.gpath(_g) not in _sm or _gd.gpath(_g) not in _ll: print('guide not in sitemap/llms.txt', _g['slug']); bad += 1
    if re.search(r'S\$|\$\s?\d|\bSGD\b|\d\s?dollars', _v): print('guide states a price', _g['slug']); bad += 1
    if _NameMasked(re.compile(r'\b(best|trusted|recommended|guaranteed|cheapest)\b', re.I)).search(_v): print('guide has endorsement wording', _g['slug']); bad += 1
    for _l in re.findall(r'href="\.\./\.\./workshops/([a-z0-9-]+)/"', _t):
        if not os.path.exists(os.path.join(root, 'workshops', _l, 'index.html')): print('guide links to a missing workshop', _l); bad += 1
if 'guides/' not in _sm: print('guides index not in sitemap'); bad += 1
if bad == _bad0: print('guides ok: 10 pages, in sitemap and llms.txt, no prices')

# Template rules (Edwin 3 Nov 2026): shared header and footer everywhere, every workshop page is a stack of block templates
SET = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.json')))
def _blocks(h):
    """[(name, inner html)] for each top-level block wrapper; also returns the html left over once the blocks are removed."""
    out, rest, pos = [], [], 0
    for m in re.finditer(r'<div class="blk" data-block="([a-z_]+)">', h):
        if m.start() < pos: continue
        depth, i = 1, m.end()
        for t in re.finditer(r'<(/?)div\b', h[i:]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                out.append((m.group(1), h[i:i + t.start()])); rest.append(h[pos:m.start()]); pos = i + t.end() + 1; break
    rest.append(h[pos:])
    return out, ''.join(rest)
for _f in files:
    _rel = os.path.relpath(_f, root); _h = open(_f, encoding='utf-8').read()
    if 'http-equiv="refresh"' in _h or 'This folder is not a page' in _h or _rel == '404.html': continue
    if '<header class="top">' not in _h or '<footer class="ft">' not in _h or '<main id="main">' not in _h: print('page lacks the shared header, main or footer', _rel); bad += 1
for _e in ENTRIES:
    _h = open(os.path.join(root, 'workshops', _e['slug'], 'index.html'), encoding='utf-8').read()
    _m = re.search(r'<main id="main">(.*?)</main>', _h, re.S)
    _bl, _left = _blocks(_m.group(1))
    _names = [n for n, _ in _bl]
    for _req in SET['required_blocks']:
        if _req not in _names: print('workshop page lacks block', _req, _e['slug']); bad += 1
    for _n, _inner in _bl:
        if not re.search(r'[A-Za-z0-9]', re.sub(r'<[^>]+>', '', _inner)) and not re.search(r'<(img|iframe|svg)', _inner): print('empty block rendered', _n, _e['slug']); bad += 1
        _nohead = re.sub(r'<h[1-6][^>]*>.*?</h[1-6]>', '', _inner, flags=re.S)
        if not re.search(r'[A-Za-z0-9]', re.sub(r'<[^>]+>', '', _nohead)) and not re.search(r'<(img|iframe|svg)', _nohead): print('block has a heading but no visible content', _n, _e['slug']); bad += 1
        if _n == 'pricing' and not re.search(r'<table class="ptab".*?<td>.*?\$\s?\d', _inner, re.S): print('Pricing block has no price table with prices', _e['slug']); bad += 1
        for _im in re.findall(r'<img[^>]*>', _inner):
            if ' width="' not in _im or ' height="' not in _im: print('image in block has no width/height (blank gap before it loads)', _n, _e['slug']); bad += 1
            if 'decoding="async"' in _im and 'loading="lazy"' not in _im: print('eager image decodes async (can stay blank in full-page screenshots)', _n, _e['slug']); bad += 1
            if 'loading="lazy"' in _im and _n in ('photos', 'gallery'): print('gallery image is lazy-loaded (blank before scrolling)', _n, _e['slug']); bad += 1
    _order = _e.get('blocks') or SET['block_order'][_e['tier']]
    if [n for n in _order if n in _names] != _names: print('block order differs from the data file', _e['slug'], _names); bad += 1
    _left = re.sub(r'<nav class="crumbs".*?</nav>', '', _left, flags=re.S)
    if re.sub(r'<[^>]+>|\s', '', _left.replace('<div class="w nar basicpg pilot">', '').replace('<div class="w nar prem">', '').replace('</div>', '')): print('hand-written markup outside the block templates', _e['slug']); bad += 1
# Thin-page and sitemap rules (Edwin 3 Nov 2026)
_mf = json.load(open(os.path.join(root, '..', 'build-manifest.json')))
_sm2 = open(os.path.join(root, 'sitemap.xml')).read()
_locs = set(re.findall(r'<loc>https://[^/]+/(.*?)</loc>', _sm2))
for _pth in _mf['noindex']:
    _t = open(os.path.join(root, _pth, 'index.html'), encoding='utf-8').read()
    if 'content="noindex, follow"' not in _t: print('manifest noindex page lacks the meta tag', _pth); bad += 1
    if _pth in _locs: print('noindex page is in sitemap.xml', _pth); bad += 1
for _pth, _n in _mf['free_count'].items():
    if _n < _mf['min_free'] and _pth not in _mf['noindex'] and _pth not in _mf.get('index_exceptions', []): print('thin page is indexable', _pth, _n); bad += 1
    if _n >= _mf['min_free'] and _pth in _mf['noindex'] and _pth not in _mf.get('index_exceptions', []): print('page with enough workshops is noindexed', _pth, _n); bad += 1
for _pth in ('areas/north/', 'areas/north-east/', 'areas/east/', 'areas/west/', 'areas/central/', 'areas/mobile/'):
    if os.path.exists(os.path.join(root, _pth, 'index.html')) and _pth not in _mf['noindex']: print('region page must be noindex', _pth); bad += 1
for _pth in _locs:
    if _pth and not os.path.exists(os.path.join(root, _pth, 'index.html')): print('sitemap URL has no page', _pth); bad += 1
for _d, _ds, _fs in os.walk(root):
    if _d != root and 'index.html' not in _fs: print('folder with no index page (directory listing risk)', os.path.relpath(_d, root)); bad += 1
for _old, _new in _mf['redirects'].items():
    if not os.path.exists(os.path.join(root, _new, 'index.html')) or (_new in _mf['redirects']): print('redirect is not one hop to a real page', _old, _new); bad += 1
# Rating rule (Edwin 3 Nov 2026): the ONLY rating text is the standard rating line:
#   <p class="rtg"><b>4.9</b> (600+ Google ratings) (checked November 2026) <a ...>See Google reviews</a></p>
_STD = re.compile(r'<p class="rtg"><b>[0-5]\.\d</b> \([\d,]+\+? Google ratings?\) \(checked (January|February|March|April|May|June|July|August|September|October|November|December) 20\d\d\) <a href="[^"]+" target="_blank" rel="noopener" data-cta="gr_[a-z0-9-]+">See Google reviews</a></p>')
_PAIDPG = {'workshops/%s/' % _e['slug'] for _e in ENTRIES if _e['tier'] == 'premium_leadgen'}
for _f in files:
    _t = open(_f, encoding='utf-8').read()
    for _m in re.findall(r'<p class="rtg">.*?</p>', _t):
        if not _STD.fullmatch(_m): print('RATING text is not the standard rating line', _f, _m[:120]); bad += 1
        elif 'maps' not in _m and 'share.google' not in _m: print('RATING line has no Google link', _f); bad += 1
    _rest = re.sub(r'<p class="rtg">.*?</p>', '', _t)
    _rel = os.path.relpath(_f, root)
    if _rel[:-10] in _PAIDPG: continue   # a paying client's own page keeps its own reviews line (not touched)
    _txt = re.sub(r'\s+', ' ', re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', _rest, flags=re.S))
    if re.search(r'\b[0-5]\.\d\s*\(\s*\d[\d,]*\+?\s*(Google )?(reviews?|ratings?)|\bRated [0-5]\.\d|\b[0-5]\.\d\s*(out of 5|stars?)\b|\u2605', _txt):
        print('RATING text outside the standard rating line', _f); bad += 1
# Edwin 3 Nov 2026 rules
for _f in files:
    _t = open(_f, encoding='utf-8').read(); _rel = os.path.relpath(_f, root)
    if re.search(r'like any other entry', _t, re.I): print('banned phrase "like any other entry"', _f); bad += 1
    # images only on sgcarworkshop.sg (relative or the live domain); hotlinked hosts still pending a copy are counted below
    for _u in re.findall(r'<img[^>]*?\bsrc="([^"]+)"|property="og:image" content="([^"]+)"|"image":\s*"([^"]+)"', _t):
        _u = next(x for x in _u if x)
        _h = urlparse(_u).netloc
        if _h and _h not in ('sgcarworkshop.sg', 'www.sgcarworkshop.sg'):
            if _h in SET_IMG['hosts']: HOTLINK.add(_u)
            else: print('IMAGE not on sgcarworkshop.sg', _rel, _u[:90]); bad += 1
    # no reviewer names or Google review text
    if re.search(r'authorAttribution|reviewer|"author"\s*:\s*\{[^}]*"Person"|class="rv-google|relativePublishTimeDescription|Reviewed by', _t): print('reviewer name or Google review markup', _rel); bad += 1
    # ItemList: no paid listing
    for _blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', _t, re.S):
        try: _j = json.loads(_blk)
        except Exception: continue
        for _o in (_j if isinstance(_j, list) else [_j]):
            if isinstance(_o, dict) and _o.get('@type') == 'ItemList':
                for _it in _o.get('itemListElement', []):
                    _m2 = re.search(r'/workshops/([^/]+)/', _it.get('url', ''))
                    if _m2 and ENT_TIER.get(_m2.group(1)) == 'premium_leadgen': print('paid listing inside an ItemList', _rel, _m2.group(1)); bad += 1
    # A to Z: every card list that holds a founder-owned or Verified listing must be A to Z (the separate Featured (paid) block is the only exception)
    _body = re.sub(r'<section class="alt featblock">.*?</section>', '', _t, flags=re.S)
    if _rel == 'index.html': _body = re.sub(r'<section id="workshops".*?</section>', '', _body, flags=re.S)   # homepage list has its own group order (Edwin 3 Nov 2026), checked below
    for _sec in re.findall(r'<section[^>]*>.*?</section>', _body, re.S):
        _cards = re.findall(r'<article class="card[^"]*"[^>]*data-tier="([^"]+)".*?<h3><a [^>]*>([^<]+)</a>', _sec, re.S)
        if len(_cards) > 1 and any(t in ('none', 'premium') for t, _n in _cards):  # paid cards, wherever they sit, are the Featured (paid) group
            _names = [html_unescape(n).lower() for t, n in _cards if t != 'premium_leadgen']
            if _names != sorted(_names): print('founder or Verified listing out of A to Z order', _rel, _names[:6]); bad += 1
# Town hub: indexable only if it shows every workshop card of its estates; one-estate towns index the estate page and noindex the hub
for _pth, _n in _mf.get('hub_cards', {}).items():
    _hp = open(os.path.join(root, _pth, 'index.html'), encoding='utf-8').read()
    _shown = len(re.findall(r'<article class="card', re.sub(r'<section class="alt featblock">.*?</section>', lambda m: m.group(0), _hp, flags=re.S)))
    if _pth not in _mf['noindex'] and _shown != _n: print('indexable town hub does not show every workshop card', _pth, _shown, _n); bad += 1
# Reviewer names or copied review text must never be stored
_gdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
for _sub in ('google_cache', 'workshops'):
    for _fn in os.listdir(os.path.join(_gdir, _sub)):
        if _fn.endswith('.json'):
            _txt2 = open(os.path.join(_gdir, _sub, _fn)).read()
            if re.search(r'"(reviews|authorAttribution|author_name|reviewer)"\s*:', _txt2): print('stored Google review text or reviewer name', _sub, _fn); bad += 1
if HOTLINK: print('NOTE: %d hotlinked images still pending a copy to sgcarworkshop.sg (hosts in settings.json image_hosts_pending)' % len(HOTLINK))
_css = open(os.path.join(root, 'assets', 'dir.css'), encoding='utf-8').read()
if re.search(r'\.rv[^{}]*\{[^}]*(opacity:\s*0\b|visibility:\s*hidden)', re.sub(r'/\*.*?\*/', '', _css, flags=re.S)): print('dir.css hides .rv blocks by default (scroll-reveal): blocks must be visible without scrolling'); bad += 1
# Homepage groups (Edwin 3 Nov 2026): Featured (paid), Verified, Basic; at most HOME_N cards each in the page, the rest in the template
import build as _b
_hs = re.search(r'<section id="workshops".*?</section>', open(os.path.join(root, 'index.html'), encoding='utf-8').read(), re.S).group(0)
_vis, _tpl = (_hs.split('<template id="more-cards">') + [''])[:2]
_pat = r'<article data-g="([a-z]+)"[^>]*class="card[^"]*".*?<h3><a href="(?:\./)?workshops/([a-z0-9-]+)/"'
_v = re.findall(_pat, _vis, re.S); _t = re.findall(_pat, _tpl, re.S)
_order = [g[0] for g in _b.HOME_GROUPS]
_gv = [g for g, _ in _v]
_err = []
if _gv != sorted(_gv, key=_order.index): _err.append('groups out of order')
for _g in _order:
    if _gv.count(_g) > _b.HOME_N: _err.append('%s shows %d > %d' % (_g, _gv.count(_g), _b.HOME_N))
for _g, _s in _v + _t:
    if _b.home_group(next(e for e in ENTRIES if e['slug'] == _s)) != _g: _err.append('%s in wrong group %s' % (_s, _g))
if sorted(s2 for _, s2 in _v + _t) != sorted(e['slug'] for e in ENTRIES): _err.append('homepage does not hold every listing once')
if 'data-sort="near"' not in _hs or 'data-sort="rating"' not in _hs: _err.append('sort bar missing')
if _err: print('homepage groups:', _err[:6]); bad += 1
else: print('homepage groups ok, shown/total:', [(_g, _gv.count(_g), _gv.count(_g) + [g for g, _ in _t].count(_g)) for _g in _order])
# Card rules v2 (Edwin 5 Nov 2026): source logs are PRIVATE (repo is public): never in the repo or the built site; every v2 card has one in the project folder.
_CS = '/mnt/project-files/sgcarworkshop/card_sources'
for _dp, _dn, _fn in os.walk(os.path.join(root, '..')):
    if 'card_sources' in _dp.split(os.sep) or any('card_source' in f for f in _fn): print('source logs must not be in the repo or site:', _dp); bad += 1
for _f in sorted(os.listdir(os.path.join(root, '..', 'data', 'pilot'))):
    _pl = json.load(open(os.path.join(root, '..', 'data', 'pilot', _f)))
    if not _pl.get('card_rules'): continue
    _sl = _f[:-5]
    if not _pl.get('services') or not _pl.get('makes'): print('v2 card needs services and a car makes line', _sl); bad += 1
    for _w in (_pl.get('themes', ''), ' '.join(_pl.get('specialties', [])), ' '.join(_pl.get('good_to_know', []))):
        if re.search(r'[\u201c\u201d"]', _w): print('v2 card must not quote anyone', _sl); bad += 1
    if os.path.isdir(_CS):
        _lp = os.path.join(_CS, _sl + '.json')
        if not os.path.exists(_lp): print('v2 card has no private source log', _sl); bad += 1
        else:
            for _c in json.load(open(_lp)).get('claims', []):
                if not (_c.get('claim') and _c.get('source_url') and _c.get('checked') and _c.get('snippet')): print('source log claim incomplete', _sl, _c.get('claim')); bad += 1
    else:
        print('WARNING (not a failure): project folder not mounted, source logs not checked for', _sl)

# POSITIVE ONLY (Edwin 5 Nov 2026): no complaint or negative review summary about any workshop, on any page, attribute, feed or data file.
import positive_only as _PO
for _dp, _dn, _fn in os.walk(root):
    for _f in _fn:
        if _f.endswith(('.html', '.json', '.txt', '.xml', '.js')):
            for _s in _PO.page_hits(open(os.path.join(_dp, _f), errors='ignore').read())[:1]: print('NEGATIVE line on page (positive-only rule):', os.path.relpath(os.path.join(_dp, _f), root), _s); bad += 1
for _g in ('pilot', 'google_cache'):
    for _f in os.listdir(os.path.join(root, '..', 'data', _g)):
        _d = json.load(open(os.path.join(root, '..', 'data', _g, _f)))
        for _k in ('themes', 'review_themes', 'lede', 'good_for_note', 'good_to_know_note'):
            if isinstance(_d.get(_k), str) and _PO.bad(_d[_k]): print('NEGATIVE line in data (positive-only rule):', _g, _f, _PO.bad(_d[_k])[0]); bad += 1

print('pages checked:', len(files), 'problems:', bad)
sys.exit(1 if bad else 0)
