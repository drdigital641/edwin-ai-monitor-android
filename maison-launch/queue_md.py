import json,sys
q=json.load(open(sys.argv[1]))
P=q['projects']
L=["# Maison new-launch queue (generated from launch-queue.json, do not hand-edit)","",
"Updated "+q['updated']+". "+q['rule'],
"Daily rule: build ONE TODO per day, the next in this order that has a v4 concept set; skipped ones are listed as waiting for images.",
"Mark DONE in launch-queue.json (status) only after live check + ?p1test=1 tap, then rerun queue_md.py and sort_hub.py.","",
"| # | Project | Type | Launch | Basis | Status | v4 set | Floor plan |","|---|---|---|---|---|---|---|---|"]
for i,p in enumerate(P,1):
    L.append(f"| {i} | {p['name']} | {p['type']} | {p['launch']} | {p['launch_basis']} | {p['status']} | {'Y' if p['v4_set'] else 'N'} | {'Y' if p['floor_plan'] else 'N'} |")
todo=[p for p in P if p['status']=='TODO']
nxt=[p for p in todo if p['v4_set']]
wait=[p['name'] for p in todo if not p['v4_set']]
L+=["","Next builds (have a v4 set, in order): "+", ".join(p['name'] for p in nxt),
"","Waiting for v4 images ("+str(len(wait))+"): "+", ".join(wait),
"","Basis: firm = official source; recorded = date recorded on our page from a third-party list; planned = planned/unconfirmed; none = no launch date on file (sorted A-Z last)."]
open(sys.argv[2],'w').write("\n".join(L)+"\n")
