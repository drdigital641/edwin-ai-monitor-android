import re, json, html
from PIL import Image, ImageDraw, ImageFont
BASE='wk/client-builds/2026-11-13/battery-rescue/articles/does-a-dashcam-drain-the-car-battery-singapore/index.html'
s=open(BASE,encoding='utf-8').read()
OLD='does-a-dashcam-drain-the-car-battery-singapore'; NEW='can-i-change-my-own-car-battery-singapore'
TITLE='Can I Change My Own Car Battery? | Battery Rescue'
DESC='Changing a car battery yourself is possible on some older cars, but many modern cars need care. What to check, what can go wrong, and when to ask a technician.'
H1='Can I change my own car battery?'
faq=[('Can I change a car battery myself?','On some older cars with a simple battery in an easy spot, many owners do. On modern cars, especially with start-stop, a battery management system or a battery in the boot or under a seat, it is safer to have a technician do it.'),
('What can go wrong if I change my own car battery?','Touching the terminals in the wrong order can cause a short or sparks, a loose clamp can leave the car unable to start, and fitting the wrong type (for example a standard battery on a car that needs EFB or AGM) can shorten its life. Memory settings such as the radio code and windows may also need resetting.'),
('Do I need to reset anything after changing the battery?','Often, yes: the clock, radio, window auto-up and, on some cars, idle or start-stop settings. See our guide on what to reset after changing a car battery. Check your owner manual for your model.'),
('What do I do with the old car battery?','Do not put it in household rubbish. A used car battery contains lead and acid and should be handed in for recycling, for example to the shop or technician who supplies the new battery.'),
('Is it better to have a technician change it?','If you are not sure of the battery type, cannot reach the battery safely, or your car has start-stop, yes. Battery Rescue SG fits a Delkor at your location or at one of 10 Motoserv outlets, and every Delkor has a 1-year warranty.')]
body='''<div class="ans"><div class="k">QUICK ANSWER</div>You can change a car battery yourself on some older cars, if you have the right type, the right tools and a safe place to work. Many modern cars are harder: start-stop systems need an EFB or AGM battery, some batteries sit in the boot or under a seat, and settings may need resetting afterwards. If you are unsure, ask a technician.</div>
<h2>When is it reasonable to change it yourself?</h2><ul><li>The battery sits under the bonnet where you can reach it easily.</li><li>You know the exact size and type your car needs. See <a href="../../articles/car-battery-size-codes-explained/">car battery size codes explained</a> and <a href="../../articles/efb-vs-agm-vs-standard-battery/">EFB vs AGM vs standard battery</a>.</li><li>The car has no start-stop system and no special battery requirement in the owner manual.</li><li>You have the correct spanner, a way to hold the settings if needed, and a safe, dry, well-lit place.</li></ul>
<h2>When should you leave it to a technician?</h2><ul><li><b>Start-stop cars:</b> these usually need an EFB or AGM battery, and the wrong type can wear out early.</li><li><b>Battery in the boot, under a seat or behind a panel:</b> harder to reach and to vent safely.</li><li><b>European cars with battery management:</b> some need the new battery registered or settings reset. Check your owner manual.</li><li><b>You are not sure of the size, type or terminal side:</b> a battery that does not fit properly can move or short.</li></ul>
<h2>What are the basic safety steps?</h2><ol><li>Switch the engine off, remove the key and keep metal tools away from both terminals at once.</li><li>Disconnect the negative (black, marked minus) terminal first, then the positive.</li><li>Lift the old battery out carefully. It is heavy, and it contains acid.</li><li>Fit the new battery the right way round, secure the hold-down clamp, then connect the positive terminal first and the negative last.</li><li>Check the clamps are tight and the terminals are clean. See <a href="../../articles/white-powder-on-car-battery-terminals-singapore/">white powder on battery terminals</a>.</li></ol><p>These are general steps. Your owner manual comes first.</p>
<h2>What should you do afterwards?</h2><p>Check that the car starts, then see what needs resetting: clock, radio, window auto-up and any start-stop or idle settings. Our guide on <a href="../../articles/what-to-reset-after-changing-a-car-battery-singapore/">what to reset after changing a car battery</a> goes through them. Take the old battery to be recycled; do not throw it away with household rubbish.</p>
<h2>Not sure, or stuck now?</h2><p>If the car will not start, a jump-start may get you going: see <a href="../../articles/how-to-jump-start-a-car-safely-singapore/">how to jump-start a car safely</a>. Battery Rescue SG fits a Delkor at your location or at one of 10 Motoserv outlets. Every Delkor has a 1-year warranty. Find your car's battery on the <a href="../../rescue/">battery rescue page</a>, or call <a href="tel:+6581259169" data-ref="art">8125 9169</a> (24 hours) and tell us your car model first.</p>
<div class="enq"><b>Please note:</b> If our technician comes to you and finds the problem is not battery-related, an onsite service fee of $50 to $80 applies. Final charges depend on location and service requirements.</div>
<h2>Frequently asked questions</h2><div class="faq">'''+''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q,a in faq)+'</div>'
# split pieces of old
m=re.search(r'<article class="sec">(.*?)</article>',s,re.S)
assert m
s=s.replace(m.group(1),body)
# strings
s=s.replace(OLD,NEW)
s=s.replace('Does a Dashcam Drain the Car Battery? | Battery Rescue',TITLE)
s=s.replace('Can a dashcam flatten your car battery? How parking mode, cable type and low-voltage cut-off decide it, and what to do if your car will not start.',DESC)
s=s.replace('Does a dashcam drain the car battery?',H1)
s=s.replace('13 Nov 2026','15 Nov 2026').replace('2026-11-13','2026-11-15')
s=s.replace('Dashcam and car battery, Battery Rescue SG','Changing a car battery, Battery Rescue SG')
# JSON-LD FAQ
ld=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]
def fix(mm):
    d=json.loads(mm.group(1))
    for n in d['@graph']:
        if n.get('@type')=='FAQPage': n['mainEntity']=ld
    return '<script type="application/ld+json">'+json.dumps(d,ensure_ascii=False)+'</script>'
s=re.sub(r'<script type="application/ld\+json">(.*?)</script>',fix,s,count=1,flags=re.S)
open('brbuild/index.html','w',encoding='utf-8').write(s)
# share
W,H=1200,630
im=Image.new('RGB',(W,H),(11,27,77)); d=ImageDraw.Draw(im); d.rectangle([0,0,18,H],fill=(255,196,0))
fb='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; fr='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
d.text((80,82),'DELKOR CAR BATTERY GUIDE',font=ImageFont.truetype(fb,26),fill=(255,196,0))
f=ImageFont.truetype(fb,80)
d.text((80,170),'Can I change my',font=f,fill='white'); d.text((80,258),'own car battery?',font=f,fill='white')
d.text((80,358),'Older cars, start-stop cars and safe steps',font=ImageFont.truetype(fr,30),fill='white')
d.line([80,540,1120,540],fill=(255,196,0),width=3)
d.text((80,570),'Battery Rescue SG  |  by Motoserv  |  8125 9169',font=ImageFont.truetype(fb,26),fill='white')
im.save('brbuild/share.jpg',quality=88)
