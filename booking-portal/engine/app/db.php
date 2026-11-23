<?php
/* One data-access layer. Tenant-scoped queries live ONLY in class Tenant, whose client_id is fixed at
   construction from the authenticated session (or the URL slug before login). No method takes a client_id. */
declare(strict_types=1);
if (!defined('P1B')) { http_response_code(404); exit; }

function db(): PDO {
    static $pdo = null;
    if ($pdo) return $pdo;
    $dsn = cfg('db_dsn') ?: ('mysql:host=' . cfg('db_host', 'localhost') . ';dbname=' . cfg('db_name') . ';charset=utf8mb4');
    $pdo = new PDO($dsn, (string) cfg('db_user'), (string) cfg('db_pass'), [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        PDO::ATTR_EMULATE_PREPARES => false,
        PDO::ATTR_STRINGIFY_FETCHES => false,
    ]);
    $pdo->exec("SET time_zone = '+00:00'");
    return $pdo;
}
function db_reset(): void { /* tests only */ }

function q(string $sql, array $p = []): PDOStatement { $s = db()->prepare($sql); $s->execute($p); return $s; }
function utc_now(): string { return gmdate('Y-m-d H:i:s'); }

const P1B_SCHEMA = [
"CREATE TABLE IF NOT EXISTS clients (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, slug VARCHAR(60) NOT NULL UNIQUE, name VARCHAR(120) NOT NULL,
  logo_url VARCHAR(500) NOT NULL DEFAULT '', colour_primary CHAR(7) NOT NULL DEFAULT '#1f4fa0', colour_accent CHAR(7) NOT NULL DEFAULT '#f2c94c',
  colour_bg CHAR(7) NOT NULL DEFAULT '#ffffff', whatsapp_e164 VARCHAR(20) NOT NULL DEFAULT '', timezone VARCHAR(40) NOT NULL DEFAULT 'Asia/Singapore',
  recurring_enabled TINYINT(1) NOT NULL DEFAULT 0, allowed_embed_domains TEXT NULL, status ENUM('setup','live','paused') NOT NULL DEFAULT 'setup',
  slot_step_min SMALLINT UNSIGNED NOT NULL DEFAULT 30, max_days_ahead SMALLINT UNSIGNED NOT NULL DEFAULT 60, min_notice_min INT UNSIGNED NOT NULL DEFAULT 120,
  cancel_cutoff_min INT UNSIGNED NOT NULL DEFAULT 720, capacity TINYINT UNSIGNED NOT NULL DEFAULT 1, max_repeats TINYINT UNSIGNED NOT NULL DEFAULT 12,
  is_test TINYINT(1) NOT NULL DEFAULT 0, created_at DATETIME NOT NULL, updated_at DATETIME NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS services (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, slug VARCHAR(80) NOT NULL, group_slug VARCHAR(80) NOT NULL DEFAULT '',
  name VARCHAR(160) NOT NULL, description TEXT NOT NULL, duration_min SMALLINT UNSIGNED NULL, full_day TINYINT(1) NOT NULL DEFAULT 0, price DECIMAL(10,2) NULL, price_note VARCHAR(200) NOT NULL DEFAULT '',
  recurring_allowed TINYINT(1) NOT NULL DEFAULT 0, active TINYINT(1) NOT NULL DEFAULT 0, sort_order SMALLINT NOT NULL DEFAULT 0, admin_note VARCHAR(200) NOT NULL DEFAULT '',
  default_freq ENUM('one','weekly','monthly') NOT NULL DEFAULT 'one', default_repeats TINYINT UNSIGNED NULL,
  UNIQUE KEY uq_svc (client_id, slug), KEY k_client (client_id, active, sort_order),
  CONSTRAINT fk_svc_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS weekly_hours (
  client_id INT UNSIGNED NOT NULL, weekday TINYINT UNSIGNED NOT NULL, open_time TIME NULL, close_time TIME NULL, closed TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (client_id, weekday), CONSTRAINT fk_wh_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS off_days (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, start_date DATE NOT NULL, end_date DATE NOT NULL, reason VARCHAR(160) NOT NULL DEFAULT '',
  KEY k_client (client_id, start_date), CONSTRAINT fk_off_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS customers (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, mobile_e164 VARCHAR(20) NOT NULL, name VARCHAR(120) NOT NULL,
  pin_hash VARCHAR(255) NULL, review ENUM('new','approved','flagged') NOT NULL DEFAULT 'new', created_by ENUM('customer','admin') NOT NULL DEFAULT 'customer', must_change_pin TINYINT(1) NOT NULL DEFAULT 0, failed_count TINYINT UNSIGNED NOT NULL DEFAULT 0, locked_until DATETIME NULL,
  is_test TINYINT(1) NOT NULL DEFAULT 0, created_at DATETIME NOT NULL,
  UNIQUE KEY uq_cust (client_id, mobile_e164), CONSTRAINT fk_cust_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS series (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, customer_id INT UNSIGNED NOT NULL, service_id INT UNSIGNED NOT NULL,
  frequency ENUM('weekly','monthly') NOT NULL, count TINYINT UNSIGNED NOT NULL, created_at DATETIME NOT NULL,
  KEY k_client (client_id), CONSTRAINT fk_ser_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS bookings (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NOT NULL, ref VARCHAR(16) NOT NULL UNIQUE, customer_id INT UNSIGNED NOT NULL,
  service_id INT UNSIGNED NOT NULL, start_at DATETIME NOT NULL, end_at DATETIME NOT NULL,
  status ENUM('confirmed','cancelled_customer','cancelled_admin','done','no_show') NOT NULL DEFAULT 'confirmed',
  note VARCHAR(500) NOT NULL DEFAULT '', series_id INT UNSIGNED NULL, created_by ENUM('customer','admin') NOT NULL, is_test TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL, updated_at DATETIME NOT NULL,
  KEY k_time (client_id, start_at), KEY k_cust (client_id, customer_id), KEY k_series (client_id, series_id),
  CONSTRAINT fk_bk_client FOREIGN KEY (client_id) REFERENCES clients(id), CONSTRAINT fk_bk_cust FOREIGN KEY (customer_id) REFERENCES customers(id),
  CONSTRAINT fk_bk_svc FOREIGN KEY (service_id) REFERENCES services(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS admins (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NULL, username VARCHAR(60) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL,
  role ENUM('client_admin','super_admin') NOT NULL, failed_count TINYINT UNSIGNED NOT NULL DEFAULT 0, locked_until DATETIME NULL, created_at DATETIME NOT NULL,
  KEY k_client (client_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS rate_limits (
  scope VARCHAR(24) NOT NULL, key_hash CHAR(64) NOT NULL, window_start DATETIME NOT NULL, hits INT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (scope, key_hash)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS audit_log (
  id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY, client_id INT UNSIGNED NULL, actor VARCHAR(40) NOT NULL, action VARCHAR(40) NOT NULL,
  ref VARCHAR(16) NOT NULL DEFAULT '', detail VARCHAR(200) NOT NULL DEFAULT '', created_at DATETIME NOT NULL, KEY k_client (client_id, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
"CREATE TABLE IF NOT EXISTS meta (k VARCHAR(40) PRIMARY KEY, v VARCHAR(255) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4",
];

function migrate(): void {
    foreach (P1B_SCHEMA as $sql) db()->exec($sql);
    // v2.1: per-service repeat defaults (idempotent, MySQL + MariaDB); same change as deploy/migrate-v2.1.sql
    $have = q("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='services' AND COLUMN_NAME IN ('default_freq','default_repeats')")->fetchAll(PDO::FETCH_COLUMN);
    if (!in_array('default_freq', $have, true)) db()->exec("ALTER TABLE services ADD COLUMN default_freq ENUM('one','weekly','monthly') NOT NULL DEFAULT 'one'");
    if (!in_array('default_repeats', $have, true)) db()->exec('ALTER TABLE services ADD COLUMN default_repeats TINYINT UNSIGNED NULL');
}
/** per-service repeat defaults: preselected Repeat choice and Number of bookings when the customer picks the service */
function svc_freq(array $s): string { $f = (string) ($s['default_freq'] ?? 'one'); return in_array($f, ['one', 'weekly', 'monthly'], true) ? $f : 'one'; }
function svc_reps(array $s): ?int { $n = (int) ($s['default_repeats'] ?? 0); return $n >= 2 ? min($n, 52) : null; }
function meta_get(string $k): ?string { $r = q('SELECT v FROM meta WHERE k=?', [$k])->fetchColumn(); return $r === false ? null : (string) $r; }
function meta_set(string $k, string $v): void { q('INSERT INTO meta (k,v) VALUES (?,?) ON DUPLICATE KEY UPDATE v=VALUES(v)', [$k, $v]); }

/* ---------- audit (no PIN, password, full mobile or note text) ---------- */
function audit(?int $clientId, string $actor, string $action, string $ref = '', string $detail = ''): void {
    $detail = preg_replace('/\+?\d{8,15}/', '[num]', $detail);
    q('INSERT INTO audit_log (client_id, actor, action, ref, detail, created_at) VALUES (?,?,?,?,?,?)',
      [$clientId, mb_substr($actor, 0, 40), $action, $ref, mb_substr($detail, 0, 200), utc_now()]);
}

/* ---------- rate limit by IP + scope (fixed window) ---------- */
function rate_hit(string $scope, int $limit, int $windowSec, ?string $key = null): bool {   // true = allowed
    $key = $key ?? ip_key();
    $now = time();
    $row = q('SELECT window_start, hits FROM rate_limits WHERE scope=? AND key_hash=?', [$scope, $key])->fetch();
    if (!$row || strtotime($row['window_start'] . ' UTC') + $windowSec <= $now) {
        q('INSERT INTO rate_limits (scope,key_hash,window_start,hits) VALUES (?,?,?,1) ON DUPLICATE KEY UPDATE window_start=VALUES(window_start), hits=1',
          [$scope, $key, gmdate('Y-m-d H:i:s', $now)]);
        return true;
    }
    if ((int) $row['hits'] >= $limit) return false;
    q('UPDATE rate_limits SET hits=hits+1 WHERE scope=? AND key_hash=?', [$scope, $key]);
    return true;
}
function rate_blocked(string $scope, int $limit, int $windowSec): bool {
    $row = q('SELECT window_start, hits FROM rate_limits WHERE scope=? AND key_hash=?', [$scope, ip_key()])->fetch();
    return $row && strtotime($row['window_start'] . ' UTC') + $windowSec > time() && (int) $row['hits'] >= $limit;
}

/* ---------- client lookup (public, by slug) ---------- */
function client_by_slug(string $slug): ?array {
    if (!preg_match('/^[a-z0-9][a-z0-9-]{1,59}$/', $slug)) return null;
    $r = q('SELECT * FROM clients WHERE slug=?', [$slug])->fetch();
    return $r ?: null;
}

function new_ref(string $slug): string {
    $prefix = strtoupper(substr(preg_replace('/[^a-z]/', '', str_replace('-', '', $slug)) ?: 'BKG', 0, 3));
    $alpha = '23456789ABCDEFGHJKMNPQRSTUVWXYZ';
    for ($try = 0; $try < 10; $try++) {
        $s = ''; for ($i = 0; $i < 6; $i++) $s .= $alpha[random_int(0, strlen($alpha) - 1)];
        $ref = $prefix . '-' . $s;
        if (!q('SELECT 1 FROM bookings WHERE ref=?', [$ref])->fetchColumn()) return $ref;
    }
    throw new RuntimeException('ref space');
}

/* =====================================================================================
   Tenant: the ONLY way to touch tenant rows. client_id is private and fixed.
   ===================================================================================== */
final class Tenant {
    private int $cid;
    public array $client;
    public function __construct(array $client) { $this->cid = (int) $client['id']; $this->client = $client; }
    public function id(): int { return $this->cid; }

    /* -- client settings -- */
    public function reload(): void { $this->client = q('SELECT * FROM clients WHERE id=?', [$this->cid])->fetch(); }
    public function setStatus_(string $st): void { q('UPDATE clients SET status=?, updated_at=? WHERE id=?', [$st, utc_now(), $this->cid]); $this->reload(); }
    public function updateRules(array $r): void {
        q('UPDATE clients SET slot_step_min=?, max_days_ahead=?, min_notice_min=?, cancel_cutoff_min=?, capacity=?, max_repeats=?, updated_at=? WHERE id=?',
          [$r['slot_step_min'], $r['max_days_ahead'], $r['min_notice_min'], $r['cancel_cutoff_min'], $r['capacity'], $r['max_repeats'], utc_now(), $this->cid]);
        $this->reload();
    }
    public function updateBranding(array $b): void {
        q('UPDATE clients SET name=?, logo_url=?, colour_primary=?, colour_accent=?, colour_bg=?, whatsapp_e164=?, updated_at=? WHERE id=?',
          [$b['name'], $b['logo_url'], $b['colour_primary'], $b['colour_accent'], $b['colour_bg'], $b['whatsapp_e164'], utc_now(), $this->cid]);
        $this->reload();
    }

    /* -- services -- */
    public function services(bool $activeOnly = true): array {
        return q('SELECT * FROM services WHERE client_id=?' . ($activeOnly ? ' AND active=1' : '') . ' ORDER BY sort_order, id', [$this->cid])->fetchAll();
    }
    public function service(int $id): ?array { $r = q('SELECT * FROM services WHERE client_id=? AND id=?', [$this->cid, $id])->fetch(); return $r ?: null; }
    public function saveService(array $s): int {
        if (!empty($s['id'])) {
            q('UPDATE services SET name=?, description=?, duration_min=?, full_day=?, price=?, price_note=?, recurring_allowed=?, active=?, sort_order=?, group_slug=?, default_freq=?, default_repeats=? WHERE client_id=? AND id=?',
              [$s['name'], $s['description'], $s['duration_min'], $s['full_day'] ?? 0, $s['price'], $s['price_note'], $s['recurring_allowed'], $s['active'], $s['sort_order'], $s['group_slug'], svc_freq($s), svc_reps($s), $this->cid, (int) $s['id']]);
            return (int) $s['id'];
        }
        $slug = $s['slug'] ?: (trim(preg_replace('/[^a-z0-9]+/', '-', strtolower($s['name'])), '-') ?: 'service');
        $base = $slug; $n = 2;
        while (q('SELECT 1 FROM services WHERE client_id=? AND slug=?', [$this->cid, $slug])->fetchColumn()) $slug = $base . '-' . $n++;
        q('INSERT INTO services (client_id, slug, group_slug, name, description, duration_min, full_day, price, price_note, recurring_allowed, active, sort_order, admin_note, default_freq, default_repeats) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
          [$this->cid, $slug, $s['group_slug'] ?? '', $s['name'], $s['description'], $s['duration_min'], $s['full_day'] ?? 0, $s['price'], $s['price_note'], $s['recurring_allowed'], $s['active'], $s['sort_order'], $s['admin_note'] ?? '', svc_freq($s), svc_reps($s)]);
        return (int) db()->lastInsertId();
    }

    /* -- hours + off days -- */
    public function hours(): array {   // weekday 1..7 (ISO, Mon=1) => row
        $out = [];
        foreach (q('SELECT weekday, open_time, close_time, closed FROM weekly_hours WHERE client_id=?', [$this->cid])->fetchAll() as $r) $out[(int) $r['weekday']] = $r;
        return $out;
    }
    public function saveHours(array $rows): void {
        foreach ($rows as $wd => $r) {
            q('INSERT INTO weekly_hours (client_id, weekday, open_time, close_time, closed) VALUES (?,?,?,?,?) ON DUPLICATE KEY UPDATE open_time=VALUES(open_time), close_time=VALUES(close_time), closed=VALUES(closed)',
              [$this->cid, (int) $wd, $r['open_time'], $r['close_time'], $r['closed'] ? 1 : 0]);
        }
    }
    public function offDays(?string $fromDate = null): array {
        return q('SELECT * FROM off_days WHERE client_id=?' . ($fromDate ? ' AND end_date>=?' : '') . ' ORDER BY start_date', $fromDate ? [$this->cid, $fromDate] : [$this->cid])->fetchAll();
    }
    public function addOffDay(string $s, string $e, string $reason): void {
        q('INSERT INTO off_days (client_id, start_date, end_date, reason) VALUES (?,?,?,?)', [$this->cid, $s, $e, $reason]);
    }
    public function removeOffDay(int $id): void { q('DELETE FROM off_days WHERE client_id=? AND id=?', [$this->cid, $id]); }

    /* -- customers -- */
    public function customerByMobile(string $e164): ?array { $r = q('SELECT * FROM customers WHERE client_id=? AND mobile_e164=?', [$this->cid, $e164])->fetch(); return $r ?: null; }
    public function customer(int $id): ?array { $r = q('SELECT * FROM customers WHERE client_id=? AND id=?', [$this->cid, $id])->fetch(); return $r ?: null; }
    /** $pin null = admin-created, unclaimed: the customer claims it by registering with the same mobile */
    public function createCustomer(string $e164, string $name, ?string $pin, string $by = 'customer'): int {
        q('INSERT INTO customers (client_id, mobile_e164, name, pin_hash, review, created_by, must_change_pin, is_test, created_at) VALUES (?,?,?,?,?,?,0,?,?)',
          [$this->cid, $e164, $name, $pin === null ? null : password_hash($pin, PASSWORD_DEFAULT), $by === 'admin' ? 'approved' : 'new', $by, is_test_mobile($e164) ? 1 : 0, utc_now()]);
        return (int) db()->lastInsertId();
    }
    /** claim an unclaimed (admin-created or PIN-reset) account; true if claimed */
    public function claim(int $customerId, string $name, string $pin): bool {
        return q('UPDATE customers SET pin_hash=?, name=?, must_change_pin=0, failed_count=0, locked_until=NULL WHERE client_id=? AND id=? AND pin_hash IS NULL',
          [password_hash($pin, PASSWORD_DEFAULT), $name, $this->cid, $customerId])->rowCount() === 1;
    }
    public function setReview(int $customerId, string $review): void {
        if (!in_array($review, ['new', 'approved', 'flagged'], true)) throw new InvalidArgumentException('review');
        q('UPDATE customers SET review=? WHERE client_id=? AND id=?', [$review, $this->cid, $customerId]);
    }
    public function newRegistrations(): array {
        return q("SELECT * FROM customers WHERE client_id=? AND review='new' AND created_by='customer' ORDER BY created_at DESC LIMIT 100", [$this->cid])->fetchAll();
    }
    public function setPin(int $customerId, string $pin): void {
        q('UPDATE customers SET pin_hash=?, must_change_pin=0, failed_count=0, locked_until=NULL WHERE client_id=? AND id=?',
          [password_hash($pin, PASSWORD_DEFAULT), $this->cid, $customerId]);
    }
    /** admin reset: clears the PIN so the customer sets a new one by re-registering (claim) with the same mobile */
    public function resetPin(int $customerId): void {
        q('UPDATE customers SET pin_hash=NULL, failed_count=0, locked_until=NULL WHERE client_id=? AND id=?', [$this->cid, $customerId]);
    }
    public function loginFail(int $customerId): void {
        q('UPDATE customers SET failed_count=failed_count+1 WHERE client_id=? AND id=?', [$this->cid, $customerId]);
        q('UPDATE customers SET locked_until=?, failed_count=0 WHERE client_id=? AND id=? AND failed_count>=5', [gmdate('Y-m-d H:i:s', time() + 900), $this->cid, $customerId]);
    }
    public function loginOk(int $customerId): void { q('UPDATE customers SET failed_count=0, locked_until=NULL WHERE client_id=? AND id=?', [$this->cid, $customerId]); }
    public function searchCustomers(string $digits): array {
        $digits = preg_replace('/\D/', '', $digits);
        if ($digits === '') return q('SELECT * FROM customers WHERE client_id=? ORDER BY created_at DESC LIMIT 50', [$this->cid])->fetchAll();
        return q('SELECT * FROM customers WHERE client_id=? AND mobile_e164 LIKE ? ORDER BY created_at DESC LIMIT 50', [$this->cid, '%' . $digits . '%'])->fetchAll();
    }

    /* -- bookings -- */
    private const BK = 'SELECT b.*, s.name AS service_name, s.duration_min, s.price, s.price_note, c.name AS customer_name, c.mobile_e164
        FROM bookings b JOIN services s ON s.id=b.service_id AND s.client_id=b.client_id JOIN customers c ON c.id=b.customer_id AND c.client_id=b.client_id ';
    public function booking(int $id): ?array { $r = q(self::BK . 'WHERE b.client_id=? AND b.id=?', [$this->cid, $id])->fetch(); return $r ?: null; }
    public function bookingByRef(string $ref): ?array { $r = q(self::BK . 'WHERE b.client_id=? AND b.ref=?', [$this->cid, $ref])->fetch(); return $r ?: null; }
    public function customerBooking(int $customerId, string $ref): ?array {
        $r = q(self::BK . 'WHERE b.client_id=? AND b.customer_id=? AND b.ref=?', [$this->cid, $customerId, $ref])->fetch(); return $r ?: null;
    }
    public function bookingsBetween(string $fromUtc, string $toUtc, bool $includeTest = false): array {
        $includeTest = $includeTest || !empty($this->client['is_test']);   // test bookings show only on test clients
        return q(self::BK . 'WHERE b.client_id=? AND b.start_at>=? AND b.start_at<?' . ($includeTest ? '' : ' AND b.is_test=0') . ' ORDER BY b.start_at', [$this->cid, $fromUtc, $toUtc])->fetchAll();
    }
    public function customerBookings(int $customerId): array {
        return q(self::BK . 'WHERE b.client_id=? AND b.customer_id=? ORDER BY b.start_at DESC LIMIT 200', [$this->cid, $customerId])->fetchAll();
    }
    public function seriesBookings(int $seriesId, ?string $fromUtc = null): array {
        return q(self::BK . 'WHERE b.client_id=? AND b.series_id=?' . ($fromUtc ? ' AND b.start_at>=?' : '') . ' ORDER BY b.start_at', $fromUtc ? [$this->cid, $seriesId, $fromUtc] : [$this->cid, $seriesId])->fetchAll();
    }
    /** confirmed bookings overlapping [from,to) as [startTs, endTs, id] */
    public function busy(int $fromTs, int $toTs, int $excludeId = 0): array {
        $rows = q("SELECT id, start_at, end_at FROM bookings WHERE client_id=? AND status='confirmed' AND start_at<? AND end_at>? AND id<>?",
                  [$this->cid, gmdate('Y-m-d H:i:s', $toTs), gmdate('Y-m-d H:i:s', $fromTs), $excludeId])->fetchAll();
        return array_map(fn($r) => [strtotime($r['start_at'] . ' UTC'), strtotime($r['end_at'] . ' UTC'), (int) $r['id']], $rows);
    }
    public function createSeries(int $customerId, int $serviceId, string $freq, int $count): int {
        q('INSERT INTO series (client_id, customer_id, service_id, frequency, count, created_at) VALUES (?,?,?,?,?,?)', [$this->cid, $customerId, $serviceId, $freq, $count, utc_now()]);
        return (int) db()->lastInsertId();
    }
    public function insertBooking(int $customerId, int $serviceId, int $startTs, int $endTs, string $note, ?int $seriesId, string $by, bool $isTest): string {
        $ref = new_ref($this->client['slug']);
        q('INSERT INTO bookings (client_id, ref, customer_id, service_id, start_at, end_at, status, note, series_id, created_by, is_test, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',
          [$this->cid, $ref, $customerId, $serviceId, gmdate('Y-m-d H:i:s', $startTs), gmdate('Y-m-d H:i:s', $endTs), 'confirmed', $note, $seriesId, $by, $isTest ? 1 : 0, utc_now(), utc_now()]);
        return $ref;
    }
    public function moveBooking(int $id, int $startTs, int $endTs): void {
        q("UPDATE bookings SET start_at=?, end_at=?, updated_at=? WHERE client_id=? AND id=? AND status='confirmed'",
          [gmdate('Y-m-d H:i:s', $startTs), gmdate('Y-m-d H:i:s', $endTs), utc_now(), $this->cid, $id]);
    }
    public function setStatus(int $id, string $status): void {
        if (!in_array($status, ['confirmed', 'cancelled_customer', 'cancelled_admin', 'done', 'no_show'], true)) throw new InvalidArgumentException('status');
        q('UPDATE bookings SET status=?, updated_at=? WHERE client_id=? AND id=?', [$status, utc_now(), $this->cid, $id]);
    }
    public function hideTestBookings(): int {   // after tests: test bookings never show as confirmed
        return q("UPDATE bookings SET status='cancelled_admin', updated_at=? WHERE client_id=? AND is_test=1 AND status='confirmed'", [utc_now(), $this->cid])->rowCount();
    }

    /* -- admins of THIS client -- */
    public function adminByUsername(string $u): ?array {
        $r = q("SELECT * FROM admins WHERE client_id=? AND username=? AND role='client_admin'", [$this->cid, $u])->fetch(); return $r ?: null;
    }

    /* -- the booking lock: serialises every write that can change availability for this client -- */
    public function withLock(callable $fn) {
        $pdo = db();
        $pdo->beginTransaction();
        try {
            q('SELECT id FROM clients WHERE id=? FOR UPDATE', [$this->cid]);
            $res = $fn();
            $pdo->commit();
            return $res;
        } catch (Throwable $e) { if ($pdo->inTransaction()) $pdo->rollBack(); throw $e; }
    }
}

/* ---------- super-admin repository (clients + admins only) ---------- */
final class SuperRepo {
    public static function clients(): array { return q('SELECT * FROM clients ORDER BY is_test, name')->fetchAll(); }
    public static function client(int $id): ?array { $r = q('SELECT * FROM clients WHERE id=?', [$id])->fetch(); return $r ?: null; }
    public static function saveClient(array $c): int {
        $cols = ['slug', 'name', 'logo_url', 'colour_primary', 'colour_accent', 'colour_bg', 'whatsapp_e164', 'timezone', 'recurring_enabled', 'allowed_embed_domains', 'status', 'is_test'];
        $vals = array_map(fn($k) => $c[$k] ?? null, $cols);
        if (!empty($c['id'])) {
            $set = implode(',', array_map(fn($k) => "$k=?", array_slice($cols, 1)));
            q("UPDATE clients SET $set, updated_at=? WHERE id=?", array_merge(array_slice($vals, 1), [utc_now(), (int) $c['id']]));
            return (int) $c['id'];
        }
        q('INSERT INTO clients (' . implode(',', $cols) . ',created_at,updated_at) VALUES (' . rtrim(str_repeat('?,', count($cols)), ',') . ',?,?)', array_merge($vals, [utc_now(), utc_now()]));
        return (int) db()->lastInsertId();
    }
    public static function clientAdmins(int $clientId): array { return q("SELECT id, username, failed_count, locked_until, created_at FROM admins WHERE client_id=? AND role='client_admin'", [$clientId])->fetchAll(); }
    public static function upsertClientAdmin(int $clientId, string $username, string $password): void {
        $h = password_hash($password, PASSWORD_DEFAULT);
        $ex = q('SELECT id, client_id, role FROM admins WHERE username=?', [$username])->fetch();
        if ($ex) {
            if ((int) $ex['client_id'] !== $clientId || $ex['role'] !== 'client_admin') throw new DomainException('username_taken');
            q('UPDATE admins SET password_hash=?, failed_count=0, locked_until=NULL WHERE id=?', [$h, $ex['id']]);
        } else {
            q("INSERT INTO admins (client_id, username, password_hash, role, created_at) VALUES (?,?,?,'client_admin',?)", [$clientId, $username, $h, utc_now()]);
        }
    }
    public static function superByUsername(string $u): ?array { $r = q("SELECT * FROM admins WHERE role='super_admin' AND client_id IS NULL AND username=?", [$u])->fetch(); return $r ?: null; }
    public static function superExists(): bool { return (bool) q("SELECT 1 FROM admins WHERE role='super_admin' LIMIT 1")->fetchColumn(); }
    public static function createSuper(string $u, string $p): void {
        q("INSERT INTO admins (client_id, username, password_hash, role, created_at) VALUES (NULL,?,?,'super_admin',?)", [$u, password_hash($p, PASSWORD_DEFAULT), utc_now()]);
    }
}

/* admin login bookkeeping (works for both roles; row id comes from a scoped lookup above) */
function admin_fail(int $adminId): void {
    q('UPDATE admins SET failed_count=failed_count+1 WHERE id=?', [$adminId]);
    q('UPDATE admins SET locked_until=?, failed_count=0 WHERE id=? AND failed_count>=5', [gmdate('Y-m-d H:i:s', time() + 900), $adminId]);
}
function admin_ok(int $adminId): void { q('UPDATE admins SET failed_count=0, locked_until=NULL WHERE id=?', [$adminId]); }
function is_locked(?string $lockedUntil): bool { return $lockedUntil !== null && strtotime($lockedUntil . ' UTC') > time(); }
