-- Booking engine schema, ONE client database (MySQL/MariaDB, utf8mb4). Every client has its own database with these 11 tables.
-- The engine also creates them itself on first open (CREATE TABLE IF NOT EXISTS), so this import is optional. Existing v2 databases: run migrate-v2.1.sql instead.
-- Import: mysql --defaults-extra-file=$HOME/booking-clients/<client-slug>/my.cnf <client database> < schema.sql

CREATE TABLE IF NOT EXISTS clients (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, slug VARCHAR(60) NOT NULL UNIQUE, name VARCHAR(120) NOT NULL,
  logo_url VARCHAR(500) NOT NULL DEFAULT '', colour_primary CHAR(7) NOT NULL DEFAULT '#1f4fa0', colour_accent CHAR(7) NOT NULL DEFAULT '#f2c94c',
  colour_bg CHAR(7) NOT NULL DEFAULT '#ffffff', whatsapp_e164 VARCHAR(20) NOT NULL DEFAULT '', timezone VARCHAR(40) NOT NULL DEFAULT 'Asia/Singapore',
  recurring_enabled TINYINT(1) NOT NULL DEFAULT 0, allowed_embed_domains TEXT NULL, status ENUM('setup','live','paused') NOT NULL DEFAULT 'setup',
  slot_step_min SMALLINT UNSIGNED NOT NULL DEFAULT 30, max_days_ahead SMALLINT UNSIGNED NOT NULL DEFAULT 60, min_notice_min INT UNSIGNED NOT NULL DEFAULT 120,
  cancel_cutoff_min INT UNSIGNED NOT NULL DEFAULT 720, capacity TINYINT UNSIGNED NOT NULL DEFAULT 1, max_repeats TINYINT UNSIGNED NOT NULL DEFAULT 12,
  is_test TINYINT(1) NOT NULL DEFAULT 0, created_at DATETIME NOT NULL, updated_at DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS services (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, slug VARCHAR(80) NOT NULL, group_slug VARCHAR(80) NOT NULL DEFAULT '',
  name VARCHAR(160) NOT NULL, description TEXT NOT NULL, duration_min SMALLINT UNSIGNED NULL, full_day TINYINT(1) NOT NULL DEFAULT 0, price DECIMAL(10,2) NULL, price_note VARCHAR(200) NOT NULL DEFAULT '',
  recurring_allowed TINYINT(1) NOT NULL DEFAULT 0, active TINYINT(1) NOT NULL DEFAULT 0, sort_order SMALLINT NOT NULL DEFAULT 0, admin_note VARCHAR(200) NOT NULL DEFAULT '',
  default_freq ENUM('one','weekly','monthly') NOT NULL DEFAULT 'one', default_repeats TINYINT UNSIGNED NULL,
  UNIQUE KEY uq_svc (client_id, slug), KEY k_client (client_id, active, sort_order),
  CONSTRAINT fk_svc_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS weekly_hours (
  client_id INT UNSIGNED NOT NULL, weekday TINYINT UNSIGNED NOT NULL, open_time TIME NULL, close_time TIME NULL, closed TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (client_id, weekday), CONSTRAINT fk_wh_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS off_days (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, start_date DATE NOT NULL, end_date DATE NOT NULL, reason VARCHAR(160) NOT NULL DEFAULT '',
  KEY k_client (client_id, start_date), CONSTRAINT fk_off_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS customers (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, mobile_e164 VARCHAR(20) NOT NULL, name VARCHAR(120) NOT NULL,
  pin_hash VARCHAR(255) NULL, review ENUM('new','approved','flagged') NOT NULL DEFAULT 'new', created_by ENUM('customer','admin') NOT NULL DEFAULT 'customer', must_change_pin TINYINT(1) NOT NULL DEFAULT 0, failed_count TINYINT UNSIGNED NOT NULL DEFAULT 0, locked_until DATETIME NULL,
  is_test TINYINT(1) NOT NULL DEFAULT 0, created_at DATETIME NOT NULL,
  UNIQUE KEY uq_cust (client_id, mobile_e164), CONSTRAINT fk_cust_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS series (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, customer_id INT UNSIGNED NOT NULL, service_id INT UNSIGNED NOT NULL,
  frequency ENUM('weekly','monthly') NOT NULL, count TINYINT UNSIGNED NOT NULL, created_at DATETIME NOT NULL,
  KEY k_client (client_id), CONSTRAINT fk_ser_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS bookings (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, ref VARCHAR(16) NOT NULL UNIQUE, customer_id INT UNSIGNED NOT NULL,
  service_id INT UNSIGNED NOT NULL, start_at DATETIME NOT NULL, end_at DATETIME NOT NULL,
  status ENUM('confirmed','cancelled_customer','cancelled_admin','done','no_show') NOT NULL DEFAULT 'confirmed',
  note VARCHAR(500) NOT NULL DEFAULT '', series_id INT UNSIGNED NULL, created_by ENUM('customer','admin') NOT NULL, is_test TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL, updated_at DATETIME NOT NULL,
  KEY k_time (client_id, start_at), KEY k_cust (client_id, customer_id), KEY k_series (client_id, series_id),
  CONSTRAINT fk_bk_client FOREIGN KEY (client_id) REFERENCES clients(id), CONSTRAINT fk_bk_cust FOREIGN KEY (customer_id) REFERENCES customers(id),
  CONSTRAINT fk_bk_svc FOREIGN KEY (service_id) REFERENCES services(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS admins (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NULL, username VARCHAR(60) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL,
  role ENUM('client_admin','super_admin') NOT NULL, failed_count TINYINT UNSIGNED NOT NULL DEFAULT 0, locked_until DATETIME NULL, created_at DATETIME NOT NULL,
  KEY k_client (client_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS rate_limits (
  scope VARCHAR(24) NOT NULL, key_hash CHAR(64) NOT NULL, window_start DATETIME NOT NULL, hits INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (scope, key_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS audit_log (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NULL, actor VARCHAR(40) NOT NULL, action VARCHAR(40) NOT NULL,
  ref VARCHAR(16) NOT NULL DEFAULT '', detail VARCHAR(200) NOT NULL DEFAULT '', created_at DATETIME NOT NULL, KEY k_client (client_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS meta (k VARCHAR(40) PRIMARY KEY, v VARCHAR(255) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

