(function(){
var d=document,h=d.documentElement,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
h.classList.add('js');
d.addEventListener('click',function(e){var b=e.target.closest&&e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  /* reveal on scroll: decorates only, text is always in the HTML */
  var els=d.querySelectorAll('.rv');
  if(!('IntersectionObserver' in window)||rm){[].forEach.call(els,function(e){e.classList.add('in')})}
  else{var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    [].forEach.call(els,function(e){var r=e.getBoundingClientRect();if(r.top<innerHeight*1.2&&r.bottom>0){e.classList.add('in')}else io.observe(e)});
    /* safety net: nothing stays hidden for a reader that never scrolls */
    setTimeout(function(){[].forEach.call(els,function(e){e.classList.add('in')})},2500)}
  /* homepage promo: hides after its end date, a close lasts for the browser session only; it comes back in a new visit */
  var pr=d.getElementById('promo');
  if(pr){var key='kd_promo_'+pr.getAttribute('data-id'),ends=new Date(pr.getAttribute('data-ends')+'T23:59:59+08:00'),days=+pr.getAttribute('data-days')||7,seen=0;
    try{seen=+sessionStorage.getItem(key)||0}catch(e){}
    function close(){pr.hidden=true;d.body.style.overflow='';try{sessionStorage.setItem(key,String(Date.now()))}catch(e){}var v=pr.querySelector('video');if(v)v.pause()}
    if(Date.now()<=ends.getTime()&&Date.now()-seen>days*864e5){
      setTimeout(function(){pr.hidden=false;d.body.style.overflow='hidden';var v=pr.querySelector('video');if(v&&v.play){var k=v.play();if(k&&k.catch)k.catch(function(){})}var x=pr.querySelector('.promo-x');if(x)x.focus()},1400);
      pr.addEventListener('click',function(e){if(e.target.closest('[data-promo-close]'))close()});
      d.addEventListener('keydown',function(e){if(e.key==='Escape'&&!pr.hidden)close()});
      [].forEach.call(pr.querySelectorAll('a.btn-wa'),function(a){a.addEventListener('click',function(){try{sessionStorage.setItem(key,String(Date.now()))}catch(e){}})});
    }
  }
  /* lazy photos: some Safari versions never start a native lazy image (blank tiles). Load each one as it comes near,
     and load any that are still waiting shortly after the page has loaded. The src stays in the HTML for search engines. */
  var lz=[].slice.call(d.querySelectorAll('img[loading="lazy"]'));
  function go(i){if(i.getAttribute('loading')==='lazy'){i.setAttribute('loading','eager');if(!i.complete){var s=i.getAttribute('srcset');if(s)i.srcset=s;i.src=i.getAttribute('src')}}}
  if('IntersectionObserver' in window){var lo=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){go(x.target);lo.unobserve(x.target)}})},{rootMargin:'800px 800px'});lz.forEach(function(i){lo.observe(i)})}
  function late(){setTimeout(function(){lz.forEach(go)},1800)}
  if(d.readyState==='complete')late();else window.addEventListener('load',late);
  /* service galleries: arrow buttons move one photo; swipe works natively */
  [].forEach.call(d.querySelectorAll('[data-swipe]'),function(g){var nav=g.nextElementSibling;if(!nav||!nav.classList.contains('gal-nav'))return;
    nav.removeAttribute('aria-hidden');[].forEach.call(nav.querySelectorAll('.gal-b'),function(b){b.setAttribute('aria-label',b.getAttribute('data-dir')>0?'Next photo':'Previous photo');
      b.addEventListener('click',function(){var it=g.querySelector('.gal-i');var w=it?it.getBoundingClientRect().width+14:300;g.scrollBy({left:w*+b.getAttribute('data-dir'),behavior:rm?'auto':'smooth'})})})});
  /* rails glide slowly; pause on touch, hover or sideways swipe */
  [].forEach.call(d.querySelectorAll('[data-glide]'),function(r){
    var t=r.querySelector('.rail-track');if(!t||rm)return;
    if(t.scrollWidth<r.clientWidth*1.2)return;
    [].slice.call(t.children).forEach(function(c){var k=c.cloneNode(true);k.setAttribute('aria-hidden','true');k.classList.add('in');[].forEach.call(k.querySelectorAll('a'),function(a){a.tabIndex=-1});t.appendChild(k)});
    var speed=r.getAttribute('data-glide')==='slow'?0.018:0.03,hold=0,last=0,acc=0,tm;
    function half(){return t.scrollWidth/2}
    function step(ts){if(last&&!hold&&!d.hidden){acc+=(ts-last)*speed;if(acc>=1){r.scrollLeft+=Math.floor(acc);acc-=Math.floor(acc)}}if(r.scrollLeft>=half())r.scrollLeft-=half();last=ts;requestAnimationFrame(step)}
    requestAnimationFrame(step);
    function pause(ms){hold=1;clearTimeout(tm);tm=setTimeout(function(){hold=0},ms)}
    r.addEventListener('mouseenter',function(){hold=1});r.addEventListener('mouseleave',function(){hold=0});
    r.addEventListener('touchstart',function(){pause(4000)},{passive:true});r.addEventListener('touchmove',function(){pause(4000)},{passive:true});
    r.addEventListener('focusin',function(){hold=1});r.addEventListener('focusout',function(){hold=0});
  });
});
})();
