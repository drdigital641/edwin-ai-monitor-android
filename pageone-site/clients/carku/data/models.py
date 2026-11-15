"""Carku passenger-car sodium-ion models (12V CBN series).

Source: carkubattery.com product tables as read by Edwin, 15 Nov 2026, plus his
answers the same night. Never add a figure that is not here. TBC = to be confirmed.
Peak current is Carku's published PEAK figure, never CCA.
"""
U = "https://www.carkubattery.com/wp-content/uploads/"
CARKU = "https://www.carkubattery.com"

TBC = None  # rendered as "To be confirmed"

MODELS = [
    dict(slug="cbn30-d23", code="CBN30-D23", size="D23", size_long="JIS D23 size",
         din="", ah=30, volt="12V", peak=1000, wh=360,
         dims="240 × 170 × 187.5 mm", dims_tbc=True, kg="4.5 kg",
         img=["carku-cbn-d23-front.webp", "carku-cbn-d23-angle.webp", "carku-cbn-d23-angle-right.webp", "carku-cbn-d23-top.webp"],
         src=CARKU + "/product/car-sodium-starting-battery-cbn1230/",
         line="The JIS-size model of the range, for cars that take a D23 battery.",
         official=["Reliable cold-start battery: ensures instant engine ignition even in extreme low temperatures.",
                   "Long-life, 3000+ cycle battery, durable and maintenance-free.",
                   "Remote battery monitoring and Bluetooth."]),
    dict(slug="cbn30-h5", code="CBN30-L2/H5", size="H5", size_long="DIN H5 (L2) size",
         din="L2", ah=30, volt="12.2V", peak=1000, wh=366,
         dims="244 × 175 × 189 mm", dims_tbc=False, kg="6 kg",
         img=["carku-cbn-h5-front.webp", "carku-cbn-h5-angle.webp", "carku-cbn-h5-angle-high.webp", "carku-cbn-h5-back.webp"],
         src=CARKU + "/product/cbn1230-h5/",
         line="30Ah and 1000A peak in the DIN H5 (L2) case.",
         official=["Reliable cold and hot starts, from −40 °C to 80 °C.",
                   "High instant cranking current for passenger cars.",
                   "Smart remote monitoring: state of charge, voltage, current and temperature, with alerts."]),
    dict(slug="cbn30-h6", code="CBN30-L3/H6", size="H6", size_long="DIN H6 (L3) size",
         din="L3", ah=30, volt="12.2V", peak=1000, wh=366,
         dims="280 × 176 × 185 mm", dims_tbc=False, kg="6.1 kg",
         img=["carku-cbn-h6-front.webp", "carku-cbn-h6-scene.webp", "carku-cbn-h6-certificates.webp"],
         src=CARKU + "/product/cbn1230-h6/",
         line="Carku's AGM replacement in the standard H6 size, plug-and-play like a normal battery swap.",
         official=["Designed in standard H6 size, it fits as a direct replacement for your original AGM battery.",
                   "Simple plug-and-play design, just like replacing a standard battery.",
                   "With the Carku app, monitor battery health in real time."]),
    dict(slug="cbn30-l3h", code="CBN30-L3H", size="H6", size_long="DIN H6 (L3) case",
         din="L3", ah=30, volt="12V", peak=1000, wh=TBC,
         dims="280 × 176 × 185 mm (same case as the CBN30-L3/H6)", dims_tbc=False, kg=TBC,
         img=["carku-cbn-l3h-front.webp", "carku-cbn-l3h-scene.webp", "carku-cbn-l3h-certificates.webp"],
         src=CARKU + "/product/cbn1230e-h6/",
         line="A second 30Ah model in the H6 case. Kohden can tell you how it differs from the CBN30-L3/H6 for your car.",
         official=["Over 3000 cycles, maintenance-free, for cars with or without start-stop.",
                   "Delivers strong peak current, up to 1000A.",
                   "Bluetooth-enabled remote diagnostics to check battery health any time."]),
    dict(slug="cbn40-h7", code="CBN40-L4/H7", size="H7", size_long="DIN H7 (L4) size",
         din="L4", ah=40, volt="12.2V", peak=1200, wh=488,
         dims=TBC, dims_tbc=False, kg=TBC,
         img=["carku-cbn-h7-front.webp", "carku-cbn-h7-angle.webp", "carku-cbn-h7-angle-right.webp", "carku-cbn-h7-back.webp"],
         src=CARKU + "/product/cbn1240-h7/",
         line="40Ah and 1200A peak in the DIN H7 (L4) case.",
         official=["Reliable cold and hot starts, from −40 °C to 80 °C.",
                   "Strong peak current, up to 1200A.",
                   "Smart remote monitoring with wireless alerts."]),
    dict(slug="cbn40-h8", code="CBN40-L5/H8", size="H8", size_long="DIN H8 (L5) size",
         din="L5", ah=40, volt="12.2V", peak=1200, wh=488,
         dims="354 × 176 × 187 mm", dims_tbc=False, kg="7.6 kg",
         img=["carku-cbn-h8-front.webp", "carku-cbn-h8-angle.webp", "carku-cbn-h8-angle-right.webp", "carku-cbn-h8-back.webp"],
         src=CARKU + "/product/cbn1240-h8/",
         line="40Ah and 1200A peak in the longer DIN H8 (L5) case.",
         official=["Reliable cold and hot starts, from −40 °C to 80 °C.",
                   "Strong peak current, up to 1200A.",
                   "Smart remote monitoring with wireless alerts."]),
    dict(slug="cbn50-h9", code="CBN50-L6/H9", size="H9", size_long="DIN H9 (L6) size",
         din="L6", ah=50, volt="12.2V", peak=1500, wh=610,
         dims="398 × 176 × 188 mm", dims_tbc=True, kg="9 kg",
         img=["carku-cbn-h9-front.webp", "carku-cbn-h9-angle.webp", "carku-cbn-h9-angle-right.webp", "carku-cbn-h9-back.webp"],
         src=CARKU + "/product/cbn1250-h9/",
         line="The biggest passenger model: 50Ah and 1500A peak in the DIN H9 (L6) case.",
         official=["Reliable cold and hot starts, from −40 °C to 80 °C.",
                   "Strong peak current, up to 1500A.",
                   "Smart remote monitoring with wireless alerts."]),
]

MEDIA = dict(  # local files in assets/img/carku/ (Website Manager drop, 15 Nov 2026; manifest has sources)
    logo="carku-logo-english-slogan-blue.webp",
    icon="carku-app-icon.webp",
    hero_graphic="carku-hero-next-gen-lead-acid-replacement.webp",
    lineup="carku-sodium-ion-starting-battery-lineup.webp",
    features="carku-sodium-ion-features-scene.webp",
    sustain="carku-sodium-ion-sustainability.webp",
    workshop="carku-workshop-h6-in-hand.webp",
    factory="carku-factory-exterior.webp",
    appguide="carku-app-installation-guide.webp",
    shot_params="carku-app-screenshot-parameters.webp",
    shot_activate="carku-app-screenshot-activate-device.webp",
)
DIMS = {"logo": (300, 100), "icon": (512, 512), "hero_graphic": (1600, 776), "lineup": (1600, 776), "features": (1600, 776),
        "sustain": (1600, 676), "workshop": (768, 389), "factory": (1600, 1067), "appguide": (1600, 776),
        "shot_params": (800, 1422), "shot_activate": (800, 1422), "product": (1600, 1310)}

APP_IOS = "https://apps.apple.com/sg/app/carku-battery/id6464281693"
APP_ANDROID = "https://play.google.com/store/apps/details?id=com.mini.carkubattery&hl=en_SG"
