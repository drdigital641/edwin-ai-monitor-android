# XADO shared parts (xado-shop.sg)

How the site is built: plain static HTML files edited live on Bluehost through the Bridge (folder
public_html/website_b1ec45f5/preview/xado). There is no server-side include (that needs `Options +Includes`
in .htaccess, which only Edwin can approve), so repeated parts come from this folder instead:

- related-articles.json : the ONE list of article titles, categories, images and "Keep reading" picks.
  Rules: 3-4 related per article, from the same topic group where possible; every article listed by 2+ others.
- xado_shared.py        : renders the Keep reading block and fixes Home/logo links.
  `python3 xado_shared.py check` | `render <slug>` | `apply <page.html> [slug]`

Rules for every page (17 Nov 2026, GSC fix):
- Home/logo/breadcrumb links are `href="/"`; BreadcrumbList Home item is `https://xado-shop.sg/` (never index.html,
  which 301s and shows as "Page with redirect" in Search Console).
- 404.html has noindex and NO canonical.

Night run (new XADO article):
1. Copy head/header/footer from a current live article (read_live_file), Home links already "/".
2. Add the new article to related-articles.json and add its slug to the related list of 2+ existing articles.
3. `python3 xado_shared.py check`, then `render <new-slug>` for the new page's Keep reading block, and for each
   existing article whose list changed, replace its Keep reading block live with edit_file (expected_sha256 = base).
Copy for night workers: /mnt/project-files/xado/shared/ (keep in step with the repo).
