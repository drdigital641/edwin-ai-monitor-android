# One page per client case study (/results/<slug>/), learned from First Page Digital's /client-results/<brand>/
# pages (20 Oct 2026): a named business, its own URL, the numbers, what was done. /results/ stays the hub.
# Edwin Garage keeps its existing owner page (the /articles/seo-case-study-singapore-car-workshop/ article plus the
# /results/ section), so it gets no second page here: one owner page per search intent.
# Every figure comes from builder/showcase.json (Google Search Console via CaseStudyStats); never type one by hand.
# Run from build.py (exec) after the /results/ page, so kpis(), months_table() and ranks_table() exist.

CS_UPDATED = SC_UPDATED


def _cs_month_rows(key):
    """Every month with data, partial months labelled with their day count (the first and the current month)."""
    rows = []
    for m in SC_BY[key]["gsc"]["monthly"]:
        name = month_long(m["month"]).split()[0]
        days_in = 31 if m["month"][5:] in ("01", "03", "05", "07", "08", "10", "12") else 30
        if m["days"] < days_in:
            name += f" ({m['days']} days)"
        rows.append((name, _n(m["clicks"]), _n(m["impressions"]), f"{m['position']:.1f}"))
    return rows


def _cs_faq_html(faqs):
    return "".join(f'        <details class="reveal"><summary>{q}</summary><p>{a}</p></details>\n' for q, a in faqs)


def case_page(key, slug, title, desc, kicker, h1, lead, story, did, lessons, faqs, about_type):
    c, f, g = SC_BY[key], G[key], SC_BY[key]["gsc"]
    url = f"/results/{slug}/"
    first_m, last_m = g["monthly"][0], g["monthly"][-1]
    kpi = [
        ("Clicks from Google, last 28 days", f["clicks"], ("Up from " if g["clicks"] > g["prev_clicks"] else "Compared with ") + f["prev_clicks"] + " the 28 days before"),
        ("Times shown on Google, last 28 days", f["impr"], ("Up from " if g["impressions"] > g["prev_impressions"] else "Compared with ") + f["prev_impr"]),
        ("Average position", f["pos"], ("Better than " if g["position"] < g["prev_position"] else "Compared with ") + f["prev_pos"] + " the 28 days before"),
        ("Searches on page one", f["page_one"], f"{f['top3']} in the top 3"),
    ]
    ranks = ""
    if g["top_queries"]:
        ranks = f"""
        <h3 class="reveal">Where it shows up on Google</h3>
        <p class="reveal">A few of the searches it ranks for (28 days to {THROUGH_SHORT}):</p>
        <div class="reveal">{ranks_table(query_rows(key))}</div>"""
    did_html = "".join(f"<li>{x}</li>" for x in did)
    lessons_html = "".join(f'<div class="card reveal"><h3>{t}</h3><p>{p}</p></div>' for t, p in lessons)
    others = [(u, n) for u, n in CASE_LINKS if u != url]
    others_html = " ".join(f'<a class="card-link" href="{u}">{n} →</a>' for u, n in others)
    schemas = [
        {"@context": "https://schema.org", "@type": "Article", "headline": h1, "url": SITE + url,
         "description": desc, "author": {"@type": "Person", "name": "Edwin"}, "publisher": PROVIDER,
         "datePublished": "2026-10-21", "dateModified": CS_UPDATED, "inLanguage": "en-SG",
         "about": {"@type": about_type, "name": c["name"], "url": c["url"]}},
        _faq_ld(faqs),
    ]
    page(f"results/{slug}/index.html", title, desc, schemas,
         hero(f'<a href="/results/">Results</a> / {c["name"]}', kicker, h1, lead, buttons=False) + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">At a glance</p>
        <h2 class="reveal">{c["name"]} on Google, in numbers</h2>
        <p class="section-lead reveal">Last 28 days ({WINDOW}), compared with the 28 days before ({PREV_WINDOW}). Straight from Google Search Console, unedited. "Page one" means an average position of 1 to 10.</p>
        <div class="reveal">{kpis(kpi)}</div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <div class="split">
          <div class="reveal">
            <p class="kicker">The business</p>
            <h2>{c["industry"]}</h2>
{story}
            <p><a class="link" href="{c["url"]}" target="_blank" rel="noopener">Visit {c["domain"]} ↗</a></p>
          </div>
          <div class="panel reveal" style="background:#fff">
            <h3>What we did</h3>
            <ul class="ticks">{did_html}</ul>
            <p class="fine" style="margin:0">{_n(c["articles"])} articles published so far, each aimed at a different real search.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Month by month</p>
        <h2 class="reveal">From {month_long(first_m["month"]).split()[0]} to {month_long(last_m["month"]).split()[0]} {last_m["month"][:4]}</h2>
        <p class="reveal">Search Console data starts on {f["first_long"]}. Months with fewer days are marked; data runs to {THROUGH}.</p>
        <div class="reveal">{months_table(_cs_month_rows(key))}</div>{ranks}
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">What you can take from it</p>
        <h2 class="reveal">Lessons for your own business</h2>
        <div class="cards three" style="margin-top:24px">{lessons_html}</div>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">About this case study</h2>
{_cs_faq_html(faqs)}        <p class="note reveal"><a class="card-link" href="/results/">All results →</a> {others_html}</p>
      </div>
    </section>

""" + cta("Want the same system on your website?", "S$50 a month, no contract. Or check your website free first, or ask Edwin on WhatsApp."),
         crumb=c["name"], crumb_parent=("Results", "/results/"), updated=CS_UPDATED)
    return url


CASE_LINKS = [
    ("/results/#edwin-garage", "Edwin Garage (car workshop)"),
    ("/results/cleanic-detailing/", "Cleanic Detailing (car detailing)"),
    ("/results/danny-chua-financial/", "Danny Chua Financial (financial consultant)"),
]

_cl = SC_BY["cleanic"]["gsc"]
_cl_months = _cl["monthly"]
_cl_dip = max(_cl_months, key=lambda m: m["position"])
_cl_later = [m for m in _cl_months if m["month"] > _cl_dip["month"]]

case_page(
    "cleanic", "cleanic-detailing",
    "Car Detailing SEO Case Study Singapore: Cleanic Detailing | Page One",
    f"How Cleanic Detailing, a Singapore mobile car grooming service, reached page one on Google for {CL['page_one']} searches. Real Search Console numbers to {THROUGH_SHORT}.",
    "Case study · Mobile car detailing",
    f"Cleanic Detailing: page one on Google for {CL['page_one']} searches",
    f"A mobile car grooming and fumigation service run by Colin Loo. In the 28 days to {THROUGH_SHORT}, Google showed it {CL['impr']} times and it ranked in the top 3 for searches like {top3_examples('cleanic')}.",
    f"""            <p>Cleanic Detailing goes to the customer's car to groom, steam-clean and fumigate it. Customers find this kind of service by searching for the job and the area, so every service needed its own page that answers what people type.</p>
            <p>Its Search Console data starts on {CL['first_long']}. The average position dipped to {_cl_dip['position']:.1f} in {month_long(_cl_dip['month']).split()[0]}, while Google began showing the site for many more searches, which usually pulls the average down for a while. It improved every month after that: {", ".join(f"{m['position']:.1f} in {month_long(m['month']).split()[0]}" for m in _cl_later)}.</p>""",
    SC_BY["cleanic"]["built"] + ["New articles chosen from the searches Google already shows the site for"],
    [("One page per service", "Grooming, steam cleaning, fumigation and odour removal each have their own page, so each can rank for its own searches instead of one page trying to cover everything."),
     ("Write about the customer's problem", "Many searches are problems, not service names: a smell, cockroaches, a spill. Guides that answer those bring in people who need the service now."),
     ("Let the data pick the topics", "New articles target searches Search Console already shows the site for, so effort goes where Google is already paying attention.")],
    [("Where do these numbers come from?", f"Google Search Console, Google's own report on how a website performs in Google Search. We collect the final data automatically and don't edit it. Data runs to {THROUGH}."),
     ("How long did it take?", f"Search Console data for Cleanic Detailing starts on {CL['first_long']}. It reached page one for {CL['page_one']} different searches in the 28 days to {THROUGH_SHORT}. Every business is different, so we don't promise the same timing."),
     ("Will my business get the same results?", "We can't promise that, and no honest provider can. Results depend on your industry, your competition and how long your site has been running. What we can promise is the same system, and Search Console connected so you see your own numbers.")],
    "LocalBusiness")

_dn = SC_BY["danny"]["gsc"]
_dn_first, _dn_last = _dn["monthly"][0], _dn["monthly"][-1]

case_page(
    "danny", "danny-chua-financial",
    "Financial Adviser SEO Case Study Singapore: the First Months | Page One",
    f"What the first months of SEO look like for a Singapore financial consultant's website: Danny Chua Financial's real Search Console numbers to {THROUGH_SHORT}.",
    "Case study · Financial consultant",
    "Danny Chua Financial: what the first months of SEO really look like",
    f"A newer website in a competitive, regulated field. In the 28 days to {THROUGH_SHORT}, Google showed it {G['danny']['impr']} times, up from {G['danny']['prev_impr']} the 28 days before. Still early, and shown honestly.",
    f"""            <p>Danny Chua is a financial consultant. Financial planning is a crowded field on Google, and a regulated one, so the site sticks to plain explanations and shows representative details that visitors can check for themselves.</p>
            <p>Search Console data starts on {G['danny']['first_long']}. In {month_long(_dn_first['month']).split()[0]} ({_dn_first['days']} days) Google showed the site {_n(_dn_first['impressions'])} times at an average position of {_dn_first['position']:.1f}. In the first {_dn_last['days']} days of {month_long(_dn_last['month']).split()[0]} it was shown {_n(_dn_last['impressions'])} times at {_dn_last['position']:.1f}. Most of its searches are not on page one yet; this is what the climb looks like before they are.</p>""",
    SC_BY["danny"]["built"] + ["Google Search Console connected, so the numbers on this page are Google's own"],
    [("Impressions come before clicks", "In the first months, Google tests a new site by showing it lower down for more searches. Clicks follow once pages move up, so a rising 'times shown' figure is the early sign to watch."),
     ("Average position moves slowly", f"It went from {_dn_first['position']:.1f} to {_dn_last['position']:.1f} here. A big average hides the searches already on page one: {G['danny']['page_one']} of them in the 28 days to {THROUGH_SHORT}."),
     ("Regulated fields need care", "Plain facts, no promises, and details visitors can verify. That builds trust with people and gives Google and AI assistants something reliable to show.")],
    [("Why show a case study that is still early?", "Because most new websites look like this for the first few months, and anyone selling SEO should say so. Our newer client sites are shown the same way on the results page."),
     ("Where do these numbers come from?", f"Google Search Console, Google's own report on how a website performs in Google Search. We collect the final data automatically and don't edit it. Data runs to {THROUGH}."),
     ("How long does SEO take for a new website?", "Usually months, not weeks. Google first needs to find and test the pages, then rankings build as articles add up. We can't promise timing or rankings for any business.")],
    "Person")
