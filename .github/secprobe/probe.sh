#!/usr/bin/env bash
# Read-only live content checks (6 Nov 2026): reviewer initials, shortened quote, privacy footer links.
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
get() { curl -sL -A "$UA" -m 30 -H 'Cache-Control: no-cache' "$1?nc=$RANDOM"; }
cnt() { grep -o -- "$2" <<<"$1" | wc -l; }
h=$(get https://www.sggarage.com/)
echo "##### sggarage.com"
for s in "Wahlin Lee" "Meyan Lim" "Nurhayati Rahmad" "Derrick Khoo" "Rui Yang Chia" "Chuan Kiat Low" "Tarlo Gill" "previous workshop" "half the price" "W. L." "M. L." "N. R." "D. K." "R. Y. C." "C. K. L." "T. G."; do echo "$s: $(cnt "$h" "$s")"; done
echo "##### cleanicdetailing.com home"
h=$(get https://www.cleanicdetailing.com/)
for s in "Azura A." "Shafiq Thair" "Idris Talib" "A. A." "S. T." "I. T."; do echo "$s: $(cnt "$h" "$s")"; done
echo "##### cleanicdetailing.com/about/"
h=$(get https://www.cleanicdetailing.com/about/)
for s in "Azura" "Grace Pang" "Benjamin Loo" '"A. A."' '"G. P."' '"B. L."'; do echo "$s: $(cnt "$h" "$s")"; done
echo "##### sofacaresg.com privacy footer link"
for p in / /faq.html /pricing.html /contact.html /articles.html /sofa-cleaning-singapore.html; do
  h=$(get "https://sofacaresg.com$p"); echo "$p: privacy links $(cnt "$h" 'href="/privacy.html"')"; done
echo "privacy.html: $(curl -s -o /dev/null -w '%{http_code}' -A "$UA" https://sofacaresg.com/privacy.html)"
echo "sitemap: $(cnt "$(get https://sofacaresg.com/sitemap.xml)" 'privacy.html')"
