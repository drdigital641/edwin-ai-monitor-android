(function(){
var d=document,els=d.querySelectorAll('.rv');
if('IntersectionObserver' in window&&els.length){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});els.forEach(function(el){io.observe(el)})}
else{els.forEach(function(el){el.classList.add('in')})}
var form=d.getElementById('finder');
var RM=!!(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches);
if(form){var cards=d.querySelectorAll('#results [data-search]'),em=d.getElementById('empty'),q=d.getElementById('q'),ct=d.getElementById('count');
var STOP=' in at near for the a an my and of to with need needs want looking car cars workshop workshops shop singapore sg around area please ',RG={north:'north',east:'east',west:'west',central:'central',ne:'north-east',mobile:'mobile'};
function parse(v){v=' '+v.toLowerCase().replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ')+' ';v=v.replace(/ north ?east /g,' ne ').replace(/ ne /g,' ne ');var t=v.trim().split(' '),w=[],r=[];
t.forEach(function(x){if(!x||STOP.indexOf(' '+x+' ')>-1)return;if(RG[x])r.push(RG[x]);else w.push(x)});return{w:w,r:r}}
function hit(s,x){return s.indexOf(' '+x)>-1||(x.length>3&&x.slice(-1)==='s'&&s.indexOf(' '+x.slice(0,-1))>-1)}
var feat=d.querySelector('section.feat'),wk=d.getElementById('workshops'),moved=false;
/* While a search or filter is active, the Premium carousel sits below the results; clearing the search puts it back above the list. */
function place(on){if(!feat||!wk||on===moved)return;moved=on;if(on)wk.parentNode.insertBefore(feat,wk.nextSibling);else wk.parentNode.insertBefore(feat,wk)}
function f(){var sv=form.querySelector('input[name=svc]:checked'),svc=sv?sv.value:'',rg=[].map.call(form.querySelectorAll('input[name=reg]:checked'),function(i){return i.value}),p=parse(q.value),n=0;
cards.forEach(function(c){var r=' '+c.getAttribute('data-regions')+' ',s=' '+c.getAttribute('data-search')+' ',
ok=(!svc||c.getAttribute('data-cat')===svc)&&(!rg.length||rg.some(function(x){return r.indexOf(' '+x+' ')>-1}))&&p.r.every(function(x){return r.indexOf(' '+x+' ')>-1})&&p.w.every(function(x){return hit(s,x)});c.hidden=!ok;if(ok)n++});
if(ct)ct.innerHTML='<b>'+n+'</b> workshop'+(n==1?'':'s');if(em)em.classList.toggle('show',!n);place(!!(q.value.trim()||svc||rg.length))}
form.addEventListener('change',f);q.addEventListener('input',f);form.addEventListener('submit',function(e){e.preventDefault();f()});
var rs=d.getElementById('reset');if(rs)rs.addEventListener('click',function(){HTMLFormElement.prototype.reset.call(form);q.value='';f()});f();
/* Hint: bouncing finger + typed example placeholder. Both stop for good once the box is focused; static under reduced motion. */
var EX=['gearbox repair Woodlands','aircon servicing north','spray paint Yishun','battery replacement north','ECU repair Kaki Bukit'],base='e.g. '+EX[0],done=RM,tmr;
function stop(){done=true;clearTimeout(tmr);form.classList.add('hint-off');q.placeholder=base}
q.addEventListener('focus',stop);q.addEventListener('pointerdown',stop);
if(RM){form.classList.add('hint-off');q.placeholder=base}
else{var i=0,k=0,dir=1;(function tick(){if(done)return;if(q.value){q.placeholder=base;tmr=setTimeout(tick,1200);return}
var w=EX[i],dl=70;k+=dir;q.placeholder='e.g. '+w.slice(0,k);if(k>=w.length){dir=-1;dl=1600}else if(k<=0){dir=1;i=(i+1)%EX.length;dl=300}else if(dir<0)dl=30;tmr=setTimeout(tick,dl)})()}}
/* Featured carousel: seamless infinite marquee (rAF translateX). Never pauses on hover, scroll or visibility; stops only while pressed or dragged.
   Reduced motion: static swipeable scroll-snap row with arrow buttons. */
var tr=d.getElementById('track'),mq=d.getElementById('marq');
if(tr&&mq){
if(RM){function step(dir){var li=tr.querySelector('li');if(!li)return;var w=li.getBoundingClientRect().width+12,max=tr.scrollWidth-tr.clientWidth;
if(dir>0&&tr.scrollLeft>=max-6)tr.scrollTo({left:0});else if(dir<0&&tr.scrollLeft<=6)tr.scrollTo({left:max});else tr.scrollBy({left:dir*w})}
var pv=d.getElementById('cprev'),nx=d.getElementById('cnext');if(pv)pv.addEventListener('click',function(){step(-1)});if(nx)nx.addEventListener('click',function(){step(1)});
tr.tabIndex=0;tr.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){step(1);e.preventDefault()}else if(e.key==='ArrowLeft'){step(-1);e.preventDefault()}})}
else{var kids=[].slice.call(tr.children),n=kids.length;
if(n){var off=0,held=false,drag=false,sx=0,so=0,pid=null,moved=false,last=0,SP=38,sw=0;
mq.classList.add('on');
function addSet(){kids.forEach(function(li){var c=li.cloneNode(true);c.setAttribute('aria-hidden','true');[].forEach.call(c.querySelectorAll('a,button'),function(x){x.tabIndex=-1});tr.appendChild(c)})}
addSet();var one=tr.children[n].offsetLeft-tr.children[0].offsetLeft;sw=one;
while(one>0&&tr.children.length/n*one<mq.clientWidth+2*one){addSet()}
function draw(){tr.style.transform='translate3d('+(-off).toFixed(2)+'px,0,0)'}
function wrap(){if(sw>0){off=((off%sw)+sw)%sw}}
function loop(t){var dt=last?Math.min(t-last,100):0;last=t;if(!held&&!drag){off+=SP*dt/1000;wrap();draw()}requestAnimationFrame(loop)}
requestAnimationFrame(loop);
window.addEventListener('resize',function(){var o=tr.children[n].offsetLeft-tr.children[0].offsetLeft;if(o>0)sw=o;wrap();draw()});
function release(){held=false;if(drag){drag=false;mq.classList.remove('drag');setTimeout(function(){moved=false},0)}if(pid!==null){try{mq.releasePointerCapture(pid)}catch(x){}pid=null}}
mq.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'&&e.button!==0)return;held=true;drag=false;moved=false;sx=e.clientX;so=off;pid=e.pointerId});
mq.addEventListener('pointermove',function(e){if(!held)return;var dx=e.clientX-sx;
if(!drag&&Math.abs(dx)>6){drag=true;moved=true;mq.classList.add('drag');try{mq.setPointerCapture(e.pointerId)}catch(x){}}
if(drag){off=so-dx;wrap();draw()}});
['pointerup','pointercancel','lostpointercapture'].forEach(function(ev){mq.addEventListener(ev,release)});
mq.addEventListener('touchstart',function(){held=true},{passive:true});
['touchend','touchcancel'].forEach(function(ev){mq.addEventListener(ev,function(){if(!drag)held=false},{passive:true})});
/* a drag must not count as a tap on a button or link */
mq.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation()}},true);
mq.addEventListener('dragstart',function(e){e.preventDefault()});
}}}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-cta]');if(!a)return;var c=a.getAttribute('data-cta');try{if(window.dataLayer)window.dataLayer.push({event:'cta_click',cta:c})}catch(x){}track(a,c)});
/* Lead counter: Page One Controller public write-only "track" function (same endpoint and payload as pageonesingapore.com main.js).
   Fires ONLY on the live directory domain, so preview clicks are not counted. WhatsApp and call taps on business listings only. */
var LIVE_HOST='sgcarworkshop.sg',APP='6ac7f2548a9c3877449e2772';
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function keep(st,k){try{var v=st.getItem(k);if(!v){v=rid();st.setItem(k,v)}return v}catch(x){return rid()}}
function track(a,c){try{
if(location.hostname!==LIVE_HOST&&location.hostname!=='www.'+LIVE_HOST)return;
if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.webdriver)return;
var tier=a.getAttribute('data-tier');if(!tier||!/^(whatsapp|call)_dir_/.test(c))return;
var slug=c.replace(/^(whatsapp|call)_dir_/,''),page=a.getAttribute('data-page')||location.pathname,ua=navigator.userAgent;
var body=JSON.stringify({entity:'CtaClick',site:'sgcarworkshop',session_id:keep(sessionStorage,'sgcw-sid'),visitor_id:keep(localStorage,'sgcw-vid'),page_path:location.pathname,
referrer:(document.referrer||'').slice(0,300),device_type:/Mobi|Android|iPhone/i.test(ua)?'mobile':/iPad|Tablet/i.test(ua)?'tablet':'desktop',
cta_type:c,enquiry_ref:slug+'|'+tier+'|'+page});
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
b.href='https://wa.me/'+b.getAttribute('data-wa')+'?text='+encodeURIComponent(c[2](n,b));b.setAttribute('data-cta',c[3]+m[1])})})();
