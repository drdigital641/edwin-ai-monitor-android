"""English copy for Hock Chuan Hiong. Same keys in strings_ms.py and strings_zh.py (build.py checks).
Facts (phone, address, hours, rating) live in facts.json and are never typed here."""

UI = {
    'skip': 'Skip to content', 'menu': 'Menu', 'close': 'Close menu', 'lang': 'Language',
    'home': 'Home', 'products': 'Products', 'festive': 'Gift boxes', 'wholesale': 'Wholesale', 'visit': 'Visit us',
    'story': 'Our story', 'articles': 'Articles', 'privacy': 'Privacy', 'breadcrumb': 'Breadcrumb',
    'wa_btn': 'WhatsApp to order', 'wa_short': 'WhatsApp', 'call_btn': 'Call the shop', 'call_short': 'Call',
    'wa_price': "WhatsApp for today's price", 'wa_wholesale': 'WhatsApp a wholesale order', 'wa_festive': 'Ask about gift boxes',
    'wa_pickup': 'Order for pickup',
    'non_halal': 'Our shop sells pork products.', 'non_halal_short': 'Non-Halal / Tidak Halal / 非清真',
    'hours_h': 'Opening hours', 'address_h': 'Address', 'contact_h': 'Contact', 'follow_h': 'Follow us',
    'maps': 'Open in Google Maps', 'map_title': 'Map to Hock Chuan Hiong in Bandar Bukit Tinggi 1, Klang',
    'facebook': 'Facebook', 'instagram': 'Instagram', 'threads': 'Threads', 'email': 'Email',
    'reviews': 'Read the reviews on Google', 'all_products': 'See all products', 'more_story': 'Read our story',
    'more_wholesale': 'Wholesale details', 'more_festive': 'Gift box details', 'more_visit': 'Hours and map',
    'prev': 'Previous', 'next': 'Next', 'carousel': 'Bak kwa photos', 'play': 'Play on Facebook',
    'reel': 'Facebook reel', 'opens_fb': 'Opens on Facebook',
    'daily': 'Daily', 'hours_short': 'Open daily, 9am to 8pm',
    'tagline': 'Bak kwa shop in Klang', 'since': '1996年老字号',
    'site_by': 'Website by AutoSEO.my',
    'photo_note': 'Photos: our own shop, stalls and products.',
}

PREFILL = {
    'default': "Hi Hock Chuan Hiong, I'd like to order bak kwa.",
    'wholesale': "Hi Hock Chuan Hiong, I'd like to ask about a wholesale bak kwa order.",
    'festive': "Hi Hock Chuan Hiong, I'd like to ask about your festive gift boxes.",
    'pickup': "Hi Hock Chuan Hiong, I'd like to order bak kwa for pickup at the shop.",
}

# alt text = what the photo really shows (manifest alts for drop 1; drop 2 written from the photos)
PHOTOS = {
    'bakkwa-closeup-hero': 'Close-up of glossy, chargrilled Hock Chuan Hiong bak kwa slices',
    'bakkwa-closeup-wide': 'Chargrilled bak kwa texture close-up',
    'bakkwa-closeup-card': 'Freshly grilled bak kwa slices',
    'bakkwa-grilled-pile-hero': 'A tray piled with glossy grilled Hock Chuan Hiong bak kwa',
    'bakkwa-grilled-pile-card': 'Glossy grilled bak kwa piled high',
    'vacuum-packed-bakkwa-slices': 'Individually vacuum-packed bak kwa pieces',
    'wholesale-carton-packed-bakkwa': 'A carton of individually packed bak kwa ready for wholesale',
    'wholesale-cartons-loading-van': 'Cartons of Hock Chuan Hiong bak kwa loaded into a van outside the Klang shop',
    'pork-floss-jars': 'Jars of Hock Chuan Hiong pork floss with the chef-pig label',
    'red-carry-bag': 'Red 福荃香 肉乾至尊 carry bag',
    'counter-signage-red-band': 'Red 福荃香 shop counter signage and carry bag',
    'packaging-emblem': 'Hock Chuan Hiong packaging emblem',
    'festive-display-gift-packs': 'Festive stall with red Hock Chuan Hiong packs, floss jars and a Non-Halal sign',
    'display-cart-red-packs': 'Glass display cart with bak kwa and red Hock Chuan Hiong packs',
    'popup-stall-canopy': 'Hock Chuan Hiong pop-up stall under a red canopy',
    'mobile-stall-truck': 'Hock Chuan Hiong mobile stall on a lorry',
    'bakkwa-display-case': 'Bak kwa in a glass display case',
    'logo': 'Hock Chuan Hiong 福荃香 logo',
    'og': 'Hock Chuan Hiong 福荃香 bak kwa, Klang',
}

# short captions on the carousel (inside the frame)
CAPS = {
    'bakkwa-grilled-pile-card': 'Fresh off the grill',
    'bakkwa-closeup-card': 'Pork bak kwa',
    'vacuum-packed-bakkwa-slices': 'Packed piece by piece',
    'pork-floss-jars': 'Pork floss jars',
    'display-cart-red-packs': 'Ready packs at our stall',
    'festive-display-gift-packs': 'Festive season table',
    'red-carry-bag': 'Take it home in red',
}

PRODUCT_ORDER = ['pork', 'sliced', 'goldcoin', 'chicken', 'porkfloss', 'chickenfloss', 'bacon', 'roti']
PRODUCTS = {
    'pork': {'name': 'Pork bak kwa', 'line': 'The classic minced-pork slice, grilled till glossy. 300g and 500g packs.'},
    'sliced': {'name': 'Sliced pork bak kwa', 'line': 'Made from sliced pork instead of minced.'},
    'goldcoin': {'name': 'Gold coin bak kwa', 'line': 'Coin-sized rounds, plus the Taiwan-style gold bar (台湾金条).'},
    'chicken': {'name': 'Chicken bak kwa', 'line': 'Bak kwa made with chicken.'},
    'porkfloss': {'name': 'Pork floss', 'line': 'In our chef-pig jars.'},
    'chickenfloss': {'name': 'Chicken floss', 'line': 'The chicken version of our floss.'},
    'bacon': {'name': 'Dong Po bacon', 'line': '东坡肉 bacon, and bacon floss (培根肉丝).'},
    'roti': {'name': 'Bak kwa roti', 'line': 'Bread made with our bak kwa.'},
}

HOME = {
    'title': 'Bak Kwa Klang | Hock Chuan Hiong 福荃香 Bukit Tinggi',
    'meta': 'Hock Chuan Hiong 福荃香 bak kwa shop in Bandar Bukit Tinggi 1, Klang. Pork and chicken bak kwa, floss and gift boxes. Open daily 9am to 8pm. WhatsApp to order.',
    'h1': 'Bak kwa in Klang, since 1996',
    'line': 'Glossy grilled bak kwa at our Bukit Tinggi shop, open daily 9am-8pm.',
    'products_h': 'What we grill and pack',
    'products_p': "Prices change with the season. WhatsApp for today's price.",
    'festive_h': 'Festive gift boxes',
    'festive_p': 'Bak kwa boxes for the two big seasons. Ask what is in this season’s boxes.',
    'festive_cny': 'Chinese New Year', 'festive_moon': 'Mooncake Festival',
    'wholesale_h': 'Wholesale orders welcome',
    'wholesale_p': 'Cartons of individually packed bak kwa. Tell us what you need on WhatsApp.',
    'visit_h': 'Order ahead, pick up in store',
    'visit_p': 'WhatsApp your order, then collect it at the shop in Bandar Bukit Tinggi 1.',
    'popup_h': 'Find us at pop-ups and festive stalls',
    'popup_p': 'We also set up stalls around the festive seasons. Follow us to see where we are next.',
    'story_h': 'Pandamaran roots',
    'story_p': 'Hock Chuan Hiong started at a stall in Pandamaran, Gerai 106 on Jalan Besar. Our shop sign still reads 1996年老字号. Today you will find us in Bandar Bukit Tinggi 1, Klang.',
    'reels_h': 'Watch us on Facebook',
    'reels_p': 'Short reels from our Facebook page.',
    'proof_h': 'What Klang says',
    'proof_line': 'from {n} Google reviews',
}

PRODUCTS_PAGE = {
    'title': 'Bak Kwa, Floss & Bacon in Klang | Hock Chuan Hiong 福荃香',
    'meta': 'Pork, sliced, gold coin and chicken bak kwa, pork and chicken floss, Dong Po bacon and bak kwa roti from Hock Chuan Hiong, Klang. Non-Halal. WhatsApp for today’s price.',
    'h1': 'Bak kwa, floss and bacon from our Klang shop',
    'lead': "Eight things we make. Prices change with the season, so WhatsApp for today's price.",
    'packed_h': 'Packed piece by piece',
    'packed_p': 'Many of our bak kwa pieces are vacuum-packed one by one, which makes them easy to share and gift.',
}

FESTIVE = {
    'title': 'Bak Kwa Gift Boxes for CNY & Mooncake | Hock Chuan Hiong Klang',
    'meta': 'Festive bak kwa gift boxes for Chinese New Year and the Mooncake Festival from Hock Chuan Hiong 福荃香, Klang. WhatsApp to ask about this season’s boxes.',
    'h1': 'Bak kwa gift boxes for Chinese New Year and Mooncake',
    'lead': 'Our festive boxes change each season. WhatsApp us to ask what is in them and today’s price.',
    'cny_p': 'Bak kwa is a Chinese New Year table favourite. Order your boxes early on WhatsApp.',
    'moon_p': 'Gift boxes for the Mooncake Festival, for family, friends and clients.',
    'how_h': 'How to order',
    'how': ['WhatsApp us the box and how many you need.', 'We reply with this season’s boxes and price.', 'Collect at the shop in Bandar Bukit Tinggi 1.'],
    'corporate_p': 'Buying for a company or many families? See wholesale.',
}

WHOLESALE = {
    'title': 'Bak Kwa Wholesale Klang | Hock Chuan Hiong 福荃香',
    'meta': 'Wholesale bak kwa orders welcome at Hock Chuan Hiong 福荃香, Klang. Cartons of individually packed bak kwa. WhatsApp +60 10-234 9328.',
    'h1': 'Bak kwa wholesale in Klang',
    'lead': 'Wholesale orders welcome. Cartons of individually packed bak kwa, straight from our shop.',
    'send_h': 'What to send us on WhatsApp',
    'send': ['Which products', 'How many cartons or pieces', 'The date you need them', 'Your business name'],
    'carton_p': 'Pieces are packed one by one and boxed in cartons, ready to share out.',
    'van_p': 'Cartons are loaded right outside our Klang shop.',
}

VISIT = {
    'title': 'Bak Kwa Shop in Bukit Tinggi, Klang | Hours & Map | Hock Chuan Hiong',
    'meta': 'Visit Hock Chuan Hiong 福荃香 at 40-00-01, Lorong Batu Nilam 1D, Bandar Bukit Tinggi 1, 41200 Klang. Open daily 9am to 8pm. Order on WhatsApp, pick up in store.',
    'h1': 'Visit our bak kwa shop in Bandar Bukit Tinggi, Klang',
    'lead': 'Walk in any day from 9am to 8pm, or WhatsApp your order and pick it up.',
    'pickup_h': 'Order ahead for pickup',
    'pickup': ['WhatsApp what you want.', 'We confirm today’s price.', 'Collect at the shop.'],
    'map_h': 'Find the shop',
}

STORY = {
    'title': 'Our Story: Pandamaran Roots | Hock Chuan Hiong 福荃香 Klang',
    'meta': 'Hock Chuan Hiong 福荃香 started at a stall in Pandamaran and now runs a bak kwa shop in Bandar Bukit Tinggi 1, Klang. Our shop sign reads 1996年老字号.',
    'h1': 'Our story, from Pandamaran to Bukit Tinggi',
    'lead': 'A Klang bak kwa name with Pandamaran roots.',
    'p1': 'Hock Chuan Hiong started at a stall in Pandamaran: Gerai 106, Jalan Besar.',
    'p2': 'The sign over our counter reads 1996年老字号, a name in bak kwa since 1996.',
    'p3': 'Today our shop is at Lorong Batu Nilam 1D in Bandar Bukit Tinggi 1, Klang, open every day.',
    'ben_h': 'Ben Gor’s 我的 Pandamaran 童年美食',
    'ben_p': 'On our Facebook page, Ben Gor (Ben哥) presents 我的 Pandamaran 童年美食, a food-story series about the Pandamaran food he grew up with. 35 episodes so far.',
    'ben_link': 'Watch the series on Facebook',
    'emblem_p': 'Look for this emblem on our packs.',
}

ARTICLES = {
    'title': 'Bak Kwa Articles | Hock Chuan Hiong 福荃香 Klang',
    'meta': 'Articles on bak kwa, floss and festive gifting from Hock Chuan Hiong 福荃香, a bak kwa shop in Klang.',
    'h1': 'Bak kwa articles',
    'empty': 'Articles from our shop will appear here soon. Until then, WhatsApp us your question.',
}

PRIVACY = {
    'title': 'Privacy | Hock Chuan Hiong 福荃香',
    'meta': 'How Hock Chuan Hiong handles the details you send when you contact us.',
    'h1': 'Privacy',
    'body': [
        ('What we receive', 'When you WhatsApp, call or email us, we receive the details you choose to send, such as your name, number and order.'),
        ('How we use it', 'We use these details only to reply to you and prepare your order. We do not sell your details.'),
        ('Website taps', 'This website counts taps on its contact buttons (WhatsApp, call, email, map) to see which buttons are used. It does not record your name or number.'),
        ('Your choices', 'To ask what we hold about you or to have it removed, email or WhatsApp us using the details on this site.'),
    ],
}

SCHEMA = {
    'description': 'Bak kwa shop in Bandar Bukit Tinggi 1, Klang, Selangor: pork, sliced, gold coin and chicken bak kwa, pork and chicken floss, Dong Po bacon, bak kwa roti and festive gift boxes. Non-Halal. Wholesale orders welcome.',
}

LLMS = {
    'intro': 'Hock Chuan Hiong 福荃香肉乾至尊 is a bak kwa (Chinese dried meat) shop in Bandar Bukit Tinggi 1, Klang, Selangor, Malaysia, with roots at a stall in Pandamaran. Non-Halal (pork products). Retail walk-in and in-store pickup, festive gift boxes (Chinese New Year, Mooncake Festival) and wholesale orders.',
}
