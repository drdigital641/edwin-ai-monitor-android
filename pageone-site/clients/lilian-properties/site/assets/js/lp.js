(function(){var d=document;
d.addEventListener('click',function(e){var b=e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
 var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
 /* district map */
 var m=d.querySelector('.mapcard');
 if(m){var info=JSON.parse(m.getAttribute('data-info')),cur='15',auto=!rm,timer;
  function sel(k,user){cur=k;[].forEach.call(m.querySelectorAll('.zone'),function(z){z.classList.toggle('on',z.getAttribute('data-d')===k)});
   [].forEach.call(m.querySelectorAll('.maptabs button'),function(b){b.setAttribute('aria-pressed',b.getAttribute('data-d')===k)});
   var i=info[k];m.querySelector('.mi-n').textContent=i.n;m.querySelector('.mi-s').textContent=i.s;var a=m.querySelector('.mi-a');a.href=i.u;a.textContent='Explore '+i.k+' →';
   if(user){auto=false;clearInterval(timer)}}
  m.addEventListener('click',function(e){var t=e.target.closest('[data-d]');if(t)sel(t.getAttribute('data-d'),true)});
  sel('14');if(auto){var ks=['14','15','16'],i=0;timer=setInterval(function(){if(d.hidden)return;i=(i+1)%3;sel(ks[i])},3200)}}
 /* reveal */
 var els=[].slice.call(d.querySelectorAll('.dtile,.dcard,.prow,.box,.tl li,.cred,details.q,.why li,.crow,.proof li'));
 if(!rm&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.05});
  els.forEach(function(e){e.classList.add('rv');io.observe(e)})}
});
/* enquiry form -> WhatsApp (PDPA box must be ticked) */
ready(function(){[].forEach.call(d.querySelectorAll('form.form[data-wa]'),function(f){f.addEventListener('submit',function(e){e.preventDefault();
 if(!f.checkValidity()){f.reportValidity();return}
 var g=function(n){var x=f.elements[n];return x&&x.value?x.value.trim():''};
 var L=['Hi Li Lian, I found your website.'];if(g('topic'))L.push('I am interested in: '+g('topic'));if(g('name'))L.push('Name: '+g('name'));if(g('msg'))L.push(g('msg'));
 window.open('https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(L.join('\n')),'_blank','noopener')})})});
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
/* Find your East Coast home: 3-tap picker. Routes by MRT line (facts.json) and stage of life; brief goes to WhatsApp. */
(function(){var d=document;function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){var f=d.getElementById('pickerform');if(!f)return;var P=JSON.parse(f.getAttribute('data-p')),wa=f.getAttribute('data-wa');
 var stageLab={first:'First home',family:'Growing family',upgrade:'Upgrading to landed',invest:'Investing',right:'Rightsizing'};
 var lineLab={EWL:'East-West Line',TEL:'Thomson-East Coast Line',DTL:'Downtown Line',CCL:'Circle Line',any:'no MRT preference'};
 var pref={first:['14','16','15'],invest:['14','15','16'],family:['15','16','14'],upgrade:['16','15','14'],right:['15','14','16']};
 var why={first:'city-fringe homes with three MRT lines',invest:'the Paya Lebar hub and three MRT lines',family:'parks, the coast and schools close by',upgrade:'landed estates and sea air',right:'heritage streets and East Coast Park on the doorstep'};
 function val(n){var x=f.querySelector('input[name='+n+']:checked');return x?x.value:''}
 f.addEventListener('change',function(){var b=val('b'),s=val('s'),m=val('m');if(!s||!m)return;
  var order=pref[s]||['15','16','14'],pick=null;
  for(var i=0;i<order.length;i++){var k=order[i];if(m==='any'||P[k].lines.indexOf(m)>-1){pick=k;break}}
  if(!pick)pick=order[0];var D=P[pick],r=f.querySelector('.presult');
  r.querySelector('.pr-n').textContent=D.n;r.querySelector('.pr-l').textContent=D.l;
  r.querySelector('.pr-w').textContent='Why here: '+(m==='any'?'':'it is on the '+lineLab[m]+', and ')+'it suits '+stageLab[s].toLowerCase()+' buyers looking for '+why[s]+'.';
  r.querySelector('.pr-u').href=D.u;r.querySelector('.pr-u').textContent='Explore District '+pick;
  var g=r.querySelector('.pr-g');g.href=D.g;g.textContent='Read: '+D.gt;
  var msg=['Hi Li Lian, I found your website.','Budget: '+(b||'not sure yet'),'Stage: '+stageLab[s],'MRT: '+lineLab[m],'The site suggested District '+pick+'. Can we talk?'].join('\n');
  r.querySelector('.pr-wa').href='https://wa.me/'+wa+'?text='+encodeURIComponent(msg);
  var first=r.hidden;r.hidden=false;if(first&&r.getBoundingClientRect().top>innerHeight*.8)r.scrollIntoView({behavior:'smooth',block:'nearest'})})})})();
/* v12 home hero: load the other scenes after the page loads, then start the crossfade; count-up on the proof figures */
(function(){var d=document,c=d.querySelector('.cv');if(!c)return;
var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
function start(){var imgs=[].slice.call(c.querySelectorAll('img[data-src]')),left=imgs.length;
 if(rm&&innerWidth<900)return;
 var go=function(){if(!rm)c.classList.add('go')};if(!left){go();return}
 imgs.forEach(function(i){var done=function(){if(--left===0)go()};i.addEventListener('load',done);i.addEventListener('error',done);i.src=i.getAttribute('data-src');i.removeAttribute('data-src')})}
if('IntersectionObserver' in window)new IntersectionObserver(function(es){d.body.classList.toggle('cv-on',es[0].isIntersecting)},{threshold:.35}).observe(c);
if(d.readyState==='complete')setTimeout(start,300);else addEventListener('load',function(){setTimeout(start,300)});
var ns=[].slice.call(d.querySelectorAll('.cv-n[data-n]'));if(rm||!ns.length||!('IntersectionObserver' in window))return;
var io=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;io.unobserve(en.target);
 var el=en.target,n=+el.getAttribute('data-n'),t0=0;function step(t){t0=t0||t;var k=Math.min(1,(t-t0)/1100);el.textContent=Math.round(n*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(step)}
 el.textContent='0';requestAnimationFrame(step)})},{threshold:.6});ns.forEach(function(n){io.observe(n)})})();
