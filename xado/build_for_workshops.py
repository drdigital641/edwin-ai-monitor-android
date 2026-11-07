"""Builds xado/site/for-workshops/index.html (7 Nov 2026, Edwin approved, live directly).
Header/footer are taken from xado/site/articles/index.html so the page matches the site.
Claims come only from the existing site (about, how-it-works, product guide, become-a-dealer)."""
import json, html, os, re, urllib.parse

D = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(D, 'site')
URL = 'https://xado-shop.sg/for-workshops/'
WA_NUM = '6593391185'           # XADO Singapore WhatsApp (Edwin: use this as Roland's contact)
WA_SHOW = '+65 9339 1185'
TITLE = 'XADO for Workshops in Singapore | No Minimum Order'
DESC = ('Workshops in Singapore can add XADO engine treatments and oils with no minimum order and no obligation. '
        'WhatsApp XADO, or ask your own workshop to stock it.')
ROLAND_TEXT = "Hi Roland, I'm from [workshop name], interested in XADO for my workshop."

FAQ = [
    ('Is there a minimum order to start with XADO?',
     'No. There is no minimum order and no obligation. WhatsApp XADO Singapore on +65 9339 1185 and Roland will talk you through it.'),
    ('How does my workshop become an authorised XADO workshop?',
     'Message XADO Singapore on WhatsApp, call the distributor on +65 6876 1456 or email enquiries@revsolutions.com.sg. '
     'Authorised workshops are listed on the Find a XADO workshop page of this site, so drivers can message them directly.'),
    ('Who distributes XADO in Singapore?',
     'Rev Solutions Pte Ltd is the exclusive distributor of XADO in Singapore. XADO products are made under XADO Germany and XADO Lube B.V. (Netherlands) licences.'),
    ('How is a XADO engine treatment applied?',
     'It is added at a normal oil service. XADO says to warm the engine, switch it off, pour the treatment into the oil filler without going above the dipstick maximum, then run the engine for 3 to 5 minutes. No engine strip-down is needed.'),
    ('Can XADO fix a broken engine?',
     'No. XADO describes its products as protection and wear restoration for worn friction surfaces, not a repair for broken parts. A damaged engine needs a proper repair first.'),
    ('My regular workshop does not carry XADO. What can I do?',
     'Use the form on this page to send your workshop a ready-made WhatsApp message asking them to contact XADO Singapore. '
     'There is no minimum order and no obligation for them. Or find one of the authorised XADO workshops.'),
]

def esc(s): return html.escape(s, quote=True)

tpl = open(os.path.join(SITE, 'articles', 'index.html')).read()
head_end = tpl.index('</head>')
body_start = tpl.index('<body')
main_start = tpl.index('<main')
main_end = tpl.index('</main>') + len('</main>')
header = tpl[body_start:main_start]
footer = tpl[main_end:]

org = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', tpl, re.S).group(1))[0]
ld = [org,
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://xado-shop.sg/index.html"},
          {"@type": "ListItem", "position": 2, "name": "For workshops", "item": URL}]},
      {"@context": "https://schema.org", "@type": "WebPage", "name": TITLE, "url": URL, "description": DESC,
       "inLanguage": "en-SG", "about": {"@type": "Brand", "name": "XADO"},
       "audience": {"@type": "BusinessAudience", "audienceType": "Car workshops in Singapore"},
       "potentialAction": {"@type": "CommunicateAction", "name": "WhatsApp XADO Singapore",
                           "target": "https://wa.me/" + WA_NUM}},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
          {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}]

head = tpl[:head_end]
head = re.sub(r'<title>.*?</title>', '<title>%s</title>' % esc(TITLE), head)
head = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="%s">' % esc(DESC), head)
head = re.sub(r'<link rel="canonical" href="[^"]*">', '<link rel="canonical" href="%s">' % URL, head)
head = re.sub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="%s">' % esc(TITLE), head)
head = re.sub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="%s">' % esc(DESC), head)
head = re.sub(r'<meta property="og:url" content="[^"]*">', '<meta property="og:url" content="%s">' % URL, head)
head = re.sub(r'<script type="application/ld\+json">.*?</script>',
              lambda m: '<script type="application/ld+json">%s</script>' % json.dumps(ld, ensure_ascii=False), head, flags=re.S)
CSS = '''<style>
.fw-hero .lead{max-width:720px}
.nomin{display:inline-block;background:#e9fbf0;color:#0b6b33;border:1px solid #b6eccb;font-weight:700;border-radius:999px;padding:6px 14px;font-size:.92rem;margin:4px 0 14px}
.dark-band .nomin{background:#11351f;color:#b7f5cd;border-color:#1f6b3d}
.why{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:26px}
.why .card h3{margin-top:0}
.fw-split{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.fw-split figure{margin:0}.fw-split img{display:block;width:100%;height:auto;border-radius:16px}
.fw-split figcaption{font-size:.82rem;color:#999;margin-top:8px}
.ref-box{background:var(--soft);border:1px solid var(--line);border-radius:18px;padding:26px;max-width:640px}
.ref-box label{display:block;font-weight:700;margin:0 0 6px;color:var(--ink)}
.ref-box input{width:100%;font:inherit;font-size:1.05rem;padding:14px 16px;border:2px solid var(--line);border-radius:12px;background:#fff;color:var(--ink)}
.ref-box input:focus{outline:none;border-color:#25d366}
.ref-box input[aria-invalid=true]{border-color:var(--red)}
.ref-box .hint{font-size:.85rem;color:var(--mut);margin:6px 0 14px}
.ref-err{color:var(--red);font-weight:600;font-size:.92rem;margin:0 0 12px;min-height:1.2em}
.ref-box button{cursor:pointer;font:inherit;font-weight:700}
.ref-preview{font-size:.85rem;color:var(--mut);background:#fff;border:1px dashed var(--line);border-radius:12px;padding:12px 14px;margin-top:16px}
.btn.wa svg{width:20px;height:20px}
@media(max-width:900px){.why{grid-template-columns:1fr 1fr}.fw-split{grid-template-columns:1fr;gap:24px}}
@media(max-width:600px){.why{grid-template-columns:1fr}.ref-box{padding:18px}.ref-box button,.fw-wa{width:100%;justify-content:center}}
</style>
'''
head += CSS

WA_SVG = ('<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16.04 3C9.4 3 4 8.4 4 15.04c0 2.12.56 4.2 1.62 6.02L4 29l8.13-1.58a12 12 0 0 0 3.9.65h.01C22.68 28.07 28 22.67 28 16.03 28 9.4 22.68 3 16.04 3zm0 22.1c-1.24 0-2.45-.22-3.6-.65l-.58-.22-4.82.94.97-4.7-.25-.6a9.9 9.9 0 0 1-.83-3.97c0-5.5 4.48-9.98 9.99-9.98s9.98 4.48 9.98 9.98c0 5.5-4.47 9.2-9.98 9.2zm5.48-7.47c-.3-.15-1.77-.87-2.04-.97-.27-.1-.47-.15-.67.15s-.77.97-.94 1.17c-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.49-.9-.8-1.5-1.78-1.67-2.08-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48 0 1.47 1.07 2.88 1.22 3.08.15.2 2.1 3.2 5.08 4.49.71.3 1.27.49 1.7.63.72.23 1.37.2 1.88.12.57-.09 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35z"/></svg>')
roland_href = 'https://wa.me/%s?text=%s' % (WA_NUM, urllib.parse.quote(ROLAND_TEXT))

WHY = [
    ('Drivers are told to ask for it', 'This site tells Singapore drivers to ask for XADO by name at their next oil change, and sends them to authorised workshops to do it.'),
    ('Listed on the workshop finder', 'Authorised workshops get a listing on the XADO Singapore workshop finder, with a WhatsApp button so drivers message you directly.'),
    ('Added at a normal oil service', 'Engine treatments go into the oil filler at a normal service, with no engine strip-down. It fits into work you already do.'),
    ('A range for common jobs', 'Engine treatments, oils with Revitalizant® built in, and EX120 formulas for automatic, CVT, DSG and manual gearboxes and power steering.'),
    ('An established European brand', 'XADO was founded in 1991 and sells in more than 100 countries. Production runs under XADO Germany and XADO Lube B.V. (Netherlands) licences.'),
    ('Honest to sell', 'XADO positions its products as protection and wear restoration, not a fix for broken parts, so customer expectations stay realistic.'),
]

MAIN = '''<main id="main"><nav class="crumbs wrap" aria-label="Breadcrumb"><a href="../index.html">Home</a> › <span>For workshops</span></nav>
<header class="page-hero fw-hero"><div class="wrap"><p class="kicker">For workshops</p><h1>Offer XADO at your workshop</h1>
<p class="lead">XADO Singapore helps car workshops add XADO engine treatments and oils to their services. Message XADO on WhatsApp and Roland will take you through how it works.</p>
<p class="nomin">No minimum order, no obligation</p>
<div class="hero-btns"><a class="btn wa fw-wa" href="{ROLAND}" target="_blank" rel="noopener" data-cta="workshop_wa_roland" data-ref="workshop_wa_roland">{SVG}WhatsApp XADO (Roland)</a></div>
</div></header>

<section class="wrap"><h2>Why workshops offer XADO</h2>
<p>XADO Singapore exists to send drivers to workshops that offer XADO. Here is what that means for your workshop.</p>
<div class="why">{WHY}</div>
<p class="note">Product effects described on this site are XADO's own claims. Results depend on engine condition, oil and maintenance history.</p></section>

<section class="dark-band"><div class="wrap fw-split">
<div><p class="kicker">How to start</p><h2>Talk to XADO Singapore first</h2>
<ol class="big"><li>Tap the WhatsApp button and send the message with your workshop's name.</li><li>Roland from XADO Singapore replies to talk about the range, trade pricing, training and point-of-sale material.</li><li>Start with what suits your customers. There is no minimum order and no obligation.</li></ol>
<p class="nomin">No minimum order, no obligation</p>
<div class="hero-btns"><a class="btn wa fw-wa" href="{ROLAND}" target="_blank" rel="noopener" data-cta="workshop_wa_roland" data-ref="workshop_wa_roland_2">{SVG}WhatsApp XADO (Roland)</a></div>
<p class="note">Prefer the distributor directly? Call Rev Solutions on <a href="tel:+6568761456">+65 6876 1456</a> or email <a href="mailto:enquiries@revsolutions.com.sg?subject=XADO%20for%20my%20workshop">enquiries@revsolutions.com.sg</a>.</p></div>
<figure><picture><source type="image/webp" srcset="../assets/img/workshop/xado-1-stage-motor-oil-label-workshop.webp"><img src="../assets/img/workshop/xado-1-stage-motor-oil-label-workshop.jpg" alt="Mechanic holding a can of XADO 1 Stage full synthetic motor oil at an authorised XADO workshop in Singapore" width="900" height="1200" loading="lazy" decoding="async"></picture><figcaption>XADO 1 Stage full synthetic motor oil at an authorised XADO workshop in Singapore.</figcaption></figure>
</div></section>

<section class="wrap" id="ask-your-workshop"><p class="kicker dark">For drivers</p><h2>Want XADO at your own workshop?</h2>
<p>Happy with your regular mechanic, but they don't carry XADO yet? Send them a ready-made WhatsApp message asking them to contact XADO Singapore. It costs them nothing to ask: no minimum order, no obligation.</p>
<form class="ref-box" id="ref-form" novalidate onsubmit="return false">
<label for="ws-num">Your workshop's WhatsApp number</label>
<input id="ws-num" name="ws-num" type="tel" inputmode="tel" autocomplete="off" placeholder="e.g. 9123 4567" aria-describedby="ws-hint ws-err">
<p class="hint" id="ws-hint">A Singapore mobile number: 8 digits starting with 8 or 9. You can include +65.</p>
<p class="ref-err" id="ws-err" role="alert" aria-live="polite"></p>
<button type="button" class="btn wa" id="ws-go">{SVG}WhatsApp my workshop</button>
<div class="ref-preview"><strong>Message your workshop will get:</strong><br><span id="ws-msg"></span></div>
</form>
<p class="note">The message opens in your own WhatsApp, so you can read or edit it before you send. We don't store the number. Or <a href="../find-a-xado-workshop.html">find an authorised XADO workshop</a>.</p></section>

<section class="wrap narrow"><h2>Questions from workshops and drivers</h2><div class="faq">{FAQ}</div></section>

<section class="cta-band"><div class="wrap ctain"><div><h2>Ready to offer XADO?</h2><p>No minimum order, no obligation. Message XADO Singapore and Roland will get back to you.</p></div><div class="ctabtn"><a class="btn wa fw-wa" href="{ROLAND}" target="_blank" rel="noopener" data-cta="workshop_wa_roland" data-ref="workshop_wa_roland_3">{SVG}WhatsApp XADO (Roland)</a><a class="btn ghost" href="../xado-products-guide.html">See the product range</a></div></div></section>
</main>
<script>
(function(){
var NUM='{WA_NUM}',SHOW='{WA_SHOW}';
var MSG="Hi, I'm one of your customers. I'd like you to use XADO oil on my car at my next service. Could you please contact XADO Singapore on WhatsApp at "+SHOW+" (wa.me/"+NUM+")? There is no minimum order and no obligation. Thank you!";
var inp=document.getElementById('ws-num'),err=document.getElementById('ws-err'),go=document.getElementById('ws-go');
document.getElementById('ws-msg').textContent=MSG;
function norm(v){var d=String(v||'').replace(/[\\s().-]/g,'');if(d.charAt(0)==='+')d=d.slice(1);if(/^0065/.test(d))d=d.slice(2);
  if(/^[89]\\d{7}$/.test(d))return'65'+d;if(/^65[89]\\d{7}$/.test(d))return d;return null}
window.xadoRefLink=function(v){var n=norm(v);return n?'https://wa.me/'+n+'?text='+encodeURIComponent(MSG):null};
function fail(m){err.textContent=m;inp.setAttribute('aria-invalid','true');inp.focus()}
inp.addEventListener('input',function(){if(err.textContent){err.textContent='';inp.removeAttribute('aria-invalid')}});
inp.addEventListener('keydown',function(e){if(e.key==='Enter'){e.preventDefault();go.click()}});
go.addEventListener('click',function(){var v=inp.value.trim();
  if(!v)return fail('Please type your workshop\\'s WhatsApp number first.');
  var link=window.xadoRefLink(v);
  if(!link)return fail('That doesn\\'t look like a Singapore mobile number. Please check it: 8 digits starting with 8 or 9, for example 9123 4567.');
  err.textContent='';inp.removeAttribute('aria-invalid');
  if(window.p1CtaTap)window.p1CtaTap('driver_refer_workshop',go);
  var w=window.open(link,'_blank','noopener');if(!w)location.href=link});
})();
</script>
'''
why_html = ''.join('<div class="card"><h3>%s</h3><p>%s</p></div>' % (esc(t), esc(p)) for t, p in WHY)
faq_html = ''.join('<details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in FAQ)
rep = {'{ROLAND}': esc(roland_href), '{WHY}': why_html, '{FAQ}': faq_html, '{SVG}': WA_SVG,
       '{WA_NUM}': WA_NUM, '{WA_SHOW}': WA_SHOW}
for k, v in rep.items():
    MAIN = MAIN.replace(k, v)

# nav: add "For Workshops" and mark it
if '../for-workshops/' in header:
    header = header.replace('<a href="../for-workshops/">For Workshops</a>', '<a href="../for-workshops/" aria-current="page">For Workshops</a>')
else:
    header = header.replace('<a href="../articles/">Articles</a>',
                            '<a href="../articles/">Articles</a><a href="../for-workshops/" aria-current="page">For Workshops</a>')
if '../for-workshops/' not in footer: footer = footer.replace('<a href="../find-a-xado-workshop.html#become-a-dealer">Become a XADO dealer</a>',
                        '<a href="../for-workshops/">XADO for workshops</a><a href="../find-a-xado-workshop.html#become-a-dealer">Become a XADO dealer</a>')
page = head + '</head>\n' + header + MAIN + footer
os.makedirs(os.path.join(SITE, 'for-workshops'), exist_ok=True)
open(os.path.join(SITE, 'for-workshops', 'index.html'), 'w').write(page)
print('ok', len(page), len(TITLE), len(DESC))
