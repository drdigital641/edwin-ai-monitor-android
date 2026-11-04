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
REGION_NAMES = {
    'north': 'North', 'north-east': 'North-East', 'east': 'East', 'west': 'West', 'central': 'Central',
    'mobile': 'Mobile (island-wide)',
}
REGION_ORDER = ['north', 'north-east', 'east', 'west', 'central', 'mobile']

REGION_INTRO = {
    'north': 'Car workshops and car services in the North region of Singapore, covering Woodlands, Kranji, Yishun and the Sembawang and Admiralty areas.',
    'north-east': 'Car workshops and car services in the North-East region of Singapore, covering Ang Mo Kio, Serangoon North, Defu and Hougang, and Sengkang.',
    'east': 'Car workshops and car services in the East region of Singapore, covering Kaki Bukit, Bedok North, Tampines and the Changi and Loyang areas.',
    'west': 'Car workshops and car services in the West region of Singapore, covering Toh Guan and Jurong East, Jurong West, Pandan Loop, Bukit Batok and Tuas.',
    'central': 'Car workshops and car services in the Central region of Singapore, covering Sin Ming and Bishan, Toa Payoh, Ubi, Eunos, MacPherson, Jalan Besar and Kallang Bahru, and Alexandra and Bukit Merah.',
    'mobile': 'Mobile car services that come to your car anywhere in Singapore. These listings have no single shopfront, so the work is done where your car is parked.',
}

MOBILE_SLUGS = {'battery-rescue-sg', 'cleanic-detailing'}

# slug -> (name, region, lat, lon, nearby estate slugs, postal prefixes, address keywords, intro sentence)
# lat/lon only centre the map (approximate; the map says so). Intro sentences describe the area, never a workshop.
_E = [
    # ---- East
    ('kaki-bukit', 'Kaki Bukit', 'east', 1.3345, 103.9050, ['ubi', 'eunos', 'bedok-north'], ['415', '416', '417'], ['kaki bukit'],
     'Kaki Bukit is an industrial estate in the East region, around Kaki Bukit Avenue and Kaki Bukit Road, with many workshops, trade units and parts suppliers.'),
    ('ubi', 'Ubi', 'central', 1.3300, 103.8970, ['kaki-bukit', 'eunos', 'macpherson'], ['408'], ['ubi ave', 'ubi road', 'ubi rd', 'paya ubi'],
     'Ubi is an industrial area near Paya Lebar in the Geylang planning area (Central region), around Ubi Avenue and Ubi Road, with motor workshops mixed in among light industry.'),
    ('eunos', 'Eunos', 'central', 1.3190, 103.9040, ['ubi', 'kaki-bukit', 'bedok-north'], ['400', '401', '402', '403', '404', '405', '406', '407', '409'], ['eunos'],
     'Eunos is a mixed residential and industrial area in the Geylang planning area (Central region), close to Paya Lebar, Ubi and Kaki Bukit.'),
    ('bedok-north', 'Bedok North', 'east', 1.3350, 103.9310, ['kaki-bukit', 'eunos', 'changi-loyang', 'tampines'], ['46'], ['bedok north'],
     'Bedok North is an industrial pocket in the East region, around Bedok North Avenue and Bedok North Street.'),
    ('tampines', 'Tampines', 'east', 1.3530, 103.9440, ['bedok-north', 'changi-loyang', 'kaki-bukit'], ['52'], ['tampines'],
     'Tampines is a town in the East region with light industrial parks around Tampines Street 92 and 93.'),
    ('changi-loyang', 'Changi and Loyang', 'east', 1.3480, 103.9720, ['bedok-north', 'kaki-bukit'], ['486', '49', '50'], ['loyang', 'changi'],
     'Changi and Loyang cover the industrial areas at the east end of Singapore, around Loyang Way and Changi South.'),
    # ---- North
    ('woodlands', 'Woodlands', 'north', 1.4440, 103.7930, ['kranji', 'sembawang-admiralty', 'yishun'], ['730', '731', '732', '733', '734', '735', '736', '737', '738', '757'], ['woodlands'],
     'Woodlands is the main industrial area in the north-west, around Woodlands Industrial Park and the Woodlands Avenue roads, close to the Causeway.'),
    ('kranji', 'Kranji', 'north', 1.4200, 103.7620, ['woodlands', 'sembawang-admiralty'], ['72', '739'], ['kranji', 'jalan lam huat', 'sungei kadut'],
     'Kranji is an industrial area in the north-west, around Kranji Way, Jalan Lam Huat and Sungei Kadut.'),
    ('yishun', 'Yishun', 'north', 1.4220, 103.8350, ['sembawang-admiralty', 'woodlands', 'ang-mo-kio'], ['76', '77'], ['yishun'],
     'Yishun has two main motor trade clusters, Yishun Industrial Park A and the Yishun Industrial Street 1 area around North Spring Bizhub.'),
    ('sembawang-admiralty', 'Sembawang and Admiralty', 'north', 1.4400, 103.8170, ['woodlands', 'yishun', 'kranji'], ['750', '751', '752', '753', '754', '755', '756', '758', '759'], ['sembawang', 'admiralty'],
     'Sembawang and Admiralty are neighbourhoods in the north of Singapore, along roads such as Sembawang Road.'),
    # ---- North-East
    ('ang-mo-kio', 'Ang Mo Kio', 'north-east', 1.3800, 103.8660, ['serangoon-north', 'sin-ming-bishan', 'yishun'], ['56'], ['ang mo kio'],
     'Ang Mo Kio has a long-running industrial estate, Ang Mo Kio Industrial Park, with workshops serving the north-east.'),
    ('serangoon-north', 'Serangoon North', 'north-east', 1.3680, 103.8700, ['ang-mo-kio', 'defu-hougang', 'sin-ming-bishan'], ['55'], ['serangoon north'],
     'Serangoon North is an industrial and residential area in the North-East region, around Serangoon North Avenue.'),
    ('defu-hougang', 'Defu and Hougang', 'north-east', 1.3600, 103.8900, ['serangoon-north', 'sengkang', 'macpherson'], ['53'], ['defu', 'hougang', 'kovan'],
     'Defu and Hougang cover the Defu Lane industrial area and the Hougang neighbourhood in the North-East region.'),
    ('sengkang', 'Sengkang', 'north-east', 1.3910, 103.8950, ['defu-hougang', 'serangoon-north'], ['54', '82'], ['sengkang', 'punggol'],
     'Sengkang and nearby Punggol are newer residential towns in the North-East region.'),
    # ---- Central
    ('sin-ming-bishan', 'Sin Ming and Bishan', 'central', 1.3640, 103.8340, ['ang-mo-kio', 'toa-payoh', 'serangoon-north'], ['57'], ['sin ming', 'bishan'],
     'Sin Ming and Bishan take in the Sin Ming Industrial Estate and the Bishan area in the middle of Singapore.'),
    ('toa-payoh', 'Toa Payoh', 'central', 1.3330, 103.8560, ['sin-ming-bishan', 'macpherson', 'jalan-besar-kallang-bahru'], ['31', '32'], ['toa payoh'],
     'Toa Payoh has an industrial park and trade units in the Central region, close to Bishan and MacPherson.'),
    ('macpherson', 'MacPherson', 'central', 1.3270, 103.8870, ['toa-payoh', 'ubi', 'jalan-besar-kallang-bahru'], ['36'], ['macpherson'],
     'MacPherson is an area in the Central region around MacPherson Road, close to Ubi and Paya Lebar.'),
    ('jalan-besar-kallang-bahru', 'Jalan Besar and Kallang Bahru', 'central', 1.3110, 103.8660, ['macpherson', 'toa-payoh', 'alexandra-bukit-merah'], ['19', '33', '34'], ['jalan besar', 'kallang'],
     'Jalan Besar and Kallang Bahru are central areas with a long history of motor trade units and workshops.'),
    ('alexandra-bukit-merah', 'Alexandra and Bukit Merah', 'central', 1.2860, 103.8130, ['jalan-besar-kallang-bahru', 'toa-payoh'], ['14', '15', '16'], ['alexandra', 'bukit merah', 'henderson'],
     'Alexandra and Bukit Merah cover the south side of the Central region, around Alexandra Road, Bukit Merah and Henderson.'),
    # ---- West
    ('toh-guan-jurong-east', 'Toh Guan and Jurong East', 'west', 1.3340, 103.7430, ['jurong-west', 'bukit-batok', 'pandan-loop'], ['60', '61'], ['toh guan', 'jurong east', 'enterprise hub'],
     'Toh Guan and Jurong East are in the West region, around Toh Guan Road East and the Enterprise Hub industrial building.'),
    ('jurong-west', 'Jurong West', 'west', 1.3400, 103.7050, ['toh-guan-jurong-east', 'tuas', 'bukit-batok'], ['64'], ['jurong west'],
     'Jurong West is a large area in the West region with industrial units alongside housing estates.'),
    ('pandan-loop', 'Pandan Loop', 'west', 1.3150, 103.7500, ['toh-guan-jurong-east', 'bukit-batok'], ['12'], ['pandan'],
     'Pandan Loop is a small industrial area in the West region, near Clementi and Jurong East.'),
    ('bukit-batok', 'Bukit Batok', 'west', 1.3560, 103.7520, ['toh-guan-jurong-east', 'jurong-west', 'pandan-loop'], ['65', '66'], ['bukit batok'],
     'Bukit Batok has industrial parks in the West region, including Bukit Batok Industrial Park A.'),
    ('tuas', 'Tuas', 'west', 1.3000, 103.6400, ['jurong-west'], ['63'], ['tuas'],
     'Tuas is the industrial area at the far west of Singapore, around Tuas Avenue and Tuas South.'),
]

# Town hubs (the old "estate clusters"): /areas/<town>/ lists the industrial estates in that town. Navigation, not a listing page.
TOWNS = {}
for _s, _n, _r, _la, _lo, _nb, _pre, _kw, _intro in _E:
    TOWNS[_s] = dict(slug=_s, name=_n, region=_r, lat=_la, lon=_lo, nearby=_nb, intro=_intro)

# Industrial estates (Edwin 3 Nov 2026): the area unit, /areas/<industrial-estate>/. slug, name, town, address keywords, intro.
# An address matches an estate by keyword (first match wins). If a new workshop matches none, add its estate here.
_IE = [
    ('amk-industrial-park-2', 'Ang Mo Kio Industrial Park 2', 'ang-mo-kio', ['ang mo kio industrial park'],
     'Ang Mo Kio Industrial Park 2 is an industrial estate in Ang Mo Kio, including the AMK AutoPoint motor building, with workshops serving the north-east.'),
    ('kaki-bukit-industrial-estate', 'Kaki Bukit Industrial Estate', 'kaki-bukit', ['kaki bukit'],
     'Kaki Bukit is an industrial estate in the East region, around Kaki Bukit Avenue 4 and 6 and Kaki Bukit Road 2 and 4, with many workshops, trade units and parts suppliers.'),
    ('sin-ming-industrial-estate', 'Sin Ming Industrial Estate', 'sin-ming-bishan', ['sin ming'],
     'Sin Ming Industrial Estate, including Sin Ming Drive and the Sin Ming AutoCity and Autocare buildings, is in the middle of Singapore near Bishan.'),
    ('toh-guan-enterprise-hub', 'Toh Guan Road East and Enterprise Hub', 'toh-guan-jurong-east', ['toh guan'],
     'Toh Guan Road East and the Enterprise Hub industrial building are in the West region, near Jurong East.'),
    ('corporation-drive-jurong-east', 'Corporation Drive, Jurong East', 'toh-guan-jurong-east', ['corporation dr'],
     'Corporation Drive is an industrial road in Jurong East, in the West region.'),
    ('paya-ubi-industrial-park', 'Paya Ubi Industrial Park', 'ubi', ['ubi ave 1', 'paya ubi'],
     'Paya Ubi Industrial Park is around Ubi Avenue 1, near Paya Lebar in the Geylang planning area (Central region), with motor workshops mixed in among light industry.'),
    ('ubi-road-1', 'Ubi Road 1', 'ubi', ['ubi rd 1', 'ubi road 1'],
     'Ubi Road 1 is an industrial road in the Ubi area, near Paya Lebar in the Geylang planning area (Central region).'),
    ('bedok-industrial-park-e', 'Bedok Industrial Park E', 'bedok-north', ['bedok industrial park e', 'bedok ind park e'],
     'Bedok Industrial Park E is a block of trade units along Bedok North Avenue 4 in the East region, near Bedok Reservoir and Tampines.'),
    ('tampines-industrial-park-a', 'Tampines Industrial Park A', 'tampines', ['tampines industrial park a'],
     'Tampines Industrial Park A is a light industrial estate along Tampines Street 92 and 93 in the East region.'),
    ('woodlands-industrial-park-e9', 'Woodlands Industrial Park E9', 'woodlands', ['woodlands industrial park'],
     'Woodlands Industrial Park E9 is the main industrial park in the north-west, close to the Causeway.'),
    ('carros-centre-jalan-lam-huat', 'Jalan Lam Huat and Carros Centre', 'woodlands', ['jln lam huat', 'jalan lam huat', 'carros'],
     'Jalan Lam Huat, where Carros Centre stands, is an industrial road in the north-west of Singapore.'),
    ('woodlands-avenue-12', 'Woodlands Avenue 12 (Polaris@Woodlands)', 'woodlands', ['woodlands ave 12', 'polaris'],
     'Woodlands Avenue 12 and the Polaris@Woodlands industrial building are in the Woodlands area in the north.'),
    ('yishun-industrial-park-a', 'Yishun Industrial Park A', 'yishun', ['yishun industrial park'],
     'Yishun Industrial Park A is one of the two main motor trade clusters in Yishun, in the North region.'),
    ('yishun-industrial-street-1', 'Yishun Industrial Street 1', 'yishun', ['yishun industrial street', 'yishun industrial st'],
     'Yishun Industrial Street 1, around North Spring Bizhub and Northpoint Bizhub, is the second motor trade cluster in Yishun.'),
    ('bukit-batok-crescent', 'Bukit Batok Crescent (WCEGA Plaza)', 'bukit-batok', ['bukit batok cres', 'bukit batok crescent', 'wcega'],
     'Bukit Batok Crescent, home to the WCEGA Plaza and WCEGA Tower industrial buildings, is a light industrial area in the West region.'),
    ('woodlands-close', 'Woodlands Close (MEGA@Woodlands)', 'woodlands', ['woodlands cl', 'woodlands close', 'mega@woodland'],
     'Woodlands Close, where the MEGA@Woodlands industrial building stands, is a light industrial area in the north, near Woodlands Avenue 12.'),
]
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
