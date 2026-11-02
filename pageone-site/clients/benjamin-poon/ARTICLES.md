# Adding an article to planwithben.sg (night run, every 2 days, ODD SGT dates)

LIVE site since 24 Oct 2026. Files: /mnt/project-files/benjamin-poon/ (build.py LIVE=True, DOMAIN planwithben.sg).
1. Pick a free intent from /mnt/project-files/seo-method/articles/benjamin-poon-register.md. Chinese-first
   (write the 中文 as the main text, natural Singapore wording: 骨灰位/福位, 神主牌), English version too.
2. CONTACT RULE (Edwin, 25 Oct 2026): Ben (+65 8932 9933) is the ONLY point of contact. Never publish Nirvana phone numbers or its 24-hour line.
   Facts: only from content/locations.py, booklet/TRANSCRIPT.md (Nirvana 2025 booklet), official sites. No prices,
   no award/sales $ amounts, no unverified bus/MRT directions for the temples, Thian Leng name stays "天灵总道堂 (name
   being confirmed)". Things Ben hasn't confirmed go in 'pending' (hidden on the live site) and are not claimed in text.
3. Append a dict to GUIDES in content/guides_c.py (copy an existing one: slug, date YYYY-MM-DD, service, read_min,
   photo (a key from content/photos_booklet.py or None), card, card_text, title, desc, h1, lede, answer, sections,
   faqs, wa, related, pending) and put the slug FIRST in GUIDE_ORDER in build.py (homepage shows the first 3).
4. python3 build.py ; check site/sitemap.xml has the new /guides/<slug>/ with today's lastmod.
5. Publish: in a git worktree of branch site-assets copy site/ to pageone-site/clients/benjamin-poon/site (and
   build.py, content/*.py to src/), commit, push, then Bluehost Bridge sync_from_github
   {site:"pageone", ref:<full sha>, source_path:"pageone-site/clients/benjamin-poon/site", base_path:"preview/benjamin-poon"}.
6. Verify https://planwithben.sg/guides/<slug>/ (200, canonical planwithben.sg, datePublished), add the register
   row, IndexNow, EdgeDailyLog. The Controller finds articles via the sitemap (/guides/ counts since 24 Oct 2026).
