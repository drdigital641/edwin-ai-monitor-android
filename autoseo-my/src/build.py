#!/usr/bin/env python3
"""Build the AutoSEO.my static site in English, Malay and Chinese.

    python3 autoseo-my/src/build.py

One set of templates (templates/) for every language. Text comes from
strings/<lang>.json, brand facts from data/brand.json, page order, slugs and
icons from data/site.json. Output is fully rendered HTML in site/ (English at
the root, Malay in ms/, Chinese in zh/). check.py runs at the end; a failed
check stops the build with exit code 1.
"""
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
BRAND = json.loads((ROOT / "data" / "brand.json").read_text(encoding="utf-8"))
SITE = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
LANGS = SITE["languages"]
STR = {l["code"]: json.loads((ROOT / "strings" / f"{l['code']}.json").read_text(encoding="utf-8")) for l in LANGS}
TPL = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / "templates").glob("*.html")}
OUT = ROOT / "site"
BASE = BRAND["base_path"]
E = html.escape

CSS = (ROOT / "assets" / "base.css").read_text(encoding="utf-8") + "\n" + (ROOT / "assets" / "brand.css").read_text(encoding="utf-8")
JS = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
ASSET_V = hashlib.sha256((CSS + JS).encode()).hexdigest()[:10]
CHECK_JS = (ROOT / "assets" / "check.js").read_text(encoding="utf-8")
CHECK_V = hashlib.sha256(CHECK_JS.encode()).hexdigest()[:10]
CHECK_CSS = re.sub(r"/\*.*?\*/\s*", "", (ROOT / "assets" / "check.css").read_text(encoding="utf-8"), flags=re.S).strip()


def fill(tpl, **kw):
    out = TPL[tpl]
    for k, v in kw.items():
        out = out.replace("{{" + k + "}}", str(v))
    if "{{" in out:
        raise SystemExit(f"template {tpl}: unfilled placeholder near {out[out.find('{{'):out.find('{{') + 40]!r}")
    return out


class Lang:
    """Everything one language needs: its strings, URL prefix and helpers."""

    def __init__(self, cfg):
        self.code = cfg["code"]
        self.prefix = cfg["prefix"]
        self.s = STR[self.code]
        self.ui = self.s["ui"]

    def url(self, path=""):
        return BASE + self.prefix + path

    def wa(self, key="general", topic=""):
        msg = self.s["prefills"][key].replace("{topic}", topic)
        return E(f"https://wa.me/{BRAND['whatsapp_number']}?text={quote(msg, safe='')}")


def page_url(lang_prefix, path):
    """Root-relative while previewing, absolute once brand.site_url is set."""
    p = BASE + lang_prefix + path
    if BRAND["site_url"]:
        return BRAND["site_url"].rstrip("/") + "/" + (lang_prefix + path)
    return p


# ------------------------------------------------------------------ schema
def org_graph(L):
    s = L.s
    org = {
        "@type": "Organization", "@id": "#organization", "name": BRAND["name"], "slogan": tagline(L),
        "description": s["brand"]["org_description"],
        "parentOrganization": {"@type": "Organization", "name": BRAND["company"]},
        "areaServed": [{"@type": "Country", "name": BRAND["country"]}] + [{"@type": "Place", "name": a} for a in s["brand"]["areas"]],
        "knowsAbout": s["brand"]["knows_about"],
        "contactPoint": {"@type": "ContactPoint", "contactType": "customer service", "url": f"https://wa.me/{BRAND['whatsapp_number']}", "areaServed": "MY",
                         "availableLanguage": [STR[l["code"]]["meta"]["lang_name"] for l in LANGS]},
    }
    site = {"@type": "WebSite", "@id": "#website", "name": BRAND["name"], "inLanguage": s["meta"]["schema_lang"], "publisher": {"@id": "#organization"}}
    # Schema @id values stay page-relative, as on the live site (11 Nov 2026).
    return [org, site]


def faq_schema(L, faqs):
    return {"@type": "FAQPage", "inLanguage": L.s["meta"]["schema_lang"],
            "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]}


def schema_tag(graph):
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    return f'  <script type="application/ld+json">\n{data}\n  </script>'


# ------------------------------------------------------------------ blocks
def faq_block(L, faqs, heading, kicker=None, alt=False, after=""):
    items = "\n".join(f'          <details class="reveal"><summary>{E(f["q"])}</summary><p>{E(f["a"])}</p></details>' for f in faqs)
    return fill("faq_block", alt=" alt" if alt else "", kicker=E(kicker or L.ui["faq_kicker"]), heading=E(heading), items=items, after=after)


def cta_band(L, cta_id, primary=("audit", "")):
    h = L.s["home"]
    return fill("cta_band", heading=E(h["hero_h1"]), text=E(" ".join(h["hero_lines"])), cta_id=cta_id, wa_primary=L.wa(*primary),
                btn_primary=E(L.s["btn_audit"]), wa_secondary=L.wa("specialist"), btn_secondary=E(L.s["btn_specialist"]))


def page_hero(L, crumbs, eyebrow, h1, lead, cta_id, primary=("audit", "")):
    crumb_html = " / ".join([f'<a href="{L.url(p)}">{E(t)}</a>' for p, t in crumbs[:-1]] + [E(crumbs[-1][1])])
    return fill("page_hero", crumbs=crumb_html, eyebrow=E(eyebrow), h1=E(h1), lead=E(lead), cta_id=cta_id,
                wa_primary=L.wa(*primary), btn_primary=E(L.s["btn_audit"]), wa_secondary=L.wa("specialist"), btn_secondary=E(L.s["btn_specialist"]))


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"


def chips(L, items):
    return f'<ul class="search-chips" aria-label="{E(L.ui["example_searches_aria"])}">' + "".join(f"<li>“{E(i)}”</li>" for i in items) + "</ul>"


def section(inner, alt=False, dark=False, narrow=False):
    cls = "section" + (" alt" if alt else "") + (" dark" if dark else "")
    return f'    <section class="{cls}">\n      <div class="wrap{" narrow" if narrow else ""}">\n{inner}\n      </div>\n    </section>\n'


def kicker_h2(k, h):
    return f'        <p class="kicker reveal">{E(k)}</p>\n        <h2 class="reveal">{E(h)}</h2>\n'


def service_cards(L, full=True):
    cards = []
    for meta in SITE["services"]:
        s = L.s["services"][meta["slug"]]
        text = f'<p class="pill">{meta["n"]:02d}</p><h3>{E(s["title"])}</h3><p>{E(s["text"])}</p>' if full else f'<h3>{E(s["title"])}</h3>'
        cards.append(f'          <a class="card reveal" href="{L.url("services/" + meta["slug"] + "/")}"><div class="emoji" aria-hidden="true">{meta["emoji"]}</div>{text}<span class="card-link">{E(L.ui["more_details"])}</span></a>')
    return cards


def cards_wrap(cards, cols="three", mt=28):
    return f'        <div class="cards {cols} plain-cards" style="margin-top:{mt}px">\n' + "\n".join(cards) + "\n        </div>"


def industry_grid(L):
    cells = [f'          <a class="ind reveal" href="{L.url("industries/" + m["slug"] + "/")}"><span aria-hidden="true">{m["emoji"]}</span>{E(L.s["industries"][m["slug"]]["label"])}</a>' for m in SITE["industries"]]
    cells.append(f'          <a class="ind reveal" href="{L.wa("general")}" target="_blank" rel="noopener" data-cta="whatsapp_other_industry"><span aria-hidden="true">➕</span>{E(L.s["other_industry"])}</a>')
    return '        <div class="ind-grid">\n' + "\n".join(cells) + "\n        </div>"


def why_cards(L):
    cards = [f'          <div class="card reveal"><div class="emoji" aria-hidden="true">{em}</div><h3>{E(w["title"])}</h3><p>{E(w["text"])}</p></div>' for w, em in zip(L.s["why"], SITE["why_emoji"])]
    return cards_wrap(cards, "two")


def mission(L):
    return f'''    <section class="mission">
      <div class="wrap narrow">
        <p class="kicker reveal">{E(L.s["home"]["mission_kicker"])}</p>
        <p class="mission-text reveal">{E(L.s["mission"])}</p>
      </div>
    </section>
'''


def tagline(L):
    """The tagline in the page's own language: English on EN pages, the BM / 中文 tagline on /ms/ and /zh/ (Edwin, 11 Nov 2026)."""
    return L.s["brand"]["tagline_translation"] or BRAND["tagline"]


# ------------------------------------------------------------------ page shell
PAGES = []


def page(L, path, title, description, body, current="", faqs=None, body_class="", head_extra=""):
    graph = org_graph(L)
    if faqs:
        graph.append(faq_schema(L, faqs))
    noindex = BRAND["preview"] or path == "404.html"
    robots = '  <meta name="robots" content="noindex,nofollow">\n' if noindex else '  <meta name="robots" content="index,follow">\n'
    canonical = f'  <link rel="canonical" href="{page_url(L.prefix, path)}">\n'
    alts = "".join(f'  <link rel="alternate" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" href="{page_url(l["prefix"], path)}">\n' for l in LANGS)
    alts += f'  <link rel="alternate" hreflang="x-default" href="{page_url("", path)}">\n'
    alts += "".join(f'  <meta property="og:locale:alternate" content="{STR[l["code"]]["meta"]["og_locale"]}">\n' for l in LANGS if l["code"] != L.code)
    og_url = f'  <meta property="og:url" content="{page_url(L.prefix, path)}">\n'
    ui = L.ui
    lang_links = '<span class="sep" aria-hidden="true">|</span>'.join(
        f'<a href="{BASE + l["prefix"] + path.replace("404.html", "")}" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" lang="{STR[l["code"]]["meta"]["html_lang"]}"'
        + (' aria-current="true"' if l["code"] == L.code else "") + f'>{E(STR[l["code"]]["meta"]["switch_label"])}</a>' for l in LANGS)
    nav = "\n".join(f'        <a href="{L.url(p)}"' + (' aria-current="page"' if current == p else "") + f'>{E(ui["nav"][k])}</a>'
                    for p, k in [("services/", "services"), ("industries/", "industries"), ("how-it-works/", "how"), ("about/", "about"), ("faq/", "faq"), ("contact/", "contact")])
    shared = dict(base=BASE, home_url=L.url(), brand_name_html=BRAND["name_html"], logo_letter=BRAND["logo_letter"], wa_general=L.wa("general"), wa_icon=TPL["wa_icon"].strip(), whatsapp_label=E(L.s["brand"]["whatsapp_label"]))
    doc = fill("head", lang=L.s["meta"]["html_lang"], title=E(title), description=E(description), robots=robots, canonical=canonical, hreflang=alts,
               og_url=og_url, og_locale=L.s["meta"]["og_locale"], asset_v=ASSET_V, schema=schema_tag(graph), base=BASE, brand_name=E(BRAND["name"]),
               font_extra="&family=Noto+Sans+SC:wght@400;600;700" if L.code == "zh" else "")
    if head_extra:
        doc = doc.replace("</head>", head_extra + "</head>", 1)
    doc += fill("header", body_class=(body_class + " lang-" + L.code).strip(), nav_links=nav, skip=E(ui["skip"]), home_aria=E(ui["home_aria"]),
                nav_aria=E(ui["nav_aria"]), lang_aria=E(ui["lang_switch_aria"]), lang_links=lang_links,
                whatsapp_us=E(ui["whatsapp_us"]), menu=E(ui["menu"]), **shared)
    doc += body
    company = [("about/", ui["nav"]["about"]), ("how-it-works/", ui["nav"]["how"]), ("faq/", ui["nav"]["faq"]), ("contact/", ui["nav"]["contact"]), ("privacy/", ui["privacy"])]
    doc += fill("footer", tagline=E(tagline(L)), year=date.today().year,
                brand_line=E(L.s["brand"]["brand_line"]), areas_line=E(L.s["brand"]["areas_line"]),
                h_services=E(ui["footer_services"]), h_industries=E(ui["footer_industries"]), h_company=E(ui["footer_company"]),
                footer_services="\n".join(f'        <a href="{L.url("services/" + m["slug"] + "/")}">{E(L.s["services"][m["slug"]]["short"])}</a>' for m in SITE["services"]),
                footer_industries="\n".join(f'        <a href="{L.url("industries/" + m["slug"] + "/")}">{E(L.s["industries"][m["slug"]]["short"])}</a>' for m in SITE["industries"]),
                footer_company="\n".join(f'        <a href="{L.url(p)}">{E(t)}</a>' for p, t in company), **shared)
    PAGES.append((L.prefix + path, doc))


# ------------------------------------------------------------------ home
def hero_check(L):
    """Free website check box: one shared template for every language (templates/hero_check.html)."""
    c = L.s["check"]
    data = {"wa": BRAND["whatsapp_number"], "prefills": {k: L.s["prefills"][k] for k in ("check", "check_failed")},
            "c": {k: v for k, v in c.items() if not k.startswith("_")}}
    js = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return fill("hero_check", endpoint=E(BRAND["check_endpoint"]), lang=L.code, kicker=E(c["kicker"]), label=E(c["label"]),
                placeholder=E(c["placeholder"]), button=E(c["button"]), note=E(c["note"]), strings_json=js)


def build_home(L):
    s, h, ui = L.s, L.s["home"], L.ui
    items = [s["industries"][m["slug"]]["label"] for m in SITE["industries"]] + [s["other_industry"]]
    marquee_items = "".join(f'<span><span class="dot"></span>{E(i)}</span>' for i in items)
    chan_html = "".join(f"<li><span>{E(c)}</span><b>{E(t)}</b></li>" for c, t in h["channels"])
    body = f'''    <section class="hero hero-lean">
      <span class="glow glow-1" aria-hidden="true"></span>
      <span class="glow glow-2" aria-hidden="true"></span>
      <div class="wrap hero-grid">
        <div>
          <p class="eyebrow"><span class="live" aria-hidden="true"></span>{E(h["hero_lines"][0])}</p>
          <h1>{E(h["hero_h1"])}</h1>
          <p class="hero-tagline grad-text">{E(tagline(L))}</p>
          <p class="lead">{E(s["brand"]["positioning"])}{E(s["meta"]["full_stop"])}{E(h["hero_lines"][1])}</p>
{hero_check(L)}          <div class="cta-row hero-ctas">
            <a class="btn" href="{L.wa("audit")}" target="_blank" rel="noopener" data-cta="whatsapp_home_audit">{E(s["btn_audit"])}</a>
            <a class="btn btn-ghost" href="{L.wa("specialist")}" target="_blank" rel="noopener" data-cta="whatsapp_home_specialist">{E(s["btn_specialist"])}</a>
          </div>
          <p class="hero-paths">{E(s["brand"]["focus_line"])}</p>
        </div>
        <figure class="proof-card search-card" aria-label="{E(h["card_aria"])}">
          <span class="chip chip-1">{E(h["card_chip_1"])}</span>
          <div class="proof-top"><span class="proof-src">{E(h["card_head"])}</span><span class="proof-real">SEO · AEO · GEO</span></div>
          <p class="search-bar"><span aria-hidden="true">🔍</span> {E(h["card_query"])}</p>
          <ul class="proof-ranks channel-list">{chan_html}</ul>
          <figcaption>{E(h["card_caption"])}</figcaption>
          <span class="chip chip-2">{E(h["card_chip_2"])}</span>
        </figure>
      </div>
    </section>

    <div class="marquee" aria-label="{E(h["marquee_aria"])}">
      <p class="marquee-label">{E(h["marquee_label"])} · <a href="{L.url("industries/")}">{E(h["marquee_link"])}</a></p>
      <div class="marquee-track" aria-hidden="true">{marquee_items}{marquee_items}</div>
    </div>
'''
    about = kicker_h2(h["about_kicker"], s["brand"]["positioning"]) + f'        <p class="section-lead reveal"><strong>{E(s["brand"]["focus_line"])}</strong></p>\n'
    about += "".join(f'        <p class="reveal">{E(p)}</p>\n' for p in s["about_paras"])
    about += f'        <p class="reveal goal">{E(s["goal"])}</p>\n        <p class="reveal"><a class="link" href="{L.url("about/")}">{E(ui["more_about_us"])}</a></p>'
    body += section(about, narrow=True)
    body += section(kicker_h2(h["services_kicker"], h["services_h2"]) + f'        <p class="section-lead reveal">{E(h["services_lead"])} <a class="link" href="{L.url("services/")}">{E(ui["see_all_services"])}</a></p>\n' + cards_wrap(service_cards(L)), alt=True)
    body += section(kicker_h2(h["ind_kicker"], h["ind_h2"]) + f'        <p class="section-lead reveal">{E(h["ind_lead"])}</p>\n' + industry_grid(L), dark=True)
    body += section(kicker_h2(h["why_kicker"], h["why_h2"]) + why_cards(L))
    steps = [f'          <div class="card reveal"><p class="pill">{E(st["pill"])}</p><h3>{E(st["title"])}</h3><p>{E(st["text"])}</p></div>' for st in s["steps"]]
    body += section(kicker_h2(h["how_kicker"], h["how_h2"]) + cards_wrap(steps, "four") + f'\n        <p class="note reveal" style="text-align:center"><a class="link" href="{L.url("how-it-works/")}">{E(ui["how_detail_link"])}</a></p>', alt=True)
    body += mission(L)
    home_faqs = s["faqs"][:SITE["home_faq_count"]]
    body += faq_block(L, home_faqs, h["faq_h2"], after=f'        <p class="note reveal" style="text-align:center">{E(ui["full_faq_before"])} <a class="link" href="{L.url("faq/")}">{E(ui["full_faq_link"])}</a>.</p>')
    body += cta_band(L, "home")
    page(L, "", h["title"], h["description"], body, faqs=home_faqs, body_class="home",
         head_extra=f'  <style>\n{CHECK_CSS}\n  </style>\n  <script src="{BASE}assets/check.js?v={CHECK_V}" defer></script>\n')


# ------------------------------------------------------------------ services
def build_services(L):
    s, ui, sp = L.s, L.ui, L.s["services_page"]
    body = page_hero(L, [("", ui["home"]), ("services/", ui["nav"]["services"])], sp["eyebrow"], sp["h1"], sp["lead"], "services")
    body += section(kicker_h2(sp["list_kicker"], sp["list_h2"]) + cards_wrap(service_cards(L)))
    body += section(kicker_h2(sp["fit_kicker"], sp["fit_h2"]) + f'''        <p class="reveal">{E(sp["fit_text"])}</p>
        <p class="reveal">{E(ui["quote_line"])} <a class="link" href="{L.wa("quote")}" target="_blank" rel="noopener" data-cta="whatsapp_services_quote">{E(ui["quote_link"])}</a></p>''', alt=True, narrow=True)
    body += cta_band(L, "services")
    page(L, "services/", sp["title"], sp["description"], body, current="services/")

    for meta in SITE["services"]:
        sv = s["services"][meta["slug"]]
        cid = "svc_" + meta["slug"].replace("-", "_")
        prim = ("service", sv["prefill_topic"])
        body = page_hero(L, [("", ui["home"]), ("services/", ui["nav"]["services"]), ("", sv["short"])], ui["service_of"].replace("{n}", f'{meta["n"]:02d}'),
                         sv["h1"], sv["text"], cid, primary=prim)
        body += section(kicker_h2(sp["why_kicker"], sv["title"]) + f'        <p class="reveal">{E(sv["why"])}</p>', narrow=True)
        body += section(kicker_h2(sp["covers_kicker"], sp["covers_h2"]) + f'''        <div class="reveal">{ticks(sv["covers"])}</div>
        <h3 class="reveal" style="margin-top:28px">{E(sp["searches_h3"])}</h3>
        <p class="reveal note">{E(ui["examples_only"])}</p>
        <div class="reveal">{chips(L, sv["searches"])}</div>''', alt=True, narrow=True)
        body += faq_block(L, sv["faqs"], sp["faq_h2"].replace("{name}", sv["short"]))
        others = [m for m in SITE["services"] if m["slug"] != meta["slug"]][:3]
        rel = [c for m, c in zip(SITE["services"], service_cards(L, full=False)) if m in others]
        body += section(kicker_h2(sp["related_kicker"], sp["related_h2"]) + cards_wrap(rel, mt=24), alt=True)
        body += cta_band(L, cid, primary=prim)
        page(L, f"services/{meta['slug']}/", sv["h1"] + sp["title_suffix"], sv["meta"], body, current="services/", faqs=sv["faqs"])


# ------------------------------------------------------------------ industries
def build_industries(L):
    s, ui, ip = L.s, L.ui, L.s["industries_page"]
    body = page_hero(L, [("", ui["home"]), ("industries/", ui["nav"]["industries"])], ip["eyebrow"], ip["h1"], ip["lead"], "industries")
    body += section(kicker_h2(ip["grid_kicker"], ip["grid_h2"]) + industry_grid(L), dark=True)
    body += section(kicker_h2(ip["same_kicker"], ip["same_h2"]) + f'        <p class="reveal">{E(ip["same_text"])}</p>', narrow=True)
    body += cta_band(L, "industries")
    page(L, "industries/", ip["title"], ip["description"], body, current="industries/")

    for meta in SITE["industries"]:
        it = s["industries"][meta["slug"]]
        cid = "ind_" + meta["slug"].replace("-", "_")
        prim = ("industry", it["who"])
        body = page_hero(L, [("", ui["home"]), ("industries/", ui["nav"]["industries"]), ("", it["label"])], ip["h1"], it["h1"], it["intro"], cid, primary=prim)
        body += section(kicker_h2(ip["focus_kicker"], ip["focus_h2"].replace("{label}", it["focus_label"])) + f'        <div class="reveal">{ticks(it["focus"])}</div>', narrow=True)
        body += section(kicker_h2(ip["search_kicker"], ip["search_h2"]) + f'''        <p class="reveal note">{E(ui["examples_only_bilingual"])}</p>
        <div class="reveal">{chips(L, it["searches"])}</div>''', alt=True, narrow=True)
        body += section(kicker_h2(ip["svc_kicker"], ip["svc_h2"]) + cards_wrap(service_cards(L, full=False), mt=24))
        body += cta_band(L, cid, primary=prim)
        page(L, f"industries/{meta['slug']}/", it["h1"] + s["services_page"]["title_suffix"], it["meta"], body, current="industries/")


# ------------------------------------------------------------------ company pages
def build_company(L):
    s, ui = L.s, L.ui
    ap = s["about_page"]
    body = page_hero(L, [("", ui["home"]), ("about/", ui["nav"]["about"])], s["brand"]["focus_line"], ap["h1"], s["about_paras"][0], "about")
    body += section(kicker_h2(ap["who_kicker"], s["brand"]["positioning"]) + "".join(f'        <p class="reveal">{E(p)}</p>\n' for p in s["about_paras"][1:])
                    + f'        <p class="reveal goal">{E(s["goal"])}</p>\n        <p class="reveal">{E(s["brand"]["is_brand_of"])}</p>', narrow=True)
    body += section(kicker_h2(s["home"]["why_kicker"], ap["why_h2"]) + why_cards(L), alt=True)
    body += mission(L)
    body += section(kicker_h2(s["home"]["ind_kicker"], ap["ind_h2"]) + industry_grid(L), dark=True)
    body += cta_band(L, "about")
    page(L, "about/", ap["title"], ap["description"], body, current="about/")

    hp = s["how_page"]
    body = page_hero(L, [("", ui["home"]), ("how-it-works/", ui["nav"]["how"])], hp["eyebrow"], hp["h1"], hp["lead"], "how")
    cards = [f'<div class="card reveal"><p class="pill">{E(st["pill"])}</p><h3>{E(st["title"])}</h3><p>{E(st["text"])}</p>{ticks(st["items"])}</div>' for st in s["steps"]]
    body += section(kicker_h2(hp["steps_kicker"], hp["steps_h2"]) + cards_wrap(cards, "two"))
    body += section(kicker_h2(hp["you_kicker"], hp["you_h2"]) + f'''        <p class="reveal">{E(hp["you_text"])}</p>
        <p class="reveal">{E(ui["quote_line"])} <a class="link" href="{L.wa("quote")}" target="_blank" rel="noopener" data-cta="whatsapp_how_quote">{E(ui["quote_link"])}</a></p>''', alt=True, narrow=True)
    body += cta_band(L, "how")
    page(L, "how-it-works/", hp["title"], hp["description"], body, current="how-it-works/")

    fp = s["faq_page"]
    body = page_hero(L, [("", ui["home"]), ("faq/", ui["nav"]["faq"])], fp["eyebrow"], fp["h1"], fp["lead"], "faq")
    body += faq_block(L, s["faqs"], fp["h2"], kicker=fp["kicker"])
    body += cta_band(L, "faq")
    page(L, "faq/", fp["title"], fp["description"], body, current="faq/", faqs=s["faqs"])

    cp = s["contact_page"]
    body = page_hero(L, [("", ui["home"]), ("contact/", ui["nav"]["contact"])], cp["eyebrow"], cp["h1"], cp["lead"], "contact")
    opts = [("audit", s["btn_audit"], cp["audit_text"]), ("specialist", s["btn_specialist"], cp["specialist_text"]), ("quote", ui["quote_button"], cp["quote_text"])]
    cards = [f'<a class="card reveal" href="{L.wa(k)}" target="_blank" rel="noopener" data-cta="whatsapp_contact_{k}"><div class="emoji" aria-hidden="true">💬</div><h3>{E(label)}</h3><p>{E(d)}</p><span class="card-link">{E(ui["open_whatsapp"])}</span></a>' for k, label, d in opts]
    body += section(kicker_h2(cp["kicker"], cp["h2"]) + cards_wrap(cards, mt=24) + f'\n        <p class="note reveal" style="text-align:center">{E(cp["areas_note"])}</p>')
    page(L, "contact/", cp["title"], cp["description"], body, current="contact/")

    pp = s["privacy_page"]
    body = page_hero(L, [("", ui["home"]), ("privacy/", ui["privacy"])], pp["eyebrow"], pp["h1"], pp["lead"], "privacy")
    body += section('        <div class="prose">\n' + "".join(f"        <h2>{E(a)}</h2>\n        <p>{E(b)}</p>\n" for a, b in pp["sections"]) + "        </div>", narrow=True)
    page(L, "privacy/", pp["title"], pp["description"], body)

    np = s["notfound_page"]
    body = page_hero(L, [("", ui["home"]), ("", ui["page_not_found"])], np["eyebrow"], np["h1"], np["lead"], "notfound")
    body += section(f'        <p class="reveal"><a class="link" href="{L.url()}">{E(ui["home"])}</a> · <a class="link" href="{L.url("services/")}">{E(ui["nav"]["services"])}</a> · <a class="link" href="{L.url("industries/")}">{E(ui["nav"]["industries"])}</a> · <a class="link" href="{L.url("faq/")}">{E(ui["nav"]["faq"])}</a></p>', narrow=True)
    page(L, "404.html", np["title"], np["description"], body)


# ------------------------------------------------------------------ extras
def abs_url(path):
    """Absolute link once the site is live on its own domain (llms.txt, sitemap)."""
    return BRAND["site_url"].rstrip("/") + path if BRAND["site_url"] else path


def build_llms():
    out = [f"# {BRAND['name']}", ""]
    for cfg in LANGS:
        L = Lang(cfg)
        s, t = L.s, L.s["llms"]
        out += [f"## {s['meta']['lang_name']}", "", f"> {s['brand']['positioning']}{s['meta']['full_stop']}{BRAND['tagline']}", "", s["about_paras"][0], "", s["goal"], "",
                f"{s['brand']['is_brand_of']} {t['areas']}: {', '.join(s['brand']['areas'])}, {t['and_other']}.", f"{t['contact']}: WhatsApp https://wa.me/{BRAND['whatsapp_number']}", "",
                f"### {t['services']}"]
        out += [f"- [{s['services'][m['slug']]['title']}]({abs_url(L.url('services/' + m['slug'] + '/'))}): {s['services'][m['slug']]['text']}" for m in SITE["services"]]
        out += ["", f"### {t['industries']}"] + [f"- [{s['industries'][m['slug']]['label']}]({abs_url(L.url('industries/' + m['slug'] + '/'))})" for m in SITE["industries"]] + [f"- {s['other_industry']}"]
        out += ["", f"### {t['company']}"] + [f"- [{L.ui['nav'][k]}]({abs_url(L.url(p))})" for p, k in [("about/", "about"), ("how-it-works/", "how"), ("faq/", "faq"), ("contact/", "contact")]] + [""]
    (OUT / "llms.txt").write_text("\n".join(out), encoding="utf-8")


def build_sitemap():
    """Live only: robots.txt and sitemap.xml (every page except 404, with hreflang twins)."""
    if BRAND["preview"] or not BRAND["site_url"]:
        return
    root = BRAND["site_url"].rstrip("/")
    (OUT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {root}/sitemap.xml\n", encoding="utf-8")
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"', '        xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for cfg in LANGS:
        paths = sorted(p for p, _ in PAGES if p.startswith(cfg["prefix"]) and p[len(cfg["prefix"]):].split("/")[0] not in ("ms", "zh") and not p.endswith("404.html"))
        for p in sorted(paths, key=lambda x: x + "index.html"):
            rest = p[len(cfg["prefix"]):]
            out += ["  <url>", f"    <loc>{page_url(cfg['prefix'], rest)}</loc>"]
            out += [f'    <xhtml:link rel="alternate" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" href="{page_url(l["prefix"], rest)}"/>' for l in LANGS]
            out += [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("", rest)}"/>', "  </url>"]
    out.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(out) + "\n", encoding="utf-8")


def build_extras():
    build_llms()
    build_sitemap()
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
    (OUT / "assets" / "check.js").write_text(CHECK_JS, encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for cfg in LANGS:
        L = Lang(cfg)
        build_home(L)
        build_services(L)
        build_industries(L)
        build_company(L)
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
