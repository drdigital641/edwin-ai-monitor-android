# Towner Residences sample page, built verbatim from towner-residences-page.md (exec'd by launches.py).
import re as _re
import markdown as _md

TOWNER_IMG = BASE + "images/new-launches/towner-residences/"

def _strip(h):
    return html.unescape(_re.sub(r"<[^>]+>", "", h)).strip()

def towner_page():
    raw = open(os.path.join(HERE, "towner-residences-page.md"), encoding="utf-8").read()
    _, fm, body = raw.split("---", 2)
    meta = {k.strip(): v.strip().strip('"') for k, v in (l.split(":", 1) for l in fm.strip().splitlines() if ":" in l)}
    body = body.strip()
    h1 = body.splitlines()[0].lstrip("# ").strip()
    rest = body.split("\n", 1)[1].strip()
    intro, main = rest.split("\n## ", 1)
    main = "## " + main
    intro_blocks = intro.strip().split("\n\n")
    hero_md, top_md = "\n\n".join(intro_blocks[:2]), "\n\n".join(intro_blocks[2:])
    conv = lambda t: _md.markdown(t, extensions=["tables"])
    hero, top, main_h = conv(hero_md), conv(top_md), conv(main)

    # images + captions -> figures (label in the image stays fully visible: no cropping)
    def fig(m):
        alt, srcf, cap = m.group(1), m.group(2), m.group(3)
        f = TOWNER_IMG + srcf.replace(".png", ".webp")
        return (f'<figure class="cfig"><img src="{f}" alt="{alt}" width="1152" height="864" loading="lazy" decoding="async">'
                f'<figcaption>{cap}</figcaption></figure>')
    main_h = _re.sub(r'<p><img alt="([^"]*)" src="([^"]+)" /></p>\s*<p>(.*?)</p>', fig, main_h, flags=_re.S)
    # 2x2 gallery: wrap the four concept h3 blocks
    a = main_h.index("<h3>Living and dining</h3>")
    b = main_h.index("<h2>From keys to move-in")
    cells = ['<div class="cg-cell"><h3>' + c.strip() + "</div>" for c in main_h[a:b].split("<h3>") if c.strip()]
    main_h = main_h[:a] + '<div class="cgal">' + "".join(cells) + "</div>" + main_h[b:]
    # tables: labels for stacked mobile rows, scroll-safe wrapper
    def tbl(m):
        t = m.group(0)
        heads = [_strip(x) for x in _re.findall(r"<th[^>]*>(.*?)</th>", t, _re.S)]
        def row(r):
            cells = _re.findall(r"<td[^>]*>(.*?)</td>", r.group(1), _re.S)
            return "<tr>" + "".join(f'<td data-label="{e(heads[i] if i < len(heads) else "")}">{c}</td>' for i, c in enumerate(cells)) + "</tr>"
        t = _re.sub(r"<tr>\s*((?:<td.*?</td>\s*)+)</tr>", row, t, flags=_re.S)
        return '<div class="tw">' + t.replace("<table>", '<table class="st">') + "</div>"
    main_h = _re.sub(r"<table>.*?</table>", tbl, main_h, flags=_re.S)
    # bare URLs in the sources list become links
    main_h = _re.sub(r'(?<![="])(https://[^\s<]+)', lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>', main_h)
    # WhatsApp CTA from the copy
    main_h = _re.sub(r'<p><a href="(https://wa\.me/6593391185\?[^"]+)">WhatsApp Maison</a></p>',
                     lambda m: f'<p class="btns"><a class="btn dark-b" href="{m.group(1)}" data-cta="whatsapp" data-ref="towner-residences">WhatsApp Maison</a></p>', main_h)
    # external links open in a new tab
    main_h = _re.sub(r'<a href="(https?://(?!wa\.me)[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', main_h)
    top = _re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', top)

    # FAQ schema straight from the copy's question section
    faq_part = main_h[main_h.index("<h2>Questions Towner Residences owners ask</h2>"):main_h.index("<h2>Ready to see")]
    faq = []
    for chunk in faq_part.split("<h3>")[1:]:
        q, ans = chunk.split("</h3>", 1)
        faq.append((_strip(q), " ".join(_strip(p) for p in _re.findall(r"<p>(.*?)</p>", ans, _re.S))))
    srcs = _re.findall(r'href="(https://[^"]+)"', main_h[main_h.index("<h2>Sources and checks</h2>"):])
    path = "new-launches/towner-residences/"
    schema = {"@context": "https://schema.org", "@graph": [ORG, crumbs([("Home", ""), ("New launches", "new-launches/"), ("Towner Residences", path)]),
              {"@type": "Article", "headline": h1, "description": meta["meta_description"], "datePublished": "2026-11-07", "dateModified": "2026-11-07",
               "author": {"@id": DOMAIN + "/#business"}, "publisher": {"@id": DOMAIN + "/#business"}, "mainEntityOfPage": DOMAIN + "/" + path,
               "image": [DOMAIN + "/images/new-launches/towner-residences/concept-" + k + ".webp" for k in ("living-dining", "kitchen", "master-bedroom", "study")],
               "about": {"@type": "Place", "name": "Towner Residences, Kallang/Whampoa"}, "citation": list(dict.fromkeys(srcs))},
              faq_ld(faq)]}
    s = head(meta["seo_title"], meta["meta_description"], path, TOWNER_IMG + "concept-living-dining.webp", schema)
    s += header("new-launches/")
    s += f"""<section class="phead tw-hero"><div class="wrap narrow"><p class="eyebrow"><a href="{BASE}new-launches/">New launches</a> · <a href="{BASE}services/bto-renovation/">BTO key collection</a></p>
<h1 class="display tw-h1">{e(h1)}</h1><div class="ph-p tw-intro">{hero}</div></div></section>
<section class="sec tight tw-sec"><div class="wrap narrow nl-body tw-body">{top}{main_h}</div></section>"""
    s += footer()
    write(path + "index.html", s)
