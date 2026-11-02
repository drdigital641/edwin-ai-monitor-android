/* WhatsApp tap counter -> Page One Controller (public write-only "track" fn). Replace SLUG with the Controller Client slug. Added 22 Oct 2026. */
(function(){if(window.__p1cta)return;var h=location.hostname.replace(/^www\./,'');if(h==='pageonesingapore.com'||h==='localhost')return;window.__p1cta=1;
var WA=/^(https?:\/\/(wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\/|whatsapp:)/i,last=0;
function sid(){try{var k='p1cta_sid',v=sessionStorage.getItem(k);if(!v){v=Math.random().toString(36).slice(2)+Date.now().toString(36);sessionStorage.setItem(k,v)}return v}catch(e){return'na'}}
function send(){var n=Date.now();if(n-last<1500)return;last=n;try{fetch('https://base44.app/api/apps/6ac7f2548a9c3877449e2772/functions/track',{method:'POST',credentials:'omit',keepalive:true,headers:{'Content-Type':'application/json'},body:JSON.stringify({entity:'CtaClick',site:'rc-design-build',cta_type:'whatsapp',session_id:sid(),page_path:location.pathname.slice(0,200),device_type:/Mobi|Android|iPhone/i.test(navigator.userAgent)?'mobile':'desktop',referrer:(document.referrer||'').slice(0,200)})}).catch(function(){})}catch(e){}}
window.p1WaTap=send;
document.addEventListener('click',function(e){var a=e.target&&e.target.closest?e.target.closest('a[href]'):null;if(a&&WA.test(String(a.href||'')))send()},true);
document.addEventListener('submit',function(e){var f=e.target;if(f&&f.getAttribute&&(f.getAttribute('data-wa')||/wa\.me|whatsapp/i.test(f.getAttribute('action')||'')))send()},true)})();
