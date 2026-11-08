# Dongfeng Johor Bahru (dongfeng-jb): preview build

New client from Edwin, 19 Oct 2026. First Malaysian client. Dongfeng passenger-EV 3S centre (sales, service, spare parts) in Johor Bahru, run by **MyKar World Sdn. Bhd.** (202501050786, 1652194-X). Edwin's message said "Tong Fong"; he corrected it to **Dongfeng**.

**Preview:** https://pageonesingapore.com/preview/dongfeng-jb/ (bridge site "pageone", folder preview/dongfeng-jb). Hidden from Google by the preview/.htaccess X-Robots-Tag header; no noindex meta in pages (rule 4.3).

## What the client wants (Edwin's message + 4 Mandarin voice notes, transcribed 19 Oct 2026)
1. Sell the cars. Two passenger EVs only: **Dongfeng Vigo** (SUV) and **Dongfeng 007** (sedan). Colours and full specs came from Gavin (client staff) on 19 Oct 2026.
2. Online presence for the Johor centre. Voice note: "We are Dongfeng's 3S centre, currently Johor's first and only 3S centre."
3. Partnerships: "we hope big brands notice us and work with us" (Edwin: get dealers to cooperate). -> /partners/ page (dealers, brands, fleets).
- Test drive: WhatsApp appointment only. **No prices** ("price, not for now").
- Three languages: English (/), Bahasa Melayu (/ms/), Simplified Chinese (/zh/), hreflang en-MY / ms-MY / zh-MY + x-default.
- Luxury feel: dark + ivory theme, Dongfeng red accent, gold eyebrows, Jost font, big photos.

## Files
- `build.py` writes `site/` (48 pages = 16 x 3 languages + 404, sitemap with hreflang, robots with AI bots, llms.txt, manifest, IndexNow key). Facts, sources and CONFIRM list at the top. `COLOURS` dict: `(name, hex, cut-out photo or None)`; model pages show a tap-to-change colour picker. `OFFICIAL` dict = official photos from the client's Drive (served from site-assets commit 6f50fa4 via `IMG2`; older photos stay on `IMG` 0678e88 so unchanged pages keep identical bytes).
  - Local test build: `DF_OUT=<dir> DF_IMG=<url> python3 build.py`. Build/upload from a scratch copy; copy `favicon.ico` from site-assets.
- `df.css`, `df.js`: theme, reveal-on-scroll (only below-fold items), gliding photo carousel, WhatsApp enquiry forms. No count-ups (rule 4.12).
- `htaccess.txt` for go-live (www/https, index.html 301, 404, X-Robots-Tag only on the preview host).
- Official photos: client's Google Drive (drive.google.com/drive/folders/1SLW8PzJ4JqK7dCT0lhsa6B1Vy63qu4iC), 007 and Vigo folders only; 38 picked, resized to webp (1200-1600 px), colour cut-outs keep transparency. Skipped: ChatGPT/Gemini-generated images, shots with the Chinese-market badge, videos. Edwin (19 Oct 2026): Voyah Dream added as **coming soon** (/models/voyah-dream/, 3 photos, site-assets commit f8b49d4 via `IMG3`; facts only from Dongfeng Malaysia's KLIMS 2026 preview, no specs/price/date). 008 and MHero must NOT be listed publicly: their photos (deduped webp) sit unlinked on the server at preview/dongfeng-jb/_hold-7k3q/008/ and /mhero/ (not in sitemap, no links). MHero files are named 'Dual-car AI image' in the Drive (AI renders).
- Showroom photos: their own Facebook photos (1024px crops max, logged-out FB only serves those) + their cover banner. jsDelivr: repo drdigital641/edwin-ai-monitor-android, branch site-assets, folder site-assets/dongfeng-jb, commit 0678e88.
- Pages: home, /models/ + vigo + 007, /test-drive/, /service/, /spare-parts/, /partners/, /articles/ + 4 (3S centre explained, Vigo vs 007, EV test drive checklist, home charging in Johor), /about/, /contact/, /privacy/ (PDPA 2010).
- Schema: AutoDealer (legalName, SSM number, brand Dongfeng, sameAs FB), Car per model (no offers), Service, FAQPage = visible FAQs, Article, Breadcrumb.

## Sources
- Facebook facebook.com/dongfengjohorbahru (scraped logged-out via Bluehost Bridge Base44 sandbox Playwright, /tmp/pw): name, SSM no., address No.28 Jalan Ekoperniagaan 3/11 Taman Ekoperniagaan JB, +60 18-762 0828 (Yaya), marketing@mykar.my, mykar.my (does NOT resolve yet), 743 followers. Roadshows 2026: Sutera Mall (25-28 Jun), AEON Bandar Dato' Onn (4-9 Aug), Lotus's Tebrau (4-6 Sep), KIPMall Kota Tinggi. Merdeka 2026 kids' costume day at the showroom. Other staff numbers seen: Ivonne 010-596 1201, Gavin 012-551 2820 (hiring) - not used.
- Google Business Profile exists ("MyKar World Sdn Bhd", kgmid /g/11nc0ckknp); Google blocked reading it.
- Specs (since 19 Oct 2026): Gavin's WhatsApp (via Edwin) for Vigo Premier 120kW, 007 Long Range RWD Premium, 007 AWD Prime, incl. warranty 8 yr unlimited powertrain / 6 yr unlimited vehicle, colours, interiors. Overrides press where different (Vigo height 1,645; Prime range 463 km). NOT published: 007 "low to 80% in ~11 min" (impossible at 200 kW) - asked to confirm.
- Earlier specs: Dongfeng Cars Malaysia launch (Feb 2026) via autobuzz.my and carz.com.my; only figures that agree are used; CLTC labelled. The dealer's own posters disagree (386 km WLTP, copy errors on the 007), so posters were not used for specs.
- Dongfeng Malaysia (Central Auto Distributors Bhd via Volt Auto) announced 3S centres for Bangsar and Johor (autobuzz.my, 25 May 2026), consistent with the client's claim.
- Not used: the Dongfeng Box photos (client sells only two models), the "Panca Abadi" poster (another dealer), any price or instalment.

## CONFIRM (in build.py)
Status wording ("first and only"), hours, 007 range test cycle + 11-min charge claim, Sandstone Beige photo, service scope, parts sales, partnership offer, domain (mykar.my?), postcode 81100 + Maps pin, more real photos (front, service bay, team, handovers), IG/TikTok/Xiaohongshu.

## Malaysia search notes
- Google is the main engine in Malaysia; Bing feeds ChatGPT/Copilot. BM and Chinese pages target the same intent in each language (e.g. "pusat servis Dongfeng Johor Bahru", "新山东风").
- Off-page targets (white-hat): GBP (complete it, categories Car dealer / Electric vehicle dealer, photos, link to the site), Waze and Apple Maps listings, Bing Places, Dongfeng Malaysia official dealer locator (ask the distributor to list and link the JB 3S centre: the strongest link available), Carlist.my / Mudah.my dealer profiles, ZigWheels/Carbase dealer locators, mall roadshow pages, local press (JB EV coverage), Facebook + TikTok + Xiaohongshu for Chinese buyers.

## Go-live (only after Edwin says go)
Domain decision (mykar.my), addon domain -> preview/dongfeng-jb, LIVE=True + DOMAIN, rebuild, re-upload, .htaccess via pin/cPanel, Search Console + Bing, IndexNow, EDGE daily articles (3 languages?) + backlinks tracker, GBP website link.

## Fact-check round (19 Oct 2026)
Checked every spec against Gavin's sheet + Malaysian press (autobuzz, zigwheels, carsofmalaysia, paultan-style launch reports). 7 fixes live on preview (EN/BM/ZH + llms.txt):
007 Prime range hidden ("ask us"), Premium shown as up to 650 km CLTC; Vigo seat wording per sheet; Vigo sunroof neutral ("ask which cars in stock have it"); "flagship" Voyah wording softened; "launch figures" -> "the Malaysian figures"; home charging "about 9 hours on 6.6 kW"; unverified "sales team in EN/BM/ZH" line removed.
OPEN for Gavin: 007 Prime range (sheet 463 km vs press 565 km CLTC); Vigo panoramic roof (option vs standard); the "11-minute" charge claim; "first and only" wording. Kept per Gavin: Vigo height 1,645 mm (autobuzz says 1,654), Prime red calipers.

### Gavin's answers (19 Oct 2026, 18:16-18:34 MYT) - applied
- Showroom Mon-Sat 9am-6pm, Sun 10am-4pm; workshop Mon-Fri 9am-6pm, Sat 9am-1pm, Sun closed (visit block on home/contact + schema).
- 007 Premium 650 km CLTC / 530 km WLTP; Prime 565 km CLTC / 389 km WLTP; DC 30-80% in about 11 min.
- Vigo panoramic sunroof standard.
- Wording is "first Dongfeng 3S centre in Johor Bahru" (NOT "only", NOT "Johor's").
- Service every 10,000 km; service and parts at Dongfeng list prices (no figures shown).
- Instagram + TikTok links to come; no Xiaohongshu.

### Address (20 Oct 2026)
Edwin: follow the Google listing - 28, Jalan Eko Perniagaan 3/13, Taman Ekoperniagaan 2, 81100 Johor Bahru. Visit heading says "Eco Business Park 1, Johor Bahru".
UPDATE 20 Oct 2026 14:12 SGT (Edwin): official address is No. 28, Jalan Ekoperniagaan 3/11, Taman Ekoperniagaan, 81100 Johor Bahru, Johor. Applied site wide; the Google listing's 3/13 wording is not used.
- Edwin 20 Oct 2026: Google Business Profile https://share.google/Ku4wPPlRy8oDVCVyb = kgmid /g/11nc0ckknp (strong 5-star). Added as GBP in build.py: sameAs in schema, 'Our Google reviews' link in visit block (home + contact x3 langs), llms.txt line. Live: only home + contact pages got sameAs (other pages keep FB only until next full rebuild). No aggregateRating in schema (self-serving review markup not allowed by Google).
- 23 Oct 2026 (client via Edwin): two WhatsApp lines. Sales (new cars, promotions) stays +60 18-762 0828 / marketing@mykar.my; Service booking + aftersales + parts = SVC_NUM +60 18-224 0828 / aftersales@mykar.my. Visit block, footer, band (every page), mobile dock (Sales enquiry | Service booking), service/parts buttons, about table, schema contactPoint + AutoRepair dept, llms.txt.
- Full-site publish method (since 23 Oct 2026): build to scratch with DF_OUT, replace https://pageonesingapore.com/preview/dongfeng-jb/ -> https://mykar.my/ (and "/preview/dongfeng-jb/ -> "/ in 404.html), commit to branch dongfeng-site (folder dongfeng-jb/site), check the old build vs live first, then Bridge sync_from_github {site pageone, ref SHA, source_path dongfeng-jb/site, base_path preview/dongfeng-jb}. build.py LIVE stays False.
- 23 Oct 2026: WhatsApp tap counter (df.js v3) sends cta_type whatsapp_sales or whatsapp_service (by number). Controller totals count any type containing 'whatsapp', so both count; the Lead log shows which.

## Facebook carousel (8 Nov 2026)
Homepage "Latest from MyKar" is built from data/fb-posts.json + images/fb/. Standing rule: captions with prices, RM amounts, rebates, monthly payments, loan figures or the word "only" are hidden in code (build.py FB_HIDE, df.js HIDE). Details: data/README.md.
