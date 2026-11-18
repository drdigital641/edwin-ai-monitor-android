(function(){var d=document;function init(){var q=d.getElementById('nlq'),f=d.getElementById('nls');if(!q||!f)return;
var cards=[].slice.call(d.querySelectorAll('#lfeat .lc,#lgrid .lc')),none=d.getElementById('nls-none'),cnt=d.getElementById('nls-n'),x=d.getElementById('nls-x'),
lf=d.getElementById('lfeat'),lg=d.getElementById('lgrid'),hf=d.getElementById('nlh-f'),hl=d.getElementById('nlh-l'),wa=d.getElementById('nls-wa'),wa0=wa?wa.getAttribute('href'):'',kind='All',used=0,one=null,tm;
function N(s){s=String(s||'').toLowerCase();try{s=s.normalize('NFD').replace(/[̀-ͯ]/g,'')}catch(e){}return s.replace(/&/g,' and ').replace(/[^a-z0-9]+/g,' ').trim()}
cards.forEach(function(c){c._s=' '+N(c.getAttribute('data-s'))+' '});
function ok(s,ws){for(var i=0;i<ws.length;i++){var w=ws[i];if(w.length<3?s.indexOf(' '+w)<0:s.indexOf(w)<0)return false}return true}
function run(){var raw=q.value,ws=N(raw)?N(raw).split(' '):[],n=0,nf=0,nl=0,last=null;
cards.forEach(function(c){var m=(kind==='All'||c.getAttribute('data-kind')===kind)&&ok(c._s,ws);c.hidden=!m;if(m){n++;last=c;if(c.parentNode===lf)nf++;else nl++}});
lf.hidden=hf.hidden=!nf;lg.hidden=hl.hidden=!nl;none.hidden=n>0;x.hidden=!raw;one=n===1?last:null;
cnt.textContent=ws.length?(n?n+(n===1?' project found. Press Enter to open it.':' projects found'):''):'';
if(wa){if(ws.length&&!n){var t="Hi Maison, I couldn't find "+raw.trim().slice(0,60)+" on your new launches page. Can you check it?";wa.setAttribute('href','https://wa.me/6593391185?text='+encodeURIComponent(t))}else wa.setAttribute('href',wa0)}}
q.addEventListener('input',function(){clearTimeout(tm);tm=setTimeout(run,60);if(!used&&q.value.trim().length>=2){used=1;try{if(window.p1CtaTap)window.p1CtaTap('search_used',q)}catch(e){}}});
f.addEventListener('submit',function(e){e.preventDefault();clearTimeout(tm);run();if(one){location.href=one.getAttribute('href')}else{q.blur()}});
x.addEventListener('click',function(){q.value='';run();q.focus()});
[].forEach.call(d.querySelectorAll('.chip'),function(c){c.addEventListener('click',function(){kind=c.getAttribute('data-f')||'All';run()})});
var p='';try{p=new URLSearchParams(location.search).get('q')||''}catch(e){}if(p){q.value=p.slice(0,60);run()}}
if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',init);else init()})();
