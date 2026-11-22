# CLAUDE.md

Standing rules for Claude sessions working in this repository and on Page One Singapore / AutoSEO.my sites.

## Fixed rules

### Rule 6: write once in English (Edwin, 22 Nov 2026, 10:55am SGT, PERMANENT)

Replaces the 18 Nov 2026 "AutoSEO in three languages" rule and the 22 Nov 10:49am "English only" wording. Both are SUPERSEDED and must not be followed.

All content on every site is written ONCE, in English only. Never write Chinese or Malay content from scratch and never write content 3 times. For sites serving Malaysian clients with a Malaysian address, the English content is then translated into real, indexable /zh/ and /ms/ pages using a cheap method (Grok, or a low-cost translation step), never a full rewrite on the paid writer. Those pages get hreflang, sitemap entries and a switch that links to the same page in each language. Singapore and other sites stay English only. The switch must never lead to a missing page.

How to apply:
- Shared template: `autoseo_i18n.build_langs(malaysian_address)` gives EN + BM + 中文 for Malaysian-address sites and English only otherwise; golive `languages` defaults to `["en"]` and Malaysian-address sites set `["en","ms","zh"]`.
- On Malaysian-address sites, ms/zh strings and area-page `translations` come only from the cheap translation step of the finished English, and `check_twins` must pass.
- Do not change live site files just to apply this rule; the live switcher work is handled separately.
