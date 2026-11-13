#!/usr/bin/env python3
"""Checks for the built Hybrid World Specialist site. Exit code 1 on any problem."""
import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import live_mode  # noqa: E402
ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
SITE = live_mode.apply(CFG, ROOT)
BASE = CFG["base_path"]
WA = CFG["whatsapp_number"]
SITEJ = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
REVIEW_TEXT = [r["text"] for r in SITEJ["reviews"]]
errors = []


def err(m):
    errors.append(m)


# 1. blocklist on built files and on every source file shipped or used for text
rules = []
for line in (ROOT / "data" / "blocklist.txt").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    rules.append(re.compile(line[3:], re.I) if line.startswith("re:") else re.compile(re.escape(line), re.I))
scan = [p for p in SITE.rglob("*") if p.suffix in (".html", ".css", ".js", ".txt", ".xml")]
scan += list((ROOT / "templates").glob("*.html")) + list((ROOT / "strings").glob("*.json")) + list((ROOT / "assets").glob("*")) + [ROOT / "config.json"]
scan += list((ROOT / "data" / "articles").glob("*.json"))
for p in scan:
    t = p.read_text(encoding="utf-8")
    for r in rules:
        m = r.search(t)
        if m:
            err(f"blocklist {r.pattern!r} in {p.relative_to(ROOT)}: ...{t[max(0, m.start() - 40):m.end() + 40]!r}")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links, self.imgs, self.parts, self.ld = [], [], set(), []
        self._ld = False
        self.robots = None
        self.hreflang = 0
        self.imgs_no_size = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "img":
            self.imgs.append(a.get("src"))
            if not (a.get("width") and a.get("height") and a.get("alt")):
                self.imgs_no_size.append(a.get("src"))
        if a.get("data-part"):
            self.parts.add(a["data-part"])
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld = True
        if tag == "meta" and a.get("name") == "robots":
            self.robots = a.get("content")
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"):
            self.hreflang += 1
        if tag == "link" and a.get("rel") == "stylesheet":
            self.links.append(a["href"])
        if tag == "script" and a.get("src"):
            self.links.append(a["src"])

    def handle_data(self, d):
        if self._ld:
            self.ld.append(d)

    def handle_endtag(self, tag):
        if tag == "script":
            self._ld = False


en = json.loads((ROOT / "strings" / "en.json").read_text(encoding="utf-8"))


def flat(o):
    if isinstance(o, dict):
        for v in o.values():
            yield from flat(v)
    elif isinstance(o, list):
        for v in o:
            yield from flat(v)
    else:
        yield o


ARTS = [json.loads(p.read_text(encoding="utf-8")) for p in sorted((ROOT / "data" / "articles").glob("*.json"))]
en_long = [s for s in flat([en] + [a["en"] for a in ARTS]) if isinstance(s, str) and len(s) > 24 and " " in s]
pages = sorted(SITE.rglob("index.html"))
for f in pages:
    rel = f.relative_to(SITE).as_posix()
    t = f.read_text(encoding="utf-8")
    p = P()
    p.feed(t)
    if p.h1 != 1:
        err(f"{rel}: {p.h1} h1 tags")
    home = rel in ("index.html", "ms/index.html", "zh/index.html")
    want = {"header", "footer", "sticky", "wa", "tel"} | (set() if rel.endswith("contact/index.html") else {"cta"})
    if not home:
        want.add("crumbs")
    if home:
        want |= {"diagram", "process", "carousel", "reel", "review", "map", "faq"}
    if rel.endswith("contact/index.html"):
        want.add("map")
    miss = want - p.parts
    if miss:
        err(f"{rel}: shared parts missing {sorted(miss)}")
    if CFG["preview"] and p.robots != "noindex,nofollow":
        err(f"{rel}: robots meta is {p.robots!r}")
    if p.hreflang != 4:
        err(f"{rel}: {p.hreflang} hreflang links")
    if "{{" in t or "{topic}" in t:
        err(f"{rel}: unfilled placeholder")
    for blob in p.ld:
        try:
            g = json.loads(blob)
        except Exception as e:
            err(f"{rel}: bad JSON-LD {e}")
            continue
        types = {n.get("@type") for n in g["@graph"]}
        if "AggregateRating" in blob or "Review" in types:
            err(f"{rel}: rating/review schema (not allowed)")
        biz = [n for n in g["@graph"] if n.get("@id", "").endswith("#business")]
        if not biz:
            err(f"{rel}: no business node")
            continue
        b = biz[0]
        for k, v in (("telephone", CFG["phone_e164"]), ("email", CFG["email"]), ("hasMap", CFG["maps_url"]), ("openingHours", CFG["opening_hours"]), ("legalName", CFG["name"])):
            if b.get(k) != v:
                err(f"{rel}: schema {k} {b.get(k)!r} != config")
        if b.get("sameAs") != [CFG["facebook_url"]]:
            err(f"{rel}: schema sameAs")
        if rel.startswith(("articles/", "ms/articles/", "zh/articles/")):
            need_types = ("CollectionPage", "BreadcrumbList") if rel.endswith("articles/index.html") else ("Article", "FAQPage", "BreadcrumbList")
            for need in need_types:
                if need not in types:
                    err(f"{rel}: schema {need} missing")
        elif not home and "contact" not in rel and "about" not in rel:
            for need in ("Service", "FAQPage", "BreadcrumbList"):
                if need not in types:
                    err(f"{rel}: schema {need} missing")
        # FAQPage must equal the visible FAQ
        for n in g["@graph"]:
            if n.get("@type") == "FAQPage":
                for q in n["mainEntity"]:
                    if html.escape(q["name"]) not in t:
                        err(f"{rel}: FAQ schema question not visible: {q['name'][:50]}")
    for href in p.links:
        if href.startswith(("http", "mailto:", "tel:", "#")):
            continue
        path = href.split("#")[0].split("?")[0]
        if "/media/reel-" in path:  # reels are on the server already, not part of the build
            continue
        if not path.startswith(BASE):
            err(f"{rel}: link outside base {href}")
            continue
        target = SITE / path[len(BASE):]
        if path.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            err(f"{rel}: broken link {href}")
    for src in p.imgs:
        if "/media/" in src:  # reel posters are on the server already, not part of the build
            continue
        if not (SITE / src.split("?")[0][len(BASE):]).exists():
            err(f"{rel}: missing image {src}")
    for src in p.imgs_no_size:
        if "/media/" not in (src or "") and "logo-96" not in (src or ""):
            err(f"{rel}: image without width/height/alt {src}")
    # facts shown the same everywhere
    for needle, what in ((f'href="tel:{CFG["phone_e164"]}"', "tel link"), (f"wa.me/{WA}", "WhatsApp link"), (f'mailto:{CFG["email"]}', "email"),
                         (html.escape(CFG["address_display"]), "address"), ('data-cta="whatsapp_mobile_bar"', "sticky WhatsApp"),
                         ('data-cta="call_mobile_bar"', "sticky call"), ('data-cta="email_footer"', "footer email"), ('data-cta="map_footer"', "footer map"),
                         (CFG["credit"], "credit line")):
        if needle not in t:
            err(f"{rel}: {what} missing")
    if "<iframe" in t:
        err(f"{rel}: iframe in served HTML (map/video must load on tap)")
    if 'preload="none"' not in t and "<video" in t:
        err(f"{rel}: video without preload=none")
    if t.count("<video") != t.count('preload="none"'):
        err(f"{rel}: some video without preload=none")
    for bad in ("CT200h job", "Lexus CT200h service"):
        if bad in t:
            err(f"{rel}: {bad!r}")
    if rel.startswith(("ms/", "zh/")):
        body = t.split("<body", 1)[1]
        for r in REVIEW_TEXT:  # verbatim English quotes are allowed
            body = body.replace(html.escape(r), "")
        same = set(flat([json.loads((ROOT / "strings" / (rel[:2] + ".json")).read_text(encoding="utf-8"))] + [a[rel[:2]] for a in ARTS]))
        for s in en_long:
            if s in same:  # kept on purpose (car model names)
                continue
            if s in REVIEW_TEXT or s in CFG["address_display"]:
                continue
            if html.escape(s) in body:
                err(f"{rel}: English text left: {s[:60]!r}")
# review quotes verbatim on the home pages
for pre in ("", "ms/", "zh/"):
    t = (SITE / pre / "index.html").read_text(encoding="utf-8")
    for r in REVIEW_TEXT:
        if html.escape(r) not in t:
            err(f"{pre}index: review quote changed or missing: {r[:40]}")
for l in ("en", "ms", "zh"):
    s = json.loads((ROOT / "strings" / f"{l}.json").read_text(encoding="utf-8"))
    pre = "" if l == "en" else l + "/"
    c = (SITE / pre / "contact" / "index.html").read_text(encoding="utf-8")
    if c.count(html.escape(s["ui"]["hours_text"])) < 2:
        err(f"{pre}contact: hours not shown on the page and footer")
    for k, pg in s["pages"].items():
        if l == "ms" and len(pg["title"]) > 65:
            err(f"{l} {k}: title too long ({len(pg['title'])})")
        # contact: the client-approved live description (hours update 12 Nov 2026) is longer; kept word for word, up to 215.
        if len(pg["description"]) > (215 if k == "contact" else 165):
            err(f"{l} {k}: description too long")
for f in ("sitemap.xml", "llms.txt", "favicon.png", "apple-touch-icon.png", "img/og-1200x630.jpg"):
    if not (SITE / f).exists():
        err(f"missing {f}")
if "autoseo.my" in (SITE / "sitemap.xml").read_text() or "autoseo.my/preview" in (SITE / "llms.txt").read_text():
    err("sitemap/llms must name the planned domain, not the preview")
if CFG["preview"] and ("/articles/" in (SITE / "sitemap.xml").read_text() or "/articles/" in (SITE / "llms.txt").read_text()):
    err("preview: articles must stay out of sitemap.xml and llms.txt until move day")
if any(SITE.rglob(".htaccess")) or (SITE / "media").exists():
    err("site/ must not contain .htaccess or media/")

# customer plates: the blurred source photos must stay in place
import hashlib
for name, h in json.loads((ROOT / "data" / "blurred-photos.json").read_text())["files"].items():
    if hashlib.sha256((ROOT / "photos" / name).read_bytes()).hexdigest() != h:
        err(f"photos/{name} is not the blurred version (customer plate)")

if errors:
    print("CHECK FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"check ok: {len(pages)} pages, shared parts on every page, blocklist clean, facts consistent, links and images resolve")
