<?php
/* Booking portal bootstrap: config, headers, sessions, CSRF, escaping, errors.
   Every request goes through index.php (or a client stub) -> this file. */
declare(strict_types=1);
if (!defined('P1B')) { http_response_code(404); exit; }

const P1B_VERSION = '1.0.0';

/* ---------- config (secrets live ONLY in the private file outside public_html) ---------- */
function cfg(string $k, $default = null) {
    static $c = null;
    if ($c === null) {
        // The client's entry file defines P1B_CONFIG_FILE: that client's own config (own DB) OUTSIDE public_html.
        $p = defined('P1B_CONFIG_FILE') ? P1B_CONFIG_FILE : (string) getenv('P1B_CONFIG');
        if ($p === '' || strpos(str_replace('\\', '/', $p), '/public_html/') !== false || !is_file($p)) {
            throw new RuntimeException('config missing or inside public_html');
        }
        $c = require $p;
        if (!is_array($c)) throw new RuntimeException('config invalid');
    }
    return $c[$k] ?? $default;
}

function base_url(): string { return rtrim((string) cfg('base_url', ''), '/'); }  // e.g. https://pageonesingapore.com/preview/sg-autobots/booking
function base_path(): string { $p = parse_url(base_url(), PHP_URL_PATH); return rtrim($p ?: '/booking', '/'); }
function portal_origin(): string { $u = parse_url(base_url()); return ($u['scheme'] ?? 'https') . '://' . ($u['host'] ?? '') . (isset($u['port']) ? ':' . $u['port'] : ''); }

/* ---------- escaping + text ---------- */
function e($s): string { return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
function lang(): array { static $L = null; return $L ??= require __DIR__ . '/lang/' . preg_replace('/[^a-z]/', '', (string) cfg('lang', 'en')) . '.php'; }
function tl(string $key, array $vars = []): array { return array_map(fn($x) => strtr($x, array_combine(array_map(fn($k) => '{' . $k . '}', array_keys($vars)), array_values($vars)) ?: []), (array) (lang()[$key] ?? [])); }
function t(string $key, array $vars = []): string {
    $s = lang()[$key] ?? $key; if (is_array($s)) return $key;
    foreach ($vars as $k => $v) { $s = str_replace('{' . $k . '}', (string) $v, $s); }
    return $s;
}

/* ---------- privacy helpers ---------- */
function mask_mobile(?string $m): string {
    $m = (string) $m; if (strlen($m) < 8) return '****';
    return substr($m, 0, 3) . '****' . substr($m, -4);
}
function client_ip(): string { return (string) ($_SERVER['REMOTE_ADDR'] ?? '0.0.0.0'); }
function ip_key(): string { return hash_hmac('sha256', client_ip(), (string) cfg('pepper', 'dev-pepper')); }

/* ---------- errors: never show stack traces, never log PII ---------- */
function p1b_log(string $msg): void {
    $msg = preg_replace('/\+?\d{8,15}/', '[num]', $msg);
    error_log('[booking] ' . $msg);
}
set_exception_handler(function (Throwable $ex) {
    p1b_log(get_class($ex) . ' ' . $ex->getMessage() . ' @' . basename($ex->getFile()) . ':' . $ex->getLine());
    if (PHP_SAPI === 'cli') { fwrite(STDERR, (string) $ex . "\n"); exit(1); }
    if (!headers_sent()) { http_response_code(500); header('Content-Type: text/html; charset=utf-8'); }
    echo '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>' . e(t('err_title')) . '</title><p style="font:16px system-ui;padding:24px">' . e(t('err_generic')) . '</p>';
    exit;
});
ini_set('display_errors', '0');
error_reporting(E_ALL);

/* ---------- per-request CSP nonce + headers (sent from PHP, no .htaccess) ---------- */
function nonce(): string { static $n = null; return $n ??= rtrim(strtr(base64_encode(random_bytes(16)), '+/', '-_'), '='); }

function frame_ancestors(?array $client): string {
    $list = ["'self'"];
    if ($client) {
        $doms = (string) ($client['allowed_embed_domains'] ?? '') . ' ' . implode(' ', (array) cfg('embed_domains', []));
        foreach (preg_split('/[\s,]+/', $doms, -1, PREG_SPLIT_NO_EMPTY) as $d) {
            $d = strtolower(trim($d));
            $d = preg_replace('#^https?://#', '', $d); $d = rtrim($d, '/');
            if (preg_match('/^(\*\.)?[a-z0-9-]+(\.[a-z0-9-]+)+(:\d+)?$/', $d)) {
                $list[] = 'https://' . $d;
                if (strpos($d, '*.') !== 0 && strpos($d, 'www.') !== 0) $list[] = 'https://www.' . $d;
            }
        }
        foreach ((array) cfg('extra_frame_ancestors', []) as $x) { $list[] = $x; } // local test only
    }
    return implode(' ', array_unique($list));
}

function send_headers(?array $client): void {
    if (headers_sent()) return;
    header('Content-Type: text/html; charset=utf-8');
    header('X-Robots-Tag: noindex, nofollow', true);
    header('Cache-Control: no-store, private');
    header('X-Content-Type-Options: nosniff');
    header('Referrer-Policy: strict-origin-when-cross-origin');
    header('Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()');
    if (cfg('hsts', true)) header('Strict-Transport-Security: max-age=31536000; includeSubDomains');
    header('Cross-Origin-Opener-Policy: same-origin-allow-popups');
    $n = nonce();
    header("Content-Security-Policy: default-src 'self'; script-src 'self'; style-src 'self' 'nonce-$n'; img-src 'self' https: data:; "
        . "connect-src 'self'; font-src 'self'; form-action 'self'; base-uri 'none'; object-src 'none'; frame-src 'none'; "
        . 'frame-ancestors ' . frame_ancestors($client));
}

/* ---------- sessions: own cookie per area, Secure; HttpOnly; SameSite=None; Partitioned (CHIPS) ---------- */
function cookie_header(string $name, string $value, int $maxAge): void {
    $secure = cfg('cookie_secure', true);
    $parts = [rawurlencode($name) . '=' . rawurlencode($value), 'Path=' . base_path() . '/', 'HttpOnly'];
    if ($maxAge >= 0) $parts[] = 'Max-Age=' . $maxAge;
    if ($secure) { $parts[] = 'Secure'; $parts[] = 'SameSite=None'; $parts[] = 'Partitioned'; } else { $parts[] = 'SameSite=Lax'; }
    header('Set-Cookie: ' . implode('; ', $parts), false);
}

function session_open(string $area): void {   // $area: c (customer) | a (client admin) | s (super-admin)
    if (session_status() === PHP_SESSION_ACTIVE) return;
    $name = 'p1b' . $area;
    ini_set('session.use_cookies', '0');
    ini_set('session.use_only_cookies', '1');
    ini_set('session.use_strict_mode', '1');
    ini_set('session.use_trans_sid', '0');
    ini_set('session.cache_limiter', '');
    ini_set('session.gc_maxlifetime', (string) ($area === 'c' ? 60 * 60 * 24 * 30 : 60 * 60 * 8));
    if ($sp = cfg('session_path')) session_save_path($sp);
    session_name($name);
    $id = $_COOKIE[$name] ?? '';
    if ($id !== '' && preg_match('/^[A-Za-z0-9,-]{22,128}$/', $id)) session_id($id);
    session_start();
    if (session_id() !== $id) cookie_header($name, session_id(), $area === 'c' ? 60 * 60 * 24 * 30 : -1);
    $GLOBALS['P1B_AREA'] = $area;
}
function session_regen(): void {
    session_regenerate_id(true);
    $a = $GLOBALS['P1B_AREA'] ?? 'c';
    cookie_header('p1b' . $a, session_id(), $a === 'c' ? 60 * 60 * 24 * 30 : -1);
    unset($_SESSION['csrf']);
}
function session_end_all(): void {
    $a = $GLOBALS['P1B_AREA'] ?? 'c';
    $_SESSION = []; session_destroy(); cookie_header('p1b' . $a, '', 0);
}

/* ---------- CSRF + Origin check on every POST ---------- */
function csrf_token(): string { return $_SESSION['csrf'] ??= bin2hex(random_bytes(24)); }
function csrf_field(): string { return '<input type="hidden" name="_csrf" value="' . e(csrf_token()) . '">'; }
function is_post(): bool { return ($_SERVER['REQUEST_METHOD'] ?? 'GET') === 'POST'; }
function require_post_ok(): void {
    $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
    if ($origin !== '' && $origin !== 'null' && rtrim($origin, '/') !== portal_origin()) { http_response_code(403); exit('Bad origin'); }
    if ($origin === '' ) { // old browsers: fall back to Referer host
        $ref = $_SERVER['HTTP_REFERER'] ?? '';
        if ($ref !== '' && strpos($ref, portal_origin() . '/') !== 0) { http_response_code(403); exit('Bad origin'); }
    }
    $tok = (string) ($_POST['_csrf'] ?? '');
    if (!isset($_SESSION['csrf']) || !hash_equals($_SESSION['csrf'], $tok)) { http_response_code(403); exit('Form expired. Go back and try again.'); }
}

/* ---------- input helpers ---------- */
function in_str(string $k, int $max = 500): string { return mb_substr(trim((string) ($_POST[$k] ?? $_GET[$k] ?? '')), 0, $max); }
function in_int(string $k): int { return (int) ($_POST[$k] ?? $_GET[$k] ?? 0); }
function q_str(string $k, int $max = 100): string { return mb_substr(trim((string) ($_GET[$k] ?? '')), 0, $max); }

function flash(?string $msg = null, string $kind = 'ok') {
    if ($msg !== null) { $_SESSION['flash'] = [$kind, $msg]; return null; }
    $f = $_SESSION['flash'] ?? null; unset($_SESSION['flash']); return $f;
}

function redirect(string $url): void { header('Location: ' . $url, true, 303); exit; }

/* ---------- phone numbers (SG +65 / MY +60), E.164 ---------- */
function normalise_mobile(string $raw): ?string {
    $d = preg_replace('/[^\d+]/', '', $raw);
    if ($d === '') return null;
    if (cfg('test_mode', false) && preg_match('/^\+?65000000\d\d$/', $d)) return '+' . ltrim($d, '+');
    if ($d[0] === '+') $d = substr($d, 1); elseif (strpos($d, '00') === 0) $d = substr($d, 2);
    if (preg_match('/^[89]\d{7}$/', $d)) $d = '65' . $d;              // local SG mobile
    if (preg_match('/^01\d{8,9}$/', $d)) $d = '6' . $d;                // local MY mobile 01x
    if (preg_match('/^65[89]\d{7}$/', $d)) return '+' . $d;
    if (preg_match('/^601\d{8,9}$/', $d)) return '+' . $d;
    return null;
}
function is_test_mobile(string $e164): bool { return (bool) preg_match('/^\+65000000\d\d$/', $e164); }

function weak_pin(string $pin): bool {
    if (!preg_match('/^\d{6}$/', $pin)) return true;
    if (preg_match('/^(\d)\1{5}$/', $pin)) return true;
    if (strpos('0123456789', $pin) !== false || strpos('9876543210', $pin) !== false) return true;
    if (preg_match('/^(\d\d)\1\1$/', $pin) || preg_match('/^(\d{3})\1$/', $pin)) return true; // 121212, 123123
    if (preg_match('/^(\d)\1(\d)\2(\d)\3$/', $pin)) return true;                                // 112233
    return in_array($pin, ['696969', '159753', '147258', '258369', '520520', '131313', '102030'], true);
}

function wa_link(string $e164, string $text = ''): string {
    return 'https://wa.me/' . ltrim($e164, '+') . ($text !== '' ? '?text=' . rawurlencode($text) : '');
}

/* static files live in the engine (outside the web root) and are served through the client entry: ?asset=css|js|embed */
const P1B_ASSETS = ['css' => ['assets/portal.css', 'text/css'], 'js' => ['assets/portal.js', 'text/javascript'], 'embed' => ['embed.js', 'text/javascript']];
function asset(string $key): string {
    $f = dirname(__DIR__) . '/' . P1B_ASSETS[$key][0];
    return base_path() . '/?asset=' . $key . '&v=' . substr(hash_file('sha256', $f), 0, 10);
}
function serve_asset(string $key): void {
    if (!isset(P1B_ASSETS[$key])) { http_response_code(404); exit; }
    [$file, $type] = P1B_ASSETS[$key];
    header('Content-Type: ' . $type . '; charset=utf-8');
    header('X-Content-Type-Options: nosniff');
    header('X-Robots-Tag: noindex, nofollow');
    header('Access-Control-Allow-Origin: *');            // embed.js is loaded by the client's own site
    header('Cross-Origin-Resource-Policy: cross-origin');
    // versioned (?v=hash) = 1 year immutable (rule 30); embed.js without v = 1 hour
    header('Cache-Control: ' . (isset($_GET['v']) ? 'public, max-age=31536000, immutable' : 'public, max-age=3600'));
    readfile(dirname(__DIR__) . '/' . $file);
    exit;
}
