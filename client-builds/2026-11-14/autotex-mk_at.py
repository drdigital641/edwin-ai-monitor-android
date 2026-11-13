import re,json,os
from PIL import Image,ImageDraw,ImageFont
B='client-builds/'
W=B+'2026-11-14/autotex'
slug='foggy-yellow-headlamp-replace-or-restore-hyundai-kia'
title='Foggy or yellow headlamp: replace or restore?'
desc='Foggy or yellowed headlamp on your Hyundai or Kia? How to tell if it can be restored or needs a new unit, what to check first, and what to send us.'
lead='A foggy or yellow headlamp is usually the outer plastic lens clouding or yellowing with age and sun. If it is only hazy on the outside, a workshop can often polish and re-coat it. If there is moisture inside, a crack, a broken mounting tab or a burnt housing, replacing the headlamp unit is the safer fix.'
secs=[
("Why does a headlamp turn foggy or yellow?","<p>Most headlamp lenses are plastic with a clear protective coating. Years of sun, heat, rain and car washing can wear the coating down, so the plastic turns hazy or yellow and less light gets through at night. This is a surface problem on the outside of the lens.</p>"),
("Can a foggy headlamp be restored?","<p>Often, yes, when the haze is only on the outside. A workshop sands and polishes the lens, then adds a new protective coat. Ask the workshop to explain what it will do and how long the result is expected to last, because a lens restored without a new coating can cloud again.</p>"),
("When should I replace the headlamp unit instead?","<ul><li>Moisture or water droplets inside the lamp: the seal has failed, and the fog is on the inside where polishing cannot reach.</li><li>A crack or chip in the lens, or a missing piece.</li><li>Broken mounting tabs, so the lamp no longer sits firmly in the body.</li><li>A melted or burnt housing or reflector, or a reflector that has gone dull.</li><li>Damage from an accident.</li></ul>"),
("How can I tell if the fog is inside or outside?","<p>Wipe the outside of the lens with a clean damp cloth. If the haze stays, check from the side. A cloudy film that you can feel as rough or sticky on the outside is a surface problem. Beads or a misty film that you cannot touch means moisture inside the lamp, which usually points to a failed seal or a cracked housing. If you are unsure, ask a workshop to look at it.</p>"),
("Should I replace both headlamps?","<p>Not always. Replace only the side that is damaged. If the other lamp is also cloudy, restoring or replacing both gives an even beam and even colour, but that is your choice. Left and right units are different parts, so tell us which side you need.</p>"),
("Which lamp parts does Autotex list?","<p>For Hyundai and Kia models sold in Singapore we list headlamps, tail lamps and fog lamps on the <a href=\"../../parts/lamps/\">lamps page</a>. If the unit you need is not on the list, message us on WhatsApp and ask.</p>"),
("What should I send Autotex to get the right headlamp?","<p>Send your car plate or chassis number, which is printed on the vehicle log card, the side (left or right) and a photo of the lamp. Headlamps differ by model, generation and trim, so the chassis number saves guesswork.</p>"),
]
faqs=[(h,re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',p.replace('</li>',' '))).strip().replace(' .','.').replace(' ,',',').replace(' :',':')) for h,p in secs]
T=open(B+'2026-11-12/autotex/articles/hyundai-kia-running-hot-radiator-thermostat-water-pump/index.html').read()
old='hyundai-kia-running-hot-radiator-thermostat-water-pump'
oldt='Hyundai or Kia running hot: radiator, thermostat or water pump?'
oldd='Hyundai or Kia temperature gauge climbing? The usual causes: low coolant, radiator, radiator fan, thermostat, hoses and water pump, and what to do first.'
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
t=t.replace('cooling &amp; aircon parts for every Hyundai and Kia model','lamps for every Hyundai and Kia model').replace('../../parts/cooling-aircon/','../../parts/lamps/')
t=t.replace(old,slug).replace(oldt,title).replace(oldd,desc).replace('2026-11-12','2026-11-14').replace('12 Nov 2026','14 Nov 2026')
assert 'pageonesingapore' not in t and 'cooling' not in t.lower() and old not in t
os.makedirs(f'{W}/articles/{slug}',exist_ok=True)
open(f'{W}/articles/{slug}/index.html','w').write(t)
im=Image.new('RGB',(1200,630),(248,249,250)); d=ImageDraw.Draw(im)
fb='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; fr='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
d.rectangle([0,0,1200,12],fill=(212,42,30))
d.text((70,70),'AUTOTEX',font=ImageFont.truetype(fb,34),fill=(17,22,28))
d.text((70,120),'KOREAN CAR PART STOCKIST  |  HYUNDAI  |  KIA',font=ImageFont.truetype(fr,22),fill=(100,110,125))
f=ImageFont.truetype(fb,58)
for i,l in enumerate(['Foggy or yellow headlamp:','replace or restore?']): d.text((70,200+i*84),l,font=f,fill=(17,22,28))
d.rectangle([70,468,230,474],fill=(212,42,30))
d.text((70,495),'Surface haze, moisture inside, cracks and tabs',font=ImageFont.truetype(fr,28),fill=(100,110,125))
im.save(f'{W}/share-{slug}.jpg',quality=88)
print(len(desc),len(title+' | Autotex'),len(re.sub('<[^>]+>',' ',''.join(p for _,p in secs)).split()), len(re.sub('<[^>]+>','',lead).split()))
