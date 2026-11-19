# Rasa Sayang Automotive (AutoSEO.my client preview)

Preview: https://autoseo.my/preview/rasa-sayang/ (BM /ms/, 中文 /zh/), noindex, nofollow. No live domain yet; do not touch DNS.

- src/facts.json: the only facts allowed on the site (trimmed from the Bridge drop facts.json, 19 Nov 2026).
- src/strings_en.py, strings_ms.py, strings_zh.py: all visible copy, same keys.
- Switcher (EN / BM / 中文), hreflang + x-default, og:locale, sitemap language entries: shared ../../autoseo-template/autoseo_i18n.py.
- src/build.py builds all 33 pages into dist/. src/check.py is the pre-upload gate (banned words and claims, numbers, noindex, one H1, data-cta on every CTA, tracker, JSON-LD, hreflang).
- Photos are on the server only (preview/rasa-sayang/images/, placed from Bridge drops 6afef206... and 6afef249...), not in this repo.
- Upload dist/ only through the Bluehost Bridge: sync_from_github with a commit SHA, site autoseo, base_path preview/rasa-sayang.
- Tracker p1-cta.js site key rasa-sayang: on /preview/ it sends taps only with ?p1test=1 (stored as test taps).
