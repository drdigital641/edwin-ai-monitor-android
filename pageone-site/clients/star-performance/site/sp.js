(function(){
var d=document,h=d.documentElement,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
h.classList.add('js');
d.addEventListener('click',function(e){var b=e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  // reading progress on guides and service pages
  var art=d.querySelector('.prose');
  if(art){var bar=d.createElement('div');bar.className='progress';d.body.appendChild(bar);
    var on=function(){var r=art.getBoundingClientRect(),t=r.height-innerHeight;bar.style.transform='scaleX('+Math.min(1,Math.max(0,-r.top/(t>0?t:1)))+')'};
    addEventListener('scroll',on,{passive:true});on()}
  // gentle reveal on scroll
  var els=[].slice.call(d.querySelectorAll('.sec-head,.rail-head,.svc,.scard,.acard,.story,.revgrid .rev,.car,.stock,.faq details,.band,.prose>h2,.vals div,.numbered li'));
  if(!rm&&'IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.06});
    els.forEach(function(e){e.classList.add('rv');var i=[].indexOf.call(e.parentNode.children,e);e.style.transitionDelay=Math.min(i,5)*60+'ms';io.observe(e)});
  }
  // swipe rails: arrow buttons scroll one screen of cards
  [].forEach.call(d.querySelectorAll('.rail-head'),function(head){
    var rail=head.parentNode.querySelector('.rail');if(!rail)return;
    var btns=head.querySelectorAll('.rail-btn');
    function upd(){btns[0].disabled=rail.scrollLeft<8;btns[1].disabled=rail.scrollLeft+rail.clientWidth>=rail.scrollWidth-8}
    [].forEach.call(btns,function(b){b.addEventListener('click',function(){rail.scrollBy({left:(+b.dataset.dir)*rail.clientWidth*.85,behavior:rm?'auto':'smooth'})})});
    rail.addEventListener('scroll',upd,{passive:true});addEventListener('resize',upd);upd();
  });
});
})();
/* ---- enquiry form -> WhatsApp message ---- */
(function(){var f=document.getElementById('enquiry');if(!f)return;
f.addEventListener('submit',function(e){e.preventDefault();var g=function(n){var x=f.elements[n];return x&&x.value?x.value.trim():''};
var lines=['Hi Star Performance Motor, I found your website. I would like to: '+g('o')];
if(g('c'))lines.push('Car: '+g('c'));if(g('n'))lines.push('Name: '+g('n'));if(g('x'))lines.push('Notes: '+g('x'));
window.open('https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(lines.join('\n')),'_blank','noopener')});})();
/* ---- continuous glide on every carousel: loops seamlessly, pauses only when held or swiped sideways ---- */
(function(){var d=document;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){var rails=[];
[].forEach.call(d.querySelectorAll('.rail,.svc-grid,.glide,.revs'),function(r){
  if(r.scrollWidth<=r.clientWidth+4)return;
  var kids=[].slice.call(r.children);
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');c.setAttribute('tabindex','-1');c.removeAttribute('id');
    [].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});if(c.tagName==='A')c.setAttribute('tabindex','-1');r.appendChild(c)});
  r.classList.add('auto');
  var o={r:r,pos:r.scrollLeft,hold:0,hover:false,vis:false,half:0};
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  /* pause only on a deliberate hold or a sideways swipe; scrolling the page up/down past it keeps it moving */
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
  r.addEventListener('focusin',hold);
  var head=r.parentNode.querySelector('.rail-head');if(head)head.addEventListener('click',hold);
  if('IntersectionObserver' in window)new IntersectionObserver(function(es){o.vis=es[0].isIntersecting},{threshold:0}).observe(r);else o.vis=true;
  rails.push(o)});
if(!rails.length)return;
var last=0;
function tick(t){var dt=last?Math.min(64,t-last):16;last=t;
  rails.forEach(function(o){var r=o.r;
    if(!o.vis||d.hidden||Date.now()<o.hold){o.pos=r.scrollLeft;return}
    o.pos+=dt*0.035;            /* about 35px per second */
    if(o.half&&o.pos>=o.half)o.pos-=o.half;
    r.scrollLeft=o.pos});
  requestAnimationFrame(tick)}
requestAnimationFrame(tick)})})();
