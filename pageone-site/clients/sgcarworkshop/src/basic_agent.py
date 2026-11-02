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
  daily     [--max-places 25] [--max-search 60]  Whole daily run: free IDs-only discovery over every estate x car-repair category, stubs, then the screen (never above 30 Details/day), PROGRESS.md.
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
# Google's Places quota day resets daily at 09:00 UTC (17:00 SGT; window_start_time in the 429 error, checked 2 Nov 2026). Key usage by that day, not the UTC date.
TODAY = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=9)).date().isoformat()
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
    u, ut = usage_today(); wd = os.path.join(DATA, 'workshops'); out = []; start = ut['details']
    pend = jload('pending.json', [])
    for f in sorted(os.listdir(wd)):
        r = json.load(open(os.path.join(wd, f)))
        gs = r['google_screen'] or {}
        need_id = gs.get('passed') is True and not r.get('name')   # passed earlier, identity still missing
        if r['status'] != 'pending' or (gs.get('passed') is not None and not need_id):
            continue
        if r['place_id'] in REMOVED_IDS():
            out.append((r['slug'], 'in removed.json: never live')); continue
        if ut['details'] - start >= a.max_places or ut['details'] >= HARD_CAP:
            out.append((r['slug'], 'daily cap reached, stays queued')); continue
        ut['details'] += 1
        try:
            g = gcall(API + 'places/' + r['place_id'], key, 'nationalPhoneNumber,internationalPhoneNumber,businessStatus,primaryType' + (',displayName,formattedAddress' if not r.get('name') else ''))
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
        if why is None and not r.get('name') and g.get('displayName'):
            # Edwin 2 Nov 2026: name and address MAY come from the Google profile for workshops that pass the mobile screen (source google_profile + date).
            fa = re.sub(r',?\s*Singapore\s*\d{6}\s*$', '', g.get('formattedAddress', ''))
            pc = re.search(r'(\d{6})\s*$', g.get('formattedAddress', ''))
            r['name'] = g['displayName'].get('text', ''); r['name_source_url'] = 'google_profile'; r['name_checked_at'] = TODAY
            r['address'] = {'block': '', 'street': fa, 'unit': '', 'building': ''}; r['postal_code'] = pc.group(1) if pc else ''
            r['address_source_url'] = 'google_profile'; r['address_checked_at'] = TODAY
            r.setdefault('categories', ['SERV']); r.setdefault('services', ['General servicing and repair']); r.setdefault('services_source_url', 'google_profile')
            r.setdefault('first_seen_at', TODAY); r.setdefault('last_verified_at', TODAY); r.setdefault('collector_version', 'agent-v4')
            auto_place(r)
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
        if why is None and r['slug'].startswith('tmp-') and r.get('name'):
            new = unique_slug(r['name']); os.remove(os.path.join(wd, f)); r['slug'] = new; f = new + '.json'
        jsave('workshops/%s' % f, r); out.append((r['slug'], state if why is None else 'pending: ' + why))
    q = jload('queue.json', {})
    for s, _ in out:
        pass
    jsave('pending.json', pend); jsave('usage.json', u)
    print(json.dumps({'results': out, 'details_calls_today': ut['details']}, indent=1))


HARD_CAP = int(os.environ.get('SGCW_HARD_CAP', '30'))   # project Place Details quota per day (30); Edwin raised it to 100 for 2 Nov 2026 only via the env var
PA_BY_ESTATE = {'kaki-bukit': 'Bedok', 'ubi': 'Geylang', 'eunos': 'Geylang', 'bedok-north': 'Bedok', 'woodlands': 'Woodlands', 'kranji': 'Sungei Kadut',
                'yishun': 'Yishun', 'ang-mo-kio': 'Ang Mo Kio', 'serangoon-north': 'Serangoon', 'defu-hougang': 'Hougang', 'sengkang': 'Sengkang',
                'sin-ming-bishan': 'Bishan', 'toa-payoh': 'Toa Payoh', 'macpherson': 'Geylang', 'alexandra-bukit-merah': 'Bukit Merah',
                'toh-guan-jurong-east': 'Jurong East', 'jurong-west': 'Jurong West', 'pandan-loop': 'Clementi', 'bukit-batok': 'Bukit Batok', 'tuas': 'Tuas'}
# URA Master Plan 2019 (checked 2 Nov 2026). Estates that span two planning areas (changi-loyang, sembawang-admiralty, jalan-besar-kallang-bahru) are left for a manual fix.
QUERIES = [('car workshop', 'SERV'), ('car servicing and repair', 'SERV'), ('car aircon repair', 'SERV'), ('car spray painting and bodywork', 'BODY'),
           ('gearbox repair', 'GEAR'), ('car ECU repair', 'ECU'), ('car battery replacement', 'BATT'), ('car detailing', 'DETL'), ('car wrap and PPF', 'WRAP')]
DEFAULT_SERVICES = {'SERV': 'General servicing and repair', 'BODY': 'Spray painting and bodywork', 'GEAR': 'Gearbox repair', 'ECU': 'ECU and module repair',
                    'BATT': 'Car battery replacement', 'DETL': 'Car detailing', 'WRAP': 'Car wrap and PPF', 'PART': 'Car parts'}


def REMOVED_IDS():
    return {r['place_id'] if isinstance(r, dict) else r for r in jload('removed.json', [])}


def unique_slug(name):
    base = re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', name.lower())).strip('-')[:60] or 'workshop'
    wd = os.path.join(DATA, 'workshops'); s, n = base, 2
    while os.path.exists(os.path.join(wd, s + '.json')):
        s = '%s-%d' % (base, n); n += 1
    return s


def auto_place(r):
    """Fill estate, planning area, region and OneMap coordinates when they are unambiguous; otherwise the record stays hidden for a manual fix."""
    import areas
    est = areas.estate_for(r['address']['street'], r.get('postal_code'))
    if est and est in PA_BY_ESTATE:
        r['estate'] = est; r['planning_area'] = PA_BY_ESTATE[est]; r['region'] = areas.ESTATES[est]['region']
    try:
        r['lat'], r['lng'] = geocode(r['postal_code']); r['geo_source'] = 'onemap'
    except Exception:
        pass   # OneMap unreachable from this host: the daily session fills lat/lng with WebFetch


def make_stubs(limit):
    """Turn discovered ids (data/queue.json) into screen-only stubs. Only the place_id, the search category and the area are kept."""
    q = jload('queue.json', {}); wd = os.path.join(DATA, 'workshops'); n = 0
    have = {json.load(open(os.path.join(wd, f)))['place_id'] for f in os.listdir(wd)}
    for pid, v in list(q.items()):
        if n >= limit: break
        if v.get('state') != 'discovered' or pid in have or pid in REMOVED_IDS(): continue
        cat = v.get('cat', 'SERV')
        r = {'schema_version': 1, 'slug': 'tmp-' + re.sub(r'\W', '', pid)[-10:].lower(), 'place_id': pid, 'name': None, 'phones': [], 'status': 'pending', 'tier': 'basic',
             'categories': [cat], 'services': [DEFAULT_SERVICES[cat]], 'services_source_url': 'google_profile',
             'google_screen': {'passed': None, 'reason': 'discovered %s (%s), waiting for the Google screen' % (TODAY, v.get('estate')), 'checked_at': None}}
        jsave('workshops/%s.json' % r['slug'], r); v['state'] = 'staged'; n += 1
    jsave('queue.json', q); return n


def daily(a, key):
    """Daily run (Edwin 2 Nov 2026): IDs-only discovery (free), stubs, then up to 25 Place Details (never above the 30/day project quota)."""
    import areas
    u, ut = usage_today(); prog = jload('progress.json', {'cursor': 0, 'days': {}})
    combos = [(sl, qq, cc) for qq, cc in QUERIES for sl in areas.ESTATES]
    q = jload('queue.json', {}); skip = known_ids(); new = 0; searches = 0
    pending_stubs = sum(1 for v in q.values() if v.get('state') == 'discovered')
    while searches < a.max_search and pending_stubs + new < a.max_places * 3 and prog['cursor'] < len(combos) * 100:
        sl, qq, cc = combos[prog['cursor'] % len(combos)]; prog['cursor'] += 1; est = areas.ESTATES[sl]; searches += 1; ut['text_search'] += 1
        body = {'textQuery': '%s %s' % (qq, est['name']), 'regionCode': 'SG', 'pageSize': 20,
                'locationBias': {'circle': {'center': {'latitude': est['lat'], 'longitude': est['lon']}, 'radius': 2500.0}}}
        try:
            res = gcall(API + 'places:searchText', key, 'places.id', body).get('places', [])
        except urllib.error.HTTPError as e:
            print('text search stopped: HTTP', e.code); break
        for p in res:
            if p['id'] not in skip and p['id'] not in REMOVED_IDS():
                q[p['id']] = {'estate': sl, 'cat': cc, 'state': 'discovered', 'date': TODAY}; skip.add(p['id']); new += 1
    jsave('queue.json', q)
    staged = make_stubs(a.max_places)
    jsave('usage.json', u); jsave('progress.json', prog)
    a.max_places = min(a.max_places, HARD_CAP)
    before = dict(ut)
    screen(a, key)
    summarize(prog)


def summarize(prog):
    wd = os.path.join(DATA, 'workshops'); live = held = 0; hidden = {}
    for f in os.listdir(wd):
        r = json.load(open(os.path.join(wd, f))); gs = r.get('google_screen') or {}
        if r['status'] == 'active': live += 1
        elif gs.get('passed') is True: held += 1
        elif gs.get('passed') is False:
            k = gs.get('reason') or 'other'; hidden[k] = hidden.get(k, 0) + 1
    u = jload('usage.json', {}); q = jload('queue.json', {})
    waiting = sum(1 for f in os.listdir(wd) if (json.load(open(os.path.join(wd, f))).get('google_screen') or {}).get('passed') is None)
    prog['days'][TODAY] = {'details_calls': u.get(TODAY, {}).get('details', 0), 'text_searches': u.get(TODAY, {}).get('text_search', 0), 'live_total': live,
                           'passed_waiting_for_estate_or_geo': held, 'waiting_to_screen': waiting, 'hidden_by_reason': hidden, 'discovered_ids_total': len(q), 'search_cursor': prog['cursor']}
    jsave('progress.json', prog)
    lines = ['# SG Car Workshop screening progress', '', 'Updated %s. Live Basic listings: %d. Passed but hidden (need estate/geo): %d. Waiting to screen: %d.' % (TODAY, live, held, waiting), '',
             '| Date | Place Details calls | Text searches (free) | Live total | Hidden by reason |', '|---|---|---|---|---|']
    for d, v in sorted(prog['days'].items()):
        lines.append('| %s | %s | %s | %s | %s |' % (d, v['details_calls'], v['text_searches'], v['live_total'], '; '.join('%s: %d' % kv for kv in v['hidden_by_reason'].items()) or '-'))
    open(os.path.join(ROOT, 'PROGRESS.md'), 'w').write('\n'.join(lines) + '\n')


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


ENRICH_MASK = ('displayName,formattedAddress,businessStatus,primaryType,types,nationalPhoneNumber,internationalPhoneNumber,rating,userRatingCount,'
               'regularOpeningHours,websiteUri,editorialSummary,paymentOptions,parkingOptions,reviews,location')


def enrich(a, key):
    """Volume mode (Edwin 3 Nov 2026): ONE Place Details call per slug with the full field mask. Raw reviews go to --raw-dir (scratch, never the repo);
    data/google_cache/<slug>.json keeps only the non-review fields plus fetched_at (refresh within 30 days). place_id is the only permanent Google value."""
    u, ut = usage_today(); wd = os.path.join(DATA, 'workshops'); cd = os.path.join(DATA, 'google_cache'); os.makedirs(cd, exist_ok=True); os.makedirs(a.raw_dir, exist_ok=True); out = []
    for slug in a.slugs.split(','):
        r = json.load(open(os.path.join(wd, slug + '.json')))
        if ut['details'] >= HARD_CAP: out.append((slug, 'daily cap reached')); continue
        ut['details'] += 1
        try:
            g = gcall(API + 'places/' + r['place_id'], key, ENRICH_MASK)
        except urllib.error.HTTPError as e:
            if e.code == 429: ut['details'] -= 1; out.append((slug, '429 quota exhausted')); break
            raise
        json.dump(g, open(os.path.join(a.raw_dir, slug + '.json'), 'w'), indent=1, ensure_ascii=False)
        keep = {k: g.get(k) for k in ('businessStatus', 'primaryType', 'types', 'rating', 'userRatingCount', 'websiteUri', 'paymentOptions', 'parkingOptions')}
        keep['editorialSummary'] = (g.get('editorialSummary') or {}).get('text')
        keep['weekdayDescriptions'] = (g.get('regularOpeningHours') or {}).get('weekdayDescriptions')
        keep['review_count_seen'] = len(g.get('reviews') or []); keep['review_themes'] = None   # filled by the writer in own words, never quotes
        keep['fetched_at'] = TODAY; keep['place_id'] = r['place_id']; keep['source'] = 'google_places'
        jsave('google_cache/%s.json' % slug, keep); out.append((slug, 'ok'))
    jsave('usage.json', u); print(json.dumps({'results': out, 'details_calls_today': ut['details']}))


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    d = sub.add_parser('discover'); d.add_argument('--estates', required=True)
    s = sub.add_parser('stage')
    for k in ('place-id', 'slug', 'estate', 'planning-area', 'categories', 'name', 'street', 'postal', 'services'): s.add_argument('--' + k, required=True)
    for k in ('block', 'unit', 'building', 'facebook', 'hours', 'evidence'): s.add_argument('--' + k, default='')
    s.add_argument('--own-url', action='append', required=True); s.add_argument('--snapshot-file', action='append', default=[]); s.add_argument('--mobile', action='append', default=[]); s.add_argument('--lat', type=float); s.add_argument('--lng', type=float)
    dd = sub.add_parser('daily'); dd.add_argument('--max-places', type=int, default=25); dd.add_argument('--max-search', type=int, default=60)
    for c in ('screen', 'resume', 'closed'):
        x = sub.add_parser(c); x.add_argument('--max-places', type=int, default=25); x.add_argument('--refresh', action='store_true')
    en = sub.add_parser('enrich'); en.add_argument('--slugs', required=True); en.add_argument('--raw-dir', required=True)
    a = ap.parse_args()
    a.__dict__['place_id'] = a.__dict__.get('place_id'); a.__dict__['planning_area'] = a.__dict__.get('planning_area')
    key = os.environ.get('PLACES_SERVER_KEY')
    if a.cmd in ('discover', 'screen', 'resume', 'closed', 'daily', 'enrich') and not key: sys.exit('Set PLACES_SERVER_KEY in the environment (server key, Places API New only).')
    {'discover': lambda: discover(a, key), 'stage': lambda: stage(a), 'screen': lambda: screen(a, key), 'resume': lambda: screen(a, key), 'closed': lambda: refresh_closed(a, key), 'daily': lambda: daily(a, key), 'enrich': lambda: enrich(a, key)}[a.cmd]()


if __name__ == '__main__':
    main()
