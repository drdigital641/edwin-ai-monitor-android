# Visual-first new-launch pages built from pages/<slug>.md (copy supplied by Edwin's team, 7 Nov 2026).
# Visible text is short; the full copy (captions, FAQ, caveats, sources) sits in collapsed accordions.
import re as _re
import markdown as _md

VWA = "https://wa.me/6593391185"

VPAGES = {
 "towner-residences": dict(
  kind="bto", hero="towner-residences-living-dining", layout="towner-residences-layout-4room",
  tag="BTO · Kallang/Whampoa · Key date not yet confirmed",
  rooms=[("towner-residences-living-dining", "Living and dining: a clear route through a warm, compact layout."),
         ("towner-residences-kitchen", "Kitchen and service yard: follows the selected plan; joinery is a proposal."),
         ("towner-residences-master-bedroom", "Main bedroom: starts from the plan; verify your stack and measurements."),
         ("towner-residences-study", "Common bedroom as a study: the household shelter stays a shelter.")],
  layout_cap="Simplified redraw based on HDB brochure p.12. Not to scale.",
  glance=[dict(name="4-room, first brochure arrangement", size="90 sqm internal (93 sqm incl. ledge)", beds="3 bedrooms",
               idea="Turn the middle common bedroom into a study; never use the household shelter as one.")],
  steps=[("Keys", "Collect on your own HDB date. No project-wide key date is confirmed."),
         ("Defects", "Inspect and report defects, then coordinate rectification."),
         ("Survey", "Measure the home against your approved plan and OCS selections."),
         ("Approvals", "Confirm HDB renovation and permitted-work requirements."),
         ("Build", "Procure and build. Any 8–12-week example is a planning allowance, not a guarantee.")]),
 "norwood-grand": dict(
  kind="condo", hero="norwood-grand-living-dining", layout="norwood-grand-layout-b1",
  tag="Condo · Woodlands · TOP obtained Aug 2026",
  rooms=[("norwood-grand-living-dining", "Living and dining: central space with the balcony beyond."),
         ("norwood-grand-kitchen", "Kitchen: compact open kitchen by the entry, as on the plan."),
         ("norwood-grand-master-bedroom", "Main bedroom: warm timber wardrobe and a calm palette."),
         ("norwood-grand-study", "Bedroom 2 as a study, with a movable desk and no ensuite added.")],
  layout_cap="Simplified diagram based on the developer brochure, PDF p.16. Not to scale.",
  glance=[dict(name="2-bedroom Type B1", size="58 sqm / 624 sq ft", beds="2 bedrooms",
               idea="Convert bedroom 2 into a study with a movable desk; keep the supplied wardrobe.")],
  steps=[("Keys / access", "TOP obtained Aug 2026. Key and access appointments are not confirmed."),
         ("Defects", "Inspect and log defects; agree rectification and access."),
         ("Survey", "Survey the unit and freeze the scope."),
         ("Approvals", "Management requirements and any work-specific authority approvals."),
         ("Build", "Procure, build, test and inspect. 6–10 on-site weeks is an allowance, not a guarantee.")]),
}
VPAGE_ON_HOLD = {"lumina-grand", "parc-point-tengah"}

def _txt(h):
    return " ".join(html.unescape(_re.sub(r"<[^>]+>", " ", h)).split())

def vimg(slug, name, alt, cls="", lazy=True, sizes="100vw", w=1920, h=1080):
    b = f"{BASE}images/new-launches/{slug}/{name}"
    return (f'<img class="{cls}" src="{b}.webp" srcset="{b}-960.webp 960w, {b}.webp 1920w" sizes="{sizes}" alt="{e(alt)}" '
            f'width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async">')

def parse_copy(slug):
    raw = open(os.path.join(HERE, "pages", slug + ".md"), encoding="utf-8").read()
    seo = _re.search(r"^SEO title:\s*(.+)$", raw, _re.M).group(1).strip()
    desc = _re.search(r"^Meta description:\s*(.+)$", raw, _re.M).group(1).strip()
    body = raw[raw.index("\n# ") + 1:]
    h1 = body.splitlines()[0][2:].strip()
    parts = _re.split(r"^## ", body, flags=_re.M)
    head_part, secs = parts[0], {p.split("\n", 1)[0].strip(): p.split("\n", 1)[1] for p in parts[1:]}
    conv = lambda t: _md.markdown(t.strip(), extensions=["tables"])
    lead = head_part.split("\n", 1)[1]
    lead = _re.sub(r"!\[[^\]]*\]\([^)]*\)", "", lead)
    rooms = [(k, conv(_re.sub(r"!\[[^\]]*\]\([^)]*\)", "", v))) for k, v in secs.items()
             if k not in ("FAQ and detailed planning notes", "Talk to Maison", "Sources")]
    faq_md = secs["FAQ and detailed planning notes"]
    faq = []
    for chunk in _re.split(r"^### ", faq_md, flags=_re.M)[1:]:
        q, a = chunk.split("\n", 1)
        faq.append((q.strip(), conv(a)))
    src_md = secs["Sources"]
    return dict(seo=seo, desc=desc, h1=h1, lead=conv(lead), rooms=rooms, faq=faq, sources=conv(src_md))

def _links(h):
    h = _re.sub(r'(?<![="])(https://[^\s<]+)', lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', h)
    return _re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', h)

ICON = {"size": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3h18v18H3zM3 9h6V3M15 21v-6h6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>',
        "beds": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 18V7M3 13h18v5M21 18v-3M6 13v-2.5A1.5 1.5 0 0 1 7.5 9h3A1.5 1.5 0 0 1 12 10.5V13" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>',
        "idea": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9V16h7v-2.1A6 6 0 0 0 12 3Z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'}

def wa_btn(slug, cls="btn dark-b"):
    return f'<a class="{cls} vwa" href="{VWA}" data-cta="whatsapp" data-ref="{slug}"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Z"/></svg>WhatsApp Maison</a>'

def vpage(slug):
    c, cfg = parse_copy(slug), VPAGES[slug]
    path = f"new-launches/{slug}/"
    gal = "".join(f'<figure class="vg-card">{vimg(slug, n, "AI concept: " + cap.split(":")[0] + " for " + c["h1"], sizes="(min-width:900px) 45vw, 85vw")}'
                  f'<figcaption>{e(cap)} <span>AI concept, for illustration only</span></figcaption></figure>' for n, cap in cfg["rooms"])
    first_src = _re.search(r'href="([^"]+)"', c["lead"])
    glance = "".join(f'<article class="vgl"><h3>{e(g["name"])}</h3><ul>'
                     + (f'<li>{ICON["size"]}<span>{e(g["size"])}</span></li>' if g.get("size") else "")
                     + (f'<li>{ICON["beds"]}<span>{e(g["beds"])}</span></li>' if g.get("beds") else "")
                     + f'<li>{ICON["idea"]}<span>{e(g["idea"])}</span></li></ul></article>' for g in cfg["glance"])
    steps = "".join(f'<li><span class="sn">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(x)}</p></li>' for i, (t, x) in enumerate(cfg["steps"]))
    faqs = "".join(f'<details class="qa"><summary><h3>{e(q)}</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq">{_links(a)}</div></details>' for q, a in c["faq"])
    notes = "".join(f"<h4>{e(k)}</h4>{_links(v)}" for k, v in c["rooms"])
    gk, gs = KINDS[cfg["kind"]]
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("New launches", "new-launches/"), (c["h1"], path)]),
              {"@type": "Article", "headline": c["h1"], "description": c["desc"], "datePublished": "2026-11-07", "dateModified": "2026-11-07",
               "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "mainEntityOfPage": DOMAIN + "/" + path,
               "image": [DOMAIN + f"/images/new-launches/{slug}/{n}.webp" for n, _ in cfg["rooms"]] + [DOMAIN + f"/images/new-launches/{slug}/{cfg['layout']}.webp"],
               "citation": _re.findall(r'href="(https://[^"]+)"', c["sources"])},
              {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _txt(a)}} for q, a in c["faq"]]}]}
    s = head(c["seo"], c["desc"], path, f"{BASE}images/new-launches/{slug}/{cfg['hero']}.webp", schema)
    s += header("new-launches/")
    s += f"""<section class="vhero">{vimg(slug, cfg['hero'], "AI concept: living and dining for " + c['h1'], cls="vh-img", lazy=False)}
<div class="vh-txt"><div class="wrap"><p class="vh-tag">{e(cfg['tag'])}</p><h1>{e(c['h1'])}</h1></div></div></section>
<div class="wrap vh-cta">{wa_btn(slug)}<a class="link" href="{BASE}services/{gs}/">{e(GBY[gs]['short'])} guide</a></div>
<section class="vsec"><div class="wrap"><h2 class="vh2">Four concept rooms</h2><p class="vsub">Plan-informed style studies, not exact reconstructions. Swipe to see all four.</p>
<div class="vgal">{gal}</div></div></section>
<section class="vsec"><div class="wrap"><h2 class="vh2">The layout these concepts use</h2>
<figure class="vlay">{vimg(slug, cfg['layout'], "Simplified layout diagram for " + c['h1'], sizes="(min-width:1240px) 1160px, 100vw", h=1340)}
<figcaption>{e(cfg['layout_cap'])} {('<a href="' + first_src.group(1) + '" target="_blank" rel="noopener">Source</a>') if first_src else ''}</figcaption></figure></div></section>
<section class="vsec"><div class="wrap"><h2 class="vh2">Layout at a glance</h2><div class="vgls">{glance}</div></div></section>
<section class="vsec"><div class="wrap"><h2 class="vh2">From keys to move-in</h2><ol class="vsteps">{steps}</ol></div></section>
<section class="vsec vfaq"><div class="wrap narrow"><h2 class="vh2">Details, caveats and sources</h2>
<details class="qa"><summary><h3>About this page and the images</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq">{_links(c['lead'])}{notes}</div></details>
{faqs}
<details class="qa"><summary><h3>Sources</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq">{_links(c['sources'])}</div></details>
<div class="vh-cta end">{wa_btn(slug)}</div></div></section>"""
    s += footer()
    write(path + "index.html", s)
    return c
