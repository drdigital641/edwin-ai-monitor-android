#!/bin/sh
# Nightly dump of the booking database (run from the ONE existing nightly cron, rule 21; do not add a second cron if one exists).
# Credentials come from booking-private/my.cnf (chmod 600), never from the command line.
set -eu
P="$HOME/booking-private"
OUT="$HOME/backups-private/booking"
mkdir -p "$OUT"; chmod 700 "$OUT"
DB=$(sed -n 's/^database *= *//p' "$P/my.cnf")
F="$OUT/booking-$(date +%Y%m%d-%H%M%S).sql.gz"
mysqldump --defaults-extra-file="$P/my.cnf" --single-transaction --quick --routines --no-tablespaces "$DB" | gzip -9 > "$F"
chmod 600 "$F"
# keep 14 days (only files this script made, only in this folder)
find "$OUT" -maxdepth 1 -name 'booking-*.sql.gz' -type f -mtime +14 -print -exec rm -f {} \;
