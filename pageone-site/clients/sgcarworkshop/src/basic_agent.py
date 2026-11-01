#!/usr/bin/env python3
"""Basic-listing agent (Google Places API New). Cheapest path, run monthly.

  GOOGLE_PLACES_SERVER_KEY=... python3 basic_agent.py [--estates kaki-bukit,ubi] [--refresh] [--dry-run]

1. Per estate: ONE Text Search ("car workshop <estate>"), field mask places.id,places.displayName,places.formattedAddress,places.location (IDs/basic tier), up to 20 results.
2. Skip IDs already listed (hand-made BASIC entries in data.py, or already in basic_auto.json) and anything not OPERATIONAL.
   (businessStatus is NOT in the cheap mask, so it is requested in the details call and non-operational places are dropped there.)
3. ONE Place Details per NEW id, mask limited to: displayName, formattedAddress, nationalPhoneNumber, websiteUri, regularOpeningHours, rating,
   userRatingCount, googleMapsUri, photos (first photo name only is used; photos themselves are never stored) + businessStatus.
4. Stores place_id permanently. Every other field carries fetched_at and is dropped from the build after 30 days; --refresh re-fetches records older than 25 days.
5. Estate comes from address + postal code at build time (areas.assign), so nothing here guesses it.
6. Writes basic_auto.json; data.py turns each record into a Basic listing in the existing format. Then: python3 build.py && python3 check.py, commit, sync.
Quota guard: hard cap of MAX_DETAILS new details calls per run.
"""
import argparse, datetime as dt, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(HERE, 'basic_auto.json')
API = 'https://places.googleapis.com/v1/'
MAX_DETAILS = 40
FRESH_DAYS, REFRESH_DAYS = 30, 25
SEARCH_MASK = 'places.id,places.displayName,places.formattedAddress,places.location'
DETAIL_MASK = ('id,displayName,formattedAddress,nationalPhoneNumber,websiteUri,regularOpeningHours,rating,userRatingCount,googleMapsUri,photos,businessStatus')
# Names that are not general car workshops (dealers, car washes, parking, insurers...) are dropped before spending a details call.
SKIP = re.compile(r'\b(showroom|dealer|motors? pte|leasing|rental|rent a car|parking|car ?wash|insurance|driving|petrol|shell|esso|caltex|spc|sembcorp)\b', re.I)


def call(method, url, key, mask=None, body=None):
    h = {'X-Goog-Api-Key': key, 'Content-Type': 'application/json'}
    if mask:
        h['X-Goog-FieldMask'] = mask
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, headers=h, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def known_ids():
    ids = set()
    sys.path.insert(0, HERE)
    import data  # hand-made listings
    for e in data.ENTRIES:
        if e.get('place_id'):
            ids.add(e['place_id'])
    return ids


def load():
    return json.load(open(STORE)) if os.path.exists(STORE) else {}


def slugify(n):
    return re.sub(r'[^a-z0-9]+', '-', n.lower()).strip('-')


def search_estate(est, key):
    d = call('POST', API + 'places:searchText', key, SEARCH_MASK,
             {'textQuery': 'car workshop ' + est['name'], 'regionCode': 'SG', 'pageSize': 20, 'locationBias': {'circle': {'center': {'latitude': est['lat'], 'longitude': est['lon']}, 'radius': 2500.0}}})
    return d.get('places', [])


def details(pid, key):
    return call('GET', API + 'places/' + pid, key, DETAIL_MASK)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--estates'); ap.add_argument('--refresh', action='store_true'); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    key = os.environ.get('GOOGLE_PLACES_SERVER_KEY')
    if not key and not a.dry_run:
        sys.exit('Set GOOGLE_PLACES_SERVER_KEY (server key, no referrer restriction, Places API New only, IP-restricted if possible).')
    import areas
    store, have, now = load(), known_ids(), dt.datetime.utcnow()
    have |= set(store)
    want = [x for x in areas.ESTATES.values() if not a.estates or x['slug'] in a.estates.split(',')]
    new = []
    for est in want:
        if a.dry_run:
            print('would search: car workshop', est['name']); continue
        for p in search_estate(est, key):
            pid, name = p['id'], p.get('displayName', {}).get('text', '')
            if pid in have or SKIP.search(name) or any(pid == n[0] for n in new):
                continue
            new.append((pid, name))
    todo = new[:MAX_DETAILS]
    if a.refresh:
        todo += [(k, v['name']) for k, v in store.items() if (now - dt.datetime.fromisoformat(v['fetched_at'])).days >= REFRESH_DAYS]
    print('new:', len(new), 'details calls:', len(todo), '(cap %d)' % MAX_DETAILS)
    for pid, name in ([] if a.dry_run else todo):
        d = details(pid, key)
        if d.get('businessStatus') != 'OPERATIONAL':
            store.pop(pid, None); print('skip (not operational):', name); continue
        store[pid] = dict(place_id=pid, name=d['displayName']['text'], address=d.get('formattedAddress', ''), phone=d.get('nationalPhoneNumber', ''),
                          website=d.get('websiteUri', ''), hours=d.get('regularOpeningHours', {}).get('weekdayDescriptions', []), rating=d.get('rating'),
                          reviews=d.get('userRatingCount'), maps=d.get('googleMapsUri', ''), fetched_at=now.isoformat(timespec='seconds'))
    if not a.dry_run:
        json.dump(store, open(STORE, 'w'), indent=1, ensure_ascii=False)
        print('saved', len(store), 'records to', STORE)


if __name__ == '__main__':
    main()
