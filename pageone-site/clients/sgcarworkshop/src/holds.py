#!/usr/bin/env python3
"""Hold reason codes for SG Car Workshop cards that are not built (Edwin 22 Nov 2026: "add a hold reason column ... with per-reason
counts in each nightly report so we can tune the sweep").

Every held record in data/workshops/<slug>.json keeps its free-text "hold" note and now also a short "hold_code" from CODES.
Sweep-stage drops (data/seen_places.json outcomes) are counted under the same codes, so one report covers the whole funnel.

    python3 src/holds.py backfill          # set hold_code on every held record that lacks one (from its hold note)
    python3 src/holds.py report            # per-reason counts (all held records) + sweep-stage counts
    python3 src/holds.py report --since 2026-11-21   # only records held on/after that date (held_on), plus a list
"""
import argparse, collections, glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..', 'data')

CODES = {
    'no_mobile':        'no mobile number on Google',
    'landline_only':    'landline only on Google',
    'complaints':       'too many complaints in sampled reviews',
    'not_enough_facts': 'not enough facts (retired 22 Nov 2026: a basic card is built instead)',
    'live_check_failed': 'live check failed (retired for OneMap 401 / blocked websites 22 Nov 2026: those are retries or skipped sources)',
    'duplicate':        'duplicate (same mobile, address or name as another card)',
    'closed':           'closed on Google',
    'not_car_workshop': 'not a car workshop (motorcycle, e-bike, supplier, office, car sales)',
    'no_estate':        'no estate page for its address yet',
}

# order matters: the first match wins. Edwin 22 Nov 2026: a duplicate first, then not-a-car-workshop (so a motorcycle shop with complaints
# is coded not_car_workshop), then complaints. "closed" is never matched from the note text: it comes only from Google businessStatus CLOSED_*.
# not_enough_facts and website-blocked are no longer hold reasons (a basic card is built instead); their rules stay so old notes still code.
_RULES = [
    ('duplicate', r'same mobile|shares mobile|is also on|same address|identical to|same unit|slug clash|same mobile/slug|same as star'),
    ('not_car_workshop', r'motorcycle|motorbike|scooter|e-bike|\bbikes\b|not a car workshop|equipment supplier|used car sales|\boffice\b|claims service'),
    ('complaints', r'complaint|dishonest|allege|dispute|overcharg|hidden charge|impersonation|damage|honesty'),
    ('landline_only', r'landline'),
    ('no_mobile', r'no mobile|no sg mobile'),
    ('no_estate', r'no estate|no workshop estate'),
    ('live_check_failed', r'live check|fetch failed'),
    ('not_enough_facts', r'only \d+ (google )?rating|\b1 rating|\b2 ratings|no (positive )?written|no review text|not enough'),
]
# Hard holds that the sweep may still set (Edwin 22 Nov 2026). Anything else gets a basic card or an infrastructure retry instead.
HARD = ('duplicate', 'not_car_workshop', 'complaints', 'landline_only', 'no_mobile', 'closed', 'no_estate')
SEEN = {'landline_or_none': 'landline_only', 'not_eligible': 'not_car_workshop'}


def classify(note, business_status=None):
    """Hold code for a held record. Closed only from Google's businessStatus (CLOSED_TEMPORARILY / CLOSED_PERMANENTLY), never a word match."""
    if (business_status or '').upper().startswith('CLOSED'): return 'closed'
    t = (note or '').lower()
    for code, rx in _RULES:
        if re.search(rx, t): return code
    return None


def business_status(slug):
    try: return json.load(open(os.path.join(D, 'google_cache', slug + '.json'))).get('businessStatus')
    except Exception: return None


def held_records():
    for f in sorted(glob.glob(os.path.join(D, 'workshops', '*.json'))):
        r = json.load(open(f))
        if r.get('status') != 'active' and (r.get('hold') or r.get('hold_code')): yield f, r


def backfill(a):
    n = 0; miss = []
    for f, r in held_records():
        if r.get('hold_code') in CODES: continue
        c = classify(r.get('hold'), business_status(r['slug']))
        if not c: miss.append(r['slug']); continue
        r['hold_code'] = c
        m = re.match(r'held (\d+) Nov', r.get('hold') or '')
        if m and not r.get('held_on'): r['held_on'] = '2026-11-%02d' % int(m.group(1))   # SGT night the card was held
        json.dump(r, open(f, 'w'), indent=1, ensure_ascii=False); n += 1
    print(json.dumps({'set': n, 'unclassified': miss}, indent=1))
    if miss: sys.exit(1)


def report(a):
    rows = [(r['slug'], r.get('name'), r.get('hold_code') or 'unclassified', r.get('held_on') or '', r.get('hold'))
            for _, r in held_records() if not a.since or (r.get('held_on') or '') >= a.since]
    by = collections.Counter(x[2] for x in rows)
    seen = json.load(open(os.path.join(D, 'seen_places.json')))
    sw = collections.Counter(SEEN[v[0]] for v in seen.values() if isinstance(v, list) and v and v[0] in SEEN)
    out = {'held_cards': len(rows), 'held_by_reason': dict(by.most_common()),
           'sweep_stage_not_queued': dict(sw.most_common()), 'codes': CODES}
    if a.since: out['held'] = [{'slug': s, 'name': n, 'code': c, 'held_on': d, 'note': h} for s, n, c, d, h in rows]
    print(json.dumps(out, indent=1, ensure_ascii=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('backfill'); r = sub.add_parser('report'); r.add_argument('--since', default='')
    a = ap.parse_args(); {'backfill': backfill, 'report': report}[a.cmd](a)
