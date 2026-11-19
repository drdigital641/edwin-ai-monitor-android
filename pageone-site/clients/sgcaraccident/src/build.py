#!/usr/bin/env python3
"""SGCarAccident preview builder. ONE shared layout (head, emergency row, header, footer, Call-hotline dock, tracker)
for every page in EN (root) and ZH (/zh/). Copy lives in content_en.py / content_zh.py, verified facts in
../research/facts.json. Run: python3 build.py -> ../site/. Rebuild, then upload site/ through the Bridge."""
import json, os, re, html, hashlib, shutil, urllib.parse, datetime, importlib

SRC = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(SRC), "site")
FACTS = json.load(open(os.path.join(os.path.dirname(SRC), "research", "facts.json")))
ORIGIN = "https://pageonesingapore.com"
BASE = "/preview/sgcaraccident/"
WA_NUMBER = "6589976612"  # hotline: used only inside wa.me links, never shown
API = "https://sgcar-accident-settlement-4d8df539.base44.app/api/settle"
TODAY = datetime.date.today().isoformat()
E = html.escape
L = {"en": importlib.import_module("content_en"), "zh": importlib.import_module("content_zh")}

def sha8(p):
    return hashlib.sha256(open(os.path.join(SRC, "assets", p), "rb").read()).hexdigest()[:8]
V = {k: sha8(k) for k in ["site.css", "site.js", "settle.js", "p1-cta.js", "jspdf.umd.min.js"]}

def url(lang, path=""):
    return BASE + ("zh/" if lang == "zh" else "") + path

def absu(lang, path=""):
    return ORIGIN + url(lang, path)

def wa(lang, key):
    return "https://wa.me/%s?text=%s" % (WA_NUMBER, urllib.parse.quote(L[lang].WA[key]))

# ---------------- verified facts (EN from official pages; ZH is a faithful rendering) ----------------
GIA_URL = FACTS["gia_24h"]["url"]
SPF = FACTS["spf_police_cases"]
FACT_TEXT = {
    "en": {
        "gia_24h": "The GIA Motor Claims Framework says: report the accident to your insurer within 24 hours or by the next working day. Take your vehicle, damaged or not, to your insurer's approved reporting centre or authorised workshop.",
        "police_cases": ["Someone died", "Someone was taken to hospital by ambulance, or got 3 or more days of medical leave", "Government property was damaged", "A foreign vehicle was involved", "A pedestrian or cyclist was involved", "Hit and run"],
        "spf_how": "Report online through the SPF e-services Traffic Accident Report (Singpass needed) or at any police station. A Police report does not replace your report to your insurer.",
    },
    "zh": {
        "gia_24h": "根据新加坡通用保险协会（GIA）汽车索赔框架：须在24小时内或下一个工作日之前向保险公司报案。无论车辆是否受损，都要把车开到保险公司认可的报案中心或授权车厂。",
        "police_cases": ["有人死亡", "有人被救护车送院，或获得3天或以上的病假", "政府财产受损", "涉及外国车辆", "涉及行人或骑脚车者", "肇事逃逸"],
        "spf_how": "可通过新加坡警察部队（SPF）电子服务的交通事故报告在线报案（需要Singpass），或到任何警署报案。向警方报案不能代替向保险公司报案。",
    },
}
SOURCES = [("GIA: Do's and don'ts following an accident", GIA_URL), ("SPF: Reporting traffic accidents", SPF["url"])]

# ---------------- icons (one authored set, 2px stroke) ----------------
def ic(p, fill=False):
    a = 'fill="currentColor"' if fill else 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    return '<svg viewBox="0 0 24 24" aria-hidden="true" %s>%s</svg>' % (a, p)
I_WA = ic('<path d="M12 2.2A9.7 9.7 0 0 0 3.7 16.9L2.3 21.8l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.5Z"/>', True)
ICONS = {
    "own-damage": ic('<path d="M3 16v-3l2-5h9l3 4h3a1 1 0 0 1 1 1v3"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="m11 4 1 2 2-1"/>'),
    "third-party": ic('<path d="M12 3 4 6v6c0 4.5 3.4 7.8 8 9 4.6-1.2 8-4.5 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>'),
    "settlement": ic('<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8l-5-5Z"/><path d="M14 3v5h5"/><path d="M8 17c1.5-1.5 2.5-1.5 3 0s1.5 1.5 3-1"/>'),
    "report": ic('<path d="M9 4h6v3H9z"/><path d="M8 5H6a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2"/><path d="M9 12h6M9 16h4"/>'),
    "windscreen": ic('<path d="M3 17c0-6 4-10 9-10s9 4 9 10H3Z"/><path d="m11 9 2 3-2 2 2 3"/>'),
    "tow": ic('<path d="M2 17V9h7l3 4h6a2 2 0 0 1 2 2v2"/><circle cx="6" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M12 13V6l6-2"/>'),
}
LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="2" y="2" width="28" height="28" rx="6" fill="#0B5A8C"/>'
        '<path d="M16 7 26 24H6L16 7Z" fill="none" stroke="#F2A900" stroke-width="2.6" stroke-linejoin="round"/>'
        '<path d="M16 13v5" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/><circle cx="16" cy="21.2" r="1.5" fill="#fff"/></svg>')

def hotline(lang, key, ref, label=None, cls="btn btn-go block"):
    t = L[lang].T
    return '<a class="%s" href="%s" target="_blank" rel="noopener" data-ref="%s">%s<span>%s</span></a>' % (
        cls, E(wa(lang, key)), E(ref), I_WA, E(label or t["call_hotline"]))

def sos(lang, ref):
    t = L[lang].T
    return ('<nav class="sos" aria-label="Emergency" data-ref="%s"><a class="s-red" href="tel:999"><b>999</b>%s</a>'
            '<a class="s-amb" href="tel:995"><b>995</b>%s</a><a class="s-tow" href="%s" target="_blank" rel="noopener" data-ref="%s-tow"><b>%s</b>%s</a></nav>') % (
        E(ref), E(t["police"]), E(t["ambulance"]), E(wa(lang, "tow")), E(ref), ICONS["tow"].replace('<svg ', '<svg width="22" height="22" '), E(t["tow"]))

def jsonld(o):
    return '<script type="application/ld+json">%s</script>' % json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

def faq_block(lang, faq):
    t = L[lang].T
    if not faq:
        return "", None
    h = '<section class="faq"><h2>%s</h2>%s</section>' % (E(t["faq_h"]), "".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (E(q), E(a)) for q, a in faq))
    sd = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    return h, sd

def page(lang, path, title, desc, body, key, ref, schema=(), alt=True, robots_extra="", scripts=("site.js",), crumbs=None):
    """The ONE shared layout. key = WhatsApp prefill for this page's dock; ref = tap label prefix (path name)."""
    t = L[lang].T
    other = "zh" if lang == "en" else "en"
    links = ""
    if alt:
        links = ('<link rel="alternate" hreflang="en-SG" href="%s"><link rel="alternate" hreflang="zh-Hans-SG" href="%s">'
                 '<link rel="alternate" hreflang="x-default" href="%s">') % (absu("en", path), absu("zh", path), absu("en", path))
    bc = ""
    if crumbs:
        items = [(t["home"], url(lang))] + crumbs
        bc = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % " / ".join(
            '<a href="%s">%s</a>' % (E(u), E(n)) if u else E(n) for n, u in items)
        schema = list(schema) + [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + (u or url(lang, path))} for i, (n, u) in enumerate(items)]}]
    js = "".join('<script src="%s" defer></script>' % E(url("en", "assets/%s?v=%s" % (s, V[s]))) for s in scripts)
    srcs = " ".join('<a href="%s" rel="noopener">%s</a>' % (E(u), E(n)) for n, u in SOURCES)
    return """<!doctype html>
<html lang="%(hl)s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>%(title)s</title><meta name="description" content="%(desc)s"><meta name="robots" content="noindex, nofollow%(rx)s">
<link rel="canonical" href="%(canon)s">%(alts)s
<meta property="og:type" content="website"><meta property="og:title" content="%(title)s"><meta property="og:description" content="%(desc)s"><meta property="og:url" content="%(canon)s"><meta property="og:locale" content="%(ogl)s">
<meta name="theme-color" content="#0B5A8C"><link rel="icon" href="%(fav)s" type="image/svg+xml">
%(preload)s<link rel="stylesheet" href="%(css)s"><script>document.documentElement.className+=" js"</script>
%(schema)s</head>
<body><a class="skip" href="#main">%(skip)s</a>
%(sos)s
<header class="hd"><a class="logo" href="%(home)s">%(logo)s<span>%(brand)s</span></a><a class="lang" href="%(olink)s" hreflang="%(ohl)s" lang="%(ohl)s">%(switch)s</a></header>
<main id="main" class="wrap">%(bc)s%(body)s</main>
<footer class="ft"><div class="wrap"><div class="links"><a href="%(home)s">%(all)s</a><a href="%(ins)s">%(insl)s</a><a href="%(priv)s">%(privl)s</a></div>
<p>%(disc)s</p><p class="srcs">%(srcl)s: %(srcs)s</p></div></footer>
<div class="dock">%(dock)s</div>
<script src="%(cta)s" defer></script>%(js)s
</body></html>
""" % {
        "hl": t["html_lang"], "title": E(title), "desc": E(desc), "rx": robots_extra, "canon": absu(lang, path), "alts": links,
        "ogl": "en_SG" if lang == "en" else "zh_SG", "fav": url("en", "assets/icon.svg"),
        "preload": ('<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' % url("en", "assets/barlow-semi-condensed-latin-700-normal.woff2")) if lang == "en" else "",
        "css": url("en", "assets/site.css?v=" + V["site.css"]), "schema": "".join(jsonld(s) for s in schema if s),
        "skip": E(t["skip"]), "sos": sos(lang, ref + ":sos"), "home": url(lang), "logo": LOGO, "brand": E(t["brand"]),
        "olink": url(other, path), "ohl": "zh-Hans" if other == "zh" else "en", "switch": E(t["switch_label"]), "bc": bc, "body": body,
        "all": E(t["all_guides"]), "ins": url(lang, "insurers/"), "insl": E(t["insurers_link"]), "priv": url(lang, "privacy/"), "privl": E(t["privacy"]),
        "disc": E(t["disclaimer"]), "srcl": E(t["sources"]), "srcs": srcs, "dock": hotline(lang, key, ref + ":dock"),
        "cta": url("en", "assets/p1-cta.js?v=" + V["p1-cta.js"]), "js": js,
    }

# ---------------- insurers ----------------
NAMES = {  # display name, what the source list is (EN, ZH)
    "income": ("Income Insurance", "reporting centres", "报案中心名单"),
    "aig": ("AIG", "approved reporting centres", "认可报案中心名单"),
    "qbe": ("QBE", "approved reporting centres and authorised motor workshops (dated May 2024)", "认可报案中心和授权车厂名单（2024年5月版）"),
    "etiqa": ("Etiqa", "authorised motor workshops (private and light commercial)", "授权车厂名单（私家车和轻型商用车）"),
    "tokiomarine": ("Tokio Marine", "approved workshops, where Tokio Marine says accidents are reported", "认可车厂名单（Tokio Marine表示在这些车厂报案）"),
    "greateastern": ("Great Eastern General", "authorised workshops", "授权车厂名单"),
    "directasia": ("DirectAsia", "authorised workshops", "授权车厂名单"),
    "budgetdirect": ("Budget Direct", "authorised workshops and accident reporting centres", "授权车厂和事故报案中心名单"),
    "msig": ("MSIG", "motor claims workshops", "汽车索赔车厂名单"),
    "liberty": ("Liberty Insurance", "accident reporting point", "事故报案点"),
    "sompo": ("Sompo", "ExcelDrive workshops and accident reporting centres", "ExcelDrive车厂和事故报案中心名单"),
    "allianz": ("Allianz", "Motor Protect workshop list", "Motor Protect车厂名单"),
    "singlife": ("Singlife", "authorised car repairers", "授权修车厂名单"),
}
REGIONS = [("North", "北部"), ("East", "东部"), ("West", "西部"), ("Central", "中部"), ("South", "南部")]
DROP = re.compile(r"hours not shown|as printed|document layout|postal|page spells|customers only|incomplete|unc$|^\s*$", re.I)

def clean_note(n):
    parts = [p.strip() for p in re.split(r";", n or "")]
    keep = []
    for p in parts:
        if DROP.search(p):
            continue
        if re.search(r"\b(North|South|East|West|Central)\b", p) and len(p) < 22:
            continue  # region shown separately
        keep.append(re.sub(r"\s*\(as stated\)", "", p))
    return "; ".join(keep)

def region_of(n):
    hit = [en for en, zh in REGIONS if re.search(r"\b%s\b" % en, n or "")]
    return hit[0] if hit else ""

INSURERS = []
for ins in FACTS["insurers"]:
    if ins["slug"] not in NAMES:
        continue
    cs = []
    for c in ins["centres"]:
        if not c.get("address"):
            continue
        cs.append({"address": c["address"].strip(), "hours": (c.get("hours") or "").strip(), "region": region_of(c.get("notes", "")), "note": clean_note(c.get("notes", ""))})
    seen, uniq = set(), []
    for c in cs:
        k = re.sub(r"\W", "", c["address"].lower())
        if k not in seen:
            seen.add(k); uniq.append(c)
    order = {r[0]: i for i, r in enumerate(REGIONS)}
    uniq.sort(key=lambda c: (order.get(c["region"], 9), c["address"]))
    INSURERS.append({"slug": ins["slug"], "name": NAMES[ins["slug"]][0], "kind": NAMES[ins["slug"]][1:], "centres": uniq, "src": ins["source_url"].replace(" ", "%20"), "read": ins.get("read", "2026-11-19")})
INSURERS.sort(key=lambda x: x["name"])

def chips(lang, ref):
    return '<div class="chips" data-ref="%s">%s</div>' % (E(ref), "".join(
        '<a href="%s">%s</a>' % (url(lang, "insurers/%s/" % i["slug"]), E(i["name"])) for i in INSURERS))

# ---------------- flows ----------------
def fill(lang, s):
    ft = FACT_TEXT[lang]
    return s.replace("{gia_24h}", ft["gia_24h"]).replace("{spf_how}", ft["spf_how"])

def acts(lang, ref, optional):
    t = L[lang].T
    return ('<div class="acts"%s><a class="a-red" href="tel:995">995 %s</a><a class="a-red" href="tel:999">999 %s</a>'
            '<a class="a-tow" href="%s" target="_blank" rel="noopener" data-ref="%s">%s</a></div>') % (
        ' data-opt' if optional else "", E(t["ambulance"]), E(t["police"]), E(wa(lang, "tow")), E(ref + ":tow"), E(t["tow"]))

def flow_page(lang, slug):
    C = L[lang]; t = C.T; F = C.FLOWS[slug]
    steps = []
    for k, s in enumerate(F["steps"]):
        h = '<h2>%s</h2>' % E(s["h"])
        for p in s.get("p", []):
            h += "<p>%s</p>" % E(fill(lang, p))
        li = s.get("li")
        if li == "{police_cases}":
            li = FACT_TEXT[lang]["police_cases"]
        if li:
            h += "<ul>%s</ul>" % "".join("<li>%s</li>" % E(x) for x in li)
        for p in s.get("p2", []):
            h += "<p>%s</p>" % E(fill(lang, p))
        if s.get("li2"):
            h += "<ul>%s</ul>" % "".join("<li>%s</li>" % E(x) for x in s["li2"])
        if s.get("ch"):
            h += '<div class="choices">%s</div>' % "".join(
                '<button type="button" class="choice" data-k="%s" aria-pressed="false">%s</button>' % (E(c[0]), E(c[1])) for c in s["ch"])
            h += "".join('<p class="note" data-k="%s">%s</p>' % (E(c[0]), E(c[2])) for c in s["ch"])
        if s.get("act"):
            h += acts(lang, slug, bool(s.get("ch")))
        if s.get("chips"):
            h += chips(lang, slug + ":insurer-chips")
        end = ""
        if s.get("cta"):
            h += '<div class="endcta">%s<a class="btn btn-ghost block" href="%s">%s</a></div>' % (
                hotline(lang, s["cta"], slug + ":end"), url(lang), E(t["all_guides"]))
            end = " data-end"
        steps.append('<section class="step" id="s%d"%s>%s</section>' % (k + 1, end, h))
    faq_h, faq_sd = faq_block(lang, F["faq"])
    body = """<h1 class="page-h1">%s</h1><p class="lead">%s</p>
<div class="prog" aria-hidden="true"><i></i></div><p class="prog-l" data-tpl="%s" aria-live="polite"></p>
<div class="flow">%s</div>
<div class="nav"><button type="button" class="btn btn-ghost" data-back>%s</button><button type="button" class="btn btn-sign" data-next>%s</button></div>
<p class="allsteps"><a href="#" data-all>%s</a></p>
%s""" % (E(F["h1"]), E(F["lead"]), E(t["step_of"]), "".join(steps), E(t["back"]), E(t["next"]), E(t["read_all"]), faq_h)
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": F["h1"], "step": [
        {"@type": "HowToStep", "position": i + 1, "name": s["h"]} for i, s in enumerate(F["steps"]) if not s.get("cta")]}
    return page(lang, slug + "/", F["title"], F["desc"], body, slug, slug, schema=[faq_sd, howto], crumbs=[(F["nav"], None)])

# ---------------- home ----------------
TRIAGE = {
    "tow": ["tow", "towing", "can't drive", "cannot drive", "won't start", "stuck", "breakdown", "拖车", "拖", "开不动", "不能开"],
    "windscreen": ["windscreen", "windshield", "glass", "crack", "chip", "挡风", "玻璃", "裂"],
    "settlement": ["settle", "settlement", "private", "privately", "agree", "pay me", "pay him", "pay her", "私了", "和解", "私下"],
    "report": ["report", "police", "where to report", "reporting", "报案", "报警", "报告", "警察"],
    "third-party": ["not my fault", "hit me", "hit my", "rear-ended me", "rear ended me", "banged me", "bumped me", "knocked me", "crashed into me", "reversed into me", "other driver", "他撞", "撞到我", "被撞", "不是我的错", "对方"],
    "own-damage": ["my fault", "i hit", "i banged", "i bumped", "i knocked", "i crashed", "i reversed", "i scratched", "own damage", "我撞", "我的错", "我倒车", "自己"],
}
HURT = ["hurt", "injur", "blood", "bleed", "pain", "ambulance", "unconscious", "受伤", "流血", "救护", "痛", "昏"]

def home(lang):
    C = L[lang]; t = C.T; H = C.HOME
    def tile(slug, cls=""):
        b, s = H["cards"][slug]
        return '<a class="tile %s" href="%s" data-ref="home:%s">%s<b>%s</b><small>%s</small></a>' % (cls, url(lang, slug + "/"), slug, ICONS[slug], E(b), E(s))
    rules = {"paths": [{"u": url(lang, k + "/"), "l": H["cards"][k][0], "k": v} for k, v in TRIAGE.items()], "hurt": HURT,
             "msg": {"hit": H["triage_hit"], "none": H["triage_none"], "hurt": H["triage_hurt"]}}
    faq_h, faq_sd = faq_block(lang, H["faq"])
    body = """<section class="hero"><h1>%s</h1>
<form class="triage" role="search" data-rules="%s"><label for="tri">%s</label><div class="row"><input id="tri" type="text" autocomplete="off" enterkeyhint="go" placeholder="%s"><button type="submit">%s</button></div><div class="out" aria-live="polite"></div></form></section>
<section class="group"><h2>%s</h2><div class="tiles">%s%s</div></section>
<section class="group"><h2>%s</h2><div class="tiles">%s%s</div></section>
<section class="group"><h2>%s</h2><div class="tiles">%s%s</div></section>
<div class="lane" aria-hidden="true"></div>
<section class="group"><h2>%s</h2><p>%s</p>%s</section>
%s""" % (
        h1_split(H["h1"]), E(json.dumps(rules, ensure_ascii=False)), E(H["triage_label"]), E(H["triage_ph"]), E(H["triage_go"]),
        E(H["g_cause"]), tile("own-damage", "alt"), tile("third-party"),
        E(H["g_report"]), tile("settlement"), tile("report", "alt"),
        E(H["g_other"]), tile("windscreen", "alt"), tile("tow", "warn"),
        E(H["g_insurer"]), E(H["g_insurer_p"]), chips(lang, "home:insurer-chips"), faq_h)
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "SGCarAccident", "url": absu(lang), "inLanguage": t["html_lang"]}
    return page(lang, "", H["title"], H["desc"], body, "home", "home", schema=[site, faq_sd])

def h1_split(h):
    # "Had an accident? We'll guide you, step by step." -> question line + answer line in sign blue
    m = re.match(r"^(.+?[?？])\s*(.+)$", h)
    return E(h) if not m else "%s <span>%s</span>" % (E(m.group(1)), E(m.group(2)))

# ---------------- insurer pages ----------------
def insurer_index(lang):
    C = L[lang]; t = C.T; F = C.FLOWS["insurers"]
    lis = "".join('<a href="%s" data-ref="insurers:index">%s<span>%d</span></a>' % (url(lang, "insurers/%s/" % i["slug"]), E(i["name"]), len(i["centres"])) for i in INSURERS)
    body = '<h1 class="page-h1">%s</h1><p class="lead">%s</p><div class="ins-index">%s</div><p class="src">%s</p><div class="endcta">%s</div>' % (
        E(F["h1"]), E(F["lead"]), lis, E(F["missing"]), hotline(lang, "insurers", "insurers:index-end"))
    il = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": i["name"], "url": absu(lang, "insurers/%s/" % i["slug"])} for k, i in enumerate(INSURERS)]}
    return page(lang, "insurers/", F["title"], F["desc"], body, "insurers", "insurers", schema=[il], crumbs=[(F["nav"], None)])

def insurer_page(lang, ins):
    C = L[lang]; t = C.T; P = C.INSURER_PAGE; n = ins["name"]
    has_hours = any(c["hours"] for c in ins["centres"])
    reg_zh = dict(REGIONS)
    out, cur = [], None
    for k, c in enumerate(ins["centres"]):
        if c["region"] != cur and any(x["region"] for x in ins["centres"]):
            cur = c["region"]
            out.append('<h2 class="region">%s</h2>' % E((reg_zh.get(cur, cur) if lang == "zh" else cur) or ("其他" if lang == "zh" else "Other areas")))
        q = urllib.parse.quote(c["address"])
        out.append('<div class="ins"><h3>%s</h3>%s%s<a class="map" href="https://www.google.com/maps/search/?api=1&amp;query=%s" target="_blank" rel="noopener">%s</a></div>' % (
            E(c["address"]), ('<p class="meta">%s: %s</p>' % (E(t["hours"]), E(c["hours"])) if c["hours"] else ""),
            ('<p class="meta">%s</p>' % E(c["note"]) if c["note"] else ""), q, E(t["map"])))
    kind = ins["kind"][0] if lang == "en" else ins["kind"][1]
    src = '<p class="src">%s: <a href="%s" rel="noopener">%s %s</a>, %s %s.</p>' % (
        E(t["source"]), E(ins["src"]), E(n), E(kind), E(t["read_on"]), E(ins["read"]))
    faq = [[q.replace("{name}", n), a.replace("{name}", n)] for q, a in P["faq"]]
    faq_h, faq_sd = faq_block(lang, faq)
    body = '<h1 class="page-h1">%s</h1><p class="lead">%s</p>%s<div class="remind">%s</div><div class="ins-list">%s</div>%s<div class="endcta">%s</div>%s' % (
        E(P["h1"].replace("{name}", n)), E(P["lead"]), src, E(FACT_TEXT[lang]["gia_24h"]), "".join(out), src,
        hotline(lang, "insurers", "insurer:" + ins["slug"]), faq_h)
    title = P["title"].replace("{name}", n)
    desc = P["desc"].replace("{name}", n).replace("{hours_bit}", P["hours_bit"] if has_hours else "")
    return page(lang, "insurers/%s/" % ins["slug"], title, desc, body, "insurers", "insurer:" + ins["slug"], schema=[faq_sd],
                crumbs=[(C.FLOWS["insurers"]["nav"], url(lang, "insurers/")), (n, None)])

# ---------------- settlement ----------------
def field(name, label, typ="text", req=True, extra="", ph=""):
    return '<div class="field"><label for="f-%s">%s</label><input id="f-%s" name="%s" type="%s" %s%s%s></div>' % (
        name, E(label), name, name, typ, 'data-req ' if req else "", extra, (' placeholder="%s"' % E(ph)) if ph else "")

def party_fields(S, p, req_contact):
    return (field(p + "_name", S["name"], extra='autocomplete="%s" maxlength="80"' % ("name" if p == "a" else "off"))
            + '<div class="two">' + field(p + "_nric", S["nric"], extra='maxlength="4" pattern="[0-9A-Za-z]{4}" autocapitalize="characters"', ph=S["nric_ph"])
            + field(p + "_phone", S["phone"], "tel", req_contact, 'inputmode="tel" maxlength="20" autocomplete="%s"' % ("tel" if p == "a" else "off")) + "</div>"
            + '<div class="two">' + field(p + "_vehicle_no", S["vehicle_no"], extra='maxlength="12" autocapitalize="characters"')
            + field(p + "_vehicle_make", S["vehicle_make"], req=False, extra='maxlength="60"') + "</div>"
            + field(p + "_insurer", S["insurer"], extra='maxlength="60" list="insurer-list"'))

def settle_strings(lang):
    S = dict(L[lang].SETTLE); S.update({k: L[lang].T[k] for k in ["back", "next"]})
    return '<script type="application/json" id="settle-strings">%s</script>' % json.dumps(S, ensure_ascii=False).replace("</", "<\\/")

def settlement(lang):
    C = L[lang]; t = C.T; S = C.SETTLE; F = C.FLOWS["settlement"]
    dl = '<datalist id="insurer-list">%s</datalist>' % "".join('<option value="%s">' % E(i["name"]) for i in INSURERS)
    steps = [
        '<section class="step"><h2>%s</h2><div class="two">%s%s</div>%s<div class="field"><label for="f-description">%s</label><textarea id="f-description" name="description" maxlength="500" placeholder="%s"></textarea></div></section>' % (
            E(S["s_accident"]), field("accident_date", S["date"], "date"), field("accident_time", S["time"], "time", False),
            field("location", S["location"], extra='maxlength="160"', ph=S["location_ph"]), E(S["description"]), E(S["description_ph"])),
        '<section class="step"><h2>%s</h2>%s</section>' % (E(S["s_a"]), party_fields(S, "a", False)),
        '<section class="step"><h2>%s</h2>%s</section>' % (E(S["s_b"]), party_fields(S, "b", False)),
        '<section class="step"><h2>%s</h2><div class="field"><div class="opts" data-req tabindex="-1"><label class="opt"><input type="radio" name="settlement_option" value="A"><span>%s</span></label><label class="opt"><input type="radio" name="settlement_option" value="B"><span>%s</span></label></div></div>'
        '<div data-if-b hidden><div class="field"><span class="lbl">%s</span><div class="opts" data-req tabindex="-1"><label class="opt"><input type="radio" name="payer" value="a"><span>%s</span></label><label class="opt"><input type="radio" name="payer" value="b"><span>%s</span></label></div></div>%s</div></section>' % (
            E(S["s_agree"]), E(S["opt_a"]), E(S["opt_b"]), E(S["payer"]), E(S["payer_a"]), E(S["payer_b"]),
            field("amount", S["amount"], "text", True, 'inputmode="decimal" maxlength="10" pattern="\\d{1,7}(\\.\\d{1,2})?"')),
        '<section class="step"><h2>%s</h2><p>%s</p><label class="btn btn-ghost block" for="photoIn">%s</label><input id="photoIn" class="vh" type="file" accept="image/*" multiple><div class="thumbs" id="thumbs"></div></section>' % (
            E(S["s_photos"]), E(S["photos_p"]), E(S["add_photo"])),
        '<section class="step" data-review><h2>%s</h2><div class="review" id="reviewA"></div><p class="lbl"><strong>%s</strong></p><div class="pad" id="padA"><canvas></canvas><button type="button" class="clr">%s</button></div>'
        '<label class="tick"><input type="checkbox" name="consent"><span>%s</span></label><p class="privacy-note">%s <a href="%s">%s</a></p><div class="remind">%s</div></section>' % (
            E(S["s_sign"]), E(S["sign_here"]), E(S["clear"]), E(S["consent"]), E(S["privacy_note"]), url(lang, "privacy/"), E(t["privacy"]), E(S["remind"])),
    ]
    body = """<h1 class="page-h1">%(h1)s</h1><p class="lead">%(lead)s</p>
<div id="settle" data-api="%(api)s" data-lang="%(lang)s" data-sign="%(sign)s">
<div id="settle-intro"><div class="intro"><ul>%(intro)s</ul></div><div class="remind">%(remind)s</div><button type="button" class="btn btn-sign block" data-start>%(start)s</button>
<noscript><p class="err">JavaScript is needed for this form.</p></noscript></div>
<form id="settle-form" class="form" hidden novalidate>
<div class="prog" aria-hidden="true"><i></i></div><p class="prog-l" data-tpl="%(stepof)s" aria-live="polite"></p>
%(steps)s<p class="err" role="alert"></p>
<div class="nav" style="display:grid"><button type="button" class="btn btn-ghost" data-back>%(back)s</button><button type="button" class="btn btn-sign" data-next>%(next)s</button><button type="submit" class="btn btn-go" data-save hidden><span>%(save)s</span></button></div>
</form>
<div id="settle-done" hidden><div class="step" style="display:block"><h2>%(done_h)s</h2><p>%(done_p)s</p><div class="endcta">
<button type="button" class="btn btn-sign block" data-pdf>%(dl)s</button><button type="button" class="btn btn-go block" data-share data-cta="share_link">%(share)s</button>
<input id="shareLink" readonly aria-label="%(share)s" style="width:100%%;min-height:48px;font-size:14px;border:1px solid #D5DEE5;border-radius:6px;padding:0 10px"><p data-copied aria-live="polite"></p></div>
<div class="remind">%(remind)s</div></div></div>
</div>%(dl_list)s%(strings)s
%(faq)s""" % {
        "h1": E(F["h1"]), "lead": E(F["lead"]), "api": API, "lang": lang, "sign": url(lang, "private-settlement/sign/"),
        "intro": "".join("<li>%s</li>" % E(x) for x in S["intro_li"]), "remind": E(S["remind"]), "start": E(S["start"]),
        "stepof": E(t["step_of"]), "steps": "".join(steps), "back": E(t["back"]), "next": E(t["next"]), "save": E(S["save"]),
        "done_h": E(S["done_h"]), "done_p": E(S["done_p"]), "dl": E(S["download"]), "share": E(S["share"]),
        "dl_list": dl, "strings": settle_strings(lang), "faq": "",
    }
    faq = SETTLE_FAQ[lang]
    faq_h, faq_sd = faq_block(lang, faq)
    body = body.replace('%(faq)s', '') + faq_h
    return page(lang, "private-settlement/", F["title"], F["desc"], body, "settlement", "settlement", schema=[faq_sd],
                scripts=("jspdf.umd.min.js", "settle.js"), crumbs=[(F["nav"], None)])

SETTLE_FAQ = {
    "en": [["Is a private settlement legal in Singapore?", "Yes, drivers can agree to settle privately. You must still report the accident to your own insurer within 24 hours or by the next working day."],
           ["What goes into a private settlement form?", "Both drivers' particulars, vehicles and insurers, the date, time and place, a short description, how it is settled (no payment, or an agreed amount) and both signatures."],
           ["Can the other driver sign on their own phone?", "Yes. Share the secure link. They check the details and sign on screen, and either of you can then download the signed PDF."]],
    "zh": [["在新加坡私下和解合法吗？", "可以，双方司机可以同意私下和解。但您仍须在24小时内或下一个工作日之前向自己的保险公司报案。"],
           ["私下和解表格要填什么？", "双方司机的资料、车辆和保险公司，事故日期、时间和地点，简短经过，和解方式（互不赔偿，或约定金额），以及双方签名。"],
           ["对方司机可以用自己的手机签名吗？", "可以。分享安全链接，对方核对资料后在屏幕上签名，之后双方都可以下载已签署的PDF。"]],
}

def sign_page(lang):
    C = L[lang]; t = C.T; S = C.SETTLE
    body = """<h1 class="page-h1">%s</h1><p class="lead">%s</p>
<div id="settle" data-api="%s" data-lang="%s" data-sign="%s"><p id="sign-msg" class="err" aria-live="polite"></p>
<div id="sign-view" hidden><div class="step" style="display:block"><div class="review" id="reviewB"></div></div>
<form id="sign-form" novalidate><div class="step" style="display:block"><p><strong>%s</strong></p><div class="pad" id="padB"><canvas></canvas><button type="button" class="clr">%s</button></div>
<label class="tick"><input type="checkbox" name="consent"><span>%s</span></label><p class="privacy-note">%s</p><p class="err" role="alert"></p>
<button type="submit" class="btn btn-go block">%s</button><div class="remind">%s</div></div></form>
<div id="signed" hidden><div class="step" style="display:block"><h2>%s</h2><p>%s</p><button type="button" class="btn btn-sign block" data-pdf>%s</button><div class="remind">%s</div></div></div>
</div></div>%s""" % (
        E(S["sign_h1"]), E(S["sign_lead"]), API, lang, url(lang, "private-settlement/sign/"), E(S["sign_wrong"]), E(S["clear"]),
        E(S["consent"]), E(S["privacy_note"]), E(S["sign_btn"]), E(S["remind"]), E(S["signed_h"]), E(S["signed_p"]), E(S["download"]), E(S["remind"]),
        settle_strings(lang))
    return page(lang, "private-settlement/sign/", S["sign_h1"] + " | SGCarAccident", S["sign_lead"], body, "settlement", "settlement-sign",
                alt=False, robots_extra=", noarchive", scripts=("jspdf.umd.min.js", "settle.js"))

def privacy(lang):
    P = L[lang].PRIVACY
    body = '<h1 class="page-h1">%s</h1>%s' % (E(P["h1"]), "".join("<p>%s</p>" % E(p) for p in P["body"]))
    return page(lang, "privacy/", P["title"], P["desc"], body, "home", "privacy", crumbs=[(P["h1"], None)])

def notfound(lang):
    t = L[lang].T; H = L[lang].HOME
    tiles = "".join('<a class="tile" href="%s">%s<b>%s</b><small>%s</small></a>' % (url(lang, k + "/"), ICONS[k], E(v[0]), E(v[1])) for k, v in H["cards"].items())
    body = '<h1 class="page-h1">%s</h1><p class="lead">%s</p><div class="tiles">%s</div>' % (E(t["not_found"]), E(t["not_found_p"]), tiles)
    return page(lang, "404.html", t["not_found"] + " | SGCarAccident", t["not_found_p"], body, "home", "404", alt=False)

# ---------------- write ----------------
def write(rel, s):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets"))
    for f in os.listdir(os.path.join(SRC, "assets")):
        shutil.copy(os.path.join(SRC, "assets", f), os.path.join(OUT, "assets", f))
    open(os.path.join(OUT, "assets", "icon.svg"), "w").write(LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '))
    paths = []
    for lang in ("en", "zh"):
        pre = "zh/" if lang == "zh" else ""
        write(pre + "index.html", home(lang)); paths.append("")
        for slug in ["own-damage", "third-party", "report", "windscreen", "tow"]:
            write(pre + slug + "/index.html", flow_page(lang, slug)); paths.append(slug + "/")
        write(pre + "private-settlement/index.html", settlement(lang)); paths.append("private-settlement/")
        write(pre + "private-settlement/sign/index.html", sign_page(lang))
        write(pre + "insurers/index.html", insurer_index(lang)); paths.append("insurers/")
        for ins in INSURERS:
            write(pre + "insurers/%s/index.html" % ins["slug"], insurer_page(lang, ins)); paths.append("insurers/%s/" % ins["slug"])
        write(pre + "privacy/index.html", privacy(lang)); paths.append("privacy/")
        write(pre + "404.html", notfound(lang))
    paths = sorted(set(paths), key=paths.index)
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for p in paths:
        for lang in ("en", "zh"):
            sm.append("<url><loc>%s</loc><lastmod>%s</lastmod>"
                      '<xhtml:link rel="alternate" hreflang="en-SG" href="%s"/><xhtml:link rel="alternate" hreflang="zh-Hans-SG" href="%s"/><xhtml:link rel="alternate" hreflang="x-default" href="%s"/></url>'
                      % (absu(lang, p), TODAY, absu("en", p), absu("zh", p), absu("en", p)))
    sm.append("</urlset>")
    write("sitemap.xml", "\n".join(sm) + "\n")
    # robots.txt for the future domain (sgcaraccident.sg). In the preview folder it has no effect; the preview stays noindex.
    write("robots.txt", "User-agent: *\nDisallow: /private-settlement/sign/\nDisallow: /zh/private-settlement/sign/\n\nSitemap: https://sgcaraccident.sg/sitemap.xml\n")
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("built", n, "files,", len(paths) * 2, "sitemap urls,", len(INSURERS), "insurers")

if __name__ == "__main__":
    import sys
    sys.path.insert(0, SRC)
    main()
