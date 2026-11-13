"""K Tech articles (/articles/ hub + one page per article), EN + BM + 中文 (13 Nov 2026).

Template-first: every page reuses build.py's head(), header(), footer(), wabtn() and schema, so header/footer/dock changes
reach the articles too. One article = one file data/articles/<slug>.json (en / ms / zh). The article look is
src/articles.css, loaded on article pages only (k.css unchanged).
"""
import glob
import html
import json
import os
from datetime import date

E_ = html.escape
UIA = {
 'en': {'nav': 'Articles', 'title': 'Articles for workshops | K Tech', 'desc': 'Practical notes for Malaysian workshops on diagnostics, ADAS, TPMS and key programming, from K Tech, Autel dealer in Johor Bahru.',
        'h1': 'Articles for workshops', 'intro': 'Practical notes on diagnostic tools and jobs, written for workshop technicians and owners.',
        'report': 'Workshop note', 'result': 'Short answer', 'published': 'Published', 'updated': 'Updated', 'read': 'Read time', 'min': '{n} min',
        'faq': 'Questions', 'more': 'More articles', 'empty': 'The first articles are on the way.', 'tool_lead': 'The Autel tools for this job:', 'tool_link': 'See {topic} →',
        'cta_h': 'Not sure which tool fits your jobs?', 'cta_p': 'WhatsApp us your car brands and the jobs you do. We suggest the Autel tool that fits.'},
 'ms': {'nav': 'Artikel', 'title': 'Artikel untuk bengkel | K Tech', 'desc': 'Nota praktikal untuk bengkel di Malaysia tentang diagnostik, ADAS, TPMS dan program kunci, daripada K Tech, pengedar Autel di Johor Bahru.',
        'h1': 'Artikel untuk bengkel', 'intro': 'Nota praktikal tentang alat diagnostik dan kerja bengkel, ditulis untuk juruteknik dan pemilik bengkel.',
        'report': 'Nota bengkel', 'result': 'Jawapan ringkas', 'published': 'Diterbitkan', 'updated': 'Dikemas kini', 'read': 'Masa membaca', 'min': '{n} minit',
        'faq': 'Soalan', 'more': 'Artikel lain', 'empty': 'Artikel pertama akan menyusul tidak lama lagi.', 'tool_lead': 'Alat Autel untuk kerja ini:', 'tool_link': 'Lihat {topic} →',
        'cta_h': 'Tidak pasti alat mana yang sesuai?', 'cta_p': 'WhatsApp jenama kereta dan kerja yang anda buat. Kami cadangkan alat Autel yang sesuai.'},
 'zh': {'nav': '文章', 'title': '写给维修厂的文章 | K Tech', 'desc': 'K Tech（新山 Autel 经销商）为马来西亚维修厂写的实用笔记：诊断、ADAS、胎压监测和钥匙匹配。',
        'h1': '写给维修厂的文章', 'intro': '关于诊断工具和维修工作的实用笔记，写给维修厂的技师和老板。',
        'report': '维修厂笔记', 'result': '简短回答', 'published': '发布日期', 'updated': '更新日期', 'read': '阅读时间', 'min': '{n} 分钟',
        'faq': '常见问题', 'more': '更多文章', 'empty': '第一批文章即将推出。', 'tool_lead': '适合这项工作的 Autel 工具：', 'tool_link': '查看{topic} →',
        'cta_h': '不确定哪款工具适合您？', 'cta_p': '通过 WhatsApp 告诉我们您修的车款和工作，我们推荐合适的 Autel 工具。'},
}
MS_MON = ['Jan', 'Feb', 'Mac', 'Apr', 'Mei', 'Jun', 'Jul', 'Ogo', 'Sep', 'Okt', 'Nov', 'Dis']


def load(base):
    arts = [json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(base, 'data', 'articles', '*.json'))]
    return sorted(arts, key=lambda a: (a['published'], a['slug']), reverse=True)


def nice(l, iso):
    d = date.fromisoformat(iso)
    return f'{d.year}年{d.month}月{d.day}日' if l == 'zh' else f'{d.day} {MS_MON[d.month - 1]} {d.year}' if l == 'ms' else f"{d.day} {d.strftime('%b')} {d.year}"


def register(g, arts):
    """Give the hub and every article a page key so head()/header()/curl_() work unchanged."""
    g['SLUG']['articles'] = 'articles/'
    for l in g['LANGS']:
        g['UI'][l]['nav']['articles'] = UIA[l]['nav']
    g['TITLE']['articles'] = {l: UIA[l]['title'] for l in g['LANGS']}
    g['DESC']['articles'] = {l: UIA[l]['desc'] for l in g['LANGS']}
    for a in arts:
        k = 'art:' + a['slug']
        g['SLUG'][k] = f"articles/{a['slug']}/"
        g['TITLE'][k] = {l: a[l]['title'] + ' | K Tech' for l in g['LANGS']}
        g['DESC'][k] = {l: a[l]['description'] for l in g['LANGS']}
    return ['articles'] + ['art:' + a['slug'] for a in arts]


def _css(g):
    return f'<link rel="stylesheet" href="{g["A"]}articles.css{g["V"]}"></head>'


def _card(g, l, a, i):
    t = a[l]
    return (f'<a class="rp-card" href="{g["url"]("art:" + a["slug"], l)}"><span class="mono">N{i:02d}</span><h3>{E_(t["h1"])}</h3>'
            f'<time datetime="{a["published"]}">{E_(nice(l, a["published"]))}</time><p>{E_(t["description"])}</p></a>')


def _crumbs(g, l, items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': n, 'item': g['curl_'](k, l)} for i, (k, n) in enumerate(items, 1)]}


def page_hub(g, l, arts):
    u, nav = UIA[l], g['UI'][l]['nav']
    n = len(arts)
    cards = ''.join(_card(g, l, a, n - i) for i, a in enumerate(arts)) or f'<p class="rp-empty">{E_(u["empty"])}</p>'
    body = (f'<section class="ph"><div class="wrap"><div class="crumb"><a href="{g["url"]("home", l)}">{E_(nav["home"])}</a> / {E_(u["nav"])}</div>'
            f'<h1>{E_(u["h1"])}</h1><p>{E_(u["intro"])}</p>{g["wabtn"](l, ref="top")}</div></section>'
            f'<section class="sec"><div class="wrap"><div class="rp-list-cards">{cards}</div></div></section>' + g['end_cta'](l, u['cta_h'], u['cta_p']))
    items = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': u['h1'], 'url': g['curl_']('articles', l),
             'mainEntity': {'@type': 'ItemList', 'itemListElement': [{'@type': 'ListItem', 'position': i, 'url': g['curl_']('art:' + a['slug'], l), 'name': a[l]['h1']} for i, a in enumerate(arts, 1)]}}
    return (g['head']('articles', l, [g['schema_org'](l), items, _crumbs(g, l, [('home', nav['home']), ('articles', u['nav'])])]).replace('</head>', _css(g), 1)
            + g['header']('articles', l) + body + g['footer'](l))


def page_article(g, l, a, num, others):
    t, u, nav, F = a[l], UIA[l], g['UI'][l]['nav'], g['F']
    k = 'art:' + a['slug']
    meta = [f'<li>{E_(u["published"])} <b><time datetime="{a["published"]}">{E_(nice(l, a["published"]))}</time></b></li>']
    if a['updated'] != a['published']:
        meta.append(f'<li>{E_(u["updated"])} <b><time datetime="{a["updated"]}">{E_(nice(l, a["updated"]))}</time></b></li>')
    meta.append(f'<li>{E_(u["read"])} <b>{E_(u["min"].format(n=a["minutes"]))}</b></li>')
    hero = (f'<section class="rp-hero"><div class="wrap"><div class="crumb"><a href="{g["url"]("home", l)}">{E_(nav["home"])}</a> / '
            f'<a href="{g["url"]("articles", l)}">{E_(u["nav"])}</a></div><div class="rp-sheet">'
            f'<div class="rp-strip"><span>{E_(u["report"])} <b>N{num:02d}</b></span><span>K Tech · Johor Bahru</span></div>'
            f'<p class="rp-tag">{E_(t["keyword"])}</p><h1>{E_(t["h1"])}</h1><p class="lead">{E_(t["lead"])}</p>'
            f'<div class="rp-result" role="note"><span class="mono">{E_(u["result"])}</span><p>{E_(t["answer"])}</p></div>'
            f'<ul class="rp-meta">{"".join(meta)}</ul></div></div></section>')
    inner = ''
    for i, sec in enumerate(t['sections'], 1):
        inner += f'<h2><span class="mono">{i:02d}</span><span>{E_(sec["h2"])}</span></h2>' + ''.join(f'<p>{E_(x)}</p>' for x in sec.get('p', []))
        if sec.get('checks'):
            inner += '<ol class="rp-checks">' + ''.join(f'<li><span class="mono">C{j}</span><div><b>{E_(c["b"])}</b>{E_(c["t"])}</div></li>' for j, c in enumerate(sec['checks'], 1)) + '</ol>'
        if sec.get('list'):
            inner += '<ul class="rp-list">' + ''.join(f'<li>{E_(x)}</li>' for x in sec['list']) + '</ul>'
        if sec.get('note'):
            inner += f'<p class="rp-note">{E_(sec["note"])}</p>'
    fam = next(f for f in g['FAMILIES'] if f['k'] == a['family'])
    inner += (f'<div class="rp-tool"><span class="mono">{fam["code"]} · Autel</span><div>{E_(u["tool_lead"])} '
              f'<a href="{g["url"]("tools", l)}#{fam["k"]}">{E_(u["tool_link"].format(topic=fam[l][0]))}</a></div>{g["wabtn"](l, ref="article")}</div>')
    body = hero + f'<section class="sec"><div class="wrap"><div class="rp-body">{inner}</div></div></section>'
    faqs = [(f['q'], f['a']) for f in t['faqs']]
    body += f'<section class="sec alt"><div class="wrap"><div class="sh"><div><h2>{E_(u["faq"])}</h2></div></div>{g["faq_html"](l, faqs)}</div></section>'
    if others:
        body += f'<section class="sec"><div class="wrap"><div class="sh"><div><h2>{E_(u["more"])}</h2></div></div><div class="rp-list-cards">{"".join(_card(g, l, o, n) for o, n in others)}</div></div></section>'
    body += g['end_cta'](l, u['cta_h'], u['cta_p'])
    art = {'@context': 'https://schema.org', '@type': 'Article', 'headline': t['h1'], 'description': t['description'], 'inLanguage': g['LANG_META'][l]['html'],
           'datePublished': a['published'], 'dateModified': a['updated'], 'url': g['curl_'](k, l), 'mainEntityOfPage': g['curl_'](k, l), 'keywords': t['keyword'],
           'image': g['CANON'] + 'assets/og.jpg', 'author': {'@id': g['CANON'] + '#org'}, 'publisher': {'@id': g['CANON'] + '#org'}}
    schemas = [g['schema_org'](l), art, g['faq_schema'](l, faqs), _crumbs(g, l, [('home', nav['home']), ('articles', u['nav']), (k, t['h1'])])]
    return g['head'](k, l, schemas).replace('</head>', _css(g), 1) + g['header'](k, l) + body + g['footer'](l)


def build(g, arts):
    """Write the hub + articles for every language into g['OUT']; copy articles.css. Returns the page keys (for sitemap/llms)."""
    import shutil
    shutil.copy(os.path.join(g['B'], 'src', 'articles.css'), os.path.join(g['OUT'], 'assets'))
    n = len(arts)
    num = {a['slug']: n - i for i, a in enumerate(arts)}
    for l in g['LANGS']:
        d = os.path.join(g['OUT'], g['LANG_META'][l]['prefix'] + 'articles/')
        os.makedirs(d, exist_ok=True)
        open(d + 'index.html', 'w', encoding='utf-8').write(page_hub(g, l, arts))
        for a in arts:
            others = [(o, num[o['slug']]) for o in arts if o['slug'] != a['slug']][:3]
            p = os.path.join(d, a['slug'])
            os.makedirs(p, exist_ok=True)
            open(os.path.join(p, 'index.html'), 'w', encoding='utf-8').write(page_article(g, l, a, num[a['slug']], others))
