#!/usr/bin/env python3
"""Basic-listing agent (Google Places API New). Cheapest path: ONE Text Search per estate, no Place Details calls at all.

  PLACES_SERVER_KEY=... python3 basic_agent.py --estates kaki-bukit [--cap 20] [--dry-run]

Per estate: one Text Search ("car workshop <estate>"), up to 20 results, field mask
  places.id, displayName, formattedAddress, location, businessStatus, types, primaryType.
Keeps a result only if: not already listed (hand-made entries or basic_auto.json), businessStatus == OPERATIONAL, a car-repair type, not a dealer/car wash/etc.,
and its address maps to a known estate (postal code / address keywords, areas.py). Stops at --cap new listings.
Stored in basic_auto.json: place_id (permanent) + name + address + our own slug and estate. NOT stored: phone, opening hours, rating, review count,
website, photos. dir.js loads those live in the browser from Places (browser key, referrer-restricted).
The key is read from the environment only; it must never be written to the repo, built site or client JS.
Then: python3 build.py && python3 check.py, commit, sync. Monthly: re-run to find new workshops; --refresh re-checks stored names/addresses/status.
"""
import argparse, datetime as dt, json, os, re, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
STORE = os.path.join(HERE, 'basic_auto.json')
API = 'https://places.googleapis.com/v1/'
MASK = 'places.id,places.displayName,places.formattedAddress,places.location,places.businessStatus,places.types,places.primaryType'
OK_TYPES = {'car_repair', 'auto_parts_store', 'car_repair_service'}
SKIP = re.compile(r'\b(showroom|dealer|leasing|rental|rent a car|parking|car ?wash|insurance|driving|petrol|shell|esso|caltex|spc|sembcorp|tyre|tire|autobay)\b', re.I)
CALLS = {'text_search': 0}


def search(est, key):
    body = {'textQuery': 'car workshop ' + est['name'], 'regionCode': 'SG', 'pageSize': 20,
            'locationBias': {'circle': {'center': {'latitude': est['lat'], 'longitude': est['lon']}, 'radius': 2500.0}}}
    req = urllib.request.Request(API + 'places:searchText', data=json.dumps(body).encode(), method='POST',
                                 headers={'X-Goog-Api-Key': key, 'X-Goog-FieldMask': MASK, 'Content-Type': 'application/json'})
    CALLS['text_search'] += 1
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get('places', [])


def slugify(n):
    s = re.sub(r'[^a-z0-9]+', '-', re.sub(r'\b(pte\.?|ltd\.?)\b', '', n.lower())).strip('-')
    return s if len(s) <= 36 else s[:36].rsplit('-', 1)[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--estates', required=True); ap.add_argument('--cap', type=int, default=20); ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    key = os.environ.get('PLACES_SERVER_KEY')
    if not key and not a.dry_run:
        sys.exit('Set PLACES_SERVER_KEY in the environment (server key, Places API New only).')
    import areas, data
    store = json.load(open(STORE)) if os.path.exists(STORE) else {}
    have_ids = {e['place_id'] for e in data.ENTRIES if e.get('place_id')} | set(store)
    slugs = {e['slug'] for e in data.ENTRIES} | {v['slug'] for v in store.values()}
    added, skipped = [], []
    for sl in a.estates.split(','):
        est = areas.ESTATES[sl]
        if a.dry_run:
            print('would search: car workshop', est['name']); continue
        for p in search(est, key):
            if len(added) >= a.cap:
                break
            pid, name, addr = p['id'], p.get('displayName', {}).get('text', ''), p.get('formattedAddress', '')
            why = None
            m = re.search(r'Singapore\s+(\d{6})', addr)
            street = re.sub(r',?\s*Singapore\s+\d{6}\s*$', '', addr)
            es = areas.estate_for(street, m.group(1) if m else '')
            if pid in have_ids: why = 'already listed'
            elif p.get('businessStatus') != 'OPERATIONAL': why = 'not operational'
            elif not (set(p.get('types', [])) & OK_TYPES or p.get('primaryType') in OK_TYPES): why = 'not a car repair type'
            elif SKIP.search(name): why = 'excluded name'
            elif not es: why = 'no estate for address'
            if why:
                skipped.append((name, why)); continue
            s = slugify(name); n = 2
            while s in slugs: s = '%s-%d' % (slugify(name), n); n += 1
            slugs.add(s)
            store[pid] = dict(place_id=pid, name=name, address=addr, slug=s, estate=es, fetched_at=dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'))
            added.append((s, es, name))
    if not a.dry_run:
        json.dump(store, open(STORE, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps(dict(added=added, skipped=skipped, places_calls=CALLS), indent=1, ensure_ascii=False))


if __name__ == '__main__':
    main()
