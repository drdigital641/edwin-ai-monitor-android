# Article auto-index template (21 Nov 2026, Edwin, PERMANENT, every roster site)

Every article the API runner (Grok Bot box, `jobs/midnight_article.py`) publishes goes through ONE shared step,
`article_autoindex.publish()`. It is a template, not a per-site script: `sites.json` holds one row per site.

What it does for each new article (all reads and writes through the Bridge runner API, live edit rule):

| Step | How |
|---|---|
| Hub card | reads the site's hub, puts the new card FIRST in its card list (same markup as the current first card: `first_card()` finds it), appends to a JSON-LD ItemList if the hub has one, writes with `expected_sha256` |
| Page + hub write | one `bridgeWriteMany` call. The Bridge auto-sitemap step adds the article to the site's `sitemap.xml` with today's lastmod (SGT), bumps the hub lastmod, adds `llms.txt` lines, sends IndexNow |
| Sitemap check | the article URL must be in `autoSitemap.added/bumped`; if not, one `bridgeRunnerSitemap` resend. Page One's own root is excluded from the Bridge step by design, so the template adds its `<url>` and bumps `/articles/` itself. After the write it reads `sitemap.xml` back and confirms the URL + lastmod |
| IndexNow | article URL + hub URL + `https://<host>/sitemap.xml` (IndexNow = Bing, Yandex, Seznam, Naver). Google finds the page from the updated sitemap; the deprecated Google sitemap ping is never used |
| 429 / failure | URLs go to `state/indexnow-queue.json`; `resend_queue()` resends them at the start of the next `--live` or `--resend-indexnow` run; expired after 7 days (logged) |
| Log | one JSON line per article in `state/article-autoindex.log.jsonl` (no keys, no page content) |

Sitemaps are `sitemap.xml` ONLY (Edwin 16 Nov 2026): the template never reads, writes or pings a `sitemap.txt`.
Cleanic and ContiExpert: articles only (`articles_only` rows), the template writes only the article page and the hub.

## Wiring it into the runner (Grok Bot / Website Manager, one-time)

```python
from article_autoindex import Bridge, load_sites, Page, publish, resend_queue
br, sites = Bridge(), load_sites()          # Bridge() reads BRIDGE_RUNNER_KEY from the environment
resend_queue(br, sites)                     # first line of every --live and --resend-indexnow run
# per article, after the page HTML, hero image and card HTML are final:
rep = publish(br, sites[site_key], [Page(path=page_path, html=page_html, card_html=card_html)])
# Rule 6 (Edwin 22 Nov 2026 10:55am): write the article ONCE in English. Malaysian-address sites: add ms/zh Page() entries only from the
# cheap translation step (hub_path='ms/articles/index.html' etc.), never written on the paid writer. Other sites: one English Page().
if not rep['ok']: ...                       # rep['problems'] lists what failed; put it in the run's done/blocked alert
```

The runner's own sitemap / hub / IndexNow code for articles is then replaced by this call (keep its 429 queue only
if it also queues non-article URLs). Test offline: `python3 test_article_autoindex.py` (10 tests, fake Bridge).

## Sites (sites.json)

36 rows: the 34 active roster sites Edwin listed (Hon Win Motor and the sgcarworkshop.sg directory are separate rows
on the same sitemap) plus HX Auto. Status other than `active` = skipped and logged:

- `autotex` blocked: autotexautoparts.com.sg does not resolve (NXDOMAIN at SGNIC, checked 21 Nov 2026).
- `hx-auto` hold: hxautoservice.com.my is served from autoseo.my `preview/hx-auto/`; the Bridge only covers it after
  the "article-autoindex" Bridge change (hold-resolve/article-autoindex/) is saved and Published. Then set it `active`.
- Fitout (commercialfitout.sg) and preview-only sites (911 Garage, Carku, Hyper Power, EXN Lube, Moon Wiper) have no row.

New site on the runner = add a row the same day (host as the live sitemap uses it, Bridge site, base folder, hub path).
An AutoSEO client served from an autoseo.my folder also needs its line in the Bridge `AUTO_SITEMAP_SITE_FOLDERS`.

## 22 Nov 2026 update (thread "Fix AutoSEO article runner gaps")
- Bridge cp 6b01e564b5721916f9ec0770 (Edwin Publishes): runner key may use site `cchauto` (CCH live folder); hx-auto, overseas-tyre,
  rasa-sayang and sp-precision-parts get Bridge auto-sitemap + IndexNow on their own domains; IndexNow carries the sitemap URL; 429 = retry_later.
  After Publish set those 5 rows in sites.json to `active`.
- insert_hub_card(): an EMPTY AutoSEO hub list (`<div class="art-list" id="articles"></div>`) now gets the first card (status `inserted_first`).
- publish(): an English article whose ms/ or zh/ copy does not exist gets that hreflang line removed and the BM / 中文 switch
  pointed at /ms/articles/ or /zh/articles/ (drop_missing_lang_links), so runner articles never link a 404.
- Card markup for AutoSEO hubs: `<article class="art-card"><a href="/articles/<slug>/"><img src="/images/articles/<slug>.jpg" ...><div class="ac-b"><h2>Title</h2><p>One line</p><span class="ac-more">Read the article</span></div></a></article>`
  (first_card() copies the hub's first card, so HX and Rasa Sayang already carry the pattern). Tests 12/12.
