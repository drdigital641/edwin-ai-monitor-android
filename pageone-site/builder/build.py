import json, os, sys

ROOT = sys.argv[1]
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://pageonesingapore.com"
WA = "6597856612"
WA_DISPLAY = "+65 9785 6612"
WA_LINK = f"https://wa.me/{WA}?text=Hi%20Page%20One%20Singapore%2C%20I%27d%20like%20to%20know%20more."
UPDATED = "2026-10-08"
BIZ_ID = SITE + "/#business"
GBP = "https://maps.google.com/?cid=8757289318297107567"
API = "https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions"
PROMO = '<div class="promo-bar"><div class="wrap"><b>Introductory price:</b> S$20/month until we reach our early-client target. Grab it before it goes up. Any new price will stay close to S$20. <a href="/signup/">Sign up &rarr;</a></div></div>'

NAV = [
    ("/website/", "Website"),
    ("/get-found/", "Get Found"),
    ("/seo-boost/", "SEO Boost"),
    ("/pricing/", "Pricing"),
    ("/results/", "Results"),
    ("/about/", "About"),
    ("/faq/", "FAQ"),
]

CHAT_ICON = '<svg viewBox="0 0 24 24" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M4 4h16a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H9l-5 4v-4a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2zm3 6.5a1.5 1.5 0 1 0 0 .01zm5 0a1.5 1.5 0 1 0 0 .01zm5 0a1.5 1.5 0 1 0 0 .01z"/></svg>'
WA_ICON = '<svg viewBox="0 0 24 24" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.6.3-.2.2-.8.8-.8 2s.8 2.3 1 2.5c.1.2 1.7 2.6 4.1 3.6 1.5.7 2.1.7 2.9.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'

PROVIDER = {"@id": BIZ_ID}

COMPANY = {"@type": "Organization", "@id": SITE + "/#company", "name": "Snap Commercial Pte. Ltd.",
           "legalName": "SNAP COMMERCIAL PTE. LTD.", "foundingDate": "2022-03-23",
           "identifier": {"@type": "PropertyValue", "propertyID": "UEN", "value": "202209904W"},
           "address": {"@type": "PostalAddress", "addressCountry": "SG"}}

FOUNDER = {"@type": "Person", "name": "Edwin", "jobTitle": "Founder, Page One Singapore",
           "alumniOf": {"@type": "CollegeOrUniversity", "name": "National University of Singapore", "sameAs": "https://www.nus.edu.sg/"},
           "hasCredential": {"@type": "EducationalOccupationalCredential", "credentialCategory": "degree",
                             "name": "Bachelor's degree in Computer Science with Honours"},
           "knowsAbout": ["Computer science", "Search engine optimisation", "AI search visibility", "Small business operations"]}


# One description of the business, used in the JSON-LD of every page (full version on the homepage).
# Only facts that are stated on the site. sameAs lists only real profiles: the Google Business Profile.
CONTACT_POINT = {"@type": "ContactPoint", "contactType": "customer support", "telephone": "+" + WA,
                 "url": f"https://wa.me/{WA}", "availableLanguage": "English", "areaServed": "SG",
                 "hoursAvailable": {"@type": "OpeningHoursSpecification",
                                    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                    "opens": "00:00", "closes": "23:59"}}
ORG_CORE = {"@type": "ProfessionalService", "@id": BIZ_ID, "name": "Page One Singapore",
            "alternateName": ["Page One SG", "PageOne Singapore"], "url": SITE + "/",
            "logo": {"@type": "ImageObject", "url": SITE + "/icon-512.png", "width": 512, "height": 512},
            "image": SITE + "/images/og.png",
            "description": "Done-for-you website and SEO for Singapore small businesses: a website (or SEO landing page) built and managed, found on Google Search, Google Maps and AI assistants, from S$20 a month. No setup fee, no contract.",
            "telephone": "+" + WA, "priceRange": "S$20 - S$70 per month",
            "address": {"@type": "PostalAddress", "addressCountry": "SG"},
            "areaServed": {"@type": "Country", "name": "Singapore"},
            "contactPoint": CONTACT_POINT, "hasMap": GBP, "sameAs": [GBP]}
WEBSITE_NODE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Page One Singapore",
                "alternateName": ["Page One SG", "PageOne Singapore", "pageonesingapore.com"],
                "inLanguage": "en-SG", "publisher": {"@id": BIZ_ID}}
AIV_UPDATED = "2026-10-14"  # AI-visibility release: at-a-glance blocks and plain answers
LASTMOD = {}     # page URL -> dateModified, for the sitemap (bridge/lastmod.json)
LLMS_PAGES = []  # (url, title, description, [(question, answer)]) for llms-full.txt


# Client list and every Search Console figure on the site (builder/showcase.json).
exec(open(os.path.join(HERE, "showcase.py"), encoding="utf-8").read())


def crumbs_ld(name, url, parent=None):
    trail = [("Home", "/")] + ([parent] if parent else []) + [(name.replace("&amp;", "&"), url)]
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(trail)],
    }


def page(path, title, desc, schemas, body, crumb=None, robots="index, follow, max-image-preview:large", updated=None, head_extra="", foot_extra="", crumb_parent=None):
    managed_link = '        <a href="/managed-website-singapore/">Fully managed website</a>\n'
    clients_href = "/clients/"
    if path == "index.html":
        current = "/"
    elif path.endswith("index.html"):
        current = "/" + path[: -len("index.html")]
    else:
        current = "/" + path
    if crumb:
        schemas = schemas + [crumbs_ld(crumb, current, crumb_parent)]
    if "noindex" not in robots:
        schemas = schemas + [{
            "@context": "https://schema.org", "@type": "WebPage", "@id": SITE + current + "#webpage", "url": SITE + current, "name": title.replace("&amp;", "&"),
            "description": desc, "inLanguage": "en-SG", "isPartOf": {"@id": SITE + "/#website"},
            "about": {"@id": BIZ_ID}, "publisher": {"@id": BIZ_ID},
            "primaryImageOfPage": {"@type": "ImageObject", "url": SITE + "/images/og.png", "width": 600, "height": 315},
            "dateModified": updated or UPDATED}]
        if path != "index.html":  # the homepage carries the full business description
            schemas = schemas + [{"@context": "https://schema.org", "@graph": [ORG_CORE, WEBSITE_NODE]}]
        LASTMOD[current] = updated or UPDATED
        LLMS_PAGES.append((current, title.replace("&amp;", "&"), desc, [
            (q["name"], q["acceptedAnswer"]["text"]) for s in schemas if s.get("@type") == "FAQPage" for q in s["mainEntity"]]))
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
  <script>if(/(^|\\.)pageonesingapore\\.com$/.test(location.hostname)&&(location.protocol==="http:"||location.hostname!=="pageonesingapore.com"))location.replace("https://pageonesingapore.com"+location.pathname+location.search+location.hash);</script>
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
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{SITE}/images/og.png">
  <meta name="twitter:image:alt" content="Page One Singapore: get found on Google and AI search from S$20 a month">
  <meta name="theme-color" content="#060b18">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap">
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap"></noscript>
  <link rel="stylesheet" href="/styles.css?v=14">
  <script>document.documentElement.classList.add("js");</script>
{ld}{head_extra}
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  {PROMO}
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="logo" href="/">
        <span class="logo-mark">1</span><span>Page One <b>Singapore</b></span>
      </a>
      <nav class="nav" id="nav" aria-label="Main">
{nav}
      </nav>
      <a class="btn btn-small" href="/signup/">Sign up</a>
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
        <p><a class="footer-wa" href="{WA_LINK}" target="_blank" rel="noopener">WhatsApp {WA_DISPLAY}</a><br><span>Chat with Edwin · no obligation</span></p>
      </div>
      <div>
        <h2>Services</h2>
        <a href="/website/">Website, built and managed</a>
{managed_link}        <a href="/seo-aeo-geo-singapore/">SEO, AEO and GEO</a>
        <a href="/new-business-website/">New business website</a>
        <a href="/seo-services-singapore/">SEO services compared</a>
        <a href="/get-found/">Get Found</a>
        <a href="/seo-boost/">SEO Boost</a>
        <a href="/pricing/">Pricing</a>
        <a href="/signup/">Sign up</a>
        <a href="/free-website-check/">Free website check</a>
        <a href="/industries/">Industries we help</a>
        <a href="/cheapest-seo-singapore/">Low-cost SEO</a>
        <a href="/cheapest-website-singapore/">Website without the lump sum</a>
        <a href="/report.html">Sample report</a>
      </div>
      <div>
        <h2>Company</h2>
        <a href="/about/">About</a>
        <a href="/results/">Results</a>
        <a href="{clients_href}">Clients</a>
        <a href="/articles/">Articles</a>
        <a href="/faq/">FAQ</a>
        <a href="/seo-explained/">SEO explained simply</a>
        <a href="/contact/">Contact</a>
      </div>
      <div>
        <h2>Legal</h2>
        <a href="/privacy/">Privacy policy</a>
        <a href="/terms/">Terms of service</a>
      </div>
    </div>
    <div class="wrap footer-bottom">
      <p class="fine">© <span id="year">2026</span> Page One Singapore. All rights reserved. Page One Singapore is a project of Snap Commercial Pte. Ltd. (UEN 202209904W).</p>
    </div>
  </footer>

  <a class="wa-float" id="wa-float" href="{WA_LINK}" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">
    {WA_ICON}
  </a>

  <script src="/main.js?v=12" defer></script>{foot_extra}
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
        "offers": {"@type": "Offer", "price": price, "priceCurrency": "SGD", "url": SITE + url,
                   **({"priceSpecification": {"@type": "UnitPriceSpecification", "price": price, "priceCurrency": "SGD", "unitCode": "MON"}}
                      if price == "20" else {})},
    }


def cta(title="Not sure where you stand?", text="Check your website free in under a minute, or chat with Edwin on WhatsApp. No obligation."):
    return f"""    <section class="cta-band">
      <div class="wrap">
        <h2>{title}</h2>
        <p>{text}</p>
        <div class="cta-row center">
          <a class="btn" href="/signup/">Sign up from S$20/month</a>
          <a class="btn btn-ghost" href="{WA_LINK}" target="_blank" rel="noopener">Chat on WhatsApp</a>
        </div>
      </div>
    </section>"""


def hero(crumb, eyebrow, h1, lead, price_html="", buttons=True):
    btns = """
        <div class="cta-row">
          <a class="btn" href="/signup/">Sign up from S$20/month</a>
          <a class="btn btn-ghost" href="/#check">Check my website free</a>
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
              <li>Your business on Google Maps, with hours, photos and a call button <span class="term">Google Business Profile</span></li>
              <li>Google and Bing told your site exists, with Google's free report connected so you can see who finds you. Bing also powers ChatGPT search. <span class="term">Search Console</span> <span class="term">Bing Webmaster Tools</span></li>
              <li>Your name, address, hours and services labelled so Google and AI assistants read them correctly <span class="term">Structured data (Schema.org)</span></li>
              <li>Regular new articles written for your site, answering what your customers search for, so Google and AI assistants keep finding fresh content <span class="term">Content SEO</span></li>
              <li>A list of all your pages, plus a short summary for AI tools, so nothing gets missed <span class="term">XML sitemap</span> <span class="term">llms.txt</span></li>
              <li>Fast, secure website (the padlock in the address bar) with a WhatsApp chat button <span class="term">Hosting</span> <span class="term">HTTPS / SSL</span></li>
            </ul>
            <p class="fine" style="margin:0"><a class="link" href="/seo-explained/">What do these terms mean? →</a></p>"""

PLAN_COMPARE = """<div class="cards two plan-compare">
          <div class="card reveal">
            <p class="pill">Every month · S$20</p>
            <h3>Get Found: discovered naturally</h3>
            <ul class="ticks">
              <li>Found in the free, unpaid results on Google, Google Maps and ChatGPT when customers search for what you do. No ad spend. <span class="term">Organic search</span> <span class="term">AI search visibility</span></li>
              <li>Regular new articles written for your site, answering what your customers search for, so Google and AI assistants keep finding fresh content <span class="term">Content SEO</span></li>
              <li>A technical audit of your page every month: can Google and AI assistants still find it, read it and understand it? <span class="term">Technical SEO audit</span></li>
              <li>Your website or landing page kept online, secure and fast, with a WhatsApp button <span class="term">Hosting</span> <span class="term">HTTPS</span></li>
              <li>Google's free report connected, so you can see who finds you <span class="term">Search Console</span></li>
            </ul>
          </div>
          <div class="card reveal">
            <p class="pill">Optional extra · S$10 each</p>
            <h3>SEO Boost: accelerated growth</h3>
            <ul class="ticks">
              <li>More articles and content on top of your regular ones, aimed at new niche searches: specific phrases like "aircon chemical wash Tampines". Fewer businesses compete for them, and the people searching are ready to buy. <span class="term">Long-tail keywords</span></li>
              <li>Extra processing to fix the SEO issues found in your audit <span class="term">Technical SEO fixes</span></li>
              <li>A before/after report of what was done and what's next</li>
              <li>Top up anytime, as many or as few as you like</li>
            </ul>
          </div>
        </div>"""

# "Page One at a glance": the plain facts an AI assistant (or a busy owner) needs, in one place.
# Homepage and About. Only facts already stated elsewhere on the site.
GLANCE_ANSWER = ("Page One Singapore is a done-for-you website and SEO service for Singapore small businesses. "
                 "We build your website (or add an SEO landing page to the one you have), get it found on Google Search, Google Maps "
                 "and AI assistants like ChatGPT, and look after it every month, for S$20 a month with no setup fee and no contract.")
GLANCE_ROWS = [
    ("Who it's for", 'New businesses that need their first website, and small businesses looking for affordable SEO. '
                     '<a class="link" href="/new-business-website/">New business</a> · <a class="link" href="/seo-services-singapore/">Shopping for SEO</a>'),
    ("What you get", "A website on your own domain (or an SEO landing page next to your current site), hosting and SSL, Google Business Profile, "
                     "Google Search Console and Bing setup, structured data and llms.txt for AI search, regular new articles, a monthly technical audit "
                     "and small changes over WhatsApp."),
    ("Price", 'S$20 a month on the Get Found plan (introductory price). Optional SEO Boosts are S$10 each. No setup fee, no contract, cancel anytime. '
              'Your domain, usually S$15–30 a year, is registered in your name and paid by you directly. <a class="link" href="/pricing/">Pricing</a>'),
    ("Where", "Singapore, island-wide."),
    ("How fast", "Usually live within 7 days of receiving your details and photos."),
    ("How to start", f'WhatsApp Edwin on <a class="link" href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a> '
                     'or <a class="link" href="/signup/">sign up online</a>. No obligation.'),
    ("Who runs it", 'Founder Edwin (NUS Computer Science, Honours). Page One Singapore is a project of Snap Commercial Pte. Ltd. (UEN 202209904W). '
                    '<a class="link" href="/results/">Results</a> · <a class="link" href="/clients/">Client websites</a> · '
                    '<a class="link" href="/is-page-one-singapore-legit/">How to check us</a>'),
]


def glance(section_class="section"):
    rows = "\n".join(f"              <tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in GLANCE_ROWS)
    return f"""    <section class="{section_class}" id="at-a-glance">
      <div class="wrap narrow">
        <p class="kicker reveal">At a glance</p>
        <h2 class="reveal">Page One at a glance</h2>
        <p class="section-lead reveal">{GLANCE_ANSWER}</p>
        <div class="table-wrap reveal">
          <table class="compare">
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
      </div>
    </section>"""


# ---------- Get Found ----------
page("get-found/index.html",
     "Small Business SEO Singapore: Get Found Plan from S$20/month",
     "Our S$20/month basic plan. No website? We build one. Have one? We add an SEO landing page, set up for Google and AI search. No setup fee or contract.",
     [service("Get Found basic subscription", "/get-found/",
              "A website on the client's own domain, or an SEO landing page on a subdomain of their existing website, set up for Google Search, Google Maps and AI assistants.", "20")],
     hero("Get Found", "Basic subscription",
          "Get Found: your shopfront on Google and AI.",
          "Get Found is our S$20-a-month plan that gets your business found on Google Search, Google Maps and AI assistants like ChatGPT. No website? We build one on your own domain. Already have one? We add an SEO landing page next to it.",
          '<p class="hero-price"><b>S$20</b>/month · <span class="intro-tag">Introductory price</span> · no setup fee · no contract</p>') + """

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Which describes you?</p>
        <h2 class="reveal">Same plan, either way</h2>
        <div class="cards two" style="margin-top:32px">
          <div class="card reveal">
            <p class="pill">No website yet</p>
            <h3>We build your website</h3>
            <p>A fast, mobile-friendly site on your own domain, managed for you every month. The domain is registered in your name, so you always own it (usually S$15–30 a year, paid directly). <a class="link" href="/website/">More about our websites →</a></p>
          </div>
          <div class="card reveal">
            <p class="pill">Already have a website</p>
            <h3>We add a landing page</h3>
            <p>Keep your current site exactly as it is. We build an SEO landing page (an extra page designed to bring in customers from Google) at an address like <code>go.yourbrand.com</code>. You, or whoever manages your domain, add one setting called a DNS record. We send simple step-by-step instructions, and Edwin can guide you through it.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">What S$20 covers every month</p>
        <h2 class="reveal">Get Found every month, Boost when you want</h2>
        <p class="section-lead reveal">Your S$20 plan keeps you discovered naturally on Google and ChatGPT, with regular new articles and a technical audit every month. A Boost accelerates growth: more content aimed at new keywords, so you show up for more searches, faster.</p>
        """ + PLAN_COMPARE + """
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
          <p class="no-tech"><b>No tech skills needed.</b> You tell us about your business on WhatsApp. We handle the website, Google, Maps and AI setup.</p>
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
          <li class="reveal"><span>1</span><h3>Free website check</h3><p>See where your website stands on Google, mobile and AI search in under a minute.</p></li>
          <li class="reveal"><span>2</span><h3>Chat with Edwin</h3><p>On WhatsApp: tell us what you do, where, and send a few photos. No obligation.</p></li>
          <li class="reveal"><span>3</span><h3>We build and launch</h3><p>Your site or landing page goes live, connected to Google, Maps and Bing.</p></li>
        </ol>
        <div class="price-strip reveal">
          <p><b>S$20/month</b> · introductory price · no setup fee · cancel anytime</p>
          <a class="card-link" href="/signup/">Sign up now →</a>
        </div>
      </div>
    </section>

""" + cta(), crumb="Get Found", updated=AIV_UPDATED)


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


redirect("new-website/index.html", "/website/")
redirect("landing-page/index.html", "/get-found/")

# ---------- Website: built and managed ----------
WEBSITE_FAQ = [
    ("How much does a website cost with Page One Singapore?", "S$20 a month on the Get Found plan, at an introductory price for a limited time. That covers building your website, hosting it, keeping it secure and fast, and looking after it every month. There's no setup fee and no contract. Your domain is registered in your name and paid by you directly, usually S$15–30 a year."),
    ("Who looks after the website after it's built?", "We do. We host it, keep it online, secure and fast, run a technical audit every month, and make small text and photo changes when you need them. You just WhatsApp Edwin."),
    ("I only have a Facebook or Instagram page. Do I still need a website?", "A social page is a good start, but Google and ChatGPT can't rank it like a website. A website with a page for each service and your area gives customers searching on Google a way to find you, and it's yours, not a social platform's."),
    ("Do I own my website and domain?", "Your domain is registered in your name, so you always own it. If you cancel, your site stays live until the end of the month you paid for, you keep your domain, and you can buy the site files if you want to host them elsewhere."),
    ("How long does it take to build my website?", "Usually within 7 days of receiving your details and photos. You send them over WhatsApp, and we do the rest."),
    ("Do I need any technical skills?", "No. You tell us about your business and send a few photos. We handle the domain setup, design, hosting, Google setup and updates."),
    ("What does a small business website cost per year with Page One?", "About S$255–270 a year all in: 12 months at S$20 (S$240) plus your domain name, usually S$15–30 a year, paid by you directly. Building the website, hosting, the security certificate, Google setup, a monthly technical audit and small changes are all inside the S$20. There is no setup fee and no separate renewal bill for hosting or maintenance."),
    ("What pages does a small business website need?", "Most local businesses need a homepage that says what you do and which area you serve, one page for each main service, a way to see prices or how you quote, an about page, and a contact page with your hours and a WhatsApp button. We build these pages for you. If your site has a contact form, add a short privacy notice too: under the PDPA you need to tell people what you will use their details for."),
    ("I already have a website but no one looks after it. Can you help?", "Yes. We can take over looking after your existing website, or keep your site as it is and add an SEO landing page next to it. WhatsApp Edwin with your website address and he'll check it and tell you honestly which makes sense for you."),
]

_site_html = site_cards_html()
_wfaq_html = "\n".join(f"        <details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>" for q, a in WEBSITE_FAQ)

page("website/index.html",
     "Small Business Website Singapore: Built &amp; Managed, S$20/mo",
     "No website yet? We build a fast, mobile-friendly website for your Singapore business and manage it for you: hosting, updates and Google setup. S$20/month.",
     [service("Website design and management for small businesses", "/website/",
              "A website built on the client's own domain, set up for Google, Google Maps and AI search, then hosted and managed every month: security, speed, a monthly technical audit and small text and photo changes.", "20"),
      {"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in WEBSITE_FAQ]}],
     hero("Website", "No website yet?",
          "A good website for your business, built and managed for S$20 a month.",
          "Just starting out, or still relying on a Facebook page? We build a fast, mobile-friendly website on your own domain, set it up so Google, Google Maps and ChatGPT can find it, then look after it for you every month. No setup fee, no contract, no tech skills needed.",
          '<p class="hero-price"><b>S$20</b>/month · <span class="intro-tag">Introductory price</span> · website + management · no setup fee</p>') + """

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Who it's for</p>
        <h2 class="reveal">Sound familiar?</h2>
        <div class="cards three" style="margin-top:32px">
          <div class="card reveal"><h3>You're starting a new business</h3><p>You need a proper website so customers can find you and trust you, without paying a big amount upfront. <a class="link" href="/new-business-website/">Start here →</a></p></div>
          <div class="card reveal"><h3>You're only on Facebook or Instagram</h3><p>Social pages are a start, but Google and ChatGPT can't rank them like a website. A website is yours, and it shows up when people search.</p></div>
          <div class="card reveal"><h3>You don't want to manage a website</h3><p>No time to learn a website builder, chase a designer for changes or worry about hosting. Already have a website that no one looks after? We can take it over and manage it for you. <a class="link" href="/managed-website-singapore/">What fully managed covers →</a></p></div>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">What you get</p>
        <h2 class="reveal">Built for you, set up for Google, managed every month</h2>
        <div class="cards three plain-cards" style="margin-top:32px">
          <div class="card reveal"><div class="emoji" aria-hidden="true">🛠️</div><h3>Built for you</h3><p>A fast website that works well on phones, on your own domain, with your services, area, photos and a WhatsApp button so customers can message you in one tap.</p><p class="tech"><b>Technical name</b><span class="term">Mobile-first design</span><span class="term">Custom domain</span></p></div>
          <div class="card reveal"><div class="emoji" aria-hidden="true">🔍</div><h3>Set up to be found</h3><p>Your Google Maps listing, Google and Bing connected, and your business details labelled so Google and AI assistants like ChatGPT can read them.</p><p class="tech"><b>Technical name</b><span class="term">Google Business Profile</span><span class="term">Structured data</span><span class="term">llms.txt</span></p></div>
          <div class="card reveal"><div class="emoji" aria-hidden="true">🧰</div><h3>Managed every month</h3><p>We keep it online, secure and fast, run a technical audit every month, and make small text and photo changes when you need them. Just WhatsApp Edwin.</p><p class="tech"><b>Technical name</b><span class="term">Hosting</span><span class="term">HTTPS / SSL</span><span class="term">Technical SEO audit</span></p></div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">Websites we built and run</p>
        <h2 class="reveal">Real Singapore businesses, live today</h2>
        <p class="section-lead reveal">Visit them and judge for yourself. Each one is built and looked after with the same system you get.</p>
        <div class="cards three site-cards" style="margin-top:32px">
""" + _site_html + """
        </div>
        <p class="note reveal"><a class="card-link" href="/clients/">See every client website and its Google numbers →</a></p>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Your options</p>
        <h2 class="reveal">Website builder, web designer, or Page One?</h2>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th></th><th>DIY website builder</th><th>Web designer (one-off)</th><th>Page One</th></tr></thead>
            <tbody>
              <tr><th>Who builds it</th><td>You</td><td>The designer</td><td>We do</td></tr>
              <tr><th>Google, Maps and AI setup</th><td>Up to you</td><td>Depends on the designer</td><td>Included</td></tr>
              <tr><th>Hosting and security</th><td>Through the builder</td><td>Often up to you</td><td>Included</td></tr>
              <tr><th>Changes after launch</th><td>You do them</td><td>Often charged separately</td><td>Small changes included</td></tr>
              <tr><th>Cost</th><td>Builder plan plus your time</td><td>Usually an upfront fee</td><td>S$20 a month, no setup fee</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">How it works</p>
        <h2 class="reveal">Live within 7 days</h2>
        <ol class="steps" style="margin-top:72px">
          <li class="reveal"><span>1</span><h3>Chat with Edwin</h3><p>On WhatsApp: tell us what you do and where. No obligation.</p></li>
          <li class="reveal"><span>2</span><h3>Send details and photos</h3><p>We register your domain in your name and build your website.</p></li>
          <li class="reveal"><span>3</span><h3>We launch and look after it</h3><p>Usually live within 7 days, connected to Google, Maps and Bing, and managed every month after that.</p></li>
        </ol>
        <div class="price-strip reveal">
          <p><b>S$20/month</b> · introductory price · website + management · no setup fee · cancel anytime</p>
          <a class="card-link" href="/signup/">Sign up now →</a>
        </div>
        <p class="note reveal">Same system, real numbers: Edwin Garage, built and run this way, got """ + EG["clicks"] + """ clicks from Google in the 28 days to """ + THROUGH + """, with an average position of """ + EG["pos"] + """ (Google Search Console). <a class="link" href="/results/">See the case studies →</a> <a class="link" href="/clients/">See every client website →</a></p>
      </div>
    </section>

    <section class="section alt" id="checklist">
      <div class="wrap narrow">
        <p class="kicker reveal">Small business website checklist</p>
        <h2 class="reveal">What every small business website in Singapore needs</h2>
        <p class="section-lead reveal">Whoever builds it, check your website has these. Most website price guides talk about design and page count. These are the things that decide whether customers can find you and contact you.</p>
        <ul class="ticks reveal">
          <li><b>Says what you do and where, in the first screen.</b> "Aircon servicing in Tampines", not "Welcome to our website".</li>
          <li><b>One page per main service.</b> Google ranks pages, not businesses. A service with no page is hard to find.</li>
          <li><b>Fast and easy on a phone.</b> Most people searching for a local business are on their phone.</li>
          <li><b>One-tap WhatsApp or call button</b> on every page, with the number you actually answer.</li>
          <li><b>The padlock (HTTPS).</b> Browsers warn visitors about sites without it.</li>
          <li><b>Linked to your Google Business Profile</b>, with the same name, phone and hours on both.</li>
          <li><b>Business details labelled for Google and AI assistants</b> (structured data), so ChatGPT and Google read your name, area and services correctly.</li>
          <li><b>Search Console connected</b>, so you can see which searches find you.</li>
          <li><b>A privacy notice if you have a contact form.</b> Under the PDPA, tell people what you'll use their details for.</li>
          <li><b>Someone looking after it.</b> Hosting renewals, security updates and new content don't stop after launch.</li>
        </ul>
        <p class="note reveal">On the S$20 plan we build and look after all of these except the privacy notice, which is your business's own policy: send us the wording and we add it to your site. <a class="link" href="/#check">Check your current website free →</a> · <a class="link" href="/new-business-website/">Starting a new business? See the launch checklist →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">Small business websites: your questions, answered</h2>
        <div style="margin-top:24px">
""" + _wfaq_html + """
        </div>
      </div>
    </section>

""" + cta("Get your business online this week", "Tell Edwin about your business on WhatsApp. No obligation, no tech skills needed."),
     crumb="Website", updated="2026-10-13")


# ---------- SEO Boost ----------
BOOST_FAQ = [
    ("How much does an SEO Boost cost?", "S$10 per Boost, on top of the S$20-a-month Get Found plan. There is no package to commit to: add Boosts at sign-up or top up anytime on WhatsApp. Most businesses start with 1 or 2 a month and add more when they want to push harder, for example before a busy season."),
    ("What is the difference between the plan and a Boost?", "The S$20 Get Found plan already includes regular new articles and a technical audit every month. Each Boost adds more content on top, aimed at new niche long-tail searches, plus extra processing to fix the issues found in your audit, and ends with a before/after report."),
    ("Does an SEO Boost guarantee better rankings?", "No. Google decides rankings, so no honest provider can guarantee them. What we guarantee is the work: every Boost is documented in a before/after report, so you can see exactly what was done and what changed."),
]
BOOST_FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in BOOST_FAQ]}

page("seo-boost/index.html",
     "SEO Boost: S$10 Top-up for Faster Results | Page One SG",
     "An optional S$10 SEO Boost: one full round of Google and AI visibility improvements, with a before/after report. Add at sign-up or top up anytime on WhatsApp.",
     [service("SEO Boost (optional top-up)", "/seo-boost/",
              "One full round of Google and AI search visibility improvements with a before/after report. Optional, topped up anytime.", "10"), BOOST_FAQ_LD],
     hero("SEO Boost", "Optional top-up",
          "Want faster results? Add an SEO Boost.",
          "An SEO Boost is an optional S$10 top-up for faster results: more content aimed at new niche long-tail searches, extra processing to fix SEO issues, then a report of exactly what changed. Your S$20 plan already includes regular new articles and a technical audit every month.",
          '<p class="hero-price"><b>S$10</b>/boost · top up anytime</p>') + """

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">What's in one Boost</p>
        <h2 class="reveal">Find niche searches, fix issues, report</h2>
        <div class="cards three" style="margin-top:32px">
          <div class="card reveal"><div class="icon">1</div><h3>Find niche searches</h3><p>The specific phrases your customers type, like "aircon chemical wash Tampines". Fewer businesses compete for them, and the people searching are ready to buy. We also check where you stand on Google, Maps and ChatGPT.</p><p class="tech"><b>Technical name</b><span class="term">Long-tail keyword research</span><span class="term">Rank tracking</span></p></div>
          <div class="card reveal"><div class="icon">2</div><h3>Target them and fix issues</h3><p>New content and FAQs aimed at those niche searches, plus extra processing to fix the SEO issues found in your monthly audit.</p><p class="tech"><b>Technical name</b><span class="term">Content SEO</span><span class="term">Technical SEO fixes</span></p></div>
          <div class="card reveal"><div class="icon">3</div><h3>Report</h3><p>A before/after report: what was done, what improved, and what's planned next, explained in plain words.</p><p class="tech"><b>Technical name</b><span class="term">Search Console data</span><span class="term">Change log</span></p></div>
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
            <li>Add Boosts at sign-up, or top up anytime on WhatsApp</li>
            <li>Works on top of your Get Found plan</li>
            <li>Rankings aren't guaranteed, but every Boost is documented</li>
          </ul>
          <a class="card-link" href="/pricing/">Work out your monthly cost →</a>
        </div>
      </div>
    </section>

    <section class="section" id="top-up">
      <div class="wrap narrow">
        <p class="kicker reveal">Already a client?</p>
        <h2 class="reveal">Top up SEO Boosts</h2>
        <form class="topup-form panel reveal" id="topup-form" novalidate>
          <label>Your business name<input name="business" required autocomplete="organization"></label>
          <label>How many Boosts?
            <select name="boosts"><option value="1">1 Boost · S$10</option><option value="2" selected>2 Boosts · S$20</option><option value="3">3 Boosts · S$30</option><option value="4">4 Boosts · S$40</option><option value="6">6 Boosts · S$60</option><option value="10">10 Boosts · S$100</option></select>
          </label>
          <p class="form-error" role="alert" hidden></p>
          <button class="btn" type="submit">Top up on WhatsApp</button>
          <p class="fine">Opens WhatsApp with your request filled in. Not a client yet? <a href="/signup/">Sign up here</a> and add Boosts at the same time.</p>
        </form>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">SEO Boost: your questions, answered</h2>
        <div style="margin-top:24px">
""" + "".join(f"        <details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>\n" for q, a in BOOST_FAQ) + """        </div>
        <p class="note reveal"><a class="link" href="/report.html">See a sample Boost report →</a> <a class="link" href="/faq/">Full FAQ →</a></p>
      </div>
    </section>

""" + cta("Start with a free website check", "Before you spend anything, see where your website stands on Google, mobile and AI search. Takes under a minute."),
     crumb="SEO Boost", updated="2026-10-15")

# ---------- Pricing ----------
# "SEO packages / SEO pricing Singapore" owner page. Only Page One's own prices are numbers; other packages are
# described by what buyers should compare, never by a provider's price.
PRICING_FAQ = [
    ("How much does SEO cost in Singapore with Page One?", "S$20 a month on the Get Found plan (introductory price), with no setup fee and no minimum contract. Optional SEO Boosts are S$10 each. The only other cost is your domain name, usually S$15–30 a year, which is registered in your name and paid by you directly."),
    ("Is there a minimum contract?", "No. You pay monthly in advance and can cancel anytime by WhatsApp. If you cancel, your site stays live until the end of the month you paid for, and you keep your domain."),
    ("Is there a setup fee?", "No. Building your website (or SEO landing page), Google Business Profile, Search Console and Bing setup are all part of the S$20 a month."),
    ("What happens when the introductory price ends?", "S$20 is an introductory price until we reach our early-client target. Any new price will stay close to S$20."),
    ("What is not included?", "Paid ads, running your social media accounts and buying links. Your domain name is paid by you directly. We also don't promise rankings, because Google decides them and no honest provider can guarantee them."),
    ("Do I need a website before I sign up?", "No. If you don't have one, we build it on your own domain as part of the S$20 plan. If you already have one, we add an SEO landing page on a subdomain and leave your current site as it is."),
]

page("pricing/index.html",
     "SEO Packages &amp; Pricing Singapore: S$20/month, No Contract",
     "SEO pricing for Singapore small businesses: S$20/month with your website, Google Maps and ChatGPT setup, articles and a monthly audit. No setup fee or contract.",
     [{"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in PRICING_FAQ]},
      {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Page One Singapore pricing", "url": SITE + "/pricing/",
       "itemListElement": [
           {"@type": "Offer", "name": "Get Found basic subscription (website or landing page + Google & AI visibility setup)", "price": "20", "priceCurrency": "SGD",
            "url": SITE + "/get-found/", "seller": PROVIDER,
            "priceSpecification": {"@type": "UnitPriceSpecification", "price": "20", "priceCurrency": "SGD", "unitCode": "MON"}},
           {"@type": "Offer", "name": "SEO Boost (optional top-up) with before/after report", "price": "10", "priceCurrency": "SGD",
            "url": SITE + "/seo-boost/", "seller": PROVIDER}]}],
     hero("Pricing", "No setup fee · No contract · Cancel anytime",
          "Simple pricing. Start at S$20.",
          "One monthly plan at an introductory price, plus optional SEO Boosts when you want faster results. Sign up by chatting with Edwin on WhatsApp.", buttons=False) + """

    <section class="section">
      <div class="wrap">
        <div class="pricing">
          <div class="price-card reveal">
            <p class="pill">Basic subscription</p>
            <h2 class="h3">Get Found</h2>
            <p class="price"><span>S$20</span>/month</p>
            <p class="intro-note"><span class="intro-tag">Introductory price</span> Goes up once we reach our early-client target, so grab it now. Any new price will stay close to S$20.</p>
            <ul class="ticks">
              <li><a href="/get-found/">Your own website <em>or</em> a landing page on your subdomain</a></li>
              <li>Found naturally on Google and ChatGPT: free, unpaid results, no ad spend</li>
              <li>Regular new articles written for your site</li>
              <li>A technical audit of your page every month</li>
              <li>Your business on Google Maps <span class="term">Google Business Profile</span></li>
              <li>We keep your site online, secure (padlock) and fast, with a WhatsApp button</li>
              <li>No setup fee · cancel anytime</li>
            </ul>
            <a class="btn btn-block" href="/signup/">Sign up now</a>
          </div>
          <div class="price-card accent reveal">
            <p class="pill">Optional top-up</p>
            <h2 class="h3">SEO Boost</h2>
            <p class="price"><span>S$10</span>/boost</p>
            <ul class="ticks">
              <li>Accelerated growth: more articles aimed at new niche keywords, on top of your regular ones</li>
              <li>Extra processing to fix SEO issues found in your audit</li>
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
            <a class="btn btn-block" href="/signup/" id="calc-signup">Sign up with this plan</a>
          </form>
        </div>
        <p class="note reveal" style="margin-top:32px">Why so low? AI now does the daily SEO work that used to be billed by the hour. <a class="link" href="/cheapest-seo-singapore/">Cheap SEO doesn't have to mean bad SEO →</a> · <a class="link" href="/cheapest-website-singapore/">A website without the lump sum →</a></p>
        <h2 class="reveal" style="margin-top:64px">Get Found vs SEO Boost</h2>
        """ + PLAN_COMPARE + """
        <div class="split" style="margin-top:56px">
          <div class="panel reveal">
            <h2 class="h3">How payment works</h2>
            <p>Message Edwin on WhatsApp. He confirms what you need, then sends payment details for your first month. SEO Boosts are added at sign-up or <a class="link" href="/seo-boost/#top-up">topped up anytime</a> the same way. Nothing is charged until you agree.</p>
          </div>
          <div class="panel reveal">
            <h2 class="h3">Your domain</h2>
            <p>A new domain is registered in your name and paid by you directly, usually S$15–30 a year. If you cancel, you keep it.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="section alt" id="compare-packages">
      <div class="wrap">
        <p class="kicker reveal">Comparing SEO packages?</p>
        <h2 class="reveal">What to check in any SEO package, and our answers</h2>
        <p class="section-lead reveal">SEO packages in Singapore are hard to compare: different keyword counts, minimum terms, setup fees and "guarantees". These are the lines that change what you actually pay and get. Ask every provider for theirs.</p>
        <div class="table-wrap reveal" style="margin-top:24px">
          <table class="compare">
            <thead><tr><th>Ask about</th><th>Why it matters</th><th>Page One Get Found</th></tr></thead>
            <tbody>
              <tr><th>Monthly price</th><td>Is it the full price, or before add-ons?</td><td><b>S$20</b> (introductory price), optional SEO Boosts S$10 each</td></tr>
              <tr><th>Setup or audit fee</th><td>Some packages charge one before month one</td><td>S$0</td></tr>
              <tr><th>Minimum term</th><td>Many SEO contracts have one; know yours before the first invoice</td><td>None, cancel anytime</td></tr>
              <tr><th>Website</th><td>Many SEO packages assume you already have one</td><td>Included: we build it if you don't have one</td></tr>
              <tr><th>Google Maps (Business Profile)</th><td>Local customers often find you on Maps first</td><td>Included</td></tr>
              <tr><th>AI search (ChatGPT, Google AI answers)</th><td>Often a separate or higher-tier package</td><td>Included: Bing, structured data and llms.txt</td></tr>
              <tr><th>Content</th><td>Who writes it, and is it about your customers' questions?</td><td>Regular new articles written for your site</td></tr>
              <tr><th>Seeing results yourself</th><td>A report made by the provider is not the same as Google's own numbers</td><td>Search Console connected, so you see your own Google numbers</td></tr>
              <tr><th>Ranking guarantee</th><td>No one controls Google's rankings</td><td>None, and be careful of anyone who offers one</td></tr>
            </tbody>
          </table>
        </div>
        <p class="note reveal">Comparing an agency retainer or an in-house hire? <a class="link" href="/seo-services-singapore/">SEO services in Singapore compared →</a> · Starting a new business? <a class="link" href="/new-business-website/">Your first-year cost, all in →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Questions</p>
        <h2 class="reveal">SEO pricing: your questions, answered</h2>
        <div style="margin-top:24px">
""" + "\n".join(f"        <details class=\"reveal\"><summary>{q}</summary><p>{a}</p></details>" for q, a in PRICING_FAQ) + """
        </div>
      </div>
    </section>

""" + cta(), crumb="Pricing", updated="2026-10-13")

# ---------- FAQ ----------
FAQS = [
    ("What is SEO, in simple words?", "SEO stands for search engine optimisation. In simple words, it means making your business easy for Google to find, understand and recommend, so you show up when customers search for what you sell. Today it also covers AI assistants like ChatGPT, which many people now ask for recommendations. See SEO explained simply for the common terms."),
    ("Can you build and manage a website for my new business?", "Yes. If you don't have a website, the S$20 Get Found plan includes building one on your own domain and managing it every month: hosting, security, speed, a monthly technical audit and small text and photo changes. It's usually live within 7 days. See our website page for details."),
    ("What do I get every month for S$20?", "Get Found means your business is discovered naturally: it shows up in the free, unpaid results on Google, Google Maps and ChatGPT when customers search for what you do, with no ad spend. We write regular new articles for your site, and every month we run a technical audit of your page to check that Google and AI assistants can still find, read and understand it. Your website or landing page stays online, secure and fast, with a WhatsApp button. Want to grow faster? SEO Boosts add more content aimed at new keywords on top."),
    ("I'm not good with computers. Do I need to do anything technical?", "No. You tell us about your business and send a few photos on WhatsApp, and we do the technical work: the website, Google and Bing setup, Google Maps and the AI-search setup. If you already have a website, there's one setting to add to your domain. We send simple step-by-step instructions, and Edwin can guide you through it."),
    ("How will I know it's working?", "We connect your website to Google Search Console, Google's own free report. It shows how many times you appeared in Google, how many people clicked, and what they searched. Every SEO Boost also comes with a before/after report of what was done."),
    ("Is there a setup fee or contract?", "No. There's no setup fee and no minimum contract. You pay S$20 a month in advance and can cancel anytime."),
    ("Will the S$20 price go up?", "Yes, a little. S$20 a month is an introductory price until we reach our early-client target, so now is the time to grab it. When it goes up, the new price will stay close to S$20, so SEO stays affordable for small businesses."),
    ('Is S$20 a month a gimmick price?', "No. S$20 isn't a teaser to upsell you later, and it isn't budget SEO with steps skipped. It's a baseline for what SEO costs now that AI does the daily work that used to be billed by the hour. The same system runs every website we manage, and it's proven on real businesses: " + PROOF_EG + ", according to Google Search Console. No setup fee, no contract, so you can judge it for yourself."),
    ("Is the free website check really free?", "Yes. Enter your website address on our homepage and the checker tests Google basics, mobile setup, speed and AI-search readiness in under a minute. No sign-up needed."),
    ("How do I reach you?", "WhatsApp Edwin on " + WA_DISPLAY + ". You can also tap the green chat button on any page. No obligation to buy anything."),
    ("How do I sign up and pay?", "Fill in the short form on our sign-up page or tap the chat button. It opens WhatsApp with your details filled in. Edwin confirms what you need and sends payment details for your first month. SEO Boosts are added or topped up the same way."),
    ("I already have a website. Do I need to change it?", "No. You give us a subdomain such as go.yourbrand.com and we build a separate SEO landing page there. Your current website stays exactly as it is. If you'd rather have someone look after your whole website, we can also take it over and manage it for you."),
    ("What is an SEO Boost?", "An optional S$10 top-up for accelerated growth. Your plan already includes regular articles; each Boost adds more content on top, aimed at new niche long-tail searches (specific phrases, like \"aircon chemical wash Tampines\", that fewer businesses compete for and that come from customers ready to buy) and do extra processing to fix the SEO issues found in your audit. You get a before/after report of what was done and what's next. Your S$20 plan works without it."),
    ("How do you help me show up in ChatGPT and other AI search?", "AI assistants like ChatGPT, Gemini and Perplexity rely on search indexes such as Bing and Google and on clearly structured information. We connect your site to Google and Bing, mark up your business details so machines can read them, publish an llms.txt file, and write content that answers the questions customers ask."),
    ("Who pays for the domain?", "If you need a new domain, it's registered in your name and you pay for it directly (usually S$15–30 a year). You always own your domain."),
    ("Do you have proof it works?", "Yes. Our results page shows real Google Search Console numbers from the businesses we run. " + PROOF_BOTH.replace(", according to Google Search Console", "") + " Results vary by business, so we don't guarantee them."),
    ("Do you guarantee first page on Google?", "No honest provider can guarantee rankings, because Google decides. We guarantee the work: every SEO Boost is documented in a before/after report so you can see exactly what changed."),
    ("How do I cancel?", "Just WhatsApp us. Your service runs to the end of the month you've paid for."),
    ("What happens if I cancel?", "Your site stays live until the end of the month you paid for. You keep your domain, and you can buy the site files if you want to host them elsewhere."),
    ("How long until my site is live?", "Usually within 7 days of receiving your details and photos."),
]
faq_html = "\n".join(
    f"        <details><summary>{q}</summary><p>{a.replace('go.yourbrand.com', '<code>go.yourbrand.com</code>').replace('llms.txt', '<code>llms.txt</code>').replace('results page', '<a class="link" href="/results/">results page</a>').replace('SEO explained simply', '<a class="link" href="/seo-explained/">SEO explained simply</a>').replace('our website page', '<a class="link" href="/website/">our website page</a>')}</p></details>"
    for q, a in FAQS)
page("faq/index.html",
     "FAQ: Fees, Contracts, SEO & AI Search | Page One Singapore",
     "Page One Singapore FAQ: introductory pricing, setup fees, contracts, signing up, SEO landing pages, SEO Boost, ChatGPT visibility and cancelling.",
     [{"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS]}],
     hero("FAQ", "", "Questions, answered",
          "Can't find yours? Tap the chat button and ask Edwin on WhatsApp. No obligation.", buttons=False) + """

    <section class="section">
      <div class="wrap narrow">
""" + faq_html + """
      </div>
    </section>

""" + cta(), crumb="FAQ")

# ---------- About ----------
page("about/index.html",
     "About Page One Singapore: Built by a Business Owner",
     "Page One Singapore was built by Edwin, an NUS Computer Science (Honours) graduate with 18+ years in business, and proven on real Singapore businesses first.",
     [{"@context": "https://schema.org", "@type": "AboutPage", "url": SITE + "/about/", "name": "About Page One Singapore",
       "about": PROVIDER, "mainEntity": dict(FOUNDER, worksFor=PROVIDER,
                                             owns={"@type": "AutoRepair", "name": "Edwin Garage", "url": "https://sggarage.com/"})}],
     hero("About", "Built by a business owner", "An SEO system built by a Singapore business owner, not an agency.",
          "Page One Singapore builds and looks after websites that get small businesses found on Google and ChatGPT, from S$20 a month. Our founder combines a computer science degree with 18+ years of running businesses, and every method was proven on real Singapore businesses before we offered it to you.", buttons=False) + """

    <section class="section">
      <div class="wrap split">
        <div class="reveal">
          <p class="kicker">Our founder</p>
          <h2>Meet Edwin</h2>
          <p>Edwin graduated from the National University of Singapore (NUS) with a Bachelor's degree in Computer Science with Honours, and has spent more than 18 years running businesses. He owns Edwin Garage, a car workshop in Ang Mo Kio.</p>
          <p>He built Page One to solve his own problem: getting found on Google without paying for work he couldn't see. He combined his computing background with AI to build a system that does the SEO work every day, and used it on his own workshop first.</p>
          <p>It worked. Edwin Garage now gets over 2,000 clicks a month from Google, and the same system runs every client website we manage today.</p>
          <a class="card-link" href="/results/">See the results →</a>
        </div>
        <div class="panel reveal">
          <h3>Why that matters to you</h3>
          <ul class="ticks">
            <li><b>Proven before it was sold.</b> Tested on real businesses, measured in Google Search Console.</li>
            <li><b>Built by someone who pays for marketing too.</b> Priced for what a new or small business can actually afford.</li>
            <li><b>Technical and practical.</b> Computer science for the system, 18+ years of business sense for what brings in customers.</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap split">
        <div class="reveal">
          <p class="kicker">Why we exist</p>
          <h2>Online visibility shouldn't need a big budget</h2>
          <p>Page One Singapore runs the websites and Google listings for """ + LIVE_COUNT_WORD + """ local businesses today, from a car workshop and a car detailing service to a sofa cleaning company, a property agent and a financial consultant. <a class="link" href="/clients/">See them all</a>.</p>
          <p>We started because new and small businesses were being quoted hundreds of dollars a month for SEO they couldn't see or measure. So we built a simpler way: S$20 a month, a report for every SEO Boost, and no contract. Start small, and add more only when you see it working.</p>
          <p>Page One Singapore is a project of Snap Commercial Pte. Ltd., a Singapore company registered in 2022 (UEN 202209904W).</p>
          <a class="card-link" href="/#stories">See the websites we run →</a>
          <p><a class="link" href="/is-page-one-singapore-legit/">Is Page One legit? Check every claim yourself →</a></p>
        </div>
        <div class="panel reveal" style="background:#fff">
          <h3>How we work</h3>
          <ul class="ticks">
            <li><b>Honest.</b> No one can guarantee Google rankings, so we never promise them. We show you the work and the numbers instead.</li>
            <li><b>Transparent.</b> Every SEO Boost comes with a before/after report.</li>
            <li><b>No lock-in.</b> No setup fee, no contract. You own your domain.</li>
            <li><b>Reachable.</b> WhatsApp Edwin directly. He replies personally.</li>
            <li><b>Local.</b> We serve businesses across Singapore.</li>
          </ul>
        </div>
      </div>
    </section>

""" + glance() + """

""" + cta("Talk to us, no obligation", "Ask Edwin anything on WhatsApp. Or start with a free website check."),
     crumb="About", updated=AIV_UPDATED)

# ---------- Results ----------
# Every figure below comes from builder/showcase.json (Google Search Console via CaseStudyStats in the
# SearchInsight Bridge app). Refresh with builder/showcase_refresh.py; never edit numbers by hand.
DATA_THROUGH = THROUGH


def kpis(items):
    return '<div class="kpis">' + "".join(
        f'<div class="kpi"><div class="label">{l}</div><div class="value">{v}</div><div class="delta">{d}</div></div>'
        for l, v, d in items) + "</div>"


def months_table(rows):
    body = "".join(f"<tr><td>{m}</td><td>{c}</td><td>{i}</td><td>{p}</td></tr>" for m, c, i, p in rows)
    return ('<div class="table-wrap"><table><thead><tr><th>Month (2026)</th><th>Clicks from Google</th>'
            '<th>Times shown on Google</th><th>Average position</th></tr></thead><tbody>' + body + "</tbody></table></div>")


def ranks_table(rows):
    body = "".join(f"<tr><td>{q}</td><td>{p}</td><td>{i}</td></tr>" for q, p, i in rows)
    return ('<div class="table-wrap"><table><thead><tr><th>Search on Google</th><th>Average position</th>'
            '<th>Times shown (28 days)</th></tr></thead><tbody>' + body + "</tbody></table></div>")


def _month_change(key, field):
    m = G[key]["full_months"]
    a, b = m[0], m[-1]
    return (f"{_n(b[field])}", month_long(b["month"]).split()[0] + " " + b["month"][:4],
            _n(a[field]), month_long(a["month"]).split()[0])


_eg_c, _eg_i = _month_change("sggarage", "clicks"), _month_change("sggarage", "impressions")
_cl_c, _cl_i = _month_change("cleanic", "clicks"), _month_change("cleanic", "impressions")
_eg_pos = [m["position"] for m in G["sggarage"]["full_months"]]
_others = [c for c in SC["clients"] if stage(c["key"]) != "case"]
_others_html = "\n".join(
    f'          <div class="card reveal"><p class="pill">{pill(c["key"])}</p><h3>{c["name"]}</h3><p>{result_text(c["key"])}</p>'
    f'<p><a class="link" href="{c["url"]}" target="_blank" rel="noopener">{c["domain"]} ↗</a></p></div>' for c in _others)

RESULTS_FAQ = [
    ("Where do these numbers come from?", "Every figure on this page comes from Google Search Console, Google's own report of how a website performs in Google Search. We collect the final data automatically and don't edit it. Data runs to " + DATA_THROUGH + "."),
    ("What does average position mean?", "Where the website appears in Google results, on average, when someone searches. Positions 1 to 10 are page one. A lower number is better."),
    ("Will my business get the same results?", "We can't promise that, and no honest provider can. Results depend on your industry, competition and how long your site has been running. Edwin Garage and Cleanic Detailing took about three months to get here. What we can promise is the same system and a report showing the work."),
    ("Can I see the full report?", "Yes. WhatsApp us and we'll walk you through the Search Console reports behind this page. No obligation."),
]

page("results/index.html",
     "SEO Case Studies Singapore: Real Google Results | Page One",
     f"Real Google Search Console results from Singapore businesses on Page One. Edwin Garage: {EG['clicks']} clicks from Google in the 28 days to {THROUGH_SHORT}, position {EG['pos']}.",
     [{"@context": "https://schema.org", "@type": "CollectionPage", "url": SITE + "/results/",
       "name": "SEO Results & Case Studies", "about": PROVIDER, "inLanguage": "en-SG", "dateModified": SC_UPDATED,
       "hasPart": [
           {"@type": "Article", "headline": f"Edwin Garage: from first Google data to {EG['clicks']} clicks in 28 days",
            "url": SITE + "/results/#edwin-garage", "author": {"@type": "Person", "name": "Edwin"}, "publisher": PROVIDER,
            "datePublished": UPDATED, "dateModified": SC_UPDATED, "about": {"@type": "AutoRepair", "name": "Edwin Garage", "url": "https://sggarage.com/"}},
           {"@type": "Article", "headline": f"Cleanic Detailing: page one for {CL['page_one']} searches within four months",
            "url": SITE + "/results/#cleanic-detailing", "author": {"@type": "Person", "name": "Edwin"}, "publisher": PROVIDER,
            "datePublished": UPDATED, "dateModified": SC_UPDATED, "about": {"@type": "LocalBusiness", "name": "Cleanic Detailing", "url": "https://cleanicdetailing.com/"}}]},
      {"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in RESULTS_FAQ]}],
     hero("Results", "Straight from Google Search Console",
          "Real results, on real Singapore businesses.",
          "We built Page One on our own businesses first. These are their actual Google numbers, unedited, with data to " + DATA_THROUGH + ".", buttons=False) + """

    <section class="section">
      <div class="wrap">
        <p class="kicker reveal">At a glance</p>
        <h2 class="reveal">Two businesses, about three months of SEO</h2>
        <p class="section-lead reveal">Last 28 days (""" + WINDOW + """), compared with the 28 days before (""" + PREV_WINDOW + """). "Page one" means an average position of 1 to 10 on Google.</p>
        <div class="reveal">""" + kpis([
            ("Edwin Garage: clicks from Google", EG["clicks"], f"Up from {EG['prev_clicks']} · average position {EG['pos']}"),
            ("Edwin Garage: searches on page one", EG["page_one"], f"{EG['top3']} in the top 3"),
            ("Cleanic Detailing: clicks from Google", CL["clicks"], f"Up from {CL['prev_clicks']} · average position {CL['pos']}, from {CL['prev_pos']}"),
            ("Cleanic Detailing: searches on page one", CL["page_one"], f"{CL['top3']} in the top 3"),
        ]) + """</div>
        <p class="note reveal">Want to see the websites themselves? <a class="link" href="/clients/">See every client website →</a></p>
      </div>
    </section>

    <section class="section alt" id="edwin-garage">
      <div class="wrap">
        <p class="kicker reveal">Case study 1 · Car workshop, Ang Mo Kio</p>
        <h2 class="reveal">Edwin Garage: from first Google data to """ + EG["clicks"] + """ clicks in 28 days</h2>
        <div class="split" style="margin-top:24px">
          <div class="reveal">
            <p>Edwin Garage is our founder's own car workshop, and the first business to run on the Page One system. Its Search Console data starts on """ + EG["first_long"] + """. Within three months, Google was sending it more than 2,000 visitors a month.</p>
            <ul class="ticks">
              <li><b>""" + _eg_c[0] + """ clicks</b> from Google in """ + _eg_c[1] + """, up from """ + _eg_c[2] + """ in """ + _eg_c[3] + """</li>
              <li><b>""" + _eg_i[0] + """ times shown</b> on Google in """ + _eg_i[1].split()[0] + """, up from """ + _eg_i[2] + """ in """ + _eg_i[3] + """</li>
              <li>Average position between <b>""" + f"{min(_eg_pos):.1f} and {max(_eg_pos):.1f}" + """</b> every full month since launch, which is page one</li>
              <li>On page one for <b>""" + EG["page_one"] + """ different searches</b> in the 28 days to """ + THROUGH_SHORT + """</li>
            </ul>
          </div>
          <div class="panel reveal" style="background:#fff">
            <h3>What we did</h3>
            <ul class="ticks">
              <li>A fast website with a page for each service customers search for</li>
              <li>Google Business Profile, Search Console and Bing set up</li>
              <li>Business details marked up for Google and AI assistants, plus <code>llms.txt</code></li>
              <li>Helpful articles published regularly, picked from real Search Console data</li>
            </ul>
          </div>
        </div>
        <h3 class="reveal" style="margin-top:40px">Month by month</h3>
        <div class="reveal">""" + months_table(months_rows("sggarage")) + """</div>
        <h3 class="reveal">Where it shows up on Google</h3>
        <p class="reveal">A few of the searches it ranks for (28 days to """ + THROUGH_SHORT + """):</p>
        <div class="reveal">""" + ranks_table(query_rows("sggarage")) + """</div>
        <a class="card-link reveal" href="https://sggarage.com/" target="_blank" rel="noopener">Visit sggarage.com ↗</a>
      </div>
    </section>

    <section class="section" id="cleanic-detailing">
      <div class="wrap">
        <p class="kicker reveal">Case study 2 · Mobile car detailing</p>
        <h2 class="reveal">Cleanic Detailing: page one for """ + CL["page_one"] + """ searches within four months</h2>
        <div class="split" style="margin-top:24px">
          <div class="reveal">
            <p>Cleanic Detailing is a mobile car grooming and fumigation service run by Colin Loo. Its Search Console data starts on """ + CL["first_long"] + """. It now ranks in the top 3 for searches like """ + top3_examples("cleanic") + """.</p>
            <ul class="ticks">
              <li><b>""" + _cl_c[0] + """ clicks</b> from Google in """ + _cl_c[1] + """, up from """ + _cl_c[2] + """ in """ + _cl_c[3] + """</li>
              <li><b>""" + _cl_i[0] + """ times shown</b> on Google in """ + _cl_i[1].split()[0] + """, up from """ + _cl_i[2] + """ in """ + _cl_i[3] + """</li>
              <li>Average position improved to <b>""" + CL["pos"] + """</b> in the 28 days to """ + THROUGH_SHORT + """, from """ + CL["prev_pos"] + """ the 28 days before</li>
              <li>On page one for <b>""" + CL["page_one"] + """ different searches</b>, """ + CL["top3"] + """ of them in the top 3</li>
            </ul>
          </div>
          <div class="panel reveal">
            <h3>What we did</h3>
            <ul class="ticks">
              <li>Service pages for car grooming, steam cleaning, fumigation and odour removal</li>
              <li>Guides on the problems customers search for, like cockroaches or vomit in the car</li>
              <li>Google Business Profile, Search Console, Bing and structured data set up</li>
              <li>New articles chosen from the searches Google already shows the site for</li>
            </ul>
          </div>
        </div>
        <h3 class="reveal" style="margin-top:40px">Month by month</h3>
        <div class="reveal">""" + months_table(months_rows("cleanic")) + """</div>
        <h3 class="reveal">Where it shows up on Google</h3>
        <p class="reveal">A few of the searches it ranks for (28 days to """ + THROUGH_SHORT + """):</p>
        <div class="reveal">""" + ranks_table(query_rows("cleanic")) + """</div>
        <a class="card-link reveal" href="https://cleanicdetailing.com/" target="_blank" rel="noopener">Visit cleanicdetailing.com ↗</a>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap">
        <p class="kicker reveal">Newer websites</p>
        <h2 class="reveal">The other """ + LIVE_COUNT_WORD_OTHERS + """, shown honestly</h2>
        <p class="section-lead reveal">SEO takes time. These sites started later, so their numbers are smaller, or not there yet. We show them anyway, because that's what an honest early stage looks like.</p>
        <div class="cards three">
""" + _others_html + """
        </div>
        <p class="note reveal"><a class="card-link" href="/clients/">See all the client websites →</a></p>
      </div>
    </section>

    <section class="section">
      <div class="wrap narrow">
        <p class="kicker reveal">Reading the numbers</p>
        <h2 class="reveal">Questions about these results</h2>
""" + "".join(f"""        <details><summary>{q}</summary><p>{a}</p></details>
""" for q, a in RESULTS_FAQ) + """      </div>
    </section>

""" + cta("Want this for your business?", "Sign up at the introductory price, or check where your website stands today. No obligation."),
     crumb="Results", updated=SC_UPDATED)


# ---------- Contact ----------
page("contact/index.html",
     "Contact Page One Singapore: WhatsApp Edwin, +65 9785 6612",
     "Ask Page One Singapore about websites, SEO and getting found on Google and AI search. WhatsApp Edwin on +65 9785 6612; he replies personally. No obligation.",
     [{"@context": "https://schema.org", "@type": "ContactPage", "url": SITE + "/contact/", "name": "Contact Page One Singapore", "about": PROVIDER}],
     hero("Contact", "Edwin replies personally", "Questions? Chat with Edwin.",
          "The fastest way to reach us is WhatsApp. No obligation to buy anything.", buttons=False) + f"""

    <section class="section">
      <div class="wrap split">
        <div class="reveal">
          <p class="kicker">WhatsApp</p>
          <h2>{WA_DISPLAY}</h2>
          <a class="btn" href="{WA_LINK}" target="_blank" rel="noopener" style="margin-bottom:28px">Chat on WhatsApp</a>
          <p>Or tell us a bit first, and we'll open WhatsApp with it filled in:</p>
          <form class="lead-form" id="lead-form" novalidate>
            <label>Your name<input name="name" required autocomplete="name"></label>
            <label>Business name<input name="business" autocomplete="organization"></label>
            <label>Website (if any)<input name="website" inputmode="url" placeholder="yourbusiness.com.sg"></label>
            <label>How can we help?<textarea name="message" rows="4" maxlength="1500"></textarea></label>
            <p class="form-error" role="alert" hidden></p>
            <button class="btn btn-block" type="submit">Send on WhatsApp</button>
            <p class="fine">Opens WhatsApp with your message filled in. You choose whether to send it. See our <a href="/privacy/">privacy policy</a>.</p>
          </form>
        </div>
        <div class="panel reveal">
          <h3>Faster answers</h3>
          <ul class="ticks">
            <li><a class="link" href="/results/">See real results</a> from businesses we run</li>
            <li><a class="link" href="/#check">Check your website free</a> in under a minute</li>
            <li><a class="link" href="/faq/">Read the FAQ</a>: fees, contracts, cancelling</li>
            <li><a class="link" href="/signup/">Sign up</a> at the introductory price</li>
            <li><a class="link" href="{GBP}" target="_blank" rel="noopener">Find us on Google Maps</a> and read our reviews</li>
          </ul>
          <p class="fine">Already a client and want to change or cancel your plan? Just WhatsApp us.</p>
        </div>
      </div>
    </section>

    <section class="section alt">
      <div class="wrap narrow">
        <p class="kicker reveal">Who you are talking to</p>
        <h2 class="reveal">Business details</h2>
        <div class="table-wrap reveal">
          <table class="compare">
          <tr><th>Business</th><td>Page One Singapore, a done-for-you website and SEO service for Singapore small businesses</td></tr>
          <tr><th>Company</th><td>A project of Snap Commercial Pte. Ltd., UEN 202209904W, incorporated in Singapore on 23 March 2022. You can look the UEN up on <a class="link" href="https://www.bizfile.gov.sg/" target="_blank" rel="noopener">ACRA Bizfile</a>.</td></tr>
          <tr><th>Founder</th><td>Edwin, NUS Computer Science (Honours). <a class="link" href="/about/">About Edwin →</a></td></tr>
          <tr><th>WhatsApp and phone</th><td><a class="link" href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a></td></tr>
          <tr><th>Area served</th><td>Singapore, island-wide.</td></tr>
          <tr><th>Google Maps</th><td><a class="link" href="{GBP}" target="_blank" rel="noopener">Page One Singapore on Google</a></td></tr>
        </table></div>
        <p class="note reveal">Want to check us before you message? <a class="link" href="/is-page-one-singapore-legit/">Every claim with a way to verify it →</a> <a class="link" href="/clients/">The client websites we run →</a></p>
      </div>
    </section>
""", crumb="Contact", updated="2026-10-15")

# ---------- Privacy ----------
page("privacy/index.html",
     "Privacy Policy | Page One Singapore",
     "How Page One Singapore collects, uses and protects your personal data, in line with Singapore's Personal Data Protection Act (PDPA).",
     [],
     hero("Privacy policy", "", "Privacy policy", "Last updated 9 October 2026", buttons=False) + f"""

    <section class="section">
      <div class="wrap narrow prose">
        <p>Page One Singapore ("we", "us"), a project of Snap Commercial Pte. Ltd. (UEN 202209904W), respects your privacy. This policy explains how we handle personal data in line with Singapore's Personal Data Protection Act 2012 (PDPA).</p>
        <h2>What we collect</h2>
        <p>Only what you choose to send us: your name, phone number, business name, website and messages when you contact us on WhatsApp, the website address you enter in our free checker, and any photos or information you share for your website.</p>
        <h2>How we use it</h2>
        <ul>
          <li>To reply to your enquiry and run the website checks you ask for</li>
          <li>To build and maintain your website or landing page</li>
          <li>To set up your Google Business Profile and search listings, with your permission</li>
          <li>To arrange payment and send SEO Boost reports</li>
        </ul>
        <p>We don't sell your personal data, and we don't use it for marketing unrelated to your enquiry.</p>
        <h2>Sharing</h2>
        <p>We share data only as needed to deliver our service, for example with our web host, domain registrar, Google and Bing, our cloud platform (Base44), WhatsApp, and payment providers. These providers handle data under their own privacy policies.</p>
        <h2>This website</h2>
        <p>This site doesn't use advertising or tracking cookies. It loads fonts from Google Fonts and stores a small note in your browser so the chat pop-up doesn't repeat. To see which pages are useful, it counts visits and button clicks anonymously: the page, how you arrived (for example Google or ChatGPT), your device type and a random ID kept in your browser. This never includes your name or phone number, and it's switched off if your browser sends a Do Not Track signal. Our forms don't send data to us directly; they open WhatsApp with your details filled in, and you choose whether to send them. To stop abuse of the free checker, we keep a one-way scrambled code of your IP address (not the address itself) for rate limiting.</p>
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
     hero("Terms of service", "", "Terms of service", "Last updated 9 October 2026", buttons=False) + f"""

    <section class="section">
      <div class="wrap narrow prose">
        <p>These terms apply when you use Page One Singapore's services. Page One Singapore is a project of Snap Commercial Pte. Ltd. (UEN 202209904W), which provides the services. By signing up, you agree to these terms.</p>
        <h2>Our services</h2>
        <p><b>Get Found</b> (S$20 a month, an introductory price) covers a website on your own domain or a landing page on your subdomain, plus the Google and AI search setup described on our <a href="/get-found/">Get Found page</a> and regular new articles for your site. <b>SEO Boost</b> (S$10 each) is an optional round of improvements with a report.</p>
        <h2>Payment</h2>
        <p>The monthly fee is paid in advance. SEO Boosts are paid when you top up. We arrange payment over WhatsApp. Prices are in Singapore dollars.</p>
        <h2>Introductory price</h2>
        <p>S$20 a month is an introductory price for a limited time. We will raise the price for new sign-ups once we reach our early-client target, and we intend to keep the new price close to S$20. We'll tell you before any price change applies to your own subscription.</p>
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
        <p>Questions? WhatsApp us on <a href="{WA_LINK}" target="_blank" rel="noopener">{WA_DISPLAY}</a>.</p>
      </div>
    </section>
""", crumb="Terms of service")

# ---------- Sign up ----------
page("signup/index.html",
     "Sign Up: Get Found from S$20/month | Page One Singapore",
     "Sign up for the Get Found plan at the introductory price of S$20/month: website, Google and AI search setup, articles and monthly audits. No setup fee or contract.",
     [service("Get Found basic subscription", "/signup/",
              "A website or SEO landing page set up for Google Search, Google Maps and AI assistants. Introductory price, billed monthly.", "20")],
     hero("Sign up", "Introductory price · limited time", "Get found on Google and AI from S$20 a month.",
          "Tell us a little about your business and continue on WhatsApp with Edwin. No setup fee, no contract, cancel anytime.", buttons=False) + """

    <section class="section">
      <div class="wrap signup-grid">
        <form class="signup-card reveal" id="signup-form" novalidate>
          <p class="pill">Get Found plan</p>
          <p class="price"><span>S$20</span>/month</p>
          <p class="intro-note"><span class="intro-tag">Introductory price</span> The price goes up once we reach our early-client target, so grab it now. Any new price will stay close to S$20, so it stays affordable.</p>
          <label>Business name<input name="business" required autocomplete="organization" maxlength="100"></label>
          <label>Your name<input name="name" required autocomplete="name" maxlength="80"></label>
          <label>What does your business do? (optional)<input name="industry" maxlength="120" placeholder="e.g. hair salon in Bedok"></label>
          <label>Current website (if any)<input name="website" inputmode="url" placeholder="yourbusiness.com.sg" maxlength="200"></label>
          <fieldset class="boost-pick">
            <legend>Add SEO Boosts for faster results? <small>S$10 each, charged once</small></legend>
            <label><input type="radio" name="boosts" value="0" checked> None</label>
            <label><input type="radio" name="boosts" value="1"> 1</label>
            <label><input type="radio" name="boosts" value="2"> 2</label>
            <label><input type="radio" name="boosts" value="4"> 4</label>
          </fieldset>
          <div class="total" aria-live="polite"><span>First month</span><strong id="signup-total">S$20</strong><span id="signup-then">then S$20/month</span></div>
          <p class="form-error" role="alert" hidden></p>
          <button class="btn btn-block" type="submit">Continue on WhatsApp</button>
          <p class="fine">Opens WhatsApp with your details filled in. Edwin confirms what you need and sends payment details. Nothing is charged until you agree. See our <a href="/terms/">terms</a>.</p>
        </form>
        <div class="reveal">
          <h2 class="h3">What you get</h2>
          <ul class="ticks">
            <li>Found naturally on Google and ChatGPT: free, unpaid results, no ad spend</li>
            <li>A technical audit of your page every month</li>
            <li>Your own website, or an SEO landing page on your current site's subdomain</li>
            <li>Google Business Profile set up and completed</li>
            <li>Google Search Console and Bing connected (Bing feeds ChatGPT search)</li>
            <li>Business details marked up for Google and AI assistants</li>
            <li>Fast hosting, SSL padlock, small changes when you need them</li>
            <li>Usually live within 7 days</li>
          </ul>
          <h2 class="h3" style="margin-top:32px">What happens next</h2>
          <ol class="mini-steps">
            <li>Chat with Edwin on WhatsApp and confirm your plan.</li>
            <li>Send your details and a few photos, and pay your first month.</li>
            <li>Your site goes live, connected to Google, Maps and Bing.</li>
          </ol>
          <p class="fine" style="margin-top:20px">Proof it works: <a class="link" href="/results/">see real Google Search Console results</a>. Questions? <a class="link" href="""+ "\"" + WA_LINK + "\"" + """ target="_blank" rel="noopener">WhatsApp Edwin</a>.</p>
        </div>
      </div>
    </section>
""", crumb="Sign up")

page("signup/success/index.html",
     "Thank You for Signing Up | Page One Singapore",
     "Your Page One Singapore sign-up is confirmed.",
     [],
     hero("Sign up", "Thank you", "Thank you for signing up!",
          "Edwin will be in touch on WhatsApp to get you started.", buttons=False) + """

    <section class="section">
      <div class="wrap narrow">
        <h2 class="h3">What happens next</h2>
        <ol class="mini-steps">
          <li>We'll contact you on WhatsApp to collect your business details and a few photos.</li>
          <li>We build your website or landing page and connect it to Google, Maps and Bing. Usually live within 7 days.</li>
          <li>You pay S$20 each month until you cancel. Cancel anytime by WhatsApp.</li>
        </ol>
        <p>Want faster results? <a class="link" href="/seo-boost/#top-up">Top up SEO Boosts</a> anytime.</p>
      </div>
    </section>
""", crumb="Sign up", robots="noindex, follow")

# ---------- Sample report ----------
page("report.html",
     "Sample SEO Boost Report | Page One Singapore",
     "See what one S$10 SEO Boost from Page One Singapore delivers: Google and AI visibility checks, improvements made, and a before/after report.",
     [],
     open(os.path.join(HERE, "report_body.html"), encoding="utf-8").read(), crumb="Sample report",
     # Kept out of Google: it's a fictional sample, and Search Console showed it ranking
     # for our own brand search ("page one") instead of the homepage.
     robots="noindex, follow")

# ---------- 404 ----------
page("404.html",
     "Page Not Found | Page One Singapore",
     "The page you're looking for doesn't exist.",
     [],
     # /check/<site> links (from prospect messages) go to the homepage checker, which runs the report.
     """    <script>(function(){var m=location.pathname.match(/^\\/check\\/(.+)$/);if(m){var s=m[1];try{s=decodeURIComponent(s)}catch(e){}location.replace("/?check="+encodeURIComponent(s.replace(/\\/+$/,""))+"#check")}})();</script>
""" + hero("Not found", "", "This page doesn't exist.",
          "It may have moved. Try one of these, or WhatsApp us.", buttons=False) + """

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

# ---------- SEO explained simply (glossary) ----------
GLOSSARY = [
    ("found", "Being found on Google", [
        ("seo", "Showing up when customers search", "SEO (search engine optimisation)",
         "Making your business easy for Google to find, understand and recommend, so you appear when people search for what you sell.",
         "People searching on Google are already looking to buy. Unlike ads, you don't pay each time someone clicks on an unpaid result.",
         "Everything on this page, set up when you join and kept up every month."),
        ("keywords", "The words customers type", "Keywords / search queries",
         "The exact words people type into Google, like \"car aircon repair\" or \"sofa cleaning Tampines\".",
         "If your website doesn't use the words your customers use, Google has no reason to show you for them.",
         "We write your pages around the real searches in your trade and area."),
        ("indexing", "Being listed by Google", "Indexing",
         "Google keeping a copy of your page in its library, so it can show it in search results.",
         "A page that isn't indexed can't appear on Google at all, however good it is.",
         "We submit your site to Google and Bing and check your pages get listed."),
        ("sitemap", "A list of your pages for Google", "XML sitemap",
         "A simple file listing every page on your website, made for search engines.",
         "It helps Google find all your pages, not just the homepage.",
         "We create it and keep it up to date for you."),
        ("long-tail", "Niche, specific searches", "Long-tail keywords",
         "Longer, very specific searches, like \"aircon chemical wash Tampines\" instead of just \"aircon\".",
         "Fewer businesses compete for them, and the people typing them usually know exactly what they want, so they're more likely to call.",
         "Each SEO Boost goes after niche long-tail searches for your business."),
        ("title", "Your headline on Google", "Title tag and meta description",
         "The blue headline and the short description under it that people see in Google results.",
         "It's your shop sign in the search results. A clear one gets more people to tap on you instead of a competitor.",
         "We write them for every page."),
        ("landing-page", "A page built to bring in customers", "Landing page and subdomain",
         "A page designed for one job, such as getting enquiries for one service. A subdomain is an extra address on your own domain, like go.yourbrand.com.",
         "If you already have a website, a landing page lets us add an SEO page without touching your current site.",
         "If you have a website, we build your landing page on a subdomain. You keep your current site as it is."),
    ]),
    ("local", "Google Maps and local searches", [
        ("gbp", "Your listing on Google Maps", "Google Business Profile (GBP)",
         "Your free business listing on Google Maps, and the box with your hours, photos, reviews and phone number that appears on the right of Google Search.",
         "For \"near me\" searches, this listing is often the first thing customers see, before any website.",
         "We set it up and complete it as part of Get Found."),
        ("local-seo", "Being found by people nearby", "Local SEO",
         "Helping your business show up for searches in your area, like \"plumber Jurong\" or \"near me\".",
         "Most small businesses serve their own area. Local searches are the customers most likely to call.",
         "We add your location or service area to your website, Google listing and business details."),
        ("nap", "Same name, address and phone everywhere", "NAP consistency",
         "Your business Name, Address and Phone number written the same way everywhere they appear online.",
         "If they don't match, Google is less sure the details are correct, and customers can get confused.",
         "We keep them the same on your website, Google listing and business details."),
    ]),
    ("ai", "ChatGPT and AI assistants", [
        ("ai-search", "Getting recommended by AI", "AI search / GEO (generative engine optimisation)",
         "More people now ask ChatGPT, Gemini or Perplexity for recommendations instead of typing into Google. Making your business easy for these tools to find and describe is called GEO, or AEO (answer engine optimisation).",
         "If an AI assistant can't read your website, it can't recommend you.",
         "We connect your site to Bing (which ChatGPT search uses), label your business details for machines, and write content that answers customers' questions."),
        ("schema", "Business details labelled for machines", "Structured data (Schema.org)",
         "Hidden labels in your website's code that tell Google and AI, for example, \"this is our phone number\" and \"these are our opening hours\".",
         "Without them, machines have to guess your details, and sometimes guess wrong.",
         "We add them to your website as part of Get Found."),
        ("llms", "A summary of your business for AI tools", "llms.txt",
         "A short plain-text file that sums up your business and links to your main pages, written for AI tools to read.",
         "It's a new, emerging standard: nice to have, and cheap to add.",
         "We publish one on your website."),
        ("crawlers", "Letting AI tools read your site", "Crawlers / bots and robots.txt",
         "Google and AI companies use programs called crawlers to read websites. A small file called robots.txt tells them what they may read.",
         "Some websites block AI crawlers by accident, so those tools can never recommend them.",
         "We make sure Google, Bing and AI assistants aren't blocked."),
    ]),
    ("website", "Your website", [
        ("mobile", "Works well on a phone", "Mobile-first / responsive design",
         "A website that fits and works properly on a phone screen. Google mainly looks at the phone version of your site.",
         "Most of your customers will find you on their phone. A site that's hard to use there loses them.",
         "Every site and landing page we build is designed for phones first."),
        ("speed", "How fast your website feels", "Page speed / Core Web Vitals",
         "Google's measures of how quickly a page shows its main content (LCP), whether things jump around while loading (CLS), and how fast it reacts to taps (INP).",
         "Slow pages make people press back. Google also uses these measures as a ranking signal.",
         "We build lightweight pages and host them on fast servers. Our free checker shows your own scores."),
        ("https", "The padlock in the address bar", "HTTPS / SSL certificate",
         "A security certificate that encrypts the connection between your website and your visitor.",
         "Without it, browsers label your site \"Not secure\", which puts customers off. Google prefers secure sites.",
         "Included with your hosting."),
    ]),
    ("measuring", "Measuring results", [
        ("audit", "A health check of your page", "Technical SEO audit",
         "A check of whether Google and AI assistants can find your page, read it and understand it: things like loading, mobile layout, page titles and business details.",
         "Small technical problems can quietly stop you showing up, even when everything looks fine to you.",
         "Included every month in your S$20 Get Found plan. SEO Boosts add extra processing to fix the issues it finds."),
        ("gsc", "Google's free report on your website", "Google Search Console (GSC)",
         "A free tool from Google that shows how your website performs in Google Search: how often you appear, how many people click, and what they searched.",
         "It's real data straight from Google, not a guess. Our results page uses it too.",
         "We connect it for you, and use it to decide what to improve."),
        ("impressions", "How often you were seen", "Impressions",
         "The number of times your website appeared in someone's Google results, even if they didn't click.",
         "A rising number means Google is showing you for more searches.", None),
        ("clicks", "People who visited from Google", "Clicks and CTR (click-through rate)",
         "Clicks are people who tapped through to your website from Google. CTR is the share of people who clicked after seeing you: 50 clicks from 1,000 impressions is a 5% CTR.",
         "Clicks are real potential customers. A low CTR usually means your headline on Google needs work.", None),
        ("position", "Where you appear on Google", "Average position",
         "Your average spot in Google's results. 1 is the top result, and 1 to 10 is roughly page one. Lower is better.",
         "Most people never look past page one, so getting into the top 10 is where the clicks are. For example, Edwin Garage averaged position " + EG["pos"] + " in the 28 days to " + THROUGH + ".", None),
        ("organic", "Free results vs paid ads", "Organic vs paid search",
         "Organic results are the normal, unpaid listings. Paid results are ads marked \"Sponsored\", where you pay Google for every click.",
         "Ads stop the moment you stop paying. Organic visibility keeps working in the background.",
         "Our plans work on your organic (unpaid) visibility. There's no ad spend."),
    ]),
]

_gl_cards = []
_gl_terms = []
for gid, gname, terms in GLOSSARY:
    arts = []
    for tid, plain, tech, what, why, we in terms:
        we_html = f'\n            <p class="we"><b>What we do:</b> {we}</p>' if we else ""
        arts.append(f"""          <article class="reveal" id="{tid}">
            <h3>{plain}<br><span class="term">{tech}</span></h3>
            <p><b>In plain English:</b> {what}</p>
            <p><b>Why it matters:</b> {why}</p>{we_html}
          </article>""")
        _gl_terms.append({"@type": "DefinedTerm", "@id": SITE + "/seo-explained/#" + tid, "name": tech.replace("&amp;", "&"),
                          "alternateName": plain, "description": what, "url": SITE + "/seo-explained/#" + tid})
    _gl_cards.append(f"""    <section class="section{' alt' if len(_gl_cards) % 2 else ''}" id="{gid}">
      <div class="wrap">
        <h2 class="reveal">{gname}</h2>
        <div class="gloss">
""" + "\n".join(arts) + """
        </div>
      </div>
    </section>""")

_gl_nav = "".join(f'<li><a href="#{gid}">{gname}</a></li>' for gid, gname, _ in GLOSSARY)
page("seo-explained/index.html",
     "SEO Explained Simply: Jargon in Plain English | Page One SG",
     "SEO, Google Business Profile, structured data, Core Web Vitals, Search Console and AI search, explained in plain English for Singapore business owners.",
     [{"@context": "https://schema.org", "@type": "DefinedTermSet", "@id": SITE + "/seo-explained/#terms",
       "name": "SEO and AI search terms, explained simply", "url": SITE + "/seo-explained/", "inLanguage": "en-SG",
       "hasDefinedTerm": _gl_terms}],
     hero("SEO explained simply", "No jargon needed", "SEO and AI search, explained simply.",
          "You don't need to understand any of this to work with us. But if you'd like to know what we're doing for your business, here's what each term means, why it matters and what we do about it. The technical name is in grey, in case you hear it elsewhere.", buttons=False) + f"""

    <section class="section" style="padding-bottom:0">
      <div class="wrap">
        <ul class="gloss-nav" aria-label="Topics">{_gl_nav}</ul>
      </div>
    </section>

""" + "\n\n".join(_gl_cards) + """

""" + cta("Still not sure? Just ask.", "No question is too basic. WhatsApp Edwin and he'll explain how it applies to your business. No obligation."),
     crumb="SEO explained simply")


# ---------- Home ----------
HOME_QA = [('What is Page One Singapore?', 'Page One Singapore is an affordable SEO service for Singapore small businesses. It gets businesses found on Google Search, Google Maps and AI assistants such as ChatGPT. It was built by Edwin, an NUS Computer Science (Honours) graduate with 18+ years in business, and proven first on his own car workshop, Edwin Garage.'), ('How much does SEO cost with Page One Singapore?', 'The Get Found plan is S$20 a month at an introductory price, with no setup fee and no minimum contract. Optional SEO Boosts cost S$10 each, for when you want faster results.'), ('What do I get every month for S$20?', 'Your business is found naturally in the free, unpaid results on Google, Google Maps and ChatGPT. We write regular new articles for your site and run a technical audit of your page every month. Your website or SEO landing page is kept online, secure and fast, with a WhatsApp button. Want to grow faster? SEO Boosts add more content aimed at new keywords.'), ('Does it actually work?', PROOF_BOTH + " Results vary by business, so we don't guarantee rankings.")]
HOME_FAQ_LD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in HOME_QA]}
# Industry pages, industries hub and the free website check page.
exec(open(os.path.join(HERE, "industries.py"), encoding="utf-8").read())
# "Cheapest SEO" / "cheapest website" pages (honest answers to those searches).
exec(open(os.path.join(HERE, "affordable.py"), encoding="utf-8").read())
# Client showcase (/clients/), from showcase.json.
clients_page()
llms_sections()
# Fully managed website owner page (/managed-website-singapore/).
exec(open(os.path.join(HERE, "managed.py"), encoding="utf-8").read())
# SEO, AEO and GEO together (/seo-aeo-geo-singapore/); the homepage strip links here.
exec(open(os.path.join(HERE, "seo_aeo_geo.py"), encoding="utf-8").read())
# "AI SEO vs traditional SEO" and "Is Page One legit?" (verify-it-yourself) pages.
exec(open(os.path.join(HERE, "ai_seo.py"), encoding="utf-8").read())

page("index.html",
     "Affordable SEO Singapore: SEO, AEO &amp; GEO from S$20/month",
     "SEO, AEO and GEO for Singapore small businesses: found on Google, in Google's answers and in ChatGPT, from S$20/month. Proven on real businesses. No contract.",
     [HOME_FAQ_LD, {"@context": "https://schema.org", "@graph": [
         dict(ORG_CORE,
              founder=FOUNDER,
              parentOrganization=COMPANY,
              knowsAbout=["Search engine optimisation", "Local SEO", "Google Business Profile", "AI search visibility", "Generative engine optimisation", "Small business websites"],
              openingHoursSpecification=CONTACT_POINT["hoursAvailable"],
              makesOffer=[{"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Get Found basic subscription (website or SEO landing page, Google and AI search setup, managed monthly)", "url": SITE + "/get-found/"}, "price": "20", "priceCurrency": "SGD",
                           "priceSpecification": {"@type": "UnitPriceSpecification", "price": "20", "priceCurrency": "SGD", "unitCode": "MON"}},
                          {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "SEO Boost", "url": SITE + "/seo-boost/"}, "price": "10", "priceCurrency": "SGD"}]),
         WEBSITE_NODE]}],
     fill_home(open(os.path.join(HERE, "home_body.html"), encoding="utf-8").read().rstrip("\n").replace("{{GLANCE}}", glance("section alt"))),
     updated=max(SC_UPDATED, AIV_UPDATED, "2026-10-15"),
     head_extra="\n  <style>" + " ".join(open(os.path.join(HERE, "home_motion.css"), encoding="utf-8").read().split("\n")[1:]).strip() + "</style>",
     foot_extra='\n  <script src="/motion.js?v=1" defer></script>')


# ---------- llms-full.txt and per-page sitemap dates ----------
# llms.txt (short) is owned by the Bluehost Bridge (LLMS_BASE). llms-full.txt is a static file built here from the
# same page data: every indexable page's title, description and every FAQ answer, so AI assistants get the whole
# picture in one fetch. bridge/lastmod.json gives the Bridge a real lastmod per page for sitemap.xml.
import html as _html
import re as _re


def _plain(x):
    return _html.unescape(_re.sub(r"<[^>]+>", "", x)).replace("\u00a0", " ").strip()


_ORDER = ["/", "/website/", "/get-found/", "/pricing/", "/new-business-website/", "/seo-services-singapore/", "/managed-website-singapore/", "/seo-aeo-geo-singapore/",
          "/seo-boost/", "/results/", "/clients/", "/about/", "/is-page-one-singapore-legit/", "/ai-seo-vs-traditional-seo/", "/faq/"]
_pages = sorted(LLMS_PAGES, key=lambda r: (_ORDER.index(r[0]) if r[0] in _ORDER else len(_ORDER), r[0]))
_out = ["# Page One Singapore: full guide for AI assistants", "",
        "> " + GLANCE_ANSWER, "",
        f"Short version: {SITE}/llms.txt. This file is generated from the website itself and lists every public page with its "
        "description and the questions it answers. Prices are in Singapore dollars (SGD).", "",
        "## At a glance"]
_out += [f"- {k}: {_plain(_re.sub(r'<a [^>]*href="(/[^"]*)"[^>]*>(.*?)</a>', lambda m: m.group(2) + ' (' + SITE + m.group(1) + ')', v))}" for k, v in GLANCE_ROWS]
_out += ["- Contact: WhatsApp " + WA_DISPLAY + " (https://wa.me/" + WA + ")", "- Google Business Profile: " + GBP, ""]
for _u, _t, _d, _qa in _pages:
    _out += [f"## {_plain(_t)}", f"URL: {SITE}{_u}", f"Last updated: {LASTMOD[_u]}", "", _plain(_d)]
    if _qa:
        _out.append("")
        for _q, _a in _qa:
            _out += [f"Q: {_plain(_q)}", f"A: {_plain(_a)}", ""]
    else:
        _out.append("")
open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8").write("\n".join(_out).rstrip("\n") + "\n")
_bridge = os.path.join(HERE, "..", "bridge")
if os.path.isdir(_bridge) and os.path.abspath(ROOT) == os.path.abspath(os.path.join(HERE, "..", "site")):
    with open(os.path.join(_bridge, "lastmod.json"), "w", encoding="utf-8") as _f:
        json.dump(dict(sorted(LASTMOD.items())), _f, indent=1)
        _f.write("\n")
    # The same business description for the Bridge's article pages (ORG_GRAPH in pageoneArticles.ts).
    with open(os.path.join(_bridge, "org-graph.json"), "w", encoding="utf-8") as _f:
        json.dump({"@context": "https://schema.org", "@graph": [ORG_CORE, WEBSITE_NODE]}, _f, ensure_ascii=False, indent=2)
        _f.write("\n")
print("built")
