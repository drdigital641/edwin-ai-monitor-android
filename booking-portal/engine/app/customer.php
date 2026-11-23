<?php
/* Customer screens. Tenant is fixed from the URL slug; a logged-in customer is only valid for that same client. */
declare(strict_types=1);
if (!defined('P1B')) { http_response_code(404); exit; }

function cust(Tenant $T): ?array {
    if (empty($_SESSION['cust']) || (int) ($_SESSION['cid'] ?? 0) !== $T->id()) return null;
    $c = $T->customer((int) $_SESSION['cust']);
    if (!$c || $c['pin_hash'] === null) { unset($_SESSION['cust']); return null; }   // PIN reset by admin => logged out
    return $c;
}
function need_cust(Tenant $T, string $back = ''): array {
    $c = cust($T);
    if (!$c) { $_SESSION['after_login'] = $back; redirect(curl_($T->client['slug'], 'login')); }
    return $c;
}
function cpage(Tenant $T, string $title, string $body, bool $h1 = true): void {
    page(['client' => $T->client, 'title' => $title, 'h1' => $h1 ? $title : '', 'body' => $body, 'area' => 'c', 'nav' => customer_nav($T->client)]);
}
function slug_url(Tenant $T, string $r = '', array $p = []): string { return curl_($T->client['slug'], $r, $p); }

function find_service(Tenant $T, string $key): ?array {
    foreach ($T->services(true) as $s) if ((string) $s['id'] === $key || $s['slug'] === $key) return $s;
    return null;
}

function customer_route(Tenant $T, string $r): void {
    $c = $T->client;
    switch ($r) {
        case '': c_home($T); return;
        case 'login': c_login($T); return;
        case 'register': c_register($T); return;
        case 'logout': if (is_post()) { require_post_ok(); $e = $_SESSION['embed'] ?? null; session_end_all(); } redirect(slug_url($T)); return;
        case 'forgot': c_forgot($T); return;
        case 'book': c_book($T); return;
        case 'done': c_done($T); return;
        case 'mine': c_mine($T); return;
        case 'move': c_move($T); return;
        case 'cancel': c_cancel($T); return;
        case 'privacy': c_privacy($T); return;
        default: http_response_code(404); cpage($T, t('not_found'), '');
    }
}

function c_home(Tenant $T): void {
    $c = $T->client;
    // ?service=<slug or group> from the client site preselects or filters
    $want = q_str('service', 80);
    $all = $T->services(true);
    if ($want !== '') {
        $hit = array_values(array_filter($all, fn($s) => $s['slug'] === $want));
        if ($hit && client_bookable($T)) { $_SESSION['pick'] = (int) $hit[0]['id']; redirect(slug_url($T, 'book', ['s' => $hit[0]['id']])); }
        $grp = array_values(array_filter($all, fn($s) => $s['group_slug'] === $want));
        if ($grp) $all = $grp;
    }
    if (!client_bookable($T) || !$all) {
        cpage($T, t('book_title'), '<div class="card center"><p>' . e(t('wa_not_open')) . '</p>' . wa_button($c, t('wa_prefill_book', ['name' => $c['name']]), t('wa_to_book'), 'btn wa big') . '</div>');
        return;
    }
    $hours = $T->hours();
    $h = '<h2 class="sub">' . e(t('choose_service')) . '</h2><ul class="svcs">';
    foreach ($all as $s) {
        $meta = array_filter([dur_label($s), price_label($s)]);
        $h .= '<li class="svc"><div class="svc-t"><h3>' . e($s['name']) . '</h3><p class="muted">' . e($s['description']) . '</p>'
            . ($meta ? '<p class="meta">' . implode('<span class="sep"></span>', array_map('e', $meta)) . '</p>' : '') . '</div>';
        if (service_fits_any_day($s, $hours)) $h .= '<a class="btn" href="' . e(slug_url($T, 'book', ['s' => $s['id']])) . '">' . e(t('book')) . '</a>';
        else $h .= wa_button($c, t('wa_prefill_one', ['name' => $c['name'], 'service' => $s['name']]), t('wa_to_book_one'), 'btn wa');
        $h .= '</li>';
    }
    $h .= '</ul>';
    cpage($T, t('book_title'), $h);
}

/* ---------- accounts ---------- */
function c_login(Tenant $T): void {
    $errs = []; $mobile = '';
    if (is_post()) {
        require_post_ok();
        $mobile = in_str('mobile', 30);
        $pin = in_str('pin', 12);
        if (!rate_hit('c_login', 20, 900)) { $errs[] = t('err_rate'); }
        else {
            $e164 = normalise_mobile($mobile);
            $cu = $e164 ? $T->customerByMobile($e164) : null;
            $ok = false;
            if ($cu && $cu['pin_hash'] !== null && !is_locked($cu['locked_until'])) {
                $ok = password_verify($pin, $cu['pin_hash']);
                if ($ok) { $T->loginOk((int) $cu['id']); if (password_needs_rehash($cu['pin_hash'], PASSWORD_DEFAULT)) $T->setPin((int) $cu['id'], $pin); }
                else { $T->loginFail((int) $cu['id']); audit($T->id(), 'cust:' . $cu['id'], 'login_fail'); }
            } else {
                password_verify($pin, '$2y$10$abcdefghijklmnopqrstuuJ3D1Ga8iUqH2uP7l1dYlQ3yJ5v4zCq'); // same timing
            }
            if ($ok) {
                session_regen();
                $_SESSION['cid'] = $T->id(); $_SESSION['cust'] = (int) $cu['id'];
                audit($T->id(), 'cust:' . $cu['id'], 'login');
                $back = $_SESSION['after_login'] ?? ''; unset($_SESSION['after_login']);
                redirect($back && strpos($back, base_path() . '/') === 0 ? $back : slug_url($T, 'mine'));
            }
            $errs[] = t('err_login');
        }
    }
    $h = errors_html($errs) . '<form method="post" class="card form" novalidate>' . csrf_field()
        . field('mobile', t('mobile'), ['type' => 'tel', 'inputmode' => 'tel', 'autocomplete' => 'tel', 'value' => $mobile, 'required' => 1, 'hint' => t('mobile_hint')])
        . field('pin', t('pin'), ['type' => 'password', 'inputmode' => 'numeric', 'autocomplete' => 'current-password', 'maxlength' => 6, 'pattern' => '[0-9]{6}', 'required' => 1])
        . '<button class="btn big">' . e(t('log_in')) . '</button>'
        . '<div class="reg-cta"><p class="muted">' . e(t('no_account')) . '</p><a class="btn ghost big" href="' . e(slug_url($T, 'register')) . '">' . e(t('create_account')) . '</a></div></form>'
        . '<p class="alt"><a href="' . e(slug_url($T, 'forgot')) . '">' . e(t('forgot_pin')) . '</a></p>';
    cpage($T, t('log_in'), $h);
}

function c_register(Tenant $T): void {
    $errs = []; $mobile = ''; $name = '';
    if (is_post()) {
        require_post_ok();
        $mobile = in_str('mobile', 30); $name = in_str('name', 120);
        $pin = in_str('pin', 12); $pin2 = in_str('pin2', 12);
        $e164 = normalise_mobile($mobile);
        if (!rate_hit('c_reg', 10, 900)) $errs[] = t('err_rate');
        if (!$e164) $errs[] = t('err_mobile');
        if ($name === '') $errs[] = t('err_name');
        if (!preg_match('/^\d{6}$/', $pin)) $errs[] = t('err_pin_format');
        elseif ($pin !== $pin2) $errs[] = t('err_pin_match');
        elseif (weak_pin($pin)) $errs[] = t('err_pin_weak');
        if (empty($_POST['consent'])) $errs[] = t('err_consent');
        if (!$errs) {
            $ex = $T->customerByMobile($e164);
            if ($ex && $ex['pin_hash'] !== null) $errs[] = t('err_exists');
            else {
                if ($ex) { $T->claim((int) $ex['id'], $name, $pin); $id = (int) $ex['id']; audit($T->id(), 'cust:' . $id, 'claim'); }
                else { $id = $T->createCustomer($e164, $name, $pin, 'customer'); audit($T->id(), 'cust:' . $id, 'register', '', 'mobile ' . mask_mobile($e164)); }
                session_regen();
                $_SESSION['cid'] = $T->id(); $_SESSION['cust'] = $id;
                flash(t('reg_done'));
                $back = $_SESSION['after_login'] ?? ''; unset($_SESSION['after_login']);
                redirect($back && strpos($back, base_path() . '/') === 0 ? $back : slug_url($T));
            }
        }
    }
    $plink = '<a href="' . e(slug_url($T, 'privacy')) . '" target="_blank" rel="noopener">' . e(t('consent_link')) . '</a>';
    $consent = str_replace(['{link}', '{name}'], [$plink, e($T->client['name'])], e(t('consent')));
    $consent = str_replace(e('{link}'), $plink, $consent);
    $h = errors_html($errs) . '<form method="post" class="card form" novalidate>' . csrf_field()
        . field('mobile', t('mobile'), ['type' => 'tel', 'inputmode' => 'tel', 'autocomplete' => 'tel', 'value' => $mobile, 'required' => 1, 'hint' => t('mobile_hint')])
        . field('name', t('name'), ['autocomplete' => 'name', 'value' => $name, 'required' => 1, 'maxlength' => 120])
        . field('pin', t('pin'), ['type' => 'password', 'inputmode' => 'numeric', 'autocomplete' => 'new-password', 'maxlength' => 6, 'pattern' => '[0-9]{6}', 'required' => 1, 'hint' => t('pin_hint')])
        . field('pin2', t('pin_again'), ['type' => 'password', 'inputmode' => 'numeric', 'autocomplete' => 'new-password', 'maxlength' => 6, 'pattern' => '[0-9]{6}', 'required' => 1])
        . '<label class="chk" for="c_consent"><input type="checkbox" id="c_consent" name="consent" value="1" required><span>' . $consent . '</span></label>'
        . '<button class="btn big">' . e(t('register')) . '</button></form>'
        . '<p class="alt">' . e(t('have_account')) . ' <a href="' . e(slug_url($T, 'login')) . '">' . e(t('log_in')) . '</a></p>';
    cpage($T, t('register'), $h);
}

function c_forgot(Tenant $T): void {
    $c = $T->client;
    cpage($T, t('forgot_pin'), '<div class="card center"><p>' . e(t('forgot_text')) . '</p>' . wa_button($c, t('forgot_prefill', ['name' => $c['name']]), t('whatsapp_us'), 'btn wa big') . '</div>');
}

function c_privacy(Tenant $T): void {
    $c = $T->client;
    $wa = $c['whatsapp_e164'] ? '+' . ltrim($c['whatsapp_e164'], '+') : '';
    $h = '<div class="card prose">';
    foreach (tl('privacy_body', ['name' => $c['name'], 'wa' => $wa]) as $p) $h .= '<p>' . e($p) . '</p>';
    $h .= wa_button($c, '', t('whatsapp_us')) . '</div>';
    cpage($T, t('privacy_title'), $h);
}

/* ---------- booking ---------- */
function c_book(Tenant $T): void {
    $c = $T->client;
    $svc = find_service($T, (string) ($_GET['s'] ?? $_POST['s'] ?? ''));
    if (!$svc || !client_bookable($T)) redirect(slug_url($T));
    $cu = need_cust($T, slug_url($T, 'book', ['s' => $svc['id']]));
    if ($cu['review'] === 'flagged') { cpage($T, t('book_title'), '<div class="card center"><p>' . e(t('err_flagged')) . '</p>' . wa_button($c, t('wa_prefill_book', ['name' => $c['name']]), t('whatsapp_us'), 'btn wa big') . '</div>'); return; }
    $ctx = ctx_for($T);
    $busy = busy_fn($T);
    $canRepeat = $c['recurring_enabled'] && $svc['recurring_allowed'];
    $errs = [];

    if (is_post()) {
        require_post_ok();
        $act = in_str('act', 20);
        $note = in_str('note', 500);
        $start = in_int('t');
        $freq = $canRepeat ? in_str('freq', 10) : 'one';
        $count = max(2, min((int) $c['max_repeats'], in_int('count')));
        if ($act === 'confirm' && ($freq === 'one' || !in_array($freq, ['weekly', 'monthly'], true))) {
            try {
                $ref = book_one($T, $svc, (int) $cu['id'], $start, $note, 'customer', [], null, (bool) $cu['is_test']);
                audit($T->id(), 'cust:' . $cu['id'], 'book', $ref);
                $_SESSION['last_refs'] = [$ref];
                redirect(slug_url($T, 'done'));
            } catch (DomainException $ex) { $errs[] = problem_text($ex->getMessage()); }
        } elseif ($act === 'confirm' || $act === 'series') {
            // recurring: preview first (act=confirm), then commit (act=series)
            $plan = series_plan($ctx, $svc, $start, $freq, $count, $busy);
            if ($act === 'series') {
                $starts = [];
                foreach ($plan as $it) {
                    $choice = (string) ($_POST['pick'][$it['i']] ?? 'skip');
                    if ($it['ok'] && $choice === 'keep') $starts[] = $it['start'];
                    elseif (!$it['ok'] && $choice === 'sugg' && $it['suggestion']) $starts[] = $it['suggestion'];
                }
                if ($starts) {
                    try {
                        $refs = book_series($T, $svc, (int) $cu['id'], $freq, $starts, $note, 'customer', (bool) $cu['is_test']);
                        audit($T->id(), 'cust:' . $cu['id'], 'book_series', $refs[0], count($refs) . ' bookings');
                        $_SESSION['last_refs'] = $refs;
                        redirect(slug_url($T, 'done'));
                    } catch (DomainException $ex) { $errs[] = problem_text($ex->getMessage()); $plan = series_plan($ctx, $svc, $start, $freq, $count, $busy); }
                }
            }
            series_preview($T, $ctx, $svc, $plan, $start, $freq, $count, $note, $errs);
            return;
        }
    }

    $sel = (int) ($_GET['t'] ?? $_POST['t'] ?? 0);
    if ($sel && slot_problem($ctx, $svc, $sel, $busy($sel, $sel + 86400)) === null) {
        // details + confirm
        $end = $sel + svc_block_minutes($ctx, $svc, $sel) * 60;
        $h = errors_html($errs) . '<div class="card"><dl class="kv"><dt>' . e(t('service')) . '</dt><dd>' . e($svc['name']) . '</dd><dt>' . e(t('date')) . '</dt><dd>' . e(fmt_local($ctx, $sel, 'D j M Y')) . '</dd>'
            . '<dt>' . e(t('time')) . '</dt><dd>' . e(fmt_local($ctx, $sel, 'g:i a') . ' - ' . fmt_local($ctx, $end, 'g:i a')) . '</dd>'
            . (($p = price_label($svc)) !== '' ? '<dt>' . e(t('price')) . '</dt><dd>' . e($p) . '</dd>' : '') . '</dl>'
            . '<a class="link" href="' . e(slug_url($T, 'book', ['s' => $svc['id'], 'd' => local_date($ctx, $sel)])) . '">' . e(t('change')) . '</a></div>'
            . '<form method="post" class="card form" action="' . e(slug_url($T, 'book', ['s' => $svc['id']])) . '">' . csrf_field()
            . '<input type="hidden" name="t" value="' . $sel . '"><input type="hidden" name="act" value="confirm">'
            . field('note', t('note'), ['type' => 'textarea', 'maxlength' => 500, 'hint' => t('note_hint'), 'value' => in_str('note', 500)]);
        if ($canRepeat) {
            // defaults come from the service's own settings (admin > Services); a posted value wins when the form is shown again
            $maxr = (int) $c['max_repeats'];
            $dfreq = in_array($pf = in_str('freq', 10), ['one', 'weekly', 'monthly'], true) ? $pf : svc_freq($svc);
            $dcount = max(2, min($maxr, in_int('count') ?: (svc_reps($svc) ?? 4)));
            $h .= '<fieldset class="seg"><legend>' . e(t('repeat')) . '</legend>';
            foreach (['one' => t('one_off'), 'weekly' => t('weekly'), 'monthly' => t('monthly')] as $k => $lbl)
                $h .= '<label><input type="radio" name="freq" value="' . $k . '"' . ($k === $dfreq ? ' checked' : '') . '><span>' . e($lbl) . '</span></label>';
            $h .= '</fieldset><div class="rep-count">' . field('count', t('repeats_n'), ['type' => 'number', 'inputmode' => 'numeric', 'min' => 2, 'max' => $maxr, 'value' => (string) $dcount])
                . '<p class="rep-note">' . e(t('repeat_self_move')) . '</p></div>';
        }
        $h .= '<div class="sticky"><button class="btn big">' . e($canRepeat ? t('continue') : t('confirm')) . '</button></div></form>';
        cpage($T, $svc['name'], $h);
        return;
    }

    $strip = date_strip($ctx, $svc, $busy);
    $d = q_str('d', 10);
    if (!isset($strip[$d]) || $strip[$d] !== 'open') $d = first_open($strip);
    $slots = [];
    if ($d !== '') { $w = day_window($ctx, $d); $slots = is_array($w) ? slots_for_date($ctx, $svc, $d, $busy($w[0], $w[1])) : []; }
    $h = errors_html($errs) . '<p class="muted svc-line">' . e(implode(' / ', array_filter([dur_label($svc), price_label($svc)]))) . '</p>';
    $h .= $d === '' ? '<div class="card center"><p>' . e(t('no_dates')) . '</p>' . wa_button($c, t('wa_prefill_one', ['name' => $c['name'], 'service' => $svc['name']]), t('whatsapp_us'), 'btn wa') . '</div>'
        : picker_html($ctx, $svc, $strip, $d, $slots, fn($x) => slug_url($T, 'book', ['s' => $svc['id'], 'd' => $x]), fn($s) => slug_url($T, 'book', ['s' => $svc['id'], 't' => $s]));
    cpage($T, $svc['name'], $h);
}

function series_preview(Tenant $T, array $ctx, array $svc, array $plan, int $start, string $freq, int $count, string $note, array $errs): void {
    $h = errors_html($errs) . '<form method="post" class="form" action="' . e(slug_url($T, 'book', ['s' => $svc['id']])) . '">' . csrf_field()
        . '<input type="hidden" name="act" value="series"><input type="hidden" name="t" value="' . $start . '"><input type="hidden" name="freq" value="' . e($freq) . '">'
        . '<input type="hidden" name="count" value="' . $count . '"><input type="hidden" name="note" value="' . e($note) . '"><ol class="plan">';
    $day = (int) fmt_local($ctx, $start, 'j');
    foreach ($plan as $it) {
        $i = $it['i'];
        $when = fmt_local($ctx, $it['start'], 'D j M Y, g:i a');
        $h .= '<li class="pl ' . ($it['ok'] ? 'ok' : 'bad') . '"><div class="pl-h"><b>' . e($when) . '</b><span class="tag">' . e($it['ok'] ? t('preview_ok') : t('preview_clash')) . '</span></div>';
        if ($it['last_day']) $h .= '<p class="muted small">' . e(t('preview_lastday', ['day' => $day])) . '</p>';
        if ($it['ok']) {
            $h .= '<input type="hidden" name="pick[' . $i . ']" value="keep">';
        } else {
            $h .= '<p class="muted small">' . e($it['problem'] === 'full' ? t('preview_taken') : problem_text((string) $it['problem'])) . '</p>';
            if ($it['suggestion']) {
                $h .= '<p>' . e(t('preview_suggest', ['when' => fmt_local($ctx, $it['suggestion'], 'D j M, g:i a')])) . '</p>'
                    . '<div class="seg"><label><input type="radio" name="pick[' . $i . ']" value="sugg" checked><span>' . e(t('preview_use')) . '</span></label>'
                    . '<label><input type="radio" name="pick[' . $i . ']" value="skip"><span>' . e(t('preview_skip')) . '</span></label></div>';
            } else {
                $h .= '<p>' . e(t('preview_none')) . '</p><input type="hidden" name="pick[' . $i . ']" value="skip">';
            }
        }
        $h .= '</li>';
    }
    $h .= '</ol><div class="sticky"><button class="btn big">' . e(t('confirm_series')) . '</button></div></form>'
        . '<p class="alt"><a href="' . e(slug_url($T, 'book', ['s' => $svc['id'], 't' => $start])) . '">' . e(t('back')) . '</a></p>';
    cpage($T, t('preview_title'), $h);
}

function c_done(Tenant $T): void {
    $cu = need_cust($T);
    $refs = (array) ($_SESSION['last_refs'] ?? []);
    $ctx = ctx_for($T);
    $list = array_values(array_filter(array_map(fn($r) => $T->customerBooking((int) $cu['id'], (string) $r), $refs)));
    if (!$list) redirect(slug_url($T, 'mine'));
    $h = '<div class="card done"><p class="shot">' . e(t('screenshot')) . '</p>';
    foreach ($list as $b) $h .= booking_rows($ctx, $b);
    $h .= '</div><p class="alt"><a class="btn ghost" href="' . e(slug_url($T, 'mine')) . '">' . e(t('my_bookings')) . '</a> <a class="btn ghost" href="' . e(slug_url($T)) . '">' . e(t('book_another')) . '</a></p>'
        . '<span hidden data-confirmed="' . e($T->client['slug']) . '"></span>';
    cpage($T, count($list) > 1 ? t('confirmed_series_title') : t('confirmed_title'), $h);
}

function c_mine(Tenant $T): void {
    $cu = need_cust($T, slug_url($T, 'mine'));
    $ctx = ctx_for($T);
    $up = []; $past = [];
    foreach ($T->customerBookings((int) $cu['id']) as $b) {
        if ($b['status'] === 'confirmed' && db_ts($b['end_at']) > time()) $up[] = $b; else $past[] = $b;
    }
    usort($up, fn($a, $b) => strcmp($a['start_at'], $b['start_at']));
    $h = '<h2>' . e(t('upcoming')) . '</h2>';
    if (!$up) $h .= '<p class="muted">' . e(t('none_upcoming')) . '</p>';
    foreach ($up as $b) {
        $h .= '<div class="card bk">' . booking_rows($ctx, $b);
        if ($b['series_id']) $h .= '<p class="muted small">' . e(t('series_of', ['freq' => ''])) . '</p>';
        if (before_cutoff($ctx, db_ts($b['start_at']))) {
            $h .= '<div class="acts"><a class="btn ghost" href="' . e(slug_url($T, 'move', ['ref' => $b['ref']])) . '">' . e(t('reschedule')) . '</a>'
                . '<a class="btn ghost danger" href="' . e(slug_url($T, 'cancel', ['ref' => $b['ref']])) . '">' . e(t('cancel')) . '</a></div>';
        } else {
            $h .= '<p class="note">' . e(t('after_cutoff')) . '</p>' . wa_button($T->client, t('wa_prefill_book', ['name' => $T->client['name']]) . ' ' . $b['ref'], t('whatsapp_us'), 'btn wa');
        }
        $h .= '</div>';
    }
    $h .= '<h2>' . e(t('past')) . '</h2>';
    if (!$past) $h .= '<p class="muted">' . e(t('none_past')) . '</p>';
    else {
        $h .= '<ul class="hist">';
        foreach ($past as $b) $h .= '<li><span>' . e(fmt_local($ctx, db_ts($b['start_at']), 'j M Y')) . '</span><span>' . e($b['service_name']) . '</span><span class="tag">' . e(status_label($b['status'])) . '</span></li>';
        $h .= '</ul>';
    }
    $h .= '<p class="alt"><a class="btn" href="' . e(slug_url($T)) . '">' . e(t('book_another')) . '</a></p>';
    cpage($T, t('my_bookings'), $h);
}

function own_booking(Tenant $T, array $cu): array {
    $b = $T->customerBooking((int) $cu['id'], strtoupper(in_str('ref', 16)));
    if (!$b) redirect(slug_url($T, 'mine'));
    return $b;
}

function c_move(Tenant $T): void {
    $cu = need_cust($T, slug_url($T, 'mine'));
    $b = own_booking($T, $cu);
    $ctx = ctx_for($T);
    if ($b['status'] !== 'confirmed' || !before_cutoff($ctx, db_ts($b['start_at']))) { flash(t('after_cutoff'), 'err'); redirect(slug_url($T, 'mine')); }
    $svc = $T->service((int) $b['service_id']);
    $busy = busy_fn($T, (int) $b['id']);
    $errs = [];
    if (is_post()) {
        require_post_ok();
        $new = in_int('t');
        try {
            if ($b['series_id'] && in_str('scope', 10) === 'later') reschedule_series($T, $b, $new, false); else reschedule($T, $b, $new, false);
            audit($T->id(), 'cust:' . $cu['id'], 'reschedule', $b['ref']);
            flash(t('moved', ['ref' => $b['ref'], 'when' => fmt_local($ctx, $new, 'D j M, g:i a')]));
            redirect(slug_url($T, 'mine'));
        } catch (DomainException $ex) { $errs[] = problem_text($ex->getMessage()); }
    }
    $sel = (int) ($_GET['t'] ?? 0);
    if ($sel && !$errs) {
        $h = '<div class="card"><dl class="kv"><dt>' . e(t('ref')) . '</dt><dd><b class="ref">' . e($b['ref']) . '</b></dd><dt>' . e(t('date')) . '</dt><dd>' . e(fmt_local($ctx, $sel, 'D j M Y, g:i a')) . '</dd></dl></div>'
            . '<form method="post" class="form">' . csrf_field() . '<input type="hidden" name="t" value="' . $sel . '">'
            . ($b['series_id'] ? '<fieldset class="seg col"><legend>' . e(t('move_scope')) . '</legend><label><input type="radio" name="scope" value="one" checked><span>' . e(t('this_only')) . '</span></label><label><input type="radio" name="scope" value="later"><span>' . e(t('this_and_later')) . '</span></label><small>' . e(t('move_later_note')) . '</small></fieldset>' : '')
            . '<div class="sticky"><button class="btn big">' . e(t('reschedule')) . '</button></div></form>';
        cpage($T, t('reschedule'), $h);
        return;
    }
    $strip = date_strip($ctx, $svc, $busy);
    $d = q_str('d', 10);
    if (!isset($strip[$d]) || $strip[$d] !== 'open') $d = first_open($strip);
    $slots = [];
    if ($d !== '') { $w = day_window($ctx, $d); $slots = is_array($w) ? slots_for_date($ctx, $svc, $d, $busy($w[0], $w[1])) : []; }
    $h = errors_html($errs) . '<p class="muted">' . e(t('move_q', ['ref' => $b['ref']])) . '</p>'
        . picker_html($ctx, $svc, $strip, $d, $slots, fn($x) => slug_url($T, 'move', ['ref' => $b['ref'], 'd' => $x]), fn($s) => slug_url($T, 'move', ['ref' => $b['ref'], 't' => $s]));
    cpage($T, t('reschedule'), $h);
}

function c_cancel(Tenant $T): void {
    $cu = need_cust($T, slug_url($T, 'mine'));
    $b = own_booking($T, $cu);
    $ctx = ctx_for($T);
    if (is_post()) {
        require_post_ok();
        try {
            $refs = cancel_bookings($T, $b, in_str('scope', 10) === 'later', false);
            foreach ($refs as $r) audit($T->id(), 'cust:' . $cu['id'], 'cancel', $r);
            flash(t('cancelled_n', ['refs' => implode(', ', $refs)]));
        } catch (DomainException $ex) { flash(problem_text($ex->getMessage()), 'err'); }
        redirect(slug_url($T, 'mine'));
    }
    $h = '<div class="card">' . booking_rows($ctx, $b) . '</div><form method="post" class="card form">' . csrf_field();
    if ($b['series_id']) {
        $h .= '<fieldset class="seg col"><legend>' . e(t('cancel_q')) . '</legend><label><input type="radio" name="scope" value="one" checked><span>' . e(t('this_only')) . '</span></label>'
            . '<label><input type="radio" name="scope" value="later"><span>' . e(t('this_and_later')) . '</span></label></fieldset>';
    }
    $h .= '<button class="btn big danger">' . e(t('cancel')) . '</button></form><p class="alt"><a href="' . e(slug_url($T, 'mine')) . '">' . e(t('back')) . '</a></p>';
    cpage($T, t('cancel'), $h);
}
