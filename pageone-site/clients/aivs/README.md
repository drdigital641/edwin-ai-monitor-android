# AIVS, AI Vending Solution Pte. Ltd. (aivs) — preview build

New client (16 Oct 2026). Existing site: aivs.sg (WordPress/Elementor, 11 URLs, scraped 16 Oct 2026 via the Bluehost Bridge sandbox because the container cannot reach aivs.sg).
Business: sells refurbished self-service vending machines to owner-operators (0% royalties, cost-price stock, training, support plan) and places them. Two machines: AI Printbox (3-min phone case printing, from S$5,000, 14 mall/airport locations) and Topi Express (5-min helmet cleaning, from S$1,800, 6 motorcycle-shop locations).
Preview: https://pageonesingapore.com/preview/aivs/ (bridge site "pageone", folder preview/aivs). Noindex until go-live.

- `build.py` writes all 26 pages into `site/` (facts, sources and CONFIRM list at the top). Photos: the client's own, downloaded from aivs.sg uploads, resized to webp (sandbox PIL), 25 photos ~1.3 MB.
- Pages: home, /machines/ + 2 machine pages, /services/ + 4 (own-a-vending-machine, support-and-maintenance, host-a-machine, custom-branding), /locations/ + 2 (per machine, all addresses), /prices/, /articles/ + 8, /about/, /contact/ (WhatsApp enquiry form), /terms/, /privacy/, 404. Schema: Organization+LocalBusiness with Offers, Product per machine, Service, FAQPage, Article, ItemList (locations), Breadcrumb. llms.txt, sitemap, robots (AI bots allowed), htaccess.txt with 301 map from the old WordPress URLs (go-live, via cPanel).
- Theme: charcoal + gold (their logo), pink accent for AI Printbox, teal for Topi Express. aivs.css / aivs.js adapted from EC Coffee Bar (reveal, hero slideshow, ticker, count-up, tilt).
- Deliberately NOT claimed: "Proven monthly revenue $3,000+" from the old homepage, ROI timeframes, review ratings, the AI Shieldbox machine (in photos, not described), the second phone number 8335 4865.
- Build/upload from the scratchpad copy (files under /mnt/project-files gain C2PA metadata).

## Facts (16 Oct 2026)
ACRA via opengovsg/recordowl: AI VENDING SOLUTION PTE. LTD., UEN 202439764G, inc. 27 Sep 2024, live, exempt private company, 60 Jalan Lam Huat #05-55 Carros Centre S737869 (former name Foot N Tip Wellness Group; SSIC 18112 primary, 95301 secondary). Contact from their site: WhatsApp +65 8878 4061, info@aivs.sg, Sales@topiexpress.sg; FB/IG/TikTok/YouTube aivendingsolution.

## To confirm with the client: see CONFIRM in build.py.

## Go-live
Addon domain aivs.sg -> preview/aivs folder, DNS from the WordPress host, AutoSSL, LIVE=True in build.py, rebuild, re-upload, htaccess.txt -> .htaccess via cPanel (301s from old URLs), Search Console + Bing, add to EDGE daily articles + backlinks tracker, GBP website link.
