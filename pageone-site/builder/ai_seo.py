# "AI SEO vs traditional SEO" and "Is Page One Singapore legit?" pages.
# Run from build.py (exec) after affordable.py, so it uses build.py's helpers, _faq_html/_faq_ld/_cards/_myths
# and PROOF_GARAGE / PROOF_CLEANIC.
# Content rules: every claim either describes what the system really does or points to something a reader can
# check without trusting us (ACRA Bizfile, live websites, Google itself, Search Console data with dates).
# No invented numbers, testimonials, rankings guarantees or "cheapest" claims. Traditional SEO is described
# fairly and generally ("often", "usually"), never as any named provider.

# Client list, counts and every Search Console figure come from showcase.json (see showcase.py).
SITES_LIST = names_list([f'<a class="link" href="{c["url"]}" target="_blank" rel="noopener">{c["name"]}</a> ({c["short"]})' for c in SC["clients"]])
_N = LIVE_COUNT_WORD
_BQ_CL, _BQ_EG = SC_BY["cleanic"]["gsc"]["best_query"], SC_BY["sggarage"]["gsc"]["best_query"]
_LATER = names_list([c["name"] for c in SC["clients"] if c["key"] not in ("sggarage", "cleanic")])


def _rows(rows, head):
    th = "".join(f"<th>{h}</th>" for h in head)
    trs = "".join("<tr><th>" + r[0] + "</th>" + "".join(f"<td>{c}</td>" for c in r[1:]) + "</tr>" for r in rows)
    return f"""<div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr>{th}</tr></thead>
            <tbody>{trs}</tbody>
          </table>
        </div>"""


# ---------- AI SEO vs traditional SEO ----------
AI_VS_FAQ = [
    ("What is the difference between AI SEO and traditional SEO?",
     "The goal is the same: help a business show up when customers search. The difference is how the work gets done. Traditional SEO is mostly done by hand, so it's priced by the hours people spend on it. Page One has designed a set of AI tools that do the repetitive daily work automatically, such as checking pages, reading Search Console data, writing articles and telling Google and Bing about changes. Edwin designs the strategy and the system and reviews the results."),
    ("Why is Page One so cheap?",
     "Because most of the cost of SEO has always been people's time, and AI tools we designed now do most of the routine work automatically. The Get Found plan is S$50 a month because fewer hours are needed, not because steps are skipped. The same system runs Edwin Garage, Edwin's own workshop, which got " + EG["clicks"] + " clicks from Google in the 28 days to " + THROUGH + ", according to Google Search Console."),
    ("Is automated SEO low quality?",
     "Quality comes from the strategy, the site structure and what gets published, not from how many hours were billed. The results are measurable: in the 28 days to " + THROUGH + ", Edwin Garage appeared on page one of Google for " + (("more than " + EG["page_one"].rstrip("+")) if EG["page_one"].endswith("+") else EG["page_one"]) + " different searches and Cleanic Detailing for " + CL["page_one"] + ", according to Google Search Console. We follow Google's guidelines: no bought links, no fake reviews and no keyword stuffing."),
    ("Is AI SEO weaker than an expensive agency?",
     "No. An agency's edge is its analysis of the competition: studying the pages Google already ranks and building something better. Page One's EDGE Loop does the same analysis, then keeps watching your Search Console data every day instead of once a month. The cost is lower because the repetitive work is automated, not because steps are skipped."),
    ("What is GEO (generative engine optimisation)?",
     "GEO means making a business easy for AI assistants such as ChatGPT, Gemini and Perplexity to read, understand and mention. Page One does this with structured data (Schema.org), an llms.txt summary, Bing Webmaster Tools (Bing powers ChatGPT search) and content that answers customers' questions clearly. No one can guarantee an AI assistant will recommend a business, but these steps make it possible."),
    ("Does the system really work around the clock?",
     "It runs on a schedule, every day, including weekends and public holidays. Google Search Console data is pulled in automatically, and new articles are picked from the searches Google already shows a site for. When something needs a person, it is flagged to Edwin."),
    ("Does a person still look after my site?",
     "Yes. Edwin designs the strategy and the system, reviews the results and replies on WhatsApp personally. Automation does the legwork. It doesn't replace judgement."),
    ("Can you guarantee page one rankings?",
     "No, and no honest provider can, because Google decides rankings. What we can show you is the same system working on real Singapore businesses, with dated Google Search Console data, and a report for every SEO Boost."),
    ("When is traditional SEO the better choice?",
     "When you need more than search groundwork: paid ads managed for you, a large online shop with thousands of products, several countries, or a big link-building and PR campaign. An agency or an in-house team is the better fit there."),
]

page("ai-seo-vs-traditional-seo/index.html",
     "AI SEO vs Traditional SEO: Cheap, Not Low Quality | Page One",
     "Why AI-powered SEO costs less than traditional, labour-based SEO without cutting quality. A side-by-side comparison, GEO for AI search, and real Google results.",
     [{"@context": "https://schema.org", "@type": "Article",
       "headline": "AI SEO vs traditional SEO: low cost, not low quality",
       "description": "How Page One Singapore uses AI and automation to do SEO with fewer hours, why that lowers the price without lowering quality, and the Google Search Console results behind it.",
       "url": SITE + "/ai-seo-vs-traditional-seo/", "inLanguage": "en-SG",
       "author": {"@type": "Person", "name": "Edwin", "jobTitle": "Founder, Page One Singapore"},
       "publisher": PROVIDER, "datePublished": "2026-10-14", "dateModified": "2026-10-14",
       "about": ["Search engine optimisation", "Generative engine optimisation", "AI automation"],
       "image": SITE + "/images/og.png"},
      service("AI-powered SEO for Singapore businesses", "/ai-seo-vs-traditional-seo/",
              "SEO and AI search visibility (GEO) run by an AI-driven system with a person in charge: website, Google and Bing setup, structured data, llms.txt, a technical audit every day and a new article every day chosen from Search Console data. S$50 a month, no setup fee, no contract.", "50"),
      _faq_ld(AI_VS_FAQ)],
     hero("AI SEO vs traditional SEO", "Why the price is low",
          "Cheap because AI cut the hours. Not because we cut corners.",
          "Traditional SEO is priced by the hour, because people do the work by hand. Page One has designed a set of AI tools to optimise your SEO daily, with Edwin in charge of the strategy. Fewer hours means a lower price. The quality is in the results, and you can check them yourself.",
          '<p class="hero-price"><b>S$50</b>/month · <span class="intro-tag">Register by 31 Dec 2026</span> · no setup fee · no contract</p>') + f"""

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">The short answer</p>
        <h2 class="reveal">Price follows labour. AI made the labour cheap.</h2>
        <p class="section-lead reveal">Most of what you pay for in SEO is people's time: checking pages, fixing problems, writing articles, updating listings and writing reports, every week. When AI tools designed for that routine work monitor, adapt and deploy automatically, far fewer hours are needed, so the price can fall a long way while the work still gets done, and done every day.</p>
        <p class="section-lead reveal">Cheap doesn't have to mean bad, and good doesn't have to be expensive. A price tells you how much labour went in. It doesn't tell you how good the result is. That's why we publish our <a class="link" href="/results/">results</a>, with dates, straight from Google Search Console.</p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Side by side</p>
        <h2 class="reveal">Traditional SEO vs Page One's AI system</h2>
        {_rows([
            ("Where your money goes", "Mostly people's hours, billed as a retainer or by the hour", "A system that does the routine work, with a person setting the strategy"),
            ("How often your site gets attention", "Often weekly or monthly, when someone has time", "Every day, on a schedule, weekends and public holidays included"),
            ("How new content is chosen", "Keyword research done by hand, often at the start of a campaign", "Picked from the searches Google already shows your site for, using your Search Console data"),
            ("Learning from results", "A monthly report, then the next round of work", "A feedback loop: measure, decide, publish, measure again"),
            ("AI search (ChatGPT, Gemini, Perplexity)", "Often an add-on, or not covered", "Built in: structured data, llms.txt, Bing setup and clear answers"),
            ("Adapting when search changes", "Each account is updated by hand", "The system is updated once, and every site on it gets the change"),
            ("Consistency", "Depends on who is doing it and how busy they are", "The same checks, the same way, every time"),
            ("Who's in charge", "An account manager or SEO executive", "Edwin, the founder, who you can WhatsApp directly"),
            ("Price", "Usually priced as a professional service, often hundreds of dollars a month or more", "<b>S$50 a month</b>, no setup fee, no contract"),
        ], ["", "Traditional, labour-based SEO", "Page One (AI + a person in charge)"])}
        <p class="note reveal">The traditional column describes common ways SEO is sold and delivered, not any particular provider. Good agencies do excellent work; it just takes more hours, so it costs more. <a class="link" href="/seo-services-singapore/">Agency, in-house hire or Page One: full comparison →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">How it works</p>
        <h2 class="reveal">A feedback loop that never clocks off</h2>
        <ol class="steps" style="margin-top:56px">
          <li class="reveal"><span>1</span><h3>Measure</h3><p>Google Search Console data, Google's own report of how your site performs, is pulled in automatically every day.</p></li>
          <li class="reveal"><span>2</span><h3>Decide</h3><p>The system looks for the searches Google already shows your site for, and the pages that need work.</p></li>
          <li class="reveal"><span>3</span><h3>Publish</h3><p>New articles and fixes go live, and Google and Bing are told about the changes.</p></li>
        </ol>
        <p class="section-lead reveal" style="margin-top:32px">Then it measures again, and the next round is based on what actually happened, not on guesswork. Edwin sets the strategy, the site structure and the design, and reviews the results. The system does the legwork.</p>
      </div>
    </section>

    <section class="section alt" id="edge-loop">
      <div class="wrap">
        <p class="kicker reveal">Edwin's method</p>
        <h2 class="reveal">The EDGE Loop: traditional SEO craft, run by AI that never stops</h2>
        <p class="section-lead reveal">Traditional agencies study Google's top 10 for your keyword, find where those pages are weak, and build something better. It works, but people do it once a month. Edwin designed the EDGE Loop to keep that craft and remove the wait: every keyword we target is studied against the pages Google already ranks, and our AI checks your Search Console data every day, adjusting whenever the numbers move.</p>
        <div class="cards three" style="margin-top:32px">{_cards([
            ("We study who you have to beat", "For each keyword we break down the current top 10: what they answer, what they miss, where they contradict themselves."),
            ("We build the better answer", "Your page covers everything they do, plus the questions they skip, with real prices, real proof and Singapore detail."),
            ("Our AI never clocks off", "Daily Search Console checks, every change measured, and what doesn't work is dropped while wins are repeated across your site."),
        ])}</div>
        <p class="section-lead reveal" style="margin-top:32px">Early signs, from Google Search Console in October 2026:</p>
        <ul class="ticks reveal">
          <li>A sofa-cleaning client's problem guides already sit on Google's first page, at average positions 6.6 to 10 for pet and urine questions (7 to 13 Oct 2026).</li>
          <li>A financial consultant's guide reaches page one for "ILP meaning", at an average position of 9.8 (7 to 13 Oct 2026).</li>
        </ul>
        <p class="note reveal"><b>No copied content, no fake reviews, no bought links.</b> Just a better page and a loop that keeps improving it. We don't share the full method, and we don't guarantee rankings. We show the results and the work.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">GEO: generative engine optimisation</p>
        <h2 class="reveal">Built for AI answers, not just blue links</h2>
        <p class="section-lead reveal">More people now ask ChatGPT, Gemini or Perplexity instead of scrolling through Google. Those assistants can only recommend a business they can read and trust. Every site on Page One is set up for that from day one.</p>
        <div class="cards three" style="margin-top:32px">{_cards([
            ("Structured data", "Your name, services, area, hours and prices labelled in Schema.org, so machines read them correctly."),
            ("llms.txt", "A plain summary of your business and pages, written for AI tools."),
            ("Bing Webmaster Tools", "Bing powers ChatGPT search, so your site is submitted there as well as to Google."),
            ("Clear answers", "Articles that answer real customer questions directly, the way AI assistants quote them."),
            ("Facts, not fluff", "Claims backed by details people can check, like your registered business name and real service areas."),
            ("Kept current", "When AI search changes, the system is updated once and every site gets the change."),
        ])}</div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">A new way of thinking about price</p>
        <h2 class="reveal">"If it's cheap, it can't be good." Is that still true?</h2>
        {_myths([
            ("Cheap means low quality.", "Cheap used to mean fewer hours, and fewer hours meant less work done. When AI tools designed for the job do the hours, a low price and thorough work can go together."),
            ("Automated means nobody is watching.", "The system flags problems the day they appear, and Edwin reviews the results. It is watched more often than a site that gets a look once a month."),
            ("AI content is spam.", "Google's guidance is that it rewards helpful, accurate content however it's produced. We write useful answers to real customer questions, based on facts about the business and real Search Console data."),
            ("Big agencies must be better because they're big.", "Size tells you how many people are billing hours. Results tell you whether it works. Ask any provider for dated Search Console data."),
            ("Something this cheap must be a trick.", "There's no setup fee and no contract, so you can judge it month by month. Your domain stays in your name."),
        ])}
        <p class="note reveal">The same thing has happened before: online banking didn't make banking worse, it made a bank visit unnecessary. AI is doing the same to the routine work in SEO.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Proof, not promises</p>
        <h2 class="reveal">Tested on real Singapore businesses first</h2>
        <p class="section-lead reveal">The system was built and tested on Edwin's own car workshop before it was offered to anyone. It now runs {_N} live websites: {SITES_LIST}.</p>
        <div style="margin-top:28px">{PROOF_GARAGE}</div>
        <div style="margin-top:28px">{PROOF_CLEANIC}</div>
        <p class="note reveal">Want to check any of this yourself? <a class="link" href="/is-page-one-singapore-legit/">Here's how to verify Page One →</a></p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">AI SEO vs traditional SEO: your questions, answered</h2>
        <div style="margin-top:24px">
{_faq_html(AI_VS_FAQ)}        </div>
        <p class="note reveal">More on price: <a class="link" href="/cheapest-seo-singapore/">Cheap SEO doesn't have to mean bad SEO →</a></p>
      </div>
    </section>

""" + cta("See what the system can do for you", "Check your website free in under a minute, or chat with Edwin on WhatsApp. No obligation."),
     crumb="AI SEO vs traditional SEO", updated="2026-10-19")


# ---------- Is Page One Singapore legit? (verify it yourself) ----------
LEGIT_FAQ = [
    ("Is Page One Singapore legit?",
     "Yes, and you can check it without trusting us. Page One Singapore is run by Snap Commercial Pte. Ltd., a Singapore company registered on 23 March 2022 (UEN 202209904W), which you can look up on ACRA's Bizfile. The " + _N + " websites it runs are live, its Google Search Console results are published with dates, and you can search Google yourself to see those sites on page one."),
    ("Why might an AI assistant call Page One unverified?",
     "AI assistants usually say a business is unverified when they find few independent sources about it. That is normal for a new service: Page One's own website only started appearing in Google Search in October 2026. Being new is not the same as being untested. The system has run Edwin Garage, Edwin's own workshop, since June 2026, and every claim on this page points to something you can check."),
    ("Is the S$50 a month price real, and what does it include?",
     "Yes. S$50 a month is the published price of the Get Found plan, shown on our pricing page. It includes a website at no extra charge: if you don't have one, we build it from scratch, and if you already have one, we fix its on-page technical SEO on your current website, or redesign it free if you ask. It also includes hosting and security, small text and photo changes when you need them, a new article every day, a technical audit every day with problems fixed, Google Business Profile, Google Search Console and Bing setup, and structured data for AI search. Search Console is connected so you can see your own Google numbers. There is no setup fee and no minimum contract. Your domain is paid by you directly, usually S$15 to S$30 a year. Optional SEO Boosts are S$10 per run."),
    ("Who is behind Page One Singapore?",
     "Edwin, the founder. He has a Bachelor's degree in Computer Science with Honours from the National University of Singapore, has run businesses for more than 18 years and owns Edwin Garage, a car workshop in Ang Mo Kio. You can WhatsApp him directly on +65 9785 6612."),
    ("How can I check the Google results are real?",
     "Two ways. First, search Google yourself for the searches listed on this page and look for the websites. Your position may differ a little, because Google varies results by location and device. Second, WhatsApp us and we'll walk you through the Search Console reports behind our published numbers."),
    ("Does Page One guarantee rankings?",
     "No. Google decides rankings, so no one can promise them. Be careful with any provider that does. We show the work and the numbers instead."),
    ("What's the risk of trying it?",
     "There's no setup fee and no contract, so the most you commit is one month at S$50. Your domain is registered in your name, so you keep it whatever happens."),
]

CHECK_ITEMS = [
    ("A registered Singapore company",
     "Page One Singapore is run by <b>Snap Commercial Pte. Ltd.</b>, registered on 23 March 2022, <b>UEN 202209904W</b>.",
     'Search the UEN on <a class="link" href="https://www.bizfile.gov.sg/" target="_blank" rel="noopener">ACRA Bizfile</a>.'),
    (_N.capitalize() + " live websites",
     f"We run the websites for {SITES_LIST}.",
     "Open them and see for yourself. Run any of them through our <a class=\"link\" href=\"/free-website-check/\">free website check</a>."),
    ("On page one of Google, right now",
     f"In the 28 days to {THROUGH}, Cleanic Detailing averaged position {_BQ_CL['position']:.1f} for “{_BQ_CL['query']}” and Edwin Garage averaged {_BQ_EG['position']:.1f} for “{_BQ_EG['query']}”, according to Google Search Console.",
     "Search those phrases on Google yourself. Your exact position may differ a little by location and device."),
    ("Results from Google's own report",
     f"Edwin Garage: {EG['clicks']} clicks from Google and page one for {EG['page_one']} searches in the 28 days to {THROUGH}. Cleanic Detailing: page one for {CL['page_one']} searches.",
     'See the month-by-month data on our <a class="link" href="/results/">results page</a>, or ask us on WhatsApp to walk you through the Search Console reports.'),
    ("Tested on the founder's own business first",
     "The system was built on Edwin Garage, Edwin's own car workshop in Ang Mo Kio, with Search Console data from 26 June 2026.",
     'Visit <a class="link" href="https://sggarage.com/" target="_blank" rel="noopener">sggarage.com</a>, or search Google for “Edwin Garage”.'),
    ("A real person you can talk to",
     "Edwin, the founder, replies on WhatsApp personally.",
     f'Message <a class="link" href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a> and ask him anything.'),
    ("Public prices, no lock-in",
     "S$50 a month, no setup fee, no contract. Your domain is registered in your name.",
     'Every price is on our <a class="link" href="/pricing/">pricing page</a>.'),
]


def _checks(items):
    rows = "".join(f"<tr><th>{t}</th><td>{c}</td><td>{h}</td></tr>" for t, c, h in items)
    return f"""<div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th>What we say</th><th>The facts</th><th>How to check it yourself</th></tr></thead>
            <tbody>{rows}</tbody>
          </table>
        </div>"""


page("is-page-one-singapore-legit/index.html",
     "Is Page One Singapore Legit? Verify Us Yourself | Page One",
     "Is Page One Singapore legit, and is the S$50/month price real? Check it yourself: ACRA-registered company, " + _N + " live client sites, Google results, GSC data.",
     [{"@context": "https://schema.org", "@type": "AboutPage", "url": SITE + "/is-page-one-singapore-legit/",
       "name": "Is Page One Singapore legit? Verify us yourself", "inLanguage": "en-SG",
       "about": {"@type": "ProfessionalService", "@id": BIZ_ID, "name": "Page One Singapore", "url": SITE + "/",
                 "founder": FOUNDER, "parentOrganization": COMPANY, "sameAs": [GBP],
                 "subjectOf": {"@type": "WebPage", "url": SITE + "/results/", "name": "Google Search Console results"}},
       "mentions": [{"@type": "WebSite", "name": c["name"], "url": c["url"]} for c in SC["clients"]]},
      _price_ld("/is-page-one-singapore-legit/"),
      _faq_ld(LEGIT_FAQ)],
     hero("Is Page One legit?", "Verify us yourself",
          "Is Page One Singapore legit? Don't take our word for it.",
          "A low price makes people ask, and they should. Here is every claim we make, with a way to check it that doesn't depend on trusting us.",
          buttons=False) + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">The checklist</p>
        <h2 class="reveal">Seven things you can check in a few minutes</h2>
        {_checks(CHECK_ITEMS)}
      </div>
    </section>

    <section class="section alt" id="price">
      <div class="wrap">
        <p class="kicker reveal">Is the S$50 price real?</p>
        <h2 class="reveal">Yes. Here's exactly what S$50 a month includes</h2>
        <p class="section-lead reveal">AI assistants have described our price as unconfirmed and suggested checking what it covers. These are the questions they recommend asking, answered.</p>
        {_rows([
            ("Actual website changes?", "<b>Yes.</b> No website yet? We design and build one on your own domain, free. Already have one? We fix its on-page technical SEO on your current website, or redesign it free if you ask. Small text and photo changes are included whenever you need them."),
            ("Monthly content?", "<b>Yes.</b> A new article every day, each aimed at a different search Google already shows you for, so your pages don't compete with each other."),
            ("Google Search Console reporting?", "<b>Yes.</b> Search Console, Google's own report, is connected so you can see your own impressions, clicks and searches. Every SEO Boost also comes with a before/after report."),
            ("Minimum contract?", "<b>None.</b> Monthly, cancel anytime. No setup fee and no lump sum."),
            ("Anything else included?", "Hosting and security, a technical audit every day with problems fixed, Google Business Profile, Bing setup, structured data and llms.txt for AI search, and a WhatsApp button."),
            ("What costs extra?", "Your domain, registered in your name and paid by you directly, usually S$15 to S$30 a year. Optional SEO Boosts at S$10 per run, each a first-page competitor analysis for one of your search terms."),
        ], ["Question", "Answer"])}
        <p class="note reveal">S$50 a month is our price for anyone who registers by 31 Dec 2026. From 2027 the price may rise, depending on demand, and we'll tell you before it changes. Every price is published on our <a class="link" href="/pricing/">pricing page</a>.</p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">About “unverified”</p>
        <h2 class="reveal">New is not the same as untested</h2>
        <p class="section-lead reveal">AI assistants such as ChatGPT sometimes describe Page One as “unverified”. That usually means they found few independent sources about us yet, which is normal for a new service: our own website only started appearing in Google Search in October 2026.</p>
        <p class="section-lead reveal">The system itself is not new. It has run Edwin Garage and Cleanic Detailing since June 2026, and later {_LATER}. Their results come from Google's own report, and their websites are live for anyone to see.</p>
        <p class="section-lead reveal">The low price isn't a sign of corners being cut either. It comes from a set of AI tools we designed doing the routine work that used to be billed by the hour. <a class="link" href="/ai-seo-vs-traditional-seo/">How AI SEO compares with traditional SEO →</a></p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">What we don't claim</p>
        <h2 class="reveal">Honest about the limits</h2>
        <ul class="ticks reveal">
          <li><b>No ranking guarantees.</b> Google decides rankings. Anyone who guarantees them is guessing.</li>
          <li><b>No “cheapest in Singapore” claim.</b> We can't check every provider's prices, so we only tell you ours.</li>
          <li><b>No fake reviews or bought links.</b> They break Google's guidelines and can hurt your site.</li>
          <li><b>Not right for everyone.</b> If you need paid ads, social media or a large online shop, an agency is the better fit.</li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Checking out Page One: your questions, answered</h2>
        <div style="margin-top:24px">
{_faq_html(LEGIT_FAQ)}        </div>
      </div>
    </section>

""" + cta("Still unsure? Ask Edwin.", "WhatsApp the founder directly, or check your own website free. No obligation."),
     crumb="Is Page One legit?", updated="2026-10-19")
