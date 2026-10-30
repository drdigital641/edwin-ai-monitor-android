"""Partware Auto catalogue definitions (brand, models, part groups, part types, sample prices).

Everything here is DEMO structure for the preview. Model names, generation codes and years are public
facts about the cars; WHICH parts Partware Auto stocks, their part numbers, grades and prices are NOT confirmed yet.
Every product is marked sample=True until staff confirm it in the dashboard (or catalogue.json).
Groups (CATS) are Partware Auto's own five Facebook product groups.
"""

BRANDS = [
    ("honda", "Honda"),
]

# id, brand, name, generation code, years, aliases (what owners type), fuel, tier (sample price factor)
MODELS = [
    ("civic-fd", "honda", "Civic", "FD", "2006-2011", ["civic fd", "civic 1.8", "civic 8th gen"], "petrol", 0.9),
    ("civic-fb", "honda", "Civic", "FB", "2012-2015", ["civic fb", "civic 1.8 fb"], "petrol", 0.95),
    ("civic-fc", "honda", "Civic", "FC", "2016-2021", ["civic fc", "civic turbo", "civic 1.5 turbo", "civic fk"], "petrol", 1.2),
    ("civic-fe", "honda", "Civic", "FE", "2022-now", ["civic fe", "new civic", "civic 11th gen"], "petrol", 1.4),
    ("jazz-ge", "honda", "Jazz / Fit", "GE", "2008-2014", ["jazz", "fit", "jazz ge", "fit ge", "honda fit"], "petrol", 0.8),
    ("jazz-gk", "honda", "Jazz / Fit", "GK", "2014-2020", ["jazz", "fit", "jazz gk", "fit gk", "fit hybrid", "jazz hybrid", "honda fit"], "petrol / hybrid", 0.95),
    ("city-gm", "honda", "City", "GM", "2009-2014", ["city gm", "honda city"], "petrol", 0.8),
    ("city-gn", "honda", "City", "GN", "2020-now", ["city gn", "new city", "honda city"], "petrol", 1.0),
    ("vezel-ru", "honda", "Vezel / HR-V", "RU", "2014-2021", ["vezel", "hrv", "hr-v", "vezel hybrid", "hrv hybrid", "vezel ru", "hrv ru"], "hybrid", 1.15),
    ("vezel-rv", "honda", "Vezel / HR-V", "RV", "2021-now", ["vezel", "hrv", "hr-v", "new vezel", "new hrv", "vezel hybrid", "hrv hybrid", "vezel rv", "hrv rv", "ehev"], "hybrid", 1.35),
    ("crv-rm", "honda", "CR-V", "RM", "2012-2016", ["crv", "cr v", "crv rm", "cr-v rm"], "petrol", 1.1),
    ("crv-rw", "honda", "CR-V", "RW", "2017-2022", ["crv", "cr v", "crv rw", "cr-v rw", "crv turbo"], "petrol", 1.3),
    ("odyssey-rb", "honda", "Odyssey", "RB", "2003-2013", ["odyssey rb", "odessey", "oddysey"], "petrol", 1.05),
    ("odyssey-rc", "honda", "Odyssey", "RC", "2014-2021", ["odyssey rc", "odessey", "odyssey hybrid", "oddysey"], "petrol / hybrid", 1.3),
    ("shuttle", "honda", "Shuttle", "GP7 / GK8", "2015-2022", ["fit shuttle", "shuttle hybrid", "shuttle gp7", "shuttle gk8", "gp7", "gk8"], "petrol / hybrid", 1.0),
    ("freed-gb3", "honda", "Freed", "GB3", "2008-2016", ["freed gb3", "freed gb4", "freed+", "honda freed"], "petrol", 0.95),
    ("freed-gb5", "honda", "Freed", "GB5", "2016-2024", ["freed gb5", "freed gb6", "freed gb7", "freed hybrid", "freed+", "honda freed"], "petrol / hybrid", 1.15),
    ("stepwgn-rp", "honda", "Stepwgn", "RP", "2015-now", ["step wgn", "step wagon", "stepwagon", "stepwgn rp", "stepwgn hybrid"], "petrol / hybrid", 1.3),
    ("accord-cr", "honda", "Accord", "CR", "2013-2018", ["accord cr", "accord 9th gen", "accord hybrid"], "petrol / hybrid", 1.15),
    ("accord-cv", "honda", "Accord", "CV", "2018-2022", ["accord cv", "accord 10th gen", "accord turbo"], "petrol / hybrid", 1.35),
    ("insight-ze", "honda", "Insight", "ZE", "2009-2014", ["insight ze", "insight hybrid"], "hybrid", 0.95),
    ("stream-rn", "honda", "Stream", "RN", "2006-2014", ["stream rn", "honda stream"], "petrol", 0.9),
]

# The five Partware Auto product groups: id, name, short line, icon key
CATS = [
    ("servicing-essentials", "Servicing Essentials", "Filters, spark plugs and wiper blades", "service"),
    ("engine-parts", "Engine Parts", "Ignition coils, mountings, pumps, belts and radiators", "engine"),
    ("body-parts", "Body Parts", "Bumpers, lamps, mirrors and bonnets", "body"),
    ("undercarriage-parts", "Undercarriage Parts", "Brakes, shock absorbers, arms, links and CV joints", "under"),
    ("interior-parts", "Interior Parts", "Window switches, regulators and blower motors", "interior"),
]

# id, cat, name, aliases (what owners type), side option, unit, base sample price S$, needs (fuel rule)
#   needs: "ice" = has a petrol engine (hybrids too), "petrol" = spark ignition (hybrids too), "any" = every model
PARTS = [
    ("oil-filter", "servicing-essentials", "Oil Filter", ["oil filter", "engine oil filter"], False, "piece", 12, "ice"),
    ("air-filter", "servicing-essentials", "Engine Air Filter", ["air filter", "engine air filter", "air cleaner", "engine filter"], False, "piece", 25, "ice"),
    ("cabin-filter", "servicing-essentials", "Cabin Filter", ["cabin filter", "cabin air filter", "aircon filter", "pollen filter", "ac filter"], False, "piece", 22, "any"),
    ("spark-plugs", "servicing-essentials", "Spark Plugs", ["spark plug", "spark plugs", "plugs", "plug", "sparkplug"], False, "set of 4", 48, "petrol"),
    ("wiper-blades", "servicing-essentials", "Wiper Blades", ["wiper", "wipers", "wiper blade", "wiper blades"], False, "set (front pair)", 28, "any"),
    ("ignition-coil", "engine-parts", "Ignition Coil", ["ignition coil", "coil", "coil pack", "plug coil"], False, "piece", 65, "petrol"),
    ("engine-mount", "engine-parts", "Engine Mounting", ["engine mount", "engine mounting", "mounting", "engine support", "gearbox mount"], False, "piece", 85, "ice"),
    ("water-pump", "engine-parts", "Water Pump", ["water pump", "coolant pump"], False, "piece", 75, "ice"),
    ("drive-belt", "engine-parts", "Timing / Drive Belt", ["timing belt", "drive belt", "fan belt", "serpentine belt", "alternator belt", "belt"], False, "piece", 40, "ice"),
    ("radiator", "engine-parts", "Radiator", ["radiator", "cooling radiator"], False, "piece", 180, "any"),
    ("front-bumper", "body-parts", "Front Bumper", ["front bumper", "bumper", "bumper cover", "front bumper cover"], False, "piece", 220, "any"),
    ("rear-bumper", "body-parts", "Rear Bumper", ["rear bumper", "back bumper", "bumper", "rear bumper cover"], False, "piece", 210, "any"),
    ("headlamp", "body-parts", "Headlamp", ["headlamp", "headlight", "head lamp", "head light", "front light"], True, "piece", 340, "any"),
    ("tail-lamp", "body-parts", "Tail Lamp", ["tail lamp", "taillight", "tail light", "rear lamp", "back light", "brake light"], True, "piece", 200, "any"),
    ("side-mirror", "body-parts", "Side Mirror", ["side mirror", "wing mirror", "door mirror", "mirror"], True, "piece", 160, "any"),
    ("bonnet", "body-parts", "Bonnet", ["bonnet", "hood", "engine hood"], False, "piece", 280, "any"),
    ("front-brake-pads", "undercarriage-parts", "Front Brake Pads", ["brake pads", "brake pad", "front pads", "front brake pad"], False, "set (one axle)", 55, "any"),
    ("rear-brake-pads", "undercarriage-parts", "Rear Brake Pads", ["brake pads", "brake pad", "rear pads", "rear brake pad", "back brake pad"], False, "set (one axle)", 50, "any"),
    ("front-brake-discs", "undercarriage-parts", "Front Brake Discs", ["brake disc", "brake discs", "rotor", "rotors", "brake rotor", "disc rotor", "disk"], False, "pair", 115, "any"),
    ("rear-brake-discs", "undercarriage-parts", "Rear Brake Discs", ["brake disc", "brake discs", "rotor", "rotors", "brake rotor", "disc rotor", "disk"], False, "pair", 100, "any"),
    ("front-shock-absorber", "undercarriage-parts", "Front Shock Absorber", ["shock absorber", "absorber", "shock", "strut", "front absorber"], True, "piece", 125, "any"),
    ("rear-shock-absorber", "undercarriage-parts", "Rear Shock Absorber", ["shock absorber", "absorber", "shock", "rear absorber"], True, "piece", 105, "any"),
    ("lower-control-arm", "undercarriage-parts", "Front Lower Control Arm", ["control arm", "lower arm", "wishbone", "lower control arm"], True, "piece", 95, "any"),
    ("stabiliser-link", "undercarriage-parts", "Stabiliser Link", ["stabiliser link", "stabilizer link", "sway bar link", "anti roll bar link"], True, "piece", 32, "any"),
    ("cv-joint", "undercarriage-parts", "CV Joint (Drive Shaft)", ["cv joint", "cv", "drive shaft", "driveshaft", "axle shaft"], True, "piece", 110, "any"),
    ("power-window-switch", "interior-parts", "Power Window Switch", ["power window switch", "window switch", "window button", "master switch"], False, "piece", 55, "any"),
    ("window-regulator", "interior-parts", "Window Regulator", ["window regulator", "regulator", "window motor", "window lifter"], True, "piece", 90, "any"),
    ("blower-motor", "interior-parts", "Aircon Blower Motor", ["blower motor", "aircon blower", "ac blower", "blower fan", "heater blower", "blower"], False, "piece", 95, "any"),
]

GRADES = ["Genuine", "OEM", "Aftermarket"]  # grade OPTIONS to ask about; none is claimed as stocked


# Honda engines here are all petrol or petrol-hybrid; there is no electric model, but the rule is kept for future additions.
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
