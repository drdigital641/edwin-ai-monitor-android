"""Autotex catalogue definitions: brands, categories and part types.

Models (cars) and products come from the database (src/db/cars.json and src/db/products.json, raw API rows).
This file only defines the part TYPES Autotex supplies and the brands. No prices here.
"""

BRANDS = [
    ("hyundai", "Hyundai"),
    ("kia", "Kia"),
]

# id, name, short line, icon key
CATS = [
    ("body-parts", "Body Parts", "Bumpers, bonnets, grilles, mirrors and wipers", "body"),
    ("lamps", "Headlamps & Tail Lamps", "Head, tail and fog lamp units", "lamp"),
    ("brake-pads", "Brake Pads", "Front and rear pad sets", "pad"),
    ("brake-discs", "Brake Discs (Rotors)", "Front and rear discs, sold in pairs", "disc"),
    ("suspension", "Suspension & Steering", "Absorbers, arms, links, tie rods and bearings", "susp"),
    ("engine-mounting", "Engine Mounting", "Engine and gearbox mounts", "mount"),
    ("spark-plugs", "Spark Plugs", "Plug sets for petrol engines", "plug"),
    ("ignition-coils", "Ignition Coils", "Coil packs per cylinder", "coil"),
    ("engine-parts", "Engine Parts", "Filters, belts, pumps and service parts", "engine"),
    ("cooling-aircon", "Cooling & Aircon", "Radiators, fans and aircon parts", "fan"),
    ("electrical", "Starting & Charging", "Alternators and starter motors", "bolt"),
    ("oils-fluids", "Oils & Fluids", "Engine oil and transmission oil (ATF)", "engine"),
]

# id, cat, name, aliases (what owners type), side option, unit, needs (fuel rule)
#   needs: "ice" = has a petrol/diesel engine, "petrol" = spark ignition only, "any" = every model
PARTS = [
    ('front-bumper', 'body-parts', 'Front Bumper', ['front bumper', 'bumper', 'bumper cover', 'front bumper cover'], False, 'piece', 'any'),
    ('rear-bumper', 'body-parts', 'Rear Bumper', ['rear bumper', 'back bumper', 'bumper'], False, 'piece', 'any'),
    ('bonnet', 'body-parts', 'Bonnet', ['bonnet', 'hood', 'engine hood'], False, 'piece', 'any'),
    ('front-grille', 'body-parts', 'Front Grille', ['grille', 'front grille', 'grill', 'radiator grille'], False, 'piece', 'any'),
    ('front-fender', 'body-parts', 'Front Fender', ['fender', 'front fender', 'wing', 'front wing', 'side panel'], True, 'piece', 'any'),
    ('side-mirror', 'body-parts', 'Side Mirror', ['side mirror', 'wing mirror', 'door mirror', 'mirror'], True, 'piece', 'any'),
    ('wiper-blades', 'body-parts', 'Wiper Blades', ['wiper', 'wipers', 'wiper blade', 'wiper blades', 'windscreen wiper'], False, 'set (front pair)', 'any'),
    ('headlamp', 'lamps', 'Headlamp', ['headlamp', 'headlight', 'head lamp', 'head light', 'front light'], True, 'piece', 'any'),
    ('tail-lamp', 'lamps', 'Tail Lamp', ['tail lamp', 'taillight', 'tail light', 'rear lamp', 'back light', 'brake light'], True, 'piece', 'any'),
    ('fog-lamp', 'lamps', 'Fog Lamp', ['fog lamp', 'fog light', 'foglamp', 'front fog lamp'], True, 'piece', 'any'),
    ('front-brake-pads', 'brake-pads', 'Front Brake Pads', ['brake pads', 'brake pad', 'front pads', 'front brake pad'], False, 'set (one axle)', 'any'),
    ('rear-brake-pads', 'brake-pads', 'Rear Brake Pads', ['brake pads', 'brake pad', 'rear pads', 'rear brake pad', 'back brake pad'], False, 'set (one axle)', 'any'),
    ('front-brake-discs', 'brake-discs', 'Front Brake Discs', ['brake disc', 'brake discs', 'rotor', 'rotors', 'brake rotor', 'disc rotor', 'disk'], False, 'pair', 'any'),
    ('rear-brake-discs', 'brake-discs', 'Rear Brake Discs', ['rear disc', 'rear brake disc', 'rear rotor', 'rear rotors', 'back brake disc'], False, 'pair', 'any'),
    ('front-shock-absorber', 'suspension', 'Front Shock Absorber', ['shock absorber', 'absorber', 'shock', 'strut', 'front absorber'], True, 'piece', 'any'),
    ('rear-shock-absorber', 'suspension', 'Rear Shock Absorber', ['rear absorber', 'rear shock', 'rear shock absorber', 'back absorber'], True, 'piece', 'any'),
    ('lower-control-arm', 'suspension', 'Front Lower Control Arm', ['control arm', 'lower arm', 'wishbone', 'lower control arm'], True, 'piece', 'any'),
    ('stabilizer-link', 'suspension', 'Front Stabilizer Link', ['stabilizer link', 'stabiliser link', 'sway bar link', 'anti roll bar link', 'link'], True, 'piece', 'any'),
    ('tie-rod-end', 'suspension', 'Tie Rod End', ['tie rod', 'tie rod end', 'steering rod end', 'rack end'], True, 'piece', 'any'),
    ('wheel-bearing', 'suspension', 'Front Wheel Bearing', ['wheel bearing', 'bearing', 'hub bearing', 'wheel hub', 'front bearing'], True, 'piece', 'any'),
    ('engine-mount', 'engine-mounting', 'Engine Mounting', ['engine mount', 'engine mounting', 'mounting', 'engine support'], False, 'piece', 'ice'),
    ('gearbox-mount', 'engine-mounting', 'Gearbox Mounting', ['gearbox mount', 'transmission mount', 'gearbox mounting', 'mounting'], False, 'piece', 'ice'),
    ('spark-plugs', 'spark-plugs', 'Spark Plugs', ['spark plug', 'spark plugs', 'plugs', 'plug'], False, 'set of 4', 'petrol'),
    ('ignition-coil', 'ignition-coils', 'Ignition Coil', ['ignition coil', 'coil', 'coil pack', 'plug coil'], False, 'piece', 'petrol'),
    ('oil-filter', 'engine-parts', 'Oil Filter', ['oil filter', 'engine oil filter', 'filter'], False, 'piece', 'ice'),
    ('air-filter', 'engine-parts', 'Engine Air Filter', ['air filter', 'engine filter', 'air cleaner', 'filter'], False, 'piece', 'ice'),
    ('drive-belt', 'engine-parts', 'Drive Belt', ['fan belt', 'drive belt', 'alternator belt', 'aircon belt', 'belt'], False, 'piece', 'ice'),
    ('water-pump', 'engine-parts', 'Water Pump', ['water pump', 'coolant pump', 'pump'], False, 'piece', 'ice'),
    ('thermostat', 'engine-parts', 'Thermostat', ['thermostat', 'thermostat valve', 'coolant thermostat'], False, 'piece', 'ice'),
    ('radiator', 'cooling-aircon', 'Radiator', ['radiator', 'engine radiator', 'coolant radiator'], False, 'piece', 'ice'),
    ('radiator-fan', 'cooling-aircon', 'Radiator Fan', ['radiator fan', 'cooling fan', 'fan motor', 'engine fan'], False, 'piece', 'ice'),
    ('aircon-compressor', 'cooling-aircon', 'Aircon Compressor', ['aircon compressor', 'ac compressor', 'a/c compressor', 'compressor'], False, 'piece', 'any'),
    ('aircon-condenser', 'cooling-aircon', 'Aircon Condenser', ['condenser', 'aircon condenser', 'ac condenser', 'cooling coil'], False, 'piece', 'any'),
    ('cabin-filter', 'cooling-aircon', 'Cabin Air Filter', ['cabin filter', 'aircon filter', 'ac filter', 'pollen filter', 'cabin air filter'], False, 'piece', 'any'),
    ('alternator', 'electrical', 'Alternator', ['alternator', 'dynamo', 'charging'], False, 'piece', 'ice'),
    ('starter-motor', 'electrical', 'Starter Motor', ['starter', 'starter motor', 'self starter', 'starting motor'], False, 'piece', 'ice'),
    ('engine-oil', 'oils-fluids', 'Engine Oil (4 L)', ['engine oil', 'oil', 'motor oil', 'oil change', 'engine oil 4l'], False, '4 L bottle', 'ice'),
    ('transmission-oil', 'oils-fluids', 'Transmission Oil / ATF (4 L)', ['transmission oil', 'gearbox oil', 'atf', 'auto transmission fluid', 'gear oil', 'transmission fluid'], False, '4 L', 'ice'),
    ('strut-top-mount', 'suspension', 'Strut Top Mount', ['top mount', 'strut mount', 'absorber mount', 'top mounting', 'shock mount'], True, 'piece', 'any'),
    ('strut-bearing', 'suspension', 'Strut Top Bearing', ['top bearing', 'strut bearing', 'bearing stopper', 'absorber bearing', 'top bearing stopper'], True, 'piece', 'any'),
    ('control-arm-bush', 'suspension', 'Lower Arm Bush', ['bush', 'lower arm bush', 'control arm bush', 'arm bush', 'bushing'], True, 'piece', 'any'),
    ('steering-rack', 'suspension', 'Steering Rack', ['steering rack', 'rack', 'power steering rack', 'steering gear'], False, 'piece', 'any'),
    ('radiator-cap', 'cooling-aircon', 'Radiator Cap', ['radiator cap', 'coolant cap', 'pressure cap'], False, 'piece', 'ice'),
    ('thermostat-housing', 'cooling-aircon', 'Thermostat Housing (Outlet)', ['thermostat housing', 'thermostat outlet', 'water outlet', 'thermostat cover'], False, 'piece', 'ice'),
    ('upper-radiator-hose', 'cooling-aircon', 'Upper Radiator Hose', ['upper hose', 'radiator hose', 'top hose', 'upper radiator hose'], False, 'piece', 'ice'),
    ('lower-radiator-hose', 'cooling-aircon', 'Lower Radiator Hose', ['lower hose', 'radiator hose', 'bottom hose', 'lower radiator hose'], False, 'piece', 'ice'),
]

# EVs have no engine parts; diesel-only models have no spark plugs or ignition coils.
def fits(fuel, part):
    """True if the part type applies to a car with this fuel string (e.g. "petrol / hybrid")."""
    need = part[6]
    if need == "any":
        return True
    if fuel == "electric":
        return False
    if need == "petrol":
        return "petrol" in fuel or "hybrid" in fuel
    return True  # "ice": anything with an engine


# Service kits and repair sets (Edwin, 31 Oct 2026). Built per car from that car's listed parts.
# id, name, short line, included [(part id, qty)], optional add-ons [(part id, qty)]
# Parts that do not fit a car (e.g. spark plugs on a diesel) are left out for that car; sets with no fitting items are skipped.
SET_DISCOUNT = 0.05  # set price = included items minus 5%
BUNDLES = [
    ("minor-service-kit", "Minor Service Kit", "Engine oil, oil filter, aircon (cabin) filter and air filter",
     [("engine-oil", 1), ("oil-filter", 1), ("cabin-filter", 1), ("air-filter", 1)], []),
    ("major-service-kit", "Major Service Kit", "Engine oil, transmission oil, all filters and spark plugs",
     [("engine-oil", 1), ("transmission-oil", 1), ("oil-filter", 1), ("cabin-filter", 1), ("air-filter", 1), ("spark-plugs", 1)],
     [("drive-belt", 1), ("front-brake-pads", 1), ("ignition-coil", 4)]),
    ("front-suspension-set", "Front Suspension Set", "Absorbers, top mounts, top bearings, links, bushes and lower arms (both sides)",
     [("front-shock-absorber", 2), ("strut-top-mount", 2), ("strut-bearing", 2), ("stabilizer-link", 2), ("control-arm-bush", 2), ("lower-control-arm", 2)],
     [("steering-rack", 1)]),
    ("cooling-system-set", "Cooling System Set", "Radiator, cap, thermostat and outlet, hoses, water pump and fan motor",
     [("radiator", 1), ("radiator-cap", 1), ("thermostat", 1), ("thermostat-housing", 1), ("upper-radiator-hose", 1), ("lower-radiator-hose", 1), ("water-pump", 1), ("radiator-fan", 1)], []),
]
