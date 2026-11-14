# Bridge HOLD resolve (14 Nov 2026)
Working files for checking each HOLD site's source against the live server (read-only HTTP compare).
- client-source-shas.txt: site, live base URL, file path, sha256 of the current source file
  (star 6e8184c0c, klar 3f33257f5, cska 533d84627, ben 96fb6c9bd, jacky ffbfafe1b + c22979e57, folder pageone-site/clients/<slug>/site).
- compare-live.sh: fetches each file from live and records SAME / DIFF / 404, plus live sitemap URLs missing from source.
