# /seo-aeo-geo-singapore/: the owner page for "SEO AEO GEO Singapore" searches, angled as "all three together".
# The homepage shows only a three-card strip that links here; the detail and the FAQs live on this page.
# Different intents, linked both ways: /ai-seo-vs-traditional-seo/ (why AI-run SEO costs less) and
# /seo-services-singapore/ (agency vs in-house vs S$50). Run from build.py (exec) after managed.py.
# Facts rule: only what every Page One site already gets; no promise that Google or an AI tool will show anyone.

SAG_URL = "/seo-aeo-geo-singapore/"

SAG_FAQ = [
    ("What is AEO (answer engine optimisation)?",
     "AEO, answer engine optimisation, means shaping your pages so Google can lift a short answer straight from them into a featured snippet, a People Also Ask box or an AI Overview. We do it by putting customers' real questions in headings and answering each one in two or three plain sentences, marked up with FAQ structured data."),
    ("What is GEO (generative engine optimisation)?",
     "GEO, generative engine optimisation, means helping AI assistants such as ChatGPT, Gemini, Perplexity and Copilot find your business, describe it correctly and name it as a source. We publish clear business facts and an llms.txt summary, allow AI crawlers in robots.txt, connect your site to Bing and Google, and keep your details consistent. No one can guarantee a mention."),
    ("Do I need SEO, AEO and GEO?",
     "Most small businesses benefit from all three, because customers now look in three places: Google's results, the answers Google shows above them, and AI assistants. The three share the same groundwork, so doing them together costs less than doing them separately. With Page One, all three are part of the S$50 a month plan, with no setup fee."),
    ("How do I know it's working?",
     "Google Search Console is connected to your site from day one, so you can see how often you appear on Google, what people searched and how many clicked. AI assistants have no official report yet, so the simplest check is to ask ChatGPT or Perplexity about your type of business in your area and see who is named."),
]

_SAG_ITEMS = [
    ("seo", "🔍", "SEO: rank on Google",
     "Search engine optimisation. Getting your website into Google Search and Google Maps when customers type what you do and where, like \"aircon repair Tampines\".",
     ["Your pages use the words customers actually search for",
      "Google Business Profile, Google Search Console and Bing set up",
      "Fast, mobile-friendly pages, with a technical audit every day and problems fixed",
      "A new article every day, each aimed at a different real search from your own Search Console data"],
     ["Keyword research", "Local SEO", "Technical SEO"]),
    ("aeo", "💬", "AEO: be the answer Google shows first",
     "Answer engine optimisation. Being the short answer Google lifts out and shows above the usual results: featured snippets, People Also Ask boxes and AI Overviews.",
     ["Customers' real questions used as headings",
      "A short, direct answer right under each question",
      "FAQ structured data, so Google can read each question and answer",
      "Plain facts (price, area, hours) written where they are easy to quote"],
     ["Featured snippets", "People Also Ask", "FAQ schema"]),
    ("geo", "🤖", "GEO: get named by ChatGPT and AI",
     "Generative engine optimisation. Helping AI assistants such as ChatGPT, Gemini, Perplexity and Copilot find your business, describe it correctly and cite it as a source.",
     ["Clear business facts marked up with structured data",
      "An llms.txt summary written for AI tools",
      "AI crawlers allowed in your robots.txt",
      "Bing connected (ChatGPT search and Copilot use Bing), and your details kept the same everywhere",
      'More on this: <a class="link" href="/chatgpt-seo-singapore/">ChatGPT SEO →</a>'],
     ["Structured data (Schema.org)", "llms.txt", "Bing Webmaster Tools"]),
]


def _sag_card(k, e, t, what, does, terms):
    lis = "".join(f"<li>{x}</li>" for x in does)
    return (f'          <div class="card reveal" id="{k}"><div class="emoji" aria-hidden="true">{e}</div><h3>{t}</h3>'
            f'<p><b>What it is.</b> {what}</p><p><b>What we do:</b></p><ul class="ticks">{lis}</ul>'
            f'<p class="tech"><b>Technical name</b>{_terms(terms)}</p></div>')


_sag_cards = "\n".join(_sag_card(*x) for x in _SAG_ITEMS)

page("seo-aeo-geo-singapore/index.html",
     "SEO, AEO and GEO Singapore: All Three from S$50/month",
     "SEO for Google, AEO for Google's answers and AI Overviews, GEO for ChatGPT, Gemini and Perplexity: what each means and how we do all three for S$50/month.",
     [service("SEO, AEO and GEO", SAG_URL,
              "Search engine optimisation (Google Search and Maps), answer engine optimisation (featured snippets, People Also Ask, AI Overviews) "
              "and generative engine optimisation (ChatGPT, Gemini, Perplexity, Copilot), done together for Singapore small businesses.", "50"),
      _faq_ld(SAG_FAQ)],
     hero("SEO, AEO and GEO", "SEO + AEO + GEO",
          "SEO, AEO and GEO: found on Google, in its answers and in AI assistants.",
          "Customers now look in three places: Google's results, the short answers Google shows above them, and AI assistants like ChatGPT. "
          "Page One works on all three at the same time, for S$50 a month, with no setup fee and no contract.",
          '<p class="hero-price"><b>S$50</b>/month · <span class="intro-tag">Register by 31 Dec 2026</span> · all three together</p>') + f"""

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">The three, in plain words</p>
        <h2 class="reveal">What each one is, and what we do for it</h2>
        <div class="cards three plain-cards" style="margin-top:32px">
{_sag_cards}
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Why together</p>
        <h2 class="reveal">One set of groundwork, three places to be found</h2>
        <p class="reveal">Clear pages, honest business facts, structured data and a new article every day help Google rank you, give Google a short answer to show, and give AI assistants something reliable to quote. Doing them together means nothing is done twice, which is part of why it fits in S$50 a month.</p>
        <p class="reveal">{PROOF_BOTH} Results vary by business, so we don't guarantee rankings or AI mentions.</p>
        <p class="note reveal"><a class="card-link" href="/results/">See the results →</a> <a class="card-link" href="/managed-website-singapore/">What fully managed covers →</a> <a class="card-link" href="/pricing/">Full pricing →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">SEO, AEO and GEO: your questions, answered</h2>
""" + "\n".join(f'        <details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in SAG_FAQ) + """
        <p class="note reveal">Wondering why it costs so little? See <a class="link" href="/ai-seo-vs-traditional-seo/">AI SEO vs traditional SEO</a>. Comparing providers? See <a class="link" href="/seo-services-singapore/">agency vs in-house vs S$50 a month</a>.</p>
      </div>
    </section>

""" + cta("Want to be found in all three places?", "Sign up at S$50 a month, or chat with Edwin on WhatsApp first. No obligation."),
     crumb="SEO, AEO and GEO", updated="2026-10-19")
