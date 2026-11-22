#!/usr/bin/env python3
"""SGCarAccident v2 builder (21 Nov 2026): an accident-help APP, not a workshop site.
One homepage, three accident situations, one next step at a time.

ONE shared layout for every page in EN (root) and ZH (/zh/). Copy lives in content_en.py / content_zh.py,
articles in guides_en.py / guides_zh.py, verified facts in ../research/facts.json (+ research_addendum.json).
Host-dependent tags (canonical, hreflang, og:image, sitemap, robots) come from site.json through golive.py
(the one-switch go-live module). Preview hiding is the host-conditional X-Robots header in preview/.htaccess,
never a per-page tag.

Every enquiry goes to Edwin's WhatsApp (number used only inside wa.me links, never shown) and carries a
pathway category + reference + consent line (assets/lead.js). Categories are in LEAD_PATHWAYS below; the
same keys are the future lead-routing keys (workshops, reporting-centre referrals, partner fees).

Run: python3 build.py -> ../site/. Then commit and Bridge sync_from_github (base_path preview/sgcaraccident)."""
import json, os, re, html, hashlib, shutil, urllib.parse, datetime, importlib, sys

SRC = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SRC)
import golive

OUT = os.path.join(os.path.dirname(SRC), "site")
RES = os.path.join(os.path.dirname(SRC), "research")
FACTS = json.load(open(os.path.join(RES, "facts.json")))
CFG = golive.load(os.path.join(SRC, "site.json"))
BASE = "/" if CFG.live else CFG.preview_path          # page links: preview folder until the Live switch is on
WA_NUMBER = "6589976612"  # Edwin's mobile / WhatsApp. Used only inside wa.me links, never printed on a page.
API = "https://sgcar-accident-settlement-4d8df539.base44.app/api/settle"
TODAY = datetime.date.today().isoformat()
E = html.escape
L = {"en": importlib.import_module("content_en"), "zh": importlib.import_module("content_zh")}
G = {"en": importlib.import_module("guides_en"), "zh": importlib.import_module("guides_zh")}

# Lead pathway categories (Edwin's brief section 7). key -> (code used in the WhatsApp reference, EN label)
LEAD_PATHWAYS = {
    "own_damage": ("OD", "Own Damage / At Fault"),
    "unsure": ("UA", "Unsure / Assistance"),
    "third_party": ("TP", "Third-Party Claim"),
    "windscreen": ("WS", "Windscreen"),
    "private_settlement": ("PS", "Private Settlement"),
    "reporting": ("RP", "General Accident Reporting"),
}

ASSETS = ["site.css", "site.js", "lead.js", "settle.js", "p1-cta.js", "jspdf.umd.min.js"]
def sha8(p):
    return hashlib.sha256(open(os.path.join(SRC, "assets", p), "rb").read()).hexdigest()[:8]
V = {k: sha8(k) for k in ASSETS}

def url(lang, path=""):
    return BASE + ("zh/" if lang == "zh" else "") + path

def asset(name):
    return BASE + "assets/" + name + ("?v=" + V[name] if name in V else "")

def absu(lang, path=""):
    return CFG.canon(CFG.lang_path(lang, path))

def wa(lang, key):
    return "https://wa.me/%s?text=%s" % (WA_NUMBER, urllib.parse.quote(L[lang].WA[key]))

# ---------------- verified facts (EN from official pages; ZH is a faithful rendering) ----------------
GIA_DOS = FACTS["gia_24h"]["url"]
GIA_MCF = "https://gia.org.sg/motor-insurance/22-premium-renewal-of-policy/348-motor-claims-framewor"
SPF = FACTS["spf_police_cases"]
FACT_TEXT = {
    "en": {
        "gia_24h": "Report the accident to your insurer within 24 hours or by the next working day. Take your vehicle, damaged or not, to your insurer's approved reporting centre or authorised workshop. (GIA Motor Claims Framework)",
        "police_cases": ["Someone died", "Someone was taken to hospital by ambulance, or got 3 or more days of medical leave", "Government property was damaged", "A foreign vehicle was involved", "A pedestrian or cyclist was involved", "Hit and run"],
        "spf_how": "Make the Police report online through the SPF e-services Traffic Accident Report (Singpass needed), or at any police station. A Police report does not replace your report to your insurer.",
    },
    "zh": {
        "gia_24h": "须在24小时内或下一个工作日之前向保险公司报案。无论车辆是否受损，都要把车开到保险公司认可的报案中心或授权车厂。（GIA汽车索赔框架）",
        "police_cases": ["有人死亡", "有人被救护车送院，或获得3天或以上的病假", "政府财产受损", "涉及外国车辆", "涉及行人或骑脚车者", "肇事逃逸"],
        "spf_how": "可通过新加坡警察部队（SPF）电子服务的交通事故报告在线报案（需要Singpass），或到任何警署报案。向警方报案不能代替向保险公司报案。",
    },
}
SOURCES = [("GIA: Motor Claims Framework", GIA_MCF), ("GIA: Do's and don'ts after an accident", GIA_DOS), ("SPF: Reporting traffic accidents", SPF["url"])]

# ---------------- icons (one authored set, 2px stroke) ----------------
def ic(p, fill=False):
    a = 'fill="currentColor"' if fill else 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    return '<svg viewBox="0 0 24 24" aria-hidden="true" %s>%s</svg>' % (a, p)
I_WA = ic('<path d="M12 2.2A9.7 9.7 0 0 0 3.7 16.9L2.3 21.8l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.3 3.8c1.6.7 2.2.7 3 .6.5-.1 1.4-.6 1.6-1.1.2-.6.2-1 .1-1.1l-.5-.5Z"/>', True)
I_CHEV = ic('<path d="m9 6 6 6-6 6"/>')
I_BACK = ic('<path d="m15 6-6 6 6 6"/>')
ICONS = {
    "fault": ic('<path d="M12 3 2.5 20h19L12 3Z"/><path d="M12 10v4"/><circle cx="12" cy="17" r=".6" fill="currentColor"/>'),
    "unsure": ic('<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.6 2.6 0 0 1 5 .8c0 1.8-2.5 2.2-2.5 3.7"/><circle cx="12" cy="17.2" r=".6" fill="currentColor"/>'),
    "notfault": ic('<path d="M12 3 4 6v6c0 4.5 3.4 7.8 8 9 4.6-1.2 8-4.5 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>'),
    "windscreen": ic('<path d="M3 17c0-6 4-10 9-10s9 4 9 10H3Z"/><path d="m11 9 2 3-2 2 2 3"/>'),
    "centre": ic('<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>'),
    "statement": ic('<path d="M9 4h6v3H9z"/><path d="M8 5H6a1 1 0 0 0-1 1v14a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V6a1 1 0 0 0-1-1h-2"/><path d="M9 12h6M9 16h4"/>'),
    "settlement": ic('<path d="M14 3H6a1 1 0 0 0-1 1v16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8l-5-5Z"/><path d="M14 3v5h5"/><path d="M8 17c1.5-1.5 2.5-1.5 3 0s1.5 1.5 3-1"/>'),
    "faq": ic('<path d="M4 5h16v11H9l-5 4V5Z"/><path d="M9 9h6M9 12h4"/>'),
    "tow": ic('<path d="M2 17V9h7l3 4h6a2 2 0 0 1 2 2v2"/><circle cx="6" cy="17" r="2"/><circle cx="17" cy="17" r="2"/><path d="M12 13V6l6-2"/>'),
    "minor": ic('<path d="M3 16v-3l2-5h9l3 5h3a1 1 0 0 1 1 1v2"/><circle cx="7" cy="16.5" r="1.8"/><circle cx="17" cy="16.5" r="1.8"/><path d="M19 5l-2 2M21 9h-2"/>'),
    "hitrun": ic('<path d="M3 16v-3l2-5h9l3 5h3a1 1 0 0 1 1 1v2"/><circle cx="7" cy="16.5" r="1.8"/><circle cx="17" cy="16.5" r="1.8"/><path d="M2 5h6M4 2.5h5"/>'),
    "guide": ic('<path d="M4 4h6a2 2 0 0 1 2 2v14a2 2 0 0 0-2-2H4V4Z"/><path d="M20 4h-6a2 2 0 0 0-2 2v14a2 2 0 0 1 2-2h6V4Z"/>'),
}
LOGO = ('<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="2" y="2" width="28" height="28" rx="6" fill="#0B5A8C"/>'
        '<path d="M16 7 26 24H6L16 7Z" fill="none" stroke="#F2A900" stroke-width="2.6" stroke-linejoin="round"/>'
        '<path d="M16 13v5" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/><circle cx="16" cy="21.2" r="1.5" fill="#fff"/></svg>')

def hotline(lang, key, ref, label=None, cls="btn btn-go block"):
    t = L[lang].T
    return '<a class="%s" href="%s" target="_blank" rel="noopener" data-ref="%s">%s<span>%s</span></a>' % (
        cls, E(wa(lang, key)), E(ref), I_WA, E(label or t["wa_us"]))

def dock_btn(lang, key, ref):
    t = L[lang].T
    return '<a class="btn btn-go d-wa calm-wa" href="%s" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="%s"><span class="nudge" aria-hidden="true"></span>%s<span>%s</span></a>' % (
        E(wa(lang, key)), E(ref), I_WA, E(t["wa_guide"]))

def jsonld(o):
    return '<script type="application/ld+json">%s</script>' % json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

def faq_block(lang, faq, h=None, cls="faq"):
    t = L[lang].T
    if not faq:
        return "", None
    out = '<section class="%s"><h2>%s</h2>%s</section>' % (cls, E(h or t["faq_h"]), "".join(
        "<details><summary>%s</summary><p>%s</p></details>" % (E(q), E(fill(lang, a))) for q, a in faq))
    sd = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": fill(lang, a)}} for q, a in faq]}
    return out, sd

def fill(lang, s):
    ft = FACT_TEXT[lang]
    return s.replace("{gia_24h}", ft["gia_24h"]).replace("{spf_how}", ft["spf_how"])

# ---------------- the ONE layout ----------------
def page(lang, path, title, desc, body, key, ref, schema=(), alt=True, scripts=("site.js",), crumbs=None, extra_head="", img=None, img_alt=None):
    """key = WhatsApp prefill for this page's dock; ref = tap label prefix (pathway name)."""
    t = L[lang].T
    other = "zh" if lang == "en" else "en"
    tags = golive.head_tags(CFG, path, lang, img) if alt else '<link rel="canonical" href="%s">' % absu(lang, path)
    bc = ""
    if crumbs:
        items = [(t["home"], url(lang))] + crumbs
        bc = '<nav class="crumbs" aria-label="Breadcrumb"><a class="bk" href="%s">%s<span>%s</span></a><span class="trail">%s</span></nav>' % (
            E(items[-2][1] or url(lang)), I_BACK, E(t["back"]),
            " / ".join('<a href="%s">%s</a>' % (E(u), E(n)) if u else "<span>%s</span>" % E(n) for n, u in items))
        schema = list(schema) + [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": (CFG.canonical_base.rstrip("/") + (u[len(BASE) - 1:] if u else "/" + CFG.lang_path(lang, path)))} for i, (n, u) in enumerate(items)]}]
    js = "".join('<script src="%s" defer></script>' % E(asset(s)) for s in scripts)
    srcs = " ".join('<a href="%s" rel="noopener">%s</a>' % (E(u), E(n)) for n, u in SOURCES)
    return """<!doctype html>
<html lang="%(hl)s"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>%(title)s</title><meta name="description" content="%(desc)s">
%(tags)s
<meta property="og:type" content="website"><meta property="og:site_name" content="SGCarAccident"><meta property="og:title" content="%(title)s"><meta property="og:description" content="%(desc)s"><meta property="og:locale" content="%(ogl)s"><meta property="og:image:alt" content="%(ogalt)s"><meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B5A8C"><link rel="icon" href="%(fav)s" type="image/svg+xml">
%(preload)s<link rel="stylesheet" href="%(css)s"><script>document.documentElement.className+=" js"</script>%(extra)s
%(schema)s</head>
<body data-lang="%(lang)s" data-base="%(base)s"><a class="skip" href="#main">%(skip)s</a>
<header class="hd"><a class="logo" href="%(home)s">%(logo)s<span>%(brand)s</span></a><a class="lang" href="%(olink)s" hreflang="%(ohl)s" lang="%(ohl)s">%(switch)s</a></header>
<main id="main" class="wrap">%(bc)s%(body)s</main>
<footer class="ft"><div class="wrap"><nav class="links" aria-label="%(more)s"><a href="%(home)s">%(homel)s</a><a href="%(ins)s">%(insl)s</a><a href="%(rep)s">%(repl)s</a><a href="%(ps)s">%(psl)s</a><a href="%(faq)s">%(faql)s</a><a href="%(gd)s">%(gdl)s</a><a href="%(priv)s">%(privl)s</a></nav>
<p>%(disc)s</p><p class="safe">%(safe)s</p><p class="srcs">%(srcl)s: %(srcs)s</p></div></footer>
<nav class="dock" aria-label="%(helpl)s">%(dock)s</nav>
<script type="application/json" id="ui">%(ui)s</script><script src="%(cta)s" defer></script>%(js)s
</body></html>
""" % {
        "hl": t["html_lang"], "lang": lang, "base": BASE, "title": E(title), "desc": E(desc), "tags": tags,
        "ogl": "en_SG" if lang == "en" else "zh_SG", "ogalt": E(img_alt or t["og_alt"]), "fav": asset("icon.svg"),
        "preload": ('<link rel="preload" href="%s" as="font" type="font/woff2" crossorigin>' % (BASE + "assets/barlow-semi-condensed-latin-700-normal.woff2")) if lang == "en" else "",
        "css": asset("site.css"), "extra": extra_head, "schema": "".join(jsonld(s) for s in schema if s),
        "skip": E(t["skip"]), "home": url(lang), "logo": LOGO, "brand": E(t["brand"]),
        "olink": url(other, path), "ohl": "zh-Hans" if other == "zh" else "en", "switch": E(t["switch_label"]), "bc": bc, "body": body,
        "more": E(t["more_nav"]), "homel": E(t["home"]), "ins": url(lang, "insurers/"), "insl": E(t["insurers_link"]),
        "rep": url(lang, "report/"), "repl": E(t["report_link"]), "ps": url(lang, "private-settlement/"), "psl": E(t["settlement_link"]),
        "faq": url(lang, "faq/"), "faql": E(t["faq_link"]), "gd": url(lang, "guides/"), "gdl": E(t["guides_link"]),
        "priv": url(lang, "privacy/"), "privl": E(t["privacy"]),
        "disc": E(t["disclaimer"]), "safe": E(t["safe"]), "srcl": E(t["sources"]), "srcs": srcs, "helpl": E(t["help_nav"]),
        "dock": dock_btn(lang, key, ref + ":dock"),
        "cta": asset("p1-cta.js"), "js": js, "ui": json.dumps(t["js"], ensure_ascii=False).replace("</", "<\\/"),
    }

# ---------------- insurers + reporting centres ----------------
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
    "liberty": ("Liberty Insurance", "accident reporting point and preferred workshops", "事故报案点和首选车厂名单"),
    "sompo": ("Sompo", "ExcelDrive workshops and accident reporting centres", "ExcelDrive车厂和事故报案中心名单"),
    "allianz": ("Allianz", "Motor Protect workshop list", "Motor Protect车厂名单"),
    "singlife": ("Singlife", "authorised car repairers", "授权修车厂名单"),
}
# 24-hour lines quoted verbatim from the insurers' own pages (research/research_addendum.json, read 21 Nov 2026).
HOTLINES = {
    "msig": ("+65 6827 7660", "https://www.msig.com.sg/claims/personal/motor-claims"),
    "aig": ("6338 6200", "https://aig.sg/car-claim"),
    "tokiomarine": ("1800 225 8647", "https://www.tokiomarine.com/sg/en/non-life/claim/step-by-step-claim-guide/motor-claims-process.html"),
    "singlife": ("+65 6333 2222", "https://singlife.com/en/claims/lifestyle/car"),
    "liberty": ("1800-LIBERTY (5423 789)", "https://www.libertyinternational.com/sg/claims/claim-vehicle-individual", "plain"),  # Liberty's page does not say 24-hour
}
def tel(n):
    return "tel:" + re.sub(r"[^\d+]", "", n if n.startswith(("+", "1800")) else "+65" + n)
REGIONS = [("North", "北部"), ("East", "东部"), ("West", "西部"), ("Central", "中部"), ("South", "南部")]
DROP = re.compile(r"hours not shown|as printed|document layout|postal|page spells|customers only|incomplete|unc$|^\s*$", re.I)
UNNAMED = re.compile(r"not matched|^\s*$", re.I)

def clean_note(n):
    keep = []
    for p in [p.strip() for p in re.split(r";", n or "")]:
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
        nm = (c.get("name") or "").strip()
        cs.append({"name": "" if UNNAMED.search(nm) else nm, "address": c["address"].strip(), "hours": (c.get("hours") or "").strip(),
                   "region": region_of(c.get("notes", "")), "note": clean_note(c.get("notes", ""))})
    seen, uniq = set(), []
    for c in cs:
        k = re.sub(r"\W", "", (c["name"] + c["address"]).lower())
        if k not in seen:
            seen.add(k); uniq.append(c)
    order = {r[0]: i for i, r in enumerate(REGIONS)}
    uniq.sort(key=lambda c: (order.get(c["region"], 9), c["name"] or "~", c["address"]))
    INSURERS.append({"slug": ins["slug"], "name": NAMES[ins["slug"]][0], "kind": NAMES[ins["slug"]][1:], "centres": uniq,
                     "src": ins["source_url"].replace(" ", "%20"), "read": ins.get("read", "2026-11-19")})
INSURERS.sort(key=lambda x: x["name"])

def maps(addr):
    return "https://www.google.com/maps/dir/?api=1&destination=" + urllib.parse.quote(addr)

def centre_json(lang, ins):
    reg = dict(REGIONS)
    return {"name": ins["name"], "url": url(lang, "insurers/%s/" % ins["slug"]), "src": ins["src"], "read": ins["read"],
            "kind": ins["kind"][0 if lang == "en" else 1], "hl": HOTLINES.get(ins["slug"], ["", ""])[0], "hlt": tel(HOTLINES[ins["slug"]][0]) if ins["slug"] in HOTLINES else "", "hls": HOTLINES.get(ins["slug"], ["", ""])[1],
            "c": [{"n": c["name"], "a": c["address"], "h": c["hours"], "r": (reg.get(c["region"], c["region"]) if lang == "zh" else c["region"]), "x": c["note"], "m": maps(c["address"])} for c in ins["centres"]]}

def insurer_picker(lang, ref, store=True):
    """Pick your insurer -> its reporting centres load inline (assets/centres/<slug>.<lang>.json). Works without JS as links."""
    t = L[lang].T
    opts = "".join('<option value="%s">%s</option>' % (i["slug"], E(i["name"])) for i in INSURERS)
    links = "".join('<a href="%s">%s</a>' % (url(lang, "insurers/%s/" % i["slug"]), E(i["name"])) for i in INSURERS)
    return ('<div class="picker" data-ref="%s" data-json="%s"%s><label class="lbl" for="pick-%s">%s</label>'
            '<select id="pick-%s" class="sel"><option value="">%s</option>%s<option value="other">%s</option></select>'
            '<div class="pick-out" aria-live="polite"></div><noscript><div class="chips">%s</div></noscript></div>') % (
        E(ref), BASE + "assets/centres/", " data-store" if store else "", E(ref.replace(":", "-")), E(t["pick_insurer"]),
        E(ref.replace(":", "-")), E(t["pick_insurer_ph"]), opts, E(t["pick_insurer_other"]), links)

# ---------------- lead forms (every enquiry -> WhatsApp, with pathway + consent) ----------------
def lead_form(lang, key, pathway, ref, title=None, intro=None):
    C = L[lang]; t = C.T; F = C.FORMS[key]
    code, label_en = LEAD_PATHWAYS[pathway]
    rows = []
    for f in F["fields"]:
        name, lab, typ = f[0], f[1], f[2]
        req = f[3] if len(f) > 3 else False
        extra = f[4] if len(f) > 4 else ""
        lab_full = lab + ("" if req else " " + t["optional"])
        rq = " required" if req else ""
        if typ == "textarea":
            ctl = '<textarea id="%s-%s" name="%s" maxlength="600"%s%s></textarea>' % (key, name, name, rq, (' placeholder="%s"' % E(extra)) if extra else "")
        elif typ == "select":
            ctl = '<select id="%s-%s" name="%s"%s><option value="">%s</option>%s</select>' % (key, name, name, rq, E(t["choose"]), "".join('<option>%s</option>' % E(o) for o in extra))
        elif typ == "insurer":
            ctl = '<input id="%s-%s" name="%s" type="text" maxlength="60" list="dl-insurers"%s>' % (key, name, name, rq)
        else:
            attrs = {"tel": ' inputmode="tel" autocomplete="tel" maxlength="20"', "name": ' autocomplete="name" maxlength="80"',
                     "plate": ' autocapitalize="characters" maxlength="12"', "date": "", "text": ' maxlength="80"'}[typ]
            ctl = '<input id="%s-%s" name="%s" type="%s"%s%s>' % (key, name, name, {"name": "text", "plate": "text"}.get(typ, typ), attrs, rq)
        rows.append('<div class="field"><label for="%s-%s">%s</label>%s</div>' % (key, name, E(lab_full), ctl))
    dl = '<datalist id="dl-insurers">%s</datalist>' % "".join('<option value="%s">' % E(i["name"]) for i in INSURERS)
    return """<form class="lead" id="lead-%(key)s" data-lead="%(pathway)s" data-code="%(code)s" data-cat="%(cat)s" data-wa="%(wa)s" data-ref="%(ref)s" novalidate>
<h3>%(title)s</h3>%(intro)s%(rows)s%(photos)s
<label class="tick"><input type="checkbox" name="consent" required><span>%(consent)s</span></label>
<p class="err" role="alert"></p>
<button type="submit" class="btn btn-go block">%(wa_ic)s<span>%(send)s</span></button>
<p class="fine">%(fine)s</p>
<div class="sent" hidden><p><strong>%(sent_h)s</strong></p><p>%(sent_p)s</p><a class="btn btn-ghost block" data-reopen href="#">%(reopen)s</a></div>
%(dl)s</form>""" % {
        "key": key, "pathway": pathway, "code": code, "cat": E(t["cat"][pathway]), "wa": WA_NUMBER, "ref": E(ref),
        "title": E(title or F["title"]), "intro": ('<p class="lead-intro">%s</p>' % E(intro or F.get("intro", ""))) if (intro or F.get("intro")) else "",
        "rows": "".join(rows), "photos": ('<p class="photo-note">%s</p>' % E(t["photos_in_wa"])) if F.get("photos") else "",
        "consent": E(t["consent"]), "wa_ic": I_WA, "send": E(F.get("send", t["send_wa"])), "fine": E(t["lead_fine"]),
        "sent_h": E(t["sent_h"]), "sent_p": E(t["sent_p"]), "reopen": E(t["reopen"]), "dl": dl if any(f[2] == "insurer" for f in F["fields"]) else "",
    }

# ---------------- flows (one step per screen) ----------------
def acts(lang, ref, optional=False):
    t = L[lang].T
    return ('<div class="acts"%s><a class="a-tow" href="%s" target="_blank" rel="noopener" data-cta="whatsapp" data-cta-label="tow" data-ref="%s">%s</a></div>') % (
        ' data-opt' if optional else "", E(wa(lang, "tow")), E("tow:" + ref + "-flow"), E(t["tow"]))

def ul(items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % E(x) for x in items)

def step_html(lang, slug, s):
    C = L[lang]; t = C.T
    h = '<h2>%s</h2>' % E(s["h"])
    if s.get("warn"):
        h += '<p class="warn">%s</p>' % E(fill(lang, s["warn"]))
    for p in s.get("p", []):
        h += "<p>%s</p>" % E(fill(lang, p))
    li = s.get("li")
    if li == "{police_cases}":
        li = FACT_TEXT[lang]["police_cases"]
    if li:
        h += ul(li)
    for p in s.get("p2", []):
        h += "<p>%s</p>" % E(fill(lang, p))
    if s.get("li2"):
        h += ul(s["li2"])
    if s.get("ch"):  # single choice, a note per answer
        h += '<div class="choices" role="group">%s</div>' % "".join(
            '<button type="button" class="choice" data-k="%s" aria-pressed="false">%s</button>' % (E(c[0]), E(c[1])) for c in s["ch"])
        h += "".join('<p class="note" data-k="%s">%s</p>' % (E(c[0]), E(fill(lang, c[2]))) for c in s["ch"])
    if s.get("flags"):  # tick everything that applies
        h += '<div class="flags" role="group">%s</div>' % "".join(
            '<button type="button" class="flag" data-k="%s" data-police="%s" aria-pressed="false"><i aria-hidden="true"></i>%s</button>' % (E(c[0]), "1" if c[3] else "", E(c[1])) for c in s["flags"])
        h += "".join('<p class="note" data-k="%s">%s</p>' % (E(c[0]), E(c[2])) for c in s["flags"])
        h += '<p class="note police" data-k="_police">%s</p>' % E(t["police_needed"])
        h += '<p class="note ok" data-k="_none">%s</p>' % E(s.get("none", t["no_flags"]))
        h += '<button type="button" class="choice none-btn" data-none aria-pressed="false">%s</button>' % E(s.get("none_label", t["none_apply"]))
    if s.get("checks"):  # yes / not yet questions, tip on "not yet"
        rows = []
        for k, q, tip in s["checks"]:
            rows.append('<div class="chk" data-k="%s"><p class="q">%s</p><div class="yn"><button type="button" data-v="y" aria-pressed="false">%s</button><button type="button" data-v="n" aria-pressed="false">%s</button></div><p class="note" data-k="%s">%s</p></div>' % (
                E(k), E(q), E(t["yes"]), E(t["not_yet"]), E(k), E(tip)))
        h += '<div class="checks">%s</div>' % "".join(rows)
    if s.get("act"):
        h += acts(lang, slug, bool(s.get("ch")))
    if s.get("insurer"):
        h += insurer_picker(lang, slug + ":insurer")
    if s.get("ask"):  # optional help, e.g. statement
        a = s["ask"]
        h += '<div class="choices ask" role="group"><button type="button" class="choice" data-k="y" aria-pressed="false">%s</button><button type="button" class="choice" data-k="n" aria-pressed="false" data-skip>%s</button></div><div class="note" data-k="y">%s</div><p class="note" data-k="n">%s</p>' % (
            E(a["yes"]), E(a["no"]), statement_tool(lang, slug) if a.get("tool") else E(a["yes_note"]), E(a["no_note"]))
    if s.get("summary"):  # final action screen: insurer chosen earlier is filled in by site.js
        h += '<div class="final"><p class="lbl">%s</p><div class="final-ins" data-final-insurer><p>%s</p></div></div>' % (E(t["where_report"]), E(t["no_insurer_yet"]))
    if s.get("links"):
        h += '<div class="rlinks">%s</div>' % "".join('<a class="btn btn-ghost block" href="%s">%s</a>' % (url(lang, u), E(n)) for n, u in s["links"])
    if s.get("lead"):
        h += lead_form(lang, s["lead"][0], s["lead"][1], slug + ":form")
    if s.get("helpbox"):  # the three contact buttons (Edwin: WhatsApp / callback / submit details)
        hb = s["helpbox"]
        h += '<div class="helpbox"><h3>%s</h3><p>%s</p><div class="endcta">%s<a class="btn btn-sign block" href="#lead-%s" data-open="callback-%s">%s</a><a class="btn btn-ghost block" href="#lead-%s" data-open="lead-%s">%s</a></div></div>' % (
            E(hb["h"]), E(hb["p"]), hotline(lang, hb["wa"], slug + ":help-wa", t["wa_assist"]),
            "callback-" + hb["pathway"], hb["pathway"], E(t["callback"]), hb["form"], hb["form"], E(t["submit_details"]))
        h += '<div class="lead-wrap" id="wrap-callback-%s" hidden>%s</div>' % (hb["pathway"], lead_form(lang, "callback-" + hb["pathway"] if ("callback-" + hb["pathway"]) in C.FORMS else "callback", hb["pathway"], slug + ":callback").replace('id="lead-callback"', 'id="lead-callback-%s"' % hb["pathway"]))
        h += '<div class="lead-wrap" id="wrap-lead-%s" hidden>%s</div>' % (hb["form"], lead_form(lang, hb["form"], hb["pathway"], slug + ":form"))
    end = ""
    if s.get("cta"):
        h += '<div class="endcta">%s%s<a class="btn btn-ghost block" href="%s">%s</a></div>' % (
            "" if s.get("helpbox") else hotline(lang, s["cta"], slug + ":end"), "".join('<a class="btn btn-sign block" href="%s">%s</a>' % (url(lang, u), E(n)) for n, u in s.get("cta_links", [])),
            url(lang), E(t["start_over"]))
        end = " data-end"
    return '<section class="step"%s>%s</section>' % (end, h)

def flow_page(lang, slug):
    C = L[lang]; t = C.T; F = C.FLOWS[slug]
    steps = "".join(step_html(lang, slug, s).replace('<section class="step"', '<section class="step" id="s%d"' % (k + 1), 1) for k, s in enumerate(F["steps"]))
    labels = E(json.dumps([s.get("tab", s["h"]) for s in F["steps"]], ensure_ascii=False))
    faq_h, faq_sd = faq_block(lang, F.get("faq"))
    body = """<div class="flowhead"><span class="pic">%s</span><div><h1 class="page-h1">%s</h1><p class="lead">%s</p></div></div>

<div class="prog" aria-hidden="true"><i></i></div><p class="prog-l" data-tpl="%s" data-labels="%s" aria-live="polite"></p>
<div class="flow" data-flow="%s">%s</div>
<div class="nav"><button type="button" class="btn btn-ghost" data-back>%s</button><button type="button" class="btn btn-sign" data-next>%s</button></div>
<p class="allsteps"><a href="#" data-all>%s</a></p>
%s%s""" % (ICONS[F["icon"]], E(F["h1"]), E(F["lead"]), E(t["step_of"]), labels, slug, steps, E(t["back"]), E(t["next"]), E(t["read_all"]),
           faq_h, source_box(lang))
    howto = {"@context": "https://schema.org", "@type": "HowTo", "name": F["h1"], "step": [
        {"@type": "HowToStep", "position": i + 1, "name": s["h"]} for i, s in enumerate(F["steps"]) if not s.get("cta")]}
    return page(lang, slug + "/", F["title"], F["desc"], body, F.get("wa", slug), slug, schema=[faq_sd, howto], crumbs=[(F["nav"], None)],
                scripts=("site.js", "lead.js"))

def source_box(lang):
    t = L[lang].T
    return '<div class="srcbox"><p class="lbl">%s</p><ul>%s</ul></div>' % (E(t["sources_box"]), "".join(
        '<li><a href="%s" rel="noopener">%s</a></li>' % (E(u), E(n)) for n, u in SOURCES))

# ---------------- home ----------------
def home(lang):
    C = L[lang]; t = C.T; H = C.HOME
    def path_btn(k, icon, href):
        b, s = H["paths"][k]
        return '<a class="path p-%s" href="%s" data-ref="home:path-%s"><span class="pi">%s</span><span class="pt"><b>%s</b><small>%s</small></span><span class="chev">%s</span></a>' % (
            k, url(lang, href), k, ICONS[icon], E(b), E(s), I_CHEV)
    def card(k, icon, href):
        b, s = H["res"][k]
        return '<a class="rcard" href="%s" data-ref="home:res-%s"><span class="ri">%s</span><b>%s</b><small>%s</small></a>' % (url(lang, href), k, ICONS[icon], E(b), E(s))
    guides = "".join('<li><a href="%s">%s</a></li>' % (url(lang, "guides/%s/" % g["slug"]), E(g["h1"])) for g in G[lang].GUIDES)
    faq_h, faq_sd = faq_block(lang, H["faq"])
    body = """<section class="pick" aria-labelledby="h1"><h1 id="h1">%(h1)s</h1><p class="q">%(q)s</p>
<div class="paths">%(p1)s%(p2)s%(p3)s</div>
</section>
<section class="more"><h2>%(res_h)s</h2><div class="rgrid">%(c7)s%(c8)s%(c1)s%(c2)s%(c3)s%(c4)s%(c5)s%(c6)s</div></section>
<section class="glist"><h2>%(g_h)s</h2><p>%(g_p)s</p><ul>%(guides)s</ul><a class="btn btn-ghost block" href="%(gall)s">%(g_all)s</a></section>
%(faq)s""" % {
        "h1": E(H["h1"]), "q": E(H["q"]),
        "p1": path_btn("fault", "fault", "own-damage/"), "p2": path_btn("unsure", "unsure", "not-sure/"), "p3": path_btn("notfault", "notfault", "third-party/"),
        "hurt": E(H["hurt"]), "res_h": E(H["res_h"]),
        "c1": card("windscreen", "windscreen", "windscreen/"), "c2": card("centre", "centre", "insurers/"), "c3": card("statement", "statement", "report/"),
        "c4": card("settlement", "settlement", "private-settlement/"), "c5": card("faq", "faq", "faq/"), "c6": card("tow", "tow", "tow/"),
        "c7": card("minor", "minor", "minor-car-accident/"), "c8": card("hitrun", "hitrun", "hit-and-run/"),
        "g_h": E(H["g_h"]), "g_p": E(H["g_p"]), "guides": guides, "gall": url(lang, "guides/"), "g_all": E(H["g_all"]), "faq": faq_h,
    }
    org_id = CFG.canonical_base.rstrip("/") + "/#org"
    org = {"@context": "https://schema.org", "@type": "Organization", "@id": org_id, "name": "SGCarAccident", "url": CFG.canonical_base,
           "logo": CFG.canonical_base.rstrip("/") + "/assets/icon.svg", "areaServed": {"@type": "Country", "name": "Singapore"},
           "description": "General guidance for drivers after a car accident in Singapore. Not an insurer, law firm or reporting centre."}
    site = {"@context": "https://schema.org", "@type": "WebSite", "name": "SGCarAccident", "url": absu(lang), "inLanguage": t["html_lang"], "publisher": {"@id": org_id}}
    return page(lang, "", H["title"], H["desc"], body, "home", "home", schema=[org, site, faq_sd])

# ---------------- reporting centres ----------------
def insurer_index(lang):
    C = L[lang]; t = C.T; F = C.PAGES["insurers"]
    lis = "".join('<a href="%s" data-ref="insurers:index">%s<span>%s</span></a>' % (url(lang, "insurers/%s/" % i["slug"]), E(i["name"]), E(t["n_places"].replace("{n}", str(len(i["centres"]))))) for i in INSURERS)
    body = ('<h1 class="page-h1">%s</h1><p class="lead">%s</p><div class="remind">%s</div>%s<h2 class="sub">%s</h2><div class="ins-index">%s</div>'
            '<p class="src">%s</p><div class="endcta">%s</div>%s') % (
        E(F["h1"]), E(F["lead"]), E(FACT_TEXT[lang]["gia_24h"]), insurer_picker(lang, "insurers:picker", store=True), E(F["all_h"]), lis, E(F["missing"]),
        hotline(lang, "insurers", "insurers:index-end"), faq_block(lang, F["faq"])[0])
    il = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": i["name"], "url": absu(lang, "insurers/%s/" % i["slug"])} for k, i in enumerate(INSURERS)]}
    return page(lang, "insurers/", F["title"], F["desc"], body, "insurers", "insurers", schema=[il, faq_block(lang, F["faq"])[1]], crumbs=[(F["nav"], None)])

def centre_card(lang, c):
    t = L[lang].T
    head = c["name"] or c["address"]
    return '<div class="ins"><h3>%s</h3>%s%s%s<a class="map" href="%s" target="_blank" rel="noopener">%s</a></div>' % (
        E(head), ('<p>%s</p>' % E(c["address"])) if c["name"] else "",
        ('<p class="meta">%s: %s</p>' % (E(t["hours"]), E(c["hours"]))) if c["hours"] else "",
        ('<p class="meta">%s</p>' % E(c["note"])) if c["note"] else "", E(maps(c["address"])), E(t["map"]))

def insurer_page(lang, ins):
    C = L[lang]; t = C.T; P = C.INSURER_PAGE; n = ins["name"]
    has_hours = any(c["hours"] for c in ins["centres"])
    reg_zh = dict(REGIONS)
    out, cur = [], None
    regions_present = [r for r, _ in REGIONS if any(c["region"] == r for c in ins["centres"])]
    for c in ins["centres"]:
        if c["region"] != cur and any(x["region"] for x in ins["centres"]):
            cur = c["region"]
            out.append('<h2 class="region" id="r-%s">%s</h2>' % (E((cur or "other").lower()), E((reg_zh.get(cur, cur) if lang == "zh" else cur) or ("其他" if lang == "zh" else "Other areas"))))
        out.append(centre_card(lang, c))
    jump = ""
    if len(regions_present) > 1:
        jump = '<nav class="chips jump" aria-label="%s">%s</nav>' % (E(t["jump_region"]), "".join(
            '<a href="#r-%s">%s</a>' % (r.lower(), E(reg_zh[r] if lang == "zh" else r)) for r in regions_present))
    kind = ins["kind"][0] if lang == "en" else ins["kind"][1]
    src = '<p class="src">%s: <a href="%s" rel="noopener">%s %s</a>, %s %s. %s</p>' % (
        E(t["source"]), E(ins["src"]), E(n), E(kind), E(t["read_on"]), E(ins["read"]), E(t["check_before"]))
    faq = [[q.replace("{name}", n), a.replace("{name}", n)] for q, a in P["faq"]]
    faq_h, faq_sd = faq_block(lang, faq)
    hl = ""
    if ins["slug"] in HOTLINES:
        num, su = HOTLINES[ins["slug"]][:2]
        lbl = t["hotline_plain"] if HOTLINES[ins["slug"]][2:] else t["hotline"]
        hl = '<div class="hl"><p class="lbl">%s</p><a class="btn btn-ghost block" href="%s">%s</a><p class="fine"><a href="%s" rel="noopener">%s</a></p></div>' % (E(lbl), tel(num), E(n + " " + num), E(su), E(t["source"]))
    src = hl + src
    body = '<h1 class="page-h1">%s</h1><p class="lead">%s</p>%s<div class="remind">%s</div>%s<div class="ins-list">%s</div>%s<div class="endcta">%s<a class="btn btn-ghost block" href="%s">%s</a></div>%s' % (
        E(P["h1"].replace("{name}", n)), E(P["lead"]), src, E(FACT_TEXT[lang]["gia_24h"]), jump, "".join(out), src,
        hotline(lang, "insurers", "insurer:" + ins["slug"]), url(lang, "report/"), E(t["prep_statement"]), faq_h)
    title = P["title"].replace("{name}", n)
    desc = P["desc"].replace("{name}", n).replace("{hours_bit}", P["hours_bit"] if has_hours else "")
    return page(lang, "insurers/%s/" % ins["slug"], title, desc, body, "insurers", "insurer:" + ins["slug"], schema=[faq_sd],
                crumbs=[(C.PAGES["insurers"]["nav"], url(lang, "insurers/")), (n, None)])

# ---------------- accident report + statement guide ----------------
def statement_tool(lang, ref):
    C = L[lang]; t = C.T; S = C.STATEMENT
    rows = []
    for grp, fields in S["groups"]:
        fs = []
        for f in fields:
            name, lab, typ = f[0], f[1], f[2]
            if typ == "select":
                ctl = '<select id="st-%s-%s" name="%s"><option value="">%s</option>%s</select>' % (ref, name, name, E(t["choose"]), "".join("<option>%s</option>" % E(o) for o in f[3]))
            elif typ == "textarea":
                ctl = '<textarea id="st-%s-%s" name="%s" maxlength="900"%s></textarea>' % (ref, name, name, (' placeholder="%s"' % E(f[3])) if len(f) > 3 else "")
            else:
                ctl = '<input id="st-%s-%s" name="%s" type="%s"%s>' % (ref, name, name, "text" if typ in ("plate",) else typ, ' autocapitalize="characters" maxlength="12"' if typ == "plate" else ' maxlength="120"')
            fs.append('<div class="field"><label for="st-%s-%s">%s</label>%s</div>' % (ref, name, E(lab), ctl))
        rows.append('<fieldset><legend>%s</legend>%s</fieldset>' % (E(grp), "".join(fs)))
    return """<form class="stmt" data-stmt data-ref="%(ref)s:statement" novalidate><p class="warn">%(not_official)s</p>%(rows)s
<button type="button" class="btn btn-sign block" data-make>%(make)s</button>
<div class="stmt-out" hidden><p class="lbl">%(out_h)s</p><pre class="stmt-text" tabindex="0"></pre>
<div class="endcta"><button type="button" class="btn btn-ghost block" data-copy>%(copy)s</button><button type="button" class="btn btn-ghost block" data-print>%(print)s</button>
<a class="btn btn-go block" data-wa-stmt href="#" target="_blank" rel="noopener" data-ref="%(ref)s:statement-wa">%(wa_ic)s<span>%(send)s</span></a></div><p class="fine" data-copied aria-live="polite"></p><p class="fine">%(send_note)s</p></div>
<script type="application/json" class="stmt-strings">%(strings)s</script></form>""" % {
        "ref": E(ref), "not_official": E(S["not_official"]), "rows": "".join(rows), "make": E(S["make"]), "out_h": E(S["out_h"]),
        "copy": E(S["copy"]), "print": E(S["print"]), "wa_ic": I_WA, "send": E(S["send"]), "send_note": E(S["send_note"]),
        "strings": json.dumps({"title": S["text_title"], "copied": S["copied"], "footer": S["text_footer"], "wa_pre": S["wa_pre"], "wa": WA_NUMBER,
                               "labels": {f[0]: f[1] for _, fs in S["groups"] for f in fs}, "groups": [[g, [f[0] for f in fs]] for g, fs in S["groups"]]}, ensure_ascii=False).replace("</", "<\\/"),
    }

def report_page(lang):
    C = L[lang]; t = C.T; F = C.PAGES["report"]
    ft = FACT_TEXT[lang]
    body = """<div class="flowhead"><span class="pic">%(ic)s</span><div><h1 class="page-h1">%(h1)s</h1><p class="lead">%(lead)s</p></div></div>
<nav class="tabs" aria-label="%(on)s"><a href="#insurer">%(t1)s</a><a href="#police">%(t2)s</a><a href="#bring">%(t3)s</a><a href="#statement">%(t4)s</a></nav>
<section class="card" id="insurer"><h2>%(h_ins)s</h2><p>%(gia)s</p><p>%(arc)s</p>%(picker)s</section>
<section class="card" id="police"><h2>%(h_pol)s</h2><p>%(pol_p)s</p>%(cases)s<p>%(spf)s</p><p class="warn">%(not_same)s</p></section>
<section class="card" id="bring"><h2>%(h_bring)s</h2>%(bring)s<p class="fine">%(bring_note)s</p></section>
<section class="card" id="statement"><h2>%(h_st)s</h2><p>%(st_p)s</p>%(tool)s</section>
<div class="helpbox"><h3>%(help_h)s</h3><p>%(help_p)s</p><div class="endcta">%(wa)s</div></div>
%(lead)s%(faq)s%(srcbox)s""" % {
        "ic": ICONS["statement"], "h1": E(F["h1"]), "lead": E(F["lead"]), "on": E(F["on_page"]), "t1": E(F["t1"]), "t2": E(F["t2"]), "t3": E(F["t3"]), "t4": E(F["t4"]),
        "h_ins": E(F["h_ins"]), "gia": E(ft["gia_24h"]), "arc": E(F["arc"]), "picker": insurer_picker(lang, "report:insurer"),
        "h_pol": E(F["h_pol"]), "pol_p": E(F["pol_p"]), "cases": ul(ft["police_cases"]), "spf": E(ft["spf_how"]), "not_same": E(F["not_same"]),
        "h_bring": E(F["h_bring"]), "bring": ul(F["bring"]), "bring_note": E(F["bring_note"]),
        "h_st": E(F["h_st"]), "st_p": E(F["st_p"]), "tool": statement_tool(lang, "report"),
        "help_h": E(F["help_h"]), "help_p": E(F["help_p"]), "wa": hotline(lang, "report", "report:help-wa", t["wa_assist"]),
        "lead": lead_form(lang, "reporting", "reporting", "report:form"), "faq": faq_block(lang, F["faq"])[0], "srcbox": source_box(lang),
    }
    return page(lang, "report/", F["title"], F["desc"], body, "report", "report", schema=[faq_block(lang, F["faq"])[1]], crumbs=[(F["nav"], None)],
                scripts=("site.js", "lead.js"))

# ---------------- windscreen ----------------
def windscreen_page(lang):
    C = L[lang]; t = C.T; F = C.PAGES["windscreen"]
    secs = "".join('<section class="card"><h2>%s</h2>%s%s</section>' % (E(s["h"]), "".join("<p>%s</p>" % E(p) for p in s.get("p", [])), ul(s["li"]) if s.get("li") else "") for s in F["sections"])
    cover = '<section class="card"><h2>%s</h2><div class="choices" role="group" data-solo>%s</div>%s</section>' % (
        E(F["cover_h"]), "".join('<button type="button" class="choice" data-k="%s" aria-pressed="false">%s</button>' % (E(c[0]), E(c[1])) for c in F["cover"]),
        "".join('<p class="note" data-k="%s">%s</p>' % (E(c[0]), E(c[2])) for c in F["cover"]))
    body = """<div class="flowhead"><span class="pic">%s</span><div><h1 class="page-h1">%s</h1><p class="lead">%s</p></div></div>%s%s
<div class="helpbox"><h3>%s</h3><p>%s</p><div class="endcta">%s</div></div>%s%s%s""" % (
        ICONS["windscreen"], E(F["h1"]), E(F["lead"]), cover, secs, E(F["help_h"]), E(F["help_p"]), hotline(lang, "windscreen", "windscreen:help-wa", t["wa_assist"]),
        lead_form(lang, "windscreen", "windscreen", "windscreen:form"), faq_block(lang, F["faq"])[0], source_box(lang))
    return page(lang, "windscreen/", F["title"], F["desc"], body, "windscreen", "windscreen", schema=[faq_block(lang, F["faq"])[1]], crumbs=[(F["nav"], None)],
                scripts=("site.js", "lead.js"))

# ---------------- FAQ, guides ----------------
def faq_page(lang):
    C = L[lang]; F = C.PAGES["faq"]
    parts, allq = [], []
    for grp, qs in F["groups"]:
        parts.append(faq_block(lang, qs, grp, "faq faq-g")[0]); allq += qs
    sd = faq_block(lang, allq)[1]
    body = '<h1 class="page-h1">%s</h1><p class="lead">%s</p>%s<div class="helpbox"><h3>%s</h3><div class="endcta">%s</div></div>%s' % (
        E(F["h1"]), E(F["lead"]), "".join(parts), E(F["help_h"]), hotline(lang, "home", "faq:help-wa", L[lang].T["wa_assist"]), source_box(lang))
    return page(lang, "faq/", F["title"], F["desc"], body, "home", "faq", schema=[sd], crumbs=[(F["nav"], None)])

def guides_index(lang):
    C = L[lang]; F = C.PAGES["guides"]
    lis = "".join('<li><a href="%s"><b>%s</b><small>%s</small></a></li>' % (url(lang, "guides/%s/" % g["slug"]), E(g["h1"]), E(g["desc"])) for g in G[lang].GUIDES)
    body = '<h1 class="page-h1">%s</h1><p class="lead">%s</p><ul class="gl">%s</ul>' % (E(F["h1"]), E(F["lead"]), lis)
    il = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": k + 1, "name": g["h1"], "url": absu(lang, "guides/%s/" % g["slug"])} for k, g in enumerate(G[lang].GUIDES)]}
    return page(lang, "guides/", F["title"], F["desc"], body, "home", "guides", schema=[il], crumbs=[(F["nav"], None)])

IMG_V = "1"
def guide_img(lang, slug):
    """Each guide's own cover / share image (Bridge IMAGE GATE): images/articles/<slug>.jpg, <slug>-zh.jpg for 中文."""
    return "images/articles/%s%s.jpg" % (slug, "" if lang == "en" else "-zh")

GUIDE_PUBLISHED = "2026-11-21"  # live Article JSON-LD datePublished/dateModified on all guides (22 Nov 2026 sync)

def upd_html(lang, t):
    """Live (22 Nov 2026): EN 'Updated 22 Nov 2026 . Sources: GIA, SPF'; ZH keeps the older 'last checked' line (live ZH wording not captured)."""
    if lang != "en":
        return E(t["updated"].replace("{d}", TODAY))
    d = datetime.date.fromisoformat(TODAY)
    return 'Updated %d %s %d<span class="qw-s"> · Sources: <a href="%s" rel="noopener">GIA</a>, <a href="%s" rel="noopener">SPF</a></span>' % (
        d.day, d.strftime("%b"), d.year, E(GIA_MCF), E(SPF["url"] if isinstance(SPF, dict) else SPF))

def guide_page(lang, g):
    C = L[lang]; t = C.T
    secs = []
    for s in g["sections"]:
        x = '<h2>%s</h2>' % E(s["h"])
        x += "".join("<p>%s</p>" % E(fill(lang, p)) for p in s.get("p", []))
        if s.get("li"):
            x += ul(s["li"])
        x += "".join("<p>%s</p>" % E(fill(lang, p)) for p in s.get("p2", []))
        secs.append(x)
    rel = "".join('<a class="btn btn-ghost block" href="%s">%s</a>' % (url(lang, u), E(n)) for n, u in g.get("next", []))
    srcs = "".join('<li><a href="%s" rel="noopener">%s</a></li>' % (E(u), E(n)) for n, u in g.get("sources", []))
    faq_h, faq_sd = faq_block(lang, g.get("faq"))
    img = guide_img(lang, g["slug"])
    alt = ("Illustrative guide cover: " if lang == "en" else "示意指南封面：") + g["nav"]
    hero = '<img class="hero-img" src="%s" alt="%s" width="1200" height="630" fetchpriority="high" style="display:block;width:100%%;height:auto;border-radius:14px;margin:4px 0 14px;background:#0B5A8C">' % (E(BASE + img + "?v=" + IMG_V), E(alt))
    body = ("""<article class="art"><h1 class="page-h1">%s</h1><p class="lead">%s</p>""" + hero.replace("%", "%%") + """<p class="upd">%s</p>
<div class="tldr"><p class="lbl">%s</p>%s</div>%s
<div class="helpbox"><h3>%s</h3><div class="endcta">%s%s</div></div>%s
<div class="srcbox"><p class="lbl">%s</p><ul>%s</ul></div></article>""") % (
        E(g["h1"]), E(g["lead"]), upd_html(lang, t), E(t["in_short"]), ul(g["short"]), "".join(secs),
        E(t["next_step"]), rel, hotline(lang, g.get("wa", "home"), "guide:" + g["slug"], t["wa_assist"]), faq_h, E(t["sources_box"]), srcs)
    art = {"@context": "https://schema.org", "@type": "Article", "headline": g["h1"], "description": g["desc"], "inLanguage": t["html_lang"],
           "datePublished": GUIDE_PUBLISHED, "dateModified": GUIDE_PUBLISHED, "mainEntityOfPage": absu(lang, "guides/%s/" % g["slug"]), "image": CFG.share_base + img,
           "author": {"@type": "Organization", "name": "SGCarAccident"}, "publisher": {"@type": "Organization", "name": "SGCarAccident"}}
    return page(lang, "guides/%s/" % g["slug"], g["title"], g["desc"], body, g.get("wa", "home"), "guide:" + g["slug"], schema=[art, faq_sd],
                crumbs=[(C.PAGES["guides"]["nav"], url(lang, "guides/")), (g["nav"], None)], img=img, img_alt=alt)

# ---------------- private settlement (form kept from v1, plus guidance) ----------------
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
    C = L[lang]; t = C.T; S = C.SETTLE; F = C.PAGES["settlement"]
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
    explain = '<section class="card"><h2>%s</h2>%s<p class="warn">%s</p><p>%s</p></section>' % (
        E(F["what_h"]), "".join("<p>%s</p>" % E(p) for p in F["what_p"]), E(F["mcf_warn"]), E(F["no_guarantee"]))
    body = """<div class="flowhead"><span class="pic">%(ic)s</span><div><h1 class="page-h1">%(h1)s</h1><p class="lead">%(lead)s</p></div></div>
%(explain)s
<div id="settle" data-api="%(api)s" data-lang="%(lang)s" data-sign="%(sign)s">
<div id="settle-intro"><div class="intro"><p class="lbl">%(how_h)s</p><ul>%(intro)s</ul></div><button type="button" class="btn btn-sign block" data-start>%(start)s</button>
<noscript><p class="err">JavaScript is needed for this form.</p></noscript></div>
<form id="settle-form" class="form" hidden novalidate>
<div class="prog" aria-hidden="true"><i></i></div><p class="prog-l" data-tpl="%(stepof)s" aria-live="polite"></p>
%(steps)s<p class="err" role="alert"></p>
<div class="nav" style="display:grid"><button type="button" class="btn btn-ghost" data-back>%(back)s</button><button type="button" class="btn btn-sign" data-next>%(next)s</button><button type="submit" class="btn btn-go" data-save hidden><span>%(save)s</span></button></div>
</form>
<div id="settle-done" hidden><div class="step" style="display:block"><h2>%(done_h)s</h2><p>%(done_p)s</p><div class="endcta">
<button type="button" class="btn btn-sign block" data-pdf>%(dl)s</button><button type="button" class="btn btn-go block" data-share data-cta="share_link">%(share)s</button>
<input id="shareLink" readonly aria-label="%(share)s" class="share-in"><p data-copied aria-live="polite"></p></div>
<div class="remind">%(remind)s</div></div></div>
</div>%(dl_list)s%(strings)s
<div class="helpbox"><h3>%(help_h)s</h3><p>%(help_p)s</p><div class="endcta">%(wa)s<a class="btn btn-ghost block" href="%(ns)s">%(ns_l)s</a></div></div>""" % {
        "ic": ICONS["settlement"], "h1": E(F["h1"]), "lead": E(F["lead"]), "explain": explain, "api": API, "lang": lang, "sign": url(lang, "private-settlement/sign/"),
        "how_h": E(F["how_h"]), "intro": "".join("<li>%s</li>" % E(x) for x in S["intro_li"]), "start": E(S["start"]),
        "stepof": E(t["step_of"]), "steps": "".join(steps), "back": E(t["back"]), "next": E(t["next"]), "save": E(S["save"]),
        "done_h": E(S["done_h"]), "done_p": E(S["done_p"]), "dl": E(S["download"]), "share": E(S["share"]), "remind": E(S["remind"]),
        "dl_list": dl, "strings": settle_strings(lang), "help_h": E(F["help_h"]), "help_p": E(F["help_p"]),
        "wa": hotline(lang, "settlement", "settlement:help-wa", t["wa_assist"]), "ns": url(lang, "not-sure/"), "ns_l": E(F["ns_link"]),
    }
    faq_h, faq_sd = faq_block(lang, F["faq"])
    return page(lang, "private-settlement/", F["title"], F["desc"], body + faq_h + source_box(lang), "settlement", "settlement", schema=[faq_sd],
                scripts=("jspdf.umd.min.js", "settle.js"), crumbs=[(F["nav"], None)])

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
                alt=False, scripts=("jspdf.umd.min.js", "settle.js"), extra_head='<meta name="robots" content="noindex, noarchive">')

def simple_page(lang, path, P, key="home", ref=None):
    body = '<h1 class="page-h1">%s</h1>%s' % (E(P["h1"]), "".join("<p>%s</p>" % E(p) for p in P["body"]))
    return page(lang, path, P["title"], P["desc"], body, key, ref or path.strip("/"), crumbs=[(P["h1"], None)])

def notfound(lang):
    t = L[lang].T; H = L[lang].HOME
    paths = "".join('<a class="path p-%s" href="%s"><span class="pt"><b>%s</b><small>%s</small></span><span class="chev">%s</span></a>' % (k, url(lang, h), E(H["paths"][k][0]), E(H["paths"][k][1]), I_CHEV)
                    for k, h in [("fault", "own-damage/"), ("unsure", "not-sure/"), ("notfault", "third-party/")])
    body = '<h1 class="page-h1">%s</h1><p class="lead">%s</p><div class="paths">%s</div>' % (E(t["not_found"]), E(t["not_found_p"]), paths)
    return page(lang, "404.html", t["not_found"] + " | SGCarAccident", t["not_found_p"], body, "home", "404", alt=False,
                extra_head='<meta name="robots" content="noindex">')

def moved(lang, to):
    """Old/broken URL -> real page (the 19 Nov home card pointed at /settlement/)."""
    u = url(lang, to)
    return '<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>SGCarAccident</title><meta name="robots" content="noindex"><link rel="canonical" href="%s"><meta http-equiv="refresh" content="0;url=%s"></head><body><p><a href="%s">%s</a></p></body></html>\n' % (
        L[lang].T["html_lang"], absu(lang, to), u, u, E(L[lang].PAGES["settlement"]["h1"]))

# ---------------- write ----------------
def write(rel, s):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(s)

def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "assets", "centres"))
    for f in os.listdir(os.path.join(SRC, "assets")):
        if os.path.isfile(os.path.join(SRC, "assets", f)):
            shutil.copy(os.path.join(SRC, "assets", f), os.path.join(OUT, "assets", f))
    if os.path.isdir(os.path.join(SRC, "images")):
        shutil.copytree(os.path.join(SRC, "images"), os.path.join(OUT, "images"))
    open(os.path.join(OUT, "assets", "icon.svg"), "w").write(LOGO.replace('<svg ', '<svg xmlns="http://www.w3.org/2000/svg" '))
    paths = []
    for lang in ("en", "zh"):
        pre = "zh/" if lang == "zh" else ""
        for ins in INSURERS:
            write("assets/centres/%s.%s.json" % (ins["slug"], lang), json.dumps(centre_json(lang, ins), ensure_ascii=False, separators=(",", ":")))
        write(pre + "index.html", home(lang)); paths.append("")
        for slug in ["own-damage", "not-sure", "third-party", "minor-car-accident", "hit-and-run", "tow"]:
            write(pre + slug + "/index.html", flow_page(lang, slug)); paths.append(slug + "/")
        write(pre + "windscreen/index.html", windscreen_page(lang)); paths.append("windscreen/")
        write(pre + "report/index.html", report_page(lang)); paths.append("report/")
        write(pre + "private-settlement/index.html", settlement(lang)); paths.append("private-settlement/")
        write(pre + "private-settlement/sign/index.html", sign_page(lang))
        write(pre + "settlement/index.html", moved(lang, "private-settlement/"))
        write(pre + "insurers/index.html", insurer_index(lang)); paths.append("insurers/")
        for ins in INSURERS:
            write(pre + "insurers/%s/index.html" % ins["slug"], insurer_page(lang, ins)); paths.append("insurers/%s/" % ins["slug"])
        write(pre + "faq/index.html", faq_page(lang)); paths.append("faq/")
        write(pre + "guides/index.html", guides_index(lang)); paths.append("guides/")
        for g in G[lang].GUIDES:
            write(pre + "guides/%s/index.html" % g["slug"], guide_page(lang, g)); paths.append("guides/%s/" % g["slug"])
        write(pre + "privacy/index.html", simple_page(lang, "privacy/", L[lang].PRIVACY)); paths.append("privacy/")
        write(pre + "404.html", notfound(lang))
    paths = sorted(set(paths), key=paths.index)
    write("sitemap.xml", golive.sitemap_xml(CFG, paths, TODAY))
    write("robots.txt", golive.robots_txt(CFG).replace("Allow: /\n", "Allow: /\nDisallow: %sprivate-settlement/sign/\nDisallow: %szh/private-settlement/sign/\n" % (
        "/" if CFG.live_domain else CFG.preview_path, "/" if CFG.live_domain else CFG.preview_path)))
    llms = golive.llms_header(CFG, "SGCarAccident", "Step-by-step help after a car accident in Singapore: at fault, not sure, or not at fault (third-party claim); minor accidents; hit and run; insurer reporting centres; accident statement helper; private settlement form; windscreen claims. General guidance, not an insurer or law firm.")
    llms += "\n## Pages\n" + "\n".join("- %s" % absu("en", p) for p in paths) + "\n"
    write("llms.txt", llms)
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print("built", n, "files,", len(paths) * 2, "sitemap urls,", len(INSURERS), "insurers,", len(G["en"].GUIDES), "guides")

if __name__ == "__main__":
    main()
