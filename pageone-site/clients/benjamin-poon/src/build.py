# -*- coding: utf-8 -*-
"""Benjamin Poon (潘国雄): personal consultant website, English + Simplified Chinese. Builds site/ (python3 build.py).

New Page One client, 22 Oct 2026 (Edwin). Spec: HANDOVER-from-client.md (client's own handover, 22 Oct 2026).
Facts used and where they came from:
- Client handover (from Benjamin via Edwin): name Benjamin Poon (潘国雄); WhatsApp/mobile +65 8932 9933; email
  benpoon.nirvana@gmail.com; represents Nirvana Singapore (富貴山庄; nirvana.com.sg is the company's site, not his);
  describes himself as 生命经理师 (English title pending); services: columbarium niches, ancestral tablets, funeral
  services, will planning (Certified Will Planner with Advance Planners, wording pending); joined around late 2025;
  three venues: Nirvana Memorial Garden (950 Old Choa Chu Kang Road S699816), Lin San Temple 灵山寺 (27 Lorong 12 Geylang
  S399004), Thian Leng Chong Toh Tong 天灵总道堂 (472 Changi Road S419890, name pending). English + Chinese only, no Malay.
- Award images supplied by Edwin (22 Oct 2026): "APG Sep 2025 Award, Benjamin Poon" (cropped: the sales dollar figure and
  the "$50K Elite Club" box/badge are removed, Edwin: do not show his award amount); "APG October 2025 Sales Award"
  awardees incl. Benjamin Poon (Advance Planners + 富貴 Nirvana logos); "APG May 2026 Sales Award" awardees incl. Benjamin
  Poon ("APG, Authorised Agency of 富貴 Nirvana"; 富貴山莊生命紀念館 CCK | 靈山寺 LIN SAN TEMPLE).
- Portrait: cropped from the Sep 2025 award image (no figures in the crop).
- Content modules in content/ (services, locations, guides) were written from the brief content/BRIEF.md; their sources
  are in each module's SOURCES list and in CONTENT_SOURCES.md.
Never shown anywhere: any sales or award dollar amount, prices, hours, tenure, testimonials, ratings, years of experience.
Open questions: CONFIRM below (also shown on the preview in dashed "PENDING CLIENT APPROVAL" boxes while LIVE is False).
"""
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get('BP_OUT', os.path.join(HERE, 'site'))

SLUG = 'benjamin-poon'
DOMAIN = 'benjaminpoon.sg'  # placeholder: domain not chosen or bought yet (PENDING)
LIVE = False
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
# Hidden from Google by the X-Robots-Tag header in pageonesingapore.com/preview/.htaccess, never a meta tag (Edwin, 17 Oct 2026).
IMG = os.environ.get('BP_IMG', 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@52ab531/site-assets/benjamin-poon/')
SHOW_PENDING = not LIVE
UPDATED = '2026-10-22'

NAME = 'Benjamin Poon'
NAME_ZH = '潘国雄'
TEL, TEL_SHOW = '+6589329933', '+65 8932 9933'
WA_NUM = '6589329933'
EMAIL = 'benpoon.nirvana@gmail.com'
NIRVANA = 'https://nirvana.com.sg/'
INDEXNOW_KEY = '5b8e2d7f1c9a4e06a3d2f8b7c6e1a940'

LANGS = ['en', 'zh']
PFX = {'en': '', 'zh': 'zh/'}
HREFLANG = {'en': 'en-SG', 'zh': 'zh-SG'}
LANG_ATTR = {'en': 'en-SG', 'zh': 'zh-Hans-SG'}
OG_LOCALE = {'en': 'en_SG', 'zh': 'zh_SG'}
LANG_LABEL = {'en': 'EN', 'zh': '中文'}
E = html.escape


def T(en, zh):
    return {'en': en, 'zh': zh}


def t(v, L):
    return v[L] if isinstance(v, dict) else v


def load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, 'content', name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


SV = load('services')
LO = load('locations')
GA, GB = load('guides_a'), load('guides_b')
SERVICES, LOCATIONS = SV.SERVICES, LO.LOCATIONS
PX = dict(load('photos_client').PHOTOS_CLIENT, **load('photos_nirvana').PHOTOS_NV, **load('photos').PHOTOS_EXT, **load('photos_booklet').PHOTOS_BK)  # licensed stock / Commons photos, hotlinked for the preview (see content/photos.py)


def role(r):
    return [k for k, v in PX.items() if v.get('role') == r]


HERO_KEYS = ['nv-chandelier-hall', 'nv-gold-suite', 'nv-lobby']  # warm, welcoming first; no niche-wall close-up as the opening image
MOOD_KEYS = role('mood')
def role_for(prefix, slug):
    for k, v in PX.items():
        r = v.get('role', '')
        if r.startswith(prefix) and r[len(prefix):] and r[len(prefix):] in slug:
            return k
    return MOOD_KEYS[0]


SVC_PHOTO = {s['slug']: role_for('service:', s['slug']) for s in SERVICES}
VENUE_PHOTO = {v['slug']: role_for('venue:', v['slug']) for v in LOCATIONS}
role = lambda r: [k for k, v in PX.items() if v.get('role') == r or k == r]
GUIDE_ORDER = ['columbarium-niche-vs-ancestral-tablet', 'questions-before-choosing-a-columbarium-niche', 'arranging-a-columbarium-viewing',
               'pre-planning-vs-immediate-funeral-arrangements', 'what-to-do-when-a-loved-one-passes-away-singapore',
               'will-planning-basics-singapore', 'preparing-for-a-memorial-planning-consultation']
_g = {g['slug']: g for g in GA.GUIDES + GB.GUIDES}
GUIDES = [_g[s] for s in GUIDE_ORDER if s in _g]

ROLE = T('Service Advisor · Life Managing Director (生命经理师)', '生命经理师 · Service Advisor')

CONFIRM = [
    T('How you represent Nirvana: your badge says "NVG Authorised Agency" and the award images say Advance Planners. Which name should the site use?',
      '您与富贵山庄的关系：名牌上写 "NVG Authorised Agency"，奖项图片则是 Advance Planners。网站应使用哪个名称？'),
    T('Written OK from Nirvana / Advance Planners to run a personal consultant website using their names (and later logos or official photos).',
      '富贵山庄 / Advance Planners 是否同意您以个人顾问名义建立网站并使用其名称（以及日后的标志或官方照片）。'),
    T('Exact name of the Changi Road venue in English and Chinese (天灵总道堂 or 天灵总道寺?), and which products you can offer at each of the three venues.',
      '樟宜路场所的正式中英文名称（天灵总道堂还是天灵总道寺？），以及您在三个场所各能提供哪些产品。'),
    T('Will planning: exact credential name and issuer ("Certified Will Planner"?), and the legal relationship of Advance Planners.',
      '遗嘱规划：证书的正式名称与颁发机构（"Certified Will Planner"？），以及 Advance Planners 的法律关系。'),
    T('Funeral services: who provides them (which funeral company) and what you arrange personally.',
      '殡葬服务：由哪家殡仪公司提供，哪些部分由您亲自安排。'),
    T('OK to show the three APG award images (dollar amounts removed) and your portrait.', '是否同意展示三张 APG 奖项图片（已去除金额）及您的个人照片。'),
    T('Real photos of each venue that you are allowed to use (or permission to use the operators\' photos).', '各场所可使用的真实照片（或运营方授权使用其照片）。'),
    T('Your domain name (e.g. benjaminpoon.sg, not bought yet) and whether the site should open in English or Chinese first.', '网站域名（例如 benjaminpoon.sg，尚未购买），以及网站默认显示英文还是中文。'),
]

# ------------------------------------------------------------------------------------------------
# Shared words
# ------------------------------------------------------------------------------------------------
W = {
    'nav': [('about-benjamin-poon/', T('About', '关于我')), ('services/', T('Services', '服务')), ('nirvana-products-services/', T('Nirvana', '富贵山庄')), ('locations/', T('Locations', '地点')),
            ('guides/', T('Guides', '指南')), ('contact/', T('Contact', '联系'))],
    'home': T('Home', '首页'),
    'menu': T('Menu', '菜单'),
    'whatsapp': T('WhatsApp', 'WhatsApp'),
    'call': T('Call', '致电'),
    'more': T('More details', '了解更多'),
    'read': T('Read guide', '阅读指南'),
    'pending': T('PENDING CLIENT APPROVAL', '待客户确认'),
    'pending_note': T('Preview only. These points will be confirmed with Benjamin before the site goes live:', '仅预览可见。以下内容上线前需与 Benjamin 确认：'),
    'faq': T('Common questions', '常见问题'),
    'related': T('Related pages', '相关页面'),
    'band_h': T('Talk to Benjamin directly', '直接与 Benjamin 联系'),
    'band_p': T('WhatsApp or call +65 8932 9933. English or Chinese, at your pace, no obligation.', 'WhatsApp 或致电 +65 8932 9933。中英文皆可，按您的节奏，没有任何义务。'),
    'wa_home': T('Hello Benjamin, I found your website homepage and would like to understand your services.', '您好 Benjamin，我在您的网站首页看到您的服务，想进一步了解。'),
    'wa_btn': T('WhatsApp Benjamin', 'WhatsApp 联系 Benjamin'),
    'independent': T('This is Benjamin Poon\'s personal professional website. It is not the official website of Nirvana Singapore, Lin San Temple, Thian Leng Chong Toh Tong or Advance Planners.',
                     '本网站为潘国雄（Benjamin Poon）的个人专业网站，并非富贵山庄（Nirvana Singapore）、灵山寺、天灵总道堂或 Advance Planners 的官方网站。'),
    'ftr_about': T('Benjamin Poon (潘国雄) helps Singapore families with columbarium niches, ancestral tablets, funeral arrangements and will planning, in English and Chinese.',
                   '潘国雄（Benjamin Poon）以中英文协助新加坡家庭了解福位、神主牌、殡葬安排与遗嘱规划。'),
    'privacy': T('Privacy policy', '隐私政策'),
    'disclaimer': T('Disclaimer', '免责声明'),
    'explore': T('Explore', '浏览'),
    'contact_h': T('Contact', '联系方式'),
    'built': T('Website by', '网站制作'),
    'updated': T('Updated', '更新于'),
    'by': T('By Benjamin Poon', '作者：潘国雄 Benjamin Poon'),
    'min': T('min read', '分钟阅读'),
    'address': T('Address', '地址'),
    'official': T('Official website', '官方网站'),
    'map': T('Map', '地图'),
    'open_map': T('Open in Google Maps', '在 Google 地图打开'),
    'ask': T('Ask Benjamin', '请询问 Benjamin'),
}

SVG = {
    'wa': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>',
    'phone': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>',
    'mail': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
    'niche': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg>',
    'tablet': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M7 21V7a5 5 0 0 1 10 0v14M5 21h14M10 11h4M10 15h4"/></svg>',
    'funeral': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M12 21c-4-3-7-6-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 11c0 4-3 7-7 10z"/></svg>',
    'will': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 3h9l3 3v15H6z"/><path d="M9 9h6M9 13h6M9 17h3"/></svg>',
    'book': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2z"/><path d="M4 19V5M8 7h7"/></svg>',
}
SVC_ICON = {'columbarium-niches': 'niche', 'ancestral-tablets': 'tablet', 'funeral-services': 'funeral', 'will-planning': 'will'}
VENUE_MARK = {'nirvana-memorial-garden': '富贵山庄', 'lin-san-temple': '灵山寺', 'thian-leng-temple': '天灵总道堂'}

PHOTOS = {  # name: (file, w, h, alt)
    'portrait': ('benjamin-badge.webp', 1000, 1000, T('Benjamin Poon (潘国雄), Service Advisor and Life Managing Director (生命经理师) 2025', '潘国雄（Benjamin Poon），生命经理师 Life Managing Director 2025，Service Advisor')),
    'face': ('benjamin-badge-sm.webp', 240, 240, T('Benjamin Poon (潘国雄)', '潘国雄（Benjamin Poon）')),
    'award-sep': ('award-sep-2025.webp', 1200, 469, T('APG September 2025 Award banner naming Benjamin Poon', 'APG 2025 年 9 月奖项海报，获奖者潘国雄（Benjamin Poon）')),
    'award-oct': ('award-oct-2025.webp', 960, 600, T('APG October 2025 Sales Award awardees, including Benjamin Poon', 'APG 2025 年 10 月销售奖获奖名单，包括潘国雄（Benjamin Poon）')),
    'award-may': ('award-may-2026.webp', 960, 600, T('APG May 2026 Sales Award awardees, including Benjamin Poon', 'APG 2026 年 5 月销售奖获奖名单，包括潘国雄（Benjamin Poon）')),
}


def img(name, L, eager=False, cls='', small=False):
    if name in PX:
        x = PX[name]
        src, w, h, alt = (x.get('url_small') if small and x.get('url_small') else x['url_large']), x['w'], x['h'], T(x['alt_en'], x['alt_zh'])
    else:
        f, w, h, alt = PHOTOS[name]
        src = IMG + f
    return '<img src="%s" alt="%s" width="%d" height="%d"%s%s>' % (E(src), E(t(alt, L)), w, h,
                                                                     ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"', ' class="%s"' % cls if cls else '')


def wa_url(msg, L):
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(t(msg, L)))


def wa_btn(msg, L, label=None, cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener" data-wa="1">%s<span>%s</span></a>' % (cls, E(wa_url(msg, L)), SVG['wa'], E(t(label or W['wa_btn'], L)))


def call_btn(L):
    return '<a class="btn btn-ghost" href="tel:%s">%s<span>%s %s</span></a>' % (TEL, SVG['phone'], E(t(W['call'], L)), TEL_SHOW)


def pending_box(items, L):
    if not SHOW_PENDING or not items:
        return ''
    return '<div class="pending" role="note"><strong>%s</strong><br>%s<ul>%s</ul></div>' % (
        E(t(W['pending'], L)), E(t(W['pending_note'], L)), ''.join('<li>%s</li>' % E(t(i, L)) for i in items))


def rich(s):
    """Content strings may hold <strong>, <em> and <a href>; everything else is escaped."""
    keep = []

    def stash(m):
        keep.append(m.group(0))
        return '\x00%d\x00' % (len(keep) - 1)
    s = re.sub(r'</?(strong|em)>|<a href="[^"<>]*"(?: target="_blank" rel="noopener")?>|</a>', stash, s)
    s = E(s, quote=False)
    s = re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], s)
    # external links open in a new tab
    return re.sub(r'<a href="(https?://[^"]+)">', r'<a href="\1" target="_blank" rel="noopener">', s)


def sections_html(secs, L):
    out = []
    for s in secs:
        part = ['<h2>%s</h2>' % E(t(s['h'], L))]
        part += ['<p>%s</p>' % rich(t(p, L)) for p in s.get('p', [])]
        if s.get('list'):
            tag = 'ol' if s.get('ol') else 'ul'
            part.append('<%s>%s</%s>' % (tag, ''.join('<li>%s</li>' % rich(t(i, L)) for i in s['list']), tag))
        if s.get('table'):
            head = [t(h, L) for h in s['table']['head']]
            rows = ''.join('<tr>%s</tr>' % ''.join('<td data-h="%s">%s</td>' % (E(head[i]) if i < len(head) else '', rich(t(c, L))) for i, c in enumerate(r))
                           for r in s['table']['rows'])
            part.append('<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>' % (''.join('<th>%s</th>' % E(h) for h in head), rows))
        if s.get('p_after'):
            part += ['<p>%s</p>' % rich(t(p, L)) for p in s['p_after']]
        out.append(''.join(part))
    return ''.join(out)


def faq_html(items, L):
    if not items:
        return ''
    return '<section class="faq"><h2>%s</h2>%s</section>' % (E(t(W['faq'], L)), ''.join(
        '<details><summary>%s</summary><p>%s</p></details>' % (E(t(q, L)), rich(t(a, L))) for q, a in items))


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


def faq_schema(items, L):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': t(q, L), 'acceptedAnswer': {'@type': 'Answer', 'text': strip_tags(t(a, L))}} for q, a in items]}


def find_title(path, L):
    for s in SERVICES:
        if path == 'services/%s/' % s['slug']:
            return t(s['card'], L), t(s['card_text'], L)
    for v in LOCATIONS:
        if path == 'locations/%s/' % v['slug']:
            return t(v['name'], L), t(v['card_text'], L)
    for g in GUIDES:
        if path == 'guides/%s/' % g['slug']:
            return t(g['h1'], L), t(g['card_text'], L)
    named = dict(W['nav'])
    if path == NB_PATH:
        return t(T('Nirvana products & services', '富贵山庄产品与服务'), L), t(T('A general guide to the columbarium suites, tablets, ceremonies, funeral services and facilities.', '福殿、神主牌、法会、殡仪服务与设施总览。'), L)
    if path in named:
        return t(named[path], L), ''
    return None, None


def related_html(paths, L):
    cards = []
    for p in paths or []:
        title, text = find_title(p, L)
        if title:
            cards.append('<a class="acard" href="%s"><figure>%s</figure><div class="ac-body"><h3>%s</h3><p>%s</p><span class="more">%s</span></div></a>' % (
                p, img(path_photo(p), L, small=True), E(title), E(text or ''), E(t(W['more'], L))))
    if not cards:
        return ''
    return '<section class="sec sec-white"><div class="wrap"><h2>%s</h2><div class="acards">%s</div></div></section>' % (E(t(W['related'], L)), ''.join(cards))


def path_photo(p):
    for s_ in SERVICES:
        if p == 'services/%s/' % s_['slug']:
            return SVC_PHOTO[s_['slug']]
    for v in LOCATIONS:
        if p == 'locations/%s/' % v['slug']:
            return VENUE_PHOTO[v['slug']]
    for g in GUIDES:
        if p == 'guides/%s/' % g['slug']:
            return guide_photo(g)
    if p == NB_PATH:
        return 'nb-modern-suites'
    return (MOOD_KEYS or list(PX))[0]


def aside(L, msg):
    return ('<aside class="aside">%s<h3>Benjamin Poon %s</h3><p>%s</p>%s<p style="margin-top:12px"><a href="tel:%s">%s</a><br><a href="mailto:%s">%s</a></p></aside>') % (
        img('portrait', L), NAME_ZH, E(t(ROLE, L)), wa_btn(msg, L), TEL, TEL_SHOW, EMAIL, EMAIL)


# ------------------------------------------------------------------------------------------------
# Page bodies
# ------------------------------------------------------------------------------------------------
FAQ_HOME = [
    (T('Who is Benjamin Poon?', 'Benjamin Poon（潘国雄）是谁？'),
     T('Benjamin Poon (潘国雄) is a Service Advisor and Life Managing Director in Singapore who represents Nirvana Singapore. He helps families understand columbarium niches, ancestral tablets, funeral arrangements and will planning, in English or Chinese.',
       '潘国雄（Benjamin Poon）是新加坡的生命经理师，代表富贵山庄（Nirvana Singapore）。他以中文或英文协助家庭了解福位、神主牌、殡葬安排与遗嘱规划。')),
    (T('Is this the official Nirvana website?', '这是富贵山庄的官方网站吗？'),
     T('No. This is Benjamin\'s personal website. The company\'s official website is <a href="https://nirvana.com.sg/">nirvana.com.sg</a>.',
       '不是。这是 Benjamin 的个人网站。公司官方网站为 <a href="https://nirvana.com.sg/">nirvana.com.sg</a>。')),
    (T('Can I plan ahead without committing on the first call?', '第一次咨询就要做决定吗？'),
     T('No. A first conversation is for questions and options. Benjamin explains what is available and you decide in your own time.',
       '不需要。第一次交谈只是了解问题与选择。Benjamin 会说明有哪些选项，您可按自己的时间做决定。')),
    (T('Which places can Benjamin help with?', 'Benjamin 可协助哪些地点？'),
     T('He works with three venues: Nirvana Memorial Garden on Old Choa Chu Kang Road, Lin San Temple in Geylang and Thian Leng Chong Toh Tong on Changi Road. See <a href="locations/">Locations</a>.',
       '他主要协助三个地点：位于旧蔡厝港路的富贵山庄、芽笼的灵山寺，以及樟宜路的天灵总道堂。详见<a href="locations/">地点</a>。')),
]

STEPS = [
    (T('Message or call', 'WhatsApp 或致电'), T('Tell Benjamin what you are looking into. English or Chinese.', '告诉 Benjamin 您想了解什么，中英文皆可。')),
    (T('Talk through options', '了解选择'), T('He explains niches, tablets, funeral or will options in plain words.', '他以浅白的方式说明福位、神主牌、殡葬或遗嘱的选项。')),
    (T('Visit if you wish', '可安排参观'), T('Arrange a viewing at the venue with Benjamin at a time that suits your family.', '在方便的时间与 Benjamin 一同参观场所。')),
    (T('Decide in your own time', '按您的节奏决定'), T('No pressure. He helps with the paperwork once your family is ready.', '没有压力。家人准备好后，他会协助办理手续。')),
]


def svc_card(s, L, i=0):
    return '<a class="pcard" href="services/%s/"><figure>%s</figure><div class="pc-body"><span class="tag">%02d</span><h3>%s</h3><p>%s</p><span class="more">%s</span></div></a>' % (
        s['slug'], img(SVC_PHOTO[s['slug']], L, small=True), i + 1, E(t(s['card'], L)), E(t(s['card_text'], L)), E(t(W['more'], L)))


def venue_card(v, L):
    return ('<a class="pcard" href="locations/%s/"><figure>%s</figure><div class="pc-body"><span class="tag">%s</span><h3>%s</h3><p>%s</p>'
            '<p class="addr">%s</p><span class="more">%s</span></div></a>') % (
        v['slug'], img(VENUE_PHOTO[v['slug']], L, small=True), VENUE_MARK.get(v['slug'], ''), E(t(v['name'], L)), E(t(v['card_text'], L)),
        E(v['address'] if L == 'en' else v.get('address_zh') or v['address']), E(t(W['more'], L)))


def guide_photo(g):
    i = GUIDES.index(g) if g in GUIDES else 0
    pool = MOOD_KEYS or list(PX)
    return pool[(i * 3 + 1) % len(pool)]


def guide_card(g, L):
    return '<a class="acard" href="guides/%s/"><figure>%s</figure><div class="ac-body"><span class="meta">%d %s</span><h3>%s</h3><p>%s</p><span class="more">%s</span></div></a>' % (
        g['slug'], img(guide_photo(g), L, small=True), g.get('read_min', 5), E(t(W['min'], L)), E(t(g['h1'], L)), E(t(g['card_text'], L)), E(t(W['read'], L)))


def glide(keys, L, caps=None, cls=''):
    return '<div class="glide" role="region" aria-label="%s" tabindex="0">%s</div>' % (E(t(T('Photo carousel', '图片轮播'), L)), ''.join(
        '<figure class="gl-item %s">%s<figcaption>%s</figcaption></figure>' % (cls, img(k, L, small=True), E(t(caps[i], L)) if caps else E(t(T(PX[k]['alt_en'], PX[k]['alt_zh']), L)) if k in PX else '')
        for i, k in enumerate(keys)))


def sec_head(eb, h, p, L, center=False):
    return '<div class="sec-head%s"><span class="eyebrow">%s</span><h2>%s</h2>%s</div>' % (' center' if center else '', E(t(eb, L)), E(t(h, L)), '<p>%s</p>' % E(t(p, L)) if p else '')


AWARD_CAPS = [T('APG September 2025 Award', 'APG 2025 年 9 月奖项'), T('APG October 2025 Sales Award awardee', 'APG 2025 年 10 月销售奖获奖者'),
              T('APG May 2026 Sales Award awardee', 'APG 2026 年 5 月销售奖获奖者')]


def awards_html(L):
    return glide(['award-sep', 'award-oct', 'award-may'], L, AWARD_CAPS, cls='wide contain')


def title_lines(eb, h, L, sub=None):
    return '<div class="tl"><span class="eyebrow-c">%s</span><h2>%s</h2>%s</div>' % (E(t(eb, L)), E(t(h, L)), '<p>%s</p>' % E(t(sub, L)) if sub else '')


def zz_row(s, L, i):
    return ('<article class="zz%s"><figure>%s</figure><div class="zz-text"><span class="num">%02d</span><span class="eyebrow">%s</span><h3>%s</h3><p>%s</p>'
            '<a class="btn btn-outline" href="services/%s/">%s</a></div></article>') % (
        ' rev' if i % 2 else '', img(SVC_PHOTO[s['slug']], L), i + 1, E(t(T('Service', '服务'), L)), E(t(s['card'], L)), E(t(s['card_text'], L)), s['slug'], E(t(T('Explore', '了解更多'), L)))


def nb_feature(L):
    return ('<a class="nbfeat" href="%s"><figure>%s</figure><div><span class="eyebrow">%s</span><h3>%s</h3><p>%s</p><span class="more">%s</span></div></a>') % (
        NB_PATH, img('nb-royal-suite', L, small=True), E(t(T('Nirvana Memorial Garden · 富贵山庄', '富贵山庄 · Nirvana Memorial Garden'), L)),
        E(t(T('See all Nirvana products & services', '浏览富贵山庄全部产品与服务'), L)),
        E(t(T('Columbarium suites, ancestral tablets, prayer ceremonies, funeral services, the FRECCIA hearse and more, in one illustrated guide.', '福殿、神主牌、法会、殡仪服务、FRECCIA 灵车等，一页图文总览。'), L)),
        E(t(W['more'], L)))


def home_body(L):
    hero_imgs = ''.join(img(k, L, eager=(i == 0)) for i, k in enumerate(HERO_KEYS[:3]))
    hero_steps = ''.join('<li><span>%02d</span><b>%s</b></li>' % (i + 1, E(t(a_, L))) for i, (a_, b_) in enumerate(STEPS))
    hero = ('<section class="hero"><figure class="hero-bg" aria-hidden="true">%s</figure><div class="wrap"><div class="hero-in">'
            '<span class="eyebrow-c light">%s</span><h1>%s</h1><p class="hero-sub">%s</p>'
            '<div class="cta-row center">%s<a class="btn btn-ghost" href="services/">%s</a></div></div>'
            '<div class="hero-steps"><p>%s</p><ol>%s</ol></div></div></section>') % (
        hero_imgs, E(t(T('Benjamin Poon 潘国雄 · Service Advisor · Life Managing Director · Singapore', '潘国雄 Benjamin Poon · 生命经理师 · 新加坡'), L)),
        E(t(T('Columbarium niches, ancestral tablets, funerals & wills', '福位 · 神主牌 · 殡葬安排 · 遗嘱规划'), L)),
        E(t(T('Personal, no-pressure guidance at Nirvana Memorial Garden, Lin San Temple and Thian Leng, explained in English or 中文.',
              '在富贵山庄、灵山寺与天灵总道堂，为您亲自讲解、安排参观，没有压力，中英文皆可。'), L)),
        wa_btn(W['wa_home'], L), E(t(T('See the 4 services', '查看 4 项服务'), L)),
        E(t(T('How it works', '咨询流程'), L)), hero_steps)
    facts = [(T('4 services', '4 项服务'), T('Niches · Tablets · Funerals · Wills', '福位 · 神主牌 · 殡葬 · 遗嘱')),
             (T('3 venues', '3 个地点'), T('CCK · Geylang · Changi Road', '蔡厝港 · 芽笼 · 樟宜路')),
             (T('English / 中文', '中文 / English'), T('Explained in your language', '用您习惯的语言说明')),
             (T('Direct line', '直接联系'), T('WhatsApp +65 8932 9933', 'WhatsApp +65 8932 9933'))]
    intro = ('<section class="sec intro" id="intro"><div class="wrap narrow center"><span class="eyebrow-c">%s</span><h2 class="statement">%s</h2><p class="lead">%s</p>'
             '<div class="facts">%s</div><p class="hero-note">%s</p></div></section>') % (
        E(t(T('Benjamin Poon · 潘国雄', '潘国雄 · Benjamin Poon'), L)),
        E(t(T('Thoughtful guidance for the arrangements that matter most', '为最重要的安排，提供用心的指引'), L)),
        E(t(T('Clear, respectful guidance on memorial options and life planning in Singapore. Speak directly with Benjamin about columbarium niches, ancestral tablets, funeral arrangements and wills.',
              '以清晰、尊重的方式，为您讲解新加坡的身后事安排与生命规划。福位、神主牌、殡葬安排与遗嘱，都可以直接与潘国雄商量。'), L)),
        ''.join('<div><b>%s</b><span>%s</span></div>' % (E(t(a, L)), E(t(b, L))) for a, b in facts), E(t(W['independent'], L)))
    svcs = '<section class="sec sec-white"><div class="wrap">%s%s</div></section>' % (
        title_lines(T('Services', '服务'), T('What Benjamin can help with', 'Benjamin 能协助的事项'), L),
        ''.join(zz_row(s, L, i) for i, s in enumerate(SERVICES)) + nb_feature(L))
    mood = '<section class="sec sec-cream gal"><div class="wrap">%s</div>%s<div class="wrap" style="margin-top:22px">%s</div></section>' % (
        title_lines(T('A place of peace', '安宁之所'), T('Calm, dignified and close to family', '宁静、庄重，离家人更近'), L,
                    T('Choosing a resting place is a family decision. Benjamin helps you see the options clearly before you decide.', '选择安息之所是全家人的决定。Benjamin 帮您在决定前把选择看清楚。')),
        glide(MOOD_KEYS[:9], L), pending_box([CONFIRM[6]], L))
    meet = ('<section class="sec sec-white meet"><div class="wrap split"><figure class="portrait">%s</figure><div><span class="eyebrow">%s</span><h2>%s</h2><p>%s</p><p>%s</p>'
            '<div class="cta-row" style="margin-top:26px"><a class="btn btn-outline" href="about-benjamin-poon/">%s</a>%s</div></div></div></section>') % (
        img('portrait', L), E(t(T('Meet Benjamin', '认识潘国雄'), L)), E(t(T('A personal guide, from first question to final arrangement', '从第一个问题到最后安排，全程亲自陪伴'), L)),
        E(t(T('Benjamin Poon (潘国雄) helps Singapore families compare memorial options at Nirvana Memorial Garden, Lin San Temple and Thian Leng, and plan ahead with wills.',
              '潘国雄协助新加坡家庭比较富贵山庄、灵山寺与天灵总道堂的身后事选择，并提前做好遗嘱规划。'), L)),
        E(t(T('He explains things plainly in English or Chinese, arranges viewings, and lets your family decide at its own pace.',
              '他以中文或英文清楚说明，安排参观，让家人按自己的步调做决定。'), L)),
        E(t(T('About Benjamin', '关于潘国雄'), L)), wa_btn(W['wa_home'], L))
    venues = '<section class="sec sec-cream"><div class="wrap">%s<div class="pcards three">%s</div></div></section>' % (
        title_lines(T('Locations', '地点'), T('Three places families ask about', '家庭常询问的三个地点'), L,
                    T('Benjamin can explain the options and arrange a viewing at each.', 'Benjamin 可说明各处的选择，并安排参观。')),
        ''.join(venue_card(v, L) for v in LOCATIONS))
    steps = '<section class="sec sec-white"><div class="wrap">%s<ol class="steps">%s</ol><div class="cta-row center" style="margin-top:34px">%s</div></div></section>' % (
        title_lines(T('How it works', '咨询流程'), T('How I can help', '我如何协助您'), L),
        ''.join('<li><b>%s</b><span>%s</span></li>' % (E(t(a, L)), E(t(b, L))) for a, b in STEPS), wa_btn(W['wa_home'], L))
    trust = '<section class="sec sec-cream gal"><div class="wrap">%s</div>%s<div class="wrap" style="margin-top:22px">%s</div></section>' % (
        title_lines(T('Recognition', '肯定'), T('Awards from Advance Planners (APG)', 'Advance Planners（APG）颁发的奖项'), L,
                    T('Benjamin joined in late 2025 and has been named in these APG sales awards.', 'Benjamin 于 2025 年底加入，并获得以下 APG 销售奖项。')),
        awards_html(L), pending_box([CONFIRM[5]], L))
    guides = '<section class="sec sec-white"><div class="wrap">%s<div class="acards">%s</div><p class="center" style="margin-top:34px"><a class="btn btn-outline" href="guides/">%s</a></p></div></section>' % (
        title_lines(T('Guides', '指南'), T('Plain answers before you decide', '做决定前的实用解答'), L),
        ''.join(guide_card(g, L) for g in GUIDES[:3]), E(t(T('All guides', '全部指南'), L)))
    faq = '<section class="sec sec-cream"><div class="wrap">%s<div class="faq-wrap">%s</div></div></section>' % (
        title_lines(T('FAQ', '常见问题'), T('Good to know', '您可能想知道'), L), faq_html(FAQ_HOME, L).replace('<h2>%s</h2>' % E(t(W['faq'], L)), '', 1))
    return hero + intro + svcs + mood + meet + venues + steps + trust + guides + faq


def about_body(L):
    p = [
        T('Benjamin Poon (潘国雄) is a Service Advisor and Life Managing Director in Singapore. He represents Nirvana Singapore (富贵山庄) and helps families look into columbarium niches, ancestral tablets, funeral arrangements and will planning.',
          '潘国雄（Benjamin Poon）是新加坡的生命经理师，代表富贵山庄（Nirvana Singapore），协助家庭了解福位、神主牌、殡葬安排与遗嘱规划。'),
        T('He joined in late 2025. He speaks English and Chinese, and he prefers to explain options calmly so that families can decide together, without pressure.',
          '他于 2025 年底加入，能说中文和英文。他习惯平和地说明各种选择，让家人可以一起商量、从容决定。'),
        T('Benjamin works with three venues: <a href="locations/nirvana-memorial-garden/">Nirvana Memorial Garden</a> on Old Choa Chu Kang Road, <a href="locations/lin-san-temple/">Lin San Temple</a> in Geylang and <a href="locations/thian-leng-temple/">Thian Leng Chong Toh Tong</a> on Changi Road.',
          'Benjamin 主要协助三个地点：旧蔡厝港路的<a href="locations/nirvana-memorial-garden/">富贵山庄</a>、芽笼的<a href="locations/lin-san-temple/">灵山寺</a>，以及樟宜路的<a href="locations/thian-leng-temple/">天灵总道堂</a>。'),
        T('For will planning he works with Advance Planners as a certified will planner. He gives general information and helps you prepare; questions that need legal advice go to a qualified lawyer. See <a href="services/will-planning/">Will planning</a>.',
          '在遗嘱规划方面，他以认证遗嘱规划师身份与 Advance Planners 合作。他提供一般资讯并协助您准备；需要法律意见的问题，会建议您咨询合格律师。详见<a href="services/will-planning/">遗嘱规划</a>。'),
    ]
    facts = [
        (T('Name', '姓名'), T('Benjamin Poon (潘国雄)', '潘国雄（Benjamin Poon）')),
        (T('Role', '职务'), ROLE),
        (T('Affiliation', '所属'), T('Represents Nirvana Singapore; Advance Planners (APG)', '代表富贵山庄（Nirvana Singapore）；Advance Planners（APG）')),
        (T('Languages', '语言'), T('English, Chinese', '中文、英文')),
        (T('WhatsApp / phone', 'WhatsApp / 电话'), T(TEL_SHOW, TEL_SHOW)),
        (T('Email', '电邮'), T(EMAIL, EMAIL)),
    ]
    info = '<div class="info">%s</div>' % ''.join('<div><b>%s</b><span>%s</span></div>' % (E(t(a, L)), E(t(b, L))) for a, b in facts)
    body = '<div class="layout"><div class="prose"><div class="answer">%s</div>%s%s<h2>%s</h2>%s<p class="notice">%s</p>%s</div>%s</div>' % (
        rich(t(p[0], L)), ''.join('<p>%s</p>' % rich(t(x, L)) for x in p[1:]), info,
        E(t(T('Recognition', '获奖'), L)), awards_html(L), E(t(W['independent'], L)), pending_box(CONFIRM[:5], L),
        aside(L, T('Hello Benjamin, I read your About page and would like to talk to you.', '您好 Benjamin，我看了您的个人介绍，想与您聊聊。')))
    return '<section class="sec"><div class="wrap">%s</div></section>' % body


def service_body(s, L):
    body = '<div class="layout"><div class="prose"><div class="answer">%s</div>%s%s<div class="cta-row" style="margin:28px 0">%s</div>%s</div>%s</div>' % (
        rich(t(s['answer'], L)), inline_fig(SVC_PHOTO[s['slug']], L) + sections_html(s['sections'], L), pending_box(s.get('pending'), L), wa_btn(s['wa'], L), faq_html(s['faqs'], L), aside(L, s['wa']))
    return '<section class="sec"><div class="wrap">%s</div></section>%s' % (body, related_html(s.get('related'), L))


def inline_fig(k, L):
    x = PX.get(k, {})
    return '<figure class="inline">%s<figcaption>%s</figcaption></figure>' % (img(k, L), E(x.get('credit', '')))


def services_hub(L):
    hub = getattr(SV, 'HUB', {})
    intro = '<div class="prose">%s</div>' % ''.join('<p>%s</p>' % rich(t(x, L)) for x in ([hub['intro']] if hub.get('intro') else []))
    return '<section class="sec"><div class="wrap">%s<div class="pcards" style="margin-top:24px">%s</div><div class="prose" style="margin-top:48px">%s</div></div></section>' % (
        intro, ''.join(svc_card(s, L, i) for i, s in enumerate(SERVICES)) + '</div><div style="margin-top:48px">' + nb_feature(L), sections_html(hub.get('sections', []), L))


def location_body(v, L):
    addr = v['address'] if L == 'en' else (v.get('address_zh') or v['address'])
    rows = [(W['address'], E(addr))]
    if v.get('official_url'):
        rows.append((W['official'], '<a href="%s" target="_blank" rel="noopener">%s</a>' % (E(v['official_url']), E(re.sub(r'^https?://(www\.)?|/$', '', v['official_url'])))))
    rows.append((W['map'], '<a href="https://www.google.com/maps/search/?api=1&amp;query=%s" target="_blank" rel="noopener">%s</a>' % (quote(v['map_q']), E(t(W['open_map'], L)))))
    if v.get('nearby'):
        rows.append((T('Getting there', '交通'), rich(t(v['nearby'], L))))
    info = '<div class="info">%s</div>' % ''.join('<div><b>%s</b><span>%s</span></div>' % (E(t(a, L)), b) for a, b in rows)
    body = '<div class="layout"><div class="prose"><div class="answer">%s</div>%s<p class="notice">%s</p>%s%s<div class="cta-row" style="margin:28px 0">%s</div>%s</div>%s</div>' % (
        rich(t(v['answer'], L)), info, E(t(W['independent'], L)), sections_html(v['sections'], L), pending_box(v.get('pending'), L),
        wa_btn(v['wa'], L), faq_html(v['faqs'], L), aside(L, v['wa']))
    return '<section class="sec"><div class="wrap">%s</div></section>%s' % (body, related_html(v.get('related'), L))


def locations_hub(L):
    hub = getattr(LO, 'HUB', {})
    parts = ['<p>%s</p>' % rich(t(hub['intro'], L))] if hub.get('intro') else []
    if hub.get('table'):
        parts.append(sections_html([{'h': T('The three venues at a glance', '三个地点一览'), 'table': hub['table']}], L))
    return '<section class="sec"><div class="wrap"><div class="pcards three">%s</div><div class="prose" style="margin-top:48px">%s<p class="notice">%s</p></div></div></section>' % (
        ''.join(venue_card(v, L) for v in LOCATIONS), ''.join(parts), E(t(W['independent'], L)))


def guide_body(g, L):
    by = '<div class="byline">%s<span>%s · %s %s · %d %s</span></div>' % (
        img('face', L), E(t(W['by'], L)), E(t(W['updated'], L)), g.get('date', UPDATED), g.get('read_min', 5), E(t(W['min'], L)))
    body = '<div class="layout"><article class="prose">%s<div class="answer">%s</div>%s%s<div class="cta-row" style="margin:28px 0">%s</div>%s</article>%s</div>' % (
        by, rich(t(g['answer'], L)), sections_html(g['sections'], L), pending_box(g.get('pending'), L), wa_btn(g['wa'], L), faq_html(g['faqs'], L), aside(L, g['wa']))
    rel = list(g.get('related') or [])
    if g.get('service') and g['service'] not in rel:
        rel.insert(0, g['service'])
    return '<section class="sec"><div class="wrap">%s</div></section>%s' % (body, related_html(rel[:3], L))


def contact_body(L):
    msg = T('Hello Benjamin, I found your contact page and would like to ask about your services.', '您好 Benjamin，我在您的联系页面看到资料，想询问您的服务。')
    cards = [
        (SVG['wa'], T('WhatsApp', 'WhatsApp'), T('Fastest. Send a short message and Benjamin will reply.', '最快捷。发一条简短讯息，Benjamin 会回复您。'), wa_btn(msg, L, T('Open WhatsApp', '打开 WhatsApp'))),
        (SVG['phone'], T('Call', '电话'), T(TEL_SHOW, TEL_SHOW), '<a class="btn btn-line" href="tel:%s">%s</a>' % (TEL, E(t(T('Call now', '立即致电'), L)))),
        (SVG['mail'], T('Email', '电邮'), T(EMAIL, EMAIL), '<a class="btn btn-line" href="mailto:%s">%s</a>' % (EMAIL, E(t(T('Send email', '发送电邮'), L)))),
    ]
    grid = '<div class="ccards">%s</div>' % ''.join('<div class="ccard"><div class="ico">%s</div><h3>%s</h3><p>%s</p>%s</div>' % (i, E(t(a, L)), E(t(b, L)), c) for i, a, b, c in cards)
    tips = [T('What you are looking into (niche, ancestral tablet, funeral arrangement or will).', '您想了解的事项（福位、神主牌、殡葬安排或遗嘱）。'),
            T('Which venue, if you already have one in mind.', '如已有心仪的地点，请告知。'),
            T('Whether you prefer English or Chinese, and a good time to talk.', '您希望用中文还是英文沟通，以及方便的时间。')]
    note = T('Please do not send medical or other sensitive personal details by WhatsApp. Benjamin will ask only what he needs.',
             '请勿通过 WhatsApp 发送医疗或其他敏感个人资料。Benjamin 只会询问必要的资料。')
    return '<section class="sec"><div class="wrap">%s<div class="prose" style="margin-top:40px"><h2>%s</h2><ul>%s</ul><p class="notice">%s</p><p class="notice">%s</p></div></div></section>' % (
        grid, E(t(T('Helpful to mention', '联系时可告诉 Benjamin'), L)), ''.join('<li>%s</li>' % E(t(x, L)) for x in tips), E(t(note, L)), E(t(W['independent'], L)))


def privacy_body(L):
    if L == 'zh':
        paras = ['本隐私政策说明潘国雄（Benjamin Poon）个人网站如何依据新加坡《2012 年个人资料保护法》（PDPA）处理个人资料。',
                 '<strong>我们收集什么：</strong>本网站没有表格。只有当您通过 WhatsApp、电话或电邮联系 Benjamin 时，他才会收到您提供的资料（例如姓名、电话号码与查询内容）。',
                 '<strong>用途：</strong>仅用于回复您的查询、提供您要求的资讯与安排参观或咨询。不会出售或出租您的资料。',
                 '<strong>点击记录：</strong>网站可能记录 WhatsApp 按钮的点击次数与页面浏览量（不含姓名或讯息内容），以了解哪些页面有帮助。点击不代表已发送讯息。',
                 '<strong>第三方：</strong>WhatsApp、Google 地图与字体服务由第三方提供，适用其各自的隐私政策。',
                 '<strong>查阅与更正：</strong>如需查阅、更正或删除您的资料，或撤回同意，请电邮 <a href="mailto:%s">%s</a>。' % (EMAIL, EMAIL),
                 '最后更新：2026 年 10 月 22 日。']
    else:
        paras = ['This policy explains how Benjamin Poon\'s personal website handles personal data under Singapore\'s Personal Data Protection Act 2012 (PDPA).',
                 '<strong>What is collected:</strong> the site has no forms. Benjamin only receives what you choose to send when you WhatsApp, call or email him (for example your name, number and question).',
                 '<strong>How it is used:</strong> only to answer your enquiry, send the information you asked for and arrange a viewing or consultation. Your details are never sold or rented.',
                 '<strong>Click counts:</strong> the site may count page views and taps on WhatsApp buttons (no names or message content) to learn which pages help. A tap does not mean a message was sent.',
                 '<strong>Third parties:</strong> WhatsApp, Google Maps and font services are run by third parties under their own privacy policies.',
                 '<strong>Access and correction:</strong> to see, correct or delete your data, or withdraw consent, email <a href="mailto:%s">%s</a>.' % (EMAIL, EMAIL),
                 'Last updated 22 October 2026.']
    return '<section class="sec"><div class="wrap prose">%s</div></section>' % ''.join('<p>%s</p>' % x for x in paras)


def disclaimer_body(L):
    if L == 'zh':
        paras = [E(t(W['independent'], L)),
                 '本网站内容仅供一般参考，并非法律、财务或宗教意见。有关产品、价格、供应情况及条款，以相关运营方当时提供的正式资料为准。',
                 '遗嘱相关页面只提供一般资讯。如涉及个人情况、资产在海外、家庭关系复杂或其他特殊情况，请咨询合格律师。',
                 '第三方网站链接仅为方便读者，不代表认可其内容。所列名称与商标属于其各自拥有者。']
    else:
        paras = [E(t(W['independent'], L)),
                 'The content on this site is general information, not legal, financial or religious advice. Products, prices, availability and terms are as set by the relevant operator at the time; Benjamin will share the current official details.',
                 'Will-related pages give general information only. For your own situation, assets overseas, complex family arrangements or anything unusual, please see a qualified lawyer.',
                 'Links to other websites are for convenience and do not mean endorsement. Names and trademarks belong to their owners.']
    used, seen = [], set()
    for k in PX:
        if k != 'venue-nirvana-alt' and PX[k].get('source_page') and (PX[k]['source_page'], PX[k]['credit']) not in seen:
            seen.add((PX[k]['source_page'], PX[k]['credit']))
            used.append(k)
    credits = '<h2>%s</h2><p>%s</p><ul>%s</ul>' % (E(t(T('Photo credits', '图片来源'), L)),
        E(t(T('Some photos are illustrative stock images and do not show the named venue.', '部分图片为示意图库照片，并非所提地点的实景。'), L)),
        ''.join('<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (E(PX[k]['source_page']), E(PX[k]['credit'])) for k in used))
    return '<section class="sec"><div class="wrap prose">%s%s</div></section>' % (''.join('<p>%s</p>' % x for x in paras), credits)


# ------------------------------------------------------------------------------------------------
# Pages
# ------------------------------------------------------------------------------------------------
NB_PATH = 'nirvana-products-services/'
NB_SRC = 'https://www.flipsnack.com/nirvanasg/nirvana-booklet-25.html'
NB_JUMP = [('suites', T('Columbarium', '福殿')), ('tablets', T('Ancestral tablets', '神主牌')), ('ceremonies', T('Prayer ceremonies', '法会')),
           ('funeral', T('Funeral services', '殡仪服务')), ('freccia', T('FRECCIA hearse', 'FRECCIA 灵车')), ('facilities', T('Facilities', '设施')),
           ('why', T('Why Nirvana', '为何选择')), ('trust', T('Trust fund', '信托基金')), ('visit', T('Visiting', '交通'))]
NB_SUITES = [('nb-family-suites', T('Family Suites', '家庭骨灰福殿'), T('Family columbarium suites in white, with a crystal chandelier and seating for visits.', '家庭骨灰福殿，白色装潢配水晶吊灯，设有座椅方便探望。')),
             ('nb-freethinker-suites', T('Free Thinker Suites', '无宗教骨灰福殿'), T('Suites for families who prefer a non-religious setting, with softly lit walls of round niches.', '适合无宗教信仰家庭的福殿，柔光圆形福位墙。')),
             ('nb-modern-suites', T('Modern Suites', '现代化骨灰福殿'), T('Gold walls with blue-and-white porcelain-style niches and a seating area for visits.', '金色墙面配青花瓷风格福位，设有座椅方便家人探望。')),
             ('nb-royal-suite', T('Royal Suite', '帝王阁'), T('Warm gold niche walls, a timber ceiling and a lounge with sofas and a marble table.', '金色福位墙、木质天花，配沙发与大理石茶几的休息区。'))]
NB_WHY = [(T('Excellent fengshui', '卓越风水'), T('Faces southeast in Choa Chu Kang, on what Nirvana describes as a rare "Toad\'s Lair" formation, a symbol of prosperity.', '坐落于蔡厝港，坐西北向东南，富贵山庄称之为罕见的"蟾蜍穴"格局，象征财富与繁荣。')),
          (T('Exquisite design', '精致设计'), T('Each niche is designed with fengshui principles in mind, for a harmonious resting place.', '福位设计遵循风水原理，打造和谐吉祥的安息之所。')),
          (T('Distinguished environment', '庄重宁静'), T('Peaceful, carefully designed surroundings that feel calm and dignified.', '环境宁静庄严，设计细致，氛围安宁和谐。')),
          (T('Open all year', '全年开放'), T('Open every day, including weekends and public holidays, with longer hours on special occasions.', '全年开放，包括周末与公共假期，特别节日延长开放时间。')),
          (T('Interest-free instalments', '零利息分期'), T('Interest-free instalment plans so families can spread the cost.', '提供零利息分期付款计划，减轻一次性负担。')),
          (T('24-hour security', '24 小时保安'), T('Guarded around the clock, so memorials are always cared for.', '全天候保安，让先人居所时刻受到守护。')),
          (T('One-time maintenance fee', '一次性维护费'), T('A one-time, perpetual maintenance fee for niches and tablets, with no yearly bills.', '福位与神主牌只需缴付一次性维护费。')),
          (T('99-year lease to 2098', '99 年地契至 2098 年'), T('The land lease was extended in 2016 from 2029 to 2098.', '地契于 2016 年由 2029 年延长至 2098 年。'))]
NB_MILES = [('2009', T('Nirvana Memorial Garden Singapore starts operating (January).', '新加坡富贵山庄正式运营（1 月）。')),
            ('2012', T('Nirvana Trust Fund set up to protect customers\' interests (August).', '成立富贵信托基金，保障客户权益（8 月）。')),
            ('2015', T('Excellence Brand Award (Brands Entrepreneurs\' Alliance) and The Hoffen Award (One Asia Awards 2015).', '荣获新加坡品牌企业联盟"卓越品牌奖"及 One Asia Awards 2015 "Hoffen 大奖"。')),
            ('2016', T('99-year land lease extended from 2029 to 2098 (June).', '土地地契由 2029 年延长至 2098 年（6 月）。')),
            ('2017', T('Funeral service packages launched (April).', '开始提供殡仪服务配套（4 月）。')),
            ('2018', T('Named "Largest Bereavement Company in Singapore" by the Singapore Book of Records (April).', '获新加坡记录大全颁发"新加坡最大殡葬企业"称号（4 月）。')),
            ('2020', T('Journey With Love launched: a care service for the departed by an all-female team (October).', '推出"爱。相随"，由全女性团队提供礼体护理服务（10 月）。')),
            ('2021', T('Donation to the Singapore Red Cross at its first virtual concert (January).', '于首场虚拟音乐会向新加坡红十字会捐款（1 月）。')),
            ('2022', T('FRECCIA custom hearse launched (January).', '推出 FRECCIA 定制灵车（1 月）。')),
            ('2023', T('Donation to the Singapore Red Cross for Pakistan flood relief (February).', '向新加坡红十字会捐款，支援巴基斯坦洪灾救援（2 月）。'))]
NB_FAQ = [
    (T('Is this the official Nirvana website?', '这是富贵山庄的官方网站吗？'),
     T('No. This page is a general overview prepared by Benjamin Poon from Nirvana Memorial Garden\'s 2025 booklet. For official details see nirvana.com.sg, or ask Benjamin to check anything for you.',
       '不是。本页由潘国雄根据富贵山庄 2025 年宣传册整理，仅作一般介绍。官方资料请参阅 nirvana.com.sg，或请 Benjamin 为您查证。')),
    (T('Are prices shown here?', '本页有价格吗？'),
     T('No. The booklet does not list prices, and prices depend on the suite, the location of the niche and current promotions. WhatsApp Benjamin for current options.',
       '没有。宣传册没有列出价格，价格视福殿类型、福位位置及当期优惠而定。请 WhatsApp Benjamin 了解最新选择。')),
    (T('Can Benjamin arrange a viewing?', 'Benjamin 可以安排参观吗？'),
     T('Yes. He can show you the suites, the tablet halls and the facilities at 950 Old Choa Chu Kang Road, in English or Chinese.',
       '可以。他可带您参观旧蔡厝港路 950 号的福殿、神主牌区与设施，中英文皆可。')),
]


def nb_zz(key, eb, h, paras, L, rev=False, link=None, extra=''):
    btn = '<a class="btn btn-outline" href="%s">%s</a>' % (link[0], E(t(link[1], L))) if link else ''
    return ('<article class="zz%s"><figure>%s</figure><div class="zz-text"><span class="eyebrow">%s</span><h3>%s</h3>%s%s<div class="cta-row">%s%s</div></div></article>') % (
        ' rev' if rev else '', img(key, L), E(t(eb, L)), E(t(h, L)), ''.join('<p>%s</p>' % E(t(p, L)) for p in paras), extra, btn,
        wa_btn(T('Hello Benjamin, I read your Nirvana products page and would like to know more about %s.' % h['en'], '您好 Benjamin，我看了您的富贵山庄产品介绍，想了解%s。' % h['zh']), L, cls='btn btn-wa btn-sm'))


FB_BASE = 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@45664d3/site-assets/benjamin-poon/booklet/pages/'


def nb_flipbook(L):
    pages = ''.join('<div class="fb-page"><img src="%sp%02d.webp" alt="%s %d" width="900" height="1273"%s></div>' % (
        FB_BASE, i, E(t(T('Nirvana booklet 2025, page', '富贵山庄 2025 宣传册，第'), L)), i, '' if i <= 3 else ' loading="lazy" decoding="async"') for i in range(1, 33))
    return ('<section class="sec sec-cream fbsec"><div class="wrap"><div class="tl"><span class="eyebrow-c">%s</span><h2>%s</h2><p>%s</p></div>'
            '<div class="fb-wrap"><div id="flipbook">%s</div></div>'
            '<div class="fb-ctl"><button type="button" id="fb-prev" aria-label="%s">&larr;</button><span id="fb-count">1 / 32</span><button type="button" id="fb-next" aria-label="%s">&rarr;</button></div>'
            '<div class="cta-row center" style="margin-top:26px">%s<a class="btn btn-outline" href="%s" target="_blank" rel="noopener">%s</a></div></div></section>') % (
        E(t(T('Nirvana booklet 2025', '富贵山庄 2025 宣传册'), L)), E(t(T('Flip through the booklet', '翻阅宣传册'), L)),
        E(t(T('Tap or drag the corner of a page to turn it. Benjamin can explain anything inside, in English or Chinese.', '点击或拖动页角即可翻页。册内任何内容，Benjamin 都可以中英文为您讲解。'), L)),
        pages, E(t(T('Previous page', '上一页'), L)), E(t(T('Next page', '下一页'), L)),
        wa_btn(T('Hello Benjamin, I looked at the Nirvana booklet on your website and would like to know more.', '您好 Benjamin，我在您的网站看了富贵山庄宣传册，想进一步了解。'), L),
        NB_SRC, E(t(T('Open on Flipsnack', '在 Flipsnack 打开'), L)))


def nb_body(L):
    note = T('A general illustration of Nirvana Memorial Garden\'s products and services, based on Nirvana\'s 2025 booklet. Prices, availability and terms are confirmed by Nirvana at the time of purchase; Benjamin will check the details for you.',
             '本页根据富贵山庄 2025 年宣传册整理，概括介绍富贵山庄的产品与服务。价格、供应及条款以购买时富贵山庄的确认为准，Benjamin 会为您查证细节。')
    facts = [(T('Since 2009', '2009 年成立'), T('In Singapore', '在新加坡运营')), (T('Lease to 2098', '地契至 2098'), T('99-year land lease', '99 年地契')),
             (T('Open daily', '全年开放'), T('Incl. weekends & holidays', '包括周末与假期')), (T('One-time fee', '一次性维护费'), T('Trust fund protected', '信托基金保障'))]
    intro = ('<section class="sec intro"><div class="wrap narrow center"><span class="eyebrow-c">%s</span><h2 class="statement">%s</h2><p class="lead">%s</p><p class="lead">%s</p>'
             '<div class="facts">%s</div><p class="hero-note">%s</p><nav class="jump" aria-label="%s">%s</nav></div></section>') % (
        E(t(T('Rest assured · 安心托付 圆满无忧', '安心托付 圆满无忧 · Rest assured'), L)),
        E(t(T('Memorial care in Singapore since 2009', '2009 年起服务新加坡'), L)),
        E(t(T('Nirvana Memorial Garden at 950 Old Choa Chu Kang Road is part of Nirvana Asia Group, founded in Malaysia in 1990 by Tan Sri Kong Hon Kong, which describes itself as Asia\'s largest integrated bereavement care provider. It brings columbarium niches, ancestral tablets, prayer ceremonies and funeral services together in one place, under the philosophy "Caring for Life".',
              '位于旧蔡厝港路 950 号的富贵山庄，隶属 1990 年由丹斯里邝汉光在马来西亚创立、自称亚洲最大综合殡葬企业的富贵集团。福位、神主牌、法会与殡仪服务集中一处，秉持"关怀生命"的理念。'), L)),
        E(t(T('Below is an overview of each product and service. Benjamin can walk you through any of them in person, in English or Chinese.',
              '以下逐项介绍各产品与服务。Benjamin 可以中文或英文，亲自为您讲解任何一项。'), L)),
        ''.join('<div><b>%s</b><span>%s</span></div>' % (E(t(a, L)), E(t(b, L))) for a, b in facts), E(t(note, L)),
        E(t(T('On this page', '本页内容'), L)), ''.join('<a href="#%s">%s</a>' % (a, E(t(b, L))) for a, b in NB_JUMP))
    suites = '<section class="sec sec-white" id="suites"><div class="wrap">%s<div class="pcards">%s</div><div class="cta-row center" style="margin-top:34px">%s<a class="btn btn-outline" href="services/columbarium-niches/">%s</a></div></div></section>' % (
        title_lines(T('Columbarium · 福殿', '福殿 · Columbarium'), T('Honour with elegance', '典雅致敬，永恒安息'), L,
                    T('Tradition and modern design in a serene, dignified space for remembrance. Open to all, designed for comfort, built to last.', '融合传统文化与现代美学的宁静缅怀空间，开放予所有人，舒适持久。')),
        ''.join('<div class="pcard"><figure>%s</figure><div class="pc-body"><span class="tag">%s</span><h3>%s</h3><p>%s</p></div></div>' % (img(k, L, small=True), E(t(T('Suite', '福殿'), L)), E(t(h, L)), E(t(d, L))) for k, h, d in NB_SUITES),
        wa_btn(T('Hello Benjamin, I would like to know more about the columbarium suites at Nirvana.', '您好 Benjamin，我想了解富贵山庄的福殿。'), L),
        E(t(T('How niches work', '福位须知'), L)))
    rows = [
        nb_zz('nb-tablets', T('Ancestral tablets · 神主牌', '神主牌 · Ancestral tablets'), T('A modern way to honour tradition', '传承传统的现代方式'),
              [T('With families living apart, smaller homes and growing environmental concerns, keeping ancestral tablets at home is becoming less practical.', '家庭成员分居各地、居住空间有限，加上环保意识提高，在家中供奉神主牌已不再方便。'),
               T('Nirvana offers a respectful, modern alternative: tablets kept in dedicated halls, preserving tradition while honouring loved ones with dignity and care.', '富贵山庄提供庄重而现代的选择，把神主牌安奉于专属殿堂，延续传统，以尊重与关怀缅怀先人。')],
              L, link=('services/ancestral-tablets/', T('About ancestral tablets', '神主牌须知'))),
        nb_zz('nb-grand-hall', T('Major prayer ceremonies · 大型法会', '大型法会 · Prayer ceremonies'), T('Honouring traditions, uniting families', '传承传统，凝聚亲情'),
              [T('Nirvana marks Chinese festivals such as Qing Ming and Zhong Yuan with prayer ceremonies and blessings, keeping filial piety alive and families connected across generations.', '富贵山庄于清明、中元等传统节日举行祈福法会，延续孝道，让家人跨越时空心意相连。'),
               T('Many ceremonies take place in the Block B Grand Hall (大雄宝殿), with its lotus ceiling light and golden statues.', '许多法会在 B 座大雄宝殿举行，殿内有莲花吊灯与金色佛像。')],
              L, rev=True),
        nb_zz('nb-eternal-flowers', T('Ceremonial services · 山庄礼仪服务', '山庄礼仪服务 · Ceremonial services'), T('Eternal flowers and personal touches', '永生花与心意布置'),
              [T('Ceremonial services include an ling (安灵) rites, memorial engravings on tablets and eternal flower dedications.', '礼仪服务包括安灵、牌位刻字及永生花装饰等。'),
               T('Eternal flowers are fresh flowers that are carefully preserved so they keep their beauty for a long time. Families use them to decorate a niche: "always remembered, forever loved."', '永生花是经过精心加工、可长久保持美丽的鲜花。家属可用来布置福位，寄托"永远记得，永远爱着"的心意。')],
              L),
    ]
    tradition = '<section class="sec sec-cream" id="tablets"><div class="wrap">%s<div id="ceremonies"></div>%s</div></section>' % (rows[0], rows[1])
    prayer = '<section class="sec sec-cream gal" style="padding-top:0"><div class="wrap">%s</div>%s</section>' % (
        '', glide(['nb-prayer-monk', 'nb-prayer-offerings', 'nb-staff', 'nb-grand-hall'], L,
                  [T('Prayers at a tablet wall', '牌位墙前诵经祈福'), T('Zhong Yuan offering hall', '中元法会供品大厅'), T('Staff explain each option', '职员细心讲解'), T('Block B Grand Hall · 大雄宝殿', 'B 座大雄宝殿')]))
    funeral = '<section class="sec sec-white" id="funeral"><div class="wrap">%s%s%s</div></section>' % (rows[2],
        nb_zz('nb-wake', T('Funeral services · 殡仪服务', '殡仪服务 · Funeral services'), T('Complete funeral services, handled with care', '全面殡仪服务，细致周到'),
              [T('Funeral planning and coordination, embalming, encoffinment and funeral processions, with a choice of packages to suit different needs and traditions.', '服务涵盖殡仪策划与协调、防腐、入殓及出殡，并备有多款配套，适合不同需求与习俗。'),
               T('For departed women, an all-female team of embalmers, beauticians and ceremony specialists handles every step, from cleansing to make-up and dressing.', '为女性往生者，全程由全女性团队负责，包括遗体整容师、美容师及礼仪专员，从洁身、化妆到更衣。')],
              L, rev=True, link=('services/funeral-services/', T('Funeral arrangements', '殡葬安排须知'))),
        nb_zz('nb-spa', T('Journey With Love · 爱。相随', '爱。相随 · Journey With Love'), T('A signature care service for the departed', '礼体净身护理服务'),
              [T('Launched in 2020, Journey With Love is a care service for the departed delivered by professionally trained female embalmers and beauticians, using quality spa products.', '"爱。相随"于 2020 年推出，由受过专业训练的女性遗体整容师与美容师，选用优质 SPA 产品，为逝者细心护理。'),
               T('Nirvana says it leaves a comforting impression on spouses, parents and children.', '富贵山庄表示，这份尊重让配偶、父母与子女倍感安慰。')], L))
    freccia = ('<section class="sec sec-cream" id="freccia"><div class="wrap">%s</div></section>') % nb_zz(
        'nb-freccia', T('FRECCIA · 尊荣典雅', '尊荣典雅 · FRECCIA'), T('Prestigious & esteemed', '尊荣典雅的最后旅程'),
        [T('FRECCIA is Nirvana\'s luxury custom hearse, launched in 2022, for families who wish to send their loved one off in style.', 'FRECCIA 是富贵山庄于 2022 年推出的豪华定制灵车，让挚爱以体面与尊崇之姿踏上最后旅程。')],
        L, extra='<p class="notice">%s</p>' % E(t(T('Nirvana notes that the Maserati Freccia may be arranged on request, depending on availability.', '富贵山庄注明：玛莎拉蒂 Freccia 可按需求安排，视当时供应情况而定。'), L)))
    fac = '<section class="sec sec-white gal" id="facilities"><div class="wrap">%s</div>%s</section>' % (
        title_lines(T('Facilities · 设施', '设施 · Facilities'), T('Solemn, and comfortable', '庄严而舒适'), L,
                    T('The 2U Zone with a payment counter and private consultation rooms, the Level 5 lounge, the Level 9 prayer space and the Level 9 cafe.', '2U 区设有付款柜台与私人洽谈室，另有五楼休息厅、九楼祈福区及九楼咖啡厅。')),
        glide(['nb-atrium', 'nb-lounge', 'nb-fac-1', 'nb-fac-2', 'nb-fac-3', 'nb-fac-4', 'nb-facade'], L,
              [T('Skylit atrium', '天窗中庭'), T('Block B Level 5 lounge · 贵宾休息厅', 'B 座五楼贵宾休息厅'), T('Lounge area', '休息区'), T('Level 9 cafe', '九楼咖啡厅'),
               T('Private consultation room', '私人洽谈室'), T('Reception', '接待处'), T('950 Old Choa Chu Kang Road', '旧蔡厝港路 950 号')], cls='wide'))
    why = '<section class="sec sec-cream" id="why"><div class="wrap">%s<ol class="steps eight">%s</ol></div></section>' % (
        title_lines(T('Why families choose Nirvana', '为什么选择富贵山庄'), T('Eight reasons from the booklet', '宣传册列出的八大理由'), L),
        ''.join('<li><b>%s</b><span>%s</span></li>' % (E(t(a, L)), E(t(b, L))) for a, b in NB_WHY))
    trust = '<section class="sec sec-white" id="trust"><div class="wrap">%s</div></section>' % nb_zz(
        'nb-signage', T('Trust fund · 信托基金', '信托基金 · Trust fund'), T('Your maintenance fee, protected', '维护费专款专用'),
        [T('When you buy a niche or pedestal, 75% of the one-time maintenance fee goes into the Nirvana Trust Fund, and the remaining 25% is kept as current maintenance reserves.', '购买福位时，一次性维护费的 75% 拨入富贵信托基金，其余 25% 作为维修储备金。'),
         T('Precepts Trustee Limited is the appointed trustee and checks that the money is used only for its purpose. Certified accountants audit the fund\'s accounts every year.', 'Precepts Trustee Limited 为指定受托人，确保资金专款专用；注册会计师每年审计相关财务报表。')], L, rev=True)
    miles = '<section class="sec sec-cream"><div class="wrap narrow">%s<ol class="tline">%s</ol><div class="facts" style="margin-top:44px">%s</div></div></section>' % (
        title_lines(T('Milestones', '里程碑'), T('Nirvana in Singapore, 2009 to 2023', '富贵山庄在新加坡，2009 至 2023'), L),
        ''.join('<li><b>%s</b><span>%s</span></li>' % (y, E(t(x, L))) for y, x in NB_MILES),
        ''.join('<div><b>%s</b><span>%s</span></div>' % (E(t(a, L)), E(t(b, L))) for a, b in [
            (T('1990', '1990'), T('Nirvana Asia Group founded', '富贵集团成立')), (T('5 countries', '5 个国家'), T('MY · SG · ID · TH · VN', '马来西亚·新加坡·印尼·泰国·越南')),
            (T('22 branches', '22 家分行'), T('Locally and overseas', '本地及海外')), (T('16,000+', '16,000+'), T('Authorised agents', '授权代理'))]))
    bus = [('09:45', '09:15'), ('10:45', '10:15'), ('11:45', '11:15'), ('12:45*', '12:15*'), ('13:45', '13:15'), ('14:45', '14:15'), ('15:45', '15:15'), ('', '16:45')]
    visit = ('<section class="sec sec-white" id="visit"><div class="wrap split"><figure>%s</figure><div><span class="eyebrow">%s</span><h2>%s</h2>'
             '<div class="info"><div><b>%s</b><span>950 Old Choa Chu Kang Road, Singapore 699816</span></div><div><b>%s</b><span>%s</span></div><div><b>%s</b><span>%s</span></div></div>'
             '<table class="bus"><thead><tr><th>%s</th><th>%s</th></tr></thead><tbody>%s</tbody></table><p class="notice">%s</p><div class="cta-row" style="margin-top:22px">%s'
             '<a class="btn btn-outline" href="locations/nirvana-memorial-garden/">%s</a></div></div></div></section>') % (
        img('nb-facade', L), E(t(T('Visiting · 交通', '交通 · Visiting'), L)), E(t(T('Getting to Nirvana', '如何前往富贵山庄'), L)),
        E(t(W['address'], L)), E(t(T('Shuttle bus', '接驳巴士'), L)), E(t(T('Shuttle between Boon Lay MRT (Exit C) and Nirvana Block B entrance', '文礼地铁站 C 出口与富贵山庄 B 座入口之间的接驳巴士'), L)),
        E(t(T('Public bus', '公共巴士'), L)), E(t(T('SMRT 975 from Bukit Panjang Interchange / opposite Choa Chu Kang station', 'SMRT 975 号巴士（武吉班让转换站 / 蔡厝港地铁站对面）'), L)),
        E(t(T('Leaves Boon Lay MRT', '文礼地铁站开出'), L)), E(t(T('Leaves Nirvana', '富贵山庄开出'), L)),
        ''.join('<tr><td>%s</td><td>%s</td></tr>' % (a or '–', b) for a, b in bus),
        E(t(T('* Weekends and public holidays only. Timings as printed in Nirvana\'s 2025 booklet; please check before you travel, or ask Benjamin to arrange your visit.', '* 仅限周末及公共假期。时间依据富贵山庄 2025 年宣传册，出发前请再确认，或请 Benjamin 为您安排参观。'), L)),
        wa_btn(T('Hello Benjamin, I would like to arrange a viewing at Nirvana Memorial Garden.', '您好 Benjamin，我想预约参观富贵山庄。'), L), E(t(T('Location details', '地点详情'), L)))
    src = '<section class="sec sec-cream"><div class="wrap narrow">%s<div class="faq-wrap">%s</div><p class="notice" style="margin-top:28px">%s <a href="%s" target="_blank" rel="noopener">%s</a>. %s</p>%s</div></section>' % (
        title_lines(T('FAQ', '常见问题'), T('About this page', '关于本页'), L), faq_html(NB_FAQ, L).replace('<h2>%s</h2>' % E(t(W['faq'], L)), '', 1),
        E(t(T('Source: Nirvana Memorial Garden booklet 2025,', '资料来源：富贵山庄 2025 年宣传册，'), L)), NB_SRC, E(t(T('view the original booklet', '查看原版宣传册'), L)), E(t(W['independent'], L)),
        pending_box([T('Nirvana / Advance Planners OK for Benjamin to reuse the booklet photos and wording on his personal website.', '富贵山庄 / Advance Planners 是否同意 Benjamin 在个人网站使用宣传册的照片与文字。')], L))
    text = intro + suites + tradition + prayer + funeral + freccia + fac + why + trust + miles + visit + src
    return nb_flipbook(L) + ('<details class="nbtext"><summary><span>%s</span></summary>%s</details>' % (
        E(t(T('Read the booklet as text (English & 中文)', '阅读宣传册文字版（中文 & English）'), L)), text))


PAGES = {}


def page(L, path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, kind='website', photo=None):
    PAGES[(L, path)] = dict(title=t(title, L), desc=t(desc, L), h1=t(h1, L), body=body, crumbs=crumbs, lede=t(lede, L), schema=schema or [], hero=hero, cta=cta, kind=kind,
                            photo=photo or path_photo(path) if path else None)


def person(L):
    return {'@type': 'Person', '@id': SITE + '#benjamin', 'name': NAME, 'alternateName': NAME_ZH, 'jobTitle': t(T('Service Advisor, Life Managing Director', '生命经理师'), L),
            'telephone': TEL, 'email': EMAIL, 'image': IMG + PHOTOS['portrait'][0], 'url': SITE + PFX[L] + 'about-benjamin-poon/',
            'affiliation': [{'@type': 'Organization', 'name': 'Nirvana Singapore', 'alternateName': '富貴山庄', 'url': NIRVANA},
                            {'@type': 'Organization', 'name': 'Advance Planners'}],
            'knowsLanguage': ['en', 'zh'], 'areaServed': {'@type': 'Country', 'name': 'Singapore'},
            'award': ['APG September 2025 Award', 'APG October 2025 Sales Award', 'APG May 2026 Sales Award']}


def build_pages():
    for L in LANGS:
        nav = dict(W['nav'])
        page(L, '', T('Benjamin Poon 潘国雄 | Niches, Tablets & Wills Singapore', '潘国雄 Benjamin Poon | 新加坡福位、神主牌与遗嘱规划'),
             T('Benjamin Poon (潘国雄), Nirvana Singapore: columbarium niches, ancestral tablets, funeral arrangements and will planning. WhatsApp +65 8932 9933.',
               '潘国雄（Benjamin Poon），富贵山庄生命经理师：福位、骨灰位、神主牌、殡葬安排与遗嘱规划。中英文服务，WhatsApp +65 8932 9933。'),
             'Benjamin Poon', home_body(L), hero=False, schema=[faq_schema(FAQ_HOME, L)])
        page(L, 'about-benjamin-poon/', T('About Benjamin Poon (潘国雄) | Nirvana Singapore', '关于潘国雄 Benjamin Poon | 生命经理师'),
             T('Benjamin Poon (潘国雄) is a Service Advisor and Life Managing Director representing Nirvana Singapore. Niches, ancestral tablets, funerals and will planning, in English and Chinese.',
               '潘国雄（Benjamin Poon），代表富贵山庄的生命经理师，以中英文协助福位、神主牌、殡葬与遗嘱规划。'),
             T('About Benjamin Poon', '关于潘国雄'), about_body(L), crumbs=[('about-benjamin-poon/', nav['about-benjamin-poon/'])],
             lede=T('Service Advisor and Life Managing Director, Singapore. English and Chinese.', '新加坡生命经理师，中英文服务。'), schema=[])
        page(L, 'services/', T('Memorial & Will Planning Services | Benjamin Poon', '福位、神主牌、殡葬与遗嘱服务 | 潘国雄'),
             T('Columbarium niches, ancestral tablets, funeral services and will planning in Singapore, explained by Benjamin Poon (潘国雄). WhatsApp +65 8932 9933.',
               '潘国雄为您讲解新加坡福位、神主牌、殡葬服务与遗嘱规划。WhatsApp +65 8932 9933。'),
             T('Services', '服务'), services_hub(L), crumbs=[('services/', nav['services/'])],
             lede=T('Four areas, each with its own page of details and answers.', '四个方面，每项都有详细说明与解答。'))
        for s in SERVICES:
            path = 'services/%s/' % s['slug']
            page(L, path, s['title'], s['desc'], s['h1'], service_body(s, L), crumbs=[('services/', nav['services/']), (path, s['card'])], lede=s['lede'],
                 schema=[{'@type': 'Service', 'name': t(s['card'], L), 'serviceType': t(s['card'], L), 'provider': {'@id': SITE + '#benjamin'},
                          'areaServed': {'@type': 'Country', 'name': 'Singapore'}, 'url': SITE + PFX[L] + path, 'description': strip_tags(t(s['answer'], L))},
                         faq_schema(s['faqs'], L)])
        page(L, NB_PATH, T('Nirvana Memorial Garden Products & Services | Benjamin Poon', '富贵山庄产品与服务介绍 | 潘国雄'),
             T('A general guide to Nirvana Memorial Garden Singapore: columbarium suites, ancestral tablets, prayer ceremonies, funeral services, FRECCIA hearse, facilities and trust fund.',
               '富贵山庄（新加坡）产品与服务总览：福殿、神主牌、法会、殡仪服务、FRECCIA 灵车、设施与信托基金。'),
             T('Nirvana Memorial Garden: products & services', '富贵山庄：产品与服务'), nb_body(L), crumbs=[(NB_PATH, T('Nirvana products & services', '富贵山庄产品与服务'))],
             lede=T('A general illustration of everything Nirvana offers, from columbarium suites to funeral services, explained by Benjamin Poon.', '从福殿到殡仪服务，潘国雄为您概括介绍富贵山庄的全部产品与服务。'),
             photo='nb-facade', schema=[faq_schema(NB_FAQ, L)])
        page(L, 'locations/', T('Nirvana, Lin San & Thian Leng Niches | Benjamin Poon', '富贵山庄、灵山寺、天灵总道堂福位 | 潘国雄'),
             T('Three venues Benjamin Poon can help with: Nirvana Memorial Garden (Old Choa Chu Kang Rd), Lin San Temple (Geylang) and Thian Leng (Changi Rd).',
               '潘国雄协助的三个地点：旧蔡厝港路富贵山庄、芽笼灵山寺、樟宜路天灵总道堂。'),
             T('Locations', '地点'), locations_hub(L), crumbs=[('locations/', nav['locations/'])],
             lede=T('Three venues, each with its own page.', '三个地点，各有详细页面。'))
        for v in LOCATIONS:
            path = 'locations/%s/' % v['slug']
            page(L, path, v['title'], v['desc'], v['h1'], location_body(v, L), crumbs=[('locations/', nav['locations/']), (path, v['name'])], lede=v['lede'],
                 schema=[{'@type': 'Place', 'name': t(v['name'], L), 'address': v['address'], 'hasMap': 'https://www.google.com/maps/search/?api=1&query=' + quote(v['map_q'])},
                         faq_schema(v['faqs'], L)])
        page(L, 'guides/', T('Memorial & Will Planning Guides Singapore | Benjamin Poon', '新加坡身后事与遗嘱规划指南 | 潘国雄'),
             T('Plain guides on columbarium niches, ancestral tablets, funeral arrangements and wills in Singapore, by Benjamin Poon (潘国雄).',
               '潘国雄撰写的实用指南：新加坡福位、神主牌、殡葬安排与遗嘱。'),
             T('Guides', '指南'), '<section class="sec"><div class="wrap"><div class="acards">%s</div></div></section>' % ''.join(guide_card(g, L) for g in GUIDES),
             crumbs=[('guides/', nav['guides/'])], lede=T('Plain answers to the questions families ask most.', '家庭最常问的问题，浅白解答。'))
        for g in GUIDES:
            path = 'guides/%s/' % g['slug']
            page(L, path, g['title'], g['desc'], g['h1'], guide_body(g, L), crumbs=[('guides/', nav['guides/']), (path, g['h1'])], lede=g['lede'], kind='article',
                 schema=[{'@type': 'Article', 'headline': t(g['h1'], L), 'description': t(g['desc'], L), 'inLanguage': LANG_ATTR[L], 'image': IMG + 'og-benjamin-poon-4.jpg',
                          'datePublished': g.get('date', UPDATED), 'dateModified': g.get('date', UPDATED), 'author': {'@id': SITE + '#benjamin'},
                          'mainEntityOfPage': SITE + PFX[L] + path}, faq_schema(g['faqs'], L)])
        page(L, 'contact/', T('Contact Benjamin Poon | WhatsApp +65 8932 9933', '联系潘国雄 | WhatsApp +65 8932 9933'),
             T('WhatsApp or call Benjamin Poon (潘国雄) on +65 8932 9933, or email benpoon.nirvana@gmail.com. English or Chinese.',
               'WhatsApp 或致电 +65 8932 9933 联系潘国雄，或电邮 benpoon.nirvana@gmail.com。中英文皆可。'),
             T('Contact Benjamin', '联系 Benjamin'), contact_body(L), crumbs=[('contact/', nav['contact/'])], cta=False,
             lede=T('WhatsApp is the fastest way to reach him.', 'WhatsApp 是最快的联系方式。'))
        page(L, 'privacy-policy/', T('Privacy Policy | Benjamin Poon', '隐私政策 | 潘国雄'), T('How Benjamin Poon\'s website handles personal data under Singapore\'s PDPA.', '潘国雄个人网站依据新加坡 PDPA 处理个人资料的方式。'),
             W['privacy'], privacy_body(L), crumbs=[('privacy-policy/', W['privacy'])], cta=False)
        page(L, 'disclaimer/', T('Disclaimer | Benjamin Poon', '免责声明 | 潘国雄'), T('Benjamin Poon\'s personal website: independent, general information only, not legal advice.', '潘国雄个人网站：独立运营，仅供一般参考，并非法律意见。'),
             W['disclaimer'], disclaimer_body(L), crumbs=[('disclaimer/', W['disclaimer'])], cta=False)


# ------------------------------------------------------------------------------------------------
# Render
# ------------------------------------------------------------------------------------------------
ASSET_V = hashlib.sha256(b''.join(open(os.path.join(HERE, f), 'rb').read() for f in ('bp.css', 'bp.js'))).hexdigest()[:8]


def brand_html(lpre, L):
    return '<a class="brand" href="%s" aria-label="Benjamin Poon, %s"><span class="brand-mark" aria-hidden="true">BP</span><span class="brand-name">Benjamin Poon<small>潘国雄 · %s</small></span></a>' % (
        lpre or './', E(t(W['home'], L)), E(t(T('Life Managing Director', '生命经理师'), L)))


def render(L, path, p):
    full = PFX[L] + path
    pre = '../' * full.count('/')
    lpre = pre + PFX[L]
    url = SITE + full
    share = IMG + 'og-benjamin-poon-4.jpg'

    def fix(s):
        return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), lpre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (lpre, h, ' aria-current="page"' if path.startswith(h) else '', E(t(x, L))) for h, x in W['nav'])
    langs = ''.join('<a href="%s%s%s" hreflang="%s" lang="%s"%s>%s</a>' % (pre, PFX[l], path, HREFLANG[l], LANG_ATTR[l], ' aria-current="true"' if l == L else '', LANG_LABEL[l]) for l in LANGS)
    alts = ''.join('<link rel="alternate" hreflang="%s" href="%s%s%s">\n' % (HREFLANG[l], SITE, PFX[l], path) for l in LANGS) + \
        '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE, path)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">%s</a>' % (lpre or './', E(t(W['home'], L)))] + ['<a href="%s%s">%s</a>' % (lpre, h, E(t(x, L))) for h, x in p['crumbs'][:-1]] + \
            ['<span>%s</span>' % E(t(p['crumbs'][-1][1], L))]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': t(W['home'], L), 'item': SITE + PFX[L]}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t(x, L), 'item': SITE + PFX[L] + h} for i, (h, x) in enumerate(p['crumbs'])]}
    graph = [person(L), {'@type': 'WebSite', '@id': SITE + '#website', 'url': SITE, 'name': 'Benjamin Poon 潘国雄', 'inLanguage': ['en-SG', 'zh-Hans-SG'], 'publisher': {'@id': SITE + '#benjamin'}},
             {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'], 'inLanguage': LANG_ATTR[L], 'dateModified': UPDATED,
              'about': {'@id': SITE + '#benjamin'}, 'primaryImageOfPage': share, 'isPartOf': {'@id': SITE + '#website'}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        bg = '<figure class="phero-bg" aria-hidden="true">%s</figure>' % img(p['photo'], L, eager=True) if p.get('photo') else ''
        head_hero = '<section class="phero%s">%s<div class="wrap">%s<h1>%s</h1>%s</div></section>' % (' has-bg' if bg else '', bg, crumbs_html, E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else '')
    band = ''
    if p['cta']:
        band = '<section class="sec"><div class="wrap"><div class="band"><div><h2>%s</h2><p>%s</p></div><div class="cta-row">%s</div></div></div></section>' % (
            E(t(W['band_h'], L)), E(t(W['band_p'], L)), wa_btn(W['wa_home'], L))
    body = fix(p['body'] + band)
    brand = brand_html(lpre, L)
    ftr_svc = ''.join('<li><a href="%sservices/%s/">%s</a></li>' % (lpre, s['slug'], E(t(s['card'], L))) for s in SERVICES)
    ftr_loc = ''.join('<li><a href="%slocations/%s/">%s</a></li>' % (lpre, v['slug'], E(t(v['name'], L))) for v in LOCATIONS)
    ftr_more = ''.join('<li><a href="%s%s">%s</a></li>' % (lpre, h, E(t(x, L))) for h, x in [('about-benjamin-poon/', W['nav'][0][1]), ('guides/', W['nav'][3][1]),
                                                                                        ('contact/', W['nav'][4][1]), ('privacy-policy/', W['privacy']), ('disclaimer/', W['disclaimer'])])
    title = E(p['title'])
    return f'''<!doctype html>
<html lang="{LANG_ATTR[L]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{url}">
{alts}<meta property="og:type" content="{p['kind']}">
<meta property="og:site_name" content="Benjamin Poon 潘国雄">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{share}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(t(T('Benjamin Poon (潘国雄), Service Advisor and Life Managing Director, Singapore', '潘国雄 Benjamin Poon，新加坡生命经理师'), L))}">
<meta property="og:locale" content="{OG_LOCALE[L]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{share}">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="icon" href="{pre}icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=Jost:wght@400;500;600{'&family=Noto+Serif+SC:wght@600' if L == 'zh' else ''}&display=swap">
<link rel="stylesheet" href="{pre}bp.css?v={ASSET_V}">
<script src="{pre}bp.js?v={ASSET_V}" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">{E(t(T('Skip to content', '跳到正文'), L))}</a>
<header class="hdr"><div class="wrap">
{brand}
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
<div class="lang" aria-label="Language">{langs}</div>
{wa_btn(W['wa_home'], L, W['whatsapp'], cls='btn btn-wa hdr-wa')}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">{E(t(W['menu'], L))}</button>
</div></header>
<main id="main">
{head_hero}
{body}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div>{brand}<p>{E(t(W['ftr_about'], L))}</p></div>
<div><h3>{E(t(W['nav'][1][1], L))}</h3><ul>{ftr_svc}</ul><h3 style="margin-top:18px">{E(t(W['nav'][2][1], L))}</h3><ul>{ftr_loc}</ul></div>
<div><h3>{E(t(W['explore'], L))}</h3><ul>{ftr_more}</ul></div>
<div><h3>{E(t(W['contact_h'], L))}</h3><ul>
<li><a href="{E(wa_url(W['wa_home'], L))}" target="_blank" rel="noopener" data-wa="1">WhatsApp {TEL_SHOW}</a></li>
<li><a href="tel:{TEL}">{E(t(W['call'], L))} {TEL_SHOW}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
</ul></div>
</div>
<p style="margin-top:26px;font-size:.85rem">{E(t(W['independent'], L))}</p>
<div class="ftr-legal"><span>© 2026 Benjamin Poon 潘国雄</span><span>{E(t(W['built'], L))} <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<div class="dock"><a class="dock-wa" href="{E(wa_url(W['wa_home'], L))}" target="_blank" rel="noopener" data-wa="1">{SVG['wa']}<span>WhatsApp</span></a><a class="dock-call" href="tel:{TEL}">{SVG['phone']}<span>{E(t(W['call'], L))}</span></a></div>
</body>
</html>
'''


def not_found():
    L = 'en'
    body = ('<section class="sec"><div class="wrap prose"><p>The page you were looking for has moved or does not exist. 找不到该页面。</p>'
            '<ul>%s<li><a href="zh/">中文首页</a></li></ul></div></section>') % ''.join('<li><a href="%s">%s</a></li>' % (h or './', E(t(x, L))) for h, x in [('', W['home'])] + W['nav'])
    p = dict(title='Page not found | Benjamin Poon', desc='This page could not be found.', h1='Sorry, that page is not here.', body=body,
             crumbs=None, lede='', schema=[], hero=True, cta=True, kind='website')
    out = render(L, '', p).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    out = re.sub(r'<link rel="(canonical|alternate)"[^>]*>\n', '', out)
    base = '/' if LIVE else '/preview/%s/' % SLUG
    return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|/|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), base, m.group(2) if m.group(2) != './' else ''), out)


BOTS = ['Googlebot', 'Googlebot-Image', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot',
        'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']

HTACCESS = """# Benjamin Poon ({DOMAIN}). Document root for {DOMAIN}; also served as
# pageonesingapore.com/preview/benjamin-poon/ before go-live. Overrides the parent pageonesingapore.com .htaccess.
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://{DOMAIN}/$1 [L,R=301]
ErrorDocument 404 /404.html
AddDefaultCharset UTF-8
<IfModule mod_headers.c>
SetEnvIfNoCase Host ^(www\\.)?pageonesingapore\\.com$ P1_PREVIEW=1
Header set X-Robots-Tag "noindex, nofollow" env=P1_PREVIEW
<FilesMatch "\\.(html)$">
Header set Cache-Control "max-age=3600, public"
</FilesMatch>
</IfModule>
"""


def main():
    build_pages()
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    with open(os.path.join(OUT, INDEXNOW_KEY + '.txt'), 'w') as f:
        f.write(INDEXNOW_KEY)
    for (L, path), p in PAGES.items():
        d = os.path.join(OUT, PFX[L] + path)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(render(L, path, p))
    with open(os.path.join(OUT, '404.html'), 'w') as f:
        f.write(not_found())
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write(''.join('User-agent: %s\nAllow: /\n\n' % b for b in BOTS) + 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
        for (L, path) in PAGES:
            f.write('  <url><loc>%s%s%s</loc><lastmod>%s</lastmod>%s</url>\n' % (SITE, PFX[L], path, UPDATED, ''.join(
                '<xhtml:link rel="alternate" hreflang="%s" href="%s%s%s"/>' % (HREFLANG[l], SITE, PFX[l], path) for l in LANGS) +
                '<xhtml:link rel="alternate" hreflang="x-default" href="%s%s"/>' % (SITE, path)))
        f.write('</urlset>\n')
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write('# Benjamin Poon (潘国雄), Service Advisor and Life Managing Director, Singapore\n\n'
                '> Benjamin Poon (潘国雄) is a Service Advisor and Life Managing Director (生命经理师) in Singapore who represents Nirvana Singapore (富贵山庄). '
                'He helps families with columbarium niches (福位/骨灰位), ancestral tablets (神主牌), funeral arrangements (殡葬服务) and will planning (遗嘱规划, with Advance Planners). '
                'Venues: Nirvana Memorial Garden, 950 Old Choa Chu Kang Road, Singapore 699816; Lin San Temple (灵山寺), 27 Lorong 12 Geylang, Singapore 399004; '
                'Thian Leng Chong Toh Tong (天灵总道堂), 472 Changi Road, Singapore 419890. He is named in the APG (Advance Planners) September 2025 Award, October 2025 Sales Award and May 2026 Sales Award. '
                'Languages: English and Chinese. WhatsApp or call +65 8932 9933, email %s. This is his personal website, not the official website of Nirvana (nirvana.com.sg) or any temple. '
                'Prices and availability are given by Benjamin on request from the operators; none are published here.\n\n'
                '## Pages (English; Chinese under /zh/)\n' % EMAIL)
        for (L, path), p in PAGES.items():
            if L == 'en':
                f.write('- [%s](%s%s): %s\n' % (p['title'].split(' | ')[0], SITE, path, p['desc']))
        f.write('\nLast updated 22 October 2026.\n')
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': 'Benjamin Poon 潘国雄', 'short_name': 'Benjamin Poon', 'icons': [{'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
                                                                                         {'src': IMG + 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
                   'theme_color': '#163028', 'background_color': '#f7f3eb', 'display': 'browser'}, f, ensure_ascii=False)
    with open(os.path.join(HERE, 'htaccess.txt'), 'w') as f:
        f.write(HTACCESS.replace('{DOMAIN}', DOMAIN))
    for fn in ('bp.css', 'bp.js'):
        shutil.copy(os.path.join(HERE, fn), os.path.join(OUT, fn))
    for fn in ('favicon.ico', 'icon-192.png', 'apple-touch-icon.png'):
        shutil.copy(os.path.join(HERE, 'icons', fn), os.path.join(OUT, fn))
    print('built %d pages' % len(PAGES))


if __name__ == '__main__':
    main()
