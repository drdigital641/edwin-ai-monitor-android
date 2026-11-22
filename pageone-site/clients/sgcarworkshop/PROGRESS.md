# SG Car Workshop screening progress

Updated 2026-11-02. Live Basic listings: 18. Passed but hidden (need estate/geo): 11. Waiting to screen: 96.

| Date | Place Details calls | Text searches (free) | Live total | Hidden by reason |
|---|---|---|---|---|
| 2026-11-02 | 25 | 1 | 18 | primaryType is not car repair: 5; Google profile has no SG mobile (landline only or no phone): 19 |

## 23 Nov 2026 SGT: 15 thin pages made indexable (Edwin 7:17am)
- settings.json index_exceptions: services/car-parts/, areas/mobile/ and 13 estate pages (below the 5-listing minimum, minimum stays 5). build.py now honours index_exceptions on service and region pages too (estates already did); check.py region check honours it.
- Kept noindex: areas/bukit-timah-road-newton/ (no workshops in its own list, only one paid Featured card).
- Live: robots line changed in place on the 15 pages through the Bridge (live edit, WM header/hub edits untouched), live sitemap.xml +15 URLs lastmod 2026-11-23. No full rebuild/publish.
