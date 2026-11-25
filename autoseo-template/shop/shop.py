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


def load_catalog(data_dir, products=None):
    """products=None: legacy products.json rows. products=[...]: groups from resolve_products()+normalize_products()
    (v3 feed path, used by BIY from 26 Nov 2026); the same brand/category/slug checks run on them."""
    facts = _read(os.path.join(data_dir, "facts.json"))
    brands_all = _read(os.path.join(data_dir, "brands.json"))
    cats = _read(os.path.join(data_dir, "categories.json"))
    prod = {"products": products} if products is not None else _read(os.path.join(data_dir, "products.json"))
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


# ================================================================ PRODUCT FEED RESOLVER (26 Nov 2026, BIY v3)
# ONE function decides which product data a build uses. Three states, same code path for every page:
#   not configured   (shop-config.json live_feed.url null)            -> products.sample.json, mode "sample"
#   configured, bad  (HTTP error / bad JSON / schema fail / < min_active / any is_sample) -> last good live snapshot if the
#                    site was ever live (live-state.json live_seen), else products.sample.json, mode "sample"
#   live             (200 + valid + >= min_active active + no is_sample) -> ONLY the live records, mode "live";
#                    snapshot products.live.json + live-state.json written. Sample and live are never mixed.
# Records use product-feed.schema.json (vendor push API fields). normalize_products() turns them into site product
# groups (SKUs sharing group.code = sizes of ONE product page) through category-map.json + the brand allow-list.

SCHEMA_TYPES = {"string": str, "boolean": bool, "number": (int, float), "integer": int, "object": dict, "array": list}


def _type_ok(v, t):
    ts = t if isinstance(t, list) else [t]
    for x in ts:
        if x == "null" and v is None:
            return True
        py = SCHEMA_TYPES.get(x)
        if py and isinstance(v, py) and not (x in ("number", "integer") and isinstance(v, bool)):
            return True
    return False


def validate_record(r, schema):
    """Small JSON-schema subset (required, type, maxLength, pattern, enum, minimum, maxItems, nested items/required).
    Returns a list of error strings (empty = valid). No third-party library needed on the build box."""
    errs = []

    def chk(v, sc, path):
        if "type" in sc and not _type_ok(v, sc["type"]):
            errs.append("%s: type" % path)
            return
        if v is None:
            return
        if isinstance(v, str):
            if "maxLength" in sc and len(v) > sc["maxLength"]:
                errs.append("%s: too long" % path)
            if "pattern" in sc and not re.search(sc["pattern"], v):
                errs.append("%s: pattern" % path)
            if "enum" in sc and v not in sc["enum"]:
                errs.append("%s: enum" % path)
        if isinstance(v, (int, float)) and not isinstance(v, bool) and "minimum" in sc and v < sc["minimum"]:
            errs.append("%s: minimum" % path)
        if isinstance(v, dict):
            for k in sc.get("required", []):
                if k not in v:
                    errs.append("%s.%s: required" % (path, k))
            for k, sub in sc.get("properties", {}).items():
                if k in v:
                    chk(v[k], sub, "%s.%s" % (path, k))
        if isinstance(v, list):
            if "maxItems" in sc and len(v) > sc["maxItems"]:
                errs.append("%s: maxItems" % path)
            if "items" in sc:
                for i, it in enumerate(v):
                    chk(it, sc["items"], "%s[%d]" % (path, i))

    if not isinstance(r, dict):
        return ["record: not an object"]
    chk(r, dict(schema, type="object"), r.get("sku") or "record")
    return errs


def _fetch_https(url, key, timeout):
    import urllib.request
    if not url.lower().startswith("https://"):
        raise ValueError("feed url must be https")
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + key, "Accept": "application/json",
                                               "User-Agent": "autoseo-shop-build"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


def _read_key(path):
    p = os.path.expanduser(path or "")
    if not p or not os.path.isfile(p):
        return None
    k = open(p, encoding="utf-8").read().strip()
    return k if k and not k.startswith("#") and "FILL" not in k.upper() else None


def resolve_products(data_dir, fetch=None, write_state=True, now=None):
    """Returns {mode: 'sample'|'live', records: [...], feed_version, reason, report: [...]}.
    fetch(url, key, timeout) -> (status, bytes) is injectable for tests; default = HTTPS GET with Bearer key."""
    import datetime as _dt
    cfg = _read(os.path.join(data_dir, "shop-config.json"))
    schema = _read(os.path.join(data_dir, "product-feed.schema.json"))
    lf = cfg.get("live_feed") or {}
    state_p = os.path.join(data_dir, "live-state.json")
    snap_p = os.path.join(data_dir, "products.live.json")
    state = _read(state_p) if os.path.isfile(state_p) else {"live_seen": False}
    report = []

    def fallback(reason):
        if state.get("live_seen") and os.path.isfile(snap_p):
            snap = _read(snap_p)
            return {"mode": "live", "records": snap.get("products", []), "feed_version": snap.get("feed_version"),
                    "reason": reason + "; using last good live snapshot (site has been live, never back to sample)", "report": report}
        smp = _read(os.path.join(data_dir, "products.sample.json"))
        return {"mode": "sample", "records": smp.get("products", []), "feed_version": smp.get("feed_version"),
                "reason": reason, "report": report}

    url = lf.get("url")
    if not url:
        return fallback("live feed not configured (shop-config.json live_feed.url is null)")
    key = _read_key(lf.get("key_file"))
    if not key:
        return fallback("live feed key file missing or not filled")
    try:
        status, body = (fetch or _fetch_https)(url, key, lf.get("timeout_s", 10))
    except Exception as e:  # network, TLS, timeout
        return fallback("feed fetch failed (%s)" % type(e).__name__)
    if status != 200:
        return fallback("feed HTTP %s" % status)
    try:
        feed = json.loads(body.decode("utf-8") if isinstance(body, bytes) else body)
    except Exception:
        return fallback("feed is not valid JSON")
    prods = feed.get("products") if isinstance(feed, dict) else None
    if not isinstance(prods, list):
        return fallback("feed has no products list")
    bad = [(r.get("sku") if isinstance(r, dict) else "?", e) for r in prods for e in validate_record(r, schema)]
    if bad:
        return fallback("feed failed schema on %d field(s), first: %s %s" % (len(bad), bad[0][0], bad[0][1]))
    if any(r.get("is_sample") for r in prods):
        return fallback("feed contains is_sample=true records")
    active = [r for r in prods if r.get("active")]
    if len(active) < int(lf.get("min_active", 1)):
        return fallback("feed has %d active products (< min_active %s)" % (len(active), lf.get("min_active", 1)))
    deleted = set(feed.get("deleted") or [])
    active = [r for r in active if r.get("slug") not in deleted and r.get("sku") not in deleted]
    at = now or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if write_state:
        with open(snap_p, "w", encoding="utf-8") as f:
            json.dump({"feed_version": feed.get("feed_version"), "generated_at": feed.get("generated_at"), "saved_at": at,
                       "products": active}, f, ensure_ascii=False, indent=1)
        with open(state_p, "w", encoding="utf-8") as f:
            json.dump({"live_seen": True, "feed_version": feed.get("feed_version"), "at": at}, f, indent=1)
    return {"mode": "live", "records": active, "feed_version": feed.get("feed_version"), "reason": "live feed OK", "report": report}


def slugify(s):
    s = re.sub(r"[\"'’]", "", str(s or "").lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def real_sku(sku, is_sample):
    """A SKU may be printed (UI, WhatsApp, schema) only when it is a real AutoCount code, never a SAMPLE- one."""
    return sku if sku and not is_sample and not str(sku).upper().startswith("SAMPLE-") else None


def normalize_products(records, cat_map, brands, category_slugs, mode):
    """Feed records -> site product groups. brands: published brand dicts (slug, name, aliases). Unknown category or
    non-allow-listed brand -> skipped and reported (non-allow-listed brands are never rendered anywhere)."""
    bmap = {}
    for b in brands:
        for n in [b["name"], b["slug"]] + list(b.get("aliases", [])):
            bmap[re.sub(r"[^a-z0-9]", "", n.lower())] = b["slug"]
    cmap = {re.sub(r"\s+", " ", k.strip().lower()): v for k, v in (cat_map.get("map") or {}).items()}
    groups, order, skipped = {}, [], []
    for r in records:
        if not r.get("active"):
            continue
        bslug = bmap.get(re.sub(r"[^a-z0-9]", "", str(r.get("brand") or "").lower()))
        if not bslug:
            skipped.append((r.get("sku"), "brand not on allow-list"))
            continue
        raw_c = re.sub(r"\s+", " ", str(r.get("category") or "").strip().lower())
        cslug = cmap.get(raw_c) or (raw_c if raw_c in category_slugs else None)
        if not cslug and ">" in raw_c:
            cslug = cmap.get(raw_c.split(">")[0].strip())
        if cslug not in category_slugs:
            skipped.append((r.get("sku"), "unknown category %r" % r.get("category")))
            continue
        g = r.get("group") or None
        gid = (g or {}).get("code") or r["sku"]
        v = {"sku": r["sku"], "real_sku": real_sku(r["sku"], bool(r.get("is_sample"))), "label": (g or {}).get("variant_label") or "",
             "unit": r.get("unit") or "", "model": r.get("model") or "",
             "prices": [p for p in (r.get("prices") or []) if p.get("amount")], "stock": r.get("stock") or [],
             "barcode": r.get("barcode")}
        if gid not in groups:
            name = (g or {}).get("name") or r.get("title")
            slug = slugify(name) if g else (r.get("slug") or slugify(r.get("title")))
            groups[gid] = {"id": gid, "slug": slug, "name": name, "brand": bslug, "category": cslug,
                           "model": r.get("model") or "", "description": r.get("description"),
                           "short": r.get("short_description"), "specs": [s for s in (r.get("specs") or []) if s.get("key") != "Pack size"],
                           "images": [{"src": i["url"], "alt": i.get("alt", "")} for i in (r.get("images") or [])],
                           "is_sample": bool(r.get("is_sample")), "status": "active", "variants": [],
                           "indexable": not r.get("is_sample")}
            order.append(gid)
        grp = groups[gid]
        grp["variants"].append(v)
        if not grp["images"] and r.get("images"):
            grp["images"] = [{"src": i["url"], "alt": i.get("alt", "")} for i in r["images"]]
        grp["is_sample"] = grp["is_sample"] or bool(r.get("is_sample"))
    out = [groups[g] for g in order]
    seen = {}
    for p in out:
        if p["slug"] in seen:
            p["slug"] = p["slug"] + "-" + slugify(p["id"])[-6:]
        seen[p["slug"]] = 1
        for v in p["variants"]:
            v["sample"] = p["is_sample"]
    return out, skipped
