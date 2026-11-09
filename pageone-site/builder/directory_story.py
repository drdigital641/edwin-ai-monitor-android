# /results/sg-car-workshop-directory/: short results-style page for workshop OWNERS on how SG Car Workshop
# (sgcarworkshop.sg, run by Page One) works. Edwin approved 10 Nov 2026 (SGCW supporter push, step 2).
# Rules: only facts already published on sgcarworkshop.sg (home, /about/, /list-your-workshop/) or on Page One;
# no traffic, ranking or enquiry numbers; one link to /list-your-workshop/; disclose that Page One runs it;
# never repeat the exact phrase "Singapore car workshop directory". Linked once from /results/.
# Run from build.py (exec) after affordable_seo.py (uses affordable.py helpers _faq_html/_faq_ld).

DIR_URL = "/results/sg-car-workshop-directory/"
DIR_UPDATED = "2026-11-10"
DIR_CLAIM = "https://sgcarworkshop.sg/list-your-workshop/"

DIR_FAQ = [
    ("Who runs SG Car Workshop?",
     "Page One Singapore runs it. Page One is a website and SEO service for small businesses, a project of Snap Commercial Pte. Ltd. "
     "Two listings, Edwin Garage and EV Body Parts, belong to our founder and are labelled as owned by the site's founder."),
    ("Is it free to list or claim my workshop?",
     "Yes. Claiming your listing is free, with no fee and no contract, and you can ask for your listing to be removed at any time. "
     "Page One checks that you run the business before changing anything."),
    ("Can I pay to rank higher?",
     "No. SG Car Workshop does not sell rankings. Paid placements are shown in their own block marked Featured (paid) and are never part of a ranking. "
     "Claiming a listing does not change the order either."),
    ("Will a listing bring me a set number of enquiries?",
     "No one can promise that, and the directory does not. What it gives you is a listing with WhatsApp and Call buttons and an open count "
     "of how many drivers tapped them through SG Car Workshop."),
]

page(DIR_URL.strip("/") + "/index.html",
     "How SG Car Workshop Works for Workshop Owners | Page One",
     "How SG Car Workshop, the car workshop listings site run by Page One Singapore, matches drivers to workshops, keeps paid placements out of ranking, and lets owners claim a free listing.",
     [{"@context": "https://schema.org", "@type": "Article",
       "headline": "How SG Car Workshop works for a workshop owner",
       "description": "SG Car Workshop is run by Page One Singapore. Drivers describe a car problem, car or area and see matching workshops; paid placements are labelled Featured (paid) and kept out of ranking; owners can claim a free listing.",
       "url": SITE + DIR_URL, "mainEntityOfPage": SITE + DIR_URL, "inLanguage": "en-SG",
       "author": {"@type": "Person", "name": "Edwin", "jobTitle": "Founder, Page One Singapore", "url": SITE + "/about/"},
       "publisher": PROVIDER, "datePublished": DIR_UPDATED, "dateModified": DIR_UPDATED,
       "about": {"@type": "WebSite", "name": "SG Car Workshop", "url": "https://sgcarworkshop.sg/", "creator": PROVIDER}},
      _faq_ld(DIR_FAQ)],
     hero('<a href="/results/">Results</a> / SG Car Workshop', "For workshop owners",
          "How SG Car Workshop works for a workshop owner",
          "SG Car Workshop (sgcarworkshop.sg) lists car workshops and car services in Singapore. Page One Singapore runs it. "
          "Here is what it does for a workshop owner, and what it doesn't.", buttons=False) + f"""

    <section class="section">
      <div class="wrap narrow">
        <div class="panel reveal">
          <h2 class="h3">Who is behind it</h2>
          <p>Page One Singapore runs SG Car Workshop. Two of its listings belong to our founder, Edwin: Edwin Garage and EV Body Parts. Both carry an "Owned by the site's founder" label, so drivers can see that link for themselves. Eligible automotive clients of Page One also get a premium listing.</p>
        </div>

        <p class="kicker reveal" style="margin-top:40px">How drivers find you</p>
        <h2 class="reveal">A driver describes the problem, the site shows matching workshops</h2>
        <p class="reveal">A driver can describe their car problem in their own words, or type a service, an area or a workshop name. The site matches what they typed, their car and their area to the workshops that fit. Each listing has WhatsApp and Call buttons. The WhatsApp message is prefilled with your workshop's name and says the driver found you on SG Car Workshop, so you know where the enquiry came from.</p>

        <p class="kicker reveal" style="margin-top:40px">Fair order</p>
        <h2 class="reveal">Paid placements are labelled and kept out of ranking</h2>
        <ul class="ticks reveal">
          <li>SG Car Workshop does not sell rankings and does not write reviews.</li>
          <li>Paid placements sit in their own block, marked <b>Featured (paid)</b>, and are never part of a ranking.</li>
          <li>Claiming your listing does not move you up. Owner-confirmed listings are shown in their own Verified group, in a random order like every group.</li>
          <li>The founder's own listings are labelled, as above.</li>
        </ul>

        <p class="kicker reveal" style="margin-top:40px">For owners</p>
        <h2 class="reveal">What you get when you claim your listing</h2>
        <ul class="ticks reveal">
          <li>A verified badge once Page One has checked that you run the business.</li>
          <li>Your own photos, services and brands on your page, so drivers see what you really do.</li>
          <li>Correct hours and WhatsApp number, kept up to date by you.</li>
          <li>An open count of how many drivers tapped WhatsApp and Call through SG Car Workshop.</li>
          <li>No fee and no contract. You can ask for your listing to be removed at any time.</li>
        </ul>
        <p class="reveal">If your workshop is already listed, or you would like it added, you can <a class="link" href="{DIR_CLAIM}" target="_blank" rel="noopener">claim or add your workshop's free listing</a>. Page One checks that you run the business first, then makes the changes you ask for.</p>

        <p class="kicker reveal" style="margin-top:40px">What it won't do</p>
        <h2 class="reveal">No promised enquiries</h2>
        <p class="reveal">A listing is a way for drivers to find and contact you. It does not promise a number of enquiries, and no one can honestly promise you a place on Google's first page. If you also want your own website found on Google and AI search, that is what Page One's Get Found plan does: S$50 a month, website included, no setup fee and no contract, for anyone who registers by 31 Dec 2026. See the <a class="link" href="/results/">results from businesses we run</a>.</p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Questions from workshop owners</h2>
        <div style="margin-top:24px">
{_faq_html(DIR_FAQ)}        </div>
      </div>
    </section>

""" + cta("Want your own website found too?", "Sign up at S$50 a month, or ask Edwin anything on WhatsApp first. No obligation."),
     crumb="SG Car Workshop", crumb_parent=("Results", "/results/"), updated=DIR_UPDATED)
