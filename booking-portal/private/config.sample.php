<?php
/* COPY to /home/<account>/booking-private/config.php (outside public_html), chmod 600.
   Fill the values on the server only. Never commit the real file. Secret NAMES only here. */
return [
    'base_url'      => 'https://pageonesingapore.com/booking',   // one value: move to a white-label subdomain later by editing this
    'db_host'       => 'localhost',
    'db_name'       => '<cpanelprefix>_booking',
    'db_user'       => '<cpanelprefix>_bookapp',
    'db_pass'       => '<BOOKING_DB_PASSWORD>',                  // set in cPanel by Domain Go-Live
    'pepper'        => '<BOOKING_PEPPER: 64 random hex chars>',  // keys IP hashes for rate limits
    'setup_token'   => '<BOOKING_SETUP_TOKEN: 40+ random chars>',// one-time super-admin setup; blank it after setup
    'session_path'  => '/home/<account>/booking-private/sessions',// private session files (create, chmod 700)
    'test_mode'     => false,   // true only while testing: allows +65000000xx numbers (always flagged is_test)
    'cookie_secure' => true,
    'hsts'          => true,
    'lang'          => 'en',
];
