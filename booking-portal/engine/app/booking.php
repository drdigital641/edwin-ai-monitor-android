<?php
/* Booking actions shared by customer and admin flows. Every write that changes availability runs inside
   Tenant::withLock (SELECT ... FOR UPDATE on the client row) and re-checks the slot with slot_problem(). */
declare(strict_types=1);
if (!defined('P1B')) { http_response_code(404); exit; }

function ctx_for(Tenant $T, array $opts = [], ?int $now = null): array {
    return engine_ctx($T->client, $T->hours(), $T->offDays(gmdate('Y-m-d', time() - 86400 * 2)), $now, $opts);
}
function busy_fn(Tenant $T, int $excludeId = 0): callable { return fn(int $a, int $b) => $T->busy($a, $b, $excludeId); }

/** online booking open for this client? (paused, or no hours yet => WhatsApp us) */
function client_bookable(Tenant $T): bool {
    return $T->client['status'] !== 'paused' && has_open_hours($T->hours());
}

/** re-load service + customer through THIS tenant: rows from another client are refused */
function own_rows(Tenant $T, array $svc, int $customerId): array {
    $s = $T->service((int) $svc['id']);
    if (!$s || !$T->customer($customerId)) throw new DomainException('not_found');
    return $s;
}

function svc_block_minutes(array $ctx, array $svc, int $start): int {
    $w = day_window($ctx, local_date($ctx, $start));
    return (int) service_minutes($svc, is_array($w) ? $w : null);
}

/** book one slot; returns ref or throws DomainException(problem) */
function book_one(Tenant $T, array $svc, int $customerId, int $start, string $note, string $by, array $opts = [], ?int $seriesId = null, bool $isTest = false): string {
    $svc = own_rows($T, $svc, $customerId);
    return $T->withLock(function () use ($T, $svc, $customerId, $start, $note, $by, $opts, $seriesId, $isTest) {
        $ctx = ctx_for($T, $opts);
        $end = $start + svc_block_minutes($ctx, $svc, $start) * 60;
        $p = slot_problem($ctx, $svc, $start, $T->busy($start, max($end, $start + 60)));
        if ($p !== null) throw new DomainException($p);
        return $T->insertBooking($customerId, (int) $svc['id'], $start, $end, $note, $seriesId, $by, $isTest);
    });
}

/** book a series. $starts = list of chosen starts (skips already removed). All or nothing. Returns [ref...] */
function book_series(Tenant $T, array $svc, int $customerId, string $freq, array $starts, string $note, string $by, bool $isTest = false): array {
    $svc = own_rows($T, $svc, $customerId);
    return $T->withLock(function () use ($T, $svc, $customerId, $freq, $starts, $note, $by, $isTest) {
        $ctx = ctx_for($T);
        $sid = $T->createSeries($customerId, (int) $svc['id'], $freq, count($starts));
        $refs = [];
        foreach ($starts as $start) {
            $end = $start + svc_block_minutes($ctx, $svc, $start) * 60;
            $p = slot_problem($ctx, $svc, $start, $T->busy($start, max($end, $start + 60)));
            if ($p !== null) throw new DomainException($p . '@' . $start);
            $refs[] = $T->insertBooking($customerId, (int) $svc['id'], $start, $end, $note, $sid, $by, $isTest);
        }
        return $refs;
    });
}

/** move a booking (same ref). $asAdmin may override notice + cut-off, never capacity or hours */
function reschedule(Tenant $T, array $bk, int $newStart, bool $asAdmin): void {
    $T->withLock(function () use ($T, $bk, $newStart, $asAdmin) {
        $ctx = ctx_for($T, ['ignore_notice' => $asAdmin]);
        if ($bk['status'] !== 'confirmed') throw new DomainException('not_confirmed');
        if (!$asAdmin && !before_cutoff($ctx, db_ts($bk['start_at']))) throw new DomainException('cutoff');
        $svc = $T->service((int) $bk['service_id']);
        $end = $newStart + svc_block_minutes($ctx, $svc, $newStart) * 60;
        $p = slot_problem($ctx, $svc, $newStart, $T->busy($newStart, max($end, $newStart + 60), (int) $bk['id']));
        if ($p !== null) throw new DomainException($p);
        $T->moveBooking((int) $bk['id'], $newStart, $end);
    });
}

/** move this and every later booking in its series by the same shift. All or nothing. */
function reschedule_series(Tenant $T, array $bk, int $newStart, bool $asAdmin): int {
    return $T->withLock(function () use ($T, $bk, $newStart, $asAdmin) {
        $ctx = ctx_for($T, ['ignore_notice' => $asAdmin]);
        $shift = $newStart - db_ts($bk['start_at']);
        $list = array_values(array_filter($T->seriesBookings((int) $bk['series_id'], $bk['start_at']), fn($b) => $b['status'] === 'confirmed'));
        $svc = $T->service((int) $bk['service_id']);
        $ids = array_map(fn($b) => (int) $b['id'], $list);
        $planned = [];
        foreach ($list as $b) {
            if (!$asAdmin && !before_cutoff($ctx, db_ts($b['start_at']))) throw new DomainException('cutoff');
            $s = db_ts($b['start_at']) + $shift;
            $e = $s + svc_block_minutes($ctx, $svc, $s) * 60;
            $busy = array_merge(array_filter($T->busy($s, max($e, $s + 60)), fn($x) => !in_array($x[2], $ids, true)), $planned);
            $p = slot_problem($ctx, $svc, $s, $busy);
            if ($p !== null) throw new DomainException($p . '@' . $s);
            $planned[] = [$s, $e, 0];
        }
        foreach ($list as $i => $b) $T->moveBooking((int) $b['id'], $planned[$i][0], $planned[$i][1]);
        return count($list);
    });
}

/** cancel one booking or this-and-later in its series. Returns refs cancelled */
function cancel_bookings(Tenant $T, array $bk, bool $wholeSeries, bool $asAdmin): array {
    return $T->withLock(function () use ($T, $bk, $wholeSeries, $asAdmin) {
        $ctx = ctx_for($T);
        $list = ($wholeSeries && $bk['series_id']) ? $T->seriesBookings((int) $bk['series_id'], $bk['start_at']) : [$bk];
        $done = [];
        foreach ($list as $b) {
            if ($b['status'] !== 'confirmed') continue;
            if (!$asAdmin && $bk['customer_id'] !== $b['customer_id']) continue;
            if (!$asAdmin && !before_cutoff($ctx, db_ts($b['start_at']))) { if ($b['id'] === $bk['id']) throw new DomainException('cutoff'); continue; }
            $T->setStatus((int) $b['id'], $asAdmin ? 'cancelled_admin' : 'cancelled_customer');
            $done[] = $b['ref'];
        }
        return $done;
    });
}

function problem_text(string $p): string {
    $p = explode('@', $p)[0];
    return t('prob_' . $p) !== 'prob_' . $p ? t('prob_' . $p) : t('prob_generic');
}
