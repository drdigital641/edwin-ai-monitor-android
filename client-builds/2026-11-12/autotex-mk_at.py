import re,json,os
from PIL import Image,ImageDraw,ImageFont
W='/tmp/claude-0/wt-night-e2/client-builds/2026-11-12/autotex'
slug='hyundai-kia-running-hot-radiator-thermostat-water-pump'
title='Hyundai or Kia running hot: radiator, thermostat or water pump?'
desc='Hyundai or Kia temperature gauge climbing? The usual causes: low coolant, radiator, radiator fan, thermostat, hoses and water pump, and what to do first.'
url=f'https://autotexautoparts.com.sg/articles/{slug}/'
lead='A Hyundai or Kia that runs hot usually has a problem in the cooling system: low coolant from a leak, a blocked or leaking radiator, a radiator fan that is not running, a stuck thermostat, a split hose or a failing water pump. If the gauge is in the red, stop safely and switch off. Driving on can wreck the engine.'
secs=[
("What should I do first if my Hyundai or Kia is overheating?","<p>Pull over safely, switch the engine off and let it cool. Do not open the radiator cap or the coolant reservoir cap while the engine is hot, because the system is under pressure and hot coolant can spray out. Driving on with the gauge in the red can damage the engine, so call a workshop or tow service rather than carrying on.</p>"),
("Which cooling parts usually cause overheating?","<ul><li>Low coolant: from a leak at a hose, the radiator, the water pump or a loose clamp. Topping up without finding the leak only delays the problem.</li><li>Radiator: a blocked core or a leak at the tanks stops it shedding heat.</li><li>Radiator fan: if it does not spin when the engine is hot, the car runs hot in traffic and in queues, and often cools down once you are moving.</li><li>Thermostat: if it sticks closed, coolant cannot circulate to the radiator and the temperature climbs quickly.</li><li>Upper and lower radiator hoses: a soft, swollen or cracked hose can leak or collapse.</li><li>Radiator cap: a weak cap cannot hold system pressure, which lets the coolant boil at a lower temperature.</li><li>Water pump: a leak at the pump or a worn bearing means coolant is not pushed round the engine.</li></ul>"),
("How can I tell which part is the problem?","<p>Note when it happens. Heating up in slow traffic but fine at speed points to the radiator fan. A temperature that climbs soon after a cold start points to the thermostat or low coolant. Coolant smell, drips under the car or a falling reservoir level point to a leak, so look at the hoses, radiator and pump. A workshop can pressure test the system and confirm the part before you buy.</p>"),
("Can I just top up the coolant and keep driving?","<p>Only as a short-term step, and only when the engine is cold. Coolant does not disappear by itself, so a falling level means a leak or a more serious engine problem. Use the coolant type in your owner's manual, and have the cause found soon.</p>"),
("Should I replace the thermostat or the radiator hoses together?","<p>Workshops often check the thermostat, its housing and the hoses together, because they are on the same coolant circuit and a worn hose or housing can leak after the job. Ask your workshop what it recommends for your car and how old the parts are.</p>"),
("Which cooling parts does Autotex list?","<p>For Hyundai and Kia models sold in Singapore we list radiators, radiator fans, radiator caps, thermostat housings (outlets), and upper and lower radiator hoses, on the <a href=\"../../parts/cooling-aircon/\">cooling &amp; aircon parts page</a>. If you need a part that is not on that list, message us on WhatsApp and ask.</p>"),
("What should I send Autotex to get the right part?","<p>Send your car plate or chassis number, which is printed on the vehicle log card, and the part you think you need. Cooling parts differ by model, generation and engine, so the chassis number saves guesswork. If you are not sure which part has failed, have the cooling system checked first.</p>"),
]
import html as H
faqs=[(h,re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',p.replace('</li>',' '))).strip().replace(' .','.').replace(' ,',',').replace(' :',':')) for h,p in secs]
T=open('/tmp/claude-0/wt-night-c2/client-builds/2026-11-10/autotex/articles/clunk-over-bumps-worn-suspension-parts-hyundai-kia/index.html').read()
old='clunk-over-bumps-worn-suspension-parts-hyundai-kia'
oldt='Clunk over bumps: worn suspension parts on a Hyundai or Kia'
oldd='Clunking over bumps in a Hyundai or Kia? Usual worn parts: stabilizer links, top mounts, bushes, ball joints, tie rods, absorbers, and how to narrow it down.'
t=T
m=re.search(r'<script type="application/ld\+json">(.*?)</script>',t,re.S)
j=json.loads(m.group(1))
img=f'https://autotexautoparts.com.sg/share-{slug}.jpg'
for n in j['@graph']:
    if n['@type']=='FAQPage': n['mainEntity']=[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]
j['@graph'][0]['image']=img
t=t[:m.start(1)]+json.dumps(j,ensure_ascii=False)+t[m.end(1):]
a=t.index('<p class="lead">'); b=t.index('<p class="small muted">')
t=t[:a]+f'<p class="lead">{lead}</p>\n'+t[b:]
a=t.index('<article class="sec art-b">'); b=t.index('<div class="callout">')
t=t[:a]+'<article class="sec art-b"><div class="wrap narrow">'+''.join(f'<h2>{h}</h2>{p}' for h,p in secs)+'\n'+t[b:]
t=t.replace('suspension &amp; steering parts for every Hyundai and Kia model','cooling &amp; aircon parts for every Hyundai and Kia model').replace('../../parts/suspension/','../../parts/cooling-aircon/')
t=t.replace(old,slug).replace(oldt,title).replace(oldd,desc).replace('2026-11-10','2026-11-12').replace('10 Nov 2026','12 Nov 2026')
t=t.replace(' · Website &amp; SEO by <a href="https://pageonesingapore.com/">Page One Singapore</a>','')
assert 'pageonesingapore' not in t and 'suspension' not in t.lower() and old not in t
os.makedirs(f'{W}/articles/{slug}',exist_ok=True)
open(f'{W}/articles/{slug}/index.html','w').write(t)
im=Image.new('RGB',(1200,630),(248,249,250)); d=ImageDraw.Draw(im)
fb='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; fr='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
d.rectangle([0,0,1200,12],fill=(212,42,30))
d.text((70,70),'AUTOTEX',font=ImageFont.truetype(fb,34),fill=(17,22,28))
d.text((70,120),'KOREAN CAR PART STOCKIST  |  HYUNDAI  |  KIA',font=ImageFont.truetype(fr,22),fill=(100,110,125))
f=ImageFont.truetype(fb,58)
for i,l in enumerate(['Hyundai or Kia running hot:','radiator, thermostat','or water pump?']): d.text((70,200+i*84),l,font=f,fill=(17,22,28))
d.rectangle([70,468,230,474],fill=(212,42,30))
d.text((70,495),'Coolant, radiator, fan, thermostat and hoses',font=ImageFont.truetype(fr,28),fill=(100,110,125))
im.save(f'{W}/share-{slug}.jpg',quality=88)
print(len(desc),len(title),len(re.sub('<[^>]+>',' ',''.join(p for _,p in secs)).split()))
