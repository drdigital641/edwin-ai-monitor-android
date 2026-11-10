"""Area descriptions for estate pages (SEO pass, 2 Nov 2026).

General public knowledge only: MRT stations, malls, parks, hospitals, roads. Nothing here describes a workshop, its services,
prices, hours or quality. slug -> (paragraph, [MRT stations], [landmarks]). Keep every fact checkable on a street map.
"""

import json as _cj, os as _co
def _content(name):
    """Site content lives in data/content/*.json (Edwin 10 Nov 2026: data-driven site); code only renders it."""
    return _cj.load(open(_co.path.join(_co.path.dirname(_co.path.abspath(__file__)), "..", "data", "content", name)))
AREA_COPY = _content("area_copy.json")

# Plain-English region notes used on region pages (general public knowledge).
REGION_COPY = _content("region_copy.json")
