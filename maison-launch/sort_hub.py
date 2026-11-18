#!/usr/bin/env python3
"""Re-sort the Maison /new-launches/ hub from launch-queue.json AND rebuild its layout (image cards + search + list).
Usage: sort_hub.py hub.html launch-queue.json out.html   (same call as before; the daily run needs no change)
Since 18 Nov 2026 this delegates to hub_cards.py: order = hub_order (DONE first, then TODO by launch date, undated last);
launches with a concept detail page get image cards on top, the rest stay in the compact list. Run it on the LIVE hub."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hub_cards
src, qf, out = sys.argv[1:4]
res, nf, nl, fs = hub_cards.build(open(src, encoding="utf-8").read(), json.load(open(qf, encoding="utf-8")))
open(out, "w", encoding="utf-8").write(res)
print(f"{nf + nl} cards ({nf} image cards, {nl} list rows); top: {', '.join(fs[:10])}")
