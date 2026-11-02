# CSKA Auto Enterprise website (preview)

- Preview: https://pageonesingapore.com/preview/cska-auto/ (hidden from Google by the preview folder's X-Robots-Tag header; pages themselves are index,follow).
- Bridge site "pageone", folder preview/cska-auto. Images on jsDelivr: drdigital641/edwin-ai-monitor-android@2f91c78/site-assets/cska-auto/ (42 handover photos from their own Facebook reels, logo from the name card, favicon, share image).
- Build: `python3 build.py` writes site/. Styles cska.css, script cska.js. 28 pages: home, products hub + 9 product pages, brands hub + THINKCAR/Autel/TOPDON/SP ZONE, handovers, support, guides hub + 6 guides, about, contact, privacy, 404.
- Controller: Client "CSKA Auto Enterprise", slug cska-auto, status preview. IndexNow key 208f285bfeaaa073ac0b7bb77afc1625.
- Daily system: seo-method/rollout/cska-auto.md (article queue), seo-method/backlinks/cska-auto.md.

## Sources (checked 19 Oct 2026)
- Name cards Edwin sent (Steven Chai, Kai Kiat), Edwin's note (Ah Yii 9037 2820, workshop customers, authorised distributor of a few products).
- ACRA via data.gov.sg: CSKA AUTO ENTERPRISE PTE. LTD., UEN 202127592M, incorporated 7 Aug 2021, registered at 101 Woodlands Ave 12 #07-03B S737719, SSIC 46599 / 46563.
- Facebook (logged out): facebook.com/chai.steven.393 and facebook.com/kiat.ah.712675, about 180 reels. Their brand card video: THINKCAR, AUTEL, TOPDON, SP ZONE, STIRLING, ThreeBond, Ingersoll Rand + one unclear German lubricant logo. Model specs are from their own posts (which quote the makers). Alvis Kiew's title is from their video name card. The third link Edwin sent (a story) needs login and was not read.

## CONFIRM with CSKA (left off the site until answered)
1. Which brands they are authorised distributor for (site says "authorised distributor for several of the products it sells", no brand named).
2. Opening hours; is Polaris @ Woodlands a showroom (walk-ins, demos) or office only.
3. Domain: cskatrading.com (Edwin added it 19 Oct; set DOMAIN in build.py at go-live).
4. Permission to name the customer workshops in photos (names left out; Edwin Garage is named on one photo caption as Edwin's own workshop - remove if not wanted).
5. Top Dealer Award from Speed Car Auto Parts (SP ZONE): year.
6. The German lubricant brand on their brand card (reads like "ARZOIL").
7. Do they offer TPMS programming / ADAS calibration as a service, or tools only.
8. What a purchase includes: delivery, installation (lifts, aircon machines), training.
9. Their own warranty / repair handling on top of the makers'.
10. Company Facebook page, TikTok, Xiaohongshu, Google Business Profile?
11. Any prices or promotions to publish.

## Go live
Set DOMAIN and LIVE=True in build.py, rebuild, upload to the domain folder, add htaccess.txt as .htaccess via cPanel, activate in the Controller.
