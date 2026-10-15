# "Cheapest SEO" and "cheapest website" pages: answer those searches honestly and make the case that low-cost SEO can be good SEO.
# Run from build.py (exec) after industries.py, so it uses build.py's helpers and PROOF_GARAGE / PROOF_CLEANIC.
# Content rules: the search phrase is the topic, never a claim. We don't say we are the cheapest or the first,
# don't quote other providers' prices, don't promise rankings, and only say what the system really does.


def _faq_html(faqs):
    return "".join(f"        <details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>\n" for q, a in faqs)


def _faq_ld(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def _cards(items):
    return "".join(f'<div class="card reveal"><h3>{t}</h3><p>{p}</p></div>' for t, p in items)


def _myths(rows, left="What people say", right="What's true now"):
    trs = "".join(f"<tr><th>{m}</th><td>{t}</td></tr>" for m, t in rows)
    return f"""<div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th>{left}</th><th>{right}</th></tr></thead>
            <tbody>{trs}</tbody>
          </table>
        </div>"""


PRICE_GLANCE = """    <section class="section alt" id="price">
      <div class="wrap">
        <p class="kicker reveal">Price at a glance</p>
        <h2 class="reveal">SEO and a website in Singapore from S$20 a month</h2>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th>Page One Singapore</th><th>Price</th><th>What you get</th></tr></thead>
            <tbody>
              <tr><th>Get Found plan</th><td><b>S$20 a month</b> (introductory price)</td><td>Your website (or an SEO landing page), Google, Google Maps and ChatGPT setup, regular new articles, a technical audit every month, hosting and security</td></tr>
              <tr><th>SEO Boost (optional)</th><td><b>S$10 each</b></td><td>Accelerated growth: more articles aimed at new keywords, extra SEO fixes and a before/after report</td></tr>
              <tr><th>Setup fee</th><td><b>S$0</b></td><td>No setup fee and no lump sum</td></tr>
              <tr><th>Contract</th><td><b>None</b></td><td>Monthly, cancel anytime</td></tr>
            </tbody>
          </table>
        </div>
        <p class="note reveal">Your domain is registered in your name and paid by you directly, usually S$15–30 a year. <a class="link" href="/pricing/">Full pricing →</a></p>
      </div>
    </section>
"""


def _price_ld(url):
    return {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Page One Singapore prices", "url": SITE + url,
            "itemListElement": [
                {"@type": "Offer", "name": "Get Found: website or SEO landing page, Google and AI search setup, regular articles, monthly audit",
                 "price": "20", "priceCurrency": "SGD", "url": SITE + "/get-found/", "seller": PROVIDER,
                 "priceSpecification": {"@type": "UnitPriceSpecification", "price": "20", "priceCurrency": "SGD", "unitCode": "MON"}},
                {"@type": "Offer", "name": "SEO Boost (optional): accelerated growth with more articles for new keywords",
                 "price": "10", "priceCurrency": "SGD", "url": SITE + "/seo-boost/", "seller": PROVIDER}]}


# ---------- Cheapest SEO in Singapore ----------
CHEAP_SEO_FAQ = [
    ("Is Page One the cheapest SEO in Singapore?",
     "We can't check every provider's prices, so we won't claim that. What we can tell you is our price: the Get Found plan is S$20 a month at an introductory price, with no setup fee and no contract. Optional SEO Boosts are S$10 each."),
    ("How much does SEO cost in Singapore?",
     "It depends on the provider and on how much of the work is done by hand. When Edwin started, small businesses like his own workshop were being quoted hundreds of dollars a month for SEO they couldn't see or measure. With Page One, the Get Found plan is S$20 a month (introductory price) and includes your website or landing page, Google, Maps and ChatGPT setup, regular new articles and a monthly technical audit. Optional SEO Boosts are S$10 each. No setup fee, no contract."),
    ("What's the difference between the S$20 plan and an SEO Boost?",
     "The S$20 plan is the steady base: your site, the Google and AI search setup, regular new articles and a monthly audit. An SEO Boost (S$10) is for accelerated growth: more articles aimed at new keywords, so you show up for more searches sooner, plus extra fixes and a before/after report."),
    ("Is S$20 a month too cheap for SEO to work?",
     "The price is low because the daily work is automated, not because steps are skipped. Edwin Garage, where the system was first built, got " + EG["clicks"] + " clicks from Google in the 28 days to " + THROUGH + " with an average position of " + EG["pos"] + ", according to Google Search Console. Results vary by business, so we don't guarantee rankings."),
    ("What's the catch?",
     "There's no setup fee or contract, and you can cancel anytime. S$20 is an introductory price: it goes up once we reach our early-client target, so it's worth grabbing now. Any new price will stay close to S$20. Your domain is registered in your name and paid by you directly, usually S$15–30 a year."),
    ('Is S$20 a month a gimmick price?', "No. S$20 isn't a teaser to upsell you later, and it isn't budget SEO with steps skipped. It's a baseline for what SEO costs now that AI does the daily work that used to be billed by the hour. The same system runs every website we manage, and it's proven on real businesses: " + PROOF_EG + ", according to Google Search Console. No setup fee, no contract, so you can judge it for yourself."),
    ("How can I check that S$20 SEO really works?",
     "Look at the evidence yourself. Our Google Search Console results for Edwin Garage and Cleanic Detailing are published on our results page with dates. The websites we run are live: " + names_list(LIVE_NAMES) + ", " + LIVE_COUNT_WORD + " businesses in all (see them on our client page). Run any of them through our free website check. Page One Singapore is a project of Snap Commercial Pte. Ltd. (UEN 202209904W), a registered Singapore company."),
    ("Does Google penalise content written with AI?",
     "Google's guidance is that it rewards helpful, accurate content, however it's produced, and acts against content mass-produced only to game rankings. We use AI to write useful answers to real customer questions, based on facts about your business and real Search Console data, not to churn out filler."),
    ("Is anyone actually looking after my site, or is it all robots?",
     "Both. Edwin designs the strategy and the system and reviews the results. The system does the repetitive work every day and flags anything that breaks, so it gets fixed."),
    ("Why monthly and not a one-off fee?",
     "Because SEO never finishes. Google keeps re-checking sites, competitors keep changing theirs, and customers keep asking new questions. A monthly subscription matches the work, and you don't pay a big sum upfront."),
]

page("cheapest-seo-singapore/index.html",
     "Cheapest SEO in Singapore? Why Cheap SEO Can Work | Page One",
     "Looking for the cheapest SEO in Singapore? AI now does the daily SEO work, so good SEO costs less. Page One: S$20/month, no setup fee, no contract.",
     [service("Affordable SEO subscription for Singapore businesses", "/cheapest-seo-singapore/",
              "Low-cost, automated SEO for Singapore small businesses: Google, Google Maps and AI search visibility for S$20 a month, no setup fee, no contract.", "20"),
      _faq_ld(CHEAP_SEO_FAQ), _price_ld("/cheapest-seo-singapore/")],
     hero("Cheap SEO that works", "Looking for the cheapest SEO in Singapore?",
          "Cheap SEO doesn't have to mean bad SEO.",
          "SEO used to be expensive because it took a lot of people's time. AI now does most of that daily work. With the right strategy, structure and design, good SEO, including regular new articles, can cost S$20 a month.",
          '<p class="hero-price"><b>S$20</b>/month · <span class="intro-tag">Introductory price</span> · no setup fee · no contract</p>') + "\n\n" + PRICE_GLANCE + f"""

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Why SEO used to cost so much</p>
        <h2 class="reveal">You were paying for hours, not results</h2>
        <p class="section-lead reveal">Doing SEO properly is a lot of small jobs, repeated every week: checking pages for problems, fixing them, writing new content, updating business listings, telling Google about changes and reporting what happened. Done by hand, every one of those jobs is someone's billable time.</p>
        <p class="section-lead reveal">When Edwin started, small businesses like his own car workshop were being quoted hundreds of dollars a month for SEO they couldn't see or measure.</p>
        <p class="section-lead reveal">That's why SEO has usually been priced like a professional service, with a big setup fee or a high monthly retainer. It wasn't that anyone was overcharging. It was simply the only way to do it.</p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">What changed</p>
        <h2 class="reveal">AI does the repetitive work. A good system does the rest.</h2>
        <p class="section-lead reveal">Edwin built Page One as a system: he designs the strategy, the site structure and the design once, and the daily work runs automatically. When the biggest cost, people's time, is mostly automated, the price can come down a long way. That's how the Get Found plan costs S$20 a month.</p>
        <div class="cards three" style="margin-top:32px">{_cards([
            ("Faster", "A full technical check of a website takes seconds, not an afternoon. Problems are found the day they appear, not at next month's review."),
            ("Every day", "The system runs on a schedule every day, weekends and public holidays included. It doesn't wait for office hours or someone to come back from leave."),
            ("Consistent", "The same checks run the same way every time. Nothing gets skipped because it was a busy week."),
            ("Data, not guesswork", "New content is picked from the searches Google already shows your site for, using your Search Console data."),
            ("Built for AI search too", "Structured data, an llms.txt summary and Bing setup, so assistants like ChatGPT can read and cite your business."),
            ("A person in charge", "Edwin sets the strategy and reviews the results. Automation does the legwork; it doesn't replace judgement."),
        ])}</div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Myths about cheap SEO</p>
        <h2 class="reveal">"Cheap is never good." Is that still true?</h2>
        {_myths([
            ("Cheap SEO is low-quality SEO.", "Quality comes from the strategy and the system, not from the number of hours billed. When the routine work is automated, a low price and good work can go together."),
            ("Good SEO needs a big upfront fee.", "SEO is ongoing work, so a monthly subscription fits it better. Get Found has no setup fee and no lump sum."),
            ("Build a website once and you're done.", "A site that never changes gives Google little reason to come back. Regular, useful updates keep your site fresh and visited."),
            ("Cheap SEO uses risky shortcuts.", "We follow Google's guidelines: no bought links, no fake reviews, no keyword stuffing. Just a well-built site with helpful content."),
            ("Automated means nobody is watching.", "Edwin designs and oversees the system. The automation flags problems so they get fixed, instead of waiting for someone to notice."),
        ])}
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Why SEO is never one-and-done</p>
        <h2 class="reveal">Search engines and customers both want what's current</h2>
        <p class="section-lead reveal">Think about it as a customer: when you search, you want the latest information, not a page nobody has touched in three years. Search engines think the same way. Google keeps re-visiting websites to look for changes, and for many searches it prefers pages that are up to date.</p>
        <p class="section-lead reveal">A website that's built once and left alone slowly falls behind sites that keep adding useful content and fixing problems. That's why SEO works best as a small, continuous effort, and why doing it by hand gets expensive. Automating it is what makes continuous SEO affordable.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">A baseline, not a gimmick</p>
        <h2 class="reveal">S$20 isn't budget SEO. It's what SEO costs now.</h2>
        <p class="section-lead reveal">A low price can look too good to be true, so here's the honest answer. S$20 isn't a teaser to upsell you later, and it isn't SEO with steps skipped. It's the new baseline: when AI does the daily work that used to be billed by the hour, the cost of doing SEO properly falls, and the price can fall with it.</p>
        <ul class="ticks reveal">
          <li><b>The same system for everyone.</b> Every website we manage runs on it, including Edwin's own workshop.</li>
          <li><b>Proven, with dates and sources.</b> Real Google Search Console results, published on our <a class="link" href="/results/">results page</a>.</li>
          <li><b>Checkable.</b> The {LIVE_COUNT_WORD} websites we run are live. Run any of them through our <a class="link" href="/free-website-check/">free website check</a>, or follow our <a class="link" href="/is-page-one-singapore-legit/">verification checklist</a>.</li>
          <li><b>A registered company.</b> Page One Singapore is a project of Snap Commercial Pte. Ltd. (UEN 202209904W).</li>
          <li><b>An introductory price.</b> S$20 goes up once we reach our early-client target, so grab it now. Any new price will stay close to S$20, so it stays affordable.</li>
        </ul>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Proof, not promises</p>
        <h2 class="reveal">The same system, on real Singapore businesses</h2>
        {PROOF_GARAGE}
        <div style="margin-top:28px">{PROOF_CLEANIC}</div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">What S$20 a month gets you</p>
        <h2 class="reveal">The Get Found plan</h2>
        {GET_FOUND}
        <div class="price-strip reveal">
          <p><b>S$20/month</b> · introductory price · no setup fee · cancel anytime · optional SEO Boosts S$10 each</p>
          <a class="card-link" href="/pricing/">See pricing →</a>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Cheap SEO: your questions, answered</h2>
        <div style="margin-top:24px">
{_faq_html(CHEAP_SEO_FAQ)}        </div>
        <p class="note reveal">Need a website too? <a class="link" href="/cheapest-website-singapore/">A website without the lump sum →</a> · Comparing agencies or an in-house hire? <a class="link" href="/seo-services-singapore/">SEO services compared →</a> · <a class="link" href="/ai-seo-vs-traditional-seo/">AI SEO vs traditional SEO →</a> · <a class="link" href="/is-page-one-singapore-legit/">Is Page One legit? Check us yourself →</a></p>
      </div>
    </section>

""" + cta("See what S$20 a month can do for you", "Check your website free in under a minute, or chat with Edwin on WhatsApp. No obligation."),
     crumb="Cheap SEO that works", updated="2026-10-13")


# ---------- Cheapest website maker in Singapore ----------
CHEAP_SITE_FAQ = [
    ("Is Page One the cheapest website maker in Singapore?",
     "We can't check every provider's prices, so we won't claim that. Our price is S$20 a month on the Get Found plan (introductory price), which covers building, hosting and looking after your website. There's no setup fee and no contract."),
    ("Why a monthly fee instead of paying once?",
     "A website isn't finished on launch day. It needs hosting, security updates, fixes, new content and Google setup to keep being found. A small monthly fee covers all of that, and you don't pay a big sum upfront."),
    ("Do I own my website and domain?",
     "Your domain is registered in your name, so you always own it. If you cancel, your site stays live until the end of the month you paid for, you keep your domain, and you can buy the site files if you want to host them elsewhere."),
    ("How long does it take?",
     "Usually within 7 days of receiving your details and photos. If you already have an old website, just send us the address: we read your services, contact details and photos from it and show you a preview."),
    ("Is a cheap website good enough for Google?",
     "What Google cares about is whether the site is fast, secure, clear about what you do and where, and useful to customers, not how much it cost. Every site we build has a page per service, your business details labelled for Google and AI assistants, and a WhatsApp button."),
    ("Do I need any technical skills?",
     "No. You tell us about your business on WhatsApp and send a few photos. We handle the domain setup, design, hosting, Google setup and updates."),
]

page("cheapest-website-singapore/index.html",
     "Cheapest Website Maker in Singapore? From S$20/month",
     "Looking for the cheapest way to get a website in Singapore? Page One builds, hosts and updates it for S$20/month. No lump sum, no setup fee, no contract.",
     [service("Website built and managed for Singapore businesses", "/cheapest-website-singapore/",
              "A website built, hosted and kept up to date for a monthly subscription instead of a lump sum: S$20 a month, no setup fee, no contract.", "20"),
      _faq_ld(CHEAP_SITE_FAQ), _price_ld("/cheapest-website-singapore/")],
     hero("A website without the lump sum", "Looking for the cheapest website maker in Singapore?",
          "A website without the lump sum.",
          "Most websites are a big one-off payment, then left alone until they're out of date. Page One builds your website, hosts it and keeps it updated for S$20 a month, so it keeps working for you.",
          '<p class="hero-price"><b>S$20</b>/month · <span class="intro-tag">Introductory price</span> · no setup fee · no contract</p>') + "\n\n" + PRICE_GLANCE + f"""

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">The old way</p>
        <h2 class="reveal">Pay a lump sum, then watch it go stale</h2>
        <p class="section-lead reveal">The usual way to get a website is to pay a designer upfront, launch it, and then leave it. Nobody updates the content, nobody checks it still works, and nobody tells Google about changes. A year or two later it looks dated and doesn't show up when customers search.</p>
        <p class="section-lead reveal">The problem isn't the design. It's that a website was treated as a one-off purchase, when it really needs looking after to keep bringing in customers.</p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">The new way</p>
        <h2 class="reveal">Your website as an ongoing service, run by automation</h2>
        <p class="section-lead reveal">Building and maintaining a website used to take a lot of manual work. Page One uses AI and automation for the repetitive parts, so we can build your site and keep looking after it for a small monthly fee instead of a big upfront one.</p>
        <div class="cards three" style="margin-top:32px">{_cards([
            ("Built from what you already have", "Send us your old website address, or just your details on WhatsApp. We pull in your services, contact details and photos, and show you a preview first."),
            ("Kept fresh", "Regular new articles are included in the S$20 plan, so search engines have a reason to keep coming back. Want to grow faster? Add SEO Boosts."),
            ("Checked automatically", "The system checks your site on a schedule, every day including weekends, and problems get fixed instead of waiting to be noticed."),
            ("Ready for Google and AI", "A page for each service, your business details labelled for Google, Bing and AI assistants, and a sitemap so nothing gets missed."),
            ("Fast and secure", "Hosting, the padlock (HTTPS) and a one-tap WhatsApp button, all included."),
            ("No lump sum", "S$20 a month at an introductory price. No setup fee, no contract, cancel anytime. Your domain is in your name."),
        ])}</div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Your options</p>
        <h2 class="reveal">Lump sum, DIY, or a monthly service?</h2>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th></th><th>DIY website builder</th><th>Web designer (one-off)</th><th>Page One</th></tr></thead>
            <tbody>
              <tr><th>Who builds it</th><td>You</td><td>The designer</td><td>We do</td></tr>
              <tr><th>How you pay</th><td>Builder plan plus your time</td><td>Usually an upfront fee</td><td>S$20 a month, no setup fee</td></tr>
              <tr><th>Updates after launch</th><td>You do them</td><td>Often charged separately</td><td>Included, done for you</td></tr>
              <tr><th>Google, Maps and AI setup</th><td>Up to you</td><td>Depends on the designer</td><td>Included</td></tr>
              <tr><th>Keeps getting checked</th><td>Up to you</td><td>Usually not</td><td>Yes, automatically</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Websites we built and run</p>
        <h2 class="reveal">See them for yourself</h2>
        <p class="section-lead reveal">These Singapore businesses use the same system you get: """ + names_list([f'<a class="link" href="{c["url"]}" target="_blank" rel="noopener">{c["name"]}</a>' for c in SC["clients"]]) + f""". <a class="link" href="/clients/">See them all →</a> <a class="link" href="/website/">More about our websites →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Low-cost websites: your questions, answered</h2>
        <div style="margin-top:24px">
{_faq_html(CHEAP_SITE_FAQ)}        </div>
        <p class="note reveal">Why can good SEO cost so little now? <a class="link" href="/cheapest-seo-singapore/">Cheap SEO doesn't have to mean bad SEO →</a></p>
      </div>
    </section>

""" + cta("Get your website without the lump sum", "Chat with Edwin on WhatsApp and send your old website address or your details. No obligation."),
     crumb="A website without the lump sum", updated="2026-10-15")


# ---------- New business website ----------
# For people starting a business who need their first website. Compares doing it yourself (no market prices quoted)
# with Page One's all-in plan. Only Page One's own prices appear as numbers.
NEW_BIZ_FAQ = [
    ("How much does a website for a new business cost with Page One?",
     "S$20 a month on the Get Found plan (introductory price). That covers building the website, hosting it, keeping it secure, writing the content with you, setting it up on Google and Google Maps, regular new articles and looking after it every month. No setup fee and no contract. The only separate cost is your domain name, registered in your name, usually S$15–30 a year."),
    ("What would I need to do it myself?",
     "Usually: a domain name, a hosting plan or a website builder subscription, a design or template, the words and photos for every page, the security certificate, Google Business Profile, Google Search Console and Bing set up, and someone to keep it updated. Each has its own bill or takes your time. With Page One, all of that except the domain is in the S$20 a month."),
    ("I've just registered my business. How soon can I have a website?",
     "Usually within 7 days of receiving your details and a few photos on WhatsApp. If you don't have photos yet, we can start with what you have and add more later."),
    ("I don't have a logo or photos yet. Can I still start?",
     "Yes. We can start with a clean text logo and a simple layout, and add your logo and photos when you have them."),
    ("Do I own the website and domain?",
     "Your domain is registered in your name, so you always own it. If you cancel, your site stays live until the end of the month you paid for, you keep your domain, and you can buy the site files if you want to host them elsewhere."),
    ("Is S$20 a month just a starter price that jumps later?",
     "S$20 is an introductory price. It goes up once we reach our early-client target, so it's worth grabbing now, and any new price will stay close to S$20 so it stays affordable."),
    ("What does a new business website cost in the first year with Page One?",
     "About S$255–270 in total: 12 months at S$20 (S$240) plus your domain name, which is usually S$15–30 a year and paid by you directly. That includes building the website, hosting, the security certificate, Google Business Profile, Search Console and Bing setup, regular new articles, a monthly technical audit and small changes. There is no setup fee."),
    ("Can I get a .com.sg domain before my company is registered?",
     "A .com.sg domain is for businesses registered, or in the process of registering, with ACRA or another recognised Singapore body, under SGNIC's rules. A .com or plain .sg domain has no such requirement, so you can start with one of those and add .com.sg once your registration is done."),
]

page("new-business-website/index.html",
     "Website for a New Business in Singapore: S$20/month",
     "Starting a business in Singapore? Website, hosting, content and Google listing for S$20/month, about S$255–270 for year one. No setup fee, live in 7 days.",
     [service("Website for new businesses in Singapore", "/new-business-website/",
              "A website for a new Singapore business, set up and managed: hosting, content, Google and Google Maps setup and monthly updates for S$20 a month.", "20"),
      _faq_ld(NEW_BIZ_FAQ), _price_ld("/new-business-website/")],
     hero("New business website", "Starting a business in Singapore?",
          "Your new business website, done for you.",
          "You've got a business to run. Page One sets up everything you need to be found online: the website, the hosting, the content and your Google listing. One plan, S$20 a month, and Edwin looks after it from then on.",
          '<p class="hero-price"><b>S$20</b>/month · <span class="intro-tag">Introductory price</span> · hosting included · no setup fee</p>') + "\n\n" + PRICE_GLANCE + f"""

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Start the right way</p>
        <h2 class="reveal">What a new business needs to be found online</h2>
        <p class="section-lead reveal">Most new owners know they need a website, but not where to start: which builder, which hosting, what to write, how to get on Google. It's easy to spend weeks on it, or to end up with a site nobody finds. Here's what matters, in order:</p>
        <ol class="steps" style="margin-top:56px">
          <li class="reveal"><span>1</span><h3>Your own domain</h3><p>yourbusiness.com.sg or .com, registered in your name. It's yours for as long as you keep it.</p></li>
          <li class="reveal"><span>2</span><h3>A website built to be found</h3><p>A page for each service, your area, opening hours and a one-tap WhatsApp button, fast on phones and secure.</p></li>
          <li class="reveal"><span>3</span><h3>Google and Maps from day one</h3><p>Google Business Profile, Search Console and Bing set up, so you can start showing up when people search nearby.</p></li>
        </ol>
        <p class="note reveal">With Page One, steps 2 and 3 are done for you, and we help you with step 1. After launch, it's <a class="link" href="/managed-website-singapore/">fully managed</a>: hosting, upkeep, SEO articles and AI search setup.</p>
      </div>
    </section>

    <section class="section alt" id="launch-checklist">
      <div class="wrap narrow">
        <p class="kicker reveal">New business launch checklist</p>
        <h2 class="reveal">Your first five steps online</h2>
        <p class="section-lead reveal">Work through these in order. The ones marked <b>we do this</b> are part of the S$20 plan.</p>
        <ul class="ticks reveal">
          <li><b>ACRA registration done.</b> Your business is registered through Bizfile and you have your UEN. Use the exact registered or trading name everywhere: website, Google listing and social pages.</li>
          <li><b>Domain registered in your name.</b> yourbusiness.com.sg or .com, usually S$15–30 a year, paid by you directly so you always own it. <span class="term">We help you set it up</span></li>
          <li><b>Google Business Profile.</b> Your listing on Google Maps with your category, hours, photos and area. Home-based? You can hide your address and show the area you serve. <span class="term">We do this</span></li>
          <li><b>WhatsApp button.</b> One tap from any page to message you, on the number you'll use for the business. <span class="term">We do this</span></li>
          <li><b>Your first pages.</b> A homepage that says what you do and where, a page for each main service or product, prices or how you quote, an about page and a contact page with your hours. Then Google Search Console and Bing connected so you can see who finds you. <span class="term">We do this</span></li>
        </ul>
        <p class="note reveal">Opening a <a class="link" href="/industries/home-bakery/">home bakery</a>, <a class="link" href="/industries/cafe/">cafe</a>, <a class="link" href="/industries/nail-lash-studio/">nail or lash studio</a> or <a class="link" href="/industries/fitness-studio/">fitness studio</a>? See what to set up for your type of business.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Do it yourself, or let Edwin do it</p>
        <h2 class="reveal">Everything you'd otherwise sort out yourself</h2>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th></th><th>Doing it yourself</th><th>Page One (S$20 a month)</th></tr></thead>
            <tbody>
              <tr><th>Hosting / server</th><td>Choose a plan and pay for it yourself</td><td>Included</td></tr>
              <tr><th>Website builder or developer</th><td>A subscription, or a developer's fee</td><td>Included: we build it</td></tr>
              <tr><th>Design and page content</th><td>Your evenings and weekends</td><td>Included: we write it with you</td></tr>
              <tr><th>Security (the padlock)</th><td>Set up and renew it yourself</td><td>Included</td></tr>
              <tr><th>Google, Maps and Bing setup</th><td>Learn how, then do it</td><td>Included</td></tr>
              <tr><th>New articles and updates</th><td>Whenever you find time</td><td>Included, regularly</td></tr>
              <tr><th>Domain name</th><td>Yours to buy</td><td>Yours to buy (usually S$15–30 a year), we set it up</td></tr>
            </tbody>
          </table>
        </div>
        <p class="note reveal">S$20 a month is S$240 a year for the website, hosting, content, Google setup and monthly care. Add up what the do-it-yourself column would cost you, including your own hours, and compare.</p>
      </div>
    </section>

    <section class="section alt" id="first-year-cost">
      <div class="wrap narrow">
        <p class="kicker reveal">The real first-year cost</p>
        <h2 class="reveal">What your website costs in year one, all in</h2>
        <p class="section-lead reveal">Most website price guides quote the build and stop there. A new business pays for the whole first year: the build, the domain, hosting, the security certificate, changes after launch and getting set up on Google. Here is that whole year with Page One, using only our published prices.</p>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th>First-year item</th><th>With Page One</th></tr></thead>
            <tbody>
              <tr><th>Building the website</th><td>S$0 setup fee</td></tr>
              <tr><th>Hosting and security (the padlock)</th><td>Included in S$20 a month</td></tr>
              <tr><th>Google Business Profile, Search Console and Bing setup</th><td>Included</td></tr>
              <tr><th>Regular new articles and a technical audit every month</th><td>Included</td></tr>
              <tr><th>Small text and photo changes after launch</th><td>Included: WhatsApp Edwin</td></tr>
              <tr><th>Domain name (in your name, paid by you)</th><td>Usually S$15–30 a year</td></tr>
              <tr><th><b>Total for the first 12 months</b></th><td><b>About S$255–270</b> (12 × S$20, plus your domain)</td></tr>
            </tbody>
          </table>
        </div>
        <p class="note reveal">S$20 is an introductory price. If it goes up later, any new price will stay close to S$20. Year two costs the same as year one: there is no separate renewal bill for hosting or maintenance.</p>
        <h3 class="reveal" style="margin-top:40px">Two Singapore rules to know before you launch</h3>
        <ul class="ticks reveal">
          <li><b>A .com.sg address needs a registered business.</b> SGNIC, which runs .sg domains, only gives .com.sg to businesses registered (or registering) with ACRA or another recognised Singapore body. A plain .sg or .com has no such rule. If you're still registering, you can start with .com and add .com.sg later.</li>
          <li><b>Your contact form collects personal data.</b> Under the PDPA, if your website asks for names, phone numbers or emails, tell people what you'll use them for. A short privacy notice and a line next to the form usually does it. See the <a class="link" href="https://www.pdpc.gov.sg/organisations/resources/guidance-by-topic/guide-to-notification" target="_blank" rel="noopener">PDPC guide to notification</a>.</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Why it's only S$20</p>
        <h2 class="reveal">One-stop, because the busywork is automated</h2>
        <p class="section-lead reveal">Edwin built a system where AI does the repetitive work: checking the site, writing helpful articles, telling Google about changes. That's how one person can set up and look after your whole online presence for S$20 a month, so you can spend your time on your customers. <a class="link" href="/cheapest-seo-singapore/">Why cheap doesn't mean bad →</a></p>
        <ol class="steps" style="margin-top:56px">
          <li class="reveal"><span>1</span><h3>Chat with Edwin</h3><p>On WhatsApp: tell us what you do and where. No obligation.</p></li>
          <li class="reveal"><span>2</span><h3>Send details and photos</h3><p>We help register your domain in your name and build your website.</p></li>
          <li class="reveal"><span>3</span><h3>Live within 7 days</h3><p>Connected to Google, Maps and Bing, and looked after every month after that.</p></li>
        </ol>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">New business website: your questions, answered</h2>
        <div style="margin-top:24px">
{_faq_html(NEW_BIZ_FAQ)}        </div>
        <p class="note reveal">Comparing this with an SEO agency or hiring a marketing executive? <a class="link" href="/seo-services-singapore/">See how S$20 a month compares →</a></p>
      </div>
    </section>

""" + cta("Starting a business? Let's get you online.", "Chat with Edwin on WhatsApp: tell us what you do and where. Live within 7 days, S$20 a month."),
     crumb="New business website", updated="2026-10-13")


# ---------- SEO services in Singapore: agency vs in-house vs Page One ----------
# For people actively shopping for SEO or about to hire an SEO / digital marketing executive. Market figures are
# general Singapore ranges, labelled as typical ranges and never as any provider's quote. CPF 17% is the employer
# rate for Singapore citizens and PRs aged 55 and below. The salary example is an illustration, not a benchmark.
SEO_SERVICES_FAQ = [
    ("How much do SEO services cost in Singapore?",
     "It varies a lot by provider and scope. As a general guide, small business SEO retainers from agencies are often somewhere around S$500 to S$3,000 or more a month, sometimes with a setup or audit fee. Hiring an in-house SEO or digital marketing executive typically means a salary of roughly S$3,000 to S$5,000 a month plus employer CPF and tools. These are typical ranges, not quotes. Page One's Get Found plan is S$20 a month (introductory price), with optional SEO Boosts at S$10 each, no setup fee and no contract."),
    ("Is an SEO agency better than Page One?",
     "It depends on what you need. An agency can make sense if you have a larger budget, compete for national searches, sell in several markets or want ads and SEO handled together. Page One is built for new and small local businesses that want the essentials done properly at a low monthly cost: a website, Google and Google Maps setup, AI search setup, regular articles and a monthly technical audit."),
    ("Should I hire an in-house SEO executive or outsource?",
     "Hire if you have enough marketing work to keep a full-time person busy, for example social media, ads, content and events as well as SEO. If what you mainly need is for your website to be found on Google and Google Maps, outsourcing the SEO groundwork usually costs far less, and you can still hire later when there's more to do."),
    ("How much does it cost to hire an SEO or digital marketing executive in Singapore?",
     "Salaries for these roles typically range from around S$3,000 to S$5,000 a month depending on experience, as a general guide. On top of salary, employers pay CPF of 17% for Singapore citizens and PRs aged 55 and below, plus paid SEO tools, leave cover, training and your own time managing the role. For example, a S$3,500 salary plus 17% CPF is about S$4,095 a month before tools or bonus."),
    ("What does Page One not do?",
     "We don't run paid ads, manage your social media accounts, or buy links. We don't promise rankings, because no honest provider can. We focus on organic (unpaid) visibility on Google, Google Maps and AI assistants like ChatGPT for local small businesses."),
    ("Can Page One work alongside my marketing executive?",
     "Yes. We look after the website and the Google and AI search groundwork, and your executive can send us updates on WhatsApp while they focus on social media, ads and customers."),
    ("Do you guarantee page one on Google?",
     "No. Google decides rankings, so no honest provider can guarantee them. Be careful of anyone who does. We document the work instead, and you can see your own numbers in Google Search Console."),
    ("Is there a contract or setup fee?",
     "No. The Get Found plan is S$20 a month at an introductory price, paid monthly in advance, with no setup fee and no minimum contract. Cancel anytime by WhatsApp."),
    ("How do I check that an SEO company in Singapore is legitimate?",
     "Look the company up on ACRA's Bizfile by name or UEN, ask for Google Search Console numbers with the date range shown for a website you can visit, open the client websites they name, and read the minimum term in the contract. Be careful with headline promises like \"Rank #1\" that their own small print says no one can guarantee. Page One's company details, client websites and dated Search Console results are all published so you can check them."),
]

page("seo-services-singapore/index.html",
     "SEO Services Singapore: Agency vs In-house vs S$20/month",
     "Comparing SEO services in Singapore? Agency retainers, hiring an SEO executive or Page One at S$20/month: typical costs, what you get and when each makes sense.",
     [service("SEO services for Singapore small businesses", "/seo-services-singapore/",
              "Done-for-you SEO for Singapore small businesses: a website or SEO landing page, Google, Google Maps and AI search setup, regular articles and a monthly technical audit for S$20 a month.", "20"),
      _faq_ld(SEO_SERVICES_FAQ), _price_ld("/seo-services-singapore/")],
     hero("SEO services compared", "Shopping for SEO in Singapore?",
          "SEO services in Singapore: agency, in-house hire, or S$20 a month?",
          "If you're comparing SEO companies, or thinking of hiring someone to do it, here's an honest side-by-side: typical costs, what each option is good at, and where Page One fits, and where it doesn't.",
          '<p class="hero-price"><b>S$20</b>/month · <span class="intro-tag">Introductory price</span> · no setup fee · no contract</p>') + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Side by side</p>
        <h2 class="reveal">SEO agency vs in-house executive vs Page One</h2>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th></th><th>SEO agency</th><th>In-house SEO / digital marketing executive</th><th>Page One</th></tr></thead>
            <tbody>
              <tr><th>Typical monthly cost</th><td>Often around S$500 to S$3,000+ for a small business retainer</td><td>Salary often around S$3,000 to S$5,000, plus 17% employer CPF and tools</td><td><b>S$20</b> (introductory price), optional SEO Boosts S$10 each</td></tr>
              <tr><th>Upfront</th><td>Sometimes a setup or audit fee</td><td>Recruitment time, equipment and training</td><td>No setup fee</td></tr>
              <tr><th>Commitment</th><td>Minimum terms are common</td><td>Employment contract and notice period</td><td>None, cancel anytime</td></tr>
              <tr><th>Website included</th><td>Usually quoted separately</td><td>Depends on their skills</td><td>Yes, if you need one</td></tr>
              <tr><th>AI search (ChatGPT, Google AI answers)</th><td>Varies: some packages include it only in higher tiers</td><td>Depends on their skills</td><td>Included: Bing connected (ChatGPT search uses it), business details labelled with structured data, an llms.txt summary. <a class="link" href="/seo-aeo-geo-singapore/">SEO, AEO and GEO explained</a></td></tr>
              <tr><th>Can you check results yourself?</th><td>Ask for Google Search Console access</td><td>Yes, it's your own account</td><td>Yes: Search Console is connected so you see your own Google numbers</td></tr>
              <tr><th>What's covered</th><td>Depends on the package: can include competitive keywords, links, content and ads</td><td>Often SEO plus social media, ads, content and events</td><td>Organic Google, Google Maps and AI search for a local business: website, setup, regular articles, monthly audit</td></tr>
              <tr><th>Best for</th><td>Larger budgets, national or multi-market searches</td><td>Enough marketing work to keep a full-time person busy</td><td>New and small local businesses that want the essentials done properly</td></tr>
            </tbody>
          </table>
        </div>
        <p class="note reveal"><b>About these figures:</b> agency and salary figures are general Singapore market ranges for illustration only. They are typical ranges, not quotes from any provider, and real prices vary a lot by experience and scope. Always ask for a written quote. Only Page One's own prices are exact.</p>
      </div>
    </section>

    <section class="section alt" id="hiring">
      <div class="wrap split">
        <div class="reveal">
          <p class="kicker">Thinking of hiring an SEO executive?</p>
          <h2>Add up the full cost first</h2>
          <p>A good SEO or digital marketing executive can be worth every dollar, if there's enough work for them. Before you post the job ad, count everything the role costs, not just the salary.</p>
          <ul class="ticks">
            <li><b>Salary.</b> Typically around S$3,000 to S$5,000 a month for these roles, depending on experience (general range, not a quote).</li>
            <li><b>Employer CPF.</b> 17% on top for Singapore citizens and PRs aged 55 and below.</li>
            <li><b>Tools.</b> Professional SEO tools are usually paid monthly subscriptions.</li>
            <li><b>Your time.</b> Recruiting, training, managing and covering leave or a resignation.</li>
          </ul>
          <p class="fine">Example only: a S$3,500 salary plus 17% CPF is about S$4,095 a month, or roughly S$49,000 a year, before tools or bonus.</p>
        </div>
        <div class="panel reveal" style="background:#fff">
          <h3>When each makes sense</h3>
          <ul class="ticks">
            <li><b>Hire</b> when you have ongoing marketing work across social media, ads, content and events, and someone to manage the role.</li>
            <li><b>Use Page One</b> when what you mainly need is to be found on Google, Google Maps and ChatGPT, with the website looked after for you.</li>
            <li><b>Or both.</b> We handle the website and search groundwork, and your executive focuses on social media, ads and customers.</li>
          </ul>
          <a class="card-link" href="/get-found/">See what S$20 a month covers →</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Before you sign with anyone</p>
        <h2 class="reveal">Seven questions to ask any SEO provider</h2>
        <ul class="ticks reveal">
          <li><b>Who owns the website and the domain?</b> It should be you. With Page One, your domain is registered in your name.</li>
          <li><b>Is there a minimum contract or setup fee?</b> Know what you're committing to before you start.</li>
          <li><b>What exactly is done each month?</b> Ask for a list, not "ongoing optimisation".</li>
          <li><b>Will I get access to Google Search Console?</b> It's Google's own free report, so you can check results yourself.</li>
          <li><b>Do you guarantee rankings?</b> If the answer is yes, be careful. Google decides rankings, so no one can promise them.</li>
          <li><b>How do you get links?</b> Bought links break Google's guidelines and can hurt your site.</li>
          <li><b>Does it cover AI search?</b> More people now ask ChatGPT or read Google's AI answers before they click. Ask what is done for that, and whether it costs extra.</li>
        </ul>
        <p class="kicker reveal" id="check-claims" style="margin-top:56px">Check before you trust</p>
        <h2 class="reveal">How to check any SEO provider's claims in 10 minutes</h2>
        <p class="section-lead reveal">SEO pages are full of big numbers: "#1 ranked", "200+ clients", "300% more leads". Many come with no client name, no date and no way to check. Here's how to test them, whoever you are talking to, including us.</p>
        <ul class="ticks reveal">
          <li><b>Look up the company.</b> Search the company name or UEN on ACRA's Bizfile. A real Singapore company shows its registration date and status.</li>
          <li><b>Ask for dated Search Console numbers.</b> Search Console is Google's own report. Ask for clicks, impressions and average position with the date range shown, for a site you can visit.</li>
          <li><b>Visit the client websites.</b> If they name clients, open the sites and search for their services yourself.</li>
          <li><b>Read the headline against the small print.</b> A page that promises "Rank #1" but says in its FAQ that no one can guarantee rankings is telling you something.</li>
          <li><b>Find the minimum term.</b> Many SEO contracts have one. Know yours before you pay the first invoice.</li>
        </ul>
        <p class="note reveal">We publish ours: company registration, live client websites and dated Search Console numbers. <a class="link" href="/is-page-one-singapore-legit/">Check Page One's claims yourself →</a> · <a class="link" href="/results/">Our Search Console results →</a></p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Where Page One fits</p>
        <h2 class="reveal">Honest about what S$20 a month is for</h2>
        <div class="cards two" style="margin-top:32px">
          <div class="card reveal"><p class="pill">A good fit</p><h3>New and small local businesses</h3><p>You're opening a business, or you're a small business that wants to be found on Google, Google Maps and ChatGPT without a big retainer. You'd rather WhatsApp someone than learn SEO tools. No website yet? We build one. Already have one? We add an SEO landing page next to it.</p></div>
          <div class="card reveal"><p class="pill">Probably not a fit</p><h3>When you need more than search groundwork</h3><p>You need paid ads managed, social media run for you, a large online shop with thousands of products, several countries, or someone in your office every day. An agency or an in-house hire is the better choice there.</p></div>
        </div>
        <p class="note reveal">Why can it cost this little? AI now does the daily SEO work that used to be billed by the hour. <a class="link" href="/cheapest-seo-singapore/">Cheap SEO doesn't have to mean bad SEO →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Proof, not promises</p>
        <h2 class="reveal">The same system, on real Singapore businesses</h2>
        {PROOF_GARAGE}
        <div style="margin-top:28px">{PROOF_CLEANIC}</div>
      </div>
    </section>

""" + PRICE_GLANCE + f"""
    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">SEO services in Singapore: your questions, answered</h2>
        <div style="margin-top:24px">
{_faq_html(SEO_SERVICES_FAQ)}        </div>
        <p class="note reveal">Starting a new business? <a class="link" href="/new-business-website/">Get your first website and Google listing →</a></p>
      </div>
    </section>

""" + cta("Compare it for yourself", "Start at S$20 a month with no setup fee and no contract, or ask Edwin anything on WhatsApp first. No obligation."),
     crumb="SEO services compared", updated="2026-10-13")
