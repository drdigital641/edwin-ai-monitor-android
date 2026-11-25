#!/usr/bin/env python3
"""BIY Home Store preview build (AutoSEO.my, 25 Nov 2026). Phase 1: catalogue + WhatsApp enquiry, no cart.

Data layer (AutoCount-ready): data/facts.json, brands.json, categories.json, products.json, synonyms.json.
Adding a product = add a row to products.json and rebuild. Nothing else.
Copy: strings/en.json written once (Rule 6); strings/ms.json + zh.json from the cheap translation step only.
Shared template parts: autoseo-template/autoseo_i18n.py, golive/golive.py, privacy/privacy_page.py, shop/ (shop.py,
shop.js, shop.css). One switch go-live: site.json go_live_domain.

  python3 build.py [--out DIR]        builds into ../site (default), runs every gate, exits 1 on any failure
"""
import json, os, re, sys, hashlib, shutil, datetime
from html import escape as E

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.environ.get("AUTOSEO_TEMPLATE", "/mnt/project-files/autoseo-template")
for p in (TPL, os.path.join(TPL, "golive"), os.path.join(TPL, "privacy"), os.path.join(TPL, "shop")):
    sys.path.insert(0, p)
import autoseo_i18n as I18N
import golive
import privacy_page
import shop

OUT = os.path.join(HERE, "..", "site")
if "--out" in sys.argv:
    OUT = sys.argv[sys.argv.index("--out") + 1]
OUT = os.path.abspath(OUT)
DATA = os.environ.get("BIY_DATA", os.path.join(HERE, "data"))

SITE = json.load(open(os.path.join(HERE, "site.json")))
CFG = golive.Cfg(SITE)
P = CFG.base_path                       # '/preview/biy-home-store' on preview, '' when live
CAT = shop.load_catalog(DATA)
F = CAT["facts"]
SYN = json.load(open(os.path.join(DATA, "synonyms.json")))
LANGS = I18N.build_langs(SITE.get("malaysian_address", True))
S = {L["code"]: json.load(open(os.path.join(HERE, "strings", L["code"] + ".json"), encoding="utf-8")) for L in LANGS}
WA_E164 = F["whatsapp"]["e164"]
WA_NUM = re.sub(r"\D", "", WA_E164)
TEL = F["main_phone_for_call_cta"]["tel"]
TEL_D = F["main_phone_for_call_cta"]["display"]
BR = F["branches"]
HQ = next(b for b in BR if b.get("is_hq"))
TODAY = datetime.date(2026, 11, 25).isoformat()
MISSING = []


def t(L, key, **kw):
    s = S[L["code"]].get(key)
    if s is None:
        MISSING.append((L["code"], key))
        s = S["en"].get(key, key)
    return shop.fill(s, **kw) if kw else s


def u(path=""):
    return P + "/" + path


def lp(L, path=""):
    return I18N.page_path(L, path)


def absu(path=""):
    return CFG.canon(path)


def ver(fn):
    return hashlib.sha256(open(os.path.join(OUT, fn), "rb").read()).hexdigest()[:8]


# ------------------------------------------------------------------ icons (authored line SVG, one stroke weight)
def svg(d, fill=False, cls=""):
    c = f' class="{cls}"' if cls else ""
    if fill:
        return f'<svg{c} viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{d}"/></svg>'
    return (f'<svg{c} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
            f'stroke-linejoin="round" aria-hidden="true">{d}</svg>')


IC = {
    "paint-roller": svg('<rect x="3" y="3.5" width="14" height="6" rx="2"/><path d="M17 6.5h2.5a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1H12v2.5"/><rect x="10" y="14" width="4" height="7" rx="1.2"/>'),
    "drill": svg('<path d="M3 6.5h10.5a2.5 2.5 0 0 1 2.5 2.5v1a2.5 2.5 0 0 1-2.5 2.5H3z"/><path d="M16 9.5h5M19 8v3"/><path d="M6.5 12.5 5.5 20h4l1-7.5"/><path d="M3 9.5h2.5"/>'),
    "wrench": svg('<path d="M14.6 6.4a4 4 0 0 0-5.3 5.3L3.5 17.5a2.1 2.1 0 0 0 3 3l5.8-5.8a4 4 0 0 0 5.3-5.3l-2.6 2.6-2.4-.6-.6-2.4z"/>'),
    "bricks": svg('<rect x="3" y="4" width="18" height="16" rx="1.6"/><path d="M3 9.3h18M3 14.7h18M9.5 4v5.3M14.5 9.3v5.4M9.5 14.7V20"/>'),
    "search": svg('<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>'),
    "wa": svg("M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.1-1.2l-.5-.3z", fill=True),
    "phone": svg('<path d="M21 16.4v2.8a1.9 1.9 0 0 1-2 1.9 18.6 18.6 0 0 1-8.1-2.9 18.3 18.3 0 0 1-5.6-5.6A18.6 18.6 0 0 1 2.4 4.5a1.9 1.9 0 0 1 1.9-2h2.8a1.9 1.9 0 0 1 1.9 1.6c.1.9.3 1.7.6 2.5a1.9 1.9 0 0 1-.4 2l-1.2 1.2a15 15 0 0 0 5.6 5.6l1.2-1.2a1.9 1.9 0 0 1 2-.4c.8.3 1.6.5 2.5.6a1.9 1.9 0 0 1 1.7 2z"/>'),
    "pin": svg('<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.4"/>'),
    "home": svg('<path d="M4 10.5 12 4l8 6.5V20a1 1 0 0 1-1 1h-4.5v-6h-5v6H5a1 1 0 0 1-1-1z"/>'),
    "grid": svg('<rect x="4" y="4" width="6.5" height="6.5" rx="1.8" transform="rotate(-6 7.25 7.25)"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.8"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.8"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.8"/>'),
    "store": svg('<path d="M4 9.5 5.5 4h13L20 9.5"/><path d="M4 9.5a2.7 2.7 0 0 0 5.3 0 2.7 2.7 0 0 0 5.4 0 2.7 2.7 0 0 0 5.3 0"/><path d="M5 11.5V20h14v-8.5M10 20v-5h4v5"/>'),
    "arrow": svg('<path d="M5 12h14M13 6l6 6-6 6"/>'),
    "ext": svg('<path d="M14 4h6v6M20 4l-9 9"/><path d="M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/>'),
    "menu": svg('<path d="M4 7h16M4 12h16M4 17h16"/>'),
    "close": svg('<path d="M6 6l12 12M18 6 6 18"/>'),
    "fb": svg('<path d="M14.5 21v-7.5h2.6l.4-3h-3V8.6c0-.9.3-1.5 1.5-1.5h1.6V4.4a21 21 0 0 0-2.3-.1c-2.3 0-3.9 1.4-3.9 4v2.2H8.8v3h2.6V21"/>'),
    "list": svg('<path d="M9 6h11M9 12h11M9 18h11"/><rect x="3.5" y="4.5" width="3" height="3" rx=".8"/><rect x="3.5" y="10.5" width="3" height="3" rx=".8"/><rect x="3.5" y="16.5" width="3" height="3" rx=".8"/>'),
}


# ------------------------------------------------------------------ CTA helpers (one place: same data-cta/data-ref on every language)
def default_branch():
    return HQ["short"]


def wa(L, key, ref, label, cls="btn btn-wa", icon=True, **v):
    tpl = t(L, key, **v)
    text = shop.fill(tpl, branch=v.get("branch") or default_branch())
    dyn = "{branch}" in tpl and not v.get("branch")
    extra = f' data-wa-tpl="{E(tpl)}" data-wa-num="{WA_NUM}"' if dyn else ""
    ic = IC["wa"] if icon else ""
    return (f'<a class="{cls}" href="{E(shop.wa_url(WA_E164, text))}" target="_blank" rel="noopener" data-cta="whatsapp" '
            f'data-ref="{ref}"{extra}>{ic}<span>{label}</span></a>')


def call(L, ref, label=None, tel=TEL, cls="btn btn-line"):
    return f'<a class="{cls}" href="tel:{tel}" data-cta="call" data-ref="{ref}">{IC["phone"]}<span>{label or t(L, "ui.call")}</span></a>'


def directions(L, br, cls="btn btn-line", label=None):
    return (f'<a class="{cls}" href="{E(shop.maps_search(br["address_line"]))}" target="_blank" rel="noopener" data-cta="directions" '
            f'data-ref="directions_{br["slug"].replace("-", "_")}">{IC["pin"]}<span>{label or t(L, "ui.directions")}</span></a>')


def fb(L, ref, cls="tlink"):
    return f'<a class="{cls}" href="{E(F["facebook"])}" target="_blank" rel="noopener" data-cta="facebook" data-ref="{ref}">{IC["fb"]}<span>{t(L, "ui.facebook_page")}</span></a>'


def ext(href, label, cls="src"):
    return f'<a class="{cls}" href="{E(href)}" target="_blank" rel="noopener">{E(label)}{IC["ext"]}</a>'


# ------------------------------------------------------------------ data helpers
def brand_name(b):
    return b.get("name")


def cat_name(L, c, short=False):
    return t(L, f"cat.{c['slug']}.{'short' if short else 'name'}")


def dtx(L, s):
    return t(L, "data." + s) if s else ""


def products_of(**kw):
    return [p for p in CAT["products"] if all(p.get(k) == v for k, v in kw.items())]


def pname(b, p):
    """Product name for a prefill that already starts with {brand}: drop a leading brand word (no 'Bosch Bosch')."""
    n = p["name"]
    return n[len(b["name"]):].strip() if n.lower().startswith(b["name"].lower() + " ") else n


def range_source(b):
    return b.get("ranges_source", "").split(" ")[0]


# ------------------------------------------------------------------ shared chrome
def head(L, path, title, desc, graph, noindex=False):
    code = L["code"]
    robots = '<meta name="robots" content="noindex,follow">\n' if noindex else ""
    css = f'{u("assets/site.css")}?v={VER["css"]}'
    return f"""<!doctype html>
<html lang="{L['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
{robots}{golive.head_tags(CFG, path, code)}
<meta property="og:type" content="website">
<meta property="og:site_name" content="BIY Home Store">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image:alt" content="BIY Home Store logo: hardware, paint and power tools in Kota Tinggi, Kota Masai and Pontian">
{I18N.og_locale_tags(L)}
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="theme-color" content="#2B2B2B">
<link rel="icon" type="image/png" sizes="32x32" href="{u('images/icon-32.png')}">
<link rel="apple-touch-icon" href="{u('images/icon-180.png')}">
<link rel="manifest" href="{u('site.webmanifest')}">
<link rel="preload" as="font" type="font/woff2" href="{u('assets/fonts/archivo.woff2')}" crossorigin>
<link rel="stylesheet" href="{css}">
{shop.ld_script(graph)}
</head>"""


def org_ld():
    return shop.ld_org(F, absu(""), absu("images/logo-mark.png"), absu("#org"))


def crumbs_ld(L, items):
    return shop.ld_breadcrumb([(t(L, "ui.home"), absu(lp(L, "")))] + [(n, absu(lp(L, p))) for n, p in items])


def crumbs_html(L, items):
    lis = [f'<li><a href="{u(lp(L, ""))}">{t(L, "ui.home")}</a></li>']
    for i, (n, p) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{E(n)}</li>')
        else:
            lis.append(f'<li><a href="{u(lp(L, p))}">{E(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="{t(L, "ui.breadcrumb")}"><ol>{"".join(lis)}</ol></nav>'


NAV = [("category/", "ui.categories"), ("brand/", "ui.brands"), ("stores/", "ui.stores"),
       ("contractors/", "ui.contractors"), ("articles/", "ui.articles"), ("about/", "ui.about"), ("contact/", "ui.contact")]


def header(L, path, home=False):
    nav = "".join(f'<a href="{u(lp(L, p))}"{" aria-current=page" if path.startswith(p) else ""}>{t(L, k)}</a>' for p, k in NAV)
    sw = I18N.switcher(u, path, L, t(L, "ui.lang_aria"), cls="lsw")
    sf = shop.search_form(u(lp(L, "search/")), t(L, "ui.search_label"), t(L, "ui.search_ph_short"),
                          IC["search"] + f'<span class="vh">{t(L, "ui.search_btn")}</span>', ref="search_header")
    sheet_links = "".join(f'<a class="sl" href="{u(lp(L, p))}"><span>{t(L, k)}</span>{IC["arrow"]}</a>' for p, k in [("", "ui.home")] + NAV)
    return f"""<body{BODY_ATTR}>
<a class="skip" href="#main">{t(L, 'ui.skip')}</a>
<header class="hd{' hd-home' if home else ''}"><div class="hd-in">
<a class="hd-logo" href="{u(lp(L, ''))}"><img src="{u('images/logo-mark-96.webp')}" width="96" height="98" alt="BIY Home Store"><span class="hd-name">BIY Home Store</span></a>
<div class="hd-search">{sf}</div>
<nav class="hd-nav" aria-label="{t(L, 'ui.main_nav')}">{nav}</nav>
{sw}
{wa(L, 'wa.general', 'whatsapp_header', t(L, 'ui.wa'), cls='btn btn-wa hd-wa')}
<button class="mbtn" id="mopen" type="button" aria-controls="sheet" aria-expanded="false" aria-label="{t(L, 'ui.menu')}">{IC['menu']}</button>
</div></header>
<div class="sheet" id="sheet" aria-hidden="true" role="dialog" aria-modal="true" aria-label="{t(L, 'ui.menu')}"><div class="sheet-in">
<div class="sheet-top"><img src="{u('images/logo-mark-96.webp')}" width="96" height="98" alt="BIY Home Store"><button class="mbtn" id="mclose" type="button" aria-label="{t(L, 'ui.menu_close')}">{IC['close']}</button></div>
{sheet_links}
<div class="sheet-cta">{wa(L, 'wa.general', 'whatsapp_menu', t(L, 'ui.wa_us'))}{call(L, 'call_menu', t(L, 'ui.call_num', num=TEL_D))}</div>
</div></div>"""


def footer(L, path):
    cats = "".join(f'<li><a href="{u(lp(L, "category/" + c["slug"] + "/"))}">{cat_name(L, c)}</a></li>' for c in CAT["categories"])
    brands = "".join(f'<li><a href="{u(lp(L, "brand/" + b["slug"] + "/"))}">{E(b["name"])}</a></li>' for b in CAT["brands"])
    stores = "".join(f'<li><a href="{u(lp(L, "stores/" + b["slug"] + "/"))}"><b>{E(b["short"])}</b><small>{E(b["address_line"])}</small></a></li>' for b in BR)
    bar = [("", "home", "ui.home"), ("category/", "grid", "ui.categories"), ("search/", "search", "ui.search")]
    items = "".join(f'<a class="mb-i" href="{u(lp(L, p))}">{IC[i]}<span>{t(L, k)}</span></a>' for p, i, k in bar)
    items += wa(L, "wa.general", "whatsapp_mobile_bar", t(L, "ui.wa"), cls="mb-i mb-wa")
    items += f'<a class="mb-i" href="{u(lp(L, "stores/"))}">{IC["store"]}<span>{t(L, "ui.stores")}</span></a>'
    return f"""<footer class="ft"><div class="wrap">
<div class="ft-brand"><img src="{u('images/logo-mark-192.webp')}" width="192" height="197" alt="BIY Home Store" loading="lazy"><p>{E(F['tagline_from_own_site'])}</p></div>
<div class="ft-cols">
<div><h2>{t(L, 'ui.footer_cats')}</h2><ul>{cats}</ul></div>
<div><h2>{t(L, 'ui.footer_brands')}</h2><ul>{brands}</ul></div>
<div class="ft-stores"><h2>{t(L, 'ui.footer_stores')}</h2><ul>{stores}</ul></div>
<div><h2>{t(L, 'ui.footer_follow')}</h2><ul class="ft-talk">
<li>{wa(L, 'wa.general', 'whatsapp_footer', 'WhatsApp ' + E(F['whatsapp']['display']), cls='tlink')}</li>
<li>{call(L, 'call_footer', t(L, 'ui.call_num', num=TEL_D), cls='tlink')}</li>
<li>{fb(L, 'facebook_footer')}</li>
<li><small>{t(L, 'ui.hours_note')}</small></li></ul></div>
</div>
<div class="ft-bot"><span>{t(L, 'ui.copyright')}</span><span>{I18N.privacy_link(u, L)} <a href="https://autoseo.my/" target="_blank" rel="noopener">{t(L, 'ui.footer_credit')}</a></span></div>
</div></footer>
<nav class="mbar" aria-label="{t(L, 'ui.bottom_nav')}">{items}</nav>
<script type="application/json" id="branches-data">{json.dumps({b['slug']: b['short'] for b in BR}, ensure_ascii=False)}</script>
<script src="{u('assets/shop.js')}?v={VER['js']}" defer></script>
<script src="{u('assets/p1-cta.js')}?v={VER['cta']}" defer></script>
</body>
</html>
"""


# ------------------------------------------------------------------ blocks
def cat_tile(L, c):
    return (f'<a class="ct" href="{u(lp(L, "category/" + c["slug"] + "/"))}" data-select-category="{c["slug"]}">'
            f'<span class="tsq">{IC[c["icon"]]}</span><span class="ct-t"><b>{cat_name(L, c)}</b><small>{t(L, "cat." + c["slug"] + ".desc")}</small></span>'
            f'{IC["arrow"]}</a>')


def cat_icon(L, c):
    return (f'<a class="hi" href="{u(lp(L, "category/" + c["slug"] + "/"))}" data-select-category="{c["slug"]}">'
            f'<span class="hi-i">{IC[c["icon"]]}</span><span class="hi-t">{cat_name(L, c, True)}</span></a>')


def brand_card(L, b):
    return (f'<a class="bw bw-{b["slug"]}" href="{u(lp(L, "brand/" + b["slug"] + "/"))}"><span class="bw-mark">{E(b["name"])}</span>'
            f'<small>{t(L, "brand." + b["slug"] + ".tag")} · {len(b["ranges"])} {t(L, "ui.ranges").lower()}</small></a>')


def range_card(L, b, r, ref="whatsapp_range"):
    c = CAT["category"][b["category"]]
    btn = wa(L, "wa.range", ref, t(L, "ui.wa_ask_range"), cls="btn btn-wa btn-sm", brand=b["name"], range=r["name"])
    return (f'<article class="rg">{shop.product_frame(IC[c["icon"]], b["name"], None, cls="pf")}'
            f'<div class="rg-b"><small>{dtx(L, r["type"])}</small><h3>{E(r["name"])}</h3><p>{dtx(L, r["brand_site_note"])}</p>{btn}</div></article>')


def product_card(L, p):
    b = CAT["brand"][p["brand"]]
    c = CAT["category"][p["category"]]
    url = u(lp(L, "product/" + p["slug"] + "/"))
    img = [dict(i, src=u(i["src"])) for i in p.get("images") or []]
    return (f'<article class="pc"><a class="pc-a" href="{url}">{shop.product_frame(IC[c["icon"]], b["name"], img, alt=p["name"], cls="pf")}'
            f'<small>{E(b["name"])}</small><h3>{E(p["name"])}</h3><span class="pc-m">{t(L, "ui.model")} {E(p.get("model") or "")}</span></a>'
            f'<span class="stock">{t(L, "ui.stock." + shop.stock_label_key(p))}</span>'
            f'{wa(L, "wa.product_no_sku" if not p.get("sku") else "wa.product", "whatsapp_product_card", t(L, "ui.wa_price"), cls="btn btn-wa btn-sm", brand=b["name"], name=pname(b, p), sku=p.get("sku") or "", variant="", url=absu(lp(L, "product/" + p["slug"] + "/")))}</article>')


def branch_card(L, br, ref_wa="whatsapp_branch"):
    return (f'<article class="bc"><span class="tsq tsq-s">{IC["store"]}</span><h3><a href="{u(lp(L, "stores/" + br["slug"] + "/"))}">{E(br["short"])}</a></h3>'
            f'<p class="bc-a">{E(br["address_line"])}</p><p class="bc-h">{t(L, "ui.hours_note")}</p>'
            f'<div class="bc-cta">{wa(L, "wa.branch", ref_wa, t(L, "ui.wa"), cls="btn btn-wa btn-sm", branch=br["short"])}{directions(L, br, cls="btn btn-line btn-sm")}</div></article>')


def branch_picker(L):
    chips = "".join(f'<button type="button" class="bp-c" data-branch-pick="{b["slug"]}" aria-pressed="{"true" if b is HQ else "false"}">{E(b["short"])}</button>' for b in BR)
    return f'<div class="bp" role="group" aria-label="{t(L, "ui.branch_pick")}"><span class="bp-l">{t(L, "ui.branch_pick")}</span><div class="bp-row">{chips}</div></div>'


def band(inner, cls="", id_=""):
    i = f' id="{id_}"' if id_ else ""
    return f'<section class="band {cls}"{i}><div class="wrap">{inner}</div></section>'


def page_top(L, items, h1, lead="", extra=""):
    lead_h = f'<p class="lead">{lead}</p>' if lead else ""
    return f'<section class="ptop"><div class="wrap">{crumbs_html(L, items)}<h1>{E(h1)}</h1>{lead_h}{extra}</div></section>'


# ------------------------------------------------------------------ pages
PAGES = []          # (path, indexable)
OUTFILES = {}       # site path -> html


def emit(L, path, title, desc, graph, main, noindex=False, home=False):
    html = head(L, path, title, desc, graph, noindex) + "\n" + header(L, path, home) + f'\n<main id="main">{main}</main>\n' + footer(L, path)
    OUTFILES[lp(L, path)] = html


def home_feed(L, n=12):
    """Shopee-style 2-column feed: real products first, then brand ranges taken round-robin across brands."""
    cards = [product_card(L, p) for p in products_of()]
    queues = [[(b, r) for r in b["ranges"]] for b in CAT["brands"]]
    while len(cards) < n and any(queues):
        for q in queues:
            if q and len(cards) < n:
                b, r = q.pop(0)
                c = CAT["category"][b["category"]]
                cards.append(f'<article class="pc pc-rg">{shop.product_frame(IC[c["icon"]], b["name"], None, cls="pf")}'
                             f'<small class="pc-b">{E(b["name"])}</small><h3>{E(r["name"])}</h3><span class="pc-m">{dtx(L, r["type"])}</span>'
                             f'<span class="stock">{t(L, "ui.stock.check")}</span>'
                             f'{wa(L, "wa.range", "whatsapp_range", t(L, "ui.wa_price"), cls="btn btn-wa btn-sm", brand=b["name"], range=r["name"])}</article>')
    return cards


def sec_head(L, h, href):
    return f'<div class="hm-h"><h2>{h}</h2><a href="{u(lp(L, href))}">{t(L, "ui.view_all")}{IC["arrow"]}</a></div>'


def p_home(L):
    chips = [(f'category/{c["slug"]}/', cat_name(L, c, True), c["slug"]) for c in CAT["categories"]] + \
            [(f'brand/{b["slug"]}/', b["name"], "") for b in CAT["brands"]]
    chip_h = "".join(f'<a class="chip" href="{u(lp(L, p))}"{(" data-select-category=" + chr(34) + s + chr(34)) if s else ""}>{E(n)}</a>' for p, n, s in chips)
    sf = shop.search_form(u(lp(L, "search/")), t(L, "ui.search_label"), t(L, "ui.search_ph_short"),
                          IC["search"] + f'<span>{t(L, "ui.search_btn")}</span>', big=True, ref="search_home_hero")
    # 1. search first (the star), quick chips under it
    top = f"""<section class="hm-top"><div class="wrap">
<div id="hero-search">{sf}</div>
<nav class="chips" aria-label="{t(L, 'home.chips_label')}">{chip_h}</nav>
</div></section>"""
    # 2. banner row: main banner (small H1) + two side cards
    banner = f"""<section class="hm-bnr"><div class="wrap hm-bnr-in">
<div class="hm-bn"><div class="hero-motif" aria-hidden="true"><i></i><i></i><i></i></div>
<h1>{t(L, 'home.h1')}</h1><p>{t(L, 'home.lead')}</p>
{wa(L, 'wa.general', 'whatsapp_home_hero', t(L, 'ui.wa_us'), cls='btn btn-wa-w btn-sm')}</div>
<div class="hm-side">
<a class="hm-sc" href="{u(lp(L, 'stores/'))}"><span class="tsq tsq-s">{IC['store']}</span><b>{t(L, 'home.branches_h')}</b><small>{t(L, 'home.branches_lead')}</small></a>
<div class="hm-sc hm-sc-d"><span class="tsq tsq-s">{IC['list']}</span><b>{t(L, 'home.trade_h')}</b>{wa(L, 'wa.contractor', 'whatsapp_contractors_home', t(L, 'ui.wa_quote'), cls='tlink', icon=False)}</div>
</div></div></section>"""
    # 3. icon grid (categories + shortcuts)
    ic_items = [cat_icon(L, c) for c in CAT["categories"]]
    for href, icon, key in [("brand/", "grid", "ui.brands"), ("stores/", "pin", "ui.stores"),
                            ("contractors/", "list", "ui.contractors"), ("contact/", "phone", "ui.contact")]:
        ic_items.append(f'<a class="hi" href="{u(lp(L, href))}"><span class="hi-i">{IC[icon]}</span><span class="hi-t">{t(L, key)}</span></a>')
    icons = f'<section class="hm-sec"><div class="wrap"><div class="hm-card"><h2>{t(L, "home.cats_h")}</h2><div class="hi-grid">{"".join(ic_items)}</div></div></div></section>'
    # 4. brands row
    bt = "".join(f'<a class="hb" href="{u(lp(L, "brand/" + b["slug"] + "/"))}"><span class="hb-m">{E(b["name"])}</span><small>{t(L, "brand." + b["slug"] + ".tag")}</small></a>' for b in CAT["brands"])
    brands = f'<section class="hm-sec"><div class="wrap"><div class="hm-card">{sec_head(L, t(L, "home.brands_h"), "brand/")}<div class="hb-grid">{bt}</div></div></div></section>'
    # 5. product feed
    feed = f'<section class="hm-sec"><div class="wrap"><div class="hm-feed-h">{sec_head(L, t(L, "ui.products") + " · " + t(L, "ui.ranges"), "brand/")}</div>' \
           f'<div class="pc-grid hm-feed">{"".join(home_feed(L))}</div><p class="fine">{t(L, "ui.note_price")}</p></div></section>'
    # 6. branches, how to enquire, proof, FAQ
    strip = "".join(f'<a class="bs" href="{u(lp(L, "stores/" + b["slug"] + "/"))}"><b>{E(b["short"])}</b><small>{E(b["city"])}</small></a>' for b in BR)
    branches = f'<section class="hm-sec"><div class="wrap"><div class="hm-card">{sec_head(L, t(L, "home.branches_h"), "stores/")}<div class="bs-strip">{strip}</div></div></div></section>'
    steps = "".join(f'<li><span class="sq-n">{i}</span><b>{t(L, f"home.step{i}_t")}</b><span>{t(L, f"home.step{i}_d")}</span></li>' for i in (1, 2, 3))
    steps = f'<section class="hm-sec"><div class="wrap"><div class="hm-card"><h2>{t(L, "home.steps_h")}</h2><ol class="track">{steps}</ol></div></div></section>'
    proof_items = [("nippon-paint", "home.proof.nippon", CAT["brand"]["nippon-paint"]["evidence_url"]),
                   ("dong-cheng", "home.proof.dongcheng", CAT["brand"]["dong-cheng"]["evidence_url"]),
                   ("jotun", "home.proof.jotun", CAT["brand"]["jotun"]["evidence_url"])]
    pc = "".join(f'<li class="ev"><span class="ev-b">{E(CAT["brand"][s]["name"])}</span><p>{t(L, k)}</p>{ext(href, t(L, "home.proof.open"))}</li>' for s, k, href in proof_items)
    proof = f'<section class="hm-sec"><div class="wrap"><div class="hm-card"><div class="sec-h"><h2>{t(L, "home.proof_h")}</h2><p>{t(L, "home.proof_lead")}</p></div><ul class="ev-grid">{pc}</ul></div></div></section>'
    faqs = [(t(L, f"faq.{k}_q"), t(L, f"faq.{k}_a")) for k in ("price", "branches", "hours", "biy", "brands")]
    fq = "".join(f'<details class="fq"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faqs)
    faq = f'<section class="hm-sec hm-last"><div class="wrap"><div class="hm-card"><h2>{t(L, "home.faq_h")}</h2><div class="fq-list">{fq}</div></div></div></section>'
    graph = [org_ld(), shop.ld_website("BIY Home Store", absu(lp(L, "")), absu(lp(L, "search/")), L["hreflang"], absu("#website")),
             shop.ld_faq(faqs)]
    main = '<div class="hm">' + top + banner + icons + brands + feed + branches + steps + proof + faq + '</div>'
    emit(L, "", t(L, "home.title"), t(L, "home.meta"), graph, main, home=True)


def p_cat_index(L):
    main = page_top(L, [(t(L, "cat.index.h1"), "category/")], t(L, "cat.index.h1"), t(L, "cat.index.lead")) + \
        band(f'<div class="ct-grid">{"".join(cat_tile(L, c) for c in CAT["categories"])}</div>', "band-rise")
    emit(L, "category/", t(L, "cat.index.title"), t(L, "cat.index.meta"), [org_ld(), crumbs_ld(L, [(t(L, "cat.index.h1"), "category/")])], main)


def p_category(L, c):
    path = f'category/{c["slug"]}/'
    items = [(t(L, "ui.categories"), "category/"), (cat_name(L, c), path)]
    brands = [CAT["brand"][s] for s in c.get("brands", []) if s in CAT["brand"]]
    cta = wa(L, "wa.category", "whatsapp_category", t(L, "ui.wa_us"), category=cat_name(L, c))
    top = page_top(L, items, t(L, f"cat.{c['slug']}.h1"), t(L, f"cat.{c['slug']}.intro"), f'<div class="ptop-cta">{cta}</div>')
    body = ""
    if brands:
        body += band(f'<h2>{t(L, "ui.brands_in_cat")}</h2><div class="bw-row">{"".join(brand_card(L, b) for b in brands)}</div>', "band-rise")
        for b in brands:
            body += band(f'<div class="sec-h"><h2>{t(L, "ui.ranges_of", brand=b["name"])}</h2><p class="note">{t(L, "ui.stock_note")}</p></div>' +
                         shop.rail([range_card(L, b, r) for r in b["ranges"]], t(L, "ui.ranges_of", brand=b["name"])) +
                         f'<p class="fine">{t(L, "ui.range_source", source=t(L, "brand." + b["slug"] + ".source"))}</p>', "band-white band-rail")
    prods = products_of(category=c["slug"])
    if prods:
        body += band(f'<h2>{t(L, "ui.products")}</h2><div class="pc-grid">{"".join(product_card(L, p) for p in prods)}</div><p class="fine">{t(L, "ui.note_price")}</p>', "band-rise")
    if not brands and not prods:
        body += band(f'<div class="empty"><span class="tsq tsq-l">{IC[c["icon"]]}</span><p>{t(L, "cat.no_items")}</p>{cta}</div>', "band-rise")
    others = "".join(cat_tile(L, o) for o in CAT["categories"] if o is not c)
    body += band(f'<h2>{t(L, "ui.all_categories")}</h2><div class="ct-grid ct-grid-3">{others}</div>', "band-white")
    emit(L, path, t(L, f"cat.{c['slug']}.title"), t(L, f"cat.{c['slug']}.meta"), [org_ld(), crumbs_ld(L, items)], top + body,
         noindex=not c.get("indexable", True))


def p_brand_index(L):
    items = [(t(L, "ui.brands"), "brand/")]
    main = page_top(L, items, t(L, "brand.index.h1"), t(L, "brand.index.lead")) + \
        band(f'<div class="bw-row">{"".join(brand_card(L, b) for b in CAT["brands"])}</div>', "band-rise")
    emit(L, "brand/", t(L, "brand.index.title"), t(L, "brand.index.meta"), [org_ld(), crumbs_ld(L, items)], main)


def p_brand(L, b):
    path = f'brand/{b["slug"]}/'
    items = [(t(L, "ui.brands"), "brand/"), (b["name"], path)]
    evl = t(L, f"brand.{b['slug']}.evidence")
    ev = ext(b["evidence_url"], evl) if evl and "biyhomestore.com" not in b["evidence_url"] else ""
    cta = wa(L, "wa.brand", "whatsapp_brand", t(L, "ui.wa_ask_brand", brand=b["name"]), brand=b["name"])
    top = page_top(L, items, t(L, f"brand.{b['slug']}.h1"), t(L, f"brand.{b['slug']}.intro"), f'<div class="ptop-ev">{ev}</div><div class="ptop-cta">{cta}</div>')
    body = band(f'<div class="sec-h"><h2>{t(L, "ui.ranges_of", brand=b["name"])}</h2><p class="note">{t(L, "ui.stock_note")}</p></div>' +
                shop.rail([range_card(L, b, r) for r in b["ranges"]], t(L, "ui.ranges_of", brand=b["name"])) +
                f'<p class="fine">{t(L, "ui.range_source", source=t(L, "brand." + b["slug"] + ".source"))}</p>', "band-rise band-rail")
    prods = products_of(brand=b["slug"])
    if prods:
        body += band(f'<h2>{t(L, "ui.products")}</h2><div class="pc-grid">{"".join(product_card(L, p) for p in prods)}</div><p class="fine">{t(L, "ui.note_price")}</p>', "band-white")
    c = CAT["category"][b["category"]]
    body += band(f'<h2>{t(L, "ui.other_brands")}</h2><div class="bw-row">{"".join(brand_card(L, o) for o in CAT["brands"] if o is not b)}</div>'
                 f'<div class="ct-grid ct-grid-1">{cat_tile(L, c)}</div>', "band-rise")
    emit(L, path, t(L, f"brand.{b['slug']}.title"), t(L, f"brand.{b['slug']}.meta"), [org_ld(), crumbs_ld(L, items)], top + body)


def p_product(L, p):
    path = f'product/{p["slug"]}/'
    b = CAT["brand"][p["brand"]]
    c = CAT["category"][p["category"]]
    r = CAT["ranges"].get(p.get("range"), (None, None))[1]
    items = [(cat_name(L, c), f'category/{c["slug"]}/'), (p["name"], path)]
    url = absu(lp(L, path))
    key = "wa.product" if p.get("sku") else "wa.product_no_sku"
    img = [dict(i, src=u(i["src"])) for i in p.get("images") or []]
    rows = [(t(L, "ui.brand"), f'<a href="{u(lp(L, "brand/" + b["slug"] + "/"))}">{E(b["name"])}</a>'),
            (t(L, "ui.model"), E(p.get("model") or "")), (t(L, "ui.category"), f'<a href="{u(lp(L, "category/" + c["slug"] + "/"))}">{cat_name(L, c)}</a>')]
    if p.get("sku"):
        rows.insert(2, (t(L, "ui.sku"), E(p["sku"])))
    if r:
        rows.append((t(L, "ui.range"), E(dtx(L, r["name"]) if ("data." + r["name"]) in S["en"] else r["name"])))
    dl = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    desc = f'<p>{E(p["description"])}</p>' if p.get("description") else f'<p class="pending">{t(L, "ui.details_pending")}</p>'
    specs = ""
    if p.get("specs"):
        specs = f'<h2>{t(L, "ui.specs")}</h2><table class="spec">' + "".join(f'<tr><th>{E(s.get("key", ""))}</th><td>{E(str(s.get("value", "")))} {E(s.get("unit", ""))}</td></tr>' for s in p["specs"]) + "</table>"
    seen = f'<p class="fine">{t(L, "ui.seen_on", date=p.get("seen_on", ""))}</p>' if "biyhomestore.com" in (p.get("source_url") or "") else ""
    btn = wa(L, key, "whatsapp_product", t(L, "ui.wa_price"), cls="btn btn-wa btn-lg", brand=b["name"], name=pname(b, p), sku=p.get("sku") or "", variant="", url=url)
    main = f"""<section class="ptop ptop-p"><div class="wrap">{crumbs_html(L, items)}
<div class="pd">
<div class="pd-media">{shop.product_frame(IC[c['icon']], b['name'], img, alt=t(L, 'product.alt', name=p['name']), cls='pf')}</div>
<div class="pd-info"><a class="pd-brand" href="{u(lp(L, 'brand/' + b['slug'] + '/'))}">{E(b['name'])}</a>
<h1>{E(p['name'])}</h1>
<p class="pd-model">{t(L, 'ui.model')} {E(p.get('model') or '')}{(' · ' + t(L, 'ui.sku') + ' ' + E(p['sku'])) if p.get('sku') else ''}</p>
<p class="stock">{t(L, 'ui.stock.' + shop.stock_label_key(p))}</p>
<p class="pd-price">{t(L, 'ui.note_price')}</p>
{branch_picker(L)}
<div class="pd-cta">{btn}{call(L, 'call_product', t(L, 'ui.call'))}<a class="btn btn-line" href="{u(lp(L, 'stores/'))}">{IC['pin']}<span>{t(L, 'ui.stores')}</span></a></div>
</div></div></div></section>"""
    body = band(f'<div class="pd-body"><div>{desc}{specs}{seen}</div><dl class="pd-dl">{dl}</dl></div>', "band-rise")
    if r:
        body += band(f'<div class="sec-h"><h2>{E(b["name"])} {E(dtx(L, r["name"]) if ("data." + r["name"]) in S["en"] else r["name"])}</h2><p class="note">{t(L, "ui.stock_note")}</p></div>'
                     f'<div class="rg-one">{range_card(L, b, r)}</div>', "band-white")
    more = [o for o in products_of(category=c["slug"]) if o is not p]
    if more:
        body += band(f'<h2>{t(L, "ui.more_in", category=cat_name(L, c))}</h2><div class="pc-grid">{"".join(product_card(L, o) for o in more)}</div>', "band-rise")
    vi = {"item_id": p.get("sku") or p["id"], "item_name": p["name"], "item_brand": b["name"], "item_category": c["name"]}
    main += body + f'<script type="application/json" id="view-item">{json.dumps(vi, ensure_ascii=False)}</script>'
    graph = [org_ld(), crumbs_ld(L, items), shop.ld_product(p, b["name"], url, image=[absu(i["src"]) for i in p.get("images") or []] or None)]
    emit(L, path, t(L, "product.title", name=p["name"]), t(L, "product.meta", name=p["name"], model=p.get("model") or ""), graph, main,
         noindex=not shop.product_indexable(p))


def store_ld(L, br):
    tel = F["hq_landline"]["tel"] if br.get("is_hq") else TEL
    return shop.ld_store(br, F, absu(lp(L, "stores/" + br["slug"] + "/")), absu("stores/" + br["slug"] + "/#store"), absu("#org"),
                         absu("images/og.jpg"), tel)


def p_stores(L):
    items = [(t(L, "ui.stores"), "stores/")]
    main = page_top(L, items, t(L, "stores.h1"), t(L, "stores.lead")) + band(f'<div class="bc-grid">{"".join(branch_card(L, b) for b in BR)}</div>', "band-rise")
    emit(L, "stores/", t(L, "stores.title"), t(L, "stores.meta"), [org_ld(), crumbs_ld(L, items)] + [store_ld(L, b) for b in BR], main)


def p_branch(L, br):
    path = f'stores/{br["slug"]}/'
    items = [(t(L, "ui.stores"), "stores/"), (br["short"], path)]
    k = br["slug"]
    calls = call(L, "call_branch", t(L, "ui.call_num", num=TEL_D))
    if br.get("is_hq"):
        calls += call(L, "call_branch_landline", t(L, "ui.call_landline", num=F["hq_landline"]["display"]), tel=F["hq_landline"]["tel"])
    opened = f'<p class="tag">{t(L, "ui.opened_2024")}</p>' if k in ("kota-masai", "pontian") else ""
    addr = f"""<div class="addr"><span class="tsq tsq-l">{IC['pin']}</span><div><h2>{t(L, 'ui.address')}</h2><p>{E(br['address_line'])}</p><p class="bc-h">{t(L, 'ui.hours_note')}</p>{opened}</div></div>
<div class="br-cta">{wa(L, 'wa.branch', 'whatsapp_branch', t(L, 'ui.wa_ask_branch'), cls='btn btn-wa btn-lg', branch=br['short'])}{directions(L, br)}{calls}</div>"""
    others = []
    for o in BR:
        if o is br:
            continue
        d = shop.km((br["lat"], br["lng"]), (o["lat"], o["lng"]))
        dist = f'<small>{t(L, "ui.km_from", km=("%.1f" % d) if d < 10 else str(round(d)), place=br["short"])}</small>' if d is not None else f'<small>{E(o["city"])}</small>'
        others.append(f'<a class="bs" href="{u(lp(L, "stores/" + o["slug"] + "/"))}"><b>{E(o["short"])}</b>{dist}</a>')
    body = band(addr, "band-rise") + band(
        f'<div class="ask"><h2>{t(L, "branch.ask_h")}</h2><p>{t(L, "branch.ask_p")}</p></div><div class="ct-grid">{"".join(cat_tile(L, c) for c in CAT["categories"])}</div>', "band-white") + \
        band(f'<h2>{t(L, "branch.others_h")}</h2><div class="bs-strip">{"".join(others)}</div>', "band-rise")
    emit(L, path, t(L, f"branch.{k}.title"), t(L, f"branch.{k}.meta"), [org_ld(), crumbs_ld(L, items), store_ld(L, br)],
         page_top(L, items, t(L, f"branch.{k}.h1"), t(L, f"branch.{k}.intro")) + body)
    OUTFILES[lp(L, path)] = OUTFILES[lp(L, path)].replace("<body>", f'<body data-branch="{br["slug"]}">', 1)


def p_contractors(L):
    items = [(t(L, "ui.contractors"), "contractors/")]
    cta = wa(L, "wa.contractor", "whatsapp_contractors", t(L, "ui.wa_quote"), cls="btn btn-wa btn-lg")
    lst = "".join(f'<li><span class="sq-n">{i}</span><span>{t(L, f"trade.list{i}")}</span></li>' for i in (1, 2, 3))
    main = page_top(L, items, t(L, "trade.h1"), t(L, "trade.lead"), f'<div class="ptop-cta">{cta}</div>') + \
        band(f'<h2>{t(L, "trade.list_h")}</h2><ol class="track track-v">{lst}</ol>', "band-rise") + \
        band(f'<h2>{t(L, "trade.cats_h")}</h2><div class="ct-grid">{"".join(cat_tile(L, c) for c in CAT["categories"])}</div><div class="bw-row">{"".join(brand_card(L, b) for b in CAT["brands"])}</div>', "band-white") + \
        band(f'<h2>{t(L, "home.branches_h")}</h2><div class="bc-grid">{"".join(branch_card(L, b, "whatsapp_branch") for b in BR)}</div>', "band-rise")
    emit(L, "contractors/", t(L, "trade.title"), t(L, "trade.meta"), [org_ld(), crumbs_ld(L, items)], main)


def p_about(L):
    items = [(t(L, "ui.about"), "about/")]
    tl = "".join(f'<li><span class="sq-n sq-y">{y}</span><span>{t(L, "about.t" + y)}</span></li>' for y in ("2012", "2014", "2020", "2024"))
    ev = "".join(f'<li class="ev"><span class="ev-b">{E(b["name"])}</span><p>{t(L, "brand." + b["slug"] + ".intro")}</p>{ext(b["evidence_url"], t(L, "brand." + b["slug"] + ".evidence")) if t(L, "brand." + b["slug"] + ".evidence") else ""}</li>' for b in CAT["brands"])
    main = page_top(L, items, t(L, "about.h1"), t(L, "about.lead")) + \
        band(f'<ol class="track track-v">{tl}</ol>', "band-rise") + \
        band(f'<div class="mission"><span class="tsq tsq-l">{IC["home"]}</span><div><h2>{t(L, "about.mission_h")}</h2><p>{t(L, "about.mission")}</p><p class="tag">{E(F["tagline_from_own_site"])}</p></div></div>', "band-white") + \
        band(f'<h2>{t(L, "ui.brands")}</h2><ul class="ev-grid">{ev}</ul>', "band-rise")
    emit(L, "about/", t(L, "about.title"), t(L, "about.meta"), [org_ld(), crumbs_ld(L, items)], main)


def p_contact(L):
    items = [(t(L, "ui.contact"), "contact/")]
    cta = f'<div class="ptop-cta">{wa(L, "wa.general", "whatsapp_contact", t(L, "ui.wa_us") + " " + E(F["whatsapp"]["display"]), cls="btn btn-wa btn-lg")}{call(L, "call_contact", t(L, "ui.call_num", num=TEL_D))}{fb(L, "facebook_contact", cls="btn btn-line")}</div>'
    main = page_top(L, items, t(L, "contact.h1"), t(L, "contact.lead"), cta) + band(f'<div class="bc-grid">{"".join(branch_card(L, b) for b in BR)}</div>', "band-rise")
    emit(L, "contact/", t(L, "contact.title"), t(L, "contact.meta"), [org_ld(), crumbs_ld(L, items)] + [store_ld(L, b) for b in BR], main)


def p_search(L):
    items = [(t(L, "ui.search"), "search/")]
    sf = shop.search_form(u(lp(L, "search/")), t(L, "ui.search_label"), t(L, "ui.search_ph"), IC["search"] + f'<span>{t(L, "ui.search_btn")}</span>', big=True, ref="search_page")
    labels = {"results": t(L, "ui.search_results"), "brand": t(L, "ui.type.brand"), "category": t(L, "ui.type.category"),
              "range": t(L, "ui.type.range"), "product": t(L, "ui.type.product"), "store": t(L, "ui.type.store")}
    app = (f'<div id="search-app" data-lang="{L["code"]}" data-prefix="{u(lp(L, ""))}" data-index="{u("search-index.json")}?v={VER["idx"]}" data-labels="{E(json.dumps(labels, ensure_ascii=False))}">'
           f'<div id="search-results" class="sr" hidden aria-live="polite"></div>'
           f'<div id="search-none" class="empty" hidden><p>{t(L, "ui.search_none")}</p>{wa(L, "wa.general", "whatsapp_search", t(L, "ui.wa_us"))}</div></div>')
    browse = (f'<h2>{t(L, "search.browse_brands")}</h2><div class="bw-row">{"".join(brand_card(L, b) for b in CAT["brands"])}</div>'
              f'<h2>{t(L, "search.browse_cats")}</h2><div class="ct-grid">{"".join(cat_tile(L, c) for c in CAT["categories"])}</div>')
    main = page_top(L, items, t(L, "search.h1"), "", f'<div class="ptop-search">{sf}</div>') + band(app, "band-rise") + band(browse, "band-white")
    emit(L, "search/", t(L, "search.title"), t(L, "search.meta"), [org_ld(), crumbs_ld(L, items)], main, noindex=True)


def p_articles(L):
    items = [(t(L, "ui.articles"), "articles/")]
    main = page_top(L, items, t(L, "articles.h1"), t(L, "articles.lead")) + \
        band(f'<div class="ct-grid">{"".join(cat_tile(L, c) for c in CAT["categories"])}</div>', "band-rise")
    emit(L, "articles/", t(L, "articles.title"), t(L, "articles.meta"), [org_ld(), crumbs_ld(L, items)], main)


def p_privacy(L):
    items = [(privacy_page.TITLES[L["code"]], "privacy/")]
    pf = {"name": F["name"], "address": HQ["address_line"], "wa_display": F["whatsapp"]["display"],
          "wa_link": shop.wa_url(WA_E164, t(L, "wa.general")), "tel_display": TEL_D, "tel_link": "tel:" + TEL,
          "extras": ["maps", "facebook"], "updated": t(L, "privacy.updated"), "trade": "retail"}
    inner = privacy_page.render_main(L["code"], "my", pf)
    inner = inner.replace('data-cta="whatsapp_privacy" data-ref="privacy"', 'data-cta="whatsapp" data-ref="whatsapp_privacy"')
    inner = inner.replace('data-cta="call_privacy" data-ref="privacy"', 'data-cta="call" data-ref="call_privacy"')
    main = f'<section class="ptop"><div class="wrap">{crumbs_html(L, items)}<div class="prose">{inner}</div></div></section>'
    emit(L, "privacy/", t(L, "privacy.title"), t(L, "privacy.meta"), [org_ld(), crumbs_ld(L, items)], main)


# ------------------------------------------------------------------ files
def search_rows():
    rows = []
    def names(fn):
        return {L["code"]: fn(L) for L in LANGS}
    for c in CAT["categories"]:
        rows.append({"t": "category", "p": f'category/{c["slug"]}/', "n": names(lambda L: cat_name(L, c)),
                     "k": SYN["category"].get(c["slug"], []) + [t(L, f"cat.{c['slug']}.desc") for L in LANGS]})
    for b in CAT["brands"]:
        rows.append({"t": "brand", "p": f'brand/{b["slug"]}/', "n": names(lambda L: b["name"]), "k": SYN["brand"].get(b["slug"], []) + [b.get("display_alt", "")]})
        for r in b["ranges"]:
            rows.append({"t": "range", "p": f'brand/{b["slug"]}/', "n": names(lambda L: r["name"]), "b": b["name"],
                         "k": SYN["brand"].get(b["slug"], []) + SYN["category"].get(b["category"], []) + [dtx(L, r["type"]) for L in LANGS]})
    for p in CAT["products"]:
        b = CAT["brand"][p["brand"]]
        rows.append({"t": "product", "p": f'product/{p["slug"]}/', "n": names(lambda L: p["name"]), "b": b["name"],
                     "k": [p.get("model"), (p.get("model") or "").replace(" ", ""), p.get("sku"), p.get("autocount_item_code")] +
                          SYN["brand"].get(p["brand"], []) + SYN["category"].get(p["category"], [])})
    for br in BR:
        rows.append({"t": "store", "p": f'stores/{br["slug"]}/', "n": names(lambda L: br["short"]), "k": [br["city"], br["street"], "kedai hardware", "hardware shop", "五金店"]})
    return rows


def llms(index_paths):
    lines = [golive.llms_header(CFG, F["name"], "Hardware, paint and power tools shop in Johor, Malaysia, with 4 branches (Kota Tinggi HQ, Kota Tinggi JTH, Kota Masai in Pasir Gudang, Pontian). Prices on WhatsApp only.")]
    lines.append("\n## Facts\n")
    lines.append(f"- WhatsApp and call: {F['whatsapp']['display']} ({F['whatsapp']['wa_me']})")
    lines.append(f"- Kota Tinggi HQ landline: {F['hq_landline']['display']}")
    lines.append(f"- Facebook: {F['facebook']}")
    lines.append(f"- Brands: {', '.join(b['name'] for b in CAT['brands'])}")
    lines.append("- Opening hours: please WhatsApp to confirm. Prices: WhatsApp only.")
    for br in BR:
        lines.append(f"- Branch {br['short']}: {br['address_line']}")
    titles = {}
    for L in LANGS:
        lines.append(f"\n## Pages ({L['name']})\n")
        for p in index_paths:
            html = OUTFILES[lp(L, p)]
            ti = re.search(r"<title>(.*?)</title>", html).group(1)
            lines.append(f"- [{ti}]({absu(lp(L, p))})")
    return "\n".join(lines) + "\n"


def write(rel, text, binary=False):
    fp = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "wb" if binary else "w", **({} if binary else {"encoding": "utf-8"})) as f:
        f.write(text)


BANNED = [
    ("lorem", r"(?i)lorem", "raw"), ("TODO", r"\bTODO\b", "raw"), ("Page One", r"(?i)page\s*one", "raw"),
    ("pageonesingapore", r"(?i)pageonesingapore", "raw"),
    ("biyhomestore.com link", r"(?i)(href|src|content)=\"[^\"]*biyhomestore\.com", "raw"),
    ("biyhomestore.com in data", r"(?i)\"(url|item|@id|sameAs)\"\s*:\s*\"[^\"]*biyhomestore\.com", "raw"),
    ("ICI", r"\bICI\b", "text"), ("Dulux", r"(?i)dulux", "raw"), ("ICI in json", r"\"ici\"|/brand/ici", "raw"),
    ("RM price", r"\bRM\s?\d", "raw"), ("price number", r"(?i)price[^<\n]{0,20}\d+[.,]\d{2}", "text"),
    ("price field", r"(?i)\"(price|offers|priceCurrency|lowPrice|highPrice)\"\s*:", "raw"),
    ("aggregateRating", r"(?i)aggregateRating|ratingValue|reviewCount", "raw"), ("openingHours", r"(?i)openingHours", "raw"),
    ("Makita", r"(?i)makita", "raw"), ("Hiltem", r"(?i)hiltem", "raw"), ("Stanley", r"(?i)stanley", "raw"),
    ("Anchor", r"(?i)\banchor\b", "text"), ("Riland", r"(?i)riland", "raw"), ("Atlas Copco", r"(?i)atlas\s*copco", "raw"),
    ("Daihuu", r"(?i)daihuu", "raw"),
    ("Pontian postcode", r"(?i)(8200\b|82000)", "raw"), ("24,000", r"24[,.]?000", "raw"), ("20,000", r"20[,.]?000", "raw"),
    ("demo", r"(?i)demo (data|product)|\"is_demo\"\s*:\s*true", "raw"),
    ("placeholder", r"(?i)placeholder text|\{(brand|name|sku|url|branch|range|category|model|variant)\}(?![^<]*data-wa-tpl)", "text"),
    ("email", r"(?i)biyhomestorekt@gmail", "raw"), ("rating text", r"(?i)\b4\.9\b|\(790\)|1,098", "raw"),
    ("hours text", r"(?i)\b(9am|8:30am|7pm|6:30pm)\b", "raw"), ("branch phones", r"12-553 8961|12-863 8852|125538961|128638852", "raw"),
    ("delivery claim", r"(?i)\b(free delivery|we deliver|delivery available|warranty|wholesale price)", "text"),
    ("8959", r"8959", "raw"), ("Kota Masai FB", r"61557140841368", "raw"),
]


def check():
    problems = []
    files = set(OUTFILES)
    problems += [f"missing string {c}:{k}" for c, k in sorted(set(MISSING))]
    problems += I18N.check_twins({p for p in files})
    problems += I18N.check_privacy(files, OUTFILES)
    for p, html in OUTFILES.items():
        if html.count("<h1") != 1:
            problems.append(f"/{p} has {html.count('<h1')} h1")
        if 'name="robots" content="noindex' in html and ("search/" not in p) and not NOINDEX_OK(p):
            problems.append(f"/{p} unexpected noindex")
        for m in re.finditer(r'data-cta="(whatsapp|call|facebook|directions)"(?! data-ref)', html):
            problems.append(f"/{p} CTA without data-ref")
        for m in re.finditer(r'href="(https://wa\.me/[^"]+)"', html):
            if not m.group(1).startswith("https://wa.me/60125688961?text="):
                problems.append(f"/{p} wrong WhatsApp {m.group(1)[:40]}")
        for m in re.finditer(r'<a [^>]*href="(https://wa\.me/[^"]+|tel:[^"]+)"[^>]*>', html):
            if "data-ref=" not in m.group(0):
                problems.append(f"/{p} untracked CTA")
    for f, rule, snip in shop.banned_hits(OUT, BANNED):
        problems.append(f"BANNED {rule} in {f}: ...{snip}...")
    # internal link crawl
    links = 0
    for p, html in OUTFILES.items():
        for m in re.finditer(r'(?:href|src)="(' + re.escape(P) + r'/[^"#?]*)', html):
            links += 1
            rel = m.group(1)[len(P) + 1:]
            fp = os.path.join(OUT, rel, "index.html") if rel.endswith("/") or rel == "" else os.path.join(OUT, rel)
            if not os.path.exists(fp):
                problems.append(f"/{p} broken link {m.group(1)}")
    return problems, links


NOINDEX_SET = set()


def NOINDEX_OK(p):
    return p in NOINDEX_SET


def main():
    global VER, BODY_ATTR
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    # static assets
    shutil.copytree(os.path.join(HERE, "images"), os.path.join(OUT, "images"))
    shutil.copytree(os.path.join(HERE, "assets", "fonts"), os.path.join(OUT, "assets", "fonts"))
    css = open(os.path.join(TPL, "shop", "shop.css"), encoding="utf-8").read() + "\n" + open(os.path.join(HERE, "assets", "site.css"), encoding="utf-8").read()
    css = css.replace("@@FONT_ARCHIVO@@", u("assets/fonts/archivo.woff2")).replace("@@FONT_PUBLIC@@", u("assets/fonts/publicsans.woff2"))
    write("assets/site.css", css)
    shutil.copy(os.path.join(TPL, "shop", "shop.js"), os.path.join(OUT, "assets", "shop.js"))
    shutil.copy(os.path.join(HERE, "assets", "p1-cta.js"), os.path.join(OUT, "assets", "p1-cta.js"))
    rows = search_rows()
    write("search-index.json", shop.search_index(rows))
    VER = {"css": ver("assets/site.css"), "js": ver("assets/shop.js"), "cta": ver("assets/p1-cta.js"), "idx": ver("search-index.json")}
    BODY_ATTR = f' data-ga4="{E(SITE.get("ga4_id", ""))}"' if SITE.get("ga4_id") else ""
    index_paths = []
    for L in LANGS:
        p_home(L); p_cat_index(L); p_brand_index(L); p_stores(L); p_contractors(L); p_about(L); p_contact(L)
        p_search(L); p_articles(L); p_privacy(L)
        for c in CAT["categories"]:
            p_category(L, c)
        for b in CAT["brands"]:
            p_brand(L, b)
        for p in CAT["products"]:
            p_product(L, p)
        for br in BR:
            p_branch(L, br)
    # page list -> indexable paths (data flags)
    en_paths = [p for p in OUTFILES if not p.startswith(("ms/", "zh/"))]
    for p in en_paths:
        noidx = 'name="robots" content="noindex' in OUTFILES[p]
        for L in LANGS:
            if noidx:
                NOINDEX_SET.add(lp(L, p))
        if not noidx:
            index_paths.append(p)
    order = lambda p: (p.count("/"), p)
    index_paths.sort(key=order)
    for rel, html in OUTFILES.items():
        write(os.path.join(rel, "index.html") if rel else "index.html", html)
    write("sitemap.xml", golive.sitemap_xml(CFG, index_paths, TODAY))
    write("robots.txt", golive.robots_txt(CFG))
    write("llms.txt", llms(index_paths))
    write("site.webmanifest", json.dumps({"name": "BIY Home Store", "short_name": "BIY", "start_url": u(""), "display": "standalone",
                                          "background_color": "#FAF6F1", "theme_color": "#2B2B2B",
                                          "icons": [{"src": u("images/icon-192.png"), "sizes": "192x192", "type": "image/png"},
                                                    {"src": u("images/favicon-512.png"), "sizes": "512x512", "type": "image/png"}]}, indent=1))
    problems, links = check()
    n = sum(len(fs) for _, _, fs in os.walk(OUT))
    print(f"built {len(OUTFILES)} pages, {n} files into {OUT}; {len(index_paths)} indexable EN paths ({len(index_paths) * len(LANGS)} sitemap URLs); internal links checked: {links}")
    if problems:
        print("GATE FAILED:")
        for p in problems[:80]:
            print("  -", p)
        sys.exit(1)
    print("GATES PASS: strings, twins, privacy, one H1, tracked CTAs, WhatsApp number, banned grep, link crawl")


if __name__ == "__main__":
    main()
