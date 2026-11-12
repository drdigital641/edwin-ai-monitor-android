# New launches hub, project pages and service guides (exec'd by build.py after its helpers).
# Project pages are data: data/new-launches/<slug>.json, rendered by newlaunch.py (format: docs/new-launch-data-format.md).
exec(open(os.path.join(HERE, "launches_guides.py"), encoding="utf-8").read())
VPAGE_ON_HOLD = {"parc-point-tengah": "parc-point"}   # old slug -> real page (noindex stub). lumina-grand is a real page again from 11 Nov
LAUNCHES, LAUNCH_URLS, NL_LASTMOD = [], [], {}   # filled by launches_build() from the JSON data

KINDS = {"bto": ("BTO / HDB", "bto-renovation"), "ec": ("Executive condo", "new-condo-renovation"),
         "condo": ("Private condo", "new-condo-renovation"), "landed": ("Landed", "landed-renovation"),
         "office": ("Office", "office-fit-out"), "retail": ("Retail", "retail-shop-fit-out")}
GBY = {g["slug"]: g for g in GUIDES}
PUB = "2026-11-07"
MAISON_INDEP = "Maison Interior Design is an independent interior design firm. We are not appointed by, or affiliated with, the developer, HDB or the building's owner."

# Short type-level checks; the full version lives on the matching guide page.
DEFECTS = {
 "bto": ["Report defects within 30 days of key collection, before renovation starts (HDB move-in guide). The Defects Liability Period runs 1 year from key collection.",
         "Check floor and wall tiles for hollow or chipped pieces, plaster for cracks, and paint for stains.",
         "Test every door, window, lock, tap, floor trap, light point and power socket.",
         "Report through the QR code in your Welcome Kit or your project's Building Service Centre, with photos."],
 "condo": ["Your sale and purchase agreement sets the defects liability period, commonly 12 months from vacant possession. Check yours.",
           "Inspect before your contractor starts, so new marks are not blamed on the renovation.",
           "Check floors, walls, doors, windows, balcony glass, sealant, appliances, taps, water heater and air-conditioning.",
           "Submit a list with photos through the developer's defects process and keep a copy."],
 "landed": ["Your sale and purchase agreement sets the defects liability period. Check it before work starts.",
            "Walk every floor, the roof and outdoor areas. Look for water stains, cracks, hollow tiles and blocked drains.",
            "Test the gate, doors, windows, sanitary fittings, water heaters and every electrical point.",
            "Submit defects with photos to the developer and keep a copy."],
 "office": ["Ask the landlord for the handover condition in writing and walk the space against it.",
            "Check ceilings, raised floors, air-conditioning outlets, sprinkler heads, power and data provisions.",
            "Photograph existing marks and defects before your contractor starts.",
            "Agree how and when landlord defects will be fixed so they do not hold up the fit-out."],
 "retail": ["Ask the landlord for the handover condition in writing and walk the unit against it.",
            "Check the shopfront, floor, ceiling, power supply, water and drainage points, and any exhaust provision.",
            "Photograph existing marks and defects before work starts.",
            "Agree how landlord defects will be fixed so they do not delay opening."]}
DEFECTS["ec"] = DEFECTS["condo"]
RULES = {
 "bto": ["Use a contractor listed in HDB's Directory of Renovation Contractors; they can apply for the permit for you.",
         "A permit is needed for works such as removing floor finishes, raising floor levels in wet areas, or hacking or altering walls.",
         "For the first 3 years, toilet wall and floor finishes in a new BTO flat cannot be removed. New tiles can be overlaid.",
         "General works: Monday to Saturday, 9am to 6pm. Noisy works: Monday to Friday, 9am to 5pm. No works on Sundays or public holidays.",
         "Household shelter walls must not be hacked or drilled. Windows need a BCA-approved window contractor; air-conditioners need a BCA-trained installer."],
 "condo": ["Renovation approval comes from the condo's management (the managing agent, then the MCST). Expect a form, a deposit and contractor registration.",
           "Working hours are set by the condo's by-laws and are usually shorter than HDB's. Check them before booking work.",
           "Changes seen from outside, such as balcony screens, grilles and the main door, need approval and must follow the approved design.",
           "Structural changes need a professional engineer and building approvals."],
 "landed": ["Interior work usually needs no planning approval, but structural changes and extra floor area usually need plans by a qualified person (URA and BCA).",
            "In a landed development with shared facilities, the management controls changes to the facade, gates and roof.",
            "Protect shared walls, drains and neighbours' property, and agree access before work starts."],
 "office": ["The building's fit-out guidelines: approved contractors, insurance, deposits, hours and drawing submissions.",
            "Changes to sprinklers, fire alarms or escape routes usually need a qualified person and SCDF approval.",
            "Structural changes need BCA approval. If your use differs from the approved use, check URA's change-of-use rules."],
 "retail": ["The landlord's fit-out guidelines: contractors, hours, deposits, signage and drawing submissions.",
            "Food businesses need the right SFA licence; plan the kitchen with it in mind.",
            "Fire safety changes need a qualified person and SCDF approval; structural changes need BCA approval."]}
RULES["ec"] = RULES["condo"] + ["Executive condominiums follow the condo's rules, not HDB's renovation permits."]
SRC_RULES = {"bto": [("HDB renovation guide", HDB_RENO), ("HDB move-in guide", HDB_MOVE)], "ec": [], "condo": [], "landed": [("URA", URA), ("BCA", BCA)],
             "office": [("SCDF", SCDF), ("BCA", BCA), ("URA", URA)], "retail": [("SFA", SFA), ("SCDF", SCDF)]}
TL = {"bto": GBY["bto-renovation"]["timeline"], "ec": GBY["new-condo-renovation"]["timeline"], "condo": GBY["new-condo-renovation"]["timeline"],
      "landed": GBY["landed-renovation"]["timeline"], "office": GBY["office-fit-out"]["timeline"], "retail": GBY["retail-shop-fit-out"]["timeline"]}

def ul(items, cls="ticks"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(x)}</li>" for x in items) + "</ul>"

def tl_html(steps, note):
    rows = "".join(f'<li><span class="sn">0{i+1}</span><div><h3>{e(t)} <small>{e(d)}</small></h3><p>{e(x)}</p></div></li>' for i, (t, d, x) in enumerate(steps))
    return f'<ol class="tl">{rows}</ol><p class="tl-note">{e(note)}</p>'

def faq_block(faq, title="Questions owners ask"):
    rows = "".join(f'<details class="qa"><summary><h3>{e(q)}</h3><span class="pm" aria-hidden="true"></span></summary><p>{e(a)}</p></details>' for q, a in faq)
    return f'<section class="sec faq"><div class="wrap narrow"><p class="eyebrow">Good to know</p><h2 class="display">{title}</h2>{rows}</div></section>'

def faq_ld(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}

def src_line(sources):
    return '<p class="nl-src"><b>Sources:</b> ' + " · ".join(f'<a href="{u}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in sources) + "</p>"

def wa_cta(q, msg, ref):
    return f"""<section class="cta dark"><div class="wrap cta-in">
<p class="eyebrow">Talk to Maison</p><h2 class="display">{e(q)}<br><em>WhatsApp Maison</em></h2>
<p class="cta-p">Send your floor plan and your key or handover date. Roland and the team will reply with first ideas, a realistic timeline and an itemised quote.</p>
<div class="btns"><a class="btn light" href="{wa(msg)}" data-cta="whatsapp" data-ref="{ref}">WhatsApp {PHONE}</a><a class="btn ghost-l" href="{BASE}new-launches/">All new launches</a></div>
</div></section>"""

def guide_page(g):
    path = f"services/{g['slug']}/"
    rel = sorted([p for p in LAUNCHES if _nl_guide(p) in g["kind"] or (g["slug"] == "new-condo-renovation" and _nl_guide(p) in ("condo", "ec"))], key=lambda p: p["name"].lower())
    secs = "".join(f'<section class="nl-sec"><h2 class="display">{e(h)}</h2>{ul(items)}</section>' for h, items in g["secs"])
    rel_html = ("<section class=\"nl-sec\"><h2 class=\"display\">New launches with guides</h2><ul class=\"nl-links\">" +
                "".join(f'<li><a href="{BASE}new-launches/{p["slug"]}/">{e(p["name"])} <span>{e(p["area"])}</span></a></li>' for p in rel) + "</ul></section>") if rel else ""
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("Services", "services/"), (g["short"], path)]),
              {"@type": "Service", "name": g["short"], "provider": {"@id": DOMAIN + "/#business"}, "areaServed": {"@type": "Country", "name": "Singapore"}, "description": g["desc"]},
              faq_ld(g["faq"])]}
    s = head(g["title"], g["desc"], path, "62-Havelock-Road-Living-1-small-1024x683.jpg", schema)
    s += header("services/")
    s += f"""<section class="phead"><div class="wrap narrow"><p class="eyebrow"><a href="{BASE}services/">Services</a> · {e(g['short'])}</p>
<h1 class="display">{e(g['h1'][0])} <em>{e(g['h1'][1])}</em></h1><p class="ph-p">{e(g['intro'])}</p>
<div class="btns"><a class="btn dark-b" href="{wa(g['cta'])}" data-cta="whatsapp" data-ref="{g['slug']}">WhatsApp Maison</a><a class="btn ghost-d" href="{BASE}new-launches/">See new launches</a></div></div></section>
<section class="sec tight nl-s"><div class="wrap narrow nl-body">{secs}
<section class="nl-sec"><h2 class="display">A realistic timeline</h2>{tl_html(g['timeline'], g['timeline_note'])}</section>
{rel_html}{src_line(g['sources'])}</div></section>
{faq_block(g['faq'])}{wa_cta("Ready to plan?", g['cta'], g['slug'])}"""
    s += footer()
    write(path + "index.html", s)

exec(open(os.path.join(HERE, "newlaunch.py"), encoding="utf-8").read())

def launches_build(dirs=None):
    global LAUNCHES, LAUNCH_URLS
    LAUNCHES = nl_load(dirs)
    NL_LASTMOD.update({f"new-launches/{p['slug']}/": p.get("date_modified") or p.get("date_published") or "2026-11-11" for p in LAUNCHES})
    NL_LASTMOD["new-launches/"] = max(NL_LASTMOD.values(), default="2026-11-11")
    LAUNCH_URLS = ["new-launches/"] + [f"new-launches/{p['slug']}/" for p in LAUNCHES] + [f"services/{g['slug']}/" for g in GUIDES]
    for sl, to in VPAGE_ON_HOLD.items():  # old URLs kept as noindex redirect stubs
        u = f"{BASE}new-launches/{to}/" if to else f"{BASE}new-launches/"
        write(f"new-launches/{sl}/index.html", f'<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={u}"><link rel="canonical" href="{DOMAIN}{u}"><title>New launches | Maison Interior Design</title></head><body><a href="{u}">New launches</a></body></html>')
    for g in GUIDES: guide_page(g)
    for p in LAUNCHES: nl_page(p, LAUNCHES)
    nl_hub(LAUNCHES)
