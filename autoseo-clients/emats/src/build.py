#!/usr/bin/env python3
"""Build the EMATS site in English, Malay and Chinese.

    python3 autoseo-clients/emats/src/build.py

Business facts and the ONE WhatsApp number: config.json (key whatsapp_number).
Page order, photos, reels: data/site.json.
Every visible string and the WhatsApp prefills: strings/<lang>.json (same keys).
Shared parts (head, header, footer, WhatsApp button, sticky bar, service card,
reel facade, FAQ, CTA, breadcrumb, photo): templates/.
Output is fully rendered static HTML in site/ (English at the root, Malay in
ms/, Chinese in zh/). check.py runs at the end; a failed check stops the build.
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

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
SITE = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
LANGS = SITE["languages"]
STR = {l["code"]: json.loads((ROOT / "strings" / f"{l['code']}.json").read_text(encoding="utf-8")) for l in LANGS}
TPL = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / "templates").glob("*.html")}
OUT = ROOT / "site"
BASE = CFG["base_path"]
E = html.escape

WA_NUM = re.sub(r"\D", "", CFG.get("whatsapp_number") or "")
if CFG.get("whatsapp_number") and not re.fullmatch(r"\d{9,15}", CFG["whatsapp_number"]):
    raise SystemExit("config.json whatsapp_number: digits only with country code, e.g. 60123456789")

CSS = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
JS = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
ASSET_V = hashlib.sha256((CSS + JS).encode()).hexdigest()[:10]
PHOTO = {p["key"]: p for p in SITE["photos"]}
SVC = {s["key"]: s for s in SITE["services"]}
SIZES = {}
PAGES = []  # (path, html)
YEAR = date.today().year


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


# ------------------------------------------------------------------ WhatsApp (one switch: config.json whatsapp_number)
def wa(L, key="general", topic="", short=False, extra_cls=""):
    if WA_NUM:
        msg = L.s["prefills"][key].replace("{topic}", topic)
        href = f"https://wa.me/{WA_NUM}?text={quote(msg, safe='')}"
        label = L.ui["wa_cta_short" if short else "wa_cta"]
        return fill("wa_button", cls=extra_cls, href=E(href), attrs=' target="_blank" rel="noopener"', label=E(label))
    label = L.ui["wa_soon_short" if short else "wa_soon"]
    return fill("wa_button", cls=" is-soon" + extra_cls, href=E(L.url("contact/") + "#contact"),
                attrs=' aria-disabled="true"', label=E(label))


def tel(L, cls="btn-ghost"):
    """Secondary CTA: phone call. Empty phone in config = no button."""
    if not CFG.get("phone_e164"):
        return ""
    return (f'<a class="{cls} btn-tel" href="tel:{E(CFG["phone_e164"])}" data-part="tel">'
            f'{E(L.ui["call"].replace("{phone}", CFG["phone_display"]))}</a>')


def hours_line(L):
    if not CFG.get("hours"):
        return ""
    return f'<p class="hours" data-part="hours"><span class="mono">{E(L.ui["hours_label"])}</span> {E(L.ui["hours_text"])}</p>'


# ------------------------------------------------------------------ images
def build_images():
    dst = OUT / "img"
    dst.mkdir(parents=True, exist_ok=True)
    for key, p in PHOTO.items():
        im = Image.open(ROOT / "photos" / p["file"]).convert("RGB")
        stem = p["file"][:-5]
        big = im.copy()
        big.thumbnail((1200, 1200), Image.LANCZOS)
        big.save(dst / f"{stem}-1200.webp", "WEBP", quality=80)
        SIZES[key] = big.size
        small = im.copy()
        small.thumbnail((640, 640), Image.LANCZOS)
        small.save(dst / f"{stem}-640.webp", "WEBP", quality=76)
    # favicon: green chip on black
    for size, name in ((192, "favicon.png"), (180, "apple-touch-icon.png")):
        s = size / 32
        ic = Image.new("RGB", (size, size), (5, 10, 7))
        d = ImageDraw.Draw(ic)
        g = (34, 224, 122)
        d.rounded_rectangle([8 * s, 8 * s, 24 * s, 24 * s], radius=2.5 * s, outline=g, width=round(2 * s))
        d.rectangle([12.5 * s, 12.5 * s, 19.5 * s, 19.5 * s], fill=g)
        for v in (12, 16, 20):
            w = round(1.6 * s)
            d.line([v * s, 3 * s, v * s, 8 * s], fill=g, width=w)
            d.line([v * s, 24 * s, v * s, 29 * s], fill=g, width=w)
            d.line([3 * s, v * s, 8 * s, v * s], fill=g, width=w)
            d.line([24 * s, v * s, 29 * s, v * s], fill=g, width=w)
        ic.save(OUT / name)


def photo(L, key, n, sizes="(max-width: 760px) 100vw, 50vw", eager=False, cls=""):
    w, h = SIZES[key]
    stem = PHOTO[key]["file"][:-5]
    extra = ' fetchpriority="high"' if eager else ""
    cap = f"IMG_{n:02d}"
    return fill("photo", base=BASE, stem=stem, w=w, h=h, sizes=sizes, alt=E(L.s["photos"][key]),
                loading="eager" if eager else "lazy", extra=extra, cls=(" " + cls) if cls else "", cap=E(cap))


# ------------------------------------------------------------------ graphics (no fake photos: circuit art)
GLYPH = {
    "ecu": '<rect x="150" y="110" width="100" height="100" rx="8" class="g-chip"/><rect x="175" y="135" width="50" height="50" rx="4" class="g-core"/>',
    "abs": '<circle cx="200" cy="160" r="62" class="g-line"/><circle cx="200" cy="160" r="40" class="g-line"/><circle cx="200" cy="160" r="12" class="g-core"/>'
           + "".join(f'<circle cx="{200 + 51 * __import__("math").cos(a * 0.785):.1f}" cy="{160 + 51 * __import__("math").sin(a * 0.785):.1f}" r="4" class="g-core"/>' for a in range(8)),
    "cluster": '<path d="M110 200a90 90 0 0 1 180 0" class="g-line"/><path d="M200 200l45-55" class="g-line g-needle"/><circle cx="200" cy="200" r="9" class="g-core"/>',
    "modules": '<rect x="120" y="110" width="70" height="50" rx="6" class="g-chip"/><rect x="210" y="110" width="70" height="50" rx="6" class="g-chip"/><rect x="165" y="175" width="70" height="50" rx="6" class="g-chip"/>',
    "marine": '<path d="M200 95v120M170 120h60M140 175a60 60 0 0 0 120 0" class="g-line"/><circle cx="200" cy="90" r="10" class="g-line"/><path d="M90 245q27-16 55 0t55 0 55 0 55 0" class="g-line"/>',
}


def board_art(kind, label, hero=False):
    """Inline SVG circuit board with data pulses (cyan + green) running along the traces and amber LEDs."""
    traces = [
        "M0 60H90L120 90H150", "M0 260H80L110 230H150", "M400 70H310L280 100H250", "M400 250H320L290 220H250",
        "M200 0V60L185 75V110", "M200 320V260L215 245V210", "M0 160H150", "M400 160H250",
        "M0 20H40L60 40V90L80 110H150", "M400 20H360L340 40V95L320 115H250", "M0 300H50L70 280V230L90 210H150",
        "M400 300H350L330 280V225L310 205H250", "M140 0V40L160 60V110", "M260 320V280L240 260V210",
    ]
    paths = "".join(f'<path d="{d}" class="trace"/>' for d in traces)
    flows = "".join(f'<path d="{d}" class="flow f{(i + k) % 6}" pathLength="100"/>' for i, d in enumerate(traces) for k in ((0, 3) if hero else (0,)))
    pads = "".join(f'<circle cx="{x}" cy="{y}" r="5" class="pad"/>' for x, y in ((0, 60), (0, 260), (400, 70), (400, 250), (200, 0), (200, 320), (0, 160), (400, 160)))
    vias = "".join(f'<circle cx="{x}" cy="{y}" r="3.5" class="via{" led l" + str(n % 3) if n % 2 == 0 else ""}"/>'
                   for n, (x, y) in enumerate(((90, 60), (120, 90), (80, 260), (110, 230), (310, 70), (280, 100), (320, 250), (290, 220),
                                               (185, 75), (215, 245), (60, 40), (340, 40), (70, 280), (330, 280))))
    lbl = f'<text x="200" y="300" text-anchor="middle" class="g-lbl">{E(label)}</text>' if label else ""
    cls = "art art-hero anim" if hero else "art anim"
    return (f'<svg class="{cls}" viewBox="0 0 400 320" role="img" aria-label="{E(label)}">'
            f'{paths}{flows}{vias}{pads}{GLYPH[kind]}{lbl}</svg>')


def bit_stream():
    """Two rows of binary that flow across the hero graphic (CSS moves them; decorative)."""
    a = "".join("1" if (j * 5 + j // 3) % 3 else "0" for j in range(96))
    b = "".join("0" if (j * 7 + j // 2) % 4 else "1" for j in range(96))
    return f'<div class="bstream mono anim" aria-hidden="true"><span>{a}{a}</span><span>{b}{b}</span></div>'


BINARY = "\n".join(
    "".join("1" if (i * 7 + j * 13 + (i * j) % 5) % 3 == 0 else "0" for j in range(64)) for i in range(28))


def binary_bg():
    return f'<div class="binary" aria-hidden="true"><pre>{BINARY}</pre></div>'


# ------------------------------------------------------------------ schema
def business_node(L):
    node = {
        "@type": "AutoRepair", "@id": CFG["site_url"] + "#business", "name": CFG["name"], "legalName": CFG["name"],
        "alternateName": CFG["short_name"], "description": L.s["pages"]["home"]["description"],
        "url": abs_url(L.prefix), "image": abs_url("", "img/" + PHOTO[SITE["og_photo"]]["file"][:-5] + "-1200.webp"),
        "logo": abs_url("", "favicon.png"),
        "identifier": {"@type": "PropertyValue", "propertyID": "SSM registration no.", "value": CFG["registration_no"]},
        "areaServed": [{"@type": "City", "name": CFG["city"]}, {"@type": "Country", "name": CFG["country"]}],
        "sameAs": [CFG["facebook_url"]],
        "knowsLanguage": [STR[l["code"]]["meta"]["schema_lang"] for l in LANGS],
    }
    if CFG.get("phone_e164") or WA_NUM:
        node["telephone"] = CFG.get("phone_e164") or "+" + WA_NUM
    if CFG.get("hours"):
        node["openingHoursSpecification"] = [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": [f"https://schema.org/{d}" for d in h["days"]],
             "opens": h["opens"], "closes": h["closes"]} for h in CFG["hours"]]
    return node


def crumbs_node(L, trail):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(L.prefix, p)} for i, (n, p) in enumerate(trail)]}


def faq_node(faq):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in faq]}


def schema(L, path, page, trail, extra=()):
    graph = [business_node(L),
             {"@type": "WebSite", "@id": CFG["site_url"] + "#website", "name": CFG["short_name"], "url": abs_url(""),
              "inLanguage": [STR[l["code"]]["meta"]["schema_lang"] for l in LANGS], "publisher": {"@id": CFG["site_url"] + "#business"}},
             {"@type": "WebPage", "@id": abs_url(L.prefix, path) + "#webpage", "url": abs_url(L.prefix, path), "name": page["title"],
              "description": page["description"], "inLanguage": L.s["meta"]["schema_lang"],
              "isPartOf": {"@id": CFG["site_url"] + "#website"}, "about": {"@id": CFG["site_url"] + "#business"}}]
    if len(trail) > 1:
        graph.append(crumbs_node(L, trail))
    graph += list(extra)
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    return f'  <script type="application/ld+json">{data.replace("</", "<\\/")}</script>'


# ------------------------------------------------------------------ shared page frame
def nav_items(L, active):
    ui = L.ui["nav"]
    sub = "".join(f'<li><a href="{L.url(SVC[k]["slug"])}"{" aria-current=page" if active == k else ""}>{E(L.s["services"][k]["name"])}</a></li>'
                  for k in SVC)
    items = [
        f'        <li><a href="{L.url()}"{" aria-current=page" if active == "home" else ""}>{E(ui["home"])}</a></li>',
        f'        <li class="has-sub"><details><summary>{E(ui["services"])}</summary><ul class="sub">{sub}</ul></details></li>',
        f'        <li><a href="{L.url("for-workshops/")}"{" aria-current=page" if active == "workshops" else ""}>{E(ui["workshops"])}</a></li>',
        f'        <li><a href="{L.url("about/")}"{" aria-current=page" if active == "about" else ""}>{E(ui["about"])}</a></li>',
        f'        <li><a href="{L.url("contact/")}"{" aria-current=page" if active == "contact" else ""}>{E(ui["contact"])}</a></li>',
    ]
    return "\n".join(items)


def page(L, path, key, active, body, trail, extra_schema=(), body_class=""):
    s, pg = L.s, L.s["pages"][key]
    robots = '  <meta name="robots" content="noindex,nofollow">\n' if CFG["preview"] else '  <meta name="robots" content="index,follow">\n'
    alts = "".join(f'  <link rel="alternate" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" href="{abs_url(l["prefix"], path)}">\n' for l in LANGS)
    alts += f'  <link rel="alternate" hreflang="x-default" href="{abs_url("", path)}">\n'
    switch = "".join(
        f'<a href="{BASE + l["prefix"] + path}" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" lang="{STR[l["code"]]["meta"]["html_lang"]}"'
        + (' aria-current="true"' if l["code"] == L.code else "") + f'>{E(STR[l["code"]]["meta"]["switch_name"])}</a>' for l in LANGS)
    og = abs_url("", "img/" + PHOTO[SITE["og_photo"]]["file"][:-5] + "-1200.webp")
    doc = fill("head", lang=s["meta"]["html_lang"], title=E(pg["title"]), description=E(pg["description"]), robots=robots,
               canonical=abs_url(L.prefix, path), hreflang=alts, base=BASE, brand_name=E(CFG["short_name"]), og_image=og,
               og_locale=s["meta"]["og_locale"], asset_v=ASSET_V, schema=schema(L, path, pg, trail, extra_schema))
    doc += fill("header", body_class=body_class, skip=E(L.ui["skip"]), home=L.url(), brand=E(CFG["short_name"]),
                tagline=E(L.s["services"]["ecu"]["name"] + " · " + CFG["city"]), nav_label=E(L.ui["nav_label"]),
                nav_items=nav_items(L, active), lang_label=E(L.ui["lang_label"]), switcher=switch, menu=E(L.ui["menu"]))
    doc += '<main id="main">\n'
    if len(trail) > 1:
        doc += crumbs(L, trail)
    doc += body
    rl = "\n".join(f'        <li><a href="{L.url(SVC[k]["slug"])}">{E(L.s["services"][k]["name"])}</a></li>' for k in SVC)
    cl = "\n".join(f'        <li><a href="{L.url(p)}">{E(L.ui["nav"][n])}</a></li>' for n, p in (("workshops", "for-workshops/"), ("about", "about/"), ("contact", "contact/")))
    doc += fill("footer", brand=E(CFG["short_name"]), about=E(L.ui["footer_about"]), legal_name=E(CFG["name"]),
                reg_label=E(L.ui["reg_label"]), reg_no=E(CFG["registration_no"]), city=E(STR[L.code]["meta"].get("city", CFG["city"])),
                country=E(STR[L.code]["meta"].get("country", CFG["country"])), repairs_h=E(L.ui["footer_repairs"]), repair_links=rl,
                company_h=E(L.ui["footer_company"]), company_links=cl, follow_h=E(L.ui["footer_follow"]),
                facebook_url=E(CFG["facebook_url"]), facebook=E(L.ui["facebook"]), wa=wa(L) + tel(L, "btn-ghost btn-block") + hours_line(L), year=YEAR,
                rights=E(L.ui["rights"]), credit_url=E(CFG["credit_url"]), credit=E(CFG["credit"]),
                sticky=fill("wa_sticky", button=wa(L, short=False)))
    PAGES.append((L.prefix + path, doc))


def crumbs(L, trail):
    items = []
    for i, (n, p) in enumerate(trail):
        if i == len(trail) - 1:
            items.append(f'<li aria-current="page">{E(n)}</li>')
        else:
            items.append(f'<li><a href="{L.url(p)}">{E(n)}</a></li>')
    return '<div class="wrap">' + fill("crumbs", label=E(L.ui["breadcrumb_label"]), items="".join(items)) + "</div>\n"


def faq_block(L, faq):
    items = "\n".join(f'      <details><summary>{E(q["q"])}</summary><p>{E(q["a"])}</p></details>' for q in faq)
    return fill("faq", h2=E(L.ui["faq_h2"]), items=items)


def cta(L, h2=None, key="workshop", topic=""):
    return fill("cta_band", kicker=E(L.ui["cta_kicker"]), h2=E(h2 or L.ui["cta_h2"]), p=E(L.ui["cta_p"]),
                wa=wa(L, key, topic) + tel(L), facebook_url=E(CFG["facebook_url"]), facebook=E(L.ui["facebook"]))


def card(L, k):
    sv = L.s["services"][k]
    return fill("service_card", href=L.url(SVC[k]["slug"]), code=E(sv["code"]), name=E(sv["name"]), text=E(sv["card"]), more=E(L.ui["read_more"]))


def reel_wall(L):
    """Reels from data/site.json "reels": self-hosted MP4 when has_mp4, else Facebook click-to-load."""
    out = []
    for i, r in enumerate(SITE["reels"], 1):
        url = f"https://www.facebook.com/reel/{r['id']}"
        embed = "https://www.facebook.com/plugins/video.php?href=" + quote(url, safe="") + "&show_text=false&autoplay=true&width=360"
        if r.get("has_mp4"):
            out.append(fill("reel_video", url=E(url), embed=E(embed), mp4=f"{BASE}media/reel-{r['id']}.mp4",
                            poster=f"{BASE}media/reel-{r['id']}.jpg", label=E(L.ui["reel_video_label"]),
                            play=E(L.ui["reel_video_play"]), n=f"{i:02d}"))
        else:
            out.append(fill("reel_facade", url=E(url), embed=E(embed), label=E(L.ui["reel_label"]), play=E(L.ui["reel_play"]), n=f"{i:02d}"))
    return '<div class="reels">\n' + "\n".join(out) + "\n</div>"


def steps_html(L, big=False):
    li = "".join(f'<li><span class="node mono">{i:02d}</span><h3>{E(st["t"])}</h3><p>{E(st["d"])}</p></li>' for i, st in enumerate(L.s["steps"], 1))
    return f'<ol class="trace-steps{" big" if big else ""} anim"><span class="trace-line" aria-hidden="true"></span>{li}</ol>'


def kh(kicker, h2, p="", hid=""):
    idattr = f' id="{hid}"' if hid else ""
    return (f'<p class="kicker mono">{E(kicker)}</p><h2{idattr}>{E(h2)}</h2>' + (f'<p class="lead">{E(p)}</p>' if p else ""))


def sections_html(sections):
    out = ""
    for sec in sections:
        out += f'<h2>{E(sec["h2"])}</h2>' + "".join(f"<p>{E(p)}</p>" for p in sec["p"])
        if sec.get("list"):
            out += '<ul class="ticks">' + "".join(f"<li>{E(x)}</li>" for x in sec["list"]) + "</ul>"
    return out


def service_schema(L, k, path):
    sv = L.s["services"][k]
    pg = L.s["pages"][k]
    return {"@type": "Service", "@id": abs_url(L.prefix, path) + "#service", "name": sv["name"], "serviceType": sv["name"],
            "description": pg["description"], "provider": {"@id": CFG["site_url"] + "#business"},
            "areaServed": [{"@type": "City", "name": CFG["city"]}, {"@type": "Country", "name": CFG["country"]}],
            "url": abs_url(L.prefix, path), "inLanguage": L.s["meta"]["schema_lang"]}


# ------------------------------------------------------------------ pages
def build_home(L):
    h = L.s["pages"]["home"]
    console = "".join(f'<li><span class="ok">✓</span> {E(c)}</li>' for c in h["console"])
    badges = "".join(f'<li>{E(b)}</li>' for b in h["badges"])
    body = f'''<section class="hero sec-black">
  {binary_bg()}
  <div class="wrap hero-grid">
    <div class="hero-txt">
      <p class="kicker mono">{E(h["kicker"])}</p>
      <h1>{E(h["h1"])}</h1>
      <p class="lead">{E(h["intro"])}</p>
      <ul class="badges mono">{badges}</ul>
      <div class="cta-row">{wa(L, "workshop")}{tel(L)}</div>
      <p class="more-link"><a href="{L.url("for-workshops/")}">{E(h["process_link"])} →</a></p>
    </div>
    <div class="hero-art">
      {board_art("ecu", "", hero=True)}
      {bit_stream()}
      <ol class="console mono" aria-hidden="true">{console}</ol>
    </div>
  </div>
</section>
<section class="sec sec-dark" id="services">
  <div class="wrap">
    {kh(h["services_kicker"], h["services_h2"], h["services_p"])}
    <div class="chip-grid feat">{"".join(card(L, k) for k in SVC)}</div>
  </div>
</section>
<section class="sec sec-paper">
  <div class="wrap">
    {kh(h["process_kicker"], h["process_h2"], h["process_p"])}
    {steps_html(L)}
    <p class="more-link"><a href="{L.url("for-workshops/")}">{E(h["process_link"])} →</a></p>
  </div>
</section>
<section class="sec sec-black">
  <div class="wrap">
    {kh(h["photos_kicker"], h["photos_h2"], h["photos_p"])}
    <div class="bench-grid">{"".join(photo(L, k, i, sizes="(max-width: 760px) 50vw, 25vw") for i, k in enumerate(SITE["home_photos"], 1))}</div>
  </div>
</section>
<section class="sec sec-dark">
  <div class="wrap">
    {kh(h["why_kicker"], h["why_h2"])}
    <div class="why-grid">{"".join(f'<div class="why"><span class="mono">0{i}</span><h3>{E(w["t"])}</h3><p>{E(w["d"])}</p></div>' for i, w in enumerate(h["why"], 1))}</div>
  </div>
</section>
<section class="sec sec-black" id="reels">
  <div class="wrap">
    {kh(h["reels_kicker"], h["reels_h2"], h["reels_p"])}
    {reel_wall(L)}
    <p class="note mono">{E(L.ui["reel_note"])}</p>
  </div>
</section>
'''
    body += faq_block(L, h["faq"]) + cta(L)
    page(L, "", "home", "home", body, [(L.ui["nav"]["home"], "")], [faq_node(h["faq"])], "home")


def inner_hero(L, pg, figure):
    return f'''<section class="phero sec-black">
  {binary_bg()}
  <div class="wrap phero-grid">
    <div>
      <p class="kicker mono">{E(pg["kicker"])}</p>
      <h1>{E(pg["h1"])}</h1>
      <p class="lead">{E(pg["intro"])}</p>
      <div class="cta-row">{{WA}}</div>
    </div>
    <div class="phero-fig">{figure}</div>
  </div>
</section>
'''


def side_panel(L, key, topic):
    li = "".join(f'<li><span class="mono">{i:02d}</span>{E(st["t"])}</li>' for i, st in enumerate(L.s["steps"], 1))
    return (f'<aside class="panel"><p class="kicker mono">{E(L.ui["cta_kicker"])}</p><ol class="mini-steps">{li}</ol>'
            f'{wa(L, key, topic)}{tel(L, "btn-ghost btn-block")}<p class="small"><a href="{L.url("for-workshops/")}">{E(L.ui["nav"]["workshops"])} →</a></p></aside>')


def build_service(L, k):
    sv, pg, cfg = L.s["services"][k], L.s["pages"][k], SVC[k]
    path = cfg["slug"]
    if cfg["hero"]:
        fig = photo(L, cfg["hero"], 1, sizes="(max-width: 760px) 100vw, 45vw", eager=True, cls="ph-hero")
    else:
        fig = '<figure class="ph ph-art">' + board_art(cfg["art"], sv["name"]) + f'<figcaption class="mono">{E(sv["code"])} · {E(sv["name"])}</figcaption></figure>'
    body = inner_hero(L, pg, fig).replace("{WA}", wa(L, "service", sv["topic"]) + tel(L))
    body += f'''<section class="sec sec-dark">
  <div class="wrap sheet">
    <div class="prose">{sections_html(pg["sections"])}</div>
    {side_panel(L, "service", sv["topic"])}
  </div>
</section>
'''
    if cfg["photos"]:
        body += ('<section class="sec sec-black"><div class="wrap"><div class="bench-row">'
                 + "".join(photo(L, p, i, sizes="(max-width: 760px) 100vw, 33vw") for i, p in enumerate(cfg["photos"], 2)) + "</div></div></section>\n")
    body += faq_block(L, pg["faq"])
    body += (f'<section class="sec sec-paper"><div class="wrap"><h2>{E(L.ui["related_h2"])}</h2>'
             f'<div class="chip-grid four">{"".join(card(L, o) for o in SVC if o != k)}</div></div></section>\n')
    body += cta(L, pg["cta_h2"], "service", sv["topic"])
    trail = [(L.ui["nav"]["home"], ""), (sv["name"], path)]
    page(L, path, k, k, body, trail, [service_schema(L, k, path), faq_node(pg["faq"])])


def build_workshops(L):
    pg = L.s["pages"]["workshops"]
    path = "for-workshops/"
    fig = photo(L, SITE["workshops_photos"][0], 1, sizes="(max-width: 760px) 100vw, 45vw", eager=True, cls="ph-hero")
    body = inner_hero(L, pg, fig).replace("{WA}", wa(L, "workshop") + tel(L))
    body += f'''<section class="sec sec-dark"><div class="wrap"><h2>{E(pg["steps_h2"])}</h2>{steps_html(L, big=True)}</div></section>
<section class="sec sec-paper"><div class="wrap two">
  <div><h2>{E(pg["include_h2"])}</h2><ul class="checklist">{"".join(f"<li>{E(x)}</li>" for x in pg["include"])}</ul></div>
  <div><h2>{E(pg["why_h2"])}</h2>{"".join(f"<p>{E(p)}</p>" for p in pg["why_p"])}</div>
</div></section>
<section class="sec sec-black"><div class="wrap"><div class="bench-row two-up">{photo(L, SITE["workshops_photos"][1], 2, sizes="(max-width: 760px) 100vw, 50vw")}<figure class="ph ph-art">{board_art("modules", L.s["services"]["modules"]["name"])}<figcaption class="mono">{E(L.ui["cta_kicker"])}</figcaption></figure></div></div></section>
'''
    body += faq_block(L, pg["faq"]) + cta(L, pg["cta_h2"])
    trail = [(L.ui["nav"]["home"], ""), (L.ui["nav"]["workshops"], path)]
    svc = {"@type": "Service", "@id": abs_url(L.prefix, path) + "#service", "name": pg["h1"], "serviceType": L.ui["cta_kicker"],
           "description": pg["description"], "provider": {"@id": CFG["site_url"] + "#business"},
           "areaServed": {"@type": "Country", "name": CFG["country"]}, "url": abs_url(L.prefix, path)}
    page(L, path, "workshops", "workshops", body, trail, [svc, faq_node(pg["faq"])])


def build_about(L):
    pg = L.s["pages"]["about"]
    path = "about/"
    fig = photo(L, SITE["about_photos"][0], 1, sizes="(max-width: 760px) 100vw, 45vw", eager=True, cls="ph-hero")
    body = inner_hero(L, pg, fig).replace("{WA}", wa(L) + tel(L))
    body += f'''<section class="sec sec-dark"><div class="wrap narrow prose">{sections_html(pg["sections"])}</div></section>
<section class="sec sec-black"><div class="wrap"><div class="bench-row">{"".join(photo(L, p, i, sizes="(max-width: 760px) 100vw, 33vw") for i, p in enumerate(SITE["about_photos"][1:], 2))}</div></div></section>
'''
    body += cta(L, pg["cta_h2"], "general")
    trail = [(L.ui["nav"]["home"], ""), (L.ui["nav"]["about"], path)]
    page(L, path, "about", "about", body, trail, [{"@type": "AboutPage", "url": abs_url(L.prefix, path), "about": {"@id": CFG["site_url"] + "#business"}}])


def build_contact(L):
    pg = L.s["pages"]["contact"]
    path = "contact/"
    wa_p = pg["wa_p"] if WA_NUM else pg["wa_soon_p"]
    body = f'''<section class="phero sec-black">
  {binary_bg()}
  <div class="wrap narrow">
    <p class="kicker mono">{E(pg["kicker"])}</p>
    <h1>{E(pg["h1"])}</h1>
    <p class="lead">{E(pg["intro"])}</p>
  </div>
</section>
<section class="sec sec-dark" id="contact">
  <div class="wrap contact-grid">
    <div class="ccard"><p class="mono kicker">01</p><h2>{E(pg["wa_h2"])}</h2><p>{E(wa_p)}</p>{wa(L)}{tel(L, "btn-ghost btn-block")}</div>
    <div class="ccard"><p class="mono kicker">02</p><h2>{E(pg["fb_h2"])}</h2><p>{E(pg["fb_p"])}</p><a class="btn-ghost" href="{E(CFG["facebook_url"])}" target="_blank" rel="noopener">{E(L.ui["facebook"])}</a></div>
    <div class="ccard"><p class="mono kicker">03</p><h2>{E(pg["loc_h2"])}</h2><p>{E(pg["loc_p"])}</p>{hours_line(L)}<p class="mono small">{E(CFG["name"])}<br>{E(L.ui["reg_label"])}: {E(CFG["registration_no"])}</p></div>
  </div>
</section>
'''
    trail = [(L.ui["nav"]["home"], ""), (L.ui["nav"]["contact"], path)]
    page(L, path, "contact", "contact", body, trail, [{"@type": "ContactPage", "url": abs_url(L.prefix, path), "about": {"@id": CFG["site_url"] + "#business"}}])


# ------------------------------------------------------------------ sitemap + llms (for the live domain later)
def all_paths():
    return [""] + [SVC[k]["slug"] for k in SVC] + ["for-workshops/", "about/", "contact/"]


def write_sitemap():
    today = date.today().isoformat()
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for l in LANGS:
        for p in all_paths():
            out += ["  <url>", f"    <loc>{live_url(l['prefix'], p)}</loc>", f"    <lastmod>{today}</lastmod>"]
            out += [f'    <xhtml:link rel="alternate" hreflang="{STR[x["code"]]["meta"]["html_lang"]}" href="{live_url(x["prefix"], p)}"/>' for x in LANGS]
            out += [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{live_url("", p)}"/>', "  </url>"]
    out.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(out) + "\n", encoding="utf-8")


def write_llms():
    en = STR["en"]
    lines = [f"# {CFG['short_name']} ({CFG['name']})", "",
             f"> {en['pages']['home']['description']}", "",
             f"- Registration: {CFG['registration_no']}", f"- Location: {CFG['city']}, {CFG['country']}",
             "- Customers: mainly car workshops (send-in service); car owners also welcome",
             "- How it works: diagnosis before quote; repair, not replace",
             f"- Facebook: {CFG['facebook_url']}"]
    if WA_NUM:
        lines.append(f"- WhatsApp: https://wa.me/{WA_NUM}")
    if CFG.get("phone_e164"):
        lines.append(f"- Phone: {CFG['phone_display']}")
    if CFG.get("hours"):
        lines.append(f"- Hours: {en['ui']['hours_text']}")
    lines += ["", "## Pages", ""]
    names = {"": en["ui"]["nav"]["home"], "for-workshops/": en["ui"]["nav"]["workshops"], "about/": en["ui"]["nav"]["about"], "contact/": en["ui"]["nav"]["contact"]}
    names.update({SVC[k]["slug"]: en["services"][k]["name"] for k in SVC})
    for p in all_paths():
        lines.append(f"- [{names[p]}]({live_url('', p)})")
    lines += ["", "## Other languages", "", f"- Bahasa Melayu: {live_url('ms/')}", f"- 简体中文: {live_url('zh/')}", ""]
    (OUT / "llms.txt").write_text("\n".join(lines), encoding="utf-8")


# ------------------------------------------------------------------ main
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
        build_workshops(L)
        build_about(L)
        build_contact(L)
    for path, doc in PAGES:
        f = OUT / path / "index.html"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(doc, encoding="utf-8")
    write_sitemap()
    write_llms()
    print(f"built {len(PAGES)} pages, WhatsApp {'ON (' + WA_NUM + ')' if WA_NUM else 'placeholder (config.json whatsapp_number is empty)'}")
    r = subprocess.run([sys.executable, str(ROOT / "src" / "check.py")])
    if r.returncode:
        raise SystemExit("check failed")


if __name__ == "__main__":
    main()
