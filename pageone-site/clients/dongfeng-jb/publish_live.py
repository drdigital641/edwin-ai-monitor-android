#!/usr/bin/env python3
"""Build the LIVE (mykar.my) copy of the site into ./site (build.py keeps LIVE=False, so URLs are swapped here).
Method from README: build with DF_OUT, replace the preview URL with https://mykar.my/ (and /preview/dongfeng-jb/ -> / in 404.html)."""
import os, re, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join('/tmp', 'df-build-live')
OUT = os.path.join(HERE, 'site')
shutil.rmtree(TMP, ignore_errors=True)
env = dict(os.environ, DF_OUT=TMP)
subprocess.check_call([sys.executable, os.path.join(HERE, 'build.py')], env=env)
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
for root, _, files in os.walk(TMP):
    for fn in files:
        p = os.path.join(root, fn)
        rel = os.path.relpath(p, TMP)
        dst = os.path.join(OUT, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if fn.endswith(('.html', '.xml', '.txt', '.webmanifest', '.js', '.css')):
            s = open(p, encoding='utf-8').read()
            s = s.replace('https://pageonesingapore.com/preview/dongfeng-jb/', 'https://mykar.my/')
            s = s.replace('"/preview/dongfeng-jb/', '"/')
            open(dst, 'w', encoding='utf-8').write(s)
        else:
            shutil.copy(p, dst)
print('live copy written to', OUT)
