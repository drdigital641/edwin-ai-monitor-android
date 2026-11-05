#!/usr/bin/env bash
# Read-only header check: preview URLs must send X-Robots-Tag noindex; live client domains must send none.
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
echo "##### robots.txt"; curl -s -A "$UA" -m 20 https://pageonesingapore.com/robots.txt | grep -ciE '^disallow: /preview/' | sed 's/^/preview disallow lines: /'
echo "##### PREVIEW (expect noindex)"
while read -r u; do [ -z "$u" ] && continue
  h=$(curl -sI -A "$UA" -m 20 "$u" | tr -d '\r')
  echo "$u | $(echo "$h" | head -1) | $(echo "$h" | grep -i '^x-robots-tag' || echo 'NO X-Robots-Tag') | $(echo "$h" | grep -i '^location' )"
done < .github/secprobe/preview.txt
echo "##### LIVE (expect no X-Robots-Tag, no meta noindex)"
while read -r d; do [ -z "$d" ] && continue
  for u in "https://$d/" "https://$d/robots.txt"; do
    h=$(curl -sIL -A "$UA" -m 20 "$u" | tr -d '\r')
    xr=$(echo "$h" | grep -i '^x-robots-tag' | tr '\n' ' ')
    echo "$u | $(echo "$h" | grep '^HTTP' | tail -1) | ${xr:-no X-Robots-Tag}"
  done
  m=$(curl -sL -A "$UA" -m 20 "https://$d/" | grep -oiE '<meta[^>]+name="robots"[^>]*>' | head -1)
  echo "   meta robots: ${m:-none}"
done < .github/secprobe/live.txt
