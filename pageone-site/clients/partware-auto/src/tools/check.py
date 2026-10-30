#!/usr/bin/env python3
"""Static checker for the built site: JSON-LD parses, FAQ schema == visible FAQs, title/description limits, internal links/assets resolve.
Run from the project folder:  python3 tools/check.py site"""
import sys, re, json, html
from pathlib import Path
from urllib.parse import urlsplit, unquote
from html.parser import HTMLParser

SITE = Path(sys.argv[1] if len(sys.argv) > 1 else "site").resolve()
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links = []; s.ld = []; s.faq = 0; s.title = ""; s.desc = ""; s.canon = ""; s.h1 = 0; s._t = False; s._ld = False; s._buf = ""; s.noindex = False; s.imgs = []
    def handle_starttag(s, tag, a):
        a = dict(a)
        if tag == "title": s._t = True
        if tag == "meta":
            if a.get("name") == "description": s.desc = a.get("content", "")
            if a.get("name") == "robots" and "noindex" in a.get("content", ""): s.noindex = True
        if tag == "link" and a.get("rel") == "canonical": s.canon = a.get("href", "")
        if tag == "link" and a.get("href") and a.get("rel") in ("icon", "stylesheet", "apple-touch-icon", "manifest") and not a["href"].startswith("http"): s.links.append(a["href"])
        if tag in ("a",) and a.get("href"): s.links.append(a["href"])
        if tag in ("script",) and a.get("src") and not a["src"].startswith("http"): s.links.append(a["src"])
        if tag == "script" and a.get("type") == "application/ld+json": s._ld = True; s._buf = ""
        if tag == "details" and "faq" in "": pass
        if tag == "details" and "faq" in (a.get("class") or ""): s.faq += 1
        if tag == "h1": s.h1 += 1
        if tag == "img":
            s.imgs.append(a)
    def handle_endtag(s, tag):
        if tag == "title": s._t = False
        if tag == "script" and s._ld: s.ld.append(s._buf); s._ld = False
    def handle_data(s, d):
        if s._t: s.title += d
        if s._ld: s._buf += d

def resolve(page, href):
    u = urlsplit(href)
    if u.scheme in ("http", "https", "mailto", "tel", "whatsapp") or href.startswith("#") or not href: return True
    path = unquote(u.path)
    base = page.parent
    t = (SITE / path.lstrip("/")) if path.startswith("/") else (base / path)
    t = Path(str(t.resolve()))
    if t.is_dir(): t = t / "index.html"
    return t.exists()

bad = []; n = 0; ldc = 0; faq_ld_total = 0; faq_vis_total = 0; links = 0; pages = 0; faqpages = []
for f in sorted(SITE.rglob("*.html")):
    pages += 1; p = P(); p.feed(f.read_text()); rel = f.relative_to(SITE)
    if p.noindex: bad.append(f"{rel}: has noindex")
    if "staff" not in str(rel):
        if not (0 < len(p.title) < 60): bad.append(f"{rel}: title length {len(p.title)}")
        if not (0 < len(p.desc) < 160): bad.append(f"{rel}: desc length {len(p.desc)}")
        if not p.canon: bad.append(f"{rel}: no canonical")
        if p.h1 != 1: bad.append(f"{rel}: h1 count {p.h1}")
    for a in p.imgs:
        if "alt" not in a or not a.get("width") or not a.get("height"): bad.append(f"{rel}: img missing alt/width/height {a.get('src','')[:60]}")
    fl = 0
    for s in p.ld:
        try:
            j = json.loads(s); ldc += 1
            for node in j.get("@graph", [j]):
                if node.get("@type") == "FAQPage": fl += len(node["mainEntity"])
        except Exception as ex: bad.append(f"{rel}: JSON-LD parse error {ex}")
    if fl or p.faq:
        faqpages.append((str(rel), fl, p.faq))
        if fl != p.faq: bad.append(f"{rel}: FAQ schema {fl} != visible {p.faq}")
    faq_ld_total += fl; faq_vis_total += p.faq
    for h in p.links:
        links += 1
        if not resolve(f, h): bad.append(f"{rel}: broken link {h}")
for f in SITE.rglob("*.html"):
    if "noindex" in f.read_text().lower(): bad.append(f"{f.relative_to(SITE)}: contains 'noindex'")
import re as _re
hm = (SITE/"index.html").read_text()
vis = _re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", hm, flags=_re.S); vis = _re.sub(r"<[^>]+>", " ", vis)
wc = len(html.unescape(vis).split()); print(f"home visible words: {wc}")
if not 500 <= wc <= 900: bad.append(f"home word count {wc} outside 500-900")
for f in SITE.rglob("*.html"):
    t = f.read_text()
    for pat in ("authorised", "authorized", "best price", "cheapest", "guarantee", "ratings", "stars"):
        if pat in t.lower(): bad.append(f"{f.relative_to(SITE)}: contains '{pat}'")
    if 'honda-logo' in t.lower() or 'logo-honda' in t.lower(): bad.append(f"{f.relative_to(SITE)}: Honda logo reference")
print(f"pages checked: {pages}")
print(f"JSON-LD blocks parsed OK: {ldc}")
print(f"FAQ pages (schema questions vs visible): {faqpages}  totals schema={faq_ld_total} visible={faq_vis_total}")
print(f"internal links/assets checked: {links}")
print("PROBLEMS:" if bad else "NO PROBLEMS", *bad, sep="\n  ")
sys.exit(1 if bad else 0)
