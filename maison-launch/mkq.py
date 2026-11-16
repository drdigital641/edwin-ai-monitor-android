import json,glob
nl='/tmp/claude-0/nl/'
D={json.load(open(f))['slug']:json.load(open(f)) for f in glob.glob(nl+'*.json')}
# launch: (sort_key, label, basis, source)  basis: firm | recorded | planned | none
L={}
def put(s,k,lab,basis,src): L[s]=(k,lab,basis,src)
for s in ['chencharu-acres','toa-payoh-hillside','bayshore-sails','plantation-dew','sembawang-anchor','bayshore-oasis','merpati-meadow']:
    put(s,'2026-11','Nov 2026 BTO','firm','HDB BTO portal (page facts)')
for s in ['berlayar-rise','kebun-baru-breeze','kebun-baru-ridge','lakeview-cascadia','sembawang-brook','sembawang-portico','woodgrove-acres']:
    put(s,'2026-06-16','16 Jun 2026 BTO','firm','HDB June 2026 BTO (page facts)')
put('brickland-weave','2023-02','Feb 2023 BTO','firm','HDB Feb 2023 BTO brochure')
put('keat-hong-grange','2022-08','Aug 2022 BTO','firm','HDB Aug 2022 BTO brochure')
put('towner-residences','2021-08','Aug 2021 BTO','firm','HDB press release 11 Aug 2021 (Kallang/Whampoa)')
put('canninghill-piers','2021-11-05','5 Nov 2021 preview','firm','CDL/CapitaLand release')
put('amo-residence','2022-07-09','9 Jul 2022 preview','firm','UOL release / EdgeProp')
put('the-myst','2023-06-24','24 Jun 2023 preview','firm','CDL release')
put('lumina-grand','2024','2024 (year only)','firm','CDL release "first EC launch in 2024"')
put('norwood-grand','2024-10-04','4 Oct 2024 preview','firm','CDL release')
put('the-orie','2025-01','Jan 2025','recorded','page facts')
put('coastal-cabana','2026-01','Jan 2026','recorded','page (newspaper report)')
put('narra-residences','2026-01-31','end Jan 2026','recorded','page (third-party report)')
put('newport-residences','2026-01','Jan 2026','firm','CDL (page facts)')
put('february-2026-sbf-exercise','2026-02-04','4 Feb 2026 SBF','recorded','page (news report)')
for s in ['pinery-residences','rivelle-tampines','river-modern']: put(s,'2026-03','Mar 2026','recorded','page (third-party list)')
for s in ['tengah-garden-residences','vela-bay']: put(s,'2026-04','Apr 2026','recorded','page (third-party list)')
put('hudson-place-residences','2026-05','May 2026','recorded','page (third-party list)')
for s in ['duet-at-emily','dunearn-house','lentor-gardens-residences','the-bronze']: put(s,'2026-07','Jul 2026','recorded','page (third-party list)')
for s in ['amberwood-at-holland','lucerne-grand']: put(s,'2026-09','Sep 2026','recorded','page (third-party list)')
for s in ['the-serra-residences','thomson-reserve']: put(s,'2026-10','Oct 2026','recorded','page (third-party list)')
put('luxus-hills-phase-10','2026-09','Sep 2026 (unofficial)','planned','page (caveat data, not official)')
for s in ['solano-grand','wynwood-grand']: put(s,'2027-03','Q1 2027 planned','planned','CDL SGX update (page facts)')
put('dorset-gardens','2027-06','H1 2027 planned','planned','page (third-party report)')
put('hougang-central-mixed-use-development','2027-12','H2 2027 planned','planned','page (third-party report)')
DONE={'chencharu-acres','toa-payoh-hillside','bayshore-sails','plantation-dew','sembawang-anchor','brickland-weave','keat-hong-grange'}
SET={'towner-residences':('towner-v4',True),'canninghill-piers':('canninghill-piers-v4',True),'norwood-grand':('norwood-grand-v4',True),
 'the-myst':('the-myst-v4',True),'pollen-collection':('pollen-collection-v4',True),'shaw-tower':('shaw-tower-v4',True),
 'amo-residence':('amo-residence-v4',False),'lumina-grand':('lumina-grand-v4',False)}
for s in DONE: SET[s]=(s+'-v4',True)
rows=[]
for s,d in D.items():
    k,lab,basis,src=L.get(s,('9999','not on file','none',''))
    st='DONE' if s in DONE else 'TODO'
    cs,fp=SET.get(s,(None,False))
    rows.append(dict(slug=s,name=d['name'],type=d['type'],launch_sort=k,launch=lab,launch_basis=basis,launch_source=src,
      status=st,v4_set=cs,floor_plan=fp))
grp={'firm':0,'recorded':0,'planned':1,'none':2}
rows.sort(key=lambda r:(r['status']!='DONE',grp[r['launch_basis']],r['launch_sort'],r['name'].lower()))
json.dump(dict(updated='2026-11-16',rule='Hub order: DONE first, then TODO; inside each: dated launches earliest first, then planned/unconfirmed, then no date on file (A-Z).',projects=rows),open('launch-queue.json','w'),indent=1,ensure_ascii=False)
print(len(rows))
for i,r in enumerate(rows[:20],1): print(i,r['status'],r['name'],r['launch'],r['v4_set'])
