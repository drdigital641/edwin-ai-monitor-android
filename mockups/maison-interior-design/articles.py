# Articles for maisoninteriordesign.sg (loaded by build.py via exec, after launches.py).
# One JSON file per article in data/articles/<slug>.json, rendered by ONE template (article_page) with the site's
# shared head/header/footer/CTA. Format: docs/article-data-format.md. Hub: /articles/. Styles: articles.css
# (article pages only, so mid.css and every other page stay untouched by a new article).
#
# Content rules (Edwin 12 Nov 2026): topics only from Maison's real services, real reviews and the new-launch pages;
# real facts only (no prices, no promises or guarantees, no invented results); no CEA-regulated property talk
# (no selling, prices, yields or investment advice for any project). check_article() stops the build on a breach.

import re as _re

ART_DIR = os.path.join(HERE, "data", "articles")
ARTICLES, ART_URLS, ART_LASTMOD = [], [], {}
ART_CSS = "articles.css"
ART_VER = hashlib.md5(open(os.path.join(HERE, ART_CSS), "rb").read()).hexdigest()[:8]

# Words that never appear in an article: prices and money, promises, and property-agent talk (CEA).
ART_BANNED = [
    (r"(?:S\$|\$\s?\d|SGD|\bdollars?\b)", "a price or amount of money"),
    (r"\b(?:price[ds]?|pricing|cheap(?:est)?|discount|promo(?:tion)?|budget of|cost(?:s)? from|psf|per square f(?:oo|ee)t)\b", "price talk"),
    (r"\bguarantee[ds]?\b|\bpromise[ds]?\b|\b100%|\bbest in singapore\b|\bno\.? ?1\b|\bcheapest\b", "a promise or claim we cannot back"),
    (r"\b(?:yield|rental income|capital (?:gain|appreciation)|appreciat(?:e|ion)|investment|investor|ROI|resale value|en bloc|for sale|buy(?:ing)? a unit|showflat booking|balloting odds|CEA)\b", "property sales or investment talk (CEA)"),
    (r"\bappointed (?:by|designer)\b|\bofficial (?:designer|partner)\b", "an appointed-designer claim"),
]

def _art_text(a):
    out = [a["title"], a["description"], a["lead"], " ".join(a["h1"])]
    for s in a["sections"]:
        out += [s.get("h2", "")] + s.get("p", []) + s.get("list", []) + [x for st in s.get("steps", []) for x in st]
    out += [x for q in a.get("faq", []) for x in q]
    return "\n".join(out)

def check_article(a, path):
    bad = []
    need = ("slug", "date_published", "title", "description", "keyword", "eyebrow", "h1", "lead", "hero", "sections", "related", "faq", "wa_text")
    bad += [f"missing {k}" for k in need if not a.get(k)]
    if bad: return bad
    if not _re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", a["slug"]): bad.append("slug must be lower-case words joined by -")
    if os.path.basename(path) != a["slug"] + ".json": bad.append("file name must be <slug>.json")
    for k in ("date_published", "date_modified"):
        if a.get(k) and not _re.fullmatch(r"20\d\d-\d\d-\d\d", a[k]): bad.append(f"{k} must be YYYY-MM-DD")
    if len(a["title"]) > 70: bad.append(f"title is {len(a['title'])} characters (max 70)")
    if not 110 <= len(a["description"]) <= 160: bad.append(f"description is {len(a['description'])} characters (110 to 160)")
    kw = a["keyword"].lower()
    for k, v in (("title", a["title"]), ("h1", " ".join(a["h1"])), ("lead", a["lead"])):
        if kw not in v.lower(): bad.append(f'keyword "{a["keyword"]}" missing from {k}')
    if len(a["h1"]) != 2: bad.append("h1 is [plain part, italic part]")
    if len(a["faq"]) < 3: bad.append("at least 3 FAQ")
    if len(a["related"]) < 2: bad.append("at least 2 related service or project links")
    for s in a["sections"]:
        if not s.get("h2"): bad.append("every section needs an h2")
    txt = _art_text(a)
    for pat, why in ART_BANNED:
        m = _re.search(pat, txt, _re.I)
        if m: bad.append(f'{why}: "{m.group(0)}"')
    if "<" in txt: bad.append("no HTML in the text fields (plain text only)")
    return bad

def art_load():
    arts, problems = [], []
    for f in sorted(glob.glob(os.path.join(ART_DIR, "*.json"))):
        try: a = json.load(open(f, encoding="utf-8"))
        except Exception as x: problems.append(f"{os.path.basename(f)}: not valid JSON ({x})"); continue
        problems += [f"{os.path.basename(f)}: {p}" for p in check_article(a, f)]
        arts.append(a)
    slugs = [a.get("slug") for a in arts]
    problems += [f"duplicate slug {s}" for s in set(slugs) if slugs.count(s) > 1]
    if problems: raise SystemExit("article check failed (nothing was built):\n  " + "\n  ".join(problems))
    return sorted(arts, key=lambda a: (a["date_published"], a["slug"]), reverse=True)

def _date_h(d):
    import datetime as _dt
    x = _dt.date.fromisoformat(d)
    return f"{x.day} {x.strftime('%B %Y')}"

def _mins(a):
    return max(2, round(len(_art_text(a).split()) / 220))

def _art_head(s, a=None):
    """The site's shared head, plus the article stylesheet; article pages are og:type article."""
    s = s.replace("</head>", f'<link rel="stylesheet" href="{BASE}{ART_CSS}?v={ART_VER}">\n</head>', 1)
    if a:
        s = s.replace('<meta property="og:type" content="website">',
                      f'<meta property="og:type" content="article"><meta property="article:published_time" content="{a["date_published"]}">', 1)
    return s

def _sec(i, s):
    body = "".join(f"<p>{e(p)}</p>" for p in s.get("p", []))
    if s.get("list"): body += ul(s["list"])
    if s.get("steps"):
        body += '<ol class="ar-steps">' + "".join(f'<li><span class="sn">0{j+1}</span><div><h3>{e(t)}</h3><p>{e(x)}</p></div></li>' for j, (t, x) in enumerate(s["steps"])) + "</ol>"
    for p in s.get("p_after", []): body += f"<p>{e(p)}</p>"
    return f'<section class="ar-sec" id="s{i+1}"><h2 class="display"><span class="ar-n" aria-hidden="true">{i+1:02d}</span>{e(s["h2"])}</h2>{body}</section>'

def article_page(a, others):
    path = f"articles/{a['slug']}/"
    url = DOMAIN + "/" + path
    h = a["hero"]
    mod = a.get("date_modified") or a["date_published"]
    toc = "".join(f'<li><a href="#s{i+1}">{e(s["h2"])}</a></li>' for i, s in enumerate(a["sections"]))
    secs = "".join(_sec(i, s) for i, s in enumerate(a["sections"]))
    rel = "".join(f'<li><a href="{BASE}{u}">{e(t)}</a></li>' for u, t in a["related"])
    more = "".join(f'<li><a href="{BASE}articles/{o["slug"]}/"><span>{_date_h(o["date_published"])}</span>{e(o["title"].split(" | ")[0])}</a></li>' for o in others[:3])
    src = src_line([tuple(x) for x in a["sources"]]) if a.get("sources") else ""
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("Articles", "articles/"), (a["title"].split(" | ")[0], path)]),
              {"@type": "Article", "headline": a["title"].split(" | ")[0], "description": a["description"], "datePublished": a["date_published"],
               "dateModified": mod, "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"},
               "mainEntityOfPage": url, "image": absu(h["src"]), "inLanguage": "en-SG", "keywords": a["keyword"],
               "about": [{"@type": "Thing", "name": t} for _, t in a["related"][:3]]},
              faq_ld([tuple(x) for x in a["faq"]])]}
    s = _art_head(head(a["title"], a["description"], path, h["src"], schema), a)
    s += header("articles/")
    s += f"""<article class="ar">
<header class="ar-hd"><div class="wrap narrow">
<nav class="ar-crumbs" aria-label="Breadcrumb"><a href="{BASE}">Home</a><span aria-hidden="true">/</span><a href="{BASE}articles/">Articles</a></nav>
<p class="eyebrow">{e(a['eyebrow'])}</p>
<h1 class="display">{e(a['h1'][0])} <em>{e(a['h1'][1])}</em></h1>
<p class="ar-meta"><time datetime="{a['date_published']}">{_date_h(a['date_published'])}</time><span aria-hidden="true">·</span><span>{_mins(a)} min read</span><span aria-hidden="true">·</span><span>Maison Interior Design</span></p>
<p class="ar-lead">{e(a['lead'])}</p>
</div><figure class="ar-hero wrap">{img(h['src'], h['alt'], w=h.get('w', 1024), h=h.get('h', 683), lazy=False, sizes="(min-width:1100px) 1040px, 100vw")}{f"<figcaption>{e(h['caption'])}</figcaption>" if h.get('caption') else ""}</figure></header>
<div class="ar-body"><div class="wrap ar-grid">
<aside class="ar-toc" aria-label="In this article"><p class="eyebrow">In this article</p><ol>{toc}</ol></aside>
<div class="ar-main nl-body">{secs}
<aside class="ar-rel"><p class="eyebrow">Related at Maison</p><ul>{rel}</ul></aside>{src}</div>
</div></div>
</article>
{faq_block([tuple(x) for x in a['faq']], "Quick answers")}
{f'<section class="sec ar-more"><div class="wrap narrow"><p class="eyebrow">More articles</p><ul class="ar-list-s">{more}</ul><p><a class="link" href="{BASE}articles/">All articles</a></p></div></section>' if more else ''}
{wa_cta("Planning your space?", a['wa_text'], 'article-' + a['slug']).replace(f'<a class="btn ghost-l" href="{BASE}new-launches/">All new launches</a>', f'<a class="btn ghost-l" href="{BASE}contact/">Send your floor plan</a>')}"""
    s += footer()
    write(path + "index.html", s)

def articles_hub():
    path = "articles/"
    items = []
    for i, a in enumerate(ARTICLES):
        items.append(f"""<li class="ah-i"><a href="{BASE}articles/{a['slug']}/">
<span class="ah-n" aria-hidden="true">{len(ARTICLES)-i:02d}</span>
<span class="ah-t"><span class="ah-m"><time datetime="{a['date_published']}">{_date_h(a['date_published'])}</time> · {e(a['eyebrow'])}</span>
<h2>{e(a['title'].split(' | ')[0])}</h2><span class="ah-d">{e(a['description'])}</span><span class="more">Read the article</span></span></a></li>""")
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("Articles", path)]),
              {"@type": "CollectionPage", "name": "Interior design articles", "url": DOMAIN + "/" + path,
               "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i+1, "url": f"{DOMAIN}/articles/{a['slug']}/", "name": a["title"].split(" | ")[0]} for i, a in enumerate(ARTICLES)]}}]}
    s = _art_head(head("Interior Design Articles Singapore | Renovation Planning Notes | Maison",
                       "Plain-English notes from Maison Interior Design on planning a renovation or fit-out in Singapore: what to prepare, what to ask and what happens when.",
                       path, ARTICLES[0]["hero"]["src"] if ARTICLES else "Jimmy-Monkey-Completed-6.jpg", schema))
    s += header("articles/")
    s += f"""<section class="phead ah-hd"><div class="wrap"><p class="eyebrow">Articles</p><h1 class="display">Renovation notes, <em>in plain English</em></h1>
<p class="ph-p">Practical notes from the Maison team on planning a home renovation or a commercial fit-out in Singapore, drawn from how we work on our own projects.</p></div></section>
<section class="sec tight ah"><div class="wrap narrow"><ol class="ah-list">{''.join(items)}</ol>
<p class="ah-also">Looking for a specific project? See the <a href="{BASE}services/">services</a>, <a href="{BASE}new-launches/">new launch guides</a> and <a href="{BASE}portfolio/">portfolio</a>.</p></div></section>
{cta_block()}"""
    s += footer()
    write(path + "index.html", s)

def articles_build():
    global ARTICLES, ART_URLS
    ARTICLES = art_load()
    ART_URLS = [f"articles/{a['slug']}/" for a in ARTICLES]
    ART_LASTMOD.update({f"articles/{a['slug']}/": a.get("date_modified") or a["date_published"] for a in ARTICLES})
    ART_LASTMOD["articles/"] = max(ART_LASTMOD.values(), default="2026-11-12")
    for i, a in enumerate(ARTICLES):
        article_page(a, [o for o in ARTICLES if o is not a])
    articles_hub()
    shutil.copy(os.path.join(HERE, ART_CSS), os.path.join(OUT, ART_CSS))

def art_llms():
    if not ARTICLES: return ""
    return "\n## Articles\n- [Articles hub](" + DOMAIN + "/articles/)\n" + "".join(
        f'- [{a["title"].split(" | ")[0]}]({DOMAIN}/articles/{a["slug"]}/): {a["description"]}\n' for a in ARTICLES)

# Live-only pages (12 Nov 2026): a few pages were changed on the live server without a repo commit (Lumina Grand V4
# hub card). Their live copies sit in live-overrides/ and replace the built page; header, footer and asset versions
# are taken from the current template so a nav change still reaches them.
LIVE_ONLY = {"new-launches/": "2026-11-12", "new-launches/lumina-grand/": "2026-11-12"}

# Changed on the live server with no copy here yet: never built, so no zip can overwrite the live page.
# Remove a line once its live copy is saved in live-overrides/ (same path).
LIVE_KEEP = {"new-launches/lumina-grand/index.html"}   # Lumina Grand V4 (live 12 Nov 2026)

def apply_overrides():
    od = os.path.join(HERE, "live-overrides")
    for k in LIVE_KEEP:
        if os.path.isfile(os.path.join(od, k)): raise SystemExit(f"{k} is in live-overrides/ now: remove it from LIVE_KEEP")
        f = os.path.join(OUT, k)
        if os.path.isfile(f): os.remove(f)
    hd = header("new-launches/"); ft = footer()
    for root, _, files in os.walk(od):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), od).replace(os.sep, "/")
            t = open(os.path.join(root, f), encoding="utf-8").read()
            t = _re.sub(r'<body class="[^"]*">.*?<main id="main">', lambda m: hd, t, count=1, flags=_re.S)
            t = _re.sub(r'</main><footer class="ft">.*</html>', lambda m: ft, t, count=1, flags=_re.S)
            t = _re.sub(r'(mid\.(?:css|js))\?v=[0-9a-f]+', lambda m: f"{m.group(1)}?v={VER}", t)
            write(rel, t)
