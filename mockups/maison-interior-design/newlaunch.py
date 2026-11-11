# New-launch pages, template first (11 Nov 2026).
# One JSON file per project in data/new-launches/<slug>.json  ->  /new-launches/<slug>/index.html
# Header, footer, WhatsApp button, breadcrumb and schema come from the shared helpers in build.py,
# so one edit here (or in build.py) updates every project page. Format: docs/new-launch-data-format.md
# exec'd by launches.py, after launches_guides.py (GUIDES) and the type-level DEFECTS / RULES / TL tables.
import glob, re as _re
import markdown as _md

NL_DIR = os.path.join(HERE, "data", "new-launches")
NL_TYPES = ["Condo", "EC", "BTO", "HDB", "Landed", "Commercial"]
NL_REGIONS = ["Central", "East", "North", "North-East", "West", "Islandwide"]
NL_GUIDES = ["bto", "condo", "ec", "landed", "office", "retail"]
NL_TYPE_GUIDE = {"Condo": "condo", "EC": "ec", "BTO": "bto", "HDB": "bto", "Landed": "landed", "Commercial": "office"}
NL_NOT = "Not confirmed"          # a required fact we could not confirm: kept in the data, not shown on the page
NL_NOTE = "Concept design by Maison, not the actual unit"
NL_AI = "AI-generated style concept; layouts, fittings and views are illustrative."
NL_DEFAULT_OG = "62-Havelock-Road-Living-1-small-1024x683.jpg"

# field -> (kind, required). kind: str, list, int, "img" (image object), "list:<item fields>"
NL_REQ = ["name", "slug", "type", "area", "region", "developer", "tenure", "top", "unit_mix", "official_site",
          "sources", "nearby_hints", "intro", "faq", "keywords"]
NL_OPT = ["h1", "eyebrow", "hero_whatsapp_label", "facts_after", "district", "label", "top_label", "facts", "facts_note", "title", "description", "whatsapp_text", "hero_whatsapp_text", "hero",
          "renders", "renders_heading", "renders_intro", "renders_note",
          "floor_plans", "plans_heading", "plans_intro", "plans_note",
          "unit_tips", "unit_tips_heading", "unit_tips_note", "sections", "gallery", "gallery_heading",
          "steps", "steps_heading", "timeline_note", "guide", "cta_text", "reviewed", "date_published", "date_modified", "hub_image"]
NL_ITEM = {  # list fields: required keys / optional keys of each item
    "sources": (["label", "url"], ["nofollow"]),
    "faq": (["q", "a"], []),
    "facts": (["label", "value"], ["link_label", "link_url"]),
    "renders": (["image", "width", "height", "alt"], ["image_small", "style", "room", "title", "text", "whatsapp_text"]),
    "floor_plans": (["image", "width", "height", "alt", "caption", "credit"], ["credit_url", "credit_link_text", "title"]),
    "gallery": (["image", "width", "height", "alt"], ["image_small", "caption"]),
    "unit_tips": (["unit", "tip"], ["size", "bedrooms"]),
    "sections": (["heading", "text"], ["bullets"]),
    "steps": (["title", "text"], ["duration"]),
}
NL_IMG = (["image", "width", "height", "alt"], ["image_small"])
NL_BLANK_OK = ("developer", "tenure", "top", "unit_mix", "official_site")  # may be "" (or "Not confirmed"): not shown

def _nl_h1(p):
    # homes: "Renovation & Interior Design"; shops, offices and other commercial space: "Fit-Out & Interior Design"
    return p.get("h1") or f'{p["name"]} {"Fit-Out" if _nl_work(p) == "fit-out" else "Renovation"} & Interior Design'

def _nl_title(p):
    return p.get("title") or f'{_nl_h1(p)} | {p["area"]} | Maison'

def _nl_desc(p):
    return p.get("description") or (f'{p["name"]} renovation and interior design ideas: key facts, what owners change, '
                                    f'handover checks and a timeline. WhatsApp Maison.')

def _nl_guide(p):
    return p.get("guide") or NL_TYPE_GUIDE[p["type"]]

def _nl_work(p):
    return "fit-out" if _nl_guide(p) in ("office", "retail") else "renovation"

def _nl_wa_text(p):
    return p.get("whatsapp_text") or f"Hi Maison, I’m planning my {p['name']} {_nl_work(p)}. Can we discuss my layout?"

def _nl_check_img(o, where, err):
    path = o.get("image", "")
    if not isinstance(path, str) or not path.startswith(("/images/", "/img/")):
        err.append(f"{where}.image must be a root path under /images/ or /img/ (got {path!r})"); return
    if not path.endswith(".webp"): err.append(f"{where}.image must be a .webp file ({path})")
    if not os.path.isfile(os.path.join(HERE, path.lstrip("/"))): err.append(f"{where}.image file not found in the repo: {path}")
    sm = o.get("image_small")
    if sm and not os.path.isfile(os.path.join(HERE, sm.lstrip("/"))): err.append(f"{where}.image_small file not found: {sm}")
    for k in ("width", "height"):
        if not isinstance(o.get(k), int) or o[k] <= 0: err.append(f"{where}.{k} must be a whole number of pixels")
    if not str(o.get("alt", "")).strip(): err.append(f"{where}.alt is empty")

def nl_validate(p, fname):
    """Return a list of problems with one project's data (empty list = OK)."""
    err = []
    if not isinstance(p, dict): return [f"{fname}: the file must hold one JSON object"]
    for k in p:
        if k not in NL_REQ and k not in NL_OPT: err.append(f"unknown field '{k}' (typo?)")
    for k in NL_REQ:
        v = p.get(k)
        if v is None or (isinstance(v, str) and not v.strip() and k not in NL_BLANK_OK) or (isinstance(v, list) and k != "nearby_hints" and not v):
            err.append(f"required field '{k}' is missing or empty")
        elif k in ("sources", "nearby_hints", "faq", "keywords") and not isinstance(v, list):
            err.append(f"'{k}' must be a list")
        elif k not in ("sources", "nearby_hints", "faq", "keywords") and not isinstance(v, str):
            err.append(f"'{k}' must be text")
    if err: return err
    stem = os.path.splitext(os.path.basename(fname))[0]
    if not _re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", p["slug"]): err.append("slug must be lower-case words joined by hyphens")
    if p["slug"] != stem: err.append(f"slug '{p['slug']}' must match the file name '{stem}.json'")
    if p["type"] not in NL_TYPES: err.append(f"type must be one of {', '.join(NL_TYPES)}")
    if p["region"] not in NL_REGIONS: err.append(f"region must be one of {', '.join(NL_REGIONS)}")
    if p.get("guide") and p["guide"] not in NL_GUIDES: err.append(f"guide must be one of {', '.join(NL_GUIDES)}")
    if p["official_site"] not in (NL_NOT, "") and not p["official_site"].startswith(("https://", "http://")):
        err.append(f"official_site must be a full URL, \"{NL_NOT}\" or empty")
    for k, (req, opt) in NL_ITEM.items():
        if k not in p: continue
        if not isinstance(p[k], list): err.append(f"'{k}' must be a list"); continue
        for i, it in enumerate(p[k]):
            w = f"{k}[{i}]"
            if not isinstance(it, dict): err.append(f"{w} must be an object"); continue
            for f in req:
                if it.get(f) in (None, "") and f not in ("width", "height"): err.append(f"{w}.{f} is missing")
            for f in it:
                if f not in req and f not in opt: err.append(f"{w}: unknown field '{f}'")
            if "image" in req: _nl_check_img(it, w, err)
            if k == "sources" and not str(it.get("url", "")).startswith(("https://", "http://")): err.append(f"{w}.url must be a full URL")
    if "hero" in p: _nl_check_img(p["hero"], "hero", err)
    if "hub_image" in p: _nl_check_img(p["hub_image"], "hub_image", err)
    if not all(isinstance(x, str) and x.strip() for x in p["keywords"]): err.append("keywords must be a list of text")
    elif not err:
        kw = p["keywords"][0].lower()
        first_para = p["intro"].strip().split("\n\n")[0].lower()
        for where, txt in (("title", _nl_title(p)), ("H1", _nl_h1(p)), ("first paragraph of intro", first_para)):
            if kw not in txt.lower(): err.append(f"main keyword '{p['keywords'][0]}' (keywords[0]) is not in the {where}")
    if len(_nl_desc(p)) > 155: err.append(f"description is {len(_nl_desc(p))} characters; keep it to 155 or fewer")
    if any(not isinstance(x, str) for x in p["nearby_hints"]): err.append("nearby_hints must be a list of project slugs")
    return err

def nl_load(dirs=None):
    """Load and check every project file. Stops the build with a full list of problems."""
    files = []
    for d in (dirs or [NL_DIR]):
        files += sorted(glob.glob(os.path.join(d, "*.json")))
    projects, problems, seen = [], [], {}
    for f in files:
        try:
            p = json.load(open(f, encoding="utf-8"))
        except Exception as x:
            problems.append(f"{f}: not valid JSON ({x})"); continue
        errs = nl_validate(p, f)
        if errs:
            problems += [f"{os.path.relpath(f, HERE)}: {x}" for x in errs]; continue
        if p["slug"] in seen:
            problems.append(f"{f}: slug '{p['slug']}' is also used by {seen[p['slug']]}"); continue
        seen[p["slug"]] = f
        projects.append(p)
    if problems:
        raise SystemExit("New-launch data check failed (nothing was built):\n  " + "\n  ".join(problems))
    slugs = set(seen) | {os.path.splitext(os.path.basename(x))[0] for x in glob.glob(os.path.join(NL_DIR, "*.json"))}
    for p in projects:
        for h in p["nearby_hints"]:
            if h not in slugs: print(f"note: {p['slug']}: nearby hint '{h}' has no page yet (skipped)")
    return projects

# ---------------------------------------------------------------- text helpers
def _nl_links(h):
    # external links open in a new tab; internal links stay as they are
    return _re.sub(r'<a href="(https?://[^"]+)"(?![^>]*target=)', r'<a href="\1" target="_blank" rel="noopener"', h)

def _nl_md(t):
    return _nl_links(_md.markdown(t.strip()))

def _nl_inline(t):
    h = _nl_md(t)
    return h[3:-4] if h.startswith("<p>") and h.endswith("</p>") and h.count("<p>") == 1 else h

def _nl_plain(t):
    return " ".join(html.unescape(_re.sub(r"<[^>]+>", " ", _md.markdown(t))).split())

def _nl_img(o, sizes, lazy=True, cls=""):
    small = o.get("image_small")
    srcset = f' srcset="{small} {_nl_w(small, o)}w, {o["image"]} {o["width"]}w" sizes="{sizes}"' if small else ""
    return (f'<img{f" class={chr(34)}{cls}{chr(34)}" if cls else ""} src="{o["image"]}"{srcset} width="{o["width"]}" height="{o["height"]}" '
            f'alt="{e(o["alt"])}" decoding="async"' + (' loading="lazy"' if lazy else ' fetchpriority="high"') + '>')

def _nl_w(small, o):
    m = _re.search(r"-(\d{3,4})\.webp$", small)
    return m.group(1) if m else str(o["width"] // 2)

NL_WA_ICON = ('<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Z"/></svg>')

def _nl_wa(label, msg, ref, p, cls="nlp-wa"):
    return (f'<a class="{cls}" href="{wa(msg)}" data-cta="whatsapp" data-ref="{ref}" data-path="{BASE}new-launches/{p["slug"]}/" rel="noopener">'
            f'{NL_WA_ICON}<span>{e(label)}</span></a>')

def _nl_shown(v):
    return v and v.strip() != NL_NOT

def _nl_hero(p):
    if p.get("hero"): return p["hero"]
    if p.get("renders"): return p["renders"][0]
    if p.get("gallery"): return p["gallery"][0]
    return None

def _nl_card_img(p):
    if p.get("hub_image"): return p["hub_image"]
    h = _nl_hero(p)
    if not h: return None
    if h.get("image_small"):
        return dict(image=h["image_small"], width=int(_nl_w(h["image_small"], h)), height=round(int(_nl_w(h["image_small"], h)) * h["height"] / h["width"]), alt=h["alt"])
    return h

# ---------------------------------------------------------------- nearby projects
def nl_nearby(p, projects, n=3):
    """Homes with homes, commercial with commercial. Then hints, same district, same area, same region, same type."""
    biz = lambda q: q["type"] == "Commercial"
    others = [q for q in projects if q["slug"] != p["slug"] and biz(q) == biz(p)]
    by = {q["slug"]: q for q in others}
    def rank(q):
        if q["slug"] in p["nearby_hints"]: return (0, p["nearby_hints"].index(q["slug"]))
        if p.get("district") and q.get("district") == p["district"]: return (1, 0)
        if q["area"] == p["area"]: return (2, 0)
        if q["region"] == p["region"]: return (3, 0 if q["type"] == p["type"] else 1)
        if q["type"] == p["type"]: return (4, 0)
        return (5, 0)
    return sorted(others, key=lambda q: (rank(q), q["name"]))[:n]

def nl_card(q, cls="lc"):
    im = _nl_card_img(q)
    tag = " · ".join(x for x in (q.get("label") or q["type"], q["area"]) if x)
    fig = f'<figure>{_nl_img(im, "(min-width:900px) 30vw, 100vw")}</figure>' if im else ""
    line = (q["top"].split(". ")[0].rstrip(".") + ".") if _nl_shown(q["top"]) else "Renovation planning notes for new owners."
    return (f'<a class="{cls}{" lc-img" if im else ""}" href="{BASE}new-launches/{q["slug"]}/" data-kind="{e(q["type"])}">{fig}'
            f'<span class="tag">{e(tag)}</span><h3>{e(q["name"])} <em>{e(q["area"])}</em></h3>'
            f'<p>{e(line)}</p><span class="more">{"See the concepts" if q.get("renders") else "Read the guide"}</span></a>')

# ---------------------------------------------------------------- one project page
def nl_page(p, projects):
    slug, name = p["slug"], p["name"]
    path = f"new-launches/{slug}/"
    g = _nl_guide(p)
    gslug = KINDS[g][1]
    work = _nl_work(p)
    h1 = _nl_h1(p)
    hero = _nl_hero(p)
    msg = _nl_wa_text(p)
    # hero
    hero_fig = (f'<figure class="nlp-hero-f">{_nl_img(hero, "(min-width:1100px) 680px, 100vw", lazy=False)}'
                + (f'<figcaption><b>{NL_NOTE}</b><span>{NL_AI}</span></figcaption>' if hero in p.get("renders", []) else
                   (f'<figcaption>{e(hero.get("caption", ""))}</figcaption>' if hero.get("caption") else "")) + '</figure>') if hero else ""
    eb = p.get("eyebrow") or " · ".join(x for x in (p.get("label") or p["type"], p["area"] if p["area"] != p["region"] else "", p["region"] + ("" if p["region"] == "Islandwide" else " region")) if x)
    s_hero = (f'<nav class="wrap nlp-crumbs" aria-label="Breadcrumb"><a href="{BASE}">Home</a><span aria-hidden="true">/</span>'
              f'<a href="{BASE}new-launches/">New launches</a><span aria-hidden="true">/</span><span aria-current="page">{e(name)}</span></nav>'
              f'<section class="nlp-hero{" nlp-hero-img" if hero else ""}"><div class="wrap nlp-hero-g"><div class="nlp-hero-t">'
              f'<p class="nlp-eb">{e(eb)}</p><h1>{e(h1)}</h1><div class="nlp-intro">{_nl_md(p["intro"])}</div>'
              f'<div class="nlp-cta-row">{_nl_wa(p.get("hero_whatsapp_label") or ("WhatsApp Maison about " + name), p.get("hero_whatsapp_text") or msg, slug + "-hero", p)}'
              f'<a class="link" href="{BASE}services/{gslug}/">{e(GBY[gslug]["short"])} guide</a></div></div>{hero_fig}</div></section>')
    # key facts (definition list of cards: stacks on phones, no tables)
    rows = [("Type", p.get("label") or p["type"]), ("Developer", p["developer"]), ("Tenure", p["tenure"]),
            (p.get("top_label") or "TOP", p["top"]), ("Unit mix", p["unit_mix"]),
            ("Area", p["area"] + (f' ({p["district"]})' if p.get("district") and not p["area"].startswith("District") else "")), ("Region", p["region"])]
    facts = "".join(f'<div><dt>{e(a)}</dt><dd>{e(b)}</dd></div>' for a, b in rows if _nl_shown(b))
    facts += "".join(f'<div><dt>{e(f["label"])}</dt><dd>{e(f["value"])}'
                     + (f' <a href="{f["link_url"]}" target="_blank" rel="noopener">{e(f.get("link_label") or "Source")}</a>' if f.get("link_url") else "")
                     + '</dd></div>' for f in p.get("facts", []) if _nl_shown(f["value"]))
    if _nl_shown(p["official_site"]):
        host = _re.sub(r"^https?://(www\.)?", "", p["official_site"]).split("/")[0]
        facts += f'<div><dt>Official site</dt><dd><a href="{p["official_site"]}" target="_blank" rel="nofollow noopener">{e(host)}</a></dd></div>'
    s_facts = (f'<section class="nlp-s nlp-facts-s"><div class="wrap"><h2 class="nlp-h2">{e(name)} at a glance</h2>'
               f'<dl class="nlp-facts">{facts}</dl>' + (f'<div class="nlp-note">{_nl_md(p["facts_note"])}</div>' if p.get("facts_note") else "") + f'<p class="nlp-small">Facts from the sources listed at the end of this page.</p></div></section>')
    # concept renders
    s_rend = ""
    if p.get("renders"):
        arts = ""
        for i, r in enumerate(p["renders"]):
            k = " · ".join(x for x in (r.get("style"), r.get("room")) if x)
            label = f'Discuss {r["style"]} on WhatsApp' if r.get("style") else "Discuss this look on WhatsApp"
            rmsg = r.get("whatsapp_text") or (f'Hi Maison, I’m interested in the {r["style"]} {(r.get("room") or "").lower()} concept for my {name} unit. Can we discuss my layout?'.replace("  ", " ") if r.get("style") else msg)
            rid = _re.sub(r"[^a-z0-9]+", "-", (r.get("style") or f"concept-{i+1}").lower()).strip("-")
            arts += (f'<article class="nlp-render" id="{rid}"><figure>{_nl_img(r, "(min-width:900px) 56vw, 100vw")}'
                     f'<figcaption><b>{NL_NOTE}</b><span>{NL_AI}</span></figcaption></figure><div class="nlp-render-t">'
                     + (f'<p class="nlp-k">{e(k)}</p>' if k else "")
                     + (f'<h3>{e(r["title"])}</h3>' if r.get("title") else f'<h3>{e(k or name + " concept")}</h3>')
                     + (f'<p>{_nl_inline(r["text"])}</p>' if r.get("text") else "")
                     + _nl_wa(label, rmsg, f"{slug}-{rid}", p) + '</div></article>')
        s_rend = (f'<section class="nlp-s nlp-renders"><div class="wrap"><h2 class="nlp-h2">{e(p.get("renders_heading") or name + " interior design concepts")}</h2>'
                  + (f'<p class="nlp-sub">{_nl_inline(p["renders_intro"])}</p>' if p.get("renders_intro") else "")
                  + (f'<p class="nlp-small">{_nl_inline(p["renders_note"])}</p>' if p.get("renders_note") else "")
                  + f'<div class="nlp-render-list">{arts}</div></div></section>')
    # floor plans
    s_plans = ""
    if p.get("floor_plans"):
        figs = ""
        for f in p["floor_plans"]:
            cr = e(f["credit"])
            if f.get("credit_url"):
                lt = f.get("credit_link_text") or f["credit"]
                cr = e(f["credit"]).replace(e(lt), f'<a href="{f["credit_url"]}" target="_blank" rel="nofollow noopener">{e(lt)}</a>', 1)
            figs += (f'<figure class="nlp-plan"><a class="nlp-zoom" href="{f["image"]}" target="_blank" rel="noopener" aria-label="Open the full-size {e(f.get("title") or "floor plan")}">'
                     f'{_nl_img(f, "(min-width:900px) 760px, 100vw")}<span class="nlp-zl" aria-hidden="true">Tap to enlarge ↗</span></a>'
                     f'<figcaption><b>{cr}</b>{_nl_inline(f["caption"])}</figcaption></figure>')
        s_plans = (f'<section class="nlp-s nlp-plans-s"><div class="wrap"><h2 class="nlp-h2">{e(p.get("plans_heading") or name + " floor plans")}</h2>'
                   + (f'<p class="nlp-sub">{_nl_inline(p["plans_intro"])}</p>' if p.get("plans_intro") else "")
                   + f'<div class="nlp-plans">{figs}</div>'
                   + (f'<div class="nlp-small">{_nl_md(p["plans_note"])}</div>' if p.get("plans_note") else "") + '</div></section>')
    # unit-type tips
    s_tips = ""
    if p.get("unit_tips"):
        cards = "".join(f'<article class="nlp-tip"><h3>{e(t["unit"])}</h3>'
                        + (f'<p class="nlp-tip-m">{e(" · ".join(x for x in (t.get("size"), t.get("bedrooms")) if x))}</p>' if (t.get("size") or t.get("bedrooms")) else "")
                        + f'<p>{_nl_inline(t["tip"])}</p></article>' for t in p["unit_tips"])
        s_tips = (f'<section class="nlp-s"><div class="wrap"><h2 class="nlp-h2">{e(p.get("unit_tips_heading") or "Layouts and renovation ideas")}</h2>'
                  f'<div class="nlp-tips">{cards}</div>'
                  + (f'<p class="nlp-small">{_nl_inline(p["unit_tips_note"])}</p>' if p.get("unit_tips_note") else "") + '</div></section>')
    # free sections
    s_secs = "".join(f'<section class="nlp-s"><div class="wrap nlp-prose"><h2 class="nlp-h2">{e(x["heading"])}</h2>{_nl_md(x["text"])}'
                     + ('<ul class="ticks">' + "".join(f"<li>{_nl_inline(b)}</li>" for b in x["bullets"]) + "</ul>" if x.get("bullets") else "")
                     + '</div></section>' for x in p.get("sections", []))
    # gallery
    s_gal = ""
    if p.get("gallery"):
        s_gal = (f'<section class="nlp-s"><div class="wrap"><h2 class="nlp-h2">{e(p.get("gallery_heading") or name + " gallery")}</h2><div class="nlp-gal">'
                 + "".join(f'<figure>{_nl_img(x, "(min-width:900px) 30vw, 100vw")}' + (f'<figcaption>{_nl_inline(x["caption"])}</figcaption>' if x.get("caption") else "") + '</figure>' for x in p["gallery"])
                 + '</div></div></section>')
    # planning: type-level checks (shared) + the project's own steps or the type timeline
    if p.get("steps"):
        steps = p["steps"]
        st = "".join(f'<li><span class="sn">{i+1:02d}</span><div><h3>{e(x["title"])}' + (f' <small>{e(x["duration"])}</small>' if x.get("duration") else "")
                     + f'</h3><p>{_nl_inline(x["text"])}</p></div></li>' for i, x in enumerate(steps))
    else:
        st = "".join(f'<li><span class="sn">{i+1:02d}</span><div><h3>{e(t)} <small>{e(d)}</small></h3><p>{e(x)}</p></div></li>' for i, (t, d, x) in enumerate(TL[g]))
    s_plan = (f'<section class="nlp-s nlp-plan-s"><div class="wrap"><h2 class="nlp-h2">Planning your {e(name)} {work}</h2>'
              f'<div class="nlp-2col"><div><h3 class="nlp-h3">{"Handover check" if work == "fit-out" else "Defects check at handover"}</h3>{ul(DEFECTS[g])}</div>'
              f'<div><h3 class="nlp-h3">{"Rules and approvals" if work == "fit-out" else "What the rules allow"}</h3>{ul(RULES[g])}'
              f'<p class="nlp-small">Rules change, so we check the current version for your unit before we quote. <a href="{BASE}services/{gslug}/">Full {e(GBY[gslug]["short"].lower())} guide</a></p></div></div>'
              f'<h3 class="nlp-h3">{e(p.get("steps_heading") or ("From handover to opening" if work == "fit-out" else "From keys to move-in"))}</h3>'
              f'<ol class="nlp-steps">{st}</ol>'
              + (f'<p class="nlp-small">{_nl_inline(p["timeline_note"])}</p>' if p.get("timeline_note") else "") + '</div></section>')
    # FAQ, sources, nearby, CTA
    faqs = "".join(f'<details class="qa"><summary><h3>{e(x["q"])}</h3><span class="pm" aria-hidden="true"></span></summary><div class="vq">{_nl_md(x["a"])}</div></details>' for x in p["faq"])
    s_faq = f'<section class="nlp-s nlp-faq"><div class="wrap narrow"><h2 class="nlp-h2">{e(name)} {work} FAQ</h2>{faqs}</div></section>'
    srcs = p["sources"] + [dict(label=n, url=u) for n, u in SRC_RULES[g] if u not in [x["url"] for x in p["sources"]]]
    s_src = (f'<section class="nlp-s nlp-src"><div class="wrap narrow"><h2 class="nlp-h2">Sources</h2><ul>'
             + "".join(f'<li><a href="{x["url"]}" target="_blank" rel="{"nofollow noopener" if x.get("nofollow") else "noopener"}">{e(x["label"])}</a></li>' for x in srcs)
             + '</ul>' + (f'<p class="nlp-small">{e(p["reviewed"])}</p>' if p.get("reviewed") else "")
             + f'<p class="nlp-small">{e(MAISON_INDEP)} We have not worked at {e(name)} unless our portfolio says so. Concept pictures are AI-generated style concepts, not photos of a finished unit.</p></div></section>')
    near = nl_nearby(p, projects)
    s_near = (f'<section class="nlp-s nlp-near"><div class="wrap"><h2 class="nlp-h2">Nearby new launches</h2>'
              f'<div class="lgrid nlp-near-g">{"".join(nl_card(q) for q in near)}</div>'
              f'<p class="nlp-small"><a href="{BASE}new-launches/">All new launches</a></p></div></section>') if near else ""
    s_cta = (f'<section class="cta dark"><div class="wrap cta-in"><p class="eyebrow">Talk to Maison</p>'
             f'<h2 class="display">Planning your {e(name)} {work}?<br><em>WhatsApp Maison</em></h2>'
             f'<p class="cta-p">{e(p.get("cta_text") or "Send your floor plan and your key or handover date. Roland and the team will reply with first ideas, a realistic timeline and an itemised quote.")}</p>'
             f'<div class="btns">{_nl_wa("WhatsApp " + PHONE, msg, slug + "-end", p, cls="btn light nlp-wa-l")}<a class="btn ghost-l" href="{BASE}new-launches/">All new launches</a></div></div></section>')
    # head + schema
    og = absu(hero["image"]) if hero else absu(NL_DEFAULT_OG)
    imgs = [absu(x["image"]) for x in p.get("renders", []) + p.get("gallery", [])] or ([og] if hero else [])
    art = {"@type": "Article", "headline": h1, "description": _nl_desc(p), "datePublished": p.get("date_published", "2026-11-07"),
           "dateModified": p.get("date_modified", p.get("date_published", "2026-11-11")), "author": {"@id": DOMAIN + "/#business"},
           "publisher": {"@id": DOMAIN + "/#business"}, "mainEntityOfPage": DOMAIN + "/" + path,
           "about": {"@type": "Place", "name": name, "address": {"@type": "PostalAddress", "addressLocality": p["area"], "addressCountry": "SG"}},
           "keywords": ", ".join(p["keywords"]), "citation": [x["url"] for x in p["sources"]]}
    if imgs: art["image"] = imgs
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("New launches", "new-launches/"), (name, path)]), art,
              {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": x["q"], "acceptedAnswer": {"@type": "Answer", "text": _nl_plain(x["a"])}} for x in p["faq"]]}]}
    title, desc = _nl_title(p), _nl_desc(p)
    s = head(title, desc, path, og, schema)
    tw = (f'<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}">'
          f'<meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{og}">')
    if hero: tw += f'<meta property="og:image:width" content="{hero["width"]}"><meta property="og:image:height" content="{hero["height"]}"><meta property="og:image:alt" content="{e(hero["alt"])}">'
    s = s.replace('<meta name="twitter:card" content="summary_large_image">', tw)
    s += header("new-launches/")
    body = (f"{s_rend}{s_plans}{s_tips}{s_secs}{s_facts}" if p.get("facts_after") else f"{s_facts}{s_rend}{s_plans}{s_tips}{s_secs}")  # facts_after: picture-first V4 order
    s += f'<div class="nlp">{s_hero}{body}{s_gal}{s_plan}{s_faq}{s_src}{s_near}</div>{s_cta}'
    s += footer()
    write(path + "index.html", s)

# ---------------------------------------------------------------- hub
HUB_FAQ = [("What is the difference between TOP and key collection?", "TOP (Temporary Occupation Permit) means the building can be occupied. Key collection comes after, on a date your developer or HDB gives you. We never treat a TOP date as your key date."),
           ("When should I contact an interior designer?", "One to two months before keys for a BTO or condo, and before you sign the lease for an office or shop. That leaves time for design, quotation and approvals so work starts on day one."),
           ("Are you the appointed interior designer for these projects?", "No. Maison is an independent firm, not appointed by or affiliated with any developer, HDB or building owner. We write these guides to help new owners and tenants plan."),
           ("Where do the project facts come from?", "Only from public sources linked on each page, such as HDB, the developer's own site or published reports. If we could not confirm a fact, we left it out or marked it as reported.")]

def nl_hub(projects):
    order = sorted(projects, key=lambda q: (0 if _nl_card_img(q) else 1, q["name"].lower()))
    counts = {t: sum(1 for q in projects if q["type"] == t) for t in NL_TYPES}
    chips = (f'<button class="chip on" data-f="All" aria-pressed="true">All <span>{len(projects)}</span></button>'
             + "".join(f'<button class="chip" data-f="{t}" aria-pressed="false"{" disabled" if not counts[t] else ""}>{t} <span>{counts[t]}</span></button>' for t in NL_TYPES))
    cards = "".join(nl_card(q) for q in order)
    gcards = "".join(f'<a class="gc" href="{BASE}services/{g["slug"]}/"><h3>{e(g["short"])}</h3><p>{e(g["desc"])}</p><span class="more">Read the guide</span></a>' for g in GUIDES)
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("New launches", "new-launches/")]),
              {"@type": "CollectionPage", "name": "New launches renovation and fit-out guides",
               "hasPart": [{"@type": "Article", "headline": _nl_h1(q), "url": DOMAIN + "/new-launches/" + q["slug"] + "/"} for q in order]},
              faq_ld(HUB_FAQ)]}
    s = head("New Launches Singapore 2026-2027 | BTO, Condo, Office & Shop Fit-Out Guides | Maison",
             "Renovation and fit-out guides for new BTO, EC, condo, landed, office and retail projects in Singapore reaching TOP or key collection in 2026-2027. Facts from public sources.",
             "new-launches/", NL_DEFAULT_OG, schema)
    s += header("new-launches/")
    s += f"""<section class="phead"><div class="wrap"><p class="eyebrow">New launches · 2026 to 2027</p>
<h1 class="display">Getting your keys? <em>Plan the renovation first</em></h1>
<p class="ph-p">Guides for BTO, EC, condo, landed, office and retail projects reaching TOP or handover in 2026 and 2027. Each page lists key facts from public sources, what owners usually change, a handover check, the rules that apply and a realistic timeline.</p>
<div class="chips nlh-chips" role="group" aria-label="Filter by property type">{chips}</div></div></section>
<section class="sec tight"><div class="wrap"><div class="lgrid" id="lgrid">{cards}</div>
<p class="nl-indep">{e(MAISON_INDEP)} Dates follow the wording of each page's source; a TOP date is not a key-collection date.</p></div></section>
<section class="sec tight nl-guides"><div class="wrap"><p class="eyebrow">Guides by property type</p><h2 class="display">Renovation and fit-out, <em>by type</em></h2><div class="ggrid">{gcards}</div></div></section>
{faq_block(HUB_FAQ, "About these guides")}{wa_cta("Collecting keys soon?", "Hi Maison, I'm collecting keys soon and would like to plan the renovation.", "new-launches")}"""
    s += footer()
    write("new-launches/index.html", s)

exec(open(os.path.join(HERE, "newlaunch_pack.py"), encoding="utf-8").read())
