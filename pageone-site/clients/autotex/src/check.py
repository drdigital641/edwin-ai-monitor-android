#!/usr/bin/env python3
"""Autotex build checks. Run after build.py:  python3 check.py ../site
Checks: JSON-LD parses, FAQPage equals the visible FAQ, lang en-SG, title <= 65, description 120-160 (indexed pages),
sitemap = indexable + self-canonical + file exists, brand x part page length and near-duplicate score, llms.txt coverage."""
import sys, re, json, html, itertools
from pathlib import Path
SITE = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "site")
BASE = "https://autotexautoparts.com.sg"
errs, warns = [], []

def text_of(h):
    h = re.sub(r"<(script|style|header|footer)[\s\S]*?</\1>", " ", h)
    return html.unescape(re.sub(r"<[^>]+>", " ", h))

sm = re.findall(r"<loc>(.*?)</loc>", (SITE / "sitemap.xml").read_text())
smset = set(sm)
pages = {}
for f in SITE.rglob("*.html"):
    rel = f.relative_to(SITE).as_posix()
    if rel.startswith(("assets/", "retired/", "upload/")): continue
    pages[rel] = f.read_text()

def url_of(rel):
    return BASE + "/" + ("" if rel == "index.html" else rel.replace("index.html", ""))

indexed = 0
for rel, h in pages.items():
    url = url_of(rel)
    ti = re.search(r"<title>(.*?)</title>", h)
    de = re.search(r'<meta name="description" content="(.*?)">', h)
    ro = re.search(r'<meta name="robots" content="(.*?)">', h)
    ca = re.search(r'<link rel="canonical" href="(.*?)">', h)
    noidx = bool(ro and "noindex" in ro.group(1))
    lang = re.search(r'<html lang="(.*?)"', h)
    if not lang or lang.group(1) != "en-SG": errs.append(f"{rel}: lang {lang and lang.group(1)}")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        try: j = json.loads(m.group(1))
        except Exception as ex: errs.append(f"{rel}: JSON-LD does not parse {ex}"); continue
        for node in j.get("@graph", []):
            if node.get("@type") == "FAQPage":
                vis = re.findall(r'<details class="faq"><summary>(.*?)</summary><p>(.*?)</p></details>', h, re.S)
                want = [(html.unescape(q), html.unescape(re.sub("<[^>]+>", "", a))) for q, a in vis]
                got = [(q["name"], q["acceptedAnswer"]["text"]) for q in node["mainEntity"]]
                if vis and want != got: errs.append(f"{rel}: FAQPage differs from visible FAQ")
    if rel == "404.html": continue
    if rel.startswith("staff/"): continue
    if not noidx:
        indexed += 1
        if url not in smset: errs.append(f"{rel}: indexable but not in sitemap")
        if ca and ca.group(1) != url: errs.append(f"{rel}: canonical {ca.group(1)}")
        t = html.unescape(ti.group(1)) if ti else ""
        d = html.unescape(de.group(1)) if de else ""
        if len(t) > 65: errs.append(f"{rel}: title {len(t)} chars")
        if not 120 <= len(d) <= 160: errs.append(f"{rel}: description {len(d)} chars")
    else:
        if url in smset: errs.append(f"{rel}: noindex but in sitemap")
for u in sm:
    rel = u.replace(BASE + "/", "") or "index.html"
    rel = rel + "index.html" if rel.endswith("/") or rel == "index.html" and False else rel
    if rel == "index.html" or u == BASE + "/": rel = "index.html"
    if rel not in pages: errs.append(f"sitemap URL has no file: {u}")
if len(sm) != len(smset): errs.append("sitemap has duplicate URLs")

# brand x part pages
bp = {rel: h for rel, h in pages.items() if re.fullmatch(r"(kia|hyundai)/[a-z-]+/index\.html", rel) and "bplist" in h}
sh = {}
for rel, h in bp.items():
    t = text_of(h); words = t.split()
    lead = re.search(r'<p class="lead">(.*?)</p>', h, re.S)
    lw = len(html.unescape(re.sub("<[^>]+>", "", lead.group(1))).split())
    if not 40 <= lw <= 60: errs.append(f"{rel}: direct answer {lw} words")
    if len(words) < 600: warns.append(f"{rel}: only {len(words)} words")
    sh[rel] = {" ".join(words[i:i + 5]) for i in range(0, len(words) - 4)}
    if len(re.findall(r'<details class="faq">', h)) != 3: errs.append(f"{rel}: not 3 FAQs")
if bp:
    wc = [len(text_of(h).split()) for h in bp.values()]
    print(f"brand x part pages {len(bp)}: words min {min(wc)} avg {sum(wc)//len(wc)} max {max(wc)}")
    # near-duplicate: share of 5-word shingles that also occur on some other page of a DIFFERENT part
    keys = list(sh)
    cnt = {}
    for k in keys:
        for s in sh[k]: cnt[s] = cnt.get(s, 0) + 1
    uniq = [sum(1 for s in sh[k] if cnt[s] == 1) / max(1, len(sh[k])) for k in keys]
    print(f"share of 5-word phrases unique to the page: min {min(uniq):.0%} avg {sum(uniq)/len(uniq):.0%}")
    pair = []
    for a, b in [(k, k.replace("kia/", "hyundai/")) for k in keys if k.startswith("kia/")]:
        if b in sh: pair.append((len(sh[a] & sh[b]) / len(sh[a] | sh[b]), a))
    if pair: print(f"kia/hyundai twin Jaccard: max {max(pair)[0]:.0%} avg {sum(p for p,_ in pair)/len(pair):.0%}")
    noi = [r for r, h in bp.items() if "noindex" in h]
    print(f"brand x part noindex: {len(noi)}; in sitemap: {sum(1 for r in bp if url_of(r) in smset)}")
    ll = (SITE / "llms.txt").read_text()
    miss = [r for r in bp if url_of(r) in smset and url_of(r) not in ll]
    if miss: errs.append(f"{len(miss)} indexed brand x part pages missing from llms.txt")
    leak = [r for r in noi if url_of(r) in ll]
    if leak: errs.append(f"{len(leak)} noindex pages in llms.txt")
print(f"pages {len(pages)}, indexable {indexed}, sitemap {len(sm)}")
for w in warns[:20]: print("WARN", w)
for x in errs[:80]: print("ERR", x)
print("FAIL" if errs else "OK", len(errs), "errors")
sys.exit(1 if errs else 0)
