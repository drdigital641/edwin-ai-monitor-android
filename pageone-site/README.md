# Page One Singapore website (pageonesingapore.com)

Static site for Page One Singapore, hosted on Bluehost (`public_html/website_b1ec45f5`) and published through the Bluehost Bridge (Base44 app `6ac6d47b4ec84148578914c7`, site key `pageone`).

- `site/` — the files as published (HTML, CSS, JS, icons, images).
- `builder/build.py` — generates every page from one template: `python3 builder/build.py site`. Homepage and sample-report bodies live in `builder/home_body.html` and `builder/report_body.html`.
- `builder/mkedits.py` — makes minimal edit lists (old_text/new_text) between the last commit and the working copy, for uploading through the bridge's `edit_file`.
- `htaccess.txt` — speed and HTTPS settings to paste into `.htaccess` in cPanel (the bridge does not write `.htaccess`).

- `site/llms-full.txt` — built by `build.py` from the pages themselves (every indexable page's title, description and FAQ answers). Published as a pinned file; the short `llms.txt` stays with the Bridge.
- `site/robots.txt` — allows Google, Bing, ChatGPT (OAI-SearchBot, ChatGPT-User, GPTBot), Perplexity, Claude (ClaudeBot, Claude-SearchBot, Claude-User), Google-Extended, Applebot and others. Publish it as a pinned file too.
- `bridge/lastmod.json` and `bridge/org-graph.json` — written by `build.py`; `bridge/update_pins.mjs` copies them into the Bridge (per-page sitemap dates and the business JSON-LD on article pages) once the Bridge has `PAGE_LASTMOD` and the `ORG_GRAPH` markers.

Articles are not in this folder. They are written by the Page One Singapore Controller (Base44 app `6ac7f2548a9c3877449e2772`) and published hourly by `publishPageOneArticles` in the bridge, which also owns `sitemap.xml`, `sitemap.txt`, `llms.txt` and `/articles/` on the server. Do not upload those four from here.
