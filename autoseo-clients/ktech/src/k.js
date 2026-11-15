(function(){var d=document,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
d.addEventListener('click',function(e){var b=e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
 /* scan tablet: systems tick OK one by one, then loop */
 var t=d.querySelector('.tab');if(t){var li=[].slice.call(t.querySelectorAll('.sys li')),bar=t.querySelector('.bar b'),st=t.querySelector('.st'),i=0,rpm=t.querySelector('.rpm b');
  var run=function(){if(d.hidden)return;if(i<li.length){li[i].classList.add('on');i++;bar.style.width=(i/li.length*100)+'%';if(i===li.length)st.textContent=st.getAttribute('data-done')}
   else{li.forEach(function(x){x.classList.remove('on')});i=0;bar.style.width='0';st.textContent=st.getAttribute('data-run')}};
  if(rm){li.forEach(function(x){x.classList.add('on')});bar.style.width='100%';st.textContent=st.getAttribute('data-done')}else{setInterval(run,850)}
  if(rpm&&!rm)setInterval(function(){rpm.textContent=String(780+Math.round(Math.random()*60))},700)}
 /* reveal */
 var els=[].slice.call(d.querySelectorAll('.real figure,.sh,.proof>*,.steps li,.seo,.faq details,.svc article,.flist .fam,.cbox'));
 if(!rm&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.06});
  els.forEach(function(e){e.classList.add('rv');io.observe(e)})}
});
/* enquiry form -> WhatsApp */
ready(function(){var f=d.getElementById('enquiry');if(!f)return;f.addEventListener('submit',function(e){e.preventDefault();var g=function(n){var x=f.elements[n];return x&&x.value?x.value.trim():''};
 var L=JSON.parse(f.getAttribute('data-lines')),o=[L[0]];if(g('need'))o.push(L[1]+g('need'));if(g('name'))o.push(L[2]+g('name'));if(g('shop'))o.push(L[3]+g('shop'));
 window.open('https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(o.join('\n')),'_blank','noopener')})});
})();
/* continuous glide on carousels: loops, pauses only when held or swiped sideways; page scrolling never pauses it */
(function(){var d=document;if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){var rails=[];
[].forEach.call(d.querySelectorAll('.glide'),function(r){
  if(r.scrollWidth<=r.clientWidth+4)return;
  var kids=[].slice.call(r.children);
  kids.forEach(function(k){var c=k.cloneNode(true);c.setAttribute('aria-hidden','true');c.setAttribute('tabindex','-1');c.removeAttribute('id');
    [].forEach.call(c.querySelectorAll('a,button'),function(a){a.setAttribute('tabindex','-1')});r.appendChild(c)});
  r.classList.add('auto');
  var o={r:r,pos:r.scrollLeft,hold:0,vis:false,half:0,speed:+(r.getAttribute('data-speed')||0.04)};
  var measure=function(){o.half=r.children[kids.length].offsetLeft-r.children[0].offsetLeft};measure();addEventListener('resize',measure);
  var hold=function(){o.hold=Date.now()+1500},sx=0,sy=0,touching=false,grab=false,tm=0;
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
  if('IntersectionObserver' in window)new IntersectionObserver(function(es){o.vis=es[0].isIntersecting},{threshold:0}).observe(r);else o.vis=true;
  rails.push(o)});
if(!rails.length)return;
var last=0;
function tick(t){var dt=last?Math.min(64,t-last):16;last=t;
  rails.forEach(function(o){var r=o.r;
    if(!o.vis||d.hidden||Date.now()<o.hold){o.pos=r.scrollLeft;return}
    o.pos+=dt*o.speed;
    if(o.half&&o.pos>=o.half)o.pos-=o.half;
    r.scrollLeft=o.pos});
  requestAnimationFrame(tick)}
requestAnimationFrame(tick)})})();
