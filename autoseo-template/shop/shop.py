"""Shared AutoSEO SHOP template pieces (first used by BIY Home Store, 25 Nov 2026).

For any e-commerce / catalogue client in Phase 1 (catalogue + WhatsApp enquiry, no cart). The site build owns the
look (its own CSS tokens, section order, copy); this module owns the data layer and the invisible, repeatable parts:

  cat = load_catalog(data_dir)             facts/brands/categories/products JSON -> validated dict (AutoCount-ready shape)
  product_indexable(p)                     INDEX RULE: data flag AND active AND real photo AND real description/specs
  wa_url(e164, text)                       wa.me link with the prefill URL-encoded (decode-tested in test_shop.py)
  fill(tpl, **v)                           prefill template filler; unknown {keys} stay visible so a check can catch them
  maps_search(address)                     Google Maps search link by address (no invented place IDs)
  stock_label_key(p)                       'in_stock' | 'limited' | 'check' from products.json stock_label
  search_index(...)                        static search-index.json rows (brands, categories, ranges, products + synonyms)
  ld_org / ld_store / ld_product / ld_breadcrumb / ld_faq / ld_website   JSON-LD with NO offers, price or rating
  product_frame(icon_svg, brand, images)   uniform 1:1 frame: real image (contain/cover) or icon tile + brand text
  rail(items_html, label)                  finger-drag rail; shop.js autoplays it only when it overflows
  banned_hits(dist, rules)                 pre-upload grep, returns hits (empty = pass)
  km(a, b)                                 straight-line distance between two lat/lng points

Hard rules carried here: prices are never stored or rendered (a non-null price in products.json fails load_catalog);
brands with published:false never render; is_demo rows fail the build; status != active rows are skipped.
"""
import json, math, os, re
from html import escape as _e
from urllib.parse import quote

STOCK_KEYS = {"in-stock": "in_stock", "limited": "limited", "check-availability": "check"}


class CatalogError(Exception):
    pass


def _read(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def load_catalog(data_dir):
    facts = _read(os.path.join(data_dir, "facts.json"))
    brands_all = _read(os.path.join(data_dir, "brands.json"))
    cats = _read(os.path.join(data_dir, "categories.json"))
    prod = _read(os.path.join(data_dir, "products.json"))
    errors = []
    published = set(facts.get("brands_published", []))
    brands = [b for b in brands_all if b.get("published") and b["slug"] in published]
    held = [b for b in brands_all if not b.get("published")]
    bslugs = {b["slug"] for b in brands}
    cslugs = {c["slug"] for c in cats}
    rng = {r["id"]: (b["slug"], r) for b in brands for r in b.get("ranges", [])}
    products, seen = [], set()
    for p in prod.get("products", []):
        if p.get("is_demo"):
            errors.append("demo product %s" % p.get("id"))
            continue
        if p.get("price") not in (None, "", 0):
            errors.append("price stored on %s (price_mode whatsapp_only)" % p.get("id"))
        if p.get("status") != "active":
            continue
        if p.get("brand") not in bslugs:
            continue  # held or unknown brand never renders
        if p.get("category") not in cslugs:
            errors.append("unknown category on %s" % p.get("id"))
            continue
        if p.get("range") and p["range"] not in rng:
            errors.append("unknown range on %s" % p.get("id"))
        if p["slug"] in seen:
            errors.append("duplicate slug %s" % p["slug"])
        seen.add(p["slug"])
        products.append(p)
    if errors:
        raise CatalogError("; ".join(errors))
    return {"facts": facts, "brands": brands, "held": held, "categories": cats, "products": products,
            "ranges": rng, "brand": {b["slug"]: b for b in brands}, "category": {c["slug"]: c for c in cats}}


def product_indexable(p):
    """INDEX RULE (blueprint): indexable only if the data says so AND active AND a real photo AND real text."""
    return bool(p.get("indexable")) and p.get("status") == "active" and bool(p.get("images")) and \
        bool(p.get("description") or p.get("specs"))


def stock_label_key(p):
    return STOCK_KEYS.get(p.get("stock_label") or "", "check")


def fill(tpl, **v):
    def rep(m):
        k = m.group(1)
        return str(v[k]) if k in v and v[k] is not None else m.group(0)
    return re.sub(r"\{([a-z_]+)\}", rep, tpl)


def wa_url(e164, text):
    n = re.sub(r"\D", "", e164)
    return "https://wa.me/%s?text=%s" % (n, quote(text, safe=""))


def maps_search(address):
    return "https://www.google.com/maps/search/?api=1&query=" + quote(address, safe="")


def km(a, b):
    if None in (a[0], a[1], b[0], b[1]):
        return None
    r = 6371.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(h))


# ---------------------------------------------------------------- JSON-LD (no offers, no price, no rating, no hours)
def ld_org(facts, url, logo, org_id):
    return {"@type": "Organization", "@id": org_id, "name": facts["name"], "alternateName": facts.get("short_name"),
            "url": url, "logo": logo, "foundingDate": str(facts["founded"]) if facts.get("founded") else None,
            "sameAs": [facts["facebook"]] if facts.get("facebook") else None}


def ld_store(br, facts, url, store_id, org_id, image, telephone):
    addr = {"@type": "PostalAddress", "streetAddress": br["street"], "addressLocality": br["city"],
            "addressRegion": br["state"], "addressCountry": "MY"}
    if br.get("postcode"):
        addr["postalCode"] = br["postcode"]
    d = {"@type": "HardwareStore", "@id": store_id, "name": br["name"], "url": url, "image": image,
         "parentOrganization": {"@id": org_id}, "address": addr, "telephone": telephone,
         "hasMap": maps_search(br["address_line"]),
         "sameAs": [facts["facebook"]] if facts.get("facebook") else None}
    if br.get("lat") is not None and br.get("lng") is not None:
        d["geo"] = {"@type": "GeoCoordinates", "latitude": br["lat"], "longitude": br["lng"]}
    return d


def ld_product(p, brand_name, url, description=None, image=None):
    d = {"@type": "Product", "@id": url + "#product", "name": p["name"], "url": url,
         "brand": {"@type": "Brand", "name": brand_name}, "model": p.get("model"), "sku": p.get("sku") or None,
         "mpn": None, "description": description or p.get("description") or None,
         "image": image}
    return d


def ld_breadcrumb(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def ld_faq(qas):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qas]}


def ld_website(name, url, search_url, lang, site_id):
    return {"@type": "WebSite", "@id": site_id, "name": name, "url": url, "inLanguage": lang,
            "potentialAction": {"@type": "SearchAction", "target": search_url + "?q={search_term_string}",
                                "query-input": "required name=search_term_string"}}


def _clean(o):
    if isinstance(o, dict):
        return {k: _clean(v) for k, v in o.items() if v not in (None, [], "")}
    if isinstance(o, list):
        return [_clean(v) for v in o]
    return o


def ld_script(graph):
    g = _clean({"@context": "https://schema.org", "@graph": graph})
    return '<script type="application/ld+json">' + json.dumps(g, ensure_ascii=False).replace("</", "<\\/") + "</script>"


# ---------------------------------------------------------------- render helpers
def product_frame(icon_svg, brand_text, images=None, alt="", cls="pf"):
    """Uniform 1:1 frame. Real image if images[] exists (pack shot = contain on white, lifestyle = cover),
    otherwise the category icon on a soft tile with the brand as plain text. Never an empty or broken image."""
    if images:
        im = images[0]
        fit = "cover" if im.get("kind") == "lifestyle" else "contain"
        return ('<div class="%s %s-img"><img src="%s" alt="%s" width="%s" height="%s" loading="lazy" decoding="async" '
                'style="object-fit:%s"></div>' % (cls, cls, _e(im["src"]), _e(alt), im.get("w", 800), im.get("h", 800), fit))
    return ('<div class="%s %s-icon" aria-hidden="true"><span class="%s-tile">%s</span><span class="%s-brand">%s</span></div>'
            % (cls, cls, cls, icon_svg, cls, _e(brand_text)))


def rail(items_html, label, cls="rail"):
    """Finger-drag rail. shop.js: native overflow-x scroll, rAF autoplay with cloned children ONLY when it overflows,
    vertical scroll never pauses it, ~350ms hold or horizontal drag pauses, resume 1.5s after release,
    prefers-reduced-motion = no autoplay."""
    return '<div class="%s" data-rail role="region" aria-label="%s" tabindex="0"><div class="%s-track">%s</div></div>' % (
        cls, _e(label), cls, "".join(items_html))


def search_form(action, label, placeholder, button, big=False, value="", ref="search_header", cls="sf"):
    v = (' value="%s"' % _e(value)) if value else ""
    return ('<form class="%s%s" role="search" action="%s" method="get" data-search-form data-ref="%s">'
            '<label class="vh" for="q-%s">%s</label>'
            '<input id="q-%s" type="search" name="q" placeholder="%s" autocomplete="off" enterkeyhint="search"%s>'
            '<button type="submit">%s</button></form>' % (
                cls, " %s-big" % cls if big else "", _e(action), ref, ref, _e(label), ref, _e(placeholder), v, button))


def search_index(rows):
    """rows: dicts {t: type, p: english path, n: {lang: name}, b: brand, k: [synonyms...]} -> compact JSON text."""
    out = []
    for r in rows:
        k = " ".join(sorted(set(str(x).lower() for x in r.get("k", []) if x)))
        out.append({"t": r["t"], "p": r["p"], "n": r["n"], "b": r.get("b", ""), "k": k})
    return json.dumps({"v": 1, "items": out}, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------- pre-upload grep
def _visible(html):
    h = re.sub(r"<script\b[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    h = re.sub(r"<style\b[^>]*>.*?</style>", " ", h, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", h)


def banned_hits(dist, rules, exts=(".html", ".xml", ".txt", ".json", ".js", ".css")):
    """rules: list of (name, regex, scope) with scope 'raw' (whole file) or 'text' (visible HTML text only).
    Returns [(file, rule, snippet)]."""
    hits = []
    for root, _, files in os.walk(dist):
        for fn in files:
            if not fn.endswith(exts):
                continue
            fp = os.path.join(root, fn)
            raw = open(fp, encoding="utf-8", errors="ignore").read()
            vis = _visible(raw) if fn.endswith(".html") else raw
            for name, rx, scope in rules:
                src = raw if scope == "raw" else vis
                m = re.search(rx, src)
                if m:
                    s = src[max(0, m.start() - 30): m.end() + 30].replace("\n", " ")
                    hits.append((os.path.relpath(fp, dist), name, s))
    return hits
