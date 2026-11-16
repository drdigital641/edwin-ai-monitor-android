import json,sys
q=json.load(open(sys.argv[1])); P=q['projects']
yn=lambda b:'Y' if b else 'N'
L=["# Maison new-launch queue (generated from launch-queue.json, do not hand-edit)","",
f"Updated {q['updated']}. GSC data: {q['gsc']['date']}, {q['gsc']['window']} ({q['gsc']['source']}).","",q['rule'],"",
"Daily rule: ONE page a day = top TODO in A until A is empty, then B. Mark DONE only after live check + ?p1test=1 tap, then rerun queue_md.py and sort_hub.py.",
f"No v4 set on the next project: policy '{q['no_images_policy']}' (make = create the Base44 v4 set + official plan first; skip = take the next one that has a set, list the skipped one as waiting for images).",""]
A=[p for p in P if p['section']=='A']; B=[p for p in P if p['section']=='B']; D=[p for p in P if p['section']=='DONE']
L+=["## A) GSC priority (TODO pages with clicks, most clicks, then impressions)","","| # | Project | Type | Clicks | Impr. | Pos. | Launch | v4 set | Floor plan |","|---|---|---|---|---|---|---|---|---|"]
for i,p in enumerate(A,1):
    g=p['gsc_28d']; L.append(f"| {i} | {p['name']} | {p['type']} | {g['clicks']} | {g['impressions']} | {g['position']} | {p['launch']} | {yn(p['v4_set'])} | {yn(p['floor_plan'])} |")
L+=["","## B) Everything else (launch date, earliest first; planned/unconfirmed, then no date on file, last)","","| # | Project | Type | Launch | Basis | v4 set | Floor plan |","|---|---|---|---|---|---|---|"]
for i,p in enumerate(B,1):
    L.append(f"| {i} | {p['name']} | {p['type']} | {p['launch']} | {p['launch_basis']} | {yn(p['v4_set'])} | {yn(p['floor_plan'])} |")
L+=["","## DONE (full-concept pages, top of the /new-launches/ listing)","","| Project | Launch |","|---|---|"]+[f"| {p['name']} | {p['launch']} |" for p in D]
drops=[p for p in P if p.get('v4_drop')]
if drops:
    L+=["","## v4 drops waiting in the Bridge drop-folder (use these, do not regenerate; follow each README, state its gaps)",""]
    L+=[f"- {p['name']}: drop {p['v4_drop']['drop_id']} ({p['v4_drop']['status']}). Plan: {p['v4_drop']['plan']}. Gaps: {p['v4_drop']['gaps']}." for p in drops]
L+=["","Basis: firm = official source; recorded = date recorded on our page from a third-party list; planned = planned/unconfirmed; none = no launch date on file (A-Z)."]
open(sys.argv[2],'w').write("\n".join(L)+"\n")
