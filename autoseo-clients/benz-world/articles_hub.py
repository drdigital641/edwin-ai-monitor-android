#!/usr/bin/env python3
"""Benz World /ms/articles/ and /zh/articles/ hubs (18 Nov 2026, AutoSEO 3-language rule).

Benz World has no site generator in the repo: its pages were built one by one. Until the planned template migration,
this script is the single source for the articles hub in all languages. The shared head/header/footer below are copied
from the live ms/zh article pages (Bridge read 18 Nov 2026) and the hreflang + sitemap entries come from the shared
AutoSEO template (autoseo-template/autoseo_i18n.py). No person names, no Google rating (Benz World rules).
  python3 articles_hub.py  -> out/ms/articles/index.html, out/zh/articles/index.html, out/sitemap-hub-rows.xml
"""
import html, json, os, sys, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'autoseo-template'))
import autoseo_i18n as I18N
E = html.escape
SITE = 'https://benzworld.my/'
absu = lambda p='': SITE + p
V = '20261114r10'
WA_NUM = '60127162860'

# Articles on the hub, newest first. Copy = the live article's own H1 and meta description in each language.
ARTICLES = [
    {'slug': 'electrical-faults-european-cars', 'date': '2026-11-18',
     'img': ('/assets/articles/electrical-faults-european-cars.jpg', 'Illustrative workshop check of a car battery and wiring with a multimeter'),
     'ms': ('Masalah elektrik kereta di Johor Bahru: tanda dan apa yang diperiksa',
            'Bateri kong, lampu berkelip atau amaran pelik pada Mercedes atau BMW anda? Ketahui tanda masalah elektrik dan apa yang diperiksa di Johor Bahru.'),
     'zh': ('新山汽车电路故障：常见迹象与检查内容', '奔驰或宝马电瓶没电、灯光闪烁或警告灯乱跳？了解常见电路故障迹象，以及在新山检查时会做什么。')},
    {'slug': 'how-to-choose-a-workshop-for-continental-cars-jb', 'date': '2026-11-16', 'img': None,
     'ms': ('Cara memilih bengkel untuk Mercedes atau BMW anda di Johor Bahru',
            'Soalan untuk ditanya sebelum memilih bengkel bagi Mercedes, BMW atau kereta Eropah lain di Johor Bahru, dari diagnosis hingga alat ganti.'),
     'zh': ('在新山如何为您的奔驰或宝马选修车厂', '在新山为奔驰、宝马或其他欧洲车选修车厂前该问的问题：从诊断、零件到车辆接送。')},
]

S = {
 'ms': {'title': 'Artikel Bengkel | Benz World', 'h1': 'Artikel bengkel', 'kicker': 'Artikel',
        'desc': 'Panduan ringkas dari bengkel Benz World di Permas Jaya, Johor Bahru, tentang servis Mercedes, BMW serta kereta British dan Amerika.',
        'lede': 'Nota dari bengkel di Permas Jaya tentang penjagaan Mercedes, BMW dan jenama lain yang kami servis.',
        'all': 'Semua artikel', 'home': 'Utama', 'og_locale': 'ms_MY', 'skip': 'Langkau ke kandungan', 'hours_top': 'Isnin hingga Sabtu 9 pagi hingga 7 malam',
        'lang_aria': 'Bahasa', 'logo_alt': 'Benz World 奔驰世界, Utama', 'brand_txt': 'Bengkel kereta<br>Permas Jaya, JB',
        'nav': [('', 'Utama'), ('services/', 'Servis'), ('about/', 'Tentang'), ('contact/', 'Hubungi')], 'menu': 'Menu', 'all_svc': 'Semua servis',
        'svcs': [('servicing', 'Servis berkala'), ('diagnostics', 'Diagnostik komputer'), ('engine-overhaul', 'Baiki enjin'), ('gearbox-overhaul', 'Baiki gearbox'),
                 ('suspension', 'Suspensi'), ('tyres-and-alignment', 'Tayar dan penjajaran'), ('brakes', 'Brek'), ('aircon', 'Aircond dan elektrik'),
                 ('performance', 'Prestasi dan hibrid'), ('pickup-and-delivery', 'Ambil dan hantar')],
        'ask_h': 'Tanya tentang kereta anda', 'ask_p': 'Hantar model, tahun dan apa yang anda perasan. Gambar atau video pendek bunyi itu membantu.',
        'wa_us': 'WhatsApp kami', 'call_long': 'Telefon +60 12-716 2860', 'wa_short': 'WhatsApp', 'call_short': 'Telefon',
        'prefill': 'Hi Benz World, saya ingin bertanya tentang kereta saya. Model dan tahun: ',
        'biz_desc': 'Benz World ialah bengkel di Permas Jaya, JB untuk Mercedes-Benz, BMW, jenama British dan Amerika. Isnin–Sabtu 9 pagi–7 malam. WhatsApp +60 12-716 2860.',
        'company_no': 'No. syarikat 202001016511 (1372831-U)', 'review': 'Tinggalkan ulasan Google', 'f_workshop': 'Bengkel', 'maps': 'Buka di Google Maps',
        'f_hours': 'Waktu', 'h_row': ('Isnin hingga Sabtu', '9:00 pagi hingga 7:00 malam'), 'sun': ('Ahad', 'Tutup'), 'f_phones': 'Telefon',
        'mobile': 'Telefon bimbit', 'landline': 'Talian bengkel', 'f_else': 'Pautan lain', 'fb': 'Halaman Facebook',
        'rights': '© 2026 Benz World (M) Sdn Bhd. Hak cipta terpelihara.', 'privacy': 'Privasi', 'credit': 'Laman web oleh AutoSEO',
        'date': lambda d: f"{int(d[8:])} November {d[:4]}", 'articles_label': 'Artikel'},
 'zh': {'title': '修车厂文章 | Benz World', 'h1': '修车厂文章', 'kicker': '文章',
        'desc': 'Benz World 新山 Permas Jaya 修车厂的实用短文：奔驰、宝马以及英国和美国品牌汽车的保养与维修。',
        'lede': '来自 Permas Jaya 修车厂的笔记，讲解如何照顾奔驰、宝马和我们维修的其他品牌。',
        'all': '全部文章', 'home': '首页', 'og_locale': 'zh_CN', 'skip': '跳到内容', 'hours_top': '星期一至六 上午9点至下午7点',
        'lang_aria': '语言', 'logo_alt': 'Benz World 奔驰世界, 首页', 'brand_txt': '修车厂<br>新山 Permas Jaya',
        'nav': [('', '首页'), ('services/', '服务'), ('about/', '关于我们'), ('contact/', '联系')], 'menu': '菜单', 'all_svc': '全部服务',
        'svcs': [('servicing', '定期保养'), ('diagnostics', '电脑诊断'), ('engine-overhaul', '发动机维修'), ('gearbox-overhaul', '变速箱维修'),
                 ('suspension', '悬挂避震'), ('tyres-and-alignment', '轮胎与定位'), ('brakes', '刹车'), ('aircon', '冷气与电路'),
                 ('performance', '性能升级与混动'), ('pickup-and-delivery', '车辆接送')],
        'ask_h': '咨询您的车子', 'ask_p': '请发送车型、年份和您察觉到的情况。附上照片或声音的短视频会有帮助。',
        'wa_us': 'WhatsApp 我们', 'call_long': '致电 +60 12-716 2860', 'wa_short': 'WhatsApp', 'call_short': '致电',
        'prefill': '你好 Benz World，我想咨询我的车子。车型和年份：',
        'biz_desc': 'Benz World 位于柔佛州新山百万镇（Permas Jaya），专修奔驰、宝马及欧美豪华品牌。星期一至六 上午9点至下午7点。WhatsApp +60 12-716 2860。',
        'company_no': '公司注册号 202001016511 (1372831-U)', 'review': '在 Google 给我们留评价', 'f_workshop': '修车厂', 'maps': '在 Google Maps 打开',
        'f_hours': '营业时间', 'h_row': ('星期一至六', '上午 9:00 至 下午 7:00'), 'sun': ('星期日', '休息'), 'f_phones': '电话',
        'mobile': '手机', 'landline': '车间直线', 'f_else': '其他链接', 'fb': 'Facebook 专页',
        'rights': '© 2026 Benz World (M) Sdn Bhd. 版权所有。', 'privacy': '隐私政策', 'credit': '网站由 AutoSEO 制作',
        'date': lambda d: f"{d[:4]}年{int(d[5:7])}月{int(d[8:])}日", 'articles_label': '文章'},
}

OFFERS = ['Car computer diagnostics', 'Standard routine servicing', 'Engine overhaul', 'Gearbox overhaul', 'Air conditioning services', 'Brakes repair',
          'Suspension repair and parts', 'Wheel, tyres and rims services', 'Wheel alignment and balancing', 'Vehicle pick-up and delivery', 'Battery services',
          'Electrical part repair', 'Wiring repair', 'Mechanical part repair', 'Engine tuning and conversion', 'Performance parts and upgrades',
          'Car wash and polish', 'Accessories retail']

WA_SVG = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path fill="currentColor" d="M12 2.2a9.7 9.7 0 0 0-8.4 14.6L2.3 21.8l5.1-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8 8 0 1 1 12 19.9Zm4.4-6c-.2-.1-1.4-.7-1.7-.8-.2-.1-.4-.1-.5.1l-.8 1c-.1.2-.3.2-.5.1a6.6 6.6 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.5-.4h-.5a.9.9 0 0 0-.7.3 2.8 2.8 0 0 0-.9 2.1 4.9 4.9 0 0 0 1 2.6 11.2 11.2 0 0 0 4.31 3.8c1.6.7 2.2.7 3 .6a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .2-1.2c-.1-.1-.2-.2-.5-.3Z"/></svg>'
CALL_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" d="M5 3.5h3.2l1.6 4.2-2.1 1.4a11 11 0 0 0 7.2 7.2l1.4-2.1 4.2 1.6V19a1.5 1.5 0 0 1-1.6 1.5A16.5 16.5 0 0 1 3.5 5.1 1.5 1.5 0 0 1 5 3.5Z"/></svg>'
REVIEW_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M8 9.5h8M8 12.5h5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>'
MAPS = 'https://www.google.com/maps/search/?api=1&amp;query=Benz%20World%20%28M%29%20Sdn%20Bhd&amp;query_place_id=ChIJsa08fGBr2jERpkLjv1U3qNw'


def langs_nav(L, path, T, cls):
    return I18N.switcher(lambda p: '/' + p, path, L, T['lang_aria'], cls)


def hub(code):
    L, T = I18N.lang(code), S[code]
    path = 'articles/'
    pre = L['prefix']
    wa = f"https://wa.me/{WA_NUM}?text={urllib.parse.quote(T['prefill'])}"
    biz = {"@type": ["AutomotiveBusiness", "AutoRepair"], "@id": "https://benzworld.my/#business", "name": "Benz World (M) Sdn Bhd",
           "legalName": "BENZ WORLD (M) SDN. BHD.", "alternateName": "Benz World", "description": T['biz_desc'], "url": absu(pre),
           "image": ["https://benzworld.my/assets/photos/cw-shop-cloud-1080.webp", "https://benzworld.my/assets/photos/cw-shop-sky-800.webp", "https://benzworld.my/assets/og.jpg"],
           "logo": {"@type": "ImageObject", "url": "https://benzworld.my/assets/brand/logo-dark-1200.png", "width": 1200, "height": 305},
           "telephone": "+60127162860",
           "contactPoint": [{"@type": "ContactPoint", "telephone": "+60127162860", "contactType": "customer service", "availableLanguage": ["en", "ms", "zh"]},
                            {"@type": "ContactPoint", "telephone": "+6073882660", "contactType": "customer service"}],
           "address": {"@type": "PostalAddress", "streetAddress": "No. 66, Jalan Permas 9/13, Bandar Baru Permas Jaya", "postalCode": "81750",
                       "addressLocality": "Masai", "addressRegion": "Johor", "addressCountry": "MY"},
           "geo": {"@type": "GeoCoordinates", "latitude": 1.4960935, "longitude": 103.822687}, "hasMap": "https://maps.google.com/?cid=15900019325862625958",
           "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": [f"https://schema.org/{d}" for d in
                                          ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]], "opens": "09:00", "closes": "19:00"}],
           "areaServed": [{"@type": "Place", "name": n} for n in ["Permas Jaya", "Masai", "Johor Bahru", "Johor"]],
           "sameAs": ["https://www.facebook.com/BenzWorldMSdnBhd/", "https://maps.google.com/?cid=15900019325862625958"],
           "identifier": {"@type": "PropertyValue", "propertyID": "SSM", "value": "202001016511"}, "knowsLanguage": ["en", "ms", "zh"],
           "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": o}} for o in OFFERS]}
    graph = [biz,
             {"@type": "WebPage", "@id": absu(pre + path) + "#page", "url": absu(pre + path), "name": T['title'], "inLanguage": L['hreflang'], "about": {"@id": "https://benzworld.my/#business"}},
             {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": T['home'], "item": absu(pre)},
                                                             {"@type": "ListItem", "position": 2, "name": T['articles_label'], "item": absu(pre + path)}]},
             {"@type": "CollectionPage", "name": T['h1'], "url": absu(pre + path), "inLanguage": L['hreflang'],
              "hasPart": [{"@type": "Article", "headline": a[code][0], "url": absu(pre + 'articles/' + a['slug'] + '/'), "datePublished": a['date']} for a in ARTICLES]}]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    nav = ''.join(f'<a href="/{pre}{p}">{E(n)}</a>' for p, n in T['nav']) + f'<a href="/{pre}articles/" aria-current="page">{E(T["articles_label"])}</a>'
    svcs = ''.join(f'<a href="/{pre}services/{s}/">{E(n)}</a>' for s, n in T['svcs'])
    cards = ''
    for a in ARTICLES:
        h, d = a[code]
        img = ''
        if a['img']:
            img = (f'<img src="{a["img"][0]}" alt="{E(a["img"][1])}" width="1024" height="1024" loading="lazy" decoding="async" '
                   'style="display:block;width:100%;height:auto;aspect-ratio:16/10;object-fit:cover;border-radius:12px;margin-bottom:12px">')
        cards += (f'<a class="art-card card" href="/{pre}articles/{a["slug"]}/">{img}<p class="kicker">{T["date"](a["date"])}</p>'
                  f'<h3>{E(h)}</h3><p>{E(d)}</p></a>')
    return f'''<!DOCTYPE html>
<html lang="{L['hreflang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(T['title'])}</title>
<meta name="description" content="{E(T['desc'])}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#121A33">
<script>document.documentElement.classList.add('js')</script>
<link rel="canonical" href="{absu(pre + path)}">
{I18N.hreflang_links(absu, path).replace(chr(10), '')}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Benz World">
<meta property="og:title" content="{E(T['title'])}">
<meta property="og:description" content="{E(T['desc'])}">
<meta property="og:url" content="{absu(pre + path)}">
<meta property="og:image" content="https://benzworld.my/assets/og.jpg">
<meta property="og:image:secure_url" content="https://benzworld.my/assets/og.jpg">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{T['og_locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(T['title'])}">
<meta name="twitter:description" content="{E(T['desc'])}">
<meta name="twitter:image" content="https://benzworld.my/assets/og.jpg">
<link rel="icon" href="/assets/brand/favicon.svg?v={V}" type="image/svg+xml">
<link rel="icon" href="/assets/favicon-32.png?v={V}" sizes="32x32" type="image/png">
<link rel="manifest" href="/site.webmanifest">
<link rel="apple-touch-icon" href="/assets/icon-180.png?v={V}">
<link rel="preload" href="/assets/fonts/newsreader-var.woff?v={V}" as="font" type="font/woff" crossorigin>

<link rel="stylesheet" href="/assets/site.css?v={V}">
<script type="application/ld+json">{ld}</script>
</head>

<body class="lang-{code} ">
<a class="skip" href="#main">{E(T['skip'])}</a>
<header class="site-head">
  <div class="topbar"><div class="wrap topbar-in">
    <span class="tb-hours">{E(T['hours_top'])}</span>
    {langs_nav(L, path, T, 'langs')}
  </div></div>
  <div class="wrap head-in">
    <a class="brand" href="/{pre}">
      <img class="brand-logo" src="/assets/brand/logo-dark.svg?v={V}" width="172" height="44" alt="{E(T['logo_alt'])}">
      <span class="brand-txt">{T['brand_txt']}</span>
    </a>
    <nav class="nav" aria-label="Menu">{nav}</nav>
    <details class="menu">
      <summary><span class="burger" aria-hidden="true"><i></i><i></i></span><span>{E(T['menu'])}</span></summary>
      <div class="menu-panel">
        <nav class="menu-main" aria-label="Menu">{nav}</nav>
        {langs_nav(L, path, T, 'langs langs-menu')}
        <p class="menu-k">{E(T['all_svc'])}</p>
        <nav class="menu-svcs" aria-label="{E(T['all_svc'])}">{svcs}</nav>
      </div>
    </details>
  </div>
</header>

<main id="main"><nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><a href="/{pre}">{E(T['home'])}</a><span aria-hidden="true">/</span><span aria-current="page">{E(T['articles_label'])}</span></div></nav><section class="sec tight"><div class="wrap art-intro">
  <p class="kicker">{E(T['kicker'])}</p>
  <h1>{E(T['h1'])}</h1>
  <p class="lede">{E(T['lede'])}</p>
</div></section>
<section class="sec" aria-labelledby="art-list-h"><div class="wrap">
  <h2 id="art-list-h" class="vh">{E(T['all'])}</h2>
  <div class="art-list">{cards}</div>
</div></section>
<section class="ask"><div class="wrap"><div class="ask-card ask-in" data-rv>
  <div><p class="kicker on-dark">WhatsApp</p><h2>{E(T['ask_h'])}</h2><p>{E(T['ask_p'])}</p></div>
  <div class="btn-row"><a class="btn btn-wa" href="{E(wa)}" data-cta="whatsapp_articles_hub">{WA_SVG}<span>{E(T['wa_us'])}</span></a>
<a class="btn btn-call btn-ghost" href="tel:+60127162860" data-cta="call_articles_hub">{CALL_SVG}<span>{E(T['call_long'])}</span></a>
</div>
</div></div></section></main>
<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="foot-col foot-brand">
      <img class="foot-logo" src="/assets/brand/logo-light.svg?v={V}" width="220" height="56" alt="Benz World 奔驰世界" loading="lazy" decoding="async">
      <p class="foot-legal">Benz World (M) Sdn Bhd<br>{E(T['company_no'])}</p>
      <a class="btn btn-review" href="/review.html?business=benzworld" data-cta="google_review_footer">{REVIEW_SVG}{E(T['review'])}</a>

    </div>
    <div class="foot-col">
      <h2 class="foot-h">{E(T['f_workshop'])}</h2>
      <address>Benz World (M) Sdn Bhd<br>No. 66, Jalan Permas 9/13, Bandar Baru Permas Jaya<br>81750 Masai, Johor, Malaysia</address>
      <p><a class="lnk" href="{MAPS}" target="_blank" rel="noopener" data-cta="map_footer">{E(T['maps'])}</a></p>
      <h2 class="foot-h">{E(T['f_hours'])}</h2>
      <table class="hours"><tr><th scope="row">{E(T['h_row'][0])}</th><td>{E(T['h_row'][1])}</td></tr><tr><th scope="row">{E(T['sun'][0])}</th><td>{E(T['sun'][1])}</td></tr></table>
    </div>
    <div class="foot-col">
      <h2 class="foot-h">{E(T['f_phones'])}</h2>
      <ul class="phones">
        <li><span class="who">{E(T['mobile'])}</span><a href="{E(wa)}" data-cta="whatsapp_footer" class="lnk">WhatsApp +60 12-716 2860</a></li>
        <li><span class="who">{E(T['mobile'])}</span><a href="tel:+60127162860" data-cta="call_footer" class="lnk">{E(T['call_long'])}</a></li>
        <li><span class="who">{E(T['landline'])}</span><a href="tel:+6073882660" data-cta="call_footer_landline" class="lnk">+60 7-388 2660</a></li>
      </ul>
      <h2 class="foot-h">{E(T['f_else'])}</h2>
      <p><a class="lnk" href="https://www.facebook.com/BenzWorldMSdnBhd/" target="_blank" rel="noopener" data-cta="facebook_footer">{E(T['fb'])}</a></p>
    </div>
  </div>
  <div class="wrap foot-base">
    <p>{E(T['rights'])}</p>
    <p><a class="lnk" href="/{pre}articles/" aria-current="page">{E(T['articles_label'])}</a><span aria-hidden="true"> · </span><a class="lnk" href="/{pre}privacy/">{E(T['privacy'])}</a><span aria-hidden="true"> · </span>{E(T['credit'])}</p>
  </div>
</footer>
<div class="mbar" role="group" aria-label="WhatsApp">
  <a class="btn btn-wa" href="{E(wa)}" data-cta="whatsapp_mobile_bar">{WA_SVG}<span>{E(T['wa_short'])}</span></a>
  <a class="btn btn-call" href="tel:+60127162860" data-cta="call_mobile_bar">{CALL_SVG}<span>{E(T['call_short'])}</span></a>
</div>

<script src="/assets/glide-wrapstar.js?v={V}" defer></script>
<script src="/assets/site.js?v={V}" defer></script>
<script src="/p1-cta.js?v=63c70953" defer></script>
</body>
</html>
'''


if __name__ == '__main__':
    out = os.path.join(HERE, 'out')
    for code in ('ms', 'zh'):
        d = os.path.join(out, code, 'articles')
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w', encoding='utf8').write(hub(code))
    print('built out/ms/articles/index.html, out/zh/articles/index.html')
