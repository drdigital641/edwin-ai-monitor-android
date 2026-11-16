import sys
E=[("/* p1-cta.js v4 (16 Nov 2026):","/* p1-cta.js v4.1 (16 Nov 2026, adds bot:1 for automated browsers):"),
("waOpen=0;","waOpen=0,BOT=(function(){try{return navigator.webdriver===true||/bot|crawl|spider|slurp|headless|lighthouse|pagespeed|gtmetrix|pingdom|phantomjs|selenium|puppeteer|playwright/i.test(navigator.userAgent||'')}catch(e){return false}})();"),
("screen:(screen.width||0)+'x'+(screen.height||0),test:","screen:(screen.width||0)+'x'+(screen.height||0),bot:BOT?1:undefined,test:")]
for p in sys.argv[1:]:
    s=open(p).read()
    for a,b in E:
        assert s.count(a)==1,(p,a); s=s.replace(a,b)
    open(p,'w').write(s)
