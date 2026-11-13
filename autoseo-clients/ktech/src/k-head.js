(function(){var d=document,rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
d.addEventListener('click',function(e){var b=e.target.closest('.menu-btn');if(!b)return;var n=d.getElementById('mnav');var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)});
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
ready(function(){
 /* scan tablet: systems tick OK one by one, then loop */
 var t=d.querySelector('.tab');if(t){var li=[].slice.call(t.querySelectorAll('.sys li')),bar=t.querySelector('.bar b'),st=t.querySelector('.st'),i=0,rpm=t.querySelector('.rpm b');
  var run=function(){if(d.hidden)return;if(i<li.length){li[i].classList.add('on');i++;bar.style.width=(i/li.length*100)+'%';if(i===li.length)st.textContent=st.getAttribute('data-done')}
   else{li.forEach(function(x){x.classList.remove('on')});i=0;bar.style.width='0';st.textContent=st.getAttribute('data-run')}};
  if(rm){li.forEach(function(x){x.classList.add('on')});bar.style.width='100%';st.textContent=st.getAttribute('data-done')}else{setInterval(run,850)}
  if(rpm&&!rm)setInterval(function(){rpm.textContent=String(780+Math.round(Math.random()*60))},700)}
 /* reveal */
 var els=[].slice.call(d.querySelectorAll('.real figure,.sh,.proof>*,.steps li,.seo,.faq details,.svc article,.flist .fam,.cbox'));
 if(!rm&&'IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add('in');io.unobserve(en.target)}})},{rootMargin:'0px 0px -6% 0px',threshold:.06});
  els.forEach(function(e){e.classList.add('rv');io.observe(e)})}
});
/* enquiry form -> WhatsApp */
ready(function(){var f=d.getElementById('enquiry');if(!f)return;f.addEventListener('submit',function(e){e.preventDefault();var g=function(n){var x=f.elements[n];return x&&x.value?x.value.trim():''};
 var L=JSON.parse(f.getAttribute('data-lines')),o=[L[0]];if(g('need'))o.push(L[1]+g('need'));if(g('name'))o.push(L[2]+g('name'));if(g('shop'))o.push(L[3]+g('shop'));
 window.open('https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(o.join('\n')),'_blank','noopener')})});
})();
