# Light project packs (markdown) -> new-launch JSON data (11 Nov 2026).
# A pack is <slug>/page.md (or <slug>.md) with: "# <Name> Interior Design & Renovation | <place> <Condo|EC> — Maison",
# "Meta description:", "Keywords:", "## Project facts" bullets, "## <Name> interior design and renovation" copy,
# "## Frequently asked questions" (**Q?** A), "## Nearby projects" links, "## Talk to Maison", "## Sources".
# Only facts in the pack are used. Blank facts stay blank (not shown on the page). "Floor plan", "Target keywords" and
# internal "File note" lines are not published. exec'd by newlaunch.py.
import re as _re

PACK_TYPES = {"condominium": ("Condo", "Private condominium"), "executive condominium": ("EC", "Executive condominium"),
              "bto": ("BTO", "HDB BTO"), "hdb bto": ("BTO", "HDB BTO"), "hdb": ("HDB", "HDB flat"), "landed": ("Landed", "Landed home"),
              "office": ("Commercial", "Office"), "retail": ("Commercial", "Retail"), "commercial": ("Commercial", "Commercial")}
# URA planning regions by postal district (used for nearby cards and the page eyebrow only)
PACK_REGION = {**{d: "Central" for d in range(1, 16)}, 16: "East", 17: "East", 18: "East", 19: "North-East", 20: "Central",
               21: "Central", 22: "West", 23: "West", 24: "West", 25: "North", 26: "North-East", 27: "North", 28: "North-East"}
PACK_TOWN_REGION = {"bukit batok": "West", "jurong": "West", "tengah": "West", "choa chu kang": "West", "bukit panjang": "West",
                    "woodlands": "North", "yishun": "North", "sembawang": "North", "tampines": "East", "pasir ris": "East",
                    "bedok": "East", "ang mo kio": "North-East", "hougang": "North-East", "punggol": "North-East",
                    "sengkang": "North-East", "serangoon": "North-East", "toa payoh": "Central", "bishan": "Central",
                    "geylang": "Central", "kallang/whampoa": "Central", "kallang": "Central", "queenstown": "Central",
                    "bukit merah": "Central", "bukit timah": "Central", "clementi": "West", "jurong east": "West",
                    "jurong west": "West", "bukit batok west": "West", "tengah": "West", "tanjong pagar": "Central",
                    "cbd": "Central", "lentor": "North-East", "islandwide": "Islandwide", "anson": "Central"}
PACK_HOSTS = {"cdlhomes.com.sg": "CDL Homes", "cdl.com.sg": "City Developments Limited", "links.sgx.com": "SGX announcement",
              "bukitsembawang.sg": "Bukit Sembawang Estates", "stackedhomes.com": "Stacked Homes", "hdb.gov.sg": "HDB",
              "ura.gov.sg": "URA", "edgeprop.sg": "EdgeProp"}

def _pk_month(t):
    """'2027-Q4' -> 'Q4 2027', '2026-03' -> 'March 2026', '2026-01-17' -> '17 January 2026', '2027-H1' -> 'H1 2027'."""
    M = "January February March April May June July August September October November December".split()
    t = _re.sub(r"\b(20\d\d)-(Q[1-4]|H[12])\b", r"\2 \1", t)
    t = _re.sub(r"\b(20\d\d)-(\d\d)-(\d\d)\b", lambda m: f"{int(m.group(3))} {M[int(m.group(2)) - 1]} {m.group(1)}", t)
    return _re.sub(r"\b(20\d\d)-(\d\d)\b", lambda m: f"{M[int(m.group(2)) - 1]} {m.group(1)}", t)

def _pk_src_label(u, nofollow=False):
    host = _re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
    name = next((v for k, v in PACK_HOSTS.items() if host == k or host.endswith("." + k)), host)
    tail = _re.sub(r"\.(pdf|ashx|html?)$", "", _re.sub(r"[?#].*", "", u.rstrip("/")).split("/")[-1], flags=_re.I)
    tail = _re.sub(r"%20|[-_.]+", " ", tail).strip()
    lab = name + (f": {tail}" if tail and tail.lower() not in (host.lower(), "construction") and len(tail) < 70 else
                  (": construction updates" if tail.lower() == "construction" else ""))
    if u.lower().split("?")[0].endswith(".pdf"): lab += " (PDF)"
    return lab + (" (third-party, not used as official confirmation)" if nofollow else "")

def _pk_short_desc(d, name, typ_word, place):
    d = d.replace(" a executive", " an executive").strip()
    if len(d) <= 155: return d
    for cut in (" Unconfirmed figures are left blank.", " Verified facts only;", " WhatsApp Maison with your plan."):
        d2 = d.replace(cut, "").strip()
        if len(d2) <= 155: return d2
        d = d2
    d = _re.sub(r", around [^.]+\.", ".", d).strip()
    if len(d) <= 155: return d
    d = f"{name} renovation and interior design: built-in carpentry for this {typ_word} in {place}. WhatsApp Maison with your plan."
    return d if len(d) <= 155 else d[:152].rsplit(" ", 1)[0] + "…"

PACK_WORDING = [("for this light pack", "for this page"), ("this light pack", "this page"), ("This row", "This project"), ("this row", "this project"),
                ("The row is", "This entry is"), ("the row is", "this entry is")]

def _pk_public(t):
    """Swap internal pack words for reader words (the meaning is unchanged)."""
    for a, b in PACK_WORDING: t = t.replace(a, b)
    return t

def pack_to_project(text, slug):
    """One pack (markdown text) -> one project dict in the JSON data format. Raises ValueError with the reason."""
    text = _pk_public(text)
    lines = text.replace("\r\n", "\n").split("\n")
    m = _re.match(r"#\s+(.+?)\s+(?:Interior Design & Renovation|Fit-Out & Interior Design)\s*\|\s*(.+?)\s*[—-]\s*Maison\s*$", lines[0])
    if not m: raise ValueError("first line is not '# <Name> Interior Design & Renovation | <place> … — Maison' (or '<Name> Fit-Out & Interior Design | …')")
    name, place_full = m.group(1).strip(), m.group(2).strip()
    place = _re.sub(r"\s+(Condo|EC|BTO|HDB|Landed|Office|Retail(\s*/\s*Community)?|Commercial|Mixed-Use|Neighbourhood Centre|SBF Exercise)$", "", place_full).strip()
    def meta(k):
        mm = _re.search(rf"^{k}:\s*(.*)$", text, _re.M)
        return mm.group(1).strip() if mm else ""
    secs, cur = {}, None
    for l in lines[1:]:
        if l.startswith("## "): cur = l[3:].strip(); secs[cur] = []; continue
        if cur: secs[cur].append(l)
    S = {k: "\n".join(v).strip() for k, v in secs.items()}
    body_key = next((k for k in S if _re.search(r"(interior design and renovation|fit-out and interior design|interior design notes)$", k, _re.I)), None)
    for need in ("Project facts", "Frequently asked questions", "Sources"):
        if need not in S: raise ValueError(f"section '## {need}' is missing")
    if not body_key: raise ValueError(f"section '## {name} interior design and renovation' is missing")
    # facts
    F, sources, notes = {}, [], []
    def add_src(u, nofollow=False):
        u = u.strip().rstrip(".")
        if u.startswith("http") and u not in [s["url"] for s in sources]:
            sources.append(dict(label=_pk_src_label(u, nofollow), url=u, **({"nofollow": True} if nofollow else {})))
    for l in S["Project facts"].splitlines():
        mm = _re.match(r"-\s*([^:]+?):\s*(.*)$", l.strip())
        if not mm: continue
        lab, val = mm.group(1).strip(), mm.group(2).strip()
        if lab.lower().startswith("recorded source"):
            add_src(val, nofollow=True); continue
        sm = _re.search(r"\s*Source:\s*(\S+)\s*$", val)
        if sm:
            add_src(sm.group(1)); val = val[:sm.start()].strip()
        if not val or lab.lower().startswith(("official floor-plan", "file note")): continue
        F[lab] = val.rstrip(".") if not val.endswith("etc.") else val
        if lab.lower() == "note": notes.append(val)
    def pick(prefix):
        for k, v in F.items():
            if k.lower().startswith(prefix): return k, v
        return None, ""
    tk, tv = pick("type")
    tv = _re.sub(r"\s+project$", "", tv.lower().rstrip("."))
    guide = None
    if tv in PACK_TYPES: typ, label = PACK_TYPES[tv]
    elif "sale of balance flats" in tv: typ, label = "HDB", "HDB Sale of Balance Flats"
    elif tv.startswith("retail"): typ, label, guide = "Commercial", "Retail", "retail"
    elif tv.startswith("mixed-use commercial"): typ, label, guide = "Commercial", "Mixed-use commercial", "retail"
    elif tv.startswith("office"): typ, label, guide = "Commercial", "Office", "office"
    elif tv.startswith("landed"): typ, label = "Landed", "Landed home"
    else: raise ValueError(f"unknown Type '{tv}'")
    dk, dev = pick("developer")
    if dk and "not treated as officially confirmed" in dk: dev = f"{dev} (listed in our project file, not officially confirmed)"
    _, ten = pick("tenure")
    topk, top = pick("launch / top")
    if not topk: topk, top = pick("top")
    if not topk: topk, top = pick("opening")
    _, umix = pick("unit types")
    _, dist = pick("district")
    district = dist.upper() if _re.fullmatch(r"d\d{1,2}", dist, _re.I) else ""
    # area: the place in the title, without the district part ("Shelford / D11" -> "Shelford", "District 5" stays)
    area = _re.sub(r"\s*/\s*D\d{1,2}$", "", place).strip()
    if not district:
        dm = _re.search(r"\bD(\d{1,2})\b|District (\d{1,2})", place)
        if dm: district = "D" + (dm.group(1) or dm.group(2))
    town = dist.rstrip(".")
    if not district and town and town.lower() != area.lower() and not area.lower().startswith(town.lower()):
        district = town   # HDB town, e.g. Farrer Park (Kallang/Whampoa)
    is_d = bool(_re.fullmatch(r"D\d{1,2}", district))
    region = PACK_TOWN_REGION.get(town.lower()) or (PACK_REGION.get(int(district[1:])) if is_d else None) \
             or PACK_TOWN_REGION.get(area.lower())
    if not region: raise ValueError(f"cannot tell the region from district '{dist}' / place '{place}'")
    facts = []
    for k, v in F.items():
        kl = k.lower()
        if kl.startswith(("type", "developer", "tenure", "launch / top", "unit types", "district", "note")) or kl == "top" or k == topk: continue
        facts.append(dict(label=k[0].upper() + k[1:], value=_pk_month(v)))
    # copy
    paras = [x.strip() for x in _re.split(r"\n\s*\n", S[body_key]) if x.strip()]
    kw_line = meta("Keywords")
    keywords = [k.strip() for k in kw_line.split(",") if k.strip()]
    if not keywords: raise ValueError("Keywords line is empty")
    work = "fit-out" if typ == "Commercial" else "renovation"
    if f"{name} {work}".lower() not in keywords[0].lower() or not keywords[0].lower().startswith(name.lower()):
        keywords = [f"{name} {work}"] + [k for k in keywords if k.lower() != f"{name} {work}".lower()]
    k0 = keywords[0]
    intro = paras[0]
    if k0.lower() not in intro.lower():
        intro += f" This page sets out what is on file and how to plan your {k0}."
    p = dict(name=name, slug=slug, type=typ, label=label, area=area)
    if district: p["district"] = district
    if guide: p["guide"] = guide
    p.update(region=region, developer=dev, tenure=ten)
    p["top_label"] = ("TOP" if topk and topk.lower().startswith("top") else
                      "Opening" if topk and topk.lower().startswith("opening") else "Launch / TOP / key date")
    top = _pk_month(top)
    p.update(top=top[:1].upper() + top[1:], unit_mix=umix, official_site="", facts=facts)
    if notes: p["facts_note"] = " ".join(n[0].upper() + n[1:] for n in notes)
    t = meta("SEO title")
    tail = t.split("|", 1)[1].strip() if "|" in t else f"{place_full} — Maison"
    p["title"] = f"{name} {work.title()} & Interior Design | {tail}"
    p["description"] = _pk_short_desc(meta("Meta description"), name, label.lower(), place)
    p["keywords"] = keywords
    p["intro"] = intro
    if len(paras) > 1:
        p["sections"] = [dict(heading=f"Planning your {name} interior", text="\n\n".join(paras[1:]))]
    faq = []
    for mm in _re.finditer(r"\*\*(.+?)\*\*\s*(.+?)(?=\n\s*\*\*|\Z)", S["Frequently asked questions"], _re.S):
        faq.append(dict(q=mm.group(1).strip(), a=" ".join(mm.group(2).split())))
    if not faq: raise ValueError("no FAQ items found (expected **Question?** Answer)")
    p["faq"] = faq
    talk = S.get("Talk to Maison", "").split("\n\n")[0]
    talk = _re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", talk).strip()
    if talk: p["cta_text"] = talk
    for l in S["Sources"].splitlines():
        mm = _re.match(r"-\s*(https?://\S+)", l.strip())
        if mm: add_src(mm.group(1))
    if not sources: raise ValueError("no source URLs")
    p["sources"] = sources
    p["nearby_hints"] = [_re.sub(r"^/(new-launches/)?|/$", "", u) for u in _re.findall(r"\]\((/[^)]+)\)", S.get("Nearby projects", ""))]
    rv = _re.search(r"^Light pack prepared ([^,.]+)", text, _re.M)
    if rv: p["reviewed"] = f"Facts checked against the sources on file, {rv.group(1).strip()}."
    p["date_published"] = p["date_modified"] = "2026-11-11"
    return p

def pack_files(folder):
    """Every pack in a folder: <slug>/page.md or <slug>.md (INDEX.md and README.md are skipped)."""
    out = []
    for f in sorted(glob.glob(os.path.join(folder, "*", "page.md"))): out.append((os.path.basename(os.path.dirname(f)), f))
    for f in sorted(glob.glob(os.path.join(folder, "*.md"))):
        b = os.path.splitext(os.path.basename(f))[0]
        if b.upper() not in ("INDEX", "README"): out.append((b, f))
    return out

def packs_to_json(folder, out_dir):
    """Convert every pack in folder into out_dir/<slug>.json. Returns (converted slugs, [(slug, reason)] that failed)."""
    os.makedirs(out_dir, exist_ok=True)
    ok, bad = [], []
    for slug, f in pack_files(folder):
        try:
            p = pack_to_project(open(f, encoding="utf-8").read(), slug)
        except ValueError as x:
            bad.append((slug, str(x))); continue
        with open(os.path.join(out_dir, slug + ".json"), "w", encoding="utf-8") as fh:
            json.dump(p, fh, ensure_ascii=False, indent=2); fh.write("\n")
        ok.append(slug)
    return ok, bad
