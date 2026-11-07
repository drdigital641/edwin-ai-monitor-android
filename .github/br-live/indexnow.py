import json, re, urllib.request, urllib.error
key = 'b7e1c94a2f6d4e3b8a5c0d9e1f2a3b4c'; host = 'batteryrescue.sg'
sm = urllib.request.urlopen('https://batteryrescue.sg/sitemap.xml', timeout=30).read().decode()
urls = [u for u, d in re.findall(r'<loc>([^<]+)</loc><lastmod>([^<]+)</lastmod>', sm) if d == '2026-11-07'] + ['https://batteryrescue.sg/llms.txt']
data = json.dumps({'host': host, 'key': key, 'keyLocation': f'https://{host}/{key}.txt', 'urlList': urls}).encode()
try:
    st = urllib.request.urlopen(urllib.request.Request('https://api.indexnow.org/indexnow', data=data, headers={'Content-Type': 'application/json; charset=utf-8'}), timeout=40).status
except urllib.error.HTTPError as e:
    st = f'{e.code} {e.read()[:120]}'
except Exception as e:
    st = str(e)
print('INDEXNOW', st)
open('shots/result.txt', 'a').write(f'\nIndexNow {len(urls)} URLs: {st}\n')
