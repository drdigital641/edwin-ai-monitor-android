# Evan Lee Homes (evanlee)

Client: Evan Lee 李敏彦, Associate, ERA Realty Network Pte Ltd (L3002382K), CEA R074252A.
Live preview: https://pageonesingapore.com/preview/evanlee/ (Bluehost folder public_html/website_b1ec45f5/preview/evanlee, bridge site "pageone").

- `build.py` writes every page into `site/` (DOMAIN, LIVE flags at the top). `share.py` makes the portrait, icons and share image.
- Run: `python3 build.py && python3 share.py`, then upload changed files through the Bluehost Bridge.
- `manual-upload/` holds the two files the bridge cannot write: `.htaccess` (saved as htaccess.txt) and `img/share/home.jpg`.
- Portrait is cut from the business card photo; drop a real headshot in `source/portrait.jpg` and rerun share.py.
- Go-live: addon domain in cPanel with document root public_html/website_b1ec45f5/preview/evanlee, client DNS A @ -> 173.254.31.20 and CNAME www -> domain, AutoSSL, then LIVE=True in build.py, rebuild and re-upload.

## Update 13 Oct 2026 (real photo, awards, division)
- Headshot now taken from Evan's ERA profile (source/portrait.jpg). Awards and division from his Instagram/ERA screenshots.
- Uploaded to preview: index, about, contact, evan.css (v=2), img/evan-lee.webp.
- Other pages differ from the live preview only in schema (Facebook link, awards) and the css version; they will be re-uploaded at go-live.
- manual-upload/img/share/home.jpg has the new portrait; upload via cPanel.

## Photos (13 Oct 2026)
Crops of Edwin's screenshots live in source/social/ and are written to site/img/ as webp:
award-top100, award-top5, award-ceremony (home hero card, award gallery on home and About),
post-welcome, post-tour, post-launches ("From Evan's feed" on home; welcome post also on About).
build.py: AWARD_IMGS, POSTS, award_gallery(), feed_section(). Styles at the end of site/evan.css.
manual-upload/img/share/home.jpg was regenerated with the new portrait; upload it in cPanel.
