<?php
/* Booking engine front controller. Lives OUTSIDE the web root (e.g. /home/<account>/booking-engine/engine.php).
   Each client has a 3-line public entry that defines P1B_CONFIG_FILE (that client's own config + own database) and requires this file:
     <client folder>/booking/index.php        customer screens
     <client folder>/booking/admin/index.php  admin screens (defines P1B_ADMIN)
   Static files are served through the entry (?asset=css|js|embed), so nothing of the engine is web-reachable. */
declare(strict_types=1);
define('P1B', true);
require __DIR__ . '/app/bootstrap.php';
require __DIR__ . '/app/db.php';
require __DIR__ . '/app/slots.php';
require __DIR__ . '/app/booking.php';
require __DIR__ . '/app/views.php';

if (isset($_GET['asset'])) serve_asset((string) $_GET['asset']);

$r = preg_replace('/[^a-z_]/', '', (string) ($_GET['r'] ?? ''));
if ($r === '' && defined('P1B_ADMIN')) $r = 'a';
$slug = (string) cfg('client_slug', '');

migrate();   // CREATE TABLE IF NOT EXISTS: a no-op once the schema is in
$client = client_by_slug($slug);
$area = strpos($r, 'a') === 0 ? 'a' : 'c';

if (!$client) {
    // first run of a new client database: only the admin setup (token from the private config) can create the client row
    session_open('a');
    require __DIR__ . '/app/admin.php';
    a_setup(null);
    exit;
}
$T = new Tenant($client);

/* iframe: check that the (partitioned) cookie comes back; if not, offer a first-party tab instead */
if (!empty($_GET['embed'])) {
    $cookie = 'p1b' . $area;
    if (!isset($_COOKIE[$cookie]) && !isset($_COOKIE['p1bt'])) {
        if (empty($_GET['ck'])) {
            cookie_header('p1bt', '1', 600);
            $qs = $_GET; $qs['ck'] = 1;
            redirect(strtok($_SERVER['REQUEST_URI'], '?') . '?' . http_build_query($qs));
        }
        $qs = $_GET; unset($qs['embed'], $qs['ck']);
        $url = curl_($slug, (string) ($qs['r'] ?? ''), array_diff_key($qs, ['r' => 1]));
        page(['client' => $client, 'title' => t('book_title'), 'area' => $area,
              'body' => '<div class="card center" data-nocookie="' . e($slug) . '"><p>' . e(t('cookie_blocked')) . '</p><a class="btn big" href="' . e($url) . '" target="_blank" rel="noopener">' . e(t('cookie_open')) . '</a></div>']);
        exit;
    }
}

session_open($area);
if (!empty($_GET['embed'])) $_SESSION['embed'] = 1;
elseif (isset($_GET['top'])) unset($_SESSION['embed']);

if ($area === 'a') { require __DIR__ . '/app/admin.php'; admin_route($T, $r); }
else { require __DIR__ . '/app/customer.php'; customer_route($T, $r); }
