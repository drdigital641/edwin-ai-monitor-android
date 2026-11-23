# Booking engine (booking-portal)

One shared booking engine (PHP 8.1+, MySQL/MariaDB) for many clients. **v2 layout (Edwin 23 Nov 2026, 8:54pm SGT):** the engine lives outside the web root, each client has a thin public entry folder on its own site, and its OWN config + OWN database outside public_html. Nothing is served at pageonesingapore.com/booking/.
White-label: no agency name in the UI. Not for search engines (noindex meta + X-Robots-Tag on every response).

Deploy, smoke tests, domain move, backups: **deploy/DEPLOY.md**.

## Layout
```
engine/                     -> /home/<account>/booking-engine/          (not web-reachable)
  engine.php                front controller; assets served through the entry (?asset=css|js|embed)
  embed.js, assets/         Book popup + inline iframe height; the only CSS and JS
  app/bootstrap.php         config (P1B_CONFIG_FILE, refuses public_html), headers, CHIPS sessions, CSRF
  app/db.php                schema + the ONE tenant-scoped data layer (class Tenant)
  app/slots.php             the ONE slot engine
  app/booking.php           book / series / reschedule / cancel under SELECT ... FOR UPDATE
  app/views.php, customer.php, admin.php (incl. first-run setup by token + seed import)
  app/lang/en.php, app/seed/sg-autobots.json
entry/booking/index.php       -> <client site>/booking/index.php        (3 lines: config path + require engine)
entry/booking/admin/index.php -> <client site>/booking/admin/index.php
private/                      -> /home/<account>/booking-clients/<slug>/ (config.php, my.cnf, sessions/) + backup.sh
deploy/schema.sql             one client database (11 tables)
tests/run_tests.php, concurrency.php   (P1B_CONFIG=<test config>)
tests/e2e/v2.js, v2_demo_hours.php     local browser test, two client databases
```

## Tests
```
P1B_CONFIG=/path/test/config.php php tests/run_tests.php      # 59 checks
P1B_CONFIG=/path/test/config.php php tests/concurrency.php    # 25 races, 0 double bookings
node tests/e2e/v2.js                                          # local HTTPS test hosts portal.test / clientsite.test
```
