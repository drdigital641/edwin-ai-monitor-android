# EC Coffee Bar (ec-coffee-bar) — preview build

New client (16 Oct 2026). Café, bar and event space at 40 Carpenter Street #01-01, Singapore 059919 (CBD, near Clarke Quay MRT).
Positioning (Edwin): CBD professionals; company events, team bonding, group celebrations; easy WhatsApp enquiry. Theme: cozy, relaxed, professional (cream, cocoa, logo pink).
Target preview: https://pageonesingapore.com/preview/ec-coffee-bar/ (bridge site "pageone", folder preview/ec-coffee-bar). Noindex until go-live.

- `images.py` crops photos from `source/` (her July 2025 menu PDF and Grab Dine Out photos) into `site/img/`.
- `build.py` writes all pages into `site/` (facts and sources at the top; DOMAIN/LIVE flags; CONFIRM list).
- Pages: home, events hub + 6 event pages (corporate events, team lunch, VIP room, celebrations, business breakfast, after-work drinks), menu hub + 4 menu pages with prices, 5 planning-guide articles, about, contact (event enquiry form that opens WhatsApp), 404. Schema CafeOrCoffeeShop+BarOrPub, Service, FAQPage, Article, BreadcrumbList. llms.txt, sitemap, robots (AI bots allowed).
- ec.css / ec.js adapted from New Zen Werkz (reveal, slideshow, ticker, count-up stats, tilt, wipe), all off for reduced motion.
- Screens for Edwin: screens/*.jpg.

## Facts
ACRA: EC COFFEE BAR PTE. LTD., UEN 202416189N, inc. 23 Apr 2024, SSIC 56112 cafés / 56111 restaurants. Instagram @eccoffeebar: hours Mon-Sat 8.30am-9pm, Sun 8.30am-8pm; text/WhatsApp 9365 6626; email eccoffeebar@gmail.com (IG typo "gamil", Edwin confirmed). Edwin: ~50 pax full capacity, VIP room ~10 pax. Menu PDF (Jul 2025): motto "Where Chicks Grow into Eagles", E for Entrepreneurs, C for Chick; Chinese name 创鸡咖啡吧; WeChat/TikTok/Xiaohongshu eccoffeebar. Grab lists different hours (Mon-Fri 8.30-10, Sat-Sun 9-10); IG used.
Not shown: Google rating (Eatigo says 4.9, no count), review quotes, buyout terms.

## How the preview was published (16 Oct 2026)
Uploaded file by file with the Bluehost Bridge write_file tool (site "pageone", path preview/ec-coffee-bar/...): text with `content`, images with `content_base64`. Images were recompressed to ~6-24 KB each (18 used images + icons, ~200 KB total) so base64 writes are practical. Build/upload from the scratchpad copy, not from this folder: files written under /mnt/project-files gain C2PA metadata (e.g. logo 6 KB -> 12 KB). No git needed. .htaccess can't be written by the bridge (not needed for the noindex preview).

## To confirm with the client: see CONFIRM in build.py.
