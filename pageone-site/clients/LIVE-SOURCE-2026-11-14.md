# Client site sources = live copies (14 Nov 2026, Bridge HOLD resolve)

Edwin, 14 Nov 2026 9:24am SGT: bring the source for Star, Klar, CSKA, Jacky and Ben up to match live, using the
read-only live snapshot. On this branch (claude/project-thread-xc39oz) each `site/` folder below is a byte-exact copy
of the live site as served on 14 Nov 2026 01:33 UTC (workflow "HOLD live snapshot (read-only)", hold-resolve/live/):

| Site | Folder | Live docroot |
|---|---|---|
| Star Performance | star-performance/site | preview/star-performance (starperformancemotor.com) |
| Klar Details | klar-details/site | preview/klar-details (klardetails.com.sg) |
| CSKA | cska-auto/site | preview/cska-auto (cskatrading.com) |
| Jacky Gearbox | dmts/site | preview/dmts (jackygearbox.com) |
| Benjamin Poon | benjamin-poon/site | preview/benjamin-poon (planwithben.sg) |

Not included (cannot be read over HTTP, never synced): .htaccess. Files only in the old source and not on live
(e.g. Jacky cost-estimator/price-estimator, which 301 on live) are left out so a sync can never add them.

WARNING: the build.py files on other branches and in /mnt/project-files/<site>/ are BEHIND live (they predate the
night articles, the review footer and server edits). Never build from them and sync over live. New work starts from
these site/ folders. Every HOLD flag stays ON until Edwin lifts it.
