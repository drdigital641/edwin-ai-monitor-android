# -*- coding: utf-8 -*-
"""External photo candidates (Pexels free licence; Wikimedia Commons CC-BY/CC-BY-SA).
w/h are real pixel dimensions of url_large. Verified 200 image/jpeg via sandbox curl.
Commons originals are below 1600px wide (served unscaled); Commons credits require attribution.
generic=True means the photo is NOT of the named venue.
"""

_PX = "https://images.pexels.com/photos/{0}/pexels-photo-{0}.jpeg?auto=compress&cs=tinysrgb&w={1}"
_PG = "https://www.pexels.com/photo/{0}/"


def _p(pid, slug, w, h, alt_en, alt_zh, author, role, generic=False):
    return dict(
        url_large=_PX.format(pid, 1600), url_small=_PX.format(pid, 900),
        w=1600, h=h, orig_w=w, orig_h=h and None, alt_en=alt_en, alt_zh=alt_zh,
        credit="Photo: %s / Pexels" % author,
        source_page=_PG.format("%s-%s" % (slug, pid)), role=role, generic=generic)


def _px(pid, slug, ow, oh, alt_en, alt_zh, author, role, generic=False):
    h = round(1600 * oh / ow)
    d = _p(pid, slug, ow, h, alt_en, alt_zh, author, role, generic)
    d["orig_h"] = oh
    return d


PHOTOS_EXT = {
    # ---- hero (dark; check text-safe left area visually) ----
    "hero-misty-lanterns": _px(31767621, "misty-forest-pathway-at-twilight-with-lanterns", 2725, 1817,
        "Misty garden pathway at twilight lit by soft lanterns",
        "暮色薄雾中的花园小径，灯笼散发柔和光芒", "Samet Burak Dağlıoğlu", "hero"),
    "hero-temple-night": _px(30606165, "traditional-chinese-temple-at-night-in-chongqing", 5184, 3456,
        "Traditional Chinese temple lit at night with red lanterns",
        "夜晚亮灯的传统中式寺庙，悬挂红灯笼", "miyou_ 77", "hero"),

    # ---- mood / carousel ----
    "mood-lotus-pond": _px(12891912, "lotus-among-leaves-on-pond", 4445, 2963,
        "Pink lotus flower among green leaves on a calm pond",
        "平静池塘中绿叶间的粉色莲花", "Alexas Fotos", "mood"),
    "mood-lotus-bloom": _px(16717536, "close-up-of-a-lotus-flower", 5472, 3648,
        "Close-up of a pink lotus flower in bloom",
        "盛开粉色莲花特写", "Yvonne Lee", "mood"),
    "mood-white-lilies": _px(15312442, "close-up-of-a-bouquet-of-white-lilies", 3888, 2592,
        "Close-up of white lilies with green leaves",
        "白百合与绿叶特写", "Ashlee Marie", "mood"),
    "mood-garden-path": _px(36884894, "serene-garden-pathway-with-lush-greenery", 8192, 5464,
        "Garden pathway surrounded by lush greenery",
        "被茂盛绿植环绕的花园小径", "Shutter Speed", "mood"),
    "mood-incense-smoke": _px(13081588, "burning-incense-stick-with-white-smoke", 3024, 4032,
        "Burning incense stick with a thin trail of white smoke (portrait)",
        "燃烧的线香与袅袅白烟（竖幅）", "Nurgül Kelebek", "mood"),
    "mood-temple-eaves": _px(6531107, "traditional-asian-temple-facade-with-decorative-elements-and-red-lanterns", 4608, 3456,
        "Intricate Chinese temple roof against a blue sky",
        "蓝天下精致的中式寺庙屋檐", "John Lee", "mood", generic=True),
    "mood-lanterns": _px(18328759, "illuminated-traditional-lanterns", 6000, 4000,
        "Rows of glowing red lanterns at night",
        "夜晚成排发光的红灯笼", "Chris", "mood"),
    "mood-calm-lake": _px(31666728, "tranquil-lake-scene-at-sunrise-with-reflective-water", 5091, 3818,
        "Still lake at sunrise reflecting sky and trees",
        "日出时分平静湖面倒映天空与树木", "Courtney RA", "mood"),
    "mood-family-park": _px(33433751, "happy-family-in-a-lush-green-park-setting", 6048, 4024,
        "Family of three enjoying time together in a green park",
        "一家三口在绿意盎然的公园里共度时光", "Amodita's Frame", "mood"),
    "mood-singapore-skyline": _px(2499786, "photo-of-singapore-cityscape-during-golden-hour", 6000, 4000,
        "Singapore skyline and Marina Bay at golden hour",
        "黄金时刻的新加坡天际线与滨海湾", "Stijn Dijkstra", "mood"),

    # ---- services ----
    "svc-niches": _px(13069314, "modern-architecture-arcade", 5568, 3712,
        "Minimalist modern colonnade with clean lines and symmetry",
        "线条简洁、对称整齐的现代柱廊建筑", "Andrea Musto", "service:niches", generic=True),
    "svc-tablets": _px(20300733, "ornamented-sculptures-on-altar-wall-in-buddhist-temple", 5725, 3288,
        "Ornate gilded altar wall inside a Buddhist temple",
        "佛寺内金色华丽的神坛墙面", "phiraphon srithakae", "service:tablets", generic=True),
    "svc-funeral": _px(6724508, "a-person-holding-white-and-yellow-flowers-beside-a-candlelight", 6146, 4097,
        "Hands arranging white flowers beside a lit candle",
        "双手在烛光旁整理白色鲜花", "RDNE Stock project", "service:funeral"),
    "svc-will": _px(7054505, "a-person-signing-a-document", 5184, 2920,
        "Hand signing a document with a pen",
        "手持笔在文件上签名", "Kindel Media", "service:will"),

    # ---- venues ----
    "venue-nirvana": dict(
        url_large="https://upload.wikimedia.org/wikipedia/commons/8/80/Nirvana_Memorial_Garden_Singapore_%E6%96%B0%E5%8A%A0%E5%9D%A1%E5%AF%8C%E8%B4%B5%E5%B1%B1%E5%BA%84.jpg",
        url_small="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Nirvana_Memorial_Garden_Singapore_%E6%96%B0%E5%8A%A0%E5%9D%A1%E5%AF%8C%E8%B4%B5%E5%B1%B1%E5%BA%84.jpg/900px-Nirvana_Memorial_Garden_Singapore_%E6%96%B0%E5%8A%A0%E5%9D%A1%E5%AF%8C%E8%B4%B5%E5%B1%B1%E5%BA%84.jpg",
        w=1024, h=768,
        alt_en="Nirvana Memorial Garden columbarium, Singapore",
        alt_zh="新加坡富贵山庄骨灰安置所",
        credit="Nirvanafugui, CC BY-SA 4.0, Wikimedia Commons",
        source_page="https://commons.wikimedia.org/wiki/File:Nirvana_Memorial_Garden_Singapore_%E6%96%B0%E5%8A%A0%E5%9D%A1%E5%AF%8C%E8%B4%B5%E5%B1%B1%E5%BA%84.jpg",
        role="venue:nirvana", generic=False),
    # NOT Singapore: Nirvana Memorial Park, Thailand (GPS 13.24N 101.28E), 1344x768, CC BY 4.0, author Phasvarum.
    "venue-nirvana-alt": dict(
        url_large="https://upload.wikimedia.org/wikipedia/commons/5/50/Nirvana-memorial-park-garden.jpg",
        url_small="https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Nirvana-memorial-park-garden.jpg/900px-Nirvana-memorial-park-garden.jpg",
        w=1344, h=768,
        alt_en="Memorial park garden in front of a columbarium building",
        alt_zh="骨灰堂大楼前的纪念园林景观",
        credit="Phasvarum, CC BY 4.0, Wikimedia Commons",
        source_page="https://commons.wikimedia.org/wiki/File:Nirvana-memorial-park-garden.jpg",
        role="venue:nirvana", generic=True),
    # No Commons photos exist for Lin San Temple or Thian Leng; generic Pexels temples proposed.
    "venue-lin-san": _px(12587136, "interior-of-a-chinese-buddhist-temple", 5659, 3773,
        "Chinese Buddhist temple interior with red lanterns and ornate decor",
        "挂着红灯笼、装饰华美的中式佛寺内部", "vitalina", "venue:lin-san", generic=True),
    "venue-thian-leng": _px(20436778, "traditional-chinese-dragon-head-temple-roof-with-golden-elements", 6720, 4480,
        "Traditional Chinese temple roof with golden dragon ornaments",
        "饰有金色龙头的传统中式寺庙屋顶", "jacky xing", "venue:thian-leng", generic=True),
}

# tidy helper fields
for _v in PHOTOS_EXT.values():
    _v.pop("orig_h", None); _v.pop("orig_w", None)
