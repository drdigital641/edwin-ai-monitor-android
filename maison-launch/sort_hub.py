#!/usr/bin/env python3
"""Re-sort the Maison /new-launches/ hub cards from launch-queue.json (data-driven, no card content change).
Usage: sort_hub.py hub.html launch-queue.json out.html
Order = launch-queue.json 'hub_order' (DONE first, then TODO (DONE first, then TODO, each by launch date; planned/undated last).
Cards not in the queue keep their old relative order at the end. Everything outside the card list is byte-identical."""
import re, sys, json
src, qf, out = sys.argv[1:4]
h = open(src, encoding="utf-8").read()
OPEN = '<div class="lgrid" id="lgrid">'
s = h.index(OPEN) + len(OPEN)
rx = re.compile(r'<a class="lc[^"]*" href="/new-launches/([^/"]+)/"[^>]*>.*?</a>', re.S)
cards, pos = [], s
while True:
    m = rx.match(h, pos)
    if not m: break
    cards.append((m.group(1), m.group(0))); pos = m.end()
e = pos
assert h[e:e+6] == '</div>', 'card list not contiguous'
Q = json.load(open(qf, encoding="utf-8"))
order = Q.get("hub_order") or [p["slug"] for p in Q["projects"]]
rank = {slug: i for i, slug in enumerate(order)}
new = sorted(cards, key=lambda c: (rank.get(c[0], 10**6), [x[0] for x in cards].index(c[0])))
assert sorted(new) == sorted(cards) and len(new) == len(cards)
res = h[:s] + "".join(c[1] for c in new) + h[e:]
assert len(res) == len(h)
open(out, "w", encoding="utf-8").write(res)
print(len(new), "cards;", ", ".join(c[0] for c in new[:10]))
