# Daily crawler check (Edwin's permanent rule, 19 Oct 2026). Run from a Base44 sandbox (live sites block this container):
#   python3 crawlcheck.py host1 host2 ...
import re,sys,urllib.request,urllib.error,xml.dom.minidom
UA='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
BOTS={'OAI-SearchBot':'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.3; +https://openai.com/searchbot',
'Googlebot':'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
'bingbot':'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)'}
def get(u,ua=UA):
  try:
    r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':ua}),timeout=20); return r.status,r.read().decode('utf-8','replace'),r.geturl()
  except urllib.error.HTTPError as e: return e.code,'',u
  except Exception as e: return 0,str(e),u
def groups(txt):
  g=[];cur=None;last_ua=False
  for line in txt.splitlines():
    line=line.split('#')[0].strip()
    if not line or ':' not in line: continue
    k,v=[x.strip() for x in line.split(':',1)];k=k.lower()
    if k=='user-agent':
      if not last_ua: cur={'ua':[],'rules':[]};g.append(cur)
      cur['ua'].append(v.lower());last_ua=True
    else:
      last_ua=False
      if cur and k in('allow','disallow'): cur['rules'].append((k,v))
  return g
def verdict(g,bot):
  b=bot.lower()
  m=[x for x in g if any(u!='*' and u in b for u in x['ua'])] or [x for x in g if '*' in x['ua']]
  named=any(any(u!='*' and u in b for u in x['ua']) for x in g)
  rules=[r for x in m for r in x['rules']]
  blocked=any(k=='disallow' and v=='/' for k,v in rules) and not any(k=='allow' and v=='/' for k,v in rules)
  return named,blocked
for host in sys.argv[1:]:
  st,rb,_=get(f'https://{host}/robots.txt')
  g=groups(rb) if st==200 else []
  sms=re.findall(r'(?im)^\s*sitemap:\s*(\S+)',rb)
  out=[f'{host}: robots {st}']
  for bot in BOTS:
    n,b=verdict(g,bot); out.append(f'{bot}:{"BLOCKED" if b else ("named-allow" if n else "allowed(*)")}')
  smok=[]
  for s in sms[:3]:
    s2,x,_=get(s)
    try: xml.dom.minidom.parseString(x.encode()); v='valid'
    except Exception: v='INVALID'
    smok.append(f'{s.split("/",3)[-1]}={s2}/{v}/{x.count("<loc>")}urls')
  out.append('sitemaps:'+(','.join(smok) if smok else 'NONE-IN-ROBOTS'))
  hs=[]
  for bot,ua in BOTS.items():
    s3,_,_=get(f'https://{host}/',ua); hs.append(f'{bot[:4]}{s3}')
  out.append('home:'+' '.join(hs))
  print(' | '.join(out))
