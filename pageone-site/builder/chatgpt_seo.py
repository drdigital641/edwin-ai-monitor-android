# /chatgpt-seo-singapore/: the owner page for "ChatGPT SEO Singapore" (service intent). Learned from First Page Digital
# (20 Oct 2026), which has a page per AI engine. Different intents, linked both ways: /seo-aeo-geo-singapore/ (all three
# together; its GEO card links here) and the DIY article /articles/how-to-get-my-business-recommended-by-chatgpt-singapore/.
# Claims rule (18 Oct 2026): never promise being found on or recommended by ChatGPT. No one controls AI answers.
# Run from build.py (exec) after seo_aeo_geo.py.

CG_URL = "/chatgpt-seo-singapore/"
CG_ARTICLE = "/articles/how-to-get-my-business-recommended-by-chatgpt-singapore/"

CG_FAQ = [
    ("What is ChatGPT SEO?",
     "ChatGPT SEO means making your business easy for ChatGPT to find, read and describe correctly when someone asks it a question with web search on. "
     "It is part of GEO, generative engine optimisation. In practice it is the same groundwork as good SEO, plus a few AI-specific steps: allowing OpenAI's search crawler, connecting Bing, and publishing clear facts AI tools can quote."),
    ("How does ChatGPT decide which businesses to mention?",
     "When ChatGPT searches the web, it reads pages from its own crawler (OAI-SearchBot) and from search partners such as Bing, then writes an answer and links its sources. "
     "Pages that answer the question directly, state facts like price and area clearly, and are mentioned by other websites are easier for it to use. OpenAI does not publish a ranking formula, and no one can control what it says."),
    ("Can you guarantee ChatGPT will recommend my business?",
     "No, and no honest provider can. ChatGPT's answers change with the question, the user and the day. What we can do is make sure nothing stops ChatGPT from finding and understanding your site, and keep adding pages that answer what your customers ask."),
    ("How much does ChatGPT SEO cost with Page One?",
     "It is included in the S$50 a month plan together with Google SEO, with no setup fee and no contract. There is no separate ChatGPT package."),
    ("How do I check if ChatGPT knows my business?",
     "Open ChatGPT, turn on search, and ask the way a customer would, for example \"best aircon servicing in Tampines\" or \"what does [your business name] do?\". See whether you are named, and whether the details are right. Try a few different wordings, because answers vary."),
    ("Does this help with Gemini, Perplexity and Copilot too?",
     "Yes. The same steps (clear facts, structured data, crawlers allowed, Bing and Google connected, consistent details everywhere) help every AI assistant that searches the web. Copilot uses Bing directly, and Gemini draws on Google."),
]

_CG_STEPS = [
    ("1", "Let ChatGPT in", "Your robots.txt allows OAI-SearchBot, the crawler ChatGPT search uses. Many sites block them by accident, and a blocked site can't be read.", ["robots.txt", "OAI-SearchBot"]),
    ("2", "Be in Bing", "ChatGPT search draws on Bing among its sources, so your site is verified in Bing Webmaster Tools and Bing is told about new and changed pages every day.", ["Bing Webmaster Tools", "IndexNow"]),
    ("3", "State the facts plainly", "Who you are, what you do, where, your hours and prices written where they are easy to quote, and marked up as structured data so machines read them correctly.", ["Structured data (Schema.org)", "llms.txt"]),
    ("4", "Answer real questions", "Customers' questions as headings, with a short direct answer under each. A new article every day, each aimed at a different real search.", ["Answer-first content", "AEO"]),
    ("5", "Keep your details the same everywhere", "Name, address, phone and services match on your website, Google Business Profile and listings, so AI tools don't get mixed messages.", ["Entity consistency", "Google Business Profile"]),
    ("6", "Check the AI crawlers can reach you", "We watch for OpenAI's crawler on your site and fix anything that blocks it, like a firewall rule or a broken page.", ["Crawler monitoring"]),
]

_cg_steps_html = "\n".join(
    f'          <div class="card reveal"><div class="icon">{n}</div><h3>{t}</h3><p>{p}</p><p class="tech"><b>Technical name</b>{_terms(terms)}</p></div>'
    for n, t, p, terms in _CG_STEPS)

page("chatgpt-seo-singapore/index.html",
     "ChatGPT SEO Singapore: Help ChatGPT Find Your Business | S$50/month",
     "ChatGPT SEO for Singapore small businesses: how ChatGPT search picks sources, the six things we set up so it can find and describe you, and how to check. Included in S$50/month.",
     [service("ChatGPT SEO (generative engine optimisation)", CG_URL,
              "Helping ChatGPT and other AI assistants find, read and correctly describe a Singapore business: OpenAI crawlers allowed, Bing connected, "
              "structured data, llms.txt, answer-first content and consistent business details. Included with Google SEO in the S$50 a month plan.", "50"),
      _faq_ld(CG_FAQ)],
     hero("ChatGPT SEO", "SEO for ChatGPT search",
          "ChatGPT SEO: help ChatGPT find your business, and describe it right.",
          "More customers now ask ChatGPT \"who is good for this near me?\" before they search Google. "
          "We set up your website so ChatGPT and other AI assistants can find it, read it and quote it correctly, as part of the same S$50 a month plan as your Google SEO.",
          '<p class="hero-price"><b>S$50</b>/month · <span class="intro-tag">Register by 31 Dec 2026</span> · Google and ChatGPT together</p>') + f"""

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Short answer</p>
        <h2 class="reveal">How does ChatGPT pick which businesses to name?</h2>
        <p class="reveal">When it searches the web, ChatGPT reads pages from its own crawler and from search partners such as Bing, then writes an answer and links the sources it used. It favours pages that answer the question directly, state facts clearly, and are backed up by other websites. So ChatGPT SEO is mostly good SEO done carefully, plus making sure AI crawlers are let in and Bing knows your site.</p>
        <p class="reveal">No one controls what ChatGPT says, so we don't promise mentions. We make sure nothing stops it from finding and understanding you.</p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">What we set up</p>
        <h2 class="reveal">Six things that help ChatGPT find and describe you</h2>
        <div class="cards three" style="margin-top:32px">
{_cg_steps_html}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Google or ChatGPT?</p>
        <h2 class="reveal">You don't have to choose</h2>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th></th><th>Google SEO</th><th>ChatGPT SEO</th></tr></thead>
            <tbody>
              <tr><th>Where customers see you</th><td>Google results and Google Maps</td><td>ChatGPT's written answer and its source links</td></tr>
              <tr><th>What it reads</th><td>Your pages, via Googlebot</td><td>Your pages, via OAI-SearchBot and search partners such as Bing</td></tr>
              <tr><th>What helps most</th><td>Relevant pages, good structure, reviews, links</td><td>The same, plus direct answers, clear facts and mentions on other sites</td></tr>
              <tr><th>How to measure</th><td>Google Search Console (connected for you)</td><td>No official report yet: ask ChatGPT the way a customer would</td></tr>
            </tbody>
          </table>
        </div>
        <p class="reveal" style="margin-top:20px">The groundwork is shared, which is why both fit in one plan. {PROOF_EG}, according to Google Search Console. Results vary by business, so we don't guarantee rankings or AI mentions.</p>
        <p class="note reveal"><a class="card-link" href="/seo-aeo-geo-singapore/">SEO, AEO and GEO explained →</a> <a class="card-link" href="/results/">See the results →</a> <a class="card-link" href="{CG_ARTICLE}">Doing it yourself? Read the guide →</a></p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">ChatGPT SEO: your questions, answered</h2>
""" + "\n".join(f'        <details class="reveal"><summary>{q}</summary><p>{a}</p></details>' for q, a in CG_FAQ) + """
      </div>
    </section>

""" + cta("Want ChatGPT and Google to find you?", "S$50 a month, no contract. Check your website free first, or chat with Edwin on WhatsApp."),
     crumb="ChatGPT SEO", updated="2026-10-21")
