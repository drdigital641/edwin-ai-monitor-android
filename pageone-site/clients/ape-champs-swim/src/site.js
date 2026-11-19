/* Ape Champs Swim: contact form opens WhatsApp with the parent's details. Works without JS (plain wa.me link). */
(function(){var f=document.getElementById('waform');if(!f)return;
f.addEventListener('submit',function(e){e.preventDefault();var g=function(n){var el=f.elements[n];return el&&el.value?el.value.trim():''};
var t='Hi, I would like to enquire about kids swimming lessons at my condo.';
if(g('age'))t+='\nChild\'s age: '+g('age');if(g('area'))t+='\nArea: '+g('area');if(g('condo'))t+='\nCondo: '+g('condo');
if(g('exp'))t+='\nSwimming experience: '+g('exp');if(g('msg'))t+='\n'+g('msg');
window.open('https://wa.me/'+f.action.split('/').pop()+'?text='+encodeURIComponent(t),'_blank','noopener');});
/* close the phone menu after a tap on a link */
var m=document.querySelector('.menu');if(m)m.addEventListener('click',function(e){if(e.target.closest('a'))m.removeAttribute('open')});})();
