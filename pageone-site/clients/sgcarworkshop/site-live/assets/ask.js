/* "Describe your problem" search. Runs fully in the browser: no AI, no API, no running cost.
   Tier 1 exact: service names, car makes/models, areas, workshop names.
   Tier 2 flexible: everyday and Singlish symptoms, synonyms, plurals and typos mapped to a service and a plain-English "likely issue".
   Tier 3 fallback: closest services as "Did you mean" plus popular workshops. Never an empty result.
   Each typed query is logged anonymously (no ids, no names, digits stripped) through the same write-only "track" beacon as the tap counter. */
(function(root){
'use strict';
var MAKES={toyota:'Toyota',honda:'Honda',nissan:'Nissan',mazda:'Mazda',mitsubishi:'Mitsubishi',suzuki:'Suzuki',subaru:'Subaru',daihatsu:'Daihatsu',lexus:'Lexus',hyundai:'Hyundai',kia:'Kia',ssangyong:'SsangYong',bmw:'BMW',mercedes:'Mercedes-Benz',audi:'Audi',volkswagen:'Volkswagen',volvo:'Volvo',porsche:'Porsche',peugeot:'Peugeot',renault:'Renault',citroen:'Citroen',opel:'Opel',skoda:'Skoda',mini:'MINI',landrover:'Land Rover',jaguar:'Jaguar',ford:'Ford',chevrolet:'Chevrolet',jeep:'Jeep',tesla:'Tesla',byd:'BYD',mg:'MG',proton:'Proton',perodua:'Perodua',maserati:'Maserati',ferrari:'Ferrari',lamborghini:'Lamborghini',fiat:'Fiat',alfa:'Alfa Romeo',dongfeng:'Dongfeng',chery:'Chery',maxus:'Maxus',isuzu:'Isuzu',hino:'Hino',mitsubishifuso:'Mitsubishi'};
var MODELS={corolla:'toyota',altis:'toyota',camry:'toyota',vios:'toyota',yaris:'toyota',hiace:'toyota',alphard:'toyota',vellfire:'toyota',harrier:'toyota',prius:'toyota',wish:'toyota',estima:'toyota',civic:'honda',accord:'honda',jazz:'honda',vezel:'honda',freed:'honda',odyssey:'honda',stepwgn:'honda',crv:'honda',hrv:'honda',lancer:'mitsubishi',attrage:'mitsubishi',outlander:'mitsubishi',asx:'mitsubishi',colt:'mitsubishi',mirage:'mitsubishi',pajero:'mitsubishi',evo:'mitsubishi',swift:'suzuki',vitara:'suzuki',jimny:'suzuki',ertiga:'suzuki',qashqai:'nissan',juke:'nissan',serena:'nissan',sylphy:'nissan',note:'nissan',nv200:'nissan',nv350:'nissan',gtr:'nissan',impreza:'subaru',forester:'subaru',wrx:'subaru',xv:'subaru',cerato:'kia',sportage:'kia',picanto:'kia',avante:'hyundai',elantra:'hyundai',tucson:'hyundai',ioniq:'hyundai',kona:'hyundai',golf:'volkswagen',passat:'volkswagen',polo:'volkswagen',tiguan:'volkswagen',scirocco:'volkswagen',cooper:'mini',cayenne:'porsche',macan:'porsche',carrera:'porsche',mazda3:'mazda',mazda6:'mazda',cx5:'mazda',cx3:'mazda',mx5:'mazda',rx8:'mazda',hilux:'toyota',ranger:'ford',focus:'ford',fiesta:'ford',mustang:'ford',x5:'bmw',x3:'bmw',m3:'bmw',e90:'bmw',f30:'bmw',c200:'mercedes',e200:'mercedes',a180:'mercedes',cla:'mercedes',a4:'audi',a3:'audi',q5:'audi',q3:'audi'};
var MAKE_ALIAS={merc:'mercedes',mercs:'mercedes',benz:'mercedes',vw:'volkswagen',chevy:'chevrolet',beemer:'bmw',bimmer:'bmw',lr:'landrover',citroen:'citroen',toyata:'toyota',misubishi:'mitsubishi',mitsubshi:'mitsubishi',mitsu:'mitsubishi',hundai:'hyundai',hyundi:'hyundai',nisan:'nissan',lexis:'lexus',subaro:'subaru',audio:'audi',merz:'mercedes',kya:'kia'};
var REGION_ALIAS={tampines:'east',pasirris:'east',bedok:'east',simei:'east',paya:'east',marine:'east',punggol:'north-east',hougang:'north-east',sengkang:'north-east',geylang:'central',kallang:'central',orchard:'central',novena:'central',queenstown:'central',tiong:'central',jurong:'west',clementi:'west',boon:'west',bukitpanjang:'west',choa:'west',tengah:'west',pioneer:'west',mandai:'north',lim:'north'};
/* Symptom rules. g = [weight, direct-service-name?, words]. A rule needs score >= t. */
function G(w,d,s){return{w:w,d:d,s:s.split(' ')}}
var RULES=[
{id:'susp',cat:'general-servicing-repair',label:'Suspension and undercarriage',issue:'This sounds like a worn suspension or undercarriage part, such as a bush, absorber, lower arm or drive shaft joint.',t:2,g:[G(2,0,'suspension absorber shock shocks bush bushing lowerarm driveshaft cvjoint tierod linkage arm wobble wobbling steering'),G(1,0,'knock knocking clunk clunking thud thump rattle rattling squeak squeaking creak creaking bang banging vibrate vibration shake shaking pull pulling drift'),G(1,0,'under underneath undercarriage below bottom chassis bump bumps hump humps pothole potholes road wheel wheels corner turning')]},
{id:'aircon',cat:'general-servicing-repair',label:'Aircon',issue:'This sounds like an aircon fault, such as low gas, a leak, a weak compressor, a dirty cooling coil or a blocked condenser.',t:2,g:[G(2,1,'aircon compressor condenser blower evaporator'),G(1,0,'cold warm hot weak smelly smell stink leak leaking noisy noise cooling coil')]},
{id:'idle',cat:'general-servicing-repair',alt:'abs-ecu-module-repair',label:'Engine tuning and diagnosis',issue:'An unstable idle is often a dirty throttle body, worn spark plugs, a vacuum leak or a faulty sensor. A scan and tune-up usually finds the cause.',t:2,g:[G(2,0,'idle idling hunting misfire misfiring stall stalling tuneup'),G(1,0,'unstable rough shaky shaking jerk jerky jerking hesitate hesitation sluggish lag power acceleration vibrate vibration engine')]},
{id:'cooling',cat:'general-servicing-repair',label:'Cooling system',issue:'Overheating usually points to low coolant, a leak, a weak water pump, a stuck thermostat or a blocked radiator. Stop driving if the temperature gauge is in the red.',t:2,g:[G(2,0,'overheat overheating overheated radiator coolant thermostat'),G(1,0,'temperature steam smoke hot leak leaking water engine')]},
{id:'brake',cat:'general-servicing-repair',alt:'abs-ecu-module-repair',label:'Brakes',issue:'This sounds like worn brake pads or discs, or air or fluid problems in the brake system. Brakes are a safety item, so have them checked soon.',t:2,g:[G(2,1,'brake brakes braking pad pads disc discs rotor rotors handbrake'),G(1,0,'squeal squealing squeak grinding grind soft spongy vibrate shake pedal stop stopping')]},
{id:'tyre',cat:'general-servicing-repair',label:'Tyres and alignment',issue:'This sounds like a tyre, wheel or alignment matter, such as uneven wear, a puncture, a bent rim or the car pulling to one side.',t:2,g:[G(2,1,'tyre tire tyres tires alignment balancing rim rims puncture'),G(1,0,'flat pull pulling uneven worn bald vibrate shake wheel wheels')]},
{id:'service',cat:'general-servicing-repair',label:'General servicing',issue:'This is routine servicing, such as an engine oil and filter change, fluids and a general check.',t:2,g:[G(2,1,'service servicing oilchange maintenance tuneup mileage'),G(1,0,'oil filter due routine yearly check general')]},
{id:'ecu',cat:'abs-ecu-module-repair',label:'Warning light, ABS or ECU',issue:'A warning light means the car has stored a fault code. A scan reads the code, and the cause may be a sensor, an ABS pump, a control module or a wiring fault.',t:2,g:[G(2,1,'abs ecu ecm tcm module checkengine airbag limp scanner obd'),G(2,0,'warning'),G(1,0,'light lights lit dashboard dash fault code codes error sensor limp')]},
{id:'gear',cat:'gearbox-repair',label:'Gearbox',issue:'This sounds like a gearbox problem, such as worn clutch packs, low or old gearbox fluid, a faulty valve body or a failing mechatronic or CVT unit.',t:2,g:[G(2,1,'gearbox transmission cvt dsg mechatronic clutch'),G(1,0,'gear gears shift shifting slip slipping jerk jerking harsh delay delayed stuck automatic reverse drive noise whine')]},
{id:'battery',cat:'car-battery',label:'Car battery',issue:'A car that will not start or cranks slowly often has a weak battery, but it can also be the alternator or starter. A battery test tells which.',t:2,g:[G(2,1,'battery batteries nostart jumpstart jump alternator'),G(1,0,'dead flat click clicking crank cranking slow starter start starting dim')]},
{id:'paint',cat:'spray-painting-bodywork',label:'Spray painting and bodywork',issue:'Scratches and dents are usually fixed by touch-up, polishing or a panel respray, depending on how deep the damage is.',t:2,g:[G(2,1,'respray spraypaint paint painting bodywork'),G(2,0,'scratch scratches scratched scrape scrapes scraped dent dents dented bumper'),G(1,0,'kena hit bump accident panel peel peeling flake flaking fade faded oxidised rust crack cracked clearcoat door fender')]},
{id:'accident',cat:'spray-painting-bodywork',label:'Accident repair',issue:'After an accident, a workshop usually checks the damage, handles panel beating and spray painting, and can often help with the insurance claim.',t:2,g:[G(2,0,'accident collision claim claims insurance panelbeating beating'),G(1,0,'tow towing crash crashed bump bumped hit kena damage damaged')]},
{id:'detail',cat:'car-detailing-coating',label:'Car detailing and coating',issue:'Smells, stains and dull paint are usually handled by interior steam cleaning, odour treatment, polishing or a protective coating.',t:2,g:[G(2,1,'detailing detail coating ceramic polish polishing fumigation odour odor grooming'),G(2,0,'smell smelly stink stinky mould mold stain stains stained vomit cigarette'),G(1,0,'dirty clean cleaning interior seat seats carpet dull watermark waterspot wash steam')]},
{id:'wrap',cat:'car-wrap-ppf',label:'Car wrap and PPF',issue:'This is wrap, film or protection work: colour-change vinyl, paint protection film (PPF) or window tint.',t:2,g:[G(2,1,'wrap wrapping ppf film tint tinted vinyl colourchange sticker stickers decal')]},
{id:'parts',cat:'car-parts',label:'Car parts',issue:'You are looking for car parts. Say the car model and the part, so the shop can match it.',t:2,g:[G(2,1,'parts part spare accessories genuine oem aftermarket headlamp headlight taillight mirror grille')]}
];
var CAT_WORDS={};   /* words that name a service directly -> tier 1 */
var STOP=' i a an the my me we is are am was be been have has had got get to of in on at for with and or but not no it its this that there here very so just also please can could would should will do does did how why what when where who which want need needs wanna looking look find search help someone anyone workshop workshops shop shops garage garages car cars vehicle vehicles auto sg singapore near nearby around area lah lor leh sia meh hor ah one abit bit little some still always sometimes when whenever after before while going getting like seem seems sounds sound sounding noise feel feels feeling make makes making ';
var VOCAB={},STOPSET={};
STOP.split(' ').forEach(function(w){if(w)STOPSET[w]=1});
function addV(w){if(w&&w.length>1)VOCAB[w]=1}
RULES.forEach(function(r){r.g.forEach(function(g){g.s.forEach(addV)})});
Object.keys(MAKES).forEach(addV);Object.keys(MODELS).forEach(addV);Object.keys(MAKE_ALIAS).forEach(addV);Object.keys(REGION_ALIAS).forEach(addV);
var PH=[[/ air ?con(d|ditioner|ditioning|ditioned)? /g,' aircon '],[/ a ?c /g,' aircon '],[/ drive ?shafts? /g,' driveshaft '],[/ cv joints? /g,' cvjoint '],[/ lower arms? /g,' lowerarm '],[/ tie rods? /g,' tierod '],
[/ (check engine|engine light|engine warning|engine check) /g,' checkengine '],[/ (airbag|abs|brake|oil|battery|engine) (light|warning)( light)? /g,' warning $1 '],[/ warning light /g,' warning light '],
[/ (cannot|cant|can not|wont|will not|doesnt|does not|dont|do not|not|unable to|fail to|failed to|fails to|refuse to|refuses to|never) (start|starting|turn on|crank|ignite|fire up) /g,' nostart '],[/ (car|engine|battery) (is |was )?dead /g,' nostart dead '],[/ jump ?start(ed|ing)? /g,' jumpstart '],
[/ not (stable|steady|smooth|consistent) /g,' unstable '],[/ (unstable|uneven|rough|hunting|fluctuat\w*) /g,' unstable '],[/ tune ?up /g,' tuneup '],[/ oil change /g,' oilchange '],[/ spray ?paint(ing|ed)? /g,' spraypaint '],[/ body ?work /g,' bodywork '],
[/ paint job /g,' paint '],[/ colou?r change /g,' colourchange '],[/ change (the )?colou?r /g,' colourchange '],[/ steering wheel /g,' steering '],[/ gear ?box(es)? /g,' gearbox '],[/ auto(matic)? (gear|trans\w*) /g,' gearbox '],[/ land ?rover /g,' landrover '],
[/ (mercedes ?benz|mercedes|merc|mercs|benz) /g,' mercedes '],[/ alfa romeo /g,' alfa '],[/ pasir ris /g,' pasirris '],[/ bukit panjang /g,' bukitpanjang '],[/ panel beating /g,' panelbeating '],[/ (spoil|spoilt|spoiled|rosak|kaput|jialat) /g,' broken '],[/ (idling|idles) /g,' idle '],[/ (tyres|tires) /g,' tyre '],
[/ (dun|dont|donot|nt|tak|tk) /g,' not '],[/ ponding| ponded /g,' flooded ']];
function norm(s){s=' '+String(s).toLowerCase().replace(/[‘’'`]/g,'').replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ')+' ';
 for(var i=0;i<PH.length;i++)s=s.replace(PH[i][0],PH[i][1]);return s.replace(/\s+/g,' ').trim()}
function lev(a,b,max){var la=a.length,lb=b.length;if(Math.abs(la-lb)>max)return max+1;var p=[],c,i,j;for(j=0;j<=lb;j++)p[j]=j;
 for(i=1;i<=la;i++){c=[i];var mn=i;for(j=1;j<=lb;j++){var v=Math.min(p[j]+1,c[j-1]+1,p[j-1]+(a.charAt(i-1)===b.charAt(j-1)?0:1));
  if(i>1&&j>1&&a.charAt(i-1)===b.charAt(j-2)&&a.charAt(i-2)===b.charAt(j-1))v=Math.min(v,p[j-2]+1);c[j]=v;if(v<mn)mn=v}
  if(mn>max)return max+1;p=c}return p[lb]}
function stems(t){var o=[t],m;if((m=/^(.{3,})ies$/.exec(t)))o.push(m[1]+'y');if((m=/^(.{3,})(es|s)$/.exec(t))){o.push(m[1]);o.push(t.slice(0,-1))}
 if((m=/^(.{3,}?)(ing|ed)$/.exec(t))){o.push(m[1]);o.push(m[1]+'e');if(/(.)\1$/.test(m[1]))o.push(m[1].slice(0,-1))}return o}
function fixTok(t){if(!t||STOPSET[t]||VOCAB[t])return t;var st=stems(t);for(var i=1;i<st.length;i++)if(VOCAB[st[i]])return st[i];
 if(/\d/.test(t)||t.length<4)return t;var mx=t.length<=5?1:t.length<=8?1:2,best=null,bd=mx+1;
 for(var w in VOCAB){if(w.length<4||w.charAt(0)!==t.charAt(0))continue;var d=lev(t,w,mx);if(d<bd){bd=d;best=w;if(d===1&&mx===1)break}}
 return best||t}
function findMake(toks,joined){for(var i=0;i<toks.length;i++){var t=toks[i];if(MAKE_ALIAS[t])t=MAKE_ALIAS[t];if(MAKES[t])return t;if(MODELS[t])return MODELS[t]}return ''}
function findArea(joined,toks,areas){var best=null,len=0;areas.forEach(function(a){var n=' '+norm(a.name)+' ';var variants=[n];if(/ and /.test(n))n.split(' and ').forEach(function(p){p=p.trim();if(p.length>3)variants.push(' '+p+' ')});
 variants.forEach(function(v){if(joined.indexOf(v)>-1&&v.length>len){best={estate:a.slug,name:a.name,region:a.region};len=v.length}})});
 if(best)return best;
 for(var i=0;i<toks.length;i++){var r=REGION_ALIAS[toks[i]];if(r)return{estate:'',name:toks[i].replace(/^./,function(c){return c.toUpperCase()}),region:r}}
 var RG={north:'north',east:'east',west:'west',central:'central',ne:'north-east',northeast:'north-east',northwest:'north',mobile:'mobile'};
 for(i=0;i<toks.length;i++)if(RG[toks[i]])return{estate:'',name:RG[toks[i]].replace(/^./,function(c){return c.toUpperCase()}),region:RG[toks[i]]};
 return null}
function analyse(raw,data){var s=norm(raw),toks=s.split(' ').filter(Boolean).map(fixTok),have={};
 toks.forEach(function(t){have[t]=1;stems(t).forEach(function(x){have[x]=1})});
 var joined=' '+toks.join(' ')+' ',make=findMake(toks,joined),area=findArea(joined,toks,data.areas||[]),res=[];
 RULES.forEach(function(r,i){var sc=0,dir=true,n=0,part=0;r.g.forEach(function(g){var h=g.s.some(function(w){return have[w]});if(h){sc+=g.w;n++;if(!g.d)dir=false}});
  if(sc>=r.t)res.push({r:r,sc:sc,dir:dir,i:i});else if(sc>0)part+=sc;r.part=part});
 res.sort(function(a,b){return b.sc-a.sc||a.i-b.i});
 var top=res[0]||null,second=null;for(var k=1;k<res.length;k++)if(res[k].r.cat!==top.r.cat){second=res[k];break}
 var close={};RULES.forEach(function(r){var sc=0;r.g.forEach(function(g){if(g.s.some(function(w){return have[w]}))sc+=g.w});if(sc>0)close[r.cat]=Math.max(close[r.cat]||0,sc)});
 return{raw:raw,toks:toks,make:make,area:area,top:top,second:second,close:close,tier:top?(top.dir?1:2):(area?1:3)}}
var api={analyse:analyse,norm:norm,RULES:RULES,MAKES:MAKES};
if(typeof module!=='undefined'&&module.exports){module.exports=api}
root.SGCWAsk=api;
if(typeof document==='undefined')return;
var d=document,form=d.getElementById('finder');if(!form)return;
var inp=d.getElementById('q'),out=d.getElementById('askres'),body=d.getElementById('askbody'),DATA={};
try{DATA=JSON.parse(d.getElementById('askdata').textContent)}catch(e){return}
var cards=[],catName={};function getCards(){if(window.sgcwMore)window.sgcwMore();cards=[].slice.call(d.querySelectorAll('#results .card[data-cat]'));return cards}getCards();(DATA.cats||[]).forEach(function(c){catName[c.slug]=c});
function el(tag,cls,txt){var e=d.createElement(tag);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e}
function cardsFor(cats,area,fallback){var list=getCards().filter(function(c){return cats.indexOf(c.getAttribute('data-cat'))>-1});
 if(area){var f=list.filter(function(c){var r=' '+c.getAttribute('data-regions')+' ',s=' '+c.getAttribute('data-search')+' ';
  if(area.estate)return s.indexOf(' '+norm(area.name)+' ')>-1||s.indexOf(' '+norm(area.name).split(' and ')[0]+' ')>-1;return r.indexOf(' '+area.region+' ')>-1});
  if(f.length||!fallback)return{list:f,relaxed:false};return{list:list,relaxed:true}}
 return{list:list,relaxed:false}}
function nameMatch(a){var out2=[];cards.forEach(function(c){var n=norm((c.querySelector('h3')||{}).textContent||'').split(' ').filter(function(w){return w.length>3&&!STOPSET[w]&&['auto','motor','motors','pte','ltd','service','services','centre','center','enterprise','engineering','trading'].indexOf(w)<0});
  if(n.length&&n.some(function(w){return a.toks.indexOf(w)>-1}))out2.push(c)});return out2}
function prefill(node,a){var wa=node.querySelector('a[href*="wa.me"]');if(!wa)return;var extra='';
 if(a.make)extra+='\nMy car: '+MAKES[a.make];if(a.raw)extra+='\nWhat I need: '+a.raw.trim().slice(0,160);if(!extra)return;
 try{var u=new URL(wa.href),t=u.searchParams.get('text')||'';u.searchParams.set('text',t+'\n'+extra);wa.href=u.toString()}catch(e){}}
function pwords(c){var s=c.__pw;if(!s){s={};(c.getAttribute('data-profile')||'').split(' ').forEach(function(w){if(w){s[w]=1;stems(w).forEach(function(x){s[x]=1})}});c.__pw=s}return s}
var GEN={car:1,cars:1,workshop:1,garage:1,repair:1,service:1,servicing:1,the:1,for:1,and:1,my:1,has:1,have:1,with:1,problem:1,need:1,fix:1,not:1,got:1};
function qtoks(a){return a.toks.filter(function(t){return t.length>2&&!STOPSET[t]&&!GEN[t]})}
function mentionHits(c,a){var m=(c.getAttribute('data-mention')||'').split('|').filter(Boolean),qt=qtoks(a),qs={};qt.forEach(function(t){qs[t]=1;stems(t).forEach(function(x){qs[x]=1})});
 if(a.make)qs[a.make]=1;return m.filter(function(x){return norm(x).split(' ').some(function(w){return qs[w]||stems(w).some(function(y){return qs[y]})})})}
function profScore(c,a){if(!c.getAttribute('data-profile'))return 0;var pw=pwords(c),sc=0;qtoks(a).forEach(function(t){if(pw[t]||stems(t).some(function(x){return pw[x]}))sc+=1});
 if(a.make&&pw[a.make])sc+=3;sc+=mentionHits(c,a).length*3;return sc}
function ranked(list,a){return list.map(function(c,i){return{c:c,s:profScore(c,a),i:i}}).sort(function(x,y){return y.s-x.s||x.i-y.i}).map(function(x){return x.c})}
function why(n,c,a){var h=mentionHits(c,a);if(!h.length)return;var p=el('p','why');p.appendChild(el('b',null,'Customers mention: '));p.appendChild(d.createTextNode(h.slice(0,3).join(', ')));var bd=n.querySelector('.bd');if(bd){var acts=bd.querySelector('.acts');bd.insertBefore(p,acts||null)}}
function clone(c,a){var n=c.cloneNode(true);why(n,c,a);n.hidden=false;n.removeAttribute('data-search');[].forEach.call(n.querySelectorAll('[id]'),function(x){x.removeAttribute('id')});prefill(n,a);return n}
function chip(label,val){var s=el('span','achip');s.appendChild(el('small',null,label+': '));s.appendChild(el('b',null,val));return s}
function grid(list,a,max){var g=el('div','grid'),extra=null;list=ranked(list,a);list.forEach(function(c,i){var n=clone(c,a);if(i>=max)n.hidden=true;g.appendChild(n)});
 if(list.length>max){extra=el('button','btn alt askmore','Show all '+list.length+' workshops');extra.type='button';extra.addEventListener('click',function(){[].forEach.call(g.children,function(x){x.hidden=false});extra.hidden=true})}
 var w=el('div');w.appendChild(g);if(extra)w.appendChild(extra);return w}
function popular(a){var p=cards.filter(function(c){return c.getAttribute('data-tier')==='premium_leadgen'});if(p.length<3)p=p.concat(cards.filter(function(c){return c.getAttribute('data-tier')==='premium'}));return p.slice(0,4)}
function didYouMean(a,note){var wrap=el('div','dym');wrap.appendChild(el('h3',null,note||'Did you mean one of these?'));var row=el('div','opts');
 var cats=(DATA.cats||[]).slice().sort(function(x,y){return (a.close[y.slug]||0)-(a.close[x.slug]||0)});var showN=Object.keys(a.close).length?Math.min(3,Math.max(1,Object.keys(a.close).length)):4;
 cats.slice(0,Math.max(showN,3)).forEach(function(c){var b=el('button','opt dymb',c.short);b.type='button';b.addEventListener('click',function(){render(Object.assign({},a,{top:{r:{cat:c.slug,label:c.short,issue:c.blurb||''}},tier:3,forced:true}),true)});row.appendChild(b)});
 wrap.appendChild(row);return wrap}
function guidesFor(a){var n=' '+norm(a.raw||'')+' ',out=[];(DATA.guides||[]).forEach(function(g){var s=0;g.kw.forEach(function(k){var kk=norm(k);if(kk&&n.indexOf(' '+kk+' ')>=0)s+=kk.length>3?2:1});if(s)out.push({g:g,s:s})});out.sort(function(x,y){return y.s-x.s});return out.slice(0,2).map(function(x){return x.g})}
function guideBox(list){var w=el('div','guidebox');w.appendChild(el('h3',null,'Read our guide'));list.forEach(function(g){var p=el('p');var a=el('a',null,g.h1);a.href=g.path;a.setAttribute('data-cta','guide_'+g.slug);p.appendChild(a);w.appendChild(p)});return w}
function render(a,viaChip){body.textContent='';var chips=el('div','achips'),r=a.top&&a.top.r,cats=[],area=a.area;
 if(a.make)chips.appendChild(chip('Car',MAKES[a.make]));if(area)chips.appendChild(chip('Area',area.name));if(r)chips.appendChild(chip('Service',r.label));
 var nm=a.tier!==3||a.forced?nameMatch(a):[];
 var pm=(!r&&!nm.length)?ranked(cards.filter(function(c){return profScore(c,a)>=(a.make?3:2)}),a).filter(function(c){return profScore(c,a)>0}).slice(0,9):[];
 if(r){cats=[r.cat].concat(r.alt?[r.alt]:[])}
 var head=el('h2','ah',(r||area||nm.length||pm.length)?'Here is what we understood':'We could not match that exactly');body.appendChild(head);if(chips.children.length)body.appendChild(chips);
 var gl=guidesFor(a);if(gl.length)body.appendChild(guideBox(gl));
 if(r&&r.issue){var it=el('p','likely');it.appendChild(el('b',null,'Likely issue: '));it.appendChild(d.createTextNode(r.issue+(a.forced?'':' This is a general guide, not a diagnosis. A workshop has to inspect the car to be sure.')));body.appendChild(it)}
 var shown=0,shownSet={};function mark(c){shownSet[c.getAttribute('data-tier')+c.querySelector('h3').textContent]=1}
 if(nm.length&&!r){body.appendChild(el('h3','sub','Matching workshop'));body.appendChild(grid(nm,a,6));shown=nm.length;nm.forEach(mark)}
 else if(pm.length&&!r){body.appendChild(el('h3','sub','Matches from what customers mention'));body.appendChild(el('p','fine','Found by matching your words to each profile: services, car brands and what customers say.'));body.appendChild(grid(pm,a,6));shown=pm.length;pm.forEach(mark)}
 else if(cats.length||area){var c=cardsFor(cats.length?cats:(DATA.cats||[]).map(function(x){return x.slug}),area,true);
  if(c.relaxed)body.appendChild(el('p','fine','No listed workshop in '+area.name+' yet for this, so here are others you can message.'));
  if(c.list.length){body.appendChild(el('h3','sub',(area&&!c.relaxed?'Workshops in '+area.name:'Workshops')+(r?' for '+r.label.toLowerCase():'')));body.appendChild(grid(c.list,a,6));shown=c.list.length;c.list.forEach(mark)}
  var ex=cards.filter(function(x){return c.list.indexOf(x)<0&&mentionHits(x,a).length});if(ex.length){body.appendChild(el('h3','sub','Also mentioned by customers'));body.appendChild(grid(ex,a,3));ex.forEach(mark)}}
 if(!shown||(!r&&!pm.length)){body.appendChild(didYouMean(a,r?null:(a.make?'What does your '+MAKES[a.make]+' need?':'Did you mean...')));
  var p=popular(a).filter(function(c){return !shownSet[c.getAttribute('data-tier')+c.querySelector('h3').textContent]});if(p.length){body.appendChild(el('h3','sub','Popular workshops'));body.appendChild(grid(p,a,4))}}
 else if(a.second){var alt=a.second.r;var al=el('p','fine');al.appendChild(d.createTextNode('Could also be '+alt.label.toLowerCase()+'. '));var b=el('button','linkbtn','Show those workshops');b.type='button';b.addEventListener('click',function(){render(Object.assign({},a,{top:a.second,second:null,tier:a.second.dir?1:2}),true)});al.appendChild(b);body.appendChild(al)}
 var cl=el('button','linkbtn askclear','Clear this search');cl.type='button';cl.addEventListener('click',function(){inp.value='';var any=form.querySelector('input[name=svc][value=""]');if(any)any.checked=true;out.hidden=true;inp.focus()});body.appendChild(cl);
 out.hidden=false;if(!viaChip||true){try{out.scrollIntoView({behavior:window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'})}catch(e){}}
 body.setAttribute('tabindex','-1');
 if(!viaChip)log(a,r?r.id:'none');}
/* Anonymous log: normalized words only (no word with 3+ digits, no @ or links), a random per-visit id, device and referrer. No IP, name or phone is stored. */
var LIVE_HOST='sgcarworkshop.sg',APP='6ac7f2548a9c3877449e2772',seen={};
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function keep(k){try{var v=sessionStorage.getItem(k);if(!v){v=rid();sessionStorage.setItem(k,v)}return v}catch(x){return rid()}}
function scrub(raw){if(/@|https?:|www\./i.test(raw))return '';return norm(raw).split(' ').filter(function(w){return w&&!/\d{3,}/.test(w)}).join(' ').slice(0,60)}
function log(a,rule){try{var h=location.hostname.replace(/^www\./,''),site=h===LIVE_HOST?'sgcarworkshop':(h==='pageonesingapore.com'?'sgcarworkshop-test':'');
 if(!site||navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.webdriver)return;var q=scrub(a.raw);if(!q||seen[q])return;seen[q]=1;
 var ref=('t'+a.tier+'|'+rule+'|'+(a.make||'-')+'|'+(a.area?(a.area.estate||a.area.region):'-')).slice(0,40),ua=navigator.userAgent;
 var body2=JSON.stringify({entity:'CtaClick',site:site,session_id:keep('sgcw-sid'),page_path:location.pathname,referrer:(d.referrer||'').slice(0,300),
  device_type:/Mobi|Android|iPhone/i.test(ua)?'mobile':/iPad|Tablet/i.test(ua)?'tablet':'desktop',cta_type:'search',cta_label:q,enquiry_ref:ref});
 var url='https://base44.app/api/apps/'+APP+'/functions/track',sent=false;
 if(navigator.sendBeacon){try{sent=navigator.sendBeacon(url,new Blob([body2],{type:'application/json'}))}catch(x){}}
 if(!sent&&window.fetch){fetch(url,{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:body2}).catch(function(){})}}catch(x){}}
form.addEventListener('submit',function(e){e.preventDefault();var v=inp.value.trim();if(!v){inp.focus();return}
 var any=form.querySelector('input[name=svc][value=""]');if(any&&!any.checked){any.checked=true}render(analyse(v,DATA))});
inp.addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();form.dispatchEvent(new Event('submit',{cancelable:true,bubbles:true}))}});
/* Category chips run the same results panel (no typing needed). */
form.addEventListener('change',function(e){var t=e.target;if(!t||t.name!=='svc')return;
 if(!t.value){out.hidden=true;return}var c=catName[t.value];if(!c)return;inp.value='';
 render({raw:'',toks:[],make:'',area:null,close:{},second:null,forced:true,tier:1,top:{r:{cat:c.slug,label:c.short,issue:c.blurb||''}}},true)});
})(typeof window!=='undefined'?window:this);
