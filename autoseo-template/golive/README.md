# One-switch go-live template (Edwin, 20 Nov 2026, 6:59pm SGT; addendum 7:03pm)

Going live = addon domain + SSL + flip ONE switch. No per-page tag rewrites.

## Config (site.json, later the Controller site record)
`slug`, `preview_url`, `live_domain` (EMPTY at preview build time), `live` (false/true), `languages`, `og_image` (JPG 1200x630, default images/og.jpg), `og_version`.
Examples: hx-auto.site.json, cch-automotive.site.json, site.example.json. `live` is forced false while `live_domain` is empty.

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

## Flip runbook (what one run must do)
1. domain_status OK, else refuse and show the status.
2. set live=true, live_domain; retarget_tree on the built site (or rebuild); regenerate sitemap.xml, robots.txt, llms.txt.
3. sync_from_github (base_sha256 map from dry run) to the site; backup is automatic.
4. htaccess: read, write generated rules with test_urls (auto-restore on 5xx).
5. go_live_check, report to Controller + needs_you done/blocked. Flip Off = live=false, retarget back, htaccess regenerated (noindex on preview host only; live host serves the preview-state files).

## Parent rules (done 20 Nov)
autoseo.my root .htaccess: host-limited (HX thread) + golive:cch-automotive block; pageonesingapore.com folder .htaccess: redirects now only for pageonesingapore.com / www, ACME excluded. public_html/.htaccess (sgmodder.com main domain) has no Bridge key: not touched.

## Not built yet
The Controller "Go live" control (domain field + Live toggle + status display) and the single Bridge function that runs the flip are Base44 backend work (needs a checkpoint and Edwin Publish). Spec above is the contract.
