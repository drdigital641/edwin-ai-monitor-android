"""简体中文 copy for the MCS Auto Spray Painting preview. Same keys as strings_en.py (build.py checks)."""

UI = {
    'skip': '跳到正文', 'menu': '菜单', 'close': '关闭菜单', 'lang': '语言', 'breadcrumb': '页面路径',
    'home': '首页', 'services': '服务', 'about': '关于我们', 'contact': '联系我们', 'articles': '文章', 'privacy': '隐私',
    'wa_btn': 'WhatsApp 发车辆照片', 'wa_short': 'WhatsApp', 'call_btn': '致电 016-556 2998', 'call_short': '致电',
    'facebook': 'Facebook', 'youtube': 'YouTube', 'maps': '在 Google 地图打开', 'directions': '导航前往',
    'reviews': '查看我们的 Google 评价', 'email_h': '电邮',
    'hours_h': '营业时间', 'address_h': '车厂地址', 'contact_h': '联系我们', 'find_h': '找到我们',
    'closed': '休息', 'today': '今天',
    'prev': '上一张', 'next': '下一张', 'gallery_label': '完工车辆与喷漆房照片',
    'zones_label': '选择服务', 'see_service': '了解这项服务', 'all_services': '全部服务',
    'other_services': '其他服务', 'tagline': 'Pusat Kecantikan Kereta',
    'map_title': 'MCS Auto Spray Painting 武吉英达花园地图',
}

HOURS = [('星期一', '上午9:00至晚上7:00'), ('星期二', '休息'), ('星期三至星期五', '上午9:00至下午5:00'), ('星期六和星期日', '上午9:00至晚上7:00')]
HOURS_SHORT = '星期一、六、日上午9点至晚上7点；星期三至五上午9点至下午5点；星期二休息。'

PREFILL = {
    'default': '你好，MCS Auto Spray Painting，我想询问喷漆 / 钣金维修。车型和年份：',
    'spray-painting': '你好，MCS Auto Spray Painting，我想询问汽车喷漆报价。车型和年份：',
    'custom-colour': '你好，MCS Auto Spray Painting，我想询问定制颜色。车型和年份：',
    'body-repair': '你好，MCS Auto Spray Painting，我的车发生意外，需要钣金维修。车型和年份：',
    'paint-protection': '你好，MCS Auto Spray Painting，我想询问 Nippon AI-PPS 漆面保护。车型和年份：',
    'rims-calipers-engine': '你好，MCS Auto Spray Painting，我想给轮毂 / 卡钳 / 引擎舱喷漆。车型和年份：',
    'interior-repair': '你好，MCS Auto Spray Painting，我想询问座椅 / 内饰维修。车型和年份：',
    'carbon-bodykits': '你好，MCS Auto Spray Painting，我想询问碳纤维维修 / 包围套件。车型和年份：',
    'insurance-windscreen': '你好，MCS Auto Spray Painting，我需要保险 / 挡风玻璃索赔的协助。车型和年份：',
    'motorbike': '你好，MCS Auto Spray Painting，我想询问摩托车喷漆。摩托车型号：',
}

CHIPS = {'cyan': '糖果青蓝', 'green': '赛车绿', 'black': '亮光黑'}

HOME = {
    'title': '武吉英达汽车喷漆与钣金维修，柔佛 | MCS Auto Spray Painting',
    'meta': 'MCS Auto Spray Painting 位于依斯干达公主城武吉英达花园：全车与局部喷漆、糖果色与珍珠色定制、事故钣金维修和保险索赔。WhatsApp 016-556 2998。',
    'h1': '柔佛武吉英达的汽车喷漆与钣金维修',
    'chips_label': '来自真实作品的漆面',
    'promise_h': '喷漆、钣金、内饰，一家车厂搞定',
    'promise': [
        'MCS Auto Spray Painting 是位于依斯干达公主城武吉英达花园 Jalan Indah 16/11 的汽车喷漆与钣金车厂。全车喷漆、局部补漆、糖果色和珍珠色定制、事故钣金维修以及保险索赔，都在同一块招牌下完成：Pusat Kecantikan Kereta。',
        '用 WhatsApp 发来车辆照片，告诉我们您的想法。我们会回复这项工作需要做些什么。',
    ],
    'zones_h': '您想做哪一项？',
    'zones_p': '点选服务，查看我们车厂的真实作品。',
    'process_h': '从颜色沟通到取车',
    'process_p': '四个步骤，无论是保险杠刮花还是全车改色都一样。',
    'proof_h': '刚出喷漆房的完工车辆',
    'proof_line': 'Google 评分 4.5，共 65 条评价',
    'proof_themes': '车主们提到 WhatsApp 回复及时、颜色建议耐心细致、糖果蓝喷漆、事故维修以及摩托车喷漆。',
    'hours_h': '欢迎到车厂',
    'hours_p': '星期二休息。星期三至星期五下午5:00关门。',
    'band_h': '有刮痕、凹陷，或想换个颜色？',
    'band_p': '用 WhatsApp 发照片到 016-556 2998，并附上车型和年份。',
}

STEPS = [
    ('WhatsApp 颜色沟通', '发来车辆照片以及想要的颜色或损坏情况。我们一起讨论漆面效果和所需的工作。'),
    ('打底与钣金修复', '修复凹陷和受损板件，打磨并遮蔽，只让需要喷漆的表面上漆。'),
    ('喷漆房与清漆', '在喷漆房内上色，再喷上清漆，带来层次和光泽。'),
    ('取车', '到 Jalan Indah 16/11 取车，和我们一起查看漆面效果。'),
]

SERVICE_ORDER = ['spray-painting', 'custom-colour', 'body-repair', 'paint-protection', 'rims-calipers-engine',
                 'interior-repair', 'carbon-bodykits', 'insurance-windscreen', 'motorbike']

SERVICES = {
    'spray-painting': {
        'zone': '汽车喷漆', 'short': '在自家喷漆房完成全车与局部喷漆。',
        'title': '武吉英达汽车喷漆，依斯干达公主城 | MCS Auto Spray Painting',
        'meta': 'MCS Auto Spray Painting 提供全车与局部喷漆，位于柔佛依斯干达公主城武吉英达花园。喷漆房作业，WhatsApp 发照片即可询价。',
        'h1': '武吉英达汽车喷漆',
        'lead': '全车重喷与单片补漆，都在我们位于 Jalan Indah 16/11 的喷漆房内完成。',
        'paras': ['车顶褪色、车门刮花或想换全新颜色：我们先处理表面、遮蔽不需喷漆的部位，在喷漆房内喷涂，最后上清漆。',
                  '用 WhatsApp 发来照片并附上车型和年份，我们会告诉您这项工作包括哪些内容。'],
        'points': ['全车重喷', '单片、保险杠和车门', '按原车颜色调色', '喷漆房喷涂与清漆'],
    },
    'custom-colour': {
        'zone': '定制颜色', 'short': '调色配色，糖果色与珍珠色漆面。',
        'title': '新山定制车色、糖果色与珍珠色喷漆 | MCS Auto Spray Painting',
        'meta': 'MCS Auto Spray Painting 提供糖果色与珍珠色的定制调色，位于依斯干达公主城武吉英达花园。看看我们的糖果青蓝 Toyota Vellfire。',
        'h1': '定制颜色，糖果色与珍珠色漆面',
        'lead': '本网站上的糖果青蓝 Toyota Vellfire 就是在我们喷漆房完成的。把您的颜色想法带来吧。',
        'paras': ['定制颜色从沟通开始。分享一张照片、您喜欢的颜色或色板，我们会一起讨论它在白天、阴影下和夜晚的效果。',
                  '我们也为原车漆调色，让修补的板件与原漆一致。'],
        'points': ['糖果色与珍珠色漆面', '修补时的颜色匹配', '全车改色', '调漆之前先给建议'],
        'posted': '已发布在我们的 Facebook 专页：',
        'posted_aikka': 'Aikka 双色水晶改色作品',
        'posted_glasurit': '使用 Glasurit 清漆的 Mercedes-Benz 黑水晶作品',
    },
    'body-repair': {
        'zone': '钣金维修', 'short': '事故损伤修复、打底并重新喷漆。',
        'title': '武吉英达事故钣金维修，柔佛 | MCS Auto Spray Painting',
        'meta': 'MCS Auto Spray Painting 位于依斯干达公主城武吉英达花园，提供事故钣金维修：凹陷、受损板件和保险杠修复后在喷漆房重新喷漆。',
        'h1': '武吉英达事故钣金维修',
        'lead': '凹陷、破裂的保险杠和受损板件，修复后喷漆配色。',
        'paras': ['发生碰撞后，从几个角度拍下损坏部位发给我们。我们会判断哪些可以修、哪些需要更换，然后打底并在喷漆房重新喷漆。',
                  '如果维修经由您的保险公司处理，我们也可以协助索赔。'],
        'points': ['凹陷与板件损伤', '保险杠修复与重喷', '与全车颜色一致', '协助保险索赔'],
    },
    'paint-protection': {
        'zone': 'Nippon AI-PPS', 'short': '为完工车辆喷涂漆面保护。',
        'title': '依斯干达公主城 Nippon AI-PPS 漆面保护 | MCS Auto Spray Painting',
        'meta': 'MCS Auto Spray Painting 提供 Nippon AI-PPS 喷涂式漆面保护，位于柔佛依斯干达公主城武吉英达花园。WhatsApp 016-556 2998。',
        'h1': 'Nippon AI-PPS 漆面保护',
        'lead': '一层喷涂式的漆面保护，在我们武吉英达的车厂施工。',
        'paras': ['Nippon AI-PPS 是一种喷涂式漆面保护，适合刚重新喷漆的车，也适合想好好保养原漆的车。',
                  '用 WhatsApp 发来车型和年份，我们会向您说明施工方式。'],
        'points': ['喷涂施工', '适用于新漆或原车漆', '在我们车厂施工', '欢迎询问施工方式'],
    },
    'rims-calipers-engine': {
        'zone': '轮毂与卡钳', 'short': '轮毂、刹车卡钳和引擎舱喷漆。',
        'title': '柔佛轮毂、刹车卡钳与引擎舱喷漆 | MCS Auto Spray Painting',
        'meta': 'MCS Auto Spray Painting 提供轮毂、刹车卡钳和引擎舱喷漆，位于柔佛依斯干达公主城武吉英达花园。WhatsApp 发照片即可询价。',
        'h1': '轮毂、卡钳与引擎舱喷漆',
        'lead': '在细节上添色：轮毂、刹车卡钳和引擎舱。',
        'paras': ['轮毂或卡钳换上新颜色，整辆车的样子都会不同。我们也为引擎舱部件喷漆。',
                  '告诉我们您想要的颜色，并发来轮毂或卡钳目前的照片。'],
        'points': ['轮毂喷漆', '刹车卡钳喷漆', '引擎舱喷漆', '与车身同色或撞色'],
    },
    'interior-repair': {
        'zone': '内饰与座椅', 'short': '座椅、方向盘和车顶内衬维修，门板翻新。',
        'title': '武吉英达汽车座椅与内饰维修、翻新 | MCS Auto Spray Painting',
        'meta': 'MCS Auto Spray Painting 提供座椅、方向盘和车顶内衬维修、座椅翻新以及门板翻新，位于依斯干达公主城武吉英达花园。',
        'h1': '座椅与内饰维修、翻新',
        'lead': '座椅破损、方向盘磨旧或车顶内衬下垂，都在我们的内饰间修复。',
        'paras': ['我们的内饰间负责座椅维修与翻新、方向盘和车顶内衬维修，以及门板翻新。本页的米色配黑色双色座椅和门板就是我们的翻新作品之一。',
                  '发来车内照片，告诉我们您想要的样子。'],
        'points': ['座椅维修与翻新', '方向盘维修', '车顶内衬维修', '门板翻新'],
    },
    'carbon-bodykits': {
        'zone': '碳纤维与包围', 'short': '碳纤维维修与定制包围套件。',
        'title': '新山碳纤维维修与定制包围套件 | MCS Auto Spray Painting',
        'meta': 'MCS Auto Spray Painting 提供碳纤维维修和定制包围套件，位于柔佛依斯干达公主城武吉英达花园。WhatsApp 016-556 2998。',
        'h1': '碳纤维维修与定制包围套件',
        'lead': '修复碳纤维部件，安装并喷涂定制包围套件。',
        'paras': ['破裂或刮花的碳纤维部件，很多时候都可以修复。我们也安装定制包围套件，并按车身喷漆。',
                  '用 WhatsApp 发来部件或您计划的包围套件照片，并附上车型和年份。'],
        'points': ['碳纤维维修', '定制包围套件', '包围按车身喷漆', '先看照片，再给建议'],
    },
    'insurance-windscreen': {
        'zone': '保险与挡风玻璃', 'short': '协助保险索赔和挡风玻璃索赔。',
        'title': '柔佛保险索赔喷漆与挡风玻璃索赔 | MCS Auto Spray Painting',
        'meta': 'MCS Auto Spray Painting 协助保险索赔和挡风玻璃索赔，位于柔佛依斯干达公主城武吉英达花园。WhatsApp 发来您的索赔资料。',
        'h1': '保险与挡风玻璃索赔',
        'lead': '经由保险公司的事故维修，以及挡风玻璃索赔，都在我们车厂处理。',
        'paras': ['发生事故后，用 WhatsApp 发来损坏照片，并告诉我们您的保险公司。我们会告诉您开始索赔需要准备什么。',
                  '挡风玻璃索赔也是同样方式：发来裂痕或崩口的照片。'],
        'points': ['事故保险索赔', '挡风玻璃索赔', '批准后进行维修和喷漆', '在 WhatsApp 告诉我们您的保险公司'],
    },
    'motorbike': {
        'zone': '摩托车喷漆', 'short': '摩托车喷漆与改色。',
        'title': '武吉英达摩托车喷漆，柔佛 | MCS Auto Spray Painting',
        'meta': 'MCS Auto Spray Painting 提供摩托车喷漆，位于柔佛依斯干达公主城武吉英达花园。WhatsApp 发来您的摩托车照片。',
        'h1': '摩托车喷漆',
        'lead': '摩托车也会来我们车厂，做喷漆和改色。',
        'paras': ['车友们在我们的 Google 评价中提到摩托车喷漆。发来摩托车照片和想要喷漆的部位。',
                  '照片中的绿色摩托车就停在我们车厂地面上，旁边是内饰间。'],
        'points': ['摩托车喷漆', '改色与重新喷漆', '先发摩托车照片', '与汽车作业同一车厂'],
    },
}

SERVICES_PAGE = {
    'title': '武吉英达汽车喷漆、钣金与内饰服务 | MCS Auto Spray Painting',
    'meta': 'MCS Auto Spray Painting 全部服务，位于依斯干达公主城武吉英达花园：喷漆、定制颜色、钣金、Nippon AI-PPS、轮毂、内饰、碳纤维、索赔与摩托车。',
    'h1': '我们的服务',
    'lead': '喷漆、钣金、内饰和索赔，都在 Jalan Indah 16/11 的同一家车厂。',
    'one_stop_h': '一站式汽车服务',
    'one_stop': 'MCS AUTO DETAILER 招牌就在同一排店屋的隔壁单位，属于同一家车厂。',
}

ABOUT = {
    'title': '关于 MCS Auto Spray Painting，依斯干达公主城武吉英达花园',
    'meta': 'MCS Auto Spray Painting 是位于柔佛依斯干达公主城武吉英达花园 Jalan Indah 16/11 的多单位喷漆与钣金车厂。Pusat Kecantikan Kereta。',
    'h1': '关于 MCS Auto Spray Painting',
    'lead': 'Pusat Kecantikan Kereta：Jalan Indah 16/11 的汽车美容中心。',
    'sign_h': '认准深色招牌',
    'sign_p': '我们的招牌写着 Pusat Kecantikan Kereta，配有 MCS BODY & PAINT 盾牌标志和红白色的 MCS AUTO SPRAY PAINTING 字样。车厂占用同一排店屋的几个单位，隔壁单位挂着 MCS AUTO DETAILER 招牌。',
    'unit_h': '57号单位与喷漆房',
    'unit_p': '横梁上的金色 57 标示着我们的主单位。里面有喷漆房、调漆工作台和内饰间。车厂里可以看到 3M、HyperTint 和 HyperFilm 的标识。',
    'contact_h': '找谁',
    'contact_p': '通过 WhatsApp 或电话 016-556 2998 联系时，请找小龙（Ah Long）。',
    'area_p': '我们服务武吉英达花园、依斯干达公主城以及新山一带的车主。',
}

CONTACT = {
    'title': '联系 MCS Auto Spray Painting 武吉英达 | WhatsApp 016-556 2998',
    'meta': 'MCS Auto Spray Painting，No. 57, Jalan Indah 16/11, Taman Bukit Indah, 79000 Iskandar Puteri, Johor。WhatsApp 或致电 016-556 2998。星期二休息。',
    'h1': '联系方式与路线',
    'lead': 'WhatsApp 是最快的联系方式。发来车辆照片，并附上车型和年份。',
    'map_h': '地图位置',
    'ask_for': '请找小龙（Ah Long）。',
}

PRIVACY = {
    'title': '隐私 | MCS Auto Spray Painting',
    'meta': 'MCS Auto Spray Painting 如何处理您联系我们时提供的资料。',
    'h1': '隐私',
    'body': [
        ('我们收到的资料', '当您通过 WhatsApp、电话或电邮联系我们时，我们会收到您选择提供的资料，例如姓名、电话号码、车型和车辆照片。'),
        ('资料用途', '这些资料只用于回复您、报价以及为您的车辆施工。我们不会出售您的资料。'),
        ('网站点击', '本网站会统计联系按钮（WhatsApp、电话、电邮、地图）的点击次数，以了解哪些按钮被使用。不会记录您的姓名或电话号码。'),
        ('您的选择', '如需查询我们保存的您的资料或要求删除，请电邮 mcs01092020@gmail.com 或 WhatsApp 016-556 2998。'),
    ],
}

ARTICLES = {
    'title': '汽车喷漆与钣金文章 | MCS Auto Spray Painting',
    'meta': '来自依斯干达公主城武吉英达花园 MCS Auto Spray Painting 的汽车喷漆、颜色与钣金维修文章。',
    'h1': '文章',
    'empty': '车厂的文章很快会在这里发布。在此之前，欢迎用 WhatsApp 向我们提问。',
}

PHOTOS = {
    'cover': '糖果青蓝 Toyota Vellfire 停在武吉英达花园 Jalan Indah 16/11 的 MCS Auto Spray Painting 店前',
    'vellfire-front': '完成改色后的糖果青蓝 Vellfire 车头，停在武吉英达街道上',
    'vellfire-rear': '同一辆 Vellfire 的车尾，展示日光下的珍珠漆面',
    'vellfire-unit-57': '57号单位内的 Vellfire，上方是 MCS AUTO SPRAY PAINTING 招牌',
    'vellfire-booth': '喷漆房内施工中的 Vellfire，车窗用报纸和胶带遮蔽',
    'handover': '与完工的糖果青蓝 Vellfire 合影竖起大拇指',
    'mclaren-shopfront': 'MCS AUTO SPRAY PAINTING 招牌下的亮黑色 McLaren',
    'lotus-booth': '舞狮到访时，停在 MCS 喷漆房内的赛车绿 Lotus',
    'panels-booth': '喷漆房内架子上刚喷好的红色和黑色板件',
    'shopfront-booth': 'MCS 招牌下的喷漆房门和技师',
    'signboard': 'MCS 招牌：Pusat Kecantikan Kereta、MCS BODY & PAINT 盾牌和 MCS AUTO SPRAY PAINTING 字样',
    'motorbike': 'MCS 车厂地面上的绿色探险摩托车',
    'upholstery-bay': '内饰间里的座椅和成卷的面料',
    'door-panel': '翻新成米色配黑色双色、白色缝线的门板',
    'seats': '翻新成米色配黑色双色的前座椅',
}

SCHEMA = {
    'description': '位于柔佛依斯干达公主城武吉英达花园的汽车喷漆与钣金车厂：全车与局部喷漆、糖果色与珍珠色定制、事故钣金维修、Nippon AI-PPS 漆面保护、内饰维修、保险与挡风玻璃索赔、摩托车喷漆。',
}

LLMS = {
    'intro': '位于马来西亚新山依斯干达公主城武吉英达花园的汽车喷漆、钣金与内饰车厂。招牌：Pusat Kecantikan Kereta。',
}
