# /managed-website-singapore/: the owner page for "fully managed website singapore" and
# "website subscription singapore" searches (EDGE teardown 14 Oct 2026, serp/pageone/2026-10-14-managed-website.md).
# Run from build.py (exec) after affordable.py, so it can use _faq_ld, _price_ld and the showcase data.
# Facts rule: only Page One facts already published on the site or in llms.txt; no other provider's prices;
# AEO and GEO described plainly, with no promise that an AI tool will recommend anyone.

MANAGED_FAQ = [
    ("What does a fully managed website mean?",
     "It means you don't have to touch the technical side at all. Page One builds the website on your own domain, hosts it, keeps it online, secure and fast, runs a technical audit every day and fixes the problems it finds, makes small text and photo changes when you WhatsApp us, and publishes a new article every 2 days, each aimed at a different real search, so Google and AI assistants have reasons to show you. All of it is in the S$50 a month plan."),
    ("What is AEO (answer engine optimisation)?",
     "AEO means setting up your pages so that when someone asks a question, Google's AI answers or ChatGPT can use your page as the answer. In practice that means clear question-and-answer content, FAQ structured data, and your business details written plainly, which we do for every site."),
    ("What is GEO (generative engine optimisation)?",
     "GEO means helping AI tools that write answers, such as ChatGPT, Gemini and Perplexity, find, read and correctly describe your business. We connect your site to Google and Bing, mark up your business details with structured data, publish an llms.txt summary and keep your details the same everywhere. No one can guarantee an AI tool will recommend you, but these steps make it possible."),
    ("What is not included in the S$50?",
     "Your domain name, which is registered in your name and paid to the registrar directly, usually S$15–30 a year. SEO Boosts are optional at S$10 per run: each one checks who is on Google's first page for one of your search terms, improves your page to compete with the one directly above you, and comes with a report of what we found and changed. There is no setup fee and no contract."),
    ("Will the S$50 price go up?",
     "S$50 a month is our price for anyone who registers by 31 Dec 2026. From 2027 the price may rise, depending on demand, and we'll tell you before it changes."),
    ("Who owns the website and the domain?",
     "Your domain is registered in your name, so you always own it. If you cancel, your site stays live until the end of the month you paid for, you keep your domain, and you can buy the site files if you want to host them elsewhere."),
    ("How long until my website is live?",
     "Usually within 7 days of receiving your details and photos. You send them over WhatsApp, and we do the rest."),
    ("Is S$50 a month too cheap to be any good?",
     "The price is low because a set of AI tools we designed does the daily SEO work that used to be billed by the hour, not because steps are skipped. " + PROOF_EG + ", according to Google Search Console, and every client website is live for you to check."),
]

_MANAGED_ITEMS = [
    ("🖥️", "Hosting and speed", "Your website lives on our hosting with a security certificate (the padlock), set up to load fast on phones.", ["Hosting", "SSL"]),
    ("🛡️", "Security and upkeep", "We keep it online, secure and fast, and run a technical audit every day to catch and fix anything that breaks.", ["Technical SEO audit"]),
    ("✏️", "Changes on WhatsApp", "New photo, new price, new opening hours? Send it on WhatsApp and we make the small change for you.", ["Content updates"]),
    ("📝", "SEO articles", "A new article is written for your site every 2 days, each answering a different question your customers search for, so your pages don't compete with each other.", ["SEO content"]),
    ("💬", "AEO: be the answer", "Question-and-answer content and FAQ structured data, so Google's AI answers and ChatGPT can use your page when someone asks.", ["Answer engine optimisation"]),
    ("🤖", "GEO: be described correctly by AI", "Google and Bing connected, business details marked up, an llms.txt summary, so AI tools can find and describe you.", ["Generative engine optimisation", "llms.txt"]),
    ("📍", "Google Maps and Search", "Your Google Business Profile, Google Search Console and Bing set up, so you can show up when people search nearby.", ["Google Business Profile", "Search Console"]),
    ("📊", "Your own Google numbers", "Search Console is connected to your site, so you can see how often you appear on Google and what people searched.", ["Reporting"]),
]

def _terms(terms):
    return "".join('<span class="term">' + x + "</span>" for x in terms)


_managed_cards = "\n".join(
    f'          <div class="card reveal"><div class="emoji" aria-hidden="true">{e}</div><h3>{t}</h3><p>{d}</p>'
    f'<p class="tech"><b>Technical name</b>{_terms(terms)}</p></div>'
    for e, t, d, terms in _MANAGED_ITEMS)

_MANAGED_TABLE = [
    ("Website: a new one built free, or your current one's SEO fixed (or redesigned free if you ask)", "Included", "No setup fee"),
    ("Hosting and security certificate (SSL)", "Included", ""),
    ("Kept online, secure and fast, with a technical audit every day and problems fixed", "Included", ""),
    ("Small text and photo changes on WhatsApp", "Included", ""),
    ("A new SEO article every 2 days", "Included", ""),
    ("Google Business Profile, Search Console and Bing setup", "Included", ""),
    ("AEO and GEO setup: FAQ and business structured data, llms.txt", "Included", ""),
    ("Domain name", "Extra", "About S$15–30 a year, paid to the registrar in your name"),
    ("SEO Boost (first-page competitor analysis for one search term, with a report)", "Optional", "S$10 per run, top up anytime"),
    ("Minimum contract", "None", "Cancel anytime"),
]
_managed_rows = "\n".join(f"              <tr><th>{a}</th><td>{c}</td><td>{b}</td></tr>" for a, b, c in _MANAGED_TABLE)

page("managed-website-singapore/index.html",
     "Fully Managed Website Singapore: S$50/month, All-In",
     "A fully managed website for your Singapore business: design, hosting, security, SEO articles, AEO and GEO, all for S$50/month. No setup fee or contract.",
     [service("Fully managed website", "/managed-website-singapore/",
              "A website built on the client's own domain and fully managed every day: hosting, security, a daily technical audit, updates, SEO articles every 2 days, Google setup and AEO/GEO for AI search.", "50"),
      _faq_ld(MANAGED_FAQ), _price_ld("/managed-website-singapore/")],
     hero("Managed website", "Fully managed website",
          "A fully managed website for S$50 a month.",
          "Page One builds your website on your own domain, then manages everything for S$50 a month: hosting, security, a technical audit every day, a new SEO article every 2 days, and the setup that helps Google, Google Maps and AI assistants like ChatGPT find and quote you. Already have a website? We fix its on-page technical SEO, or redesign it free if you ask. No setup fee, no contract. The only extra is your domain, about S$15–30 a year.",
          '<p class="hero-price"><b>S$50</b>/month · <span class="intro-tag">Register by 31 Dec 2026</span> · everything managed · no setup fee</p>') + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">What's managed</p>
        <h2 class="reveal">Everything we look after, in plain words</h2>
        <p class="section-lead reveal">You run your business. We run the website, and the work that gets it found on Google and in AI answers. <a class="link" href="/seo-aeo-geo-singapore/">SEO, AEO and GEO explained →</a></p>
        <div class="cards three plain-cards" style="margin-top:32px">
{_managed_cards}
        </div>
      </div>
    </section>

    <section class="section alt" id="price">
      <div class="wrap">
        <p class="kicker reveal">The price</p>
        <h2 class="reveal">What you get for S$50, and what's extra</h2>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th>Item</th><th>Notes</th><th>S$50 a month</th></tr></thead>
            <tbody>
{_managed_rows}
            </tbody>
          </table>
        </div>
        <p class="note reveal">S$50 a month is our price for anyone who registers by 31 Dec 2026. From 2027 the price may rise, depending on demand, and we'll tell you before it changes. Year one all in is about S$615–630: 12 months at S$50 plus your domain. <a class="link" href="/pricing/">Full pricing →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">How it works</p>
        <h2 class="reveal">Three steps, then we take it from there</h2>
        <ol class="steps" style="margin-top:56px">
          <li class="reveal"><span>1</span><h3>Tell us about your business</h3><p>Your services, area, hours and a few photos, over WhatsApp. No forms to fill in, no tech skills needed.</p></li>
          <li class="reveal"><span>2</span><h3>We build and set it up</h3><p>Your website on your own domain, plus Google Business Profile, Search Console, Bing and the AI search setup.</p></li>
          <li class="reveal"><span>3</span><h3>We manage it every day</h3><p>Usually live within 7 days. After that: hosting, upkeep, a new article every 2 days, a technical audit every day and changes when you ask.</p></li>
        </ol>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Real results</p>
        <h2 class="reveal">Cheap can still be good. Here are the numbers.</h2>
        <p class="section-lead reveal">The same managed system runs every website we look after. Last 28 days ({WINDOW}), from Google Search Console.</p>
        <div class="reveal">""" + kpis([
            ("Edwin Garage: clicks from Google", EG["clicks"], f"Up from {EG['prev_clicks']} · average position {EG['pos']}"),
            ("Cleanic Detailing: clicks from Google", CL["clicks"], f"Up from {CL['prev_clicks']} · average position {CL['pos']}"),
            ("Websites live and managed", str(len(SC["clients"])), "Each on the business's own domain"),
        ]) + """</div>
        <div class="cards three site-cards" style="margin-top:32px">
""" + site_cards_html() + """
        </div>
        <p class="note reveal"><a class="card-link" href="/clients/">See every client website and its numbers →</a> <a class="card-link" href="/results/">Read the case studies →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Fully managed website: your questions, answered</h2>
""" + "\n".join(f'        <details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in MANAGED_FAQ) + """
        <p class="note reveal">Just starting a business? See <a class="link" href="/new-business-website/">the new business website setup</a>. Comparing on price? See <a class="link" href="/cheapest-website-singapore/">a website without the lump sum</a>.</p>
      </div>
    </section>

""" + cta("Want your website fully managed?", "Sign up at S$50 a month, or chat with Edwin on WhatsApp first. No obligation."),
     crumb="Managed website", updated="2026-10-19")
