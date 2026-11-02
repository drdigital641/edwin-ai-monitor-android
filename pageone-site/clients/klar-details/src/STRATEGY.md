# Klar Details: competitive analysis and revamp strategy (1 Nov 2026)

Preview: https://pageonesingapore.com/preview/klar-details/ (46 pages, hidden from Google by the preview folder header).
Research: research/content-inventory.md (their site, 23 posts, media), research/competitors.md (9 SERPs, 6 competitor profiles), research/media.md.

## 1. Where Klar stands today
- Google (SG, 1 Nov 2026): not in the top 20 for "car detailing singapore" (720/mo), "ceramic coating singapore" (390), "car polishing singapore" (320), "car grooming singapore" (260), "interior car cleaning singapore" (170). Footholds: #3 "ceramic coating jurong east", #5 "graphene coating singapore" (blog post), #7 "car grooming jurong". In no local pack, in no listicle. About 42 organic visits a month, 63 keywords.
- Site: WordPress/Elementor, one services page, three thin KlarCOAT/INTERIOR/MAINTENANCE pages hidden from the menu, no prices except the S$88 trial, no warranty terms, no schema, no H1, logo linking to a raw IP, "30+ years" next to "since 2014", two different opening hours, About counters showing "0 +", leftover shop/checkout pages.

## 2. Who wins and why (full detail in research/competitors.md)
| Competitor | Why they win | Where they are weak |
|---|---|---|
| Lambency (Ubi + Bukit Batok) | Local pack in 6 of 9 SERPs, #1 for "car detailing singapore", page per service, SONAX partner, accreditation strip | No warranty terms, price ranges only, typos, no FAQ on service pages |
| Revol Carz (Blk 42 Toh Guan, same estate as Klar) | 7,000+ Google reviews at 4.8, 14 sgCarMart awards, prices from S$688 with 36-month warranty, heavy blog | Inconsistent prices and hours, workshop/spray focus dilutes detailing |
| MintGroom (Millenia Walk) | 16 service pages, 500+ reviews, PPF strength | Prices hidden, no warranty, single central location |
| Zenith, Car Armour | One page per coating; Car Armour publishes full size-band prices | No address / mobile only, contradictory warranty claims |
| EA Detailer, Motorist, GetGo listicles | "Best ceramic coating 2026" rankings take page one for money terms | Klar is in none of them |

What nobody does well: a clear price-and-warranty page, written aftercare, local pages for Jurong East / Bukit Batok / Clementi / Boon Lay, consistent facts, schema, deep FAQs per service.

## 3. Why a customer should choose Klar (the positioning built into the preview)
1. **Detailing only, in enclosed bays.** Not a workshop that also polishes. At least six man-hours per Signature treatment, infrared curing, pure-water final rinse.
2. **A fixed quote before work starts, no hard sell** (a customer's own words). Free assessment at Toh Guan Road East.
3. **In-house lines you can try first:** KlarCOAT, KlarGRAPHENE, KlarINTERIOR, KlarMAINTENANCE, KlarSHIELD, and the S$88 graphene bonnet trial (nobody else offers a paid try-before-you-buy).
4. **EV-ready:** in-house EV charging, EV-safe processes, Tesla / BYD / Polestar jobs in the gallery.
5. **Backed by MK Group**, sister brands for servicing (Motoserv), aircon (Mr Kool), gearbox.
6. **Facts that agree everywhere:** one address, one set of hours, one phone, one WhatsApp, on every page, in schema and llms.txt.

## 4. Site structure (one page per intent)
Home (lean) · /services/ + 8 service pages (ceramic, graphene, paint correction, interior, interior pest control, coating maintenance, new car and EV, premium hand wash) · /graphene-bonnet-trial/ · /areas/ hub + Jurong East, Bukit Batok, Clementi, Jurong West and Boon Lay · /prices/ (how a quote is built; S$88 is the only number until Klar confirms prices) · /our-work/ · /reviews/ (6 verbatim reviews, no rating schema) · /about/ · /faq/ · /articles/ (20 guides rewritten from their 23 posts, two duplicate pairs merged, the self-promotional "Top 5 workshops" dropped, old slugs kept so 301s are one-to-one) · /products/ and /franchise/ (new, from Edwin 1 Nov 2026) · /contact/ · /privacy/ · 404, sitemap with lastmod, robots.txt naming all AI bots, llms.txt, IndexNow key, JSON-LD on every page (AutoDetailing, Service, Offer, FAQPage, Article, Breadcrumb).

## 5. Keyword plan
| Priority | Keyword | Volume | Owner page | Goal |
|---|---|---|---|---|
| Now (West) | ceramic coating jurong east (Klar #3) | low, real | /areas/jurong-east/ + /services/ceramic-coating/ | #1 organic + local pack |
| Now (West) | car detailing jurong, car grooming jurong (Klar #7) | low, real | /areas/jurong-east/, /areas/jurong-west-boon-lay/ | page 1 |
| Now (West) | car detailing bukit batok / clementi / toh guan | no data, no owner | area pages | own them first |
| Next | graphene coating singapore (Klar #5) | 90 | /services/graphene-coating/ + trial page | top 3 |
| Next | interior car cleaning singapore, car interior detailing singapore | 170 + 50 | /services/interior-detailing/ | page 1 |
| Then | car polishing singapore, paint correction singapore | 320 + 20 | /services/paint-correction/ | page 1 |
| Then | ceramic coating singapore, ceramic coating price singapore | 390 + 20 | /services/ceramic-coating/, /prices/ | page 1 |
| Long | car detailing singapore, car grooming singapore | 720 + 260 | home + guides | top 10 |

## 6. What wins the local pack (not on the website)
Google Business Profile: correct category (Car detailing service), services with prices, weekly photo posts, a review drive to 100+ (Revol next door has 7,000), Q&A seeded with the FAQ, the S$88 trial as an Offer post. Bing Places and Apple Business Connect with the same facts. Listicle pitches: Motorist, GetGo, SBO, rating.sg, sgCarMart Star Merchant. Daily Klar article after go-live, IndexNow daily, weekly AI visibility check (ChatGPT and Perplexity currently name Lambency, Revol, MintGroom).

## 7. The one lever that beats everyone: publish prices and written warranty terms
Every top competitor either hides prices or contradicts itself. The preview has the slots ready (/prices/, price box on each service page). Klar only needs to confirm: from-prices by car size for KlarCOAT, KlarGRAPHENE, paint correction stages, KlarINTERIOR, KlarMAINTENANCE, and the warranty / cover terms per coating. See CONFIRM in content/pages.py (27 items).

## 8. Feb 2027 and beyond (Edwin, 1 Nov 2026)
- Move to Carros Centre (MK Group HQ, Woodlands) in Feb 2027: the build keeps all facts in one place (build.py ADDR/HOURS, schema, llms.txt), so the move is a one-line change plus a Woodlands / Sembawang / Yishun area set and 301s. The Jurong area pages become "we moved" pages pointing North. Not published until Klar confirms the date.
- Merchandise branding and Klar products: /products/ is live in the preview as a register-interest page; it becomes a catalogue (Base44 app, like Autotex) once product names, contents and prices exist.
- Klar franchise: /franchise/ is live in the preview as an enquiry page; add a partner deck and territory list when terms are set.

## 9. Go-live steps
Domain stays klardetails.com.sg: point it at the new folder, upload htaccess.txt (https, www, 301s for every old URL), copy the client's images and video onto the new host (preview references them from the current site), replace the generated K-mark favicon and og.jpg with Klar's real logo files, GSC + Bing verification, GBP link, add the domain to both crawler monitor lists, join the nightly loops.
