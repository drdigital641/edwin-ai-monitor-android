(function(){
var d=document,els=d.querySelectorAll('.rv');
if('IntersectionObserver' in window&&els.length){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});els.forEach(function(el){io.observe(el)})}
else{els.forEach(function(el){el.classList.add('in')})}
var form=d.getElementById('finder');
if(form){var cards=d.querySelectorAll('#results [data-search]'),em=d.getElementById('empty'),q=d.getElementById('q'),ct=d.getElementById('count');
function f(){var sv=form.querySelector('input[name=svc]:checked'),svc=sv?sv.value:'',rg=[].map.call(form.querySelectorAll('input[name=reg]:checked'),function(i){return i.value}),v=q.value.trim().toLowerCase(),n=0;
cards.forEach(function(c){var r=' '+c.getAttribute('data-regions')+' ',ok=(!svc||c.getAttribute('data-cat')===svc)&&(!rg.length||rg.some(function(x){return r.indexOf(' '+x+' ')>-1}))&&(!v||c.getAttribute('data-search').indexOf(v)>-1);c.hidden=!ok;if(ok)n++});
if(ct)ct.innerHTML='<b>'+n+'</b> workshop'+(n==1?'':'s');if(em)em.classList.toggle('show',!n)}
form.addEventListener('change',f);q.addEventListener('input',f);form.addEventListener('submit',function(e){e.preventDefault();f()});
var rs=d.getElementById('reset');if(rs)rs.addEventListener('click',function(){HTMLFormElement.prototype.reset.call(form);f()});f()}
/* Featured carousel: CSS scroll-snap row; glides on its own unless the visitor prefers reduced motion; pauses on hover, focus and touch. */
var tr=d.getElementById('track');
if(tr){var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches,hold=false,vis=true,tm;
function step(dir){var li=tr.querySelector('li');if(!li)return;var w=li.getBoundingClientRect().width+12,max=tr.scrollWidth-tr.clientWidth;
if(dir>0&&tr.scrollLeft>=max-6)tr.scrollTo({left:0,behavior:rm?'auto':'smooth'});else if(dir<0&&tr.scrollLeft<=6)tr.scrollTo({left:max,behavior:rm?'auto':'smooth'});else tr.scrollBy({left:dir*w,behavior:rm?'auto':'smooth'})}
var pv=d.getElementById('cprev'),nx=d.getElementById('cnext');if(pv)pv.addEventListener('click',function(){step(-1)});if(nx)nx.addEventListener('click',function(){step(1)});
tr.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){step(1);e.preventDefault()}else if(e.key==='ArrowLeft'){step(-1);e.preventDefault()}});
if(!rm){var pause=function(){hold=true;clearTimeout(tm)},resume=function(ms){clearTimeout(tm);tm=setTimeout(function(){hold=false},ms||800)};
tr.addEventListener('mouseenter',pause);tr.addEventListener('mouseleave',function(){resume(800)});tr.addEventListener('focusin',pause);tr.addEventListener('focusout',function(){resume(800)});
tr.addEventListener('touchstart',pause,{passive:true});tr.addEventListener('touchend',function(){resume(6000)},{passive:true});tr.addEventListener('pointerdown',pause);
if('IntersectionObserver' in window)new IntersectionObserver(function(es){vis=es[0].isIntersecting}).observe(tr);
setInterval(function(){if(!hold&&vis&&!d.hidden)step(1)},4500)}}
d.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[data-cta]');if(!a)return;var c=a.getAttribute('data-cta');try{if(window.dataLayer)window.dataLayer.push({event:'cta_click',cta:c})}catch(x){}track(a,c)});
/* Lead counter: Page One Controller public write-only "track" function (same endpoint and payload as pageonesingapore.com main.js).
   Fires ONLY on the live directory domain, so preview clicks are not counted. WhatsApp and call taps on business listings only. */
var LIVE_HOST='sgcarworkshop.sg',APP='6ac7f2548a9c3877449e2772';
function rid(){return Math.random().toString(36).slice(2)+Date.now().toString(36)}
function keep(st,k){try{var v=st.getItem(k);if(!v){v=rid();st.setItem(k,v)}return v}catch(x){return rid()}}
function track(a,c){try{
if(location.hostname!==LIVE_HOST&&location.hostname!=='www.'+LIVE_HOST)return;
if(navigator.doNotTrack==='1'||window.doNotTrack==='1'||navigator.webdriver)return;
var tier=a.getAttribute('data-tier');if(!tier||!/^(whatsapp|call)_dir_/.test(c))return;
var slug=c.replace(/^(whatsapp|call)_dir_/,''),page=a.getAttribute('data-page')||location.pathname,ua=navigator.userAgent;
var body=JSON.stringify({entity:'CtaClick',site:'sgcarworkshop',session_id:keep(sessionStorage,'sgcw-sid'),visitor_id:keep(localStorage,'sgcw-vid'),page_path:location.pathname,
referrer:(document.referrer||'').slice(0,300),device_type:/Mobi|Android|iPhone/i.test(ua)?'mobile':/iPad|Tablet/i.test(ua)?'tablet':'desktop',
cta_type:c,enquiry_ref:slug+'|'+tier+'|'+page});
var url='https://base44.app/api/apps/'+APP+'/functions/track',sent=false;
if(navigator.sendBeacon){try{sent=navigator.sendBeacon(url,new Blob([body],{type:'application/json'}))}catch(x){}}
if(!sent&&window.fetch){fetch(url,{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:body}).catch(function(){})}
}catch(x){}}
})();

/* Basic cards: 1 Google listing photo via Places API (New), shown with the photographer credit Google requires.
   Runs only when a gmaps-key meta is present (added at go-live). Loads when the card scrolls into view. Nothing is cached. */
(function () {
  var m = document.querySelector('meta[name="gmaps-key"]'); if (!m || !('IntersectionObserver' in window)) return;
  var key = m.content;
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (en) {
      if (!en.isIntersecting) return; io.unobserve(en.target);
      var el = en.target, pid = el.getAttribute('data-place'); if (!pid) return;
      fetch('https://places.googleapis.com/v1/places/' + encodeURIComponent(pid) + '?fields=photos&key=' + key)
        .then(function (r) { return r.ok ? r.json() : null; })
        .then(function (d) {
          var ph = d && d.photos && d.photos[0]; if (!ph) return;
          var img = new Image(); img.alt = ''; img.loading = 'lazy'; img.className = 'gph-img';
          img.src = 'https://places.googleapis.com/v1/' + ph.name + '/media?maxWidthPx=480&key=' + key;
          var a = (ph.authorAttributions || [])[0], cr = document.createElement('span'); cr.className = 'gph-credit';
          cr.textContent = 'Photo: ' + (a ? a.displayName : 'Google') + ' via Google';
          img.onload = function () { el.appendChild(img); el.appendChild(cr); el.classList.add('has-img'); };
        }).catch(function () {});
    });
  }, { rootMargin: '200px' });
  document.querySelectorAll('.gph[data-place]').forEach(function (el) { io.observe(el); });
})();
