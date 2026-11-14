import re, json, html
W='/tmp/claude-0/-home-claude/42f72391-fce0-59b0-8c4f-3ec2a15b46a7/scratchpad/wk/'
s=open(W+'client-builds/2026-11-13/xado/articles/how-to-use-less-fuel-in-stop-start-traffic-singapore.html',encoding='utf-8').read()
OLD='how-to-use-less-fuel-in-stop-start-traffic-singapore'; NEW='manual-gearbox-hard-to-shift-notchy-singapore'
T='Manual Gearbox Hard to Shift or Notchy? Causes and Care | XADO SG'
D='Manual gearbox stiff, notchy or grinding into gear? The usual causes, what to check first, when to stop driving, and what XADO says about its manual gearbox treatment.'
H='Manual gearbox hard to shift or notchy: causes and care'
faq=[('Why is my manual gearbox hard to shift?','The usual causes are a clutch that is not fully releasing (low or aired hydraulic fluid, wear or cable adjustment), worn shift linkage or bushes, low or old gearbox oil, or worn synchromesh. A workshop can tell which by checking the clutch and the gearbox oil first.'),
('Why is my gearbox only stiff when it is cold?','Gearbox oil is thicker when cold, so shifts can feel notchy until it warms up. If it stays stiff after a few minutes, or is getting worse, have the oil level and grade checked against your owner manual.'),
('Is it safe to keep driving with a notchy manual gearbox?','Mild stiffness can be checked at your next service, but grinding into a gear, a clutch pedal that sticks to the floor, or a gear that will not engage means stop and get it checked. Forcing a gear can add damage.'),
('Will a gearbox additive fix a hard-to-shift manual gearbox?','No additive can repair a failed clutch, bent linkage or broken part. XADO lists its EX120 Revitalizant for manual gearboxes and transfer cases and describes revitalizant as designed to rebuild a protective layer on worn metal surfaces; ask a workshop to diagnose the cause first. These are XADO\'s statements, not a promise.'),
('How often should manual gearbox oil be changed?','Follow your maker\'s manual: some give an interval and some call the oil lifetime fill. If your car is old, was used hard or the history is unknown, ask a workshop whether to check or change it.')]
body='''<article class="wrap prose"><div class="takeaways"><h2>Key takeaways</h2><ul><li>A hard-to-shift manual gearbox is often the <strong>clutch, the linkage or the gearbox oil</strong>, not the gears themselves. Find out which before spending money.</li><li><strong>Stiff only when cold</strong> is common; <strong>grinding, a pedal that sticks to the floor or a gear that will not engage</strong> means stop and get it checked.</li><li>XADO lists a revitalizant for manual gearboxes and transfer cases. That is XADO's statement about its product, and it does not replace a repair.</li></ul></div>
<p>A stiff, notchy or crunchy gear change is a common complaint on older manual cars in Singapore, where stop-go traffic means a lot of clutch and gear use. Below are the usual causes, what to check in order, and where XADO fits in. This is general advice; your owner manual and a workshop come first.</p>
<h2>What makes a manual gearbox hard to shift?</h2>
<ul><li><strong>The clutch is not fully releasing.</strong> Low or aired hydraulic clutch fluid, a worn clutch or a stretched cable can stop the clutch separating cleanly, so gears resist or grind. A high bite point or a spongy pedal points here.</li><li><strong>Worn shift linkage or bushes.</strong> The lever feels loose, vague or notchy because the cables, rods or rubber bushes between the lever and the gearbox have worn.</li><li><strong>Low, old or wrong gearbox oil.</strong> Oil that is low, degraded or of the wrong grade makes shifts stiff, and a leak can be the reason it is low.</li><li><strong>Worn synchromesh.</strong> Grinding into one particular gear, especially when shifting quickly, can mean the synchro for that gear is worn.</li><li><strong>Cold oil.</strong> Gearbox oil is thicker when cold, so a slightly notchy shift on a cold start that eases as the car warms up is common.</li></ul>
<h2>What should you check first?</h2>
<ol class="big"><li><strong>Notice when it happens.</strong> Cold only, one gear only, or every gear with the clutch pedal down? Tell the workshop; it narrows the cause quickly.</li><li><strong>Feel the clutch pedal.</strong> A pedal that is spongy, sticks low or has a different bite point than before points to the clutch system.</li><li><strong>Check the clutch fluid level</strong> if your car has a hydraulic clutch (the reservoir is under the bonnet; see your manual).</li><li><strong>Look at the gearbox oil service history.</strong> If it has never been checked on an older car, ask a workshop to check the level and condition.</li><li><strong>Look for oil drips</strong> under the gearbox or around the shafts.</li></ol>
<h2>When should you stop driving?</h2>
<p>Stop and get the car checked if a gear grinds loudly or will not engage, the clutch pedal sticks to the floor, you smell burning from the clutch, or the car will not move off. Forcing a gear can add damage. If you are unsure, ask a workshop before a long trip.</p>
<h2>Can a manual gearbox additive help?</h2>
<p>An additive cannot repair a failed clutch, a bent linkage or a broken part. XADO lists its EX120 Revitalizant for manual gearboxes and transfer cases in the <a href="../xado-products-guide.html">XADO product guide</a>, and describes revitalizant as designed to use the energy of friction to rebuild a protective ceramic-metal (cermet) layer on worn metal surfaces (see <a href="../how-xado-works.html">how XADO works</a>). Those are XADO's statements about its products. Results depend on the gearbox condition, oil and maintenance history, and XADO Singapore does not give a figure. For an automatic car see <a href="gearbox-additive-automatic-transmission-singapore.html">gearbox additive for automatic transmissions</a>.</p>
<div class="inline-cta"><p><strong>Gearbox getting stiffer on an older manual car?</strong> Ask an authorised XADO workshop to check it and plan any treatment with your next service.</p><a class="btn sm" href="../find-a-xado-workshop.html">Find a workshop</a></div>
<h2>How to get it done in Singapore</h2>
<ol class="big"><li><strong>Note the symptoms</strong> (cold only, one gear, pedal feel).</li><li><strong>Book a check</strong> with an authorised XADO workshop and tell them the car has a hard-to-shift manual gearbox.</li><li><strong>Fix the cause first,</strong> then ask which XADO product suits your car using the <a href="../xado-products-guide.html">XADO product guide</a>.</li></ol>
<p>Want XADO at your own workshop? <a href="../for-workshops/#own-workshop">XADO Singapore will contact them</a>.</p>
<h2>FAQs</h2><div class="faq">'''+''.join(f'<details><summary>{html.escape(q,quote=False)}</summary><p>{html.escape(a,quote=False)}</p></details>' for q,a in faq)+'</div></article>'
m=re.search(r'<article class="wrap prose">.*?</article>',s,re.S); s=s.replace(m.group(0),body)
s=s.replace(OLD,NEW)
s=s.replace('How to Use Less Fuel in Singapore Stop-Start Traffic | XADO SG',T)
s=s.replace('Stuck in CTE or PIE jams? Driving habits, tyre and servicing checks that cut fuel use, and what XADO says about worn engines and fuel.',D)
s=s.replace('How to use less fuel in Singapore stop-start traffic',H)
s=s.replace('Running costs','Gearbox care').replace('Updated 13 November 2026','Updated 15 November 2026').replace('2026-11-13','2026-11-15')
s=s.replace('p-xadoamctwinturbonew.jpg','og.jpg',2) if False else s
# og/ld image
s=s.replace('https://xado-shop.sg/assets/img/p-xadoamctwinturbonew.jpg','https://xado-shop.sg/assets/img/og.jpg')
# keep reading: swap the oil-change card for gearbox article, keep stop-go
m=re.search(r'<div class="rels">.*?</div></section>',s,re.S)
rels='<div class="rels"><a class="rel" href="gearbox-additive-automatic-transmission-singapore.html"><img src="../assets/img/p-xadoex120atf.jpg" alt="" loading="lazy"><span>Gearbox care</span><b>Gearbox additive in Singapore: what it does and when to use it</b></a><a class="rel" href="stop-go-traffic-engine-wear-singapore.html"><img src="../assets/img/sg-traffic.jpg" alt="" loading="lazy"><span>Singapore driving</span><b>How Singapore\'s stop-go traffic wears out your engine</b></a></div></section>'
s=s.replace(m.group(0),rels)
def fix(mm):
    d=json.loads(mm.group(1))
    for n in d:
        if n.get('@type')=='FAQPage': n['mainEntity']=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]
    return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'
s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',fix,s,count=1,flags=re.S)
open('/tmp/claude-0/-home-claude/42f72391-fce0-59b0-8c4f-3ec2a15b46a7/scratchpad/xbuild/'+NEW+'.html','w',encoding='utf-8').write(s)
