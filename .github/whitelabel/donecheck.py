# White-label DONE CHECK (10 Nov 2026): per site, home + 2 inner pages + 1 article, footer must have 0 "pageonesingapore" / 0 "Page One".
import re, json, random, urllib.request
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
def get(u):
    try:
        r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA,'Cache-Control':'no-cache'}),timeout=30)
        return r.status, r.read().decode('utf-8','replace'), r.geturl()
    except urllib.error.HTTPError as e: return e.code,'',u
    except Exception as e: return 0,'',u
ART=re.compile(r'/(articles|insights|guides|blog|news)/[^/]+')
out={}
for line in open('.github/whitelabel/sites.txt'):
    slug,dom=line.split()
    c,b,final=get('https://'+dom+'/'); base=re.match(r'https?://[^/]+',final).group(0)
    _,sm,_=get(base+'/sitemap.xml')
    locs=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',sm)
    if '<sitemapindex' in sm:
        locs2=[]
        for s in locs: locs2+=re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',get(s)[1])
        locs=locs2
    locs=[u for u in locs if u.rstrip('/')!=base]
    arts=[u for u in locs if ART.search(u) and not re.search(r'/(articles|insights|guides|blog|news)/?$',u)]
    inner=[u for u in locs if u not in arts and not re.search(r'/(articles|insights|guides|blog|news)/?$',u)]
    pick=[base+'/']+inner[:1]+inner[len(inner)//2:len(inner)//2+1]+arts[-1:]
    rows=[]
    for u in pick:
        c,h,_=get(u+('&' if '?' in u else '?')+'nc=%d'%random.randint(1,10**9))
        foot=(re.findall(r'<footer\b.*?</footer>',h,re.S) or [''])[-1]
        rows.append(dict(url=u,code=c,footer_found=bool(foot),footer_pageonesingapore=foot.count('pageonesingapore'),footer_page_one=foot.count('Page One'),page_credit_links=len(re.findall(r'href="https://pageonesingapore\.com/?"',h))))
        r=rows[-1]; print(f"{slug:16} {c} footer:{'yes' if foot else 'NO'} pageonesingapore={r['footer_pageonesingapore']} 'Page One'={r['footer_page_one']} credit_links_on_page={r['page_credit_links']}  {u}")
    out[slug]=dict(base=base,rows=rows)
json.dump(out,open('whitelabel/20261110/donecheck.json','w'),indent=1)
