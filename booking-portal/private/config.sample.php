<?php
/* ONE file per client: /home/<account>/booking-clients/<client-slug>/config.php  (chmod 600, outside public_html).
   Placeholders only. Fill the values on the server; never commit, drop, log or paste them. */
return [
    'client_slug'   => 'sg-autobots',                                      // must match the seed file / clients row
    'seed'          => 'sg-autobots',                                      // engine/app/seed/<seed>.json, used once at setup
    'base_url'      => 'https://pageonesingapore.com/preview/sg-autobots/booking',  // the entry folder; the ONLY URL to change on a domain move
    'embed_domains' => ['pageonesingapore.com'],                           // sites allowed to frame the portal (+www added automatically)
    'db_host'       => 'localhost',
    'db_name'       => '<cpanelprefix>_bk_sgautobots',                     // this client's OWN database
    'db_user'       => '<cpanelprefix>_bksga',
    'db_pass'       => '<BOOKING_DB_PASSWORD_SGAUTOBOTS>',
    'pepper'        => '<BOOKING_PEPPER_SGAUTOBOTS: 64 random hex chars>',
    'setup_token'   => '<BOOKING_SETUP_TOKEN_SGAUTOBOTS: 40+ random chars>', // first admin login; blank it after setup
    'session_path'  => '/home/<account>/booking-clients/sg-autobots/sessions', // chmod 700
    'test_client'   => false,                                              // true ONLY for the separate smoke-test client (marks its row is_test)
    'test_mode'     => false,                                              // true only during the smoke test (+65000000xx)
    'cookie_secure' => true,
    'hsts'          => true,
    'lang'          => 'en',
];
