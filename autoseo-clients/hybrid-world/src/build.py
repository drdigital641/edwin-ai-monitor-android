#!/usr/bin/env python3
"""Build the Hybrid World Specialist site in English, Malay and Chinese.

    python3 autoseo-clients/hybrid-world/src/build.py

Business facts: config.json. Page order, photos, reels, review quotes: data/site.json.
Every visible string and the WhatsApp prefills: strings/<lang>.json (same keys).
Shared parts (head, header, footer, WhatsApp/call buttons, sticky bar, service tile,
step, carousel, reel, review, map facade, FAQ, CTA, breadcrumb): templates/.
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

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
SITE = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
LANGS = SITE["languages"]
STR = {l["code"]: json.loads((ROOT / "strings" / f"{l['code']}.json").read_text(encoding="utf-8")) for l in LANGS}
TPL = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / "templates").glob("*.html")}
OUT = ROOT / "site"
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


def img_tag(L, key, sizes, eager=False, cls=""):
    (bw, bh), (sw, sh) = SIZES[key]
    stem = PHOTO[key]["file"][:-5]
    srcset = f"{BASE}img/{stem}-640.webp {sw}w" + (f", {BASE}img/{stem}-1200.webp {bw}w" if bw > sw else "")
    extra = ' fetchpriority="high"' if eager else ""
    c = f' class="{cls}"' if cls else ""
    return (f'<img{c} src="{BASE}img/{stem}-640.webp" srcset="{srcset}" sizes="{sizes}" width="{sw}" height="{sh}" '
            f'alt="{E(L.s["photos"][key])}" loading="{"eager" if eager else "lazy"}" decoding="async"{extra}>')


def figure(L, key, sizes="(max-width: 760px) 100vw, 560px", eager=False, cls=""):
    return f'<figure class="ph{(" " + cls) if cls else ""}">{img_tag(L, key, sizes, eager)}<figcaption>{E(L.s["photo_caps"][key])}</figcaption></figure>'


# ------------------------------------------------------------------ graphics (no fake photos: icon art in the energy style)
ICON = {
    "battery": '<rect x="18" y="26" width="64" height="44" rx="7" class="i-line"/><rect x="82" y="40" width="7" height="16" rx="2" class="i-fill"/><rect x="26" y="34" width="10" height="28" rx="2" class="i-cell c1"/><rect x="40" y="34" width="10" height="28" rx="2" class="i-cell c2"/><rect x="54" y="34" width="10" height="28" rx="2" class="i-cell c3"/><rect x="68" y="34" width="8" height="28" rx="2" class="i-cell c4"/>',
    "recon": '<path d="M50 14a34 34 0 1 1-30 18" class="i-line i-spin"/><path d="M14 18l6 14 14-5" class="i-line"/><path d="M54 30 42 52h12l-6 18 16-26H52l6-14Z" class="i-fill"/>',
    "inverter": '<rect x="20" y="22" width="60" height="52" rx="8" class="i-line"/><path d="M30 48c5-12 10-12 15 0s10 12 15 0" class="i-line i-wave"/><path d="M8 40h12M8 56h12M80 40h12M80 56h12" class="i-line"/><path d="M62 30h10M67 25v10" class="i-line"/>',
    "car": '<path d="M16 62V50l9-16c2-4 5-6 9-6h32c4 0 7 2 9 6l9 16v12" class="i-line"/><path d="M12 62h76" class="i-line"/><circle cx="30" cy="66" r="8" class="i-line"/><circle cx="70" cy="66" r="8" class="i-line"/><path d="M53 30 44 46h9l-5 12 12-18h-9l4-10Z" class="i-fill"/>',
    "honda": '<circle cx="50" cy="48" r="32" class="i-line"/><path d="M50 16v8M50 72v8M18 48h8M74 48h8" class="i-line"/><path d="M53 28 40 52h11l-5 16 15-24H50l6-16Z" class="i-fill"/>',
    "aircon": '<path d="M50 14v68M21 31l58 34M21 65l58-34" class="i-line"/><path d="M42 20l8 8 8-8M42 76l8-8 8 8M17 41l11-3-3-11M83 55l-11 3 3 11M17 55l11 3-3 11M83 41l-11-3 3-11" class="i-line"/><circle cx="50" cy="48" r="7" class="i-fill"/>',
    "transmission": '<circle cx="38" cy="50" r="18" class="i-line"/><circle cx="38" cy="50" r="6" class="i-fill"/><circle cx="68" cy="30" r="12" class="i-line"/><circle cx="68" cy="30" r="4" class="i-fill"/>'
                    + "".join(f'<path d="M{38 + 18 * c:.1f} {50 + 18 * s:.1f}l{5 * c:.1f} {5 * s:.1f}" class="i-line"/>' for c, s in ((1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7), (-1, 0), (-0.7, -0.7), (0, -1), (0.7, -0.7))),
    "engine": '<path d="M22 38h12v-8h22v8h10l6 8h8v-6h6v24h-6v-6h-8l-6 10H34l-6-8h-6Z" class="i-line"/><path d="M14 44v16M14 52h8" class="i-line"/><path d="M50 40l-7 12h6l-3 9 9-13h-6l4-8Z" class="i-fill"/>',
    "whatsapp": '<path d="M50 14a34 34 0 0 0-29 51l-5 17 18-5a34 34 0 1 0 16-63Z" class="i-line"/><path d="M38 36c2-3 5-3 6 0l2 6c0 2-2 3-3 4 2 5 6 9 11 11 1-1 2-3 4-3l6 2c3 1 3 4 0 6-3 3-9 4-18-2s-12-14-11-19c0-2 1-4 3-5Z" class="i-fill"/>',
    "scan": '<circle cx="44" cy="44" r="24" class="i-line"/><path d="m62 62 18 18" class="i-line"/><path d="M28 44h8l4-8 6 16 4-8h8" class="i-line i-wave"/>',
    "quote": '<path d="M26 14h36l14 14v56H26Z" class="i-line"/><path d="M36 40h30M36 52h30M36 64h18" class="i-line"/><path d="M60 64l6 6 12-14" class="i-line i-ok"/>',
    "drive": '<circle cx="50" cy="50" r="32" class="i-line"/><circle cx="50" cy="50" r="8" class="i-fill"/><path d="M50 18v24M22 64l21-10M78 64 57 54" class="i-line"/>',
}


def icon_art(kind, label="", big=False):
    role = f' role="img" aria-label="{E(label)}"' if label else ' aria-hidden="true"'
    return (f'<svg class="iart{" iart-big" if big else ""} anim" viewBox="0 0 100 96"{role}>'
            f'<defs><linearGradient id="ig-{kind}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a6e34f"/><stop offset="1" stop-color="#22b8ff"/></linearGradient></defs>'
            f'<g style="--ig:url(#ig-{kind})">{ICON[kind]}</g></svg>')


def energy_flow(label):
    """Hero animation: energy flows between battery cells, the hybrid core, an engine and a wheel."""
    cells = "".join(f'<rect x="{30 + i * 15}" y="86" width="11" height="44" rx="3" class="cell cell{i}"/>' for i in range(5))
    spokes = "".join(f'<path d="M300 158 L{300 + 24 * c:.1f} {158 + 24 * s:.1f}" class="spoke"/>' for c, s in ((1, 0), (0.5, 0.866), (-0.5, 0.866), (-1, 0), (-0.5, -0.866), (0.5, -0.866)))
    flows = [("M106 108 C125 108 130 108 150 108", "fb"), ("M206 98 C232 88 240 60 262 56", "fg"),
             ("M206 118 C232 128 244 150 268 156", "fb"), ("M300 82 V124", "fg"), ("M150 108 C130 108 125 108 106 108", "fg rev")]
    tracks = "".join(f'<path d="{d}" class="track"/>' for d, _ in flows[:4])
    runs = "".join(f'<path d="{d}" class="flow {c}" pathLength="100"/>' for d, c in flows)
    sparks = "".join(f'<circle r="3.2" class="spark {c}"><animateMotion dur="{t}s" begin="{b}s" repeatCount="indefinite" path="{d}"/></circle>'
                     for d, c, t, b in (("M106 108 C125 108 130 108 150 108", "sb", 1.6, 0), ("M206 98 C232 88 240 60 262 56", "sg", 1.9, 0),
                                        ("M206 118 C232 128 244 150 268 156", "sb", 1.7, 0), ("M300 82 V124", "sg", 1.4, 0)))
    return f'''<svg class="flowart anim" viewBox="0 0 360 200" role="img" aria-label="{E(label)}">
  <defs>
    <linearGradient id="gB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#22b8ff"/><stop offset="1" stop-color="#7fe0ff"/></linearGradient>
    <linearGradient id="gG" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#a6e34f"/><stop offset="1" stop-color="#d9ff7a"/></linearGradient>
    <radialGradient id="gC"><stop offset="0" stop-color="#22b8ff" stop-opacity=".55"/><stop offset="1" stop-color="#22b8ff" stop-opacity="0"/></radialGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <g class="pack"><rect x="20" y="76" width="86" height="64" rx="10" class="shell"/><rect x="46" y="68" width="34" height="8" rx="3" class="shell-cap"/>{cells}</g>
  {tracks}
  <g filter="url(#glow)">{runs}{sparks}</g>
  <circle cx="178" cy="108" r="46" fill="url(#gC)" class="core-halo"/>
  <g class="core"><path d="M178 80 202 94v28l-24 14-24-14V94Z" class="hex"/><path d="M182 88 166 112h11l-5 18 17-26h-11l4-16Z" class="bolt"/></g>
  <g class="engine"><path d="M262 40h12v-7h22v7h8l6 7h6v-5h5v21h-5v-5h-6l-6 9h-30l-5-7h-7Z" class="shell"/><circle cx="288" cy="54" r="5" class="piston"/></g>
  <g class="wheel"><circle cx="300" cy="158" r="32" class="tyre"/><circle cx="300" cy="158" r="22" class="rim"/><g class="spokes">{spokes}</g><circle cx="300" cy="158" r="5" class="hub"/></g>
</svg>'''


def charge_bar(label):
    segs = "".join(f"<i style=\"--i:{i}\"></i>" for i in range(10))
    return f'<div class="chargebar anim" aria-hidden="true"><span class="cb-lbl">{E(label)}</span><span class="cb-segs">{segs}</span><span class="cb-plug"></span></div>'


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
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": [f"https://schema.org/{d}" for d in h["days"]],
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
    sub = "".join(f'<li><a href="{L.url(SVC[k]["slug"])}"{" aria-current=page" if active == k else ""}>{E(L.s["services"][k]["name"])}</a></li>' for k in SVC)
    cur = lambda k: ' aria-current="page"' if active == k else ""
    return "\n".join([
        f'        <li><a href="{L.url()}"{cur("home")}>{E(ui["home"])}</a></li>',
        f'        <li class="has-sub"><details><summary>{E(ui["services"])}</summary><ul class="sub">{sub}</ul></details></li>',
        f'        <li><a href="{L.url("about/")}"{cur("about")}>{E(ui["about"])}</a></li>',
        f'        <li><a href="{L.url("contact/")}"{cur("contact")}>{E(ui["contact"])}</a></li>',
    ])


def page(L, path, key, active, body, trail, extra_schema=(), body_class=""):
    s, pg = L.s, L.s["pages"][key]
    robots = '  <meta name="robots" content="noindex,nofollow">\n' if CFG["preview"] else '  <meta name="robots" content="index,follow,max-image-preview:large">\n'
    alts = "".join(f'  <link rel="alternate" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" href="{abs_url(l["prefix"], path)}">\n' for l in LANGS)
    alts += f'  <link rel="alternate" hreflang="x-default" href="{abs_url("", path)}">\n'
    switch = "".join(
        f'<a href="{BASE + l["prefix"] + path}" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" lang="{STR[l["code"]]["meta"]["html_lang"]}"'
        + (' aria-current="true"' if l["code"] == L.code else "") + f'>{E(STR[l["code"]]["meta"]["switch_name"])}</a>' for l in LANGS)
    doc = fill("head", lang=s["meta"]["html_lang"], title=E(pg["title"]), description=E(pg["description"]), robots=robots,
               canonical=abs_url(L.prefix, path), hreflang=alts, base=BASE, brand_name=E(CFG["brand"]),
               og_image=abs_url("", "img/og-1200x630.jpg"), og_alt=E(s["photos"][SITE["og_photo"]]), og_locale=s["meta"]["og_locale"],
               asset_v=ASSET_V, schema=schema(L, path, pg, trail, extra_schema))
    doc += fill("header", body_class=body_class, skip=E(L.ui["skip"]), home=L.url(), base=BASE, brand=E(CFG["brand"]), short=E(CFG["short_name"]),
                tagline=E(L.ui["tagline"]), nav_label=E(L.ui["nav_label"]), nav_items=nav_items(L, active),
                lang_label=E(L.ui["lang_label"]), switcher=switch, menu=E(L.ui["menu"]),
                wa=wa(L, "header", short=True, cls=" btn-sm hdr-wa"))
    doc += '<main id="main">\n'
    if len(trail) > 1:
        doc += crumbs(L, trail)
    doc += body
    sl = "\n".join(f'        <li><a href="{L.url(SVC[k]["slug"])}">{E(L.s["services"][k]["name"])}</a></li>' for k in SVC)
    cl = "\n".join(f'        <li><a href="{L.url(p)}">{E(L.ui["nav"][n])}</a></li>' for n, p in (("home", ""), ("about", "about/"), ("contact", "contact/")))
    doc += fill("footer", base=BASE, brand=E(CFG["brand"]), about=E(L.ui["footer_about"]), legal_name=E(CFG["name"]),
                reg_label=E(L.ui["reg_label"]), reg_no=E(CFG["registration_no"]), services_h=E(L.ui["footer_services"]), service_links=sl,
                company_h=E(L.ui["footer_company"]), company_links=cl, visit_h=E(L.ui["footer_visit"]), address=E(CFG["address_display"]),
                hours_label=E(L.ui["hours_label"]), hours=E(L.ui["hours_text"]), wa_href=E(wa_href(L)), phone=E(CFG["phone_display"]),
                phone_e164=CFG["phone_e164"], call_short=E(L.ui["call_short"]), email=E(CFG["email"]), maps_url=E(CFG["maps_url"]),
                map_open=E(L.ui["map_open"]), facebook_url=E(CFG["facebook_url"]), facebook=E(L.ui["facebook"]), year=YEAR,
                rights=E(L.ui["rights"]), credit_url=E(CFG["credit_url"]), credit=E(CFG["credit"]),
                sticky=fill("sticky", wa=wa(L, "mobile_bar", cls=" dock-wa"), tel=tel(L, "mobile_bar", short=True, cls=" dock-tel")))
    PAGES.append((L.prefix + path, doc))


def crumbs(L, trail):
    items = "".join(f'<li aria-current="page">{E(n)}</li>' if i == len(trail) - 1 else f'<li><a href="{L.url(p)}">{E(n)}</a></li>'
                    for i, (n, p) in enumerate(trail))
    return '<div class="wrap">' + fill("crumbs", label=E(L.ui["breadcrumb_label"]), items=items) + "</div>\n"


def faq_block(L, faq):
    items = "\n".join(f'      <details><summary>{E(q["q"])}</summary><p>{E(q["a"])}</p></details>' for q in faq)
    return fill("faq", h2=E(L.ui["faq_h2"]), items=items)


def cta(L, place, key="general", topic=""):
    return fill("cta_band", kicker=E(L.ui["cta_kicker"]), h2=E(L.ui["cta_h2"]), p=E(L.ui["cta_p"]),
                wa=wa(L, place, key, topic), tel=tel(L, place, cls=" btn-ghost"))


def tile(L, k):
    sv, c = L.s["services"][k], SVC[k]
    media = img_tag(L, c["tile_photo"], "(max-width: 760px) 50vw, 300px") if c.get("tile_photo") else icon_art(c["icon"])
    return fill("service_tile", href=L.url(c["slug"]), media=media, name=E(sv["name"]), sub=E(sv["tile"]))


STEP_ICONS = ["whatsapp", "scan", "quote", "drive"]


def steps(L):
    return '<ol class="isteps">' + "".join(fill("step_icon", icon=icon_art(STEP_ICONS[i]), n=i + 1, t=E(st["t"]), d=E(st["d"]))
                                             for i, st in enumerate(L.s["steps4"])) + "</ol>"


def carousel(L, keys, label):
    n = len(keys)
    items = "".join(f'<figure class="car-slide" role="group" aria-roledescription="slide" aria-label="{i + 1} / {n}">'
                    f'{img_tag(L, k, "(max-width: 760px) 86vw, 400px")}<figcaption>{E(L.s["photo_caps"][k])}</figcaption></figure>'
                    for i, k in enumerate(keys))
    dots = "".join(f'<button class="car-dot" type="button" aria-label="{E(L.ui["car_dot"].replace("{n}", str(i + 1)))}"></button>' for i in range(n))
    return fill("carousel", label=E(label), items=items, dots=dots, prev=E(L.ui["car_prev"]), next=E(L.ui["car_next"]))


def reel_wall(L):
    out = []
    for r in SITE["reels"]:
        land = r["shape"] == "landscape"
        cap = L.s["reels"][r["id"]]
        out.append(fill("reel", shape=r["shape"], poster=f'{BASE}media/reel-{r["id"]}.jpg', mp4=f'{BASE}media/reel-{r["id"]}.mp4',
                        w=640 if land else 360, h=360 if land else 640, caption=E(cap), play=E(L.ui["reel_play"]),
                        time=f'{r["seconds"] // 60}:{r["seconds"] % 60:02d}'))
    return '<div class="reels">\n' + "\n".join(out) + "\n</div>"


def reviews(L, order=None):
    revs = SITE["reviews"]
    if order:
        revs = sorted(revs, key=lambda r: order.index(r["name"]) if r["name"] in order else 99)
    note = f'<p class="small muted">{E(L.ui["review_lang_note"])}</p>' if L.ui.get("review_lang_note") else ""
    return '<div class="reviews">' + "".join(fill("review", text=E(r["text"]), name=E(r["name"])) for r in revs) + "</div>" + note


def rating_badge(L, place):
    return (f'<a class="rating" href="{E(CFG["maps_url"])}" target="_blank" rel="noopener" data-cta="google_reviews_{place}">'
            f'<span class="stars" aria-hidden="true">★★★★<span class="half">★</span></span><span>{E(L.ui["rating"])}</span></a>')


def map_block(L, place):
    return fill("map_facade", embed=E(CFG["maps_embed"]), map_title=E(CFG["brand"]), map_load=E(L.ui["map_load"]), place=place,
                brand=E(CFG["brand"]), address=E(CFG["address_display"]), hours_label=E(L.ui["hours_label"]), hours=E(L.ui["hours_text"]),
                wa=wa(L, place), tel=tel(L, place, cls=" btn-ghost"), maps_url=E(CFG["maps_url"]), map_open=E(L.ui["map_open"]),
                email=E(CFG["email"]), email_label=E(L.ui["email"]), map_note=E(L.ui["map_note"]))


def models_list(L, only=None):
    ms = L.s["models"] if only is None else [L.s["models"][i] for i in only]
    return f'<h3>{E(L.ui["models_h3"])}</h3><ul class="chips">' + "".join(f"<li>{E(m)}</li>" for m in ms) + "</ul>"


def sections_html(secs):
    return "".join(f'<h2>{E(x["h2"])}</h2>' + "".join(f"<p>{E(p)}</p>" for p in x["p"]) for x in secs)


def sec_head(h2, hid, p=""):
    return f'<h2 id="{hid}">{E(h2)}</h2>' + (f'<p class="lead">{E(p)}</p>' if p else "")


# ------------------------------------------------------------------ pages
def build_home(L):
    h = L.s["pages"]["home"]
    tiles = "".join(tile(L, k) for k in SVC)
    body = f'''<section class="hero" aria-labelledby="h1">
  <div class="hero-bg" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div class="hero-art">{energy_flow(L.s["art"]["hero"])}{charge_bar(h["charge"])}</div>
    <div class="hero-txt">
      <h1 id="h1">{E(h["h1"])}</h1>
      <p class="hero-line">{E(h["tagline"])}</p>
      <div class="cta-row">{wa(L, "home_hero", cls=" btn-lg")}{tel(L, "home_hero", cls=" btn-ghost hide-sm")}</div>
      {rating_badge(L, "hero")}
    </div>
  </div>
</section>
<section class="sec sec-a" id="services" aria-labelledby="svc-h">
  <div class="wrap">{sec_head(h["services_h2"], "svc-h")}<div class="tiles">{tiles}</div></div>
</section>
<section class="sec sec-b" id="steps" aria-labelledby="steps-h">
  <div class="wrap">{sec_head(h["steps_h2"], "steps-h")}{steps(L)}</div>
</section>
<section class="sec sec-a" id="photos" aria-labelledby="ph-h">
  <div class="wrap">{sec_head(h["photos_h2"], "ph-h")}{carousel(L, SITE["carousel"], h["photos_h2"])}</div>
</section>
<section class="sec sec-b" id="reels" aria-labelledby="reels-h">
  <div class="wrap">{sec_head(h["reels_h2"], "reels-h", h["reels_p"])}{reel_wall(L)}
  <p class="more"><a class="btn btn-ghost" href="{E(CFG["facebook_url"])}" target="_blank" rel="noopener">{E(L.ui["more_reels"])}</a></p></div>
</section>
<section class="sec sec-a" id="reviews" aria-labelledby="rev-h">
  <div class="wrap">{sec_head(h["reviews_h2"], "rev-h")}{rating_badge(L, "reviews")}{reviews(L)}</div>
</section>
<section class="sec sec-b" id="visit" aria-labelledby="visit-h">
  <div class="wrap">{sec_head(h["visit_h2"], "visit-h")}{map_block(L, "home")}</div>
</section>
<section class="sec sec-a" id="about" aria-labelledby="about-h">
  <div class="wrap two">
    <div class="prose">{sec_head(h["about_h2"], "about-h")}{"".join(f"<p>{E(p)}</p>" for p in h["about"])}</div>
    <div class="prose">{models_list(L)}</div>
  </div>
</section>
{faq_block(L, h["faq"])}{cta(L, "home_bottom")}'''
    page(L, "", "home", "home", body, [(L.ui["nav"]["home"], "")], [faq_node(h["faq"])], body_class="home")


def build_service(L, k):
    c, sv, pg = SVC[k], L.s["services"][k], L.s["pages"][k]
    path = c["slug"]
    trail = [(L.ui["nav"]["home"], ""), (sv["name"], path)]
    hero = figure(L, c["hero"], eager=True, cls="ph-hero") if c.get("hero") else f'<div class="art-hero">{icon_art(c["icon"], L.s["art"].get(k, sv["name"]), big=True)}</div>'
    gal = ""
    ph = c.get("photos", [])
    if len(ph) >= 3:
        gal = f'<section class="sec sec-b" aria-labelledby="g-h"><div class="wrap"><h2 id="g-h">{E(L.ui["photo_label"])}</h2>{carousel(L, ph, sv["name"])}</div></section>'
    elif ph:
        gal = '<div class="side-ph">' + "".join(figure(L, p) for p in ph) + "</div>"
    models = ""
    if k in ("battery", "recon", "toyota", "inverter"):
        models = models_list(L, None if k != "toyota" else [0, 1, 2, 3, 4, 5])
    elif k == "honda":
        models = models_list(L, [6])
    rel = "".join(tile(L, o) for o in SVC if o != k)
    order = ["David"] if k == "honda" else None
    body = f'''<section class="phero" aria-labelledby="h1">
  <div class="wrap phero-grid">
    <div class="phero-txt">
      <h1 id="h1">{E(pg["h1"])}</h1>
      <p class="intro">{E(pg["intro"])}</p>
      <div class="cta-row">{wa(L, "service_" + k, "service", sv["name"])}{tel(L, "service_" + k, cls=" btn-ghost")}</div>
      {rating_badge(L, "service")}
    </div>
    <div class="phero-fig">{hero}</div>
  </div>
</section>
<section class="sec sec-a">
  <div class="wrap two">
    <div class="prose">{sections_html(pg["sections"])}</div>
    <aside class="prose aside">{models}{gal if gal.startswith('<div') else ""}</aside>
  </div>
</section>
{gal if gal.startswith('<section') else ""}
<section class="sec sec-b" aria-labelledby="rv-h"><div class="wrap"><h2 id="rv-h">{E(L.s["pages"]["home"]["reviews_h2"])}</h2>{reviews(L, order)}</div></section>
{faq_block(L, pg["faq"])}
<section class="sec sec-a" aria-labelledby="rel-h"><div class="wrap"><h2 id="rel-h">{E(L.ui["related_h2"])}</h2><div class="tiles tiles-sm">{rel}</div></div></section>
{cta(L, "service_" + k + "_bottom", "service", sv["name"])}'''
    svc = {"@type": "Service", "@id": abs_url(L.prefix, path) + "#service", "name": sv["name"], "serviceType": sv["name"],
           "description": pg["description"], "provider": {"@id": CFG["site_url"] + "#business"},
           "areaServed": {"@type": "City", "name": "Johor Bahru"}, "url": abs_url(L.prefix, path)}
    page(L, path, k, k, body, trail, [svc, faq_node(pg["faq"])], body_class="svc")


def build_about(L):
    pg = L.s["pages"]["about"]
    trail = [(L.ui["nav"]["home"], ""), (L.ui["nav"]["about"], "about/")]
    facts = [(L.ui["reg_label"], f'{CFG["name"]} ({CFG["registration_no"]})'), (L.ui["address_label"], CFG["address_display"]),
             (L.ui["hours_label"], L.ui["hours_text"])]
    dl = "".join(f"<dt>{E(a)}</dt><dd>{E(b)}</dd>" for a, b in facts)
    dl += (f'<dt>{E(L.ui["phone_label"])}</dt><dd><a href="{E(wa_href(L))}" target="_blank" rel="noopener" data-cta="whatsapp_about">{E(CFG["phone_display"])}</a></dd>'
           f'<dt>{E(L.ui["email_label"])}</dt><dd><a href="mailto:{CFG["email"]}" data-cta="email_about">{E(CFG["email"])}</a></dd>'
           f'<dt>Facebook</dt><dd><a href="{E(CFG["facebook_url"])}" target="_blank" rel="noopener">{E(L.ui["facebook"])}</a></dd>')
    figs = "".join(figure(L, p, eager=(i == 0)) for i, p in enumerate(SITE["about_photos"]))
    body = f'''<section class="phero" aria-labelledby="h1">
  <div class="wrap"><h1 id="h1">{E(pg["h1"])}</h1><p class="intro">{E(pg["intro"])}</p>
  <div class="cta-row">{wa(L, "about_top")}{tel(L, "about_top", cls=" btn-ghost")}</div>{rating_badge(L, "about")}</div>
</section>
<section class="sec sec-a"><div class="wrap"><div class="photo-row">{figs}</div></div></section>
<section class="sec sec-b"><div class="wrap two">
  <div class="prose">{sections_html(pg["sections"])}</div>
  <div class="prose"><h2>{E(pg["company_h2"])}</h2><dl class="facts">{dl}</dl></div>
</div></section>
{cta(L, "about_bottom")}'''
    page(L, "about/", "about", "about", body, trail)


def build_contact(L):
    pg = L.s["pages"]["contact"]
    trail = [(L.ui["nav"]["home"], ""), (L.ui["nav"]["contact"], "contact/")]
    body = f'''<section class="phero" aria-labelledby="h1">
  <div class="wrap"><h1 id="h1">{E(pg["h1"])}</h1><p class="intro">{E(pg["intro"])}</p>
  <div class="cta-row">{wa(L, "contact_top", cls=" btn-lg")}{tel(L, "contact_top", cls=" btn-ghost")}</div></div>
</section>
<section class="sec sec-a" id="contact"><div class="wrap">{map_block(L, "contact")}</div></section>
<section class="sec sec-b"><div class="wrap two">
  <div>{figure(L, "shopfront")}</div>
  <div class="prose"><dl class="facts">
    <dt>{E(L.ui["phone_label"])}</dt><dd><a href="{E(wa_href(L))}" target="_blank" rel="noopener" data-cta="whatsapp_contact_card">WhatsApp {E(CFG["phone_display"])}</a><br><a href="tel:{CFG["phone_e164"]}" data-cta="call_contact_card">{E(L.ui["call_short"])} {E(CFG["phone_display"])}</a></dd>
    <dt>{E(L.ui["email_label"])}</dt><dd><a href="mailto:{CFG["email"]}" data-cta="email_contact_card">{E(CFG["email"])}</a></dd>
    <dt>{E(L.ui["address_label"])}</dt><dd>{E(CFG["address_display"])}</dd>
    <dt>{E(L.ui["hours_label"])}</dt><dd>{E(L.ui["hours_text"])}</dd>
    <dt>Facebook</dt><dd><a href="{E(CFG["facebook_url"])}" target="_blank" rel="noopener">{E(L.ui["facebook"])}</a></dd>
  </dl>{rating_badge(L, "contact")}</div>
</div></section>'''
    page(L, "contact/", "contact", "contact", body, trail)


# ------------------------------------------------------------------ sitemap + llms.txt (written for the planned domain)
def all_paths():
    return [""] + [SVC[k]["slug"] for k in SVC] + ["about/", "contact/"]


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
    lines += [f"- [About]({live_url('', 'about/')})", f"- [Contact]({live_url('', 'contact/')})", "", "## Other languages", "",
              f"- Bahasa Melayu: {live_url('ms/')}", f"- 简体中文: {live_url('zh/')}", ""]
    (OUT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "assets").mkdir(parents=True)
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "site.js").write_text(JS, encoding="utf-8")
    build_images()
    for cfg in LANGS:
        L = Lang(cfg)
        build_home(L)
        for k in SVC:
            build_service(L, k)
        build_about(L)
        build_contact(L)
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
