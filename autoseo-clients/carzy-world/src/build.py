#!/usr/bin/env python3
"""Build the Carzy World Sdn Bhd site in English, Malay and Chinese.

    python3 autoseo-clients/carzy-world/src/build.py

Business facts: data/business.json. Page order, photos, clips: data/site.json.
Every visible string: strings/<lang>.json (same keys in each).
Shared parts (head, header, footer, mobile WhatsApp bar, page hero, trust strip,
service card, FAQ, CTA band, photo, video parts): templates/.
Output is fully rendered static HTML in site/ (English at the root, Malay in
ms/, Chinese in zh/). check.py runs at the end; a failed check stops the build.
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
BIZ = json.loads((ROOT / "data" / "business.json").read_text(encoding="utf-8"))
SITE = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
LANGS = SITE["languages"]
STR = {l["code"]: json.loads((ROOT / "strings" / f"{l['code']}.json").read_text(encoding="utf-8")) for l in LANGS}
TPL = {p.stem: p.read_text(encoding="utf-8") for p in (ROOT / "templates").glob("*.html")}
OUT = ROOT / "site"
BASE = BIZ["base_path"]
E = html.escape

CSS = (ROOT / "assets" / "site.css").read_text(encoding="utf-8")
JS = (ROOT / "assets" / "site.js").read_text(encoding="utf-8")
ASSET_V = hashlib.sha256((CSS + JS).encode()).hexdigest()[:10]
PHOTO = {p["key"]: p for p in SITE["photos"]}
SIZES = {}  # key -> (w, h), filled by build_images()
PAGES = []  # (path, html, lang)


def fill(tpl, **kw):
    out = TPL[tpl]
    for k, v in kw.items():
        out = out.replace("{{" + k + "}}", str(v))
    if "{{" in out:
        raise SystemExit(f"template {tpl}: unfilled placeholder near {out[out.find('{{'):out.find('{{') + 40]!r}")
    return out


def abs_url(prefix, path=""):
    return BIZ["site_url"] + prefix + path


def live_url(prefix, path=""):
    return BIZ["live_site_url"] + prefix + path


class Lang:
    def __init__(self, cfg):
        self.code, self.prefix = cfg["code"], cfg["prefix"]
        self.s = STR[self.code]
        self.ui = self.s["ui"]

    def url(self, path=""):
        return BASE + self.prefix + path

    def wa(self, key="general", topic=""):
        msg = self.s["prefills"][key].replace("{topic}", topic)
        return E(f"https://wa.me/{BIZ['whatsapp_number']}?text={quote(msg, safe='')}")

    def call_label(self):
        return E(self.ui["call_us"].replace("{phone}", BIZ["phone_display"]))


# ------------------------------------------------------------------ images
def build_images():
    """Copy each real photo plus a 640px-wide copy; make the header logo and icons."""
    dst = OUT / "img"
    dst.mkdir(parents=True, exist_ok=True)
    for key, p in PHOTO.items():
        src = ROOT / "photos" / p["file"]
        im = Image.open(src)
        SIZES[key] = im.size
        shutil.copy(src, dst / p["file"])
        if key == "logo":
            continue
        small = im.convert("RGB")
        small.thumbnail((640, 10000))
        small.save(dst / p["file"].replace(".webp", "-640.webp"), "WEBP", quality=78)
    logo = Image.open(ROOT / "photos" / PHOTO["logo"]["file"]).convert("RGBA")
    box = logo.convert("L").point(lambda v: 255 if v < 200 else 0).getbbox()
    crop = logo.crop((box[0] - 6, box[1] - 6, box[2] + 6, box[3] + 6))
    crop = crop.resize((300, round(300 * crop.height / crop.width)), Image.LANCZOS)
    head = Image.new("RGBA", (300, 100), (255, 255, 255, 0))
    head.paste(crop, (0, (100 - crop.height) // 2), crop)
    head.save(dst / "carzy-world-logo-header.webp", "WEBP", quality=90)
    sq = logo.convert("RGB")
    sq.resize((192, 192), Image.LANCZOS).save(OUT / "favicon.png")
    sq.resize((180, 180), Image.LANCZOS).save(OUT / "apple-touch-icon.png")


def photo(L, key, sizes="(max-width: 700px) 100vw, 50vw", eager=False, cls=""):
    w, h = SIZES[key]
    stem = PHOTO[key]["file"][:-5]
    extra = ' fetchpriority="high"' if eager else ""
    extra += f' class="{cls}"' if cls else ""
    return fill("photo", base=BASE, stem=stem, w=w, h=h, sizes=sizes, alt=E(L.s["photos"][key]),
                loading="eager" if eager else "lazy", extra=extra).strip()


# ------------------------------------------------------------------ schema
def hours_spec():
    return [{"@type": "OpeningHoursSpecification", "dayOfWeek": [f"https://schema.org/{d}" for d in h["days"]],
             "opens": h["opens"], "closes": h["closes"]} for h in BIZ["hours"]]


def business_node(L):
    return {
        "@type": "AutoRepair", "@id": BIZ["site_url"] + "#business", "name": BIZ["name"],
        "alternateName": BIZ["short_name"], "slogan": BIZ["tagline"], "description": L.s["schema"]["description"],
        "url": abs_url(L.prefix), "telephone": BIZ["phone_e164"], "email": BIZ["email"],
        "image": abs_url("", "img/" + PHOTO["shop-exterior"]["file"]), "logo": abs_url("", "img/" + PHOTO["logo"]["file"]),
        "address": {"@type": "PostalAddress", "streetAddress": BIZ["street"], "addressLocality": BIZ["city"],
                    "postalCode": BIZ["postcode"], "addressRegion": BIZ["state"], "addressCountry": BIZ["country_code"]},
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
        "hasMap": BIZ["google_listing_url"], "openingHoursSpecification": hours_spec(),
        "areaServed": {"@type": "City", "name": "Klang"},
        "identifier": {"@type": "PropertyValue", "propertyID": "SSM company no.", "value": BIZ["company_no"]},
        "sameAs": [BIZ["facebook_url"], BIZ["google_listing_url"], BIZ["maps_url"]],
        "availableLanguage": [STR[l["code"]]["meta"]["lang_name"] for l in LANGS],
    }


def website_node(L):
    return {"@type": "WebSite", "@id": BIZ["site_url"] + "#website", "name": BIZ["short_name"], "url": abs_url(""),
            "inLanguage": [STR[l["code"]]["meta"]["schema_lang"] for l in LANGS], "publisher": {"@id": BIZ["site_url"] + "#business"}}


def crumbs_node(L, crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": name, "item": abs_url(L.prefix, path)} for i, (path, name) in enumerate(crumbs)]}


def faq_node(L, faqs):
    return {"@type": "FAQPage", "inLanguage": L.s["meta"]["schema_lang"],
            "mainEntity": [{"@type": "Question", "name": f["q"], "acceptedAnswer": {"@type": "Answer", "text": f["a"]}} for f in faqs]}


def schema_tag(graph):
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return f'  <script type="application/ld+json">\n{data}\n  </script>'


# ------------------------------------------------------------------ shared blocks
def wa_icon():
    return TPL["wa_icon"].strip()


# ------------------------------------------------------------------ video components
SELF = {v["key"]: v for v in SITE["self_videos"]}
CLIPS = {c["id"]: c for c in SITE["embeds"]}
# One builder per platform: add a platform here once, then clips are one data entry each.
EMBED = {
    "facebook": lambda url: "https://www.facebook.com/plugins/video.php?href=" + quote(url, safe="") + "&show_text=false&autoplay=true&width=360",
    "youtube": lambda url: "https://www.youtube-nocookie.com/embed/" + url.rstrip("/").split("/")[-1].split("v=")[-1] + "?autoplay=1",
    "tiktok": lambda url: "https://www.tiktok.com/embed/v2/" + url.rstrip("/").split("/")[-1],
}


def media(L, path, file):
    """Page-relative link into media/ (files uploaded to the server by hand)."""
    return "../" * (L.prefix + path).count("/") + "media/" + file


def month(L, ym):
    y, m = ym.split("-")
    return L.ui["months"][int(m) - 1] + " " + y


def facade(L, path, clip):
    """Click-to-load tile. Portrait thumbs fill the 9:16 tile; a landscape thumb sits centred on a blurred copy of itself."""
    v = L.s["videos"][clip["id"]]
    tw, th = clip.get("thumb_w", 360), clip.get("thumb_h", 640)
    thumb = media(L, path, clip["thumb"])
    wide = tw > th
    dur = f'<span class="dur">{E(L.ui["seconds"].replace("{n}", str(clip["seconds"])))}</span>' if clip.get("seconds") else ""
    return fill("embed_facade", cls=" wide" if wide else "", url=E(clip["url"]), embed=E(EMBED[clip["platform"]](clip["url"])), title=E(v["title"]),
                play_clip=E(L.ui["play_clip"]), thumb=thumb, tw=tw, th=th, alt=E(v["caption"]), dur=dur,
                bg=f'<span class="facade-bg" style="background-image:url({thumb})" aria-hidden="true"></span>' if wide else "").strip()


def clip_card(L, path, clip, show_more=True):
    v = L.s["videos"][clip["id"]]
    tag = more = ""
    if clip["service"]:
        sv = L.s["services"][clip["service"]]
        tag = f'<span class="tag">{E(sv["short"])}</span>'
        if show_more:
            more = f' <a class="link" href="{L.url("services/" + clip["service"] + "/")}">{E(L.ui["see_service"])} →</a>'
    more += f' <a class="link fb-link" href="{E(clip["url"])}" target="_blank" rel="noopener">{E(L.ui["watch_fb"])} ↗</a>'
    meta = " · ".join(x for x in (E(month(L, clip["date"])) if clip.get("date") else "", tag) if x)
    return fill("clip_card", facade=facade(L, path, clip), meta=meta, title=E(v["title"]), caption=E(v["caption"]),
                wa=L.wa("service", v["topic"]), id=clip["id"], wa_icon=wa_icon(), ask_this=E(L.ui["ask_this"]), more=more).rstrip("\n")


def clip_strip(L, path, ids, show_more=True):
    cards = "\n".join(clip_card(L, path, CLIPS[i], show_more) for i in ids)
    return (f'        <div class="reels" role="region" aria-label="{E(L.ui["clip_aria"])}" tabindex="0">\n{cards}\n        </div>\n'
            f'        <p class="note">{E(L.ui["video_note"])} <a class="link" href="{E(SITE["facebook_videos_url"])}" target="_blank" rel="noopener">{E(L.ui["watch_more"])} →</a></p>\n')


def video_click(L, path, key, label, caption):
    v = SELF[key]
    return fill("video_click", poster=media(L, path, v["poster"]), label=E(label), src=media(L, path, v["file"]), caption=E(caption)).strip()


def video_node(L, key):
    v, t = SELF[key], L.s["videos"][key]
    return {"@type": "VideoObject", "name": t["title"], "description": t["caption"], "thumbnailUrl": abs_url("", "media/" + v["poster"]),
            "contentUrl": abs_url("", "media/" + v["file"]), "uploadDate": v["upload_date"], "duration": v["duration"],
            "inLanguage": L.s["meta"]["schema_lang"], "publisher": {"@id": BIZ["site_url"] + "#business"}}


# ------------------------------------------------------------------ shared blocks
def trust(L):
    ui = L.ui
    return fill("trust_strip", listing_url=E(BIZ["google_listing_url"]), read_reviews=E(ui["read_reviews"]), stars_aria=E(ui["stars_aria"]), rating_line=E(ui["rating_line"]),
                hours_short=E(ui["hours_short"]), location_short=E(ui["location_short"]), brands_short=E(ui["brands_short"])).rstrip("\n")


def page_hero(L, crumbs, eyebrow, h1, lead, cta_id, wa, side=""):
    links = [f'<a href="{L.url(p)}">{E(t)}</a>' for p, t in crumbs[:-1]] + [f'<span aria-current="page">{E(crumbs[-1][1])}</span>']
    return fill("page_hero", hero_cls=" has-side" if side else "", crumb_aria=E(L.ui["breadcrumb_aria"]), crumbs=" / ".join(links), eyebrow=E(eyebrow),
                h1=E(h1), lead=E(lead), cta_id=cta_id, wa_primary=wa, wa_icon=wa_icon(), whatsapp_now=E(L.ui["whatsapp_now"]),
                phone_e164=BIZ["phone_e164"], call_label=L.call_label(), trust=trust(L), side=f'        <div class="ph-side">{side}</div>' if side else "")


def cta_band(L, cta_id, wa=None):
    h = L.s["home"]
    return fill("cta_band", heading=E(h["cta_h2"]), text=E(h["cta_text"]), wa=wa or L.wa("general"), cta_id=cta_id, wa_icon=wa_icon(),
                whatsapp_now=E(L.ui["whatsapp_now"]), phone_e164=BIZ["phone_e164"], call_label=L.call_label(),
                discount_badge=E(L.ui["discount_badge"]), discount_terms=E(L.ui["discount_terms"]), wa_discount=L.wa("discount"))


def faq_block(L, faqs, heading, kicker=None, alt=False):
    items = "\n".join(f'          <details><summary>{E(f["q"])}</summary><p>{E(f["a"])}</p></details>' for f in faqs)
    return fill("faq_block", cls=" alt" if alt else "", kicker=E(kicker or L.s["home"]["faq_kicker"]), heading=E(heading), items=items)


def visual(L, path, meta, sizes="(max-width: 700px) 100vw, 33vw"):
    """The one image for a service: matching real photo, matching hosted media, or a branded icon tile."""
    v = meta["visual"]
    sv = L.s["services"][meta["slug"]]
    if v["type"] == "photo":
        return photo(L, v["key"], sizes)
    if v["type"] == "media":
        alt = L.s["videos"][v["alt_from"]]["title"]
        return f'<img src="{media(L, path, v["file"])}" width="{v["w"]}" height="{v["h"]}" alt="{E(alt)}" loading="lazy" decoding="async">'
    return fill("svc_graphic", name=E(sv["title"]), icon=TPL["icon_" + v["icon"]].strip()).strip()


def service_cards(L, path, skip=None):
    out = []
    for m in SITE["services"]:
        if m["slug"] == skip:
            continue
        sv = L.s["services"][m["slug"]]
        out.append(fill("service_card", url=L.url(f"services/{m['slug']}/"), visual=visual(L, path, m), title=E(sv["title"]), text=E(sv["card"]),
                        more=E(L.ui["more_details"])).rstrip("\n"))
    return '        <div class="svc-grid">\n' + "\n".join(out) + "\n        </div>\n"


def reviews_link(L):
    """No review cards on the site: the rating line plus a link to the reviews on Google Maps."""
    return (f'        <div class="cta-row"><a class="btn btn-outline-light" href="{E(BIZ["google_listing_url"])}" target="_blank" rel="noopener" data-cta="google_reviews">'
            f'{E(L.ui["read_reviews"])} ↗</a></div>\n')


def hours_table(L, cls="hours"):
    ui = L.ui
    rows = "".join(f'<tr><th scope="row">{E(ui["days"][k])}</th><td>{E(ui["times"][k])}</td></tr>' for k in ("mon_fri", "sat", "sun"))
    return f'        <table class="{cls}"><caption>{E(ui["hours_title"])}</caption>{rows}</table>'


def ticks(items):
    return '<ul class="ticks">' + "".join(f"<li>{E(i)}</li>" for i in items) + "</ul>"


def section(inner, alt="", narrow=False, sid=""):
    cls = "section" + (f" {alt}" if alt else "")
    ida = f' id="{sid}"' if sid else ""
    return f'    <section class="{cls}"{ida}>\n      <div class="wrap{" narrow" if narrow else ""}">\n{inner}      </div>\n    </section>\n'


def kh2(kicker, h2):
    return f'        <p class="kicker">{E(kicker)}</p>\n        <h2>{E(h2)}</h2>\n'


def visit_block(L, with_map=False):
    ui = L.ui
    left = (f'          <div class="visit-info">\n'
            f'            <p><b>{E(ui["address_label"])}</b><br><span class="addr">{E(BIZ["address_full"])}</span></p>\n'
            f'            <p><b>{E(ui["phone_label"])}</b><br><a class="link" href="{L.wa("general")}" target="_blank" rel="noopener" data-cta="whatsapp_visit">{E(BIZ["phone_display"])}</a></p>\n'
            f'            <p><b>{E(ui["email_label"])}</b><br><a class="link" href="mailto:{BIZ["email"]}" data-cta="email_visit">{E(BIZ["email"])}</a></p>\n'
            f'{hours_table(L)}\n'
            f'            <div class="cta-row">'
            + (f'<a class="btn btn-red btn-maps" href="{E(BIZ["google_listing_url"])}" target="_blank" rel="noopener" data-cta="google_listing_contact"><span aria-hidden="true">📍</span><span>{E(ui["find_on_maps"])}</span></a>' if with_map else "")
            + f'<a class="btn btn-dark" href="{E(BIZ["maps_url"])}" target="_blank" rel="noopener" data-cta="directions">{E(ui["directions"])}</a>'
            f'<a class="btn btn-wa" href="{L.wa("directions")}" target="_blank" rel="noopener" data-cta="whatsapp_directions">{wa_icon()}<span>{E(ui["whatsapp_us"])}</span></a></div>\n'
            f'          </div>\n')
    if with_map:
        right = (f'          <div class="map-box">\n            <iframe title="{E(ui["map_title"])}" src="{E(BIZ["map_embed"])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>\n'
                 f'            <p class="note"><a class="link" href="{E(BIZ["maps_url"])}" target="_blank" rel="noopener">{E(ui["open_maps"])} →</a> · Plus code {E(BIZ["plus_code"])}</p>\n          </div>\n')
    else:
        right = f'          <a class="visit-photo" href="{E(BIZ["maps_url"])}" target="_blank" rel="noopener">{photo(L, "shop-exterior")}</a>\n'
    return f'        <div class="split visit">\n{left}{right}        </div>\n'





def service_pills(L):
    pills = "".join(f'          <a class="pill-link" href="{L.url("services/" + m["slug"] + "/")}"><span aria-hidden="true">{m["icon"]}</span>{E(L.s["services"][m["slug"]]["title"])}</a>\n'
                    for m in SITE["services"])
    return f'        <div class="pill-grid">\n{pills}        </div>\n'


# ------------------------------------------------------------------ page shell
NAV = [("services/", "services"), ("#work", "work"), ("#reviews", "reviews"), ("about/", "about"), ("contact/", "contact")]


def page(L, path, title, description, body, graph_extra=(), current="", body_class="", cta=None, preload=""):
    s, ui = L.s, L.ui
    graph = [business_node(L), website_node(L)] + list(graph_extra)
    robots = '  <meta name="robots" content="noindex,nofollow">\n' if BIZ["preview"] else '  <meta name="robots" content="index,follow">\n'
    alts = "".join(f'  <link rel="alternate" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" href="{abs_url(l["prefix"], path)}">\n' for l in LANGS)
    alts += f'  <link rel="alternate" hreflang="x-default" href="{abs_url("", path)}">\n'
    lang_links = '<span class="sep" aria-hidden="true">|</span>'.join(
        f'<a href="{BASE + l["prefix"] + path}" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" lang="{STR[l["code"]]["meta"]["html_lang"]}"'
        + (' aria-current="true"' if l["code"] == L.code else "") + f'>{E(STR[l["code"]]["meta"]["switch_label"])}</a>' for l in LANGS)
    nav = "\n".join(f'        <a href="{L.url() + p if p.startswith("#") else L.url(p)}"' + (' aria-current="page"' if current == p else "")
                    + f'>{E(ui["nav"][k])}</a>' for p, k in NAV)
    doc = fill("head", lang=s["meta"]["html_lang"], title=E(title), description=E(description), robots=robots, canonical=abs_url(L.prefix, path),
               hreflang=alts, base=BASE, brand_name=E(BIZ["short_name"]), og_image=abs_url("", "img/" + PHOTO["shop-exterior"]["file"]),
               og_locale=s["meta"]["og_locale"], preload=preload, asset_v=ASSET_V, schema=schema_tag(graph))
    doc += fill("header", body_class=(body_class + " lang-" + L.code).strip(), skip=E(ui["skip"]), home_url=L.url(), home_aria=E(ui["home_aria"]),
                base=BASE, logo_alt=E(s["photos"]["logo"]), nav_aria=E(ui["nav_aria"]), nav_links=nav, lang_aria=E(ui["lang_aria"]),
                lang_links=lang_links, wa_general=L.wa("general"), wa_icon=wa_icon(), whatsapp_us=E(ui["whatsapp_us"]), menu=E(ui["menu"]))
    doc += body
    pages = [("", ui["nav"]["home"]), ("services/", ui["nav"]["services"]), ("about/", ui["nav"]["about"]), ("contact/", ui["nav"]["contact"])]
    doc += fill("footer", cta_band=cta if cta is not None else cta_band(L, "page"), name=E(BIZ["name"]), tagline=E(BIZ["tagline"]),
                company_label=E(ui["company_label"]), company_no=E(BIZ["company_no"]), facebook_url=E(BIZ["facebook_url"]), facebook=E(ui["facebook"]),
                listing_url=E(BIZ["google_listing_url"]), find_on_maps=E(ui["find_on_maps"]), read_reviews=E(ui["read_reviews"]), h_visit=E(ui["footer_visit"]), address=E(BIZ["address_full"]),
                wa_general=L.wa("general"), phone=E(BIZ["phone_display"]), phone_e164=BIZ["phone_e164"], call=E(ui["call"]), email=E(BIZ["email"]),
                hours_table=hours_table(L, "hours hours-footer"), h_services=E(ui["footer_services"]),
                footer_services="\n".join(f'        <a href="{L.url("services/" + m["slug"] + "/")}">{E(s["services"][m["slug"]]["short"])}</a>' for m in SITE["services"]),
                h_pages=E(ui["footer_pages"]), footer_pages="\n".join(f'        <a href="{L.url(p)}">{E(t)}</a>' for p, t in pages),
                year=date.today().year, credit_url=E(BIZ["credit_url"]), credit=E(ui["credit"]), wa_icon=wa_icon(), whatsapp_us=E(ui["whatsapp_us"]))
    PAGES.append((L.prefix + path, doc, L.code))


# ------------------------------------------------------------------ pages
def build_home(L):
    s, h, ui = L.s, L.s["home"], L.ui
    path = ""
    sig = SELF["signature"]
    preload = f'  <link rel="preload" as="image" href="{media(L, path, sig["poster"])}" fetchpriority="high">\n'
    body = fill("hero_video", poster=media(L, path, sig["poster"]), video_label=E(h["hero_video_label"]), src=media(L, path, sig["file"]),
                sound_on=E(ui["sound_on"]), sound_off=E(ui["sound_off"]), play=E(ui["play"]), pause=E(ui["pause"]), eyebrow=E(h["eyebrow"]),
                h1=E(h["h1"]), lead=E(h["hero_lead"]), wa=L.wa("general"), wa_icon=wa_icon(), whatsapp_now=E(ui["whatsapp_now"]),
                phone_e164=BIZ["phone_e164"], call_label=L.call_label(), listing_url=E(BIZ["google_listing_url"]), read_reviews=E(ui["read_reviews"]), stars_aria=E(ui["stars_aria"]),
                rating_line=E(ui["rating_line"]), discount_badge=E(ui["discount_badge"]), wa_discount=L.wa("discount"))
    body += f'    <div class="ribbon">\n      <div class="wrap">\n{trust(L)}\n      </div>\n    </div>\n'
    # signature story: the 190E restoration (self-hosted, click to play)
    w201 = h["work"]["w201"]
    body += section(f'        <div class="classic">\n          <div class="classic-video rv">{video_click(L, path, "classic190e", h["classic_video_label"], L.s["videos"]["classic190e"]["caption"])}</div>\n'
                    f'          <div class="rv">\n            <p class="kicker">{E(h["classic_kicker"])}</p>\n            <h2>{E(h["classic_h2"])}</h2>\n'
                    f'            <p class="section-lead">{E(h["classic_text"])}</p>\n            <p class="when-line">{E(w201["when"])} · {E(w201["title"])}</p>\n'
                    f'            <div class="cta-row"><a class="btn btn-wa" href="{L.wa("service", L.s["services"]["classic-continental-cars"]["prefill_topic"])}" target="_blank" rel="noopener" data-cta="whatsapp_home_classic">{wa_icon()}<span>{E(ui["whatsapp_now"])}</span></a>'
                    f'<a class="btn btn-outline-light" href="{L.url("services/classic-continental-cars/")}">{E(L.s["services"]["classic-continental-cars"]["short"])} →</a></div>\n'
                    f'          </div>\n        </div>\n', alt="s-classic", sid="story")
    # services: every tile shows that service (photo, hosted clip still or branded graphic)
    body += section(f'        <div class="sec-head rv">\n          <p class="kicker">{E(h["services_kicker"])}</p>\n          <h2>{E(h["services_h2"])}</h2>\n'
                    f'          <p class="section-lead">{E(h["lead"])}</p>\n        </div>\n' + service_cards(L, path)
                    + f'        <p class="note">{E(ui["brands_note"])} {E(ui["price_note"])}</p>\n', alt="s-services", sid="services")
    # reel wall
    body += section(f'        <div class="sec-head rv">\n          <p class="kicker">{E(h["reels_kicker"])}</p>\n          <h2>{E(h["reels_h2"])}</h2>\n'
                    f'          <p class="section-lead">{E(h["reels_lead"])}</p>\n        </div>\n'
                    + clip_strip(L, path, [c["id"] for c in SITE["embeds"]]), alt="s-reels", sid="videos")
    # recent works: real photos, card text says what the photo shows
    cards = "".join(f'          <a class="work-card rv" href="{L.url("services/" + w["service"] + "/")}"><span class="wc-img">{photo(L, w["photo"], "(max-width: 700px) 80vw, 33vw")}</span>'
                    f'<span class="wc-body"><h3>{E(h["works"][w["key"]]["title"])}</h3><span>{E(h["works"][w["key"]]["text"])}</span></span></a>\n' for w in SITE["works"])
    also = "".join(f'<li><b>{E(h["work"][k]["title"])}</b>' + (f' · {E(h["work"][k]["when"])}' if h["work"][k]["when"] != h["work"]["dmax"]["when"] else "") + f': {E(h["work"][k]["text"])}</li>' for k in SITE["works_also"])
    body += section(f'        <div class="sec-head rv">\n          <p class="kicker">{E(h["works_kicker"])}</p>\n          <h2>{E(h["works_h2"])}</h2>\n'
                    f'          <p class="section-lead">{E(h["works_lead"])}</p>\n        </div>\n        <div class="works">\n{cards}        </div>\n'
                    f'        <div class="also rv"><h3>{E(h["works_also"])}</h3><ul>{also}</ul></div>\n', alt="s-works", sid="work")
    # the man in the suit
    body += section(f'        <div class="suit-band rv">\n          <p class="kicker">{E(h["suit_kicker"])}</p>\n          <h2>{E(h["suit_h2"])}</h2>\n'
                    f'          <p class="section-lead">{E(h["suit_text"])}</p>\n          <a class="link" href="{L.url("about/")}">{E(ui["nav"]["about"])} →</a>\n        </div>\n', alt="s-suit")
    # reviews
    body += section(f'        <div class="reviews-head rv">\n          <p class="big-score"><span>5.0</span><span class="stars" aria-label="{E(ui["stars_aria"])}">★★★★★</span><span class="bs-sub">19 · Google</span></p>\n'
                    f'          <div>\n            <p class="kicker">{E(h["reviews_kicker"])}</p>\n            <h2>{E(h["reviews_h2"])}</h2>\n'
                    f'            <p class="section-lead">{E(h["reviews_lead"])}</p>\n' + reviews_link(L) + '          </div>\n        </div>\n', alt="s-reviews", sid="reviews")
    body += section(f'        <div class="sec-head rv">\n          <p class="kicker">{E(h["visit_kicker"])}</p>\n          <h2>{E(h["visit_h2"])}</h2>\n'
                    f'          <p class="section-lead">{E(h["visit_text"])}</p>\n        </div>\n' + visit_block(L), alt="s-visit", sid="visit")
    faqs = s["faqs"][:SITE["home_faq_count"]]
    body += faq_block(L, faqs, h["faq_h2"], alt=True)
    page(L, path, h["title"], h["description"], body, graph_extra=[faq_node(L, faqs), video_node(L, "signature"), video_node(L, "classic190e")],
         body_class="home", cta=cta_band(L, "home"), preload=preload)


def build_services(L):
    s, ui, sp = L.s, L.ui, L.s["services_page"]
    crumbs = [("", ui["nav"]["home"]), ("services/", ui["nav"]["services"])]
    body = page_hero(L, crumbs, sp["eyebrow"], sp["h1"], sp["lead"], "services", L.wa("booking"))
    body += section(f'        <h2>{E(sp["list_h2"])}</h2>\n' + service_cards(L, "services/") + f'        <p class="note center">{E(ui["price_note"])}</p>\n', alt="tint-a")
    body += section(kh2(s["home"]["reels_kicker"], s["home"]["reels_h2"]) + clip_strip(L, "services/", [c["id"] for c in SITE["embeds"] if c["service"]]), alt="dark")
    page(L, "services/", sp["title"], sp["description"], body, graph_extra=[crumbs_node(L, crumbs)], current="services/", cta=cta_band(L, "services"))

    for m in SITE["services"]:
        sv = s["services"][m["slug"]]
        path = f"services/{m['slug']}/"
        cid = "svc_" + m["slug"].replace("-", "_")
        wa = L.wa("service", sv["prefill_topic"])
        crumbs_p = crumbs + [(path, sv["short"])]
        clips = m["clips"]
        hv = m.get("hero_video")
        if hv:
            side = video_click(L, path, hv, L.s["home"]["classic_video_label"], L.s["videos"][hv]["caption"])
            rest = clips
        else:
            rest = clips[1:]
            side = (f'<figure class="clip-solo">{facade(L, path, CLIPS[clips[0]])}<figcaption>{E(L.s["videos"][clips[0]]["caption"])}</figcaption></figure>'
                    if clips else f'<figure class="side-photo svc-side">{visual(L, path, m, "(max-width: 860px) 300px, 340px")}</figure>')
        body = page_hero(L, crumbs_p, sp["eyebrow"], sv["h1"], sv["intro"], cid, wa, side=side)
        inner = (f'        <div class="split">\n          <div>\n            <h2>{E(sv["covers_h2"])}</h2>\n            {ticks(sv["covers"])}\n          </div>\n'
                 f'          <div>\n            <h2>{E(sv["signs_h2"])}</h2>\n            {ticks(sv["signs"])}\n          </div>\n        </div>\n'
                 f'        <p class="section-lead">{E(sv["body"])}</p>\n        <p class="note">{E(ui["brands_note"])} {E(ui["price_note"])}</p>\n')
        body += section(inner, alt="tint-a")
        if rest:
            body += section(kh2(s["home"]["reels_kicker"], sv["title"]) + clip_strip(L, path, rest, show_more=False), alt="dark")
        body += faq_block(L, sv["faqs"], sp["faq_h2"].replace("{name}", sv["short"]))
        body += section(kh2(ui["related_kicker"], ui["related_h2"]) + service_cards(L, path, skip=m["slug"]), alt="tint-b")
        service = {"@type": "Service", "name": sv["title"], "serviceType": sv["title"], "description": sv["intro"],
                   "provider": {"@id": BIZ["site_url"] + "#business"}, "areaServed": {"@type": "City", "name": "Klang"}, "url": abs_url(L.prefix, path)}
        page(L, path, sv["meta_title"] + s["meta"]["title_suffix"], sv["meta_description"], body,
             graph_extra=[service, crumbs_node(L, crumbs_p), faq_node(L, sv["faqs"])] + ([video_node(L, hv)] if hv else []), current="services/", cta=cta_band(L, cid, wa))


def build_about(L):
    s, ui, ap = L.s, L.ui, L.s["about_page"]
    path = "about/"
    crumbs = [("", ui["nav"]["home"]), (path, ui["nav"]["about"])]
    body = page_hero(L, crumbs, ap["eyebrow"], ap["h1"], ap["lead"], "about", L.wa("general"),
                     side=f'<figure class="side-photo">{photo(L, "shop-exterior", eager=True)}</figure>')
    story = "".join(f"            <p>{E(p)}</p>\n" for p in ap["paras"])
    body += section(f'        <div class="split">\n          <div>\n            <h2>{E(ap["story_h2"])}</h2>\n{story}'
                    f'            <h3>{E(ap["video_h2"])}</h3>\n            <p>{E(ap["video_text"])}</p>\n          </div>\n'
                    f'          <div class="classic-video">{video_click(L, path, "signature", s["home"]["hero_video_label"], s["videos"]["signature"]["caption"])}</div>\n        </div>\n', alt="tint-a")
    vals = "".join(f'          <div class="card"><h3>{E(v["title"])}</h3><p>{E(v["text"])}</p></div>\n' for v in ap["values"])
    body += section(f'        <h2>{E(ap["values_h2"])}</h2>\n        <div class="cards cards-four">\n{vals}        </div>\n')
    body += section(kh2(s["home"]["reviews_kicker"], s["home"]["reviews_h2"]) + f'        <p class="section-lead">{E(s["home"]["reviews_lead"])}</p>\n' + reviews_link(L), alt="tint-b")
    details = (f'        <h2>{E(ap["company_h2"])}</h2>\n        <dl class="facts">\n'
               f'          <dt>{E(BIZ["name"])}</dt><dd>{E(ui["company_label"])} {E(BIZ["company_no"])}</dd>\n'
               f'          <dt>{E(ui["address_label"])}</dt><dd>{E(BIZ["address_full"])}</dd>\n'
               f'          <dt>{E(ui["phone_label"])}</dt><dd>{E(BIZ["phone_display"])}</dd>\n'
               f'          <dt>{E(ui["email_label"])}</dt><dd>{E(BIZ["email"])}</dd>\n        </dl>\n')
    body += section(details, narrow=True)
    page(L, path, ap["title"], ap["description"], body, graph_extra=[crumbs_node(L, crumbs), video_node(L, "signature")], current="about/", cta=cta_band(L, "about"))


def build_contact(L):
    ui, cp = L.ui, L.s["contact_page"]
    crumbs = [("", ui["nav"]["home"]), ("contact/", ui["nav"]["contact"])]
    body = page_hero(L, crumbs, cp["eyebrow"], cp["h1"], cp["lead"], "contact", L.wa("general"))
    ways = [(L.wa("general"), ' target="_blank" rel="noopener"', "whatsapp_contact_card", "💬", "WhatsApp", BIZ["phone_display"], cp["whatsapp_text"]),
            (f'tel:{BIZ["phone_e164"]}', "", "call_contact_card", "📞", ui["call"], BIZ["phone_display"], cp["call_text"]),
            (f'mailto:{BIZ["email"]}', "", "email_contact_card", "✉️", ui["email_us"], BIZ["email"], cp["email_text"])]
    cards = "".join(f'          <a class="card way" href="{href}"{tgt} data-cta="{cta}"><span class="svc-icon" aria-hidden="true">{ic}</span><h3>{E(t)}</h3>'
                    f'<p class="way-value">{E(v)}</p><p>{E(d)}</p></a>\n' for href, tgt, cta, ic, t, v, d in ways)
    body += section(f'        <h2>{E(cp["ways_h2"])}</h2>\n        <div class="cards cards-three">\n{cards}        </div>\n', alt="tint-a")
    body += section(f'        <h2>{E(cp["find_h2"])}</h2>\n' + visit_block(L, with_map=True))
    page(L, "contact/", cp["title"], cp["description"], body, graph_extra=[crumbs_node(L, crumbs)], current="contact/", cta=cta_band(L, "contact"))


# ------------------------------------------------------------------ extras
def page_paths():
    return [""] + ["services/"] + [f"services/{m['slug']}/" for m in SITE["services"]] + ["about/", "contact/"]


def build_sitemap():
    """Written for the planned domain, ready for move day. Not linked from anywhere while previewing."""
    out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for cfg in LANGS:
        for p in page_paths():
            out += ["  <url>", f"    <loc>{live_url(cfg['prefix'], p)}</loc>", f"    <lastmod>{date.today().isoformat()}</lastmod>"]
            out += [f'    <xhtml:link rel="alternate" hreflang="{STR[l["code"]]["meta"]["html_lang"]}" href="{live_url(l["prefix"], p)}"/>' for l in LANGS]
            out += [f'    <xhtml:link rel="alternate" hreflang="x-default" href="{live_url("", p)}"/>', "  </url>"]
    out.append("</urlset>")
    (OUT / "sitemap.xml").write_text("\n".join(out) + "\n", encoding="utf-8")


def build_llms():
    en = STR["en"]
    t = en["llms"]
    out = [f"# {BIZ['name']}", "", f"> {BIZ['tagline']}. {t['summary']}", "",
           f"- Address: {BIZ['address_full']}", f"- Plus code: {BIZ['plus_code']}", f"- Phone and WhatsApp: {BIZ['phone_display']} (https://wa.me/{BIZ['whatsapp_number']})",
           f"- Email: {BIZ['email']}", f"- {t['hours']}: Monday to Friday 10:00 to 19:00, Saturday 10:00 to 16:30, Sunday closed",
           f"- Company no.: {BIZ['company_no']}", f"- {t['reviews']}", f"- Google Business listing: {BIZ['google_listing_url']}", f"- Google Maps: {BIZ['maps_url']}", f"- Facebook: {BIZ['facebook_url']}",
           f"- {t['offer']}", "", f"## {t['services']}", ""]
    out += [f"- [{en['services'][m['slug']]['title']}]({live_url('', 'services/' + m['slug'] + '/')}): {en['services'][m['slug']]['intro']}" for m in SITE["services"]]
    out += ["", f"## {t['pages']}", ""]
    for cfg in LANGS:
        s = STR[cfg["code"]]
        out.append(f"- {s['meta']['lang_name']}: [{s['ui']['nav']['home']}]({live_url(cfg['prefix'])}), [{s['ui']['nav']['services']}]({live_url(cfg['prefix'], 'services/')}), "
                   f"[{s['ui']['nav']['about']}]({live_url(cfg['prefix'], 'about/')}), [{s['ui']['nav']['contact']}]({live_url(cfg['prefix'], 'contact/')})")
    (OUT / "llms.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    build_images()
    for cfg in LANGS:
        L = Lang(cfg)
        build_home(L)
        build_services(L)
        build_about(L)
        build_contact(L)
    for path, doc, _ in PAGES:
        f = OUT / (path + "index.html")
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(doc, encoding="utf-8")
    (OUT / "assets").mkdir(exist_ok=True)
    (OUT / "assets" / "site.css").write_text(CSS, encoding="utf-8")
    (OUT / "assets" / "site.js").write_text(JS, encoding="utf-8")
    build_sitemap()
    build_llms()
    print(f"built {len(PAGES)} pages into {OUT}")
    r = subprocess.run([sys.executable, str(ROOT / "src" / "check.py")])
    if r.returncode:
        print("BUILD STOPPED: pre-upload check failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
