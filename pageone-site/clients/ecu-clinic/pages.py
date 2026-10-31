"""Service pages and articles for The ECU Clinic (added 13 Oct 2026, Edwin's standing rule: one page per
specialised service plus an articles section for long-tail searches).

Client facts come only from source/content.md. Articles add general, widely documented car knowledge
in hedged wording ("can", "often"), with no prices, no model-specific failure claims and no promises.
Body text is HTML; {wa} is replaced with the WhatsApp link by build.py.
Every WhatsApp link (including {wa}) is prefilled by build.py with the page name and the button tapped
(16 Oct 2026), so never hand-write a wa.me link here.
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
        what=['ABS, ESP and ESC module repair', 'Honda VSA modulator faults, such as “VSA Solenoid Valve Malfunction” (121-11)',
              'Honda yaw rate and acceleration sensor faults inside the modulator (81-19, 81-20)',
              'Used and reconditioned ABS pumps', 'Mercedes-Benz ESP pumps and units, such as the N30/4 control unit',
              'Hyundai and Kia ESC units', 'Toyota Voxy, Noah and Sienta: repair, replace, used or recon',
              'Plug and play available', 'Makes include Audi, VW, BMW, Chevrolet, Honda, Mercedes, Nissan, Toyota, Skoda, Mini, Kia and Volvo'],
        signs=[('ABS light stays on', 'The ABS warning light comes on and stays on after the car is restarted.'),
               ('ESP or traction light too', 'ESP, ESC or traction control warnings appear together with the ABS light.'),
               ('Brake system message', 'The dashboard shows a brake system or brake assist message.'),
               ('Fault code points to the module', 'A scan shows a code for the ABS control module or pump motor.')],
        faq=[('Can you repair my ABS pump or module?', 'Yes. We repair ABS, ESP and ESC modules and supply used and reconditioned ABS pumps for makes such as Toyota, Honda, Mercedes-Benz, Hyundai, Kia, Volkswagen, Audi, Nissan, Volvo and Chevrolet.'),
             ('Do you fix the Honda “VSA Solenoid Valve Malfunction” fault?', 'Yes. The Honda VSA (ABS) unit fault 121-11 is one of the Honda jobs we see most often. WhatsApp us the model, year and fault codes.'),
             ('Do you do Toyota Voxy, Noah and Sienta ABS pumps?', 'Yes. We repair, replace or supply used and recon ABS pumps and modules for the Toyota Voxy, Noah and Sienta, with plug and play available.'),
             ('Is there a warranty?', 'Yes. Our repairs come with a 6-month warranty.'),
             ('What should I send you?', 'Your car model, chassis number and the fault code. A photo of the scan tool screen or the warning light also helps.'),
             ('Is it safe to drive with the ABS light on?', 'In most cases your normal brakes still work, but the anti-lock function may be off until the fault is fixed, so the wheels can lock under hard braking, especially on wet roads. If the red brake warning light is on too, or the pedal feels different, stop driving and get the car checked.'),
             ('Can I bring in just the ABS unit?', 'Yes. You can bring the car or the part to us at Premier @ Kaki Bukit, or use our pick-up and delivery service.')],
        # EDGE Loop, 13 Oct 2026 (owner page for "abs pump repair singapore" and "abs module repair singapore").
        # The Singapore top 10 (Carousell listings, workshop pages, a V-Tec product page) mostly skip these:
        # driving with the light on, how sensor vs unit is told apart, and a plain comparison of the options.
        updated='27 Oct 2026',
        jobs=[('mercedes-c180-esp-unit', 'Mercedes C180 CGI (W204): ESP unit we repaired, internal faults 5944 and 5001'),
              ('mercedes-c180-esp-codes', 'Same car: internal faults in the ESP control unit (N30/4)'),
              ('mercedes-esp-pumps', 'Mercedes-Benz ESP pumps on our bench'), ('hyundai-kia-esc', 'Hyundai / Kia ESC unit'),
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
        related=['honda-vsa-solenoid-valve-malfunction', 'mercedes-esp-control-unit-fault-n30-4', 'abs-warning-light-causes'],
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
        desc='Key won’t turn or Mercedes won’t start? We test and repair the electronic steering lock (ELV/ESL), or fit an ELV emulator, in Kaki Bukit. Pick-up if your car can’t be driven.',
        h1='Mercedes Steering Lock (ELV) Repair',
        lead='Key won’t turn, or the car won’t start because of the steering lock? We diagnose and repair the electronic steering lock (ELV) on Mercedes-Benz.',
        photo='mercedes-elv', alt='Mercedes-Benz electronic steering lock (ELV) on the bench',
        share='mercedes-elv-steering-lock.jpg',
        intro=['Many Mercedes-Benz models use an electronic steering lock, often called the ELV or ESL. It is a small motorised unit on the steering column that locks the steering when the car is off and unlocks it when the key is turned or the start button is pressed.',
               'If the ELV does not unlock, the car cannot start. We test the unit, repair it, and get your car driving again. WhatsApp us your model and what the car is doing, and we will tell you what we can do.'],
        what=['Mercedes-Benz ELV diagnosis', 'Steering lock repair', 'Mercedes ELV emulators', 'Pick-up and delivery available'],
        signs=[('Key won’t turn', 'The key goes in but will not turn in the ignition.'),
               ('No start, no crank', 'Nothing happens when you try to start the car.'),
               ('Steering stays locked', 'The steering wheel stays locked after you switch on.'),
               ('Works sometimes', 'The car starts on some tries and not on others.')],
        faq=[('Do you repair Mercedes steering locks?', 'Yes. We repair the electronic steering lock (ELV) on Mercedes-Benz cars. WhatsApp us your model and what the car is doing.'),
             ('My car won’t start. Can you collect it?', 'Pick-up and delivery service is available. WhatsApp us your location.'),
             ('Is it the steering lock, or just the key or battery?', 'A flat key battery, a weak car battery or an ignition switch fault can look like a steering lock fault, so we rule those out first. Then we test the steering lock itself.'),
             ('It still starts sometimes. Can I wait?', 'A steering lock that works on some tries and not others often gets worse over time, and when it stops unlocking the car will not start at all. Get it checked before it leaves you stranded.'),
             ('What is an ELV emulator, and when is it used?', 'An ELV emulator is a small electronic unit that takes the place of the steering lock. It gives the car the signal it expects from the lock, so the car can start. It is used instead of repairing the lock when the lock itself has failed and repairing it is not the right fix. The original lock comes off, so the steering no longer locks when you switch off. We explain both options before any work starts.'),
             ('Is there a warranty?', 'Yes. Our repairs come with a 6-month warranty.')],
        # EDGE Loop, 14 Oct 2026 (owner page for "mercedes steering lock repair singapore" / "mercedes elv repair").
        # The top results are overseas: US DIY guides and dealer quotes in USD, eBay parts and tool listings, a South
        # African mobile mechanic. None is a Singapore workshop, none says how to tell the lock from a key or battery
        # fault, and none deals with the car that cannot be driven to a workshop.
        updated='14 Oct 2026',
        jobs=[('mercedes-elv', 'ELV emulator and Mercedes ignition switch with key on our test bench'), ('elv-units', 'ELV emulator (top) and Mercedes ignition switch on our bench')],
        more=[('Steering lock, key or battery: what we check first',
               '<ol class="steps"><li><strong>The simple causes.</strong> A flat key battery, a weak car battery or an ignition switch fault can look just like a steering lock fault.</li>'
               '<li><strong>The fault codes.</strong> The car’s control units store codes that show whether they can talk to the steering lock.</li>'
               '<li><strong>The steering lock itself.</strong> We test the unit to confirm it is the part that is failing.</li>'
               '<li><strong>Your options.</strong> Repair the steering lock, or fit an ELV emulator. We tell you what we can do before any work starts.</li></ol>'
               '<p>More in our guide: <a href="{u}articles/mercedes-steering-lock-elv-failure/">Mercedes steering lock (ELV) failure: signs and repair</a>.</p>'),
              # Client sells Mercedes ELV emulators (Edwin, 14 Oct 2026). No prices, brands or emulator warranty terms stated.
              ('Your options: repair the lock or fit an ELV emulator',
               '<div class="grid g2">'
               '<div class="card"><h3>Repair the steering lock</h3><p>We repair your car’s own electronic steering lock, so it keeps locking the steering when the car is off.</p></div>'
               '<div class="card"><h3>Fit an ELV emulator</h3><p>A small electronic unit that takes the place of the steering lock. It gives the car the signal it expects from the lock, so the car starts. The original lock comes off, so the steering no longer locks when you switch off.</p></div>'
               '</div>'
               '<p style="margin-top:16px">An emulator is used instead of repairing the lock when the lock itself has failed and repairing it is not the right fix for your car. We test the lock first and explain both options before any work starts.</p>'),
              ('Car stuck and won’t start? We can collect it',
               '<p>When the steering lock fails, the car usually cannot be driven to a workshop. Our pick-up and delivery service can collect it. '
               'WhatsApp us your car model, your location and what the car is doing: for example, the key will not turn, nothing happens when you press start, or a message appears on the dashboard. '
               'WhatsApp enquiries are welcome 24/7.</p>'),
              ('Repaired here in Singapore',
               '<p>Most of what you will find online about Mercedes steering lock faults is written for drivers abroad: do-it-yourself guides, parts and tools posted from overseas, and dealer quotes in US dollars. '
               'With us, the testing and repair are done at our workshop at Premier @ Kaki Bukit, and our repairs come with a 6-month warranty.</p>')],
        steps=[('WhatsApp us the details', 'Send your car model and what the car is doing to <a href="{wa}" target="_blank" rel="noopener">9893 1923</a>. If you have a fault code, send that too.'),
               ('We check and advise', 'We rule out the key and battery, test the steering lock, and tell you the options (repair the lock or fit an ELV emulator) before any work starts.'),
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
        slug='honda-radar-repair', key='radar', name='Honda Front Radar (ADAS) Repair',
        title='Honda Sensing Radar Repair Singapore | The ECU Clinic',
        desc='Honda front radar (millimeter wave radar) repair in Kaki Bukit. P2583 radar function error and Honda Sensing warnings. We repair your unit instead of replacing it. WhatsApp 9893 1923.',
        h1='Honda Front Radar (ADAS) Repair',
        lead='Honda Sensing warning, or a “Millimeter Wave Radar Function Error” on the scan tool? We repair your existing front radar unit instead of replacing it with a new one.',
        photo='honda-radar-fault-codes', alt='Scan tool showing Honda Vezel millimeter wave radar fault codes P2583-4A and P2583-54',
        share='honda-vezel-radar-fault-codes.jpg',
        intro=['Honda Sensing driver assistance features, such as collision mitigation braking and adaptive cruise control, rely on a millimeter wave radar unit at the front of the car. When that radar unit develops a fault, Honda Sensing warnings come on and the driver assistance features can switch off.',
               'On the scan tool this often shows as P2583, “Millimeter Wave Radar Function Error”, in the driver assistance system. We read the codes first, then repair the radar unit you already have, instead of fitting a new one.',
               'A second code, “Millimeter Wave Radar Aiming Incomplete”, means the radar also needs to be aimed (calibrated) before the system works normally. We tell you what your car needs before any work starts.'],
        what=['Honda front radar (millimeter wave radar) repair', 'Repair of your existing unit, no new radar needed',
              'Fault code reading and diagnosis', 'Honda models with Honda Sensing, such as the Vezel'],
        signs=[('Honda Sensing warning', 'A Honda Sensing or driver assistance warning appears on the dashboard.'),
               ('Features switched off', 'Adaptive cruise control or collision mitigation braking is unavailable.'),
               ('Radar fault code', 'A scan shows P2583 “Millimeter Wave Radar Function Error”.'),
               ('Aiming incomplete', 'A scan shows “Millimeter Wave Radar Aiming Incomplete”.')],
        faq=[('Do I need a new radar unit?', 'Not always. We repair the existing front radar unit instead of replacing it.'),
             ('My Honda has both ABS and radar faults. Can you fix both?', 'Yes. We see cars with both the VSA (ABS) unit and the front radar faulty, and repair both on the same visit. WhatsApp us all the fault codes.'),
             ('Which Honda models do you work on?', 'Honda models with Honda Sensing and a front millimeter wave radar, such as the Vezel. WhatsApp us your model and year to check.'),
             ('Is there a warranty?', 'Yes. Our repairs come with a 6-month warranty.'),
             ('What should I send you?', 'Your car model, year and the fault codes. A photo of the scan tool screen or the dashboard warning helps.')],
        related=['honda-millimeter-wave-radar-error-p2583', 'honda-vsa-solenoid-valve-malfunction'],
        jobs=[('honda-radar-fault-codes', '2019 Honda Vezel: radar function error and aiming incomplete'),
              ('honda-abs-radar-codes', 'Honda Vezel with both the radar and the VSA (ABS) unit faulty')],
    ),
    dict(
        slug='bmw-cas-module-repair', key='cas', name='BMW CAS Module Repair',
        title='BMW CAS Module Repair Singapore | The ECU Clinic',
        desc='BMW CAS (Car Access System) module repair in Kaki Bukit. Key not recognised, car won’t start or steering lock (ELV) faults. WhatsApp 9893 1923.',
        h1='BMW CAS Module Repair',
        lead='Key not recognised, car won’t start, or CAS and steering lock faults on the scan tool? We repair the BMW CAS module.',
        photo='bmw-cas-fault-codes', alt='Scan tool showing BMW CAS fault codes for ELV, processor and engine start',
        share='bmw-cas-fault-codes.jpg',
        intro=['The CAS (Car Access System) is the BMW control unit that recognises your key, works with the immobiliser and allows the engine to start. On many BMWs it also controls the electric steering lock (ELV).',
               'When the CAS module develops a fault, the car may not recognise the key, the engine may not start, or the steering lock may stay locked. We read the fault codes first, then repair the CAS module, or fit a used CAS module matched to your car’s own keys and engine control unit.'],
        what=['BMW CAS module diagnosis and repair', 'Used CAS module fitted and matched to your car’s own keys', 'CAS faults linked to the electric steering lock (ELV)',
              'Engine start and key recognition faults', 'Fault code reading'],
        signs=[('Key not recognised', 'The car does not detect the key, or shows a key or immobiliser message.'),
               ('Engine won’t start', 'The starter does not turn, or the engine does not crank.'),
               ('Steering lock problems', 'The steering stays locked, or a steering lock message appears.'),
               ('CAS fault codes', 'A scan shows CAS codes such as “ELV Fault”, “Processor” or “Engine Start, Starter Operation”.')],
        faq=[('What does the CAS module do?', 'It recognises the key, works with the immobiliser, allows the engine to start and, on many BMWs, controls the electric steering lock.'),
             ('My BMW won’t start and shows CAS codes. Can you help?', 'Yes. WhatsApp us your model, year and the fault codes. Our pick-up and delivery service can collect a car that will not start.'),
             ('Can you fit a used CAS module?', 'Yes. Where repairing the original is not the right fix, we fit a used CAS module and match it to your car’s own keys and engine control unit.'),
             ('Is there a warranty?', 'Yes. Our repairs come with a 6-month warranty.')],
        related=['bmw-cas-elv-fault-codes'],
        updated='27 Oct 2026',
        jobs=[('bmw-cas3-modules', 'Two BMW E90 CAS3 modules on our bench, including the used unit we fitted'),
              ('bmw-cas-fault-codes', '2009 BMW 320i: CAS and steering lock fault codes')],
        more=[('Recent job: 2009 BMW 320i (E90) that would not start',
               '<p>This 320i came in with a long list of CAS codes: ELV (steering lock) fault, processor, power supply to the steering lock, engine start and control-unit fault. The car’s own CAS module was faulty.</p>'
               '<p>We fitted a used E90 CAS3 module and matched it to the car’s own keys and engine control unit, so the car recognises its keys and starts again. The codes are explained in our guide: <a href="{u}articles/bmw-cas-elv-fault-codes/">BMW CAS fault codes</a>.</p>')],
    ),
    dict(
        slug='mercedes-ecu-repair', key='ecu', name='Mercedes Engine ECU Repair',
        title='Mercedes ECU Repair Singapore | Engine Control Unit | The ECU Clinic',
        desc='Mercedes-Benz engine ECU repair in Kaki Bukit. We test the ECU and repair your own unit on the bench, such as the Bosch MED17.7.2 on the M274 engine. WhatsApp 9893 1923.',
        h1='Mercedes-Benz Engine ECU Repair',
        lead='Several engine circuit faults at once, such as Camtronic, camshaft or sensor codes? We test the engine ECU and repair your own unit on the bench.',
        photo='mercedes-me17-ecus', alt='Two Mercedes-Benz Bosch MED17.7.2 engine ECUs (M274 engine) on our repair bench',
        share='mercedes-me17-ecus-c205.jpg',
        intro=['The engine ECU (engine control unit) runs the engine: it reads the sensors and drives the injectors, ignition, camshaft adjusters and, on Mercedes engines such as the M274, the Camtronic valve lift solenoids.',
               'When a driver circuit or a sensor supply inside the ECU fails, the scan tool can show several circuit codes at the same time, even though the sensors and solenoids themselves may be fine. We read every code, check the wiring and parts first, and if the ECU is at fault we repair your own unit on the bench and refit it.'],
        what=['Mercedes-Benz engine ECU (ME / MED17) diagnosis and repair', 'Bench repair of your own ECU',
              'Camtronic solenoid, camshaft and sensor circuit faults traced to the ECU', 'Fault code reading'],
        signs=[('Many circuit codes at once', 'A scan shows several circuit faults together, such as Camtronic solenoids, camshaft position, intake air pressure and charge air temperature.'),
               ('Engine warning light', 'The check engine light stays on, or comes back soon after the codes are cleared.'),
               ('Codes return after new parts', 'A sensor or solenoid was replaced, but the same circuit fault comes back.')],
        faq=[('Can you repair my Mercedes ECU instead of replacing it?', 'Often, yes. WhatsApp us the model, year and fault codes. If the fault is inside the ECU, we repair your own unit on the bench.'),
             ('Can I bring in just the ECU?', 'Yes. Bring the car or the ECU to us at Premier @ Kaki Bukit, or use our pick-up and delivery service.'),
             ('Is there a warranty?', 'Yes. Our repairs come with a 6-month warranty.')],
        related=[],
        img_commit='0ec3278037d64b025d7e569b9735eef6d32f293f',  # share image added after IMG_COMMIT
        updated='27 Oct 2026',
        jobs=[('mercedes-me17-ecus', 'Mercedes C-Class (C205): Bosch MED17.7.2 engine ECUs on our bench'),
              ('mercedes-camtronic-codes', 'Scan of the same car: Camtronic, camshaft and sensor circuit codes')],
        more=[('Recent job: Mercedes C-Class (C205), M274 engine',
               '<p>The engine control unit (N3/10) had stored codes including:</p><ul class="ticks">'
               '<li><strong>P001A13</strong> Camtronic solenoid 1 “Intake”: open circuit</li>'
               '<li><strong>P002A13</strong> Camtronic solenoid 1 “Exhaust”: open circuit</li>'
               '<li><strong>P261612</strong> Camshaft position output signal: short circuit to positive</li>'
               '<li><strong>P119012</strong> Intake air pressure sensor: short circuit to positive</li>'
               '<li><strong>P007D12</strong> Charge air temperature sensor: short circuit to positive</li></ul>'
               '<p>With several unrelated circuits faulty at the same time, we tested the ECU itself. The fault was in the car’s own ECU, so we repaired it on the bench, refitted it and cleared the codes.</p>')],
    ),
    dict(
        slug='audi-abs-repair', key='audi', name='Audi ABS Pump & Module Repair',
        title='Audi ABS Repair Specialist Singapore | ABS Module | The ECU Clinic',
        desc='Audi ABS pump and ABS module repair in Kaki Bukit. We read the brake electronics codes and repair your own ABS module. 6-month warranty. WhatsApp 9893 1923.',
        h1='Audi ABS Repair Specialist in Singapore',
        lead='ABS and ESP lights on in your Audi? We read the brake electronics codes and repair your own ABS module.',
        photo='audi-abs-fault-codes', alt='Scan tool showing Audi brake electronics codes: ABS hydraulic pump and control module defective',
        share='audi-a3-abs-codes.jpg',
        intro=['On an Audi, the ABS unit in the engine bay combines the hydraulic pump with the brake electronics control module (address 03 on the scan tool). When the module fails, it often stores a long list of codes at once, including wheel speed sensor codes, even when the sensors themselves may be fine.',
               'We read every code first and rule out the simple causes, such as sensors, wiring and a weak battery. Then we repair your own ABS module. ABS pumps and modules are our main work, and many car workshops send their ABS repairs to us.'],
        what=['Audi ABS module (brake electronics) repair', 'ABS hydraulic pump faults',
              'Codes such as 01276 “ABS Hydraulic Pump” and 16352 “Control Module” defective', 'Volkswagen and Skoda ABS units too'],
        signs=[('ABS and ESP lights on', 'The ABS and ESP (ESC) warning lights come on together and stay on.'),
               ('Many codes at once', 'Wheel speed sensor, rotation rate sensor and reference voltage codes appear together with pump or module codes.'),
               ('Pump or module “defective”', 'The scan shows 01276 ABS Hydraulic Pump or 16352 Control Module as defective.')],
        faq=[('Do you repair Audi ABS modules?', 'Yes. We repair the ABS module on Audi cars, and on Volkswagen and Skoda too. WhatsApp us the model, year and fault codes.'),
             ('Is it safe to drive with the ABS light on?', 'In most cases your normal brakes still work, but the anti-lock function may be off until the fault is fixed, so the wheels can lock under hard braking, especially on wet roads. If the red brake warning light is on too, or the pedal feels different, stop driving and get the car checked.'),
             ('Is there a warranty?', 'Yes. Our repairs come with a 6-month warranty.')],
        related=['vw-audi-abs-esp-light-on'],
        img_commit='0ec3278037d64b025d7e569b9735eef6d32f293f',  # share image added after IMG_COMMIT
        updated='27 Oct 2026',
        jobs=[('audi-abs-fault-codes', 'Audi A3: ABS hydraulic pump and control module defective, with sensor codes')],
        more=[('Recent job: Audi A3 with 10 ABS codes',
               '<p>The brake electronics (03) had stored 10 codes, including:</p><ul class="ticks">'
               '<li><strong>01276</strong> ABS Hydraulic Pump: defective</li>'
               '<li><strong>16352</strong> Control Module: defective</li>'
               '<li><strong>00290</strong> and <strong>00287</strong> Left and right rear ABS wheel speed sensors: electrical fault in circuit</li>'
               '<li><strong>01542</strong> Rotation Rate Sensor: electrical fault in circuit</li>'
               '<li><strong>00538</strong> Reference Voltage: electrical fault in circuit</li>'
               '<li><strong>01130</strong> ABS Operation: implausible signal</li></ul>'
               '<p>With the pump, the module and several sensor circuits all faulty at once, the codes pointed to the ABS control module. We repaired the car’s own module, refitted it and cleared the faults.</p>'
               '<p>This scan also had a low voltage code (terminal 30), which a weak battery can cause, so we check the battery as well. More on the lights in our guide: <a href="{u}articles/vw-audi-abs-esp-light-on/">VW or Audi ABS and ESP lights on</a>.</p>')],
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
        slug='honda-yaw-rate-sensor-malfunction', service='abs-pump-repair', date='2026-10-14',
        title='Honda Yaw Rate Sensor Fault 81-19 | The ECU Clinic',
        desc='Honda yaw rate sensor and acceleration sensor faults inside the VSA modulator control unit (81-19, 81-20, C0063, C0062): what they mean and how they are repaired.',
        h1='Honda Yaw Rate Sensor Malfunction (81-19)',
        lead='A well-known Honda ABS fault: the yaw rate sensor inside the VSA modulator, and why it brings up so many other codes.',
        photo='honda-yaw-rate-codes', alt='Scan tool showing Honda codes 81-19 yaw rate sensor and 81-20 acceleration sensor inside the modulator control unit', share='honda-yaw-rate-sensor-codes.jpg',
        body='''<p>The yaw rate sensor measures how fast the car is turning. Together with the acceleration sensor, it tells the VSA (Vehicle Stability Assist) system whether the car is going where the driver is steering. On many Honda models these sensors are built into the VSA modulator control unit, the ABS unit in the engine bay.</p>
<h2>The codes</h2>
<p>The scan in the photo above shows how one fault spreads across several systems:</p>
<ul class="ticks">
<li><strong>81-19</strong> Yaw Rate Sensor (Inside Of Modulator Control Unit) Internal Circuit Malfunction (ABS)</li>
<li><strong>81-20</strong> Acceleration Sensor (Inside Of Modulator Control Unit) Internal Circuit Malfunction (ABS)</li>
<li><strong>38-11</strong> ABS Solenoid Valve Malfunction (ABS)</li>
<li><strong>C0063-F0</strong> Yaw Rate Sensor Malfunction and <strong>U0415-68</strong> ABS System Malfunction (electric servo brake)</li>
<li><strong>C0062-F0</strong> Longitudinal Acceleration Sensor Malfunction and <strong>U0416-68</strong> VSA System Malfunction (electric parking brake)</li>
</ul>
<p>The brake, parking brake and other systems log these codes because they rely on the sensor data from the VSA unit. The words “inside of modulator control unit” point to the unit itself, not to a separate sensor you can swap.</p>
<h2>What you see on the dashboard</h2>
<p>Usually the ABS, VSA and brake warning lights together, often with parking brake or driver assistance warnings as well.</p>
<h2>How it is fixed</h2>
<p>We read all the codes first, then repair the VSA modulator control unit, or supply a reconditioned, used or new one. Our repairs come with a 6-month warranty.</p>
<p>WhatsApp us your car model, year and the fault codes. A photo of the scan tool screen helps.</p>''',
    ),
    dict(
        slug='bmw-cas-elv-fault-codes', service='bmw-cas-module-repair', date='2026-10-14', updated_iso='2026-10-27',
        title='BMW CAS Fault Codes A11E, A0AF, A0B4 | The ECU Clinic',
        desc='What BMW CAS fault codes such as A11E ELV Fault, A0AF Processor and A0B4 Engine Start mean, why the car may not start, and repairing the CAS module.',
        h1='BMW CAS Fault Codes: ELV Fault, Processor and Engine Start',
        lead='Why a BMW shows a list of CAS and steering lock codes, and what to do when the car won’t start.',
        photo='bmw-cas-fault-codes', alt='Scan tool showing BMW CAS fault codes on a 2009 BMW 320i', share='bmw-cas-fault-codes.jpg',
        body='''<p>On many BMWs, the CAS (Car Access System) module recognises the key, works with the immobiliser, allows the engine to start and controls the electric steering lock (ELV). Because it does so much, a CAS fault can show up as several codes at once.</p>
<h2>The codes</h2>
<p>The scan in the photo above, from a 2009 BMW 320i, listed these in the CAS:</p>
<ul class="ticks">
<li><strong>A11E</strong> and <strong>A11A</strong> CAS: ELV Fault</li>
<li><strong>A0AF</strong> CAS: Processor</li>
<li><strong>A119</strong> CAS: Power Supply, El. Steering Lock</li>
<li><strong>A116</strong> CAS: Critical Status, El. Steering Lock</li>
<li><strong>A0B4</strong> CAS: Engine Start, Starter Operation</li>
<li><strong>A0B5</strong> CAS: Fault, Road Speed Signal</li>
<li>CAS: Control-Unit Fault</li>
</ul>
<h2>What the driver notices</h2>
<ul class="ticks">
<li>The key is not recognised</li>
<li>The engine does not crank or start</li>
<li>The steering stays locked, or a steering lock message appears</li>
</ul>
<h2>CAS or steering lock?</h2>
<p>The steering lock and the CAS work together, so codes from one often appear in the other. Reading all the codes, and checking power supply to the steering lock, helps tell which part is at fault before anything is replaced.</p>
<h2>How it is fixed</h2>
<p>We diagnose the CAS and steering lock, then repair the CAS module. For the 320i in the photo, the car’s own CAS module was faulty, so we fitted a used E90 CAS3 module and matched it to the car’s own keys and engine control unit, and the car started again. If the car cannot be driven, our pick-up and delivery service can collect it. Our repairs come with a 6-month warranty.</p>
<p>WhatsApp us your BMW model, year and the fault codes.</p>''',
    ),
    dict(
        slug='honda-vsa-solenoid-valve-malfunction', service='abs-pump-repair', date='2026-10-14',
        title='Honda 121-11 VSA Solenoid Valve Fault | The ECU Clinic',
        desc='What the Honda VSA Solenoid Valve Malfunction code (121-11) means, why ABS, VSA, parking brake and steering warnings come on together, and how it is fixed.',
        h1='Honda VSA Solenoid Valve Malfunction (121-11)',
        lead='One of the most common Honda ABS faults we see: what the code means and why so many warning lights come on at once.',
        photo='honda-vsa-fault-codes', alt='Scan tool showing Honda Vezel fault 121-11 VSA Solenoid Valve Malfunction', share='honda-vezel-vsa-fault-codes.jpg',
        body='''<p>VSA (Vehicle Stability Assist) is Honda’s name for its stability control system. On Honda cars, the ABS and VSA share one unit in the engine bay, often called the VSA modulator: a hydraulic block with solenoid valves, a pump motor and an electronic control module.</p>
<p>When the scan tool shows <strong>121-11 “VSA Solenoid Valve Malfunction”</strong>, the car has found a fault with the valves in that unit. It is one of the Honda ABS faults we handle most often, including on the Honda Vezel.</p>
<h2>Why so many warning lights come on</h2>
<p>Other systems in the car take information from the VSA unit. When it has a fault, they can log their own codes too. On the Vezel in the photo above, the scan showed:</p>
<ul class="ticks">
<li><strong>121-11</strong> VSA Solenoid Valve Malfunction (ABS)</li>
<li><strong>83-141</strong> Electric Parking Brake System Malfunction (ABS)</li>
<li><strong>U0416-68</strong> VSA System Malfunction (electric power steering)</li>
</ul>
<p>On the dashboard this can show up as the ABS, VSA, brake and parking brake lights together, and on cars with Honda Sensing, driver assistance warnings as well. The cause is often the single VSA unit, not several separate faults.</p>
<h2>Is it safe to drive?</h2>
<p>Normal braking usually still works, but anti-lock braking and stability control can be switched off. If the red brake light is on or the brake pedal feels different, stop driving and get the car checked.</p>
<h2>How it is fixed</h2>
<p>We read all the codes first, to confirm the fault is in the VSA unit and not in a sensor or wiring. Then we repair the unit, or supply a reconditioned, used or new one. Our repairs come with a 6-month warranty.</p>
<p>WhatsApp us your car model, year and the fault codes. A photo of the scan tool screen helps.</p>''',
    ),
    dict(
        slug='mercedes-esp-control-unit-fault-n30-4', service='abs-pump-repair', date='2026-10-14',
        title='Mercedes ESP Fault N30/4 (5001) | The ECU Clinic',
        desc='What the Mercedes-Benz fault “internal fault in component N30/4 (Electronic Stability Program control unit)” means, the warnings it causes, and repairing the ESP unit.',
        h1='Mercedes ESP Control Unit Fault: N30/4 Internal Fault (5001)',
        lead='What the N30/4 code means on a Mercedes-Benz, and your options for the ESP pump and module.',
        photo='mercedes-esp-fault-code', alt='Scan tool showing Mercedes-Benz fault 5001, internal fault in component N30/4 ESP control unit', share='mercedes-esp-n30-4-fault-code.jpg',
        body='''<p>On a Mercedes-Benz, <strong>N30/4</strong> is the part number Mercedes uses for the ESP (Electronic Stability Program) control unit. It is fitted to the ESP pump in the engine bay, and it runs the anti-lock brakes, stability control and traction control.</p>
<p>The scan in the photo above, from a Mercedes-Benz C 180 Kompressor (W204), shows <strong>5001: “There is an internal fault in component N30/4 (Electronic Stability Program control unit)”</strong>. An internal fault means the control unit itself has found a problem inside the unit, rather than with a sensor or wire outside it.</p>
<h2>What you see on the dashboard</h2>
<ul class="ticks">
<li>ABS and ESP warning lights</li>
<li>Brake or brake assist messages</li>
<li>On newer models, messages such as “Active Brake Assist functions limited”</li>
</ul>
<h2>Is it safe to drive?</h2>
<p>Normal braking usually still works, but anti-lock braking and stability control can be switched off. If the red brake light is on or the brake pedal feels different, stop driving and get the car checked.</p>
<h2>How it is fixed</h2>
<p>We read all the codes first, to confirm the fault is in the ESP unit. Then we repair your Mercedes ESP pump and module, or supply a reconditioned, used or new one. Our repairs come with a 6-month warranty.</p>
<p>WhatsApp us your car model, chassis number and the fault code. A photo of the scan tool screen helps.</p>''',
    ),
    dict(
        slug='honda-millimeter-wave-radar-error-p2583', service='honda-radar-repair', date='2026-10-14',
        title='Honda P2583 Millimeter Wave Radar Error | The ECU Clinic',
        desc='What the Honda P2583 Millimeter Wave Radar Function Error and Aiming Incomplete codes mean, why Honda Sensing switches off, and repairing the radar instead of replacing it.',
        h1='Honda Millimeter Wave Radar Function Error (P2583)',
        lead='Why Honda Sensing switches off, what the radar codes mean, and how the front radar can be repaired.',
        photo='honda-radar-fault-codes', alt='Scan tool showing Honda Vezel codes P2583-4A and P2583-54', share='honda-vezel-radar-fault-codes.jpg',
        body='''<p>Honda Sensing uses a millimeter wave radar at the front of the car to measure the distance to the vehicle ahead. Features such as collision mitigation braking and adaptive cruise control depend on it. When the radar has a fault, Honda Sensing warnings appear and those features can switch off.</p>
<h2>The codes</h2>
<p>On the 2019 Honda Vezel in the photo above, the driver assistance system showed two codes:</p>
<ul class="ticks">
<li><strong>P2583-4A</strong> Millimeter Wave Radar Function Error: the radar unit itself has a fault.</li>
<li><strong>P2583-54</strong> Millimeter Wave Radar Aiming Incomplete: the radar needs to be aimed (calibrated).</li>
</ul>
<p>Everything else on the car scanned clean, so the problem was the radar.</p>
<h2>Radar and ABS faults on the same car</h2>
<p>Honda Sensing also uses information from the VSA (ABS) unit, so the two systems can show faults together. We have seen a Honda Vezel with three permanent codes at once: <strong>U3000-49</strong> “Multipurpose Camera Unit/Millimeter Wave Radar Internal Electronic Failure”, plus <strong>U0416-68</strong> and <strong>U0416-F8</strong> for the VSA brake actuator and modulator control unit. In a case like that both units need attention, and we read every code before deciding what to repair.</p>
<h2>Other things that can upset the radar</h2>
<ul class="ticks">
<li>Dirt, mud or a sticker over the front emblem or grille where the radar sits</li>
<li>A knock to the front of the car, which can move the radar out of line</li>
<li>Front bumper or grille repairs</li>
</ul>
<p>These are worth ruling out first. If the radar unit itself has failed, clearing the code will not fix it.</p>
<h2>Repair instead of replace</h2>
<p>A new radar unit is an expensive part. We repair the existing radar unit instead of replacing it, and tell you before any work starts whether the radar will also need aiming. Our repairs come with a 6-month warranty.</p>
<p>WhatsApp us your car model, year and the fault codes. A photo of the scan tool screen helps.</p>''',
    ),
    dict(
        slug='abs-warning-light-causes', service='abs-pump-repair', date='2026-10-13', updated_iso='2026-10-22',
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
        slug='mercedes-active-brake-assist-functions-limited', service='abs-pump-repair', date='2026-10-13', updated_iso='2026-10-19',
        title='Active Brake Assist Functions Limited? | The ECU Clinic',
        desc='Mercedes “Active Brake Assist functions limited”? Often a dirty or knocked radar sensor. If it stays on or an ABS or ESP light shows, read the fault code.',
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
    dict(
        # EDGE daily article, 15 Oct 2026 (8pm run). Gap: the results for this question are US DIY pages (YOUCANIC),
        # a US forum and an overseas mail-in seller; none is a Singapore workshop that repairs the Hyundai / Kia ESC unit.
        slug='hyundai-kia-abs-esc-light-on', service='abs-pump-repair', date='2026-10-15', img_commit='5aca7fa95f89177d2c80cb6af8329a685bc3a6fe',
        title='Hyundai or Kia ABS and ESC Light On? Causes and Repair | The ECU Clinic',
        desc='Why the ABS and ESC lights come on together in a Hyundai or Kia, whether it is safe to drive, the usual causes, and how the ESC unit is checked and repaired in Singapore.',
        h1='Why Are the ABS and ESC Lights On in My Hyundai or Kia?',
        lead='One fault, two warning lights: what it means, what to check first, and when the ESC unit itself needs repair.',
        photo='hyundai-kia-esc', alt='Hyundai / Kia ESC unit on our repair bench', share='hyundai-kia-esc-units.jpg',
        body='''<p><strong>Short answer:</strong> in a Hyundai or Kia, the ABS and ESC (Electronic Stability Control) systems share one unit in the engine bay, so a single fault usually turns on both lights. The cause can be a wheel speed sensor, wiring, a switch or sensor the system relies on, or the ESC unit itself. Reading the fault code tells you which.</p>
<h2>What is the ESC unit?</h2>
<p>ESC is the stability control system. It uses the same hydraulic block, pump motor and electronic control module as the anti-lock brakes (ABS). That is why the ABS light, the ESC light and sometimes the brake warning light come on together: the systems run through the same unit.</p>
<h2>Is it safe to drive with the ABS and ESC lights on?</h2>
<p>In most cases your normal brakes still work, but anti-lock braking and stability control may be switched off until the fault is fixed. The wheels can then lock under hard braking, and the car will not correct a skid on a wet road. Leave more distance and avoid hard stops. If the red brake warning light is also on, or the brake pedal feels different, stop driving and get the car checked first.</p>
<h2>What are the common causes?</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has one. A dirty, damaged or failed sensor is a common cause.</li>
<li><strong>Wiring and connectors.</strong> Sensor wiring runs close to the wheels and can be damaged or corroded.</li>
<li><strong>Other inputs the ESC relies on.</strong> Stability control also uses signals such as steering angle and brake pedal position, so a fault there can turn on the ESC light.</li>
<li><strong>Low brake fluid or a blown fuse.</strong> Simple causes worth ruling out first.</li>
<li><strong>The ESC unit itself.</strong> The control module or the pump motor in the unit can develop internal faults.</li>
</ul>
<h2>How do we find which part is at fault?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ESC module stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> Sensors, wiring, fluid level and fuses.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the module or pump, the ESC unit is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Repair, recon, used or new?</h2>
<p>If the fault is in the ESC unit, we can repair your own unit, or supply a reconditioned, used or new one. The photo above is a Hyundai / Kia ESC unit on our bench. Our repairs come with a 6-month warranty. See <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Can I clear the ABS and ESC lights myself?', 'Clearing the code only turns the lights off until the fault is found again. If the cause is still there, the lights come back, so read the code first.'),
             ('How long can I keep driving with the ESC light on?', 'There is no safe fixed limit. Normal braking usually still works, but anti-lock braking and stability control may be off, so get it checked soon, and stop driving if the red brake light is on too.'),
             ('Can you repair the unit without the car?', 'Yes. You can bring just the ESC unit to us at Premier @ Kaki Bukit, or use our pick-up and delivery service.')],
    ),
    dict(
        # EDGE daily article, 16 Oct 2026 (8pm run). Gap: for "toyota abs vsc trc lights on" the results are UK and AU
        # owners' club forum threads and a Pakistani forum; no answer page and no Singapore workshop.
        slug='toyota-abs-vsc-trc-lights-on', service='abs-pump-repair', date='2026-10-16', img_commit='e5ff66e16633185e4cfde2c4e1d2d475b7e1e06b',
        title='Toyota ABS, VSC and TRC Lights On? Causes | The ECU Clinic',
        desc='Why the ABS, VSC and TRC OFF lights come on together in a Toyota, if it is safe to drive, what to check first, and how the ABS unit is repaired in Singapore.',
        h1='Why Are the ABS, VSC and TRC Lights On in My Toyota?',
        lead='Three warning lights at once usually means one fault: what it can be, what to check first, and when the ABS unit needs repair.',
        photo='abs-pump-in-car', alt='ABS pump and module in a car’s engine bay', share='abs-unit-engine-bay-1.jpg',
        body='''<p><strong>Short answer:</strong> in a Toyota, the ABS (anti-lock brakes), VSC (Vehicle Stability Control) and TRC (traction control) systems work through the same brake actuator and control unit, so one fault often turns on all three lights. Common causes are a wheel speed sensor, wiring, a switch or sensor the system relies on, or the ABS unit itself. The fault code tells you which.</p>
<h2>What do the ABS, VSC and TRC lights mean?</h2>
<ul class="ticks">
<li><strong>ABS</strong> is the anti-lock braking system. It stops the wheels locking when you brake hard.</li>
<li><strong>VSC</strong> is Toyota’s stability control. It brakes single wheels to help the car hold its line in a skid.</li>
<li><strong>TRC</strong> is traction control. It stops the wheels spinning when you pull away. On many Toyotas the light reads “TRC OFF” when the system has switched itself off.</li>
</ul>
<p>VSC and TRC both need the wheel speed signals and the brake actuator that ABS uses. When the ABS side has a fault, the car usually switches VSC and TRC off too, which is why the lights come on together.</p>
<h2>Is it safe to drive with the ABS, VSC and TRC lights on?</h2>
<p>In most cases your normal brakes still work, but anti-lock braking, stability control and traction control may be switched off until the fault is fixed. The wheels can then lock under hard braking, and the car will not correct a skid on a wet road. Leave more distance and avoid hard stops. If the red BRAKE warning light is also on, or the brake pedal feels different, stop driving and get the car checked first. Our pick-up and delivery service can collect it.</p>
<h2>Why is the check engine light on as well?</h2>
<p>On many Toyota models, VSC and TRC are also switched off when the engine or hybrid system reports a fault, so the VSC and TRC lights can come on with the check engine light even when the brakes are fine. That is one more reason to read all the stored codes, not just the ABS ones, before any part is changed.</p>
<h2>What are the common causes?</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has one. A dirty, damaged or failed sensor is a common cause.</li>
<li><strong>Wiring and connectors.</strong> Sensor wiring runs close to the wheels and can be damaged or corroded.</li>
<li><strong>Other inputs the system relies on.</strong> Stability control also uses signals such as steering angle, yaw rate and the brake light switch, so a fault there can turn on the VSC light.</li>
<li><strong>Low brake fluid or a blown fuse.</strong> Simple causes worth ruling out first.</li>
<li><strong>The ABS unit itself.</strong> The control module or the pump motor in the brake actuator can develop internal faults.</li>
</ul>
<h2>How do we find which part is at fault?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ABS and skid control system stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> Sensors, wiring, switches, fluid level and fuses.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the module or pump, the ABS unit is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Repair, recon, used or new?</h2>
<p>If the fault is in the ABS unit, we can repair your own unit, or supply a reconditioned, used or new one. Plug and play is available, and our repairs come with a 6-month warranty. Driving a Voxy, Noah or Sienta? See <a href="../toyota-voxy-noah-sienta-abs-pump/">Toyota Voxy, Noah and Sienta ABS pump options</a>, or <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Will the ABS, VSC and TRC lights go off by themselves?', 'Sometimes they go off after a restart if the fault is intermittent, but the code stays stored and the lights usually come back until the cause is fixed. Read the code first.'),
             ('Can a weak battery turn on the VSC light?', 'Low voltage can make some control units store faults, so it is worth checking the battery and charging. If the lights stay on, the stored codes show where the fault really is.'),
             ('Can you repair the ABS unit without the car?', 'Yes. You can bring just the unit to us at Premier @ Kaki Bukit, or use our pick-up and delivery service.')],
    ),
    dict(
        # EDGE daily article, 17 Oct 2026 (8pm run). Gap: for "nissan abs vdc slip light on" the results are US owners' forums
        # (my350z, infinitiscene, cargurus) and Q&A sites (RepairPal, YourMechanic); no answer page and no Singapore workshop.
        slug='nissan-abs-vdc-slip-lights-on', service='abs-pump-repair', date='2026-10-17', img_commit='da285199c37dea7d534214fead290640f7345856',
        title='Nissan ABS, VDC and SLIP Lights On? Causes | The ECU Clinic',
        desc='Why the ABS, VDC OFF and SLIP lights come on together in a Nissan, if it is safe to drive, what to check first, and how the ABS unit is repaired in Singapore.',
        h1='Why Are the ABS, VDC and SLIP Lights On in My Nissan?',
        lead='ABS, VDC OFF and SLIP lights on together? What each light means, the button to check first, and when the ABS unit needs repair.',
        photo='abs-module-in-car', alt='ABS module in a car’s engine bay', share='abs-unit-engine-bay-2.jpg',
        body='''<p><strong>Short answer:</strong> in a Nissan, the ABS (anti-lock brakes), VDC (Vehicle Dynamic Control) and traction control share the same ABS actuator, control unit and wheel speed signals, so one fault often turns on the ABS, VDC OFF and SLIP lights together. Common causes are a wheel speed sensor, wiring, the steering angle sensor or the ABS unit itself. The fault code tells you which.</p>
<h2>What do the ABS, VDC OFF and SLIP lights mean?</h2>
<ul class="ticks">
<li><strong>ABS</strong> is the anti-lock braking system. It stops the wheels locking when you brake hard.</li>
<li><strong>VDC</strong> is Nissan’s stability control. It brakes single wheels and can reduce engine power to help the car hold its line in a skid. The “VDC OFF” light comes on when the system is switched off, by the button or by a fault.</li>
<li><strong>SLIP</strong> is the traction and stability indicator. A short flash while driving on a slippery road means the system is working. A SLIP light that stays on with VDC OFF usually means the system has switched itself off because of a fault.</li>
</ul>
<p>VDC and traction control need the wheel speed signals and the actuator that ABS uses. When the ABS side has a fault, the car usually switches VDC off too, which is why the lights come on together.</p>
<h2>Is it safe to drive with the ABS, VDC and SLIP lights on?</h2>
<p>In most cases your normal brakes still work, but anti-lock braking, stability control and traction control may be switched off until the fault is fixed. The wheels can then lock under hard braking, and the car will not correct a skid on a wet road. Leave more distance and avoid hard stops. If the red brake warning light is also on, or the brake pedal feels different, stop driving and get the car checked first. Our pick-up and delivery service can collect it.</p>
<h2>Did someone press the VDC OFF button?</h2>
<p>If only the VDC OFF light is on, check the button first: on many Nissans it sits low on the dashboard, near the driver’s knee, and is easy to press by accident. Pressing it again usually turns the system back on. If the ABS light is on as well, or the lights stay on after a restart, there is a stored fault.</p>
<h2>Why can the check engine light come on as well?</h2>
<p>On many Nissan models, VDC is also switched off when the engine or gearbox reports a fault, because the system can no longer control engine power. So the VDC OFF and SLIP lights can come on with the check engine light even when the brakes are fine. That is why all the stored codes should be read, not just the ABS ones, before any part is changed.</p>
<h2>What are the common causes?</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has one. A dirty, damaged or failed sensor is a common cause.</li>
<li><strong>Wiring and connectors.</strong> Sensor wiring runs close to the wheels and can be damaged or corroded.</li>
<li><strong>Steering angle sensor.</strong> VDC needs to know where the steering is pointing. On some models the sensor needs resetting after a wheel alignment or steering work, or the VDC light can come on.</li>
<li><strong>Low brake fluid, a blown fuse or low battery voltage.</strong> Simple causes worth ruling out first.</li>
<li><strong>The ABS unit itself.</strong> The control module or the pump motor in the ABS actuator can develop internal faults.</li>
</ul>
<h2>How do we find which part is at fault?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ABS control unit stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> The VDC OFF button, sensors, wiring, fluid level, fuses and battery.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the module or pump, the ABS unit is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Repair, recon, used or new?</h2>
<p>If the fault is in the ABS unit, we can repair your own ABS module, or supply a reconditioned, used or new unit. Plug and play is available, and our repairs come with a 6-month warranty. See <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare, or <a href="../abs-warning-light-causes/">ABS warning light causes</a> for the ABS light on its own.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Why does the SLIP light flash while I am driving?', 'A short flash on a wet or slippery road means traction or stability control is working. If the SLIP light stays on with the VDC OFF light, the system has switched itself off, usually because of a stored fault.'),
             ('Will the ABS, VDC and SLIP lights go off by themselves?', 'Sometimes they go off after a restart if the fault is intermittent, but the code stays stored and the lights usually come back until the cause is fixed. Read the code first.'),
             ('Can you repair the ABS unit without the car?', 'Yes. You can bring just the unit to us at Premier @ Kaki Bukit, or use our pick-up and delivery service.')],
    ),
    dict(
        # EDGE daily article, 18 Oct 2026 (8pm run, by hand). Gap: for "vw audi abs esp light on" the results are US owners'
        # forums (audizine, audiworld, cargurus) and one UK mail-in seller page (ecutesting.com) that blames the pump alone;
        # no answer page and no Singapore workshop.
        slug='vw-audi-abs-esp-light-on', service='abs-pump-repair', date='2026-10-18', img_commit='149b8e72f958915d4e996861d283fb96193b3764',
        title='VW or Audi ABS and ESP Lights On? Causes | The ECU Clinic',
        desc='Why the ABS and ESP (ESC) lights come on together in a VW, Audi or Skoda, if it is safe to drive, what to check first, and ABS unit repair in Singapore.',
        h1='Why Are the ABS and ESP Lights On in My VW or Audi?',
        lead='ABS and ESP lights on together in a Volkswagen, Audi or Skoda? What each light means, the simple causes to rule out first, and when the ABS unit needs repair.',
        photo='abs-esc-units-bench', alt='ABS and ESC units on the workbench at The ECU Clinic', share='abs-esc-units-on-bench.jpg',
        body='''<p><strong>Short answer:</strong> in most Volkswagen, Audi and Skoda models, ABS (anti-lock brakes) and ESP (electronic stability programme, called ESC on newer cars) are run by the same ABS unit and use the same wheel speed signals, so one fault often turns on both lights. Common causes are a wheel speed sensor, the brake light switch, the steering angle sensor, low voltage or the ABS unit itself. The fault code tells you which.</p>
<h2>What do the ABS and ESP lights mean?</h2>
<ul class="ticks">
<li><strong>ABS</strong> is the anti-lock braking system. It stops the wheels locking when you brake hard.</li>
<li><strong>ESP</strong> (or ESC) is the stability system. It brakes single wheels and can reduce engine power to help the car hold its line in a skid. Traction control (ASR) is part of it. A light that flashes briefly on a slippery road means it is working; a light that stays on means it has switched itself off.</li>
</ul>
<p>ESP needs the wheel speed signals, the brake pressure reading and the pump that ABS uses. When the ABS side has a fault, the car switches ESP off too, which is why the two lights come on together.</p>
<h2>Is it safe to drive with the ABS and ESP lights on?</h2>
<p>In most cases your normal brakes still work, but anti-lock braking, stability control and traction control may be off until the fault is fixed. The wheels can then lock under hard braking, and the car will not correct a skid on a wet road. Leave more distance and avoid hard stops. If the red brake warning light is also on, or the brake pedal feels different, stop driving and get the car checked first. Our pick-up and delivery service can collect it.</p>
<h2>Did someone switch ESP off?</h2>
<p>On many models a button marked ESC, ESP or ASR OFF turns traction control off, and the ESP light or an "OFF" light then stays on. Press the button again, or restart the car, and it usually switches back on. If the ABS light is on as well, or the lights stay on after a restart, there is a stored fault.</p>
<h2>What are the common causes?</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has one. A dirty, damaged or failed sensor, or its wiring, is a common cause.</li>
<li><strong>Brake light switch.</strong> ESP uses it to know when you are braking, so a faulty switch can turn the ESP light on, sometimes with brake lights that stay on or do not work.</li>
<li><strong>Steering angle sensor.</strong> ESP needs to know where the steering is pointing. On many models the sensor must be set up again after a wheel alignment, steering work or a battery change, or the ESP light comes on.</li>
<li><strong>Low battery voltage or a blown fuse.</strong> Simple causes worth ruling out first, especially after a battery has gone flat.</li>
<li><strong>The ABS unit itself.</strong> The control module, the pump motor or a sensor inside the unit, such as the brake pressure sensor on many models, can develop internal faults.</li>
</ul>
<h2>How do we find which part is at fault?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ABS control unit stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> The ESC button, sensors, wiring, the brake light switch, steering angle setup, battery and fuses.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the module, the pump or a sensor inside the unit, the ABS unit is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Repair, recon, used or new?</h2>
<p>If the fault is in the ABS unit, we can repair your own ABS module, or supply a reconditioned, used or new unit. Our repairs come with a 6-month warranty. See <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare, or <a href="../abs-warning-light-causes/">ABS warning light causes</a> for the ABS light on its own.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Can a bad brake light switch turn on the ESP light?', 'Yes, on many Volkswagen and Audi models. ESP uses the switch to know when you brake, so a faulty switch can store a fault and turn the ESP light on. Reading the code shows whether the switch is the cause.'),
             ('Why did the ESP light come on after a wheel alignment or battery change?', 'On many models the steering angle sensor has to be set up again after alignment, steering work or a flat battery. Until it is, ESP may switch itself off and the light stays on.'),
             ('Can you repair the ABS unit without the car?', 'Yes. You can bring just the unit to us at Premier @ Kaki Bukit, or use our pick-up and delivery service.')],
    ),
    dict(
        slug='bmw-abs-dsc-light-on', service='abs-pump-repair', date='2026-10-19', img_commit='1490c0ca596d204d9117dff70d1c9d1ae7b76f62',
        title='BMW ABS and DSC Lights On? Causes | The ECU Clinic',
        desc='Why the ABS and DSC lights come on together in a BMW or Mini, whether it is safe to drive, what to check first, and BMW ABS unit repair in Singapore.',
        h1='Why Are the ABS and DSC Lights On in My BMW?',
        lead='ABS and DSC lights on together in a BMW or Mini? What each light means, the simple causes to rule out first, and when the ABS unit needs repair.',
        photo='abs-pump-in-car', alt='ABS pump and module in a car’s engine bay', share='abs-unit-engine-bay-1.jpg',
        body='''<p><strong>Short answer:</strong> on BMW and Mini cars, ABS (anti-lock brakes) and DSC (Dynamic Stability Control) are run by the same ABS/DSC unit and share the same wheel speed signals, so one fault usually turns on both lights, often with the brake warning too. Common causes are a wheel speed sensor, the steering angle sensor, the brake light switch, low battery voltage or the ABS/DSC unit itself. The fault code tells you which.</p>
<h2>What do the ABS and DSC lights mean?</h2>
<ul class="ticks">
<li><strong>ABS</strong> is the anti-lock braking system. It stops the wheels locking when you brake hard.</li>
<li><strong>DSC</strong> is BMW’s name for stability control. It brakes single wheels and can reduce engine power to help the car hold its line. A DSC light that flashes briefly on a slippery road means it is working; a light that stays on means the system has switched itself off.</li>
</ul>
<p>DSC needs the wheel speed signals and the pump and valves that ABS uses. When the ABS side has a fault, DSC is switched off too, which is why the two lights come on together.</p>
<h2>Is it safe to drive with the ABS and DSC lights on?</h2>
<p>In most cases your normal brakes still work, but anti-lock braking and stability control may be off until the fault is fixed. The wheels can then lock under hard braking, and the car will not correct a skid on a wet road. Leave more distance and avoid hard stops. If the red brake warning light is on, the brake pedal feels different or the brake fluid is low, stop driving and get the car checked first. Our pick-up and delivery service can collect it.</p>
<h2>Did someone press the DSC button?</h2>
<p>On many BMW models a short press of the DSC button switches to DTC (Dynamic Traction Control) and a long press switches DSC off, and a “DSC OFF” or traction light then stays on. Press the button again, or restart the car, and it usually switches back on. If the ABS light is on as well, or the lights stay on after a restart, there is a stored fault.</p>
<h2>What are the common causes?</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has one. A dirty, damaged or failed sensor, or its wiring, is the most common cause.</li>
<li><strong>Steering angle sensor.</strong> DSC needs to know where the steering is pointing. On many models it must be set up again after a wheel alignment, steering work or a battery change.</li>
<li><strong>Brake light switch.</strong> DSC uses it to know when you are braking, so a faulty switch can turn the lights on.</li>
<li><strong>Low battery voltage.</strong> A weak battery, or one that has just gone flat, can make several modules store faults at once.</li>
<li><strong>The ABS/DSC unit itself.</strong> The control module, the pump motor or a sensor inside the unit can develop internal faults.</li>
</ul>
<p>A separate orange or yellow brake pad warning on many BMW models comes from the pad wear sensor, not the ABS unit.</p>
<h2>How do we find which part is at fault?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ABS/DSC unit stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> The DSC button, sensors, wiring, the brake light switch, steering angle setup, battery and fuses.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the module, the pump or a sensor inside the unit, the ABS/DSC unit is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Can the ABS/DSC unit be repaired?</h2>
<p>Often, yes. We repair ABS units for BMW and Mini as well as other makes, and explain the options before any work starts. Our repairs come with a 6-month warranty. See <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare, or <a href="../abs-warning-light-causes/">ABS warning light causes</a> for the ABS light on its own.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Can a weak battery turn on the ABS and DSC lights in a BMW?', 'Yes. Low voltage can make the ABS/DSC unit and other modules store faults. If the lights came on after a flat battery or a jump start, have the battery checked and the codes read before replacing parts.'),
             ('Why did the DSC light come on after a wheel alignment or battery change?', 'On many models the steering angle sensor has to be set up again after alignment, steering work or a flat battery. Until it is, DSC may switch itself off and the light stays on.'),
             ('Do I need to bring the whole car?', 'No. You can bring just the ABS unit to us at Premier @ Kaki Bukit, or use our pick-up and delivery service for the car.')],
    ),
    dict(
        # EDGE daily article, 20 Oct 2026 (8pm run). Make series (Hyundai/Kia, Toyota, Nissan, VW/Audi, BMW done): Honda's general
        # "ABS + VSA lights" question; the code articles (81-19, 121-11) stay the owners of their codes and are linked from here.
        slug='honda-abs-vsa-light-on', service='abs-pump-repair', date='2026-10-20', img_commit='6b208e2e80166158ff8903d4631487949185d6df',
        title='Honda ABS and VSA Lights On? Causes | The ECU Clinic',
        desc='Why the ABS and VSA lights come on together in a Honda, whether it is safe to drive, the simple causes to rule out first, and Honda ABS repair in Singapore.',
        h1='Why Are the ABS and VSA Lights On in My Honda?',
        lead='ABS and VSA lights on together in a Honda? What each light means, the simple causes to rule out first, and when the ABS (VSA modulator) unit needs repair.',
        photo='honda-vsa-fault-codes', alt='Scan tool showing a Honda VSA fault code read at The ECU Clinic', share='honda-vezel-vsa-fault-codes.jpg',
        body='''<p><strong>Short answer:</strong> on Honda cars, ABS (anti-lock brakes) and VSA (Vehicle Stability Assist, Honda’s stability control) share one unit in the engine bay, often called the VSA modulator, and use the same wheel speed signals. So one fault usually turns on both lights, sometimes with the brake warning too. Common causes are a wheel speed sensor, low battery voltage, the brake light switch or a fault inside the ABS/VSA unit itself. The fault code tells you which.</p>
<h2>What do the ABS and VSA lights mean?</h2>
<ul class="ticks">
<li><strong>ABS</strong> is the anti-lock braking system. It stops the wheels locking when you brake hard.</li>
<li><strong>VSA</strong> is Honda’s stability and traction control. It brakes single wheels and can reduce engine power to help the car hold its line. A VSA light that flashes briefly on a slippery road means it is working; a light that stays on means the system has switched itself off.</li>
</ul>
<p>VSA needs the wheel speed signals and the pump and valves that ABS uses. When the ABS side has a fault, VSA is switched off too, which is why the two lights come on together.</p>
<h2>Is it safe to drive with the ABS and VSA lights on?</h2>
<p>In most cases your normal brakes still work, but anti-lock braking and stability control may be off until the fault is fixed. The wheels can then lock under hard braking, and the car will not correct a skid on a wet road. Leave more distance and avoid hard stops. If the red brake warning light is on, the brake pedal feels different or the brake fluid is low, stop driving and get the car checked first. Our pick-up and delivery service can collect it.</p>
<h2>Did someone press the VSA OFF button?</h2>
<p>Many Honda models have a VSA OFF button. When it is pressed, a “VSA OFF” light stays on. Press the button again, or restart the car, and VSA usually switches back on. If the ABS light is on as well, or the lights stay on after a restart, there is a stored fault.</p>
<h2>What are the common causes?</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has one. A dirty, damaged or failed sensor, or its wiring, is a common cause.</li>
<li><strong>Low battery voltage.</strong> A weak battery, or one that has just gone flat, can make several modules store faults at once.</li>
<li><strong>Brake light switch.</strong> VSA uses it to know when you are braking, so a faulty switch can turn the lights on.</li>
<li><strong>The ABS/VSA unit itself.</strong> Faults inside the unit are among the Honda ABS faults we handle most often, for example <a href="../honda-vsa-solenoid-valve-malfunction/">121-11 VSA Solenoid Valve Malfunction</a> and the <a href="../honda-yaw-rate-sensor-malfunction/">81-19 yaw rate sensor</a> code for the sensor inside the modulator.</li>
</ul>
<p>When the VSA unit has a fault, other systems that take information from it, such as the electric parking brake and power steering, can show their own warnings too.</p>
<h2>How do we find which part is at fault?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ABS/VSA unit stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> The VSA OFF button, sensors, wiring, the brake light switch, battery and fuses.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the module, the pump or a sensor inside the unit, the ABS/VSA unit is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Repair, used or new?</h2>
<p>If the fault is in the ABS unit, we can repair your own Honda ABS module, or supply a used unit. Our repairs come with a 6-month warranty. See <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare, or <a href="../abs-warning-light-causes/">ABS warning light causes</a> for the ABS light on its own.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Why do the ABS, VSA and brake lights all come on in my Honda?', 'ABS and VSA share one unit, and the brake system warning can come on with them when that unit has a fault. Reading the fault code shows which part is the cause. If the brake pedal feels different or the fluid is low, stop driving first.'),
             ('Will the ABS and VSA lights go off by themselves?', 'Sometimes they go off after a restart if the fault is intermittent, but the code stays stored and the lights usually come back until the cause is fixed. Read the code first.'),
             ('Can you repair the ABS unit without the car?', 'Yes. You can bring just the unit to us at Premier @ Kaki Bukit, or use our pick-up and delivery service.')],
    ),
    dict(
        # Catch-up article dated 21 Oct 2026 (odd-day article missed when the every-2-days cadence began). Make series (Hyundai/Kia, Toyota,
        # Nissan, VW/Audi, BMW, Honda done): Chevrolet is named in content.md for ABS repair and used ABS pumps/modules.
        slug='chevrolet-abs-esc-light-on', service='abs-pump-repair', date='2026-10-21', img_commit='59f5037b0c1156a01f2eb042dc1162ac70e2f1fa',
        title='Chevrolet ABS and ESC Lights On? Causes | The ECU Clinic',
        desc='Why the ABS and traction or stability control lights come on in a Chevrolet, whether it is safe to drive, what to check first, and ABS repair in Singapore.',
        h1='Why Are the ABS and Traction Control Lights On in My Chevrolet?',
        lead='ABS and traction or stability control lights on in a Chevrolet? What the lights mean, the simple causes to rule out first, and when the ABS module needs repair.',
        photo='abs-pump-in-car', alt='ABS pump and module in a car’s engine bay', share='abs-unit-engine-bay-1.jpg',
        body='''<p><strong>Short answer:</strong> on a Chevrolet, ABS (anti-lock brakes) and the traction or stability control system (ESC) share the same brake control module and the same wheel speed signals, so one fault often turns on more than one light. Common causes are a wheel speed sensor or its wiring, low battery voltage, the brake light switch, or a fault in the ABS module itself. The fault code tells you which, and we repair Chevrolet ABS units in Singapore.</p>
<h2>What do the ABS and traction control lights mean?</h2>
<ul class="ticks">
<li><strong>ABS</strong> is the anti-lock braking system. It stops the wheels locking when you brake hard.</li>
<li><strong>Traction or stability control</strong> brakes single wheels and can reduce engine power to help the car grip or hold its line. The light flashes briefly when it is working on a slippery road. A light that stays on means the system has switched itself off, or has a fault.</li>
</ul>
<p>Stability control needs the wheel speed signals and the pump and valves that ABS uses. When the ABS side has a fault, stability control is usually switched off too, which is why the lights often come on together.</p>
<h2>Is it safe to drive with the ABS and traction control lights on?</h2>
<p>In most cases your normal brakes still work, but anti-lock braking and stability control may be off until the fault is fixed. The wheels can then lock under hard braking, and the car will not correct a skid on a wet road. Leave more distance and avoid hard stops. If the red brake warning light is on, the brake pedal feels different or the brake fluid is low, stop driving and get the car checked first. Our pick-up and delivery service can collect it.</p>
<h2>Did someone press the traction control button?</h2>
<p>Many Chevrolet models have a button that switches traction control off, and a light then stays on. Press the button again, or restart the car, and the system usually switches back on. If the ABS light is on as well, or the lights stay on after a restart, there is a stored fault.</p>
<h2>What are the common causes?</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has one. A dirty, damaged or failed sensor, or its wiring, is a common cause.</li>
<li><strong>Low battery voltage.</strong> A weak battery, or one that has just gone flat, can make several modules store faults at once.</li>
<li><strong>Brake light switch.</strong> The system uses it to know when you are braking, so a faulty switch can turn the lights on.</li>
<li><strong>Steering angle or other sensors.</strong> Stability control also reads the steering angle, so a fault in that signal can switch it off.</li>
<li><strong>The ABS module itself.</strong> The control module, the pump motor or a sensor inside the unit can develop internal faults. This is the cause when the simple checks come back clean.</li>
</ul>
<h2>How do we find which part is at fault?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ABS module stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> The traction control button, sensors, wiring, the brake light switch, battery and fuses.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the module, the pump or a sensor inside the unit, the ABS module is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Repair, used or new?</h2>
<p>If the fault is in the ABS unit, we can repair your own Chevrolet ABS module, or supply a used unit. Our repairs come with a 6-month warranty. See <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare, or <a href="../abs-warning-light-causes/">ABS warning light causes</a> for the ABS light on its own.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Can a weak battery turn on the ABS and traction control lights in a Chevrolet?', 'Yes. Low voltage can make the ABS module and other modules store faults. If the lights came on after a flat battery or a jump start, have the battery checked and the codes read before replacing parts.'),
             ('Will the lights go off by themselves?', 'Sometimes they go off after a restart if the fault is intermittent, but the code stays stored and the lights usually come back until the cause is fixed. Read the code first.'),
             ('Do I need to bring the whole car?', 'No. You can bring just the ABS unit to us at Premier @ Kaki Bukit, or use our pick-up and delivery service for the car.')],
    ),
    dict(
        # Night article dated 23 Oct 2026. Make series (Hyundai/Kia, Toyota, Nissan, VW/Audi, BMW, Honda, Chevrolet done): Volvo is named in
        # content.md for used ABS pumps and ABS module repair only, so the article says "used ABS unit" and "ABS module repair", nothing more.
        slug='volvo-abs-dstc-light-on', service='abs-pump-repair', date='2026-10-23', img_commit='eabc77ebbddffba696ab81d1eb694679e1a0e70b',
        title='Volvo ABS and DSTC Lights On? Causes | The ECU Clinic',
        desc='Why the ABS and DSTC or stability and traction control lights come on in a Volvo, whether it is safe to drive, what to check first, and ABS module repair in Singapore.',
        h1='Why Are the ABS and DSTC Lights On in My Volvo?',
        lead='ABS and DSTC (stability and traction control) lights on in a Volvo? What they mean, the simple causes to rule out first, and when the ABS module needs repair.',
        photo='abs-pump-in-car', alt='ABS pump and module in a car’s engine bay', share='abs-unit-engine-bay-1.jpg',
        body='''<p><strong>Short answer:</strong> in a Volvo, ABS (anti-lock brakes) and the stability and traction control system, which Volvo calls DSTC on many models, use the same wheel speed signals and the same brake control module, so one fault often turns on more than one light or message. Common causes are a wheel speed sensor or its wiring, low battery voltage, the brake light switch, or a fault in the ABS module itself. The fault code tells you which. We repair ABS modules and supply used ABS units for Volvo in Singapore.</p>
<h2>What do the ABS and DSTC lights mean?</h2>
<ul class="ticks">
<li><strong>ABS</strong> is the anti-lock braking system. It stops the wheels locking when you brake hard.</li>
<li><strong>DSTC</strong> (Dynamic Stability and Traction Control) brakes single wheels and can reduce engine power to help the car grip or hold its line. The exact wording and symbol depend on the model and year: some cars show a stability or traction control message instead. The light flashes briefly when the system is working on a slippery road. A light or message that stays on means the system has switched itself off, or has a fault.</li>
</ul>
<p>Stability control needs the wheel speed signals and the pump and valves that ABS uses. When the ABS side has a fault, stability control is usually switched off too, which is why the lights often come on together.</p>
<h2>Is it safe to drive with the ABS and DSTC lights on?</h2>
<p>In most cases your normal brakes still work, but anti-lock braking and stability control may be off until the fault is fixed. The wheels can then lock under hard braking, and the car will not correct a skid on a wet road. Leave more distance and avoid hard stops. If the red brake warning light is on, the brake pedal feels different or the brake fluid is low, stop driving and get the car checked first. Our pick-up and delivery service can collect it.</p>
<h2>Did someone press the DSTC button?</h2>
<p>Many Volvo models have a button that switches stability control off or to a reduced mode, and a light then stays on. Press the button again, or restart the car, and the system usually switches back on. If the ABS light is on as well, or the lights stay on after a restart, there is a stored fault.</p>
<h2>What are the common causes?</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has one. A dirty, damaged or failed sensor, or its wiring, is a common cause.</li>
<li><strong>Low battery voltage.</strong> A weak battery, or one that has just gone flat, can make several modules store faults at once.</li>
<li><strong>Brake light switch.</strong> The system uses it to know when you are braking, so a faulty switch can turn the lights on.</li>
<li><strong>Steering angle or other sensors.</strong> Stability control also reads the steering angle, so a fault in that signal can switch it off.</li>
<li><strong>The ABS module itself.</strong> The control module, the pump motor or a sensor inside the unit can develop internal faults. This is the cause when the simple checks come back clean.</li>
</ul>
<h2>How do we find which part is at fault?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ABS module stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> The stability control button, sensors, wiring, the brake light switch, battery and fuses.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the module, the pump or a sensor inside the unit, the ABS module is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Repair, used or new?</h2>
<p>If the fault is in the ABS unit, we can repair your own Volvo ABS module, or supply a used ABS unit. Our repairs come with a 6-month warranty. See <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare, or <a href="../abs-warning-light-causes/">ABS warning light causes</a> for the ABS light on its own.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Can a weak battery turn on the ABS and DSTC lights in a Volvo?', 'Yes. Low voltage can make the ABS module and other modules store faults. If the lights came on after a flat battery or a jump start, have the battery checked and the codes read before replacing parts.'),
             ('Will the lights go off by themselves?', 'Sometimes they go off after a restart if the fault is intermittent, but the code stays stored and the lights usually come back until the cause is fixed. Read the code first.'),
             ('Do I need to bring the whole car?', 'No. You can bring just the ABS unit to us at Premier @ Kaki Bukit, or use our pick-up and delivery service for the car.')],
    ),
    dict(
        # Night article dated 25 Oct 2026. Make series: Mercedes-Benz. Mercedes has a message article (Active Brake Assist functions limited) and a
        # fault-code article (N30/4 5001); this one owns the general "ABS and ESP lights on in a Mercedes" intent and links down to both.
        # Client facts: Mercedes ABS repair, used ABS pump and ABS module repair, Mercedes ESP pump repair (content.md).
        slug='mercedes-abs-esp-light-on', service='abs-pump-repair', date='2026-10-25', img_commit='9c65549ccba1858dc9c715548780adcd16ff2b29',
        title='Mercedes ABS and ESP Lights On? Causes | The ECU Clinic',
        desc='Why the ABS and ESP lights come on in a Mercedes-Benz, whether it is safe to drive, what to check first, and ESP pump and ABS module repair in Singapore.',
        h1='Why Are the ABS and ESP Lights On in My Mercedes-Benz?',
        lead='ABS and ESP lights on in a Mercedes-Benz? What they mean, the simple causes to rule out first, and when the ESP pump and module need repair.',
        photo='mercedes-esp-pumps', alt='Mercedes-Benz ESP pump and module units on the bench', share='mercedes-esp-pumps.jpg',
        body='''<p><strong>Short answer:</strong> in a Mercedes-Benz, ABS (anti-lock brakes), ESP (Electronic Stability Program) and, on many models, brake assist (BAS) all work through the same ESP pump and control unit, so one fault often turns on more than one light or message. Common causes are a wheel speed sensor or its wiring, a steering angle sensor, low battery voltage, the brake light switch, or a fault in the ESP unit itself. The fault code tells you which. We repair Mercedes ESP pumps and ABS modules in Singapore.</p>
<h2>What do the ABS and ESP lights mean?</h2>
<ul class="ticks">
<li><strong>ABS</strong> is the anti-lock braking system. It stops the wheels locking when you brake hard.</li>
<li><strong>ESP</strong> brakes single wheels and can reduce engine power to help the car hold its line. The light flashes briefly when the system is working on a slippery road. A light that stays on means ESP has switched itself off, or has a fault.</li>
<li><strong>BAS</strong> (brake assist) adds braking force in an emergency stop. On newer models you may see a message such as “Active Brake Assist functions limited” instead. That message has its own page: <a href="../mercedes-active-brake-assist-functions-limited/">Active Brake Assist functions limited</a>.</li>
</ul>
<p>Stability control needs the wheel speed signals and the pump and valves that ABS uses. When the ABS side has a fault, ESP is usually switched off too, which is why the lights often come on together.</p>
<h2>Is it safe to drive with the ABS and ESP lights on?</h2>
<p>In most cases your normal brakes still work, but anti-lock braking and stability control may be off until the fault is fixed. The wheels can then lock under hard braking, and the car will not correct a skid on a wet road. Leave more distance and avoid hard stops. If the red brake warning light is on, the brake pedal feels different or the brake fluid is low, stop driving and get the car checked first. Our pick-up and delivery service can collect it.</p>
<h2>Did someone press the ESP button?</h2>
<p>Many Mercedes-Benz models have a button that switches ESP off, and a light then stays on. Press the button again, or restart the car, and the system usually switches back on. If the ABS light is on as well, or the lights stay on after a restart, there is a stored fault.</p>
<h2>What are the common causes?</h2>
<ul class="ticks">
<li><strong>Wheel speed sensor.</strong> Each wheel has one. A dirty, damaged or failed sensor, or its wiring, is a common cause.</li>
<li><strong>Low battery voltage.</strong> A weak battery, or one that has just gone flat, can make several modules store faults at once.</li>
<li><strong>Brake light switch.</strong> The system uses it to know when you are braking, so a faulty switch can turn the lights on.</li>
<li><strong>Steering angle or other sensors.</strong> ESP also reads the steering angle, so a fault in that signal can switch it off.</li>
<li><strong>The ESP pump and control unit.</strong> The control module, the pump motor or a sensor inside the unit can develop internal faults. This is the cause when the simple checks come back clean. One example is the code “internal fault in component N30/4”, explained on <a href="../mercedes-esp-control-unit-fault-n30-4/">Mercedes ESP fault N30/4 (5001)</a>.</li>
</ul>
<h2>How do we find which part is at fault?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ESP unit stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> The ESP button, sensors, wiring, the brake light switch, battery and fuses.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the control module, the pump or a sensor inside the unit, the ESP unit is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Repair, used or new?</h2>
<p>If the fault is in the ESP unit, we can repair your own Mercedes ESP pump and module, or supply a used ABS unit. Our repairs come with a 6-month warranty. See <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare, or <a href="../abs-warning-light-causes/">ABS warning light causes</a> for the ABS light on its own.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Can a weak battery turn on the ABS and ESP lights in a Mercedes-Benz?', 'Yes. Low voltage can make the ESP unit and other modules store faults. If the lights came on after a flat battery or a jump start, have the battery checked and the codes read before replacing parts.'),
             ('Will the lights go off by themselves?', 'Sometimes they go off after a restart if the fault is intermittent, but the code stays stored and the lights usually come back until the cause is fixed. Read the code first.'),
             ('Do I need to bring the whole car?', 'No. You can bring just the ESP pump or ABS unit to us at Premier @ Kaki Bukit, or use our pick-up and delivery service for the car.')],
    ),
    dict(
        # Night article dated 27 Oct 2026. New intent (not a make-series article): ABS pump noise / buzzing / pedal pulsing when braking, normal or fault.
        # No client fact beyond: ABS pump and module repair, used ABS units, 6-month warranty, pick-up and delivery. General knowledge is hedged.
        slug='abs-pump-noise-buzzing-when-braking', service='abs-pump-repair', date='2026-10-27', img_commit='72ce95c65946f40493773a5153f46d087d03e37c',
        title='ABS Pump Buzzing or Noisy When Braking? Normal or Fault | The ECU Clinic',
        desc='Why the ABS pump buzzes, clicks or pulses the brake pedal when braking, when that is normal, when it points to a fault, and what to do next in Singapore.',
        h1='Why Does My ABS Pump Buzz or Make Noise When Braking?',
        lead='A buzz, click or pulsing pedal when you brake hard is often the ABS doing its job. Here is how to tell normal from a fault.',
        photo='abs-pump-in-car', alt='ABS pump and module in a car’s engine bay', share='abs-unit-engine-bay-1.jpg',
        body='''<p><strong>Short answer:</strong> a buzzing, clicking or grinding sound from the engine bay, together with a pulsing brake pedal, during a hard stop or on a wet or loose road is usually the ABS working normally. It is worth checking when the ABS light is on, when the noise happens in ordinary light braking, when the pump keeps running after you stop, or when the pedal feels different. A fault code shows whether the ABS unit is at fault.</p>
<h2>When is ABS pump noise normal?</h2>
<ul class="ticks">
<li><strong>Hard braking or a slippery road.</strong> When a wheel is about to lock, the ABS releases and re-applies brake pressure many times a second. You can hear a buzz, a rattle or a grinding sound and feel the pedal pulse under your foot. This is the system working.</li>
<li><strong>A short hum or click after starting or moving off.</strong> Many cars run a brief self-check of the ABS pump and valves. It is usually over in a second or two. Makers differ, so your owner’s manual is the best guide for your car.</li>
</ul>
<h2>When may the noise point to a fault?</h2>
<ul class="ticks">
<li><strong>The ABS light is on</strong> (or the ESP, ESC or traction control light with it). The system has stored a fault. See <a href="../abs-warning-light-causes/">ABS warning light causes</a>.</li>
<li><strong>The noise or pulsing happens in normal, gentle braking</strong> on a dry road.</li>
<li><strong>The pump motor keeps running</strong> or buzzes for a long time after you stop, or each time you switch on.</li>
<li><strong>The brake pedal feels different:</strong> unusually hard, soft or sinking.</li>
</ul>
<p>If the red brake warning light is on, the pedal feels different or the brake fluid is low, stop driving and get the car checked. Our pick-up and delivery service can collect it.</p>
<h2>What else can make noise or pulsing when braking?</h2>
<p>Not every noise comes from the ABS unit. Worn brake pads, rough or uneven brake discs, a dirty or damaged wheel speed sensor or a worn wheel bearing can also cause grinding, squealing or a pulsing pedal. That is why it is better to read the fault codes first than to replace parts by guesswork.</p>
<h2>How do we find the cause?</h2>
<ol class="steps">
<li><strong>Read the fault codes.</strong> The ABS module stores codes that point to the circuit at fault.</li>
<li><strong>Rule out the simple causes.</strong> Brake pads and discs, wheel speed sensors and their wiring, brake fluid level, battery and fuses.</li>
<li><strong>Check the unit.</strong> If the codes and tests point to the pump motor, the valves or the control module, the ABS unit is the problem.</li>
<li><strong>Tell you the options.</strong> You decide before any work starts.</li>
</ol>
<h2>Repair, used or new?</h2>
<p>If the fault is in the ABS unit, we can repair your own ABS pump and module, or supply a used ABS unit. Our repairs come with a 6-month warranty. See <a href="../../services/abs-pump-repair/">ABS pump and module repair</a> for how the options compare.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year, chassis number and the fault codes. A photo of the dashboard or the scan tool screen also helps, and a short description of when the noise happens. You can bring the car, or just the unit, to Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Is it normal for the ABS to buzz and the brake pedal to pulse?', 'Yes, during a hard stop or on a wet or loose surface the ABS can buzz and pulse the pedal as it stops the wheels locking. If it happens in normal braking, or the ABS light is on, have the codes read.'),
             ('Why does my ABS pump make a noise when I start the car?', 'Many cars run a short self-check of the ABS pump and valves after starting or when first moving off, which can sound like a brief hum or click. A noise that is long, loud or comes with a warning light is worth checking.'),
             ('Can I keep driving if the ABS pump is noisy?', 'If the ABS light is off and the brakes feel normal, it is probably the ABS working. If the light is on, expect the anti-lock function to be off, so leave more distance and avoid hard stops. If the red brake light is on or the pedal feels different, stop driving.')],
    ),
    dict(
        # Night article dated 29 Oct 2026. New intent (not a make-series article): is a BMW running at 100-120 C normal.
        # Client facts only: many BMWs of 2010-2018 run 120C+; we reprogram the engine's temperature setting to about 95C; models list on the
        # BMW temperature programming page; no "100% safe" claim. General knowledge is hedged. No prices.
        slug='bmw-coolant-temperature-120-normal', service='bmw-temperature-programming', date='2026-10-29', img_commit='6b2463ab3492e899fe89301b7208a1d5c5538679',
        title='BMW Running at 120°C? Is Coolant Temperature Normal | The ECU Clinic',
        desc='Is it normal for a BMW to show 100 to 120°C on the temperature display? What is usually normal, the warning signs, and what temperature programming does.',
        h1='Is It Normal for a BMW to Run at 120°C?',
        lead='Seeing 110 or 120°C in iDrive or on the engine temperature display? Here is what is usually normal, what is not, and your options.',
        photo='bmw-fault-code-scan', alt='Scan tool reading BMW engine data and fault codes', share='diagnostic-bmw-fault-codes.jpg',
        body='''<p><strong>Short answer:</strong> many BMWs are designed to run hotter than older cars, and a reading of about 100 to 110°C is common. A reading of 120°C or more is higher than most owners expect, even if there is no warning light. It is worth a cooling system check if the reading keeps climbing, a warning message appears or you lose coolant. If the car is not overheating, some owners choose to have the temperature setting reprogrammed so the engine runs nearer 95°C.</p>
<h2>Why do many BMWs run so hot?</h2>
<p>Many modern BMWs use an electronically controlled thermostat. The engine control unit can let the coolant run hotter under light load, which helps fuel economy and emissions, and run cooler when you drive hard. The temperature you see can therefore change a lot during one trip. The exact setting depends on the model and engine, so your owner’s manual is the best guide for your car.</p>
<h2>When is the temperature a warning sign?</h2>
<ul class="ticks">
<li><strong>A warning message</strong> or a red temperature light is on. Stop in a safe place and let the engine cool.</li>
<li><strong>The reading keeps climbing</strong> in traffic or on a normal drive, or it jumps up and down.</li>
<li><strong>The coolant level drops,</strong> or you see a leak, steam or a sweet smell.</li>
<li><strong>The heater blows cold</strong> or the cooling fans run all the time.</li>
</ul>
<p>Do not keep driving an engine that is overheating. If any of these apply, have the car checked before you think about programming.</p>
<h2>What can make a BMW run hotter than it should?</h2>
<ul class="ticks">
<li><strong>Thermostat.</strong> A thermostat that sticks, or its electric heater, can keep the engine hotter than intended.</li>
<li><strong>Water pump and fans.</strong> A weak pump or a slow fan reduces the cooling.</li>
<li><strong>Coolant level, leaks or old coolant.</strong> Low or poor coolant cools less well.</li>
<li><strong>A blocked radiator</strong> or air in the system after a repair.</li>
</ul>
<h2>What is BMW temperature programming?</h2>
<p>Many BMWs from this period run at a high coolant temperature, often 120°C or more. We reprogram the engine’s temperature setting so it runs at about 95°C instead, for steady performance and long-term engine protection. Daily driving and the car’s other functions are not changed. It covers most BMW models from 2010 to 2018, including the 1 to 8 Series, X1 to X6, M2 and Z4.</p>
<p>Programming changes the temperature the engine control unit aims for. It does not repair a leak, a faulty thermostat or a failing pump, so fix any real cooling fault first. See <a href="../../services/bmw-temperature-programming/">BMW temperature programming</a> for the full list of models.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your BMW model and year, and tell us what temperature you see and when. If there is a warning message or fault codes, send a photo of the dashboard or the scan tool screen. We will tell you whether your model is on the list. You can bring the car to Premier @ Kaki Bukit.</p>''',
        faq=[('Is 110°C normal for a BMW?', 'On many modern BMWs, readings of about 100 to 110°C are common because the engine control unit lets the coolant run hotter under light load. Check your owner’s manual for your model, and have the car checked if a warning message appears or the reading keeps climbing.'),
             ('Is it safe to keep driving if my BMW shows 120°C?', 'If there is no warning light or message and the coolant level is steady, the car may be running as designed, but 120°C is high and worth checking. If a warning appears, stop in a safe place and let the engine cool. Do not keep driving an overheating engine.'),
             ('Which BMWs can have temperature programming?', 'Most BMW models from 2010 to 2018, including the 1 to 8 Series, X1 to X6, M2 and Z4. WhatsApp us your model and year to confirm.')],
    ),
    dict(
        # Real job photos from Edwin, 29 Oct 2026. Edwin did not say what the fix was, so this is DIAGNOSIS ONLY:
        # never claim a repair, cost or time. Airbag/SRS/NECK-PRO repair is NOT a confirmed ECU Clinic service (no service page).
        slug='mercedes-airbag-light-neck-pro-b1c1113', service=None, date='2026-10-29', img_commit='3d936a900680ddbeabd5b521b9e2e6031792d016',
        title='Mercedes Airbag Light: NECK-PRO B1C1113 and B1C1713 | The ECU Clinic',
        desc='A Mercedes C-Class with the airbag light on and "Front left malfunction, Consult workshop". What the NECK-PRO codes B1C1113 and B1C1713 mean and what to do.',
        h1='Mercedes Airbag Light On: NECK-PRO Codes B1C1113 and B1C1713',
        lead='A real job from our workshop: a Mercedes-Benz C-Class with the airbag light on and “Front left malfunction, Consult workshop”. Here is what the scan showed.',
        photo='mercedes-srs-neck-pro-codes', alt='Scan tool showing Mercedes SRS codes B1C1113 and B1C1713, NECK-PRO head restraint open circuit',
        share='mercedes-airbag-warning-cluster.jpg',
        body='''<p><strong>Short answer:</strong> on this Mercedes-Benz C-Class the airbag light and the message “Front left malfunction, Consult workshop” came with two stored airbag (SRS) codes: <strong>B1C1113</strong> and <strong>B1C1713</strong>. Both say the NECK-PRO head restraint has an open circuit, one for the driver’s seat and one for the front passenger seat. The scan tool tells you which circuit to check before anything is replaced.</p>
<h2>What the car showed</h2>
<p>The instrument cluster showed the red airbag warning light and the message <em>“Front left malfunction, Consult workshop”</em>.</p>
<p><img src="{img_cluster}" alt="Mercedes C-Class instrument cluster with the airbag light and the message Front left malfunction, Consult workshop" width="1200" height="585" loading="lazy" style="width:100%;height:auto;border-radius:12px"></p>
<h2>What the scan tool found</h2>
<p>A full scan of all control units showed these codes in the SRS (Supplemental Inflatable Restraint System) module, both <em>current and stored</em>:</p>
<ul class="ticks">
<li><strong>B1C1113</strong>: the NECK-PRO head restraint “Driver” has a malfunction. There is an open circuit.</li>
<li><strong>B1C1713</strong>: the NECK-PRO head restraint “Front passenger” has a malfunction. There is an open circuit.</li>
</ul>
<p>The same scan also listed faults in other modules that have nothing to do with the airbag light: a navigation data fault in the COMAND audio unit (9549) and a mirror adjustment output fault in the left front door module. That is why we scan every module, not only the one with the warning light.</p>
<h2>What is NECK-PRO?</h2>
<p>NECK-PRO is the Mercedes-Benz name for the front head restraints that move forward in a rear-end collision, to reduce the risk of whiplash. They are part of the restraint system, so the airbag (SRS) control unit monitors their circuits. When it sees an open circuit, it stores a code and turns on the airbag light.</p>
<h2>What does “open circuit” mean?</h2>
<p>The control unit is not seeing the electrical connection it expects. In general this points to the release unit in the head restraint, or the wiring and connectors between the seat and the car. The code tells you which seat; it does not on its own tell you which of these is at fault. Testing is needed before any part is replaced.</p>
<h2>Is it safe to drive with the airbag light on?</h2>
<p>While the airbag light is on, the restraint system has a stored fault, and parts of it may not work as designed in a crash. Get it checked soon. Airbag parts must only be tested with the right equipment: probing airbag circuits with a test lamp or multimeter can be dangerous.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year and the fault codes, with a photo of the dashboard message or the scan tool screen. We will tell you whether it is a job we can take on. You can find us at Premier @ Kaki Bukit.</p>''',
        faq=[('What do Mercedes codes B1C1113 and B1C1713 mean?', 'On this car the scan tool described them as an open circuit in the NECK-PRO head restraint: B1C1113 for the driver’s seat and B1C1713 for the front passenger seat.'),
             ('Why does my Mercedes say “Front left malfunction, Consult workshop”?', 'On this C-Class the message came with the airbag light and stored SRS codes. Read the codes with a scan tool to see which part of the restraint system the airbag control unit is reporting.'),
             ('Can I clear the airbag light myself?', 'Clearing the codes does not fix an open circuit. If the fault is still there, the light comes back. Find the cause first.')],
    ),
    dict(
        # Real job photos from Edwin, 30 Oct 2026: scan (C1391, C13A9) plus a NEW brake actuator 44510-30290 next to the
        # removed original. Published: new actuator fitted. No price, time, warranty term or test-drive result was given:
        # do not add any. Plate, VIN and scanner serial are removed from the photos.
        slug='toyota-alphard-hybrid-c1391-brake-actuator', service='abs-pump-repair', date='2026-10-30', img_commit='987e39dbd9078e72b25c09135f6a79d79384b86c',
        title='Toyota Alphard Hybrid C1391 Accumulator Leak: Brake Actuator | The ECU Clinic',
        desc='A 2020 Toyota Alphard / Vellfire Hybrid with C1391 "Abnormal Leak in Accumulator" and C13A9. What the codes mean and the new brake actuator 44510-30290 we fitted.',
        h1='Toyota Alphard Hybrid C1391 “Abnormal Leak in Accumulator”: New Brake Actuator Fitted',
        lead='A real job from our workshop: a 2020 Toyota Alphard / Vellfire Hybrid (2AR-FXE) with brake codes C1391 and C13A9. Here is what the scan showed and what we fitted.',
        photo='toyota-alphard-old-vs-new-actuator', alt='New Toyota brake actuator 44510-30290 next to the original unit removed from a Toyota Alphard Hybrid',
        share='toyota-alphard-old-vs-new-brake-actuator.jpg',
        body='''<p><strong>Short answer:</strong> on this 2020 Toyota Alphard / Vellfire Hybrid the scan tool found <strong>C1391 “Abnormal Leak in Accumulator”</strong> in the ABS / VSC / TRC system and <strong>C13A9 “Brake System Malfunction”</strong> under the electronic parking brake. Both point to the hybrid brake system. We replaced the brake actuator with a new unit, part number <strong>44510-30290</strong>.</p>
<h2>What the scan tool found</h2>
<p>A full system scan of the car (Alphard HV / Vellfire HV, 2AR-FXE hybrid engine) showed two systems with one fault each. The engine, hybrid control and OBD systems were all normal.</p>
<p><img src="{img:toyota-alphard-abs-codes}" alt="Scan tool on a Toyota Alphard Hybrid showing C1391 Abnormal Leak in Accumulator and C13A9 Brake System Malfunction" width="640" height="480" loading="lazy" style="width:100%;height:auto;border-radius:12px"></p>
<ul class="ticks">
<li><strong>C1391 Abnormal Leak in Accumulator</strong>: stored in the Anti-lock Braking System (ABS) / Vehicle Stability Control (VSC) / Traction Control (TRC) system.</li>
<li><strong>C13A9 Brake System Malfunction</strong>: stored in the Electronic Parking Brake (EPB) system.</li>
</ul>
<h2>What is the accumulator?</h2>
<p>On Toyota hybrids like the Alphard and Vellfire, braking is electronically controlled. The brake actuator has a pump motor that builds hydraulic pressure and an accumulator that stores it, so the brakes have pressure ready the moment you press the pedal. C1391 means the control unit has seen the stored pressure fall in a way it does not expect: in plain words, pressure is leaking away inside the unit.</p>
<p>The label on the pump says it plainly: <em>“High pressure inside brake system.”</em> The system must be depressurised as the repair manual describes before anyone opens a brake line or removes the unit. This is not a job for a test lamp and a spanner.</p>
<h2>What we did</h2>
<p>We replaced the brake actuator with a new unit, part number 44510-30290. The photo at the top of this page shows the new unit next to the original that came off the car. Here is the new unit before fitting:</p>
<p><img src="{img:toyota-alphard-new-actuator}" alt="New Toyota brake actuator with accumulator and pump, part number 44510-30290, still wrapped on its box" width="640" height="480" loading="lazy" style="width:100%;height:auto;border-radius:12px"></p>
<p>After a brake actuator is changed on a Toyota hybrid, the brake system has to be bled and set up with a scan tool, not just bolted in. That is why we do this work with full diagnostic equipment.</p>
<h2>Signs your Toyota hybrid brake actuator needs attention</h2>
<ul class="ticks">
<li>The brake, ABS, VSC or TRC warning lights come on, sometimes together.</li>
<li>The scan shows an accumulator or brake system code such as C1391 or C13A9.</li>
<li>The brake pump runs more often or for longer than it used to.</li>
</ul>
<p>Any of these is worth checking soon. If the red BRAKE warning light is on, or the pedal feels different, stop driving and get the car checked first. Our pick-up and delivery service can collect it.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your car model, year and the fault codes, with a photo of the dashboard or the scan tool screen. We will tell you what we can do, whether that is repairing your unit or fitting a new, used or reconditioned one. You can find us at Premier @ Kaki Bukit.</p>''',
        faq=[('What does Toyota code C1391 mean?', 'On this Toyota Alphard / Vellfire Hybrid the scan tool read C1391 as “Abnormal Leak in Accumulator”: the brake system’s stored hydraulic pressure is falling in a way the control unit does not expect.'),
             ('What part number was the new brake actuator?', 'The new brake actuator we fitted to this 2020 Alphard / Vellfire Hybrid (2AR-FXE) was part number 44510-30290. Check the part number for your own car before ordering.'),
             ('Is it safe to drive with C1391?', 'Get it checked soon. If the red BRAKE light is on or the pedal feels different, stop driving and have the car collected.')],
    ),
    dict(
        # Real job (Edwin's photo, 27 Oct 2026): Audi A3 ABS module repaired. Codes read from the photo; no year, price or
        # time given: do not add any. VIN and scanner serial are blurred in the photo.
        slug='audi-abs-fault-code-01276-hydraulic-pump', service='audi-abs-repair', date='2026-10-31', img_commit='ded90dba3566152a2b57662c0787983fb5a8a2f2',
        title='Audi ABS Code 01276 Hydraulic Pump Defective | The ECU Clinic',
        desc='An Audi A3 with ABS code 01276 "ABS Hydraulic Pump: Defective" and 16352 "Control Module: Defective" plus sensor codes. What they mean and how the ABS module was repaired.',
        h1='Audi ABS Code 01276 “ABS Hydraulic Pump: Defective” and 16352 “Control Module”',
        lead='A real job from our workshop: an Audi A3 with ten brake electronics codes at once. Here is what they meant and why the sensors were not the first thing to replace.',
        photo='audi-abs-fault-codes', alt='Scan tool showing Audi brake electronics codes 01276 ABS Hydraulic Pump defective and 16352 Control Module defective',
        share='audi-a3-abs-codes.jpg',
        body='''<p><strong>Short answer:</strong> on this Audi A3 the brake electronics (address 03) stored <strong>01276 “ABS Hydraulic Pump: Defective”</strong> and <strong>16352 “Control Module: Defective”</strong>, together with several sensor circuit codes. When the pump and the control module are both reported defective, the fault is usually in the ABS unit itself, not in the wheel sensors. We repaired the car’s own ABS module.</p>
<h2>What the scan tool showed</h2>
<p>The scan of the brake electronics listed ten codes:</p>
<ul class="ticks">
<li><strong>01276</strong> ABS Hydraulic Pump: defective</li>
<li><strong>16352</strong> Control Module: defective</li>
<li><strong>00290</strong> Left Rear ABS Wheel Speed Sensor: electrical fault in circuit</li>
<li><strong>00287</strong> Right Rear ABS Wheel Speed Sensor: electrical fault in circuit</li>
<li><strong>01542</strong> Rotation Rate Sensor: electrical fault in circuit</li>
<li><strong>00538</strong> Reference Voltage: electrical fault in circuit</li>
<li><strong>01130</strong> ABS Operation: implausible signal</li>
<li>Vehicle Voltage Terminal 30: lower limit exceeded</li>
</ul>
<h2>What does code 01276 mean?</h2>
<p>On an Audi the ABS hydraulic pump and the brake electronics control module sit in one unit in the engine bay. 01276 names the pump as defective. It does not say by itself whether the cause is the pump motor, its circuit or the module, so the unit is tested before anything is replaced.</p>
<h2>Why so many sensor codes at once?</h2>
<p>When the ABS module fails, it often stores a long list of codes at once, including wheel speed sensor codes, even when the sensors themselves may be fine. In this job the pump, the module and several sensor circuits were all faulty at once, so the codes pointed at the ABS control module rather than at several separate parts. That is why we read every code first and rule out the simple causes before replacing sensors.</p>
<h2>Why check the battery as well?</h2>
<p>The same scan had a low-voltage code for terminal 30, the permanent battery supply. A weak battery or a poor supply can cause brake electronics faults, so it is checked alongside the unit.</p>
<h2>What did we do?</h2>
<p>We repaired the car’s own ABS module, refitted it and cleared the faults. We repair Volkswagen and Skoda ABS units too. More in our <a href="../vw-audi-abs-esp-light-on/">guide to VW and Audi ABS and ESP lights</a>.</p>
<h2>Is it safe to drive with these codes?</h2>
<p>In most cases the normal brakes still work, but the anti-lock function may be off until the fault is fixed, so the wheels can lock under hard braking, especially on wet roads. If the red brake warning light is on too, or the pedal feels different, stop driving and have the car checked. Our pick-up and delivery service can collect it.</p>
<h2>What should I send?</h2>
<p>WhatsApp us your Audi model, year and the fault codes, with a photo of the scan tool screen. You can find us at Premier @ Kaki Bukit. Our repairs come with a 6-month warranty.</p>''',
        faq=[('What does Audi code 01276 mean?', 'On this Audi A3 the scan tool read 01276 as “ABS Hydraulic Pump: Defective” in the brake electronics (address 03). The ABS pump and control module are one unit, so the code points to that unit; testing shows whether it is the pump, its circuit or the module.'),
             ('Does code 16352 mean the ABS module is dead?', 'It means the scan tool reports the control module as defective. On this car, with the pump code and several sensor codes at the same time, we repaired the car’s own ABS module and the faults were cleared.'),
             ('Should I replace the wheel speed sensors first?', 'Not on the codes alone. When the pump and module codes appear with sensor codes, the module can be the cause of all of them, so every code is read and the simple causes ruled out before parts are replaced.')],
    ),
    dict(
        # Real job photos from Edwin, 31 Oct 2026: Toyota C-HR Hybrid, Ni-MH hybrid battery under the rear seat, the pack
        # removed and the cover off. The photos do not show a fault code, the cause, or what was fitted (new pack,
        # new or reconditioned modules): do not add any of these until Edwin confirms. Plate blurred in the source copy.
        slug='toyota-chr-hybrid-battery-removal', service='hybrid-battery-replacement', date='2026-10-31', img_commit='2332c72c9a8c659e3c83adc897109aac049c9cd5',
        title='Toyota C-HR Hybrid Battery: Where It Is and How It Comes Out | The ECU Clinic',
        desc='A Toyota C-HR Hybrid in our workshop: the Ni-MH hybrid battery under the rear seat, taken out and opened on the bench. What it looks like inside and what to know before replacing one.',
        h1='Toyota C-HR Hybrid Battery: Taken Out From Under the Rear Seat',
        lead='A real job from our workshop: a Toyota C-HR Hybrid with its hybrid battery out of the car and the cover off. Here is where the pack sits, what is inside, and why it is checked before anything is replaced.',
        photo='toyota-chr-battery-opened', alt='Toyota C-HR Hybrid nickel-metal hydride battery pack with the cover off, showing the row of battery modules',
        share='toyota-chr-hybrid-battery-opened.jpg',
        body='''<p><strong>Short answer:</strong> on the Toyota C-HR Hybrid the high-voltage hybrid battery sits <strong>under the rear seat</strong>. It is a <strong>nickel-metal hydride (Ni-MH)</strong> pack, as its label says. To reach it, the rear seat cushion comes out, the high-voltage system is made safe, and the pack is unbolted and lifted out of the floor.</p>
<p><img src="{img:toyota-chr-hybrid-rear}" alt="Silver Toyota C-HR with Hybrid Synergy Drive badge in The ECU Clinic workshop, number plate blurred" width="640" height="480" loading="lazy" style="width:100%;height:auto;border-radius:12px"></p>
<h2>Where is the hybrid battery on a Toyota C-HR?</h2>
<p>Under the rear seat cushion, in the floor of the car. With the cushion out you can see the pack: a long silver case with the orange high-voltage cables and the battery junction block at one end. On the C-HR the pack is a single unit across the width of the car.</p>
<p><img src="{img:toyota-chr-battery-in-car}" alt="Toyota C-HR Hybrid battery under the rear seat with the seat cushion removed, orange high-voltage cables at one end" width="640" height="480" loading="lazy" style="width:100%;height:auto;border-radius:12px"></p>
<p>The orange cables carry high voltage. The label on the pack carries a <em>danger</em> warning in Japanese and says it contains an alkaline electrolyte. Before the pack is unbolted, the high-voltage system has to be shut down and isolated as the repair manual describes. This is a job for trained hands and insulated tools.</p>
<h2>The pack out of the car</h2>
<p>Out of the car, the pack is easier to inspect and to work on safely on the floor of the workshop.</p>
<p><img src="{img:toyota-chr-battery-removed}" alt="Toyota C-HR Hybrid Ni-MH battery pack removed from the car, lying on the workshop floor with its cover on" width="640" height="480" loading="lazy" style="width:100%;height:auto;border-radius:12px"></p>
<h2>What is inside a C-HR hybrid battery?</h2>
<p>With the cover off you can see how the pack is built: a long row of identical battery modules held together in one stack, with sensing wires running along the top and the junction block with the main high-voltage connections at the end. The photo at the top of this page shows this pack open.</p>
<p>Because the pack is made of many modules in series, one weak module can pull the whole pack down. That is why a hybrid battery warning is read and checked properly before anyone decides what to replace.</p>
<h2>Check before you replace</h2>
<p>A hybrid system warning can come from the battery pack or from other parts of the hybrid system. We read the fault codes first, so you only replace the battery when the battery is the problem. When it is, we fit a <a href="../../services/hybrid-battery-replacement/">brand-new OEM hybrid battery</a>, with a warranty of 1 year or 100,000 km.</p>
<p>Common signs that a hybrid battery is getting weak:</p>
<ul class="ticks">
<li>A hybrid system warning on the dashboard.</li>
<li>The car uses more petrol than it used to.</li>
<li>The engine starts more often, even at low speed.</li>
<li>The battery level on the display drops or rises quickly.</li>
</ul>
<h2>What should I send?</h2>
<p>WhatsApp us your car model and year, and the fault code or a photo of the warning if you have one. We will check availability and price for your car. You can find us at Premier @ Kaki Bukit, or use our pick-up and delivery service.</p>''',
        faq=[('Where is the hybrid battery on a Toyota C-HR?', 'Under the rear seat cushion, in the floor of the car. The cushion comes out to reach it.'),
             ('What type of hybrid battery does the Toyota C-HR Hybrid in this job use?', 'A nickel-metal hydride (Ni-MH) pack, as printed on the label of the pack we took out.'),
             ('Can I take the hybrid battery out myself?', 'No. The pack and its orange cables carry high voltage. The system must be shut down and isolated as the repair manual describes, with insulated tools, before the pack is unbolted.'),
             ('What hybrid battery do you fit?', 'Brand-new OEM hybrid batteries, with a warranty of 1 year or 100,000 km. WhatsApp us your car model and year to check availability and price.')],
    ),
]
