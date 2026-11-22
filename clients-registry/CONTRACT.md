# Clients registry + /clients pages contract (22 Nov 2026, thread "Build master clients page and registry")

Source of truth: registry.json (this folder; agency / visibility / industry / card fields) + Controller Client.status (live | preview -> in_build | dormant).
Refresh status: update controller-snapshot.json from the Controller, run `python3 sync_controller.py`. Numbers: stats.py.

## Rules (Edwin 22 Nov 2026)
- agency: pageone | autoseo. visibility: public (named card on pageonesingapore.com/clients) | white-label (counts only on Page One, never a name, host, url, logo, screenshot, tagline) | own (Page One, SG Garage, SG Car Workshop, AutoSEO.my: never counted).
- AutoSEO clients are white-label on Page One, incl. K Tech, Klar Details, Battery Rescue, MyKar (Controller brand says Page One for these four; registry wins for agency/visibility).
- Hon Win Motor is NOT a client-website card (mini-site on sgcarworkshop.sg, not its own domain). Controller rows whose domain contains "/" are mini-sites: excluded.
- Controller duplicate_of rows skipped. billing_only rows: status not trusted when the registry has status_override (SofaCare). Rows missing in the Controller = unknown, left out (911 Garage).
- In build = Controller preview/activating only; dormant never counted.
- Last 30 days = white-label live rows with live_date > today-30 (SGT). Last updated = build date SGT.

## Page One page markers (both the Python builder and the Bridge op must produce byte-identical output for the same numbers)
1. Stats block, regenerated whole:
```
<!-- wl-stats:start -->...<!-- wl-stats:end -->
```
Exact inner HTML = fixtures/wl-stats.html with the numbers (render function: build_pageone.py `wl_stats_html(stats)`; golden fixture made from stats.py output of 22 Nov).
2. Count spans anywhere on the page: `<span data-reg="po_live">24</span>`, `data-reg="po_industries"`, `data-reg="po_build"`, `data-reg="wl_live"`, `data-reg="wl_build"`: op replaces the inner number only.
3. JSON-LD `"dateModified": "YYYY-MM-DD"` -> today SGT. `<meta property="og:description"` / `twitter:description` / `<meta name="description"` contain the counts as written by `meta_text(stats)` and are regenerated whole.
4. Named cards (pageone + public + live only) inside `<div class="industry-block..." id="<industry_id>">`; industry ids are those already on the live page.
