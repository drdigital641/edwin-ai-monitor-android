/* Urban Eco Solutions site script (built by build.py). Small, no libraries. */
(function(){
var d=document,root=d.documentElement;root.classList.add('js');
var reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;

/* menu sheet */
var sheet=d.getElementById('sheet'),openBtn=d.querySelector('.menu-btn');
function setMenu(o){if(!sheet)return;sheet.classList.toggle('open',o);openBtn&&openBtn.setAttribute('aria-expanded',o);d.body.style.overflow=o?'hidden':'';if(o){var f=sheet.querySelector('a,button');f&&f.focus();}else{openBtn&&openBtn.focus();}}
openBtn&&openBtn.addEventListener('click',function(){setMenu(true)});
sheet&&sheet.querySelector('.sheet__close').addEventListener('click',function(){setMenu(false)});
d.addEventListener('keydown',function(e){if(e.key==='Escape'&&sheet&&sheet.classList.contains('open'))setMenu(false)});

/* hero week counter, synced to the 7s CSS grow loop */
var wk=d.querySelector('[data-week]');
if(wk&&!reduce){var t0=performance.now();setInterval(function(){var p=((performance.now()-t0)%7000)/7000;var w=p<.62?Math.round(p/.62*5):5;wk.textContent=w>=5?'Week 5 · harvest':'Week '+w;},250);}

/* reveal on scroll */
var rv=d.querySelectorAll('.rv');
if('IntersectionObserver' in window&&!reduce){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{rootMargin:'0px 0px -8% 0px'});rv.forEach(function(el){io.observe(el)});}else{rv.forEach(function(el){el.classList.add('in')});}

/* crop picker: filter + sort server-rendered cards */
var picker=d.querySelector('[data-picker]');
if(picker){var list=picker.querySelector('.crops'),cards=[].slice.call(list.children),btns=picker.querySelectorAll('[data-filter]'),sel=picker.querySelector('select'),cnt=picker.querySelector('[data-count]'),cur='all';
 function apply(){var n=0;cards.forEach(function(c){var ok=cur==='all'||c.dataset.group===cur||('w'+c.dataset.weeks)===cur;c.hidden=!ok;if(ok)n++;});cnt&&(cnt.textContent=n+' of '+cards.length+' trialled crops');}
 btns.forEach(function(b){b.addEventListener('click',function(){cur=b.dataset.filter;btns.forEach(function(x){x.setAttribute('aria-pressed',x===b)});apply();})});
 sel&&sel.addEventListener('change',function(){var k=sel.value;cards.sort(function(a,b){if(k==='kg')return b.dataset.kg-a.dataset.kg;if(k==='weeks')return a.dataset.weeks-b.dataset.weeks||b.dataset.kg-a.dataset.kg;return a.dataset.i-b.dataset.i;});cards.forEach(function(c){list.appendChild(c)});});
 apply();}

/* value calculator */
var calc=d.querySelector('[data-calc]');
if(calc){var data=JSON.parse(d.getElementById('calc-data').textContent),crop=data.crops[0].id;
 var cbtn=calc.querySelectorAll('[data-crop]'),cyc=calc.querySelector('#cycles'),cycOut=calc.querySelector('#cycles-out'),lab=calc.querySelector('#labour');
 function $(id){return calc.querySelector('[data-out="'+id+'"]')}
 function m(v){return (v<0?'−':'')+'S$'+Math.abs(Math.round(v)).toLocaleString('en-SG')}
 function rng(a,b){return Math.round(a)===Math.round(b)?m(a):m(a)+' – '+m(b).replace('S$','S$')}
 function run(){var c=data.crops.filter(function(x){return x.id===crop})[0],n=+cyc.value;cycOut.value=n;
  var kg=c.kg*n,lo=kg*c.pf_low,hi=kg*c.pf_high,cost=c.cost*n,labour=lab.checked?data.labour*n:0;
  $('kg').textContent=(Math.round(kg*100)/100).toLocaleString('en-SG')+' kg';
  $('weeks').textContent=c.weeks+' weeks per cycle';
  $('pf').textContent=rng(lo,hi);
  $('reg').textContent=c.reg?m(kg*c.reg):'no regular price checked';
  $('cost').textContent=m(cost);
  $('labrow').hidden=!lab.checked;$('lab').textContent=m(labour);
  $('net').textContent=rng(lo-cost-labour,hi-cost-labour);}
 cbtn.forEach(function(b){b.addEventListener('click',function(){crop=b.dataset.crop;cbtn.forEach(function(x){x.setAttribute('aria-pressed',x===b)});run();})});
 cyc.addEventListener('input',run);lab.addEventListener('change',run);run();}

/* muted looping clips: play when in view, poster only if reduced motion */
var clips=d.querySelectorAll('video[data-autoplay]');
if(clips.length){
  clips.forEach(function(v){v.muted=true;v.defaultMuted=true;v.setAttribute('muted','');v.playsInline=true;});
  if(!reduce && 'IntersectionObserver' in window){
    var vio=new IntersectionObserver(function(es){
      es.forEach(function(en){
        var v=en.target;
        if(en.isIntersecting){v.muted=true;var p=v.play();if(p&&p.catch)p.catch(function(){});}
        else {v.pause();}
      });
    },{rootMargin:'80px 0px',threshold:0.2});
    clips.forEach(function(v){vio.observe(v);});
  }
}

/* lightweight diagram zoom: native <dialog>, falls back to the full-image link */
d.addEventListener('click',function(ev){
  var a=ev.target&&ev.target.closest?ev.target.closest('[data-open-zoom]'):null;
  if(!a)return;
  var dlg=d.getElementById(a.getAttribute('data-open-zoom'));
  if(!dlg||!dlg.showModal)return;
  ev.preventDefault();
  var img=dlg.querySelector('img[data-src]');
  if(img){img.src=img.getAttribute('data-src');img.removeAttribute('data-src');}
  dlg.showModal();
});
d.addEventListener('click',function(ev){
  if(ev.target&&ev.target.matches&&ev.target.matches('dialog.zoomdlg')) ev.target.close();
});


/* tap the tower: numbered hotspots on the real diagram; buttons work by tap, click or keyboard, no hover needed */
var tap=d.querySelector('[data-tap]');
if(tap){var dots=tap.querySelectorAll('[data-spot]'),cards=tap.querySelectorAll('[data-card]');
 function show(k){dots.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.spot===k)});cards.forEach(function(c){if(c.dataset.card===k)c.removeAttribute('data-off');else c.setAttribute('data-off','')});}
 dots.forEach(function(b){b.addEventListener('click',function(){show(b.dataset.spot)})});}

/* build it your way: layers slide apart as the section scrolls through the screen (only while visible) */
var st=d.querySelector('[data-stack]');
if(st&&!reduce&&'IntersectionObserver' in window){var art=st.querySelector('.stack__art'),on=false,tick=false;
 function upd(){tick=false;var r=art.getBoundingClientRect(),vh=innerHeight;var p=(vh*.85-r.top)/(vh*.75);p=Math.max(0,Math.min(1,p));art.style.setProperty('--p',p.toFixed(3));}
 function onScroll(){if(on&&!tick){tick=true;requestAnimationFrame(upd);}}
 new IntersectionObserver(function(es){on=es[0].isIntersecting;if(on)upd();},{rootMargin:'100px 0px'}).observe(art);
 addEventListener('scroll',onScroll,{passive:true});}
else if(st){st.querySelector('.stack__art').style.setProperty('--p',1);}

/* stories reel: click-to-load video (nothing downloads until tapped) */
d.addEventListener('click',function(ev){var b=ev.target&&ev.target.closest?ev.target.closest('[data-video]'):null;if(!b)return;
 var v=d.createElement('video');v.src=b.dataset.video;v.muted=true;v.loop=true;v.playsInline=true;v.setAttribute('playsinline','');v.controls=true;v.setAttribute('aria-label',b.getAttribute('aria-label').replace('Play video: ',''));
 var img=b.querySelector('img');if(img)v.poster=img.currentSrc||img.src;
 var w=d.createElement('div');w.className='story__play';w.appendChild(v);b.replaceWith(w);var p=v.play();if(p&&p.catch)p.catch(function(){});});

/* WhatsApp tap counting for the owner's dashboard. No personal data, no cookies.
   Sends nothing while the site runs as a /preview/ copy; counts only on the client's own domain. */
(function(){if(window.__p1cta)return;window.__p1cta=1;
 if(/^\/preview\//.test(location.pathname)||location.protocol==='file:')return;
 var site='urban-eco',WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,last=0;
 function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=Math.random().toString(36).slice(2)+Date.now().toString(36);sessionStorage.setItem(k,v);}return v;}catch(e){return 'na';}}
 function send(a){var now=Date.now();if(now-last<1500)return;last=now;
  try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},
   body:JSON.stringify({entity:'CtaClick',site:site,cta_type:'whatsapp',cta_ref:(a&&a.dataset.ref)||'',session_id:sid(),page_path:location.pathname.slice(0,200),
   device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:(d.referrer||'').slice(0,200),flag:/[?&]p1test=1/.test(location.search)?'test':undefined})}).catch(function(){});}catch(e){}}
 d.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(a&&WA.test(String(a.href||'')))send(a);},true);
})();
})();
