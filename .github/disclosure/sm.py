import re,urllib.request
UA='Mozilla/5.0 Chrome/130'
def get(u): return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=30).read().decode('utf-8','replace')
T={'autotexautoparts.com.sg':['/about/'],'cskatrading.com':['/articles/new-car-workshop-equipment-checklist/'],'starperformancemotor.com':['/articles/what-to-do-after-buying-a-used-car/'],'newzenwerkz.com.sg':['/articles/brake-warning-signs/','/zh/articles/brake-warning-signs/'],'wrapstarautostyle.com':['/articles/car-wrap-or-respray-which-is-better/'],'jackygearbox.com':['/gearbox-problems/car-jerks-when-changing-gear/'],'theecuclinicsg.com':['/articles/find-abs-ecu-module-specialist-singapore/'],'xado-shop.sg':['/find-a-xado-workshop.html']}
for h,ps in T.items():
    for pre in ('https://'+h,'https://www.'+h):
        try: x=get(pre+'/sitemap.xml'); break
        except Exception as e: x=None; print('ERR',pre,e)
    if x is None: continue
    print('=====',h,len(x),'index' if '<sitemapindex' in x else 'urlset', repr(x[:200]))
    docs=[(pre+'/sitemap.xml',x)]
    if '<sitemapindex' in x:
        docs=[(c,get(c)) for c in re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',x)]
    for p in ps:
        for sm,d in docs:
            for m in re.finditer(r'<url>(?:(?!</url>).)*?'+re.escape(p)+r'</loc>.*?</url>',d,re.S):
                print('SM',sm,repr(m.group(0)))
