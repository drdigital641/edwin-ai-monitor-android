# DEPLOY: booking portal (job booking-portal-deploy)

Edwin approved 23 Nov 2026 8:45pm SGT: MySQL DB + user, private config, upload of booking/ (PHP), booking/.htaccess, backup first.
Do NOT change booking_url on the SgAutobots preview (Edwin: not yet).
No real secrets are in this package. Every value in <angle brackets> is a placeholder to fill on the server only.

## 0. Requirements
- PHP 8.1 or newer (tested on 8.3) with pdo_mysql and mbstring. In cPanel > MultiPHP Manager, check the version on pageonesingapore.com.
- MySQL 5.7+/MariaDB 10.3+ (tested on MariaDB 10.11), InnoDB, utf8mb4.
- Apache with mod_headers (already used by the root .htaccess).

## 1. Backup first
```
mkdir -p ~/backups-private && tar czf ~/backups-private/pageone-booking-predeploy-$(date -u +%Y%m%d-%H%M%SZ).tgz -C ~/public_html/<pageonesingapore docroot> .htaccess
```
(booking/ does not exist yet; the root .htaccess is backed up as proof it is not touched). Report the tgz path to Edwin.

## 2. Database (cPanel > MySQL Databases)
- Database: `<cpanelprefix>_booking` (cPanel adds the prefix)
- User: `<cpanelprefix>_bookapp`, strong random password (40+ chars, cPanel generator)
- Privileges for that user on that DB only: SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX
- Host: localhost

## 3. Private folder OUTSIDE the web root
```
/home/<account>/booking-private/            chmod 700
/home/<account>/booking-private/config.php  chmod 600   (from private__config.sample.php.txt)
/home/<account>/booking-private/my.cnf      chmod 600   (from private__my.cnf.sample.txt)
/home/<account>/booking-private/backup.sh   chmod 700   (from private__backup.sh.txt)
/home/<account>/booking-private/sessions/   chmod 700   (empty folder)
/home/<account>/backups-private/booking/    chmod 700   (empty folder)
```
config.php keys (fill on the server; never paste values into chat, a drop, a log or the repo):
| key | value |
|---|---|
| base_url | `https://pageonesingapore.com/booking` |
| db_host | `localhost` |
| db_name | `<cpanelprefix>_booking` |
| db_user | `<cpanelprefix>_bookapp` |
| db_pass | `<BOOKING_DB_PASSWORD>` |
| pepper | `<BOOKING_PEPPER>`: 64 random hex chars |
| setup_token | `<BOOKING_SETUP_TOKEN>`: 40+ random chars; give it to Edwin privately; blank it after step 6 |
| session_path | `/home/<account>/booking-private/sessions` |
| test_mode | `true` for the smoke test only (allows +65000000xx numbers, flagged is_test), then `false` |
| cookie_secure, hsts | `true` |
| lang | `en` |
The app reads `$HOME/booking-private/config.php`; if PHP has no HOME it walks up from booking/app to the first folder outside public_html (the account home) and reads `booking-private/config.php` there. It never looks inside public_html.

## 4. Schema
```
mysql --defaults-extra-file=$HOME/booking-private/my.cnf <cpanelprefix>_booking < schema.sql
```
(or cPanel > phpMyAdmin > Import schema.sql). Optional: the app also creates the same tables itself on the first super-admin visit. 11 tables.

## 5. Upload the app (20 files total in the package; 15 go in booking/)
Folder: `public_html/<pageonesingapore docroot>/booking/` (the root .htaccess comment names the docroot `public_html/website_b1ec45f5/`; confirm in cPanel > Domains) (create `booking/`, `booking/app/`, `booking/app/lang/`, `booking/app/seed/`, `booking/assets/`, `booking/sg-autobots/`). Files 644, folders 755.
The PHP user must be able to create new client folders inside booking/ (the super-admin "Add client" makes `booking/<slug>/index.php`). With suPHP/PHP-FPM as the account user (Bluehost default) 755 is enough.

| Package file | Install as (drop the .txt, `__` = folder) | sha256 (first 16) |
|---|---|---|
| app__admin.php.txt | public_html/<pageonesingapore docroot>/booking/app/admin.php | `fe12a536073100e2` |
| app__booking.php.txt | public_html/<pageonesingapore docroot>/booking/app/booking.php | `5877cae5c3dd15ad` |
| app__bootstrap.php.txt | public_html/<pageonesingapore docroot>/booking/app/bootstrap.php | `6059933efeb1f6e2` |
| app__customer.php.txt | public_html/<pageonesingapore docroot>/booking/app/customer.php | `d4161b76318193b5` |
| app__db.php.txt | public_html/<pageonesingapore docroot>/booking/app/db.php | `7918c63773307eb0` |
| app__lang__en.php.txt | public_html/<pageonesingapore docroot>/booking/app/lang/en.php | `4efd0f6c4e6849a6` |
| app__seed__sg-autobots.json.txt | public_html/<pageonesingapore docroot>/booking/app/seed/sg-autobots.json | `5592903cc2987bad` |
| app__slots.php.txt | public_html/<pageonesingapore docroot>/booking/app/slots.php | `b299162c2a9ac9c9` |
| app__super.php.txt | public_html/<pageonesingapore docroot>/booking/app/super.php | `debf651a1377c04c` |
| app__views.php.txt | public_html/<pageonesingapore docroot>/booking/app/views.php | `6f6bed16771e847b` |
| assets__portal.css.txt | public_html/<pageonesingapore docroot>/booking/assets/portal.css | `64d674281e4de82f` |
| assets__portal.js.txt | public_html/<pageonesingapore docroot>/booking/assets/portal.js | `c1af3e6c153aad19` |
| embed.js.txt | public_html/<pageonesingapore docroot>/booking/embed.js | `43ac99bbb09d6119` |
| index.php.txt | public_html/<pageonesingapore docroot>/booking/index.php | `e9279ea0ec0b1d31` |
| sg-autobots__index.php.txt | public_html/<pageonesingapore docroot>/booking/sg-autobots/index.php | `27121868e96078ce` |
| booking.htaccess.txt | public_html/<pageonesingapore docroot>/booking/.htaccess | `4bcc79a159b9ecc4` |
| private__config.sample.php.txt | /home/<account>/booking-private/config.php (fill values on the server) | sample |
| private__my.cnf.sample.txt | /home/<account>/booking-private/my.cnf (fill values on the server) | sample |
| private__backup.sh.txt | /home/<account>/booking-private/backup.sh | `8d7647f8fa19f990` |
| schema.sql.txt | not installed: import once into the DB (step 4) | `a3471baaa060924d` |

Leave no .txt, .sql, .bak or .md copies in public folders (the .htaccess also denies them).

## 6. First setup (Edwin)
1. Open `https://pageonesingapore.com/booking/?r=s`, enter the setup token, choose a username and a password of 12+ characters. Then blank `setup_token` in config.php.
2. Super-admin page: under "Import starter client" press **sg-autobots**. This creates the client (status setup, 8 services from the owner's list, hours EMPTY) and the folder stub if it is missing.
3. On the SgAutobots client page: "Create or reset client admin" with a username and a 12+ character password. Edwin hands it to the client. Nobody else receives it.
4. The client sets Mon-Sun hours and off days in Admin > Settings. Until then customers see "WhatsApp us to book". Saving hours switches the client to live.

## 7. Smoke test (test_mode true; fake numbers only; never contact anyone)
For the booking steps, make a TEST client so SgAutobots stays untouched: super-admin > Add client, slug `smoke-test`, any colours, status live; give it a client admin; in its admin set hours Mon-Sat 09:00-18:00 and switch one service on (Admin > Settings > Services > Add a service, 60 min, active).
1. `curl -sI https://pageonesingapore.com/booking/sg-autobots/` -> 200, has `X-Robots-Tag: noindex, nofollow`, `Content-Security-Policy ... frame-ancestors 'self' https://pageonesingapore.com https://www.pageonesingapore.com`, and NO `X-Frame-Options`.
2. Open `/booking/sg-autobots/` -> shows "WhatsApp us to book" (hours empty). Correct.
3. `/booking/smoke-test/` -> Register with mobile `+6500000001`, name "Smoke test", PIN `480317` twice, tick the privacy box.
4. Book a service -> pick a date -> pick a time -> Confirm. The confirmation shows a ref like `SMO-XXXXXX`.
5. My bookings -> Reschedule -> pick another time -> "Moved ...". The ref stays the same.
6. My bookings -> Cancel booking -> "Cancelled: ...".
7. Admin: `/booking/smoke-test/?r=a` -> log in -> Day view -> date picker to the booking date -> the booking shows (time, name, mobile, service, status). Week view works.
8. Log out, then 5 wrong PINs for +6500000001 -> the account locks for 15 minutes.
9. `curl -sI https://pageonesingapore.com/booking/app/db.php` -> 404 (direct include access refused). `curl -sI .../booking/app/seed/sg-autobots.json` -> 403.
10. After the test: super-admin > smoke-test > status `paused`; set `test_mode` to false in config.php. Test customers are is_test and never mix with SgAutobots.
Report each step's result (pass/fail) to Edwin.

## 8. Backups (rule 21: no duplicate crons)
Add `sh $HOME/booking-private/backup.sh` to the existing nightly cron job. If there is none, one line: `17 3 * * * sh $HOME/booking-private/backup.sh`.
Dumps go to `~/backups-private/booking/booking-YYYYmmdd-HHMMSS.sql.gz` and 14 days are kept.
Restore: dump first, then `gunzip -c <file> | mysql --defaults-extra-file=$HOME/booking-private/my.cnf <cpanelprefix>_booking`.

## 9. URLs after deploy
```
Customer (SgAutobots): https://pageonesingapore.com/booking/sg-autobots/
Client admin:          https://pageonesingapore.com/booking/sg-autobots/?r=a
Super-admin:           https://pageonesingapore.com/booking/?r=s
embed.js:              https://pageonesingapore.com/booking/embed.js
```
Source: repo drdigital641/edwin-ai-monitor-android, branch claude/project-thread-yndfoh, folder booking-portal/ (README has full notes).
