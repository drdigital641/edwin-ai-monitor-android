"""Standalone listing template for the car workshop directory (separate domain, not bought yet).

Domain-agnostic: nothing here depends on build.py or on pageonesingapore.com. The base URL is passed in.
    from directory_listing import listing_page
    html = listing_page(data, base_url="https://example-directory.sg")   # returns the page as a string
    write_listing(data, base_url, out_root)                              # writes <out_root>/<trade_slug>/<slug>/index.html

data keys: name, trade, slug, area, services[list], hours[list of {label, days[list], opens, closes}], phone,
whatsapp (digits, country code), photos[list of {src, alt, width, height}], gbp_url (optional), about (text),
trade_slug (optional, derived from trade), updated (optional YYYY-MM-DD).
Rules: only facts given in `data` appear; no review/rating schema (third-party Google reviews are banned in schema);
the Google Business Profile is a plain link. WhatsApp links carry data-cta="whatsapp_directory_<slug>" so the
site's tap counter (the same click handler as Page One's main.js: any wa.me link whose data-cta starts with
"whatsapp") can count them; pass tap_script="/main.js" or the counter's URL to include it.
"""
import html as _h
import json
import os
import re
from urllib.parse import quote


def _slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def _e(x):
    return _h.escape(str(x), quote=True)


def listing_url(data, base_url):
    return f"{base_url.rstrip('/')}/{data.get('trade_slug') or _slugify(data['trade'])}/{data['slug']}/"


def _jsonld(data, url):
    ld = {"@context": "https://schema.org", "@type": "LocalBusiness", "@id": url + "#business", "name": data["name"], "url": url}
    if data.get("about"):
        ld["description"] = data["about"]
    if data.get("phone"):
        ld["telephone"] = data["phone"]
    if data.get("area"):
        ld["areaServed"] = {"@type": "Place", "name": data["area"]}
    if data.get("photos"):
        ld["image"] = [p["src"] for p in data["photos"]]
    if data.get("services"):
        ld["makesOffer"] = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s}} for s in data["services"]]
    if data.get("hours"):
        ld["openingHoursSpecification"] = [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["opens"], "closes": h["closes"]} for h in data["hours"]]
    if data.get("gbp_url"):
        ld["hasMap"] = data["gbp_url"]
        ld["sameAs"] = [data["gbp_url"]]
    return ld


_CSS = """
:root{--bg:#fff;--fg:#0f172a;--muted:#475569;--line:#e2e8f0;--accent:#128c7e;--card:#f8fafc}
@media (prefers-color-scheme:dark){:root{--bg:#0b1220;--fg:#e2e8f0;--muted:#94a3b8;--line:#1e293b;--accent:#25d366;--card:#111a2e}}
*{box-sizing:border-box}body{margin:0;font:16px/1.6 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:var(--bg);color:var(--fg)}
.w{max-width:760px;margin:0 auto;padding:0 16px}h1{font-size:1.9rem;line-height:1.2;margin:24px 0 4px}h2{font-size:1.2rem;margin:28px 0 8px}
.sub{color:var(--muted);margin:0 0 16px}.btns{display:flex;flex-wrap:wrap;gap:10px;margin:16px 0}
.b{display:inline-block;padding:12px 18px;border-radius:10px;border:1px solid var(--accent);color:var(--fg);text-decoration:none;font-weight:600;transition:transform .2s}
.b.p{background:var(--accent);color:#fff}.b:hover{transform:translateY(-2px)}
@media (prefers-reduced-motion:reduce){.b{transition:none}.b:hover{transform:none}}
.ph{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:10px;margin:12px 0}.ph img{width:100%;height:auto;border-radius:10px;background:var(--card)}
ul{padding-left:20px}table{border-collapse:collapse;width:100%}th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line)}
.fine{color:var(--muted);font-size:.85rem;margin:32px 0 24px}
"""


def listing_page(data, base_url, tap_script=None):
    url = listing_url(data, base_url)
    name, trade, area = data["name"], data["trade"], data.get("area", "")
    title = f"{name}: {trade}" + (f" in {area}" if area else "")
    desc = (data.get("about") or title)[:155]
    msg = f"Hi {name}, I found your listing and would like to ask about your services.\n\n(From {url})"
    wa = f"https://wa.me/{re.sub(r'[^0-9]', '', data['whatsapp'])}?text={quote(msg)}" if data.get("whatsapp") else ""
    btns = []
    if wa:
        btns.append(f'<a class="b p" href="{_e(wa)}" target="_blank" rel="noopener" data-cta="whatsapp_directory_{_e(data["slug"])}">WhatsApp us</a>')
    if data.get("phone"):
        btns.append(f'<a class="b" href="tel:{_e(re.sub(r"[^0-9+]", "", data["phone"]))}">Call {_e(data["phone"])}</a>')
    if data.get("gbp_url"):
        btns.append(f'<a class="b" href="{_e(data["gbp_url"])}" target="_blank" rel="noopener">See us on Google Maps</a>')
    photos = "".join(
        f'<img src="{_e(p["src"])}" alt="{_e(p["alt"])}" width="{int(p["width"])}" height="{int(p["height"])}" loading="lazy">' for p in data.get("photos", []))
    services = "".join(f"<li>{_e(s)}</li>" for s in data.get("services", []))
    hours = "".join(f'<tr><th scope="row">{_e(h["label"])}</th><td>{_e(h["opens"])} to {_e(h["closes"])}</td></tr>' for h in data.get("hours", []))
    about = "".join(f"<p>{_e(p)}</p>" for p in (data.get("about") or "").split("\n\n") if p.strip())
    ld = json.dumps(_jsonld(data, url), ensure_ascii=False, indent=2).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(title)}</title>
<meta name="description" content="{_e(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{_e(url)}">
<style>{_CSS}</style>
<script type="application/ld+json">
{ld}
</script>
</head>
<body>
<main class="w">
<h1>{_e(name)}</h1>
<p class="sub">{_e(trade)}{(" in " + _e(area)) if area else ""}</p>
<div class="btns">{"".join(btns)}</div>
{f'<div class="ph">{photos}</div>' if photos else ""}
{f"<h2>About</h2>{about}" if about else ""}
{f"<h2>Services</h2><ul>{services}</ul>" if services else ""}
{f'<h2>Opening hours</h2><table><tbody>{hours}</tbody></table>' if hours else ""}
<div class="btns">{"".join(btns)}</div>
<p class="fine">Listing details were supplied by the business. WhatsApp taps on this page are counted and reported to the business each month.</p>
</main>
{f'<script src="{_e(tap_script)}" defer></script>' if tap_script else ""}
</body>
</html>
"""


def write_listing(data, base_url, out_root, **kw):
    path = os.path.join(out_root, data.get("trade_slug") or _slugify(data["trade"]), data["slug"], "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(listing_page(data, base_url, **kw))
    return path
