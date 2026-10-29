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

# id, cat, name, aliases (what owners type), side option, unit, needs (fuel rule)
#   needs: "ice" = has a petrol/diesel engine, "petrol" = spark ignition only, "any" = every model
PARTS = [
    ('front-bumper', 'body-parts', 'Front Bumper', ['front bumper', 'bumper', 'bumper cover', 'front bumper cover'], False, 'piece', 'any'),
    ('rear-bumper', 'body-parts', 'Rear Bumper', ['rear bumper', 'back bumper', 'bumper'], False, 'piece', 'any'),
    ('bonnet', 'body-parts', 'Bonnet', ['bonnet', 'hood', 'engine hood'], False, 'piece', 'any'),
    ('side-mirror', 'body-parts', 'Side Mirror', ['side mirror', 'wing mirror', 'door mirror', 'mirror'], True, 'piece', 'any'),
    ('headlamp', 'lamps', 'Headlamp', ['headlamp', 'headlight', 'head lamp', 'head light', 'front light'], True, 'piece', 'any'),
    ('tail-lamp', 'lamps', 'Tail Lamp', ['tail lamp', 'taillight', 'tail light', 'rear lamp', 'back light', 'brake light'], True, 'piece', 'any'),
    ('front-brake-pads', 'brake-pads', 'Front Brake Pads', ['brake pads', 'brake pad', 'front pads', 'front brake pad'], False, 'set (one axle)', 'any'),
    ('rear-brake-pads', 'brake-pads', 'Rear Brake Pads', ['brake pads', 'brake pad', 'rear pads', 'rear brake pad', 'back brake pad'], False, 'set (one axle)', 'any'),
    ('front-brake-discs', 'brake-discs', 'Front Brake Discs', ['brake disc', 'brake discs', 'rotor', 'rotors', 'brake rotor', 'disc rotor', 'disk'], False, 'pair', 'any'),
    ('front-shock-absorber', 'suspension', 'Front Shock Absorber', ['shock absorber', 'absorber', 'shock', 'strut', 'front absorber'], True, 'piece', 'any'),
    ('lower-control-arm', 'suspension', 'Front Lower Control Arm', ['control arm', 'lower arm', 'wishbone', 'lower control arm'], True, 'piece', 'any'),
    ('stabilizer-link', 'suspension', 'Front Stabilizer Link', ['stabilizer link', 'stabiliser link', 'sway bar link', 'anti roll bar link', 'link'], True, 'piece', 'any'),
    ('engine-mount', 'engine-mounting', 'Engine Mounting', ['engine mount', 'engine mounting', 'mounting', 'engine support'], False, 'piece', 'ice'),
    ('gearbox-mount', 'engine-mounting', 'Gearbox Mounting', ['gearbox mount', 'transmission mount', 'gearbox mounting', 'mounting'], False, 'piece', 'ice'),
    ('spark-plugs', 'spark-plugs', 'Spark Plugs', ['spark plug', 'spark plugs', 'plugs', 'plug'], False, 'set of 4', 'petrol'),
    ('ignition-coil', 'ignition-coils', 'Ignition Coil', ['ignition coil', 'coil', 'coil pack', 'plug coil'], False, 'piece', 'petrol'),
    ('oil-filter', 'engine-parts', 'Oil Filter', ['oil filter', 'engine oil filter', 'filter'], False, 'piece', 'ice'),
    ('air-filter', 'engine-parts', 'Engine Air Filter', ['air filter', 'engine filter', 'air cleaner', 'filter'], False, 'piece', 'ice'),
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
