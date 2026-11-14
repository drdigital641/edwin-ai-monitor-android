# Shared Google review button (15 Nov 2026)

One block for every site, so one change updates all of them.

- `p1_blocks.py`: `review_button(key, lang, label, data_ref, nofollow, with_css, href)` for Python builders. Labels EN / BM / ZH built in.
- `review-button.html`: the same block as a file, for Apache SSI sites (`<!--#include virtual="/inc/review-button.html" -->`, KEY replaced per site).
- Default output is byte-for-byte the button that is live today (checked against the SG Garage article footer), so moving a builder onto this helper changes no live page.
- Safety: the key must be letters, digits, - or _; a custom href must be a Google review link or /review.html (no javascript:).
- The review helper page itself stays noindex and out of sitemaps, llms.txt and IndexNow (the Bridge auto-sitemap step skips review pages).

Open point for Edwin: the review-helper rule (8 Nov) says links to it should carry rel="nofollow". The live button does not. `nofollow=True` adds it; turning it on changes every footer once.

Tests: `python3 p1_blocks.py` (6 checks) plus a byte compare with the live footer.
Not rolled out anywhere.
