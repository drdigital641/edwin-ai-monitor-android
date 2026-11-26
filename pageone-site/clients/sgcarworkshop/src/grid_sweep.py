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
Cards are still built only from data/candidate_queue.json via enrich-queue (Google is the source of truth).

26 Nov 2026 (Website Manager diagnosis, Edwin's nights fell under 10 cards): all 396 squares were swept once by 17 Nov, so nothing was due.
  * EXTRA_QUERIES are swept square by square as a second pass, with the same free IDs-only step first and the same car_repair type filter,
    square limit, OK_PRIMARY and 60-result split. Each query keeps its own date in cell["q"][query] (swept/listings/new/paid), so due()
    works per query; "car workshop" keeps the cell's own swept date and its 90-day recheck.
  * Zero-review shops are queued (OPERATIONAL + OK_PRIMARY + Google +65 8/9 mobile) as basic cards (Edwin 22 Nov). Seen outcomes are now
    specific: closed, not_car_repair, landline_or_none, no_reviews_queued, queued, known (+ the square id).
  * Old "not_eligible" ids (written before 26 Nov, no reason kept) are re-checked last: a square's free "car workshop" ids are listed, and
    if any is an old not_eligible id the square gets the paid full search, within the same nightly paid cap. Done once per square.
    python3 grid_sweep.py yield --squares 10 --queries "car servicing;car aircon;car spray painting"   # free IDs only, no paid call"""
import argparse, datetime as dt, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import basic_agent as B  # noqa: E402
import registry as R  # noqa: E402

S, N, W, E = 1.235, 1.475, 103.605, 104.045   # mainland + Jurong Island bounding box
STEP = 0.02                                   # ~2.2 km squares
QUERY = 'car workshop'
EXTRA_QUERIES = ['car servicing', 'car aircon', 'car spray painting', 'car battery', 'tyre shop', 'auto electrical', 'gearbox repair']
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


def qstate(cell, query):
    """Per-query sweep record of a square; "car workshop" uses the square's own fields."""
    return cell if query == QUERY else cell.setdefault('q', {}).setdefault(query, {})


def due(cell, days, query=QUERY):
    if cell.get('split'): return False
    sw = (cell if query == QUERY else (cell.get('q') or {}).get(query) or {}).get('swept')
    return not sw or (dt.date.today() - dt.date.fromisoformat(sw)).days >= days


def search(key, bbox, mask, tok=None, query=QUERY):
    s, w, n, e = bbox
    body = {'textQuery': query, 'regionCode': 'SG', 'pageSize': 20, 'includedType': 'car_repair', 'strictTypeFiltering': True,
            'locationRestriction': {'rectangle': {'low': {'latitude': s, 'longitude': w}, 'high': {'latitude': n, 'longitude': e}}}}
    if tok: body['pageToken'] = tok
    return B.gcall(B.API + 'places:searchText', key, mask, body)


def free_ids(key, cell, query, st, ut):
    ids, tok = [], None
    for _ in range(3):                                   # free IDs-only pages
        res = search(key, cell['bbox'], 'places.id,nextPageToken', tok, query); st['free_calls'] += 1; ut['free_id_calls'] += 1
        ids += [p['id'] for p in res.get('places', [])]; tok = res.get('nextPageToken')
        if not tok: break
    return ids


def run(a, key):
    g, seen = load(); reg = R.load(); q = B.jload('candidate_queue.json', []); inq = {c['place_id'] for c in q}
    u, ut = B.usage_today(); ut.setdefault('sweep_calls', 0); ut.setdefault('free_id_calls', 0)
    score = priority(g); today = dt.date.today().isoformat()
    left = B.night_sweep_paid() - ut['sweep_calls'] - ut.get('text_search', 0)   # one sweep per Google day; an approved one-night raise lets the same sweep continue
    if left <= 0: sys.exit('STOP: this Google day\'s paid sweep allowance is used (%d). Zero-spend rule, Edwin 6 Nov 2026.' % B.night_sweep_paid())
    a.max_paid = min(a.max_paid, left)
    queries = [QUERY] + [x for x in (a.queries.split(';') if a.queries else EXTRA_QUERIES) if x and x != QUERY]
    st = {'free_calls': 0, 'paid_calls': 0, 'squares_done': 0, 'squares_split': 0, 'listings_seen': 0, 'new_ids': 0, 'queued': [],
          'landline_or_none': 0, 'closed': 0, 'not_car_repair': 0, 'no_reviews_queued': 0, 'per_query': {}, 'not_eligible_squares': 0}
    known = lambda pid: pid in seen or pid in inq or R.match(reg, pid)[0] is not None

    def full(c, cell, query, want):
        """Paid full search of a square; queue every wanted id that qualifies. Returns (paid calls, ids not reached)."""
        paid = 0; tok = None; left = set(want)
        while left and paid < 3 and st['paid_calls'] < a.max_paid:
            res = search(key, cell['bbox'], FULL_MASK, tok, query); paid += 1; st['paid_calls'] += 1; ut['sweep_calls'] += 1
            for p in res.get('places', []):
                if p['id'] not in left: continue
                left.discard(p['id'])
                gm = re.sub(r'\D', '', p.get('internationalPhoneNumber', '')); gm = '+' + gm if gm else ''
                name = (p.get('displayName') or {}).get('text', ''); fa = p.get('formattedAddress', '')
                pc = re.search(r'(\d{6})\s*$', fa); pc = pc.group(1) if pc else ''
                if not re.match(r'^\+65[89]\d{7}$', gm): seen[p['id']] = ['landline_or_none', today, c]; st['landline_or_none'] += 1; continue
                if p.get('businessStatus') != 'OPERATIONAL': seen[p['id']] = ['closed', today, c]; st['closed'] += 1; continue
                if p.get('primaryType') not in B.OK_PRIMARY: seen[p['id']] = ['not_car_repair', today, c]; st['not_car_repair'] += 1; continue
                if R.match(reg, None, None, name, pc)[0]: seen[p['id']] = ['known', today, c]; continue
                q.append(dict(place_id=p['id'], name_hint=name, address_hint=re.sub(r',?\s*Singapore\s*\d{6}\s*$', '', fa), postal_code=pc, mobile_hint=gm,
                              source='google_grid_sweep_%s "%s" (Google phone, Edwin asked)' % (B.TODAY, query), added=B.TODAY))
                inq.add(p['id']); out = 'queued' if p.get('userRatingCount') else 'no_reviews_queued'
                seen[p['id']] = [out, today, c]
                if out == 'no_reviews_queued': st['no_reviews_queued'] += 1
                st['queued'].append('%s (%s, %s/%s, "%s")' % (name, pc, p.get('rating'), p.get('userRatingCount') or 0, query))
                st['per_query'].setdefault(query, {}).setdefault('queued', 0); st['per_query'][query]['queued'] += 1
            tok = res.get('nextPageToken')
            if not tok: break
        return paid, left

    for query in queries:                                    # pass 1 "car workshop" (90-day recheck), then the extra queries
        pq = st['per_query'].setdefault(query, {'squares': 0, 'free_calls': 0, 'paid_calls': 0, 'new_ids': 0, 'queued': 0})
        todo = sorted([c for c in g if due(g[c], a.recheck_days, query)], key=lambda c: (-score(c), c))
        while todo:
            c = todo.pop(0); cell = g[c]
            if st['free_calls'] + 3 > a.max_free or st['paid_calls'] >= a.max_paid: break
            f0, p0 = st['free_calls'], st['paid_calls']
            ids = free_ids(key, cell, query, st, ut)
            if len(ids) >= 60:                               # Google's maximum: split into 4 smaller squares, sweep them next
                s, w, n, e = cell['bbox']; ms, mw = (s + n) / 2, (w + e) / 2
                kids = {c + 'a': [s, w, ms, mw], c + 'b': [s, mw, ms, e], c + 'c': [ms, w, n, mw], c + 'd': [ms, mw, n, e]}
                for k, bb in kids.items():
                    g[k] = {'bbox': [round(x, 5) for x in bb]}
                    if query != QUERY:                       # children keep the parent's "car workshop" and other query dates
                        for f in ('swept', 'listings', 'new', 'paid'):
                            if f in cell: g[k][f] = cell[f]
                        g[k]['q'] = {k2: dict(v) for k2, v in (cell.get('q') or {}).items() if k2 != query}
                cell.update(split=True); qstate(cell, query)['swept'] = today; st['squares_split'] += 1; todo = list(kids) + todo
                pq['free_calls'] += st['free_calls'] - f0; continue
            new = [p for p in ids if not known(p)]; st['listings_seen'] += len(ids); st['new_ids'] += len(new); pq['new_ids'] += len(new)
            paid, left = full(c, cell, query, new) if new else (0, set())
            pq['free_calls'] += st['free_calls'] - f0; pq['paid_calls'] += st['paid_calls'] - p0
            if left: continue                                # paid budget ran out mid-square: leave it due, retry next run
            for p in ids: seen.setdefault(p, ['known', today, c])
            qstate(cell, query).update(swept=today, listings=len(ids), new=len(new), paid=paid); st['squares_done'] += 1; pq['squares'] += 1

    # pass 3: old not_eligible ids (no reason kept before 26 Nov), once per square, with whatever paid budget is left
    old_ne = {p for p, v in seen.items() if v and v[0] == 'not_eligible'}
    if old_ne and not a.no_recheck_old:
        for c in sorted([c for c in g if not g[c].get('split') and not g[c].get('ne_checked')], key=lambda c: (-score(c), c)):
            if st['free_calls'] + 3 > a.max_free or st['paid_calls'] >= a.max_paid: break
            cell = g[c]; ids = free_ids(key, cell, QUERY, st, ut); hit = [p for p in ids if p in old_ne]
            if hit:
                for p in hit: seen.pop(p, None)              # re-judge with today's rules
                paid, left = full(c, cell, QUERY, hit); st['not_eligible_squares'] += 1
                for p in left: seen[p] = ['not_eligible', today, c]
                if left: continue
                for p in hit: seen.setdefault(p, ['known', today, c])   # listed in the free step but not reached: keep as known
            cell['ne_checked'] = today
    B.jsave('sweep_grid.json', g); B.jsave('seen_places.json', seen); B.jsave('candidate_queue.json', q); B.jsave('usage.json', u)
    st['queue_size'] = len(q); st['nights_of_supply'] = round(len(q) / 22.0, 1)
    st['squares_still_due'] = {qq: sum(1 for c in g.values() if due(c, a.recheck_days, qq)) for qq in queries}
    st['old_not_eligible_left'] = sum(1 for v in seen.values() if v and v[0] == 'not_eligible')
    print(json.dumps(st, indent=1, ensure_ascii=False))


def yield_test(a, key):
    """Free IDs-only test: top squares x queries, counts ids we have never seen. No paid call."""
    g, seen = load(); reg = R.load(); inq = {c['place_id'] for c in B.jload('candidate_queue.json', [])}
    u, ut = B.usage_today(); ut.setdefault('free_id_calls', 0); score = priority(g)
    known = lambda pid: pid in seen or pid in inq or R.match(reg, pid)[0] is not None
    cells = sorted([c for c in g if not g[c].get('split')], key=lambda c: (-score(c), c))[:a.squares]
    st = {'free_calls': 0}; out = {}
    for query in [x for x in a.queries.split(';') if x]:
        ids = set()
        for c in cells: ids |= set(free_ids(key, g[c], query, st, ut))
        new = sorted(p for p in ids if not known(p)); out[query] = {'listed': len(ids), 'unseen': len(new)}
    B.jsave('usage.json', u)
    print(json.dumps({'squares': cells, 'free_calls': st['free_calls'], 'paid_calls': 0, 'by_query': out}, indent=1))


def status(a):
    g, seen = load(); leaves = [c for c in g.values() if not c.get('split')]
    done = [c for c in leaves if c.get('swept')]
    print(json.dumps({'squares': len(leaves), 'swept': len(done), 'due': sum(1 for c in leaves if due(c, a.recheck_days)),
                      'listings_seen': sum(c.get('listings', 0) for c in done), 'new_found': sum(c.get('new', 0) for c in done),
                      'paid_calls_used': sum(c.get('paid', 0) for c in done), 'place_ids_remembered': len(seen)}, indent=1))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=['run', 'status', 'yield'])
    ap.add_argument('--queries', default=''); ap.add_argument('--squares', type=int, default=10); ap.add_argument('--no-recheck-old', action='store_true')
    ap.add_argument('--max-paid', type=int, default=20); ap.add_argument('--max-free', type=int, default=300); ap.add_argument('--recheck-days', type=int, default=90)
    a = ap.parse_args()
    if a.cmd == 'status': status(a)
    else:
        # Google key: ONLY the PLACES_SERVER_KEY environment variable (Edwin 5 Nov 2026); never copy, print, echo or log it.
        key = os.environ.get('PLACES_SERVER_KEY') or sys.exit('Set PLACES_SERVER_KEY in the environment.')
        yield_test(a, key) if a.cmd == 'yield' else run(a, key)
