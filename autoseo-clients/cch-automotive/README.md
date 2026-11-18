# CCH Automotive (AutoSEO.my client preview)

Preview: https://autoseo.my/preview/cch-automotive/ (noindex, nofollow). Photos are already on the server in images/ (placed from the Bridge drop, not in this repo).

- src/facts.json: the only facts allowed on the site. src/strings_en.py: all visible copy (add strings_ms.py later for Bahasa Malaysia).
- src/build.py builds every page from one set of templates into dist/. src/check.py is the pre-upload gate (banned words, numbers, noindex, one H1, CTA data-cta, tracker).
- Upload dist/ only through the Bluehost Bridge (sync_from_github with a commit SHA, base_path preview/cch-automotive).
