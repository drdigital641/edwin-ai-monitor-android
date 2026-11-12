# AutoSEO client dashboard (autoseo.my/admin)

Spec: Edwin 12 Nov 2026 (thread "Build AutoSEO admin mini dashboard"). PREVIEW ONLY until the Security & Privacy Officer
reviews login and data scoping. Never put live without Edwin's word.

- Static page: `index.html` + `config.js` (public Google Client ID + Controller function URL, no secrets).
- One dictionary for every word, EN + Simplified Chinese together: `assets/strings.js`.
- Templates (header/menu, KPI tile, client card, 3-step strip, payment block, form) in `assets/admin.js`.
- `?demo=1` loads `assets/demo.js` (made-up rows) for design review only.
- noindex: meta robots here + X-Robots-Tag from the folder .htaccess; never in sitemap/llms.txt.

Server contract (Controller function, POST JSON with `id_token` = Google ID token):
`me`, `clients`, `save_memo {client_id, memo}`, `create_client {company, url, url_type: new|existing, notes}`.
The function verifies the Google token (signature, audience, email_verified), checks the allowlist and
returns/edits ONLY rows owned by that account. The page never filters other accounts' data itself.
