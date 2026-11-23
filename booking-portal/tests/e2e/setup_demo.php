<?php
/* Test-only demo client "test-sga": SgAutobots look + services, invented TEST hours, is_test=1. Never used for the real client. */
declare(strict_types=1);
define('P1B', true);
$root = dirname(__DIR__, 2) . '/public';
foreach (['bootstrap', 'db', 'slots', 'booking'] as $f) require "$root/app/$f.php";
require "$root/app/views.php"; require "$root/app/super.php";
if (!cfg('test_mode')) exit(2);
migrate();
$j = json_decode(file_get_contents("$root/app/seed/sg-autobots.json"), true);
if (!client_by_slug('test-sga')) {
    $c = $j['client']; $c['slug'] = 'test-sga'; $c['name'] = 'SgAutobots'; $c['status'] = 'live'; $c['is_test'] = 1; $c['logo_url'] = getenv('DEMO_LOGO') ?: '';
    $c['allowed_embed_domains'] = 'clientsite.test';
    $id = SuperRepo::saveClient($c);
    $T = new Tenant(SuperRepo::client($id));
    foreach ($j['services'] as $i => $s) $T->saveService($s + ['price' => null, 'recurring_allowed' => 0, 'sort_order' => $i, 'full_day' => 0, 'admin_note' => '', 'duration_min' => null]);
    $h = []; for ($wd = 1; $wd <= 7; $wd++) $h[$wd] = ['open_time' => '09:00:00', 'close_time' => '18:00:00', 'closed' => $wd === 7];
    $T->saveHours($h);
    $off = (new DateTimeImmutable('today', new DateTimeZone('Asia/Singapore')))->modify('+4 day')->format('Y-m-d');
    $T->addOffDay($off, $off, 'Test off day');
    SuperRepo::upsertClientAdmin($id, 'test-sga-admin', getenv('DEMO_ADMIN_PW'));
    ensure_stub('test-sga');
}
$T = new Tenant(client_by_slug('test-sga'));
// a clash for the recurring preview: other test customer holds next-next Wednesday 10:00
$other = $T->customerByMobile('+6500000004') ?? $T->customer($T->createCustomer('+6500000004', 'Other tester', '480317'));
$wash = array_values(array_filter($T->services(), fn($s) => $s['slug'] === 'car-wash-package'))[0];
$wed = (new DateTimeImmutable('next wednesday 10:00', new DateTimeZone('Asia/Singapore')))->modify('+7 day')->getTimestamp();
if (!$T->busy($wed, $wed + 3600)) book_one($T, $wash, (int) $other['id'], $wed, 'Test clash', 'admin', [], null, true);
echo json_encode(['client_id' => $T->id(), 'wash' => (int) $wash['id']]), "\n";
