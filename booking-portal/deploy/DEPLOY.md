# Booking engine v2: deploy manifest (job booking-portal-deploy-v2)

Edwin, 23 Nov 2026, 8:54pm SGT: nothing at pageonesingapore.com/booking/, no links from Page One, each client has its own booking data.
Trial client: SgAutobots on its preview. **Hold the v1 package (deploy/ of job booking-portal-deploy): it is superseded and must not be installed.**

Placeholders only in this package. `<account>` is the cPanel home user, `<prefix>` the cPanel DB prefix, `<docroot>` the folder that serves https://pageonesingapore.com/ (the one holding `preview/sg-autobots/index.html`, likely `public_html/website_b1ec45f5/`). Real passwords, pepper and setup token are made on the server and never written into a drop, the repo, notes, a log or a reply.

## 1. Layout

```
/home/<account>/booking-engine/            SHARED CODE, outside public_html (chmod 755 dirs, 644 files)
  engine.php                               front controller
  embed.js                                 Book button popup + inline iframe height (served through each entry, ?asset=embed)
  assets/portal.css  assets/portal.js      served through each entry (?asset=css|js)
  app/bootstrap.php db.php slots.php booking.php views.php customer.php admin.php
  app/lang/en.php
  app/seed/sg-autobots.json                SgAutobots client row + 8 services (Edwin 8:16pm list), hours empty

/home/<account>/booking-clients/sg-autobots/   THIS CLIENT'S PRIVATE FOLDER, outside public_html (chmod 700)
  config.php                               from config.sample.php (chmod 600): own DB, own pepper, own setup token, base_url
  my.cnf                                   from my.cnf.sample (chmod 600): for backups/restores
  sessions/                                (chmod 700)

<docroot>/preview/sg-autobots/booking/index.php         PUBLIC ENTRY, customer (3 lines, no secrets)
<docroot>/preview/sg-autobots/booking/admin/index.php   PUBLIC ENTRY, admin (4 lines, no secrets)

/home/<account>/backups-private/booking/<client-slug>/  nightly dumps (chmod 700)
```

Package file -> server path (rename `.php.txt` to `.php`; `.txt` names exist only because drops allow one dot):

| Package file | Server path |
|---|---|
| engine/engine.php.txt | /home/<account>/booking-engine/engine.php |
| engine/embed.js | /home/<account>/booking-engine/embed.js |
| engine/assets/portal.css, portal.js | /home/<account>/booking-engine/assets/ |
| engine/app/*.php.txt (7 files) | /home/<account>/booking-engine/app/*.php |
| engine/app/lang/en.php.txt | /home/<account>/booking-engine/app/lang/en.php |
| engine/app/seed/sg-autobots.json | /home/<account>/booking-engine/app/seed/sg-autobots.json |
| entry/booking/index.php.txt | <docroot>/preview/sg-autobots/booking/index.php |
| entry/booking/admin/index.php.txt | <docroot>/preview/sg-autobots/booking/admin/index.php |
| private/config.php.txt (= private/config.sample.php in the repo) | /home/<account>/booking-clients/sg-autobots/config.php (fill in) |
| private/my.cnf.txt (= private/my.cnf.sample) | /home/<account>/booking-clients/sg-autobots/my.cnf (fill in) |
| private/backup.sh | /home/<account>/booking-clients/backup.sh (chmod 700) |
| schema.sql.txt | import into the client database (optional: the engine creates the tables itself) |

In both entry files replace `<account>` and `<client-slug>` (`sg-autobots`). Nothing else goes in a public folder: no config, no .sql, no .bak, no engine code.

## 2. Why one database per client (recommended, built this way)
- **No query can cross clients.** Each entry loads one config, which opens one database. The data layer is also tenant-scoped (every query carries the client id), so there are two walls, not one.
- **Moving a client is zero migration.** The database stays where it is; only the entry folder and `base_url` change (section 6).
- **Separate backup, restore and export.** One client's restore never rolls back another client. A client who leaves gets their own dump.
- **Smaller blast radius.** A leaked DB password exposes one client only, because each client has its own DB user.
- Cost: one DB + one DB user per client in cPanel, and one config folder. backup.sh loops over all of them, so there is still one cron line.

## 3. Install steps (Domain Go-Live, cPanel)
0. **Backup first** (timestamped .tgz in `~/backups-private/` of `<docroot>/preview/sg-autobots/`), and tell Edwin the path.
1. Check PHP is 8.1 or newer for `<docroot>` (built for 8.1+, tested on 8.3).
2. MySQL Databases: create DB `<prefix>_bk_sgautobots` (utf8mb4) and user `<prefix>_bksga` with a strong random password. Privileges on that DB only, host localhost: SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX.
3. Upload the engine to `/home/<account>/booking-engine/` (table above).
4. Create `/home/<account>/booking-clients/sg-autobots/` (700), `sessions/` (700), `config.php` and `my.cnf` (600). Fill: db_pass, pepper (64 random hex), setup_token (40+ random chars). Keep `base_url = https://pageonesingapore.com/preview/sg-autobots/booking`, `embed_domains = ['pageonesingapore.com']`, `test_mode = false`, `test_client = false`.
5. Optional: import `schema.sql` into the DB (`mysql --defaults-extra-file=.../my.cnf <prefix>_bk_sgautobots < schema.sql`).
6. Upload the two entry files to `<docroot>/preview/sg-autobots/booking/` and `.../booking/admin/`.
7. Open `https://pageonesingapore.com/preview/sg-autobots/booking/admin/`. It shows **First-time setup**. Enter the setup token, an admin username and a password (12+). This imports SgAutobots and its 8 services and creates the client admin. Then blank `setup_token` in config.php.
8. Cron: add `sh $HOME/booking-clients/backup.sh` to the existing nightly job (rule 21), or one line `17 3 * * *` if none exists. Note: backup.sh removes its own dumps older than 14 days in `~/backups-private/booking/` only; drop the `find` line if Edwin wants every dump kept.
9. Do **not** change `booking_url` in the preview's site-config.json. It stays "" until Edwin says go.

## 4. .htaccess (listed separately): NONE needed now
- The trial embeds on pageonesingapore.com itself (same origin), so the root `.htaccess` headers (X-Frame-Options SAMEORIGIN, CSP frame-ancestors 'self') already allow it.
- PHP sends its own noindex (`X-Robots-Tag: noindex, nofollow` + meta), CSP, `Cache-Control: no-store` on every response.
- Only needed later, and only inside a client's entry folder, if that client's host adds framing headers that block its own domain. Edwin's OK first. Content would be:
```
<IfModule mod_headers.c>
  Header always unset X-Frame-Options
  Header always unset Content-Security-Policy
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive Off
</IfModule>
```

## 5. Smoke tests (fake numbers +65000000xx only; never a real customer)
SgAutobots stays clean: its hours are empty, so it cannot take bookings. Booking flows are tested on a separate **smoke client** with its own database, then closed.

**A. SgAutobots (real client, no test data)**
1. `curl -sI https://pageonesingapore.com/preview/sg-autobots/booking/` -> 200, `X-Robots-Tag: noindex, nofollow`, `Content-Security-Policy ... frame-ancestors 'self' https://pageonesingapore.com https://www.pageonesingapore.com`, `Cache-Control: no-store`.
2. The page shows "Online booking is not open yet ... WhatsApp us to book" (WhatsApp +65 8366 7010).
3. `.../booking/?asset=css&v=1` -> 200 text/css; `.../booking/?asset=embed` -> 200 JavaScript.
4. Admin: log in at `.../booking/admin/`. Settings > Services lists the 8 services with Edwin's prices; Opening hours is empty; Embed codes shows URLs under `/preview/sg-autobots/booking/`.
5. `https://pageonesingapore.com/booking/` -> 404 (nothing there). The engine and config are not reachable by any URL.

**B. Smoke client (test only)**
1. DB `<prefix>_bk_smoke`, user `<prefix>_bksmk` (same privileges), folder `/home/<account>/booking-clients/smoke-test/` with config: `client_slug 'smoke-test'`, `seed 'none'`, `base_url https://pageonesingapore.com/preview/booking-smoke`, `test_mode true`, `test_client true`, own pepper + setup token.
2. Entries at `<docroot>/preview/booking-smoke/index.php` and `admin/index.php` (same 3/4 lines, slug smoke-test). Not linked anywhere, noindex.
3. Admin setup with the token -> Settings: hours Mon-Sat 09:00-18:00; add service "Smoke test wash", 60 min, active.
4. Customer: register **+6500000001**, name "Smoke Test", PIN 480317 -> book tomorrow's first slot -> confirmation shows a ref -> My bookings -> Reschedule to another slot -> Cancel.
5. Admin day view for that date (`.../admin/?r=a&d=YYYY-MM-DD`) shows the booking, tagged test, status Cancelled.
6. Isolation: the same +6500000001 / 480317 on `.../preview/sg-autobots/booking/?r=login` -> "The mobile or PIN is wrong" (separate database).
7. Five wrong PINs on +6500000001 -> locked for 15 minutes.
8. Finish: in the smoke admin, Settings > Opening hours: tick every day **closed** (customers then see "WhatsApp us to book"); blank its setup_token. The folders stay (no deletions); Edwin decides later.

## 6. Moving SgAutobots to his own domain (zero data migration)
Same server (Bluehost addon domain):
1. Copy the two entry files to `<his docroot>/booking/` and `<his docroot>/booking/admin/` (still pointing at the same engine and the same `/home/<account>/booking-clients/sg-autobots/config.php`).
2. In that config: `base_url => 'https://<his-domain>/booking'`, `embed_domains => ['<his-domain>']`.
3. Update the Book buttons / booking_url on his site to the new URL, and in admin Settings > Branding point the logo at his domain. The database, customers, PINs and bookings are untouched.
4. Old preview entry: leave it, or (Edwin's OK) replace it with a redirect page to the new URL.

Different server later: dump `<prefix>_bk_sgautobots` with `my.cnf`, import it there, copy the engine + his config folder, change the db_* values. Still one client's data only; nothing to separate.

## 7. Backups and restore
- Nightly: `~/backups-private/booking/<slug>/<slug>-YYYYmmdd-HHMMSS.sql.gz`, one folder per client, 14 days.
- Restore one client: take a fresh dump first, then `gunzip -c <file> | mysql --defaults-extra-file=$HOME/booking-clients/<slug>/my.cnf <that client's db>`. No other client is touched.
- Back up before every upload.

## 8. Adding the next client
New DB + user, new `booking-clients/<slug>/` folder with its own config (own pepper and token), a seed file `app/seed/<slug>.json` (or none: the admin fills Settings), two entry files in that client's site folder. The engine is not copied.

## 9. Tests run off-server (23 Nov 2026)
Unit 59/59 (slot engine, isolation, lockout). Concurrency: 25 races, 0 double bookings. Browser (Chromium) on the v2 layout with two client databases: SgAutobots setup imported 8 services and shows WhatsApp; demo client register, book, reschedule, cancel at 390 and 360 with no horizontal scroll and all taps 44px+; demo login refused on SgAutobots; popup + inline iframe from another site with the session held; Esc closes. Not tested: real iOS Safari, and the live server.
