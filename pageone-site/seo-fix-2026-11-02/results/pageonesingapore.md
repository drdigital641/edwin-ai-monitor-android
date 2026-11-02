# pageonesingapore.com (2 Nov 2026) - confirmation only
| item | result |
|---|---|
| robots.txt Disallow /preview/ | confirmed in live file (all user-agent blocks disallow /preview/ and /dmts/) |
| X-Robots-Tag noindex on previews | confirmed in live preview/.htaccess (sha dfebd929..., Header always set for host pageonesingapore.com). HTTP header itself not fetched: probe prints status only |
| other changes | none |

## Continuation (2 Nov 2026, second helper)
X-Robots-Tag check: .github/probe/probe.sh now prints headers (HTTP, x-robots-tag, location) for .github/probe/urls/headers.txt (preview/cska-auto, ecu-clinic, dmts, aivs and the root). Pushed in a9dfbea9c; run 41418868108 and later include a "##### HEADERS" section. NOT yet read by me. Run 41417680060 log tail is the sitemap audit; hub 200 / unknown-URL 404 / single-hop 301 lines were NOT confirmed by me.
Warning: a later push from another thread overwrote my first probe.sh edit (e42d430c9); re-applied in a9dfbea9c. Pushes from stale trees can revert others' files.

## X-Robots-Tag confirmed (2 Nov 2026, third helper; probe run 41418868108, "##### HEADERS" section)
| URL | result |
|---|---|
| /preview/cska-auto/ | HTTP/2 200, x-robots-tag: noindex, nofollow |
| /preview/ecu-clinic/ | HTTP/2 200, x-robots-tag: noindex, nofollow |
| /preview/dmts/ | HTTP/2 200, x-robots-tag: noindex, nofollow |
| /preview/aivs/ | HTTP/2 200, x-robots-tag: noindex, nofollow |
| root / | HTTP/2 200, no x-robots-tag (correct) |
Note: probe.sh header printing was reverted once by stale-tree commit 9ecfc7279 and restored in 77eb2094f.
