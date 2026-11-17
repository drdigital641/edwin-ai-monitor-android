# autoseo.my/sales - commission web (internal, noindex)

Edwin, 17 Nov 2026 9:41pm SGT. Internal sales-team page, AutoSEO.my as the centre node.

- Page: `site/sales/index.html` (one file). 17 Nov 10:01pm Edwin: simplified to ONE folder-list view (no web diagram). Live at https://autoseo.my/sales/ via Bridge sync_from_github.
- Commission numbers: ONE config object `SPLIT` at the top of the page script (RM300 sale, RM200 kept, RM100 pool, RM60 Level 1, RM40 Level 2, 2 levels).
- noindex,nofollow meta (robots + googlebot). Not in sitemap.xml, llms.txt, nav or footer. No WhatsApp/public CTAs; p1-cta.js kept as on every page.
- Backend: Base44 app "AutoSEO Sales Web" (6afc5a60aa13789d675618e9). Entities SalesNode (id, name, role centre|dealer|salesperson, parentId, createdAt; public read, admin-only writes) and EditGuard (admin-only). Server route `src/routes/api/sales-web.js` (copy in `base44/sales-web.js`): GET = list, POST = check/add/remove with PIN.
- Edit PIN = Base44 secret SALES_EDIT_PIN (never in page source or this repo). Wrong PINs: 10 per 15 min across everyone, then all edits locked for the rest of the window. POST only from https://autoseo.my origin.
- The page works only after the Base44 app is Published (Publish only, never Activate). Until then it shows the AutoSEO centre node and "Live data is not connected yet".
