# Wrapstar Autostyle (wrapstar) — preview build

New client 17 Oct 2026 (Edwin). Car wrap studio, sister business of Star Performance Motor, same unit: 9 Yishun Industrial Street 1 #01-82, North Spring Bizhub S768163. WhatsApp +65 9754 1833. Sole proprietorship UEN 53513245W, registered 3 Nov 2025.
Preview: https://pageonesingapore.com/preview/wrapstar/ (bridge site "pageone", folder preview/wrapstar). Hidden from search by /preview/ Disallow in pageonesingapore.com robots.txt; htaccess.txt adds an X-Robots-Tag header for the preview host when pasted via cPanel. No meta noindex in pages (rule 4.3).

- `build.py [outdir]` writes 19 pages + 404, sitemap, robots, llms.txt, manifest. Facts, sources and CONFIRM list at the top. `check.py <dir>` validates.
- Pages: home (photo hero slideshow, gliding colour catalogue, 5 service tiles, past-works grid, review + sister-business card, 4 FAQs), /colours/ (10 colours "seen on our past jobs"), /past-works/ (gallery grouped by colour, filter chips, lightbox), /services/ + 5 (colour-change-wrap, colour-ppf, paint-protection-film, window-film, dechrome), /prices/ (posted offers with dates), /articles/ + 5, /about/, /contact/ (form opens WhatsApp), /privacy/.
- Theme: black + logo yellow #ffc205, Archivo italic 900 display (Google Fonts), slanted buttons. ws.css / ws.js (glide carousel copied from Star Performance: glides continuously, pauses only when held or swiped sideways).
- Photos: their own Facebook photos (Nov 2025 onwards; earlier photos on that page are from Finest Detailing Express and are not used). jsDelivr, repo site-assets branch commit da2c02e, folder site-assets/wrapstar/. dims.json holds sizes.
- Scraping: container cannot reach FB/IG. Bluehost Bridge Base44 sandbox (app 6ac6d47b4ec84148578914c7), Playwright at /tmp/pw (needed `npx playwright install-deps chromium`). FB photo grid URLs: drop `&ctp=s206x206` to get full size. IG blocks the sandbox IP (login wall). Big outputs from run_command land in a tool-results file, which is the way to move binaries to the container.
- Not claimed: film brands, wrap/PPF warranty, hours, Google rating, which jobs were wrap vs PPF (except the Model 3 satin black colour PPF).
- A 3D car configurator was not built; a colour catalogue + past works was chosen instead. Could be added later.

## Go-live
LIVE since 18 Oct 2026 (01:11 UTC, Controller switch) on https://wrapstarautostyle.com (www and http 301 to it). build.py now has LIVE=True; a LIVE build matched all 27 live files byte for byte (18 Oct 2026). Always rebuild with LIVE=True before uploading.

Original checklist: Domain (CONFIRM), addon domain -> preview/wrapstar folder, LIVE=True + DOMAIN in build.py, rebuild, re-upload, htaccess.txt -> .htaccess via cPanel, Search Console + Bing, IndexNow, EDGE daily articles + backlinks tracker, GBP website link, link from starperformancemotor.com.
