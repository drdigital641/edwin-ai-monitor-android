# Lead generation repositioning (Edwin, 28 Oct 2026; brief in edwin-ai-context handoffs/2026-10-28-...).
# Page One sells "get found, get enquiries": the website is included, SEO/AEO/GEO are how customers find you,
# and the WhatsApp buttons turn visits into enquiries. Two pages, each owning its own search intent:
#   /how-it-works/               process and expectations (what we do, what you do, how you know it works)
#   /lead-generation-singapore/  owner page for "lead generation Singapore" / organic enquiries for small businesses
# Facts rule: only what every Page One site already gets. No promise of leads, rankings or AI mentions.
# Run from build.py (exec) after ads_compare.py.

_WA_MSG = "Hi Edwin, I'd like more customer enquiries for my business."


def _lg_buttons(source):
    return f"""
        <div class="cta-row">
          <a class="btn" href="{wa_src(_WA_MSG, source)}" target="_blank" rel="noopener" data-cta="whatsapp_{source.split(',')[0].replace(' ', '_')}">Get more enquiries</a>
          <a class="btn btn-ghost" href="/pricing/">See pricing</a>
        </div>"""


def _lg_cta(title, text, source):
    return f"""    <section class="cta-band">
      <div class="wrap">
        <h2>{title}</h2>
        <p>{text}</p>
        <div class="cta-row center">
          <a class="btn" href="{wa_src(_WA_MSG, source)}" target="_blank" rel="noopener" data-cta="whatsapp_{source.split(',')[0].replace(' ', '_')}_bottom">Get more enquiries</a>
          <a class="btn btn-ghost" href="/signup/">Sign up from S$50/month</a>
        </div>
      </div>
    </section>"""


def _faq_html(faqs):
    return "\n".join(f'        <details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)


# ---------- /how-it-works/ ----------
HIW_URL = "/how-it-works/"
HIW_FAQ = [
    ("How long until my website is live?",
     "Usually within 7 days of receiving your details and photos. Google then needs time to find and trust a new site, often a few weeks to a few months, depending on your trade and area."),
    ("What do I need to do?",
     "Tell Edwin on WhatsApp what you do, where you serve and how customers should reach you, and send a few photos. After that we do the work. Small changes are a WhatsApp message away."),
    ("I already have a website. Do I need a new one?",
     "No. We fix and improve the one you have (its on-page technical SEO, pages and enquiry buttons), or redesign it free if you ask. We won't sell you a replacement you don't need."),
    ("Can you guarantee enquiries or a page one ranking?",
     "No, and nobody honestly can. Google and AI assistants decide what to show. We do the work that gives you the best chance and show you the real numbers from Google Search Console, so you can judge it yourself."),
]

_hiw_steps = [
    ("1", "Build your online presence",
     "Customers can't enquire if there's nothing to find. A clear website is the base everything else stands on.",
     ["No website? We build one on your own domain, included in the plan",
      "Have one? We fix its on-page technical SEO, or redesign it free if you ask",
      "One page for each service you offer, so each one can be found on its own",
      "Hosting, SSL and Google Business Profile setup"]),
    ("2", "Help customers find you",
     "People look in three places now: Google's results, the short answers Google shows first, and AI assistants like ChatGPT.",
     ["SEO: your pages use the words customers search for, on Google Search and Maps",
      "AEO: real customer questions answered plainly, so Google can quote you",
      "GEO: clear business facts, llms.txt and Bing setup, so AI tools can describe you correctly",
      "A technical audit every day with problems fixed, and a new article every 2 days"]),
    ("3", "Turn visitors into enquiries",
     "Being found is only half of it. A visitor needs a clear reason and an easy way to contact you.",
     ["A WhatsApp button on every page, with a pre-filled message",
      "Service pages that answer the usual questions before the customer messages you",
      "WhatsApp taps counted per site, so we can see which pages bring enquiries",
      "Pages improved over time based on what Search Console and the taps show"]),
]
_hiw_cards = "\n".join(
    f'          <div class="card reveal"><p class="pill">Step {n}</p><h3>{t}</h3><p>{why}</p><ul class="ticks">{"".join(f"<li>{x}</li>" for x in items)}</ul></div>'
    for n, t, why, items in _hiw_steps)

page("how-it-works/index.html",
     "How Page One Works: Get Found, Then Get Enquiries",
     "How Page One Singapore works in three steps: build your online presence, help customers find you on Google and AI search, and turn visitors into enquiries.",
     [{"@context": "https://schema.org", "@type": "HowTo", "name": "How Page One Singapore helps a small business get found and get enquiries",
       "step": [{"@type": "HowToStep", "position": int(n), "name": t, "text": why} for n, t, why, _ in _hiw_steps]},
      _faq_ld(HIW_FAQ)],
     hero("How it works", "Three steps, no tech skills needed",
          "How it works: get found, then get enquiries.",
          "Page One helps Singapore small businesses reach more potential customers. Your website is included, we work on Google and AI search every day, "
          "and every page is set up to turn visitors into WhatsApp enquiries. S$50 a month, no setup fee, no contract.",
          buttons=False) .replace('</p>\n      </div>\n    </section>', '</p>' + _lg_buttons("how it works, top") + '\n      </div>\n    </section>', 1) + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">The three steps</p>
        <h2 class="reveal">What we do at each step</h2>
        <div class="cards three plain-cards" style="margin-top:32px">
{_hiw_cards}
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Your part</p>
        <h2 class="reveal">What we need from you</h2>
        <p class="reveal">A short WhatsApp chat: what you do, the areas you serve, your opening hours, how customers should contact you, and a few photos of your work or shop. That's it. Your domain is registered in your name, usually S$15 to S$30 a year, paid by you directly.</p>
        <p class="kicker reveal" style="margin-top:32px">After you go live</p>
        <h2 class="reveal">What happens every month</h2>
        <ul class="ticks reveal">
          <li>A technical audit every day, with problems fixed</li>
          <li>A new article every 2 days, aimed at a real search from your own Search Console data</li>
          <li>Small changes over WhatsApp, such as new prices, photos or opening hours</li>
          <li>Google Search Console connected from day one, so you can see searches and clicks yourself</li>
        </ul>
        <p class="reveal">{PROOF_BOTH} Results vary by business, so we don't guarantee rankings, AI mentions or a number of enquiries.</p>
        <p class="note reveal"><a class="card-link" href="/lead-generation-singapore/">More on getting enquiries →</a> <a class="card-link" href="/seo-aeo-geo-singapore/">SEO, AEO and GEO explained →</a> <a class="card-link" href="/results/">See the results →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">How it works: your questions, answered</h2>
{_faq_html(HIW_FAQ)}
        <p class="note reveal">Starting a new business? See <a class="link" href="/new-business-website/">your first website</a>. More answers in the <a class="link" href="/faq/">full FAQ</a>.</p>
      </div>
    </section>

""" + _lg_cta("Ready to get found and get enquiries?", "Tell Edwin what you do and where. No obligation.", "how it works, bottom"),
     crumb="How it works", updated="2026-10-28")


# ---------- /lead-generation-singapore/ ----------
LG_URL = "/lead-generation-singapore/"
LG_FAQ = [
    ("What is organic lead generation?",
     "Getting customer enquiries from people who find you on their own, through Google Search, Google Maps or AI assistants, instead of paying for every click with ads. It takes longer to start than ads, but the visits don't stop when you stop paying for each one."),
    ("Is this the same as buying leads?",
     "No. We don't sell lists or contact details. Customers find your business, read your pages and choose to message you. Every enquiry comes straight to your own WhatsApp."),
    ("How much does it cost?",
     "S$50 a month on the Get Found plan, for anyone who registers by 31 Dec 2026, with the website included. No setup fee, no contract. Optional SEO Boosts are S$10 per run."),
    ("How many enquiries will I get?",
     "We can't promise a number. It depends on your trade, your area, how many people search for it and your competitors. We count WhatsApp taps on your site and show you the Google Search Console figures, so you can see what is happening."),
]

_lg_rows = [
    ("🔍", "Be found", "Customers search Google, look at Google Maps or ask ChatGPT. Your website, Google Business Profile and articles give them something to find.", "/seo-aeo-geo-singapore/", "SEO, AEO and GEO →"),
    ("📄", "Be understood", "One clear page per service, with prices from, areas served and plain answers to the usual questions, so the right customers stay.", "/website/", "About the website →"),
    ("💬", "Be easy to contact", "A WhatsApp button on every page, with a pre-filled message, so enquiring takes one tap. Taps are counted so we can improve the pages that matter.", HIW_URL, "How it works →"),
]
_lg_cards = "\n".join(
    f'          <a class="card reveal" href="{href}"><div class="emoji" aria-hidden="true">{e}</div><h3>{t}</h3><p>{d}</p><span class="card-link">{link}</span></a>'
    for e, t, d, href, link in _lg_rows)

page("lead-generation-singapore/index.html",
     "Lead Generation Singapore for Small Businesses, S$50/month",
     "Organic lead generation for Singapore small businesses: get found on Google and AI search, then turn visitors into WhatsApp enquiries. From S$50/month.",
     [service("Organic lead generation for small businesses", LG_URL,
              "Website included, SEO for Google Search and Maps, AEO and GEO for AI search, and WhatsApp enquiry buttons on every page, "
              "so Singapore small businesses can be found by customers and receive enquiries directly.", "50"),
      _faq_ld(LG_FAQ)],
     hero("Lead generation", "Organic lead generation",
          "More customer enquiries, without paying for every click.",
          "Page One helps Singapore small businesses get enquiries from people who are already searching: on Google, Google Maps and AI assistants like ChatGPT. "
          "Your website is included, and every page is built to make enquiring easy. S$50 a month, no contract.",
          '<p class="hero-price"><b>S$50</b>/month · <span class="intro-tag">Register by 31 Dec 2026</span> · website included</p>',
          buttons=False).replace('</p>\n      </div>\n    </section>', '</p>' + _lg_buttons("lead generation, top") + '\n      </div>\n    </section>', 1) + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">From search to enquiry</p>
        <h2 class="reveal">Three things a customer needs before they message you</h2>
        <div class="cards three plain-cards" style="margin-top:32px">
{_lg_cards}
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Who it suits</p>
        <h2 class="reveal">Built for businesses customers can't find online yet</h2>
        <p class="reveal">It suits new businesses that need their first website, and owners who are busy on Facebook, Instagram, TikTok, Carousell or Google Maps, often with good reviews, but have no website of their own. A website gives those customers a place to check you out and a one-tap way to enquire. <a class="link" href="/new-business-website/">New business? Start here</a>.</p>
        <p class="kicker reveal" style="margin-top:32px">Organic vs ads</p>
        <h2 class="reveal">Why organic, not only ads</h2>
        <p class="reveal">Google Ads bring visits as long as you keep paying for each click. Organic search takes longer to build, but each page keeps working without a cost per visit. Many businesses use both. See <a class="link" href="/google-ads-vs-seo-vs-ai-blog-tools/">Google Ads vs SEO vs AI blog tools</a>.</p>
        <p class="reveal">{PROOF_BOTH} Results vary by business, so we don't guarantee rankings, AI mentions or a number of enquiries.</p>
        <p class="note reveal"><a class="card-link" href="/get-found/">What the plan includes →</a> <a class="card-link" href="/results/">See the results →</a> <a class="card-link" href="/pricing/">Full pricing →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Lead generation: your questions, answered</h2>
{_faq_html(LG_FAQ)}
        <p class="note reveal">Shopping for SEO? See <a class="link" href="/affordable-seo-services-singapore/">affordable SEO services</a> and <a class="link" href="/seo-services-singapore/">how we compare</a>.</p>
      </div>
    </section>

""" + _lg_cta("Want more enquiries from people already searching?", "Tell Edwin what you do and where. No obligation.", "lead generation, bottom"),
     crumb="Lead generation", updated="2026-10-28")
