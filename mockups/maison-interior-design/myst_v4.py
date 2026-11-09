# The Myst V4 (9 Nov 2026): same template as Towner and Norwood V4 (towner_v4.py), four themes, CDL simplified brochure plans p.8-10.
# exec'd by launches.py after norwood_v4.py.

MY_BROCHURE = "https://www.cdlhomes.com.sg/themyst/assets/pdf/The%20Myst%20Simplified%20Brochure_Final.pdf"
MY_RELEASE = "https://www.cdl.com.sg/assets/en-newsroom-press-release-pdf/CDL-News-Release-The-Myst-Preview-web.pdf"
MY_CON = "https://www.cdlhomes.com.sg/construction/"

def _my_msg(x):
    return f"Hi Maison, I’m interested in the {x} concept for my The Myst unit. Can we discuss my layout?"

MY_THEMES = [
    dict(key="misty-forest-modern", img="the-myst-v4-living-misty-forest-modern", theme="Misty Forest Modern", room="Living room",
         h3="The Myst living room interior design — Misty Forest Modern",
         cap="A fluted pale-oak feature wall, a floating moss-green stone TV console, a built-in window bench and soft cove lighting bring the green outlook indoors. A calm starting point for your The Myst renovation.",
         alt="Misty Forest Modern living room concept at The Myst with fluted oak built-in wall and balcony greenery",
         btn="Discuss Misty Forest Modern on WhatsApp", msg=_my_msg("Misty Forest Modern living room")),
    dict(key="champagne-marble-deco", img="the-myst-v4-kitchen-champagne-marble-deco", theme="Champagne Marble Deco", room="Kitchen (close-up)",
         h3="Upper Bukit Timah condo kitchen design idea — Champagne Marble Deco",
         cap="Handleless champagne lacquer cabinets with brass edges, a calacatta-look sintered-stone counter and backsplash, and fluted bronze-glass wall cabinets give the kitchen a light, polished finish. Adapt the finishes and storage to your actual unit.",
         alt="Close-up of Champagne Marble Deco kitchen concept with sintered-stone counter and brass-edged cabinets",
         btn="Discuss Champagne Marble Deco on WhatsApp", msg=_my_msg("Champagne Marble Deco kitchen")),
    dict(key="mocha-limewash-contemporary", img="the-myst-v4-main-bedroom-mocha-limewash-contemporary", theme="Mocha Limewash Contemporary", room="Main bedroom",
         h3="The Myst main bedroom design — Mocha Limewash Contemporary",
         cap="A full-width limewash headboard wall with backlit floating shelves, a built-in platform bed and a ribbed walnut full-height wardrobe keep the main bedroom warm, quiet and uncluttered.",
         alt="Mocha Limewash Contemporary main bedroom concept with built-in headboard wall and walnut wardrobe",
         btn="Discuss Mocha Limewash Contemporary on WhatsApp", msg=_my_msg("Mocha Limewash Contemporary main bedroom")),
    dict(key="navy-oak-heritage", img="the-myst-v4-common-bedroom-navy-oak-heritage", theme="Navy Oak Heritage", room="Common bedroom (close-up)",
         h3="The Myst common bedroom renovation idea — Navy Oak Heritage",
         cap="A navy lacquer study-and-wardrobe run, an oak desktop under the window and a built-in daybed corner turn a compact common bedroom into a study that still has room to rest.",
         alt="Navy Oak Heritage common bedroom concept with built-in study desk and full-height wardrobe",
         btn="Discuss Navy Oak Heritage on WhatsApp", msg=_my_msg("Navy Oak Heritage common bedroom")),
]

_MY_P = [(8, "1-Bedroom + Study A1Sa 48 sq m / 517 sq ft (A1Sa(d) 61 sq m / 657 sq ft); 2-Bedroom B1 63 sq m / 678 sq ft (B1(d) 78 sq m / 840 sq ft)"),
         (9, "2-Bedroom + Study B3S 65 sq m / 700 sq ft (B3S(d) 79 sq m / 850 sq ft); 3-Bedroom C1 79 sq m / 850 sq ft (C1(d) 95 sq m / 1,023 sq ft)"),
         (10, "4-Bedroom D2 141 sq m / 1,518 sq ft (D2(d) 172 sq m / 1,851 sq ft); 5-Bedroom E1 157 sq m / 1,690 sq ft (E1(d) 189 sq m / 2,034 sq ft)")]
MY_PLANS = [dict(img=f"the-myst-cdl-brochure-plans-p{n}", w=2000, h=1327, title=f"page {n}",
                 alt=f"The Myst CDL simplified brochure page {n} floor plans: {a}",
                 cap=f"Brochure p.{n}: {t}.") for (n, t), a in zip(_MY_P, ["1-Bedroom + Study A1Sa and 2-Bedroom B1",
                 "2-Bedroom + Study B3S and 3-Bedroom C1", "4-Bedroom D2 and 5-Bedroom E1"])]

V4CFG["the-myst"] = dict(
    dir="the-myst-v4", ref="myst-v4", w=1920, themes=MY_THEMES, plans=MY_PLANS,
    hero=dict(eyebrow="Four Maison-inspired concepts · The Myst",
              intro="Explore four interior design themes for your The Myst home, then WhatsApp Maison to discuss your own layout.",
              btn="WhatsApp Maison about this look",
              msg="Hi Maison, I’m planning my The Myst renovation. I like the Misty Forest Modern living room concept. Can we discuss my layout?"),
    themes_h2="Four The Myst interior design themes",
    themes_sub="Four rooms, four looks, each built around bespoke carpentry. We adapt every idea to your actual unit.",
    themes_note="All four are styled on Type B1 typical 2-bedroom, 63 sq m / 678 sq ft (CDL simplified brochure p8; standard ceiling, not the B1(d) 4.5m-void variant).",
    plans_h2="The Myst floor plans",
    plans_sub="Original CDL simplified-brochure pages 8 to 10, copied as-is (scaled only, not redrawn).",
    plans_note="(d) variants include a strata void above living/dining with 4.5m ceiling height; (p) = ground-floor PES variants. Other types in the block schematic (e.g. B1a, C2, C3Pa, C4PSa) have no plan in the public simplified brochure; ask CDL or your agent for those. Plans are subject to change and final survey; areas include A/C ledge, balcony and strata void where applicable.",
    plan_label="Floor plan: The Myst simplified brochure, CDL", plans_cls="v4-plans v4-wide",
    plans_src=f'Source: <a href="{MY_BROCHURE}" target="_blank" rel="noopener">The Myst simplified brochure, CDL (PDF)</a>.',
    citation=[MY_BROCHURE, MY_RELEASE, MY_CON],
    facts=("The Myst project facts", [
        ("408 units in two 24-storey towers at 800 and 802 Upper Bukit Timah Road. Developer: CDL Aries Pte. Ltd., wholly owned by CDL. Land area approx. 179,008 sq ft.", "CDL news release", MY_RELEASE),
        ("99-year lease from 11 May 2023. TOP obtained September 2026; expected vacant possession 31 March 2029.", "CDL construction page", MY_CON),
        ("CDL describes a 5-minute walk to Cashew MRT (Downtown Line) and 75% of the footprint as landscaping and communal facilities.", "CDL news release", MY_RELEASE)],
        "Maison is an independent interior design firm, not affiliated with CDL. Key dates are set per buyer by CDL."),
    glance_h2="Layouts and renovation ideas",
    glance_note="Ideas only; check walls, services and management rules before work.",
    extra=[("Views tips", "CDL describes “picturesque views of its lush surroundings”, but no unit’s view is guaranteed. Check your stack, floor and facing on the brochure key plan, then plan blinds, glare control and window benches around your actual outlook.")],
    steps_h2="Keys to move-in (planning guide)",
    end_note="WhatsApp Maison with your unit type, key date and wish list.",
    css=V4CFG["norwood-grand"]["css"],
    end_msg="Hi Maison, I’m planning my The Myst renovation. Can we discuss my layout?")
