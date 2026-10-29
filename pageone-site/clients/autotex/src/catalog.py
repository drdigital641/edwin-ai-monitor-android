"""Autotex catalogue definitions (brands, models, part types, sample prices).

Everything here is DEMO structure for the preview. Model names, generation codes and years are public
facts about the cars; WHICH parts Autotex stocks, their part numbers and prices are NOT confirmed yet.
Every product is marked sample=True until staff confirm it in the dashboard (or catalogue.json).
"""

BRANDS = [
    ("hyundai", "Hyundai"),
    ("kia", "Kia"),
]

# id, brand, name, generation code, years, aliases (what owners type), fuel, tier (price factor)
MODELS = [
    ("avante-ad", "hyundai", "Avante", "AD", "2016-2020", ["elantra", "avante ad", "elantra ad"], "petrol", 1.0),
    ("avante-cn7", "hyundai", "Avante", "CN7", "2020-now", ["elantra", "avante cn7", "elantra cn7", "new avante"], "petrol", 1.05),
    ("i30-pd", "hyundai", "i30", "PD", "2017-2020", ["i30 hatchback", "i 30"], "petrol", 1.0),
    ("ioniq-ae", "hyundai", "Ioniq Hybrid", "AE", "2016-2022", ["ioniq", "ionic", "ioniq hybrid"], "hybrid", 1.1),
    ("ioniq-5", "hyundai", "Ioniq 5", "NE", "2021-now", ["ioniq5", "ionic 5", "ioniq 5 ev"], "electric", 1.35),
    ("kona-os", "hyundai", "Kona", "OS", "2017-2023", ["kona electric", "kona ev", "kona hybrid"], "petrol / hybrid / electric", 1.1),
    ("tucson-tl", "hyundai", "Tucson", "TL", "2015-2020", ["tuscon", "tucson tl"], "petrol / diesel", 1.15),
    ("tucson-nx4", "hyundai", "Tucson", "NX4", "2021-now", ["tuscon", "new tucson", "tucson hybrid"], "petrol / hybrid", 1.25),
    ("santa-fe-tm", "hyundai", "Santa Fe", "TM", "2018-2023", ["santafe", "santa fe"], "petrol / diesel", 1.3),
    ("starex-tq", "hyundai", "Starex / H-1", "TQ", "2007-2021", ["h1", "h-1", "grand starex", "starex van"], "diesel", 1.2),
    ("cerato-yd", "kia", "Cerato K3", "YD", "2013-2018", ["k3", "forte", "cerato forte", "cerato k3"], "petrol", 0.95),
    ("cerato-bd", "kia", "Cerato K3", "BD", "2018-now", ["k3", "forte", "new cerato", "cerato bd"], "petrol", 1.0),
    ("picanto-ja", "kia", "Picanto", "JA", "2017-now", ["morning", "picanto ja"], "petrol", 0.85),
    ("sportage-ql", "kia", "Sportage", "QL", "2016-2021", ["sportage ql"], "petrol / diesel", 1.15),
    ("sportage-nq5", "kia", "Sportage", "NQ5", "2022-now", ["new sportage", "sportage hybrid"], "petrol / hybrid", 1.25),
    ("sorento-um", "kia", "Sorento", "UM", "2015-2020", ["sorento um"], "petrol / diesel", 1.3),
    ("niro-de", "kia", "Niro", "DE", "2016-2022", ["niro hybrid", "niro ev", "e-niro"], "hybrid / electric", 1.1),
    ("ev6", "kia", "EV6", "CV", "2021-now", ["ev 6", "kia ev6"], "electric", 1.35),
    ("carens-rp", "kia", "Carens", "RP", "2013-2019", ["carens rp", "rondo"], "petrol", 1.05),
    ("optima-jf", "kia", "Optima K5", "JF", "2015-2020", ["k5", "optima k5"], "petrol", 1.1),
]

# id, name, short line, icon key
CATS = [
    ("body-parts", "Body Parts", "Bumpers, bonnets and mirrors", "body"),
    ("lamps", "Headlamps & Tail Lamps", "Front and rear lamp units", "lamp"),
    ("brake-pads", "Brake Pads", "Front and rear pad sets", "pad"),
    ("brake-discs", "Brake Discs (Rotors)", "Front discs, sold in pairs", "disc"),
    ("suspension", "Suspension", "Absorbers, arms and links", "susp"),
    ("engine-mounting", "Engine Mounting", "Engine and gearbox mounts", "mount"),
    ("spark-plugs", "Spark Plugs", "Plug sets for petrol engines", "plug"),
    ("ignition-coils", "Ignition Coils", "Coil packs per cylinder", "coil"),
    ("engine-parts", "Engine Parts", "Filters and service parts", "engine"),
]

# id, cat, name, aliases (what owners type), side option, unit, base sample price S$, needs (fuel rule)
#   needs: "ice" = has a petrol/diesel engine, "petrol" = spark ignition only, "any" = every model
PARTS = [
    ("front-bumper", "body-parts", "Front Bumper", ["front bumper", "bumper", "bumper cover", "front bumper cover"], False, "piece", 180, "any"),
    ("rear-bumper", "body-parts", "Rear Bumper", ["rear bumper", "back bumper", "bumper"], False, "piece", 170, "any"),
    ("bonnet", "body-parts", "Bonnet", ["bonnet", "hood", "engine hood"], False, "piece", 260, "any"),
    ("side-mirror", "body-parts", "Side Mirror", ["side mirror", "wing mirror", "door mirror", "mirror"], True, "piece", 150, "any"),
    ("headlamp", "lamps", "Headlamp", ["headlamp", "headlight", "head lamp", "head light", "front light"], True, "piece", 320, "any"),
    ("tail-lamp", "lamps", "Tail Lamp", ["tail lamp", "taillight", "tail light", "rear lamp", "back light", "brake light"], True, "piece", 190, "any"),
    ("front-brake-pads", "brake-pads", "Front Brake Pads", ["brake pads", "brake pad", "front pads", "front brake pad"], False, "set (one axle)", 55, "any"),
    ("rear-brake-pads", "brake-pads", "Rear Brake Pads", ["brake pads", "brake pad", "rear pads", "rear brake pad", "back brake pad"], False, "set (one axle)", 50, "any"),
    ("front-brake-discs", "brake-discs", "Front Brake Discs", ["brake disc", "brake discs", "rotor", "rotors", "brake rotor", "disc rotor", "disk"], False, "pair", 110, "any"),
    ("front-shock-absorber", "suspension", "Front Shock Absorber", ["shock absorber", "absorber", "shock", "strut", "front absorber"], True, "piece", 120, "any"),
    ("lower-control-arm", "suspension", "Front Lower Control Arm", ["control arm", "lower arm", "wishbone", "lower control arm"], True, "piece", 95, "any"),
    ("stabilizer-link", "suspension", "Front Stabilizer Link", ["stabilizer link", "stabiliser link", "sway bar link", "anti roll bar link", "link"], True, "piece", 35, "any"),
    ("engine-mount", "engine-mounting", "Engine Mounting", ["engine mount", "engine mounting", "mounting", "engine support"], False, "piece", 85, "ice"),
    ("gearbox-mount", "engine-mounting", "Gearbox Mounting", ["gearbox mount", "transmission mount", "gearbox mounting", "mounting"], False, "piece", 75, "ice"),
    ("spark-plugs", "spark-plugs", "Spark Plugs", ["spark plug", "spark plugs", "plugs", "plug"], False, "set of 4", 48, "petrol"),
    ("ignition-coil", "ignition-coils", "Ignition Coil", ["ignition coil", "coil", "coil pack", "plug coil"], False, "piece", 65, "petrol"),
    ("oil-filter", "engine-parts", "Oil Filter", ["oil filter", "engine oil filter", "filter"], False, "piece", 12, "ice"),
    ("air-filter", "engine-parts", "Engine Air Filter", ["air filter", "engine filter", "air cleaner", "filter"], False, "piece", 22, "ice"),
]

# EVs have no engine parts; diesel-only models have no spark plugs or ignition coils.
def fits(model, part):
    fuel = model[6]
    need = part[7]
    if need == "any":
        return True
    if fuel == "electric":
        return False
    if need == "petrol":
        return "petrol" in fuel or "hybrid" in fuel
    return True  # "ice": anything with an engine


def sample_price(model, part):
    """Clearly fake demo price: base x model tier, rounded to the nearest S$5 (S$1 under S$30)."""
    v = part[6] * model[7]
    return round(v) if v < 30 else int(5 * round(v / 5))
