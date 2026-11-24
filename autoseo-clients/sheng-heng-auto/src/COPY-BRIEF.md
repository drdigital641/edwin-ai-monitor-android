# English copy brief: Sheng Heng Auto Service Centre preview (write once in English)

You write ONE file: /tmp/claude-0/sh/src/content_en_pages.json (UTF-8, valid JSON). English only.
Facts: read facts.md with the Bluehost Bridge tool mcp__Bluehost_Bridge__invoke_drop_read (drop_id 6b054106d26e59b6a7bcc0cc, path facts.md). Use ONLY facts in that file. If a fact is not there, leave it out.

## Hard bans (the build grep fails on these, case-insensitive)
Seri Orkid; any Google rating number or review count; "5-star workshop"; "rated 5"; aggregate rating; Page One; lorem; TODO; placeholder; the word "best"; "No.1"; "number one"; guarantee / guaranteed; warranty; authorised / authorized; "official dealer"; "dealer-level"; Korean; "RM" followed by a digit; "from RM"; LAUNCH (uppercase); Shopee; "Auto restoration"; any phone other than 016-335 2124 (main, WhatsApp) — do not write phone numbers in copy at all, the templates add them.
Also never: prices, turnaround times, drive times, pickup/towing, team size, staff names (except "Mr. Yaw" on about/contact), customer names (except reviewer quotes below), equipment brand names, part numbers beyond facts.md, competitors, Johor Bahru city centre / Taman Pelangi / Mount Austin / Johor Jaya / Kulai / Masai / Permas Jaya / Pasir Gudang / Pontian / Singapore as served places. "Johor Bahru" only as a region ("Skudai, Johor Bahru").
Design-guide copy bans: no em dashes (use commas, colons or full stops), no "elevate", "unlock", "seamless", "cutting-edge", "trusted partner", "look no further", no emoji, no ALL CAPS.

## Style
Short and scannable. Max ~3 lines per paragraph on a phone (about 35 words). Plain, mature, confident workshop voice. Malaysian English, metric. "Est. 2010" / "our workshop since 2010" only for the workshop (never say the Sdn Bhd dates from 2010).
Each service page: the FIRST TWO SENTENCES of intro[0] say what we do and that the workshop is at Jalan Hang Lekir 12, Taman Industri Jaya, Skudai.
Translation will be done cheaply later, so keep sentences simple and literal-friendly.

## JSON shape (exactly these keys)
```
{
 "services": {
  "<slug>": {
   "title": "starts with the keyword, < 60 chars total, carries a fact (Skudai / Taman Industri Jaya / Est. 2010)",
   "meta": "one sentence, 140-160 chars: keyword + benefit + 'WhatsApp us' CTA",
   "h1": "contains the keyword, <= 10 words",
   "nav": "2-3 word short name for menus",
   "tile": "one line for the home service board, <= 9 words",
   "kicker": "6-8 words, shown in italic under the H1",
   "intro": ["paragraph 1 (2-3 sentences, first two as above)", "optional paragraph 2"],
   "sections": [
     {"h2": "...", "paras": ["..."], "bullets": ["short real items from facts.md"], "media": "<media id or null>"}
   ],               // 3-5 sections
   "faqs": [{"q": "...", "a": "1-3 sentences, ONLY from facts.md"}],   // 3-5; omit any FAQ facts.md cannot answer
   "wa": "WhatsApp prefill, e.g. Hi Sheng Heng, I'd like to ask about ADAS calibration for my car.",
   "schema_name": "Service name for schema",
   "schema_desc": "one sentence for Service schema"
  }
 },
 "areas": {
  "<slug>": {
   "title": "< 60 chars, e.g. Car workshop near Bukit Indah | Sheng Heng, Skudai",
   "meta": "one sentence 140-160 chars with WhatsApp CTA",
   "h1": "<= 10 words, e.g. Car workshop near Bukit Indah and Perling",
   "nav": "cluster short name, e.g. Bukit Indah & Perling",
   "intro": ["2-3 sentences: the cluster, about X km from 17 Jalan Hang Lekir 12 (straight line), what drivers here bring in"],
   "setting": ["1-2 short paragraphs of genuinely local context: the cluster's real setting and 2-3 real roads / landmarks, given below. No drive times."],
   "why": ["1 short paragraph: which of our real services matter for drivers here, e.g. warning lights, ADAS after windscreen work, continental servicing"],
   "faqs": [{"q": "...", "a": "..."}],   // exactly 2, e.g. 'How far is the workshop from X?' (about N km straight line from Jalan Hang Lekir 12, Taman Industri Jaya) and 'Can I WhatsApp a photo of the warning light first?' (yes, WhatsApp 016-335 2124 ... no, do not write the number; say 'WhatsApp us')
   "wa": "Hi Sheng Heng, I'm in <area> - can I bring my car in?  (use a comma not a dash)"
  }
 },
 "pages": {
  "about": {"title","meta","h1","kicker","intro":[...],"sections":[{"h2","paras","bullets","media"}]},   // the Jalan Hang Lekir 12 workshop, since 2010, Mr. Yaw, the kind of work, makes, hours, legal line (Sheng Heng Auto Service (M) Sdn Bhd, SSM 202401053168 (1599010-M)). No team size.
  "contact": {"title","meta","h1","kicker","intro":[...]},          // short; the template adds the map, hours, numbers, email, Facebook, AhaPay
  "articles": {"title","meta","h1","intro":[...]},                  // hub shell: articles coming soon, written from real jobs at the workshop
  "home": {"title","meta","h1","kicker","faqs":[...3-4]}            // title starts "Car workshop Skudai"; h1 like "Continental & Asian Car Workshop in Skudai"; kicker "ADAS, ECU, coding and gearbox since 2010" style (no middle dots, no dashes)
 }
}
```

## Pages and their keyword (title starts with it)
- continental-car-specialist-skudai: "Continental car specialist Skudai". BMW, Mercedes-Benz, Porsche, VW, MINI, Peugeot servicing and repair. Real jobs: BMW B48 valve stem seals (media g03), BMW turbochargers removed for repair (w04), BMW 5 Series on the lift (g02), Porsche Macan S / Mercedes C250 full service, Mini Cooper S radiator-fan temperature programming, VW Passat DCC programming.
- adas-calibration-skudai: "ADAS calibration Skudai" (also mention Johor Bahru as region). Camera/radar calibration after warnings or windscreen work. Real cases: Toyota pre-collision system malfunction warning (w01), Toyota Alphard in the bay (g01), BMW (our Facebook reel, media "video"), Honda CR-V P2583, Nissan Navara windscreen camera, Porsche Cayenne / Panamera. No equipment brands, no "dealer" claims.
- ecu-repair-programming-skudai: "ECU repair Skudai". ECU repair, ECU programming & coding, Online SCN coding (Mercedes), immobilizer resetting. Media: w01 or "pair:p02". No part numbers.
- car-key-immobilizer-skudai: "Car key programming Skudai". Smart key copy / programming (e.g. Toyota Vios NCP150), immobilizer reset. Stan G's review mentions a key tumbler wear-and-tear fix: you may quote this exact fragment in quotes: "Also fixed for another day for key tumble wear-and-tear." Media g05. Keep it short and real (3 sections).
- car-coding-instrument-cluster-skudai: "Car coding & meter repair Johor Bahru" (title may start "Car coding & meter repair, Skudai JB"). BMW 3 Series full LCD cluster change ("pair:p02"), Mercedes meter screen repair ("pair:p01"), BMW M steering-wheel retrofit (w03, g04), Mercedes C200 W205 AIRMATIC disable/coding, VW Passat DCC programming.
- gearbox-overhaul-skudai: "Gearbox overhaul Skudai". Lexus GS300 (GRS190), Hyundai Sonata, BMW X5/X6 transfer case rebuild, CVT K114 final-gear bearings (g07, Koyo bearings shown), friction plates OEM vs original (g06), clutch plate wear (w05).
- car-diagnostic-skudai: "Car diagnostic Skudai". Computer diagnostic and electronic trouble-shooting: warning lights, ABS pump/module repair (VW Golf; Stan G's Honda Shuttle 2015 ABS pump, may quote "Great service and turnaround in 1 for replacing ABS pump failure that had been causing dashboard indicators kept on lit up." exactly), smoke leak test (Honda Civic), Peugeot 308 P0016, Ford Focus steering lock, VW Beetle CD screen. Media w01.
- car-service-skudai: "Car service Skudai". Engine oil (our recommended interval 5,000 to 10,000 km, their own words), gear oil (every 20,000 to 40,000 km, our recommended interval), full service (Toyota Alphard w02, Camry ACV30, Ford Raptor), brakes, battery, tyre check, shock absorbers (Toyota Altis), lower arm, hybrid car maintenance & hybrid battery service, aircon (list only). Mention "Pay by instalment with AhaPay" once (no tenure/interest).

Media ids you may use in "media": h01, g01..g07, w01..w05, "pair:p01", "pair:p02", "video" (ADAS page only), or null. Use each page's listed media; 2-4 media across a page.

## Areas (straight-line km from the workshop; say "about X km")
1. taman-industri-jaya-nusa-bestari-selesa-jaya: Taman Industri Jaya 0.7, Taman Nusa Bestari 1.4, Taman Selesa Jaya / Skudai Baru 1.5. Walk-in neighbours. Roads: Jalan Hang Lekir, Jalan Bistari, Jalan Skudai.
2. taman-universiti-mutiara-rini-lima-kedai: Mutiara Rini 2.7, Lima Kedai 2.7, Taman Universiti 4.4, UTM Skudai about 6.6. Roads/landmarks: Jalan Pendidikan, Jalan Utama, UTM campus.
3. tun-aminah-sutera-utama-impian-emas: Taman Ungku Tun Aminah 3.2, Taman Sutera Utama 3.6, Taman Impian Emas 6.7. Roads: Jalan Bentara, Jalan Sutera, Lebuhraya Skudai.
4. bukit-indah-perling: Bukit Indah 3.0, Taman Perling 4.6. Roads/landmarks: Jalan Indah, AEON Bukit Indah, Jalan Persisiran Perling.
5. iskandar-puteri-medini-gelang-patah: Iskandar Puteri 6.1, Gelang Patah 8.2, Medini 9.9. Roads: Lebuhraya Iskandar / Second Link highway corridor, Medini, Gelang Patah town.
6. tampoi-kempas-larkin: Tampoi 6.8, Kempas 7.8, Taman Damansara Aliff 9.1, Larkin 11.1. Roads: Jalan Tampoi, Jalan Kempas Lama, Larkin.
7. senai-kangkar-pulai-sri-pulai: Taman Sri Pulai 7.4, Kangkar Pulai 8.5, Senai 11.2. Roads: Jalan Kulai-Skudai (write "Jalan Skudai-Kulai" with a hyphen), Senai town, Kangkar Pulai.
Each area must read genuinely different (different angle per cluster: walk-in neighbours; student/university family cars; housing estates & highway commuters; Bukit Indah shopping & Perling coastal; Iskandar Puteri new township & Second Link; Tampoi/Kempas/Larkin city-side commuters; Senai airport/industrial & Pulai). No customer names, no drive times, no pickup claims, no invented landmarks beyond the ones given (you may say generic things like "housing estates", "shophouses").

Return when the file is written and valid JSON (check with python3 -c "import json;json.load(open(...))"), and run this grep on it, fixing any hit: grep -n -i -E "seri orkid|\bbest\b|guarantee|warranty|authori[sz]ed|dealer|korean|RM ?[0-9]|shopee|restoration|no\.1|number one|placeholder|todo|lorem|—|–" . Report only "done" plus any fact you were unsure about.
