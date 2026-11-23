<?php
/* Client admin screens. Separate session (cookie p1ba). Tenant comes from the URL slug and must equal the session's client. */
declare(strict_types=1);
if (!defined('P1B')) { http_response_code(404); exit; }

function aurl(Tenant $T, string $r = 'a', array $p = []): string { return curl_($T->client['slug'], $r, $p); }
function admin_nav(Tenant $T): string {
    $l = ['a' => t('a_day'), 'a_week' => t('a_week'), 'a_new' => t('a_new'), 'a_cust' => t('a_customers'), 'a_regs' => t('a_regs'), 'a_set' => t('a_settings')];
    $h = '';
    foreach ($l as $r => $txt) $h .= '<a href="' . e(aurl($T, $r)) . '">' . e($txt) . '</a>';
    return $h . '<form method="post" action="' . e(aurl($T, 'a_logout')) . '" class="inl">' . csrf_field() . '<button class="link">' . e(t('log_out')) . '</button></form>';
}
function apage(Tenant $T, string $title, string $body): void {
    page(['client' => $T->client, 'title' => t('admin') . ' ' . $title, 'h1' => $title, 'body' => $body, 'area' => 'a', 'nav' => admin_nav($T), 'wide' => true]);
}
function admin_user(Tenant $T): ?array {
    if (empty($_SESSION['admin']) || (int) ($_SESSION['acid'] ?? 0) !== $T->id()) return null;
    $r = q("SELECT * FROM admins WHERE id=? AND client_id=? AND role='client_admin'", [(int) $_SESSION['admin'], $T->id()])->fetch();
    return $r ?: null;
}

function admin_route(Tenant $T, string $r): void {
    if ($r === 'a_login') { a_login($T); return; }
    $ad = admin_user($T);
    if (!$ad) redirect(aurl($T, 'a_login'));
    $actor = 'admin:' . $ad['id'];
    switch ($r) {
        case 'a': a_day($T); return;
        case 'a_week': a_week($T); return;
        case 'a_bk': a_booking($T, $actor); return;
        case 'a_move': a_move($T, $actor); return;
        case 'a_new': a_new($T, $actor); return;
        case 'a_cust': a_customers($T); return;
        case 'a_custv': a_customer($T, $actor); return;
        case 'a_regs': a_regs($T, $actor); return;
        case 'a_set': a_settings($T, $actor); return;
        case 'a_svc': a_service($T, $actor); return;
        case 'a_logout': if (is_post()) { require_post_ok(); session_end_all(); } redirect(aurl($T, 'a_login')); return;
    }
    http_response_code(404); apage($T, t('not_found'), '');
}

function a_login(Tenant $T): void {
    $errs = []; $u = '';
    if (is_post()) {
        require_post_ok();
        $u = in_str('username', 60); $p = (string) ($_POST['password'] ?? '');
        if (!rate_hit('a_login', 20, 900)) $errs[] = t('err_rate');
        else {
            $ad = $T->adminByUsername($u);
            if ($ad && !is_locked($ad['locked_until']) && password_verify($p, $ad['password_hash'])) {
                admin_ok((int) $ad['id']);
                session_regen();
                $_SESSION['acid'] = $T->id(); $_SESSION['admin'] = (int) $ad['id'];
                audit($T->id(), 'admin:' . $ad['id'], 'admin_login');
                redirect(aurl($T));
            }
            if ($ad) { admin_fail((int) $ad['id']); audit($T->id(), 'admin:' . $ad['id'], 'admin_login_fail'); }
            else password_verify($p, '$2y$10$abcdefghijklmnopqrstuuJ3D1Ga8iUqH2uP7l1dYlQ3yJ5v4zCq');
            $errs[] = t('a_login_err');
        }
    }
    $h = errors_html($errs) . '<form method="post" class="card form">' . csrf_field()
        . field('username', t('username'), ['autocomplete' => 'username', 'value' => $u, 'required' => 1])
        . field('password', t('password'), ['type' => 'password', 'autocomplete' => 'current-password', 'required' => 1])
        . '<button class="btn big">' . e(t('log_in')) . '</button></form>';
    page(['client' => $T->client, 'title' => t('admin'), 'h1' => t('admin') . ' ' . t('log_in'), 'body' => $h, 'area' => 'a']);
}

function day_bounds(array $ctx, string $date): array { return [local_ts($ctx, $date, 0), local_ts($ctx, $date, 1440)]; }
function valid_date(string $d, array $ctx): string { return preg_match('/^\d{4}-\d{2}-\d{2}$/', $d) ? $d : today_local($ctx); }

function bk_line(Tenant $T, array $ctx, array $b): string {
    $s = db_ts($b['start_at']); $e = db_ts($b['end_at']);
    $m = $b['mobile_e164'];
    return '<li class="arow st-' . e($b['status']) . '"><a class="arow-main" href="' . e(aurl($T, 'a_bk', ['id' => $b['id']])) . '">'
        . '<span class="at">' . e(fmt_local($ctx, $s, 'g:i a')) . '<small>' . e(fmt_local($ctx, $e, 'g:i a')) . '</small></span>'
        . '<span class="ab"><b>' . e($b['customer_name']) . '</b> <span class="tag">' . e(status_label($b['status'])) . '</span><br>' . e($b['service_name']) . ' <span class="muted">(' . e(dur_label(['full_day' => 0, 'duration_min' => intdiv($e - $s, 60)])) . ')</span>'
        . ($b['note'] !== '' ? '<br><span class="muted">' . e($b['note']) . '</span>' : '') . '</span></a>'
        . '<span class="ac"><a class="btn ghost sm" href="tel:' . e($m) . '">' . e(t('a_call')) . '</a><a class="btn ghost sm" href="' . e(wa_link($m)) . '" target="_blank" rel="noopener">' . e(t('a_wa')) . '</a><span class="mob">' . e($m) . '</span></span></li>';
}

function date_nav(Tenant $T, string $r, string $date, int $stepDays): string {
    $d = new DateTimeImmutable($date);
    return '<form method="get" class="dnav" action="' . e(aurl($T, $r)) . '"><input type="hidden" name="r" value="' . e($r) . '">'
        . '<a class="btn ghost sm" href="' . e(aurl($T, $r, ['d' => $d->modify("-$stepDays day")->format('Y-m-d')])) . '" aria-label="Previous">&lsaquo;</a>'
        . '<input type="date" name="d" value="' . e($date) . '" aria-label="' . e(t('date')) . '"><button class="btn sm">' . e(t('a_go')) . '</button>'
        . '<a class="btn ghost sm" href="' . e(aurl($T, $r, ['d' => $d->modify("+$stepDays day")->format('Y-m-d')])) . '" aria-label="Next">&rsaquo;</a>'
        . '<a class="btn ghost sm" href="' . e(aurl($T, $r)) . '">' . e(t('a_today')) . '</a></form>';
}

function a_day(Tenant $T): void {
    $ctx = ctx_for($T);
    $date = valid_date(q_str('d', 10), $ctx);
    [$a, $b] = day_bounds($ctx, $date);
    $list = $T->bookingsBetween(gmdate('Y-m-d H:i:s', $a), gmdate('Y-m-d H:i:s', $b));
    $h = (!client_bookable($T) ? '<p class="flash warn">' . e(t('a_hours_needed')) . '</p>' : '') . date_nav($T, 'a', $date, 1)
        . '<h2>' . e((new DateTimeImmutable($date))->format('l j M Y')) . '</h2>';
    $h .= $list ? '<ul class="alist">' . implode('', array_map(fn($x) => bk_line($T, $ctx, $x), $list)) . '</ul>' : '<p class="muted">' . e(t('a_none_day')) . '</p>';
    apage($T, t('a_day'), $h);
}

function a_week(Tenant $T): void {
    $ctx = ctx_for($T);
    $date = valid_date(q_str('d', 10), $ctx);
    $mon = (new DateTimeImmutable($date))->modify('monday this week');
    [$a] = day_bounds($ctx, $mon->format('Y-m-d'));
    [, $b] = day_bounds($ctx, $mon->modify('+6 day')->format('Y-m-d'));
    $by = [];
    foreach ($T->bookingsBetween(gmdate('Y-m-d H:i:s', $a), gmdate('Y-m-d H:i:s', $b)) as $x) $by[local_date($ctx, db_ts($x['start_at']))][] = $x;
    $h = date_nav($T, 'a_week', $mon->format('Y-m-d'), 7) . '<div class="week">';
    for ($i = 0; $i < 7; $i++) {
        $d = $mon->modify("+$i day")->format('Y-m-d');
        $h .= '<section class="wday"><h3><a href="' . e(aurl($T, 'a', ['d' => $d])) . '">' . e((new DateTimeImmutable($d))->format('D j M')) . '</a></h3>';
        $h .= !empty($by[$d]) ? '<ul class="alist">' . implode('', array_map(fn($x) => bk_line($T, $ctx, $x), $by[$d])) . '</ul>' : '<p class="muted small">-</p>';
        $h .= '</section>';
    }
    apage($T, t('a_week'), $h . '</div>');
}

function a_booking(Tenant $T, string $actor): void {
    $b = $T->booking(in_int('id'));
    if (!$b) redirect(aurl($T));
    $ctx = ctx_for($T);
    if (is_post()) {
        require_post_ok();
        $act = in_str('act', 20);
        try {
            if ($act === 'done' || $act === 'no_show' || $act === 'confirmed') { $T->setStatus((int) $b['id'], $act); audit($T->id(), $actor, 'status_' . $act, $b['ref']); }
            elseif ($act === 'cancel' || $act === 'cancel_series') { foreach (cancel_bookings($T, $b, $act === 'cancel_series', true) as $r) audit($T->id(), $actor, 'cancel', $r); }
            flash(t('a_saved'));
        } catch (DomainException $ex) { flash(problem_text($ex->getMessage()), 'err'); }
        redirect(aurl($T, 'a_bk', ['id' => $b['id']]));
    }
    $m = $b['mobile_e164'];
    $h = '<div class="card">' . booking_rows($ctx, $b) . '<dl class="kv"><dt>' . e(t('name')) . '</dt><dd><a href="' . e(aurl($T, 'a_custv', ['id' => $b['customer_id']])) . '">' . e($b['customer_name']) . '</a></dd>'
        . '<dt>' . e(t('mobile')) . '</dt><dd><a href="tel:' . e($m) . '">' . e($m) . '</a> <a href="' . e(wa_link($m)) . '" target="_blank" rel="noopener">' . e(t('a_wa')) . '</a></dd>'
        . '<dt>' . e(t('status')) . '</dt><dd>' . e(status_label($b['status'])) . '</dd>'
        . ($b['note'] !== '' ? '<dt>' . e(t('note')) . '</dt><dd>' . e($b['note']) . '</dd>' : '') . '</dl></div>';
    $btn = fn($act, $label, $cls = 'ghost') => '<form method="post" class="inl">' . csrf_field() . '<input type="hidden" name="act" value="' . $act . '"><button class="btn ' . $cls . '">' . e($label) . '</button></form>';
    $h .= '<div class="acts wrap-acts">';
    if ($b['status'] === 'confirmed') {
        $h .= '<a class="btn" href="' . e(aurl($T, 'a_move', ['id' => $b['id']])) . '">' . e(t('a_move')) . '</a>' . $btn('done', t('a_done')) . $btn('no_show', t('a_noshow')) . $btn('cancel', t('a_cancel'), 'ghost danger');
        if ($b['series_id']) $h .= $btn('cancel_series', t('a_cancel_series'), 'ghost danger');
    } elseif (in_array($b['status'], ['done', 'no_show'], true)) $h .= $btn('confirmed', t('st_confirmed'));
    apage($T, $b['ref'], $h . '</div>');
}

function a_move(Tenant $T, string $actor): void {
    $b = $T->booking(in_int('id'));
    if (!$b || $b['status'] !== 'confirmed') redirect(aurl($T));
    $ctx = ctx_for($T, ['ignore_notice' => true]);
    $svc = $T->service((int) $b['service_id']);
    $busy = busy_fn($T, (int) $b['id']);
    $errs = [];
    if (is_post()) {
        require_post_ok();
        try {
            $new = in_int('t');
            if ($b['series_id'] && in_str('scope', 10) === 'later') reschedule_series($T, $b, $new, true); else reschedule($T, $b, $new, true);
            audit($T->id(), $actor, 'reschedule', $b['ref']);
            flash(t('moved', ['ref' => $b['ref'], 'when' => fmt_local($ctx, $new, 'D j M, g:i a')]));
            redirect(aurl($T, 'a_bk', ['id' => $b['id']]));
        } catch (DomainException $ex) { $errs[] = problem_text($ex->getMessage()); }
    }
    $sel = in_int('t');
    if ($sel && !$errs) {
        $h = '<form method="post" class="card form">' . csrf_field() . '<input type="hidden" name="t" value="' . $sel . '"><p><b>' . e($b['ref']) . '</b>: ' . e(fmt_local($ctx, $sel, 'D j M Y, g:i a')) . '</p>'
            . ($b['series_id'] ? '<fieldset class="seg col"><legend>' . e(t('move_scope')) . '</legend><label><input type="radio" name="scope" value="one" checked><span>' . e(t('this_only')) . '</span></label><label><input type="radio" name="scope" value="later"><span>' . e(t('this_and_later')) . '</span></label></fieldset>' : '')
            . '<button class="btn big">' . e(t('a_move')) . '</button></form>';
        apage($T, t('a_move'), $h); return;
    }
    $strip = date_strip($ctx, $svc, $busy);
    $d = q_str('d', 10); if (!isset($strip[$d]) || $strip[$d] !== 'open') $d = first_open($strip);
    $slots = []; if ($d !== '') { $w = day_window($ctx, $d); $slots = is_array($w) ? slots_for_date($ctx, $svc, $d, $busy($w[0], $w[1])) : []; }
    apage($T, t('a_move') . ' ' . $b['ref'], errors_html($errs) . picker_html($ctx, $svc, $strip, $d, $slots, fn($x) => aurl($T, 'a_move', ['id' => $b['id'], 'd' => $x]), fn($s) => aurl($T, 'a_move', ['id' => $b['id'], 't' => $s])));
}

function a_new(Tenant $T, string $actor): void {
    $errs = [];
    $st = $_SESSION['anew'] ?? null;
    if ($st && (int) $st['cid'] !== $T->id()) $st = null;
    $ov = !empty($_GET['ov']) || !empty($_POST['ov']);
    if (is_post()) {
        require_post_ok();
        $act = in_str('act', 10);
        if ($act === 'cust') {
            $e164 = normalise_mobile(in_str('mobile', 30)); $name = in_str('name', 120); $svc = $T->service(in_int('service'));
            if (!$e164) $errs[] = t('err_mobile');
            if (!$svc || !(service_minutes($svc) || $svc['full_day'])) $errs[] = t('a_err_required');
            if (!$errs) {
                $cu = $T->customerByMobile($e164);
                if (!$cu) {
                    if ($name === '') $errs[] = t('err_name');
                    else { $id = $T->createCustomer($e164, $name, null, 'admin'); audit($T->id(), $actor, 'customer_create', '', mask_mobile($e164)); $cu = $T->customer($id); }
                }
                if ($cu) { $_SESSION['anew'] = ['cid' => $T->id(), 'cust' => (int) $cu['id'], 'svc' => (int) $svc['id']]; redirect(aurl($T, 'a_new', $ov ? ['ov' => 1] : [])); }
            }
        } elseif ($act === 'book' && $st) {
            $svc = $T->service((int) $st['svc']); $cu = $T->customer((int) $st['cust']);
            try {
                $ref = book_one($T, $svc, (int) $cu['id'], in_int('t'), in_str('note', 500), 'admin', ['ignore_notice' => $ov], null, (bool) $cu['is_test']);
                audit($T->id(), $actor, 'book', $ref);
                unset($_SESSION['anew']);
                $b = $T->bookingByRef($ref);
                flash(t('confirmed_title') . ': ' . $ref);
                redirect(aurl($T, 'a_bk', ['id' => $b['id']]));
            } catch (DomainException $ex) { $errs[] = problem_text($ex->getMessage()); }
        } elseif ($act === 'reset') { unset($_SESSION['anew']); redirect(aurl($T, 'a_new')); }
    }
    if (!$st || !empty($errs) && in_str('act', 10) === 'cust') {
        $opts = '';
        foreach ($T->services(false) as $s) $opts .= '<option value="' . (int) $s['id'] . '">' . e($s['name'] . ($s['active'] ? '' : ' (off)')) . '</option>';
        $h = errors_html($errs) . '<form method="post" class="card form">' . csrf_field() . '<input type="hidden" name="act" value="cust">'
            . field('mobile', t('a_find_or_new'), ['type' => 'tel', 'inputmode' => 'tel', 'required' => 1, 'hint' => t('mobile_hint')])
            . field('name', t('name'), ['hint' => t('a_new_cust_note')])
            . '<label for="f_service">' . e(t('service')) . '</label><select id="f_service" name="service">' . $opts . '</select>'
            . check('ov', t('a_override'), $ov) . '<button class="btn big">' . e(t('continue')) . '</button></form>';
        apage($T, t('a_new'), $h); return;
    }
    $svc = $T->service((int) $st['svc']); $cu = $T->customer((int) $st['cust']);
    $ctx = ctx_for($T, ['ignore_notice' => $ov]);
    $busy = busy_fn($T);
    $head = '<div class="card"><b>' . e($cu['name']) . '</b> ' . e($cu['mobile_e164']) . '<br>' . e($svc['name']) . ' (' . e(dur_label($svc)) . ')'
        . '<form method="post" class="inl">' . csrf_field() . '<input type="hidden" name="act" value="reset"><button class="link">' . e(t('change')) . '</button></form></div>';
    $sel = in_int('t');
    if ($sel && !$errs) {
        $h = $head . '<form method="post" class="card form">' . csrf_field() . '<input type="hidden" name="act" value="book"><input type="hidden" name="t" value="' . $sel . '">' . ($ov ? '<input type="hidden" name="ov" value="1">' : '')
            . '<p><b>' . e(fmt_local($ctx, $sel, 'D j M Y, g:i a')) . '</b></p>' . field('note', t('note'), ['type' => 'textarea', 'maxlength' => 500]) . '<button class="btn big">' . e(t('confirm')) . '</button></form>';
        apage($T, t('a_new'), $h); return;
    }
    $strip = date_strip($ctx, $svc, $busy);
    $d = q_str('d', 10); if (!isset($strip[$d]) || $strip[$d] !== 'open') $d = first_open($strip);
    $slots = []; if ($d !== '') { $w = day_window($ctx, $d); $slots = is_array($w) ? slots_for_date($ctx, $svc, $d, $busy($w[0], $w[1])) : []; }
    $x = $ov ? ['ov' => 1] : [];
    apage($T, t('a_new'), $head . errors_html($errs) . ($d === '' ? '<p class="muted">' . e(t('no_dates')) . '</p>' :
        picker_html($ctx, $svc, $strip, $d, $slots, fn($v) => aurl($T, 'a_new', $x + ['d' => $v]), fn($s) => aurl($T, 'a_new', $x + ['t' => $s]))));
}

function cust_row(Tenant $T, array $c): string {
    return '<li class="crow"><a href="' . e(aurl($T, 'a_custv', ['id' => $c['id']])) . '"><b>' . e($c['name']) . '</b> <span class="mob">' . e($c['mobile_e164']) . '</span></a>'
        . '<span class="tag">' . e(t('a_rev_' . $c['review'])) . '</span>' . ($c['pin_hash'] === null ? '<span class="tag">' . e(t('a_unclaimed')) . '</span>' : '') . ($c['is_test'] ? '<span class="tag">test</span>' : '') . '</li>';
}

function a_customers(Tenant $T): void {
    $qv = is_post() ? (require_post_ok() ?? in_str('q', 20)) : '';
    $list = $T->searchCustomers($qv);
    $h = '<form method="post" class="dnav" role="search">' . csrf_field() . '<input type="search" name="q" inputmode="tel" value="' . e($qv) . '" aria-label="' . e(t('a_search')) . '" placeholder="' . e(t('a_search')) . '"><button class="btn sm">' . e(t('a_go')) . '</button></form>'
        . '<ul class="clist">' . implode('', array_map(fn($c) => cust_row($T, $c), $list)) . '</ul>';
    apage($T, t('a_customers'), $h);
}

function a_regs(Tenant $T, string $actor): void {
    if (is_post()) {
        require_post_ok();
        $cu = $T->customer(in_int('id'));
        $rv = in_str('review', 10);
        if ($cu && in_array($rv, ['approved', 'flagged'], true)) { $T->setReview((int) $cu['id'], $rv); audit($T->id(), $actor, 'review_' . $rv, '', 'cust:' . $cu['id']); }
        redirect(aurl($T, 'a_regs'));
    }
    $h = '<p class="muted">' . e(t('a_flagged_note')) . '</p><ul class="clist">';
    foreach ($T->newRegistrations() as $c) {
        $h .= '<li class="crow"><a href="' . e(aurl($T, 'a_custv', ['id' => $c['id']])) . '"><b>' . e($c['name']) . '</b> <span class="mob">' . e($c['mobile_e164']) . '</span></a><span class="acts">';
        foreach (['approved' => t('a_approve'), 'flagged' => t('a_flag')] as $k => $l)
            $h .= '<form method="post" class="inl">' . csrf_field() . '<input type="hidden" name="id" value="' . (int) $c['id'] . '"><input type="hidden" name="review" value="' . $k . '"><button class="btn ghost sm">' . e($l) . '</button></form>';
        $h .= '</span></li>';
    }
    apage($T, t('a_regs'), $h . '</ul>');
}

function a_customer(Tenant $T, string $actor): void {
    $cu = $T->customer(in_int('id'));
    if (!$cu) redirect(aurl($T, 'a_cust'));
    if (is_post()) {
        require_post_ok();
        $act = in_str('act', 12);
        if ($act === 'reset') { $T->resetPin((int) $cu['id']); audit($T->id(), $actor, 'pin_reset', '', 'cust:' . $cu['id']); flash(t('a_pin_reset_done')); }
        elseif (in_array($act, ['approved', 'flagged'], true)) { $T->setReview((int) $cu['id'], $act); audit($T->id(), $actor, 'review_' . $act, '', 'cust:' . $cu['id']); flash(t('a_saved')); }
        redirect(aurl($T, 'a_custv', ['id' => $cu['id']]));
    }
    $ctx = ctx_for($T);
    $m = $cu['mobile_e164'];
    $f = fn($act, $l, $cls = 'ghost') => '<form method="post" class="inl">' . csrf_field() . '<input type="hidden" name="act" value="' . $act . '"><button class="btn ' . $cls . ' sm">' . e($l) . '</button></form>';
    $h = '<div class="card"><p><b>' . e($cu['name']) . '</b><br><a href="tel:' . e($m) . '">' . e($m) . '</a> <a href="' . e(wa_link($m)) . '" target="_blank" rel="noopener">' . e(t('a_wa')) . '</a></p>'
        . '<p><span class="tag">' . e(t('a_rev_' . $cu['review'])) . '</span>' . ($cu['pin_hash'] === null ? ' <span class="tag">' . e(t('a_unclaimed')) . '</span>' : '') . '</p>'
        . '<div class="acts wrap-acts">' . $f('approved', t('a_approve')) . $f('flagged', t('a_flag')) . $f('reset', t('a_reset_pin'), 'ghost danger') . '</div><small class="muted">' . e(t('a_reset_pin_note')) . '</small></div>'
        . '<h2>' . e(t('a_history')) . '</h2><ul class="alist">';
    foreach ($T->customerBookings((int) $cu['id']) as $b) $h .= bk_line($T, $ctx, $b);
    apage($T, $cu['name'], $h . '</ul>');
}

/* ---------- settings ---------- */
function time_ok(string $t): ?string { return preg_match('/^([01]\d|2[0-3]):[0-5]\d$|^24:00$/', $t) ? $t . ':00' : null; }
function int_in(string $k, int $min, int $max, int $def): int { $v = isset($_POST[$k]) ? (int) $_POST[$k] : $def; return max($min, min($max, $v)); }

function a_settings(Tenant $T, string $actor): void {
    $tab = q_str('tab', 10) ?: 'services';
    $c = $T->client;
    $errs = [];
    if (is_post()) {
        require_post_ok();
        if ($tab === 'hours') {
            $rows = [];
            for ($wd = 1; $wd <= 7; $wd++) {
                $closed = !empty($_POST['closed'][$wd]);
                $o = time_ok((string) ($_POST['open'][$wd] ?? '')); $cl = time_ok((string) ($_POST['close'][$wd] ?? ''));
                if (!$closed && (!$o || !$cl || time_to_min($cl) <= time_to_min($o))) { $errs[] = t('a_err_required') . ' (' . (new DateTimeImmutable('monday this week'))->modify('+' . ($wd - 1) . ' day')->format('D') . ')'; continue; }
                $rows[$wd] = ['open_time' => $closed ? null : $o, 'close_time' => $closed ? null : $cl, 'closed' => $closed];
            }
            if (!$errs) {
                $T->saveHours($rows); audit($T->id(), $actor, 'hours_save');
                if ($c['status'] === 'setup' && has_open_hours($T->hours())) { $T->setStatus_('live'); audit($T->id(), $actor, 'status_live'); }
            }
        } elseif ($tab === 'off') {
            if (in_str('act', 10) === 'remove') { $T->removeOffDay(in_int('id')); }
            else {
                $s = in_str('start', 10); $e = in_str('end', 10) ?: $s;
                if (!preg_match('/^\d{4}-\d{2}-\d{2}$/', $s) || !preg_match('/^\d{4}-\d{2}-\d{2}$/', $e) || $e < $s) $errs[] = t('a_err_required');
                else { $T->addOffDay($s, $e, in_str('reason', 160)); audit($T->id(), $actor, 'offday_add'); }
            }
        } elseif ($tab === 'rules') {
            $T->updateRules(['slot_step_min' => int_in('slot_step_min', 5, 240, 30), 'max_days_ahead' => int_in('max_days_ahead', 1, 365, 60), 'min_notice_min' => int_in('min_notice_min', 0, 20160, 120),
                'cancel_cutoff_min' => int_in('cancel_cutoff_min', 0, 20160, 720), 'capacity' => int_in('capacity', 1, 20, 1), 'max_repeats' => int_in('max_repeats', 2, 52, 12)]);
            audit($T->id(), $actor, 'rules_save');
        } elseif ($tab === 'brand') {
            $wa = normalise_mobile(in_str('whatsapp_e164', 30)) ?? '';
            $logo = in_str('logo_url', 500);
            if ($logo !== '' && !preg_match('#^(https://|/)[^\s"<>]+$#', $logo)) $errs[] = t('a_b_logo');
            if (in_str('name', 120) === '') $errs[] = t('a_b_name');
            if (!$errs) {
                $T->updateBranding(['name' => in_str('name', 120), 'logo_url' => $logo, 'colour_primary' => hex_ok(in_str('colour_primary', 7), $c['colour_primary']),
                    'colour_accent' => hex_ok(in_str('colour_accent', 7), $c['colour_accent']), 'colour_bg' => hex_ok(in_str('colour_bg', 7), $c['colour_bg']), 'whatsapp_e164' => $wa]);
                audit($T->id(), $actor, 'brand_save');
            }
        }
        if (!$errs) { flash(t('a_saved')); redirect(aurl($T, 'a_set', ['tab' => $tab])); }
        $T->reload(); $c = $T->client;
    }
    $tabs = '<nav class="tabs">';
    foreach (['services' => t('a_services'), 'hours' => t('a_hours'), 'off' => t('a_off'), 'rules' => t('a_rules'), 'brand' => t('a_brand')] as $k => $l)
        $tabs .= '<a href="' . e(aurl($T, 'a_set', ['tab' => $k])) . '"' . ($k === $tab ? ' aria-current="page"' : '') . '>' . e($l) . '</a>';
    $h = $tabs . '</nav>' . errors_html($errs);
    $form = fn($inner) => '<form method="post" class="card form" action="' . e(aurl($T, 'a_set', ['tab' => $tab])) . '">' . csrf_field() . $inner . '<button class="btn big">' . e(t('a_save')) . '</button></form>';
    if ($tab === 'services') {
        $h .= '<p><a class="btn" href="' . e(aurl($T, 'a_svc')) . '">' . e(t('a_add_service')) . '</a></p><ul class="clist">';
        foreach ($T->services(false) as $s)
            $h .= '<li class="crow"><a href="' . e(aurl($T, 'a_svc', ['id' => $s['id']])) . '"><b>' . e($s['name']) . '</b> <span class="muted">' . e(implode(' / ', array_filter([dur_label($s), price_label($s)]))) . '</span></a>'
                . '<span class="tag">' . e($s['active'] ? t('a_open') : 'off') . '</span>' . ($s['admin_note'] !== '' ? '<small class="muted">' . e($s['admin_note']) . '</small>' : '') . '</li>';
        $h .= '</ul>';
    } elseif ($tab === 'hours') {
        $hrs = $T->hours();
        $in = (!has_open_hours($hrs) ? '<p class="flash warn">' . e(t('a_hours_needed')) . '</p>' : '') . '<div class="hours">';
        for ($wd = 1; $wd <= 7; $wd++) {
            $r = $hrs[$wd] ?? ['open_time' => null, 'close_time' => null, 'closed' => 1];
            $dn = (new DateTimeImmutable('monday this week'))->modify('+' . ($wd - 1) . ' day')->format('l');
            $in .= '<fieldset class="hrow"><legend>' . e($dn) . '</legend>'
                . '<label>' . e(t('a_open')) . ' <input type="time" name="open[' . $wd . ']" value="' . e(substr((string) $r['open_time'], 0, 5)) . '" step="300"></label>'
                . '<label>' . e(t('a_close')) . ' <input type="time" name="close[' . $wd . ']" value="' . e(substr((string) $r['close_time'], 0, 5)) . '" step="300"></label>'
                . check('closed[' . $wd . ']', t('a_closed'), (bool) $r['closed'], 'cl' . $wd) . '</fieldset>';
        }
        $h .= $form($in . '</div>');
    } elseif ($tab === 'off') {
        $h .= $form(field('start', t('a_off_from'), ['type' => 'date', 'required' => 1]) . field('end', t('a_off_to'), ['type' => 'date']) . field('reason', t('a_off_reason'), ['maxlength' => 160]));
        $h .= '<ul class="clist">';
        foreach ($T->offDays(today_local(ctx_for($T))) as $o)
            $h .= '<li class="crow"><span>' . e($o['start_date'] . ($o['end_date'] !== $o['start_date'] ? ' to ' . $o['end_date'] : '')) . ' <span class="muted">' . e($o['reason']) . '</span></span>'
                . '<form method="post" class="inl" action="' . e(aurl($T, 'a_set', ['tab' => 'off'])) . '">' . csrf_field() . '<input type="hidden" name="act" value="remove"><input type="hidden" name="id" value="' . (int) $o['id'] . '"><button class="btn ghost sm">' . e(t('a_remove')) . '</button></form></li>';
        $h .= '</ul>';
    } elseif ($tab === 'rules') {
        $num = fn($k, $l, $min, $max) => field($k, $l, ['type' => 'number', 'inputmode' => 'numeric', 'min' => $min, 'max' => $max, 'value' => (string) $c[$k], 'required' => 1]);
        $h .= $form($num('slot_step_min', t('a_r_step'), 5, 240) . $num('max_days_ahead', t('a_r_ahead'), 1, 365) . $num('min_notice_min', t('a_r_notice'), 0, 20160)
            . $num('cancel_cutoff_min', t('a_r_cutoff'), 0, 20160) . $num('capacity', t('a_r_cap'), 1, 20) . $num('max_repeats', t('a_r_rep'), 2, 52));
    } elseif ($tab === 'brand') {
        $h .= $form(field('name', t('a_b_name'), ['value' => $c['name'], 'required' => 1]) . field('logo_url', t('a_b_logo'), ['type' => 'url', 'value' => $c['logo_url']])
            . field('colour_primary', t('a_b_primary'), ['type' => 'color', 'value' => $c['colour_primary']]) . field('colour_accent', t('a_b_accent'), ['type' => 'color', 'value' => $c['colour_accent']])
            . field('colour_bg', t('a_b_bg'), ['type' => 'color', 'value' => $c['colour_bg']]) . field('whatsapp_e164', t('a_b_wa'), ['type' => 'tel', 'value' => $c['whatsapp_e164']]));
    }
    apage($T, t('a_settings'), $h);
}

function a_service(Tenant $T, string $actor): void {
    $id = in_int('id');
    $s = $id ? $T->service($id) : null;
    if ($id && !$s) redirect(aurl($T, 'a_set'));
    $errs = [];
    if (is_post()) {
        require_post_ok();
        $full = !empty($_POST['full_day']);
        $dur = in_int('duration_min');
        $priceRaw = in_str('price', 12);
        $row = ['id' => $id, 'slug' => '', 'group_slug' => $s['group_slug'] ?? '', 'name' => in_str('name', 160), 'description' => in_str('description', 1000),
            'duration_min' => $dur > 0 ? min($dur, 1440) : null, 'full_day' => $full ? 1 : 0, 'price' => $priceRaw === '' ? null : (string) round((float) $priceRaw, 2),
            'price_note' => in_str('price_note', 200), 'recurring_allowed' => empty($_POST['recurring_allowed']) ? 0 : 1, 'active' => empty($_POST['active']) ? 0 : 1, 'sort_order' => in_int('sort_order')];
        if ($row['name'] === '' || $row['description'] === '' || (!$full && !$row['duration_min'])) $errs[] = t('a_err_required');
        if (!$errs) { $T->saveService($row); audit($T->id(), $actor, $id ? 'service_edit' : 'service_add'); flash(t('a_saved')); redirect(aurl($T, 'a_set')); }
        $s = $row;
    }
    $s = $s ?? ['name' => '', 'description' => '', 'duration_min' => '', 'full_day' => 0, 'price' => '', 'price_note' => '', 'recurring_allowed' => 0, 'active' => 0, 'sort_order' => 0];
    $h = errors_html($errs) . '<form method="post" class="card form">' . csrf_field()
        . field('name', t('a_svc_name') . ' *', ['value' => $s['name'], 'required' => 1]) . field('description', t('a_svc_desc') . ' *', ['type' => 'textarea', 'value' => $s['description'], 'required' => 1])
        . field('duration_min', t('a_svc_dur') . ' *', ['type' => 'number', 'inputmode' => 'numeric', 'min' => 5, 'max' => 1440, 'value' => (string) $s['duration_min']])
        . check('full_day', t('a_svc_full'), (bool) $s['full_day'])
        . field('price', t('a_svc_price'), ['type' => 'number', 'step' => '0.01', 'min' => 0, 'value' => (string) $s['price']]) . field('price_note', t('a_svc_price_note'), ['value' => $s['price_note'], 'maxlength' => 200])
        . check('recurring_allowed', t('a_svc_rec'), (bool) $s['recurring_allowed']) . check('active', t('a_svc_active'), (bool) $s['active'])
        . field('sort_order', t('a_svc_sort'), ['type' => 'number', 'value' => (string) $s['sort_order']])
        . '<button class="btn big">' . e(t('a_save')) . '</button></form>';
    apage($T, $id ? $s['name'] : t('a_add_service'), $h);
}
