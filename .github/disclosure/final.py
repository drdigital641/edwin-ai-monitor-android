import re,json,urllib.request,concurrent.futures as cf,random
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
def get(u,t=30):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=t); return r.status,r.read().decode('utf-8','replace'),r.geturl()
    except urllib.error.HTTPError as e: return e.code,'',u
    except Exception as e: return 0,str(e)[:80],u
K={'autotexautoparts.com.sg':('7d3e9a51c4b84f2e9a0c6b1d58e2f437',['/about/']),
'cskatrading.com':('208f285bfeaaa073ac0b7bb77afc1625',['/articles/new-car-workshop-equipment-checklist/']),
'wrapstarautostyle.com':('dcf0dd5907cd49c0ba4cdeee3318b569',['/articles/car-wrap-or-respray-which-is-better/']),
'starperformancemotor.com':('99381246b278105dbbf132423ac73bbc',['/articles/what-to-do-after-buying-a-used-car/']),
'jackygearbox.com':('bae8ecc2b65d5772f8be703cd544d1bc',['/gearbox-problems/car-jerks-when-changing-gear/']),
'theecuclinicsg.com':('a297274b0e018294438558b379efa82a',['/articles/find-abs-ecu-module-specialist-singapore/']),
'newzenwerkz.com.sg':('ea97d7cd7c1340c781fcd248d8d2c2ec',['/articles/brake-warning-signs/','/zh/articles/brake-warning-signs/']),
'xado-shop.sg':('879bbba824426e5ff0c647ecf4805b25',['/find-a-xado-workshop.html'])}
OLD=re.compile(r'run by Page One|both this website|This website and the SG Car Workshop|and this website are both|both sites are run|由 ?Page One Singapore 运营|都由 Page One',re.I)
NEWEN='This business supports SG Car Workshop (sgcarworkshop.sg), a driver-focused workshop directory run by Page One Singapore.'
NEWZH='本公司支持 SG Car Workshop（sgcarworkshop.sg），这是一个由 Page One Singapore 运营、以车主为本的车厂名录。'
def sm(base):
    out=[];todo=[base+'/sitemap.xml'];seen=set()
    while todo:
        s=todo.pop()
        if s in seen: continue
        seen.add(s);c,b,_=get(s);l=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',b)
        if '<sitemapindex' in b: todo+=l
        else: out+=l
    return out
for h,(key,paths) in K.items():
    c,b,fin=get('https://'+h+'/'); base=re.match(r'https?://[^/]+',fin).group(0)
    # IndexNow for changed pages only
    urls=[base+p for p in paths]
    kc,kb,_=get(f'{base}/{key}.txt'); kl='yes' if kb.strip()==key else f'NO({kc})'
    code='-'
    if kl=='yes':
        host=re.sub(r'^https?://','',base)
        data=json.dumps({'host':host,'key':key,'keyLocation':f'{base}/{key}.txt','urlList':urls}).encode()
        try: code=urllib.request.urlopen(urllib.request.Request('https://api.indexnow.org/indexnow',data=data,headers={'Content-Type':'application/json; charset=utf-8'}),timeout=40).status
        except urllib.error.HTTPError as e: code=f'{e.code} {e.read()[:100]}'
        except Exception as e: code=str(e)[:80]
    print(f'INDEXNOW {h} key={kl} urls={len(urls)} code={code}',flush=True)
    # live counts
    allu=list(dict.fromkeys([base+'/']+sm(base)+[base+'/'+f for f in ('llms.txt','llms-full.txt')]+urls))
    def chk(u):
        c,b,_=get(u+('&' if '?' in u else '?')+'nc=%d'%random.randint(1,10**9)); return u,c,len(OLD.findall(b)),b.count(NEWEN)+b.count(NEWZH)
    old=0;new=0;oldp=[];newp=[];non=0
    with cf.ThreadPoolExecutor(8) as ex:
        for u,c,o,n in ex.map(chk,allu):
            if c!=200: non+=1
            old+=o;new+=n
            if o: oldp.append(u)
            if n: newp.append(u.replace(base,''))
    print(f'COUNT {h} pages={len(allu)} non200={non} OLD={old} NEW={new} oldpages={oldp[:5]} newpages={newp}',flush=True)
