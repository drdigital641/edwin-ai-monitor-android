(function(){
var d=document,els=d.querySelectorAll('.rv');
if('IntersectionObserver' in window&&els.length){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});els.forEach(function(el){io.observe(el)})}
else{els.forEach(function(el){el.classList.add('in')})}
var form=d.getElementById('finder');
var RM=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
/* Home page: only the first workshops are in the HTML; the rest wait in <template id="more-cards"> and are added on Show more, on any search or filter, or when the browser is idle. */
var cards;function more(){var t=d.getElementById('more-cards');if(!t)return;var g=d.getElementById('results'),w=d.getElementById('more-btn-wrap');g.appendChild(t.content);t.parentNode.removeChild(t);if(w)w.parentNode.removeChild(w);cards=d.querySelectorAll('#results [data-search]');if(window.sgcwRefresh)window.sgcwRefresh()}
window.sgcwMore=more;var mb=d.getElementById('more-btn');if(mb)mb.addEventListener('click',more);
if(d.getElementById('more-cards')){(window.requestIdleCallback||function(f){setTimeout(f,2500)})(function(){setTimeout(more,1500)})}
if(form){cards=d.querySelectorAll('#results [data-search]');var em=d.getElementById('empty'),q=d.getElementById('q'),ct=d.getElementById('count');
var STOP=' in at near for the a an my and of to with need needs want looking car cars workshop workshops shop singapore sg around area please ',RG={north:'north',east:'east',west:'west',central:'central',ne:'north-east',mobile:'mobile'};
function parse(v){v=' '+v.toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ')+' ';v=v.replace(/ north ?east /g,' ne ').replace(/ ne /g,' ne ');var t=v.trim().split(' '),w=[],r=[];
t.forEach(function(x){if(!x||STOP.indexOf(' '+x+' ')>-1)return;if(RG[x])r.push(RG[x]);else w.push(x)});return{w:w,r:r}}
function hit(s,x){return s.indexOf(' '+x)>-1||(x.length>3&&x.slice(-1)==='s'&&s.indexOf(' '+x.slice(0,-1))>-1)}
var feat=d.querySelector('section.feat'),wk=d.getElementById('workshops'),moved=false;
/* While a search or filter is active, the Premium carousel sits below the results; clearing the search puts it back above the list. */
function place(on){if(!feat||!wk||on===moved)return;moved=on;if(on)wk.parentNode.insertBefore(feat,wk.nextSibling);else wk.parentNode.insertBefore(feat,wk)}
function f(){more();var sv=form.querySelector('input[name=svc]:checked'),svc=sv?sv.value:'',rg=[].map.call(form.querySelectorAll('input[name=reg]:checked'),function(i){return i.value}),p={w:[],r:[]},n=0;
cards.forEach(function(c){var r=' '+c.getAttribute('data-regions')+' ',s=' '+c.getAttribute('data-search')+' ',
ok=(!svc||c.getAttribute('data-cat')===svc)&&(!rg.length||rg.some(function(x){return r.indexOf(' '+x+' ')>-1}))&&p.r.every(function(x){return r.indexOf(' '+x+' ')>-1})&&p.w.every(function(x){return hit(s,x)});c.hidden=!ok;if(ok)n++});
if(ct)ct.innerHTML='<b>'+n+'</b> workshop'+(n==1?'':'s');if(em)em.classList.toggle('show',!n);place(!!(svc||rg.length))}
form.addEventListener('change',f);form.addEventListener('submit',function(e){e.preventDefault();f()});
f();
/* Hint: bouncing finger + typed example placeholder. Both stop for good once the box is focused; static under reduced motion. */
var EX=['gearbox repair Woodlands','aircon servicing north','spray paint Yishun','battery replacement north','ECU repair Kaki Bukit'],base=q.getAttribute('placeholder'),done=true,tmr;
function stop(){done=true;clearTimeout(tmr);form.classList.add('hint-off');q.placeholder=base}
q.addEventListener('focus',stop);q.addEventListener('pointerdown',stop);
if(RM){form.classList.add('hint-off');q.placeholder=base}
else{var i=0,k=0,dir=1;(function tick(){if(done)return;if(q.value){q.placeholder=base;tmr=setTimeout(tick,1200);return}
var w=EX[i],dl=70;k+=dir;q.placeholder='e.g. '+w.slice(0,k);if(k>=w.length){dir=-1;dl=1600}else if(k<=0){dir=1;i=(i+1)%EX.length;dl=300}else if(dir<0)dl=30;tmr=setTimeout(tick,dl)})()}}
/* Featured carousel: seamless infinite marquee (rAF translateX). Never pauses on hover, scroll or visibility; stops while pressed or dragged and for 2s after you let go.
   Reduced motion: static swipeable scroll-snap row with arrow buttons. */
var tr=d.getElementById('track'),mq=d.getElementById('marq');
if(tr&&mq){
if(RM){function step(dir){var li=tr.querySelector('li');if(!li)return;var w=li.getBoundingClientRect().width+12,max=tr.scrollWidth-tr.clientWidth;
if(dir>0&&tr.scrollLeft>=max-6)tr.scrollTo({left:0});else if(dir<0&&tr.scrollLeft<=6)tr.scrollTo({left:max});else tr.scrollBy({left:dir*w})}
var pv=d.getElementById('cprev'),nx=d.getElementById('cnext');if(pv)pv.addEventListener('click',function(){step(-1)});if(nx)nx.addEventListener('click',function(){step(1)});
tr.tabIndex=0;tr.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){step(1);e.preventDefault()}else if(e.key==='ArrowLeft'){step(-1);e.preventDefault()}})}
else{var kids=[].slice.call(tr.children),n=kids.length;
if(n){var off=0,tt=false,until=0,held=false,drag=false,sx=0,so=0,pid=null,moved=false,last=0,SP=38,sw=0;
mq.classList.add('on');
function addSet(){kids.forEach(function(li){var c=li.cloneNode(true);c.setAttribute('aria-hidden','true');[].forEach.call(c.querySelectorAll('a,button'),function(x){x.tabIndex=-1});tr.appendChild(c)})}
addSet();var one=tr.children[n].offsetLeft-tr.children[0].offsetLeft;sw=one;
while(one>0&&tr.children.length/n*one<mq.clientWidth+2*one){addSet()}
function draw(){tr.style.transform='translate3d('+(-off).toFixed(2)+'px,0,0)'}
function wrap(){if(sw>0){off=((off%sw)+sw)%sw}}
function loop(t){var dt=last?Math.min(t-last,100):0;last=t;if(!held&&!drag&&!tt&&t>until){off+=SP*dt/1000;wrap();draw()}requestAnimationFrame(loop)}
requestAnimationFrame(loop);
window.addEventListener('resize',function(){var o=tr.children[n].offsetLeft-tr.children[0].offsetLeft;if(o>0)sw=o;wrap();draw()});
function release(){held=false;until=performance.now()+2000;if(drag){drag=false;mq.classList.remove('drag');setTimeout(function(){moved=false},0)}if(pid!==null){try{mq.releasePointerCapture(pid)}catch(x){}pid=null}}
mq.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'&&e.button!==0)return;held=true;drag=false;moved=false;sx=e.clientX;so=off;pid=e.pointerId});
mq.addEventListener('pointermove',function(e){if(!held)return;var dx=e.clientX-sx;
if(!drag&&Math.abs(dx)>6){drag=true;moved=true;mq.classList.add('drag');try{mq.setPointerCapture(e.pointerId)}catch(x){}}
if(drag){off=so-dx;wrap();draw()}});
['pointerup','pointercancel','lostpointercapture'].forEach(function(ev){mq.addEventListener(ev,release)});
mq.addEventListener('touchstart',function(){tt=true},{passive:true});
['touchend','touchcancel'].forEach(function(ev){mq.addEventListener(ev,function(){tt=false;until=performance.now()+2000},{passive:true})});
/* a drag must not count as a tap on a button or link */
mq.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation()}},true);
mq.addEventListener('dragstart',function(e){e.preventDefault()});
}}}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-cta]');if(!a)return;var c=a.getAttribute('data-cta');try{if(window.dataLayer)window.dataLayer.push({event:'cta_click',cta:c})}catch(x){}track(a,c)});
/* Lead counter: Page One Controller public write-only "track" function (same endpoint and payload as pageonesingapore.com main.js).
   Live domain taps are real; preview (pageonesingapore.com) taps are stored as site sgcarworkshop-test. WhatsApp, call, Google Maps, Directions and opening-hours taps on business listings only. */
var LIVE_HOST='sgcarworkshop.sg',APP='6ac7f2548a9c3877449e2772';
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function keep(st,k){try{var v=st.getItem(k);if(!v){v=rid();st.setItem(k,v)}return v}catch(x){return rid()}}
function pagetype(p){return p==='/'?'home':/^\/workshops\//.test(p)?'profile':/^\/areas\//.test(p)?'area':/^\/services\//.test(p)?'service':/^\/regions\//.test(p)?'region':'other'}
function track(a,c){try{
var h=location.hostname.replace(/^www\./,''),site=h===LIVE_HOST?'sgcarworkshop':(h==='pageonesingapore.com'?'sgcarworkshop-test':'');
if(!site)return;   /* live domain = real taps; the pageonesingapore.com preview = separate "test" taps; anything else is ignored */
if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.webdriver)return;
var tier=a.getAttribute('data-tier'),m=/^(whatsapp|call)_dir_(.+)$|^(maps|directions|hours|closed_flag)_(.+)$/.exec(c);if(!tier||!m)return;
var kind=m[1]||m[3],slug=m[2]||m[4],ua=navigator.userAgent;
/* Fields kept: which button (cta_type), which workshop (cta_label = slug), tier, page type and month (enquiry_ref), page, device. No referrer. A random per-visit id only (session_id). No visitor id, no IP, nothing about the person. */
var body=JSON.stringify({entity:'CtaClick',site:site,session_id:keep(sessionStorage,'sgcw-sid'),page_path:location.pathname,
referrer:'',device_type:/Mobi|Android|iPhone/i.test(ua)?'mobile':/iPad|Tablet/i.test(ua)?'tablet':'desktop',
cta_type:kind,cta_label:slug.slice(0,60),enquiry_ref:tier+'|'+pagetype(location.pathname)+'|'+new Date().toISOString().slice(0,7)});
var url='https://base44.app/api/apps/'+APP+'/functions/track',sent=false;
if(navigator.sendBeacon){try{sent=navigator.sendBeacon(url,new Blob([body],{type:'application/json'}))}catch(x){}}
if(!sent&&window.fetch){fetch(url,{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:body}).catch(function(){})}
}catch(x){}}
})();

/* Owner sections on the list page: ?w=<slug> names the listing in the WhatsApp message to Page One (claim and removal). */
(function(){var m=/[?&]w=([a-z0-9-]+)/.exec(location.search);if(!m)return;
[['claim-wa','claim-for',function(n,b){return "Hi Page One, I'm from "+n+", about my "+b.getAttribute('data-site')+" listing.\n\n(From "+location.href.split('#')[0]+")"},'claim_'],
 ['remove-wa','remove-for',function(n,b){return "Hi Page One, please remove the "+n+" listing from "+b.getAttribute('data-site')+". I run this business.\n\n(From "+location.href.split('#')[0]+")"},'remove_']].forEach(function(c){
var b=document.getElementById(c[0]);if(!b)return;var n;try{n=JSON.parse(b.getAttribute('data-names'))[m[1]]}catch(e){}if(!n)return;
var f=document.getElementById(c[1]);if(f){f.querySelector('b').textContent=n;f.hidden=false}
b.href='https://wa.me/'+b.getAttribute('data-wa')+'?text='+encodeURIComponent(c[2](n,b));b.setAttribute('data-cta',c[3]+m[1]);
if(c[0]==='claim-wa'){var tp=document.getElementById('claim-taps'),t;try{t=JSON.parse(b.getAttribute('data-taps')||'{}')[m[1]]}catch(e){}if(tp&&t){tp.textContent=t+' drivers have WhatsApped this workshop via '+b.getAttribute('data-site');tp.hidden=false}}})})();

/* Estate pages: filter (Open Sunday / Open late) and sort (highest Google rating) using data-* computed at build time. */
(function(){var g=document.getElementById('estate-grid'),t=document.querySelector('.etools');if(!g||!t)return;
var cards=[].slice.call(g.querySelectorAll('.card[data-search]')),order=cards.slice(),on={sun:false,late:false},note=t.querySelector('.et-n');
function apply(){var any=on.sun||on.late,shown=0;cards.forEach(function(c){var ok=!((on.sun&&c.getAttribute('data-sun')!=='1')||(on.late&&c.getAttribute('data-late')!=='1'));c.hidden=!ok;if(ok)shown++});if(note){note.hidden=!any;var ec=note.querySelector('.et-c');if(ec)ec.textContent='Showing '+shown+' of '+cards.length+' workshops.'}}
var clr=t.querySelector('[data-clear]');if(clr)clr.addEventListener('click',function(){on.sun=on.late=false;[].forEach.call(t.querySelectorAll('[data-f]'),function(b){b.setAttribute('aria-pressed','false')});apply()});
[].forEach.call(t.querySelectorAll('[data-f]'),function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-f');on[k]=!on[k];b.setAttribute('aria-pressed',on[k]?'true':'false');apply()})});
var s=t.querySelector('[data-sort]');if(s)s.addEventListener('change',function(){var l=order.slice();if(s.value==='rating')l.sort(function(a,b){return (parseFloat(b.getAttribute('data-rating'))||0)-(parseFloat(a.getAttribute('data-rating'))||0)});
var cta=g.querySelector('.card.list');l.forEach(function(c){g.insertBefore(c,cta)})})})();
