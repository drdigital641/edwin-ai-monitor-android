# Booking engine v2.1: changed files only (Edwin 23 Nov 2026, 9:52pm SGT)

Base: v2 (commit 79967808, live). Domain Go-Live replaces ONLY these files, the same way as v2. Back up first (timestamped .tgz of ~/booking-engine/ in ~/backups-private/). No config, entry-file or .htaccess change. No secrets in any file.

## What changes
1. **Car Wash package (10 washes):** when picked, Repeat opens on **Monthly** and Number of bookings on **10**, with one line under it: "You can reschedule any of these bookings yourself, in your account under My bookings." The default comes from the service's own settings (two new per-service fields, editable in admin > Settings > Services > the service: "Repeat preselected for customers" and "Number of bookings preselected"). Other services are unchanged (One-off / 4 as before, and non-recurring services show no repeat choice).
2. **Log in page:** "New here?" + a full-width **Create an account** button directly under Log in, inside the same card, same style as the site's secondary buttons (54px tall at 390 and 360; no horizontal scroll). Forgot your PIN stays below.

## Files (package path -> server path)
| Package file | Server path |
|---|---|
| engine/app/db.php.txt | ~/booking-engine/app/db.php |
| engine/app/customer.php.txt | ~/booking-engine/app/customer.php |
| engine/app/admin.php.txt | ~/booking-engine/app/admin.php |
| engine/app/lang/en.php.txt | ~/booking-engine/app/lang/en.php |
| engine/app/seed/sg-autobots.json | ~/booking-engine/app/seed/sg-autobots.json (only used by new installs) |
| engine/assets/portal.css | ~/booking-engine/assets/portal.css |
| migrate-v2.1.sql.txt | not uploaded: run once on the SgAutobots DB (below) |

Nothing changes in ~/booking-clients/sg-autobots/ (config.php, my.cnf, sessions/) or in the entry files under preview/sg-autobots/booking/. The CSS link carries a content hash, so browsers pick up the new CSS straight away.

## Database
Two new columns on `services`: `default_freq` ENUM('one','weekly','monthly') DEFAULT 'one', `default_repeats` TINYINT UNSIGNED NULL.
- Run, after the upload:
  `mysql --defaults-extra-file=$HOME/booking-clients/sg-autobots/my.cnf <prefix>_bk_sgautobots < migrate-v2.1.sql`
- It is idempotent (checks information_schema first; works on MySQL and MariaDB) and also sets SgAutobots' Car Wash package to Monthly x 10 only while that value is still empty.
- Safety net: the v2.1 engine also adds the two columns itself on first open if the SQL was not run. The Car Wash default then needs the SQL (or the admin sets it in Services).

## Smoke test after deploy (no bookings needed on SgAutobots)
1. https://pageonesingapore.com/preview/sg-autobots/booking/?r=login on a phone: "Create an account" is a full-width button under Log in and opens the Register page.
2. SgAutobots admin > Settings > Services > Car Wash package: "Repeat preselected" = Monthly, "Number of bookings preselected" = 10.
3. The customer Repeat screen can only be reached once SgAutobots has opening hours. Until then it was checked on the local demo client: Car Wash opens Monthly / 10 with the reschedule line, the preview lists 10 monthly dates, and Engine Bay Cleaning shows no repeat choice.
4. Response headers still include `X-Robots-Tag: noindex, nofollow`.

## Tests (off-server, 23 Nov 2026)
Unit 59/59. Migration run twice on the SgAutobots test DB (second run no-op). Chromium at 390 and 360: results above; screenshots in /mnt/project-files/booking-portal/screens-v2.1/.
