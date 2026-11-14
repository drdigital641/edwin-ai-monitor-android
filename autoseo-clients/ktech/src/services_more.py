# -*- coding: utf-8 -*-
"""K Tech service pages (14 Nov 2026): /services/<slug>/ in EN / BM / 中文.

From K Tech's own notes (Andrew, 14 Nov 2026 via Edwin), photos from K Tech (cleaned, faces/plates/phone blurred).
Template-first: every page reuses build.py's head(), header(), footer(), wabtn(), schema_org(), faq_html() and end_cta().
Look: src/svc.css, loaded on these pages only (k.css unchanged). No prices, times, warranties or brand affiliations invented.
"""
import html
import os
import shutil
from urllib.parse import quote

E_ = html.escape

UIS = {
 'en': {'do_h': 'What we do', 'steps_h': 'How it works', 'notes_h': 'Good to know', 'faq': 'Questions', 'back': 'All services',
        'more_h': 'Other services', 'redraw': 'Redrawn from the scan above so it is easy to read on a phone. Module names left out.',
        'wa': 'Hi K Tech, I found {d}. I would like to ask about: ', 'ask': 'WhatsApp us about this'},
 'ms': {'do_h': 'Apa yang kami buat', 'steps_h': 'Cara ia berjalan', 'notes_h': 'Perlu tahu', 'faq': 'Soalan', 'back': 'Semua servis',
        'more_h': 'Servis lain', 'redraw': 'Dilukis semula daripada imbasan di atas supaya mudah dibaca di telefon. Nama modul tidak ditunjukkan.',
        'wa': 'Hai K Tech, saya jumpa {d}. Saya mahu bertanya tentang: ', 'ask': 'WhatsApp kami tentang ini'},
 'zh': {'do_h': '我们做什么', 'steps_h': '怎么进行', 'notes_h': '须知', 'faq': '常见问题', 'back': '全部服务',
        'more_h': '其他服务', 'redraw': '根据上方扫描画面重新绘制，方便在手机上阅读，未显示模块名称。',
        'wa': '你好 K Tech，我在 {d} 看到你们。我想询问：', 'ask': 'WhatsApp 询问此服务'},
}

TM = {
 'en': 'Mercedes-Benz and BMW are trademarks of their owners. K Tech is an independent company and is not appointed by or affiliated with Mercedes-Benz or BMW.',
 'ms': 'Mercedes-Benz dan BMW ialah tanda dagangan pemilik masing-masing. K Tech ialah syarikat bebas dan tidak dilantik oleh atau bergabung dengan Mercedes-Benz atau BMW.',
 'zh': 'Mercedes-Benz 与 BMW 为其各自所有者的商标。K Tech 为独立公司，并非由 Mercedes-Benz 或 BMW 委任，也与其无关联。',
}

SERVICES_MORE = [
 {'slug': 'local-technical-support', 'code': 'S7', 'img': 'ktec-team-workshop.webp', 'wh': (900, 1125), 'tm': False,
  'stype': 'Automotive technical support',
  'en': {'name': 'Local technical support for workshops', 'card': 'A local Johor company behind your workshop: technical support, plus aftermarket equipment supply.',
         'title': 'Local Technical Support for Workshops, Johor | K Tech', 'desc': 'Workshops that want a local company for technical support: K Tech in Johor Bahru helps with diagnostics, programming and coding, and also supplies aftermarket equipment.',
         'h1': 'Local technical support for workshops', 'line': 'A Johor company you can call when a job gets technical.',
         'fig': 'K Tech team at a workshop, Johor',
         'do': ['Technical support from a local company in Johor Bahru, for workshops that ask for one.',
                'Help with diagnostics on difficult jobs, using Autel tools.',
                'Module programming and coding at your workshop.',
                'Aftermarket (non-original) workshop equipment, as well as Autel tools.',
                'Technical training for your technicians when you want your team to do the job in-house.'],
         'steps': [('WhatsApp us', 'The car, the fault and what you need.'), ('We plan it', 'Support, onsite visit or the right equipment.'), ('Job done', 'Your customer drives away.')],
         'notes': ['We are based in Johor Bahru and work with workshops around Johor Bahru and Masai.',
                   'Aftermarket equipment is not made by the car maker. We tell you plainly what you are buying.',
                   'Tell us the car model and year up front. It helps us give a straight answer on what we can do.'],
         'faq': [('Why use a local company for technical support?', 'When a job needs someone on site, or a follow-up, a company in Johor can reach you and pick up the phone in your time zone.'),
                 ('Do you sell aftermarket equipment?', 'Yes. Besides Autel tools, K Tech supplies aftermarket (non-original) workshop equipment. WhatsApp us what you need and we check what is available.'),
                 ('Which areas do you cover?', 'We are in Taman Ekoperniagaan, Johor Bahru, and work with workshops around Johor Bahru and Masai. WhatsApp us your location.')]},
  'ms': {'name': 'Sokongan teknikal tempatan untuk bengkel', 'card': 'Syarikat tempatan Johor di belakang bengkel anda: sokongan teknikal, serta bekalan peralatan aftermarket.',
         'title': 'Sokongan Teknikal Tempatan untuk Bengkel, Johor | K Tech', 'desc': 'Bengkel yang mahukan syarikat tempatan untuk sokongan teknikal: K Tech di Johor Bahru membantu diagnostik, program dan coding, serta membekalkan peralatan aftermarket.',
         'h1': 'Sokongan teknikal tempatan untuk bengkel', 'line': 'Syarikat Johor yang boleh anda hubungi bila kerja jadi teknikal.',
         'fig': 'Pasukan K Tech di bengkel, Johor',
         'do': ['Sokongan teknikal daripada syarikat tempatan di Johor Bahru, untuk bengkel yang memintanya.',
                'Bantuan diagnostik untuk kerja yang sukar, dengan alat Autel.',
                'Program dan coding modul di bengkel anda.',
                'Peralatan bengkel aftermarket (bukan asli), selain alat Autel.',
                'Latihan teknikal untuk juruteknik anda jika anda mahu pasukan sendiri membuat kerja itu.'],
         'steps': [('WhatsApp kami', 'Kereta, masalah dan apa yang anda perlukan.'), ('Kami rancang', 'Sokongan, lawatan ke lokasi atau peralatan yang betul.'), ('Kerja siap', 'Pelanggan anda boleh memandu pulang.')],
         'notes': ['Kami berpangkalan di Johor Bahru dan bekerja dengan bengkel di sekitar Johor Bahru dan Masai.',
                   'Peralatan aftermarket tidak dibuat oleh pengeluar kereta. Kami beritahu dengan jelas apa yang anda beli.',
                   'Beritahu model dan tahun kereta dari awal. Ia membantu kami memberi jawapan yang tepat.'],
         'faq': [('Kenapa guna syarikat tempatan untuk sokongan teknikal?', 'Bila kerja memerlukan orang di lokasi atau susulan, syarikat di Johor boleh sampai kepada anda dan menjawab telefon pada waktu yang sama.'),
                 ('Adakah anda menjual peralatan aftermarket?', 'Ya. Selain alat Autel, K Tech membekalkan peralatan bengkel aftermarket (bukan asli). WhatsApp kami apa yang anda perlukan dan kami semak apa yang ada.'),
                 ('Kawasan mana yang anda liputi?', 'Kami di Taman Ekoperniagaan, Johor Bahru, dan bekerja dengan bengkel di sekitar Johor Bahru dan Masai. WhatsApp lokasi anda.')]},
  'zh': {'name': '车厂本地技术支持', 'card': '车厂背后的柔佛本地公司：技术支持，以及副厂设备供应。',
         'title': '柔佛车厂本地技术支持 | K Tech 新山', 'desc': '车厂需要本地公司提供技术支持？新山 K Tech 协助诊断、编程与设码，也供应副厂（非原厂）设备。',
         'h1': '车厂本地技术支持', 'line': '遇到技术难题时，一通电话就能找到的柔佛公司。',
         'fig': 'K Tech 团队在柔佛车厂',
         'do': ['为需要本地公司支持的车厂，提供来自新山的技术支持。',
                '用 Autel 工具协助处理疑难诊断。',
                '到你的车厂进行模块编程与设码。',
                '除了 Autel 工具，也供应副厂（非原厂）车厂设备。',
                '如果你想让自己的团队独立完成，也可安排技师技术培训。'],
         'steps': [('WhatsApp 我们', '车型、故障与需求。'), ('我们安排', '技术支持、上门或合适的设备。'), ('完工', '客户把车开走。')],
         'notes': ['我们在新山，服务新山与 Masai 一带的车厂。',
                   '副厂设备并非原车厂出品，我们会清楚说明你买的是什么。',
                   '请先告诉我们车型与年份，方便我们给你明确的答复。'],
         'faq': [('为什么要找本地公司做技术支持？', '需要上门或后续跟进时，柔佛本地公司能更快到场，也在同一时区接电话。'),
                 ('你们卖副厂设备吗？', '是的。除了 Autel 工具，K Tech 也供应副厂（非原厂）车厂设备。请 WhatsApp 告诉我们需求，我们查看现有货品。'),
                 ('服务哪些地区？', '我们位于新山 Taman Ekoperniagaan，服务新山与 Masai 一带的车厂。请 WhatsApp 告诉我们你的位置。')]}},

 {'slug': 'mercedes-benz-engineering-software-training', 'code': 'S8', 'img': 'ktech-mercedes-training-session.webp', 'wh': (918, 1480), 'tm': True,
  'stype': 'Technical training',
  'en': {'name': 'One-to-one Mercedes-Benz engineering software training', 'card': 'One technician, one trainer: Mercedes-Benz engineering software training at your pace.',
         'title': 'Mercedes-Benz Engineering Software Training, 1-to-1 | K Tech JB', 'desc': 'One-to-one Mercedes-Benz engineering software training for workshop technicians in Johor Bahru. Topics agreed with you first. WhatsApp K Tech to arrange.',
         'h1': 'One-to-one Mercedes-Benz engineering software training', 'line': 'One trainer, one technician, your Mercedes-Benz jobs.',
         'fig': 'K Tech session on a Mercedes-Benz in a workshop (faces and plates blurred)',
         'do': ['One-to-one training: just you and the trainer, so the pace and questions are yours.',
                'Mercedes-Benz engineering software, for technicians who already do everyday diagnostics.',
                'Topics agreed with you before the session, based on the Mercedes-Benz jobs you get.',
                'Hands-on work on a real car where the topic needs it.'],
         'steps': [('WhatsApp us', 'Your level and the jobs you want to learn.'), ('We agree topics', 'And a date and place.'), ('Train 1-to-1', 'On a real car, at your pace.')],
         'notes': ['Engineering software goes deeper than a normal scan. A wrong change can disable a module, so it pays to learn it properly.',
                   'Bring the questions from jobs you got stuck on. One-to-one time is best spent on your own cases.',
                   'K Tech also runs group technical training sessions for workshop technicians.'],
         'faq': [('Who is this training for?', 'Technicians and workshop owners who work on Mercedes-Benz and want to use engineering software, beyond everyday diagnostics.'),
                 ('Why one-to-one?', 'You set the pace and every question is about your own jobs. Nothing is skipped because a group has to move on.'),
                 ('Which software and topics are covered?', 'We agree this with you before the session. WhatsApp us the jobs you do and the software you have, and we confirm what the session covers.')]},
  'ms': {'name': 'Latihan perisian kejuruteraan Mercedes-Benz satu-dengan-satu', 'card': 'Seorang juruteknik, seorang jurulatih: latihan perisian kejuruteraan Mercedes-Benz ikut rentak anda.',
         'title': 'Latihan Perisian Kejuruteraan Mercedes-Benz 1-dengan-1 | K Tech', 'desc': 'Latihan perisian kejuruteraan Mercedes-Benz satu-dengan-satu untuk juruteknik bengkel di Johor Bahru. Topik dipersetujui dahulu. WhatsApp K Tech untuk mengatur.',
         'h1': 'Latihan perisian kejuruteraan Mercedes-Benz satu-dengan-satu', 'line': 'Seorang jurulatih, seorang juruteknik, kerja Mercedes-Benz anda.',
         'fig': 'Sesi K Tech pada Mercedes-Benz di bengkel (wajah dan nombor plat dikaburkan)',
         'do': ['Latihan satu-dengan-satu: hanya anda dan jurulatih, jadi rentak dan soalan ikut anda.',
                'Perisian kejuruteraan Mercedes-Benz, untuk juruteknik yang sudah biasa dengan diagnostik harian.',
                'Topik dipersetujui sebelum sesi, berdasarkan kerja Mercedes-Benz yang anda terima.',
                'Kerja hands-on pada kereta sebenar jika topik memerlukannya.'],
         'steps': [('WhatsApp kami', 'Tahap anda dan kerja yang mahu dipelajari.'), ('Setuju topik', 'Serta tarikh dan tempat.'), ('Latihan 1-dengan-1', 'Pada kereta sebenar, ikut rentak anda.')],
         'notes': ['Perisian kejuruteraan pergi lebih dalam daripada imbasan biasa. Perubahan yang salah boleh melumpuhkan modul, jadi berbaloi belajar dengan betul.',
                   'Bawa soalan daripada kerja yang pernah tersekat. Masa satu-dengan-satu paling berguna untuk kes anda sendiri.',
                   'K Tech juga mengendalikan sesi latihan teknikal berkumpulan untuk juruteknik bengkel.'],
         'faq': [('Latihan ini untuk siapa?', 'Juruteknik dan pemilik bengkel yang membaiki Mercedes-Benz dan mahu menggunakan perisian kejuruteraan, melebihi diagnostik harian.'),
                 ('Kenapa satu-dengan-satu?', 'Anda tetapkan rentak dan setiap soalan tentang kerja anda sendiri. Tiada yang dilangkau kerana kumpulan perlu bergerak.'),
                 ('Perisian dan topik apa yang diliputi?', 'Kami persetujui bersama anda sebelum sesi. WhatsApp kerja yang anda buat dan perisian yang anda ada, dan kami sahkan liputan sesi.')]},
  'zh': {'name': '一对一奔驰工程软件培训', 'card': '一位导师，一位技师：按你的节奏学习奔驰工程软件。',
         'title': '一对一奔驰工程软件培训 | K Tech 新山', 'desc': '新山 K Tech 为车厂技师提供一对一奔驰（Mercedes-Benz）工程软件培训，课程内容事先与你商定。WhatsApp 预约。',
         'h1': '一对一奔驰工程软件培训', 'line': '一位导师，一位技师，专讲你的奔驰工作。',
         'fig': 'K Tech 在车厂进行奔驰实车课程（已模糊人脸与车牌）',
         'do': ['一对一培训：只有你和导师，节奏和问题由你决定。',
                '奔驰工程软件，适合已经熟悉日常诊断的技师。',
                '课程内容按你平时接的奔驰工作，事先与你商定。',
                '需要时在实车上动手操作。'],
         'steps': [('WhatsApp 我们', '你的程度与想学的工作。'), ('商定内容', '以及日期与地点。'), ('一对一上课', '实车操作，按你的节奏。')],
         'notes': ['工程软件比一般诊断扫描更深入，改错设置可能令模块无法工作，所以值得好好学。',
                   '把以前卡住的案例带来。一对一的时间最适合解决你自己的问题。',
                   'K Tech 也为车厂技师举办小组技术培训课程。'],
         'faq': [('这个培训适合谁？', '维修奔驰、想在日常诊断之外使用工程软件的技师与车厂老板。'),
                 ('为什么是一对一？', '节奏由你决定，每个问题都围绕你自己的工作，不会因为要跟上小组进度而跳过。'),
                 ('涵盖哪些软件与内容？', '上课前与你商定。请 WhatsApp 告诉我们你做的工作与你现有的软件，我们确认课程内容。')]}},

 {'slug': 'autel-repair-and-parts', 'code': 'S9', 'img': 'ktech-autel-tablet-battery-pack.webp', 'wh': (1380, 640), 'tm': False,
  'stype': 'Diagnostic tool repair and replacement parts',
  'en': {'name': 'Autel replacement parts & repair', 'card': 'Replacement parts for Autel tools, such as tablet battery packs, or a repair plan for a damaged unit.',
         'title': 'Autel Tool Repair & Replacement Parts Malaysia | K Tech JB', 'desc': 'Damaged Autel tablet or tool? K Tech in Johor Bahru supplies Autel replacement parts, such as tablet battery packs, and offers repair options. WhatsApp a photo.',
         'h1': 'Autel replacement parts & repair', 'line': 'Damaged Autel tool? Send us a photo and the fault.',
         'fig': 'Replacement battery pack for an Autel diagnostic tablet (serial labels blurred)',
         'do': ['Replacement parts for Autel tools, for example a battery pack for an Autel tablet that no longer holds a charge.',
                'Repair options for a damaged Autel unit.',
                'A straight answer on whether repair or replacement makes more sense.'],
         'steps': [('WhatsApp a photo', 'The unit, its model and the fault.'), ('We check', 'Part or repair, and what it takes.'), ('Back to work', 'Your tool is on the job again.')],
         'notes': ['Send the model name from the label on the back of the unit. Parts differ between Autel models.',
                   'Common signs: the battery drains fast or swells, the screen is cracked, the tablet will not charge or start.',
                   'A swollen battery should not be charged. Switch the tool off and WhatsApp us a photo.'],
         'faq': [('Can you replace an Autel tablet battery?', 'Yes, K Tech supplies replacement parts such as battery packs for Autel tablets. WhatsApp us the model so we can check the right part.'),
                 ('My Autel tool is damaged. Can it be repaired?', 'Often there is a repair option. WhatsApp us a photo of the unit, the model and what happened, and we tell you the options.'),
                 ('Do I need to bring the tool in?', 'Start with a WhatsApp photo and description. We tell you the next step from there.')]},
  'ms': {'name': 'Alat ganti & pembaikan Autel', 'card': 'Alat ganti untuk alat Autel, seperti pek bateri tablet, atau pelan pembaikan untuk unit yang rosak.',
         'title': 'Pembaikan Alat Autel & Alat Ganti Malaysia | K Tech JB', 'desc': 'Tablet atau alat Autel rosak? K Tech di Johor Bahru membekalkan alat ganti Autel, seperti pek bateri tablet, dan pilihan pembaikan. WhatsApp gambar.',
         'h1': 'Alat ganti & pembaikan Autel', 'line': 'Alat Autel rosak? Hantar gambar dan masalahnya.',
         'fig': 'Pek bateri gantian untuk tablet diagnostik Autel (label siri dikaburkan)',
         'do': ['Alat ganti untuk alat Autel, contohnya pek bateri untuk tablet Autel yang tidak lagi tahan cas.',
                'Pilihan pembaikan untuk unit Autel yang rosak.',
                'Jawapan jelas sama ada membaiki atau menukar lebih berbaloi.'],
         'steps': [('WhatsApp gambar', 'Unit, model dan masalahnya.'), ('Kami semak', 'Alat ganti atau pembaikan, dan apa yang diperlukan.'), ('Kembali bekerja', 'Alat anda boleh digunakan semula.')],
         'notes': ['Hantar nama model daripada label di belakang unit. Alat ganti berbeza mengikut model Autel.',
                   'Tanda biasa: bateri cepat habis atau membengkak, skrin retak, tablet tidak mahu dicas atau hidup.',
                   'Bateri yang membengkak tidak patut dicas. Matikan alat dan WhatsApp gambar kepada kami.'],
         'faq': [('Bolehkah anda tukar bateri tablet Autel?', 'Ya, K Tech membekalkan alat ganti seperti pek bateri untuk tablet Autel. WhatsApp model supaya kami boleh semak alat ganti yang betul.'),
                 ('Alat Autel saya rosak. Boleh dibaiki?', 'Selalunya ada pilihan pembaikan. WhatsApp gambar unit, model dan apa yang berlaku, dan kami beritahu pilihannya.'),
                 ('Perlukah saya bawa alat itu?', 'Mula dengan gambar dan penerangan di WhatsApp. Kami beritahu langkah seterusnya.')]},
  'zh': {'name': 'Autel 零部件更换与维修', 'card': 'Autel 工具零部件更换（如平板电池组），或受损设备的维修方案。',
         'title': 'Autel 诊断仪维修与零部件更换 | K Tech 新山', 'desc': 'Autel 平板或工具受损？新山 K Tech 提供 Autel 零部件更换（如平板电池组）与维修方案。WhatsApp 发照片给我们。',
         'h1': 'Autel 零部件更换与维修', 'line': 'Autel 工具坏了？把照片和故障发给我们。',
         'fig': 'Autel 诊断平板的替换电池组（已模糊序列号标签）',
         'do': ['Autel 工具零部件更换，例如不再蓄电的 Autel 平板电池组。',
                '受损 Autel 设备的维修方案。',
                '清楚告诉你维修还是更换更划算。'],
         'steps': [('WhatsApp 照片', '设备、型号与故障。'), ('我们检查', '换零件还是维修，需要什么。'), ('恢复工作', '工具重新上岗。')],
         'notes': ['请提供机身背面标签上的型号，不同 Autel 型号的零件不同。',
                   '常见情况：电池掉电快或鼓包、屏幕破裂、平板无法充电或开机。',
                   '电池鼓包请勿再充电。请关机并 WhatsApp 照片给我们。'],
         'faq': [('可以更换 Autel 平板电池吗？', '可以，K Tech 提供 Autel 平板电池组等零部件。请 WhatsApp 告诉我们型号，以便确认正确的零件。'),
                 ('我的 Autel 工具坏了，能修吗？', '通常有维修方案。请 WhatsApp 发设备照片、型号与发生的情况，我们告诉你可选方案。'),
                 ('需要把工具带过来吗？', '先用 WhatsApp 发照片与说明，我们再告诉你下一步。')]}},

 {'slug': 'mercedes-engine-starts-test', 'code': 'S10', 'img': 'ktech-engine-starts-scan-photo.webp', 'wh': (1200, 640), 'tm': True,
  'stype': 'Vehicle diagnostics',
  'en': {'name': 'Mercedes-Benz “Number of engine starts” test', 'card': 'Read the starter counters in a Mercedes-Benz engine ECU with an Autel intelligent diagnostic scanner.',
         'title': 'Mercedes “Number of Engine Starts” Test with Autel | K Tech', 'desc': 'How an Autel intelligent diagnostic scanner runs the Mercedes-Benz ECM test “Number of engine starts”: what the screen shows and why it helps with starter jobs.',
         'h1': 'Mercedes-Benz “Number of engine starts” test with an Autel scanner', 'line': 'Read the starter counters before you replace a starter.',
         'fig': 'Autel scanner on a Mercedes-Benz: Perform test “Number of engine starts” (phone photo, straightened)',
         'do': ['The test runs from the engine control unit: Mercedes-Benz › Automatic selection › Auto scan › ECM (Engine Control Unit) › Special function › Perform test “Number of engine starts”.',
                'The screen lists the odometer reading from the CAN bus, the travel distance since the last service due, the number of engine starts, and the travel distance since the last starter replacement.',
                'A note at the top gives the result. On the car in our photo it read “Do not replace starter”.'],
         'steps': [('Connect', 'Autel scanner on the OBD port, auto scan.'), ('Open ECM', 'Special function, engine starts test.'), ('Decide', 'Read the counters before changing parts.')],
         'notes': ['Cars with ECO start/stop crank far more often than older cars, so the starter counter is a useful number before a starter job.',
                   'The counters back up your own checks. Still test the battery and charging first: a weak battery is a common reason for slow cranking.',
                   'Which special functions show depends on the car, its engine ECU and the Autel model and software. WhatsApp us the model and year to check.'],
         'faq': [('What is the “Number of engine starts” test?', 'A special function in the engine control unit of many Mercedes-Benz cars. It shows counters linked to the starter, such as the number of engine starts and the distance since the starter was last replaced.'),
                 ('Can an Autel scanner run it?', 'Yes. The photo on this page shows an Autel intelligent diagnostic scanner running the test on a Mercedes-Benz, from the ECM special functions.'),
                 ('Does it tell me to replace the starter?', 'The screen gives a status note, for example “Do not replace starter”. Use it together with your battery, charging and cranking checks.')]},
  'ms': {'name': 'Ujian “Number of engine starts” Mercedes-Benz', 'card': 'Baca kaunter starter dalam ECU enjin Mercedes-Benz dengan pengimbas diagnostik pintar Autel.',
         'title': 'Ujian “Number of Engine Starts” Mercedes dengan Autel | K Tech', 'desc': 'Cara pengimbas diagnostik pintar Autel menjalankan ujian ECM Mercedes-Benz “Number of engine starts”: apa yang dipaparkan dan kenapa ia membantu kerja starter.',
         'h1': 'Ujian “Number of engine starts” Mercedes-Benz dengan pengimbas Autel', 'line': 'Baca kaunter starter sebelum menukar starter.',
         'fig': 'Pengimbas Autel pada Mercedes-Benz: Perform test “Number of engine starts” (gambar telefon, diluruskan)',
         'do': ['Ujian dijalankan dari unit kawalan enjin: Mercedes-Benz › Automatic selection › Auto scan › ECM (Engine Control Unit) › Special function › Perform test “Number of engine starts”.',
                'Skrin menyenaraikan bacaan odometer daripada CAN bus, jarak perjalanan sejak servis terakhir, bilangan hidupkan enjin, dan jarak perjalanan sejak starter terakhir ditukar.',
                'Nota di bahagian atas memberi keputusan. Pada kereta dalam gambar kami, ia berbunyi “Do not replace starter”.'],
         'steps': [('Sambung', 'Pengimbas Autel pada port OBD, auto scan.'), ('Buka ECM', 'Special function, ujian engine starts.'), ('Putuskan', 'Baca kaunter sebelum menukar alat ganti.')],
         'notes': ['Kereta dengan ECO start/stop menghidupkan enjin jauh lebih kerap, jadi kaunter starter berguna sebelum kerja starter.',
                   'Kaunter ini menyokong semakan anda sendiri. Uji bateri dan sistem pengecasan dahulu: bateri lemah ialah sebab biasa enjin lambat hidup.',
                   'Fungsi khas yang dipaparkan bergantung pada kereta, ECU enjin dan model serta perisian Autel. WhatsApp model dan tahun untuk semakan.'],
         'faq': [('Apakah ujian “Number of engine starts”?', 'Fungsi khas dalam unit kawalan enjin banyak kereta Mercedes-Benz. Ia menunjukkan kaunter berkaitan starter, seperti bilangan hidupkan enjin dan jarak sejak starter terakhir ditukar.'),
                 ('Bolehkah pengimbas Autel menjalankannya?', 'Ya. Gambar di halaman ini menunjukkan pengimbas diagnostik pintar Autel menjalankan ujian pada Mercedes-Benz, daripada fungsi khas ECM.'),
                 ('Adakah ia memberitahu saya untuk menukar starter?', 'Skrin memberi nota status, contohnya “Do not replace starter”. Gunakannya bersama semakan bateri, pengecasan dan cranking anda.')]},
  'zh': {'name': '奔驰“发动机启动次数”测试', 'card': '用 Autel 智能诊断仪读取奔驰发动机电脑里的起动机计数。',
         'title': '用 Autel 做奔驰“发动机启动次数”测试 | K Tech', 'desc': 'Autel 智能诊断仪如何执行奔驰 ECM 的“Number of engine starts”（发动机启动次数）测试：画面显示什么，为什么对起动机维修有帮助。',
         'h1': '用 Autel 诊断仪做奔驰“发动机启动次数”测试', 'line': '换起动机之前，先读起动机计数。',
         'fig': 'Autel 诊断仪在奔驰上执行“Number of engine starts”测试（手机照片，已校正）',
         'do': ['测试在发动机控制单元中执行：Mercedes-Benz › Automatic selection › Auto scan › ECM (Engine Control Unit) › Special function › Perform test “Number of engine starts”。',
                '画面列出 CAN 总线里程读数、上次保养以来的行驶距离、发动机启动次数，以及上次更换起动机以来的行驶距离。',
                '顶部的提示给出结果。我们照片中的这辆车显示 “Do not replace starter”（无需更换起动机）。'],
         'steps': [('连接', 'Autel 诊断仪接 OBD，自动扫描。'), ('进入 ECM', '特殊功能，启动次数测试。'), ('判断', '换件前先看计数。')],
         'notes': ['有 ECO 自动启停的车起动次数多得多，所以在做起动机工作前，这个计数很有参考价值。',
                   '计数只是辅助判断。请先检测电瓶与充电系统：电瓶弱是起动慢的常见原因。',
                   '能显示哪些特殊功能，取决于车型、发动机电脑以及 Autel 型号与软件。请 WhatsApp 告诉我们车型与年份。'],
         'faq': [('什么是“Number of engine starts”测试？', '许多奔驰车型发动机控制单元里的特殊功能，显示与起动机相关的计数，例如发动机启动次数，以及上次更换起动机以来的距离。'),
                 ('Autel 诊断仪能做吗？', '可以。本页照片就是 Autel 智能诊断仪在奔驰上，通过 ECM 特殊功能执行此测试。'),
                 ('它会告诉我要不要换起动机吗？', '画面会给出状态提示，例如 “Do not replace starter”。请结合电瓶、充电与起动检测一起判断。')]}},

 {'slug': 'autel-topology-mapping', 'code': 'S11', 'img': 'ktech-topology-scan-photo.webp', 'wh': (1200, 860), 'tm': True, 'svg': True,
  'stype': 'Vehicle diagnostics',
  'en': {'name': 'Autel topology mapping (version 2)', 'card': 'See every module on the car network in one map, with faults marked in colour. Shown here on a BMW.',
         'title': 'Autel Topology Mapping Version 2 on a BMW | K Tech JB', 'desc': 'How Autel intelligent diagnostic scanners show topology mapping version 2: every control module on one network map, faults in colour. Real BMW scan from K Tech, Johor Bahru.',
         'h1': 'Autel topology mapping version 2 on a BMW', 'line': 'The whole car network on one screen, faults in colour.',
         'fig': 'Autel scanner topology view after an auto scan on a BMW (phone photo, straightened)',
         'do': ['After an auto scan, the Topology tab draws every control module the scanner found, connected to the OBD port through the gateway, bus by bus.',
                'Modules are colour-coded. Green modules answered with no fault. On this BMW, two modules were flagged in orange for faults.',
                'You can switch between the Topology map and the List view, then go straight to Fault Scan, Quick Erase or a Report from the same screen.'],
         'steps': [('Auto scan', 'Autel scanner on the OBD port.'), ('Read the map', 'Find the modules in colour.'), ('Fix and clear', 'Repair, clear codes, rescan.')],
         'notes': ['A map helps when several modules show faults: modules on the same bus with faults often point to one wiring or network problem, not many broken parts.',
                   'K Tech’s note calls this topology mapping version 2. Newer Autel tablets such as the MaxiSys Ultra S2 list Topology 3.0 in their brochure.',
                   'Coverage depends on the car and on the Autel model and software. WhatsApp us the make, model and year.'],
         'faq': [('What is topology mapping on an Autel scanner?', 'A picture of the car’s network: every control module the scanner found, linked to the gateway and bus it sits on, with its status shown in colour.'),
                 ('What do the colours mean?', 'Green means the module answered with no fault. Orange marks a module with fault codes. The legend at the top of the screen explains each colour.'),
                 ('Which Autel tools have topology mapping?', 'Many MaxiSys tablets do. WhatsApp us the jobs you do and we suggest the model that fits.')]},
  'ms': {'name': 'Pemetaan topologi Autel (versi 2)', 'card': 'Lihat setiap modul dalam rangkaian kereta pada satu peta, dengan ralat ditanda berwarna. Ditunjukkan pada BMW.',
         'title': 'Pemetaan Topologi Autel Versi 2 pada BMW | K Tech JB', 'desc': 'Cara pengimbas diagnostik pintar Autel memaparkan pemetaan topologi versi 2: setiap modul kawalan pada satu peta rangkaian, ralat berwarna. Imbasan BMW sebenar oleh K Tech, Johor Bahru.',
         'h1': 'Pemetaan topologi Autel versi 2 pada BMW', 'line': 'Seluruh rangkaian kereta pada satu skrin, ralat berwarna.',
         'fig': 'Paparan topologi pengimbas Autel selepas auto scan pada BMW (gambar telefon, diluruskan)',
         'do': ['Selepas auto scan, tab Topology melukis setiap modul kawalan yang ditemui, disambung ke port OBD melalui gateway, mengikut bus.',
                'Modul berkod warna. Modul hijau menjawab tanpa ralat. Pada BMW ini, dua modul ditanda oren kerana ralat.',
                'Anda boleh tukar antara peta Topology dan paparan List, kemudian terus ke Fault Scan, Quick Erase atau Report dari skrin yang sama.'],
         'steps': [('Auto scan', 'Pengimbas Autel pada port OBD.'), ('Baca peta', 'Cari modul yang berwarna.'), ('Baiki dan padam', 'Baiki, padam kod, imbas semula.')],
         'notes': ['Peta membantu bila beberapa modul ada ralat: modul pada bus yang sama yang beralat selalunya menunjuk kepada satu masalah pendawaian atau rangkaian, bukan banyak alat rosak.',
                   'Nota K Tech menyebutnya pemetaan topologi versi 2. Tablet Autel yang lebih baharu seperti MaxiSys Ultra S2 menyenaraikan Topology 3.0 dalam brosurnya.',
                   'Liputan bergantung pada kereta serta model dan perisian Autel. WhatsApp jenama, model dan tahun.'],
         'faq': [('Apakah pemetaan topologi pada pengimbas Autel?', 'Gambaran rangkaian kereta: setiap modul kawalan yang ditemui, dipautkan kepada gateway dan bus masing-masing, dengan status ditunjukkan dalam warna.'),
                 ('Apa maksud warnanya?', 'Hijau bermaksud modul menjawab tanpa ralat. Oren menanda modul yang ada kod ralat. Petunjuk di bahagian atas skrin menerangkan setiap warna.'),
                 ('Alat Autel mana yang ada pemetaan topologi?', 'Banyak tablet MaxiSys ada. WhatsApp kerja yang anda buat dan kami cadangkan model yang sesuai.')]},
  'zh': {'name': 'Autel 拓扑图第二版', 'card': '一张图看清整车网络里的每个模块，故障用颜色标出。本页以 BMW 为例。',
         'title': 'Autel 拓扑图第二版（BMW 实车）| K Tech 新山', 'desc': 'Autel 智能诊断仪的拓扑图第二版：整车控制模块一张网络图看清，故障以颜色标示。K Tech 新山 BMW 实车扫描。',
         'h1': 'Autel 拓扑图第二版：BMW 实车扫描', 'line': '整车网络一屏看清，故障用颜色标出。',
         'fig': 'Autel 诊断仪在 BMW 上自动扫描后的拓扑画面（手机照片，已校正）',
         'do': ['自动扫描后，Topology（拓扑）页会画出扫描到的每个控制模块，经网关连到 OBD 接口，按总线分布。',
                '模块以颜色区分。绿色表示模块有回应且无故障。这辆 BMW 有两个模块以橙色标出故障。',
                '可在拓扑图与 List（列表）之间切换，并直接在同一画面进入 Fault Scan、Quick Erase 或 Report。'],
         'steps': [('自动扫描', 'Autel 诊断仪接 OBD。'), ('看拓扑图', '找出有颜色标记的模块。'), ('维修并清码', '维修、清除故障码、再扫描。')],
         'notes': ['多个模块报故障时，拓扑图特别有用：同一总线上的多个故障，往往指向一处线路或网络问题，而不是很多零件坏了。',
                   'K Tech 的说明称此为拓扑图第二版。较新的 Autel 平板如 MaxiSys Ultra S2，手册上列明 Topology 3.0。',
                   '覆盖范围取决于车型以及 Autel 型号与软件。请 WhatsApp 告诉我们品牌、车型与年份。'],
         'faq': [('Autel 诊断仪的拓扑图是什么？', '整车网络的示意图：扫描到的每个控制模块，连到所在的网关与总线，并用颜色显示状态。'),
                 ('颜色代表什么？', '绿色表示模块有回应且无故障，橙色表示模块有故障码。画面顶部的图例说明每种颜色。'),
                 ('哪些 Autel 工具有拓扑图？', '许多 MaxiSys 平板都有。请 WhatsApp 告诉我们你做的工作，我们推荐合适的型号。')]}},
]
BY = {s['slug']: s for s in SERVICES_MORE}


def topo_svg(l):
    """Clean redraw of the BMW topology screen: layout and colours only, no module names (unreadable in the photo)."""
    G, O, L, B = '#2f9e44', '#e8590c', '#8a8f98', '#5b4bb7'
    leg = {'en': ['OK', 'Fault'], 'ms': ['OK', 'Ralat'], 'zh': ['正常', '故障']}[l]
    box = lambda x, y, c: f'<rect x="{x}" y="{y}" width="46" height="18" rx="2" fill="{c}"/>'
    s = [f'<rect x="276" y="14" width="48" height="20" fill="#fff" stroke="{L}"/><text x="300" y="28" text-anchor="middle" font-size="11" font-family="monospace" fill="#15171a">OBD</text>',
         f'<path d="M300 34v22" stroke="#15171a" stroke-width="2"/>', box(277, 56, G), box(277, 80, G),
         f'<path d="M60 64H500M60 64v62M500 64v156M450 64v70" stroke="{B}" stroke-width="2" fill="none"/>',
         f'<path d="M323 66h40v62M363 128v80M335 66h55v86" stroke="{O}" stroke-width="1.6" fill="none" opacity=".8"/>',
         f'<path d="M110 64v60M160 64v60M220 64v60" stroke="#f2a516" stroke-width="1.4" fill="none" opacity=".7"/>',
         f'<rect x="210" y="104" width="100" height="48" fill="none" stroke="#0f9fb3" stroke-width="1.4"/>']
    s += [box(40, 126, G)] + [box(98, 126 + 24 * i, G) for i in range(5)] + [box(148, 126 + 24 * i, G) for i in range(4)]
    s += [box(204, 126, G), box(262, 126, G), box(204, 178, G), box(320, 126, G), box(320, 150, O), box(380, 150, O),
          box(380, 196, G), box(380, 220, G), box(436, 126, G), box(436, 150, G), box(436, 252, G)]
    s += [f'<circle cx="366" cy="150" r="5" fill="{O}" stroke="#fff"/><circle cx="426" cy="150" r="5" fill="{O}" stroke="#fff"/>']
    lg = ''.join(f'<rect x="{30 + i * 150}" y="284" width="22" height="16" fill="{c}"/><text x="{60 + i * 150}" y="299" font-size="19" font-weight="600" fill="#3b4047">{E_(t)}</text>'
                 for i, (c, t) in enumerate(zip([G, O], leg)))
    return ('<svg class="sv-topo" viewBox="0 0 560 312" role="img" aria-label="Topology map redraw: OBD port, gateway, buses and modules; '
            'green = OK, orange = fault">' + ''.join(s) + lg + '</svg>')


def register(g):
    for s in SERVICES_MORE:
        k = 'svc:' + s['slug']
        g['SLUG'][k] = 'services/' + s['slug'] + '/'
        g['TITLE'][k] = {l: s[l]['title'] for l in g['LANGS']}
        g['DESC'][k] = {l: s[l]['desc'] for l in g['LANGS']}
        for l in g['LANGS']:
            g['UI'][l]['nav'][k] = s[l]['name']
    return ['svc:' + s['slug'] for s in SERVICES_MORE]


def list_items(l):
    """Extra rows for the /services/ list: (code, name, text, page key)."""
    return [(s['code'], s[l]['name'], s[l]['card'], 'svc:' + s['slug']) for s in SERVICES_MORE]


def _wa(g, l, s):
    dom = g['BASE_URL'].split('//')[-1].strip('/').split('/')[0] if g['LIVE'] else 'ktec.my'
    return 'https://wa.me/' + g['F']['whatsapp'] + '?text=' + quote(UIS[l]['wa'].format(d=dom) + s[l]['name'])


def _btn(g, l, s, ref):
    return f'<a class="btn btn-wa" href="{_wa(g, l, s)}" target="_blank" rel="noopener" data-ref="{ref}">{g["WA_SVG"]}<span>{E_(UIS[l]["ask"])}</span></a>'


def page(g, l, s):
    t, u, nav, A = s[l], UIS[l], g['UI'][l]['nav'], g['A']
    k = 'svc:' + s['slug']
    w, h = s['wh']
    crumb = (f'<div class="crumb"><a href="{g["url"]("home", l)}">{E_(nav["home"])}</a> / '
             f'<a href="{g["url"]("services", l)}">{E_(nav["services"])}</a> / {E_(t["name"])}</div>')
    hero = (f'<section class="ph sv-ph"><div class="wrap">{crumb}<span class="sv-code mono">{s["code"]}</span>'
            f'<h1>{E_(t["h1"])}</h1><p>{E_(t["line"])}</p>{_btn(g, l, s, "top")}</div></section>')
    fig = (f'<figure class="sv-fig{" tall" if h > w else ""}"><img src="{A}{s["img"]}{g["V"]}" alt="{E_(t["fig"])}" width="{w}" height="{h}" decoding="async" fetchpriority="high">'
           f'<figcaption>{E_(t["fig"])}</figcaption></figure>')
    if s.get('svg'):
        fig += f'<figure class="sv-fig sv-draw">{topo_svg(l)}<figcaption>{E_(u["redraw"])}</figcaption></figure>'
    do = '<ol class="sv-do">' + ''.join(f'<li><span class="mono">{s["code"]}.{i}</span><p>{E_(x)}</p></li>' for i, x in enumerate(t['do'], 1)) + '</ol>'
    steps = ''.join(f'<li><span class="n">0{i}</span><div><h3>{E_(a)}</h3><p>{E_(b)}</p></div></li>' for i, (a, b) in enumerate(t['steps'], 1))
    notes = ''.join(f'<li>{E_(x)}</li>' for x in t['notes'])
    tm = f'<p class="sv-tm">{E_(TM[l])}</p>' if s['tm'] else ''
    others = ''.join(f'<a href="{g["url"]("svc:" + o["slug"], l)}"><span class="mono">{o["code"]}</span>{E_(o[l]["name"])}</a>' for o in SERVICES_MORE if o is not s)
    body = (hero
            + f'<section class="sec"><div class="wrap sv-grid"><div>{fig}</div><div><h2 class="sv-h">{E_(u["do_h"])}</h2>{do}</div></div></section>'
            + f'<section class="sec alt"><div class="wrap"><div class="sh"><div><h2>{E_(u["steps_h"])}</h2></div></div><ol class="steps">{steps}</ol></div></section>'
            + f'<section class="sec"><div class="wrap"><div class="sv-notes"><h2 class="sv-h">{E_(u["notes_h"])}</h2><ul>{notes}</ul>{tm}</div>'
            + f'<div class="sh" style="margin-top:34px"><div><h2>{E_(u["faq"])}</h2></div></div>{g["faq_html"](l, t["faq"])}'
            + f'<h2 class="sv-h" style="margin-top:34px">{E_(u["more_h"])}</h2><nav class="sv-more" aria-label="{E_(u["more_h"])}">{others}'
            + f'<a href="{g["url"]("services", l)}"><span class="mono">S1-S6</span>{E_(u["back"])} →</a></nav></div></section>'
            + f'<section class="sec dark end"><div class="wrap"><h2>{E_(t["name"])}</h2><p>{E_(t["line"])}</p>{_btn(g, l, s, "end")}</div></section>')
    svc = {'@context': 'https://schema.org', '@type': 'Service', 'name': t['name'], 'description': t['desc'], 'serviceType': s['stype'],
           'url': g['curl_'](k, l), 'image': g['CANON'] + 'assets/' + s['img'], 'provider': {'@id': g['CANON'] + '#org'},
           'areaServed': [{'@type': 'City', 'name': 'Johor Bahru'}, {'@type': 'City', 'name': 'Masai'}, {'@type': 'Country', 'name': 'Malaysia'}],
           'inLanguage': g['LANG_META'][l]['html']}
    crumbs = {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': nav['home'], 'item': g['curl_']('home', l)},
        {'@type': 'ListItem', 'position': 2, 'name': nav['services'], 'item': g['curl_']('services', l)},
        {'@type': 'ListItem', 'position': 3, 'name': t['name'], 'item': g['curl_'](k, l)}]}
    css = f'<link rel="stylesheet" href="{A}svc.css{g["V"]}"></head>'
    return (g['head'](k, l, [g['schema_org'](l), svc, g['faq_schema'](l, t['faq']), crumbs], og_image=g['CANON'] + 'assets/' + s['img']).replace('</head>', css, 1)
            + g['header']('services', l, lang_href=lambda x, kk=k: g['url'](kk, x)) + body + g['footer'](l))


def build(g):
    shutil.copy(os.path.join(g['B'], 'src', 'svc.css'), os.path.join(g['OUT'], 'assets'))
    for l in g['LANGS']:
        for s in SERVICES_MORE:
            d = os.path.join(g['OUT'], g['LANG_META'][l]['prefix'] + 'services', s['slug'])
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(page(g, l, s))
