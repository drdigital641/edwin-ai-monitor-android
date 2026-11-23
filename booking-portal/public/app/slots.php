<?php
/* THE slot engine. One set of pure functions used by the customer flow, admin flow, reschedules and
   recurring previews. No database access here: callers pass rules, hours, off days and busy intervals. */
declare(strict_types=1);
if (!defined('P1B')) { http_response_code(404); exit; }

/** $ctx = ['tz','step','max_days','notice','capacity','hours'=>[wd=>row],'off'=>[[start,end],...],'now'=>ts,
 *          'ignore_notice'=>bool,'ignore_cutoff'=>bool] */
function engine_ctx(array $client, array $hours, array $offDays, ?int $now = null, array $opts = []): array {
    return [
        'tz' => new DateTimeZone($client['timezone'] ?: 'Asia/Singapore'),
        'step' => max(5, (int) $client['slot_step_min']),
        'max_days' => (int) $client['max_days_ahead'],
        'notice' => (int) $client['min_notice_min'],
        'capacity' => max(1, (int) $client['capacity']),
        'cutoff' => (int) $client['cancel_cutoff_min'],
        'hours' => $hours,
        'off' => array_map(fn($o) => [$o['start_date'], $o['end_date']], $offDays),
        'now' => $now ?? time(),
        'ignore_notice' => !empty($opts['ignore_notice']),
    ];
}

function time_to_min(?string $t): ?int {
    if ($t === null || $t === '') return null;
    if (!preg_match('/^(\d{1,2}):(\d{2})/', $t, $m)) return null;
    return (int) $m[1] * 60 + (int) $m[2];
}

/** local date string for a timestamp */
function local_date(array $ctx, int $ts): string { return (new DateTimeImmutable('@' . $ts))->setTimezone($ctx['tz'])->format('Y-m-d'); }
function today_local(array $ctx): string { return local_date($ctx, $ctx['now']); }
function local_ts(array $ctx, string $date, int $minutes): int {
    $d = new DateTimeImmutable($date . ' 00:00:00', $ctx['tz']);
    return $d->modify('+' . $minutes . ' minutes')->getTimestamp();
}
function is_off_day(array $ctx, string $date): bool {
    foreach ($ctx['off'] as [$s, $e]) if ($date >= $s && $date <= $e) return true;
    return false;
}
function has_open_hours(array $hours): bool {
    foreach ($hours as $h) if (!$h['closed'] && time_to_min($h['open_time']) !== null && time_to_min($h['close_time']) > time_to_min($h['open_time'])) return true;
    return false;
}

/** [openTs, closeTs] for that local date, or a reason string */
function day_window(array $ctx, string $date) {
    $wd = (int) (new DateTimeImmutable($date, $ctx['tz']))->format('N');
    $h = $ctx['hours'][$wd] ?? null;
    if (!$h || $h['closed']) return 'closed';
    $o = time_to_min($h['open_time']); $c = time_to_min($h['close_time']);
    if ($o === null || $c === null || $c <= $o) return 'closed';
    if (is_off_day($ctx, $date)) return 'off';
    return [local_ts($ctx, $date, $o), local_ts($ctx, $date, $c)];
}

/** minutes the service blocks on a given window (full_day = the whole open window) */
function service_minutes(array $service, ?array $win = null): ?int {
    if (!empty($service['full_day'])) return $win ? intdiv($win[1] - $win[0], 60) : null;
    $d = $service['duration_min'] ?? null;
    return $d ? (int) $d : null;
}

/** can this service be booked online at all with these hours? false => "WhatsApp us to book this one" */
function service_fits_any_day(array $service, array $hours): bool {
    if (!empty($service['full_day'])) return has_open_hours($hours);
    $d = service_minutes($service);
    if (!$d) return false;
    foreach ($hours as $h) {
        if ($h['closed']) continue;
        $o = time_to_min($h['open_time']); $c = time_to_min($h['close_time']);
        if ($o !== null && $c !== null && $c - $o >= $d) return true;
    }
    return false;
}

/** most confirmed bookings running at the same minute inside [s,e) */
function peak_overlap(array $busy, int $s, int $e): int {
    $pts = [];
    foreach ($busy as $b) {
        $bs = max($s, $b[0]); $be = min($e, $b[1]);
        if ($bs < $be) { $pts[] = [$bs, 1]; $pts[] = [$be, -1]; }
    }
    usort($pts, fn($a, $b) => $a[0] <=> $b[0] ?: $a[1] <=> $b[1]);   // ends before starts at the same instant
    $cur = 0; $max = 0;
    foreach ($pts as $p) { $cur += $p[1]; $max = max($max, $cur); }
    return $max;
}

/** why a given start is not bookable (null = OK). The final word before every insert or move. */
function slot_problem(array $ctx, array $service, int $start, array $busy): ?string {
    $date = local_date($ctx, $start);
    $win = day_window($ctx, $date);
    if (!is_array($win)) return $win;                               // closed | off
    $dur = service_minutes($service, $win);
    if (!$dur) return 'no_duration';
    if (!empty($service['full_day']) && $start !== $win[0]) return 'not_a_slot';
    if ($start < $win[0] || ($start - $win[0]) % ($ctx['step'] * 60) !== 0) return 'not_a_slot';
    $end = $start + $dur * 60;
    if ($end > $win[1]) return 'too_late';                          // must end by closing
    if (!$ctx['ignore_notice'] && $start < $ctx['now'] + $ctx['notice'] * 60) return 'notice';
    if ($start < $ctx['now']) return 'past';
    $last = (new DateTimeImmutable(today_local($ctx), $ctx['tz']))->modify('+' . $ctx['max_days'] . ' days')->format('Y-m-d');
    if ($date > $last) return 'too_far';
    if (peak_overlap($busy, $start, $end) >= $ctx['capacity']) return 'full';
    return null;
}

/** every free start (UTC ts) on a local date */
function slots_for_date(array $ctx, array $service, string $date, array $busy): array {
    $win = day_window($ctx, $date);
    if (!is_array($win)) return [];
    $dur = service_minutes($service, $win);
    if (!$dur) return [];
    $out = [];
    $step = !empty($service['full_day']) ? PHP_INT_MAX : $ctx['step'] * 60;
    for ($s = $win[0]; $s + $dur * 60 <= $win[1]; $s += $step) {
        if (slot_problem($ctx, $service, $s, $busy) === null) $out[] = $s;
        if ($step === PHP_INT_MAX) break;
    }
    return $out;
}

/** the date strip: [date => 'open'|'closed'|'off'|'full'|'past'] from today to today+max_days */
function date_strip(array $ctx, array $service, callable $busyFor): array {
    $out = [];
    $d = new DateTimeImmutable(today_local($ctx), $ctx['tz']);
    for ($i = 0; $i <= $ctx['max_days']; $i++, $d = $d->modify('+1 day')) {
        $date = $d->format('Y-m-d');
        $win = day_window($ctx, $date);
        if (!is_array($win)) { $out[$date] = $win; continue; }
        $out[$date] = slots_for_date($ctx, $service, $date, $busyFor($win[0], $win[1])) ? 'open' : ($win[1] <= $ctx['now'] ? 'past' : 'full');
    }
    return $out;
}

/** first free start at or after $fromTs (same day later, then next days), within max_days */
function next_free(array $ctx, array $service, int $fromTs, callable $busyFor): ?int {
    $d = new DateTimeImmutable(local_date($ctx, max($fromTs, $ctx['now'])), $ctx['tz']);
    $last = (new DateTimeImmutable(today_local($ctx), $ctx['tz']))->modify('+' . $ctx['max_days'] . ' days')->format('Y-m-d');
    for (; $d->format('Y-m-d') <= $last; $d = $d->modify('+1 day')) {
        $win = day_window($ctx, $d->format('Y-m-d'));
        if (!is_array($win)) continue;
        foreach (slots_for_date($ctx, $service, $d->format('Y-m-d'), $busyFor($win[0], $win[1])) as $s) if ($s >= $fromTs) return $s;
    }
    return null;
}

/** the local date+time of repeat $i (0 = first). Monthly: same day of month, or the month's last day */
function repeat_start(array $ctx, int $firstTs, string $freq, int $i): array {
    $f = (new DateTimeImmutable('@' . $firstTs))->setTimezone($ctx['tz']);
    $hm = (int) $f->format('G') * 60 + (int) $f->format('i');
    if ($freq === 'weekly') { $date = $f->modify('+' . (7 * $i) . ' days')->format('Y-m-d'); return [$date, local_ts($ctx, $date, $hm), false]; }
    $y = (int) $f->format('Y'); $m = (int) $f->format('n') + $i; $day = (int) $f->format('j');
    $y += intdiv($m - 1, 12); $m = ($m - 1) % 12 + 1;
    $dim = (int) (new DateTimeImmutable(sprintf("%04d-%02d-01", $y, $m)))->format("t");
    $clamped = $day > $dim;
    $date = sprintf('%04d-%02d-%02d', $y, $m, min($day, $dim));
    return [$date, local_ts($ctx, $date, $hm), $clamped];
}

/** recurring preview: each item = [i, date, start, ok, problem, suggestion, last_day] */
function series_plan(array $ctx, array $service, int $firstTs, string $freq, int $count, callable $busyFor): array {
    $items = []; $taken = [];   // starts already planned in this series also block
    for ($i = 0; $i < $count; $i++) {
        [$date, $start, $clamped] = repeat_start($ctx, $firstTs, $freq, $i);
        $busy = fn($a, $b) => array_merge($busyFor($a, $b), $taken);
        $win = day_window($ctx, $date);
        $dur = service_minutes($service, is_array($win) ? $win : null) ?? 0;
        if (!empty($service['full_day']) && is_array($win)) $start = $win[0];
        $prob = slot_problem($ctx, $service, $start, $busy($start, $start + max(1, $dur) * 60));
        $sugg = null;
        if ($prob !== null) $sugg = next_free($ctx, $service, $start, $busy);
        $use = $prob === null ? $start : $sugg;
        if ($use !== null) {
            $w = day_window($ctx, local_date($ctx, $use));
            $taken[] = [$use, $use + (service_minutes($service, is_array($w) ? $w : null) ?? 0) * 60, 0];
        }
        $items[] = ['i' => $i, 'date' => $date, 'start' => $start, 'ok' => $prob === null, 'problem' => $prob, 'suggestion' => $sugg, 'last_day' => $clamped];
    }
    return $items;
}

/** may the customer still change this booking? (cut-off before the start) */
function before_cutoff(array $ctx, int $startTs): bool { return $startTs - $ctx['now'] >= $ctx['cutoff'] * 60; }

function fmt_local(array $ctx, int $ts, string $fmt): string { return (new DateTimeImmutable('@' . $ts))->setTimezone($ctx['tz'])->format($fmt); }
function db_ts(string $utc): int { return strtotime($utc . ' UTC'); }
