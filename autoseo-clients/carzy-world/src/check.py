#!/usr/bin/env python3
"""Pre-upload check for the built Carzy World site. Exit 1 stops the build.

1. Blocklist (data/blocklist.txt) over every built and source file.
2. Every page: one <h1>, robots noindex,nofollow while preview, html lang,
   canonical, hreflang en/ms/zh-Hans/x-default, JSON-LD that parses with an
   AutoRepair node whose name, address, phone and hours match business.json.
3. Every shared part reached every page (header, language switch, header
   WhatsApp, trust strip, CTA band, footer, credit, mobile WhatsApp bar), and
   the same name, phone and address appear on every page.
4. Every <img> has alt text and points to a file that exists; css/js carry ?v=.
5. Malay and Chinese pages: no leftover English and no {placeholders}.
6. sitemap.xml and llms.txt use the planned domain only (no preview URLs).
"""
import html as H
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
BIZ = json.loads((ROOT / "data" / "business.json").read_text(encoding="utf-8"))
SITE_DATA = json.loads((ROOT / "data" / "site.json").read_text(encoding="utf-8"))
STR = {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in (ROOT / "strings").glob("*.json")}
terms = [t.strip() for t in (ROOT / "data" / "blocklist.txt").read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]
problems, hits = [], []

# 1. blocklist
scan = [p for p in SITE.rglob("*") if p.suffix in (".html", ".css", ".js", ".txt", ".xml")]
scan += list((ROOT / "strings").glob("*.json")) + list((ROOT / "templates").glob("*.html")) + [ROOT / "data" / "business.json", ROOT / "data" / "site.json", ROOT / "src" / "build.py"]
for p in scan:
    text = p.read_text(encoding="utf-8", errors="replace").lower()
    for t in terms:
        if t.lower() in text:
            i = text.find(t.lower())
            hits.append(f"{p.relative_to(ROOT)}: {t!r} … {text[max(0, i - 40):i + 40]!r}")

# 2-4. pages
SHARED = {
    "header": 'class="site-header"', "language switch": 'class="lang-switch"', "header WhatsApp": 'data-cta="whatsapp_header"',
    "trust strip": 'class="trust"', "CTA band": 'class="cta-band"', "footer": 'class="site-footer"', "credit": BIZ["credit_url"],
    "mobile WhatsApp bar": 'data-cta="whatsapp_mobile_bar"', "footer Google Maps button": 'data-cta="google_listing_footer"',
    "rating badge Google reviews link": 'data-cta="google_reviews_badge"', "Google listing link": BIZ["google_listing_url"], "WhatsApp number": f"wa.me/{BIZ['whatsapp_number']}",
}
LANG_ATTR = {"en": "en", "ms": "ms", "zh": "zh-Hans"}
pages = sorted(SITE.rglob("*.html"))
counts = {k: 0 for k in SHARED}
want_hours = sorted((tuple(sorted(h["days"])), h["opens"], h["closes"]) for h in BIZ["hours"])
for p in pages:
    rel = p.relative_to(SITE)
    code = rel.parts[0] if rel.parts[0] in ("ms", "zh") else "en"
    h = p.read_text(encoding="utf-8")
    u = H.unescape(h)
    if "<blockquote" in h or 'class="card review"' in h:
        problems.append(f"{rel}: no individual review cards (rating line + Google Maps link only)")
    for bad in ("1128044756568418", "1358776602985089"):
        if bad in h:
            problems.append(f"{rel}: dropped clip {bad} must not appear")
    if rel.parts[-2:-1] == ("contact",) and 'data-cta="google_listing_contact"' not in h:
        problems.append(f"{rel}: contact page needs the Find us on Google Maps button")
    for m in re.finditer(r'<a [^>]*href="' + re.escape(BIZ["google_listing_url"]) + r'"[^>]*>', h):
        if 'target="_blank"' not in m.group(0) or 'rel="noopener"' not in m.group(0):
            problems.append(f"{rel}: Google listing link must open in a new tab with rel=noopener")
    if len(re.findall(r"<h1[\s>]", h)) != 1:
        problems.append(f"{rel}: needs exactly one <h1>")
    if BIZ["preview"] and '<meta name="robots" content="noindex,nofollow">' not in h:
        problems.append(f"{rel}: missing robots noindex,nofollow")
    if f'<html lang="{LANG_ATTR[code]}">' not in h:
        problems.append(f"{rel}: html lang should be {LANG_ATTR[code]}")
    if '<link rel="canonical" href="' + BIZ["site_url"] not in h:
        problems.append(f"{rel}: canonical missing")
    for hl in ("en", "ms", "zh-Hans", "x-default"):
        if f'hreflang="{hl}" href="' not in h:
            problems.append(f"{rel}: no hreflang {hl}")
    for name, needle in SHARED.items():
        if needle in h:
            counts[name] += 1
        else:
            problems.append(f"{rel}: shared part missing: {name}")
    for needle in (BIZ["name"], BIZ["phone_display"], BIZ["address_full"]):
        if needle not in u:
            problems.append(f"{rel}: NAP text missing: {needle[:40]}")
    types = []
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try:
            g = json.loads(b)["@graph"]
        except Exception as e:  # noqa: BLE001
            problems.append(f"{rel}: JSON-LD does not parse ({e})")
            continue
        for node in g:
            types.append(node["@type"])
            if node["@type"] == "AutoRepair":
                a = node["address"]
                if node["name"] != BIZ["name"] or node["telephone"] != BIZ["phone_e164"] or a["streetAddress"] != BIZ["street"] or a["postalCode"] != BIZ["postcode"]:
                    problems.append(f"{rel}: AutoRepair name/phone/address differs from business.json")
                got = sorted((tuple(sorted(x.rsplit("/", 1)[-1] for x in s["dayOfWeek"])), s["opens"], s["closes"]) for s in node["openingHoursSpecification"])
                if got != want_hours:
                    problems.append(f"{rel}: opening hours differ")
                if "aggregateRating" in node or "review" in node or "Review" in str(node.get("@type")):
                    problems.append(f"{rel}: no review markup for self-hosted reviews")
    if "AutoRepair" not in types:
        problems.append(f"{rel}: no AutoRepair schema")
    if rel.parts[-2:-1] and rel.as_posix() not in ("index.html", "ms/index.html", "zh/index.html") and "BreadcrumbList" not in types:
        problems.append(f"{rel}: no BreadcrumbList")
    for img in re.findall(r"<img [^>]*>", h):
        alt = re.search(r'alt="([^"]*)"', img)
        if not alt or not alt.group(1).strip():
            problems.append(f"{rel}: image without alt: {img[:80]}")
        src = re.search(r'src="([^"?]+)', img).group(1)
        if "media/" in src:
            if src.split("media/")[-1] not in SITE_DATA["server_media"]:
                problems.append(f"{rel}: media file not on the server list: {src}")
        elif not (SITE / src[len(BIZ["base_path"]):]).exists():
            problems.append(f"{rel}: missing image {src}")
    # media links: page-relative, resolve to <site>/media/<known file>
    depth = len(rel.parts) - 1
    for m in re.findall(r'(?:src|poster|href)="((?:\.\./)*)media/([^"]+)"', h):
        if len(m[0]) // 3 != depth or m[1] not in SITE_DATA["server_media"]:
            problems.append(f"{rel}: bad media link {m[0]}media/{m[1]}")
    # facades: no third-party video request before a tap
    if re.search(r'<(?:iframe|script)[^>]+src="https://[^"]*(facebook|youtube|tiktok)', h):
        problems.append(f"{rel}: video platform loads before a tap")
    if rel.name == "index.html" and len(rel.parts) <= 2 and rel.parts[0] in ("index.html", "ms", "zh") and "VideoObject" not in types:
        problems.append(f"{rel}: homepage without VideoObject")
    for ref in re.findall(r'(?:href|src)="([^"]+\.(?:css|js)[^"]*)"', h):
        if "?v=" not in ref:
            problems.append(f"{rel}: asset without ?v= {ref}")
    for ref in re.findall(r'href="(' + re.escape(BIZ["base_path"]) + r'[^"#?]*)', h):
        target = SITE / ref[len(BIZ["base_path"]):]
        if not (target.is_file() or (target / "index.html").exists()):
            problems.append(f"{rel}: broken internal link {ref}")


# 5. leftover English on ms/zh pages
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


en = dict(leaves(STR["en"]))
for code in ("ms", "zh"):
    other = dict(leaves(STR[code]))
    if set(en) != set(other):
        problems.append(f"strings/{code}.json keys differ from en.json: {sorted(set(en) ^ set(other))[:8]}")
    changed = [v for k, v in en.items() if len(v) >= 12 and other.get(k) != v]
    for p in sorted((SITE / code).rglob("*.html")):
        u = H.unescape(p.read_text(encoding="utf-8"))
        for v in changed:
            if v in u:
                problems.append(f"{p.relative_to(SITE)}: leftover English {v[:60]!r}")
                break
        if re.search(r"\{(topic|phone|name)\}", u):
            problems.append(f"{p.relative_to(SITE)}: unfilled placeholder")

# 6. sitemap + llms for the planned domain
for name in ("sitemap.xml", "llms.txt"):
    f = SITE / name
    if not f.exists():
        problems.append(f"{name} missing")
    elif "autoseo.my/preview" in f.read_text(encoding="utf-8"):
        problems.append(f"{name} contains preview URLs")
for name in ("robots.txt",):
    if (SITE / name).exists() and BIZ["preview"]:
        problems.append(f"{name} must not be in the preview folder")

print(f"checked {len(pages)} pages, {len(scan)} files, {len(terms)} blocked terms")
print("shared parts: " + ", ".join(f"{k} {v}/{len(pages)}" for k, v in counts.items()))
print(f"blocklist hits: {len(hits)}")
for x in hits:
    print("  HIT", x)
print(f"page problems: {len(problems)}")
for x in problems[:60]:
    print("  FAIL", x)
sys.exit(1 if hits or problems else 0)
