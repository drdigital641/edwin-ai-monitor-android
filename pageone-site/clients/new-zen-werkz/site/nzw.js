(function(){
var d=document,h=d.documentElement,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
h.classList.add('js');
d.addEventListener('click',function(e){var b=e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  h.classList.add('loaded');
  // header shadow + reading progress
  var hdr=d.querySelector('.hdr'),bar=d.createElement('div');bar.className='progress';d.body.appendChild(bar);
  var art=d.querySelector('.prose');
  function onScroll(){var y=window.scrollY;hdr&&hdr.classList.toggle('scrolled',y>10);
    if(art){var r=art.getBoundingClientRect(),t=r.height-innerHeight;bar.style.transform='scaleX('+Math.min(1,Math.max(0,-r.top/(t>0?t:1)))+')'}}
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  // scroll reveal with stagger
  var sel='.sec-head,.scard,.acard,.review,.gallery figure,.faq details,.ticks li,.minis .mini,.prose>h2,.prose>p,.prose>figure,.card,.band,.facts .wrap>div,.mapbox,.split2>div>h2';
  var els=[].slice.call(d.querySelectorAll(sel));
  if(rm||!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')})}
  else{
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){var t=en.target;t.classList.add('in');io.unobserve(t);setTimeout(function(){t.style.transitionDelay=''},1300)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    els.forEach(function(e){e.classList.add('rv');var p=e.parentNode,i=[].indexOf.call(p.children,e);e.style.transitionDelay=Math.min(i,6)*70+'ms';io.observe(e)});
  }
  // hero slideshow (crossfade between workshop photos)
  var bg=d.querySelector('.hero-bg');
  if(bg&&!rm){var first=bg.querySelector('img'),base=first.src.replace(/[^\/]+$/,''),names=['engine-teardown.webp','mercedes-hummer.webp','workshop-lineup.webp'],imgs=[first];
    names.slice(0,2).forEach(function(n){var im=new Image();im.src=base+n;im.alt='';im.className='slide';im.decoding='async';bg.insertBefore(im,bg.firstChild.nextSibling);imgs.push(im)});
    first.classList.add('slide','on');var k=0;
    setInterval(function(){imgs[k].classList.remove('on');k=(k+1)%imgs.length;imgs[k].classList.add('on')},6000)}
  // services ticker under the facts strip (home)
  var facts=d.querySelector('.facts');
  if(facts){var links=[].slice.call(d.querySelectorAll('.scards .scard')).map(function(a){return '<a tabindex="-1" href="'+a.getAttribute('href')+'">'+a.querySelector('b').textContent+'</a>'}).join('<span>•</span>');
    if(links){var t=d.createElement('div');t.className='ticker';t.setAttribute('aria-hidden','true');t.innerHTML='<div class="ticker-in">'+links+'<span>•</span>'+links+'<span>•</span></div>';facts.parentNode.insertBefore(t,facts.nextSibling)}}
});
})();
/* ---- wow layer (v3) ---- */
(function(){
var d=document,h=d.documentElement;
if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var fine=window.matchMedia&&matchMedia('(hover: hover) and (pointer: fine)').matches;
// 1. intro splash, once per visit
var seen=false;try{seen=sessionStorage.getItem('nzw-intro')}catch(e){}
if(!seen&&d.querySelector('.hero')){
  try{sessionStorage.setItem('nzw-intro','1')}catch(e){}
  var s=d.createElement('div');s.className='splash';
  s.innerHTML='<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="9" fill="#1d2127"/><path class="z" d="M10 12h20L10 28h20" fill="none" stroke="#e1251b" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/></svg><div class="splash-t">'+'NEW ZEN WERKZ'.split('').map(function(c,i){return '<span style="animation-delay:'+(0.55+i*0.04)+'s">'+(c===' '?'&nbsp;':c)+'</span>'}).join('')+'</div><div class="splash-s">Car repair · Kaki Bukit</div>';
  h.classList.add('intro');d.body?d.body.appendChild(s):d.addEventListener('DOMContentLoaded',function(){d.body.appendChild(s)});
  setTimeout(function(){s.classList.add('out');h.classList.remove('intro')},1900);
  setTimeout(function(){s.remove()},2700);
}
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  // 2. hero light streak + parallax
  var hero=d.querySelector('.hero');
  if(hero){var st=d.createElement('div');st.className='streak';hero.appendChild(st);
    var bg=hero.querySelector('.hero-bg'),inn=hero.querySelector('.hero-in');
    addEventListener('scroll',function(){var y=scrollY;if(y<900){bg.style.transform='translateY('+(y*.35)+'px)';inn.style.transform='translateY('+(y*.12)+'px)';inn.style.opacity=Math.max(0,1-y/650)}},{passive:true})}
  // 3. photo wipe reveals
  var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('wiped');io.unobserve(en.target)}})},{threshold:.2});
  [].forEach.call(d.querySelectorAll('.lead-fig,.gallery figure,.prose figure:not(.lead-fig)'),function(f){f.classList.add('wipe');io.observe(f)});
  // 4. heading underline draw
  [].forEach.call(d.querySelectorAll('.sec-head h2,.prose>h2,.split2 h2'),function(x){x.classList.add('uline');io.observe(x)});
  var io2=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('drawn');io2.unobserve(en.target)}})},{threshold:.6});
  [].forEach.call(d.querySelectorAll('.uline'),function(x){io2.observe(x)});
  // 5. 3D tilt + shine on cards (mouse only)
  if(fine)[].forEach.call(d.querySelectorAll('.scard,.acard,.review,.mini'),function(c){
    var sh=d.createElement('i');sh.className='shine';c.appendChild(sh);
    c.addEventListener('mouseenter',function(){c.classList.add('tilt')});
    c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;
      c.style.transform='perspective(800px) rotateX('+((.5-y)*8)+'deg) rotateY('+((x-.5)*10)+'deg) translateY(-6px)';sh.style.background='radial-gradient(circle at '+x*100+'% '+y*100+'%,rgba(255,255,255,.35),transparent 55%)'});
    c.addEventListener('mouseleave',function(){c.style.transform='';sh.style.background=''})});
  // 6. stats band with count-up (home only, facts from records and Google)
  var svc=d.querySelector('section[aria-labelledby="h-svc"]');
  if(svc){var n=d.querySelectorAll('.scards .scard').length;
    var band=d.createElement('section');band.className='stats';band.setAttribute('aria-label','Workshop at a glance');
    band.innerHTML='<div class="wrap">'+[[2016,'At Eunos Technolink since','first as Zen Werkz LLP'],[n,'Workshop services','under one roof'],[13,'Years one customer has trusted Ah Mun','from a Google review'],[6,'Days a week','Mon to Sat']].map(function(s){return '<div class="stat"><b data-to="'+s[0]+'"'+(s[0]>1000?' data-from="1990"':'')+'>0</b><span>'+s[1]+'</span><small>'+s[2]+'</small></div>'}).join('')+'</div>';
    svc.parentNode.insertBefore(band,svc.nextSibling);
    var io3=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;io3.disconnect();
      [].forEach.call(band.querySelectorAll('b'),function(b,i){var to=+b.dataset.to,fr=+(b.dataset.from||0),t0=null;
        function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/1600),e=1-Math.pow(1-p,3);b.textContent=Math.round(fr+(to-fr)*e);if(p<1)requestAnimationFrame(step)}
        setTimeout(function(){requestAnimationFrame(step)},i*150)})})},{threshold:.4});io3.observe(band)}
  // 7. spotlight that follows the cursor on dark sections
  if(fine)[].forEach.call(d.querySelectorAll('.sec-dark,.band'),function(s){s.classList.add('spot');s.addEventListener('mousemove',function(e){var r=s.getBoundingClientRect();s.style.setProperty('--mx',(e.clientX-r.left)+'px');s.style.setProperty('--my',(e.clientY-r.top)+'px')})});
  // 8. magnetic main buttons
  if(fine)[].forEach.call(d.querySelectorAll('.hero .btn,.band .btn'),function(b){b.addEventListener('mousemove',function(e){var r=b.getBoundingClientRect();b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.18)+'px,'+((e.clientY-r.top-r.height/2)*.25)+'px)'});b.addEventListener('mouseleave',function(){b.style.transform=''})});
});
})();
