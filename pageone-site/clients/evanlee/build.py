"""Evan Lee Homes: builds every page into site/ (python3 build.py).

Copy, FAQ and business details live at the top of this file. Only facts from Evan's business card
(13 Oct 2026) and Edwin are claimed: no invented years, sales figures, reviews or awards.
"""
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')

SLUG = 'evanlee'
DOMAIN = 'evanleehomes.com'          # change here once Edwin confirms the domain, then rebuild
LIVE = False                         # True once DOMAIN serves this folder (images then use DOMAIN)
NOINDEX = False
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = 'https://%s/' % DOMAIN
ASSET = SITE if LIVE else PREVIEW

NAME, NAME_ZH = 'Evan Lee', '李敏彦'
TITLE = 'Associate'
DIVISION = 'Anthony Sentosa Siantar Division'
# From Evan's ERA Explorer Group award posts on Instagram/TikTok (screenshots sent by Edwin, 13 Oct 2026).
AWARDS = [('Top 100 Achievers', '8th place, Super Gold', 'ERA Explorer Group, July 2026'),
          ('Top 5 New Achievers', '3rd place', 'ERA Explorer Group, 2026')]
AGENCY, AGENCY_LIC = 'ERA Realty Network Pte Ltd', 'L3002382K'
CEA = 'R074252A'
WA_NUM, WA_SHOW = '6588242798', '+65 8824 2798'
EMAIL = 'evanleehomes@gmail.com'
OFFICE = ['ERA APAC Centre', '450 Lorong 6 Toa Payoh', 'Singapore 319394']
MAP = 'https://www.google.com/maps/search/?api=1&query=ERA+APAC+Centre+450+Lorong+6+Toa+Payoh+Singapore+319394'
SOCIAL = {
    'Facebook': 'https://www.facebook.com/evanleeproperties/',
    'Instagram': 'https://www.instagram.com/evanlee.homes/',
    'TikTok': 'https://www.tiktok.com/@evanleehomes',
    'ERA profile': 'https://profile.era.com.sg/%s' % CEA,
}
SAME_AS = [SOCIAL['Facebook'], SOCIAL['Instagram'], SOCIAL['TikTok'], SOCIAL['ERA profile']]

NAV = [('buy/', 'Buy'), ('sell/', 'Sell'), ('upgrade/', 'Upgrade'), ('rent/', 'Rent'),
       ('stamp-duty-calculator/', 'Stamp duty'), ('guides/', 'Guides'), ('about/', 'About'), ('contact/', 'Contact')]

E = html.escape


def wa(text):
    from urllib.parse import quote
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(text))


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 '
          '11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>')


def wa_btn(text, label='WhatsApp Evan', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa(text)), WA_SVG, E(label))


ICONS = {
    'buy': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M17 6l2 2M15 8l2 2"/></svg>',
    'sell': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9-9-9Z"/><circle cx="8" cy="8" r="1.6"/></svg>',
    'upgrade': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21h18M5 21V11l7-6 7 6v10"/><path d="M12 17v-6M9.5 13.5 12 11l2.5 2.5"/></svg>',
    'rent': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V4a1 1 0 0 1 1-1h10a1 1 0 0 1 1 1v17"/><path d="M2 21h20M13 12h.01"/><path d="M16 7h3a1 1 0 0 1 1 1v13"/></svg>',
}

MARK = ('<svg class="brand-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#16202e"/>'
        '<path d="M8 21 20 10l12 11" fill="none" stroke="#c8102e" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"/>'
        '<text x="20" y="32" text-anchor="middle" font-family="Arial,Helvetica,sans-serif" font-weight="800" font-size="11.5" fill="#fff" letter-spacing=".5">EL</text></svg>')

HERO_ART = '''<svg viewBox="0 0 520 440" role="img" aria-label="Line drawing of an HDB block, a condominium tower and terrace houses">
<circle cx="392" cy="92" r="58" fill="#f1e9dd"/>
<g fill="none" stroke="#16202e" stroke-width="2.2" stroke-linejoin="round">
<rect x="40" y="120" width="128" height="268" rx="3"/>
<path d="M40 150h128M40 182h128M40 214h128M40 246h128M40 278h128M40 310h128M40 342h128" stroke-width="1.2"/>
<path d="M72 120v268M104 120v268M136 120v268" stroke-width="1.2"/>
<rect x="88" y="352" width="32" height="36" fill="#fbf8f3"/>
<rect x="206" y="64" width="96" height="324" rx="3"/>
<path d="M206 96h96M206 128h96M206 160h96M206 192h96M206 224h96M206 256h96M206 288h96M206 320h96M206 352h96" stroke-width="1.2"/>
<path d="M198 96h8M302 96h8M198 160h8M302 160h8M198 224h8M302 224h8M198 288h8M302 288h8" stroke-width="2.2"/>
<path d="M254 64V42" stroke-width="1.6"/>
<path d="M330 388V300l38-34 38 34v88M406 388V300l38-34 38 34v88" />
<rect x="352" y="336" width="32" height="52"/><rect x="428" y="336" width="32" height="52"/>
<rect x="352" y="302" width="32" height="20" stroke-width="1.4"/><rect x="428" y="302" width="32" height="20" stroke-width="1.4"/>
<path d="M14 388h492" stroke-width="2.6"/>
</g>
<path d="M150 262 278 158l128 104" fill="none" stroke="#c8102e" stroke-width="7" stroke-linejoin="round" stroke-linecap="round"/>
<path d="M176 246v142M380 246v142" fill="none" stroke="#c8102e" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>
</svg>'''

# Short text used in several places
FAQ_HOME = [
    ('Who is Evan Lee?', 'Evan Lee (李敏彦) is a property agent and Associate with ERA Realty Network Pte Ltd (Estate Agent Licence %s). His CEA registration number is %s, which you can check on the CEA Public Register.' % (AGENCY_LIC, CEA)),
    ('What can Evan help with?', 'Buying a home (HDB resale, condominium or landed), selling your property, planning an HDB-to-private upgrade, and renting out or finding a place to rent.'),
    ('How do I contact Evan?', 'The quickest way is WhatsApp at %s. Tell him what you are planning, the area you have in mind and your timing, and he will get back to you.' % WA_SHOW),
    ('Where is Evan based?', 'Evan works from ERA APAC Centre, 450 Lorong 6 Toa Payoh, Singapore 319394, and helps buyers, sellers, landlords and tenants across Singapore.'),
    ('How much does it cost to talk to Evan?', 'A first conversation about your plans costs nothing. Commission for a sale, purchase or tenancy is agreed with you in writing before any work starts, using the CEA prescribed estate agency agreement.'),
]

PAGES = {}


def page(path, title, desc, h1, body, crumbs=None, lede='', share=None, schema=None, hero=True, cta=True):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede,
                       share=share or path.strip('/').replace('/', '-') or 'home', schema=schema or [], hero=hero, cta=cta)


# ----------------------------------------------------------------------------------------------
# Home
# ----------------------------------------------------------------------------------------------
AWARD_IMGS = [('award-top100.webp', 236, 269, 'Top 100 Achievers poster, 8th place, Super Gold, July 2026', 'Top 100 Achievers, July 2026'),
              ('award-top5.webp', 236, 269, 'Top 5 New Achievers poster, 3rd place', 'Top 5 New Achievers, 3rd place'),
              ('award-ceremony.webp', 239, 240, 'Evan Lee receiving his Top 5 New Achievers award', 'Receiving his award')]
# Evan's own posts (TikTok/Instagram screenshots, 13 Oct 2026). Captions only restate what each post shows.
POSTS = [('post-welcome.webp', 236, 238, 'Welcome post', 'New journey. Same purpose. Starting his new chapter as a real estate salesperson.'),
         ('post-tour.webp', 236, 314, 'Home tour video', 'A 2-bedroom unit near the MRT at S$1,200,000.'),
         ('post-launches.webp', 255, 340, 'New launch line-up', 'Upcoming condo and EC launches, from a list compiled by ERA in June 2026.')]


def award_gallery(pre=''):
    return '<div class="award-pics">%s</div>' % ''.join(
        '<figure><img src="%simg/%s" alt="%s" width="%d" height="%d" loading="lazy"><figcaption>%s</figcaption></figure>'
        % (pre, f, E(alt), w, h, E(cap)) for f, w, h, alt, cap in AWARD_IMGS)


def feed_section():
    tiles = ''.join(
        '<a class="post" href="%s" target="_blank" rel="noopener"><img src="img/%s" alt="%s" width="%d" height="%d" loading="lazy"><span><b>%s</b>%s</span></a>'
        % (SOCIAL['TikTok'], f, E(t + '. ' + d), w, h, E(t), E(d)) for f, w, h, t, d in POSTS)
    follow = ''.join('<a href="%s" target="_blank" rel="noopener">%s ↗</a>' % (SOCIAL[k], k) for k in ('Facebook', 'Instagram', 'TikTok'))
    return f'''<section class="sec sec-sand" aria-labelledby="h-feed"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">From Evan's feed</span><h2 id="h-feed">New launches, home tours and updates.</h2><p>Evan posts new launch updates, unit tours and market notes on social media. Follow along, or WhatsApp him about anything you see.</p></div>
  <div class="posts">{tiles}</div>
  <div class="socials" style="margin-top:20px">{follow}</div>
</div></section>'''


def home_body():
    moves = [
        ('buy/', 'buy', 'Buy a home', 'HDB resale, condo or landed. A shortlist that fits your budget and your daily life.'),
        ('sell/', 'sell', 'Sell your home', 'Pricing from recent transactions, careful marketing and a calm negotiation.'),
        ('upgrade/', 'upgrade', 'Upgrade from HDB', 'Sell and buy in the right order, so you are never caught between two homes.'),
        ('rent/', 'rent', 'Rent or lease', 'Landlords find suitable tenants. Tenants find a place that works.'),
    ]
    cards = ''.join('<a class="move" href="{p}"><span class="ic">{ic}</span><h3>{t}</h3><p>{d}</p><span class="more">Read more →</span></a>'
                    .format(p=p, ic=ICONS[i], t=E(t), d=E(d)) for p, i, t, d in moves)
    return f'''
<section class="hero"><div class="wrap hero-grid">
  <div>
    <span class="eyebrow">ERA property agent · Singapore</span>
    <h1>Your next home, <em>planned properly</em>.</h1>
    <p class="lede">I am Evan Lee (李敏彦), a property agent with ERA. Whether you are buying your first flat, selling, upgrading from HDB or renting out, I help you see the numbers clearly and take each step in the right order.</p>
    <div class="btns">{wa_btn("Hi Evan, I found your website. I would like to talk about my property plans.", "WhatsApp Evan")}<a class="btn btn-line" href="stamp-duty-calculator/">Stamp duty calculator</a></div>
    <ul class="trust">
      <li><b>8th</b><span>ERA Top 100 Achievers, July 2026</span></li>
      <li><b>3rd</b><span>ERA Top 5 New Achievers</span></li>
      <li><b>CEA</b><span>Registered agent, {CEA}</span></li>
    </ul>
  </div>
  <div class="hero-art">
    <img class="hero-portrait" src="img/evan-portrait.webp" alt="Evan Lee, ERA property agent" width="352" height="352" fetchpriority="high">
    <a class="hero-award" href="#awards" aria-label="See Evan's ERA awards"><img src="img/award-top100.webp" alt="ERA Explorer Group Top 100 Achievers poster for Evan Lee, 8th place, Super Gold, July 2026" width="236" height="269"></a>
    <div class="agent-chip"><div><b>Evan Lee 李敏彦</b><span>Associate · ERA Realty</span><span class="chip-award">★ ERA Top 100 Achievers, July 2026</span></div></div>
  </div>
</div></section>

<section class="sec sec-tight" id="awards" aria-labelledby="h-awards"><div class="wrap">
  <div class="awards"><div><span class="eyebrow">Recognition</span><h2 id="h-awards">Recognised by ERA Explorer Group.</h2>
  <ul>{''.join('<li><b>%s</b><span>%s</span><small>%s</small></li>' % (E(a), E(b), E(c)) for a, b, c in AWARDS)}</ul></div>
  {award_gallery()}</div>
</div></section>

<section class="sec" aria-labelledby="h-moves"><div class="wrap">
  <div class="sec-head"><h2 id="h-moves">What are you planning?</h2><p>Pick the move you are thinking about. Each page explains how Evan works on it, what to prepare and the questions people usually ask.</p></div>
  <div class="moves">{cards}</div>
</div></section>

<section class="sec sec-sand" aria-labelledby="h-how"><div class="wrap split">
  <div>
    <span class="eyebrow">How Evan works</span>
    <h2 id="h-how">Clear numbers first. Decisions after.</h2>
    <p>Property is usually the largest purchase a family makes. Before you view, list or sign anything, Evan sits down with you to work out what is realistic: your budget, your loan, your CPF, the stamp duty and the timeline.</p>
    <div class="btns" style="margin-top:20px">{wa_btn("Hi Evan, could you help me work out my budget and timeline before I start?", "Plan my numbers with Evan")}</div>
  </div>
  <ul class="ticks">
    <li><div><b>Plain explanations</b><span>The Option to Purchase, HDB resale steps, ABSD and loan limits, explained in everyday language before you commit.</span></div></li>
    <li><div><b>The right order of steps</b><span>Selling and buying in sequence, with dates that line up, so you are not paying for two homes or left without one.</span></div></li>
    <li><div><b>Honest pricing</b><span>Asking prices and offers are based on recent transactions nearby, not on wishful numbers.</span></div></li>
    <li><div><b>One person to message</b><span>You WhatsApp Evan directly. He keeps the buyer, seller, banker and lawyer conversations moving.</span></div></li>
  </ul>
</div></section>

<section class="sec sec-ink" aria-labelledby="h-steps"><div class="wrap">
  <div class="sec-head"><span class="eyebrow" style="color:#ff8a9c">Working together</span><h2 id="h-steps">Four steps from first message to keys.</h2><p>Every move is different, but most follow the same shape.</p></div>
  <ol class="steps">
    <li><h3>Tell Evan your plan</h3><p>A WhatsApp message is enough to start: what you want to do, where, and roughly when.</p></li>
    <li><h3>Get the numbers right</h3><p>Budget, loan, CPF, stamp duty and timing, worked out before any viewing or listing.</p></li>
    <li><h3>View, list and negotiate</h3><p>A focused shortlist for buyers. Pricing, photos and viewings for sellers. Evan handles the negotiation.</p></li>
    <li><h3>Sign and complete</h3><p>Option to Purchase, HDB or lawyer paperwork, and completion dates, followed through to handover.</p></li>
  </ol>
</div></section>

<section class="sec" aria-labelledby="h-tool"><div class="wrap">
  <div class="tool">
    <div>
      <span class="eyebrow">Free tools</span>
      <h2 id="h-tool">Check your numbers before you view.</h2>
      <p>Two calculators Evan uses with clients: stamp duty on a Singapore home, worked out tier by tier, and how much you may be able to borrow under the bank's debt limits.</p>
      <div class="btns"><a class="btn btn-line" href="stamp-duty-calculator/">Stamp duty calculator</a><a class="btn btn-line" href="loan-calculator/">Home loan calculator</a></div>
    </div>
    <div class="tool-fig" aria-label="Example: S$1,200,000 home bought by a Singapore Citizen as a first property">
      <p style="margin:0 0 12px;font-weight:700">Example: S$1,200,000, first home, Singapore Citizen</p>
      <dl><dt>Buyer's Stamp Duty</dt><dd>S$32,600</dd><dt>ABSD (0%)</dt><dd>S$0</dd><dt class="tot">Total</dt><dd class="tot">S$32,600</dd></dl>
    </div>
  </div>
</div></section>

<section class="sec sec-sand" aria-labelledby="h-meet"><div class="wrap split">
  <div>
    <span class="eyebrow">Meet your agent</span>
    <h2 id="h-meet">You will always know who you are dealing with.</h2>
    <p>Every Singapore property agent must be registered with the Council for Estate Agencies (CEA) and work under a licensed agency. Here are Evan's details, so you can check them yourself.</p>
    <p><a href="about/">More about Evan →</a></p>
  </div>
  {cred_card()}
</div></section>

{guides_teaser()}

{feed_section()}

<section class="sec" aria-labelledby="h-faq"><div class="wrap">
  <div class="sec-head"><h2 id="h-faq">Questions people ask first</h2></div>
  {faq_html(FAQ_HOME)}
</div></section>
'''


def cred_card(prefix=''):
    return f'''<div class="cred"><img src="{prefix}img/evan-portrait.webp" alt="Evan Lee, ERA property agent" width="132" height="132" loading="lazy">
  <div><h3>Evan Lee <span class="zh">李敏彦</span></h3><span style="color:var(--muted)">{TITLE}, {AGENCY}<br>{DIVISION}</span>
  <dl><dt>CEA Reg. No.</dt><dd>{CEA}</dd><dt>Agency licence</dt><dd>{AGENCY_LIC}</dd><dt>WhatsApp</dt><dd>{WA_SHOW}</dd><dt>Office</dt><dd>{', '.join(OFFICE)}</dd></dl>
  <div class="socials"><a href="https://www.cea.gov.sg/aceas/public-register" target="_blank" rel="noopener">Check on CEA Public Register ↗</a><a href="{SOCIAL['ERA profile']}" target="_blank" rel="noopener">ERA profile ↗</a></div></div></div>'''


def faq_html(items):
    return '<div class="faq">' + ''.join('<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items) + '</div>'


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


page('', 'Evan Lee 李敏彦 | ERA Property Agent Singapore | Buy, Sell, Upgrade, Rent',
     'Evan Lee (李敏彦), ERA property agent (CEA R074252A). Help buying, selling, upgrading from HDB and renting in Singapore. WhatsApp +65 8824 2798.',
     'Your next home, planned properly.', '', hero=False, schema=[faq_schema(FAQ_HOME)])


# ----------------------------------------------------------------------------------------------
# Service pages
# ----------------------------------------------------------------------------------------------
def service(path, crumb, title, desc, h1, lede, sections, faqs, wa_text, aside_title, aside_text, share_line=None):
    body = '<section class="sec"><div class="wrap layout"><div class="prose">' + sections
    body += '<h2>Common questions</h2>' + faq_html(faqs) + '</div>'
    body += ('<aside class="aside"><h3>%s</h3><p>%s</p>%s<small>Evan Lee · CEA %s · %s (%s)</small></aside>'
             % (E(aside_title), E(aside_text), wa_btn(wa_text), CEA, AGENCY, AGENCY_LIC))
    body += '</div></section>'
    page(path, title, desc, h1, body, crumbs=[(path, crumb)], lede=lede,
         schema=[faq_schema(faqs), {'@type': 'Service', 'name': crumb, 'serviceType': crumb, 'areaServed': 'Singapore',
                                     'provider': {'@id': SITE + '#evan'}, 'url': SITE + path,
                                     'image': ASSET + 'img/share/home.jpg'}])


service('buy/', 'Buying a home',
        'Buy an HDB, Condo or Landed Home in Singapore | Evan Lee, ERA',
        'Buying an HDB resale flat, condo or landed home in Singapore? Evan Lee (ERA, CEA R074252A) helps with budget, shortlist, offer and paperwork. WhatsApp +65 8824 2798.',
        'Buying a home in Singapore, step by step.',
        'HDB resale, condominium or landed. Evan helps you set a realistic budget, find homes that fit how you live, and negotiate and complete the purchase.',
        '''<h2>Start with what you can really afford</h2>
<p>The asking price is only part of the cost. Before viewing, Evan helps you put together the full picture:</p>
<ul><li><b>Loan limit.</b> Your bank or HDB loan amount depends on your income, age, existing debts and the loan-to-value limit. Try the <a href="loan-calculator/">home loan calculator</a>.</li>
<li><b>Cash and CPF.</b> How much of the down payment must be cash and how much can come from your CPF Ordinary Account.</li>
<li><b>Stamp duty.</b> Buyer's Stamp Duty on every purchase, and Additional Buyer's Stamp Duty if it applies to you. Try the <a href="stamp-duty-calculator/">stamp duty calculator</a>.</li>
<li><b>Other costs.</b> Legal fees, valuation, renovation and, for HDB resale, any cash over valuation you agree to.</li></ul>
<h2>HDB resale flats</h2>
<p>To buy an HDB resale flat you need a valid HDB Flat Eligibility (HFE) letter before the seller grants you an Option to Purchase. Evan checks that the flat suits your eligibility (citizenship, household, income ceiling for grants and the remaining lease) and walks you through the HDB resale portal from the Option to the completion appointment.</p>
<h2>Condominiums and new launches</h2>
<p>For private homes, Evan compares the projects you are considering on the things that matter day to day: location and transport, the size and layout you actually need, maintenance fees, remaining lease and recent transaction prices in the same development.</p>
<h2>Landed homes</h2>
<p>Landed purchases need extra checks: tenure, land size and any plans to rebuild, and the eligibility rules for buying landed residential property.</p>
<h2>From offer to keys</h2>
<ol><li>Shortlist and viewings, planned around your schedule.</li><li>Offer and negotiation based on recent transactions.</li><li>Option to Purchase, option fee and exercise within the stated period.</li><li>Loan, lawyer or HDB paperwork, and stamp duty payment.</li><li>Completion and handover.</li></ol>''',
        [('Do I pay commission when I buy?', 'For HDB resale and many private purchases, buyers may pay their own agent a commission. Whether a fee applies and how much is agreed with you in writing before Evan starts work, using the CEA prescribed agreement.'),
         ('Can Evan help with a new launch condo?', 'Yes. Evan can help you compare projects and units and guide you through the booking and the Option to Purchase.'),
         ('What do I need before making an offer on an HDB resale flat?', 'A valid HDB Flat Eligibility (HFE) letter, and if you are taking a bank loan, an in-principle approval from the bank. Evan will check what applies to you.'),
         ('How much stamp duty will I pay?', 'Buyer\'s Stamp Duty applies to every purchase, and Additional Buyer\'s Stamp Duty depends on your residency status and how many homes you own. The calculator on this site gives an estimate; IRAS has the final figure.')],
        'Hi Evan, I am looking to buy a home. Budget: , area: , timing: .',
        'Thinking of buying?', 'Send Evan your budget, preferred area and timing. He will suggest the next step.')

service('sell/', 'Selling your home',
        'Sell Your HDB or Condo in Singapore | Evan Lee, ERA Property Agent',
        'Selling your HDB flat, condo or landed home in Singapore? Evan Lee (ERA, CEA R074252A) prices from recent transactions and handles viewings, offers and paperwork.',
        'Sell your home with a clear plan and a fair price.',
        'A good sale starts with an honest price. Evan works out what your home is likely to fetch, prepares it for the market and handles viewings, offers and paperwork.',
        '''<h2>An honest asking price</h2>
<p>Evan looks at recent transactions for similar homes nearby, the floor, facing, condition and remaining lease, then talks you through a realistic price range and why. Pricing too high can leave a home sitting on the market; pricing too low leaves money on the table.</p>
<h2>Know your sale proceeds before you list</h2>
<p>Before listing, Evan helps you work out what you will receive after the sale: outstanding loan, the CPF you need to refund with accrued interest, any HDB resale levy, and fees. This matters even more if the proceeds fund your next home.</p>
<h2>Marketing your home</h2>
<ul><li>Preparing the home for photos and viewings. See <a href="guides/preparing-your-home-for-sale/">how to prepare your home for sale</a>.</li><li>Listings on the major property portals and Evan's own social media.</li><li>Video walkthroughs of your home, like the home tours on <a href="https://www.tiktok.com/@evanleehomes" target="_blank" rel="noopener">Evan's TikTok</a>.</li><li>Viewings arranged around your schedule, with feedback after each one.</li></ul>
<h2>HDB flat owners</h2>
<p>Most HDB owners must meet their Minimum Occupation Period before selling, and you need to register an Intent to Sell on the HDB Flat Portal before granting an Option to Purchase. Evan helps you get the timing right, especially if you are also buying your next home.</p>
<h2>From offer to completion</h2>
<ol><li>Offers negotiated with you, in writing.</li><li>Option to Purchase granted and exercised.</li><li>HDB resale application or lawyers' conveyancing.</li><li>Completion, handover of keys, and sale proceeds.</li></ol>''',
        [('How much commission does a seller pay?', 'Commission is not fixed by law. It is agreed between you and Evan in writing, using the CEA prescribed estate agency agreement, before your home is marketed.'),
         ('How long does it take to sell an HDB flat?', 'It depends on the price, the flat and the market. Once an Option to Purchase is exercised, the HDB resale process to completion usually takes a few more weeks. Evan will give you a timeline for your case.'),
         ('Can I sell and buy at the same time?', 'Yes, and timing matters. See the HDB upgrading page for how Evan lines up the sale of one home with the purchase of the next.'),
         ('Do I need to renovate before selling?', 'Usually not. Simple repairs, decluttering and good photos often matter more. Evan will tell you honestly what is worth doing.')],
        'Hi Evan, I am thinking of selling my home. Property type and area: , timing: .',
        'Thinking of selling?', 'Tell Evan the property type, area and when you want to move. He will give you a realistic price range.')

service('upgrade/', 'HDB upgrading',
        'Upgrade from HDB to Condo in Singapore | Evan Lee, ERA Property Agent',
        'Upgrading from your HDB flat to a condo or another home? Evan Lee (ERA, CEA R074252A) plans the sale and purchase in the right order. WhatsApp +65 8824 2798.',
        'Upgrade from HDB without being caught between two homes.',
        'Selling one home and buying the next is the move where timing matters most. Evan plans both sides together, so the numbers and the dates line up.',
        '''<h2>Why upgrading needs a plan</h2>
<p>When you upgrade, the money from your HDB sale usually funds the next purchase, and the dates have to work: when you must move out, when you can move in, and when each payment is due. Getting the order wrong can mean paying Additional Buyer's Stamp Duty you did not expect, or needing somewhere to stay in between.</p>
<h2>What Evan works out with you</h2>
<ul><li><b>Your sale proceeds.</b> Expected price, minus outstanding loan, CPF refund with accrued interest and fees.</li>
<li><b>Your new budget.</b> Sale proceeds, savings, CPF and the loan you can take on the next home.</li>
<li><b>Stamp duty.</b> Whether ABSD applies if you buy before selling, and the rules on when it can be refunded for married couples. Try the <a href="stamp-duty-calculator/">stamp duty calculator</a>.</li>
<li><b>Timeline.</b> Minimum Occupation Period, the HDB resale timeline, and the completion or TOP date of the next home.</li></ul>
<h2>Sell first or buy first?</h2>
<p>Selling first gives you certainty on your cash, but you may need to rent or ask the buyer for an extension of stay. Buying first secures the home you want, but you need to plan for ABSD and two loans for a period. Evan lays out both options with your real numbers, so you can choose.</p>
<h2>A typical upgrade timeline</h2>
<ol><li>Budget and plan: proceeds, new loan, CPF and stamp duty.</li><li>Shortlist the next home while preparing your flat for sale.</li><li>List your HDB flat and negotiate an offer.</li><li>Secure the next home, timing the Option to Purchase with your sale.</li><li>Complete the HDB sale, then the purchase, and move.</li></ol>''',
        [('When can I sell my HDB flat?', 'Most HDB flats can be sold once the Minimum Occupation Period is met, which is usually five years from when you collected the keys. Some newer flats have longer periods. Evan will check the rules for your flat.'),
         ('Will I have to pay ABSD if I buy a condo before selling my HDB?', 'It depends on your profile. Singapore Citizen married couples buying a second home may need to pay ABSD first and can apply for a refund if they sell the first home within the allowed period. Evan will explain what applies to you.'),
         ('Where do I stay if I sell before my new home is ready?', 'Options include negotiating an extension of stay with your buyer, renting short term, or timing the sale later. Evan helps you choose.'),
         ('How much can I afford for my next home?', 'Evan works this out with you from your sale proceeds, savings, CPF and the loan you qualify for, before you start viewing.')],
        'Hi Evan, I would like to plan an upgrade from my HDB flat. Current flat: , next home: , timing: .',
        'Planning an upgrade?', 'Share your current flat, what you would like next and your timing. Evan will map out the steps.')

service('rent/', 'Renting and leasing',
        'Rent Out or Rent a Home in Singapore | Evan Lee, ERA Property Agent',
        'Renting out your HDB or condo, or looking for a home to rent in Singapore? Evan Lee (ERA, CEA R074252A) helps landlords and tenants. WhatsApp +65 8824 2798.',
        'Renting out your home, or finding one to rent.',
        'For landlords, Evan helps find suitable tenants and puts the tenancy on a clear footing. For tenants, he helps find a place that fits your budget and commute.',
        '''<h2>For landlords</h2>
<ul><li><b>Rental pricing</b> from recent rental transactions for similar homes nearby.</li>
<li><b>Marketing and viewings</b> on the major portals, with viewings arranged around your tenants and your schedule.</li>
<li><b>Tenant checks.</b> Work pass or identity checks, and confirming the tenant is eligible to rent your type of property.</li>
<li><b>Tenancy agreement</b> with clear terms on deposit, repairs, diplomatic clause and handover, plus a checklist of the home's condition.</li></ul>
<h2>HDB flat owners</h2>
<p>Renting out a whole HDB flat or rooms has its own rules, including the Minimum Occupation Period, approval from HDB, occupancy caps and quotas for non-Malaysian non-citizen tenants. Evan will check what applies before you list.</p>
<h2>For tenants</h2>
<p>Tell Evan your budget, the areas you are considering and your move-in date. He shortlists suitable homes, arranges viewings and helps you understand the tenancy agreement before you sign.</p>''',
        [('How much commission does a landlord pay?', 'Commission for a tenancy is agreed with you in writing before Evan starts work. It commonly depends on the length of the lease.'),
         ('Can I rent out my HDB flat?', 'You can usually rent out a whole flat once the Minimum Occupation Period is met and HDB has approved it. Rooms may be rented out earlier in some cases. Evan will check the rules for your flat.'),
         ('What is a diplomatic clause?', 'A clause that lets a tenant end the lease early, with notice, if they have to leave Singapore for work. It is common in leases to foreign professionals.'),
         ('Who pays for repairs during a tenancy?', 'The tenancy agreement sets this out. Commonly, tenants pay for minor repairs up to an agreed amount, and landlords pay for larger repairs and structural issues.')],
        'Hi Evan, I would like help with a rental. I am a landlord / tenant. Property or area: , timing: .',
        'Renting out or renting?', 'Tell Evan whether you are a landlord or tenant, the area and your timing.')


# ----------------------------------------------------------------------------------------------
# Stamp duty calculator
# ----------------------------------------------------------------------------------------------
SD_FAQ = [
    ('What is Buyer\'s Stamp Duty (BSD)?', 'A tax paid on every property purchase in Singapore. For residential property it is charged in tiers: 1% on the first S$180,000, 2% on the next S$180,000, 3% on the next S$640,000, 4% on the next S$500,000, 5% on the next S$1,500,000 and 6% on the rest.'),
    ('What is Additional Buyer\'s Stamp Duty (ABSD)?', 'An extra tax on top of BSD for some buyers. For residential property bought from 27 April 2023: Singapore Citizens pay 0% on a first home, 20% on a second and 30% on a third or more. Singapore Permanent Residents pay 5%, 30% and 35%. Foreigners pay 60%, and most entities pay 65%.'),
    ('When is stamp duty paid?', 'Within 14 days of exercising the Option to Purchase or signing the sale and purchase agreement. It is paid in cash or, for BSD and in some cases ABSD, partly from CPF depending on your purchase.'),
    ('What if I buy jointly with someone else?', 'For joint purchases, ABSD is based on the buyer with the highest applicable rate. Married couples have specific remission rules. Evan can walk you through your case.'),
]


def calc_body():
    return f'''<section class="sec"><div class="wrap">
<div class="calc">
  <form id="sdcalc" novalidate aria-label="Stamp duty calculator">
    <div class="field"><label for="sd-price">Purchase price (or market value, if higher)</label><div class="money"><span>S$</span><input id="sd-price" inputmode="numeric" autocomplete="off" value="1200000"></div></div>
    <div class="field"><label for="sd-who">Buyer profile</label><select id="sd-who"><option value="sc">Singapore Citizen</option><option value="pr">Singapore Permanent Resident</option><option value="fr">Foreigner</option><option value="en">Entity (company)</option></select><small>For joint buyers, choose the profile with the highest ABSD rate.</small></div>
    <div class="field"><label for="sd-nth">This will be my</label><select id="sd-nth"><option value="1">First residential property</option><option value="2">Second residential property</option><option value="3">Third or more</option></select></div>
  </form>
  <div class="result" aria-live="polite">
    <dl><dt>Buyer's Stamp Duty</dt><dd id="sd-bsd">S$0</dd><dt>Additional Buyer's Stamp Duty</dt><dd id="sd-absd">S$0</dd><dt class="tot">Estimated total</dt><dd class="tot" id="sd-total">S$0</dd></dl>
    <table aria-label="Buyer's Stamp Duty by tier"><tbody id="sd-rows"></tbody></table>
    <p>Residential rates for purchases from 27 April 2023, as published by IRAS. This is an estimate only: remissions, refunds and special cases are not included. Confirm the exact amount with IRAS or your lawyer before you commit.</p>
    <a id="sd-wa" class="btn btn-wa" href="{E(wa('Hi Evan, I used the stamp duty calculator on your website. Can we talk through my purchase?'))}" target="_blank" rel="noopener">{WA_SVG}<span>Ask Evan about my numbers</span></a>
  </div>
</div>
<div class="prose" style="margin-top:56px"><h2>How stamp duty works</h2>{faq_html(SD_FAQ)}</div>
</div></section>'''


page('stamp-duty-calculator/', 'Stamp Duty Calculator Singapore (BSD + ABSD) | Evan Lee, ERA',
     'Free Singapore stamp duty calculator for residential property: Buyer\'s Stamp Duty and ABSD for Citizens, PRs and foreigners. By Evan Lee, ERA property agent.',
     'Stamp duty calculator for Singapore homes.', calc_body(), crumbs=[('stamp-duty-calculator/', 'Stamp duty calculator')],
     lede='Work out the Buyer\'s Stamp Duty and Additional Buyer\'s Stamp Duty on a residential purchase, tier by tier.',
     schema=[faq_schema(SD_FAQ), {'@type': 'WebApplication', 'name': 'Singapore stamp duty calculator', 'applicationCategory': 'FinanceApplication',
                                  'operatingSystem': 'Any', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'SGD'}, 'url': SITE + 'stamp-duty-calculator/'}])


# ----------------------------------------------------------------------------------------------
# Guides
# ----------------------------------------------------------------------------------------------
GUIDES = [
    ('hdb-resale-buying-steps', 'HDB resale: the buying steps in order',
     'From the HDB Flat Eligibility letter to collecting your keys, the steps of buying an HDB resale flat in Singapore, explained simply.',
     'Buying',
     '''<p>Buying an HDB resale flat follows a set order. Knowing it in advance helps you avoid delays and surprises.</p>
<h2>1. Get your HDB Flat Eligibility (HFE) letter</h2>
<p>Apply on the HDB Flat Portal. The HFE letter tells you whether you can buy a resale flat, which grants you may qualify for, and how much HDB loan you could take if you choose an HDB loan. You need a valid HFE letter before a seller can grant you an Option to Purchase.</p>
<h2>2. Work out your budget</h2>
<p>Add up your loan, CPF Ordinary Account savings, cash, any grants and the stamp duty. Leave room for legal fees, renovation, and any cash over valuation if the agreed price is above the valuation.</p>
<h2>3. View flats and agree a price</h2>
<p>Look beyond the listing photos: remaining lease, floor, facing, condition, and the walk to the MRT, schools or your parents' home. Compare against recent transactions in the same block or street.</p>
<h2>4. Option to Purchase</h2>
<p>The seller grants you an Option to Purchase in exchange for an option fee. You then have a set period to exercise it. Before exercising, request the HDB valuation if you need it.</p>
<h2>5. Submit the resale application</h2>
<p>After exercising the Option, buyer and seller each submit their part of the resale application on the HDB portal. HDB processes the application and sets a completion appointment.</p>
<h2>6. Completion</h2>
<p>At completion, the payments are made and you collect your keys.</p>
<p class="note">Rules and timelines are set by HDB and change from time to time. Check the latest on the HDB website, or ask Evan to walk through your case.</p>'''),
    ('selling-before-or-after-buying', 'Upgrading: sell first or buy first?',
     'Upgrading from HDB? Compare selling first and buying first: cash certainty, ABSD, bridging, and where you will live in between.',
     'Upgrading',
     '''<p>For most upgraders the biggest question is the order: sell the current home first, or secure the next one first. Both can work. The right choice depends on your numbers and your appetite for risk.</p>
<h2>Selling first</h2>
<ul><li><b>Pros.</b> You know exactly how much cash and CPF you will have for the next home. No second loan to carry.</li>
<li><b>Cons.</b> You may need somewhere to stay between homes. You may feel rushed to buy.</li>
<li><b>Ways to manage it.</b> Ask your buyer for an extension of stay, rent short term, or time your sale for when your next home is nearly ready.</li></ul>
<h2>Buying first</h2>
<ul><li><b>Pros.</b> You secure the home you want, and move only once.</li>
<li><b>Cons.</b> ABSD may be payable upfront, and you may need to service two loans for a while. If the sale takes longer than planned, cash flow can get tight.</li>
<li><b>Ways to manage it.</b> Check whether you qualify for an ABSD refund after selling, plan a bridging loan if needed, and price the current home realistically from the start.</li></ul>
<h2>The numbers to work out first</h2>
<ol><li>Expected sale price of your current home.</li><li>Outstanding loan and CPF refund with accrued interest.</li><li>Your loan limit on the next home.</li><li>Stamp duty, including any ABSD paid upfront.</li><li>Monthly payments if you hold two homes for a few months.</li></ol>
<p class="note">Evan works through these numbers with you before you list or view. <a href="upgrade/">See how Evan plans upgrades</a>.</p>'''),
    ('option-to-purchase-explained', 'The Option to Purchase, explained',
     'What the Option to Purchase (OTP) is in a Singapore property sale, the option fee, the exercise period, and what happens if a buyer does not exercise it.',
     'Buying and selling',
     '''<p>In Singapore, most resale property deals are made with an Option to Purchase (OTP). It is the document that turns an agreed price into a commitment.</p>
<h2>What it is</h2>
<p>The seller grants the buyer an option to buy the property at the agreed price, for a fixed period. The buyer pays an option fee in return. During the option period the seller cannot sell to anyone else.</p>
<h2>Exercising the option</h2>
<p>If the buyer decides to go ahead, they sign the acceptance and pay the exercise fee within the option period. The deal is then binding on both sides, and stamp duty becomes payable within 14 days.</p>
<h2>If the buyer does not exercise</h2>
<p>The option lapses at the end of the period, and the seller usually keeps the option fee. Buyers should arrange their loan approval and valuation before the period runs out.</p>
<h2>HDB and private property differ</h2>
<p>HDB resale transactions use HDB's own OTP form with set amounts and periods. Private property OTPs are prepared by the seller's side, and the option fee and exercise period are agreed between the parties. Read every OTP carefully, or have Evan and your lawyer go through it with you.</p>'''),
]


def guides_index():
    cards = ''.join('<a class="card" href="guides/%s/"><span class="tag">%s</span><h3>%s</h3><p>%s</p></a>' % (s, E(cat), E(t), E(d)) for s, t, d, cat, _ in GUIDES)
    cards += '<a class="card" href="stamp-duty-calculator/"><span class="tag">Tool</span><h3>Stamp duty calculator</h3><p>Work out BSD and ABSD on a Singapore home, tier by tier.</p></a>'
    cards += '<a class="card" href="loan-calculator/"><span class="tag">Tool</span><h3>Home loan calculator</h3><p>Estimate how much you can borrow under TDSR and MSR, and the price range it supports.</p></a>'
    return '<section class="sec"><div class="wrap"><div class="cards">%s</div></div></section>' % cards


page('guides/', 'Property Guides for Singapore Buyers and Sellers | Evan Lee, ERA',
     'Plain-language guides to buying, selling and upgrading property in Singapore: HDB resale steps, the Option to Purchase, and selling before or after buying.',
     'Property guides, in plain language.', guides_index(), crumbs=[('guides/', 'Guides')],
     lede='Short, practical explainers on the steps and terms you will meet when you buy, sell or upgrade in Singapore.')

for slug, t, d, cat, content in GUIDES:
    body = ('<section class="sec"><div class="wrap layout"><article class="prose">%s</article>'
            '<aside class="aside"><h3>Questions about your case?</h3><p>Every situation is a little different. Send Evan a message and he will walk you through yours.</p>%s'
            '<small>Evan Lee · CEA %s · %s (%s)</small></aside></div></section>') % (
        content, wa_btn('Hi Evan, I read your guide "%s". I have a question: ' % t), CEA, AGENCY, AGENCY_LIC)
    page('guides/%s/' % slug, '%s | Evan Lee, ERA' % t, d, t, body,
         crumbs=[('guides/', 'Guides'), ('guides/%s/' % slug, t)], lede=d, share='guide-' + slug,
         schema=[{'@type': 'Article', 'headline': t, 'description': d, 'author': {'@id': SITE + '#evan'},
                  'datePublished': '2026-10-13', 'dateModified': '2026-10-13', 'mainEntityOfPage': SITE + 'guides/%s/' % slug,
                  'image': ASSET + 'img/share/home.jpg', 'publisher': {'@id': SITE + '#evan'}}])


# ----------------------------------------------------------------------------------------------
# More guides, home loan calculator, home guides teaser
# ----------------------------------------------------------------------------------------------
GUIDES_MORE = [
    ('new-launch-progressive-payments', 'New launch condos: how progressive payments work',
     'Buying a new launch condo in Singapore? How the progressive payment scheme works, stage by stage, and what it means for your cash, CPF and loan.',
     'New launches',
     '''<p>When you buy a new launch condo that is still being built, you do not pay the full price at once. Under the Normal Payment Scheme, you pay in stages as construction progresses. Knowing the schedule helps you plan your cash, CPF and loan from the day you book.</p>
<h2>The payment stages</h2>
<table class="tbl"><thead><tr><th>Stage</th><th>Share of price</th></tr></thead><tbody>
<tr><td>Booking fee, when you receive the Option to Purchase</td><td>5%</td></tr>
<tr><td>On signing the Sale and Purchase Agreement</td><td>15%</td></tr>
<tr><td>Foundation work completed</td><td>10%</td></tr>
<tr><td>Reinforced concrete framework completed</td><td>10%</td></tr>
<tr><td>Partition walls completed</td><td>5%</td></tr>
<tr><td>Roofing or ceiling completed</td><td>5%</td></tr>
<tr><td>Doors, windows, electrical wiring, plumbing completed</td><td>5%</td></tr>
<tr><td>Car park, roads and drains completed</td><td>5%</td></tr>
<tr><td>Temporary Occupation Permit (TOP)</td><td>25%</td></tr>
<tr><td>Certificate of Statutory Completion (CSC)</td><td>15%</td></tr>
</tbody></table>
<h2>What it means for your cash</h2>
<ul><li><b>The first 20% comes from you.</b> The 5% booking fee is paid in cash. The next 15% can usually be paid from cash and your CPF Ordinary Account.</li>
<li><b>The bank loan starts at foundation.</b> From the third stage, the bank disburses its share of each payment, so your loan and monthly instalments grow as the building goes up.</li>
<li><b>Stamp duty is due early.</b> Buyer's Stamp Duty, and Additional Buyer's Stamp Duty if it applies, is payable within 14 days of signing the Sale and Purchase Agreement. Try the <a href="stamp-duty-calculator/">stamp duty calculator</a>.</li></ul>
<h2>Why buyers like it</h2>
<p>In the early years you only service interest on the part of the loan that has been drawn, which keeps instalments lower while the project is under construction. Upgraders often use this window to sell their current home before the large TOP payment falls due.</p>
<h2>Questions to ask before booking</h2>
<ol><li>When is the expected TOP date, and what is the legal completion date in the contract?</li><li>Can I meet the 20% upfront, and the stamp duty within 14 days?</li><li>What will my monthly instalment be at each stage, at today's rates and at a higher rate?</li><li>If I am upgrading, when must my current home be sold?</li></ol>
<p class="note">The schedule above is the standard Normal Payment Scheme set by the Housing Developers Rules. Each developer's contract sets out the exact terms. Ask Evan to map the payments against your own cash flow before you book.</p>'''),
    ('preparing-your-home-for-sale', 'Preparing your home for sale: a practical checklist',
     'How to get your HDB flat or condo ready for photos and viewings in Singapore, what is worth fixing, and what to have ready for buyers.',
     'Selling',
     '''<p>Buyers decide quickly. Most first see your home as photos and a video on a phone, then form their view within minutes of walking in. A little preparation helps your home stand out and supports a better price.</p>
<h2>Before the photos and video</h2>
<ul><li><b>Declutter every room.</b> Clear counters, tables and the floor. Pack away personal items and anything you will not need before you move.</li>
<li><b>Let the light in.</b> Open curtains and blinds, replace dead bulbs and clean the windows.</li>
<li><b>Fix the small things.</b> Dripping taps, loose handles, stained grout and scuffed walls are cheap to fix and noticed by every buyer.</li>
<li><b>Set the scene.</b> Make the beds, put out fresh towels and keep the kitchen and bathrooms spotless.</li></ul>
<h2>What is usually not worth doing</h2>
<p>A full renovation rarely pays for itself before a sale, because many buyers plan to renovate to their own taste. A fresh coat of paint in neutral colours and simple repairs usually give a better return.</p>
<h2>On viewing days</h2>
<ul><li>Air the home, switch on the lights and turn on the air-conditioning a little before buyers arrive.</li>
<li>Keep pets and valuables out of the way.</li>
<li>Let buyers look around freely. Your agent can answer their questions and gather honest feedback afterwards.</li></ul>
<h2>Documents to have ready</h2>
<ul><li>Your outstanding loan amount and the CPF you have used, with accrued interest, so you know your sale proceeds.</li>
<li>For HDB flats, confirmation that the Minimum Occupation Period has been met.</li>
<li>For condos, the latest maintenance fee statement and any upcoming sinking fund or special levy.</li>
<li>Details of any renovation, approvals or warranties that come with the home.</li></ul>
<p class="note">Evan can walk through your home with you and tell you honestly what is worth doing before listing. <a href="sell/">See how Evan sells homes</a>.</p>'''),
]

for slug, t, d, cat, content in GUIDES_MORE:
    GUIDES.append((slug, t, d, cat, content))
    body = ('<section class="sec"><div class="wrap layout"><article class="prose">%s</article>'
            '<aside class="aside"><h3>Questions about your case?</h3><p>Every situation is a little different. Send Evan a message and he will walk you through yours.</p>%s'
            '<small>Evan Lee · CEA %s · %s (%s)</small></aside></div></section>') % (
        content, wa_btn('Hi Evan, I read your guide "%s". I have a question: ' % t), CEA, AGENCY, AGENCY_LIC)
    page('guides/%s/' % slug, '%s | Evan Lee, ERA' % t, d, t, body,
         crumbs=[('guides/', 'Guides'), ('guides/%s/' % slug, t)], lede=d, share='guide-' + slug,
         schema=[{'@type': 'Article', 'headline': t, 'description': d, 'author': {'@id': SITE + '#evan'},
                  'datePublished': '2026-10-13', 'dateModified': '2026-10-13', 'mainEntityOfPage': SITE + 'guides/%s/' % slug,
                  'image': ASSET + 'img/share/home.jpg', 'publisher': {'@id': SITE + '#evan'}}])

PAGES['guides/']['body'] = guides_index()


LOAN_FAQ = [
    ('What is TDSR?', 'The Total Debt Servicing Ratio limits the share of your gross monthly income that can go to all your debt repayments, including the new home loan, car loans and credit facilities. The limit set by MAS is 55%.'),
    ('What is MSR?', 'The Mortgage Servicing Ratio applies to loans for HDB flats and for executive condominiums bought from the developer. It caps the home loan instalment at 30% of gross monthly income, on top of the TDSR.'),
    ('Why does the calculator use a higher interest rate?', 'Banks do not assess you at the current rate. They use a higher medium-term rate, so you can still afford the loan if rates rise. The default here is 4% a year; change it to match what your bank tells you.'),
    ('What is the loan-to-value limit?', 'The most a bank can lend as a share of the price or valuation, whichever is lower. For a first housing loan it is usually 75%, with at least 5% of the price paid in cash. It is lower if you already have a housing loan, or if the loan tenure or your age at the end of the loan is above the set limits.'),
]


def loan_body():
    return f'''<section class="sec"><div class="wrap">
<div class="calc">
  <form id="lncalc" novalidate aria-label="Home loan calculator">
    <div class="field"><label for="ln-inc">Gross monthly income (all borrowers)</label><div class="money"><span>S$</span><input id="ln-inc" inputmode="numeric" autocomplete="off" value="10000"></div><small>For variable income such as commission, banks usually count only part of it.</small></div>
    <div class="field"><label for="ln-debt">Existing monthly debt repayments</label><div class="money"><span>S$</span><input id="ln-debt" inputmode="numeric" autocomplete="off" value="0"></div><small>Car loans, other property loans, personal loans and credit card minimums.</small></div>
    <div class="field"><label for="ln-type">Property</label><select id="ln-type"><option value="pte">Condo, landed or resale EC</option><option value="hdb">HDB flat, or new EC from the developer</option></select></div>
    <div class="field"><label for="ln-ltv">Loan-to-value limit</label><select id="ln-ltv"><option value="75">75% (first housing loan)</option><option value="45">45% (second housing loan)</option><option value="35">35% (third or more)</option></select></div>
    <div class="field"><label for="ln-yrs">Loan tenure (years)</label><input id="ln-yrs" inputmode="numeric" value="30"><small>Up to 30 years for HDB flats and 35 years for private homes, within age limits.</small></div>
    <div class="field"><label for="ln-rate">Assessment interest rate (% a year)</label><input id="ln-rate" inputmode="decimal" value="4"></div>
  </form>
  <div class="result" aria-live="polite">
    <dl><dt>Monthly instalment allowed</dt><dd id="ln-inst">S$0</dd><dt>Limit applied</dt><dd id="ln-rule">TDSR 55%</dd><dt class="tot">Estimated maximum loan</dt><dd class="tot" id="ln-loan">S$0</dd></dl>
    <dl><dt>Price this loan supports</dt><dd id="ln-price">S$0</dd><dt>Down payment</dt><dd id="ln-down">S$0</dd><dt>of which in cash, at least</dt><dd id="ln-cash">S$0</dd></dl>
    <p>An estimate using the MAS TDSR (55%) and MSR (30%) limits. It is not a loan approval: banks also look at your age, credit record, how income is counted and the property's valuation. Stamp duty and legal fees are extra.</p>
    <a class="btn btn-wa" href="{E(wa('Hi Evan, I used the home loan calculator on your website. Can you help me check my budget?'))}" target="_blank" rel="noopener">{WA_SVG}<span>Check my budget with Evan</span></a>
  </div>
</div>
<div class="prose" style="margin-top:56px"><h2>How banks work out your loan</h2>{faq_html(LOAN_FAQ)}
<p>Next, see what you will pay in tax with the <a href="stamp-duty-calculator/">stamp duty calculator</a>.</p></div>
</div></section>
<script src="loan.js?v=1" defer></script>'''


page('loan-calculator/', 'Home Loan Calculator Singapore (TDSR, MSR) | Evan Lee, ERA',
     'Free Singapore home loan calculator: estimate your maximum loan under TDSR and MSR, the price range it supports and the cash you need. By Evan Lee, ERA property agent.',
     'How much can you borrow for a home?', loan_body(), crumbs=[('loan-calculator/', 'Home loan calculator')],
     lede='Estimate your maximum home loan under the bank debt limits, and the price range and down payment that go with it.',
     schema=[faq_schema(LOAN_FAQ), {'@type': 'WebApplication', 'name': 'Singapore home loan calculator', 'applicationCategory': 'FinanceApplication',
                                    'operatingSystem': 'Any', 'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'SGD'}, 'url': SITE + 'loan-calculator/'}])


def guides_teaser():
    pick = ['hdb-resale-buying-steps', 'new-launch-progressive-payments', 'selling-before-or-after-buying', 'preparing-your-home-for-sale']
    g = {s: (t, d, c) for s, t, d, c, _ in GUIDES}
    cards = ''.join('<a class="card" href="guides/%s/"><span class="tag">%s</span><h3>%s</h3><p>%s</p></a>' % (s, E(g[s][2]), E(g[s][0]), E(g[s][1])) for s in pick)
    return f'''<section class="sec" aria-labelledby="h-guides"><div class="wrap">
  <div class="sec-head"><span class="eyebrow">Guides by Evan</span><h2 id="h-guides">Know the process before you start.</h2><p>Plain-language explainers on the steps, payments and paperwork you will meet when you buy, sell or upgrade in Singapore.</p></div>
  <div class="cards cards-4">{cards}</div>
  <p style="margin-top:20px"><a href="guides/">All guides and tools →</a></p>
</div></section>'''


PAGES['']['body'] = home_body()


# ----------------------------------------------------------------------------------------------
# About and contact
# ----------------------------------------------------------------------------------------------
def about_body():
    return f'''<section class="sec"><div class="wrap split">
<div class="prose">
<h2>Hello, I am Evan.</h2>
<p>I am a property agent and Associate with ERA Realty Network, in the {DIVISION}, working from ERA APAC Centre in Toa Payoh. I help families and individuals across Singapore buy, sell, rent and invest in property.</p>
<figure class="about-post"><img src="img/post-welcome.webp" alt="Evan's welcome post: New journey. Same purpose. Helping you find a place you'll love coming home to." width="236" height="238" loading="lazy"><figcaption>From Evan's welcome post</figcaption></figure>
<p>Real estate is a new chapter for me, with the same purpose I have always had: helping people find a place they will love coming home to. Whether you are buying, selling, investing or still exploring your options, you can expect honest advice, genuine service and guidance at every step.</p>
<p>My approach is simple: work out the real numbers first, explain each step in plain language, and keep the process moving so you always know what happens next. You message me directly on WhatsApp, and I keep the conversations with the other agent, the bank, HDB and the lawyers going for you.</p>
<h2>What I help with</h2>
<ul><li><a href="buy/">Buying</a> an HDB resale flat, condominium or landed home</li><li><a href="sell/">Selling</a> your home at a realistic price</li><li><a href="upgrade/">Upgrading</a> from HDB to private property, in the right order</li><li><a href="rent/">Renting</a> out your home, or finding one to rent</li></ul>
<h2>Recognition</h2>
<ul>{''.join('<li><b>%s</b>, %s. %s.</li>' % (E(a), E(b), E(c)) for a, b, c in AWARDS)}</ul>
{award_gallery()}
<h2>Follow along</h2>
<p>I share new launch updates, listings and property tips on Facebook (<a href="{SOCIAL['Facebook']}" target="_blank" rel="noopener">Evan Lee Properties</a>), Instagram (<a href="{SOCIAL['Instagram']}" target="_blank" rel="noopener">@evanlee.homes</a>) and TikTok (<a href="{SOCIAL['TikTok']}" target="_blank" rel="noopener">@evanleehomes</a>).</p>
<div class="btns" style="margin-top:22px">{wa_btn("Hi Evan, I read about you on your website. I would like to chat about my property plans.")}</div>
</div>
<div>{cred_card()}
<p style="margin-top:18px;color:var(--muted);font-size:.92rem">ERA Realty Network Pte Ltd is a wholly owned subsidiary of SGX Mainboard-listed APAC Realty.</p></div>
</div></section>'''


page('about/', 'About Evan Lee 李敏彦 | ERA Property Agent, CEA R074252A',
     'Evan Lee (李敏彦) is an Associate with ERA Realty Network Pte Ltd (licence L3002382K), CEA registration R074252A, based at ERA APAC Centre, Toa Payoh.',
     'Evan Lee 李敏彦, ERA property agent.', about_body(), crumbs=[('about/', 'About')],
     lede='Associate, ERA Realty Network Pte Ltd, %s. Helping' % DIVISION + ' Singapore homeowners, buyers and tenants plan each move properly.',
     schema=[{'@type': 'ProfilePage', 'mainEntity': {'@id': SITE + '#evan'}}])


def contact_body():
    social = ''.join('<a href="%s" target="_blank" rel="noopener">%s ↗</a>' % (u, k) for k, u in SOCIAL.items())
    return f'''<section class="sec"><div class="wrap contact-grid">
<form id="qform" class="calc-form" style="background:#fff;border:1px solid var(--line);border-radius:var(--r);padding:26px;display:grid;gap:16px" aria-label="Message Evan on WhatsApp">
  <h2 style="font-size:1.4rem;margin:0">Send Evan a WhatsApp message</h2>
  <p style="margin:0;color:var(--muted)">Fill this in and press the button. WhatsApp opens with your message ready to send. Nothing is stored on this website.</p>
  <div class="field"><label for="q-name">Your name</label><input id="q-name" required autocomplete="name"></div>
  <div class="field"><label for="q-goal">I would like help with</label><select id="q-goal"><option>Buying a home</option><option>Selling my home</option><option>Upgrading from HDB</option><option>Renting out my home</option><option>Finding a home to rent</option><option>Something else</option></select></div>
  <div class="field"><label for="q-area">Area or property (optional)</label><input id="q-area" placeholder="e.g. 4-room HDB in Toa Payoh"></div>
  <div class="field"><label for="q-time">Timing (optional)</label><input id="q-time" placeholder="e.g. within 6 months"></div>
  <div class="field"><label for="q-msg">Anything else (optional)</label><textarea id="q-msg" rows="3"></textarea></div>
  <button class="btn btn-wa" type="submit">{WA_SVG}<span>Open WhatsApp</span></button>
</form>
<div class="c-cards">
  <div class="c-card"><h3>WhatsApp</h3><p><a href="{E(wa('Hi Evan, I found your website. I have a property question.'))}" target="_blank" rel="noopener">{WA_SHOW}</a></p></div>
  <div class="c-card"><h3>Email</h3><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
  <div class="c-card"><h3>Office</h3><p>{'<br>'.join(OFFICE)}</p><p style="margin-top:8px"><a href="{MAP}" target="_blank" rel="noopener">Open in Google Maps ↗</a></p></div>
  <div class="c-card"><h3>Agency</h3><p>{AGENCY}<br>Estate Agent Licence {AGENCY_LIC}<br>CEA Reg. No. {CEA}</p></div>
  <div class="c-card"><h3>Social</h3><div class="socials">{social}</div></div>
</div>
</div></section>'''


page('contact/', 'Contact Evan Lee | ERA Property Agent | WhatsApp +65 8824 2798',
     'Contact Evan Lee (李敏彦), ERA property agent, on WhatsApp +65 8824 2798 or at evanleehomes@gmail.com. Office: ERA APAC Centre, 450 Lorong 6 Toa Payoh.',
     'Talk to Evan.', contact_body(), crumbs=[('contact/', 'Contact')],
     lede='WhatsApp is the quickest way to reach Evan. Tell him what you are planning and he will get back to you.', cta=False,
     schema=[{'@type': 'ContactPage', 'mainEntity': {'@id': SITE + '#evan'}}])


# ----------------------------------------------------------------------------------------------
# Layout
# ----------------------------------------------------------------------------------------------
def person_schema():
    return {'@type': ['RealEstateAgent', 'Person'], '@id': SITE + '#evan', 'name': NAME, 'alternateName': NAME_ZH,
            'jobTitle': 'Property Agent (Associate)', 'url': SITE, 'image': ASSET + 'img/evan-portrait.webp', 'logo': ASSET + 'icon-512.png',
            'telephone': '+' + WA_NUM, 'email': EMAIL, 'priceRange': 'Commission agreed in writing',
            'worksFor': {'@type': 'RealEstateAgent', 'name': AGENCY, 'identifier': {'@type': 'PropertyValue', 'propertyID': 'CEA Estate Agent Licence', 'value': AGENCY_LIC}},
            'identifier': {'@type': 'PropertyValue', 'propertyID': 'CEA Registration', 'value': CEA},
            'address': {'@type': 'PostalAddress', 'streetAddress': '450 Lorong 6 Toa Payoh, ERA APAC Centre', 'postalCode': '319394', 'addressLocality': 'Singapore', 'addressCountry': 'SG'},
            'areaServed': {'@type': 'Country', 'name': 'Singapore'}, 'sameAs': SAME_AS,
            'award': ['%s (%s), %s' % a for a in AWARDS], 'knowsAbout': ['Property investment', 'New launch condominiums', 'HDB resale', 'Condominium purchase', 'Landed property', 'HDB upgrading', 'Property selling', 'Residential leasing', 'Stamp duty']}


def render(path, p):
    depth = path.count('/')
    pre = '../' * depth
    url = SITE + path
    share = ASSET + 'img/share/home.jpg'  # one image for all pages for now; per-page cards: share.card(p['share'], p['h1'])

    def fix(s):  # make root-relative-style links in page bodies relative to this page
        return re.sub(r'(href|src)="(?!https?:|mailto:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (pre, h, ' aria-current="page"' if path.startswith(h) else '', t) for h, t in NAV)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">Home</a>' % (pre or './')] + ['<a href="%s%s">%s</a>' % (pre, h, E(t)) for h, t in p['crumbs'][:-1]] + [E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + h} for i, (h, t) in enumerate(p['crumbs'])]}
    graph = [person_schema(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'],
                               'primaryImageOfPage': {'@type': 'ImageObject', 'url': share, 'width': 1200, 'height': 630},
                               'inLanguage': 'en-SG', 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': 'Evan Lee Homes'}}]
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
        band = ('<section class="sec" style="padding-top:8px"><div class="wrap"><div class="band"><div><h2>Ready to talk about your next move?</h2>'
                '<p>Send Evan a WhatsApp message with what you are planning. No obligation.</p></div>%s</div></div></section>') % wa_btn(
            'Hi Evan, I found your website. I would like to talk about my property plans.')
    robots = 'noindex,nofollow' if NOINDEX else 'index,follow,max-image-preview:large'
    title = E(p['title'])
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
<meta name="robots" content="{robots}">
<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#16202e">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Evan Lee Homes">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{share}">
<meta property="og:image:secure_url" content="{share}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{E(p['h1'] if p['h1'][-1] in '.?' else p['h1'] + '.')}{'' if 'Evan Lee' in p['h1'] else ' Evan Lee, ERA property agent,'} WhatsApp {WA_SHOW}">
<meta property="og:locale" content="en_SG">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{share}">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="icon" href="{pre}favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="stylesheet" href="{pre}evan.css?v=4">
<script src="{pre}evan.js?v=1" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span>Evan Lee · {TITLE}, {AGENCY} · Licence {AGENCY_LIC} · CEA Reg. {CEA}</span><a href="{E(wa('Hi Evan, I found your website. I have a property question.'))}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></div></div>
<header class="hdr"><div class="wrap">
<a class="brand" href="{pre or './'}" aria-label="Evan Lee Homes, home page">{MARK}<span><span class="brand-name">Evan Lee<span>李敏彦</span></span><span class="brand-sub">ERA property agent</span></span></a>
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
{wa_btn('Hi Evan, I found your website. I have a property question.', 'WhatsApp', 'btn btn-wa')}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
</div></header>
<main id="main">
{head_hero}
{fix(p['body'])}
{band}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div><a class="brand" href="{pre or './'}">{MARK}<span><span class="brand-name">Evan Lee<span style="color:#b9c2cf">李敏彦</span></span><span class="brand-sub" style="color:#b9c2cf">ERA property agent</span></span></a>
<p style="margin-top:16px">Helping Singapore homeowners, buyers, landlords and tenants plan each move properly.</p></div>
<div><h3>Explore</h3><ul>{''.join('<li><a href="%s%s">%s</a></li>' % (pre, h, t) for h, t in NAV)}</ul></div>
<div><h3>Contact</h3><ul>
<li><a href="{E(wa('Hi Evan, I found your website. I have a property question.'))}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{'<br>'.join(OFFICE)}</li>
<li><a href="{SOCIAL['Instagram']}" target="_blank" rel="noopener">Instagram</a> · <a href="{SOCIAL['TikTok']}" target="_blank" rel="noopener">TikTok</a> · <a href="{SOCIAL['ERA profile']}" target="_blank" rel="noopener">ERA profile</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>Evan Lee 李敏彦 · {TITLE} · CEA Reg. No. {CEA} · {AGENCY} · Estate Agent Licence No. {AGENCY_LIC}</span><span>© 2026 Evan Lee · Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<a class="dock" href="{E(wa('Hi Evan, I found your website. I have a property question.'))}" target="_blank" rel="noopener" aria-label="WhatsApp Evan Lee at {WA_SHOW}"><img src="{pre}img/evan-portrait.webp" alt="" width="42" height="42"><span>WhatsApp Evan</span></a>
</body>
</html>
'''


def not_found():
    body = ('<section class="sec"><div class="wrap prose"><p>The page you were looking for has moved or does not exist. These may help:</p>'
            '<ul>%s</ul></div></section>') % ''.join('<li><a href="/%s">%s</a></li>' % (h, t) for h, t in NAV)
    p = dict(title='Page not found | Evan Lee, ERA', desc='This page could not be found.', h1='Sorry, that page is not here.', body=body,
             crumbs=None, lede='', share='home', schema=[], hero=True, cta=True)
    out = render('', p).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    # 404s are served at any depth: use root-relative links (works on the client's domain).
    out = re.sub(r'(href|src)="(?!https?:|mailto:|#|/|data:)([^"]*)"', lambda m: '%s="/%s"' % (m.group(1), m.group(2) if m.group(2) != './' else ''), out)
    return out


HTACCESS = """# Evan Lee Homes ({DOMAIN}). This folder is {DOMAIN}'s document root and also
# pageonesingapore.com/preview/evanlee/. Anything here overrides the parent pageonesingapore.com
# .htaccess for this folder; compression, caching and security headers still come from the parent.
#
# RewriteEngine On here switches off the parent's rewrite rules for this folder, because they assume
# pageonesingapore.com's paths. So the https / no-www / index.html rules are repeated here.
RewriteEngine On

# One address only: https://{DOMAIN} (no www, always https)
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]

# /index.html and /about/index.html -> the clean folder address ({DOMAIN} only)
RewriteCond %{HTTP_HOST} ^{DQ}$ [NC]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://{DOMAIN}/$1 [L,R=301]

# Our own "page not found" page (the parent's /404.html does not exist on {DOMAIN})
ErrorDocument 404 /404.html
"""


def main():
    for path, p in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(render(path, p))
    with open(os.path.join(OUT, '404.html'), 'w') as f:
        f.write(not_found())
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write('User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for path in PAGES:
            f.write('  <url><loc>%s%s</loc><lastmod>2026-10-13</lastmod></url>\n' % (SITE, path))
        f.write('</urlset>\n')
    with open(os.path.join(OUT, '23a57c4e63533ad53cd56ac7615f2feb.txt'), 'w') as f:
        f.write('23a57c4e63533ad53cd56ac7615f2feb')
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write('# Evan Lee 李敏彦, ERA property agent (Singapore)\n\n'
                '> Evan Lee is an Associate with %s (Estate Agent Licence %s), CEA registration %s. '
                'He helps people buy, sell, upgrade from HDB and rent homes in Singapore. Contact: WhatsApp %s, %s. '
                'Office: %s.\n\n## Pages\n' % (AGENCY, AGENCY_LIC, CEA, WA_SHOW, EMAIL, ', '.join(OFFICE)))
        for path, p in PAGES.items():
            f.write('- [%s](%s%s): %s\n' % (p['title'].split(' | ')[0], SITE, path, p['desc']))
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': 'Evan Lee Homes', 'short_name': 'Evan Lee', 'icons': [
            {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}, {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'}],
            'theme_color': '#16202e', 'background_color': '#fbf8f3', 'display': 'browser'}, f)
    with open(os.path.join(OUT, 'favicon.svg'), 'w') as f:
        f.write(MARK.replace(' class="brand-mark"', ' xmlns="http://www.w3.org/2000/svg"').replace(' aria-hidden="true"', ''))
    for d in ('img', 'img/share'):
        with open(os.path.join(OUT, d, 'index.html'), 'w') as f:
            f.write('')
    dq = DOMAIN.replace('.', r'\.')
    with open(os.path.join(OUT, '.htaccess'), 'w') as f:
        f.write(HTACCESS.replace('{DOMAIN}', DOMAIN).replace('{DQ}', dq))
    print('built %d pages' % len(PAGES))


if __name__ == '__main__':
    main()
