#!/usr/bin/env python3
"""Battery Rescue SG (batteryrescue.sg, by Motoserv) static app-style site.

Run:  python3 build.py OUT_DIR      (writes the whole site into OUT_DIR)
Facts: FACTS.md in this folder (Edwin, 24-26 Oct 2026). Prices: Delkor official list 26 Oct 2026 (incl. GST).
Fitment: data/sg-chart.csv (Bateriku/Astra 2023 chart, Asian makes) + data/namwah-fit.json (Nam Wah 2024 guide,
other makes). Reference data only: we sell DELKOR, sizes are matched to the Delkor list; unmatched sizes = enquire.
Price rules (confirmed): walk-in at Motoserv = list - $20 web code (walk-in only); fitted at your location
before 10pm incl. Sunday = list + $30 (launch promo, normally + $50); 10pm-9am and public holidays = list + $80. 1-year warranty.
Preview: pageonesingapore.com/preview/battery-rescue/ (hidden by the preview .htaccess header, no noindex in pages).
"""
import csv, html, json, os, re, sys, hashlib, datetime
from PIL import Image
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else HERE / "site")
LIVE = False
DOMAIN = "batteryrescue.sg"
BASE = "https://batteryrescue.sg"
GBP = "https://maps.app.goo.gl/VrQtHKzr6Yx2y8Wv5"  # Battery Rescue Google profile (Edwin, 28 Oct 2026: 5 stars)
TODAY = datetime.date.today().isoformat()
CHECKED = "26 Oct 2026"
# Pages keep their sitemap lastmod until their rendered content changes (ledger in lastmod.json, committed with the source).
LEDGER_F = HERE / "lastmod.json"
try: LEDGER = json.loads(LEDGER_F.read_text())
except Exception: LEDGER = {}
NEWLEDGER = {}
LASTMOD = {}
ART_UPDATED = "2026-11-02"; ART_UPDATED_TXT = "2 Nov 2026"
HOT = "8125 9169"; TEL = "+6581259169"; WA = "6581259169"
HOURS_WALK = "Mon-Sat 9am-6pm"
BRAND = "Battery Rescue SG"
CALLX = f'<a href="tel:{TEL}" data-ref="art">{HOT}</a>'

# ---------------- prices (Delkor official list, SGD incl. GST) ----------------
PRICES = [  # key, also-known-as, Ah, list price, type
 ("NS40ZL","42B20L",38,119.90,"Standard"),("NS60L","65B24L",50,130.80,"Standard"),("NS60LS","65B24LS",50,130.80,"Standard"),
 ("NS60ST","65B24R",45,130.80,"Standard"),("85D23L","",65,174.40,"Standard"),("100D26L","",75,207.10,"Standard"),
 ("130D31L","",100,239.80,"Standard"),("130D31R","",100,239.80,"Standard"),("DIN45L","54533",45,152.60,"Standard (DIN)"),
 ("DIN60L","56030",60,207.10,"Standard (DIN)"),("DIN66L","56618",66,218.00,"Standard (DIN)"),("DIN74L","57412",74,239.80,"Standard (DIN)"),
 ("M42","60B20L",40,174.40,"Start-stop (Japanese)"),("EFB-N55","80B24L",55,196.20,"EFB start-stop"),("EFB-Q85L","115D23L",70,228.90,"EFB start-stop"),
 ("EFB-S95","130D26L",75,272.50,"EFB start-stop"),("EFB-LN2","DIN60",60,239.80,"EFB start-stop"),("EFB-LN3","DIN75L",70,261.60,"EFB start-stop"),
 ("AGM-LN1","DIN45L",50,250.70,"AGM"),("AGM-LN2","DIN55L",60,283.40,"AGM"),("AGM-LN3","DIN75L",70,337.90,"AGM"),
 ("AGM-LN4","DIN80L",80,414.20,"AGM"),("AGM-LN5","DIN100L",95,468.70,"AGM"),
]
P = {k: (ah, lp) for k, aka, ah, lp, t in PRICES}
AKA = {k: aka for k, aka, ah, lp, t in PRICES}
TYPE = {k: t for k, aka, ah, lp, t in PRICES}
NAME = {k: k.replace("AGM-", "AGM ").replace("EFB-LN3", "EFB LN3") for k in P}
def slug(s): return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
def m(x): return f"${x:,.2f}"
def walk(k): return P[k][1] - 20
PROMO_LBL = "Launch promo: $20 off before 10pm, incl. Sunday"
def day(k): return P[k][1] + 30   # launch promo (Edwin, 7 Nov 2026): $20 off the usual list + $50, before 10pm incl. Sunday
def dayw(k): return P[k][1] + 50  # usual before-10pm price, shown struck through
def md(k): return f"\u27ea{m(dayw(k))}|{m(day(k))}\u27eb"  # promo price token, rendered by promo_html / promo_txt
PTOK = re.compile("\u27ea([^|\u27eb]+)\\|([^\u27eb]+)\u27eb")
def promo_html(t): return PTOK.sub(lambda x: f'<span class="pp"><s>{x[1]}</s> {x[2]}</span>', t)
def promo_txt(t): return PTOK.sub(lambda x: f'{x[2]} (launch promo, usually {x[1]})', t)
def promo_short(t): return PTOK.sub(lambda x: f'{x[2]} (launch promo)', t)
def night(k): return P[k][1] + 80

# ---------------- outlets (Motoserv poster; coords approximate, for nearest-first sorting only) ----------------
OUTLETS = [
 ("Bukit Batok","Shell","28 Bukit Batok East Ave 6",1.3463,103.7569),
 ("Bukit Panjang","Shell","772 Upper Bukit Timah Rd",1.3772,103.7652),
 ("Boon Lay","Shell","2 Boon Lay Ave",1.3446,103.7123),
 ("Sembawang","Shell","595 Sembawang Rd",1.4146,103.8215),
 ("Toa Payoh","Shell","248 Lorong 1 Toa Payoh",1.3381,103.8526),
 ("Havelock Road","Shell","548 Havelock Rd, Singapore 169637",1.2893,103.8317),
 ("Bukit Timah","Shell","219 Upper Bukit Timah Rd",1.3437,103.7752),
 ("Upper Thomson Road","Mobil","553 Upper Thomson Rd, Singapore 574416",1.3577,103.8292),
 ("Jervois","Shell","2 Jervois Rd, Singapore 248994",1.2933,103.8273),
 ("Serangoon Garden","Shell","49 Serangoon Garden Way, Singapore 555944",1.3641,103.8659),
]
AREAS = [("Woodlands",1.4360,103.7865),("Sembawang",1.4491,103.8185),("Yishun",1.4304,103.8354),("Ang Mo Kio",1.3691,103.8454),
         ("Yio Chu Kang",1.3818,103.8448),("Hougang",1.3612,103.8863),("Sengkang",1.3911,103.8950),("Punggol",1.4043,103.9020)]
AREA_TXT = "Woodlands, Sembawang, Yishun, Ang Mo Kio, Yio Chu Kang, Hougang, Sengkang and Punggol"
COVER_TXT = f"all of Singapore, fastest in the North and North-East ({AREA_TXT})"
import math
def dist(a, b):
    R_ = 6371; dl = math.radians(b[0]-a[0]); dn = math.radians(b[1]-a[1])
    x = math.sin(dl/2)**2 + math.cos(math.radians(a[0]))*math.cos(math.radians(b[0]))*math.sin(dn/2)**2
    return 2*R_*math.asin(math.sqrt(x))
STATION = {"Shell":"Shell Autoserv station","Mobil":"Mobil One CarCare"}

# ---------------- fitment ----------------
NORM = {}
def put(keys, v):
    for k in keys.split(): NORM[k] = v
put("NS40ZL 42B20L 38B20L NS40ZLS", "NS40ZL")
put("NS60L 55B24L 46B24L 65B24L 50B24L NS60", "NS60L")
put("NS60LS 55B24LS 65B24LS 50B24LS", "NS60LS")
put("85D23L 55D23L 70D23L 75D23L 90D23L", "85D23L")
put("100D26L 80D26L 75D26L 95D26L 65D26L NS70L 110D26L 60D26L", "100D26L")
put("130D31L 95D31L 105D31L 115D31L 125D31L NX1207L", "130D31L")
put("130D31R 95D31R 105D31R 115D31R 125D31R NX1207R", "130D31R")
put("DIN45L", "DIN45L"); put("DIN60L", "DIN60L"); put("DIN66L", "DIN66L"); put("DIN74L", "DIN74L")
put("M42 M42L 60B20L", "M42")
put("N55 N55L EFBN55 EFBN55L", "EFB-N55"); put("Q85 Q85L EFBQ85 EFBQ85L", "EFB-Q85L"); put("S95 S95L EFBS95 EFBS95L", "EFB-S95")
put("LN2EFB EFBL2 EFBLN2", "EFB-LN2"); put("LN3EFB EFBL3 EFBLN3", "EFB-LN3")
for i in range(1, 6): put(f"AGML{i} AGMLN{i} LN{i}AGM", f"AGM-LN{i}")
def to_delkor(raw):
    s = raw.upper().replace("AMARON", "").replace("X 2", "")
    s = re.sub(r"\b(FLO|PRO|JADE|ONYX|SMF)\b", "", s)
    for part in re.split(r"[/,]", s):
        k = re.sub(r"[^A-Z0-9]", "", part)
        if k in NORM: return NORM[k]
    return None
# Sizes not on the Delkor list, matched by standard case size (JIS/EN), Edwin 1 Nov 2026.
# R-terminal D23/D26/B20 and twin-battery cars stay "enquire": no same-size Delkor on the list.
EQN = ["", "Same L4 case size. AGM is an upgrade on a standard battery.", "Same L5 case size. AGM is an upgrade on a standard battery.",
       "Same L2 case size, slightly higher capacity.", "Same L3 case size.", "Same B24 size, right-hand terminal.",
       "AGM suits cars built for AGM or EFB.", "Same D26 size, left-hand terminal."]
EQUIV = {"DIN80L":("AGM-LN4",1), "DIN100L":("AGM-LN5",2), "DIN100LDIN110L":("AGM-LN5",2), "DIN55L":("DIN60L",3), "DIN75L":("DIN74L",4),
         "NS60R":("NS60ST",5), "S46B24R":("NS60ST",5), "55B24R":("NS60ST",5), "46B24R":("NS60ST",5),
         "DIN60AGMEFB":("AGM-LN2",6), "DIN70AGMEFB":("AGM-LN3",6), "DIN70AGM":("AGM-LN3",0), "LNE3EFBAGM":("AGM-LN3",6), "85D26L":("100D26L",7)}
def equiv(raw):
    k = re.sub(r"[^A-Z0-9]", "", re.sub(r"\bAMARON\b|\b(FLO|PRO|JADE|ONYX|SMF)\b", "", raw.upper()))
    return EQUIV.get(k, (None, 0))
def clean_size(raw):
    s = re.sub(r"\bAMARON\b|\b(FLO|PRO|JADE|ONYX|SMF)\b", "", raw.upper()).replace("X 2", "x2")
    return re.sub(r"\s+", " ", s).strip(" /")
def yr_end(y):
    if re.search(r"present|preset|on\b", y, re.I): return 2099
    n = re.findall(r"(19|20)(\d\d)", y)
    return int("".join(n[-1])) if n else 2099
ASIAN = {"Toyota","Honda","Nissan","Mazda","Mitsubishi","Hyundai","Kia","Lexus","Subaru","Suzuki","Daihatsu","Perodua","Proton",
         "Isuzu","Infiniti","Ssangyong","Inokom","Naza","Hino","Chery","Great Wall","Haval","Byd","Mg","Maxus","Tata","Mahindra"}
MAKE_FIX = {"Mercedes":"Mercedes-Benz","Landrover":"Land Rover","Range Rover":"Land Rover","Chev / Gmc":"Chevrolet","Rolls Royce":"Rolls-Royce","Mg":"MG","Byd":"BYD","Ssangyong":"SsangYong"}
def _w(w):
    if w in ("NEW","GEN","OLD","VAN","CAB","AND"): return w.title()
    if re.search(r"\d", w) or len(w) <= 3 or re.match(r"^[A-Z]{1,3}-[A-Z0-9]+$", w): return w
    return w[0] + w[1:].lower()
def tidy_model(s):
    s = re.sub(r"\s+", " ", s).strip()
    return " ".join(_w(w) for w in s.split(" ")) if s.isupper() else s
def tidy_years(y):
    y = re.sub(r"\s*-\s*", "-", y.strip()); y = re.sub(r"(?i)preset|present", "now", y); return re.sub(r"(?i)-on$", "-now", y)
rows = []
sg = HERE / "data" / "sg-chart.csv"
sg_makes = set()
if sg.exists():
    for r in csv.DictReader(open(sg, encoding="utf-8")):
        mk = r["make"].strip().title()
        if "UNREADABLE" in (r["battery_size"] + r["model"]).upper() or mk not in ASIAN: continue
        sg_makes.add(mk)
        rows.append([MAKE_FIX.get(mk, mk), tidy_model(r["model"]), tidy_years(r["years"]), clean_size(r["battery_size"]), to_delkor(r["battery_size"]) or equiv(r["battery_size"])[0], "sg", 0 if to_delkor(r["battery_size"]) else equiv(r["battery_size"])[1]])
for mk, model, yrs, code in json.load(open(HERE / "data" / "namwah-fit.json")):
    mk = mk.strip()
    if mk in sg_makes or mk in ("Holden",) or yr_end(yrs) < 2005: continue
    rows.append([MAKE_FIX.get(mk, mk), tidy_model(model), tidy_years(yrs), clean_size(code), to_delkor(code) or equiv(code)[0], "nw", 0 if to_delkor(code) else equiv(code)[1]])
# Edwin 26 Oct 2026: Honda Shuttle follows Vezel
if not any(r[0] == "Honda" and "Shuttle" in r[1] for r in rows):
    rows += [["Honda","Shuttle","2015-2022","55B24L","NS60L","edwin",0],["Honda","Shuttle Hybrid","2015-2022","M42L","M42","edwin",0]]
# Edwin 3 Nov 2026: Toyota Yaris Cross non-hybrid uses DIN45
if not any(r[0] == "Toyota" and "Yaris Cross" in r[1] for r in rows):
    rows += [["Toyota","Yaris Cross (non-hybrid)","2020-now","DIN45L","DIN45L","edwin",0]]
# Edwin 3 Nov 2026: Honda N-Van uses M42L
if not any(r[0] == "Honda" and "N-Van" in r[1] for r in rows):
    rows += [["Honda","N-Van","2018-now","M42L","M42","edwin",0]]
rows.sort(key=lambda r: (r[0], r[1], r[2]))
MAKES = {}
for r in rows: MAKES.setdefault(r[0], []).append(r)
# brand pages only for makes with enough rows to be useful
BRAND_PAGES = sorted(mk for mk in ["Toyota","Honda","Nissan","Mazda","Mitsubishi","Hyundai","Kia","Lexus","Subaru","Suzuki","Mercedes-Benz","BMW","Audi",
  "Volkswagen","Volvo","Porsche","Mini","Peugeot","Renault","Citroen","Skoda","Ford","Jaguar","Land Rover"] if mk in MAKES)
BY_SIZE = {}
for r in rows:
    if r[4]: BY_SIZE.setdefault(r[4], []).append(r)

# ---------------- icons ----------------
BOLT = '<svg viewBox="0 0 24 24" fill="none"><rect x="2.5" y="7" width="19" height="13" rx="2.5" fill="#ffc400"/><rect x="6" y="4.5" width="3.2" height="2.6" rx=".6" fill="#ffc400"/><rect x="14.8" y="4.5" width="3.2" height="2.6" rx=".6" fill="#ffc400"/><path d="M13 9.2 9.2 14h3l-1.2 4 4-5.1h-3.1z" fill="#0b1b4d"/></svg>'
I = {
 "phone":'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>',
 "wa":'<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 14.2c-.2.6-1.3 1.2-1.8 1.3-.5.1-1 .1-1.7-.1-.4-.1-.9-.3-1.5-.6-2.7-1.2-4.4-3.9-4.6-4.1-.1-.2-1.1-1.4-1.1-2.7s.7-1.9.9-2.2c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.3 0 .5l-.3.5-.4.4c-.1.1-.3.3-.1.6.2.3.7 1.2 1.6 2 1.1 1 2 1.3 2.3 1.4.3.1.5.1.6-.1l.9-1c.2-.3.4-.2.7-.1l1.9.9c.3.1.5.2.5.3.1.2.1.7-.1 1.3z"/></svg>',
 "sos":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M12 3 2 20h20z"/><path d="M12 9v5M12 17.5v.01"/></svg>',
 "tag":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"><path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/></svg>',
 "pin":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
 "menu":'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 6h16M4 12h16M4 18h16"/></svg>',
 "shield":'<svg viewBox="0 0 24 24" fill="none" stroke="#1d3fa8" stroke-width="2"><path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/></svg>',
}

# ---------------- page shell ----------------
CSS = (HERE / "br.css").read_text(); JS = (HERE / "br.js").read_text()
def h8(s): return hashlib.sha1(s.encode()).hexdigest()[:8]
pages = []  # (path, priority)
PTITLES = {}; PDESC = {}  # path -> page <title>, used by llms.txt
def esc(s): return html.escape(str(s), quote=True)
def org():
    return {"@type":"AutomotiveBusiness","@id":BASE+"/#org","name":BRAND,"url":BASE+"/","sameAs":[GBP],"telephone":TEL,"image":BASE+"/og.jpg","logo":BASE+"/icon-512.png",
     "description":"Delkor car battery replacement in Singapore: fitted at your location (24-hour hotline) or walk-in at 10 Motoserv outlets.",
     "areaServed":[{"@type":"Country","name":"Singapore"}]+[{"@type":"Place","name":a+", Singapore"} for a,_,_ in AREAS],"priceRange":"$99.90-$548.70",
     "parentOrganization":{"@type":"Organization","name":"Motoserv","url":"https://motoserv.sg/","sameAs":["https://www.facebook.com/motoserv.sg","https://www.tiktok.com/@motoserv.sg"]},
     "brand":{"@type":"Brand","name":"Delkor"},
     "contactPoint":{"@type":"ContactPoint","telephone":TEL,"contactType":"customer service","hoursAvailable":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"00:00","closes":"23:59"}}}
def crumbs_ld(cr):
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":BASE+u} for i,(n,u) in enumerate(cr)]}
def faq_ld(faqs):
    return {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub("<[^>]+>","",a)}} for q,a in faqs]}
def faq_html(faqs):
    return '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q,a in faqs) + "</div>"
def tab(active):
    t = [("/","sos","Rescue","sos"),("/#compare","tag","Prices",""),("/outlets/","pin","Outlets",""),("/more/","menu","More","")]
    return '<nav class="tabs" aria-label="App">' + "".join(
        f'<a href="{u}" class="{c}{" on" if active==l else ""}">{I[ic]}{l}</a>' for u,ic,l,c in t) + "</nav>"
def actbar(ref=""):
    return (f'<div class="act"><a class="c" href="tel:{TEL}" data-ref="{ref}">{I["phone"]}Call</a>'
            f'<a class="w wa-dyn" href="https://wa.me/{WA}" data-ref="{ref}">{I["wa"]}WhatsApp</a></div>')
TFIX = {" | Size by Model": "", " | 24h Hotline": "", ": We Come to You": "", " | Battery Rescue SG": " | Battery Rescue"}
def short_title(t):
    for a, b in TFIX.items(): t = t.replace(a, b)
    return t
def page(path, title, desc, body, ld=None, active="", cr=None, prio="0.6", img_alt="Battery Rescue SG: Delkor car battery replacement in Singapore", lean=False):
    title = short_title(promo_short(title)); desc = promo_short(desc); body = promo_html(body)
    assert PTOK.search(title + desc + body) is None, path
    assert len(title) <= 65, (path, len(title), title)
    assert path == "/404.html" or 120 <= len(desc) <= 160, (path, len(desc), desc)
    url = BASE + path
    graph = [org()] + (ld or [])
    if cr: graph.append(crumbs_ld(cr))
    graph.append({"@type":"WebPage","@id":url,"url":url,"name":title,"description":desc,"dateModified":"__LM__","inLanguage":"en-SG",
                  "isPartOf":{"@type":"WebSite","name":BRAND,"url":BASE+"/"},"primaryImageOfPage":BASE+"/og.jpg"})
    crumb = ""
    if cr and len(cr) > 1:
        crumb = '<div class="crumb">' + " › ".join(f'<a href="{u}">{esc(n)}</a>' for n,u in cr[:-1]) + f" › {esc(cr[-1][0])}</div>"
    doc = f"""<!doctype html><html lang="en-SG"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}">
{"" if path == "/404.html" else f'<link rel="canonical" href="{url}">'}<meta name="robots" content="max-image-preview:large">
<meta name="theme-color" content="#0b1b4d"><link rel="manifest" href="/manifest.webmanifest">
<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-title" content="Battery Rescue">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
{"" if path == "/404.html" else f'<meta property="og:url" content="{url}">'}<meta property="og:image" content="{BASE}/og.jpg"><meta property="og:image:secure_url" content="{BASE}/og.jpg"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(img_alt)}">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}/og.jpg">
<link rel="stylesheet" href="/br.css?v={h8(CSS)}">
<script type="application/ld+json">{promo_txt(json.dumps({"@context":"https://schema.org","@graph":graph},ensure_ascii=False))}</script>
</head><body{' class="nobar"' if lean else ''}>
<header class="top"><div class="wrap"><a class="logo" href="/" aria-label="Battery Rescue SG home">{BOLT}<span>Battery<b>Rescue</b>.sg<small>by Motoserv · Delkor batteries</small></span></a>
<nav class="dnav"><a href="/">Rescue</a><a href="/#compare">Compare prices</a><a href="/prices/">Price list</a><a href="/outlets/">Outlets</a><a href="/delkor/">Why Delkor</a><a href="/more/">More</a></nav>
{"" if lean else f'<a class="hot" href="tel:{TEL}" data-ref="top">{I["phone"]}<span>{HOT}</span></a>'}</div></header>
<main class="wrap">{crumb}{body}
<footer class="foot"><p><b>{BRAND}</b> is the car battery service of Motoserv, a CaseTrust-accredited group of neighbourhood car service centres. Every battery we fit is a Delkor with a 1-year warranty. Prices include GST, checked {CHECKED}.</p>
<p>24-hour hotline <a href="tel:{TEL}" data-ref="foot">{HOT}</a> · <a href="/prices/">Prices</a> · <a href="/outlets/">Outlets</a> · <a href="/about/">About</a> · <a href="/privacy/">Privacy</a></p>
<p>Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></p></footer></main>
{"" if lean else actbar(slug(path) or "home")}{tab(active)}
<div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-label="Your walk-in code"><div class="in">
<div class="h1" style="font-size:20px">Your $20 walk-in code</div><div class="code">BR-0000</div>
<p><b id="sh-b"></b></p><p class="sub">Show this code at <b id="sh-o"></b> ({HOURS_WALK}). Walk-in only, one code per battery. Take a screenshot.</p>
<button class="big n" data-close="1">Done</button></div></div>
<script src="/data.js?v={h8(DATAJS)}" defer></script><script src="/br.js?v={h8(JS)}" defer></script>
</body></html>"""
    hh = hashlib.sha1(re.sub(r"\?v=[0-9a-f]{8}", "", doc).encode()).hexdigest()[:12]
    led = LEDGER.get(path)
    lm = led["d"] if led and led["h"] == hh else TODAY
    NEWLEDGER[path] = {"h": hh, "d": lm}; LASTMOD[path] = lm
    doc = doc.replace("__LM__", lm)
    # relative links so the same files work at /preview/battery-rescue/ and on the live domain
    depth = path.strip("/").count("/") + 1 if path.strip("/") and path.endswith("/") else 0
    pre = "../" * depth or "./"
    if path != "/404.html": doc = re.sub(r'(href|src)="/(?!/)', lambda mm: f'{mm.group(1)}="{pre}', doc)
    out = OUT / path.lstrip("/") / "index.html" if path.endswith("/") else OUT / path.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc)
    if path != "/404.html": pages.append((path, prio)); PTITLES[path] = title; PDESC[path] = desc

# ---------------- data.js for the finder ----------------
DATAJS = "window.BR=" + json.dumps({"domain":DOMAIN,"wa":WA,"hours":"Walk-in "+HOURS_WALK,
  "bolt":BOLT, "name":NAME, "areas":[[a,la,lo] for a,la,lo in AREAS], "areaTxt":AREA_TXT, "price":{k:[P[k][0],P[k][1]] for k in P},
  "fit":[[r[0],r[1],r[2],r[3],r[4]]+([r[6]] if r[6] else []) for r in rows], "eqn":EQN,
  "out":[{"name":f"Motoserv @ {n}","slug":slug(n),"addr":f"{a} ({STATION[s]})","map":f"Motoserv {n} {a}","lat":la,"lng":lo} for n,s,a,la,lo in OUTLETS]},
  ensure_ascii=False, separators=(",",":")) + ";"

def size_link(k): return f'<a href="/battery/{slug(k)}/">{esc(NAME[k])}</a>'
def price_rows(keys):
    return "".join(f'<tr><td class="s">{size_link(k)}</td><td class="num">{m(walk(k))}</td><td class="num">{md((k))}</td><td class="num">{m(night(k))}</td></tr>' for k in keys)
PRICE_HEAD = '<tr><th>Delkor battery</th><th class="num">Walk-in*</th><th class="num">Fitted at you<br><small class="plbl">Launch promo</small></th><th class="num">Night/PH</th></tr>'
DISCLAIMER = "If our technician comes to you and finds the problem is not battery-related, an onsite service fee of $50 to $80 applies. Final charges depend on location and service requirements."
EXTRA = [  # client message via Edwin, 26 Oct 2026
 {"slug":"jump-start","name":"Jump-start service","short":"Jump-start","price":"$50","sub":"$80 on public holidays","from":50,
  "lead":"Battery flat but still good? We come to your car and jump-start it.","wa":"Hi Battery Rescue, I need a jump-start."},
 {"slug":"towing","name":"Emergency towing","short":"Towing","price":"From $80","sub":"King dolly (4 wheels off the ground) from $120","from":80,
  "lead":"Car can't be driven? We arrange a tow truck to move it.","wa":"Hi Battery Rescue, I need a tow truck."},
]
def wa_url(text): return f"https://wa.me/{WA}?text=" + __import__("urllib.parse").parse.quote(text)
def svc_cards(ref):
    out = '<div class="card"><b>Not the battery? Other help</b>'
    for e in EXTRA:
        out += (f'<div class="tier day" style="margin-top:10px"><div><div class="n"><a href="/services/{e["slug"]}/" style="color:inherit">{esc(e["name"])}</a></div><div class="d">{esc(e["sub"])}</div></div><div class="p">{esc(e["price"])}</div></div>'
                f'<a class="btn o" style="width:100%;margin-top:6px" href="{wa_url(e["wa"]+" (Website source: batteryrescue.sg)")}" data-ref="{e["slug"]}">{I["wa"]} WhatsApp for {esc(e["short"].lower())}</a>')
    return out + f'<p class="note"><b>Please note:</b> {DISCLAIMER}</p></div>'
PRICE_NOTE = f'<p class="note">*Walk-in price at any Motoserv outlet with the $20 website code (list price minus $20, {HOURS_WALK}). "Fitted at you" = list price + $30 (launch promo, normally + $50), before 10pm including Sunday. Night/PH = list price + $80, 10pm to 9am and public holidays. Battery, fitting and GST included. Prices checked {CHECKED}.</p>'

# ================= HOME (the app) =================
TOP = ["NS40ZL","NS60L","85D23L","100D26L","DIN45L","EFB-Q85L"]
home_faq = [
 ("How much is a car battery replacement in Singapore?", f"At Battery Rescue SG a Delkor NS40ZL (most small Japanese cars) is {m(walk('NS40ZL'))} walk-in at a Motoserv outlet with the website code, {md(('NS40ZL'))} fitted at your location before 10pm, and {m(night('NS40ZL'))} at night or on public holidays. Prices include the battery, fitting and GST."),
 ("Can you come to me if my car won't start?", f"Yes, islandwide, and fastest in the North and North-East ({AREA_TXT}). Call the 24-hour hotline {HOT} or WhatsApp us your location and car model. We bring the right Delkor battery and fit it where your car is."),
 ("Which battery brand do you fit?", 'Delkor, a Korean battery brand made by Clarios Delkor. Every battery comes with a 1-year warranty. <a href="/delkor/">More about Delkor</a>.'),
 ("Where can I walk in?", f'At any of 10 Motoserv outlets, {HOURS_WALK}. Get the $20 code on this page first. <a href="/outlets/">See all outlets</a>.'),
]
HERO_SIREN = '<svg class="siren" viewBox="0 0 48 48" aria-hidden="true"><g class="beam"><path d="M24 22 2 8v28z" fill="#fff" opacity=".35"/><path d="M24 22 46 8v28z" fill="#fff" opacity=".35"/></g><rect x="10" y="36" width="28" height="6" rx="2" fill="#fff"/><path d="M14 36v-9a10 10 0 0 1 20 0v9z" fill="#ffd34d"/><path d="M19 27a5 5 0 0 1 5-5" stroke="#fff" stroke-width="2.5" stroke-linecap="round" fill="none"/></svg>'
HERO_TICK = '<svg class="tick" viewBox="0 0 48 48" aria-hidden="true"><circle cx="24" cy="24" r="20" fill="#1faa53"/><path d="m15 24.5 6.5 6.5L34 18" stroke="#fff" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>'
# Homepage hero redesign, approved by Edwin 6 Nov 2026 ("This is good"): two choice cards, trust strip, WhatsApp first.
home = f"""<div id="app">
<section data-panel="stuck" class="stk">
 <div class="hero"><h1 class="h1"><span class="kick">Onsite car battery replacement · Singapore</span>What's happening with your car?</h1>
 <div class="pick">
  <a class="pk red" href="#help" data-ref="hero-stuck">{HERO_SIREN}<b>My car won't start</b><span>We come to you, 24 hours ›</span></a>
  <a class="pk grn" href="/#compare" data-ref="hero-compare">{HERO_TICK}<b>My car can start</b><span>See prices &amp; outlets ›</span></a>
 </div>
 <div class="trio"><div>{I["tag"]}<b>Fixed prices</b><span>No kena chop</span></div><div>{I["pin"]}<b>Send location</b><span>Get ETA</span></div><div>{I["shield"]}<b>By Motoserv</b><span>Outlets + warranty</span></div></div>
 <p class="where">📍 <b>Islandwide</b> · Fastest in the North &amp; North-East · From {md(('NS40ZL'))} fitted <a href="#car-price" data-ref="hero-price">Check my car price ›</a><br><span class="plbl">{PROMO_LBL}</span></p>
 <div id="help">
 <a class="big w wa-dyn wa-loc" href="https://wa.me/{WA}" data-ref="stuck">{I["wa"]}<span class="t">WhatsApp + send my location<small>We get your car's exact spot</small></span></a>
 <a class="big cl" href="tel:{TEL}" data-ref="stuck">{I["phone"]}<span class="t">Call {HOT}<small>Open 24 hours</small></span></a>
 </div>
 <div class="enq" id="s-out" hidden></div>
 <p class="note" style="margin-top:12px;text-align:center"><a href="{GBP}" target="_blank" rel="noopener" data-ref="gbp-home" style="color:inherit;text-decoration:none"><span style="color:#f5a400">★★★★★</span> <b>5-star rating on Google</b> · <u>See our reviews</u></a></p></div>
 <div class="card" id="car-price"><label class="l" for="s-in">Optional: your car, for the price</label>
 <div class="field carbox" id="s-car"><input id="s-in" type="search" placeholder="e.g. Honda Vezel, Altis" autocomplete="off" enterkeyhint="search"><button class="x" type="button" aria-label="Clear">×</button><ul class="sug"></ul></div>
 <div class="res" id="s-res" aria-live="polite"></div>
 <p class="note">Fitted at your location: battery price + $30 (launch promo, normally + $50) before 10pm (incl. Sunday), + $80 from 10pm to 9am and on public holidays.</p></div>
 {svc_cards("home")}
</section>
<section data-panel="compare" hidden>
 <div class="cmp"><div>
 <a class="back" href="/">‹ Car won't start? Get help</a>
 <div class="card"><h2 class="h1" style="font-size:22px">Your car's battery and price</h2><p class="sub">Type your car. See the Delkor battery and all 3 prices.</p>
 <label class="l" for="c-in">Your car</label>
 <div class="field carbox" id="c-car"><input id="c-in" type="search" placeholder="e.g. Toyota Corolla Altis 2015" autocomplete="off" enterkeyhint="search"><button class="x" type="button" aria-label="Clear">×</button><ul class="sug"></ul></div>
 <div class="res" id="c-res" aria-live="polite"></div></div>
 <div class="card"><b>Save $20 at a Motoserv outlet</b><p class="sub">Pick an outlet below, tap "Get $20 code" and show it at the counter. Walk-in only, {HOURS_WALK}.</p></div>
 </div><div>
 <div class="card"><b>10 Motoserv outlets</b>
 <div class="near"><button class="btn o" id="c-gps" type="button">{I["pin"]} Nearest to me</button></div>
 <form class="near" id="c-pc"><input inputmode="numeric" maxlength="6" placeholder="or postal code" aria-label="Postal code"><button class="btn o" style="flex:none;padding:0 16px">Sort</button></form>
 <ul class="olist" id="c-out"></ul></div></div></div>
</section>
</div>
<section class="sec rv"><h2>Delkor battery prices at a glance</h2>
<div class="tblw"><table class="tbl">{PRICE_HEAD}{price_rows(TOP)}</table></div>{PRICE_NOTE}<p><a href="/prices/">All 23 Delkor batteries and prices →</a></p></section>
<section class="sec rv"><h2>Find your car brand</h2><div class="grid">{"".join(f'<a class="tile" href="/car-battery/{slug(mk)}/"><span class="dot">{esc(mk[:2])}</span><span>{esc(mk)}<small>{len(MAKES[mk])} models</small></span></a>' for mk in BRAND_PAGES[:12])}</div>
<p><a href="/car-battery/">All car brands →</a></p></section>
<section class="sec rv"><h2>How it works</h2><ol><li><b>Call or WhatsApp</b> with your car model and location.</li><li><b>We bring the matching Delkor battery</b> and fit it where your car is, or you walk in to a Motoserv outlet.</li><li><b>Pay the price you saw here.</b> GST included, 1-year warranty, old battery taken away.</li></ol>
<div class="trust">{I["shield"]}<div><b>Why Delkor?</b><br>Korean-made by Clarios Delkor. Every battery we fit is Delkor, with a 1-year warranty. <a href="/delkor/">About Delkor and its quality award</a></div></div></section>
<section class="sec rv"><h2>Questions</h2>{faq_html(home_faq)}</section>
<section class="sec rv areas"><h2>Fastest response areas</h2><p>We cover all of Singapore. Our fastest response is in the North and North-East: {", ".join(f'<a href="/rescue/{slug(a)}/">{esc(a)}</a>' for a,_,_ in AREAS)}.</p></section>"""
page("/", "Onsite Car Battery Replacement Singapore | Battery Rescue SG",
     f"Car won't start? Delkor battery fitted at your location, 24-hour hotline {HOT}, or walk in to 10 Motoserv outlets with $20 off.",
     home, [faq_ld(home_faq)], "Rescue", prio="1.0", lean=True)

# ================= PRICES =================
allk = [k for k, *_ in PRICES]
groups = [("Standard batteries (most Japanese and Korean cars)",[k for k in allk if TYPE[k]=="Standard"]),("DIN batteries (most European cars)",[k for k in allk if TYPE[k]=="Standard (DIN)"]),
          ("Start-stop batteries (EFB)",[k for k in allk if TYPE[k] in ("EFB start-stop","Start-stop (Japanese)")]),("AGM batteries (premium and start-stop cars)",[k for k in allk if TYPE[k]=="AGM"])]
svc_tbl = '<section class="sec"><h2>Other onsite services</h2><div class="tblw"><table class="tbl"><tr><th>Service</th><th class="num">Price</th><th></th></tr>' + "".join(
    f'<tr><td><a href="/services/{e["slug"]}/">{esc(e["name"])}</a><br><small>{esc(e["sub"])}</small></td><td class="num"><b>{esc(e["price"])}</b></td><td><a href="{wa_url(e["wa"])}" data-ref="prices-{e["slug"]}">WhatsApp</a></td></tr>' for e in EXTRA) + f'</table></div><p class="note"><b>Please note:</b> {DISCLAIMER}</p></section>'
pbody = f"""<h1 class="h1" style="margin-top:8px">Delkor car battery prices in Singapore</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>Delkor car batteries cost from {m(walk('NS40ZL'))} (NS40ZL, walk-in with the $20 website code) to {m(night('AGM-LN5'))} (AGM LN5 fitted at night). Fitted at your location adds $30 to the list price before 10pm (launch promo, normally $50), or $80 from 10pm to 9am and on public holidays. GST and fitting included, 1-year warranty.</div>
""" + "".join(f'<section class="sec"><h2>{esc(g)}</h2><div class="tblw"><table class="tbl">{PRICE_HEAD}{price_rows(ks)}</table></div></section>' for g, ks in groups) + PRICE_NOTE + svc_tbl + \
 '<section class="sec"><h2>Next step</h2><ul class="menu"><li><a href="/rescue/">Onsite battery replacement at your location</a></li><li><a href="/walk-in/">Walk-in at a Motoserv outlet with $20 off</a></li><li><a href="/car-battery/">Find the battery for your car brand</a></li><li><a href="/#compare">Use the finder</a></li></ul></section>' + \
 f'<section class="sec"><h2>List prices</h2><p>The Delkor list price is the price at the Motoserv counter without the website code: ' + ", ".join(f"{NAME[k]} {m(P[k][1])}" for k in allk) + ".</p></section>"
offers_ld = {"@type":"ItemList","name":"Delkor car battery prices","itemListElement":[{"@type":"ListItem","position":i+1,"url":f"{BASE}/battery/{slug(k)}/","name":f"Delkor {NAME[k]}"} for i,k in enumerate(allk)]}
page("/prices/", "Car Battery Price Singapore: Delkor List | Battery Rescue",
     f"Car battery prices in Singapore: Delkor walk-in from {m(walk('NS40ZL'))}, fitted at you +$30 (launch promo), night and PH +$80. 23 sizes, GST incl., 1-year warranty.",
     pbody, [offers_ld], "Prices", [("Home","/"),("Prices","/prices/")], "0.9")

# ================= OUTLETS =================
ob = f"""<h1 class="h1" style="margin-top:8px">Motoserv outlets for battery replacement</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>Walk in to any of 10 Motoserv outlets, {HOURS_WALK}, for a Delkor battery at the list price minus $20 with the website code. Example: NS40ZL {m(walk('NS40ZL'))} instead of {m(P['NS40ZL'][1])}.</div>
<p><a class="big y" href="/#compare">{I["tag"]}<span class="t">Get my battery price + $20 code</span></a></p>
<ul class="olist">""" + "".join(f'<li><b>Motoserv @ {esc(n)}</b><div class="ad">{esc(a)} ({STATION[s]})</div><div class="ad">Walk-in {HOURS_WALK}</div><div class="row"><a class="btn o" href="https://www.google.com/maps/search/?api=1&amp;query={esc(html.escape("Motoserv "+n+" "+a))}" target="_blank" rel="noopener">Open in Maps</a></div></li>' for n,s,a,la,lo in OUTLETS) + \
 f'</ul><p class="note">Sundays and late nights: call {HOT} and we fit the battery at your location instead.</p><div class="pending">CONFIRM with Motoserv: Sunday/PH opening, postal codes for 6 outlets, Google Maps profile per outlet.</div>'
outlet_ld = [{"@type":"AutoRepair","name":f"Motoserv @ {n}","address":{"@type":"PostalAddress","streetAddress":a.split(", Singapore")[0],"addressLocality":"Singapore","addressCountry":"SG"},
  "geo":{"@type":"GeoCoordinates","latitude":la,"longitude":lo},"parentOrganization":{"@id":BASE+"/#org"},
  "openingHoursSpecification":{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"09:00","closes":"18:00"}} for n,s,a,la,lo in OUTLETS]
page("/outlets/", "10 Motoserv Outlets for Car Batteries | Battery Rescue SG",
     f"Walk in to 10 Motoserv outlets ({HOURS_WALK}) for a Delkor battery with $20 off: Bukit Batok, Toa Payoh, Serangoon Garden, Upper Thomson and more.",
     ob, outlet_ld, "Outlets", [("Home","/"),("Outlets","/outlets/")], "0.8")

# ================= BATTERY SIZE PAGES =================
for k, aka, ah, lp, t in PRICES:
    cars = BY_SIZE.get(k, [])
    mk_count = {}
    for r in cars: mk_count[r[0]] = mk_count.get(r[0], 0) + 1
    popular = ", ".join(f"{mk}" for mk, _ in sorted(mk_count.items(), key=lambda x: -x[1])[:6])
    sample = [r for r in cars if r[5] in ("sg", "edwin")][:40] or cars[:40]
    ctable = ("<div class='tblw'><table class='tbl'><tr><th>Car</th><th>Years</th></tr>" + "".join(f"<tr><td>{esc(r[0])} {esc(r[1])}{'<br><small>Replaces '+esc(r[3])+' (same size)</small>' if r[6] else ''}</td><td>{esc(r[2])}</td></tr>" for r in sample) + "</table></div>") if sample else "<p>Call us to check if this size fits your car.</p>"
    nm = NAME[k]
    body = f"""<h1 class="h1" style="margin-top:8px">Delkor {esc(nm)} battery price in Singapore</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>The Delkor {esc(nm)}{f" ({esc(aka)})" if aka else ""} is a {ah}Ah {esc(t.lower())} battery. Price: {m(walk(k))} walk-in at Motoserv with the $20 web code, {md((k))} fitted at your location before 10pm, {m(night(k))} at night or on public holidays. List price {m(lp)}. GST included, 1-year warranty.</div>
<div class="tiers"><div class="tier walk"><div><div class="n">Walk-in at Motoserv</div><div class="d">$20 web code · {HOURS_WALK}</div></div><div class="p">{m(walk(k))}<s>{m(lp)}</s></div></div>
<div class="tier day"><div><div class="n">Fitted at your location</div><div class="d promo">{PROMO_LBL}</div></div><div class="p">{md((k))}</div></div>
<div class="tier night"><div><div class="n">Night & public holiday</div><div class="d">10pm to 9am, and PH</div></div><div class="p">{m(night(k))}</div></div></div>
<section class="sec"><h2>Which cars use the {esc(nm)}?</h2><p>{f"Mostly {esc(popular)}. " if popular else ""}{len(cars)} models in our list match this size{" (first 40 shown)" if len(cars) > 40 else ""}. Always check against your current battery; we confirm before fitting.</p>{ctable}
<p><a class="big y" href="/#compare">{I["tag"]}<span class="t">Check my exact car</span></a></p></section>"""
    prod = {"@type":"Product","name":f"Delkor {nm} car battery","brand":{"@type":"Brand","name":"Delkor"},"sku":k,"image":BASE+"/og.jpg",
            "description":f"Delkor {nm} {ah}Ah {t.lower()} car battery, fitted in Singapore with a 1-year warranty.",
            "offers":[{"@type":"Offer","name":"Walk-in at Motoserv with website code","price":f"{walk(k):.2f}","priceCurrency":"SGD","availability":"https://schema.org/InStock","url":f"{BASE}/battery/{slug(k)}/","seller":{"@id":BASE+"/#org"}},
                      {"@type":"Offer","name":"Fitted at your location (before 10pm)","price":f"{day(k):.2f}","priceCurrency":"SGD","availability":"https://schema.org/InStock","url":f"{BASE}/battery/{slug(k)}/","seller":{"@id":BASE+"/#org"}}]}
    page(f"/battery/{slug(k)}/", f"Delkor {nm} Battery Price Singapore: {m(walk(k))} | Battery Rescue SG",
         f"Delkor {nm} ({ah}Ah) price in Singapore: {m(walk(k))} walk-in, {md((k))} fitted at your location, {m(night(k))} night/PH. Which cars use it.",
         body, [prod], "Prices", [("Home","/"),("Prices","/prices/"),(f"Delkor {nm}",f"/battery/{slug(k)}/")], "0.7")

# ================= CAR BRAND PAGES =================
def brand_table(rr):
    out = "<div class='tblw'><table class='tbl'><tr><th>Model</th><th>Years</th><th>Battery</th><th class='num'>Walk-in*</th><th class='num'>At you<br><small class='plbl'>Launch promo</small></th></tr>"
    for r in rr:
        if r[4]: out += f"<tr><td>{esc(r[1])}</td><td>{esc(r[2])}</td><td class='s'>{size_link(r[4])}{'<br><small>'+esc(EQN[r[6]])+'</small>' if r[6] else ''}</td><td class='num'>{m(walk(r[4]))}</td><td class='num'>{md((r[4]))}</td></tr>"
        else: out += f"<tr><td>{esc(r[1])}</td><td>{esc(r[2])}</td><td class='s'>{esc(r[3])}</td><td class='num' colspan='2'><a href='https://wa.me/{WA}?text={html.escape(__import__('urllib.parse').parse.quote('Hi Battery Rescue, price for '+r[0]+' '+r[1]+' ('+r[2]+'), battery '+r[3]+'?'))}'>Ask</a></td></tr>"
    return out + "</table></div>"
idx_tiles = ""
for mk in BRAND_PAGES:
    rr = MAKES[mk]; ks = {}
    for r in rr:
        if r[4]: ks[r[4]] = ks.get(r[4], 0) + 1
    common = sorted(ks.items(), key=lambda x: -x[1])[:3]
    cheapest = min((walk(k) for k in ks), default=None)
    ans = (f"Most {esc(mk)} cars in our list use a Delkor " + ", ".join(f"{NAME[k]}" for k,_ in common) + ". " if common else "") + \
          (f"Prices start at {m(cheapest)} walk-in at a Motoserv outlet with the $20 website code; fitted at your location is the list price + $30 (launch promo, normally + $50) before 10pm, + $80 at night and on public holidays. GST included." if cheapest else "Call us for the price of your model.")
    body = f"""<h1 class="h1" style="margin-top:8px">{esc(mk)} car battery: size and price in Singapore</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>{ans}</div>
<p><a class="big y" href="/#compare">{I["tag"]}<span class="t">Find my exact {esc(mk)}</span></a></p>
<section class="sec"><h2>Which battery fits my {esc(mk)}?</h2>{brand_table(rr)}{PRICE_NOTE}<p class="note">Fitment from battery makers' application lists. Some cars have more than one option; we check your current battery before fitting. "Ask" means we confirm stock and price on WhatsApp.</p></section>
<section class="sec"><h2>{esc(mk)} won't start?</h2><p>Call <a href="tel:{TEL}" data-ref="{slug(mk)}">{HOT}</a> (24 hours) or WhatsApp your location. We bring the matching Delkor battery to your car.</p></section>"""
    page(f"/car-battery/{slug(mk)}/", f"{mk} Car Battery Price Singapore | Size by Model | Battery Rescue SG",
         f"{mk} car battery sizes by model and year, with Delkor prices: walk-in, fitted at your location and night rates. 24-hour hotline {HOT}.",
         body, [], "Prices", [("Home","/"),("Car brands","/car-battery/"),(mk,f"/car-battery/{slug(mk)}/")], "0.7")
    idx_tiles += f'<a class="tile" href="/car-battery/{slug(mk)}/"><span class="dot">{esc(mk[:2])}</span><span>{esc(mk)}<small>{len(rr)} models</small></span></a>'
others = sorted(set(MAKES) - set(BRAND_PAGES))
brand_faq = [
 ("How do I find the right battery for my car?", f"Open your brand below, find your model and year, and read the Delkor size and price next to it. Or type your car into the finder on our home page. If your car is not listed, call or WhatsApp {HOT} with your model and year."),
 ("Where do these battery sizes come from?", "From the Bateriku/Astra 2023 chart (Asian makes) and the Nam Wah 2024 application guide (other makes), matched to the Delkor sizes we sell. They are reference data, so we confirm the size with you before fitting. We sell Delkor batteries only."),
 ("What does it cost to have the battery fitted?", f"The Delkor list price + $30 (launch promo, normally + $50) at your location before 10pm (including Sunday), or + $80 from 10pm to 9am and on public holidays. Walk in to a Motoserv outlet with our website code ({HOURS_WALK}) and you pay the list price minus $20."),
]
page("/car-battery/", "Car Battery by Car Brand | Battery Rescue SG", "Find the Delkor battery size and price for your car brand and model: Toyota, Honda, Nissan, Mazda, Mercedes-Benz, BMW and more.",
     f'<h1 class="h1" style="margin-top:8px">Car battery by brand</h1><section class="sec"><p>Pick your car brand to see the Delkor battery that fits each model and year, with three prices: walk-in at a Motoserv outlet with the $20 website code, fitted at your location before 10pm, and the night and public holiday rate. The lists cover {len(BRAND_PAGES)} brands and {len(rows):,} model entries, including the Japanese and Korean cars most common in Singapore. Every battery we fit is a Delkor with a 1-year warranty, and all prices include GST. Start-stop cars are matched to the EFB or AGM size they need. If your car is not listed, or the size shows as an enquiry, call or WhatsApp us on {CALLX} and we will confirm the right battery with you.</p></section>'
     f'<div class="grid" style="margin-top:12px">{idx_tiles}</div>'
     + (f'<p class="note">Also in the finder: {esc(", ".join(others))}.</p>' if others else "") + f'<section class="sec"><h2>Questions</h2>{faq_html(brand_faq)}</section>', [faq_ld(brand_faq)], "Prices", [("Home","/"),("Car brands","/car-battery/")], "0.7")

# ================= SERVICE + TRUST PAGES =================
rescue_faq = [
 ("How much does it cost to replace a flat battery at my location?", f"The Delkor battery list price + $30 (launch promo, normally + $50) before 10pm (including Sunday), or + $80 from 10pm to 9am and on public holidays. Example: NS40ZL {md(('NS40ZL'))} by day, {m(night('NS40ZL'))} at night. Fitting and GST included."),
 ("Is the hotline open 24 hours?", f"Yes, {HOT} answers 24 hours."),
 ("What should I send on WhatsApp?", "Your car model and year, your location (the button on our home page attaches it), and a photo of the battery label if you can."),
 ("Do you take away the old battery?", "Yes, we take the old battery away when we fit the new one."),
]
page("/rescue/", "Onsite Car Battery Replacement Singapore | 24h Hotline | Battery Rescue SG",
     f"Car battery flat? We bring a Delkor battery and fit it where you are. Battery price + $30 before 10pm (launch promo), + $80 night/PH. 24-hour hotline {HOT}.",
     f"""<h1 class="h1" style="margin-top:8px">Onsite car battery replacement in Singapore</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>We cover {COVER_TXT}. Call {HOT} (24 hours) or WhatsApp your location. We bring a Delkor battery that fits your car and replace it on the spot. You pay the battery list price + $30 (launch promo, normally + $50) before 10pm, or + $80 from 10pm to 9am and on public holidays. 1-year warranty.</div>
<a class="big c" href="tel:{TEL}" data-ref="rescue">{I["phone"]}<span class="t">Call {HOT}</span></a><a class="big w wa-dyn wa-loc" href="https://wa.me/{WA}" data-ref="rescue">{I["wa"]}<span class="t">WhatsApp + send my location</span></a>
<section class="sec"><h2>Where we come to</h2><div class="grid">{"".join(f'<a class="tile" href="/rescue/{slug(a)}/"><span>{esc(a)}<small>Battery rescue</small></span></a>' for a,_,_ in AREAS)}</div><p class="note">These are our fastest response areas. We come to you anywhere in Singapore, or you can walk in to any of the 10 <a href="/outlets/">Motoserv outlets</a>.</p></section>
<section class="sec"><h2>Jump-start and towing</h2>{svc_cards("rescue")}</section>
<section class="sec"><h2>Signs it is the battery</h2><ul><li>Clicking or a slow crank when you turn the key or press start.</li><li>Dashboard lights dim or flicker.</li><li>The car was parked for many days, or lights were left on.</li></ul><p>If the engine cranks normally but won't start, it may not be the battery. Tell us what you hear and we will advise before coming down.</p></section>
<section class="sec"><h2>Prices for popular batteries</h2><div class="tblw"><table class="tbl">{PRICE_HEAD}{price_rows(TOP)}</table></div>{PRICE_NOTE}</section>
<section class="sec"><h2>Questions</h2>{faq_html(rescue_faq)}</section>""",
     [faq_ld(rescue_faq),{"@type":"Service","name":"Car battery replacement at your location","serviceType":"Mobile car battery replacement","provider":{"@id":BASE+"/#org"},"areaServed":[{"@type":"Country","name":"Singapore"}]+[{"@type":"Place","name":a+", Singapore"} for a,_,_ in AREAS],
      "offers":{"@type":"AggregateOffer","priceCurrency":"SGD","lowPrice":f"{day('NS40ZL'):.2f}","highPrice":f"{night('AGM-LN5'):.2f}"}}],
     "Rescue", [("Home","/"),("Battery rescue","/rescue/")], "0.9")

for e in EXTRA:
    jfaq = [(f"How much is {e['name'].lower()} in Singapore?", f"{e['price']}. {e['sub']}. Final charges depend on location and service requirements. GST included."),
            ("What if the problem is not the battery?", DISCLAIMER),
            ("Which areas do you cover?", f"All of Singapore. Our fastest response is in {AREA_TXT}. Call {HOT} for an ETA.")]
    page(f"/services/{e['slug']}/", f"{e['name']} Singapore: {e['price']} | Battery Rescue SG",
         f"{e['name']} in Singapore by Battery Rescue SG (Motoserv): {e['price']}. {e['sub']}. 24-hour hotline {HOT}.",
         f"""<h1 class="h1" style="margin-top:8px">{esc(e['name'])} in Singapore</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>{esc(e['lead'])} Price: <b>{esc(e['price'])}</b> ({esc(e['sub'])}). Final charges depend on location and service requirements. Call {HOT} (24 hours) or WhatsApp us.</div>
<a class="big w" href="{wa_url(e['wa']+' (Website source: batteryrescue.sg/services/'+e['slug']+'/)')}" data-ref="{e['slug']}">{I["wa"]}<span class="t">WhatsApp for {esc(e['short'].lower())}</span></a>
<a class="big c" href="tel:{TEL}" data-ref="{e['slug']}">{I["phone"]}<span class="t">Call {HOT}</span></a>
<div class="enq" style="margin-top:14px"><b>Please note:</b> {DISCLAIMER}</div>
<section class="sec"><h2>Battery needs replacing?</h2><p>Our main service is onsite car battery replacement with a Delkor battery: from {md(('NS40ZL'))} fitted where your car is. <a href="/rescue/">Onsite battery replacement</a> · <a href="/#compare">Find my battery and price</a></p></section>
<section class="sec"><h2>Questions</h2>{faq_html(jfaq)}</section>""",
         [faq_ld(jfaq), {"@type":"Service","name":e["name"],"provider":{"@id":BASE+"/#org"},"areaServed":[{"@type":"Country","name":"Singapore"}]+[{"@type":"Place","name":a+", Singapore"} for a,_,_ in AREAS],
           "offers":{"@type":"Offer","priceCurrency":"SGD","price":f"{e['from']:.2f}","description":e["sub"]}}],
         "Rescue", [("Home","/"),("Onsite battery replacement","/rescue/"),(e["name"],f"/services/{e['slug']}/")], "0.6")
for a, la, lo in AREAS:
    near = sorted(OUTLETS, key=lambda o: dist((la,lo),(o[3],o[4])))[:2]
    afaq = [(f"How fast can you reach me in {a}?", f"Call {HOT} and tell us where your car is; we give you an arrival time on the call."),
            (f"How much is a car battery replacement in {a}?", f"Fitted where your car is in {a}: the Delkor list price + $30 (launch promo, normally + $50) before 10pm (incl. Sunday), + $80 from 10pm to 9am and on public holidays. Example: NS40ZL {md(('NS40ZL'))}, NS60L {md(('NS60L'))}. GST included."),
            (f"Is there a Motoserv outlet near {a}?", "The nearest are " + " and ".join(f"Motoserv @ {o[0]} ({o[2]}, about {dist((la,lo),(o[3],o[4])):.0f} km)" for o in near) + f". Walk in {HOURS_WALK} for $20 off with our code.")]
    page(f"/rescue/{slug(a)}/", f"Car Battery Replacement {a}: We Come to You | Battery Rescue SG",
         f"Car won't start in {a}? We bring a Delkor battery and fit it where your car is. From {md(('NS40ZL'))} fitted, 24-hour hotline {HOT}.",
         f"""<h1 class="h1" style="margin-top:8px">Car battery replacement in {esc(a)}</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>Battery flat in {esc(a)}? Call {HOT} (24 hours) or WhatsApp your location. We bring a Delkor battery and fit it where your car is: from {md(('NS40ZL'))} before 10pm, {m(night('NS40ZL'))} at night or on public holidays (NS40ZL), GST included, 1-year warranty.</div>
<a class="big c" href="tel:{TEL}" data-ref="{slug(a)}">{I["phone"]}<span class="t">Call {HOT}</span></a><a class="big w wa-dyn wa-loc" href="https://wa.me/{WA}" data-ref="{slug(a)}">{I["wa"]}<span class="t">WhatsApp + send my location</span></a>
<section class="sec"><h2>Prices in {esc(a)}</h2><div class="tblw"><table class="tbl">{PRICE_HEAD}{price_rows(TOP)}</table></div>{PRICE_NOTE}<p><a href="/#compare">Find the price for your exact car →</a></p></section>
<section class="sec"><h2>Questions from {esc(a)} drivers</h2>{faq_html(afaq)}</section>
<p class="note">Also covered: {esc(", ".join(x for x,_,_ in AREAS if x != a))}.</p>""",
         [faq_ld(afaq)], "Rescue", [("Home","/"),("Battery rescue","/rescue/"),(a,f"/rescue/{slug(a)}/")], "0.7")
page("/walk-in/", "Walk-in Car Battery Replacement: $20 Off | Battery Rescue SG",
     f"Walk in to any of 10 Motoserv outlets ({HOURS_WALK}) and pay the Delkor list price minus $20 with the code from this website.",
     f"""<h1 class="h1" style="margin-top:8px">Walk-in battery replacement with $20 off</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>Find your car on our finder, tap "Get $20 code" at the outlet you want, and show the code at the counter. You pay the Delkor list price minus $20, fitted, GST included. Walk-in only, {HOURS_WALK}, at 10 Motoserv outlets.</div>
<p><a class="big y" href="/#compare">{I["tag"]}<span class="t">Find my price and get the code</span></a></p>
<section class="sec"><h2>Walk-in prices</h2><div class="tblw"><table class="tbl"><tr><th>Delkor battery</th><th class="num">List</th><th class="num">With code</th></tr>{"".join(f'<tr><td class="s">{size_link(k)}</td><td class="num">{m(P[k][1])}</td><td class="num"><b>{m(walk(k))}</b></td></tr>' for k in allk)}</table></div>
<p class="note">The $20 code is for walk-in at a Motoserv outlet only. It does not apply to batteries fitted at your location.</p></section>
<p><a href="/outlets/">See all 10 outlets →</a></p>""",
     [{"@type":"Service","name":"Walk-in car battery replacement","provider":{"@id":BASE+"/#org"},"areaServed":"Singapore","offers":{"@type":"AggregateOffer","priceCurrency":"SGD","lowPrice":f"{walk('NS40ZL'):.2f}","highPrice":f"{walk('AGM-LN5'):.2f}"}}],
     "Outlets", [("Home","/"),("Walk-in","/walk-in/")], "0.8")

page("/delkor/", "Delkor Car Batteries: Who Makes Them | Battery Rescue SG",
     "Every battery we fit is a Delkor: Korean-made by Clarios Delkor, a Korean Standards Association quality award winner for 16 years to 2021. 1-year warranty.",
     f"""<h1 class="h1" style="margin-top:8px">Why we fit Delkor batteries</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>Every battery Battery Rescue SG fits is a Delkor. Delkor is a Korean battery brand made by Clarios Delkor Corporation (formerly Johnson Controls Delkor Battery Corporation). It has won the Korean Standards Association's Quality Excellence award for car batteries every year since 2006, the 16th straight year in 2021. We give a 1-year warranty on every battery.</div>
<section class="sec"><h2>Facts about Delkor</h2><ul>
<li>Maker: Clarios Delkor Corporation, Korea (formerly Johnson Controls Delkor Battery Corporation).</li>
<li>Award: Korean Standard Quality Excellence Index (KS-QEI), top car battery, from the Korean Standards Association, 16 consecutive years as of November 2021 (<a href="https://www.rjbatt.com.au/news-and-advice/delkor-batteries-win-16th-consecutive-award-for-quality-excellence" rel="noopener" target="_blank">source</a>).</li>
<li>History: described as the first automotive battery maker in Korea to supply maintenance-free (MF) batteries (<a href="https://www.mining-technology.com/contractors/data//pressreleases/delkor-wins-korean-standard-quality-excellence-for-13th-straight-year/" rel="noopener" target="_blank">source</a>).</li>
<li>Range we stock: 23 sizes, from the NS40ZL for small cars to EFB and AGM batteries for start-stop and European cars. <a href="/prices/">See prices</a>.</li></ul>
<div class="pending">CONFIRM with supplier Ktech: official Delkor website link for Singapore, and any Singapore distributor warranty terms to show here.</div></section>
<section class="sec"><h2>Our warranty</h2><p>1 year on every Delkor battery we fit, whether at your location or at a Motoserv outlet. Keep your receipt.</p></section>""",
     [{"@type":"Brand","name":"Delkor","description":"Korean car battery brand made by Clarios Delkor Corporation."}], "More", [("Home","/"),("Why Delkor","/delkor/")], "0.7")

page("/about/", "About Battery Rescue SG by Motoserv", "Battery Rescue SG is the car battery service of Motoserv, a CaseTrust-accredited group with 10 neighbourhood car service centres in Singapore.",
     f"""<h1 class="h1" style="margin-top:8px">About Battery Rescue SG</h1>
<div class="ans"><div class="k">QUICK ANSWER</div>Battery Rescue SG is the car battery service of Motoserv, a CaseTrust-accredited group of neighbourhood car service centres with 10 outlets in Singapore. We fit Delkor batteries at your location (24-hour hotline {HOT}) or at any Motoserv outlet.</div>
<section class="sec"><ul><li>Owner: Motoserv group (<a href="https://motoserv.sg/" rel="noopener">motoserv.sg</a>, <a href="https://www.facebook.com/motoserv.sg" rel="noopener">Facebook</a>, <a href="https://www.tiktok.com/@motoserv.sg" rel="noopener">TikTok</a>)</li>
<li>Accreditation: CaseTrust-accredited (Motoserv group)</li><li>Battery brand: Delkor, 1-year warranty</li><li>Hotline: <a href="tel:{TEL}" data-ref="about">{HOT}</a>, 24 hours</li><li>Google rating: <span style="color:#f5a400">★★★★★</span> 5 stars, <a href="{GBP}" target="_blank" rel="noopener">see our reviews on Google</a></li><li>Walk-in: 10 Motoserv outlets, {HOURS_WALK}</li></ul>
<div class="pending">CONFIRM: Motoserv legal entity name and UEN; CaseTrust certificate holder name as listed by CASE.</div></section>""",
     [], "More", [("Home","/"),("About","/about/")], "0.6")

# ---------------- articles ----------------
ARTS = [
 ("car-wont-start-what-to-do", "Car won't start in Singapore: what to do in the next 5 minutes",
  "Car won't start? Check these signs, stay safe, and know when it's the battery. What a battery rescue costs in Singapore.",
  f"""<p>Most no-start problems in a car park are a flat battery. Here is how to tell, and what to do.</p>
<h2>1. Listen when you turn the key or press start</h2><ul><li><b>Rapid clicking, or nothing at all:</b> almost always a weak or flat battery.</li><li><b>Slow, heavy cranking:</b> the battery is weak; it may start once and fail again.</li><li><b>Normal cranking but no start:</b> probably not the battery (fuel, ignition or a sensor). Tell us before we come down.</li></ul>
<h2>2. Stay safe</h2><p>If you are on a road, switch on the hazard lights and wait in a safe place. Don't try to jump-start a battery that is swollen, leaking or smells of rotten eggs.</p>
<h2>3. Get help</h2><p>Call <a href="tel:{TEL}" data-ref="art">{HOT}</a> (24 hours) or WhatsApp your location from our <a href="/">home page</a>. Tell us your car model so we bring the right Delkor battery.</p>
<h2>What does it cost?</h2><p>The battery list price + $30 (launch promo, normally + $50) before 10pm, + $80 from 10pm to 9am and on public holidays. A Delkor NS40ZL, which fits many small Japanese cars, is {md(('NS40ZL'))} by day. See <a href="/prices/">all prices</a>.</p>"""),
 ("efb-vs-agm-vs-standard-battery", "EFB vs AGM vs standard car battery: which does your car need?",
  "Start-stop cars need EFB or AGM batteries. How to tell which type your car uses, and Delkor prices for each in Singapore.",
  f"""<div class="ans"><div class="k">QUICK ANSWER</div>If your car has start-stop (the engine switches off at traffic lights), it needs the same type it came with: EFB or AGM. Cars without start-stop use a standard battery. Fitting a standard battery to a start-stop car shortens its life and can upset the car's charging system.</div>
<h2>Standard (flooded / maintenance-free)</h2><p>Most Japanese and Korean cars without start-stop. Delkor examples: <a href="/battery/ns40zl/">NS40ZL</a> {m(walk('NS40ZL'))} walk-in, <a href="/battery/ns60l/">NS60L</a> {m(walk('NS60L'))}.</p>
<h2>EFB (Enhanced Flooded Battery)</h2><p>Many start-stop Japanese cars and some European cars. Delkor examples: <a href="/battery/efb-q85l/">EFB Q85L</a> {m(walk('EFB-Q85L'))}, <a href="/battery/efb-s95/">EFB S95</a> {m(walk('EFB-S95'))} walk-in.</p>
<h2>AGM (Absorbent Glass Mat)</h2><p>Most European cars with start-stop and many premium models. One battery maker's guide says plainly for Audi and BMW: use only AGM where AGM was fitted from the factory. Delkor examples: <a href="/battery/agm-ln3/">AGM LN3</a> {m(walk('AGM-LN3'))}, <a href="/battery/agm-ln4/">AGM LN4</a> {m(walk('AGM-LN4'))} walk-in.</p>
<h2>How to check yours</h2><p>Look at the label on your current battery (it says EFB or AGM), or type your car into our <a href="/#compare">finder</a>.</p>"""),
 ("signs-car-battery-is-dying", "6 signs your car battery is dying (before it leaves you stranded)",
  "Slow starts, dim lights, a warning light: signs your car battery needs replacing, and what a Delkor replacement costs in Singapore.",
  f"""<p>A battery rarely dies without warning. Watch for these:</p><ol><li><b>Slow crank</b> on the first start of the day.</li><li><b>Dim headlights</b> at idle that brighten when you rev.</li><li><b>Battery or charging warning light</b> on the dashboard.</li><li><b>Start-stop stops working</b> (the car keeps the engine running at lights): many cars disable start-stop when the battery is weak.</li><li><b>White or green crust</b> on the terminals.</li><li><b>A swollen or leaking case</b>: replace it now and don't jump-start it.</li></ol>
<h2>Replace before it fails</h2><p>Walking in is the cheapest way: the Delkor list price minus $20 at any <a href="/outlets/">Motoserv outlet</a> with our web code. Example: NS60L {m(walk('NS60L'))}. Get your price in the <a href="/#compare">finder</a>.</p>"""),
 ("battery-or-alternator", "Battery or alternator? How to tell why your car won't start",
  "A new battery won't fix a bad alternator. The simple voltage check, the warning signs, and what happens if your problem isn't the battery.",
  f"""<div class="ans"><div class="k">QUICK ANSWER</div>The battery starts the car; the alternator recharges the battery while the engine runs. If a new or freshly charged battery keeps going flat, or the battery light stays on while driving, suspect the alternator. A battery at rest should read about 12.6V or more; with the engine running the charging voltage should rise to roughly 13.5 to 14.5V.</div>
<figure style="margin:14px 0"><img src="/photos/battery-voltage-12-80v.jpg" alt="Multimeter on a car battery showing 12.80 volts" width="800" height="1067" loading="lazy" style="width:100%;height:auto;border-radius:14px"><figcaption class="note">A multimeter on the battery reads 12.80V: a fully charged battery at rest. If the car still keeps dying, the charging side needs checking.</figcaption></figure>
<h2>Signs it is the alternator, not the battery</h2><ul><li>The battery or charging warning light stays on while you drive.</li><li>Lights dim and brighten with engine speed, or electrics act up while driving.</li><li>The car starts after a jump-start, then dies again within a day or so.</li><li>A whining or grinding noise from the front of the engine, where the drive belt turns the alternator.</li></ul>
<h2>The simple check</h2><ol><li>Engine off: battery voltage. About 12.6V or more is full; under about 12.4V it is low.</li><li>Engine running: the voltage should rise to roughly 13.5 to 14.5V. If it stays at battery level or falls, the alternator is not charging.</li></ol>
<figure style="margin:14px 0"><img src="/photos/old-alternator.jpg" alt="A worn alternator removed from a car" width="619" height="1100" loading="lazy" style="width:100%;height:auto;border-radius:14px"><figcaption class="note">A worn alternator after removal. When it stops charging, even a brand-new battery runs flat.</figcaption></figure>
<figure style="margin:14px 0"><img src="/photos/new-alternator-fitted.jpg" alt="A replacement alternator fitted in the engine bay, driven by the belt" width="619" height="1100" loading="lazy" style="width:100%;height:auto;border-radius:14px"><figcaption class="note">The replacement alternator fitted, turned by the engine's drive belt.</figcaption></figure>
<p class="note">Photos: an alternator job at SG Garage, used here to show the parts.</p>
<h2>What we do when we come to you</h2><p>Tell us your symptoms when you call or WhatsApp: it helps us bring the right help. If the battery is the problem, we fit a Delkor battery on the spot (<a href="/rescue/">onsite battery replacement</a>). If it's not, the car may need a workshop: we can <a href="/services/towing/">arrange a tow</a> (from $80) or <a href="/services/jump-start/">jump-start</a> you ($50) so you can drive there.</p>
<div class="enq"><b>Please note:</b> {DISCLAIMER}</div>"""),
 ("how-long-does-a-car-battery-last-singapore", "How long does a car battery last? Singapore",
  "A car battery typically lasts a few years, but heat and short trips shorten it. What to expect in Singapore and what a Delkor replacement costs.",
  f"""<div class="ans"><div class="k">QUICK ANSWER</div>A car battery typically lasts a few years, but there is no fixed number. In Singapore's heat, with lots of short trips and a car full of electronics, many batteries wear out sooner. Don't wait for a date: watch for slow starts, and replace it before it leaves you stranded. Every Delkor we fit has a 1-year warranty.</div>
<h2>Why Singapore can be hard on a battery</h2><ul><li><b>Heat:</b> constant high temperatures speed up the wear inside a battery. A car parked in the sun, or an engine bay that stays hot, does not help.</li><li><b>Short trips:</b> starting the engine takes a lot of power, and a short drive may not put it all back. Repeated short hops, like school runs and quick errands, can leave the battery under-charged.</li><li><b>Electrical load:</b> air-conditioning, a dashcam, screens and alarms all draw power, even when the car is parked.</li><li><b>Long parking:</b> a car left unused for weeks slowly drains its battery.</li></ul>
<h2>How to tell yours is near the end</h2><p>You don't need to know its age. A slow crank on the first start of the day, dim headlights at idle, or start-stop that stops working are the usual hints. Read our guide to the <a href="/articles/signs-car-battery-is-dying/">6 signs your car battery is dying</a>. If the car keeps going flat even after a new battery, the problem may be the charging side: see <a href="/articles/battery-or-alternator/">battery or alternator</a>.</p>
<h2>Ways to get more life from it</h2><ul><li>Take the car for a longer drive from time to time, so the alternator can recharge the battery.</li><li>Switch off lights and accessories before you turn the engine off.</li><li>Keep the terminals clean and tight.</li><li>If your car has start-stop, replace like with like: <a href="/articles/efb-vs-agm-vs-standard-battery/">EFB, AGM or standard</a>.</li></ul>
<h2>Replacing it before it fails</h2><p>Replacing on your own schedule is cheaper and calmer than a breakdown. Walk in to any <a href="/outlets/">Motoserv outlet</a> ({HOURS_WALK}) with our web code for $20 off the Delkor list price. Example: a Delkor <a href="/battery/ns40zl/">NS40ZL</a> is {m(walk('NS40ZL'))} walk-in, against a list price of {m(P['NS40ZL'][1])}.</p>
<h2>Already stuck?</h2><p>We fit the battery at your location: the list price + $30 (launch promo, normally + $50) before 10pm, or + $80 from 10pm to 9am and on public holidays. The same NS40ZL is {md(('NS40ZL'))} by day and {m(night('NS40ZL'))} at night. Call <a href="tel:{TEL}" data-ref="art">{HOT}</a> (24 hours) or see the <a href="/rescue/">rescue areas</a> and <a href="/prices/">all prices</a>. Not sure of your size? Use the <a href="/#compare">finder</a>.</p>
<div class="enq"><b>Please note:</b> {DISCLAIMER}</div>"""),

 ("car-battery-flat-every-morning", "Why does my car battery go flat overnight? Causes and what to do",
  "Car battery dead every morning? Common causes of an overnight drain in Singapore, a simple check, and when to replace the battery or look at the charging side.",
  f"""<div class="ans"><div class="k">QUICK ANSWER</div>A car battery that is flat every morning has one of three causes: the battery is worn out and can't hold a charge, something is drawing power while the car is off (a light left on, a dashcam or accessory, a faulty switch), or the alternator is not recharging it while you drive. Check the simple things first. If a new or fully charged battery still goes flat, get the charging and drain checked.</div>
<h2>1. The battery is worn out</h2><p>An old battery can start the car one day and fail the next, because it no longer holds its charge. Slow cranking, dim lights and a start-stop system that stops working are the usual hints: see the <a href="/articles/signs-car-battery-is-dying/">6 signs your car battery is dying</a>. If this is the cause, replacing the battery fixes it.</p>
<h2>2. Something is drawing power while the car is off</h2><ul><li><b>Lights or accessories left on:</b> interior lights, a boot light that does not switch off, or a door not fully shut.</li><li><b>Add-ons:</b> a dashcam, tracker, alarm or extra audio fitted to the car can keep drawing power when parked.</li><li><b>A faulty part:</b> a stuck relay or a wiring fault can drain the battery slowly. This needs a workshop to trace.</li></ul>
<p>Look around the cabin and boot before you lock the car. If the battery is fine but goes flat after the car sits, an unwanted drain is likely.</p>
<h2>3. The alternator is not charging</h2><p>The alternator recharges the battery while the engine runs. If it fails, the battery slowly runs down until the car won't start. A battery warning light on while driving, or a car that starts after a jump-start but dies again, points here. Read <a href="/articles/battery-or-alternator/">battery or alternator</a> for the simple voltage check.</p>
<h2>4. The car is used for short trips only</h2><p>Starting the engine takes a lot of power, and a very short drive may not put it all back. Over weeks the battery can end up under-charged. A longer drive now and then helps. See <a href="/articles/how-long-does-a-car-battery-last-singapore/">how long a car battery lasts in Singapore</a>.</p>
<h2>What to do this morning</h2><ol><li>Check that no lights are on and every door and the boot are shut.</li><li>If the car won't start, don't keep cranking: see <a href="/articles/car-wont-start-what-to-do/">what to do when your car won't start</a>.</li><li>Get it started with a <a href="/services/jump-start/">jump-start</a> ($50), or have a Delkor battery fitted where you are.</li><li>If it goes flat again within days, ask a workshop to test the charging and look for a drain, as a new battery will not fix those.</li></ol>
<h2>If the battery needs replacing</h2><p>Walk in to any <a href="/outlets/">Motoserv outlet</a> ({HOURS_WALK}) with our web code: the Delkor list price minus $20. Example: a Delkor <a href="/battery/ns40zl/">NS40ZL</a> is {m(walk('NS40ZL'))} walk-in. We can also fit it at your location: the list price + $30 (launch promo, normally + $50) before 10pm, or + $80 from 10pm to 9am and on public holidays ({md(('NS40ZL'))} and {m(night('NS40ZL'))} for the same NS40ZL). Call <a href="tel:{TEL}" data-ref="art">{HOT}</a> (24 hours) or find your size in the <a href="/#compare">finder</a>. Every Delkor has a 1-year warranty.</p>
<div class="enq"><b>Please note:</b> {DISCLAIMER}</div>"""),
] 
ART_DATES = {"car-wont-start-what-to-do":"2026-10-26","efb-vs-agm-vs-standard-battery":"2026-10-26","signs-car-battery-is-dying":"2026-10-26","battery-or-alternator":"2026-10-27","how-long-does-a-car-battery-last-singapore":"2026-10-30","car-battery-flat-every-morning":"2026-11-02"}

# ---- article expansion helpers (2 Nov 2026 SEO pass). Everything below is built from this file, FACTS.md and data/ only. ----
def find_row(make, model, years):
    for r in rows:
        if r[0] == make and r[1] == model and r[2] == years and r[4]: return r
    raise KeyError((make, model, years))
SRC_NOTE = "Sizes come from the Bateriku/Astra 2023 chart and the Nam Wah 2024 fitment guide, matched to the Delkor list; they are reference data, so confirm yours in the <a href=\"/#compare\">finder</a>."
def cars_table(picks, note=""):
    body = ""
    for pk in picks:
        r = find_row(*pk[:3]); k = r[4]; label = pk[3] if len(pk) > 3 else f"{r[0]} {r[1]}"
        body += f'<tr><td class="s">{esc(label)}</td><td>{esc(r[2])}</td><td>{size_link(k)}</td><td class="num">{m(walk(k))}</td><td class="num">{md((k))}</td></tr>'
    return ('<div class="tblw"><table class="tbl"><tr><th>Car</th><th>Years</th><th>Delkor size</th><th class="num">Walk-in*</th><th class="num">Fitted at you<br><small class="plbl">Launch promo</small></th></tr>' + body + '</table></div>'
            f'<p class="note">*Walk-in = list price minus $20 with the website code, at a Motoserv outlet ({HOURS_WALK}). Fitted at you = list price + $30 (launch promo, normally + $50) before 10pm including Sunday; + $80 from 10pm to 9am and on public holidays. GST included, checked {CHECKED}. {note}{SRC_NOTE}</p>')
def type_table(keys):
    return ('<div class="tblw"><table class="tbl"><tr><th>Delkor battery</th><th>Type</th><th class="num">List price</th><th class="num">Walk-in*</th><th class="num">Fitted at you<br><small class="plbl">Launch promo</small></th></tr>' +
            "".join(f'<tr><td class="s">{size_link(k)}</td><td>{esc(TYPE[k])}</td><td class="num">{m(P[k][1])}</td><td class="num">{m(walk(k))}</td><td class="num">{md((k))}</td></tr>' for k in keys) + '</table></div>')
def plain_table(head, rws):
    return '<div class="tblw"><table class="tbl"><tr>' + "".join(f"<th>{h}</th>" for h in head) + "</tr>" + "".join("<tr>" + "".join(f'<td class="s">{c}</td>' if i == 0 else f"<td>{c}</td>" for i, c in enumerate(r)) + "</tr>" for r in rws) + "</table></div>"
def fig(src, alt, w, h, cap):
    return f'<figure style="margin:14px 0"><img src="/photos/{src}" alt="{esc(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async" style="width:100%;height:auto;border-radius:14px"><figcaption class="note">{cap}</figcaption></figure>'
PHOTOS = {}
for ph in sorted((HERE / "assets" / "photos").glob("*.jpg")):
    im = Image.open(ph).convert("RGB"); PHOTOS[ph.stem] = im.size
def ans_box(t): return f'<div class="ans"><div class="k">QUICK ANSWER</div>{t}</div>'
def words(h): return len(re.sub(r"<[^>]+>", " ", h).split())
NS40, NS60, D85 = "NS40ZL", "NS60L", "85D23L"
n_matched = sum(1 for r in rows if r[4])
size_count = {}
n_sg = sum(1 for r in rows if r[4] and r[5] in ("sg", "edwin"))
for r in rows:
    if r[4] and r[5] in ("sg", "edwin"): size_count[r[4]] = size_count.get(r[4], 0) + 1
top3 = sorted(size_count.items(), key=lambda kv: -kv[1])[:3]
EFB_K = [k for k in allk if TYPE[k] == "EFB start-stop"]; AGM_K = [k for k in allk if TYPE[k] == "AGM"]
efb_lo, efb_hi = min(P[k][1] for k in EFB_K), max(P[k][1] for k in EFB_K)
agm_lo, agm_hi = min(P[k][1] for k in AGM_K), max(P[k][1] for k in AGM_K)
DAY_NIGHT = f"the Delkor list price + $30 (launch promo, normally + $50) before 10pm (including Sunday), or + $80 from 10pm to 9am and on public holidays"
CALLX = f'<a href="tel:{TEL}" data-ref="art">{HOT}</a>'

X = {}  # slug -> dict(title, desc, ans, after, faq, drop_ans)

X["car-wont-start-what-to-do"] = dict(
 title="Car Won't Start? What to Do in 5 Minutes | Battery Rescue SG",
 ans=f"Rapid clicking or silence when you start the car almost always means a flat or weak battery. Stay safe, then call our 24-hour hotline {HOT}. We fit a Delkor battery where you are for the list price + $30 (launch promo, normally + $50) before 10pm, or + $80 from 10pm to 9am and on public holidays.",
 after=f"""<h2>Battery or something else? A quick guide</h2>
{plain_table(["What you notice","Most likely cause","What to do"],[
 ["Rapid clicking, or no sound at all","Weak or flat battery","Call us; a battery fitted where you are, or a jump-start, usually fixes it"],
 ["Slow, heavy cranking","Battery is weak; it may start once and fail again","Replace it soon: see the <a href='/articles/signs-car-battery-is-dying/'>signs a battery is dying</a>"],
 ["Normal cranking but the engine will not fire","Probably not the battery (fuel, ignition or a sensor)","Tell us before we come down; the car may need a workshop or a tow"],
 ["Starts after a jump-start, then dies again","The charging side may be at fault","Read <a href='/articles/battery-or-alternator/'>battery or alternator</a>"]])}
<h2>What to tell us when you call</h2><p>Give us your <b>location</b> (the WhatsApp button on our <a href="/">home page</a> can send a map link), your <b>car model and year</b> so we bring the right Delkor size, and whether you have <b>start-stop</b>, which needs an EFB or AGM battery (see <a href="/articles/efb-vs-agm-vs-standard-battery/">EFB vs AGM vs standard</a>). We fit at your location in {AREA_TXT}. Outside those areas you can still walk in to one of our <a href="/outlets/">10 Motoserv outlets</a>, or we can <a href="/services/towing/">arrange a tow</a> from $80.</p>
<h2>Popular family cars and the Delkor size they use</h2><p>If you can name your car, you already know most of what we need. A few common Singapore cars from our fitment data:</p>
{cars_table([("Toyota","Wish","2011-2015"),("Toyota","Sienta","2003-now"),("Toyota","Alphard","2013-2016"),("Toyota","Vellfire","2008-2018"),("Toyota","Harrier (XU30)","2003-now"),("Honda","Odyssey","2013-2017"),("Honda","Stream","2006-2014"),("Nissan","Serena Comfort/highway Star","2005-2010"),("Mitsubishi","Outlander","2001-now"),("Subaru","Forester","1997-now"),("Subaru","XV","2012-now")])}
<div class="enq"><b>Please note:</b> {DISCLAIMER}</div>""",
 faq=[
  ("How much does it cost to replace a flat battery where I am?", f"The Delkor battery list price + $30 (launch promo, normally + $50) before 10pm (including Sunday), or + $80 from 10pm to 9am and on public holidays. Example: a Delkor NS40ZL is {md((NS40))} by day and {m(night(NS40))} at night. Fitting and GST are included."),
  ("Can you just jump-start my car instead?", "Yes. Our jump-start service is $50, or $80 on public holidays. If the battery is worn out, it may fail again, so we can fit a new Delkor battery on the spot."),
  ("Which areas do you come to?", f"Our onsite rescue covers {COVER_TXT}. You can also walk in to any of the 10 Motoserv outlets ({HOURS_WALK}), or ask us to arrange a tow."),
  ("What if the problem is not the battery?", f"{DISCLAIMER} We can arrange a tow from $80 (king dolly from $120)."),
  ("How do I know which battery my car needs?", "Type your car into the finder on our home page, or tell us your model and year when you call. Every battery we fit is a Delkor with a 1-year warranty."),
 ])

X["efb-vs-agm-vs-standard-battery"] = dict(
 title="EFB vs AGM vs Standard Car Battery | Battery Rescue SG",
 ans=f"A start-stop car (the engine switches off at traffic lights) needs the battery type it came with: EFB or AGM. A car without start-stop uses a standard battery. Delkor EFB lists from {m(efb_lo)} to {m(efb_hi)} and AGM from {m(agm_lo)} to {m(agm_hi)}; the smallest standard is {m(P[NS40][1])}.",
 after=f"""<h2>Delkor prices by type</h2><p>Every battery we fit is Delkor. Here are the standard sizes our customers ask for most, then every EFB and AGM size on the Delkor list.</p>
{type_table([NS40, NS60, D85] + EFB_K + AGM_K)}
<p class="note">*Walk-in = list price minus $20 with the website code, at a Motoserv outlet ({HOURS_WALK}). Fitted at you = list price + $30 (launch promo, normally + $50) before 10pm including Sunday; + $80 from 10pm to 9am and on public holidays. GST included, checked {CHECKED}.</p>
<h2>Cars that use EFB or AGM, from our fitment data</h2><p>These cars are listed in our fitment data with an EFB or AGM size. If your car is not here, use the <a href="/#compare">finder</a>.</p>
{cars_table([("Mazda","3 HATCHBACK SEDAN (WITH i-STOP)","2015-now","Mazda 3 (with i-STOP)"),("Mazda","CX-5 WITH i-STOP (PETROL)","2013-now","Mazda CX-5 (with i-STOP, petrol)"),("Mazda","6 WITH i-STOP (PETROL)","2012-now","Mazda 6 (with i-STOP, petrol)"),("Honda","Odyssey","2018-now"),("Honda","Accord","2020-now"),("Honda","Civic FK8 Type R","2017-2019"),("Nissan","Almera Vlt/vlp/vl (N18)","2019-now","Nissan Almera (N18)"),("Nissan","Juke (F15)","2010-2020"),("Toyota","Alphard 3.5 (start Stop)","2018-now","Toyota Alphard 3.5 (start-stop)"),("Toyota","Camry","2017-2020"),("Toyota","Hilux N80","2016-now"),("Lexus","NX 200T (AGZ10)","2014-2022","Lexus NX 200T"),("Mazda","CX-9 (tc)","2016-now","Mazda CX-9 (tc)")],
   "Where the chart gives a size we do not list (for example DIN80L or DIN100L), the finder shows the Delkor AGM of the same case size. ")}
<h2>Same case size matters</h2><p>A battery has to physically fit the tray and reach the terminals. That is why the finder works by size code and case size, not just by model name. In a few cases the nearest Delkor in the same case is an AGM, which is an upgrade on a standard battery: for example the finder pairs DIN80L with <a href="/battery/agm-ln4/">AGM LN4</a> and DIN100L with <a href="/battery/agm-ln5/">AGM LN5</a>.</p>""",
 faq=[
  ("What is the difference between EFB, AGM and a standard car battery?", "A standard (flooded, maintenance-free) battery suits most Japanese and Korean cars without start-stop. EFB (Enhanced Flooded Battery) is used in many start-stop Japanese cars and some European cars. AGM (Absorbent Glass Mat) is used in most European start-stop cars and many premium models."),
  ("Can I fit a standard battery in a start-stop car?", "We do not recommend it. A standard battery in a start-stop car shortens its life and can upset the car's charging system. Replace like with like: EFB with EFB, AGM with AGM."),
  ("How do I check which type my car has?", "Look at the label on your current battery, which says EFB or AGM, or type your car into our finder. If the label is unreadable, WhatsApp us your car model and year."),
  ("How much do Delkor EFB and AGM batteries cost?", f"On the Delkor list, EFB batteries run from {m(efb_lo)} to {m(efb_hi)} and AGM from {m(agm_lo)} to {m(agm_hi)}. Walk in to a Motoserv outlet with our website code for $20 off, or have it fitted at your location for the list price + $30 (launch promo, normally + $50) before 10pm."),
  ("Do you fit these at my location?", f"Yes, anywhere in Singapore (fastest in {AREA_TXT}), for the list price + $30 (launch promo, normally + $50) before 10pm including Sunday, or + $80 from 10pm to 9am and on public holidays. Every Delkor has a 1-year warranty."),
 ])

X["signs-car-battery-is-dying"] = dict(
 title="6 Signs Your Car Battery Is Dying | Battery Rescue SG",
 ans=f"The six signs are a slow crank on the first start, dim headlights at idle, a battery or charging warning light, start-stop that stops working, crust on the terminals, and a swollen or leaking case. Replace the battery before it fails: at a Motoserv outlet with our website code you pay the Delkor list price minus $20.",
 after=f"""<h2>What each sign suggests</h2>
{plain_table(["Sign","What it suggests","What to do"],[
 ["Slow crank on the first start of the day","The battery is losing its ability to hold a charge","Plan a replacement soon"],
 ["Dim headlights at idle that brighten when you rev","Weak battery, or a charging problem","Do the voltage check in <a href='/articles/battery-or-alternator/'>battery or alternator</a>"],
 ["Battery or charging warning light","Could be the battery or the charging side","Get it checked; do not wait for a no-start"],
 ["Start-stop stops working","Many cars disable start-stop when the battery is weak","Replace like with like: <a href='/articles/efb-vs-agm-vs-standard-battery/'>EFB or AGM</a>"],
 ["White or green crust on the terminals","Corrosion at the terminals","Have the terminals cleaned and the battery checked"],
 ["Swollen or leaking case","The battery is damaged","Replace it now and do not jump-start it"]])}
<h2>Replace on your terms, not at midnight</h2><p>The same battery costs different amounts depending on when and where you buy it. Take the Delkor NS60L, which fits many Japanese sedans: {m(walk(NS60))} as a walk-in with the website code, {md((NS60))} fitted at your location before 10pm, and {m(night(NS60))} from 10pm to 9am or on a public holiday. Replacing at the first signs lets you choose the cheapest option. Walk-in outlets are open {HOURS_WALK}; the full list is on the <a href="/outlets/">outlets page</a>.</p>
<h2>Sedans and hybrids: Delkor sizes from our fitment data</h2>
{cars_table([("Toyota","Altis","2006-2018"),("Toyota","Altis","2018-now"),("Toyota","Camry","2010-2017"),("Toyota","Prius","2011-2021"),("Honda","Accord","2012-2019"),("Honda","Civic","2016-now"),("Honda","Insight","2009-2014"),("Mazda","3","2010-2013"),("Nissan","Sylphy","2012-now"),("Nissan","Teana 2.0 ,2.5","2003-now","Nissan Teana (2.0, 2.5)"),("Lexus","Lexus ES 300H (AXZH10)","2018-now","Lexus ES 300H"),("Mitsubishi","Lancer","1992-2016")])}""",
 faq=[
  ("How do I know my car battery is dying?", "Watch for a slow crank on the first start of the day, dim headlights at idle, a battery or charging warning light, start-stop that stops working, white or green crust on the terminals, and a swollen or leaking case."),
  ("How much does a replacement cost?", f"It depends on the size. A Delkor NS40ZL is {m(walk(NS40))} as a walk-in with our website code and {md((NS40))} fitted at your location before 10pm. A Delkor NS60L is {m(walk(NS60))} walk-in and {md((NS60))} fitted. See the full <a href=\"/prices/\">price list</a>."),
  ("Is it the battery or the alternator?", "A new or freshly charged battery that keeps going flat, or a battery light that stays on while you drive, points to the alternator. Our <a href=\"/articles/battery-or-alternator/\">battery or alternator guide</a> has a simple voltage check."),
  ("Is there a warranty on the new battery?", "Yes. Every battery we fit is a Delkor with a 1-year warranty."),
  ("Where can I walk in?", f"At any of the 10 Motoserv outlets, {HOURS_WALK}. Show the website code to take $20 off the Delkor list price."),
 ])

X["battery-or-alternator"] = dict(
 title="Battery or Alternator? How to Tell | Battery Rescue SG",
 ans="The battery starts the car; the alternator recharges it while the engine runs. If a new or freshly charged battery keeps going flat, or the battery light stays on while you drive, suspect the alternator. A rested battery should read about 12.6V or more; with the engine running, about 13.5 to 14.5V.",
 after=f"""<h2>Voltage readings at a glance</h2>
{plain_table(["Reading","Engine","What it means"],[
 ["About 12.6V or more","Off","Battery is full"],
 ["Under about 12.4V","Off","Battery is low"],
 ["Rises to roughly 13.5 to 14.5V","Running","The alternator is charging"],
 ["Stays at battery level, or falls","Running","The alternator is not charging"]])}
<h2>Battery or alternator: which symptom points where</h2>
{plain_table(["Symptom","Points to"],[
 ["Slow crank, clicking, or silence at the first start of the day","Battery (flat or worn out)"],
 ["Battery or charging light stays on while driving","Alternator or charging circuit"],
 ["Lights dim and brighten with engine speed","Alternator"],
 ["Starts after a jump-start, dies again within a day or so","Alternator, or a battery that cannot hold a charge"],
 ["Whining or grinding noise at the front of the engine","Alternator or drive belt"]])}
<h2>If it is not the battery</h2><p>A new battery will not fix a bad alternator, and it will run flat again. Tell us your symptoms when you call: it helps us bring the right help. If the problem is the charging side, the car may need a workshop, and we can <a href="/services/towing/">arrange a tow</a> from $80 (king dolly from $120). A <a href="/services/jump-start/">jump-start</a> is $50 ($80 on public holidays) and can get you moving, but it will not cure a charging fault. See also <a href="/articles/car-battery-flat-every-morning/">why a battery goes flat overnight</a>.</p>
<p class="note">These photos are of an alternator job at SG Garage, used to show the parts. They are not a Battery Rescue job. Battery fitting prices are in our <a href="/prices/">price list</a>.</p>""",
 faq=[
  ("How can I tell if it is my battery or my alternator?", "With a multimeter, measure the battery with the engine off: about 12.6V or more is full, under about 12.4V is low. Then start the car: the voltage should rise to roughly 13.5 to 14.5V. If it stays at battery level or falls, the alternator is not charging."),
  ("Can a bad alternator ruin a new battery?", "A failing alternator stops recharging, so even a brand-new battery runs flat. That is why a new battery that keeps dying points to the charging side."),
  ("Why does my car start after a jump-start and then die again?", "That pattern suggests the alternator is not recharging the battery, or the battery cannot hold a charge. Check the voltage with the engine running, or have the car looked at before you rely on it."),
  ("What does a jump-start cost?", "$50, or $80 on public holidays. If the problem turns out not to be battery-related, an onsite service fee of $50 to $80 applies; final charges depend on location and service requirements."),
  ("What if the alternator is the problem?", "The car may need a workshop. We can arrange a tow from $80, or from $120 with a king dolly."),
 ])

X["how-long-does-a-car-battery-last-singapore"] = dict(
 title="How Long Does a Car Battery Last in Singapore? | Battery Rescue SG",
 ans=f"A car battery typically lasts a few years, but there is no fixed number, and Singapore's heat, short trips and a car full of electronics can wear one out sooner. Watch for slow starts and replace it before it strands you. Every Delkor we fit has a 1-year warranty.",
 after=f"""<h2>What a replacement costs, by size</h2><p>Replacing on your own schedule is the cheapest route. Of the {n_sg:,} Japanese, Korean and other Asian model entries in our Bateriku/Astra-based fitment data that map to a Delkor size, the three sizes used most are {top3[0][0]} ({top3[0][1]} entries), {top3[1][0]} ({top3[1][1]}) and {top3[2][0]} ({top3[2][1]}). Their prices:</p>
{type_table([k for k, _ in top3])}
<p class="note">*Walk-in = list price minus $20 with the website code, at a Motoserv outlet ({HOURS_WALK}). Fitted at you = list price + $30 (launch promo, normally + $50) before 10pm including Sunday; + $80 from 10pm to 9am and on public holidays. GST included, checked {CHECKED}.</p>
<h2>Small cars: Delkor sizes from our fitment data</h2>
{cars_table([("Toyota","Vios","2019-now"),("Toyota","Yaris","2007-now"),("Toyota","Altis","2018-now"),("Honda","Jazz","2015-now"),("Honda","City","2004-2019"),("Honda","Freed","2016-now"),("Honda","HR-V / Vezel","2015-2021"),("Nissan","Almera (N17)","2011-now"),("Suzuki","Swift","2017-2020"),("Kia","Picanto","2004-2016"),("Hyundai","i10","2008-2013")])}
<h2>A simple routine</h2><p>You do not need to know the battery's age. Use the signs in <a href="/articles/signs-car-battery-is-dying/">6 signs your car battery is dying</a> as your guide, and if the car is not starting at all, see <a href="/articles/car-wont-start-what-to-do/">what to do in the next 5 minutes</a>.</p>""",
 faq=[
  ("How long does a car battery last?", "Typically a few years, but there is no fixed number. Heat, short trips and electrical load all shorten it, so go by the warning signs rather than the calendar."),
  ("Why do batteries wear out faster in Singapore?", "Constant high temperatures speed up wear inside a battery, and repeated short trips can leave it under-charged. A car full of electronics adds to the load."),
  ("How do I know when to replace mine?", "A slow crank on the first start of the day, dim headlights at idle or start-stop that stops working are the usual hints. See our guide to the 6 signs a battery is dying."),
  ("What warranty do you give?", "Every Delkor battery we fit has a 1-year warranty."),
  ("How much is a replacement?", f"A Delkor NS40ZL is {m(walk(NS40))} as a walk-in with our website code, against a list price of {m(P[NS40][1])}. Fitted at your location it is {md((NS40))} before 10pm and {m(night(NS40))} from 10pm to 9am or on public holidays."),
 ])

X["car-battery-flat-every-morning"] = dict(
 title="Why Does a Car Battery Go Flat Overnight? | Battery Rescue SG",
 ans="A battery that is flat every morning has one of three causes: the battery is worn out and cannot hold a charge, something draws power while the car is off, or the alternator is not recharging it as you drive. Check the simple things first. If a new battery keeps going flat, look at the charging side.",
 after=f"""<h2>Quick diagnosis</h2>
{plain_table(["Clue","Likely cause","Next step"],[
 ["Slow crank for weeks, then a flat morning","Worn-out battery","Replace it: see the <a href='/articles/signs-car-battery-is-dying/'>6 signs</a>"],
 ["Flat only after the car sits for a few days","Something drawing power when parked","Check lights, doors and boot; look at add-ons such as a dashcam or tracker"],
 ["Battery light on while driving, or dies again after a jump-start","Alternator not charging","Do the voltage check in <a href='/articles/battery-or-alternator/'>battery or alternator</a>"],
 ["Mostly very short trips","Battery under-charged over weeks","Take a longer drive from time to time"]])}
{fig("battery-voltage-12-80v.webp", "Multimeter on a car battery showing 12.80 volts", PHOTOS["battery-voltage-12-80v"][0], PHOTOS["battery-voltage-12-80v"][1], "A multimeter on the battery reads 12.80V: a fully charged battery at rest. If it reads much lower after the car has sat overnight, suspect a drain or a worn battery. Photo: an alternator job at SG Garage, not a Battery Rescue job.")}
<h2>SUVs and crossovers: Delkor sizes from our fitment data</h2>
{cars_table([("Toyota","CHR","2016-now","Toyota C-HR"),("Toyota","Harrier (XU60)","2013-2020"),("Honda","CR-V","2017-now"),("Honda","HR-V / Vezel New Gen Hybrid","2019-now","Honda HR-V / Vezel hybrid"),("Mazda","CX-5 WITH i-STOP (PETROL)","2013-now","Mazda CX-5 (with i-STOP, petrol)"),("Nissan","X-TRAIL Petrol 1.3/1.6,DIESEL 1.6/1.7/2.0","2017-now","Nissan X-Trail (2017-now)"),("Subaru","XV","2012-now"),("Mitsubishi","ASX","2010-now"),("Kia","Sportage","2018-now")])}
<h2>If a new battery is the answer</h2><p>We can fit it where the car is, anywhere in Singapore (fastest in {AREA_TXT}): {DAY_NIGHT}. Or walk in to any <a href="/outlets/">Motoserv outlet</a> with our website code for $20 off. If the problem is a drain or the charging side, a new battery will not cure it, so ask a workshop to test those first.</p>""",
 faq=[
  ("Why is my car battery dead every morning?", "Usually one of three things: the battery is worn out, something is drawing power while the car is off (a light left on, a dashcam or other accessory, a faulty switch), or the alternator is not recharging it while you drive."),
  ("Can a dashcam or tracker drain my battery?", "Add-ons such as a dashcam, tracker, alarm or extra audio can keep drawing power when the car is parked. If the battery is fine but goes flat after the car sits, an unwanted drain is likely."),
  ("Will a new battery stop it?", "Only if the old battery was the cause. A drain or a failing alternator will flatten a new battery too, so check those if it keeps happening."),
  ("How much is a jump-start?", "$50, or $80 on public holidays. We can also fit a new Delkor battery where you are."),
  ("Can short trips flatten a battery?", "Starting the engine takes a lot of power, and a very short drive may not put it all back. Over weeks the battery can end up under-charged. A longer drive now and then helps."),
 ])

ANS_RE = re.compile(r'<div class="ans"><div class="k">QUICK ANSWER</div>.*?</div>', re.S)
def fmt_date(iso): return datetime.date.fromisoformat(iso).strftime("%-d %b %Y")
art_cards = ""; ART_WORDS = {}
for s_, t, d, b in ARTS:
    x = X[s_]; AD = ART_DATES[s_]
    b = ANS_RE.sub("", b, count=1).replace(".jpg\"", ".webp\"")
    aw = words(x["ans"]); assert 40 <= aw <= 60, (s_, aw)
    faq_block = f'<h2>Frequently asked questions</h2>{faq_html(x["faq"])}'
    art = f'{b}{x["after"]}{faq_block}'
    ART_WORDS[s_] = words(f'{x["ans"]} {art}')
    page(f"/articles/{s_}/", x["title"], d,
         f'<h1 class="h1" style="margin-top:8px">{esc(t)}</h1>{ans_box(x["ans"])}<p class="note">By {BRAND} (Motoserv) · Last updated {ART_UPDATED_TXT} · First published {fmt_date(AD)}</p><article class="sec">{art}</article>',
         [{"@type":"Article","headline":t,"datePublished":AD,"dateModified":ART_UPDATED,"author":{"@type":"Organization","name":BRAND,"url":BASE+"/"},"publisher":{"@id":BASE+"/#org"},"image":BASE+"/og.jpg","inLanguage":"en-SG","mainEntityOfPage":BASE+f"/articles/{s_}/"}, faq_ld(x["faq"])],
         "More", [("Home","/"),("Articles","/articles/"),(t,f"/articles/{s_}/")], "0.6")
    art_cards += f'<a class="tile" href="/articles/{s_}/" style="grid-column:1/-1"><span>{esc(t)}<small>{esc(d)}</small></span></a>'
art_faq = [
 ("What do these guides cover?", "Six short guides on car batteries in Singapore: what to do when your car won't start, how to tell a battery from an alternator problem, why a battery goes flat overnight, the signs a battery is dying, how long a battery lasts, and EFB vs AGM vs standard batteries."),
 ("Where can I find the battery size and price for my car?", f"Use the finder on our home page, or open your brand under <a href=\"/car-battery/\">car battery by brand</a>. Every battery we fit is a Delkor, with a 1-year warranty. Prices include GST and were checked {CHECKED}."),
 ("What if I am stuck right now?", f"Call our 24-hour hotline {HOT} or WhatsApp your location. We fit a Delkor battery at your location anywhere in Singapore (fastest in {AREA_TXT}) for the list price + $30 (launch promo, normally + $50) before 10pm, or + $80 from 10pm to 9am and on public holidays."),
]
page("/articles/", "Car Battery Tips Singapore | Battery Rescue SG", "Short guides: what to do when your car won't start, battery or alternator, EFB vs AGM batteries, and signs your battery is dying.",
     f'<h1 class="h1" style="margin-top:8px">Car battery guides</h1><section class="sec"><p>These guides are written for Singapore drivers who want a straight answer about their car battery. They cover what to do when the car will not start, how to tell a flat battery from a charging fault, why a battery can go flat overnight, how long a battery lasts, and when you need an EFB or AGM battery instead of a standard one. Each guide shows the Delkor battery sizes and prices that apply to common cars, taken from the same fitment data and price list as our finder. Battery Rescue SG is the car battery service of Motoserv, and every battery we fit is a Delkor with a 1-year warranty. If you are stuck now, skip the reading and call {CALLX}.</p></section>'
     f'<div class="grid" style="margin-top:12px">{art_cards}</div><section class="sec"><h2>Questions</h2>{faq_html(art_faq)}</section>', [faq_ld(art_faq)], "More", [("Home","/"),("Articles","/articles/")], "0.6")

page("/more/", "More | Battery Rescue SG", "Prices, outlets, car brands, Delkor, guides and contact for Battery Rescue SG, the Motoserv car battery service. 24-hour hotline 8125 9169.",
     f"""<h1 class="h1" style="margin-top:8px">More</h1><ul class="menu" style="margin-top:12px">
<li><a href="/rescue/">Onsite battery replacement</a></li><li><a href="/services/jump-start/">Jump-start ($50)</a></li><li><a href="/services/towing/">Emergency towing (from $80)</a></li><li><a href="/walk-in/">Walk-in with $20 off</a></li><li><a href="/prices/">Full price list</a></li>
<li><a href="/car-battery/">Battery by car brand</a></li><li><a href="/outlets/">Motoserv outlets</a></li><li><a href="/delkor/">Why Delkor</a></li>
<li><a href="/articles/">Guides</a></li><li><a href="/about/">About us</a></li><li><a href="/privacy/">Privacy</a></li></ul>""", [], "More", [("Home","/"),("More","/more/")], "0.3")
page("/privacy/", "Privacy Policy | Battery Rescue SG", "How Battery Rescue SG, the Motoserv car battery service, handles the details you send us by WhatsApp or phone to arrange a battery replacement.",
     f"""<h1 class="h1" style="margin-top:8px">Privacy policy</h1><section class="sec"><p>We collect only what you send us to arrange a battery replacement: your name, phone number, car model and location, through WhatsApp or a call. We use it to serve you and keep job records, and we do not sell it.</p>
<p>If you share your location with the WhatsApp button, your phone puts a map link in the message; the website does not store it. The finder remembers your $20 code on your own phone only.</p>
<p>We count taps on the Call, WhatsApp and code buttons (without your name or number) to see which pages help customers. For questions or to ask us to delete your data, call {HOT}.</p>
<div class="pending">CONFIRM: Motoserv's Data Protection Officer contact (PDPA).</div></section>""", [], "More", [("Home","/"),("Privacy","/privacy/")], "0.2")
page("/404.html", "Page not found | Battery Rescue SG", "This page does not exist.",
     f'''<div class="card" style="margin-top:16px"><h1 class="h1">Page not found</h1><p class="sub">That page is not here, but we can still help. Stuck with a flat battery? Call <a href="tel:{TEL}" data-ref="404">{HOT}</a> (24 hours) or WhatsApp us.</p><a class="big n" href="/">Go to the battery finder</a></div>
<section class="sec"><h2>Services</h2><ul class="menu"><li><a href="/rescue/">Onsite battery replacement</a></li><li><a href="/services/jump-start/">Jump-start ($50)</a></li><li><a href="/services/towing/">Emergency towing (from $80)</a></li><li><a href="/walk-in/">Walk-in with $20 off</a></li><li><a href="/prices/">Full price list</a></li><li><a href="/car-battery/">Battery by car brand</a></li><li><a href="/outlets/">Motoserv outlets</a></li></ul></section>
<section class="sec"><h2>Guides</h2><ul class="menu">''' + "".join(f'<li><a href="/articles/{sl}/">{esc(tt)}</a></li>' for sl, tt, _d, _b in ARTS) + f'''<li><a href="/articles/">All guides</a></li></ul></section>
<section class="sec"><h2>Contact</h2><p>24-hour hotline and WhatsApp: <a href="tel:{TEL}" data-ref="404">{HOT}</a>. <a href="/about/">About us</a> · <a href="/more/">More</a></p></section>''')

# ---------------- static files ----------------
(OUT / "br.css").write_text(CSS); (OUT / "br.js").write_text(JS); (OUT / "data.js").write_text(DATAJS)
(OUT / "manifest.webmanifest").write_text(json.dumps({"name":"Battery Rescue SG","short_name":"Battery Rescue","start_url":"./","scope":"./","display":"standalone","background_color":"#f3f5fa","theme_color":"#0b1b4d",
  "icons":[{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]}))
KEY = "b7e1c94a2f6d4e3b8a5c0d9e1f2a3b4c"
(OUT / f"{KEY}.txt").write_text(KEY)
(OUT / "robots.txt").write_text(f"""User-agent: *
Allow: /

User-agent: Googlebot
Allow: /
User-agent: Bingbot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: GPTBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: DuckAssistBot
Allow: /

Sitemap: {BASE}/sitemap.xml
""")
(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  "".join(f"<url><loc>{BASE}{p}</loc><lastmod>{LASTMOD[p]}</lastmod><priority>{pr}</priority></url>\n" for p, pr in pages) + "</urlset>\n")
LLMS_UPDATED = max(LASTMOD.values())
llms = [f"# {BRAND}", "", f"> Car battery replacement in Singapore by Motoserv (CaseTrust-accredited group, 10 outlets). Every battery is a Delkor with a 1-year warranty. 24-hour hotline {HOT} (also WhatsApp). Prices include GST and fitting, checked {CHECKED}.", "",
  f"Last updated: {LLMS_UPDATED}", "", "## Contact (NAP)", f"- Name: {BRAND} (by Motoserv), {BASE}/", f"- Phone / WhatsApp: {HOT} ({TEL})", "- Address: no single head office; 10 Motoserv walk-in outlets, listed under Outlets below", f"- Hours: hotline and onsite rescue 24 hours (night rate 10pm-9am and public holidays); walk-in outlets {HOURS_WALK}", "",
  f"## On-site rescue area: {COVER_TXT}. Walk-in also at the 10 Motoserv outlets.", "", "## Other services", "- Jump-start: $50 ($80 on public holidays).", "- Emergency towing: from $80; king dolly (4-wheel) from $120.", f"- {DISCLAIMER}", "", "## Price rules", f"- Walk-in at any Motoserv outlet ({HOURS_WALK}): Delkor list price minus $20 with the website code (walk-in only).", "- Fitted at your location before 10pm, including Sunday: list price + $30 (launch promo, normally + $50).", "- Fitted at your location 10pm-9am and on public holidays: list price + $80.", "",
  "## Delkor prices (walk-in with code / list / at your location before 10pm, launch promo / night & PH)"] + \
  [f"- {NAME[k]} ({P[k][0]}Ah{', '+AKA[k] if AKA[k] else ''}): {m(walk(k))} / {m(P[k][1])} / {md((k))} / {m(night(k))}  {BASE}/battery/{slug(k)}/" for k in allk] + \
  ["", "## Common Singapore cars (battery size)"] + \
  [f"- {r[0]} {r[1]} ({r[2]}): {NAME[r[4]]}" + (f" (replaces {r[3]}, same case size)" if r[6] else "") for r in rows if r[5] in ("sg","edwin") and r[4] and r[0] in ("Toyota","Honda","Nissan","Mazda","Hyundai","Kia","Mitsubishi")][:120] + \
  ["", "## Outlets"] + [f"- Motoserv @ {n}: {a} ({STATION[s]})" for n,s,a,la,lo in OUTLETS] + \
  ["", "## Pages", f"- Finder (car to battery and price): {BASE}/", f"- Price list: {BASE}/prices/", f"- Battery rescue: {BASE}/rescue/", f"- Walk-in $20 off: {BASE}/walk-in/", f"- Car brands: {BASE}/car-battery/", f"- Why Delkor: {BASE}/delkor/", f"- About: {BASE}/about/"] + \
  [f"- {PTITLES[p].rsplit(' | ', 1)[0]}: {BASE}{p} - {PDESC[p]}" for p in ["/outlets/", "/services/jump-start/", "/services/towing/"] + sorted(q for q in PTITLES if q.startswith("/rescue/") and q != "/rescue/") + ["/articles/"] + sorted(q for q in PTITLES if q.startswith("/articles/") and q != "/articles/") + ["/more/"] if p in PTITLES]
(OUT / "llms.txt").write_text(promo_txt("\n".join(llms)) + "\n")
(OUT / "photos").mkdir(exist_ok=True)
for ph in (HERE / "assets" / "photos").glob("*.jpg"):
    im = Image.open(ph).convert("RGB")
    for q in (82, 76, 70, 62):
        im.save(OUT / "photos" / (ph.stem + ".webp"), "WEBP", quality=q, method=6)
        if (OUT / "photos" / (ph.stem + ".webp")).stat().st_size <= 150 * 1024: break
for f in ("favicon.ico","icon-192.png","icon-512.png","apple-touch-icon.png","og.jpg"):
    src = HERE / "assets" / f
    if src.exists(): (OUT / f).write_bytes(src.read_bytes())
(OUT / "htaccess.txt").write_text("""# Battery Rescue SG (batteryrescue.sg). Document root for the domain; also served as pageonesingapore.com/preview/battery-rescue/.
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://batteryrescue.sg/$1 [L,R=301]
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8
AddType application/manifest+json .webmanifest
<IfModule mod_headers.c>
SetEnvIfNoCase Host ^(www\\.)?pageonesingapore\\.com$ P1_PREVIEW=1
Header set X-Robots-Tag "noindex, nofollow" env=P1_PREVIEW
<FilesMatch "\\.(html)$">
Header set Cache-Control "max-age=3600, public"
</FilesMatch>
</IfModule>
""")
print(f"pages {len(pages)+1}, fitment rows {len(rows)} (matched {sum(1 for r in rows if r[4])}), brand pages {len(BRAND_PAGES)}, data.js {len(DATAJS)//1024} KB")
LEDGER_F.write_text(json.dumps(NEWLEDGER, indent=0, sort_keys=True))
print("article words:", ART_WORDS)
