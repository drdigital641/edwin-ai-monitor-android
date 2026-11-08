(function(){
var d=document,h=d.documentElement,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
h.classList.add('js');
d.addEventListener('click',function(e){var b=e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  var art=d.querySelector('.prose');
  if(art){var bar=d.createElement('div');bar.className='progress';d.body.appendChild(bar);
    var on=function(){var r=art.getBoundingClientRect(),t=r.height-innerHeight;bar.style.transform='scaleX('+Math.min(1,Math.max(0,-r.top/(t>0?t:1)))+')'};
    addEventListener('scroll',on,{passive:true});on()}
  /* gentle reveal: only elements below the fold are hidden, so nothing on screen ever blanks */
  var els=[].slice.call(d.querySelectorAll('.sec-head,.mcard,.card,.acard,.faq details,.band,.steps li,.figs,.split figure,.visit>*'));
  if(!rm&&'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.06});
    els.forEach(function(e){if(e.getBoundingClientRect().top<innerHeight)return;e.classList.add('rv');var i=[].indexOf.call(e.parentNode.children,e);e.style.transitionDelay=Math.min(i,4)*70+'ms';io.observe(e)});
  }
});
})();
/* enquiry forms open WhatsApp with the details filled in */
(function(){[].forEach.call(document.querySelectorAll('form[data-wa]'),function(f){
f.addEventListener('submit',function(e){e.preventDefault();var lines=[f.getAttribute('data-intro')];
[].forEach.call(f.elements,function(x){if(x.name&&x.value&&x.value.trim())lines.push((x.getAttribute('data-label')||x.name)+': '+x.value.trim())});
window.open('https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(lines.join('\n')),'_blank','noopener')})})})();
/* continuous glide on photo carousels: loops seamlessly, pauses when held or swiped sideways */
(function(){var d=document;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){var rails=[];
[].forEach.call(d.querySelectorAll('.glide'),function(r){
  if(r.scrollWidth<=r.clientWidth+4)return;
  var kids=[].slice.call(r.children);
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');r.appendChild(c)});
  r.classList.add('auto');
  var o={r:r,pos:r.scrollLeft,hold:0,vis:false,half:0};
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  var hold=function(){o.hold=Date.now()+3000},sx=0,sy=0,touching=false,grab=false,tm=0;
  r.addEventListener('touchstart',function(e){var t=e.touches[0];sx=t.clientX;sy=t.clientY;touching=true;grab=false;
    clearTimeout(tm);tm=setTimeout(function(){if(touching){grab=true;o.hold=Infinity}},350)},{passive:true});
  r.addEventListener('touchmove',function(e){var t=e.touches[0],dx=Math.abs(t.clientX-sx),dy=Math.abs(t.clientY-sy);
    if(grab){if(dy>12&&dy>dx*1.5){grab=false;o.hold=0}return}
    if(dx>8&&dx>dy){grab=true;o.hold=Infinity;clearTimeout(tm)}else if(dy>8){clearTimeout(tm)}},{passive:true});
  var end=function(){touching=false;clearTimeout(tm);if(grab){grab=false;hold()}};
  r.addEventListener('touchend',end,{passive:true});r.addEventListener('touchcancel',end,{passive:true});
  r.addEventListener('mousedown',function(){o.hold=Infinity});addEventListener('mouseup',function(){if(o.hold===Infinity&&!touching)hold()});
  r.addEventListener('wheel',function(e){if(Math.abs(e.deltaX)>Math.abs(e.deltaY))hold()},{passive:true});
  if('IntersectionObserver' in window)new IntersectionObserver(function(es){o.vis=es[0].isIntersecting},{threshold:0}).observe(r);else o.vis=true;
  rails.push(o)});
if(!rails.length)return;
var last=0;
function tick(t){var dt=last?Math.max(0,Math.min(64,t-last)):16;last=t;
  rails.forEach(function(o){var r=o.r;
    if(!o.vis||d.hidden||Date.now()<o.hold){o.pos=r.scrollLeft;return}
    o.pos+=dt*0.035;
    if(o.half&&o.pos>=o.half)o.pos-=o.half;
    r.scrollLeft=o.pos});
  requestAnimationFrame(tick)}
requestAnimationFrame(tick)})})();
/* colour picker: swap the car photo when a swatch is tapped */
(function(){[].forEach.call(document.querySelectorAll('[data-cpick]'),function(c){
var imgs=c.querySelectorAll('.cp-img'),sws=c.querySelectorAll('.cp-sw'),nm=c.querySelector('.cp-name');
[].forEach.call(sws,function(b){b.addEventListener('click',function(){var i=b.getAttribute('data-i');
[].forEach.call(imgs,function(m){m.classList.toggle('on',m.getAttribute('data-i')===i)});
[].forEach.call(sws,function(s){var on=s===b;s.classList.toggle('on',on);s.setAttribute('aria-pressed',on)});
nm.textContent=b.querySelector('span').textContent})})})})();
/* WhatsApp tap counter -> Page One Controller (public write-only "track" fn). Site: dongfeng-jb. Added 22 Oct 2026. 23 Oct: cta_type whatsapp_sales / whatsapp_service (Controller counts any type containing 'whatsapp'). 8 Nov: whatsapp_dealership (Gavin, B2B page); forms with data-cta send that type (form_submit). */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,'');if(h==='pageonesingapore.com'||h==='localhost')return;window.__p1cta=1;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,last={};
var T=(function(){var q=/[?&]p1test=1(&|$)/.test(location.search);try{if(q)sessionStorage.setItem('p1test','1');return sessionStorage.getItem('p1test')==='1'}catch(e){return q}})();
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=Math.random().toString(36).slice(2)+Date.now().toString(36);sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function send(ty,a){ty=ty||'whatsapp';var n=Date.now();if(last[ty]&&n-last[ty]<1500)return;last[ty]=n;var lab=a?String(a.getAttribute('aria-label')||a.textContent||'').replace(/\s+/g,' ').trim().slice(0,60):'';try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'dongfeng-jb',cta_type:ty||'whatsapp',session_id:sid(),page_path:location.pathname.slice(0,200),device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:(document.referrer||'').slice(0,200),cta_label:lab,test:T?1:undefined})}).catch(function(){})}catch(e){}}
window.p1WaTap=function(ty){send(ty)};window.p1CtaTap=function(type,a){send(type,a||null)};
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(!a)return;var u=String(a.href||'');if(WA.test(u))send(/60182240828/.test(u)?'whatsapp_service':/60125512820/.test(u)?'whatsapp_dealership':'whatsapp_sales',a);else if(/^tel:/i.test(u))send('call',a);else if(/^mailto:/i.test(u))send('email',a)},true);
document.addEventListener('submit',function(e){var f=e.target;if(f&&f.getAttribute&&(f.getAttribute('data-wa')||/wa\.me|whatsapp/i.test(f.getAttribute('action')||'')))send(f.getAttribute('data-cta')||'whatsapp_sales')},true)})();
/* Latest from MyKar (Facebook posts, 8 Nov 2026): arrow buttons + refresh from /data/fb-posts.json (weekly swap needs no rebuild).
   Cards are server-rendered; captions quoting a price or loan stay hidden (same rule as build.py FB_HIDE). Nothing loads from facebook.com. */
(function(){var d=document,ul=d.getElementById('fbc-list');if(!ul)return;
var wrap=ul.parentNode,prev=wrap.querySelector('.fbc-prev'),next=wrap.querySelector('.fbc-next'),HIDE=/RM\s?\d|\bOTR\b|rebate|月供|\$\d/i,M=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function st(){var m=ul.scrollWidth-ul.clientWidth-2;prev.disabled=ul.scrollLeft<=2;next.disabled=ul.scrollLeft>=m}
function go(k){var it=ul.querySelector('.fbc-item');var w=it?it.getBoundingClientRect().width+16:ul.clientWidth;ul.scrollBy({left:k*Math.max(w,Math.floor(ul.clientWidth/w)*w),behavior:'smooth'})}
prev.addEventListener('click',function(){go(-1)});next.addEventListener('click',function(){go(1)});ul.addEventListener('scroll',st,{passive:true});addEventListener('resize',st);st();
function esc(s){return String(s).replace(/[&<>"']/g,function(c){return'&#'+c.charCodeAt(0)+';'})}
function dt(s){var p=s.split('-');return (+p[2])+' '+M[+p[1]-1]+' '+p[0]}
function load(){fetch(ul.getAttribute('data-src'),{cache:'no-cache'}).then(function(r){return r.ok?r.json():null}).then(function(j){
if(!j||!j.posts||!j.posts.length||j.updated===ul.getAttribute('data-updated'))return;
ul.innerHTML=j.posts.map(function(p){var t=dt(p.date),c=p.caption&&!HIDE.test(p.caption)?'<p class="fbc-cap">'+esc(p.caption)+'</p>':'';
return '<li class="fbc-item"><div class="fbc-img"><img src="'+esc(p.image)+'" alt="MyKar World Facebook post, '+t+'" width="'+(+p.width)+'" height="'+(+p.height)+'" loading="lazy" decoding="async"></div><div class="fbc-body"><time datetime="'+esc(p.date)+'">'+t+'</time>'+c+'<a href="'+esc(p.permalink)+'" target="_blank" rel="noopener">View on Facebook<span class="vh"> (post of '+t+')</span></a></div></li>'}).join('');
ul.setAttribute('data-updated',j.updated||'');ul.scrollLeft=0;st()}).catch(function(){})}
if('IntersectionObserver' in window){var io=new IntersectionObserver(function(e){if(e[0].isIntersecting){io.disconnect();load()}},{rootMargin:'300px'});io.observe(ul)}else load();
})();
