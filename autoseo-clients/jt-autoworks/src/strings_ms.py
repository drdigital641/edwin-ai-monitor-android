# JT Autoworks, salinan Bahasa Melayu. Kunci sama dengan strings_en.py (build gagal jika ada yang tiada).
# Fakta (nombor, alamat, harga, waktu) datang dari facts.json; {placeholder} diisi oleh build.py.
# Peraturan: tiada em dash, tiada fakta rekaan, nama pemilik hanya melalui {tech}.

UI = {
    'skip': 'Langkau ke kandungan',
    'menu': 'Menu', 'close': 'Tutup menu', 'lang': 'Bahasa',
    'wa_btn': 'WhatsApp kami', 'wa_short': 'WhatsApp', 'call_btn': 'Telefon 6222 3102', 'call_short': 'Telefon',
    'home': 'Utama', 'packages': 'Pakej', 'services': 'Perkhidmatan', 'find_us': 'Cara mencari kami', 'about': 'Tentang kami',
    'areas': 'Kawasan perkhidmatan', 'articles': 'Artikel', 'privacy': 'Privasi',
    'breadcrumb': 'Breadcrumb',
    'prev': 'Foto sebelumnya', 'next': 'Foto seterusnya',
    'play': 'Main video', 'tap_sound': 'Ketik untuk bunyi', 'load_fb': 'Dimainkan dari Facebook selepas anda ketik',
    'watch_more': 'Tonton lagi di Facebook',
    'hours_h': 'Waktu operasi', 'mon_fri': 'Isnin hingga Jumaat', 'sat': 'Sabtu', 'sun': 'Ahad', 'closed': 'Tutup',
    'hours_mf': '9:00 pagi hingga 5:00 petang', 'hours_sat': '9:00 pagi hingga 3:00 petang', 'hours_short': 'Isn hingga Jum 9 pagi hingga 5 petang, Sab 9 pagi hingga 3 petang, Ahad tutup',
    'address_h': 'Alamat bengkel', 'contact_h': 'Hubungi kami',
    'maps': 'Buka di Google Maps', 'directions': 'Dapatkan arah', 'reviews': 'Baca ulasan Google kami', 'write_review': 'Tulis ulasan Google',
    'facebook': 'Facebook', 'instagram': 'Instagram', 'email': 'E-mel',
    'credit': 'Website by AutoSEO.my',
    'per_litre': 'setiap liter tambahan', 'litres': 'liter', 'for3': 'untuk 3 servis',
    'pkg_wa': 'WhatsApp tentang Pakej {L}',
    'see_packages': 'Lihat tiga pakej', 'see_services': 'Semua perkhidmatan', 'see_find': 'Cara mencari kami',
    'faq_h': 'Soalan yang sering ditanya',
    'map_title': 'Peta JT Autoworks di Premier @ Kaki Bukit',
    'all_makes': 'Semua jenama kereta dialu-alukan.',
    'reel_more': 'Lagi klip dari bengkel',
    'legal': 'JT AUTOWORKS PTE. LTD.',
}

TECH = 'juruteknik kami'          # used while facts.flags.show_owner_name is false
TECH_CAP = 'Juruteknik kami'

# ---------- WhatsApp prefills (per page / per button) ----------
PREFILL = {
    'default': "Hai JT Autoworks, saya ingin bertanya tentang kereta saya. Model dan tahun kereta: ",
    'home': "Hai JT Autoworks, saya ingin bertanya tentang kereta saya. Model dan tahun kereta: ",
    'pkg_a': "Hai JT Autoworks, saya ingin bertanya tentang Pakej A (Liqui Moly Top Tec, 6L, $628).",
    'pkg_b': "Hai JT Autoworks, saya ingin bertanya tentang Pakej B (Castrol Edge, 6L, $528).",
    'pkg_c': "Hai JT Autoworks, saya ingin bertanya tentang Pakej C (Castrol Edge, 4L, $428).",
    'packages': "Hai JT Autoworks, saya ingin tahu pakej servis mana yang sesuai untuk kereta saya. Model dan tahun kereta: ",
    'services': "Hai JT Autoworks, saya ingin bertanya tentang pembaikan. Model dan tahun kereta: ",
    'diagnostics': "Hai JT Autoworks, saya mahu kereta saya didiagnosis. Masalah kereta: ",
    'aircon': "Hai JT Autoworks, aircond kereta saya tidak sejuk. Model dan tahun kereta: ",
    'battery': "Hai JT Autoworks, saya mahu bateri kereta saya diuji. Model dan tahun kereta: ",
    'ev': "Hai JT Autoworks, saya ingin bertanya tentang EV saya. Model dan tahun: ",
    'ppi': "Hai JT Autoworks, saya mahu pemeriksaan sebelum membeli kereta. Model dan tahun kereta: ",
    'towing': "Hai JT Autoworks, saya perlukan tunda. Lokasi saya: ",
    'german': "Hai JT Autoworks, saya ingin bertanya tentang kereta saya. Jenama, model dan tahun: ",
    'find_us': "Hai JT Autoworks, saya perlukan arah ke #02-52, Gate 1.",
    'about': "Hai JT Autoworks, saya ingin bertanya tentang kereta saya. Model dan tahun kereta: ",
    'areas': "Hai JT Autoworks, saya ingin membawa kereta saya ke bengkel. Model dan tahun kereta: ",
    'articles': "Hai JT Autoworks, saya ingin bertanya tentang kereta saya. Model dan tahun kereta: ",
    'privacy': "Hai JT Autoworks, saya ada soalan.",
    'reel_aircon': "Hai JT Autoworks, aircond kereta saya tidak sejuk. Model dan tahun kereta: ",
    'reel_battery': "Hai JT Autoworks, saya mahu bateri kereta saya diuji. Model dan tahun kereta: ",
    'reel_ev_light': "Hai JT Autoworks, lampu amaran EV saya menyala. Model dan tahun: ",
    'reel_dash_lights': "Hai JT Autoworks, ada lampu amaran menyala pada papan pemuka kereta saya. Model dan tahun kereta: ",
    'reel_ev_owners': "Hai JT Autoworks, saya ingin bertanya tentang servis EV saya. Model dan tahun: ",
    'reel_diagnostics': "Hai JT Autoworks, saya mahu kereta saya didiagnosis. Masalah kereta: ",
    'reel_used_car': "Hai JT Autoworks, saya mahu pemeriksaan sebelum membeli kereta. Model dan tahun kereta: ",
    'reel_oil_leak': "Hai JT Autoworks, saya rasa kereta saya ada kebocoran minyak. Model dan tahun kereta: ",
    'reel_bmw5': "Hai JT Autoworks, kereta saya tersentak-sentak. Model dan tahun kereta: ",
    'reel_new_chapter': "Hai JT Autoworks, saya ingin bertanya tentang kereta saya. Model dan tahun kereta: ",
}

# ---------- Reel captions (plain language, not the promo text) ----------
REELS = {
    'aircon': 'Aircond tidak sejuk? Cari kebocoran dahulu.',
    'battery': 'Uji bateri sebelum sebarang penggantian.',
    'ev_light': 'Lampu amaran EV, diperiksa dengan betul.',
    'dash_lights': 'Apa yang cuba disampaikan oleh lampu papan pemuka anda.',
    'ev_owners': 'Servis untuk pemilik EV selepas waranti.',
    'diagnostics': 'Punca masalah dahulu, kemudian baiki.',
    'used_car': 'Periksa kereta terpakai sebelum anda bayar.',
    'oil_leak': 'Mengesan kebocoran minyak hingga ke puncanya.',
    'bmw5': 'Masalah BMW 5 Series tersentak-sentak, sudah dikesan.',
    'new_chapter': 'Bengkel baharu kami di Premier @ Kaki Bukit.',
}

# ---------- Shared blocks ----------
PKG = {
    'h2': 'Pakej servis',
    'lead': 'Tiga pakej, setiap satu merangkumi 3 servis. Harga ditunjukkan sepenuhnya.',
    'name': 'Pakej {L}',
    'oil_line': '{oil}, minyak enjin {litres}L',
    'extra': 'Minyak tambahan ${x} setiap liter',
    'inc_h': 'Termasuk dalam setiap pakej',
    'common': {
        'oil_filter': 'Penapis minyak x{n}',
        'check_50': 'Pemeriksaan 50 titik x{n}',
        'aircon_flush_gas': 'Basuh aircond dan tambah gas x{n}',
        'tyre_rotation': 'Putaran tayar x{n}',
        'tyre_patch': 'Tampal tayar x{n}',
        'coolant': 'Tambah penyejuk enjin, sehingga 10L, x{n}',
    },
    'flush': 'Pembersih enjin Liqui Moly, bahan tambah minyak dan pembersih pic penyuntik',
    'windshield': 'Pembersih cermin depan Liqui Moly 50ml',
    'no_flush': 'Tiada set pembersih enjin atau pembersih cermin depan',
    'brake_fluid': 'Minyak brek hanya dibasuh apabila pad brek diganti.',
    'lifetime': 'Pelanggan pakej mendapat pemeriksaan percuma seumur hidup.',
    'visc': 'Gred minyak pada poster: {v}.',
    'poster_alt': 'Poster harga Pakej {L} JT Autoworks',
    'combined_alt': 'Pakej servis A, B dan C JT Autoworks bersebelahan',
}

PROCESS = {
    'h2': 'Cara kerja kami',
    'lead': 'Diagnosis dahulu, baru alat ganti.',
    'steps': [
        ('WhatsApp kami', 'Beritahu kami kereta anda dan masalahnya. Video pendek sangat membantu.'),
        ('Periksa dan diagnosis', 'Kami cari punca masalah sebelum bercakap tentang alat ganti.'),
        ('Sebut harga percuma', 'Anda mendapat sebut harga tanpa obligasi dan tanpa bayaran.'),
        ('Baiki yang perlu sahaja', 'Alat ganti hanya diganti apabila memang perlu.'),
        ('Ambil kereta anda', 'Kereta anda di tangan yang baik.'),
    ],
}

PROOF = {
    'h2': 'Mengapa pemandu kembali lagi',
    'items': [
        ('Upah $50', 'Masalah turbo yang disebut hampir $2,000 di tempat lain dibaiki di sini dengan upah $50, tanpa sebarang caj alat ganti.'),
        ('Masalah yang terlepas pandang di bengkel lain', 'BMW 5 Series yang asyik tersentak-sentak telah diperiksa di tempat lain. Kami mengesan puncanya yang sebenar.'),
        ('Sejak 2018. Seorang mekanik.', 'Satu hubungan yang dibina atas kepercayaan.'),
    ],
    'note': 'JT Autoworks dibuka di Premier @ Kaki Bukit pada Mei 2026.',
    'reviews_line': 'Baca apa yang pelanggan tulis di Google.',
}

PHOTOS = {
    'h2': 'Di dalam bengkel',
    'shopfront-corridor-tighter-4x5': 'Papan tanda JT Autoworks di unit #02-52',
    'mercedes-c-class-on-lift-4x5': 'Sebuah Mercedes-Benz di atas lif di JT Autoworks',
    'volkswagen-golf-cabriolet-on-lift-4x5': 'Sebuah Volkswagen Golf Cabriolet di atas lif di JT Autoworks',
    'shopfront-corridor-4x5': 'Bahagian depan JT Autoworks di Premier @ Kaki Bukit',
    'hero': 'Bahagian depan JT Autoworks di unit #02-52, Premier @ Kaki Bukit',
}

GATE = {
    'h2': 'Cari kami: Gate 1, unit #02-52',
    'lead': 'Premier @ Kaki Bukit mempunyai lebih 100 bengkel. Masuk melalui Gate 1 dan cari papan tanda kami di #02-52.',
    'landmarks_h': 'Mercu tanda berhampiran blok',
    'landmarks': {
        'Gate 1': 'Gunakan Gate 1 Premier @ Kaki Bukit.',
        'VICOM Inspection Centre': 'VICOM Inspection Centre ialah mercu tanda berhampiran.',
        'Kaki Bukit Camp': 'Kaki Bukit Camp ialah mercu tanda berhampiran.',
        'Bartley Rd East': 'Bartley Rd East berhampiran.',
        'POSB': 'Ada POSB berhampiran.',
    },
    'poster_alt': 'Poster lokasi JT Autoworks menunjukkan Gate 1 dan unit #02-52',
    'poster_labels': 'Poster ini juga menandakan Bike Labz, Sri Udhayan Coffee Bar, Atlas Vending Solutions dan KB-1 dalam blok ini.',
    'lost': 'Sesat dalam blok? WhatsApp kami dan kami akan membimbing anda ke #02-52.',
}

SERVICES = {
    'diagnostics': {
        'name': 'Diagnosis', 'card': 'Punca masalah dahulu. Tiada main teka dan tiada alat ganti yang tidak perlu.',
        'title': 'Diagnosis kereta di Kaki Bukit | JT Autoworks',
        'meta': 'Diagnosis kereta yang jujur di Premier @ Kaki Bukit, Gate 1. Kami cari punca dahulu dan ganti yang perlu sahaja. WhatsApp 8358 4927.',
        'h1': 'Diagnosis kereta di Kaki Bukit, punca masalah dahulu',
        'lead': 'Lampu amaran, kereta tersentak-sentak, bunyi yang tidak diketahui puncanya? Kami diagnosis sebelum menukar apa-apa.',
        'body': [
            'Banyak pembaikan menelan kos lebih tinggi kerana alat ganti ditukar sehingga masalah hilang. Kami buat sebaliknya: diagnosis yang betul dahulu, tiada main teka dan tiada penggantian alat ganti yang tidak perlu.',
            'Satu kerja turbo yang disebut hampir $2,000 di tempat lain dibaiki di sini dengan upah $50 tanpa caj alat ganti. Masalah BMW 5 Series tersentak-sentak yang terlepas pandang di bengkel lain telah dikesan dan dibaiki.',
        ],
        'list_h': 'Apa yang kami periksa',
        'list': ['Lampu amaran pada papan pemuka', 'Tersentak-sentak, teragak-agak dan enjin kasar', 'Masalah enjin dan kebocoran', 'Masalah elektrik', 'Lampu amaran EV'],
    },
    'aircon': {
        'name': 'Aircond', 'card': 'Tidak sejuk? Kami cari kebocoran dahulu, kemudian baiki.',
        'title': 'Baiki aircond kereta di Kaki Bukit | JT Autoworks',
        'meta': 'Aircond kereta tidak sejuk? JT Autoworks di Premier @ Kaki Bukit cari kebocoran dahulu, kemudian baiki. Basuh aircond dan tambah gas. WhatsApp 8358 4927.',
        'h1': 'Baiki aircond kereta di Kaki Bukit',
        'lead': 'Menambah gas tanpa mencari kebocoran hanya menangguhkan masalah. Kami cari kebocoran dahulu.',
        'body': [
            'Tambah gas sahaja tidak menghentikan kebocoran. Kami cari sebab aircond bocor sebelum menukar apa-apa, kemudian beri sebut harga tanpa obligasi dan tanpa bayaran.',
            'Basuh aircond dan tambah gas juga termasuk dalam setiap pakej servis.',
        ],
        'list_h': 'Kerja aircond',
        'list': ['Mengesan kebocoran', 'Basuh aircond', 'Tambah gas', 'Baiki bahagian yang bocor'],
    },
    'battery': {
        'name': 'Bateri', 'card': 'Diuji dahulu, diganti jika perlu sahaja, dengan pendaftaran dan pengekodan.',
        'title': 'Uji dan tukar bateri kereta di Kaki Bukit | JT Autoworks',
        'meta': 'Bateri kereta diuji dahulu di JT Autoworks, Premier @ Kaki Bukit. Diganti jika perlu sahaja, dengan pendaftaran dan pengekodan bateri. WhatsApp 8358 4927.',
        'h1': 'Uji dan tukar bateri kereta di Kaki Bukit',
        'lead': 'Kami uji bateri dahulu. Anda hanya menukarnya jika memang perlu.',
        'body': [
            'Kereta sukar dihidupkan tidak semestinya bateri sudah mati. Kami uji bateri dan sistem pengecasan dahulu supaya anda tidak membayar untuk bateri yang tidak diperlukan.',
            'Banyak kereta moden memerlukan bateri baharu didaftarkan dan dikodkan pada kereta. Kami lakukannya sebagai sebahagian daripada kerja ini.',
        ],
        'list_h': 'Kerja bateri',
        'list': ['Ujian bateri dan pengecasan', 'Ganti hanya apabila perlu', 'Pendaftaran dan pengekodan bateri'],
    },
    'ev': {
        'name': 'Diagnosis dan servis EV', 'card': 'Juruteknik terlatih EV. Pilihan berpatutan selepas waranti.',
        'title': 'Bengkel EV di Kaki Bukit | JT Autoworks',
        'meta': 'Diagnosis dan servis EV di Premier @ Kaki Bukit oleh juruteknik terlatih EV. Alternatif berpatutan selepas waranti pengilang. WhatsApp 8358 4927.',
        'h1': 'Bengkel EV di Kaki Bukit untuk diagnosis dan servis',
        'lead': 'Juruteknik terlatih EV, diagnosis dahulu, selepas waranti pengilang anda tamat.',
        'body': [
            'Apabila waranti pengilang tamat, ramai pemilik EV mencari alternatif yang berpatutan. Juruteknik terlatih EV kami mengendalikan diagnosis dan servis EV di Premier @ Kaki Bukit.',
            'Lampu amaran EV dilayan sama seperti masalah lain: kami cari puncanya sebelum menukar apa-apa. Tunda juga boleh diaturkan untuk EV.',
        ],
        'list_h': 'Kerja EV',
        'list': ['Diagnosis lampu amaran EV', 'Servis EV', 'Tunda diaturkan untuk EV'],
        'tags': 'Pemilik EV ini sering bertanya kepada kami:',
    },
    'ppi': {
        'name': 'Pemeriksaan sebelum membeli', 'card': 'Periksa kereta terpakai dengan betul sebelum anda membayar.',
        'title': 'Pemeriksaan kereta sebelum membeli di Kaki Bukit | JT Autoworks',
        'meta': 'Pemeriksaan kereta terpakai sebelum membeli di JT Autoworks, Premier @ Kaki Bukit. Ketahui apa yang anda beli sebelum membayar. WhatsApp 8358 4927.',
        'h1': 'Pemeriksaan kereta sebelum membeli di Kaki Bukit',
        'lead': 'Ketahui apa yang anda beli sebelum membayar.',
        'body': [
            'Kereta terpakai nampak bersih tetapi mungkin menyembunyikan masalah yang mahal. Bawa kepada kami sebelum anda membuat keputusan, kami akan memeriksanya dan memberitahu anda dengan jelas apa yang kami temui.',
        ],
        'list_h': 'Apa yang kami periksa',
        'list': ['Enjin dan kotak gear', 'Brek dan suspensi', 'Aircond dan elektronik', 'Kebocoran, kehausan dan tanda kemalangan'],
    },
    'towing': {
        'name': 'Tunda 24/7', 'card': 'Tunda diaturkan sepanjang masa, untuk kereta dan EV.',
        'title': 'Tunda kereta dan EV 24/7 diaturkan | JT Autoworks Kaki Bukit',
        'meta': 'Kereta rosak? JT Autoworks mengatur tunda 24/7 untuk kereta dan EV ke bengkel kami di Premier @ Kaki Bukit, Gate 1. WhatsApp 8358 4927.',
        'h1': 'Tunda 24/7 diaturkan untuk kereta dan EV',
        'lead': 'Kereta rosak? WhatsApp lokasi anda dan kami aturkan tunda.',
        'body': [
            'Kami mengatur tunda 24/7 untuk kereta dan EV ke bengkel kami di Premier @ Kaki Bukit. Hantar lokasi anda dan model kereta melalui WhatsApp supaya kami dapat mengatur tunda yang sesuai.',
            'Apabila kereta sudah bersama kami, ia mendapat pendekatan diagnosis dahulu yang sama: punca masalah dahulu, kemudian sebut harga tanpa obligasi dan tanpa bayaran.',
        ],
        'list_h': 'Hantar kepada kami melalui WhatsApp',
        'list': ['Lokasi anda', 'Jenama dan model kereta, atau model EV', 'Apa yang berlaku'],
    },
    'german': {
        'name': 'Kereta Jerman dan mewah', 'card': 'BMW, Mercedes-Benz, Audi, Porsche dan lain-lain. Semua jenama dialu-alukan.',
        'title': 'Bengkel BMW, Mercedes dan Audi di Kaki Bukit | JT Autoworks',
        'meta': 'Bengkel kereta Eropah dan mewah di Premier @ Kaki Bukit: BMW, Mercedes-Benz, Audi, Volkswagen, Porsche, Lexus, Land Rover, Volvo. Semua jenama dialu-alukan.',
        'h1': 'Bengkel BMW, Mercedes dan Audi di Kaki Bukit',
        'lead': 'Fokus kereta Eropah dan mewah, semua jenama dialu-alukan.',
        'body': [
            'Kereta Jerman dan mewah ialah fokus kami: BMW, Mercedes-Benz, Audi, Volkswagen dan Porsche, serta Lexus, Land Rover dan Volvo. Kereta ini memerlukan diagnosis yang teliti, dan main teka tidak sesuai.',
            'BMW 5 Series yang asyik tersentak-sentak telah pun dibawa ke bengkel lain. Kami mengesan puncanya yang sebenar. Apa pun kereta anda, pendekatan kami sama.',
        ],
        'list_h': 'Jenama yang menjadi fokus kami',
    },
}
SERVICE_ORDER = ['diagnostics', 'aircon', 'battery', 'ev', 'ppi', 'towing', 'german']
OTHER_SERVICES = {
    'h2': 'Juga di bengkel',
    'items': [('Pembaikan enjin', 'Didiagnosis dahulu, dibaiki dengan betul.'), ('Brek', 'Pemeriksaan dan pembaikan brek.'),
              ('Servis minyak', 'Atau jimat dengan salah satu daripada tiga pakej.'), ('Pemeriksaan 50 titik', 'Termasuk dalam setiap servis pakej.')],
}
CHECK_50 = {
    'engine': 'Enjin', 'brakes': 'Brek', 'suspension_steering': 'Suspensi dan stereng', 'tyres': 'Tayar',
    'electrical': 'Elektrik', 'lights': 'Lampu', 'fluids': 'Cecair', 'aircon': 'Aircond',
    'battery_charging': 'Bateri dan pengecasan', 'exhaust': 'Ekzos', 'safety': 'Ciri keselamatan', 'body_interior': 'Badan kereta dan dalaman',
}

# ---------- Pages ----------
HOME = {
    'title': 'Bengkel kereta diagnosis dahulu di Kaki Bukit | JT Autoworks',
    'meta': 'JT Autoworks, bengkel kereta di Premier @ Kaki Bukit, Gate 1, #02-52. Pakar kereta Eropah dan EV yang diagnosis dahulu, harga pakej jelas, semua jenama dialu-alukan.',
    'h1': 'Bengkel kereta diagnosis dahulu di Kaki Bukit',
    'line': 'Pakar kereta Eropah dan EV. Kami baiki yang perlu sahaja.',
    'chips': [('Diagnosis dahulu', 'Punca masalah sebelum alat ganti'), ('Sebut harga percuma', 'Tanpa obligasi, tanpa bayaran'), ('#02-52, Gate 1', 'Premier @ Kaki Bukit')],
    'intro_h': 'Bengkel kereta di Premier @ Kaki Bukit yang menerangkan sebelum mengenakan bayaran',
    'intro': 'JT Autoworks ialah bengkel kereta diagnosis dahulu di Kaki Bukit, di unit #02-52 Premier @ Kaki Bukit. Kami fokus pada BMW, Mercedes-Benz, Audi dan kereta Eropah lain serta EV, dan semua jenama dialu-alukan. Sebut harga diberi tanpa obligasi dan tanpa bayaran, dan alat ganti hanya diganti apabila perlu.',
    'svc_h': 'Apa yang kami lakukan',
    'lounge': 'Menunggu? Ada ruang rehat dengan minuman percuma.',
    'final_h': 'Beritahu kami masalah kereta anda',
    'final_line': 'WhatsApp 8358 4927. Video pendek tentang masalah itu sangat membantu.',
    'faq': [
        ('Apakah waktu operasi anda?', 'Isnin hingga Jumaat 9:00 pagi hingga 5:00 petang, Sabtu 9:00 pagi hingga 3:00 petang. Tutup pada hari Ahad.'),
        ('Di mana tepatnya bengkel ini?', 'Unit #02-52, Premier @ Kaki Bukit, 8 Kaki Bukit Ave 4, Singapore 415875. Masuk melalui Gate 1.'),
        ('Adakah anda mengenakan bayaran untuk sebut harga?', 'Tidak. Sebut harga diberi tanpa obligasi dan tanpa bayaran.'),
        ('Apa yang termasuk dalam pakej servis?', 'Setiap pakej merangkumi 3 servis dengan minyak enjin, penapis minyak, pemeriksaan 50 titik dan tambah penyejuk enjin setiap kali, serta basuh aircond dan tambah gas, putaran tayar dan tampal tayar sekali.'),
        ('Adakah anda membaiki EV?', 'Ya. Juruteknik terlatih EV mengendalikan diagnosis dan servis EV, dan tunda boleh diaturkan untuk EV.'),
        ('Jenama kereta apa yang anda servis?', 'Fokus kami ialah BMW, Mercedes-Benz, Audi, Volkswagen, Porsche, Lexus, Land Rover dan Volvo. Semua jenama dialu-alukan.'),
    ],
}

PACKAGES = {
    'title': 'Pakej servis minyak enjin di Kaki Bukit | JT Autoworks',
    'meta': 'Tiga pakej servis minyak enjin di JT Autoworks, Kaki Bukit: A $628 Liqui Moly Top Tec 6L, B $528 Castrol Edge 6L, C $428 Castrol Edge 4L. 3 servis setiap satu.',
    'h1': 'Pakej servis minyak enjin di Kaki Bukit',
    'lead': 'Tiga pakej, 3 servis setiap satu, dengan harga ditunjukkan sepenuhnya.',
    'compare_h': 'Ketiga-tiga pakej dalam satu poster',
    'faq': [
        ('Berapa banyak servis dalam satu pakej?', 'Setiap pakej merangkumi 3 servis.'),
        ('Apakah perbezaan antara pakej?', 'Pakej A menggunakan 6L Liqui Moly Top Tec ($628). Pakej B menggunakan 6L Castrol Edge ($528). Kedua-duanya termasuk pembersih enjin Liqui Moly, bahan tambah minyak dan pembersih pic penyuntik, serta pembersih cermin depan Liqui Moly 50ml. Pakej C menggunakan 4L Castrol Edge ($428) tanpa set pembersih enjin atau pembersih cermin depan.'),
        ('Bagaimana jika kereta saya perlukan lebih minyak?', 'Minyak tambahan ialah $29 setiap liter untuk Pakej A dan $20 setiap liter untuk Pakej B dan C.'),
        ('Gred minyak apa yang disenaraikan dalam pakej?', 'Poster pakej menyenaraikan 5W-40, 5W-30 dan 0W20.'),
        ('Adakah minyak brek termasuk?', 'Minyak brek hanya dibasuh apabila pad brek diganti.'),
        ('Adakah apa-apa selepas 3 servis?', 'Pelanggan pakej mendapat pemeriksaan percuma seumur hidup.'),
    ],
}

SERVICES_PAGE = {
    'title': 'Baiki dan servis kereta di Kaki Bukit | JT Autoworks',
    'meta': 'Diagnosis, aircond, bateri, servis EV, pemeriksaan sebelum membeli, tunda dan pembaikan kereta Eropah di JT Autoworks, Premier @ Kaki Bukit, Gate 1.',
    'h1': 'Baiki dan servis kereta di Kaki Bukit',
    'lead': 'Setiap kerja bermula dengan diagnosis. Semua jenama dialu-alukan.',
}

FIND = {
    'title': 'Cara mencari JT Autoworks di Premier @ Kaki Bukit, Gate 1',
    'meta': 'JT Autoworks terletak di 8 Kaki Bukit Ave 4, #02-52, Premier @ Kaki Bukit, Singapore 415875. Masuk melalui Gate 1. Peta, arah dan waktu operasi.',
    'h1': 'Cara mencari kami di Premier @ Kaki Bukit',
    'lead': 'Masuk melalui Gate 1, kemudian cari unit #02-52.',
}

ABOUT = {
    'title': 'Tentang JT Autoworks, bengkel baharu di Kaki Bukit',
    'meta': 'JT Autoworks dibuka di Premier @ Kaki Bukit pada Mei 2026: bengkel diagnosis dahulu untuk kereta Eropah dan EV, dengan harga jelas dan sebut harga percuma.',
    'h1': 'Tentang JT Autoworks',
    'lead': 'Bengkel baharu di Kaki Bukit, dengan tabiat lama: diagnosis dahulu.',
    'body': [
        'JT Autoworks dibuka di unit #02-52, Premier @ Kaki Bukit, pada Mei 2026. Bengkelnya baharu. Pendekatannya tidak.',
        'Sejak 2018. Seorang mekanik. Satu hubungan yang dibina atas kepercayaan. Pendekatannya tetap sama: cari punca sebenar, baiki masalah sebenar, dan ganti alat ganti hanya apabila perlu.',
        'Kami fokus pada kereta Eropah dan EV serta mengalu-alukan semua jenama. Sebut harga diberi tanpa obligasi dan tanpa bayaran, dan tiga pakej servis berharga sepenuhnya.',
    ],
    'values_h': 'Apa yang boleh anda harapkan',
    'values': [('Cepat membalas', 'WhatsApp soalan anda dan kami cepat membalas.'),
               ('Diagnosis jujur', 'Punca masalah dahulu. Tiada main teka dan tiada alat ganti yang tidak perlu.'),
               ('Harga jelas', 'Harga pakej sepenuhnya, dan sebut harga tanpa bayaran.'),
               ('Kerja boleh dipercayai', 'Kerja mahir, dibuat dengan betul pada kali pertama.')],
    'lounge': 'Semasa menunggu, ada ruang rehat dengan minuman percuma.',
}

AREAS = {
    'title': 'Bengkel kereta berhampiran Ubi, Eunos, Bedok dan Tampines | JT Autoworks',
    'meta': 'JT Autoworks melayani pemandu dari Kaki Bukit, Ubi, Eunos, Bedok, Tampines, Paya Lebar, MacPherson dan Hougang di Premier @ Kaki Bukit, Gate 1.',
    'h1': 'Bengkel kereta untuk Kaki Bukit dan kawasan sekitar',
    'lead': 'Satu bengkel, satu alamat: Premier @ Kaki Bukit, Gate 1, #02-52.',
    'area_h': 'Bengkel kereta untuk pemandu {area}',
    'area_p': 'Datang dari {area}? JT Autoworks terletak di Premier @ Kaki Bukit. Masuk melalui Gate 1 dan cari unit #02-52. Diagnosis dahulu, sebut harga tanpa bayaran, dan tiga pakej servis berharga sepenuhnya.',
    'here_p': 'Kami berada di Kaki Bukit sendiri, di Premier @ Kaki Bukit, 8 Kaki Bukit Ave 4. Masuk melalui Gate 1 dan cari unit #02-52.',
}

PRIVACY = {
    'title': 'Privasi | JT Autoworks',
    'meta': 'Cara JT Autoworks mengendalikan butiran yang anda hantar apabila menghubungi kami.',
    'h1': 'Privasi',
    'body': [
        ('Apa yang kami kumpul', 'Apabila anda WhatsApp, telefon atau e-mel kami, kami menerima butiran yang anda pilih untuk hantar, seperti nama, nombor, model kereta dan foto atau video masalah itu.'),
        ('Cara kami menggunakannya', 'Kami menggunakan butiran ini hanya untuk membalas anda, memberi sebut harga dan melakukan kerja pada kereta anda. Kami tidak menjual butiran anda.'),
        ('Ketikan di laman web', 'Laman web ini mengira ketikan pada butang hubungannya (WhatsApp, telefon, e-mel, peta) untuk melihat butang mana yang digunakan. Ia tidak merekod nama atau nombor anda.'),
        ('Pilihan anda', 'Untuk bertanya apa yang kami simpan tentang anda atau meminta ia dipadam, e-mel hao@jtautoworks.com.sg atau WhatsApp 8358 4927.'),
    ],
}

ARTICLES = {
    'title': 'Artikel penjagaan kereta | JT Autoworks Kaki Bukit',
    'meta': 'Artikel penjagaan kereta daripada JT Autoworks, bengkel diagnosis dahulu di Premier @ Kaki Bukit.',
    'h1': 'Artikel penjagaan kereta',
    'empty': 'Artikel dari bengkel akan muncul di sini tidak lama lagi. Sementara itu, WhatsApp soalan anda kepada kami.',
}

SCHEMA = {
    'description': 'Bengkel kereta diagnosis dahulu di Premier @ Kaki Bukit, Gate 1, #02-52. Pakar kereta Eropah dan EV, semua jenama dialu-alukan.',
}
LLMS = {
    'intro': 'JT Autoworks (JT AUTOWORKS PTE. LTD.) ialah bengkel kereta diagnosis dahulu di Premier @ Kaki Bukit, Singapore, yang fokus pada kereta Eropah dan EV, semua jenama dialu-alukan.',
}

# ---------- redesign blocks (20 Nov) ----------
LOOK = {
    'poster_alt': 'Poster JT Autoworks: {name}',
    'kicker': 'Premier @ Kaki Bukit, Gate 1, #02-52',
    'reels_h': 'Sorotan video',
    'reels_lead': 'Klip pendek dari bengkel. Ketik video untuk menontonnya.',
    'pkg_kicker': 'Harga jelas',
    'quotes_h': 'Kata pelanggan',
    'quotes': ['Pengetahuan beliau tentang kereta dan kemahiran membaiki memang terbaik.',
               'Saya langsung tidak risau membiarkan mereka mengurus servis dan pembaikan kereta saya!',
               'Saya percaya integriti dan kejujuran ialah sifat paling penting dalam perniagaan membaiki kereta.'],
    'quote_src': 'Daripada ulasan Google',
    'about_more': 'Tentang bengkel',
    'gallery_lead': 'Foto sebenar dari unit #02-52.',
}
