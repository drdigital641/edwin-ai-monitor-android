"""Rough Singapore stockist price estimates (S$, parts only, OEM-quality) used ONLY to pre-fill the
staff "Add prices" tab. Staff check each one before saving; nothing here is shown on the shop.
BASE is for a mid-size car (Avante / Cerato class); per-car factors scale it."""
BASE = {  # part id: S$ per unit in catalog.py (side parts are per side). Revised 31 Oct 2026 (Edwin):
    # service items at or just under Singapore genuine retail (autopartsdirect.com.sg, Oct 2026: oil filter S$9-16,
    # air filter S$18-34, cabin filter S$20-38, spark plug S$9-27 each, brake pads S$74-149, engine mounts S$69-172);
    # body parts and lamps raised towards typical Singapore stockist prices.
    "front-bumper": 320, "rear-bumper": 300, "bonnet": 420, "front-grille": 180, "front-fender": 180,
    "side-mirror": 260, "wiper-blades": 25, "headlamp": 520, "tail-lamp": 260, "fog-lamp": 90,
    "front-brake-pads": 95, "rear-brake-pads": 70, "front-brake-discs": 160, "rear-brake-discs": 140,
    "front-shock-absorber": 170, "rear-shock-absorber": 130, "lower-control-arm": 140, "stabilizer-link": 45,
    "tie-rod-end": 55, "wheel-bearing": 160, "engine-mount": 100, "gearbox-mount": 90, "spark-plugs": 42,
    "ignition-coil": 75, "oil-filter": 8, "air-filter": 18, "drive-belt": 40, "water-pump": 140,
    "thermostat": 55, "radiator": 260, "radiator-fan": 280, "aircon-compressor": 650, "aircon-condenser": 240,
    "cabin-filter": 22, "alternator": 420, "starter-motor": 340,
    # added 31 Oct 2026 for the service kits and sets (ATF S$44 vs S$46 genuine 4 L at autopartsdirect.com.sg)
    "engine-oil": 55, "transmission-oil": 44, "strut-top-mount": 60, "strut-bearing": 28, "control-arm-bush": 28,
    "steering-rack": 650, "radiator-cap": 15, "thermostat-housing": 45, "upper-radiator-hose": 35, "lower-radiator-hose": 40,
    "rear-bump-stop": 25, "rear-top-mount": 45,
}
LOOKS = {"body-parts", "lamps"}  # categories scaled by the body/lamp factor
SIZE = {  # (body/lamp factor, mechanical factor)
    "small": (0.8, 0.85), "mid": (1.0, 1.0), "large": (1.25, 1.15), "xl": (1.45, 1.3)}
CAR_SIZE = {
    "small": "picanto-ja picanto-ta rio-yb stonic-yb inster venue-qx",
    "mid": "avante-ad avante-cn7 cerato-bd cerato-yd i30-pd veloster-fs ioniq-ae kona-os kona-sx2 niro-de niro-sg2 seltos-sp2 carens-rp ev3 soul-sk3 ev4",
    "large": "optima-jf k5-dl3 sonata-lf sonata-dn8 i40-vf tucson-tl tucson-nx4 sportage-ql sportage-nq5 ioniq-5 ioniq-6 ev6 ev5 stinger-ck avante-n i30-n",
    "xl": "santa-fe-dm santa-fe-tm santa-fe-mx5 sorento-um sorento-mq4 carnival-yp carnival-ka4 starex-tq staria-us4 ev9 ioniq-9 pv5",
}
SIZE_OF = {k: s for s, ks in CAR_SIZE.items() for k in ks.split()}

def car_factors(car):
    """(body/lamp factor, mechanical factor) for a car row from cars.json."""
    b, m = SIZE[SIZE_OF.get(car["key"], "mid")]
    start = int((car.get("years") or "2016")[:4])
    if start >= 2020: b *= 1.2           # newer LED lamps and sensor bumpers cost more
    if car.get("fuel") == "electric": b *= 1.1
    return round(b, 3), round(m, 3)

def rnd(v):
    return int(round(v)) if v < 30 else int(5 * round(v / 5)) if v < 100 else int(10 * round(v / 10))
