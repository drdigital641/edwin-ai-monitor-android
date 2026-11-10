#!/usr/bin/env python3
"""Build the AutoSEO.my static site.

    python3 autoseo-my/src/build.py

Reads brand facts from data/brand.json, page text from data/content.py and the
shared parts (head, header/nav, page hero, FAQ block, CTA band, footer +
WhatsApp button) from templates/. Writes fully rendered HTML to site/, then
runs check.py; a failed check stops the build with exit code 1.
"""
import hashlib
import html
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "data"))
import content as C  # noqa: E402

BRAND = json.loads((ROOT / "data" / "brand.json").read_text(encoding="utf-8"))
TPL = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / "templates").glob("*.html")}
OUT = ROOT / "site"
BASE = BRAND["base_path"]
E = html.escape


def fill(tpl, **kw):
    out = TPL[tpl]
    for k, v in kw.items():
        out = out.replace("{{" + k + "}}", str(v))
    if "{{" in out:
        raise SystemExit(f"template {tpl}: unfilled placeholder near {out[out.find('{{'):out.find('{{') + 40]!r}")
    return out


def wa(key="general", topic=""):
    msg = BRAND["prefills"][key].replace("{topic}", topic)
    return E(f"https://wa.me/{BRAND['whatsapp_number']}?text={quote(msg, safe='')}")


def url(path=""):
    return BASE + path


def abs_url(path=""):
    return BRAND["site_url"].rstrip("/") + "/" + path if BRAND["site_url"] else ""


# ------------------------------------------------------------------ assets
CSS = (ROOT / "assets" / "base.css").read_text(encoding="utf-8") + "\n" + (ROOT / "assets" / "brand.css").read_text(encoding="utf-8")
JS = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
ASSET_V = hashlib.sha256((CSS + JS).encode()).hexdigest()[:10]

NAV = [("services/", "Services"), ("industries/", "Industries"), ("how-it-works/", "How it works"), ("about/", "About"), ("faq/", "FAQ"), ("contact/", "Contact")]


def nav_links(current):
    rows = []
    for p, label in NAV:
        cur = ' aria-current="page"' if current and current.startswith(p) else ""
        rows.append(f'        <a href="{url(p)}"{cur}>{label}</a>')
    return "\n".join(rows)


# ------------------------------------------------------------------ schema
def org_schema():
    org = {
        "@type": "Organization",
        "@id": "#organization",
        "name": BRAND["name"],
        "slogan": BRAND["tagline"],
        "description": f"{BRAND['name']} is a brand of {BRAND['company']}: an automotive-exclusive SEO, AEO and GEO marketing agency for automotive businesses in Malaysia.",
        "parentOrganization": {"@type": "Organization", "name": BRAND["company"]},
        "areaServed": [{"@type": "Country", "name": BRAND["country"]}] + [{"@type": "Place", "name": a} for a in BRAND["areas"]],
        "knowsAbout": ["Search Engine Optimisation", "Answer Engine Optimisation", "Generative Engine Optimisation", "Automotive marketing", "Google Business Profile"],
        "contactPoint": {"@type": "ContactPoint", "contactType": "customer service", "url": f"https://wa.me/{BRAND['whatsapp_number']}", "areaServed": "MY"},
    }
    site = {"@type": "WebSite", "@id": "#website", "name": BRAND["name"], "inLanguage": BRAND["lang"], "publisher": {"@id": "#organization"}}
    if BRAND["site_url"]:
        org["url"] = abs_url()
        org["@id"] = abs_url() + "#organization"
        site["url"] = abs_url()
        site["@id"] = abs_url() + "#website"
        site["publisher"] = {"@id": org["@id"]}
    return [org, site]


def faq_schema(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def schema_tag(graph):
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f'  <script type="application/ld+json">\n{data}\n  </script>'


# ------------------------------------------------------------------ blocks
def faq_block(faqs, heading, kicker="Questions, answered", alt=False, after=""):
    items = "\n".join(f'          <details class="reveal"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs)
    return fill("faq_block", alt=" alt" if alt else "", kicker=kicker, heading=heading, items=items, after=after)


def cta_band(cta_id, primary=("audit", ""), heading=C.HERO_H1, text=" ".join(C.HERO_LINES)):
    return fill("cta_band", heading=E(heading), text=E(text), cta_id=cta_id, wa_primary=wa(*primary),
                btn_primary=C.BTN_AUDIT, wa_secondary=wa("specialist"), btn_secondary=C.BTN_SPECIALIST)


def page_hero(crumbs, eyebrow, h1, lead, cta_id, primary=("audit", "")):
    crumb_html = " / ".join([f'<a href="{url(p)}">{E(t)}</a>' for p, t in crumbs[:-1]] + [E(crumbs[-1][1])])
    return fill("page_hero", crumbs=crumb_html, eyebrow=E(eyebrow), h1=E(h1), lead=E(lead), cta_id=cta_id,
                wa_primary=wa(*primary), btn_primary=C.BTN_AUDIT, wa_secondary=wa("specialist"), btn_secondary=C.BTN_SPECIALIST)


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"


def chips(items):
    return '<ul class="search-chips" aria-label="Example searches">' + "".join(f"<li>“{E(i)}”</li>" for i in items) + "</ul>"


def section(inner, alt=False, dark=False, narrow=False, sid=""):
    cls = "section" + (" alt" if alt else "") + (" dark" if dark else "")
    idattr = f' id="{sid}"' if sid else ""
    return f'    <section class="{cls}"{idattr}>\n      <div class="wrap{" narrow" if narrow else ""}">\n{inner}\n      </div>\n    </section>\n'


def service_cards(link_text="More details →"):
    cards = []
    for s in C.SERVICES:
        cards.append(f'          <a class="card reveal" href="{url("services/" + s["slug"] + "/")}"><div class="emoji" aria-hidden="true">{s["emoji"]}</div><p class="pill">{s["n"]:02d}</p><h3>{E(s["title"])}</h3><p>{E(s["text"])}</p><span class="card-link">{link_text}</span></a>')
    return '        <div class="cards three plain-cards" style="margin-top:28px">\n' + "\n".join(cards) + "\n        </div>"


def industry_grid():
    cells = [f'          <a class="ind reveal" href="{url("industries/" + i["slug"] + "/")}"><span aria-hidden="true">{i["emoji"]}</span>{E(i["label"])}</a>' for i in C.INDUSTRIES]
    cells.append(f'          <a class="ind reveal" href="{wa("general")}" target="_blank" rel="noopener" data-cta="whatsapp_other_industry"><span aria-hidden="true">➕</span>{E(C.OTHER_INDUSTRY)}</a>')
    return '        <div class="ind-grid">\n' + "\n".join(cells) + "\n        </div>"


def why_cards():
    cards = [f'          <div class="card reveal"><div class="emoji" aria-hidden="true">{em}</div><h3>{E(t)}</h3><p>{E(d)}</p></div>' for t, d, em in C.WHY]
    return '        <div class="cards two plain-cards" style="margin-top:28px">\n' + "\n".join(cards) + "\n        </div>"


# ------------------------------------------------------------------ page shell
PAGES = []


def page(path, title, description, body, current="", faqs=None, body_class="", extra_schema=None):
    graph = org_schema()
    if faqs:
        graph.append(faq_schema(faqs))
    if extra_schema:
        graph.extend(extra_schema)
    robots = '  <meta name="robots" content="noindex,nofollow">\n' if BRAND["preview"] else '  <meta name="robots" content="index, follow, max-image-preview:large">\n'
    canonical = f'  <link rel="canonical" href="{abs_url(path)}">\n' if BRAND["site_url"] else ""
    og_url = f'  <meta property="og:url" content="{abs_url(path)}">\n' if BRAND["site_url"] else ""
    shared = dict(base=BASE, brand_name=E(BRAND["name"]), brand_name_html=BRAND["name_html"], logo_letter=BRAND["logo_letter"],
                  wa_general=wa("general"))
    doc = fill("head", lang=BRAND["lang"], title=E(title), description=E(description), robots=robots, canonical=canonical,
               og_url=og_url, og_locale=BRAND["og_locale"], asset_v=ASSET_V, schema=schema_tag(graph), base=BASE, brand_name=E(BRAND["name"]))
    doc += fill("header", body_class=body_class, nav_links=nav_links(current), **shared)
    doc += body
    doc += fill("footer", tagline=E(BRAND["tagline"]), whatsapp_label=E(BRAND["whatsapp_label"]), year=date.today().year,
                brand_line=E(BRAND["brand_line"]),
                footer_services="\n".join(f'        <a href="{url("services/" + s["slug"] + "/")}">{E(s["short"])}</a>' for s in C.SERVICES),
                footer_industries="\n".join(f'        <a href="{url("industries/" + i["slug"] + "/")}">{E(i["short"])}</a>' for i in C.INDUSTRIES),
                **shared)
    PAGES.append((path, doc))


# ------------------------------------------------------------------ home
def build_home():
    marquee_items = "".join(f'<span><span class="dot"></span>{E(i["label"])}</span>' for i in C.INDUSTRIES) + f'<span><span class="dot"></span>{E(C.OTHER_INDUSTRY)}</span>'
    channels = [("Google Search", "SEO"), ("Google Maps", "Local SEO"), ("Featured snippets", "AEO"), ("ChatGPT", "GEO"), ("Google Gemini", "GEO"), ("Perplexity", "GEO")]
    chan_html = "".join(f"<li><span>{E(c)}</span><b>{E(t)}</b></li>" for c, t in channels)
    body = f'''    <section class="hero hero-lean">
      <span class="glow glow-1" aria-hidden="true"></span>
      <span class="glow glow-2" aria-hidden="true"></span>
      <div class="wrap hero-grid">
        <div>
          <p class="eyebrow"><span class="live" aria-hidden="true"></span>{E(C.HERO_LINES[0])}</p>
          <h1>{E(C.HERO_H1)}</h1>
          <p class="hero-tagline grad-text">{E(BRAND["tagline"])}</p>
          <p class="lead">{E(BRAND["positioning"])}. {E(C.HERO_LINES[1])}</p>
          <div class="cta-row hero-ctas">
            <a class="btn" href="{wa("audit")}" target="_blank" rel="noopener" data-cta="whatsapp_home_audit">{C.BTN_AUDIT}</a>
            <a class="btn btn-ghost" href="{wa("specialist")}" target="_blank" rel="noopener" data-cta="whatsapp_home_specialist">{C.BTN_SPECIALIST}</a>
          </div>
          <p class="hero-paths">{E(BRAND["focus_line"])}</p>
        </div>
        <figure class="proof-card search-card" aria-label="Where motorists look for automotive businesses">
          <span class="chip chip-1">🚗 Built for automotive</span>
          <div class="proof-top"><span class="proof-src">Where motorists look</span><span class="proof-real">SEO · AEO · GEO</span></div>
          <p class="search-bar"><span aria-hidden="true">🔍</span> car workshop near me</p>
          <ul class="proof-ranks channel-list">{chan_html}</ul>
          <figcaption>Is your business there when they search?</figcaption>
          <span class="chip chip-2">📍 KL · Selangor · JB · Penang</span>
        </figure>
      </div>
    </section>

    <div class="marquee" aria-label="Industries we serve">
      <p class="marquee-label">100% automotive · <a href="{url("industries/")}">Industries we serve</a></p>
      <div class="marquee-track" aria-hidden="true">{marquee_items}{marquee_items}</div>
    </div>
'''
    about = f'''        <p class="kicker reveal">About {E(BRAND["name"])}</p>
        <h2 class="reveal">{E(BRAND["positioning"])}</h2>
        <p class="section-lead reveal"><strong>{E(BRAND["focus_line"])}</strong></p>
''' + "".join(f'        <p class="reveal">{E(p)}</p>\n' for p in C.ABOUT_PARAS) + f'        <p class="reveal goal">{E(C.GOAL)}</p>\n        <p class="reveal"><a class="link" href="{url("about/")}">More about us →</a></p>'
    body += section(about, narrow=True)
    services = f'''        <p class="kicker reveal">Our Digital Marketing Solutions</p>
        <h2 class="reveal">Six ways we help motorists find you</h2>
        <p class="section-lead reveal">Each service has its own page with the detail. <a class="link" href="{url("services/")}">See all services →</a></p>
{service_cards()}'''
    body += section(services, alt=True)
    ind = f'''        <p class="kicker reveal">Industries We Serve</p>
        <h2 class="reveal">Only automotive businesses</h2>
        <p class="section-lead reveal">We work with the whole automotive trade, from the workshop down the road to the distributor that supplies it.</p>
{industry_grid()}'''
    body += section(ind, dark=True)
    why = f'''        <p class="kicker reveal">Why Choose {E(BRAND["name"])}?</p>
        <h2 class="reveal">Specialists in automotive search</h2>
{why_cards()}'''
    body += section(why)
    steps = "".join(f'          <div class="card reveal"><p class="pill">{E(s[0])}</p><h3>{E(s[1])}</h3><p>{E(s[2])}</p></div>\n' for s in C.STEPS)
    how = f'''        <p class="kicker reveal">How it works</p>
        <h2 class="reveal">From free audit to more enquiries</h2>
        <div class="cards four plain-cards" style="margin-top:28px">
{steps}        </div>
        <p class="note reveal" style="text-align:center"><a class="link" href="{url("how-it-works/")}">How it works in detail →</a></p>'''
    body += section(how, alt=True)
    body += f'''    <section class="mission">
      <div class="wrap narrow">
        <p class="kicker reveal">Our Mission</p>
        <p class="mission-text reveal">{E(C.MISSION)}</p>
      </div>
    </section>
'''
    home_faqs = C.FAQS[:C.HOME_FAQ_COUNT]
    body += faq_block(home_faqs, "Automotive SEO in Malaysia: your questions, answered",
                      after=f'        <p class="note reveal" style="text-align:center">More in the <a class="link" href="{url("faq/")}">full FAQ</a>.</p>')
    body += cta_band("home")
    page("", f"{BRAND['name']} | Automotive SEO, AEO & GEO Agency in Malaysia",
         "Automotive-only SEO, AEO and GEO agency in Malaysia. Help motorists in KL, Selangor, Johor Bahru and Penang find your business on Google, Maps and AI search.",
         body, faqs=home_faqs, body_class="home")


# ------------------------------------------------------------------ services
def build_services():
    body = page_hero([("", "Home"), ("services/", "Services")], "Our Digital Marketing Solutions",
                     "Automotive SEO, AEO and GEO services in Malaysia",
                     "Six services, one aim: make your automotive business easier to find, easier to trust and easier to choose.", "services")
    body += section(f'''        <p class="kicker reveal">What we do</p>
        <h2 class="reveal">Choose a service to see what it covers</h2>
{service_cards()}''')
    body += section(f'''        <p class="kicker reveal">How they fit together</p>
        <h2 class="reveal">Search has changed. Your marketing should too.</h2>
        <p class="reveal">Motorists still search Google and Google Maps, but more of them now get a direct answer, or ask an AI tool such as ChatGPT, Gemini or Perplexity. SEO gets your pages ranking, AEO turns your knowledge into clear answers, and GEO helps AI tools find and trust your brand. Your website, Google Business Profile and content tie it all together, and every page ends with an easy WhatsApp enquiry.</p>
        <p class="reveal">Pricing depends on what your business needs. <a class="link" href="{wa("quote")}" target="_blank" rel="noopener" data-cta="whatsapp_services_quote">WhatsApp for a quote →</a></p>''', alt=True, narrow=True)
    body += cta_band("services")
    page("services/", f"Automotive SEO, AEO & GEO Services in Malaysia | {BRAND['name']}",
         "Automotive SEO, AEO, GEO, website design, Google Maps and content services for Malaysian automotive businesses. WhatsApp for a free audit.",
         body, current="services/")

    for s in C.SERVICES:
        topic = s["short"]
        body = page_hero([("", "Home"), ("services/", "Services"), ("", s["short"])], f"Service {s['n']:02d} of 06",
                         s["h1"], s["text"], "svc_" + s["slug"].replace("-", "_"), primary=("service", topic))
        body += section(f'''        <p class="kicker reveal">Why it matters</p>
        <h2 class="reveal">{E(s["title"])}</h2>
        <p class="reveal">{E(s["why"])}</p>''', narrow=True)
        body += section(f'''        <p class="kicker reveal">What it covers</p>
        <h2 class="reveal">What we work on</h2>
        <div class="reveal">{ticks(s["covers"])}</div>
        <h3 class="reveal" style="margin-top:28px">The kind of searches this is for</h3>
        <p class="reveal note">Examples only. Your plan is built on what your own customers search.</p>
        <div class="reveal">{chips(s["searches"])}</div>''', alt=True, narrow=True)
        others = [o for o in C.SERVICES if o["slug"] != s["slug"]]
        rel = "".join(f'<a class="card reveal" href="{url("services/" + o["slug"] + "/")}"><div class="emoji" aria-hidden="true">{o["emoji"]}</div><h3>{E(o["title"])}</h3><span class="card-link">More details →</span></a>' for o in others[:3])
        body += faq_block(s["faqs"], f"{s['short']}: common questions")
        body += section(f'''        <p class="kicker reveal">Works well with</p>
        <h2 class="reveal">Related services</h2>
        <div class="cards three plain-cards" style="margin-top:24px">{rel}</div>''', alt=True)
        body += cta_band("svc_" + s["slug"].replace("-", "_"), primary=("service", topic))
        page(f"services/{s['slug']}/", f"{s['h1']} | {BRAND['name']}", s["meta"], body, current="services/", faqs=s["faqs"])


# ------------------------------------------------------------------ industries
def build_industries():
    body = page_hero([("", "Home"), ("industries/", "Industries")], "100% automotive",
                     "Industries We Serve", "We focus entirely on the automotive industry, so we understand how motorists and trade buyers search for each kind of business.", "industries")
    body += section(f'''        <p class="kicker reveal">Who we help</p>
        <h2 class="reveal">Automotive businesses across Malaysia</h2>
{industry_grid()}''', dark=True)
    body += section(f'''        <p class="kicker reveal">Same goal for every business</p>
        <h2 class="reveal">Easier to find, easier to trust, easier to choose</h2>
        <p class="reveal">Whatever part of the automotive trade you are in, the work starts with how your customers search: the words they use, the areas they search in, and whether they use Google, Google Maps or an AI tool. Choose your industry above to see what we focus on, or WhatsApp us if yours isn’t listed.</p>''', narrow=True)
    body += cta_band("industries")
    page("industries/", f"Automotive Industries We Serve in Malaysia | {BRAND['name']}",
         "SEO, AEO and GEO for car workshops, dealerships, tyre shops, accessories, aircon, detailing, EV and hybrid, parts and equipment businesses in Malaysia.",
         body, current="industries/")

    for i in C.INDUSTRIES:
        body = page_hero([("", "Home"), ("industries/", "Industries"), ("", i["label"])], "Industries We Serve",
                         i["h1"], i["intro"], "ind_" + i["slug"].replace("-", "_"), primary=("industry", i["who"]))
        body += section(f'''        <p class="kicker reveal">What we focus on</p>
        <h2 class="reveal">How we help {E(i["label"].lower())}</h2>
        <div class="reveal">{ticks(i["focus"])}</div>''', narrow=True)
        body += section(f'''        <p class="kicker reveal">How your customers search</p>
        <h2 class="reveal">Searches worth being found for</h2>
        <p class="reveal note">Examples only. Your plan is built on what your own customers search, in English and Bahasa Malaysia.</p>
        <div class="reveal">{chips(i["searches"])}</div>''', alt=True, narrow=True)
        svc = "".join(f'<a class="card reveal" href="{url("services/" + s["slug"] + "/")}"><div class="emoji" aria-hidden="true">{s["emoji"]}</div><h3>{E(s["title"])}</h3><span class="card-link">More details →</span></a>' for s in C.SERVICES)
        body += section(f'''        <p class="kicker reveal">Services</p>
        <h2 class="reveal">What we can do for you</h2>
        <div class="cards three plain-cards" style="margin-top:24px">{svc}</div>''')
        body += cta_band("ind_" + i["slug"].replace("-", "_"), primary=("industry", i["who"]))
        page(f"industries/{i['slug']}/", f"{i['h1']} | {BRAND['name']}", i["meta"], body, current="industries/")


# ------------------------------------------------------------------ company pages
def build_company():
    # About
    body = page_hero([("", "Home"), ("about/", "About")], BRAND["focus_line"], f"About {BRAND['name']}", C.ABOUT_PARAS[0], "about")
    body += section(f'''        <p class="kicker reveal">Who we are</p>
        <h2 class="reveal">{E(BRAND["positioning"])}</h2>
''' + "".join(f'        <p class="reveal">{E(p)}</p>\n' for p in C.ABOUT_PARAS[1:]) + f'''        <p class="reveal goal">{E(C.GOAL)}</p>
        <p class="reveal">{E(BRAND["name"])} is a brand of {E(BRAND["company"])}.</p>''', narrow=True)
    body += section(f'''        <p class="kicker reveal">Why Choose {E(BRAND["name"])}?</p>
        <h2 class="reveal">What makes us different</h2>
{why_cards()}''', alt=True)
    body += f'''    <section class="mission">
      <div class="wrap narrow">
        <p class="kicker reveal">Our Mission</p>
        <p class="mission-text reveal">{E(C.MISSION)}</p>
      </div>
    </section>
'''
    body += section(f'''        <p class="kicker reveal">Industries We Serve</p>
        <h2 class="reveal">Every part of the automotive trade</h2>
{industry_grid()}''', dark=True)
    body += cta_band("about")
    page("about/", f"About {BRAND['name']}: Automotive Digital Marketing in Malaysia",
         f"{BRAND['name']} is an automotive-exclusive SEO, AEO and GEO agency in Malaysia, a brand of {BRAND['company']}.", body, current="about/")

    # How it works
    body = page_hero([("", "Home"), ("how-it-works/", "How it works")], "Four steps, no tech skills needed",
                     "How it works: from free audit to more enquiries",
                     "Start with a WhatsApp message. We check how your business shows up today, agree a plan with you, do the work and keep improving it.", "how")
    cards = "".join(f'<div class="card reveal"><p class="pill">{E(a)}</p><h3>{E(b)}</h3><p>{E(c)}</p>{ticks(d)}</div>' for a, b, c, d in C.STEPS)
    body += section(f'''        <p class="kicker reveal">The steps</p>
        <h2 class="reveal">What happens at each step</h2>
        <div class="cards two plain-cards" style="margin-top:28px">{cards}</div>''')
    body += section(f'''        <p class="kicker reveal">Your part</p>
        <h2 class="reveal">What we need from you</h2>
        <p class="reveal">A short WhatsApp chat about your business: what you do, the areas you serve and the customers you want more of. Real photos of your premises and work help a lot. Before anything that describes your business goes live, you check it for accuracy.</p>
        <p class="reveal">Pricing depends on what your business needs. <a class="link" href="{wa("quote")}" target="_blank" rel="noopener" data-cta="whatsapp_how_quote">WhatsApp for a quote →</a></p>''', alt=True, narrow=True)
    body += cta_band("how")
    page("how-it-works/", f"How It Works: Automotive SEO in Malaysia | {BRAND['name']}",
         "How AutoSEO.my works: a free automotive SEO audit on WhatsApp, a plan for your business, the work on SEO, AEO and GEO, then regular improvements.", body, current="how-it-works/")

    # FAQ
    body = page_hero([("", "Home"), ("faq/", "FAQ")], "Plain answers", "Automotive SEO questions, answered",
                     "What we do, who we work with, what it costs and how to start.", "faq")
    body += faq_block(C.FAQS, "Frequently asked questions", kicker="FAQ")
    body += cta_band("faq")
    page("faq/", f"FAQ: Automotive SEO, AEO & GEO in Malaysia | {BRAND['name']}",
         "Answers about AutoSEO.my: what SEO, AEO and GEO mean, who we work with, areas covered, pricing and the free automotive SEO audit.", body, current="faq/", faqs=C.FAQS)

    # Contact (WhatsApp only)
    body = page_hero([("", "Home"), ("contact/", "Contact")], "WhatsApp is the fastest way to reach us",
                     f"Contact {BRAND['name']}", "Send us a WhatsApp message with your business name, what you do and where you are. We’ll reply on WhatsApp.", "contact")
    opts = [("audit", "", C.BTN_AUDIT, "Ask for a free check of how your business shows up on Google, Maps and AI search."),
            ("specialist", "", C.BTN_SPECIALIST, "Talk through your business and what you want more of."),
            ("quote", "", "WhatsApp for a quote", "Tell us what you need and we’ll suggest what fits.")]
    cards = "".join(f'<a class="card reveal" href="{wa(k, t)}" target="_blank" rel="noopener" data-cta="whatsapp_contact_{k}"><div class="emoji" aria-hidden="true">💬</div><h3>{E(label)}</h3><p>{E(d)}</p><span class="card-link">Open WhatsApp →</span></a>' for k, t, label, d in opts)
    body += section(f'''        <p class="kicker reveal">Pick a message</p>
        <h2 class="reveal">Each button opens WhatsApp with a message ready to send</h2>
        <div class="cards three plain-cards" style="margin-top:24px">{cards}</div>
        <p class="note reveal" style="text-align:center">We work with automotive businesses across Malaysia, including Kuala Lumpur, Selangor, Johor Bahru and Penang.</p>''')
    page("contact/", f"Contact {BRAND['name']} on WhatsApp", "Contact AutoSEO.my on WhatsApp for a free automotive SEO audit or a quote. Serving automotive businesses across Malaysia.", body, current="contact/")

    # Privacy
    body = page_hero([("", "Home"), ("privacy/", "Privacy")], "Short and plain", "Privacy notice", f"How {BRAND['name']} handles information on this website.", "privacy")
    body += section(f'''        <div class="prose">
        <h2>What this website collects</h2>
        <p>This website has no forms and asks for no personal details. It sets no advertising or tracking cookies.</p>
        <h2>WhatsApp messages</h2>
        <p>When you tap a WhatsApp button, WhatsApp opens with a message ready to send. Nothing is sent until you press send. Messages you send reach us through WhatsApp and are handled under WhatsApp’s own terms. We use them only to reply to you and to provide the service you ask about.</p>
        <h2>Fonts</h2>
        <p>Pages load fonts from Google Fonts, so your browser connects to Google’s servers when you view them.</p>
        <h2>Who we are</h2>
        <p>{E(BRAND["name"])} is a brand of {E(BRAND["company"])}. For any privacy question, or to ask us to delete your messages, contact us on WhatsApp.</p>
        </div>''', narrow=True)
    page("privacy/", f"Privacy Notice | {BRAND['name']}", "How the AutoSEO.my website handles information: no forms, no tracking cookies, WhatsApp messages used only to reply.", body)

    # 404
    body = page_hero([("", "Home"), ("", "Page not found")], "404", "Sorry, that page isn’t here",
                     "The link may be old or mistyped. Try the services or industries pages, or ask us on WhatsApp.", "notfound")
    body += section(f'''        <p class="reveal"><a class="link" href="{url()}">Home</a> · <a class="link" href="{url("services/")}">Services</a> · <a class="link" href="{url("industries/")}">Industries</a> · <a class="link" href="{url("faq/")}">FAQ</a></p>''', narrow=True)
    page("404.html", f"Page not found | {BRAND['name']}", "This page could not be found.", body)


# ------------------------------------------------------------------ extras
def build_extras():
    lines = [f"# {BRAND['name']}", "", f"> {BRAND['positioning']}. {BRAND['tagline']}", "",
             C.ABOUT_PARAS[0], "", C.GOAL, "", f"{BRAND['name']} is a brand of {BRAND['company']}. Areas: {', '.join(BRAND['areas'])} and other Malaysian locations.",
             f"Contact: WhatsApp https://wa.me/{BRAND['whatsapp_number']}", "", "## Services"]
    lines += [f"- [{s['title']}]({url('services/' + s['slug'] + '/')}): {s['text']}" for s in C.SERVICES]
    lines += ["", "## Industries"] + [f"- [{i['label']}]({url('industries/' + i['slug'] + '/')})" for i in C.INDUSTRIES] + [f"- {C.OTHER_INDUSTRY}"]
    lines += ["", "## Company", f"- [About]({url('about/')})", f"- [How it works]({url('how-it-works/')})", f"- [FAQ]({url('faq/')})", f"- [Contact]({url('contact/')})", ""]
    (OUT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")
    manifest = {"name": BRAND["name"], "short_name": BRAND["name"], "start_url": BASE, "display": "browser", "background_color": "#060b18", "theme_color": "#060b18",
                "icons": [{"src": BASE + "favicon.svg", "sizes": "any", "type": "image/svg+xml"}]}
    (OUT / "site.webmanifest").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    (OUT / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#ff3d57"/><stop offset=".5" stop-color="#ff8a3d"/><stop offset="1" stop-color="#8b5cf6"/></linearGradient></defs>'
        f'<rect width="64" height="64" rx="16" fill="url(#g)"/><text x="32" y="45" font-family="Arial,Helvetica,sans-serif" font-size="38" font-weight="700" fill="#fff" text-anchor="middle">{BRAND["logo_letter"]}</text></svg>\n',
        encoding="utf-8")
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "site.js").write_text(JS, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    build_home()
    build_services()
    build_industries()
    build_company()
    for path, doc in PAGES:
        f = OUT / (path if path.endswith(".html") else path + "index.html")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(doc, encoding="utf-8")
    build_extras()
    print(f"built {len(PAGES)} pages into {OUT}")
    r = subprocess.run([sys.executable, str(ROOT / "src" / "check.py")])
    if r.returncode:
        print("BUILD STOPPED: pre-upload check failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
