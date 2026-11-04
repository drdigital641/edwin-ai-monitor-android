import json, html, urllib.parse, os
D = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(D, 'sg_css.txt')).read()
WAP = open(os.path.join(D, 'wa_path.txt')).read().strip()
SLUG = 'why-edwin-built-sg-car-workshop-directory'
URL = 'https://www.sggarage.com/articles/%s.html' % SLUG
TITLE = 'Why We Built a Car Workshop Directory | Edwin Garage'
H1 = 'Why a Workshop Owner Built SG Car Workshop, a Directory That Listens to Drivers'
DESC = 'Edwin of Edwin Garage on why he started SG Car Workshop: listings built from Google profiles, what customers say and workshops’ own posts.'
IMG = 'https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@ebdf067f/site-assets/sggarage/edwin-garage-shopfront-01-295.webp'
DATE = '2026-11-05T07:30:00+08:00'
WA = 'https://wa.me/6597856612?text=' + urllib.parse.quote('Hi Edwin, I read your article about SG Car Workshop and would like to enquire.')
FAQ = [
 ('Who runs SG Car Workshop?', 'SG Car Workshop is run by Page One Singapore. Edwin, who runs Edwin Garage, founded both. Edwin Garage and SG Garage carry an "Owned by the site’s founder" label in the directory, are never in the paid Featured block and get no boost in ordering.'),
 ('Where does the information on a free listing come from?', 'Basic listings are built from the workshop’s public Google Business Profile and, where available, what its customers mention in Google reviews, summarised in the directory’s own words. Job stories are added only from the workshop’s own public posts.'),
 ('Does SG Car Workshop rank workshops?', 'Only where an estate has at least 8 workshops with 20 or more Google ratings. Those are ranked by a formula that weighs the rating against the number of ratings. Everywhere else workshops are listed A to Z, and paid Featured workshops are never ranked.'),
 ('Can a workshop remove its listing?', 'Yes. Basic listings are free and are not arranged with the business, so any owner can ask for theirs to be removed through the Remove my listing page on the directory.'),
]
def esc(s): return html.escape(s, quote=True)
faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
graph = {"@context":"https://schema.org","@graph":[
 {"@type":["AutoRepair","LocalBusiness"],"@id":"https://www.sggarage.com/#business","name":"Edwin Garage Aircon & Car Repair","url":"https://www.sggarage.com",
  "address":{"@type":"PostalAddress","streetAddress":"Blk 5032 Ang Mo Kio Industrial Park 2 #01-295","addressLocality":"Ang Mo Kio","addressRegion":"Singapore","postalCode":"569535","addressCountry":"SG"},
  "geo":{"@type":"GeoCoordinates","latitude":1.3721,"longitude":103.8458},
  "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"10:00","closes":"20:00"}],
  "sameAs":["https://share.google/hYkZhnKyoAEeERhWM"],"hasMap":"https://share.google/hYkZhnKyoAEeERhWM"},
 {"@type":"Article","@id":URL+"#article","headline":H1,"description":DESC,"image":{"@type":"ImageObject","url":IMG,"width":1400,"height":1050},
  "datePublished":DATE,"dateModified":DATE,"author":{"@type":"Person","name":"Edwin","jobTitle":"Master Automotive Technician","worksFor":{"@id":"https://www.sggarage.com/#business"}},
  "publisher":{"@id":"https://www.sggarage.com/#business"},"mainEntityOfPage":{"@type":"WebPage","@id":URL},"articleSection":"Our Workshop","inLanguage":"en-SG",
  "about":{"@type":"WebSite","name":"SG Car Workshop","url":"https://sgcarworkshop.sg/"}},
 {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":"https://www.sggarage.com"},{"@type":"ListItem","position":2,"name":"Car Guides","item":"https://www.sggarage.com/articles/"},{"@type":"ListItem","position":3,"name":H1,"item":URL}]}]}
svg = lambda n: '<svg width="%d" height="%d" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="%s"/></svg>' % (n, n, WAP)
BODY = '''
<p><strong>Short answer: SG Car Workshop is a Singapore car workshop directory I started so drivers can judge a workshop by what is real: the name and mobile number on its Google Business Profile, what its own customers mention, and jobs the workshop has posted itself. It does not sell rankings, it never invents a story, and an AI reads what you type into the search box the way a person would.</strong></p>

<h2>Why a workshop owner started a directory</h2>
<p>I have run Edwin Garage in Ang Mo Kio since 2010. Over those years I have seen how drivers choose a workshop. Most ask a friend, look at Google Maps, or search for a symptom and hope the first result is honest. Many directories did not help much. Some list businesses under names that do not match the signboard, show phone numbers that ring nowhere, or rank whoever pays.</p>
<p>A driver with a warning light on the dashboard needs three things fast: a workshop near them that does that kind of work, a number that actually reaches the shop, and a fair idea of what other drivers experienced there. So I built a directory around those three things and nothing else.</p>

<h2>How does SG Car Workshop listen to drivers?</h2>
<p>The idea is simple: the people best placed to describe a workshop are the drivers who used it and the workshop itself. Each free (Basic) listing is built from those voices, in this order.</p>
<ol>
<li><strong>The workshop’s own Google Business Profile.</strong> The listing uses the exact business name on that profile, not a name copied from another directory, and the mobile number the workshop put there. Only workshops with a Singapore mobile number on their profile are listed, so the WhatsApp button reaches the shop.</li>
<li><strong>What customers mention in Google reviews.</strong> Where reviews clearly mention a service, a car make or a speciality, the listing says so in its own words, for example “customers mention aircon repairs on Japanese cars”. Review text is never copied and nothing is guessed.</li>
<li><strong>The workshop’s own public posts.</strong> A job story, such as a gearbox fault found and fixed, appears only when the workshop itself posted it in public, with the source kept on file. If there is no real story, the page shows none. Nothing is invented to fill space.</li>
</ol>
<div class="case-box"><p>Plain rule: if a detail cannot be traced to the workshop or to what its customers wrote, it stays off the page.</p></div>

<h2>An AI that reads your search like a person</h2>
<p>Drivers do not search like a database. They type things like “aircon blowing warm air Honda Vezel near Ang Mo Kio open Sunday”. The search box on SG Car Workshop sends each typed search to an AI that picks out the service, the car make, the area and whether you need Sunday or late hours, then shows matching workshops. If the AI is ever unavailable, a simpler built-in reader takes over, so the search still works.</p>
<p>What drivers type also tells the directory which problems people are trying to solve. That is the other half of listening: the guides and service categories follow what drivers actually ask, not what we guess they want.</p>

<h2>What it does not do</h2>
<ul>
<li><strong>No paid rankings.</strong> Workshops are ranked only where an estate has at least 8 workshops with 20 or more Google ratings, using a published formula that weighs the rating against how many ratings there are. Everywhere else the list is A to Z.</li>
<li><strong>Paid listings are labelled.</strong> Workshops that pay appear in a separate Featured block, marked as such, and are never part of a ranking.</li>
<li><strong>No dealers or insurers.</strong> Only car workshops and car services: servicing and repair, gearbox, ABS and ECU, spray painting, batteries, aircon, detailing, wraps and parts.</li>
<li><strong>Free listings can be removed.</strong> Basic listings are not arranged with the business, so any owner can ask for theirs to be taken down.</li>
</ul>

<h2>Where Edwin Garage stands in it</h2>
<p>In the interest of transparency: Edwin Garage (unit #01-295) and SG Garage, our aircon unit (#01-309), are both mine. In the directory they carry an “Owned by the site’s founder” label, sit in the normal A to Z lists, are never in the paid Featured block and get no boost in ordering. The directory is run by Page One Singapore, which I also founded.</p>
<p>The aim is for <a href="https://sgcarworkshop.sg/">SG Car Workshop</a> to become the most useful place in Singapore to find a car workshop, by staying close to what drivers and workshops actually say. Whether it gets there is for drivers to judge.</p>

<h2>What this means for you as a driver</h2>
<p>Use any directory, including this one, the same way you would use a friend’s tip: as a starting point. Check that the name and number match the shop’s Google profile, read what customers mention, and look for jobs the workshop has posted itself. Then message the workshop with your car model and the symptom. Our own guide on <a href="https://www.sggarage.com/articles/how-to-choose-an-honest-car-workshop-in-singapore.html">how to choose an honest car workshop in Singapore</a> covers the questions worth asking.</p>
<p>And if your car is near Ang Mo Kio, you are welcome to ask us directly. We work by appointment and explain what we find before any work starts.</p>

<h2>Questions about SG Car Workshop</h2>
''' + ''.join('<h3>%s</h3>\n<p>%s</p>\n' % (esc(q), esc(a)) for q, a in FAQ) + '''
    <div class="takeaways-box">
      <h3>Key Takeaways</h3>
      <ul>
        <li>SG Car Workshop is a Singapore car workshop directory founded by Edwin of Edwin Garage and run by Page One Singapore.</li>
        <li>Free listings use the workshop’s Google Business Profile name and mobile number, what customers mention in reviews, and only real job posts by the workshop.</li>
        <li>An AI reads each typed search for service, car make, area and opening days.</li>
        <li>No paid rankings; Edwin Garage and SG Garage are labelled as the founder’s and get no boost.</li>
      </ul>
    </div>
'''
page = '''<!DOCTYPE html>
<html lang="en-SG">
<head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{T}</title>
<meta name="description" content="{D}">
<meta property="og:title" content="{T}">
<meta property="og:description" content="{D}">
<meta property="og:image" content="{IMG}"><meta property="og:image:width" content="1400"><meta property="og:image:height" content="1050"><meta property="og:image:alt" content="Edwin Garage shopfront at Ang Mo Kio Industrial Park 2"><meta property="og:type" content="article">
<meta property="og:url" content="{U}">
<meta property="og:locale" content="en_SG"><meta property="og:site_name" content="Edwin Garage Singapore">
<meta property="article:published_time" content="{DT}"><meta property="article:modified_time" content="{DT}">
<meta property="article:section" content="Our Workshop">
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
{CSS}</style>
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
      <span>Why We Built a Car Workshop Directory</span>
    </nav>
    <div class="art-category">Our Workshop</div>
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
  <img src="{IMG}" width="1400" height="1050" alt="Edwin Garage shopfront at Blk 5032 Ang Mo Kio Industrial Park 2, unit #01-295" class="hero-img" loading="eager">
  <figcaption class="hero-caption">Our shopfront at #01-295, Ang Mo Kio Industrial Park 2. Real photo, number plates blurred.</figcaption>
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
  <h3>📚 More About Edwin Garage</h3>
  <ul class="cluster-list">
<li><a href="https://www.sggarage.com/articles/how-edwin-garage-got-found-on-google.html">How Edwin Garage Got Found on Google</a></li>
<li><a href="https://www.sggarage.com/articles/edwin-garage-promise-honest-car-workshop-singapore.html">The Edwin Garage Promise</a></li>
<li><a href="https://www.sggarage.com/articles/first-visit-edwin-garage-what-to-expect.html">Your First Visit to Edwin Garage: What to Expect</a></li>
<li><a href="https://www.sggarage.com/articles/why-edwin-garage-is-appointment-only-singapore.html">Why Edwin Garage Is Appointment Only</a></li>
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
    <p>© 2025 Edwin Garage Singapore · Blk 5032 Ang Mo Kio Industrial Park 2 #01-295 · S569535 · <a href="https://sggarageedwin.as.me/">Book online</a></p>
  </div>
</footer>

<a class="wa-float" href="{WA}" target="_blank" rel="noopener" aria-label="WhatsApp Edwin with an enquiry">{SVG18}WhatsApp enquiry · 97856612</a>
</body>
</html>
'''
rep = dict(T=esc(TITLE), D=esc(DESC), IMG=IMG, U=URL, DT=DATE, H1=esc(H1), WA=esc(WA), CSS=CSS, BODY=BODY,
           FAQLD=json.dumps(faq_ld, ensure_ascii=False), GRAPH=json.dumps(graph, ensure_ascii=False), SVG16=svg(16), SVG18=svg(18))
for k, v in rep.items(): page = page.replace('{%s}' % k, v)
os.makedirs(os.path.join(D, 'sggarage/articles'), exist_ok=True)
open(os.path.join(D, 'sggarage/articles/%s.html' % SLUG), 'w').write(page)
print(len(TITLE), len(DESC), len(page))
