# -*- coding: utf-8 -*-
"""SEO/AEO additions (2 Nov 2026): hub intros, extra paragraphs and FAQs for hub/thin pages.
Facts only from this site's build.py / README / memory (hours, address, WhatsApp lines, specs, warranty, service interval). No prices."""


def T(en, ms, zh):
    return {'en': en, 'ms': ms, 'zh': zh}


EXTRA = {
    'models/': {
        'intro': [
            T("Dongfeng Johor Bahru is the first Dongfeng 3S centre in Johor Bahru, and two passenger EVs are on show in the showroom at Taman Ekoperniagaan: the Dongfeng Vigo electric SUV and the Dongfeng 007 electric sedan. The Voyah Dream luxury MPV is listed as coming soon, and Malaysian specifications, price and launch date have not been announced.",
              "Dongfeng Johor Bahru ialah pusat 3S Dongfeng pertama di Johor Bahru, dan dua kereta penumpang elektrik dipamerkan di bilik pameran di Taman Ekoperniagaan: Dongfeng Vigo SUV elektrik dan Dongfeng 007 sedan elektrik. Voyah Dream MPV mewah disenaraikan sebagai akan datang, dan spesifikasi, harga serta tarikh pelancaran Malaysia belum diumumkan.",
              "新山东风是新山首家东风 3S 中心，位于 Taman Ekoperniagaan 的展厅展出两款纯电乘用车：东风 Vigo 纯电 SUV 和东风 007 纯电轿跑。Voyah Dream 豪华 MPV 目前标示为即将登场，马来西亚的规格、价格和上市日期尚未公布。"),
            T("Pick a model to see its Malaysian specifications, colours and photos, then WhatsApp us to book a test drive. This website does not publish prices; ask us for current offers.",
              "Pilih model untuk melihat spesifikasi Malaysia, warna dan foto, kemudian WhatsApp kami untuk menempah pandu uji. Laman web ini tidak menyiarkan harga; tanya kami untuk tawaran terkini.",
              "选择车型即可查看马来西亚规格、颜色和照片，然后 WhatsApp 我们预约试驾。本网站不公布价格，请向我们询问最新优惠。"),
        ],
        'faqs': [
            (T("Which Dongfeng models can I see in Johor Bahru?", "Model Dongfeng yang manakah boleh dilihat di Johor Bahru?", "在新山可以看到哪些东风车型？"),
             T("The Dongfeng Vigo electric SUV and the Dongfeng 007 electric sedan are in our showroom. The Voyah Dream is coming soon, with no Malaysian specifications, price or date announced yet.",
               "Dongfeng Vigo SUV elektrik dan Dongfeng 007 sedan elektrik berada di bilik pameran kami. Voyah Dream akan datang, tanpa spesifikasi, harga atau tarikh Malaysia yang diumumkan lagi.",
               "展厅有东风 Vigo 纯电 SUV 和东风 007 纯电轿跑。Voyah Dream 即将登场，马来西亚的规格、价格和日期尚未公布。")),
            (T("Does this website show prices?", "Adakah laman web ini menunjukkan harga?", "网站上有列出价格吗？"),
             T("No. We do not publish prices online. WhatsApp +60 18-762 0828 and we will tell you the current offer for the model you want.",
               "Tidak. Kami tidak menyiarkan harga dalam talian. WhatsApp +60 18-762 0828 dan kami akan beritahu tawaran semasa untuk model yang anda mahu.",
               "没有。我们不在网上公布价格。请 WhatsApp +60 18-762 0828，我们会告知您所选车型的最新优惠。")),
            (T("How do I book a test drive?", "Bagaimana saya menempah pandu uji?", "如何预约试驾？"),
             T("Test drives are by WhatsApp appointment. Send the model and a time to +60 18-762 0828. The showroom is open Monday to Saturday 9am to 6pm and Sunday 10am to 4pm.",
               "Pandu uji adalah melalui temujanji WhatsApp. Hantar model dan masa ke +60 18-762 0828. Bilik pameran dibuka Isnin hingga Sabtu 9 pagi hingga 6 petang dan Ahad 10 pagi hingga 4 petang.",
               "试驾需通过 WhatsApp 预约。请将车型和时间发送至 +60 18-762 0828。展厅营业时间：周一至周六上午 9 点至下午 6 点，周日上午 10 点至下午 4 点。")),
        ],
    },
    'articles/': {
        'intro': [
            T("These guides answer the questions Johor drivers ask before and after buying an electric car: what a 3S centre is, how the Dongfeng Vigo compares with the 007, what to check on a test drive, how home charging works in Johor, EV maintenance, battery care in hot weather, charging tax relief and driving an EV from Johor Bahru to Singapore.",
              "Panduan ini menjawab soalan yang ditanya pemandu Johor sebelum dan selepas membeli kereta elektrik: apa itu pusat 3S, bagaimana Dongfeng Vigo dibandingkan dengan 007, apa yang perlu disemak semasa pandu uji, bagaimana pengecasan di rumah di Johor, penyelenggaraan EV, penjagaan bateri dalam cuaca panas, pelepasan cukai pengecasan dan memandu EV dari Johor Bahru ke Singapura.",
              "这些指南解答柔佛车主在买电动车前后最常问的问题：3S 中心是什么、东风 Vigo 与 007 如何比较、试驾要检查什么、在柔佛如何家用充电、电动车保养、炎热天气下的电池养护、充电税务减免，以及从新山驾驶电动车前往新加坡。"),
            T("They are written from Dongfeng Johor Bahru's own published specifications and official Malaysian sources, and each guide shows its date. They give general information, not tax or legal advice.",
              "Panduan ini ditulis berdasarkan spesifikasi yang diterbitkan Dongfeng Johor Bahru dan sumber rasmi Malaysia, dan setiap panduan menunjukkan tarikhnya. Ia memberi maklumat umum, bukan nasihat cukai atau undang-undang.",
              "指南依据东风新山公布的规格和马来西亚官方来源撰写，每篇都标明日期。内容属一般资讯，并非税务或法律意见。"),
        ],
        'faqs': [
            (T("Who writes these guides?", "Siapa yang menulis panduan ini?", "这些指南由谁撰写？"),
             T("Dongfeng Johor Bahru (MyKar World Sdn. Bhd.), the first Dongfeng 3S centre in Johor Bahru. Each guide is dated.",
               "Dongfeng Johor Bahru (MyKar World Sdn. Bhd.), pusat 3S Dongfeng pertama di Johor Bahru. Setiap panduan bertarikh.",
               "由东风新山（MyKar World Sdn. Bhd.，新山首家东风 3S 中心）撰写，每篇都标明日期。")),
            (T("Are the guides available in other languages?", "Adakah panduan tersedia dalam bahasa lain?", "指南有其他语言版本吗？"),
             T("Yes. Every guide is available in English, Bahasa Melayu and Simplified Chinese.",
               "Ya. Setiap panduan tersedia dalam Bahasa Inggeris, Bahasa Melayu dan Cina Ringkas.",
               "有。每篇指南都提供英文、马来文和简体中文版本。")),
            (T("Can I ask a question that is not covered?", "Bolehkah saya bertanya soalan yang tidak dibincangkan?", "没有涵盖的问题可以询问吗？"),
             T("Yes. WhatsApp +60 18-762 0828 for sales questions or +60 18-224 0828 for service and parts.",
               "Boleh. WhatsApp +60 18-762 0828 untuk soalan jualan atau +60 18-224 0828 untuk servis dan alat ganti.",
               "可以。销售问题请 WhatsApp +60 18-762 0828，服务与配件请 WhatsApp +60 18-224 0828。")),
        ],
    },
    'about/': {
        'faqs': [
            (T("Who runs Dongfeng Johor Bahru?", "Siapa yang mengendalikan Dongfeng Johor Bahru?", "东风新山由谁经营？"),
             T("MyKar World Sdn. Bhd. (company no. 202501050786, 1652194-X). The 3S centre at No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru handles sales, service and spare parts for Dongfeng passenger EVs.",
               "MyKar World Sdn. Bhd. (no. syarikat 202501050786, 1652194-X). Pusat 3S di No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru mengendalikan jualan, servis dan alat ganti untuk EV penumpang Dongfeng.",
               "由 MyKar World Sdn. Bhd.（公司编号 202501050786，1652194-X）经营。位于 81100 新山 Taman Ekoperniagaan, Jalan Ekoperniagaan 3/11 门牌 28 号的 3S 中心负责东风纯电乘用车的销售、服务和配件。")),
            (T("What are the opening hours?", "Apakah waktu operasi?", "营业时间是什么时候？"),
             T("Showroom: Monday to Saturday 9am to 6pm, Sunday 10am to 4pm. Workshop: Monday to Friday 9am to 6pm, Saturday 9am to 1pm, Sunday closed.",
               "Bilik pameran: Isnin hingga Sabtu 9 pagi hingga 6 petang, Ahad 10 pagi hingga 4 petang. Bengkel: Isnin hingga Jumaat 9 pagi hingga 6 petang, Sabtu 9 pagi hingga 1 tengah hari, Ahad tutup.",
               "展厅：周一至周六上午 9 点至下午 6 点，周日上午 10 点至下午 4 点。维修车间：周一至周五上午 9 点至下午 6 点，周六上午 9 点至下午 1 点，周日休息。")),
            (T("How do I reach sales and service?", "Bagaimana saya menghubungi jualan dan servis?", "如何联系销售和售后？"),
             T("Sales: WhatsApp +60 18-762 0828 or marketing@mykar.my. Service booking, aftersales and parts: WhatsApp +60 18-224 0828 or aftersales@mykar.my.",
               "Jualan: WhatsApp +60 18-762 0828 atau marketing@mykar.my. Tempahan servis, selepas jualan dan alat ganti: WhatsApp +60 18-224 0828 atau aftersales@mykar.my.",
               "销售：WhatsApp +60 18-762 0828 或 marketing@mykar.my。预约保养、售后和配件：WhatsApp +60 18-224 0828 或 aftersales@mykar.my。")),
        ],
    },
    'contact/': {
        'more': [
            T("For new cars, test drives and promotions, WhatsApp the sales line on +60 18-762 0828. For service booking, aftersales and spare parts, WhatsApp +60 18-224 0828. We are at No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru. The showroom is open Monday to Saturday 9am to 6pm and Sunday 10am to 4pm; the workshop is open Monday to Friday 9am to 6pm and Saturday 9am to 1pm.",
              "Untuk kereta baharu, pandu uji dan promosi, WhatsApp talian jualan di +60 18-762 0828. Untuk tempahan servis, selepas jualan dan alat ganti, WhatsApp +60 18-224 0828. Kami di No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru. Bilik pameran dibuka Isnin hingga Sabtu 9 pagi hingga 6 petang dan Ahad 10 pagi hingga 4 petang; bengkel dibuka Isnin hingga Jumaat 9 pagi hingga 6 petang dan Sabtu 9 pagi hingga 1 tengah hari.",
              "新车、试驾和优惠请 WhatsApp 销售专线 +60 18-762 0828；预约保养、售后和配件请 WhatsApp +60 18-224 0828。地址：81100 新山 Taman Ekoperniagaan, Jalan Ekoperniagaan 3/11 门牌 28 号。展厅营业时间为周一至周六上午 9 点至下午 6 点、周日上午 10 点至下午 4 点；维修车间为周一至周五上午 9 点至下午 6 点、周六上午 9 点至下午 1 点。"),
        ],
        'faqs': [
            (T("What is the fastest way to contact Dongfeng Johor Bahru?", "Apakah cara terpantas menghubungi Dongfeng Johor Bahru?", "联系东风新山最快的方式是什么？"),
             T("WhatsApp. Use +60 18-762 0828 for sales and +60 18-224 0828 for service, aftersales and spare parts.",
               "WhatsApp. Gunakan +60 18-762 0828 untuk jualan dan +60 18-224 0828 untuk servis, selepas jualan dan alat ganti.",
               "WhatsApp。销售请用 +60 18-762 0828，服务、售后和配件请用 +60 18-224 0828。")),
            (T("Is the workshop open on Sundays?", "Adakah bengkel dibuka pada hari Ahad?", "维修车间周日营业吗？"),
             T("No. The workshop is open Monday to Friday 9am to 6pm and Saturday 9am to 1pm, and is closed on Sunday. The showroom is open on Sunday from 10am to 4pm.",
               "Tidak. Bengkel dibuka Isnin hingga Jumaat 9 pagi hingga 6 petang dan Sabtu 9 pagi hingga 1 tengah hari, dan tutup pada hari Ahad. Bilik pameran dibuka pada hari Ahad dari 10 pagi hingga 4 petang.",
               "不营业。维修车间周一至周五上午 9 点至下午 6 点、周六上午 9 点至下午 1 点营业，周日休息。展厅周日上午 10 点至下午 4 点开放。")),
            (T("Should I message before visiting?", "Perlukah saya menghantar mesej sebelum melawat?", "到访前需要先发讯息吗？"),
             T("It helps. WhatsApp before you come so we can have the car you want to see charged and ready.",
               "Ia membantu. WhatsApp sebelum datang supaya kereta yang anda mahu lihat sudah dicas dan sedia.",
               "最好先发讯息。到访前 WhatsApp 我们，我们可以把您想看的车充好电备好。")),
        ],
    },
    'partners/': {
        'faqs': [
            (T("Who can partner with Dongfeng Johor Bahru?", "Siapa yang boleh bekerjasama dengan Dongfeng Johor Bahru?", "哪些对象可以与东风新山合作？"),
             T("Dealers, brands and companies in Johor, including fleets. We work from our showroom in Taman Ekoperniagaan and run roadshows across Johor.",
               "Pengedar, jenama dan syarikat di Johor, termasuk armada. Kami beroperasi dari bilik pameran di Taman Ekoperniagaan dan menjalankan jelajah di seluruh Johor.",
               "柔佛的经销商、品牌和企业，包括车队。我们以 Taman Ekoperniagaan 的展厅为基地，并在柔佛各地举办巡展。")),
            (T("How do I start a conversation?", "Bagaimana saya memulakan perbincangan?", "如何开始洽谈？"),
             T("WhatsApp +60 18-762 0828 or email marketing@mykar.my with a short note on your business and what you have in mind.",
               "WhatsApp +60 18-762 0828 atau e-mel marketing@mykar.my dengan nota ringkas tentang perniagaan anda dan idea anda.",
               "请 WhatsApp +60 18-762 0828 或电邮 marketing@mykar.my，简述您的业务和合作想法。")),
            (T("Where have you held roadshows?", "Di manakah anda pernah mengadakan jelajah?", "你们在哪里举办过巡展？"),
             T("In 2026: Sutera Mall, AEON Mall Bandar Dato' Onn, Lotus's Tebrau and KIPMall Kota Tinggi.",
               "Pada 2026: Sutera Mall, AEON Mall Bandar Dato' Onn, Lotus's Tebrau dan KIPMall Kota Tinggi.",
               "2026 年：Sutera Mall、AEON Mall Bandar Dato' Onn、Lotus's Tebrau 和 KIPMall Kota Tinggi。")),
        ],
    },
    'spare-parts/': {
        'more': [
            T("Genuine Dongfeng parts are ordered through our centre in Taman Ekoperniagaan, and parts are charged at Dongfeng's list prices. WhatsApp +60 18-224 0828 with your model, year and the part you need, with a photo if you can, and we check availability and arrange fitting. The workshop is open Monday to Friday 9am to 6pm and Saturday 9am to 1pm.",
              "Alat ganti Dongfeng tulen ditempah melalui pusat kami di Taman Ekoperniagaan, dan alat ganti dikenakan mengikut harga senarai Dongfeng. WhatsApp +60 18-224 0828 dengan model, tahun dan alat ganti yang anda perlukan, dengan foto jika boleh, dan kami semak ketersediaan serta atur pemasangan. Bengkel dibuka Isnin hingga Jumaat 9 pagi hingga 6 petang dan Sabtu 9 pagi hingga 1 tengah hari.",
              "原厂东风配件可通过我们位于 Taman Ekoperniagaan 的中心订购，配件按东风官方价目表收费。请 WhatsApp +60 18-224 0828，告知车型、年份和所需配件（最好附上照片），我们会查询库存并安排安装。维修车间营业时间：周一至周五上午 9 点至下午 6 点，周六上午 9 点至下午 1 点。"),
        ],
    },
}
