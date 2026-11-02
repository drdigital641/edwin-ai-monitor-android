#!/usr/bin/env python3
"""Checks for a built Battery Rescue site:  python3 check.py BUILT_DIR
Titles <=65, descriptions 120-160, one H1, lang en-SG, JSON-LD parses, FAQPage == visible FAQ, sitemap URLs all built + self-canonical,
images WebP <=150 KB with width/height, no noindex meta."""
import json, re, sys
from pathlib import Path
R = Path(sys.argv[1]); bad = []
def err(m): bad.append(m); print("FAIL", m)
pages = {}
for f in R.rglob("*.html"):
    p = "/" + str(f.relative_to(R)).replace("index.html", "")
    pages[p] = f.read_text()
for p, s in pages.items():
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    if len(t) > 80 or len(re.sub(r"&#x27;|&amp;", "x", t)) > 65: err(f"{p} title {len(t)}")
    d = re.search(r'name="description" content="(.*?)"', s).group(1)
    if p != "/404.html" and not 120 <= len(re.sub(r"&#x27;|&amp;", "x", d)) <= 160: err(f"{p} desc {len(d)}")
    if s.count("<h1") != 1: err(f"{p} h1 count {s.count('<h1')}")
    if 'lang="en-SG"' not in s: err(f"{p} lang")
    if re.search(r'<meta name="robots" content="[^"]*noindex', s): err(f"{p} noindex meta")
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: j = json.loads(blk)
        except Exception as e: err(f"{p} jsonld {e}"); continue
        for n in j.get("@graph", []):
            if n.get("@type") == "FAQPage":
                for q in n["mainEntity"]:
                    a = q["acceptedAnswer"]["text"]
                    vis = re.sub(r"<[^>]+>", "", re.search(r"<summary>" + re.escape(q["name"].replace("&", "&amp;").replace("'", "&#x27;")) + r"</summary><p>(.*?)</p>", s, re.S).group(1)) if re.search(r"<summary>" + re.escape(q["name"].replace("&", "&amp;").replace("'", "&#x27;")) + r"</summary><p>(.*?)</p>", s, re.S) else None
                    if vis is None or vis.strip() != a.strip(): err(f"{p} FAQ mismatch: {q['name']}")
    for im in re.findall(r"<img [^>]*>", s):
        if "width=" not in im or "height=" not in im or "alt=" not in im: err(f"{p} img attrs {im[:60]}")
for u in re.findall(r"<loc>(.*?)</loc>", (R / "sitemap.xml").read_text()):
    path = u.replace("https://batteryrescue.sg", "")
    if path not in pages: err(f"sitemap URL not built {u}")
    elif f'<link rel="canonical" href="{u}">' not in pages[path]: err(f"sitemap URL not self-canonical {u}")
for f in (R / "photos").glob("*"):
    if f.suffix != ".webp" or f.stat().st_size > 150 * 1024: err(f"photo {f.name}")
print("pages", len(pages), "failures", len(bad))
sys.exit(1 if bad else 0)
