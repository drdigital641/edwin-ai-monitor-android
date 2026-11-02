"""Official photos from nirvana.com.sg (Nirvana Singapore). Benjamin is an agent through Advance Planners;
use is PENDING CLIENT APPROVAL (Benjamin to confirm Nirvana allows agents to use these). Hotlinked for the preview."""
B = 'https://nirvana.com.sg/wp-content/uploads/'
CR = 'Photo: Nirvana Singapore (nirvana.com.sg)'


def _n(path, w, h, alt_en, alt_zh, role, page='https://nirvana.com.sg/legacy-suites/'):
    return dict(url_large=B + path, url_small=B + path, w=w, h=h, alt_en=alt_en, alt_zh=alt_zh, credit=CR, source_page=page, role=role, generic=False, official=True)


PHOTOS_NV = {
    'nv-luxury-suite': _n('2024/01/Legacy-Suites-Luxury-Suites.jpg', 1125, 720, 'Gold-trimmed luxury columbarium suite at Nirvana Memorial Garden', '富贵山庄金色豪华骨灰福位套房', 'hero'),
    'nv-chandelier-hall': _n('2023/12/DSC03649-edit-crop.jpg', 1920, 1080, 'Chandelier hall with a golden centrepiece at Nirvana Memorial Garden', '富贵山庄水晶吊灯大厅与金色装饰', 'hero', 'https://nirvana.com.sg/legacy-suites/columbaria-pedestals/'),
    'nv-gold-suite': _n('2024/09/H512-01.jpg', 1920, 1440, 'Golden columbarium suite with seating at Nirvana Memorial Garden', '富贵山庄设有座椅的金色福位套房', 'hero', 'https://nirvana.com.sg/legacy-suites/suite-galleries/'),
    'nv-modern-suite': _n('2024/01/Legacy-Suites-Modern-Suites.jpg', 1125, 720, 'Modern columbarium suite with niches and lounge chairs', '设有福位与座椅的现代骨灰套房', 'service:niches'),
    'nv-tablet-hall': _n('2024/01/Block-A.jpg', 1920, 1080, 'Hall of ancestral tablets at Nirvana Memorial Garden', '富贵山庄神主牌殿堂', 'service:tablets', 'https://nirvana.com.sg/prayer-services/'),
    'nv-funeral-hall': _n('2023/12/20231202-F.png', 1920, 1080, 'Funeral parlour hall at Nirvana Memorial Garden', '富贵山庄殡仪礼堂', 'service:funeral', 'https://nirvana.com.sg/funeral-services/'),
    'nv-lobby': _n('2023/12/ATLT_0803-edit.jpg', 1920, 1280, 'Lobby with lotus artwork at Nirvana Memorial Garden', '富贵山庄饰有莲花艺术的大堂', 'venue:nirvana', 'https://nirvana.com.sg/'),
    'nv-lotus-gold': _n('2023/08/S78-07-945x475-2.jpg', 1580, 892, 'Golden and white lotus sculptures', '金白两色莲花雕塑', 'mood', 'https://nirvana.com.sg/legacy-suites/columbaria-pedestals/'),
    'nv-white-suite': _n('2025/01/Suite-H523-01.jpg', 1920, 1440, 'White and gold columbarium suite', '白金色调福位套房', 'mood', 'https://nirvana.com.sg/legacy-suites/suite-galleries/'),
    'nv-buddha-suite': _n('2024/09/Suite-93-01.jpg', 1920, 1280, 'Columbarium suite with a Buddha altar', '供奉佛像的福位套房', 'mood', 'https://nirvana.com.sg/legacy-suites/suite-galleries/'),
    'nv-gallery-lotus': _n('2023/08/gallery_img_3.png', 2100, 1050, 'White lotus sculpture', '白色莲花雕塑', 'mood', 'https://nirvana.com.sg/gallery/'),
    'nv-gallery-art': _n('2023/08/gallery_img_1.png', 2100, 1050, 'Golden sculpture in a garden setting', '园林中的金色雕塑', 'mood', 'https://nirvana.com.sg/gallery/'),
    'nv-corridor': _n('2023/08/gallery_img_10.png', 2100, 1050, 'Quiet marble corridor with golden lamps', '金色灯饰的宁静大理石长廊', 'mood', 'https://nirvana.com.sg/gallery/'),
    'nv-family-prayer': _n('2024/03/20231118_100122-edit-crop.jpg', 1920, 1080, 'Family paying respects before golden Buddha statues', '家人在金色佛像前礼拜', 'mood-family', 'https://nirvana.com.sg/prayer-services/'),
    'nv-offering': _n('2023/12/Image-031-edit.jpg', 1920, 1080, 'Making an offering at a prayer service', '在法会上供奉', 'mood', 'https://nirvana.com.sg/prayer-services/'),
}
