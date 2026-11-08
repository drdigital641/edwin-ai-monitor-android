"""Decode every wa.me link in site/ and print the distinct prefilled texts (sends nothing)."""
import glob, html, re, sys
from urllib.parse import urlparse, parse_qs
S = 'site'
seen, bad = {}, 0
for f in sorted(glob.glob(S + '/**/*.html', recursive=True)):
    for href in re.findall(r'href="(https://wa\.me/[^"]*)"', open(f, encoding='utf-8').read()):
        u = urlparse(html.unescape(href))
        q = parse_qs(u.query, keep_blank_values=True)
        txt = q.get('text', [''])[0]
        if u.path != '/6590062198' or not txt.startswith('[House: ') or '___' not in txt or ' ' in u.query or '[' in u.query:
            print('BAD', f, href); bad += 1
        seen.setdefault(txt, set()).add(f)
for t, fs in sorted(seen.items()):
    print('%3d pages | %s' % (len(fs), t))
print('distinct prefills', len(seen), 'bad', bad)
sys.exit(1 if bad else 0)
