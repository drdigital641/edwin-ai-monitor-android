(function(){'use strict';
var d=document,RM=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

/* header: solid after scrolling, mobile menu */
var hd=d.getElementById('hd'),bg=d.getElementById('burger'),nav=d.getElementById('nav');
function onScroll(){if(hd)hd.classList.toggle('scrolled',window.scrollY>40)}
window.addEventListener('scroll',onScroll,{passive:true});onScroll();
if(bg&&nav){bg.addEventListener('click',function(){var o=!nav.classList.contains('open');nav.classList.toggle('open',o);d.body.classList.toggle('menu',o);bg.setAttribute('aria-expanded',o?'true':'false');d.body.style.overflow=o?'hidden':''});
nav.addEventListener('click',function(e){if(e.target.closest('a')){nav.classList.remove('open');d.body.classList.remove('menu');d.body.style.overflow='';bg.setAttribute('aria-expanded','false')}})}

/* reveal on scroll */
var rv=[].slice.call(d.querySelectorAll('.rv'));
if('IntersectionObserver' in window&&!RM){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.06});
rv.forEach(function(el){io.observe(el)})}else rv.forEach(function(el){el.classList.add('in')});

/* hero slideshow: slow crossfade with Ken Burns, progress lines */
var slides=[].slice.call(d.querySelectorAll('.slide')),dots=[].slice.call(d.querySelectorAll('.hdot')),cap=d.getElementById('cap'),cur=0,tm;
function show(i){if(!slides.length)return;cur=(i+slides.length)%slides.length;
slides.forEach(function(s,k){s.classList.toggle('on',k===cur)});
dots.forEach(function(b,k){b.classList.remove('on');if(k===cur){void b.offsetWidth;b.classList.add('on')}});
if(cap){cap.textContent=slides[cur].getAttribute('data-cap');cap.href=slides[cur].getAttribute('data-href')}
clearTimeout(tm);if(!RM)tm=setTimeout(function(){show(cur+1)},6500)}
if(slides.length){slides.forEach(function(s){var im=s.querySelector('img');if(im)im.loading='eager'});dots.forEach(function(b,k){b.addEventListener('click',function(){show(k)})});show(0)}
var ph=d.querySelector('.phero .kb');if(ph&&!RM)requestAnimationFrame(function(){requestAnimationFrame(function(){ph.classList.add('go')})});

/* reviews */
var qs=[].slice.call(d.querySelectorAll('.q')),qi=0,qt;
function q(i){qi=(i+qs.length)%qs.length;qs.forEach(function(x,k){x.classList.toggle('on',k===qi)});clearTimeout(qt);if(!RM)qt=setTimeout(function(){q(qi+1)},7000)}
if(qs.length){var qp=d.getElementById('qprev'),qn=d.getElementById('qnext');if(qp)qp.addEventListener('click',function(){q(qi-1)});if(qn)qn.addEventListener('click',function(){q(qi+1)});q(0)}

/* portfolio filter */
var chips=[].slice.call(d.querySelectorAll('.chip')),cards=[].slice.call(d.querySelectorAll('#pgrid .pc,#lgrid .lc'));
chips.forEach(function(c){c.addEventListener('click',function(){var f=c.getAttribute('data-f');
chips.forEach(function(x){var on=x===c;x.classList.toggle('on',on);x.setAttribute('aria-pressed',on?'true':'false')});
cards.forEach(function(k){k.hidden=!(f==='All'||k.getAttribute('data-kind')===f)})})});

/* lightbox */
var lb=d.getElementById('lb'),links=[].slice.call(d.querySelectorAll('[data-lb]')),li=0;
if(lb&&links.length){var lim=lb.querySelector('img');lim.referrerPolicy='no-referrer';
function open(i){li=(i+links.length)%links.length;lim.src=links[li].href;lim.alt=links[li].querySelector('img').alt;lb.hidden=false;d.body.style.overflow='hidden'}
function close(){lb.hidden=true;d.body.style.overflow=''}
links.forEach(function(a,i){a.addEventListener('click',function(e){e.preventDefault();open(i)})});
lb.querySelector('.lb-x').addEventListener('click',close);lb.querySelector('.lb-p').addEventListener('click',function(){open(li-1)});lb.querySelector('.lb-n').addEventListener('click',function(){open(li+1)});
lb.addEventListener('click',function(e){if(e.target===lb)close()});
d.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')open(li-1);if(e.key==='ArrowRight')open(li+1)});
var sx=0;lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});lb.addEventListener('touchend',function(e){var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50)open(li+(dx<0?1:-1))},{passive:true})}

/* contact form -> WhatsApp with details filled in */
var cf=d.getElementById('cform');
if(cf)cf.addEventListener('submit',function(e){e.preventDefault();var g=function(n){return (cf.elements[n].value||'').trim()};
var t='Hi Maison Interior Design, I would like a consultation.\nName: '+g('n')+'\nPhone: '+g('p')+'\nProperty: '+g('t')+(g('m')?'\nProject: '+g('m'):'');
window.open('https://wa.me/6593391185?text='+encodeURIComponent(t),'_blank','noopener')});

/* project reel: Wrapstar-style marquee. Slides on its own, keeps sliding while the page scrolls,
   pauses only while held or slid sideways, resumes 2s after release. Reduced motion: plain swipe row. */
var tr=d.getElementById('track'),mq=d.getElementById('marq');
if(tr&&mq&&!RM){var kids=[].slice.call(tr.children),n=kids.length;
if(n){var off=0,tt=false,until=0,held=false,drag=false,sx2=0,so=0,pid=null,moved=false,last=0,SP=34,sw=0;
mq.classList.add('on');
function addSet(){kids.forEach(function(x){var c=x.cloneNode(true);c.setAttribute('aria-hidden','true');[].forEach.call(c.querySelectorAll('a'),function(a){a.tabIndex=-1});tr.appendChild(c)})}
addSet();var one=tr.children[n].offsetLeft-tr.children[0].offsetLeft;sw=one;
while(one>0&&tr.children.length/n*one<mq.clientWidth+2*one){addSet()}
function draw(){tr.style.transform='translate3d('+(-off).toFixed(2)+'px,0,0)'}
function wrap(){if(sw>0){off=((off%sw)+sw)%sw}}
function loop(t){var dt=last?Math.min(t-last,100):0;last=t;if(!held&&!drag&&!tt&&t>until){off+=SP*dt/1000;wrap();draw()}requestAnimationFrame(loop)}
requestAnimationFrame(loop);
window.addEventListener('resize',function(){var o=tr.children[n].offsetLeft-tr.children[0].offsetLeft;if(o>0)sw=o;wrap();draw()});
function release(){held=false;if(drag)until=performance.now()+2000;if(drag){drag=false;mq.classList.remove('drag');setTimeout(function(){moved=false},0)}if(pid!==null){try{mq.releasePointerCapture(pid)}catch(x){}pid=null}}
mq.addEventListener('pointerdown',function(e){if(e.pointerType!=='mouse'||e.button!==0)return;held=true;drag=false;moved=false;sx2=e.clientX;so=off;pid=e.pointerId});
mq.addEventListener('pointermove',function(e){if(!held)return;var dx=e.clientX-sx2;
if(!drag&&Math.abs(dx)>6){drag=true;moved=true;mq.classList.add('drag');try{mq.setPointerCapture(e.pointerId)}catch(x){}}
if(drag){off=so-dx;wrap();draw()}});
['pointerup','pointercancel','lostpointercapture'].forEach(function(ev){mq.addEventListener(ev,release)});
mq.addEventListener('pointerup',function(){if(held&&!drag){held=false}});
var tx=0,ty=0,tso=0,mode='';
mq.addEventListener('touchstart',function(e){var t=e.touches[0];tx=t.clientX;ty=t.clientY;tso=off;mode='';tt=true;moved=false},{passive:true});
mq.addEventListener('touchmove',function(e){if(!tt)return;var t=e.touches[0],dx=t.clientX-tx,dy=t.clientY-ty;
if(!mode){if(Math.abs(dx)<6&&Math.abs(dy)<6)return;mode=Math.abs(dx)>=Math.abs(dy)?'h':'v';if(mode==='v'){tt=false;return}drag=true;moved=true;mq.classList.add('drag')}
if(mode==='h'){if(e.cancelable)e.preventDefault();off=tso-dx;wrap();draw()}},{passive:false});
['touchend','touchcancel'].forEach(function(ev){mq.addEventListener(ev,function(){if(mode==='h'){drag=false;mq.classList.remove('drag');setTimeout(function(){moved=false},0)}if(tt)until=performance.now()+2000;tt=false;mode=''},{passive:true})});
mq.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation()}},true);
mq.addEventListener('dragstart',function(e){e.preventDefault()});}}

/* video modal: full home tour with sound */
var vm=d.getElementById('vm');
if(vm){var vv=vm.querySelector('video');
function vclose(){vv.pause();vm.hidden=true;d.body.style.overflow=''}
[].slice.call(d.querySelectorAll('[data-video]')).forEach(function(b){b.addEventListener('click',function(){vv.poster=b.getAttribute('data-poster')||'';if(vv.getAttribute('src')!==b.getAttribute('data-video'))vv.src=b.getAttribute('data-video');vm.hidden=false;d.body.style.overflow='hidden';var p=vv.play();if(p&&p.catch)p.catch(function(){})})});
vm.querySelector('.vm-x').addEventListener('click',vclose);vm.addEventListener('click',function(e){if(e.target===vm)vclose()});
d.addEventListener('keydown',function(e){if(!vm.hidden&&e.key==='Escape')vclose()})}
/* teaser autoplay only when visible, never with reduced motion */
[].slice.call(d.querySelectorAll('.bk-vid video')).forEach(function(v){if(RM){v.removeAttribute('autoplay');v.pause();return}
if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){var p=v.play();if(p&&p.catch)p.catch(function(){})}else v.pause()})},{threshold:.2}).observe(v)}});
})();
