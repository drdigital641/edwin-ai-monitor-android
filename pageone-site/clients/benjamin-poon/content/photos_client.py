"""Photos supplied by Benjamin Poon via Edwin (22 Oct 2026). Served from jsDelivr (site-assets branch)."""
B = 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@90768b1/site-assets/benjamin-poon/'
CR = 'Photo: supplied by Benjamin Poon'


def _c(f, w, h, alt_en, alt_zh, role):
    return dict(url_large=B + f, url_small=B + f, w=w, h=h, alt_en=alt_en, alt_zh=alt_zh, credit=CR, source_page='', role=role, generic=False, client=True)


PHOTOS_CLIENT = {
    'cl-hall-buddhas': _c('hall-buddhas.webp', 1400, 1050, 'Grand hall with three golden Buddha statues and a lotus chandelier', '供奉三尊金色佛像、莲花吊灯的大殿', 'service:tablets'),
    'cl-lin-san': _c('lin-san-temple.webp', 1440, 1080, 'Lin San Temple 灵山寺 building at 27 Lorong 12 Geylang, lit at dusk', '芽笼12巷27号灵山寺外观（黄昏灯光）', 'venue:lin-san'),
    'cl-thian-leng': _c('thian-leng-temple.webp', 1024, 777, 'Thian Leng Chong Toh Tong 天灵总道堂 building on Changi Road', '樟宜路天灵总道堂外观', 'venue:thian-leng'),
}
