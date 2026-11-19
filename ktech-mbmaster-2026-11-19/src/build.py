"""Build the ktech.my MBMaster announcement page in EN, BM and 中文 from strings.py + the shared AutoSEO template.
Header, footer and dock are the live ktech.my shared parts (read through the Bridge 19 Nov 2026), re-rendered per language.
Usage: python3 -I build.py OUTDIR
"""
import hashlib, json, os, sys
from html import escape as e
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import autoseo_i18n as I18N
from strings import FACTS, S, UI

# K Tech keeps its existing hreflang codes and og:locale (template README).
for L, code, loc in zip(I18N.LANGS, ['en-MY', 'ms-MY', 'zh-MY'], ['en_MY', 'ms_MY', 'zh_MY']):
    L['hreflang'] = code
    L['og_locale'] = loc

SITE = FACTS['site']
SLUG = FACTS['slug']
absu = lambda p: SITE + p
u = lambda p: '/' + p
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, 'mbmaster.css'), encoding='utf-8').read()
CSS_V = hashlib.sha256(CSS.encode()).hexdigest()[:8]
KV = '20261114t'  # live k.css / k.js / logo version
WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.2c0-.1-.2-.2-.5-.3z"/></svg>')
MAP = 'https://www.google.com/maps/search/?api=1&query=No.%2028%2C%20Jalan%20Ekoperniagaan%203/11%2C%20Taman%20Ekoperniagaan%2C%2081100%20Johor%20Bahru%2C%20Johor%2C%20Malaysia'
ADDR = 'No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor, Malaysia'


def wa(text):
    return f'https://wa.me/{FACTS["wa"]}?text=' + quote(text, safe='')


def wa_btn(text, label, ref):
    return (f'<a class="btn btn-wa" href="{e(wa(text))}" target="_blank" rel="noopener" data-ref="{ref}">'
            f'{WA_SVG}<span>{e(label)}</span></a>')


def shot(L, key, s, eager=False):
    name = FACTS['img'][key]
    w, h = FACTS['img_w'], FACTS['img_h']
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<figure class="shot"><div class="fr"><picture>'
            f'<source type="image/webp" srcset="/assets/mbmaster/{name}.webp">'
            f'<img src="/assets/mbmaster/{name}.jpg" alt="{e(s["alt_" + key])}" width="{w}" height="{h}" {load} decoding="async" draggable="false">'
            f'</picture></div><figcaption>{e(s["cap_" + key])}</figcaption></figure>')


def chips(items):
    return '<ul class="mb-chips">' + ''.join(f'<li>{e(x)}</li>' for x in items) + '</ul>'


def page(L):
    c = L['code']
    s, ui = S[c], UI[c]
    p = I18N.page_path(L, SLUG)
    hp = I18N.page_path(L, '')
    url = absu(p)
    og = absu('assets/mbmaster/' + FACTS['og'])
    sw = I18N.switcher(u, SLUG, L, 'Language', cls='lang').replace('<span class="sl" aria-hidden="true">/</span>', '')
    sw = sw.replace('<nav class="lang"', '<div class="lang"').replace('</nav>', '</div>')
    navp = ['autel-diagnostic-tools/', 'services/', 'about/', 'contact/']
    tnav = ''.join(f'<a href="{u(I18N.page_path(L, q))}">{e(n)}</a>' for q, n in zip(navp, ui['nav']))
    mnav = f'<a href="{u(hp)}">{e(s["home"])}</a>' + tnav
    fnav = (f'<a href="{u(hp)}">{e(s["home"])}</a>' + tnav
            + ''.join(f'<a href="{u(I18N.page_path(L, q))}">{e(n)}</a>' for q, n in zip(['articles/', 'privacy/'], ui['foot_extra'])))
    ld_page = {"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#page", "url": url,
               "name": s['title'], "description": s['desc'], "inLanguage": L['hreflang'],
               "publisher": {"@id": "https://ktech.my/#org"},
               "primaryImageOfPage": {"@type": "ImageObject", "url": absu('assets/mbmaster/' + FACTS['img']['hero'] + '.jpg'),
                                      "width": FACTS['img_w'], "height": FACTS['img_h']}}
    ld_bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": s['home'], "item": absu(hp)},
        {"@type": "ListItem", "position": 2, "name": s['crumb'], "item": url}]}
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld_page, ld_bc))
    head = f'''<!doctype html><html lang="{L['hreflang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(s['title'])}</title><meta name="description" content="{e(s['desc'])}"><meta name="robots" content="index,follow,max-image-preview:large">
<link rel="canonical" href="{url}">{I18N.hreflang_links(absu, SLUG).replace(chr(10), '')}
<meta property="og:type" content="website"><meta property="og:title" content="{e(s['title'])}"><meta property="og:description" content="{e(s['desc'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{og}"><meta property="og:image:secure_url" content="{og}"><meta property="og:image:type" content="image/jpeg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{e(s['alt_hero'])}"><meta name="twitter:image" content="{og}">{I18N.og_locale_tags(L).replace(chr(10), '')}<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f3f4f0"><link rel="icon" type="image/png" href="/assets/favicon.png"><link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{ui['fonts']}&display=swap">
<link rel="stylesheet" href="/assets/k.css?v={KV}"><link rel="stylesheet" href="/assets/mbmaster.css?v={CSS_V}">
<link rel="preload" as="image" type="image/webp" href="/assets/mbmaster/{FACTS['img']['hero']}.webp">{ld}</head>'''
    header = f'''<body><header class="top"><div class="wrap"><a class="brand" href="{u(hp)}" aria-label="K Tech Auto Solution"><img src="/assets/ktech-logo.webp?v={KV}" alt="K Tech Auto Solution logo" width="110" height="56" decoding="async"></a>
<nav class="tnav" aria-label="Main">{tnav}</nav>{sw}
<button class="menu-btn" aria-expanded="false" aria-controls="mnav" aria-label="{e(ui['menu'])}"><i></i><i></i><i></i></button></div><nav id="mnav" aria-label="Mobile">{mnav}</nav></header>'''
    main = f'''<main><section class="ph mb-hero"><div class="wrap"><div class="hgrid"><div><div class="crumb"><a href="{u(hp)}">{e(s['home'])}</a> / {e(s['crumb'])}</div><h1>{e(s['h1'])}</h1><p>{e(s['lead'])}</p>{wa_btn(s['wa_text'], s['btn_top'], 'top')}</div>
{shot(L, 'hero', s, eager=True)}</div></div></section>
<section class="sec"><div class="wrap"><div class="mb-row"><div class="mb-tx"><h2>{e(s['s1_h'])}</h2><p>{e(s['s1_p'])}</p>
<h2 style="margin-top:28px">{e(s['s2_h'])}</h2><p class="mb-sub">{e(s['s2_tabs'])}</p>{chips(FACTS['tabs'])}<p class="mb-sub">{e(s['s2_sub'])}</p>{chips(FACTS['subtabs'])}</div>
{shot(L, 'ui', s)}</div></div></section>
<section class="sec alt"><div class="wrap"><div class="mb-row flip"><div class="mb-tx"><h2>{e(s['s3_h'])}</h2><p>{e(s['s3_p1'])}</p><p>{e(s['s3_p2'])}</p></div>
{shot(L, 'info', s)}</div><div class="mb-row"><div class="mb-tx"><p>{e(s['s3_p3'])}</p></div>
{shot(L, 'result', s)}</div></div></section>
<section class="sec"><div class="wrap"><div class="mb-tx"><h2>{e(s['s4_h'])}</h2>{chips(FACTS['buttons'])}<p class="mb-sub">{e(s['s4_note'])}</p></div>
<div class="newbox mb-auth" style="margin:34px 0 0"><h2>{e(s['s5_h'])}</h2><p>{e(s['s5_p'])}</p><p class="mb-line">{e(s['s5_line'])}</p></div></div></section>
<section class="sec dark end"><div class="wrap"><h2>{e(s['end_h'])}</h2><p>{e(s['end_p'])}</p>{wa_btn(s['wa_text'], s['btn_end'], 'end')}</div></section></main>'''
    gen = wa(ui['wa_generic'])
    footer = f'''<footer class="foot"><div class="wrap"><div class="fg">
<div><img src="/assets/ktech-logo-white.webp?v={KV}" alt="K Tech Auto Solution" width="110" height="56" loading="lazy" decoding="async"><p>K Tech Auto Solution Sdn. Bhd.<br>{e(ui['co'])} 201801038870 (1300901-K)<br><a href="{e(MAP)}" target="_blank" rel="noopener">{ADDR}</a></p>
<p><a href="{e(gen)}" target="_blank" rel="noopener" data-ref="footer">WhatsApp +60 12-546 2820</a><br><a href="tel:+60125462820" data-ref="footer-call">{e(ui['call'])} Autel Hooi +60 12-546 2820</a><br><a href="tel:+60109362820" data-ref="footer-call3">{e(ui['call'])} Tony +60 10-936 2820</a><br><a href="tel:+60125512820" data-ref="footer-call2">{e(ui['call'])} Gavin +60 12-551 2820</a><br>{e(ui['email'])}: <a href="mailto:sales@k-techmy.com">sales@k-techmy.com</a><br><a href="https://www.facebook.com/ktechautosolutionsb/" target="_blank" rel="noopener">Facebook: K Tech Auto Solution Sdn. Bhd. →</a><br><a href="https://www.facebook.com/KTechHooi/" target="_blank" rel="noopener">Facebook: K Tech-Autel-Hooi →</a></p></div>
<nav aria-label="Footer">{fnav}</nav>
<div><p>{e(ui['seo_p'])}</p><a class="seo-l" href="https://autoseo.my/">AutoSEO.my — SEO websites for automotive workshops</a></div></div>
<p class="tm">{e(s['tm_note'])}</p><p class="tm" style="border:0;margin:0 0 12px;padding:0">{e(ui['tm_autel'])}</p><p class="tm" style="border:0;margin:0;padding:0">© 2026 K Tech Auto Solution Sdn. Bhd.</p></div></footer>
<div class="dock">{wa_btn(s['wa_text'], ui['dock'], 'dock')}</div><script src="/assets/k.js?v={KV}" defer></script><script src="/p1-cta.js?v=020caac6" defer></script>
</body></html>'''
    return p + 'index.html', head + header + main + footer


def main(out):
    files = {}
    for L in I18N.LANGS:
        path, html = page(L)
        files[path] = html
    probs = I18N.check_twins({p for p in files})
    assert not probs, probs
    files['assets/mbmaster.css'] = CSS
    for p, html in files.items():
        fp = os.path.join(out, p)
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        open(fp, 'w', encoding='utf-8').write(html)
    print('built', len(files), 'files; css v', CSS_V)


if __name__ == '__main__':
    main(sys.argv[1])
