# pageonesingapore.com

Marketing site for **Page One Singapore**: Google + AI visibility for Singapore businesses.
Plain static HTML/CSS/JS with no build step.

## Files
- `index.html`: home, two ways to start, how it works, pricing + calculator, free check form, FAQ (with ProfessionalService + FAQPage schema)
- `report.html`: sample SEO Run report (fictional example business)
- `main.js`: pricing calculator, free-check form → prefilled WhatsApp message, floating WhatsApp button
- `robots.txt`, `sitemap.xml`, `llms.txt`, `favicon.svg`

## Before going live
1. Set `WHATSAPP_NUMBER` in `main.js` to the business WhatsApp number (e.g. `6591234567`).
2. Upload all files (including the hidden `.htaccess`) into `public_html` on Bluehost (cPanel → File Manager), replacing any placeholder `index.html`/`index.php`.
3. Add the site to Google Search Console and Bing Webmaster Tools and submit `sitemap.xml`.

## Local preview
    python3 -m http.server 8000
