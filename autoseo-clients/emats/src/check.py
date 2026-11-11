#!/usr/bin/env python3
"""Checks for the built EMATS site. Exit code 1 on any problem."""
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
CFG = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
BASE = CFG["base_path"]
WA = (CFG.get("whatsapp_number") or "").strip()
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


en_long = [s for s in flat(en) if isinstance(s, str) and len(s) > 24 and " " in s]
pages = sorted(SITE.rglob("index.html"))
owner_hits = {}
for f in pages:
    rel = f.relative_to(SITE).as_posix()
    t = f.read_text(encoding="utf-8")
    p = P()
    p.feed(t)
    if p.h1 != 1:
        err(f"{rel}: {p.h1} h1 tags")
    want = {"header", "footer", "sticky", "wa"} | (set() if rel.endswith("contact/index.html") else {"cta"})
    if "/" in rel.replace("index.html", "").strip("/") or rel.count("/") > 1 or rel not in ("index.html", "ms/index.html", "zh/index.html"):
        want.add("crumbs")
    if rel in ("index.html", "ms/index.html", "zh/index.html"):
        want |= {"service-card", "reel", "faq"}
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
        biz = [n for n in g["@graph"] if n.get("@id", "").endswith("#business")]
        if not biz:
            err(f"{rel}: no business node")
        else:
            want_tel = CFG.get("phone_e164") or ("+" + WA if WA else None)
            if biz[0].get("telephone") != want_tel:
                err(f"{rel}: schema telephone {biz[0].get('telephone')!r} does not match config {want_tel!r}")
            if CFG.get("hours"):
                ohs = biz[0].get("openingHoursSpecification") or []
                if [(o["opens"], o["closes"], len(o["dayOfWeek"])) for o in ohs] != [(h["opens"], h["closes"], len(h["days"])) for h in CFG["hours"]]:
                    err(f"{rel}: openingHoursSpecification does not match config")
            if "address" in biz[0] or "hasMap" in biz[0]:
                err(f"{rel}: address/map in schema (not given)")
    for href in p.links:
        if href.startswith(("http", "mailto:", "tel:", "#")):
            continue
        path = href.split("#")[0].split("?")[0]
        if not path.startswith(BASE):
            err(f"{rel}: link outside base {href}")
            continue
        target = SITE / path[len(BASE):]
        if path.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            err(f"{rel}: broken link {href}")
    for src in p.imgs:
        if not (SITE / src[len(BASE):]).exists():
            err(f"{rel}: missing image {src}")
    for src in p.imgs_no_size:
        err(f"{rel}: image without width/height/alt {src}")
    if CFG.get("phone_e164") and f'href="tel:{CFG["phone_e164"]}"' not in t:
        err(f"{rel}: no tel: link")
    if CFG.get("hours") and 'data-part="hours"' not in t.split('data-part="footer"', 1)[-1]:
        err(f"{rel}: hours missing in footer")
    if WA:
        if "is-soon" in t:
            err(f"{rel}: coming-soon button while number is set")
    else:
        if "wa.me" in t:
            err(f"{rel}: wa.me link while whatsapp_number is empty")
    n = t.count("Jackie Sky")
    if n:
        owner_hits[rel] = n
    if rel.startswith(("ms/", "zh/")):
        body = t.split("<body", 1)[1]
        for s in en_long:
            if s in body or s.replace("'", "&#x27;") in body:
                err(f"{rel}: English text left: {s[:60]!r}")
for l in ("en", "ms", "zh"):
    s = json.loads((ROOT / "strings" / f"{l}.json").read_text(encoding="utf-8"))
    pre = "" if l == "en" else l + "/"
    c = (SITE / pre / "contact" / "index.html").read_text(encoding="utf-8")
    if CFG.get("hours") and c.count(s["ui"]["hours_text"]) < 2:
        err(f"{pre}contact: hours not shown on the page and footer")
for rel, n in owner_hits.items():
    if not rel.endswith("about/index.html") or n > 1:
        err(f"owner name on {rel} x{n} (only once, About page)")

if errors:
    print("CHECK FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"check ok: {len(pages)} pages, shared parts on every page, blocklist clean, links and images resolve")
