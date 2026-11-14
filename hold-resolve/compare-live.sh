# input cl.txt: site base rel sha ; output res.txt: site rel status http livesha
cd /tmp/cl
: > res.txt
while read site base rel sha; do
  u="$base/$rel"; case "$rel" in index.html) u="$base/";; */index.html) u="$base/${rel%index.html}";; esac
  st=""; for t in 1 2 3; do code=$(curl -s -m 30 -o body -w '%{http_code}' "$u"); h=$(sha256sum body | cut -c1-64); [ "$code" = 200 ] && [ "$h" = "$sha" ] && { st=SAME; break; }; [ "$code" = 404 ] && break; sleep 2; done
  [ -z "$st" ] && st=DIFF
  echo "$site $rel $st $code $h" >> res.txt; sleep 0.5
done < cl.txt
# live sitemap URLs not in source
for e in "star https://starperformancemotor.com" "klar https://klardetails.com.sg" "cska https://cskatrading.com" "jacky https://jackygearbox.com" "ben https://planwithben.sg"; do set -- $e
  curl -s -m 30 "$2/sitemap.xml" | grep -o '<loc>[^<]*' | sed 's#<loc>##' | while read u; do p=${u#$2/}; case "$p" in ""|*/) p="${p}index.html";; esac; grep -q "^$1 $p " res.txt || echo "$1 $p LIVEONLY sitemap" >> res.txt; done
done
echo DONE >> res.txt
