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
     "The price is low because the daily work is automated, not because steps are skipped. Edwin Garage, where the system was first built, got 2,280 clicks from Google in the 28 days to 5 October 2026 with an average position of 6.1, according to Google Search Console. Results vary by business, so we don't guarantee rankings."),
    ("What's the catch?",
     "There's no setup fee or contract, and you can cancel anytime. S$20 is an introductory price: it goes up once we reach our early-client target, so it's worth grabbing now. Any new price will stay close to S$20. Your domain is registered in your name and paid by you directly, usually S$15–30 a year."),
    ('Is S$20 a month a gimmick price?', "No. S$20 isn't a teaser to upsell you later, and it isn't budget SEO with steps skipped. It's a baseline for what SEO costs now that AI does the daily work that used to be billed by the hour. The same system runs every website we manage, and it's proven on real businesses: Edwin Garage got 2,280 clicks from Google in the 28 days to 5 October 2026, according to Google Search Console. No setup fee, no contract, so you can judge it for yourself."),
    ("How can I check that S$20 SEO really works?",
     "Look at the evidence yourself. Our Google Search Console results for Edwin Garage and Cleanic Detailing are published on our results page with dates. The websites we run are live: Edwin Garage, Cleanic Detailing, SofaCare SG, Alicia Ong Property and Danny Chua Financial, across five different industries. Run any of them through our free website check. Page One Singapore is a project of Snap Commercial Pte. Ltd. (UEN 202209904W), a registered Singapore company."),
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
          <li><b>Checkable.</b> The websites we run are live, across five industries. Run any of them through our <a class="link" href="/free-website-check/">free website check</a>.</li>
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
        <p class="note reveal">Need a website too? <a class="link" href="/cheapest-website-singapore/">A website without the lump sum →</a></p>
      </div>
    </section>

""" + cta("See what S$20 a month can do for you", "Check your website free in under a minute, or chat with Edwin on WhatsApp. No obligation."),
     crumb="Cheap SEO that works")


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
     "Cheapest Website Maker in Singapore? From S$20/month | Page One",
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
        <p class="section-lead reveal">These Singapore businesses use the same system you get: <a class="link" href="https://sggarage.com/" target="_blank" rel="noopener">Edwin Garage</a>, <a class="link" href="https://cleanicdetailing.com/" target="_blank" rel="noopener">Cleanic Detailing</a>, <a class="link" href="https://sofacaresg.com/" target="_blank" rel="noopener">SofaCare SG</a>, <a class="link" href="https://aliciaongproperty.com/" target="_blank" rel="noopener">Alicia Ong Property</a> and <a class="link" href="https://dannychuafinancial.com/" target="_blank" rel="noopener">Danny Chua Financial</a>. <a class="link" href="/website/">More about our websites →</a></p>
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
     crumb="A website without the lump sum")


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
]

page("new-business-website/index.html",
     "Website for a New Business in Singapore: S$20/month, All Done",
     "Starting a business in Singapore? Page One sets up your website, hosting, content and Google listing for S$20/month. No setup fee, no contract, live in 7 days.",
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
        <p class="note reveal">With Page One, steps 2 and 3 are done for you, and we help you with step 1.</p>
      </div>
    </section>

    <section class="section alt">
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
        <p class="note reveal">Already have a website that nobody looks after? <a class="link" href="/website/">We can take it over →</a></p>
      </div>
    </section>

""" + cta("Starting a business? Let's get you online.", "Chat with Edwin on WhatsApp: tell us what you do and where. Live within 7 days, S$20 a month."),
     crumb="New business website")
