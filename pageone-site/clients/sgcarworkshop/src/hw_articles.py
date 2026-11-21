"""Hon Win Motor articles (Edwin 21 Nov 2026: an article section, one new article every 2 days; 3 sample articles to start).
Each article targets one area + service niche and maps to one of his own service pages (NICHE GATE). Facts come only from
hw_content.py (his site, his Google profile, Edwin's brief) plus general, well-known Singapore motoring practice. No prices,
no Google score, no invented customers or numbers. Written in the workshop's voice ("we"), plain English, no em dashes.
Kept apart from the directory's own /guides/ (car-aircon-not-cold, gearbox-cvt-jerking ...): different intent, local angle.
Section items: a str is a paragraph, a list is a bullet list. Hero images: Base44 via Bridge hero_image (Illustrative), 1200x630 JPG."""

ARTICLES = [
 dict(slug='used-car-inspection-hougang', date='2026-11-21', maps='car-servicing',
      title='Used Car Inspection Before You Buy, Hougang | Hon Win Motor',
      desc='Buying a used car in Hougang, Sengkang or Punggol? What our 1.5-hour pre-purchase inspection at Defu Lane checks, and how to use the report.',
      h1='Used car inspection before you buy: what we check at Defu Lane',
      img='hw/articles/used-car-inspection-hougang.jpg',
      alt='Illustrative: mechanic scanning a used car with an OBD tool in a Singapore workshop',
      card='What a pre-purchase inspection covers, how long it takes, and how to use the report before you pay.',
      intro=['A used car in Singapore is a big purchase, and most of the money goes into a car you only see for a short viewing. A seller can show you a clean interior and a fresh service sticker. What you cannot see on a viewing is what is happening under the car, inside the gearbox, or in the car\'s computer.',
             'That is what a pre-purchase inspection is for. If you are buying a car in Hougang, Sengkang, Punggol or anywhere nearby, you can bring it to our workshop at 6 Defu Lane 10 before you pay. The check takes about 1.5 hours and you get an OBD scan report.'],
      sections=[
        ('What we check', [
            'We look at the parts of a car that cost the most to put right, and the faults a short test drive will not show.',
            ['Engine condition: leaks, unusual noises, how it starts and idles, and the engine mounts',
             'Gearbox condition: how it shifts, whether it slips or jerks, and any signs of trouble',
             'Electrical faults: an OBD scan for stored fault codes, warning lights, the battery and the lights',
             'Hidden structural problems: we raise the car on a lift and look underneath for signs of past damage or earlier repair work',
             'Known faults for that model: problems that model is known for, so you know what to ask the seller'],
            'At the end you get the OBD scan report and we explain what we found in plain words.']),
        ('Why the car goes on a lift', [
            'A lot of what matters is underneath. Oil and coolant leaks, damaged or rusted parts, and repairs after an accident are much easier to spot when the car is raised. A car that looks perfect from the outside can still need expensive work underneath, and that is better to know before you pay than after.']),
        ('Why the OBD scan matters', [
            'A warning light can be switched off, but the car\'s computer often still holds the fault codes behind it. The scan shows us stored and pending faults in the engine, gearbox and other systems, so a problem that was cleared just before the viewing is less likely to slip past.']),
        ('How to use the report', [
            'A fault on the report does not always mean you should walk away. Some faults are small and cheap to fix. Others are worth a lot of money. Here is how most buyers use the result:',
            ['If the faults are small, buy the car and plan the repairs',
             'If the faults are bigger, ask us what the repair involves and use that to talk to the seller about the price, or ask the seller to fix it first',
             'If the problems are serious, for example in the gearbox or the structure, you can walk away before any money changes hands'],
            'We tell you what we found. The decision is always yours.']),
        ('Hybrid and electric cars', [
            'We work on petrol and hybrid cars, so a used hybrid gets the same inspection. On electric cars we do not work on the high-voltage battery, so an EV inspection with us would not cover the battery. Tell us the model on WhatsApp and we will tell you what we can check.']),
        ('How to arrange it', [
            ['Agree with the seller or dealer that you can bring the car for an inspection before you pay',
             'WhatsApp us on 9171 8466 with the car model and the day you would like to come, so we can keep a lift free',
             'Bring the car to 6 Defu Lane 10, #01-544, in Defu Industrial Estate. We are open Monday to Friday 10am to 7pm and Saturday 10am to 3pm'],
            'The workshop is a short drive from Hougang, Sengkang, Punggol, Serangoon and Kovan, so it is easy to fit in between a viewing and a decision.']),
      ],
      faqs=[('How long does a pre-purchase inspection take?', 'About 1.5 hours at our workshop.'),
            ('What do I get at the end?', 'An OBD scan report, and we explain what we found on the engine, gearbox, electrics and underside of the car.'),
            ('Do I need to book?', 'Please WhatsApp 9171 8466 first with the car model and the day you want to come, so we can keep a lift free.'),
            ('Can you inspect a hybrid?', 'Yes. We work on petrol and hybrid cars. On electric cars we do not work on the high-voltage battery.')],
      wa='a pre-purchase inspection for a used car'),

 dict(slug='car-accident-hougang-what-to-do', date='2026-11-21', maps='accident-repair-insurance-claim',
      title='Car Accident in Hougang? What to Do Next | Hon Win Motor',
      desc='Had a car accident in Hougang, Sengkang or Punggol? What to do at the scene, when to report it, and how the repair and insurance claim work.',
      h1='Car accident in Hougang or Sengkang: what to do, from the scene to the repair',
      img='hw/articles/car-accident-hougang-what-to-do.jpg',
      alt='Illustrative: driver photographing a dented bumper after a minor accident on a Singapore estate road',
      card='The steps after a car accident: at the scene, reporting to your insurer, and getting the car repaired.',
      intro=['Even a small bump on Hougang Avenue or in a Sengkang car park is stressful. You are not sure who to call, what to photograph or whether you need to report it at all. The order you do things in matters, because what you collect in the first few minutes is what your insurance claim is built on.',
             'This is the order we suggest to drivers who come to us after an accident.'],
      sections=[
        ('1. At the scene', [
            'Safety comes first. Stop, switch on your hazard lights and check that everyone is all right. Call for help first if anyone is hurt.',
            'Then, if it is safe, collect what you will need later:',
            ['Photos of every car involved, from a distance and close up, including the number plates',
             'Photos of the damage on both cars, and of the road, the lanes and any traffic lights or signs nearby',
             'The other driver\'s name, phone number, car number and insurer\'s name',
             'Names and phone numbers of any witnesses',
             'Your dash cam footage. Many dash cams record over old footage, so save or copy the file as soon as you can'],
            'If no one is hurt and the cars can still be driven, move them out of the traffic once you have taken your photos.']),
        ('2. Report it to your insurer', [
            'Report the accident to your insurer within 24 hours, or by the next working day, even if you do not plan to claim. Your insurer will tell you where to report and what to bring.',
            'Keep your photos, the other driver\'s details and your dash cam footage together. You will be asked for them.']),
        ('3. Do you also need a police report?', [
            'Most accidents only need a report to your insurer. You also need to make a police report if anyone is injured, if the other driver drives off, or if a government vehicle, a foreign vehicle, or public property is involved.']),
        ('4. Your claim and your policy', [
            'If the other driver caused the accident, the claim is usually made against their insurer. If it was your fault, or it is not clear, the claim usually goes through your own policy, and that can affect your no-claim discount. Your insurer can explain how this works for your policy.',
            'Before you choose a workshop, check your policy. Some motor policies only cover repairs at the insurer\'s own authorised workshops. Others let you choose. If you are not sure, send us your insurer\'s name and policy type and we will tell you whether we can take the job before you decide.']),
        ('5. Getting the car repaired', [
            'We do accident repairs and body work at our workshop in Defu Lane, and we help you with the insurance claim for the repair. To start, WhatsApp us on 9171 8466 with:',
            ['Photos of the damage', 'Your car model', 'Your insurer\'s name'],
            'We will tell you what to do next. If your car cannot be driven after the accident, call or WhatsApp us. Towing is free when the repair is done at our workshop.']),
        ('Close to where it happened', [
            'Our workshop at 6 Defu Lane 10 is close to Hougang, Kovan, Serangoon, Sengkang, Punggol and Paya Lebar, so a car that has to be towed does not have to go far. We are open Monday to Friday 10am to 7pm and Saturday 10am to 3pm.']),
      ],
      faqs=[('Do I have to report a small accident if I am not claiming?', 'Yes. Report it to your insurer within 24 hours, or by the next working day, even if you do not plan to claim.'),
            ('When do I need a police report?', 'If anyone is injured, if the other driver drives off, or if a government vehicle, a foreign vehicle, or public property is involved.'),
            ('Can I send my car to Hon Win Motor for an insurance repair?', 'It depends on your policy. Send us your insurer\'s name and policy type on WhatsApp and we will check with you.'),
            ('My car cannot be driven. What now?', 'Call or WhatsApp 9171 8466. Towing is free when the repair is done at our workshop.')],
      wa='an accident repair and insurance claim'),

 dict(slug='gearbox-repair-or-replace-hougang', date='2026-11-21', maps='car-repair',
      title='Gearbox Repair or Replace? Hougang Guide | Hon Win Motor',
      desc='Gearbox trouble near Hougang or Paya Lebar? How we decide between repair, overhaul and replacement for automatic, CVT, DCT and manual gearboxes.',
      h1='Gearbox repair or replacement: how to decide, from a Hougang workshop',
      img='hw/articles/gearbox-repair-or-replace-hougang.jpg',
      alt='Illustrative: opened automatic gearbox on a workbench during an overhaul in a Singapore workshop',
      card='Repair, overhaul or replace: how we decide what a faulty gearbox needs, and what to tell us first.',
      intro=['A gearbox fault is one of the repairs drivers worry about most. The car jerks, slips or will not move, and the first answer they often hear is "change the whole gearbox". Sometimes that is right. Often it is not.',
             'At our workshop in Defu Lane we repair and overhaul automatic, manual, CVT and DCT gearboxes in-house, and repair is always the first option we look at. This is how we decide what a gearbox needs.'],
      sections=[
        ('Signs to bring the car in', [
            ['Jerky or late gear changes', 'The revs rise but the car does not speed up', 'Whining, humming or clunking from the gearbox',
             'The car will not move in Drive or Reverse', 'A warning light comes on with any of the above'],
            'Do not wait for it to get worse. A small fault that is driven on can turn into a bigger one.']),
        ('Step 1: find the fault first', [
            'We diagnose before we touch anything: a scan for fault codes, a look at the gearbox oil, and a check of how the car drives. The diagnosis fee is waived if you go ahead with the repair at our workshop.',
            'You can help by telling us when it happens: on a cold start or when the car is warm, at what speed, when you change gears, or when going uphill. A short video with the sound on is useful too.']),
        ('Step 2: repair, overhaul or replace', [
            'There are three ways to put a gearbox right, and the diagnosis tells us which one fits:',
            ['Repair: fix the part that has failed, when the rest of the gearbox is healthy',
             'Overhaul: take the gearbox out, strip it, replace the worn and damaged parts, and rebuild it',
             'Replace: fit another gearbox, when yours is beyond repair'],
            'If a gearbox is beyond repair, we tell you, and you decide whether to replace it. A gearbox oil flush is a separate service, not a cure for a gearbox that is already damaged.']),
        ('Automatic, CVT, DCT or manual: does the type matter?', [
            'Each type works differently. A conventional automatic changes gear with fluid pressure and clutch packs. A CVT has no fixed gears and uses a belt or chain between two pulleys. A DCT uses two clutches to pre-select the next gear. A manual relies on your clutch and the gear selectors.',
            'Because they wear in different ways, the same symptom can mean different things on different gearboxes. That is why we diagnose first instead of guessing from the symptom.']),
        ('Think about your COE too', [
            'In Singapore the right answer also depends on how long you plan to keep the car. If the COE has many years left, a proper overhaul makes sense. If the car is close to the end of its COE, you may want the most sensible repair for the time you have left. Tell us your plans and we will talk you through the options.']),
        ('Time and warranty', [
            'A gearbox job usually keeps the car with us for about a week, and our gearbox work carries a 6-month warranty. If the car cannot be driven, call or WhatsApp 9171 8466. Towing is free when the repair is done at our workshop.']),
        ('Near Hougang and Paya Lebar', [
            'Our workshop is at 6 Defu Lane 10, #01-544, in Defu Industrial Estate, a short drive from Hougang, Kovan, Serangoon, Paya Lebar and Ubi. We are open Monday to Friday 10am to 7pm and Saturday 10am to 3pm.']),
      ],
      faqs=[('Do you repair CVT and DCT gearboxes?', 'Yes. We repair and overhaul automatic, manual, CVT and DCT gearboxes in-house.'),
            ('Do I have to replace my gearbox?', 'Not always. Repair is the first option. If a gearbox is beyond repair, we tell you and you decide whether to replace it.'),
            ('How long does a gearbox repair take?', 'A gearbox job usually keeps the car with us for about a week.'),
            ('Is there a warranty on gearbox work?', 'Yes, our gearbox work carries a 6-month warranty. Parts you supply yourself are not covered.')],
      wa='a gearbox problem'),
]
