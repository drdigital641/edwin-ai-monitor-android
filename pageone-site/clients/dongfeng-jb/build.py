"""Dongfeng Johor Bahru (MyKar World): builds the 3-language site into site/ (python3 build.py).

New client from Edwin, 19 Oct 2026. English at /, Bahasa Melayu at /ms/, Simplified Chinese at /zh/.
Facts used, and where they came from:
- Edwin's message (19 Oct 2026): Dongfeng distributor for Johor Bahru; two models now, more colours to come from the
  client; prices NOT to be published yet; test drives welcome; three goals: sell the cars, online presence for the JB
  distributorship, attract dealers/partners.
- Client voice notes (Mandarin, forwarded by Edwin, 19 Oct 2026): "We are Dongfeng's 3S centre, currently Johor's first and
  only 3S centre. Besides Dongfeng, we want people to notice we are here, target Johor, and we hope big brands notice us and
  work with us." / "We only do passenger EVs, currently two models." / "Test drive: just WhatsApp to make an appointment."
  / "Price: not for now."
- Facebook page facebook.com/dongfengjohorbahru (read logged out, 19 Oct 2026): "DongFeng Johor Bahru", intro
  "MYKAR WORLD SDN BHD 202501050786(1652194-X) DongFeng Dealer Johor Bahru, Test Drive | Car Booking | EV Info";
  No.28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor (Edwin 20 Oct 2026 14:12 SGT: official address, site wide; Google listing's 3/13 is NOT used); +60 18-762 0828; marketing@mykar.my; mykar.my
  (does not resolve yet). Posts: Vigo and 007 (cover photo shows 007 Prime, 007 Premium, Vigo); roadshows at AEON Mall
  Bandar Dato' Onn (4-9 Aug 2026), Sutera Mall (25-28 Jun 2026), Lotus's Tebrau (4-6 Sep 2026), KIPMall Kota Tinggi;
  Merdeka 2026 children's event at the showroom; Yaya can bring a car to you for a test drive.
- Model figures: Dongfeng Cars Malaysia launch specifications, Feb 2026, as reported by autobuzz.my (5 and 6 Feb 2026)
  and carz.com.my. Only figures that agree between sources are used. Range is CLTC.
- Gavin (Dongfeng Johor Bahru staff), WhatsApp forwarded by Edwin 19 Oct 2026: full specs, colours, interiors and warranty for
  007 Long Range RWD Premium, 007 AWD Prime and Vigo Premier 120kW, plus a Google Drive folder of official photos. These
  client figures override the press figures where they differ (Vigo height 1,645 mm, also carsofmalaysia).
  Fact check 19 Oct 2026, Gavin's answers (WhatsApp 18:16-18:34 MYT): 007 Premium 650 km CLTC / 530 km WLTP; 007 Prime
  565 km CLTC / 389 km WLTP (his earlier 463 km was wrong); 007 DC 30-80%% in about 11 min; Vigo panoramic sunroof standard;
  "first in JB" OK (not "only"); showroom Mon-Sat 9am-6pm, Sun 10am-4pm; workshop Mon-Fri 9am-6pm, Sat 9am-1pm, Sun closed;
  service every 10,000 km; service and parts at Dongfeng list price; Instagram/TikTok links to follow, no Xiaohongshu.
- Official address (Edwin, 20 Oct 2026): No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor.
Not claimed anywhere: prices, monthly instalments, promotions, ratings, service menu prices.
"""
import html
import json
import os
import re
import shutil
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('DF_OUT', os.path.join(HERE, 'site'))

SLUG = 'dongfeng-jb'
DOMAIN = 'mykar.my'  # CONFIRM: domain on their Facebook page, not resolving yet
LIVE = False
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
# Hidden from Google by the X-Robots-Tag header in pageonesingapore.com/preview/.htaccess, never a meta tag (Edwin, 17 Oct 2026).
IMG = os.environ.get('DF_IMG', 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@0678e88/site-assets/dongfeng-jb/')
# Official photos added 19 Oct 2026 live in a later commit (kept separate so older pages did not all change).
IMG2 = os.environ.get('DF_IMG', 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@6f50fa4/site-assets/dongfeng-jb/')
IMG3 = os.environ.get('DF_IMG', 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@f8b49d4/site-assets/dongfeng-jb/')  # Voyah Dream
IMG4 = os.environ.get('DF_IMG', 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@5f2cea9/site-assets/dongfeng-jb/')  # full-res homepage photo (Edwin, 20 Oct 2026)
UPDATED = '2026-10-23'

NAME = 'Dongfeng Johor Bahru'
TRADE = 'MyKar World'
LEGAL, REGNO = 'MyKar World Sdn. Bhd.', '202501050786 (1652194-X)'
WA_NUM, WA_SHOW = '60187620828', '+60 18-762 0828'
TEL = '+60187620828'
EMAIL = 'marketing@mykar.my'
# Service / aftersales line (client, 23 Oct 2026): servicing, aftersales and parts go here; sales stays on WA_NUM.
SVC_NUM, SVC_SHOW = '60182240828', '+60 18-224 0828'
SVC_TEL = '+60182240828'
SVC_EMAIL = 'aftersales@mykar.my'
STREET, AREA, POSTAL, CITY = 'No. 28, Jalan Ekoperniagaan 3/11', 'Taman Ekoperniagaan', '81100', 'Johor Bahru'
ADDR = ['No. 28, Jalan Ekoperniagaan 3/11', 'Taman Ekoperniagaan, 81100 Johor Bahru', 'Johor, Malaysia']
MAPQ = quote('Dongfeng MyKar World, No. 28 Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru')
MAP = 'https://www.google.com/maps/search/?api=1&query=' + MAPQ
MAP_EMBED = 'https://www.google.com/maps?q=' + MAPQ + '&output=embed'
# Google Business Profile (Edwin 20 Oct 2026, share.google/Ku4wPPlRy8oDVCVyb -> kgmid /g/11nc0ckknp)
GBP = 'https://www.google.com/search?kgmid=/g/11nc0ckknp&q=MyKar+World+Sdn+Bhd'
FB = 'https://www.facebook.com/dongfengjohorbahru'
INDEXNOW_KEY = '8e41c2f7a9d34b6e90b1c5f2d7a3e816'

CONFIRM = [
    'Any appointment letter or certificate for "first Dongfeng 3S centre in Johor Bahru" we can show?',
    'Vigo Sandstone Beige: we have no photo of it yet',
    'Service centre: what you handle (scheduled service, warranty claims, repairs, EV battery checks) and how to book',
    'Spare parts: do you sell parts over the counter to the public and to other workshops?',
    'Partnerships: what you offer dealers and brands (sub-dealer terms, 3S hosting, roadshows) and who handles enquiries',
    'Domain: use mykar.my (on your Facebook page, not set up yet) or another?',
    'Real photos: showroom front, service bay, team, handovers (with customers\' permission)',
    'Instagram and TikTok links (Gavin will send; no Xiaohongshu yet)',
]

LANGS = ['en', 'ms', 'zh']
PFX = {'en': '', 'ms': 'ms/', 'zh': 'zh/'}
HREFLANG = {'en': 'en-MY', 'ms': 'ms-MY', 'zh': 'zh-MY'}
LANG_ATTR = {'en': 'en-MY', 'ms': 'ms-MY', 'zh': 'zh-Hans-MY'}
OG_LOCALE = {'en': 'en_MY', 'ms': 'ms_MY', 'zh': 'zh_CN'}
LANG_LABEL = {'en': 'EN', 'ms': 'BM', 'zh': '中文'}
E = html.escape


def T(en, ms, zh):
    return {'en': en, 'ms': ms, 'zh': zh}


def t(v, L):
    return v[L] if isinstance(v, dict) else v


PHOTOS = {  # name: (w, h, alt)
    'hero': (1773, 656, T('Dongfeng 007 Prime, 007 Premium and Vigo electric cars at night',
                         'Kereta elektrik Dongfeng 007 Prime, 007 Premium dan Vigo pada waktu malam',
                         '夜色中的东风 007 Prime、007 Premium 与 Vigo 纯电车')),
    'vigo-showroom': (720, 720, T('Orange Dongfeng Vigo electric SUV in the Johor Bahru showroom',
                                  'Dongfeng Vigo SUV elektrik oren di bilik pameran Johor Bahru',
                                  '新山展厅里的橙色东风 Vigo 纯电 SUV')),
    '007-showroom': (720, 720, T('White Dongfeng 007 electric sedan in the Johor Bahru showroom',
                                 'Dongfeng 007 sedan elektrik putih di bilik pameran Johor Bahru',
                                 '新山展厅里的白色东风 007 纯电轿跑')),
    'vigo-cabin': (720, 720, T('Dongfeng Vigo cabin: floating screen, two-spoke wheel and grey seats',
                               'Kabin Dongfeng Vigo: skrin terapung, stereng dua jejari dan tempat duduk kelabu',
                               '东风 Vigo 座舱：悬浮屏、双辐方向盘与灰色座椅')),
    'vigo-dash': (720, 720, T('Dongfeng Vigo dashboard and centre console, new car in the showroom',
                              'Papan pemuka dan konsol tengah Dongfeng Vigo, kereta baharu di bilik pameran',
                              '东风 Vigo 仪表台与中控台，展厅新车')),
    'cabin-quilted': (720, 720, T('Dongfeng EV cabin with quilted white trim and large centre screen',
                                  'Kabin EV Dongfeng dengan kemasan putih berjahit dan skrin tengah besar',
                                  '东风电动车座舱：白色绗缝饰板与大尺寸中控屏')),
    'pair-skyline': (495, 405, T('Dongfeng Vigo and Dongfeng 007 side by side',
                                 'Dongfeng Vigo dan Dongfeng 007 bersebelahan',
                                 '东风 Vigo 与东风 007 并排')),
    'showroom-front': (525, 385, T('Dongfeng MyKar World showroom front in Taman Ekoperniagaan, Johor Bahru',
                                   'Hadapan bilik pameran Dongfeng MyKar World di Taman Ekoperniagaan, Johor Bahru',
                                   '位于新山 Taman Ekoperniagaan 的东风 MyKar World 展厅外观')),
    'merdeka-2026': (1000, 1000, T('Merdeka 2026 children\'s costume day at the Dongfeng Johor Bahru showroom',
                                   'Hari kostum kanak-kanak Merdeka 2026 di bilik pameran Dongfeng Johor Bahru',
                                   '2026 年国庆日儿童服装活动，在东风新山展厅举行')),
}
# Official Dongfeng photos from the client's Google Drive (Gavin, 19 Oct 2026). Colour cut-outs have transparent backgrounds.
OFFICIAL = {
    '007-hero': (1600, 1092, T('Dongfeng 007 electric sedan on an open road at sunset', 'Sedan elektrik Dongfeng 007 di jalan terbuka ketika matahari terbenam', '夕阳下行驶在开阔公路上的东风 007 纯电轿跑')),
    '007-studio': (1200, 718, T('Dongfeng 007 in Celestial White Metallic, front three-quarter view', 'Dongfeng 007 warna Celestial White Metallic, pandangan tiga suku hadapan', '星云白金属漆东风 007，前 45 度视角')),
    '007-sea': (1200, 630, T('Dongfeng 007 fastback by the sea at dusk', 'Dongfeng 007 fastback di tepi laut waktu senja', '黄昏海边的东风 007 轿跑')),
    '007-top': (970, 545, T('Dongfeng 007 in Starlit Silver from above, showing the glass roof', 'Dongfeng 007 Starlit Silver dari atas, menunjukkan bumbung kaca', '俯视星光银东风 007，可见全景玻璃车顶')),
    '007-black': (1200, 718, T('Dongfeng 007 in Obsidian Black Metallic', 'Dongfeng 007 warna Obsidian Black Metallic', '曜石黑金属漆东风 007')),
    '007-life': (1200, 800, T('Dongfeng 007 parked outside a café while its owner works on a laptop', 'Dongfeng 007 diletakkan di luar kafe sementara pemiliknya bekerja dengan komputer riba', '停在咖啡馆外的东风 007，车主在一旁用电脑办公')),
    '007-cabin': (1200, 750, T('Dongfeng 007 cabin with 15.6-inch screen and light seats', 'Kabin Dongfeng 007 dengan skrin 15.6 inci dan tempat duduk cerah', '东风 007 座舱：15.6 英寸中控屏与浅色座椅')),
    '007-seats': (1163, 609, T('Dongfeng 007 front and rear seats through the frameless door', 'Tempat duduk hadapan dan belakang Dongfeng 007 melalui pintu tanpa bingkai', '透过无框车门看东风 007 前后排座椅')),
    '007-seat': (1200, 750, T('Dongfeng 007 front seat with white contrast stitching', 'Tempat duduk hadapan Dongfeng 007 dengan jahitan kontras putih', '东风 007 前排座椅，白色撞色设计')),
    '007-dash': (1200, 750, T('Dongfeng 007 dashboard, steering wheel and centre screen', 'Papan pemuka, stereng dan skrin tengah Dongfeng 007', '东风 007 仪表台、方向盘与中控屏')),
    '007-wheel': (1200, 750, T('Dongfeng 007 steering wheel and 8.8-inch driver display', 'Stereng dan paparan pemandu 8.8 inci Dongfeng 007', '东风 007 方向盘与 8.8 英寸液晶仪表')),
    '007-boot': (1200, 750, T('Dongfeng 007 boot with the lid and rear window open', 'But Dongfeng 007 dengan penutup dan cermin belakang terbuka', '东风 007 后备箱，尾门连同后挡风玻璃开启')),
    '007-door': (1200, 750, T('Dongfeng 007 frameless door and mirror', 'Pintu tanpa bingkai dan cermin sisi Dongfeng 007', '东风 007 无框车门与外后视镜')),
    '007-charge': (1200, 800, T('Dongfeng 007 wireless phone charger in the centre console', 'Pengecas telefon tanpa wayar di konsol tengah Dongfeng 007', '东风 007 中控台无线手机充电')),
    '007-c-white': (900, 346, T('Dongfeng 007 in Celestial White Metallic, side view', 'Dongfeng 007 Celestial White Metallic, pandangan sisi', '星云白金属漆东风 007 侧面')),
    '007-c-grey': (900, 346, T('Dongfeng 007 in Eclipse Grey Metallic, side view', 'Dongfeng 007 Eclipse Grey Metallic, pandangan sisi', '日蚀灰金属漆东风 007 侧面')),
    '007-c-black': (900, 346, T('Dongfeng 007 in Obsidian Black Metallic, side view', 'Dongfeng 007 Obsidian Black Metallic, pandangan sisi', '曜石黑金属漆东风 007 侧面')),
    '007-c-silver': (900, 346, T('Dongfeng 007 in Starlit Silver Metallic, side view', 'Dongfeng 007 Starlit Silver Metallic, pandangan sisi', '星光银金属漆东风 007 侧面')),
    'vigo-hero': (1600, 1200, T('Dongfeng Vigo in Mosswood Green on a coastal highway', 'Dongfeng Vigo Mosswood Green di lebuh raya pantai', '行驶在海滨公路上的苔林绿东风 Vigo')),
    'vigo-beach': (1200, 748, T('Two Dongfeng Vigo SUVs on a beach', 'Dua SUV Dongfeng Vigo di pantai', '海滩上的两辆东风 Vigo')),
    'vigo-picnic': (1200, 800, T('Family picnic beside a Dongfeng Vigo with the tailgate open', 'Keluarga berkelah di sebelah Dongfeng Vigo dengan pintu belakang terbuka', '一家人在打开尾门的东风 Vigo 旁野餐')),
    'vigo-bed': (1200, 800, T('Dongfeng Vigo rear seats folded flat into a bed, children playing inside', 'Tempat duduk belakang Dongfeng Vigo dilipat rata menjadi katil, kanak-kanak bermain di dalam', '东风 Vigo 后排放平成床，孩子们在车里玩耍')),
    'vigo-boot': (1200, 800, T('Loading groceries into the Dongfeng Vigo boot', 'Memuatkan barang ke dalam but Dongfeng Vigo', '往东风 Vigo 后备箱里装东西')),
    'vigo-camp': (1200, 800, T('Couple relaxing in the open boot of a Dongfeng Vigo', 'Pasangan berehat di but terbuka Dongfeng Vigo', '坐在东风 Vigo 敞开后备箱里休息的情侣')),
    'vigo-tailgate': (1200, 675, T('Dongfeng Vigo split tailgate open', 'Pintu belakang terbelah Dongfeng Vigo dibuka', '东风 Vigo 分体式尾门开启')),
    'vigo-rear': (900, 1359, T('Dongfeng Vigo rear view in Canyon Orange', 'Pandangan belakang Dongfeng Vigo Canyon Orange', '峡谷橙东风 Vigo 车尾')),
    'vigo-front': (1200, 675, T('Dongfeng Vigo front view in Canyon Orange', 'Pandangan hadapan Dongfeng Vigo Canyon Orange', '峡谷橙东风 Vigo 车头')),
    'vigo-cabin2': (1200, 669, T('Dongfeng Vigo cabin with light grey and black seats', 'Kabin Dongfeng Vigo dengan tempat duduk kelabu cerah dan hitam', '东风 Vigo 座舱，浅灰与黑色双拼座椅')),
    'vigo-screen': (1200, 900, T('Dongfeng Vigo 12.8-inch centre screen', 'Skrin tengah 12.8 inci Dongfeng Vigo', '东风 Vigo 12.8 英寸中控屏')),
    'vigo-roof': (1200, 800, T('Dongfeng Vigo panoramic sunroof above the seats', 'Bumbung matahari panoramik Dongfeng Vigo', '东风 Vigo 全景天窗')),
    'vigo-rims': (1200, 568, T('Dongfeng Vigo alloy wheel in Mosswood Green', 'Rim aloi Dongfeng Vigo Mosswood Green', '苔林绿东风 Vigo 轮毂特写')),
    'vigo-ambient': (1200, 900, T('Dongfeng Vigo ambient door lighting', 'Lampu suasana pintu Dongfeng Vigo', '东风 Vigo 门板氛围灯')),
    'vigo-charge': (1200, 800, T('Dongfeng Vigo 50 W wireless charger in the sunken console', 'Pengecas tanpa wayar 50 W di konsol tenggelam Dongfeng Vigo', '东风 Vigo 下沉式中控台 50 W 无线充电')),
    'vigo-c-green': (900, 454, T('Dongfeng Vigo in Mosswood Green', 'Dongfeng Vigo Mosswood Green', '苔林绿东风 Vigo')),
    'vigo-c-orange': (900, 454, T('Dongfeng Vigo in Canyon Orange', 'Dongfeng Vigo Canyon Orange', '峡谷橙东风 Vigo')),
    'vigo-c-white': (900, 454, T('Dongfeng Vigo in Arctic White', 'Dongfeng Vigo Arctic White', '极地白东风 Vigo')),
    'vigo-c-silver': (900, 454, T('Dongfeng Vigo in Titanium Silver', 'Dongfeng Vigo Titanium Silver', '钛银东风 Vigo')),
    'vigo-c-black': (900, 454, T('Dongfeng Vigo in Cyber Black', 'Dongfeng Vigo Cyber Black', '赛博黑东风 Vigo')),
}
PHOTOS.update(OFFICIAL)
VOYAH_PHOTOS = {
    'voyah-side': (1600, 800, T('Voyah Dream luxury MPV by a calm lake with snow-capped hills', 'MPV mewah Voyah Dream di tepi tasik dengan bukit bersalji', '湖畔雪山前的岚图梦想家豪华 MPV')),
    'voyah-door': (1600, 800, T('Voyah Dream with its sliding door open, showing the captain seats', 'Voyah Dream dengan pintu gelongsor terbuka, menunjukkan tempat duduk kapten', '岚图梦想家侧滑门打开，可见航空座椅')),
    'voyah-rear': (1600, 800, T('Voyah Dream MPV, rear three-quarter view by the water', 'MPV Voyah Dream, pandangan tiga suku belakang di tepi air', '水边的岚图梦想家 MPV，后 45 度视角')),
}
PHOTOS.update(VOYAH_PHOTOS)


try:
    IMGMAP = json.load(open(os.path.join(HERE, 'assets', 'img', 'map.json'))) if os.environ.get('DF_LOCAL_IMG') else {}
except Exception:
    IMGMAP = {}


def img_base(name):
    return IMG4 if name == 'hero' else IMG3 if name in VOYAH_PHOTOS else IMG2 if name in OFFICIAL else IMG


def img(name, L, cls='', eager=False):
    w, h, alt = PHOTOS[name]
    src = '%s%s.webp' % (img_base(name), name)
    if src in IMGMAP:  # compressed copy hosted on this site (assets/img, built by the image-fetch workflow)
        m = IMGMAP[src]
        src, w, h = SITE + 'img/' + m['f'], m['w'], m['h']
    return '<img src="%s" alt="%s" width="%d" height="%d"%s%s>' % (
        src, E(t(alt, L)), w, h, ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"', ' class="%s"' % cls if cls else '')


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.8-1.4.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 '
          '11.9 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3Z"/></svg>')

# ---------------------------------------------------------------------------------------------
# Shared words
# ---------------------------------------------------------------------------------------------
W = {
    'tagline': T('Dongfeng 3S Centre · Johor Bahru', 'Pusat 3S Dongfeng · Johor Bahru', '东风 3S 中心 · 新山'),
    'book': T('Book a test drive', 'Tempah pandu uji', '预约试驾'),
    'explore': T('Explore the models', 'Lihat model', '查看车型'),
    'whatsapp': T('WhatsApp us', 'WhatsApp kami', 'WhatsApp 联系我们'),
    'more': T('More details', 'Maklumat lanjut', '了解更多'),
    'read': T('Read the guide', 'Baca panduan', '阅读文章'),
    'home': T('Home', 'Utama', '首页'),
    'menu': T('Menu', 'Menu', '菜单'),
    'models': T('Models', 'Model', '车型'),
    'nav': [('models/', T('Models', 'Model', '车型')), ('test-drive/', T('Test drive', 'Pandu uji', '试驾')),
            ('service/', T('Service', 'Servis', '售后服务')), ('partners/', T('Partners', 'Rakan niaga', '合作')),
            ('articles/', T('Guides', 'Panduan', 'EV 指南')), ('about/', T('About', 'Tentang kami', '关于我们')),
            ('contact/', T('Contact', 'Hubungi', '联系'))],
    'band_h': T('Ready to feel it on the road?', 'Mahu rasa sendiri di jalan raya?', '想亲自上路感受一下吗？'),
    'band_p': T('WhatsApp us to book a test drive in Johor Bahru. Tell us the model and a time that suits you. Already driving a Dongfeng? Tap Service booking.',
                'WhatsApp kami untuk tempah pandu uji di Johor Bahru. Beritahu model dan masa yang sesuai. Sudah memandu Dongfeng? Tekan Tempahan servis.',
                'WhatsApp 我们预约新山试驾，告诉我们想试的车型和方便的时间即可。已是东风车主？请点“保养预约”。'),
    'wa_msg': T('Hi Dongfeng Johor Bahru, I saw your website. I would like to ask about ',
                'Hai Dongfeng Johor Bahru, saya lihat laman web anda. Saya ingin bertanya tentang ',
                '你好，东风新山，我在网站上看到你们，想询问 '),
    'wa_td': T('a test drive.', 'pandu uji.', '试驾。'),
    'wa_svc': T('servicing my Dongfeng.', 'servis Dongfeng saya.', '我的东风车保养。'),
    'sales': T('Sales enquiry', 'Pertanyaan jualan', '销售咨询'),
    'sales_sub': T('New cars and promotions', 'Kereta baharu dan promosi', '新车与优惠'),
    'svc': T('Service booking', 'Tempahan servis', '保养预约'),
    'svc_sub': T('Servicing and aftersales support', 'Servis dan sokongan selepas jualan', '保养与售后支持'),
    'sales_wa': T('Sales WhatsApp', 'WhatsApp jualan', '销售 WhatsApp'),
    'svc_wa': T('Service WhatsApp', 'WhatsApp servis', '售后 WhatsApp'),
    'sales_em': T('Sales email', 'E-mel jualan', '销售电邮'),
    'svc_em': T('Aftersales email', 'E-mel selepas jualan', '售后电邮'),
    'ftr_about': T('Johor\'s Dongfeng 3S centre for sales, service and spare parts. Dongfeng passenger EVs in Johor Bahru, operated by MyKar World Sdn. Bhd.',
                   'Pusat 3S Dongfeng di Johor untuk jualan, servis dan alat ganti. Kereta penumpang elektrik Dongfeng di Johor Bahru, dikendalikan oleh MyKar World Sdn. Bhd.',
                   '柔佛东风 3S 中心：销售、售后服务与零配件。东风纯电乘用车，新山，由 MyKar World Sdn. Bhd. 经营。'),
    'explore_h': T('Explore', 'Terokai', '浏览'),
    'contact_h': T('Contact', 'Hubungi', '联系'),
    'privacy': T('Privacy', 'Privasi', '隐私政策'),
    'built': T('Website & SEO by', 'Laman web & SEO oleh', '网站与 SEO：'),
    'reg': T('Company No.', 'No. Syarikat', '公司注册号'),
    'faq_h': T('Questions', 'Soalan lazim', '常见问题'),
    'updated': T('Updated', 'Dikemas kini', '更新于'),
    'by': T('By the Dongfeng Johor Bahru team', 'Oleh pasukan Dongfeng Johor Bahru', '东风新山团队'),
    'specsrc': T('Figures are the Malaysian specifications of the Vigo Premier 120kW, 007 Long Range RWD Premium and 007 AWD Prime (Dongfeng Johor Bahru, October 2026). Range is the manufacturer\'s test figure; real-world range is lower and depends on speed, load, weather and air-con. Ask us to confirm the figures for the exact car you are buying.',
                 'Angka ialah spesifikasi Malaysia bagi Vigo Premier 120kW, 007 Long Range RWD Premium dan 007 AWD Prime (Dongfeng Johor Bahru, Oktober 2026). Jarak ialah angka ujian pengeluar; jarak sebenar lebih rendah dan bergantung pada kelajuan, muatan, cuaca dan penghawa dingin. Tanya kami untuk mengesahkan angka bagi kereta yang anda beli.',
                 '数据为 Vigo Premier 120kW、007 Long Range RWD Premium 与 007 AWD Prime 的马来西亚规格（东风新山，2026 年 10 月）。续航为厂家测试数据，实际续航会更低，并受车速、载重、天气与冷气影响。购车前请向我们确认具体车辆的数据。'),
}


def wa_url(L, topic=None, svc=False):
    return 'https://wa.me/%s?text=%s' % (SVC_NUM if svc else WA_NUM, quote(t(W['wa_msg'], L) + (topic or t(W['wa_svc' if svc else 'wa_td'], L))))


def wa_btn(L, label=None, topic=None, cls='btn btn-red', svc=False):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa_url(L, topic, svc)), WA_SVG, E(label or t(W['book'], L)))


def wa_pair(L, dark=False):
    # Two WhatsApp lines (client, 23 Oct 2026): Sales enquiry on the sales number, Service booking on the service number.
    return wa_btn(L, t(W['sales'], L), t(T('new cars and promotions.', 'kereta baharu dan promosi.', '新车与优惠。'), L)) + \
        wa_btn(L, t(W['svc'], L), cls='btn btn-ghost' if dark else 'btn btn-line', svc=True)


def brand_html(pre):
    return ('<a class="brand" href="%s"><img src="%semblem-128.webp" alt="Dongfeng" width="38" height="38">'
            '<span><b>DONGFENG</b><small>Johor Bahru · MyKar World</small></span></a>') % (pre or './', IMG)


def faq_html(items, L):
    return '<div class="faq">%s</div>' % ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(t(q, L)), E(t(a, L))) for q, a in items)


def faq_schema(items, L):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': t(q, L), 'acceptedAnswer': {'@type': 'Answer', 'text': t(a, L)}} for q, a in items]}


def ticks(items, L):
    return '<ul class="ticks">%s</ul>' % ''.join('<li>%s</li>' % E(t(i, L)) for i in items)


def steps(items, L):
    return '<ol class="steps">%s</ol>' % ''.join('<li><b>%s</b><span>%s</span></li>' % (E(t(a, L)), E(t(b, L))) for a, b in items)


def glide(names, L, caps=None, label=None):
    out = []
    for i, n in enumerate(names):
        cap = t(caps[i], L) if caps else ''
        out.append('<figure class="gl-item">%s%s</figure>' % (img(n, L), '<figcaption>%s</figcaption>' % E(cap) if cap else ''))
    return '<div class="glide" role="region" aria-label="%s">%s</div>' % (E(t(label or T('Showroom photos', 'Foto bilik pameran', '展厅照片'), L)), ''.join(out))


def sec_head(eyebrow, h2, p, L, center=False):
    return '<div class="sec-head%s"><span class="eyebrow">%s</span><h2>%s</h2>%s</div>' % (
        ' center' if center else '', E(t(eyebrow, L)), E(t(h2, L)), '<p>%s</p>' % E(t(p, L)) if p else '')


# ---------------------------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------------------------
# Colours from Gavin (Dongfeng Johor Bahru), 19 Oct 2026: (name, swatch hex, photo name or None). Hex is an on-screen approximation.
COLOURS = {
    'vigo': [('Mosswood Green', '#56604a', 'vigo-c-green'), ('Canyon Orange', '#c45a2a', 'vigo-c-orange'), ('Arctic White', '#e9ebea', 'vigo-c-white'),
             ('Sandstone Beige', '#c9b596', None), ('Titanium Silver', '#a6aaad', 'vigo-c-silver'), ('Cyber Black', '#1c1d20', 'vigo-c-black')],
    '007': [('Celestial White Metallic', '#eceeee', '007-c-white'), ('Eclipse Grey Metallic', '#555a60', '007-c-grey'),
            ('Obsidian Black Metallic', '#16171a', '007-c-black'), ('Starlit Silver Metallic', '#b9bdc1', '007-c-silver')],
}
WARRANTY = (T('Warranty', 'Waranti', '保修'), T('8 years, unlimited mileage (powertrain) · 6 years, unlimited mileage (vehicle)', '8 tahun, tanpa had perbatuan (powertrain) · 6 tahun, tanpa had perbatuan (kenderaan)', '动力总成 8 年不限里程 · 整车 6 年不限里程'))
WTY_SHORT = T('8 yr powertrain · 6 yr vehicle, unlimited km', '8 thn powertrain · 6 thn kenderaan, tanpa had km', '动力总成 8 年 · 整车 6 年，不限里程')

MODELS = [
    dict(slug='vigo', name='Dongfeng Vigo', interior=T('Six colours. Mosswood Green is the launch colour. Cabin: light grey and black dual-tone vegan leather. On-screen colours are a guide; see the real paint in our showroom.', 'Enam warna. Mosswood Green ialah warna pelancaran. Kabin: kulit vegan dua tona kelabu cerah dan hitam. Warna di skrin hanya panduan; lihat cat sebenar di bilik pameran kami.', '共六色，苔林绿为上市主打色。内饰：浅灰与黑色双拼素食皮革。屏幕颜色仅供参考，实车漆面请到展厅查看。'), photo='vigo-showroom', card='vigo-hero', hero='vigo-hero',
         official=['vigo-beach', 'vigo-front', 'vigo-tailgate', 'vigo-bed', 'vigo-picnic', 'vigo-cabin2', 'vigo-screen', 'vigo-roof', 'vigo-ambient', 'vigo-charge', 'vigo-rims', 'vigo-camp', 'vigo-rear'],
         tag=T('Electric SUV · 5 seats', 'SUV elektrik · 5 tempat duduk', '纯电 SUV · 5 座'),
         short=T('A roomy electric SUV for family life in Johor: 500-litre boot, split tailgate bench and rear seats that fold into a 2-metre bed.',
                 'SUV elektrik yang luas untuk keluarga di Johor: but 500 liter, pintu belakang terbelah dengan bangku dan tempat duduk belakang yang dilipat menjadi katil 2 meter.',
                 '宽敞的纯电 SUV：500 升后备箱、可当长凳的分体尾门，后排放平即成 2 米大床，适合柔佛家庭日常。'),
         title=T('Dongfeng Vigo Electric SUV Johor Bahru | Dongfeng JB',
                 'Dongfeng Vigo SUV Elektrik di Johor Bahru | Dongfeng JB',
                 '东风 Vigo 纯电 SUV 新山 | 东风新山 3S 中心'),
         desc=T('See the Dongfeng Vigo electric SUV at our Johor Bahru 3S centre: 51.87 kWh battery, 471 km CLTC range, 500 L boot. Book a test drive on WhatsApp.',
                'Lihat Dongfeng Vigo SUV elektrik di pusat 3S kami di Johor Bahru: bateri 51.87 kWh, jarak 471 km CLTC, but 500 L. Tempah pandu uji melalui WhatsApp.',
                '到新山东风 3S 中心看东风 Vigo 纯电 SUV：51.87 kWh 电池、CLTC 续航 471 公里、500 升后备箱。WhatsApp 预约试驾。'),
         h1=T('Dongfeng Vigo electric SUV in Johor Bahru', 'Dongfeng Vigo SUV elektrik', '东风 Vigo 纯电 SUV'),
         lede=T('Smart, spacious and fully electric. See it, sit in it and drive it in Johor Bahru.',
                'Pintar, luas dan elektrik sepenuhnya. Lihat, duduk dan pandu sendiri di Johor Bahru.',
                '聪明、宽敞、纯电驱动。在新山亲眼看、亲自坐、亲手开。'),
         answer=T('The Dongfeng Vigo is a five-seat electric SUV with a 51.87 kWh LFP battery, a 120 kW (161 hp) front motor and a claimed 471 km range on the CLTC cycle. It has a 500-litre boot (1,040 litres with the rear seats folded), a split tailgate whose lower half folds out as a bench, and a 3.3 kW V2L socket to power devices from the battery. You can see it and book a test drive at our 3S centre in Taman Ekoperniagaan, Johor Bahru.',
                  'Dongfeng Vigo ialah SUV elektrik lima tempat duduk dengan bateri LFP 51.87 kWh, motor hadapan 120 kW (161 hp) dan jarak 471 km pada kitaran CLTC. Ia mempunyai but 500 liter (1,040 liter apabila tempat duduk belakang dilipat), pintu belakang terbelah yang bahagian bawahnya menjadi bangku, dan soket V2L 3.3 kW untuk menghidupkan peranti daripada bateri. Anda boleh melihatnya dan tempah pandu uji di pusat 3S kami di Taman Ekoperniagaan, Johor Bahru.',
                  '东风 Vigo 是一款五座纯电 SUV，配备 51.87 kWh 磷酸铁锂电池、120 kW（161 匹）前置电机，CLTC 工况续航 471 公里。它拥有 500 升后备箱（后排放倒可达 1,040 升）、下半部可翻成长凳的分体式尾门，以及 3.3 kW V2L 对外放电。欢迎到新山 Taman Ekoperniagaan 的东风 3S 中心看车并预约试驾。'),
         figs=[('51.87 kWh', T('LFP battery', 'Bateri LFP', '磷酸铁锂电池')), ('471 km', T('Range (CLTC)', 'Jarak (CLTC)', '续航（CLTC）')),
               ('120 kW', T('161 hp · 230 Nm', '161 hp · 230 Nm', '161 匹 · 230 牛·米')), ('500 L', T('Boot space', 'Ruang but', '后备箱容积'))],
         spec=[(T('Body', 'Badan', '车身'), T('5-seat electric SUV', 'SUV elektrik 5 tempat duduk', '5 座纯电 SUV')),
               (T('Battery', 'Bateri', '电池'), T('51.87 kWh LFP', '51.87 kWh LFP', '51.87 kWh 磷酸铁锂')),
               (T('Motor', 'Motor', '电机'), T('Single front motor, 120 kW (161 hp), 230 Nm', 'Motor tunggal hadapan, 120 kW (161 hp), 230 Nm', '单前电机，120 kW（161 匹），230 牛·米')),
               (T('0-100 km/h', '0-100 km/j', '0-100 公里/时加速'), T('9.5 seconds', '9.5 saat', '9.5 秒')),
               (T('Range', 'Jarak', '续航'), T('471 km (CLTC)', '471 km (CLTC)', '471 公里（CLTC）')),
               (T('Charging', 'Pengecasan', '充电'), T('DC up to 167 kW (30-80% in about 18 min) · AC 6.6 kW (full in about 9 h) · V2L 3.3 kW', 'DC sehingga 167 kW (30-80% kira-kira 18 min) · AC 6.6 kW (penuh kira-kira 9 jam) · V2L 3.3 kW', '直流快充最高 167 kW（30-80% 约 18 分钟）· 交流 6.6 kW（充满约 9 小时）· V2L 对外放电 3.3 kW')),
               (T('Gearbox', 'Kotak gear', '变速箱'), T('Single-ratio', 'Nisbah tunggal', '单速')),
               (T('Length x width x height', 'Panjang x lebar x tinggi', '长 x 宽 x 高'), T('4,306 x 1,868 x 1,645 mm', '4,306 x 1,868 x 1,645 mm', '4,306 x 1,868 x 1,645 毫米')),
               (T('Wheelbase', 'Jarak roda', '轴距'), T('2,715 mm', '2,715 mm', '2,715 毫米')),
               (T('Boot', 'But', '后备箱'), T('500 litres, 1,040 litres with rear seats folded; split tailgate, lower half folds into a bench (up to 150 kg)', '500 liter, 1,040 liter apabila tempat duduk belakang dilipat; pintu belakang terbelah, bahagian bawah menjadi bangku (sehingga 150 kg)', '500 升，后排放倒 1,040 升；分体式尾门，下半部可翻成长凳（承重 150 公斤）')),
               (T('Seats', 'Tempat duduk', '座椅'), T('6-way electric front seats; driver\'s seat with memory and welcome function; rear seats fold flat into a 2,000 mm bed', 'Tempat duduk hadapan elektrik 6 arah; tempat duduk pemandu dengan memori dan fungsi alu-aluan; tempat duduk belakang dilipat rata menjadi katil 2,000 mm', '6 向电动前排座椅，主驾带记忆与迎宾功能；后排放平成 2,000 毫米大床')),
               (T('Screen and audio', 'Skrin dan audio', '屏幕与音响'), T('12.8-inch centre screen, wireless Apple CarPlay, wired Android Auto, digital radio, 6 speakers', 'Skrin tengah 12.8 inci, Apple CarPlay tanpa wayar, Android Auto berwayar, radio digital, 6 pembesar suara', '12.8 英寸中控屏、无线 Apple CarPlay、有线 Android Auto、数字收音机、6 扬声器')),
               (T('Inside', 'Dalaman', '内饰'), T('Sunken centre console, 50 W wireless charger, USB-C and 12 V sockets, ambient lighting with 128-colour ripple door lamps, panoramic sunroof', 'Konsol tengah tenggelam, pengecas tanpa wayar 50 W, soket USB-C dan 12 V, lampu suasana dengan lampu pintu riak 128 warna, bumbung matahari panoramik', '下沉式中控台、50 W 无线充电、USB-C 与 12 V 接口、128 色涟漪门板氛围灯、全景天窗')),
               (T('Interior colour', 'Warna dalaman', '内饰颜色'), T('Light grey and black dual-tone vegan leather', 'Kulit vegan dua tona kelabu cerah dan hitam', '浅灰与黑色双拼素食皮革')),
               (T('Safety', 'Keselamatan', '安全'), T('6 airbags, Level 2 driver assistance (ADAS), 540-degree camera', '6 beg udara, bantuan pemandu Tahap 2 (ADAS), kamera 540 darjah', '6 气囊、L2 级驾驶辅助（ADAS）、540 度全景影像')),
               WARRANTY],
         gallery=['vigo-showroom', 'vigo-cabin', 'vigo-dash', 'pair-skyline'],
         faqs=[(T('How far can the Dongfeng Vigo go on one charge?', 'Berapa jauh Dongfeng Vigo boleh bergerak dengan satu cas?', '东风 Vigo 充满电能跑多远？'),
                T('Dongfeng quotes 471 km on the CLTC test cycle. Real driving in Johor, with highway speeds and air-con, gives less, so plan on a lower everyday figure. We can talk you through your own daily distance.',
                  'Dongfeng menyatakan 471 km pada kitaran ujian CLTC. Pemanduan sebenar di Johor, dengan kelajuan lebuh raya dan penghawa dingin, memberi jarak lebih rendah. Kami boleh bantu kira jarak harian anda.',
                  '东风公布的 CLTC 工况续航为 471 公里。在柔佛实际驾驶（高速、开冷气）会更少，日常请按较低数字规划。我们可以按您的每日里程帮您估算。')),
               (T('How many people and how much luggage fit in the Vigo?', 'Berapa ramai penumpang dan beg boleh dimuatkan dalam Vigo?', 'Vigo 能坐几人、能装多少行李？'),
                T('It seats five. The boot holds 500 litres, or 1,040 litres with the rear seats folded, and the rear seats fold flat into a 2-metre bed. Bring your stroller or golf bag to the test drive and try it.',
                  'Ia memuatkan lima orang. But 500 liter, atau 1,040 liter apabila tempat duduk belakang dilipat, dan tempat duduk belakang boleh dilipat rata menjadi katil 2 meter. Bawa stroler atau beg golf anda semasa pandu uji dan cuba sendiri.',
                  '可坐五人。后备箱 500 升，后排放倒可达 1,040 升，后排还能放平成 2 米大床。试驾时可带上婴儿车或高尔夫球包实际试放。')),
               (T('What colours does the Vigo come in?', 'Vigo ada dalam warna apa?', 'Vigo 有哪些颜色？'),
                T('Six: Mosswood Green (the launch colour), Canyon Orange, Arctic White, Sandstone Beige, Titanium Silver and Cyber Black. The cabin is light grey and black dual-tone vegan leather. WhatsApp us to see which colours are in the showroom now.',
                  'Enam: Mosswood Green (warna pelancaran), Canyon Orange, Arctic White, Sandstone Beige, Titanium Silver dan Cyber Black. Kabin berkulit vegan dua tona kelabu cerah dan hitam. WhatsApp kami untuk tahu warna yang ada di bilik pameran sekarang.',
                  '共六色：Mosswood Green 苔林绿（上市主打色）、Canyon Orange 峡谷橙、Arctic White 极地白、Sandstone Beige 砂岩米、Titanium Silver 钛银、Cyber Black 赛博黑。内饰为浅灰与黑色双拼素食皮革。WhatsApp 我们，了解展厅现有颜色。')),
               (T('What warranty does the Vigo have?', 'Apakah waranti Vigo?', 'Vigo 的保修是怎样的？'),
                T('8 years with unlimited mileage on the powertrain, and 6 years with unlimited mileage on the vehicle. Ask us for the full terms.',
                  '8 tahun tanpa had perbatuan untuk powertrain, dan 6 tahun tanpa had perbatuan untuk kenderaan. Tanya kami untuk terma penuh.',
                  '动力总成 8 年不限里程，整车 6 年不限里程。完整条款请向我们索取。')),
               (T('How much is the Dongfeng Vigo?', 'Berapakah harga Dongfeng Vigo?', '东风 Vigo 售价多少？'),
                T('Ask us on WhatsApp for the current price and any offer. We share prices directly so you get the latest figure.',
                  'Tanya kami di WhatsApp untuk harga semasa dan sebarang tawaran. Kami kongsi harga terus supaya anda dapat angka terkini.',
                  '请 WhatsApp 我们询问最新价格与优惠，我们会直接把最新报价发给您。'))]),
    dict(slug='007', name='Dongfeng 007', interior=T('Four metallic colours for both versions. Cabin: Premium in black with white contrast; Prime in black with white-contrast seats, or the Prime-only white dashboard with grey contrast. On-screen colours are a guide; see the real paint in our showroom.', 'Empat warna metalik untuk kedua-dua versi. Kabin: Premium hitam dengan kontras putih; Prime hitam dengan tempat duduk berkontras putih, atau papan pemuka putih berkontras kelabu khas Prime. Warna di skrin hanya panduan; lihat cat sebenar di bilik pameran kami.', '两个版本均有四种金属漆。内饰：Premium 为黑色配白色撞色；Prime 为黑色配白色撞色座椅，或 Prime 专属白色仪表台配灰色撞色。屏幕颜色仅供参考，实车漆面请到展厅查看。'), photo='007-showroom', card='007-studio', hero='007-hero',
         official=['007-sea', '007-studio', '007-top', '007-black', '007-life', '007-door', '007-cabin', '007-seats', '007-dash', '007-wheel', '007-seat', '007-charge', '007-boot'],
         tag=T('Electric fastback sedan', 'Sedan fastback elektrik', '纯电轿跑'),
         short=T('A long, low electric sedan with a 73.48 kWh battery, a 19-speaker WANOS system and 544 PS in the dual-motor Prime.',
                 'Sedan elektrik panjang dan rendah dengan bateri 73.48 kWh, sistem WANOS 19 pembesar suara dan 544 PS dalam Prime dua motor.',
                 '修长低趴的纯电轿跑，73.48 kWh 电池、WANOS 19 扬声器音响，双电机 Prime 达 544 匹（PS）。'),
         title=T('Dongfeng 007 Electric Sedan in Johor Bahru | Dongfeng JB',
                 'Dongfeng 007 Sedan Elektrik di Johor Bahru | Dongfeng JB',
                 '东风 007 纯电轿跑 新山 | 东风新山 3S 中心'),
         desc=T('See the Dongfeng 007 electric sedan in Johor Bahru: 73.48 kWh battery, up to 650 km (Premium), 0-100 km/h in 3.9 s (Prime). Book a test drive on WhatsApp.',
                'Lihat Dongfeng 007 sedan elektrik di Johor Bahru: bateri LFP 73.48 kWh, jarak sehingga 650 km (Premium), 0-100 km/j 3.9 s (Prime). Tempah pandu uji di WhatsApp.',
                '在新山看东风 007 纯电轿跑：73.48 kWh 磷酸铁锂电池，Premium 续航最高 650 公里，Prime 版 0-100 加速 3.9 秒。WhatsApp 预约试驾。'),
         h1=T('Dongfeng 007 electric sedan', 'Dongfeng 007 sedan elektrik', '东风 007 纯电轿跑'),
         lede=T('Sleek power in silence. Two versions: Premium with rear-wheel drive, Prime with all-wheel drive.',
                'Bergaya, berkuasa dan senyap. Dua versi: Premium pacuan roda belakang, Prime pacuan semua roda.',
                '静谧中的澎湃动力。两个版本：后驱 Premium 与四驱 Prime。'),
         answer=T('The Dongfeng 007 is an electric fastback sedan with a 73.48 kWh LFP battery and DC charging up to 200 kW. The rear-wheel-drive Premium makes 200 kW (268 hp) with up to 650 km of range (CLTC; 530 km WLTP) and 0-100 km/h in 5.8 seconds; the dual-motor Prime makes 400 kW (544 PS), goes up to 565 km (CLTC; 389 km WLTP) and does 0-100 km/h in 3.9 seconds. Both have a 19-speaker WANOS sound system and an 8-year unlimited-mileage powertrain warranty. See it at our Johor Bahru 3S centre.',
                  'Dongfeng 007 ialah sedan fastback elektrik dengan bateri LFP 73.48 kWh dan pengecasan DC sehingga 200 kW. Premium pacuan roda belakang menghasilkan 200 kW (268 hp) dengan jarak sehingga 650 km (CLTC; 530 km WLTP) dan 0-100 km/j dalam 5.8 saat; Prime dua motor menghasilkan 400 kW (544 PS), jarak sehingga 565 km (CLTC; 389 km WLTP) dan 0-100 km/j dalam 3.9 saat. Kedua-duanya ada sistem bunyi WANOS 19 pembesar suara dan waranti powertrain 8 tahun tanpa had perbatuan. Lihat sendiri di pusat 3S kami di Johor Bahru.',
                  '东风 007 是一款纯电轿跑，配备 73.48 kWh 磷酸铁锂电池，直流快充最高 200 kW。后驱 Premium 版功率 200 kW（268 匹），续航最高 650 公里（CLTC；WLTP 530 公里），0-100 公里/时加速 5.8 秒；双电机 Prime 版功率 400 kW（544 PS），续航最高 565 公里（CLTC；WLTP 389 公里），0-100 加速 3.9 秒。两版均配 WANOS 19 扬声器音响，动力总成 8 年不限里程保修。欢迎到新山东风 3S 中心看车。'),
         figs=[('73.48 kWh', T('LFP battery', 'Bateri LFP', '磷酸铁锂电池')), ('650 km', T('Range, Premium (CLTC)', 'Jarak, Premium (CLTC)', 'Premium 续航（CLTC）')),
               ('3.9 s', T('0-100 km/h, Prime', '0-100 km/j, Prime', 'Prime 0-100 加速')), ('200 kW', T('DC fast charging', 'Pengecasan pantas DC', '直流快充'))],
         spec=[(T('Body', 'Badan', '车身'), T('5-seat electric fastback sedan', 'Sedan fastback elektrik 5 tempat duduk', '5 座纯电轿跑')),
               (T('Versions', 'Versi', '版本'), T('Long Range RWD Premium (single rear motor) · AWD Prime (dual motor)', 'Long Range RWD Premium (motor tunggal belakang) · AWD Prime (dua motor)', 'Long Range RWD Premium（单后电机）· AWD Prime（双电机四驱）')),
               (T('Battery', 'Bateri', '电池'), T('73.48 kWh LFP', '73.48 kWh LFP', '73.48 kWh 磷酸铁锂')),
               (T('Power and torque', 'Kuasa dan tork', '功率与扭矩'), T('Premium 200 kW (268 hp), 310 Nm · Prime 400 kW (544 PS / 536 hp), 620 Nm', 'Premium 200 kW (268 hp), 310 Nm · Prime 400 kW (544 PS / 536 hp), 620 Nm', 'Premium 200 kW（268 匹），310 牛·米 · Prime 400 kW（544 PS / 536 hp），620 牛·米')),
               (T('0-100 km/h', '0-100 km/j', '0-100 公里/时加速'), T('Premium 5.8 s · Prime 3.9 s', 'Premium 5.8 s · Prime 3.9 s', 'Premium 5.8 秒 · Prime 3.9 秒')),
               (T('Range', 'Jarak', '续航'), T('Premium 650 km CLTC (530 km WLTP) · Prime 565 km CLTC (389 km WLTP)', 'Premium 650 km CLTC (530 km WLTP) · Prime 565 km CLTC (389 km WLTP)', 'Premium 650 公里 CLTC（WLTP 530 公里）· Prime 565 公里 CLTC（WLTP 389 公里）')),
               (T('Charging', 'Pengecasan', '充电'), T('DC up to 200 kW (30-80% in about 11 min) · AC 6.6 kW · V2L', 'DC sehingga 200 kW (30-80% kira-kira 11 min) · AC 6.6 kW · V2L', '直流快充最高 200 kW（30-80% 约 11 分钟）· 交流 6.6 kW · V2L 对外放电')),
               (T('Length x width x height', 'Panjang x lebar x tinggi', '长 x 宽 x 高'), T('4,880 x 1,895 x 1,465 mm', '4,880 x 1,895 x 1,465 mm', '4,880 x 1,895 x 1,465 毫米')),
               (T('Wheelbase', 'Jarak roda', '轴距'), T('2,915 mm', '2,915 mm', '2,915 毫米')),
               (T('Boot', 'But', '后备箱'), T('452 litres, 1,026 litres with rear seats folded; boot lid opens with the rear window', '452 liter, 1,026 liter apabila tempat duduk belakang dilipat; penutup but dibuka bersama cermin belakang', '452 升，后排放倒 1,026 升；尾门连同后挡风玻璃一起开启')),
               (T('Wheels', 'Rim', '轮毂'), T('18-inch (Premium), 19-inch with performance calipers (Prime)', '18 inci (Premium), 19 inci dengan kaliper prestasi (Prime)', '18 英寸（Premium），19 英寸配性能卡钳（Prime）')),
               (T('Inside', 'Dalaman', '内饰'), T('15.6-inch centre screen, 8.8-inch driver display, WANOS 19-speaker system with headrest speakers, panoramic glass roof, wireless charger, ambient lighting', 'Skrin tengah 15.6 inci, paparan pemandu 8.8 inci, sistem WANOS 19 pembesar suara termasuk pembesar suara di sandaran kepala, bumbung kaca panoramik, pengecas tanpa wayar, lampu suasana', '15.6 英寸中控屏、8.8 英寸液晶仪表、WANOS 19 扬声器音响（含头枕扬声器）、全景玻璃车顶、无线充电、氛围灯')),
               (T('Interior colour', 'Warna dalaman', '内饰颜色'), T('Premium: black with white contrast · Prime: black dashboard with white-contrast faux-leather seats, or the Prime-only white dashboard with grey contrast', 'Premium: hitam dengan kontras putih · Prime: papan pemuka hitam dengan tempat duduk kulit tiruan berkontras putih, atau papan pemuka putih berkontras kelabu khas Prime', 'Premium：黑色配白色撞色 · Prime：黑色仪表台配白色撞色仿皮座椅，或 Prime 专属白色仪表台配灰色撞色')),
               (T('Safety', 'Keselamatan', '安全'), T('6 airbags, Level 2 driver assistance (ADAS)', '6 beg udara, bantuan pemandu Tahap 2 (ADAS)', '6 气囊、L2 级驾驶辅助（ADAS）')),
               WARRANTY],
         gallery=['007-showroom', 'cabin-quilted', 'pair-skyline'],
         faqs=[(T('What is the difference between the 007 Premium and 007 Prime?', 'Apakah beza 007 Premium dan 007 Prime?', '007 Premium 和 Prime 有什么区别？'),
                T('Premium has one rear motor (200 kW, 268 hp) and the longer range, up to 650 km. Prime has two motors and all-wheel drive, 400 kW (544 PS), 0-100 km/h in 3.9 seconds and up to 565 km (CLTC), plus 19-inch wheels with performance calipers and an optional white dashboard.',
                  'Premium mempunyai satu motor belakang (200 kW, 268 hp) dan jarak lebih jauh, sehingga 650 km. Prime mempunyai dua motor dan pacuan semua roda, 400 kW (544 PS), 0-100 km/j dalam 3.9 saat dan jarak sehingga 565 km (CLTC), serta rim 19 inci dengan kaliper prestasi dan pilihan papan pemuka putih.',
                  'Premium 为单后电机（200 kW，268 匹），续航更长，最高 650 公里。Prime 为双电机四驱，400 kW（544 PS），0-100 加速 3.9 秒，续航最高 565 公里（CLTC），并配 19 英寸轮毂、性能卡钳及可选白色仪表台。')),
               (T('How fast does the Dongfeng 007 charge?', 'Berapa pantas Dongfeng 007 dicas?', '东风 007 充电有多快？'),
                T('It accepts DC fast charging up to 200 kW and AC charging at 6.6 kW. Actual charging time depends on the charger, the battery temperature and how full the battery is.',
                  'Ia menerima pengecasan pantas DC sehingga 200 kW dan pengecasan AC 6.6 kW. Masa sebenar bergantung pada pengecas, suhu bateri dan tahap cas.',
                  '支持最高 200 kW 直流快充和 6.6 kW 交流慢充。实际充电时间取决于充电桩、电池温度与剩余电量。')),
               (T('What colours does the 007 come in?', '007 ada dalam warna apa?', '007 有哪些颜色？'),
                T('Four, for both versions: Celestial White Metallic, Eclipse Grey Metallic, Obsidian Black Metallic and Starlit Silver Metallic. WhatsApp us to see which colours are in the showroom now.',
                  'Empat, untuk kedua-dua versi: Celestial White Metallic, Eclipse Grey Metallic, Obsidian Black Metallic dan Starlit Silver Metallic. WhatsApp kami untuk tahu warna yang ada di bilik pameran sekarang.',
                  '两个版本均有四色：Celestial White 星云白金属漆、Eclipse Grey 日蚀灰金属漆、Obsidian Black 曜石黑金属漆、Starlit Silver 星光银金属漆。WhatsApp 我们，了解展厅现有颜色。')),
               (T('What warranty does the 007 have?', 'Apakah waranti 007?', '007 的保修是怎样的？'),
                T('8 years with unlimited mileage on the powertrain, and 6 years with unlimited mileage on the vehicle, for both Premium and Prime. Ask us for the full terms.',
                  '8 tahun tanpa had perbatuan untuk powertrain, dan 6 tahun tanpa had perbatuan untuk kenderaan, bagi Premium dan Prime. Tanya kami untuk terma penuh.',
                  'Premium 与 Prime 均为动力总成 8 年不限里程、整车 6 年不限里程保修。完整条款请向我们索取。')),
               (T('How much is the Dongfeng 007?', 'Berapakah harga Dongfeng 007?', '东风 007 售价多少？'),
                T('Ask us on WhatsApp for the current price of each version and any offer. We share prices directly so you get the latest figure.',
                  'Tanya kami di WhatsApp untuk harga semasa setiap versi dan sebarang tawaran. Kami kongsi harga terus supaya anda dapat angka terkini.',
                  '请 WhatsApp 我们询问各版本最新价格与优惠，我们会直接发给您最新报价。'))]),
]
MOD = {m['slug']: m for m in MODELS}

# Coming soon (Edwin, 19 Oct 2026: "Only add Voyah Dream as upcoming"). Facts only from Dongfeng Malaysia's KLIMS 2026 preview
# (paultan.org, 19 Jun 2026). No Malaysian specs, price or launch date published until the client confirms them.
VOYAH = dict(slug='voyah-dream', name='Voyah Dream', card='voyah-side', hero='voyah-side', gallery=['voyah-side', 'voyah-door', 'voyah-rear'],
    tag=T('Luxury MPV · Coming soon', 'MPV mewah · Akan datang', '豪华 MPV · 即将上市'),
    short=T('The luxury MPV from Voyah, Dongfeng\'s premium brand. Coming to Johor: register your interest.', 'MPV mewah daripada Voyah, jenama premium Dongfeng. Akan tiba di Johor: daftar minat anda.', '东风旗下高端品牌岚图的豪华 MPV，即将登陆柔佛，欢迎登记意向。'),
    title=T('Voyah Dream Luxury MPV, Coming to Johor Bahru | Dongfeng JB', 'Voyah Dream MPV Mewah, Akan Tiba di JB | Dongfeng Johor', '岚图梦想家 Voyah Dream 豪华 MPV 即将登陆新山 | 东风新山'),
    desc=T('The Voyah Dream luxury MPV from Dongfeng\'s premium brand is coming to Johor Bahru. Register your interest on WhatsApp for first news on launch and test drives.',
           'MPV mewah Voyah Dream daripada jenama premium Dongfeng akan tiba di Johor Bahru. Daftar minat di WhatsApp untuk berita pertama pelancaran dan pandu uji.',
           '东风旗下高端品牌岚图的梦想家 Voyah Dream 豪华 MPV 即将登陆新山。WhatsApp 登记意向，第一时间获知上市与试驾消息。'),
    h1=T('Voyah Dream: coming soon to Johor', 'Voyah Dream: akan tiba di Johor', '岚图梦想家：即将登陆柔佛'),
    lede=T('A luxury MPV from Dongfeng\'s premium brand. Be the first to see it in Johor Bahru.', 'MPV mewah daripada jenama premium Dongfeng. Jadi yang pertama melihatnya di Johor Bahru.', '东风高端品牌的豪华 MPV，抢先在新山一睹真容。'),
    answer=T('The Voyah Dream is a luxury MPV from Voyah, Dongfeng\'s premium brand. Dongfeng Malaysia previewed it at the Kuala Lumpur International Mobility Show (KLIMS) in June 2026 as a seven-seater. It is not on sale in Malaysia yet; the Malaysian version, specifications, price and launch date have not been announced. Register your interest with us and we will tell you first.',
             'Voyah Dream ialah MPV mewah daripada Voyah, jenama premium Dongfeng. Dongfeng Malaysia mempamerkannya di Kuala Lumpur International Mobility Show (KLIMS) pada Jun 2026 sebagai model tujuh tempat duduk. Ia belum dijual di Malaysia; versi Malaysia, spesifikasi, harga dan tarikh pelancaran belum diumumkan. Daftar minat dengan kami dan kami akan maklumkan anda dahulu.',
             '岚图梦想家（Voyah Dream）是东风旗下高端品牌岚图推出的豪华 MPV。东风马来西亚已于 2026 年 6 月在吉隆坡国际移动出行展（KLIMS）上以七座版本进行预览。目前尚未在马来西亚开售，马来西亚版本、规格、价格与上市日期均未公布。欢迎向我们登记意向，我们会第一时间通知您。'),
    facts=[(T('Brand', 'Jenama', '品牌'), T('Voyah, Dongfeng\'s luxury brand', 'Voyah, jenama mewah Dongfeng', '岚图（Voyah），东风旗下高端品牌')),
           (T('Body', 'Badan', '车身'), T('Luxury MPV; shown in Malaysia as a seven-seater', 'MPV mewah; dipamerkan di Malaysia sebagai tujuh tempat duduk', '豪华 MPV；在马来西亚以七座版本亮相')),
           (T('Shown in Malaysia', 'Dipamerkan di Malaysia', '马来西亚亮相'), T('KLIMS 2026, Kuala Lumpur, June 2026 (preview by Dongfeng Malaysia)', 'KLIMS 2026, Kuala Lumpur, Jun 2026 (pratonton oleh Dongfeng Malaysia)', '2026 年 6 月吉隆坡 KLIMS 2026（东风马来西亚预览）')),
           (T('Malaysian specs, price, launch date', 'Spesifikasi, harga, tarikh pelancaran Malaysia', '马来西亚规格、价格、上市日期'), T('Not announced yet', 'Belum diumumkan', '尚未公布'))],
    faqs=[(T('When is the Voyah Dream coming to Johor?', 'Bilakah Voyah Dream akan tiba di Johor?', '岚图梦想家什么时候到柔佛？'),
           T('The launch date has not been announced. Register your interest on WhatsApp and we will tell you as soon as it is confirmed.', 'Tarikh pelancaran belum diumumkan. Daftar minat di WhatsApp dan kami akan maklumkan sebaik sahaja disahkan.', '上市日期尚未公布。WhatsApp 登记意向，一经确认我们马上通知您。')),
          (T('Is the Voyah Dream electric or a plug-in hybrid?', 'Adakah Voyah Dream elektrik atau hibrid palam masuk?', '岚图梦想家是纯电还是插电混动？'),
           T('The car Dongfeng Malaysia showed at KLIMS 2026 was a plug-in hybrid. Which versions Malaysia gets has not been confirmed; we will update this page when it is.', 'Kereta yang dipamerkan Dongfeng Malaysia di KLIMS 2026 ialah hibrid palam masuk. Versi untuk Malaysia belum disahkan; kami akan kemas kini halaman ini.', '东风马来西亚在 KLIMS 2026 展出的是插电混动版。马来西亚引进哪些版本尚未确认，确认后我们会更新本页。')),
          (T('How much will the Voyah Dream cost?', 'Berapakah harga Voyah Dream?', '岚图梦想家售价多少？'),
           T('The price has not been announced. Register your interest and we will send it to you when it is out.', 'Harga belum diumumkan. Daftar minat dan kami akan hantar harga apabila keluar.', '价格尚未公布。登记意向后，公布时我们会第一时间发给您。'))])

# ---------------------------------------------------------------------------------------------
# Articles
# ---------------------------------------------------------------------------------------------
ARTICLES = [
    dict(slug='what-is-a-3s-car-centre', photo='showroom-front', owner='service/',
         title=T('What Is a 3S Car Centre? Sales, Service, Spare Parts', 'Apa Itu Pusat Kereta 3S? Jualan, Servis, Alat Ganti', '什么是汽车 3S 中心？销售、服务、配件一站式'),
         h1=T('What is a 3S car centre?', 'Apa itu pusat kereta 3S?', '什么是汽车 3S 中心？'),
         desc=T('A 3S centre puts sales, service and spare parts for one brand under one roof. What that means when you buy an EV in Johor Bahru.',
                'Pusat 3S menggabungkan jualan, servis dan alat ganti satu jenama di satu tempat. Apa maksudnya apabila anda membeli EV di Johor Bahru.',
                '3S 中心把同一品牌的销售、售后服务和零配件集中在一处。在新山买电动车时，这意味着什么？'),
         answer=T('A 3S centre is a car dealership that handles three things for one brand in one place: Sales, Service and Spare parts. You buy the car, bring it back for servicing and get genuine parts from the same team, so the people who sold you the car are the ones who look after it.',
                  'Pusat 3S ialah pengedar kereta yang mengendalikan tiga perkara untuk satu jenama di satu tempat: Sales (jualan), Service (servis) dan Spare parts (alat ganti). Anda beli kereta, hantar servis dan dapatkan alat ganti tulen daripada pasukan yang sama.',
                  '3S 中心是在同一地点为同一品牌提供三项服务的汽车经销店：销售（Sales）、售后服务（Service）和零配件（Spare parts）。买车、保养、换原厂配件都找同一个团队，卖车的人就是照顾您爱车的人。'),
         sections=[(T('Why it matters more for an electric car', 'Mengapa ia lebih penting untuk kereta elektrik', '为什么对电动车更重要'),
                    T('An EV has a high-voltage battery, an electric motor and software that a general workshop may not be set up for. A brand 3S centre is where the brand\'s own diagnostic tools and parts supply are meant to be, which makes routine checks and warranty matters simpler.',
                      'EV mempunyai bateri voltan tinggi, motor elektrik dan perisian yang mungkin tidak dapat dikendalikan bengkel biasa. Pusat 3S jenama ialah tempat alat diagnostik dan bekalan alat ganti jenama itu sendiri, jadi pemeriksaan rutin dan urusan waranti lebih mudah.',
                      '电动车有高压电池、电机和软件系统，一般修车厂未必具备相应设备。品牌 3S 中心配有品牌自己的诊断工具和配件渠道，日常检查与保修事宜都更省心。')),
                   (T('3S, 4S: what is the difference?', '3S, 4S: apa bezanya?', '3S 和 4S 有什么不同？'),
                    T('A 4S centre adds a fourth S, usually Survey (customer feedback). In practice, what you want to know is simple: can you buy, service and get parts for your car at the same address? At a 3S centre the answer is yes.',
                      'Pusat 4S menambah S keempat, biasanya Survey (maklum balas pelanggan). Hakikatnya, soalan anda mudah: bolehkah anda beli, servis dan dapatkan alat ganti di alamat yang sama? Di pusat 3S, jawapannya ya.',
                      '4S 店多了第四个 S，通常指信息反馈（Survey）。对车主来说，关键问题很简单：能不能在同一个地方买车、保养、拿配件？3S 中心的答案是可以。')),
                   (T('Dongfeng\'s 3S centre in Johor', 'Pusat 3S Dongfeng di Johor', '柔佛的东风 3S 中心'),
                    T('Our showroom at No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru is Johor\'s Dongfeng 3S centre for passenger EVs: the Dongfeng Vigo and Dongfeng 007. WhatsApp us to book a test drive or a service visit.',
                      'Bilik pameran kami di No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru ialah pusat 3S Dongfeng di Johor untuk kereta penumpang elektrik: Dongfeng Vigo dan Dongfeng 007. WhatsApp kami untuk tempah pandu uji atau servis.',
                      '我们位于81100 新山 Taman Ekoperniagaan, Jalan Ekoperniagaan 3/11 门牌 28 号的展厅，就是柔佛的东风纯电乘用车 3S 中心，主营东风 Vigo 和东风 007。WhatsApp 我们预约试驾或保养。'))],
         faqs=[(T('Does 3S mean the centre also repairs the car?', 'Adakah 3S bermaksud pusat itu juga membaiki kereta?', '3S 中心也负责维修吗？'),
                T('Yes, the second S is Service, which covers servicing and repairs for the brand\'s cars. Ask the centre which jobs it handles on site.',
                  'Ya, S kedua ialah Service, termasuk servis dan pembaikan kereta jenama itu. Tanya pusat tersebut kerja apa yang dibuat di premis.',
                  '是的，第二个 S 就是售后服务，包括该品牌车辆的保养和维修。具体能做哪些项目，可直接询问门店。'))]),
    dict(slug='dongfeng-vigo-vs-007', photo='pair-skyline', owner='models/',
         title=T('Dongfeng Vigo vs 007: Which EV Suits You?', 'Dongfeng Vigo vs 007: EV Mana Sesuai?', '东风 Vigo 和 007 怎么选？'),
         h1=T('Dongfeng Vigo or Dongfeng 007: which one suits you?', 'Dongfeng Vigo atau Dongfeng 007: mana sesuai untuk anda?', '东风 Vigo 还是东风 007：哪款更适合您？'),
         desc=T('Vigo is the practical family SUV; 007 is the long-range, faster sedan. A side-by-side of size, battery, range and space, with the Malaysian figures.',
                'Vigo ialah SUV keluarga yang praktikal; 007 ialah sedan yang lebih laju dan jauh. Perbandingan saiz, bateri, jarak dan ruang, dengan angka Malaysia.',
                'Vigo 是实用的家庭 SUV，007 是续航更长、更快的轿跑。按马来西亚规格对比尺寸、电池、续航和空间。'),
         answer=T('Choose the Dongfeng Vigo if you want a higher seat, a 500-litre boot and an easy family SUV. Choose the Dongfeng 007 if you drive long distances or want more performance: its 73.48 kWh battery gives up to 650 km in the Premium, and the Prime does 0-100 km/h in 3.9 seconds.',
                  'Pilih Dongfeng Vigo jika anda mahu kedudukan duduk lebih tinggi, but 500 liter dan SUV keluarga yang mudah. Pilih Dongfeng 007 jika anda kerap memandu jauh atau mahu prestasi lebih: bateri 73.48 kWh memberi sehingga 650 km bagi Premium, dan Prime 0-100 km/j dalam 3.9 saat.',
                  '想要更高坐姿、500 升后备箱和好开的家庭 SUV，选东风 Vigo。常跑长途或追求性能，选东风 007：73.48 kWh 电池让 Premium 版续航最高 650 公里，Prime 版 0-100 加速仅 3.9 秒。'),
         sections=[(T('Side by side', 'Perbandingan', '数据对比'), None),
                   (T('Who usually picks which', 'Siapa biasanya pilih yang mana', '一般谁选哪款'),
                    T('Families who do school runs and weekend trips around Johor often like the Vigo for its height, boot and split tailgate. Drivers who cover long distances, or simply want a quiet, fast sedan, lean to the 007. The best way to decide is to drive both back to back: WhatsApp us and we will line them up.',
                      'Keluarga yang menghantar anak ke sekolah dan berjalan hujung minggu di sekitar Johor biasanya suka Vigo kerana ketinggian, but dan pintu belakang terbelah dua. Pemandu yang kerap memandu jauh, atau mahu sedan senyap dan laju, lebih cenderung kepada 007. Cara terbaik ialah pandu kedua-duanya: WhatsApp kami dan kami sediakan.',
                      '每天接送孩子、周末在柔佛周边游玩的家庭，通常喜欢 Vigo 的高度、后备箱和分体尾门。常跑长途、或想要安静又快的轿跑的车主，更倾向 007。最好的办法是两款都试：WhatsApp 我们，我们帮您安排连试。'))],
         faqs=[(T('Which is bigger, the Vigo or the 007?', 'Mana lebih besar, Vigo atau 007?', 'Vigo 和 007 哪个更大？'),
                T('The 007 is longer (4,880 mm vs 4,306 mm) with a longer wheelbase, but the Vigo is taller (1,645 mm vs 1,465 mm) and has the bigger boot (500 L vs 452 L).',
                  '007 lebih panjang (4,880 mm berbanding 4,306 mm) dengan jarak roda lebih panjang, tetapi Vigo lebih tinggi (1,645 mm berbanding 1,465 mm) dan butnya lebih besar (500 L berbanding 452 L).',
                  '007 更长（4,880 毫米对 4,306 毫米），轴距也更长；但 Vigo 更高（1,645 毫米对 1,465 毫米），后备箱也更大（500 升对 452 升）。'))]),
    dict(slug='ev-test-drive-checklist', photo='vigo-cabin', owner='test-drive/',
         title=T('EV Test Drive in Johor Bahru: What to Check', 'Pandu Uji EV di Johor Bahru: Apa Perlu Diperiksa', '新山电动车试驾：要注意什么'),
         h1=T('Your first EV test drive in Johor Bahru: what to check', 'Pandu uji EV pertama anda di Johor Bahru: apa perlu diperiksa', '在新山第一次试驾电动车：该看什么'),
         desc=T('A short checklist for an electric car test drive: driving position, one-pedal feel, cabin noise, screens, charging and the questions to ask.',
                'Senarai semak ringkas untuk pandu uji kereta elektrik: kedudukan memandu, rasa pedal tunggal, bunyi kabin, skrin, pengecasan dan soalan untuk ditanya.',
                '电动车试驾简明清单：驾驶姿势、单踏板感受、车内噪音、屏幕操作、充电方式，以及该问的问题。'),
         answer=T('On an EV test drive, check four things: how the car pulls away and slows when you lift off (regenerative braking), how quiet the cabin is at speed, whether the screens and phone connection are easy for you, and how you would charge it at home or near work. Book a slot on WhatsApp so the car is charged and ready.',
                  'Semasa pandu uji EV, periksa empat perkara: bagaimana kereta bergerak dan memperlahan apabila anda lepas pedal (brek regeneratif), betapa senyap kabin pada kelajuan tinggi, sama ada skrin dan sambungan telefon mudah digunakan, dan bagaimana anda akan mengecas di rumah atau berhampiran tempat kerja. Tempah slot di WhatsApp supaya kereta sudah dicas dan sedia.',
                  '试驾电动车时看四点：起步和松开电门时的减速（动能回收）感受、高速时车内是否安静、屏幕和手机互联是否顺手，以及您在家或公司附近如何充电。请先 WhatsApp 预约，我们会把车充好电等您。'),
         sections=[(T('Before you come', 'Sebelum datang', '出发前'),
                    T('Bring your driving licence. Think about your usual week: daily distance, where you park at night and whether you can fit a home charger. Those three answers decide which model and which charging plan suit you.',
                      'Bawa lesen memandu anda. Fikirkan minggu biasa anda: jarak harian, tempat letak kereta waktu malam dan sama ada anda boleh pasang pengecas di rumah. Tiga jawapan itu menentukan model dan pelan pengecasan yang sesuai.',
                      '请带上驾照。想一想您平常的一周：每天开多远、晚上停在哪、家里能不能装充电桩。这三点决定哪款车、哪种充电方式适合您。')),
                   (T('On the drive', 'Semasa memandu', '试驾中'),
                    T('Try a stretch at highway speed, a U-turn and parking. Feel the regenerative braking, switch drive modes, and test the camera views when reversing. Sit in the back seat too.',
                      'Cuba pandu pada kelajuan lebuh raya, buat pusingan U dan letak kereta. Rasai brek regeneratif, tukar mod pemanduan dan uji paparan kamera semasa mengundur. Duduk di tempat duduk belakang juga.',
                      '试一段高速、一次掉头和一次停车。感受动能回收，切换驾驶模式，倒车时看看影像效果。也到后排坐一坐。')),
                   (T('Questions to ask us', 'Soalan untuk ditanya', '可以问我们的问题'),
                    T('Ask about warranty terms, service at our 3S centre, home charger installation, delivery time and the current price. We answer on the spot or on WhatsApp.',
                      'Tanya tentang terma waranti, servis di pusat 3S kami, pemasangan pengecas di rumah, masa penghantaran dan harga semasa. Kami jawab terus atau melalui WhatsApp.',
                      '可以问保修条款、在 3S 中心的保养、家用充电桩安装、交车时间和最新价格。我们会当场或在 WhatsApp 上回答。'))],
         faqs=[(T('Do I need an appointment for a test drive?', 'Perlukah temujanji untuk pandu uji?', '试驾需要预约吗？'),
                T('Yes, please WhatsApp us first so the model you want is charged and free at your time.',
                  'Ya, sila WhatsApp kami dahulu supaya model yang anda mahu sudah dicas dan tersedia pada masa anda.',
                  '需要，请先 WhatsApp 我们，确保您想试的车型在约定时间已充好电、可以试驾。'))]),
    dict(slug='charging-an-ev-at-home-in-johor', photo='vigo-dash', owner='models/',
         title=T('Charging an EV at Home in Johor: The Basics', 'Mengecas EV di Rumah di Johor: Asas', '在柔佛家里给电动车充电：基础知识'),
         h1=T('Charging an EV at home in Johor: the basics', 'Mengecas EV di rumah di Johor: asas', '在柔佛家里给电动车充电：基础知识'),
         desc=T('AC wall box or public DC charger? How long a full charge takes at 6.6 kW, what to check before installing, and how to plan charging around Johor.',
                'Pengecas dinding AC atau pengecas awam DC? Berapa lama cas penuh pada 6.6 kW, apa perlu diperiksa sebelum pasang, dan cara merancang pengecasan di Johor.',
                '家用交流壁挂充电盒还是公共直流快充？6.6 kW 充满要多久、安装前要检查什么，以及在柔佛如何规划充电。'),
         answer=T('Most EV owners charge at home overnight on an AC wall box and use DC fast chargers on longer trips. Both the Dongfeng Vigo and 007 take AC charging at up to 6.6 kW, so a near-empty Vigo battery (51.87 kWh) needs about 9 hours on a 6.6 kW wall box. Have a licensed electrician check your home wiring before installing one.',
                  'Kebanyakan pemilik EV mengecas di rumah pada waktu malam menggunakan pengecas dinding AC dan menggunakan pengecas pantas DC untuk perjalanan jauh. Dongfeng Vigo dan 007 menerima pengecasan AC sehingga 6.6 kW, jadi bateri Vigo (51.87 kWh) yang hampir kosong memerlukan kira-kira 9 jam pada pengecas dinding 6.6 kW. Minta juruelektrik berlesen periksa pendawaian rumah sebelum pemasangan.',
                  '大多数电动车车主晚上在家用交流壁挂充电盒充电，长途时再用直流快充。东风 Vigo 和 007 的交流充电功率最高 6.6 kW，因此 Vigo 的 51.87 kWh 电池从接近没电充满，在 6.6 kW 壁挂充电盒上大约需要 9 小时。安装前请让持证电工检查家中线路。'),
         sections=[(T('AC at home, DC on the road', 'AC di rumah, DC di jalan', '在家用交流，出门用直流'),
                    T('AC charging is slower and gentle, ideal overnight. DC fast charging is for when you need range quickly: the Vigo accepts up to 167 kW and the 007 up to 200 kW, though the speed you actually get depends on the charger and the battery\'s state.',
                      'Pengecasan AC lebih perlahan dan sesuai waktu malam. Pengecasan pantas DC untuk bila anda perlukan jarak dengan cepat: Vigo menerima sehingga 167 kW dan 007 sehingga 200 kW, walaupun kelajuan sebenar bergantung pada pengecas dan keadaan bateri.',
                      '交流充电较慢、对电池温和，适合夜间。直流快充用于急需补电时：Vigo 最高 167 kW，007 最高 200 kW，实际速度取决于充电桩和电池状态。')),
                   (T('Before you install a wall box', 'Sebelum pasang pengecas dinding', '安装壁挂充电盒之前'),
                    None)],
         install=[T('Ask a licensed electrician to check your main switchboard and wiring.', 'Minta juruelektrik berlesen periksa papan suis utama dan pendawaian.', '请持证电工检查家中总电箱与线路。'),
                  T('Choose a spot near where you park, sheltered from rain if possible.', 'Pilih lokasi berhampiran tempat letak kereta, terlindung daripada hujan jika boleh.', '选在停车位附近，尽量能遮雨。'),
                  T('For condos and landed homes in a managed estate, check the management\'s rules first.', 'Bagi kondominium dan rumah dalam kawasan berpengurusan, semak peraturan pihak pengurusan dahulu.', '公寓或有管理的住宅区，请先向管理处确认规定。'),
                  T('Ask us about the charger that comes with your car and its installation.', 'Tanya kami tentang pengecas yang disertakan dengan kereta dan pemasangannya.', '可以问我们随车充电设备及安装事宜。')],
         faqs=[(T('Can I charge an EV from a normal three-pin socket?', 'Bolehkah saya cas EV dari soket tiga pin biasa?', '能用普通三脚插座给电动车充电吗？'),
                T('It is very slow and puts a long load on household wiring, so it is only a stop-gap. A proper wall box, installed by a licensed electrician, is the safer everyday choice.',
                  'Ia sangat perlahan dan membebankan pendawaian rumah untuk masa yang lama, jadi hanya sebagai sementara. Pengecas dinding yang dipasang oleh juruelektrik berlesen ialah pilihan harian yang lebih selamat.',
                  '速度很慢，而且长时间加重家庭线路负荷，只适合临时应急。由持证电工安装的壁挂充电盒才是更安全的日常选择。'))]),
    # Daily article 21 Oct 2026 (catch-up for the missed odd day; queue #1, LOW risk: no prices, no range/charging claims, service interval = Gavin's sheet).
    dict(slug='ev-maintenance-in-malaysia', photo='vigo-rims', owner='service/', date='2026-10-21',
         title=T('EV Maintenance in Malaysia: What Owners Should Know', 'Penyelenggaraan EV di Malaysia: Apa Pemilik Perlu Tahu', '马来西亚电动车保养：车主须知'),
         h1=T('EV maintenance in Malaysia: what owners should know', 'Penyelenggaraan EV di Malaysia: apa pemilik perlu tahu', '马来西亚电动车保养：车主须知'),
         desc=T('What an electric car no longer needs, what still needs regular attention in Malaysian heat and rain, and why high-voltage work belongs to trained technicians.',
                'Apa yang tidak lagi diperlukan kereta elektrik, apa yang masih perlu diberi perhatian dalam cuaca panas dan hujan Malaysia, dan mengapa kerja voltan tinggi untuk juruteknik terlatih.',
                '电动车不再需要保养什么、在马来西亚的炎热与多雨天气下还要关注什么，以及为什么高压系统要交给受过培训的技师。'),
         answer=T('An EV needs less routine maintenance than a petrol car because it has no engine oil, spark plugs or exhaust, but it still needs regular servicing. Tyres, brakes, brake fluid, the cabin air filter, coolant circuits, the 12V battery, suspension and software checks all matter, and the high-voltage system should only be handled by trained technicians. At Dongfeng Johor Bahru, scheduled service is every 10,000 km.',
                  'EV memerlukan penyelenggaraan rutin yang lebih sedikit berbanding kereta petrol kerana tiada minyak enjin, palam pencucuh atau ekzos, tetapi ia masih perlu diservis secara berkala. Tayar, brek, minyak brek, penapis udara kabin, litar penyejuk, bateri 12V, suspensyen dan semakan perisian semuanya penting, dan sistem voltan tinggi hanya boleh dikendalikan oleh juruteknik terlatih. Di Dongfeng Johor Bahru, servis berjadual dibuat setiap 10,000 km.',
                  '电动车的日常保养比燃油车少，因为没有机油、火花塞和排气系统，但仍然需要定期保养。轮胎、刹车、刹车油、空调滤芯、冷却回路、12V 电瓶、悬挂和软件检查都很重要，高压系统只能由受过培训的技师处理。东风新山的定期保养为每 10,000 公里一次。'),
         sections=[(T('What you no longer need to do', 'Apa yang tidak lagi perlu dibuat', '不再需要做的保养'),
                    T('A battery electric car has no engine, so there are no engine oil changes, spark plugs, timing belt or exhaust to look after. That is the main reason routine upkeep is simpler than on a petrol car.',
                      'Kereta elektrik bateri tiada enjin, jadi tiada tukar minyak enjin, palam pencucuh, tali sesondol atau ekzos untuk dijaga. Itulah sebab utama penyelenggaraan rutin lebih mudah berbanding kereta petrol.',
                      '纯电动车没有发动机，所以不用换机油，也没有火花塞、正时皮带和排气管需要照顾。这是日常保养比燃油车简单的主要原因。')),
                   (T('What still needs regular attention', 'Apa yang masih perlu diberi perhatian', '仍需定期关注的项目'), None),
                   (T('Software and health checks', 'Semakan perisian dan kesihatan kereta', '软件与状态检查'),
                    T('Modern EVs run on software. At a service, the technician can read the car\'s fault records, check for available software updates and look over the charging port and cables. Ask the centre what is included in your service visit.',
                      'EV moden bergantung pada perisian. Semasa servis, juruteknik boleh membaca rekod kerosakan kereta, menyemak kemas kini perisian yang ada dan memeriksa port pengecasan serta kabel. Tanya pusat servis apa yang termasuk dalam lawatan servis anda.',
                      '现代电动车依靠软件运行。保养时，技师可以读取车辆的故障记录、查看是否有可用的软件更新，并检查充电口和线束。请向服务中心确认保养项目包含哪些内容。')),
                   (T('Leave the high-voltage system to trained technicians', 'Serahkan sistem voltan tinggi kepada juruteknik terlatih', '高压系统交给受过培训的技师'),
                    T('An EV\'s battery and the orange high-voltage cables carry dangerous voltage. Do not open, test or repair them yourself, and do not let an untrained workshop do it. If a warning light comes on, stop safely and contact a service centre.',
                      'Bateri EV dan kabel voltan tinggi berwarna oren membawa voltan yang bahaya. Jangan buka, uji atau baiki sendiri, dan jangan benarkan bengkel yang tidak terlatih melakukannya. Jika lampu amaran menyala, berhenti dengan selamat dan hubungi pusat servis.',
                      '电动车的电池和橙色高压线束带有危险电压。请不要自行拆开、检测或维修，也不要交给未受过培训的修车厂。如果仪表出现警告灯，请安全停车并联系服务中心。')),
                   (T('Servicing at our 3S centre in Johor Bahru', 'Servis di pusat 3S kami di Johor Bahru', '在新山 3S 中心保养'),
                    T('Our scheduled service for the Dongfeng Vigo and Dongfeng 007 is every 10,000 km, with service and parts at Dongfeng\'s list prices. WhatsApp us your model and mileage to book, and keep your service record: the warranty terms are on the Vigo and 007 pages.',
                      'Servis berjadual kami untuk Dongfeng Vigo dan Dongfeng 007 ialah setiap 10,000 km, dengan servis dan alat ganti mengikut harga senarai Dongfeng. WhatsApp kami model dan jarak perjalanan anda untuk menempah, dan simpan rekod servis anda: terma waranti ada di halaman Vigo dan 007.',
                      '东风 Vigo 和东风 007 的定期保养为每 10,000 公里一次，保养与配件按东风官方价目表收费。请 WhatsApp 告诉我们车型和里程来预约，并保存好保养记录：保修条款请见 Vigo 和 007 车型页面。'))],
         checks=[T('Tyres: check pressure often, and ask about rotation and alignment. EVs are heavy and deliver torque instantly, which can wear tyres faster.', 'Tayar: semak tekanan kerap, dan tanya tentang putaran dan penjajaran. EV berat dan menghantar tork serta-merta, yang boleh menyebabkan tayar haus lebih cepat.', '轮胎：经常检查胎压，并询问是否需要换位和四轮定位。电动车较重且扭矩瞬间输出，轮胎磨损可能更快。'),
                 T('Brakes: regenerative braking saves the pads, but discs that are rarely used can rust in humid weather, and brake fluid ages over time.', 'Brek: brek regeneratif menjimatkan pad, tetapi cakera yang jarang digunakan boleh berkarat dalam cuaca lembap, dan minyak brek merosot mengikut masa.', '刹车：动能回收能减少刹车片磨损，但很少使用的刹车盘在潮湿天气下可能生锈，刹车油也会随时间老化。'),
                 T('Cabin air filter and aircon: hot, humid Malaysian weather keeps the aircon working hard, so filters and vents need regular attention.', 'Penapis udara kabin dan penyaman udara: cuaca Malaysia yang panas dan lembap membuatkan penyaman udara bekerja keras, jadi penapis dan salur udara perlu diberi perhatian berkala.', '空调滤芯与空调：马来西亚炎热潮湿，空调常年高负荷运行，滤芯和出风口需要定期留意。'),
                 T('Coolant: the battery and motor have their own cooling circuits, checked and changed as the service schedule says.', 'Penyejuk: bateri dan motor mempunyai litar penyejuk sendiri, diperiksa dan ditukar mengikut jadual servis.', '冷却液：电池和电机都有各自的冷却回路，按保养计划检查和更换。'),
                 T('12V battery, wipers, lights and suspension: still there, still wear, still checked at every service.', 'Bateri 12V, pengelap, lampu dan suspensyen: masih ada, masih haus, dan masih diperiksa pada setiap servis.', '12V 电瓶、雨刷、灯光和悬挂：依然存在，依然会磨损，每次保养都要检查。')],
         faqs=[(T('Do electric cars need servicing?', 'Adakah kereta elektrik perlu diservis?', '电动车需要保养吗？'),
                T('Yes. An EV has fewer moving parts than a petrol car, but tyres, brakes, fluids, filters, suspension and software still need regular checks.',
                  'Ya. EV mempunyai bahagian bergerak yang lebih sedikit berbanding kereta petrol, tetapi tayar, brek, cecair, penapis, suspensyen dan perisian masih perlu diperiksa secara berkala.',
                  '需要。电动车的运动部件比燃油车少，但轮胎、刹车、油液、滤芯、悬挂和软件仍然需要定期检查。')),
               (T('Do EVs need an oil change?', 'Adakah EV perlu tukar minyak enjin?', '电动车需要换机油吗？'),
                T('A battery electric car has no engine, so there is no engine oil to change. Other fluids, such as brake fluid and coolant, are still serviced on schedule.',
                  'Kereta elektrik bateri tiada enjin, jadi tiada minyak enjin untuk ditukar. Cecair lain seperti minyak brek dan penyejuk masih diservis mengikut jadual.',
                  '纯电动车没有发动机，所以没有机油可换。刹车油、冷却液等其他油液仍按计划保养。')),
               (T('How often should I service a Dongfeng EV?', 'Berapa kerap saya perlu servis EV Dongfeng?', '东风电动车多久保养一次？'),
                T('Every 10,000 km at our Johor Bahru 3S centre. WhatsApp us your model and mileage to book.',
                  'Setiap 10,000 km di pusat 3S Johor Bahru kami. WhatsApp kami model dan jarak perjalanan anda untuk menempah.',
                  '在我们的新山 3S 中心，每 10,000 公里保养一次。请 WhatsApp 告诉我们车型和里程来预约。')),
               (T('Can I check or repair the high-voltage battery myself?', 'Bolehkah saya periksa atau baiki bateri voltan tinggi sendiri?', '我可以自己检查或维修高压电池吗？'),
                T('No. High-voltage parts carry dangerous voltage and need trained technicians with the right tools. Contact a service centre instead.',
                  'Tidak. Bahagian voltan tinggi membawa voltan yang bahaya dan memerlukan juruteknik terlatih dengan peralatan yang betul. Hubungi pusat servis sebaliknya.',
                  '不可以。高压部件带有危险电压，必须由受过培训、使用正确工具的技师处理。请联系服务中心。'))]),
    # Night article 23 Oct 2026 (queue #2, LOW risk, register row). Figures only from the model pages: Vigo 51.87 kWh / 471 km CLTC / DC up to 167 kW,
    # 007 Premium up to 650 km CLTC / DC up to 200 kW, AC up to 6.6 kW (about 9 h for a near-empty Vigo). No prices, no savings, no cross-border rules.
    dict(slug='is-an-ev-practical-for-daily-driving-in-johor', photo='vigo-front', owner='test-drive/', date='2026-10-23',
         title=T('Is an EV Practical for Daily Driving in Johor?', 'Adakah EV Praktikal untuk Pemanduan Harian di Johor?', '电动车适合在柔佛日常使用吗？'),
         h1=T('Is an EV practical for daily driving in Johor?', 'Adakah EV praktikal untuk pemanduan harian di Johor?', '电动车适合在柔佛日常使用吗？'),
         desc=T('How to tell if an electric car suits your daily drive in Johor: your own distance, where you can charge, heat and traffic, and what to ask before you decide.',
                'Cara menilai sama ada kereta elektrik sesuai dengan pemanduan harian anda di Johor: jarak sendiri, tempat mengecas, cuaca panas dan trafik, serta apa perlu ditanya sebelum membuat keputusan.',
                '如何判断电动车是否适合您在柔佛的日常出行：自己的行驶距离、能在哪里充电、炎热天气与塞车，以及决定前该问什么。'),
         answer=T('For most daily driving in Johor, an EV is practical if you can charge where you park and your usual day is well within the car\'s real-world range. Work out your own daily distance first, then compare it with the range: the Dongfeng Vigo is rated at 471 km (CLTC) and the Dongfeng 007 Premium up to 650 km (CLTC). Real range is lower and depends on speed, weather, air-con and charger.',
                  'Bagi kebanyakan pemanduan harian di Johor, EV adalah praktikal jika anda boleh mengecas di tempat letak kereta dan hari biasa anda jauh di bawah jarak sebenar kereta. Kira jarak harian anda dahulu, kemudian bandingkan dengan jarak kereta: Dongfeng Vigo bernilai 471 km (CLTC) dan Dongfeng 007 Premium sehingga 650 km (CLTC). Jarak sebenar lebih rendah dan bergantung pada kelajuan, cuaca, penyaman udara dan pengecas.',
                  '在柔佛的大多数日常驾驶中，只要您能在停车的地方充电，而且平时一天的行程远低于车辆的实际续航，电动车就是实用的。先算出自己每天的行驶距离，再与续航对照：东风 Vigo 的续航为 471 公里（CLTC），东风 007 Premium 最高 650 公里（CLTC）。实际续航会更低，并取决于车速、天气、空调和充电设备。'),
         sections=[(T('Start with your own daily distance', 'Mulakan dengan jarak harian anda sendiri', '先算自己每天的行驶距离'),
                    T('Add up a normal day: home to work, school runs, errands and the drive back. Check the odometer for a week if you are not sure. If that figure is a small part of the car\'s range, you will not need to think about charging every day. The published range is measured on the CLTC test cycle, so treat it as a guide and expect less in everyday use.',
                      'Jumlahkan hari biasa anda: rumah ke tempat kerja, hantar anak ke sekolah, urusan harian dan perjalanan pulang. Semak odometer selama seminggu jika anda tidak pasti. Jika angka itu hanya sebahagian kecil daripada jarak kereta, anda tidak perlu risau tentang mengecas setiap hari. Jarak yang diterbitkan diukur pada kitaran ujian CLTC, jadi anggap ia sebagai panduan dan jangkakan kurang dalam penggunaan harian.',
                      '把平常一天的行程加起来：家到公司、接送孩子、办事和回家。如果不确定，可以看一个星期的里程表。如果这个数字只占车辆续航的一小部分，就不必每天都为充电操心。公布的续航是按 CLTC 测试循环测得的，请当作参考，日常使用中会更低。')),
                   (T('Where will you charge?', 'Di mana anda akan mengecas?', '您在哪里充电？'),
                    T('Charging at home or work is what makes an EV easy day to day. Both the Vigo and the 007 take AC charging at up to 6.6 kW, so a near-empty Vigo battery (51.87 kWh) needs about 9 hours on a 6.6 kW wall box: an overnight charge. If you live in a condo or a managed estate, ask the management about charging first. For longer trips, DC fast charging is faster: the Vigo accepts up to 167 kW and the 007 up to 200 kW, depending on the charger.',
                      'Mengecas di rumah atau tempat kerja menjadikan EV mudah digunakan setiap hari. Vigo dan 007 menerima pengecasan AC sehingga 6.6 kW, jadi bateri Vigo (51.87 kWh) yang hampir kosong memerlukan kira-kira 9 jam pada pengecas dinding 6.6 kW: cas semalaman. Jika anda tinggal di kondominium atau kawasan berpengurusan, tanya pihak pengurusan tentang pengecasan dahulu. Untuk perjalanan jauh, pengecasan pantas DC lebih cepat: Vigo menerima sehingga 167 kW dan 007 sehingga 200 kW, bergantung pada pengecas.',
                      '在家或公司充电，是电动车日常使用方便的关键。Vigo 和 007 的交流充电功率最高都是 6.6 kW，因此 Vigo 的 51.87 kWh 电池从接近没电充满，在 6.6 kW 壁挂充电盒上大约需要 9 小时，也就是充一晚。如果住公寓或有管理的住宅区，请先向管理处询问充电事宜。长途出行时，直流快充更快：Vigo 最高 167 kW，007 最高 200 kW，实际取决于充电桩。')),
                   (T('Heat, rain and traffic', 'Cuaca panas, hujan dan trafik', '炎热、下雨与塞车'),
                    T('Air-con works hard in Johor\'s heat, and that uses battery energy, so expect it to take some range. Stop-start traffic is easier on an EV than on a petrol car, because regenerative braking recovers some energy when you slow down. High motorway speeds use more energy than city driving. None of this stops an EV working day to day; it is why real-world range is a range, not a fixed number.',
                      'Penyaman udara bekerja keras dalam cuaca panas Johor, dan itu menggunakan tenaga bateri, jadi jangkakan ia mengurangkan sedikit jarak. Trafik henti-dan-gerak lebih sesuai untuk EV berbanding kereta petrol, kerana brek regeneratif memulihkan sedikit tenaga apabila anda memperlahankan kereta. Kelajuan lebuh raya yang tinggi menggunakan lebih banyak tenaga berbanding pemanduan bandar. Semua ini tidak menghalang EV digunakan setiap hari; itulah sebabnya jarak sebenar ialah satu julat, bukan angka tetap.',
                      '柔佛天气炎热，空调负荷大，会消耗电池电量，所以要预期它占用一部分续航。走走停停的塞车路况对电动车比燃油车更友好，因为减速时动能回收可以回收部分能量。高速公路上的高车速比市区行驶更耗电。这些都不妨碍电动车的日常使用，这也是为什么实际续航是一个范围，而不是固定数字。')),
                   (T('Questions to ask yourself', 'Soalan untuk diri sendiri', '先问问自己'), None),
                   (T('Try it before you decide', 'Cuba sebelum anda membuat keputusan', '决定之前先试一试'),
                    T('The best test is your own drive. Book a test drive at our Johor Bahru 3S centre, ask about charging at your home, and bring your usual questions. Our guide to the EV test drive checklist tells you what to look for.',
                      'Ujian terbaik ialah pemanduan anda sendiri. Tempah pandu uji di pusat 3S kami di Johor Bahru, tanya tentang pengecasan di rumah anda dan bawa soalan biasa anda. Panduan senarai semak pandu uji EV kami menerangkan apa yang perlu diperhatikan.',
                      '最好的检验就是亲自驾驶。到我们的新山 3S 中心预约试驾，问问您家里的充电安排，并带上平时关心的问题。我们的电动车试驾清单文章会告诉您该留意什么。'))],
         checks=[T('Can I charge where I park, at home or at work?', 'Bolehkah saya mengecas di tempat saya letak kereta, di rumah atau di tempat kerja?', '我停车的地方（家里或公司）能充电吗？'),
                 T('Is my usual day well inside the car\'s real-world range?', 'Adakah hari biasa saya jauh di dalam jarak sebenar kereta?', '我平常一天的行程是否远在车辆实际续航之内？'),
                 T('Do I drive long distances often enough to need DC fast charging?', 'Adakah saya kerap memandu jauh sehingga perlu pengecasan pantas DC?', '我是否经常长途出行，需要用到直流快充？'),
                 T('Do I know who services the car, and how often? Ours is every 10,000 km.', 'Adakah saya tahu siapa yang menservis kereta, dan berapa kerap? Servis kami setiap 10,000 km.', '我是否清楚由谁保养、多久保养一次？我们的保养周期为每 10,000 公里。')],
         faqs=[(T('Is 471 km of range enough for daily driving?', 'Adakah jarak 471 km mencukupi untuk pemanduan harian?', '471 公里续航够日常使用吗？'),
                T('For most people, a normal day is far shorter than that. The 471 km figure is the Dongfeng Vigo\'s CLTC rating and real range is lower, so compare it with your own daily distance and ask us about your usual routes.',
                  'Bagi kebanyakan orang, hari biasa jauh lebih pendek daripada itu. Angka 471 km ialah nilai CLTC Dongfeng Vigo dan jarak sebenar lebih rendah, jadi bandingkan dengan jarak harian anda sendiri dan tanya kami tentang laluan biasa anda.',
                  '对大多数人来说，平常一天的行程要短得多。471 公里是东风 Vigo 的 CLTC 续航，实际续航会更低，请与自己的每日行驶距离对照，也可以向我们询问您常走的路线。')),
               (T('Can I charge an EV at home in Johor?', 'Bolehkah saya mengecas EV di rumah di Johor?', '在柔佛可以在家给电动车充电吗？'),
                T('Usually yes, with an AC wall box installed by a licensed electrician. Condos and managed estates may have their own rules, so ask the management first.',
                  'Biasanya boleh, dengan pengecas dinding AC yang dipasang oleh juruelektrik berlesen. Kondominium dan kawasan berpengurusan mungkin ada peraturan sendiri, jadi tanya pihak pengurusan dahulu.',
                  '通常可以，由持证电工安装交流壁挂充电盒即可。公寓和有管理的住宅区可能有自己的规定，请先向管理处询问。')),
               (T('Does the air-con reduce range?', 'Adakah penyaman udara mengurangkan jarak?', '空调会减少续航吗？'),
                T('Yes, the air-con uses battery energy, so some range is used in Johor\'s heat. It is one of the reasons real-world range is lower than the CLTC figure.',
                  'Ya, penyaman udara menggunakan tenaga bateri, jadi sedikit jarak digunakan dalam cuaca panas Johor. Ia salah satu sebab jarak sebenar lebih rendah daripada angka CLTC.',
                  '会的，空调要用电池电量，在柔佛的炎热天气里会占用一部分续航。这也是实际续航低于 CLTC 数字的原因之一。')),
               (T('How do I try a Dongfeng EV?', 'Bagaimana saya boleh mencuba EV Dongfeng?', '怎样试驾东风电动车？'),
                T('Book a test drive on WhatsApp and tell us your model and a time that suits you. We will confirm the appointment.',
                  'Tempah pandu uji melalui WhatsApp dan beritahu kami model serta masa yang sesuai. Kami akan mengesahkan temujanji.',
                  '通过 WhatsApp 预约试驾，告诉我们车型和方便的时间，我们会确认预约。'))]),
    # Night article 25 Oct 2026 (odd day; queue #8). Risk gate LOW: only the Vigo model-page figures (seats, 500 L / 1,040 L boot, split tailgate bench 150 kg, 2,000 mm bed,
    # 6 airbags, L2 ADAS, 540-degree camera, panoramic sunroof, AC 6.6 kW about 9 h, V2L 3.3 kW, 471 km CLTC); no prices, no warranty terms, no competitors, no child-seat claims.
    dict(slug='dongfeng-vigo-for-families', photo='vigo-boot', owner='models/', date='2026-10-25',
         title=T('Is the Dongfeng Vigo a Good Family Car? Space and Boot', 'Adakah Dongfeng Vigo Kereta Keluarga yang Baik? Ruang dan But', '东风 Vigo 适合家用吗？空间与后备箱'),
         h1=T('Is the Dongfeng Vigo a good family car?', 'Adakah Dongfeng Vigo kereta keluarga yang baik?', '东风 Vigo 适合家用吗？'),
         desc=T('What the Dongfeng Vigo offers a family in Johor: five seats, a 500-litre boot, a split tailgate, fold-flat rear seats, and what to test with your own stroller and child seats.',
                'Apa yang ditawarkan Dongfeng Vigo kepada keluarga di Johor: lima tempat duduk, but 500 liter, pintu belakang terbelah, tempat duduk belakang dilipat rata, dan apa yang perlu dicuba dengan stroler dan kerusi kanak-kanak anda.',
                '东风 Vigo 能为柔佛家庭带来什么：五座、500 升后备箱、分体式尾门、后排放平，以及试驾时该带上婴儿车和儿童座椅实际试放。'),
         answer=T('The Dongfeng Vigo is a five-seat electric SUV with a 500-litre boot (1,040 litres with the rear seats folded), a split tailgate whose lower half folds into a bench, and rear seats that fold flat into a 2-metre bed. That is a lot of practical space for a family, but only your own stroller, child seats and routine can confirm it, so bring them to a test drive at our Johor Bahru 3S centre.',
                  'Dongfeng Vigo ialah SUV elektrik lima tempat duduk dengan but 500 liter (1,040 liter apabila tempat duduk belakang dilipat), pintu belakang terbelah yang bahagian bawahnya menjadi bangku, dan tempat duduk belakang yang dilipat rata menjadi katil 2 meter. Itu ruang praktikal yang banyak untuk keluarga, tetapi hanya stroler, kerusi kanak-kanak dan rutin anda sendiri yang dapat mengesahkannya, jadi bawa semuanya semasa pandu uji di pusat 3S kami di Johor Bahru.',
                  '东风 Vigo 是一款五座纯电 SUV，后备箱 500 升（后排放倒达 1,040 升），分体式尾门的下半部可翻成长凳，后排放平后成为 2 米大床。对家庭来说，这是相当实用的空间，但要确认是否合适，还得用您自己的婴儿车、儿童座椅和日常习惯来试，欢迎带到我们的新山 3S 中心试驾。'),
         sections=[(T('How much room is there for the family?', 'Berapa banyak ruang untuk keluarga?', '一家人的空间够不够？'),
                    T('The Vigo seats five and measures 4,306 mm long and 1,868 mm wide, with a 2,715 mm wheelbase. Those are compact-SUV dimensions, so it is easy to park in a Johor mall or a terrace-house porch, while the boot and fold-flat seats give the load space of a larger car. Numbers do not show how a back seat feels with children in it, so sit in the rear with the people who will use it.',
                      'Vigo memuatkan lima orang dan berukuran 4,306 mm panjang dan 1,868 mm lebar, dengan jarak roda 2,715 mm. Itu dimensi SUV padat, jadi mudah diparkir di pusat membeli-belah di Johor atau porch rumah teres, sementara but dan tempat duduk lipat rata memberi ruang muatan sebuah kereta yang lebih besar. Angka tidak menunjukkan keselesaan tempat duduk belakang dengan kanak-kanak, jadi duduk di belakang bersama orang yang akan menggunakannya.',
                      'Vigo 可坐五人，车长 4,306 毫米、车宽 1,868 毫米，轴距 2,715 毫米。这是紧凑型 SUV 的尺寸，停进新山的商场车位或排屋车道都方便，而后备箱和可放平的后排又提供了更大车型的载物空间。数字看不出后排坐着孩子的感觉，所以请和将来坐后排的家人一起坐进去感受。')),
                   (T('What does the 500-litre boot hold?', 'Apa yang boleh dimuatkan dalam but 500 liter?', '500 升后备箱能装什么？'),
                    T('The boot is 500 litres, or 1,040 litres with the rear seats folded. The tailgate is split: the lower half folds out as a bench that holds up to 150 kg, which is handy for changing shoes at the beach, a picnic or waiting at a roadside stall. The rear seats also fold flat into a bed 2,000 mm long. The best test is your own gear: bring a stroller, a trolley bag or a sports bag to the showroom and load it.',
                      'But ialah 500 liter, atau 1,040 liter apabila tempat duduk belakang dilipat. Pintu belakangnya terbelah: bahagian bawah dibuka menjadi bangku yang menanggung sehingga 150 kg, berguna untuk menukar kasut di pantai, berkelah atau menunggu di gerai tepi jalan. Tempat duduk belakang juga boleh dilipat rata menjadi katil sepanjang 2,000 mm. Ujian terbaik ialah barang anda sendiri: bawa stroler, beg troli atau beg sukan ke bilik pameran dan muatkan.',
                      '后备箱容积 500 升，后排放倒达 1,040 升。尾门是分体式：下半部翻出来就是一条可承重 150 公斤的长凳，在海边换鞋、野餐或路边摊等位时很方便。后排还能放平成长 2,000 毫米的大床。最好的检验就是用自己的东西：把婴儿车、拉杆箱或运动背包带到展厅，装装看。')),
                   (T('What equipment will parents notice?', 'Kelengkapan apa yang diperhatikan ibu bapa?', '家长会留意哪些配置？'),
                    T('The Vigo has a panoramic sunroof, a 12.8-inch centre screen with wireless Apple CarPlay, a 50 W wireless charger, USB-C and 12 V sockets, 6 airbags, Level 2 driver assistance (ADAS) and a 540-degree camera. Driver assistance supports the driver and does not replace attention, and equipment can differ by version, so ask us to confirm it on the car you are looking at.',
                      'Vigo mempunyai bumbung matahari panoramik, skrin tengah 12.8 inci dengan Apple CarPlay tanpa wayar, pengecas tanpa wayar 50 W, soket USB-C dan 12 V, 6 beg udara, bantuan pemandu Tahap 2 (ADAS) dan kamera 540 darjah. Bantuan pemandu menyokong pemandu dan tidak menggantikan perhatian, dan kelengkapan boleh berbeza mengikut versi, jadi minta kami mengesahkannya pada kereta yang anda lihat.',
                      'Vigo 配有全景天窗、12.8 英寸中控屏（支持无线 Apple CarPlay）、50 W 无线充电、USB-C 和 12 V 接口、6 个气囊、L2 级驾驶辅助（ADAS）以及 540 度全景影像。驾驶辅助只是协助驾驶者，不能取代专注驾驶，配置也可能因版本而异，请向我们确认您看的那辆车的实际配置。')),
                   (T('What about charging with a family routine?', 'Bagaimana pengecasan dengan rutin keluarga?', '家庭日常怎么充电？'),
                    T('The Vigo has a 51.87 kWh battery and a claimed 471 km range on the CLTC cycle; real range is lower and depends on speed, load, weather and air-con. At home, AC charging at up to 6.6 kW takes about 9 hours for a full charge, which suits an overnight charge, and the car has a 3.3 kW V2L socket to power devices from the battery. Ask the management first if you live in a condo.',
                      'Vigo mempunyai bateri 51.87 kWh dan jarak 471 km pada kitaran CLTC; jarak sebenar lebih rendah dan bergantung pada kelajuan, muatan, cuaca dan penghawa dingin. Di rumah, pengecasan AC sehingga 6.6 kW mengambil kira-kira 9 jam untuk cas penuh, sesuai untuk cas semalaman, dan kereta ini mempunyai soket V2L 3.3 kW untuk menghidupkan peranti daripada bateri. Tanya pihak pengurusan dahulu jika anda tinggal di kondominium.',
                      'Vigo 配备 51.87 kWh 电池，CLTC 工况续航 471 公里；实际续航更低，并受车速、载重、天气和空调影响。在家使用交流慢充，最高 6.6 kW，充满约需 9 小时，适合充一晚；车上还有 3.3 kW 的 V2L 对外放电接口，可从电池给设备供电。住公寓的话请先询问管理处。')),
                   (T('What to bring to a test drive', 'Apa yang perlu dibawa semasa pandu uji', '试驾时带什么'), None)],
         checks=[T('Your stroller or trolley bag, to load it through the tailgate', 'Stroler atau beg troli anda, untuk dimuatkan melalui pintu belakang', '婴儿车或拉杆箱，试着从尾门装进去'),
                 T('Your child seats, to see how they fit on the rear seats', 'Kerusi kanak-kanak anda, untuk melihat kesesuaiannya di tempat duduk belakang', '儿童座椅，看看装在后排合不合适'),
                 T('The family members who will sit in the back', 'Ahli keluarga yang akan duduk di belakang', '将来坐后排的家人'),
                 T('Your usual daily distance, so we can talk through charging at home', 'Jarak harian biasa anda, supaya kami boleh bincang tentang pengecasan di rumah', '您平时每天的行驶距离，方便一起谈谈在家充电的安排')],
         faqs=[(T('Is the Dongfeng Vigo a five-seater?', 'Adakah Dongfeng Vigo lima tempat duduk?', '东风 Vigo 是五座车吗？'),
                T('Yes. The Dongfeng Vigo is a five-seat electric SUV.', 'Ya. Dongfeng Vigo ialah SUV elektrik lima tempat duduk.', '是的，东风 Vigo 是一款五座纯电 SUV。')),
               (T('How big is the Vigo boot?', 'Sebesar mana but Vigo?', 'Vigo 的后备箱有多大？'),
                T('500 litres, or 1,040 litres with the rear seats folded. The lower half of the split tailgate also folds out as a bench that holds up to 150 kg.',
                  '500 liter, atau 1,040 liter apabila tempat duduk belakang dilipat. Bahagian bawah pintu belakang terbelah juga boleh dibuka menjadi bangku yang menanggung sehingga 150 kg.',
                  '500 升，后排放倒后为 1,040 升。分体式尾门的下半部还能翻出来当长凳，承重最高 150 公斤。')),
               (T('Can I try my own stroller or child seat in the car?', 'Bolehkah saya mencuba stroler atau kerusi kanak-kanak sendiri dalam kereta?', '可以带自己的婴儿车或儿童座椅来试吗？'),
                T('Yes. Tell us when you book your test drive on WhatsApp and bring them along, so you can see how they fit before you decide.',
                  'Boleh. Beritahu kami semasa tempah pandu uji melalui WhatsApp dan bawa bersama, supaya anda dapat melihat kesesuaiannya sebelum membuat keputusan.',
                  '可以。通过 WhatsApp 预约试驾时告诉我们，并把它们带来，在决定之前亲自看看合不合适。')),
               (T('Can the Vigo be charged overnight at home?', 'Bolehkah Vigo dicas semalaman di rumah?', 'Vigo 能在家充一晚吗？'),
                T('With AC charging at up to 6.6 kW, a full charge takes about 9 hours, so an overnight charge suits many households. Condos and managed estates may have their own rules, so ask the management first.',
                  'Dengan pengecasan AC sehingga 6.6 kW, cas penuh mengambil kira-kira 9 jam, jadi cas semalaman sesuai untuk banyak isi rumah. Kondominium dan kawasan berpengurusan mungkin ada peraturan sendiri, jadi tanya pihak pengurusan dahulu.',
                  '交流慢充最高 6.6 kW，充满约需 9 小时，因此很多家庭可以充一晚。公寓和有管理的住宅区可能有自己的规定，请先询问管理处。'))]),
    # Night article 27 Oct 2026 (odd day; queue #10). Risk gate LOW: only 007 model-page figures (Premium: single rear motor 200 kW / 268 hp / 310 Nm, 0-100 in 5.8 s, 650 km CLTC / 530 WLTP, 18-inch wheels;
    # Prime: dual motor AWD 400 kW / 544 PS / 620 Nm, 0-100 in 3.9 s, 565 km CLTC / 389 WLTP, 19-inch wheels with performance calipers; both 73.48 kWh LFP, 5 seats, 452 L boot, 6 airbags, L2 ADAS, interior colours).
    # No prices, no warranty terms, no charging-time claims, no competitors, no savings; "official dealer" wording not used.
    dict(slug='dongfeng-007-premium-or-prime', photo='007-studio', owner='models/', date='2026-10-27',
         title=T('Dongfeng 007 Premium or Prime: Which Suits You?', 'Dongfeng 007 Premium atau Prime: Mana Sesuai Untuk Anda?', '东风 007 Premium 还是 Prime：哪个适合您？'),
         h1=T('Dongfeng 007 Premium or Prime: which one suits you?', 'Dongfeng 007 Premium atau Prime: yang mana sesuai untuk anda?', '东风 007 Premium 还是 Prime：哪个适合您？'),
         desc=T('Dongfeng 007 Premium (rear-wheel drive, up to 650 km CLTC) or Prime (dual-motor all-wheel drive, 0-100 km/h in 3.9 s)? The differences in range, power, wheels and interior, and how to choose in Johor Bahru.',
                'Dongfeng 007 Premium (pacuan roda belakang, sehingga 650 km CLTC) atau Prime (dua motor pacuan semua roda, 0-100 km/j 3.9 s)? Perbezaan jarak, kuasa, rim dan dalaman, dan cara memilih di Johor Bahru.',
                '东风 007 Premium（后驱，CLTC 最高 650 公里）还是 Prime（双电机四驱，0-100 加速 3.9 秒）？续航、动力、轮毂与内饰的差别，以及在新山如何选择。'),
         answer=T('Choose the Dongfeng 007 Premium if you want the longest range: it has one rear motor, 200 kW (268 hp) and up to 650 km on the CLTC cycle. Choose the 007 Prime if you want the most performance: it has two motors, all-wheel drive, 400 kW (544 PS) and goes from 0-100 km/h in 3.9 seconds, with up to 565 km CLTC range. Both share the same 73.48 kWh battery and body, so a test drive of both is the best way to decide.',
                  'Pilih Dongfeng 007 Premium jika anda mahu jarak paling jauh: satu motor belakang, 200 kW (268 hp) dan sehingga 650 km pada kitaran CLTC. Pilih 007 Prime jika anda mahu prestasi tertinggi: dua motor, pacuan semua roda, 400 kW (544 PS) dan 0-100 km/j dalam 3.9 saat, dengan jarak sehingga 565 km CLTC. Kedua-duanya berkongsi bateri 73.48 kWh dan badan yang sama, jadi pandu uji kedua-duanya ialah cara terbaik untuk membuat keputusan.',
                  '想要最长续航，选东风 007 Premium：单后电机，功率 200 kW（268 匹），CLTC 续航最高 650 公里。想要最强性能，选 007 Prime：双电机四驱，功率 400 kW（544 PS），0-100 公里/时加速 3.9 秒，CLTC 续航最高 565 公里。两个版本共用 73.48 kWh 电池和同一车身，所以最好的办法是两款都试驾。'),
         sections=[(T('What is the main difference between the 007 Premium and the 007 Prime?', 'Apakah perbezaan utama antara 007 Premium dan 007 Prime?', '007 Premium 和 Prime 的主要区别是什么？'),
                    T('The difference is the drivetrain. The Premium (Long Range RWD) has a single rear motor and drives the rear wheels. The Prime (AWD) adds a second motor so it drives all four wheels. Both are five-seat electric fastback sedans with a 73.48 kWh LFP battery, 4,880 mm long, with a 2,915 mm wheelbase.',
                      'Perbezaannya ialah sistem pemacu. Premium (Long Range RWD) mempunyai satu motor belakang dan memacu roda belakang. Prime (AWD) menambah motor kedua supaya memacu keempat-empat roda. Kedua-duanya sedan fastback elektrik lima tempat duduk dengan bateri LFP 73.48 kWh, panjang 4,880 mm, dengan jarak roda 2,915 mm.',
                      '区别在于驱动方式。Premium（Long Range RWD）为单后电机，驱动后轮。Prime（AWD）多了第二个电机，四轮驱动。两者都是五座纯电轿跑，配 73.48 kWh 磷酸铁锂电池，车长 4,880 毫米，轴距 2,915 毫米。')),
                   (T('How do range and power compare?', 'Bagaimana jarak dan kuasa dibandingkan?', '续航和动力怎么比？'),
                    T('The Premium makes 200 kW (268 hp) and 310 Nm, goes from 0-100 km/h in 5.8 seconds and has up to 650 km of range on the CLTC cycle (530 km WLTP). The Prime makes 400 kW (544 PS) and 620 Nm, does 0-100 km/h in 3.9 seconds and has up to 565 km on CLTC (389 km WLTP). Range figures are test-cycle numbers: real range is lower and depends on speed, load, weather and air-con.',
                      'Premium menghasilkan 200 kW (268 hp) dan 310 Nm, 0-100 km/j dalam 5.8 saat dan jarak sehingga 650 km pada kitaran CLTC (530 km WLTP). Prime menghasilkan 400 kW (544 PS) dan 620 Nm, 0-100 km/j dalam 3.9 saat dan jarak sehingga 565 km CLTC (389 km WLTP). Angka jarak ialah angka kitaran ujian: jarak sebenar lebih rendah dan bergantung pada kelajuan, muatan, cuaca dan penghawa dingin.',
                      'Premium 功率 200 kW（268 匹），扭矩 310 牛·米，0-100 公里/时加速 5.8 秒，CLTC 续航最高 650 公里（WLTP 530 公里）。Prime 功率 400 kW（544 PS），扭矩 620 牛·米，0-100 加速 3.9 秒，CLTC 续航最高 565 公里（WLTP 389 公里）。续航是测试工况数据：实际续航更低，并受车速、载重、天气和空调影响。')),
                   (T('What else changes between the two versions?', 'Apa lagi yang berbeza antara kedua-dua versi?', '两个版本还有哪些不同？'),
                    T('The Premium runs on 18-inch wheels, while the Prime has 19-inch wheels with performance calipers. Inside, the Premium is black with white contrast; the Prime is black with white-contrast faux-leather seats, or the Prime-only white dashboard with grey contrast. Both have a 15.6-inch centre screen, a 19-speaker WANOS sound system, a panoramic glass roof, 6 airbags and Level 2 driver assistance (ADAS). Driver assistance supports the driver and does not replace attention. Equipment can change, so ask us to confirm it on the car you are looking at.',
                      'Premium menggunakan rim 18 inci, manakala Prime mempunyai rim 19 inci dengan kaliper prestasi. Di dalam, Premium berwarna hitam dengan kontras putih; Prime hitam dengan tempat duduk kulit tiruan berkontras putih, atau papan pemuka putih berkontras kelabu khas Prime. Kedua-duanya mempunyai skrin tengah 15.6 inci, sistem bunyi WANOS 19 pembesar suara, bumbung kaca panoramik, 6 beg udara dan bantuan pemandu Tahap 2 (ADAS). Bantuan pemandu menyokong pemandu dan tidak menggantikan perhatian. Kelengkapan boleh berubah, jadi minta kami mengesahkannya pada kereta yang anda lihat.',
                      'Premium 配 18 英寸轮毂，Prime 配 19 英寸轮毂和性能卡钳。内饰方面，Premium 为黑色配白色撞色；Prime 为黑色配白色撞色仿皮座椅，或 Prime 专属的白色仪表台配灰色撞色。两者都配 15.6 英寸中控屏、WANOS 19 扬声器音响、全景玻璃车顶、6 个气囊和 L2 级驾驶辅助（ADAS）。驾驶辅助只是协助驾驶者，不能取代专注驾驶。配置可能调整，请向我们确认您看的那辆车的实际配置。')),
                   (T('Which one suits which driver?', 'Yang mana sesuai untuk pemandu yang mana?', '什么样的车主适合哪一款？'),
                    T('If you drive long distances, such as regular trips between Johor Bahru and the north or south of the peninsula, the Premium\'s longer range is the point of the version. If you enjoy strong acceleration and the grip of all-wheel drive, the Prime is built for that. For daily driving around Johor, either one covers a typical day, so let the way you drive and the cabin you prefer decide.',
                      'Jika anda kerap memandu jauh, seperti perjalanan berkala dari Johor Bahru ke utara atau selatan semenanjung, jarak lebih jauh Premium ialah tujuan versi itu. Jika anda suka pecutan kuat dan cengkaman pacuan semua roda, Prime dibina untuk itu. Untuk pemanduan harian sekitar Johor, kedua-duanya meliputi hari biasa, jadi biarkan cara anda memandu dan kabin pilihan anda yang menentukan.',
                      '如果您常跑长途，例如经常往返新山与半岛南北，Premium 更长的续航正是这个版本的重点。如果您喜欢强劲加速和四驱的抓地力，Prime 就是为此而设。在柔佛日常通勤，两款都足以应付一天的行程，所以让驾驶习惯和您喜欢的座舱来决定。')),
                   (T('What to check when you test drive both', 'Apa yang perlu diperiksa semasa menguji kedua-duanya', '试驾两款时可以看什么'), None)],
         checks=[T('How the Premium and Prime feel when you accelerate from a stop and when you overtake', 'Bagaimana Premium dan Prime terasa semasa memecut dari berhenti dan semasa memotong', 'Premium 和 Prime 起步加速、超车时的感觉'),
                 T('Ride comfort on 18-inch versus 19-inch wheels on the roads you use', 'Keselesaan pemanduan pada rim 18 inci berbanding 19 inci di jalan yang anda guna', '18 英寸与 19 英寸轮毂在您常走的路上的舒适度'),
                 T('The interior colours in real light, since on-screen colours are only a guide', 'Warna dalaman dalam cahaya sebenar, kerana warna di skrin hanya panduan', '在真实光线下看内饰颜色，屏幕上的颜色仅供参考'),
                 T('Your usual daily and weekend distances, so we can talk through range and charging', 'Jarak harian dan hujung minggu biasa anda, supaya kami boleh bincang tentang jarak dan pengecasan', '您平时的日常与周末行驶距离，方便一起谈谈续航与充电')],
         faqs=[(T('What is the difference between the Dongfeng 007 Premium and Prime?', 'Apakah beza Dongfeng 007 Premium dan Prime?', '东风 007 Premium 和 Prime 有什么区别？'),
                T('The Premium has one rear motor (200 kW, 268 hp) and the longer range, up to 650 km CLTC. The Prime has two motors and all-wheel drive (400 kW, 544 PS), 0-100 km/h in 3.9 seconds and up to 565 km CLTC.',
                  'Premium mempunyai satu motor belakang (200 kW, 268 hp) dan jarak lebih jauh, sehingga 650 km CLTC. Prime mempunyai dua motor dan pacuan semua roda (400 kW, 544 PS), 0-100 km/j dalam 3.9 saat dan sehingga 565 km CLTC.',
                  'Premium 为单后电机（200 kW，268 匹），续航更长，CLTC 最高 650 公里。Prime 为双电机四驱（400 kW，544 PS），0-100 加速 3.9 秒，CLTC 续航最高 565 公里。')),
               (T('Do the Premium and Prime use the same battery?', 'Adakah Premium dan Prime menggunakan bateri yang sama?', 'Premium 和 Prime 用的是同一块电池吗？'),
                T('Yes. Both use a 73.48 kWh LFP battery. The range differs because the drivetrain, weight and wheels differ.', 'Ya. Kedua-duanya menggunakan bateri LFP 73.48 kWh. Jarak berbeza kerana sistem pemacu, berat dan rim berbeza.', '是的，两者都用 73.48 kWh 磷酸铁锂电池。续航不同，是因为驱动系统、重量和轮毂不同。')),
               (T('Is the Prime much faster than the Premium?', 'Adakah Prime jauh lebih laju daripada Premium?', 'Prime 比 Premium 快很多吗？'),
                T('On the manufacturer\'s figures, the Prime does 0-100 km/h in 3.9 seconds and the Premium in 5.8 seconds. How that feels depends on you, so try both.', 'Mengikut angka pengeluar, Prime mencapai 0-100 km/j dalam 3.9 saat dan Premium dalam 5.8 saat. Bagaimana rasanya bergantung pada anda, jadi cuba kedua-duanya.', '按厂家数据，Prime 0-100 公里/时加速 3.9 秒，Premium 为 5.8 秒。实际感受因人而异，所以两款都试一试。')),
               (T('Can I test drive both versions in Johor Bahru?', 'Bolehkah saya pandu uji kedua-dua versi di Johor Bahru?', '可以在新山试驾两个版本吗？'),
                T('Book a test drive on WhatsApp and tell us you want to compare the Premium and the Prime. We will confirm the appointment and the cars available.', 'Tempah pandu uji melalui WhatsApp dan beritahu kami anda mahu membandingkan Premium dan Prime. Kami akan mengesahkan temujanji dan kereta yang ada.', '通过 WhatsApp 预约试驾，告诉我们您想比较 Premium 和 Prime。我们会确认预约和现有车辆。'))]),
    # Night article 29 Oct 2026 (every-2-days rule; queue #7). Risk gate MEDIUM-general: no tariffs/tax/regulatory figures, no warranty terms, no range/charging/battery-life guarantees, no competitors, no high-voltage how-to.
    dict(slug='ev-battery-care-in-malaysias-hot-weather', photo='vigo-dash', owner='service/', date='2026-10-29',
         title=T('EV Battery Care in Malaysia\'s Hot Weather: Simple Habits', 'Penjagaan Bateri EV Dalam Cuaca Panas Malaysia: Tabiat Mudah', '马来西亚炎热天气下的电动车电池保养：简单习惯'),
         h1=T('How do you look after an EV battery in Malaysia\'s hot weather?', 'Bagaimana menjaga bateri EV dalam cuaca panas Malaysia?', '在马来西亚的炎热天气里，怎样保养电动车电池？'),
         desc=T('Heat ages every battery over time. Simple habits for EV owners in Johor and Malaysia: shade, gentle charging, charge-limit advice from the owner\'s manual, and regular servicing.',
                'Haba mempercepatkan penuaan semua bateri. Tabiat mudah untuk pemilik EV di Johor dan Malaysia: tempat teduh, pengecasan lembut, nasihat had cas dalam manual pemilik, dan servis berkala.',
                '高温会让所有电池随时间老化。给柔佛和马来西亚电动车车主的简单习惯：停在阴凉处、温和充电、按车主手册的充电上限建议，以及定期保养。'),
         answer=T('Heat ages every battery over time, and Malaysia is warm all year, but a few habits help. Park in shade or covered parking when you can, rely on gentle home charging for everyday use, follow your owner\'s manual on charge limits, and keep up regular servicing. The Dongfeng Vigo and 007 both use LFP (lithium iron phosphate) batteries. No habit can guarantee battery life, so ask our service team about your car.',
                  'Haba mempercepatkan penuaan semua bateri dari masa ke masa, dan Malaysia panas sepanjang tahun, tetapi beberapa tabiat membantu. Letak kereta di tempat teduh atau tempat letak kereta berbumbung apabila boleh, guna pengecasan rumah yang lembut untuk kegunaan harian, ikut manual pemilik tentang had cas, dan teruskan servis berkala. Dongfeng Vigo dan 007 kedua-duanya menggunakan bateri LFP (litium ferum fosfat). Tiada tabiat yang boleh menjamin hayat bateri, jadi tanya pasukan servis kami tentang kereta anda.',
                  '高温会让所有电池随时间老化，而马来西亚全年炎热，但几个习惯会有帮助：尽量停在阴凉处或有顶的停车位，日常以温和的家用充电为主，按车主手册的建议设定充电上限，并坚持定期保养。东风 Vigo 和 007 都使用磷酸铁锂（LFP）电池。没有任何习惯能保证电池寿命，所以请向我们的售后团队咨询您的车。'),
         sections=[(T('Does Malaysia\'s heat damage an EV battery?', 'Adakah cuaca panas Malaysia merosakkan bateri EV?', '马来西亚的高温会损坏电动车电池吗？'),
                    T('Heat speeds up the slow ageing that every lithium-ion battery goes through, and a warm country gives it more heat to deal with than a cool one. That does not mean you should avoid driving or charging. EVs are built with systems that manage battery temperature, and everyday use in a warm climate is normal for them. The aim of good habits is to avoid piling on unnecessary stress, not to treat the battery as fragile.',
                      'Haba mempercepatkan proses penuaan perlahan yang dilalui oleh setiap bateri litium-ion, dan negara panas memberi lebih banyak haba berbanding negara sejuk. Itu tidak bermakna anda perlu mengelak memandu atau mengecas. EV dibina dengan sistem yang menguruskan suhu bateri, dan penggunaan harian dalam iklim panas adalah perkara biasa bagi mereka. Tujuan tabiat yang baik ialah mengelak tekanan yang tidak perlu, bukan menganggap bateri itu rapuh.',
                      '高温会加快每一块锂离子电池都会经历的缓慢老化，而热带国家的高温比凉爽地区更多。但这并不意味着要少开车或少充电。电动车带有管理电池温度的系统，在炎热气候下日常使用对它们来说是正常的。好习惯的目的，是避免给电池增加不必要的压力，而不是把电池当成易碎品。')),
                   (T('Which everyday habits are kind to the battery?', 'Tabiat harian yang manakah baik untuk bateri?', '哪些日常习惯对电池友好？'),
                    T('These are general good practice for any EV owner. Your owner\'s manual comes first for your car:',
                      'Ini ialah amalan baik yang umum untuk mana-mana pemilik EV. Manual pemilik anda diutamakan untuk kereta anda:',
                      '以下是适用于所有电动车车主的通用做法，具体以您车辆的车主手册为准：')),
                   (T('Does fast charging hurt the battery in hot weather?', 'Adakah pengecasan pantas merosakkan bateri dalam cuaca panas?', '高温天气下快充会伤电池吗？'),
                    T('DC fast charging is made for trips and quick top-ups, and the car controls the charging speed to protect the battery. Doing it again and again in strong heat adds more stress than slow charging, so for daily use most owners rely on gentle AC charging at home and keep fast charging for longer drives. Charging speed on any day depends on the car, the charger and the battery temperature.',
                      'Pengecasan pantas DC dibuat untuk perjalanan jauh dan tambah cas cepat, dan kereta mengawal kelajuan pengecasan untuk melindungi bateri. Melakukannya berulang kali dalam cuaca sangat panas menambah lebih banyak tekanan berbanding pengecasan perlahan, jadi untuk kegunaan harian kebanyakan pemilik bergantung pada pengecasan AC yang lembut di rumah dan menyimpan pengecasan pantas untuk perjalanan jauh. Kelajuan pengecasan pada mana-mana hari bergantung pada kereta, pengecas dan suhu bateri.',
                      '直流快充适合长途出行和快速补电，车辆会控制充电速度来保护电池。在高温下反复快充，比慢充更容易给电池增加压力，所以日常使用时，多数车主以家里温和的交流慢充为主，把快充留给长途行程。任何一天的充电速度，都取决于车辆、充电桩和电池温度。')),
                   (T('Should I always charge to 100%?', 'Perlukah saya sentiasa mengecas sehingga 100%?', '需要每次都充到 100% 吗？'),
                    T('Advice on charge limits differs by battery type and by maker, so follow the owner\'s manual for your car rather than a rule you read online. If you are unsure what suits your car and the way you drive, ask us.',
                      'Nasihat tentang had cas berbeza mengikut jenis bateri dan pengeluar, jadi ikut manual pemilik untuk kereta anda dan bukannya peraturan yang anda baca dalam talian. Jika anda tidak pasti apa yang sesuai untuk kereta dan cara pemanduan anda, tanya kami.',
                      '充电上限的建议因电池类型和厂家而异，所以请以您车辆的车主手册为准，而不是网上看到的某条规则。如果不确定什么适合您的车和驾驶方式，欢迎问我们。')),
                   (T('What does regular servicing add?', 'Apakah yang ditambah oleh servis berkala?', '定期保养能带来什么？'),
                    T('Dongfeng\'s service interval is every 10,000 km. Regular servicing at our 3S centre in Johor Bahru lets a technician look over the car on schedule, so small issues are caught early. Ask us what is covered at each visit for your model. High-voltage battery work should only ever be done by trained technicians, never at home.',
                      'Selang servis Dongfeng ialah setiap 10,000 km. Servis berkala di pusat 3S kami di Johor Bahru membolehkan juruteknik memeriksa kereta mengikut jadual, supaya masalah kecil dapat dikesan awal. Tanya kami apa yang dilindungi pada setiap lawatan untuk model anda. Kerja bateri voltan tinggi hanya boleh dilakukan oleh juruteknik terlatih, tidak pernah di rumah.',
                      '东风的保养周期为每 10,000 公里。在我们新山 3S 中心定期保养，技术人员可以按计划检查车辆，及早发现小问题。请向我们询问您的车型每次保养包含哪些项目。高压电池相关的作业只能由受过培训的技术人员进行，绝不能自己在家处理。'))],
         checks=[T('Park in shade or covered parking when you can, especially for long stops at midday', 'Letak kereta di tempat teduh atau tempat letak kereta berbumbung apabila boleh, terutamanya untuk berhenti lama pada waktu tengah hari', '尽量停在阴凉处或有顶的停车位，尤其是中午长时间停放'),
                 T('Use gentle home AC charging for everyday driving and save DC fast charging for longer trips', 'Guna pengecasan AC rumah yang lembut untuk pemanduan harian dan simpan pengecasan pantas DC untuk perjalanan lebih jauh', '日常以家用交流慢充为主，把直流快充留给较长的行程'),
                 T('Follow the charge-limit advice in your owner\'s manual', 'Ikut nasihat had cas dalam manual pemilik anda', '按车主手册里的充电上限建议操作'),
                 T('Avoid leaving the car for long periods at a very low charge', 'Elakkan membiarkan kereta lama dengan cas yang sangat rendah', '避免让车长时间处于很低的电量'),
                 T('Plug in rather than letting a hot car sit at a very high or very low charge for days', 'Cas kereta dan bukannya membiarkan kereta panas berada pada cas yang sangat tinggi atau sangat rendah selama beberapa hari', '不要让一辆很热的车连续几天停在过高或过低的电量，必要时接上充电')],
         faqs=[(T('Is Malaysia\'s heat bad for an EV battery?', 'Adakah cuaca panas Malaysia buruk untuk bateri EV?', '马来西亚的高温对电动车电池不好吗？'),
                T('Heat speeds up battery ageing in general, which is why habits like shade parking help. It does not stop you using the car every day. We cannot promise battery life, because it depends on how the car is used and charged.',
                  'Haba mempercepatkan penuaan bateri secara amnya, itulah sebabnya tabiat seperti meletak di tempat teduh membantu. Ia tidak menghalang anda menggunakan kereta setiap hari. Kami tidak boleh menjanjikan hayat bateri, kerana ia bergantung pada cara kereta digunakan dan dicas.',
                  '高温总体上会加快电池老化，所以停在阴凉处这类习惯会有帮助，但这不妨碍您每天用车。我们不能承诺电池寿命，因为它取决于车辆的使用和充电方式。')),
               (T('Do the Dongfeng Vigo and 007 use LFP batteries?', 'Adakah Dongfeng Vigo dan 007 menggunakan bateri LFP?', '东风 Vigo 和 007 用的是磷酸铁锂电池吗？'),
                T('Yes. The Vigo has a 51.87 kWh LFP battery and the 007 has a 73.48 kWh LFP battery, as listed on the model pages.',
                  'Ya. Vigo mempunyai bateri LFP 51.87 kWh dan 007 mempunyai bateri LFP 73.48 kWh, seperti disenaraikan di halaman model.',
                  '是的。Vigo 配 51.87 kWh 磷酸铁锂电池，007 配 73.48 kWh 磷酸铁锂电池，详见车型页面。')),
               (T('Should I avoid DC fast charging in hot weather?', 'Perlukah saya mengelak pengecasan pantas DC dalam cuaca panas?', '天气热时要避免直流快充吗？'),
                T('You do not need to avoid it. Use it when you need it, such as on a longer drive, and rely on slower AC charging at home for everyday use. The car manages the charging speed.',
                  'Anda tidak perlu mengelaknya. Gunakannya apabila perlu, seperti semasa perjalanan lebih jauh, dan bergantung pada pengecasan AC yang lebih perlahan di rumah untuk kegunaan harian. Kereta mengurus kelajuan pengecasan.',
                  '不需要刻意避免。需要时就用，比如较长的行程，日常使用则以家里较慢的交流充电为主。充电速度由车辆自行管理。')),
               (T('Where can I ask about my car\'s battery in Johor Bahru?', 'Di mana saya boleh bertanya tentang bateri kereta saya di Johor Bahru?', '在新山哪里可以咨询我的车的电池问题？'),
                T('Message our service team on WhatsApp or visit our 3S centre in Johor Bahru. Tell us the model and what you would like to know.',
                  'Mesej pasukan servis kami melalui WhatsApp atau lawati pusat 3S kami di Johor Bahru. Beritahu kami model dan apa yang anda ingin tahu.',
                  '可以通过 WhatsApp 联系我们的售后团队，或到新山 3S 中心。请告诉我们车型和您想了解的内容。'))]),
    # Night article 31 Oct 2026 (odd day; queue #6, MEDIUM). Official source: LTA OneMotoring "Cars and motorcycles registered in Malaysia" (page last updated 23 June 2026, read 31 Oct 2026).
    # No fee figures quoted (they change on 1 Jan 2027); no prices, no warranty terms, no competitors, no claim that we process permits.
    dict(slug='driving-an-ev-from-johor-bahru-to-singapore', photo='vigo-showroom', owner='models/', date='2026-10-31', share=True, checks_after=1,
         source=('https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/entering_and_exiting_singapore/cars-and-motorcycles-registered-in-malaysia.html',
                 T('Source: LTA OneMotoring, "Cars and motorcycles registered in Malaysia" (page last updated 23 June 2026, read on 31 October 2026)',
                   'Sumber: LTA OneMotoring, "Cars and motorcycles registered in Malaysia" (halaman dikemas kini 23 Jun 2026, dibaca pada 31 Oktober 2026)',
                   '来源：新加坡陆路交通管理局 LTA OneMotoring，“Cars and motorcycles registered in Malaysia”（页面最后更新于 2026 年 6 月 23 日，2026 年 10 月 31 日查阅）')),
         title=T('Driving an EV From Johor Bahru to Singapore: What to Check', 'Memandu EV Dari Johor Bahru ke Singapura: Apa Perlu Disemak', '从新山开电动车去新加坡：出发前要确认什么'),
         h1=T('What do you need to drive a Malaysia-registered EV from Johor Bahru into Singapore?', 'Apa yang anda perlukan untuk memandu EV berdaftar Malaysia dari Johor Bahru ke Singapura?', '开马来西亚车牌的电动车从新山进入新加坡，需要准备什么？'),
         desc=T('Before a Malaysia-registered car, electric or not, enters Singapore, LTA asks for VEP approval, an Autopass card, insurance and road tax. What to check first, with the official source.',
                'Sebelum kereta berdaftar Malaysia, elektrik atau tidak, memasuki Singapura, LTA meminta kelulusan VEP, kad Autopass, insurans dan cukai jalan. Apa yang perlu disemak dahulu, dengan sumber rasmi.',
                '马来西亚车牌的车进入新加坡前，无论是否电动车，LTA 要求 VEP 批准、Autopass 卡、保险和路税。出发前先确认什么，附官方来源。'),
         answer=T('According to LTA\'s OneMotoring page, a Malaysia-registered car must have LTA\'s VEP approval, an activated Autopass card, valid insurance and road tax before it enters Singapore, and LTA asks you to register at least 2 weeks before you travel. The page lists no separate step for electric cars. This is our reading as of 31 October 2026, so check the LTA page for your own case before you go.',
                  'Menurut laman OneMotoring LTA, kereta berdaftar Malaysia mesti mempunyai kelulusan VEP LTA, kad Autopass yang telah diaktifkan, insurans yang sah dan cukai jalan sebelum memasuki Singapura, dan LTA meminta anda mendaftar sekurang-kurangnya 2 minggu sebelum perjalanan. Laman itu tidak menyenaraikan langkah berasingan untuk kereta elektrik. Ini bacaan kami setakat 31 Oktober 2026, jadi semak laman LTA untuk kes anda sebelum bertolak.',
                  '根据 LTA OneMotoring 页面，马来西亚车牌的车进入新加坡前，必须有 LTA 的 VEP 批准、已激活的 Autopass 卡、有效保险和路税，LTA 并要求至少在出行前 2 周注册。该页面没有为电动车列出单独的步骤。以上是我们截至 2026 年 10 月 31 日的理解，出发前请就您的情况查看 LTA 页面。'),
         sections=[(T('Does an electric car need a VEP?', 'Adakah kereta elektrik memerlukan VEP?', '电动车需要 VEP 吗？'),
                    T('LTA\'s page for Malaysia-registered cars and motorcycles sets out one set of steps for cars, and we found no separate step for electric cars. So a Malaysia-registered EV such as the Dongfeng Vigo or 007 appears to be handled like any other Malaysia-registered car. Rules change, so read the LTA page again before each trip.',
                      'Laman LTA untuk kereta dan motosikal berdaftar Malaysia menyenaraikan satu set langkah untuk kereta, dan kami tidak menemui langkah berasingan untuk kereta elektrik. Maka EV berdaftar Malaysia seperti Dongfeng Vigo atau 007 nampaknya dikendalikan sama seperti kereta berdaftar Malaysia yang lain. Peraturan boleh berubah, jadi baca semula laman LTA sebelum setiap perjalanan.',
                      'LTA 针对马来西亚车牌汽车和摩托车的页面，只为汽车列出一套步骤，我们没有发现针对电动车的单独步骤。所以像东风 Vigo 或 007 这样的马来西亚车牌电动车，看起来和其他马来西亚车牌的车一样处理。规则可能变动，每次出行前请重新查看 LTA 页面。')),
                   (T('What does LTA ask you to have?', 'Apakah yang LTA minta anda sediakan?', 'LTA 要求您准备什么？'),
                    T('LTA lists these for a Malaysia-registered car entering Singapore, and says you must show them when officers ask:',
                      'LTA menyenaraikan perkara ini untuk kereta berdaftar Malaysia yang memasuki Singapura, dan menyatakan anda mesti menunjukkannya apabila pegawai meminta:',
                      'LTA 为进入新加坡的马来西亚车牌车辆列出以下项目，并表示执法人员要求时您必须出示：')),
                   (T('How early should you apply?', 'Berapa awal anda perlu memohon?', '要提前多久申请？'),
                    T('LTA says to register for an Autopass account on its VEP portal at least 2 weeks ahead of your travel. Once the VEP application is approved, you can pay for the Autopass card online and collect it. The card must be activated online before you bring the car into Singapore. LTA also says that from 2 November 2026, applications by foreign-registered vehicles with outstanding fines will not be accepted.',
                      'LTA menyatakan anda perlu mendaftar akaun Autopass di portal VEP sekurang-kurangnya 2 minggu sebelum perjalanan. Setelah permohonan VEP diluluskan, anda boleh membayar kad Autopass dalam talian dan mengambilnya. Kad mesti diaktifkan dalam talian sebelum anda membawa kereta ke Singapura. LTA juga menyatakan bahawa mulai 2 November 2026, permohonan oleh kenderaan berdaftar asing yang mempunyai saman tertunggak tidak akan diterima.',
                      'LTA 表示，应至少在出行前 2 周，在其 VEP 门户注册 Autopass 账户。VEP 申请获批后，可在线支付 Autopass 卡费用并领取。卡必须在把车开进新加坡之前在线激活。LTA 还表示，自 2026 年 11 月 2 日起，有未缴罚款的外国车牌车辆，其申请将不被受理。')),
                   (T('What about tolls and charges?', 'Bagaimana dengan tol dan caj?', '过路费和其他费用呢？'),
                    T('LTA lists entry and exit tolls, a road charge and VEP fees on the same page, and says the VEP fee rules change from 1 January 2027. We do not copy amounts here because they change. Read the current figures on the LTA page before you go.',
                      'LTA menyenaraikan tol masuk dan keluar, caj jalan dan yuran VEP pada laman yang sama, dan menyatakan peraturan yuran VEP berubah mulai 1 Januari 2027. Kami tidak menyalin jumlah di sini kerana ia berubah. Baca angka semasa di laman LTA sebelum bertolak.',
                      'LTA 在同一页面列出了入境和出境过路费、道路费和 VEP 费用，并表示 VEP 收费规则自 2027 年 1 月 1 日起调整。金额会变动，所以我们不在此抄录。出发前请查看 LTA 页面上的最新数字。')),
                   (T('What should you think about for the EV itself?', 'Apa yang perlu difikirkan tentang EV itu sendiri?', '关于电动车本身，要考虑什么？'),
                    T('Plan the trip around the car\'s range and where you will charge. The Dongfeng Vigo lists 471 km on the CLTC cycle and the 007 Premium up to 650 km on CLTC, as on our model pages. Real-world range depends on the variant, speed, weather, air-con and charger, so do not treat those figures as a promise. Check where you will charge in Singapore yourself, because this guide does not cover that.',
                      'Rancang perjalanan mengikut jarak kereta dan tempat anda akan mengecas. Dongfeng Vigo menyenaraikan 471 km pada kitaran CLTC dan 007 Premium sehingga 650 km pada CLTC, seperti di halaman model kami. Jarak sebenar bergantung pada varian, kelajuan, cuaca, penyaman udara dan pengecas, jadi jangan anggap angka itu sebagai janji. Semak sendiri tempat anda akan mengecas di Singapura, kerana panduan ini tidak merangkumnya.',
                      '请按车辆的续航和您的充电安排来规划行程。如我们车型页面所示，东风 Vigo 的 CLTC 续航为 471 公里，007 Premium 最高 650 公里（CLTC）。实际续航取决于车型版本、车速、天气、空调和充电桩，所以不要把这些数字当作承诺。在新加坡的充电地点请自行确认，本文不涵盖这部分。'))],
         checks=[T('The VEP approval email from LTA', 'E-mel kelulusan VEP daripada LTA', 'LTA 发出的 VEP 批准电邮'),
                 T('An Autopass card for that car, activated online before you enter', 'Kad Autopass untuk kereta itu, diaktifkan dalam talian sebelum anda masuk', '该车对应的 Autopass 卡，进入前已在线激活'),
                 T('An insurance certificate valid for use on Singapore roads', 'Sijil insurans yang sah untuk digunakan di jalan raya Singapura', '可在新加坡道路使用的有效保险证明'),
                 T('Road tax', 'Cukai jalan', '路税'),
                 T('The vehicle registration certificate', 'Sijil pendaftaran kenderaan', '车辆注册证')],
         faqs=[(T('Does an electric car need a VEP to enter Singapore?', 'Adakah kereta elektrik memerlukan VEP untuk memasuki Singapura?', '电动车进入新加坡需要 VEP 吗？'),
                T('LTA\'s page for Malaysia-registered cars lists VEP approval for cars and mentions no separate rule for electric cars. Check the LTA page for your own situation before you travel.',
                  'Laman LTA untuk kereta berdaftar Malaysia menyenaraikan kelulusan VEP untuk kereta dan tidak menyebut peraturan berasingan untuk kereta elektrik. Semak laman LTA untuk keadaan anda sebelum bertolak.',
                  'LTA 针对马来西亚车牌汽车的页面列出了汽车需要 VEP 批准，没有提到电动车的单独规定。出行前请就您的具体情况查看 LTA 页面。')),
               (T('Where do I apply for a VEP?', 'Di mana saya boleh memohon VEP?', '在哪里申请 VEP？'),
                T('LTA says to register for an Autopass account on its VEP portal. Follow the steps on the LTA page linked above. For questions about the car itself, ask our team on WhatsApp.',
                  'LTA menyatakan anda perlu mendaftar akaun Autopass di portal VEP mereka. Ikut langkah di laman LTA yang dipautkan di atas. Untuk soalan tentang kereta itu sendiri, tanya pasukan kami di WhatsApp.',
                  'LTA 表示要在其 VEP 门户注册 Autopass 账户。请按上面链接的 LTA 页面操作。关于车辆本身的问题，可以通过 WhatsApp 问我们的团队。')),
               (T('Are the fees different for electric cars?', 'Adakah yuran berbeza untuk kereta elektrik?', '电动车的费用不同吗？'),
                T('The LTA page does not list a separate fee for electric cars. Read the current fee table on the page, and note that VEP fee rules change from 1 January 2027.',
                  'Laman LTA tidak menyenaraikan yuran berasingan untuk kereta elektrik. Baca jadual yuran semasa pada laman itu, dan ambil perhatian bahawa peraturan yuran VEP berubah mulai 1 Januari 2027.',
                  'LTA 页面没有列出电动车的单独费用。请查看页面上的最新收费表，并注意 VEP 收费规则自 2027 年 1 月 1 日起调整。')),
               (T('Does this guide cover driving a Singapore car into Johor?', 'Adakah panduan ini merangkumi memandu kereta Singapura ke Johor?', '本文涵盖开新加坡车牌的车进入柔佛吗？'),
                T('No. It covers a Malaysia-registered car entering Singapore, based on LTA\'s page. For the other direction, check the official Malaysian sources.',
                  'Tidak. Ia merangkumi kereta berdaftar Malaysia yang memasuki Singapura, berdasarkan laman LTA. Untuk arah sebaliknya, semak sumber rasmi Malaysia.',
                  '不涵盖。本文依据 LTA 页面，讲的是马来西亚车牌的车进入新加坡。反方向的情况请查看马来西亚官方来源。'))]),
    # Night article 2 Nov 2026 (every-2-days rule; queue #9, MEDIUM). Official source: LHDN "Tax Relief" table (hasil.gov.my, page metadata modified 26 June 2026, read 2 Nov 2026).
    # Only the item LHDN lists (EV charging facility expenses, RM2,500 restricted, not for business use, YA 2022-2025 on the page read). No prices, no tax advice, no car-purchase incentive claims, no savings promises.
    dict(slug='ev-charging-tax-relief-malaysia', photo='vigo-dash', owner='models/', date='2026-11-02', share=True, checks_after=3,
         source=('https://www.hasil.gov.my/en/?p=8298',
                 T('Source: LHDN (Inland Revenue Board of Malaysia), "Tax Relief" table, hasil.gov.my (page last modified 26 June 2026, read on 2 November 2026)',
                   'Sumber: LHDN (Lembaga Hasil Dalam Negeri), jadual "Pelepasan Cukai", hasil.gov.my (halaman diubah suai 26 Jun 2026, dibaca pada 2 November 2026)',
                   '来源：马来西亚内陆税收局 LHDN，“税务减免”（Tax Relief）表，hasil.gov.my（页面最后修改于 2026 年 6 月 26 日，2026 年 11 月 2 日查阅）')),
         title=T('EV Home Charger Tax Relief in Malaysia: What LHDN Lists', 'Pelepasan Cukai Pengecas EV di Rumah: Apa Yang LHDN Senaraikan', '电动车家用充电设施税务减免：LHDN 列出了什么'),
         h1=T('Is there an income tax relief for EV charging facilities in Malaysia?', 'Adakah terdapat pelepasan cukai pendapatan untuk kemudahan pengecasan EV di Malaysia?', '马来西亚有针对电动车充电设施的个人所得税减免吗？'),
         desc=T('LHDN\'s tax relief table lists expenses on EV charging facilities (RM2,500, restricted, not for business use). What it says, what it does not say, and where to check.',
                'Jadual pelepasan cukai LHDN menyenaraikan perbelanjaan kemudahan pengecasan EV (RM2,500, terhad, bukan untuk kegunaan perniagaan). Apa yang dinyatakan, apa yang tidak, dan di mana untuk menyemak.',
                'LHDN 的税务减免表列出电动车充电设施开支（RM2,500，设上限，不适用于业务用途）。它说了什么、没说什么，以及到哪里核实。'),
         answer=T('Yes. LHDN\'s tax relief table lists "expenses on charging facilities for Electric Vehicle (not for business use)" as an individual relief of up to RM2,500 (marked "restricted") for years of assessment 2022 to 2025. The table gives no other conditions, so check LHDN or a tax adviser on what counts and which year applies to you. This is our reading as of 2 November 2026, not tax advice.',
                  'Ya. Jadual pelepasan cukai LHDN menyenaraikan "perbelanjaan untuk kemudahan pengecasan Kenderaan Elektrik (bukan untuk kegunaan perniagaan)" sebagai pelepasan individu sehingga RM2,500 (ditanda "terhad") untuk tahun taksiran 2022 hingga 2025. Jadual itu tidak memberikan syarat lain, jadi semak dengan LHDN atau penasihat cukai tentang apa yang layak dan tahun mana yang terpakai kepada anda. Ini bacaan kami setakat 2 November 2026, bukan nasihat cukai.',
                  '有。LHDN 的税务减免表把“电动车充电设施开支（不适用于业务用途）”列为个人减免，2022 至 2025 评税年最高 RM2,500（标注为“受限”）。该表没有给出其他条件，所以哪些开支符合、适用哪个评税年，请向 LHDN 或税务顾问确认。以上是我们截至 2026 年 11 月 2 日的理解，不构成税务建议。'),
         sections=[(T('What does the LHDN table actually say?', 'Apa sebenarnya yang dinyatakan oleh jadual LHDN?', 'LHDN 的表格到底写了什么？'),
                    T('On its Tax Relief page, LHDN lists item 21 as "expenses on charging facilities for Electric Vehicle (not for business use)" with an amount of RM2,500, marked "restricted", meaning the claim is capped. For year of assessment 2025 the same item also covers domestic food waste composting machines. We saw the item in the tables for years of assessment 2022, 2023, 2024 and 2025.',
                      'Pada laman Pelepasan Cukainya, LHDN menyenaraikan item 21 sebagai "perbelanjaan untuk kemudahan pengecasan Kenderaan Elektrik (bukan untuk kegunaan perniagaan)" dengan jumlah RM2,500, ditanda "terhad", bermaksud tuntutan dihadkan. Bagi tahun taksiran 2025 item yang sama juga merangkumi mesin pengkomposan sisa makanan domestik. Kami melihat item itu dalam jadual tahun taksiran 2022, 2023, 2024 dan 2025.',
                      'LHDN 在其税务减免页面把第 21 项列为“电动车充电设施开支（不适用于业务用途）”，金额 RM2,500，标注为“受限”，即有上限。2025 评税年的同一项还包括家用厨余堆肥机。我们在 2022、2023、2024 和 2025 评税年的表格中都看到了这一项。')),
                   (T('What does the table not tell you?', 'Apa yang tidak diberitahu oleh jadual itu?', '这张表没有告诉您什么？'),
                    T('The table is a summary. In the version we read, it does not say which costs count (for example buying, installing or renting a charger), what proof you must keep, or whether the relief continues for later years of assessment. We have not found those details on the page, so we do not state them here. Ask LHDN or a tax adviser before you rely on it.',
                      'Jadual itu hanyalah ringkasan. Dalam versi yang kami baca, ia tidak menyatakan kos mana yang layak (contohnya membeli, memasang atau menyewa pengecas), bukti apa yang perlu disimpan, atau sama ada pelepasan itu berterusan untuk tahun taksiran seterusnya. Kami tidak menemui butiran itu pada laman tersebut, jadi kami tidak menyatakannya di sini. Tanya LHDN atau penasihat cukai sebelum anda bergantung padanya.',
                      '这张表只是摘要。在我们阅读的版本中，它没有说明哪些费用算数（例如购买、安装或租用充电设备）、需要保留什么凭证，也没有说明该减免是否延续到之后的评税年。我们没有在该页面找到这些细节，所以不在此陈述。依赖它之前，请先向 LHDN 或税务顾问确认。')),
                   (T('Who can claim it?', 'Siapa yang boleh menuntutnya?', '谁可以申报？'),
                    T('It is an individual income tax relief, so it concerns people who file Malaysian income tax. It says "not for business use", so a charger bought for a company or a business does not fall under this line. Whether it applies to you depends on your own tax position, which we cannot assess.',
                      'Ia ialah pelepasan cukai pendapatan individu, jadi ia berkaitan dengan orang yang memfailkan cukai pendapatan Malaysia. Ia menyatakan "bukan untuk kegunaan perniagaan", jadi pengecas yang dibeli untuk syarikat atau perniagaan tidak termasuk dalam baris ini. Sama ada ia terpakai kepada anda bergantung pada kedudukan cukai anda sendiri, yang tidak dapat kami nilai.',
                      '这是个人所得税减免，所以和在马来西亚申报个人所得税的人有关。表中写明“不适用于业务用途”，因此为公司或生意购买的充电设备不属于这一项。是否适用于您，取决于您自己的税务情况，我们无法评估。')),
                   (T('What should you keep if you plan to claim?', 'Apa yang perlu anda simpan jika bercadang untuk menuntut?', '打算申报的话，应该保留什么？'),
                    T('Keeping your paperwork is sensible for any relief. Until LHDN or your adviser confirms what it needs, keep these:',
                      'Menyimpan dokumen anda adalah wajar untuk apa-apa pelepasan. Sehingga LHDN atau penasihat anda mengesahkan apa yang diperlukan, simpan perkara ini:',
                      '对任何减免，保留文件都是明智之举。在 LHDN 或您的顾问确认需要什么之前，建议保留：')),
                   (T('Where does the dealership fit in?', 'Di mana peranan pengedar?', '经销商在其中扮演什么角色？'),
                    T('We are a car centre, not a tax adviser, so we cannot tell you whether your expense qualifies or how much you can claim. We can tell you about the Dongfeng Vigo and 007 charging figures on our model pages, and our guide to charging an EV at home in Johor covers the practical side of a home charger.',
                      'Kami ialah pusat kereta, bukan penasihat cukai, jadi kami tidak boleh memberitahu sama ada perbelanjaan anda layak atau berapa banyak yang boleh dituntut. Kami boleh menerangkan angka pengecasan Dongfeng Vigo dan 007 di halaman model kami, dan panduan kami tentang mengecas EV di rumah di Johor merangkumi sisi praktikal pengecas rumah.',
                      '我们是汽车中心，不是税务顾问，所以无法告诉您开支是否符合条件或可以申报多少。Vigo 和 007 的充电数据可以在我们的车型页面查到，我们那篇“在柔佛家里给电动车充电”的指南讲了家用充电的实际问题。'))],
         checks=[T('The invoice or receipt for the charging facility, with the date', 'Invois atau resit untuk kemudahan pengecasan, dengan tarikh', '充电设施的发票或收据，注明日期'),
                 T('Proof of payment', 'Bukti pembayaran', '付款凭证'),
                 T('Any installation or rental agreement', 'Apa-apa perjanjian pemasangan atau sewa', '任何安装或租用合同'),
                 T('A note of the year of assessment you are claiming it in', 'Catatan tahun taksiran yang anda tuntut', '注明您申报的评税年'),
                 T('LHDN\'s reply or your adviser\'s confirmation of what qualifies', 'Jawapan LHDN atau pengesahan penasihat anda tentang apa yang layak', 'LHDN 的答复或您的顾问对符合条件开支的确认')],
         faqs=[(T('How much is the EV charging relief in Malaysia?', 'Berapakah pelepasan pengecasan EV di Malaysia?', '马来西亚的电动车充电减免是多少？'),
                T('LHDN\'s tax relief table shows RM2,500 for expenses on EV charging facilities, marked "restricted", which means it is capped. It is a deduction from taxable income, not a refund of RM2,500.',
                  'Jadual pelepasan cukai LHDN menunjukkan RM2,500 untuk perbelanjaan kemudahan pengecasan EV, ditanda "terhad", bermaksud ia dihadkan. Ia ialah potongan daripada pendapatan bercukai, bukan bayaran balik RM2,500.',
                  'LHDN 税务减免表显示电动车充电设施开支为 RM2,500，标注“受限”，即设有上限。它是从应税收入中扣除，不是返还 RM2,500。')),
               (T('Can a company claim it?', 'Bolehkah syarikat menuntutnya?', '公司可以申报吗？'),
                T('The line is an individual relief and says "not for business use". For business expenses, ask your tax adviser.',
                  'Baris ini ialah pelepasan individu dan menyatakan "bukan untuk kegunaan perniagaan". Untuk perbelanjaan perniagaan, tanya penasihat cukai anda.',
                  '这一项是个人减免，并注明“不适用于业务用途”。企业开支请咨询您的税务顾问。')),
               (T('Does the relief apply to 2026 and later?', 'Adakah pelepasan ini terpakai untuk 2026 dan seterusnya?', '这项减免适用于 2026 年及之后吗？'),
                T('The tables we read on LHDN\'s page show it for years of assessment 2022 to 2025. We did not find a table for later years on the version we read, so check LHDN for the year you are filing.',
                  'Jadual yang kami baca pada laman LHDN menunjukkannya untuk tahun taksiran 2022 hingga 2025. Kami tidak menemui jadual untuk tahun seterusnya pada versi yang kami baca, jadi semak LHDN untuk tahun yang anda failkan.',
                  '我们在 LHDN 页面读到的表格显示它适用于 2022 至 2025 评税年。在我们阅读的版本中没有找到之后年份的表格，所以请就您申报的年份向 LHDN 核实。')),
               (T('Does Dongfeng Johor Bahru give tax advice?', 'Adakah Dongfeng Johor Bahru memberi nasihat cukai?', '东风新山提供税务建议吗？'),
                T('No. We can answer questions about the cars and charging figures on our model pages. For tax, ask LHDN or a qualified tax adviser.',
                  'Tidak. Kami boleh menjawab soalan tentang kereta dan angka pengecasan di halaman model kami. Untuk cukai, tanya LHDN atau penasihat cukai yang bertauliah.',
                  '不提供。关于车辆和车型页面上的充电数据，我们可以解答。税务问题请咨询 LHDN 或合资格的税务顾问。'))]),
]
ART = {a['slug']: a for a in ARTICLES}
# Per-page lastmod (sitemap + WebPage dateModified): dated articles carry their own date; pages they change are listed here (21 Oct 2026).
LASTMOD = {'articles/%s/' % a['slug']: a['date'] for a in ARTICLES if a.get('date')}
LASTMOD['articles/'] = '2026-11-02'
LASTMOD['test-drive/'] = '2026-11-05'  # title/desc + model/service links (GSC quick win)
LASTMOD['service/'] = '2026-10-28'  # service-specific closing block (ChatGPT bridge draft)

FAQ_HOME = [
    (T('Where is the Dongfeng showroom in Johor Bahru?', 'Di manakah bilik pameran Dongfeng di Johor Bahru?', '新山的东风展厅在哪里？'),
     T('Our 3S centre is at No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru. WhatsApp +60 18-762 0828 before you come so we can have the car you want ready.',
       'Pusat 3S kami di No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru. WhatsApp +60 18-762 0828 sebelum datang supaya kereta yang anda mahu sudah sedia.',
       '我们的 3S 中心位于81100 新山 Taman Ekoperniagaan, Jalan Ekoperniagaan 3/11 门牌 28 号。来之前请 WhatsApp +60 18-762 0828，我们会提前把您想看的车准备好。')),
    (T('Which Dongfeng models can I buy in Johor?', 'Model Dongfeng mana boleh dibeli di Johor?', '在柔佛可以买到哪些东风车型？'),
     T('We sell Dongfeng passenger EVs: the Dongfeng Vigo electric SUV and the Dongfeng 007 electric sedan.',
       'Kami menjual kereta penumpang elektrik Dongfeng: Dongfeng Vigo SUV elektrik dan Dongfeng 007 sedan elektrik.',
       '我们销售东风纯电乘用车：东风 Vigo 纯电 SUV 和东风 007 纯电轿跑。')),
    (T('How do I book a test drive?', 'Bagaimana tempah pandu uji?', '怎么预约试驾？'),
     T('WhatsApp us with the model and a day and time that suit you. We confirm the slot and have the car charged and ready.',
       'WhatsApp kami dengan model, hari dan masa yang sesuai. Kami sahkan slot dan sediakan kereta yang sudah dicas.',
       'WhatsApp 我们，告诉我们车型和方便的日期时间。我们确认时段后，会把车充好电等您。')),
    (T('Why are prices not on the website?', 'Mengapa harga tiada di laman web?', '网站上为什么没有价格？'),
     T('Prices and offers change, so we give you the current figure directly. WhatsApp us and ask.',
       'Harga dan tawaran berubah, jadi kami berikan angka semasa terus kepada anda. WhatsApp dan tanya kami.',
       '价格和优惠会变动，我们会直接给您最新报价。欢迎 WhatsApp 询问。')),
]

ROADSHOWS = [T('AEON Mall Bandar Dato\' Onn', 'AEON Mall Bandar Dato\' Onn', 'AEON Mall Bandar Dato\' Onn'),
             T('Lotus\'s Tebrau', 'Lotus\'s Tebrau', 'Lotus\'s Tebrau'),
             T('Sutera Mall', 'Sutera Mall', 'Sutera Mall'),
             T('KIPMall Kota Tinggi', 'KIPMall Kota Tinggi', 'KIPMall Kota Tinggi')]

# ---------------------------------------------------------------------------------------------
# Page bodies
# ---------------------------------------------------------------------------------------------
PAGES = {}  # (L, path) -> dict


import importlib.util as _ilu
_sp = _ilu.spec_from_file_location('seo_extra', os.path.join(HERE, 'seo_extra.py'))
_sm = _ilu.module_from_spec(_sp)
_sp.loader.exec_module(_sm)
XTRA = _sm.EXTRA
TAIL = {'en': ' WhatsApp +60 18-762 0828.', 'ms': ' WhatsApp +60 18-762 0828.', 'zh': 'WhatsApp +60 18-762 0828，欢迎预约试驾。'}


def fit_title(s):
    """Titles <= 65 chars: shorten the brand suffix first (Dongfeng Johor Bahru -> Dongfeng JB), then drop it."""
    if len(s) <= 65:
        return s
    s2 = s.replace(' | Dongfeng Johor Bahru', ' | Dongfeng JB')
    if len(s2) <= 65:
        return s2
    return s2.split(' | ')[0] if len(s2.split(' | ')[0]) <= 65 else s2


def fit_desc(d, L):
    """EN/BM 120-160 chars; ZH at least 70 characters (CJK is denser)."""
    if L == 'zh':
        if len(d) < 70:
            d += ('' if d.endswith(('。', '.')) else '。') + TAIL['zh']
        return d
    if len(d) < 120 and TAIL[L].strip() not in d:
        d += TAIL[L]
    if len(d) > 160:
        cut = d[:159]
        for sep in ('. ', ': ', '; ', ', ', ' '):
            i = cut.rfind(sep)
            if i >= 120:
                cut = cut[:i]
                break
        d = cut.rstrip(' ,;:') + '.'
    return d


def page(L, path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, photo=None, kind='website'):
    title, desc = fit_title(t(title, L)), fit_desc(t(desc, L), L)
    schema = list(schema or [])
    ex = XTRA.get(path)
    if ex:
        pre_h = '<section class="sec"><div class="wrap"><div class="prose">%s</div></div></section>' % ''.join('<p>%s</p>' % E(t(x, L)) for x in ex['intro']) if ex.get('intro') else ''
        post_h = ''
        if ex.get('more'):
            post_h += '<section class="sec"><div class="wrap"><div class="prose">%s</div></div></section>' % ''.join('<p>%s</p>' % E(t(x, L)) for x in ex['more'])
        if ex.get('faqs'):
            post_h += '<section class="sec"><div class="wrap"><div class="prose"><h2>%s</h2>%s</div></div></section>' % (E(t(T('Common questions', 'Soalan lazim', '常见问题'), L)), faq_html(ex['faqs'], L))
            schema.append(faq_schema(ex['faqs'], L))
        body = pre_h + body + post_h
    PAGES[(L, path)] = dict(title=t(title, L), desc=t(desc, L), h1=t(h1, L), body=body, crumbs=crumbs, lede=t(lede, L) if lede else '',
                            schema=schema or [], hero=hero, cta=cta, photo=photo, kind=kind)


def model_card(m, L):
    return ('<a class="mcard" href="models/%s/"><div class="mc-img">%s</div><div class="mc-body"><span class="tag">%s</span><h3>%s</h3><p>%s</p><span class="more">%s</span></div></a>') % (
        m['slug'], img(m.get('card', m['photo']), L), E(t(m['tag'], L)), E(m['name']), E(t(m['short'], L)), E(t(W['more'], L)))


def article_card(a, L):
    return '<a class="acard" href="articles/%s/"><figure>%s</figure><div><h3>%s</h3><p>%s</p><span class="more">%s</span></div></a>' % (
        a['slug'], img(a['photo'], L), E(t(a['h1'], L)), E(t(a['desc'], L)), E(t(W['read'], L)))


S3 = [  # the three S
    ('models/', T('01 · Sales', '01 · Jualan', '01 · 销售'), T('New Dongfeng EVs', 'EV Dongfeng baharu', '东风新车'),
     T('See the Vigo and 007 in our showroom and book a test drive.', 'Lihat Vigo dan 007 di bilik pameran kami dan tempah pandu uji.', '在展厅看 Vigo 和 007，并预约试驾。')),
    ('service/', T('02 · Service', '02 · Servis', '02 · 售后服务'), T('Servicing by the brand\'s team', 'Servis oleh pasukan jenama', '品牌团队保养'),
     T('Bring your Dongfeng back to the people who sold it to you.', 'Bawa Dongfeng anda kembali kepada pasukan yang menjualnya.', '保养回到卖车给您的团队。')),
    ('spare-parts/', T('03 · Spare parts', '03 · Alat ganti', '03 · 零配件'), T('Dongfeng parts in Johor', 'Alat ganti Dongfeng di Johor', '柔佛东风配件'),
     T('Parts for Dongfeng cars, ordered and fitted through our centre.', 'Alat ganti kereta Dongfeng, ditempah dan dipasang melalui pusat kami.', '东风车型配件，经由我们中心订购与安装。')),
]


def home_body(L):
    facts = [(T('3S centre', 'Pusat 3S', '3S 中心'), T('Sales · Service · Spare parts', 'Jualan · Servis · Alat ganti', '销售 · 服务 · 配件')),
             (T('First in JB', 'Pertama di JB', '新山首家'), T('Dongfeng 3S centre in Johor Bahru', 'Pusat 3S Dongfeng di Johor Bahru', '东风 3S 中心')),
             (T('2 models', '2 model', '2 款车型'), T('Vigo SUV and 007 sedan', 'SUV Vigo dan sedan 007', 'Vigo SUV 与 007 轿跑')),
             (T('Test drive', 'Pandu uji', '试驾'), T('Book on WhatsApp', 'Tempah di WhatsApp', 'WhatsApp 预约'))]
    hero = ('<section class="hero"><div class="wrap"><span class="eyebrow">%s</span><h1>%s</h1><p class="lede">%s</p><div class="cta-row">%s'
            '<a class="btn btn-ghost" href="models/">%s</a></div><div class="stage">%s</div><div class="hero-facts">%s</div></div></section>') % (
        E(t(W['tagline'], L)),
        E(t(T('Dongfeng electric cars in Johor Bahru', 'Kereta elektrik Dongfeng di Johor Bahru', '新山东风纯电汽车'), L)),
        E(t(T('The first Dongfeng 3S centre in Johor Bahru: sales, service and spare parts under one roof in Taman Ekoperniagaan. Come and see the Vigo and the 007.',
              'Pusat 3S Dongfeng pertama di Johor Bahru: jualan, servis dan alat ganti di bawah satu bumbung di Taman Ekoperniagaan. Datang lihat Vigo dan 007.',
              '新山首家东风 3S 中心：销售、售后服务、零配件一站式，位于 Taman Ekoperniagaan。欢迎来看 Vigo 和 007。'), L)),
        wa_btn(L), E(t(W['explore'], L)), img('hero', L, eager=True),
        ''.join('<div><b>%s</b><span>%s</span></div>' % (E(t(a, L)), E(t(b, L))) for a, b in facts))
    models = '<section class="sec"><div class="wrap">%s<div class="models">%s</div></div></section>' % (
        sec_head(T('The models', 'Model', '车型'), T('Two Dongfeng EVs, ready to drive', 'Dua EV Dongfeng, sedia dipandu', '两款东风纯电车，随时试驾'),
                 T('Colours and versions in the showroom change; ask us what is in stock today.', 'Warna dan versi di bilik pameran berubah; tanya kami stok hari ini.', '展厅颜色和版本会变动，欢迎询问当日现车。'), L),
        ''.join(model_card(m, L) for m in MODELS) + upcoming_card(L))
    gallery = '<section class="sec sec-dark" style="padding-bottom:40px"><div class="wrap">%s</div>%s</section>' % (
        sec_head(T('Inside the showroom', 'Di bilik pameran', '展厅实拍'), T('Come and sit in them', 'Datang dan cuba duduk', '欢迎进来坐一坐'),
                 T('Real photos from our Johor Bahru 3S centre.', 'Foto sebenar dari pusat 3S kami di Johor Bahru.', '新山 3S 中心实拍照片。'), L),
        glide(['vigo-showroom', '007-showroom', 'vigo-cabin', 'cabin-quilted', 'vigo-dash', 'showroom-front', 'pair-skyline'], L,
              [T('Dongfeng Vigo', 'Dongfeng Vigo', '东风 Vigo'), T('Dongfeng 007', 'Dongfeng 007', '东风 007'), T('Vigo cabin', 'Kabin Vigo', 'Vigo 座舱'),
               T('Quilted trim', 'Kemasan berjahit', '绗缝内饰'), T('Vigo dashboard', 'Papan pemuka Vigo', 'Vigo 仪表台'),
               T('Our showroom, Taman Ekoperniagaan', 'Bilik pameran kami, Taman Ekoperniagaan', '我们的展厅，Taman Ekoperniagaan'), T('Vigo and 007', 'Vigo dan 007', 'Vigo 与 007')]))
    s3 = '<section class="sec"><div class="wrap">%s<div class="cards">%s</div></div></section>' % (
        sec_head(T('One roof', 'Satu bumbung', '一站式'), T('Sales, service and spare parts', 'Jualan, servis dan alat ganti', '销售、服务、配件'), None, L),
        ''.join('<a class="card" href="%s"><span class="num">%s</span><h3>%s</h3><p>%s</p><span class="more">%s</span></a>' % (
            h, E(t(n, L)), E(t(a, L)), E(t(b, L)), E(t(W['more'], L))) for h, n, a, b in S3))
    partner = ('<section class="sec sec-white"><div class="wrap split"><figure>%s</figure><div><span class="eyebrow">%s</span><h2>%s</h2><p>%s</p>'
               '<a class="btn btn-dark" href="partners/">%s</a></div></div></section>') % (
        img('showroom-front', L), E(t(T('Partners', 'Rakan niaga', '合作伙伴'), L)),
        E(t(T('Dealers and brands: work with us in Johor', 'Pengedar dan jenama: bekerjasama dengan kami di Johor', '经销商与品牌：与我们在柔佛合作'), L)),
        E(t(T('We run a brand 3S centre in Johor Bahru and take EVs to malls across the state. If you are a dealer or a brand looking for a partner in Johor, talk to us.',
              'Kami mengendalikan pusat 3S jenama di Johor Bahru dan membawa EV ke pusat beli-belah di seluruh negeri. Jika anda pengedar atau jenama yang mencari rakan di Johor, hubungi kami.',
              '我们在新山经营品牌 3S 中心，也把电动车带到柔佛各地商场巡展。如果您是寻找柔佛合作伙伴的经销商或品牌，欢迎联系。'), L)),
        E(t(T('Partner with us', 'Jadi rakan niaga', '洽谈合作'), L)))
    road = ('<section class="sec sec-dark"><div class="wrap split"><div><span class="eyebrow">%s</span><h2>%s</h2><p>%s</p><ul class="chips">%s</ul></div>'
            '<figure>%s</figure></div></section>') % (
        E(t(T('Across Johor', 'Seluruh Johor', '遍布柔佛'), L)),
        E(t(T('Roadshows and community days', 'Jelajah dan hari komuniti', '商场巡展与社区活动'), L)),
        E(t(T('We bring the cars to you. In 2026 we have shown Dongfeng EVs at malls around Johor and hosted a Merdeka costume day for children at the showroom. Follow our Facebook page for the next one.',
              'Kami bawa kereta kepada anda. Pada 2026 kami mempamerkan EV Dongfeng di pusat beli-belah sekitar Johor dan menganjurkan hari kostum Merdeka untuk kanak-kanak di bilik pameran. Ikuti Facebook kami untuk acara seterusnya.',
              '我们把车带到您身边。2026 年我们在柔佛多个商场展出东风电动车，并在展厅举办了国庆儿童服装日。关注我们的 Facebook，留意下一场活动。'), L)),
        ''.join('<li>%s</li>' % E(t(r, L)) for r in ROADSHOWS), img('merdeka-2026', L))
    arts = '<section class="sec"><div class="wrap">%s<div class="acards">%s</div></div></section>' % (
        sec_head(T('EV guides', 'Panduan EV', 'EV 指南'), T('Straight answers before you buy', 'Jawapan jelas sebelum membeli', '买车前的实用解答'), None, L),
        ''.join(article_card(a, L) for a in ARTICLES[:3]))
    faq = '<section class="sec sec-white"><div class="wrap">%s%s</div></section>' % (
        sec_head(W['faq_h'], T('Good to know', 'Perlu tahu', '您可能想知道'), None, L), faq_html(FAQ_HOME, L))
    return hero + models + gallery + s3 + partner + road + arts + faq + visit_block(L)


def visit_block(L):
    return ('<section class="sec"><div class="wrap">%s<div class="visit"><div class="info"><dl>'
            '<dt>%s</dt><dd>%s<br><a href="%s" target="_blank" rel="noopener">%s</a> · <a href="%s" target="_blank" rel="noopener">%s</a></dd>'
            '<dt>%s</dt><dd>%s<br>%s</dd>'
            '<dt>%s</dt><dd>%s<br>%s</dd>'
            '<dt>%s</dt><dd><a href="%s" target="_blank" rel="noopener">%s</a><br><small>%s</small></dd>'
            '<dt>%s</dt><dd><a href="%s" target="_blank" rel="noopener">%s</a><br><small>%s</small></dd>'
            '<dt>Email</dt><dd>%s: <a href="mailto:%s">%s</a><br>%s: <a href="mailto:%s">%s</a></dd>'
            '<dt>%s</dt><dd>%s</dd></dl><div class="cta-row" style="margin-top:22px">%s</div></div>'
            '<iframe src="%s" loading="lazy" title="%s" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div></section>') % (
        sec_head(T('Visit', 'Kunjungi', '到访'), T('Find us in Eco Business Park 1, Johor Bahru', 'Cari kami di Eco Business Park 1, Johor Bahru', '新山 Eco Business Park 1 欢迎您'), None, L),
        E(t(T('Showroom', 'Bilik pameran', '展厅'), L)), '<br>'.join(E(a) for a in ADDR), E(MAP), E(t(T('Open in Google Maps', 'Buka di Google Maps', '在 Google 地图打开'), L)),
        E(GBP), E(t(T('Our Google reviews', 'Ulasan Google kami', '我们的 Google 评价'), L)),
        E(t(T('Showroom hours', 'Waktu bilik pameran', '展厅营业时间'), L)),
        E(t(T('Monday to Saturday: 9am to 6pm', 'Isnin hingga Sabtu: 9 pagi hingga 6 petang', '周一至周六：上午 9 点至下午 6 点'), L)),
        E(t(T('Sunday: 10am to 4pm', 'Ahad: 10 pagi hingga 4 petang', '周日：上午 10 点至下午 4 点'), L)),
        E(t(T('Workshop hours', 'Waktu bengkel', '维修车间时间'), L)),
        E(t(T('Monday to Friday: 9am to 6pm', 'Isnin hingga Jumaat: 9 pagi hingga 6 petang', '周一至周五：上午 9 点至下午 6 点'), L)),
        E(t(T('Saturday: 9am to 1pm · Sunday: closed', 'Sabtu: 9 pagi hingga 1 petang · Ahad: tutup', '周六：上午 9 点至下午 1 点 · 周日休息'), L)),
        E(t(W['sales_wa'], L)), E(wa_url(L, t(T('new cars and promotions.', 'kereta baharu dan promosi.', '新车与优惠。'), L))), E(WA_SHOW), E(t(W['sales_sub'], L)),
        E(t(W['svc_wa'], L)), E(wa_url(L, svc=True)), E(SVC_SHOW), E(t(W['svc_sub'], L)),
        E(t(T('Sales', 'Jualan', '销售'), L)), EMAIL, EMAIL, E(t(T('Aftersales', 'Selepas jualan', '售后'), L)), SVC_EMAIL, SVC_EMAIL,
        E(t(T('Visits', 'Lawatan', '到访提示'), L)),
        E(t(T('WhatsApp us before you come so the car you want is ready. Closed on some public holidays; we post notices on Facebook.',
              'WhatsApp kami sebelum datang supaya kereta yang anda mahu sudah sedia. Tutup pada sesetengah cuti umum; notis di Facebook.',
              '来之前请先 WhatsApp，我们会把车准备好。部分公共假期休息，会在 Facebook 公告。'), L)),
        wa_pair(L), E(MAP_EMBED), E(t(T('Map to Dongfeng Johor Bahru', 'Peta ke Dongfeng Johor Bahru', '东风新山地图'), L)))


def upcoming_card(L):
    v = VOYAH
    return ('<a class="mcard soon" href="models/%s/"><div class="mc-img">%s<span class="badge">%s</span></div><div class="mc-body"><span class="tag">%s</span><h3>%s</h3><p>%s</p><span class="more">%s</span></div></a>') % (
        v['slug'], img(v['card'], L), E(t(T('Coming soon', 'Akan datang', '即将上市'), L)), E(t(v['tag'], L)), E(v['name']), E(t(v['short'], L)), E(t(W['more'], L)))


def voyah_body(L):
    v = VOYAH
    rows = ''.join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (E(t(a, L)), E(t(b, L))) for a, b in v['facts'])
    reg = t(T('the Voyah Dream. Please register my interest.', 'Voyah Dream. Sila daftar minat saya.', '岚图梦想家 Voyah Dream，请帮我登记意向。'), L)
    return ('<section class="sec"><div class="wrap split"><div><span class="eyebrow">%s</span><h2>%s</h2><p class="answer">%s</p><div class="cta-row">%s</div></div>'
            '<figure>%s</figure></div></section>'
            '<section class="sec sec-dark" style="padding-bottom:40px"><div class="wrap">%s</div>%s</section>'
            '<section class="sec sec-white"><div class="wrap">%s<div class="tbl"><table class="spec"><tbody>%s</tbody></table></div><p class="note" style="margin-top:12px">%s</p>'
            '<p>%s <a href="models/vigo/">Dongfeng Vigo</a> · <a href="models/007/">Dongfeng 007</a></p></div></section>'
            '<section class="sec"><div class="wrap">%s%s</div></section>') % (
        E(t(v['tag'], L)), E(t(T('What is the Voyah Dream?', 'Apa itu Voyah Dream?', '岚图梦想家是什么车？'), L)), E(t(v['answer'], L)),
        wa_btn(L, label=t(T('Register your interest', 'Daftar minat', '登记意向'), L), topic=reg), img('voyah-door', L),
        sec_head(T('Photos', 'Foto', '照片'), T('The Voyah Dream', 'Voyah Dream', '岚图梦想家'), T('Official Voyah photos. The car for Malaysia may differ.', 'Foto rasmi Voyah. Kereta untuk Malaysia mungkin berbeza.', '岚图官方图片，马来西亚版本可能有所不同。'), L),
        glide(v['gallery'], L, label=T('Voyah Dream photos', 'Foto Voyah Dream', '岚图梦想家照片')),
        sec_head(T('What we know', 'Apa yang kami tahu', '目前已知'), T('Confirmed so far', 'Disahkan setakat ini', '目前已确认'), None, L), rows,
        E(t(T('Source: Dongfeng Malaysia\'s preview at KLIMS 2026, as reported by the Malaysian motoring press (June 2026). We will add Malaysian specifications when they are announced.',
              'Sumber: pratonton Dongfeng Malaysia di KLIMS 2026, seperti dilaporkan media automotif Malaysia (Jun 2026). Kami akan tambah spesifikasi Malaysia apabila diumumkan.',
              '来源：东风马来西亚 KLIMS 2026 预览，据马来西亚汽车媒体报道（2026 年 6 月）。马来西亚规格公布后我们会补充。'), L)),
        E(t(T('Available now:', 'Ada sekarang:', '现已在售：'), L)),
        sec_head(W['faq_h'], T('Questions about the Voyah Dream', 'Soalan tentang Voyah Dream', '关于岚图梦想家的常见问题'), None, L), faq_html(v['faqs'], L))


def models_index(L):
    return '<section class="sec"><div class="wrap"><div class="models">%s</div><p class="note" style="margin-top:22px">%s</p></div></section>' % (
        ''.join(model_card(m, L) for m in MODELS) + upcoming_card(L), E(t(W['specsrc'], L)))


def colours_html(m, L):
    cols = COLOURS[m['slug']]
    if cols:
        stage, sws = [], []
        for k, (n, hx, ph) in enumerate(cols):
            on = ' on' if k == 0 else ''
            if ph:
                w, h, alt = PHOTOS[ph]
                stage.append('<img class="cp-img%s" data-i="%d" src="%s%s.webp" alt="%s" width="%d" height="%d"%s>' % (
                    on, k, img_base(ph), ph, E(t(alt, L)), w, h, '' if k == 0 else ' loading="lazy" decoding="async"'))
            else:
                stage.append('<div class="cp-img cp-ph%s" data-i="%d"><i style="background:%s"></i><span>%s</span></div>' % (
                    on, k, E(hx), E(t(T('Photo coming soon. Ask us to see this colour.', 'Foto akan datang. Tanya kami untuk melihat warna ini.', '照片即将上线，欢迎询问实车颜色。'), L))))
            sws.append('<button type="button" class="cp-sw%s" data-i="%d" aria-pressed="%s"><i style="background:%s"></i><span>%s</span></button>' % (
                on, k, 'true' if k == 0 else 'false', E(hx), E(n)))
        return ('<div class="cpick" data-cpick><div class="cp-stage">%s</div><p class="cp-name" aria-live="polite">%s</p><div class="cp-sws">%s</div>'
                '<p class="note" style="margin-top:14px">%s</p></div>') % (
            ''.join(stage), E(cols[0][0]), ''.join(sws), E(t(m['interior'], L)))
    soon = ''.join('<div class="sw soon"><i></i>%s</div>' % E(t(T('Coming soon', 'Akan datang', '即将公布'), L)) for _ in range(4))
    return '<div class="soon-box"><div class="swatches">%s</div><p class="note" style="margin:0">%s</p></div>' % (
        soon, E(t(T('The full colour range for Johor is being confirmed. WhatsApp us to see which colours are in the showroom now.',
                    'Senarai penuh warna untuk Johor sedang disahkan. WhatsApp kami untuk tahu warna yang ada di bilik pameran sekarang.',
                    '柔佛完整颜色清单正在确认中。WhatsApp 我们，了解展厅现有颜色。'), L)))


def model_body(m, L):
    figs = '<div class="figs">%s</div>' % ''.join('<div><b>%s</b><span>%s</span></div>' % (E(a), E(t(b, L))) for a, b in m['figs'])
    rows = ''.join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (E(t(a, L)), E(t(b, L))) for a, b in m['spec'])
    other = MOD['007' if m['slug'] == 'vigo' else 'vigo']
    vs = ART['dongfeng-vigo-vs-007']
    return ('<section class="sec"><div class="wrap split"><div><span class="eyebrow">%s</span><h2>%s</h2><p class="answer">%s</p><div class="cta-row">%s</div></div>'
            '<figure>%s</figure></div></section>'
            '<section class="sec sec-white"><div class="wrap">%s%s<p class="note">%s</p></div></section>'
            '<section class="sec sec-dark" style="padding-bottom:40px"><div class="wrap">%s</div>%s</section>'
            '<section class="sec"><div class="wrap">%s%s</div></section>'
            '<section class="sec sec-dark" style="padding-bottom:40px"><div class="wrap">%s</div>%s</section>'
            '<section class="sec sec-white"><div class="wrap">%s<div class="tbl"><table class="spec"><tbody>%s</tbody></table></div><p class="note" style="margin-top:12px">%s</p>'
            '<p>%s <a href="articles/%s/">%s</a> · <a href="models/%s/">%s</a></p></div></section>'
            '<section class="sec"><div class="wrap">%s%s</div></section>') % (
        E(t(m['tag'], L)), E(t(T('What is the %s?', 'Apa itu %s?', '%s 是什么样的车？'), L) % m['name']), E(t(m['answer'], L)), wa_btn(L, topic=m['name'] + '.'),
        img(m['photo'], L),
        sec_head(T('Key figures', 'Angka utama', '核心数据'), T('At a glance', 'Sepintas lalu', '一览'), None, L), figs, E(t(W['specsrc'], L)),
        sec_head(T('Photos', 'Foto', '照片'), T('In our showroom', 'Di bilik pameran kami', '展厅实拍'), None, L), glide(m['gallery'], L),
        sec_head(T('Colours', 'Warna', '颜色'), T('Choose your colour', 'Pilih warna anda', '选择您的颜色'), None, L), colours_html(m, L),
        sec_head(T('Design and details', 'Reka bentuk dan perincian', '设计与细节'), T('The %s up close', '%s dari dekat', '细看 %s'), T('Official Dongfeng photos.', 'Foto rasmi Dongfeng.', '东风官方图片。'), L).replace('%s', m['name']),
        glide(m['official'], L, label=T('Official photos', 'Foto rasmi', '官方图片')),
        sec_head(T('Specifications', 'Spesifikasi', '规格'), T('Full specifications', 'Spesifikasi penuh', '详细规格'), None, L), rows, E(t(W['specsrc'], L)),
        E(t(T('Comparing?', 'Membandingkan?', '在比较？'), L)), vs['slug'], E(t(vs['h1'], L)), other['slug'], E(other['name']),
        sec_head(W['faq_h'], T('Questions about the %s', 'Soalan tentang %s', '关于 %s 的常见问题'), None, L).replace('%s', m['name']), faq_html(m['faqs'], L))


TD_STEPS = [(T('WhatsApp us', 'WhatsApp kami', 'WhatsApp 我们'), T('Tell us the model (Vigo or 007), and a day and time that suit you.', 'Beritahu model (Vigo atau 007), hari dan masa yang sesuai.', '告诉我们车型（Vigo 或 007）以及方便的日期时间。')),
            (T('We confirm the slot', 'Kami sahkan slot', '确认时段'), T('We reply with the time and have the car charged and ready.', 'Kami balas dengan masa dan sediakan kereta yang sudah dicas.', '我们回复确认时间，并把车充好电备好。')),
            (T('Drive it', 'Pandu', '试驾'), T('Bring your driving licence. Take your time: highway, U-turn, parking, back seat.', 'Bawa lesen memandu. Ambil masa anda: lebuh raya, pusingan U, letak kereta, tempat duduk belakang.', '请带驾照。慢慢试：高速、掉头、停车、后排。')),
            (T('Ask anything', 'Tanya apa sahaja', '尽管问'), T('Warranty, charging at home, delivery and price: we answer on the spot.', 'Waranti, pengecasan di rumah, penghantaran dan harga: kami jawab terus.', '保修、家用充电、交车与价格，现场为您解答。'))]

TD_FAQ = [(T('Do I need an appointment?', 'Adakah saya perlu buat temujanji?', '试驾需要预约吗？'),
           T('Test drives are by appointment; WhatsApp us to book a slot.', 'Pandu uji dengan temujanji; WhatsApp kami untuk tempah slot.', '试驾需预约，请 WhatsApp 我们预约时段。')),
          (T('Can you bring the car to me?', 'Bolehkah anda bawa kereta kepada saya?', '可以把车开到我这里试驾吗？'),
           T('Ask us. Our team has brought cars to customers for test drives; it depends on the day and your location.',
             'Tanya kami. Pasukan kami pernah membawa kereta kepada pelanggan untuk pandu uji; bergantung pada hari dan lokasi anda.',
             '可以问问我们。我们的团队曾把车开到客户那里试驾，具体视日期和地点而定。')),
          (T('Can I test drive both models on the same day?', 'Bolehkah saya pandu uji kedua-dua model pada hari yang sama?', '可以同一天试驾两款车吗？'),
           T('Yes, tell us when you book and we will line up the Vigo and the 007.', 'Ya, beritahu kami semasa menempah dan kami sediakan Vigo dan 007.', '可以，预约时告诉我们，我们会把 Vigo 和 007 都准备好。'))]


def test_drive_body(L):
    form = ('<form class="form" data-wa="%s" data-intro="%s"><label>%s<select name="m" data-label="%s"><option>Dongfeng Vigo</option><option>Dongfeng 007</option><option>%s</option></select></label>'
            '<label>%s<input name="d" data-label="%s" placeholder="%s"></label><label>%s<input name="n" data-label="%s" autocomplete="name"></label>'
            '<button class="btn btn-red" type="submit">%s<span>%s</span></button></form>') % (
        WA_NUM, E(t(T('Hi Dongfeng Johor Bahru, I would like to book a test drive.', 'Hai Dongfeng Johor Bahru, saya ingin tempah pandu uji.', '你好，东风新山，我想预约试驾。'), L)),
        E(t(T('Model', 'Model', '车型'), L)), E(t(T('Model', 'Model', '车型'), L)), E(t(T('Both', 'Kedua-dua', '两款都试'), L)),
        E(t(T('Preferred day and time', 'Hari dan masa pilihan', '希望的日期和时间'), L)), E(t(T('When', 'Bila', '时间'), L)), E(t(T('e.g. Saturday morning', 'cth. Sabtu pagi', '例如：周六上午'), L)),
        E(t(T('Your name', 'Nama anda', '您的姓名'), L)), E(t(T('Name', 'Nama', '姓名'), L)), WA_SVG, E(t(T('Send on WhatsApp', 'Hantar di WhatsApp', '通过 WhatsApp 发送'), L)))
    return ('<section class="sec"><div class="wrap split"><div><span class="eyebrow">%s</span><h2>%s</h2><p class="answer">%s</p>%s</div><div>%s</div></div></section>'
            '<section class="sec sec-white"><div class="wrap">%s<p>%s <a href="articles/ev-test-drive-checklist/">%s</a></p><p>%s <a href="models/vigo/">Dongfeng Vigo</a> · <a href="models/007/">Dongfeng 007</a> · <a href="service/">%s</a></p></div></section>'
            '<section class="sec"><div class="wrap">%s%s</div></section>') % (
        E(t(T('By appointment', 'Dengan temujanji', '预约制'), L)), E(t(T('How do I book a Dongfeng test drive in Johor Bahru?', 'Bagaimana tempah pandu uji Dongfeng di Johor Bahru?', '如何预约新山东风试驾？'), L)),
        E(t(T('Send us a WhatsApp with the model you want and a day and time that suit you. We confirm the slot and have the car charged and ready at our 3S centre in Taman Ekoperniagaan, Johor Bahru.',
              'Hantar WhatsApp dengan model yang anda mahu serta hari dan masa yang sesuai. Kami sahkan slot dan sediakan kereta yang sudah dicas di pusat 3S kami di Taman Ekoperniagaan, Johor Bahru.',
              '发 WhatsApp 告诉我们想试的车型和方便的日期时间。我们确认时段后，会在新山 Taman Ekoperniagaan 的 3S 中心把车充好电等您。'), L)),
        steps(TD_STEPS, L), form,
        sec_head(T('Checklist', 'Senarai semak', '清单'), T('What to check on the drive', 'Apa perlu diperiksa semasa memandu', '试驾时要注意什么'), None, L),
        E(t(T('Our short guide:', 'Panduan ringkas kami:', '我们的简明指南：'), L)), E(t(ART['ev-test-drive-checklist']['h1'], L)),
        E(t(T('Know the models first:', 'Kenali model dahulu:', '先了解车型：'), L)), E(t(T('Service at our 3S centre', 'Servis di pusat 3S kami', '3S 中心保养服务'), L)),
        sec_head(W['faq_h'], T('Test drive questions', 'Soalan pandu uji', '试驾常见问题'), None, L), faq_html(TD_FAQ, L))


SERVICE_FAQ = [(T('How often does a Dongfeng EV need a service?', 'Berapa kerap EV Dongfeng perlu diservis?', '东风电动车多久保养一次？'),
                T('Every 10,000 km. Service and spare parts follow Dongfeng\'s list prices; WhatsApp us your model and mileage for a quote. Our workshop is open Monday to Friday 9am to 6pm and Saturday 9am to 1pm.',
                  'Setiap 10,000 km. Servis dan alat ganti mengikut harga senarai Dongfeng; WhatsApp model dan perbatuan kereta anda untuk sebut harga. Bengkel kami dibuka Isnin hingga Jumaat 9 pagi hingga 6 petang dan Sabtu 9 pagi hingga 1 petang.',
                  '每 10,000 公里保养一次。保养与配件按东风官方价目表收费，WhatsApp 我们车型和里程即可报价。维修车间营业时间为周一至周五上午 9 点至下午 6 点，周六上午 9 点至下午 1 点。')),
               (T('How do I book a service for my Dongfeng?', 'Bagaimana tempah servis untuk Dongfeng saya?', '怎么预约东风车保养？'),
                T('WhatsApp us with your car model, plate number and what you need. We will give you a slot.', 'WhatsApp kami dengan model kereta, nombor plat dan keperluan anda. Kami akan beri slot.', 'WhatsApp 我们车型、车牌和需求，我们为您安排时段。')),
               (T('Do you service Dongfeng cars bought elsewhere?', 'Adakah anda servis kereta Dongfeng yang dibeli di tempat lain?', '在别处买的东风车也能来保养吗？'),
                T('Ask us with your model and plate number and we will tell you what we can do.', 'Tanya kami dengan model dan nombor plat dan kami akan beritahu apa yang boleh dibuat.', '请提供车型和车牌询问，我们会告诉您可以提供的服务。'))]


def service_body(L):
    return ('<section class="sec"><div class="wrap split"><div><span class="eyebrow">%s</span><h2>%s</h2><p class="answer">%s</p>%s<div class="cta-row">%s</div></div><figure>%s</figure></div></section>'
            '<section class="sec sec-white"><div class="wrap">%s%s</div></section>') % (
        E(t(T('The second S', 'S kedua', '第二个 S'), L)), E(t(T('Where do I service a Dongfeng EV in Johor?', 'Di mana servis EV Dongfeng di Johor?', '在柔佛去哪里保养东风电动车？'), L)),
        E(t(T('At our Dongfeng 3S centre in Taman Ekoperniagaan, Johor Bahru. Sales, service and spare parts sit under one roof, so the team that sold you the car looks after it afterwards. WhatsApp us to book.',
              'Di pusat 3S Dongfeng kami di Taman Ekoperniagaan, Johor Bahru. Jualan, servis dan alat ganti di bawah satu bumbung, jadi pasukan yang menjual kereta anda juga menjaganya. WhatsApp kami untuk tempahan.',
              '就在新山 Taman Ekoperniagaan 的东风 3S 中心。销售、服务、配件一站式，卖车的团队也负责之后的照顾。WhatsApp 预约。'), L)),
        ticks([T('Book by WhatsApp with your model and plate number', 'Tempah melalui WhatsApp dengan model dan nombor plat', 'WhatsApp 预约，提供车型和车牌'),
               T('Scheduled service every 10,000 km', 'Servis berjadual setiap 10,000 km', '每 10,000 公里定期保养'),
               T('Service and parts charged at Dongfeng\'s list prices', 'Servis dan alat ganti mengikut harga senarai Dongfeng', '保养与配件按东风官方价目表收费'),
               T('Genuine Dongfeng parts through our centre', 'Alat ganti tulen Dongfeng melalui pusat kami', '经由我们中心提供东风原厂配件')], L),
        wa_btn(L, t(T('Book a service', 'Tempah servis', '预约保养'), L), svc=True),
        img('vigo-dash', L),
        sec_head(W['faq_h'], T('Service questions', 'Soalan servis', '保养常见问题'), None, L), faq_html(SERVICE_FAQ, L)) + service_cta(L)


def service_cta(L):
    # Service-specific closing block (ChatGPT draft 26 Oct, approved by Edwin 27 Oct; facts already on this page: service WhatsApp line, address, workshop hours).
    return ('<section class="sec" style="padding-top:0"><div class="wrap"><div class="band"><div><h2>%s</h2><p>%s</p><p>%s</p><p><a href="test-drive/">%s</a></p></div><div class="cta-row">%s</div></div></div></section>') % (
        E(t(T('Book your Dongfeng service in Johor Bahru', 'Tempah servis Dongfeng anda di Johor Bahru', '在新山预约您的东风车保养'), L)),
        E(t(T('Send our service team your Dongfeng model, plate number, current mileage and what you need checked. Ask for an appointment and a quote for your car before your visit.',
              'Hantar kepada pasukan servis kami model Dongfeng, nombor plat, perbatuan semasa dan perkara yang perlu diperiksa. Minta temujanji dan sebut harga untuk kereta anda sebelum anda datang.',
              '请把您的东风车型、车牌号、当前里程和需要检查的项目发给我们的售后团队。到店前可先预约时段，并索取您爱车的报价。'), L)),
        E(t(T('Visit our 3S centre at %s, %s, %s %s. Workshop hours are Monday to Friday, 9am\u20136pm, and Saturday, 9am\u20131pm.' % (STREET, AREA, POSTAL, CITY),
              'Kunjungi pusat 3S kami di %s, %s, %s %s. Waktu bengkel ialah Isnin hingga Jumaat, 9 pagi hingga 6 petang, dan Sabtu, 9 pagi hingga 1 petang.' % (STREET, AREA, POSTAL, CITY),
              '欢迎莅临我们位于 %s 新山 %s, Jalan Ekoperniagaan 3/11 门牌 28 号的 3S 中心。维修车间营业时间：周一至周五上午 9 点至下午 6 点，周六上午 9 点至下午 1 点。' % (POSTAL, AREA)), L)),
        E(t(T('Looking for a new Dongfeng? Book a test drive.', 'Mencari Dongfeng baharu? Tempah pandu uji.', '想看新车？预约试驾。'), L)),
        wa_btn(L, t(T('WhatsApp the service team', 'WhatsApp pasukan servis', 'WhatsApp 售后团队'), L), svc=True))


PARTS_FAQ = [(T('How do I order a Dongfeng part?', 'Bagaimana memesan alat ganti Dongfeng?', '怎么订购东风配件？'),
              T('WhatsApp us your model, year and the part you need, with a photo if you can. We check availability and reply.', 'WhatsApp kami model, tahun dan alat ganti yang diperlukan, dengan foto jika boleh. Kami semak stok dan balas.', 'WhatsApp 我们车型、年份和所需配件，最好附上照片。我们查询库存后回复。'))]


def parts_body(L):
    return ('<section class="sec"><div class="wrap split"><div><span class="eyebrow">%s</span><h2>%s</h2><p class="answer">%s</p><div class="cta-row">%s</div></div><figure>%s</figure></div></section>'
            '<section class="sec sec-white"><div class="wrap">%s%s</div></section>') % (
        E(t(T('The third S', 'S ketiga', '第三个 S'), L)), E(t(T('Where can I get Dongfeng spare parts in Johor Bahru?', 'Di mana boleh dapat alat ganti Dongfeng di Johor Bahru?', '在新山哪里买东风配件？'), L)),
        E(t(T('Through our Dongfeng 3S centre in Taman Ekoperniagaan, Johor Bahru. Send us your model and the part you need on WhatsApp, and we will check availability and arrange fitting.',
              'Melalui pusat 3S Dongfeng kami di Taman Ekoperniagaan, Johor Bahru. Hantar model dan alat ganti yang diperlukan di WhatsApp, kami semak stok dan aturkan pemasangan.',
              '通过我们位于新山 Taman Ekoperniagaan 的东风 3S 中心。WhatsApp 发来车型与所需配件，我们查询库存并安排安装。'), L)),
        wa_btn(L, t(T('Ask about a part', 'Tanya alat ganti', '咨询配件'), L), t(T('a spare part for my Dongfeng.', 'alat ganti untuk Dongfeng saya.', '东风车配件。'), L), svc=True),
        img('cabin-quilted', L),
        sec_head(W['faq_h'], T('Parts questions', 'Soalan alat ganti', '配件常见问题'), None, L), faq_html(PARTS_FAQ, L))


def partners_body(L):
    offer = [T('A Dongfeng 3S showroom in Taman Ekoperniagaan, Johor Bahru', 'Bilik pameran 3S Dongfeng di Taman Ekoperniagaan, Johor Bahru', '位于新山 Taman Ekoperniagaan 的东风 3S 展厅'),
             T('Mall roadshows across Johor: Johor Bahru, Tebrau, Bandar Dato\' Onn, Kota Tinggi', 'Jelajah pusat beli-belah di seluruh Johor: Johor Bahru, Tebrau, Bandar Dato\' Onn, Kota Tinggi', '柔佛各地商场巡展：新山、Tebrau、Bandar Dato\' Onn、哥打丁宜'),
             T('Service and spare parts under the same roof', 'Servis dan alat ganti di bawah satu bumbung', '服务与配件同在一处')]
    who = [(T('Dealers and sub-dealers', 'Pengedar dan sub-pengedar', '经销商与二级经销商'),
            T('Sell Dongfeng EVs in your area of Johor with our 3S centre behind you for service and parts.', 'Jual EV Dongfeng di kawasan anda di Johor dengan sokongan servis dan alat ganti pusat 3S kami.', '在您所在的柔佛地区销售东风电动车，由我们的 3S 中心提供服务与配件支持。')),
           (T('Brands', 'Jenama', '汽车品牌'),
            T('Looking for a partner to represent your brand in Johor? We know the market and already run a brand 3S centre.', 'Mencari rakan untuk mewakili jenama anda di Johor? Kami faham pasaran dan sudah mengendalikan pusat 3S jenama.', '想在柔佛找代理伙伴？我们熟悉本地市场，已在经营品牌 3S 中心。')),
           (T('Corporate and fleet', 'Korporat dan armada', '企业与车队'),
            T('Companies in Johor looking at EVs for staff or fleets can talk to us about a plan.', 'Syarikat di Johor yang mempertimbangkan EV untuk kakitangan atau armada boleh berbincang dengan kami.', '考虑为员工或车队采购电动车的柔佛企业，欢迎与我们洽谈方案。'))]
    form = ('<form class="form" data-wa="%s" data-intro="%s"><label>%s<select name="k" data-label="%s"><option>%s</option><option>%s</option><option>%s</option></select></label>'
            '<label>%s<input name="c" data-label="%s" autocomplete="organization"></label><label>%s<input name="n" data-label="%s" autocomplete="name"></label>'
            '<label>%s<textarea name="x" data-label="%s"></textarea></label><button class="btn btn-red" type="submit">%s<span>%s</span></button>'
            '<p class="note" style="margin:0">%s <a href="mailto:%s">%s</a></p></form>') % (
        WA_NUM, E(t(T('Hi Dongfeng Johor Bahru, I would like to talk about a partnership.', 'Hai Dongfeng Johor Bahru, saya ingin berbincang tentang kerjasama.', '你好，东风新山，我想洽谈合作。'), L)),
        E(t(T('I am a', 'Saya', '我是'), L)), E(t(T('Type', 'Jenis', '类型'), L)), *[E(t(a, L)) for a, _ in who],
        E(t(T('Company', 'Syarikat', '公司'), L)), E(t(T('Company', 'Syarikat', '公司'), L)), E(t(T('Your name', 'Nama anda', '您的姓名'), L)), E(t(T('Name', 'Nama', '姓名'), L)),
        E(t(T('What you have in mind', 'Cadangan anda', '合作构想'), L)), E(t(T('Notes', 'Nota', '备注'), L)), WA_SVG, E(t(T('Send on WhatsApp', 'Hantar di WhatsApp', '通过 WhatsApp 发送'), L)),
        E(t(T('Prefer email?', 'Lebih suka e-mel?', '偏好电邮？'), L)), EMAIL, EMAIL)
    return ('<section class="sec"><div class="wrap split"><div><span class="eyebrow">%s</span><h2>%s</h2><p class="answer">%s</p>%s</div><figure>%s</figure></div></section>'
            '<section class="sec sec-dark"><div class="wrap">%s<div class="cards">%s</div></div></section>'
            '<section class="sec"><div class="wrap split"><div>%s</div>%s</div></section>') % (
        E(t(T('Partnerships', 'Kerjasama', '合作'), L)), E(t(T('Partner with Dongfeng\'s 3S centre in Johor', 'Bekerjasama dengan pusat 3S Dongfeng di Johor', '与柔佛东风 3S 中心合作'), L)),
        E(t(T('MyKar World runs Johor\'s Dongfeng 3S centre in Johor Bahru. We are open to working with dealers who want to sell Dongfeng EVs in Johor, with brands looking for a partner in the state, and with companies planning EV fleets.',
              'MyKar World mengendalikan pusat 3S Dongfeng di Johor Bahru. Kami terbuka untuk bekerjasama dengan pengedar yang mahu menjual EV Dongfeng di Johor, jenama yang mencari rakan di negeri ini, dan syarikat yang merancang armada EV.',
              'MyKar World 在新山经营柔佛东风 3S 中心。我们欢迎想在柔佛销售东风电动车的经销商、在柔佛寻找合作伙伴的品牌，以及规划电动车队的企业与我们合作。'), L)),
        ticks(offer, L), img('showroom-front', L),
        sec_head(T('Who we work with', 'Dengan siapa kami bekerjasama', '合作对象'), T('Three ways to work together', 'Tiga cara bekerjasama', '三种合作方式'), None, L),
        ''.join('<div class="card"><h3>%s</h3><p>%s</p></div>' % (E(t(a, L)), E(t(b, L))) for a, b in who),
        sec_head(T('Talk to us', 'Hubungi kami', '联系我们'), T('Start the conversation', 'Mulakan perbincangan', '开始洽谈'),
                 T('Tell us who you are and what you have in mind. The form opens WhatsApp with your details filled in.', 'Beritahu siapa anda dan cadangan anda. Borang ini membuka WhatsApp dengan maklumat anda.', '告诉我们您是谁、有什么想法。表单会打开 WhatsApp 并自动填好资料。'), L), form)


def about_body(L):
    rows = [(T('Company', 'Syarikat', '公司'), LEGAL), (T('Company No.', 'No. Syarikat', '注册号'), REGNO),
            (T('Brand', 'Jenama', '品牌'), T('Dongfeng passenger EVs (Vigo, 007)', 'Kereta penumpang elektrik Dongfeng (Vigo, 007)', '东风纯电乘用车（Vigo、007）')),
            (T('Role', 'Peranan', '定位'), T('Dongfeng 3S centre for Johor: sales, service, spare parts', 'Pusat 3S Dongfeng untuk Johor: jualan, servis, alat ganti', '柔佛东风 3S 中心：销售、服务、配件')),
            (T('Address', 'Alamat', '地址'), ', '.join(ADDR)), (W['sales_wa'], WA_SHOW), (W['svc_wa'], SVC_SHOW), (W['sales_em'], EMAIL), (W['svc_em'], SVC_EMAIL), ('Facebook', 'facebook.com/dongfengjohorbahru')]
    tbl = ''.join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (E(t(a, L)), E(t(b, L))) for a, b in rows)
    return ('<section class="sec"><div class="wrap split"><div><span class="eyebrow">%s</span><h2>%s</h2><p class="answer">%s</p><p>%s</p></div><figure>%s</figure></div></section>'
            '<section class="sec sec-white"><div class="wrap">%s<div class="tbl"><table class="spec"><tbody>%s</tbody></table></div></div></section>'
            '<section class="sec sec-dark"><div class="wrap split"><figure>%s</figure><div><span class="eyebrow">%s</span><h2>%s</h2><p>%s</p><ul class="chips">%s</ul></div></div></section>') % (
        E(t(T('About us', 'Tentang kami', '关于我们'), L)), E(t(T('Who runs Dongfeng in Johor Bahru?', 'Siapa mengendalikan Dongfeng di Johor Bahru?', '谁在新山经营东风？'), L)),
        E(t(T('Dongfeng Johor Bahru is run by MyKar World Sdn. Bhd. (202501050786, 1652194-X). Our showroom at No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, is the first Dongfeng 3S centre in Johor Bahru, handling sales, service and spare parts for Dongfeng passenger EVs.',
              'Dongfeng Johor Bahru dikendalikan oleh MyKar World Sdn. Bhd. (202501050786, 1652194-X). Bilik pameran kami di No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, ialah pusat 3S Dongfeng pertama di Johor Bahru, mengendalikan jualan, servis dan alat ganti kereta penumpang elektrik Dongfeng.',
              '东风新山由 MyKar World Sdn. Bhd.（202501050786，1652194-X）经营。我们位于 81100 新山 Taman Ekoperniagaan, Jalan Ekoperniagaan 3/11 门牌 28 号的展厅，是新山首家东风 3S 中心，负责东风纯电乘用车的销售、服务与配件。'), L)),
        E(t(T('We want Johor drivers to know there is a full Dongfeng centre right here, and we want to build the brand in the state together with dealers and partners.',
              'Kami mahu pemandu Johor tahu ada pusat Dongfeng lengkap di sini, dan kami mahu membina jenama ini di negeri ini bersama pengedar dan rakan niaga.',
              '我们希望柔佛车主知道，这里就有一家完整的东风中心；我们也希望与经销商和合作伙伴一起，在柔佛把品牌做大。'), L)),
        img('showroom-front', L),
        sec_head(T('Company details', 'Butiran syarikat', '公司资料'), T('The facts', 'Fakta', '基本资料'), None, L), tbl,
        img('merdeka-2026', L), E(t(T('Community', 'Komuniti', '社区'), L)), E(t(T('Part of the neighbourhood', 'Sebahagian komuniti', '融入社区'), L)),
        E(t(T('Besides mall roadshows across Johor, we hosted a Merdeka 2026 costume day for children at the showroom.',
              'Selain jelajah pusat beli-belah di seluruh Johor, kami menganjurkan hari kostum Merdeka 2026 untuk kanak-kanak di bilik pameran.',
              '除了在柔佛各地商场巡展，我们还在展厅举办了 2026 年国庆儿童服装日。'), L)),
        ''.join('<li>%s</li>' % E(t(r, L)) for r in ROADSHOWS))


def contact_body(L):
    return visit_block(L)


def article_body(a, L):
    out = ['<section class="sec"><div class="wrap"><article class="prose"><p class="meta">%s %s · %s</p><p class="answer">%s</p><figure>%s</figure>' % (
        E(t(W['updated'], L)), a.get('date', UPDATED), E(t(W['by'], L)), E(t(a['answer'], L)), img(a['photo'], L))]
    for _i, (h, p) in enumerate(a['sections']):
        out.append('<h2>%s</h2>' % E(t(h, L)))
        if p is None and a['slug'] == 'dongfeng-vigo-vs-007':
            v, s = MOD['vigo'], MOD['007']
            rows = [(T('Body', 'Badan', '车身'), T('SUV', 'SUV', 'SUV'), T('Fastback sedan', 'Sedan fastback', '轿跑')),
                    (T('Battery', 'Bateri', '电池'), '51.87 kWh LFP', '73.48 kWh LFP'),
                    (T('Range', 'Jarak', '续航'), T('471 km', '471 km', '471 公里'), T('Up to 650 km (Premium, CLTC)', 'Sehingga 650 km (Premium, CLTC)', '最高 650 公里（Premium，CLTC）')),
                    ('0-100 km/h', T('9.5 s', '9.5 s', '9.5 秒'), T('5.8 s Premium · 3.9 s Prime', '5.8 s Premium · 3.9 s Prime', 'Premium 5.8 秒 · Prime 3.9 秒')),
                    (T('Length', 'Panjang', '车长'), '4,306 mm', '4,880 mm'), (T('Height', 'Tinggi', '车高'), '1,645 mm', '1,465 mm'),
                    (T('Boot', 'But', '后备箱'), '500 L / 1,040 L', '452 L / 1,026 L'), (T('Warranty', 'Waranti', '保修'), WTY_SHORT, WTY_SHORT), (T('DC charging', 'Pengecasan DC', '直流快充'), T('up to 167 kW', 'sehingga 167 kW', '最高 167 kW'), T('up to 200 kW', 'sehingga 200 kW', '最高 200 kW'))]
            out.append('<div class="tbl"><table class="spec"><thead><tr><th></th><th><a href="../../models/vigo/" style="color:#fff">%s</a></th><th><a href="../../models/007/" style="color:#fff">%s</a></th></tr></thead><tbody>%s</tbody></table></div><p class="note">%s</p>' % (
                v['name'], s['name'], ''.join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td></tr>' % (E(t(r[0], L)), E(t(r[1], L)), E(t(r[2], L))) for r in rows), E(t(W['specsrc'], L))))
        elif p is None and 'install' in a:
            out.append(ticks(a['install'], L))
        elif p is None and 'checks' in a:
            out.append(ticks(a['checks'], L))
        elif p is not None:
            out.append('<p>%s</p>' % E(t(p, L)))
            if a.get('checks_after') == _i:
                out.append(ticks(a['checks'], L))
    if a.get('source'):
        out.append('<p class="note"><a href="%s" rel="noopener">%s</a></p>' % (a['source'][0], E(t(a['source'][1], L))))
    owner_lbl = {'service/': T('Service at our 3S centre', 'Servis di pusat 3S kami', '3S 中心售后服务'),
                 'models/': T('See the Dongfeng Vigo and 007', 'Lihat Dongfeng Vigo dan 007', '查看东风 Vigo 和 007'),
                 'test-drive/': T('Book a Dongfeng test drive in Johor Bahru', 'Tempah pandu uji Dongfeng di Johor Bahru', '预约新山东风试驾')}[a['owner']]
    out.append('<p><a href="%s">%s →</a></p><h2>%s</h2>%s' % (
        a['owner'], E(t(owner_lbl, L)), E(t(W['faq_h'], L)), faq_html(a['faqs'], L)))
    if a.get('date'):  # dated daily articles: soft WhatsApp CTA that names the article (rollout rule)
        out.append('<div class="cta-row" style="margin-top:24px">%s</div>' % wa_btn(L, t(T('Ask us on WhatsApp', 'Tanya kami di WhatsApp', 'WhatsApp 咨询我们'), L), t(T('your guide', 'panduan anda', '您的文章'), L) + ': ' + t(a['h1'], L) + '.'))
    out.append('</article></div></section>')
    return ''.join(out)


def privacy_body(L):
    txt = T(['We collect only what you send us: your name, phone number and message when you WhatsApp, call or email us, and the details you type into our enquiry forms (which open WhatsApp on your phone).',
             'We use it to answer you, arrange test drives, service and parts, and to follow up on your enquiry. We do not sell your data.',
             'This site loads fonts from Google Fonts, photos from jsDelivr and a Google Maps embed; those services may log your visit under their own policies.',
             'You can ask us to see, correct or delete your personal data at %s or on WhatsApp %s. This notice follows Malaysia\'s Personal Data Protection Act 2010.' % (EMAIL, WA_SHOW)],
            ['Kami hanya mengumpul apa yang anda hantar: nama, nombor telefon dan mesej apabila anda WhatsApp, telefon atau e-mel kami, dan butiran dalam borang pertanyaan kami (yang membuka WhatsApp di telefon anda).',
             'Kami menggunakannya untuk menjawab anda, mengatur pandu uji, servis dan alat ganti, serta susulan pertanyaan anda. Kami tidak menjual data anda.',
             'Laman ini memuatkan fon dari Google Fonts, foto dari jsDelivr dan peta Google Maps; perkhidmatan tersebut mungkin merekod lawatan anda mengikut dasar mereka.',
             'Anda boleh meminta untuk melihat, membetulkan atau memadam data peribadi anda di %s atau WhatsApp %s. Notis ini mengikut Akta Perlindungan Data Peribadi 2010 Malaysia.' % (EMAIL, WA_SHOW)],
            ['我们只收集您主动提供的信息：通过 WhatsApp、电话或电邮联系时的姓名、电话和留言，以及您在询问表单中填写的内容（表单会在您的手机上打开 WhatsApp）。',
             '这些信息用于回复您、安排试驾、保养和配件，以及跟进您的询问。我们不会出售您的资料。',
             '本网站会从 Google Fonts 加载字体、从 jsDelivr 加载图片，并嵌入 Google 地图；这些服务可能按其自身政策记录访问。',
             '如需查看、更正或删除个人资料，请电邮 %s 或 WhatsApp %s。本声明依据马来西亚《2010 年个人资料保护法令》。' % (EMAIL, WA_SHOW)])
    return '<section class="sec"><div class="wrap prose">%s</div></section>' % ''.join('<p>%s</p>' % E(p) for p in t(txt, L))


def _hrs(days, o, c):
    return {'@type': 'OpeningHoursSpecification', 'dayOfWeek': days, 'opens': o, 'closes': c}


SHOWROOM_HOURS = [_hrs(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], '09:00', '18:00'), _hrs(['Sunday'], '10:00', '16:00')]
WORKSHOP_HOURS = [_hrs(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'], '09:00', '18:00'), _hrs(['Saturday'], '09:00', '13:00')]


def business_schema(L):
    return {'@type': 'AutoDealer', '@id': SITE + '#business', 'name': NAME, 'alternateName': ['Dongfeng MyKar World Johor Bahru', 'DongFeng Johor Bahru', '东风新山'],
            'legalName': LEGAL, 'identifier': {'@type': 'PropertyValue', 'propertyID': 'SSM company number', 'value': REGNO},
            'url': SITE, 'telephone': TEL, 'email': EMAIL, 'image': [IMG + 'share/home.jpg', IMG + 'icon-512.png'], 'logo': {'@type': 'ImageObject', 'url': IMG + 'icon-512.png', 'width': 512, 'height': 512, 'caption': 'Dongfeng Johor Bahru logo'},
            'brand': {'@type': 'Brand', 'name': 'Dongfeng'}, 'knowsLanguage': ['en', 'ms', 'zh'],
            'description': t(W['ftr_about'], L),
            'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'addressLocality': AREA + ', ' + CITY, 'postalCode': POSTAL,
                        'addressRegion': 'Johor', 'addressCountry': 'MY'},
            'openingHoursSpecification': SHOWROOM_HOURS,
            'contactPoint': [{'@type': 'ContactPoint', 'contactType': 'sales', 'telephone': TEL, 'email': EMAIL, 'areaServed': 'MY', 'availableLanguage': ['en', 'ms', 'zh']},
                             {'@type': 'ContactPoint', 'contactType': 'customer service', 'name': 'Service booking and aftersales', 'telephone': SVC_TEL, 'email': SVC_EMAIL, 'areaServed': 'MY', 'availableLanguage': ['en', 'ms', 'zh']}],
            'department': {'@type': 'AutoRepair', 'name': NAME + ' service workshop', 'telephone': SVC_TEL, 'email': SVC_EMAIL, 'address': {'@type': 'PostalAddress', 'streetAddress': STREET,
                           'addressLocality': AREA + ', ' + CITY, 'postalCode': POSTAL, 'addressRegion': 'Johor', 'addressCountry': 'MY'},
                           'openingHoursSpecification': WORKSHOP_HOURS},
            'areaServed': {'@type': 'State', 'name': 'Johor'}, 'hasMap': MAP, 'sameAs': [FB, GBP]}


def car_schema(m, L, path):
    return {'@type': 'Car', 'name': m['name'], 'brand': {'@type': 'Brand', 'name': 'Dongfeng'}, 'manufacturer': {'@type': 'Organization', 'name': 'Dongfeng Motor Corporation'},
            'fuelType': 'Electric', 'vehicleEngine': {'@type': 'EngineSpecification', 'fuelType': 'Electric'},
            'bodyType': 'SUV' if m['slug'] == 'vigo' else 'Sedan', 'seatingCapacity': 5, 'image': [IMG + m['photo'] + '.webp', IMG2 + m['card'] + '.webp'], 'color': [c[0] for c in COLOURS[m['slug']]],
            'description': t(m['answer'], L), 'url': SITE + PFX[L] + path}


def article_schema(a, L, path):
    return {'@type': 'Article', 'headline': t(a['h1'], L), 'description': t(a['desc'], L), 'inLanguage': LANG_ATTR[L],
            'image': (SITE + 'share/%s.jpg' % a['slug']) if a.get('share') else img_base(a['photo']) + a['photo'] + '.webp', 'datePublished': a.get('date', UPDATED), 'dateModified': a.get('date', UPDATED),
            'author': {'@type': 'Organization', 'name': NAME, 'url': SITE}, 'publisher': {'@id': SITE + '#business'},
            'mainEntityOfPage': SITE + PFX[L] + path}


def build_pages():
    for L in LANGS:
        nav = dict(W['nav'])
        page(L, '', T('Dongfeng Johor Bahru | EV 3S Centre: Vigo & 007', 'Dongfeng Johor Bahru | Pusat 3S EV: Vigo & 007', '东风新山 3S 中心 | Vigo 与 007 纯电车'),
             T('Johor\'s Dongfeng 3S centre in Taman Ekoperniagaan, JB: Dongfeng Vigo electric SUV and 007 electric sedan, service and parts. Book a test drive on WhatsApp.',
               'Pusat 3S Dongfeng di Taman Ekoperniagaan, JB: Dongfeng Vigo SUV elektrik dan 007 sedan elektrik, servis dan alat ganti. Tempah pandu uji di WhatsApp.',
               '柔佛东风 3S 中心，位于新山 Taman Ekoperniagaan：东风 Vigo 纯电 SUV、007 纯电轿跑，售后服务与配件。WhatsApp 预约试驾。'),
             NAME, home_body(L), hero=False, photo='hero', schema=[faq_schema(FAQ_HOME, L)])
        page(L, 'models/', T('Dongfeng EV Models in Johor Bahru: Vigo, 007 | Dongfeng JB', 'Model EV Dongfeng di Johor Bahru: Vigo, 007 | Dongfeng JB', '新山东风纯电车型：Vigo、007 | 东风新山'),
             T('Dongfeng passenger EVs at our Johor Bahru 3S centre: the Vigo electric SUV and the 007 electric sedan. Specs, photos and test drives.',
               'Kereta penumpang elektrik Dongfeng di pusat 3S Johor Bahru: Vigo SUV elektrik dan 007 sedan elektrik. Spesifikasi, foto dan pandu uji.',
               '新山东风 3S 中心在售纯电乘用车：Vigo 纯电 SUV 与 007 纯电轿跑。规格、照片与试驾。'),
             T('Dongfeng models', 'Model Dongfeng', '东风车型'), models_index(L), crumbs=[('models/', nav['models/'])], photo='pair-skyline',
             lede=T('Two passenger EVs, both in our Johor Bahru showroom.', 'Dua kereta penumpang elektrik, kedua-duanya di bilik pameran Johor Bahru.', '两款纯电乘用车，新山展厅均有展示。'))
        for m in MODELS:
            path = 'models/%s/' % m['slug']
            page(L, path, m['title'], m['desc'], m['h1'], model_body(m, L), crumbs=[('models/', nav['models/']), (path, m['name'])], lede=m['lede'], photo=m['hero'],
                 schema=[car_schema(m, L, path), faq_schema(m['faqs'], L)])
        vpath = 'models/%s/' % VOYAH['slug']
        page(L, vpath, VOYAH['title'], VOYAH['desc'], VOYAH['h1'], voyah_body(L), crumbs=[('models/', nav['models/']), (vpath, VOYAH['name'])], lede=VOYAH['lede'],
             photo=VOYAH['hero'], schema=[faq_schema(VOYAH['faqs'], L)])
        page(L, 'test-drive/', T('Dongfeng Test Drive Johor Bahru: Vigo & 007 | Dongfeng JB', 'Tempah Pandu Uji Dongfeng di Johor Bahru | Dongfeng JB', '预约新山东风试驾 | 东风新山 3S 中心'),
             T('Book a Dongfeng test drive in Johor Bahru: try the Vigo or 007 by WhatsApp appointment at our 3S centre. Car charged and ready; bring your licence.',
               'Pandu uji Dongfeng Vigo atau 007 di Johor Bahru. WhatsApp +60 18-762 0828 dengan model dan masa; kereta dicas dan sedia.',
               '在新山试驾东风 Vigo 或 007。WhatsApp +60 18-762 0828 告诉我们车型与时间，车会充好电等您。'),
             T('Book a test drive', 'Tempah pandu uji', '预约试驾'), test_drive_body(L), crumbs=[('test-drive/', nav['test-drive/'])], photo='vigo-showroom', schema=[faq_schema(TD_FAQ, L)],
             lede=T('By WhatsApp appointment at our Johor Bahru 3S centre.', 'Dengan temujanji WhatsApp di pusat 3S Johor Bahru.', '新山 3S 中心，WhatsApp 预约。'))
        page(L, 'service/', T('Dongfeng EV Service Centre in Johor Bahru | Dongfeng JB', 'Pusat Servis EV Dongfeng di Johor Bahru | Dongfeng JB', '新山东风电动车售后服务中心 | 东风新山'),
             T('Service your Dongfeng EV at Johor\'s Dongfeng 3S centre in Taman Ekoperniagaan, Johor Bahru. Book on WhatsApp +60 18-762 0828.',
               'Servis EV Dongfeng anda di pusat 3S Dongfeng di Taman Ekoperniagaan, Johor Bahru. Tempah di WhatsApp +60 18-762 0828.',
               '在新山 Taman Ekoperniagaan 的柔佛东风 3S 中心保养您的东风电动车。WhatsApp +60 18-762 0828 预约。'),
             T('Dongfeng service in Johor Bahru', 'Servis Dongfeng di Johor Bahru', '新山东风售后服务'), service_body(L), crumbs=[('service/', nav['service/'])], photo='vigo-cabin', cta=False,
             lede=T('The second S of our 3S centre.', 'S kedua pusat 3S kami.', '3S 中心的第二个 S。'),
             schema=[{'@type': 'Service', 'name': 'Dongfeng EV service', 'serviceType': 'Car servicing', 'provider': {'@id': SITE + '#business'}, 'areaServed': {'@type': 'State', 'name': 'Johor'}}, faq_schema(SERVICE_FAQ, L)])
        page(L, 'spare-parts/', T('Dongfeng Spare Parts in Johor Bahru | Dongfeng JB', 'Alat Ganti Dongfeng di Johor Bahru | Dongfeng JB', '新山东风零配件 | 东风新山 3S 中心'),
             T('Dongfeng spare parts through Johor\'s Dongfeng 3S centre in Taman Ekoperniagaan, Johor Bahru. WhatsApp your model and part to +60 18-762 0828.',
               'Alat ganti Dongfeng melalui pusat 3S Dongfeng di Taman Ekoperniagaan, Johor Bahru. WhatsApp model dan alat ganti ke +60 18-762 0828.',
               '通过新山 Taman Ekoperniagaan 的柔佛东风 3S 中心订购东风配件。WhatsApp +60 18-762 0828 发送车型与配件需求。'),
             T('Dongfeng spare parts in Johor Bahru', 'Alat ganti Dongfeng di Johor Bahru', '新山东风零配件'), parts_body(L), crumbs=[('spare-parts/', t(T('Spare parts', 'Alat ganti', '零配件'), L))], photo='cabin-quilted',
             lede=T('The third S of our 3S centre.', 'S ketiga pusat 3S kami.', '3S 中心的第三个 S。'),
             schema=[faq_schema(PARTS_FAQ, L)])
        page(L, 'partners/', T('Dongfeng Dealer & Brand Partnerships in Johor | Dongfeng JB', 'Kerjasama Pengedar & Jenama Dongfeng di Johor | Dongfeng JB', '柔佛东风经销与品牌合作 | 东风新山'),
             T('Dealers, brands and fleets: partner with Johor\'s Dongfeng 3S centre in Johor Bahru. Showroom, roadshows across Johor, service and parts.',
               'Pengedar, jenama dan armada: bekerjasama dengan pusat 3S Dongfeng di Johor Bahru. Bilik pameran, jelajah seluruh Johor, servis dan alat ganti.',
               '经销商、品牌与车队：与新山的柔佛东风 3S 中心合作。展厅、柔佛各地巡展、服务与配件。'),
             T('Partner with us', 'Bekerjasama dengan kami', '与我们合作'), partners_body(L), crumbs=[('partners/', nav['partners/'])], photo='showroom-front',
             lede=T('For dealers, brands and companies in Johor.', 'Untuk pengedar, jenama dan syarikat di Johor.', '面向柔佛的经销商、品牌与企业。'))
        page(L, 'articles/', T('Dongfeng EV Guides for Johor Drivers | Dongfeng JB', 'Panduan EV Dongfeng untuk Pemandu Johor | Dongfeng JB', '柔佛车主电动车指南 | 东风新山'),
             T('Plain guides for buying and owning an electric car in Johor: 3S centres, Vigo vs 007, test drives and home charging.',
               'Panduan mudah untuk membeli dan memiliki kereta elektrik di Johor: pusat 3S, Vigo vs 007, pandu uji dan pengecasan di rumah.',
               '在柔佛买电动车、用电动车的实用指南：3S 中心、Vigo 与 007 对比、试驾和家用充电。'),
             T('EV guides', 'Panduan EV', 'EV 指南'),
             '<section class="sec"><div class="wrap"><div class="acards">%s</div></div></section>' % ''.join(article_card(a, L) for a in ARTICLES),
             crumbs=[('articles/', nav['articles/'])], photo='pair-skyline',
             lede=T('Straight answers before you buy an EV in Johor.', 'Jawapan jelas sebelum membeli EV di Johor.', '在柔佛买电动车前的实用解答。'))
        for a in ARTICLES:
            path = 'articles/%s/' % a['slug']
            page(L, path, a['title'], a['desc'], a['h1'], article_body(a, L), crumbs=[('articles/', nav['articles/']), (path, t(a['h1'], L))], photo=a['photo'],
                 schema=[article_schema(a, L, path), faq_schema(a['faqs'], L)], kind='article')
        page(L, 'about/', T('About Dongfeng Johor Bahru (MyKar World Sdn Bhd)', 'Tentang Dongfeng Johor Bahru (MyKar World Sdn Bhd)', '关于东风新山（MyKar World Sdn Bhd）'),
             T('Dongfeng Johor Bahru is run by MyKar World Sdn. Bhd. (202501050786), the first Dongfeng 3S centre in Johor Bahru, in Taman Ekoperniagaan, Johor Bahru.',
               'Dongfeng Johor Bahru dikendalikan oleh MyKar World Sdn. Bhd. (202501050786), pusat 3S Dongfeng pertama di Johor Bahru, di Taman Ekoperniagaan, Johor Bahru.',
               '东风新山由 MyKar World Sdn. Bhd.（202501050786）经营，是新山首家东风 3S 中心，位于 Taman Ekoperniagaan。'),
             T('About Dongfeng Johor Bahru', 'Tentang Dongfeng Johor Bahru', '关于东风新山'), about_body(L), crumbs=[('about/', nav['about/'])], photo='showroom-front',
             lede=T('MyKar World Sdn. Bhd., Johor\'s Dongfeng 3S centre.', 'MyKar World Sdn. Bhd., pusat 3S Dongfeng di Johor.', 'MyKar World Sdn. Bhd.，柔佛东风 3S 中心。'))
        page(L, 'contact/', T('Contact Dongfeng Johor Bahru | WhatsApp +60 18-762 0828', 'Hubungi Dongfeng Johor Bahru | WhatsApp +60 18-762 0828', '联系东风新山 | WhatsApp +60 18-762 0828'),
             T('No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru. WhatsApp +60 18-762 0828 or email marketing@mykar.my.',
               'No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru. WhatsApp +60 18-762 0828 atau e-mel marketing@mykar.my.',
               '81100 新山 Taman Ekoperniagaan, Jalan Ekoperniagaan 3/11 门牌 28 号。WhatsApp +60 18-762 0828 或电邮 marketing@mykar.my。'),
             T('Contact us', 'Hubungi kami', '联系我们'), contact_body(L), crumbs=[('contact/', nav['contact/'])], cta=False,
             lede=T('WhatsApp is the fastest way to reach us.', 'WhatsApp ialah cara paling pantas menghubungi kami.', 'WhatsApp 是最快的联系方式。'))
        page(L, 'privacy/', T('Privacy Notice | Dongfeng Johor Bahru', 'Notis Privasi | Dongfeng Johor Bahru', '隐私声明 | 东风新山'),
             T('How Dongfeng Johor Bahru (MyKar World Sdn. Bhd.) handles personal data under the PDPA 2010.', 'Cara Dongfeng Johor Bahru (MyKar World Sdn. Bhd.) mengendalikan data peribadi di bawah PDPA 2010.', '东风新山（MyKar World Sdn. Bhd.）依据 PDPA 2010 处理个人资料的方式。'),
             T('Privacy notice', 'Notis privasi', '隐私声明'), privacy_body(L), crumbs=[('privacy/', t(W['privacy'], L))], cta=False)


# ---------------------------------------------------------------------------------------------
# Render
# ---------------------------------------------------------------------------------------------
def render(L, path, p):
    full = PFX[L] + path
    pre = '../' * full.count('/')
    lpre = pre + PFX[L]  # links within the same language
    url = SITE + full
    share = IMG + 'share/home.jpg'
    for _a in ARTICLES:
        if _a.get('share') and path == 'articles/%s/' % _a['slug']:
            share = SITE + 'share/%s.jpg' % _a['slug']  # per-article JPG share image, served from the site itself

    def fix(s):
        return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), lpre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (lpre, h, ' aria-current="page"' if path.startswith(h) else '', E(t(x, L))) for h, x in W['nav'])
    langs = ''.join('<a href="%s%s%s" hreflang="%s" lang="%s"%s>%s</a>' % (pre, PFX[l], path, HREFLANG[l], LANG_ATTR[l], ' aria-current="true"' if l == L else '', LANG_LABEL[l]) for l in LANGS)
    alts = ''.join('<link rel="alternate" hreflang="%s" href="%s%s%s">\n' % (HREFLANG[l], SITE, PFX[l], path) for l in LANGS) + \
        '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE, path)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">%s</a>' % (lpre or './', E(t(W['home'], L)))] + ['<a href="%s%s">%s</a>' % (lpre, h, E(t(x, L))) for h, x in p['crumbs'][:-1]] + ['<span>%s</span>' % E(t(p['crumbs'][-1][1], L))]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': t(W['home'], L), 'item': SITE + PFX[L]}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t(x, L), 'item': SITE + PFX[L] + h} for i, (h, x) in enumerate(p['crumbs'])]}
    graph = [business_schema(L), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'],
                                  'inLanguage': LANG_ATTR[L], 'dateModified': LASTMOD.get(path, '2026-11-02'), 'about': {'@id': SITE + '#business'},
                                  'primaryImageOfPage': img_base(p['photo'] or 'hero') + (p['photo'] or 'hero') + '.webp',
                                  'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': NAME, 'inLanguage': ['en-MY', 'ms-MY', 'zh-Hans-MY']}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        bg = '<figure class="phero-bg">%s</figure>' % img(p['photo'], L, eager=True) if p['photo'] and not (path.startswith('articles/') and path != 'articles/') else ''
        head_hero = '<section class="phero%s">%s<div class="wrap">%s<h1>%s</h1>%s</div></section>' % (
            ' has-bg' if bg else '', bg, crumbs_html, E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else '')
    band = ''
    if p['cta']:
        band = '<section class="sec" style="padding-top:0"><div class="wrap"><div class="band"><div><h2>%s</h2><p>%s</p></div><div class="cta-row">%s</div></div></div></section>' % (
            E(t(W['band_h'], L)), E(t(W['band_p'], L)), wa_btn(L) + wa_btn(L, t(W['svc'], L), cls='btn btn-ghost', svc=True))
    title = E(p['title'])
    preload = '<link rel="preload" as="image" href="%s%s.webp" fetchpriority="high">' % (img_base(p['photo'] or ''), p['photo']) if p['photo'] and (p['hero'] or path == '') else ''
    body = fix(p['body'] + band)
    brand = brand_html(lpre)
    ftr_models = ''.join('<li><a href="%smodels/%s/">%s</a></li>' % (lpre, m['slug'], E(m['name'])) for m in MODELS) + \
        ''.join('<li><a href="%s%s">%s</a></li>' % (lpre, h, E(t(x, L))) for h, x in [('test-drive/', W['nav'][1][1]), ('service/', W['nav'][2][1]), ('spare-parts/', T('Spare parts', 'Alat ganti', '零配件')), ('partners/', W['nav'][3][1])])
    ftr_explore = ''.join('<li><a href="%s%s">%s</a></li>' % (lpre, h, E(t(x, L))) for h, x in [('articles/', W['nav'][4][1]), ('about/', W['nav'][5][1]), ('contact/', W['nav'][6][1]), ('privacy/', W['privacy'])])
    return f'''<!doctype html>
<html lang="{LANG_ATTR[L]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#0b0c0f">
<link rel="canonical" href="{url}">
{alts}{preload}
<meta property="og:type" content="{p['kind']}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{share}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(t(PHOTOS['hero'][2], L))}">
<meta property="og:locale" content="{OG_LOCALE[L]}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="icon" href="{IMG}icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{IMG}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="{pre}df.css?v=2">
<script src="{pre}df.js?v=3" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap">
{brand}
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
<div class="lang" aria-label="Language">{langs}</div>
{wa_btn(L, t(W['whatsapp'], L), cls='btn btn-red hdr-wa')}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">{E(t(W['menu'], L))}</button>
</div></header>
<main id="main">
{head_hero}
{body}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div>{brand}<p>{E(t(W['ftr_about'], L))}</p></div>
<div><h3>{E(t(W['models'], L))}</h3><ul>{ftr_models}</ul></div>
<div><h3>{E(t(W['explore_h'], L))}</h3><ul>{ftr_explore}</ul></div>
<div><h3>{E(t(W['contact_h'], L))}</h3><ul>
<li>{E(t(W['sales'], L))}: <a href="{E(wa_url(L))}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></li>
<li>{E(t(W['svc'], L))}: <a href="{E(wa_url(L, svc=True))}" target="_blank" rel="noopener">WhatsApp {SVC_SHOW}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><a href="mailto:{SVC_EMAIL}">{SVC_EMAIL}</a></li>
<li>{'<br>'.join(E(a) for a in ADDR)}</li>
<li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>© 2026 {LEGAL} · {E(t(W['reg'], L))} {REGNO}</span><span>{E(t(W['built'], L))} <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<div class="dock"><a class="dock-wa" href="{E(wa_url(L))}" target="_blank" rel="noopener">{WA_SVG}<span>{E(t(W['sales'], L))}</span></a><a class="dock-alt" href="{E(wa_url(L, svc=True))}" target="_blank" rel="noopener">{WA_SVG}<span>{E(t(W['svc'], L))}</span></a></div>
</body>
</html>
'''


def not_found():
    L = 'en'
    body = ('<section class="sec"><div class="wrap prose"><p>The page you were looking for has moved or does not exist. / Halaman tidak dijumpai. / 找不到该页面。</p>'
            '<ul>%s</ul></div></section>') % ''.join('<li><a href="%s">%s</a></li>' % (h or './', E(t(x, L))) for h, x in [('', W['home'])] + W['nav'])
    p = dict(title='Page not found | Dongfeng Johor Bahru', desc='This page could not be found.', h1='Sorry, that page is not here.', body=body,
             crumbs=None, lede='', schema=[], hero=True, cta=True, photo=None, kind='website')
    out = render(L, '', p).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    base = '/' if LIVE else '/preview/%s/' % SLUG
    return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|/|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), base, m.group(2) if m.group(2) != './' else ''), out)


BOTS = ['Googlebot', 'Googlebot-Image', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot',
        'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']

HTACCESS = """# Dongfeng Johor Bahru ({DOMAIN}). Document root for {DOMAIN}; also served as
# pageonesingapore.com/preview/dongfeng-jb/ before go-live. Overrides the parent pageonesingapore.com .htaccess.
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://{DOMAIN}/$1 [L,R=301]
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8
<IfModule mod_headers.c>
SetEnvIfNoCase Host ^(www\\.)?pageonesingapore\\.com$ P1_PREVIEW=1
Header set X-Robots-Tag "noindex, nofollow" env=P1_PREVIEW
<FilesMatch "\\.(html)$">
Header set Cache-Control "max-age=3600, public"
</FilesMatch>
</IfModule>
"""


def main():
    build_pages()
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w') as f:
        f.write(INDEXNOW_KEY)
    for (L, path), p in PAGES.items():
        d = os.path.join(OUT, PFX[L] + path)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(render(L, path, p))
    with open(os.path.join(OUT, '404.html'), 'w') as f:
        f.write(not_found())
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write(''.join('User-agent: %s\nAllow: /\n\n' % b for b in BOTS) + 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
        for (L, path) in PAGES:
            f.write('  <url><loc>%s%s%s</loc><lastmod>%s</lastmod>%s</url>\n' % (SITE, PFX[L], path, LASTMOD.get(path, '2026-11-02'), ''.join(
                '<xhtml:link rel="alternate" hreflang="%s" href="%s%s%s"/>' % (HREFLANG[l], SITE, PFX[l], path) for l in LANGS)))
        f.write('</urlset>\n')
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write('# Dongfeng Johor Bahru (MyKar World), Dongfeng EV 3S centre in Johor Bahru, Malaysia\n\n'
                '> Dongfeng Johor Bahru is the first Dongfeng 3S centre in Johor Bahru (sales, service and spare parts) for Dongfeng passenger electric cars. '
                'It sells the Dongfeng Vigo Premier 120kW (5-seat electric SUV, 51.87 kWh LFP battery, 471 km range, 500 L boot; colours Mosswood Green, Canyon Orange, Arctic White, Sandstone Beige, Titanium Silver, Cyber Black) and the Dongfeng 007 '
                '(electric fastback sedan, 73.48 kWh LFP battery; Long Range RWD Premium 200 kW, 650 km CLTC / 530 km WLTP, 0-100 km/h 5.8 s; AWD Prime 400 kW / 544 PS, 565 km CLTC / 389 km WLTP, 0-100 km/h 3.9 s; DC 30-80%% in about 11 min; colours Celestial White, Eclipse Grey, Obsidian Black, Starlit Silver). '
                'Warranty: 8 years unlimited mileage powertrain, 6 years unlimited mileage vehicle. '
                'Coming soon: the Voyah Dream luxury MPV (Voyah is Dongfeng\'s luxury brand; previewed by Dongfeng Malaysia at KLIMS 2026); Malaysian specs, price and launch date not announced yet. '
                'Showroom hours: Monday to Saturday 9am-6pm, Sunday 10am-4pm. Workshop hours: Monday to Friday 9am-6pm, Saturday 9am-1pm, Sunday closed. '
                'Scheduled service every 10,000 km; service and spare parts follow Dongfeng list prices. '
                'Address: %s, %s, %s %s, Johor, Malaysia. Sales (new cars, promotions): WhatsApp or call %s, email %s. Service booking, aftersales and spare parts: WhatsApp or call %s, email %s. Operated by %s, company no. %s. '
                'Test drives by WhatsApp appointment. Prices are given on request, not published. Languages: English, Bahasa Melayu, Chinese. '
                'Also open to dealer, brand and fleet partnerships in Johor. Logo: %sicon-512.png (red Dongfeng emblem). Google Business Profile and reviews: %s . Facebook: %s\n\n'
                '## Pages (English; Bahasa Melayu under /ms/, Chinese under /zh/)\n' % (STREET, AREA, POSTAL, CITY, WA_SHOW, EMAIL, SVC_SHOW, SVC_EMAIL, LEGAL, REGNO, IMG, GBP, FB))
        for (L, path), p in PAGES.items():
            if L == 'en':
                f.write('- [%s](%s%s): %s\n' % (p['title'].split(' | ')[0], SITE, path, p['desc']))
        f.write('\nLast updated 2 November 2026.\n')
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': NAME, 'short_name': 'Dongfeng JB', 'icons': [{'src': IMG + 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                                                         {'src': IMG + 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
                   'theme_color': '#0b0c0f', 'background_color': '#f5f2ec', 'display': 'browser'}, f)
    with open(os.path.join(HERE, 'htaccess.txt'), 'w') as f:
        f.write(HTACCESS.replace('{DOMAIN}', DOMAIN))
    for fn in ('df.css', 'df.js'):
        shutil.copy(os.path.join(HERE, fn), os.path.join(OUT, fn))
    if IMGMAP:
        os.makedirs(os.path.join(OUT, 'img'), exist_ok=True)
        for fn in {m['f'] for m in IMGMAP.values()}:
            shutil.copy(os.path.join(HERE, 'assets', 'img', fn), os.path.join(OUT, 'img', fn))
    print('built %d pages' % len(PAGES))


if __name__ == '__main__':
    main()
