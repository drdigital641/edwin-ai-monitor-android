"""ONE shared tag list (Edwin 3 Nov 2026) for services, brands and problems. Cards, service pages, guides and search all read from here,
so they never disagree. A card gets a tag when what its customers mention (data/pilot mentioned_services, in our own words) matches the tag's pattern.
kind: service | brand | problem.  cat: the service-page category a service tag can move a card to (refile) or None.
guide: slug of the guide page that explains the tag (problem and brand tags), else None."""
import re

TAGS = [
    # ---- services
    dict(id='aircon', kind='service', label='Aircon', rx=r'aircon|air-?con|\bac\b', cat='car-aircon-repair', guide='car-aircon-not-cold'),
    dict(id='brakes', kind='service', label='Brakes', rx=r'brake', cat=None, guide='brake-squeal-noise'),
    dict(id='suspension', kind='service', label='Suspension and undercarriage', rx=r'undercarriage|suspension|absorber|stabiliser|drive ?shaft|wear-and-tear|alignment', cat=None, guide='car-knocking-over-humps'),
    dict(id='gearbox', kind='service', label='Gearbox and transmission', rx=r'gearbox|transmission|clutch|cvt', cat='gearbox-repair', guide='gearbox-cvt-jerking'),
    dict(id='diagnostics', kind='service', label='Fault diagnosis', rx=r'fault|under-bonnet|sensor|throttle|diagnos', cat=None, guide='engine-warning-light'),
    dict(id='cooling', kind='service', label='Cooling', rx=r'radiator|cooling|coolant|fan motor', cat=None, guide='car-overheating'),
    dict(id='battery', kind='service', label='Battery and starter', rx=r'starter|battery', cat='car-battery', guide='car-wont-start-battery'),
    dict(id='ecu-abs', kind='service', label='ABS and ECU', rx=r'\becu\b|\babs\b', cat='abs-ecu-module-repair', guide=None),
    dict(id='bodywork', kind='service', label='Bodywork and dents', rx=r'dent|bodywork|fender|scratch|spray|paint|accident', cat='spray-painting-bodywork', guide=None),
    dict(id='detailing', kind='service', label='Detailing and coating', rx=r'detailing|coating|polish|nano|car wash|snow foam', cat='car-detailing-coating', guide=None),
    dict(id='wrap-ppf', kind='service', label='Wrap and PPF', rx=r'wrap|\bppf\b', cat='car-wrap-ppf', guide=None),
    dict(id='oil-service', kind='service', label='Oil and servicing', rx=r'oil|servicing|full car service|spark plug', cat=None, guide=None),
    dict(id='tyres', kind='service', label='Tyres', rx=r'tyre|tire', cat=None, guide=None),
    # ---- brands (the three with a brand page also carry its guide)
    dict(id='bmw-mercedes', kind='brand', label='BMW and Mercedes-Benz', rx=r'bmw|mercedes|continental', cat=None, guide='bmw-mercedes-workshops-singapore'),
    dict(id='toyota', kind='brand', label='Toyota', rx=r'toyota|harrier|vios|camry|corolla|alphard|prius', cat=None, guide='toyota-workshops-singapore'),
    dict(id='honda', kind='brand', label='Honda', rx=r'honda', cat=None, guide='honda-workshops-singapore'),
    dict(id='volkswagen-audi', kind='brand', label='Volkswagen and Audi', rx=r'volkswagen|\bvw\b|audi', cat=None, guide=None),
    # ---- problems (what the customer notices)
    dict(id='p-knocking', kind='problem', label='Knocking over humps', rx=r'undercarriage|suspension|absorber|stabiliser|noise|drive ?shaft|wear-and-tear', cat=None, guide='car-knocking-over-humps'),
    dict(id='p-aircon-not-cold', kind='problem', label='Aircon not cold', rx=r'aircon|air-?con|\bac\b', cat=None, guide='car-aircon-not-cold'),
    dict(id='p-wont-start', kind='problem', label="Car won't start", rx=r'starter|breakdown|battery', cat=None, guide='car-wont-start-battery'),
    dict(id='p-gearbox-jerking', kind='problem', label='Gearbox or CVT jerking', rx=r'gearbox|transmission|clutch|cvt', cat=None, guide='gearbox-cvt-jerking'),
    dict(id='p-brake-squeal', kind='problem', label='Brake squeal', rx=r'brake', cat=None, guide='brake-squeal-noise'),
    dict(id='p-warning-light', kind='problem', label='Engine warning light', rx=r'fault|under-bonnet|sensor|throttle|diagnostics', cat=None, guide='engine-warning-light'),
    dict(id='p-overheating', kind='problem', label='Car overheating', rx=r'radiator|cooling|coolant|fan', cat=None, guide='car-overheating'),
    # ---- driver guides (Edwin 6 Nov 2026: layman guides for what drivers search; matched from card data only)
    dict(id='p-dent', kind='problem', label='Dents and scratches', rx=r'\bdent|scratch|bumper|panel beat|fender', cat=None, guide='dent-repair-singapore'),
    dict(id='p-spray', kind='problem', label='Spray painting', rx=r'spray|respray|paint', cat=None, guide='car-spray-painting-singapore'),
    dict(id='p-battery-dead', kind='problem', label='Battery dead', rx=r'battery|jump ?start', cat=None, guide='car-battery-dead'),
    dict(id='p-dash-lights', kind='problem', label='Dashboard warning lights', rx=r'warning light|engine light|check engine|diagnos', cat=None, guide='dashboard-warning-lights'),
    dict(id='h-choose', kind='howto', label='Choosing a workshop', rx=r'repair|diagnos|overhaul', cat=None, guide='how-to-choose-a-car-workshop'),
    dict(id='h-servicing-cost', kind='howto', label='Servicing cost', rx=r'servicing|oil change|service package|maintenance', cat=None, guide='car-servicing-cost-singapore'),
    dict(id='h-before-visit', kind='howto', label='Before a workshop visit', rx=r'pre-?purchase|inspection|diagnos|health check', cat=None, guide='before-a-workshop-visit'),
]
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
