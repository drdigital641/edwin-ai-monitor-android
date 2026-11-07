#!/usr/bin/env bash
# Live check of the new privacy pages + IndexNow ping (8 Nov 2026). Runs on a GitHub runner because Claude sandboxes can't reach the live sites.
set -u
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
chk() { # url
  local u="$1" f=/tmp/p.html
  local code=$(curl -s -A "$UA" -o $f -w '%{http_code}' "$u?nc=$RANDOM$RANDOM")
  echo "URL $u code=$code bytes=$(wc -c <$f) h1=$(grep -o '<h1' $f | wc -l) privacy_links=$(grep -o 'privacy-policy/' $f | wc -l) noindex=$(grep -ci 'noindex' $f) canon=$(grep -o '<link rel="canonical" href="[^"]*"' $f | head -1)"
  curl -s -A "$UA" -I "$u?nc=$RANDOM" | grep -i -E '^(x-robots-tag|cache-control|content-type):' | sed 's/^/   hdr /'
}
for u in https://www.sggarage.com/privacy-policy/ https://autotexautoparts.com.sg/privacy-policy/ \
  https://www.sggarage.com/ https://www.sggarage.com/prices/ https://www.sggarage.com/articles/ https://www.sggarage.com/404.html \
  https://www.sggarage.com/articles/transmission-problems-warning-signs-singapore.html https://www.sggarage.com/articles/first-visit-edwin-garage-what-to-expect.html \
  https://www.sggarage.com/articles/byd-atto-3-servicing-singapore.html https://www.sggarage.com/car-servicing-repair/ \
  https://autotexautoparts.com.sg/ https://autotexautoparts.com.sg/kia/ https://autotexautoparts.com.sg/hyundai/accent-rb/air-filter/ \
  https://autotexautoparts.com.sg/articles/ https://autotexautoparts.com.sg/articles/hyundai-kia-aircon-not-cold-which-parts/ https://autotexautoparts.com.sg/about/; do chk "$u"; done
for s in https://www.sggarage.com/sitemap.xml https://www.sggarage.com/llms.txt https://autotexautoparts.com.sg/sitemap.xml https://autotexautoparts.com.sg/llms.txt; do
  echo "FILE $s privacy_mentions=$(curl -s -A "$UA" "$s?nc=$RANDOM" | grep -c 'privacy-policy')"; done
# IndexNow: only the new page and the homepage of each site
ping() { # host key urls...
  local h=$1 k=$2; shift 2; local list=$(printf '"%s",' "$@"); list="[${list%,}]"
  echo "INDEXNOW $h code=$(curl -s -o /dev/null -w '%{http_code}' -H 'Content-Type: application/json; charset=utf-8' -d "{\"host\":\"$h\",\"key\":\"$k\",\"keyLocation\":\"https://$h/$k.txt\",\"urlList\":$list}" https://api.indexnow.org/indexnow)"
}
if [ "$(cat .github/privacy-check/indexnow)" = "submit" ]; then
  ping www.sggarage.com adba3d204db0f9cd2fb386bf0cc497ce https://www.sggarage.com/privacy-policy/ https://www.sggarage.com/
  ping autotexautoparts.com.sg 7d3e9a51c4b84f2e9a0c6b1d58e2f437 https://autotexautoparts.com.sg/privacy-policy/ https://autotexautoparts.com.sg/
fi
# Full Autotex footer check: every synced page must carry the privacy link
miss=0; : > /tmp/miss.txt
while read p; do
  b=$(curl -s -A "$UA" --max-time 20 "https://autotexautoparts.com.sg/$p?nc=$RANDOM")
  if ! printf '%s' "$b" | grep -q 'privacy-policy/'; then echo "$p" >> /tmp/miss.txt; miss=$((miss+1)); fi
done < <(grep -v '^$' .github/privacy-check/autotex-paths.txt | sed 's|^$||')
echo "AUTOTEX_MISSING $miss"; sed 's/^/MISS /' /tmp/miss.txt
