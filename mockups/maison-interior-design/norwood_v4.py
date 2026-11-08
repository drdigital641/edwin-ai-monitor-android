# Norwood Grand V4 (8 Nov 2026): same template as Towner V4 (towner_v4.py), four themes, CDL brochure plans p.16-21.
# exec'd by launches.py after towner_v4.py.

NG_BROCHURE = "https://www.cdlhomes.com.sg/norwoodgrand/brochure.pdf"
NG_RELEASE = "https://www.cdl.com.sg/assets/en-newsroom-press-release-pdf/CDL-News-Release-Norwood-Grand-launch-weekend-web.pdf"
NG_CON = "https://www.cdlhomes.com.sg/construction/"

def _ng_msg(x):
    return f"Hi Maison, I’m interested in the {x} concept for my Norwood Grand unit. Can we discuss my layout?"

NG_THEMES = [
    dict(key="tropical-resort-modern", img="norwood-grand-v4-living-tropical-resort-modern", theme="Tropical Resort Modern", room="Living room",
         h3="Norwood Grand living room interior design — Tropical Resort Modern",
         cap="A fluted teak feature wall, a floating teak-and-travertine console and built-in display niches give the living room a warm, resort-like calm. An easy starting point for your Norwood Grand renovation.",
         alt="Tropical Resort Modern living room concept with fluted teak built-in wall and balcony greenery",
         btn="Discuss Tropical Resort Modern on WhatsApp", msg=_ng_msg("Tropical Resort Modern living room")),
    dict(key="smoked-walnut-noir", img="norwood-grand-v4-kitchen-smoked-walnut-noir", theme="Smoked Walnut Noir", room="Kitchen (close-up)",
         h3="Woodlands condo kitchen design idea — Smoked Walnut Noir",
         cap="Handleless smoked-walnut carpentry, a black sintered-stone counter and fluted-glass wall cabinets give the kitchen a dark, tailored finish. Adapt the finishes and storage to your actual unit.",
         alt="Close-up of Smoked Walnut Noir kitchen concept with walnut cabinets and black stone counter",
         btn="Discuss Smoked Walnut Noir on WhatsApp", msg=_ng_msg("Smoked Walnut Noir kitchen")),
    dict(key="quiet-luxury-greige", img="norwood-grand-v4-main-bedroom-quiet-luxury-greige", theme="Quiet Luxury Greige", room="Main bedroom",
         h3="Norwood Grand main bedroom design — Quiet Luxury Greige",
         cap="A wall-to-wall upholstered headboard panel, a full-height bronze-glass wardrobe and a built-in vanity keep the main bedroom soft, quiet and uncluttered.",
         alt="Quiet Luxury Greige main bedroom concept with built-in headboard wall and glass wardrobe",
         btn="Discuss Quiet Luxury Greige on WhatsApp", msg=_ng_msg("Quiet Luxury Greige main bedroom")),
    dict(key="terrazzo-mid-century", img="norwood-grand-v4-common-bedroom-terrazzo-mid-century", theme="Terrazzo Mid-Century", room="Common bedroom",
         h3="Norwood Grand common bedroom renovation idea — Terrazzo Mid-Century",
         cap="A one-piece built-in platform bed, a window desk with a terrazzo top and rounded olive overhead cabinets make a compact common bedroom work for both rest and study.",
         alt="Terrazzo Mid-Century common bedroom concept with built-in bed, desk and curved cabinets",
         btn="Discuss Terrazzo Mid-Century on WhatsApp", msg=_ng_msg("Terrazzo Mid-Century common bedroom")),
]

_NG_P = [(16, 914, "1-Bedroom + Study (A1S), 2-Bedroom (B1)"),
         (17, 1333, "2-Bedroom + Ensuite Study (B1S), 2-Bedroom + Study (B2S)"),
         (18, 1333, "3-Bedroom Deluxe (C1, C2)"),
         (19, 1333, "3-Bedroom + Study (C3S), 3-Bedroom Premium + Study (C4PS)"),
         (20, 1333, "3-Bedroom Premium + Study (C5PS), 4-Bedroom Deluxe + Study (D1S)"),
         (21, 1333, "4-Bedroom Premium + Study (D2PS, D3PS)")]
NG_PLANS = [dict(img=f"norwood-grand-cdl-brochure-plans-p{n}", w=2000, h=hh, title=f"page {n}",
                 alt=f"Norwood Grand CDL brochure page {n} floor plans: {t}",
                 cap=f"Brochure p.{n}: {t}. (P) variants shown on the same page.") for n, hh, t in _NG_P]

V4CFG["norwood-grand"] = dict(
    dir="norwood-grand-v4", ref="norwood-v4", themes=NG_THEMES, plans=NG_PLANS,
    hero=dict(eyebrow="Four Maison-inspired concepts · Norwood Grand",
              intro="Explore four interior design themes for your Norwood Grand home, then WhatsApp Maison to discuss your own layout.",
              btn="WhatsApp Maison about this look",
              msg="Hi Maison, I’m planning my Norwood Grand renovation. I like the Tropical Resort Modern living room concept. Can we discuss my layout?"),
    themes_h2="Four Norwood Grand interior design themes",
    themes_sub="Four rooms, four looks, each built around bespoke carpentry. We adapt every idea to your actual unit.",
    plans_h2="Norwood Grand floor plans",
    plans_sub="Original CDL brochure pages 16 to 21, copied as-is (scaled only, not redrawn). Plans are subject to change and final survey; owners confirm their actual unit.",
    plan_label="Floor plan: Norwood Grand brochure, CDL", plans_cls="v4-plans v4-wide",
    plans_src=f'Source: <a href="{NG_BROCHURE}" target="_blank" rel="noopener">Norwood Grand brochure, CDL (PDF)</a>.',
    citation=[NG_BROCHURE, NG_RELEASE, NG_CON],
    facts=("Norwood Grand project facts", [
        ("348 units in four 11-storey blocks at 2, 6, 8 and 10 Champions Way, Woodlands. Developer: CDL Stellar Pte. Ltd., a CDL subsidiary.", "CDL news release", NG_RELEASE),
        ("99-year lease from 18 December 2023. TOP obtained August 2026 (CDL construction update, 2 November 2026).", "CDL construction page", NG_CON),
        ("Unit sizes from about 495 to 1,335 sq ft, depending on type.", "CDL brochure", NG_BROCHURE)],
        "Maison is an independent interior design firm, not affiliated with CDL. Key and access appointments are set per owner and are not confirmed here."),
    css=".v4-facts{margin:16px 0 0;padding:0 0 0 20px;max-width:72ch;font-size:16px;line-height:1.6;color:var(--ink2)}.v4-facts li{margin:0 0 10px}.v4-facts a{color:var(--brass);text-decoration:underline;white-space:nowrap}"
        "@media(min-width:900px){.v4-plans.v4-wide{grid-template-columns:1fr;max-width:1100px}}"
        "@media(max-width:899px){.v4-fig figcaption,.v4-plan figcaption{padding-right:68px}}",
    end_msg="Hi Maison, I’m planning my Norwood Grand renovation. Can we discuss my layout?")
