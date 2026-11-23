<?php
/* CLI test runner: php tests/run_tests.php   (needs P1B_CONFIG pointing at a TEST config + test database) */
declare(strict_types=1);
define('P1B', true);
$root = dirname(__DIR__) . '/engine';
require $root . '/app/bootstrap.php';
require $root . '/app/db.php';
require $root . '/app/slots.php';
require $root . '/app/booking.php';
if (!cfg('test_mode')) { fwrite(STDERR, "refusing: config is not test_mode\n"); exit(2); }

$pass = 0; $fail = 0; $log = [];
function ok(bool $c, string $name): void { global $pass, $fail, $log; if ($c) { $pass++; $log[] = "PASS $name"; } else { $fail++; $log[] = "FAIL $name"; } }

$SG = new DateTimeZone('Asia/Singapore');
function sg(string $s): int { return (new DateTimeImmutable($s, new DateTimeZone('Asia/Singapore')))->getTimestamp(); }
$client = ['timezone' => 'Asia/Singapore', 'slot_step_min' => 30, 'max_days_ahead' => 60, 'min_notice_min' => 120, 'capacity' => 1, 'cancel_cutoff_min' => 720];
$hours = [];
for ($wd = 1; $wd <= 7; $wd++) $hours[$wd] = ['open_time' => '09:00:00', 'close_time' => '18:00:00', 'closed' => $wd === 7 ? 1 : 0];   // Sunday closed
$now = sg('2026-12-01 08:00');   // Tuesday
$ctx = engine_ctx($client, $hours, [['start_date' => '2026-12-10', 'end_date' => '2026-12-12']], $now);
$svc90 = ['duration_min' => 90, 'full_day' => 0];
$none = fn($a, $b) => [];

/* ---- slot engine ---- */
$s = slots_for_date($ctx, $svc90, '2026-12-02', []);
ok(fmt_local($ctx, end($s), 'H:i') === '16:30', 'duration fits before closing (last 90-min slot 16:30, ends 18:00)');
ok(fmt_local($ctx, $s[0], 'H:i') === '09:00' && fmt_local($ctx, $s[1], 'H:i') === '09:30', 'slot step 30 from open_time');
$c15 = engine_ctx(['slot_step_min' => 15] + $client, $hours, [], $now);
$s15 = slots_for_date($c15, $svc90, '2026-12-02', []);
ok(fmt_local($c15, $s15[1], 'H:i') === '09:15' && count($s15) === 31, 'slot step 15 gives 31 starts');
ok(slot_problem($ctx, $svc90, sg('2026-12-02 16:45'), []) !== null, 'start off the step grid refused');
ok(slot_problem($ctx, $svc90, sg('2026-12-02 17:00'), []) === 'too_late', 'job running past closing refused');
$sToday = slots_for_date($ctx, $svc90, '2026-12-01', []);
ok(fmt_local($ctx, $sToday[0], 'H:i') === '10:00', 'min notice 120: first slot today 10:00 when now is 08:00');
ok(slot_problem($ctx, $svc90, sg('2026-12-01 09:30'), []) === 'notice', 'inside notice refused');
ok(slot_problem(engine_ctx($client, $hours, [], $now, ['ignore_notice' => true]), $svc90, sg('2026-12-01 09:30'), []) === null, 'admin override of notice works');
ok(slot_problem($ctx, $svc90, sg('2026-12-01 07:00'), []) !== null, 'past time refused even with override');
ok(slots_for_date($ctx, $svc90, '2027-01-30', []) !== [] && slot_problem($ctx, $svc90, sg('2027-02-01 09:00'), []) === 'too_far', 'max_days_ahead 60: day 60 (30 Jan) ok, 1 Feb refused');
ok(slots_for_date($ctx, $svc90, '2026-12-11', []) === [] && day_window($ctx, '2026-12-10') === 'off' && day_window($ctx, '2026-12-12') === 'off' && is_array(day_window($ctx, '2026-12-09')), 'off-day range 10-12 Dec blocked, 9 Dec open');
ok(day_window($ctx, '2026-12-06') === 'closed' && slots_for_date($ctx, $svc90, '2026-12-06', []) === [], 'closed weekday (Sunday) has no slots');
$busy = [[sg('2026-12-02 10:00'), sg('2026-12-02 11:30'), 1]];
ok(slot_problem($ctx, $svc90, sg('2026-12-02 09:00'), $busy) === 'full' && slot_problem($ctx, $svc90, sg('2026-12-02 11:30'), $busy) === null && slot_problem($ctx, $svc90, sg('2026-12-02 08:30') + 3600, $busy) === 'full', 'capacity 1: overlap refused, back-to-back allowed');
$ctx2 = engine_ctx(['capacity' => 2] + $client, $hours, [], $now);
$busy2 = [[sg('2026-12-02 10:00'), sg('2026-12-02 11:30'), 1], [sg('2026-12-02 11:00'), sg('2026-12-02 12:30'), 2]];
ok(slot_problem($ctx2, $svc90, sg('2026-12-02 09:00'), $busy2) === null, 'capacity 2: one overlap allowed');
ok(slot_problem($ctx2, $svc90, sg('2026-12-02 10:30'), $busy2) === 'full', 'capacity 2: two overlapping at the same minute refused');
ok(slot_problem($ctx2, $svc90, sg('2026-12-02 12:00'), $busy2) === null, 'capacity 2: only one running at 12:00-13:30, allowed');
ok(peak_overlap([[0, 10, 1], [10, 20, 2]], 0, 20) === 1, 'touching bookings do not count as overlapping');
$long = ['duration_min' => 600, 'full_day' => 0];
ok(!service_fits_any_day($long, $hours) && slots_for_date($ctx, $long, '2026-12-02', []) === [], 'service longer than open hours: not bookable online (WhatsApp)');
ok(service_fits_any_day($svc90, $hours) && !service_fits_any_day($svc90, []), 'no hours set => nothing bookable');
$full = ['duration_min' => null, 'full_day' => 1];
$sf = slots_for_date($ctx, $full, '2026-12-02', []);
ok(count($sf) === 1 && fmt_local($ctx, $sf[0], 'H:i') === '09:00' && slot_problem($ctx, $full, sg('2026-12-02 09:00'), [[sg('2026-12-02 17:00'), sg('2026-12-02 18:00'), 1]]) === 'full', 'full-day service: one slot at opening, blocked by any booking that day');

/* ---- recurring ---- */
$first = sg('2026-12-02 10:00');
$plan = series_plan($ctx, $svc90, $first, 'weekly', 4, fn($a, $b) => [[sg('2026-12-16 10:00'), sg('2026-12-16 11:30'), 9]]);
ok($plan[0]['ok'] && $plan[1]['ok'] && $plan[2]['problem'] === 'full' && $plan[3]['ok'], 'weekly series: 16 Dec clash flagged, other dates free');
$plan = series_plan($ctx, $svc90, sg('2026-12-03 10:00'), 'weekly', 3, fn($a, $b) => [[sg('2026-12-17 10:00'), sg('2026-12-17 11:30'), 9]]);
ok($plan[1]['problem'] === 'off' && fmt_local($ctx, $plan[1]['suggestion'], 'Y-m-d H:i') === '2026-12-14 09:00', 'repeat on off day 10 Dec suggests next free 14 Dec 09:00 (11-12 off, 13 Sunday)');
ok($plan[2]['problem'] === 'full' && fmt_local($ctx, $plan[2]['suggestion'], 'Y-m-d H:i') === '2026-12-17 11:30', 'clashing repeat suggests next free slot same day 11:30');
$cm = engine_ctx(['max_days_ahead' => 200] + $client, $hours, [], sg('2026-12-20 08:00'));
$pm = series_plan($cm, $svc90, sg('2026-12-31 10:00'), 'monthly', 4, $none);
ok(array_map(fn($i) => $i['date'], $pm) === ['2026-12-31', '2027-01-31', '2027-02-28', '2027-03-31'] && $pm[2]['last_day'] && !$pm[1]['last_day'], 'monthly 31st: Feb uses last day 28th and is marked');
ok($pm[1]['problem'] === 'closed' && fmt_local($cm, $pm[1]['suggestion'], 'Y-m-d') === '2027-02-01', '31 Jan 2027 is a Sunday: flagged closed, next free 1 Feb');
$self = series_plan($ctx, $svc90, $first, 'weekly', 2, $none);
ok($self[0]['ok'] && $self[1]['ok'], 'series items do not block themselves');

/* ---- cut-off ---- */
ok(before_cutoff($ctx, sg('2026-12-01 20:00')) && !before_cutoff($ctx, sg('2026-12-01 19:59')), 'cut-off 12 h: 20:00 can change, 19:59 cannot (now 08:00)');

/* ---- normalise + PIN ---- */
ok(normalise_mobile('8366 7010') === '+6583667010' && normalise_mobile('+60 12-345 6789') === '+60123456789' && normalise_mobile('012 3456789') === '+60123456789' && normalise_mobile('6123 4567') === null && normalise_mobile('+6500000001') === '+6500000001', 'mobile normalising SG/MY + test range');
ok(weak_pin('123456') && weak_pin('000000') && weak_pin('111111') && weak_pin('654321') && weak_pin('121212') && weak_pin('112233') && !weak_pin('480317'), 'weak PINs rejected');
ok(mask_mobile('+6583667010') === '+65****7010', 'mobile masked for logs');

/* ===== DB tests ===== */
migrate();
function mkclient(string $slug, int $cap = 1): Tenant {
    $old = client_by_slug($slug);
    if ($old) return new Tenant($old);
    $id = SuperRepo::saveClient(['slug' => $slug, 'name' => 'Test ' . $slug, 'logo_url' => '', 'colour_primary' => '#13529f', 'colour_accent' => '#f4e940', 'colour_bg' => '#ffffff',
        'whatsapp_e164' => '+6500000099', 'timezone' => 'Asia/Singapore', 'recurring_enabled' => 1, 'allowed_embed_domains' => 'clientsite.test', 'status' => 'live', 'is_test' => 1]);
    $T = new Tenant(SuperRepo::client($id));
    $T->saveHours(array_map(fn($h) => $h, (function () { $r = []; for ($i = 1; $i <= 7; $i++) $r[$i] = ['open_time' => '00:00:00', 'close_time' => '24:00:00', 'closed' => 0]; return $r; })()));
    $T->updateRules(['slot_step_min' => 30, 'max_days_ahead' => 60, 'min_notice_min' => 0, 'cancel_cutoff_min' => 720, 'capacity' => $cap, 'max_repeats' => 12]);
    $T->saveService(['name' => 'Wash', 'description' => 'Test wash', 'duration_min' => 60, 'price' => '50', 'price_note' => '', 'recurring_allowed' => 1, 'active' => 1, 'sort_order' => 0, 'slug' => 'wash']);
    return $T;
}
$A = mkclient('test-a'); $B = mkclient('test-b');
$custA = $A->customerByMobile('+6500000001') ?? $A->customer($A->createCustomer('+6500000001', 'Tester A', '480317'));
$custB = $B->customerByMobile('+6500000001') ?? $B->customer($B->createCustomer('+6500000001', 'Tester B', '480317'));
ok((int) $custA['id'] !== (int) $custB['id'], 'same mobile at two clients = two separate accounts');
ok((bool) $custA['is_test'], 'test-range customer flagged is_test');
$svcA = $A->services()[0]; $svcB = $B->services()[0];
$start = (new DateTimeImmutable('today 10:00', new DateTimeZone('Asia/Singapore')))->modify('+3 day')->getTimestamp();
$refA = book_one($A, $svcA, (int) $custA['id'], $start, 'note A', 'customer', [], null, true);

/* tenant isolation */
ok($B->bookingByRef($refA) === null, 'isolation: client B cannot read A booking by ref');
$bkA = $A->bookingByRef($refA);
ok($B->booking((int) $bkA['id']) === null, 'isolation: client B cannot read A booking by id');
ok($B->customer((int) $custA['id']) === null, 'isolation: client B cannot read A customer by id');
ok($B->service((int) $svcA['id']) === null, 'isolation: client B cannot load A service');
$B->setStatus((int) $bkA['id'], 'cancelled_admin');
ok($A->bookingByRef($refA)['status'] === 'confirmed', 'isolation: client B status change on A booking id has no effect');
$B->moveBooking((int) $bkA['id'], $start + 3600, $start + 7200);
ok($A->bookingByRef($refA)['start_at'] === gmdate('Y-m-d H:i:s', $start), 'isolation: client B move on A booking id has no effect');
$B->resetPin((int) $custA['id']);
ok($A->customer((int) $custA['id'])['pin_hash'] !== null, 'isolation: client B PIN reset on A customer id has no effect');
ok($B->customerBooking((int) $custA['id'], $refA) === null, 'isolation: customer lookup by ref is scoped');
ok(count($B->busy($start - 10, $start + 10)) === 0, 'isolation: A bookings never block B slots');
try { book_one($B, $svcA, (int) $custB['id'], $start, '', 'customer'); ok(false, 'isolation: B cannot book with A service row'); } catch (DomainException $e) { ok($e->getMessage() === 'not_found', 'isolation: B cannot book with A service row'); }
try { book_one($B, $svcB, (int) $custA['id'], $start, '', 'customer'); ok(false, 'isolation: B cannot book for an A customer id'); } catch (DomainException $e) { ok($e->getMessage() === 'not_found', 'isolation: B cannot book for an A customer id'); }
$aAdminId = (int) q("SELECT id FROM admins WHERE username='test-a-admin'")->fetchColumn();
if (!$aAdminId) SuperRepo::upsertClientAdmin($A->id(), 'test-a-admin', 'long-test-password-1');
ok($B->adminByUsername('test-a-admin') === null && $A->adminByUsername('test-a-admin') !== null, 'isolation: A admin cannot log in on B');

/* booking rules in the DB layer */
try { book_one($A, $svcA, (int) $custA['id'], $start + 1800, '', 'customer', [], null, true); ok(false, 'capacity 1 enforced in book_one'); } catch (DomainException $e) { ok($e->getMessage() === 'full', 'capacity 1 enforced in book_one (overlap 30 min later refused)'); }
$ref2 = book_one($A, $svcA, (int) $custA['id'], $start + 3600, '', 'customer', [], null, true);
ok((bool) preg_match('/^TES-[23456789ABCDEFGHJKMNPQRSTUVWXYZ]{6}$/', $ref2), 'ref format short and non-guessable (' . $ref2 . ')');
$b2 = $A->bookingByRef($ref2);
reschedule($A, $b2, $start + 7200, false);
ok($A->bookingByRef($ref2)['start_at'] === gmdate('Y-m-d H:i:s', $start + 7200) && $A->bookingByRef($ref2)['ref'] === $ref2, 'reschedule keeps the same ref');
$near = (int) (ceil((time() + 3600) / 1800) * 1800); if ((int) fmt_local($ctx, $near, 'G') >= 23) $near = (new DateTimeImmutable('tomorrow 00:00', new DateTimeZone('Asia/Singapore')))->getTimestamp();
$refN = book_one($A, $svcA, (int) $custA['id'], $near, '', 'customer', [], null, true);
try { cancel_bookings($A, $A->bookingByRef($refN), false, false); ok(false, 'customer cancel after cut-off refused'); } catch (DomainException $e) { ok($e->getMessage() === 'cutoff', 'customer cancel after cut-off refused'); }
ok(cancel_bookings($A, $A->bookingByRef($refN), false, true) === [$refN], 'admin may cancel after cut-off');
$refs = book_series($A, $svcA, (int) $custA['id'], 'weekly', [$start + 86400 * 7, $start + 86400 * 14, $start + 86400 * 21], '', 'customer', true);
ok(count($refs) === 3 && count(array_unique($refs)) === 3, 'series booked with one ref per date');
$mid = $A->bookingByRef($refs[1]);
ok(cancel_bookings($A, $mid, true, false) === [$refs[1], $refs[2]] && $A->bookingByRef($refs[0])['status'] === 'confirmed', 'cancel "this and later" leaves earlier bookings');

/* lockout + IP limit */
$custL = $A->customerByMobile('+6500000002') ?? $A->customer($A->createCustomer('+6500000002', 'Lock test', '480317'));
$A->loginOk((int) $custL['id']);
for ($i = 0; $i < 5; $i++) $A->loginFail((int) $custL['id']);
$custL = $A->customer((int) $custL['id']);
ok(is_locked($custL['locked_until']), 'lockout: 5 wrong PINs lock the account');
ok(strtotime($custL['locked_until'] . ' UTC') - time() > 880 && strtotime($custL['locked_until'] . ' UTC') - time() <= 900, 'lockout lasts 15 minutes');
$A->loginOk((int) $custL['id']);
$_SERVER['REMOTE_ADDR'] = '203.0.113.' . random_int(1, 250);
q("DELETE FROM rate_limits WHERE scope='t_ip'");
$allowed = 0; for ($i = 0; $i < 25; $i++) if (rate_hit('t_ip', 20, 900)) $allowed++;
ok($allowed === 20, 'IP rate limit: 20 tries per 15 min, then blocked (allowed ' . $allowed . ')');

/* claim flow (Edwin 8:16pm) */
$m = '+65000000' . str_pad((string) random_int(10, 89), 2, '0', STR_PAD_LEFT);
$ex = $A->customerByMobile($m); if ($ex) { $A->resetPin((int) $ex['id']); $cid = (int) $ex['id']; } else $cid = $A->createCustomer($m, 'Admin made', null, 'admin');
ok($A->customer($cid)['pin_hash'] === null, 'admin-created customer has no PIN until claimed');
ok($A->claim($cid, 'Claimed', '480317') && !$A->claim($cid, 'Again', '573920'), 'customer claims once; a claimed account cannot be claimed again');
$A->resetPin($cid);
ok($A->claim($cid, 'Claimed', '573920'), 'after admin PIN reset the customer can claim again with a new PIN');

/* audit has no PII */
$bad = (int) q("SELECT COUNT(*) FROM audit_log WHERE detail REGEXP '[0-9]{8}' OR detail LIKE '%480317%'")->fetchColumn();
ok($bad === 0, 'audit log holds no full mobile or PIN');

/* cleanup: test bookings never show as confirmed */
$A->hideTestBookings(); $B->hideTestBookings();
ok((int) q("SELECT COUNT(*) FROM bookings WHERE is_test=1 AND status='confirmed' AND client_id IN (?,?)", [$A->id(), $B->id()])->fetchColumn() === 0, 'test bookings cancelled after the run');

echo implode("\n", $log), "\n\n$pass passed, $fail failed\n";
exit($fail ? 1 : 0);
