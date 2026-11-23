-- Booking engine v2.1 migration (23 Nov 2026): per-service repeat defaults. Idempotent: safe to run more than once. MySQL 5.7+/8 and MariaDB 10.3+.
-- Run on EACH client database, e.g.:
--   mysql --defaults-extra-file=$HOME/booking-clients/sg-autobots/my.cnf <prefix>_bk_sgautobots < migrate-v2.1.sql
-- (The v2.1 engine also adds the two columns by itself on first open; this file makes it explicit and sets the SgAutobots Car Wash default.)

SET @c := (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'services' AND COLUMN_NAME = 'default_freq');
SET @s := IF(@c = 0, 'ALTER TABLE services ADD COLUMN default_freq ENUM(''one'',''weekly'',''monthly'') NOT NULL DEFAULT ''one''', 'DO 0');
PREPARE st FROM @s; EXECUTE st; DEALLOCATE PREPARE st;

SET @c := (SELECT COUNT(*) FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'services' AND COLUMN_NAME = 'default_repeats');
SET @s := IF(@c = 0, 'ALTER TABLE services ADD COLUMN default_repeats TINYINT UNSIGNED NULL', 'DO 0');
PREPARE st FROM @s; EXECUTE st; DEALLOCATE PREPARE st;

-- SgAutobots only: Car Wash package (10 washes) opens on Monthly x 10. Only fills it while unset, so a later admin edit is never overwritten.
-- On any other client database this matches no row (no client 'sg-autobots' there).
UPDATE services s JOIN clients c ON c.id = s.client_id
   SET s.default_freq = 'monthly', s.default_repeats = 10
 WHERE c.slug = 'sg-autobots' AND s.slug = 'car-wash-package' AND s.default_repeats IS NULL;
