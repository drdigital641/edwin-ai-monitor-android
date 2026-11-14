"""Ethel Zhang (ethelzhang.com): builds every page into site/ (python3 build.py).

Facts come only from Ethel's own notes (sent by Edwin, 16 Oct 2026), her current ethelzhang.com scorecard page,
and her PropertyGuru profile (checked 16 Oct 2026). No invented numbers, reviews or awards. See CONFIRM.
"""
import html
import json
import os
import re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')

SLUG = 'ethel-zhang'
DOMAIN = 'ethelzhang.com'
LIVE = False                       # True once ethelzhang.com serves this folder
NOINDEX = not LIVE                 # preview stays out of Google
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = 'https://%s/' % DOMAIN
ASSET = SITE if LIVE else PREVIEW
TODAY = '2026-10-16'

NAME = 'Ethel Zhang'
TITLE = 'Associate Division Director'
AGENCY, AGENCY_LIC = 'Huttons Asia Pte Ltd', 'L3008899K'
CEA = 'R059986J'
WA_NUM, WA_SHOW = '6591836325', '+65 9183 6325'  # from Edwin, 16 Oct 2026
PG_URL = 'https://www.propertyguru.com.sg/agent/ethel-zhang-622413'
SOCIAL = {'Instagram': 'https://www.instagram.com/ethel0212/',
          'Facebook': 'https://www.facebook.com/p/Ethel-Zhangs-real-estate-page-100029882864004/',
          'PropertyGuru': PG_URL}
CAFE = ('EC Coffee Bar', 'https://pageonesingapore.com/preview/ec-coffee-bar/')  # confirmed by Edwin 16 Oct 2026; switch to her domain at go-live

CONFIRM = """Open items for Ethel / Edwin:
- Email (WhatsApp 9183 6325 confirmed by Edwin).
- Agency: PropertyGuru says Huttons (Associate Division Director); Facebook page still says PropNex.
- Is her 2024 CBD cafe EC Coffee Bar? (link the two sites if yes)
- Languages (English and Mandarin assumed from her notes).
- Her own photos (beach home, cafe, UPW / Date with Destiny, Taiwan trips).
- '100+ families' and '8 years full-time' are her own statements (current ethelzhang.com page).
- Left out on purpose: the $400k+ profit and 'don't wait' lines (CEA: no implied returns or pressure).
- Go-live replaces the GoHighLevel scorecard funnel on ethelzhang.com; the PDF opt-in can move to a subdomain.
"""

E = html.escape
NAV = [('dream-method/', 'D.R.E.A.M. Method'), ('services/', 'How I help'), ('scorecard/', 'Scorecard'),
       ('about/', 'About'), ('articles/', 'Articles'), ('contact/', 'Contact')]


def wa(text):
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(text)) if WA_NUM else 'contact/'


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 '
          '11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>')


def wa_btn(text, label='WhatsApp Ethel', cls='btn btn-wa'):
    ext = ' target="_blank" rel="noopener"' if WA_NUM else ''
    return '<a class="%s" href="%s"%s>%s<span>%s</span></a>' % (cls, E(wa(text)), ext, WA_SVG, E(label))


MARK = ('<svg class="brand-mark" viewBox="0 0 44 44" aria-hidden="true"><circle cx="22" cy="22" r="22" fill="#b24a7c"/>'
        '<path d="M9 27a13 13 0 0 1 26 0" fill="none" stroke="#e2709a" stroke-width="2.6" stroke-linecap="round"/>'
        '<path d="M7 31h30" stroke="#c98ba0" stroke-width="2" stroke-linecap="round"/>'
        '<text x="22" y="25" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="13" fill="#fff">EZ</text></svg>')

I = lambda d: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % d
ICONS = {
    'buy': I('<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>'),
    'upgrade': I('<path d="M4 20h16"/><path d="M6 20V12h5v8M13 20V6h5v14"/><path d="m8.5 7 2-2 2 2"/>'),
    'sell': I('<path d="M3 12V4h8l10 10-8 8L3 12Z"/><circle cx="7.5" cy="7.5" r="1.5"/>'),
    'invest': I('<path d="M3 20h18"/><path d="M5 16l4-5 4 3 6-8"/><path d="M15 6h4v4"/>'),
    'rent': I('<rect x="4" y="3" width="16" height="18" rx="2"/><path d="M9 7h6M9 11h6M9 15h3"/>'),
    'legacy': I('<path d="M12 21c-5-3-8-6.5-8-10.5A4.5 4.5 0 0 1 12 8a4.5 4.5 0 0 1 8 2.5C20 14.5 17 18 12 21Z"/>'),
    'compass': I('<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5 5-2Z"/>'),
    'calendar': I('<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
    'question': I('<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14M12 17h.01"/>'),
    'swap': I('<path d="M4 8h13l-3-3M20 16H7l3 3"/>'),
    'person': I('<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>'),
    'office': I('<rect x="4" y="3" width="16" height="18" rx="1"/><path d="M8 7h2M14 7h2M8 11h2M14 11h2M8 15h2M14 15h2M10 21v-3h4v3"/>'),
    'shop': I('<path d="M3 9 5 4h14l2 5"/><path d="M3 9h18a3 3 0 0 1-6 0 3 3 0 0 1-6 0 3 3 0 0 1-6 0Z"/><path d="M5 12v9h14v-9M10 21v-5h4v5"/>'),
    'key': I('<circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l2 2"/>'),
}

PAGES = {}

# Ethel's own Instagram photos (screenshots sent by Edwin, 16 Oct 2026). Captions only restate what each post shows.
PHOTOS = [('booth.webp', 640, 883, 'Ethel at her Huttons booth beside her bilingual banner: "Let\'s talk Singapore property"', 'Meeting buyers and investors at a property fair'),
          ('latte.webp', 640, 855, 'Ethel in pink, making a latte at her cafe', 'Behind the counter at EC Coffee Bar'),
          ('cafe-poster.webp', 640, 853, 'Ethel at her laptop with a latte: "Live your dream. Build your legacy."', 'Building more than a business (June 2026)'),
          ('masterclass.webp', 640, 855, 'Ethel at a masterclass in Kuala Lumpur, holding a paper gratitude flower', 'Learning at a masterclass in Kuala Lumpur (March 2026)'),
          ('dinner.webp', 480, 640, 'Ethel at an outdoor dinner table at dusk', 'A good moment, on her own feed (July 2026)'),
          ('lily.webp', 560, 560, 'Portrait of Ethel Zhang with white lilies', 'Trust the flow of life (October 2025)')]


def gallery(items=None, prefix=''):
    return '<div class="gallery">' + ''.join('<figure><img src="%simg/%s" alt="%s" width="%d" height="%d" loading="lazy"><figcaption>%s</figcaption></figure>'
                                              % (prefix, f, E(alt), w, h, E(cap)) for f, w, h, alt, cap in (items or PHOTOS)) + '</div>'


def page(path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, kind='WebPage'):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede, schema=schema or [],
                       hero=hero, cta=cta, kind=kind)


def faq_html(items):
    return '<div class="faq">' + ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items) + '</div>'


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


# ------------------------------------------------------------------------------------------------
# Shared content
# ------------------------------------------------------------------------------------------------
DREAM = [('D', 'Discover the dream', 'What must this property do for your life now and over the next 10 years?', 'dream'),
         ('R', 'Review your financial reality', 'Cash, CPF, loan limits and a buffer for when life changes.', 'reality'),
         ('E', 'Evaluate all viable options', 'Compare every realistic route, including staying where you are.', 'options'),
         ('A', 'Align with your whole life', 'Family, career or business, timing and legacy, pulling the same way.', 'align'),
         ('M', 'Masterplan the execution', 'A clear sequence, timeline and next steps before you sign anything.', 'masterplan')]

SERVICES = [
    ('services/buying-your-next-home/', 'buy', 'Buying your next home',
     'For singles and couples choosing a private home that fits the next 10 years, not just today.'),
    ('services/offices-and-shophouses/', 'office', 'Offices and shophouses',
     'Buying, renting or investing in commercial space, with own-use versus investment, costs and tax laid out clearly.'),
    ('services/business-premises/', 'shop', 'Business premises and setup',
     'Finding the right space for your café, clinic or office, and guidance through the setup steps from someone who has done it.'),
    ('services/upgrading/', 'upgrade', 'Upgrading your home',
     'Moving from HDB to private, or to a bigger home, without stretching your finances too thin.'),
    ('services/selling/', 'sell', 'Selling your home',
     'Pricing, timing and sequencing a sale so your next move is ready when the money is.'),
    ('services/property-investment/', 'invest', 'Investment and portfolio planning',
     'Deciding whether a second property makes sense for you, and which kind.'),
    ('services/renting-and-leasing/', 'rent', 'Renting and leasing',
     'For landlords renting out a home and tenants looking for one, with clear terms on both sides.'),
    ('services/retirement-and-legacy/', 'legacy', 'Retirement, family and legacy',
     'Right-sizing, planning around parents and children, and what you want to leave behind.'),
]

TIMELINE = [
    ('2010', 18, 'Dreamed of owning my own condo one day.'),
    ('2018', 26, 'Bought my first condo, together with my mum, and started full-time in real estate.'),
    ('2019', 27, 'Attended Tony Robbins\' Unleash the Power Within, fire walk included, to build a stronger mindset.'),
    ('2022', 30, 'Sold that first condo and moved to a home near the beach in District 15, alongside a new launch investment.'),
    ('2023', 31, 'Flew to the USA for Tony Robbins\' Date with Destiny, which reshaped my purpose and how I make decisions.'),
    ('2024', 32, 'Opened my own café and workspace{cafe} in a conservation shophouse in Singapore\'s CBD, and learned about location, licensing and hiring the hard way.'),
    ('2026', 34, 'Eight years and more than 100 families later, I value a simpler life. Each life stage brings different priorities, and the right property follows them.'),
]

FAQ_HOME = [
    ('Who is Ethel Zhang?', 'Ethel Zhang is a Singapore property agent and %s with %s (Estate Agent Licence %s). Her CEA registration number is %s, which you can check on the CEA Public Register. She has been in full-time real estate since 2018.' % (TITLE, AGENCY, AGENCY_LIC, CEA)),
    ('What makes Ethel different from other agents?', 'Ethel starts with purpose, not a project. Using her D.R.E.A.M. Method, she first works out what your next property must do for your life, then checks your finances and every realistic option before recommending a move.'),
    ('Does Ethel handle commercial property?', 'Yes. Besides homes, Ethel helps business owners buy, rent or invest in offices and shophouses, and find premises for F&B and other businesses. She runs her own café in a CBD shophouse, so she knows the setup side first-hand.'),
    ('How much does a first conversation cost?', 'Nothing. Any commission for a purchase, sale or tenancy is agreed with you in writing before work starts, using the CEA prescribed estate agency agreement.'),
]


def dream_cards(link=True):
    return '<div class="dream">' + ''.join('<div class="dl"><span class="L">%s</span><h3>%s</h3><p>%s</p></div>' % (l, t, d) for l, t, d, _ in DREAM) + '</div>'


def service_cards(prefix=''):
    return '<div class="cards">' + ''.join(
        '<a class="card" href="%s%s"><span class="ic">%s</span><h3>%s</h3><p>%s</p><span class="more">More details</span></a>' % (prefix, p, ICONS[ic], t, d)
        for p, ic, t, d in SERVICES) + '</div>'


APHOTO = {'should-i-upgrade-or-stay-put': 'masterclass', 'buying-a-condo-as-a-single-in-singapore': 'studio',
          'questions-to-ask-before-choosing-a-new-launch': 'booth', 'how-to-plan-a-10-year-property-roadmap': 'dinner',
          'sell-first-or-buy-first-singapore': 'ethel', 'renting-out-your-condo-checklist': 'lily',
          'buying-a-shophouse-in-singapore': 'cafe-poster', 'finding-fnb-premises-in-the-cbd': 'latte'}
# AI topic images made by the Base44 writer (auto/legacy_images.json: slug -> https URL) replace the stand-in photos.
LEGACY_IMG = json.load(open(os.path.join(HERE, 'auto', 'legacy_images.json'))) if os.path.exists(os.path.join(HERE, 'auto', 'legacy_images.json')) else {}
APHOTO.update(LEGACY_IMG)


def photo_src(name):
    return name if name.startswith('https://') else 'img/%s.webp' % name


def article_cards(items):
    return '<div class="acards">' + ''.join(
        '<a class="acard" href="articles/%s/"><span class="thumb %s"><img src="%s" alt="" width="640" height="300" loading="lazy"></span><span class="in"><h3>%s</h3><p>%s</p><span class="more">Read article</span></span></a>'
        % (a['slug'], a['tone'], photo_src(APHOTO[a['slug']]), E(a['h1']), E(a['card'])) for a in items) + '</div>'


def aside(title, text, wa_text):
    return ('<aside class="aside"><img src="img/wa.webp" alt="Ethel Zhang" width="88" height="88" loading="lazy">'
            '<h3>%s</h3><p>%s</p>%s<small>%s · CEA Reg. %s · %s (%s)</small></aside>'
            % (E(title), E(text), wa_btn(wa_text), NAME, CEA, AGENCY, AGENCY_LIC))


# ------------------------------------------------------------------------------------------------
# Articles (defined first so the home page can show cards)
# ------------------------------------------------------------------------------------------------
ARTICLES = []


def article(slug, h1, title, desc, card, icon, tone, owner, owner_label, body, faqs):
    ARTICLES.append(dict(slug=slug, h1=h1, card=card, icon=icon, tone=tone))
    full = ('<section class="sec"><div class="wrap layout"><article class="prose"><p class="meta">By %s · %s, %s · Updated 16 October 2026</p><figure class="lead-fig art-fig"><img src="%s" alt="" width="640" height="360" loading="eager"></figure>%s'
            '<h2>Questions people also ask</h2>%s<p class="note">This article is general information, not financial or legal advice. Rules on loans, CPF, HDB eligibility and stamp duty change; check the official sources linked above for the current position.</p>'
            '<p>Related: <a href="%s">%s</a> · <a href="dream-method/">The D.R.E.A.M. Method</a> · <a href="scorecard/">Take the 10-Year Property Fit Scorecard</a></p></article>%s</div></section>'
            % (NAME, TITLE, AGENCY, photo_src(APHOTO[slug]), body, faq_html(faqs), owner, owner_label,
               aside('Talk it through with Ethel', 'Every situation is different. Tell Ethel where you are and what you are weighing up.',
                     'Hi Ethel, I read your article "%s". I would like to talk about my situation.' % h1)))
    page('articles/%s/' % slug, title, desc, h1, full, crumbs=[('articles/', 'Articles'), ('articles/%s/' % slug, h1)], kind='Article',
         schema=[faq_schema(faqs), {'@type': 'Article', 'headline': h1, 'description': desc, 'datePublished': TODAY, 'dateModified': TODAY,
                                    'author': {'@id': SITE + '#ethel'}, 'publisher': {'@id': SITE + '#ethel'}, 'inLanguage': 'en-SG',
                                    'mainEntityOfPage': SITE + 'articles/%s/' % slug, 'image': ASSET + 'img/hero.webp'}])


IRAS_ABSD = 'https://www.iras.gov.sg/taxes/stamp-duty/for-property/buying-or-acquiring-property/additional-buyer%27s-stamp-duty-(absd)'
HDB_SINGLES = 'https://www.hdb.gov.sg/residential/buying-a-flat/understanding-your-eligibility-and-housing-loan-options/flat-and-grant-eligibility/singles'
URA_MP = 'https://www.ura.gov.sg/Corporate/Planning/Master-Plan'
CEA_REG = 'https://www.cea.gov.sg/aceas/public-register'
CPF_HOUSING = 'https://www.cpf.gov.sg/member/home-ownership'

article('should-i-upgrade-or-stay-put',
        'Should I upgrade my home or stay put? A 10-year way to decide',
        'Should I Upgrade My Home or Stay Put? | Ethel Zhang',
        'How Singapore homeowners can decide between upgrading and staying: start with purpose, check the finances, compare every route, then plan the move.',
        'A simple way to decide between upgrading and staying, starting from the life you want.', 'swap', 't1',
        'services/upgrading/', 'Upgrading your home',
        '''<p class="answer">Upgrade when a new home clearly does something your current one cannot, such as space for a growing family, a better location for work or school, or a long-term plan, and when you can afford it with a buffer left over. If the main reason is that "everyone is upgrading" or a launch looks attractive, staying put is often the stronger choice.</p>
<h2>Start with what the next home must do</h2>
<p>Most upgrade conversations start with a project, a location or a price. Ethel starts somewhere else: what should the next home do for your life over the next 10 years? Write down the two or three things your current home cannot give you. If you struggle to name them, that is useful information.</p>
<ul><li>More space for children, parents or working from home.</li><li>A shorter commute or a school you want to be near.</li><li>A home that also supports a longer-term wealth or retirement plan.</li></ul>
<h2>Check your financial reality, not just your loan limit</h2>
<p>A bank may lend you more than is comfortable. Look at the full picture: cash and CPF available for the down payment, stamp duty, legal and renovation costs, and the monthly instalment if interest rates rise. Leave a buffer for a job change, a new baby or caring for parents. CPF's <a href="''' + CPF_HOUSING + '''" target="_blank" rel="noopener">home ownership pages</a> explain how CPF can be used for housing.</p>
<h2>Compare more than one route</h2>
<p>Upgrading is not one decision. Compare at least three realistic routes side by side:</p>
<table><tr><th>Route</th><th>Good when</th><th>Watch out for</th></tr>
<tr><td>Stay and renovate</td><td>Location still works and the gap is mostly space or layout</td><td>Renovation cost versus value added</td></tr>
<tr><td>Sell, then buy</td><td>You need the sale proceeds for the next purchase</td><td>Temporary housing and timing</td></tr>
<tr><td>Buy, then sell</td><td>You want to move once, with the next home ready</td><td>Stamp duty rules and carrying two loans</td></tr></table>
<p>Stamp duty can change the numbers a lot when you own more than one property, even briefly. IRAS sets out the current <a href="''' + IRAS_ABSD + '''" target="_blank" rel="noopener">Additional Buyer's Stamp Duty rules and remission conditions</a>.</p>
<h2>Align it with the rest of your life</h2>
<p>A good upgrade fits your career, your family plans and your timing. If you might change jobs, start a business or support parents in the next few years, factor that in before choosing a bigger commitment.</p>
<h2>Plan the execution</h2>
<ol><li>Agree the purpose and the budget ceiling as a family.</li><li>Get your loan position confirmed in principle.</li><li>Decide the sequence: sell first, buy first, or renovate.</li><li>Set a timeline with a fallback if a step takes longer.</li></ol>''',
        [('Is it better to upgrade when prices are high?', 'Price level matters less than whether the move fits your plan. When you sell and buy in the same market, both sides tend to move together; the bigger risks are overcommitting on the loan or getting the timing between sale and purchase wrong.'),
         ('How do I know if I can afford to upgrade?', 'Add up cash and CPF for the down payment, stamp duty and other costs, then test the monthly instalment at a higher interest rate. If the plan only works when nothing goes wrong, it is too tight.'),
         ('Can I keep my current home and buy another?', 'Sometimes, but owning two homes usually brings Additional Buyer\'s Stamp Duty and stricter loan limits. Check IRAS and your bank before deciding.')])

article('buying-a-condo-as-a-single-in-singapore',
        'Buying a condo as a single in Singapore: what to think about first',
        'Buying a Condo as a Single in Singapore | Ethel Zhang',
        'What singles in Singapore should consider before buying a condo: HDB versus private, budget and buffer, resale value, and planning for life changes.',
        'Freedom, privacy and flexibility: how singles can choose a home that keeps their options open.', 'person', 't2',
        'services/buying-your-next-home/', 'Buying your next home',
        '''<p class="answer">A single Singapore Citizen can buy a private condo at any age, while HDB sets separate age and flat-type rules for singles. Before choosing a project, decide what the home must do for you in the next 10 years, keep a cash buffer, and favour a unit that is easy to rent or resell if your life changes.</p>
<h2>HDB or private: know the rules that apply to you</h2>
<p>HDB has specific eligibility rules for singles, including a minimum age under the Single Singapore Citizen Scheme and limits on which flats you can buy. See HDB's page on <a href="''' + HDB_SINGLES + '''" target="_blank" rel="noopener">eligibility for singles</a> for the current rules. Private property has no such age limit for citizens, which is why many high-income singles look at condos first.</p>
<h2>What singles often value most</h2>
<ul><li><b>Speed and privacy.</b> A clear process and an adviser who respects your time.</li><li><b>Freedom.</b> A home that does not lock you in if you move overseas, change careers or start a business.</li><li><b>Well-reasoned advice.</b> A recommendation you can follow the logic of, not hype about a launch.</li></ul>
<h2>Plan for the life you may have later</h2>
<p>Ten years is long. You may marry, want children, care for parents, or move abroad. A two-bedroom near transport is often more flexible than the largest one-bedroom you can afford. Ask: if my life changed in three years, could I rent this out or sell it without loss of sleep?</p>
<h2>Keep a buffer</h2>
<p>As a single buyer, there is one income behind the loan. Test the instalment at a higher interest rate and keep several months of expenses in cash after paying the down payment, stamp duty and legal fees.</p>
<h2>Questions to ask before choosing a project</h2>
<ol><li>Why this location, for my work and lifestyle?</li><li>Who would rent or buy this unit from me later?</li><li>What happens to my plan if my income dips for six months?</li><li>Does this purchase affect what I can buy later, for example with a partner?</li></ol>''',
        [('Can a single buy a condo in Singapore?', 'Yes. Singapore Citizens can buy private condos without an age requirement. Stamp duty and loan limits still apply; check IRAS and your bank for your case.'),
         ('Should a single buy a one-bedroom or two-bedroom?', 'It depends on your plans. A two-bedroom often gives more flexibility for a future partner, a home office or renting out a room, but it costs more. Decide based on your next 10 years, not only on today.'),
         ('Does buying alone affect buying with a partner later?', 'It can. Owning a property may change the stamp duty and loan limits on a later purchase. Plan the sequence before you buy.')])

article('questions-to-ask-before-choosing-a-new-launch',
        'Questions to ask before choosing a new launch condo',
        'Questions to Ask Before Choosing a New Launch | Ethel Zhang',
        'Before choosing a new launch condo in Singapore, ask what it is for, whether the numbers hold, how it compares with resale, and what URA plans mean nearby.',
        'Purpose before project: the questions that matter more than the showflat.', 'question', 't3',
        'services/property-investment/', 'Investment and portfolio planning',
        '''<p class="answer">Before choosing a new launch, ask what the property is for (home, investment, income or legacy), whether the full cost works with a buffer, how it compares with resale homes nearby, and what the area's plans and supply look like. A good project can still be the wrong decision if the purpose is unclear.</p>
<h2>1. What is this property meant to do?</h2>
<p>Ethel's first question is always purpose. Is it meant to improve your family's lifestyle, grow wealth, produce income, support a life transition or become part of your legacy? Each purpose points to a different size, location and budget.</p>
<h2>2. Do the numbers work with room to spare?</h2>
<p>New launches are paid in stages as construction progresses, so check the cash and CPF needed at each stage, the stamp duty, and what happens if interest rates rise before completion.</p>
<h2>3. How does it compare with resale nearby?</h2>
<p>Look at completed homes in the same area: size, age, price and how quickly they sell or rent. A new launch should be worth the wait and any premium over a comparable resale unit.</p>
<h2>4. What is planned around it?</h2>
<p>Check the <a href="''' + URA_MP + '''" target="_blank" rel="noopener">URA Master Plan</a> for transport, amenities and land use nearby, and how many other homes are being built in the area. Supply affects both rental demand and resale.</p>
<h2>5. What is your exit?</h2>
<ul><li>Who is the likely buyer or tenant for this unit later?</li><li>How long do you plan to hold it, and why?</li><li>What would make you sell earlier, and could you?</li></ul>
<h2>Read the whole market before acting</h2>
<p>Cooling measures, supply, URA plans, the wider economy and the details of one unit all matter. Ethel connects these before recommending any project, which is the third of her "three secrets": read the whole market before acting.</p>''',
        [('Are new launches better than resale condos?', 'Neither is better in general. New launches offer a new home and staged payments; resale lets you see exactly what you buy and move in sooner. The right choice depends on your purpose and timeline.'),
         ('What should I check at a showflat?', 'The real unit layout and facing, the site plan, the payment schedule, maintenance fees, the expected completion date and what is planned nearby.'),
         ('Where can I check plans for an area?', 'The URA Master Plan shows planned land use, and URA and LTA publish upcoming developments and transport lines.')])

article('sell-first-or-buy-first-singapore',
        'Sell first or buy first in Singapore? How to choose the order',
        'Sell First or Buy First in Singapore? | Ethel Zhang',
        'Should you sell your home first or buy the next one first in Singapore? Compare cash flow, stamp duty, timing risk and temporary housing.',
        'Sequencing a move so the money and the keys arrive in the right order.', 'calendar', 't4',
        'services/selling/', 'Selling your home',
        '''<p class="answer">Selling first gives you certainty about the money but may mean renting in between. Buying first lets you move once but can mean carrying two loans and paying extra stamp duty for a while. The right order depends on your cash, loan position and how much timing risk you can live with.</p>
<h2>Selling first</h2>
<ul><li><b>Pros:</b> you know your sale price and proceeds before committing; one loan at a time.</li><li><b>Cons:</b> you may need temporary housing or a longer completion to bridge the gap.</li></ul>
<h2>Buying first</h2>
<ul><li><b>Pros:</b> you secure the home you want and move once.</li><li><b>Cons:</b> owning two properties at once can bring Additional Buyer's Stamp Duty, stricter loan limits and two sets of payments. IRAS explains <a href="''' + IRAS_ABSD + '''" target="_blank" rel="noopener">when ABSD applies and when remission may be possible</a>.</li></ul>
<h2>How to decide</h2>
<ol><li>Work out how much you need from the sale to fund the next purchase.</li><li>Check your loan eligibility while you still own the current home.</li><li>Map both timelines: option, exercise and completion dates on each side.</li><li>Decide what you would do if the sale takes longer than planned.</li></ol>
<h2>Line up the dates</h2>
<p>The smoothest moves line up the completion of the sale and the purchase closely, with a short, planned overlap or a short-term rental. Ethel plans these dates before the first viewing, so the sequence is clear before any money changes hands.</p>''',
        [('Can I sell and buy at the same time?', 'You can try to align both, but the dates rarely match exactly. Plan a fallback, such as a short rental or a longer completion period agreed with the buyer.'),
         ('Do I pay ABSD if I buy before selling?', 'It depends on your profile and how many properties you will own on the date of purchase. Check the current IRAS rules and remission conditions before you commit.'),
         ('How long does selling a home take?', 'It varies with the property, price and market. Plan for marketing time plus the option and completion periods, and keep a buffer.')])

article('how-to-plan-a-10-year-property-roadmap',
        'How to plan a 10-year property roadmap',
        'How to Plan a 10-Year Property Roadmap | Ethel Zhang',
        'A step-by-step way to build a 10-year property plan in Singapore using the D.R.E.A.M. Method: dream, reality, options, alignment and masterplan.',
        'Five steps to a property plan that supports your next decade, not just your next purchase.', 'compass', 't5',
        'dream-method/', 'The D.R.E.A.M. Method',
        '''<p class="answer">A 10-year property roadmap starts with what you want your life to look like, checks your real financial position, compares every realistic option, makes sure the choice fits your family and career, and ends with a clear sequence of steps. Ethel calls this the D.R.E.A.M. Method.</p>
<h2>D: Discover the dream</h2>
<p>Describe your life in 10 years: where you live, who lives with you, how you work and what you want property to do for you. Lifestyle, wealth, income, a life transition and legacy are all valid purposes, but they lead to different decisions.</p>
<h2>R: Review your financial reality</h2>
<p>List your cash, CPF, income stability and existing commitments. Work out a comfortable ceiling, not the maximum a bank would lend, and keep a buffer.</p>
<h2>E: Evaluate all viable options</h2>
<p>Put staying, renovating, upgrading, right-sizing and adding an investment property side by side. Compare cost, risk and how each one serves the purpose from step one.</p>
<h2>A: Align property with your whole life plan</h2>
<p>Check the shortlist against your family plans, career or business, timing and legacy. The right option is the one that pulls in the same direction as everything else.</p>
<h2>M: Masterplan the execution</h2>
<ol><li>Order the steps (for example, sell, then buy, then renovate).</li><li>Set target dates and the decision points in between.</li><li>Decide what would make you pause or change course.</li><li>Review the plan once a year or when life changes.</li></ol>
<p>Want a quick check of where you stand? Take the <a href="scorecard/">10-Year Property Fit Scorecard</a>.</p>''',
        [('Why plan property over 10 years?', 'Buying and selling are costly, so most homes are held for years. A 10-year view helps you choose a property that still fits after a marriage, a child, a job change or caring for parents.'),
         ('How often should I review my property plan?', 'Once a year, and whenever something big changes, such as income, family or government rules.'),
         ('Do I need an agent to make a property plan?', 'No, but an experienced adviser can help you see options and risks you may miss, and connect the plan with the market.')])

article('renting-out-your-condo-checklist',
        'Renting out your condo in Singapore: a landlord checklist',
        'Renting Out Your Condo in Singapore: Checklist | Ethel Zhang',
        'A practical checklist for Singapore landlords: preparing the unit, setting rent, screening tenants, the tenancy agreement and handover.',
        'From preparing the unit to handover day, what landlords should get right.', 'key', 't6',
        'services/renting-and-leasing/', 'Renting and leasing',
        '''<p class="answer">To rent out a condo in Singapore smoothly: prepare and photograph the unit well, set the rent from recent comparable rentals, check the tenant's identity and right to stay in Singapore, use a clear tenancy agreement, and record the unit's condition at handover.</p>
<h2>1. Prepare the unit</h2>
<ul><li>Fix small defects, service the air-conditioning and clean thoroughly.</li><li>Decide what furniture and appliances stay.</li><li>Take good photos in daylight.</li></ul>
<h2>2. Set the rent</h2>
<p>Look at recent rentals of similar units in the same development and nearby, not only asking prices. A realistic rent usually finds a good tenant faster than a high one.</p>
<h2>3. Screen tenants carefully</h2>
<ul><li>Check identity documents and, for foreigners, their pass and its validity.</li><li>Understand who will live in the unit and for how long.</li><li>Ask about the reason for moving and the expected start date.</li></ul>
<h2>4. Agree clear terms</h2>
<p>The tenancy agreement should cover rent, deposit, the lease period, who pays for minor repairs, diplomatic or early-termination clauses and handover condition. Clear terms prevent most disputes.</p>
<h2>5. Hand over properly</h2>
<p>Do a joint inventory and condition check with photos on handover day, and keep a copy signed by both sides. It makes the end of the lease much easier.</p>''',
        [('How much rent can I ask for my condo?', 'Base it on recent rentals of similar units nearby. URA publishes private rental statistics, and an agent can pull comparable recent transactions for your development.'),
         ('Who pays the agent when renting out a condo?', 'It depends on the arrangement. Fees and who pays them are agreed in writing before the agent starts work.'),
         ('What should a tenancy agreement include?', 'Rent, deposit, lease length, repair responsibilities, early-termination terms, and the condition and inventory at handover.')])

GOBIZ = 'https://licensing.gobusiness.gov.sg/'
URA_CONS = 'https://www.ura.gov.sg/Corporate/Guidelines/Conservation'
SFA_SHOP = 'https://www.sfa.gov.sg/food-retail/licences-permits-registration'

article('buying-a-shophouse-in-singapore',
        'Buying a shophouse in Singapore: what to check first',
        'Buying a Shophouse in Singapore: What to Check | Ethel Zhang',
        'What to check before buying a shophouse in Singapore: own use or investment, zoning and allowed use, conservation rules, tenure, costs and GST.',
        'Zoning, conservation rules, tenure and costs: the checks that matter before you commit.', 'shop', 't2',
        'services/offices-and-shophouses/', 'Offices and shophouses',
        """<p class="answer">Before buying a shophouse, decide whether it is for your own business or for investment, then check the zoning and allowed use, any conservation rules, the tenure, the existing tenancy and the full cost, including stamp duty and GST. A shophouse that cannot be used the way you plan is an expensive mistake.</p>
<h2>Own use or investment?</h2>
<p>An owner-occupier cares about layout, frontage, approved use and whether the space suits the business. An investor cares about the tenant, the lease terms, rental demand in the street and the exit. The same unit can be right for one and wrong for the other.</p>
<h2>Check the zoning and allowed use</h2>
<p>What a shophouse may be used for depends on its zoning and approved use. Uses such as food and beverage often need specific approvals. Check with URA before relying on a planned use, and ask for the approved floor plans.</p>
<h2>Conservation shophouses</h2>
<p>Many shophouses are conserved buildings. Restoration and alteration works must follow URA's <a href=\"""" + URA_CONS + """\" target="_blank" rel="noopener">conservation guidelines</a>, which can affect renovation cost and timing.</p>
<h2>Tenure and the existing lease</h2>
<ul><li>Freehold, 999-year or leasehold, and how much lease is left.</li><li>Whether there is a sitting tenant, the rent, the remaining lease and any renewal options.</li><li>Who is responsible for repairs and the building's condition.</li></ul>
<h2>Costs people forget</h2>
<p>Additional Buyer's Stamp Duty applies to residential property, not to commercial property, but Buyer's Stamp Duty still applies, and GST may be charged if the seller is GST-registered. Commercial loans are set by each bank, so check financing early. Renovation and fitting-out can also be significant.</p>
<h2>Plan the purchase</h2>
<ol><li>Agree the purpose: own use, investment or both.</li><li>Confirm zoning, approved use and any conservation conditions.</li><li>Check financing and the full cost, including GST.</li><li>Review the tenancy and building condition.</li><li>Negotiate, then complete with your lawyer.</li></ol>""",
        [('Is ABSD payable on a shophouse?', 'Additional Buyer\'s Stamp Duty applies to residential property. For commercial property, Buyer\'s Stamp Duty still applies, and GST may be charged if the seller is GST-registered. Mixed-use properties can be treated differently, so check with IRAS and your lawyer.'),
         ('Can I run a café in any shophouse?', 'No. It depends on the zoning and approved use, and F&B usually needs specific approvals and licences. Check the allowed use before you commit.'),
         ('Should my business buy or rent its premises?', 'It depends on your cash flow, how long you will stay, and whether the property also makes sense as an investment. Ethel compares both routes with you.')])

article('finding-fnb-premises-in-the-cbd',
        'Finding F&B premises in the CBD: a practical checklist',
        'Finding F&B Premises in the CBD: Checklist | Ethel Zhang',
        'A practical checklist for finding café or restaurant premises in Singapore\'s CBD: location, approved use, licences, fit-out, lease terms and timing.',
        'Location, approved use, licences and lease terms, from someone who opened her own café.', 'office', 't1',
        'services/business-premises/', 'Business premises and setup',
        """<p class="answer">To find F&B premises in the CBD, start with your customers and opening hours, then check that the unit's approved use allows F&B, what licences you will need, the cost and time of fitting out, and the lease terms. Ethel learned these steps first-hand when she opened her own café and workspace in a CBD shophouse in 2024.</p>
<h2>1. Start with your customers</h2>
<p>Office workers, after-work crowds and weekend visitors want different things. Your opening hours, foot traffic and visibility should match the people you serve.</p>
<h2>2. Check the approved use</h2>
<p>Not every unit may be used for F&B. Check the zoning and approved use, and whether a change of use approval is needed, before you sign anything.</p>
<h2>3. Plan the licences</h2>
<p>Food businesses need a licence from the Singapore Food Agency, and some works may need other approvals. See SFA's <a href=\"""" + SFA_SHOP + """\" target="_blank" rel="noopener">licences and permits</a> and the <a href=\"""" + GOBIZ + """\" target="_blank" rel="noopener">GoBusiness licensing portal</a>, and allow time in your plan.</p>
<h2>4. Budget the fit-out</h2>
<p>Kitchen exhaust, grease traps, electrical load, plumbing and fire safety can change your budget a lot. Ask what the previous tenant left behind and what the landlord will allow.</p>
<h2>5. Read the lease carefully</h2>
<ul><li>Lease length, renewal options and rent reviews.</li><li>Rent-free fitting-out period.</li><li>Reinstatement obligations at the end of the lease.</li><li>Who pays for repairs and building works.</li></ul>
<h2>6. Line up the timeline</h2>
<p>Licences, renovation and hiring all take time. Work backwards from your opening date and keep a buffer.</p>""",
        [('How long does it take to open a café in Singapore?', 'It varies with the premises, approvals and renovation. Plan for finding the space, approvals and licences, fit-out and hiring, with a buffer at each step.'),
         ('Do I need a licence to run a café?', 'Yes. Food businesses need a licence from the Singapore Food Agency, and the premises must be approved for the use. Check SFA and GoBusiness for the current requirements.'),
         ('Can Ethel help with licensing?', 'Ethel can guide you on what to check, based on opening her own café, and coordinate with the right professionals. Formal applications and legal advice sit with the relevant agencies and your consultants.')])


exec(open(os.path.join(HERE, 'auto_articles.py')).read())  # daily Base44-written articles (auto/*.json)

# ------------------------------------------------------------------------------------------------
# Home
# ------------------------------------------------------------------------------------------------
def home_body():
    sparks = ''.join('<i class="spark s%d" aria-hidden="true">✦</i>' % i for i in range(1, 9))
    hero = f"""<section class="hero hero-dream"><div class="aurora" aria-hidden="true"></div>{sparks}<div class="wrap">
<div><span class="eyebrow">Ethel Zhang · Property adviser · {AGENCY.replace(' Pte Ltd', '')}</span>
<h1>Your next property decision should begin with <em>the life you want</em> it to support.</h1>
<p class="lede">Homes, offices and shophouses for professionals, families and business owners. I connect each property move with your finances, your business and the next 10 years, in English or 中文.</p>
<div class="btns"><a class="btn btn-main" href="scorecard/">Take the 2-minute scorecard</a>{wa_btn("Hi Ethel, I found your website. I would like to talk about my next property move.")}</div>
<ul class="chips" aria-label="Ethel at a glance"><li><b data-to="8">8</b> years full-time</li><li><b data-to="100" data-suf="+">100+</b> families</li><li><b data-to="47">47</b> transactions in 3 years <a href="{PG_URL}" target="_blank" rel="noopener">(PropertyGuru, Oct 2026)</a></li></ul></div>
<div class="hero-fig"><div class="arch"><img src="img/hero-new.webp" alt="Ethel Zhang, property adviser with Huttons" width="600" height="716" fetchpriority="high"></div>
<div class="float f1"><b>8 years</b>full-time in real estate</div><div class="float f2"><b>100+</b>families served</div></div>
</div></section>"""
    quote_ = """<section class="sec fq"><div class="wrap quote"><blockquote>Most people begin with a project, location or price. I begin with purpose. When the purpose is unclear, even a good property can become the wrong decision.</blockquote><cite>Ethel Zhang</cite></div></section>"""
    dream = f"""<section class="sec fdream"><div class="wrap"><div class="sec-head c"><span class="eyebrow">My method</span><h2>The D.R.E.A.M. Alignment Method</h2>
<p>Five steps that turn your purpose into a clear 10-year property roadmap.</p></div>{dream_cards()}
<div class="btns c"><a class="btn btn-ghost" href="dream-method/">See how the method works</a></div></div></section>"""
    svc = f"""<section class="sec fsvc"><div class="wrap"><div class="sec-head c"><span class="eyebrow">How I help</span><h2>A property adviser for every stage of life</h2>
<p>I don't focus on one project, location or property type. I help you make the right decision as your life changes.</p></div>{service_cards()}</div></section>"""
    who = """<section class="sec fwho"><div class="wrap"><div class="sec-head c"><span class="eyebrow">Who I work with</span><h2>For people at a property crossroads</h2>
<p>Singapore Citizens, PRs and business owners, typically aged 30 to 50, who can make a move but want to be sure it is the right one.</p></div>
<ul class="wishes"><li><h3>High-income singles</h3><p>You value speed, privacy, freedom and well-reasoned advice. You want a home that keeps your options open.</p></li>
<li><h3>Couples and families</h3><p>You are planning an upgrade, a life change, retirement or legacy, and want the property to fit the whole family plan.</p></li>
<li><h3>Entrepreneurs and business owners</h3><p>You need an office, shophouse or F&amp;B space, or want to decide between owning and renting your premises. Ethel runs her own café, so she knows the setup side too.</p></li>
<li><h3>Professionals and international families</h3><p>Lawyers, doctors and company directors, and families originally from Korea, Japan, Indonesia and China who now call Singapore home. Ethel works in English and Mandarin.</p></li></ul></div></section>"""
    rows = [t for t in TIMELINE if t[0] in ('2010', '2018', '2022', '2024', '2026')]
    short = {'2010': 'The dream of my own condo', '2018': 'First condo, with my mum', '2022': 'Sold, moved near the beach in D15',
             '2024': 'Opened my café in the CBD', '2026': '100+ families, a simpler life'}
    story = """<section class="sec fstory"><div class="wrap"><div class="sec-head c"><span class="eyebrow">My story</span><h2>I have made these decisions myself</h2>
<p>From dreaming of a condo at 18 to moving from one private home to two, my own moves taught me that property must leave room for family, work and future choices.</p></div>
<ol class="tl-row">""" + ''.join('<li><b>%s</b><span>%s</span></li>' % (y, short[y]) for y, _, _ in rows) + """</ol>
<div class="btns c"><a class="btn btn-ghost" href="about/">Read my story</a></div></div></section>"""
    feed = ('<section class="sec ffeed"><div class="wrap"><div class="sec-head c"><span class="eyebrow">From Ethel\'s feed</span><h2>Life, not just property</h2>'
            '<p>Moments from Ethel\'s own Instagram, <a href="%s" target="_blank" rel="noopener">@ethel0212</a>.</p></div>%s</div></section>' % (SOCIAL['Instagram'], gallery()))
    band = """<section class="sec fband"><div class="wrap"><div class="band"><div><h2>Is your next move the right one?</h2>
<p>Answer five questions and see which part of your plan needs more thought. It takes about two minutes.</p></div><a class="btn btn-wa" style="background:#e2709a" href="scorecard/">Take the scorecard</a></div></div></section>"""
    arts = """<section class="sec fart"><div class="wrap"><div class="sec-head c"><span class="eyebrow">Articles</span><h2>Clear thinking for big decisions</h2></div>%s
<div class="btns c"><a class="btn btn-ghost" href="articles/">All articles</a></div></div></section>""" % article_cards(ARTICLES[:3])
    faq = '<section class="sec ffaq"><div class="wrap" style="max-width:860px"><div class="sec-head c"><h2>Questions about working with Ethel</h2></div>%s</div></section>' % faq_html(FAQ_HOME)
    return '<div class="fairy">' + hero + quote_ + dream + svc + who + story + feed + band + arts + faq + '</div>'


page('', 'Ethel Zhang | Homes, Offices & Shophouses, Singapore',
     'Ethel Zhang, Huttons property agent (CEA %s). Homes, offices, shophouses and business premises, planned with a 10-year D.R.E.A.M. Property Plan. English and 中文.' % CEA,
     'Ethel Zhang', home_body(), hero=False, schema=[faq_schema(FAQ_HOME)])


# ------------------------------------------------------------------------------------------------
# D.R.E.A.M. Method
# ------------------------------------------------------------------------------------------------
DM_FAQ = [('What is the D.R.E.A.M. Method?', 'It is Ethel Zhang\'s five-step way of turning your purpose into a 10-year property roadmap: Discover the dream, Review your financial reality, Evaluate all viable options, Align property with your whole life plan, and Masterplan the execution.'),
          ('How long does it take?', 'A first conversation covers the dream and your financial reality. The options, alignment and plan usually follow over one or two more conversations, depending on how complex your situation is.'),
          ('Is there a fee for the plan?', 'A first conversation costs nothing. Any commission for a purchase, sale or tenancy is agreed with you in writing before work starts.')]
dm_body = '''<section class="sec"><div class="wrap layout"><div class="prose">
<p class="answer">The D.R.E.A.M. Alignment Method is how I turn your purpose into a clear 10-year property roadmap. We start with the life you want, check what is financially realistic, compare every viable option, make sure the choice fits your whole life, and only then plan the steps.</p>
<h2>Why start with purpose?</h2>
<p>Is this property meant to improve your family's lifestyle, grow wealth, produce income, support a life transition or become part of your legacy? When the purpose is unclear, even a good property can become the wrong decision.</p>
''' + ''.join('<h2>%s: %s</h2><p>%s</p>' % (l, t, x) for l, t, x in [
    ('D', 'Discover the dream', 'We talk about where you want to be in 10 years: family, work, lifestyle and what you want property to do for you. This sets the purpose every later step is measured against.'),
    ('R', 'Review your financial reality', 'Cash, CPF, income, existing loans and a buffer for when life changes. We work out a comfortable ceiling, not the most a bank would lend.'),
    ('E', 'Evaluate all viable options', 'Staying, renovating, upgrading, right-sizing, buying a second property or renting: we compare the realistic routes side by side.'),
    ('A', 'Align property with your whole life plan', 'We check the shortlist against your family, career or business, timing and legacy, so the property supports the rest of your plans.'),
    ('M', 'Masterplan the execution', 'A clear sequence, dates and decision points, so you know what happens next and what would make you pause.')]) + '''
<h2>My three secrets</h2>
<ol><li><b>Purpose before property.</b> Identify what the property must accomplish at your present life stage.</li>
<li><b>Connect every decision with D.R.E.A.M.</b> Align property with finances, family, career or business, timing and legacy.</li>
<li><b>Read the whole market before acting.</b> Connect cooling measures, supply, URA plans, macro trends and the details of each property.</li></ol>
<h2>What you leave with</h2>
<p>A personalised D.R.E.A.M. Property Plan: the purpose, the budget ceiling, the option we chose and why, and the steps and dates to get there.</p>
<h2>Common questions</h2>''' + faq_html(DM_FAQ) + '</div>' + aside('Start your D.R.E.A.M. Plan', 'Tell Ethel where you are today and what you are weighing up.', 'Hi Ethel, I would like to start a D.R.E.A.M. Property Plan.') + '</div></section>'
page('dream-method/', 'The D.R.E.A.M. Method: a 10-Year Property Plan | Ethel Zhang',
     'Ethel Zhang\'s D.R.E.A.M. Method turns your purpose into a 10-year property roadmap: Discover, Review, Evaluate, Align, Masterplan.',
     'The D.R.E.A.M. Alignment Method', dm_body, crumbs=[('dream-method/', 'D.R.E.A.M. Method')],
     lede='How to turn your purpose into a clear 10-year property roadmap.', schema=[faq_schema(DM_FAQ)])


# ------------------------------------------------------------------------------------------------
# Scorecard
# ------------------------------------------------------------------------------------------------
SC = [('D', 'Your dream', 'I can clearly describe what my next home must do for my life over the next 10 years.',
       'Write down the two or three things your next home must do that your current one cannot.', 'dream-method/'),
      ('R', 'Your financial reality', 'After this move I would still have a comfortable buffer if my income dropped or interest rates rose.',
       'Test the monthly instalment at a higher rate and keep several months of expenses in cash.', 'articles/should-i-upgrade-or-stay-put/'),
      ('E', 'Your options', 'I have compared at least three realistic routes, including staying where I am.',
       'Put staying, upgrading and at least one other route side by side before choosing.', 'articles/questions-to-ask-before-choosing-a-new-launch/'),
      ('A', 'Your whole life', 'My family\'s needs, my career or business and my timing all point to the same decision.',
       'Check the plan against family, career and timing before committing.', 'articles/how-to-plan-a-10-year-property-roadmap/'),
      ('M', 'Your execution', 'I know my next three steps, the order to do them in and the timeline.',
       'Map the sequence and dates, including a fallback if a step takes longer.', 'articles/sell-first-or-buy-first-singapore/')]
SC_FAQ = [('What is the 10-Year Property Fit Scorecard?', 'A five-question self-check by Ethel Zhang. It shows which part of your property plan (dream, finances, options, whole life or execution) needs more thought before you commit.'),
          ('Is the scorecard free?', 'Yes. Your answers stay in your browser; nothing is sent unless you choose to WhatsApp your result to Ethel.'),
          ('What should I do with a low score?', 'Pause before committing and work on the weakest area first. Ethel can talk it through with you.')]
labels = ['Not at all', 'A little', 'Somewhat', 'Mostly', 'Fully']
sc_form = '<form class="sc" id="scorecard" data-wa="%s">' % WA_NUM + ''.join(
    '<fieldset data-k="%s" data-l="%s" data-tip="%s" data-href="%s"><legend><span class="L">%s</span>%s</legend><p class="q">%s</p><div class="scale">%s</div></fieldset>'
    % (k, E(l), E(tip), href, k, E(l), E(q), ''.join('<label><input type="radio" name="q%s" value="%d" required><span><b>%d</b>%s</span></label>' % (k, v, v, labels[v - 1]) for v in range(1, 6)))
    for k, l, q, tip, href in SC) + '<p id="sc-miss" class="note" hidden></p><button class="btn btn-main" type="submit">See my score</button></form>'
sc_res = '''<div class="res sc" id="sc-res" aria-live="polite" style="margin-top:22px"><span class="eyebrow">Your result</span><div class="tot"></div><p class="band-txt"></p><div class="bars"></div><p class="weakest"></p>
<div class="btns"><a class="btn btn-wa sc-wa" href="contact/" data-fallback="contact/" target="_blank" rel="noopener">''' + WA_SVG + '''<span>Send my result to Ethel</span></a><a class="btn btn-ghost" href="dream-method/">How the D.R.E.A.M. Method works</a></div></div>'''
sc_body = ('<section class="sec"><div class="wrap" style="max-width:860px"><div class="prose"><p class="answer">Many Singapore buyers start with a project. This scorecard shows what to check before you commit. '
           'Rate each statement from 1 to 5, honestly, and see which part of your life, finances and future needs more thought.</p>'
           '<h2>Use it in 3 simple steps</h2><ol><li><b>Score.</b> Answer five questions honestly.</li><li><b>Spot.</b> Find the weakest part of your plan.</li><li><b>Pause.</b> Do not commit until that gap is clearer.</li></ol></div>'
           + '</div></div><div class="wrap" style="max-width:860px;margin-top:10px">' + sc_form + sc_res
           + '<div style="margin-top:40px"><h2>About the scorecard</h2>' + faq_html(SC_FAQ) + '</div></div></section>')
page('scorecard/', '10-Year Property Fit Scorecard (Free) | Ethel Zhang',
     'Free 2-minute scorecard for Singapore buyers: check your dream, finances, options, whole life and execution before your next property move.',
     '10-Year Property Fit Scorecard', sc_body, crumbs=[('scorecard/', 'Scorecard')],
     lede='Five questions, about two minutes. For Singapore Citizens and PRs at a property crossroads.', schema=[faq_schema(SC_FAQ)])


# ------------------------------------------------------------------------------------------------
# Services
# ------------------------------------------------------------------------------------------------
def service(path, crumb, title, desc, h1, lede, sections, faqs, wa_text):
    body = ('<section class="sec"><div class="wrap layout"><div class="prose">' + sections + '<h2>Common questions</h2>' + faq_html(faqs)
            + '<p>See also: <a href="dream-method/">The D.R.E.A.M. Method</a> · <a href="scorecard/">10-Year Property Fit Scorecard</a> · <a href="services/">All services</a></p></div>'
            + aside('Talk to Ethel about ' + crumb.lower(), 'Tell Ethel what you are planning and your timing. A first conversation costs nothing.', wa_text) + '</div></section>')
    page(path, title, desc, h1, body, crumbs=[('services/', 'How I help'), (path, crumb)], lede=lede,
         schema=[faq_schema(faqs), {'@type': 'Service', 'name': crumb, 'serviceType': crumb, 'areaServed': 'Singapore',
                                     'provider': {'@id': SITE + '#ethel'}, 'url': SITE + path}])


service('services/buying-your-next-home/', 'Buying your next home',
        'Buying a Condo or Private Home in Singapore | Ethel Zhang',
        'Buying your next home in Singapore? Ethel Zhang (Huttons, CEA %s) helps singles and couples choose a home that fits the next 10 years.' % CEA,
        'Buying your next home, with the next 10 years in mind.',
        'For singles and couples choosing a private home or their first home. We start with purpose, then find the property.',
        '''<p class="answer">Ethel helps you buy a home by first agreeing what it must do for your life, then setting a comfortable budget, comparing realistic options (new launch, resale, different areas and sizes), and guiding you from shortlist to keys.</p>
<h2>Who this is for</h2>
<ul><li>High-income singles who want speed, privacy and well-reasoned advice.</li><li>Couples buying their first private home or planning for children.</li><li>Buyers who don't want to buy on hype, fear or a single project recommendation.</li></ul>
<h2>How we work</h2>
<ol><li><b>Purpose.</b> What the home must do for you now and in 10 years.</li><li><b>Budget.</b> Cash, CPF, loan and a buffer, before viewing anything.</li><li><b>Options.</b> New launch versus resale, areas and sizes, compared side by side.</li><li><b>Shortlist and viewings.</b> Planned around your schedule.</li><li><b>Offer to keys.</b> Negotiation, Option to Purchase, loan, lawyer and completion.</li></ol>
<h2>What we check on every shortlist</h2>
<p>Location and transport, layout and the size you really need, maintenance fees, tenure, recent transactions in the same development, and who would buy or rent the unit from you later.</p>''',
        [('Do I pay commission when I buy?', 'It depends on the purchase. For many new launches the developer pays the agent; for resale, buyers may pay their own agent. Any fee is agreed with you in writing before Ethel starts work.'),
         ('Can a single buy a condo?', 'Yes. Singapore Citizens can buy private condos without an age requirement. See Ethel\'s article on buying a condo as a single for what to think about first.'),
         ('New launch or resale?', 'Neither is better in general. New launches give staged payments and a new home; resale lets you see exactly what you buy and move in sooner. It depends on your purpose and timing.')],
        'Hi Ethel, I am looking to buy my next home. Budget: , area: , timing: .')

service('services/offices-and-shophouses/', 'Offices and shophouses',
        'Offices & Shophouses in Singapore: Buy, Rent, Invest | Ethel Zhang',
        'Buying, renting or investing in an office or shophouse in Singapore? Ethel Zhang (Huttons, CEA %s) lays out own-use versus investment, costs and tax.' % CEA,
        'Offices and shophouses, for business owners and investors.',
        'Buying, renting or investing in commercial space, with the numbers and the trade-offs clear before you commit.',
        """<p class="answer">Ethel helps business owners and investors buy, rent or invest in offices and shophouses. She starts with what the space must do for you, own use, investment or both, then checks the approved use, tenure, costs, tax and financing, and guides you through to completion.</p>
<h2>Own use or investment</h2>
<p>Owning your premises can give stability and control; renting keeps cash free for the business. As an investment, the tenant, lease and rental demand matter most. Ethel compares the routes side by side with your finances and business plans.</p>
<h2>What we check</h2>
<ul><li>Zoning and approved use, and whether your planned use is allowed.</li><li>Conservation conditions for conserved shophouses.</li><li>Tenure and remaining lease.</li><li>Existing tenancy and rent.</li><li>Stamp duty, GST and financing.</li></ul>
<h2>Costs and tax, plainly</h2>
<p>Additional Buyer's Stamp Duty applies to residential property, not to commercial property. Buyer's Stamp Duty still applies, and GST may be charged if the seller is GST-registered. Commercial loans are set by each bank. Ethel lays these out early and works with your lawyer and accountant on the details.</p>
<h2>Read more</h2>
<p><a href="articles/buying-a-shophouse-in-singapore/">Buying a shophouse in Singapore: what to check first</a></p>""",
        [('Do I pay ABSD on an office or shophouse?', 'ABSD applies to residential property. For commercial property, Buyer\'s Stamp Duty still applies and GST may be charged if the seller is GST-registered. Mixed-use property can be treated differently, so confirm with IRAS and your lawyer.'),
         ('Can Ethel help me rent an office?', 'Yes. She helps business owners find and negotiate office and shophouse leases, and checks the approved use and lease terms.'),
         ('Does Ethel work with foreign-owned businesses?', 'Yes. Many of her clients are business owners originally from Korea, Japan, Indonesia and China. She works in English and Mandarin.')],
        'Hi Ethel, I am looking at an office / shophouse. Purpose (own use or investment): , area: , timing: .')

service('services/business-premises/', 'Business premises and setup',
        'Business Premises & F&B Space in Singapore | Ethel Zhang',
        'Looking for café, F&B or office premises in Singapore? Ethel Zhang, who opened her own CBD café, helps you find the space and plan the setup steps.',
        'Business premises and setup, from someone who has done it.',
        'Finding the right space for your café, clinic or office, and a clear view of the setup steps before you sign.',
        """<p class="answer">Ethel helps entrepreneurs find premises that suit the business and plan the steps from lease to opening day. In 2024 she opened her own café and workspace, EC Coffee Bar, in a CBD conservation shophouse, so she has worked through location, approved use, licensing, fit-out and hiring herself.</p>
<h2>How we work</h2>
<ol><li><b>Your business first.</b> Customers, opening hours, size and budget.</li><li><b>Shortlist.</b> Units whose approved use fits your business.</li><li><b>Setup check.</b> Licences, approvals and fit-out needs for each option.</li><li><b>Lease or purchase.</b> Negotiation, terms and paperwork.</li><li><b>Handover.</b> A timeline from keys to opening day.</li></ol>
<h2>What Ethel brings from running her own café</h2>
<ul><li>Choosing a location that matches the customers.</li><li>Working through approved use and licensing.</li><li>Living with the character, and the rules, of a conservation shophouse.</li><li>Recruiting and opening on a timeline.</li></ul>
<h2>Working with the right professionals</h2>
<p>Licence applications, legal and tax matters sit with the relevant agencies and your consultants. Ethel helps you know what to ask, and coordinates the property side.</p>
<h2>Read more</h2>
<p><a href="articles/finding-fnb-premises-in-the-cbd/">Finding F&amp;B premises in the CBD: a practical checklist</a></p>""",
        [('Can Ethel help me find F&B premises?', 'Yes. She shortlists units whose approved use suits F&B, checks fit-out and licensing needs, and negotiates the lease.'),
         ('Does Ethel apply for licences on my behalf?', 'No. Licence applications go to the relevant agencies, often through your consultants. Ethel guides you on what to check from her own experience and coordinates the property side.'),
         ('Can Ethel help with company relocation to Singapore?', 'She can help find office premises and homes for the people relocating, and introduce the right professionals for company setup.')],
        'Hi Ethel, I am looking for business premises. Business type: , area: , size: , timing: .')

service('services/upgrading/', 'Upgrading your home',
        'Upgrade from HDB to Condo in Singapore | Ethel Zhang',
        'Planning an HDB-to-private or family upgrade? Ethel Zhang plans the budget, sequence and timing so you upgrade without overstretching.',
        'Upgrading your home without overstretching.',
        'From HDB to private, or to a bigger home for a growing family. The right upgrade fits your finances and your future.',
        '''<p class="answer">A good upgrade gives your family something the current home cannot, while leaving a buffer for life changes. Ethel helps you decide whether to upgrade at all, how much to spend, and whether to sell first or buy first, then plans the dates so the move goes smoothly.</p>
<h2>Should you upgrade at all?</h2>
<p>Sometimes staying put or renovating is the better choice. We compare upgrading with the alternatives before looking at any project. Read: <a href="articles/should-i-upgrade-or-stay-put/">Should I upgrade or stay put?</a></p>
<h2>The upgrade plan</h2>
<ol><li>Agree the purpose and the budget ceiling as a family.</li><li>Value your current home and estimate the proceeds.</li><li>Check loan eligibility and stamp duty for your sequence.</li><li>Choose the order: sell first, buy first, or a planned overlap.</li><li>Line up option, exercise and completion dates on both sides.</li></ol>
<h2>Common mistakes we help you avoid</h2>
<ul><li>Choosing the project before the budget.</li><li>Using the bank's maximum loan as the budget.</li><li>Not planning where to live if the sale completes first.</li></ul>''',
        [('When is the right time to upgrade?', 'When the new home clearly serves your plan and the numbers work with a buffer. Market timing matters less than the fit and your sequence.'),
         ('Do I need to sell my HDB before buying a condo?', 'It depends on your situation and the current HDB, loan and stamp duty rules. Ethel will map the options for your case.'),
         ('How long does an upgrade take?', 'From first conversation to moving in can range from a few months to longer for a new launch. We plan the timeline before you start.')],
        'Hi Ethel, I am thinking of upgrading my home. Current home: , timing: .')

service('services/selling/', 'Selling your home',
        'Sell Your Home in Singapore | Ethel Zhang, Huttons',
        'Selling your HDB or condo in Singapore? Ethel Zhang plans the price, timing and your next move so the sale supports your plan.',
        'Selling your home, with your next move ready.',
        'Pricing, presenting and timing your sale so the proceeds arrive when your next home needs them.',
        '''<p class="answer">Ethel sells your home with your next move in mind: a realistic price based on recent transactions, good presentation, steady marketing and negotiation, and completion dates that line up with your next purchase or rental.</p>
<h2>How we sell</h2>
<ol><li><b>Purpose and plan.</b> Why you are selling and where you are going next.</li><li><b>Pricing.</b> Based on recent comparable transactions, not hopes.</li><li><b>Preparation.</b> Small fixes, styling advice and good photos.</li><li><b>Marketing and viewings.</b> Organised so your home life is disrupted as little as possible.</li><li><b>Negotiation and paperwork.</b> Option to Purchase through to completion.</li></ol>
<h2>Sell first or buy first?</h2>
<p>The order changes your cash flow, stamp duty and timing risk. Read: <a href="articles/sell-first-or-buy-first-singapore/">Sell first or buy first in Singapore?</a></p>''',
        [('How do you decide the asking price?', 'From recent transactions of similar homes nearby, the condition of your home and current demand. We agree the price with you before marketing starts.'),
         ('What commission do sellers pay?', 'Commission is agreed with you in writing before work starts, using the CEA prescribed estate agency agreement.'),
         ('Can I stay in my home while it is on the market?', 'Yes. Viewings are planned around your schedule, and completion dates can be agreed to suit your next move.')],
        'Hi Ethel, I am thinking of selling my home. Property: , timing: .')

service('services/property-investment/', 'Investment and portfolio planning',
        'Property Investment Planning in Singapore | Ethel Zhang',
        'Thinking about a second property or an investment condo in Singapore? Ethel Zhang helps you decide if, what and when, with purpose first.',
        'Investment and portfolio planning, purpose first.',
        'Whether a second property makes sense for you, which kind, and how it fits with your home, family and finances.',
        '''<p class="answer">Ethel helps you decide whether an investment property suits you at all, and if so which kind: one that grows wealth, produces rental income or supports a future need. She checks stamp duty, loan limits and holding costs, and reads the whole market before recommending anything.</p>
<h2>Start with what the investment is for</h2>
<ul><li>Long-term wealth growth.</li><li>Rental income.</li><li>A future home for children or parents.</li><li>Part of a retirement or legacy plan.</li></ul>
<h2>Read the whole market before acting</h2>
<p>Cooling measures, supply, URA plans, macro trends and the details of each unit. A good-looking project can still be the wrong investment for your purpose. Read: <a href="articles/questions-to-ask-before-choosing-a-new-launch/">Questions to ask before choosing a new launch</a>.</p>
<h2>The costs people forget</h2>
<p>Stamp duty (including Additional Buyer's Stamp Duty where it applies), loan limits for second properties, maintenance fees, property tax, vacancy periods and repairs. IRAS publishes the <a href="''' + IRAS_ABSD + '''" target="_blank" rel="noopener">current ABSD rules</a>.</p>
<h2>A note on returns</h2>
<p>No one can promise property returns. Ethel's job is to make sure the decision fits your purpose and finances, with the risks clear before you commit.</p>''',
        [('Should I buy a second property?', 'Only if it serves a clear purpose and the numbers work with stamp duty, loan limits and a buffer included. For some people, the better choice is to strengthen their own home first.'),
         ('Is a new launch a good investment?', 'It can be, but it depends on price, supply nearby, your holding period and exit. Compare it with resale options and your purpose first.'),
         ('Can Ethel advise on decoupling or ownership structure?', 'Ownership structure has legal and tax consequences. Ethel will explain the property side and suggest you confirm the legal and tax side with a lawyer and IRAS.')],
        'Hi Ethel, I would like to talk about property investment. Current properties: , goal: .')

service('services/renting-and-leasing/', 'Renting and leasing',
        'Rent Out Your Condo or Find a Home to Rent | Ethel Zhang',
        'Landlords and tenants in Singapore: Ethel Zhang helps with rent setting, tenant screening, tenancy agreements and handover.',
        'Renting and leasing, done properly.',
        'For landlords renting out a home and tenants looking for one, with clear terms on both sides.',
        '''<p class="answer">For landlords, Ethel helps set a realistic rent, market the home, screen tenants and agree a clear tenancy agreement. For tenants, she helps find a home that fits your budget, commute and lease needs, and checks the terms before you sign.</p>
<h2>For landlords</h2>
<ol><li>Prepare and photograph the unit.</li><li>Set the rent from recent comparable rentals.</li><li>Screen tenants: identity, pass validity, household and lease length.</li><li>Agree the tenancy terms and handle the paperwork.</li><li>Joint inventory and condition check at handover.</li></ol>
<p>Read: <a href="articles/renting-out-your-condo-checklist/">Renting out your condo: a landlord checklist</a>.</p>
<h2>For tenants</h2>
<ul><li>A shortlist that fits your budget, commute and move-in date.</li><li>Clear explanation of the lease terms before you sign.</li><li>Help with handover and the inventory list.</li></ul>''',
        [('How do you set the rent?', 'From recent rentals of similar units in the same development and nearby, plus the unit\'s condition and furnishing.'),
         ('Who pays the agent fee for a rental?', 'It depends on the arrangement and is agreed in writing before Ethel starts work.'),
         ('What is checked on a tenant?', 'Identity, the validity of any pass, who will live in the unit, the lease length and the start date.')],
        'Hi Ethel, I would like help with a rental. I am a landlord / tenant. Area: , timing: .')

service('services/retirement-and-legacy/', 'Retirement, family and legacy',
        'Right-Sizing, Retirement and Legacy Property Planning | Ethel Zhang',
        'Planning to right-size, house your parents or plan a property legacy in Singapore? Ethel Zhang helps you plan the move around your family.',
        'Retirement, family and legacy planning.',
        'Right-sizing, planning around parents and children, and what you want your property to leave behind.',
        '''<p class="answer">Ethel helps families plan property around the next stage of life: right-sizing to free up cash or reduce upkeep, living near or with parents, preparing a home for children, and thinking about legacy. Each plan starts with what the family wants, then the numbers and the steps.</p>
<h2>Common situations</h2>
<ul><li>Children have moved out and the home is now too big.</li><li>Parents need to live closer, or with you.</li><li>You want to plan which property goes to whom, and when.</li><li>You want simpler living and less upkeep in retirement.</li></ul>
<h2>How we plan it</h2>
<ol><li>Agree the family's priorities, and who needs to be part of the decision.</li><li>Review the finances: proceeds, CPF, costs and income in retirement.</li><li>Compare options: right-size, stay and adapt, or a two-step move.</li><li>Plan the timing around the family, not only the market.</li></ol>
<h2>Working with your other advisers</h2>
<p>Wills, trusts, CPF and tax questions belong with the right professionals. Ethel coordinates the property side and makes sure it fits the rest of the plan.</p>''',
        [('When should we think about right-sizing?', 'When the home no longer fits how you live, or when freeing up cash or reducing upkeep would make retirement easier. Planning a few years ahead gives more choice.'),
         ('Can Ethel help with buying a home near our parents?', 'Yes. Location, layout for different generations and the right ownership arrangement are all part of the plan.'),
         ('Does Ethel give legal or tax advice?', 'No. Ethel handles the property side and works alongside your lawyer, financial adviser or tax adviser.')],
        'Hi Ethel, I would like to plan a move for my family / retirement. Situation: .')

svc_hub = ('<section class="sec"><div class="wrap"><div class="prose" style="margin-bottom:28px"><p class="answer">Ethel Zhang is a long-term property adviser for every stage of life. '
           'Instead of focusing on one project, location or property type, she helps individuals and families make the right decision as their lives change: '
           'from renting and buying a first home to upgrading, investing, restructuring and planning for retirement. She also helps business owners with offices, shophouses and business premises.</p></div>' + service_cards() + '</div></section>')
page('services/', 'How Ethel Helps: Buy, Upgrade, Sell, Invest, Rent | Ethel Zhang',
     'Buying, upgrading, selling, investing, renting and retirement planning in Singapore, with Ethel Zhang\'s purpose-first approach.',
     'A property adviser for every stage of life', svc_hub, crumbs=[('services/', 'How I help')],
     lede='People come back to me because I understand their changing lives, not just property.')


# ------------------------------------------------------------------------------------------------
# About, articles hub, contact, privacy
# ------------------------------------------------------------------------------------------------
def cred():
    return f'''<div class="cred"><img src="img/ethel.webp" alt="Ethel Zhang" width="120" height="154" loading="lazy"><div><h3>{NAME}</h3>
<span style="color:var(--muted)">{TITLE}, {AGENCY}</span>
<dl><dt>CEA Reg. No.</dt><dd>{CEA}</dd><dt>Agency licence</dt><dd>{AGENCY_LIC}</dd><dt>In real estate</dt><dd>Full-time since 2018</dd><dt>Languages</dt><dd>English, Mandarin</dd></dl>
<p style="margin-top:12px"><a href="{CEA_REG}" target="_blank" rel="noopener">Check on the CEA Public Register ↗</a> · <a href="{PG_URL}" target="_blank" rel="noopener">PropertyGuru profile ↗</a></p></div></div>'''


cafe_line = ('<a href="%s" target="_blank" rel="noopener">%s</a>, ' % (CAFE[1], CAFE[0])) if CAFE else ''
about_body = ('<section class="sec"><div class="wrap layout"><div class="prose">'
              '<figure class="lead-fig"><img src="img/lily.webp" alt="Portrait of Ethel Zhang with white lilies" width="560" height="560" fetchpriority="high"><figcaption>Ethel, from her own Instagram: "Trust the flow of life."</figcaption></figure>'
              '<p class="answer">Ethel Zhang is a Singapore property agent with %s who helps financially capable Singaporeans and PRs connect property decisions with the life they want over the next 10 years. '
              'Her background in finance and economics, eight years in full-time real estate and work with more than 100 families shape a practical, whole-life approach.</p>' % AGENCY
              + '<h2>Why I work this way</h2><p>I am not the kind of agent who only sells one project, one area or one type of home. What stays constant in my work is people and relationships. I follow my clients through their life stages: renting, buying a first home, upgrading, selling, investing, family arrangements, and sometimes coming back to me many years later.</p>'
              '<p>My own decisions have included moving from one private home to a two-condo structure, an idea first sparked by <i>Rich Dad Poor Dad</i>, while building a business in Singapore. That experience shaped my belief that property must leave room for family, work and future choices.</p>'
              '<h2>Homes and business, in two languages</h2><p>Running my own café since 2024 taught me what business owners worry about: location, approved use, licensing, hiring and cash flow. Today I help families with their homes and entrepreneurs with offices, shophouses and business premises, often both at once. I work in English and 中文, so clients from Singapore, China, Korea, Japan and Indonesia can talk through big decisions in the language they are most comfortable with.</p>'
              '<h2>My property journey</h2><ol class="tl">' + ''.join('<li><span class="yr">%s</span><span class="age">Age %d</span><p>%s</p></li>' % (y, a, t.replace('{cafe}', ', %s,' % cafe_line.rstrip(', ') if CAFE else '') + ('<figure><img src="img/cafe-poster.webp" alt="Ethel at her laptop with a latte in her cafe" width="640" height="853" loading="lazy"></figure>' if y == '2024' else '')) for y, a, t in TIMELINE) + '</ol>'
              '<h2>Always learning</h2><figure class="lead-fig" style="max-width:420px"><img src="img/masterclass.webp" alt="Ethel at a masterclass in Kuala Lumpur, holding a paper gratitude flower" width="640" height="855" loading="lazy"><figcaption>At a masterclass in Kuala Lumpur, March 2026.</figcaption></figure><p>I have flown to Taiwan nine times for masterclasses, walked on fire at Tony Robbins\' Unleash the Power Within in 2019, and attended Date with Destiny in the USA in 2023. I invest in my own growth because my clients deserve an adviser who keeps getting better.</p>'
              '<h2>What I believe</h2><blockquote style="margin:0;font-family:var(--serif);font-size:1.3rem;color:var(--navy)">"Your next property decision should not begin with a project. It should begin with the life you want that property to support."</blockquote>'
              '<h2>Credentials</h2>' + cred() + '</div>'
              + aside('Work with Ethel', 'Tell Ethel where you are in life and what you are considering next.', 'Hi Ethel, I read your story on your website. I would like to talk about my property plans.') + '</div></section>')
page('about/', 'About Ethel Zhang | Singapore Property Adviser, Huttons',
     'Ethel Zhang: 8 years full-time in Singapore real estate, 100+ families, Huttons (CEA %s). Homes, offices and shophouses, in English and Chinese.' % CEA,
     'About Ethel Zhang', about_body, crumbs=[('about/', 'About')], lede='From dreaming of a condo at 18 to advising more than 100 families.', kind='AboutPage')

arts_body = ('<section class="sec"><div class="wrap"><p class="lede" style="max-width:760px;color:var(--muted);margin-bottom:28px">Plain-English guides for Singapore buyers, sellers, upgraders, investors and landlords. Each one starts with the answer.</p>'
             + article_cards(ARTICLES) + '</div></section>')
page('articles/', 'Property Articles for Singapore Buyers and Owners | Ethel Zhang',
     'Articles by Ethel Zhang on upgrading, buying as a single, new launches, selling and renting in Singapore, with a 10-year view.',
     'Articles', arts_body, crumbs=[('articles/', 'Articles')], lede='Clear thinking for big property decisions.', kind='CollectionPage')

opts = ['Buying my next home', 'Upgrading', 'Selling', 'Investment property', 'Renting out / renting', 'Retirement, family or legacy', 'Not sure yet']
contact_body = (f'''<section class="sec"><div class="wrap split"><div class="prose"><p class="answer">The quickest way to reach Ethel is WhatsApp. Tell her what you are considering, your stage of life and your timing, and she will get back to you.</p>
<h2>Contact details</h2><ul><li><b>WhatsApp:</b> {WA_SHOW or 'number coming soon'}</li><li><b>Agency:</b> {AGENCY} (licence {AGENCY_LIC})</li><li><b>CEA Reg. No.:</b> {CEA}</li>
<li><b>Social:</b> <a href="{SOCIAL['Instagram']}" target="_blank" rel="noopener">Instagram</a> · <a href="{SOCIAL['Facebook']}" target="_blank" rel="noopener">Facebook</a> · <a href="{PG_URL}" target="_blank" rel="noopener">PropertyGuru</a></li></ul>
<p lang="zh">欢迎用中文联系 Ethel，咨询住宅、办公室、店屋或商业场地。</p>
<p>Not ready to talk yet? Try the <a href="scorecard/">10-Year Property Fit Scorecard</a> first.</p></div>
<form class="cform" id="enquiry" data-wa="{WA_NUM}"><h2 style="margin:0">Send Ethel a message</h2>
<label>What would you like to talk about?<select name="o">''' + ''.join('<option>%s</option>' % o for o in opts) + '''</select></label>
<label>Your stage of life (optional)<input name="s" placeholder="e.g. single, married with young kids, parents moving in"></label>
<label>Timing<select name="t"><option>Just exploring</option><option>In the next 3 months</option><option>In 3 to 12 months</option><option>More than a year away</option></select></label>
<label>Your name<input name="n" autocomplete="name"></label>
<label>Anything else? (optional)<textarea name="x" rows="3"></textarea></label>
<button class="btn btn-wa" type="submit">''' + WA_SVG + '''<span>Continue on WhatsApp</span></button>
<p class="note" style="margin:0">This opens WhatsApp with your message filled in. Nothing is stored on this website.</p></form></div></section>''')
page('contact/', 'Contact Ethel Zhang | WhatsApp, Huttons Property Agent',
     'Contact Ethel Zhang, Huttons property agent (CEA %s), on WhatsApp about buying, upgrading, selling, investing or renting in Singapore.' % CEA,
     'Contact Ethel', contact_body, crumbs=[('contact/', 'Contact')], lede='Tell Ethel what you are planning. A first conversation costs nothing.', cta=False, kind='ContactPage')

privacy_body = '''<section class="sec"><div class="wrap prose"><p>This website is run by Ethel Zhang. It does not use forms that store your details: the contact form and the scorecard open WhatsApp with a message you can review and choose to send.</p>
<h2>What we collect</h2><p>Only what you choose to send by WhatsApp, email or phone, such as your name, contact number and details of your property plans.</p>
<h2>How we use it</h2><p>To reply to you and advise on your property matters. We do not sell your personal data. We follow the Personal Data Protection Act (PDPA) and the Do Not Call rules.</p>
<h2>Website analytics</h2><p>We may count visits and button taps anonymously to understand which pages are useful.</p>
<h2>Your choices</h2><p>You can ask us to stop contacting you, or to access or correct your data, at any time by messaging Ethel.</p></div></section>'''
page('privacy/', 'Privacy Policy | Ethel Zhang', 'How Ethel Zhang handles personal data under the PDPA.', 'Privacy Policy', privacy_body,
     crumbs=[('privacy/', 'Privacy')], cta=False)


# ------------------------------------------------------------------------------------------------
# Render
# ------------------------------------------------------------------------------------------------
def person_schema():
    p = {'@type': ['RealEstateAgent', 'Person'], '@id': SITE + '#ethel', 'name': NAME, 'jobTitle': 'Property Agent (%s)' % TITLE,
         'url': SITE, 'image': ASSET + 'img/hero.webp', 'description': 'Relationship-based property adviser in Singapore for homes, offices and shophouses, for every stage of life and business.',
         'worksFor': {'@type': 'RealEstateAgent', 'name': AGENCY, 'identifier': {'@type': 'PropertyValue', 'propertyID': 'CEA Estate Agent Licence', 'value': AGENCY_LIC}},
         'identifier': {'@type': 'PropertyValue', 'propertyID': 'CEA Registration', 'value': CEA},
         'areaServed': {'@type': 'Country', 'name': 'Singapore'}, 'knowsLanguage': ['en', 'zh'],
         'sameAs': list(SOCIAL.values()),
         'knowsAbout': ['Singapore residential property', 'Office and shophouse property', 'Commercial premises for F&B and business',  'Condominium purchase', 'HDB to private upgrading', 'Property selling',
                        'Property investment planning', 'Residential leasing', 'Retirement and legacy property planning']}
    if WA_NUM:
        p['telephone'] = '+' + WA_NUM
    return p


NAV_ZH = [('dream-method/', 'D.R.E.A.M. 方法'), ('services/', '服务项目'), ('scorecard/', '评分卡'),
          ('about/', '关于我'), ('articles/', '文章'), ('contact/', '联系')]
ZH = {'home': '首页', 'skip': '跳到正文', 'sub': '房产顾问', 'menu': '菜单', 'wa': 'WhatsApp',
      'strip_wa': 'WhatsApp ', 'ftr_tag': '陪伴您每个人生阶段的房产顾问。', 'explore': '探索', 'privacy': '隐私政策', 'contact': '联系方式',
      'cea': 'CEA 公共注册', 'band_h': '准备好规划下一步了吗？', 'band_p': '告诉 Ethel 您目前的情况和正在考虑的方向，无需任何承诺。',
      'band_wa': '您好 Ethel，我在您的网站上看到您的信息，想聊聊我的房产计划。', 'wa_main': '您好 Ethel，我在您的网站上看到您的信息，我有一个房产问题。',
      'dock': 'WhatsApp Ethel', 'legal': '网站及 SEO 由', 'brandlbl': 'Ethel Zhang，首页', 'wa_btn': 'WhatsApp Ethel'}


def render(path, p, lang='en'):
    zh = lang == 'zh'
    rel = path[3:] if zh else path
    pre = '../' * path.count('/')
    url = SITE + path
    nav_items = NAV_ZH if zh else NAV
    zp = 'zh/' if zh else ''
    if rel == '' and not zh:
        alt_en, alt_zh = SITE, SITE + 'zh/'
    else:
        alt_en, alt_zh = SITE + rel, SITE + 'zh/' + rel
    switch = ('<a class="lang" href="%s%s" hreflang="en" lang="en" aria-label="Switch to English">EN</a>' % (pre, rel or './')) if zh else \
             ('<a class="lang" href="%szh/%s" hreflang="zh-Hans" lang="zh-Hans" aria-label="切换到中文">中文</a>' % (pre, rel))

    def fix(s):
        return re.sub(r'(href|src)="(?!https?:|mailto:|#|\.\./|data:|/)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2) or './'), s)

    nav = ''.join('<a href="%s%s%s"%s>%s</a>' % (pre, zp, h, ' aria-current="page"' if rel.startswith(h) else '', t) for h, t in nav_items)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s%s">%s</a>' % (pre, zp, ZH['home'] if zh else 'Home')] + ['<a href="%s%s%s">%s</a>' % (pre, zp, h, E(t)) for h, t in p['crumbs'][:-1]] + [E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': ZH['home'] if zh else 'Home', 'item': SITE + zp}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + zp + h} for i, (h, t) in enumerate(p['crumbs'])]}
    share = ASSET + 'img/share/home.jpg'
    graph = [person_schema(), {'@type': p['kind'] if p['kind'] != 'Article' else 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'],
                               'description': p['desc'], 'inLanguage': 'zh-CN' if zh else 'en-SG', 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': NAME}}]
    if crumbs_ld:
        graph.append(crumbs_ld)
    graph += p['schema']
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('</', '<\\/')
    head_hero = ''
    if p['hero']:
        head_hero = '<section class="phero"><div class="wrap">%s<h1>%s</h1>%s</div></section>' % (
            crumbs_html, E(p['h1']), '<p class="lede">%s</p>' % E(p['lede']) if p['lede'] else '')
    band = ''
    if p['cta']:
        band = ('<section class="sec" style="padding-top:8px"><div class="wrap"><div class="band"><div><h2>%s</h2>'
                '<p>%s</p></div>%s</div></div></section>') % (ZH['band_h'] if zh else 'Ready to plan your next move?',
            ZH['band_p'] if zh else 'Tell Ethel where you are and what you are weighing up. No obligation.',
            wa_btn(ZH['band_wa'], ZH['wa_btn']) if zh else wa_btn('Hi Ethel, I found your website. I would like to talk about my property plans.'))
    robots = 'noindex,nofollow' if NOINDEX else 'index,follow,max-image-preview:large'
    title = E(p['title'])
    wa_main = ZH['wa_main'] if zh else 'Hi Ethel, I found your website. I have a property question.'
    ext = ' target="_blank" rel="noopener"' if WA_NUM else ''
    body = fix(head_hero + p['body'] + band)
    return f'''<!doctype html>
<html lang="{'zh-CN' if zh else 'en-SG'}" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
<meta name="robots" content="{robots}">
<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#b24a7c">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en-SG" href="{alt_en}">
<link rel="alternate" hreflang="zh-Hans" href="{alt_zh}">
<link rel="alternate" hreflang="x-default" href="{alt_en}">
<meta property="og:type" content="{'article' if p['kind'] == 'Article' else 'website'}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{share}">
<meta property="og:image:secure_url" content="{share}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{'zh_CN' if zh else 'en_SG'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{share}">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Great+Vibes&family=Playfair+Display:ital,wght@0,600;1,600&display=swap">
<link rel="stylesheet" href="{pre}ethel.css?v=11">
<script src="{pre}ethel.js?v=3" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">{'跳到正文' if zh else 'Skip to content'}</a>
<div class="strip"><div class="wrap"><span>{NAME} · {TITLE}, {AGENCY} · Licence {AGENCY_LIC} · CEA Reg. {CEA}</span><a href="{E(fix('href="' + wa(wa_main) + '"')[6:-1])}"{ext}>{('WhatsApp ' + WA_SHOW) if WA_SHOW else ('联系 Ethel' if zh else 'Contact Ethel')}</a></div></div>
<header class="hdr"><div class="wrap">
<a class="brand" href="{(pre + zp) or './'}" aria-label="{ZH['brandlbl'] if zh else 'Ethel Zhang, home page'}">{MARK}<span><span class="brand-name">Ethel Zhang</span><span class="brand-sub">{ZH['sub'] if zh else 'Property adviser'}</span></span></a>
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
{switch}
{fix(wa_btn(wa_main, 'WhatsApp'))}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">{ZH['menu'] if zh else 'Menu'}</button>
</div></header>
<main id="main">
{body}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div><a class="brand" href="{(pre + zp) or './'}">{MARK}<span><span class="brand-name">Ethel Zhang</span><span class="brand-sub">{ZH['sub'] if zh else 'Property adviser'}</span></span></a>
<p style="margin-top:16px">{ZH['ftr_tag'] if zh else 'Your trusted property adviser through every stage of life.'}</p></div>
<div><h3>{ZH['explore'] if zh else 'Explore'}</h3><ul>{''.join('<li><a href="%s%s%s">%s</a></li>' % (pre, zp, h, t) for h, t in nav_items)}<li><a href="{pre}{zp}privacy/">{ZH['privacy'] if zh else 'Privacy'}</a></li></ul></div>
<div><h3>{ZH['contact'] if zh else 'Contact'}</h3><ul>
<li><a href="{E(fix('href="' + wa(wa_main) + '"')[6:-1])}"{ext}>{('WhatsApp ' + WA_SHOW) if WA_SHOW else 'Contact Ethel'}</a></li>
<li><a href="{SOCIAL['Instagram']}" target="_blank" rel="noopener">Instagram</a> · <a href="{SOCIAL['Facebook']}" target="_blank" rel="noopener">Facebook</a> · <a href="{PG_URL}" target="_blank" rel="noopener">PropertyGuru</a></li>
<li><a href="{CEA_REG}" target="_blank" rel="noopener">{ZH['cea'] if zh else 'CEA Public Register'}</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>{NAME} · {TITLE} · CEA Reg. No. {CEA} · {AGENCY} · Estate Agent Licence No. {AGENCY_LIC}</span><span>© 2026 Ethel Zhang · {'网站及 SEO 由' if zh else 'Website &amp; SEO by'} <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<a class="dock" href="{E(fix('href="' + wa(wa_main) + '"')[6:-1])}"{ext} aria-label="WhatsApp Ethel Zhang"><img src="{pre}img/wa.webp" alt="" width="40" height="40"><span>WhatsApp Ethel</span></a>
</body>
</html>
'''


def not_found():
    body = ('<section class="sec"><div class="wrap prose"><p>The page you were looking for has moved or does not exist. These may help:</p>'
            '<ul>%s</ul></div></section>') % ''.join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in [('', 'Home')] + NAV)
    p = dict(title='Page not found | Ethel Zhang', desc='This page could not be found.', h1='Sorry, that page is not here.', body=body,
             crumbs=None, lede='', schema=[], hero=True, cta=True, kind='WebPage')
    out = render('', p).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    base = '/' if LIVE else '/preview/%s/' % SLUG
    return re.sub(r'(href|src)="(?!https?:|mailto:|#|/|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), base, '' if m.group(2) == './' else m.group(2)), out)


HTACCESS = """# Ethel Zhang ({DOMAIN}). Document root of {DOMAIN}; also pageonesingapore.com/preview/ethel-zhang/.
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTP_HOST} ^{DQ}$ [NC]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://{DOMAIN}/$1 [L,R=301]
<IfModule mod_headers.c>
<FilesMatch "\\.html$">
Header set Cache-Control "max-age=3600, must-revalidate"
</FilesMatch>
</IfModule>
ErrorDocument 404 /404.html
"""

ROBOTS = """User-agent: *
Allow: /

# Search and AI assistants are welcome
User-agent: Googlebot
User-agent: Bingbot
User-agent: OAI-SearchBot
User-agent: GPTBot
User-agent: ChatGPT-User
User-agent: PerplexityBot
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: DuckAssistBot
Allow: /

Sitemap: {SITE}sitemap.xml
"""

INDEXNOW = 'e7a1c3f95b2d4e6a8c0f1b3d5e7a9c2f'


def load_zh():
    out = {}
    for path, p in PAGES.items():
        key = path.strip('/').replace('/', '__') or 'home'
        fn = os.path.join(HERE, 'zh', key + '.json')
        if not os.path.exists(fn):
            continue
        z = json.load(open(fn))
        q = dict(p)
        for k in ('title', 'desc', 'h1', 'lede', 'crumbs', 'schema'):
            if k in z:
                q[k] = z[k]
        def link(m):
            h = m.group(2)
            if h.startswith(('img/', 'ethel', 'favicon', 'icon', 'site.', 'manual')) or h.endswith(('.webp', '.png', '.jpg', '.svg', '.css', '.js')):
                return m.group(0)
            return 'href="zh/%s"' % ('' if h in ('', './') else h)
        body = z['body']
        if key == 'articles' and ZH_AUTO_CARDS:
            _i = body.index('</a></div>', body.index('<div class="acards">')) + len('</a>')
            body = body[:_i] + ''.join(ZH_AUTO_CARDS) + body[_i:]
        for _s, _u in LEGACY_IMG.items():
            body = re.sub(r'(href="articles/%s/"><span class="thumb t\d+"><img src=")img/[a-z0-9-]+\.webp' % re.escape(_s), lambda m: m.group(1) + _u, body)
            if key == 'articles__' + _s:
                body = re.sub(r'(<figure class="lead-fig art-fig"><img src=")img/[a-z0-9-]+\.webp', lambda m: m.group(1) + _u, body)
        body = re.sub(r'(href)="(?!https?:|mailto:|tel:|#|\.\./|data:|/)([^"]*)"', link, body)
        def punct(m):
            t = m.group(1)
            t = re.sub(r'(?<=[\u4e00-\u9fff\u3000-\u303f]),\s*', '，', t)
            t = re.sub(r'(?<=[\u4e00-\u9fff]);\s*', '；', t)
            t = re.sub(r'(?<=[\u4e00-\u9fff]):(?!//)', '：', t)
            t = re.sub(r'(?<=[\u4e00-\u9fff])\?', '？', t)
            t = re.sub(r'(?<=[\u4e00-\u9fff])!', '！', t)
            return '>' + t + '<'
        body = re.sub(r'>([^<]+)<', punct, body)
        q['body'] = body
        def fw(t):
            t = re.sub(r'(?<=[\u4e00-\u9fff]),\s*', '，', t)
            t = re.sub(r'(?<=[\u4e00-\u9fff]);\s*', '；', t)
            t = re.sub(r'(?<=[\u4e00-\u9fff]):(?!//)', '：', t)
            return t
        for k in ('h1', 'lede', 'desc', 'title'):
            q[k] = fw(q[k])
        for g in q['schema']:
            if isinstance(g, dict) and 'inLanguage' in g:
                g['inLanguage'] = 'zh-CN'
        out[path] = q
    return out


ZHPAGES = {}


def main():
    global ZHPAGES
    ZHPAGES = load_zh()
    for path, p in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(render(path, p))
    for path, p in ZHPAGES.items():
        d = os.path.join(OUT, 'zh', path)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(render('zh/' + path, p, 'zh'))
    with open(os.path.join(OUT, '404.html'), 'w') as f:
        f.write(not_found())
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write(ROBOTS.replace('{SITE}', SITE))
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
        for path in PAGES:
            if path != 'privacy/':
                f.write('  <url><loc>%s%s</loc><lastmod>%s</lastmod><xhtml:link rel="alternate" hreflang="en-SG" href="%s%s"/><xhtml:link rel="alternate" hreflang="zh-Hans" href="%szh/%s"/></url>\n' % (SITE, path, TODAY, SITE, path, SITE, path))
        for path in ZHPAGES:
            if path != 'privacy/':
                f.write('  <url><loc>%szh/%s</loc><lastmod>%s</lastmod><xhtml:link rel="alternate" hreflang="en-SG" href="%s%s"/><xhtml:link rel="alternate" hreflang="zh-Hans" href="%szh/%s"/></url>\n' % (SITE, path, TODAY, SITE, path, SITE, path))
        f.write('</urlset>\n')
    with open(os.path.join(OUT, INDEXNOW + '.txt'), 'w') as f:
        f.write(INDEXNOW)
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write('# Ethel Zhang, Singapore property adviser\n\n'
                '> Ethel Zhang is a property agent and %s with %s (Estate Agent Licence %s), CEA registration %s. '
                'Full-time in Singapore real estate since 2018, she has worked with more than 100 families and recorded 47 transactions in the three years to October 2026 (PropertyGuru). '
                'She is a relationship-based residential adviser for every stage of life: buying, upgrading, selling, investment planning, renting and retirement or legacy planning, '
                'using her D.R.E.A.M. Method (Discover, Review, Evaluate, Align, Masterplan) to build a 10-year property plan. '
                'She also helps business owners buy, rent or invest in offices and shophouses and find F&B and business premises, drawing on running her own CBD café (EC Coffee Bar) since 2024. '
                'She works in English and Mandarin, mainly with Singapore Citizens, PRs and business owners aged around 30 to 50. Website: %s\n\n## Pages\n' % (TITLE, AGENCY, AGENCY_LIC, CEA, SITE))
        for path, p in PAGES.items():
            f.write('- [%s](%s%s): %s\n' % (p['title'].split(' | ')[0], SITE, path, p['desc']))
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': 'Ethel Zhang', 'short_name': 'Ethel Zhang', 'icons': [
            {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
            'theme_color': '#b24a7c', 'background_color': '#fffafb', 'display': 'browser'}, f)
    with open(os.path.join(OUT, 'favicon.svg'), 'w') as f:
        f.write(MARK.replace(' class="brand-mark"', ' xmlns="http://www.w3.org/2000/svg"').replace(' aria-hidden="true"', ''))
    dq = DOMAIN.replace('.', r'\.')
    os.makedirs(os.path.join(HERE, 'manual-upload'), exist_ok=True)
    with open(os.path.join(HERE, 'manual-upload', 'htaccess.txt'), 'w') as f:
        f.write(HTACCESS.replace('{DOMAIN}', DOMAIN).replace('{DQ}', dq))
    with open(os.path.join(HERE, 'CONFIRM.txt'), 'w') as f:
        f.write(CONFIRM)
    print('built %d pages' % len(PAGES))


if __name__ == '__main__':
    main()
