"""Entries for the SG Car Workshop directory (preview). Every fact has a source note in `source`.

Rules (MASTER-RULES 1-4, PLAN.md): verified facts only; if a fact is not in the client's own build files it is left out;
card wording is fresh (never copied from the client's site); no ratings or review schema; no bypass work; no prices
unless confirmed.

tier (PLAN.md "Tiers", Edwin 1 Nov 2026, permanent rule: a premium listing never has less than a free one):
  "free"             Basic: card plus a SHORT profile page (/workshops/<slug>/): one Google photo slot, short text, plain service names,
                     address + Directions, hours, Google rating line (text only), WhatsApp or Call. No gallery, FAQs, service
                     descriptions, prices or carousel placement (those are Verified/Premium)
  "premium"          full page: real photos, job gallery, services, full address, phone, WhatsApp + Call, map, reviews line with
                     source link and date (no rating schema), FAQs, LocalBusiness data
  "premium_leadgen"  everything in premium, plus the business's own website (Page One own-domain clients): badge
                     "Premium", website link as a SECONDARY button below WhatsApp/Call
"""

PAGE_ONE_WA = "6597856612"  # pageone-site/builder/build.py: WA = "6597856612" (Edwin / Page One Singapore)
PAGE_ONE_WA_SHOW = "9785 6612"

CATEGORIES = [
    dict(slug="spray-painting-bodywork", name="Spray painting and bodywork", short="Spray painting",
         icon="spray",
         blurb="Respray, colour change and body kit work in a spray booth.",
         intro="Car spray painting covers panel respray, full respray and colour change. A workshop sands the old paint, "
               "fixes any dents, primes the panel and sprays colour and clear coat in a booth. Ask for a quote with photos "
               "of your car, and check LTA rules before changing your car's colour."),
    dict(slug="gearbox-repair", name="Gearbox repair", short="Gearbox",
         icon="gear",
         blurb="Automatic gearbox diagnosis, repair, servicing and upgrades.",
         intro="Gearbox repair starts with a diagnosis: reading the car's fault codes, checking the fluid and test driving it. "
               "From there a specialist can service, repair or overhaul the gearbox. Slipping gears, harsh shifts and warning "
               "lights are common reasons to book in early, before a small fault grows."),
    dict(slug="abs-ecu-module-repair", name="ABS, ECU and module repair", short="ABS and ECU",
         icon="chip",
         blurb="Repair of ABS pumps and control modules instead of costly replacement.",
         intro="ABS and ECU module repair fixes the electronic units that control braking, gearbox shifts and engine functions. "
               "Many warning lights come from a failed pump or circuit board, not the whole car. A specialist tests the unit, "
               "repairs it on the bench where possible and refits it. Ask for the car model and fault codes."),
    dict(slug="car-battery", name="Car battery replacement", short="Car battery",
         icon="battery",
         blurb="Battery testing and replacement, at a workshop or where your car is.",
         intro="A car battery that struggles to start the engine, or has been flat more than once, usually needs testing and "
               "often replacement. Some providers come to your car, others fit it at a workshop. Share your car model so the "
               "right battery size is matched, and ask about warranty before you pay."),
    dict(slug="car-detailing-coating", name="Car detailing and coating", short="Detailing",
         icon="sparkle",
         blurb="Grooming, steam cleaning, fumigation and odour removal for your car.",
         intro="Car detailing cleans and restores the inside and outside of a car beyond a normal wash. It can cover interior "
               "steam cleaning, fumigation, odour removal, polishing and protective coatings. Some detailers travel to you. "
               "Tell them what bothers you most, such as smell, stains or dull paint, so the job fits."),
    dict(slug="car-wrap-ppf", name="Car wrap and PPF", short="Wrap and PPF",
         icon="film",
         blurb="Colour change wraps, paint protection film and window film.",
         intro="A car wrap changes colour with vinyl, while paint protection film (PPF) is a clear or coloured layer that shields "
               "the paint from stone chips and scratches. Window film is a separate service. Ask what film is used, how long the "
               "job takes, and check current LTA rules before changing your car's colour."),
    dict(slug="car-parts", name="Car parts", short="Car parts",
         icon="parts",
         blurb="Parts shops for specific makes, with models and part types to browse.",
         intro="A car parts shop supplies the pieces a workshop or a driver needs for a repair, such as filters, brakes and "
               "suspension. Some shops focus on one maker, which helps when you need the correct part for a specific model. "
               "Bring your car model and plate details, or send photos of the old part."),
    dict(slug="general-servicing-repair", name="General servicing and repair", short="Servicing",
         icon="wrench",
         blurb="Everyday servicing and repairs: battery checks, alternators, aircon and more.",
         intro="General servicing keeps a car reliable between the big repairs. A workshop checks fluids, the battery, charging "
               "system and aircon, then fixes what it finds. Tell the workshop your symptoms, such as a flat battery or weak "
               "cooling, and ask for the fault explained and the price confirmed before work starts."),
]

# Singapore's five URA planning regions (North, North-East, East, West, Central). A region page is built only if a listing covers it.
REGIONS = {
    "north": dict(name="North", intro="Car workshops and services in the North region of Singapore, which takes in Yishun, Woodlands, Sembawang and Kranji. "
                  "Some listings here are mobile or onsite and come to your car."),
    "north-east": dict(name="North-East", intro="Car workshops and services in the North-East region of Singapore, including Ang Mo Kio, Hougang, Sengkang, "
                       "Punggol and Serangoon."),
    "east": dict(name="East", intro="Car workshops and services in the East region of Singapore, which includes the Kaki Bukit and Bedok car trade units."),
    "west": dict(name="West", intro="Car workshops and services in the West region of Singapore, including Bukit Batok, Bukit Panjang and Boon Lay. "
                 "Listings here are mobile services or have an outlet in the west."),
    "central": dict(name="Central", intro="Car workshops and services in the Central region of Singapore, including Toa Payoh, Bukit Timah, Upper Thomson "
                    "and the Jervois and Havelock Road areas."),
}


# Tier names, badges and monthly prices (S$). Edwin set these on 1 Nov 2026. The Verified S$20 is the DIRECTORY Verified listing;
# it is not Page One's older S$20 early-bird SEO plan. Prices live here so they change in one place.
TIERS = {
    "free": dict(label="Basic listing", badge="Basic listing", price=0, price_text="Free", tagline="Get found"),
    "premium": dict(label="Verified listing", badge="Verified", price=20, price_text="Ask us on WhatsApp", tagline="Landing page"),
    "premium_leadgen": dict(label="Premium", badge="Premium", price=50, price_text="Ask us on WhatsApp", tagline="Full Page One website setup"),
}
PRICE_NOTE = "Prices are not published: ask us on WhatsApp. Basic is free."  # Edwin 1 Nov 2026: Verified S$20/mo, Premium S$50/mo, internal only

# One clearly labelled example of the free tier, shown only on /list-your-workshop/ (made-up name, not a real business).
FREE_EXAMPLE = dict(
    name="Your Workshop Name", category="general-servicing-repair", area_label="Your area, Singapore",
    text="A short description of what your workshop does, in one or two lines.", site_label="yourwebsite.example")

WD = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
SAT = ["Saturday"]

# Photos: "f" = file in src/img (copied to site/assets/img); "u" = absolute URL hotlinked from the client's own live pages (preview only).
# Prose is written fresh (never copied from the client's site). Prices only where the client's own live page publishes them.
_SG = "https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@ebdf067f4edf3a93c5ac6a73b1c127675dfa3eac/site-assets/sggarage/"
_ECU = "https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@cee16fe230df8b19cf7d5b0562dd956c9d36b813/pageone-site/clients/ecu-clinic/site/img/"
_WS = "https://cdn.jsdelivr.net/gh/drdigital641/edwin-ai-monitor-android@da2c02e/site-assets/wrapstar/"
_CL = "https://www.cleanicdetailing.com/wp-content/uploads/cleanic-photos/"
_JG = "https://jackygearbox.com/img/"
_BR = "https://batteryrescue.sg/photos/"
_AT = "https://autotexautoparts.com.sg/assets/parts/"

ENTRIES = [
    dict(
        slug="wei-car-spray-painting", tier="premium",
        name="Wei Car Spray Painting", legal="Wei Car Spray Painting Pte. Ltd.", uen="201215981N",
        category="spray-painting-bodywork", regions=['north'], regions_note='Yishun is in the North region (URA). Address: Yishun Industrial Park A.', area_label="Yishun",
        title="Wei Car Spray Painting | Yishun Car Spray Painting",
        desc="Wei Car Spray Painting is a spray painting and bodywork workshop in Yishun for resprays, colour changes and body kits. WhatsApp 9638 3306.",
        card_img=dict(f="wei/jobs-mg-british-racing-green.webp", alt="MG sprayed in British Racing Green at Wei Car Spray Painting"),
        card_text=["Spray painting and bodywork at a Yishun industrial park workshop.",
                   "Colour changes, full resprays and body kit fitting."],
        lede=("Wei Car Spray Painting is a spray painting and bodywork workshop at Blk 1017 Yishun Industrial Park A, Singapore. It resprays single panels "
              "and whole cars, changes car colours and fits body kits. WhatsApp or call 9638 3306 with photos of your car to ask about your job."),
        services=[
            dict(n="Car spray painting", d="Single panels or several panels resprayed in your car's colour.", p=None),
            dict(n="Full respray and colour change", d="The whole car repainted in its own colour or a new one. Check the current LTA rules on OneMotoring before you change your car's colour.", p=None),
            dict(n="Body kit installation", d="Kits and spoilers fitted to the car and painted to match.", p=None),
        ],
        price_note="Prices are not listed. Ask Wei on WhatsApp with photos of your car.",
        phone="+6596383306", phone_show="9638 3306", whatsapp="6596383306",
        addresses=[dict(label=None, street="Blk 1017 Yishun Industrial Park A, #01-242, #01-246 and #01-252", postal="768759")],
        map_url="https://www.google.com/maps/search/?api=1&query=Wei%20Car%20Spray%20Painting%2C%201017%20Yishun%20Industrial%20Park%20A%20%2301-242%20Singapore%20768759",
        hours=[("Mon to Fri", "9am to 7pm"), ("Sat", "9am to 5:15pm"), ("Sun", "Closed")],  # Google business listing, checked 1 Nov 2026
        hours_ld=[(WD, "09:00", "19:00"), (SAT, "09:00", "17:15")], hours_note="Hours from the workshop's Google listing (checked 1 Nov 2026). Call or WhatsApp to confirm before you visit.",
        social=["https://www.facebook.com/share/19YgRcqvBh/", "https://www.instagram.com/weicarspraypainting/"],
        reviews=dict(text="100% recommend on Facebook from 238 reviews (checked 1 November 2026)", url="https://www.facebook.com/share/19YgRcqvBh/", label="See the Facebook page"),
        photos=[
            dict(f="wei/shopfront.webp", alt="Wei Car Spray Painting signboard and spray booth at Blk 1017 Yishun Industrial Park A", cap="The workshop and spray booth."),
            dict(f="wei/jobs-mg-british-racing-green.webp", alt="MG after an exterior respray in British Racing Green", cap="MG exterior respray in British Racing Green, November 2023."),
            dict(f="wei/jobs-honda-civic-grey-blue.webp", alt="Honda Civic after a full respray with a gloss black roof and a new spoiler", cap="Honda Civic: full respray, gloss black roof and a new spoiler, November 2023."),
            dict(f="wei/jobs-mini-cooper-pink.webp", alt="Mini Cooper after a colour change to pink", cap="Mini Cooper colour change from orange to pink, May 2022."),
            dict(f="wei/jobs-porsche-cayenne-bodykit-front.webp", alt="Porsche Cayenne with a new-model body kit installed", cap="Porsche Cayenne with a new-model body kit imported from overseas, February 2026."),
        ],
        og_img="wei/og.jpg",
        sections=[
            ("About the workshop", "p", [
                "The company, Wei Car Spray Painting Pte. Ltd., was incorporated in June 2012 (UEN 201215981N) and is registered for repair and maintenance of motor vehicles. The workshop is in Yishun Industrial Park A, across three adjoining units, and the shopfront photo shows its signboard with a spray booth behind it.",
                "Most of what the workshop posts on Facebook is paint work: full resprays, colour changes and the occasional body kit. One post, from March 2023, thanks a customer who was back for the fourth time."]),
            ("Jobs the workshop has posted", "ul", [
                "Porsche Macan: full body colour change to Fountain Blue Metallic, May 2025.",
                "Porsche Cayenne: new-model body kit, imported from overseas and installed, February 2026.",
                "MG: exterior respray in British Racing Green, November 2023.",
                "Honda Civic: full respray inside and out, gloss black roof and a new spoiler, November 2023.",
                "Mini Cooper: new colour, from orange to pink, May 2022."]),
            ("How to ask for a quote", "p", [
                "Send clear photos of the car in daylight, with the model and year, and say what you want done. Prices are not listed on this page, so ask Wei directly on WhatsApp."]),
        ],
        faqs=[
            ("Where is Wei Car Spray Painting?", "At Blk 1017 Yishun Industrial Park A, units #01-242, #01-246 and #01-252, Singapore 768759. The Google Maps link on this page opens the location."),
            ("What work does the workshop do?", "Panel resprays, full resprays, colour changes and body kit installation with matching paint, done in a spray booth."),
            ("How do I get a quote?", "WhatsApp or call 9638 3306 with clear daylight photos of the car, its model and year, and what you want done. Prices are not listed on this page."),
            ("Can I change my car's colour freely?", "Check the current LTA rules on OneMotoring before you change your car's colour, and tell the workshop what you plan."),
        ],
        source=dict(
            name="ACRA (via acrawatch.sg / recordowl.com, data.gov.sg): WEI CAR SPRAY PAINTING PTE. LTD., UEN 201215981N, inc. 28 Jun 2012",
            address="ACRA registered address + Facebook page (screenshot 1 Nov 2026)",
            phone="Facebook page and own poster (8 Apr 2026): 9638 3306 (WhatsApp Now)",
            jobs="Facebook posts (screenshots from Edwin, 1 Nov 2026)",
            faqs="All FAQ answers restate facts already on this page"),
        left_out=["all prices", "scratch, dent, bumper repair, servicing and insurance-claim services (unconfirmed)",
                  "paint brands", "owner name", "second phone 6759 3229 (2022 listing)"],
    ),
    dict(
        slug="sg-garage", tier="premium_leadgen", name="SG Garage", domain="sggarage.com", url="https://sggarage.com/",
        category="general-servicing-repair", regions=['north-east'], regions_note='Ang Mo Kio is in the North-East region (URA). Address: Ang Mo Kio Industrial Park 2.', area_label="Ang Mo Kio",
        title="SG Garage | Car Servicing and Repair, Ang Mo Kio",
        desc="SG Garage (Edwin Garage) in Ang Mo Kio: servicing from $128, aircon, brakes, batteries and accident repair. WhatsApp 9785 6612, Mon to Sat.",
        card_img=dict(u=_SG + "edwin-garage-shopfront-01-295.webp", alt="SG Garage shopfront at Blk 5032 Ang Mo Kio Industrial Park 2"),
        card_text=["Owner-run car workshop in Ang Mo Kio Industrial Park 2, open Monday to Saturday.",
                   "Servicing from $128, aircon, brakes, batteries and accident repair."],
        lede=("SG Garage, also known as Edwin Garage, is an owner-run workshop in Ang Mo Kio Industrial Park 2. It services and repairs Japanese, Korean, "
              "European and electric cars, fixes car aircon and handles accident repairs with the insurance paperwork. WhatsApp 9785 6612 to ask about your car."),
        services=[
            dict(n="Car servicing", d="Engine oil and filter service. A major service is priced after the car is inspected.", p="From $128 (Japanese, Korean) / $148 (European)"),
            dict(n="Car aircon repair", d="Gas top-up after a leak check, chemical wash, and cooling coil or compressor replacement when the fault goes deeper.", p="Gas top-up from $20, chemical wash from $120, coil from $600, compressor from $800"),
            dict(n="Brake pads", d="Pad replacement, with the brakes checked before and after.", p="From $120 (Japanese) / $140 (European)"),
            dict(n="Car battery replacement", d="Walk-in, Monday to Saturday 10am to 8pm, subject to stock. The battery, alternator and starter are tested first so the right part is replaced.", p="From $120, AGM from $250"),
            dict(n="ABS pump repair", d="Repair of the ABS pump, with a new unit as the alternative.", p="Repair from $950, new unit from $1,600"),
            dict(n="Accident claim and spray painting", d="Accident repair with help on the insurance claim, panel beating and spray painting.", p="Quoted after inspection"),
            dict(n="Tesla, hybrid and EV work", d="Electric and hybrid cars are worked on in the same bays. Tesla jobs since 2019.", p=None),
        ],
        price_note="Prices are starting prices and include parts, labour and GST. The final price is confirmed after inspection and before work starts. Diagnosis is $30 if you decide not to go ahead.",
        phone="+6597856612", phone_show="9785 6612", whatsapp="6597856612",
        book_url="https://sggarageedwin.as.me/", book_label="Book a slot online",
        addresses=[dict(label=None, street="Blk 5032 Ang Mo Kio Industrial Park 2, #01-295", postal="569535", note="Ground floor, look for the green Edwin Garage signboard. About 5 to 10 minutes from Ang Mo Kio MRT.")],
        map_url="https://www.google.com/maps/search/?api=1&query=Edwin%20Garage%2C%205032%20Ang%20Mo%20Kio%20Industrial%20Park%202%20%2301-295%20Singapore%20569535",
        hours=[("Mon to Sat", "10am to 8pm"), ("Sun", "Closed")],
        hours_ld=[(WD + SAT, "10:00", "20:00")],
        hours_note="Servicing, repairs and diagnosis are by appointment. Battery replacement is walk-in, subject to stock.",
        social=[],
        reviews=dict(text="Rated 4.9 from 600+ Google reviews, as stated on sggarage.com (checked 1 November 2026)", url="https://share.google/hYkZhnKyoAEeERhWM", label="Read the Google reviews"),
        photos=[
            dict(u=_SG + "edwin-garage-shopfront-01-295.webp", alt="SG Garage shopfront with green signboard and cars parked outside", cap="The shopfront at unit #01-295."),
            dict(u=_SG + "edwin-garage-workshop-bays.webp", alt="A Kia on the lift and a Tesla Model 3 in the SG Garage service bay", cap="Inside the bays: a Kia on the lift and a Tesla Model 3 being worked on."),
            dict(u="https://sggarage.com/uploads/tesla-radiator-cleaning-hero.jpg", alt="Mechanic clearing dried leaves from a Tesla radiator", cap="Clearing dried leaves from a Tesla radiator."),
            dict(u="https://sggarage.com/uploads/tesla-lca-1.jpg", alt="Tesla suspension arms laid out during a lower control arm replacement", cap="Tesla lower control arm job: the suspension arms laid out."),
            dict(u="https://sggarage.com/uploads/tesla-lca-3.jpg", alt="Close-up of a worn Tesla control arm bushing", cap="A worn control arm bushing, close up."),
        ],
        note="SG Garage belongs to the founder of Page One Singapore, who built this directory. We list it like any other entry and say so openly.",
        faqs=[
            ("Do I need an appointment?", "Yes for servicing, repairs and diagnosis: book a slot online or message on WhatsApp. Battery replacement is the exception, it is walk-in from Monday to Saturday, 10am to 8pm, subject to stock."),
            ("Are the listed prices the final price?", "They are starting prices that cover parts, labour and GST. The final price is confirmed after the car is inspected, and nothing starts until you agree. If you decide against the repair, diagnosis is $30."),
            ("Where is SG Garage and when is it open?", "Blk 5032 Ang Mo Kio Industrial Park 2, #01-295, Singapore 569535, open Monday to Saturday, 10am to 8pm, closed on Sundays."),
            ("Which cars can it work on?", "Japanese, Korean and European cars, hybrids and electric cars. Tesla work has been part of the mix since 2019."),
            ("How can I pay?", "Cash or PayNow are preferred. Credit cards carry a 3% surcharge."),
        ],
        source=dict(name="sggarage.com live pages (index, about, prices), read via the Bluehost Bridge on 1 Nov 2026",
                    contact="Site says enquiries by WhatsApp; the same number is the telephone in its LocalBusiness data, so a Call button is shown (CONFIRM with Edwin)",
                    reviews="Home and about pages: 4.9 stars, 600+ Google reviews, share.google link"),
        left_out=["customer review quotes (rating line only)", "towing partner number (third party)"],
    ),
    dict(
        slug="jacky-gearbox", tier="premium_leadgen", name="Jacky Gearbox", domain="jackygearbox.com", url="https://jackygearbox.com/",
        category="gearbox-repair", regions=['north'], regions_note='Woodlands and Kranji are both in the North region (URA). Addresses: Woodlands Industrial Park E9 and Jalan Lam Huat.', area_label="Woodlands and Kranji",
        title="Jacky Gearbox | Gearbox Repair, Woodlands and Kranji",
        desc="Jacky Gearbox: gearbox diagnosis from S$30, repair, overhaul, servicing and upgrades at Woodlands and Kranji. 6-month warranty. WhatsApp 8430 9665.",
        card_img=dict(u=_JG + "hero-workshop.webp", alt="Jacky Gearbox workshop in Woodlands"),
        card_text=["Gearbox specialist with workshops in Woodlands and Kranji.",
                   "Diagnosis from S$30, repair, servicing and upgrades."],
        lede=("Jacky Gearbox is a gearbox and automatic transmission specialist with a main workshop at Woodlands Wave 9 and a second one in Kranji. "
              "Jacky tests the gearbox himself, explains the fault, quotes before any work starts and road-tests the car before handing it back. WhatsApp or call 8430 9665."),
        services=[
            dict(n="Gearbox diagnostic", d="Fault codes are read and the gearbox checked first, so the quote is based on the real cause.", p="From S$30"),
            dict(n="Gearbox repair and overhaul", d="Repair or full overhaul of automatic gearboxes, with a standard 6-month warranty unless stated otherwise.", p=None),
            dict(n="Gearbox upgrades", d="Strengthening work to suit the power and torque of the car.", p=None),
            dict(n="Gearbox (ATF) servicing", d="Regular transmission servicing with the correct fluid for the gearbox.", p=None),
            dict(n="Free towing and pick-up", d="Free pick-up to the workshop for gearbox repairs during office hours, and a free tow if the car cannot move.", p="Free"),
        ],
        price_note="No blind quotes: the diagnostic comes first, then a clear price before any repair starts.",
        phone="+6584309665", phone_show="8430 9665", whatsapp="6584309665",
        addresses=[
            dict(label="Woodlands (main workshop)", street="71 Woodlands Industrial Park E9, #01-25 Wave 9", postal="757048", map_url="https://www.google.com/maps/search/?api=1&query=71%20Woodlands%20Industrial%20Park%20E9%20Wave%209%20Singapore"),
            dict(label="Kranji (second workshop)", street="60 Jalan Lam Huat, #05-48", postal="737869", map_url="https://www.google.com/maps/search/?api=1&query=60%20Jalan%20Lam%20Huat%20Singapore%20737869"),
        ],
        map_url="https://www.google.com/maps/search/?api=1&query=71%20Woodlands%20Industrial%20Park%20E9%20Wave%209%20Singapore",
        hours=[("Mon to Fri", "9am to 6pm"), ("Sat", "9am to 3pm"), ("Sun and public holidays", "Closed")],
        hours_ld=[(WD, "09:00", "18:00"), (SAT, "09:00", "15:00")],
        hours_note=None, social=[],
        reviews=dict(text="Customer reviews are on Jacky's Google profile. His website does not state a rating or review count (checked 1 November 2026).", url="https://share.google/ZXSk6rE3VdUNgZyKS", label="Open the Google profile"),
        photos=[
            dict(u=_JG + "hero-workshop.webp", alt="Jacky Gearbox workshop in Woodlands", cap="The Woodlands workshop."),
            dict(u=_JG + "gearbox-teardown.webp", alt="Technician rebuilding an automatic gearbox on the teardown bench", cap="An automatic gearbox on the teardown bench."),
            dict(u=_JG + "gearbox-parts.webp", alt="Gearbox clutch packs and gear sets laid out for inspection", cap="Clutch packs and gear sets laid out for inspection."),
            dict(u=_JG + "diagnostics.webp", alt="Laptop running a transmission diagnostic test on a BMW", cap="A transmission diagnostic test running on a BMW."),
            dict(u=_JG + "gearbox-removal.webp", alt="Gearbox being removed from a car on a transmission jack", cap="A gearbox coming out of a car on a transmission jack."),
            dict(u=_JG + "workshop-lifts.webp", alt="Car lifts in the Jacky Gearbox workshop", cap="Lifts in the workshop."),
        ],
        faqs=[
            ("How much does a gearbox repair cost?", "It depends on the car and the fault, so there are no blind quotes. The diagnostic (from S$30) finds the cause, then you get a clear price before the repair starts."),
            ("Can you collect a car that cannot move?", "Yes. Pick-up to the workshop for gearbox repairs is free during office hours, and a tow truck is sent free of charge if the transmission has failed."),
            ("Which cars does Jacky work on?", "Continental, Japanese and Korean cars, plus makes such as Land Rover, Jaguar, Volvo, Ford, Renault, Peugeot and Chevrolet."),
            ("Is there a warranty?", "Repairs carry a standard 6-month warranty unless stated otherwise."),
        ],
        source=dict(name="Page One preview folder preview/dmts index (live domain jackygearbox.com), read via the Bluehost Bridge on 1 Nov 2026",
                    photos="Image paths as used by that page, hotlinked from jackygearbox.com/img/ (not fetchable from this sandbox, CONFIRM they load)"),
        left_out=["customer review quotes (no source or date on the site)", "'15 years combined experience' claim", "any former company name or old email", "rating and review count (not stated)"],
    ),
    dict(
        slug="the-ecu-clinic", tier="premium_leadgen", name="The ECU Clinic", domain="theecuclinicsg.com", url="https://theecuclinicsg.com/",
        category="abs-ecu-module-repair", regions=['east'], regions_note='Kaki Bukit is in the East region (URA). Address: 8 Kaki Bukit Avenue 4.', area_label="Kaki Bukit",
        title="The ECU Clinic | ABS and Module Repair, Kaki Bukit",
        desc="The ECU Clinic in Kaki Bukit repairs ABS pumps and modules, Mercedes gearbox control units and steering locks. 6-month warranty. WhatsApp 9893 1923.",
        card_img=dict(u=_ECU + "mercedes-esp-pumps.webp", alt="Mercedes-Benz ESP pumps on the repair bench"),
        card_text=["Repairs ABS pumps and control modules at a Kaki Bukit workshop.",
                   "Also Mercedes gearbox control units, steering locks and hybrid batteries."],
        lede=("The ECU Clinic repairs car electronics at Premier @ Kaki Bukit. When an ABS or brake warning light will not clear, the unit is tested and repaired on "
              "the bench where possible instead of simply replaced. WhatsApp the car model, chassis number and fault code to 9893 1923, or call."),
        services=[
            dict(n="ABS pump and module repair", d="ABS, ESP and ESC units repaired, or a reconditioned or used unit supplied when that is the better route.", p=None),
            dict(n="Mercedes 7-speed and 9-speed TCU repair", d="Gearbox warnings, harsh shifts or a gear that sticks: the transmission control unit is diagnosed and repaired.", p=None),
            dict(n="Mercedes steering lock (ELV) repair", d="For a key that will not turn or a car that will not start because of the electronic steering lock.", p=None),
            dict(n="Hybrid battery replacement", d="A brand-new OEM hybrid battery, with a warranty of 1 year or 100,000 km.", p=None),
        ],
        price_note="Prices are not listed. Send the fault code and car details by WhatsApp to get the options and a price.",
        phone="+6598931923", phone_show="9893 1923", whatsapp="6598931923",
        addresses=[dict(label=None, street="Premier @ Kaki Bukit, 8 Kaki Bukit Avenue 4, #06-43", postal="415875")],
        map_url="https://www.google.com/maps/search/?api=1&query=Premier%20%40%20Kaki%20Bukit%2C%208%20Kaki%20Bukit%20Avenue%204%2C%20Singapore%20415875",
        hours=[("Mon to Fri", "9am to 7pm"), ("Sat", "9am to 3pm"), ("Sun and public holidays", "Closed")],
        hours_ld=[(WD, "09:00", "19:00"), (SAT, "09:00", "15:00")],
        hours_note="WhatsApp enquiries are welcome at any hour. Pick-up and delivery are available.",
        social=["https://www.facebook.com/TheECUclinicSG"],
        reviews=dict(text="Rated 5.0 on Google from 1 review so far, as stated on theecuclinicsg.com (checked 1 November 2026)", url="https://search.google.com/local/reviews?placeid=ChIJU8-75AAX2jERRmA8PvLfV7k", label="Read the Google reviews"),
        photos=[
            dict(u=_ECU + "mercedes-esp-pumps.webp", alt="Mercedes-Benz ESP pumps on the repair bench", cap="Mercedes-Benz ESP pumps on the bench."),
            dict(u=_ECU + "abs-esc-units-bench.webp", alt="ABS and ESC units on the repair bench", cap="ABS and ESC units waiting for repair."),
            dict(u=_ECU + "mercedes-7g-conductor-plate.webp", alt="Mercedes 7-speed gearbox conductor plate with new filter, gasket and oil", cap="A Mercedes 7-speed gearbox job, with the new filter, gasket and oil."),
            dict(u=_ECU + "mercedes-elv.webp", alt="Mercedes-Benz electronic steering lock on the bench", cap="A Mercedes electronic steering lock on the bench."),
            dict(u=_ECU + "hybrid-battery-modules.webp", alt="Hybrid battery with new modules", cap="A hybrid battery fitted with new modules."),
            dict(u=_ECU + "hyundai-kia-esc.webp", alt="Hyundai or Kia ESC unit on the bench", cap="A Hyundai or Kia ESC unit."),
        ],
        faqs=[
            ("Can you repair my ABS pump or module?", "Yes. ABS, ESP and ESC modules are repaired, and used or reconditioned pumps are supplied for makes such as Toyota, Honda, Mercedes-Benz, Hyundai, Kia, Volkswagen and Audi."),
            ("What should I send on WhatsApp?", "The car model, chassis number and fault code. A photo of the scan tool screen or the dashboard warning helps."),
            ("Is there a warranty?", "Repairs carry a 6-month warranty. New hybrid batteries carry 1 year or 100,000 km."),
            ("Do you collect cars?", "Pick-up and delivery are available, and after-hours appointments can be arranged."),
        ],
        source=dict(name="preview/ecu-clinic index read via the Bluehost Bridge on 1 Nov 2026", photos="jsDelivr URLs used by that page"),
        left_out=["Honda radar, BMW CAS and temperature programming and engine ECU services (kept off the directory)", "customer quotes"],
    ),
    dict(
        slug="wrapstar-autostyle", tier="premium_leadgen", name="Wrapstar Autostyle", domain="wrapstarautostyle.com", url="https://wrapstarautostyle.com/",
        category="car-wrap-ppf", regions=['north'], regions_note='Yishun is in the North region (URA). Address: 9 Yishun Industrial Street 1.', area_label="Yishun",
        title="Wrapstar Autostyle | Car Wrap and PPF, Yishun",
        desc="Wrapstar Autostyle in Yishun: colour wraps from $1,588, colour and clear PPF, window film and dechrome. See past jobs and WhatsApp 9754 1833.",
        card_img=dict(u=_WS + "tesla-model-3-satin-black-rear.webp", alt="Tesla Model 3 in satin black colour PPF at the Wrapstar Autostyle studio"),
        card_text=["Car wrap and film studio at North Spring Bizhub in Yishun.",
                   "Colour wraps from $1,588, PPF, window film and dechrome."],
        lede=("Wrapstar Autostyle is a car wrap and film studio at North Spring Bizhub in Yishun. It changes car colours with vinyl or colour PPF, protects paint "
              "with clear PPF, fits window film and blacks out chrome trims. WhatsApp 9754 1833 with your car model and the look you want."),
        services=[
            dict(n="Colour change wrap", d="A new colour without a respray, in gloss, satin or matte vinyl that can be removed later.", p="From $1,588"),
            dict(n="Colour PPF", d="Thick film in colour: a new look plus protection against stone chips.", p="Priced by car and film"),
            dict(n="Clear PPF", d="An invisible layer over the paint you already have, against chips, swirls and stains.", p="Priced by car and film"),
            dict(n="Window film", d="Solar film to cut cabin heat, fitted to meet LTA rules.", p="Priced by car and film"),
            dict(n="Dechrome", d="Chrome trims and badges turned black for a sportier look.", p="Priced by car and film"),
            dict(n="Ceramic coating and polishing", d="Paint polished first, then coated for gloss and easier washing.", p=None),
        ],
        price_note="The $1,588 is the studio's posted starting price for a full colour wrap. Other jobs are priced by car and film: WhatsApp your model for a quote.",
        phone="+6597541833", phone_show="9754 1833", whatsapp="6597541833",
        addresses=[dict(label=None, street="9 Yishun Industrial Street 1, #01-82, North Spring Bizhub", postal="768163")],
        map_url="https://www.google.com/maps/search/?api=1&query=Wrapstar%20Autostyle%2C%209%20Yishun%20Industrial%20Street%201%20%2301-82%20Singapore%20768163",
        hours=[("Mon to Fri", "9am to 6pm"), ("Sat", "9am to 3pm"), ("Sun", "Closed")],
        hours_ld=[(WD, "09:00", "18:00"), (SAT, "09:00", "15:00")],
        hours_note="WhatsApp before you come down.",
        social=["https://www.facebook.com/wrapstarautostyle", "https://www.instagram.com/wrapstar.autostyle/"],
        reviews=dict(text="100% recommend on Facebook from 24 reviews, as stated on wrapstarautostyle.com (checked 17 October 2026)", url="https://www.facebook.com/wrapstarautostyle/reviews", label="Read the Facebook reviews"),
        photos=[
            dict(u=_WS + "tesla-model-3-satin-black-rear.webp", alt="Tesla Model 3 in satin black colour PPF inside the Wrapstar studio", cap="Tesla Model 3 in satin black colour PPF."),
            dict(u=_WS + "mercedes-c-class-baby-blue-studio.webp", alt="Mercedes-Benz C-Class coupe being wrapped baby blue", cap="Mercedes-Benz C-Class coupe, mid-wrap in baby blue."),
            dict(u=_WS + "byd-sealion-7-matte-green-front.webp", alt="BYD Sealion 7 in matte green", cap="BYD Sealion 7 in matte green."),
            dict(u=_WS + "bmw-m4-stealth-grey-studio.webp", alt="BMW M4 in stealth matte grey under the studio lights", cap="BMW M4 in stealth matte grey."),
            dict(u=_WS + "tesla-model-y-yellow-front.webp", alt="Bright yellow Tesla Model Y", cap="Tesla Model Y in bright yellow."),
            dict(u=_WS + "installer-ppf-bonnet.webp", alt="Installer trimming film on a bonnet edge", cap="Trimming PPF along a bonnet edge."),
        ],
        faqs=[
            ("How much does a car wrap cost?", "The studio's posted starting price for a full colour wrap is $1,588. Colour PPF, clear PPF, window film and dechrome are priced by car and film, so send your model on WhatsApp for a quote."),
            ("Should I pick a vinyl wrap or colour PPF?", "Vinyl is the lower-cost way to change colour. Colour PPF also changes colour and adds protection against stone chips, so it suits owners who want protection as well as looks."),
            ("Which colours can I choose?", "The studio's website shows colours from past jobs, from satin black and matte green to baby blue and bright yellow, and other colours can be sourced on request."),
            ("Where is the studio and when is it open?", "9 Yishun Industrial Street 1, #01-82, North Spring Bizhub, Singapore 768163. Open Monday to Friday 9am to 6pm and Saturday 9am to 3pm, closed Sunday."),
        ],
        source=dict(name="preview/wrapstar index read via the Bluehost Bridge on 1 Nov 2026", photos="jsDelivr URLs used by that page"),
        left_out=["film brands, warranty terms", "customer review quote (rating line only)", "sister business details"],
    ),
    dict(
        slug="battery-rescue-sg", tier="premium_leadgen", name="Battery Rescue SG", domain="batteryrescue.sg", url="https://batteryrescue.sg/",
        category="car-battery", regions=['north', 'north-east', 'west', 'central'], regions_note='Onsite areas on its site: Woodlands, Sembawang, Yishun, Yio Chu Kang (North); Ang Mo Kio, Hougang, Sengkang, Punggol (North-East). Its walk-in Motoserv outlets add Serangoon Garden (North-East), Toa Payoh, Upper Thomson, Bukit Timah, Jervois, Havelock Road (Central) and Bukit Batok, Bukit Panjang, Boon Lay (West). The Sembawang outlet is North.', area_label="Onsite, north and north-east Singapore",
        title="Battery Rescue SG | Onsite Car Battery Replacement",
        desc="Battery Rescue SG fits Delkor car batteries at your car in the north of Singapore, or walk in to 10 Motoserv outlets. Hotline 8125 9169, 24 hours.",
        card_img=dict(u=_BR + "battery-voltage-12-80v.jpg", alt="Battery voltage reading during a battery test"),
        card_text=["Onsite car battery replacement that comes to where your car is stuck.",
                   "Delkor batteries with a one-year warranty, plus jump-start and towing."],
        lede=("Battery Rescue SG replaces car batteries where the car is stuck, so a flat battery does not mean waiting for a tow. Every battery fitted is a Delkor with "
              "a one-year warranty. Call the 24-hour hotline on 8125 9169, or send your location and car model on WhatsApp."),
        services=[
            dict(n="Onsite battery replacement", d="A matching Delkor battery fitted at your car in Woodlands, Sembawang, Yishun, Ang Mo Kio, Yio Chu Kang, Hougang, Sengkang and Punggol.", p="Battery price + $50 (before 10pm), + $80 (10pm to 9am, public holidays)"),
            dict(n="Walk-in replacement at Motoserv outlets", d="Ten outlets, Monday to Saturday 9am to 6pm. A $20 website code takes $20 off the list price, for walk-ins only.", p="Example: NS40ZL $99.90 instead of $119.90"),
            dict(n="Jump-start", d="A jump-start at your car when the battery is flat but may still be good.", p="$50 ($80 on public holidays)"),
            dict(n="Emergency towing", d="Towing when the car cannot be started on the spot. King dolly lifts all four wheels off the ground.", p="From $80, king dolly from $120"),
        ],
        price_note="Prices include the battery, fitting and GST and were checked on 26 October 2026. If the technician attends and the fault is not the battery, an onsite fee of $50 to $80 applies.",
        phone="+6581259169", phone_show="8125 9169", whatsapp="6581259169",
        addresses=[
            dict(label="Motoserv @ Sembawang", street="595 Sembawang Rd", postal=None), dict(label="Motoserv @ Toa Payoh", street="248 Lorong 1 Toa Payoh", postal=None),
            dict(label="Motoserv @ Serangoon Garden", street="49 Serangoon Garden Way", postal="555944"), dict(label="Motoserv @ Upper Thomson", street="553 Upper Thomson Rd", postal="574416"),
            dict(label="Motoserv @ Bukit Batok", street="28 Bukit Batok East Ave 6", postal=None), dict(label="Motoserv @ Bukit Panjang", street="772 Upper Bukit Timah Rd", postal=None),
            dict(label="Motoserv @ Bukit Timah", street="219 Upper Bukit Timah Rd", postal=None), dict(label="Motoserv @ Boon Lay", street="2 Boon Lay Ave", postal=None),
            dict(label="Motoserv @ Jervois", street="2 Jervois Rd", postal="248994"), dict(label="Motoserv @ Havelock Road", street="548 Havelock Rd", postal="169637"),
        ],
        addr_heading="Walk-in outlets (Motoserv)",
        service_area="Onsite service: Woodlands, Sembawang, Yishun, Ang Mo Kio, Yio Chu Kang, Hougang, Sengkang and Punggol.",
        map_url="https://maps.app.goo.gl/VrQtHKzr6Yx2y8Wv5",
        hours=[("Hotline", "24 hours"), ("Onsite fitting", "Any day, 24 hours (night rate 10pm to 9am)"), ("Walk-in outlets", "Mon to Sat, 9am to 6pm")],
        hours_ld=[], hours_note="Sundays and late nights: call and the battery is fitted at your car instead.",
        social=["https://motoserv.sg/"],
        reviews=dict(text="5-star rating on Google, as stated on batteryrescue.sg (rating count not stated; checked 1 November 2026)", url="https://maps.app.goo.gl/VrQtHKzr6Yx2y8Wv5", label="See the Google reviews"),
        photos=[
            dict(u=_BR + "battery-voltage-12-80v.jpg", alt="Battery voltage reading of 12.80 V during a test", cap="A battery test reading 12.80 V."),
            dict(u=_BR + "new-alternator-fitted.jpg", alt="New alternator fitted in an engine bay", cap="A new alternator fitted."),
            dict(u=_BR + "old-alternator.jpg", alt="Old alternator removed from a car", cap="The old alternator that was removed."),
        ],
        faqs=[
            ("Can you come to me if my car will not start?", "Yes, in Woodlands, Sembawang, Yishun, Ang Mo Kio, Yio Chu Kang, Hougang, Sengkang and Punggol. Call the 24-hour hotline or WhatsApp your location and car model."),
            ("Which battery brand do you fit?", "Delkor only, made by Clarios Delkor in Korea. Every battery carries a one-year warranty."),
            ("How is the onsite price worked out?", "It is the battery price plus a $50 onsite fee before 10pm, or plus $80 from 10pm to 9am and on public holidays. Example for an NS40ZL: $169.90 by day, $199.90 at night."),
            ("Where can I walk in?", "At any of 10 Motoserv outlets, Monday to Saturday 9am to 6pm. The $20 website code applies to walk-ins only."),
        ],
        source=dict(name="preview/battery-rescue index and outlets pages, plus FACTS.md, read 1 Nov 2026",
                    contact="WhatsApp on the hotline number is shown on the live preview but FACTS.md still marks it as assumed (CONFIRM)",
                    photos="batteryrescue.sg/photos/ files; captions kept neutral because the site does not say whose job they show"),
        left_out=["Motoserv group name in headline", "promo code value", "CaseTrust wording", "postal codes for 6 outlets"],
    ),
    dict(
        slug="cleanic-detailing", tier="premium_leadgen", name="Cleanic Detailing", domain="cleanicdetailing.com", url="https://cleanicdetailing.com/",
        category="car-detailing-coating", regions=['north', 'north-east', 'east', 'west', 'central'], regions_note='Mobile service. Its site says island-wide and 24/7 across Singapore, so all five regions.', area_label="Mobile service, island-wide",
        title="Cleanic Detailing | Mobile Car Fumigation, Singapore",
        desc="Cleanic Detailing comes to your carpark: car fumigation from $118, steam and interior cleaning from $148, 24/7 island-wide. WhatsApp or call 9108 6931.",
        card_img=dict(u=_CL + "cleanic-panamera-interior-clean2-1024x768.jpg", alt="Cleaned leather interior of a Porsche after a Cleanic job"),
        card_text=["Mobile car fumigation and interior cleaning that comes to you.",
                   "From $118, island-wide, any day of the week."],
        lede=("Cleanic Detailing is a mobile car fumigation and interior cleaning service run by Colin. The work is done where the car is parked, at an HDB, condo or office carpark "
              "across Singapore. Send your car model, location and what you noticed to 9108 6931 and you get advice on the right service before you book."),
        services=[
            dict(n="MIRAKN Express fumigation", d="A short pest-control treatment of about one hour. It does not include steam cleaning.", p="$118"),
            dict(n="Full MIRAKN dry gas fumigation", d="The longer treatment for cockroach and other pest problems, about an hour and a half.", p="From $180"),
            dict(n="Hot dry steam cleaning", d="For stained seats, spills and pet hair. Most full interior jobs take one to two hours.", p="From $148"),
            dict(n="Shampoo scrub cleaning", d="A scrub clean of seats and carpets for dirty or neglected interiors.", p="From $148"),
            dict(n="Odour, damp and mould", d="The source is found first, then the area is cleaned or treated.", p=None),
        ],
        price_note="A small surcharge may apply for multi-storey carparks, condos or landed properties. Final advice comes after you describe the problem.",
        phone="+6591086931", phone_show="9108 6931", whatsapp="6591086931",
        addresses=[], address=None,
        service_area="Mobile service across Singapore. There is no shopfront: the work is done where your car is parked.",
        map_url="https://share.google/h5xraYa2f2jkMRdx7", map_label="Find Cleanic on Google",
        hours=[("Every day", "24 hours, including weekends and public holidays, subject to availability")],
        hours_ld=[], hours_note=None,
        social=["https://www.instagram.com/cleanicdetail/"],
        reviews=dict(text="Rated 5.0 from 400+ Google reviews, as stated on cleanicdetailing.com (checked 1 November 2026)", url="https://share.google/h5xraYa2f2jkMRdx7", label="Read the Google reviews"),
        photos=[
            dict(u=_CL + "cleanic-door-panel.jpg", alt="Specialist steam cleaning a car seat", cap="Steam cleaning a car seat."),
            dict(u=_CL + "cleanic-panamera-interior-clean2-1024x768.jpg", alt="Detailed leather interior after cleaning", cap="A Porsche leather interior after cleaning."),
            dict(u=_CL + "cleanic-panamera-front.jpg", alt="Porsche at a Cleanic mobile detailing job", cap="A Porsche on a mobile job at a carpark."),
            dict(u=_CL + "cleanic-real-mirakn-768x1024.jpg", alt="MIRAKN dry gas fumigation equipment", cap="The MIRAKN dry gas fumigation equipment."),
            dict(u=_CL + "cleanic-real-steam-1024x768.jpg", alt="Steam cleaning equipment packed for mobile work", cap="Steam cleaning equipment used on mobile jobs."),
        ],
        faqs=[
            ("Do you work at night and on weekends?", "Yes, every day including public holidays, subject to availability. It is a 24-hour mobile service."),
            ("How much does car fumigation cost?", "The MIRAKN Express package is $118 and takes about an hour, without steam cleaning. Full MIRAKN dry gas fumigation starts from $180 and takes about an hour and a half."),
            ("How much is interior cleaning and how long does it take?", "Hot dry steam cleaning and shampoo scrub cleaning each start from $148. Most full interior jobs take one to two hours on site."),
            ("Do I need to bring my car to a workshop?", "No. The work is done where the car is parked, at an HDB, condo, office or other accessible location in Singapore."),
        ],
        source=dict(name="cleanicdetailing.com home page read via the Bluehost Bridge on 1 Nov 2026", photos="the site's own /wp-content/uploads/cleanic-photos/ files"),
        left_out=["street address (none: mobile service)", "email address", "customer review quotes (rating line only)", "UEN", "'500+ cars treated' claim"],
    ),
    dict(
        slug="autotex", tier="premium_leadgen", name="Autotex", domain="autotexautoparts.com.sg", url="https://autotexautoparts.com.sg/",
        category="car-parts", regions=['east'], regions_note='Kaki Bukit is in the East region (URA). Address: 1 Kaki Bukit Avenue 6.', area_label="Kaki Bukit",
        title="Autotex | Kia and Hyundai Parts, Kaki Bukit",
        desc="Autotex is a Kia and Hyundai parts shop at AutoBay@Kaki Bukit. Browse parts by model, then ask price and stock on WhatsApp 9731 9547 or call 6747 9618.",
        card_img=None, tile_text="Kia and Hyundai parts",
        card_text=["Kia and Hyundai parts shop in Kaki Bukit.",
                   "Browse parts by model and part type, then ask about price and stock."],
        lede=("Autotex is a parts shop for Kia and Hyundai cars at AutoBay@Kaki Bukit. Pick your model and part on its website, or send your car plate or chassis number "
              "on WhatsApp and the shop checks the exact part for your car before you pay. Collection is at the shop, so message first to have the parts ready."),
        services=[
            dict(n="Body parts and lamps", d="Bumpers, bonnets, grilles, mirrors, wipers, and head, tail and fog lamps.", p=None),
            dict(n="Brake pads and discs", d="Front and rear pad sets, and discs sold in pairs.", p=None),
            dict(n="Suspension and steering", d="Absorbers, arms, links, tie rods and bearings, plus engine and gearbox mounts.", p=None),
            dict(n="Engine and service parts", d="Spark plugs, ignition coils, filters, belts and pumps, plus engine and transmission oil.", p=None),
            dict(n="Cooling, aircon and electrical", d="Radiators, fans, aircon parts, alternators and starter motors.", p=None),
        ],
        price_note="Where the shop's site shows a price it is the price for the part listed. For other parts, ask on WhatsApp for price and stock.",
        phone="+6567479618", phone_show="6747 9618", whatsapp="6597319547", whatsapp_show="9731 9547",
        addresses=[dict(label=None, street="1 Kaki Bukit Avenue 6, #01-42, AutoBay@Kaki Bukit", postal="417883")],
        map_url="https://www.google.com/maps/search/?api=1&query=Autotex+Aircon+Enterprise+1+Kaki+Bukit+Ave+6+%2301-42+Singapore+417883",
        hours=[("Mon to Fri", "9:30am to 5:30pm"), ("Sat", "9:30am to 3:30pm"), ("Sun", "Closed")],
        hours_ld=[(WD, "09:30", "17:30"), (SAT, "09:30", "15:30")],
        hours_note="WhatsApp first so stock can be checked and the parts ready for collection.",
        social=[],
        reviews=dict(text="Rated 5.0 on Google from 4 reviews, as stated on autotexautoparts.com.sg (checked 1 November 2026)", url="https://www.google.com/maps/search/?api=1&query=Autotex+Aircon+Enterprise+1+Kaki+Bukit+Ave+6+%2301-42+Singapore+417883", label="See Autotex on Google Maps"),
        photos=[],
        illustrations=[
            dict(u=_AT + "headlamp.svg", alt="Illustration of a headlamp", cap="Headlamps (illustration)."),
            dict(u=_AT + "front-brake-pads.svg", alt="Illustration of front brake pads", cap="Brake pads (illustration)."),
            dict(u=_AT + "side-mirror.svg", alt="Illustration of a side mirror", cap="Side mirrors (illustration)."),
            dict(u=_AT + "front-bumper.svg", alt="Illustration of a front bumper", cap="Bumpers (illustration)."),
        ],
        faqs=[
            ("Do I need the part number?", "No. Pick your car model and the part, or send your car plate or chassis number on WhatsApp. The shop checks the exact part for your car before you pay."),
            ("Which cars are covered?", "Hyundai and Kia only, for models sold in Singapore such as the Avante, Tucson, Kona, Ioniq, Cerato, Sportage, Sorento, Niro and Picanto. Ask if your model is not listed."),
            ("Where do I collect parts?", "At 1 Kaki Bukit Avenue 6, #01-42, AutoBay@Kaki Bukit, Singapore 417883. Open Monday to Friday 9:30am to 5:30pm and Saturday 9:30am to 3:30pm."),
            ("Is the price on the website final?", "A listed price is for the part shown. For everything else, ask for the price on WhatsApp. Stock and exact fit are confirmed before you pay."),
        ],
        source=dict(name="preview/autotex index read via the Bluehost Bridge on 1 Nov 2026; README (autotex.net is NOT theirs)",
                    photos="No real shop or product photos found on the live site: hero is a clean tile, gallery uses the site's part illustrations (not counted as photos)"),
        left_out=["'direct from Korea' and 'distribution price' wording", "og.jpg card image", "sample part prices", "registered-since claim"],
    ),
]


# ---- Basic (tier "free") listings: card + short profile page. Source: basic-run/2026-11-01.json (public Google business listings, checked 1 Nov 2026).
# Fields shown on the card: name, desc, category, area + region, WhatsApp (only if a mobile number) or Call, Directions (Google Maps cid).
BASIC = [
    dict(slug="everest-garage", place_id="ChIJ6zFftrUX2jERlx4oI_q1cYw", name="Everest Garage", area_label="Kaki Bukit", regions=["east"], category="general-servicing-repair",
         cid="10120069923614498455",
         desc="Car repair and maintenance workshop in Kaki Bukit, on level 5 of 25 Kaki Bukit Road 4.",
         source="Google business listing cid 10120069923614498455, checked 1 Nov 2026"),
    dict(slug="hup-soon-lee-motor-service", place_id="ChIJKcgic4gU2jER-SiN1fV9wY4", name="Hup Soon Lee Motor Service", area_label="Yishun", regions=["north"], category="general-servicing-repair",
         cid="10286641518694181113",
         desc="Long-running car repair workshop in Yishun Industrial Park A that works on private and commercial vehicles, including Euro 4, 5 and 6 models.",
         source="Google business listing cid 10286641518694181113, checked 1 Nov 2026"),
    dict(slug="cys-automobile-services", place_id="ChIJSYwXNWsT2jERZWyiONA8GI4", name="CYS Automobile Services", area_label="Woodlands", regions=["north"], category="general-servicing-repair",
         cid="10239000617827855461",
         desc="Woodlands workshop for servicing and repairs that also handles accident reporting and motor insurance claims.",
         source="Google business listing cid 10239000617827855461, checked 1 Nov 2026"),
    # Added 1 Nov 2026 from details Edwin sent (Google business listings). WhatsApp only where Edwin said the number takes WhatsApp.
    dict(slug="sonic-auto-garage", place_id="ChIJOdFuZBkZ2jERzzREQDSArDQ", name="Sonic Auto Garage", area_label="Ubi", regions=["central"], category="general-servicing-repair",
         cid=None,
         desc="Car servicing and repair workshop in Paya Ubi Industrial Park, with gearbox, aircon, tyre and battery work, plus towing and accident claims.",
         source="Google business listing place_id ChIJOdFuZBkZ2jERzzREQDSArDQ, details from Edwin 1 Nov 2026"),
    dict(slug="allen-motor-workshop", place_id="ChIJjxxlECQX2jERdH2P4TiAez4", name="Allen Motor Workshop", area_label="Sin Ming", regions=["central"], category="general-servicing-repair",
         cid="4502333234277743988",
         desc="Car servicing and repair workshop in Sin Ming Industrial Estate Sector C.",
         source="Google business listing cid 4502333234277743988, details from Edwin 1 Nov 2026"),
    dict(slug="jss-motorworkz", place_id="ChIJeRLlTn4R2jEReZM-FkbmCwE", name="JSS MotorWorkz", area_label="Toh Guan", regions=["west"], category="general-servicing-repair",
         cid="75407007477044089",
         desc="Workshop at Enterprise Hub, Toh Guan, for servicing, engine and gearbox overhauls, diagnostics, aircon and walnut blasting.",
         source="Google business listing cid 75407007477044089, details from Edwin 1 Nov 2026"),
]
# Public facts for Basic listings (address, plain services, wording). Phone, hours, rating and reviews are deliberately NOT stored: they load live from Google Places.
_BX = {
    "everest-garage": dict(
        address_public="25 Kaki Bukit Rd 4, #05-81, Singapore 417800",
        services_public=["Car servicing", "Oil change", "Car aircon", "General repairs"],
        services_source="Google listing category + topics customers mention",
        whatsapp_source="WhatsApp number confirmed through the wa.link on its Google listing, 1 Nov 2026",
        lede=("Everest Garage is a car repair and maintenance workshop in Kaki Bukit, on the fifth floor of 25 Kaki Bukit Road 4. "
              "Its Google listing shows servicing, oil change, aircon and general repairs. Message the workshop on WhatsApp, or tap Directions to find the unit."),
        area_ctx="Kaki Bukit is in the East planning region of Singapore, which also takes in the Bedok car trade units."),
    "hup-soon-lee-motor-service": dict(
        address_public="1018 Yishun Industrial Park A, #01-352, Singapore 768760",
        services_public=["Car repair and servicing", "Private and commercial vehicles", "Euro 4, 5 and 6 vehicles"],
        services_source="Google listing description",
        lede=("Hup Soon Lee Motor Service is a long-running car repair workshop at 1018 Yishun Industrial Park A. "
              "According to its Google listing it works on private and commercial vehicles, including Euro 4, 5 and 6 models. Call to ask about your car."),
        area_ctx="Yishun is in the North planning region of Singapore, alongside Woodlands, Sembawang and Kranji."),
    "cys-automobile-services": dict(
        address_public="38 Woodlands Industrial Park E1, #07-17, Singapore 757700",
        services_public=["Servicing and repair", "Accident reporting", "Motor insurance claims", "Vehicle inspection", "Vehicle rental"],
        services_source="Google listing description",
        lede=("CYS Automobile Services is a servicing and repair workshop on level 7 of 38 Woodlands Industrial Park E1. "
              "Its Google listing also mentions accident reporting, motor insurance claims, vehicle inspection and vehicle rental. Call to ask which of these fits your car."),
        area_ctx="Woodlands is in the North planning region of Singapore, alongside Yishun, Sembawang and Kranji."),
    "sonic-auto-garage": dict(
        address_public="53 Ubi Ave 1, #01-21 Paya Ubi Industrial Park, Singapore 408934",
        services_public=["General servicing and repair", "Brakes", "Diagnostics", "Gearbox", "Car aircon", "Tyres and batteries", "Towing and accident claims"],
        services_source="Google listing, details from Edwin",
        lede=("Sonic Auto Garage is a car servicing and repair workshop at unit #01-21 of Paya Ubi Industrial Park, 53 Ubi Avenue 1. "
              "Its Google listing covers servicing, brakes, diagnostics, gearbox, aircon, tyres and batteries, as well as towing and accident claims. Call to book your car in."),
        area_ctx="Ubi is in the Geylang planning area, part of the Central region of Singapore."),
    "allen-motor-workshop": dict(
        address_public="1 Sin Ming Industrial Estate Sector C, #01-127, Singapore 575636",
        services_public=["Car servicing", "Car repair"],
        services_source="Google listing, details from Edwin",
        lede=("Allen Motor Workshop is a car servicing and repair workshop at unit #01-127, 1 Sin Ming Industrial Estate Sector C. "
              "Call to ask about servicing or a repair for your car, or tap Directions to find the unit."),
        area_ctx="Sin Ming is in the Bishan planning area, part of the Central region of Singapore."),
    "jss-motorworkz": dict(
        address_public="48 Toh Guan Road East, #02-140 Enterprise Hub, Singapore 608586",
        services_public=["Servicing", "Engine repair and overhaul", "Gearbox repair and overhaul", "Diagnostics", "Car aircon", "Walnut blasting", "Tyres and batteries"],
        services_source="Google listing, details from Edwin",
        lede=("JSS MotorWorkz is a workshop on level 2 of Enterprise Hub, 48 Toh Guan Road East. "
              "Its Google listing covers servicing, engine and gearbox repair and overhauls, diagnostics, aircon, walnut blasting, tyres and batteries. Message the workshop on WhatsApp to ask about your car."),
        area_ctx="Toh Guan is in the Jurong East planning area, part of the West region of Singapore."),
}
for _b in BASIC:
    _b.update(_BX[_b["slug"]])
    _b.update(tier="free", services=[], regions_note="Region from the public listing area (URA planning regions).")


def _auto_basic():
    """Basic listings found by basic_agent.py (basic_auto.json). Stored: place_id + name + address + our own estate/slug only.
    Phone, hours, rating, reviews, website and photos are never stored: dir.js loads them live from Google Places in the visitor's browser."""
    import json as _j, os as _os, re as _re
    import areas as _ar
    p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "basic_auto.json")
    if not _os.path.exists(p):
        return []
    out = []
    for r in _j.load(open(p)).values():
        m = _re.search(r"(\d{6})\s*$", r.get("address", ""))
        postal = m.group(1) if m else ""
        street = _re.sub(r",?\s*(?:Singapore\s+)?\d{6}\s*$", "", r["address"])
        es = r.get("estate") or _ar.estate_for(street, postal)
        if not es:
            continue
        en, rg = _ar.ESTATES[es]["name"], _ar.ESTATES[es]["region"]
        out.append(dict(slug=r["slug"], place_id=r["place_id"], name=r["name"], area_label=en, regions=[rg], category="general-servicing-repair", cid=None,
                        desc="Car workshop at " + street + ".", source="Google Places API (New) place_id %s" % r["place_id"],
                        addresses=[dict(label=None, street=street, postal=postal)], address_public=r["address"],
                        services_public=["Car repair and servicing"], services_source="Google listing category",
                        lede="%s is a car workshop at %s. Tap Directions to find the unit, or use the contact button to get in touch." % (r["name"], street),
                        area_ctx="%s is in the %s region of Singapore." % (en, rg.replace("-", " ").title()),
                        tier="free", services=[], regions_note="Region from the public listing area (URA planning regions)."))
    return out


_AUTO = _auto_basic()
BASIC.extend(_AUTO)
ENTRIES.extend(BASIC)
_RANK = {"premium_leadgen": 0, "premium": 1, "free": 2}
ENTRIES.sort(key=lambda e: _RANK[e["tier"]])  # Premium, Verified, Basic (stable within a tier)
