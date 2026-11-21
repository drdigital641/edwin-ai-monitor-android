"""Hon Win Motor mini-site content (paid Premium client, Edwin 21 Nov 2026). Facts only from honwin.sg (read 21 Nov 2026),
its Google Business Profile record (data/google_cache/hon-win-motor.json) and Edwin's brief (full workshop incl. accident claims,
mainly passenger cars). No prices (its own pages disagree), no overall Google score (21 Nov rule), no stock testimonials,
no second towing number (its pages disagree). Written in the workshop's voice ("we"), plain English, no em dashes."""

SLUG = 'hon-win-motor'
BASE_PATH = 'workshops/hon-win-motor/'
SITE = 'hon-win-motor'   # p1-cta.js SITE = Controller Client slug
WA = '6591718466'
TEL = '+6591718466'
TEL_SHOW = '9171 8466'
EMAIL = 'honwinmotor@gmail.com'
NAME = 'Hon Win Motor'
TRADING = 'Hon Win Motor Trading'
STREET = '6 Defu Lane 10, #01-544'
POSTAL = '539187'
LAT, LNG = 1.359057119420834, 103.8948428184969
PLACE_ID = 'ChIJ-bSN1ssX2jER-SbNNJfI4WM'
GOOGLE_URL = 'https://www.google.com/maps/search/?api=1&query=Hon%20Win%20Motor&query_place_id=' + PLACE_ID
HOURS = [('Monday to Friday', '10am to 7pm'), ('Saturday', '10am to 3pm'), ('Sunday', 'Closed')]
HOURS_NOTE = 'Hours from our Google Business Profile. WhatsApp us before you come on a public holiday.'
PAY = 'Cash, scan to pay, bank transfer, or Atome instalments.'
MAKES = 'Japanese, Korean and Continental cars, petrol and hybrid, including Mercedes-Benz, Audi, Porsche and Volvo.'
REVIEW_THEMES = 'Drivers on Google mention Mercedes oil leak and coolant repairs, spray painting and repair work, and full servicing at our workshop in Defu Lane.'

TEAM = [('Thachna', 'Team leader'), ('Ah Meng', 'Classic car specialist'), ('Jega', 'Petrol and EV specialist')]

# ------------------------------------------------------------------ services
SERVICES = [
 dict(slug='car-servicing', short='Servicing', nav='Servicing',
      title='Car Servicing in Hougang, Defu Lane | Hon Win Motor',
      desc='Car servicing at Hon Win Motor, 6 Defu Lane 10, Hougang: oil and filter, OBD scan, full safety check. Petrol and hybrid. Walk-ins welcome. WhatsApp 9171 8466.',
      h1='Car servicing in Hougang, at Defu Lane',
      line='Oil, filter, a scan and a full safety check, usually in about 1.5 hours.',
      wa='car servicing',
      photo=('hw/car-on-lift.webp', 'Toyota hybrid raised on a lift for servicing at Hon Win Motor'),
      card='Engine oil and filter, an OBD scan, top-ups and a full safety check. Petrol and hybrid.',
      job_title='Every service on the job card',
      job=['Engine oil and oil filter changed', 'OBD diagnostic scan', 'Wiper water, coolant and brake fluid topped up',
           'Battery health checked', 'Engine warning lights checked', 'Belts, idling speed and ignition timing checked',
           'Radiator hoses and water pump checked', 'Brake pads and engine mounts checked'],
      job_note='Spark plugs and automatic gearbox oil are checked and changed only if they need it.',
      sections=[
        ('Pick your engine oil', ['We stock Total Quartz 9000, Petronas Syntium, Castrol Edge and Mobil 1. The price of a service depends on the oil you choose and how much your engine takes, so tell us your car model on WhatsApp and we will give you the price before we start.',
                                  'Continental cars need brand-specific oil filters, so their servicing is priced differently from Japanese and Korean cars.']),
        ('How long it takes', ['An oil and filter change takes about 20 to 40 minutes. A full service takes about 1.5 hours. Walk-ins are welcome, but a WhatsApp first lets us tell you if a lift is free.']),
        ('Hybrids and EVs', ['We service petrol and hybrid cars. On electric cars we do not work on the high-voltage battery, but we can handle tyres, body repairs and other non-battery work.']),
        ('Buying a used car? Check it first', ['We also do pre-purchase inspections at our workshop. It takes about 1.5 hours and covers engine and gearbox condition, electrical faults, hidden structural problems and known faults for that model, with an OBD scan report.']),
      ],
      faqs=[('How long does a car service take?', 'An oil and filter change takes about 20 to 40 minutes. A full service takes about 1.5 hours.'),
            ('Do I need to book a service?', 'No, walk-ins are welcome. WhatsApp 9171 8466 first to check that a lift is free.'),
            ('Which engine oils do you use?', 'Total Quartz 9000, Petronas Syntium, Castrol Edge and Mobil 1. The price depends on the oil you pick.'),
            ('Do you change parts that do not need changing?', 'No. Spark plugs and gearbox oil are checked and changed only if needed, and we quote before we replace any part.')]),
 dict(slug='car-repair', short='Repairs', nav='Repairs',
      title='Car Repair in Hougang: Engine & Gearbox | Hon Win Motor',
      desc='Engine, electrical and gearbox repairs at Hon Win Motor, Defu Lane, Hougang. We find the fault first and quote before work starts. WhatsApp 9171 8466.',
      h1='Car repairs in Hougang: engine, electrical and gearbox',
      line='We find the fault first, then quote before any work starts.',
      wa='a car repair',
      photo=('hw/engine-overhaul.webp', 'Hon Win Motor mechanic working on an engine removed from a car'),
      card='Warning lights, starting faults, overheating, engine and gearbox overhauls.',
      job_title='Bring it in if you notice',
      job=['Check engine or warning light on', 'Car struggles to start or will not start', 'Battery keeps going flat', 'Lights flickering or not working',
           'Loss of power, or a whistle from the turbo', 'Engine overheating', 'Jerky or late gear changes', 'Revs rise but the car does not speed up',
           'Whining, humming or clunking from the gearbox', 'Car will not move in Drive or Reverse'],
      job_note='We diagnose before we touch anything. The diagnosis fee is waived if you go ahead with the repair here.',
      sections=[
        ('Engine and electrical repairs', ['Batteries, alternators and starter motors. Headlamp and tail lamp overhauls and wiring faults. Turbo repairs, water pumps and other engine parts.',
                                           'If you already have the part, you can bring your own. We will fit it, but parts you supply are not covered by our warranty.']),
        ('Engine overhaul', ['A top overhaul fixes the upper part of the engine while it stays in the car: valves, gaskets, timing parts and other worn parts. A full overhaul takes the engine out, strips it, replaces the damaged parts and rebuilds it. We can also swap in a used or reconditioned engine, in line with LTA rules.',
                             'An overhaul usually takes 1 to 2 weeks. We quote after we inspect the engine, and our engine overhaul work carries a 1-month warranty.']),
        ('Gearbox overhaul and repair', ['We repair and overhaul automatic, manual, CVT and DCT gearboxes in-house. Repair is always the first option. If a gearbox is beyond repair, you decide whether to replace it.',
                                          'A gearbox job usually keeps the car with us for about a week, and our gearbox work carries a 6-month warranty. A gearbox oil flush is a separate service.']),
        ('Car cannot be driven?', ['WhatsApp or call us on 9171 8466. Towing is free when the repair is done at our workshop.']),
      ],
      faqs=[('Do you charge for diagnosis?', 'Yes, but the fee is waived if you go ahead with the repair at our workshop.'),
            ('Can I bring my own parts?', 'Yes. We will install them, but customer-supplied parts are not covered by our warranty.'),
            ('Do you repair CVT and DCT gearboxes?', 'Yes. We repair and overhaul automatic, manual, CVT and DCT gearboxes in-house.'),
            ('How long does an engine overhaul take?', 'Usually 1 to 2 weeks, depending on the engine and the parts needed.'),
            ('Is there a warranty?', 'Our engine overhaul work carries a 1-month warranty and our gearbox work a 6-month warranty. Parts you supply yourself are not covered.')]),
 dict(slug='car-aircon-repair', short='Aircon', nav='Aircon',
      title='Car Aircon Repair in Hougang, Defu Lane | Hon Win Motor',
      desc='Car aircon not cold? Hon Win Motor at Defu Lane, Hougang checks for leaks, tops up gas and repairs coils, compressors and blowers. WhatsApp 9171 8466.',
      h1='Car aircon repair in Hougang',
      line='Aircon not cold or losing gas? We find the cause before we quote.',
      wa='car aircon repair',
      photo=('hw/aircon-cooling-coil.webp', 'New aircon cooling coil and expansion valve ready to be fitted at Hon Win Motor'),
      card='Gas top-up and leak check, cooling coils, compressors, condensers and blowers.',
      job_title='What we check and fix',
      job=['Aircon gas top-up', 'Leak check on the system', 'Cooling coil replacement', 'Expansion valve replacement',
           'Compressor repairs', 'Condenser repairs', 'Blower repairs'],
      job_note='We diagnose the problem and quote before any work starts.',
      sections=[
        ('Why gas alone may not fix it', ['If the aircon keeps losing cold air, there is usually a leak. A gas top-up alone will not fix a leaking cooling coil, hose or other faulty part, so we check for leaks first and tell you what we find.']),
        ('Original or aftermarket parts', ['Original parts cost more and match the factory specification. Aftermarket parts cost less. We tell you both options and you choose.',
                                           'Parts we supply come with the supplier\'s warranty. Parts you bring in yourself are not covered.']),
        ('How long it takes', ['A cooling coil replacement usually takes 1 to 2 days. Simpler jobs are quicker: WhatsApp us your car model and the problem and we will give you an idea of time.']),
      ],
      faqs=[('Do I need an appointment for an aircon check?', 'No, walk-ins are welcome. WhatsApp 9171 8466 first if you want to check we are free.'),
            ('Will a gas top-up fix my aircon?', 'Only if there is no leak. If the system is leaking, a top-up will not last, so we check for leaks first.'),
            ('How long does a cooling coil replacement take?', 'Usually 1 to 2 days.'),
            ('Which cars do you do aircon for?', 'Japanese, Korean and Continental cars, including Mercedes-Benz, Audi, Porsche and Volvo, and diesel vehicles.')]),
 dict(slug='accident-repair-insurance-claim', short='Accident claims', nav='Accident',
      title='Accident Repair & Insurance Claim, Hougang | Hon Win Motor',
      desc='Car accident in Hougang or nearby? Hon Win Motor at Defu Lane does accident repairs and helps with your insurance claim. WhatsApp photos to 9171 8466.',
      h1='Accident repair and insurance claims in Hougang',
      line='Had an accident? WhatsApp us photos and we will tell you the next step.',
      wa='an accident repair and insurance claim',
      photo=('hw/workshop-front.webp', 'Hon Win Motor Trading signboard above the workshop at 6 Defu Lane 10'),
      card='Accident repairs and body work, with help on your insurance claim.',
      job_title='At the scene, if it is safe',
      job=['Stop and switch on your hazard lights', 'Take photos of every car, the damage, the number plates and the road',
           'Exchange names, phone numbers, car numbers and insurer names with the other driver', 'Keep your dash cam footage',
           'Call for help first if anyone is hurt'],
      job_note='Report the accident to your insurer within 24 hours, or by the next working day, even if you do not plan to claim. Your insurer will tell you where to report.',
      sections=[
        ('How we help', ['We do accident repairs and body work at our workshop in Defu Lane, and we help you with the insurance claim for the repair. Send us photos of the damage, your car model and your insurer\'s name on WhatsApp, and we will tell you what to do next.',
                         'If your car cannot be driven, call or WhatsApp 9171 8466. Towing is free when the repair is done at our workshop.']),
        ('Check your policy first', ['Some motor policies only cover repairs at the insurer\'s own authorised workshops. Others let you choose. Check your policy, or send us your insurer\'s name and policy type and we will tell you if we can take the job before you decide.']),
        ('When you also need a police report', ['Most accidents only need a report to your insurer. You also need to make a police report if anyone is injured, if the other driver drives off, or if a government vehicle, a foreign vehicle, or public property is involved.']),
      ],
      faqs=[('Do you handle accident insurance claims?', 'Yes. We do the accident repair and help you with the insurance claim. WhatsApp us photos of the damage and your insurer\'s name to start.'),
            ('Do I need to report the accident if I am not claiming?', 'Yes. Report it to your insurer within 24 hours, or by the next working day, even if you do not plan to claim.'),
            ('Can I choose my own workshop?', 'It depends on your policy. Some only cover repairs at the insurer\'s authorised workshops. Send us your insurer and policy type and we will check with you.'),
            ('My car cannot be driven after the accident. What now?', 'WhatsApp or call 9171 8466. Towing is free when the repair is done at our workshop.')]),
]

EXTRAS = [('Dash cams and accessories', 'Front and rear dash cams, parking mode wiring, reverse cameras, parking sensors, speakers and Android Auto head units. Bring your own parts or let us source them.'),
          ('Pre-purchase inspection', 'About 1.5 hours at our workshop before you buy a used car, with an OBD scan report.'),
          ('Classic cars', 'Routine maintenance, restoration and hard-to-find parts, looked after by Ah Meng, our classic car specialist.'),
          ('Lorry servicing', 'Servicing, fault finding and safety checks for 10, 14 and 24-footer lorries, for owners and fleets.')]

STEPS = [('WhatsApp us', 'Send your car model and what is wrong. Photos help.'),
         ('We check the car', 'We diagnose before we touch anything.'),
         ('You get a quote', 'The price comes before any work starts, with no hidden costs.'),
         ('We fix it', 'Towing is free if the car cannot be driven and the repair is done here.')]

# ------------------------------------------------------------------ areas within about 8 km (reference point: the town's MRT station)
AREAS = [
 dict(slug='hougang', name='Hougang', lat=1.3712, lng=103.8923, mrt='Hougang MRT (North East Line)',
      intro='Our workshop is inside the Hougang planning area, in Defu Industrial Estate at the south end of the town. For most Hougang drivers we are a few minutes away, whether you live near Hougang Central, Hougang Mall or Buangkok.',
      local='Leave the car with us in the morning and get home by bus or from Hougang MRT on the North East Line.'),
 dict(slug='kovan', name='Kovan', lat=1.3602, lng=103.8851, mrt='Kovan MRT (North East Line)',
      intro='Kovan is the closest MRT station to our workshop. Drivers around Kovan Hub and along Upper Serangoon Road are just across from Defu Industrial Estate.',
      local='Drop the car off and walk or take a short bus ride back to Kovan MRT.'),
 dict(slug='serangoon', name='Serangoon', lat=1.3498, lng=103.8737, mrt='Serangoon MRT (North East and Circle lines)',
      intro='Serangoon, Serangoon Central and Serangoon Gardens are a short drive from Defu Lane. We are open on Saturday until 3pm, so a weekend service fits around work.',
      local='Serangoon MRT is on both the North East and Circle lines, so getting home after you drop the car off is easy.'),
 dict(slug='sengkang', name='Sengkang', lat=1.3917, lng=103.8954, mrt='Sengkang MRT (North East Line and LRT)',
      intro='Sengkang is north of us, past Hougang. From Compass One, Anchorvale, Rivervale or Fernvale, it is a short drive south to Defu Lane.',
      local='After dropping the car off, the North East Line takes you back to Sengkang MRT from Kovan or Hougang.'),
 dict(slug='punggol', name='Punggol', lat=1.4052, lng=103.9024, mrt='Punggol MRT (North East Line and LRT)',
      intro='Punggol is at the north end of the North East Line, the same line that stops at Kovan and Hougang near our workshop.',
      local='Leave the car with us and take the North East Line from Kovan or Hougang back to Punggol.'),
 dict(slug='paya-lebar', name='Paya Lebar', lat=1.3177, lng=103.8926, mrt='Paya Lebar MRT (East West and Circle lines)',
      intro='Paya Lebar, around Paya Lebar Quarter and the Upper Paya Lebar area, is south of our workshop. It is a short drive up for servicing or a repair.',
      local='Paya Lebar MRT is on the East West and Circle lines, handy if you work in the area and want to drop the car off on the way.'),
 dict(slug='ubi-kaki-bukit', name='Ubi and Kaki Bukit', lat=1.3325, lng=103.9038, mrt='Ubi and Kaki Bukit MRT (Downtown Line)',
      intro='Ubi and Kaki Bukit sit south-east of Defu, with homes and industrial estates side by side. Drivers who work in Ubi or Kaki Bukit can drop the car with us and collect it after work.',
      local='Ubi and Kaki Bukit MRT stations are on the Downtown Line.'),
 dict(slug='bedok-north', name='Bedok North', lat=1.3347, lng=103.9180, mrt='Bedok North MRT (Downtown Line)',
      intro='Bedok North, around Bedok Reservoir and Bedok North Avenue, is east of our workshop. Bedok North drivers can reach Defu Lane without going into town.',
      local='Bedok North MRT and Bedok Reservoir MRT are on the Downtown Line.'),
 dict(slug='tampines', name='Tampines', lat=1.3535, lng=103.9453, mrt='Tampines MRT (East West and Downtown lines)',
      intro='Tampines is the largest town to the east of us. From Tampines Mall or Our Tampines Hub, Defu Lane is a short drive west.',
      local='Tampines MRT is on the East West and Downtown lines.'),
 dict(slug='ang-mo-kio', name='Ang Mo Kio', lat=1.3700, lng=103.8496, mrt='Ang Mo Kio MRT (North South Line)',
      intro='Ang Mo Kio is west of us, across Serangoon. From AMK Hub, Defu Lane is a short drive east.',
      local='Ang Mo Kio MRT is on the North South Line.'),
]
