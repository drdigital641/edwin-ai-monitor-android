# Runner article records + image gate hero + runnerFeed built-in slugs (22 Nov 2026)

Edwin batch brief 22 Nov 2026 (Priority 4, urgent follow-up 7:41am SGT). Thread "Fix runner and checker faults".

| App | Change | Checkpoint | Live |
|---|---|---|---|
| Bluehost Bridge 6ac6d47b | imageGate.ts hero detection (Plan with Ben block); new bridgeRunnerArticle + runnerArticle.ts; signedAppCall; runner action runner_article; OpenAPI 1.6.0 | 6b0230640dd2763a6cfe511f (git a482d9c) | new function live on save; image gate (used by bridgeWrite) needs Publish |
| SofaCare SG 6a9c4351 | new runnerArticleIngest + shared/runnerArticleChecks.ts (Bridge-signed only) | 6b023066d26b8d5378423adc (git 67ac80a) | live on save |
| Page One Controller 6ac7f254 | runnerFeed article_last: built-in sites (alicia, danny, sggarage, cleanic, sofacare, pageone) answer ok as a no-op; lilian -> lilian-properties | 6b0230658e64abbb7c83a973 (git 85cd10d) | Publish (also carries earlier unpublished Controller saves) |

SPO review: SPO-REVIEW.md. Must-fix F1 (strict media URL after upload) and F2 (no raw HTML / javascript: / data:)
and should-fix F3 (header fallback), F4 (exact slug/title lookups), F5 (3 runner records per 24 h) were applied
before saving. Tests: Bridge 107 pass, 1 fail (frozenHeaders, fails the same on the base); gate tests 8/8.
