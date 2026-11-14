"""EC Coffee Bar Pte. Ltd.: builds every page into site/ (python3 images.py && python3 build.py).

Facts used (16 Oct 2026), and where they came from:
- ACRA (recordowl.com / sgpbusiness.com): EC COFFEE BAR PTE. LTD., UEN 202416189N, incorporated 23 Apr 2024, live,
  SSIC 56112 cafes (secondary 56111 restaurants), registered at 40 Carpenter Street #01-01, Singapore 059919.
- Instagram @eccoffeebar (Edwin's screenshots, 16 Oct 2026): "EC Coffeebar", hours Mon-Sat 8.30am-9pm, Sun 8.30am-8pm,
  "Your new favourite spot to meet, sip, and create connections. Where every conversation counts.", text 93656626,
  email eccoffeebar@gmail.com (Instagram shows "gamil", Edwin confirmed gmail), Facebook "EC Coffeebar".
- Edwin (16 Oct 2026): about 50 pax at full capacity, a VIP room of about 10 pax, target CBD professionals, company events,
  team bonding and group celebrations, WhatsApp enquiry and booking.
- Her own menu PDF (July 2025, on her Grab Dine Out listing): story ("Where Chicks Grow into Eagles", "E for Entrepreneurs,
  C for Chick", all-day cafe, bar and business event space), every dish, set and price used below, social handles
  (WeChat, TikTok, Xiaohongshu: eccoffeebar). Chinese name 创鸡咖啡吧.
- Chope listing: "Good for business meetings, private functions"; Eatigo: Google highlights 4.9 (not shown, no count).
Not claimed anywhere: Google rating or review quotes, awards, buyout minimum spend, GST/service charge, halal status,
  opening year beyond the ACRA date. Things Edwin must confirm are in CONFIRM and README.md.
"""
import html
import json
import os
import shutil
import re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site')

SLUG = 'ec-coffee-bar'
DOMAIN = ''                          # client domain once confirmed, then LIVE = True and rebuild
LIVE = False
NOINDEX = not LIVE
PREVIEW = 'https://pageonesingapore.com/preview/%s/' % SLUG
SITE = ('https://%s/' % DOMAIN) if LIVE else PREVIEW
IMG = os.environ.get('EC_IMG', 'img/')   # relative by default; set to a CDN base if photos are served elsewhere
UPDATED = '2026-10-16'

NAME = 'EC Coffee Bar'
LEGAL = 'EC Coffee Bar Pte. Ltd.'
ZH = '创鸡咖啡吧'
UEN = '202416189N'
FOUNDER = ('Ethel Zhang', 'https://pageonesingapore.com/preview/ethel-zhang/')  # owner confirmed by Edwin 16 Oct 2026; switch to ethelzhang.com at go-live
WA_NUM, WA_SHOW = '6593656626', '9365 6626'
TEL = '+6593656626'
EMAIL = 'eccoffeebar@gmail.com'
WA_MSG = 'Hi EC Coffee Bar, I found your website. I would like to ask about '
HOURS = [('Monday to Saturday', '8.30am to 9pm'), ('Sunday', '8.30am to 8pm')]
HOURS_SHORT = 'Mon–Sat 8.30am–9pm · Sun 8.30am–8pm'
HOURS_LD = [{'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 'opens': '08:30', 'closes': '21:00'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Sunday', 'opens': '08:30', 'closes': '20:00'}]
ADDR = ['40 Carpenter Street, #01-01', 'Singapore 059919']
STREET, POSTAL = '40 Carpenter Street, #01-01', '059919'
GEO = (1.2878919, 103.8479014)
MAPQ = 'EC+COFFEE+BAR+40+Carpenter+Street+%2301-01+Singapore+059919'
MAP = 'https://www.google.com/maps/search/?api=1&query=' + MAPQ
MAP_EMBED = 'https://www.google.com/maps?q=' + MAPQ + '&output=embed'
IG = 'https://www.instagram.com/eccoffeebar/'
TIKTOK = 'https://www.tiktok.com/@eccoffeebar'
CAPACITY, VIP = 50, 10
MENU_DATE = 'July 2025'

CONFIRM = [
    'Domain name for go-live',
    'Menu prices are still current (taken from the July 2025 menu on Grab) and whether GST / service charge apply',
    'Full-café bookings for up to 50: buyout terms (hours, deposit) and how far ahead to book (Edwin 16 Oct 2026: no minimum order)',
    'VIP room: exact seats, any room charge, screen or projector for presentations',
    'Low-sugar cakes: which cakes (the menu says "afternoon tea with low-sugar cakes")',
    'Photos: the interior, storefront and anniversary shots on the preview are customer photos from Google Maps and Instagram, used as placeholders. Ask for her own originals (or permission) and photos of the VIP room',
    'Facebook page URL, and Google reviews she is happy to quote',
    'For the event planner page: deposit and cancellation terms, whether the café invoices companies, screen/projector or mic, outside cake policy, nearest parking',
]

NAV = [('events/', 'Events'), ('plan-an-event/', 'Plan an event'), ('menu/', 'Menu'), ('articles/', 'Articles'), ('about/', 'About'), ('contact/', 'Contact')]
E = html.escape

PHOTOS = {  # name: (width, height, alt)
    'signature-spread': (490, 600, 'The Signature Spread for 4 to 6 people at EC Coffee Bar: lamb rack, striploin, barramundi, two chicken mains, fish and chips and a bottle of wine'),
    'lunch-spread': (490, 400, 'EC mixed lunch set: spaghetti, striploin, chicken rice, fried rice and cake laid out for a group'),
    'afternoon-tea': (491, 303, 'EC afternoon Glow Tea Set on a gold stand with mini burgers, cheese tarts, strawberry cupcakes and a matcha latte'),
    'sunrise-sharing': (490, 272, 'EC Sunrise sharing breakfast set with a breakfast platter, croissants, oatmeal, tea and latte'),
    'croissant-set': (490, 242, 'Sunrise croissants set: a basket of croissants, filled croissants, tea and a latte'),
    'cake-slices': (564, 198, 'Slices of Golden Biscoff Dream, Silk Whisk Cheesecake, Hazelnut Truffle Delight and Berry Fruit Cake'),
    'cocktails': (493, 242, 'EC signature cocktails: amaretto sour, whisky highball, gin tonic, espresso martini and Bailey\'s coffee'),
    'wine-dinner': (491, 327, 'Mango Salsa Soul Fire Chicken with a glass of white wine and a bottle in an ice bucket'),
    'lamb-wine': (352, 327, 'Kindfire lamb rack with a glass of red wine'),
    'cheese-wine': (550, 315, 'Love and cheese platter with blue cheese, cheddar, melon, strawberries, blueberries, pecans and toast'),
    'beer-snacks': (566, 234, 'Chicken bites and orange-glazed chicken wings served with bottles of Heineken'),
    'dinner-for-two': (372, 224, 'Dinner set for two with mango salsa chicken, lamb rack and two glasses of wine'),
    'iced-drinks': (384, 440, 'Matcha tiramisu latte in a glass on a wooden tray'),
    'carbonara': (640, 420, 'Casa Carbonara spaghetti with shaved parmesan'),
    'breakfast-platter': (1080, 1220, 'EC Signature Breakfast Platter with scrambled eggs, sausage, baked potato, roasted tomato, sourdough, mushroom soup and a long black'),
    'breakfast-studio': (1000, 500, 'EC Signature Breakfast Platter with sourdough, scrambled eggs, sausage and mushroom soup'),
    'prawn-bowl': (674, 448, 'Deep Dive Prawn Bowl with prawns, egg and noodles in a spicy broth'),
    'chocolate-cake': (590, 579, 'A slice of Hazelnut Truffle Delight chocolate cake with the EC Coffee Bar topper'),
    'lamb-rack': (626, 471, 'Kindfire lamb rack on mashed potato with vegetables'),
    'dining-corridor': (720, 947, 'Inside EC Coffee Bar: light wood tables, cream chairs, rattan lamps and red roses along the dining room'),
    'dining-room-long': (632, 494, 'The long dining room at EC Coffee Bar with banquette seating, rattan lamps and the bar at the far end'),
    'storefront': (612, 948, 'The EC Coffee Bar shopfront at 40 Carpenter Street with its pink chick sign and opening flowers'),
    'anniversary-party': (720, 416, 'Guests raising glasses around a long table at the EC Coffee Bar 1st anniversary celebration'),
    'bar-counter': (948, 713, 'The EC Coffee Bar counter with its lit sign, wine shelf and coffee machine at 40 Carpenter Street'),
    'melon-salad': (1080, 840, 'Melon Harmony Salad with rock melon, parma ham and greens on an EC Coffee Bar plate'),
}


def img(name, sm=False, cls='', eager=False):
    w, h, alt = PHOTOS[name]
    src = IMG + name + '.webp'
    if w > 560:
        h, w = round(h * 560 / w), 560
    return '<img%s src="%s" alt="%s" width="%d" height="%d"%s>' % (
        ' class="%s"' % cls if cls else '', src, E(alt), w, h, ' fetchpriority="high"' if eager else ' loading="lazy" decoding="async"')


WA_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 '
          '18.2a8.2 8.2 0 0 1-4.2-1.1l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 '
          '6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 '
          '11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>')
PIN_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>')
CAL_SVG = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
           '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>')


def wa_url(topic='a booking.'):
    return 'https://wa.me/%s?text=%s' % (WA_NUM, quote(WA_MSG + topic))


def wa_btn(label='WhatsApp to book', topic='a booking.', cls='btn btn-wa'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, E(wa_url(topic)), WA_SVG, E(label))


def map_btn(label='Get directions', cls='btn btn-ghost'):
    return '<a class="%s" href="%s" target="_blank" rel="noopener">%s<span>%s</span></a>' % (cls, MAP, PIN_SVG, E(label))


def enquire_btn(label='Plan an event', cls='btn btn-rose', href='plan-an-event/'):
    return '<a class="%s" href="%s">%s<span>%s</span></a>' % (cls, href, CAL_SVG, E(label))


def hours_html():
    return '<dl class="hours">%s</dl>' % ''.join('<dt>%s</dt><dd>%s</dd>' % (E(d), E(t)) for d, t in HOURS)


MARK = '<img class="brand-mark" src="%slogo-160.webp" alt="" width="44" height="44">' % IMG


def brand_html(pre):
    return ('<a class="brand" href="%s" aria-label="%s, home page">%s<span><span class="brand-name">EC Coffee Bar</span>'
            '<span class="brand-sub">Café · Bar · Events · CBD</span></span></a>') % (pre or './', NAME, MARK.replace('src="', 'src="' + pre) if not IMG.startswith('http') else MARK)


PAGES = {}


def page(path, title, desc, h1, body, crumbs=None, lede='', schema=None, hero=True, cta=True, photo=None):
    PAGES[path] = dict(title=title, desc=desc, h1=h1, body=body, crumbs=crumbs, lede=lede, schema=schema or [],
                       hero=hero, cta=cta, photo=photo)


def faq_html(items):
    return '<div class="faq">%s</div>' % ''.join(
        '<details><summary>%s</summary><p>%s</p></details>' % (E(q), E(a)) for q, a in items)


def faq_schema(items):
    return {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in items]}


def price_list(items):
    rows = []
    for it in items:
        n, p, note = (tuple(it) + ('',))[:3]
        frm = note == 'from'
        rows.append('<li><span>%s%s</span><b>%s$%s</b></li>' % (E(n), '' if frm or not note else '<small>%s</small>' % E(note), 'from ' if frm else '', p))
    return '<ul class="plist">%s</ul>' % ''.join(rows)


PRICE_NOTE = ('Prices in Singapore dollars from EC Coffee Bar\'s %s menu. Prices and items can change, so please check '
              'with the team on WhatsApp before you book.' % MENU_DATE)

# ----------------------------------------------------------------------------------------------
# Group packages (from her menu) used on event pages
# ----------------------------------------------------------------------------------------------
PKG = {
    'spread': ('The Signature Spread wine set', 'For 4 to 6 people: mango salsa chicken, black pepper chicken, Royale barramundi, fish and chips, striploin and lamb rack, with a bottle of house pour wine (red or white).', '219.90', 'signature-spread'),
    'lunch': ('EC mixed lunch set', 'A sharing spread of lunch mains, cakes and drinks for the table.', '100.90', 'lunch-spread'),
    'sunrise': ('EC Sunrise sharing set with 4 drinks', 'Signature breakfast platter, filled croissants, oatmeal and four drinks.', '89.90', 'sunrise-sharing'),
    'croissants': ('Sunrise croissants set with 4 drinks', 'A basket of croissants and filled croissants with four drinks.', '69.90', 'croissant-set'),
    'tea': ('EC afternoon Glow Tea Set', 'A tiered afternoon tea set. Reserve ahead.', '39.90', 'afternoon-tea'),
    'cocktails': ('EC 6 signature cocktails set', 'Six of the house cocktails to share.', '89.90', 'cocktails'),
    'beer': ('Beer package, 10 bottles', 'Heineken or Hoegaarden, ten bottles.', '79.90', 'beer-snacks'),
    'cheese': ('Love & Cheese platter for 3 to 4', 'Cheeses, fruit, nuts and toast to share.', '29.90', 'cheese-wine'),
    'cakes': ('Whole cakes (4, 6 or 8 inch)', 'Cheesecake, hazelnut truffle, berry fruit or Biscoff. Reserve ahead.', '19.90', 'cake-slices'),
    'dinner2': ('Dinner sets for 2 with wine', 'Two mains with two glasses of wine.', '57.90', 'dinner-for-two'),
}


def pkg_cards(keys):
    return '<div class="pkgs">%s</div>' % ''.join(
        '<figure class="pkg">%s<figcaption><b>%s</b><span>%s</span><em>%s$%s</em></figcaption></figure>' % (
            img(PKG[k][3], sm=True), E(PKG[k][0]), E(PKG[k][1]), 'From ' if k in ('cakes', 'dinner2') else '', PKG[k][2]) for k in keys)


# ----------------------------------------------------------------------------------------------
# Events (the main reason people book)
# ----------------------------------------------------------------------------------------------
EVENTS = [
    dict(slug='corporate-events', short='Corporate events', photo='anniversary-party',
         gist='Host up to %d guests for a company lunch, dinner, launch or networking evening in the CBD.' % CAPACITY,
         title='Corporate Event Venue in the CBD for up to 50 | EC Coffee Bar',
         desc='Company lunches, dinners and networking events for up to 50 guests at EC Coffee Bar, 40 Carpenter Street near Clarke Quay. Sharing sets, wine and cocktails. WhatsApp 9365 6626.',
         h1='Corporate events in the CBD',
         lede='A relaxed, cozy café and bar for company lunches, dinners and networking evenings, with room for up to %d guests and a private room for 10.' % CAPACITY,
         pkgs=['spread', 'lunch', 'cocktails', 'beer'],
         sections=[
             ('Events we host', [
                 'Company lunches and dinners, client appreciation evenings, product and business launches, networking sessions, '
                 'department gatherings and year-end get-togethers. EC Coffee Bar calls itself an all-day café, bar and business event space, '
                 'built for entrepreneurs and professionals.']),
             ('How many guests?', [
                 'The café holds about %d guests at full capacity. For a smaller, more private group, the VIP room seats about %d.' % (CAPACITY, VIP),
                 'Small groups are just as welcome as big ones, and there is no minimum order. Tell us your headcount when you enquire and we will suggest the best layout for your group.']),
             ('Food and drinks for groups', [
                 'Sharing sets keep a group event simple: the Signature Spread feeds 4 to 6 people with six mains and a bottle of wine, '
                 'and the EC mixed lunch set covers a table at lunchtime. Add wine from France and Italy, signature cocktails or a beer package for the evening.']),
             ('Why a café near Clarke Quay works for CBD teams', [
                 'We are at 40 Carpenter Street, a short walk from Clarke Quay MRT and the Raffles Place offices. Colleagues can walk over '
                 'after work, and the room feels calm and warm rather than loud, so people can actually talk.']),
         ],
         faqs=[
             ('How many people can EC Coffee Bar host for a corporate event?', 'About %d guests at full capacity in the café, or about %d in the VIP room. Share your headcount on WhatsApp and the team will advise on layout and menu.' % (CAPACITY, VIP)),
             ('Do you have set menus for company events?', 'Yes. Sharing sets such as the Signature Spread for 4 to 6 people and the EC mixed lunch set suit groups, and wine, cocktail and beer packages are available. Ask on WhatsApp for options that fit your group.'),
             ('Where is EC Coffee Bar?', 'At 40 Carpenter Street, #01-01, Singapore 059919, a short walk from Clarke Quay MRT and the Raffles Place office area.'),
             ('How do I book a company event?', 'WhatsApp 9365 6626 with your date, time, number of guests and the occasion. The team will reply with availability and menu options.'),
         ]),
    dict(slug='team-lunch', short='Team lunches & team bonding', photo='dining-room-long',
         gist='Relaxed team lunches and bonding meals for CBD teams, with sharing sets that make ordering easy.',
         title='Team Lunch & Team Bonding Venue near Raffles Place | EC Coffee Bar',
         desc='Book a team lunch or team bonding meal at EC Coffee Bar near Clarke Quay and Raffles Place. Sharing sets, lunch sets from $9.90 and space for up to 50. WhatsApp 9365 6626.',
         h1='Team lunches and team bonding',
         lede='Get the team out of the office for an hour or an afternoon. Good food, a calm room and sharing sets that make ordering for a group easy.',
         pkgs=['lunch', 'sunrise', 'cheese', 'cakes'],
         sections=[
             ('Lunch with the whole team', [
                 'Team lunches work best when nobody has to organise a complicated order. Sharing sets such as the EC mixed lunch set '
                 'cover the table, and individual lunch sets (a main with a drink or cake) start from $17.90.']),
             ('Team bonding without the hard sell', [
                 'Not every team wants an escape room. A long lunch or an afternoon tea session gives people time to talk. '
                 'Book a breakfast set for an early team huddle, an afternoon tea for a quarterly catch-up, or after-work drinks to end a project.']),
             ('Groups of every size', [
                 'Small teams fit into the VIP room for about %d. Whole departments of up to about %d can fill the café.' % (VIP, CAPACITY)]),
         ],
         faqs=[
             ('Is EC Coffee Bar good for a team lunch in the CBD?', 'Yes. It is a short walk from Raffles Place and Clarke Quay, seats about 50, and has sharing and lunch sets that make group ordering simple.'),
             ('How much does a team lunch cost?', 'Lunch sets with a drink or cake start from $17.90 per person, and the EC mixed lunch set for sharing is $100.90 (July 2025 menu). Ask on WhatsApp for current prices.'),
             ('Can we book a table for a team of 10 to 20?', 'Yes. WhatsApp 9365 6626 with your date, time and headcount so the team can hold the right tables for you.'),
             ('Do you do team breakfasts?', 'Yes. The café opens at 8.30am, and sharing breakfast sets come with four drinks.'),
         ]),
    dict(slug='vip-room', short='VIP room for 10', photo='lamb-wine',
         gist='A private room for about %d: client lunches, board meetings and small celebrations.' % VIP,
         title='Private Dining Room for 10 in the CBD | EC Coffee Bar VIP Room',
         desc='EC Coffee Bar\'s VIP room seats about 10 for client lunches, business meetings and small private dinners, at 40 Carpenter Street near Clarke Quay. WhatsApp 9365 6626.',
         h1='The VIP room for about 10 guests',
         lede='A private room for client lunches, partner meetings and small celebrations, when you want the food of a café and the privacy of a meeting room.',
         pkgs=['spread', 'dinner2', 'cheese', 'cocktails'],
         sections=[
             ('What the room is for', [
                 'Client lunches, partner and board meetings, interview lunches, small team dinners and private birthday dinners. '
                 'It seats about %d guests, so a full team or a client group can sit together.' % VIP]),
             ('Food that suits a meeting', [
                 'Order individual mains such as the Kindfire striploin or lamb rack, or share the Signature Spread across the table. '
                 'Wine is served by the glass or the bottle, from France, Italy and other European countries.']),
             ('Booking the room', [
                 'The room is popular for lunch and dinner, so message us early with your date, time and number of guests.']),
         ],
         faqs=[
             ('Does EC Coffee Bar have a private room?', 'Yes. The VIP room seats about 10 guests and suits client lunches, meetings and small private dinners.'),
             ('How do I reserve the VIP room?', 'WhatsApp 9365 6626 with your date, time and number of guests.'),
             ('Can we order wine in the VIP room?', 'Yes. House pour wine, bottles from France and Italy, cocktails and beer are on the menu.'),
             ('Is the VIP room good for a client lunch near Raffles Place?', 'Yes. It is a short walk from Raffles Place and Clarke Quay, and the room is private enough to talk business over lunch.'),
         ]),
    dict(slug='celebrations', short='Birthdays & farewells', photo='afternoon-tea',
         gist='Office birthdays, farewells, promotions and anniversaries, with whole cakes made to order.',
         title='Office Birthday & Farewell Party Venue in the CBD | EC Coffee Bar',
         desc='Celebrate office birthdays, farewells and promotions at EC Coffee Bar near Clarke Quay. Whole cakes from $19.90, afternoon tea sets and sharing dinners. WhatsApp 9365 6626.',
         h1='Birthdays, farewells and office celebrations',
         lede='Mark the moment with the team: a farewell lunch, a surprise birthday cake, a promotion toast or a project wrap party.',
         pkgs=['cakes', 'tea', 'spread', 'cocktails'],
         sections=[
             ('Celebrations we help with', [
                 'Farewell lunches, office birthdays, promotion and anniversary dinners, baby showers for colleagues, and team wins worth toasting.']),
             ('Whole cakes by reservation', [
                 'Order a whole Silk Whisk Cheesecake, Hazelnut Truffle Delight, Berry Fruit Cake or Golden Biscoff Dream in 4, 6 or 8 inch sizes, '
                 'from $19.90 for 4 inch. Reserve ahead so it is ready when your group arrives.']),
             ('Afternoon tea for a softer celebration', [
                 'The EC afternoon Glow Tea Set comes on a tiered stand and is made to order, so reserve it ahead. '
                 'The menu also offers afternoon tea with low-sugar cakes, a good fit for colleagues who prefer something lighter.']),
         ],
         faqs=[
             ('Can I order a birthday cake for the office?', 'Yes. Whole cakes come in 4, 6 and 8 inch sizes from $19.90 and need a reservation. WhatsApp 9365 6626 with the cake, size and date.'),
             ('Where can we have a farewell lunch near Clarke Quay?', 'EC Coffee Bar at 40 Carpenter Street seats about 50, has a VIP room for about 10, and offers sharing sets for groups.'),
             ('Can we bring our own decorations?', 'Ask the team on WhatsApp when you book so they can plan the table for you.'),
             ('Do you serve wine and cocktails for celebrations?', 'Yes: wine by the glass or bottle, a set of six signature cocktails, and beer packages.'),
         ]),
    dict(slug='business-breakfast', short='Business breakfasts & meetings', photo='sunrise-sharing',
         gist='Open from 8.30am for breakfast meetings, coffee catch-ups and client chats before the workday.',
         title='Business Breakfast & Meeting Café near Raffles Place | EC Coffee Bar',
         desc='Breakfast meetings from 8.30am at EC Coffee Bar near Clarke Quay and Raffles Place. Croissant sets with coffee from $9.90 and sharing breakfasts for 4. WhatsApp 9365 6626.',
         h1='Business breakfasts and meetings',
         lede='A quiet table, proper coffee and a good breakfast from 8.30am, a short walk from the Raffles Place offices.',
         pkgs=['sunrise', 'croissants', 'cheese', 'tea'],
         sections=[
             ('Breakfast before the day starts', [
                 'The café opens at 8.30am every day. Breakfast sets pair a dish with a coffee or tea, from $9.90 for a classic croissant and drink, '
                 'up to the EC Signature Breakfast Platter set at $21.90.']),
             ('Meetings that need a little privacy', [
                 'For a client or partner meeting, book the VIP room for about %d. For a casual catch-up, any table works, and the room is calm rather than loud.' % VIP]),
             ('Built for professionals', [
                 'EC Coffee Bar was set up as a place for the business community to meet, recharge and rise together. '
                 'The name says it: E for Entrepreneurs, C for Chick, and the house motto is "Where Chicks Grow into Eagles".']),
         ],
         faqs=[
             ('What time does EC Coffee Bar open?', 'From 8.30am every day. It closes at 9pm Monday to Saturday and 8pm on Sunday.'),
             ('How much is breakfast?', 'Breakfast sets with a drink start from $9.90 (classic croissant and drink) on the July 2025 menu.'),
             ('Is it a good place for a business meeting near Raffles Place?', 'Yes. It is a short walk from Raffles Place, opens at 8.30am, and has a VIP room for about 10 when you need privacy.'),
             ('Can I book a table for a breakfast meeting?', 'Yes. WhatsApp 9365 6626 with your time and number of guests.'),
         ]),
    dict(slug='after-work-drinks', short='After-work drinks', photo='cocktails',
         gist='Wine, cocktails and beer packages with sharing plates to wind down after work.',
         title='After-Work Drinks near Clarke Quay | Wine & Cocktails | EC Coffee Bar',
         desc='After-work wine, cocktails and beer near Clarke Quay and Raffles Place. House pour from $16.90, 6 cocktails set $89.90, 10-beer package $79.90. WhatsApp 9365 6626.',
         h1='After-work drinks',
         lede='Wind down with the team over wine, cocktails or beer and plates to share, in a café that turns into a cozy bar in the evening.',
         pkgs=['cocktails', 'beer', 'cheese', 'spread'],
         sections=[
             ('What we pour', [
                 'House pour wine by the glass, and bottles from France, Italy and other European countries. Cocktails include an amaretto sour, '
                 'whisky highball, gin or vodka tonic, espresso martini and the house "First Love". Heineken and Hoegaarden come by the bottle or in packages.']),
             ('Plates to share', [
                 'Truffle fries, warm cheesy fries, orange-glazed chicken wings, chicken bites, the Love & Cheese platter and the Heavenly Camembert Melt '
                 'are made for the table. Snack and beer or wine sets bundle them together.']),
             ('For the whole team', [
                 'For a bigger group, book ahead: the café holds about %d and the VIP room about %d.' % (CAPACITY, VIP)]),
         ],
         faqs=[
             ('Does EC Coffee Bar serve alcohol?', 'Yes. Wine, cocktails, beer, whisky, brandy and gin are on the menu.'),
             ('How much is a glass of wine?', 'House pour is $16.90 a glass or $29.90 for two (July 2025 menu).'),
             ('Do you have beer packages for groups?', 'Yes. Five bottles of Heineken or Hoegaarden are $48.90 and ten bottles $79.90 (July 2025 menu).'),
             ('Until what time can we stay?', 'The café is open until 9pm Monday to Saturday and 8pm on Sunday.'),
         ]),
]
EVT = {e['slug']: e for e in EVENTS}

# ----------------------------------------------------------------------------------------------
# Menu (her July 2025 menu)
# ----------------------------------------------------------------------------------------------
MENUS = [
    dict(slug='breakfast', short='All-day breakfast', photo='breakfast-platter', from_price='9.90',
         gist='Breakfast platters, croissants, open sandwiches and oatmeal, with coffee sets from $9.90.',
         title='All-Day Breakfast near Clarke Quay & Raffles Place | EC Coffee Bar',
         desc='All-day breakfast at EC Coffee Bar, 40 Carpenter Street: signature breakfast platter, croissants, avocado toast and oatmeal. Breakfast sets with coffee from $9.90.',
         h1='All-day breakfast',
         lede='Power breakfasts for the CBD from 8.30am: platters, croissants, open sandwiches and oatmeal, most with a drink set option.',
         groups=[
             ('Breakfast', [('EC Signature Breakfast Platter', '19.90', 'scrambled eggs, sausage, baked potato, roasted tomato, sourdough, butter, mushroom soup'),
                            ('Hearty Ham Egg & Avocado open sandwich', '14.90'), ('Sunny Avocado & Scrambled Egg open sandwich', '13.90'),
                            ('Soul Roasted Chicken Croissant', '14.90'), ('Sunny Egg Mayo Croissant', '13.90'), ("Lovers' Ham & Cheese Croissant", '13.90'),
                            ('Classic Croissant', '6.90'), ('Rainbow Fruit Oatmeal', '15.90'), ('Healthy Banana Oatmeal', '13.90'),
                            ('House Salad', '15.90'), ('Cheesy Ham Omelette', '13.90'), ('Cozy Cinnamon French Toast', '12.90'),
                            ('Golden Brioche', '9.90'), ('Shouka Sunrise', '12.90'), ('Homemade Mushroom Soup', '9.90'), ('Deep Dive Prawn Bowl', '9.90')]),
             ('Breakfast sets with a drink', [('Classic Croissant & drink', '9.90'), ('Golden Brioche (3 pcs) & drink', '11.90'), ('Deep Dive Prawn Bowl & drink', '11.90'),
                                             ('Cozy Cinnamon French Toast & drink', '14.90'), ('Shouka Sunrise & drink', '14.90'),
                                             ('Sunny Egg Mayo Croissant & drink', '15.90'), ('Cheesy Ham Omelette & drink', '15.90'),
                                             ('Healthy Banana Oatmeal & drink', '15.90'), ('Hearty Ham Egg & Avocado & drink', '16.90'),
                                             ('Soul Roasted Chicken Croissant & drink', '16.90'), ('Rainbow Fruit Oatmeal & drink', '17.90'),
                                             ('EC Signature Breakfast Platter & drink', '21.90')]),
             ('Sharing breakfasts', [('Breakfast sets for 2 with 2 drinks', '35.90', 'from'), ('Sunrise croissants with 4 drinks', '69.90'), ('EC Sunrise sharing with 4 drinks', '89.90')]),
         ],
         faqs=[('Does EC Coffee Bar serve breakfast all day?', 'Yes. EC Coffee Bar is an all-day café, and breakfast is on the menu from opening at 8.30am.'),
               ('What is in the EC Signature Breakfast Platter?', 'Scrambled eggs, grilled sausage, oven-baked potato, roasted tomato, sourdough with butter and a cup of mushroom soup. It is $19.90, or $21.90 with a drink.'),
               ('What is the cheapest breakfast set?', 'The classic croissant with a drink at $9.90 (July 2025 menu).')]),
    dict(slug='lunch', short='Lunch & lunch sets', photo='carbonara', from_price='13.90',
         gist='Pasta, rice bowls, striploin and lamb, with lunch sets that include a drink or cake.',
         title='Lunch Sets near Raffles Place & Clarke Quay | EC Coffee Bar',
         desc='Lunch at EC Coffee Bar near Raffles Place: pasta, fried rice, striploin, lamb rack and barramundi. Lunch sets with a drink or cake from $13.90.',
         h1='Lunch and lunch sets',
         lede='Western mains, pasta and rice bowls for a CBD lunch break, with sets that add a drink or a slice of cake.',
         groups=[
             ('Mains', [('Black Pepper Soul Fire Chicken Rice', '15.90'), ('Sunny Fish and Chips', '17.90'), ('Happy Chicky Fried Rice', '18.90'),
                        ('EC Scallop Delight Fried Rice', '18.90'), ('Black Pepper Soul Fire Chicken', '22.90'), ('Mango Salsa Soul Fire Chicken', '22.90'),
                        ('Ocean Royale Barramundi', '22.90'), ('Sunny Striploin', '25.90'), ('Kindfire Striploin', '38.90'), ('Kindfire Lamb Rack', '38.90')]),
             ('Spaghetti', [('Classic Tomato Spaghetti', '15.90'), ('Sunny Aglio Olio', '15.90'), ('Casa Carbonara', '22.90'),
                            ('Velvet Truffle Spaghetti', '22.90'), ('Scorching Ocean Spaghetti', '25.90')]),
             ('Lunch sets with a drink or cake', [('Mushroom Soup with Crust Sourdough', '13.90'), ('House Salad', '17.90'), ('Black Pepper Soul Fire Chicken Rice', '17.90'),
                                                 ('Sunny Aglio Olio', '17.90'), ('Classic Tomato Spaghetti', '17.90'), ('Sunny Fish and Chips', '19.90'),
                                                 ('EC Scallop Delight Fried Rice', '20.90'), ('Velvet Truffle Spaghetti', '24.90'), ('Casa Carbonara', '24.90'),
                                                 ('Sunny Striploin', '27.90'), ('EC mixed lunch set (sharing)', '100.90')]),
         ],
         faqs=[('How much is lunch at EC Coffee Bar?', 'Lunch sets with a drink or cake run from $13.90 to $27.90, and mains from $15.90 (July 2025 menu).'),
               ('Is there a lunch set for groups?', 'Yes. The EC mixed lunch set at $100.90 is a sharing spread for the table.'),
               ('Is EC Coffee Bar near Raffles Place?', 'Yes. 40 Carpenter Street is a short walk from Raffles Place and Clarke Quay MRT.')]),
    dict(slug='afternoon-tea-cakes', short='Afternoon tea & cakes', photo='chocolate-cake', from_price='7.90',
         gist='Afternoon tea sets, tiramisu and cakes by the slice, plus whole cakes to order.',
         title='Afternoon Tea & Cakes in the CBD | Whole Cakes to Order | EC Coffee Bar',
         desc='Afternoon tea at EC Coffee Bar near Clarke Quay: the EC Glow Tea Set, cake and drink sets from $12.90, and whole cakes in 4, 6 and 8 inch from $19.90.',
         h1='Afternoon tea and cakes',
         lede='Slow down mid-afternoon with cake and tea, or order a whole cake for the office celebration.',
         groups=[
             ('Afternoon tea sets', [('EC afternoon Glow Tea Set (reserve ahead)', '39.90'), ('Silk Whisk Cheesecake & drink', '12.90'), ('Golden Biscoff Dream & drink', '13.90'),
                                     ('Berry Fruit Cake & drink', '13.90'), ('Hazelnut Truffle Delight & drink', '14.90'), ('Matcha Tiramisu & drink', '14.90'), ('Tiramisu & drink', '14.90')]),
             ('Cakes by the slice', [('Silk Whisk Cheesecake', '7.90'), ('Golden Biscoff Dream', '8.90'), ('Berry Fruit Cake', '8.90'),
                                     ('Hazelnut Truffle Delight', '9.90'), ('Matcha Tiramisu Whisper', '9.90'), ('Classic Tiramisu Dream', '9.90')]),
             ('Whole cakes (reserve ahead)', [('Silk Whisk Cheesecake', '19.90', '4 in · $58.90 6 in · $68.90 8 in'), ('Berry Fruit Cake', '19.90', '4 in · $59.90 6 in · $69.90 8 in'),
                                              ('Hazelnut Truffle Delight', '19.90', '4 in · $59.90 6 in · $75.90 8 in'), ('Golden Biscoff Dream', '19.90', '4 in · $59.90 6 in · $79.90 8 in')]),
         ],
         faqs=[('Does EC Coffee Bar have afternoon tea?', 'Yes. The EC afternoon Glow Tea Set is $39.90 and needs a reservation, and cake and drink sets start at $12.90.'),
               ('Can I order a whole cake?', 'Yes. Four cakes come whole in 4, 6 and 8 inch sizes from $19.90. Reserve ahead on WhatsApp 9365 6626.'),
               ('Are there low-sugar options?', 'The café describes its afternoon tea as coming with low-sugar cakes. Ask the team which cakes are low-sugar on the day.')]),
    dict(slug='dinner-drinks', short='Dinner, wine & cocktails', photo='wine-dinner', from_price='16.90',
         gist='Dinner sets with wine, sharing spreads for 4 to 6, cocktails, beer and spirits.',
         title='Dinner with Wine near Clarke Quay | Cocktails & Beer | EC Coffee Bar',
         desc='Dinner at EC Coffee Bar near Clarke Quay: mains with a glass of wine from $25.90, dinner for two from $57.90, the Signature Spread for 4-6, cocktails and beer.',
         h1='Dinner, wine and cocktails',
         lede='In the evening the café becomes a cozy bar: mains paired with wine, sharing spreads, cocktails and beer.',
         groups=[
             ('Dinner sets with wine', [('Sunny Aglio Olio with wine', '25.90'), ('Casa Carbonara with wine', '32.90'), ('Velvet Truffle Spaghetti with wine', '32.90'),
                                        ('Mango Salsa Soul Fire Chicken with wine', '32.90'), ('Black Pepper Soul Fire Chicken with wine', '32.90'),
                                        ('Ocean Royale Barramundi with wine', '32.90'), ('Scorching Ocean Spaghetti with wine', '35.90'),
                                        ('Kindfire Striploin with wine', '48.90'), ('Kindfire Lamb Rack with wine', '48.90')]),
             ('For two or more', [('Dinner sets for 2 with 2 glasses of wine', '57.90', 'from'), ('Snack and beer sets for 2 with 2 bottles', '51.90', 'from'),
                                  ('The Signature Spread wine set, 4 to 6 people', '219.90')]),
             ('Drinks', [('House pour wine, per glass', '16.90'), ('House pour wine, 2 glasses', '29.90'), ('Wine by the bottle', '79.90', 'from'),
                         ('Cocktails', '18.00'), ("Bailey's Coffee", '9.00'), ('EC 6 signature cocktails set', '89.90'),
                         ('Heineken or Hoegaarden', '12.90'), ('Beer package, 5 bottles', '48.90'), ('Beer package, 10 bottles', '79.90')]),
             ('Coffee and tea', [('Espresso', '4.50'), ('Cappuccino, latte, flat white, Americano', '5.50'), ('Café mocha', '6.00'), ('Iced latte', '6.50'),
                                 ('Matcha latte', '6.00'), ('Goma latte', '7.50'), ('Matcha Tira-Latte', '9.00'), ('Selected fine tea, hot', '6.00')]),
         ],
         faqs=[('Does EC Coffee Bar serve dinner?', 'Yes. Dinner runs until closing (9pm Monday to Saturday, 8pm Sunday), with mains, pasta and dinner sets that include wine.'),
               ('Is there a dinner set for a group?', 'Yes. The Signature Spread wine set feeds 4 to 6 people with six mains and a bottle of house pour wine for $219.90 (July 2025 menu).'),
               ('Which wines do you serve?', 'House pour red and white, plus bottles from France, Italy and other European countries.')]),
]
MNU = {m['slug']: m for m in MENUS}


def tile(href, photo, title, gist, more='More details →'):
    return ('<a class="scard" href="%s">%s<span class="scard-t"><b>%s</b><span>%s</span><em>%s</em></span></a>'
            % (href, img(photo, sm=True), E(title), E(gist), more))


def side_card(topic):
    return f'''<aside class="side"><div class="card sticky"><h2>Book or ask</h2>
<p>Send your date, time, number of guests and the occasion. The team replies on WhatsApp.</p>
{wa_btn(topic=topic)}{enquire_btn(cls='btn btn-ghost')}{map_btn()}
<p class="small">{'<br>'.join(ADDR)}<br>{HOURS_SHORT}</p></div></aside>'''


def event_body(e):
    secs = ''.join('<h2>%s</h2>%s' % (E(h), ''.join('<p>%s</p>' % E(p) for p in ps)) for h, ps in e['sections'])
    others = ''.join('<a class="mini" href="events/%s/">%s<span>%s</span></a>' % (o['slug'], img(o['photo'], sm=True), E(o['short']))
                     for o in EVENTS if o['slug'] != e['slug'])
    rel = [a for a in ARTICLES if e['slug'] in a['links']][:2]
    rel_html = ('<h2>Planning guides</h2><ul class="rel">%s</ul>' % ''.join(
        '<li><a href="articles/%s/">%s</a></li>' % (a['slug'], E(a['h1'])) for a in rel)) if rel else ''
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img(e['photo'], eager=True)}</figure>
{secs}
<h2>Popular for groups</h2>
{pkg_cards(e['pkgs'])}
<p class="small">{E(PRICE_NOTE)}</p>
<h2>Common questions</h2>
{faq_html(e['faqs'])}
{rel_html}
</article>
{side_card(e['short'].lower() + '.')}
</div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>More ways to gather</h2></div><div class="minis">{others}</div></div></section>'''


def menu_body(m):
    groups = ''.join('<h2>%s</h2>%s' % (E(g), price_list(items)) for g, items in m['groups'])
    others = ''.join('<a class="mini" href="menu/%s/">%s<span>%s</span></a>' % (o['slug'], img(o['photo'], sm=True), E(o['short']))
                     for o in MENUS if o['slug'] != m['slug'])
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img(m['photo'], eager=True)}</figure>
{groups}
<p class="small">{E(PRICE_NOTE)} Pictures are for reference.</p>
<h2>Common questions</h2>
{faq_html(m['faqs'])}
</article>
{side_card('a table.')}
</div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>More from the menu</h2></div><div class="minis">{others}
<a class="mini" href="events/">{img('signature-spread', sm=True)}<span>Group events</span></a></div></div></section>'''


# ----------------------------------------------------------------------------------------------
# Articles (planning guides for CBD office organisers; general advice plus confirmed café facts)
# ----------------------------------------------------------------------------------------------
ARTICLES = [
    dict(slug='how-to-plan-a-company-lunch-for-a-big-team', photo='lunch-spread', links=['corporate-events', 'team-lunch'],
         title='How to Plan a Company Lunch for 20 to 50 People | EC Coffee Bar',
         desc='A practical checklist for organising a company lunch for a big team in the CBD: headcount, budget, dietary needs, venue, menu and timing.',
         h1='How to plan a company lunch for 20 to 50 people',
         answer='Fix the date and headcount first, set a per-head budget, collect dietary needs, then book a venue within a short walk of the office that can seat everyone together. Choose sharing sets or a short set menu so ordering is fast, and confirm final numbers two or three days before.',
         body=[
             ('1. Lock the date and a rough headcount', 'Pick two or three possible dates and check them against leave calendars and month-end deadlines. A rough headcount (20, 35, 50) is enough to start asking venues.'),
             ('2. Set the budget per head', 'Agree a per-head figure with whoever approves the claim, and ask whether drinks are included. A clear number makes it easy for the venue to suggest a menu.'),
             ('3. Collect dietary needs early', 'Ask for allergies, vegetarian and no-pork or no-beef needs in the same message as the invitation. Pass the list to the venue when you book, not on the day.'),
             ('4. Choose a venue people can walk to', 'In the CBD, a venue five to ten minutes on foot from the office keeps the lunch to a sensible length. Check it can seat the whole group together and is quiet enough to talk.'),
             ('5. Keep ordering simple', 'Sharing sets or a short set menu save twenty minutes of ordering and splitting bills. For example, at EC Coffee Bar a sharing spread covers a table, and individual lunch sets come with a drink or cake.'),
             ('6. Confirm two or three days before', 'Send the final headcount, dietary list and arrival time to the venue. Share the address and a map link with the team the morning of the lunch.'),
         ]),
    dict(slug='team-bonding-ideas-for-cbd-offices', photo='cheese-wine', links=['team-lunch', 'after-work-drinks'],
         title='Easy Team Bonding Ideas for CBD Offices in Singapore | EC Coffee Bar',
         desc='Low-effort team bonding ideas for busy CBD teams: long lunches, breakfast huddles, afternoon tea, after-work drinks and simple games that fit a workday.',
         h1='Easy team bonding ideas for CBD offices',
         answer='The easiest team bonding fits inside a normal workday: a long team lunch, an early breakfast huddle, an afternoon tea break or after-work drinks nearby. Add one light activity, such as sharing wins from the quarter, and keep it optional and inclusive.',
         body=[
             ('Long team lunch', 'Book a table near the office, order sharing plates and leave the laptops behind. A meal is still the simplest way to get people talking across teams.'),
             ('Breakfast huddle', 'Start a big week with breakfast before 9.30am. Sharing breakfast sets and coffee make it feel like a treat rather than another meeting.'),
             ('Afternoon tea break', 'A cake and tea session mid-afternoon suits teams with mixed schedules and people who do not drink. Order a whole cake if someone has a birthday that week.'),
             ('After-work drinks with food', 'End a project or a quarter with wine, beer or cocktails and plates to share. Always offer non-alcoholic drinks too.'),
             ('Add one light activity', 'Try a round of "best moment of the quarter", a quick quiz about the team, or thank-you notes passed around the table. Keep it short and optional.'),
         ]),
    dict(slug='farewell-lunch-ideas-for-a-colleague', photo='afternoon-tea', links=['celebrations', 'team-lunch'],
         title='Farewell Lunch Ideas for a Colleague in Singapore | EC Coffee Bar',
         desc='How to organise a warm farewell lunch for a colleague: choosing the venue, a card and cake, a short speech and keeping it inclusive.',
         h1='Farewell lunch ideas for a colleague',
         answer='Book a relaxed venue close to the office for a long lunch, collect a group card and a small gift, order a cake to arrive at the end, and keep speeches to one or two short ones. Ask the leaving colleague about food preferences without spoiling the surprise.',
         body=[
             ('Pick a place they would choose', 'Think about what the colleague enjoys: a quiet café, a lively bar or a long lunch with wine. A walkable venue makes it easy for everyone to come.'),
             ('Card, gift and cake', 'Pass a card around a week ahead. Order a whole cake in advance so it is ready when you arrive; a 6 or 8 inch cake usually covers a team.'),
             ('Keep the speech short', 'One manager and one close teammate is plenty. A short story beats a long list of achievements.'),
             ('Make it easy to join', 'Choose a time that suits most people, share the address and map link, and offer non-alcoholic drinks.'),
         ]),
    dict(slug='choosing-a-venue-for-a-client-meeting-in-the-cbd', photo='lamb-wine', links=['vip-room', 'business-breakfast'],
         title='Choosing a Venue for a Client Meeting in the CBD | EC Coffee Bar',
         desc='What to look for in a CBD venue for a client breakfast, lunch or dinner meeting: noise, privacy, timing, menu and how close it is to the office.',
         h1='Choosing a venue for a client meeting in the CBD',
         answer='Choose somewhere quiet enough to talk, within a short walk of your client\'s office, with a menu that is easy to order from. For a sensitive conversation or a group, book a private room. Reserve ahead and arrive early to settle the table and the bill.',
         body=[
             ('Noise level comes first', 'If you cannot hear each other, the meeting fails. Visit at the same time of day beforehand, or ask the venue how busy it gets.'),
             ('Privacy when it matters', 'For pricing, contracts or a group of five or more, a private room is worth it. EC Coffee Bar\'s VIP room seats about 10.'),
             ('Make it easy for the client', 'Pick a place near their office, not yours, and send a map link with the invitation.'),
             ('Breakfast, lunch or dinner?', 'Breakfast is shorter and easier to fit into a diary. Lunch suits a first meeting. Dinner with wine suits a relationship you already have.'),
             ('Handle the bill quietly', 'Arrive early and settle payment with the staff so the bill does not interrupt the conversation.'),
         ]),
    dict(slug='ordering-a-birthday-cake-for-the-office', photo='cake-slices', links=['celebrations'],
         title='Ordering a Birthday Cake for the Office: Size Guide | EC Coffee Bar',
         desc='How big a cake to order for an office birthday, how far ahead to book, and how to plan the surprise, with EC Coffee Bar\'s whole cake sizes and prices.',
         h1='Ordering a birthday cake for the office',
         answer='As a rough guide, a 4 inch cake suits 2 to 4 people, a 6 inch cake 6 to 10 and an 8 inch cake 12 to 16, depending on slice size. Order a few days ahead, check for allergies, and arrange for the cake to come out at the end of the meal.',
         body=[
             ('Rough size guide', 'Cake portions depend on how thin you slice, but the rough guide above works for most offices. If in doubt, size up; leftovers rarely go to waste in an office.'),
             ('Pick a flavour most people like', 'Cheesecake and chocolate are safe choices. A fruit cake is lighter after a big lunch.'),
             ('Order ahead', 'Whole cakes at EC Coffee Bar need a reservation. They come in 4, 6 and 8 inch sizes from $19.90 (July 2025 menu).'),
             ('Plan the surprise', 'Tell the venue the name to write or the moment to bring the cake out, and have someone ready with a lighter and a phone camera.'),
         ]),
]
ART = {a['slug']: a for a in ARTICLES}


def article_body(a):
    secs = ''.join('<h2>%s</h2><p>%s</p>' % (E(h), E(p)) for h, p in a['body'])
    links = ''.join('<a class="mini" href="events/%s/">%s<span>%s</span></a>' % (s, img(EVT[s]['photo'], sm=True), E(EVT[s]['short'])) for s in a['links'])
    more = ''.join('<li><a href="articles/%s/">%s</a></li>' % (o['slug'], E(o['h1'])) for o in ARTICLES if o['slug'] != a['slug'])
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img(a['photo'], eager=True)}</figure>
<p class="answer"><strong>Short answer:</strong> {E(a['answer'])}</p>
{secs}
<p class="byline">By the EC Coffee Bar team, 40 Carpenter Street, Singapore. Updated {UPDATED}.</p>
</article>
{side_card('an event.')}
</div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>Book it at EC Coffee Bar</h2></div><div class="minis">{links}</div>
<h2 style="margin-top:32px">More planning guides</h2><ul class="rel">{more}</ul></div></section>'''


def article_schema(a, path):
    return {'@type': 'Article', 'headline': a['h1'], 'description': a['desc'], 'datePublished': UPDATED, 'dateModified': UPDATED,
            'image': SITE + 'img/' + a['photo'] + '.webp', 'mainEntityOfPage': SITE + path,
            'author': {'@type': 'Organization', 'name': LEGAL, '@id': SITE + '#business'}, 'publisher': {'@id': SITE + '#business'}}


def article_card(a):
    return '<a class="acard" href="articles/%s/">%s<span><b>%s</b>%s</span></a>' % (a['slug'], img(a['photo'], sm=True), E(a['h1']), E(a['answer'][:115].rsplit(' ', 1)[0] + '...'))


# ----------------------------------------------------------------------------------------------
# Home
# ----------------------------------------------------------------------------------------------
FAQ_HOME = [
    ('How many people can EC Coffee Bar host?', 'About %d guests at full capacity, and the VIP room seats about %d. Groups of 10 to 30 get reserved tables in the café.' % (CAPACITY, VIP)),
    ('Is there a minimum order or minimum spend?', 'No. Everyone is welcome, from one person dropping in for coffee to a whole company. For the VIP room or a whole-café booking, ask the team on WhatsApp for the current terms.'),
    ('Roughly how much should I budget per person?', 'From the July 2025 menu: lunch sets $13.90 to $27.90, dinner sets with a glass of wine $25.90 to $48.90, and the Signature Spread for 4 to 6 people $219.90. See the event planner page for the full guide.'),
    ('How do I book an event for my office?', 'WhatsApp %s with the date, time, number of guests, the occasion and any dietary needs. The team replies with availability and menu options. There is a ready-made message on the event planner page.' % WA_SHOW),
    ('Where is EC Coffee Bar, and how do we get there?', 'At 40 Carpenter Street, #01-01, Singapore 059919, a short walk from Clarke Quay MRT and the Raffles Place offices.'),
    ('What are the opening hours?', 'Monday to Saturday 8.30am to 9pm, and Sunday 8.30am to 8pm.'),
]


def home_body():
    ecards = ''.join(tile('events/%s/' % e['slug'], e['photo'], e['short'], e['gist']) for e in EVENTS)
    mcards = ''.join(tile('menu/%s/' % m['slug'], m['photo'], m['short'], m['gist'], 'From $%s · See menu →' % m['from_price']) for m in MENUS)
    gallery = ''.join('<figure>%s</figure>' % img(n, sm=True) for n in ('anniversary-party', 'dining-room-long', 'storefront', 'bar-counter', 'afternoon-tea'))
    return f'''<section class="hero hero-dream">
<div class="aurora" aria-hidden="true"></div>
<div class="wrap hero-grid">
<div class="hero-in">
<p class="eyebrow">Café · Bar · Events · CBD</p>
<h1>The easy venue for your office lunch, event or celebration.</h1>
<p class="lede">A cozy café and bar near Clarke Quay with room for up to {CAPACITY}, a private room for {VIP} and no minimum order. Send one WhatsApp message and the team takes it from there.</p>
<div class="cta-row">{wa_btn(topic='an event.')}{enquire_btn('Event planner\'s guide', cls='btn btn-light')}</div>
</div>
<div class="hero-fig">
<div class="hero-bg">{img('dining-corridor', eager=True)}</div>
<span class="chip c1"><b>{CAPACITY}</b>guests at full capacity</span>
<span class="chip c2"><b>{VIP}</b>seats in the VIP room</span>
<span class="chip c3">Short walk from Clarke Quay MRT</span>
</div>
</div></section>
<div class="facts glance"><div class="wrap">
<div><b>Capacity</b><span>Up to {CAPACITY} guests</span></div>
<div><b>Private room</b><span>VIP room for {VIP}</span></div>
<div><b>Location</b><span>40 Carpenter St, near Clarke Quay MRT</span></div>
<div><b>Book on WhatsApp</b><a href="{E(wa_url())}" target="_blank" rel="noopener">{WA_SHOW}</a></div>
</div></div>
<section class="sec" aria-labelledby="h-plan"><div class="wrap">
<div class="sec-head"><p class="eyebrow">For the person doing the booking</p><h2 id="h-plan">Booking for your office? Here is the short version.</h2></div>
<div class="ptiles">
<div class="ptile"><b>Fits your group</b><p>VIP room for about {VIP}, reserved tables for 10 to 30, or the whole café for up to {CAPACITY}.</p></div>
<div class="ptile"><b>Budget guide</b><p>Lunch sets $13.90 to $27.90 a head, dinner sets with wine $25.90 to $48.90, sharing spread for 4 to 6 $219.90.</p></div>
<div class="ptile"><b>One message to book</b><p>Date, time, headcount, occasion and dietary needs on WhatsApp. The team replies with options.</p></div>
<div class="ptile"><b>No surprises</b><p>No minimum order. Open daily from 8.30am. Company details on the About page for your records.</p></div>
</div>
<div class="cta-row">{enquire_btn('Read the event planner\'s guide')}{wa_btn(topic='an event.', cls='btn btn-ghost')}</div>
</div></section>
<section class="sec sec-alt" aria-labelledby="h-evt"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Occasions</p><h2 id="h-evt">Pick the occasion for details and prices</h2></div>
<div class="scards">{ecards}</div>
</div></section>
<section class="sec sec-dark" aria-labelledby="h-why"><div class="wrap split2">
<div><p class="eyebrow">Where Chicks Grow into Eagles</p><h2 id="h-why">A calm, happy place to bring the team.</h2>
<ul class="ticks">
<li><b>Room for everyone.</b> Up to {CAPACITY} guests in the café, a VIP room for {VIP}, and small groups just as welcome.</li>
<li><b>Easy to order for a group.</b> Sharing sets, lunch sets and drink packages, so nobody has to collect 30 orders.</li>
<li><b>Easy to reach.</b> 40 Carpenter Street, a short walk from Clarke Quay MRT and the Raffles Place offices.</li>
</ul>
<a class="btn btn-light" href="about/">Our story</a></div>
<div class="gallery">{gallery}</div>
</div></section>
<section class="sec" aria-labelledby="h-menu"><div class="wrap">
<div class="sec-head"><p class="eyebrow">The menu</p><h2 id="h-menu">Breakfast to dinner, all day</h2></div>
<div class="scards">{mcards}</div>
</div></section>
<section class="sec sec-alt" aria-labelledby="h-faq"><div class="wrap narrow">
<div class="sec-head"><h2 id="h-faq">Quick answers</h2></div>
{faq_html(FAQ_HOME)}
<p class="small" style="margin-top:18px">Planning a team outing? Read our <a href="articles/">planning guides</a>.</p>
</div></section>'''

def events_index():
    cards = ''.join(tile('events/%s/' % e['slug'], e['photo'], e['short'], e['gist']) for e in EVENTS)
    return f'''<section class="sec"><div class="wrap"><div class="scards">{cards}</div></div></section>
<section class="sec sec-alt"><div class="wrap"><div class="sec-head"><h2>Group packages from the menu</h2><p>{E(PRICE_NOTE)}</p></div>
{pkg_cards(['spread', 'lunch', 'sunrise', 'tea', 'cocktails', 'beer', 'cheese', 'cakes'])}</div></section>'''


def menu_index():
    cards = ''.join(tile('menu/%s/' % m['slug'], m['photo'], m['short'], m['gist'], 'From $%s · See menu →' % m['from_price']) for m in MENUS)
    return f'''<section class="sec"><div class="wrap"><div class="scards">{cards}</div>
<p class="small" style="margin-top:20px">{E(PRICE_NOTE)}</p></div></section>'''


def articles_index():
    return '<section class="sec"><div class="wrap"><div class="acards">%s</div></div></section>' % ''.join(article_card(a) for a in ARTICLES)


def about_body():
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img('bar-counter', eager=True)}</figure>
<p>EC Coffee Bar ({ZH}) is an all-day café, bar and business event space at 40 Carpenter Street in Singapore's CBD, a short walk from Clarke Quay and Raffles Place. It was set up for entrepreneurs, professionals and urban dreamers: a place to meet, recharge and rise together.</p>
<p>The café was opened in 2024 by its founder, <a href="{FOUNDER[1]}" target="_blank" rel="noopener">{FOUNDER[0]}</a>.</p>
<h2>Where Chicks Grow into Eagles</h2>
<p>The name carries the idea. E is for Entrepreneurs and C is for Chick, and the house motto is "Where Chicks Grow into Eagles". The chick in the logo, sitting in a coffee cup, is the start of that journey. In the café's own words: "We offer more than just great food. We create space for connection, ideas, and growth."</p>
<h2>What we serve</h2>
<p>Power breakfasts, artisan coffee and wholesome brunch from 8.30am, lunch sets for the working day, afternoon tea with low-sugar cakes, and cozy dinners with wine, beer and cocktails.</p>
<h2>Made for groups</h2>
<p>The café holds about {CAPACITY} guests at full capacity, and a VIP room seats about {VIP}. Company lunches, team bonding, client meetings, birthdays and farewells are all part of a normal week here.</p>
<figure>{img('storefront')}<figcaption>The entrance at 40 Carpenter Street, look for the pink chick sign.</figcaption></figure>
<h2>Company details</h2>
<p>{LEGAL} (UEN {UEN}), incorporated 23 April 2024. Registered activity: cafés (SSIC 56112) and restaurants.<br>{'<br>'.join(ADDR)}<br>
WhatsApp: <a href="{E(wa_url())}" target="_blank" rel="noopener">{WA_SHOW}</a> · Email: <a href="mailto:{EMAIL}">{EMAIL}</a><br>
Instagram, TikTok, WeChat and Xiaohongshu: eccoffeebar</p>
</article>
<aside class="side"><div class="card sticky"><h2>Visit us</h2><p>{'<br>'.join(ADDR)}</p>{hours_html()}{wa_btn()}{map_btn()}</div></aside>
</div></section>'''


def enquiry_form(heading='Plan an event'):
    occasions = ['Company lunch or dinner', 'Team bonding', 'VIP room booking', 'Birthday or farewell', 'Business breakfast or meeting', 'After-work drinks', 'Whole cake order', 'Table booking']
    opts = ''.join('<option>%s</option>' % E(o) for o in occasions)
    return f'''<form class="enquiry" id="enquiry" action="https://wa.me/{WA_NUM}" method="get" target="_blank">
<h2>{E(heading)}</h2>
<p class="small">Fill this in and tap the button. It opens WhatsApp with your message ready to send.</p>
<label>Occasion<select name="o">{opts}</select></label>
<div class="row2"><label>Date<input name="d" type="date"></label><label>Time<input name="t" type="time" value="12:30"></label></div>
<div class="row2"><label>Number of guests<input name="p" type="number" min="1" max="{CAPACITY}" value="10"></label><label>Your name and company<input name="n" type="text" autocomplete="organization"></label></div>
<label>Anything else? (budget per person, dietary needs, cake)<textarea name="x" rows="3"></textarea></label>
<input type="hidden" name="text" value="{E(WA_MSG + 'an event.')}">
<button class="btn btn-wa" type="submit">{WA_SVG}<span>Send on WhatsApp</span></button>
</form>'''


BRIEF = ('a company event.\n\n'
         'Company: \nDate and time: \nNumber of guests: \nOccasion: \nBudget per person: \nDietary needs: \nAnything else (room, cake, speech): ')
BUDGET = [  # (occasion, what is on the menu, guide per person) from the July 2025 menu
    ('Breakfast meeting', 'Breakfast sets with a drink, from a croissant to the Signature Breakfast Platter', '$9.90 to $21.90'),
    ('Team lunch', 'Lunch sets with a drink or cake. The EC mixed lunch set for sharing is $100.90', '$13.90 to $27.90'),
    ('Afternoon tea', 'Cake and drink sets. The EC afternoon Glow Tea Set is $39.90 (reserve ahead)', '$12.90 to $14.90'),
    ('Dinner', 'Dinner sets with a glass of wine, from aglio olio to lamb rack', '$25.90 to $48.90'),
    ('Sharing dinner with wine', 'The Signature Spread: six mains and a bottle of wine for 4 to 6 people, $219.90', 'about $37 to $55'),
    ('Drinks add-ons', 'Beer package of 10 bottles $79.90 · 6 signature cocktails $89.90 · wine by the bottle from $79.90', 'per package'),
    ('Celebration cake', 'Whole cakes in 4, 6 and 8 inch: cheesecake, hazelnut truffle, berry or Biscoff', '$19.90 to $79.90 per cake'),
]
FAQ_PLAN = [
    ('Is there a minimum spend, room charge or deposit?', 'There is no minimum order for a table. For the VIP room or a whole-café booking, the team confirms any room terms, deposit and cancellation policy when it confirms your date. Ask on WhatsApp and you will have it in writing in the chat.'),
    ('Can the café invoice my company?', 'Ask the team when you book. For your records, the café is EC Coffee Bar Pte. Ltd., UEN %s, at 40 Carpenter Street, #01-01, Singapore 059919.' % UEN),
    ('Can we make a speech or show slides?', 'A short speech or toast is no problem. For a screen, projector or microphone, tell the team what you need when you enquire and they will confirm what is available for your date.'),
    ('How do you handle dietary needs?', 'List allergies and dietary needs in your booking message. The menu is Western café food with chicken, beef, lamb, fish, pasta and rice dishes, and the kitchen will advise which suit your guests.'),
    ('How far ahead should I book?', 'As early as you can. A table for ten needs less notice than the VIP room or the whole café. Send your date first and the team will tell you what is open.'),
    ('Can we order a cake for the occasion?', 'Yes. Whole cakes come in 4, 6 and 8 inch sizes from $19.90 and need to be reserved ahead. If you would rather bring your own cake, ask the team first.'),
    ('How do guests get there?', 'Clarke Quay MRT is a short walk away, and so are the Raffles Place offices. Use the Google Maps link on this page for directions, and ask the team about parking nearby.'),
    ('What time can an evening event run until?', 'The café is open until 9pm Monday to Saturday and 8pm on Sunday. Ask the team if your plan needs a different time.'),
]


def plan_body():
    sheet = [('Guests', 'Up to about %d at full capacity' % CAPACITY), ('Private room', 'VIP room for about %d' % VIP),
             ('Minimum order', 'None'), ('Address', '40 Carpenter Street, #01-01, Singapore 059919'),
             ('Nearest MRT', 'Clarke Quay, a short walk'), ('Hours', HOURS_SHORT),
             ('Food', 'Western café menu, breakfast to dinner, cakes to order'), ('Drinks', 'Coffee, tea, wine, cocktails and beer'),
             ('Book by', 'WhatsApp %s or %s' % (WA_SHOW, EMAIL)), ('Company', '%s, UEN %s' % (LEGAL, UEN))]
    sheet_html = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (E(k), E(v)) for k, v in sheet)
    rows = ''.join('<li><b>%s</b><span>%s</span><em>%s</em></li>' % (E(o), E(w), E(g)) for o, w, g in BUDGET)
    return f'''<section class="sec"><div class="wrap">
<div class="sec-head"><p class="eyebrow">The venue at a glance</p><h2>The facts for your booking form</h2></div>
<dl class="sheet">{sheet_html}</dl>
</div></section>
<section class="sec sec-alt" aria-labelledby="h-fit"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Step 1</p><h2 id="h-fit">Which setup fits your group?</h2></div>
<div class="setups">
<div class="setup"><b>Up to {VIP}</b><strong>The VIP room</strong><p>A private room for a client lunch, a board meeting or a small farewell. Door closed, your own table.</p><a href="events/vip-room/">About the VIP room →</a></div>
<div class="setup"><b>10 to 30</b><strong>Reserved tables in the café</strong><p>Long tables for a team lunch or an after-work gathering, with the rest of the café open as usual.</p><a href="events/team-lunch/">Team lunches →</a></div>
<div class="setup"><b>30 to {CAPACITY}</b><strong>The whole café</strong><p>Company lunches, dinners, launches and anniversaries for the whole office. Ask the team about booking the full room.</p><a href="events/corporate-events/">Corporate events →</a></div>
</div></div></section>
<section class="sec" aria-labelledby="h-budget"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Step 2</p><h2 id="h-budget">Budget guide, per person</h2><p>Worked out from the café\'s {MENU_DATE} menu so you can quote a figure before you enquire. Confirm current prices, GST and service charge with the team.</p></div>
<ul class="budget"><li class="bhead"><b>Occasion</b><span>What\'s on the menu</span><em>Guide per person</em></li>{rows}</ul>
<p class="small">{E(PRICE_NOTE)}</p>
</div></section>
<section class="sec sec-alt" aria-labelledby="h-how"><div class="wrap">
<div class="sec-head"><p class="eyebrow">Step 3</p><h2 id="h-how">How booking works</h2></div>
<ol class="steps">
<li><strong>Send one message</strong><p>WhatsApp the date, time, headcount, occasion and dietary needs. Copy the template below or use the form.</p></li>
<li><strong>Get options back</strong><p>The team replies on WhatsApp with availability for your date and menu suggestions for your budget.</p></li>
<li><strong>Confirm and relax</strong><p>Agree the menu and any room terms in the chat, then send the final headcount a few days before.</p></li>
</ol>
</div></section>
<section class="sec" aria-labelledby="h-brief"><div class="wrap split">
<div class="prose">
<h2 id="h-brief">Send your brief in one tap</h2>
<p>This opens WhatsApp with the message below. Fill in the blanks and send.</p>
<pre class="brief">Hi EC Coffee Bar, I would like to ask about a company event.

Company:
Date and time:
Number of guests:
Occasion:
Budget per person:
Dietary needs:
Anything else (room, cake, speech):</pre>
{wa_btn('Open this message in WhatsApp', topic=BRIEF)}
<h2>Or fill in the form</h2>
{enquiry_form('Event enquiry')}
<h2>Questions office managers ask us</h2>
{faq_html(FAQ_PLAN)}
</div>
{side_card('a company event.')}
</div></section>'''


def contact_body():
    return f'''<section class="sec"><div class="wrap split">
<div class="prose">
<h2>WhatsApp the café</h2>
<p class="big"><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></p>
<p>The quickest way to book a table, the VIP room or a group event. Tell us the date, time, number of guests and the occasion. Booking for your office? The <a href="plan-an-event/">event planner page</a> has capacity, a budget guide and a ready-made message.</p>
{enquiry_form()}
<h2>Address</h2>
<p>{LEGAL}<br>{'<br>'.join(ADDR)}</p>
<p>On Carpenter Street, a short walk from Clarke Quay MRT, Hong Lim Park and the Raffles Place offices.</p>
<h2>Opening hours</h2>
{hours_html()}
<p class="small">Public holiday hours may differ. WhatsApp us before you come.</p>
<h2>Email and social</h2>
<p><a href="mailto:{EMAIL}">{EMAIL}</a><br><a href="{IG}" target="_blank" rel="noopener">Instagram @eccoffeebar</a> · <a href="{TIKTOK}" target="_blank" rel="noopener">TikTok @eccoffeebar</a><br>WeChat and Xiaohongshu ID: eccoffeebar</p>
</div>
<div class="mapbox"><iframe title="Map to EC Coffee Bar at 40 Carpenter Street" src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
</div></section>'''


def business_schema():
    return {'@type': ['CafeOrCoffeeShop', 'BarOrPub'], '@id': SITE + '#business', 'name': NAME, 'legalName': LEGAL, 'alternateName': ['EC Coffeebar', 'EC COFFEE. BAR', ZH],
            'url': SITE, 'telephone': TEL, 'email': EMAIL, 'openingHoursSpecification': HOURS_LD,
            'image': [SITE + 'img/' + n + '.webp' for n in ('dining-corridor', 'bar-counter', 'signature-spread')], 'logo': SITE + 'icon-192.png',
            'address': {'@type': 'PostalAddress', 'streetAddress': STREET, 'addressLocality': 'Singapore', 'postalCode': POSTAL, 'addressCountry': 'SG'},
            'geo': {'@type': 'GeoCoordinates', 'latitude': GEO[0], 'longitude': GEO[1]},
            'hasMap': MAP, 'foundingDate': '2024-04-23', 'founder': {'@type': 'Person', 'name': FOUNDER[0], 'url': FOUNDER[1]}, 'sameAs': [IG, TIKTOK],
            'servesCuisine': ['Cafe', 'All-day breakfast', 'Western', 'Coffee', 'Cakes'], 'priceRange': '$$', 'acceptsReservations': True,
            'hasMenu': SITE + 'menu/', 'maximumAttendeeCapacity': CAPACITY,
            'amenityFeature': [{'@type': 'LocationFeatureSpecification', 'name': 'Private VIP room for about %d guests' % VIP, 'value': True},
                               {'@type': 'LocationFeatureSpecification', 'name': 'Group and corporate event bookings', 'value': True},
                               {'@type': 'LocationFeatureSpecification', 'name': 'No minimum order; individuals and small groups welcome', 'value': True}],
            'identifier': {'@type': 'PropertyValue', 'propertyID': 'UEN', 'value': UEN},
            'slogan': 'Where Chicks Grow into Eagles', 'areaServed': 'Singapore CBD'}


# ----------------------------------------------------------------------------------------------
# Register pages
# ----------------------------------------------------------------------------------------------
page('', 'EC Coffee Bar | Café, Bar & Event Space in the CBD, Singapore',
     'EC Coffee Bar, 40 Carpenter Street near Clarke Quay: the easy venue for office lunches, company events and celebrations. Up to 50 guests, a VIP room for 10, no minimum order. WhatsApp 9365 6626.',
     NAME, home_body(), hero=False, schema=[faq_schema(FAQ_HOME)])
page('events/', 'Corporate Events, Team Lunches & Celebrations | EC Coffee Bar',
     'Company events for up to 50, team lunches, a VIP room for 10, birthdays, farewells and after-work drinks at EC Coffee Bar near Clarke Quay and Raffles Place.',
     'Events and group bookings', events_index(), crumbs=[('events/', 'Events')],
     lede='Groups of every size are welcome, from a table of three to company events for up to %d guests, with a VIP room for %d and no minimum order.' % (CAPACITY, VIP))
for e in EVENTS:
    path = 'events/%s/' % e['slug']
    page(path, e['title'], e['desc'], e['h1'], event_body(e), crumbs=[('events/', 'Events'), (path, e['short'])], lede=e['lede'],
         photo=e['photo'], schema=[{'@type': 'Service', 'name': e['h1'], 'serviceType': e['short'], 'description': e['desc'], 'url': SITE + path,
                                    'provider': {'@id': SITE + '#business'}, 'areaServed': 'Singapore CBD'}, faq_schema(e['faqs'])])
page('plan-an-event/', 'Plan a Company Event in the CBD | Capacity, Budget Guide & Booking | EC Coffee Bar',
     'Everything an office manager or PA needs to book EC Coffee Bar: room for up to 50, a VIP room for 10, per-person budget guide from the menu, how booking works and a ready-made WhatsApp brief.',
     'Plan a company event at EC Coffee Bar', plan_body(), crumbs=[('plan-an-event/', 'Plan an event')],
     lede='Everything the person doing the booking needs on one page: capacity, room options, a budget guide, how booking works and the questions we will ask you.',
     schema=[{'@type': 'Service', 'name': 'Company event venue booking', 'serviceType': 'Event venue', 'url': SITE + 'plan-an-event/',
              'provider': {'@id': SITE + '#business'}, 'areaServed': 'Singapore CBD'}, faq_schema(FAQ_PLAN)])
page('menu/', 'Menu & Prices | Breakfast, Lunch, Cakes & Wine | EC Coffee Bar',
     'EC Coffee Bar menu with prices: all-day breakfast sets from $9.90, lunch sets, afternoon tea and whole cakes, dinner with wine, cocktails and beer.',
     'Menu and prices', menu_index(), crumbs=[('menu/', 'Menu')],
     lede='Breakfast, lunch, afternoon tea and dinner with wine, served all day at 40 Carpenter Street.')
for m in MENUS:
    path = 'menu/%s/' % m['slug']
    page(path, m['title'], m['desc'], m['h1'], menu_body(m), crumbs=[('menu/', 'Menu'), (path, m['short'])], lede=m['lede'],
         photo=m['photo'], schema=[faq_schema(m['faqs'])])
page('articles/', 'Planning Guides for Office Events | EC Coffee Bar',
     'Guides for CBD office organisers: planning a company lunch, team bonding ideas, farewell lunches, client meeting venues and ordering office birthday cakes.',
     'Planning guides', articles_index(), crumbs=[('articles/', 'Articles')],
     lede='Practical guides for whoever is organising the next team lunch, farewell or client meeting.')
for a in ARTICLES:
    path = 'articles/%s/' % a['slug']
    page(path, a['title'], a['desc'], a['h1'], article_body(a), crumbs=[('articles/', 'Articles'), (path, a['h1'])],
         photo=a['photo'], schema=[article_schema(a, path)])
page('about/', 'About EC Coffee Bar | Where Chicks Grow into Eagles',
     'EC Coffee Bar (创鸡咖啡吧) is an all-day café, bar and business event space for professionals at 40 Carpenter Street, Singapore. UEN 202416189N.',
     'About EC Coffee Bar', about_body(), crumbs=[('about/', 'About')],
     lede='An all-day café, bar and business event space for entrepreneurs and professionals in the CBD.')
page('contact/', 'Book a Table or Event | WhatsApp 9365 6626 | EC Coffee Bar',
     'Book EC Coffee Bar on WhatsApp 9365 6626. 40 Carpenter Street, #01-01, Singapore 059919. Open Mon-Sat 8.30am-9pm, Sun 8.30am-8pm.',
     'Book a table or an event', contact_body(), crumbs=[('contact/', 'Contact')], cta=False,
     lede='WhatsApp %s, email %s, or visit us at 40 Carpenter Street.' % (WA_SHOW, EMAIL))


# ----------------------------------------------------------------------------------------------
# Render
# ----------------------------------------------------------------------------------------------
def render(path, p):
    pre = '../' * path.count('/')
    url = SITE + path
    share = SITE + 'og-image.jpg'  # 1200x630 JPG (WhatsApp needs jpg/png, not webp); file og-image.jpg sits next to build.py and is copied to site/

    def fix(s):
        return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|\.\./|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), pre, m.group(2)), s)

    nav = ''.join('<a href="%s%s"%s>%s</a>' % (pre, h, ' aria-current="page"' if path.startswith(h) else '', t) for h, t in NAV)
    crumbs_html, crumbs_ld = '', None
    if p['crumbs']:
        parts = ['<a href="%s">Home</a>' % (pre or './')] + ['<a href="%s%s">%s</a>' % (pre, h, E(t)) for h, t in p['crumbs'][:-1]] + ['<span>%s</span>' % E(p['crumbs'][-1][1])]
        crumbs_html = '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % ' / '.join(parts)
        crumbs_ld = {'@type': 'BreadcrumbList', 'itemListElement': [{'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': SITE}] +
                     [{'@type': 'ListItem', 'position': i + 2, 'name': t, 'item': SITE + h} for i, (h, t) in enumerate(p['crumbs'])]}
    graph = [business_schema(), {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': p['title'], 'description': p['desc'],
                                 'inLanguage': 'en-SG', 'dateModified': UPDATED, 'about': {'@id': SITE + '#business'},
                                 'isPartOf': {'@type': 'WebSite', 'url': SITE, 'name': NAME}}]
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
        band = ('<section class="sec"><div class="wrap"><div class="band"><div><h2>Planning a team lunch or event?</h2>'
                '<p>WhatsApp the date, time and headcount. Any group size from 1 to %d, no minimum order. VIP room for %d.</p></div><div class="cta-row">%s%s</div></div></div></section>') % (
            CAPACITY, VIP, wa_btn(topic='an event.'), enquire_btn(cls='btn btn-light'))
        band = fix(band)
    robots = 'noindex,nofollow' if NOINDEX else 'index,follow,max-image-preview:large'
    title = E(p['title'])
    lcp = p['photo'] or ('dining-corridor' if path == '' else None)
    preload = '<link rel="preload" as="image" href="%s%s%s.webp" fetchpriority="high">' % ('' if IMG.startswith('http') else pre, IMG, lcp) if lcp else ''
    body = fix(p['body'])
    brand = brand_html(pre)
    return f'''<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{E(p['desc'])}">
<meta name="robots" content="{robots}">
<meta name="p1-site" content="{SLUG}">
<meta name="theme-color" content="#7d2e57">
<link rel="canonical" href="{url}">
{preload}
<meta property="og:type" content="{'article' if path.startswith('articles/') and path != 'articles/' else 'website'}">
<meta property="og:site_name" content="{NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{E(p['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:locale" content="en_SG">
<meta property="og:image" content="{share}">
<meta property="og:image:secure_url" content="{share}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{share}">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48">
<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="stylesheet" href="{pre}ec.css?v=6">
<script src="{pre}ec.js?v=5" defer></script>
<script type="application/ld+json">{ld}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="strip"><div class="wrap"><span>{STREET}, Singapore {POSTAL} · {HOURS_SHORT}</span><span class="strip-r"><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></span></div></div>
<header class="hdr"><div class="wrap">
{brand}
<nav class="nav" id="mnav" aria-label="Main">{nav}</nav>
{wa_btn('Book', cls='btn btn-wa hdr-call')}
<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mnav">Menu</button>
</div></header>
<main id="main">
{head_hero}
{body}
{band}
</main>
<footer class="ftr"><div class="wrap">
<div class="ftr-grid">
<div>{brand}
<p>All-day café, bar and business event space for professionals in Singapore's CBD. Where Chicks Grow into Eagles.</p></div>
<div><h3>Events</h3><ul>{''.join('<li><a href="%sevents/%s/">%s</a></li>' % (pre, e['slug'], E(e['short'])) for e in EVENTS)}</ul></div>
<div><h3>Visit</h3><ul>
<li>{'<br>'.join(ADDR)}</li>
<li><a href="{E(wa_url())}" target="_blank" rel="noopener">WhatsApp {WA_SHOW}</a></li>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li>{HOURS_SHORT}</li>
<li><a href="{MAP}" target="_blank" rel="noopener">Google Maps</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
<li><a href="{pre}menu/">Menu</a> · <a href="{pre}articles/">Guides</a> · <a href="{pre}about/">About</a> · <a href="{pre}contact/">Contact</a></li>
</ul></div>
</div>
<div class="ftr-legal"><span>{LEGAL} · UEN {UEN}</span><span>© 2026 {LEGAL} · Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a></span></div>
</div></footer>
<div class="dock"><a class="dock-wa" href="{E(wa_url())}" target="_blank" rel="noopener" aria-label="WhatsApp EC Coffee Bar on {WA_SHOW}">{WA_SVG}<span>WhatsApp to book</span></a></div>
</body>
</html>
'''


def not_found():
    body = ('<section class="sec"><div class="wrap prose"><p>The page you were looking for has moved or does not exist. These may help:</p>'
            '<ul>%s</ul></div></section>') % ''.join('<li><a href="%s">%s</a></li>' % (h or './', t) for h, t in [('', 'Home')] + NAV)
    p = dict(title='Page not found | EC Coffee Bar', desc='This page could not be found.', h1='Sorry, that page is not here.', body=body,
             crumbs=None, lede='', schema=[], hero=True, cta=True, photo=None)
    out = render('', p).replace('content="index,follow,max-image-preview:large"', 'content="noindex"')
    base = '/' if LIVE else '/preview/%s/' % SLUG
    return re.sub(r'(href|src|action)="(?!https?:|mailto:|tel:|#|/|data:)([^"]*)"', lambda m: '%s="%s%s"' % (m.group(1), base, m.group(2) if m.group(2) != './' else ''), out)


HTACCESS = """# EC Coffee Bar ({DOMAIN}). This folder is {DOMAIN}'s document root and also
# pageonesingapore.com/preview/ec-coffee-bar/. It overrides the parent pageonesingapore.com .htaccess.
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\\.(.+)$ [NC]
RewriteRule ^ https://%1%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTPS} off
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
RewriteCond %{HTTP_HOST} ^{DQ}$ [NC]
RewriteCond %{THE_REQUEST} \\s/(.*/)?index\\.html[\\s?] [NC]
RewriteRule ^(.*/)?index\\.html$ https://{DOMAIN}/$1 [L,R=301]
ErrorDocument 404 /404.html
"""

BOTS = ['Googlebot', 'Bingbot', 'OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'ClaudeBot', 'Claude-SearchBot',
        'Google-Extended', 'Applebot-Extended', 'DuckAssistBot']


def main():
    for path, p in PAGES.items():
        d = os.path.join(OUT, path)
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, 'index.html'), 'w') as f:
            f.write(render(path, p))
    if os.path.exists(os.path.join(HERE, 'og-image.jpg')):
        shutil.copy(os.path.join(HERE, 'og-image.jpg'), os.path.join(OUT, 'og-image.jpg'))
    with open(os.path.join(OUT, '404.html'), 'w') as f:
        f.write(not_found())
    with open(os.path.join(OUT, 'robots.txt'), 'w') as f:
        f.write(''.join('User-agent: %s\nAllow: /\n\n' % b for b in BOTS) + 'User-agent: *\nAllow: /\n\nSitemap: %ssitemap.xml\n' % SITE)
    with open(os.path.join(OUT, 'sitemap.xml'), 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for path in PAGES:
            f.write('  <url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, path, UPDATED))
        f.write('</urlset>\n')
    with open(os.path.join(OUT, 'llms.txt'), 'w') as f:
        f.write('# %s (%s), café, bar and event space in Singapore\'s CBD\n\n'
                '> %s is an all-day café, bar and business event space at %s, Singapore %s (UEN %s), a short walk from Clarke Quay MRT '
                'and Raffles Place. It hosts company events, team lunches, team bonding and group celebrations for up to about %d guests, '
                'and has a VIP room for about %d. Everyone is welcome, from individuals and small groups to large corporate groups, with no minimum order. Open Monday to Saturday 8.30am-9pm and Sunday 8.30am-8pm. Bookings by WhatsApp %s '
                '(+65 %s) or %s. Breakfast sets from $9.90, lunch sets from $13.90, whole cakes from $19.90, the Signature Spread wine set '
                'for 4-6 people $219.90 (%s menu). Motto: "Where Chicks Grow into Eagles" (E for Entrepreneurs, C for Chick). Founded in 2024 by %s (%s).\n\n## Pages\n'
                % (NAME, ZH, LEGAL, STREET, POSTAL, UEN, CAPACITY, VIP, WA_SHOW, WA_SHOW, EMAIL, MENU_DATE, FOUNDER[0], FOUNDER[1]))
        for path, p in PAGES.items():
            f.write('- [%s](%s%s): %s\n' % (p['title'].split(' | ')[0], SITE, path, p['desc']))
    with open(os.path.join(OUT, 'site.webmanifest'), 'w') as f:
        json.dump({'name': LEGAL, 'short_name': NAME, 'icons': [
            {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'}],
            'theme_color': '#7d2e57', 'background_color': '#fffafb', 'display': 'browser'}, f)
    with open(os.path.join(OUT, '.htaccess'), 'w') as f:
        dom = DOMAIN or 'CLIENT-DOMAIN'
        f.write(HTACCESS.replace('{DOMAIN}', dom).replace('{DQ}', dom.replace('.', r'\.')))
    print('built %d pages' % len(PAGES))


if __name__ == '__main__':
    main()
