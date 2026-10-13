"""Service pages and articles for The ECU Clinic (added 13 Oct 2026, Edwin's standing rule: one page per
specialised service plus an articles section for long-tail searches).

Client facts come only from source/content.md. Articles add general, widely documented car knowledge
in hedged wording ("can", "often"), with no prices, no model-specific failure claims and no promises.
Body text is HTML; {wa} is replaced with the WhatsApp link by build.py.
"""

# slug, short name, title tag, meta description, h1, lead, photo (web name), photo alt, share photo (source jpg),
# intro paragraphs, what we do (ticks), signs (title, text), faq [(q, a)], related article slugs
SERVICE_PAGES = [
    dict(
        slug='abs-pump-repair', key='abs', name='ABS Pump & Module Repair',
        title='ABS Pump Repair Singapore | ABS Module Repair | The ECU Clinic',
        desc='ABS pump and ABS module repair in Kaki Bukit. ABS, ESP and ESC units, used and recon pumps, Toyota Voxy, Noah and Sienta. 6-month warranty. WhatsApp 9893 1923.',
        h1='ABS Pump & ABS Module Repair in Singapore',
        lead='ABS, ESP or ESC warning light on? We find the fault, then repair your pump or module, or supply a used or reconditioned unit.',
        photo='abs-esc-units-bench', alt='ABS and ESC units on the repair bench at The ECU Clinic',
        share='abs-esc-units-on-bench.jpg',
        intro=['ABS pumps and modules are our main work. The ABS unit sits in the engine bay and combines a hydraulic pump with an electronic control module. When the module or pump develops a fault, the ABS warning light comes on, and on many cars the ESP or traction control light comes on with it.',
               'We start with the fault code, so we know whether the problem is the unit itself or something around it, such as a sensor or wiring. Then we tell you the options: repair your unit, or fit a reconditioned, used or new one.',
               'Many car workshops send their ABS and module repairs to us. Come direct and deal with the technician who does the repair.'],
        what=['ABS, ESP and ESC module repair', 'Used and reconditioned ABS pumps', 'Mercedes-Benz ESP units',
              'Hyundai and Kia ESC units', 'Toyota Voxy, Noah and Sienta: repair, replace, used or recon',
              'Plug and play available', 'Makes include Audi, VW, BMW, Chevrolet, Honda, Mercedes, Nissan, Toyota, Skoda, Mini, Kia and Volvo'],
        signs=[('ABS light stays on', 'The ABS warning light comes on and stays on after the car is restarted.'),
               ('ESP or traction light too', 'ESP, ESC or traction control warnings appear together with the ABS light.'),
               ('Brake system message', 'The dashboard shows a brake system or brake assist message.'),
               ('Fault code points to the module', 'A scan shows a code for the ABS control module or pump motor.')],
        faq=[('Can you repair my ABS pump or module?', 'Yes. We repair ABS, ESP and ESC modules and supply used and reconditioned ABS pumps for makes such as Toyota, Honda, Mercedes-Benz, Hyundai, Kia, Volkswagen, Audi, Nissan, Volvo and Chevrolet.'),
             ('Do you do Toyota Voxy, Noah and Sienta ABS pumps?', 'Yes. We repair, replace or supply used and recon ABS pumps and modules for the Toyota Voxy, Noah and Sienta, with plug and play available.'),
             ('Is there a warranty?', 'Yes. Our repairs come with a 6-month warranty.'),
             ('What should I send you?', 'Your car model, chassis number and the fault code. A photo of the scan tool screen or the warning light also helps.'),
             ('Is it safe to drive with the ABS light on?', 'In most cases your normal brakes still work, but the anti-lock function may be off until the fault is fixed, so the wheels can lock under hard braking, especially on wet roads. If the red brake warning light is on too, or the pedal feels different, stop driving and get the car checked.'),
             ('Can I bring in just the ABS unit?', 'Yes. You can bring the car or the part to us at Premier @ Kaki Bukit, or use our pick-up and delivery service.')],
        # EDGE Loop, 13 Oct 2026 (owner page for "abs pump repair singapore" and "abs module repair singapore").
        # The Singapore top 10 (Carousell listings, workshop pages, a V-Tec product page) mostly skip these:
        # driving with the light on, how sensor vs unit is told apart, and a plain comparison of the options.
        updated='13 Oct 2026',
        jobs=[('mercedes-esp-pumps', 'Mercedes-Benz ESP pumps on our bench'), ('hyundai-kia-esc', 'Hyundai / Kia ESC unit'),
              ('abs-pump-in-car', 'ABS pump in the engine bay'), ('abs-module-in-car', 'ABS module in a car’s engine bay')],
        more=[('Is it safe to drive with the ABS light on?',
               '<p>In most cases your normal brakes still work, but the anti-lock function may be switched off until the fault is fixed. That means the wheels can lock under hard braking, especially on wet roads, so leave more distance and avoid hard stops.</p>'
               '<p>If the red brake warning light comes on together with the ABS light, or the brake pedal feels different, stop driving and get the car checked first. Our pick-up and delivery service can collect it. More in our guide: <a href="{u}articles/abs-warning-light-causes/">ABS warning light causes</a>.</p>'),
              ('Sensor, wiring, pump or module: how we find the fault',
               '<ol class="steps"><li><strong>Read the fault code.</strong> The ABS control module stores a code that points to the circuit at fault.</li>'
               '<li><strong>Rule out the simple causes.</strong> Wheel speed sensors, their wiring and connectors, brake fluid level and fuses.</li>'
               '<li><strong>Check the unit itself.</strong> If the code and tests point to the pump motor or the module, the ABS unit is the problem.</li>'
               '<li><strong>Tell you the options.</strong> You decide before any work starts.</li></ol>'
               '<p>This order matters: the same warning light can come from a wheel speed sensor or from the ABS unit, and replacing parts without the code can mean paying for parts you did not need.</p>'),
              ('Your options: repair, recon, used or new',
               '<div class="grid g2">'
               '<div class="card"><h3>Repair your unit</h3><p>We repair the fault in your own ABS pump or module, down to the circuit board where we can.</p></div>'
               '<div class="card"><h3>Reconditioned unit</h3><p>A rebuilt ABS pump, for when repairing your own unit is not the right fix.</p></div>'
               '<div class="card"><h3>Used unit</h3><p>A used ABS pump for the same model, for example the Toyota Voxy, Noah and Sienta.</p></div>'
               '<div class="card"><h3>New unit</h3><p>A new part, where that is the right fix for your car.</p></div>'
               '</div>'
               '<p style="margin-top:16px">Plug and play is available. We explain the options before any work starts, and our repairs come with a 6-month warranty.</p>')],
        visit=True,
        related=['abs-warning-light-causes', 'toyota-voxy-noah-sienta-abs-pump', 'mercedes-active-brake-assist-functions-limited'],
    ),
    dict(
        slug='mercedes-7g-9g-tcu-repair', key='tcu', name='Mercedes 7G & 9G TCU Repair',
        title='Mercedes 7G-Tronic 722.9 TCU & Conductor Plate Repair Singapore | The ECU Clinic',
        desc='Mercedes 7G-Tronic (722.9) TCU and conductor plate repair, done locally in Kaki Bukit: fault codes read first, new filter, gasket and oil on the same job. 9G-Tronic TCU too.',
        h1='Mercedes 7-Speed & 9-Speed TCU Repair',
        lead='Gearbox warning, harsh shifts or stuck in one gear? We diagnose and repair the transmission control unit (TCU) on Mercedes 7G-Tronic and 9G-Tronic automatics.',
        photo='mercedes-7g-conductor-plate', alt='Mercedes 722.9 conductor plate with new filter, pan gasket and gearbox oil',
        share='mercedes-722-9-conductor-plate-kit.jpg',
        intro=['On the Mercedes 7-speed automatic (7G-Tronic, gearbox code 722.9), the transmission control unit sits inside the gearbox, on the conductor plate of the valve body. Because it lives in hot gearbox oil, faults in this unit can cause gear changes to go wrong even when the mechanical parts of the gearbox are fine.',
               'We read the fault codes first, then work on the TCU and conductor plate. When the gearbox pan is off, we fit a new filter, pan gasket and gearbox oil on the same job. We also work on the TCU of the 9-speed 9G-Tronic.'],
        what=['7G-Tronic (722.9) TCU and conductor plate', '9G-Tronic TCU', 'Fault code reading and diagnosis',
              'New filter, pan gasket and gearbox oil fitted on the same job'],
        signs=[('Gearbox warning', 'A transmission warning or message appears on the dashboard.'),
               ('Limp mode', 'The car stays in one gear and will not shift up.'),
               ('Harsh or late shifts', 'Gear changes feel rough, jerky or delayed.'),
               ('Gear display problems', 'The gear indicator flashes, is blank, or shows the wrong gear.')],
        faq=[('Which Mercedes gearboxes do you work on?', 'The 7-speed 7G-Tronic (722.9) and the 9-speed 9G-Tronic. Send us the car model, chassis number and fault code to check.'),
             ('Do you change the gearbox oil too?', 'Yes. When we work on the conductor plate we fit a new filter, pan gasket and gearbox oil on the same job.'),
             ('Do I have to remove and post the unit myself?', 'No. We read the fault codes and do the TCU and conductor plate work at our workshop in Kaki Bukit. If the car is stuck in limp mode, pick-up and delivery service is available.'),
             ('Can I keep driving in limp mode?', 'Limp mode is meant to get the car home or to a workshop, not for daily driving. The longer the gearbox runs with a fault, the more can go wrong, so get it checked soon.'),
             ('Is there a warranty?', 'Yes. Our repairs come with a 6-month warranty.')],
        # EDGE Loop, 13 Oct 2026 (owner page for "mercedes 722.9 tcu repair singapore" / "7g tronic conductor plate").
        # The top results are overseas mail-in services and eBay listings priced in USD, with no local option.
        updated='13 Oct 2026',
        more=[('Repaired here in Singapore, not posted overseas',
               '<p>Many of the 722.9 conductor plate repair services you will find online are mail-in services abroad: you remove the unit, ship it overseas and wait for it to come back. '
               'With us, the fault codes are read, the TCU and conductor plate work is done, and the new filter, pan gasket and gearbox oil are fitted, all at our workshop at Premier @ Kaki Bukit.</p>'),
              ('What the conductor plate does',
               '<p>On the 7G-Tronic, the transmission control unit is built onto the conductor plate, which sits on the valve body inside the gearbox and also carries the gearbox speed sensors. '
               'Because it lives in hot gearbox oil, its electronics and sensors can develop faults over the years. A speed sensor or TCU fault can put the gearbox into limp mode even when the gears and clutches are fine, which is why we read the codes before anything is opened.</p>'
               '<p>More in our guide: <a href="{u}articles/mercedes-7g-tronic-722-9-tcu-problems/">Mercedes 7G-Tronic (722.9) TCU problems</a>.</p>')],
        visit=True,
        related=['mercedes-7g-tronic-722-9-tcu-problems', 'mercedes-active-brake-assist-functions-limited'],
    ),
    dict(
        slug='mercedes-steering-lock-elv-repair', key='elv', name='Mercedes Steering Lock (ELV) Repair',
        title='Mercedes Steering Lock (ELV/ESL) Repair Singapore | The ECU Clinic',
        desc='Key won’t turn or Mercedes won’t start? We test and repair the electronic steering lock (ELV/ESL) in Kaki Bukit. Pick-up if your car can’t be driven. 6-month warranty.',
        h1='Mercedes Steering Lock (ELV) Repair',
        lead='Key won’t turn, or the car won’t start because of the steering lock? We diagnose and repair the electronic steering lock (ELV) on Mercedes-Benz.',
        photo='mercedes-elv', alt='Mercedes-Benz electronic steering lock (ELV) on the bench',
        share='mercedes-elv-steering-lock.jpg',
        intro=['Many Mercedes-Benz models use an electronic steering lock, often called the ELV or ESL. It is a small motorised unit on the steering column that locks the steering when the car is off and unlocks it when the key is turned or the start button is pressed.',
               'If the ELV does not unlock, the car cannot start. We test the unit, repair it, and get your car driving again. WhatsApp us your model and what the car is doing, and we will tell you what we can do.'],
        what=['Mercedes-Benz ELV diagnosis', 'Steering lock repair', 'Pick-up and delivery available'],
        signs=[('Key won’t turn', 'The key goes in but will not turn in the ignition.'),
               ('No start, no crank', 'Nothing happens when you try to start the car.'),
               ('Steering stays locked', 'The steering wheel stays locked after you switch on.'),
               ('Works sometimes', 'The car starts on some tries and not on others.')],
        faq=[('Do you repair Mercedes steering locks?', 'Yes. We repair the electronic steering lock (ELV) on Mercedes-Benz cars. WhatsApp us your model and what the car is doing.'),
             ('My car won’t start. Can you collect it?', 'Pick-up and delivery service is available. WhatsApp us your location.'),
             ('Is it the steering lock, or just the key or battery?', 'A flat key battery, a weak car battery or an ignition switch fault can look like a steering lock fault, so we rule those out first. Then we test the steering lock itself.'),
             ('It still starts sometimes. Can I wait?', 'A steering lock that works on some tries and not others often gets worse over time, and when it stops unlocking the car will not start at all. Get it checked before it leaves you stranded.'),
             ('Is there a warranty?', 'Yes. Our repairs come with a 6-month warranty.')],
        # EDGE Loop, 14 Oct 2026 (owner page for "mercedes steering lock repair singapore" / "mercedes elv repair").
        # The top results are overseas: US DIY guides and dealer quotes in USD, eBay parts and tool listings, a South
        # African mobile mechanic. None is a Singapore workshop, none says how to tell the lock from a key or battery
        # fault, and none deals with the car that cannot be driven to a workshop.
        updated='14 Oct 2026',
        jobs=[('mercedes-elv', 'Mercedes ignition switch and key on our test bench'), ('elv-units', 'Steering lock parts on our bench')],
        more=[('Steering lock, key or battery: what we check first',
               '<ol class="steps"><li><strong>The simple causes.</strong> A flat key battery, a weak car battery or an ignition switch fault can look just like a steering lock fault.</li>'
               '<li><strong>The fault codes.</strong> The car’s control units store codes that show whether they can talk to the steering lock.</li>'
               '<li><strong>The steering lock itself.</strong> We test the unit to confirm it is the part that is failing.</li>'
               '<li><strong>Your options.</strong> We tell you what we can do before any work starts.</li></ol>'
               '<p>More in our guide: <a href="{u}articles/mercedes-steering-lock-elv-failure/">Mercedes steering lock (ELV) failure: signs and repair</a>.</p>'),
              ('Car stuck and won’t start? We can collect it',
               '<p>When the steering lock fails, the car usually cannot be driven to a workshop. Our pick-up and delivery service can collect it. '
               'WhatsApp us your car model, your location and what the car is doing: for example, the key will not turn, nothing happens when you press start, or a message appears on the dashboard. '
               'WhatsApp enquiries are welcome 24/7.</p>'),
              ('Repaired here in Singapore',
               '<p>Most of what you will find online about Mercedes steering lock faults is written for drivers abroad: do-it-yourself guides, parts and tools posted from overseas, and dealer quotes in US dollars. '
               'With us, the testing and repair are done at our workshop at Premier @ Kaki Bukit, and our repairs come with a 6-month warranty.</p>')],
        steps=[('WhatsApp us the details', 'Send your car model and what the car is doing to <a href="{wa}" target="_blank" rel="noopener">9893 1923</a>. If you have a fault code, send that too.'),
               ('We check and advise', 'We rule out the key and battery, test the steering lock, and tell you what we can do before any work starts.'),
               ('Drop off or pick-up', 'Bring the car to us at Premier @ Kaki Bukit. If it cannot be driven, use our pick-up and delivery service.'),
               ('Fixed, with warranty', 'Your car is back on the road, and the repair comes with a 6-month warranty.')],
        band=('Mercedes won’t start?', 'WhatsApp us your car model and what the car is doing. If it can’t be driven, we can collect it.'),
        visit=True,
        related=['mercedes-steering-lock-elv-failure'],
    ),
    dict(
        slug='hybrid-battery-replacement', key='hybrid', name='Hybrid Battery Replacement',
        title='Hybrid Battery Replacement Singapore | Brand-New OEM | The ECU Clinic',
        desc='Brand-new OEM hybrid battery replacement in Kaki Bukit, with a warranty of 1 year or 100,000 km. WhatsApp your car model and year: 9893 1923.',
        h1='Hybrid Battery Replacement in Singapore',
        lead='Hybrid battery warning or a weak battery? We replace it with a brand-new OEM hybrid battery, with a warranty of 1 year or 100,000 km.',
        photo='hybrid-battery-pack', alt='Brand-new hybrid battery pack ready to fit',
        share='hybrid-battery-pack-1.jpg',
        intro=['A hybrid car has a high-voltage battery pack that stores energy for the electric motor. As the pack ages, it holds less charge, and the car relies more on the engine. In time the hybrid system warning light can come on.',
               'We replace the pack with a brand-new OEM hybrid battery, and we do the removal and fitting. WhatsApp us your car model and year, and we will check availability and price.'],
        what=['Brand-new OEM hybrid batteries', 'Warranty: 1 year or 100,000 km', 'Removal and fitting',
              'WhatsApp us your car model and year to check availability'],
        signs=[('Hybrid warning light', 'A hybrid system warning appears on the dashboard.'),
               ('Fuel use goes up', 'The car uses more petrol than it used to.'),
               ('Engine runs more often', 'The engine starts more often, even at low speed.'),
               ('Battery gauge jumps', 'The battery level drops or rises quickly.')],
        faq=[('What hybrid batteries do you fit?', 'Brand-new OEM hybrid batteries, with a warranty of 1 year or 100,000 km.'),
             ('Is the battery new or reconditioned?', 'Brand-new OEM. The warranty is 1 year or 100,000 km.'),
             ('Can I drive with the hybrid warning light on?', 'The car may still drive, but get it checked soon. A weak pack makes the engine work harder, and some cars reduce power to protect the system. WhatsApp us the fault code and your car model.'),
             ('How do I get a price?', 'WhatsApp us your car model and year. We will check availability and price.')],
        # EDGE Loop, 13 Oct 2026 (owner page for "hybrid battery replacement singapore"). The top 10 often leave
        # unclear whether a pack is new or reconditioned, and one shows three different warranties on one page.
        updated='13 Oct 2026',
        jobs=[('hybrid-battery-pack', 'Brand-new hybrid battery pack ready to fit'), ('hybrid-battery-side', 'Brand-new hybrid battery pack')],
        more=[('New, reconditioned or repaired: know what you are buying',
               '<p>When you shop for a hybrid battery in Singapore you will be offered different things under the same name. Ask which one it is, and what the warranty covers:</p>'
               '<div class="grid g3">'
               '<div class="card"><h3>Brand-new OEM pack</h3><p>A new pack made for your car. This is what we fit, with a warranty of 1 year or 100,000 km.</p></div>'
               '<div class="card"><h3>Reconditioned pack</h3><p>A used pack that has been rebuilt, usually by replacing weak modules. The rest of the pack keeps its age.</p></div>'
               '<div class="card"><h3>Module repair</h3><p>Only the failed modules in your pack are replaced. The other modules keep their age and wear.</p></div>'
               '</div>'),
              ('Is it the battery?',
               '<p>A hybrid system warning can come from the battery pack or from other parts of the hybrid system. We read the fault code first, so you only replace the battery when the battery is the problem. '
               'More in our guide: <a href="{u}articles/hybrid-battery-replacement-signs/">signs your hybrid battery needs replacing</a>.</p>')],
        # Own steps (14 Oct 2026): the shared steps offer "repair, recon, used or new" and a 6-month repair warranty,
        # which do not fit a page that fits brand-new OEM packs only, with a 1 year or 100,000 km warranty.
        steps=[('WhatsApp us the details', 'Send your car model and year, and the fault code if you have one, to <a href="{wa}" target="_blank" rel="noopener">9893 1923</a>.'),
               ('We check and advise', 'We read the fault code to confirm the battery is the problem, then check availability and price of a brand-new OEM battery for your car.'),
               ('Drop off or pick-up', 'Bring the car to us at Premier @ Kaki Bukit, or use our pick-up and delivery service.'),
               ('Fitted, with warranty', 'We remove the old pack and fit the new one. The battery comes with a warranty of 1 year or 100,000 km.')],
        visit=True,
        related=['hybrid-battery-replacement-signs'],
    ),
    dict(
        slug='bmw-temperature-programming', key='bmw', name='BMW Temperature Programming',
        title='BMW Temperature Programming Singapore | Coolant 120°C to 95°C | The ECU Clinic',
        desc='BMW coolant temperature programming in Kaki Bukit: bring a high running temperature down to about 95°C. Most models 2010–2018. WhatsApp 9893 1923.',
        h1='BMW Temperature Programming',
        lead='BMW running hot at 120°C or more? We reprogram it to bring a high coolant temperature down to a stable 95°C or so.',
        photo='bmw-fault-code-scan', alt='Scan tool reading BMW engine fault codes',
        share='diagnostic-bmw-fault-codes.jpg',
        intro=['Many BMWs from this period run at a high coolant temperature, often 120°C or more. We reprogram the engine’s temperature setting so it runs at about 95°C instead, for steady performance and long-term engine protection.',
               'Daily driving and the car’s other functions are not changed. Check the list below for your model, or WhatsApp us your model and year to confirm.'],
        what=['Reduces high coolant temperature to about 95°C', 'Keeps the engine at a stable operating temperature',
              'No change to daily driving or other functions', 'Most BMW models from 2010 to 2018'],
        signs=[], faq=[('Which BMWs can have temperature programming?', 'Most BMW models from 2010 to 2018, including the 1 to 8 Series, X1 to X6, M2 and Z4. See the full list on this page, or WhatsApp us your model to check.')],
        related=[],
    ),
]

# slug, title tag, meta desc, h1, lead, photo, alt, share photo, date, related service slug, body html
ARTICLES = [
    dict(
        slug='abs-warning-light-causes', service='abs-pump-repair', date='2026-10-13',
        title='ABS Warning Light On? Common Causes and What To Do | The ECU Clinic',
        desc='Why the ABS warning light comes on, what it means for your brakes, the common causes from sensors to the ABS pump and module, and what to do next.',
        h1='ABS Warning Light On? Common Causes and What To Do',
        lead='What the ABS light means, the usual causes, and how to get it fixed without guessing.',
        photo='abs-pump-in-car', alt='ABS pump and module in a car’s engine bay', share='abs-unit-engine-bay-1.jpg',
        body='''<p>The ABS (anti-lock braking system) light tells you the car has found a fault in its anti-lock braking system. In most cases your normal brakes still work, but the anti-lock function may be switched off until the fault is fixed. That means the wheels can lock under hard braking, especially on wet roads.</p>
<p>If the red brake warning light comes on together with the ABS light, or the brake pedal feels different, stop driving and get the car checked before you go further.</p>
<h2>Common causes of an ABS warning light</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has a sensor that tells the ABS how fast it is turning. A dirty, damaged or failed sensor is a common cause.</li>
<li><strong>Wiring and connectors.</strong> Sensor wires run close to the wheels and can be damaged or corroded.</li>
<li><strong>ABS module.</strong> The electronic control module can develop internal faults. On many cars it is mounted on the pump.</li>
<li><strong>ABS pump.</strong> The pump motor or hydraulic unit can fail.</li>
<li><strong>Low brake fluid or a blown fuse.</strong> Simple causes worth ruling out first.</li>
</ul>
<h2>Why the fault code matters</h2>
<p>The same warning light can come from a cheap sensor or from the ABS unit itself. Reading the fault code with a scan tool is the quickest way to know which. Replacing parts without the code often means paying for parts you did not need.</p>
<h2>Repair, recon, used or new?</h2>
<p>If the fault is in the ABS pump or module, there is usually more than one way to fix it. We can repair your unit, or supply a reconditioned, used or new one. We explain the options before any work starts.</p>
<h2>What to send us</h2>
<p>WhatsApp us your car model, chassis number and the fault code. A photo of the dashboard or the scan tool screen also helps. Our repairs come with a 6-month warranty.</p>''',
    ),
    dict(
        slug='mercedes-active-brake-assist-functions-limited', service='abs-pump-repair', date='2026-10-13',
        title='Mercedes “Active Brake Assist Functions Limited”: What It Means | The ECU Clinic',
        desc='What the Mercedes “Active Brake Assist functions limited” message means, common reasons it appears, and when it needs a diagnosis.',
        h1='Mercedes “Active Brake Assist Functions Limited”: What It Means',
        lead='Why this message appears on a Mercedes dashboard, and when it is more than a dirty sensor.',
        photo='active-brake-assist-warning', alt='Mercedes dashboard showing Active Brake Assist functions limited',
        share='mercedes-active-brake-assist-warning.jpg',
        body='''<p>Active Brake Assist is the Mercedes-Benz system that watches the road ahead and can warn you, or help brake, if a collision is likely. When the dashboard says “Active Brake Assist functions limited”, the car is telling you the system cannot work fully right now.</p>
<h2>Common reasons for the message</h2>
<ul class="ticks">
<li><strong>Blocked sensor.</strong> Dirt, rain, snow or a sticker over the radar sensor in the front of the car, or the camera area of the windscreen, can limit the system for a while.</li>
<li><strong>Sensor or alignment fault.</strong> A damaged or misaligned radar sensor, for example after a minor knock to the front.</li>
<li><strong>Other brake or stability faults.</strong> Active Brake Assist relies on other systems such as ESP. A fault there can also limit it.</li>
</ul>
<h2>What to check first</h2>
<p>If the message appears in heavy rain or after the car gets dirty, clean the front of the car and the windscreen, then restart. If the message clears and stays away, it was most likely a temporary blockage.</p>
<h2>When it needs a diagnosis</h2>
<p>If the message stays on, keeps coming back, or appears with an ABS or ESP warning, the system has stored a fault code. Reading that code shows whether the cause is the sensor, the wiring, or a brake system unit such as the ESP module.</p>
<p>We diagnose brake system warnings like this one and tell you what is causing it before any part is changed. WhatsApp us a photo of the dashboard, your car model, chassis number and the fault code.</p>''',
    ),
    dict(
        slug='mercedes-7g-tronic-722-9-tcu-problems', service='mercedes-7g-9g-tcu-repair', date='2026-10-13',
        title='Mercedes 7G-Tronic (722.9) TCU Problems: Signs and Repair | The ECU Clinic',
        desc='Signs of a failing TCU on the Mercedes 7G-Tronic 722.9 gearbox: limp mode, harsh shifts and gearbox warnings. What the conductor plate does and how it is repaired.',
        h1='Mercedes 7G-Tronic (722.9) TCU Problems: Signs and Repair',
        lead='How a gearbox control fault shows up on the Mercedes 7-speed, and why the fault code comes first.',
        photo='mercedes-7g-conductor-plate', alt='Mercedes 722.9 conductor plate with new filter, gasket and gearbox oil',
        share='mercedes-722-9-conductor-plate-kit.jpg',
        body='''<p>The 7G-Tronic is the 7-speed automatic gearbox used in many Mercedes-Benz cars. Its gearbox code is 722.9. Unlike older designs, its transmission control unit (TCU) is mounted inside the gearbox, on a part called the conductor plate, which also carries speed sensors.</p>
<h2>Common signs of a TCU or conductor plate fault</h2>
<ul class="ticks">
<li><strong>Limp mode.</strong> The gearbox stays in one gear to protect itself and will not shift up.</li>
<li><strong>Gearbox warning.</strong> A transmission message or warning appears on the dashboard.</li>
<li><strong>Harsh or delayed shifts.</strong> Gear changes feel rough or late.</li>
<li><strong>Gear display problems.</strong> The gear indicator flashes, goes blank or shows the wrong gear.</li>
</ul>
<p>These signs can also come from low or old gearbox oil, wiring or mechanical problems, so they do not always mean the TCU has failed.</p>
<h2>Why the fault code comes first</h2>
<p>The TCU stores fault codes that point to the cause, such as a speed sensor or a solenoid circuit. Reading them tells us whether the TCU and conductor plate are the problem before the gearbox is opened.</p>
<h2>How we repair it</h2>
<p>We work on the TCU and conductor plate. Because the gearbox pan has to come off, we fit a new filter, pan gasket and gearbox oil on the same job. We also work on the TCU of the 9-speed 9G-Tronic.</p>
<p>WhatsApp us your car model, chassis number and the fault code. Our repairs come with a 6-month warranty.</p>''',
    ),
    dict(
        slug='mercedes-steering-lock-elv-failure', service='mercedes-steering-lock-elv-repair', date='2026-10-13',
        title='Mercedes Steering Lock (ELV) Failure: Signs and Repair | The ECU Clinic',
        desc='Key won’t turn or Mercedes won’t start? Signs of a failing electronic steering lock (ELV/ESL), what it does, and how it is repaired in Singapore.',
        h1='Mercedes Steering Lock (ELV) Failure: Signs and Repair',
        lead='When a Mercedes will not start and the key will not turn, the steering lock is one of the first things to check.',
        photo='elv-units', alt='Mercedes electronic steering lock units', share='elv-steering-lock-units.jpg',
        body='''<p>Many Mercedes-Benz cars have an electronic steering lock, usually called the ELV or ESL. It is a small motorised lock on the steering column. When you switch off, it locks the steering. When you insert the key or press start, the car checks the key and the ELV unlocks.</p>
<h2>Signs of an ELV fault</h2>
<ul class="ticks">
<li><strong>The key will not turn</strong> in the ignition, even though it is the right key.</li>
<li><strong>No start, no crank.</strong> Nothing happens when you try to start.</li>
<li><strong>Steering stays locked</strong> after switching on.</li>
<li><strong>It works sometimes.</strong> The car starts on one try and not the next, which often gets worse over time.</li>
</ul>
<p>A flat key battery, a weak car battery or an ignition switch fault can cause similar symptoms, so these are worth ruling out.</p>
<h2>How it is fixed</h2>
<p>We test the steering lock and repair it. If your car cannot be driven, our pick-up and delivery service can collect it.</p>
<p>WhatsApp us your car model and what the car is doing. Our repairs come with a 6-month warranty.</p>''',
    ),
    dict(
        slug='hybrid-battery-replacement-signs', service='hybrid-battery-replacement', date='2026-10-13',
        title='Signs Your Hybrid Battery Needs Replacing | The ECU Clinic Singapore',
        desc='The common signs of a weak hybrid battery, what causes it, and replacing it with a brand-new OEM battery with a 1-year or 100,000 km warranty.',
        h1='Signs Your Hybrid Battery Needs Replacing',
        lead='How a tired hybrid battery shows up in daily driving, and what replacement involves.',
        photo='hybrid-battery-modules', alt='Hybrid battery pack with new modules', share='hybrid-battery-new-modules.jpg',
        body='''<p>A hybrid car stores energy in a high-voltage battery pack made of many cells or modules. Like any rechargeable battery, it slowly loses capacity with age and use. When it can no longer hold enough charge, the car leans more on the petrol engine, and eventually the hybrid system flags a fault.</p>
<h2>Common signs of a weak hybrid battery</h2>
<ul class="ticks">
<li><strong>Hybrid system warning light</strong> on the dashboard.</li>
<li><strong>Higher fuel use</strong> than the car used to have.</li>
<li><strong>The engine runs more often</strong>, including at low speed where it used to run on electric power.</li>
<li><strong>The battery gauge jumps</strong>, dropping or filling quickly.</li>
<li><strong>Less pulling power</strong> when you accelerate.</li>
</ul>
<p>These signs can have other causes too, so a diagnosis with a scan tool is the way to be sure.</p>
<h2>Replacing the battery</h2>
<p>We replace hybrid batteries with brand-new OEM packs, including removal and fitting. Each comes with a warranty of 1 year or 100,000 km.</p>
<p>WhatsApp us your car model and year, and we will check availability and price.</p>''',
    ),
    dict(
        slug='toyota-voxy-noah-sienta-abs-pump', service='abs-pump-repair', date='2026-10-13',
        title='Toyota Voxy, Noah & Sienta ABS Pump: Repair, Recon or Used | The ECU Clinic',
        desc='ABS pump and module options for the Toyota Voxy, Noah and Sienta in Singapore: repair, replace, used or recon, with plug and play available and a 6-month warranty.',
        h1='Toyota Voxy, Noah & Sienta ABS Pump: Repair, Recon or Used',
        lead='Your options when the ABS pump or module on a Voxy, Noah or Sienta gives trouble.',
        photo='abs-module-in-car', alt='ABS module in a car’s engine bay', share='abs-unit-engine-bay-2.jpg',
        body='''<p>The Toyota Voxy, Noah and Sienta are common family cars in Singapore. Like any car with ABS, they can develop faults in the ABS pump or module, which usually shows up as warning lights on the dashboard.</p>
<h2>Signs to look out for</h2>
<ul class="ticks">
<li>ABS warning light on</li>
<li>Brake system or skid control (VSC) warnings at the same time</li>
<li>A fault code for the ABS actuator or pump motor</li>
</ul>
<p>A sensor or wiring fault can cause the same lights, so we read the fault code first.</p>
<h2>Your options</h2>
<p>For the Voxy, Noah and Sienta we can:</p>
<ul class="ticks">
<li><strong>Repair</strong> your existing ABS pump or module</li>
<li><strong>Replace</strong> it</li>
<li>Supply a <strong>used</strong> unit</li>
<li>Supply a <strong>reconditioned</strong> unit</li>
</ul>
<p>Plug and play is available, and our repairs come with a 6-month warranty.</p>
<h2>Get a quick answer</h2>
<p>WhatsApp us your car model, chassis number and the fault code. A photo of the warning lights also helps.</p>''',
    ),
]
