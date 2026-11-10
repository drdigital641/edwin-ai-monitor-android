# CanningHill Piers V4 (10 Nov 2026): same template as the other V4 pages (towner_v4.py), four themes, e-brochure B1(S) crop + p.31.
# exec'd by launches.py after myst_v4.py.

CP_BROCHURE = "https://canninghillpiers.com.sg/floorplans/CanningHill-Piers-e-brochure.pdf"
CP_KEYPLAN = "https://canninghillpiers.com.sg/floorplans/storey-key-plans.pdf"
CP_RELEASE = "https://www.cdl.com.sg/newsroom/capitaland-and-cdl-to-launch-canninghill-piers-tallest-residential-development-along-the-singapore-river-sales-previews-commence-from-friday-5-november-2021"
CP_CON = "https://www.cdlhomes.com.sg/construction/"

def _cp_msg(x):
    return f"Hi Maison, I’m interested in the {x} concept for my CanningHill Piers unit. Can we discuss my layout?"

CP_THEMES = [
    dict(key="riverside-teak-modernist", img="canninghill-piers-v4-living-riverside-teak-modernist", theme="Riverside Teak Modernist", room="Living room",
         h3="CanningHill Piers living room interior design — Riverside Teak Modernist",
         cap="A vertical teak slat TV wall with a floating granite console, a built-in L-shaped window bench, a fluted teak dining banquette and cove lighting. Styled on the B1(S) living and dining, which run in one line from the kitchen to the living balcony.",
         alt="Riverside Teak Modernist living room concept at CanningHill Piers with teak slat feature wall and built-in window bench",
         btn="Discuss Riverside Teak Modernist on WhatsApp", msg=_cp_msg("Riverside Teak Modernist living room")),
    dict(key="ivory-travertine-minimal", img="canninghill-piers-v4-kitchen-ivory-travertine-minimal", theme="Ivory Travertine Minimal", room="Kitchen (close-up)",
         h3="River Valley condo kitchen design idea — Ivory Travertine Minimal",
         cap="Handleless ivory cabinets, a travertine-look sintered-stone counter with a waterfall end and full-height backsplash, and an oak appliance tower. Styled on the B1(S) galley kitchen beside the entrance, open to dining; the developer names Ernestomeda kitchen systems with Miele and De Dietrich appliances (models not shown).",
         alt="Close-up of Ivory Travertine Minimal kitchen concept with sintered-stone waterfall counter",
         btn="Discuss Ivory Travertine Minimal on WhatsApp", msg=_cp_msg("Ivory Travertine Minimal kitchen")),
    dict(key="oxblood-walnut-nocturne", img="canninghill-piers-v4-main-bedroom-oxblood-walnut-nocturne", theme="Oxblood Walnut Nocturne", room="Main bedroom",
         h3="CanningHill Piers main bedroom design — Oxblood Walnut Nocturne",
         cap="An oxblood upholstered headboard wall framed in walnut, a built-in platform bed with bedside shelves and a full-height lit walnut wardrobe. Styled on the B1(S) master bedroom, which has its own balcony and ensuite.",
         alt="Oxblood Walnut Nocturne main bedroom concept with upholstered headboard wall and walnut wardrobe",
         btn="Discuss Oxblood Walnut Nocturne on WhatsApp", msg=_cp_msg("Oxblood Walnut Nocturne main bedroom")),
    dict(key="sage-linen-contemporary", img="canninghill-piers-v4-common-bedroom-sage-linen-contemporary", theme="Sage Linen Contemporary", room="Common bedroom (close-up)",
         h3="CanningHill Piers common bedroom renovation idea — Sage Linen Contemporary",
         cap="A sage lacquer desk-and-shelf run under the window flows into a fluted ash wardrobe, with a linen headboard panel. Styled on B1(S) Bedroom 2, so a compact room works for both study and rest.",
         alt="Sage Linen Contemporary common bedroom concept with built-in study desk and fluted wardrobe",
         btn="Discuss Sage Linen Contemporary on WhatsApp", msg=_cp_msg("Sage Linen Contemporary common bedroom")),
]

CP_PLANS = [
    dict(img="canninghill-piers-brochure-type-b1s", w=1600, h=1760, title="Type B1(S)",
         alt="CanningHill Piers e-brochure floor plan of Type B1(S), 2-bedroom + ensuite study, 77 sq m / 829 sq ft",
         cap="Type B1(S): 2-Bedroom + Ensuite Study, 77 sq m / 829 sq ft, Blk 1 #04-07 to #23-07. Living/dining to the balcony, Bedroom 2, master with its own balcony and bath, ensuite study, Bath 2, and the kitchen by the entry."),
    dict(img="canninghill-piers-brochure-plans-p31", w=2000, h=1401, title="brochure page 31",
         alt="CanningHill Piers e-brochure page 31: Type B1(S) 2-bedroom + ensuite study and Type BS1 2-bedroom + study floor plans",
         cap="Full brochure page 31: Type B1(S), and Type BS1 2-Bedroom + Study, 68 sq m / 732 sq ft, Blk 1 #40-02 to #44-02."),
]

V4CFG["canninghill-piers"] = dict(
    dir="canninghill-piers-v4", ref="canninghill-v4", w=1920, themes=CP_THEMES, plans=CP_PLANS,
    hero=dict(eyebrow="Four Maison-inspired concepts · CanningHill Piers",
              intro="Explore four interior design themes for your CanningHill Piers home, then WhatsApp Maison to discuss your own layout.",
              intro_html='Explore four interior design themes for your CanningHill Piers home, then <a href="https://wa.me/6593391185" data-cta="whatsapp" data-ref="canninghill-v4-intro" rel="noopener" style="color:inherit;text-decoration:underline">WhatsApp Maison</a> to discuss your own layout.',
              btn="WhatsApp Maison about this look",
              msg="Hi Maison, I’m planning my CanningHill Piers renovation. I like the Riverside Teak Modernist living room concept. Can we discuss my layout?"),
    themes_h2="Four CanningHill Piers interior design themes",
    themes_sub="Four rooms, four looks, each built around bespoke carpentry. We adapt every idea to your actual unit.",
    themes_note="All four are styled on Type B1(S) 2-bedroom + ensuite study, 77 sq m / 829 sq ft (official e-brochure p31).",
    plans_h2="CanningHill Piers floor plan",
    plans_sub="Official e-brochure plan copied as-is (crop and scale only, tap to enlarge).",
    plans_note="The brochure has plans for 1-bedroom to 5-bedroom premium types (PDF pp. 23-40); Sky Suites and the Super Penthouse are not shown in it. Brochure note: plans subject to change; areas include A/C ledge, balcony and void where applicable.",
    plan_label="Floor plan: CanningHill Piers e-brochure (source)", plans_cls="v4-plans v4-wide",
    plan_label_html=f'Floor plan: <a href="{CP_BROCHURE}" target="_blank" rel="nofollow noopener">CanningHill Piers e-brochure</a> (source)',
    hub=dict(img="canninghill-piers-v4-living-riverside-teak-modernist-900", w=900, h=506,
             alt="CanningHill Piers living room concept by Maison: teak slat TV wall, built-in window bench and river view"),
    plans_src=f'Source: <a href="{CP_BROCHURE}" target="_blank" rel="noopener">CanningHill Piers e-brochure (PDF)</a>.',
    citation=[CP_BROCHURE, CP_RELEASE, CP_CON],
    facts=("CanningHill Piers project facts", [
        ("696 apartments in 48- and 24-storey towers linked at Level 24; joint development by CapitaLand Development and City Developments Limited; direct link to Fort Canning MRT.", "CDL news release", CP_RELEASE),
        ("99-year lease from 17 September 2021. TOP obtained October 2026; expected vacant possession 30 June 2027.", "CDL construction page", CP_CON),
        ("Level 24 facilities include pools, a yoga deck, two gyms and a Flexi Lounge; Level 45 has lounges.", "CDL news release", CP_RELEASE)],
        "Maison is an independent interior design firm, not affiliated with the developers. Key dates are set per buyer by the developer."),
    glance_h2="Layouts and renovation ideas",
    glance_note="Ideas only; check walls, services and management rules before work. Sizes: official e-brochure.",
    extra=[("Views tips", "The developer describes a riverside 48-storey tower and a 24-storey tower facing Fort Canning Hill, linked at Level 24. No unit’s view is guaranteed: check your stack on the storey key plan, then plan blinds and glare control around your real outlook.")],
    steps_h2="Keys to move-in (planning guide)",
    end_note="WhatsApp Maison with your unit type, key date and wish list.",
    src_labels={CP_BROCHURE: "CanningHill Piers e-brochure (PDF)"},
    css=V4CFG["norwood-grand"]["css"] + "@media(min-width:900px){.v4-wide .v4-plan:first-child{max-width:720px}}.v4-plan figcaption b a{color:inherit;text-decoration:underline}",
    end_msg="Hi Maison, I’m planning my CanningHill Piers renovation. Can we discuss my layout?")
