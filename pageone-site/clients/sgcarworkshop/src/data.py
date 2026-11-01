"""Entries for the SG Car Workshop directory (preview). Every fact has a source note in `source`.

Rules (MASTER-RULES 1-4, PLAN.md): verified facts only; if a fact is not in the client's own build files it is left out;
card wording is fresh (never copied from the client's site); no ratings or review schema; no bypass work; no prices
unless confirmed.

kind = "listing": full ~500-word page, the page is the business's website (Wei).
kind = "card":    profile card plus a short profile page that links out to the client's own domain.
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

# area slug -> display name and a one-line fact about where it sits (only things we know from the entries)
AREAS = {
    "yishun": dict(name="Yishun", intro="Car workshops and services in and around Yishun. The workshops below are on Yishun industrial streets, and the battery "
                   "service listed attends cars across the north of Singapore."),
    "woodlands": dict(name="Woodlands", intro="Car workshops and services in Woodlands, including a gearbox workshop at Woodlands Industrial Park and an "
                      "onsite battery service that covers Woodlands."),
    "kaki-bukit": dict(name="Kaki Bukit", intro="Kaki Bukit has a cluster of car trade units. The listings below are a module repair workshop and a Kia and "
                       "Hyundai parts shop, both on Kaki Bukit avenues."),
    "ang-mo-kio": dict(name="Ang Mo Kio", intro="A car workshop in Ang Mo Kio for servicing and repairs, with its own website."),
}

# Photos and card images are stored in src/img (copied to site/assets/img by build.py).
ENTRIES = [
    dict(
        slug="wei-car-spray-painting", kind="listing",
        name="Wei Car Spray Painting", legal="Wei Car Spray Painting Pte. Ltd.", uen="201215981N",
        category="spray-painting-bodywork", areas=["yishun"], area_label="Yishun",
        card_img="wei/jobs-mg-british-racing-green.webp", card_alt="MG sprayed in British Racing Green at Wei Car Spray Painting",
        card_text=["Spray painting and bodywork at a Yishun industrial park workshop.",
                   "Colour changes, full resprays and body kit fitting."],
        services=["Car spray painting (panel respray)", "Full respray and colour change", "Body kit installation and paint"],
        phone="+6596383306", phone_show="9638 3306", whatsapp="6596383306",
        address=dict(street="Blk 1017 Yishun Industrial Park A, #01-242, #01-246 and #01-252", postal="768759", locality="Singapore"),
        map_url="https://www.google.com/maps/search/?api=1&query=Wei%20Car%20Spray%20Painting%2C%201017%20Yishun%20Industrial%20Park%20A%20%2301-242%20Singapore%20768759",
        facebook="https://www.facebook.com/share/19YgRcqvBh/", instagram="https://www.instagram.com/weicarspraypainting/",
        fb_note="100% recommend on Facebook from 238 reviews (checked 1 November 2026)",
        photos=[
            dict(f="wei/shopfront.webp", alt="Wei Car Spray Painting signboard and spray booth at Blk 1017 Yishun Industrial Park A", cap="The workshop and spray booth."),
            dict(f="wei/jobs-mg-british-racing-green.webp", alt="MG after an exterior respray in British Racing Green", cap="MG exterior respray in British Racing Green, November 2023."),
            dict(f="wei/jobs-honda-civic-grey-blue.webp", alt="Honda Civic after a full respray with a gloss black roof and a new spoiler", cap="Honda Civic: full respray, gloss black roof and a new spoiler, November 2023."),
            dict(f="wei/jobs-mini-cooper-pink.webp", alt="Mini Cooper after a colour change to pink", cap="Mini Cooper colour change from orange to pink, May 2022."),
            dict(f="wei/jobs-porsche-cayenne-bodykit-front.webp", alt="Porsche Cayenne with a new-model body kit installed", cap="Porsche Cayenne with a new-model body kit imported from overseas, February 2026."),
        ],
        og_img="wei/og.jpg",
        source=dict(
            name="ACRA (via acrawatch.sg / recordowl.com, data.gov.sg): WEI CAR SPRAY PAINTING PTE. LTD., UEN 201215981N, inc. 28 Jun 2012; SSIC 95301 repair and maintenance of motor vehicles",
            address="ACRA registered address + Facebook page (screenshot 1 Nov 2026): Blk 1017 Yishun Industrial Park A #01-242/246/252, S768759",
            phone="Facebook page and own poster (8 Apr 2026): 9638 3306 (WhatsApp Now)",
            jobs="Facebook posts (screenshots from Edwin, 1 Nov 2026): Macan May 2025, MG Nov 2023, Civic Nov 2023, Mini May 2022, Cayenne Feb 2026",
            shopfront="sgCarmart listing photo (8 Sep 2022): signboard and spray booth",
            fb_note="Facebook page screenshot 1 Nov 2026 (plain text only, no rating schema)"),
        left_out=["opening hours (2022 sgCarmart listing only, unconfirmed)", "all prices incl. the expired $888 respray offer",
                  "scratch, dent, bumper repair, servicing and insurance-claim services (in-house/current status unconfirmed)",
                  "paint brands (Aiika / Spies Hecker)", "owner name", "second phone 6759 3229 (2022 listing)"],
    ),
    dict(
        slug="sg-garage", kind="card", name="SG Garage", domain="sggarage.com", url="https://sggarage.com/",
        category="general-servicing-repair", areas=["ang-mo-kio"], area_label="Ang Mo Kio",
        card_img="cards/sggarage.webp", card_alt="Screenshot of the SG Garage website",
        card_text=["A car workshop in Ang Mo Kio for everyday servicing and repairs.",
                   "Battery and alternator checks, aircon work and more, with the price confirmed after inspection."],
        services=["Battery and charging system checks", "Alternator replacement", "Car aircon repair"],
        phone=None, whatsapp=None,
        profile=("SG Garage is a car workshop in Ang Mo Kio that handles everyday servicing and repairs. Its recent work includes alternator "
                 "replacements, where the team first checks the battery voltage with a multimeter so that a weak battery is not mistaken for a "
                 "charging fault. It also works on car aircon. The workshop belongs to the founder of Page One Singapore, who built this "
                 "directory, so we say so openly. Full service details and ways to book are on the workshop's own website, one tap away."),
        source=dict(
            name="Page One clients page (1 Nov 2026): sggarage.com, Edwin Garage, car workshop, Ang Mo Kio (the Google profile name)",
            services="sggarage/alternator-job-2026-10-27.md (battery voltage check, alternator replacement at the Ang Mo Kio workshop); Page One text: ranks for 'car aircon repair'",
            founder="Watchdog portfolio spec: founder's own workshop, keep the disclosure"),
        left_out=["phone/WhatsApp (not in the files available)", "hours, prices, address, ratings and review counts (three conflicting counts in the old audit)"],
    ),
    dict(
        slug="jacky-gearbox", kind="card", name="Jacky Gearbox", domain="jackygearbox.com", url="https://jackygearbox.com/",
        category="gearbox-repair", areas=["woodlands"], area_label="Woodlands",
        card_img="cards/jackygearbox.webp", card_alt="Screenshot of the Jacky Gearbox website",
        card_text=["Gearbox specialist working from Woodlands, with a second workshop at Kranji.",
                   "Diagnosis, repair, servicing and upgrades, explained in plain words."],
        services=["Gearbox diagnostic and repair", "Gearbox upgrades", "Gearbox (ATF) servicing", "Free towing"],
        phone="+6584309665", phone_show="8430 9665", whatsapp="6584309665",
        profile=("Jacky Gearbox is a gearbox and transmission specialist in Woodlands, with a second workshop in Kranji. Jacky diagnoses the gearbox himself "
                 "and explains the fault before any work starts. The pre-repair diagnostic starts from S$30, repairs carry a standard six-month warranty "
                 "unless stated otherwise, and free towing is offered. Guides on slipping gears, jerking shifts and warning lights are on the workshop's own "
                 "website, along with details for both locations. A second opinion on a gearbox quote is welcome too, so bring the quote you already have."),
        extra_address="Woodlands: 71 Woodlands Industrial Park E9, #01-25 Wave 9, Singapore 757048. Kranji: 60 Jalan Lam Huat, #05-48, Singapore 737869.",
        source=dict(
            name="Page One clients page (live 13-14 Oct 2026); dmts folder google-business-profile.md",
            contact="dmts README (confirmed 11 Oct 2026): WhatsApp/mobile 8430 9665; GBP draft: only number on the site",
            claims="dmts README: pre-repair diagnostic from S$30, standard 6-month warranty unless otherwise stated; GBP draft: free towing, Woodlands HQ and Kranji branch addresses"),
        left_out=["opening hours (differ between drafts)", "'15 years combined experience' claim", "any former company name"],
    ),
    dict(
        slug="the-ecu-clinic", kind="card", name="The ECU Clinic", domain="theecuclinicsg.com", url="https://theecuclinicsg.com/",
        category="abs-ecu-module-repair", areas=["kaki-bukit"], area_label="Kaki Bukit",
        card_img="cards/theecuclinicsg.webp", card_alt="Screenshot of The ECU Clinic website",
        card_text=["Repairs ABS pumps and control modules at a Kaki Bukit workshop.",
                   "Also Mercedes gearbox control units, steering locks and hybrid batteries."],
        services=["ABS pump and module repair", "Mercedes 7G/9G gearbox control unit (TCU) repair", "Mercedes steering lock (ELV) diagnosis and repair", "New OEM hybrid battery replacement"],
        phone="+6598931923", phone_show="9893 1923", whatsapp="6598931923",
        profile=("The ECU Clinic repairs car electronics at Premier @ Kaki Bukit. The main work is ABS pumps and brake modules: when the ABS or "
                 "stability warning light stays on, the team tests the unit and repairs it on the bench instead of simply replacing it. It also "
                 "handles Mercedes 7-speed and 9-speed gearbox control units, Mercedes steering lock faults and new hybrid battery replacement. "
                 "Repairs carry a six-month warranty. Send the car model and symptoms by WhatsApp, or read the fault guides on the workshop's website."),
        extra_address="Premier @ Kaki Bukit, 8 Kaki Bukit Avenue 4, #06-43, Singapore 415875.",
        source=dict(
            name="Page One clients page (live Oct 2026); ecu-clinic README on branch claude/ecu-night-31-oct (confirmed with Edwin)",
            contact="ecu-clinic README: WhatsApp 9893 1923, address Premier @ Kaki Bukit #06-43, 6-month warranty",
            services="ecu-clinic build.py service cards (13 Oct 2026 refocus) and Page One clients page (5 service pages)"),
        left_out=["opening hours (README and build.py disagree)", "any bypass, delete or coding work", "Honda radar and engine ECU cards"],
    ),
    dict(
        slug="wrapstar-autostyle", kind="card", name="Wrapstar Autostyle", domain="wrapstarautostyle.com", url="https://wrapstarautostyle.com/",
        category="car-wrap-ppf", areas=["yishun"], area_label="Yishun",
        card_img="cards/wrapstarautostyle.webp", card_alt="Screenshot of the Wrapstar Autostyle website",
        card_text=["Car wrap studio in Yishun with a colour catalogue and past jobs to browse.",
                   "Colour wraps, paint protection film, window film and dechrome."],
        services=["Colour change wraps", "Paint protection film (PPF), clear and colour", "Window film", "Dechrome"],
        phone="+6597541833", phone_show="9754 1833", whatsapp="6597541833",
        profile=("Wrapstar Autostyle is a car wrap studio at North Spring Bizhub in Yishun. It offers colour change wraps, paint protection film in "
                 "clear or colour, window film and dechrome. The studio's own website has a colour catalogue and a gallery of past jobs grouped by colour, "
                 "which is the quickest way to see what a finish looks like on a real car. Message the studio on WhatsApp with your car model and the look "
                 "you want. Check LTA rules before changing your car's colour."),
        extra_address="9 Yishun Industrial Street 1, #01-82, North Spring Bizhub, Singapore 768163.",
        source=dict(
            name="wrapstar README (live 18 Oct 2026); Page One clients page",
            contact="wrapstar README: WhatsApp +65 9754 1833, 9 Yishun Industrial Street 1 #01-82 North Spring Bizhub S768163",
            services="Page One clients page: colour wraps, colour and clear PPF, window film, dechrome; colour catalogue and past works"),
        left_out=["hours, film brands, warranty, Google rating (README: not claimed)", "dated prices"],
    ),
    dict(
        slug="battery-rescue-sg", kind="card", name="Battery Rescue SG", domain="batteryrescue.sg", url="https://batteryrescue.sg/",
        category="car-battery", areas=["yishun", "woodlands"], area_label="Onsite, north and north-east Singapore",
        card_img="cards/batteryrescue.webp", card_alt="Screenshot of the Battery Rescue SG website",
        card_text=["Onsite car battery replacement that comes to where your car is stuck.",
                   "Delkor batteries with a one-year warranty, plus jump-start and towing."],
        services=["Onsite car battery replacement", "Delkor batteries, one-year warranty", "Jump-start", "Emergency towing"],
        phone="+6581259169", phone_show="8125 9169", whatsapp=None,
        profile=("Battery Rescue SG replaces car batteries onsite, so a flat battery does not mean waiting for a tow. Every battery fitted is a Delkor "
                 "with a one-year warranty, and the website has a finder where you pick your car to see the matching battery. The rescue service covers "
                 "Woodlands, Sembawang, Yishun, Punggol, Sengkang, Ang Mo Kio, Yio Chu Kang and Hougang. Jump-start and emergency towing are also "
                 "offered. Call the 24-hour hotline, or open the website for the battery finder and outlets."),
        source=dict(
            name="battery-rescue/FACTS.md (26 Oct 2026); Page One clients page (live 27 Oct 2026)",
            contact="FACTS.md: 24-hour hotline 8125 9169 (WhatsApp on the same number is only assumed, so no WhatsApp button here)",
            services="FACTS.md: Delkor only, 1 year warranty confirmed, rescue areas, jump-start and towing services"),
        left_out=["all prices and the website promo code (change often)", "WhatsApp number (assumed, not confirmed)", "CaseTrust wording (entity unconfirmed)"],
    ),
    dict(
        slug="cleanic-detailing", kind="card", name="Cleanic Detailing", domain="cleanicdetailing.com", url="https://cleanicdetailing.com/",
        category="car-detailing-coating", areas=[], area_label="Mobile service",
        card_img="cards/cleanic.webp", card_alt="Screenshot of the Cleanic Detailing website",
        card_text=["Mobile car grooming that comes to you.",
                   "Steam cleaning, fumigation and odour removal for the car interior."],
        services=["Car grooming", "Steam cleaning", "Fumigation", "Odour removal"],
        phone=None, whatsapp=None,
        profile=("Cleanic Detailing is a mobile car grooming and fumigation service in Singapore. Its website has a page for each job, "
                 "covering grooming, steam cleaning, fumigation and odour removal, plus guides on the problems drivers search for, such as smells "
                 "that will not go away. Because the service is mobile, the website is the place to check what is offered and how to get in touch. "
                 "It suits drivers who would rather the work came to them than spend time at a workshop. Browse the service pages to see which problem matches yours, then tap the button below to visit the website."),
        source=dict(
            name="Page One clients page (1 Nov 2026): Cleanic Detailing, mobile car grooming and fumigation, live since Jun 2026",
            services="Page One clients page: service pages for grooming, steam cleaning, fumigation and odour removal (no cleanic folder in project files)"),
        left_out=["phone/WhatsApp, address, hours, prices (no cleanic build files available)", "owner name"],
    ),
    dict(
        slug="autotex", kind="card", name="Autotex", domain="autotexautoparts.com.sg", url="https://autotexautoparts.com.sg/",
        category="car-parts", areas=["kaki-bukit"], area_label="Kaki Bukit",
        card_img="cards/autotexautoparts.webp", card_alt="Screenshot of the Autotex Kia and Hyundai parts website",
        card_text=["Kia and Hyundai parts shop in Kaki Bukit.",
                   "Browse parts by model and part type, then ask about price and stock."],
        services=["Kia parts", "Hyundai parts", "Browse by model and part type"],
        phone="+6567479618", phone_show="6747 9618", whatsapp="6597319547",
        profile=("Autotex is a parts shop for Kia and Hyundai cars at AutoBay@Kaki Bukit. Its website lets you browse by car model and part type and "
                 "send a parts enquiry on WhatsApp. If you drive a Kia or Hyundai, it is a quick way to see what the shop carries before you head down. "
                 "Ask about price and stock when you enquire, since those are confirmed by the shop. Bring your car model and, if you can, a photo of the old part so the right one is matched. Phone and WhatsApp details are below, together with the address."),
        extra_address="1 Kaki Bukit Avenue 6, #01-42, AutoBay@Kaki Bukit, Singapore 417883.",
        source=dict(
            name="autotex/README.md: Autotex Aircon Enterprise, Kia and Hyundai parts shop",
            contact="README: 1 Kaki Bukit Ave 6 #01-42 AutoBay@Kaki Bukit S417883, tel 6747 9618, WhatsApp +65 9731 9547",
            warning="README: autotex.net is NOT theirs, never linked"),
        left_out=["all product prices and part numbers (sample data in README)", "'direct from Korea', 'distribution price', genuine/OEM wording (unconfirmed)", "Google 5.0 rating", "hours"],
    ),
]
