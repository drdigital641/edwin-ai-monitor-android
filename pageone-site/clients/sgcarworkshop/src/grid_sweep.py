#!/usr/bin/env python3
"""Sequential grid sweep for the candidate queue (Edwin 4 Nov 2026: "make all this sweeping efficient ... in a sequential way").

Why: town searches overlap and forget what they saw, so as the directory fills up each paid call finds fewer new shops.
How it works:
  * Singapore is split into fixed squares (~2.2 km). Each search is limited to its own square (locationRestriction), so squares never overlap.
  * Step 1 per square is an IDs-only Text Search (field mask places.id), which Google bills as Text Search Essentials IDs Only (no charge).
  * Only when that free search shows a place_id we have never seen do we pay for the full search (phone etc.) of that square.
  * A square that returns Google's 60-result maximum is split into 4 smaller squares, so dense estates are covered fully.
  * Every place_id seen is remembered with its outcome in data/seen_places.json (place_id is the only Google value we keep permanently),
    so landline-only shops and non-workshops are never paid for again.
  * data/sweep_grid.json logs each square: when swept, how many listings, how many new. A square is due again after --recheck-days (default 90).
  * Order: squares with the most listed workshops first (industrial estates), then the rest.

    PLACES_SERVER_KEY=... python3 grid_sweep.py run --max-paid 20 [--max-free 300] [--recheck-days 90]
    python3 grid_sweep.py status            # no Google calls: coverage and yield so far
Cards are still built only from data/candidate_queue.json via enrich-queue (Google is the source of truth)."""
import argparse, datetime as dt, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import basic_agent as B  # noqa: E402
import registry as R  # noqa: E402

S, N, W, E = 1.235, 1.475, 103.605, 104.045   # mainland + Jurong Island bounding box
STEP = 0.02                                   # ~2.2 km squares
QUERY = 'car workshop'
FULL_MASK = ('places.id,places.displayName,places.internationalPhoneNumber,places.primaryType,places.rating,'
             'places.userRatingCount,places.formattedAddress,places.businessStatus,nextPageToken')


def base_cells():
    out = {}
    i = 0; lat = S
    while lat < N:
        j = 0; lng = W
        while lng < E:
            out['r%02dc%02d' % (i, j)] = {'bbox': [round(lat, 4), round(lng, 4), round(min(lat + STEP, N), 4), round(min(lng + STEP, E), 4)]}
            j += 1; lng += STEP
        i += 1; lat += STEP
    return out


def load():
    g = B.jload('sweep_grid.json', None) or base_cells()
    return g, B.jload('seen_places.json', {})


def priority(g):
    pts = [(r['lat'], r['lng']) for r in (json.load(open(os.path.join(B.DATA, 'workshops', f)))
                                         for f in os.listdir(os.path.join(B.DATA, 'workshops'))) if r.get('lat')]
    def score(c):
        s, w, n, e = g[c]['bbox']
        return sum(1 for la, lo in pts if s <= la < n and w <= lo < e)
    return score


def due(cell, days):
    if cell.get('split'): return False
    sw = cell.get('swept')
    return not sw or (dt.date.today() - dt.date.fromisoformat(sw)).days >= days


def search(key, bbox, mask, tok=None):
    s, w, n, e = bbox
    body = {'textQuery': QUERY, 'regionCode': 'SG', 'pageSize': 20, 'includedType': 'car_repair', 'strictTypeFiltering': True,
            'locationRestriction': {'rectangle': {'low': {'latitude': s, 'longitude': w}, 'high': {'latitude': n, 'longitude': e}}}}
    if tok: body['pageToken'] = tok
    return B.gcall(B.API + 'places:searchText', key, mask, body)


def run(a, key):
    g, seen = load(); reg = R.load(); q = B.jload('candidate_queue.json', []); inq = {c['place_id'] for c in q}
    u, ut = B.usage_today(); ut.setdefault('sweep_calls', 0); ut.setdefault('free_id_calls', 0)
    score = priority(g); today = dt.date.today().isoformat()
    st = {'free_calls': 0, 'paid_calls': 0, 'squares_done': 0, 'squares_split': 0, 'listings_seen': 0, 'new_ids': 0, 'queued': [], 'landline_or_none': 0, 'other': 0}
    known = lambda pid: pid in seen or pid in inq or R.match(reg, pid)[0] is not None
    todo = sorted([c for c in g if due(g[c], a.recheck_days)], key=lambda c: (-score(c), c))
    while todo:
        c = todo.pop(0); cell = g[c]
        if st['free_calls'] + 3 > a.max_free or st['paid_calls'] >= a.max_paid: break
        ids, tok = [], None
        for _ in range(3):                                   # Step 1: free IDs-only pages
            res = search(key, cell['bbox'], 'places.id,nextPageToken', tok); st['free_calls'] += 1; ut['free_id_calls'] += 1
            ids += [p['id'] for p in res.get('places', [])]; tok = res.get('nextPageToken')
            if not tok: break
        if len(ids) >= 60:                                   # Google's maximum: split into 4 smaller squares, sweep them next
            s, w, n, e = cell['bbox']; ms, mw = (s + n) / 2, (w + e) / 2
            kids = {c + 'a': [s, w, ms, mw], c + 'b': [s, mw, ms, e], c + 'c': [ms, w, n, mw], c + 'd': [ms, mw, n, e]}
            for k, bb in kids.items(): g[k] = {'bbox': [round(x, 5) for x in bb]}
            cell.update(split=True, swept=today); st['squares_split'] += 1; todo = list(kids) + todo; continue
        new = [p for p in ids if not known(p)]; st['listings_seen'] += len(ids); st['new_ids'] += len(new)
        paid = 0; tok = None; left = set(new)
        while left and paid < 3 and st['paid_calls'] < a.max_paid:   # Step 2: pay only for squares with unseen listings
            res = search(key, cell['bbox'], FULL_MASK, tok); paid += 1; st['paid_calls'] += 1; ut['sweep_calls'] += 1
            for p in res.get('places', []):
                if p['id'] not in left: continue
                left.discard(p['id'])
                gm = re.sub(r'\D', '', p.get('internationalPhoneNumber', '')); gm = '+' + gm if gm else ''
                name = (p.get('displayName') or {}).get('text', ''); fa = p.get('formattedAddress', '')
                pc = re.search(r'(\d{6})\s*$', fa); pc = pc.group(1) if pc else ''
                if not re.match(r'^\+65[89]\d{7}$', gm): seen[p['id']] = ['landline_or_none', today]; st['landline_or_none'] += 1; continue
                if p.get('businessStatus') != 'OPERATIONAL' or p.get('primaryType') not in B.OK_PRIMARY or not p.get('userRatingCount'):
                    seen[p['id']] = ['not_eligible', today]; st['other'] += 1; continue
                if R.match(reg, None, None, name, pc)[0]: seen[p['id']] = ['known', today]; continue
                q.append(dict(place_id=p['id'], name_hint=name, address_hint=re.sub(r',?\s*Singapore\s*\d{6}\s*$', '', fa), postal_code=pc, mobile_hint=gm,
                              source='google_grid_sweep_%s (Google phone, Edwin asked)' % B.TODAY, added=B.TODAY))
                inq.add(p['id']); seen[p['id']] = ['queued', today]; st['queued'].append('%s (%s, %s/%s)' % (name, pc, p.get('rating'), p.get('userRatingCount')))
            tok = res.get('nextPageToken')
            if not tok: break
        if left: continue                                    # paid budget ran out mid-square: leave it due, retry next run
        for p in ids: seen.setdefault(p, ['known', today])
        cell.update(swept=today, listings=len(ids), new=len(new), paid=paid); st['squares_done'] += 1
    B.jsave('sweep_grid.json', g); B.jsave('seen_places.json', seen); B.jsave('candidate_queue.json', q); B.jsave('usage.json', u)
    st['queue_size'] = len(q); st['squares_still_due'] = sum(1 for c in g.values() if due(c, a.recheck_days))
    print(json.dumps(st, indent=1, ensure_ascii=False))


def status(a):
    g, seen = load(); leaves = [c for c in g.values() if not c.get('split')]
    done = [c for c in leaves if c.get('swept')]
    print(json.dumps({'squares': len(leaves), 'swept': len(done), 'due': sum(1 for c in leaves if due(c, a.recheck_days)),
                      'listings_seen': sum(c.get('listings', 0) for c in done), 'new_found': sum(c.get('new', 0) for c in done),
                      'paid_calls_used': sum(c.get('paid', 0) for c in done), 'place_ids_remembered': len(seen)}, indent=1))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=['run', 'status'])
    ap.add_argument('--max-paid', type=int, default=20); ap.add_argument('--max-free', type=int, default=300); ap.add_argument('--recheck-days', type=int, default=90)
    a = ap.parse_args()
    if a.cmd == 'status': status(a)
    else:
        # Google key: ONLY the PLACES_SERVER_KEY environment variable (Edwin 5 Nov 2026); never copy, print, echo or log it.
        key = os.environ.get('PLACES_SERVER_KEY') or sys.exit('Set PLACES_SERVER_KEY in the environment.')
        run(a, key)
