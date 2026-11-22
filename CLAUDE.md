# CLAUDE.md

Standing rules for Claude sessions working in this repository and on Page One Singapore / AutoSEO.my sites.

## Fixed rules

### ENGLISH ONLY (Edwin, 22 Nov 2026, 10:49am SGT, PERMANENT)

Replaces fixed rule 6 "AutoSEO in three languages" (18 Nov 2026), which is SUPERSEDED and must not be followed.

Every page on every site (articles, service pages, area pages, hubs and any new page) is written and built in ENGLISH ONLY. Chinese and Malay must come only from the site translator. Never write, generate or AI-translate separate /zh/ or /ms/ pages or strings, and no plan, brief or job may produce pages in 3 languages. This has been causing large usage spikes. The language switcher must still work on every page and never lead to a missing page.

How to apply:
- New builds render English pages only (shared template `autoseo_i18n.BUILD_LANGS`, golive `languages: ["en"]`); no `strings_ms` / `strings_zh` files, no ms/zh hreflang, English URLs only in sitemap.xml.
- Do not delete existing /ms/ or /zh/ files on live sites as part of this rule; the switcher on live sites is handled separately.
- Any older doc, brief or check that asks for /ms/ or /zh/ pages, "EN/BM/中文" copy or "all three languages" is superseded by this rule.
