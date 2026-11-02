(function(){
var d=document,h=d.documentElement,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
h.classList.add('js');
d.addEventListener('click',function(e){var b=e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  h.classList.add('loaded');
  var hdr=d.querySelector('.hdr'),bar=d.createElement('div');bar.className='progress';d.body.appendChild(bar);
  var art=d.querySelector('.prose');
  function onScroll(){var y=window.scrollY;hdr&&hdr.classList.toggle('scrolled',y>10);
    if(art){var r=art.getBoundingClientRect(),t=r.height-innerHeight;bar.style.transform='scaleX('+Math.min(1,Math.max(0,-r.top/(t>0?t:1)))+')'}}
  addEventListener('scroll',onScroll,{passive:true});onScroll();
  // scroll reveal with stagger
  var sel='.mcard,.scard,.acard,.step,.loc,.spec,.plist li,.enquiry,.sec-head,.gallery figure,.faq details,.ticks li,.minis .mini,.prose>h2,.prose>p,.prose>figure,.prose>table,.card,.band,.facts .wrap>div,.mapbox,.split2>div>h2';
  var els=[].slice.call(d.querySelectorAll(sel));
  if(rm||!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('in')})}
  else{
    var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){var t=en.target;t.classList.add('in');io.unobserve(t);setTimeout(function(){t.style.transitionDelay=''},1300)}})},{rootMargin:'0px 0px -8% 0px',threshold:.08});
    els.forEach(function(e){e.classList.add('rv');var p=e.parentNode,i=[].indexOf.call(p.children,e);e.style.transitionDelay=Math.min(i,6)*70+'ms';io.observe(e)});
  }
  // hero slideshow between the two machines
  var bg=d.querySelector('.hero-bg');
  if(bg&&!rm){var first=bg.querySelector('img'),base=first.src.replace(/[^\/]+$/,''),names=(bg.getAttribute('data-slides')||'').split(',').filter(Boolean),imgs=[first];
    names.forEach(function(n){var im=new Image();im.src=base+n+'.webp';im.alt='';im.className='slide';im.decoding='async';bg.insertBefore(im,bg.firstChild.nextSibling);imgs.push(im)});
    first.classList.add('slide','on');var k=0;
    if(imgs.length>1)setInterval(function(){imgs[k].classList.remove('on');k=(k+1)%imgs.length;imgs[k].classList.add('on')},6000)}
  // ticker of pages under the facts strip (home)
  var facts=d.querySelector('.facts');
  if(facts){var links=[].slice.call(d.querySelectorAll('.mcards .mcard,.scards .scard')).map(function(a){var b=a.querySelector('h3,b');return '<a tabindex="-1" href="'+a.getAttribute('href')+'">'+(b?b.textContent:'')+'</a>'}).join('<span>•</span>');
    if(links){var t=d.createElement('div');t.className='ticker';t.setAttribute('aria-hidden','true');t.innerHTML='<div class="ticker-in">'+links+'<span>•</span>'+links+'<span>•</span></div>';facts.parentNode.insertBefore(t,facts.nextSibling)}}
  // count-up stats
  var band=d.querySelector('.stats');
  if(band){var run=function(){[].forEach.call(band.querySelectorAll('b[data-to]'),function(b,i){var to=+b.dataset.to,fr=+(b.dataset.from||0),t0=null,suf=b.dataset.suf||'',pre=b.dataset.pre||'';
      if(rm){b.textContent=pre+to.toLocaleString()+suf;return}
      function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/1600),e=1-Math.pow(1-p,3);b.textContent=pre+Math.round(fr+(to-fr)*e).toLocaleString()+suf;if(p<1)requestAnimationFrame(step)}
      setTimeout(function(){requestAnimationFrame(step)},i*150)})};
    if(rm||!('IntersectionObserver' in window))run();else{var io3=new IntersectionObserver(function(es){es.forEach(function(en){if(!en.isIntersecting)return;io3.disconnect();run()})},{threshold:.4});io3.observe(band)}}
});
})();
/* ---- wow layer ---- */
(function(){
var d=document;
if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
var fine=window.matchMedia&&matchMedia('(hover: hover) and (pointer: fine)').matches;
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
  var hero=d.querySelector('.hero');
  if(hero){var bg=hero.querySelector('.hero-bg'),inn=hero.querySelector('.hero-in');
    addEventListener('scroll',function(){var y=scrollY;if(y<900){if(innerWidth<900)bg.style.transform='translateY('+(y*.3)+'px)';inn.style.transform='translateY('+(y*.12)+'px)';inn.style.opacity=Math.max(0,1-y/650)}},{passive:true})}
  var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('wiped','drawn');io.unobserve(en.target)}})},{threshold:.2});
  [].forEach.call(d.querySelectorAll('.lead-fig,.gallery figure,.prose figure:not(.lead-fig)'),function(f){f.classList.add('wipe');io.observe(f)});
  [].forEach.call(d.querySelectorAll('.sec-head h2,.prose>h2,.split2 h2'),function(x){x.classList.add('uline');io.observe(x)});
  if(fine)[].forEach.call(d.querySelectorAll('.scard,.acard,.mini,.mcard'),function(c){
    var sh=d.createElement('i');sh.className='shine';c.appendChild(sh);
    c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width,y=(e.clientY-r.top)/r.height;
      c.style.transform='perspective(800px) rotateX('+((.5-y)*6)+'deg) rotateY('+((x-.5)*8)+'deg) translateY(-6px)';sh.style.background='radial-gradient(circle at '+x*100+'% '+y*100+'%,rgba(255,255,255,.3),transparent 55%)'});
    c.addEventListener('mouseleave',function(){c.style.transform='';sh.style.background=''})});
  if(fine)[].forEach.call(d.querySelectorAll('.sec-dark,.band'),function(s){s.classList.add('spot');s.addEventListener('mousemove',function(e){var r=s.getBoundingClientRect();s.style.setProperty('--mx',(e.clientX-r.left)+'px');s.style.setProperty('--my',(e.clientY-r.top)+'px')})});
  if(fine)[].forEach.call(d.querySelectorAll('.hero .btn,.band .btn'),function(b){b.addEventListener('mousemove',function(e){var r=b.getBoundingClientRect();b.style.transform='translate('+((e.clientX-r.left-r.width/2)*.18)+'px,'+((e.clientY-r.top-r.height/2)*.25)+'px)'});b.addEventListener('mouseleave',function(){b.style.transform=''})});
});
})();
/* ---- enquiry form -> WhatsApp message ---- */
(function(){var f=document.getElementById('enquiry');if(!f)return;
f.addEventListener('submit',function(e){e.preventDefault();var g=function(n){var x=f.elements[n];return x&&x.value?x.value.trim():''};
var lines=['Hi AIVS, I found your website and would like to ask about: '+g('o')];
if(g('m'))lines.push('Machine: '+g('m'));if(g('l'))lines.push('Location I have in mind: '+g('l'));
if(g('n'))lines.push('Name: '+g('n'));if(g('x'))lines.push('Notes: '+g('x'));
window.open('https://wa.me/'+f.action.split('/').pop()+'?text='+encodeURIComponent(lines.join('\n')),'_blank','noopener')});})();
/* ---- WhatsApp: ask the topic once, then open the right number ---- */
(function(){var d=document,SALES='6583354865',SUP='6588784061',box,last,pre='Hi AIVS, I found your website. I would like to ask about ';
function url(n,t){return 'https://wa.me/'+n+'?text='+encodeURIComponent(t)}
function build(){box=d.createElement('div');box.className='wa-pick';box.hidden=true;
box.innerHTML='<div class="wa-box" role="dialog" aria-modal="true" aria-labelledby="wa-pick-t"><button type="button" class="wa-x" aria-label="Close">&times;</button><p class="wa-h" id="wa-pick-t">What is your WhatsApp about?</p><a class="wa-opt" data-k="s" target="_blank" rel="noopener"><b>Buying a machine or partnership</b><span>Machine purchase, hosting a machine, business collaboration</span></a><a class="wa-opt" data-k="t" target="_blank" rel="noopener"><b>Technical support or refund</b><span>A machine problem, a customer refund, help with a machine you own</span></a></div>';
d.body.appendChild(box);
box.addEventListener('click',function(e){if(e.target===box||e.target.closest('.wa-x')||e.target.closest('.wa-opt'))close()});}
function close(){if(!box||box.hidden)return;box.hidden=true;d.documentElement.classList.remove('wa-open');if(last)try{last.focus()}catch(e){}}
function open(a){if(!box)build();last=a;var t='';try{t=new URL(a.href).searchParams.get('text')||''}catch(e){}
box.querySelector('[data-k=s]').href=url(SALES,t||pre+'owning a machine.');
box.querySelector('[data-k=t]').href=url(SUP,pre+'technical support or a refund.');
box.hidden=false;d.documentElement.classList.add('wa-open');box.querySelector('.wa-opt').focus()}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href^="https://wa.me/'+SALES+'"]');
if(!a||a.hasAttribute('data-direct')||a.closest('.wa-pick'))return;e.preventDefault();open(a)});
d.addEventListener('keydown',function(e){if(e.key==='Escape')close()});
/* enquiry form: support and refund topics go to the support line */
var f=d.getElementById('enquiry');if(f&&f.dataset.sup){var s=f.elements.o,fix=function(){f.action='https://wa.me/'+(/support|refund/i.test(s.value)?f.dataset.sup:SALES)};s&&s.addEventListener('change',fix);f.addEventListener('submit',fix,true)}
})();
/* WhatsApp tap counter -> Page One Controller (public write-only "track" fn). Site: aivs. Added 22 Oct 2026. */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,'');if(h==='pageonesingapore.com'||h==='localhost')return;window.__p1cta=1;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,last=0;
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=Math.random().toString(36).slice(2)+Date.now().toString(36);sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function send(){var n=Date.now();if(n-last<1500)return;last=n;try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'aivs',cta_type:'whatsapp',session_id:sid(),page_path:location.pathname.slice(0,200),device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:(document.referrer||'').slice(0,200)})}).catch(function(){})}catch(e){}}
window.p1WaTap=send;
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(a&&WA.test(String(a.href||'')))send()},true);
document.addEventListener('submit',function(e){var f=e.target;if(f&&f.getAttribute&&(f.getAttribute('data-wa')||/wa\.me|whatsapp/i.test(f.getAttribute('action')||'')))send()},true)})();

/* bottom bar: hide while typing in a form so it never covers fields or dropdowns (26 Oct 2026) */
(function(){var d=document,k=d.querySelector('.dock');if(!k)return;
d.addEventListener('focusin',function(e){if(e.target.matches&&e.target.matches('input,select,textarea'))k.classList.add('off')});
d.addEventListener('focusout',function(e){if(e.target.matches&&e.target.matches('input,select,textarea'))setTimeout(function(){var a=d.activeElement;if(!(a&&a.matches&&a.matches('input,select,textarea')))k.classList.remove('off')},150)})})();
