# New launches hub, project pages and service guides (exec'd by build.py after its helpers).
exec(open(os.path.join(HERE, "launches_guides.py"), encoding="utf-8").read())
exec(open(os.path.join(HERE, "launches_projects.py"), encoding="utf-8").read())
exec(open(os.path.join(HERE, "vpage.py"), encoding="utf-8").read())
exec(open(os.path.join(HERE, "picker2.py"), encoding="utf-8").read())
exec(open(os.path.join(HERE, "towner_v4.py"), encoding="utf-8").read())
LAUNCHES = [p for p in LAUNCHES if p["slug"] not in VPAGE_ON_HOLD]
# visual pages first on the hub
LAUNCHES.sort(key=lambda p: (p["slug"] not in VPAGES, list(VPAGES).index(p["slug"]) if p["slug"] in VPAGES else 0))

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
    rel = [p for p in LAUNCHES if p["kind"] in g["kind"] or (g["slug"] == "new-condo-renovation" and p["kind"] in ("condo", "ec"))]
    secs = "".join(f'<section class="nl-sec"><h2 class="display">{e(h)}</h2>{ul(items)}</section>' for h, items in g["secs"])
    rel_html = ("<section class=\"nl-sec\"><h2 class=\"display\">New launches with guides</h2><ul class=\"nl-links\">" +
                "".join(f'<li><a href="{BASE}new-launches/{p["slug"]}/">{e(p["name"])} <span>{e(p["place"])}</span></a></li>' for p in rel) + "</ul></section>") if rel else ""
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

def launch_page(p):
    path = f"new-launches/{p['slug']}/"
    kl, gslug = KINDS[p["kind"]]
    g = GBY[gslug]
    facts = "".join(f"<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>" for a, b in p["facts"])
    work = "fit-out" if p["kind"] in ("office", "retail") else "renovation"
    q = f"Collecting keys at {p['name']}?"
    msg = f"Hi Maison, I'm collecting keys at {p['name']} and would like to discuss the {work}."
    title = (f"{p['name']} {'Fit-Out' if work == 'fit-out' else 'Renovation'} Guide | {p['place']} | Maison Interior Design")
    desc = f"{p['name']} ({p['place']}): key facts from public sources, what owners usually change, a handover defects check, {'landlord and authority rules' if work == 'fit-out' else 'renovation rules'} and a realistic timeline."
    srcs = p["sources"] + SRC_RULES[p["kind"]]
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("New launches", "new-launches/"), (p["name"], path)]),
              {"@type": "Article", "headline": f"{p['name']}: {work} guide for new owners and tenants", "description": desc,
               "datePublished": PUB, "dateModified": PUB, "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"},
               "mainEntityOfPage": DOMAIN + "/" + path, "about": {"@type": "Place", "name": p["name"]}, "citation": [u for _, u in p["sources"]]},
              faq_ld(p["faq"])]}
    s = head(title, desc, path, "62-Havelock-Road-Living-1-small-1024x683.jpg", schema)
    s += header("new-launches/")
    s += f"""<section class="phead"><div class="wrap narrow"><p class="eyebrow"><a href="{BASE}new-launches/">New launches</a> · {e(p['label'])}</p>
<h1 class="display">{e(p['name'])} <em>{work} guide</em></h1><p class="ph-p">{e(p['lede'])}</p></div></section>
<section class="sec tight nl-s"><div class="wrap narrow nl-body">
<dl class="nl-facts">{facts}<div class="nl-date"><dt>{e(p['date'][0])}</dt><dd>{e(p['date'][1])}</dd></div></dl>
{src_line(p['sources'])}
<section class="nl-sec"><h2 class="display">What to know about {e(p['name'])}</h2>{"".join("<p>"+e(x)+"</p>" for x in p['paras'])}</section>
<section class="nl-sec"><h2 class="display">What {'tenants' if work == 'fit-out' else 'owners'} usually change</h2>{ul(p['changes'])}</section>
<section class="nl-sec"><h2 class="display">{'Handover check' if work == 'fit-out' else 'Defects check at handover'}</h2>{ul(DEFECTS[p['kind']])}</section>
<section class="nl-sec"><h2 class="display">{'Rules and approvals' if work == 'fit-out' else 'What the rules allow'}</h2>{ul(RULES[p['kind']])}
<p>Rules change, so we check the current version for your unit before we quote. <a class="link" href="{BASE}services/{gslug}/">Full {e(g['short'].lower())} guide</a></p></section>
<section class="nl-sec"><h2 class="display">A realistic timeline</h2>{tl_html(TL[p['kind']], p['tl'])}</section>
<p class="nl-indep">{e(MAISON_INDEP)} We have not worked at {e(p['name'])} unless our portfolio says so. Facts on this page come only from the sources listed; prices and floor plans are not given.</p>
{src_line(srcs)}</div></section>
{faq_block(p['faq'])}{wa_cta(q, msg, p['slug'])}"""
    s += footer()
    write(path + "index.html", s)

HUB_FAQ = [("What is the difference between TOP and key collection?", "TOP (Temporary Occupation Permit) means the building can be occupied. Key collection comes after, on a date your developer or HDB gives you. We never treat a TOP date as your key date."),
           ("When should I contact an interior designer?", "One to two months before keys for a BTO or condo, and before you sign the lease for an office or shop. That leaves time for design, quotation and approvals so work starts on day one."),
           ("Are you the appointed interior designer for these projects?", "No. Maison is an independent firm, not appointed by or affiliated with any developer, HDB or building owner. We write these guides to help new owners and tenants plan."),
           ("Where do the project facts come from?", "Only from public sources linked on each page, such as HDB, the developer's own site or published reports. If we could not confirm a fact, we left it out or marked it as reported.")]

def hub():
    order = ["bto", "ec", "condo", "landed", "office", "retail"]
    chips = "".join(f'<button class="chip{" on" if k=="All" else ""}" data-f="{k}" aria-pressed="{"true" if k=="All" else "false"}">{k}</button>' for k in ["All"] + [KINDS[k][0] for k in order])
    def hcard(p):
        if p["slug"] in VPAGES:
            v = VPAGES[p["slug"]]
            return (f'<a class="lc lc-img" href="{BASE}new-launches/{p["slug"]}/" data-kind="{KINDS[p["kind"]][0]}">'
                    f'<figure>{vimg(p["slug"], v["hero"], "AI concept: " + p["name"] + " living and dining", sizes="(min-width:900px) 30vw, 100vw")}</figure>'
                    f'<span class="tag">{e(v["tag"])}</span><h3>{e(p["name"])} <em>{e(p["place"])}</em></h3><span class="more">See the concepts</span></a>')
        return (f'<a class="lc" href="{BASE}new-launches/{p["slug"]}/" data-kind="{KINDS[p["kind"]][0]}"><span class="tag">{e(p["label"])}</span>'
                f'<h3>{e(p["name"])} <em>{e(p["place"])}</em></h3><p>{e(p["date"][1].split(". ")[0].rstrip("."))}.</p><span class="more">Read the guide</span></a>')
    cards = "".join(hcard(p) for p in LAUNCHES)
    gcards = "".join(f'<a class="gc" href="{BASE}services/{g["slug"]}/"><h3>{e(g["short"])}</h3><p>{e(g["desc"])}</p><span class="more">Read the guide</span></a>' for g in GUIDES)
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("New launches", "new-launches/")]),
              {"@type": "CollectionPage", "name": "New launches renovation and fit-out guides", "hasPart": [{"@type": "Article", "headline": p["name"] + " guide", "url": DOMAIN + "/new-launches/" + p["slug"] + "/"} for p in LAUNCHES]},
              faq_ld(HUB_FAQ)]}
    s = head("New Launches Singapore 2026-2027 | BTO, Condo, Office & Shop Fit-Out Guides | Maison",
             "Renovation and fit-out guides for new BTO, EC, condo, landed, office and retail projects in Singapore reaching TOP or key collection in 2026-2027. Facts from public sources.",
             "new-launches/", "62-Havelock-Road-Living-1-small-1024x683.jpg", schema)
    s += header("new-launches/")
    s += f"""<section class="phead"><div class="wrap"><p class="eyebrow">New launches · 2026 to 2027</p>
<h1 class="display">Getting your keys? <em>Plan the renovation first</em></h1>
<p class="ph-p">Guides for BTO, EC, condo, landed, office and retail projects reaching TOP or handover in 2026 and 2027. Each page lists key facts from public sources, what owners usually change, a handover check, the rules that apply and a realistic timeline.</p>
<div class="chips" role="group" aria-label="Filter by property type">{chips}</div></div></section>
<section class="sec tight"><div class="wrap"><div class="lgrid" id="lgrid">{cards}</div>
<p class="nl-indep">{e(MAISON_INDEP)} Dates follow the wording of each page's source; a TOP date is not a key-collection date.</p></div></section>
<section class="sec tight nl-guides"><div class="wrap"><p class="eyebrow">Guides by property type</p><h2 class="display">Renovation and fit-out, <em>by type</em></h2><div class="ggrid">{gcards}</div></div></section>
{faq_block(HUB_FAQ, "About these guides")}{wa_cta("Collecting keys soon?", "Hi Maison, I'm collecting keys soon and would like to plan the renovation.", "new-launches")}"""
    s += footer()
    write("new-launches/index.html", s)

def launches_build():
    for sl in VPAGE_ON_HOLD:  # on hold (7 Nov): earlier pages were live, so point them to the hub
        write(f"new-launches/{sl}/index.html", f'<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url={BASE}new-launches/"><link rel="canonical" href="{DOMAIN}/new-launches/"><title>New launches | Maison Interior Design</title></head><body><a href="{BASE}new-launches/">New launches</a></body></html>')
    for g in GUIDES: guide_page(g)
    for p in LAUNCHES:
        if p["slug"] in VPAGES: vpage(p["slug"])
        else: launch_page(p)
    hub()

LAUNCH_URLS = ["new-launches/"] + [f"new-launches/{p['slug']}/" for p in LAUNCHES] + [f"services/{g['slug']}/" for g in GUIDES]
