#!/usr/bin/env python3
# Maison launch-page expander. Boilerplate (head, header, footer, plan section) copied from the LIVE pages read via the Bridge.
import sys, os, json, hashlib, html, re
from urllib.parse import quote

OUT = sys.argv[1]
WA = "6593391185"
CSS = open(os.path.join(os.path.dirname(__file__), "nlp-expand.css"), encoding="utf-8").read()
CSSV = hashlib.md5(CSS.encode()).hexdigest()[:8]
E = html.escape

SRC_MNH = "https://www.mynicehome.gov.sg/sales-launches/"
SRC_FLAT = "https://homes.hdb.gov.sg/home/landing"
SRC_HDC = "https://www.homeanddecor.com.sg/property/hdb/chencharu-acres-review"
SRC_HDP = "https://www.homeanddecor.com.sg/property/hdb/tengah-plantation-dew-review"
SRC_STK = "https://stackedhomes.com/november-2026-bto-review/"
SRC_EDGE = "https://www.edgeprop.sg/property-news/november-bto-exercise-launches-nearly-8000-flats-including-toa-payoh-and-bayshore-units"

LAY = {
 "2-room Flexi": "Keep the flat open and light. A full-height wardrobe wall, a bench seat with drawers and a sliding or fluted-glass partition give a bedroom feel without closing the space. Put a tall fridge and pantry run in the kitchen to save floor area. For senior owners we plan step-free floors, slip-resistant tiles and blocking in the walls for grab bars.",
 "3-room": "Treat the living and dining area as one room with a shoe cabinet at the entry and a slim TV and display wall. In the main bedroom a wardrobe along the longest wall usually frees the most floor. If the second bedroom doubles as a study, a fold-down or wall-hung desk keeps it flexible.",
 "4-room": "Most 4-room owners ask for four things: a kitchen with a tall pantry run, a main bedroom wardrobe wall, a living-room feature wall with hidden storage, and a built-in desk in a common bedroom. Use the service yard for a laundry cabinet and keep the walkway from the door to the living area clear.",
 "5-room": "The extra space suits a defined dining zone, a proper study nook and a longer feature wall that carries both display and closed storage. In the main bedroom a wardrobe wall plus a dressing counter works well. A full-height shoe and bag cabinet at the entry helps a larger household.",
 "3Gen": "Plan around who sleeps where and who uses which bathroom first. Keep walking routes wide and floors slip-resistant for grandparents, and give children a study corner that can be seen from the living area. Built-in wardrobes in every bedroom keep the shared spaces clear.",
 "Community Care Apartment": "Community Care Apartments are for senior owners, so the brief is comfort and safety: step-free floors, slip-resistant tiles, good lighting at night, blocking for grab bars and lever-type handles. Built-in storage keeps the walkways clear.",
}

P = {}
P["chencharu-acres"] = dict(
 name="Chencharu Acres", town="Yishun", region="North", units="1,582", cls="Standard",
 bounded="Yishun Street 82, Yishun Walk and Yishun Avenue 2",
 types=[("2-room Flexi","2room",None,None),("3-room","3room",None,None),("4-room","4room",None,None),("5-room","5room",None,None)],
 wait_off="under 4 years", wait_sec="39 or 41 months (about 3 years 3 to 5 months), per Home & Decor",
 mrt="Khatib MRT Station", mrt_note="Walking time is not stated by HDB, and the media reviews we read differ, so we leave it out.",
 schools=["Peiying Primary","Naval Base Primary","Naval Base Secondary","Orchid Park Secondary"],
 amen=["Khatib Central Neighbourhood Centre","Wisteria Mall","Northpoint City","Lower Seletar Reservoir Park","Khatib Bongsu Park Connector","Yishun Sport Centre","Yishun Swimming Complex","Nee Soon South CC","a future bus interchange"],
 sec=[("Home & Decor review of Chencharu Acres",SRC_HDC)], near=["sembawang-anchor","toa-payoh-hillside","plantation-dew"],
 extra_faq=[])
P["plantation-dew"] = dict(
 name="Plantation Dew", town="Tengah", region="West", units="710", cls="Standard",
 bounded="Tengah Garden Avenue and Plantation Walk",
 types=[("2-room Flexi","2room",None,None),("3-room","3room",None,None),("4-room","4room",None,None),("5-room","5room",None,None),("3Gen","3gen",None,None)],
 wait_off="under 4 years", wait_sec="3 years 2 months, per Home & Decor and EdgeProp (Stacked Homes says 38 months)",
 mrt="the upcoming JE2 Station on the Jurong Region Line", mrt_note="HDB names JE2. Other media name different Jurong Region Line stations, so check the station name and opening date with LTA before you plan around it.",
 schools=["Pioneer Primary","Jurong Primary","Jurongville Secondary"],
 amen=["Plantation Plaza","the future Tengah Town Centre","Tengah CC","Forest Corridor","Forest Fringe","Community Farmway","a future waterbody"],
 sec=[("Home & Decor review of Plantation Dew",SRC_HDP),("EdgeProp November 2026 BTO report",SRC_EDGE)], near=["chencharu-acres","bayshore-sails","toa-payoh-hillside"],
 extra_faq=[("Does Plantation Dew have 3Gen flats?","Yes. HDB lists 3Gen as one of the flat types at Plantation Dew, and it is the only project in the November 2026 launch that offers it. Tell us how many generations will live in the flat and we will plan the bedrooms, bathrooms and storage around them.")])
P["bayshore-sails"] = dict(
 name="Bayshore Sails", town="Bedok", region="East", units="1,637", cls="Plus",
 bounded="Bayshore Road and Bayshore Drive",
 types=[("2-room Flexi (Type 1)","2room-t1","322","38 to 40 sqm"),("2-room Flexi (Type 2)","2room-t2","568","48 sqm"),("3-room","3room","90","67 sqm"),("4-room","4room","657","90 sqm")],
 wait_off="under 4 years", wait_sec="44 months, per Stacked Homes (EdgeProp reports three years and two months for the Bayshore projects, so the media differ)",
 mrt="Bayshore MRT Station and the future Bedok South MRT Station", mrt_note="Stacked Homes puts Bayshore MRT about 110 m away in a straight line. That is not a walking time.",
 schools=["Temasek Primary","Temasek Secondary"],
 amen=["Bedok Town Centre","a future integrated development","East Coast Park","Heartbeat@Bedok","Siglap CC"],
 sec=[("Stacked Homes November 2026 BTO review (unit counts and sizes)",SRC_STK),("EdgeProp November 2026 BTO report",SRC_EDGE)], near=["toa-payoh-hillside","plantation-dew","chencharu-acres"],
 extra_faq=[("What are the Bayshore Sails flat sizes?","Stacked Homes lists the total floor area as 38 to 40 sqm for 2-room Flexi Type 1, 48 sqm for Type 2, 67 sqm for 3-room and 90 sqm for 4-room. These come from a media review, not from an HDB page we could copy, so confirm the size of your own unit on the HDB Flat Portal before you finalise a layout.")])
P["toa-payoh-hillside"] = dict(
 name="Toa Payoh Hillside", town="Toa Payoh", region="Central", units="1,432", cls="Prime",
 bounded="Toa Payoh Rise and Toa Payoh Link",
 types=[("Community Care Apartment","cca","256",None),("2-room Flexi","2room","592 (156 Type 1 and 436 Type 2)",None),("4-room","4room","584",None)],
 wait_off="under 4 years", wait_sec="45 months, per Stacked Homes",
 mrt="Caldecott MRT Station", mrt_note="Caldecott is an interchange of the Circle Line and the Thomson-East Coast Line, per Stacked Homes and EdgeProp.",
 schools=["Marymount Convent School","Raffles Girls' School (Secondary)","CHIJ Primary (Toa Payoh)","CHIJ Secondary (Toa Payoh)"],
 amen=["Toa Payoh Town Centre","Toa Payoh West Market & Food Centre","MacRitchie Reservoir","the future Toa Payoh Integrated Development","Toa Payoh West CC"],
 sec=[("Stacked Homes November 2026 BTO review (unit counts)",SRC_STK),("EdgeProp November 2026 BTO report",SRC_EDGE)], near=["bayshore-sails","chencharu-acres","sembawang-anchor"],
 extra_faq=[("What is a Community Care Apartment at Toa Payoh Hillside?","HDB lists Community Care Apartments as one of the flat types here, and EdgeProp confirms 256 of them. They are for senior owners. Tell us who will live in the flat and we will plan safety and storage first.")])
P["sembawang-anchor"] = dict(
 name="Sembawang Anchor", town="Sembawang", region="North", units="1,310", cls="Standard",
 bounded="Admiralty Lane and Sembawang Drive",
 types=[("2-room Flexi","2room",None,None),("3-room","3room",None,None),("4-room","4room",None,None),("5-room","5room",None,None)],
 wait_off="less than 3 years", wait_sec="2 years 10 months (34 months), per EdgeProp and Stacked Homes",
 mrt="Sembawang MRT Station", mrt_note="HDB does not state a walking time.",
 schools=["Northoaks Primary","Endeavour Primary","Canberra Primary","Canberra Secondary"],
 amen=["Sembawang Mart","Sun Plaza","a future neighbourhood centre","Bukit Canberra","Jelutung Harbour Park","Sembawang Park Connector","Sembawang Library"],
 sec=[("EdgeProp November 2026 BTO report",SRC_EDGE),("Stacked Homes November 2026 BTO review",SRC_STK)], near=["chencharu-acres","toa-payoh-hillside","plantation-dew"],
 extra_faq=[])

def wa(slug, name, ref, ptype=None):
    if ptype:
        t = f"Hi Maison, I’m collecting keys at {name} ({ptype}). Can I see design ideas and a quote?"
    else:
        t = f"Hi Maison, I’m planning my {name} renovation. Can I see design ideas and a quote?"
    return f"https://wa.me/{WA}?text={quote(t, safe='')}"

SVG = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>'

def btn(slug, name, ref, label, ptype=None, cls="nlp-wa"):
    return (f'<a class="{cls}" href="{wa(slug,name,ref,ptype)}" data-cta="whatsapp" data-ref="{slug}-{ref}" '
            f'data-path="/new-launches/{slug}/" rel="noopener">{SVG}<span>{E(label)}</span></a>')

def lst(items):
    return "".join(f"<li>{E(i)}</li>" for i in items)

def build(slug, d):
    n, town = d["name"], d["town"]
    title = f"{n} Renovation &amp; Interior Design | {town} BTO — Maison"
    desc = f"Interior design and built-in carpentry for {n}, an HDB BTO in {town}. Launch facts only; key dates unconfirmed. WhatsApp Maison with your plan."
    OLD_FAQ = [
     (f"When was {n} launched?","Our project file records: 2026-11 launch. That official confirmation covers the launch date only, not TOP or key collection."),
     (f"Is the key-collection date for {n} confirmed?","No. Completion and keys are unconfirmed in our file. Use your HDB documents for your own appointment, when you have one."),
     (f"Do you have the {n} floor plan?","No official floor-plan or site image is on file for this page, so none is published here. Please send your approved HDB unit plan."),
     ("What should I send Maison?","Your approved floor plan, unit type if you have it, and a key date if one is already in writing. After keys, an HDB renovation permit is required before works. WhatsApp us at https://wa.me/6593391185."),
    ]
    url = f"https://maisoninteriordesign.sg/new-launches/{slug}/"
    types = d["types"]
    tnames = ", ".join(t[0] for t in types[:-1]) + " and " + types[-1][0] if len(types) > 1 else types[0][0]

    # ---- FAQ
    faqs = [
     (f"What is the {n} floor plan?",
      f"HDB publishes the unit plans for each BTO project on the HDB Flat Portal, so that is the official source for the {n} floor plan. We do not copy or redraw them here. WhatsApp us your unit type and approved plan and we will draw layout and carpentry options for it."),
     (f"When is the {n} completion date?",
      f"HDB gives a waiting time of {d['wait_off']} for {n}, not a calendar date. Media estimate {d['wait_sec']}. Your own key-collection appointment comes from HDB after the project reaches that stage, so plan against what HDB tells you in writing."),
     (f"How many units and which flat types are in {n}?",
      f"HDB lists {d['units']} flats in {n}, {town}. The flat types are {tnames}. Unit counts and sizes per type are on the HDB Flat Portal for your exercise."),
     (f"Which MRT station is near {n}?",
      f"HDB names {d['mrt']}. {d['mrt_note']}"),
     (f"What schools and amenities are near {n}?",
      f"HDB lists these schools: {', '.join(d['schools'])}. Amenities named by HDB include {', '.join(d['amen'])}."),
     (f"How much does {n} renovation cost?",
      "The cost depends on your unit type and scope, mainly the amount of built-in carpentry. We have not published package prices, so WhatsApp us for a quote for your unit type. We give an itemised quotation so you can see what each part costs."),
     (f"What renovation ideas suit a {types[min(2,len(types)-1)][0]} at {n}?",
      LAY.get(types[min(2,len(types)-1)][0].split(" (")[0], LAY["4-room"])),
     (f"When can I start renovating {n}?",
      "After you collect your keys. Report defects within 30 days, apply for the HDB renovation permit through your contractor, then start works. Noisy works are limited to Monday to Friday, 9am to 5pm."),
    ] + d["extra_faq"] + OLD_FAQ
    faq_html = "".join(
        f'<details class="qa"><summary><h3>{E(q)}</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq"><p>{E(a)}</p></div></details>'
        for q, a in faqs)
    faq_ld = [{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in faqs]

    ld = {"@context":"https://schema.org","@graph":[
     {"@type":"HomeAndConstructionBusiness","@id":"https://maisoninteriordesign.sg/#business","name":"Maison Interior Design","url":"https://maisoninteriordesign.sg/","telephone":"+65 9339 1185","email":"maisoninteriordesignsg@gmail.com","foundingDate":"2018","areaServed":{"@type":"Country","name":"Singapore"},"image":"https://maisoninteriordesign.sg/wp-content/uploads/Jimmy-Monkey-Completed-6.jpg","founder":{"@type":"Person","name":"Roland Ng","jobTitle":"Managing Director"},"sameAs":["https://www.instagram.com/maison_interiordesign/","https://www.facebook.com/MaisonInteriorDesignSG"]},
     {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://maisoninteriordesign.sg/"},{"@type":"ListItem","position":2,"name":"New launches","item":"https://maisoninteriordesign.sg/new-launches/"},{"@type":"ListItem","position":3,"name":n,"item":url}]},
     {"@type":"Article","headline":f"{n} Renovation & Interior Design","description":desc,"datePublished":"2026-11-11","dateModified":"2026-11-11","author":{"@id":"https://maisoninteriordesign.sg/#business"},"publisher":{"@id":"https://maisoninteriordesign.sg/#business"},"mainEntityOfPage":url,
      "about":{"@type":"Place","name":n,"address":{"@type":"PostalAddress","addressLocality":town,"addressCountry":"SG"}},
      "keywords":f"{n} renovation, {n} interior design, {n} floor plan, {town} BTO renovation, {n} built-in carpentry, {town} interior design",
      "citation":["https://homes.hdb.gov.sg/home/bto"]},
     {"@type":"FAQPage","mainEntity":faq_ld}]}
    ld_s = json.dumps(ld, ensure_ascii=False, separators=(",", ":"))

    # ---- flat type cards
    cards = ""
    for tn, key, cnt, size in types:
        base = tn.split(" (")[0]
        tip = LAY.get(base, LAY["4-room"])
        meta = ""
        if cnt: meta += f"<li><b>Units</b> {E(cnt)}</li>"
        if size: meta += f"<li><b>Total floor area</b> {E(size)}</li>"
        cards += (f'<article class="nx-card"><h3>{E(tn)}</h3>'
                  + (f'<ul class="nx-meta">{meta}</ul>' if meta else '<p class="nx-meta-n">Unit count and size: see the HDB Flat Portal.</p>')
                  + f'<p>{E(tip)}</p>'
                  + btn(slug, n, f"type-{key}", f"Ideas and quote for {tn}", ptype=tn)
                  + '</article>')
    sec_note = ""
    if any(t[2] for t in types):
        sec_note = '<p class="nlp-small">Unit counts and sizes marked here come from a property-media review (see Sources), not an HDB page we could copy. Confirm your own unit on the HDB Flat Portal.</p>'

    # ---- ideas
    ideas = "".join(
        f'<div><h3 class="nlp-h3">Renovation ideas for {E(n)} {E(t[0])}</h3><p>{E(LAY.get(t[0].split(" (")[0], LAY["4-room"]))}</p></div>'
        for t in types)

    near = ""
    for s in d["near"]:
        o = P[s]
        near += (f'<a class="lc" href="/new-launches/{s}/" data-kind="BTO"><span class="tag">HDB BTO · {o["town"]}</span>'
                 f'<h3>{E(o["name"])} <em>{o["town"]}</em></h3><p>November 2026 BTO launch, {o["units"]} flats.</p><span class="more">Read the guide</span></a>')

    sources = (f'<li><a href="{SRC_MNH}" target="_blank" rel="noopener">HDB (MyNiceHome): November 2026 BTO sales launch</a> (official: location, units, flat types, MRT, schools, amenities, waiting time)</li>'
               f'<li><a href="{SRC_FLAT}" target="_blank" rel="noopener">HDB Flat Portal</a> (official floor plans and unit details)</li>'
               '<li><a href="https://homes.hdb.gov.sg/home/bto" target="_blank" rel="noopener">HDB: BTO</a></li>'
               '<li><a href="https://www.mynicehome.gov.sg/get-settled-in/hdb-renovation-guide/" target="_blank" rel="noopener">HDB renovation guide</a></li>'
               '<li><a href="https://www.mynicehome.gov.sg/get-settled-in/hdb-move-in-guide/" target="_blank" rel="noopener">HDB move-in guide</a></li>')
    sec_src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(t)}</a> (property media, not HDB)</li>' for t, u in d["sec"])

    glance = (f'<div><dt>Type</dt><dd>HDB BTO, {d["cls"]} classification (HDB)</dd></div>'
              f'<div><dt>Location</dt><dd>{town}, {d["region"]} region. Bounded by {E(d["bounded"])}</dd></div>'
              f'<div><dt>Units</dt><dd>{d["units"]} flats</dd></div>'
              f'<div><dt>Flat types</dt><dd>{E(tnames)}</dd></div>'
              f'<div><dt>Launch</dt><dd>November 2026 BTO exercise</dd></div>'
              f'<div><dt>Waiting time</dt><dd>HDB: {d["wait_off"]}. Media estimate: {E(d["wait_sec"])}. No key-collection date has been given</dd></div>'
              f'<div><dt>Nearest MRT</dt><dd>{E(d["mrt"])}</dd></div>')

    mid = f'''<section class="nx-band"><div class="wrap nx-band-in"><div><h2 class="nx-band-h">Collecting keys at {E(n)}?</h2><p>Tell us your unit type and we will send layout options and a quote for your unit.</p></div>@@BTN@@</div></section>'''
    def band(ref, label):
        return mid.replace("@@BTN@@", btn(slug, n, ref, label, cls="btn light nlp-wa-l"))

    plan = PLAN.replace("@@N@@", E(n))

    main = f'''<main id="main"><div class="nlp"><nav class="wrap nlp-crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/new-launches/">New launches</a><span aria-hidden="true">/</span><span aria-current="page">{E(n)}</span></nav><section class="nlp-hero"><div class="wrap nlp-hero-g"><div class="nlp-hero-t"><p class="nlp-eb">HDB BTO · {town} · {d["region"]} region</p><h1>{E(n)} Renovation &amp; Interior Design</h1><div class="nlp-intro"><p>Layouts, ideas and a quote for your {E(n)} flat.</p></div><div class="nlp-cta-row">{btn(slug,n,"hero","WhatsApp Maison about "+n)}<a class="link" href="#flat-types">See flat types</a></div></div></div></section>
<section class="nlp-s nx-types-s" id="flat-types"><div class="wrap"><h2 class="nlp-h2">{E(n)} flat types and renovation ideas</h2><div class="nx-types">{cards}</div>{sec_note}</div></section>
{band("cards","WhatsApp for my unit type")}
<section class="nlp-s nlp-facts-s"><div class="wrap"><h2 class="nlp-h2">{E(n)} at a glance</h2><dl class="nlp-facts">{glance}</dl><p class="nlp-small">Facts from HDB unless a line says otherwise. Sources are listed at the end of this page.</p></div></section>
<section class="nlp-s nx-ideas-s"><div class="wrap"><h2 class="nlp-h2">Renovation ideas for {E(n)}</h2><div class="nx-ideas">{ideas}</div><p>These are design approaches we use in HDB flats of each type. Your approved plan decides what is possible, so send it to us before you brief anyone on carpentry.</p></div></section>
{band("mid","Send my plan on WhatsApp")}
<section class="nlp-s nx-fp-s" id="floor-plan"><div class="wrap nlp-prose"><h2 class="nlp-h2">{E(n)} floor plan</h2><p>The official {E(n)} floor plans are published by HDB on the <a href="{SRC_FLAT}" target="_blank" rel="noopener">HDB Flat Portal</a>. We link to them instead of copying them, so you always see the current version. Once you have your unit plan, WhatsApp it to us and we will mark up where wardrobes, the kitchen run, the shoe cabinet and a study corner fit. We do not publish a {E(n)} plan of our own, and we do not guess one.</p></div></section>
<section class="nlp-s nx-around-s"><div class="wrap"><h2 class="nlp-h2">Around {E(n)}</h2><div class="nlp-2col"><div><h3 class="nlp-h3">Schools named by HDB</h3><ul class="ticks">{lst(d["schools"])}</ul></div><div><h3 class="nlp-h3">Amenities named by HDB</h3><ul class="ticks">{lst([a[0].upper()+a[1:] for a in d["amen"]])}</ul></div></div><p class="nlp-small">{E(d["mrt_note"])}</p></div></section>
<section class="nlp-s nx-check-s"><div class="wrap nlp-prose"><h2 class="nlp-h2">What to plan before key collection at {E(n)}</h2><ol class="nx-steps"><li>Confirm your unit type and keep a copy of the approved plan from HDB.</li><li>List what you need built in: kitchen run, wardrobes, shoe cabinet, living-room wall, study desk.</li><li>Ask for an itemised quotation and 3D drawings so you can compare scopes line by line.</li><li>Choose a contractor from HDB&#x27;s Directory of Renovation Contractors so the permit can be applied for properly.</li><li>After keys, report defects within 30 days, then book the start of works.</li></ol><p>Send us your unit type and we will fit this list to your plan.</p></div></section>
{plan}
<section class="nlp-s nlp-faq"><div class="wrap narrow"><h2 class="nlp-h2">{E(n)} renovation FAQ</h2>{faq_html}<div class="nx-faq-cta">{btn(slug,n,"faq","Ask Maison on WhatsApp")}</div></div></section>
<section class="nlp-s nlp-src"><div class="wrap narrow"><h2 class="nlp-h2">Sources</h2><ul>{sources}{sec_src}</ul><p class="nlp-small">Facts checked against these sources on 16 November 2026. HDB figures can change before launch day, so confirm on the HDB Flat Portal before you decide.</p><p class="nlp-small">Maison Interior Design is an independent interior design firm. We are not appointed by, or affiliated with, the developer, HDB or the building&#x27;s owner. We have not worked at {E(n)} unless our portfolio says so. We do not show concept pictures for this project yet.</p></div></section>
<section class="nlp-s nlp-near"><div class="wrap"><h2 class="nlp-h2">More November 2026 BTO launches</h2><div class="lgrid nlp-near-g">{near}</div><p class="nlp-small"><a href="/new-launches/">All new launches</a></p></div></section></div>
<section class="cta dark"><div class="wrap cta-in"><p class="eyebrow">Talk to Maison</p><h2 class="display">Planning your {E(n)} renovation?<br><em>WhatsApp Maison</em></h2><p class="cta-p">WhatsApp Maison with your unit type, approved floor plan and key date (if you have one).</p><div class="btns">{btn(slug,n,"end","WhatsApp +65 9339 1185",cls="btn light nlp-wa-l")}<a class="btn ghost-l" href="/new-launches/">All new launches</a></div></div></section></main>'''
    head = HEAD.replace("@@TITLE@@", title).replace("@@DESC@@", E(desc)).replace("@@URL@@", url).replace("@@LD@@", ld_s).replace("@@CSSV@@", CSSV)
    fab = FAB.replace("@@HREF@@", wa(slug, n, "dock")).replace("@@SLUG@@", slug)
    return head + main + FOOT.replace("@@FAB@@", fab)

HEAD = open(os.path.join(os.path.dirname(__file__), "head.html"), encoding="utf-8").read()
FOOT = open(os.path.join(os.path.dirname(__file__), "foot.html"), encoding="utf-8").read()
FAB = open(os.path.join(os.path.dirname(__file__), "fab.html"), encoding="utf-8").read().strip()
PLAN = open(os.path.join(os.path.dirname(__file__), "plan.html"), encoding="utf-8").read().strip()

os.makedirs(OUT, exist_ok=True)
for slug, d in P.items():
    p = os.path.join(OUT, "new-launches", slug)
    os.makedirs(p, exist_ok=True)
    open(os.path.join(p, "index.html"), "w", encoding="utf-8").write(build(slug, d))
open(os.path.join(OUT, "nlp-expand.css"), "w", encoding="utf-8").write(CSS)
print("css v", CSSV)
