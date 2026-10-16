# Cleeneo (cleeneo.co): pageonesingapore.com/preview/cleeneo/

New client (confirmed 13 Oct 2026). Singapore brand of drug-free, latex-free silk nasal strips, sold online
with free delivery across Singapore. Old site: https://cleeneo.co/ (a Base44 shop with cart and checkout,
owned by the client, not in Edwin's Base44 account).

- `source/content.md`: everything captured from cleeneo.co on 13 Oct 2026 (copy, prices, shipping and
  returns, reviews, old URLs). `source/photos/`: the client's logo and three product images (uploaded by
  Edwin; this session's network policy blocks cleeneo.co and media.base44.com).
- `build.py`: generates the 11 pages, 404, robots.txt, sitemap.xml, llms.txt, manifest and IndexNow key
  into `site/` (`python3 build.py`; needs Node with playwright for the images, `NODE_PATH=$(npm root -g)`).
  Copy, kits, FAQ and contact details live at the top of the file.
- `share.mjs`: draws the 1200x630 share image per page and the icons in headless Chromium from the photos.
- `site/`: the files as published to the `pageone` site under `preview/cleeneo/`. `cleeneo.css`, `cleeneo.js`
  and `.htaccess` are hand-edited.

## Decisions
- Orders go through WhatsApp: every kit has an "Order on WhatsApp" button with the kit pre-filled, and the
  kits page has an order form (kit, quantity, name, address, postal code) that opens WhatsApp with the order
  typed out. Taps are counted by `cleeneo.js` (site key `cleeneo`, same `CtaClick` tracker as the other
  sites; off on pageonesingapore.com). WhatsApp only, no tap-to-call (Edwin's preference).
- Photos in `site/img/` are 900/480 px webp copies of `source/photos/`; `mark.webp` is the "C" cut from
  the logo. The nose diagram on the home and how-to pages is still a drawn SVG.
- Health claims kept to the mechanism. Not used: "opens the passage by up to 38%" (no source). Every page
  footer carries a see-a-doctor note about loud snoring and sleep apnoea.
- Reviews and the 4.9/5 from 48 rating are copied from the old site.

## Go-live
Standard procedure in `../PLAYBOOK.md`: addon domain cleeneo.co with document root
`public_html/website_b1ec45f5/preview/cleeneo`, client sets A @ -> 173.254.31.20 and CNAME www -> cleeneo.co.
`.htaccess` cannot be written by the bridge; upload `site/.htaccess` by hand in cPanel File Manager.
After go-live set `LIVE = True` in build.py, rebuild and republish.
