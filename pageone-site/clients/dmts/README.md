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

## Status

Built once into https://pageonesingapore.com/preview/dmts/ and never moved. On activation, point
dmts.com.sg's document root (addon domain / DNS) at `public_html/preview/dmts/`; nothing is re-uploaded.

- All internal links are relative, so the same files work at both addresses.
- Canonical URLs, Open Graph and structured data always name https://dmts.com.sg/.
- pageonesingapore.com/robots.txt has `Disallow: /preview/` (and `/dmts/`) in every group, so the
  preview copy is not crawled. The folder's own `robots.txt` and `sitemap.xml` are what dmts.com.sg
  serves once it points here.
- The WhatsApp tracker in `dmts.js` skips pageonesingapore.com, so it only counts on dmts.com.sg.
- The first upload at /dmts/ now redirects to /preview/dmts/. Its old images/CSS/JS are still on the
  server (the bridge cannot delete files).
- Social share previews of the preview link show no image until dmts.com.sg is live (og:image points
  at the client domain).
