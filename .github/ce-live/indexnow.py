# IndexNow key-file check (mode=check) or full sitemap submit (mode=submit). Run on a GitHub runner.
import json,re,sys,urllib.request,urllib.error
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
mp='submit contiexpert.sg'.split(); mode=mp[0]; only=mp[1:]  # optional host filter
def get(u):
  return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA}),timeout=25).read().decode('utf-8','replace')
def locs(x): return re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',x)
for line in open('.github/ce-live/sites.txt'):
  p=line.split()
  if not p: continue
  host,key,sms=p[0],p[1],[s for s in p[2:] if s.endswith('.xml')]
  if only and host not in only: continue
  try:
    body=get(f'https://{host}/{key}.txt').strip(); live='yes' if body==key else 'WRONG:'+body[:40]
  except urllib.error.HTTPError as e: live=f'no ({e.code})'
  except Exception as e: live=f'no ({e})'
  if mode!='submit' or live!='yes': print(f'RES {host} key={live}'); continue
  urls=[]
  for sm in sms:
    try:
      x=get(f'https://{host}{sm}'); es=locs(x)
      if '<sitemapindex' in x: es=[u for c in es for u in locs(get(c))]
      urls+=es
    except Exception as e: print(f'ERR {host}{sm} {e}')
  bare=host.replace('www.','')
  urls=[u for u in dict.fromkeys(urls) if re.match(rf'https?://(www\.)?{re.escape(bare)}(/|$)',u)]
  urls=[u if u.split('/')[2]==host else u.replace(u.split('/')[2],host,1) for u in urls]
  urls=list(dict.fromkeys(urls))
  if not urls: print(f'RES {host} key=yes urls=0 code=-'); continue
  data=json.dumps({'host':host,'key':key,'keyLocation':f'https://{host}/{key}.txt','urlList':urls[:10000]}).encode()
  try: st=urllib.request.urlopen(urllib.request.Request('https://api.indexnow.org/indexnow',data=data,headers={'Content-Type':'application/json; charset=utf-8'}),timeout=40).status
  except urllib.error.HTTPError as e: st=f'{e.code} {e.read()[:120]}'
  except Exception as e: st=str(e)
  print(f'RES {host} key=yes urls={len(urls[:10000])} code={st}')
