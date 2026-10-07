#!/usr/bin/env bash
# Usage: site-config.sh <site-key>  -> prints REMOTE_DIR=... and DOMAIN=... for $GITHUB_ENV
set -euo pipefail
site="$1"
cfg="$(dirname "$0")/sites.json"
remote_dir="$(jq -r --arg s "$site" '.sites[$s].remote_dir // empty' "$cfg")"
domain="$(jq -r --arg s "$site" '.sites[$s].domain // empty' "$cfg")"
if [ -z "$remote_dir" ]; then
  echo "::error::Unknown site '$site'. Known: $(jq -r '.sites | keys | join(", ")' "$cfg")" >&2; exit 1
fi
if [ "$remote_dir" = "CHANGE_ME" ]; then
  echo "::error::bluehost/sites.json has no remote_dir for '$site' yet." >&2; exit 1
fi
case "$remote_dir" in
  /*|*..*) echo "::error::remote_dir must be relative to the home directory and must not contain '..'" >&2; exit 1 ;;
esac
echo "REMOTE_DIR=$remote_dir"
echo "DOMAIN=$domain"
