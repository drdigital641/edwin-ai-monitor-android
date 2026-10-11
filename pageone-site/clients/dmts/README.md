# Dynamic Motoring (DMTS): pageonesingapore.com/dmts/

New client (onboarding 12 Oct 2026). Gearbox / auto transmission specialist, Woodlands, Singapore. Old site: https://dmts.com.sg/ (WordPress, 2017).

- `source/`: everything captured from dmts.com.sg on 11 Oct 2026: page HTML, extracted copy (`content.md`), cost estimator prices (`prices.json`), the client's own photos (`photos/`, resized to 2000 px) and every media URL (`all-media-urls.txt`).
- `build.py`: generates the six pages into `site/` (`python3 build.py`). Copy, FAQ, business details and the image list live at the top of the file.
- `site/`: the files as published to the `pageone` site under `dmts/` (Bluehost Bridge, site key `pageone`). `dmts.css`, `dmts.js`, `favicon.svg` and `img/` are hand-edited.

The pages carry `noindex` (`NOINDEX = True` in `build.py`) so this copy never competes with dmts.com.sg in Google. Turn it off only if this becomes the client's live site.

## To confirm with the client
- HQ postcode: text says S757048, the old Google Maps embed says 757881.
- Is 8430 9665 on WhatsApp? The site's WhatsApp buttons use it.
- Cost estimator prices are from 2017. Still current?
- Warranty terms (one 2017 testimonial mentions 6 months).
- "15 years of combined experience" was written in 2017.
- Sunday / public holiday hours (old site didn't say).
- Email: the old site used both sales@ and contact@dmts.com.sg. The new site uses sales@.
- Facebook / Google Business Profile URLs (none were linked on the old site).

## Status

Published 11 Oct 2026 to https://pageonesingapore.com/dmts/ as a **preview** (noindex). It goes live
only when the client is activated through the Page One controller's create-client / Activate flow,
which moves it to the client's own domain. That flow's previews use `/preview/<slug>/`, so this folder
may be moved there.
