#!/usr/bin/env python3
# Maison full-concept launch pages (Edwin standard 16 Nov 2026). Usage: gen2.py OUTDIR [LD_MODE=full|keep]
import sys, os, json, html, hashlib
from urllib.parse import quote
from data import P, CAP
from wa_fix import fix_html  # WhatsApp link rules (16 Nov 2026): new tab, data-cta, short layout-plan text
OUT = sys.argv[1]
LD_FULL = (os.environ.get("LD_MODE", "full") == "full")
HERE = os.path.dirname(os.path.abspath(__file__))
rd = lambda f: open(os.path.join(HERE, f), encoding="utf-8").read()
HEAD, FOOT, FAB, PLAN = rd("head.html"), rd("foot.html"), rd("fab.html").strip(), rd("plan.html").strip()
CSS = rd("../gen/nlp-expand.css") + rd("nv.css")
CSSV = hashlib.md5(CSS.encode()).hexdigest()[:8]
E = html.escape
WA = "6593391185"
SVG = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>'
IMG = lambda d, f: f"/images/new-launches/{d['dir']}/{f}"

def wa(msg): return f"https://wa.me/{WA}?text={quote(msg, safe='')}"
def btn(slug, ref, label, msg, cls="nlp-wa"):
    return (f'<a class="{cls}" href="{wa(msg)}" data-cta="whatsapp" data-ref="{slug}-{ref}" data-path="/new-launches/{slug}/" target="_blank" rel="noopener">{SVG}<span>{E(label)}</span></a>')

def band(slug, n, ref, h, p, label, msg):
    return (f'<section class="nx-band"><div class="wrap nx-band-in"><div><h2 class="nx-band-h">{E(h)}</h2><p>{E(p)}</p></div>'
            + btn(slug, ref, label, msg, "btn light nlp-wa-l") + '</div></section>')

# ---- shared prose
THEORY = {
 "Living room": "Think of the living room as one long elevation. A tall, fluted or reeded wall breaks the glare of a flat surface, hides cabling and shelving behind doors, and lets cove light wash the wall. Warm timber and stone keep it calm, and handleless doors stop the wall from looking busy.",
 "Kitchen": "A compact HDB kitchen works when every surface earns its place. One continuous run keeps the working triangle short, a tall pantry column takes the bulk storage off the counter, and lit niches or a lit shelf give light where the work happens. A single matte colour on the doors keeps a small room from feeling cut up.",
 "Main bedroom": "A bedroom should feel lower, darker and quieter than the living room. A full-width bed-head wall with lit side niches replaces bedside tables, a built-in platform bed hides drawers, and a full-height wardrobe in one joinery set keeps lines continuous. Dim, warm light does the rest.",
 "Common bedroom": "A shared or child's room has to change with age. Put the bed on a platform with drawers, a wall-to-wall desk under the window with open knee space, and a tall wardrobe. A single accent colour on a few doors gives the room character that can be repainted later.",
}
PRACT = [("Light","Use the window wall for the desk or the dining bench so natural light does the work, then add cove, niche and shelf lighting for the evening. Mixing warm light in the living room and bedrooms keeps the home restful."),
 ("Flow","Keep a clear walking line from the door to the living area and from the kitchen to the dining table. Furniture that sits inside the joinery, not in front of it, keeps that line open."),
 ("Storage","Plan storage along whole walls, floor to ceiling, rather than in small pieces. Shoe and bag storage at the door, a pantry column in the kitchen and a wardrobe wall in every bedroom carry most households."),
 ("Small-space tricks","One material family across rooms, handleless doors, mirrors or reeded glass to bounce light, and built-in benches or platform beds with drawers all make a flat feel larger.")]

TS = {
 "2room": ("2-room Flexi", "Keep the flat open and light. A full-height wardrobe wall, a bench seat with drawers and a sliding or fluted-glass partition give a bedroom feel without closing the space. For senior owners, plan step-free floors, slip-resistant tiles and blocking in the walls for grab bars.", ["Wardrobe wall or bench storage","Tall fridge and pantry run in the kitchen","Slip-resistant tiles and wall blocking for grab bars where needed"], ["A sliding or fluted-glass partition","Lit niche shelf in the living area"], ["Closing the flat with full walls and losing the open feel","Choosing furniture before checking the doors and walkways"]),
 "2room-t1": None, "2room-t2": None,
 "3room": ("3-room", "Treat living and dining as one room with a shoe cabinet at the entry and a slim TV and display wall. In the main bedroom a wardrobe along the longest wall frees the most floor. If the second bedroom doubles as a study, a fold-down or wall-hung desk keeps it flexible.", ["Entry shoe cabinet","Kitchen run with a tall pantry or fridge column","Wardrobe wall in both bedrooms"], ["Fold-down desk in the second bedroom","Bench seat with drawers in the dining area"], ["Over-sized sofas that block the walkway","Deep wardrobes that leave no room to open the doors"]),
 "4room": ("4-room", "Most 4-room owners ask for four things: a kitchen with a tall pantry run, a main bedroom wardrobe wall, a living-room feature wall with hidden storage, and a built-in desk in a common bedroom. Use the service yard for a laundry cabinet and keep the walkway from the door to the living area clear.", ["Fitted kitchen with a tall pantry or fridge run","Full-height wardrobes in all bedrooms","Entry shoe cabinet and a living-room storage wall","Laundry cabinet in the service yard"], ["Built-in bench in the dining area","Platform bed with drawers in the main bedroom","Wall-to-wall study desk in a common bedroom"], ["Ordering furniture before you have the approved plan","Tall units placed where doors cannot open fully","Skipping lighting layers and relying on one ceiling light"]),
 "5room": ("5-room", "The extra space suits a defined dining zone, a proper study nook and a longer feature wall that carries both display and closed storage. In the main bedroom a wardrobe wall plus a dressing counter works well. A full-height shoe and bag cabinet at the entry helps a larger household.", ["Entry shoe and bag cabinet","Kitchen run with pantry column","Wardrobes in every bedroom"], ["A study nook with a built-in desk","Dressing counter in the main bedroom"], ["Letting the dining area crowd the living wing","Planning no storage for bulky items"]),
 "3gen": ("3Gen", "Plan around who sleeps where and who uses which bathroom first. Keep walking routes wide and floors slip-resistant for grandparents, and give children a study corner that can be seen from the living area. Built-in wardrobes in every bedroom keep the shared spaces clear.", ["Slip-resistant floors and wall blocking for grab bars where needed","Built-in wardrobes in every bedroom","Wide walking routes between bedrooms and bathrooms"], ["A study corner visible from the living area","Shared storage near the entry"], ["Planning bedrooms before agreeing who sleeps where","Narrow corridors that block a walking aid"]),
 "cca": ("Community Care Apartment", "Community Care Apartments are for senior owners, so the brief is comfort and safety: step-free floors, slip-resistant tiles, good lighting at night, blocking for grab bars and lever-type handles. Built-in storage keeps the walkways clear. Use your HDB documents for the rules that apply to this flat type.", ["Step-free floors and slip-resistant tiles","Night lighting along the route to the bathroom","Blocking for grab bars"], ["Built-in storage that keeps walkways clear"], ["Treating it like a family flat without checking HDB's rules"]),
}
TS["2room-t1"] = TS["2room-t2"] = TS["2room"]

NEARD={"sembawang-anchor":dict(name="Sembawang Anchor",town="Sembawang",units="1,310"),"chencharu-acres":dict(name="Chencharu Acres",town="Yishun",units="1,582"),"toa-payoh-hillside":dict(name="Toa Payoh Hillside",town="Toa Payoh",units="1,432"),"bayshore-sails":dict(name="Bayshore Sails",town="Bedok",units="1,637"),"plantation-dew":dict(name="Plantation Dew",town="Tengah",units="710")}

def build(slug, d):
    n, town = d["name"], d["town"]
    title = f"{E(n)} Renovation &amp; Interior Design | Floor Plan, Ideas, Quote — Maison"
    desc = f"{n} {town} {d.get('kind_lbl','BTO')}: {d.get('tw','flat')} types, floor plan guide, renovation ideas and a free layout plan for your unit type. WhatsApp Maison."
    old_title = f"{n} Renovation &amp; Interior Design | {town} BTO — Maison"
    url = f"https://maisoninteriordesign.sg/new-launches/{slug}/"
    types = d["types"]
    tn = [t[0] for t in types]
    tnames = ", ".join(tn[:-1]) + " and " + tn[-1]
    rs = d["renders"]; plans = d["plans"]
    primary = d.get("primary", "4-room"); pkey = d.get("pkey", "4room")
    TSd = dict(TS, **d.get("ts", {})); TH = dict(THEORY, **d.get("theory", {}))
    old_desc = f"Interior design and built-in carpentry for {n}, an HDB BTO in {town}. Launch facts only; key dates unconfirmed." + ("" if slug in ("sembawang-anchor","toa-payoh-hillside") else " WhatsApp Maison with your plan.")

    # ---- FAQ (every live question kept verbatim; answers refreshed)
    q7t = types[min(2, len(types)-1)][0]
    faqs = [
     (f"What is the {n} floor plan?", f"HDB publishes the official unit plans on the HDB Flat Portal. This page shows HDB's own 4-room Layout Ideas plan for {n}, copied as-is and credited, with a room-by-room walk-through below it. It is a typical plan, not your stack, so WhatsApp us your approved unit plan and we will draw layout and carpentry options for it."),
     (f"When is the {n} completion date?", f"HDB gives an estimated waiting time and estimated completion and delivery possession dates for {n}, listed in the at-a-glance table above. They are HDB estimates, not a confirmed key appointment. Plan against what HDB tells you in writing."),
     (f"How many units and which flat types are in {n}?", f"HDB lists {d['units']} flats in {n}, {town}. The flat types are {tnames}. The unit mix and approximate areas are in the flat types section above."),
     (f"Which MRT station is near {n}?", "HDB's project page lists the nearby transport and amenities. We do not publish walking times because HDB does not state them. Check the HDB project page linked in the sources for the current list."),
     (f"What schools and amenities are near {n}?", "HDB's project page lists nearby schools and amenities. Check the HDB project page linked in the sources, and confirm distances yourself before you decide."),
     (f"How much does {n} renovation cost?", "The cost depends on your unit type and scope, mainly the amount of built-in carpentry. We have not published package prices, so WhatsApp us for a quote for your unit type. We give an itemised quotation so you can see what each part costs."),
     (f"What renovation ideas suit a {q7t} at {n}?", TSd[types[min(2,len(types)-1)][1]][1]),
     (f"When can I start renovating {n}?", "After you collect your keys. Report defects within 30 days, apply for the HDB renovation permit through your contractor, then start works. Noisy works are limited to Monday to Friday, 9am to 5pm."),
    ] + d.get("faq_new", []) + [
     (f"When was {n} launched?", f"It was offered in HDB's November 2026 BTO exercise. Applications closed on 11 November 2026."),
     (f"Is the key-collection date for {n} confirmed?", "No. HDB publishes estimated waiting times and estimated completion and delivery possession dates, not individual key appointments. Use your HDB documents for your own appointment, when you have one."),
     (f"Do you have the {n} floor plan?", f"Yes. HDB's official 4-room Layout Ideas plan is shown on this page, copied as-is and credited. It is a typical type plan, not a specific stack. Please send your approved HDB unit plan."),
     ("What should I send Maison?", "Your approved floor plan, unit type if you have it, and a key date if one is already in writing. After keys, an HDB renovation permit is required before works. WhatsApp us at https://wa.me/6593391185."),
    ]
    if "faqs" in d: faqs = d["faqs"]
    faqs = [(q, d.get("ans", {}).get(q, a)) for q, a in faqs]
    faq_html = "".join(f'<details class="qa"><summary><h3>{E(q)}</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq"><p>{E(a)}</p></div></details>' for q, a in faqs)

    ld_desc = desc if LD_FULL else old_desc
    ld = {"@context":"https://schema.org","@graph":[
     {"@type":"HomeAndConstructionBusiness","@id":"https://maisoninteriordesign.sg/#business","name":"Maison Interior Design","url":"https://maisoninteriordesign.sg/","telephone":"+65 9339 1185","email":"maisoninteriordesignsg@gmail.com","foundingDate":"2018","areaServed":{"@type":"Country","name":"Singapore"},"image":"https://maisoninteriordesign.sg/wp-content/uploads/Jimmy-Monkey-Completed-6.jpg","founder":{"@type":"Person","name":"Roland Ng","jobTitle":"Managing Director"},"sameAs":["https://www.instagram.com/maison_interiordesign/","https://www.facebook.com/MaisonInteriorDesignSG"]},
     {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://maisoninteriordesign.sg/"},{"@type":"ListItem","position":2,"name":"New launches","item":"https://maisoninteriordesign.sg/new-launches/"},{"@type":"ListItem","position":3,"name":n,"item":url}]},
     {"@type":"Article","headline":f"{n} Renovation & Interior Design","description":ld_desc,"datePublished":d.get("pub","2026-11-11"),"dateModified":d.get("mod","2026-11-16") if LD_FULL else "2026-11-11","author":{"@id":"https://maisoninteriordesign.sg/#business"},"publisher":{"@id":"https://maisoninteriordesign.sg/#business"},"mainEntityOfPage":url,
      "image":[f"https://maisoninteriordesign.sg/images/new-launches/{d['dir']}/{d['dir'].replace('-v4','')}-v4-{r['stem']}-1920.webp" for r in rs],
      "about":{"@type":"Place","name":n,"address":{"@type":"PostalAddress","addressLocality":town,"addressCountry":"SG"}},
      "keywords":d.get("kw") or f"{n} renovation, {n} interior design, {n} floor plan, {town} BTO renovation, {n} built-in carpentry, {d['old_kwl']}",
      "citation":d.get("cite",["https://homes.hdb.gov.sg/home/bto"])},
     {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q, a in (faqs if LD_FULL else faqs)]}]}
    ld_s = json.dumps(ld, ensure_ascii=False, separators=(",", ":"))

    # ---- hero carousel
    slides = ""
    for i, r in enumerate(rs):
        b = f"{d['dir'].replace('-v4','')}-v4-{r['stem']}"
        slides += (f'<figure class="nv-slide" id="s{i}"><img src="{IMG(d,b+"-1920.webp")}" srcset="{IMG(d,b+"-900.webp")} 900w, {IMG(d,b+"-1920.webp")} 1920w" sizes="100vw" width="1920" height="1080" alt="{E(r["alt"])}" style="object-position:{r["pos"]}"'
                   + (' fetchpriority="high"' if i == 0 else ' loading="lazy"') + f'><figcaption><b>{E(r["room"])}: {E(r["style"])}</b><span>{E(CAP)}</span></figcaption></figure>')
    dots = "".join(f'<button type="button" class="nv-dot" aria-label="Show concept {i+1}: {E(r["room"])}" data-i="{i}"></button>' for i, r in enumerate(rs))
    hero = (f'<section class="nv-hero"><div class="nv-car" id="car" role="region" aria-label="{E(n)} concept images, swipe to browse" tabindex="0">{slides}</div>'
            f'<div class="nv-ctl"><button type="button" class="nv-arr" data-d="-1" aria-label="Previous concept">&#8592;</button><div class="nv-dots">{dots}</div><button type="button" class="nv-arr" data-d="1" aria-label="Next concept">&#8594;</button></div>'
            f'<div class="wrap nv-hero-t"><h1>{E(n)} Renovation &amp; Interior Design</h1><p class="nv-lead">Four concepts, the official plan and a free layout for your unit.</p>'
            + btn(slug, "hero", f"WhatsApp Maison about {n}", f"Hi Maison, I'm planning my {n} renovation. Can I see design ideas and a quote?") + '</div></section>')

    # ---- flat type cards
    cards = ""
    for t, key, info in types:
        k = TSd[key]
        cards += (f'<article class="nx-card"><h3>{E(t)}</h3><p class="nx-meta-n">{E(info)}</p><p>{E(k[1])}</p>'
                  + btn(slug, f"type-{key}", f"Free layout plan for {t}", f"Hi Maison, I'd like a free layout plan for my {t} at {n}.") + '</article>')
    glance = "".join(f'<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in d["glance"])

    # ---- space planning
    figs = ""
    for p in plans:
        src = IMG(d, p["img"])
        figs += (f'<figure class="nv-plan"><a href="{src}" target="_blank" rel="noopener"><img src="{src}" width="{p["w"]}" height="{p["h"]}" alt="{E(p["alt"])}" loading="lazy"></a>'
                 f'<figcaption><b>{E(p["title"])}</b>{E(p["cap"])} <span class="nv-cr">{E(p["credit"])} (<a href="{p["curl"]}" target="_blank" rel="noopener">source</a>). Tap the plan to open it full size.</span></figcaption></figure>')
    r4 = d["rooms4"]
    rooms = "".join(f'<li><h4>{h}</h4><p>{E(r4[k])}</p></li>' for h, k in [("Living and dining","living"),("Kitchen and service yard","kitchen"),("Main bedroom and bath","main"),("Common bedrooms","common"),("Common bath","other")])
    zoning = (f'<div class="nv-pl-g"><div><h3 class="nlp-h3">Zoning and traffic flow</h3><ul class="ticks"><li>Public zone: entry, living and dining. Keep the line from the door to the kitchen clear.</li><li>Service zone: kitchen and service yard, close to the dining table and the household shelter.</li><li>Private zone: bedrooms and baths, away from the entry so the living area works as a buffer.</li></ul></div>'
              f'<div><h3 class="nlp-h3">Keep or hack?</h3><ul class="ticks"><li>{d.get("keep1","Keep: the household shelter walls. HDB does not allow them to be hacked or drilled.")}</li><li>{d.get("keep2","Check first: any other wall. We confirm with your approved plan and the permit rules before we quote.")}</li><li>Prefer joinery over hacking: a fluted wall, bench or niche changes the room without touching the structure.</li></ul></div></div>')
    other_types = "".join(f'<li><h4>{E(t)}</h4><p>{E(info)}. {E(d.get("oth_txt","The official layout idea for this type is on the HDB Flat Portal."))} Send us your plan and we will draw zoning, storage and traffic flow for it.</p></li>' for t, k, info in types if k != pkey)
    space = (f'<section class="nlp-s nv-space" id="space-planning"><div class="wrap"><h2 class="nlp-h2">{E(n)} floor plan and space planning</h2>{figs}'
             f'<p class="nlp-small">{E(d["plan_gaps"])}</p><h3 class="nlp-h3">The {E(d.get("plan_lbl", primary))} plan, room by room</h3><ol class="nv-rooms">{rooms}</ol>{zoning}'
             + (f'<h3 class="nlp-h3">Other {d.get("tw","flat")} types</h3><ul class="nv-oth">{other_types}</ul>' if other_types else '') + '</div></section>')

    # ---- design concepts
    cs = ""
    for r in rs:
        feat = {"Living room":d["feat"]["living"],"Kitchen":d["feat"]["kitchen"],"Main bedroom":d["feat"]["main"],"Common bedroom":d["feat"]["common"]}[r["room"]]
        cs += (f'<article class="nv-con"><h3>{E(r["room"])}: {E(r["style"])}</h3><p>{E(r["text"])}</p><p><b>Why it suits this flat.</b> It is drawn for {E(feat)}. {E(TH[r["room"]])}</p></article>')
    prac = "".join(f'<li><h4>{a}</h4><p>{E(b)}</p></li>' for a, b in PRACT)
    concepts = f'<section class="nlp-s nv-concepts" id="concepts"><div class="wrap"><h2 class="nlp-h2">The design thinking behind the four concepts</h2><div class="nv-con-g">{cs}</div><h3 class="nlp-h3">Practical design rules we use</h3><ul class="nv-prac">{prac}</ul><p class="nlp-small">AI concept designs for illustration only. Views and room proportions are illustrative. {E(CAP)}.</p></div></section>'

    # ---- recommendations per flat type
    rec = ""
    for t, key, info in types:
        k = TSd[key]
        li = lambda xs: "".join(f"<li>{E(x)}</li>" for x in xs)
        rec += (f'<article class="nv-rec"><h3>{E(t)} at {E(n)}</h3><div class="nv-rec-g"><div><h4>Must-do</h4><ul class="ticks">{li(k[2])}</ul></div><div><h4>Nice to have</h4><ul class="ticks">{li(k[3])}</ul></div><div><h4>Common mistakes</h4><ul class="ticks">{li(k[4])}</ul></div></div></article>')
    chk = d.get("chk") or ["Confirm your unit type and keep a copy of the approved plan from HDB.","List what you need built in: kitchen run, wardrobes, shoe cabinet, living-room wall, study desk.","Ask for an itemised quotation and 3D drawings so you can compare scopes line by line.","Choose a contractor from HDB's Directory of Renovation Contractors so the permit can be applied for properly.","After keys, report defects within 30 days, then book the start of works."]
    reco = (f'<section class="nlp-s nv-recs" id="recommendations"><div class="wrap"><h2 class="nlp-h2">Recommendations for your {d.get("tw","flat")} type</h2>{rec}<h3 class="nlp-h3">Checklist before key collection</h3><ol class="nx-steps">{"".join(f"<li>{E(c)}</li>" for c in chk)}</ol></div></section>')

    # ---- trust, related, links
    trust = ('<section class="nlp-s nv-trust"><div class="wrap"><h2 class="nlp-h2">' + d.get('trust_h','HDB homes Maison has designed') + '</h2><div class="nv-tr-g">'
             '<a class="nv-tr" href="/portfolio/teck-whye-crescent/"><img src="/wp-content/uploads/Completed-Blk-10-Teck-Whye-1.jpg" alt="Completed HDB 3-bedroom flat at Teck Whye Crescent by Maison" loading="lazy" width="640" height="427"><span>Teck Whye Crescent Blk 10, HDB 3-bedroom, designed and built</span></a>'
             '<a class="nv-tr" href="/portfolio/tampines-street-22/"><img src="/wp-content/uploads/3D-Visual-Blk-296-Tampines-St-22-3-scaled.jpg" alt="3D visual of an HDB home at Tampines Street 22 by Maison" loading="lazy" width="640" height="427"><span>Tampines Street 22 Blk 296, six 3D visuals for an HDB home</span></a>'
             '<a class="nv-tr" href="/portfolio/bedok-reservoir-road/"><img src="/img/bedok/dining-living.jpg" alt="Whole-home design and build at Bedok Reservoir Road by Maison" loading="lazy" width="640" height="427"><span>Bedok Reservoir Blk 715, a whole-home design and build</span></a>'
             '</div><p class="nlp-small"><a href="/portfolio/">See the portfolio</a></p></div></section>')
    arts = ('<section class="nlp-s nv-rel"><div class="wrap"><h2 class="nlp-h2">Related articles</h2><ul class="nv-links"><li><a href="/articles/itemised-renovation-quotation/">Itemised Renovation Quotation: What to Check</a></li><li><a href="/articles/prepare-for-interior-design-consultation/">Interior Design Consultation Singapore: What to Prepare</a></li>' + d.get("rel3", '<li><a href="/services/bto-renovation/">BTO key collection renovation guide</a></li>') + '</ul></div></section>')
    near = ""
    for s in d["near"]:
        o = NEARD[s]
        near += f'<a class="lc" href="/new-launches/{s}/" data-kind="BTO"><span class="tag">HDB BTO · {o["town"]}</span><h3>{E(o["name"])} <em>{o["town"]}</em></h3><p>November 2026 BTO launch, {o["units"]} flats.</p><span class="more">Read the guide</span></a>'
    for s, kind, tag, nm, tw, blurb in d.get("near_cards", []):
        near += f'<a class="lc" href="/new-launches/{s}/" data-kind="{kind}"><span class="tag">{E(tag)}</span><h3>{E(nm)} <em>{E(tw)}</em></h3><p>{E(blurb)}</p><span class="more">Read the guide</span></a>'
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{E(t)}</a> {E(d.get("src_tag","(HDB, official)"))}</li>' for t, u in d["extra_src"])
    src += d['base_src'] if 'base_src' in d else '<li><a href="https://homes.hdb.gov.sg/home/bto" target="_blank" rel="noopener">HDB: BTO</a></li><li><a href="https://www.mynicehome.gov.sg/get-settled-in/hdb-renovation-guide/" target="_blank" rel="noopener">HDB renovation guide</a></li><li><a href="https://www.mynicehome.gov.sg/get-settled-in/hdb-move-in-guide/" target="_blank" rel="noopener">HDB move-in guide</a></li>'

    intro_sec = f'<section class="nlp-s nv-about"><div class="wrap nlp-prose"><h2 class="nlp-h2">About {E(n)}</h2><p>{E(d["intro"])}</p><p class="nlp-small">{E(d.get("checked","Facts checked against HDB sources on 16 November 2026."))} We do not list prices. {E(d.get("aff","Maison is not affiliated with HDB."))}</p></div></section>'

    ask = lambda ref, label, msg: ""
    b2 = band(slug, n, "plan", f"Get a free layout plan for your {primary} at {n}", "Send your unit plan and we will mark up zoning, storage and walkways for it.", f"Get my free {primary} layout plan", f"Hi Maison, I'd like a free layout plan for my {primary} at {n}.")
    b3 = band(slug, n, "recs", f"Want this scoped for your {n} flat?", "Tell us your unit type and we will send a checklist and an itemised quote for your scope.", "Get my itemised quote", f"Hi Maison, I'm collecting keys at {n}. Can I get an itemised quote for my unit type?")
    b4 = band(slug, n, "mid", f"Collecting keys at {n}?", "Tell us your unit type and we will send layout options and a quote for your unit.", "Send my plan on WhatsApp", f"Hi Maison, I'm collecting keys at {n}. Can you send layout options for my unit?")
    crumbs = f'<nav class="wrap nlp-crumbs" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/new-launches/">New launches</a><span aria-hidden="true">/</span><span aria-current="page">{E(n)}</span></nav>'
    main = (f'<main id="main"><div class="nlp">{crumbs}{hero}'
            f'<section class="nlp-s nx-types-s" id="flat-types"><div class="wrap"><h2 class="nlp-h2">{E(n)} {d.get("tw","flat")} types and renovation ideas</h2><div class="nx-types">{cards}</div></div></section>'
            f'<section class="nlp-s nlp-facts-s"><div class="wrap"><h2 class="nlp-h2">{E(n)} at a glance</h2><dl class="nlp-facts">{glance}</dl></div></section>'
            f'{space}{b2}{concepts}{reco}{b3}{trust}{d.get("plan_html", PLAN).replace("@@N@@", E(n))}{intro_sec}{arts}'
            f'<section class="nlp-s nlp-faq"><div class="wrap narrow"><h2 class="nlp-h2">{E(n)} renovation FAQ</h2>{faq_html}<div class="nx-faq-cta">{btn(slug,"faq","Ask Maison on WhatsApp",f"Hi Maison, I have a question about my {n} renovation.")}</div></div></section>'
            f'<section class="nlp-s nlp-src"><div class="wrap narrow"><h2 class="nlp-h2">Sources and links</h2><ul>{src}</ul><p class="nlp-small">Maison Interior Design is an independent interior design firm. We are not appointed by, or affiliated with, the developer, HDB or the building\'s owner. We have not worked at {E(n)}. Concept images are AI concept designs by Maison, not the actual unit.</p></div></section>'
            f'<section class="nlp-s nlp-near"><div class="wrap"><h2 class="nlp-h2">{E(d.get("near_h","More November 2026 BTO launches"))}</h2><div class="lgrid nlp-near-g">{near}</div><p class="nlp-small"><a href="/new-launches/">All new launches</a></p></div></section></div>'
            f'<section class="cta dark"><div class="wrap cta-in"><h2 class="display">Planning your {E(n)} renovation?<br><em>WhatsApp Maison</em></h2><p class="cta-p">WhatsApp Maison with your unit type, approved floor plan and key date (if you have one).</p><div class="btns">{btn(slug,"end","Get my free layout plan",f"Hi Maison, I'd like a free layout plan for my {primary} at {n}.","btn light nlp-wa-l")}<a class="btn ghost-l" href="/new-launches/">All new launches</a></div></div></section></main>')
    script = ('<script>(function(){var c=document.getElementById("car");if(!c)return;var s=c.children,ds=document.querySelectorAll(".nv-dot"),i=0;'
              'function go(k){i=(k+s.length)%s.length;c.scrollTo({left:s[i].offsetLeft,behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth"})}'
              'function mark(){var k=Math.round(c.scrollLeft/c.clientWidth);i=k;ds.forEach(function(d,j){d.setAttribute("aria-current",j===k?"true":"false")})}'
              'c.addEventListener("scroll",function(){window.requestAnimationFrame(mark)},{passive:true});mark();'
              'document.querySelectorAll(".nv-arr").forEach(function(b){b.addEventListener("click",function(){go(i+parseInt(b.dataset.d,10))})});'
              'ds.forEach(function(d){d.addEventListener("click",function(){go(parseInt(d.dataset.i,10))})});'
              'c.addEventListener("keydown",function(e){if(e.key==="ArrowRight")go(i+1);if(e.key==="ArrowLeft")go(i-1)})})();</script>')
    head = HEAD.replace("@@TITLE@@", title).replace("@@DESC@@", E(desc)).replace("@@URL@@", url).replace("@@LD@@", ld_s).replace("@@CSSV@@", CSSV)
    fab = FAB.replace("@@HREF@@", wa(f"Hi Maison, I'm planning my {n} renovation. Can I see design ideas and a quote?")).replace("@@SLUG@@", slug)
    foot = FOOT.replace("@@FAB@@", fab).replace('<script src="/mid.js', script + '<script src="/mid.js', 1)
    return head + main + foot
    
only = sys.argv[2].split(",") if len(sys.argv) > 2 else list(P)
os.makedirs(OUT, exist_ok=True)
for slug in only:
    html_ = build(slug, P[slug])
    html_ = html_.replace("</body>", "", 1) if False else html_
    p = os.path.join(OUT, "new-launches", slug); os.makedirs(p, exist_ok=True)
    open(os.path.join(p, "index.html"), "w", encoding="utf-8").write(fix_html(html_))
open(os.path.join(OUT, "nlp-expand.css"), "w", encoding="utf-8").write(CSS)
print("css", CSSV, only)
