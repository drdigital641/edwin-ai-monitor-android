#!/usr/bin/env python3
"""planwithben.sg /funeral-help/ hub + area pages (EN + /zh/), Edwin 17 Nov 2026.

ONE template (this file) + ONE data config (funeral-areas.json). Add or edit an area = edit the JSON, rerun:
    python3 build_funeral_help.py <header-footer-ref-en.html> <header-footer-ref-zh.html> <out_dir>
The ref pages are the live /services/funeral-services/ pages (EN + zh), read through the Bridge, so the
header, footer and dock always match live. Output mirrors the site root (funeral-help/..., zh/funeral-help/...).
Facts: only what Benjamin/Edwin confirmed (17 Nov): 24/7 calls, respond within 1 hour (urgent), Buddhist/Taoist/
Free-thinker, "Benjamin arranges Nirvana funeral services". No prices, years, wake venues, licence claims.
"""
import html, json, os, re, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
CFG = json.load(open(os.path.join(HERE, 'funeral-areas.json'), encoding='utf-8'))
FLAGS = CFG['flags']
AREAS = CFG['areas']
VENUES = CFG['venues']
SITE = 'https://planwithben.sg/'
PHONE = '+65 8932 9933'
TODAY = CFG.get('date', '2026-11-17')
E = lambda s: html.escape(str(s), quote=True)

WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3z"/></svg>'
CALL_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>'

REVIEW = {
 'en': 'Leave us a Google review', 'zh': '在 Google 留下评价'}
REVIEW_BLOCK = '''<style>
/* Google review footer button (2026-11-13) */
.p1-foot-review{margin:16px 0 0}
.p1-foot-review a{
  display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;
  min-height:44px;min-width:44px;padding:10px 18px;
  border:1.5px solid currentColor;border-radius:999px;
  text-decoration:none!important;font-weight:700;line-height:1.25;color:inherit
}
.p1-foot-review a:hover{opacity:.88}
footer.foot .p1-foot-review{margin:12px 0 8px}
</style>
<p class="p1-foot-review"><a href="/review.html?business=benjaminpoon" target="_blank" rel="noopener">%s</a></p>
'''

# Scoped styles for the new pages only (bp.css untouched).
FH_CSS = '''<style>
/* funeral-help pages (2026-11-17) */
.fh-hero{text-align:left}.fh-hero h1,.fh-hero .lede{margin-left:0;margin-right:0}
.fh-hero .lede{max-width:640px;margin-bottom:10px}
@media (max-width:560px){.fh-hero{padding-top:28px}.fh-hero h1{font-size:2rem}.fh-hero .lede,.fh-hero .fh-now{font-size:.98rem}}
.fh-hero .fh-now{font-weight:500;color:var(--brown);margin:0 0 22px;max-width:640px}
.fh-hero .cta-row{justify-content:flex-start}
.fh-split{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:22px 0}
.fh-split div{background:var(--cream);padding:22px}
.fh-split h3{font-size:1.15rem;margin-bottom:.4em}
.fh-split p{margin:0}
.fh-chips{list-style:none;padding:0;margin:14px 0 18px;display:flex;flex-wrap:wrap;gap:8px}
.fh-chips li{border:1px solid var(--line2);padding:8px 14px;font-size:.92rem;background:#fff;margin:0}
.fh-group{margin:0 0 34px}.fh-group h3{margin-bottom:.3em}.fh-group p{color:var(--muted);margin:0 0 12px}
.fh-links{list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}
.fh-links li{margin:0}
.fh-links a{display:flex;align-items:center;min-height:48px;padding:12px 16px;border:1px solid var(--line2);background:#fff;text-decoration:none;color:var(--brown)}
.fh-links a:hover{border-color:var(--gold)}
.fh-links small{display:block;color:var(--muted);font-size:.82rem}
.fh-steps{padding-left:1.2em}.fh-steps li{margin:0 0 12px}
@media (max-width:760px){.fh-split{grid-template-columns:1fr}.fh-hero .cta-row{flex-direction:column;align-items:stretch}.fh-hero .cta-row .btn{width:100%}}
</style>'''

T = {
 'en': {
  'home': 'Home', 'hub': 'Funeral help', 'lang_attr': 'en-SG', 'locale': 'en_SG',
  'calm': 'If this has just happened, we are sorry for your loss. Take a breath. You do not have to do this alone.',
  'wa_btn': 'WhatsApp Benjamin', 'call_btn': 'Call ' + PHONE,
  'dock_call': 'Call 24/7' if FLAGS['open_24_7'] else 'Call',
  'dock_wa': 'WhatsApp',
 },
 'zh': {
  'home': '首页', 'hub': '殡葬协助', 'lang_attr': 'zh-Hans-SG', 'locale': 'zh_SG',
  'calm': '如果事情刚刚发生，请节哀。先深呼吸，您不必独自面对。',
  'wa_btn': 'WhatsApp 联系 Benjamin', 'call_btn': '致电 ' + PHONE,
  'dock_call': '致电 24/7' if FLAGS['open_24_7'] else '致电',
  'dock_wa': 'WhatsApp',
 },
}


def wa_url(text):
    return 'https://wa.me/6589329933?text=' + quote(text, safe='')


def wa_btn(lang, text, ref, cls='btn btn-wa', label=None):
    return ('<a class="%s" href="%s" target="_blank" rel="noopener" data-wa="1" data-ref="%s">%s<span>%s</span></a>'
            % (cls, E(wa_url(text)), ref, WA_SVG, E(label or T[lang]['wa_btn'])))


def call_btn(lang, ref, cls='btn btn-outline', label=None):
    return '<a class="%s" href="tel:+6589329933" data-ref="%s">%s</a>' % (cls, ref, E(label or T[lang]['call_btn']))


# ---------- live chrome (header / footer / dock) from the reference pages ----------
def chrome(ref_path, lang):
    s = open(ref_path, encoding='utf-8').read()
    pre = '../../' if lang == 'en' else '../../../'
    head_links = s[s.index('<link rel="icon"'):s.index('<link rel="preconnect"')]
    hdr = s[s.index('<a class="skip"'):s.index('<main id="main">')]
    ftr = s[s.index('<footer class="ftr">'):s.index('<div class="dock">')]
    person = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))['@graph'][0]
    website = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', s, re.S).group(1))['@graph'][1]
    out = []
    for part in (head_links, hdr, ftr):
        part = part.replace(pre, '{R}')
        out.append(part)
    head_links, hdr, ftr = out
    hdr = hdr.replace(' aria-current="page"', '')
    # language switch -> filled per page
    hdr = re.sub(r'<div class="lang".*?</div>', '{LANG}', hdr, flags=re.S)
    # footer: add "Funeral help" under Services, Google review button (live since 13 Nov)
    fs = 'services/funeral-services/">Funeral services</a></li>' if lang == 'en' else 'zh/services/funeral-services/">殡葬服务</a></li>'
    add = ('<li><a href="{R}funeral-help/">Funeral help</a></li>' if lang == 'en'
           else '<li><a href="{R}zh/funeral-help/">殡葬协助（按地区）</a></li>')
    assert fs in ftr, 'footer services anchor missing'
    ftr = ftr.replace(fs, fs + add, 1)
    if 'p1-foot-review' not in ftr:
        ftr = ftr.replace('<div class="ftr-legal">', REVIEW_BLOCK % REVIEW[lang] + '<div class="ftr-legal">', 1)
    return dict(head_links=head_links, hdr=hdr, ftr=ftr, person=person, website=website)


def lang_switch(lang, en_path, zh_path):
    a = 'aria-current="true"'
    return ('<div class="lang" aria-label="Language"><a href="{R}%s" hreflang="en-SG" lang="en-SG"%s>EN</a>'
            '<a href="{R}%s" hreflang="zh-SG" lang="zh-Hans-SG"%s>中文</a></div>'
            % (en_path, ' ' + a if lang == 'en' else '', zh_path, ' ' + a if lang == 'zh' else ''))


def dock(lang, wa_text, ref):
    return ('<div class="dock"><a class="dock-wa" href="%s" target="_blank" rel="noopener" data-wa="1" data-ref="%s">%s<span>%s</span></a>'
            '<a class="dock-call" href="tel:+6589329933" data-ref="%s">%s<span>%s</span></a></div>'
            % (E(wa_url(wa_text)), ref + '-dock', WA_SVG, T[lang]['dock_wa'], ref + '-dock', CALL_SVG, E(T[lang]['dock_call'])))


def page(lang, ch, rel, en_path, zh_path, title, meta, graph, body, wa_text, ref):
    url = SITE + (en_path if lang == 'en' else zh_path)
    fonts = ('family=Bodoni+Moda:opsz,wght@6..96,400;6..96,500&family=Jost:wght@400;500;600'
             + ('&family=Noto+Serif+SC:wght@600' if lang == 'zh' else '') + '&display=swap')
    og = 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@9349d27/site-assets/benjamin-poon/og-benjamin-poon-5.jpg'
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    h = f'''<!doctype html>
<html lang="{T[lang]['lang_attr']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(meta)}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="p1-site" content="benjamin-poon">
<meta name="theme-color" content="#ffffff">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en-SG" href="{SITE}{en_path}">
<link rel="alternate" hreflang="zh-SG" href="{SITE}{zh_path}">
<link rel="alternate" hreflang="x-default" href="{SITE}{en_path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Benjamin Poon 潘国雄">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(meta)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{'Benjamin Poon (潘国雄), Service Advisor and Life Managing Director, Singapore' if lang == 'en' else '潘国雄 Benjamin Poon，新加坡生命经理师'}">
<meta property="og:locale" content="{T[lang]['locale']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{og}">
{ch['head_links']}<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{fonts}">
<link rel="stylesheet" href="{{R}}bp.css?v=504e07be">
<script src="{{R}}bp.js?v=504e07be" defer></script>
<script type="application/ld+json">{ld}</script>
{FH_CSS}
</head>
<body>
{ch['hdr'].replace('{LANG}', lang_switch(lang, en_path, zh_path))}<main id="main">
{body}
</main>
{ch['ftr']}{dock(lang, wa_text, ref)}
</body>
</html>
'''
    return h.replace('{R}', rel)


# ---------- shared content blocks ----------
def first_hour(lang, ref_rel, intro=None):
    if lang == 'en':
        mort = (' If no doctor can certify the death, the police are called and your loved one is taken to Mortuary@HSA.'
                if FLAGS['mortuary_line'] else '')
        return f'''<h2>The first hour: three things</h2>
<ol class="fh-steps"><li><strong>Get the death certified.</strong> A doctor must certify the death first.</li>
<li><strong>Have the ID ready.</strong> The NRIC, FIN card or passport of your loved one.</li>
<li><strong>Call Benjamin on {PHONE}.</strong> Tell him where your loved one is, and whether a wake is wanted.</li></ol>
<div class="fh-split"><div><h3>In a hospital</h3><p>The hospital doctor certifies the death, and the doctor or hospital staff give you the death certificate number. Then call Benjamin.</p></div>
<div><h3>At home</h3><p>The family engages a doctor to come and certify the death.{mort} Then call Benjamin.</p></div></div>
<p>In the next few days, the death is registered automatically once it is certified online. Download the digital death certificate from My Legacy (LifeSG) within 30 days, and apply for the Permit to Bury or Cremate on NEA&#x27;s ePortal (<a href="https://www.ica.gov.sg/documents/death-certificate" target="_blank" rel="noopener">ICA</a>, <a href="https://www.nea.gov.sg/our-services/after-death/post-death-matters/when-death-occurs" target="_blank" rel="noopener">NEA</a>). The full guide: <a href="{ref_rel}guides/what-to-do-when-a-loved-one-passes-away-singapore/">what to do when a loved one passes away in Singapore</a>.</p>'''
    mort = ('如果没有医生能证明死亡，就需要报警，遗体会被送往卫生科学局殓房（Mortuary@HSA）。' if FLAGS['mortuary_line'] else '')
    return f'''<h2>最初一小时：先做三件事</h2>
<ol class="fh-steps"><li><strong>先由医生证明死亡。</strong>这一步必须先完成。</li>
<li><strong>准备好身份证件。</strong>亡者的身份证（NRIC）、准证（FIN）或护照。</li>
<li><strong>致电潘国雄 {PHONE}。</strong>告诉他亲人现在在哪里，以及家人是否要办守灵。</li></ol>
<div class="fh-split"><div><h3>在医院离世</h3><p>由医院的医生证明死亡，医生或医院职员会给您死亡证书号码。接着致电 Benjamin。</p></div>
<div><h3>在家中离世</h3><p>家人需请医生上门证明死亡。{mort}接着致电 Benjamin。</p></div></div>
<p>接下来几天：医生在网上证明死亡后，死亡登记会自动完成。请在 30 天内通过 My Legacy（LifeSG）下载电子死亡证书，并在环境局（NEA）电子平台申请土葬或火化准证（<a href="https://www.ica.gov.sg/documents/death-certificate" target="_blank" rel="noopener">ICA</a>、<a href="https://www.nea.gov.sg/our-services/after-death/post-death-matters/when-death-occurs" target="_blank" rel="noopener">NEA</a>）。完整指南：<a href="{ref_rel}zh/guides/what-to-do-when-a-loved-one-passes-away-singapore/">亲人在新加坡离世后该怎么办</a>。</p>'''


def nirvana_covers(lang, rel):
    rel_line = FLAGS['religions_en'] if lang == 'en' else FLAGS['religions_zh']
    if lang == 'en':
        return f'''<h2>What Nirvana&#x27;s funeral services cover</h2>
<p>Benjamin arranges Nirvana funeral services. According to <a href="https://nirvana.com.sg/funeral-services/" target="_blank" rel="noopener">Nirvana</a>, they include:</p>
<ul><li>Coordination of the funeral service and memorial ceremony.</li><li>Embalming and encoffinment.</li><li>The funeral procession.</li><li>Preparation of the memorial ceremony.</li></ul>
<p>For women who have passed, Nirvana&#x27;s <a href="{rel}guides/journey-with-love-nirvana-care-for-women/">Journey with Love</a> care is carried out by an all-female team. {E(rel_line)}</p>
<p>Benjamin explains the options and what is included before anything is confirmed. Prices are given on request.</p>'''
    return f'''<h2>富贵山庄（Nirvana）殡葬服务包括什么</h2>
<p>潘国雄为您安排富贵山庄（Nirvana）殡葬服务。根据<a href="https://nirvana.com.sg/funeral-services/" target="_blank" rel="noopener">富贵山庄</a>的资料，服务包括：</p>
<ul><li>统筹丧礼及追思仪式。</li><li>遗体防腐与入殓。</li><li>出殡行列。</li><li>追思仪式的筹备。</li></ul>
<p>女性亡者可选择富贵山庄的<a href="{rel}zh/guides/journey-with-love-nirvana-care-for-women/">「爱。相随」</a>服务，由全女性团队照料。{E(rel_line)}</p>
<p>在确认任何安排之前，Benjamin 会先说明各项选择和所包括的内容。价格可向他询问。</p>'''


def afterwards(lang, rel, venue):
    v = VENUES[venue]
    if lang == 'en':
        return f'''<h2>Afterwards, when the family is ready</h2>
<p>There is no need to decide on a niche on the first day. When the family is ready, Benjamin can explain <a href="{rel}services/columbarium-niches/">columbarium niches</a>, <a href="{rel}services/ancestral-tablets/">ancestral tablets</a> and the options at <a href="{rel}{v['page']}">{E(v['en'])}</a>.</p>'''
    return f'''<h2>之后，等家人准备好再说</h2>
<p>福位不必在第一天就决定。家人准备好以后，Benjamin 可以为您介绍<a href="{rel}zh/services/columbarium-niches/">福位 / 骨灰位</a>、<a href="{rel}zh/services/ancestral-tablets/">神主牌</a>，以及<a href="{rel}zh/{v['page']}">{E(v['zh'])}</a>的选择。</p>'''


def faq_html(lang, faq):
    h = '<section class="faq"><h2>%s</h2>' % ('Common questions' if lang == 'en' else '常见问题')
    for f in faq:
        h += '<details><summary>%s</summary><p>%s</p></details>' % (E(f['q']), E(f['a']))
    return h + '</section>'


def band(lang, wa_text, ref):
    if lang == 'en':
        t, p = 'Talk to Benjamin directly', ('WhatsApp or call %s%s. English, Mandarin, Cantonese or Hokkien. %s' % (
            PHONE, ', 24/7' if FLAGS['open_24_7'] else '', FLAGS['response_en']))
    else:
        t, p = '直接与 Benjamin 联系', ('WhatsApp 或致电 %s%s。华语、英语、广东话、福建话都可以。%s' % (
            PHONE, '，24 小时全天候' if FLAGS['open_24_7'] else '', FLAGS['response_zh']))
    return ('<section class="sec"><div class="wrap"><div class="band"><div><h2>%s</h2><p>%s</p></div><div class="cta-row">%s%s</div></div></div></section>'
            % (t, E(p), wa_btn(lang, wa_text, ref + '-end'), call_btn(lang, ref + '-end', cls='btn btn-ghost')))


def hero(lang, h1, rel, crumbs, now_line, wa_text, ref):
    return ('<section class="phero fh-hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb">%s</nav><h1>%s</h1>'
            '<p class="lede">%s</p><p class="fh-now">%s</p><div class="cta-row">%s%s</div></div></section>'
            % (crumbs, E(h1), E(T[lang]['calm']), now_line, wa_btn(lang, wa_text, ref + '-hero'), call_btn(lang, ref + '-hero')))


def hours_spec():
    return {'@type': 'OpeningHoursSpecification',
            'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            'opens': '00:00', 'closes': '23:59'}


def now_line(lang, area_label=None):
    if lang == 'en':
        s = 'Call or WhatsApp Benjamin Poon on %s%s. He represents Nirvana Singapore and arranges Nirvana funeral services%s, in English, Mandarin, Cantonese or Hokkien. %s' % (
            PHONE, ', 24/7' if FLAGS['open_24_7'] else '', ' for families in ' + area_label if area_label else ' for families across Singapore', FLAGS['response_en'])
    else:
        s = '请致电或 WhatsApp 潘国雄（Benjamin Poon）%s%s。他代表富贵山庄（Nirvana Singapore），为%s的家庭安排富贵山庄殡葬服务，可用华语、英语、广东话或福建话沟通。%s' % (
            PHONE, '，24 小时全天候接听' if FLAGS['open_24_7'] else '', area_label or '新加坡各区', FLAGS['response_zh'])
    return E(s)


# ---------- area page ----------
def area_page(lang, a, ch):
    c = a[lang]
    slug = a['slug']
    v = VENUES[a['cluster']]
    en_path, zh_path = 'funeral-help/%s/' % slug, 'zh/funeral-help/%s/' % slug
    rel = '../../' if lang == 'en' else '../../../'
    z = '' if lang == 'en' else 'zh/'
    ref = 'fh-' + slug
    if lang == 'en':
        wa_text = 'Hello Benjamin, someone in my family has just passed away. We are in %s. [Ref: FH-%s]' % (c['label'], slug)
    else:
        wa_text = '您好 Benjamin，我家里有人刚刚离世。我们在%s。[Ref: FH-%s]' % (c['label'], slug)
    crumbs = '<a href="%s%s">%s</a> / <a href="%s%sfuneral-help/">%s</a> / <span>%s</span>' % (
        rel, z, T[lang]['home'], rel, z, T[lang]['hub'], E(c['name']))
    near_h = ('Near you: %s' % c['label']) if lang == 'en' else ('您附近：%s' % c['label'])
    chips = '<ul class="fh-chips">' + ''.join('<li>%s</li>' % E(x) for x in c['areas']) + '</ul>'
    neighbours = [x for x in AREAS if x['slug'] in a['neighbours']]
    nb = '<ul class="fh-links">' + ''.join(
        '<li><a href="%s%sfuneral-help/%s/">%s</a></li>' % (rel, z, x['slug'], E(x[lang]['label'])) for x in neighbours)
    nb += '<li><a href="%s%sfuneral-help/">%s</a></li></ul>' % (rel, z, 'All areas' if lang == 'en' else '所有地区')
    body = hero(lang, c['h1'], rel, crumbs, now_line(lang, c['name']), wa_text, ref)
    body += '<section class="sec"><div class="wrap narrow"><div class="prose">'
    body += '<div class="answer">%s</div>' % E(c['intro'])
    body += first_hour(lang, rel)
    body += '<div class="cta-row" style="margin:24px 0">%s%s</div>' % (wa_btn(lang, wa_text, ref + '-body'), call_btn(lang, ref + '-body'))
    body += '<h2>%s</h2><p>%s</p>%s' % (E(near_h), E(c['near']), chips)
    body += nirvana_covers(lang, rel)
    body += afterwards(lang, rel, a['cluster'])
    body += faq_html(lang, c['faq'])
    body += '<h2>%s</h2>%s' % ('Nearby areas' if lang == 'en' else '邻近地区', nb)
    body += '</div></div></section>'
    body += band(lang, wa_text, ref)
    url = SITE + (en_path if lang == 'en' else zh_path)
    svc = {'@type': 'Service', '@id': url + '#service',
           'name': ('Funeral help in %s' % c['label']) if lang == 'en' else ('%s殡葬协助' % c['label']),
           'serviceType': 'Funeral arrangement (Nirvana funeral services)',
           'provider': {'@id': SITE + '#benjamin'},
           'areaServed': [{'@type': 'Place', 'name': x + ', Singapore'} for x in a['en']['areas']],
           'availableChannel': {'@type': 'ServiceChannel', 'servicePhone': {'@type': 'ContactPoint', 'telephone': '+6589329933', 'contactType': 'funeral arrangement', 'availableLanguage': ['English', 'Mandarin', 'Cantonese', 'Hokkien']}},
           'url': url}
    if FLAGS['open_24_7']:
        svc['hoursAvailable'] = hours_spec()
    graph = [ch['person'], ch['website'],
             {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': c['title'], 'description': c['meta'],
              'inLanguage': T[lang]['lang_attr'], 'datePublished': TODAY, 'dateModified': TODAY,
              'about': {'@id': url + '#service'}, 'isPartOf': {'@id': SITE + '#website'}},
             {'@type': 'BreadcrumbList', 'itemListElement': [
                 {'@type': 'ListItem', 'position': 1, 'name': T[lang]['home'], 'item': SITE + z},
                 {'@type': 'ListItem', 'position': 2, 'name': T[lang]['hub'], 'item': SITE + z + 'funeral-help/'},
                 {'@type': 'ListItem', 'position': 3, 'name': c['label'], 'item': url}]},
             svc,
             {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in c['faq']]}]
    return page(lang, ch, rel, en_path, zh_path, c['title'], c['meta'], graph, body, wa_text, ref)


# ---------- hub ----------
def hub_page(lang, ch):
    H = CFG['hub'][lang]
    en_path, zh_path = 'funeral-help/', 'zh/funeral-help/'
    rel = '../' if lang == 'en' else '../../'
    z = '' if lang == 'en' else 'zh/'
    ref = 'fh-hub'
    wa_text = H['wa']
    crumbs = '<a href="%s%s">%s</a> / <span>%s</span>' % (rel, z, T[lang]['home'], T[lang]['hub'])
    body = hero(lang, H['h1'], rel, crumbs, now_line(lang), wa_text, ref)
    body += '<section class="sec"><div class="wrap narrow"><div class="prose">'
    body += '<div class="answer">%s</div>' % E(H['intro'])
    body += first_hour(lang, rel)
    body += '<div class="cta-row" style="margin:24px 0">%s%s</div>' % (wa_btn(lang, wa_text, ref + '-body'), call_btn(lang, ref + '-body'))
    body += '<h2>%s</h2>' % E(H['areas_h'])
    for key in ('linsan', 'thianleng', 'nirvana'):
        v = VENUES[key]
        group = [a for a in AREAS if a['cluster'] == key]
        if not group:
            continue
        body += '<div class="fh-group"><h3>%s</h3><p>%s</p><ul class="fh-links">' % (E(H['group_h'][key]), E(v['addr_' + lang]))
        for a in group:
            km = a['distance_km']
            small = ('about %s km from %s' % (km, v['short_en'])) if lang == 'en' else ('距离%s约 %s 公里' % (v['zh'], km))
            body += '<li><a href="%s%sfuneral-help/%s/"><span>%s<small>%s</small></span></a></li>' % (rel, z, a['slug'], E(a[lang]['label']), E(small))
        body += '</ul></div>'
    body += '<p style="font-size:.9rem;color:var(--muted)">%s</p>' % E(H['distance_note'])
    body += nirvana_covers(lang, rel)
    body += '<h2>%s</h2><ul>' % E(H['more_h'])
    for path, lab in H['more']:
        body += '<li><a href="%s%s">%s</a></li>' % (rel, path, E(lab))
    body += '</ul></div></div></section>'
    body += band(lang, wa_text, ref)
    url = SITE + (en_path if lang == 'en' else zh_path)
    svc = {'@type': 'Service', '@id': url + '#service', 'name': H['svc_name'],
           'serviceType': 'Funeral arrangement (Nirvana funeral services)', 'provider': {'@id': SITE + '#benjamin'},
           'areaServed': {'@type': 'Country', 'name': 'Singapore'}, 'url': url}
    if FLAGS['open_24_7']:
        svc['hoursAvailable'] = hours_spec()
    graph = [ch['person'], ch['website'],
             {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': H['title'], 'description': H['meta'],
              'inLanguage': T[lang]['lang_attr'], 'datePublished': TODAY, 'dateModified': TODAY,
              'about': {'@id': url + '#service'}, 'isPartOf': {'@id': SITE + '#website'}},
             {'@type': 'BreadcrumbList', 'itemListElement': [
                 {'@type': 'ListItem', 'position': 1, 'name': T[lang]['home'], 'item': SITE + z},
                 {'@type': 'ListItem', 'position': 2, 'name': T[lang]['hub'], 'item': url}]},
             svc,
             {'@type': 'ItemList', 'itemListElement': [
                 {'@type': 'ListItem', 'position': i + 1, 'name': a[lang]['label'], 'url': SITE + z + 'funeral-help/%s/' % a['slug']}
                 for i, a in enumerate(AREAS)]}]
    return page(lang, ch, rel, en_path, zh_path, H['title'], H['meta'], graph, body, wa_text, ref)


def main():
    ref_en, ref_zh, out = sys.argv[1:4]
    chs = {'en': chrome(ref_en, 'en'), 'zh': chrome(ref_zh, 'zh')}
    n = 0
    for lang in ('en', 'zh'):
        base = os.path.join(out, '' if lang == 'en' else 'zh', 'funeral-help')
        os.makedirs(base, exist_ok=True)
        open(os.path.join(base, 'index.html'), 'w', encoding='utf-8').write(hub_page(lang, chs[lang])); n += 1
        for a in AREAS:
            d = os.path.join(base, a['slug'])
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(area_page(lang, a, chs[lang])); n += 1
    print('pages', n)


if __name__ == '__main__':
    main()
