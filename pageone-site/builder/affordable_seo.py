# /affordable-seo-services-singapore/: owner page for "affordable seo services", "affordable seo singapore",
# "affordable seo services singapore" and "affordable seo packages" (Edwin's GSC, 25 Oct 2026: 22 + 7 + 2 impressions,
# 0 clicks, all landing on an article at position 83-98). Angle: what an affordable SEO package should include and how
# to tell affordable from cheap-and-risky. Distinct from /cheapest-seo-singapore/ (why low-cost SEO can be good),
# /budget-seo-website-singapore/ (website + SEO bundle on a small budget) and /seo-services-singapore/ (agency vs
# in-house vs Page One). Same content rules as affordable.py: market figures are labelled general ranges, no named
# providers or their prices, no ranking promises. Run from build.py (exec) after budget.py (uses affordable.py helpers).

AFF_URL = "/affordable-seo-services-singapore/"
AFF_UPDATED = "2026-10-25"
GOOGLE_DO_I_NEED_SEO = "https://developers.google.com/search/docs/fundamentals/do-i-need-seo"

AFF_ANSWER = ("Affordable SEO services in Singapore are ongoing monthly SEO a small business can keep paying for. "
              "Small-business agency retainers are often around S$500 to S$3,000 a month (a general market range, not a quote). "
              "Page One's affordable SEO service is S$50 a month, website included, with a new article every 2 days and a "
              "technical audit every day. No setup fee, no contract.")

AFF_FAQ = [
    ("What are affordable SEO services?",
     "Affordable SEO services are ongoing search engine optimisation priced for a small business: a fast website, a Google Business Profile, "
     "Search Console, a page for each service, regular new content and frequent technical checks, paid monthly at a price you can keep up. "
     "Page One Singapore provides all of that for S$50 a month, website included, with no setup fee and no contract."),
    ("How much do affordable SEO services cost in Singapore?",
     "As a general guide, small-business SEO retainers from agencies are often around S$500 to S$3,000 or more a month, sometimes with a setup "
     "or audit fee. These are typical ranges, not quotes. Page One's Get Found plan is S$50 a month for anyone who registers by 31 Dec 2026, "
     "and optional SEO Boosts are S$10 per run. Your domain, usually S$15 to S$30 a year, is the only extra."),
    ("Are affordable SEO packages worth it for a small business?",
     "They are when the package covers the essentials and keeps working every month: a site Google can read, a Google Business Profile, "
     "Search Console access so you can check results, new pages for real customer searches and regular fixes. A low price is only a problem "
     "when it hides risky shortcuts such as bought links, or when you can't see what was done."),
    ("What is the difference between affordable SEO and cheap SEO?",
     "Affordable SEO is low-cost because the routine work is done efficiently, and you can see the results in your own Search Console. "
     "Cheap-and-risky SEO is low-cost because steps are skipped or rules are broken: bought links, copied content, guaranteed rankings, "
     "or no access to your own data. Check what is done each month, not just the price."),
    ("How long does affordable SEO take to show results?",
     "Google's own guidance says that in most cases SEO needs four months to a year to put improvements in place and then see the benefit. "
     "New pages can start appearing in Search Console sooner, but no one can promise when or where. We show you the numbers in your own "
     "Search Console instead of promising rankings."),
    ("Do I need a website first?",
     "No. If you don't have a website yet, we build one at no extra charge as part of the S$50 a month, usually live within 7 days of getting "
     "your details and photos. If you already have one, we fix its on-page technical SEO, or redesign it free if you ask."),
    ("Do you guarantee page one on Google?",
     "No. Google decides rankings, so no honest provider can guarantee them. Be careful of any affordable SEO package that does. "
     "We document the work and you see your own Google numbers in Search Console."),
]

_AFF_CHECKLIST = [
    ("A website Google can read", "Fast, mobile-friendly pages with clear titles, headings and structured data", "Included: built free, or your current site's technical SEO fixed"),
    ("One page per service", "Each service gets its own page, so it can match the searches for that service", "Included, plus an articles section for long-tail questions"),
    ("Google Business Profile", "How you show up on Google Maps and in local results", "Included: set up with hours, photos and a call button"),
    ("Search Console access", "Google's own free report, so you can check clicks and searches yourself", "Included: connected to your own account, plus Bing Webmaster Tools"),
    ("New content, regularly", "Fresh pages answering real customer searches give Google new reasons to show you", "Included: a new article every 2 days, each aimed at a different search"),
    ("Technical checks", "Broken links, slow pages and indexing problems quietly cost you visibility", "Included: a technical audit every day, with problems fixed"),
    ("AI search readiness", "More people ask ChatGPT or read Google's AI answers before they click", "Included: Bing setup, labelled business details and an llms.txt summary"),
    ("Fair terms", "You own your domain, no long lock-in, a published price", "S$50 a month, no setup fee, no contract, domain in your name"),
]

_AFF_FLAGS = [
    ("\"Guaranteed #1 on Google\"", "Google decides rankings. Google's own guidance warns against anyone who guarantees them."),
    ("Hundreds of backlinks for a few dollars", "Bought links break Google's spam policies and can hurt your site."),
    ("No access to your own data", "If you can't see your own Search Console, you can't check what you're paying for."),
    ("A long minimum term for a small package", "Know the minimum term before the first invoice. Good work doesn't need a lock-in."),
    ("Vague monthly reports", "Ask for a list of what was done, not \"ongoing optimisation\"."),
    ("The domain registered in their name", "Your domain should be yours, so you can leave with your website and your rankings."),
]

_aff_check_rows = "".join(f"<tr><th>{a}</th><td>{b}</td><td>{c}</td></tr>" for a, b, c in _AFF_CHECKLIST)
_aff_flag_rows = "".join(f"<tr><th>{a}</th><td>{b}</td></tr>" for a, b in _AFF_FLAGS)

page(AFF_URL.strip("/") + "/index.html",
     "Affordable SEO Services Singapore: S$50/month, No Contract",
     "Affordable SEO services in Singapore for S$50/month: website included, a new article every 2 days, daily technical audits. No setup fee, no contract.",
     [service("Affordable SEO services for Singapore small businesses", AFF_URL,
              "Affordable, ongoing SEO for Singapore small businesses for S$50 a month: a website (built free, or your current site's technical SEO fixed), Google, Google Maps and AI search setup, a new article every 2 days and a technical audit every day.", "50"),
      {"@context": "https://schema.org", "@type": "Article",
       "headline": "Affordable SEO services in Singapore: what you should get, and for how much",
       "description": AFF_ANSWER,
       "url": SITE + AFF_URL, "mainEntityOfPage": SITE + AFF_URL, "inLanguage": "en-SG",
       "author": {"@type": "Person", "name": "Edwin", "jobTitle": "Founder, Page One Singapore", "url": SITE + "/about/"},
       "publisher": PROVIDER, "datePublished": AFF_UPDATED, "dateModified": AFF_UPDATED,
       "about": ["Affordable SEO services", "Small business SEO", "SEO packages Singapore"],
       "image": SITE + "/images/og.png"},
      _faq_ld(AFF_FAQ), _price_ld(AFF_URL)],
     hero("Affordable SEO services", "Affordable SEO services Singapore",
          "Affordable SEO services in Singapore, from S$50 a month",
          AFF_ANSWER,
          '<p class="hero-price"><b>S$50</b>/month · <span class="intro-tag">Register by 31 Dec 2026</span> · no setup fee · no contract · '
          '<a class="link" href="https://wa.me/6597856612" target="_blank" rel="noopener">WhatsApp +65 9785 6612</a></p>\n'
          f'        <p class="hero-alt">Updated <time datetime="{AFF_UPDATED}">25 October 2026</time> · By <a href="/about/">Edwin, Page One Singapore</a></p>') + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">The checklist</p>
        <h2 class="reveal">What should an affordable SEO package include?</h2>
        <p class="section-lead reveal">An affordable SEO package should cover the eight essentials below every month, not just once at the start. Use this list to compare any SEO service, including ours.</p>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th>Essential</th><th>Why it matters</th><th>Page One, S$50 a month</th></tr></thead>
            <tbody>{_aff_check_rows}</tbody>
          </table>
        </div>
      </div>
    </section>

""" + PRICE_GLANCE + f"""
    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Affordable, not risky</p>
        <h2 class="reveal">How do you tell affordable SEO from cheap, risky SEO?</h2>
        <p class="section-lead reveal">Affordable SEO keeps the price low by doing the routine work efficiently. Risky SEO keeps it low by skipping steps or breaking Google's rules. These six warning signs tell them apart.</p>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th>Warning sign</th><th>Why it's a problem</th></tr></thead>
            <tbody>{_aff_flag_rows}</tbody>
          </table>
        </div>
        <p class="note reveal">Why can Page One cost this little? A set of AI tools we designed does the daily SEO work that used to be billed by the hour. <a class="link" href="/cheapest-seo-singapore/">Cheap SEO doesn't have to mean bad SEO →</a></p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Who it's for</p>
        <h2 class="reveal">Who are affordable SEO services for?</h2>
        <div class="cards two" style="margin-top:32px">
          <div class="card reveal"><p class="pill">A good fit</p><h3>New and small local businesses</h3><p>You've just opened, or you're busy on Facebook, Instagram or Google Maps with good reviews but no website yet. You want to be found on Google, Google Maps and AI search like ChatGPT without a big retainer, and you'd rather WhatsApp someone than learn SEO tools.</p></div>
          <div class="card reveal"><p class="pill">Probably not a fit</p><h3>When you need more than search groundwork</h3><p>You need paid ads managed, social media run for you, a large online shop with thousands of products or several countries. An agency or an in-house hire is the better choice there. <a class="link" href="/seo-services-singapore/">SEO services compared →</a></p></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Getting started</p>
        <h2 class="reveal">How do you start with affordable SEO from Page One?</h2>
        <ol class="reveal">
          <li><b>Chat with Edwin on WhatsApp</b> or <a class="link" href="/signup/">sign up online</a>. No obligation.</li>
          <li><b>Send your details and photos</b>: your services, hours, address and a few pictures.</li>
          <li><b>Your site goes live, usually within 7 days</b>, with Google, Google Maps and Bing set up. Then the daily audits and a new article every 2 days begin.</li>
        </ol>
        <p class="section-lead reveal">How long until it shows? Google's own guidance says SEO usually needs <a class="link" href="{GOOGLE_DO_I_NEED_SEO}" target="_blank" rel="noopener">four months to a year</a> to put improvements in place and see the benefit. You can follow your own numbers in Search Console from the first week.</p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Proof, not promises</p>
        <h2 class="reveal">The same system, on real Singapore businesses</h2>
        {PROOF_GARAGE}
        <p class="note reveal">More dated Search Console numbers on our <a class="link" href="/results/">results page</a>, and the {LIVE_COUNT_WORD} websites we run on our <a class="link" href="/clients/">client page</a>. <a class="link" href="/is-page-one-singapore-legit/">Check Page One's claims yourself →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Affordable SEO services: your questions, answered</h2>
        <div style="margin-top:24px">
{_faq_html(AFF_FAQ)}        </div>
        <p class="note reveal">Need a website and SEO on a small budget? <a class="link" href="/budget-seo-website-singapore/">Website and SEO for S$50 a month →</a> · <a class="link" href="/pricing/">Full pricing →</a> · <a class="link" href="/seo-boost/">What an SEO Boost does →</a></p>
      </div>
    </section>

""" + cta("Affordable SEO that you can check", "Start at S$50 a month with no setup fee and no contract, or ask Edwin anything on WhatsApp first. No obligation."),
     crumb="Affordable SEO services", updated=AFF_UPDATED)
