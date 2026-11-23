<?php
/* TEST ONLY (local): after the demo client's admin setup, mark it is_test + live, give it invented hours and the SgAutobots service list.
   Run with P1B_CONFIG=<demo config>. Refuses unless that config has test_mode on. Never run against a real client. */
declare(strict_types=1);
define('P1B', true);
$root = dirname(__DIR__, 2) . '/engine';
foreach (['bootstrap', 'db', 'slots', 'booking'] as $f) require "$root/app/$f.php";
if (!cfg('test_mode') || cfg('client_slug') !== 'demo') exit(2);
$c = client_by_slug('demo'); if (!$c) exit(3);
$j = json_decode(file_get_contents("$root/app/seed/sg-autobots.json"), true);
$keep = array_intersect_key($j['client'], array_flip(['colour_primary', 'colour_accent', 'colour_bg', 'recurring_enabled']));
SuperRepo::saveClient(['id' => $c['id'], 'slug' => 'demo', 'name' => 'Demo Detailing', 'logo_url' => '', 'whatsapp_e164' => '+6500000099', 'timezone' => 'Asia/Singapore',
    'allowed_embed_domains' => 'clientsite.test', 'status' => 'live', 'is_test' => 1] + $keep);
$T = new Tenant(client_by_slug('demo'));
if (!$T->services()) foreach ($j['services'] as $i => $s) $T->saveService($s + ['price' => null, 'recurring_allowed' => 0, 'sort_order' => $i, 'full_day' => 0, 'admin_note' => '', 'duration_min' => null]);
$h = []; for ($wd = 1; $wd <= 7; $wd++) $h[$wd] = ['open_time' => '09:00:00', 'close_time' => '18:00:00', 'closed' => $wd === 7];
$T->saveHours($h);
echo "demo ready\n";
