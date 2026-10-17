# Dynamic Motoring (DMTS): pageonesingapore.com/preview/dmts/

New client (onboarding 12 Oct 2026). Gearbox / auto transmission specialist, Woodlands, Singapore. Old site: https://dmts.com.sg/ (WordPress, 2017).

- `source/`: everything captured from dmts.com.sg on 11 Oct 2026: page HTML, extracted copy (`content.md`), the old cost estimator's 2017 prices (`prices.json`, archive only), the client's own photos (`photos/`, resized to 2000 px) and every media URL (`all-media-urls.txt`).
- `build.py`: generates the five pages (plus a redirect for the retired estimator URL) into `site/` (`python3 build.py`). Copy, FAQ, business details and the image list live at the top of the file.
- `site/`: the files as published to the `pageone` site under `dmts/` (Bluehost Bridge, site key `pageone`). `dmts.css`, `dmts.js`, `favicon.svg` and `img/` are hand-edited.

The pages carry `noindex` (`NOINDEX = True` in `build.py`) so this copy never competes with dmts.com.sg in Google. Turn it off only if this becomes the client's live site.

## Confirmed with the client (11 Oct 2026)
- HQ postcode: 757048.
- WhatsApp 8430 9665 is the preferred contact. Every WhatsApp link is counted for the Page One dashboard
  (`dmts.js`, site key `dmts`, same `CtaClick` tracker as the other managed sites; it stays off on
  pageonesingapore.com, so it only counts once the site is on the client's own domain).
- No cost estimator: DMTS quotes after a pre-repair diagnostic from S$30. `source/prices.json` is kept as
  an archive only, and `cost-estimator/` forwards to the home page.
- Warranty: all repairs come with a standard 6-month warranty unless otherwise stated.
- "15 years of combined experience" still stands.
- Closed on Sundays and public holidays.
- Email: contact@dmts.com.sg (WhatsApp preferred).
- Google: https://share.google/ZXSk6rE3VdUNgZyKS · Facebook: https://www.facebook.com/DYNAMICMOTORINGTRANSMISSIONSPECIALIST/

## Status (12 Oct 2026): client signed up, going live

Follows the standard procedure in `../PLAYBOOK.md` (same as every client from now on):

- One folder, never moved: `public_html/website_b1ec45f5/preview/dmts/` (shown at
  https://pageonesingapore.com/preview/dmts/). On go-live, dmts.com.sg is added in cPanel as an
  **addon domain** whose document root is that folder; the client only changes DNS (A record @ to
  173.254.31.20, CNAME www to dmts.com.sg). Nothing is copied or re-uploaded.
- Controller Client record: slug `dmts`, domain dmts.com.sg, status `activating`, `custom: true`
  (hand-built, so the app never overwrites these files), `design_job: site_done`. The go-live
  checklist on the Clients page tracks DNS, site, https and Search Console.
- Every page has `<meta name="p1-site" content="dmts">` (the go-live check looks for it), canonical
  URLs/Open Graph/structured data name https://dmts.com.sg/, and the pages are indexable.
- Domain files served from this folder once dmts.com.sg points here: `robots.txt`, `sitemap.xml`,
  `llms.txt` and the IndexNow key file `5792dfeef836aebd82a445c206294c95.txt`.
- pageonesingapore.com/robots.txt disallows `/preview/` and `/dmts/`, so the copy under
  pageonesingapore.com is never crawled; dmts.com.sg uses this folder's own robots.txt.
- WhatsApp clicks are counted by `dmts.js` (site key `dmts`) only on dmts.com.sg.
- Onboarding score of the old dmts.com.sg (WordPress, 12 Oct 2026): 55/100, saved in the score history.
- Leftover: the very first upload at pageonesingapore.com/dmts/ only redirects to /preview/dmts/; its
  old copies can be deleted in cPanel File Manager whenever convenient (the bridge can't delete).
