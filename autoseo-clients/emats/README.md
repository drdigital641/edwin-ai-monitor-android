# EMATS preview site (AutoSEO.my client)

EMATS TECHNOLOGY SALES AND SERVICE (RA0076024-T), Johor Bahru. Component-level repair of car ECU/ECM, ABS modules, instrument clusters, other control modules and marine electronics, mainly for workshops (send-in service).

- Preview: https://autoseo.my/preview/emats/ (+ ms/, zh/). Upload the contents of `site/` to `public_html/autoseo.my/preview/emats/`. No .htaccess is shipped; autoseo.my/preview/.htaccess sends the noindex header, and every page also has a noindex meta tag.
- Planned domain: https://ecumats.my/ (sitemap.xml and llms.txt in site/ are already written for it).

## Build

    python3 autoseo-clients/emats/src/build.py

The build writes fully rendered HTML into `site/` and runs `src/check.py` (one H1 per page, every shared part on every page, noindex, hreflang, links, images, schema, blocklist of white-label words and claims we cannot make, owner name only once on About, no English left on BM/中文 pages). A failed check stops the build.

## Where things live

- `config.json`: business facts and **the one WhatsApp switch: `whatsapp_number`** (digits with country code, e.g. 60123456789). Empty = every button says "WhatsApp number coming soon" and points to the Contact page; filled = every button, the sticky mobile bar and schema telephone use it.
- `strings/en.json`, `ms.json`, `zh.json`: every visible word, including the WhatsApp prefills (`prefills.general`, `prefills.service`, `prefills.workshop`).
- `templates/`: shared head, header, footer, WhatsApp button, sticky bar, service card, reel facade, FAQ, CTA, breadcrumb, photo.
- `data/site.json`: page order, photo-to-service mapping, the 12 Facebook reels.
- `photos/`: the 8 real bench photos from the owner's Facebook. `emats-06-ecu-in-metal-case.webp` shows an ECU in its metal case (renamed 11 Nov from emats-06-instrument-cluster-repair).

## Move day

config.json: `site_url` = `https://ecumats.my/`, `base_path` = `/`, `preview` = false, rebuild, add a robots.txt.
