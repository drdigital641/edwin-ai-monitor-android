#!/usr/bin/env python3
"""Build the Sheng Heng Auto Service Centre preview (20 pages x EN/BM/中文 + review.html) into ../dist.
Pages come from the shared partials (partials.py); service + area pages use one template each."""
import os, sys, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from partials import *  # noqa
sys.path.insert(0, '/mnt/project-files/autoseo-template/privacy/')
import privacy_page as PV

DIST = os.path.join(HERE, '..', 'dist')
UPDATED = '2026-11-24'
PAGES = []  # English-relative paths, for sitemap/llms


def write(rel, text):
    p = os.path.join(DIST, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)


def media_html(L, m, wide=True):
    if not m:
        return ''
    if m == 'video':
        return video_tile(L)
    if m.startswith('pair:'):
        return slider(L, m.split(':')[1])
    if m == 'w03':
        return w03(L)
    return figure(L, m, '(min-width:900px) 560px, 100vw')


def ticks(items):
    if not items:
        return ''
    return '<ul class="ticks">' + ''.join(f'<li>{icon("tick")}<span>{E(b)}</span></li>' for b in items) + '</ul>'


# ---------------------------------------------------------------- home
def nb(h):
    """Keep CJK words together in the home H1 (never break inside 欧洲车 / 亚洲车)."""
    for w in ('欧洲车', '亚洲车', '修车厂'):
        h = h.replace(w, f'<span class="nb">{w}</span>')
    return h


def page_home(L):
    c, h = C[L['code']], C[L['code']]['home']
    pg = c['pages']['home']
    chip_ic = ['adas-calibration-skudai', 'ecu-repair-programming-skudai', 'gearbox-overhaul-skudai', 'car-diagnostic-skudai']
    readout = ''.join(f'<li>{icon("tick")}{E(x)}</li>' for x in h['chips'])
    board = ''.join(f'''<li><a class="tile card" href="{lp(L, s + '/')}"><span class="th">{img(L, THUMB[s], '(min-width:900px) 280px, 46vw')}</span>
<span class="tb"><span class="ic">{icon(s)}</span><h3>{E(c['services'][s]['nav'])}</h3><p>{E(c['services'][s]['tile'])}</p><span class="go">{icon('arrow')}</span></span></a></li>''' for s in ORDER)
    adas_li = ''.join(f'<li>{icon("tick")}<span>{E(x)}</span></li>' for x in h['adas_lines'])
    lamps_ic = ['lamp-check', 'lamp-scan', 'lamp-quote', 'lamp-road']
    lamps = ''.join(f'<li><span class="lamp">{icon(lamps_ic[i])}</span><div><span class="n">{i + 1}/4</span><h3>{E(t)}</h3><p>{E(d)}</p></div></li>' for i, (t, d) in enumerate(h['process']))
    makes = ''.join(f'<li><span class="chip">{E(m)}</span></li>' for m in F['makes'])
    ld_ = ld(L, ld_business(L), ld_crumbs(L, [(ui(L, 'breadcrumb_home'), '')]), ld_faq(pg['faqs']))
    body = f'''<body>
{header(L, '')}
<main id="main">
<section class="spec"><div class="wrap spec-grid">
<div class="frame stripe">{img(L, 'h01', '(min-width:1024px) 640px, 100vw', eager=True)}</div>
<div>
<p class="est"><b>Est. 2010</b> {E(ui(L, 'tagline'))}</p>
<h1>{nb(E(pg['h1']))}</h1>
<p class="kick">{E(pg['kicker'])}</p>
<div class="ctas">{wa_a(L, c['wa_home'], 'whatsapp_home_hero', label=ui(L, 'wa'))}{call_a(L, 'call_home_hero')}</div>
<ul class="readout" aria-label="{E(ui(L, 'nav_services'))}">{readout}</ul>
</div></div></section>

<section class="band ice" id="proof"><div class="wrap">
<div class="sec-h"><h2>{E(h['proof_h'])}</h2><p>{E(h['proof_sub'])}</p></div>
<div class="proofs">
<div class="ba-wrap">{slider(L, 'p01', 'p01_cap')}</div>
<div class="ba-wrap">{slider(L, 'p02', 'p02_cap')}</div>
<div class="wide">{w03(L)}</div>
</div></div></section>

<section class="band" id="services"><div class="wrap">
<div class="sec-h"><h2>{E(h['board_h'])}</h2><p>{E(h['board_sub'])}</p></div>
<ul class="board">{board}</ul>
</div></section>

<section class="band deep" id="adas"><div class="wrap adas">
<div><p class="kick">ADAS</p><h2>{E(h['adas_h'])}</h2><ul>{adas_li}</ul>
<div class="ctas">{wa_a(L, c['wa_adas'], 'whatsapp_home_adas', label=h['adas_btn'])}<a class="btn btn-ghost" href="{lp(L, 'adas-calibration-skudai/')}">{E(h['adas_link'])}</a></div></div>
<div class="adas-media">{figure(L, 'w01', '(min-width:1024px) 420px, 100vw')}{video_tile(L)}</div>
</div></section>

<section class="band" id="process"><div class="wrap">
<div class="sec-h"><h2>{E(h['process_h'])}</h2></div>
<ol class="lamps">{lamps}</ol>
</div></section>

<section class="band ice" id="reviews"><div class="wrap">
<div class="sec-h"><h2>{E(ui(L, 'reviews_h'))}</h2><p>{E(ui(L, 'reviews_sub'))}</p></div>
{tickets(L)}
<div class="proof-links"><a class="btn btn-call btn-sm" href="{E(F['maps_url'])}" target="_blank" rel="noopener" data-cta="map" data-ref="reviews_google_home">{icon('pin')}<span>{E(ui(L, 'see_reviews'))}</span></a>{review_btn(L, 'review_home')}</div>
</div></section>

<section class="band" id="workshop"><div class="wrap">
<div class="sec-h"><h2>{E(h['rail_h'])}</h2></div>
{rail(L)}
<p class="rail-note">{E(ui(L, 'photo_note'))}</p>
<h2 style="margin-top:44px">{E(h['makes_h'])}</h2><ul class="chips">{makes}</ul>
<h2 style="margin-top:44px">{E(h['areas_h'])}</h2><p class="sub">{E(h['areas_sub'])}</p>{area_chips(L)}
</div></section>

<section class="band ice" id="visit"><div class="wrap">
<div class="sec-h"><h2>{E(h['visit_h'])}</h2><p>{E(h['visit_sub'])}</p></div>
{visit_block(L, 'findus')}
</div></section>
{faq_block(L, pg['faqs'])}
</main>
{footer(L, '')}'''
    return head(L, '', pg['title'], pg['meta'], ld_, preload_hero=True) + body


# ---------------------------------------------------------------- service template
def page_service(L, slug):
    c = C[L['code']]
    s = c['services'][slug]
    path = slug + '/'
    sh = SHORT[slug]
    i = ORDER.index(slug)
    nxt = ORDER[(i + 1) % len(ORDER)]
    crumb = [(ui(L, 'breadcrumb_home'), ''), (s['nav'], path)]
    ld_ = ld(L, ld_business(L), ld_service(L, slug, path), ld_faq(s['faqs']) if s['faqs'] else None, ld_crumbs(L, crumb))
    intro = ''.join(f'<p class="lead">{E(p)}</p>' for p in s['intro'])
    # lead media = first section media that is a photo; keeps the page top visual
    sections = [dict(x) for x in s['sections']]
    top_i = next((k for k, x in enumerate(sections) if x.get('media') and x['media'] != 'video'), None)
    top_m = sections[top_i]['media'] if top_i is not None else 'h01'
    if top_i is not None:
        sections[top_i]['media'] = None
    if top_m.startswith('pair:'):
        top_html = slider(L, top_m.split(':')[1])
    elif top_m == 'w03':
        top_html = w03(L)
    else:
        top_html = figure(L, top_m, '(min-width:1024px) 520px, 100vw', extra_cls='stripe top')
    secs = []
    for k, sec in enumerate(sections):
        media = media_html(L, sec.get('media'))
        text = f'<div><h2>{E(sec["h2"])}</h2>' + ''.join(f'<p>{E(p)}</p>' for p in sec['paras']) + ticks(sec.get('bullets')) + '</div>'
        inner = f'<div class="sgrid{" flip" if k % 2 else ""}">{text}<div>{media}</div></div>' if media else f'<div class="prose">{text}</div>'
        secs.append(f'<section class="sec"><div class="wrap">{inner}</div></section>')
        if k == 1:
            secs.append(mid_cta(L, s['wa'], sh + '_mid'))
    proof = ''
    if slug in ('car-diagnostic-skudai', 'car-key-immobilizer-skudai'):
        proof = f'<section class="band ice"><div class="wrap"><div class="sec-h"><h2>{E(ui(L, "reviews_h"))}</h2></div>{tickets(L, [0])}<div class="proof-links">{review_btn(L, "review_" + sh)}</div></div></section>'
    nc = c['services'][nxt]
    body = f'''<body>
{header(L, path)}
<main id="main">
<section class="ptop"><div class="wrap">{crumbs(L, crumb)}
<div class="ptop-grid"><div>
<h1>{E(s['h1'])}</h1><p class="kick">{E(s['kicker'])}</p>{intro}
{cta_row(L, s['wa'], sh + '_intro')}
</div><div>{top_html}</div></div>
</div></section>
{''.join(secs)}
{proof}
{faq_block(L, s['faqs'])}
<section class="sec"><div class="wrap"><p class="upd">{E(ui(L, 'updated'))}</p>
<div class="links3"><div><a class="card next" href="{lp(L, nxt + '/')}"><span><small>{E(ui(L, 'next_service'))}</small><b>{E(nc['nav'])}</b></span>{icon('arrow')}</a>
<h3 style="margin-top:22px">{E(ui(L, 'all_services'))}</h3>{svc_list(L, slug)}</div>
<div><h3>{E(ui(L, 'nav_areas'))}</h3>{area_chips(L)}<p style="margin-top:18px"><a href="{lp(L, '')}">{E(ui(L, 'breadcrumb_home'))}</a></p></div></div>
</div></section>
{end_cta(L, s['wa'], sh + '_end')}
</main>
{footer(L, path)}'''
    return head(L, path, s['title'], s['meta'], ld_) + body


# ---------------------------------------------------------------- area template
def page_area(L, a):
    c = C[L['code']]
    slug = a['slug']
    ar = c['areas'][slug]
    path = 'areas/' + slug + '/'
    crumb = [(ui(L, 'breadcrumb_home'), ''), (ui(L, 'breadcrumb_areas'), path), (ar['nav'], path)]
    crumb = [crumb[0], crumb[2]]
    ref = 'area_' + slug.split('-')[0] if False else 'area_' + slug
    kms = ''.join(f'<li><div class="row">{E(n)}<span>{E(ui(L, "about_km").format(km=k))}</span></div><div class="bar"><i style="width:{max(4, round(k / 20 * 100))}%"></i></div></li>' for n, k in a['places'])
    sl = F['areas']
    idx = [x['slug'] for x in sl].index(slug)
    neigh = [sl[j] for j in (idx - 1, idx + 1) if 0 <= j < len(sl)]
    neigh_html = ''.join(f'<li><a class="chip" href="{lp(L, "areas/" + n["slug"] + "/")}">{E(c["areas"][n["slug"]]["nav"])} <small>{E(ui(L, "about_km").format(km=n["chip_km"]))}</small></a></li>' for n in neigh)
    biz = ld_business(L)
    area_node = {'@type': 'Service', 'name': ar['h1'], 'serviceType': 'Car repair and servicing', 'provider': {'@id': biz['@id']},
                 'areaServed': [{'@type': 'Place', 'name': n} for n, _ in a['places']], 'url': CFG.canon(L['prefix'] + path)}
    ld_ = ld(L, biz, area_node, ld_faq(ar['faqs']), ld_crumbs(L, crumb))
    body = f'''<body>
{header(L, path)}
<main id="main">
<section class="ptop"><div class="wrap">{crumbs(L, crumb)}
<div class="ptop-grid"><div>
<h1>{E(ar['h1'])}</h1>{''.join(f'<p class="lead">{E(p)}</p>' for p in ar['intro'])}
{cta_row(L, ar['wa'], ref)}
</div><div class="card" style="padding:20px"><h2 style="font-size:1.2rem">{E(ui(L, 'places_h'))}</h2><ul class="kms">{kms}</ul><p class="kms-note">{E(ui(L, 'straight_line'))}</p></div></div>
</div></section>
<section class="sec"><div class="wrap"><div class="sgrid"><div><h2>{E(ui(L, 'local_h'))}</h2>{''.join(f'<p>{E(p)}</p>' for p in ar['setting'])}
<h2 style="margin-top:28px">{E(ui(L, 'why_h'))}</h2>{''.join(f'<p>{E(p)}</p>' for p in ar['why'])}</div>
<div>{figure(L, 'h01', '(min-width:900px) 560px, 100vw')}</div></div></div></section>
<section class="band ice"><div class="wrap"><h2>{E(ui(L, 'services_here'))}</h2>{svc_list(L)}</div></section>
{faq_block(L, ar['faqs'])}
<section class="sec"><div class="wrap"><h2>{E(ui(L, 'areas_nearby'))}</h2><ul class="chips">{neigh_html}</ul>
<p style="margin-top:18px"><a href="{lp(L, '')}">{E(ui(L, 'breadcrumb_home'))}</a></p><p class="upd">{E(ui(L, 'updated'))}</p></div></section>
{end_cta(L, ar['wa'], ref + '_end')}
</main>
{footer(L, path)}'''
    return head(L, path, ar['title'], ar['meta'], ld_) + body


# ---------------------------------------------------------------- about / contact / articles / privacy
def page_about(L):
    c = C[L['code']]
    pg = c['pages']['about']
    path = 'about/'
    crumb = [(ui(L, 'breadcrumb_home'), ''), (ui(L, 'nav_about'), path)]
    secs = []
    for k, sec in enumerate(pg['sections']):
        media = media_html(L, sec.get('media'))
        text = f'<div><h2>{E(sec["h2"])}</h2>' + ''.join(f'<p>{E(p)}</p>' for p in sec['paras']) + ticks(sec.get('bullets')) + '</div>'
        secs.append(f'<section class="sec"><div class="wrap">' + (f'<div class="sgrid">{text}<div>{media}</div></div>' if media else f'<div class="prose">{text}</div>') + '</div></section>')
    ld_ = ld(L, ld_business(L), ld_crumbs(L, crumb))
    body = f'''<body>
{header(L, path)}
<main id="main">
<section class="ptop"><div class="wrap">{crumbs(L, crumb)}<div class="ptop-grid"><div>
<h1>{E(pg['h1'])}</h1><p class="kick">{E(pg['kicker'])}</p>{''.join(f'<p class="lead">{E(p)}</p>' for p in pg['intro'])}
{cta_row(L, c['wa_generic'], 'about')}</div>
<div class="frame stripe">{img(L, 'g02', '(min-width:1024px) 520px, 100vw').replace('<img', '<img style="object-position:50% 40%"', 1)}</div></div></div></section>
{''.join(secs)}
<section class="sec"><div class="wrap"><div class="card" style="padding:20px"><h2 style="font-size:1.2rem">{E(ui(L, 'hours_h'))}</h2><table class="hrs">{hours_rows(L)}</table>
<p style="margin:0">{E(ui(L, 'legal'))}<br>{E(ui(L, 'est'))}</p></div>
<h2 style="margin-top:34px">{E(c['home']['makes_h'])}</h2><ul class="chips">{''.join(f'<li><span class="chip">{E(m)}</span></li>' for m in F['makes'])}</ul></div></section>
{end_cta(L, c['wa_generic'], 'about_end')}
</main>
{footer(L, path)}'''
    return head(L, path, pg['title'], pg['meta'], ld_) + body


def page_contact(L):
    c = C[L['code']]
    pg = c['pages']['contact']
    path = 'contact/'
    crumb = [(ui(L, 'breadcrumb_home'), ''), (ui(L, 'nav_contact'), path)]
    ld_ = ld(L, ld_business(L), ld_crumbs(L, crumb))
    cards = f'''<ul class="cgrid">
<li><a class="wa" href="{E(wa_url(c['wa_contact']))}" target="_blank" rel="noopener" data-cta="whatsapp" data-ref="whatsapp_contact">{icon('wa')}<span><b>WhatsApp {E(F['whatsapp']['display'])}</b><small>{E(ui(L, 'contact_person'))}</small></span></a></li>
<li><a href="tel:{F['phone']['e164']}" data-cta="call" data-ref="call_contact">{icon('call')}<span><b>{E(ui(L, 'call'))} {E(F['phone']['display'])}</b><small>{E(ui(L, 'contact_person'))}</small></span></a></li>
<li><a href="tel:{F['phone2']['e164']}" data-cta="call" data-ref="call_second_line_contact">{icon('call')}<span><b>{E(ui(L, 'second_line'))} {E(F['phone2']['display'])}</b><small>{E(ui(L, 'contact_second_note'))}</small></span></a></li>
<li><a href="mailto:{F['email']}" data-cta="email" data-ref="email_contact">{icon('mail')}<span><b>{E(ui(L, 'email'))}</b><small>{E(F['email'])}</small></span></a></li>
<li><a href="{E(F['facebook'])}" target="_blank" rel="noopener" data-cta="facebook" data-ref="facebook_contact">{icon('fb')}<span><b>{E(ui(L, 'facebook'))}</b><small>Sheng Heng Auto Service Centre</small></span></a></li>
<li><a href="{E(F['directions_url'])}" target="_blank" rel="noopener" data-cta="directions" data-ref="directions_contact">{icon('nav')}<span><b>{E(ui(L, 'directions'))}</b><small>{E(F['address']['display'])}</small></span></a></li>
</ul>'''
    body = f'''<body>
{header(L, path)}
<main id="main">
<section class="ptop"><div class="wrap">{crumbs(L, crumb)}
<h1>{E(pg['h1'])}</h1><p class="kick">{E(pg['kicker'])}</p>{''.join(f'<p class="lead">{E(p)}</p>' for p in pg['intro'])}
{cards}
<div class="proof-links" style="margin-top:18px">{review_btn(L, 'review_contact')}<span class="aha" style="margin:0">{icon('card')}{E(ui(L, 'ahapay'))}</span></div>
</div></section>
<section class="band ice"><div class="wrap"><div class="sec-h"><h2>{E(c['home']['visit_h'])}</h2><p>{E(c['home']['visit_sub'])}</p></div>{visit_block(L, 'contact_visit')}</div></section>
</main>
{footer(L, path)}'''
    return head(L, path, pg['title'], pg['meta'], ld_) + body


def page_articles(L):
    c = C[L['code']]
    pg = c['pages']['articles']
    path = 'articles/'
    crumb = [(ui(L, 'breadcrumb_home'), ''), (ui(L, 'nav_articles'), path)]
    ld_ = ld(L, ld_business(L), ld_crumbs(L, crumb))
    body = f'''<body>
{header(L, path)}
<main id="main">
<section class="ptop"><div class="wrap">{crumbs(L, crumb)}
<h1>{E(pg['h1'])}</h1>{''.join(f'<p class="lead">{E(p)}</p>' for p in pg['intro'])}
<ul class="art-list" id="articles-list"></ul>
<div class="card empty"><p><b>{E(ui(L, 'articles_empty'))}</b></p>{cta_row(L, c['wa_generic'], 'articles')}<p style="margin:0"><a href="{lp(L, ORDER[0] + '/')}">{E(ui(L, 'articles_back'))}</a></p></div>
</div></section>
<section class="sec"><div class="wrap"><h2>{E(ui(L, 'all_services'))}</h2>{svc_list(L)}</div></section>
</main>
{footer(L, path)}'''
    return head(L, path, pg['title'], pg['meta'], ld_) + body


def page_privacy(L):
    path = 'privacy/'
    crumb = [(ui(L, 'breadcrumb_home'), ''), (ui(L, 'privacy'), path)]
    facts = {'name': F['name'], 'address': F['address']['display'], 'wa_link': wa_url(C[L['code']]['wa_generic']), 'wa_display': F['whatsapp']['display'],
             'tel_link': 'tel:' + F['phone']['e164'], 'tel_display': F['phone']['display'], 'email': F['email'], 'updated': '24 Nov 2026',
             'extras': ['maps', 'facebook']}
    main = PV.render_main(L['code'], 'my', facts)
    main = main.replace('data-cta="whatsapp_privacy" data-ref="privacy"', 'data-cta="whatsapp" data-ref="whatsapp_privacy"')
    main = main.replace('data-cta="call_privacy" data-ref="privacy"', 'data-cta="call" data-ref="call_privacy"')
    main = main.replace(f'<a href="mailto:{F["email"]}">', f'<a href="mailto:{F["email"]}" data-cta="email" data-ref="email_privacy">')
    ld_ = ld(L, ld_business(L), ld_crumbs(L, crumb))
    body = f'''<body>
{header(L, path)}
<main id="main"><section class="ptop"><div class="wrap">{crumbs(L, crumb)}<div class="prose">{main}</div></div></section></main>
{footer(L, path)}'''
    return head(L, path, ui(L, 'privacy_title'), ui(L, 'privacy_meta'), ld_) + body


# ---------------------------------------------------------------- main
def main():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(DIST, 'assets'))
    paths = [''] + [s + '/' for s in ORDER] + ['areas/' + a['slug'] + '/' for a in F['areas']] + ['about/', 'contact/', 'privacy/', 'articles/']
    for L in LANGS:
        pre = L['prefix']
        write(pre + 'index.html', page_home(L))
        for s in ORDER:
            write(pre + s + '/index.html', page_service(L, s))
        for a in F['areas']:
            write(pre + 'areas/' + a['slug'] + '/index.html', page_area(L, a))
        write(pre + 'about/index.html', page_about(L))
        write(pre + 'contact/index.html', page_contact(L))
        write(pre + 'articles/index.html', page_articles(L))
        write(pre + 'privacy/index.html', page_privacy(L))
    # sitemap.xml (articles hub is a preview shell: listed; preview articles stay noindex on the preview host)
    write('sitemap.xml', GL.sitemap_xml(CFG, paths, UPDATED))
    write('robots.txt', GL.robots_txt(CFG))
    en = C['en']
    lines = [GL.llms_header(CFG, F['name'], 'Continental and Asian car workshop at 17, Jalan Hang Lekir 12, Taman Industri Jaya, 81300 Skudai, Johor, Malaysia. Our workshop since 2010. ADAS calibration, ECU repair and coding, car keys, instrument clusters, gearbox overhaul, diagnostics and servicing. WhatsApp 016-335 2124 (Mr. Yaw). Mon-Sat 9:00am-6:00pm, Sunday closed. Pages in English, Bahasa Malaysia (/ms/) and Simplified Chinese (/zh/).'), '## Services']
    lines += [f'- [{en["services"][s]["title"]}]({CFG.canon(s + "/")}): {en["services"][s]["meta"]}' for s in ORDER]
    lines += ['', '## Areas (within 20 km)'] + [f'- [{en["areas"][a["slug"]]["title"]}]({CFG.canon("areas/" + a["slug"] + "/")})' for a in F['areas']]
    lines += ['', '## About', f'- [About]({CFG.canon("about/")})', f'- [Contact]({CFG.canon("contact/")})', f'- [Privacy]({CFG.canon("privacy/")})', '']
    write('llms.txt', '\n'.join(lines))
    write('site.webmanifest', json.dumps({'name': F['name'], 'short_name': 'Sheng Heng', 'start_url': u(''), 'display': 'standalone', 'background_color': '#ffffff', 'theme_color': '#1F4FA8',
                                          'icons': [{'src': u('images/brand/icon-sh-192.png'), 'sizes': '192x192', 'type': 'image/png'}]}, indent=1))
    # review helper
    import review_helper
    write('review.html', review_helper.render(True))  # review helper always noindex (standing rule)
    n = sum(1 for r, _, fs in os.walk(DIST) for f in fs if f.endswith('.html'))
    print('built', n, 'html files into', os.path.abspath(DIST))


if __name__ == '__main__':
    main()
