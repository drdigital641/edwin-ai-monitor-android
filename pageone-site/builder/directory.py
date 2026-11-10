# Directory listing plan explainer (Edwin, 1 Nov 2026): /directory-listing/ on Page One.
# The directory itself will live on a separate niche car-workshop domain (not bought yet), so Page One has NO
# /directory/ hub and links to no directory URL. The listing template is standalone: builder/directory_listing.py.
# Facts rule: no invented price, no promise of leads or rankings. Run from build.py (exec) after lead_gen.py.

DIRECTORY_PRICE = None     # S$/month, Verified directory listing (Edwin, 1 Nov 2026). Not the old S$20 early-bird SEO plan. None = "ask us on WhatsApp"
DIRECTORY_DOMAIN = None  # e.g. "sgcarworkshop.sg" once bought; None = not named on the site yet

_DIR_WA_MSG = "Hi Edwin, I'd like to ask about the directory listing plan."


def _dir_price_text():
    return "Ask us for the directory price on WhatsApp" if DIRECTORY_PRICE is None else f"Verified listing S${DIRECTORY_PRICE}/month"


def _dir_where():
    return ("on our car workshop directory site" if DIRECTORY_DOMAIN is None
            else f"on our car workshop directory, {DIRECTORY_DOMAIN}")


def _dir_btns(source):
    return f"""
        <div class="cta-row">
          <a class="btn" href="{wa_src(_DIR_WA_MSG, source)}" target="_blank" rel="noopener" data-cta="whatsapp_directory_{source.split(',')[-1].strip()}">Ask about the directory plan</a>
          <a class="btn btn-ghost" href="/get-found/">See the own-domain plan</a>
        </div>"""


DIR_URL = "/directory-listing/"
DIR_FAQ = [
    ("How much does a directory listing cost?",
     "A Basic listing card is free. For a Verified listing page, ask us on WhatsApp for the price. The own-website plan is S$80 a month."),
    ("Do I need to buy a domain?",
     "No. We set up your listing page and keep it running. You don't buy, register or renew a domain for it."),
    ("Will a listing bring me enquiries?",
     "We can't promise that. A listing gives customers a page to check you out and a one-tap way to message you. We count WhatsApp taps on it and send you the numbers every month, so you can see what it brings."),
]

_dir_rows = [
    ("Where customers find you", "Your own domain, such as yourbusiness.sg", f"One page {_dir_where()}"),
    ("Pages", "A full website: homepage and a page for each service", "One listing page"),
    ("Articles", "A new article every 2 days", "None"),
    ("SEO work", "Daily technical audit and SEO work", "Light: the listing is added to the directory"),
    ("Price", "S$80 a month, website included", _dir_price_text()),
]
_dir_table = "\n".join(f'              <tr><th scope="row">{a}</th><td>{b}</td><td>{c}</td></tr>' for a, b, c in _dir_rows)

page("directory-listing/index.html",
     "Directory Listing Plan: One Page for Your Business",
     "No website or domain of your own? Get one listing page with your photos, services, hours and WhatsApp and call buttons. Ask us on WhatsApp for the price.",
     [_faq_ld(DIR_FAQ)],
     hero("Directory listing", "Directory listing plan",
          "No website of your own? Get a listing page instead.",
          "A directory listing is one page about your business: your photos, services, area and opening hours, with WhatsApp and call buttons. "
          "You don't buy a domain, and we look after the page.",
          f'<p class="hero-price"><b>{_dir_price_text()}</b> · free basic card · own website S$80/month</p>',
          buttons=False).replace('</p>\n      </div>\n    </section>', '</p>' + _dir_btns("directory, top") + '\n      </div>\n    </section>', 1) + f"""

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Who it is for</p>
        <h2 class="reveal">Businesses that want to be found, without a website of their own</h2>
        <p class="reveal">It suits owners who want customers to find and contact them, but don't want to pay for a domain or run a full website. Listings are for car workshops first, shown {_dir_where()}, and the directory is not live yet.</p>
        <p class="kicker reveal" style="margin-top:32px">What you get</p>
        <h2 class="reveal">One page that does the basics</h2>
        <ul class="ticks reveal">
          <li>One listing page with photos of your work</li>
          <li>Your services, the area you serve and your opening hours</li>
          <li>WhatsApp and call buttons, so enquiring takes one tap</li>
          <li>A link to your Google Business Profile, if you have one</li>
          <li>WhatsApp taps counted and reported to you every month</li>
        </ul>
        <p class="reveal">Everything on the page comes from you, and we check it with you before it goes up.</p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Two ways to go live</p>
        <h2 class="reveal">Own domain or directory listing</h2>
        <div class="table-wrap reveal">
          <table class="compare">
            <thead><tr><th></th><th scope="col">Own domain</th><th scope="col">Directory listing</th></tr></thead>
            <tbody>
{_dir_table}
            </tbody>
          </table>
        </div>
        <p class="reveal">With light SEO, a single listing page is less likely to be found for competitive searches than a full website. If you want the full site and daily SEO, the <a class="link" href="/get-found/">own-domain plan</a> is the main one. See <a class="link" href="/pricing/">pricing</a>.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Directory listing: your questions, answered</h2>
{_faq_html(DIR_FAQ)}
      </div>
    </section>

    <section class="cta-band">
      <div class="wrap">
        <h2>Want a listing page?</h2>
        <p>Tell Edwin what you do and where. No obligation.</p>
        <div class="cta-row center">
          <a class="btn" href="{wa_src(_DIR_WA_MSG, "directory, bottom")}" target="_blank" rel="noopener" data-cta="whatsapp_directory_bottom">Ask about the directory plan</a>
        </div>
      </div>
    </section>
""",
     crumb="Directory listing", updated="2026-11-01")
