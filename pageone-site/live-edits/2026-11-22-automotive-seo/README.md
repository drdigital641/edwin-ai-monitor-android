# Page One automotive SEO sync (22 Nov 2026)

live/ = exact Bridge copies (sha256-checked) of the files Website Manager changed or added on 22 Nov 2026 ~3:42-3:57pm SGT:
index.html, about/, results/, industries/car-workshop/, industries/car-detailing/, sitemap.xml, llms.txt,
automotive.css, automotive-seo-singapore/ (hub + 3 sub-pages), images/automotive/ (8 files).
Website Manager owns automotive-seo-singapore/* until Mon 23 Nov 23:59 SGT: do not rebuild or rewrite those pages.

Then (this thread): "Automotive SEO" (/automotive-seo-singapore/) added as the first nav item and the 5 automotive links
(hub, /industries/car-workshop/, accident-repair-spray-painting/, car-battery-tyre-shops/, case-studies/) added at the
top of the footer Services column on every other live page, by live edit (read sha -> edit_file). 77 pages, list +
Bridge backup ids in edit-backups.tsv. review.html (noindex review helper, no site nav) skipped on purpose.
/industries/: new first card "Automotive businesses" + ItemList entry 15. /clients/: nav, footer and a hub link under the
Car workshops Search Console card; made in the clients-registry builder chrome (ref/pageone/clients/index.html), so
build_pageone.py output == live sha cacc3eb6...

No full re-render was run. The Python builder (pageone-site/builder/, last on branch claude/project-thread-xc39oz,
14 Nov) is older than live; builder-nav-footer.patch carries the same nav/footer change for it. Never re-render
from that builder without diffing against live first.

22 Nov 4:23pm SGT, follow-up: /articles/ and all 34 article pages had an older nav (no How it works, had SEO Boost) and footer
(missing How it works, Lead generation, Affordable SEO services). Nav and footer Services now match the live homepage exactly;
article content, p1-cta.js and review footer untouched. Backups: article-edit-backups.tsv.
