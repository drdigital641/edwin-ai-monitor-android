/* p1-cta.js v4.2 (17 Nov 2026): CTA tap counter -> Page One Controller "track" fn. One file per site, loaded on every page.
   maison-interior-design = the Controller Client slug. Counts whatsapp (wa.me / api.whatsapp.com / whatsapp: links, WhatsApp forms and
   window.open to WhatsApp), call (tel:), email (mailto:), booking, form_submit. Placement: data-ref on the link or a parent,
   else worked out (header, nav, footer, float, sticky, hero, article, section id), sent as "placement | button text".
   v4.2: every tap is still sent, but a repeat of the same CTA type on the same page within 30 minutes of the visit's first
   one is marked repeat:1 (the Controller shows unique visits and raw taps apart). Sends the browser's user agent text
   so the Controller can tell mobile from desktop. Two features switched on per site in CFG below (template: both off):
   CFG.ref  = short page code added to every pre-filled WhatsApp text, e.g. "(Ref: ML-merpati-meadow)", made from the page
              slug and stored on the tap record (enquiry_ref) so a chat can be matched to its page.
   CFG.form = short enquiry form (name, 8-digit SG mobile, project) saved to the Controller as an Enquiry record, with a
              honeypot, a minimum fill time and a per-tab limit (the Controller rate-limits too). Mounted where CFG says,
              or in any element with data-p1-form.
   Test mode: open any page with ?p1test=1 and every tap and enquiry in that tab is stored as a test (never counted).
   Previews (pageonesingapore.com/preview/..., autoseo.my/preview/...) always send test taps. No IP, no fingerprinting. */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,''),pv=/^\/preview\//.test(location.pathname);
if(h==='localhost'||(h==='pageonesingapore.com'&&!pv))return;window.__p1cta=4.2;var SITE='maison-interior-design';
/*CFG*/var CFG={ref:{pre:'MID',map:[['/new-launches/','ML']],hello:"Hi Maison Interior Design, I'd like to ask about my renovation."},
form:{wa:'6593391185',mounts:[{path:'^/(new-launches/([^/]+/)?)?$',before:'section.cta.dark'},{path:'^/contact/',sel:'#cform'}],
cls:{form:'cform',h:'display',btn:'btn dark-b',wa:'btn ghost-d',sec:'sec',wrap:'wrap',title:'display'},
title:function(p){return p?'Free layout plan for your '+p+' home':'Tell us about your space'},
sub:'Leave your name and mobile. Maison will WhatsApp you shortly with ideas and an itemised quote.',
h:'Send an enquiry',lName:'Name',lMobile:'Mobile (8 digits)',lProject:'Project or interest',phProject:'e.g. 4-room BTO, condo, café',send:'Send enquiry',
consent:'By submitting you agree Maison may contact you about your enquiry.',privacy:'/privacy/',privacyText:'Privacy policy',
thanks:'Thank you, Maison will WhatsApp you shortly.',waBtn:'WhatsApp us now',waNow:'Or WhatsApp us now',
waText:function(p){return p?"Hi Maison, I'd like to ask about my "+p+" renovation.":"Hi Maison Interior Design, I'd like to discuss my renovation."},
waAfter:function(n,p){return 'Hi Maison, I just sent an enquiry on your website. Name: '+n+(p?'. Project: '+p:'')+'.'},
project:function(){var m=location.pathname.match(/^\/new-launches\/([^\/]+)\//);if(!m)return'';var e=document.querySelector('h1'),t=e?e.textContent.replace(/\s+/g,' ').trim().replace(/\s+(Renovation|Interior|Home|Design)\b.*$/i,''):'';return t&&t.length<60?t:m[1].replace(/-/g,' ').replace(/\b[a-z]/g,function(c){return c.toUpperCase()})}}};/*/CFG*/
var API='https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',d=document,REP=30*60*1000;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,BOOK=/calendly\.com|setmore\.com|simplybook|fresha\.com|square\.site\/book|book\.squareup|youcanbook\.me|\/book(ing)?(-now)?\/?(\?|#|$)|appointment/i,last={},S=null,waOpen=0,UA=(navigator.userAgent||'').slice(0,200),BOT=(function(){try{return navigator.webdriver===true||/bot|crawl|spider|slurp|headless|lighthouse|pagespeed|gtmetrix|pingdom|phantomjs|selenium|puppeteer|playwright/i.test(UA)}catch(e){return false}})();
var T=pv||(function(){var q=/[?&]p1test=1(&|$)/.test(location.search);try{if(q)sessionStorage.setItem('p1test','1');return sessionStorage.getItem('p1test')==='1'}catch(e){return q}})();
var MOB=/Mobi|Android|iPhone|iPad/i.test(UA)?'mobile':'desktop';
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=rid();sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function vid(){try{var k='p1cta_vid',v=localStorage.getItem(k);if(!v){v=rid();localStorage.setItem(k,v)}return v}catch(e){return''}}
function visit(){try{var s=JSON.parse(sessionStorage.getItem('p1cta_v')||'null');if(!s){var q=new URLSearchParams(location.search),r=d.referrer||'',rh='';try{rh=new URL(r).hostname.replace(/^www\./,'')}catch(e){}
s={t:Date.now(),l:location.pathname.slice(0,200),r:rh===h?'':r.slice(0,300),us:(q.get('utm_source')||'').slice(0,100),um:(q.get('utm_medium')||'').slice(0,100),uc:(q.get('utm_campaign')||'').slice(0,100),
ad:q.get('gclid')||q.get('gbraid')||q.get('wbraid')?'google':q.get('fbclid')?'facebook':q.get('msclkid')?'microsoft':q.get('ttclid')?'tiktok':'',n:0}}
s.n++;sessionStorage.setItem('p1cta_v',JSON.stringify(s));return s}catch(e){return null}}
S=visit();
/* page code from the slug: CFG.ref.map [prefix, code] pairs first (e.g. /new-launches/<slug>/ -> ML-<slug>), else pre-<last part>, home = pre-home */
function pcode(p){var r=CFG.ref||{},m=r.map||[],i,seg;p=p||location.pathname;
for(i=0;i<m.length;i++){if(p.indexOf(m[i][0])===0){seg=p.slice(m[i][0].length).split('/')[0];if(seg)return(m[i][1]+'-'+seg).slice(0,40)}}
seg=p.split('/').filter(Boolean).pop();return((r.pre||'P1')+'-'+(seg?seg.replace(/\.html?$/i,'').toLowerCase():'home')).slice(0,40)}
var REF=CFG.ref?pcode():'';
function withRef(u){try{u=String(u||'');if(!REF||!WA.test(u))return u;var q=u.indexOf('?'),base=q<0?u:u.slice(0,q),ps=q<0?[]:u.slice(q+1).split('&'),txt=null,rest=[],i,kv;
for(i=0;i<ps.length;i++){if(!ps[i])continue;kv=ps[i].split('=');if(kv[0]==='text')txt=decodeURIComponent(kv.slice(1).join('=').replace(/\+/g,' '));else rest.push(ps[i])}
if(txt&&/\(Ref: [^)]*\)\s*$/.test(txt))return u;txt=(txt&&txt.trim()?txt.trim():(CFG.ref.hello||'Hi'))+' (Ref: '+REF+')';
rest.unshift('text='+encodeURIComponent(txt));return base+'?'+rest.join('&')}catch(e){return u}}
function tagLinks(){if(!REF)return;var a=d.querySelectorAll('a[href]'),i,x,y;for(i=0;i<a.length;i++){x=a[i].getAttribute('href');if(WA.test(x)){y=withRef(x);if(y!==x)a[i].setAttribute('href',y)}}}
function place(a){if(!a||!a.closest)return'';var r=a.closest('[data-ref]');if(r)return r.getAttribute('data-ref');
try{for(var e=a;e&&e!==d.body;e=e.parentElement){var p=getComputedStyle(e).position;if(p==='fixed')return'float';if(p==='sticky')return'sticky'}}catch(x){}
if(a.closest('header,.hd,.header,.site-header'))return a.closest('nav')?'nav':'header';if(a.closest('nav'))return'nav';if(a.closest('footer,.ft,.footer,.site-footer'))return'footer';
if(a.closest('form'))return'form';if(a.closest('.hero,[class*="hero"]'))return'hero';var s=a.closest('section[id],article,section[class]');
if(s){if(s.tagName==='ARTICLE')return'article';return'section:'+(s.id||String(s.className).split(' ')[0]).slice(0,30)}return'body'}
/* repeat = same CTA type on the same page already counted in this visit (session) within the last 30 minutes */
function rep(type){try{var k='p1cta_seen',m=JSON.parse(sessionStorage.getItem(k)||'{}'),key=type+'|'+location.pathname,n=Date.now();if(m[key]&&n-m[key]<REP)return 1;m[key]=n;sessionStorage.setItem(k,JSON.stringify(m))}catch(e){}return 0}
function tz(){try{return Intl.DateTimeFormat().resolvedOptions().timeZone||''}catch(e){return''}}
function post(body){return fetch(API,{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify(body)})}
function send(a,type,lab0){type=String(type||'whatsapp').toLowerCase().replace(/[^a-z0-9_]+/g,'_').slice(0,40);var n=Date.now();if(last[type]&&n-last[type]<1500)return;last[type]=n;var s=S||{};
var txt=lab0||(a?String(a.getAttribute('aria-label')||a.textContent||a.getAttribute('name')||a.id||''):''),pl=place(a);
var lab=((pl?pl+' | ':'')+txt).replace(/\s+/g,' ').trim().slice(0,60);
try{post({entity:'CtaClick',site:SITE,cta_type:type,session_id:sid(),visitor_id:vid(),page_path:location.pathname.slice(0,200),
device_type:MOB,referrer:s.r!=null?s.r:(d.referrer||'').slice(0,300),page_referrer:(d.referrer||'').slice(0,300),
landing_path:s.l||'',utm_source:s.us||'',utm_medium:s.um||'',utm_campaign:s.uc||'',ad_click:s.ad||'',pages_viewed:s.n||1,secs_on_site:s.t?Math.round((n-s.t)/1000):0,
cta_label:lab,enquiry_ref:REF||undefined,repeat:rep(type)||undefined,ua:UA,tz:tz(),lang:(navigator.language||'').slice(0,16),screen:(screen.width||0)+'x'+(screen.height||0),bot:BOT?1:undefined,test:T?1:undefined}).catch(function(){})}catch(e){}}
window.p1WaTap=function(a){send(a,'whatsapp')};window.p1CtaTap=function(type,a){send(a||null,type)};window.p1Ref=REF;window.p1WithRef=withRef;
function kind(el){var c=el.getAttribute&&el.getAttribute('data-cta');if(c)return c;var u=String(el.href||el.getAttribute('href')||'');
if(WA.test(u))return'whatsapp';if(/^tel:/i.test(u))return'call';if(/^mailto:/i.test(u))return'email';if(BOOK.test(u)&&!/^#/.test(el.getAttribute('href')||''))return'booking';return''}
d.addEventListener('click',function(e){var t=e.target&&e.target.closest?e.target.closest('a[href],[data-cta]'):null;if(!t||t.tagName==='FORM')return;
if(REF&&t.getAttribute('href')&&WA.test(t.getAttribute('href'))){var y=withRef(t.getAttribute('href'));if(y!==t.getAttribute('href'))t.setAttribute('href',y)}
var k=kind(t);if(k&&k!=='form_submit')send(t,k)},true);
try{var wo=window.open;window.open=function(u){var g=[].slice.call(arguments);try{if(WA.test(String(u||''))){g[0]=withRef(String(u));waOpen=Date.now();var f=d.activeElement&&d.activeElement.closest?d.activeElement.closest('form'):null;send(f||d.activeElement,'whatsapp',f?'WhatsApp form':'')}}catch(x){}return wo.apply(window,g)}}catch(e){}
d.addEventListener('submit',function(e){var f=e.target;if(!f||!f.getAttribute||f.hasAttribute('data-p1-enquiry'))return;
if(f.getAttribute('data-wa')||/wa\.me|whatsapp/i.test(f.getAttribute('action')||''))return send(f,'whatsapp');
var c=f.getAttribute('data-cta');if(c)return send(f,c);if(f.getAttribute('role')==='search'||f.querySelector('input[type=search]'))return;
if(f.querySelector('input[type=email],input[type=tel],textarea,input[name*=phone i],input[name*=email i],input[name*=mobile i]'))setTimeout(function(){if(Date.now()-waOpen>1500)send(f,'form_submit')},60)},true);
/* enquiry form (CFG.form). Class names come from CFG so it wears the site's own form and button styles. */
var F=CFG.form;
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function proj(){try{return F.project?String(F.project()||'').slice(0,120):''}catch(e){return''}}
function waUrl(t){return withRef('https://wa.me/'+F.wa+'?text='+encodeURIComponent(t))}
function css(){if(d.getElementById('p1f-css'))return;var st=d.createElement('style');st.id='p1f-css';
st.textContent='.p1f-s{padding:64px 0}.p1f-in{display:grid;gap:28px;align-items:start}@media(min-width:900px){.p1f-in{grid-template-columns:1fr 1.1fr;gap:56px}}'+
'.p1f-copy p{max-width:34em}.p1f-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden}'+
'.p1f input{min-height:48px;font-size:17px}.p1f .p1f-row{display:flex;flex-direction:column;gap:12px;margin-top:6px}'+
'.p1f-note{font-size:13px;line-height:1.5;margin:14px 0 0;opacity:.85}.p1f-note a{text-decoration:underline}'+
'.p1f-err{color:#9b2c2c;font-size:14px;margin:10px 0 0}.p1f-ok{font-size:20px;line-height:1.4;margin:0 0 18px}'+
'.p1f .p1f-btn,.p1f-wa{display:flex;align-items:center;justify-content:center;width:100%;min-height:52px;text-align:center}'+(F.css||'');d.head.appendChild(st)}
function html(withH){var p=proj(),c=F.cls||{};
return '<form class="p1f '+esc(c.form||'')+'" data-p1-enquiry data-ref="enquiry-form" novalidate>'+(withH&&F.h?'<h2 class="'+esc(c.h||'')+'">'+esc(F.h)+'</h2>':'')+
'<label>'+esc(F.lName||'Name')+'<input name="name" required maxlength="80" autocomplete="name"></label>'+
'<label>'+esc(F.lMobile||'Mobile (8 digits)')+'<input name="mobile" type="tel" inputmode="numeric" required maxlength="13" autocomplete="tel-national" placeholder="9123 4567"></label>'+
'<label>'+esc(F.lProject||'Project or interest')+'<input name="project" maxlength="120" value="'+esc(p)+'" placeholder="'+esc(F.phProject||'')+'"></label>'+
'<div class="p1f-hp" aria-hidden="true"><label>Company<input name="company" tabindex="-1" autocomplete="off"></label></div>'+
'<p class="p1f-err" role="alert" hidden></p><div class="p1f-row"><button type="submit" class="p1f-btn '+esc(c.btn||'')+'">'+esc(F.send||'Send enquiry')+'</button>'+
'<a class="p1f-wa '+esc(c.wa||'')+'" href="'+esc(waUrl(F.waText(p)))+'" data-cta="whatsapp" data-ref="enquiry-form-wa" target="_blank" rel="noopener">'+esc(F.waBtn||'WhatsApp us now')+'</a></div>'+
'<p class="p1f-note">'+esc(F.consent)+(F.privacy?' <a href="'+esc(F.privacy)+'">'+esc(F.privacyText||'Privacy policy')+'</a>':'')+'</p></form>'}
function wire(f){var t0=Date.now(),err=f.querySelector('.p1f-err');
function bad(m,el){err.textContent=m;err.hidden=false;if(el)try{el.focus()}catch(x){}}
f.addEventListener('submit',function(e){e.preventDefault();var el=function(n){return f.elements.namedItem(n)},g=function(n){return String((el(n)||{}).value||'').replace(/\s+/g,' ').trim()};
var name=g('name'),mob=g('mobile').replace(/[\s-]/g,'').replace(/^\+?65/,''),pj=g('project');err.hidden=true;
if(name.length<2)return bad(F.eName||'Please enter your name.',el('name'));
if(!/^[89]\d{7}$/.test(mob))return bad(F.eMobile||'Please enter an 8-digit Singapore mobile number.',el('mobile'));
var done=function(){var ok=d.createElement('div');ok.className='p1f p1f-done '+((F.cls||{}).form||'');ok.setAttribute('role','status');
ok.innerHTML='<p class="p1f-ok">'+esc(F.thanks)+'</p><a class="p1f-wa '+esc((F.cls||{}).wa||'')+'" href="'+esc(waUrl(F.waAfter(name,pj)))+'" data-cta="whatsapp" data-ref="enquiry-thanks-wa" target="_blank" rel="noopener">'+esc(F.waNow||'Or WhatsApp us now')+'</a>';
f.parentNode.replaceChild(ok,f)};
var k='p1f_sent',prev=0;try{prev=+sessionStorage.getItem(k)||0}catch(x){}if(Date.now()-prev<60000)return done();
var btn=f.querySelector('button');btn.disabled=true;send(f,'form_submit','Enquiry form');
post({entity:'Enquiry',site:SITE,page_path:location.pathname.slice(0,200),ref_code:REF||pcode(),name:name,mobile:mob,project:pj,hp:g('company'),fill_ms:Date.now()-t0,
session_id:sid(),visitor_id:vid(),device_type:MOB,ua:UA,tz:tz(),lang:(navigator.language||'').slice(0,16),bot:BOT?1:undefined,test:T?1:undefined})
.then(function(r){if(r.status===204||r.ok){try{sessionStorage.setItem(k,String(Date.now()))}catch(x){}done()}else{btn.disabled=false;bad(F.eSend||'Sorry, that did not go through. Please WhatsApp us instead.')}})
.catch(function(){btn.disabled=false;bad(F.eSend||'Sorry, that did not go through. Please WhatsApp us instead.')})})}
function mount(){if(!F||!F.wa)return;css();var ph=d.querySelectorAll('[data-p1-form]'),i,m,t,box,p=location.pathname,did=0;
for(i=0;i<ph.length;i++){ph[i].innerHTML=html(1);wire(ph[i].querySelector('form'));did=1}if(did)return;
for(i=0;i<(F.mounts||[]).length;i++){m=F.mounts[i];if(m.path&&!new RegExp(m.path).test(p))continue;t=d.querySelector(m.sel||m.before);if(!t)continue;
if(m.sel){box=d.createElement('div');box.innerHTML=html(1);var nf=box.firstChild;t.parentNode.replaceChild(nf,t);wire(nf)}
else{var tt=typeof F.title==='function'?F.title(proj()):F.title;box=d.createElement('section');box.className='p1f-s '+((F.cls||{}).sec||'');box.id='enquire';box.setAttribute('aria-label',F.h||'Enquiry');
box.innerHTML='<div class="p1f-in '+esc((F.cls||{}).wrap||'')+'"><div class="p1f-copy">'+(tt?'<h2 class="'+esc((F.cls||{}).title||'')+'">'+esc(tt)+'</h2>':'')+(F.sub?'<p>'+esc(F.sub)+'</p>':'')+'</div>'+html(0)+'</div>';
t.parentNode.insertBefore(box,t);wire(box.querySelector('form'))}return}}
function ready(){tagLinks();mount()}
if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',ready);else ready()})();
