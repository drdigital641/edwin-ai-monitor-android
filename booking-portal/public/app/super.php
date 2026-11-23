<?php
/* Super-admin (Edwin only). Own session (cookie p1bs). One-time setup token from the private config. */
declare(strict_types=1);
if (!defined('P1B')) { http_response_code(404); exit; }

function spage(string $title, string $body, bool $nav = true): void {
    $n = $nav ? '<a href="' . e(surl('s')) . '">' . e(t('s_clients')) . '</a><form method="post" action="' . e(surl('s_logout')) . '" class="inl">' . csrf_field() . '<button class="link">' . e(t('log_out')) . '</button></form>' : '';
    page(['client' => null, 'title' => $title, 'h1' => $title, 'body' => $body, 'area' => 's', 'nav' => $n, 'wide' => true]);
}
function super_user(): ?array {
    if (empty($_SESSION['super'])) return null;
    $r = q("SELECT * FROM admins WHERE id=? AND role='super_admin' AND client_id IS NULL", [(int) $_SESSION['super']])->fetch();
    return $r ?: null;
}

function super_route(string $r): void {
    migrate();
    if (!SuperRepo::superExists()) { s_setup(); return; }
    if ($r === 's_login') { s_login(); return; }
    $su = super_user();
    if (!$su) redirect(surl('s_login'));
    $actor = 'super:' . $su['id'];
    switch ($r) {
        case 's': s_clients($actor); return;
        case 's_client': s_client($actor); return;
        case 's_logout': if (is_post()) { require_post_ok(); session_end_all(); } redirect(surl('s_login')); return;
    }
    http_response_code(404); spage(t('not_found'), '');
}

function s_setup(): void {
    $errs = [];
    $token = (string) cfg('setup_token', '');
    if ($token === '' || strlen($token) < 24) { spage(t('s_setup'), '<p class="flash err">Setup token missing in the private config.</p>', false); return; }
    if (is_post()) {
        require_post_ok();
        if (!rate_hit('s_setup', 10, 900)) $errs[] = t('err_rate');
        elseif (!hash_equals($token, (string) ($_POST['token'] ?? ''))) $errs[] = t('a_login_err');
        else {
            $u = in_str('username', 60); $p = (string) ($_POST['password'] ?? '');
            if (!preg_match('/^[a-z0-9._-]{3,60}$/i', $u)) $errs[] = t('username');
            if (strlen($p) < 12) $errs[] = t('a_err_pw');
            if (!$errs) { SuperRepo::createSuper($u, $p); meta_set('setup_done', utc_now()); audit(null, 'system', 'super_created'); flash(t('s_setup_done')); redirect(surl('s_login')); }
        }
    }
    $h = errors_html($errs) . '<form method="post" class="card form">' . csrf_field()
        . field('token', t('s_token'), ['type' => 'password', 'autocomplete' => 'off', 'required' => 1])
        . field('username', t('username'), ['autocomplete' => 'username', 'required' => 1])
        . field('password', t('password'), ['type' => 'password', 'autocomplete' => 'new-password', 'minlength' => 12, 'required' => 1, 'hint' => t('a_err_pw')])
        . '<button class="btn big">' . e(t('s_setup')) . '</button></form>';
    spage(t('s_setup'), $h, false);
}

function s_login(): void {
    $errs = [];
    if (is_post()) {
        require_post_ok();
        $u = in_str('username', 60); $p = (string) ($_POST['password'] ?? '');
        if (!rate_hit('s_login', 10, 900)) $errs[] = t('err_rate');
        else {
            $su = SuperRepo::superByUsername($u);
            if ($su && !is_locked($su['locked_until']) && password_verify($p, $su['password_hash'])) {
                admin_ok((int) $su['id']); session_regen(); $_SESSION['super'] = (int) $su['id']; audit(null, 'super:' . $su['id'], 'super_login'); redirect(surl('s'));
            }
            if ($su) admin_fail((int) $su['id']);
            $errs[] = t('a_login_err');
        }
    }
    $h = errors_html($errs) . '<form method="post" class="card form">' . csrf_field() . field('username', t('username'), ['autocomplete' => 'username', 'required' => 1])
        . field('password', t('password'), ['type' => 'password', 'autocomplete' => 'current-password', 'required' => 1]) . '<button class="btn big">' . e(t('log_in')) . '</button></form>';
    spage(t('s_title') . ' ' . t('log_in'), $h, false);
}

/** the per-client folder stub that gives a clean URL without .htaccess */
function ensure_stub(string $slug): bool {
    $dir = dirname(__DIR__) . '/' . $slug;
    $file = $dir . '/index.php';
    if (is_file($file)) return true;
    if (!is_dir($dir) && !@mkdir($dir, 0755)) return false;
    $code = "<?php\n/* client entry: " . $slug . " */\ndefine('P1B_SLUG', '" . $slug . "');\nrequire __DIR__ . '/../index.php';\n";
    return @file_put_contents($file, $code) !== false;
}

function seed_files(): array { return glob(__DIR__ . '/seed/*.json') ?: []; }

function import_seed(string $file): int {
    $j = json_decode((string) file_get_contents($file), true, 32, JSON_THROW_ON_ERROR);
    if (client_by_slug($j['client']['slug'])) throw new DomainException('exists');
    $id = SuperRepo::saveClient($j['client'] + ['is_test' => 0]);
    $T = new Tenant(SuperRepo::client($id));
    foreach ($j['services'] as $i => $s) {
        $T->saveService($s + ['slug' => '', 'group_slug' => '', 'price' => null, 'price_note' => '', 'recurring_allowed' => 0, 'active' => 0, 'sort_order' => $i, 'full_day' => 0, 'admin_note' => '', 'duration_min' => null]);
    }
    return $id;
}

function s_clients(string $actor): void {
    if (is_post()) {
        require_post_ok();
        $f = basename(in_str('seed', 80));
        $path = __DIR__ . '/seed/' . $f;
        if (preg_match('/^[a-z0-9-]+\.json$/', $f) && is_file($path)) {
            try { $id = import_seed($path); audit($id, $actor, 'client_import', '', $f); $c = SuperRepo::client($id); ensure_stub($c['slug']); flash(t('a_saved')); redirect(surl('s_client', ['id' => $id])); }
            catch (DomainException $e) { flash('Already imported', 'err'); }
        }
        redirect(surl('s'));
    }
    $h = '<p><a class="btn" href="' . e(surl('s_client')) . '">' . e(t('s_add_client')) . '</a></p><ul class="clist">';
    foreach (SuperRepo::clients() as $c)
        $h .= '<li class="crow"><a href="' . e(surl('s_client', ['id' => $c['id']])) . '"><b>' . e($c['name']) . '</b> <span class="mob">' . e($c['slug']) . '</span></a><span class="tag">' . e($c['status']) . '</span>' . ($c['is_test'] ? '<span class="tag">test</span>' : '') . '</li>';
    $h .= '</ul>';
    $seeds = array_filter(seed_files(), fn($f) => !client_by_slug(basename($f, '.json')));
    if ($seeds) {
        $h .= '<h2>' . e(t('s_import')) . '</h2>';
        foreach ($seeds as $f) $h .= '<form method="post" class="inl">' . csrf_field() . '<input type="hidden" name="seed" value="' . e(basename($f)) . '"><button class="btn ghost">' . e(basename($f, '.json')) . '</button></form> ';
    }
    spage(t('s_clients'), $h);
}

function embed_codes(array $c): string {
    $b = base_url(); $slug = $c['slug'];
    $codes = [
        'Direct link (booking_url)' => $b . '/' . $slug . '/',
        'Direct link, one service' => $b . '/' . $slug . '/?service=<service-slug>',
        'Book button (put the script once per page, then data-p1-book on any link or button)' =>
            '<script src="' . $b . '/embed.js" data-client="' . $slug . '" defer></script>' . "\n" .
            '<a href="' . $b . '/' . $slug . '/" data-p1-book data-cta="booking" data-ref="booking_home_hero">Book now</a>',
        'Inline booking section (auto height; needs the same embed.js on the page)' =>
            '<iframe src="' . $b . '/' . $slug . '/?embed=1" data-p1-booking title="Book an appointment" loading="lazy" style="width:100%;border:0;min-height:640px"></iframe>' . "\n" .
            '<script src="' . $b . '/embed.js" data-client="' . $slug . '" defer></script>',
        'Admin embed (login still required)' =>
            '<iframe src="' . $b . '/' . $slug . '/?r=a&embed=1" data-p1-booking title="Bookings admin" style="width:100%;border:0;min-height:800px"></iframe>' . "\n" .
            '<script src="' . $b . '/embed.js" data-client="' . $slug . '" defer></script>',
        'Admin link' => $b . '/' . $slug . '/?r=a',
    ];
    $h = '';
    foreach ($codes as $label => $code) $h .= '<label>' . e($label) . '</label><textarea class="code" readonly rows="' . (substr_count($code, "\n") + 2) . '">' . e($code) . '</textarea>';
    return $h;
}

function s_client(string $actor): void {
    $id = in_int('id');
    $c = $id ? SuperRepo::client($id) : null;
    if ($id && !$c) redirect(surl('s'));
    $errs = [];
    if (is_post()) {
        require_post_ok();
        if (in_str('act', 10) === 'admin' && $c) {
            $u = in_str('username', 60); $p = (string) ($_POST['password'] ?? '');
            if (!preg_match('/^[a-z0-9._-]{3,60}$/i', $u)) $errs[] = t('username');
            if (strlen($p) < 12) $errs[] = t('a_err_pw');
            if (!$errs) {
                try { SuperRepo::upsertClientAdmin((int) $c['id'], $u, $p); audit((int) $c['id'], $actor, 'client_admin_set', '', $u); flash(t('a_saved')); redirect(surl('s_client', ['id' => $c['id']])); }
                catch (DomainException $e) { $errs[] = 'Username already used by another client.'; }
            }
        } else {
            $row = ['id' => $id, 'slug' => $c['slug'] ?? strtolower(in_str('slug', 60)), 'name' => in_str('name', 120), 'logo_url' => in_str('logo_url', 500),
                'colour_primary' => hex_ok(in_str('colour_primary', 7), '#1f4fa0'), 'colour_accent' => hex_ok(in_str('colour_accent', 7), '#f2c94c'), 'colour_bg' => hex_ok(in_str('colour_bg', 7), '#ffffff'),
                'whatsapp_e164' => normalise_mobile(in_str('whatsapp_e164', 30)) ?? '', 'timezone' => in_array(in_str('timezone', 40), ['Asia/Singapore', 'Asia/Kuala_Lumpur'], true) ? in_str('timezone', 40) : 'Asia/Singapore',
                'recurring_enabled' => empty($_POST['recurring_enabled']) ? 0 : 1, 'allowed_embed_domains' => in_str('allowed_embed_domains', 1000),
                'status' => in_array(in_str('status', 10), ['setup', 'live', 'paused'], true) ? in_str('status', 10) : 'setup', 'is_test' => $c['is_test'] ?? 0];
            if (!preg_match('/^[a-z0-9][a-z0-9-]{1,59}$/', $row['slug']) || in_array($row['slug'], ['app', 'assets'], true)) $errs[] = 'Slug: lowercase letters, numbers and dashes.';
            if (!$id && client_by_slug($row['slug'])) $errs[] = 'Slug already used.';
            if ($row['name'] === '') $errs[] = t('a_b_name');
            if (!$errs) {
                $nid = SuperRepo::saveClient($row); audit($nid, $actor, $id ? 'client_edit' : 'client_add');
                if (!ensure_stub($row['slug'])) flash('Saved, but the client folder could not be created. Use ' . base_url() . '/?c=' . $row['slug'], 'err'); else flash(t('a_saved'));
                redirect(surl('s_client', ['id' => $nid]));
            }
            $c = $row + ($c ?? []);
        }
    }
    $c = $c ?? ['slug' => '', 'name' => '', 'logo_url' => '', 'colour_primary' => '#1f4fa0', 'colour_accent' => '#f2c94c', 'colour_bg' => '#ffffff', 'whatsapp_e164' => '', 'timezone' => 'Asia/Singapore', 'recurring_enabled' => 0, 'allowed_embed_domains' => '', 'status' => 'setup'];
    $sel = fn($name, $opts, $cur) => '<label for="f_' . $name . '">' . e($name) . '</label><select id="f_' . $name . '" name="' . $name . '">' . implode('', array_map(fn($o) => '<option' . ($o === $cur ? ' selected' : '') . '>' . e($o) . '</option>', $opts)) . '</select>';
    $h = errors_html($errs) . '<form method="post" class="card form">' . csrf_field()
        . ($id ? '<p>Slug: <b>' . e($c['slug']) . '</b></p>' : field('slug', 'Slug', ['required' => 1, 'pattern' => '[a-z0-9-]+']))
        . field('name', t('a_b_name'), ['value' => $c['name'], 'required' => 1]) . field('logo_url', t('a_b_logo'), ['value' => $c['logo_url']])
        . field('colour_primary', t('a_b_primary'), ['type' => 'color', 'value' => $c['colour_primary']]) . field('colour_accent', t('a_b_accent'), ['type' => 'color', 'value' => $c['colour_accent']])
        . field('colour_bg', t('a_b_bg'), ['type' => 'color', 'value' => $c['colour_bg']]) . field('whatsapp_e164', t('a_b_wa'), ['type' => 'tel', 'value' => $c['whatsapp_e164']])
        . $sel('timezone', ['Asia/Singapore', 'Asia/Kuala_Lumpur'], $c['timezone']) . $sel('status', ['setup', 'live', 'paused'], $c['status'])
        . field('allowed_embed_domains', 'Allowed embed domains (one per line)', ['type' => 'textarea', 'value' => (string) $c['allowed_embed_domains']])
        . check('recurring_enabled', 'Recurring bookings enabled', (bool) $c['recurring_enabled']) . '<button class="btn big">' . e(t('a_save')) . '</button></form>';
    if ($id) {
        $h .= '<h2>' . e(t('s_admins')) . '</h2><ul class="clist">';
        foreach (SuperRepo::clientAdmins($id) as $a) $h .= '<li class="crow"><span><b>' . e($a['username']) . '</b></span>' . (is_locked($a['locked_until']) ? '<span class="tag">locked</span>' : '') . '</li>';
        $h .= '</ul><form method="post" class="card form">' . csrf_field() . '<input type="hidden" name="act" value="admin"><h3>' . e(t('s_set_admin')) . '</h3>'
            . field('username', t('username'), ['required' => 1, 'autocomplete' => 'off']) . field('password', t('password'), ['type' => 'password', 'autocomplete' => 'new-password', 'minlength' => 12, 'required' => 1, 'hint' => t('a_err_pw')])
            . '<button class="btn">' . e(t('a_save')) . '</button></form>'
            . '<h2>' . e(t('s_embeds')) . '</h2><div class="card form">' . embed_codes($c) . '</div>'
            . '<p><a class="btn ghost" href="' . e(curl_($c['slug'], 'a')) . '">Open client admin</a> <a class="btn ghost" href="' . e(curl_($c['slug'])) . '">Open booking page</a></p>';
    }
    spage($id ? $c['name'] : t('s_add_client'), $h);
}
