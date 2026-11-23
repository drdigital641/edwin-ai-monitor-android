# Booking portal (booking-portal)

One multi-client booking app (PHP 8.1+, MySQL/MariaDB). Built 23 Nov 2026 to Edwin's spec v1 + his 8:16pm answers.
White-label: no agency name anywhere in the UI. Not for search engines (noindex meta + X-Robots-Tag on every response).

## Files (15 public files, well under the inode budget)
```
public/                      -> public_html/pageonesingapore.com/booking/
  index.php                  front controller (routes ?r=..., per-client stub folders)
  embed.js                   Book button popup/sheet + inline iframe auto-height (one file, every client)
  assets/portal.css          the only stylesheet (client colours come from the clients row)
  assets/portal.js           iframe height, Esc-to-close, confirmed signal (no PII)
  app/bootstrap.php          config loader, security headers, sessions (CHIPS), CSRF, e(), t()
  app/db.php                 schema + the ONE data layer (class Tenant = every tenant query)
  app/slots.php              the ONE slot engine (pure functions)
  app/booking.php            book / series / reschedule / cancel, all under SELECT ... FOR UPDATE
  app/views.php              the ONE layout + header/footer + shared pickers
  app/customer.php, admin.php, super.php   screens
  app/lang/en.php            all UI text (add ms.php / zh.php by translation only)
  app/seed/sg-autobots.json  SgAutobots starter (imported from the super-admin page)
  sg-autobots/index.php      2-line stub = clean URL /booking/sg-autobots/ without .htaccess
private/                     -> /home/<account>/booking-private/ (outside public_html)
  config.sample.php, my.cnf.sample, backup.sh
tests/                       run_tests.php (59 checks), concurrency.php, e2e/*.js (Playwright)
```
Every app/*.php file exits with 404 if opened directly.

## URLs
- Customer: `https://pageonesingapore.com/booking/<slug>/` (optional `?service=<service-slug or site hub slug>`)
- Client admin: `https://pageonesingapore.com/booking/<slug>/?r=a`
- Super-admin: `https://pageonesingapore.com/booking/?r=s` (first visit = setup with the token from the private config)
- embed.js: `https://pageonesingapore.com/booking/embed.js`
- Base URL is one config value (`base_url`), so a later white-label subdomain is one edit.

## Deploy (needs cPanel / Domain Go-Live: the Bridge refuses PHP)
1. Back up first (rule): nothing exists yet at booking/; for later uploads run backup.sh before replacing files.
2. Create DB + user (see the request in the thread report), privileges SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX on that DB only, host localhost.
3. Create /home/<account>/booking-private/ (chmod 700) with config.php + my.cnf from the samples (chmod 600) and sessions/ (chmod 700).
4. Upload public/ to public_html/pageonesingapore.com/booking/ (skip any test-* folder).
5. Add booking/.htaccess (lines below, Edwin's OK needed).
6. Open /booking/?r=s, enter the setup token, set the super-admin password, then blank setup_token in the config.
7. Import sg-autobots, create its client admin, hand the login to the client.

## .htaccess needed (NOT written; needs Edwin's OK)
The root public_html/pageonesingapore.com/.htaccess sends `X-Frame-Options: SAMEORIGIN` and `Content-Security-Policy: frame-ancestors 'self'` with `Header always set`,
which blocks the iframe/popup on every client domain. And mod_expires would let browsers cache portal HTML for 10 minutes. New file booking/.htaccess:
```
<IfModule mod_headers.c>
  Header always unset X-Frame-Options
  Header always unset Content-Security-Policy
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive Off
</IfModule>
```
PHP then sends its own per-client CSP (frame-ancestors 'self' + that client's allowed_embed_domains) and Cache-Control: no-store.
The direct link (booking_url) works without this file; only the popup and iframe embeds on other domains need it.

## Backups and restore
- Nightly: `sh ~/booking-private/backup.sh` from the ONE existing nightly cron (rule 21), e.g. `17 3 * * * sh $HOME/booking-private/backup.sh`. Dumps go to `~/backups-private/booking/booking-YYYYmmdd-HHMMSS.sql.gz`, 14 days kept.
- Restore: `gunzip -c ~/backups-private/booking/booking-<stamp>.sql.gz | mysql --defaults-extra-file=$HOME/booking-private/my.cnf <dbname>` (take a fresh dump first).

## Tests
```
P1B_CONFIG=/path/to/test-config.php php tests/run_tests.php      # refuses unless test_mode
P1B_CONFIG=/path/to/test-config.php php tests/concurrency.php 25
```
