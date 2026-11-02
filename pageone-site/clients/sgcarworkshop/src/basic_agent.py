#!/usr/bin/env python3
"""Basic-listing agent v3 (Google Places API New + the workshop's OWN pages).  Static site, no messaging feature (PDPA s48B).

RULES (Edwin, 2 Nov 2026)
  * The only Google value stored is place_id (+ a pass/fail screen result and date). Never rating, reviews, photos, phone, hours, status, name, address, types, website, maps URL, cid.
  * Mobile-only: a workshop is listed only if it has an SG mobile (+65 8/9 + 7 digits).
  * Option B (Edwin 2 Nov 2026): the SG mobile on the Google Business Profile qualifies and is stored once (source google_profile + checked_at); landline-only or no phone = skip. (Older Option A note follows.) Google is ONLY the filter. The stored mobile must come from the workshop's own website / Facebook / WhatsApp Business page and MATCH the Google
    mobile (compared in memory, never saved). Mobile only on Google -> data/pending.json, never live.
  * Private snapshots of the own pages used are kept in snapshots/<slug>/ (gitignored).

COMMANDS  (PLACES_SERVER_KEY in the environment; never written anywhere)
  discover  --estates kaki-bukit,ubi          Text Search, field mask places.id ONLY (free). Adds ids to data/queue.json (skips known, removed, pending, existing).
  stage     --place-id ID --slug S --estate E --planning-area "Jurong East" --categories SERV,GEAR --name N --block 48 --street "Toh Guan Road East"
            --unit "#02-140" --building "Enterprise Hub" --postal 608586 --services "a;b;c" --own-url URL [--own-url URL2] [--facebook URL] [--hours "text"]
            Fetches the own page(s), saves the snapshot, checks the name and postal code appear on it, finds the mobile(s) on it, geocodes the postal code with OneMap,
            and writes data/workshops/<slug>.json as status "pending" (google_screen.passed null). NO Google call.
  screen    [--max-places 25]                 For every staged record: ONE Place Details call (nationalPhoneNumber,internationalPhoneNumber,businessStatus,primaryType).
            Pass = OPERATIONAL + car-repair primaryType + SG mobile on Google that equals the stored own-source mobile -> status "active". Otherwise the record
            stays pending with passed false and the reason (no Google data kept) and the place_id goes to data/pending.json.
  resume                                      same as screen: picks up the queue where the daily cap stopped it.
  closed    --refresh                         (monthly) re-screen live records; CLOSED_PERMANENTLY -> status "closed" (hidden at next build), flagged in the report.
Daily cap: --max-places (default 25) Details calls per UTC day, tracked in data/usage.json; HTTP 429 stops the run cleanly and the rest stays queued.
After any run: python3 build.py && python3 check.py, commit, sync.
"""
import argparse, datetime as dt, json, os, re, sys, urllib.parse, urllib.request, urllib.error

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DATA = os.environ.get('SGCW_DATA_DIR') or os.path.join(ROOT, 'data')
SNAP = os.path.join(ROOT, 'snapshots')
API = 'https://places.googleapis.com/v1/'
OK_PRIMARY = {'car_repair', 'car_repair_service', 'auto_repair_shop', 'auto_body_shop', 'auto_electrician', 'mechanic'}
TODAY = dt.date.today().isoformat()
MOBILE = re.compile(r'(?<!\d)(?:\+?65[\s-]?)?([89]\d{3}[\s-]?\d{4})(?!\d)')
WAME = re.compile(r'wa\.me/65([89]\d{7})')
UA = {'User-Agent': 'Mozilla/5.0 (compatible; SGCarWorkshopDirectory/3; +https://sgcarworkshop.sg/)'}


def jload(n, default):
    p = os.path.join(DATA, n)
    return json.load(open(p)) if os.path.exists(p) else default


def jsave(n, obj):
    json.dump(obj, open(os.path.join(DATA, n), 'w'), indent=1, ensure_ascii=False)


def usage_today():
    u = jload('usage.json', {})
    return u, u.setdefault(TODAY, {'text_search': 0, 'details': 0})


def gcall(url, key, mask, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, method='POST' if body else 'GET',
                                 headers={'X-Goog-Api-Key': key, 'X-Goog-FieldMask': mask, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def known_ids():
    ids = set(jload('queue.json', {})) | {r['place_id'] for r in jload('pending.json', [])}
    ids |= {r['place_id'] if isinstance(r, dict) else r for r in jload('removed.json', [])}
    wd = os.path.join(DATA, 'workshops')
    for f in os.listdir(wd) if os.path.isdir(wd) else []:
        ids.add(json.load(open(os.path.join(wd, f)))['place_id'])
    return ids


def discover(a, key):
    import areas
    q = jload('queue.json', {}); u, ut = usage_today(); skip = known_ids(); new = 0
    for sl in a.estates.split(','):
        est = areas.ESTATES[sl]
        body = {'textQuery': 'car workshop ' + est['name'], 'regionCode': 'SG', 'pageSize': 20,
                'locationBias': {'circle': {'center': {'latitude': est['lat'], 'longitude': est['lon']}, 'radius': 2500.0}}}
        ut['text_search'] += 1
        for p in gcall(API + 'places:searchText', key, 'places.id', body).get('places', []):
            if p['id'] not in skip:
                q[p['id']] = {'estate': sl, 'state': 'discovered', 'date': TODAY}; skip.add(p['id']); new += 1
    jsave('queue.json', q); jsave('usage.json', u)
    print(json.dumps({'new_ids': new, 'text_search_calls_today': ut['text_search']}))


def fetch(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read().decode('utf-8', 'replace')


def geocode(postal):
    j = json.load(urllib.request.urlopen('https://www.onemap.gov.sg/api/common/elastic/search?searchVal=%s&returnGeom=Y&getAddrDetails=Y&pageNum=1' % postal, timeout=30))
    r = j['results'][0]
    return round(float(r['LATITUDE']), 7), round(float(r['LONGITUDE']), 7)


def stage(a):
    import areas
    os.makedirs(os.path.join(SNAP, a.slug), exist_ok=True)
    texts, mobiles = [], {}
    for n, u in enumerate(a.own_url):
        if a.snapshot_file:   # page text saved by the operator when this host cannot fetch the site directly
            h = open(a.snapshot_file[min(n, len(a.snapshot_file) - 1)], encoding='utf-8').read()
        else:
            h = fetch(u)
        open(os.path.join(SNAP, a.slug, 'page%d.html' % n), 'w', encoding='utf-8').write(h)
        t = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h)); texts.append(t)
        for m in WAME.findall(h) + [re.sub(r'\D', '', x) for x in MOBILE.findall(h)]:
            mobiles.setdefault('+65' + m[-8:], u)
    if a.mobile:
        mobiles = {}   # explicit --mobile means: only the number(s) named for THIS unit, not every number on a multi-branch page
    for m in a.mobile:   # explicit mobile read from the own page (must still appear in the snapshot text)
        if re.sub(r'\D', '', m)[-8:] not in re.sub(r'\D', ' ', ' '.join(texts)).replace(' ', '') and re.sub(r'\D', '', m)[-8:] not in re.sub(r'\D', '', ' '.join(texts)):
            sys.exit('stage refused: mobile %s is not in the saved page text' % m)
        mobiles.setdefault(m, a.own_url[0])
    blob = ' '.join(texts).lower()
    problems = []
    if a.name.lower() not in blob: problems.append('name not found on the own page')
    if a.postal not in blob.replace(' ', '') and a.postal not in blob: problems.append('postal code not found on the own page')
    if not mobiles: problems.append('no SG mobile on the own page')
    if problems: sys.exit('stage refused: ' + '; '.join(problems))
    try: lat, lng = geocode(a.postal)
    except Exception as e: sys.exit('OneMap geocode failed (%s); pass --lat/--lng from OneMap' % e) if a.lat is None else None
    if a.lat is not None: lat, lng = a.lat, a.lng
    est = areas.ESTATES[a.estate]
    ph = [{'e164': k, 'kind': 'mobile', 'whatsapp': True, 'evidence': a.evidence or "Own page lists this mobile (snapshot %s)" % a.slug, 'source_url': u, 'checked_at': TODAY} for k, u in mobiles.items()]
    rec = {'schema_version': 1, 'slug': a.slug, 'place_id': a.place_id, 'place_id_checked_at': TODAY, 'name': a.name, 'name_source_url': a.own_url[0],
           'address': {'block': a.block, 'street': a.street, 'unit': a.unit, 'building': a.building}, 'postal_code': a.postal, 'address_source_url': a.own_url[0],
           'lat': lat, 'lng': lng, 'geo_source': 'onemap', 'planning_area': a.planning_area, 'region': est['region'], 'estate': a.estate,
           'categories': a.categories.split(','), 'services': [s.strip() for s in a.services.split(';') if s.strip()], 'services_source_url': a.own_url[0],
           'phones': ph, 'website_url': a.own_url[0], 'google_screen': {'passed': None, 'reason': 'staged, waiting for the Google screen', 'checked_at': None},
           'status': 'pending', 'tier': 'basic', 'first_seen_at': TODAY, 'last_verified_at': TODAY, 'collector_version': 'agent-v3'}
    if a.facebook: rec['facebook_url'] = a.facebook
    if a.hours: rec['hours'] = {'text': a.hours}; rec['hours_source_url'] = a.own_url[0]
    jsave('workshops/%s.json' % a.slug, rec)
    q = jload('queue.json', {}); q[a.place_id] = {'estate': a.estate, 'state': 'staged', 'slug': a.slug, 'date': TODAY}; jsave('queue.json', q)
    print('staged', a.slug, 'mobiles', list(mobiles))


def screen(a, key):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    global DATA_MOD
    import data as DATA_MOD
    u, ut = usage_today(); wd = os.path.join(DATA, 'workshops'); out = []
    pend = jload('pending.json', [])
    for f in sorted(os.listdir(wd)):
        r = json.load(open(os.path.join(wd, f)))
        if r['status'] != 'pending' or (r['google_screen'] or {}).get('passed') is not None:
            continue
        if ut['details'] >= a.max_places:
            out.append((r['slug'], 'daily cap reached, stays queued')); continue
        ut['details'] += 1
        try:
            g = gcall(API + 'places/' + r['place_id'], key, 'nationalPhoneNumber,internationalPhoneNumber,businessStatus,primaryType')
        except urllib.error.HTTPError as e:
            if e.code == 429:
                out.append((r['slug'], 'Google quota exhausted (429): stays queued')); ut['details'] -= 1; break
            raise
        gm = re.sub(r'\D', '', g.get('internationalPhoneNumber', ''))
        gm = '+' + gm if gm else ''
        why = None; state = None
        if g.get('businessStatus') != 'OPERATIONAL': why = 'not OPERATIONAL'
        elif g.get('primaryType') not in OK_PRIMARY: why = 'primaryType is not car repair'
        elif not re.match(r'^\+65[89]\d{7}$', gm): why = 'Google profile has no SG mobile (landline only or no phone)'
        # Option B (Edwin, 2 Nov 2026): the SG mobile on the Google Business Profile qualifies; stored ONCE, source google_profile.
        r['google_screen'] = {'passed': why is None, 'reason': why or 'OPERATIONAL, car repair, SG mobile on Google profile', 'checked_at': TODAY}
        r['place_id_checked_at'] = TODAY
        if why is None:
            r['phones'] = [p for p in r.get('phones', []) if p['e164'] != gm] + [{'e164': gm, 'kind': 'mobile', 'whatsapp': True, 'source': 'google_profile', 'checked_at': TODAY}]
            r['status'] = 'active'
            need = DATA_MOD.record_problems(r)
            if need:   # passed the screen but the own-source name/address/services are not filled yet: stays hidden
                r['status'] = 'pending'; state = 'passed, hidden, needs: ' + '; '.join(need[:4])
            else:
                state = 'active'
        else:
            pend.append({'place_id': r['place_id'], 'slug': r['slug'], 'reason': why, 'date': TODAY})
        jsave('workshops/%s' % f, r); out.append((r['slug'], state if why is None else 'pending: ' + why))
    q = jload('queue.json', {})
    for s, _ in out:
        pass
    jsave('pending.json', pend); jsave('usage.json', u)
    print(json.dumps({'results': out, 'details_calls_today': ut['details']}, indent=1))


def refresh_closed(a, key):
    """Monthly: live records whose Google businessStatus is CLOSED_PERMANENTLY become status closed (hidden at the next build)."""
    u, ut = usage_today(); wd = os.path.join(DATA, 'workshops'); flagged = []
    for f in sorted(os.listdir(wd)):
        r = json.load(open(os.path.join(wd, f)))
        if r['status'] != 'active' or ut['details'] >= a.max_places: continue
        ut['details'] += 1
        if gcall(API + 'places/' + r['place_id'], key, 'businessStatus').get('businessStatus') == 'CLOSED_PERMANENTLY':
            r['status'] = 'closed'; r['last_verified_at'] = TODAY; jsave('workshops/%s' % f, r); flagged.append(r['slug'])
    jsave('usage.json', u); print(json.dumps({'closed': flagged, 'details_calls_today': ut['details']}))


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    d = sub.add_parser('discover'); d.add_argument('--estates', required=True)
    s = sub.add_parser('stage')
    for k in ('place-id', 'slug', 'estate', 'planning-area', 'categories', 'name', 'street', 'postal', 'services'): s.add_argument('--' + k, required=True)
    for k in ('block', 'unit', 'building', 'facebook', 'hours', 'evidence'): s.add_argument('--' + k, default='')
    s.add_argument('--own-url', action='append', required=True); s.add_argument('--snapshot-file', action='append', default=[]); s.add_argument('--mobile', action='append', default=[]); s.add_argument('--lat', type=float); s.add_argument('--lng', type=float)
    for c in ('screen', 'resume', 'closed'):
        x = sub.add_parser(c); x.add_argument('--max-places', type=int, default=25); x.add_argument('--refresh', action='store_true')
    a = ap.parse_args()
    a.__dict__['place_id'] = a.__dict__.get('place_id'); a.__dict__['planning_area'] = a.__dict__.get('planning_area')
    key = os.environ.get('PLACES_SERVER_KEY')
    if a.cmd in ('discover', 'screen', 'resume', 'closed') and not key: sys.exit('Set PLACES_SERVER_KEY in the environment (server key, Places API New only).')
    {'discover': lambda: discover(a, key), 'stage': lambda: stage(a), 'screen': lambda: screen(a, key), 'resume': lambda: screen(a, key), 'closed': lambda: refresh_closed(a, key)}[a.cmd]()


if __name__ == '__main__':
    main()
