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
from urllib.parse import quote

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
PAY_REAL = C['payment_url'].startswith('https://')
END_UTC = C['ended_from_utc']                       # SSI: live while DATE_GMT < this (UTC)
_end = datetime.strptime(END_UTC, '%Y%m%d%H%M%S').replace(tzinfo=timezone.utc)
assert _end == datetime.fromisoformat(C['end_local']).astimezone(timezone.utc) + timedelta(seconds=1), 'end_local and ended_from_utc disagree'
END_SRV = (_end + timedelta(hours=C['server_utc_offset_hours'])).strftime('%Y%m%d%H%M%S')  # mod_rewrite %{TIME} is server local
SSI_IF = f'<!--#config timefmt="%Y%m%d%H%M%S" --><!--#if expr="$DATE_GMT < {END_UTC}" -->'
SSI_ELSE, SSI_END = '<!--#else -->', '<!--#endif -->'
IMG = C['img_dir']
P = C['poster']
WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.2c0-.1-.2-.2-.5-.3z"/></svg>')
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
    return s.format(price=C['price_display'], end=C['end_display'][c], end_full=C['end_full'][c],
                    wa_display=C['wa_display'], wa_name=C['wa_name'], how_buy='{how_buy}')


def T(c, k):
    return f(S[c][k], c)


def wa(text):
    return f'https://wa.me/{C["wa"]}?text=' + quote(text, safe='')


def wa_btn(text, label, ref, cls='btn btn-wa'):
    return (f'<a class="{cls}" href="{e(wa(text))}" target="_blank" rel="noopener" data-ref="{ref}">'
            f'{WA_SVG}<span>{e(label)}</span></a>')


def buy_href(L):
    return u(I18N.page_path(L, 'go/ms906max-buy/'))


def buy_btn(L):
    c = L['code']
    typ = 'booking' if PAY_REAL else 'whatsapp'
    return (f'<a class="btn btn-wa" href="{buy_href(L)}" rel="nofollow noopener" target="_blank" data-cta="{typ}" '
            f'data-ref="{C["ref_buy"]}"><span>{e(T(c, "buy"))}</span></a>')


def poster(c, eager):
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    st = P['stem']
    return (f'<figure class="pm-poster"><picture><source type="image/webp" srcset="/{IMG}{st}.webp">'
            f'<img src="/{IMG}{st}.jpg" alt="{e(T(c, "alt"))}" width="{P["w"]}" height="{P["h"]}" {load} decoding="async" draggable="false">'
            f'</picture></figure>')


def info(L, landing):
    c = L['code']
    more = '' if landing else f'<p class="pm-more"><a href="{u(I18N.page_path(L, SLUG))}">{e(T(c, "more"))}</a></p>'
    return (f'<div class="pm-i"><p class="pm-price"><b>{e(C["price_display"])}</b><span>{e(T(c, "unit"))}</span></p>'
            f'<ul class="pm-meta"><li class="pm-end">{e(T(c, "ends"))}</li><li>{e(T(c, "postage"))}</li></ul>'
            f'<div class="pm-ctas">{buy_btn(L)}{wa_btn(T(c, "wa_buy"), T(c, "wa"), C["ref_wa"], "btn btn-ghost")}</div>'
            + (f'<p class="pm-excl">{e(T(c, "excl"))}</p>' if landing else '') + f'{more}</div>')


def ended_box(c):
    return (f'<div class="pm-ended" data-promo-ended hidden><p>{e(T(c, "ended"))}</p>'
            f'{wa_btn(T(c, "wa_ended"), T(c, "wa"), "promo-ms906max-ended")}</div>')


def home_hero(L):
    # 22 Nov 2026 (Edwin): the promo is no longer the hero. It is the first section right AFTER the original scanner
    # hero, so it carries an H2 (the page keeps its one H1 in the hero) and the poster loads lazily.
    c = L['code']
    return (SSI_IF + f'<section class="sec pm-band" id="ms906max-promo"><div class="wrap"><div class="pm-grid" data-promo-live>'
            f'<div class="pm-h"><h2>{e(T(c, "home_h1"))}</h2><p class="line">{e(T(c, "home_line"))}</p></div>'
            f'{poster(c, False)}{info(L, False)}</div>{ended_box(c)}</div></section>' + SSI_END)


def head(L, title, desc, ld, og_alt, extra=''):
    p = I18N.page_path(L, SLUG)
    url, og = absu(p), absu(IMG + C['og'])
    ui = UI[L['code']]
    return f'''<!doctype html><html lang="{L['hreflang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">{I18N.hreflang_links(absu, SLUG).replace(chr(10), '')}
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}"><meta property="og:image:secure_url" content="{og}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(og_alt)}"><meta name="twitter:image" content="{og}">{I18N.og_locale_tags(L).replace(chr(10), '')}<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f3f4f0"><link rel="icon" type="image/png" href="/assets/favicon.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{ui['fonts']}&display=swap">
<link rel="stylesheet" href="/assets/k.css?v={KV}"><link rel="stylesheet" href="/assets/promo.css?v={CSS_V}">{extra}{ld}</head>'''


def header(L):
    c, ui = L['code'], UI[L['code']]
    hp = I18N.page_path(L, '')
    sw = I18N.switcher(u, SLUG, L, 'Language', cls='lang').replace('<span class="sl" aria-hidden="true">/</span>', '')
    sw = sw.replace('<nav class="lang"', '<div class="lang"').replace('</nav>', '</div>')
    navp = ['autel-diagnostic-tools/', 'services/', 'about/', 'contact/']
    tnav = ''.join(f'<a href="{u(I18N.page_path(L, q))}">{e(n)}</a>' for q, n in zip(navp, ui['nav']))
    return f'''<body class="pm-page"><header class="top"><div class="wrap"><a class="brand" href="{u(hp)}" aria-label="K Tech Auto Solution"><img src="/assets/ktech-logo.webp?v={KV}" alt="K Tech Auto Solution logo" width="110" height="56" decoding="async"></a>
<nav class="tnav" aria-label="Main">{tnav}</nav>{sw}
<button class="menu-btn" aria-expanded="false" aria-controls="mnav" aria-label="{e(ui['menu'])}"><i></i><i></i><i></i></button></div><nav id="mnav" aria-label="Mobile"><a href="{u(hp)}">{e(S[c]['home'])}</a>{tnav}</nav></header>'''


def footer(L, dock_text):
    c, ui = L['code'], UI[L['code']]
    hp = I18N.page_path(L, '')
    navp = ['autel-diagnostic-tools/', 'services/', 'about/', 'contact/']
    tnav = ''.join(f'<a href="{u(I18N.page_path(L, q))}">{e(n)}</a>' for q, n in zip(navp, ui['nav']))
    fnav = (f'<a href="{u(hp)}">{e(S[c]["home"])}</a>' + tnav
            + ''.join(f'<a href="{u(I18N.page_path(L, q))}">{e(n)}</a>' for q, n in zip(['articles/', 'privacy/'], ui['foot_extra'])))
    gen = wa(ui['wa_generic'])
    return f'''<footer class="foot"><div class="wrap"><div class="fg">
<div><img src="/assets/ktech-logo-white.webp?v={KV}" alt="K Tech Auto Solution" width="110" height="56" loading="lazy" decoding="async"><p>K Tech Auto Solution Sdn. Bhd.<br>{e(ui['co'])} 201801038870 (1300901-K)<br><a href="{e(MAP)}" target="_blank" rel="noopener">{ADDR}</a></p>
<p><a href="{e(gen)}" target="_blank" rel="noopener" data-ref="footer">WhatsApp +60 12-546 2820</a><br><a href="tel:+60125462820" data-ref="footer-call">{e(ui['call'])} Autel Hooi +60 12-546 2820</a><br><a href="tel:+60109362820" data-ref="footer-call3">{e(ui['call'])} Tony +60 10-936 2820</a><br><a href="tel:+60125512820" data-ref="footer-call2">{e(ui['call'])} Gavin +60 12-551 2820</a><br>{e(ui['email'])}: <a href="mailto:sales@k-techmy.com">sales@k-techmy.com</a><br><a href="https://www.facebook.com/ktechautosolutionsb/" target="_blank" rel="noopener">Facebook: K Tech Auto Solution Sdn. Bhd. →</a><br><a href="https://www.facebook.com/KTechHooi/" target="_blank" rel="noopener">Facebook: K Tech-Autel-Hooi →</a></p></div>
<nav aria-label="Footer">{fnav}</nav>
<div><p>{e(ui['seo_p'])}</p><a class="seo-l" href="https://autoseo.my/">AutoSEO.my — SEO websites for automotive workshops</a></div></div>
<p class="tm">{e(ui['tm_autel'])}</p><p class="tm" style="border:0;margin:0;padding:0">© 2026 K Tech Auto Solution Sdn. Bhd.</p></div></footer>
<div class="dock">{dock_text}</div><script src="/assets/k.js?v={KV}" defer></script><script src="/assets/promo.js?v={JS_V}" defer></script><script src="/p1-cta.js?v=020caac6" defer></script>
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
    how = T(c, 'how_buy_pay' if PAY_REAL else 'how_buy_wa')
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
               f'<div class="pm-ended" style="margin-top:16px"><p>{e(T(c, "ended"))}</p>{wa_btn(T(c, "wa_ended"), T(c, "wa"), "promo-ms906max-ended")}</div></div></section>')
        terms = ''
        endsec = (f'<section class="sec dark end"><div class="wrap"><h2>{e(T(c, "end_h_end"))}</h2><p>{e(T(c, "end_p_end"))}</p>'
                  f'{wa_btn(T(c, "wa_ended"), T(c, "wa"), "end")}</div></section>')
        dock = wa_btn(T(c, 'wa_ended'), UI[c]['dock'], 'dock')
    else:
        top = (f'<section class="pm-ph"><div class="wrap"><div class="pm-grid" data-promo-live><div class="pm-h">{crumb}'
               f'<h1>{e(T(c, "h1"))}</h1><p class="line">{e(T(c, "lead"))}</p></div>{poster(c, True)}{info(L, True)}</div>'
               f'{ended_box(c)}</div></section>')
        terms = (f'<section class="sec alt" id="terms"><div class="wrap"><h2 class="pm-h2">{e(T(c, "tc_h"))}</h2>'
                 f'<ol class="pm-tc">' + ''.join(f'<li>{e(f(x, c))}</li>' for x in s['tc']) + '</ol>'
                 f'<p class="pm-auth">{e(T(c, "auth"))}</p></div></section>')
        endsec = (f'<section class="sec dark end"><div class="wrap" data-promo-live><h2>{e(T(c, "end_h"))}</h2><p>{e(T(c, "end_p"))}</p>'
                  f'<div class="pm-ctas" style="max-width:460px">{buy_btn(L)}{wa_btn(T(c, "wa_buy"), T(c, "wa"), "end", "btn btn-ghost")}</div></div>'
                  f'<div class="wrap" data-promo-ended hidden><h2>{e(T(c, "end_h_end"))}</h2><p>{e(T(c, "end_p_end"))}</p>{wa_btn(T(c, "wa_ended"), T(c, "wa"), "end")}</div></section>')
        dock = wa_btn(T(c, 'wa_buy'), UI[c]['dock'], 'dock')
    feat = (f'<section class="sec"><div class="wrap"><h2 class="pm-h2">{e(T(c, "feat_h"))}</h2><p class="pm-sub">{e(T(c, "feat_p"))}</p>'
            f'<div class="pm-feats">{feats}</div>'
            f'<div class="newbox pm-pro"><h2>{e(T(c, "pro_h"))}</h2><p>{e(T(c, "pro_p"))}</p><p><a href="{u(pro)}">{e(T(c, "pro_link"))}</a></p></div></div></section>')
    faq = f'<section class="sec"><div class="wrap"><h2 class="pm-h2">{e(T(c, "faq_h"))}</h2>{faq_html(faqs)}</div></section>'
    main = f'<main>{top}{feat}{terms}{faq}{endsec}</main>'
    return h + header(L) + main + footer(L, dock)


def tools_hl(L):
    c = L['code']
    return (SSI_IF + f'<div class="newbox pm-hl" data-promo-live><span class="mono">{e(T(c, "hl_label"))}</span><h2>{e(T(c, "hl_h"))}</h2>'
            f'<p>{e(T(c, "hl_p"))}</p><a class="btn btn-wa" href="{u(I18N.page_path(L, SLUG))}" data-ref="tools-ms906max-promo"><span>{e(T(c, "hl_btn"))}</span></a></div>'
            + SSI_END)


def pro_x(L):
    c = L['code']
    return (SSI_IF + f'<p class="pm-x" data-promo-live>{e(T(c, "pro_x"))} <a href="{u(I18N.page_path(L, SLUG))}">{e(T(c, "pro_x_link"))}</a></p>' + SSI_END)


def htaccess_block():
    out = ['# K Tech Autel MS906 MAX promo (21 Nov 2026), generated from promo.json by ms906max-promo build.py.',
           '# SSI picks the live/ended block on the home, promo, tools-index and MS906 Pro pages (DATE_GMT = UTC).',
           'Options +IncludesNOEXEC', 'SSILegacyExprParser on',
           '<If "%{REQUEST_URI} =~ m#^/((ms|zh)/)?(autel-ms906-max-promo/|autel-diagnostic-tools/|autel-diagnostic-tools/maxisys-ms906pro/)?(index\\.html)?$#">',
           '  SetOutputFilter INCLUDES', '</If>']
    rw = [f'# Buy now: /go/ms906max-buy/ decides at tap time. Server clock (%{{TIME}}) is UTC{C["server_utc_offset_hours"]:+d}; promo ends {C["end_local"]}.']
    for L in I18N.LANGS:
        c, pre = L['code'], L['prefix']
        target = C['payment_url'] if PAY_REAL else wa(T(c, 'wa_buy'))
        target = target.replace('%', '\\%')
        rx = '^' + pre.replace('/', '/') + 'go/ms906max-buy/?$'
        rw += [f'RewriteCond %{{TIME}} <{END_SRV}', f'RewriteRule {rx} {target} [R=302,L,NE]',
               f'RewriteRule {rx} {absu(I18N.page_path(L, SLUG))} [R=302,L]']
    return '\n'.join(out) + '\n', '\n'.join(rw) + '\n'


def main(out):
    files = {}
    for L in I18N.LANGS:
        files[I18N.page_path(L, SLUG) + 'index.html'] = SSI_IF + landing(L, False) + SSI_ELSE + landing(L, True) + SSI_END
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
    files['parts/versions.json'] = json.dumps({'css': CSS_V, 'js': JS_V, 'end_utc': END_UTC, 'end_server': END_SRV, 'pay_real': PAY_REAL})
    for p, txt in files.items():
        fp = os.path.join(out, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, 'w', encoding='utf-8').write(txt)
    bad = [w for w in ['lowest', 'cheapest', 'below market', 'US$', 'stock subject', 'SST', 'PAYMENT_URL_TBC'] if any(w.lower() in t.lower() for t in files.values() if not t.startswith('#'))]
    assert not bad, bad
    print('built', len(files), 'files; css', CSS_V, 'js', JS_V, 'end_server', END_SRV)


if __name__ == '__main__':
    main(sys.argv[1])
