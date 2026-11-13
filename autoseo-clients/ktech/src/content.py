# -*- coding: utf-8 -*-
# All copy for ktec.my, EN / BM / ZH. Facts only (see facts.json sources). No prices, ratings or reviews.
LANGS = ['en', 'ms', 'zh']
LANG_META = {
  'en': {'prefix': '', 'html': 'en-MY', 'label': 'EN', 'og': 'en_MY'},
  'ms': {'prefix': 'ms/', 'html': 'ms-MY', 'label': 'BM', 'og': 'ms_MY'},
  'zh': {'prefix': 'zh/', 'html': 'zh-MY', 'label': '中文', 'og': 'zh_MY'},
}
WA = {
  'en': 'Hi K Tech, I found ktec.my. I would like a quote for an Autel tool: ',
  'ms': 'Hai K Tech, saya jumpa ktec.my. Saya mahu sebut harga alat Autel: ',
  'zh': '你好 K Tech，我在 ktec.my 看到你们。我想询问 Autel 诊断仪报价：',
}
PAGES = ['home', 'tools', 'services', 'about', 'contact']
SLUG = {'home': '', 'tools': 'autel-diagnostic-tools/', 'services': 'services/', 'about': 'about/', 'contact': 'contact/'}

UI = {
 'en': {'ev_h':'Events & on the ground','ev_s':'From our Facebook pages. Drag or let it glide.','ev':['Showroom grand opening','At the service counter','Autel kit and case','Tools packed for delivery','Tablet demo at a booth','Team at a trade show','Display counter with Autel tools','Training audience'],'wa_hooi':'WhatsApp Hooi','recent':'Recent job:','recent_t':'Mercedes-Benz W222 Night View (ADAS) calibration.','new_t':'New: Autel MaxiSys MS909S2','new_p':'Comes with MAX, an AI voice assistant: say “Hey MAX”.','areas':'Johor Bahru · Masai','calln':'Call {n}','call':'Call','email':'Email','map':'Open in Google Maps','addr':'Address','real_h':'On the ground','real_s':'Real K Tech moments from our Facebook.','team':'K Tech team at a workshop, Johor','train':'Technical training session','train_h':'Technical training','train_s':'Sessions for workshop technicians. Drag or let it glide.','nav': {'home':'Home','tools':'Autel tools','services':'Services','about':'About','contact':'Contact'},
        'wa':'WhatsApp us','wa_quote':'WhatsApp for a quote','menu':'Menu','see_range':'See the Autel range',
        'badge':'Authorised Autel dealer · Johor Bahru','tm':'Autel, MaxiSys, MaxiIM, MaxiTPMS, MaxiHVAC and MaxiAlign are trademarks of Autel. Product images: Autel. K Tech Auto Solution Sdn. Bhd. is listed by Autel as a dealer in Malaysia.',
        'autoseo_foot':'SEO websites for automotive workshops:','co':'Company No.','faq':'Questions','updated':'Updated','listed':'See Autel’s Where to Buy','fb':'Facebook','ask_stock':'Ask for stock & model'},
 'ms': {'ev_h':'Acara & di lapangan','ev_s':'Dari halaman Facebook kami. Seret atau biar ia bergerak.','ev':['Pembukaan rasmi bilik pameran','Di kaunter servis','Kit dan beg Autel','Alat sedia untuk dihantar','Demo tablet di gerai','Pasukan di pameran dagangan','Kaunter paparan alat Autel','Peserta latihan'],'wa_hooi':'WhatsApp Hooi','recent':'Kerja terkini:','recent_t':'Kalibrasi Mercedes-Benz W222 Night View (ADAS).','new_t':'Baharu: Autel MaxiSys MS909S2','new_p':'Dilengkapi MAX, pembantu suara AI: sebut “Hey MAX”.','areas':'Johor Bahru · Masai','calln':'Hubungi {n}','call':'Telefon','email':'E-mel','map':'Buka di Google Maps','addr':'Alamat','real_h':'Di lapangan','real_s':'Detik sebenar K Tech dari Facebook kami.','team':'Pasukan K Tech di bengkel, Johor','train':'Sesi latihan teknikal','train_h':'Latihan teknikal','train_s':'Sesi untuk juruteknik bengkel. Seret atau biar ia bergerak.','nav': {'home':'Utama','tools':'Alat Autel','services':'Servis','about':'Tentang','contact':'Hubungi'},
        'wa':'WhatsApp kami','wa_quote':'WhatsApp untuk sebut harga','menu':'Menu','see_range':'Lihat rangkaian Autel',
        'badge':'Pengedar sah Autel · Johor Bahru','tm':'Autel, MaxiSys, MaxiIM, MaxiTPMS, MaxiHVAC dan MaxiAlign ialah tanda dagangan Autel. Gambar produk: Autel. K Tech Auto Solution Sdn. Bhd. disenaraikan oleh Autel sebagai pengedar di Malaysia.',
        'autoseo_foot':'Laman web SEO untuk bengkel kereta:','co':'No. Syarikat','faq':'Soalan','updated':'Dikemas kini','listed':'Lihat Where to Buy Autel','fb':'Facebook','ask_stock':'Tanya stok & model'},
 'zh': {'ev_h':'活动与现场','ev_s':'来自我们的 Facebook 专页。可滑动，也会自动播放。','ev':['展厅开幕','服务柜台','Autel 套件与工具箱','准备送货的工具','展位平板演示','展会团队','Autel 工具展示柜台','培训现场'],'wa_hooi':'WhatsApp Hooi','recent':'近期案例：','recent_t':'Mercedes-Benz W222 Night View（ADAS）校准。','new_t':'新品：Autel MaxiSys MS909S2','new_p':'配备 AI 语音助手 MAX：说 “Hey MAX” 即可。','areas':'新山 · Masai','calln':'致电 {n}','call':'致电','email':'电邮','map':'在 Google 地图打开','addr':'地址','real_h':'现场实况','real_s':'来自我们 Facebook 的真实现场。','team':'K Tech 团队在柔佛车厂','train':'技术培训课程','train_h':'技术培训','train_s':'为车厂技师而设。可滑动，也会自动播放。','nav': {'home':'首页','tools':'Autel 诊断仪','services':'服务','about':'关于我们','contact':'联系'},
        'wa':'WhatsApp 我们','wa_quote':'WhatsApp 询价','menu':'菜单','see_range':'查看 Autel 产品系列',
        'badge':'Autel 授权经销商 · 新山','tm':'Autel、MaxiSys、MaxiIM、MaxiTPMS、MaxiHVAC 与 MaxiAlign 为 Autel 的商标。产品图片来源：Autel。K Tech Auto Solution Sdn. Bhd. 已列于 Autel 官方马来西亚经销商名单。',
        'autoseo_foot':'汽车维修厂 SEO 网站：','co':'公司注册号','faq':'常见问题','updated':'更新','listed':'查看 Autel 官方经销商名单','fb':'Facebook','ask_stock':'询问现货与型号'},
}

# Autel product families (names/taglines from autel.com, 13 Nov 2026)
FAMILIES = [
 {'k':'diag','img':'autel-maxisys-kit-fb.webp','code':'D01','models':'MaxiSys Ultra S2 · MS909S2',
  'en':('Diagnostic tablets','Full-system scans, coding and live data.'),
  'ms':('Tablet diagnostik','Imbasan semua sistem, coding dan data langsung.'),
  'zh':('诊断平板','全车系统扫描、编程设码与实时数据。')},
 {'k':'ev','img':None,'code':'E02','models':'MaxiSys Ultra EV S2 · EV Diagnostics Upgrade Kit2',
  'en':('EV & hybrid diagnostics','Battery-pack and high-voltage system checks.'),
  'ms':('Diagnostik EV & hibrid','Semakan pek bateri dan sistem voltan tinggi.'),
  'zh':('电动车与混动诊断','电池包与高压系统检测。')},
 {'k':'adas','img':'autel-adas.webp','code':'A03','models':'MaxiSys ADAS MA800 · ADAS IA1000',
  'en':('ADAS calibration','Camera and radar calibration after repairs.'),
  'ms':('Kalibrasi ADAS','Kalibrasi kamera dan radar selepas pembaikan.'),
  'zh':('ADAS 校准','维修后的摄像头与雷达校准。')},
 {'k':'tpms','img':'autel-tpms.webp','code':'T04','models':'MaxiTPMS',
  'en':('TPMS service','Sensor programming and relearn.'),
  'ms':('Servis TPMS','Program sensor dan relearn.'),
  'zh':('胎压 TPMS 服务','胎压传感器编程与匹配。')},
 {'k':'key','img':'autel-maxiim-fb.webp','code':'K05','models':'MaxiIM',
  'en':('Key programming','All-in-one key programming plus diagnostics.'),
  'ms':('Program kunci','Program kunci serba lengkap dan diagnostik.'),
  'zh':('钥匙编程','一体化钥匙匹配与诊断。')},
 {'k':'battery','img':'autel-battery.webp','code':'B06','models':'',
  'en':('Battery service','Battery and electrical system testing.'),
  'ms':('Servis bateri','Ujian bateri dan sistem elektrik.'),
  'zh':('电池检测','电池与电气系统测试。')},
 {'k':'ac','img':None,'code':'H07','models':'MaxiHVAC AC909',
  'en':('A/C & thermal','A/C and thermal management diagnostics.'),
  'ms':('A/C & terma','Diagnostik penghawa dingin dan pengurusan terma.'),
  'zh':('空调与热管理','空调与热管理系统诊断。')},
 {'k':'align','img':'autel-align.webp','code':'W08','models':'MaxiAlign IWA500',
  'en':('Wheel alignment','Intelligent wheel alignment system.'),
  'ms':('Penjajaran roda','Sistem penjajaran roda pintar.'),
  'zh':('四轮定位','智能四轮定位系统。')},
 {'k':'special','img':'autel-special.webp','code':'S09','models':'',
  'en':('Specialty tools','Videoscopes and other workshop electronics.'),
  'ms':('Alat khas','Videoskop dan elektronik bengkel lain.'),
  'zh':('专用工具','内窥镜等车间电子工具。')},
 {'k':'radar','img':'autel-radar.webp','code':'R10','models':'77GHz',
  'en':('Radar sensors','77GHz radar sensors.'),
  'ms':('Sensor radar','Sensor radar 77GHz.'),
  'zh':('雷达传感器','77GHz 雷达传感器。')},
]

TITLE = {
 'home': {'en':'Autel Diagnostic Tools Johor Bahru | K Tech','ms':'Alat Diagnostik Autel Johor Bahru | K Tech','zh':'新山 Autel 汽车诊断仪 | K Tech'},
 'tools': {'en':'Autel Diagnostic Tools Malaysia: Full Range | K Tech','ms':'Alat Diagnostik Autel Malaysia | K Tech','zh':'马来西亚 Autel 诊断仪全系列 | K Tech'},
 'services': {'en':'Autel Tool Supply & Workshop Services | K Tech JB','ms':'Bekalan Alat Autel & Servis Bengkel | K Tech JB','zh':'Autel 工具供应与车厂服务 | K Tech 新山'},
 'about': {'en':'About K Tech Auto Solution Sdn. Bhd. | Johor Bahru','ms':'Tentang K Tech Auto Solution Sdn. Bhd. | Johor Bahru','zh':'关于 K Tech Auto Solution Sdn. Bhd. | 新山'},
 'contact': {'en':'Contact K Tech Johor Bahru | WhatsApp +60 18-949 2820','ms':'Hubungi K Tech Johor Bahru | WhatsApp +60 18-949 2820','zh':'联系 K Tech 新山 | WhatsApp +60 18-949 2820'},
}
DESC = {
 'home': {'en':'Authorised Autel dealer in Johor Bahru. Diagnostic tablets, ADAS, TPMS, key programming and EV tools for workshops. WhatsApp K Tech for a quote.',
          'ms':'Pengedar sah Autel di Johor Bahru. Tablet diagnostik, ADAS, TPMS, program kunci dan alat EV untuk bengkel. WhatsApp K Tech untuk sebut harga.',
          'zh':'新山 Autel 授权经销商。为车厂提供诊断平板、ADAS、TPMS、钥匙编程与电动车工具。WhatsApp K Tech 询价。'},
 'tools': {'en':'The Autel range for Malaysian workshops: MaxiSys diagnostics, EV, ADAS calibration, TPMS, MaxiIM key programming, battery, A/C and alignment. WhatsApp for stock.',
           'ms':'Rangkaian Autel untuk bengkel Malaysia: diagnostik MaxiSys, EV, kalibrasi ADAS, TPMS, MaxiIM, bateri, A/C dan penjajaran. WhatsApp untuk stok.',
           'zh':'适合马来西亚车厂的 Autel 全系列：MaxiSys 诊断、电动车、ADAS 校准、TPMS、MaxiIM 钥匙编程、电池、空调与四轮定位。WhatsApp 询问现货。'},
 'services': {'en':'Autel tool supply and model advice in Johor Bahru, technical training sessions, and AutoSEO.my websites for automotive workshops. WhatsApp K Tech.',
              'ms':'Bekalan alat Autel dan nasihat model di Johor Bahru, sesi latihan teknikal, dan laman web AutoSEO.my untuk bengkel. WhatsApp K Tech.',
              'zh':'新山 Autel 工具供应与选型建议、技术培训课程，以及 AutoSEO.my 车厂网站。WhatsApp K Tech。'},
 'about': {'en':'K Tech Auto Solution Sdn. Bhd. (201801038870) is a Johor Bahru Autel dealer and the company behind AutoSEO.my.',
           'ms':'K Tech Auto Solution Sdn. Bhd. (201801038870) ialah pengedar Autel di Johor Bahru dan syarikat di sebalik AutoSEO.my.',
           'zh':'K Tech Auto Solution Sdn. Bhd.（201801038870）是新山的 Autel 经销商，也是 AutoSEO.my 背后的公司。'},
 'contact': {'en':'WhatsApp K Tech Auto Solution in Johor Bahru on +60 18-949 2820 for Autel diagnostic tool quotes and stock.',
             'ms':'WhatsApp K Tech Auto Solution di Johor Bahru, +60 18-949 2820, untuk sebut harga dan stok alat diagnostik Autel.',
             'zh':'WhatsApp +60 18-949 2820 联系新山 K Tech Auto Solution，询问 Autel 诊断仪报价与现货。'},
}

HOME = {
 'en': {'h1':'Autel diagnostic tools in <em>Johor Bahru</em>','line':'Scan, calibrate and code with the tools pro workshops trust.',
        'scan_t':'AUTO SCAN','scan_sys':['Engine','Transmission','ABS','SRS airbag','TPMS','ADAS camera'],'scan_ok':'OK','vin':'VIN scanning…','done':'Scan complete',
        'range_h':'The Autel range','range_s':'Drag or let it glide.','proof_h':'Listed by Autel',
        'proof':['Named on Autel’s official Where to Buy list for Malaysia.','Company No. 201801038870 (1300901-K)','Taman Ekoperniagaan, Johor Bahru'],
        'steps_h':'Get the right tool','steps':[('WhatsApp us','Your car brands and jobs.'),('We match','The Autel model that fits.'),('You fix more','Scan, code, calibrate.')],
        'seo_h':'Need more workshop customers?','seo_p':'Our AutoSEO.my team builds SEO websites for automotive businesses.','seo_b':'Visit AutoSEO.my',
        'cta_h':'Tell us what you repair.','cta_p':'We reply with the right Autel tool.'},
 'ms': {'h1':'Alat diagnostik Autel di <em>Johor Bahru</em>','line':'Imbas, kalibrasi dan coding dengan alat pilihan bengkel pro.',
        'scan_t':'IMBASAN AUTO','scan_sys':['Enjin','Transmisi','ABS','Beg udara SRS','TPMS','Kamera ADAS'],'scan_ok':'OK','vin':'Mengimbas VIN…','done':'Imbasan selesai',
        'range_h':'Rangkaian Autel','range_s':'Seret atau biar ia bergerak.','proof_h':'Disenaraikan oleh Autel',
        'proof':['Tersenarai dalam senarai rasmi Where to Buy Autel untuk Malaysia.','No. Syarikat 201801038870 (1300901-K)','Taman Ekoperniagaan, Johor Bahru'],
        'steps_h':'Dapatkan alat yang betul','steps':[('WhatsApp kami','Jenama kereta dan kerja anda.'),('Kami padankan','Model Autel yang sesuai.'),('Lebih banyak kerja','Imbas, coding, kalibrasi.')],
        'seo_h':'Mahu lebih ramai pelanggan bengkel?','seo_p':'Pasukan AutoSEO.my kami membina laman web SEO untuk perniagaan automotif.','seo_b':'Lawati AutoSEO.my',
        'cta_h':'Beritahu kami apa yang anda baiki.','cta_p':'Kami cadangkan alat Autel yang sesuai.'},
 'zh': {'h1':'<em>新山</em> Autel 汽车诊断仪','line':'专业车厂信赖的扫描、校准与编程工具。',
        'scan_t':'自动扫描','scan_sys':['发动机','变速箱','ABS','SRS 气囊','TPMS 胎压','ADAS 摄像头'],'scan_ok':'正常','vin':'正在读取 VIN…','done':'扫描完成',
        'range_h':'Autel 产品系列','range_s':'可滑动，也会自动播放。','proof_h':'Autel 官方名单',
        'proof':['列于 Autel 官方马来西亚经销商（Where to Buy）名单。','公司注册号 201801038870 (1300901-K)','新山 Taman Ekoperniagaan'],
        'steps_h':'选对工具','steps':[('WhatsApp 我们','告诉我们车型与工作。'),('为你配对','推荐合适的 Autel 型号。'),('修得更多','扫描、编程、校准。')],
        'seo_h':'想要更多车厂客户？','seo_p':'我们的 AutoSEO.my 团队为汽车行业打造 SEO 网站。','seo_b':'访问 AutoSEO.my',
        'cta_h':'告诉我们你修什么车。','cta_p':'我们推荐合适的 Autel 工具。'},
}

FAQ = {
 'en': [('Is K Tech an authorised Autel dealer?','Yes. K Tech Auto Solution Sdn Bhd is listed under Malaysia on Autel’s official Where to Buy page.'),
        ('Which Autel tools can I get?','Diagnostic tablets, EV diagnostics, ADAS calibration, TPMS, key programming, battery, A/C and wheel alignment tools. WhatsApp us for the model and current stock.'),
        ('Where is K Tech?','No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor. WhatsApp us before you visit.'),
        ('How much is an Autel scanner?','It depends on the model and package. WhatsApp us your needs for a quote.'),
        ('Do you build websites for workshops?','Yes, through AutoSEO.my, our SEO website brand for automotive businesses in Malaysia.')],
 'ms': [('Adakah K Tech pengedar sah Autel?','Ya. K Tech Auto Solution Sdn Bhd tersenarai di bawah Malaysia dalam halaman rasmi Where to Buy Autel.'),
        ('Alat Autel apa yang boleh saya dapatkan?','Tablet diagnostik, diagnostik EV, kalibrasi ADAS, TPMS, program kunci, bateri, A/C dan penjajaran roda. WhatsApp kami untuk model dan stok semasa.'),
        ('Di mana K Tech?','No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor. WhatsApp kami sebelum datang.'),
        ('Berapa harga pengimbas Autel?','Bergantung pada model dan pakej. WhatsApp keperluan anda untuk sebut harga.'),
        ('Adakah anda bina laman web untuk bengkel?','Ya, melalui AutoSEO.my, jenama laman web SEO kami untuk perniagaan automotif di Malaysia.')],
 'zh': [('K Tech 是 Autel 授权经销商吗？','是的。K Tech Auto Solution Sdn Bhd 列于 Autel 官方 Where to Buy 页面的马来西亚名单。'),
        ('可以买到哪些 Autel 工具？','诊断平板、电动车诊断、ADAS 校准、TPMS、钥匙编程、电池、空调与四轮定位工具。请 WhatsApp 询问型号与现货。'),
        ('K Tech 在哪里？','No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor。到访前请先 WhatsApp。'),
        ('Autel 诊断仪多少钱？','视型号与配套而定。请 WhatsApp 告诉我们需求，我们会报价。'),
        ('你们也帮车厂做网站吗？','是的，通过我们的汽车行业 SEO 网站品牌 AutoSEO.my。')],
}

TOOLS = {
 'en': {'h1':'Autel diagnostic tools Malaysia','intro':'K Tech supplies the Autel range to workshops from Johor Bahru. Tap a family, then WhatsApp us for the model and stock.','models':'Autel line'},
 'ms': {'h1':'Alat diagnostik Autel Malaysia','intro':'K Tech membekalkan rangkaian Autel kepada bengkel dari Johor Bahru. Pilih kategori, kemudian WhatsApp kami untuk model dan stok.','models':'Siri Autel'},
 'zh': {'h1':'马来西亚 Autel 汽车诊断仪','intro':'K Tech 在新山为车厂供应 Autel 全系列。选择类别，然后 WhatsApp 询问型号与现货。','models':'Autel 系列'},
}

SERVICES = {
 'en': {'h1':'Autel tool supply & workshop services','intro':'Tools, advice and more customers. All in one WhatsApp.',
        'items':[('S1','Autel tool supply','Car diagnostic tools, TPMS, IMMO & key programming and ADAS tools from Autel.',None,None),
                 ('S2','Model advice','Tell us your car brands and jobs. We suggest the Autel tool that fits.',None,None),
                 ('S3','Onsite programming & coding','Module programming and coding at your workshop.',None,None),
                 ('S4','ECU repair','ECU repair for workshops. WhatsApp us the part and fault.',None,None),
                 ('S5','Technical training','Technical training sessions for workshop technicians.',None,None),
                 ('S6','AutoSEO websites for workshops','SEO, AEO and GEO websites that bring workshops more WhatsApp enquiries.','autoseo','autoseo.my')]},
 'ms': {'h1':'Bekalan alat Autel & servis bengkel','intro':'Alat, nasihat dan lebih ramai pelanggan. Semua dalam satu WhatsApp.',
        'items':[('S1','Bekalan alat Autel','Alat diagnostik kereta, TPMS, IMMO & program kunci serta alat ADAS daripada Autel.',None,None),
                 ('S2','Nasihat model','Beritahu jenama kereta dan kerja anda. Kami cadangkan alat Autel yang sesuai.',None,None),
                 ('S3','Program & coding di lokasi','Program dan coding modul di bengkel anda.',None,None),
                 ('S4','Pembaikan ECU','Pembaikan ECU untuk bengkel. WhatsApp kami bahagian dan masalahnya.',None,None),
                 ('S5','Latihan teknikal','Sesi latihan teknikal untuk juruteknik bengkel.',None,None),
                 ('S6','Laman web AutoSEO untuk bengkel','Laman web SEO, AEO dan GEO yang membawa lebih banyak pertanyaan WhatsApp.','autoseo','autoseo.my')]},
 'zh': {'h1':'Autel 工具供应与车厂服务','intro':'工具、建议与更多客户，一个 WhatsApp 搞定。',
        'items':[('S1','Autel 工具供应','Autel 汽车诊断仪、TPMS、IMMO 与钥匙编程及 ADAS 工具。',None,None),
                 ('S2','选型建议','告诉我们你修的车型与项目，我们推荐合适的 Autel 工具。',None,None),
                 ('S3','上门编程与设码','到你的车厂进行模块编程与设码。',None,None),
                 ('S4','ECU 维修','为车厂提供 ECU 维修。请 WhatsApp 告诉我们零件与故障。',None,None),
                 ('S5','技术培训','为车厂技师举办的技术培训课程。',None,None),
                 ('S6','AutoSEO 车厂网站','SEO、AEO 与 GEO 网站，为车厂带来更多 WhatsApp 询问。','autoseo','autoseo.my')]},
}

ABOUT = {
 'en': {'h1':'About K Tech Auto Solution','rows':[('Company','K Tech Auto Solution Sdn. Bhd.'),('Company No.','201801038870 (1300901-K)'),('Base','Johor Bahru, Johor'),('Autel','Listed dealer for Malaysia'),('Our brand','AutoSEO.my'),('Address','No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor')],
        'p':'Your car diagnostic solution partner. We supply Autel tools, run technical training sessions, and help workshops get found online through AutoSEO.my.'},
 'ms': {'h1':'Tentang K Tech Auto Solution','rows':[('Syarikat','K Tech Auto Solution Sdn. Bhd.'),('No. Syarikat','201801038870 (1300901-K)'),('Pangkalan','Johor Bahru, Johor'),('Autel','Pengedar tersenarai untuk Malaysia'),('Jenama kami','AutoSEO.my'),('Alamat','No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor')],
        'p':'Rakan solusi diagnostik kereta anda. Kami membekalkan alat Autel, mengendalikan sesi latihan teknikal, dan membantu bengkel mudah ditemui dalam talian melalui AutoSEO.my.'},
 'zh': {'h1':'关于 K Tech Auto Solution','rows':[('公司','K Tech Auto Solution Sdn. Bhd.'),('注册号','201801038870 (1300901-K)'),('所在地','柔佛新山'),('Autel','马来西亚官方名单经销商'),('旗下品牌','AutoSEO.my'),('地址','No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor')],
        'p':'您的汽车诊断解决方案伙伴。我们供应 Autel 工具、举办技术培训课程，并通过 AutoSEO.my 帮助车厂在网上被找到。'},
}

CONTACT = {
 'en': {'h1':'Contact K Tech Johor Bahru','p':'WhatsApp is fastest.','form_h':'Quick enquiry','f_name':'Your name','f_shop':'Workshop name','f_need':'Tool you need (e.g. ADAS, TPMS, scanner)','f_send':'Send on WhatsApp',
        'lines':['Hi K Tech, I found ktec.my.','Tool needed: ','Name: ','Workshop: ']},
 'ms': {'h1':'Hubungi K Tech Johor Bahru','p':'WhatsApp paling pantas.','form_h':'Pertanyaan pantas','f_name':'Nama anda','f_shop':'Nama bengkel','f_need':'Alat diperlukan (cth. ADAS, TPMS, pengimbas)','f_send':'Hantar di WhatsApp',
        'lines':['Hai K Tech, saya jumpa ktec.my.','Alat diperlukan: ','Nama: ','Bengkel: ']},
 'zh': {'h1':'联系新山 K Tech','p':'WhatsApp 最快。','form_h':'快速询问','f_name':'你的名字','f_shop':'车厂名称','f_need':'需要的工具（如 ADAS、TPMS、诊断仪）','f_send':'通过 WhatsApp 发送',
        'lines':['你好 K Tech，我在 ktec.my 看到你们。','需要的工具：','名字：','车厂：']},
}
