# Bluehost Bridge: Grok Bot runner API (grokbot-runner key, 18 Nov 2026)

Every call: `POST https://blue-bridge-pilot.base44.app/functions/<function>`
Headers: `Content-Type: application/json` and `X-Bridge-Key: <BRIDGE_RUNNER_KEY>` (never log or print the key).
Answer: JSON with `ok: true|false` (+ `error`). Every call, allowed or refused, is logged to BridgeLog with label `grokbot-runner`.

Sites (`site`): sggarage, cleanic, alicia, danny, sofacare, pageone, ktech, benzworld, lilian, carzy, hybridworld, autoseo,
ecumats, apcar, jayven, urbaneco, snapsg. Client previews/sites hosted under Page One use `site: "pageone"` and
`path: "preview/<folder>/..."`. Cleanic and ContiExpert (`pageone`, `preview/contiexpert/`) are articles only.
NOT allowed (403): deletes, .htaccess, credentials, DB, keys, restore, sync, edit, drops, needs-you, Base44 Publish.

| Action | Function | JSON body |
|---|---|---|
| list live files | `bridgeListLive` | `{"site":"pageone","path":"preview/aivs/articles","depth":1}` |
| read live file | `bridgeReadLive` | `{"site":"sggarage","path":"articles/index.html"}` -> `content`, `sha256` |
| write_file (new) | `bridgeWrite` | `{"site":"sggarage","path":"articles/<slug>/index.html","content":"<html>..."}` |
| write_file (replace) | `bridgeWrite` | `{"site":"sggarage","path":"articles/index.html","content":"...","expected_sha256":"<sha256 from read>"}` |
| write_file (binary) | `bridgeWrite` | `{"site":"...","path":"images/x.jpg","content_base64":"..."}` |
| write_files | `bridgeWriteMany` | `{"site":"pageone","base_path":"preview/aivs","files":[{"path":"articles/<slug>/index.html","content":"..."},{"path":"articles/index.html","content":"...","expected_sha256":"<sha>"}],"dry_run":false}` (max 150 files / 6 MB) |
| sitemap.xml + llms.txt rebuild (+ IndexNow) | `bridgeRunnerSitemap` | `{"site":"pageone","paths":["preview/aivs/articles/<slug>/index.html"],"dry_run":false}` (1-20 .html pages already live) |
| IndexNow submit | `bridgeRunnerIndexNow` | `{"site":"sggarage","urls":["https://sggarage.com/articles/<slug>/"]}` (own domain only; key never returned) |
| Copy fix issues (read) | `bridgeRunnerController` | `{"op":"copy_fix"}` or `{"op":"copy_fix","site":"<controller site key>"}` |
| Tap counts (read) | `bridgeRunnerController` | `{"op":"taps"}` or `{"op":"taps","site":"sggarage"}` |
| article_last_* update | `bridgeRunnerController` | `{"op":"article_last","slug":"<client slug>","date":"2026-11-18","title":"...","url":"https://<client domain>/articles/<slug>/"}` |
| Article image | `generateArticleImage` | `{"site":"sggarage","slug":"<article-slug>","prompt":"<20-400 chars: the scene>","alt":"Illustrative ... (optional)","folder":"images/articles (optional)"}` |

Notes
- write_file / write_files: replacing any live file needs `expected_sha256` from the read; missing = 409, stale = 409. A verified
  backup is taken before every replace (the result carries `backupId`). A new article page must already have its own hero,
  og:image and twitter:image files (image gate) and pages with WhatsApp/call links need the tap tracker (CTA gate).
- write_file / write_files already run the sitemap.xml + llms.txt + IndexNow step themselves (`autoSitemap` in the result);
  use bridgeRunnerSitemap / bridgeRunnerIndexNow for resends (IndexNow 429 = try later).
- generateArticleImage returns `hero_url`, `card_url`, `og_image_url`, `alt` and `files` (paths, sizes). Files:
  `<folder>/<slug>.jpg` 1536x1024, `<slug>-card.jpg` 768x512, `<slug>-og.jpg` 1200x630. Default folder images/articles
  (alicia assets/articles, cleanic wp-content/uploads/YYYY/MM; pageone previews send folder "preview/<folder>/images/articles").
  Same slug again = cached result, no new image. Limit 3 per site, 40 in total per SGT day. Prompt must not claim
  clients/testimonials/logos/prices; alt must start with "Illustrative".
- Controller ops use the Controller's site keys (e.g. maison-interior-design) and client slugs.
