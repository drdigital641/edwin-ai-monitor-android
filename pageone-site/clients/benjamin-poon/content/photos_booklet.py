"""Photos cut from Nirvana Memorial Garden's 2025 booklet (flipsnack.com/nirvanasg/nirvana-booklet-25.html), requested by Benjamin
for the products & services page. Use is PENDING CLIENT APPROVAL (Benjamin to confirm Nirvana allows agents to reuse booklet material).
Hosted on jsDelivr from the site-assets branch."""
B = 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@299b3c6/site-assets/benjamin-poon/booklet/'
CR = 'Photo: Nirvana Memorial Garden booklet 2025'
SRC = 'https://www.flipsnack.com/nirvanasg/nirvana-booklet-25.html'


def _b(f, w, h, alt_en, alt_zh):
    return dict(url_large=B + f + '.webp', url_small=B + f + '.webp', w=w, h=h, alt_en=alt_en, alt_zh=alt_zh, credit=CR, source_page=SRC, role='booklet', generic=False, official=True)


PHOTOS_BK = {
    'nb-family-walk': _b('nb-family-walk', 1336, 1155, 'Family walking hand in hand on the grass at sunset', '一家人在夕阳下的草地上手牵手散步'),
    'nb-facade': _b('nb-facade', 1400, 931, 'Nirvana Memorial Garden Singapore building with its white fins and zen garden', '新加坡富贵山庄大楼外观与枯山水庭园'),
    'nb-family-suites': _b('nb-family-suites', 870, 1057, 'Family Suites columbarium room with a crystal chandelier', '家庭骨灰福殿，设有水晶吊灯'),
    'nb-freethinker-suites': _b('nb-freethinker-suites', 870, 645, 'Free Thinker Suites with a backlit wall of round niches', '无宗教骨灰福殿，圆形福位墙'),
    'nb-modern-suites': _b('nb-modern-suites', 1400, 970, 'Modern Suites with gold walls and blue-and-white porcelain niches', '现代化骨灰福殿，金色墙面与青花瓷福位'),
    'nb-royal-suite': _b('nb-royal-suite', 1400, 1034, 'Royal Suite with warm gold niche walls and a lounge area', '帝王阁，金色福位墙与休息区'),
    'nb-tablets': _b('nb-tablets', 1400, 950, 'Ancestral tablet hall with a Ksitigarbha statue and glass tablet shelves', '神主牌区，地藏菩萨像与玻璃牌位架'),
    'nb-grand-hall': _b('nb-grand-hall', 1400, 990, 'Block B Grand Hall with a lotus ceiling light and golden statues', 'B座大雄宝殿，莲花吊灯与金色佛像'),
    'nb-prayer-monk': _b('nb-prayer-monk', 1018, 810, 'Monk offering prayers at a tablet wall', '法师在牌位墙前诵经祈福'),
    'nb-prayer-offerings': _b('nb-prayer-offerings', 1018, 690, 'Hall of offering tables during a Zhong Yuan prayer ceremony', '中元法会的供品大厅'),
    'nb-staff': _b('nb-staff', 1357, 1560, 'Nirvana staff member presenting a tablet display', '富贵山庄职员介绍牌位'),
    'nb-freccia': _b('nb-freccia', 1169, 796, 'White FRECCIA custom hearse at sunset', '夕阳下的白色 FRECCIA 定制灵车'),
    'nb-wake': _b('nb-wake', 1400, 1287, 'Buddhist wake set with white chrysanthemums and lanterns', '佛教灵堂布置，白菊花与灯笼'),
    'nb-eternal-flowers': _b('nb-eternal-flowers', 976, 1590, 'Niche decorated with preserved eternal flowers', '以永生花布置的福位'),
    'nb-spa': _b('nb-spa', 954, 690, 'Journey With Love care room with wood panelling', '爱。相随 礼体护理室'),
    'nb-atrium': _b('nb-atrium', 1400, 911, 'Skylit atrium with lattice walls', '天窗中庭与花格墙'),
    'nb-fac-1': _b('nb-fac-1', 509, 360, 'Lounge area with a blue rug', '设有蓝色地毯的休息区'),
    'nb-fac-2': _b('nb-fac-2', 551, 360, 'Level 9 cafe dining area', '九楼咖啡厅用餐区'),
    'nb-fac-3': _b('nb-fac-3', 530, 360, 'Private consultation lounge', '私人洽谈室'),
    'nb-fac-4': _b('nb-fac-4', 530, 360, 'Reception corridor with greenery', '绿意盎然的接待走廊'),
    'nb-lounge': _b('nb-lounge', 1400, 990, 'Block B Level 5 lounge with gold screens', 'B座五楼贵宾休息厅'),
    'nb-signage': _b('nb-signage', 1400, 931, 'Nirvana sign on the building facade', '大楼外墙的富贵山庄标志'),
}
