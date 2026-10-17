# Client showcase and every Search Console figure on the site, from one data file.
# Run from build.py (exec), right after the shared constants, so every page can use SC / G / proof_*().
# Data: builder/showcase.json, refreshed by builder/showcase_refresh.py from CaseStudyStats.
# Rules: only figures from showcase.json, the date window always stated, no ratings or reviews,
# no "best" or "#1" claims, sites with no Search Console data get "launched" + what was built.
import datetime as _dt

with open(os.path.join(HERE, "showcase.json"), encoding="utf-8") as _f:
    SC = json.load(_f)
SC_BY = {c["key"]: c for c in SC["clients"]}
_MON = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def _d(iso):
    return _dt.date.fromisoformat(iso)


def date_long(iso):
    d = _d(iso)
    return f"{d.day} {_MON[d.month - 1]} {d.year}"


def date_short(iso):
    d = _d(iso)
    return f"{d.day} {_MON[d.month - 1][:3]} {d.year}"


def month_long(ym):
    y, m = ym.split("-")
    return f"{_MON[int(m) - 1]} {y}"


def month_short(ym):
    y, m = ym.split("-")
    return f"{_MON[int(m) - 1][:3]} {y}"


def _n(x):
    return f"{x:,}"


def _span(a, b):
    a, b = _d(a), _d(b)
    left = f"{a.day} {_MON[a.month - 1][:3]}" + (f" {a.year}" if a.year != b.year else "")
    return f"{left} to {b.day} {_MON[b.month - 1][:3]} {b.year}"


THROUGH = date_long(SC["data"]["data_through"])          # 11 October 2026
THROUGH_SHORT = date_short(SC["data"]["data_through"])   # 11 Oct 2026
WINDOW = _span(*SC["data"]["window"])                    # 14 Sep to 11 Oct 2026
PREV_WINDOW = _span(*SC["data"]["prev_window"])          # 17 Aug to 13 Sep 2026
SC_UPDATED = SC["data"]["generated_at"][:10]
# /clients/ changes when the figures change, when a site launches or when the being-built count moves.
CLIENTS_UPDATED = max([SC_UPDATED, SC.get("pipeline", {}).get("as_of", "")]
                      + [c["launched"] + "-01" if len(c["launched"]) == 7 else c["launched"] for c in SC["clients"]])


def _fmt(c):
    g = c["gsc"]
    p1 = g["page_one"]
    t3 = g["top3"]
    if g["capped"]:  # Search Console returned its row limit, so these are lower bounds
        p1s, t3s = _n(p1 // 10 * 10) + "+", _n(t3 // 10 * 10) + "+"
    else:
        p1s, t3s = _n(p1), _n(t3)
    full = [m for m in g["monthly"] if m["days"] >= 28 and m["month"] + "-28" <= SC["data"]["data_through"]
            and not (g["first_day"] and m["month"] == g["first_day"][:7] and not g["first_day"].endswith("-01"))]
    first = g["first_day"]
    return {
        "clicks": _n(g["clicks"]), "prev_clicks": _n(g["prev_clicks"]),
        "impr": _n(g["impressions"]), "prev_impr": _n(g["prev_impressions"]),
        "pos": f"{g['position']:.1f}", "prev_pos": f"{g['prev_position']:.1f}",
        "page_one": p1s, "top3": t3s, "full_months": full,
        "first": first, "first_long": date_long(first) if first else "",
        # The previous window is a fair comparison only if the site had data before it started.
        "prev_ok": bool(first) and first <= SC["data"]["prev_window"][0],
        "has_data": g["impressions"] > 0,
    }


G = {k: _fmt(c) for k, c in SC_BY.items()}
EG, CL = G["sggarage"], G["cleanic"]


def stage(key):
    c, f = SC_BY[key], G[key]
    if not f["has_data"]:
        return "new"
    if f["prev_ok"] and c["gsc"]["position"] <= 20 and c["gsc"]["clicks"] >= 100:
        return "case"
    return "early"


def pill(key):
    c, f = SC_BY[key], G[key]
    if stage(key) == "new":
        return "Launched " + month_short(c["launched"])
    return "Since " + (date_short(f["first"]) if stage(key) == "early" and f["first"] > SC["data"]["window"][0] else month_short(f["first"][:7]))


def result_text(key, built_follows=False):
    """One honest sentence or two about a site's Google numbers, with the window stated."""
    c, f, g = SC_BY[key], G[key], SC_BY[key]["gsc"]
    if stage(key) == "new":
        return (f"Launched in {month_long(c['launched'])}. Search Console has no data for it yet, "
                "so there are no Google results to report." + (" Here is what we built." if built_follows else f" So far: {c['built'][-1]}."))
    if stage(key) == "case":
        return (f"{f['clicks']} clicks from Google in the 28 days to {THROUGH_SHORT} (up from {f['prev_clicks']} the 28 days before), "
                f"average position {f['pos']} (from {f['prev_pos']}), on page one for {f['page_one']} different searches.")
    if f["prev_ok"]:
        move = "up from" if g["impressions"] > g["prev_impressions"] else "compared with"
        pos = (f" Average position improved from {round(g['prev_position'])} to {round(g['position'])}."
               if g["position"] < g["prev_position"] else f" Average position {round(g['position'])}.")
        return (f"Shown on Google {f['impr']} times in the 28 days to {THROUGH_SHORT}, {move} {f['prev_impr']} the 28 days before.{pos} "
                f"On page one for {f['page_one']} searches. Still early.")
    if f["first"] > SC["data"]["window"][0]:
        days = (_d(SC["data"]["data_through"]) - _d(f["first"])).days + 1
        return (f"Google started showing it on {f['first_long']}. In its first {days} days: shown {f['impr']} times, "
                f"{f['clicks']} clicks, on page one for {f['page_one']} searches. Too early to call results.")
    return (f"Shown on Google {f['impr']} times in the 28 days to {THROUGH_SHORT}, on page one for {f['page_one']} searches. "
            "Still early.")


# Sentences reused on several pages (home, FAQ, industries, low-cost pages, /website/).
PROOF_BOTH = (f"In the 28 days to {THROUGH}, Edwin Garage got {EG['clicks']} clicks from Google with an average position of {EG['pos']}, "
              f"and Cleanic Detailing appeared on page one for {CL['page_one']} different searches, according to Google Search Console.")
PROOF_EG = f"Edwin Garage got {EG['clicks']} clicks from Google in the 28 days to {THROUGH}"
LIVE_NAMES = [c["name"] for c in SC["clients"]]
LIVE_COUNT_WORD = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"][len(LIVE_NAMES)] \
    if len(LIVE_NAMES) <= 12 else str(len(LIVE_NAMES))


# Portfolio growth: live sites per launch month (cumulative) plus the signed-up sites still being built.
GROWTH = [(m, sum(1 for c in SC["clients"] if c["launched"][:7] <= m)) for m in sorted({c["launched"][:7] for c in SC["clients"]})]
BUILDING = int(SC.get("pipeline", {}).get("building", 0))
GROWTH_AS_OF = date_long(SC.get("pipeline", {}).get("as_of", SC_UPDATED))
GROWTH_LINE = (" · ".join(f"{month_long(m) if i == 0 else month_long(m).split()[0]}: {n} live" for i, (m, n) in enumerate(GROWTH))
               + (f", plus {BUILDING} more being built" if BUILDING else "") + f" (as of {GROWTH_AS_OF})")


def names_list(names):
    names = list(names)
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def site_cards_html():
    """The compact card grid used on /website/ (thumbnail, name, what they do)."""
    return "\n".join(f"""          <a class="card site-card reveal" href="{c['url']}" target="_blank" rel="noopener">
            <span class="browser"><span class="browser-bar"><i></i><i></i><i></i><span>{c['domain']}</span></span><img src="{c['img']}" width="640" height="400" alt="{c['name']} website homepage ({c['domain']})" loading="lazy" decoding="async"></span>
            <h3>{c['name']}</h3><p>{c['industry']}</p>
          </a>""" for c in SC["clients"])


def months_rows(key):
    return [(month_long(m["month"]).split()[0], _n(m["clicks"]), _n(m["impressions"]), f"{m['position']:.1f}")
            for m in G[key]["full_months"]]


def query_rows(key):
    return [(q["query"], f"{q['position']:.1f}", _n(q["impressions"])) for q in SC_BY[key]["gsc"]["top_queries"]]


def top3_examples(key, n=2):
    qs = sorted([q for q in SC_BY[key]["gsc"]["top_queries"] if q["position"] <= 3], key=lambda q: -q["impressions"])[:n]
    return " and ".join(f"&ldquo;{q['query']}&rdquo;" for q in qs)


def clients_page():
    cards = []
    for c in SC["clients"]:
        k = c["key"]
        built = "".join(f"<li>{b}</li>" for b in c["built"])
        arts = f"<li>{_n(c['articles'])} articles published so far</li>" if c.get("articles") and stage(k) != "new" else ""
        links = f'<a class="card-link" href="{c["url"]}" target="_blank" rel="noopener">Visit {c["domain"]} ↗</a>'
        if c.get("case_study"):
            links += f' <a class="card-link" href="{c["case_study"]}">Read the case study →</a>'
        note = f'<p class="fine">{c["owner_note"]}</p>' if c.get("owner_note") else ""
        cards.append(f"""          <article class="card site-card reveal" id="{k}">
            <a class="browser" href="{c['url']}" target="_blank" rel="noopener"><span class="browser-bar"><i></i><i></i><i></i><span>{c['domain']}</span></span><img src="{c['img']}" width="640" height="400" alt="{c['name']} website homepage ({c['domain']})" loading="lazy" decoding="async"></a>
            <p class="pill">{pill(k)}</p>
            <h3>{c['name']}</h3><p><b>{c['industry']}</b></p>{note}
            <p>{result_text(k, built_follows=True)}</p>
            <ul class="ticks">{built}{arts}</ul>
            {links}
          </article>""")
    faq = [
        ("Are these real businesses?", f"Yes. Every website on this page is live on the business's own domain, so you can open it and check. Edwin Garage is our founder's own car workshop, where the system was first built. The others are businesses we build and run websites for."),
        ("Where do the Google numbers come from?", f"From Google Search Console, Google's own report of how a website performs in Google Search. We collect the final data automatically and don't edit it. The figures on this page cover the 28 days to {THROUGH} ({WINDOW}), compared with the 28 days before ({PREV_WINDOW})."),
        ("Why do some websites have no numbers?", "Google needs time to find and test a new website. A site launched this month has no Search Console data yet, so we show what we built instead of guessing. The numbers will appear here once Google has them."),
        ("How can it be good if it only costs S$20 a month?", "The price is low because a set of AI tools we designed does the daily SEO work that used to be billed by the hour, not because steps are skipped. The websites and numbers on this page are the proof, not a promise: results vary by business, and newer sites show smaller numbers."),
        ("How often is this page updated?", "We refresh it from Search Console regularly, and add new client websites once they are live on their own domain. The date of the data is always shown."),
    ]
    sites_ld = [{"@type": "ListItem", "position": i + 1,
                 "item": {"@type": "WebSite", "name": c["name"], "url": c["url"], "description": c["industry"]}}
                for i, c in enumerate(SC["clients"])]
    page("clients/index.html",
         "Client Websites &amp; Google Results | Page One Singapore",
         f"See the websites Page One Singapore built and runs for real Singapore businesses, with their Google Search Console numbers to {THROUGH_SHORT}. S$20 a month.",
         [{"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE + "/clients/",
           "name": "Client websites and results", "about": PROVIDER, "inLanguage": "en-SG", "dateModified": CLIENTS_UPDATED,
           "mainEntity": {"@type": "ItemList", "name": "Websites built and run by Page One Singapore",
                          "numberOfItems": len(SC["clients"]), "itemListElement": sites_ld}},
          {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}],
         hero("Clients", "Client websites",
              "S$20 a month, and here is what it has done for real Singapore businesses.",
              f"Every website below is live on the business's own domain. Open them, judge the design yourself, and read their Google numbers straight from Search Console, with data to {THROUGH}.", buttons=False) + """

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Cheap can still be good</p>
        <h2 class="reveal">A low price, with the numbers to back it</h2>
        <p class="section-lead reveal">S$20 a month is low because a set of AI tools we designed does the daily SEO work that used to be billed by the hour, not because steps are skipped. Here is what the same system has done. Last 28 days (""" + WINDOW + """), compared with the 28 days before.</p>
        <div class="reveal">""" + kpis([
            ("Edwin Garage: clicks from Google", EG["clicks"], f"Up from {EG['prev_clicks']} · average position {EG['pos']}"),
            ("Edwin Garage: searches on page one", EG["page_one"], f"{EG['top3']} in the top 3"),
            ("Cleanic Detailing: clicks from Google", CL["clicks"], f"Up from {CL['prev_clicks']} · average position {CL['pos']}"),
            ("Websites live", str(len(SC["clients"])), "Each on the business's own domain"),
        ]) + """</div>
        <p class="note reveal"><b>Portfolio growth:</b> """ + GROWTH_LINE + """. Only sites live on the business's own domain are counted as live.</p>
        <p class="note reveal">Results vary by business, and no one can guarantee rankings. Newer sites are shown too, with smaller numbers or none yet. <a class="link" href="/cheapest-seo-singapore/">Why it costs S$20 →</a></p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">The websites</p>
        <h2 class="reveal">""" + LIVE_COUNT_WORD.capitalize() + """ Singapore businesses, live today</h2>
        <p class="section-lead reveal">The established sites first, then the newer ones, shown honestly. Tap any screenshot to open the live website.</p>
        <div class="cards three site-cards" style="margin-top:32px">
""" + "\n".join(cards) + """
        </div>
        <p class="note reveal"><a class="card-link" href="/results/">See the full case studies →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">About these numbers</p>
        <h2 class="reveal">Questions about our clients</h2>
""" + "".join(f"""        <details><summary>{q}</summary><p>{a}</p></details>
""" for q, a in faq) + """      </div>
    </section>

""" + cta("Want your business on this page?", "Sign up at the introductory price, or check where your website stands today. No obligation."),
         crumb="Clients", updated=CLIENTS_UPDATED)

_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
_n_others = sum(1 for c in SC["clients"] if stage(c["key"]) != "case")
LIVE_COUNT_WORD_OTHERS = _WORDS[_n_others] if _n_others < len(_WORDS) else str(_n_others)


def _proof_bars():
    m = G["sggarage"]["full_months"]
    top = max(x["clicks"] for x in m)
    label = "; ".join(f"{month_long(x['month']).split()[0]} {_n(x['clicks'])}" for x in m)
    bars = "\n".join(
        f'            <div class="pb" style="--h:{(1 if x["clicks"] == top else round(x["clicks"] / top, 3))}" title="{month_long(x["month"])}: {_n(x["clicks"])} clicks">'
        f'<span>{_n(x["clicks"])}</span><i></i><small>{month_long(x["month"])[:3]}</small></div>' for x in m)
    ranks = sorted(SC_BY["sggarage"]["gsc"]["top_queries"], key=lambda q: q["position"])[:3]
    ranks_html = "\n".join(f'            <li><span>{q["query"]}</span><b>#{q["position"]:.1f}</b></li>' for q in ranks)
    return (f'          <div class="proof-bars" role="img" aria-label="Monthly clicks from Google: {label}">\n{bars}\n          </div>\n'
            f'          <ul class="proof-ranks" aria-label="Average Google position for example searches">\n{ranks_html}\n          </ul>')


def _marquee():
    one = lambda c, hidden: (f'        <a href="{c["url"]}" target="_blank" rel="noopener"'
                             + (' aria-hidden="true" tabindex="-1"' if hidden else "") + f'><span class="dot"></span>{c["name"]}</a>')
    return "\n".join([one(c, False) for c in SC["clients"]] + [one(c, True) for c in SC["clients"]])


def _g(key):
    return SC_BY[key]["gsc"]


def _kbar(a, b):
    """Two-row mini bar chart under a homepage KPI (decorative: the KPI text already says the same)."""
    top = max(a[1], b[1]) or 1
    row = lambda lab, v, cls: (f'<p><small>{lab}</small><i class="{cls}" style="--w:{round(v / top, 3)}"></i></p>')
    return f'<div class="kbar" aria-hidden="true">{row(a[0], a[1], "was")}{row(b[0], b[1], "now")}</div>'


HOME_TOKENS = {
    "{{PROOF_BOTH}}": PROOF_BOTH, "{{EG_PAGE_ONE}}": EG["page_one"], "{{EG_CLICKS}}": EG["clicks"], "{{EG_POS}}": EG["pos"], "{{EG_POS_FROM}}": (f' data-from="{EG["prev_pos"]}"' if float(EG["prev_pos"]) > float(EG["pos"]) else ""),
    "{{EG_LINK}}": f'<a class="link" href="{SC_BY["sggarage"]["url"]}" target="_blank" rel="noopener">Edwin Garage</a>',
    "{{CL_LINK}}": f'<a class="link" href="{SC_BY["cleanic"]["url"]}" target="_blank" rel="noopener">Cleanic Detailing</a>',
    "{{THROUGH_SHORT}}": THROUGH_SHORT, "{{WINDOW}}": WINDOW, "{{PROOF_BARS}}": _proof_bars(), "{{MARQUEE}}": _marquee(),
    "{{MARQUEE_LABEL}}": f"Already running for {len(SC['clients'])} Singapore businesses" + (f" · {BUILDING} more being built" if BUILDING else ""),
    "{{HOME_KPIS}}": "\n".join(
        f'          <div class="kpi"><div class="label">{l}</div><div class="value">{v}</div><div class="delta">{d}</div>{b}</div>' for l, v, d, b in [
            ("Edwin Garage: clicks from Google", EG["clicks"], f"Up from {EG['prev_clicks']} · average position {EG['pos']}",
             _kbar(("Before", _g("sggarage")["prev_clicks"]), ("Now", _g("sggarage")["clicks"]))),
            ("Edwin Garage: searches on page one", EG["page_one"], f"{EG['top3']} in the top 3",
             _kbar(("Page one", _g("sggarage")["page_one"]), ("Top 3", _g("sggarage")["top3"]))),
            ("Cleanic Detailing: clicks from Google", CL["clicks"], f"Up from {CL['prev_clicks']} the 28 days before",
             _kbar(("Before", _g("cleanic")["prev_clicks"]), ("Now", _g("cleanic")["clicks"]))),
            ("Cleanic Detailing: searches on page one", CL["page_one"], f"{CL['top3']} in the top 3",
             _kbar(("Page one", _g("cleanic")["page_one"]), ("Top 3", _g("cleanic")["top3"])))]),
}


def fill_home(html):
    for k, v in HOME_TOKENS.items():
        html = html.replace(k, v)
    assert "{{" not in html, "unfilled token in home_body.html"
    return html


def llms_sections():
    """The Results and Websites sections of llms.txt (owned by the Bluehost Bridge publisher).
    Written to pageone-site/bridge/ at build time; bridge/update_pins.mjs copies them into pageoneArticles.ts."""
    s, e = SC["data"]["window"]
    ps, pe = SC["data"]["prev_window"]
    lines = [f"## Results (Google Search Console, 28 days {date_long(s).rsplit(' ', 1)[0]} to {date_long(e)}, "
             f"compared with {date_long(ps).rsplit(' ', 1)[0]} to {date_long(pe)})"]
    new = []
    for c in SC["clients"]:
        k, f, g = c["key"], G[c["key"]], c["gsc"]
        st = stage(k)
        if st == "new":
            new.append(c)
            continue
        if st == "case":
            lines.append(f"- {c['name']} ({c['domain']}): {f['clicks']} clicks from Google (up from {f['prev_clicks']}), average position "
                         f"{f['pos']} (from {f['prev_pos']}), on page one for {f['page_one']} different searches. "
                         f"Search Console data starts {f['first_long']}.")
        elif f["first"] > SC["data"]["window"][0]:
            lines.append(f"- {c['name']} ({c['domain']}): Search Console data starts {f['first_long']}; shown on Google {f['impr']} times, "
                         f"{f['clicks']} clicks so far. Too early to report results.")
        elif f["prev_ok"]:
            lines.append(f"- {c['name']} ({c['domain']}): shown on Google {f['impr']} times (up from {f['prev_impr']}), "
                         f"on page one for {f['page_one']} searches. Still early.")
        else:
            lines.append(f"- {c['name']} ({c['domain']}): shown on Google {f['impr']} times, on page one for {f['page_one']} searches. "
                         f"Search Console data starts {f['first_long']}. Still early.")
    if new:
        lines.append("- " + names_list([f"{c['name']} ({c['domain']})" for c in new]) + ": launched "
                     + names_list(sorted({month_long(c["launched"]) for c in new})) + ", no Search Console data yet.")
    lines += ["- Full case studies: https://pageonesingapore.com/results/",
              "- Every client website with its numbers: https://pageonesingapore.com/clients/",
              "- Low price, real results: S$20 a month is low because a set of AI tools we designed does the daily SEO work that used to be billed by the hour; "
              "the numbers above come from the same system."]
    growth = ", ".join(f"{n} by {month_long(m)}" for m, n in GROWTH)
    sites = ["## Websites we run",
             f"- As of {GROWTH_AS_OF}, Page One runs {len(SC['clients'])} live client websites, each on the business's own domain "
             f"(live count: {growth})" + (f", and is building {BUILDING} more for clients who have signed up." if BUILDING else ".")] + [f"- [{c['name']}]({c['url']}): {c['industry']}" + (f" (launched {month_long(c['launched'])})" if stage(c['key']) == "new" else "")
                                      for c in SC["clients"]] + ["- All client websites with screenshots and dated results: https://pageonesingapore.com/clients/"]
    out = os.path.join(HERE, "..", "bridge")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "llms-results.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    open(os.path.join(out, "llms-websites.md"), "w", encoding="utf-8").write("\n".join(sites) + "\n")
