"""Hon Win Motor mini-site inside sgcarworkshop.sg (paid Premium client, Edwin 21 Nov 2026).
Called from build.build() after the paid listing pages: replaces the standard listing page at workshops/hon-win-motor/
with the client's profile and adds 4 service pages, an areas hub and 10 nearby-area pages. Own look (assets/hw/hw.css),
own header/footer instead of the directory's (Edwin 21 Nov 2026: paid client, less confusing), with a small link back to the directory. Taps are counted by assets/hw/p1-cta.js (Controller Client slug hon-win-motor)."""
import json, math, os, shutil
from urllib.parse import quote
import hw_content as C
import hw_articles as A

HERE = os.path.dirname(os.path.abspath(__file__))
LLMS = []   # llms.txt lines, read by build.py
PG = ['']   # current page path, for data-page on tap links


def km(lat, lng):
    p = math.radians
    x = p(lng - C.LNG) * math.cos(p((lat + C.LAT) / 2))
    y = p(lat - C.LAT)
    return 6371 * math.hypot(x, y)


def km_txt(a):
    d = km(a['lat'], a['lng'])
    return 'about %s km' % (('%.1f' % d).rstrip('0').rstrip('.') if d < 3 else '%d' % round(d))


def run(B):
    E, pre, page, img_tag, abs_url, crumbs = B.E, B.pre, B.page, B.img_tag, B.abs_url, B.crumbs
    e = B.BY_SLUG[C.SLUG]
    trail0 = []   # Edwin 21 Nov 2026: breadcrumbs stay inside the mini-site (no links back to directory region/estate pages)

    def crumbs(depth, trail):
        parts, ld = [], []
        for i, (lab, rel) in enumerate(trail):
            last = i == len(trail) - 1
            parts.append(E(lab) if last else '<a href="%s%s">%s</a>' % (pre(depth), rel, E(lab)))
            ld.append({'@type': 'ListItem', 'position': i + 1, 'name': lab, 'item': abs_url(rel)} if not last else {'@type': 'ListItem', 'position': i + 1, 'name': lab})
        return '<nav class="crumbs hw-crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts), {'@type': 'BreadcrumbList', 'itemListElement': ld}
    addr = '%s, Singapore %s' % (C.STREET, C.POSTAL)
    dirs = 'https://www.google.com/maps/dir/?api=1&destination=%s&destination_place_id=%s' % (quote('%s, %s' % (C.NAME, addr)), C.PLACE_ID)

    def wa(topic, ref, label='WhatsApp us', cls='hw-btn hw-wa'):
        msg = 'Hi Hon Win Motor, I found you on SG Car Workshop. I would like to ask about %s for my car.' % topic
        return '<a class="%s" href="https://wa.me/%s?text=%s" target="_blank" rel="noopener" data-ref="%s" data-cta="whatsapp_dir_%s" data-tier="premium_leadgen" data-page="/%s">%s%s</a>' % (cls, C.WA, quote(msg), ref, C.SLUG, PG[0], B.ic('wa'), E(label))

    def call(ref, label=None, cls='hw-btn hw-call'):
        return '<a class="%s" href="tel:%s" data-ref="%s" data-cta="call_dir_%s" data-tier="premium_leadgen" data-page="/%s">%s%s</a>' % (cls, C.TEL, ref, C.SLUG, PG[0], B.ic('phone'), E(label or 'Call %s' % C.TEL_SHOW))

    def bar(topic):
        return '<div class="wabar hw-bar" role="region" aria-label="Contact Hon Win Motor">%s%s</div>' % (wa(topic, 'sticky', 'WhatsApp'), call('sticky', 'Call'))

    def head_extra(depth):
        p = pre(depth)
        return ('<link rel="preload" href="%sassets/hw/barlow-semi-condensed-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>'
                '<link rel="stylesheet" href="%sassets/hw/hw.css?v=%s">' % (p, p, CSS_V))

    def tail(depth):
        return '<script src="%sassets/hw/p1-cta.js?v=%s" defer></script>' % (pre(depth), JS_V)

    NAV = [('', 'Profile')] + [(sv['slug'] + '/', sv['nav']) for sv in C.SERVICES] + [('areas/', 'Areas'), ('articles/', 'Articles')]

    def hw_head(path):
        depth = path.count('/'); p = pre(depth); home = p + C.BASE_PATH
        rest = path[len(C.BASE_PATH):]
        cur = rest.split('/')[0] + '/' if rest.startswith(('areas/', 'articles/')) else rest
        li = ''.join('<li><a href="%s%s"%s>%s</a></li>' % (home, h, ' aria-current="page"' if h == cur else '', E(t)) for h, t in NAV)
        return ('<a class="skip" href="#main">Skip to content</a><header class="hw hw-top"><div class="hw-w hw-top-bar">'
                '<a class="hw-brand" href="%s"><span>Hon Win Motor</span><small>Car workshop, 6 Defu Lane 10</small></a>%s</div>'
                '<nav class="hw-nav" aria-label="Hon Win Motor pages"><ul class="hw-w">%s</ul></nav></header>') % (
            home, call('header', 'Call', 'hw-top-call'), li)

    def hw_foot(path):
        depth = path.count('/'); p = pre(depth); home = p + C.BASE_PATH
        li = ''.join('<li><a href="%s%s">%s</a></li>' % (home, h, E(t)) for h, t in NAV)
        hrs = '<br>'.join('%s: %s' % (E(d), E(t)) for d, t in C.HOURS)
        return ('<footer class="hw hw-ft"><div class="hw-w hw-ft-cols"><div><h2>Hon Win Motor</h2><p>%s<br>Singapore %s</p>'
                '<p><a href="tel:%s" data-ref="footer" data-cta="call_dir_%s" data-tier="premium_leadgen" data-page="/%s">%s</a> · <a href="mailto:%s">%s</a></p></div>'
                '<div><h2>Opening hours</h2><p>%s</p><p><a href="%s" target="_blank" rel="noopener">Directions on Google Maps</a></p></div>'
                '<div><h2>Pages</h2><ul>%s</ul></div></div>'
                '<div class="hw-w hw-ft-dir"><p>Featured (paid) listing on <a href="%s">SG Car Workshop</a>, the Singapore car workshop directory. '
                '<a href="%slist-your-workshop/#remove">Remove my listing</a> · <a href="%sterms/">Terms</a> · <a href="%sprivacy/">Privacy</a></p></div></footer>') % (
            E(C.STREET), C.POSTAL, C.TEL, C.SLUG, PG[0], E(C.TEL_SHOW), E(C.EMAIL), E(C.EMAIL), hrs, E(dirs, True), li, p, p, p, p)

    def subnav(depth, cur):
        return ''

    def plate():
        return '<p class="hw-plate"><span class="hw-unit">#01-544</span><span>6 Defu Lane 10<br>Singapore %s</span></p>' % C.POSTAL

    def faq_html(faqs):
        return '<div class="hw-faq">%s</div>' % ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in faqs)

    def faq_ld(faqs):
        return {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faqs]}

    def biz_ld(url_profile):
        ld = B.ld_business(e, url_profile)
        ld['@id'] = url_profile + '#business'
        ld['alternateName'] = C.TRADING
        ld['email'] = C.EMAIL
        ld['image'] = [B.BASE + 'assets/img/hw/workshop-front.webp', B.BASE + 'assets/img/hw/og.jpg']
        ld['areaServed'] = [{'@type': 'Place', 'name': 'Defu Industrial Estate, Singapore'}] + [{'@type': 'Place', 'name': a['name'] + ', Singapore'} for a in C.AREAS]
        ld.pop('geo', None)   # ld_business may already add geo (22 Nov 2026); keep the mini-site's own pin in its old position
        ld['geo'] = {'@type': 'GeoCoordinates', 'latitude': C.LAT, 'longitude': C.LNG}
        ld['paymentAccepted'] = 'Cash, scan to pay, bank transfer, Atome'
        ld['makesOffer'] = [{'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': s['h1'], 'url': B.BASE + C.BASE_PATH + s['slug'] + '/'}} for s in C.SERVICES]
        return ld

    def svc_ld(s, url):
        return {'@context': 'https://schema.org', '@type': 'Service', 'name': s['h1'], 'serviceType': s['short'], 'url': url,
                'provider': {'@id': B.BASE + C.BASE_PATH + '#business'}, 'areaServed': [{'@type': 'Place', 'name': a['name'] + ', Singapore'} for a in C.AREAS]}

    def hours_html():
        return '<table class="hw-hours"><tbody>%s</tbody></table><p class="hw-fine">%s</p>' % (
            ''.join('<tr><th scope="row">%s</th><td>%s</td></tr>' % (E(d), E(t)) for d, t in C.HOURS), E(C.HOURS_NOTE))

    def visit_block(depth, ref):
        return ('<section class="hw-sec hw-visit" id="visit"><div class="hw-w hw-split"><div><h2>Visit the workshop</h2>%s%s'
                '<p class="hw-acts"><a class="hw-btn hw-ghost" href="%s" target="_blank" rel="noopener" data-ref="%s">%sDirections</a>%s</p></div>'
                '<div><h3>Opening hours</h3>%s<h3>Payment</h3><p>%s</p></div></div></section>') % (
            plate(), '<p>Defu Industrial Estate, Hougang. Look for the red Hon Win Motor Trading signboard. Email <a href="mailto:%s">%s</a>.</p>' % (C.EMAIL, C.EMAIL),
            E(dirs), ref, B.ic('pin'), call(ref, cls='hw-btn hw-ghost'), hours_html(), E(C.PAY))

    def reviews_block(ref):
        return ('<section class="hw-sec hw-rev"><div class="hw-w"><h2>What drivers say</h2><p>%s</p>'
                '<p><a class="hw-btn hw-ghost" href="%s" target="_blank" rel="noopener" data-ref="%s">See our reviews on Google</a></p></div></section>') % (E(C.REVIEW_THEMES), E(C.GOOGLE_URL), ref)

    def cta_band(topic, ref, text='Tell us your car model and what you need. We reply on WhatsApp.'):
        return '<section class="hw-band"><div class="hw-w"><h2>Get a quote on WhatsApp</h2><p>%s</p><p class="hw-acts">%s%s</p></div></section>' % (E(text), wa(topic, ref, 'WhatsApp 9171 8466'), call(ref, 'Call us', 'hw-btn hw-call'))

    def paid_note():
        return '<p class="hw-paid w">Featured (paid) listing on SG Car Workshop. Details from the workshop\'s own website and Google profile.</p>'

    def areas_list(depth, cls='hw-areas'):
        p = pre(depth) + C.BASE_PATH + 'areas/'
        return '<ul class="%s">%s</ul>' % (cls, ''.join('<li><a href="%s%s/"><b>%s</b><span>%s</span></a></li>' % (p, a['slug'], E(a['name']), km_txt(a)) for a in sorted(C.AREAS, key=lambda a: km(a['lat'], a['lng']))))

    def art_url(a, depth):
        return pre(depth) + C.BASE_PATH + 'articles/%s/' % a['slug']

    def nice_date(d):
        import datetime
        return datetime.date.fromisoformat(d).strftime('%-d %B %Y')

    def art_cards(depth, items):
        return '<ul class="hw-cards hw-arts">%s</ul>' % ''.join(
            '<li><a href="%s"><figure>%s</figure><h3>%s</h3><p>%s</p><time datetime="%s">%s</time></a></li>' % (
                art_url(a, depth), img_tag(a['img'], a['alt'], depth), E(a['h1']), E(a['card']), a['date'], nice_date(a['date'])) for a in items)

    def arts_for(slug):
        return [a for a in sorted(A.ARTICLES, key=lambda a: a['date'], reverse=True) if a['maps'] == slug]

    def svc_cards(depth):
        p = pre(depth) + C.BASE_PATH
        return '<ul class="hw-cards">%s</ul>' % ''.join(
            '<li><a href="%s%s/"><figure>%s</figure><h3>%s</h3><p>%s</p></a></li>' % (p, s['slug'], img_tag(s['photo'][0], s['photo'][1], depth), E(s['h1'].split(' in ')[0].split(':')[0]), E(s['card'])) for s in C.SERVICES)

    # ------------------------------------------------ profile
    path = C.BASE_PATH
    PG[0] = path
    depth = path.count('/')
    url = abs_url(path)
    cr, crld = crumbs(depth, trail0 + [(C.NAME, None)])
    gallery = ''.join('<figure>%s<figcaption>%s</figcaption></figure>' % (img_tag(ph['f'], ph['alt'], depth), E(ph['cap'])) for ph in e['photos'][1:])
    body = f'''<div class="hw">
{subnav(depth, '')}
<section class="hw-hero"><div class="hw-hero-img">{img_tag('hw/workshop-front.webp', 'Hon Win Motor Trading signboard above the workshop at 6 Defu Lane 10, Defu Industrial Estate', depth, lazy=False)}</div>
<div class="hw-w hw-hero-txt"><h1>Hon Win Motor, Defu Lane</h1><p class="hw-line">Servicing, repairs, aircon and accident claims for your car, in Hougang.</p>
<p class="hw-acts">{wa('servicing or a repair', 'hero', 'WhatsApp us now')}{call('hero', 'Call 9171 8466', 'hw-btn hw-call hw-on-dark')}</p>{plate()}</div></section>
<div class="hw-w">{cr}</div>
<section class="hw-sec"><div class="hw-w"><h2>What we fix</h2><p class="hw-lead">A full workshop for passenger cars: {E(C.MAKES)}</p>{svc_cards(depth)}
<h3 class="hw-h3">Also at our workshop</h3><dl class="hw-extras">{''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (E(t), E(d)) for t, d in C.EXTRAS)}</dl></div></section>
<section class="hw-sec hw-steps-sec"><div class="hw-w"><h2>How a job goes</h2><ol class="hw-steps">{''.join('<li><b>%s</b><span>%s</span></li>' % (E(t), E(d)) for t, d in C.STEPS)}</ol></div></section>
<section class="hw-sec hw-team"><div class="hw-w hw-split"><div><h2>The people on the tools</h2><p>Our mechanics have over 20 years of experience. Walk-ins are welcome, and we only replace what actually needs replacing.</p>
<ul class="hw-crew">{''.join('<li><b>%s</b><span>%s</span></li>' % (E(n), E(r)) for n, r in C.TEAM)}</ul></div>
<figure class="hw-team-img">{img_tag('hw/mechanic-engine-bay.webp', 'Hon Win Motor mechanic working in the engine bay of a red Hyundai', depth)}</figure></div></section>
<section class="hw-sec"><div class="hw-w"><h2>Inside the workshop</h2><div class="hw-gal">{gallery}</div></div></section>
{reviews_block('reviews')}
<section class="hw-sec"><div class="hw-w"><h2>Areas we serve</h2><p>We are in Defu Industrial Estate, Hougang. These towns are within about 8 km of the workshop.</p>{areas_list(depth)}</div></section>
<section class="hw-sec"><div class="hw-w"><h2>Latest articles</h2>{art_cards(depth, sorted(A.ARTICLES, key=lambda a: a['date'], reverse=True)[:3])}<p><a href="articles/">All articles</a></p></div></section>
{visit_block(depth, 'visit')}
<div class="hw-map w"><iframe src="{E(B.embed_url(e))}" title="Map of Hon Win Motor, 6 Defu Lane 10" width="100%" height="300" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe></div>
<section class="hw-sec"><div class="hw-w"><h2>Questions</h2>{faq_html(e['faqs'])}</div></section>
{cta_band('servicing or a repair', 'band')}
{paid_note()}
</div>'''
    page(path, e['title'], e['desc'], body, [biz_ld(url), faq_ld(e['faqs']), dict(crld, **{'@context': 'https://schema.org'})],
         og='hw/og.jpg', bar=bar('servicing or a repair'), h1='Hon Win Motor, Defu Lane', head_extra=head_extra(depth), tail=tail(depth), chrome=(hw_head(path), hw_foot(path)))
    LLMS.append('- [Hon Win Motor](%s): car workshop at 6 Defu Lane 10, Hougang (Featured, paid). Servicing, engine, electrical and gearbox repairs, aircon, accident repairs and insurance claims. WhatsApp +65 9171 8466.' % url)

    # ------------------------------------------------ service pages
    for s in C.SERVICES:
        path = C.BASE_PATH + s['slug'] + '/'
        PG[0] = path
        depth = path.count('/')
        url = abs_url(path)
        cr, crld = crumbs(depth, trail0 + [(C.NAME, C.BASE_PATH), (s['short'], None)])
        secs = ''.join('<section class="hw-sec"><div class="hw-w hw-narrow"><h2>%s</h2>%s</div></section>' % (E(h), ''.join('<p>%s</p>' % E(t) for t in ps)) for h, ps in s['sections'])
        others = ''.join('<li><a href="../%s/">%s</a></li>' % (o['slug'], E(o['h1'].split(' in ')[0].split(':')[0])) for o in C.SERVICES if o is not s)
        body = f'''<div class="hw">
{subnav(depth, s['slug'] + '/')}
<section class="hw-shero"><div class="hw-w hw-split"><div><h1>{E(s['h1'])}</h1><p class="hw-line">{E(s['line'])}</p><p class="hw-acts">{wa(s['wa'], 'hero', 'WhatsApp us now')}{call('hero', None, 'hw-btn hw-call')}</p></div>
<figure class="hw-shero-img">{img_tag(s['photo'][0], s['photo'][1], depth, lazy=False)}</figure></div></section>
<div class="hw-w">{cr}</div>
<section class="hw-sec"><div class="hw-w hw-narrow"><div class="hw-job"><h2>{E(s['job_title'])}</h2><ul>{''.join('<li>%s</li>' % E(j) for j in s['job'])}</ul><p class="hw-job-note">{E(s['job_note'])}</p></div></div></section>
{secs}
{cta_band(s['wa'], 'band')}
<section class="hw-sec"><div class="hw-w hw-narrow"><h2>Questions</h2>{faq_html(s['faqs'])}</div></section>
<section class="hw-sec"><div class="hw-w"><h2>{E(s['short'])} near you</h2><p>We are within about 8 km of these towns.</p>{areas_list(depth)}<h3 class="hw-h3">Other services</h3><ul class="hw-links">{others}</ul>{('<h3 class="hw-h3">Read more</h3><ul class="hw-links">%s</ul>' % ''.join('<li><a href="../articles/%s/">%s</a></li>' % (a['slug'], E(a['h1'])) for a in arts_for(s['slug']))) if arts_for(s['slug']) else ''}</div></section>
{visit_block(depth, 'visit')}
{paid_note()}
</div>'''
        page(path, s['title'], s['desc'], body, [svc_ld(s, url), faq_ld(s['faqs']), dict(crld, **{'@context': 'https://schema.org'})],
             og='hw/og.jpg', bar=bar(s['wa']), h1=s['h1'], head_extra=head_extra(depth), tail=tail(depth), chrome=(hw_head(path), hw_foot(path)))
        LLMS.append('- [%s](%s): %s' % (s['h1'], url, s['desc']))

    # ------------------------------------------------ areas hub
    path = C.BASE_PATH + 'areas/'
    PG[0] = path
    depth = path.count('/')
    url = abs_url(path)
    cr, crld = crumbs(depth, trail0 + [(C.NAME, C.BASE_PATH), ('Areas', None)])
    body = f'''<div class="hw">
{subnav(depth, 'areas/')}
<section class="hw-shero"><div class="hw-w"><h1>Car workshop near you, from Defu Lane</h1><p class="hw-line">Towns within about 8 km of Hon Win Motor, nearest first.</p><p class="hw-acts">{wa('servicing or a repair', 'hero', 'WhatsApp us now')}</p></div></section>
<div class="hw-w">{cr}</div>
<section class="hw-sec"><div class="hw-w">{areas_list(depth, 'hw-areas hw-areas-big')}<p class="hw-fine">Distances are straight-line from the workshop to each town's MRT station.</p></div></section>
{visit_block(depth, 'visit')}
{paid_note()}
</div>'''
    page(path, 'Hon Win Motor Areas: Hougang, Sengkang, Tampines & More', 'Hon Win Motor at Defu Lane serves drivers within about 8 km: Hougang, Kovan, Serangoon, Sengkang, Punggol, Paya Lebar, Ubi, Bedok North, Tampines, Ang Mo Kio.',
         body, [dict(crld, **{'@context': 'https://schema.org'})], og='hw/og.jpg', bar=bar('servicing or a repair'), h1='Car workshop near you, from Defu Lane', head_extra=head_extra(depth), tail=tail(depth), chrome=(hw_head(path), hw_foot(path)))

    # ------------------------------------------------ area pages
    for a in C.AREAS:
        path = C.BASE_PATH + 'areas/%s/' % a['slug']
        PG[0] = path
        depth = path.count('/')
        url = abs_url(path)
        dist = km_txt(a)
        cr, crld = crumbs(depth, trail0 + [(C.NAME, C.BASE_PATH), ('Areas', C.BASE_PATH + 'areas/'), (a['name'], None)])
        frm = 'https://www.google.com/maps/dir/?api=1&origin=%s&destination=%s&destination_place_id=%s' % (quote(a['name'] + ' MRT, Singapore'), quote('%s, %s' % (C.NAME, addr)), C.PLACE_ID)
        svc = ''.join('<article class="hw-asvc"><h2>%s near %s</h2><p>%s</p><p><a href="../../%s/">More about %s</a></p></article>' % (
            E(s['h1'].split(' in ')[0].split(':')[0]), E(a['name']), E(s['card'] + ' ' + s['job_note']), s['slug'], E(s['short'].lower())) for s in C.SERVICES)
        faqs = [('How far is Hon Win Motor from %s?' % a['name'], 'Our workshop at 6 Defu Lane 10 is %s from %s in a straight line.' % (dist, a['mrt'])),
                ('Can I leave my car and go home?', a['local'] + ' WhatsApp 9171 8466 to arrange a time.'),
                ('My car broke down in %s. Can you help?' % a['name'], 'WhatsApp or call 9171 8466. Towing is free when the repair is done at our workshop.'),
                ('Are you open on Saturday?', 'Yes, from 10am to 3pm. Monday to Friday we are open from 10am to 7pm, and we are closed on Sunday.')]
        near = [o for o in sorted(C.AREAS, key=lambda o: math.hypot(o['lat'] - a['lat'], o['lng'] - a['lng'])) if o is not a][:3]
        title = B.fit_title('Car Workshop near %s | Hon Win Motor, Defu Lane' % a['name'], 'Car Workshop near %s | Hon Win Motor' % a['name'])
        desc = 'Car servicing, repairs, aircon and accident claims near %s: Hon Win Motor, 6 Defu Lane 10, %s away. WhatsApp 9171 8466.' % (a['name'], dist)
        body = f'''<div class="hw">
{subnav(depth, 'areas/')}
<section class="hw-shero"><div class="hw-w hw-split"><div><h1>Car workshop near {E(a['name'])}</h1><p class="hw-line">Hon Win Motor is {E(dist)} from {E(a['name'])}, in Defu Lane.</p><p class="hw-acts">{wa('servicing or a repair (I am in %s)' % a['name'], 'hero', 'WhatsApp us now')}<a class="hw-btn hw-ghost" href="{E(frm)}" target="_blank" rel="noopener" data-ref="hero">{B.ic('pin')}Directions from {E(a['name'])}</a></p></div>
<figure class="hw-shero-img">{img_tag('hw/workshop-front.webp', 'Hon Win Motor Trading workshop at 6 Defu Lane 10, near ' + a['name'], depth, lazy=False)}</figure></div></section>
<div class="hw-w">{cr}</div>
<section class="hw-sec"><div class="hw-w hw-narrow"><h2>From {E(a['name'])} to Defu Lane</h2><p>{E(a['intro'])}</p><p>{E(a['local'])}</p><p class="hw-dist"><b>{E(dist)}</b> from {E(a['mrt'])} to our workshop, in a straight line.</p></div></section>
<section class="hw-sec"><div class="hw-w"><div class="hw-asvcs">{svc}</div></div></section>
{cta_band('servicing or a repair (I am in %s)' % a['name'], 'band', 'Tell us your car model, what you need and that you are in %s. We reply on WhatsApp.' % a['name'])}
<section class="hw-sec"><div class="hw-w hw-narrow"><h2>Questions from {E(a['name'])} drivers</h2>{faq_html(faqs)}</div></section>
<section class="hw-sec"><div class="hw-w"><h2>Nearby areas</h2><ul class="hw-links">{''.join('<li><a href="../%s/">Car workshop near %s</a></li>' % (o['slug'], E(o['name'])) for o in near)}<li><a href="../">All areas</a></li></ul></div></section>
{visit_block(depth, 'visit')}
{paid_note()}
</div>'''
        page(path, title, desc, body, [biz_ld(B.BASE + C.BASE_PATH), faq_ld(faqs), dict(crld, **{'@context': 'https://schema.org'})],
             og='hw/og.jpg', bar=bar('servicing or a repair (I am in %s)' % a['name']), h1='Car workshop near %s' % a['name'], head_extra=head_extra(depth), tail=tail(depth), chrome=(hw_head(path), hw_foot(path)))
        LLMS.append('- [Car workshop near %s: Hon Win Motor](%s): %s' % (a['name'], url, desc))

    # ------------------------------------------------ articles (Edwin 21 Nov 2026: one every 2 days; hw_articles.py)
    AL = sorted(A.ARTICLES, key=lambda a: a['date'], reverse=True)
    path = C.BASE_PATH + 'articles/'
    PG[0] = path
    depth = path.count('/')
    url = abs_url(path)
    cr, crld = crumbs(depth, [(C.NAME, C.BASE_PATH), ('Articles', None)])
    body = f'''<div class="hw">
<section class="hw-shero"><div class="hw-w"><h1>Car care articles from Defu Lane</h1><p class="hw-line">Plain answers from our workshop for drivers in Hougang, Sengkang, Punggol and nearby. A new article every 2 days.</p></div></section>
<div class="hw-w">{cr}</div>
<section class="hw-sec"><div class="hw-w">{art_cards(depth, AL)}</div></section>
{cta_band('servicing or a repair', 'band')}
{paid_note()}
</div>'''
    page(path, 'Car Care Articles from Defu Lane, Hougang | Hon Win Motor', 'Articles from Hon Win Motor, a car workshop at Defu Lane, Hougang: used car checks, accidents and claims, gearbox repairs and more.',
         body, [dict(crld, **{'@context': 'https://schema.org'})], og='hw/og.jpg', bar=bar('servicing or a repair'), h1='Car care articles from Defu Lane', head_extra=head_extra(depth), tail=tail(depth), chrome=(hw_head(path), hw_foot(path)))
    LLMS.append('- [Hon Win Motor articles](%s): car care articles from the workshop at Defu Lane, Hougang.' % url)

    def sec_html(items):
        o = ''
        for it in items:
            o += ('<ul class="hw-list">%s</ul>' % ''.join('<li>%s</li>' % E(x) for x in it)) if isinstance(it, list) else '<p>%s</p>' % E(it)
        return o

    for a in AL:
        path = C.BASE_PATH + 'articles/%s/' % a['slug']
        PG[0] = path
        depth = path.count('/')
        url = abs_url(path)
        svc = next(x for x in C.SERVICES if x['slug'] == a['maps'])
        cr, crld = crumbs(depth, [(C.NAME, C.BASE_PATH), ('Articles', C.BASE_PATH + 'articles/'), (a['h1'].split(':')[0], None)])
        secs = ''.join('<h2>%s</h2>%s' % (E(h), sec_html(it)) for h, it in a['sections'])
        more = [o for o in AL if o is not a][:3]
        img_abs = B.BASE + 'assets/img/' + a['img']
        ld = {'@context': 'https://schema.org', '@type': 'BlogPosting', 'headline': a['h1'], 'description': a['desc'], 'image': [img_abs],
              'datePublished': a['date'], 'dateModified': a['date'], 'mainEntityOfPage': url, 'inLanguage': 'en-SG',
              'author': {'@type': 'Organization', 'name': C.NAME, 'url': B.BASE + C.BASE_PATH},
              'publisher': {'@id': B.BASE + C.BASE_PATH + '#business'}, 'about': {'@type': 'Service', 'name': svc['h1'], 'url': B.BASE + C.BASE_PATH + svc['slug'] + '/'}}
        body = f'''<div class="hw">
<article class="hw-art">
<header class="hw-w hw-narrow hw-art-head"><h1>{E(a['h1'])}</h1><p class="hw-fine">By Hon Win Motor, 6 Defu Lane 10 · <time datetime="{a['date']}">{nice_date(a['date'])}</time></p></header>
<figure class="hw-w hw-narrow hw-art-hero">{img_tag(a['img'], a['alt'], depth, lazy=False)}</figure>
<div class="hw-w">{cr}</div>
<div class="hw-sec"><div class="hw-w hw-narrow hw-prose">{''.join('<p>%s</p>' % E(t) for t in a['intro'])}{secs}
<p class="hw-related">Related service: <a href="../../{svc['slug']}/">{E(svc['h1'])}</a></p></div></div>
</article>
{cta_band(a['wa'], 'band')}
<section class="hw-sec"><div class="hw-w hw-narrow"><h2>Questions</h2>{faq_html(a['faqs'])}</div></section>
{('<section class="hw-sec"><div class="hw-w"><h2>More articles</h2>%s<p><a href="../">All articles</a></p></div></section>' % art_cards(depth, more)) if more else ''}
{visit_block(depth, 'visit')}
{paid_note()}
</div>'''
        page(path, a['title'], a['desc'], body, [ld, faq_ld(a['faqs']), dict(crld, **{'@context': 'https://schema.org'})],
             og='https://pageonesingapore.com/preview/sgcarworkshop/assets/img/' + a['img'], bar=bar(a['wa']), h1=a['h1'], head_extra=head_extra(depth), tail=tail(depth), chrome=(hw_head(path), hw_foot(path)))
        LLMS.append('- [%s](%s): %s' % (a['h1'], url, a['desc']))


def _v(name):
    import hashlib
    return hashlib.sha256(open(os.path.join(HERE, 'hw', name), 'rb').read()).hexdigest()[:8]


CSS_V, JS_V = _v('hw.css'), _v('p1-cta.js')


def write_assets(out):
    d = os.path.join(out, 'assets', 'hw')
    os.makedirs(d, exist_ok=True)
    for f in os.listdir(os.path.join(HERE, 'hw')):
        shutil.copy(os.path.join(HERE, 'hw', f), d)
