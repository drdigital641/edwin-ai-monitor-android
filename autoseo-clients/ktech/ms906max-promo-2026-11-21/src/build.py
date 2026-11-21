"""Build the ktech.my Autel MS906 MAX year-end promotion from promo.json (ONE config) + strings.py (ONE strings file).
Outputs (OUTDIR):
  autel-ms906-max-promo/index.html, ms/..., zh/...   landing pages: live + ended versions in ONE file, Apache SSI
                                                    picks one per request from the server clock (DATE_GMT, UTC)
  assets/promo.css, assets/promo.js                  shared look + client-side ended supplement (cache-busted)
  parts/home-hero-<lang>.html                         homepage hero block (SSI if/else around the old hero)
  parts/tools-hl-<lang>.html, parts/pro-x-<lang>.html tools-index highlight and MS906 Pro cross-link (SSI-wrapped)
  parts/htaccess-block.txt                            SSI switch-on + /go/ms906max-buy/ redirect (server clock)
  parts/sitemap-rows.xml                              the 3 landing URLs with xhtml:link alternates
Header, footer and dock copy the live ktech.my shared parts (read through the Bridge 21 Nov 2026).
Usage: python3 -I build.py OUTDIR
"""
import hashlib, json, os, sys
from datetime import datetime, timedelta, timezone
from html import escape as e

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import autoseo_i18n as I18N
from strings import S, UI, FEATS

for L, code, loc in zip(I18N.LANGS, ['en-MY', 'ms-MY', 'zh-MY'], ['en_MY', 'ms_MY', 'zh_MY']):
    L['hreflang'] = code
    L['og_locale'] = loc

C = json.load(open(os.path.join(HERE, 'promo.json'), encoding='utf-8'))
SITE, SLUG = C['site'], C['slug']
absu = lambda p: SITE + p
u = lambda p: '/' + p
KV = '20261114t'
END_UTC = C['ended_from_utc']                       # SSI: live while DATE_GMT < this (UTC)
_end = datetime.strptime(END_UTC, '%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
assert _end == datetime.fromisoformat(C['end_local']).astimezone(timezone.utc) + timedelta(seconds=1), 'end_local and ended_from_utc disagree'
END_SRV = (_end + timedelta(hours=C['server_utc_offset_hours'])).strftime('%Y%m%d%H%M%S')  # mod_rewrite %{TIME} is server local
SSI_IF = f'<!--#config timefmt="%Y%m%d%H%M%S" --><!--#if expr="$DATE_GMT < {END_UTC}" -->'
SSI_ELSE, SSI_END = '<!--#else -->', '<!--#endif -->'
IMG = C['img_dir']
P = C['poster']          # 1080x1080: promo pages + Product schema image
B = C['banner']          # 1600x900: homepage promo band
CO = C['checkout_slug']
MAP = 'https://www.google.com/maps/search/?api=1&query=No.%2028%2C%20Jalan%20Ekoperniagaan%203/11%2C%20Taman%20Ekoperniagaan%2C%2081100%20Johor%20Bahru%2C%20Johor%2C%20Malaysia'
ADDR = 'No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor, Malaysia'
CSS = open(os.path.join(HERE, 'promo.css'), encoding='utf-8').read()
CSS_V = hashlib.sha256(CSS.encode()).hexdigest()[:8]
JS = ('/* ktech.my MS906 MAX promo: client-side SUPPLEMENT only. The server (Apache SSI + .htaccess) already swaps to the\n'
      '   ended state; this only covers a page cached before the end time. Built from promo.json. */\n'
      "(function(){var E=Date.parse('" + C['end_local'] + "');function run(){if(Date.now()<=E)return;"
      "var a=document.querySelectorAll('[data-promo-live]'),b=document.querySelectorAll('[data-promo-ended]'),i;"
      "for(i=0;i<a.length;i++)a[i].hidden=true;for(i=0;i<b.length;i++)b[i].hidden=false}"
      "if(document.readyState!=='loading')run();else document.addEventListener('DOMContentLoaded',run);setInterval(run,60000)})();\n")
JS_V = hashlib.sha256(JS.encode()).hexdigest()[:8]


def f(s, c):
    return s.format(price=C['price_display'], end=C['end_display'][c], end_full=C['end_full'][c], how_buy='{how_buy}')


def T(c, k):
    return f(S[c][k], c)


# Round 3 (Edwin 22 Nov 2026): no salesman WhatsApp anywhere on the promo. Buy now opens the checkout page
# (same tab); the ended state points to the tools page and the contact page instead.
def buy_href(L):
    return u(I18N.page_path(L, CO))


def buy_btn(L):
    c = L['code']
    return (f'<a class="btn btn-wa pm-buy" href="{buy_href(L)}" rel="nofollow" data-cta="booking" '
            f'data-ref="{C["ref_buy"]}"><span>{e(T(c, "buy"))}</span></a>')


def ended_links(L, cls='btn btn-wa'):
    c = L['code']
    return (f'<div class="pm-ctas"><a class="{cls}" href="{u(I18N.page_path(L, "autel-diagnostic-tools/"))}" data-ref="promo-ms906max-ended"><span>{e(T(c, "ended_tools"))}</span></a>'
            f'<a class="btn btn-ghost" href="{u(I18N.page_path(L, "contact/"))}" data-ref="promo-ms906max-ended-contact"><span>{e(T(c, "ended_contact"))}</span></a></div>')


def poster(c, eager, img=None, alt_key='alt', cls='pm-poster'):
    img = img or P
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    st = img['stem']
    return (f'<figure class="{cls}"><picture><source type="image/webp" srcset="/{IMG}{st}.webp">'
            f'<img src="/{IMG}{st}.jpg" alt="{e(T(c, alt_key))}" width="{img["w"]}" height="{img["h"]}" {load} decoding="async" draggable="false">'
            f'</picture></figure>')


def info(L, landing):
    c = L['code']
    more = '' if landing else f'<p class="pm-more"><a href="{u(I18N.page_path(L, SLUG))}">{e(T(c, "more"))}</a></p>'
    return (f'<div class="pm-i"><p class="pm-price"><b>{e(C["price_display"])}</b><span>{e(T(c, "unit"))}</span></p>'
            f'<ul class="pm-meta"><li class="pm-end">{e(T(c, "ends"))}</li><li>{e(T(c, "postage"))}</li></ul>'
            f'<div class="pm-ctas pm-one">{buy_btn(L)}</div>'
            + (f'<p class="pm-excl">{e(T(c, "excl"))}</p>' if landing else '') + f'{more}</div>')


def ended_box(L):
    c = L['code']
    return f'<div class="pm-ended" data-promo-ended hidden><p>{e(T(c, "ended"))}</p>{ended_links(L)}</div>'


def home_hero(L):
    # 22 Nov 2026 (Edwin): the promo is no longer the hero. It is the first section right AFTER the original scanner
    # hero, so it carries an H2 (the page keeps its one H1 in the hero) and the poster loads lazily.
    c = L['code']
    return (SSI_IF + f'<section class="sec pm-band" id="ms906max-promo"><div class="wrap"><div class="pm-grid" data-promo-live>'
            f'<div class="pm-h"><h2>{e(T(c, "home_h1"))}</h2><p class="line">{e(T(c, "home_line"))}</p></div>'
            f'{poster(c, False, B, "alt_banner", "pm-poster pm-banner")}{info(L, False)}</div>{ended_box(L)}</div></section>' + SSI_END)


def head(L, title, desc, ld, og_alt, extra='', slug=SLUG, robots='index,follow,max-image-preview:large'):
    p = I18N.page_path(L, slug)
    url, og = absu(p), absu(IMG + C['og'])
    ui = UI[L['code']]
    return f'''<!doctype html><html lang="{L['hreflang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">{I18N.hreflang_links(absu, slug).replace(chr(10), '')}
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}"><meta property="og:image:secure_url" content="{og}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(og_alt)}"><meta name="twitter:image" content="{og}">{I18N.og_locale_tags(L).replace(chr(10), '')}<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f3f4f0"><link rel="icon" type="image/png" href="/assets/favicon.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{ui['fonts']}&display=swap">
<link rel="stylesheet" href="/assets/k.css?v={KV}"><link rel="stylesheet" href="/assets/promo.css?v={CSS_V}">{extra}{ld}</head>'''


def header(L, slug=SLUG):
    c, ui = L['code'], UI[L['code']]
    hp = I18N.page_path(L, '')
    sw = I18N.switcher(u, slug, L, 'Language', cls='lang').replace('<span class="sl" aria-hidden="true">/</span>', '')
    sw = sw.replace('<nav class="lang"', '<div class="lang"').replace('</nav>', '</div>')
    navp = ['autel-diagnostic-tools/', 'services/', 'about/', 'contact/']
    tnav = ''.join(f'<a href="{u(I18N.page_path(L, q))}">{e(n)}</a>' for q, n in zip(navp, ui['nav']))
    return f'''<body class="pm-page"><header class="top"><div class="wrap"><a class="brand" href="{u(hp)}" aria-label="K Tech Auto Solution"><img src="/assets/ktech-logo.webp?v={KV}" alt="K Tech Auto Solution logo" width="110" height="56" decoding="async"></a>
<nav class="tnav" aria-label="Main">{tnav}</nav>{sw}
<button class="menu-btn" aria-expanded="false" aria-controls="mnav" aria-label="{e(ui['menu'])}"><i></i><i></i><i></i></button></div><nav id="mnav" aria-label="Mobile"><a href="{u(hp)}">{e(S[c]['home'])}</a>{tnav}</nav></header>'''


def footer(L, extra_js=''):
    c, ui = L['code'], UI[L['code']]
    hp = I18N.page_path(L, '')
    navp = ['autel-diagnostic-tools/', 'services/', 'about/', 'contact/']
    tnav = ''.join(f'<a href="{u(I18N.page_path(L, q))}">{e(n)}</a>' for q, n in zip(navp, ui['nav']))
    fnav = (f'<a href="{u(hp)}">{e(S[c]["home"])}</a>' + tnav
            + ''.join(f'<a href="{u(I18N.page_path(L, q))}">{e(n)}</a>' for q, n in zip(['articles/', 'privacy/'], ui['foot_extra'])))
    return f'''<footer class="foot"><div class="wrap"><div class="fg">
<div><img src="/assets/ktech-logo-white.webp?v={KV}" alt="K Tech Auto Solution" width="110" height="56" loading="lazy" decoding="async"><p>K Tech Auto Solution Sdn. Bhd.<br>{e(ui['co'])} 201801038870 (1300901-K)<br><a href="{e(MAP)}" target="_blank" rel="noopener">{ADDR}</a></p>
<p><a href="tel:+60125462820" data-ref="footer-call">{e(ui['call'])} Autel Hooi +60 12-546 2820</a><br><a href="tel:+60109362820" data-ref="footer-call3">{e(ui['call'])} Tony +60 10-936 2820</a><br><a href="tel:+60125512820" data-ref="footer-call2">{e(ui['call'])} Gavin +60 12-551 2820</a><br>{e(ui['email'])}: <a href="mailto:sales@k-techmy.com">sales@k-techmy.com</a><br><a href="https://www.facebook.com/ktechautosolutionsb/" target="_blank" rel="noopener">Facebook: K Tech Auto Solution Sdn. Bhd. →</a><br><a href="https://www.facebook.com/KTechHooi/" target="_blank" rel="noopener">Facebook: K Tech-Autel-Hooi →</a></p></div>
<nav aria-label="Footer">{fnav}</nav>
<div><p>{e(ui['seo_p'])}</p><a class="seo-l" href="https://autoseo.my/">AutoSEO.my — SEO websites for automotive workshops</a></div></div>
<p class="tm">{e(ui['tm_autel'])}</p><p class="tm" style="border:0;margin:0;padding:0">© 2026 K Tech Auto Solution Sdn. Bhd.</p></div></footer>
<script src="/assets/k.js?v={KV}" defer></script><script src="/assets/promo.js?v={JS_V}" defer></script>{extra_js}<script src="/p1-cta.js?v=020caac6" defer></script>
</body></html>'''


def faq_html(items):
    return '<div class="faq">' + ''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in items) + '</div>'


def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}


def landing(L, ended):
    c = L['code']
    s = S[c]
    p = I18N.page_path(L, SLUG)
    url = absu(p)
    hp = I18N.page_path(L, '')
    tools = I18N.page_path(L, 'autel-diagnostic-tools/')
    pro = I18N.page_path(L, 'autel-diagnostic-tools/maxisys-ms906pro/')
    how = T(c, 'how_buy')
    faqs = [(f(q, c), f(a, c).replace('{how_buy}', how)) for q, a in (s['faq_end'] if ended else s['faq'])]
    feats = ''.join(f'<section><h3>{e(g)}</h3><ul>' + ''.join(f'<li>{e(f(x, c))}</li>' for x in items) + '</ul></section>'
                    for g, items in FEATS[c])
    prod = {"@context": "https://schema.org", "@type": "Product", "@id": url + "#product", "name": C['product'],
            "brand": {"@type": "Brand", "name": "Autel"}, "category": "Car diagnostic tool",
            "image": [absu(IMG + P['stem'] + '.jpg'), absu(IMG + C['og'])], "url": url,
            "description": T(c, 'desc_end' if ended else 'desc')}
    if not ended:
        prod["offers"] = {"@type": "Offer", "url": url, "price": str(C['price']), "priceCurrency": C['currency'],
                          "priceValidUntil": C['end_date'], "availability": C['availability'],
                          "seller": {"@id": "https://ktech.my/#org"},
                          "shippingDetails": {"@type": "OfferShippingDetails",
                                              "shippingRate": {"@type": "MonetaryAmount", "value": "0", "currency": C['currency']},
                                              "shippingDestination": {"@type": "DefinedRegion", "addressCountry": "MY"}}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": s['home'], "item": absu(hp)},
        {"@type": "ListItem", "position": 2, "name": s['tools'], "item": absu(tools)},
        {"@type": "ListItem", "position": 3, "name": s['crumb'], "item": url}]}
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (prod, bc, faq_ld(faqs)))
    pre = '' if ended else f'<link rel="preload" as="image" type="image/webp" href="/{IMG}{P["stem"]}.webp">'
    h = head(L, T(c, 'title_end' if ended else 'title'), T(c, 'desc_end' if ended else 'desc'), ld, T(c, 'og_alt'), pre)
    crumb = (f'<div class="crumb"><a href="{u(hp)}">{e(s["home"])}</a> / <a href="{u(tools)}">{e(s["tools"])}</a> / {e(s["crumb"])}</div>')
    if ended:
        top = (f'<section class="pm-ph"><div class="wrap">{crumb}<h1>{e(T(c, "h1_end"))}</h1><p class="line">{e(T(c, "lead_end"))}</p>'
               f'<div class="pm-ended" style="margin-top:16px"><p>{e(T(c, "ended"))}</p>{ended_links(L)}</div></div></section>')
        terms = ''
        endsec = (f'<section class="sec dark end"><div class="wrap"><h2>{e(T(c, "end_h_end"))}</h2><p>{e(T(c, "end_p_end"))}</p>'
                  f'{ended_links(L)}</div></section>')
    else:
        top = (f'<section class="pm-ph"><div class="wrap"><div class="pm-grid" data-promo-live><div class="pm-h">{crumb}'
               f'<h1>{e(T(c, "h1"))}</h1><p class="line">{e(T(c, "lead"))}</p></div>{poster(c, True)}{info(L, True)}</div>'
               f'{ended_box(L)}</div></section>')
        terms = (f'<section class="sec alt" id="terms"><div class="wrap"><h2 class="pm-h2">{e(T(c, "tc_h"))}</h2>'
                 f'<ol class="pm-tc">' + ''.join(f'<li>{e(f(x, c))}</li>' for x in s['tc']) + '</ol>'
                 f'<p class="pm-auth">{e(T(c, "auth"))}</p></div></section>')
        endsec = (f'<section class="sec dark end"><div class="wrap" data-promo-live><h2>{e(T(c, "end_h"))}</h2><p>{e(T(c, "end_p"))}</p>'
                  f'<div class="pm-ctas pm-one" style="max-width:460px">{buy_btn(L)}</div></div>'
                  f'<div class="wrap" data-promo-ended hidden><h2>{e(T(c, "end_h_end"))}</h2><p>{e(T(c, "end_p_end"))}</p>{ended_links(L)}</div></section>')
    feat = (f'<section class="sec"><div class="wrap"><h2 class="pm-h2">{e(T(c, "feat_h"))}</h2><p class="pm-sub">{e(T(c, "feat_p"))}</p>'
            f'<div class="pm-feats">{feats}</div>'
            f'<div class="newbox pm-pro"><h2>{e(T(c, "pro_h"))}</h2><p>{e(T(c, "pro_p"))}</p><p><a href="{u(pro)}">{e(T(c, "pro_link"))}</a></p></div></div></section>')
    faq = f'<section class="sec"><div class="wrap"><h2 class="pm-h2">{e(T(c, "faq_h"))}</h2>{faq_html(faqs)}</div></section>'
    main = f'<main>{top}{feat}{terms}{faq}{endsec}</main>'
    return h + header(L) + main + footer(L)


def tools_hl(L):
    c = L['code']
    return (SSI_IF + f'<div class="newbox pm-hl" data-promo-live><span class="mono">{e(T(c, "hl_label"))}</span><h2>{e(T(c, "hl_h"))}</h2>'
            f'<p>{e(T(c, "hl_p"))}</p><a class="btn btn-wa" href="{u(I18N.page_path(L, SLUG))}" data-ref="tools-ms906max-promo"><span>{e(T(c, "hl_btn"))}</span></a></div>'
            + SSI_END)


def pro_x(L):
    c = L['code']
    return (SSI_IF + f'<p class="pm-x" data-promo-live>{e(T(c, "pro_x"))} <a href="{u(I18N.page_path(L, SLUG))}">{e(T(c, "pro_x_link"))}</a></p>' + SSI_END)


# ---- Checkout payment page (round 3, Edwin 22 Nov 2026) -------------------------------------------------------------
# /autel-ms906-max-promo/checkout/ per language, noindex. Live: the form. Ended (server clock, SSI): closed message.
# The form posts to the K Tech Promo Orders backend (Base44 fn ktechOrder): it validates again, stores the order
# FIRST, then answers with a Stripe URL once K Tech's own Stripe value is set as a Base44 secret, else with only the
# order reference ("Payment link opening soon"). No key, link or order data is ever in this page or any public file.
CO_JS_SRC = open(os.path.join(HERE, 'checkout.js'), encoding='utf-8').read()
CO_JS_V = hashlib.sha256(CO_JS_SRC.encode()).hexdigest()[:8]


def field(name, label, typ='text', auto='', req=True, extra='', hint='', mode=''):
    rq = ' required' if req else ''
    hid = f' aria-describedby="h-{name}"' if hint else ''
    h = f'<small id="h-{name}">{e(hint)}</small>' if hint else ''
    im = f' inputmode="{mode}"' if mode else ''
    ac = f' autocomplete="{auto}"' if auto else ''
    return (f'<div class="pm-f" data-f="{name}"><label for="f-{name}">{e(label)}</label>{h}'
            f'<input id="f-{name}" name="{name}" type="{typ}"{ac}{im}{rq}{hid}{extra}><em class="pm-fe" id="e-{name}" hidden></em></div>')


def checkout_page(L, ended):
    c = L['code']
    s, k = S[c], S[c]['co']
    hp = I18N.page_path(L, '')
    promo = I18N.page_path(L, SLUG)
    crumb = (f'<div class="crumb"><a href="{u(hp)}">{e(s["home"])}</a> / <a href="{u(promo)}">{e(s["crumb"])}</a> / {e(k["crumb"])}</div>')
    h = head(L, k['title'], T(c, 'desc'), '', T(c, 'og_alt'), slug=CO, robots='noindex,follow')
    if ended:
        main = (f'<main><section class="pm-ph"><div class="wrap">{crumb}<h1>{e(k["h1_end"])}</h1>'
                f'<div class="pm-ended" style="margin-top:16px"><p>{e(T(c, "ended"))}</p>{ended_links(L)}</div></div></section></main>')
        return h + header(L, CO) + main + footer(L)
    msgs = {kk: f(v, c) for kk, v in k['js'].items()}
    cfg = {'api': C['checkout_api'], 'lang': c, 'price': C['price'], 'max': C['max_qty'], 'msg': msgs}
    states = ''.join(f'<option value="{e(x)}">{e(k["states"].get(x, x))}</option>' for x in C['states'])
    summ = ''.join(f'<li>{e(f(x, c))}</li>' for x in k['sum_list'])
    priv = u(I18N.page_path(L, 'privacy/'))
    form = (f'<form id="pmco" class="pm-form" novalidate data-cfg="{e(json.dumps(cfg, ensure_ascii=False))}">'
            f'<section class="pm-sum" aria-labelledby="sum-h"><h2 id="sum-h">{e(k["sum_h"])}</h2>'
            f'<p class="pm-sum-p"><b>{e(C["product"])}</b><span>{e(C["price_display"])} {e(T(c, "unit"))}</span></p>'
            f'<div class="pm-qty"><label for="f-qty">{e(k["qty"])}</label><div class="pm-step">'
            f'<button type="button" class="pm-qb" data-d="-1" aria-label="{e(k["qty_less"])}">&minus;</button>'
            f'<input id="f-qty" name="qty" type="number" inputmode="numeric" min="1" max="{C["max_qty"]}" step="1" value="1" required>'
            f'<button type="button" class="pm-qb" data-d="1" aria-label="{e(k["qty_more"])}">+</button></div><em class="pm-fe" id="e-qty" hidden></em></div>'
            f'<p class="pm-total"><span>{e(k["total"])}</span><b id="pm-total" aria-live="polite">{e(C["price_display"])}</b></p>'
            f'<ul class="pm-sum-l">{summ}</ul></section>'
            f'<fieldset><legend>{e(k["you_h"])}</legend>'
            + field('name', k['name'], auto='name', extra=' maxlength="80"')
            + field('phone', k['phone'], 'tel', 'tel', hint=k['phone_hint'], mode='tel', extra=' maxlength="20"')
            + field('email', k['email'], 'email', 'email', mode='email', extra=' maxlength="120"')
            + f'</fieldset><fieldset><legend>{e(k["addr_h"])}</legend>'
            + field('address_line1', k['a1'], auto='address-line1', extra=' maxlength="120"')
            + field('address_line2', k['a2'], auto='address-line2', req=False, extra=' maxlength="120"')
            + '<div class="pm-row2">'
            + field('postcode', k['postcode'], auto='postal-code', mode='numeric', extra=' maxlength="5" pattern="[0-9]{5}"')
            + field('city', k['city'], auto='address-level2', extra=' maxlength="60"')
            + '</div>'
            + f'<div class="pm-f" data-f="state"><label for="f-state">{e(k["state"])}</label><select id="f-state" name="state" autocomplete="address-level1" required>'
              f'<option value="">{e(k["state_pick"])}</option>{states}</select><em class="pm-fe" id="e-state" hidden></em></div>'
            + f'<p class="pm-ship">{e(k["ship_my"])}</p></fieldset>'
            + f'<div class="pm-hp" aria-hidden="true"><label for="f-cw">Company website</label><input id="f-cw" name="company_website" type="text" tabindex="-1" autocomplete="off"></div>'
            + f'<div class="pm-f pm-consent" data-f="consent"><label class="pm-cb"><input id="f-consent" name="consent" type="checkbox" required>'
              f'<span>{e(k["consent"])} <a href="{priv}" target="_blank" rel="noopener">{e(k["privacy"])}</a></span></label><em class="pm-fe" id="e-consent" hidden></em></div>'
            + f'<p class="pm-err" id="pm-err" role="alert" hidden></p>'
            + f'<button type="submit" class="btn btn-wa pm-go" data-ref="{C["ref_checkout"]}"><span>{e(k["go"])}</span></button>'
            + f'<p class="pm-note">{e(k["note"])}</p></form>')
    done = ('<div id="pmco-done" class="pm-done" tabindex="-1" hidden><h2 id="pmco-dh"></h2><p id="pmco-dp"></p>'
            f'<p class="pm-ref">{e(k["ref"])} <b id="pmco-ref"></b></p><p><a href="{u(promo)}">{e(k["back"])}</a></p></div>')
    main = (f'<main><section class="pm-ph pm-co-top"><div class="wrap">{crumb}<h1>{e(k["h1"])}</h1>'
            f'<p class="line">{e(T(c, "end_p"))}</p></div></section>'
            f'<section class="sec pm-co-sec"><div class="wrap pm-co">{form}{done}'
            f'<noscript><p class="pm-err">{e(k["noscript"])}</p></noscript></div></section></main>')
    js = f'<script src="/assets/promo-checkout.js?v={CO_JS_V}" defer></script>'
    return h + header(L, CO) + main + footer(L, js)


def htaccess_block():
    out = ['# K Tech Autel MS906 MAX promo (21 Nov 2026), generated from promo.json by ms906max-promo build.py.',
           '# SSI picks the live/ended block on the home, promo, tools-index and MS906 Pro pages (DATE_GMT = UTC).',
           'Options +IncludesNOEXEC', 'SSILegacyExprParser on',
           '<If "%{REQUEST_URI} =~ m#^/((ms|zh)/)?(autel-ms906-max-promo/|autel-ms906-max-promo/checkout/|autel-diagnostic-tools/|autel-diagnostic-tools/maxisys-ms906pro/)?(index\\.html)?$#">',
           '  SetOutputFilter INCLUDES', '</If>']
    rw = [f'# Old Buy now links: /go/ms906max-buy/ -> the checkout page while live, the promo page after (no WhatsApp, Edwin 22 Nov). Server clock (%{{TIME}}) is UTC{C["server_utc_offset_hours"]:+d}; promo ends {C["end_local"]}.']
    for L in I18N.LANGS:
        c, pre = L['code'], L['prefix']
        target = absu(I18N.page_path(L, CO))
        rx = '^' + pre.replace('/', '/') + 'go/ms906max-buy/?$'
        rw += [f'RewriteCond %{{TIME}} <{END_SRV}', f'RewriteRule {rx} {target} [R=302,L]',
               f'RewriteRule {rx} {absu(I18N.page_path(L, SLUG))} [R=302,L]']
    return '\n'.join(out) + '\n', '\n'.join(rw) + '\n'


def main(out):
    files = {}
    for L in I18N.LANGS:
        files[I18N.page_path(L, SLUG) + 'index.html'] = SSI_IF + landing(L, False) + SSI_ELSE + landing(L, True) + SSI_END
        files[I18N.page_path(L, CO) + 'index.html'] = SSI_IF + checkout_page(L, False) + SSI_ELSE + checkout_page(L, True) + SSI_END
        files[f'parts/home-hero-{L["code"]}.html'] = home_hero(L)
        files[f'parts/tools-hl-{L["code"]}.html'] = tools_hl(L)
        files[f'parts/pro-x-{L["code"]}.html'] = pro_x(L)
    assert not I18N.check_twins({p for p in files if p.endswith('promo/index.html')})
    a, b = htaccess_block()
    files['parts/htaccess-block.txt'] = a + '----- rewrite rules (after the https redirects) -----\n' + b
    sm = I18N.sitemap_xml(absu, [SLUG], '2026-11-22')
    files['parts/sitemap-rows.xml'] = '\n'.join(x for x in sm.splitlines() if x.startswith('<url>')) + '\n'
    files['assets/promo.css'] = CSS
    files['assets/promo.js'] = JS
    files['assets/promo-checkout.js'] = CO_JS_SRC
    files['parts/versions.json'] = json.dumps({'css': CSS_V, 'js': JS_V, 'end_utc': END_UTC, 'end_server': END_SRV, 'checkout_js': CO_JS_V})
    for p, txt in files.items():
        fp = os.path.join(out, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, 'w', encoding='utf-8').write(txt)
    bad = [w for w in ['lowest', 'cheapest', 'below market', 'US$', 'stock subject', 'SST', 'PAYMENT_URL_TBC', 'extremely rare', '<s>', '<del>', 'line-through'] if any(w.lower() in t.lower() for t in files.values() if not t.startswith('#'))]
    assert not bad, bad
    # Round 3 gates: no salesman WhatsApp, no rival poster, no secret-looking value anywhere in the output.
    for w in ['wa.me', 'whatsapp.com', 'autel-ms906-max-promo-poster', 'og-autel-ms906-max-promo', 'sk_live', 'sk_test', 'rk_live', 'whsec_', 'buy.stripe.com']:
        hit = [p for p, t in files.items() if w in t]
        assert not hit, (w, hit)
    print('built', len(files), 'files; css', CSS_V, 'js', JS_V, 'end_server', END_SRV)


if __name__ == '__main__':
    main(sys.argv[1])
