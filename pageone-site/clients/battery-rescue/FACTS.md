# Battery Rescue SG: fact sheet (draft, 26 Oct 2026)

Source: Edwin's message of 26 Oct 2026 plus the files in data/. Nothing is built yet.
Items marked CONFIRM must be answered before anything goes live (MASTER-RULES rule 2: verifiable facts only).

## Business
- Brand: Battery Rescue SG (batteryrescue.sg), by Motoserv ("Neighbourhood Car Service Centre"; motoserv.sg, fb.com/motoserv.sg, tiktok.com/@motoserv.sg)
- Battery brand sold: DELKOR only. Amaron is NOT sold (the Amaron/Nam Wah guide is used only as fitment reference)
- 24-hour hotline: 8125 9169
- CaseTrust-accredited workshop (supplier Ktech's wording). CONFIRM: which legal entity holds CaseTrust, and is it on the CaseTrust public list?
- Warranty: 1 year (confirmed). CaseTrust holder: Motoserv group (per poster). WhatsApp = hotline 8125 9169 (assumed).
- CONFIRM: exact legal name and UEN of the Motoserv entity.

## Prices (Delkor official list, incl. GST; this is the Motoserv shop price)
| Size | Ah | List price |
|---|---|---|
| NS40ZL (42B20L) | 38 | $119.90 |
| NS60L (65B24L) / NS60LS (65B24LS) / NS60ST (65B24R) | 50 / 50 / 45 | $130.80 |
| 85D23L | 65 | $174.40 |
| 100D26L | 75 | $207.10 |
| 130D31L / 130D31R | 100 | $239.80 |
| DIN45L | 45 | $152.60 |
| DIN60L / DIN66L / DIN74L | 60 / 66 / 74 | $207.10 / $218.00 / $239.80 |
| EFB-N55 / EFB-Q85L / EFB-S95 / EFB-LN2 / EFB LN3 | | $196.20 / $228.90 / $272.50 / $239.80 / $261.60 |
| AGM LN1 / LN2 / LN3 / LN4 / LN5 | | $250.70 / $283.40 / $337.90 / $414.20 / $468.70 |
| M42 (60B20L) | 40 | $174.40 |

## Price tiers (CONFIRMED by Edwin 26 Oct 2026 except where marked)
1. Walk-in at any of 10 Motoserv workshops, Mon-Sat 9am-6pm: list price minus $20 with the website code. Example NS40ZL $119.90 - $20 = $99.90.
2. Onsite replacement, any day incl. Sunday, before 10pm: list price + $50 onsite fee. Example NS40ZL $169.90.
3. Night (10pm-9am) and public holidays: list price + $80. Example NS40ZL $199.90.
- $50/$80 is ADDED to the battery price (confirmed). Site wording: "battery price + $50 onsite fee", never "onsite replacement from $50".
- $20 website code is for workshop walk-ins ONLY (confirmed), not onsite.
- CONFIRM: one fixed public code (e.g. RESCUE20) or a unique code per customer?

## Workshops (Motoserv locations image)
Bukit Batok (28 Bukit Batok East Ave 6), Bukit Panjang (772 Upper Bukit Timah Rd), Boon Lay (2 Boon Lay Ave), Sembawang (595 Sembawang Rd), Toa Payoh (248 Lor 1 Toa Payoh), Havelock Rd (548 Havelock Rd S169637), Bukit Timah (219 Upper Bukit Timah Rd), Upper Thomson (553 Upper Thomson Rd S574416, at Mobil One CarCare), Jervois (2 Jervois Rd S248994), Serangoon Garden (49 Serangoon Garden Way S555944). All others are at Shell Autoserv stations.
- Site may name the station as an address landmark; no Shell/Mobil logos (brand rule).
- CONFIRM: postal codes for the 6 without one; does each workshop have its own Google Maps profile?

## Fitment data check (data/fitment-draft.csv)
- Guide: 2,105 car rows, 60 makes. 73% map to a Delkor size on the list.
- No Delkor match for: DIN80L (213 rows), DIN100L (116), 80D26R (67), 85D23R (45), DIN55L flooded (42), 42B20R (25), 55B24RS (37). Ask the supplier which Delkor size replaces each.
- The guide is an Australian-market list (Holden, Ford Falcon...). Many common Singapore cars are MISSING: Toyota Corolla Altis, Wish, Sienta, Alphard/Vellfire, Harrier, Axio/Fielder; Honda Vezel, Freed, Shuttle, Stream. Motoserv needs to supply sizes for these from their own job records.
- NS60ST (65B24R): CONFIRM whether this is the R or RS (small terminal) version.

## Tracking (Edwin, 26 Oct 2026)
- Count every Call tap, WhatsApp tap and promo-code reveal (use /mnt/project-files/tracking/wa-tap-counter.js, extended for call + code events), each with page, car, battery size and tier.
- Promo code: plan is a short unique code per reveal (e.g. BR-7K3Q), $20 off, walk-in only, so redemptions at the workshops can be matched to website reveals. Workshops need a simple way to log a redeemed code. CONFIRM with Motoserv.

## Answers 26 Oct 2026 (Edwin)
- Sizes with no Delkor match (DIN80L, DIN100L, 85D23R, 80D26R, 42B20R, DIN55L flooded, etc.): finder shows "Battery not listed - tap to enquire" (WhatsApp/call CTA, counted).
- SG/JDM models: use data/bateriku-astra-chart-2023.pdf (Malaysian Bateriku/Astra chart, image-only poster; transcribe it). Examples read: Altis 2006-18 NS60L, 2018+ DIN45L; Wish 2009-11 NS60L, 2011-15 55D23L (Q85 start-stop); Sienta NS60L; Alphard 2013-16 80D26L, 2018+ S95/Q85; Vezel 2015-21 55B24L, hybrid 2019+ M42L; Freed 2016+ NS40ZL. Honda Shuttle is NOT in the chart -> enquire.
- Mapping notes: 55B24L->NS60L, 55D23L/70D23L/75D23L->85D23L, 80D26L/NS70L->100D26L, M42L->M42, Q85->EFB-Q85L, S95->EFB-S95, DIN75L->EFB LN3 or DIN74L (CONFIRM), NS60R->NS60ST? (CONFIRM), R-terminal D23/D26 and NX120 -> enquire.
- Honda Shuttle: follow Vezel (Edwin, 26 Oct 2026): petrol NS60L (55B24L size), hybrid M42.

## UX rules (Edwin, 26 Oct 2026)
- "Stuck now" path: almost no reading. Big Call + WhatsApp buttons first screen; car pick optional; location by one tap (GPS) or skip; price shown as one line. Works one-handed in a car park.
- "Comparing prices" path: show the walk-in price after the $20 code clearly (e.g. NS40ZL $99.90 vs $119.90 list), list all 10 Motoserv outlets nearest first with address, hours (Mon-Sat 9am-6pm), map link and the exact price at that outlet; customer picks an outlet, then gets the code.
- App feel (Edwin, 26 Oct 2026): phone-first app shell, not a website look: bottom tab bar (Rescue / Prices / Outlets / More), sticky bottom action bar (Call, WhatsApp), big tap targets, installable (manifest, add to home screen). Emergency = phone only; Compare = phone and desktop (desktop gets two columns: finder + outlet list).
- Brand trust (Edwin, 26 Oct 2026): say clearly every battery fitted is DELKOR, with a "About Delkor" page/section + link. Verified facts: made by Clarios Delkor (formerly Johnson Controls Delkor Battery Corporation), Korea; Korean Standards Association KS-QEI Quality Excellence award, 16th consecutive year in 2021 (source rjbatt.com.au 29 Nov 2021); first Korean maker to supply maintenance-free batteries (mining-technology.com press release). No official Delkor site reachable yet: link those sources until the client gives the official URL.
- Rescue (on-site) area (Edwin, 26 Oct 2026): Woodlands, Sembawang, Yishun, Punggol, Sengkang, Ang Mo Kio, Yio Chu Kang, Hougang. From 2027: east (Tampines, Eunos etc.). West TBC. Walk-in outlets stay all 10.

## Other services (client via Edwin, 26 Oct 2026; LIVE on preview 26 Oct)
- Main service and SEO focus stays: Onsite Car Battery Replacement Singapore.
- Jump-start: $50 ($80 PH). Night rate not stated by client; site shows only "$80 on public holidays".
- Emergency towing: $80-100 normal, $120-150 king dolly (4-wheel). Site shows "From $80" / "from $120" (From-price rule).
- Disclaimer (shown on home, rescue, prices, service pages): technician attends, issue not battery-related -> onsite service fee $50 to $80. Final charges depend on location and service requirements.
- Pages: /services/jump-start/, /services/towing/ (Service schema, WhatsApp enquiry + call buttons, FAQ).

## Same-size matches (Edwin asked 1 Nov 2026: fill "ask" prices)
Matched by standard case size (EN L-sizes / JIS codes) to the nearest Delkor size on our list; the finder shows "Your car's size is X. Same ... size." EQUIV in build.py.
- DIN80L -> AGM LN4 (L4, AGM upgrade); DIN100L -> AGM LN5 (L5, AGM upgrade); DIN55L -> DIN60L (L2); DIN75L -> DIN74L (L3)
- NS60R / 46B24R / 55B24R / S46B24R -> NS60ST (65B24R); 85D26L -> 100D26L
- "DIN60/70 AGM or EFB" -> AGM LN2/LN3 (AGM suits both)
- Still "enquire" (63 rows): right-terminal D26/D23/B20 (NS70R, 80D26R, 85D23R, 42B20R, M42R), DIN45R/55R, N120, T110, DIN65L, twin-battery cars. No same-size Delkor on the price list. CONFIRM with Motoserv if they stock R-terminal D26/D23.

## Launch promo (Edwin, 7 Nov 2026)
- Fitted at your location before 10pm, incl. Sunday: list price + $30 (launch promo: $20 off the usual list + $50). Shown as the usual price struck through (<s>) with the promo price beside it, label "Launch promo: $20 off before 10pm, incl. Sunday".
- Night 10pm-9am and public holidays: unchanged, list + $80, no promo.
- Unchanged: walk-in $20 website code (list - $20, Motoserv Mon-Sat 9am-6pm), jump-start $50/$80 PH, towing, $50-$80 non-battery onsite fee.
- No end date set. Schema Offer price = promo price, no "was" price in schema.
- In build.py: day() = promo, dayw() = usual, md(k) = struck + promo token (promo_html/promo_txt/promo_short render it).
