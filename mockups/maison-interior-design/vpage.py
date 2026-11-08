# Visual-first new-launch pages built from pages/<slug>.md (copy supplied by Edwin's team, 7 Nov 2026).
# Visible text is short; the full copy (captions, FAQ, caveats, sources) sits in collapsed accordions.
import re as _re
import markdown as _md

VWA = "https://wa.me/6593391185"

VPAGES = {
 "towner-residences": dict(
  kind="bto", hero="towner-residences-living-dining", layout="towner-residences-layout-4room",
  plan=("towner-residences-maison-plan", 1640, "Maison redrawn floor plan of a Towner Residences 4-room flat, for illustration",
        "https://assets.hdb.gov.sg/community/towner_residences/index.html"),
  v4=True,
  styles=dict(note="4-room first arrangement, 90 sqm internal / 93 sqm incl. A/C ledge.",
              src="https://btohq.sgp1.cdn.digitaloceanspaces.com/bto/aug-2021-bto/towner-residences.pdf#page=8"),
  tag="BTO · Kallang/Whampoa · Key date not yet confirmed",
  rooms=[("towner-residences-living-dining", "Living and dining: a clear route through a warm, compact layout."),
         ("towner-residences-kitchen", "Kitchen and service yard: follows the selected plan; joinery is a proposal."),
         ("towner-residences-master-bedroom", "Main bedroom: starts from the plan; verify your stack and measurements."),
         ("towner-residences-study", "Common bedroom as a study: the household shelter stays a shelter.")],
  layout_cap="Simplified redraw based on HDB brochure p.12. Not to scale.",
  glance=[dict(name="3-room", size="65 sqm internal (approx. 68 sqm incl. ledge)", beds="2 bedrooms",
               idea="Keep the dry kitchen and kitchen/utility clear to work in; adapt storage to your actual unit."),
          dict(name="4-room (two brochure arrangements)", size="90 sqm internal (approx. 93 sqm incl. ledge)", beds="3 bedrooms",
               idea="A common bedroom can double as a study; never use the household shelter as one.")],
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
 "the-myst": dict(
  kind="condo", hero="the-myst-living-dining", layout="the-myst-layout-b1",
  tag="Condo · Upper Bukit Timah · TOP obtained Sep 2026",
  rooms=[("the-myst-living-dining", "Living and dining: central space that ends at the balcony."),
         ("the-myst-kitchen", "Kitchen: open L-kitchen by the entry, behind the dining area."),
         ("the-myst-master-bedroom", "Main bedroom: window above the ledge, calm timber headboard wall."),
         ("the-myst-study", "Bedroom 2 as a study: a proposed reuse, not a separate study room.")],
  layout_cap="Simplified diagram based on the developer brochure, PDF p.8. Not to scale.",
  glance=[dict(name="2-bedroom Type B1", size="63 sqm / 678 sq ft", beds="2 bedrooms",
               idea="Use bedroom 2 as a study; keep the open L-kitchen and plan joinery around it.")],
  steps=[("Keys / access", "TOP obtained Sep 2026. Key and access appointments are not confirmed."),
         ("Defects", "Inspect and log defects; agree rectification and access."),
         ("Survey", "Survey the unit and freeze the scope."),
         ("Approvals", "Management requirements and any work-specific authority approvals."),
         ("Build", "Procure, build, test and inspect. 6–10 on-site weeks is an allowance, not a guarantee.")]),
 "canninghill-piers": dict(
  kind="condo", hero="canninghill-piers-living-dining", layout="canninghill-piers-layout-b1s",
  tag="Condo · River Valley · TOP obtained Oct 2026",
  rooms=[("canninghill-piers-living-dining", "Living and dining: living balcony beyond, kitchen near the entry."),
         ("canninghill-piers-kitchen", "Kitchen: compact open L-kitchen opening into the dining area."),
         ("canninghill-piers-master-bedroom", "Main bedroom: its own balcony, with the bath alongside."),
         ("canninghill-piers-study", "Ensuite study: a compact desk in the internal study, not a third bedroom.")],
  layout_cap="Simplified diagram based on the developer e-brochure, PDF p.31. Not to scale.",
  glance=[dict(name="2-bedroom + ensuite study Type B1(S)", size="77 sqm / 829 sq ft", beds="2 bedrooms + ensuite study",
               idea="Fit a compact built-in desk in the internal study; it has no external window on the plan.")],
  steps=[("Keys / access", "TOP obtained Oct 2026. Key and access appointments are not confirmed."),
         ("Defects", "Inspect and log defects; agree rectification and access."),
         ("Survey", "Survey the unit and freeze the scope."),
         ("Approvals", "Management requirements and any work-specific authority approvals."),
         ("Build", "Procure, build, test and inspect. 6–10 on-site weeks is an allowance, not a guarantee.")]),
 "shaw-tower": dict(
  kind="office", hero="shaw-tower-reception", layout="shaw-tower-layout-highzone", zones=True,
  tag="Office · Beach Road · TOP secured Jul 2026",
  rooms=[("shaw-tower-reception", "Reception: a reception and flexible-work zone as a proposal."),
         ("shaw-tower-open-office", "Open office: workstations on the column-free side-core plate."),
         ("shaw-tower-meeting-room", "Meeting room: room shape, size and partitions are proposals."),
         ("shaw-tower-utility-zone", "Utility zone: printer and storage along the core side; no new plumbing.")],
  layout_cap="Proposed zoning only, based on the Shaw Tower plans webpage. Doors and windows not drawn. Not to scale.",
  glance=[dict(name="Reception / flexible work", idea="Proposed zone near the entry; furniture and partitions to suit your lease plan."),
          dict(name="Workstations", idea="Proposed open zone on the column-free plate; the published test-fit is not a promised capacity."),
          dict(name="Meeting / office", idea="Meeting rooms and offices are published test-fit categories; sizes are proposals."),
          dict(name="Utility", idea="Server, compactor or printer rooms as the landlord names them; no claimed services capacity.")],
  plate=["Approx. 20,000 sq ft NLA (test-fit, subject to survey)", "3 m floor-to-ceiling", "150 mm raised floor", "Side core, column-free plate"],
  steps=[("Handover", "TOP secured Jul 2026. Your lease handover and access dates are not confirmed."),
         ("Defects", "Inspect the base build and log defects with the landlord."),
         ("Survey", "Survey the space against your lease-specific base plan."),
         ("Approvals", "Landlord fit-out rules plus any authority approvals your works need."),
         ("Build", "Procure, build, test and inspect. 8–12 weeks for a modest office is an allowance, not a guarantee.")]),
}
VPAGE_ON_HOLD = {"lumina-grand", "parc-point-tengah"}

def _txt(h):
    return " ".join(html.unescape(_re.sub(r"<[^>]+>", " ", h)).split())

def vimg(slug, name, alt, cls="", lazy=True, sizes="100vw", w=1920, h=1080):
    b = f"{BASE}images/new-launches/{slug}/{name}"
    return (f'<img class="{cls}" src="{b}.webp" srcset="{b}-960.webp 960w, {b}.webp 1920w" sizes="{sizes}" alt="{e(alt)}" '
            f'width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else " fetchpriority=\"high\""} decoding="async">')

def _glue(t):
    # the supplied copy sometimes loses spaces around numbers ("use6–10", "12weeks"); restore them outside URLs
    parts = _re.split(r"(\(https?://[^)]*\)|https?://\S+)", t)
    for i in range(0, len(parts), 2):
        x = _re.sub(r"(?<=[a-z]{3})(?=\d|[A-Z]\d)", " ", parts[i])
        parts[i] = _re.sub(r"(?<=\d)(?=[a-z]{3,}|[A-Z][a-z]{2,})", " ", x)
    return "".join(parts)

def parse_copy(slug):
    raw = open(os.path.join(HERE, "pages", slug + ".md"), encoding="utf-8").read()
    seo = _re.search(r"^SEO title:\s*(.+)$", raw, _re.M).group(1).strip()
    desc = _re.search(r"^Meta description:\s*(.+)$", raw, _re.M).group(1).strip()
    body = raw[raw.index("\n# ") + 1:]
    h1 = body.splitlines()[0][2:].strip()
    parts = _re.split(r"^## ", body, flags=_re.M)
    head_part, secs = parts[0], {p.split("\n", 1)[0].strip(): p.split("\n", 1)[1] for p in parts[1:]}
    conv = lambda t: _md.markdown(_glue(t.strip()), extensions=["tables"])
    lead = head_part.split("\n", 1)[1]
    lead = _re.sub(r"!\[[^\]]*\]\([^)]*\)", "", lead)
    rooms = [(k, conv(_re.sub(r"!\[[^\]]*\]\([^)]*\)", "", v))) for k, v in secs.items()
             if k not in ("FAQ and detailed planning notes", "Talk to Maison", "Sources")]
    faq_md = secs["FAQ and detailed planning notes"]
    faq = []
    for chunk in _re.split(r"^### ", faq_md, flags=_re.M)[1:]:
        q, a = chunk.split("\n", 1)
        faq.append((q.strip(), conv(a)))
    seen = set(); src_md = "\n".join(l for l in secs["Sources"].splitlines() if not (l.startswith("- ") and (l in seen or seen.add(l))))
    return dict(seo=seo, desc=desc, h1=h1, lead=conv(lead), rooms=rooms, faq=faq, sources=conv(src_md))

def _links(h):
    h = _re.sub(r'(?<![="])(https://[^\s<]+)', lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', h)
    return _re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', h)

ICON = {"size": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3h18v18H3zM3 9h6V3M15 21v-6h6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>',
        "beds": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 18V7M3 13h18v5M21 18v-3M6 13v-2.5A1.5 1.5 0 0 1 7.5 9h3A1.5 1.5 0 0 1 12 10.5V13" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>',
        "idea": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.5 10.9V16h7v-2.1A6 6 0 0 0 12 3Z" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>'}

def wa_btn(slug, cls="btn dark-b"):
    return f'<a class="{cls} vwa" href="{VWA}" data-cta="whatsapp" data-ref="{slug}"><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Z"/></svg>WhatsApp Maison</a>'

VSTY_CSS = '.vsty-btns{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}.vsty-btns button{min-height:44px;padding:0 18px;border:1px solid var(--ink);background:transparent;color:var(--ink);font:500 13px/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;cursor:pointer;flex:1 1 calc(50% - 8px)}.vsty-btns button[aria-pressed="true"]{background:var(--ink);color:#fff}@media(min-width:560px){.vsty-btns button{flex:0 0 auto}}.vsty-imgs{display:grid;gap:16px}.vsty-imgs figure{margin:0}.vsty-imgs img{display:block;width:100%;height:auto;aspect-ratio:16/9;background:var(--bg2)}.vsty-imgs figcaption{font-size:14px;color:var(--ink2);margin-top:8px}@media(min-width:900px){.vsty-imgs{grid-template-columns:1fr 1fr;gap:24px}}.vsty-src{font-size:13px;color:var(--mute);margin-top:12px}.vsty-src a,.vplan-link a{color:var(--brass);text-decoration:underline}.vplan{margin-top:14px}.vplan-img{display:block}.vplan-img img{display:block;width:100%;height:auto;aspect-ratio:1920/1640;border:1px solid var(--line);background:#f5f2ec}.vplan-link{margin-top:10px;font-size:15px}'

STYLES = ["Modern", "Luxury", "Scandi", "Japandi"]

def style_picker(slug, cfg, h1):
    st = cfg["styles"]
    b = f"{BASE}images/new-launches/{slug}/{slug}"
    btns = "".join(f'<button type="button" data-s="{x.lower()}" aria-pressed="{"true" if i == 0 else "false"}">{x}</button>' for i, x in enumerate(STYLES))
    def fig(room, label, alt):
        return (f'<figure><img src="{b}-modern-{room}.webp" srcset="{b}-modern-{room}-960.webp 960w, {b}-modern-{room}.webp 1920w" '
                f'sizes="(min-width:900px) 45vw, 100vw" width="1920" height="1080" alt="AI concept: Modern style {alt} for {e(h1)}" '
                f'data-room="{room}" data-alt="{alt}" decoding="async">'
                f'<figcaption><span class="vs-n">Modern</span> · {label}</figcaption></figure>')
    return (f'<style>{VSTY_CSS}</style><section class="vsec vsty"><div class="wrap"><h2 class="vh2">Choose your style</h2>'
            f'<p class="vsub">Same room, four styles. AI concepts, for illustration only; all cabinetry, furnishings and finishes are proposed.</p>'
            f'<div class="vsty-btns" role="group" aria-label="Interior style">{btns}</div>'
            f'<div class="vsty-imgs" data-base="{b}">{fig("living", "Living / dining", "living and dining")}{fig("bedroom", "Main bedroom", "main bedroom")}</div>'
            f'<p class="vsty-src">{e(st["note"])} Source: <a href="{st["src"]}" target="_blank" rel="noopener">HDB brochure (archive copy)</a></p></div></section>'
            """<script>(function(){var w=document.currentScript.previousElementSibling,g=w.querySelector('.vsty-imgs'),b=g.dataset.base;
w.querySelectorAll('.vsty-btns button').forEach(function(t){t.addEventListener('click',function(){var s=t.dataset.s,n=t.textContent;
w.querySelectorAll('.vsty-btns button').forEach(function(o){o.setAttribute('aria-pressed',o===t?'true':'false')});
g.querySelectorAll('img').forEach(function(i){var r=i.dataset.room,f=b+'-'+s+'-'+r;i.srcset=f+'-960.webp 960w, '+f+'.webp 1920w';i.src=f+'.webp';i.alt='AI concept: '+n+' style '+i.dataset.alt+' for '+document.querySelector('h1').textContent});
g.querySelectorAll('.vs-n').forEach(function(x){x.textContent=n})})})})()</script>""")

def vpage(slug):
    if VPAGES[slug].get("v4"):
        return vpage_v4(slug)
    c, cfg = parse_copy(slug), VPAGES[slug]
    path = f"new-launches/{slug}/"
    gal = "".join(f'<figure class="vg-card">{vimg(slug, n, "AI concept: " + cap.split(":")[0] + " for " + c["h1"], sizes="(min-width:900px) 45vw, 85vw")}'
                  f'<figcaption>{e(cap)} <span>AI concept, for illustration only</span></figcaption></figure>' for n, cap in cfg["rooms"])
    gsec = "" if cfg.get("picker2") else (f'<section class="vsec"><div class="wrap"><h2 class="vh2">Four concept {"zones" if cfg.get("zones") else "rooms"}</h2><p class="vsub">Plan-informed style studies, not exact reconstructions. Swipe to see all four.</p>\n'
                                          f'<div class="vgal">{gal}</div></div></section>')
    first_src = _re.search(r'href="([^"]+)"', c["lead"])
    glance = "".join(f'<article class="vgl"><h3>{e(g["name"])}</h3><ul>'
                     + (f'<li>{ICON["size"]}<span>{e(g["size"])}</span></li>' if g.get("size") else "")
                     + (f'<li>{ICON["beds"]}<span>{e(g["beds"])}</span></li>' if g.get("beds") else "")
                     + f'<li>{ICON["idea"]}<span>{e(g["idea"])}</span></li></ul></article>' for g in cfg["glance"])
    plate = ('<ul class="vplate">' + "".join(f'<li>{ICON["size"]}<span>{e(x)}</span></li>' for x in cfg["plate"]) + '</ul>') if cfg.get("plate") else ""
    if cfg.get("plan"):
        pn, ph, palt, plink = cfg["plan"]
        layout_html = (f'<div class="vplan"><a class="vplan-img" href="{BASE}images/new-launches/{slug}/{pn}.webp" target="_blank" rel="noopener">'
                       f'{vimg(slug, pn, palt, sizes="(min-width:1240px) 1160px, 100vw", h=ph).replace("AI concept: ", "")}</a>'
                       f'<p class="vplan-link"><a href="{plink}" target="_blank" rel="noopener">View official floor plan</a></p></div>')
    else:
        layout_html = (f'<figure class="vlay">{vimg(slug, cfg["layout"], "Simplified layout diagram for " + c["h1"], sizes="(min-width:1240px) 1160px, 100vw", h=1340)}'
                       f'<figcaption>{e(cfg["layout_cap"])} ' + (('<a href="' + first_src.group(1) + '" target="_blank" rel="noopener">Source</a>') if first_src else '') + '</figcaption></figure>')
    _lh = "Proposed zoning (not a lease plan)" if cfg.get("zones") else "The layout these concepts use"
    lsec = "" if cfg.get("picker2") else f'<section class="vsec"><div class="wrap"><h2 class="vh2">{_lh}</h2>\n{layout_html}</div></section>'
    steps = "".join(f'<li><span class="sn">{i+1:02d}</span><h3>{e(t)}</h3><p>{e(x)}</p></li>' for i, (t, x) in enumerate(cfg["steps"]))
    faqs = "".join(f'<details class="qa"><summary><h3>{e(q)}</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq">{_links(a)}</div></details>' for q, a in c["faq"])
    notes = "".join(f"<h4>{e(k)}</h4>{_links(v)}" for k, v in c["rooms"])
    gk, gs = KINDS[cfg["kind"]]
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("New launches", "new-launches/"), (c["h1"], path)]),
              {"@type": "Article", "headline": c["h1"], "description": c["desc"], "datePublished": "2026-11-07", "dateModified": "2026-11-07",
               "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "mainEntityOfPage": DOMAIN + "/" + path,
               "image": [DOMAIN + f"/images/new-launches/{slug}/{n}.webp" for n, _ in cfg["rooms"]] + [DOMAIN + f"/images/new-launches/{slug}/{(cfg['plan'][0] if cfg.get('plan') else cfg['layout'])}.webp"],
               "citation": _re.findall(r'href="(https://[^"]+)"', c["sources"])},
              {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": _txt(a)}} for q, a in c["faq"]]}]}
    s = head(c["seo"], c["desc"], path, f"{BASE}images/new-launches/{slug}/{cfg['hero']}.webp", schema)
    s += header("new-launches/")
    s += f"""<section class="vhero">{vimg(slug, cfg['hero'], "AI concept: " + cfg['rooms'][0][1].split(":")[0].lower() + " for " + c['h1'], cls="vh-img", lazy=False)}
<div class="vh-txt"><div class="wrap"><p class="vh-tag">{e(cfg['tag'])}</p><h1>{e(c['h1'])}</h1></div></div></section>
<div class="wrap vh-cta">{wa_btn(slug)}<a class="link" href="{BASE}services/{gs}/">{e(GBY[gs]['short'])} guide</a></div>
{picker2(slug, c['h1'], wa_btn(slug)) if cfg.get('picker2') else (style_picker(slug, cfg, c['h1']) if cfg.get('styles') else '')}
{gsec}
{lsec}
<section class="vsec"><div class="wrap"><h2 class="vh2">{"Zones at a glance" if cfg.get("zones") else "Layout at a glance"}</h2>{plate}<div class="vgls">{glance}</div></div></section>
<section class="vsec"><div class="wrap"><h2 class="vh2">{"From handover to move-in" if cfg.get("zones") else "From keys to move-in"}</h2><ol class="vsteps">{steps}</ol></div></section>
<section class="vsec vfaq"><div class="wrap narrow"><h2 class="vh2">Details, caveats and sources</h2>
<details class="qa"><summary><h3>About this page and the images</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq">{_links(c['lead'])}{notes}</div></details>
{faqs}
<details class="qa"><summary><h3>Sources</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq">{_links(c['sources'])}</div></details>
<div class="vh-cta end">{wa_btn(slug)}</div></div></section>"""
    s += footer()
    if cfg.get("picker2"):
        s = s.replace("mid.css?v=", "mid.css?v=" + PICKER2_V + "-").replace("mid.js?v=", "mid.js?v=" + PICKER2_V + "-")
        s = _re.sub(r'(' + _re.escape(BASE) + r'images/new-launches/[\w/-]+\.webp)(?!\?)', r'\1?v=' + PICKER2_V, s)
    write(path + "index.html", s)
    return c
