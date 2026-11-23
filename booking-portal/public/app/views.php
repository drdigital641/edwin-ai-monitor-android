<?php
/* ONE layout template + header/footer + shared UI pieces for every screen. */
declare(strict_types=1);
if (!defined('P1B')) { http_response_code(404); exit; }

function curl_(string $slug, string $r = '', array $p = []): string {   // client URL
    $qs = array_filter(['r' => $r] + $p, fn($v) => $v !== '' && $v !== null);
    return base_path() . '/' . rawurlencode($slug) . '/' . ($qs ? '?' . http_build_query($qs) : '');
}
function surl(string $r = 's', array $p = []): string { return base_path() . '/?' . http_build_query(['r' => $r] + $p); }

function hex_ok(string $h, string $fallback): string { return preg_match('/^#[0-9a-fA-F]{6}$/', $h) ? strtolower($h) : $fallback; }
function luminance(string $hex): float {
    $c = array_map(fn($i) => hexdec(substr($hex, $i, 2)) / 255, [1, 3, 5]);
    $c = array_map(fn($v) => $v <= 0.03928 ? $v / 12.92 : (($v + 0.055) / 1.055) ** 2.4, $c);
    return 0.2126 * $c[0] + 0.7152 * $c[1] + 0.0722 * $c[2];
}
function fg_for(string $hex): string { return luminance($hex) > 0.36 ? '#111418' : '#ffffff'; }

function theme_css(?array $c): string {
    $bg = hex_ok($c['colour_bg'] ?? '', '#f6f7f9'); $p = hex_ok($c['colour_primary'] ?? '', '#1f4fa0'); $a = hex_ok($c['colour_accent'] ?? '', '#f2c94c');
    $dark = luminance($bg) < 0.2;
    $fg = $dark ? '#f3f5f8' : '#14171c';
    $card = $dark ? '#121823' : '#ffffff';
    $line = $dark ? '#263042' : '#dfe3ea';
    $muted = $dark ? '#a8b2c3' : '#5a6373';
    // link colour must read on the background: lighten the brand colour on dark grounds
    $link = $dark && luminance($p) < 0.12 ? '#7fb0f0' : $p;
    return ":root{--bg:$bg;--fg:$fg;--card:$card;--line:$line;--muted:$muted;--p:$p;--pfg:" . fg_for($p) . ";--a:$a;--afg:" . fg_for($a) . ";--link:$link}";
}

function dur_label(array $s): string {
    if (!empty($s['full_day'])) return t('full_day');
    $m = (int) ($s['duration_min'] ?? 0);
    if ($m <= 0) return '';
    if ($m < 60) return t('mins', ['n' => $m]);
    return $m % 60 ? t('hours_nm', ['h' => intdiv($m, 60), 'm' => $m % 60]) : t('hours_n', ['n' => $m / 60]);
}
function price_label(array $s): string {
    if (($s['price_note'] ?? '') !== '') return (string) $s['price_note'];
    if ($s['price'] !== null && $s['price'] !== '') return 'S$' . rtrim(rtrim(number_format((float) $s['price'], 2), '0'), '.');
    return '';
}
function status_label(string $st): string { return t('st_' . $st); }

function in_embed(): bool { return !empty($_SESSION['embed']); }

/** the layout. $o: client, title, body, area (c|a|s), nav (html), wide (bool) */
function page(array $o): void {
    $c = $o['client'] ?? null;
    send_headers($c);
    $title = trim(($o['title'] ?? '') . ($c ? ' | ' . $c['name'] : ''), ' |');
    $n = nonce();
    $flash = flash();
    $area = $o['area'] ?? 'c';
    ?><!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="strict-origin-when-cross-origin">
<title><?= e($title) ?></title>
<?php if ($c && $c['logo_url']): ?><link rel="icon" href="<?= e($c['logo_url']) ?>"><?php endif; ?>
<link rel="stylesheet" href="<?= e(asset('assets/portal.css')) ?>">
<style nonce="<?= e($n) ?>"><?= theme_css($c) ?></style>
<script src="<?= e(asset('assets/portal.js')) ?>" defer></script>
</head><body class="area-<?= e($area) ?><?= in_embed() ? ' is-embed' : '' ?><?= !empty($o['wide']) ? ' wide' : '' ?>">
<header class="top"><div class="wrap top-in">
<?php if ($c): ?><a class="brand" href="<?= e($area === 'a' ? curl_($c['slug'], 'a') : curl_($c['slug'])) ?>"><?php if ($c['logo_url']): ?><img class="badge" src="<?= e($c['logo_url']) ?>" alt="" width="44" height="44"><?php endif; ?><span><?= e($c['name']) ?></span></a>
<?php else: ?><span class="brand"><span><?= e(t('s_title')) ?></span></span><?php endif; ?>
<nav class="topnav"><?= $o['nav'] ?? '' ?></nav></div></header>
<main class="wrap" id="main">
<?php if ($flash): ?><p class="flash <?= e($flash[0]) ?>" role="status"><?= e($flash[1]) ?></p><?php endif; ?>
<?php if (!empty($o['h1'])): ?><h1><?= e($o['h1']) ?></h1><?php endif; ?>
<?= $o['body'] ?>
</main>
<?php if ($c && $area === 'c'): ?>
<footer class="foot wrap"><a href="<?= e(curl_($c['slug'], 'privacy')) ?>"><?= e(t('privacy')) ?></a><?php if ($c['whatsapp_e164']): ?><a href="<?= e(wa_link($c['whatsapp_e164'])) ?>" target="_blank" rel="noopener"><?= e(t('whatsapp_us')) ?></a><?php endif; ?></footer>
<?php endif; ?>
</body></html><?php
}

function customer_nav(array $c): string {
    if (!empty($_SESSION['cust'])) {
        return '<a href="' . e(curl_($c['slug'], 'mine')) . '">' . e(t('my_bookings')) . '</a>'
            . '<form method="post" action="' . e(curl_($c['slug'], 'logout')) . '" class="inl">' . csrf_field() . '<button class="link">' . e(t('log_out')) . '</button></form>';
    }
    return '<a href="' . e(curl_($c['slug'], 'login')) . '">' . e(t('log_in')) . '</a>';
}

function wa_button(array $c, string $text, string $label, string $cls = 'btn wa'): string {
    if (!$c['whatsapp_e164']) return '';
    return '<a class="' . e($cls) . '" href="' . e(wa_link($c['whatsapp_e164'], $text)) . '" target="_blank" rel="noopener">' . e($label) . '</a>';
}

function field(string $name, string $label, array $o = []): string {
    $type = $o['type'] ?? 'text';
    $attrs = '';
    foreach (['inputmode', 'autocomplete', 'pattern', 'maxlength', 'minlength', 'min', 'max', 'step', 'placeholder'] as $a) if (isset($o[$a])) $attrs .= ' ' . $a . '="' . e($o[$a]) . '"';
    if (!empty($o['required'])) $attrs .= ' required';
    $id = 'f_' . $name . ($o['idsfx'] ?? '');
    $hint = isset($o['hint']) ? '<small>' . e($o['hint']) . '</small>' : '';
    if ($type === 'textarea') return '<label for="' . $id . '">' . e($label) . '</label><textarea id="' . $id . '" name="' . e($name) . '"' . $attrs . '>' . e($o['value'] ?? '') . '</textarea>' . $hint;
    return '<label for="' . $id . '">' . e($label) . '</label><input id="' . $id . '" type="' . e($type) . '" name="' . e($name) . '" value="' . e($o['value'] ?? '') . '"' . $attrs . '>' . $hint;
}
function check(string $name, string $label, bool $on, string $id = ''): string {
    $id = $id ?: 'c_' . $name;
    return '<label class="chk" for="' . e($id) . '"><input type="checkbox" id="' . e($id) . '" name="' . e($name) . '" value="1"' . ($on ? ' checked' : '') . '><span>' . e($label) . '</span></label>';
}
function errors_html(array $errs): string {
    if (!$errs) return '';
    return '<div class="flash err" role="alert">' . implode('<br>', array_map('e', $errs)) . '</div>';
}

function booking_rows(array $ctx, array $b, bool $withPrice = true): string {
    $s = db_ts($b['start_at']); $e = db_ts($b['end_at']);
    $rows = [
        [t('ref'), '<b class="ref">' . e($b['ref']) . '</b>'],
        [t('date'), e(fmt_local($ctx, $s, 'D j M Y'))],
        [t('time'), e(fmt_local($ctx, $s, 'g:i a') . ' - ' . fmt_local($ctx, $e, 'g:i a'))],
        [t('service'), e($b['service_name'])],
        [t('duration'), e(dur_label($b + ['full_day' => 0, 'duration_min' => intdiv($e - $s, 60)]))],
    ];
    if ($withPrice && ($p = price_label($b)) !== '') $rows[] = [t('price'), e($p)];
    return '<dl class="kv">' . implode('', array_map(fn($r) => '<dt>' . e($r[0]) . '</dt><dd>' . $r[1] . '</dd>', $rows)) . '</dl>';
}

/** date chips + slot chips, shared by customer booking, reschedule and admin booking */
function picker_html(array $ctx, array $svc, array $strip, string $selDate, array $slots, callable $dateHref, callable $slotHref): string {
    $h = '<h2>' . e(t('choose_date')) . '</h2><div class="days" role="list">';
    foreach ($strip as $date => $st) {
        $d = new DateTimeImmutable($date, $ctx['tz']);
        $label = '<span class="dw">' . e($d->format('D')) . '</span><span class="dn">' . e($d->format('j')) . '</span><span class="dm">' . e($d->format('M')) . '</span>';
        if ($st === 'open') $h .= '<a role="listitem" class="day' . ($date === $selDate ? ' on' : '') . '" href="' . e($dateHref($date)) . '"' . ($date === $selDate ? ' aria-current="date"' : '') . '>' . $label . '</a>';
        else $h .= '<span role="listitem" class="day off" aria-disabled="true" title="' . e(t('prob_' . ($st === 'full' ? 'full' : ($st === 'past' ? 'past' : $st)))) . '">' . $label . '</span>';
    }
    $h .= '</div>';
    if ($selDate !== '') {
        $h .= '<h2>' . e(t('choose_time')) . ' <small>' . e((new DateTimeImmutable($selDate, $ctx['tz']))->format('D j M')) . '</small></h2>';
        if (!$slots) $h .= '<p class="muted">' . e(t('no_slots')) . '</p>';
        else { $h .= '<div class="slots">'; foreach ($slots as $s) $h .= '<a class="slot" href="' . e($slotHref($s)) . '">' . e(fmt_local($ctx, $s, 'g:i a')) . '</a>'; $h .= '</div>'; }
    }
    return $h;
}
function first_open(array $strip): string { foreach ($strip as $d => $st) if ($st === 'open') return $d; return ''; }
