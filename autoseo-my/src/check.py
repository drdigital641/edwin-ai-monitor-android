#!/usr/bin/env python3
"""Pre-upload check for the built site. Exit 1 stops the build/upload.

1. Blocklist grep (data/blocklist.txt) over every built file, its path and the
   source data and templates.
2. Every HTML page: exactly one <h1>, robots noindex,nofollow (while preview),
   at least one JSON-LD block that parses, no sitemap file in the output.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BRAND = json.loads((ROOT / "data" / "brand.json").read_text(encoding="utf-8"))
terms = [t.strip() for t in (ROOT / "data" / "blocklist.txt").read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]

scan = [p for p in SITE.rglob("*") if p.is_file()]
scan += [ROOT / "data" / "brand.json", ROOT / "data" / "content.py"] + list((ROOT / "templates").glob("*.html")) + [ROOT / "assets" / "brand.css", ROOT / "assets" / "base.css", ROOT / "assets" / "site.js"]
hits = []
for p in scan:
    text = p.read_text(encoding="utf-8", errors="replace").lower()
    rel = str(p.relative_to(ROOT)).lower()
    for t in terms:
        tl = t.lower()
        if tl in rel:
            hits.append(f"{rel}: file name contains {t!r}")
        n = text.count(tl)
        if n:
            i = text.find(tl)
            hits.append(f"{rel}: {n}x {t!r} … {text[max(0, i-40):i+40]!r}")

problems = []
pages = sorted(SITE.rglob("*.html"))
for p in pages:
    h = p.read_text(encoding="utf-8")
    rel = p.relative_to(SITE)
    if len(re.findall(r"<h1[\s>]", h)) != 1:
        problems.append(f"{rel}: needs exactly one <h1>")
    if BRAND["preview"] and '<meta name="robots" content="noindex,nofollow">' not in h:
        problems.append(f"{rel}: missing robots noindex,nofollow")
    blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)
    if not blocks:
        problems.append(f"{rel}: no JSON-LD")
    for b in blocks:
        try:
            g = json.loads(b)["@graph"]
            for node in g:
                if any(k in node for k in ("telephone", "address", "email")):
                    problems.append(f"{rel}: schema has telephone/address/email")
        except Exception as e:  # noqa: BLE001
            problems.append(f"{rel}: JSON-LD does not parse ({e})")
    if re.search(r"tel:|mailto:", h):
        problems.append(f"{rel}: phone or email link")
for name in ("sitemap.xml", "sitemap.txt", "robots.txt"):
    if (SITE / name).exists():
        problems.append(f"{name} must not be in the preview")

print(f"checked {len(pages)} pages, {len(scan)} files, {len(terms)} blocked terms")
print(f"blocklist hits: {len(hits)}")
for x in hits:
    print("  HIT", x)
print(f"page problems: {len(problems)}")
for x in problems:
    print("  FAIL", x)
sys.exit(1 if hits or problems else 0)
