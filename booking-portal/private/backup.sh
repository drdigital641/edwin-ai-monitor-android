#!/bin/sh
# Nightly dump of EVERY client booking database (one loop, one cron line: rule 21).
# Each client folder /home/<account>/booking-clients/<slug>/ has its own my.cnf (chmod 600). Dumps: ~/backups-private/booking/<slug>/, 14 days kept.
set -eu
for dir in "$HOME"/booking-clients/*/; do
  slug=$(basename "$dir"); cnf="$dir/my.cnf"
  [ -f "$cnf" ] || continue
  db=$(sed -n 's/^database *= *//p' "$cnf")
  out="$HOME/backups-private/booking/$slug"; mkdir -p "$out"; chmod 700 "$out"
  f="$out/$slug-$(date +%Y%m%d-%H%M%S).sql.gz"
  mysqldump --defaults-extra-file="$cnf" --single-transaction --quick --no-tablespaces "$db" | gzip -9 > "$f"
  chmod 600 "$f"
  find "$out" -maxdepth 1 -name "$slug-*.sql.gz" -type f -mtime +14 -exec rm -f {} \;
done
