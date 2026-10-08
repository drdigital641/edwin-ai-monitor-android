import json, os, sys

ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://pageonesingapore.com"
WA = "6589976612"
WA_DISPLAY = "+65 8997 6612"
WA_LINK = f"https://wa.me/{WA}?text=Hi%20Page%20One%20Singapore%2C%20I%27d%20like%20to%20know%20more."
UPDATED = "2026-10-08"
BIZ_ID = SITE + "/#business"

NAV = [
    ("/get-found/", "Get Found"),
    ("/seo-boost/", "SEO Boost"),
    ("/pricing/", "Pricing"),
    ("/#stories", "Clients"),
    ("/about/", "About"),
    ("/faq/", "FAQ"),
]

WA_ICON = '<svg viewBox="0 0 24 24" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.8 2.3 1 2.5c.1.2 1.7 2.6 4.1 3.6 1.5.7 2.1.7 2.9.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'

PROVIDER = {"@id": BIZ_ID}


def crumbs_ld(name, url):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": name, "item": SITE + url},
        ],
    }


def page(path, title, desc, schemas, body, crumb=None, robots="index, follow, max-image-preview:large"):
    if path == "index.html":
        current = "/"
    elif path.endswith("index.html"):
        current = "/" + path[: -len("index.html")]
    else:
        current = "/" + path
    if crumb:
        schemas = schemas + [crumbs_ld(crumb, current)]
    if "noindex" not in robots:
        schemas = schemas + [{
            "@context": "https://schema.org", "@type": "WebPage", "url": SITE + current, "name": title.replace("&amp;", "&"),
            "description": desc, "inLanguage": "en-SG", "isPartOf": {"@id": SITE + "/#website"},
            "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/images/og.png", "width": 600, "height": 315},
            "dateModified": UPDATED}]
    nav = "\n".join(
        f'        <a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a>'
        for href, label in NAV
    )
    ld = "\n".join(
        '  <script type="application/ld+json">\n' + json.dumps(s, ensure_ascii=False, indent=2) + "\n  </script>"
        for s in schemas
    )
    html = f"""<!doctype html>
<html lang="en-SG">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="{robots}">
  <link rel="canonical" href="{SITE}{current}">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-48x48.png" type="image/png" sizes="48x48">
  <link rel="icon" href="/icon-192.png" type="image/png" sizes="192x192">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Page One Singapore">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{SITE}{current}">
  <meta property="og:image" content="{SITE}/images/og.png">
  <meta property="og:image:width" content="600">
  <meta property="og:image:height" content="315">
  <meta property="og:image:alt" content="Page One Singapore: get found on Google and AI search from S$20 a month">
  <meta property="og:locale" content="en_SG">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#060b18">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css?v=5">
  <script>document.documentElement.classList.add("js");</script>
{ld}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="logo" href="/" aria-label="Page One Singapore home">
        <span class="logo-mark">1</span><span>Page One <b>Singapore</b></span>
      </a>
      <nav class="nav" id="nav" aria-label="Main">
{nav}
      </nav>
      <a class="btn btn-small" href="/#check">Free check</a>
      <button class="menu-btn" id="menu-btn" type="button" aria-label="Menu" aria-expanded="false" aria-controls="nav">☰</button>
    </div>
  </header>

  <main id="main">
{body}
  </main>

  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <a class="logo" href="/"><span class="logo-mark">1</span><span>Page One <b>Singapore</b></span></a>
        <p>Google + AI visibility for Singapore businesses. Island-wide, from S$20 a month.</p>
        <p><a class="footer-wa" href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp {WA_DISPLAY}</a><br><span>24/7 · no obligation to discuss</span></p>
      </div>
      <div>
        <h2>Services</h2>
        <a href="/get-found/">Get Found</a>
        <a href="/seo-boost/">SEO Boost</a>
        <a href="/pricing/">Pricing</a>
        <a href="/report.html">Sample report</a>
      </div>
      <div>
        <h2>Company</h2>
        <a href="/about/">About</a>
        <a href="/#stories">Clients</a>
        <a href="/articles/">Articles</a>
        <a href="/faq/">FAQ</a>
        <a href="/contact/">Contact</a>
      </div>
      <div>
        <h2>Legal</h2>
        <a href="/privacy/">Privacy policy</a>
        <a href="/terms/">Terms of service</a>
      </div>
    </div>
    <div class="wrap footer-bottom">
      <p class="fine">© <span id="year">2026</span> Page One Singapore. All rights reserved.</p>
    </div>
  </footer>

  <a class="wa-float" id="wa-float" href="/#check" aria-label="Chat with us on WhatsApp">
    {WA_ICON}
  </a>

  <script src="/main.js?v=4" defer></script>
</body>
</html>
"""
    out = os.path.join(ROOT, path)
    if os.path.dirname(path):
        os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)


def service(name, url, desc, price):
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "url": SITE + url,
        "description": desc,
        "provider": PROVIDER,
        "areaServed": {"@type": "Country", "name": "Singapore"},
        "image": SITE + "/images/og.png",
        "offers": {"@type": "Offer", "price": price, "priceCurrency": "SGD"},
    }


def cta(title="Not sure where you stand?", text="Get a free Google + AI visibility check on WhatsApp. No obligation to discuss further. We're on WhatsApp 24/7."):
    return f"""    <section class="cta-band">
      <div class="wrap">
        <h2>{title}</h2>
        <p>{text}</p>
        <a class="btn" href="/#check">Get my free visibility check</a>
      </div>
    </section>"""


def hero(crumb, eyebrow, h1, lead, price_html="", buttons=True):
    btns = """
        <div class="cta-row">
          <a class="btn" href="/#check">Get my free visibility check</a>
          <a class="btn btn-ghost" href="/pricing/">See pricing</a>
        </div>""" if buttons else ""
    eb = f'\n        <p class="eyebrow"><span class="live" aria-hidden="true"></span>{eyebrow}</p>' if eyebrow else ""
    pr = f"\n        {price_html}" if price_html else ""
    return f"""    <section class="page-hero">
      <span class="glow glow-1" aria-hidden="true"></span>
      <span class="glow glow-2" aria-hidden="true"></span>
      <div class="wrap">
        <p class="crumbs"><a href="/">Home</a> / {crumb}</p>{eb}
        <h1>{h1}</h1>
        <p class="lead">{lead}</p>{pr}{btns}
      </div>
    </section>"""


GET_FOUND = """<ul class="ticks">
              <li>Google Business Profile set up and completed</li>
              <li>Google Search Console and Bing Webmaster connected (Bing feeds ChatGPT search)</li>
              <li>Business details marked up so Google and AI assistants can read them</li>
              <li><code>llms.txt</code> and sitemap so AI tools and search engines find every page</li>
              <li>Fast hosting, SSL padlock and a WhatsApp chat button</li>
            </ul>"""

# ---------- Get Found ----------
page("get-found/index.html",
     "Get Found Plan: Website or SEO Landing Page | Page One SG",
     "Our S$20/month basic plan. No website? We build one. Have one? We add an SEO landing page, set up for Google and AI search. No setup fee or contract.",
     [service("Get Found basic subscription", "/get-found/",
              "A website on the client's own domain, or an SEO landing page on a subdomain of their existing website, set up for Google Search, Google Maps and AI assistants.", "20")],
     hero("Get Found", "Basic subscription",
          "Get Found: your shopfront on Google and AI.",
          "One simple plan. Whether you have a website or not, we set you up to be found on Google Search, Google Maps and AI assistants.",
          '<p class="hero-price"><b>S$20</b>/month · no setup fee · no contract</p>') + """

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Which describes you?</p>
        <h2 class="reveal">Same plan, either way</h2>
        <div class="cards two" style="margin-top:32px">
          <div class="card reveal">
            <p class="pill">No website yet</p>
            <h3>We build your website</h3>
            <p>A fast, mobile-friendly site on your own domain. The domain is registered in your name, so you always own it (usually S$15–30 a year, paid directly).</p>
          </div>
          <div class="card reveal">
            <p class="pill">Already have a website</p>
            <h3>We add a landing page</h3>
            <p>Keep your current site exactly as it is. We build an SEO landing page on a subdomain like <code>go.yourbrand.com</code>. You just add one DNS record.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap split">
        <div class="reveal">
          <p class="kicker">What you get</p>
          <h2>Everything you need to be found</h2>
          <ul class="ticks">
            <li>Your website or landing page, written so customers understand what you do in seconds</li>
            <li>Works on phones first, because that's where your customers search</li>
            <li>WhatsApp button on every page, so enquiries come straight to you</li>
            <li>Small text and photo changes when you need them</li>
          </ul>
        </div>
        <div class="panel reveal" style="background:#fff">
          <h3>Plus the Google + AI setup</h3>
          """ + GET_FOUND + """
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">How it works</p>
        <h2 class="reveal">Live within 7 days</h2>
        <ol class="steps" style="margin-top:72px">
          <li class="reveal"><span>1</span><h3>Free visibility check</h3><p>We show you where you stand on Google, Maps and AI today. No obligation.</p></li>
          <li class="reveal"><span>2</span><h3>Tell us about your business</h3><p>A short WhatsApp chat: what you do, where, and a few photos.</p></li>
          <li class="reveal"><span>3</span><h3>We build and launch</h3><p>Your site or landing page goes live, connected to Google, Maps and Bing.</p></li>
        </ol>
        <div class="price-strip reveal">
          <p><b>S$20/month</b> · no setup fee · cancel anytime</p>
          <a class="card-link" href="/seo-boost/">Want faster results? Add SEO Boosts →</a>
        </div>
      </div>
    </section>

""" + cta(), crumb="Get Found")


def redirect(path, target):
    out = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(f"""<!doctype html>
<html lang="en-SG">
<head>
  <meta charset="utf-8">
  <title>Moved to Get Found | Page One Singapore</title>
  <link rel="canonical" href="{SITE}{target}">
  <meta http-equiv="refresh" content="0; url={target}">
  <meta name="robots" content="noindex, follow">
</head>
<body>
  <p>This page has moved to <a href="{target}">Get Found</a>.</p>
</body>
</html>
""")


redirect("new-website/index.html", "/get-found/")
redirect("landing-page/index.html", "/get-found/")

# ---------- SEO Boost ----------
page("seo-boost/index.html",
     "SEO Boost: S$10 Top-up for Faster Results | Page One SG",
     "An optional S$10 SEO Boost: one full round of Google and AI visibility improvements, with a before/after report. Top up anytime by WhatsApp.",
     [service("SEO Boost (optional top-up)", "/seo-boost/",
              "One full round of Google and AI search visibility improvements with a before/after report. Optional, topped up anytime.", "10")],
     hero("SEO Boost", "Optional top-up",
          "Want faster results? Add an SEO Boost.",
          "Your S$20 plan keeps you visible. Each SEO Boost is an extra round of improvements that helps you climb faster, with a report of exactly what changed.",
          '<p class="hero-price"><b>S$10</b>/boost · top up anytime</p>') + """

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">What's in one Boost</p>
        <h2 class="reveal">Check, improve, report</h2>
        <div class="cards three" style="margin-top:32px">
          <div class="card reveal"><div class="icon">1</div><h3>Check</h3><p>Where you rank on Google and Maps for your main searches, and whether ChatGPT, Gemini and Perplexity mention you.</p></div>
          <div class="card reveal"><div class="icon">2</div><h3>Improve</h3><p>New content and FAQs, page fixes, and a Google Business Profile post, aimed at the searches that matter.</p></div>
          <div class="card reveal"><div class="icon">3</div><h3>Report</h3><p>A before/after report: what was done, what improved, and what's planned next.</p></div>
        </div>
        <p class="note reveal"><a class="card-link" href="/report.html">See a sample report →</a></p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap split">
        <div class="reveal">
          <p class="kicker">How often?</p>
          <h2>As many or as few as you like</h2>
          <p class="section-lead" style="margin-bottom:0">No package to commit to. Most businesses start with 1 or 2 a month and add more when they want to push harder, for example before a busy season.</p>
        </div>
        <div class="panel reveal" style="background:#fff">
          <h3>Topping up</h3>
          <ul class="ticks">
            <li>S$10 per Boost</li>
            <li>Top up by WhatsApp, anytime, 24/7</li>
            <li>Works on top of your Get Found plan</li>
            <li>Rankings aren't guaranteed, but every Boost is documented</li>
          </ul>
          <a class="card-link" href="/pricing/">Work out your monthly cost →</a>
        </div>
      </div>
    </section>

""" + cta("Start with your free check", "Before you spend anything, see where you stand on Google, Maps and ChatGPT. No obligation to discuss further."),
     crumb="SEO Boost")

# ---------- Pricing ----------
page("pricing/index.html",
     "Pricing: From S$20/month, No Setup Fee | Page One Singapore",
     "Simple pricing for Google and AI visibility in Singapore. Get Found plan S$20/month. Optional SEO Boosts S$10 each. No setup fee, no contract.",
     [{"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Page One Singapore pricing", "url": SITE + "/pricing/",
       "itemListElement": [
           {"@type": "Offer", "name": "Get Found basic subscription (website or landing page + Google & AI visibility setup)", "price": "20", "priceCurrency": "SGD",
            "url": SITE + "/get-found/", "seller": PROVIDER,
            "priceSpecification": {"@type": "UnitPriceSpecification", "price": "20", "priceCurrency": "SGD", "unitCode": "MON"}},
           {"@type": "Offer", "name": "SEO Boost (optional top-up) with before/after report", "price": "10", "priceCurrency": "SGD",
            "url": SITE + "/seo-boost/", "seller": PROVIDER}]}],
     hero("Pricing", "No setup fee · No contract · Cancel anytime",
          "Simple pricing. Start at S$20.",
          "One monthly plan, plus optional SEO Boosts when you want faster results. Sign up and pay over WhatsApp.", buttons=False) + """

    <section class="section">
      <div class="wrap">
        <div class="pricing">
          <div class="price-card reveal">
            <p class="pill">Basic subscription</p>
            <h2 class="h3">Get Found</h2>
            <p class="price"><span>S$20</span>/month</p>
            <ul class="ticks">
              <li><a href="/get-found/">Your own website <em>or</em> a landing page on your subdomain</a></li>
              <li>Google Business Profile setup</li>
              <li>Google + Bing + AI visibility setup</li>
              <li>Hosting, SSL, WhatsApp button</li>
              <li>No setup fee · cancel anytime</li>
            </ul>
          </div>
          <div class="price-card accent reveal">
            <p class="pill">Optional top-up</p>
            <h2 class="h3">SEO Boost</h2>
            <p class="price"><span>S$10</span>/boost</p>
            <ul class="ticks">
              <li>Check Google, Maps &amp; AI visibility</li>
              <li>Make improvements: content, FAQs, fixes, Google posts</li>
              <li>Before/after report: what's done, what's next</li>
              <li>Optional: for faster results, top up anytime</li>
            </ul>
            <a class="link" href="/seo-boost/">How SEO Boost works →</a>
          </div>
          <form class="calc reveal" id="calc" aria-labelledby="calc-title">
            <h2 class="h3" id="calc-title">Your monthly cost</h2>
            <fieldset>
              <legend>SEO Boosts this month (optional)</legend>
              <label><input type="radio" name="runs" value="0"> No Boost <small>base plan</small></label>
              <label><input type="radio" name="runs" value="1"> 1 Boost <small>steady</small></label>
              <label><input type="radio" name="runs" value="2" checked> 2 Boosts <small>faster</small></label>
              <label><input type="radio" name="runs" value="4"> 4 Boosts <small>fastest</small></label>
            </fieldset>
            <div class="total" aria-live="polite">
              <span>Total</span>
              <strong id="calc-total">S$40</strong><span>/month</span>
            </div>
            <p class="calc-break" id="calc-break">S$20 Get Found + 2 × S$10 Boosts</p>
            <a class="btn btn-block" href="/#check">Start with a free check</a>
          </form>
        </div>
        <div class="split" style="margin-top:56px">
          <div class="panel reveal">
            <h2 class="h3">How payment works</h2>
            <p>Message us on WhatsApp, 24/7. We confirm what you need, then send payment details for your first month. Boosts are topped up the same way.</p>
          </div>
          <div class="panel reveal">
            <h2 class="h3">Your domain</h2>
            <p>A new domain is registered in your name and paid by you directly, usually S$15–30 a year. If you cancel, you keep it.</p>
          </div>
        </div>
      </div>
    </section>

""" + cta(), crumb="Pricing")

# ---------- FAQ ----------
FAQS = [
    ("Is there a setup fee or contract?", "No. There's no setup fee and no minimum contract. You pay S$20 a month in advance and can cancel anytime."),
    ("Is the free visibility check really free?", "Yes. We check how you show up on Google, Google Maps and ChatGPT and send you the results on WhatsApp. There's no obligation to discuss or buy anything afterwards."),
    ("When can I reach you?", "Anytime. Our WhatsApp support runs 24/7 on " + WA_DISPLAY + "."),
    ("How do I sign up and pay?", "Message us on WhatsApp. We'll confirm what you need, then send you the payment details for your first month. SEO Boosts are topped up the same way."),
    ("I already have a website. Do I need to change it?", "No. You give us a subdomain such as go.yourbrand.com and we build a separate SEO landing page there. Your current website stays exactly as it is."),
    ("What is an SEO Boost?", "An optional S$10 top-up for faster results. Each Boost is one full improvement round: we check your Google and AI visibility, make improvements, and send a before/after report of what was done and what's next. Your S$20 plan works without it."),
    ("How do you help me show up in ChatGPT and other AI search?", "AI assistants like ChatGPT, Gemini and Perplexity rely on search indexes such as Bing and Google and on clearly structured information. We connect your site to Google and Bing, mark up your business details so machines can read them, publish an llms.txt file, and write content that answers the questions customers ask."),
    ("Who pays for the domain?", "If you need a new domain, it's registered in your name and you pay for it directly (usually S$15–30 a year). You always own your domain."),
    ("Do you guarantee first page on Google?", "No honest provider can guarantee rankings, because Google decides. We guarantee the work: every SEO Boost is documented in a before/after report so you can see exactly what changed."),
    ("What happens if I cancel?", "Your site stays live until the end of the month you paid for. You keep your domain, and you can buy the site files if you want to host them elsewhere."),
    ("How long until my site is live?", "Usually within 7 days of receiving your details and photos."),
]
faq_html = "\n".join(
    f"        <details><summary>{q}</summary><p>{a.replace('go.yourbrand.com', '<code>go.yourbrand.com</code>').replace('llms.txt', '<code>llms.txt</code>')}</p></details>"
    for q, a in FAQS)
page("faq/index.html",
     "FAQ: Fees, Contracts, SEO & AI Search | Page One Singapore",
     "Answers about Page One Singapore: setup fees, contracts, 24/7 WhatsApp support, SEO landing pages, SEO Boost, ChatGPT visibility, domains and cancelling.",
     [{"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}],
     hero("FAQ", "", "Questions, answered",
          "Can't find yours? Tap the chat button and ask us on WhatsApp, 24/7. No obligation.", buttons=False) + """

    <section class="section">
      <div class="wrap narrow">
""" + faq_html + """
      </div>
    </section>

""" + cta(), crumb="FAQ")

# ---------- About ----------
page("about/index.html",
     "About Page One Singapore | Tested on Real Businesses",
     "Page One Singapore runs the websites and Google listings of five Singapore businesses. Affordable Google and AI visibility for new and small businesses.",
     [{"@context": "https://schema.org", "@type": "AboutPage", "url": SITE + "/about/", "name": "About Page One Singapore",
       "about": PROVIDER, "mainEntity": {"@type": "Person", "name": "Edwin", "jobTitle": "Founder, Page One Singapore",
                                         "worksFor": PROVIDER, "owns": {"@type": "AutoRepair", "name": "Edwin Garage", "url": "https://sggarage.com/"}}}],
     hero("About", "Tested on real businesses", "Built on real Singapore businesses, not theory.",
          "Five local businesses run on Page One today. Every method we offer was tested on them first.", buttons=False) + """

    <section class="section">
      <div class="wrap split">
        <div class="reveal">
          <p class="kicker">Why we exist</p>
          <h2>Online visibility shouldn't need a big budget</h2>
          <p>Page One Singapore runs the websites and Google listings for five local businesses today: a car workshop, a car detailing service, a sofa cleaning company, a property agent and a financial consultant.</p>
          <p>We started because new and small businesses were being quoted hundreds of dollars a month for SEO they couldn't see or measure. So we built a simpler way: S$20 a month, a report for every SEO Boost, and no contract. Start small, and add more only when you see it working.</p>
          <p><b>Founder:</b> Edwin, who also runs Edwin Garage in Ang Mo Kio. Every method on this site was used on his own business first.</p>
          <a class="card-link" href="/#stories">See the websites we run →</a>
        </div>
        <div class="panel reveal">
          <h3>How we work</h3>
          <ul class="ticks">
            <li><b>Honest.</b> No one can guarantee Google rankings, so we never promise them. We show you the work instead.</li>
            <li><b>Transparent.</b> Every SEO Boost comes with a before/after report.</li>
            <li><b>No lock-in.</b> No setup fee, no contract. You own your domain.</li>
            <li><b>Reachable.</b> WhatsApp us 24/7. No obligation to discuss.</li>
            <li><b>Local.</b> We serve businesses across Singapore.</li>
          </ul>
        </div>
      </div>
    </section>

""" + cta("Talk to us, no obligation", "Ask anything on WhatsApp, 24/7. Or start with a free Google + AI visibility check."),
     crumb="About")

# ---------- Contact ----------
page("contact/index.html",
     "Contact Page One Singapore | WhatsApp 24/7",
     "WhatsApp Page One Singapore 24/7 on +65 8997 6612. Ask about getting found on Google and AI search. No obligation to discuss.",
     [{"@context": "https://schema.org", "@type": "ContactPage", "url": SITE + "/contact/", "name": "Contact Page One Singapore", "about": PROVIDER}],
     hero("Contact", "WhatsApp 24/7", "Talk to us on WhatsApp, anytime.",
          "Questions, a free check, or ready to start: message us 24/7. No obligation to discuss.", buttons=False) + f"""

    <section class="section">
      <div class="wrap split">
        <div class="reveal">
          <p class="kicker">WhatsApp</p>
          <h2>{WA_DISPLAY}</h2>
          <p class="section-lead" style="margin-bottom:24px">We reply personally. Support runs 24/7, and there's no obligation to buy anything.</p>
          <a class="btn" href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a>
        </div>
        <div class="panel reveal">
          <h3>Help us help you faster</h3>
          <p>When you message, it helps to include:</p>
          <ul class="ticks">
            <li>Your business name</li>
            <li>What you do and the area you serve</li>
            <li>Your website, if you have one</li>
          </ul>
          <p>Prefer a form? Use the <a class="link" href="/#check">free visibility check</a>.</p>
        </div>
      </div>
    </section>
""", crumb="Contact")

# ---------- Privacy ----------
page("privacy/index.html",
     "Privacy Policy | Page One Singapore",
     "How Page One Singapore collects, uses and protects your personal data, in line with Singapore's Personal Data Protection Act (PDPA).",
     [],
     hero("Privacy policy", "", "Privacy policy", "Last updated 8 October 2026", buttons=False) + f"""

    <section class="section">
      <div class="wrap narrow prose">
        <p>Page One Singapore ("we", "us") respects your privacy. This policy explains how we handle personal data in line with Singapore's Personal Data Protection Act 2012 (PDPA).</p>
        <h2>What we collect</h2>
        <p>Only what you choose to send us, usually through WhatsApp or our free check form: your name, business name, phone number, business details, website address and any photos or information you share for your website.</p>
        <h2>How we use it</h2>
        <ul>
          <li>To reply to your enquiry and send your free visibility check</li>
          <li>To build and maintain your website or landing page</li>
          <li>To set up your Google Business Profile and search listings, with your permission</li>
          <li>To arrange payment and send SEO Boost reports</li>
        </ul>
        <p>We don't sell your personal data, and we don't use it for marketing unrelated to your enquiry.</p>
        <h2>Sharing</h2>
        <p>We share data only as needed to deliver our service, for example with our web host, domain registrar, Google and Bing, or messaging and payment providers. These providers handle data under their own privacy policies.</p>
        <h2>This website</h2>
        <p>This site doesn't use advertising or tracking cookies. It loads fonts from Google Fonts and stores a small note in your browser so the chat pop-up doesn't repeat. To see which pages are useful, it counts visits and WhatsApp-button clicks anonymously: the page, how you arrived (for example Google or ChatGPT), your device type and a random ID kept in your browser. This never includes your name or phone number, and it's switched off if your browser sends a Do Not Track signal. The free check form doesn't send data to us directly; it opens WhatsApp with your details filled in, and you choose whether to send them.</p>
        <h2>Keeping and protecting data</h2>
        <p>We keep personal data only as long as needed for the purposes above or as required by law, and take reasonable steps to protect it.</p>
        <h2>Your rights</h2>
        <p>You can ask to access or correct your personal data, or withdraw consent for us to use it. Contact our Data Protection Officer on WhatsApp at <a href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a>.</p>
        <h2>Changes</h2>
        <p>We may update this policy. The latest version is always on this page.</p>
      </div>
    </section>
""", crumb="Privacy policy")

# ---------- Terms ----------
page("terms/index.html",
     "Terms of Service | Page One Singapore",
     "The terms for Page One Singapore's Get Found subscription and SEO Boost top-ups: payment, cancellation, domains and what we can and can't promise.",
     [],
     hero("Terms of service", "", "Terms of service", "Last updated 8 October 2026", buttons=False) + f"""

    <section class="section">
      <div class="wrap narrow prose">
        <p>These terms apply when you use Page One Singapore's services. By signing up, you agree to them.</p>
        <h2>Our services</h2>
        <p><b>Get Found</b> (S$20 a month) covers a website on your own domain or a landing page on your subdomain, plus the Google and AI search setup described on our <a href="/get-found/">Get Found page</a>. <b>SEO Boost</b> (S$10 each) is an optional round of improvements with a report.</p>
        <h2>Payment</h2>
        <p>The monthly fee is paid in advance. SEO Boosts are paid when you top up. We arrange payment over WhatsApp. Prices are in Singapore dollars.</p>
        <h2>No contract, cancel anytime</h2>
        <p>There's no minimum term. You can cancel anytime by WhatsApp. Your service runs until the end of the month you've paid for; we don't refund part-months.</p>
        <h2>Your domain and content</h2>
        <p>Domains we register for you are in your name and paid by you directly. You keep your domain if you cancel. You confirm you have the rights to any text, photos and logos you send us. If you cancel, you can buy the site files if you want to host them elsewhere.</p>
        <h2>Results</h2>
        <p>Search engines and AI assistants decide their own rankings and answers. We don't guarantee any particular ranking, traffic or number of enquiries. We do the work described and document it.</p>
        <h2>Liability</h2>
        <p>To the extent the law allows, our total liability is limited to the fees you paid us in the 3 months before the claim.</p>
        <h2>Changes and law</h2>
        <p>We may update these terms and will tell active clients about material changes. These terms are governed by the laws of Singapore.</p>
        <p>Questions? WhatsApp us 24/7 on <a href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a>.</p>
      </div>
    </section>
""", crumb="Terms of service")

# ---------- Sample report ----------
page("report.html",
     "Sample SEO Boost Report | Page One Singapore",
     "See what one S$10 SEO Boost from Page One Singapore delivers: Google and AI visibility checks, improvements made, and a before/after report.",
     [],
     open(os.path.join(HERE, "report_body.html"), encoding="utf-8").read(), crumb="Sample report")

# ---------- 404 ----------
page("404.html",
     "Page Not Found | Page One Singapore",
     "The page you're looking for doesn't exist.",
     [],
     hero("Not found", "", "This page doesn't exist.",
          "It may have moved. Try one of these, or WhatsApp us 24/7.", buttons=False) + """

    <section class="section">
      <div class="wrap">
        <div class="cards three">
          <a class="card" href="/"><h2 class="h3">Home</h2><p>Start from the beginning.</p></a>
          <a class="card" href="/get-found/"><h2 class="h3">Get Found</h2><p>Our S$20/month plan.</p></a>
          <a class="card" href="/pricing/"><h2 class="h3">Pricing</h2><p>Plans and the cost calculator.</p></a>
        </div>
      </div>
    </section>
""", robots="noindex, follow")

# ---------- Home ----------
page("index.html",
     "Page One Singapore | Get Found on Google &amp; AI from S$20",
     "Get found on Google, Google Maps and AI search like ChatGPT. Website or SEO landing page from S$20/month. No setup fee, no contract, 24/7 WhatsApp.",
     [{"@context": "https://schema.org", "@graph": [
         {"@type": "ProfessionalService", "@id": BIZ_ID, "name": "Page One Singapore", "url": SITE + "/",
          "logo": SITE + "/icon-512.png", "image": SITE + "/images/og.png",
          "description": "Google and AI search visibility for Singapore businesses: the Get Found subscription (a website or SEO landing page) with optional SEO Boost top-ups.",
          "telephone": "+" + WA, "priceRange": "S$20 - S$70 per month",
          "areaServed": {"@type": "Country", "name": "Singapore"},
          "founder": {"@type": "Person", "name": "Edwin"},
          "knowsAbout": ["Search engine optimisation", "Local SEO", "Google Business Profile", "AI search visibility", "Generative engine optimisation"],
          "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                        "opens": "00:00", "closes": "23:59"},
          "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "telephone": "+" + WA,
                           "availableLanguage": "English", "areaServed": "SG",
                           "hoursAvailable": {"@type": "OpeningHoursSpecification",
                                              "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                              "opens": "00:00", "closes": "23:59"}},
          "makesOffer": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Get Found basic subscription", "url": SITE + "/get-found/"}, "price": "20", "priceCurrency": "SGD"},
                         {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "SEO Boost", "url": SITE + "/seo-boost/"}, "price": "10", "priceCurrency": "SGD"}]},
         {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Page One Singapore",
          "inLanguage": "en-SG", "publisher": {"@id": BIZ_ID}}]}],
     open(os.path.join(HERE, "home_body.html"), encoding="utf-8").read().rstrip("\n"))
print("built")
