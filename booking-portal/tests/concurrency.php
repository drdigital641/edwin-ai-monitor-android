<?php
/* Concurrency test: 2 processes book the SAME slot at the same instant, N runs, capacity 1.
   Usage: php tests/concurrency.php [runs]   (worker mode: php tests/concurrency.php worker <client_id> <cust_id> <svc_id> <start> <go_at>) */
declare(strict_types=1);
define('P1B', true);
$root = dirname(__DIR__) . '/engine';
foreach (['bootstrap', 'db', 'slots', 'booking'] as $f) require "$root/app/$f.php";
if (!cfg('test_mode')) exit(2);
if (($argv[1] ?? '') === 'worker') {
    [, , $cid, $cust, $svc, $start, $go] = $argv;
    $T = new Tenant(SuperRepo::client((int) $cid));
    $s = $T->service((int) $svc);
    db();                                             // connect before the barrier
    while (microtime(true) < (float) $go) usleep(200);
    try { echo book_one($T, $s, (int) $cust, (int) $start, '', 'customer', [], null, true); } catch (DomainException $e) { echo 'REFUSED:' . $e->getMessage(); }
    exit;
}
$runs = (int) ($argv[1] ?? 25);
migrate();
$T = new Tenant(client_by_slug('test-a'));
$svc = $T->services()[0];
$c1 = $T->customerByMobile('+6500000011') ?? $T->customer($T->createCustomer('+6500000011', 'Racer 1', '480317'));
$c2 = $T->customerByMobile('+6500000012') ?? $T->customer($T->createCustomer('+6500000012', 'Racer 2', '480317'));
$base = (new DateTimeImmutable('today 09:00', new DateTimeZone('Asia/Singapore')))->modify('+20 day')->getTimestamp();
$double = 0; $single = 0; $rows = [];
for ($i = 0; $i < $runs; $i++) {
    $start = $base + $i * 7200;
    $go = sprintf('%.6f', microtime(true) + 0.35);
    $p = [];
    foreach ([$c1, $c2] as $c) $p[] = proc_open([PHP_BINARY, __FILE__, 'worker', (string) $T->id(), (string) $c['id'], (string) $svc['id'], (string) $start, $go], [1 => ['pipe', 'w'], 2 => ['pipe', 'w']], $pipes[$c['id']]);
    $out = [];
    foreach ([$c1, $c2] as $k => $c) { $out[] = trim(stream_get_contents($pipes[$c['id']][1])); proc_close($p[$k]); }
    $n = (int) q("SELECT COUNT(*) FROM bookings WHERE client_id=? AND start_at=? AND status='confirmed'", [$T->id(), gmdate('Y-m-d H:i:s', $start)])->fetchColumn();
    if ($n > 1) $double++; elseif ($n === 1) $single++;
    $rows[] = sprintf('run %2d: %s | %s => confirmed %d', $i + 1, $out[0], $out[1], $n);
}
echo implode("\n", $rows), "\n\nRuns: $runs, exactly one confirmed: $single, double bookings: $double\n";
$T->hideTestBookings();
exit($double ? 1 : 0);
