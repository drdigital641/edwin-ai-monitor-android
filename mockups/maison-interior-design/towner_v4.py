# Towner Residences V4 (Edwin's direction, 8 Nov 2026): four named design themes, picture first,
# original HDB brochure plans, text below. Replaces the 36-image carousel (picker2) on this page only.
# exec'd by launches.py after vpage.py; vpage() hands over when cfg["v4"] is set.

V4_V = "v4"
V4_DIR = "towner-v4"
V4_NOTE = "Concept design by Maison, not the actual unit"
V4_AI = "AI-generated style concept; layouts, fittings and views are illustrative."
V4_BROCHURE = "https://btohq.sgp1.cdn.digitaloceanspaces.com/bto/aug-2021-bto/towner-residences.pdf"
V4_TOUR = "https://assets.hdb.gov.sg/community/towner_residences/index.html"

V4_HERO = dict(
    eyebrow="Four Maison-inspired concepts · Towner Residences",
    intro="Explore four interior design themes for your Towner Residences BTO, then WhatsApp Maison to discuss your own layout.",
    btn="WhatsApp Maison about this look",
    msg="Hi Maison, I’m planning my Towner Residences BTO renovation. I like the Warm Japandi living room concept. Can we discuss my layout?")

V4_THEMES = [
    dict(key="warm-japandi", img="towner-v4-living-warm-japandi", theme="Warm Japandi", room="Living room",
         h3="Towner Residences living room interior design — Warm Japandi",
         cap="Warm oak, tactile cream fabrics and a sculptural stone-look table create a calm, welcoming living space. An inviting starting point for your Towner BTO renovation.",
         alt="Warm Japandi living room concept with oak storage, cream sofa and framed HDB-style windows",
         btn="Discuss Warm Japandi on WhatsApp",
         msg="Hi Maison, I’m interested in the Warm Japandi living room concept for my Towner Residences BTO. Can we discuss my layout?"),
    dict(key="modern-luxe", img="towner-v4-kitchen-modern-luxe", theme="Modern Luxe", room="Kitchen",
         h3="3-room and 4-room BTO kitchen design idea — Modern Luxe",
         cap="Graphite cabinetry, pale stone surfaces and quiet task lighting bring a polished look to a compact kitchen. Adapt the finishes and storage to your actual unit.",
         alt="Modern Luxe compact kitchen concept with graphite cabinets, pale stone counters and warm task lighting",
         btn="Discuss Modern Luxe on WhatsApp",
         msg="Hi Maison, I’m interested in the Modern Luxe kitchen concept for my Towner Residences BTO. Can we discuss my layout?"),
    dict(key="hotel-suite", img="towner-v4-main-bedroom-hotel-suite", theme="Hotel Suite", room="Main bedroom",
         h3="Towner Residences main bedroom design — Hotel Suite",
         cap="Walnut tones, soft upholstery and layered lighting give the main bedroom a boutique-hotel mood. Fitted storage keeps the room grounded in everyday apartment living.",
         alt="Hotel Suite main bedroom concept with walnut headboard, fitted wardrobes and soft neutral bedding",
         btn="Discuss Hotel Suite on WhatsApp",
         msg="Hi Maison, I’m interested in the Hotel Suite main bedroom concept for my Towner Residences BTO. Can we discuss my layout?"),
    dict(key="soft-scandi", img="towner-v4-common-bedroom-soft-scandi", theme="Soft Scandi", room="Common bedroom",
         h3="Towner BTO common bedroom renovation idea — Soft Scandi",
         cap="Sage, pale oak and integrated storage make a compact bedroom feel composed and useful. A single bed and window-side desk balance rest with a practical workspace.",
         alt="Soft Scandi common bedroom concept with sage wall, single bed, oak desk and fitted wardrobe",
         btn="Discuss Soft Scandi on WhatsApp",
         msg="Hi Maison, I’m interested in the Soft Scandi common bedroom concept for my Towner Residences BTO. Can we discuss my layout?"),
]

V4_PLANS = [
    dict(img="towner-hdb-brochure-3room", w=1090, h=1460, title="3-room",
         alt="HDB brochure floor plan of a Towner Residences 3-room flat with suggested furniture layout",
         area="Approx. 68 sqm including the air-con ledge (65 sqm internal).", page="printed p.10"),
    dict(img="towner-hdb-brochure-4room-arrangements", w=1600, h=2262, title="4-room (both arrangements)",
         alt="HDB brochure page showing both Towner Residences 4-room floor plan arrangements with suggested furniture layout",
         area="Approx. 93 sqm including the air-con ledge (90 sqm internal). The brochure shows two arrangements.", page="printed p.12"),
]

V4CFG = {
 "towner-residences": dict(dir=V4_DIR, ref="towner-v4", hero=V4_HERO, themes=V4_THEMES, plans=V4_PLANS,
   themes_h2="Four Towner Residences BTO interior design themes",
   themes_sub="Four rooms, four different looks. Each is a starting point we adapt to your actual unit.",
   plans_h2="Towner Residences 3-room and 4-room floor plans",
   plans_sub="Original pages from the HDB sales brochure, with HDB’s suggested furniture layout. Not construction drawings; owners confirm their actual unit.",
   plan_label="Floor plan: HDB brochure", plans_cls="v4-plans",
   plans_src=f'Source: HDB-authored Towner Residences sales brochure, <a href="{V4_BROCHURE}" target="_blank" rel="noopener">archive copy hosted by BTO HQ</a>. '
             f'For context, see HDB’s <a href="{V4_TOUR}" target="_blank" rel="noopener">Towner Residences virtual tour</a>.',
   citation=[V4_BROCHURE, V4_TOUR], facts=None, css="",
   end_msg=V4_HERO["msg"].replace("I like the Warm Japandi living room concept. ", "")),
}
for _p in V4_PLANS:
    _p.setdefault("cap", f'{_p["title"]}, brochure {_p["page"]}. {_p["area"]}')

V4_CSS = """
.v4h{padding:22px 0 0}.v4h .wrap{max-width:1240px}
.v4-eb{font:500 12px/1.4 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--brass);margin:0 0 10px}
.v4h h1{font:400 clamp(30px,6vw,52px)/1.08 var(--serif);margin:0 0 12px;max-width:22ch}
.v4-intro{font-size:17px;line-height:1.55;color:var(--ink2);margin:0 0 20px;max-width:60ch}
.v4-fig{margin:0}.v4-fig img{display:block;width:100%;height:auto;aspect-ratio:16/9;background:#e9e2d8}
.v4-fig figcaption{margin-top:10px;font-size:14px;line-height:1.45;color:var(--ink2)}
.v4-fig figcaption b{display:block;font-weight:500;color:var(--ink)}
.v4-fig figcaption span{display:block;font-size:13px;color:var(--mute)}
.v4-wa{display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 24px;background:#1f6f4a;color:#fff;font:500 13px/1.2 var(--sans);letter-spacing:.1em;text-transform:uppercase;text-align:center;border-radius:2px;margin-top:16px;transition:background .3s}
.v4-wa:hover{background:#185a3c}.v4-wa svg{flex:0 0 auto}
.v4-hero-cta{display:flex;flex-wrap:wrap;align-items:center;gap:12px 24px}
.v4-hero-cta .link{margin-top:16px}
.v4-cards{display:grid;gap:40px;margin-top:22px}
.v4-card{display:flex;flex-direction:column}
.v4-card .v4-th{font:500 12px/1.4 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--brass);margin:16px 0 6px}
.v4-card h3{font:400 clamp(22px,3vw,28px)/1.2 var(--serif);margin:0 0 8px}
.v4-card p.v4-cap{margin:0;font-size:16px;line-height:1.55;color:var(--ink2)}
.v4-card .v4-wa{align-self:flex-start}
.v4-plans{display:grid;gap:32px;margin-top:22px}
.v4-plan{margin:0}
.v4-plan a.v4-zoom{display:block;border:1px solid var(--line);background:#fff;position:relative}
.v4-plan img{display:block;width:100%;height:auto}
.v4-plan .v4-zl{display:flex;align-items:center;justify-content:center;min-height:44px;border-top:1px solid var(--line);background:#f5f2ec;color:var(--ink);font:500 12px/1 var(--sans);letter-spacing:.12em;text-transform:uppercase}
.v4-plan figcaption{margin-top:10px;font-size:14px;line-height:1.5;color:var(--ink2)}
.v4-plan figcaption b{display:block;color:var(--ink);font-weight:500}
.v4-src{margin-top:18px;font-size:14px;line-height:1.6;color:var(--ink2)}
.v4-src a,.v4-lead a{color:var(--brass);text-decoration:underline}
.v4-lead{max-width:72ch;font-size:16px;line-height:1.6;color:var(--ink2)}
@media(max-width:599px){.v4-wa{width:100%}.v4h h1{max-width:none}}
@media(min-width:1100px){.v4h-g{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);grid-template-areas:'t f' 'c f';column-gap:48px;align-items:start}.v4h-t{grid-area:t;align-self:end}.v4h-f{grid-area:f}.v4h .v4-hero-cta{grid-area:c;align-self:start}.v4h h1{font-size:clamp(34px,3.6vw,48px)}}
@media(min-width:900px){.v4h{padding-top:40px}.v4-cards{grid-template-columns:1fr 1fr;gap:56px 40px}.v4-plans{grid-template-columns:1fr 1fr;align-items:start;gap:40px}}
body{padding-bottom:env(safe-area-inset-bottom)}
"""

WA_ICON = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>'

def _v4src(name, d=V4_DIR):
    return f"{BASE}images/new-launches/{d}/{name}.webp?v={V4_V}"

def _v4img(name, alt, sizes, lazy=True, d=V4_DIR, w=1600):
    b = f"{BASE}images/new-launches/{d}/{name}"
    return (f'<img src="{b}-{w}.webp?v={V4_V}" srcset="{b}-900.webp?v={V4_V} 900w, {b}-{w}.webp?v={V4_V} {w}w" sizes="{sizes}" '
            f'width="{w}" height="{w * 9 // 16}" alt="{e(alt)}" decoding="async"' + (' loading="lazy"' if lazy else ' fetchpriority="high"') + '>')

def _v4wa(label, msg, ref, theme, path):
    return (f'<a class="v4-wa" href="{wa(msg)}" data-cta="whatsapp" data-ref="{ref}" data-theme="{e(theme)}" '
            f'data-path="{BASE}{path}" rel="noopener">{WA_ICON}<span>{e(label)}</span></a>')

def _v4cap(extra=""):
    return f'<figcaption>{extra}<b>{V4_NOTE}</b><span>{V4_AI}</span></figcaption>'

def vpage_v4(slug):
    c, cfg, v = parse_copy(slug), VPAGES[slug], V4CFG[slug]
    path = f"new-launches/{slug}/"
    gk, gs = KINDS[cfg["kind"]]
    h, d, ref, themes_l, W = v["hero"], v["dir"], v["ref"], v["themes"], v.get("w", 1600)
    t0 = themes_l[0]
    hero = (f'<section class="v4h"><div class="wrap v4h-g"><div class="v4h-t"><p class="v4-eb">{e(h["eyebrow"])}</p><h1>{e(c["h1"])}</h1>'
            f'<p class="v4-intro">{e(h["intro"])}</p></div>'
            f'<figure class="v4-fig v4h-f">{_v4img(t0["img"], t0["alt"], "(min-width:1100px) 720px, 100vw", lazy=False, d=d, w=W)}{_v4cap()}</figure>'
            f'<div class="v4-hero-cta">{_v4wa(h["btn"], h["msg"], ref + "-hero", t0["theme"], path)}'
            f'<a class="link" href="{BASE}services/{gs}/">{e(GBY[gs]["short"])} guide</a></div></div></section>')
    cards = "".join(
        f'<article class="v4-card" id="{t["key"]}"><figure class="v4-fig">{_v4img(t["img"], t["alt"], "(min-width:1240px) 580px, (min-width:900px) 46vw, 100vw", d=d, w=W)}{_v4cap()}</figure>'
        f'<p class="v4-th">{e(t["theme"])} · {e(t["room"])}</p><h3>{e(t["h3"])}</h3><p class="v4-cap">{e(t["cap"])}</p>'
        f'{_v4wa(t["btn"], t["msg"], ref + "-" + t["key"], t["theme"], path)}</article>' for t in themes_l)
    themes = (f'<section class="vsec"><div class="wrap"><h2 class="vh2">{e(v["themes_h2"])}</h2>'
              f'<p class="vsub">{e(v["themes_sub"])}</p>'
              + (f'<p class="v4-src">{e(v["themes_note"])}</p>' if v.get("themes_note") else "") +
              f'<div class="v4-cards">{cards}</div></div></section>')
    plans = "".join(
        f'<figure class="v4-plan"><a class="v4-zoom" href="{_v4src(p["img"], d)}" target="_blank" rel="noopener" aria-label="Open the full-size {e(p["title"])} floor plan">'
        f'<img src="{_v4src(p["img"], d)}" width="{p["w"]}" height="{p["h"]}" alt="{e(p["alt"])}" loading="lazy" decoding="async"><span class="v4-zl" aria-hidden="true">Tap to enlarge ↗</span></a>'
        f'<figcaption><b>{e(v["plan_label"])}</b>{e(p["cap"])}</figcaption></figure>' for p in v["plans"])
    plan_sec = (f'<section class="vsec"><div class="wrap"><h2 class="vh2">{e(v["plans_h2"])}</h2>'
                f'<p class="vsub">{e(v["plans_sub"])}</p>'
                f'<div class="{v["plans_cls"]}">{plans}</div>'
                + (f'<p class="v4-src">{e(v["plans_note"])}</p>' if v.get("plans_note") else "") +
                f'<p class="v4-src">{v["plans_src"]}</p></div></section>')
    if v["facts"]:
        fh2, fitems, fnote = v["facts"]
        plan_sec += (f'<section class="vsec"><div class="wrap"><h2 class="vh2">{e(fh2)}</h2><ul class="v4-facts">'
                     + "".join(f'<li><span>{e(t)}</span> <a href="{u}" target="_blank" rel="noopener">{e(sl)}</a></li>' for t, sl, u in fitems)
                     + f'</ul><p class="v4-src">{e(fnote)}</p></div></section>')
    glance = "".join(f'<article class="vgl"><h3>{e(g["name"])}</h3><ul>'
                     + (f'<li>{ICON["size"]}<span>{e(g["size"])}</span></li>' if g.get("size") else "")
                     + (f'<li>{ICON["beds"]}<span>{e(g["beds"])}</span></li>' if g.get("beds") else "")
                     + f'<li>{ICON["idea"]}<span>{e(g["idea"])}</span></li></ul></article>' for g in cfg["glance"])
    steps = "".join(f'<li><span class="sn">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(x)}</p></li>' for i, (t, x) in enumerate(cfg["steps"]))
    faqs = "".join(f'<details class="qa"><summary><h3>{e(q)}</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq">{_links(a)}</div></details>' for q, a in c["faq"])
    lower = (f'<section class="vsec"><div class="wrap"><h2 class="vh2">About these concepts and plans</h2><div class="v4-lead">{_links(c["lead"])}</div></div></section>'
             f'<section class="vsec"><div class="wrap"><h2 class="vh2">{e(v.get("glance_h2", "Layout at a glance"))}</h2><div class="vgls">{glance}</div>{f'<p class="v4-src">{e(v["glance_note"])}</p>' if v.get("glance_note") else ""}</div></section>'
             + "".join(f'<section class="vsec"><div class="wrap"><h2 class="vh2">{e(xh)}</h2><div class="v4-lead"><p>{e(xt)}</p></div></div></section>' for xh, xt in v.get("extra", [])) +
             f'<section class="vsec"><div class="wrap"><h2 class="vh2">{e(v.get("steps_h2", "From keys to move-in"))}</h2><ol class="vsteps">{steps}</ol></div></section>'
             f'<section class="vsec vfaq"><div class="wrap narrow"><h2 class="vh2">Details, caveats and sources</h2>{faqs}'
             f'<details class="qa"><summary><h3>Sources</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq">{_links(c["sources"])}</div></details>'
             f'<p class="v4-src">More BTO and condo projects: <a href="{BASE}new-launches/">New launches</a>.</p>'
             + (f'<p class="v4-lead">{e(v["end_note"])}</p>' if v.get("end_note") else "") +
             f'<div class="vh-cta end">{_v4wa("WhatsApp Maison", v["end_msg"], ref + "-end", "general", path)}</div></div></section>')
    og = f"https://pageonesingapore.com{BASE}images/new-launches/{d}/{t0['img']}-{W}.webp"
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("New launches", "new-launches/"), (c["h1"], path)]),
              {"@type": "Article", "headline": c["h1"], "description": c["desc"], "datePublished": "2026-11-07", "dateModified": "2026-11-08",
               "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "mainEntityOfPage": DOMAIN + "/" + path,
               "image": [DOMAIN + f"/images/new-launches/{d}/{t['img']}-{W}.webp" for t in themes_l],
               "citation": v["citation"]},
              {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _txt(a)}} for q, a in c["faq"]]}]}
    s = head(c["seo"], c["desc"], path, og, schema)
    s = s.replace('<meta name="twitter:card" content="summary_large_image">',
                  f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(c["seo"])}">'
                  f'<meta name="twitter:description" content="{e(c["desc"])}"><meta name="twitter:image" content="{og}">'
                  f'<meta property="og:image:width" content="{W}"><meta property="og:image:height" content="{W * 9 // 16}"><meta property="og:image:alt" content="{e(t0["alt"])}">')
    s = s.replace("</head>", f"<style>{V4_CSS}{v['css']}</style></head>")
    s += header("new-launches/")
    s += hero + themes + plan_sec + lower
    s += footer()
    s = s.replace("mid.css?v=", "mid.css?v=" + V4_V + "-").replace("mid.js?v=", "mid.js?v=" + V4_V + "-")
    write(path + "index.html", s)
    return c
