/* JBStaycation UI: header, menu, reveal on scroll, carousels, lightbox. Content is fully visible and usable without JS. */
(function(){
var d=document,b=d.body,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
var hdr=d.querySelector('.hdr'),tog=d.querySelector('.mtog');
function sc(){if(hdr)hdr.classList.toggle('scrolled',window.scrollY>24)}sc();window.addEventListener('scroll',sc,{passive:true});
function setMenu(o){hdr.classList.toggle('open',o);d.documentElement.classList.toggle('menu-open',o);tog.setAttribute('aria-expanded',o);tog.setAttribute('aria-label',o?'Close menu':'Open menu')}
if(tog){tog.addEventListener('click',function(){setMenu(!hdr.classList.contains('open'))});d.querySelectorAll('#mainnav a').forEach(function(a){a.addEventListener('click',function(){setMenu(false)})});window.addEventListener('resize',function(){if(window.innerWidth>=1024&&hdr.classList.contains('open'))setMenu(false)})}
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&hdr&&hdr.classList.contains('open'))setMenu(false)});
var els=[].slice.call(d.querySelectorAll('.rv'));
setTimeout(function(){els.forEach(function(x){x.classList.add('in')})},1500);
if('IntersectionObserver' in window&&!rm){var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){x.target.classList.add('in');io.unobserve(x.target)}})},{rootMargin:'0px 0px -6% 0px'});els.forEach(function(x){io.observe(x)})}else{els.forEach(function(x){x.classList.add('in')})}
/* carousels: auto-slide (keeps going while the page scrolls), pause only while held or dragged, restart 2 s after release */
d.querySelectorAll('[data-carousel]').forEach(function(c){
var t=c.querySelector('.track'),held=false,rt=null,drag=null,moved=false,cnt=c.querySelector('.cnt'),sl=t.querySelectorAll('.slide'),n=sl.length,chips=[].slice.call(c.querySelectorAll('.rchips button'));
function idx(){return Math.round(t.scrollLeft/Math.max(1,t.clientWidth))}
function upd(){var i=Math.min(idx(),n-1);if(cnt)cnt.textContent=(i+1)+' / '+n;dots.forEach(function(b,j){b.classList.toggle('on',j===i)});if(chips.length&&sl[i]){var r=sl[i].getAttribute('data-room');chips.forEach(function(b){var on=b.getAttribute('data-room')===r;b.classList.toggle('on',on);b.setAttribute('aria-pressed',on);if(on){var p=b.parentNode;p.scrollTo({left:b.offsetLeft-12,behavior:'auto'})}})}}
chips.forEach(function(b){b.addEventListener('click',function(){hold();var i=+b.getAttribute('data-i');t.scrollTo({left:i*t.clientWidth,behavior:rm?'auto':'smooth'});release()})});
function step(dir){var w=t.clientWidth,max=t.scrollWidth-w;if(max<=4)return;var x=t.scrollLeft+dir*w;if(x>max+4&&dir>0||t.scrollLeft>=max-4&&dir>0)x=0;else if(x<-4)x=max;t.scrollTo({left:x,behavior:rm?'auto':'smooth'})}
function hold(){held=true;clearTimeout(rt)}
function release(){clearTimeout(rt);rt=setTimeout(function(){held=false},2000)}
var dots=[],dw=c.querySelector('.dots');if(dw){for(var k=0;k<n;k++){var db=d.createElement('button');db.type='button';db.setAttribute('aria-label','Photo '+(k+1));(function(i){db.addEventListener('click',function(){hold();t.scrollTo({left:i*t.clientWidth,behavior:rm?'auto':'smooth'});release()})})(k);dw.appendChild(db);dots.push(db)}}
var nx=c.querySelector('.next'),pv=c.querySelector('.prev');
if(nx)nx.addEventListener('click',function(){hold();step(1);release()});
if(pv)pv.addEventListener('click',function(){hold();step(-1);release()});
t.addEventListener('scroll',function(){upd()},{passive:true});
t.addEventListener('touchstart',hold,{passive:true});t.addEventListener('touchend',release,{passive:true});t.addEventListener('touchcancel',release,{passive:true});
t.addEventListener('pointerdown',function(e){if(e.pointerType==='mouse'&&t.scrollWidth>t.clientWidth+4){hold();moved=false;drag={x:e.clientX,l:t.scrollLeft};t.classList.add('drag')}});
t.addEventListener('pointermove',function(e){if(drag){var dx=e.clientX-drag.x;if(Math.abs(dx)>5)moved=true;t.scrollLeft=drag.l-dx}});
function up(){if(drag){drag=null;t.classList.remove('drag');var w=t.clientWidth;t.scrollTo({left:Math.round(t.scrollLeft/w)*w,behavior:'smooth'});release()}}
t.addEventListener('pointerup',up);t.addEventListener('pointercancel',up);t.addEventListener('pointerleave',up);
t.addEventListener('click',function(e){if(moved){e.preventDefault();e.stopPropagation();moved=false}},true);
t.addEventListener('focusin',hold);t.addEventListener('focusout',release);
if(!rm)setInterval(function(){if(!held&&!d.hidden)step(1)},4200);
upd();
});
/* lightbox: every [data-lb] link on the page, in page order */
var items=[].slice.call(d.querySelectorAll('[data-lb]'));
if(items.length){
var lb=d.createElement('div');lb.className='lb';lb.setAttribute('role','dialog');lb.setAttribute('aria-modal','true');lb.setAttribute('aria-label','Photo viewer');lb.hidden=true;
lb.innerHTML='<div class="lb-top"><span class="lb-n"></span><button type="button" class="lb-x" aria-label="Close photo viewer"><svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg></button></div>'+
'<figure class="lb-fig"><div class="lb-st"><img class="lb-lo" alt="" aria-hidden="true"><img class="lb-hi" alt="" decoding="async"></div><figcaption></figcaption></figure>'+
'<button type="button" class="lb-p" aria-label="Previous photo"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m15 5-7 7 7 7"/></svg></button>'+
'<button type="button" class="lb-nx" aria-label="Next photo"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="m9 5 7 7-7 7"/></svg></button>';
b.appendChild(lb);
var im=lb.querySelector('.lb-hi'),lo=lb.querySelector('.lb-lo'),cap=lb.querySelector('figcaption'),num=lb.querySelector('.lb-n'),cur=0,last=null;
im.addEventListener('load',function(){im.classList.add('ok')});
function show(i){cur=(i+items.length)%items.length;var a=items[cur],g=a.querySelector('img'),h=a.getAttribute('href');im.classList.remove('ok');lo.src=(g&&(g.currentSrc||g.src))||h.replace('/img/','/thumb/');im.removeAttribute('src');im.src=h;if(im.complete&&im.naturalWidth)im.classList.add('ok');im.alt=g?g.alt:'';cap.textContent=a.getAttribute('data-cap')||(g?g.alt:'');num.textContent=(cur+1)+' / '+items.length;
var p=new Image();p.src=items[(cur+1)%items.length].getAttribute('href')}
function open(i){last=d.activeElement;lb.hidden=false;b.classList.add('lb-on');show(i);lb.querySelector('.lb-x').focus()}
function close(){lb.hidden=true;b.classList.remove('lb-on');im.removeAttribute('src');if(last)last.focus()}
var all=items;all.forEach(function(a){a.addEventListener('click',function(e){if(e.defaultPrevented)return;e.preventDefault();var st=a.closest('[data-lb-set]');items=st?[].slice.call(st.querySelectorAll('[data-lb]')):all;open(items.indexOf(a))})});
d.querySelectorAll('[data-lb-open]').forEach(function(x){x.addEventListener('click',function(e){e.preventDefault();items=all;open(0)})});
/* /stays: Prima | Landak switcher on phones (hash selects the house) */
var hsw=d.querySelector('.hsw');if(hsw){var H=d.documentElement;
function pick(k,scroll){H.setAttribute('data-house',k);hsw.querySelectorAll('a').forEach(function(a){var on=a.getAttribute('data-h')===k;a.classList.toggle('on',on);if(on)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current')});
if(scroll&&matchMedia('(max-width:767px)').matches){var y=hsw.getBoundingClientRect().top+window.scrollY-parseFloat(getComputedStyle(H).getPropertyValue('--hh')||64);var cur=hsw.getBoundingClientRect().top;if(window.scrollY>y)window.scrollTo(0,y)}}
pick(H.getAttribute('data-house')||'prima',false);
hsw.addEventListener('click',function(e){var a=e.target.closest('a');if(!a||!matchMedia('(max-width:767px)').matches)return;e.preventDefault();var k=a.getAttribute('data-h');history.replaceState(null,'','#'+k);pick(k,true)});
window.addEventListener('hashchange',function(){var k=location.hash==='#landak'?'landak':location.hash==='#prima'?'prima':null;if(k)pick(k,false)})}
lb.querySelector('.lb-x').addEventListener('click',close);lb.querySelector('.lb-p').addEventListener('click',function(){show(cur-1)});lb.querySelector('.lb-nx').addEventListener('click',function(){show(cur+1)});
lb.addEventListener('click',function(e){if(e.target===lb||e.target.classList.contains('lb-fig'))close()});
d.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();else if(e.key==='ArrowRight')show(cur+1);else if(e.key==='ArrowLeft')show(cur-1);else if(e.key==='Tab'){var f=[].slice.call(lb.querySelectorAll('button'));var k=f.indexOf(d.activeElement);e.preventDefault();f[(k+(e.shiftKey?-1:1)+f.length)%f.length].focus()}});
var sx=null;lb.addEventListener('touchstart',function(e){sx=e.touches[0].clientX},{passive:true});
lb.addEventListener('touchend',function(e){if(sx===null)return;var dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>40)show(cur+(dx<0?1:-1));sx=null},{passive:true});
}
})();
