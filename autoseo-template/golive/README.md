# One-switch go-live template (Edwin, 20 Nov 2026, 6:59pm SGT; addendum 7:03pm)

Going live = addon domain + SSL + flip ONE switch. No per-page tag rewrites.

## Config (site.json, later the Controller site record)
`slug`, `preview_url`, `live_domain` (EMPTY at preview build time), `live` (false/true), `languages`, `og_image` (JPG 1200x630, default images/og.jpg), `og_version`.
Examples: hx-auto.site.json, cch-automotive.site.json, rasa-sayang.site.json (live 20 Nov 9:52pm), site.example.json. `live` is forced false while `live_domain` is empty.

## ONE SETTING: go_live_domain (Edwin 23 Nov 2026, after the MCS go-live hand edit, PERMANENT)
Builders must never hardcode `P = '/preview/<slug>'` or `BASE = 'https://autoseo.my' + P` again. Put one field in the site's
site.json (later the SITE-NOTES / Controller record): `"go_live_domain": ""` = preview mode, `"go_live_domain": "client.com.my"` = live
(it sets live_domain + live together). In build.py:
```
sys.path.insert(0, '<path to>/autoseo-template/golive'); import golive
P, BASE = golive.build_base(os.path.join(HERE, 'site.json'))   # preview: '/preview/<slug>', 'https://autoseo.my/preview/<slug>'
                                                               # live:    '',               'https://<domain>'
```
`python3 golive.py base site.json` prints P/BASE. For a tree that is already live on Bluehost (Rule 0: never rebuild over live
edits), `retarget_paths(text, cfg)` is the same swap file by file (read_live -> retarget_paths -> edit/write with expected_sha256);
`golive.py retarget <site.json> <dir> --paths` does it on a local copy. Tests: test_go_live_domain_one_setting, test_retarget_paths_live.
Worked example: mcs-auto-spray-painting.site.json (live 23 Nov 2026; live files switched by edit_file with this exact swap).

## Module: golive.py (tests: test_golive.py, 8 pass)
- `head_tags(cfg,path,lang)`: canonical, hreflang (+x-default), og:url, og:image(+secure_url,type,w,h), twitter:image.
  Canonical/hreflang/JSON-LD/sitemap/robots/llms always use `canonical_base` = live domain once one is set; with no domain they use the preview URL (no domain in any page). og:image/twitter:image use `share_base` = preview URL while live=false, live domain when live=true (must return 200 image/jpeg).
- `sitemap_xml`, `robots_txt`, `llms_header`: generated from cfg.
- `retarget_tree(dist,cfg)`: idempotent rewrite of those tags in an already built tree (used for existing builds; flipping back works too).
- `htaccess(cfg)`: folder .htaccess. noindex only when Host = preview host; live=true adds live www/http -> https apex (same path+query), preview host `/preview/<slug>/(.*)` -> `https://<live>/$1` (host-limited, never on live host); ACME excluded first.
- `parent_block(cfg)` / `parent_htaccess(hosts)`: host-limited block for a parent .htaccess when the folder file cannot be created (Bridge htaccess tool only replaces existing files).
- `domain_status(domain)`: gate = DNS resolves ONLY to 173.254.31.20 and https verifies. Switch On is refused otherwise.
- `go_live_check(cfg)`: http apex/http www/https www single 301; live /, /ms/, /zh/, sitemap.xml 200 and no X-Robots-Tag; preview host 301; every og/twitter image 200 image/jpeg 1200x630; http ACME test file 200.
  The Claude sandbox cannot resolve client domains, so the check must run from the Bridge/Controller side (or via the Bridge htaccess tool test_urls, which is what was used for HX/CCH).

## IndexNow key file (21 Nov 2026, after Overseas Tyre IndexNow 422, PERMANENT)
Every site serves `<key>.txt` (content = the key) in its root. Preview builds: put `indexnow_key` in site.json (Page One: the Client record key) or set env `INDEXNOW_KEY` (AutoSEO standard key), and `golive.py files` writes it. The Bridge Go live switch also places it if the folder has none (folder key, else the Controller client key, else the AutoSEO standard key read from preview/hx-auto/), and its checks include "IndexNow key file at site root (200, key matches)". `golive.py check` has the same check. Never print the key in chat, the repo or alerts.

## Flip runbook (what one run must do)
1. domain_status OK, else refuse and show the status.
2. set live=true, live_domain; retarget_tree on the built site (or rebuild); regenerate sitemap.xml, robots.txt, llms.txt.
3. sync_from_github (base_sha256 map from dry run) to the site; backup is automatic.
4. htaccess: read, write generated rules with test_urls (auto-restore on 5xx).
5. go_live_check, report to Controller + needs_you done/blocked.
6. AutoSEO clients (Edwin 20 Nov 2026 "Yes, auto update", PERMANENT): add the client to autoseo.my /clients/, /ms/clients/, /zh/clients/ (card in its industry block, counts + ItemList +1, screenshot 640x400 at assets/clients/<slug>.webp) and THEN prepend launch_entry() to assets/launches.json (add_launch, edit with base sha). The popup shows the newest entry for 30 days. Rasa Sayang 20 Nov is the worked example.
   AUTOMATIC from 21 Nov 2026 (Edwin): Bridge bridgeGoLive op `clients_card` (shared/goLiveClients.ts) does this step; the Controller calls it after every passed AutoSEO switch-on (goLive flip + clientSites Activate) and saves the result in Client.golive_status.clients_card. Industry = Client.niche (an /industries/ id such as tyre-shops) else from the live home title; thumbnail = PageSpeed desktop capture of the live home page (assets/clients/<slug>.jpg). Manual fallback: clients_card.py (same text transform) + Bridge edit_file. Overseas Tyre 21 Nov = worked example (new Tyre shops block). Review package: hold-resolve/golive-clients-card/.

Flip Off = live=false, retarget back, htaccess regenerated (noindex on preview host only; live host serves the preview-state files).

## Parent rules (done 20 Nov)
autoseo.my root .htaccess: host-limited (HX thread) + golive:cch-automotive block; pageonesingapore.com folder .htaccess: redirects now only for pageonesingapore.com / www, ACME excluded. public_html/.htaccess (sgmodder.com main domain) has no Bridge key: not touched.

## Not built yet
The Controller "Go live" control (domain field + Live toggle + status display) and the single Bridge function that runs the flip are Base44 backend work (needs a checkpoint and Edwin Publish). Spec above is the contract.

## Notes (20 Nov, Rasa Sayang go-live)
- parent_block ACME line printed %%{REQUEST_URI} (Apache would not match it); fixed to %{REQUEST_URI}, tests still 8 pass.
- Rasa build reads src/site.json directly (build.py: SITE/SHARE/NOINDEX from it, page-relative links via @@B@@). Root autoseo.my .htaccess holds the golive:rasa-sayang block (backup 20261120-135200-df179a = before).
- Bridge htaccess write: always pass the FULL file text; the tool writes exactly what it gets.
7. Articles + indexing (21 Nov 2026): a client served from an autoseo.my preview/<folder>/ needs one line in the Bridge AUTO_SITEMAP_SITE_FOLDERS (liveGuard.ts, Bridge save + Edwin Publish) and a row in night-writers/templates/article-autoindex/sites.json, or its articles get no sitemap.xml entry and no IndexNow.
