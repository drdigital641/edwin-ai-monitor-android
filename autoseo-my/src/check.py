#!/usr/bin/env python3
"""Pre-upload check for the built site. Exit 1 stops the build/upload.

1. Blocklist grep (data/blocklist.txt) over every built file, its path and the
   source data and templates.
2. Every HTML page: exactly one <h1>, robots noindex,nofollow (while preview),
   at least one JSON-LD block that parses, no sitemap file in the output,
   html lang, canonical and hreflang (en, ms, zh-Hans, x-default) present.
3. Malay and Chinese pages: no leftover English string from strings/en.json
   (any English value of 12+ characters that the language file changed),
   and no unfilled {placeholders}.
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
scan += [ROOT / "data" / "brand.json", ROOT / "data" / "site.json"] + list((ROOT / "strings").glob("*.json")) + list((ROOT / "templates").glob("*.html")) + [ROOT / "assets" / "brand.css", ROOT / "assets" / "base.css", ROOT / "assets" / "site.js", ROOT / "assets" / "check.js", ROOT / "assets" / "check.css", ROOT / "assets" / "partners.css", ROOT / "assets" / "articles.css"] + list((ROOT / "data" / "articles").glob("*.json"))
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
# leftover English on ms/zh pages
def leaves(node, path=""):
    if isinstance(node, dict):
        for k, v in node.items():
            if not k.startswith("_"):
                yield from leaves(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from leaves(v, f"{path}[{i}]")
    elif isinstance(node, str):
        yield path, node

import html as _h
STR = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "strings").glob("*.json")}
en = dict(leaves(STR["en"]))
LANG_ATTR = {"en": "en", "ms": "ms", "zh": "zh-Hans"}
for code in [c for c in STR if c != "en"]:
    other = dict(leaves(STR[code]))
    missing = sorted(set(en) - set(other))
    if missing:
        problems.append(f"strings/{code}.json missing keys: {missing[:8]}")
    changed = [v for k, v in en.items() if len(v) >= 12 and other.get(k) != v]
    for p in sorted((SITE / code).rglob("*.html")):
        h = _h.unescape(p.read_text(encoding="utf-8"))
        for v in changed:
            if v in h:
                problems.append(f"{p.relative_to(SITE)}: leftover English {v[:60]!r}")
                break
        if re.search(r"\{(n|name|label|topic)\}", h):
            problems.append(f"{p.relative_to(SITE)}: unfilled placeholder")
for p in pages:
    rel = p.relative_to(SITE)
    code = rel.parts[0] if rel.parts[0] in ("ms", "zh") else "en"
    h = p.read_text(encoding="utf-8")
    if f'<html lang="{LANG_ATTR[code]}">' not in h:
        problems.append(f"{rel}: html lang should be {LANG_ATTR[code]}")
    if '<link rel="canonical"' not in h:
        problems.append(f"{rel}: no canonical")
    for hl in ("en", "ms", "zh-Hans", "x-default"):
        if f'hreflang="{hl}" href=' not in h:
            problems.append(f"{rel}: no hreflang {hl}")

if BRAND["preview"]:
    for name in ("sitemap.xml", "sitemap.txt", "robots.txt"):
        if (SITE / name).exists():
            problems.append(f"{name} must not be in the preview")
else:
    for name in ("sitemap.xml", "robots.txt"):
        if not (SITE / name).exists():
            problems.append(f"{name} missing on the live build")
    for p in pages:
        h = p.read_text(encoding="utf-8")
        want = "noindex,nofollow" if p.name == "404.html" else "index,follow"
        if f'<meta name="robots" content="{want}">' not in h:
            problems.append(f"{p.relative_to(SITE)}: robots should be {want}")

print(f"checked {len(pages)} pages, {len(scan)} files, {len(terms)} blocked terms")
print(f"blocklist hits: {len(hits)}")
for x in hits:
    print("  HIT", x)
print(f"page problems: {len(problems)}")
for x in problems:
    print("  FAIL", x)
sys.exit(1 if hits or problems else 0)
