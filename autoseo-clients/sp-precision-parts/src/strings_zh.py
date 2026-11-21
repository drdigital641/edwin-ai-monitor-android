# Simplified Chinese (Malaysia) strings for the S & P Precision Parts (Monaer) site. Same keys as strings_en.py.
# Facts (phone, address, company no., maker claims) live in facts.json. No prices, warranty, stock counts, origin
# country, workshop names or fitment years here: none are confirmed yet.

UI = {
    'skip': '跳到内容', 'menu': '菜单', 'close': '关闭菜单', 'lang': '语言',
    'home': '首页', 'products': '产品', 'finder': '查刹车片', 'locator': '找维修厂',
    'join': '维修厂合作', 'faq': '常见问题', 'contact': '联系我们', 'articles': '文章', 'privacy': '隐私',
    'breadcrumb': '页面路径',
    'wa_btn': '用 WhatsApp 查我的车', 'wa_short': 'WhatsApp', 'call_btn': '致电 {PHONE}', 'call_short': '致电',
    'join_btn': '申请成为授权维修厂', 'locator_btn': '找维修厂',
    'finder_btn': '打开刹车片查询', 'see_more': '查看详情', 'all_products': '全部产品',
    'tagline': '新山士姑来授权 Monaer 刹车配件代理。',
    'contact_h': '联系我们', 'follow_h': '关注我们', 'facebook': 'Facebook 专页', 'maps': 'Google Maps', 'waze': 'Waze',
    'email': '电邮联系', 'address_h': '地址', 'company': '公司注册号',
    'faq_h': '车主和维修厂常问的问题',
    'maker_note': '本网站的产品资料以 Monaer Brake System Malaysia 发布的为准。想知道您那款配件的详情，请询问我们。',
    'safety': '刹车是安全部件。安装前，请务必先向我们或您的维修厂确认适合您爱车的配件。',
    'sample': '目录示例',
    'steps_h': '如何为您的车配上 Monaer 刹车片',
    'steps': [
        ('发送车辆资料', '通过 WhatsApp 告诉我们品牌、车型、年份和引擎。附上路税或旧刹车片的照片更好。'),
        ('我们帮您配对', '我们会把 Monaer 目录编号和您爱车的原厂零件编号核对。'),
        ('到车行安装', '可到士姑来我们这里取货，或到您附近的 Monaer 车行安装。'),
    ],
    'privacy_line': '发送即表示您同意我们只用这些资料来回复您（PDPA）。',
    'opens_wa': '这会打开 WhatsApp，并填好您的资料。本网站不会保存任何资料。',
}

PREFILL = {
    'default': '你好 S & P Precision Parts，我想查询适合我的车的 Monaer 刹车片。车型和年份：',
    'contact': '你好 S & P Precision Parts，我想询问有关 Monaer 刹车配件的问题：',
    'pads': '你好，请帮我查适合我的车的 Monaer 刹车片。品牌 / 车型 / 年份：',
    'discs': '你好，请帮我查适合我的车的 Monaer 刹车碟。品牌 / 车型 / 年份：',
    'care': '你好，我想询问 Monaer 刹车清洁剂和维修厂用品：',
    'locator': '你好，我附近哪间维修厂可以安装 Monaer 刹车配件？我的地区：',
    'join': '你好，我的维修厂想成为 Monaer 授权维修厂。维修厂名称和城镇：',
    # finder / join forms build these with the filled fields
    'f_intro': '你好，请帮我查适合我的车的 Monaer 刹车片。',
    'f_make': '品牌', 'f_model': '车型', 'f_year': '年份', 'f_axle': '前 / 后', 'f_part': '零件编号或 OE 编号',
    'j_intro': '你好，我的维修厂想成为 Monaer 授权维修厂。',
    'j_name': '维修厂', 'j_person': '联络人', 'j_town': '城镇', 'j_state': '州属', 'j_phone': '电话', 'j_bays': '工作位数量', 'j_note': '备注',
}

HOME = {
    'title': 'Monaer 摩纳尔刹车片和刹车碟 | S & P Precision Parts',
    'meta': '士姑来授权代理供应 Monaer 纳米陶瓷刹车片、涂层刹车碟和刹车油。用 WhatsApp 查您的车，或找附近的维修厂。',
    'h1': 'Monaer 摩纳尔刹车片和刹车碟',
    'line': '纳米陶瓷刹车片，按您的车配对。一分钟就能查。',
    'stop_label': 'Monaer 刹车碟',
    'two_h': '两种方式，为爱车换上 Monaer',
    'two': [
        ('车主', '告诉我们您的车。我们为您配对 Monaer 配件，并介绍可以安装的维修厂。', 'finder'),
        ('维修厂', '直接向代理进 Monaer 货，并列入我们的维修厂查询。', 'join'),
    ],
    'why_h': 'Monaer 刹车片有什么不同',
    'why_p': '以下资料以 Monaer Brake System Malaysia 发布的为准。',
    'why': [
        ('纳米陶瓷刹车片', 'Monaer 刹车片采用纳米陶瓷摩擦材料，针对日常路况下刹车安静、轮圈干净而设计。'),
        ('耐高温', 'Monaer 列明抗热衰退可达 600°C，性能款可达 800°C，刹车热了咬力依然稳定。'),
        ('每盒配齐工具', '每套刹车片附有刹车清洁喷剂、手套和高温防噪音润滑脂。做这个工作不用另外再买。'),
        ('刹车片、刹车碟、刹车油，一个品牌搞定', '有涂层高碳刹车碟、DOT 4 和 DOT 5.1 刹车油，也有为 EV 设计的刹车片系列。'),
    ],
    'feel_h': '上路后您会感觉到',
    'feel': ['咬力强而稳定', '刹车更安静', '轮圈的黑粉更少', '刹车热了依然稳定', '刹车碟更耐用'],
    'feel_note': '以上是 Monaer 为其纳米陶瓷刹车片列出的特点。',
    'range_h': 'Monaer 产品系列',
    'finder_h': 'Monaer 有适合我的车的刹车片吗？',
    'finder_p': 'Monaer 涵盖日常用车、高端车款和 EV。把您的车发给我们，我们帮您核对确切的配件。',
    'locator_h': '找 Monaer 维修厂',
    'locator_p': '向我们询问离您最近的 Monaer 安装点，或申请成为授权维修厂。',
    'compare_h': '陶瓷还是半金属？',
    'compare_p': '马来西亚市面上的刹车片，大多是这两种之一。简单说明差别如下。',
    'compare_rows': [
        ('噪音', '较安静', '可能较容易发出尖叫声'),
        ('轮圈粉尘', '粉尘少，颜色浅', '黑粉较多'),
        ('刹车碟磨损', '对刹车碟较温和', '刹车碟磨损较快'),
        ('适合', '日常驾驶、市区和高速公路', '重载、高强度使用'),
    ],
    'compare_cols': ('', '纳米陶瓷（Monaer）', '半金属'),
    'faq': [
        ('S & P Precision Parts 是 Monaer 的授权代理吗？', '是的。位于柔佛士姑来的 S & P Precision Parts Sdn Bhd 是 Monaer 刹车配件的授权代理。'),
        ('我怎么知道哪款 Monaer 刹车片适合我的车？', '用 WhatsApp 把车的品牌、车型、年份和引擎发给我们。购买前，我们会把 Monaer 目录编号和您爱车的原厂零件编号核对。'),
        ('可以直接买，还是一定要通过维修厂？', '请用 WhatsApp 询问我们。我们会告诉您在哪里取货，以及您附近哪间维修厂可以安装。'),
    ],
}

PRODUCTS = {
    'title': 'Monaer 刹车产品：刹车片、刹车碟、刹车保养 | S & P',
    'meta': '马来西亚 Monaer 刹车产品系列：陶瓷刹车片、刹车碟、刹车清洁剂和维修厂用品。欢迎向士姑来的 S & P Precision Parts 查询。',
    'h1': 'Monaer 刹车产品',
    'lead': '刹车片、刹车碟和刹车保养用品，同一个品牌，由柔佛士姑来供应。',
}

# one entry per product group page (build.py GROUPS drives menus, hub, pages, sitemap)
PG = {
    'pads': {
        'name': '刹车片', 'chip': '刹车片',
        'title': 'Monaer 纳米陶瓷刹车片 | S & P Precision Parts',
        'meta': 'Monaer 纳米陶瓷刹车片：安静、少粉尘、耐高温，每盒附安装工具。由柔佛士姑来授权代理按您的车配对。',
        'h1': 'Monaer 纳米陶瓷刹车片',
        'lead': '安静、少粉尘的刹车片，每盒附安装工具。',
        'line': '纳米陶瓷刹车片，适用于日常用车、高端车款和 EV。',
        'points': ['纳米陶瓷摩擦材料', '抗热衰退可达 600°C，性能款可达 800°C（以 Monaer 列明为准）',
                   '粉尘少，轮圈更干净', '刹车更安静，刹车碟更耐用',
                   '盒内工具：刹车清洁喷剂、手套和高温防噪音润滑脂', '一套 4 片，足够一个轴使用',
                   '有为 EV 设计的刹车片系列'],
        'body_h': '什么时候该换刹车片',
        'body': ['刹车时发出尖叫声或磨擦声', '踏板感觉变软，或踩得比以前深', '刹车时车子向一边偏',
                 '维修厂量出刹车片只剩约 3 毫米以下', '刹车警告灯亮起'],
        'faqs': [
            ('Monaer 刹车片的盒子里有什么？', '一套 4 片刹车片，足够一个轴使用，另附 Monaer 列明的安装工具：刹车清洁喷剂、手套和高温防噪音润滑脂。'),
            ('刹车片要成对更换吗？', '刹车片一定是按轴更换：前面两个轮子一起换，或后面两个轮子一起换。一套 Monaer 刹车片就是一个轴的分量。'),
            ('Monaer 有 EV 用的刹车片吗？', '有。Monaer 有为电动车重量设计的 EV 刹车片系列。请把您的 EV 车型发给我们查询。'),
        ],
    },
    'discs': {
        'name': '刹车碟', 'chip': '刹车碟',
        'title': 'Monaer 刹车碟 | 涂层高碳刹车碟 | S & P Precision Parts',
        'meta': 'Monaer 高碳刹车碟，防锈涂层，打孔加划线设计。用 WhatsApp 发来您的车型，向柔佛授权代理查询尺寸。',
        'h1': 'Monaer 刹车碟',
        'lead': '涂层高碳刹车碟，左右一对出售。',
        'line': '高碳刹车碟，银色防锈涂层。',
        'points': ['高碳刹车碟材质', '银色保护涂层，有助于防止雨天生锈和腐蚀',
                   '打孔加划线设计', '一盒装有左右一对',
                   '盒内附钢刷和超细纤维布', '按车款尺寸配对：购买前请确认车型、尺寸和规格'],
        'body_h': '刹车碟需要更换的迹象',
        'body': ['刹车时方向盘或踏板抖动', '刹车碟边缘有深沟或凸缘', '刹车碟表面出现蓝色过热痕迹',
                 '刹车碟已薄过上面所刻的最小厚度'],
        'faqs': [
            ('为什么 Monaer 刹车碟是银色的？', '银色那层是保护涂层，有助于防止生锈和腐蚀，对马来西亚的雨水和潮湿天气很有用。'),
            ('每次换刹车片都要换新刹车碟吗？', '不一定。维修厂会量刹车碟。如果厚度仍高于最小值而且表面平滑，只换新刹车片就可以了。'),
        ],
    },
    'care': {
        'name': '刹车油和刹车保养', 'chip': '刹车油和保养',
        'title': 'Monaer 刹车油 DOT 4 和 DOT 5.1、刹车清洁剂 | S & P',
        'meta': 'Monaer DOT 4 和 DOT 5.1 刹车油、刹车零件清洁剂和安装用品。由柔佛士姑来的 S & P Precision Parts 供应给维修厂和车主。',
        'h1': 'Monaer 刹车油和刹车保养',
        'lead': 'DOT 4 和 DOT 5.1 刹车油，以及让刹车工作做得干净利落的用品。',
        'line': 'DOT 4 和 DOT 5.1 刹车油、清洁喷剂、润滑脂和手套。',
        'points': ['Monaer 刹车油，有 DOT 4 和 DOT 5.1', 'Monaer 刹车零件清洁喷剂', '高温防噪音润滑脂', 'Monaer 工作手套'],
        'body_h': '刹车油需要更换的迹象',
        'body': ['手刹放下后刹车灯仍然亮着', '踏板感觉变软，或要踩得更深', '油壶里的刹车油看起来发黑',
                 '保养手册显示该换了'],
        'faqs': [
            ('DOT 4 还是 DOT 5.1：我的车该用哪一种？', '请用原厂指定的等级，会标示在油壶盖或车主手册上。不确定的话，把车型发给我们。'),
            ('你们有供应刹车保养用品给维修厂吗？', '有。请用 WhatsApp 告诉我们需要什么和数量。'),
        ],
    },
}

FINDER = {
    'title': 'Monaer 刹车片查询：查您的车 | S & P Precision Parts',
    'meta': '查查 Monaer 刹车片适不适合您的车。可按车辆品牌、车型或 Monaer 编号搜索，或用 WhatsApp 把车发给我们精确配对。',
    'h1': '为您的车查 Monaer 刹车片',
    'lead': '搜索目录，或把车发给我们，由我们帮您配对。',
    'search_h': '搜索目录',
    'search_label': '车辆品牌、车型或 Monaer 编号',
    'search_ph': '例如 Audi, Touareg 或 M0307',
    'none': '网上列表暂时还没有。请用 WhatsApp 发给我们，我们会查完整目录。',
    'list_note': '完整的 Monaer 目录正在陆续加入。目前列表只显示已发布的示例，所以购买前我们会通过 WhatsApp 逐辆核对。',
    'cols': ('Monaer 编号', '类型', '适用车款', '包装'),
    'type_pad': '纳米陶瓷刹车片', 'pack_4': '1 套 / 4 片',
    'form_h': '把您的车发给我们',
    'form_p': '填写您知道的资料。我们会回复配对的 Monaer 配件。',
    'f_make': '车辆品牌', 'f_model': '车型', 'f_model_ph': '例如 Myvi, X70, City', 'f_year': '年份', 'f_year_ph': '例如 2019',
    'f_axle': '前轮还是后轮', 'f_axle_opts': ['前轮', '后轮', '前后都要', '不确定'], 'f_part': '零件编号或 OE 编号（有的话）',
    'f_send': '发送到 WhatsApp', 'choose': '请选择',
    'read_h': '如何看懂 Monaer 刹车片盒子',
    'read': [
        ('Monaer 编号', 'Monaer 自己的零件编号，例如 M0307。一个编号可能适用于好几款车。'),
        ('车型和底盘代号', '这款刹车片适用的车款，括号里是底盘代号，例如 Audi A8L (D5/4N)。'),
        ('每套数量', '一套 4 片，足够一个轴的两个轮子使用。'),
    ],
    'faqs': [
        ('我的车不在列表里怎么办？', '大部分车款还没有上网。请用 WhatsApp 把车发给我们，我们会查完整目录。'),
        ('哪里可以找到原厂零件编号？', '在旧刹车片的底板上、您的维修发票上，或者问您的维修厂。用 WhatsApp 发旧刹车片的照片也可以。'),
    ],
}

LOCATOR = {
    'title': '马来西亚 Monaer 刹车维修厂 | S & P Precision Parts',
    'meta': '在马来西亚找安装 Monaer 刹车片和刹车碟的授权维修厂。可按州属搜索，或用 WhatsApp 询问离您最近的一间。',
    'h1': '在马来西亚找 Monaer 维修厂',
    'lead': '备有并安装 Monaer 刹车配件的授权维修厂。',
    'state_h': '选择您的州属',
    'all': '所有州属',
    'empty_h': '更多授权维修厂正在加入',
    'empty_p': '我们只列出已加入 Monaer 网络的维修厂。请用 WhatsApp 询问我们，我们会告诉您在您的地区哪里可以安装 Monaer。',
    'ask_btn': '询问我附近的维修厂',
    'card_call': '致电', 'card_map': '路线', 'card_wa': 'WhatsApp', 'dist_tag': '授权代理', 'dist_line': '供货、配件配对和取货。',
    'own_h': '您经营维修厂吗？',
    'own_p': '成为 Monaer 授权维修厂后，就可以列在这里。',
    'faqs': [
        ('维修厂是怎么列出来的？', '只有已加入成为 Monaer 授权维修厂的才会显示。没有维修厂同意，我们不会列出。'),
        ('我这个地区还没有维修厂，怎么办？', '请用 WhatsApp 告诉我们您的城镇。我们会告诉您最近哪里可以安装 Monaer 刹车配件。'),
    ],
}

JOIN = {
    'title': '成为 Monaer 授权维修厂 | S & P Precision Parts',
    'meta': '马来西亚维修厂：向柔佛授权代理进 Monaer 纳米陶瓷刹车片、刹车碟和刹车油，并列入我们的维修厂查询。',
    'h1': '成为 Monaer 授权维修厂',
    'lead': '直接进 Monaer 刹车配件货源，让附近的车主找到您。',
    'get_h': '您的维修厂能得到什么',
    'get': [
        ('直接供货', '直接向柔佛士姑来的授权代理订货。'),
        ('列入维修厂查询', '搜索 Monaer 的车主会看到您的维修厂、电话和地图链接。'),
        ('配件配对协助', '把车或 OE 编号发给我们，我们帮您找出 Monaer 配件。'),
        ('整个工作一个品牌', '刹车片、刹车碟、刹车油和刹车清洁剂，一张订单搞定。'),
    ],
    'form_h': '一分钟申请',
    'form_p': '您的资料会通过 WhatsApp 发给我们。我们会回复下一步和条件。',
    'f_name': '维修厂名称', 'f_person': '您的名字', 'f_town': '城镇', 'f_state': '州属', 'f_phone': '电话',
    'f_bays': '工作位数量', 'f_bays_opts': ['1 至 2', '3 至 5', '6 或以上'], 'f_note': '其他补充（选填）',
    'f_send': '用 WhatsApp 发送申请', 'choose': '请选择',
    'faqs': [
        ('加入要收费吗？', '请用 WhatsApp 询问我们。我们会直接向您说明您维修厂的条件。'),
        ('你们想找哪些地区的维修厂？', '柔佛和马来西亚各地的维修厂都可以申请。告诉我们您的城镇，我们会回复您那一带的可行方案。'),
    ],
}

FAQ_PAGE = {
    'title': 'Monaer 刹车片常见问题 | S & P Precision Parts',
    'meta': '关于马来西亚 Monaer 纳米陶瓷刹车片的解答：特点、耐热和粉尘、适用车款、刹车碟、刹车油、维修厂和如何加入。',
    'h1': 'Monaer 刹车配件：问与答',
    'lead': '给车主和维修厂的简短解答。',
    'items': [
        ('Monaer 刹车片有什么特别？', '采用纳米陶瓷材料：更安静、粉尘少、高温时依然稳定。每套还附有安装工具，包括清洁喷剂、手套和防噪音润滑脂。'),
        ('和我的车原厂的刹车片有什么不同？', '原厂刹车片满足基本使用。Monaer 表示其纳米陶瓷刹车片在市区路况和日常驾驶中，刹车更稳定、噪音和粉尘更少。'),
        ('纳米陶瓷还是半金属？', '半金属刹车片产生的黑粉较多。纳米陶瓷刹车片更干净、更安静，适合日常驾驶。'),
        ('能耐多高的温度？', 'Monaer 列明抗热衰退可达 600°C，性能款可达 800°C。想知道您那款配件的数据，请询问我们。'),
        ('怎么查 Monaer 适不适合我的车？', '使用刹车片查询，或用 WhatsApp 把车发给我们。购买前，我们会确认车型、尺寸和规格。'),
        ('你们也有刹车碟和刹车油吗？', '有。Monaer 有涂层高碳刹车碟，以及 DOT 4 和 DOT 5.1 刹车油。'),
        ('柔佛以外的地区有送货吗？', '请用 WhatsApp 告诉我们您的城镇，我们会告诉您有哪些选择。'),
        ('我的维修厂怎样进 Monaer 的货？', '请到“维修厂合作”页面申请。我们会通过 WhatsApp 回复下一步。'),
    ],
}

CONTACT = {
    'title': '联系 S & P Precision Parts | Monaer 代理 士姑来',
    'meta': '联系 Monaer 刹车配件授权代理 S & P Precision Parts Sdn Bhd：{PHONE}，No. 15 Jalan Selesa Indah 9, 81300 Skudai, Johor。',
    'h1': '联系 S & P Precision Parts',
    'lead': '用 WhatsApp 联系我们最快。',
    'about_h': '关于我们',
    'about_p': 'S & P Precision Parts Sdn Bhd 是 Monaer 刹车配件的授权代理，设在士姑来 Taman Selesa Indah。我们为车主和维修厂供应 Monaer 刹车片、刹车碟和刹车油，每件配件出货前都会先和车辆配对。',
}

ARTICLES = {
    'title': '刹车知识与资讯 | S & P Precision Parts（Monaer）',
    'meta': 'S & P Precision Parts 为马来西亚车主和维修厂提供刹车片和刹车碟小知识。我们是柔佛士姑来的 Monaer 授权代理。',
    'h1': '刹车知识与资讯',
    'empty': '适合马来西亚路况的刹车保养新文章即将推出。',
}

PRIVACY = {
    'title': '隐私政策 | S & P Precision Parts',
    'meta': 'S & P Precision Parts Sdn Bhd 如何依据马来西亚 PDPA 处理您的个人资料。',
    'h1': '隐私政策',
    'lead': '我们如何处理您的资料。',
    'body': [
        ('我们收集什么', '只收集您通过 WhatsApp、电话或电邮发给我们的资料，例如姓名、号码、车辆资料和所在地区。'),
        ('为什么收集', '用来回复您、为您的车配对刹车配件，以及安排供货或安装。'),
        ('本网站', '本网站的表格不会保存您的资料，只会打开 WhatsApp 并填好您的信息。我们会统计联系按钮的点击次数，但不收集姓名或号码。'),
        ('您的权利', '您可以随时通过 WhatsApp 或电邮，要求查看、更正或删除您的资料。'),
    ],
}

LLMS = {
    'intro': 'S & P Precision Parts Sdn Bhd（柔佛士姑来）是 Monaer 刹车配件的授权代理：纳米陶瓷刹车片、涂层高碳刹车碟、DOT 4 和 DOT 5.1 刹车油及刹车保养用品。车主可通过 WhatsApp 查询适用车款；维修厂可申请成为 Monaer 授权维修厂。',
}

ALT = {
    'monaer-kit': 'Monaer 刹车片、蓝色 Monaer 盒子、刹车零件清洁剂、润滑脂管和手套',
    'monaer-pads': '两套 Monaer 刹车片，显示摩擦面和底板',
    'monaer-box': '蓝色 Monaer 刹车碟盒子',
    'monaer-care': 'Monaer 刹车零件清洁喷剂、润滑脂管和工作手套',
    'sp-banner': 'S & P Precision Parts 横幅，展示 Monaer 刹车产品系列',
    'sp-name-card': 'S & P Precision Parts 名片，印有士姑来地址',
}

# ---- 22 Nov 2026 rebuild: client's own Facebook media, reels, nationwide state pages ----
FB = {
    'hero_line': '士姑来现货，青绿色盒装 Monaer，直接送到维修厂。',
    'stock_h': '真实的 Monaer 现货，士姑来随时可出',
    'stock_p': '盒子都来自我们自己的货架。每个标签都写明 Monaer 零件编号和适用车款。',
    'strip_label': 'Monaer 现货照片',
    'prev': '上一张', 'next': '下一张',
    'wall_h': '货架上摆满 Honda 和 Hilux 刹车片',
    'wall_p': '热门车款常备现货，所以大多数维修厂订单不用等货就能发出。',
    'deliver_h': '我们送货到柔佛各地的维修厂',
    'deliver_p': '刹车片和刹车碟用 Monaer 纸箱从士姑来发出，为维修厂包装并贴好标签。这一批送到了 Segamat 的 Buloh Kasap。',
    'brand_h': 'Monaer，由 S & P Precision Parts 供应',
    'brand_p': '刹车片、涂层刹车碟、手套和刹车保养套装，全部来自同一个品牌、同一家士姑来代理。',
    'reels_h': '到 Facebook 看我们',
    'reels_p': '来自我们 Facebook 专页的短片。点一下即可有声播放。',
    'reel_caps': ['Monaer 现货和订单，来自我们的 Facebook 专页', 'Monaer 刹车配件，来自我们的 Facebook 专页'],
    'reel_play': '播放视频',
    'reel_open': '在 Facebook 打开',
    'reel_wa': '询问这个零件',
    'ranges_h': '我们备过货的 Monaer 刹车片系列',
    'ranges_p': '根据我们自己的盒子标签整理。把您的车发给我们，购买前我们会先确认准确的零件。',
    'discs_ranges_p': '我们的刹车碟现货会随订单变动。把您的车发给我们，我们帮您核对刹车碟和刹车片的配对。',
    'states_h': '供应 Monaer 给每个州的维修厂',
    'states_p': '我们设在柔佛士姑来，供应 Monaer 刹车片和刹车碟给全马各地的维修厂。',
}

CAP = {
    'sp-monaer-sp-precision-logo': 'Monaer 和 S & P Precision Parts Sdn Bhd',
    'sp-monaer-product-range-graphic': 'Monaer 系列：刹车碟、刹车片、手套和保养套装',
    'sp-branded-carton-johor-delivery': '为柔佛 Segamat 的维修厂包装好',
    'sp-monaer-brake-pads-stock-honda': '货架上的 Honda 和 Toyota Hilux 刹车片',
    'sp-monaer-brake-pads-stock-honda-wide': '货架上的 Honda 和 Toyota Hilux 刹车片',
    'sp-monaer-warehouse-pallet': '一整托盘的 Monaer 纸箱',
    'sp-monaer-brake-system-cartons': 'Monaer 刹车系统运输纸箱',
    'sp-monaer-delivery-boot-boxes': '出发送货',
    'sp-monaer-delivery-boot-parcels': '已装车，准备送到各维修厂',
    'sp-monaer-proton-x50-x70-pads': 'Proton X50 前轮，Proton X70 后轮',
    'sp-monaer-bmw-mini-brake-pads': 'M0518 BMW F40、F48 和 MINI F60',
    'sp-monaer-toyota-estima-lexus-pads': 'M4305 Toyota Estima，M5201 Lexus',
    'sp-monaer-mazda-3-brake-pads': 'M6023 Mazda 3 (BP)，前轮',
    'sp-monaer-ford-ranger-brake-pads': 'M3037 Ford Ranger T6 和 T7，前轮',
    'sp-monaer-perodua-myvi-brake-pads': 'MCK022 Perodua Myvi，前轮',
    'sp-monaer-brembo-gt6-pads': 'M7612 适用于 Brembo GT6 卡钳，前轮',
    'sp-monaer-honda-city-jazz-pads': 'Honda City 和 Jazz (T9A)，前轮一套',
    'sp-monaer-mercedes-bmw-pads': 'M0970 Mercedes W177，M0521 BMW F10',
    'sp-monaer-kia-optima-proton-x70-pads': 'M8103 Kia Optima K5，M6811 Proton X70',
}

STATE = {
    'hub_title': '全马各州维修厂适用的 Monaer 刹车片和刹车碟 | S & P Precision Parts',
    'hub_meta': '柔佛士姑来的 S & P Precision Parts 供应 Monaer 刹车片和刹车碟给全马各州的维修厂。选择您的州，或用 WhatsApp 发来您的车。',
    'hub_h1': '按州查看 Monaer 刹车配件供应',
    'hub_lead': '一家设在柔佛士姑来的代理。全马各地的维修厂都可以通过 WhatsApp 订购 Monaer 刹车片和刹车碟。',
    'hub_nav': '各州供应',
    'title': '{state}维修厂适用的 Monaer 刹车片和刹车碟 | S & P Precision Parts',
    'meta': 'S & P Precision Parts 从柔佛士姑来供应 Monaer 纳米陶瓷刹车片和涂层刹车碟给{state}的维修厂。用 WhatsApp 发来您的车或零件编号。',
    'h1': '{state}维修厂适用的 Monaer 刹车片和刹车碟',
    'lead': '从我们设在柔佛士姑来的据点供应。请用 WhatsApp 发来车型或零件编号。',
    'prefill': '你好，我在{state}经营一间维修厂，想订购 Monaer 刹车配件。车型 / 零件编号：',
    'supply_h': '我们供应给{state}的产品',
    'supply': [
        ('纳米陶瓷刹车片', '适用于日常用车、高端车款和 EV 的 Monaer 刹车片，每套附清洁喷剂、手套和消音润滑脂。'),
        ('涂层刹车碟', '高碳打孔开槽刹车碟，附防锈涂层，左右成对出售。'),
        ('刹车油和保养用品', 'DOT 4 和 DOT 5.1 刹车油，以及同一项工作会用到的刹车保养用品。'),
    ],
    'how_h': '{state}的订购流程',
    'how': [
        ('发送车型或零件编号', '品牌、车型、年份，以及前轮还是后轮。附上旧刹车片或盒子标签的照片最快。'),
        ('我们配对并查库存', '我们把 Monaer 编号和您的车配对，并确认士姑来货架上有没有货。'),
        ('谈好送货方式', '付款前，我们会先确认零件如何送到您在{state}的维修厂。'),
    ],
    'honest': '我们设在柔佛士姑来，在{state}没有分行，也只列出已加入 Monaer 网络的维修厂。',
    'join_h': '您在{state}经营维修厂吗？',
    'join_p': '成为授权 Monaer 维修厂，并列入我们的维修厂查询名单。',
    'faq': [
        ('你们供应 Monaer 刹车配件给{state}的维修厂吗？', '有。S & P Precision Parts 从柔佛士姑来供应 Monaer 刹车片和刹车碟给{state}的维修厂。请用 WhatsApp 发来车型或零件编号即可开始。'),
        ('{state}的车主可以买 Monaer 刹车片吗？', '请用 WhatsApp 告诉我们您的车和所在城镇。我们会配对零件，并告诉您在附近哪里可以安装。'),
    ],
    'others_h': '其他州属',
    'card_go': '查看{state}',
}

# One entry per state on the workshop finder. 'line' = what is specific to that state (towns, roads, distance from Skudai).
STATES = [
    {'slug': 'johor', 'name': '柔佛', 'line': '这是我们的大本营。Johor Bahru、Skudai、Kulai、Batu Pahat、Muar、Kluang 和 Segamat 的维修厂都从士姑来同一个货架订货，我们也送货到柔佛各地的维修厂。'},
    {'slug': 'melaka', 'name': '马六甲', 'line': '沿南北大道从柔佛北上，下一个州就是马六甲。Melaka City、Alor Gajah 和 Jasin 的维修厂可以用 WhatsApp 发来零件编号，发货前我们会先确认零件和库存。'},
    {'slug': 'negeri-sembilan', 'name': '森美兰', 'line': 'Seremban、Nilai 和 Port Dickson 的维修厂，从士姑来沿南北大道一路直上即可到达。请发来您的车，我们确认零件和库存。'},
    {'slug': 'selangor', 'name': '雪兰莪', 'line': '雪兰莪有许多全马的维修厂，从 Shah Alam、Petaling Jaya 到 Klang 和 Subang Jaya 都有。当地维修厂可以直接向士姑来的代理订购 Monaer。'},
    {'slug': 'kuala-lumpur', 'name': '吉隆坡', 'line': '吉隆坡市区车多拥挤，对刹车片和刹车碟的损耗很大。吉隆坡的维修厂可以从我们士姑来的货架订购 Monaer 纳米陶瓷刹车片，刹车安静、粉尘少。'},
    {'slug': 'putrajaya', 'name': '布城', 'line': '服务布城和附近 Cyberjaya 的维修厂，可以通过 WhatsApp 订购 Monaer 刹车片和刹车碟，发货前我们会先配对好零件。'},
    {'slug': 'perak', 'name': '霹雳', 'line': 'Ipoh、Taiping 和 Teluk Intan 的维修厂，我们会先通过 WhatsApp 配对 Monaer 零件，确保正确的盒子从士姑来出发，走这趟北上的长途。'},
    {'slug': 'penang', 'name': '槟城', 'line': '槟岛以及 Butterworth 和 Bukit Mertajam 的维修厂，可以凭零件编号订购 Monaer 刹车片和刹车碟。每个编号在离开柔佛前，我们都会和车款核对。'},
    {'slug': 'kedah', 'name': '吉打', 'line': 'Alor Setar、Sungai Petani 和 Kulim 的维修厂，请用 WhatsApp 发来车型或盒子标签，我们确认 Monaer 零件和士姑来的库存。'},
    {'slug': 'perlis', 'name': '玻璃市', 'line': '玻璃市在半岛最北端，离我们士姑来的据点最远。Kangar 和 Arau 的维修厂依然可以通过 WhatsApp 订购 Monaer，发货前先配对好零件。'},
    {'slug': 'kelantan', 'name': '吉兰丹', 'line': '在东海岸，Kota Bharu 和 Pasir Mas 的维修厂可以通过 WhatsApp 订购 Monaer 刹车片和刹车碟。我们先配对零件，再谈好如何送到吉兰丹。'},
    {'slug': 'terengganu', 'name': '登嘉楼', 'line': 'Kuala Terengganu、Kemaman 和 Dungun 的维修厂，可以用 WhatsApp 发来车型或零件编号。我们确认 Monaer 零件，以及如何送到东海岸。'},
    {'slug': 'pahang', 'name': '彭亨', 'line': '从 Kuantan、Temerloh 到 Bentong，彭亨的维修厂可以向士姑来订购 Monaer 刹车配件。请发来您的车，我们核对零件和库存。'},
    {'slug': 'sabah', 'name': '沙巴', 'line': '沙巴隔着南中国海，位于柔佛对面，所以下单前我们会先谈好运送方式。Kota Kinabalu、Sandakan 和 Tawau 的维修厂可以用 WhatsApp 发来零件编号。'},
    {'slug': 'sarawak', 'name': '砂拉越', 'line': 'Kuching、Sibu、Bintulu 和 Miri 的维修厂，我们先通过 WhatsApp 配对 Monaer 零件，付款前谈好如何运到砂拉越。'},
    {'slug': 'labuan', 'name': '纳闽', 'line': '纳闽的维修厂可以凭零件编号订购 Monaer 刹车片和刹车碟。我们确认士姑来的库存，并谈好零件如何送到岛上。'},
]
