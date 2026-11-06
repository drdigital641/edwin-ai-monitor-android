#!/usr/bin/env bash
# Read-only live checks 6 Nov: bare URL (as a visitor/cache sees it) vs cache-busting query.
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
cnt() { grep -o -- "$2" <<<"$1" | wc -l; }
chk() { # url, names...
  local u=$1; shift
  for v in "$u" "$u?nc=$RANDOM"; do
    h=$(curl -sL -A "$UA" -m 30 "$v"); hd=$(curl -sIL -A "$UA" -m 30 "$v" | tr -d '\r' | grep -iE '^(last-modified|age|x-cache|x-endurance|cache-control|x-proxy-cache|cf-cache-status|server):' | tr '\n' ' ')
    echo "--- $v | bytes $(wc -c <<<"$h") | $hd"
    for s in "$@"; do echo "   $s: $(cnt "$h" "$s")"; done
  done
}
chk https://www.sggarage.com/ "Meyan Lim" "Nurhayati" "Derrick Khoo" "Rui Yang" "Chuan Kiat" "Tarlo Gill" "Wahlin Lee" "half the price" "R. Y. C." "M. L."
chk https://sggarage.com/ "Meyan Lim" "Rui Yang" "half the price" "M. L."
chk https://www.cleanicdetailing.com/about/ "Grace Pang" "Benjamin Loo" "Azura" '"G. P."' '"B. L."'
chk https://www.cleanicdetailing.com/ "Idris Talib" "Azura A." "I. T."
chk https://sofacaresg.com/ 'href="/privacy.html"'
chk https://sofacaresg.com/faq.html 'href="/privacy.html"'
