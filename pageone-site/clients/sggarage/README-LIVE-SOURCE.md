# SG Garage source = live (14 Nov 2026, HOLD resolve, read-only)

`site/` is a byte-exact copy of the live static set in /home3/sgmodde1/public_html/carbonfibre (www.sggarage.com):
every file the Bridge / night run writes for SG Garage plus every static HTML page in the 175-URL sitemap
(202 files). Copied with GET only (workflow "HOLD live snapshot (read-only)"); services/index.html answers 301 over
HTTP, so its bytes come from the Bridge read_file (cPanel exact-path read, sha 98cdf904...).

Left out on purpose: the Zen Cart PHP shop and every *.php, zc_admin, cache, logs, uploads (incl. uploads/xado),
images, includes (configure.php and other credential files were never read), .htaccess and its backups, .user.ini.
Legacy 2006-2010 shop pages (mcs_learn_more.html, nddbc.html, vbv_learn_more.html) are not in the sitemap and are
not written by any tool, so they are out too.

The old builders (sites/sggarage/*) are behind this copy. Build new pages FROM this copy. SG Garage Bridge HOLD stays ON.
Shas: hold-resolve/sggarage-live-source-shas.txt.
