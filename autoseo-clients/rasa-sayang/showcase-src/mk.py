#!/usr/bin/env python3
"""Rasa Sayang: recent-jobs showcase snippets (home + 3 service pages + hub card) and the new air suspension page, 3 languages.
Run from a copy of the src folder: imports build.py for header/footer/CTA/schema so markup matches the live template."""
import os, sys, json, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, '/tmp/claude-0/w/a/b/src')
import build as B
from PIL import Image
E = html.escape
IMG = '/tmp/claude-0/w/img/'
OUT = '/tmp/claude-0/w/out/'
NEWSLUG = 'air-suspension-supercharger-replacement'
NEWPHOTO = 'volvo-xc90-t8-air-suspension-bay'

PH = {  # job -> ordered photo stems
    'erad': ['volvo-xc90-t8-erad-motor-bar-parts', 'volvo-xc90-t8-erad-motor-bar-lift', 'volvo-xc90-t8-erad-motor-bar-wide'],
    'air': ['volvo-xc90-t8-air-suspension-bay', 'volvo-xc90-t8-air-suspension-springs'],
    'iem': ['volvo-xc90-t8-iem-unit-lift', 'volvo-xc90-t8-iem-unit-pair'],
    'ferrari': ['ferrari-f8-service-rear-bay', 'ferrari-f8-service-oil-belts', 'ferrari-f8-service-dash-before-after', 'ferrari-f8-service-reset-before-after'],
    'porsche': ['porsche-gt3-engine-lift', 'porsche-gt3-engine-out', 'porsche-gt3-rear-underbody', 'porsche-gt3-front', 'porsche-gt3-front-left'],
}
SVC = {'erad': 'hybrid-ev', 'iem': 'hybrid-ev', 'air': 'NEW', 'ferrari': 'supercar', 'porsche': 'engine'}
ORDER = ['erad', 'air', 'iem', 'ferrari', 'porsche']

T = {}
T['en'] = dict(
    h2='Recent jobs from our workshop', sub='Five jobs from our bay, with the photos from the day. Tap a photo to enlarge it.',
    see='See', strip='Photos of this job', wa='WhatsApp us about your car',
    title={'erad': 'Volvo XC90 T8: ERAD motor and rear anti-roll bar replacement',
           'air': 'Volvo XC90 T8: full set air suspension and supercharger replacement',
           'iem': 'Volvo XC90 T8: IEM control unit replacement',
           'ferrari': 'Ferrari F8: car service and fan belt replacement',
           'porsche': 'Porsche GT3: engine repair'},
    text={'erad': 'A Volvo XC90 T8 on our lift with the rear subframe down on stands. The electric rear-axle (ERAD) motors, the rear anti-roll bars and the control arms are laid out on the floor, with Volvo transmission oil beside the motors.',
          'air': 'A Volvo XC90 T8 in the bay with a full set of air suspension laid out in its boxes beside the car, and a technician working on the next part.',
          'iem': 'A Volvo XC90 T8 on the lift, with two IEM control units laid out on a bench in front of the car, one of them on its Volvo box.',
          'ferrari': 'A red Ferrari F8 in the bay with Shell Helix Ultra 5W-40 engine oil, a Ferrari oil filter and two drive belts laid out behind it. The dash photos show the service display before and after: free service within 0 km and 0 days before, and 20112 km and 365 days after.',
          'porsche': 'A blue Porsche GT3 on a lift in the workshop with its rear section stripped, and the engine out of the car on a stand on the floor. Front shots of the car in the bay are alongside.'},
    alt={'erad': ['Volvo XC90 T8 ERAD motors, Volvo transmission oil and a rear anti-roll bar laid out on the workshop floor',
                  'Volvo XC90 T8 on the lift with the rear subframe on stands and the ERAD motors and anti-roll bars laid out below',
                  'Rear view of a Volvo XC90 T8 on a two-post lift with ERAD motors, anti-roll bars and control arms on the floor'],
         'air': ['Black Volvo XC90 T8 in the bay with a full set of air suspension in boxes and a technician at work',
                 'Two air suspension struts on their boxes beside a Volvo XC90 T8'],
         'iem': ['Volvo XC90 T8 on a lift with two IEM control units on a bench in front of it',
                 'Two Volvo XC90 T8 IEM control units side by side, one on a Volvo box'],
         'ferrari': ['Red Ferrari F8 with the engine cover open and service parts laid out behind it',
                     'Shell Helix Ultra 5W-40 oil, a Ferrari oil filter and two belts laid out for a Ferrari F8 service',
                     'Ferrari F8 dash before and after the service, the service display showing 0 km and 0 days before',
                     'Ferrari F8 dash before and after the service, the service display showing 20112 km and 365 days after'],
         'porsche': ['Blue Porsche GT3 on a lift with the rear section removed and the engine on the floor below',
                     'Porsche GT3 engine out of the car on a stand beside a lift in the workshop',
                     'Rear underbody of a blue Porsche GT3 on a lift with the engine removed',
                     'Blue Porsche GT3 front view in the workshop bay',
                     'Blue Porsche GT3 front-left view in the workshop']},
    page_h2={'hybrid-ev': 'Recent hybrid jobs: Volvo XC90 T8', 'engine': 'Recent engine job: Porsche GT3', 'supercar': 'Recent supercar jobs: Ferrari F8 and Porsche GT3'},
    new=dict(name='Air suspension and supercharger replacement', card='Full set air suspension and supercharger replacement.',
             title='Air Suspension and Supercharger Replacement, Shah Alam | Rasa Sayang Automotive',
             desc='Full set air suspension and supercharger replacement on a Volvo XC90 T8 by Rasa Sayang Automotive in Shah Alam and Subang Jaya. See the job photos.',
             h1='Air suspension and supercharger replacement in Shah Alam',
             lead='Full set air suspension and supercharger work, with the photos from a Volvo XC90 T8 job.',
             body=[('A full set of air suspension', 'On a Volvo XC90 T8 we replaced a full set of air suspension. The photos show the air suspension struts in their boxes beside the car and a technician at work in the bay.'),
                   ('Supercharger replacement', 'The same job included a supercharger replacement on the XC90 T8.'),
                   ('Send us your car', 'WhatsApp us the make, model, year and what the car is doing. We reply on WhatsApp.')],
             faq=[('Do you replace a full set of air suspension?', 'Yes. We replaced a full set of air suspension and the supercharger on a Volvo XC90 T8. The photos are on this page.'),
                  ('Which cars can I ask about?', 'WhatsApp us the make, model and year. We have worked on Volvo, BMW, Mercedes-Benz, Porsche, Rolls-Royce and Ferrari cars.')]),
    more_h='More services',
)
T['ms'] = dict(
    h2='Kerja terkini dari bengkel kami', sub='Lima kerja dari bengkel kami, bersama foto pada hari tersebut. Ketik foto untuk membesarkannya.',
    see='Lihat', strip='Foto kerja ini', wa='WhatsApp kami tentang kereta anda',
    title={'erad': 'Volvo XC90 T8: Penggantian motor ERAD dan bar anti-roll belakang',
           'air': 'Volvo XC90 T8: Penggantian set penuh suspensi udara dan supercharger',
           'iem': 'Volvo XC90 T8: Penggantian unit kawalan IEM',
           'ferrari': 'Ferrari F8: Servis kereta dan penggantian tali kipas',
           'porsche': 'Porsche GT3: Pembaikan enjin'},
    text={'erad': 'Sebuah Volvo XC90 T8 di atas lif kami dengan subframe belakang diturunkan ke atas penyokong. Motor gandar belakang elektrik (ERAD), bar anti-roll belakang dan lengan kawalan diletakkan di atas lantai, dengan minyak transmisi Volvo di sebelah motor.',
          'air': 'Sebuah Volvo XC90 T8 di dalam bay dengan set penuh suspensi udara diletakkan dalam kotaknya di sebelah kereta, dan seorang juruteknik sedang mengerjakan bahagian seterusnya.',
          'iem': 'Sebuah Volvo XC90 T8 di atas lif, dengan dua unit kawalan IEM diletakkan di atas bangku di hadapan kereta, satu daripadanya di atas kotak Volvo.',
          'ferrari': 'Sebuah Ferrari F8 merah di dalam bay dengan minyak enjin Shell Helix Ultra 5W-40, penapis minyak Ferrari dan dua tali pacu diletakkan di belakangnya. Foto papan pemuka menunjukkan paparan servis sebelum dan selepas: servis percuma dalam 0 km dan 0 hari sebelum, dan 20112 km serta 365 hari selepas.',
          'porsche': 'Sebuah Porsche GT3 biru di atas lif di bengkel dengan bahagian belakangnya dibuka, dan enjin dikeluarkan daripada kereta di atas pendiri di lantai. Foto bahagian hadapan kereta di dalam bay turut disertakan.'},
    alt={'erad': ['Motor ERAD Volvo XC90 T8, minyak transmisi Volvo dan bar anti-roll belakang diletakkan di lantai bengkel',
                  'Volvo XC90 T8 di atas lif dengan subframe belakang di atas penyokong, motor ERAD dan bar anti-roll diletakkan di bawah',
                  'Pandangan belakang Volvo XC90 T8 di atas lif dua tiang dengan motor ERAD, bar anti-roll dan lengan kawalan di lantai'],
         'air': ['Volvo XC90 T8 hitam di dalam bay dengan set penuh suspensi udara dalam kotak dan seorang juruteknik sedang bekerja',
                 'Dua strut suspensi udara di atas kotaknya di sebelah Volvo XC90 T8'],
         'iem': ['Volvo XC90 T8 di atas lif dengan dua unit kawalan IEM di atas bangku di hadapannya',
                 'Dua unit kawalan IEM Volvo XC90 T8 bersebelahan, satu di atas kotak Volvo'],
         'ferrari': ['Ferrari F8 merah dengan penutup enjin terbuka dan alat ganti servis diletakkan di belakangnya',
                     'Minyak Shell Helix Ultra 5W-40, penapis minyak Ferrari dan dua tali pacu diletakkan untuk servis Ferrari F8',
                     'Papan pemuka Ferrari F8 sebelum dan selepas servis, paparan servis menunjukkan 0 km dan 0 hari sebelum',
                     'Papan pemuka Ferrari F8 sebelum dan selepas servis, paparan servis menunjukkan 20112 km dan 365 hari selepas'],
         'porsche': ['Porsche GT3 biru di atas lif dengan bahagian belakang dibuka dan enjin di lantai di bawah',
                     'Enjin Porsche GT3 dikeluarkan daripada kereta di atas pendiri di sebelah lif di bengkel',
                     'Bahagian bawah belakang Porsche GT3 biru di atas lif dengan enjin dikeluarkan',
                     'Pandangan hadapan Porsche GT3 biru di dalam bay bengkel',
                     'Pandangan hadapan kiri Porsche GT3 biru di bengkel']},
    page_h2={'hybrid-ev': 'Kerja hibrid terkini: Volvo XC90 T8', 'engine': 'Kerja enjin terkini: Porsche GT3', 'supercar': 'Kerja kereta super terkini: Ferrari F8 dan Porsche GT3'},
    new=dict(name='Penggantian suspensi udara dan supercharger', card='Penggantian set penuh suspensi udara dan supercharger.',
             title='Penggantian Suspensi Udara dan Supercharger, Shah Alam | Rasa Sayang Automotive',
             desc='Penggantian set penuh suspensi udara dan supercharger pada Volvo XC90 T8 oleh Rasa Sayang Automotive di Shah Alam dan Subang Jaya. Lihat foto kerja.',
             h1='Penggantian suspensi udara dan supercharger di Shah Alam',
             lead='Kerja set penuh suspensi udara dan supercharger, bersama foto kerja Volvo XC90 T8.',
             body=[('Set penuh suspensi udara', 'Pada sebuah Volvo XC90 T8 kami menggantikan set penuh suspensi udara. Foto menunjukkan strut suspensi udara dalam kotaknya di sebelah kereta dan seorang juruteknik sedang bekerja di dalam bay.'),
                   ('Penggantian supercharger', 'Kerja yang sama termasuk penggantian supercharger pada XC90 T8.'),
                   ('Hantar kereta anda kepada kami', 'WhatsApp kami jenama, model, tahun dan apa yang berlaku pada kereta anda. Kami membalas di WhatsApp.')],
             faq=[('Adakah anda menggantikan set penuh suspensi udara?', 'Ya. Kami menggantikan set penuh suspensi udara dan supercharger pada sebuah Volvo XC90 T8. Foto-foto ada di halaman ini.'),
                  ('Kereta apa yang boleh saya tanya?', 'WhatsApp kami jenama, model dan tahun. Kami pernah mengerjakan kereta Volvo, BMW, Mercedes-Benz, Porsche, Rolls-Royce dan Ferrari.')]),
)
T['zh'] = dict(
    h2='我们车间近期的作业', sub='来自我们车间的五项作业，附当天的照片。点按照片可放大。',
    see='查看', strip='本次作业照片', wa='WhatsApp 咨询你的爱车',
    title={'erad': '沃尔沃 XC90 T8：更换 ERAD 电机及后防倾杆',
           'air': '沃尔沃 XC90 T8：更换整套空气悬挂及机械增压器',
           'iem': '沃尔沃 XC90 T8：更换 IEM 控制单元',
           'ferrari': '法拉利 F8：保养及更换风扇皮带',
           'porsche': '保时捷 GT3：发动机维修'},
    text={'erad': '一辆沃尔沃 XC90 T8 停在我们的举升机上，后副车架放下并架在支架上。后轴电动（ERAD）电机、后防倾杆和控制臂摆放在地面上，电机旁边是沃尔沃变速箱油。',
          'air': '一辆沃尔沃 XC90 T8 停在工位，整套空气悬挂装在原包装盒中摆放在车旁，技师正在处理下一个部件。',
          'iem': '一辆沃尔沃 XC90 T8 停在举升机上，两个 IEM 控制单元摆放在车前的工作台上，其中一个放在沃尔沃包装盒上。',
          'ferrari': '一辆红色法拉利 F8 停在工位，车后摆放着 Shell Helix Ultra 5W-40 机油、法拉利机油滤清器和两条传动皮带。仪表照片显示了保养前后的保养提示：保养前为 0 公里、0 天内免费保养，保养后为 20112 公里、365 天。',
          'porsche': '一辆蓝色保时捷 GT3 停在车间的举升机上，后部已拆开，发动机已从车上取下，放在地面的支架上。旁边还有这辆车停在工位时的车头照片。'},
    alt={'erad': ['沃尔沃 XC90 T8 的 ERAD 电机、沃尔沃变速箱油和后防倾杆摆放在车间地面上',
                  '沃尔沃 XC90 T8 停在举升机上，后副车架架在支架上，ERAD 电机和防倾杆摆放在下方',
                  '停在双柱举升机上的沃尔沃 XC90 T8 车尾，地面上是 ERAD 电机、防倾杆和控制臂'],
         'air': ['黑色沃尔沃 XC90 T8 停在工位，整套空气悬挂装在盒中，技师正在工作',
                 '沃尔沃 XC90 T8 旁盒子上的两支空气悬挂减震支柱'],
         'iem': ['沃尔沃 XC90 T8 停在举升机上，车前工作台上摆放着两个 IEM 控制单元',
                 '并排摆放的两个沃尔沃 XC90 T8 IEM 控制单元，其中一个放在沃尔沃包装盒上'],
         'ferrari': ['红色法拉利 F8 打开发动机盖，保养用料摆放在车后',
                     '为法拉利 F8 保养准备的 Shell Helix Ultra 5W-40 机油、法拉利机油滤清器和两条皮带',
                     '法拉利 F8 保养前后的仪表，保养前保养提示显示 0 公里、0 天',
                     '法拉利 F8 保养前后的仪表，保养后保养提示显示 20112 公里、365 天'],
         'porsche': ['蓝色保时捷 GT3 停在举升机上，后部已拆下，发动机放在下方地面',
                     '保时捷 GT3 的发动机已从车上取下，放在车间举升机旁的支架上',
                     '蓝色保时捷 GT3 停在举升机上，发动机已拆下，后部底盘外露',
                     '蓝色保时捷 GT3 在车间工位的车头照片',
                     '蓝色保时捷 GT3 在车间的左前方照片']},
    page_h2={'hybrid-ev': '近期混合动力作业：沃尔沃 XC90 T8', 'engine': '近期发动机作业：保时捷 GT3', 'supercar': '近期超跑作业：法拉利 F8 和保时捷 GT3'},
    new=dict(name='更换空气悬挂及机械增压器', card='更换整套空气悬挂及机械增压器。',
             title='更换空气悬挂及机械增压器，莎阿南 | Rasa Sayang Automotive',
             desc='Rasa Sayang Automotive 在莎阿南和梳邦再也为沃尔沃 XC90 T8 更换整套空气悬挂及机械增压器。查看作业照片。',
             h1='莎阿南更换空气悬挂及机械增压器',
             lead='整套空气悬挂及机械增压器作业，附沃尔沃 XC90 T8 的作业照片。',
             body=[('整套空气悬挂', '我们为一辆沃尔沃 XC90 T8 更换了整套空气悬挂。照片显示盒中的空气悬挂减震支柱摆在车旁，技师正在工位里工作。'),
                   ('更换机械增压器', '同一项作业还包括为这辆 XC90 T8 更换机械增压器。'),
                   ('把你的车告诉我们', '请用 WhatsApp 告诉我们品牌、车型、年份以及车辆的情况。我们会在 WhatsApp 上回复。')],
             faq=[('你们能更换整套空气悬挂吗？', '可以。我们为一辆沃尔沃 XC90 T8 更换了整套空气悬挂和机械增压器，照片在本页。'),
                  ('我可以咨询哪些车？', '请用 WhatsApp 告诉我们品牌、车型和年份。我们处理过沃尔沃、宝马、奔驰、保时捷、劳斯莱斯和法拉利。')]),
)

DIM = {}
for ks in PH.values():
    for k in ks:
        DIM[k] = Image.open(IMG + k + '.webp').size


def fix(h, L):
    depth = B.I18N.page_path(L, 'x/').count('/') - 1  # ms/x/ -> 2 slashes... handled below
    return h


def strip(job, t, idx0=0):
    parts = []
    for k, stem in enumerate(PH[job]):
        w, h = DIM[stem]
        alt = t['alt'][job][k]
        parts.append(f'<button type="button" class="fr-b" data-full="{B.img(stem)}" data-w="{w}" data-h="{h}" data-cap="{E(alt)}" '
                     f'aria-label="{E(B.S.UI["photo_open"])}: {E(alt)}"><img src="{B.img(stem)}" width="{w}" height="{h}" alt="{E(alt)}" loading="lazy" decoding="async"></button>')
    return f'<div class="strip" role="region" tabindex="0" aria-label="{E(t["strip"])}: {E(t["title"][job])}">{"".join(parts)}</div>'


def link_for(job, t):
    sid = SVC[job]
    if sid == 'NEW':
        name, slug = t['new']['name'], NEWSLUG
    else:
        s = next(x for x in B.S.SERVICES if x['id'] == sid)
        name, slug = s['name'], s['slug']
    return f'<a href="{B.pu("services/" + slug + "/")}">{E(t["see"])}: {E(name)}</a>'


def sjob(job, t, n=None, link=True, h='h3'):
    num = f'<span class="sj-n">{n:02d}</span>' if n else ''
    ln = f'<p class="sj-l">{link_for(job, t)}</p>' if link else ''
    return (f'<article class="sjob" id="job-{job}"><div class="sj-t">{num}<{h} class="sj-h">{E(t["title"][job])}</{h}><p>{E(t["text"][job])}</p>{ln}</div>'
            f'{strip(job, t)}</article>')


CSSLINK = '<link rel="stylesheet" href="@@B@@/assets/showcase.css?v=1">'


def show_home(t):
    return (f'<section class="sec show" id="recent-jobs">{CSSLINK}<div class="wrap"><h2>{E(t["h2"])}</h2><p class="sub">{E(t["sub"])}</p>'
            + ''.join(sjob(j, t, i + 1) for i, j in enumerate(ORDER))
            + f'<div class="act">{B.wa("jobs", t["wa"])}</div></div></section>')


def show_svc(sid, t):
    jobs = [j for j in ORDER if SVC[j] == sid]
    if sid == 'supercar':
        jobs = ['ferrari', 'porsche']
    return (f'<section class="sec show">{CSSLINK}<div class="wrap"><h2>{E(t["page_h2"][sid])}</h2><p class="sub">{E(t["sub"])}</p>'
            + ''.join(sjob(j, t, None, link=(j == 'porsche' and sid == 'supercar')) for j in jobs) + '</div></section>')


def card(t, hl):
    n = t['new']
    B.PHOTOS[NEWPHOTO] = (DIM[NEWPHOTO][0], DIM[NEWPHOTO][1], DIM[NEWPHOTO][0], DIM[NEWPHOTO][1])
    B.S.CAPTIONS[NEWPHOTO] = t['alt']['air'][0]
    s = dict(slug=NEWSLUG, name=n['name'], card_line=n['card'], photo=NEWPHOTO)
    return B.spec_strip([s], hl).replace('<span class="sp-n">01</span>', '<span class="sp-n">06</span>')[len('<ol class="spec">'):-len('</ol>')]


def newpage(t):
    n = t['new']
    path = f'services/{NEWSLUG}/'
    trail = [(B.S.UI['nav_home'], ''), (B.S.UI['nav_services'], 'services/'), (n['name'], path)]
    blocks = ''.join(f'<h2>{E(h)}</h2><p>{E(p)}</p>' for h, p in n['body'])
    cta = f'<div class="act">{B.wa("service_air_suspension", B.S.UI["wa_btn_long"])}{B.call("service_air_suspension", B.S.UI["call_btn"])}</div>'
    others = ''.join(f'<a href="{B.pu("services/" + o["slug"] + "/")}">{E(o["name"])}</a>' for o in B.S.SERVICES)
    body = (B.page_head(n['h1'], n['lead'], trail)
            + f'<section class="sec"><div class="wrap narrow"><div class="prose">{blocks}{cta}</div></div></section>'
            + f'<section class="sec show">{CSSLINK}<div class="wrap">{sjob("air", t, None, link=False, h="h2")}</div></section>'
            + B.faq_block(n['faq'], B.S.UI['faq_h2'])
            + f'<section class="sec more"><div class="wrap"><h2>{E(B.S.UI["related"])}</h2><nav class="tabs" aria-label="{E(B.S.UI["related"])}">{others}</nav></div></section>'
            + B.ask_block('service_air_suspension_end'))
    graph = [B.business(), B.crumbs(trail),
             {'@type': 'Service', 'name': n['name'], 'serviceType': n['name'], 'description': n['desc'], 'url': B.pabs(path),
              'provider': {'@id': B.BIZ_ID}, 'areaServed': [{'@type': 'City', 'name': c} for c in B.F['service_area']]},
             B.faqld(n['faq'])]
    return B.page(path, n['title'], n['desc'], graph, body, 'services/')


def finish(h, L, p=''):
    depth = B.I18N.page_path(L, p).count('/')
    return h.replace('@@B@@/', '../' * depth if depth else './').replace('@@B@@', '..' if depth else '.')


os.makedirs(OUT, exist_ok=True)
for L in B.I18N.LANGS:
    code = L['code']
    B.S, B.L = B.STRINGS[code], L
    t = T[code]
    d = OUT + code + '/'
    os.makedirs(d, exist_ok=True)
    w = lambda name, h, p='': open(d + name, 'w', encoding='utf8').write(finish(h, L, p))
    w('home_li.html', card(t, 'h3'))
    w('home_show.html', show_home(t))
    w('hub_li.html', card(t, 'h2'), 'services/')
    for sid in ('hybrid-ev', 'engine', 'supercar'):
        w(f'svc_{sid}.html', show_svc(sid, t), 'services/x/')
    # new page: services lists include the new service
    B.S.SERVICES = list(B.S.SERVICES) + [dict(id='air-suspension', slug=NEWSLUG, name=t['new']['name'], card_line=t['new']['card'], photo=NEWPHOTO)]
    w('newpage.html', newpage(t), f'services/{NEWSLUG}/')
    B.S.SERVICES = B.S.SERVICES[:-1]
    json.dump({'name': t['new']['name']}, open(d + 'meta.json', 'w'), ensure_ascii=False)
print('ok')
