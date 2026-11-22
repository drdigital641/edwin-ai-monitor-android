"""Seed registry.json (22 Nov 2026). Status/live_date come from the Controller Client records (controller_slug); run sync_controller.py to refresh."""
import json
PO = 'pageone'; AS = 'autoseo'
IND_PO = {'car-workshops':'Car workshops','detailing':'Detailing, wraps and grooming','car-parts':'Car parts and products',
 'car-dealers':'Car dealers','property':'Property agents','home':'Home, renovation and cleaning',
 'finance':'Finance and professional services','travel':'Travel and stays','other':'Other local businesses'}
IND_AS = {'car-workshops':'Car workshops','car-dealerships':'Car dealerships','car-aircon-specialists':'Car aircon specialists',
 'car-detailing':'Car detailing and coating','ev-hybrid-specialists':'EV and hybrid specialists','battery-spare-parts':'Batteries and spare parts',
 'equipment-diagnostic-tools':'Equipment and diagnostic tools','tyre-shops':'Tyre shops','machinery-movers':'Machinery movers',
 'hair-salons':'Hair salons','food':'Food'}
R = []
def add(id, name, agency, vis, ind, host='', slug=None, preview='', note='', **card):
    lab = (IND_PO if vis != 'white-label' else IND_AS).get(ind, ind)
    r = dict(id=id, name=name, agency=agency, visibility=vis, status=None, live_date=None, industry_id=ind, industry_label=lab,
             host=host, url=('https://%s/' % host) if host else '', preview_url=preview, controller_slug=slug or id, note=note)
    if vis == 'public': r['card'] = card
    R.append(r)
# own sites (never counted)
add('pageone','Page One Singapore',PO,'own','other','pageonesingapore.com',slug='-')
add('sggarage','SG Garage',PO,'own','car-workshops','sggarage.com',slug='-',note='Own workshop; may appear as a case study, never counted')
add('sgcarworkshop','SG Car Workshop',PO,'own','other','sgcarworkshop.sg')
add('autoseo-my','AutoSEO.my',AS,'own','other','autoseo.my',slug='autoseo-site')
# Page One public
for a in [('ecu-clinic','The ECU Clinic','car-workshops','theecuclinicsg.com','ecu-clinic'),('jacky-gearbox','Jacky Gearbox','car-workshops','jackygearbox.com','dmts'),
 ('contiexpert','ContiExpert by Volt Autocare','car-workshops','contiexpert.sg','contiexpert'),('new-zen-werkz','New Zen Werkz','car-workshops','newzenwerkz.com.sg','new-zen-werkz'),
 ('jk-transmission','J & K Transmission Specialist','car-workshops','jktransmissionspecialist.com','jk-transmission'),
 ('cleanic','Cleanic Detailing','detailing','cleanicdetailing.com','loo-san-choon'),('wrapstar','Wrapstar Autostyle','detailing','wrapstarautostyle.com','wrapstar'),
 ('ev-body-parts','EV Body Parts','car-parts','evbodyparts.sg','ev-body-parts'),('autotex','Autotex','car-parts','autotexautoparts.com.sg','autotex'),
 ('cska-auto','CSKA Auto Enterprise','car-parts','cskatrading.com','cska-auto'),('xado','XADO Singapore','car-parts','xado-shop.sg','xado'),
 ('star-performance','Star Performance Motor','car-dealers','starperformancemotor.com','star-performance'),
 ('alicia','Alicia Ong Property','property','aliciaongproperty.com','-'),('lilian-properties','Ng Li Lian','property','lilianproperties.com','lilian-properties'),
 ('jayven-ang','Jayven Ang','property','jayvenang.sg','jayven-ang'),('sofacare','SofaCare SG','home','sofacaresg.com','sofacare'),
 ('maison','Maison Interior Design','home','maisoninteriordesign.sg','maison-interior-design'),('fitout','SG Commercial Fitout','home','commercialfitout.sg','rc-design-build'),
 ('urban-eco','Urban Eco Solutions','home','urbanecosolutions.com','urban-eco'),('danny','Danny Chua Financial','finance','dannychuafinancial.com','-'),
 ('benjamin-poon','Benjamin Poon','finance','planwithben.sg','benjamin-poon'),('jb-staycations','JB Staycations','travel','jbstaycations.com','jb-staycation'),
 ('aivs','AI Vending Solution','other','aivs.sg','aivs'),('sgcaraccident','SGCarAccident','other','sgcaraccident.sg','sgcaraccident')]:
    add(a[0],a[1],PO,'public',a[2],a[3],slug=a[4],screenshot=a[3]+'.webp')
R[-1]['card']['tagline'] = 'Step-by-step help after a car accident in Singapore, with the next step on WhatsApp.'
# Page One in build (Controller preview)
for s,n in [('hyper-power','Hyper Power'),('moon-wiper','Moon Wiper'),('exn-lube','EXN Lube'),('ape-champs-swim','Ape Champs Swim'),('carku','Carku')]:
    add(s,n,PO,'public','other',preview='https://pageonesingapore.com/preview/%s/'%s)
# White-label live (AutoSEO)
for a in [('hx-auto','HX Auto Service','car-workshops','hxautoservice.com.my'),('cch-automotive','CCH Automotive','car-workshops','cchautomotive.my'),
 ('benz-world','Benz World','car-workshops','benzworld.my'),('emats','EMATS','car-workshops','ecumats.my'),('carzy-world','Carzy World','car-workshops','carzyworld.com.my'),
 ('mykar','MyKar World','car-dealerships','mykar.my','dongfeng-jb'),('apcar','Ap Car Air-Cond Centre','car-aircon-specialists','apcar.com.my'),
 ('klar-details','Klar Details','car-detailing','klardetails.com.sg'),('rasa-sayang','Rasa Sayang Automotive','ev-hybrid-specialists','rasasayangautomotive.com'),
 ('hybrid-world','Hybrid World','ev-hybrid-specialists','hybridworld.com.my'),('sp-precision-parts','S & P Precision Parts','battery-spare-parts','spprecisionparts.my'),
 ('battery-rescue','Battery Rescue','battery-spare-parts','batteryrescue.sg'),('ktech','K Tech','equipment-diagnostic-tools','ktech.my'),
 ('overseas-tyre','Overseas Tyre And Services','tyre-shops','overseastyre.my')]:
    add(a[0],a[1],AS,'white-label',a[2],a[3],slug=a[4] if len(a)>4 else a[0])
# White-label in build (AutoSEO previews)
for s,n,i in [('jt-autoworks','JT Autoworks','car-workshops'),('mcs-auto-spray-painting','MCS Auto Spray Painting','car-workshops'),
 ('lt-automart','LT Automart','car-dealerships'),('advance-machinery-movers','Advance Machinery Movers','machinery-movers'),
 ('studio-87','Studio 87','hair-salons'),('hock-chuan-hiong','Hock Chuan Hiong','food'),('911garage','911 Garage','car-workshops')]:
    add(s,n,AS,'white-label',i,preview='https://autoseo.my/preview/%s/'%s)
json.dump({'as_of':None,'rules':'agency=pageone|autoseo; visibility=public|white-label|own; status from Controller Client.status (live|preview->in_build|dormant); own rows never counted; white-label rows never named on Page One',
           'records':R}, open('registry.json','w'), indent=1, ensure_ascii=False)
print(len(R))
