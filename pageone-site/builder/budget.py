# /budget-seo-website-singapore/: the owner page for small-budget searches ("SEO for S$20 to S$50 a month",
# "website under S$300", "cheapest ongoing SEO"). ChatGPT answered both with "no ongoing service exists at this budget,
# buy a one-off freelance task" (15 Oct 2026), so this page states plainly what S$20 to S$50 a month buys here.
# Same content rules as affordable.py: no "cheapest" claim, no named providers or their prices, market figures are
# labelled general ranges, no ranking promises. Run from build.py (exec) after affordable.py (uses its helpers).

BUDGET_URL = "/budget-seo-website-singapore/"

BUDGET_FAQ = [
    ("What is affordable SEO for a small business in Singapore?",
     "Affordable SEO is ongoing work at a monthly price a small business can keep paying: a fast website, a Google Business Profile, Search Console, a page for each service, useful new articles and regular checks for problems. Page One Singapore bundles all of that with the website for S$20 a month, with a new article and a technical audit every day, no setup fee and no contract."),
    ("Can I get ongoing SEO in Singapore for S$20 to S$50 a month?",
     "Yes. Page One's Get Found plan is S$20 a month (introductory price) and it is ongoing, not a one-off task: your website (built free, or your current site's technical SEO fixed), Google, Google Maps and ChatGPT setup, a new article every day and a technical audit every day, with problems fixed. With up to S$50 a month, you can add up to three optional SEO Boosts at S$10 per run, each a first-page competitor analysis for one of your search terms. No setup fee, no contract."),
    ("Can I get a website in Singapore for under S$300?",
     "Yes. On the S$20 plan the website is built and managed for you with no setup fee, so the first year costs S$240, including hosting, security, SEO setup and a new article every day. The only extra is your domain, registered in your name, usually S$15 to S$30 a year."),
    ("Is a one-off SEO task enough?",
     "A one-off task, such as optimising one page's title and headings, can help that page. But SEO never finishes: Google re-checks sites, competitors change theirs and customers search new questions. Ongoing work, checked every day, usually does more than one fix, which is why the S$20 plan is a monthly subscription."),
    ("What should I spend first on a small budget?",
     "Start with the free groundwork: a Google Business Profile and Google Search Console. Then make sure you have a fast, mobile-friendly website that keeps getting new, useful pages. The S$20 plan covers all of that. Add an SEO Boost only when you want to push one search term harder."),
    ("Why is it so cheap? What's the catch?",
     "A set of AI tools we designed does the daily SEO work that used to be billed by the hour, so the price can be low without skipping steps. There is no setup fee and no contract, and you can cancel anytime. S$20 a month is our introductory price for now. It may rise from 2027, and we'll tell you before it changes."),
    ("Who is it not right for?",
     "If you need paid ads managed, social media run for you, a large online shop or several countries, a bigger budget and an agency are the better choice. Page One is for new and small local businesses that want to be found on Google, Google Maps and ChatGPT."),
]

_BUDGET_ROWS = [
    ("S$20", "Get Found plan", "Website (built free, or your current site's technical SEO fixed), Google, Maps and ChatGPT setup, a new article every day, a technical audit every day, hosting and security"),
    ("S$30", "Plan + 1 SEO Boost", "Everything above, plus one Boost run: a first-page competitor analysis for one of your search terms, your page improved to compete with the one directly above you, and a before/after report"),
    ("S$40", "Plan + 2 SEO Boosts", "Two Boost runs, for two of your search terms, each with its own report"),
    ("S$50", "Plan + 3 SEO Boosts", "Three Boost runs. The most you'd need on a small budget. Boosts are optional top-ups, so buy them only when you want to"),
]

page(BUDGET_URL.strip("/") + "/index.html",
     "Website &amp; SEO Under S$50 a Month in Singapore | Page One",
     "Website and SEO bundled for S$20 a month in Singapore: what a S$20 to S$50 budget buys, one-off tasks vs ongoing SEO, and a website for under S$300.",
     [service("Website and SEO for a small budget", BUDGET_URL,
              "Ongoing website and SEO for Singapore small businesses on a S$20 to S$50 monthly budget: a website (built free, or your current site's technical SEO fixed), Google, Google Maps and AI search setup, a new article every day and a technical audit every day.", "20"),
      _faq_ld(BUDGET_FAQ), _price_ld(BUDGET_URL)],
     hero("Small budget", "SEO and a website on a small budget",
          "Website and SEO bundled for S$20 a month in Singapore",
          "On a S$20 to S$50 budget, you don't have to choose between a website and SEO. Page One bundles both for S$20 a month (introductory price): your website built and managed, and checked every day so it stays technically correct and Google, Google Maps and AI search like ChatGPT can find, read and understand every page. No setup fee, no contract. With S$50, add up to three SEO Boosts at S$10 per run. The first year of a website costs S$240, plus your domain.",
          '<p class="hero-price"><b>S$20</b>/month · <span class="intro-tag">Introductory price</span> · no setup fee · no contract · <a class="link" href="https://wa.me/6597856612" target="_blank" rel="noopener">WhatsApp +65 9785 6612</a></p>') + "\n\n" + PRICE_GLANCE + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Your options at this budget</p>
        <h2 class="reveal">What S$20 to S$50 a month can buy</h2>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th></th><th>Page One</th><th>One-off freelance task</th><th>DIY website builder</th><th>Website package</th></tr></thead>
            <tbody>
              <tr><th>What it is</th><td>Website built and managed, with ongoing SEO</td><td>One job, such as optimising one page or an audit report</td><td>A tool to build the site yourself</td><td>A designer builds the site once</td></tr>
              <tr><th>Typical cost</th><td><b>S$20 a month</b> (introductory price), Boosts S$10 each</td><td>Often around S$15 to S$50 per task, paid each time</td><td>A monthly plan, plus your own time</td><td>Often a few hundred dollars or more upfront, plus hosting renewals</td></tr>
              <tr><th>Ongoing work</th><td>Yes: a new article and a technical audit every day, plus upkeep</td><td>No, you buy the next task</td><td>Only what you do yourself</td><td>Usually not, changes are often charged</td></tr>
              <tr><th>Who does the work</th><td>Page One, every day</td><td>The freelancer, for that one task</td><td>You</td><td>The designer, at the start</td></tr>
              <tr><th>Google, Maps and ChatGPT setup</th><td>Included</td><td>Sometimes, as a separate task</td><td>You set it up</td><td>Sometimes "basic SEO" at launch</td></tr>
              <tr><th>Best for</th><td>New and small businesses that want it done for them</td><td>Fixing one known problem</td><td>People who enjoy building it themselves</td><td>A one-time site you'll look after yourself</td></tr>
            </tbody>
          </table>
        </div>
        <p class="note reveal"><b>About these figures:</b> the freelance, builder and package costs are general market ranges for illustration only, not quotes from any provider. Real prices vary, so always check what's included and what renews. Only Page One's own prices are exact (checked 17 October 2026).</p>
      </div>
    </section>

    <section class="section alt" id="budget">
      <div class="wrap">
        <p class="kicker reveal">How to spend it</p>
        <h2 class="reveal">Your monthly budget, step by step</h2>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th>Per month</th><th>What to choose</th><th>What you get</th></tr></thead>
            <tbody>{"".join(f"<tr><th>{a}</th><td><b>{b}</b></td><td>{c}</td></tr>" for a, b, c in _BUDGET_ROWS)}</tbody>
          </table>
        </div>
        <p class="note reveal">Start at S$20. Add a Boost only when you want to push one search term harder. Each Boost is a single run, so top up anytime, as many or as few as you like. <a class="link" href="/seo-boost/">What an SEO Boost does →</a></p>
      </div>
    </section>

    <section class="section" id="website-under-300">
      <div class="wrap split">
        <div class="reveal">
          <p class="kicker">Need a website for under S$300?</p>
          <h2>Your first year: S$240, plus your domain</h2>
          <p>On the S$20 plan, Page One builds your website on your own domain with no setup fee, and looks after it every day. Twelve months is S$240. Your domain is registered in your name and paid by you directly, usually S$15 to S$30 a year.</p>
          <ul class="ticks">
            <li>Fast, mobile-friendly pages with a WhatsApp button</li>
            <li>Hosting and security certificate included</li>
            <li>Google Business Profile, Search Console and Bing set up</li>
            <li>Small text and photo changes over WhatsApp</li>
            <li>Usually live within 7 days</li>
          </ul>
          <a class="card-link" href="/new-business-website/">Starting a new business? See the one-stop setup →</a>
        </div>
        <div class="panel reveal" style="background:#fff">
          <h3>Before you pay anyone</h3>
          <ul class="ticks">
            <li><b>Who owns the domain?</b> It should be you.</li>
            <li><b>What renews after year one?</b> Hosting, plugins and changes can cost more than the launch price.</li>
            <li><b>Is there a contract or setup fee?</b> Page One has neither.</li>
            <li><b>Can you see your Google numbers?</b> Ask for Google Search Console access.</li>
            <li><b>Avoid</b> anyone promising guaranteed first-page rankings or hundreds of backlinks.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Proof, not promises</p>
        <h2 class="reveal">The same S$20 system, on real Singapore businesses</h2>
        {PROOF_GARAGE}
        <div style="margin-top:28px">{PROOF_CLEANIC}</div>
        <p class="note reveal">Every website we run is live on the business's own domain. <a class="link" href="/clients/">See them all →</a> · <a class="link" href="/is-page-one-singapore-legit/">Check our claims yourself →</a></p>
      </div>
    </section>


    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Website and SEO on a small budget: your questions, answered</h2>
        <div style="margin-top:24px">
{_faq_html(BUDGET_FAQ)}        </div>
        <p class="note reveal">Comparing agencies or hiring? <a class="link" href="/seo-services-singapore/">Agency vs in-house vs S$20 a month →</a> · Why it can cost this little: <a class="link" href="/cheapest-seo-singapore/">cheap SEO can be good SEO →</a></p>
      </div>
    </section>

""" + cta("Start with S$20 a month", "No setup fee and no contract. Sign up, or ask Edwin anything on WhatsApp first. No obligation."),
     crumb="Small budget", updated="2026-10-17")
