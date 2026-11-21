# Go-live switch: AutoSEO /clients/ card + launches.json, automatic (21 Nov 2026)

Edwin 21 Nov 2026: "make the go-live switch do this step automatically for every future AutoSEO go-live" (golive README step 6, until now done by hand).
Worked example done by hand the same night: Overseas Tyre (overseastyre.my) card in a NEW "Tyre shops" block on autoseo.my /clients/, /ms/clients/, /zh/clients/ + launches.json.
The pure module reproduces those three live pages byte-for-byte from the pre-edit pages (tests/goLiveClientsPure.test.mts, 36 checks, `node --experimental-strip-types`).

## Bridge (app 6ac6d47b4ec84148578914c7), built on HEAD 860e826 (= saved cp 6b01b06a, IndexNow key, not yet Published)
- NEW base44/shared/goLiveClientsPure.ts: text-only helpers (addClientCard, addLaunch, pickIndustry, cleanName, cleanTown, defaultLine/Alt).
- NEW base44/shared/goLiveClients.ts: `clientsCardOp(body)` = op `clients_card` of bridgeGoLive.
  - registryFor(slug, site) -> must be parent autoseo, else skipped. Domain must answer 200 on https (white-label: only live sites are named).
  - industry: body.industry (Controller Client.niche, an /industries/ id or its English name) else from the live home <title>/<h1>, default car-workshops.
  - name: Client.name without Sdn Bhd; line: "<industry singular>, <area>" (EN/BM/中文) unless body.line given.
  - thumbnail: existing assets/clients/<slug>.webp|.jpg kept; else Google PageSpeed desktop final-screenshot (real capture of the live home page,
    optional secret PAGESPEED_API_KEY); else the site's own og:image (flagged "replace"); else skipped (nothing written). New file assets/clients/<slug>.jpg
    (clients.css crops any size to 16:10 with object-fit: cover).
  - 3 pages: read live, addClientCard, writeFile with base sha256 (verified backup; Bridge auto-sitemap bumps lastmod). Page already linking the domain = left alone.
  - launches.json: prepend entry (idempotent on slug/url), only if all 3 pages are fine.
  - Result: { complete, industry, industry_from, name, line, thumbnail{path,source}, pages{en,ms,zh}, launches, urls } (no `ok` key on purpose: Controller bridge() treats ok:false as an error).
- base44/functions/bridgeGoLive/entry.ts: first line inside the handler `if (body.op === 'clients_card') return await clientsCardOp(body);` (no needs_you alert for this op; the flip alert stays).

## Controller (app 6ac7f2548a9c3877449e2772), built on HEAD ad515f3 (= saved cp 6b01b06b)
- functions/goLive/entry.ts flip: after a switched-on AutoSEO flip, `bridge({ op: 'clients_card', slug, site: 'autoseo', domain, name, area, industry: c.niche })`; result (or error) saved in golive_status.clients_card. A failure never changes the switch result.
- functions/clientSites/entry.ts runGoLive: same call after a passed switch-on (Activate flow), saved in golive_status.clients_card.
- No schema change (Client.niche reused for AutoSEO industry override; Page One clients never call it).

## Not in scope / known limits
- Switch OFF does not remove the card (Edwin removes by hand if a client leaves).
- PageSpeed without a key can answer 429; then the share image is used and the result says so.
- Chip for a new industry goes last in the chip row (block goes last too, alt/plain alternation kept).
