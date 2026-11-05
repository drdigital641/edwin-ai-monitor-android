#!/usr/bin/env python3
"""Finish a batch of Basic cards made by `basic_agent.py enrich-queue` (Edwin 4 Nov 2026: "optimize card building to be efficient").

Everything on a card comes from the workshop's own Google Place Details answer (Google is the source of truth):
name, mobile, address, hours, rating, coordinates. The only hand-written part is the short "customers mention" line,
written from Google's review text in our own words (never quoted, no reviewer names).

    python3 finish_batch.py prep  --raw-dir DIR            # writes /tmp/claude-0/s/batch.json: proposed name/slug/estate + review digest
    (edit batch.json: fix names, set estate where null, fill "themes" and "mentioned")
    python3 finish_batch.py apply --raw-dir DIR            # applies batch.json to data/, records go active

Name rule (PERMANENT): the exact Google Business Profile name; only "Pte Ltd"-type suffixes and taglines are dropped.
Estate: address keyword first, else the estate of the nearest listed workshop within 1.2 km, else null (add one to areas._IE)."""
import argparse, glob, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')
BATCH = '/tmp/claude-0/s/batch.json'
# Coordinates come from OneMap (Google's lat/lng may not be stored; it is used only to suggest the nearest estate during prep).
# OneMap is blocked from this host: run the curl loop in the Controller sandbox and save {postal: [lat, lng]} here.
ONEMAP = '/tmp/claude-0/s/onemap_cache.json'
# Card rules v2 (Edwin 5 Nov 2026, sources narrowed 22:23 SGT): sources are Google Place Details plus the workshop's own website ONLY
# when Google lists one (websiteUri), never Facebook/Carousell/Instagram/other social pages; a blocked or failed site is skipped with no
# retries. One PRIVATE source log per card (the repo is public), with a "pilot" section of own-words card fields
# and "claims" [{claim, source_url, checked, snippet}]. Never copy these files into the repo or the site.
CARD_SOURCES = '/mnt/project-files/sgcarworkshop/card_sources'
V2_KEYS = ('lede', 'chips', 'services', 'services_note', 'specialties', 'makes', 'makes_note', 'good_to_know', 'good_to_know_note', 'faqs', 'sources', 'themes', 'mentioned_services')
sys.path.insert(0, HERE)
import areas  # noqa: E402
import positive_only  # noqa: E402

SUFFIX = re.compile(r'\s*(\((s|pte)\)\s*)?\b(pte\.?\s*ltd\.?|private limited|ltd|p/l|llp|pte)(?![\w/])\.?|\s*\((s|pte)\)\s*ltd\.?', re.I)
ESTATE_PA = {'soon-lee-street-pioneer': 'Pioneer', 'bukit-merah-lane-3': 'Bukit Merah', 'jurong-west-avenue-5': 'Jurong West'}
TOWN_PA = {'toh-guan-jurong-east': 'Jurong East', 'sin-ming-bishan': 'Bishan', 'kaki-bukit': 'Bedok', 'ubi': 'Geylang', 'macpherson': 'Geylang', 'defu-hougang': 'Hougang', 'serangoon-north': 'Serangoon', 'kranji': 'Mandai', 'sembawang-admiralty': 'Sembawang', 'woodlands': 'Woodlands', 'yishun': 'Yishun', 'tampines': 'Tampines', 'toa-payoh': 'Toa Payoh'}


SOCIAL = re.compile(r'(facebook\.com|fb\.com|fb\.me|carousell\.|instagram\.com|tiktok\.com|twitter\.com|x\.com/|linkedin\.com|youtube\.com|threads\.net|wa\.me|t\.me|xiaohongshu|lemon8)', re.I)


def bad_sources(log, g):
    """Sources allowed (Edwin 5 Nov 2026): Google Place Details and pages on the site Google lists as websiteUri, never social pages."""
    import urllib.parse as up
    site = (g or {}).get('websiteUri') or ''
    host = up.urlparse(site).netloc.lower().removeprefix('www.') if site and not SOCIAL.search(site) else None
    out = []
    urls = [u for u in log.get('sources_used', []) if u.startswith('http')] + [c.get('source_url', '') for c in log.get('claims', [])]
    for u in urls:
        if not u.startswith('http') or 'google.com/maps' in u: continue
        h = up.urlparse(u).netloc.lower().removeprefix('www.')
        if SOCIAL.search(u) or not host or h != host: out.append(u)
    return out


def jl(p, d=None):
    try: return json.load(open(p))
    except Exception: return d


def jw(p, o): json.dump(o, open(p, 'w'), indent=1, ensure_ascii=False)


def clean_name(n):
    n = re.split(r'\s+[|–—]\s+|\s+-\s+', n)[0]          # taglines after " | " or " - "
    n = re.sub(r'\s*\((?:[^)]*(workshop|specialist|service|repair|centre|center|singapore)[^)]*)\)', '', n, flags=re.I)
    n = SUFFIX.sub('', n)
    n = re.sub(r'\(\s+', '(', re.sub(r'\s+\)', ')', n))
    return re.sub(r'\s{2,}', ' ', n).strip(' ,.-')


def slugify(n): return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', n.lower())).strip('-')[:60]


def dist(a, b, c, d): return math.hypot((a - c) * 111.0, (b - d) * 111.0 * math.cos(math.radians(1.35)))


def listed():
    out = []
    for f in glob.glob(D + '/workshops/*.json'):
        r = jl(f, {})
        if r.get('status') == 'active' and r.get('estate') and r.get('lat'): out.append(r)
    return out


def town_pa(est):
    if est in ESTATE_PA: return ESTATE_PA[est]
    t = areas.ESTATES[est]['town']
    for r in listed():
        if r['estate'] == est and r.get('planning_area'): return r['planning_area']
    return TOWN_PA.get(t, areas.TOWNS[t]['name'])


def prep(a):
    pend = [jl(f) for f in glob.glob(D + '/workshops/*.json')]
    pend = [r for r in pend if r and r.get('status') == 'pending' and r.get('place_id')]
    ref = listed(); out = []
    for r in sorted(pend, key=lambda r: r['slug']):
        g = jl(os.path.join(a.raw_dir, r['place_id'] + '.json'), {})
        if not g: continue
        gn = (g.get('displayName') or {}).get('text') or r['name']; nn = clean_name(gn)
        loc = g.get('location') or {}; la, lo = loc.get('latitude'), loc.get('longitude')
        est = areas.estate_for(r['address']['street'], r.get('postal_code')); how = 'address'
        if not est and la:
            near = sorted(ref, key=lambda x: dist(la, lo, x['lat'], x['lng']))[:1]
            if near and dist(la, lo, near[0]['lat'], near[0]['lng']) <= 1.2: est, how = near[0]['estate'], 'near %s' % near[0]['slug']
        revs = [re.sub(r'\s+', ' ', (v.get('text') or {}).get('text', ''))[:350] for v in (g.get('reviews') or [])]
        out.append({'old': r['slug'], 'slug': slugify(nn), 'google_name': gn, 'name': nn, 'estate': est, 'estate_how': how if est else None,
                    'street': r['address']['street'], 'postal': r['postal_code'], 'rating': g.get('rating'), 'count': g.get('userRatingCount'),
                    'themes': '', 'mentioned': [], 'reviews': revs})
    jw(BATCH, out)
    print('%d records -> %s; no estate: %s' % (len(out), BATCH, [x['old'] for x in out if not x['estate']]))
    om = jl(ONEMAP, {}); need = sorted({x['postal'] for x in out if x['postal'] and x['postal'] not in om})
    print('postals needing OneMap: ' + ' '.join(need))
    for x in out:
        if x['name'] != x['google_name']: print('  name cleaned: %r -> %r' % (x['google_name'], x['name']))


def apply(a):
    import datetime as dt
    day = dt.date.today().isoformat(); B = jl(BATCH, [])
    blocks = jl(D + '/workshops/m-werkz.json')['blocks']; reg = jl(D + '/registry.json'); done = []; skip = []
    for x in B:
        x['themes'] = positive_only.clean(x.get('themes'))   # positive-only rule (Edwin 5 Nov 2026): complaint sentences never reach a card
        x['mentioned'] = [m for m in x.get('mentioned', []) if not positive_only.bad(m)]
        if not x.get('estate') or not x.get('themes'): skip.append(x['old']); continue
        r = jl('%s/workshops/%s.json' % (D, x['old'])); g = jl(os.path.join(a.raw_dir, r['place_id'] + '.json'))
        slug = x['slug']
        if slug != x['old']:
            if os.path.exists('%s/workshops/%s.json' % (D, slug)): sys.exit('slug taken: ' + slug)
            os.rename('%s/workshops/%s.json' % (D, x['old']), '%s/workshops/%s.json' % (D, slug))
            os.rename('%s/google_cache/%s.json' % (D, x['old']), '%s/google_cache/%s.json' % (D, slug))
            for e in reg:
                if e.get('place_id') == r['place_id']: e['slug'] = slug
        est = x['estate']; geo = jl(ONEMAP, {}).get(r['postal_code'])
        if not geo: skip.append(x['old'] + ' (no OneMap coordinates for %s)' % r['postal_code']); continue
        r.update(slug=slug, name=x['name'], status='active', estate=est, planning_area=town_pa(est), region=areas.ESTATES[est]['region'],
                 lat=geo[0], lng=geo[1], geo_source='onemap', blocks=blocks,
                 google_rating={'rating': g.get('rating'), 'count': g.get('userRatingCount'), 'checked': day, 'source': 'Google Places', 'source_date': day})
        jw('%s/workshops/%s.json' % (D, slug), r)
        gc = jl('%s/google_cache/%s.json' % (D, slug)); gc['review_themes'] = x['themes']; jw('%s/google_cache/%s.json' % (D, slug), gc)
        n = x['name']
        jw('%s/pilot/%s.json' % (D, slug), {
            'lede': '%s is a car repair workshop at %s. Its Google Maps listing shows opening hours and customer ratings.' % (n, r['address']['street']),
            'chips': ['Car repair'], 'services': ['General servicing and repair'], 'themes': x['themes'],
            'faqs': [['What does %s do?' % n, 'Google Maps lists it as a car repair workshop.'],
                     ['What are the opening hours?', 'The hours are listed in the Google Maps section above. Please see Google Maps for current hours.']],
            'sources': 'its Google Maps listing', 'stories': [], 'mentioned_services': x['mentioned']})
        v2 = jl(os.path.join(CARD_SOURCES, slug + '.json'))
        if v2 and bad_sources(v2, g): sys.exit('source log for %s uses a source outside the rules: %s' % (slug, bad_sources(v2, g)))
        if v2 and v2.get('pilot'):   # card rules v2 (Edwin 5 Nov 2026): own-website facts merged in; the log itself stays private
            pl = jl('%s/pilot/%s.json' % (D, slug)); pl.update({k: v for k, v in v2['pilot'].items() if k in V2_KEYS}); pl['card_rules'] = '2026-11-05'
            pl['themes'] = positive_only.clean(pl.get('themes'))
            jw('%s/pilot/%s.json' % (D, slug), pl)
        F = lambda k, v: {'field': k, 'value': v, 'source_url': 'google_places', 'retrieved': day}
        jw('%s/facts/%s.json' % (D, slug), {'slug': slug, 'researched_at': day,
            'researcher': 'Claude, Google Places Details only (candidate from Google Places Text Search sweep at Edwin\'s request; name from Google Business Profile)',
            'facts': [F('displayName', (g.get('displayName') or {}).get('text')), F('rating', str(g.get('rating'))), F('userRatingCount', str(g.get('userRatingCount'))),
                      F('websiteUri', str(g.get('websiteUri'))), F('types', str(g.get('types'))), F('primaryType', g.get('primaryType')),
                      F('opening_hours', (g.get('regularOpeningHours') or {}).get('weekdayDescriptions'))]})
        done.append(slug)
    jw(D + '/registry.json', reg)
    print(json.dumps({'active': done, 'skipped_need_estate_or_themes': skip}, indent=1))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=['prep', 'apply']); ap.add_argument('--raw-dir', default='/tmp/claude-0/s/raw')
    a = ap.parse_args(); {'prep': prep, 'apply': apply}[a.cmd](a)
