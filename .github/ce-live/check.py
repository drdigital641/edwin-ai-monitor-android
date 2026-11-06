# Live check of contiexpert.sg from a GitHub runner: titles, brand, media hosts, videos.
import re,urllib.request
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
def get(u):
  r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':UA,'Cache-Control':'no-cache'}),timeout=30); return r.status,r.read()
_,sm=get('https://contiexpert.sg/sitemap.xml'); urls=re.findall(r'<loc>([^<]+)</loc>',sm.decode())
print('SITEMAP urls',len(urls),'lastmod',sorted(set(re.findall(r'<lastmod>([^<]+)',sm.decode()))))
bad=0
bare=[]
for u in urls+['https://contiexpert.sg/404.html','https://contiexpert.sg/llms.txt','https://contiexpert.sg/ce.js','https://contiexpert.sg/ce.css','https://contiexpert.sg/wa-tap-counter.js','https://contiexpert.sg/site.webmanifest','https://contiexpert.sg/robots.txt','https://contiexpert.sg/sitemap.xml']:
  try: st,b=get(u)
  except Exception as e: print('ERR',u,e); bad+=1; continue
  t=b.decode('utf-8','replace'); hits=re.findall(r'[^\s"\']*(?:jsdelivr|github)[^\s"\']*',t,re.I)
  title=(re.search(r'<title>([^<]*)',t) or [None,''])[1]
  sn=(re.search(r'og:site_name" content="([^"]*)',t) or [None,''])[1]
  nm=(re.search(r'"@type": "AutoRepair"[^}]*?"name": "([^"]*)"',t) or [None,''])[1]
  if hits: bad+=1
  s=re.sub(r'<div class="legal">.*?</div>','',t,flags=re.S).replace('"legalName": "Volt Autocare Pte. Ltd."','')
  if u.endswith('/privacy/'): s=s.replace('Volt Autocare Pte. Ltd.','')
  for m in re.finditer(r'(?<!by )Volt(?: |\+|%20)Autocare(?!(?: |\+|%20)(?:@|%40))',s): bare.append((u.replace('https://contiexpert.sg',''),s[max(0,m.start()-40):m.end()+15]))
  print(st,u.replace('https://contiexpert.sg',''),'|',title,'|',sn,'|',nm,'| ext-media:',hits[:3])
for v in ('find-us-sm','ev-ppi-sm'):
  st,b=get(f'https://contiexpert.sg/assets/video/{v}.mp4'); print('VIDEO',v,st,len(b))
print('PAGES WITH jsdelivr/github:',bad)
print('BARE Volt Autocare (outside legal footer, privacy, legalName, Google Maps listing name):',len(bare))
for b in bare: print('  BARE',b)
