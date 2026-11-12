#!/usr/bin/env python3
"""AP Car LIVE article hand-off (Edwin, 12 Nov 2026).

apcar.com.my is built by build.py --live on Dev Desk's computer (facts.json is the source of truth), not by this repo.
So the night run writes each article ONCE as data in data/articles/<slug>.json (EN/BM/ZH), runs src/check.py, and
this script turns it into Markdown files Edwin feeds to build.py --live:

    python3 autoseo-clients/apcar/src/export_md.py <slug> [OUT_DIR]

Output: OUT_DIR/<slug>/en.md, ms.md, zh.md (YAML front matter + Markdown body) + photos.txt.
Links are root paths on the live site (EN /, BM /ms/, ZH /zh/), the same paths as the pages they point to.
Nothing here builds HTML or touches the live site. Never: prices/RM, years in business, staff names, the aggregate
Google rating, 'DTC off', 'clone', 'remap'. Reviews only word for word with first names.
"""
import json, os, re, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CFG = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8"))
PHOTOS = json.load(open(os.path.join(ROOT, "data", "photos.json"), encoding="utf-8"))
LIVE = "https://apcar.com.my/"
PRE = {"en": "", "ms": "ms/", "zh": "zh/"}
LABEL = {
    "en": {"jobs": "Jobs we have done", "faq": "Questions", "related": "Related", "wa": "WhatsApp AP Car", "pair": ("Before", "After")},
    "ms": {"jobs": "Kerja yang kami buat", "faq": "Soalan", "related": "Berkaitan", "wa": "WhatsApp AP Car", "pair": ("Sebelum", "Selepas")},
    "zh": {"jobs": "我们做过的案例", "faq": "常见问题", "related": "相关页面", "wa": "WhatsApp AP Car", "pair": ("之前", "之后")},
}
BANNED = re.compile(r"\bRM ?\d|\bringgit\b|\bprice|\bharga\b|价格|\bDTC ?off\b|\bclone\b|\bremap|\b4\.3\b|\b45 (?:reviews|ulasan)|\byears? (?:in business|of experience)|\btahun pengalaman\b|年经验|guarantee|jaminan|保证", re.I)


def q(s):
    return json.dumps(s, ensure_ascii=False)


def photo(name, lang):
    if name not in PHOTOS or name.startswith("_") or name not in CFG["photos"]:
        raise SystemExit(f"photo {name} is not an approved preview photo (config.json photos)")
    p = PHOTOS[name]
    return f'![{p[lang]}](/assets/img/{name}-960.webp "{p["w"]}x{p["h"]}")'


def md(a, lang):
    L, d, pre = LABEL[lang], a[lang], PRE[lang]
    svc = CFG["services"][a["service"]]
    url = f"{LIVE}{pre}articles/{a['slug']}/"
    alts = {l: f"{LIVE}{PRE[l]}articles/{a['slug']}/" for l in PRE}
    fm = ["---", f"slug: {a['slug']}", f"lang: {lang}", f"url: {url}",
          "alternates: {" + ", ".join(f"{l}: {u}" for l, u in alts.items()) + "}",
          f"date_published: {a['published']}", f"date_modified: {a.get('updated') or a['published']}",
          f"keyword: {q(d['keyword'])}", f"title: {q(d['title'])}", f"description: {q(d['description'])}",
          f"h1: {q(d['h1'])}", f"excerpt: {q(d['excerpt'])}", f"hero_photo: /assets/img/{a['hero_photo']}-960.webp",
          f"hero_alt: {q(PHOTOS[a['hero_photo']][lang])}", f"service_page: /{pre}{svc}",
          f"whatsapp_prefill: {q(d['prefill'])}",
          "schema: Article + BreadcrumbList + FAQPage (no AggregateRating, no review stars)", "---", ""]
    b = [f"# {d['h1']}", "", d["lead"], "", f"> {d['answer']}", ""]
    for s in d["sections"]:
        b += [f"## {s['h2']}", ""]
        for p in s.get("p", []): b += [p, ""]
        if s.get("list"): b += [f"- {x}" for x in s["list"]] + [""]
        if s.get("steps"): b += [f"{i+1}. **{t}**: {x}" for i, (t, x) in enumerate(s["steps"])] + [""]
        if s.get("jobs"): b += [f"- {x}" for x in s["jobs"]] + [""]
        if s.get("pair"): b += [f"{L['pair'][0]}: {photo(s['pair'][0], lang)}", "", f"{L['pair'][1]}: {photo(s['pair'][1], lang)}", ""]
        if s.get("photo"): b += [photo(s["photo"], lang), ""]
    b += [f"## {L['faq']}", ""]
    for f in d["faqs"]: b += [f"### {f['q']}", "", f["a"], ""]
    b += [f"## {L['related']}", "", f"- [{d['h1'].split(':')[0].split('：')[0]}](/{pre}{svc})", f"- [{L['wa']}](https://wa.me/{CFG['whatsapp']}?text={quote(d['prefill'])})", ""]
    text = "\n".join(fm + b)
    m = BANNED.search(text)
    if m: raise SystemExit(f"{lang}: banned wording '{m.group(0)}'")
    return text


def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    slug = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(ROOT, "live-md")
    a = json.load(open(os.path.join(ROOT, "data", "articles", slug + ".json"), encoding="utf-8"))
    d = os.path.join(out, slug)
    os.makedirs(d, exist_ok=True)
    used = set()
    for lang in PRE:
        open(os.path.join(d, f"{lang}.md"), "w", encoding="utf-8").write(md(a, lang))
        for s in a[lang]["sections"]:
            used.update([s["photo"]] if s.get("photo") else []); used.update(s.get("pair", []))
    used.add(a["hero_photo"])
    open(os.path.join(d, "photos.txt"), "w").write("".join(f"/assets/img/{n}-960.webp\n/assets/img/{n}-480.webp\n" for n in sorted(used)))
    print(f"OK: {d} (en.md, ms.md, zh.md, photos.txt)")


if __name__ == "__main__":
    main()
