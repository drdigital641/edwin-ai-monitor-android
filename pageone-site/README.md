# Page One Singapore website (pageonesingapore.com)

Static site for Page One Singapore, hosted on Bluehost (`public_html/website_b1ec45f5`) and published through the Bluehost Bridge (Base44 app `6ac6d47b4ec84148578914c7`, site key `pageone`).

- `site/` — the files as published (HTML, CSS, JS, icons, images).
- `builder/build.py` — generates every page from one template: `python3 builder/build.py site`. Homepage and sample-report bodies live in `builder/home_body.html` and `builder/report_body.html`.
- `builder/mkedits.py` — makes minimal edit lists (old_text/new_text) between the last commit and the working copy, for uploading through the bridge's `edit_file`.
- `htaccess.txt` — speed and HTTPS settings to paste into `.htaccess` in cPanel (the bridge does not write `.htaccess`).

Articles are not in this folder. They are written by the Page One Singapore Controller (Base44 app `6ac7f2548a9c3877449e2772`) and published hourly by `publishPageOneArticles` in the bridge, which also owns `sitemap.xml`, `sitemap.txt`, `llms.txt` and `/articles/` on the server. Do not upload those four from here.
