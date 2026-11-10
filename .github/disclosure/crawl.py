# Disclosure reword crawl (10 Nov 2026): find pages whose text says the site is run by Page One; save exact original bytes.
import re, os, sys, urllib.request, concurrent.futures as cf, random, html
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
SITES={'autotex':'autotexautoparts.com.sg','cska-auto':'cskatrading.com','wrapstar':'wrapstarautostyle.com','star-performance':'starperformancemotor.com','dmts':'jackygearbox.com','ecu-clinic':'theecuclinicsg.com','new-zen-werkz':'newzenwerkz.com.sg','xado':'xado-shop.sg'}
def get(u,t=25):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=t)
        return r.status,r.read(),r.geturl()
    except urllib.error.HTTPError as e: return e.code,b'',u
    except Exception as e: return 0,str(e)[:80].encode(),u
def sitemap_urls(base):
    out=[];seen=set();todo=[base+'/sitemap.xml']
    while todo:
        s=todo.pop()
        if s in seen: continue
        seen.add(s);c,b,_=get(s);b=b.decode('utf-8','replace')
        locs=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',b)
        if '<sitemapindex' in b: todo+=locs
        else: out+=locs
    return out
PAT=re.compile(r'.{0,260}(?:run by Page One|both this website|This website and the SG Car Workshop|运营|營運|Page One Singapore\W{0,40}(?:run|operate)).{0,200}',re.S|re.I)
only=sys.argv[1:] 
for slug,dom in SITES.items():
    if only and slug not in only: continue
    c,b,final=get('https://'+dom+'/')
    base=re.match(r'https?://[^/]+',final).group(0)
    urls=list(dict.fromkeys([base+'/']+sitemap_urls(base)))
    extra=[base+'/'+f for f in ('llms.txt','llms-full.txt','articles/','zh/','zh/articles/','sitemap.xml')]
    urls=list(dict.fromkeys(urls+extra))
    def chk(u):
        c,b,_=get(u+('&' if '?' in u else '?')+'nc=%d'%random.randint(1,10**9))
        t=b.decode('utf-8','replace')
        ms=[re.sub(r'\s+',' ',m.group(0)) for m in re.finditer(r'.{0,200}(?:run by Page One|both this website|This website and the SG Car Workshop|Page One Singapore运营|由 ?Page One).{0,200}',t,re.S|re.I)]
        return u,c,b,ms
    hits=0
    with cf.ThreadPoolExecutor(8) as ex:
        for u,c,b,ms in ex.map(chk,urls):
            if ms:
                hits+=1
                p=u[len(base):].lstrip('/') or 'index'
                if p.endswith('/') : p+='index.html'
                d=f'.github/disclosure/orig/{slug}/'+p
                os.makedirs(os.path.dirname(d),exist_ok=True); open(d,'wb').write(b)
                print(f'HIT {slug} {u} sha-bytes={len(b)} n={len(ms)}',flush=True)
                for m in ms[:6]: print('   >>',m[:420],flush=True)
    print(f'=== {slug} {base} pages={len(urls)} hit_pages={hits}',flush=True)
