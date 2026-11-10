"""Build /coe-renewal-loan/ for www.sggarage.com (10 Nov 2026, Edwin's brief 12:35pm + confirmed facts 12:38pm).

Facts used (Edwin, 10 Nov 2026): customers choose bank or in-house financing; FREE pre-renewal check worth $80, only
with a COE renewal loan taken with Edwin Garage; main CTA "WhatsApp us for a quote" on 9785 6612.
NOT used, by rule: no rates, tenure, instalments, amounts, approval times, lender or bank names, no approval promises.
Template = live /car-servicing-repair/ (same CSS, header and footer). Run: python3 build.py ; python3 check.py
"""
import html, json, os, re
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "site", "coe-renewal-loan", "index.html")
TODAY = "2026-11-10"
BASE = "https://www.sggarage.com"
URL = BASE + "/coe-renewal-loan/"
OG = "https://i.ibb.co/qM3ZKCDy/edwin-garage-og-image.jpg"
PREFILL = ("Hi Edwin Garage, I want to ask about a COE renewal loan for my car (plate/model: ...) "
           "and the free pre-renewal check.")
WA = "https://wa.me/6597856612?text=" + quote(PREFILL, safe="")
TITLE = "COE Renewal Loan Singapore: Renew or Scrap? | Edwin Garage"
DESC = ("COE renewal loan in Singapore from Edwin Garage, Ang Mo Kio. Choose from bank or in-house financing, plus a "
        "free pre-renewal check with your loan.")
H1 = "COE Renewal Loan in Singapore: Renew Your COE with Edwin Garage"
NOTE = "Financing is subject to the lender's assessment and terms."

CSS = """*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:Inter,"Segoe UI","Helvetica Neue",Arial,sans-serif;color:#374151;line-height:1.65;background:#fff}h1,h2,h3{color:#111827;line-height:1.2;margin-top:0}h1{font-size:clamp(2.15rem,5vw,3.6rem);letter-spacing:-.045em;margin-bottom:20px}h2{font-size:clamp(1.65rem,3vw,2.35rem);letter-spacing:-.025em;margin-bottom:16px}h3{font-size:1.15rem;margin-bottom:8px}a{color:#2563EB}.site-header{position:sticky;top:0;z-index:100;background:#fff;border-bottom:1px solid #e5e7eb;box-shadow:0 1px 3px rgba(0,0,0,.08)}.nav-inner{max-width:1200px;margin:0 auto;padding:0 24px;display:flex;align-items:center;height:64px;gap:32px}.nav-logo{font-weight:700;font-size:1.1rem;color:#111827;text-decoration:none}.nav-links{display:flex;list-style:none;gap:24px;margin:0;padding:0;flex:1}.nav-links a{color:#374151;text-decoration:none;font-size:.95rem;font-weight:500}.nav-links a:hover{color:#2563EB}.nav-cta{background:#2563EB;color:#fff;padding:10px 20px;border-radius:8px;text-decoration:none;font-weight:600;font-size:.9rem;white-space:nowrap}.nav-cta:hover,.btn:hover{background:#1d4ed8}.wrap{max-width:1200px;margin:auto;padding:0 24px}.hero{background:linear-gradient(135deg,#eff6ff,#fff 62%);padding:92px 0 78px}.eyebrow{font-weight:700;color:#2563EB;font-size:.9rem;text-transform:uppercase;letter-spacing:.08em}.lead{font-size:1.18rem;max-width:720px;margin:0 0 28px}.actions{display:flex;gap:12px;flex-wrap:wrap}.btn{display:inline-block;background:#2563EB;color:#fff;border-radius:8px;padding:13px 22px;text-decoration:none;font-weight:700}.btn.alt{background:#fff;color:#1d4ed8;border:1px solid #2563EB}.btn.alt:hover{background:#eff6ff}.section{padding:72px 0}.alt{background:#f8fafc}.intro{max-width:750px;margin-bottom:32px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:24px;box-shadow:0 2px 5px rgba(0,0,0,.035)}.card p{margin:0;font-size:.96rem}.steps{counter-reset:step;display:grid;grid-template-columns:repeat(3,1fr);gap:22px}.step{position:relative;padding:24px 20px 20px 72px;background:#fff;border-radius:12px;border:1px solid #e5e7eb}.step:before{counter-increment:step;content:counter(step);position:absolute;left:20px;top:20px;width:34px;height:34px;display:grid;place-items:center;border-radius:50%;background:#dbeafe;color:#1d4ed8;font-weight:800}.faq{max-width:860px}.faq details{background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:17px 20px;margin-bottom:12px}.faq summary{cursor:pointer;color:#111827;font-weight:700}.faq details p{margin:12px 0 0}.cta-band{background:#1d4ed8;color:#fff;padding:52px 0}.cta-band h2,.cta-band p{color:#fff}.cta-band .btn{background:#fff;color:#1d4ed8}.cta-band .btn.alt{border-color:#bfdbfe;background:transparent;color:#fff}.footer{background:#111827;color:#9ca3af;padding:48px 24px 24px}.footer-inner{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:32px;margin-bottom:32px}.footer-col strong{color:#fff;display:block;margin-bottom:12px;font-size:.95rem}.footer-col p,.footer-col li{font-size:.88rem;margin-bottom:8px}.footer-col ul{list-style:none;padding:0;margin:0}.footer-col a{color:#9ca3af;text-decoration:none}.footer-col a:hover{color:#fff}.footer-bottom{max-width:1200px;margin:0 auto;padding-top:24px;border-top:1px solid #374151;font-size:.82rem;text-align:center}
.btn-wa{background:#0E7A3F;color:#fff}.btn-wa:hover{background:#0B6634}.crumbs{font-size:.85rem;color:#64748b;margin-bottom:14px}.crumbs a{color:#64748b;text-decoration:none}.offer{background:#FFF7E6;border:2px solid #F5A524;border-radius:14px;padding:24px 26px;max-width:860px;margin:28px 0 0}.offer .tag{display:inline-block;background:#F5A524;color:#0B1B2E;font-weight:800;font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;border-radius:999px;padding:4px 12px;margin-bottom:10px}.offer h2,.offer h3{margin:0 0 8px;color:#0B1B2E}.offer p{margin:0 0 14px}.offer .cond{font-size:.88rem;color:#5B6676;margin:12px 0 0}.fin{font-size:.88rem;color:#64748b;margin:14px 0 0}.list{max-width:820px;padding-left:22px}.list li{margin-bottom:8px}.two{display:grid;grid-template-columns:1fr 1fr;gap:18px;max-width:980px}.src{font-size:.85rem;color:#64748b}
@media(max-width:768px){.nav-links{display:none}.nav-inner{justify-content:space-between}.hero{padding:68px 0 60px}.section{padding:54px 0}.grid,.steps,.two{grid-template-columns:1fr}.card{padding:21px}.wrap{padding:0 16px}.offer{padding:20px}.actions .btn{width:100%;text-align:center}}"""

NAV = """<header class="site-header"><nav class="nav-inner"><a href="/" class="nav-logo">Edwin Garage</a><ul class="nav-links"><li><a href="/">Home</a></li><li><a href="/car-servicing-repair/">Servicing &amp; Repair</a></li><li><a href="/car-aircon-repair/">Car Aircon</a></li><li><a href="/accident-claim-repair/">Accident Claim</a></li><li><a href="/articles/">Articles</a></li></ul><a href="https://sggarageedwin.as.me/" class="nav-cta" target="_blank" rel="noopener">Book Now</a></nav></header>"""

FOOTER = """<footer class="footer"><div class="footer-inner"><div class="footer-col"><strong>Edwin Garage</strong><p>Blk 5032 Ang Mo Kio Industrial Park 2 #01-295, Singapore 569535</p><p>Mon–Sat 10am–8pm | Closed Sundays</p></div><div class="footer-col"><strong>Services</strong><ul><li><a href="/car-servicing-repair/">Car Servicing &amp; Repair</a></li><li><a href="/car-aircon-repair/">Car Aircon Repair</a></li><li><a href="/accident-claim-repair/">Accident Claim &amp; Repair</a></li><li><a href="/coe-renewal-loan/">COE Renewal Loan</a></li><li><a href="/prices/">Starting prices</a></li><li><a href="/about/">About Edwin Garage</a></li></ul></div><div class="footer-col"><strong>Contact</strong><p>WhatsApp: <a href="https://wa.me/6597856612">97856612</a> (enquiries only)</p><p>Book: <a href="https://sggarageedwin.as.me/">sggarageedwin.as.me</a></p><p><em>Servicing and repairs: online booking. Battery replacement: walk-in.</em></p></div></div><div class="footer-bottom">© 2025 Edwin Garage Aircon &amp; Car Repair. All rights reserved. · <a href="/privacy-policy/">Privacy Policy</a></div></footer><script src="/p1-cta.js" defer></script>"""

def wa_btn(ref, cls="btn btn-wa"):
    return (f'<a class="{cls}" href="{html.escape(WA, quote=True)}" target="_blank" rel="noopener" '
            f'data-ref="{ref}">WhatsApp us for a quote</a>')

OFFER_TOP = f"""<div class="offer" id="free-check"><span class="tag">COE renewal offer</span><h2>FREE pre-renewal check (worth $80)</h2><p>Take your COE renewal loan with Edwin Garage and we'll check your car for free before you commit to keeping it, so you know what it may need for the years ahead.</p><div class="actions">{wa_btn("coe-offer-top")}</div><p class="cond">The free check (worth $80) applies only when you take your COE renewal loan with Edwin Garage. {NOTE}</p></div>"""

OFFER_FAQ = f"""<section class="section"><div class="wrap"><div class="offer" style="margin:0"><span class="tag">COE renewal offer</span><h3>Renewing your COE? Get a FREE pre-renewal check (worth $80)</h3><p>Choose from bank or in-house financing for your COE renewal. When you take your COE renewal loan with Edwin Garage, the pre-renewal check is free.</p><div class="actions">{wa_btn("coe-offer-faq")}</div><p class="cond">Free only with a COE renewal loan taken with Edwin Garage. {NOTE}</p></div></div></section>"""

FAQS = [
 ("Should I renew my COE or scrap my car?",
  "It depends on your car's condition, how much you use it and what a replacement would cost you. Renewing lets you keep a car you know; scrapping (deregistering) takes it off the road. A pre-renewal check shows what the car may need before you decide, and you can compare the official figures for your car on LTA's OneMotoring."),
 ("Should I renew for 5 years or 10 years?",
  "Under LTA's rules you can renew a car's COE for 5 or 10 years. A 5-year renewal cannot be renewed again, so the car must be deregistered when it ends. A 10-year renewal can be renewed again later. Both pay the Prevailing Quota Premium (PQP) set by LTA. If you plan to keep the car long term and it is in good condition, 10 years may suit you; if you only need it for a few more years, 5 years may be enough."),
 ("Can I choose a bank loan or an in-house loan?",
  "Yes. You can choose from bank or in-house financing for your COE renewal. WhatsApp us for a quote and we'll go through the options for your car. " + NOTE),
 ("What does the COE renewal loan cover?",
  "It is financing to help you pay for renewing your car's COE. Tell us your plate number and model on WhatsApp and we'll explain what your option covers before you decide. " + NOTE),
 ("What is the free pre-renewal check?",
  "It is a check of your car at our Ang Mo Kio workshop before you renew, normally worth $80, so you know about any work the car may need for the years ahead. It is free only when you take your COE renewal loan with Edwin Garage."),
 ("What should I prepare?",
  "Usually your NRIC, your vehicle log card or registration details, and your car's current COE expiry date. We'll confirm exactly what is needed for your case on WhatsApp."),
 ("Can I service my car at the same time?",
  "Yes. Many owners combine the renewal with servicing or repairs found in the pre-renewal check. Car servicing starts from $128 for Japanese and Korean cars and from $148 for Continental cars, including parts, labour and GST, and the final price is confirmed before any work starts."),
 ("How do I start?",
  "WhatsApp us on 9785 6612 with your plate number and car model. We'll check your options and explain the next steps."),
]

def strip(s): return re.sub(r"<[^>]+>", "", s)

def build():
    biz = {"@type": ["AutoRepair", "LocalBusiness"], "@id": BASE + "/#business", "name": "Edwin Garage Aircon & Car Repair",
           "legalName": "Edwin Garage Automotive Services Pte. Ltd.", "alternateName": ["SG Garage", "SGGarage", "Edwin Garage"],
           "url": BASE + "/", "telephone": "+6597856612",
           "address": {"@type": "PostalAddress", "streetAddress": "Blk 5032 Ang Mo Kio Industrial Park 2 #01-295",
                       "addressLocality": "Ang Mo Kio", "addressRegion": "Singapore", "postalCode": "569535", "addressCountry": "SG"},
           "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "10:00", "closes": "20:00"}],
           "sameAs": ["https://share.google/hYkZhnKyoAEeERhWM", "https://www.facebook.com/edwingarageamk/", "https://www.facebook.com/sggarageedwin/"]}
    graph = [biz,
        {"@type": "WebPage", "@id": URL + "#webpage", "url": URL, "name": H1, "description": DESC, "inLanguage": "en-SG",
         "datePublished": TODAY, "dateModified": TODAY, "about": {"@id": BASE + "/#business"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "COE Renewal Loan", "item": URL}]},
        {"@type": "FAQPage", "@id": URL + "#faq", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in FAQS]}]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")
    e = lambda s: html.escape(s, quote=True)
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQS)
    head = ('<!doctype html><html lang="en-SG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>{e(TITLE)}</title><meta name="description" content="{e(DESC)}">'
        f'<meta property="og:title" content="{e(TITLE)}"><meta property="og:description" content="{e(DESC)}">'
        f'<meta name="twitter:title" content="{e(TITLE)}"><meta name="twitter:description" content="{e(DESC)}">'
        f'<link rel="canonical" href="{URL}"><meta name="robots" content="index,follow,max-image-preview:large">'
        f'<meta property="og:type" content="website"><meta property="og:site_name" content="Edwin Garage"><meta property="og:url" content="{URL}">'
        f'<meta property="og:image" content="{OG}"><meta property="og:image:alt" content="Edwin Garage car repair and servicing workshop, Ang Mo Kio, Singapore">'
        f'<meta property="og:locale" content="en_SG"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{OG}">'
        '<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">'
        '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
        f'<style>{CSS}</style><script type="application/ld+json">{ld}</script></head>')
    body = f"""<body>{NAV}<main><section class="hero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> › COE Renewal Loan</nav><p class="eyebrow">Edwin Garage · Ang Mo Kio</p><h1>{e(H1)}</h1><p class="lead">COE prices are rising, so renewing your COE and keeping a car you know can make sense. Ask us about COE renewal financing options: choose from bank or in-house financing, and we'll help with the steps.</p><div class="actions">{wa_btn("coe-hero")}<a class="btn alt" href="/car-servicing-repair/">Car servicing &amp; repair</a></div><p class="fin">{NOTE}</p>{OFFER_TOP}</div></section>
<section class="section"><div class="wrap"><h2>Why renew your COE now?</h2><p class="intro">COE prices have been rising, so replacing a car costs more than it used to. When your COE is close to expiring, you have a choice: renew it and keep driving the same car, or scrap (deregister) the car and buy another one.</p><div class="two"><article class="card"><h3>Renewing</h3><p>You pay the Prevailing Quota Premium (PQP) set by LTA and keep the car for another 5 or 10 years. This can suit a car that is in good condition and does what you need.</p></article><article class="card"><h3>Scrapping</h3><p>The car is deregistered and taken off the road. Depending on the car, you may get some money back; check the official figures for your car before you decide.</p></article></div><p class="src">Official COE renewal rules and the current PQP are published by LTA on <a href="https://onemotoring.lta.gov.sg/" target="_blank" rel="noopener">OneMotoring</a>. We don't quote figures here because they change.</p></div></section>
<section class="section alt"><div class="wrap"><h2>How the COE renewal loan works</h2><div class="steps"><div class="step"><h3>WhatsApp us</h3><p>Message us on 9785 6612 to ask about a COE renewal loan.</p></div><div class="step"><h3>Tell us your car</h3><p>Send your plate number and car model.</p></div><div class="step"><h3>We check your options</h3><p>Choose from bank or in-house financing, and we explain the options for your car.</p></div><div class="step"><h3>Paperwork</h3><p>We guide you through the documents needed for your application.</p></div><div class="step"><h3>Renew</h3><p>Renew your COE and keep driving, after the pre-renewal check.</p></div></div><p class="fin">{NOTE}</p></div></section>
<section class="section"><div class="wrap"><h2>What to bring</h2><ul class="list"><li>Your NRIC</li><li>Your vehicle log card or registration details</li><li>Your car's current COE expiry date</li></ul><p class="intro">This is a general guide. We'll confirm exactly what is needed for your case on WhatsApp.</p></div></section>
<section class="section alt"><div class="wrap"><h2>Check your car before you renew</h2><p class="intro">If you are keeping a car for another 5 or 10 years, have it checked first. A pre-renewal check at our Ang Mo Kio workshop shows what the car may need, so you can plan servicing or repairs with no surprises. You can also book <a href="/car-servicing-repair/">car servicing and repair</a> at the same time; servicing starts from $128 for Japanese and Korean cars and from $148 for Continental cars, including parts, labour and GST, with the final price confirmed before any work starts.</p><div class="actions">{wa_btn("coe-check")}</div></div></section>
{OFFER_FAQ}
<section class="section alt"><div class="wrap"><h2>Frequently asked questions</h2><div class="faq">{faq_html}</div></div></section>
<section class="cta-band"><div class="wrap"><h2>Renewing your COE?</h2><p>WhatsApp us on 9785 6612 with your plate number and model. Choose from bank or in-house financing, plus a free pre-renewal check (worth $80) when you take your COE renewal loan with Edwin Garage. {NOTE}</p><div class="actions"><a class="btn" href="{e(WA)}" target="_blank" rel="noopener" data-ref="coe-band">WhatsApp us for a quote</a></div></div></section>
</main>{FOOTER}</body></html>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w").write(head + body)
    print(OUT, len((head + body).encode()))

if __name__ == "__main__":
    build()
