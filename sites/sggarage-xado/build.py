import json, html, urllib.parse, os
D = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(D, 'sg_css.txt')).read()
WAP = open(os.path.join(D, 'wa_path.txt')).read().strip()
SLUG = 'xado-engine-oil-treatment-ang-mo-kio'
URL = 'https://www.sggarage.com/articles/%s.html' % SLUG
TITLE = 'XADO Engine Oil & Treatment in Ang Mo Kio | Edwin Garage'
H1 = 'XADO Engine Oil and Revitalizant Treatment at Edwin Garage, Ang Mo Kio'
DESC = 'Edwin Garage is an authorised XADO workshop in Ang Mo Kio. What XADO says its 1 Stage oil and treatments do, who they suit, and how we add them.'
IMG = 'https://www.sggarage.com/uploads/xado/xado-1-stage-motor-oil-over-engine-bay.jpg'
UP = '/uploads/xado/'
DATE = '2026-11-05T11:30:00+08:00'
WA = 'https://wa.me/6597856612?text=' + urllib.parse.quote('Hi Edwin, I read your XADO article and would like to ask about XADO for my car.')
FAQ = [
 ('Is Edwin Garage an authorised XADO workshop?', 'Yes. Edwin Garage in Ang Mo Kio is one of the 11 authorised XADO workshops listed by Rev Solutions, the XADO distributor in Singapore. You can ask for XADO oil or a XADO treatment at your next service with us.'),
 ('Does XADO change my engine oil?', 'According to XADO, the oil only carries the revitalizant to the friction surfaces and its viscosity does not change. Your car still gets the oil grade its maker specifies.'),
 ('Can XADO fix a broken engine?', 'No. XADO describes its products as protection and wear restoration for worn surfaces, not a repair for broken or badly damaged parts. Oil leaks, a failed gasket or a damaged turbo still need a proper repair first.'),
 ('How long does a XADO treatment take?', 'Adding the treatment takes a few minutes during an oil service. XADO says the revitalization then happens over the next 1,000 to 1,200 km of normal driving, and the oil should not be changed during that time.'),
]
def esc(s): return html.escape(s, quote=True)
faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
graph = {"@context":"https://schema.org","@graph":[
 {"@type":["AutoRepair","LocalBusiness"],"@id":"https://www.sggarage.com/#business","name":"Edwin Garage Aircon & Car Repair","url":"https://www.sggarage.com",
  "address":{"@type":"PostalAddress","streetAddress":"Blk 5032 Ang Mo Kio Industrial Park 2 #01-295","addressLocality":"Ang Mo Kio","addressRegion":"Singapore","postalCode":"569535","addressCountry":"SG"},
  "geo":{"@type":"GeoCoordinates","latitude":1.3721,"longitude":103.8458},
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"10:00","closes":"20:00"}],
  "sameAs":["https://share.google/hYkZhnKyoAEeERhWM"],"hasMap":"https://share.google/hYkZhnKyoAEeERhWM"},
 {"@type":"Article","@id":URL+"#article","headline":H1,"description":DESC,"image":{"@type":"ImageObject","url":IMG,"width":900,"height":1200},
  "datePublished":DATE,"dateModified":DATE,"author":{"@type":"Person","name":"Edwin","jobTitle":"Master Automotive Technician","worksFor":{"@id":"https://www.sggarage.com/#business"}},
  "publisher":{"@id":"https://www.sggarage.com/#business"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"articleSection":"Car Servicing","inLanguage":"en-SG",
  "about":[{"@type":"Brand","name":"XADO","url":"https://xado-shop.sg/"},{"@type":"Thing","name":"Engine oil servicing"}],"mentions":{"@type":"Organization","name":"XADO Singapore","url":"https://xado-shop.sg/"}},
 {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.sggarage.com"},{"@type":"ListItem","position":2,"name":"Car Guides","item":"https://www.sggarage.com/articles/"},{"@type":"ListItem","position":3,"name":H1,"item":URL}]}]}
svg = lambda n: '<svg width="%d" height="%d" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="%s"/></svg>' % (n, n, WAP)
BODY = '''
<p><strong>Short answer: yes, you can ask for XADO at Edwin Garage. We are one of the 11 authorised XADO workshops in Singapore. XADO makes full synthetic motor oils and engine treatments with its 1 Stage Revitalizant&reg; technology, which XADO says forms a protective ceramic-metal layer on worn engine surfaces. We check your engine first, then tell you honestly whether XADO makes sense for your car.</strong></p>

<h2>What is XADO 1 Stage motor oil?</h2>
<p>XADO is a European car-care brand founded in 1991, with production under XADO Germany and XADO Lube B.V. (Netherlands) licences. In Singapore it is distributed by Rev Solutions Pte Ltd. The can in our photos is XADO 1 Stage full synthetic motor oil, labelled "Smart Technology for Your Car".</p>
<p>What makes it different from a normal oil is the revitalizant blended into it. According to XADO, the oil simply carries the revitalizant to the parts that rub together. Where heat and friction are highest, it builds a ceramic-metal (cermet) layer from carbides and the worn-off metal particles already in the oil. The back of the can shows XADO's own before-and-after pictures of a cylinder surface, magnified 100 times.</p>

<div class="xado-grid">
<figure><picture><source type="image/webp" srcset="{UP}xado-1-stage-motor-oil-label-workshop.webp"><img src="{UP}xado-1-stage-motor-oil-label-workshop.jpg" alt="Edwin Garage mechanic holding a can of XADO 1 Stage Technology full synthetic motor oil in the Ang Mo Kio workshop" width="900" height="1200" loading="lazy" decoding="async"></picture><figcaption>The 1 Stage label, in our workshop</figcaption></figure>
<figure><picture><source type="image/webp" srcset="{UP}xado-1-stage-motor-oil-revitalizant-before-after-label.webp"><img src="{UP}xado-1-stage-motor-oil-revitalizant-before-after-label.jpg" alt="Back label of XADO 1 Stage motor oil with XADO's before and after cylinder surface pictures magnified 100 times" width="900" height="1200" loading="lazy" decoding="async"></picture><figcaption>XADO's before/after panel on the can</figcaption></figure>
</div>

<h2>Who is XADO for?</h2>
<p>Singapore is hard on engines: stop-go traffic on the CTE and PIE, short trips that never let the engine fully warm up, and 30&deg;C days all year. With COE above $130,000, most owners also want the engine to last the full 10 years or longer. XADO Singapore suggests these options, depending on the car:</p>
<ul>
<li><strong>New cars under 20,000 km:</strong> XADO's AMC 1 Stage "New Car" formula, which XADO says protects the engine during break-in.</li>
<li><strong>Turbo cars 3 to 7 years old:</strong> AMC Maximum "Twin Turbo", aimed at heat, carbon and power loss.</li>
<li><strong>Cars over 7 years old, or before a COE renewal:</strong> an Atomex Total Flush first, then AMC Maximum, for engines showing oil burning, more noise or lower compression.</li>
<li><strong>At every oil change:</strong> a XADO oil with revitalizant built in, such as the 1 Stage oil in our photos or the LX AMC Black Edition.</li>
</ul>
<p>The <a href="https://xado-shop.sg/xado-products-guide.html">XADO product guide</a> compares the full range.</p>

<h2>When XADO is not the answer</h2>
<p>XADO describes its products as protection and wear restoration, not a fix for broken parts. If your car is leaking oil, has a failed gasket, a damaged turbo or a serious mechanical fault, that needs a proper repair first. A treatment poured into a damaged engine only wastes your money. That is why we inspect before we recommend anything. If a standard oil change is all your car needs, we will tell you.</p>

<h2>How we add XADO at Edwin Garage</h2>
<figure class="xado-wide"><picture><source type="image/webp" srcset="{UP}xado-1-stage-motor-oil-at-oil-filler.webp"><img src="{UP}xado-1-stage-motor-oil-at-oil-filler.jpg" alt="XADO full synthetic motor oil next to the engine oil filler during a service at Edwin Garage, Ang Mo Kio" width="900" height="1200" loading="lazy" decoding="async"></picture><figcaption>Ready at the oil filler, Edwin Garage, Ang Mo Kio</figcaption></figure>
<ol>
<li><strong>Check first.</strong> We look at your car's mileage, oil condition, leaks and any warning signs, and ask how you drive.</li>
<li><strong>Agree the plan and price.</strong> We tell you which XADO product suits the car, or whether you need it at all, and confirm the price before any work starts.</li>
<li><strong>Add it at the oil service.</strong> For an engine treatment, XADO's steps are to warm the engine up, switch it off, pour the treatment into the oil filler without going above the dipstick maximum, then run the engine for 3 to 5 minutes.</li>
<li><strong>Drive normally.</strong> XADO says the revitalization happens over the next 1,000 to 1,200 km, and you should not change the oil during that time.</li>
</ol>
<div class="case-box"><p>These are XADO's descriptions and claims, not a guarantee from us. Results depend on your engine's condition, the oil used and its maintenance history.</p></div>

<h2>Learn more about XADO</h2>
<p>For the science, the lab tests and the full product range, see <a href="https://xado-shop.sg/how-xado-works.html">how XADO Revitalizant works</a> on the XADO Singapore website. For our regular oil service, read our guide to <a href="https://www.sggarage.com/articles/engine-oil-servicing-packages-ang-mo-kio.html">engine oil servicing packages in Ang Mo Kio</a>, and if you plan to keep your car past 10 years, our <a href="https://www.sggarage.com/articles/coe-car-maintenance-singapore-10-year-guide.html">COE car maintenance guide</a>.</p>

<h2>Questions about XADO at Edwin Garage</h2>
''' + ''.join('<h3>%s</h3>\n<p>%s</p>\n' % (esc(q), esc(a)) for q, a in FAQ) + '''
    <div class="takeaways-box">
      <h3>Key Takeaways</h3>
      <ul>
        <li>Edwin Garage in Ang Mo Kio is one of the 11 authorised XADO workshops in Singapore.</li>
        <li>XADO says its 1 Stage Revitalizant forms a protective ceramic-metal layer on worn engine surfaces; the oil only carries it.</li>
        <li>XADO is protection and wear restoration, not a repair for broken parts, so we inspect the engine first.</li>
        <li>We confirm the product and price before any work starts.</li>
      </ul>
    </div>
'''.replace('{UP}', UP)
page = '''<!DOCTYPE html>
<html lang="en-SG">
<head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{T}</title>
<meta name="description" content="{D}">
<meta property="og:title" content="{T}">
<meta property="og:description" content="{D}">
<meta property="og:image" content="{IMG}"><meta property="og:image:width" content="900"><meta property="og:image:height" content="1200"><meta property="og:image:alt" content="XADO 1 Stage full synthetic motor oil at Edwin Garage, Ang Mo Kio"><meta property="og:type" content="article">
<meta property="og:url" content="{U}">
<meta property="og:locale" content="en_SG"><meta property="og:site_name" content="Edwin Garage Singapore">
<meta property="article:published_time" content="{DT}"><meta property="article:modified_time" content="{DT}">
<meta property="article:section" content="Car Servicing">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{T}">
<meta name="twitter:description" content="{D}"><meta name="twitter:image" content="{IMG}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{U}">
<script type="application/ld+json">{FAQLD}</script>
<script type="application/ld+json">{GRAPH}</script>
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet">
<style>
{CSS}
.xado-hero{max-width:560px;margin:0 auto}.xado-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:24px 0}.xado-grid figure,.xado-wide{margin:0}.xado-grid img,.xado-wide img{display:block;width:100%;height:auto;border-radius:10px}.xado-wide{max-width:420px;margin:20px auto}.xado-grid figcaption,.xado-wide figcaption{font-size:13px;color:#6B7280;margin-top:6px}</style>
</head>
<body>

<header class="site-header">
  <a class="logo" href="/"><span>Edwin</span> Garage</a>
  <button class="hamburger" id="hbg" aria-label="Menu" onclick="this.classList.toggle('open');document.getElementById('hnav').classList.toggle('open')">
    <span></span><span></span><span></span>
  </button>
  <nav class="hnav" id="hnav">
    <a class="nl" href="/">Home</a>
    <a class="nl" href="/car-servicing-repair/">Servicing</a>
    <a class="nl" href="/car-aircon-repair/">Aircon</a>
    <a class="nl" href="/accident-claim-repair/">Accident</a>
    <a class="nl active" href="/articles/">Articles</a>
    <a class="btn-wa-sm" href="{WA}" target="_blank" rel="noopener">{SVG16} WhatsApp</a>
    <a class="btn-book-sm" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Now</a>
  </nav>
</header>

<div class="art-header">
  <div class="art-header-inner">
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <a href="/">Home</a>
      <span class="sep">›</span>
      <a href="/articles/">Articles</a>
      <span class="sep">›</span>
      <span>XADO Engine Oil &amp; Treatment</span>
    </nav>
    <div class="art-category">Car Servicing</div>
    <h1>{H1}</h1>
    <div class="art-byline">
      <strong>Edwin</strong>
      <span class="sep">·</span>
      <span>Master Automotive Technician</span>
      <span class="sep">·</span>
      <span>November 5, 2026</span>
      <span class="sep">·</span>
      <span>Edwin Garage, Ang Mo Kio</span>
    </div>
  </div>
</div>

<div class="hero-img-wrap">
  <figure>
  <picture><source type="image/webp" srcset="/uploads/xado/xado-1-stage-motor-oil-over-engine-bay.webp"><img src="/uploads/xado/xado-1-stage-motor-oil-over-engine-bay.jpg" width="900" height="1200" alt="Can of XADO 1 Stage full synthetic motor oil held over an open engine bay at Edwin Garage, Ang Mo Kio" class="hero-img xado-hero" loading="eager" fetchpriority="high"></picture>
  <figcaption class="hero-caption">XADO 1 Stage full synthetic motor oil in our Ang Mo Kio workshop. Real photo.</figcaption>
</figure>
</div>

<div class="article-wrap">
  <article class="article">
{BODY}
    <div class="cta-block">
      <h3>Got a Question? Ask Edwin</h3>
      <p>Edwin Garage is located in Ang Mo Kio. Serving Hougang, Yio Chu Kang, Serangoon &amp; surrounding areas.</p>
      <a class="btn-wa" href="{WA}" target="_blank" rel="noopener">{SVG18} WhatsApp Edwin</a>
      <a class="btn-book" href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a>
    </div>

<div class="cluster-box">
  <h3>📚 More on Engine Oil &amp; Servicing</h3>
  <ul class="cluster-list">
<li><a href="https://www.sggarage.com/articles/engine-oil-servicing-packages-ang-mo-kio.html">Engine Oil Servicing in Singapore: Packages, Prices &amp; What You Need to Know</a></li>
<li><a href="https://www.sggarage.com/articles/what-happens-skip-engine-oil-change-singapore.html">What Happens If You Skip an Engine Oil Change</a></li>
<li><a href="https://www.sggarage.com/articles/hyundai-tucson-engine-oil-consumption-singapore.html">Hyundai Tucson Engine Oil Consumption</a></li>
<li><a href="https://www.sggarage.com/articles/coe-car-maintenance-singapore-10-year-guide.html">COE Car Maintenance: The 10-Year Guide</a></li>
</ul>
  <a href="https://www.sggarage.com/car-servicing-repair/" class="cluster-service-btn">→ View Car Servicing &amp; Repair at Edwin Garage</a>
</div>

  </article>
</div>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <a class="logo" href="/"><span>Edwin</span> Garage</a>
      <p>Japanese &amp; Korean car specialist in Ang Mo Kio since 2010. Aircon, servicing, accident repair.</p>
    </div>
    <div class="footer-links">
      <h4>Services</h4>
      <ul>
        <li><a href="/car-servicing-repair/">Car Servicing &amp; Repair</a></li>
        <li><a href="/car-aircon-repair/">Car Aircon Repair</a></li>
        <li><a href="/accident-claim-repair/">Accident &amp; Dent Repair</a></li>
      </ul>
    </div>
    <div class="footer-links">
      <h4>Visit Us</h4>
      <ul>
        <li><a href="https://maps.google.com/?q=Edwin+Garage+Singapore" target="_blank" rel="noopener">Blk 5032 AMK Industrial Park 2 #01-295</a></li>
        <li>Mon–Sat: 10am – 8pm</li>
        <li>Closed Sundays</li>
        <li><a href="https://wa.me/6597856612" target="_blank" rel="noopener">WhatsApp: 97856612</a></li>
      </ul>
    </div>
    <div class="footer-links">
      <h4>Quick Links</h4>
      <ul>
        <li><a href="/articles/">Car Guides &amp; Articles</a></li>
        <li><a href="https://sggarageedwin.as.me/" target="_blank" rel="noopener">Book Appointment</a></li>
        <li><a href="https://share.google/hYkZhnKyoAEeERhWM" target="_blank" rel="noopener">Google Reviews</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <p>© 2026 Edwin Garage Singapore · Blk 5032 Ang Mo Kio Industrial Park 2 #01-295 · S569535 · <a href="https://sggarageedwin.as.me/">Book online</a></p>
  </div>
</footer>

<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp Edwin with an enquiry">{SVG18}WhatsApp enquiry · 97856612</a>
</body>
</html>
'''
rep = dict(T=esc(TITLE), D=esc(DESC), IMG=IMG, U=URL, DT=DATE, H1=esc(H1), WA=esc(WA), CSS=CSS, BODY=BODY,
           FAQLD=json.dumps(faq_ld, ensure_ascii=False), GRAPH=json.dumps(graph, ensure_ascii=False), SVG16=svg(16), SVG18=svg(18), UP=UP)
for k, v in rep.items(): page = page.replace('{%s}' % k, v)
os.makedirs(os.path.join(D, 'site/articles'), exist_ok=True)
open(os.path.join(D, 'site/articles/%s.html' % SLUG), 'w').write(page)
print(len(TITLE), len(DESC), len(page))
