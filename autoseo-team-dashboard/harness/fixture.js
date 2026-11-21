// LOCAL SCREENSHOT HARNESS ONLY (never uploaded). Real Controller roster fields read 21 Nov 2026; health/taps/articles
// are left empty because the signed link is OFF, so the Controller has not computed them for this app.
(function(){
var P='https://autoseo.my/preview/';
function pv(n,s){return {id:s,name:n,step:'preview',preview_url:P+s+'/',live_url:'',golive_domain:'',golive:false,domain_check:null,health:'none',taps:{wa:0,call:0,other:0},articles:0};}
function lv(n,s,d,g){return {id:s,name:n,step:'live',preview_url:'',live_url:'https://'+d+'/',golive_domain:g?d:'',golive:!!g,domain_check:g?{dns_ok:true,https_ok:true,at:'2026-11-20T03:00:00Z'}:null,health:'none',taps:{wa:0,call:0,other:0},articles:0,billing_hint:s==='ktech'?'not_billed':''};}
var clients=[pv('Advance Machinery Movers Sdn. Bhd.','advance-machinery-movers'),pv('Hock Chuan Hiong 福荃香肉乾至尊','hock-chuan-hiong'),pv('JT Autoworks Pte. Ltd.','jt-autoworks'),pv('LT Automart','lt-automart'),pv('MCS Auto Spray Painting','mcs-auto-spray-painting'),pv('Overseas Tyre And Services Sdn Bhd','overseas-tyre'),pv('Studio 87','studio-87'),
lv('Ap Car Air-Cond Centre','apcar','apcar.com.my'),lv('Benz World (M) Sdn Bhd','benz-world','benzworld.my'),lv('Carzy World Sdn Bhd','carzy-world','carzyworld.com.my'),lv('CCH Automotive Sdn Bhd','cch-automotive','cchautomotive.my'),lv('EMATS TECHNOLOGY SALES AND SERVICE','emats','ecumats.my'),lv('HX Auto Service','hx-auto','hxautoservice.com.my',1),lv('HYBRID WORLD (M) SDN BHD','hybrid-world','hybridworld.com.my'),lv('K Tech Auto Solution (ktech.my)','ktech','ktech.my'),lv('Rasa Sayang Automotive Group Sdn Bhd','rasa-sayang','rasasayangautomotive.com',1)];
var plans=[];
var nodes=[{id:'c',name:'AutoSEO.my',role:'centre',parentId:''},{id:'ch',name:'Cheng',role:'salesperson',parentId:'c'},{id:'ap',name:'Ah p',role:'salesperson',parentId:'c'},{id:'ak',name:'Ah K',role:'salesperson',parentId:'ap'},{id:'kau',name:'Ah kau',role:'salesperson',parentId:'ch'},{id:'ac',name:'Ah C',role:'salesperson',parentId:'ch'},{id:'ad',name:'Ah D',role:'salesperson',parentId:'ac'},{id:'ae',name:'Ah E',role:'salesperson',parentId:'ad'}];
var mode=new URLSearchParams(location.search).get('mode');
window.AUTOSEO_API=function(a,b){
 if(mode==='off') return Promise.resolve({ok:false,code:'not_set'});
 if(a==='team_clients') return Promise.resolve({ok:true,clients:clients,as_of:'2026-11-21T01:00:00Z'});
 if(a==='billing_list') return Promise.resolve({ok:true,plans:plans});
 if(a==='sales_data') return Promise.resolve({ok:true,nodes:nodes,settings:{customer:300,direct:60,referral:40}});
 return Promise.resolve({ok:true});
};
window.AUTOSEO_SIGNOUT=function(){};
})();
