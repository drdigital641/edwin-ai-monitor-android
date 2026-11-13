# Google review footer in the source templates (13 Nov 2026 SGT)

Template-only change. Nothing was published, synced or deployed. Each fix copies the markup and styles that are live on that site, byte for byte, so a rebuild keeps the button instead of dropping it.

| Site | Source file(s) on this branch | Normally built from | Output checked |
|---|---|---|---|
| Carzy World (carzyworld.com.my) | autoseo-clients/carzy-world/templates/footer.html, src/build.py, src/check.py, strings/en,ms,zh.json, data/business.json | claude/project-thread-49q3bf | `--live` build: 42/42 pages gain only the review block (EN "Leave us a Google review", BM "Tinggalkan ulasan Google kami", ZH "给我们 Google 评价", /review.html?business=carzyworld). Preview build (autoseo.my/preview) is byte-identical, because /review.html only exists on the live domain. check.py allows the live-only /review.html link. |
| SG Commercial Fitout | pageone-site/clients/rc-design-build/build.py (footer()) | site-assets | 68/68 pages gain only the review block; built /about/ is byte-identical to the live page. |
| MyKar (mykar.my) | client-builds/2026-11-14/dongfeng-jb-source/build.py (shared footer, EN/BM/ZH labels) | newest client-builds/<date>/dongfeng-jb-source/build.py (14 Nov: night-2026-11-14-even-w2) | 89/89 pages gain only the review block; article footer matches live public-ev-charger-etiquette-malaysia (EN/BM/ZH). |
| SG Garage standalone articles | sites/sggarage/articles-extra/footer.html (new shared footer) + every build_*.py reads it | "Latest builder" in /mnt/project-files/sggarage/DAILY-ARTICLE.md | all 5 builders: only the review block added; build_engine_knock.py output is byte-identical to live /articles/car-engine-knocking-noise-singapore.html. |

Markup used everywhere (label and business key per site):

```html
<style>
/* Google review footer button (2026-11-13) */
.p1-foot-review{margin:16px 0 0}
...
</style>
<p class="p1-foot-review"><a href="/review.html?business=KEY" target="_blank" rel="noopener">Leave us a Google review</a></p>
```

The review helper page itself stays noindex and out of every sitemap, llms.txt and IndexNow list.

Next runs: build from this branch's copy of the file (or merge this commit into the branch named above) so the button stays.
