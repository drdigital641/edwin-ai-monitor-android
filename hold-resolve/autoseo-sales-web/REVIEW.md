# SPO review: AutoSEO Sales Web backend (before Publish)

App 6afc5a60aa13789d675618e9 is NEW and NOT published, so nothing is reachable yet. Publish is the gate.
Code: autoseo-sales-web/base44/sales-web.js (server route /api/sales-web).

Check points:
1. GET is public on purpose (Edwin: anyone with the link can view). Returns only id, name, role, parentId, createdAt.
2. POST: Origin must be https://autoseo.my (or www). PIN from secret SALES_EDIT_PIN, compared as SHA-256 digests in constant time. Secret missing or <6 chars = edits off (503).
3. Brute force: global EditGuard counter, 10 wrong PINs per 15 min then 429 for everyone until the window ends.
4. Writes use asServiceRole only after the PIN check. Entity RLS: SalesNode create/update/delete admin only; EditGuard all ops admin only.
5. Input: name stripped of control chars and < >, 60 chars max; role enum; parent must exist; person nodes may only get salesperson referrals; 500 node cap; centre cannot be removed.
6. Page renders names with textContent / SVG textContent only (no innerHTML).
Known limits: Origin can be faked by non-browser clients (PIN still required). No X-Robots-Tag header on autoseo.my/sales/ (would need the root .htaccess, which we don't touch); meta robots noindex,nofollow is set.
