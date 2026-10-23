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
/* WhatsApp tap counter -> Page One Controller (public write-only "track" fn). Site: dongfeng-jb. Added 22 Oct 2026. 23 Oct: cta_type whatsapp_sales / whatsapp_service (Controller counts any type containing 'whatsapp'). */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,'');if(h==='pageonesingapore.com'||h==='localhost')return;window.__p1cta=1;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,last=0;
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=Math.random().toString(36).slice(2)+Date.now().toString(36);sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function send(ty){var n=Date.now();if(n-last<1500)return;last=n;try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'dongfeng-jb',cta_type:ty||'whatsapp',session_id:sid(),page_path:location.pathname.slice(0,200),device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:(document.referrer||'').slice(0,200)})}).catch(function(){})}catch(e){}}
window.p1WaTap=send;
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(a&&WA.test(String(a.href||'')))send(/60182240828/.test(a.href)?'whatsapp_service':'whatsapp_sales')},true);
document.addEventListener('submit',function(e){var f=e.target;if(f&&f.getAttribute&&(f.getAttribute('data-wa')||/wa\.me|whatsapp/i.test(f.getAttribute('action')||'')))send('whatsapp_sales')},true)})();
