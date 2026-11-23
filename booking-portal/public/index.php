<?php
/* Front controller. /booking/<slug>/ (stub folder) or /booking/?c=<slug> for clients; /booking/?r=s for the super-admin. */
declare(strict_types=1);
define('P1B', true);
require __DIR__ . '/app/bootstrap.php';
require __DIR__ . '/app/db.php';
require __DIR__ . '/app/slots.php';
require __DIR__ . '/app/booking.php';
require __DIR__ . '/app/views.php';

$r = preg_replace('/[^a-z_]/', '', (string) ($_GET['r'] ?? ''));
$slug = defined('P1B_SLUG') ? P1B_SLUG : preg_replace('/[^a-z0-9-]/', '', (string) ($_GET['c'] ?? ''));

/* super-admin area */
if ($slug === '' ) {
    if ($r === '' ) { send_headers(null); http_response_code(404); echo '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>' . e(t('not_found')) . '</title>'; exit; }
    if (strpos($r, 's') !== 0) { http_response_code(404); exit; }
    session_open('s');
    require __DIR__ . '/app/super.php';
    super_route($r);
    exit;
}

$client = client_by_slug($slug);
if (!$client) { send_headers(null); http_response_code(404); echo '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><title>' . e(t('not_found')) . '</title><p>' . e(t('not_found')) . '</p>'; exit; }
$T = new Tenant($client);
$area = strpos($r, 'a') === 0 ? 'a' : 'c';

/* iframe: check that the (partitioned) cookie comes back; if not, offer a first-party tab instead */
if (!empty($_GET['embed'])) {
    $cookie = 'p1b' . $area;
    if (!isset($_COOKIE[$cookie]) && !isset($_COOKIE['p1bt'])) {
        if (empty($_GET['ck'])) {
            cookie_header('p1bt', '1', 600);
            $qs = $_GET; $qs['ck'] = 1;
            redirect(strtok($_SERVER['REQUEST_URI'], '?') . '?' . http_build_query($qs));
        }
        send_headers($client);
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
