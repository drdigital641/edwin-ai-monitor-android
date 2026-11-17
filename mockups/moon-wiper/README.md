# MOON wiper blades SG preview (Page One, Edwin 17 Nov 2026)
Live: https://pageonesingapore.com/preview/moon-wiper/ (noindex via the parent /preview/ X-Robots-Tag header).
- Facts: data.json only. Template + pages: build.py. CSS: static/site.css. Tracker: static/p1-cta.js (slug moon-wiper).
- Build: `python3 build.py` -> site/; deploy: commit, then Bridge sync_from_github site=pageone source_path=mockups/moon-wiper/site base_path=preview/moon-wiper.
- Photos are NOT in the repo: they were published from Bridge drop 6afc030c2c5b372926dcb5a1 to preview/moon-wiper/img/.
- WhatsApp: set "whatsapp" in data.json (digits) and rebuild; header, hero, dock, footer and shop-block slots appear together.
