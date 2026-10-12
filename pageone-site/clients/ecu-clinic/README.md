# The ECU Clinic: pageonesingapore.com/preview/ecu-clinic/

New client (onboarding 12 Oct 2026). ECU and ABS repair for cars, Premier @ Kaki Bukit, Singapore.
Built to the standard in `../PLAYBOOK.md`, with DMTS (`../dmts/`) as the reference. No old website
(ecuclinic.com is a parked page), so there is no before-report.

- `source/`: the client's logo, work photos and flyers from Edwin, and `content.md` (every fact the site
  may use, plus open questions). Flyers are wording reference only (car-maker logos, stock cars).
- `prep.py`: web photos (4:3 webp), header logo lockup and icons from `source/` (`python3 prep.py`).
  The BMW scan photo is cropped above the customer's VIN.
- `build.py`: page copy, FAQ and business details at the top; writes `site/` (`python3 build.py`).
- `share.py`: the 1200x630 share image (og:image) from the client's own photo.
- `site/`: published to the `pageone` site under `preview/ecu-clinic/` (Bluehost Bridge).

## Status (12 Oct 2026): page 1 (home page) draft published
- Live at https://pageonesingapore.com/preview/ecu-clinic/ (noindex, yellow preview strip,
  `MOCKUP = True`). Mobile Lighthouse on the live page: performance 97, accessibility 100, best practices 100
  (SEO is held down only by the intentional noindex). Phone layout 6,200 px tall at 390 px.
- On the server: index.html, ecu.css, ecu.js, site.webmanifest, favicon.ico, icon-48/96/192.png,
  apple-touch-icon.png (all checksum-verified).
- Photos, logo, icon-512 and the share image are served from jsDelivr pinned to commit
  1cf6ce2e33b8e2add12ffe807ee9c89ec98cc8e7 (`IMG_CDN` in build.py), because the bridge only accepts
  files pasted inline. **Before go-live**: upload `site/img/` and `icon-512.png` to the folder, set
  `MOCKUP = False` (and `IMG_CDN` becomes None), confirm the domain, rebuild and republish.
- Controller Client record: slug `ecu-clinic`, status `preview`, `custom: true`, `design_job: mockup_done`.

## Confirmed with Edwin
- Address: Premier @ Kaki Bukit, 8 Kaki Bukit Avenue 4, #06-43, Singapore 415875.
- Mon-Sat 10am-6pm, closed Sundays and public holidays, after-hours appointments can be arranged.
- WhatsApp 9893 1923 (Ching) preferred for enquiries and appointments.
- 6-month warranty. Team has more than a decade of experience.
- Facebook: https://www.facebook.com/TheECUclinicSG. Domain ecuclinic.com (temporary, not confirmed).

## Open
- Confirm the client owns ecuclinic.com (registered 17 Sep 2025 via a GoDaddy reseller, parked).
- WeChat ID, Google Business profile link, reviews.
- Client to confirm wording for "Airbag coding" and "AdBlue, EGR and DPF coding" (see chat notes).
