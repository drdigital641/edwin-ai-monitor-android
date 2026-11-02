#!/usr/bin/env bash
# Live probe used by the SEO fix pass. Reads domains.txt and urls/*.txt.
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
hop() { curl -s -o /dev/null -A "$UA" -m 20 -w "%{http_code} -> %{redirect_url}" "$1"; }
if [ "${MODE:-domains}" = "domains" ]; then
while read -r d; do
  [ -z "$d" ] && continue
  echo "=== $d"
  echo "http://$d/        $(hop http://$d/)"
  echo "http://www.$d/    $(hop http://www.$d/)"
  echo "https://www.$d/   $(hop https://www.$d/)"
  h=$(curl -sI -A "$UA" -m 20 https://$d/)
  echo "https home        $(echo "$h" | head -1 | tr -d '\r') | hsts: $(echo "$h" | grep -i '^strict-transport' | tr -d '\r')"
  echo "404 test          $(hop https://$d/no-such-page-xyz-123/)"
  html=$(curl -sL -A "$UA" -m 20 https://$d/)
  echo "lang              $(echo "$html" | grep -oiE '<html[^>]*lang="[^"]*"' | head -1)"
  sm=$(curl -sL -A "$UA" -m 30 https://$d/sitemap.xml)
  echo "sitemap locs      $(echo "$sm" | grep -o '<loc>' | wc -l) (sitemapindex: $(echo "$sm" | grep -c sitemapindex))"
  echo "llms.txt          $(hop https://$d/llms.txt) | $(curl -sL -A "$UA" -m 20 https://$d/llms.txt | grep -iE 'updated' | head -1)"
done < .github/probe/domains.txt
fi
for f in .github/probe/urls/*.txt; do
  [ -f "$f" ] || continue
  echo "##### $f"
  while read -r u; do
    [ -z "$u" ] && continue
    echo "$u  $(hop "$u")"
  done < "$f"
done
