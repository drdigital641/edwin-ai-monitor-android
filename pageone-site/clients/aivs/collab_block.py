
# ---- Business Collaboration page (client copy via Edwin, 26 Oct 2026) ----
COLLAB_TECH = ['AI-powered recognition or automation', 'Smart inventory management', 'IoT connectivity and remote monitoring',
               'Intelligent or robotic dispensing systems', 'Automated retail with advanced smart features']
COLLAB_WHY = ['Showcase your machines on AIVS.sg', 'Increase online visibility', 'Reach potential buyers in Singapore',
              'Generate sales enquiries', 'Explore referral or reseller partnerships']
COLLAB_RULES = ['Singapore-based suppliers and distributors only.', 'Machines must have genuine AI or smart technology features.',
                'No conventional vending machines with only basic payment or dispensing functions.', 'All machine listings are subject to AIVS approval.']
COLLAB_FAQ = [
    ('Who can partner with AIVS?', 'Singapore-based suppliers and distributors of vending machines with genuine AI or smart technology features. Traditional vending machines without meaningful AI or smart capabilities are not eligible.'),
    ('What does AIVS do, and what does the partner do?', 'AIVS focuses on digital marketing and generating enquiries. Partners handle machine supply, installation, warranty and after-sales support.'),
    ('How do I apply?', 'Email info@aivs.sg or WhatsApp +65 %s with your company name, the machines you offer and their AI or smart features. All machine listings are subject to AIVS approval.' % WA_SHOW),
]


def collab_body():
    ticks = lambda items: '<ul class="ticks">%s</ul>' % ''.join('<li>%s</li>' % E(x) for x in items)
    return f'''<section class="sec"><div class="wrap split">
<article class="prose">
<figure class="lead-fig">{img('both-machines', eager=True)}</figure>
<h2>Do you have an AI or smart vending machine? Let's collaborate!</h2>
<p>Are you a Singapore-based supplier or distributor offering innovative vending machines powered by AI or smart technology?</p>
<p>AIVS.sg is looking for local partners who want to increase their online exposure and reach more potential buyers.</p>
<p>AIVS is expanding beyond its existing AI Printbox and helmet vending machines. Our new direction is to become a multi-brand AI and smart vending machine platform in Singapore, collaborating with local suppliers and distributors offering machines equipped with AI technology or genuine smart features.</p>
<h2>We welcome machines featuring technologies such as</h2>
{ticks(COLLAB_TECH)}
<p>Traditional vending machines without meaningful AI or smart capabilities are not eligible.</p>
<h2>Why partner with AIVS?</h2>
{ticks(COLLAB_WHY)}
<p>Interested? Contact <a href="mailto:{EMAIL}">{EMAIL}</a> or WhatsApp +65 {WA_SHOW}.</p>
<h2>Important</h2>
{ticks(COLLAB_RULES)}
<h2>Our goal</h2>
<p>Position AIVS.sg as Singapore's dedicated platform for discovering innovative AI and smart vending solutions.</p>
<p>AIVS will focus on digital marketing and generating enquiries, while our partners handle machine supply, installation, warranty and after-sales support.</p>
<h2>Frequently asked questions</h2>
{faq_html(COLLAB_FAQ)}
</article>
<aside class="side"><div class="card sticky"><h2>Partner with AIVS</h2><p>Tell us your company, the machines you offer and their AI or smart features. Singapore-based suppliers and distributors only.</p>{mail_btn('Email info@aivs.sg')}{wa_btn('WhatsApp AIVS', topic='a business collaboration.')}
<p class="small" style="margin-top:14px">Also read:</p><ul class="small" style="margin:0 0 0 18px"><li><a href="ai-vending-machine-singapore/">AI vending machines</a></li><li><a href="smart-vending-machine-singapore/">Smart vending machines</a></li><li><a href="about/">About AIVS</a></li></ul></div></aside>
</div></section>'''


page('partner-with-aivs/', 'Business Collaboration with AIVS | Smart Vending Singapore',
     'Partner with AIVS: Singapore suppliers and distributors of AI or smart vending machines can showcase machines on AIVS.sg. Contact info@aivs.sg.',
     "Partner With AIVS: Let's Grow the Future of Smart Vending", collab_body(), crumbs=[('partner-with-aivs/', 'Business collaboration')],
     lede='A multi-brand platform for AI and smart vending machines in Singapore. AIVS markets and generates enquiries; partners supply, install and support the machines.',
     photo='both-machines', cta=False, schema=[faq_schema(COLLAB_FAQ)])

