#!/usr/bin/env python3
"""EV Body Parts (evbodyparts.sg) - static site builder (31 Oct 2026).

Run:  python3 build.py /tmp/ev-site
Catalogue source: db/*.json = snapshot of the Base44 app "EV Body Parts Catalogue" (id 6ae5c57dbb2270677873e207):
EvBrand, EvCar, EvProduct (published only), EvPhoto chunks. See NIGHTLY-PUBLISH.md.
The browser reads the same database live (ev.js), so new products show at once; this build gives Google real pages.
"""
import html, json, sys, re, datetime, hashlib, shutil, base64
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent / "site")
if not OUT.is_absolute():
    OUT = Path.cwd() / OUT
import os
DB = Path(os.environ.get("EV_DB") or (HERE / "db"))

# ------------------------------------------------------------------ constants
BASE = "https://evbodyparts.sg"          # canonical host (live domain). Preview copy: https://pageonesingapore.com/preview/ev-body-parts/ (relative links)
WA = "6589976612"   # WhatsApp +65 8997 6612: the ONLY contact (Edwin, 31 Oct 2026). Empty = enquiry form.
WA_DISPLAY = "+65 8997 6612"
PHONE = ""     # no phone number (WhatsApp only)
EMAIL = ""     # e.g. hello@evbodyparts.sg
LEGAL = ""     # seller company name, not known yet
UEN = ""
ADDRESS = ""   # street address, not known yet
STAFF_URL = "https://ev-body-parts-catalogue-7873e207.base44.app/staff"   # Base44 staff dashboard (URL given by the API agent, 31 Oct 2026)
APP_ID = "6ae5c57dbb2270677873e207"
API_BASES = ["https://base44.app/api/apps/" + APP_ID, "https://ev-body-parts-catalogue-7873e207.base44.app/api/apps/" + APP_ID]
TODAY = datetime.date.today().isoformat()
BRAND = "EV Body Parts"
DOMAIN = "evbodyparts.sg"
TAG = "Body parts for China & EV cars in Singapore"
KEY = "f9badb093cb250f8b0a26711842f59f2"   # IndexNow key (random, new for this site)
e = lambda s: html.escape(str(s), quote=True)
CRED = "Stock photos: Unsplash"

# ------------------------------------------------------------------ photos (Unsplash, hotlinked, mood only)
PH = {
    "hero": "1642268565002-729f4e3dad5b", "matte": "1620891549027-942fdc95d3f5", "white": "1560958089-b8a1929cea89",
    "tail": "1725745096249-f6e7c160c4be", "taillit": "1518438223361-dde09dbeed6a", "head": "1531843256863-af93f4edfcfb",
    "charge": "1593941707874-ef25b8b4a92b", "showroom": "1666919643134-d97687c1826c", "wheel": "1572191267783-5618f992aff5",
    "door": "1615903214534-582a77a2a85e", "m3": "1648866892162-9336ef9182e2",
}
def purl(k, w): return f"https://images.unsplash.com/photo-{PH[k]}?auto=format&fit=crop&w={w}&q=70"
def pic(k, alt, w, h, sizes="100vw", eager=False, cls=""):
    ss = ", ".join(f"{purl(k, x)} {x}w" for x in (800, 1400, 2000))
    return (f'<img src="{purl(k, 1400)}" srcset="{ss}" sizes="{sizes}" alt="{e(alt)}" width="{w}" height="{h}" '
            f'{"" if eager else "loading=\"lazy\" "}decoding="async"{" fetchpriority=\"high\"" if eager else ""}{f" class=\"{cls}\"" if cls else ""} onerror="this.remove()">')

# ------------------------------------------------------------------ part types (not in the database: fixed vocabulary for search)
PARTS = [  # slug, name, category, synonyms (owner language)
    ("front-bumper", "Front Bumper", "bumpers", ["front bumper", "bumper front", "fbumper", "f bumper"]),
    ("rear-bumper", "Rear Bumper", "bumpers", ["rear bumper", "back bumper", "bumper rear", "bumper back", "r bumper"]),
    ("bumper-trim", "Bumper Trim", "bumpers", ["bumper trim", "bumper lip", "bumper strip", "bumper garnish", "sticker bumper", "bumper sticker", "bumper moulding", "bumper molding"]),
    ("headlamp", "Headlamp", "lamps-lights", ["headlamp", "headlight", "head lamp", "head light", "front light", "front lamp"]),
    ("tail-lamp", "Tail Lamp", "lamps-lights", ["tail lamp", "taillamp", "tail light", "taillight", "rear lamp", "rear light", "back light", "back lamp", "brake light", "tail"]),
    ("rear-reflector", "Rear Reflector", "lamps-lights", ["rear reflector", "reflector", "bumper reflector", "rear bumper reflector"]),
    ("fog-lamp", "Fog Lamp", "lamps-lights", ["fog lamp", "fog light", "foglamp", "foglight", "fog"]),
    ("side-mirror", "Side Mirror", "mirrors", ["side mirror", "wing mirror", "mirror cover", "mirror glass", "door mirror", "mirror"]),
    ("bonnet", "Bonnet", "body-panels", ["bonnet", "hood"]),
    ("fender", "Fender", "body-panels", ["fender", "front fender", "wing", "mudguard"]),
    ("door-panel", "Door Panel", "body-panels", ["door panel", "door shell", "door"]),
    ("tailgate", "Tailgate", "body-panels", ["tailgate", "boot", "boot lid", "trunk lid", "trunk", "liftgate"]),
    ("grille", "Grille", "grilles-trims", ["grille", "grill", "front grille", "front grill"]),
    ("wheel-arch", "Wheel Arch", "grilles-trims", ["wheel arch", "arch lining", "arch liner", "fender liner", "wheel arch liner"]),
    ("front-bumper-bracket", "Front Bumper Bracket", "bumpers", ["front bumper bracket", "bumper bracket", "bumper guide", "bumper support", "bumper slide bracket", "bumper mounting bracket"]),
    ("rear-bumper-bracket", "Rear Bumper Bracket", "bumpers", ["rear bumper bracket", "rear bumper guide", "rear bumper support"]),
    ("bumper-reinforcement", "Bumper Reinforcement", "bumpers", ["bumper reinforcement", "bumper beam", "crash beam", "impact bar", "reinforcement bar", "bumper bar"]),
    ("front-lip", "Front Lip / Valance", "bumpers", ["front lip", "bumper lip front", "splitter", "front valance", "chin spoiler", "front spoiler", "lip"]),
    ("rear-diffuser", "Rear Diffuser / Lower Valance", "bumpers", ["rear diffuser", "diffuser", "rear valance", "rear lower valance", "rear lip"]),
    ("lower-grille", "Lower Grille", "grilles-trims", ["lower grille", "lower grill", "air intake", "intake trim", "bumper grille", "bumper grill", "bumper mesh"]),
    ("undertray", "Undertray / Lower Guard", "grilles-trims", ["undertray", "under tray", "lower guard", "splash shield", "under cover", "undercover", "belly pan", "engine undercover"]),
    ("bonnet-hinge", "Bonnet Hinge / Latch", "body-panels", ["bonnet hinge", "hood hinge", "bonnet latch", "hood latch", "bonnet lock", "striker"]),
    ("headlamp-bracket", "Headlamp Bracket", "lamps-lights", ["headlamp bracket", "headlight bracket", "headlamp tab", "headlight tab", "headlamp repair kit", "headlight repair kit"]),
    ("drl", "Daytime Running Light", "lamps-lights", ["daytime running light", "drl", "day light", "running light"]),
    ("front-reflector", "Front Reflector", "lamps-lights", ["front reflector", "front bumper reflector", "side reflector"]),
    ("inner-tail-lamp", "Inner Tail Lamp", "lamps-lights", ["inner tail lamp", "inner taillight", "inner tail light", "inner taillamp", "tailgate lamp", "tailgate light", "boot lamp", "boot light", "trunk light", "trunk lamp"]),
    ("third-brake-light", "Third Brake Light", "lamps-lights", ["third brake light", "3rd brake light", "high stop lamp", "high mount stop lamp", "high level brake light", "centre brake light"]),
    ("side-skirt", "Side Skirt", "grilles-trims", ["side skirt", "rocker panel", "rocker trim", "sill trim", "side sill", "side step"]),
    ("door-moulding", "Door Moulding", "grilles-trims", ["door moulding", "door molding", "door trim", "door garnish", "door applique", "door strip"]),
    ("wheel-arch-trim", "Wheel Arch Trim", "grilles-trims", ["wheel arch trim", "arch moulding", "arch molding", "arch garnish", "fender flare", "wheel arch moulding"]),
    ("rear-spoiler", "Rear Spoiler", "body-panels", ["rear spoiler", "spoiler", "boot spoiler", "trunk spoiler", "wing spoiler", "ducktail"]),
    ("tailgate-trim", "Tailgate Trim", "grilles-trims", ["tailgate trim", "tailgate garnish", "boot trim", "boot garnish", "trunk trim", "trunk garnish"]),
    ("windscreen", "Windscreen", "glass-fittings", ["windscreen", "windshield", "front glass", "front windscreen"]),
    ("rear-glass", "Rear Glass", "glass-fittings", ["rear glass", "rear windscreen", "back glass", "rear window", "back window", "rear windshield"]),
    ("door-glass", "Door / Quarter Glass", "glass-fittings", ["door glass", "window glass", "side glass", "quarter glass", "side window"]),
    ("washer-nozzle", "Washer Nozzle / Cover", "glass-fittings", ["washer nozzle", "washer jet", "washer cover", "headlamp washer cover"]),
    ("tow-hook-cover", "Tow Hook Cover", "glass-fittings", ["tow hook cover", "tow cover", "towing eye cover", "tow cap", "tow hook cap"]),
    ("plate-bracket", "Number Plate Bracket", "glass-fittings", ["number plate bracket", "plate bracket", "plate holder", "number plate holder", "licence plate holder", "license plate holder"]),
    ("clips", "Clips & Fittings", "glass-fittings", ["clips", "clip", "retainer", "fastener", "rivet", "fittings", "screws"]),
    ("crash-structure", "Crash Structure", "other-parts", ["crash structure", "crash box", "front structure", "rear structure", "chassis rail", "subframe", "longitudinal"]),
    ("radiator-support", "Radiator Support / Cooling", "other-parts", ["radiator support", "front carrier", "radiator carrier", "radiator bracket", "condenser bracket", "front panel", "radiator", "condenser", "cooling pack"]),
    ("underbody-shield", "Underbody / Battery Shield", "other-parts", ["underbody shield", "battery shield", "battery cover", "battery protection", "underbody panel", "battery guard"]),
    ("jacking-pad", "Jacking Pad / Lift Point", "other-parts", ["jacking pad", "jack pad", "jacking point", "lift point", "jack point"]),
    ("other", "Other Part", "other-parts", ["wiper", "cabin filter", "other part"]),
]
# Category art (ChatGPT, 31 Oct 2026): original AI illustrations in the Base44 media library. Illustrative only, never product evidence.
ART_BASE = "https://media.base44.com/images/public/6ae5c57dbb2270677873e207/"
ART_FILES = {"front-bumper": "48a1e6a8b_front-bumper-cover.jpg", "headlamp": "da93cd754_headlamp-assembly.jpg", "tail-lamp": "5354b9c93_tail-lamp-assembly.jpg",
             "side-mirror": "c3fb234be_side-mirror-assembly.jpg", "fender": "a8d194bce_front-fender.jpg", "rear-bumper": "2f9bf66f7_rear-bumper-cover.jpg",
             "wheel-arch": "e709fd2c1_wheel-arch-liner.jpg", "bonnet": "7a0028b07_bonnet-hood.jpg", "underbody": "4350625e4_underbody-shield.jpg"}
ART_OF = {"front-bumper": "front-bumper", "front-bumper-bracket": "front-bumper", "bumper-reinforcement": "front-bumper", "front-lip": "front-bumper", "grille": "front-bumper", "lower-grille": "front-bumper",
          "headlamp": "headlamp", "headlamp-bracket": "headlamp", "drl": "headlamp", "fog-lamp": "headlamp", "front-reflector": "headlamp",
          "tail-lamp": "tail-lamp", "inner-tail-lamp": "tail-lamp", "third-brake-light": "tail-lamp", "rear-reflector": "tail-lamp",
          "side-mirror": "side-mirror", "fender": "fender", "wheel-arch-trim": "fender", "rear-bumper": "rear-bumper", "rear-bumper-bracket": "rear-bumper", "rear-diffuser": "rear-bumper", "bumper-trim": "rear-bumper",
          "wheel-arch": "wheel-arch", "bonnet": "bonnet", "bonnet-hinge": "bonnet", "undertray": "underbody", "underbody-shield": "underbody", "jacking-pad": "underbody"}
ART = {k: ART_BASE + ART_FILES[v] for k, v in ART_OF.items()}
ILLUS = "Illustrative image — actual part and fitment must be confirmed"
# Parts that need a specialist check: never sold through the cart, always a WhatsApp quote
SPECIAL = {"crash-structure", "radiator-support", "underbody-shield", "jacking-pad", "bumper-reinforcement", "windscreen"}
# Car page groups, in the order an owner walks around the car
AREAS = [
    ("front", "Front body", "front-bumper", ["front-bumper", "front-bumper-bracket", "bumper-reinforcement", "grille", "lower-grille", "front-lip", "undertray", "wheel-arch", "fender", "bonnet", "bonnet-hinge"]),
    ("lamps", "Headlamps & front lights", "headlamp", ["headlamp", "headlamp-bracket", "drl", "fog-lamp", "front-reflector"]),
    ("side", "Side body & mirrors", "side-mirror", ["side-mirror", "door-panel", "door-moulding", "side-skirt", "wheel-arch-trim"]),
    ("rear", "Rear body", "rear-bumper", ["rear-bumper", "rear-bumper-bracket", "rear-diffuser", "bumper-trim", "rear-reflector", "tailgate", "tailgate-trim", "rear-spoiler"]),
    ("tail", "Tail lamps", "tail-lamp", ["tail-lamp", "inner-tail-lamp", "third-brake-light"]),
    ("glass", "Glass & small fittings", "glass", ["windscreen", "rear-glass", "door-glass", "washer-nozzle", "tow-hook-cover", "plate-bracket", "clips"]),
    ("special", "Structure & underbody (specialist check)", "other", ["crash-structure", "radiator-support", "underbody-shield", "jacking-pad"]),
]
PART = {p[0]: p for p in PARTS}
GENERIC = [  # generic words owners type: slug -> weight
    ("bumper", {"front-bumper": .8, "rear-bumper": .8, "bumper-trim": .4}),
    ("lamp", {"headlamp": .6, "tail-lamp": .6, "fog-lamp": .4, "rear-reflector": .3}),
    ("light", {"headlamp": .6, "tail-lamp": .6, "fog-lamp": .4, "rear-reflector": .3}),
    ("body panel", {"bonnet": .5, "fender": .5, "door-panel": .5, "tailgate": .5}),
    ("panel", {"bonnet": .5, "fender": .5, "door-panel": .5, "tailgate": .5}),
]
CATS = [  # slug, name, line, part slugs, icon, title, desc
    ("bumpers", "Bumpers", "Front bumpers, rear bumpers and bumper trim", ["front-bumper", "rear-bumper", "bumper-trim", "front-bumper-bracket", "rear-bumper-bracket", "bumper-reinforcement", "front-lip", "rear-diffuser"], "front-bumper"),
    ("lamps-lights", "Lamps & Lights", "Headlamps, tail lamps, rear reflectors and fog lamps", ["headlamp", "tail-lamp", "rear-reflector", "fog-lamp", "headlamp-bracket", "drl", "front-reflector", "inner-tail-lamp", "third-brake-light"], "tail-lamp"),
    ("mirrors", "Mirrors", "Side mirrors, covers and mirror glass", ["side-mirror"], "side-mirror"),
    ("body-panels", "Body Panels", "Bonnets, fenders, door panels and tailgates", ["bonnet", "fender", "door-panel", "tailgate", "bonnet-hinge", "rear-spoiler"], "bonnet"),
    ("grilles-trims", "Grilles & Trims", "Front grilles, bumper trim and wheel arch linings", ["grille", "lower-grille", "bumper-trim", "wheel-arch", "undertray", "side-skirt", "door-moulding", "wheel-arch-trim", "tailgate-trim"], "grille"),
    ("glass-fittings", "Glass & Fittings", "Windscreens, door glass, plate brackets and clips", ["windscreen", "rear-glass", "door-glass", "washer-nozzle", "tow-hook-cover", "plate-bracket", "clips"], "glass"),
    ("other-parts", "Other Parts", "Structure, cooling and underbody parts (specialist check) and other parts", ["crash-structure", "radiator-support", "underbody-shield", "jacking-pad", "other"], "other"),
]
CAT = {c[0]: c for c in CATS}

def slugify(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

IC = {
    "front-bumper": '<path d="M3 21h26v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM6.5 21l1.6-6.2A3 3 0 0 1 11 12.6h10a3 3 0 0 1 2.9 2.2L25.5 21M10 24h12M9 16.5h3M20 16.5h3"/>',
    "rear-bumper": '<path d="M3 21h26v3a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2zM5 21v-4.5a3 3 0 0 1 3-3h16a3 3 0 0 1 3 3V21M5.5 17h5M21.5 17h5M13 24h6"/>',
    "bumper-trim": '<path d="M3 17c8-5 18-5 26 0M3 22c8-5 18-5 26 0M8 14.6v9M24 14.6v9" />',
    "headlamp": '<path d="M5 9c6-3 12-1 15 4 1.6 3 .6 6.4-3 7.2-5.2 1.2-10-1.4-12-6-1-2.2-.6-4 0-5.2Z"/><circle cx="14" cy="14.5" r="3"/><path d="M24 11h5M25 15h4M24 19h5"/>',
    "tail-lamp": '<path d="M3 12 25 8c2.6-.4 4 1.2 4 3.4V15c0 2-1.2 3.4-3.2 3.7L5 22c-2 .3-3-.9-3-2.8Z"/><path d="M9 12.4v7M14 11.6v7M19 10.8v7"/>',
    "rear-reflector": '<rect x="4" y="10" width="24" height="12" rx="3"/><path d="M9 22 15 10M15 22l6-12M21 22l5-9"/>',
    "fog-lamp": '<circle cx="12" cy="16" r="6"/><circle cx="12" cy="16" r="2"/><path d="M21 11h8M22 16h7M21 21h8"/>',
    "side-mirror": '<path d="M12 8c8-2.5 16 1 16 7s-8 8.5-16 5.5Z"/><path d="M12 20 5.5 27M12 14.5H5"/>',
    "bonnet": '<path d="M4 23 8 11h16l4 12zM13 11l-2 12M19 11l2 12M8 23h16"/><path d="M4 26h24" opacity=".5"/>',
    "fender": '<path d="M3 25v-5.5c0-2.6 1.8-4.3 4.4-4.5l5-.4 4-4.6h5.6c3.5 0 7 2.4 7 6.5V25"/><path d="M8.5 25a5.7 5.7 0 0 1 11.4 0"/>',
    "door-panel": '<path d="M5 27V13l6-7h14a2 2 0 0 1 2 2v19zM5 13h17V6M18 19h6"/>',
    "tailgate": '<path d="M5 27V14c0-4 2-7 6-7h10c4 0 6 3 6 7v13zM9 12h14v7H9zM12 23h8"/>',
    "grille": '<rect x="4" y="9" width="24" height="14" rx="4"/><path d="M8 13h16M8 16h16M8 19h16M12 9v14M20 9v14" opacity=".6"/>',
    "wheel-arch": '<path d="M3 25a13 13 0 0 1 26 0"/><path d="M8 25a8 8 0 0 1 16 0M3 25h26"/>',
    "other": '<path d="M20 5a6 6 0 0 0-5.6 8.2L5 22.6a2.6 2.6 0 0 0 3.7 3.7l9.4-9.4A6 6 0 0 0 26.5 11l-3.5 3.5-3.4-1-1-3.4L22 6.6A6 6 0 0 0 20 5Z"/>',
}
IC["glass"] = '<path d="M5 24 8.5 9.5A2 2 0 0 1 10.4 8h11.2a2 2 0 0 1 1.9 1.5L27 24z"/><path d="m12 12-2.5 8M16 12l-1.6 5" opacity=".6"/>'
for _k, _v in {"front-bumper-bracket": "front-bumper", "rear-bumper-bracket": "rear-bumper", "bumper-reinforcement": "bumper-trim", "front-lip": "bumper-trim", "rear-diffuser": "rear-bumper",
               "lower-grille": "grille", "undertray": "wheel-arch", "bonnet-hinge": "bonnet", "headlamp-bracket": "headlamp", "drl": "headlamp", "front-reflector": "rear-reflector",
               "inner-tail-lamp": "tail-lamp", "third-brake-light": "tail-lamp", "side-skirt": "door-panel", "door-moulding": "door-panel", "wheel-arch-trim": "wheel-arch",
               "rear-spoiler": "tailgate", "tailgate-trim": "tailgate", "windscreen": "glass", "rear-glass": "glass", "door-glass": "glass", "washer-nozzle": "other",
               "tow-hook-cover": "other", "plate-bracket": "other", "clips": "other", "crash-structure": "other", "radiator-support": "other", "underbody-shield": "other", "jacking-pad": "other"}.items():
    IC.setdefault(_k, IC[_v])
_SYN = sorted([(syn, p[0]) for p in PARTS if p[0] != "other" for syn in p[3] + [p[1].lower()]], key=lambda t: -len(t[0]))
def classify(*texts):
    """Part type for a product whose p is missing/other/unknown: longest owner-language match in its name/title."""
    t = " " + re.sub(r"[^a-z0-9]+", " ", " ".join(x or "" for x in texts).lower()) + " "
    for syn, slug in _SYN:
        if " " + syn + " " in t: return slug
    return "other"
def ico(k, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{IC[k]}</svg>'
UI = {
    "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3a.4.4 0 0 0 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.3c0-.1-.2-.2-.4-.3Z"/></svg>',
    "send": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12 20 4l-5 16-3.5-6.5Z"/><path d="m11.5 13.5 4-5"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "wrench": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M20 5a6 6 0 0 0-5.6 8.2L5 22.6a2.6 2.6 0 0 0 3.7 3.7l9.4-9.4A6 6 0 0 0 26.5 11l-3.5 3.5-3.4-1-1-3.4L22 6.6A6 6 0 0 0 20 5Z"/></svg>',
    "car": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 21H3.5v-5L6 9.5h14L25 16h3.5v5H27M10 21h10"/><circle cx="8" cy="21.5" r="2.6"/><circle cx="24" cy="21.5" r="2.6"/><path d="M6 16h19"/></svg>',
    "photo": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="8" width="24" height="17" rx="3"/><circle cx="16" cy="16.5" r="4.5"/><path d="M11 8l1.6-3h6.8L21 8"/></svg>',
    "check": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="16" cy="16" r="12"/><path d="m10.5 16.5 3.8 3.8 7.2-8"/></svg>',
    "pin": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M16 29s9-8.5 9-15a9 9 0 0 0-18 0c0 6.5 9 15 9 15Z"/><circle cx="16" cy="14" r="3.2"/></svg>',
    "doc": '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M8 3h11l6 6v20H8z"/><path d="M19 3v6h6M12 15h9M12 19h9M12 23h6"/></svg>',
}


# ------------------------------------------------------------------ database snapshot (db/*.json)
def load(name):
    p = DB / name
    return json.loads(p.read_text()) if p.exists() and p.read_text().strip() else []
def is_pub(r): return (r.get("status") or "published") == "published"
slugify_ = slugify

BRANDS = sorted([b for b in load("brands.json") if is_pub(b) and b.get("key") and b.get("name")], key=lambda b: (b.get("order") or 999, b["name"]))
BR = {b["key"]: b for b in BRANDS}
CARS = [c for c in load("cars.json") if is_pub(c) and c.get("key") and c.get("b") in BR]
CAR = {}
for c in CARS:
    pre = c["b"] + "-"
    c["slug"] = c["key"][len(pre):] if c["key"].startswith(pre) and len(c["key"]) > len(pre) else c["key"]
    c["bname"] = BR[c["b"]]["name"]
    c["full"] = f'{c["bname"]} {c["name"]}'
    c["url"] = f'brands/{c["b"]}/{c["slug"]}/'
    CAR[c["key"]] = c
CARS_BY_BRAND = {b["key"]: [c for c in CARS if c["b"] == b["key"]] for b in BRANDS}

PHOTO_FILES = {}   # group -> published path (decoded from EvPhoto chunks)
_chunks = {}
for r in load("photos.json"):
    if r.get("group") and r.get("data") is not None: _chunks.setdefault(r["group"], []).append(r)
for g, rows in _chunks.items():
    rows.sort(key=lambda r: r.get("i") or 0)
    s = "".join(r["data"] for r in rows)
    m = re.match(r"data:image/(jpeg|jpg|png|webp);base64,(.+)$", s, re.S)
    if m: PHOTO_FILES[g] = ("ph/" + re.sub(r"[^A-Za-z0-9_-]", "", g) + "." + ("jpg" if m.group(1) == "jpeg" else m.group(1)), base64.b64decode(m.group(2)))
SIDE_L = {"L": "Left", "R": "Right", "pair": "Pair"}
STOCK_L = {"in": "In stock", "order": "Can order", "out": "Out of stock"}

PRODS = []
_used = set()
for r in load("products.json"):
    if not is_pub(r) or r.get("m") not in CAR or not r.get("key"): continue
    car = CAR[r["m"]]
    p = r.get("p") or "other"
    if p not in PART or p == "other": p = classify(r.get("pn"), r.get("title"))
    pname = PART[p][1] if p in PART and p != "other" else (r.get("pn") or "Other part")
    pslug = r["key"][len(car["key"]) + 1:] if r["key"].startswith(car["key"] + "-") else r["key"]
    pslug = slugify(pslug) or slugify(r["key"])
    n = 2; base_ = pslug
    while (car["key"], pslug) in _used: pslug = f"{base_}-{n}"; n += 1
    _used.add((car["key"], pslug))
    side = r.get("side") or ""
    title = r.get("title") or (f'{car["full"]} {pname}' + (f' ({SIDE_L[side]})' if side in SIDE_L else ""))
    imgs = []
    for ph in (r.get("photos") or []):
        if ph.startswith("b44photo:"):
            g = ph.split(":", 1)[1]
            if g in PHOTO_FILES: imgs.append(PHOTO_FILES[g][0])
        elif ph.startswith("http"): imgs.append(ph)
    price = r.get("price")
    price = price if isinstance(price, (int, float)) and not isinstance(price, bool) and price > 0 else None
    PRODS.append(dict(key=r["key"], car=car, p=p if p in PART else "other", pn=pname, title=title, side=side, oem=r.get("oem") or "", grade=r.get("grade") or "",
                      price=price, stock=r.get("stock") or "", desc=r.get("desc") or "", note=r.get("note") or "", photos_raw=r.get("photos") or [], imgs=imgs,
                      slug=pslug, url=f'{car["url"]}{pslug}/', created=(r.get("created_date") or "")[:10], updated=(r.get("updated_date") or r.get("created_date") or "")[:10]))
PRODS.sort(key=lambda x: x["created"], reverse=True)
PBYCAR = {}
for x in PRODS: PBYCAR.setdefault(x["car"]["key"], []).append(x)
def disp(u): return u if u.startswith("http") else "{{R}}" + u
def money(v): return "S$" + (f"{v:,.2f}" if float(v) % 1 else f"{int(v):,}")

# ------------------------------------------------------------------ links to enquiry / WhatsApp
def enq(text, r="{{R}}"):
    """WA empty -> on-site enquiry form prefilled. WA set -> wa.me with the prefilled message."""
    if WA:
        return f"https://wa.me/{WA}?text={quote(f'Hi {BRAND}, I am looking for: {text}. (from website)')}"
    return f"{r}enquiry/?q={quote(text)}"
PVN = '' if WA else '<span class="pvn">Contact details are being added. Until then, enquiry buttons open the enquiry form.</span>'

# ------------------------------------------------------------------ page shell
VER = {}
def asset(name):
    if name not in VER:
        f = OUT / name if name == "data.js" else HERE / name
        VER[name] = hashlib.sha1(f.read_bytes()).hexdigest()[:8]
    return f"{name}?v={VER[name]}"

pages = []  # (url path, priority, lastmod)
def logo_html(r):
    return (f'<a class="logo" href="{r}" aria-label="{BRAND} home"><img class="em" src="{r}logo-96.png" alt="" width="48" height="48">'
            f'<span class="wm"><b>EV BODY</b><b>PARTS</b><small>China &amp; EV cars &middot; Singapore</small></span></a>')

ORG = {"@type": ["AutoPartsStore", "Organization"], "@id": BASE + "/#org", "name": BRAND, "url": BASE + "/", "slogan": TAG,
       "logo": BASE + "/icon-512.png", "image": BASE + "/og.jpg",
       "description": "Singapore seller of body parts for China and EV cars, for workshops and car owners.",
       "areaServed": {"@type": "Country", "name": "Singapore"}}
if LEGAL: ORG["legalName"] = LEGAL
if UEN: ORG["identifier"] = {"@type": "PropertyValue", "propertyID": "UEN", "value": UEN}
if ADDRESS: ORG["address"] = {"@type": "PostalAddress", "streetAddress": ADDRESS, "addressLocality": "Singapore", "addressCountry": "SG"}
if PHONE: ORG["telephone"] = PHONE
if EMAIL: ORG["email"] = EMAIL
SITE = {"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": BRAND, "publisher": {"@id": BASE + "/#org"},
        "potentialAction": {"@type": "SearchAction", "target": BASE + "/catalogue/?q={search_term_string}", "query-input": "required name=search_term_string"}}

NAV = [("catalogue/", "Catalogue", "cat"), ("parts/", "Parts", "parts"), ("brands/", "Brands", "brands"),
       ("for-workshops/", "Workshops", "ws"), ("for-car-owners/", "Car owners", "own"), ("about/", "About", "about"), ("contact/", "Contact", "contact")]

def faq_html(items):
    return '<div class="faq">' + "".join(f'<details class="rv"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items) + "</div>"
def faq_ld(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
def fit(*c):
    for t in c:
        if len(t) < 60: return t
    return c[-1][:57].rstrip() + "..."
def short(s, n=158):
    s = re.sub(r"\s+", " ", s).strip()
    return s if len(s) <= n else s[:n - 3].rsplit(" ", 1)[0] + "..."

def shell(path, title, desc, body, active="", crumbs=None, schema=None, og_type="website", index=True, faq=None, img=None, pri=0.7, preload=None, lastmod=None):
    assert len(title) < 60, (path, len(title), title)
    assert len(desc) < 160, (path, len(desc), desc)
    depth = path.count("/")
    r = "../" * depth
    url = BASE + "/" + ("" if path == "index.html" else path.replace("index.html", ""))
    ld = [dict(ORG), dict(SITE)] if path == "index.html" else [dict(ORG)]
    if crumbs:
        ld.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u}
                                                                     for i, (n, u) in enumerate([("Home", "")] + crumbs)]})
    if faq: ld.append(faq_ld(faq))
    if schema: ld.extend(schema)
    ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False).replace("</", "<\\/")
    nav = "".join(f'<a href="{r}{u}"{" aria-current=\"page\"" if k == active else ""}>{n}</a>' for u, n, k in NAV)
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Breadcrumb"><a href="' + r + '">Home</a>' + "".join(
            (f'<span>/</span><a href="{r}{u}">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span>/</span><span aria-current="page">{e(n)}</span>')
            for i, (n, u) in enumerate(crumbs)) + "</nav>"
    body = body.replace("{{CRUMBS}}", cr).replace("{{R}}", r)
    ogi = img or BASE + "/og.jpg"
    dims = '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">' if not img else ""
    half = (len(BRANDS) + 1) // 2
    brands_ft = "".join(f'<li><a href="{r}brands/{b["key"]}/">{e(b["name"])}</a></li>' for b in BRANDS[:half])
    brands_ft2 = "".join(f'<li><a href="{r}brands/{b["key"]}/">{e(b["name"])}</a></li>' for b in BRANDS[half:])
    parts_ft = "".join(f'<li><a href="{r}parts/{c[0]}/">{e(c[1])}</a></li>' for c in CATS)
    contact_ft = "".join([f'<br>WhatsApp <a href="https://wa.me/{WA}">{WA_DISPLAY}</a>' if WA else "", f"<br>Call <a href=\"tel:{PHONE.replace(' ', '')}\">{e(PHONE)}</a>" if PHONE else "", f'<br><a href="mailto:{EMAIL}">{e(EMAIL)}</a>' if EMAIL else "",
                          f"<br>{e(ADDRESS)}" if ADDRESS else ""])
    ft_name = f"{e(LEGAL)}" + (f" (UEN {e(UEN)})" if UEN else "") if LEGAL else ""
    third = (f'<a class="wa" href="{enq("a part", r)}">{UI["wa"]}<span>WhatsApp</span></a>' if WA else f'<a href="{r}brands/">{UI["car"]}<span>Brands</span></a>')
    doc = f"""<!doctype html>
<html lang="en-SG" class="no-js" data-root="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="en_SG"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{ogi}">{dims}<meta property="og:image:alt" content="{e(BRAND)} - {e(TAG)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{ogi}">
<link rel="icon" href="{r}favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="{r}icon-192.png"><link rel="apple-touch-icon" href="{r}apple-touch-icon.png"><link rel="manifest" href="{r}site.webmanifest">
<meta name="theme-color" content="#07090B">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Saira:ital,wght@0,500;0,600;0,700;0,800;1,600;1,700;1,800&display=swap">
{'<link rel="preconnect" href="https://images.unsplash.com">' if preload else ''}
<link rel="stylesheet" href="{r}{asset('ev.css')}">
<script>document.documentElement.classList.remove('no-js');document.documentElement.classList.add('js');window.EV_ROOT="{r}";</script>
<script type="application/ld+json">{ldj}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hd"><div class="wrap">
{logo_html(r)}
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="nav-cta" href="{enq('a part', r)}">Enquire</a></nav>
<button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
</div></header>
<main id="main">
{body}
</main>
<footer class="ft"><div class="wrap">
<div class="ft-g">
<div class="ft-about">{logo_html(r)}<p>{BRAND} &middot; {DOMAIN}<br>Body parts for China and EV cars, sold in Singapore to workshops and car owners.{contact_ft}</p>{f'<p class="mu">{ft_name}</p>' if ft_name else ''}<p class="mu">Brand names are used only to describe which vehicles a part is for.</p></div>
<div><h4>Parts</h4><ul>{parts_ft}<li><a href="{r}catalogue/">Full catalogue</a></li></ul></div>
<div><h4>Brands</h4><ul>{brands_ft}</ul></div>
<div><h4>&nbsp;</h4><ul>{brands_ft2}</ul></div>
<div><h4>Company</h4><ul><li><a href="{r}for-workshops/">For workshops</a></li><li><a href="{r}for-car-owners/">For car owners</a></li><li><a href="{r}articles/">Guides</a></li><li><a href="{r}about/">About</a></li><li><a href="{r}contact/">Contact</a></li><li><a href="{r}enquiry/">Enquiry</a></li><li><a href="{r}privacy/">Privacy</a></li></ul></div>
</div>
<div class="ft-b"><span>&copy; {datetime.date.today().year} {BRAND}</span><span>Stock photos are mood imagery only. <a href="{STAFF_URL}" rel="nofollow noopener">Staff</a></span></div>
</div></footer>
<nav class="mbar" aria-label="Quick actions"><a href="{r}catalogue/">{UI['search']}<span>Search</span></a><a href="{enq('a part', r)}">{UI['send']}<span>Enquire</span></a>{third}</nav>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="{r}{asset('data.js')}" defer></script><script src="{r}{asset('ev.js')}" defer></script><script src="{r}{asset('wa.js')}" defer></script>
</body>
</html>
"""
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc)
    if index:
        pages.append(("/" + ("" if path == "index.html" else path.replace("index.html", "")), pri, lastmod or TODAY))

def btn(href, label, kind="p", extra=""):
    return f'<a class="btn btn-{kind}" href="{href}"{extra}>{label}</a>'

# product card (same markup as ev.js card())
def pill_html(x):
    return f'<span class="pill st-{x["stock"]}">{STOCK_L[x["stock"]]}</span>' if x["stock"] in STOCK_L else ""
def price_html(x):
    return f'<span class="price">{money(x["price"])}</span>' if x["price"] else '<span class="price ask">Ask for price</span>'
def card_static(x, r="{{R}}"):
    media = f'<img src="{e(disp(x["imgs"][0]))}" alt="{e(x["title"])}" width="88" height="88" loading="lazy" decoding="async" onerror="this.remove()">' if x["imgs"] else ""
    return (f'<article class="rc"><div class="rc-ic">{ico(x["p"])}{media}</div><div class="rc-b"><span class="chip">{e(x["car"]["full"])}</span>'
            f'<h3>{e(x["title"])}</h3><p class="rc-t">{e(x["pn"])}{" &middot; " + SIDE_L[x["side"]] if x["side"] in SIDE_L else ""}</p>'
            f'<div class="rc-m">{pill_html(x)}{price_html(x)}</div>'
            f'<div class="rc-a"><a class="btn btn-p btn-s" href="{enq(x["title"], r)}">Enquire</a><a class="btn btn-g btn-s" href="{r}{x["url"]}">Details</a></div></div></article>')
def empty_state(name, r="{{R}}"):
    return (f'<div class="empty"><h3>No {e(name)} listings yet</h3><p>New parts are added all the time. Tell us the car and the part and we check what we can find.</p>'
            f'<a class="btn btn-p btn-s" href="{enq(name + " part", r)}">Ask us about {e(name)} parts</a></div>')
def list_html(items, name, lim=9):
    if not items: return empty_state(name)
    return '<div class="rgrid">' + "".join(card_static(x) for x in items[:lim]) + '</div>' + (f'<p class="seeall"><a class="btn btn-g" href="{{{{R}}}}catalogue/">See all {len(items)} listings</a></p>' if len(items) > lim else "")

TRY = ["Tesla Model Y tail lamp", "Denza D9 rear reflector", "atto3 headlight", "MG4 side mirror", "zeekr 001 bonnet", "sticker bumper model y"]
def search_box(idp, ph="Brand, model and part, e.g. Tesla Model Y tail lamp", action="{{R}}catalogue/", live=True, tries=TRY, big=True):
    ch = "".join(f'<button type="button" data-try="{e(t)}">{e(t)}</button>' for t in tries)
    return f'''<form class="sbox{" big" if big else ""}" role="search" action="{action}" method="get" data-search="{idp}">
<label class="sr" for="{idp}-q">Search the catalogue</label>
<div class="srow">{UI["search"]}<input id="{idp}-q" class="sin" name="q" type="search" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search" placeholder="{e(ph)}"><button class="btn btn-p" type="submit">Search</button></div>
<p class="try"><span>Try:</span>{ch}</p>
<div class="sres" id="{idp}-res" aria-live="polite"></div></form>'''

def brandchips(r="{{R}}", marquee=True):
    one = "".join(f'<a class="bchip" href="{r}brands/{b["key"]}/">{e(b["name"])}</a>' for b in BRANDS)
    two = one.replace("<a ", '<a tabindex="-1" aria-hidden="true" ', ) if marquee else ""
    return f'<div class="bstrip" aria-label="Brands"><div class="btrack">{one}{two}</div></div>'
def brand_names():
    n = [b["name"] for b in BRANDS]
    return ", ".join(n[:-1]) + " and " + n[-1] if len(n) > 1 else "".join(n)

# ------------------------------------------------------------------ pages
def home_faq():
    return [
    ("How do I find the part for my car, for example a Tesla Model Y tail lamp?",
     "Search by brand, model and part, in the words you would use. If the part is listed you see it with its price, or Ask for price. If it is not listed yet, send us the car and the part and we check."),
    ("Who do you sell to?", f"{BRAND} sells body parts for China and EV cars in Singapore, to workshops and to car owners."),
    ("Which car brands do you cover?",
     f"We list parts for {brand_names()}, mainly body parts. If your model is not listed, send it to us and ask."),
    ("Are prices shown?",
     "Where a price is set, it is shown in Singapore dollars (S$). Where it is not, the part says Ask for price and we reply to your enquiry. We confirm fitment against your car before anything else."),
]

def home():
    faq = home_faq()
    cats = "".join(f'''<a class="cc rv" href="{{{{R}}}}parts/{c[0]}/"><span class="cc-ic">{ico(c[4])}</span><h3>{e(c[1])}</h3><p>{e(c[2])}</p><span class="more">More details {UI["arrow"]}</span></a>''' for c in CATS)
    steps = [("Search", "Type the brand, model and part in plain words, the way you would say it to us."),
             ("Send car and part", "Open the enquiry form or WhatsApp with your car details. A photo of the old part helps."),
             ("We confirm and reply", "We check fitment against your car and reply with availability and price.")]
    st = "".join(f'<li class="rv"><span class="n">{i + 1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(steps))
    new = PRODS[:6]
    body = f'''<section class="hero">
<div class="hero-bg" aria-hidden="true">{pic("hero", "Car tail light in the dark (mood image)", 2000, 1333, "100vw", True, "kb")}</div>
<div class="wrap hero-in">
<p class="eyebrow">China &amp; EV car parts &middot; Singapore</p>
<h1>Body parts for China &amp; EV cars, <em>found by car and part.</em></h1>
<p class="lead">Search the way you talk, like &ldquo;Tesla Model Y tail lamp&rdquo;. Then send us your car and the part. For workshops and car owners in Singapore.</p>
{search_box("hq")}
{PVN}
</div></section>
<section class="strip"><div class="wrap">{brandchips()}</div></section>
<section class="sec alt" data-new-sec{"" if new else " hidden"}><div class="wrap">
<div class="sec-t rv"><p class="kick">Newly added</p><h2>Latest parts in the catalogue</h2><p>Parts added most recently. Prices are shown where set. We confirm fitment on enquiry.</p></div>
<div data-list="new:" data-limit="6">{list_html(new, "", 6) if new else ""}</div>
<p class="center rv" style="margin-top:28px"><a class="btn btn-g" href="{{{{R}}}}catalogue/">See the full catalogue {UI["arrow"]}</a></p>
</div></section>
<section class="sec"><div class="wrap">
<div class="sec-t rv"><p class="kick">Parts</p><h2>Browse by part type</h2><p>Mainly body parts, plus some other parts. Pick a type to see what each part is and which cars it is listed for.</p></div>
<div class="cgrid">{cats}</div>
</div></section>
<section class="sec alt"><div class="wrap">
<div class="two">
<a class="tc rv" href="{{{{R}}}}for-workshops/"><div class="tc-ph">{pic("door", "Red and black car door, mood image", 900, 600, "(min-width:900px) 45vw, 100vw")}</div><div class="tc-b"><p class="kick">For workshops</p><h3>Parts for the job on your bay</h3><p>Send the car and the parts you need. We check fitment and reply.</p><span class="more">More details {UI["arrow"]}</span></div></a>
<a class="tc rv" href="{{{{R}}}}for-car-owners/"><div class="tc-ph">{pic("matte", "Matte black electric car under a warm sky, mood image", 900, 600, "(min-width:900px) 45vw, 100vw")}</div><div class="tc-b"><p class="kick">For car owners</p><h3>Not sure which part it is?</h3><p>Tell us your car and what is damaged. We help you find the right part name.</p><span class="more">More details {UI["arrow"]}</span></div></a>
</div></div></section>
<section class="sec"><div class="wrap">
<div class="sec-t rv"><p class="kick">How it works</p><h2>Three steps</h2></div>
<ol class="steps">{st}</ol>
</div></section>
<section class="sec alt"><div class="wrap narrow">
<div class="sec-t rv"><p class="kick">FAQ</p><h2>Quick answers</h2></div>
{faq_html(faq)}
</div></section>
<section class="cta"><div class="wrap center rv"><h2>Tell us the car and the part.</h2><p>We confirm fitment and reply.</p>{PVN}<div class="btns">{btn(enq("a part"), "Send an enquiry " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div></div></section>'''
    shell("index.html", "EV Body Parts | China & EV Body Parts in Singapore",
          "Search body parts for Tesla, BYD, Denza, MG, Zeekr and more China and EV cars. EV Body Parts serves workshops and car owners in Singapore.",
          body, "", faq=faq, pri=1.0, preload=True)

def catalogue():
    brandopts = "".join(f'<option value="{b["key"]}">{e(b["name"])}</option>' for b in BRANDS)
    partopts = "".join(f'<option value="{p[0]}">{e(p[1])}</option>' for p in PARTS)
    links = "".join(f'<li><a href="{{{{R}}}}brands/{b["key"]}/">{e(b["name"])} parts</a></li>' for b in BRANDS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Catalogue</p><h1>Search the catalogue</h1>
<p class="lead">Type the brand, model and part, or use the filters. The list is read live, so new parts show as soon as they are added.</p></div></section>
<section class="sec tight"><div class="wrap">
<form class="sbox" id="cat-form" role="search" action="" method="get" data-search="cq">
<label class="sr" for="cq-q">Search</label>
<div class="srow">{UI["search"]}<input id="cq-q" class="sin" name="q" type="search" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="Brand, model and part, e.g. Tesla Model Y tail lamp"><button class="btn btn-p" type="submit">Search</button></div>
<div class="filters"><label>Brand<select name="brand" id="f-brand"><option value="">All brands</option>{brandopts}</select></label>
<label>Model<select name="model" id="f-model"><option value="">All models</option></select></label>
<label>Part<select name="part" id="f-part"><option value="">All parts</option>{partopts}</select></label>
<button class="btn btn-g btn-s" type="button" id="f-clear">Clear</button></div>
<p class="try"><span>Try:</span>{"".join(f'<button type="button" data-try="{e(t)}">{e(t)}</button>' for t in TRY)}</p>
</form>
{PVN}
<div class="count" id="cat-count" aria-live="polite"></div>
<div class="sres full" id="cat-res"></div>
<div class="sec-t" style="margin-top:44px"><h2>Browse by brand</h2></div>
<ul class="plain brandlist">{links}</ul>
</div></section>'''
    ld = [{"@type": "ItemList", "name": f"Brands in the {BRAND} catalogue", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": f'{b["name"]} body parts', "url": f'{BASE}/brands/{b["key"]}/'} for i, b in enumerate(BRANDS)]}]
    shell("catalogue/index.html", "Catalogue | EV Body Parts Singapore",
          "Search China and EV car body parts by brand, model and part, like Tesla Model Y tail lamp. Send us your car and part to confirm fitment.",
          body, "cat", [("Catalogue", "catalogue/")], ld, pri=0.9)

def parts_hub():
    cards = "".join(f'''<a class="cc rv" href="{{{{R}}}}parts/{c[0]}/"><span class="cc-ic">{ico(c[4])}</span><h3>{e(c[1])}</h3><p>{e(c[2])}</p><span class="more">More details {UI["arrow"]}</span></a>''' for c in CATS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Parts</p><h1>Parts for China &amp; EV cars</h1><p class="lead">Mainly body parts, with some other parts. Choose a type, or go straight to the search.</p></div></section>
<section class="sec tight"><div class="wrap"><div class="cgrid">{cards}</div><div class="center" style="margin-top:32px">{btn("{{R}}catalogue/", "Search the catalogue " + UI["arrow"])}</div></div></section>'''
    shell("parts/index.html", "Car Body Parts by Type | EV Body Parts",
          "Bumpers, lamps and lights, mirrors, body panels, grilles and trims for China and EV cars in Singapore. Choose a part type.",
          body, "parts", [("Parts", "parts/")], pri=0.8)

PART_COPY = {
    "bumpers": ("Bumpers for China & EV cars", "Front bumpers, rear bumpers and bumper trim for China and EV cars sold in Singapore. Tell us the model and we confirm fitment.",
        ["A bumper is more than one piece. There is usually the outer bumper cover, and separate trim pieces such as the lower lip, strips and garnish. Tell us which piece you mean, and say front or rear.",
         "If your car has parking sensors or a camera near the bumper, mention it and send a photo. It helps us match the right part.",
         "Not sure what the piece is called? Send a photo of the damage and the car model."]),
    "lamps-lights": ("Lamps & lights for China & EV cars", "Headlamps, tail lamps, rear reflectors and fog lamps for China and EV cars in Singapore. Send your model and we confirm fitment.",
        ["Lamps are listed by position: headlamp at the front, tail lamp at the rear, rear reflector low on the rear bumper, and fog lamp. People also say headlight, taillight or brake light, and the search understands those words.",
         "Say which side you need. Left and right are as seen from the driver's seat. A photo of the old lamp, front and back, is the quickest way for us to match it."]),
    "mirrors": ("Side mirrors for China & EV cars", "Side mirrors, mirror covers and mirror glass for China and EV cars in Singapore. Tell us your model and which side you need.",
        ["Owners ask for the whole mirror, only the cover, or only the glass. Tell us which one, and which side. Left and right are as seen from the driver's seat.",
         "A photo of the broken mirror from the outside and, if possible, the back helps us confirm the right part."]),
    "body-panels": ("Body panels for China & EV cars", "Bonnets, fenders, door panels and tailgates for China and EV cars in Singapore. Send the model and we confirm fitment.",
        ["Body panels are the big pieces: the bonnet (hood), the front fender (wing), door panels and the tailgate (boot lid). Panels are specific to the model, so we always check against your car.",
         "Tell us the model and the damage. A few photos from different angles are enough to start."]),
    "grilles-trims": ("Grilles & trims for China & EV cars", "Front grilles, bumper trim and wheel arch linings for China and EV cars in Singapore. Send your model and we confirm fitment.",
        ["Grilles and trim pieces are small but easy to get wrong, because the shape changes between models. Send a photo of the piece, or of the place where it was fitted.",
         "Bumper trim also appears under Bumpers. Wheel arch lining is the liner inside the wheel arch."]),
    "glass-fittings": ("Glass & small fittings for China & EV cars", "Windscreens, door glass, number plate brackets, tow hook covers and clips for China and EV cars in Singapore. Tell us the car and the part.",
        ["Small fittings like clips, tow hook covers and plate brackets are easy to lose in a repair. Tell us the car, the part and the side, or send a photo.",
         "For a windscreen, tell us if your car has a camera or sensor behind it. Glass with cameras needs the exact version and may need calibration after fitting."]),
    "other-parts": ("Structure, underbody & other parts for China & EV cars", "Crash structure, radiator support, underbody and battery shields and other parts for China and EV cars in Singapore. Each one is checked by hand.",
        ["Structure, cooling and underbody parts are safety related, so we do not sell them through the cart. Send the car, the build year and photos on WhatsApp and we check each part one by one.",
         "Some owners also need small parts such as wipers or a cabin filter. Ask us with the car model and we check."]),
}
def part_pages():
    for c in CATS:
        slug, name, line, ps, icon = c
        h1, desc, paras = PART_COPY[slug]
        title = fit(f"{name} for China & EV Cars | {BRAND}", f"{name} for China & EV Cars")
        sub = "".join(f'<li id="{p}"><span class="ic-s">{ico(p)}</span><div><h3>{e(PART[p][1])}</h3><p class="mu">Also searched as: {e(", ".join(PART[p][3][:4]))}.</p>'
                      f'<a class="more" href="{{{{R}}}}catalogue/?part={p}">See {e(PART[p][1].lower())} listings {UI["arrow"]}</a></div></li>' for p in ps)
        others = "".join(f'<a class="bchip" href="{{{{R}}}}parts/{o[0]}/">{e(o[1])}</a>' for o in CATS if o[0] != slug)
        items = [x for x in PRODS if x["p"] in ps]
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Parts</p><h1>{h1.replace("&", "&amp;")}</h1><p class="lead">{e(line)}.</p></div></section>
<section class="sec tight"><div class="wrap two-c">
<div class="prose">{"".join(f"<p>{e(t)}</p>" for t in paras)}
<h2>Part types in this group</h2><ul class="plist">{sub}</ul>
<div class="btns">{btn(enq(name), "Enquire about " + e(name.lower()) + " " + UI["arrow"])}{btn("{{R}}catalogue/?" + "part=" + ps[0], "Search these parts", "g")}</div>{PVN}</div>
<aside class="side"><div class="panel"><h3>Search by car</h3>{search_box("pq", "Brand, model and part", tries=[f"Tesla Model Y {PART[ps[0]][1].lower()}", f"BYD Atto 3 {PART[ps[0]][1].lower()}"], big=False)}</div></aside>
</div></section>
<section class="sec alt tight"><div class="wrap"><div class="sec-t"><h2>Listed in this group</h2><p>Parts currently in the catalogue. We confirm fitment on enquiry.</p></div>
<div class="sres full" data-list="parts:{','.join(ps)}" data-limit="9">{list_html(items, name)}</div></div></section>
<section class="sec tight"><div class="wrap"><div class="sec-t"><h2>Other part types</h2></div><div class="bchips">{others}</div></div></section>'''
        shell(f"parts/{slug}/index.html", title, desc, body, "parts", [("Parts", "parts/"), (name, f"parts/{slug}/")], pri=0.8)

def brands_hub():
    def mod(b):
        cs = CARS_BY_BRAND[b["key"]]
        return ", ".join(c["name"] for c in cs) if cs else "Ask us for your model"
    cards = "".join(f'<a class="cc rv" href="{{{{R}}}}brands/{b["key"]}/"><span class="cc-ic bn">{e(b["name"][:2].upper())}</span><h3>{e(b["name"])}</h3><p>{e(mod(b))}</p><span class="more">More details {UI["arrow"]}</span></a>' for b in BRANDS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Brands</p><h1>Car brands we list parts for</h1><p class="lead">The {len(BRANDS)} brands on our brand board. Brand names only describe which vehicle a part is for.</p></div></section>
<section class="sec tight"><div class="wrap"><div class="cgrid">{cards}</div></div></section>'''
    shell("brands/index.html", "Car Brands | EV Body Parts Singapore",
          "China and EV car brands we list body parts for: Tesla, BYD, Denza, MG, Maxus, Chery, Zeekr and more. Choose your brand.",
          body, "brands", [("Brands", "brands/")], pri=0.8)

def ml(names): return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
def brand_pages():
    for b in BRANDS:
        slug, name = b["key"], b["name"]
        cs = CARS_BY_BRAND[slug]
        if cs:
            mnames = [c["name"] for c in cs]
            intro = b.get("intro") or f"{BRAND} lists body and lamp parts for {name} {ml(mnames)}. Choose your model, or search by model and part, then send us your car so we can confirm fitment."
            desc = short(f"{name} body parts in Singapore for {ml(mnames)}. Send your car and part and EV Body Parts confirms fitment.")
            rows = "".join(f'<li><h3><a href="{{{{R}}}}{c["url"]}">{e(c["full"])}</a></h3><p>{len(PBYCAR.get(c["key"], []))} listed &middot; <a href="{{{{R}}}}{c["url"]}">See {e(c["name"])} parts</a></p></li>' for c in cs)
            modelsec = f'<h2>{e(name)} models</h2><ul class="mlist">{rows}</ul>'
        else:
            intro = b.get("intro") or f"{name} is on our brand board, but no {name} model is listed here yet. Tell us your model and the part, with a photo if you can, and we check what we can find."
            desc = short(f"{name} body parts in Singapore: tell us your model and part and EV Body Parts checks what we can find.")
            modelsec = f'<h2>{e(name)} parts</h2><p>No {e(name)} model is listed yet. Send us your model and the part and we check.</p>'
        title = fit(f"{name} Body Parts in Singapore | {BRAND}", f"{name} Body Parts in Singapore")
        others = "".join(f'<a class="bchip" href="{{{{R}}}}brands/{o["key"]}/">{e(o["name"])}</a>' for o in BRANDS if o["key"] != slug)
        items = [x for x in PRODS if x["car"]["b"] == slug]
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Brand</p><h1>{e(name)} body parts in Singapore</h1><p class="lead">{e(intro)}</p></div></section>
<section class="sec tight"><div class="wrap two-c">
<div class="prose">{modelsec}<p>Not sure which part you need? Read <a href="{{{{R}}}}articles/which-part-is-it/">which part is it</a>, or <a href="{enq(name + " part")}">send us your {e(name)} and the part</a>.</p>{PVN}</div>
<aside class="side"><div class="panel"><h3>Search {e(name)} parts</h3>{search_box("bq", f"{name} model and part", tries=[f"{name} tail lamp", f"{name} front bumper"], big=False)}</div></aside>
</div></section>
<section class="sec alt tight"><div class="wrap"><div class="sec-t"><h2>{e(name)} listings</h2><p>Parts currently in the catalogue. We confirm fitment on enquiry.</p></div>
<div class="sres full" data-list="brand:{slug}" data-limit="9" data-name="{e(name)}">{list_html(items, name)}</div></div></section>
<section class="sec tight"><div class="wrap"><div class="sec-t"><h2>Other brands</h2></div><div class="bchips">{others}</div></div></section>'''
        shell(f"brands/{slug}/index.html", title, desc, body, "brands", [("Brands", "brands/"), (name, f"brands/{slug}/")], pri=0.7)

def car_pages():
    for c in CARS:
        name, full, slug = c["name"], c["full"], c["slug"]
        items = PBYCAR.get(c["key"], [])
        facts = "".join([f'<div><dt>Years</dt><dd>{e(c["years"])}</dd></div>' if c.get("years") else "", f'<div><dt>Code</dt><dd>{e(c["code"])}</dd></div>' if c.get("code") else ""])
        intro = f"Body parts for the {full} in Singapore. Search by part, or tell us the part you need and we confirm fitment against your car."
        title = fit(f"{full} Body Parts Singapore | {BRAND}", f"{full} Body Parts Singapore", f"{full} Body Parts")
        desc = short(f"{full} body parts in Singapore: bumpers, lamps, mirrors and panels. Send your car and part and EV Body Parts confirms fitment.")
        asks = "".join(f'<a class="bchip" href="{enq(full + " " + p[1])}">{e(p[1])}</a>' for p in PARTS if p[0] != "other")
        sibs = "".join(f'<a class="bchip" href="{{{{R}}}}{o["url"]}">{e(o["name"])}</a>' for o in CARS_BY_BRAND[c["b"]] if o["key"] != c["key"])
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">{e(c["bname"])}</p><h1>{e(full)} body parts in Singapore</h1><p class="lead">{e(intro)}</p></div></section>
<section class="sec tight"><div class="wrap two-c">
<div class="prose"><h2>Ask us for a {e(full)} part</h2><p>Tap a part type to send an enquiry for it. If the part is not listed below, that does not mean we cannot find it.</p>
<div class="bchips">{asks}</div>
{f'<dl class="facts">{facts}</dl>' if facts else ''}
<p>Not sure what the part is called? Read <a href="{{{{R}}}}articles/which-part-is-it/">which part is it</a>, or send a photo of the damage with your car.</p>{PVN}</div>
<aside class="side"><div class="panel"><h3>Search {e(full)} parts</h3>{search_box("cq2", f"{full} part", tries=[f"{full} tail lamp", f"{full} front bumper"], big=False)}</div></aside>
</div></section>
<section class="sec alt tight"><div class="wrap"><div class="sec-t"><h2>{e(full)} listings</h2><p>Parts currently in the catalogue for this car.</p></div>
<div class="sres full" data-list="car:{c["key"]}" data-limit="12" data-name="{e(full)}">{list_html(items, full, 12)}</div></div></section>
{f'<section class="sec tight"><div class="wrap"><div class="sec-t"><h2>Other {e(c["bname"])} models</h2></div><div class="bchips">{sibs}</div></div></section>' if sibs else ''}'''
        shell(f'{c["url"]}index.html', title, desc, body, "brands",
              [("Brands", "brands/"), (c["bname"], f'brands/{c["b"]}/'), (name, c["url"])], pri=0.7)

def product_pages():
    for x in PRODS:
        c = x["car"]
        title = fit(f'{x["title"]} | {BRAND}', f'{x["title"]} Singapore', x["title"])
        base = x["desc"] or x["note"] or f'{x["title"]} for the {c["full"]}, sold in Singapore.'
        desc = short(f'{base} {"Price " + money(x["price"]) + "." if x["price"] else "Ask for price."} Enquire with EV Body Parts.')
        facts = "".join([f'<div><dt>Car</dt><dd><a href="{{{{R}}}}{c["url"]}">{e(c["full"])}</a></dd></div>', f'<div><dt>Part type</dt><dd>{e(x["pn"])}</dd></div>',
                         f'<div><dt>Side</dt><dd>{SIDE_L[x["side"]]}</dd></div>' if x["side"] in SIDE_L else "",
                         f'<div><dt>Part number</dt><dd>{e(x["oem"])}</dd></div>' if x["oem"] else "",
                         f'<div><dt>Grade</dt><dd>{e(x["grade"])}</dd></div>' if x["grade"] else "",
                         f'<div><dt>Stock</dt><dd>{STOCK_L[x["stock"]]}</dd></div>' if x["stock"] in STOCK_L else ""])
        imgs = "".join(f'<img src="{e(disp(u))}" alt="{e(x["title"])} photo {i + 1}" width="144" height="108" loading="lazy" decoding="async">' for i, u in enumerate(x["imgs"][1:5], 1))
        main = f'<img src="{e(disp(x["imgs"][0]))}" alt="{e(x["title"])}" width="800" height="600" decoding="async" fetchpriority="high" onerror="this.remove()">' if x["imgs"] else ""
        rel = [y for y in PBYCAR[c["key"]] if y["key"] != x["key"]][:6]
        relh = f'<section class="sec alt tight"><div class="wrap"><div class="sec-t"><h2>More for the {e(c["full"])}</h2></div><div class="rgrid">{"".join(card_static(y) for y in rel)}</div></div></section>' if rel else ""
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">{e(c["full"])}</p><h1>{e(x["title"])}</h1></div></section>
<section class="sec tight"><div class="wrap two-c"><div>
<div class="pgal">{ico(x["p"])}{main}</div>{f'<div class="pthumbs">{imgs}</div>' if imgs else ''}</div>
<div class="prose"><div class="pprice{'' if x['price'] else ' ask'}">{money(x["price"]) if x["price"] else "Ask for price"}</div>
{f'<p>{e(x["desc"])}</p>' if x["desc"] else ''}{f'<p>{e(x["note"])}</p>' if x["note"] else ''}
<dl class="facts">{facts}</dl>
<p class="mu">We confirm fitment against your car before anything is final.</p>
<div class="btns">{btn(enq(x["title"]), "Enquire about this part " + UI["arrow"])}{btn("{{R}}" + c["url"], "All " + e(c["name"]) + " parts", "g")}</div>{PVN}</div></div></section>
{relh}'''
        sch = {"@type": "Product", "name": x["title"], "description": base, "sku": x["key"], "url": f'{BASE}/{x["url"]}',
               "image": [(u if u.startswith("http") else f"{BASE}/{u}") for u in x["imgs"]] or [BASE + "/og.jpg"],
               "isAccessoryOrSparePartFor": {"@type": "Car", "name": c["full"]}}
        if x["oem"]: sch["mpn"] = x["oem"]
        if x["price"]:
            off = {"@type": "Offer", "price": f'{x["price"]:.2f}', "priceCurrency": "SGD", "url": f'{BASE}/{x["url"]}', "seller": {"@id": BASE + "/#org"}}
            if x["stock"] in ("in", "out"): off["availability"] = "https://schema.org/InStock" if x["stock"] == "in" else "https://schema.org/OutOfStock"
            elif x["stock"] == "order": off["availability"] = "https://schema.org/PreOrder"
            sch["offers"] = off
        shell(f'{x["url"]}index.html', title, desc, body, "brands",
              [("Brands", "brands/"), (c["bname"], f'brands/{c["b"]}/'), (c["name"], c["url"]), (x["title"], x["url"])], [sch], og_type="website",
              img=(sch["image"][0] if x["imgs"] else None), pri=0.6, lastmod=x["updated"] or TODAY)

WS_FAQ = [("What should a workshop send us?", "The car brand and model, the part, left or right if it matters, and a photo of the old part or the damage. A list of several parts is fine."),
          ("Do you give workshop prices?", "Where a price is listed it is shown on the part. For anything else, ask in your enquiry and we reply."),
          ("Can I ask for a part that is not in the catalogue?", "Yes. Send the car and part and we check what we can find.")]
OWN_FAQ = [("I do not know what the part is called. What do I do?", "Send a photo of the damage and your car model. Our guide on part names also helps. We reply with the part name and what we can find."),
           ("Do I need to know the car year?", "It helps. Send the model and, if you can, the year shown on your car documents. We confirm fitment before anything else."),
           ("Can I buy online here?", "You search, send an enquiry, and we reply. Prices are shown where set, and we confirm fitment and availability when you enquire.")]
def audience_pages():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">For workshops</p><h1>Parts for China &amp; EV cars, for Singapore workshops</h1>
<p class="lead">Search by car and part, send us your list, and we check fitment before we reply. We sell in Singapore to workshops and car owners.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div class="prose">
<h2>How a workshop uses this site</h2>
<ul class="ticks"><li>Search the catalogue by brand, model and part, in the words you already use.</li><li>Send the car and the part from the enquiry form. A list of several parts is fine.</li><li>Add a photo of the old part or the damage, front and back for lamps.</li><li>We confirm fitment against the car and reply.</li></ul>
<h2>What we focus on</h2><p>Mainly body parts: bumpers, lamps, mirrors, panels, grilles and trims, plus some other parts, for China and EV brands such as Tesla, BYD, Denza, MG, Zeekr and more. See all <a href="{{{{R}}}}brands/">brands</a>.</p>
<h2>Terms</h2><p class="mu">Trade pricing, delivery and warranty terms are given on enquiry.</p>
<div class="btns">{btn(enq("parts for our workshop"), "Send a parts list " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div>{PVN}</div>
<aside class="side"><div class="panel photo">{pic("door", "Car door panel, mood image", 700, 520, "(min-width:900px) 30vw, 100vw")}</div></aside></div></section>
<section class="sec alt"><div class="wrap narrow"><div class="sec-t"><h2>Workshop FAQ</h2></div>{faq_html(WS_FAQ)}</div></section>'''
    shell("for-workshops/index.html", "Parts for Workshops | EV Body Parts Singapore",
          "China and EV car body parts for Singapore workshops. Search by car and part, send your list, and EV Body Parts confirms fitment.",
          body, "ws", [("For workshops", "for-workshops/")], faq=WS_FAQ, pri=0.8)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">For car owners</p><h1>Find the right part for your China or EV car</h1>
<p class="lead">Not sure what the part is called? Tell us the car and what is damaged, and we help you find it.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div class="prose">
<h2>What to tell us</h2>
<ul class="ticks"><li>Your car brand and model, for example Tesla Model Y or BYD Atto 3.</li><li>The part, or a photo of the damage if you do not know its name.</li><li>Left or right, if the part comes in pairs. Left and right are as seen from the driver's seat.</li></ul>
<h2>Useful guides</h2><p><a href="{{{{R}}}}articles/tesla-model-y-tail-lamp-what-to-send/">Tesla Model Y tail lamp: what to send us</a><br><a href="{{{{R}}}}articles/china-ev-body-parts-what-to-check/">What to check before you buy body parts</a><br><a href="{{{{R}}}}articles/which-part-is-it/">Which part is it? Names explained</a></p>
<h2>Terms</h2><p class="mu">Fitting, delivery and warranty terms are given on enquiry.</p>
<div class="btns">{btn(enq("a part for my car"), "Send an enquiry " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div>{PVN}</div>
<aside class="side"><div class="panel photo">{pic("matte", "Matte black electric car, mood image", 700, 520, "(min-width:900px) 30vw, 100vw")}</div></aside></div></section>
<section class="sec alt"><div class="wrap narrow"><div class="sec-t"><h2>Car owner FAQ</h2></div>{faq_html(OWN_FAQ)}</div></section>'''
    shell("for-car-owners/index.html", "Parts for Car Owners | EV Body Parts Singapore",
          "Find body parts for your China or EV car in Singapore. Tell EV Body Parts the car and the part and we confirm fitment.",
          body, "own", [("For car owners", "for-car-owners/")], faq=OWN_FAQ, pri=0.8)

def about():
    extra = "".join([f'<div><dt>Company</dt><dd>{e(LEGAL)}</dd></div>' if LEGAL else "", f'<div><dt>UEN</dt><dd>{e(UEN)}</dd></div>' if UEN else "",
                     f'<div><dt>Address</dt><dd>{e(ADDRESS)}</dd></div>' if ADDRESS else ""])
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">About</p><h1>About EV Body Parts</h1><p class="lead">A Singapore seller of body parts for China and EV cars, for workshops and car owners.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div class="prose">
<h2>What we do</h2><p>{BRAND} sells body parts for China and EV cars in Singapore: bumpers, lamps and lights, mirrors, body panels, grilles and trims, plus some other parts. We sell to workshops and to car owners.</p>
<dl class="facts"><div><dt>Name</dt><dd>{BRAND}</dd></div><div><dt>Website</dt><dd>{DOMAIN}</dd></div><div><dt>Sells</dt><dd>Body parts for China and EV cars</dd></div><div><dt>Serves</dt><dd>Workshops and car owners in Singapore</dd></div>{extra}</dl>
<h2>How we work</h2><p>You search the catalogue or send us your car and the part. We check fitment against your car and reply. Prices are shown where set, and otherwise given on enquiry.</p>
<h2>Brands</h2><p>Our brand board shows {brand_names()}. Brand names are used only to describe which vehicles a part is for. See <a href="{{{{R}}}}brands/">all brands</a>.</p>
<h2>Photos</h2><p class="mu">Car photos on the site are {CRED.lower().replace("stock photos: ", "stock photos from ")}: mood images, not photos of {BRAND} stock. Photos on a part listing show that part.</p>
<div class="btns">{btn(enq("a part"), "Send an enquiry " + UI["arrow"])}{btn("{{R}}contact/", "Contact", "g")}</div>{PVN}</div>
<aside class="side"><div class="panel photo">{pic("showroom", "White sports car in a showroom, mood image", 700, 520, "(min-width:900px) 30vw, 100vw")}</div></aside></div></section>'''
    shell("about/index.html", "About EV Body Parts | China & EV Car Parts Singapore",
          "EV Body Parts sells body parts for China and EV cars in Singapore, for workshops and car owners. Search by car and part.",
          body, "about", [("About", "about/")], pri=0.6)

def contact():
    det = "".join([f'<div><dt>Phone</dt><dd><a href="tel:{PHONE.replace(" ", "")}">{e(PHONE)}</a></dd></div>' if PHONE else "",
                   f'<div><dt>WhatsApp</dt><dd><a href="https://wa.me/{WA}">{WA_DISPLAY}</a></dd></div>' if WA else "",
                   f'<div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{e(EMAIL)}</a></dd></div>' if EMAIL else "",
                   f'<div><dt>Address</dt><dd>{e(ADDRESS)}</dd></div>' if ADDRESS else "",
                   f'<div><dt>Company</dt><dd>{e(LEGAL)}{" (UEN " + e(UEN) + ")" if UEN else ""}</dd></div>' if LEGAL else ""])
    detsec = f'<h2>Details</h2><dl class="facts">{det}</dl>' if det else ""
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Contact</p><h1>Contact EV Body Parts</h1><p class="lead">The quickest way is to send us your car and the part.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div class="prose">
<h2>Send an enquiry</h2><p>Use the enquiry form with your car and part, and add a photo if you can. We reply after we confirm fitment.</p>
<div class="btns">{btn(enq("a part"), "Open the enquiry form " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div>{PVN}
{detsec}</div><aside class="side"><div class="panel photo">{pic("charge", "EV charging cable plugged into a car, mood image", 700, 520, "(min-width:900px) 30vw, 100vw")}</div></aside></div></section>'''
    shell("contact/index.html", "Contact | EV Body Parts Singapore",
          "Contact EV Body Parts, Singapore: send your car and part through the enquiry form and we confirm fitment.",
          body, "contact", [("Contact", "contact/")], pri=0.6)

def enquiry():
    brandopts = "".join(f'<option value="{b["key"]}">{e(b["name"])}</option>' for b in BRANDS)
    note = "" if WA else '<div class="demo-note" role="note"><b>Note.</b> Contact details are being added. Until then this form keeps your message in this browser only and does not send it. Please check back soon.</div>'
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Enquiry</p><h1>Tell us the car and the part</h1><p class="lead">We confirm fitment against your car and reply.</p></div></section>
<section class="sec tight"><div class="wrap two-c"><div>
{note}
<form class="form" id="enq-form" novalidate>
<div class="g2"><label>I am a<select name="as"><option value="workshop">Workshop</option><option value="owner">Car owner</option></select></label>
<label>Your name<input name="name" required autocomplete="name"></label></div>
<label>Phone or WhatsApp<input name="contact" required inputmode="tel" autocomplete="tel"></label>
<div class="g2"><label>Car brand<select name="brand" id="e-brand"><option value="">Choose</option>{brandopts}<option value="other">Other</option></select></label>
<label>Car model<input name="model" id="e-model" placeholder="e.g. Model Y" autocomplete="off"></label></div>
<label>Part you need<input name="part" id="e-part" required placeholder="e.g. tail lamp, left side" autocomplete="off"></label>
<label>Anything else <span class="mu">(year, damage, photo link)</span><textarea name="note" rows="4"></textarea></label>
<label class="chk"><input type="checkbox" name="consent" required><span>I agree that {BRAND} may use these details to reply to this enquiry. See the <a href="{{{{R}}}}privacy/">privacy notice</a>.</span></label>
<div class="err" id="enq-err" hidden>Please fill in your name, contact, the part, and tick the box.</div>
<button class="btn btn-p btn-l" type="submit">{UI["send"]} Send enquiry</button>
</form>
<div class="ok" id="enq-ok" hidden><h2>Thank you.</h2><p id="enq-ok-msg">Your enquiry is ready.</p><p><a class="btn btn-g" href="{{{{R}}}}catalogue/">Back to the catalogue</a></p></div>
</div><aside class="side"><div class="panel"><h3>A photo helps</h3><p class="mu">A photo of the old part, front and back for lamps, helps us match it.</p></div></aside></div></section>'''
    shell("enquiry/index.html", "Send an Enquiry | EV Body Parts Singapore",
          "Send your car and the part you need. EV Body Parts confirms fitment for China and EV cars and replies.",
          body, "", [("Enquiry", "enquiry/")], pri=0.6)

def privacy():
    who = f"{LEGAL}" + (f" (UEN {UEN})" if UEN else "") if LEGAL else BRAND
    mail = f'Send requests to <a href="mailto:{EMAIL}">{e(EMAIL)}</a>.' if EMAIL else (f'Send requests by WhatsApp to <a href="https://wa.me/{WA}">{WA_DISPLAY}</a>.' if WA else "")
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Privacy</p><h1>Privacy notice (PDPA)</h1><p class="lead">How {e(who)} handles personal data collected on this website.</p></div></section>
<section class="sec tight"><div class="wrap narrow prose">
<h2>What we collect</h2><p>When you send an enquiry we ask for your name, a phone number or WhatsApp number, your car brand and model, the part you need and any note you add.</p>
<h2>Why we use it</h2><p>To reply to your enquiry, confirm fitment and tell you about availability. We do not use it for anything else without asking you.</p>
<h2>Keeping and sharing</h2><p>We keep enquiry details only as long as needed to deal with your enquiry. We do not sell personal data.</p>
<h2>Your rights</h2><p>Under Singapore's Personal Data Protection Act you can ask to see or correct your personal data, or withdraw your consent. {mail}</p>
<h2>Cookies and analytics</h2><p>This site stores your preferences in your browser. It also counts taps on WhatsApp buttons. When you tap a WhatsApp button or send the enquiry form, your message is sent to us through WhatsApp.</p>
</div></section>'''
    shell("privacy/index.html", "Privacy Notice | EV Body Parts Singapore",
          "How EV Body Parts handles personal data from enquiries on this website, under Singapore's PDPA.",
          body, "", [("Privacy", "privacy/")], pri=0.3)
ARTICLES = [
 ("tesla-model-y-tail-lamp-what-to-send", "Tesla Model Y tail lamp: what to send us", "Tesla Model Y Tail Lamp: What to Send | EV Body Parts",
  "Which photos and details help us match a Tesla Model Y tail lamp, and how to describe left or right. A short checklist.", "tail",
  [("The short version", "Send the brand and model, which side you need, and two photos of the old lamp. That is usually enough for us to start checking."),
   ("1. Say left or right", "Left and right are as seen from the driver's seat, not from outside the car. If you are not sure, say where the damage is, for example &ldquo;the lamp on the side next to the fuel-side kerb&rdquo; is too vague, so a photo of the whole rear of the car is better."),
   ("2. Photograph the lamp", "Take one photo from outside the car showing the whole lamp and the area around it. If the lamp is already off the car, take a second photo of the back, where any markings or numbers are."),
   ("3. Tell us the car", "Brand, model and, if you can, the year shown on your car documents. Say if the car has been modified, repainted or has had earlier repairs to the rear."),
   ("4. Mention what else is damaged", "A broken lamp often comes with bumper or reflector damage. Tell us, so we can check the right pieces together."),
   ("What happens next", "We compare your photos with the part and confirm fitment before we reply. Lamps for the same model can differ, so we do not guess from the model name alone.")]),
 ("china-ev-body-parts-what-to-check", "Body parts for China EVs in Singapore: what to check before you buy", "China EV Body Parts: What to Check Before You Buy",
  "A buyer's checklist for body parts on China and EV cars in Singapore: model, side, sensors, paint, and what is included.", "charge",
  [("Why a checklist helps", "Body parts look similar across models, but small differences decide whether a part fits. A few checks before you pay save a return trip."),
   ("Match the exact model", "Give the brand and the model name as written on the car. Parts for two models from the same brand are often different, even when they look alike."),
   ("Check the side", "Lamps, mirrors, fenders and doors come left and right. Left and right are as seen from the driver's seat."),
   ("Sensors, cameras and holes", "If your bumper has parking sensors, a camera or other fittings, tell the seller. Ask whether the part you are buying has the same openings."),
   ("Paint and finish", "Ask whether the part is bare, primed or painted, and who matches the colour. Never assume."),
   ("What is included", "Ask whether brackets, clips, bulbs or fixings come with the part, and whether the part is new. Ask any seller, including us, about returns and warranty, and get the answer in writing. Ask us the same when you enquire."),
   ("Send photos", "Photos of the old part and the damaged area let the seller compare before you commit.")]),
 ("which-part-is-it", "Which part is it? Bumper, fender, reflector and trim names explained", "Car Part Names Explained: Bumper, Fender, Reflector",
  "Plain-English names for car body parts: bumper, bumper trim, fender, bonnet, tailgate, reflector, grille and more.", "head",
  [("Why names matter", "The same part can have several names. If you search or enquire with a name we also recognise, we can find it faster. Here are the common ones."),
   ("Bumper and bumper trim", "The bumper is the large piece at the front or rear of the car. Bumper trim covers the strips, lip and garnish attached to or around it. People also say bumper lip or sticker bumper."),
   ("Rear reflector", "A reflector is the red, lamp-like panel low on the rear bumper. It is not the tail lamp."),
   ("Fender and bonnet", "The fender (also called the wing) is the panel beside the front wheel. The bonnet, called the hood in some countries, is the lid over the front of the car."),
   ("Tailgate", "The tailgate is the rear lid of a hatchback or SUV. Some people say boot, trunk lid or liftgate."),
   ("Lamps", "Headlamp or headlight is at the front. Tail lamp or taillight is at the rear, and some people also say brake light. A fog lamp is a small extra lamp, usually low at the front."),
   ("Mirror, grille and arch", "The side mirror is also called a wing mirror. The grille is the vented panel at the front. The wheel arch lining is the liner inside the wheel arch."),
   ("Still not sure?", "Send a photo and the car model. We tell you the part name and check what we can find.")]),
]

def articles():
    cards = ""
    for slug, h1, title, desc, ph, secs in ARTICLES:
        cards += f'<a class="tc rv" href="{{{{R}}}}articles/{slug}/"><div class="tc-ph">{pic(ph, "Mood image", 900, 600, "(min-width:900px) 30vw, 100vw")}</div><div class="tc-b"><p class="kick">Guide</p><h3>{h1.replace("&", "&amp;")}</h3><p>{e(desc)}</p><span class="more">Read the guide {UI["arrow"]}</span></div></a>'
        paras = "".join(f"<h2>{a}</h2><p>{b}</p>" for a, b in secs)
        sch = [{"@type": "Article", "headline": h1, "description": desc, "datePublished": "2026-10-31", "dateModified": "2026-10-31",
                "author": {"@id": BASE + "/#org"}, "publisher": {"@id": BASE + "/#org"}, "image": BASE + "/og.jpg", "mainEntityOfPage": f"{BASE}/articles/{slug}/"}]
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Guide</p><h1>{h1.replace("&", "&amp;")}</h1><p class="lead">{e(desc)}</p></div></section>
<section class="sec tight"><div class="wrap two-c"><article class="prose">{paras}
<div class="btns">{btn(enq("a part"), "Send us your car and part " + UI["arrow"])}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div>{PVN}</article>
<aside class="side"><div class="panel photo">{pic(ph, "Mood image, not EV Body Parts stock", 700, 520, "(min-width:900px) 30vw, 100vw")}</div></aside></div></section>'''
        shell(f"articles/{slug}/index.html", title, desc, body, "", [("Guides", "articles/"), (h1, f"articles/{slug}/")], sch, og_type="article", pri=0.6, lastmod="2026-10-31")
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<p class="kick">Guides</p><h1>Guides for buyers</h1><p class="lead">Short, practical notes on getting the right body part.</p></div></section>
<section class="sec tight"><div class="wrap"><div class="two three">{cards}</div></div></section>'''
    shell("articles/index.html", "Guides | EV Body Parts Singapore",
          "Short guides on getting the right body part for China and EV cars in Singapore: what to send, what to check, part names.",
          body, "", [("Guides", "articles/")], pri=0.6)

def notfound():
    body = f'''<section class="ph-hd"><div class="wrap"><p class="kick">404</p><h1>Page not found</h1><p class="lead">The page may have moved. Search the catalogue, or go to the homepage.</p></div></section>
<section class="sec tight"><div class="wrap">{search_box("nq", big=False, action="/catalogue/")}<p style="margin-top:24px"><a class="btn btn-g" href="/">Back to the homepage</a></p></div></section>'''
    shell("404.html", "Page Not Found | EV Body Parts", "Page not found. Search the EV Body Parts catalogue or go to the homepage.", body, index=False)

# ------------------------------------------------------------------ data.js (snapshot for the browser; ev.js refreshes it live)
def datajs():
    def carrec(c): return {"key": c["key"], "b": c["b"], "slug": c["slug"], "name": c["name"], "alias": c.get("alias") or [], "years": c.get("years") or "", "photo": c.get("photo") or ""}
    prods = [{"key": x["key"], "m": x["car"]["key"], "p": x["p"], "pn": x["pn"], "title": x["title"], "side": x["side"], "oem": x["oem"], "grade": x["grade"],
              "price": x["price"], "stock": x["stock"], "photos": x["photos_raw"], "desc": x["desc"], "note": x["note"], "created": x["created"], "url": x["url"]} for x in PRODS]
    data = {"read": TODAY, "base": BASE, "wa": WA, "phone": PHONE, "email": EMAIL, "brand": BRAND, "staff": STAFF_URL, "appId": APP_ID, "api": API_BASES,
            "status": STOCK_L,
            "brands": [{"key": b["key"], "name": b["name"], "alias": b.get("alias") or [], "order": b.get("order") or 0} for b in BRANDS],
            "cars": [carrec(c) for c in CARS],
            "parts": [{"slug": p[0], "name": p[1], "cat": p[2], "syn": p[3]} for p in PARTS],
            "generic": [{"w": g[0], "map": g[1]} for g in GENERIC],
            "icons": IC, "special": sorted(SPECIAL), "art": ART, "illus": ILLUS, "products": prods, "photoFiles": {g: v[0] for g, v in PHOTO_FILES.items()}}
    (OUT / "data.js").write_text("window.EV_DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")

def statics():
    for f in ("favicon.ico", "favicon-48.png", "icon-192.png", "icon-512.png", "apple-touch-icon.png", "og.jpg", "logo-96.png", "mark.svg"):
        shutil.copy(HERE / "assets" / f, OUT / f)
    for f in ("ev.css", "ev.js", "wa.js"):
        shutil.copy(HERE / f, OUT / f)
    for g, (path, raw) in PHOTO_FILES.items():
        (OUT / path).parent.mkdir(parents=True, exist_ok=True); (OUT / path).write_bytes(raw)
    (OUT / "site.webmanifest").write_text(json.dumps({"name": BRAND, "short_name": BRAND, "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"}],
        "theme_color": "#07090B", "background_color": "#07090B", "display": "standalone", "start_url": "./"}, indent=1))
    (OUT / f"{KEY}.txt").write_text(KEY)
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Applebot-Extended", "DuckAssistBot"]
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {BASE}/sitemap.xml\n")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
        "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{lm}</lastmod><priority>{pr}</priority></url>\n" for u, pr, lm in pages) + "</urlset>\n")
    L = [f"# {BRAND}", "", f"> {BRAND} ({DOMAIN}) sells body parts for China and EV cars in Singapore, to workshops and car owners. {TAG}.", "",
         "## Facts", f"- Name: {BRAND}", f"- Website: {BASE}/", "- Sells: body parts (bumpers, lamps and lights, mirrors, body panels, grilles and trims) and some other parts for China and EV cars",
         "- Serves: workshops and car owners in Singapore", "- Prices: shown in S$ where set; otherwise 'Ask for price'. Fitment is confirmed on enquiry."]
    if LEGAL: L.append(f"- Company: {LEGAL}" + (f" (UEN {UEN})" if UEN else ""))
    if ADDRESS: L.append(f"- Address: {ADDRESS}")
    if WA: L.append(f"- WhatsApp: {WA_DISPLAY}")
    if PHONE: L.append(f"- Phone: {PHONE}")
    if EMAIL: L.append(f"- Email: {EMAIL}")
    L += ["", "## Brands (names used only to describe fitment)"] + [f"- {b['name']}: {BASE}/brands/{b['key']}/" for b in BRANDS] + \
         ["", "## Part types"] + [f"- {c[1]}: {BASE}/parts/{c[0]}/" for c in CATS] + \
         ["", "## Pages", f"- Catalogue search: {BASE}/catalogue/", f"- For workshops: {BASE}/for-workshops/", f"- For car owners: {BASE}/for-car-owners/",
          f"- Guides: {BASE}/articles/", f"- Sitemap: {BASE}/sitemap.xml"]
    (OUT / "llms.txt").write_text("\n".join(L) + "\n")
    (OUT / "htaccess.txt").write_text(f"""# {BRAND} - go-live notes only (do NOT upload as .htaccess into the preview folder).
# Preview URL: https://pageonesingapore.com/preview/ev-body-parts/ (hidden by a server header on the parent /preview/ folder; pages carry no noindex).
# At go-live:
#  1. Point {DOMAIN} at this folder (addon domain), SSL on. BASE in build.py is already https://{DOMAIN}.
#  2. Set WA (digits with country code), PHONE, EMAIL, LEGAL, UEN, ADDRESS in build.py and rebuild.
#  3. Add a Controller Client row for site id 'ev-body-parts' (wa.js tap counter) when WA is set.
#  4. Add {DOMAIN} to both crawler monitor lists (Controller crawlerMonitor COLLECTED + Bridge crawlerLogs CRAWLER_DOMAINS).
#  5. Force https + one host:
RewriteEngine On
RewriteCond %{{HTTPS}} off
RewriteRule ^ https://%{{HTTP_HOST}}%{{REQUEST_URI}} [L,R=301]
ErrorDocument 404 /404.html
# 6. Submit {BASE}/sitemap.xml to Search Console + Bing; IndexNow key file: /{KEY}.txt
""")


# ====================================================================== v2 (1 Nov 2026): menu + cart + shorter pages (these definitions override the ones above)
SVG_CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 4h2.2l2.1 10.2a2 2 0 0 0 2 1.6h7.6a2 2 0 0 0 2-1.5L20.5 8H6.2"/><circle cx="10" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/></svg>'
PVN = ""
MENU = [("catalogue/", "Search the catalogue", "cat"), ("brands/", "Brands", "brands"), ("parts/", "Parts", "parts"), ("for-workshops/", "For workshops", "ws"),
        ("for-car-owners/", "For car owners", "own"), ("articles/", "Guides", "guides"), ("about/", "About", "about"), ("contact/", "Contact", "contact")]
def enq(text, r="{{R}}"):
    return f"https://wa.me/{WA}?text={quote(f'Hi {BRAND}, I am looking for: {text}. (from website)')}" if WA else f"{r}contact/"
def wa_btn(text, label="WhatsApp us", kind="p"):
    return btn(enq(text), UI["wa"] + " " + label, kind)
def addbtn(key, title, car, part, price, side="", ask=False, label="Add to cart", cls="btn btn-p btn-s"):
    a = f'data-add data-key="{e(key)}" data-title="{e(title)}" data-car="{e(car)}" data-part="{e(part)}" data-side="{e(side)}"'
    if price: a += f' data-price="{price}"'
    if ask: a += ' data-ask="1"'
    return f'<button type="button" class="{cls}" {a}>{label}</button>'

def card_static(x, r="{{R}}"):
    media = f'<img src="{e(disp(x["imgs"][0]))}" alt="{e(x["title"])}" width="88" height="88" loading="lazy" decoding="async" onerror="this.remove()">' if x["imgs"] else (f'<img class="art" src="{ART[x["p"]]}" alt="Illustrative image" title="{e(ILLUS)}" width="88" height="88" loading="lazy" decoding="async" onerror="this.remove()"><span class="illus-t">Illustrative</span>' if x["p"] in ART else "")
    add = f'<a class="btn btn-p btn-s" href="{e(enq(x["title"] + " (specialist check)"))}">Check fitment</a>' if x["p"] in SPECIAL else addbtn(x["key"], x["title"], x["car"]["full"], x["pn"], x["price"], x["side"])
    return (f'<article class="rc"><div class="rc-ic">{ico(x["p"])}{media}</div><div class="rc-b"><span class="chip">{e(x["car"]["full"])}</span>'
            f'<h3>{e(x["title"])}</h3><p class="rc-t">{e(x["pn"])}{f" &middot; OE {e(x["oem"])}" if x["oem"] else ""}</p>'
            f'<div class="rc-m">{f"<span class=\"pill side\">{SIDE_L[x["side"]]}</span>" if x["side"] in SIDE_L else ""}{pill_html(x)}{price_html(x)}</div>'
            f'<div class="rc-a">{add}<a class="btn btn-g btn-s" href="{r}{x["url"]}">Details</a></div></div></article>')
def list_html(items, name, lim=9):
    if not items: return f'<div class="empty"><p>No {e(name + " ") if name else ""}listings yet. Ask us on WhatsApp and we check.</p>{wa_btn((name + " part").strip(), "Ask on WhatsApp")}</div>'
    return '<div class="rgrid">' + "".join(card_static(x) for x in items[:lim]) + '</div>' + (f'<p class="seeall"><a class="btn btn-g" href="{{{{R}}}}catalogue/">See all {len(items)}</a></p>' if len(items) > lim else "")

def shell(path, title, desc, body, active="", crumbs=None, schema=None, og_type="website", index=True, faq=None, img=None, pri=0.7, preload=None, lastmod=None):
    assert len(title) < 60, (path, len(title), title)
    assert len(desc) < 160, (path, len(desc), desc)
    depth = path.count("/")
    r = "../" * depth
    url = BASE + "/" + ("" if path == "index.html" else path.replace("index.html", ""))
    ld = [dict(ORG), dict(SITE)] if path == "index.html" else [dict(ORG)]
    if crumbs:
        ld.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + "/" + u} for i, (n, u) in enumerate([("Home", "")] + crumbs)]})
    if faq: ld.append(faq_ld(faq))
    if schema: ld.extend(schema)
    ldj = json.dumps({"@context": "https://schema.org", "@graph": ld}, ensure_ascii=False).replace("</", "<\\/")
    nav = "".join(f'<a href="{r}{u}"{" aria-current=\"page\"" if k == active else ""}>{n}</a>' for u, n, k in MENU)
    cr = ""
    if crumbs:
        cr = '<nav class="crumbs" aria-label="Breadcrumb"><a href="' + r + '">Home</a>' + "".join(
            (f'<span>/</span><a href="{r}{u}">{e(n)}</a>' if i < len(crumbs) - 1 else f'<span>/</span><span aria-current="page">{e(n)}</span>') for i, (n, u) in enumerate(crumbs)) + "</nav>"
    body = body.replace("{{CRUMBS}}", cr).replace("{{R}}", r)
    ogi = img or BASE + "/og.jpg"
    dims = '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">' if not img else ""
    wa_link = f"https://wa.me/{WA}?text={quote(f'Hi {BRAND}, I have a question. (from website)')}" if WA else f"{r}contact/"
    foot = "".join(f'<a href="{r}{u}">{n}</a>' for u, n in [("parts/", "Parts"), ("brands/", "Brands"), ("articles/", "Guides"), ("about/", "About"), ("contact/", "Contact"), ("privacy/", "Privacy")])
    doc = f"""<!doctype html>
<html lang="en-SG" class="no-js" data-root="{r}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="{BRAND}"><meta property="og:locale" content="en_SG"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{ogi}">{dims}<meta property="og:image:alt" content="{e(BRAND)} - {e(TAG)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{ogi}">
<link rel="icon" href="{r}favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="{r}icon-192.png"><link rel="apple-touch-icon" href="{r}apple-touch-icon.png"><link rel="manifest" href="{r}site.webmanifest">
<meta name="theme-color" content="#07090B">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Saira:ital,wght@0,500;0,600;0,700;0,800;1,600;1,700;1,800&display=swap">
{'<link rel="preconnect" href="https://images.unsplash.com">' if preload else ''}
<link rel="stylesheet" href="{r}{asset('ev.css')}">
<script>document.documentElement.classList.remove('no-js');document.documentElement.classList.add('js');window.EV_ROOT="{r}";</script>
<script type="application/ld+json">{ldj}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hd"><div class="wrap">
{logo_html(r)}
<div class="hd-r"><button type="button" class="cartbtn" data-cart-open aria-label="Open cart">{SVG_CART}<span class="cbadge" data-cart-count hidden>0</span></button>
<button class="burger" aria-label="Open menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button></div>
</div></header>
<div class="scrim" data-scrim></div>
<nav class="nav" id="nav" aria-label="Main"><div class="nav-h"><b>Menu</b><button type="button" class="nav-x" data-menu-close aria-label="Close menu">&times;</button></div>{nav}<a class="nav-cta" href="{wa_link}">{UI["wa"]} WhatsApp us</a></nav>
<main id="main">
{body}
</main>
<footer class="ft"><div class="wrap">
<div class="ft-row">{logo_html(r)}<nav class="ft-l" aria-label="Footer">{foot}</nav></div>
<div class="ft-b"><span>&copy; {datetime.date.today().year} {BRAND} &middot; {DOMAIN} &middot; <a href="{wa_link}">WhatsApp {WA_DISPLAY}</a></span><span>Brand names only describe fitment. Stock photos are mood images. <a href="{STAFF_URL}" rel="nofollow noopener">Staff</a></span></div>
</div></footer>
<a class="fab" href="{wa_link}" aria-label="WhatsApp us">{UI["wa"]}</a>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script src="{r}{asset('data.js')}" defer></script><script src="{r}{asset('ev.js')}" defer></script><script src="{r}{asset('wa.js')}" defer></script>
</body>
</html>
"""
    f = OUT / path
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc)
    if index:
        pages.append(("/" + ("" if path == "index.html" else path.replace("index.html", "")), pri, lastmod or TODAY))

def home_faq():
    return [("Do you have my part?", "Search by car and part. If it is not listed, add it to the cart anyway and we check on WhatsApp."),
            ("Who do you sell to?", f"Workshops and car owners in Singapore. {brand_names()}."),
            ("Are prices shown?", "Yes, in S$ where set. Otherwise the part says Ask for price and we reply on WhatsApp.")]

def home():
    faq = home_faq()
    cats = "".join(f'''<a class="cc rv" href="{{{{R}}}}parts/{c[0]}/"><span class="cc-ic">{ico(c[4])}</span><h3>{e(c[1])}</h3><p>{e(c[2])}</p></a>''' for c in CATS)
    steps = [("Search", "Type your car and the part."), ("Add to cart", "Add what you need."), ("Send on WhatsApp", "We confirm fitment and reply.")]
    st = "".join(f'<li class="rv"><span class="n">{i + 1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(steps))
    new = PRODS[:6]
    body = f'''<section class="hero">
<div class="hero-bg" aria-hidden="true">{pic("hero", "Car tail light in the dark (mood image)", 2000, 1333, "100vw", True, "kb")}</div>
<div class="wrap hero-in">
<p class="eyebrow">China &amp; EV car parts &middot; Singapore</p>
<h1>Body parts for China &amp; EV cars, <em>found fast.</em></h1>
<p class="lead">Search by car and part. For workshops and car owners.</p>
{search_box("hq")}
</div></section>
<section class="strip"><div class="wrap">{brandchips()}</div></section>
<section class="sec tight"><div class="wrap"><div class="cgrid">{cats}</div></div></section>
<section class="sec alt tight" data-new-sec{"" if new else " hidden"}><div class="wrap">
<div class="sec-t rv"><p class="kick">Newly added</p><h2>Latest parts</h2></div>
<div data-list="new:" data-limit="6">{list_html(new, "", 6) if new else ""}</div>
</div></section>
<section class="sec tight"><div class="wrap"><ol class="steps">{st}</ol></div></section>
<section class="sec alt tight"><div class="wrap narrow">
<div class="sec-t rv"><h2>Quick answers</h2></div>
{faq_html(faq)}
</div></section>'''
    shell("index.html", "EV Body Parts | China & EV Body Parts in Singapore",
          "Search body parts for Tesla, BYD, Denza, MG, Zeekr and more China and EV cars. EV Body Parts serves workshops and car owners in Singapore.",
          body, "", faq=faq, pri=1.0, preload=True)

def catalogue():
    brandopts = "".join(f'<option value="{b["key"]}">{e(b["name"])}</option>' for b in BRANDS)
    partopts = "".join(f'<option value="{p[0]}">{e(p[1])}</option>' for p in PARTS)
    links = "".join(f'<li><a href="{{{{R}}}}brands/{b["key"]}/">{e(b["name"])} parts</a></li>' for b in BRANDS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Search the catalogue</h1><p class="lead">Brand, model and part, or use the filters.</p></div></section>
<section class="sec tight"><div class="wrap">
<form class="sbox" id="cat-form" role="search" action="" method="get" data-search="cq">
<label class="sr" for="cq-q">Search</label>
<div class="srow">{UI["search"]}<input id="cq-q" class="sin" name="q" type="search" autocomplete="off" autocapitalize="off" spellcheck="false" placeholder="e.g. Tesla Model Y tail lamp"><button class="btn btn-p" type="submit">Search</button></div>
<div class="filters"><label>Brand<select name="brand" id="f-brand"><option value="">All brands</option>{brandopts}</select></label>
<label>Model<select name="model" id="f-model"><option value="">All models</option></select></label>
<label>Part<select name="part" id="f-part"><option value="">All parts</option>{partopts}</select></label>
<button class="btn btn-g btn-s" type="button" id="f-clear">Clear</button></div>
<p class="try"><span>Try:</span>{"".join(f'<button type="button" data-try="{e(t)}">{e(t)}</button>' for t in TRY[:4])}</p>
</form>
<div class="count" id="cat-count" aria-live="polite"></div>
<div class="sres full" id="cat-res"></div>
<div class="sec-t" style="margin-top:44px"><h2>Browse by brand</h2></div>
<ul class="plain brandlist">{links}</ul>
</div></section>'''
    ld = [{"@type": "ItemList", "name": f"Brands in the {BRAND} catalogue", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": f'{b["name"]} body parts', "url": f'{BASE}/brands/{b["key"]}/'} for i, b in enumerate(BRANDS)]}]
    shell("catalogue/index.html", "Catalogue | EV Body Parts Singapore",
          "Search China and EV car body parts by brand, model and part, like Tesla Model Y tail lamp. Add to cart and send your order on WhatsApp.",
          body, "cat", [("Catalogue", "catalogue/")], ld, pri=0.9)

def parts_hub():
    cards = "".join(f'''<a class="cc rv" href="{{{{R}}}}parts/{c[0]}/"><span class="cc-ic">{ico(c[4])}</span><h3>{e(c[1])}</h3><p>{e(c[2])}</p></a>''' for c in CATS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Parts for China &amp; EV cars</h1><p class="lead">Pick a part type.</p></div></section>
<section class="sec tight"><div class="wrap"><div class="cgrid">{cards}</div></div></section>'''
    shell("parts/index.html", "Car Body Parts by Type | EV Body Parts",
          "Bumpers, lamps and lights, mirrors, body panels, grilles and trims for China and EV cars in Singapore. Choose a part type.",
          body, "parts", [("Parts", "parts/")], pri=0.8)

def part_pages():
    for c in CATS:
        slug, name, line, ps, icon = c
        h1, desc, paras = PART_COPY[slug]
        title = fit(f"{name} for China & EV Cars | {BRAND}", f"{name} for China & EV Cars")
        chips = "".join(f'<a class="bchip" href="{{{{R}}}}catalogue/?part={p}">{e(PART[p][1])}</a>' for p in ps)
        items = [x for x in PRODS if x["p"] in ps]
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>{h1.replace("&", "&amp;")}</h1><p class="lead">{e(paras[0])}</p></div></section>
<section class="sec tight"><div class="wrap"><div class="bchips" style="margin-bottom:28px">{chips}</div>
<div class="sres full" data-list="parts:{','.join(ps)}" data-limit="9">{list_html(items, name)}</div>
<p style="margin-top:28px">{wa_btn(name, "Ask on WhatsApp", "g")}</p></div></section>'''
        shell(f"parts/{slug}/index.html", title, desc, body, "parts", [("Parts", "parts/"), (name, f"parts/{slug}/")], pri=0.8)

def brands_hub():
    def mod(b):
        cs = CARS_BY_BRAND[b["key"]]
        return ", ".join(c["name"] for c in cs) if cs else "Ask us for your model"
    cards = "".join(f'<a class="cc rv" href="{{{{R}}}}brands/{b["key"]}/"><span class="cc-ic bn">{e(b["name"][:2].upper())}</span><h3>{e(b["name"])}</h3><p>{e(mod(b))}</p></a>' for b in BRANDS)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Car brands</h1><p class="lead">Pick your brand.</p></div></section>
<section class="sec tight"><div class="wrap"><div class="cgrid">{cards}</div></div></section>'''
    shell("brands/index.html", "Car Brands | EV Body Parts Singapore",
          "China and EV car brands we list body parts for: Tesla, BYD, Denza, MG, Maxus, Chery, Zeekr and more. Choose your brand.",
          body, "brands", [("Brands", "brands/")], pri=0.8)

def brand_pages():
    for b in BRANDS:
        slug, name = b["key"], b["name"]
        cs = CARS_BY_BRAND[slug]
        if cs:
            mnames = [c["name"] for c in cs]
            intro = b.get("intro") or (f"Pick your {name} first. Some models have an older and a newer version with different bumpers and lamps." if any(" — " in c["name"] for c in cs) else f"Body parts for {name} {ml(mnames)}. Pick your model.")
            desc = short(f"{name} body parts in Singapore for {ml(mnames)}. Add to cart and send your order on WhatsApp.")
            chips = "".join(f'<a class="mtile" href="{{{{R}}}}{c["url"]}"><span class="mt-ic">{UI["car"]}</span><span class="mt-b"><b>{e(c["name"])}</b>{f'<small>{e(c["years"])}</small>' if c.get("years") else ''}</span>{UI["arrow"]}</a>' for c in cs)
        else:
            intro = b.get("intro") or f"No {name} model is listed yet. Tell us your model and part on WhatsApp."
            desc = short(f"{name} body parts in Singapore: tell us your model and part and EV Body Parts checks what we can find.")
            chips = ""
        title = fit(f"{name} Body Parts in Singapore | {BRAND}", f"{name} Body Parts in Singapore")
        items = [x for x in PRODS if x["car"]["b"] == slug]
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>{e(name)} body parts</h1><p class="lead">{e(intro)}</p>{f'<h2 class="mt-h">Choose your {e(name)}</h2><div class="mtiles">{chips}</div>' if chips else ''}</div></section>
<section class="sec tight"><div class="wrap">
<div class="sres full" data-list="brand:{slug}" data-limit="9" data-name="{e(name)}">{list_html(items, name)}</div>
<p style="margin-top:28px">{wa_btn(name + " part", "Ask on WhatsApp", "g")}</p></div></section>'''
        shell(f"brands/{slug}/index.html", title, desc, body, "brands", [("Brands", "brands/"), (name, f"brands/{slug}/")], pri=0.7)

def car_pages():
    for c in CARS:
        name, full = c["name"], c["full"]
        items = PBYCAR.get(c["key"], [])
        title = fit(f"{full} Body Parts Singapore | {BRAND}", f"{full} Body Parts Singapore", f"{full} Body Parts")
        desc = short(f"{full} body parts in Singapore: bumpers, lamps, mirrors and panels. Add to cart and send your order on WhatsApp.")
        def chip(pk):
            pn = PART[pk][1]
            if pk in SPECIAL: return f'<a class="bchip chipsp" href="{e(enq(full + " " + pn + " (specialist check)"))}">{e(pn)}</a>'
            return addbtn(f'ask:{c["key"]}:{pk}', f'{full} {pn}', full, pn, None, ask=True, label=e(pn), cls="bchip chipbtn")
        def arpic(a):
            u = ART.get(a[3][0]) if a[0] != "glass" else None
            if a[0] == "special": u = ART["underbody-shield"]
            return f'<img src="{u}" alt="{e(a[1])}: illustrative image" width="64" height="64" loading="lazy" decoding="async" title="{e(ILLUS)}" onerror="this.remove()">' if u else ""
        areas = "".join(f'<details class="area"{" open" if i == 0 else ""}><summary><span class="ar-ic">{ico(a[2])}{arpic(a)}</span><b>{e(a[1])}</b><span class="ar-n">{len(a[3])}</span></summary>'
                        f'{"<p class=ar-note>Safety and structure parts: we check these one by one. Ask on WhatsApp.</p>" if a[0] == "special" else ""}<div class="bchips">{"".join(chip(pk) for pk in a[3])}</div>'
                        f'{"<p class=illus>" + e(ILLUS) + "</p>" if arpic(a) else ""}</details>' for i, a in enumerate(AREAS))
        base = name.split(" — ")[0]
        gens = [o for o in CARS_BY_BRAND[c["b"]] if o["key"] != c["key"] and " — " in (o["name"] + name) and o["name"].split(" — ")[0] == base]
        sibs = "".join(f'<a class="bchip" href="{{{{R}}}}{o["url"]}">{e(o["name"])}</a>' for o in CARS_BY_BRAND[c["b"]] if o["key"] != c["key"])
        yrs = f' ({e(c["years"])})' if c.get("years") else ""
        genl = (f'<p class="gen-n">Not sure? This page is for {e(name.split(" — ")[1] if " — " in name else name)}{yrs}. Other version: '
                + ", ".join(f'<a href="{{{{R}}}}{o["url"]}">{e(o["name"].split(" — ")[1] if " — " in o["name"] else o["name"])}{f" ({e(o["years"])})" if o.get("years") else ""}</a>' for o in gens)
                + '. Send your build year or a photo on WhatsApp and we confirm.</p>') if gens else ""
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>{e(full)} body parts</h1><p class="lead">Pick an area, then tap a part to add it to your cart. Price on request.</p>{genl}
<div class="areas">{areas}</div></div></section>
<section class="sec tight"><div class="wrap">
<div class="sres full" data-list="car:{c["key"]}" data-limit="12" data-name="{e(full)}">{list_html(items, full, 12)}</div>
{f'<div class="sec-t" style="margin-top:36px"><h2>Other {e(c["bname"])} models</h2></div><div class="bchips">{sibs}</div>' if sibs else ''}</div></section>'''
        shell(f'{c["url"]}index.html', title, desc, body, "brands", [("Brands", "brands/"), (c["bname"], f'brands/{c["b"]}/'), (name, c["url"])], pri=0.7)

def product_pages():
    for x in PRODS:
        c = x["car"]
        title = fit(f'{x["title"]} | {BRAND}', f'{x["title"]} Singapore', x["title"])
        base = x["desc"] or x["note"] or f'{x["title"]} for the {c["full"]}, sold in Singapore.'
        desc = short(f'{base} {"Price " + money(x["price"]) + "." if x["price"] else "Ask for price."} Order on WhatsApp.')
        facts = "".join([f'<div><dt>Car</dt><dd><a href="{{{{R}}}}{c["url"]}">{e(c["full"])}</a></dd></div>', f'<div><dt>Part</dt><dd>{e(x["pn"])}</dd></div>',
                         f'<div><dt>Side</dt><dd>{SIDE_L[x["side"]]}</dd></div>' if x["side"] in SIDE_L else "",
                         f'<div><dt>OE no.</dt><dd>{e(x["oem"])}</dd></div>' if x["oem"] else "",
                         f'<div><dt>Grade</dt><dd>{e(x["grade"])}</dd></div>' if x["grade"] else "",
                         f'<div><dt>Stock</dt><dd>{STOCK_L[x["stock"]]}</dd></div>' if x["stock"] in STOCK_L else ""])
        imgs = "".join(f'<img src="{e(disp(u))}" alt="{e(x["title"])} photo {i + 1}" width="144" height="108" loading="lazy" decoding="async">' for i, u in enumerate(x["imgs"][1:5], 1))
        main = f'<img src="{e(disp(x["imgs"][0]))}" alt="{e(x["title"])}" width="800" height="600" decoding="async" fetchpriority="high" onerror="this.remove()">' if x["imgs"] else ""
        rel = [y for y in PBYCAR[c["key"]] if y["key"] != x["key"]][:6]
        relh = f'<section class="sec alt tight"><div class="wrap"><div class="sec-t"><h2>More for the {e(c["full"])}</h2></div><div class="rgrid">{"".join(card_static(y) for y in rel)}</div></div></section>' if rel else ""
        body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>{e(x["title"])}</h1></div></section>
<section class="sec tight"><div class="wrap two-c"><div>
<div class="pgal">{ico(x["p"])}{main}</div>{f'<div class="pthumbs">{imgs}</div>' if imgs else ''}</div>
<div class="prose"><div class="pprice{'' if x['price'] else ' ask'}">{money(x["price"]) if x["price"] else "Ask for price"}</div>
{f'<p>{e(x["desc"])}</p>' if x["desc"] else ''}{f'<p>{e(x["note"])}</p>' if x["note"] else ''}
<dl class="facts">{facts}</dl>
<div class="btns">{wa_btn(x["title"] + " (specialist check)", "Check fitment & price") if x["p"] in SPECIAL else addbtn(x["key"], x["title"], c["full"], x["pn"], x["price"], x["side"], cls="btn btn-p")}{"" if x["p"] in SPECIAL else wa_btn(x["title"], "Check fitment & price", "g")}</div></div></div></section>
{relh}'''
        sch = {"@type": "Product", "name": x["title"], "description": base, "sku": x["key"], "url": f'{BASE}/{x["url"]}',
               "image": [(u if u.startswith("http") else f"{BASE}/{u}") for u in x["imgs"]] or [BASE + "/og.jpg"],
               "isAccessoryOrSparePartFor": {"@type": "Car", "name": c["full"]}}
        if x["oem"]: sch["mpn"] = x["oem"]
        if x["price"]:
            off = {"@type": "Offer", "price": f'{x["price"]:.2f}', "priceCurrency": "SGD", "url": f'{BASE}/{x["url"]}', "seller": {"@id": BASE + "/#org"}}
            if x["stock"] in ("in", "out"): off["availability"] = "https://schema.org/InStock" if x["stock"] == "in" else "https://schema.org/OutOfStock"
            elif x["stock"] == "order": off["availability"] = "https://schema.org/PreOrder"
            sch["offers"] = off
        shell(f'{x["url"]}index.html', title, desc, body, "brands",
              [("Brands", "brands/"), (c["bname"], f'brands/{c["b"]}/'), (c["name"], c["url"]), (x["title"], x["url"])], [sch],
              img=(sch["image"][0] if x["imgs"] else None), pri=0.6, lastmod=x["updated"] or TODAY)

WS_FAQ = [("What should a workshop send?", "Car brand and model, the part, left or right, and a photo of the old part."),
          ("Can I ask for a part that is not listed?", "Yes. Add it to the cart or WhatsApp us and we check.")]
OWN_FAQ = [("I do not know the part name. What now?", "Send a photo of the damage and your car model on WhatsApp."),
           ("Can I buy online?", "Add parts to the cart and send the order on WhatsApp. We confirm fitment and reply.")]
def audience_pages():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Parts for Singapore workshops</h1><p class="lead">Search by car and part, add to cart, send the list on WhatsApp.</p></div></section>
<section class="sec tight"><div class="wrap narrow prose">
<ul class="ticks"><li>Search by brand, model and part.</li><li>Add several parts to one cart.</li><li>Send the order on WhatsApp. We confirm fitment.</li></ul>
<div class="btns">{btn("{{R}}catalogue/", "Search the catalogue")}{wa_btn("parts for our workshop", "WhatsApp us", "g")}</div></div></section>
<section class="sec alt tight"><div class="wrap narrow"><div class="sec-t"><h2>FAQ</h2></div>{faq_html(WS_FAQ)}</div></section>'''
    shell("for-workshops/index.html", "Parts for Workshops | EV Body Parts Singapore",
          "China and EV car body parts for Singapore workshops. Search by car and part, add to cart and order on WhatsApp.",
          body, "ws", [("For workshops", "for-workshops/")], faq=WS_FAQ, pri=0.8)
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Parts for your China or EV car</h1><p class="lead">Tell us the car and what is damaged.</p></div></section>
<section class="sec tight"><div class="wrap narrow prose">
<ul class="ticks"><li>Your car brand and model.</li><li>The part, or a photo of the damage.</li><li>Left or right, as seen from the driver's seat.</li></ul>
<div class="btns">{btn("{{R}}catalogue/", "Search the catalogue")}{wa_btn("a part for my car", "WhatsApp us", "g")}</div></div></section>
<section class="sec alt tight"><div class="wrap narrow"><div class="sec-t"><h2>FAQ</h2></div>{faq_html(OWN_FAQ)}</div></section>'''
    shell("for-car-owners/index.html", "Parts for Car Owners | EV Body Parts Singapore",
          "Find body parts for your China or EV car in Singapore. Add to cart and send your order on WhatsApp.",
          body, "own", [("For car owners", "for-car-owners/")], faq=OWN_FAQ, pri=0.8)

def about():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>About EV Body Parts</h1><p class="lead">A Singapore seller of body parts for China and EV cars, for workshops and car owners.</p></div></section>
<section class="sec tight"><div class="wrap narrow prose">
<dl class="facts"><div><dt>Name</dt><dd>{BRAND}</dd></div><div><dt>Website</dt><dd>{DOMAIN}</dd></div><div><dt>Sells</dt><dd>Body parts for China and EV cars</dd></div><div><dt>Serves</dt><dd>Workshops and car owners in Singapore</dd></div><div><dt>Brands</dt><dd>{brand_names()}</dd></div>
<div><dt>Order</dt><dd>Cart, then WhatsApp</dd></div></dl>
<p class="mu">Car photos are {CRED.lower().replace("stock photos: ", "stock photos from ")}: mood images, not {BRAND} stock.</p>
<div class="btns">{wa_btn("a part")}</div></div></section>'''
    shell("about/index.html", "About EV Body Parts | China & EV Car Parts Singapore",
          "EV Body Parts sells body parts for China and EV cars in Singapore, for workshops and car owners. Search by car and part.",
          body, "about", [("About", "about/")], pri=0.6)

def contact():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Contact</h1><p class="lead">WhatsApp is the fastest way.</p></div></section>
<section class="sec tight"><div class="wrap narrow prose">
<dl class="facts"><div><dt>WhatsApp</dt><dd><a href="https://wa.me/{WA}">{WA_DISPLAY}</a></dd></div></dl>
<div class="btns">{wa_btn("a part", "Message us on WhatsApp")}{btn("{{R}}catalogue/", "Search the catalogue", "g")}</div></div></section>'''
    shell("contact/index.html", "Contact | EV Body Parts Singapore",
          "Contact EV Body Parts, Singapore, on WhatsApp. Send your car and part and we confirm fitment.",
          body, "contact", [("Contact", "contact/")], pri=0.6)

def privacy():
    body = f'''<section class="ph-hd"><div class="wrap">{{{{CRUMBS}}}}<h1>Privacy notice (PDPA)</h1><p class="lead">How {BRAND} handles personal data.</p></div></section>
<section class="sec tight"><div class="wrap narrow prose">
<h2>What we collect</h2><p>When you send an order or message on WhatsApp we receive your WhatsApp number and what you write, such as your name, car and parts.</p>
<h2>Why we use it</h2><p>To reply, confirm fitment and availability. We do not sell personal data.</p>
<h2>Your cart</h2><p>Your cart is saved in your own browser only. It is not sent to us until you tap Send order on WhatsApp.</p>
<h2>Your rights</h2><p>Under Singapore's PDPA you can ask to see, correct or delete your data. Message us on <a href="https://wa.me/{WA}">WhatsApp {WA_DISPLAY}</a>.</p>
<h2>Analytics</h2><p>We count taps on WhatsApp buttons. No other tracking.</p>
</div></section>'''
    shell("privacy/index.html", "Privacy Notice | EV Body Parts Singapore",
          "How EV Body Parts handles personal data from WhatsApp orders and messages, under Singapore's PDPA.",
          body, "", [("Privacy", "privacy/")], pri=0.3)

if __name__ == "__main__":
    if OUT.exists(): shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    datajs()
    home(); catalogue(); parts_hub(); part_pages(); brands_hub(); brand_pages(); car_pages(); product_pages(); audience_pages(); about(); contact(); privacy(); articles()
    notfound(); statics()
    print(f"pages in sitemap {len(pages)}, brands {len(BRANDS)}, cars {len(CARS)}, products {len(PRODS)}, files {sum(1 for _ in OUT.rglob('*') if _.is_file())}")
