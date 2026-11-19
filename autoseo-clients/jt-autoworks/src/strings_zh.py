# JT Autoworks, 简体中文文案。键与 strings_en.py 完全相同 (缺少任何键，build 会失败)。
# 事实资料 (号码、地址、价格、营业时间) 来自 facts.json; {placeholder} 由 build.py 填入。
# 规则: 不用破折号，不加未经证实的资料，老板姓名只通过 {tech} 使用。

UI = {
    'skip': '跳到内容',
    'menu': '菜单', 'close': '关闭菜单', 'lang': '语言',
    'wa_btn': 'WhatsApp 我们', 'wa_short': 'WhatsApp', 'call_btn': '致电 6222 3102', 'call_short': '致电',
    'home': '首页', 'packages': '套餐', 'services': '服务', 'find_us': '如何找到我们', 'about': '关于我们',
    'areas': '服务地区', 'articles': '文章', 'privacy': '隐私',
    'breadcrumb': '导航路径',
    'prev': '上一张照片', 'next': '下一张照片',
    'play': '播放视频', 'tap_sound': '点击开启声音', 'load_fb': '点击后将从 Facebook 播放',
    'watch_more': '到 Facebook 看更多',
    'hours_h': '营业时间', 'mon_fri': '星期一至星期五', 'sat': '星期六', 'sun': '星期日', 'closed': '休息',
    'hours_mf': '上午9:00至下午5:00', 'hours_sat': '上午9:00至下午3:00', 'hours_short': '周一至周五 上午9点至下午5点，周六 上午9点至下午3点，周日休息',
    'address_h': '车厂地址', 'contact_h': '联络我们',
    'maps': '在 Google Maps 打开', 'directions': '获取路线', 'reviews': '查看我们的 Google 评价', 'write_review': '撰写 Google 评价',
    'facebook': 'Facebook', 'instagram': 'Instagram', 'email': '电邮',
    'credit': 'Website by AutoSEO.my',
    'per_litre': '每额外一公升', 'litres': '公升', 'for3': '共3次服务',
    'pkg_wa': 'WhatsApp 询问套餐 {L}',
    'see_packages': '查看三个套餐', 'see_services': '所有服务', 'see_find': '如何找到我们',
    'faq_h': '常见问题',
    'map_title': 'JT Autoworks 在 Premier @ Kaki Bukit 的地图',
    'all_makes': '欢迎各种车款。',
    'reel_more': '更多车厂短片',
    'legal': 'JT AUTOWORKS PTE. LTD.',
}

TECH = '我们的技师'          # used while facts.flags.show_owner_name is false
TECH_CAP = '我们的技师'

# ---------- WhatsApp prefills (per page / per button) ----------
PREFILL = {
    'default': "你好 JT Autoworks, 我想询问我的车。车型和年份: ",
    'home': "你好 JT Autoworks, 我想询问我的车。车型和年份: ",
    'pkg_a': "你好 JT Autoworks, 我想询问套餐 A (Liqui Moly Top Tec, 6L, $628)。",
    'pkg_b': "你好 JT Autoworks, 我想询问套餐 B (Castrol Edge, 6L, $528)。",
    'pkg_c': "你好 JT Autoworks, 我想询问套餐 C (Castrol Edge, 4L, $428)。",
    'packages': "你好 JT Autoworks, 我想知道哪个服务套餐适合我的车。车型和年份: ",
    'services': "你好 JT Autoworks, 我想询问维修事宜。车型和年份: ",
    'diagnostics': "你好 JT Autoworks, 我想为我的车做检测。车子的状况: ",
    'aircon': "你好 JT Autoworks, 我的车冷气不冷。车型和年份: ",
    'battery': "你好 JT Autoworks, 我想检测车子的电池。车型和年份: ",
    'ev': "你好 JT Autoworks, 我想询问我的电动车。车型和年份: ",
    'ppi': "你好 JT Autoworks, 我想做购车前检查。车型和年份: ",
    'towing': "你好 JT Autoworks, 我需要拖车。我的位置: ",
    'german': "你好 JT Autoworks, 我想询问我的车。品牌、车型和年份: ",
    'find_us': "你好 JT Autoworks, 我需要前往 #02-52, 1号门 (Gate 1) 的路线。",
    'about': "你好 JT Autoworks, 我想询问我的车。车型和年份: ",
    'areas': "你好 JT Autoworks, 我想把车开过去。车型和年份: ",
    'articles': "你好 JT Autoworks, 我想询问我的车。车型和年份: ",
    'privacy': "你好 JT Autoworks, 我有个问题。",
    'reel_aircon': "你好 JT Autoworks, 我的车冷气不冷。车型和年份: ",
    'reel_battery': "你好 JT Autoworks, 我想检测车子的电池。车型和年份: ",
    'reel_ev_light': "你好 JT Autoworks, 我的电动车亮起了警告灯。车型和年份: ",
    'reel_dash_lights': "你好 JT Autoworks, 我的仪表板亮起了警告灯。车型和年份: ",
    'reel_ev_owners': "你好 JT Autoworks, 我想询问电动车的保养。车型和年份: ",
    'reel_diagnostics': "你好 JT Autoworks, 我想为我的车做检测。车子的状况: ",
    'reel_used_car': "你好 JT Autoworks, 我想做购车前检查。车型和年份: ",
    'reel_oil_leak': "你好 JT Autoworks, 我觉得我的车漏油。车型和年份: ",
    'reel_bmw5': "你好 JT Autoworks, 我的车行驶时一顿一顿的。车型和年份: ",
    'reel_new_chapter': "你好 JT Autoworks, 我想询问我的车。车型和年份: ",
}

# ---------- Reel captions (plain language, not the promo text) ----------
REELS = {
    'aircon': '冷气不冷? 先找出漏气处。',
    'battery': '更换电池前先检测。',
    'ev_light': '电动车警告灯，认真检查。',
    'dash_lights': '仪表板警告灯想告诉你什么。',
    'ev_owners': '电动车过了保修期后的保养。',
    'diagnostics': '先找出根本原因，再维修。',
    'used_car': '付款前先检查二手车。',
    'oil_leak': '追查漏油的源头。',
    'bmw5': 'BMW 5 Series 一顿一顿的故障，已找出原因。',
    'new_chapter': '我们在 Premier @ Kaki Bukit 的新车厂。',
}

# ---------- Shared blocks ----------
PKG = {
    'h2': '服务套餐',
    'lead': '三个套餐，每个包含3次服务。价格清楚列明。',
    'name': '套餐 {L}',
    'oil_line': '{oil}, {litres}L 引擎油',
    'extra': '额外引擎油每公升 ${x}',
    'inc_h': '每个套餐都包括',
    'common': {
        'oil_filter': '机油滤芯 x{n}',
        'check_50': '50项检查 x{n}',
        'aircon_flush_gas': '冷气管清洗及补气 x{n}',
        'tyre_rotation': '轮胎调位 x{n}',
        'tyre_patch': '补胎 x{n}',
        'coolant': '补充冷却液，最多10L, x{n}',
    },
    'flush': 'Liqui Moly 引擎清洗剂、机油添加剂及喷油嘴清洁剂',
    'windshield': 'Liqui Moly 挡风玻璃清洁剂 50ml',
    'no_flush': '不含清洗剂组合及挡风玻璃清洁剂',
    'brake_fluid': '只有更换刹车片时才会清洗刹车油。',
    'lifetime': '套餐客户享有终身免费检查。',
    'visc': '海报上的机油级别: {v}。',
    'poster_alt': 'JT Autoworks 套餐 {L} 价格海报',
    'combined_alt': 'JT Autoworks 服务套餐 A、B 和 C 并排对照',
}

PROCESS = {
    'h2': '我们的工作流程',
    'lead': '先检测，后换零件。',
    'steps': [
        ('WhatsApp 我们', '告诉我们车型和车子的状况。附上短视频会更有帮助。'),
        ('检查与诊断', '我们先找出根本原因，再谈零件。'),
        ('免费报价', '报价不设任何义务，也不收费。'),
        ('只修需要修的', '零件只在真正需要时才更换。'),
        ('取车', '你的爱车交给我们，可以放心。'),
    ],
}

PROOF = {
    'h2': '车主为什么再次光顾',
    'items': [
        ('工钱 $50', '别处报价接近 $2,000 的涡轮问题，在这里只收 $50 工钱就修好，零件没有另外收费。'),
        ('别家车厂没找出的故障', '一辆老是一顿一顿的 BMW 5 Series 曾在别处检查过。我们找出了真正的原因。'),
        ('自 2018 年。一位技师。', '一份建立在信任上的关系。'),
    ],
    'note': 'JT Autoworks 于 2026 年 5 月在 Premier @ Kaki Bukit 开业。',
    'reviews_line': '看看客户在 Google 上的留言。',
}

PHOTOS = {
    'h2': '车厂内部',
    'shopfront-corridor-tighter-4x5': 'JT Autoworks 在 #02-52 的招牌',
    'mercedes-c-class-on-lift-4x5': '一辆 Mercedes-Benz 在 JT Autoworks 的升降机上',
    'volkswagen-golf-cabriolet-on-lift-4x5': '一辆 Volkswagen Golf Cabriolet 在 JT Autoworks 的升降机上',
    'shopfront-corridor-4x5': 'JT Autoworks 位于 Premier @ Kaki Bukit 的店面',
    'hero': 'JT Autoworks 位于 Premier @ Kaki Bukit #02-52 的店面',
}

GATE = {
    'h2': '找到我们: 1号门 (Gate 1), #02-52',
    'lead': 'Premier @ Kaki Bukit 有100多间车厂。请从1号门 (Gate 1) 进入，找 #02-52 的招牌。',
    'landmarks_h': '大楼附近的地标',
    'landmarks': {
        'Gate 1': '请使用 Premier @ Kaki Bukit 的1号门 (Gate 1)。',
        'VICOM Inspection Centre': 'VICOM Inspection Centre 是附近的地标。',
        'Kaki Bukit Camp': 'Kaki Bukit Camp 是附近的地标。',
        'Bartley Rd East': 'Bartley Rd East 就在附近。',
        'POSB': '附近有一间 POSB。',
    },
    'poster_alt': 'JT Autoworks 位置海报，标示1号门 (Gate 1) 和 #02-52',
    'poster_labels': '海报也标出了这栋大楼内的 Bike Labz、Sri Udhayan Coffee Bar、Atlas Vending Solutions 和 KB-1。',
    'lost': '在楼里迷路了? WhatsApp 我们，我们会带你到 #02-52。',
}

SERVICES = {
    'diagnostics': {
        'name': '车辆检测', 'card': '先找根本原因。不靠猜，也不乱换零件。',
        'title': 'Kaki Bukit 汽车检测 | JT Autoworks',
        'meta': '在 Premier @ Kaki Bukit 1号门 (Gate 1) 诚实检测汽车。我们先找出根本原因，只更换需要的零件。WhatsApp 8358 4927。',
        'h1': 'Kaki Bukit 汽车检测，先找根本原因',
        'lead': '警告灯亮、车子一顿一顿、有说不出来的怪声? 我们先检测，再更换。',
        'body': [
            '很多维修花费过高，是因为不断换零件直到问题消失。我们的做法相反: 先做好诊断，不靠猜测，不更换不必要的零件。',
            '有一个涡轮工作在别处报价接近 $2,000, 在这里只收 $50 工钱，零件没有另外收费。另一间车厂没找出的 BMW 5 Series 一顿一顿的故障，我们也查出并修好了。',
        ],
        'list_h': '我们检查的项目',
        'list': ['仪表板警告灯', '一顿一顿、迟滞和运转粗糙', '引擎故障和漏油漏液', '电路故障', '电动车警告灯'],
    },
    'aircon': {
        'name': '冷气', 'card': '不冷? 我们先找出漏气处，再修理。',
        'title': 'Kaki Bukit 汽车冷气维修 | JT Autoworks',
        'meta': '车子冷气不冷? 位于 Premier @ Kaki Bukit 的 JT Autoworks 先找出漏气处，再维修。冷气管清洗及补气。WhatsApp 8358 4927。',
        'h1': 'Kaki Bukit 汽车冷气维修',
        'lead': '不找漏气处就补气，只是拖延时间。我们先找漏气处。',
        'body': [
            '只补冷气不能解决漏气。我们在更换任何零件前先找出冷气漏气的原因，然后提供不设义务、不收费的报价。',
            '冷气管清洗及补气也包含在每个服务套餐里。',
        ],
        'list_h': '冷气工作',
        'list': ['找漏气处', '冷气管清洗', '补气', '修理漏气的零件'],
    },
    'battery': {
        'name': '电池', 'card': '先检测，需要才更换，并做电池注册和编码。',
        'title': 'Kaki Bukit 汽车电池检测与更换 | JT Autoworks',
        'meta': '在 Premier @ Kaki Bukit 的 JT Autoworks, 汽车电池先检测。需要才更换，并做电池注册和编码。WhatsApp 8358 4927。',
        'h1': 'Kaki Bukit 汽车电池检测与更换',
        'lead': '我们先检测电池。真的需要换才换。',
        'body': [
            '发动缓慢不一定是电池坏了。我们先检测电池和充电系统，让你不必为不需要的电池付钱。',
            '许多现代汽车，换上新电池后必须向车子注册和编码。我们会把这一步一并做好。',
        ],
        'list_h': '电池工作',
        'list': ['电池及充电检测', '需要时才更换', '电池注册和编码'],
    },
    'ev': {
        'name': '电动车检测与保养', 'card': '受过电动车训练的技师。过了保修期后的实惠选择。',
        'title': 'Kaki Bukit 电动车车厂 | JT Autoworks',
        'meta': '在 Premier @ Kaki Bukit 由受过电动车训练的技师做电动车检测与保养。原厂保修期后的实惠选择。WhatsApp 8358 4927。',
        'h1': 'Kaki Bukit 电动车车厂，检测与保养',
        'lead': '受过电动车训练的技师，先检测，适合原厂保修期结束后。',
        'body': [
            '原厂保修期一过，许多电动车车主都想找实惠的选择。我们受过电动车训练的技师，在 Premier @ Kaki Bukit 负责电动车检测与保养。',
            '电动车警告灯和其他故障一样处理: 在更换任何零件前先找出原因。电动车也可以安排拖车。',
        ],
        'list_h': '电动车工作',
        'list': ['电动车警告灯检测', '电动车保养', '为电动车安排拖车'],
        'tags': '这些电动车的车主常来询问我们:',
    },
    'ppi': {
        'name': '购车前检查', 'card': '付款前，好好检查二手车。',
        'title': 'Kaki Bukit 购车前检查 | JT Autoworks',
        'meta': '在 Premier @ Kaki Bukit 的 JT Autoworks 做二手车购车前检查。付款前先了解你买的是什么车。WhatsApp 8358 4927。',
        'h1': 'Kaki Bukit 购车前检查',
        'lead': '付款前，先了解你买的是什么车。',
        'body': [
            '二手车看起来干净，也可能藏着昂贵的问题。决定购买前先带来给我们，我们会检查并坦白告诉你发现了什么。',
        ],
        'list_h': '我们检查什么',
        'list': ['引擎和变速箱', '刹车和悬挂', '冷气和电子系统', '漏油、磨损和事故痕迹'],
    },
    'towing': {
        'name': '24小时拖车', 'card': '全天候安排拖车，汽车和电动车都可以。',
        'title': '安排24小时汽车及电动车拖车 | JT Autoworks Kaki Bukit',
        'meta': '车子抛锚? JT Autoworks 安排24小时拖车，把汽车和电动车拖到 Premier @ Kaki Bukit 1号门 (Gate 1) 的车厂。WhatsApp 8358 4927。',
        'h1': '为汽车和电动车安排24小时拖车',
        'lead': '车子抛锚? WhatsApp 你的位置给我们，我们来安排拖车。',
        'body': [
            '我们为汽车和电动车安排24小时拖车，送到 Premier @ Kaki Bukit 的车厂。请通过 WhatsApp 发送你的位置和车型，让我们安排合适的拖车。',
            '车子到了我们这里，同样先检测: 先找根本原因，然后提供不设义务、不收费的报价。',
        ],
        'list_h': '请通过 WhatsApp 发给我们',
        'list': ['你的位置', '车子品牌和车型，或电动车车型', '发生了什么事'],
    },
    'german': {
        'name': '德国车及豪华车', 'card': 'BMW、Mercedes-Benz、Audi、Porsche 等。欢迎各种车款。',
        'title': 'Kaki Bukit BMW、Mercedes 和 Audi 车厂 | JT Autoworks',
        'meta': '位于 Premier @ Kaki Bukit 的欧洲车及豪华车车厂: BMW、Mercedes-Benz、Audi、Volkswagen、Porsche、Lexus、Land Rover、Volvo。欢迎各种车款。',
        'h1': 'Kaki Bukit BMW、Mercedes 和 Audi 车厂',
        'lead': '专注欧洲车和豪华车，欢迎各种车款。',
        'body': [
            '德国车和豪华车是我们的专长: BMW、Mercedes-Benz、Audi、Volkswagen 和 Porsche, 还有 Lexus、Land Rover 和 Volvo。这些车值得仔细检测，靠猜是行不通的。',
            '一辆老是一顿一顿的 BMW 5 Series 已经去过另一间车厂。我们找出了真正的故障。不论你开什么车，我们的做法都一样。',
        ],
        'list_h': '我们专注的车款',
    },
}
SERVICE_ORDER = ['diagnostics', 'aircon', 'battery', 'ev', 'ppi', 'towing', 'german']
OTHER_SERVICES = {
    'h2': '车厂其他服务',
    'items': [('引擎维修', '先检测，再好好修理。'), ('刹车', '刹车检查与维修。'),
              ('换机油', '或选择三个套餐之一更省。'), ('50项检查', '每个套餐服务都包括。')],
}
CHECK_50 = {
    'engine': '引擎', 'brakes': '刹车', 'suspension_steering': '悬挂及方向盘', 'tyres': '轮胎',
    'electrical': '电路', 'lights': '灯光', 'fluids': '油液', 'aircon': '冷气',
    'battery_charging': '电池及充电', 'exhaust': '排气管', 'safety': '安全配备', 'body_interior': '车身及内饰',
}

# ---------- Pages ----------
HOME = {
    'title': 'Kaki Bukit 先检测的汽车维修厂 | JT Autoworks',
    'meta': 'JT Autoworks, 位于 Premier @ Kaki Bukit 1号门 (Gate 1), #02-52 的汽车维修厂。先检测的欧洲车及电动车专家，套餐价格清楚，欢迎各种车款。',
    'h1': 'Kaki Bukit 先检测的汽车维修厂',
    'line': '欧洲车及电动车专家。我们只修需要修的。',
    'chips': [('先检测', '先找根本原因，再换零件'), ('免费报价', '不设义务，不收费'), ('#02-52, 1号门', 'Premier @ Kaki Bukit')],
    'intro_h': 'Premier @ Kaki Bukit 的汽车维修厂，先说明再收费',
    'intro': 'JT Autoworks 是 Kaki Bukit 一间先检测的汽车维修厂，位于 Premier @ Kaki Bukit 的 #02-52。我们专注于 BMW、Mercedes-Benz、Audi 等欧洲车和电动车，也欢迎各种车款。报价不设义务、不收费，零件只在必要时才更换。',
    'svc_h': '我们的服务',
    'lounge': '等车吗? 这里有休息室，备有免费饮料。',
    'final_h': '告诉我们你的车怎么了',
    'final_line': 'WhatsApp 8358 4927。附上问题的短视频会更有帮助。',
    'faq': [
        ('你们的营业时间是?', '星期一至星期五上午9:00至下午5:00, 星期六上午9:00至下午3:00。星期日休息。'),
        ('车厂确切在哪里?', 'Unit #02-52, Premier @ Kaki Bukit, 8 Kaki Bukit Ave 4, Singapore 415875。请从1号门 (Gate 1) 进入。'),
        ('报价要收费吗?', '不用。报价不设义务，也不收费。'),
        ('服务套餐包括什么?', '每个套餐包含3次服务，每次都有引擎油、机油滤芯、50项检查和补充冷却液，另外包括冷气管清洗及补气、轮胎调位和补胎各一次。'),
        ('你们修电动车吗?', '修。受过电动车训练的技师负责电动车检测与保养，也可以为电动车安排拖车。'),
        ('你们保养哪些车款?', '我们专注于 BMW、Mercedes-Benz、Audi、Volkswagen、Porsche、Lexus、Land Rover 和 Volvo。欢迎各种车款。'),
    ],
}

PACKAGES = {
    'title': 'Kaki Bukit 引擎油服务套餐 | JT Autoworks',
    'meta': 'JT Autoworks Kaki Bukit 的三个引擎油服务套餐: A $628 Liqui Moly Top Tec 6L, B $528 Castrol Edge 6L, C $428 Castrol Edge 4L。每个包含3次服务。',
    'h1': 'Kaki Bukit 引擎油服务套餐',
    'lead': '三个套餐，每个3次服务，价格清楚列明。',
    'compare_h': '三个套餐一张海报看清',
    'faq': [
        ('一个套餐包含几次服务?', '每个套餐包含3次服务。'),
        ('套餐之间有什么不同?', '套餐 A 使用 6L Liqui Moly Top Tec ($628)。套餐 B 使用 6L Castrol Edge ($528)。两者都包括 Liqui Moly 引擎清洗剂、机油添加剂和喷油嘴清洁剂，以及 50ml Liqui Moly 挡风玻璃清洁剂。套餐 C 使用 4L Castrol Edge ($428), 不含清洗剂组合和挡风玻璃清洁剂。'),
        ('我的车需要更多引擎油怎么办?', '额外引擎油，套餐 A 每公升 $29, 套餐 B 和 C 每公升 $20。'),
        ('配套列出哪些机油级别?', '配套海报列出 5W-40、5W-30 和 0W20。'),
        ('包括刹车油吗?', '只有更换刹车片时才会清洗刹车油。'),
        ('3次服务之后还有什么吗?', '套餐客户享有终身免费检查。'),
    ],
}

SERVICES_PAGE = {
    'title': 'Kaki Bukit 汽车维修与保养 | JT Autoworks',
    'meta': '在 Premier @ Kaki Bukit 1号门 (Gate 1) 的 JT Autoworks, 提供检测、冷气、电池、电动车保养、购车前检查、拖车及欧洲车维修。',
    'h1': 'Kaki Bukit 汽车维修与保养',
    'lead': '每项工作都从检测开始。欢迎各种车款。',
}

FIND = {
    'title': '如何找到 Premier @ Kaki Bukit 1号门的 JT Autoworks',
    'meta': 'JT Autoworks 位于 8 Kaki Bukit Ave 4, #02-52, Premier @ Kaki Bukit, Singapore 415875。请从1号门 (Gate 1) 进入。地图、路线和营业时间。',
    'h1': '如何在 Premier @ Kaki Bukit 找到我们',
    'lead': '从1号门 (Gate 1) 进入，然后找 #02-52 单位。',
}

ABOUT = {
    'title': '关于 JT Autoworks, Kaki Bukit 的新车厂',
    'meta': 'JT Autoworks 于 2026 年 5 月在 Premier @ Kaki Bukit 开业: 专门服务欧洲车和电动车、先检测的车厂，价格清楚，报价免费。',
    'h1': '关于 JT Autoworks',
    'lead': 'Kaki Bukit 的新车厂，沿用老习惯: 先检测。',
    'body': [
        'JT Autoworks 于 2026 年 5 月在 Premier @ Kaki Bukit 的 #02-52 开业。车厂是新的，做法却不是。',
        '自 2018 年。一位技师。一份建立在信任上的关系。做法始终如一: 找出真正的原因，解决真正的问题，只在必要时才更换零件。',
        '我们专注于欧洲车和电动车，也欢迎各种车款。报价不设义务、不收费，三个服务套餐的价格也清楚列明。',
    ],
    'values_h': '你可以期待',
    'values': [('回复快', '有问题就 WhatsApp 我们，我们会尽快回复。'),
               ('诚实检测', '先找根本原因。不靠猜，也不乱换零件。'),
               ('价格清楚', '套餐价格清楚列明，报价不收费。'),
               ('做事可靠', '专业手艺，一次就做好。')],
    'lounge': '等车时，这里有休息室，备有免费饮料。',
}

AREAS = {
    'title': 'Ubi、Eunos、Bedok 和 Tampines 附近的汽车维修厂 | JT Autoworks',
    'meta': 'JT Autoworks 服务来自 Kaki Bukit、Ubi、Eunos、Bedok、Tampines、Paya Lebar、MacPherson 和 Hougang 的车主，位于 Premier @ Kaki Bukit 1号门 (Gate 1)。',
    'h1': 'Kaki Bukit 及附近地区的汽车维修厂',
    'lead': '一间车厂，一个地址: Premier @ Kaki Bukit, 1号门 (Gate 1), #02-52。',
    'area_h': '{area}车主的汽车维修厂',
    'area_p': '从{area}开车过来? JT Autoworks 位于 Premier @ Kaki Bukit。请从1号门 (Gate 1) 进入，找到 #02-52。先检测，报价不收费，三个服务套餐的价格也清楚列明。',
    'here_p': '我们就在 Kaki Bukit, 位于 Premier @ Kaki Bukit, 8 Kaki Bukit Ave 4。请从1号门 (Gate 1) 进入，找到 #02-52。',
}

PRIVACY = {
    'title': '隐私 | JT Autoworks',
    'meta': 'JT Autoworks 如何处理你联络我们时提供的资料。',
    'h1': '隐私',
    'body': [
        ('我们收集什么', '当你通过 WhatsApp、电话或电邮联络我们，我们会收到你选择提供的资料，例如姓名、号码、车型，以及问题的照片或视频。'),
        ('我们如何使用', '我们只用这些资料来回复你、报价和为你的车进行维修。我们不会出售你的资料。'),
        ('网站点击记录', '本网站会统计联络按钮 (WhatsApp、电话、电邮、地图) 的点击次数，以了解哪些按钮被使用。网站不会记录你的姓名或号码。'),
        ('你的选择', '如要查询我们持有你的哪些资料，或要求删除，请电邮 hao@jtautoworks.com.sg 或 WhatsApp 8358 4927。'),
    ],
}

ARTICLES = {
    'title': '汽车保养文章 | JT Autoworks Kaki Bukit',
    'meta': 'JT Autoworks 的汽车保养文章。我们是位于 Premier @ Kaki Bukit、先检测的车厂。',
    'h1': '汽车保养文章',
    'empty': '车厂的文章很快会在这里出现。在那之前，欢迎 WhatsApp 你的问题给我们。',
}

SCHEMA = {
    'description': '位于 Premier @ Kaki Bukit 1号门 (Gate 1), #02-52 的先检测汽车维修厂。欧洲车及电动车专家，欢迎各种车款。',
}
LLMS = {
    'intro': 'JT Autoworks (JT AUTOWORKS PTE. LTD.) 是位于新加坡 Premier @ Kaki Bukit 的先检测汽车维修厂，专注于欧洲车和电动车，欢迎各种车款。',
}

# ---------- redesign blocks (20 Nov) ----------
LOOK = {
    'poster_alt': 'JT Autoworks 海报: {name}',
    'kicker': 'Premier @ Kaki Bukit，1号门，#02-52',
    'reels_h': '视频精选',
    'reels_lead': '车厂里的短片，点一下就能播放。',
    'pkg_kicker': '价格清楚',
    'quotes_h': '客户怎么说',
    'quotes': ['他对汽车的认识和维修技术一流。',
               '把保养和维修交给他们，我完全不用担心！',
               '我相信诚信和诚实是汽车维修行业最重要的品质。'],
    'quote_src': '摘自 Google 评价',
    'about_more': '了解车厂',
    'gallery_lead': '#02-52 单位的真实照片。',
}
