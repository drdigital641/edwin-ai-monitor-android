"""Rough Singapore stockist price estimates (S$, parts only, OEM-quality) used ONLY to pre-fill the
staff "Add prices" tab. Staff check each one before saving; nothing here is shown on the shop.
BASE is for a mid-size car (Avante / Cerato class); per-car factors scale it."""
BASE = {  # part id: S$ per unit in catalog.py (side parts are per side)
    "front-bumper": 220, "rear-bumper": 200, "bonnet": 280, "front-grille": 150, "front-fender": 120,
    "side-mirror": 180, "wiper-blades": 25, "headlamp": 380, "tail-lamp": 180, "fog-lamp": 70,
    "front-brake-pads": 70, "rear-brake-pads": 60, "front-brake-discs": 140, "rear-brake-discs": 120,
    "front-shock-absorber": 150, "rear-shock-absorber": 110, "lower-control-arm": 110, "stabilizer-link": 40,
    "tie-rod-end": 45, "wheel-bearing": 120, "engine-mount": 120, "gearbox-mount": 100, "spark-plugs": 60,
    "ignition-coil": 70, "oil-filter": 12, "air-filter": 25, "drive-belt": 45, "water-pump": 150,
    "thermostat": 60, "radiator": 220, "radiator-fan": 250, "aircon-compressor": 550, "aircon-condenser": 200,
    "cabin-filter": 20, "alternator": 380, "starter-motor": 300,
}
LOOKS = {"body-parts", "lamps"}  # categories scaled by the body/lamp factor
SIZE = {  # (body/lamp factor, mechanical factor)
    "small": (0.8, 0.85), "mid": (1.0, 1.0), "large": (1.25, 1.15), "xl": (1.45, 1.3)}
CAR_SIZE = {
    "small": "picanto-ja picanto-ta rio-yb stonic-yb inster",
    "mid": "avante-ad avante-cn7 cerato-bd cerato-yd i30-pd veloster-fs ioniq-ae kona-os kona-sx2 niro-de niro-sg2 seltos-sp2 carens-rp ev3",
    "large": "optima-jf k5-dl3 sonata-lf sonata-dn8 i40-vf tucson-tl tucson-nx4 sportage-ql sportage-nq5 ioniq-5 ioniq-6 ev6 ev5",
    "xl": "santa-fe-dm santa-fe-tm santa-fe-mx5 sorento-um sorento-mq4 carnival-yp carnival-ka4 starex-tq staria-us4 ev9",
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
