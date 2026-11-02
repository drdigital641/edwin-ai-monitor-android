#!/usr/bin/env bash
# Per-page audit of sitemap URLs listed in .github/probe/audit/*.txt (one sitemap URL per line).
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
for f in .github/probe/audit/*.txt; do
  [ -f "$f" ] || continue
  while read -r sm; do
    [ -z "$sm" ] && continue
    echo "##### AUDIT $sm"
    curl -sL -A "$UA" -m 40 "$sm" | grep -o '<loc>[^<]*</loc>' | sed 's/<[^>]*>//g' | grep -v '\.xml$' | head -400 | while read -r u; do
      html=$(curl -sL -A "$UA" -m 25 "$u")
      t=$(echo "$html" | tr '\n' ' ' | grep -oiE '<title[^>]*>[^<]*' | head -1 | sed 's/<[^>]*>//')
      h1=$(echo "$html" | grep -oiE '<h1[ >]' | wc -l)
      ag=$(echo "$html" | grep -c 'AggregateRating')
      lg=$(echo "$html" | grep -oiE '<html[^>]*lang="[^"]*"' | head -1 | sed 's/.*lang="//;s/"//')
      echo "${#t}|h1=$h1|agg=$ag|$lg|${u#https://}|$t"
    done
  done < "$f"
done
