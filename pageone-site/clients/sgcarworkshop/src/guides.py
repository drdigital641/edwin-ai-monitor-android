"""Driver guide pages (Edwin 3 Nov 2026): 7 common problems + 3 brand pages; 6 Nov 2026: 7 layman driver guides (4 problem, 3 how-to). General, well-known mechanical knowledge only.
No prices, no claims about any workshop. Workshops are linked only where a card's "customers mention" services match (pattern in `match`).
kw = words people type; the homepage search routes a query containing any of them to the guide."""

import json as _cj, os as _co
def _content(name):
    """Site content lives in data/content/*.json (Edwin 10 Nov 2026: data-driven site); code only renders it."""
    return _cj.load(open(_co.path.join(_co.path.dirname(_co.path.abspath(__file__)), "..", "data", "content", name)))
GUIDES = _content("guides.json")


def gpath(g):
    """Public path: brand guides live under /brands/<brand>/, problem guides under /guides/<slug>/."""
    return 'brands/%s/' % g['brand'] if g.get('kind') == 'brand' else 'guides/%s/' % g['slug']


# The match pattern of every guide comes from the shared tag list (tags.py), so a guide, a card and the search never disagree.
import tags as _t
for _g in GUIDES:
    _tag = next(t for t in _t.TAGS if t['guide'] == _g['slug'] and (t['kind'] == _g['kind'] or t['id'] == _g.get('tag_id')))
    _g['tag'] = _tag['id']
    _g['match'] = _tag['rx']
