"""Area structure for the directory (Edwin, 1 Nov 2026).

Level 1  region          /areas/<region>/                North, North-East, East, West, Central, Mobile (island-wide)
Level 2  estate cluster  /areas/<estate>/                main local SEO page; published only when it has at least 1 listing
Level 3  service x estate /areas/<estate>/<service>/      published only when 2 or more workshops match

Each workshop is assigned to an estate automatically from its address text and postal code (see assign()).
Postal prefixes are Singapore postal sectors; the first match wins in this order: address keywords, 3-digit prefix, 2-digit prefix.
An entry can force an estate with estate="<slug>" in data.py if the postal code ever points to the wrong cluster.
Mobile services (no shopfront) go to the Mobile region and have no estate.
"""
import re

# region slug -> display. Intros are written in build.py from the live estate list so they never mention an estate that is hidden.
import json as _cj, os as _co
def _content(name):
    """Site content lives in data/content/*.json (Edwin 10 Nov 2026: data-driven site); code only renders it."""
    return _cj.load(open(_co.path.join(_co.path.dirname(_co.path.abspath(__file__)), "..", "data", "content", name)))

REGION_NAMES = _content("region_names.json")
REGION_ORDER = ['north', 'north-east', 'east', 'west', 'central', 'mobile']

REGION_INTRO = _content("region_intro.json")

MOBILE_SLUGS = {'battery-rescue-sg', 'cleanic-detailing'}

# slug -> (name, region, lat, lon, nearby estate slugs, postal prefixes, address keywords, intro sentence)
# lat/lon only centre the map (approximate; the map says so). Intro sentences describe the area, never a workshop.
_E = [tuple(_t[k] for k in ['slug', 'name', 'region', 'lat', 'lon', 'nearby', 'postal_prefixes', 'keywords', 'intro']) for _t in _content("towns.json")]   # towns: data/content/towns.json

# Town hubs (the old "estate clusters"): /areas/<town>/ lists the industrial estates in that town. Navigation, not a listing page.
TOWNS = {}
for _s, _n, _r, _la, _lo, _nb, _pre, _kw, _intro in _E:
    TOWNS[_s] = dict(slug=_s, name=_n, region=_r, lat=_la, lon=_lo, nearby=_nb, intro=_intro)

# Industrial estates (Edwin 3 Nov 2026): the area unit, /areas/<industrial-estate>/. slug, name, town, address keywords, intro.
# An address matches an estate by keyword (first match wins). If a new workshop matches none, add its estate here.
_IE = [tuple(_t[k] for k in ['slug', 'name', 'town', 'keywords', 'intro']) for _t in _content("estates.json")]   # industrial estates: data/content/estates.json
ESTATES = {}
for _s, _n, _t, _kw, _intro in _IE:
    _tw = TOWNS[_t]
    ESTATES[_s] = dict(slug=_s, name=_n, town=_t, region=_tw['region'], lat=_tw['lat'], lon=_tw['lon'], prefixes=[], keywords=_kw, intro=_intro, nearby=[])
for _s, _v in ESTATES.items():   # nearby = other estates in the same town, then estates in neighbouring towns
    _sib = [k for k, w in ESTATES.items() if w['town'] == _v['town'] and k != _s]
    _nbt = [k for k, w in ESTATES.items() if w['town'] in TOWNS[_v['town']]['nearby'] and k != _s]
    _v['nearby'] = _sib + _nbt

# Longest prefix first, so 757 (Woodlands Industrial Park) beats 75 (Sembawang) and 737 beats 73.
_KW = [(k, s) for s, v in ESTATES.items() for k in v['keywords']]


def _addr_texts(e):
    """(text, postal) pairs for every address an entry has."""
    out = []
    for a in e.get('addresses') or []:
        out.append(((a.get('label') or '') + ' ' + (a.get('street') or ''), a.get('postal')))
    if e.get('address_public'):
        m = re.search(r'\b(\d{6})\b', e['address_public'])
        out.append((e['address_public'], m.group(1) if m else None))
    return out


def estate_for(text, postal):
    t = text.lower()
    for k, s in _KW:
        if k in t:
            return s
    return None


def assign(e):
    """Return (region, [estate slugs]) for an entry. First estate is the primary one (used in breadcrumbs)."""
    if e['slug'] in MOBILE_SLUGS or e.get('mobile'):
        return 'mobile', []
    if e.get('estate'):
        found = [e['estate']]
    else:
        found = []
        for text, postal in _addr_texts(e):
            s = estate_for(text, postal)
            if s and s not in found:
                found.append(s)
    if not found:
        raise ValueError('No estate for %s: add estate="..." in data.py' % e['slug'])
    return ESTATES[found[0]]['region'], found


def annotate(entries):
    """Set e['region'], e['estates'] and e['regions'] (the search filter list) on every entry."""
    for e in entries:
        region, estates = assign(e)
        coverage = list(e['regions']) if region == 'mobile' else [region]
        e['region'], e['estates'] = region, estates
        e['regions'] = coverage + (['mobile'] if region == 'mobile' else [])


def published(entries):
    """What gets built: regions with a listing, estates with at least 1 listing, service x estate pairs with 2 or more.
    Returns (regions, estates, pairs) where pairs maps (estate, category) -> [entries]."""
    regions = [r for r in REGION_ORDER if any(e['region'] == r for e in entries)]
    est = {s: [e for e in entries if s in e['estates']] for s in ESTATES}
    est = {s: v for s, v in est.items() if v}
    pairs = {}
    for s, v in est.items():
        for e in v:
            for _c in e.get('categories', [e['category']]):
                pairs.setdefault((s, _c), []).append(e)
    pairs = {k: v for k, v in pairs.items() if len(v) >= 2}
    return regions, est, pairs
