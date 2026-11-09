"""ONE shared tag list (Edwin 3 Nov 2026) for services, brands and problems. Cards, service pages, guides and search all read from here,
so they never disagree. A card gets a tag when what its customers mention (data/pilot mentioned_services, in our own words) matches the tag's pattern.
kind: service | brand | problem.  cat: the service-page category a service tag can move a card to (refile) or None.
guide: slug of the guide page that explains the tag (problem and brand tags), else None."""
import re

import json as _cj, os as _co
def _content(name):
    """Site content lives in data/content/*.json (Edwin 10 Nov 2026: data-driven site); code only renders it."""
    return _cj.load(open(_co.path.join(_co.path.dirname(_co.path.abspath(__file__)), "..", "data", "content", name)))
TAGS = _content("tags.json")
BY_ID = {t['id']: t for t in TAGS}
_RX = {t['id']: re.compile(t['rx'], re.I) for t in TAGS}


def card_tags(mentions):
    """Tag ids that match what customers mention (list of short phrases in our own words)."""
    return [t['id'] for t in TAGS if any(_RX[t['id']].search(m) for m in (mentions or []))]


def refile(mentions, current):
    """Move a general-servicing card to a specific service category only when reviews clearly support it:
    at least 2 mentions in that category and at least half of all mentions. Otherwise keep the category."""
    if current != 'general-servicing-repair' or not mentions:
        return current
    best, n_best = current, 0
    for t in TAGS:
        if t['kind'] != 'service' or not t['cat']:
            continue
        n = sum(1 for m in mentions if _RX[t['id']].search(m))
        if n >= 2 and n * 2 >= len(mentions) and n > n_best:
            best, n_best = t['cat'], n
    return best


def apply(entries, pilot_dir):
    """Tag every entry and refile cards. Called once from data.py, so build.py and check.py see the same categories. Returns [(slug, from, to)]."""
    import json, os
    moved = []
    for e in entries:
        pf = os.path.join(pilot_dir, e['slug'] + '.json')
        m = (json.load(open(pf)).get('mentioned_services') or []) if os.path.exists(pf) else []
        e['tags'] = card_tags(m)
        new = refile(m, e['category'])
        if new != e['category']:
            moved.append((e['slug'], e['category'], new))
            e['category'] = new
            e['categories'] = [new] + [c for c in e.get('categories', []) if c != new]
        # Edwin 4 Nov 2026 (decision card): a card also appears on a service page (and its area x service page) when at least one
        # customer mention in its Google reviews matches that service. The card then says "Customers mention ..." on that page.
        for t in TAGS:
            if t['kind'] != 'service' or not t['cat']:
                continue
            hit = [x for x in m if _RX[t['id']].search(x)]
            if hit and t['cat'] not in e.get('categories', [e['category']]):
                e['categories'] = list(e.get('categories', [e['category']])) + [t['cat']]
                e.setdefault('mention_cats', {})[t['cat']] = hit[0]
    return moved
