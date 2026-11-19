#!/usr/bin/env python3
"""Ape Champs Swim preview builder. One shared layout (head, header, footer, mobile bar) + facts.json.
Run: python3 build.py  -> writes ../site/. Edit facts.json or this file, rebuild, every page updates."""
import json, os, hashlib, html, shutil, urllib.parse, datetime

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SRC), "site")
F = json.load(open(os.path.join(SRC, "facts.json")))
BASE = F["base"]
ORIGIN = F["origin"]
BRAND = F["brand"]
E = html.escape
TODAY = datetime.date.today().isoformat()


def sha8(path):
    return hashlib.sha256(open(os.path.join(SRC, path), "rb").read()).hexdigest()[:8]


V_CSS, V_JS, V_CTA = sha8("site.css"), sha8("site.js"), sha8("p1-cta.js")


def u(path=""):
    return BASE + path


def abs_url(path=""):
    return ORIGIN + BASE + path


def wa(kind="default", area=None):
    t = F["wa_text"][kind]
    if area:
        t = t.replace("{area}", area)
    return "https://wa.me/%s?text=%s" % (F["wa_number"], urllib.parse.quote(t))


ICON_WA = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2.2A9.7 9.7 0 0 0 3.7 16.9L2.3 21.8l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.5Z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m4 7 8 6 8-6"/></svg>'
ICON_MENU = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
ICON_GO = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6 6 6-6 6"/></svg>'


def wa_btn(ref, label="WhatsApp us", kind="default", area=None, cls="btn btn-wa", block=False):
    c = cls + (" block" if block else "")
    return ('<a class="%s" href="%s" target="_blank" rel="noopener" data-ref="%s">%s<span>%s</span></a>'
            % (c, E(wa(kind, area)), ref, ICON_WA, E(label)))


def waterline(fill="#082F49", tint="#0C3D5E"):
    # two drifting wave layers; 200% wide so translateX(-50%) loops seamlessly
    d = "M0 30 C 75 10 150 10 225 30 S 375 50 450 30 S 600 10 675 30 S 825 50 900 30 V60 H0Z"
    return ('<div class="waterline" aria-hidden="true">'
            '<svg class="w2" viewBox="0 0 900 60" preserveAspectRatio="none"><path d="%s" fill="%s"/></svg>'
            '<svg viewBox="0 0 900 60" preserveAspectRatio="none"><path d="%s" fill="%s"/></svg></div>'
            % (d.replace("30", "34", 1), tint, d, fill))


NAV = [("programmes/", "Programmes"), ("rates/", "Rates"), ("areas/", "Areas"), ("faq/", "FAQ"), ("contact/", "Contact")]

ORG_ID = abs_url("#org")


def org_schema():
    areas = [{"@type": "Place", "name": a["name"] + ", Singapore"} for a in F["areas"]]
    return {
        "@type": "Organization", "@id": ORG_ID, "name": BRAND, "legalName": F["legal_name"],
        "url": abs_url(), "logo": abs_url("img/logo.webp"), "email": F["email"],
        "identifier": {"@type": "PropertyValue", "propertyID": "UEN", "value": F["uen"]},
        "contactPoint": {"@type": "ContactPoint", "contactType": "customer service", "telephone": "+" + F["wa_number"],
                         "email": F["email"], "availableLanguage": "English", "areaServed": "SG"},
        "areaServed": areas,
        "knowsAbout": ["Kids swimming lessons", "Water confidence", "SwimSafer syllabus"],
    }


def page(path, title, desc, body, h1_crumb=None, extra_schema=None, robots_note=None):
    url = abs_url(path)
    graph = [org_schema(), {"@type": "WebPage", "@id": url + "#page", "url": url, "name": title, "description": desc,
                            "isPartOf": {"@type": "WebSite", "@id": abs_url("#site"), "url": abs_url(), "name": BRAND,
                                         "publisher": {"@id": ORG_ID}}, "inLanguage": "en-SG"}]
    if h1_crumb:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(p)} for i, (p, n) in enumerate(h1_crumb)]})
    graph += extra_schema or []
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    nav = "".join('<a href="%s"%s>%s</a>' % (u(p), ' aria-current="page"' if p == path else "", n) for p, n in NAV)
    crumbs = ""
    if h1_crumb:
        crumbs = '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(
            ('<a href="%s">%s</a>' % (u(p), E(n))) if i < len(h1_crumb) - 1 else '<span aria-current="page">%s</span>' % E(n)
            for i, (p, n) in enumerate(h1_crumb)) + "</nav>"
        body = body.replace("<!--CRUMBS-->", crumbs)
    year = datetime.date.today().year
    areas_ft = "".join('<li><a href="%s">%s</a></li>' % (u("areas/%s/" % a["slug"]), a["name"]) for a in F["areas"])
    return f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="robots" content="noindex, nofollow">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#082F49">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="en_SG">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{abs_url('img/og.jpg')}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Ape Champs Swim logo with the line: kids swim lessons at your condo pool">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{abs_url('img/og.jpg')}">
<link rel="icon" href="{u('img/favicon-32.png')}" sizes="32x32" type="image/png">
<link rel="icon" href="{u('img/icon-192.png')}" sizes="192x192" type="image/png">
<link rel="apple-touch-icon" href="{u('img/apple-touch-icon.png')}">
<link rel="preload" href="{u('fonts/fraunces-wght.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{u('site.css')}?v={V_CSS}">
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hd">
 <div class="wrap">
  <a class="brand" href="{u()}"><img src="{u('img/logo.webp')}" width="48" height="48" alt="Ape Champs Swim logo"><span>Ape Champs Swim</span></a>
  <nav class="nav" aria-label="Main">{nav}</nav>
  {wa_btn('whatsapp_header', 'WhatsApp us', cls='btn btn-wa sm')}
  <details class="menu"><summary aria-label="Menu">{ICON_MENU}</summary>
   <div class="sheet"><a href="{u()}"{' aria-current="page"' if path == '' else ''}>Home</a>{nav}{wa_btn('whatsapp_menu', 'WhatsApp us', block=True)}</div>
  </details>
 </div>
</header>
<main id="main">
{body}
</main>
<footer class="ft">
 {waterline('#082F49', '#0C3D5E').replace('class="waterline"', 'class="waterline" style="background:var(--ground)"')}
 <div class="wrap ft-in">
  <div>
   <a class="brand" href="{u()}"><img src="{u('img/logo.webp')}" width="48" height="48" alt="" loading="lazy"><span>Ape Champs Swim</span></a>
   <p style="margin-top:12px">Private kids' swim lessons at your condo pool, from 6 months to about 12 years.</p>
   {wa_btn('whatsapp_footer', 'WhatsApp ' + F['wa_display'])}
  </div>
  <div><h2>Lessons</h2><ul><li><a href="{u('programmes/')}">Programmes</a></li><li><a href="{u('rates/')}">Rates</a></li><li><a href="{u('#trial')}">Trial class</a></li><li><a href="{u('faq/')}">FAQ</a></li></ul></div>
  <div><h2>Areas</h2><ul>{areas_ft}</ul></div>
  <div><h2>Contact</h2><ul><li><a href="mailto:{F['email']}" data-ref="email_footer">{F['email']}</a></li><li><a href="{u('contact/')}">Contact and reply hours</a></li><li><a href="{u('terms/')}">Terms and cancellation</a></li><li><a href="{u('privacy/')}">Privacy</a></li></ul></div>
  <p class="legal">&copy; {year} {F['legal_name']} (UEN {F['uen']}). {BRAND} lessons follow the SwimSafer&reg; syllabus by Sport Singapore. SwimSafer&reg; is a registered mark of Sport Singapore.</p>
 </div>
</footer>
<div class="bar">{wa_btn('whatsapp_mobile_bar', 'WhatsApp us to book a trial', block=True)}</div>
<script src="{u('site.js')}?v={V_JS}" defer></script>
<script src="{u('p1-cta.js')}?v={V_CTA}" defer></script>
</body>
</html>
"""


def sec_end(ref, label="WhatsApp us", kind="default", note=None):
    n = '<p class="cta-note">%s</p>' % note if note else ""
    return '<div class="sec-end">%s%s</div>' % (wa_btn(ref, label, kind, block=True), n)


def board_html(ref=None):
    rows = "".join(
        '<div class="board-row"><b>%s</b><span class="price num">From %s<small style="display:block;font:400 .8rem var(--body);color:var(--on-deep-2)">per lesson</small></span><small>4 &times; %d-minute lessons, once a week</small></div>'
        % (p["short"], F["lesson_from"], p["length"]) for p in F["programmes"])
    g = "".join('<tr><td>%s</td><td class="num">%s</td><td class="num">%s</td><td class="num"><span class="big">%s</span></td></tr>'
                % (r["label"], r["per_child"], r["total"], r["per_lesson"]) for r in F["group"])
    return f"""<div class="boards">
<div class="board"><h3>Kids' programmes</h3><p class="sub">Private lessons at your condo pool.</p>{rows}</div>
<div class="board"><h3>Group classes</h3><p class="sub">Siblings or close friends sharing a coach. 4 &times; 45-minute lessons.</p>
<table class="gtable"><thead><tr><th scope="col">Coach to children</th><th scope="col">Per child, 4 lessons</th><th scope="col">Total, 4 lessons</th><th scope="col">Per child, per lesson</th></tr></thead><tbody>{g}</tbody></table></div>
</div>"""


FAQ = [
    ("Who are the lessons for?",
     "<p>Children, from about 6 months to about 12 years old. Most of our families live in condos. We are not an adult swim school.</p>"),
    ("Where do lessons happen?",
     "<p>At your condo pool only. We cover Punggol, Sengkang, Hougang, Tampines, Bukit Timah and Upper East Coast. We do not teach at landed homes or public pools. WhatsApp us your condo name to check availability.</p>"),
    ("What age can my child start?",
     "<p>Children from 6 months old can be introduced to the water through gentle water orientation. Most children start structured lessons around 3 to 4 years old, when they can follow simple instructions.</p>"),
    ("How do we start?",
     "<p>Book a trial class. It lasts 30 to 45 minutes, includes a water assessment and ends with a programme recommendation. If it is a good fit, regular weekly lessons follow.</p><p>Trial price: WhatsApp us to confirm.</p>"),
    ("Does my child keep the same coach?",
     "<p>Yes. After the trial, your child keeps the same coach every week. We have about 6 coaches on the team.</p>"),
    ("What happens if the coach is sick?",
     "<p>WhatsApp us to confirm how cover is arranged.</p>"),
    ("Do we need condo management approval, or a resident to book the pool?",
     "<p>WhatsApp us to confirm, with your condo name. The same applies if you are not sure whether your condo allows outside coaches.</p>"),
    ("Is it the SwimSafer syllabus?",
     "<p>Yes. Our lessons follow Sport Singapore's SwimSafer&reg; Stage 1 to 6 syllabus, with water safety, survival skills and assessment-based progression.</p>"),
    ("Do you run the official SwimSafer test? Are there test or certificate fees?",
     "<p>WhatsApp us to confirm. Our Water Explorer and ApeCore Ready awards are our own in-house confidence milestones, not official SwimSafer certificates.</p>"),
    ("How long is each lesson?",
     "<p>30 minutes for ApeStart&trade; (the youngest children) and 45 minutes for ApeCore&trade;, SwimSafer&reg; and Stroke Refinement. Lessons are once a week, in blocks of 4.</p>"),
    ("How much are lessons?",
     "<p>Kids' programmes are from $70 per lesson. Group classes for 2 to 4 children sharing a coach work out to $45, $33 or $28.75 per child per lesson. See the <a href=\"" + u("rates/") + "\">full rates</a>.</p>"),
    ("How and when do we pay?",
     "<p>Fees are billed per month or per block of lessons, with no hidden registration or admin fees. For payment methods and timing, WhatsApp us to confirm.</p>"),
    ("Can we ask for a female coach?",
     "<p>Yes, for an extra $10 per lesson.</p>"),
    ("Do you teach children with special needs?",
     "<p>Yes. Special needs swimming lessons are 30 minutes each, at an extra $10 per lesson. Tell us about your child when you WhatsApp us.</p>"),
    ("What should my child bring?",
     "<p>Swimwear, goggles or a swim cap if needed, a towel and a change of clothes. Bring floatation aids only if the coach recommends them.</p>"),
    ("What if it rains or there is lightning?",
     "<p>Light rain: lessons continue. If there is lightning or heavy rain that affects visibility, the lesson pauses or is postponed, and coaches may switch to dryland training. Each lesson package includes bad weather cancellations. See our <a href=\"" + u("terms/") + "\">terms</a>.</p>"),
    ("What if my child is unwell or we need to cancel?",
     "<p>Each lesson package includes 2 bad weather, 2 MC and 1 discretionary cancellation. The full rules are on our <a href=\"" + u("terms/") + "\">terms and cancellation page</a>.</p>"),
]


def faq_html(items):
    out = []
    for q, a in items:
        a2 = a.replace("WhatsApp us to confirm", '<span class="confirm">WhatsApp us to confirm</span>')
        out.append('<details><summary>%s</summary><div class="a">%s</div></details>' % (E(q), a2))
    return '<div class="faq">%s</div>' % "".join(out)


def faq_schema(items):
    import re
    def txt(h):
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h))).strip()
    return {"@type": "FAQPage", "@id": abs_url("faq/#faq"),
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": txt(a)}} for q, a in items]}


def service_schema():
    return {"@type": "Service", "@id": abs_url("#lessons"), "name": "Kids swimming lessons at condo pools",
            "serviceType": "Private kids swimming lessons", "provider": {"@id": ORG_ID},
            "areaServed": [{"@type": "Place", "name": a["name"] + ", Singapore"} for a in F["areas"]],
            "audience": {"@type": "PeopleAudience", "audienceType": "Children", "suggestedMinAge": 0.5, "suggestedMaxAge": 12},
            "offers": {"@type": "Offer", "priceCurrency": "SGD", "price": "70", "description": "From $70 per lesson, kids' programmes, 4-lesson blocks"}}


def build():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    pages = {}
    area_links = "".join('<li><a href="%s">%s%s</a></li>' % (u("areas/%s/" % a["slug"]), a["name"], ICON_GO) for a in F["areas"])
    area_names = ", ".join(a["name"] for a in F["areas"][:-1]) + " and " + F["areas"][-1]["name"]

    lanes = "".join(
        '<li><div><h3>%s</h3><div class="lane-meta"><span class="chip">%s</span><span class="chip">%d-minute lessons</span></div></div>'
        '<div><p>%s</p><ul>%s</ul></div></li>'
        % (p["name"], E(p["age"]), p["length"], E(p["lead"]), "".join("<li>%s</li>" % E(x) for x in p["points"]))
        for p in F["programmes"])

    # ---------- HOME ----------
    home = f"""
<section class="hero">
 <div class="wrap hero-grid">
  <div class="hero-copy">
   <h1>Kids' swim lessons at your condo pool</h1>
   <p class="lede">Same coach every week, for children from 6 months to 12 years.</p>
   <div class="cta-row">{wa_btn('whatsapp_home_hero', 'WhatsApp us to book a trial', 'trial', block=True)}</div>
  </div>
  <ul class="hero-aside" aria-label="At a glance" style="list-style:none;margin-top:0">
   <li><b>Condo pools only</b></li><li>{area_names}</li><li>SwimSafer&reg; syllabus</li><li>From $70 per lesson</li>
  </ul>
 </div>
 {waterline()}
</section>

<section class="band deep" id="who">
 <div class="wrap who-grid">
  <div>
   <h2><span class="q">1</span>Who it's for</h2>
   <p class="sub">Children, and the parents who want them safe and happy in the water. Most of our families live in condos, so the lesson comes to your own pool.</p>
  </div>
  <ul class="facts">
   <li><b>Ages</b><span>About 6 months to 12 years, from first splashes to stroke refinement.</span></li>
   <li><b>Families</b><span>Parents in condos who want lessons downstairs, not a drive away.</span></li>
   <li><b>Not for</b><span>Adults. We are a kids' swim school.</span></li>
  </ul>
 </div>
</section>

<section class="band" id="where">
 <div class="wrap">
  <h2><span class="q">2</span>Where we teach</h2>
  <p class="sub">At condo pools only, in six areas. We teach at {F['condos_regular']} condos regularly. WhatsApp us your condo name to check availability.</p>
  <ul class="areas">{area_links}</ul>
  <p class="not-list">We don't teach at landed homes or public pools.</p>
  {sec_end('whatsapp_home_where', 'WhatsApp your condo name')}
 </div>
</section>

<section class="band shallow" id="how">
 <div class="wrap">
  <h2><span class="q">3</span>How it works</h2>
  <ol class="steps">
   <li><h3>Book a trial class</h3><p>30 to 45 minutes at your pool, with a water assessment and a programme recommendation.</p></li>
   <li><h3>Keep the same coach</h3><p>After the trial, your child keeps the same coach every week. We have {F['coaches']} coaches on the team.</p></li>
   <li><h3>Swim once a week</h3><p>Lessons run in blocks of 4: 30 minutes for the youngest, 45 minutes for older programmes.</p></li>
  </ol>
  {sec_end('whatsapp_home_how', 'WhatsApp us to book a trial', 'trial')}
 </div>
</section>

<section class="band deep" id="levels">
 <div class="wrap">
  <h2><span class="q">4</span>Levels and programmes</h2>
  <p class="sub">Each child moves up lane by lane. After the trial we recommend the right starting level.</p>
  <ul class="lanes">{lanes}</ul>
  <p style="margin-top:20px"><a href="{u('programmes/')}">See programmes and our in-house awards</a></p>
  {sec_end('whatsapp_home_levels', 'Ask which level suits my child', 'programmes')}
 </div>
</section>

<section class="band" id="prices">
 <div class="wrap">
  <h2><span class="q">5</span>Prices</h2>
  <p class="sub">Clear rates, billed per month or per block of lessons. No hidden registration or admin fees.</p>
  {board_html()}
  <p style="margin-top:18px"><a href="{u('rates/')}">Full rates, extra options and cancellation credits</a></p>
  {sec_end('whatsapp_home_rates', 'WhatsApp us for a quote', 'rates')}
 </div>
</section>

<section class="band trial" id="trial">
 <div class="wrap">
  <h2><span class="q">6</span>Start with a trial</h2>
  <div class="trial-card">
   <ul><li>30 to 45 minutes at your condo pool</li><li>A water assessment by your coach</li><li>A programme recommendation, then weekly lessons if it is a fit</li></ul>
   <p><b>Trial price:</b> WhatsApp us to confirm.</p>
   {wa_btn('whatsapp_trial', 'WhatsApp us to book a trial', 'trial', block=True)}
  </div>
 </div>
</section>

<section class="band" id="faq">
 <div class="wrap">
  <h2><span class="q">7</span>Questions parents ask</h2>
  {faq_html(FAQ[:6])}
  <p style="margin-top:18px"><a href="{u('faq/')}">All questions</a></p>
  {sec_end('whatsapp_home_faq', 'Ask us on WhatsApp', 'faq')}
 </div>
</section>
"""
    pages[""] = page("", "Kids Swimming Lessons at Your Condo Pool | Ape Champs Swim",
                     "Private kids' swim lessons at your condo pool in Punggol, Sengkang, Hougang, Tampines, Bukit Timah and Upper East Coast. Ages 6 months to 12. WhatsApp to book a trial.",
                     home, extra_schema=[service_schema()])

    # ---------- PROGRAMMES ----------
    awards = "".join('<div class="award"><h3>%s</h3><p>%s</p><p style="margin:.6em 0 0;font-weight:600">What the coach looks for</p><ul>%s</ul></div>'
                     % (a["name"], E(a["purpose"]), "".join("<li>%s</li>" % E(c) for c in a["criteria"])) for a in F["awards"])
    prog = f"""
<section class="page-hero"><div class="wrap"><!--CRUMBS--><h1>Kids' swimming programmes</h1>
<p class="lede">Four levels, from first splashes to all four strokes. Your child's starting level is confirmed after the trial.</p>
{wa_btn('whatsapp_programmes_hero', 'Ask which level suits my child', 'programmes', block=True)}</div></section>
<section class="band deep"><div class="wrap"><h2>The four levels</h2><ul class="lanes">{lanes}</ul>
<p class="sub" style="margin-top:20px">ApeCore&trade; and SwimSafer&reg; follow Sport Singapore's SwimSafer&reg; Stage 1 to 6 syllabus.</p></div></section>
<section class="band"><div class="wrap"><h2>Our in-house confidence awards</h2>
<p class="label-note">These are Ape Champs Swim's own milestones for younger swimmers. They are not official SwimSafer&reg; certificates.</p>
<div class="awards">{awards}</div>
<p class="cta-note">Exact award checks may vary depending on starting level, attendance and practice.</p>
{sec_end('whatsapp_programmes', 'WhatsApp us to book a trial', 'trial')}</div></section>
"""
    pages["programmes/"] = page("programmes/", "Kids Swimming Programmes: ApeStart, ApeCore, SwimSafer | Ape Champs Swim",
                                "ApeStart water confidence (0.5 to 4 years), ApeCore learn-to-swim, SwimSafer Stage 1 to 6 (6 to 12) and Stroke Refinement (8 to 12), taught at your condo pool.",
                                prog, h1_crumb=[("", "Home"), ("programmes/", "Programmes")])

    # ---------- RATES ----------
    addons = "".join("<li>%s</li>" % E(a) for a in F["addons"])
    notes = "".join("<li>%s</li>" % E(a) for a in F["fee_notes"])
    rates = f"""
<section class="page-hero"><div class="wrap"><!--CRUMBS--><h1>Swimming lesson rates</h1>
<p class="lede">Kids' programmes from $70 per lesson, in blocks of 4 weekly lessons at your condo pool.</p></div></section>
<section class="band" style="padding-top:28px"><div class="wrap">
{board_html()}
<h2 style="margin-top:44px;font-size:1.6rem">Extra options</h2>
<p class="sub">On top of the rates above:</p><ul class="notes">{addons}</ul>
<h2 style="margin-top:36px;font-size:1.6rem">Good to know</h2><ul class="notes">{notes}</ul>
<h2 style="margin-top:36px;font-size:1.6rem">Cancellations</h2>
<p class="sub">Each lesson package includes 2 bad weather cancellations, 2 MC cancellations and 1 discretionary cancellation. After those are used, further cancellations are charged at 50% of the lesson fee. Lesson credits are non-refundable. Full rules: <a href="{u('terms/')}">terms and cancellation</a>.</p>
<h2 style="margin-top:36px;font-size:1.6rem">Trial class</h2>
<p class="sub">30 to 45 minutes, with a water assessment and a programme recommendation. Trial price: WhatsApp us to confirm.</p>
{sec_end('whatsapp_rates', 'WhatsApp us for a quote', 'rates')}
</div></section>
"""
    pages["rates/"] = page("rates/", "Kids Swimming Lesson Rates at Your Condo | Ape Champs Swim",
                           "Kids' swim lessons from $70 per lesson. Group classes 1 to 2 ($45), 1 to 3 ($33) and 1 to 4 ($28.75) per child per lesson. No hidden registration or admin fees.",
                           rates, h1_crumb=[("", "Home"), ("rates/", "Rates")],
                           extra_schema=[service_schema()])

    # ---------- AREAS HUB ----------
    hub = f"""
<section class="page-hero"><div class="wrap"><!--CRUMBS--><h1>Areas we cover</h1>
<p class="lede">Kids' swim lessons at condo pools in six areas. WhatsApp us your condo name to check availability.</p></div></section>
<section class="band" style="padding-top:28px"><div class="wrap">
<ul class="areas">{area_links}</ul>
<p class="not-list">Condo pools only. We teach at {F['condos_regular']} condos regularly. We don't teach at landed homes or public pools.</p>
{sec_end('whatsapp_areas', 'WhatsApp your condo name')}
</div></section>
"""
    pages["areas/"] = page("areas/", "Condo Swimming Lessons: Areas We Cover | Ape Champs Swim",
                           "Kids' swim lessons at condo pools in Punggol, Sengkang, Hougang, Tampines, Bukit Timah and Upper East Coast. WhatsApp your condo name to check.",
                           hub, h1_crumb=[("", "Home"), ("areas/", "Areas")])

    for a in F["areas"]:
        n, s = a["name"], a["slug"]
        others = ", ".join('<a href="%s">%s</a>' % (u("areas/%s/" % b["slug"]), b["name"]) for b in F["areas"] if b["slug"] != s)
        body = f"""
<section class="page-hero"><div class="wrap"><!--CRUMBS--><h1>Kids' swimming lessons in {n} condos</h1>
<p class="lede">Our coach comes to your condo pool in {n}. Send us your condo name to check availability.</p>
{wa_btn('whatsapp_area_' + s.replace('-', '_'), 'WhatsApp your ' + n + ' condo name', 'area', n, block=True)}</div></section>
<section class="band" style="padding-top:28px"><div class="wrap prose">
<h2>How lessons work in {n}</h2>
<ul><li>Lessons happen at your own condo pool in {n}. We don't teach at landed homes or public pools.</li>
<li>Start with a trial class of 30 to 45 minutes, with a water assessment and a programme recommendation.</li>
<li>After the trial, your child keeps the same coach every week.</li>
<li>Lessons run once a week in blocks of 4: 30 minutes for ApeStart&trade;, 45 minutes for older programmes.</li>
<li>Kids' programmes are from $70 per lesson. Siblings or close friends can share a coach from $28.75 per child per lesson (1 to 4). <a href="{u('rates/')}">See rates</a>.</li></ul>
<h2>Ages and levels</h2>
<p>From about 6 months (ApeStart&trade; water confidence) to about 12 years (Stroke Refinement), following the SwimSafer&reg; syllabus. <a href="{u('programmes/')}">See programmes</a>.</p>
<h2>Is my condo covered?</h2>
<p>We teach at {F['condos_regular']} condos regularly across our six areas. WhatsApp us your condo name in {n} and we'll confirm availability, along with any condo pool rules.</p>
<p class="cta-note">Other areas we cover: {others}.</p>
{sec_end('whatsapp_area_' + s.replace('-', '_') + '_end', 'WhatsApp us about ' + n, 'area', n)}
</div></section>
"""
        pages["areas/%s/" % s] = page("areas/%s/" % s, "Kids Swimming Lessons in %s Condos | Ape Champs Swim" % n,
                                      "Private kids' swim lessons at your condo pool in %s. Trial class, then the same coach every week. Ages 6 months to 12. WhatsApp your condo name to check." % n,
                                      body, h1_crumb=[("", "Home"), ("areas/", "Areas"), ("areas/%s/" % s, n)])

    # ---------- FAQ ----------
    fq = f"""
<section class="page-hero"><div class="wrap"><!--CRUMBS--><h1>Swimming lesson FAQ for parents</h1>
<p class="lede">Straight answers. Where we can't answer here yet, WhatsApp us and we'll confirm for your child and your condo.</p></div></section>
<section class="band" style="padding-top:20px"><div class="wrap prose">{faq_html(FAQ)}
{sec_end('whatsapp_faq', 'Ask us on WhatsApp', 'faq')}</div></section>
"""
    pages["faq/"] = page("faq/", "Kids Swimming Lessons FAQ | Ape Champs Swim",
                         "Ages, condo pools, the trial class, same coach every week, SwimSafer syllabus, lesson length, rates, what to bring, weather and cancellations.",
                         fq, h1_crumb=[("", "Home"), ("faq/", "FAQ")], extra_schema=[faq_schema(FAQ)])

    # ---------- CONTACT ----------
    opts = "".join('<option>%s</option>' % a["name"] for a in F["areas"])
    hours = "".join('<li><span>%s</span><span>%s</span></li>' % (d, t) for d, t in F["reply_hours"])
    contact = f"""
<section class="page-hero"><div class="wrap"><!--CRUMBS--><h1>Contact Ape Champs Swim</h1>
<p class="lede">WhatsApp is the fastest way to reach us. We usually reply within one working day.</p>
{wa_btn('whatsapp_contact', 'WhatsApp ' + F['wa_display'], block=True)}</div></section>
<section class="band" style="padding-top:28px"><div class="wrap contact-grid">
<div>
<h2>Tell us about your child</h2>
<p class="sub">Fill in a few details and we'll open WhatsApp with your message ready to send.</p>
<form class="form" id="waform" data-wa="1" data-ref="whatsapp_contact_form" action="https://wa.me/{F['wa_number']}" method="get" target="_blank">
<label>Child's age<input name="age" type="text" inputmode="text" autocomplete="off" placeholder="e.g. 4 years" required></label>
<label>Area<select name="area" required><option value="">Choose an area</option>{opts}</select></label>
<label>Condo name<input name="condo" type="text" autocomplete="off" placeholder="Your condo"></label>
<label>Swimming experience<select name="exp"><option value="">Choose one</option><option>New to the water</option><option>Comfortable in the water, can't swim yet</option><option>Can swim a little</option><option>Already swims, wants to improve</option></select></label>
<label>Anything else <span class="hint">(optional: siblings joining, special needs, female coach)</span><textarea name="msg"></textarea></label>
<input type="hidden" name="text" value="{E(F['wa_text']['default'])}">
<button class="btn btn-wa block" type="submit">{ICON_WA}<span>Send on WhatsApp</span></button>
<p class="cta-note">By sending, you agree that we may reply on WhatsApp about your enquiry. See our <a href="{u('privacy/')}">privacy notice</a>.</p>
</form>
</div>
<div>
<h2>Email</h2><p><a href="mailto:{F['email']}" data-ref="email_contact">{ICON_MAIL.replace('<svg', '<svg width="20" height="20" style="vertical-align:-4px;margin-right:6px"')}{F['email']}</a></p>
<h2 style="margin-top:28px">Reply hours</h2><p class="sub">These are the hours we reply to enquiries, not lesson hours.</p><ul class="hours">{hours}</ul>
<h2 style="margin-top:28px">Areas</h2><p>{area_names}. Condo pools only.</p>
</div>
</div></section>
"""
    pages["contact/"] = page("contact/", "Contact Ape Champs Swim | WhatsApp +65 8951 0121",
                             "WhatsApp Ape Champs Swim on +65 8951 0121 or email hello@apechampsswim.com.sg about kids' swim lessons at your condo pool.",
                             contact, h1_crumb=[("", "Home"), ("contact/", "Contact")])

    # ---------- TERMS (quoted from the current /terms) ----------
    terms = f"""
<section class="page-hero"><div class="wrap"><!--CRUMBS--><h1>Terms and cancellation policy</h1>
<p class="lede">Please read our lesson package inclusions and cancellation policy before booking.</p></div></section>
<section class="band" style="padding-top:20px"><div class="wrap prose">
<h2>What's included in every lesson package</h2>
<ul><li>2 bad weather cancellations</li><li>2 medical certificate (MC) cancellations</li><li>1 discretionary cancellation</li></ul>
<p>At Ape Champs Swim, we care about both our swimmers and our coaches. When a lesson is cancelled, it affects a coach&rsquo;s schedule and income. These terms are here to keep things fair for everyone, while still giving families flexibility when life happens. Thank you for supporting our coaches and respecting the guidelines below.</p>
<h2>Bad weather</h2>
<p>Swimming is an outdoor sport, and weather can be unpredictable.</p>
<ul><li>Light rain: Lessons will continue as planned.</li>
<li>Heavy rain or lightning alert: Coaches may switch to dryland training. This can include age-appropriate fitness work and simple theory modules to help swimmers understand technique and mechanics better.</li></ul>
<p>If you prefer to skip dryland training, each package includes 2 bad weather cancellations. Bad weather cancellations can only be used within 1.5 hours before lesson time.</p>
<p>After the 2 bad weather cancellations are fully used, further cancellations in place of dryland training will be charged at 50% of the lesson fee. We strongly encourage families to save bad weather cancellations for genuinely unsafe conditions rather than light drizzle. Thank you for helping us keep lessons safe, consistent and fair.</p>
<h2>Feeling unwell or injured</h2>
<p>We understand swimmers may occasionally be unwell or injured. Each package includes 2 MC cancellations, which may be used upon submission of a valid medical certificate issued by a registered General Practitioner in Singapore.</p>
<p>After the 2 MC cancellations have been used, any further cancellations will be charged at 50% of the lesson fee. We appreciate your understanding as this helps our coaches plan their time responsibly.</p>
<h2>Discretionary cancellation</h2>
<p>Each package includes 1 discretionary cancellation, which can be used for any reason, no questions asked. To help our coaches manage their schedules, please inform us at least 4 hours before lesson time when using this cancellation.</p>
<p>All lesson credits are strictly non-refundable. Thank you for your cooperation.</p>
<h2>Group lessons</h2>
<p>For group lessons, cancellations must be unanimously agreed upon by all swimmers or parents in the group. If unanimous agreement is not reached, the lesson will proceed as scheduled and be charged accordingly.</p>
<h2>Payments</h2>
<p>All payments and lesson credits are strictly non-refundable.</p>
<h2>Thank you for your understanding</h2>
<p>Thank you for being part of the Ape Champs Swim family. Your understanding helps us create a positive, respectful and sustainable environment for our swimmers and coaches alike.</p>
{sec_end('whatsapp_terms', 'Questions? WhatsApp us', 'faq')}
</div></section>
"""
    pages["terms/"] = page("terms/", "Terms and Cancellation Policy | Ape Champs Swim",
                           "Lesson package inclusions: 2 bad weather, 2 MC and 1 discretionary cancellation. Weather, MC, group lesson and refund rules for Ape Champs Swim.",
                           terms, h1_crumb=[("", "Home"), ("terms/", "Terms")])

    # ---------- PRIVACY ----------
    priv = f"""
<section class="page-hero"><div class="wrap"><!--CRUMBS--><h1>Website privacy notice</h1>
<p class="lede">How this website handles the details you send us when you enquire.</p></div></section>
<section class="band" style="padding-top:20px"><div class="wrap prose">
<h2>Who we are</h2><p>{BRAND} is run by {F['legal_name']} (UEN {F['uen']}), Singapore.</p>
<h2>What you send us</h2><p>When you WhatsApp or email us, you may share your name, phone number, your child's age, your area and condo, and your child's swimming experience. The enquiry form on our contact page does not store anything on this website: it only prepares a WhatsApp message that you choose to send.</p>
<h2>How we use it</h2><p>Only to reply to your enquiry and arrange lessons. We do not sell your details.</p>
<h2>Button tap counts</h2><p>This website counts taps on its WhatsApp and email buttons, with the page, the button and the device type, so we know which buttons parents use. It does not record your IP address or the contents of your messages.</p>
<h2>Your rights</h2><p>Under Singapore's Personal Data Protection Act you may ask to see or correct the personal data we hold about you, or ask us to stop contacting you.</p>
<h2>Contact</h2><p>Email <a href="mailto:{F['privacy_email']}" data-ref="email_privacy">{F['privacy_email']}</a> or <a href="mailto:{F['email']}" data-ref="email_privacy_hello">{F['email']}</a>.</p>
</div></section>
"""
    pages["privacy/"] = page("privacy/", "Website Privacy Notice | Ape Champs Swim",
                             "How Ape Champs Swim handles the details parents send by WhatsApp or email when enquiring about kids' swim lessons.",
                             priv, h1_crumb=[("", "Home"), ("privacy/", "Privacy")])

    # ---------- 404 ----------
    nf = f"""<section class="page-hero"><div class="wrap"><h1>This page isn't here</h1>
<p class="lede">Try the <a href="{u()}">home page</a>, <a href="{u('rates/')}">rates</a> or <a href="{u('faq/')}">FAQ</a>.</p>
{wa_btn('whatsapp_404', 'WhatsApp us', block=True)}</div></section>"""
    nf_html = page("404.html", "Page not found | Ape Champs Swim", "This page could not be found.", nf)

    for p, h in pages.items():
        d = os.path.join(OUT, p)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(h)
    open(os.path.join(OUT, "404.html"), "w").write(nf_html)
    sm = "".join("<url><loc>%s</loc><lastmod>%s</lastmod></url>" % (abs_url(p), TODAY) for p in pages)
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % sm)
    for f in ("site.css", "site.js", "p1-cta.js"):
        shutil.copy(os.path.join(SRC, f), OUT)
    shutil.copytree(os.path.join(SRC, "fonts"), os.path.join(OUT, "fonts"))
    shutil.copytree(os.path.join(SRC, "img"), os.path.join(OUT, "img"))
    print("built", len(pages) + 1, "pages ->", OUT)


if __name__ == "__main__":
    build()
