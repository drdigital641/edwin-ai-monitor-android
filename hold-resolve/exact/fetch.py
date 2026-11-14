# GET-only exact copy: each line of the list is "<url>\t<repo path>". Writes the bytes as served, plus a sha256 manifest.
import sys, hashlib, time, urllib.request, os
rows = [l.rstrip('\n').split('\t') for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
out, bad = [], 0
for url, path in rows:
    req = urllib.request.Request(url + ('&' if '?' in url else '?') + 'cmp=' + str(int(time.time())), headers={'User-Agent': 'Mozilla/5.0 (hold-exact-fetch)'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            if r.status != 200: raise Exception('HTTP ' + str(r.status))
            b = r.read()
    except Exception as e:
        print('FAIL', url, e); bad += 1; continue
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'wb').write(b)
    out.append(hashlib.sha256(b).hexdigest() + '  ' + str(len(b)) + '  ' + path)
    print('ok', len(b), path)
open('hold-resolve/exact/manifest.txt', 'w').write('\n'.join(out) + '\n')
if bad: sys.exit(1)
