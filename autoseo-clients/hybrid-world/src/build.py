#!/usr/bin/env python3
"""Build the Hybrid World Specialist site in English, Malay and Chinese.

    python3 autoseo-clients/hybrid-world/src/build.py

Business facts: config.json. Page order, photos, reels, review quotes: data/site.json.
Every visible string and the WhatsApp prefills: strings/<lang>.json (same keys).
Shared parts (head, header, footer, WhatsApp/call buttons, floating buttons, filmstrip,
story, quote, map facade, FAQ, CTA, breadcrumb): templates/. Fonts: fonts/ (self-hosted, OFL).
Output is fully rendered static HTML in site/ (English at the root, Malay in ms/,
Chinese in zh/). check.py runs at the end; a failed check stops the build.
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

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import live_mode  # noqa: E402
ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
OUT = live_mode.apply(CFG, ROOT)
SITE = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
LANGS = SITE["languages"]
STR = {l["code"]: json.loads((ROOT / "strings" / f"{l['code']}.json").read_text(encoding="utf-8")) for l in LANGS}
TPL = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / "templates").glob("*.html")}
BASE = CFG["base_path"]
E = html.escape
CSS = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
JS = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
ASSET_V = hashlib.sha256((CSS + JS).encode()).hexdigest()[:10]
PHOTO = {p["key"]: p for p in SITE["photos"]}
SVC = {s["key"]: s for s in SITE["services"]}
SIZES = {}
PAGES = []  # (path, html)
YEAR = date.today().year
WA_NUM = CFG["whatsapp_number"]


def fill(tpl, **kw):
    out = TPL[tpl]
    for k, v in kw.items():
        out = out.replace("{{" + k + "}}", str(v))
    if "{{" in out:
        raise SystemExit(f"template {tpl}: unfilled placeholder near {out[out.find('{{'):out.find('{{') + 40]!r}")
    return out


def abs_url(prefix, path=""):
    return CFG["site_url"] + prefix + path


def live_url(prefix, path=""):
    return CFG["live_site_url"] + prefix + path


class Lang:
    def __init__(self, cfg):
        self.code, self.prefix = cfg["code"], cfg["prefix"]
        self.s = STR[self.code]
        self.ui = self.s["ui"]

    def url(self, path=""):
        return BASE + self.prefix + path


# Face-to-face diagnosis (client update 12 Nov 2026): home + service heroes show ui.diag_note and use prefills.diagnosis.
# ------------------------------------------------------------------ calls to action (data-cta names match the other AutoSEO previews)
def wa_href(L, key="general", topic=""):
    msg = L.s["prefills"][key].replace("{topic}", topic)
    return f"https://wa.me/{WA_NUM}?text={quote(msg, safe='')}"


def wa(L, place, key="general", topic="", short=False, cls=""):
    return fill("wa_button", cls=cls, href=E(wa_href(L, key, topic)), place=place,
                label=E(L.ui["wa_cta_short" if short else "wa_cta"]))


def tel(L, place, short=False, cls=""):
    label = L.ui["call_short"] if short else L.ui["call"].replace("{phone}", CFG["phone_display"])
    return fill("tel_button", cls=cls, phone_e164=CFG["phone_e164"], place=place, label=E(label))


# ------------------------------------------------------------------ images
def build_images():
    dst = OUT / "img"
    dst.mkdir(parents=True, exist_ok=True)
    for key, p in PHOTO.items():
        im = Image.open(ROOT / "photos" / p["file"]).convert("RGB")
        stem = p["file"][:-5]
        big = im.copy()
        big.thumbnail((1200, 1200), Image.LANCZOS)
        big.save(dst / f"{stem}-1200.webp", "WEBP", quality=78)
        small = im.copy()
        small.thumbnail((640, 640), Image.LANCZOS)
        small.save(dst / f"{stem}-640.webp", "WEBP", quality=74)
        SIZES[key] = (big.size, small.size)
    # og image: 1200x630 crop of the battery room photo
    og = Image.open(ROOT / "photos" / PHOTO[SITE["og_photo"]]["file"]).convert("RGB")
    w, h = og.size
    ch = int(w * 630 / 1200)
    og = og.crop((0, (h - ch) // 2, w, (h - ch) // 2 + ch)).resize((1200, 630), Image.LANCZOS)
    og.save(dst / "og-1200x630.jpg", "JPEG", quality=80, optimize=True)
    # logo (client's own round logo) for header, favicon and touch icon
    logo = Image.open(ROOT / "photos" / (SITE["logo"] + ".webp")).convert("RGB")
    for size, name in ((96, "img/logo-96.webp"), (192, "favicon.png"), (180, "apple-touch-icon.png"), (512, "img/logo-512.png")):
        im = logo.resize((size, size), Image.LANCZOS)
        im.save(OUT / name, "WEBP" if name.endswith("webp") else "PNG", **({"quality": 86} if name.endswith("webp") else {}))


def img_tag(L, key, sizes, eager=False, cls="", alt=True):
    (bw, bh), (sw, sh) = SIZES[key]
    stem = PHOTO[key]["file"][:-5]
    srcset = f"{BASE}img/{stem}-640.webp {sw}w" + (f", {BASE}img/{stem}-1200.webp {bw}w" if bw > sw else "")
    extra = ' fetchpriority="high"' if eager else ""
    c = f' class="{cls}"' if cls else ""
    a = E(L.s["photos"][key]) if alt else ""
    return (f'<img{c} src="{BASE}img/{stem}-640.webp" srcset="{srcset}" sizes="{sizes}" width="{sw}" height="{sh}" '
            f'alt="{a}" loading="{"eager" if eager else "lazy"}" decoding="async"{extra}>')


def figure(L, key, sizes="(max-width: 760px) 100vw, 560px", eager=False, cls=""):
    return f'<figure class="hw-pic{(" " + cls) if cls else ""}">{img_tag(L, key, sizes, eager)}<figcaption>{E(L.s["photo_caps"][key])}</figcaption></figure>'


# ------------------------------------------------------------------ graphics (no fake photos: line icons in the site style)
ICON = {
    "battery": '<rect x="18" y="26" width="64" height="44" rx="7" class="hw-i-l"/><rect x="82" y="40" width="7" height="16" rx="2" class="hw-i-f"/><rect x="26" y="34" width="10" height="28" rx="2" class="hw-i-c"/><rect x="40" y="34" width="10" height="28" rx="2" class="hw-i-c"/><rect x="54" y="34" width="10" height="28" rx="2" class="hw-i-c"/><rect x="68" y="34" width="8" height="28" rx="2" class="hw-i-c hw-i-dim"/>',
    "recon": '<path d="M50 14a34 34 0 1 1-30 18" class="hw-i-l"/><path d="M14 18l6 14 14-5" class="hw-i-l"/><path d="M54 30 42 52h12l-6 18 16-26H52l6-14Z" class="hw-i-f"/>',
    "inverter": '<rect x="20" y="22" width="60" height="52" rx="8" class="hw-i-l"/><path d="M30 48c5-12 10-12 15 0s10 12 15 0" class="hw-i-l"/><path d="M8 40h12M8 56h12M80 40h12M80 56h12" class="hw-i-l"/><path d="M62 30h10M67 25v10" class="hw-i-l"/>',
    "car": '<path d="M16 62V50l9-16c2-4 5-6 9-6h32c4 0 7 2 9 6l9 16v12" class="hw-i-l"/><path d="M12 62h76" class="hw-i-l"/><circle cx="30" cy="66" r="8" class="hw-i-l"/><circle cx="70" cy="66" r="8" class="hw-i-l"/><path d="M53 30 44 46h9l-5 12 12-18h-9l4-10Z" class="hw-i-f"/>',
    "honda": '<circle cx="50" cy="48" r="32" class="hw-i-l"/><path d="M50 16v8M50 72v8M18 48h8M74 48h8" class="hw-i-l"/><path d="M53 28 40 52h11l-5 16 15-24H50l6-16Z" class="hw-i-f"/>',
    "aircon": '<path d="M50 14v68M21 31l58 34M21 65l58-34" class="hw-i-l"/><path d="M42 20l8 8 8-8M42 76l8-8 8 8M17 41l11-3-3-11M83 55l-11 3 3 11M17 55l11 3-3 11M83 41l-11-3 3-11" class="hw-i-l"/><circle cx="50" cy="48" r="7" class="hw-i-f"/>',
    "transmission": '<circle cx="38" cy="50" r="18" class="hw-i-l"/><circle cx="38" cy="50" r="6" class="hw-i-f"/><circle cx="68" cy="30" r="12" class="hw-i-l"/><circle cx="68" cy="30" r="4" class="hw-i-f"/>'
                    + "".join(f'<path d="M{38 + 18 * c:.1f} {50 + 18 * s:.1f}l{5 * c:.1f} {5 * s:.1f}" class="hw-i-l"/>' for c, s in ((1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7), (-1, 0), (-0.7, -0.7), (0, -1), (0.7, -0.7))),
    "engine": '<path d="M22 38h12v-8h22v8h10l6 8h8v-6h6v24h-6v-6h-8l-6 10H34l-6-8h-6Z" class="hw-i-l"/><path d="M14 44v16M14 52h8" class="hw-i-l"/><path d="M50 40l-7 12h6l-3 9 9-13h-6l4-8Z" class="hw-i-f"/>',
    "wheel": '<circle cx="50" cy="48" r="32" class="hw-i-l"/><circle cx="50" cy="48" r="8" class="hw-i-f"/><path d="M50 16v24M22 64l21-10M78 64 57 54" class="hw-i-l"/>',
}


def icon_art(kind, label="", cls=""):
    role = f' role="img" aria-label="{E(label)}"' if label else ' aria-hidden="true"'
    return f'<svg class="hw-ico{(" " + cls) if cls else ""}" viewBox="0 0 100 96"{role}>{ICON[kind]}</svg>'


def flow_line(L):
    """Hero overlay: energy runs battery > inverter > motor > wheel (decorative; labels are plain text)."""
    names = L.ui["flow"]
    kinds = ["battery", "inverter", "engine", "wheel"]
    xs = [40, 140, 240, 340]
    nodes = "".join(f'<g class="hw-fl-node" style="--d:{i * .35}s"><circle cx="{x}" cy="40" r="22"/><svg x="{x - 15}" y="25" width="30" height="30" viewBox="0 0 100 96">{ICON[k]}</svg></g>'
                    for i, (x, k) in enumerate(zip(xs, kinds)))
    path = "M62 40 H118 M162 40 H218 M262 40 H318"
    return (f'<div class="hw-flow hw-anim" aria-hidden="true"><svg viewBox="0 0 380 80" class="hw-flow-svg">'
            f'<path d="{path}" class="hw-fl-track"/><path d="{path}" class="hw-fl-run" pathLength="100"/><path d="{path}" class="hw-fl-run hw-fl-run2" pathLength="100"/>{nodes}</svg>'
            f'<ol class="hw-flow-names">' + "".join(f"<li>{E(n)}</li>" for n in names) + "</ol></div>")


def charge_meter(L):
    return (f'<div class="hw-meter hw-anim" data-meter aria-hidden="true"><span class="hw-meter-lbl">{E(L.ui["charge_label"])}</span>'
            f'<span class="hw-meter-bar"><i></i></span><span class="hw-meter-num" data-meter-num>100%</span></div>')



# ------------------------------------------------------------------ schema
def business_node(L):
    return {
        "@type": "AutoRepair", "@id": CFG["site_url"] + "#business", "name": CFG["brand"], "legalName": CFG["name"],
        "alternateName": [CFG["short_name"], "Hybrid World"], "description": L.s["pages"]["home"]["description"],
        "url": abs_url(L.prefix), "image": abs_url("", "img/og-1200x630.jpg"), "logo": abs_url("", "img/logo-512.png"),
        "telephone": CFG["phone_e164"], "email": CFG["email"],
        "address": {"@type": "PostalAddress", "streetAddress": CFG["street"], "postalCode": CFG["postcode"],
                    "addressLocality": CFG["locality"], "addressRegion": CFG["region"], "addressCountry": CFG["country_code"]},
        "geo": {"@type": "GeoCoordinates", "latitude": CFG["lat"], "longitude": CFG["lng"]},
        "hasMap": CFG["maps_url"], "openingHours": CFG["opening_hours"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ([f"https://schema.org/{d}" for d in h["days"]] if len(h["days"]) > 1 else f"https://schema.org/{h['days'][0]}"),
                                       "opens": h["opens"], "closes": h["closes"]} for h in CFG["hours"]],
        "identifier": {"@type": "PropertyValue", "propertyID": "SSM company no.", "value": CFG["registration_no"]},
        "areaServed": [{"@type": "City", "name": "Johor Bahru"}, {"@type": "City", "name": "Iskandar Puteri"}],
        "sameAs": [CFG["facebook_url"]],
        "knowsLanguage": [STR[l["code"]]["meta"]["schema_lang"] for l in LANGS],
    }


def crumbs_node(L, trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(L.prefix, p)} for i, (n, p) in enumerate(trail)]}


def faq_node(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in faq]}


def schema(L, path, pg, trail, extra=()):
    graph = [business_node(L),
             {"@type": "WebSite", "@id": CFG["site_url"] + "#website", "name": CFG["brand"], "url": abs_url(""),
              "inLanguage": [STR[l["code"]]["meta"]["schema_lang"] for l in LANGS], "publisher": {"@id": CFG["site_url"] + "#business"}},
             {"@type": "WebPage", "@id": abs_url(L.prefix, path) + "#webpage", "url": abs_url(L.prefix, path), "name": pg["title"],
              "description": pg["description"], "inLanguage": L.s["meta"]["schema_lang"], "primaryImageOfPage": abs_url("", "img/og-1200x630.jpg"),
              "isPartOf": {"@id": CFG["site_url"] + "#website"}, "about": {"@id": CFG["site_url"] + "#business"}}]
    if len(trail) > 1:
        graph.append(crumbs_node(L, trail))
    graph += list(extra)
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return '  <script type="application/ld+json">' + data.replace("</", "<\\/") + "</script>"


# ------------------------------------------------------------------ shared page frame
def nav_items(L, active):
    ui = L.ui["nav"]
    cur = lambda k: ' aria-current="page"' if active == k else ""
    svc = "".join(f'<li><a href="{L.url(SVC[k]["slug"])}"{cur(k)}>{E(L.s["services"][k]["name"])}</a></li>' for k in SVC)
    return "\n".join([
        f'        <li><a href="{L.url()}"{cur("home")}>{E(ui["home"])}</a></li>',
        f'        <li class="hw-links-svc"><span class="hw-links-h">{E(ui["services"])}</span><ul>{svc}</ul></li>',
        f'        <li><a href="{L.url("articles/")}"{cur("articles")}>{E(ui["articles"])}</a></li>',
        f'        <li><a href="{L.url("about/")}"{cur("about")}>{E(ui["about"])}</a></li>',
        f'        <li><a href="{L.url("contact/")}"{cur("contact")}>{E(ui["contact"])}</a></li>',
    ])


def page(L, path, key, active, body, trail, extra_schema=(), body_class="", preload="", pg=None):
    s, pg = L.s, pg or L.s["pages"][key]
    robots = '  <meta name="robots" content="noindex,nofollow">\n' if CFG["preview"] else '  <meta name="robots" content="index,follow,max-image-preview:large">\n'
    alts = "".join(f'  <link rel="alternate" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" href="{abs_url(l["prefix"], path)}">\n' for l in LANGS)
    alts += f'  <link rel="alternate" hreflang="x-default" href="{abs_url("", path)}">\n'
    switch = " | ".join(
        f'<a href="{BASE + l["prefix"] + path}" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" lang="{STR[l["code"]]["meta"]["html_lang"]}"'
        + (' aria-current="true"' if l["code"] == L.code else "") + f'>{E(STR[l["code"]]["meta"]["switch_name"])}</a>' for l in LANGS)
    doc = fill("head", lang=s["meta"]["html_lang"], title=E(pg["title"]), description=E(pg["description"]), robots=robots,
               canonical=abs_url(L.prefix, path), hreflang=alts, base=BASE, brand_name=E(CFG["brand"]),
               og_image=abs_url("", "img/og-1200x630.jpg"), og_alt=E(s["photos"][SITE["og_photo"]]), og_locale=s["meta"]["og_locale"],
               asset_v=ASSET_V, preload=preload, schema=schema(L, path, pg, trail, extra_schema))
    doc += fill("header", body_class=body_class, skip=E(L.ui["skip"]), home=L.url(), base=BASE, brand=E(CFG["brand"]), short=E(CFG["short_name"]),
                nav_label=E(L.ui["nav_label"]), nav_items=nav_items(L, active), lang_label=E(L.ui["lang_label"]), switcher=switch,
                menu=E(L.ui["menu_open"]), wa=wa(L, "header", short=True, cls=" hw-wa-pill"))
    doc += '<main id="main">\n'
    if len(trail) > 1:
        doc += crumbs(L, trail)
    doc += body
    sl = "\n".join(f'          <li><a href="{L.url(SVC[k]["slug"])}">{E(L.s["services"][k]["name"])}</a></li>' for k in SVC)
    cl = " · ".join(f'<a href="{L.url(p)}">{E(L.ui["nav"][n])}</a>' for n, p in (("home", ""), ("articles", "articles/"), ("about", "about/"), ("contact", "contact/")))
    doc += fill("footer", base=BASE, brand=E(CFG["brand"]), about=E(L.ui["footer_about"]), legal_name=E(CFG["name"]),
                reg_label=E(L.ui["reg_label"]), reg_no=E(CFG["registration_no"]), services_h=E(L.ui["footer_services"]), service_links=sl,
                company_links=cl, visit_h=E(L.ui["footer_visit"]), talk_h=E(L.ui["phone_label"]), address=E(CFG["address_display"]),
                hours_label=E(L.ui["hours_label"]), hours=E(L.ui["hours_text"]), wa_href=E(wa_href(L)), phone=E(CFG["phone_display"]),
                phone_e164=CFG["phone_e164"], call_short=E(L.ui["call_short"]), email=E(CFG["email"]), maps_url=E(CFG["maps_url"]),
                map_open=E(L.ui["map_open"]), facebook_url=E(CFG["facebook_url"]), facebook=E(L.ui["facebook"]), year=YEAR,
                rights=E(L.ui["rights"]), credit_url=E(CFG["credit_url"]), credit=E(CFG["credit"]),
                wa=wa(L, "mobile_bar", short=True, cls=" hw-fab-wa"), tel=tel(L, "mobile_bar", short=True, cls=" hw-fab-call"))
    PAGES.append((L.prefix + path, doc))


def crumbs(L, trail):
    items = "".join(f'<li aria-current="page">{E(n)}</li>' if i == len(trail) - 1 else f'<li><a href="{L.url(p)}">{E(n)}</a></li>'
                    for i, (n, p) in enumerate(trail))
    return '<div class="hw-shell">' + fill("crumbs", label=E(L.ui["breadcrumb_label"]), items=items) + "</div>\n"


def faq_block(L, faq):
    items = "\n".join(f'      <details><summary>{E(q["q"])}</summary><p>{E(q["a"])}</p></details>' for q in faq)
    return fill("faq", h2=E(L.ui["faq_h2"]), items=items)


def cta(L, place, key="general", topic=""):
    return fill("cta", kicker=E(L.ui["cta_kicker"]), h2=E(L.ui["cta_h2"]), p=E(L.ui["cta_p"]),
                wa=wa(L, place, key, topic), tel=tel(L, place, cls=" hw-call-line"))


def filmstrip(L, keys, label):
    n = len(keys)
    items = "".join(f'<figure class="hw-frame" role="group" aria-roledescription="slide" aria-label="{i + 1} / {n}">'
                    f'{img_tag(L, k, "(max-width: 760px) 92vw, 380px")}<figcaption>{E(L.s["photo_caps"][k])}</figcaption></figure>'
                    for i, k in enumerate(keys))
    dots = "".join(f'<button class="hw-dot" type="button" aria-label="{E(L.ui["car_dot"].replace("{n}", str(i + 1)))}"></button>' for i in range(n))
    return fill("filmstrip", label=E(label), items=items, dots=dots, prev=E(L.ui["car_prev"]), next=E(L.ui["car_next"]))


def stories(L):
    out = []
    for r in SITE["reels"]:
        land = r["shape"] == "landscape"
        out.append(fill("story", shape=r["shape"], poster=f'{BASE}media/reel-{r["id"]}.jpg', mp4=f'{BASE}media/reel-{r["id"]}.mp4',
                        w=640 if land else 360, h=360 if land else 640, caption=E(L.s["reels"][r["id"]]), play=E(L.ui["reel_play"]),
                        time=f'{r["seconds"] // 60}:{r["seconds"] % 60:02d}'))
    player = (f'<dialog class="hw-player" aria-label="{E(L.ui["reel_label"])}"><div class="hw-player-box"></div>'
              f'<p class="hw-player-cap"></p><button class="hw-round hw-player-x" type="button" aria-label="{E(L.ui["close"])}">✕</button></dialog>')
    return '<ul class="hw-stories">\n' + "\n".join(out) + "\n</ul>" + player


def gauge(L, place):
    # 4.5 of 5 = 90% of the arc; shown as text, never as rating schema
    return (f'<li class="hw-gauge"><a href="{E(CFG["maps_url"])}" target="_blank" rel="noopener" data-cta="google_reviews_{place}">'
            f'<svg viewBox="0 0 120 70" aria-hidden="true"><path d="M10 62a50 50 0 0 1 100 0" class="hw-g-track"/><path d="M10 62a50 50 0 0 1 100 0" class="hw-g-fill" pathLength="100"/></svg>'
            f'<span class="hw-g-num" aria-hidden="true">{CFG["rating"]}</span><span class="hw-g-lbl">{E(L.ui["gauge_label"])}</span>'
            f'<span class="hw-g-txt">{E(L.ui["rating"])}</span><span class="hw-g-more">{E(L.ui["rating_link"])} ↗</span></a></li>')


def quotes(L, place, order=None):
    revs = SITE["reviews"]
    if order:
        revs = sorted(revs, key=lambda r: order.index(r["name"]) if r["name"] in order else 99)
    note = f'<p class="hw-fine">{E(L.ui["review_lang_note"])}</p>' if L.ui.get("review_lang_note") else ""
    return ('<ul class="hw-quotes">' + gauge(L, place) + "".join(fill("quote", text=E(r["text"]), name=E(r["name"])) for r in revs)
            + "</ul>" + note)


def rating_link(L, place):
    return (f'<a class="hw-rate" href="{E(CFG["maps_url"])}" target="_blank" rel="noopener" data-cta="google_reviews_{place}">'
            f'<span class="hw-rate-star" aria-hidden="true">★</span>{E(L.ui["rating"])}</a>')


def map_block(L, place):
    return fill("map_facade", embed=E(CFG["maps_embed"]), map_title=E(CFG["brand"]), map_load=E(L.ui["map_load"]), place=place,
                brand=E(CFG["brand"]), address=E(CFG["address_display"]), hours_label=E(L.ui["hours_label"]), hours=E(L.ui["hours_text"]),
                wa=wa(L, place), tel=tel(L, place, cls=" hw-call-line"), maps_url=E(CFG["maps_url"]), map_open=E(L.ui["map_open"]),
                email=E(CFG["email"]), email_label=E(L.ui["email"]), map_note=E(L.ui["map_note"]))


def models_list(L, only=None):
    ms = L.s["models"] if only is None else [L.s["models"][i] for i in only]
    return f'<h3>{E(L.ui["models_h3"])}</h3><ul class="hw-tags">' + "".join(f"<li>{E(m)}</li>" for m in ms) + "</ul>"


def sections_html(secs):
    return "".join(f'<h2>{E(x["h2"])}</h2>' + "".join(f"<p>{E(p)}</p>" for p in x["p"]) for x in secs)


def svc_links(L, skip=None):
    return ('<ul class="hw-svc-list">' + "".join(
        f'<li><a href="{L.url(SVC[k]["slug"])}"><span class="hw-svc-ico">{icon_art(SVC[k]["icon"])}</span><span>{E(L.s["services"][k]["name"])}</span></a></li>'
        for k in SVC if k != skip) + "</ul>")


# The interactive hybrid system: node -> services shown in its panel, and the photo or icon used.
NODES = [("battery", ["battery", "recon"], "battery-pack", "battery", (64, 62)),
         ("inverter", ["inverter"], None, "inverter", (40, 38)),
         ("engine", ["engine"], None, "engine", (22, 50)),
         ("gearbox", ["transmission"], None, "transmission", (36, 66)),
         ("aircon", ["aircon"], None, "aircon", (52, 30))]


def system_diagram(L):
    chips, spots, panels = [], [], []
    for i, (node, svcs, photo, icon, (x, y)) in enumerate(NODES):
        sel = "true" if i == 0 else "false"
        chips.append(f'<button class="hw-node" type="button" id="hw-node-{node}" aria-expanded="{sel}" aria-controls="hw-panel-{node}" data-node="{node}">'
                     f'<span class="hw-node-ico">{icon_art(icon)}</span>{E(L.ui["nodes"][node])}</button>')
        spots.append(f'<span class="hw-spot" data-node="{node}" style="left:{x}%;top:{y}%"><i></i></span>')
        media = img_tag(L, photo, "(max-width: 760px) 92vw, 420px") if photo else f'<div class="hw-panel-art">{icon_art(icon, L.ui["nodes"][node])}</div>'
        body = "".join(f'<h3><a href="{L.url(SVC[k]["slug"])}">{E(L.s["services"][k]["name"])}</a></h3><p>{E(L.s["services"][k]["card"])}</p>'
                       f'<p><a class="hw-more" href="{L.url(SVC[k]["slug"])}">{E(L.ui["open_page"])} →</a></p>' for k in svcs)
        panels.append(f'<div class="hw-panel{" is-on" if i == 0 else ""}" id="hw-panel-{node}" role="region" aria-labelledby="hw-node-{node}">'
                      f'<div class="hw-panel-media">{media}</div><div class="hw-panel-txt">{body}</div></div>')
    car = ('<svg class="hw-car" viewBox="0 0 400 180" aria-hidden="true">'
           '<path d="M28 128c-6 0-10-4-10-10v-14c0-8 5-14 13-16l44-12 50-36c8-6 18-9 28-9h104c12 0 23 5 31 13l34 34 36 8c10 2 16 10 16 20v12c0 6-4 10-10 10Z" class="hw-car-body"/>'
           '<path d="M140 46h56v40h-96Zm72 0h52c8 0 15 3 21 9l25 31h-98Z" class="hw-car-glass"/>'
           '<path d="M62 120 C120 120 150 112 172 112 S256 116 300 108" class="hw-car-wire" pathLength="100"/>'
           '<circle cx="92" cy="132" r="26" class="hw-car-tyre"/><circle cx="92" cy="132" r="11" class="hw-car-hub"/>'
           '<circle cx="318" cy="132" r="26" class="hw-car-tyre"/><circle cx="318" cy="132" r="11" class="hw-car-hub"/></svg>')
    return (f'<div class="hw-system" data-part="diagram" data-system>'
            f'<div class="hw-system-stage">{car}{"".join(spots)}</div>'
            f'<div class="hw-nodes" role="group">{"".join(chips)}</div>'
            f'<div class="hw-panels">{"".join(panels)}</div></div>')


def process(L):
    li = "".join(f'<li style="--p:{(i + 1) * 25}"><span class="hw-pct">{(i + 1) * 25}%</span><h3>{E(st["t"])}</h3><p>{E(st["d"])}</p></li>'
                 for i, st in enumerate(L.s["process"]))
    return f'<div class="hw-charge hw-anim" data-part="process"><div class="hw-charge-bar" aria-hidden="true"><i></i></div><ol>{li}</ol></div>'


def head2(h2, hid, p=""):
    return f'<h2 id="{hid}">{E(h2)}</h2>' + (f'<p class="hw-sub">{E(p)}</p>' if p else "")


def hero_preload(key, mobile_w=640):
    stem = PHOTO[key]["file"][:-5]
    return (f'  <link rel="preload" as="image" href="{BASE}img/{stem}-640.webp" imagesrcset="{BASE}img/{stem}-640.webp 640w, {BASE}img/{stem}-1200.webp 1200w" imagesizes="100vw">\n')


def hero_preload_home():
    p, d = PHOTO[HERO_PHONE]["file"][:-5], PHOTO[HERO_PHOTO]["file"][:-5]
    return (f'  <link rel="preload" as="image" href="{BASE}img/{p}-640.webp" media="(max-width: 699px)">\n'
            f'  <link rel="preload" as="image" href="{BASE}img/{d}-1200.webp" imagesrcset="{BASE}img/{d}-640.webp 640w, {BASE}img/{d}-1200.webp 1200w" imagesizes="100vw" media="(min-width: 700px)">\n')


# ------------------------------------------------------------------ pages
HERO_PHOTO = "battery-pack"   # desktop (landscape, 1280 px)
HERO_PHONE = "chr-lift"        # phones (portrait)


def hero_picture(L):
    """Real photo hero: the C-HR on the lift on phones, the battery pack on wider screens."""
    p, d = PHOTO[HERO_PHONE]["file"][:-5], PHOTO[HERO_PHOTO]["file"][:-5]
    (dw, dh), _ = SIZES[HERO_PHOTO]
    return (f'<picture><source media="(max-width: 699px)" srcset="{BASE}img/{p}-640.webp">'
            f'<img src="{BASE}img/{d}-1200.webp" srcset="{BASE}img/{d}-640.webp 640w, {BASE}img/{d}-1200.webp {dw}w" sizes="100vw" '
            f'width="{dw}" height="{dh}" alt="{E(L.ui["hero_alt"])}" fetchpriority="high" decoding="async"></picture>')


def build_home(L):
    h = L.s["pages"]["home"]
    body = f'''<section class="hw-hero" aria-labelledby="h1">
  <div class="hw-hero-photo">{hero_picture(L)}</div>
  <div class="hw-hero-scrim" aria-hidden="true"></div>
  <div class="hw-shell hw-hero-in">
    {flow_line(L)}
    {charge_meter(L)}
    <h1 id="h1">{E(h["h1"])}</h1>
    <p class="hw-hero-line">{E(h["tagline"])}</p>
    <p class="hw-diag-note">{E(L.ui["diag_note"])}</p>
    <div class="hw-actions">{wa(L, "home_hero", "diagnosis", cls=" hw-wa-big")}{tel(L, "home_hero", cls=" hw-call-glass hw-wide-only")}</div>
    {rating_link(L, "hero")}
  </div>
</section>
<section class="hw-band hw-band-white" id="services" aria-labelledby="svc-h">
  <div class="hw-shell">{head2(h["system_h2"], "svc-h", L.ui["system_hint"])}{system_diagram(L)}
  <h3 class="hw-list-h">{E(L.ui["all_services"])}</h3>{svc_links(L)}</div>
</section>
<section class="hw-band hw-band-mist" id="reels" aria-labelledby="reels-h">
  <div class="hw-shell">{head2(h["reels_h2"], "reels-h", h["reels_p"])}{stories(L)}
  <p class="hw-after"><a class="hw-ghost" href="{E(CFG["facebook_url"])}" target="_blank" rel="noopener">{E(L.ui["more_reels"])} ↗</a></p></div>
</section>
<section class="hw-band hw-band-white" id="process" aria-labelledby="pr-h">
  <div class="hw-shell">{head2(h["process_h2"], "pr-h")}{process(L)}</div>
</section>
<section class="hw-band hw-band-blue" id="reviews" aria-labelledby="rev-h">
  <div class="hw-shell">{head2(h["reviews_h2"], "rev-h")}{quotes(L, "reviews")}</div>
</section>
<section class="hw-band hw-band-white" id="photos" aria-labelledby="ph-h">
  <div class="hw-shell">{head2(h["photos_h2"], "ph-h")}{filmstrip(L, SITE["carousel"], h["photos_h2"])}</div>
</section>
<section class="hw-band hw-band-mist" id="visit" aria-labelledby="visit-h">
  <div class="hw-shell">{head2(h["visit_h2"], "visit-h")}{map_block(L, "home")}</div>
</section>
<section class="hw-band hw-band-white" id="about" aria-labelledby="about-h">
  <div class="hw-shell hw-split">
    <div class="hw-read">{head2(h["about_h2"], "about-h")}{"".join(f"<p>{E(p)}</p>" for p in h["about"])}</div>
    <div class="hw-side">{models_list(L)}</div>
  </div>
</section>
{faq_block(L, h["faq"])}{cta(L, "home_bottom")}'''
    page(L, "", "home", "home", body, [(L.ui["nav"]["home"], "")], [faq_node(h["faq"])], body_class="hw-home", preload=hero_preload_home())


def build_service(L, k):
    c, sv, pg = SVC[k], L.s["services"][k], L.s["pages"][k]
    path = c["slug"]
    trail = [(L.ui["nav"]["home"], ""), (sv["name"], path)]
    media = figure(L, c["hero"], eager=True, cls="hw-pic-hero") if c.get("hero") else f'<div class="hw-art-panel">{icon_art(c["icon"], L.s["art"].get(k, sv["name"]))}<span class="hw-art-wire" aria-hidden="true"></span></div>'
    ph = c.get("photos", [])
    film = side_pics = ""
    if len(ph) >= 3:
        film = f'<section class="hw-band hw-band-mist" aria-labelledby="g-h"><div class="hw-shell"><h2 id="g-h">{E(L.ui["photo_label"])}</h2>{filmstrip(L, ph, sv["name"])}</div></section>'
    elif ph:
        side_pics = "".join(figure(L, p) for p in ph)
    models = ""
    if k in ("battery", "recon", "inverter"):
        models = models_list(L)
    elif k == "toyota":
        models = models_list(L, [0, 1, 2, 3, 4, 5])
    elif k == "honda":
        models = models_list(L, [6])
    order = ["David"] if k == "honda" else None
    body = f'''<section class="hw-intro" aria-labelledby="h1">
  <div class="hw-shell hw-intro-grid">
    <div class="hw-intro-txt">
      <p class="hw-eyebrow"><span class="hw-eyebrow-ico">{icon_art(c["icon"])}</span>{E(CFG["brand"])}</p>
      <h1 id="h1">{E(pg["h1"])}</h1>
      <p class="hw-lede">{E(pg["intro"])}</p>
      <p class="hw-diag-note">{E(L.ui["diag_note"])}</p>
      <div class="hw-actions">{wa(L, "service_" + k, "diagnosis")}{tel(L, "service_" + k, cls=" hw-call-line")}</div>
      {rating_link(L, "service")}
    </div>
    <div class="hw-intro-media">{media}</div>
  </div>
</section>
<section class="hw-band hw-band-white">
  <div class="hw-shell hw-split">
    <div class="hw-read">{sections_html(pg["sections"])}</div>
    <aside class="hw-side">{models}{side_pics}</aside>
  </div>
</section>
{film}
<section class="hw-band hw-band-blue" aria-labelledby="rv-h"><div class="hw-shell"><h2 id="rv-h">{E(L.s["pages"]["home"]["reviews_h2"])}</h2>{quotes(L, "service", order)}</div></section>
{faq_block(L, pg["faq"])}
<section class="hw-band hw-band-white" aria-labelledby="rel-h"><div class="hw-shell"><h2 id="rel-h">{E(L.ui["related_h2"])}</h2>{svc_links(L, skip=k)}</div></section>
{cta(L, "service_" + k + "_bottom", "service", sv["name"])}'''
    svc = {"@type": "Service", "@id": abs_url(L.prefix, path) + "#service", "name": sv["name"], "serviceType": sv["name"],
           "description": pg["description"], "provider": {"@id": CFG["site_url"] + "#business"},
           "areaServed": {"@type": "City", "name": "Johor Bahru"}, "url": abs_url(L.prefix, path)}
    pre = hero_preload(c["hero"]) if c.get("hero") else ""
    page(L, path, k, k, body, trail, [svc, faq_node(pg["faq"])], body_class="hw-svc", preload=pre)


def facts_dl(L, place):
    return (f'<dl class="hw-facts">'
            f'<dt>{E(L.ui["reg_label"])}</dt><dd>{E(CFG["name"])} ({E(CFG["registration_no"])})</dd>'
            f'<dt>{E(L.ui["address_label"])}</dt><dd>{E(CFG["address_display"])}</dd>'
            f'<dt>{E(L.ui["hours_label"])}</dt><dd>{E(L.ui["hours_text"])}</dd>'
            f'<dt>{E(L.ui["phone_label"])}</dt><dd><a href="{E(wa_href(L))}" target="_blank" rel="noopener" data-cta="whatsapp_{place}_card">WhatsApp {E(CFG["phone_display"])}</a><br>'
            f'<a href="tel:{CFG["phone_e164"]}" data-cta="call_{place}_card">{E(L.ui["call_short"])} {E(CFG["phone_display"])}</a></dd>'
            f'<dt>{E(L.ui["email_label"])}</dt><dd><a href="mailto:{CFG["email"]}" data-cta="email_{place}_card">{E(CFG["email"])}</a></dd>'
            f'<dt>Facebook</dt><dd><a href="{E(CFG["facebook_url"])}" target="_blank" rel="noopener">{E(L.ui["facebook"])}</a></dd></dl>')


def build_about(L):
    pg = L.s["pages"]["about"]
    trail = [(L.ui["nav"]["home"], ""), (L.ui["nav"]["about"], "about/")]
    figs = "".join(figure(L, p, eager=(i == 0)) for i, p in enumerate(SITE["about_photos"]))
    body = f'''<section class="hw-intro" aria-labelledby="h1">
  <div class="hw-shell"><h1 id="h1">{E(pg["h1"])}</h1><p class="hw-lede">{E(pg["intro"])}</p>
  <div class="hw-actions">{wa(L, "about_top")}{tel(L, "about_top", cls=" hw-call-line")}</div>{rating_link(L, "about")}</div>
</section>
<section class="hw-band hw-band-mist"><div class="hw-shell"><div class="hw-mosaic">{figs}</div></div></section>
<section class="hw-band hw-band-white"><div class="hw-shell hw-split">
  <div class="hw-read">{sections_html(pg["sections"])}</div>
  <div class="hw-side"><h2>{E(pg["company_h2"])}</h2>{facts_dl(L, "about")}</div>
</div></section>
{cta(L, "about_bottom")}'''
    page(L, "about/", "about", "about", body, trail, preload=hero_preload(SITE["about_photos"][0]))


def build_contact(L):
    pg = L.s["pages"]["contact"]
    trail = [(L.ui["nav"]["home"], ""), (L.ui["nav"]["contact"], "contact/")]
    body = f'''<section class="hw-intro" aria-labelledby="h1">
  <div class="hw-shell"><h1 id="h1">{E(pg["h1"])}</h1><p class="hw-lede">{E(pg["intro"])}</p>
  <div class="hw-actions">{wa(L, "contact_top", cls=" hw-wa-big")}{tel(L, "contact_top", cls=" hw-call-line")}</div></div>
</section>
<section class="hw-band hw-band-mist" id="contact"><div class="hw-shell">{map_block(L, "contact")}</div></section>
<section class="hw-band hw-band-white"><div class="hw-shell hw-split">
  <div>{figure(L, "shopfront")}</div>
  <div class="hw-side">{facts_dl(L, "contact")}{rating_link(L, "contact")}</div>
</div></section>'''
    page(L, "contact/", "contact", "contact", body, trail)



# ------------------------------------------------------------------ articles (one JSON per article in data/articles/, EN + BM + 中文)
# Looks: charge (photo with a charge-level rail), flow (icon art on the energy line), dash (dark instrument-panel frame).
ART_LOOKS = ("charge", "flow", "dash")
ART_CSS = (ROOT / "assets" / "articles.css").read_text(encoding="utf-8")
ART_V = hashlib.sha256(ART_CSS.encode()).hexdigest()[:10]
ARTICLES = sorted((json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "data" / "articles").glob("*.json")),
                  key=lambda a: (a["published"], a["slug"]), reverse=True)
ART_HEAD = f'  <link rel="stylesheet" href="{BASE}assets/articles.css?v={ART_V}">\n'


def art_date(L, iso):
    y, m, d = (int(x) for x in iso.split("-"))
    fmt = L.s["articles"]["date_fmt"]
    return fmt.replace("{d}", str(d)).replace("{m}", L.s["articles"]["months"][m - 1]).replace("{mn}", str(m)).replace("{y}", str(y))


def art_minutes(L, t):
    words = " ".join([t["lead"], t["answer"]] + [p for s in t["sections"] for p in s.get("p", []) + s.get("list", []) + [s.get("p_after", "")]]
                     + [x["d"] for s in t["sections"] for x in s.get("pairs", [])] + [x["p"] for s in t["sections"] for x in s.get("h3", [])])
    n = len(words) / 450 if L.code == "zh" else len(words.split()) / 200
    return max(2, round(n + .4))


def art_visual(L, a, where):
    v = a["look"]["visual"]
    if v["type"] == "photo":
        sizes = "(max-width: 760px) 92vw, 520px" if where == "hero" else "(max-width: 700px) 92vw, 380px"
        return img_tag(L, v["key"], sizes, eager=(where == "hero"))
    return f'<div class="hw-art-panel">{icon_art(v["icon"], L.s["services"][a["service"]]["name"] if where == "hero" else "")}<span class="hw-art-wire" aria-hidden="true"></span></div>'


def art_image_url(a):
    v = a["look"]["visual"]
    return abs_url("", f'img/{PHOTO[v["key"]]["file"][:-5]}-1200.webp') if v["type"] == "photo" else abs_url("", "img/og-1200x630.jpg")


def art_steps(L, steps):
    return '<ol class="hw-ar-steps">' + "".join(f'<li><b>{E(s["t"])}</b> {E(s["d"])}</li>' for s in steps) + "</ol>"


def art_section(L, i, s):
    out = f'<section class="hw-ar-sec" aria-labelledby="s{i + 1}"><p class="hw-ar-n" aria-hidden="true">{i + 1:02d}</p><h2 id="s{i + 1}">{E(s["h2"])}</h2>'
    out += "".join(f"<p>{E(p)}</p>" for p in s.get("p", []))
    if s.get("pairs"):
        out += '<dl class="hw-ar-pairs">' + "".join(f'<div><dt>{E(x["t"])}</dt><dd>{E(x["d"])}</dd></div>' for x in s["pairs"]) + "</dl>"
    if s.get("process"):  # the site's own 4 steps (last one is always the final check)
        out += art_steps(L, L.s["process"])
    if s.get("steps"):
        out += art_steps(L, s["steps"])
    if s.get("list"):
        out += '<ul class="hw-ar-list">' + "".join(f"<li>{E(x)}</li>" for x in s["list"]) + "</ul>"
    for x in s.get("h3", []):
        out += f'<h3>{E(x["h3"])}</h3><p>{E(x["p"])}</p>'
    if s.get("p_after"):
        out += f'<p>{E(s["p_after"])}</p>'
    if s.get("link"):
        k = s["link"]
        out += f'<p><a class="hw-more" href="{L.url(SVC[k]["slug"])}">{E(L.s["services"][k]["name"])} →</a></p>'
    return out + "</section>"


def art_card(L, a):
    t = a[L.code]
    return fill("article_card", href=L.url(f'articles/{a["slug"]}/'), look=a["look"]["variant"], visual=art_visual(L, a, "card"),
                kicker=E(L.s["services"][a["service"]]["name"]), title=E(t["h1"]), date_iso=a["published"], date=E(art_date(L, a["published"])),
                excerpt=E(t["excerpt"]), more=E(L.s["articles"]["read_more"]))


def build_article(L, a):
    A, t, k = L.s["articles"], a[L.code], a["service"]
    path = f'articles/{a["slug"]}/'
    sv = L.s["services"][k]
    trail = [(L.ui["nav"]["home"], ""), (L.ui["nav"]["articles"], "articles/"), (t["h1"], path)]
    secs = []
    for i, s in enumerate(t["sections"]):
        secs.append(art_section(L, i, s))
        if i == a["cta_after"]:
            secs.append(fill("article_cta", h=E(A["mid_h"]), p=E(A["mid_p"]), wa=wa(L, "article_mid", "service", t["topic"])))
    others = [x for x in ARTICLES if x["slug"] != a["slug"]][:3]
    more = (f'<section class="hw-band hw-band-mist" aria-labelledby="more-h"><div class="hw-shell"><h2 id="more-h">{E(A["more_h2"])}</h2>'
            f'<div class="hw-ar-cards">{"".join(art_card(L, x) for x in others)}</div>'
            f'<p class="hw-after"><a class="hw-ghost" href="{L.url("articles/")}">{E(A["all"])} →</a></p></div></section>') if others else ""
    body = fill("article", look=a["look"]["variant"], motif=E(t["motif"]), svc_href=L.url(SVC[k]["slug"]), svc_icon=icon_art(SVC[k]["icon"]),
                svc_name=E(sv["name"]), h1=E(t["h1"]), date_iso=a["published"], date=E(art_date(L, a["published"])),
                minutes=E(A["read_time"].replace("{n}", str(art_minutes(L, t)))), byline=E(A["byline"]),
                wa=wa(L, "article_top", "service", t["topic"], cls=" hw-wa-big"), tel=tel(L, "article_top", cls=" hw-call-line"),
                visual=art_visual(L, a, "hero"), caption=E(L.s["photo_caps"][a["look"]["visual"]["key"]]) if a["look"]["visual"]["type"] == "photo" else E(sv["tile"]),
                lead=E(t["lead"]), answer_k=E(A["answer"]), answer=E(t["answer"]), sections="".join(secs),
                owner_k=E(A["owner_kicker"]), owner_card=E(sv["card"]), owner_cta=E(A["owner_cta"]), rating=rating_link(L, "article"),
                side_wa=wa(L, "article_side", "service", t["topic"], short=True))
    body += faq_block(L, t["faqs"]) + more + cta(L, "article_bottom", "service", t["topic"])
    url = abs_url(L.prefix, path)
    art = {"@type": "Article", "@id": url + "#article", "headline": t["h1"], "description": t["description"], "inLanguage": L.s["meta"]["schema_lang"],
           "datePublished": a["published"], "dateModified": a["updated"], "image": [art_image_url(a)], "keywords": t["keyword"],
           "author": {"@id": CFG["site_url"] + "#business"}, "publisher": {"@id": CFG["site_url"] + "#business"},
           "mainEntityOfPage": {"@id": url + "#webpage"}, "isPartOf": {"@id": CFG["site_url"] + "#website"},
           "about": {"@type": "Service", "name": sv["name"], "url": abs_url(L.prefix, SVC[k]["slug"]), "provider": {"@id": CFG["site_url"] + "#business"}}}
    pg = {"title": t["title"], "description": t["description"]}
    page(L, path, None, "articles", body, trail, [art, faq_node(t["faqs"])], body_class="hw-ar-page", preload=ART_HEAD, pg=pg)


def build_articles_index(L):
    A = L.s["articles"]
    trail = [(L.ui["nav"]["home"], ""), (L.ui["nav"]["articles"], "articles/")]
    cards = "".join(art_card(L, a) for a in ARTICLES)
    body = f'''<section class="hw-intro hw-ar-intro" aria-labelledby="h1">
  <div class="hw-shell"><p class="hw-eyebrow">{E(A["eyebrow"])}</p><h1 id="h1">{E(A["h1"])}</h1><p class="hw-lede">{E(A["lead"])}</p>
  <div class="hw-actions">{wa(L, "articles_top")}{tel(L, "articles_top", cls=" hw-call-line")}</div></div>
</section>
<section class="hw-band hw-band-white" aria-labelledby="list-h"><div class="hw-shell"><h2 id="list-h">{E(A["list_h2"])}</h2>
  <div class="hw-ar-cards">{cards}</div></div></section>
{cta(L, "articles_bottom")}'''
    url = abs_url(L.prefix, "articles/")
    coll = {"@type": "CollectionPage", "@id": url + "#collection", "url": url, "name": A["title"], "inLanguage": L.s["meta"]["schema_lang"],
            "mainEntity": {"@type": "ItemList", "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "url": abs_url(L.prefix, f'articles/{a["slug"]}/'), "name": a[L.code]["h1"]} for i, a in enumerate(ARTICLES)]}}
    page(L, "articles/", None, "articles", body, trail, [coll], body_class="hw-ar-page", preload=ART_HEAD, pg={"title": A["title"], "description": A["description"]})


def check_articles():
    """Stops the build on an article that breaks the brief (facts stay in strings/config; this checks shape and language)."""
    probs = []
    final = {l["code"]: STR[l["code"]]["process"][-1]["t"] for l in LANGS}
    for a in ARTICLES:
        n = a["slug"]
        if a["service"] not in SVC:
            probs.append(f"{n}: unknown service {a['service']}")
        if a["look"]["variant"] not in ART_LOOKS:
            probs.append(f"{n}: look must be one of {ART_LOOKS}")
        v = a["look"]["visual"]
        if v["type"] == "photo" and v.get("key") not in PHOTO:
            probs.append(f"{n}: unknown photo {v.get('key')}")
        if v["type"] == "icon" and v.get("icon") not in ICON:
            probs.append(f"{n}: unknown icon {v.get('icon')}")
        for l in LANGS:
            t = a.get(l["code"])
            if not t:
                probs.append(f"{n}: {l['code']} missing")
                continue
            for f in ("title", "description", "keyword", "motif", "h1", "lead", "answer", "topic", "excerpt", "sections", "faqs"):
                if not t.get(f):
                    probs.append(f"{n} {l['code']}: {f} empty")
            if len(t.get("title", "")) > 62:
                probs.append(f"{n} {l['code']}: title over 62 chars")
            if len(t.get("description", "")) > 160:
                probs.append(f"{n} {l['code']}: description over 160 chars")
            if len(t.get("faqs", [])) < 3:
                probs.append(f"{n} {l['code']}: needs 3 FAQs")
            if t.get("keyword", "").lower() not in t.get("lead", "").lower():
                probs.append(f"{n} {l['code']}: keyword not in first paragraph")
            for s in t.get("sections", []):
                if s.get("steps") and not s["steps"][-1]["t"].startswith(final[l["code"]]):
                    probs.append(f"{n} {l['code']}: last step must be '{final[l['code']]}'")
            if l["code"] != "en" and t.get("lead") == a["en"]["lead"]:
                probs.append(f"{n} {l['code']}: still English")
        en = a.get("en", {})
        kw = en.get("keyword", "").lower()
        if kw not in en.get("title", "").lower() and kw not in en.get("h1", "").lower():
            probs.append(f"{n}: English keyword not in title or H1")
        if len(en.get("answer", "").split()) not in range(35, 66):
            probs.append(f"{n}: short answer should be 40-60 words")
    if probs:
        raise SystemExit("article problems:\n - " + "\n - ".join(probs))
    print(f"articles ok: {len(ARTICLES)}")


def all_paths():
    # Articles join the sitemap only after move day (preview false): the preview keeps them out of sitemap.xml and llms.txt.
    arts = [] if CFG["preview"] else ["articles/"] + [f'articles/{a["slug"]}/' for a in ARTICLES]
    return [""] + [SVC[k]["slug"] for k in SVC] + ["about/", "contact/"] + arts


def write_sitemap():
    today = date.today().isoformat()
    urls = []
    for l in LANGS:
        for p in all_paths():
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{STR[x["code"]]["meta"]["html_lang"]}" href="{live_url(x["prefix"], p)}"/>' for x in LANGS)
            urls.append(f"  <url><loc>{live_url(l['prefix'], p)}</loc><lastmod>{today}</lastmod>{alts}</url>")
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                                     'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")


def write_llms():
    en = STR["en"]
    lines = [f"# {CFG['brand']} ({CFG['short_name']})", "", f"> {en['pages']['home']['description']}", "",
             f"- Company: {CFG['name']} ({CFG['registration_no']})", f"- Address: {CFG['address_display']}",
             f"- WhatsApp and phone: {CFG['phone_display']} (https://wa.me/{WA_NUM})", f"- Email: {CFG['email']}",
             f"- Hours: {en['ui']['hours_text']}", f"- Google: {en['ui']['rating']}: {CFG['maps_url']}", f"- Facebook: {CFG['facebook_url']}",
             "- Hybrids we work on: " + "; ".join(en["models"]),
             "- Hybrid battery replacement uses new original/OEM battery sets, sold only as complete assembled units, never single cells.",
             "", "## Pages", ""]
    lines.append(f"- [{en['pages']['home']['h1']}]({live_url('')})")
    for k in SVC:
        lines.append(f"- [{en['services'][k]['name']}]({live_url('', SVC[k]['slug'])}): {en['pages'][k]['description']}")
    lines += [f"- [About]({live_url('', 'about/')})", f"- [Contact]({live_url('', 'contact/')})"]
    if not CFG["preview"] and ARTICLES:
        lines += ["", "## Articles", ""] + [f"- [{a['en']['h1']}]({live_url('', 'articles/' + a['slug'] + '/')}): {a['en']['description']}" for a in ARTICLES]
    lines += ["", "## Other languages", "",
              f"- Bahasa Melayu: {live_url('ms/')}", f"- 简体中文: {live_url('zh/')}", ""]
    (OUT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "site.js").write_text(JS, encoding="utf-8")
    (OUT / "assets" / "articles.css").write_text(ART_CSS, encoding="utf-8")
    check_articles()
    shutil.copytree(ROOT / "fonts", OUT / "fonts", ignore=shutil.ignore_patterns("*.txt"))
    build_images()
    for cfg in LANGS:
        L = Lang(cfg)
        build_home(L)
        for k in SVC:
            build_service(L, k)
        build_about(L)
        build_contact(L)
        build_articles_index(L)
        for a in ARTICLES:
            build_article(L, a)
    for path, doc in PAGES:
        f = OUT / path / "index.html"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(doc, encoding="utf-8")
    write_sitemap()
    write_llms()
    print(f"built {len(PAGES)} pages")
    r = subprocess.run([sys.executable, str(ROOT / "src" / "check.py")])
    if r.returncode:
        raise SystemExit("check failed")


if __name__ == "__main__":
    main()
