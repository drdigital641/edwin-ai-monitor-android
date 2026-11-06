"""Chinese (Simplified) version of the New Zen Werkz site at /zh/ (Edwin, 6 Nov 2026).
Run after build.py: python3 build.py && python3 build_zh.py
Takes every built English page, swaps text for the translations in zh/strings_zh.json (same facts, nothing added),
adds hreflang + a language link to both versions, and adds the /zh/ pages to sitemap.xml and llms.txt."""
import html as H
import json
import os
import re
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from zh_lib import SITE_DIR, LD_KEYS, ATTR_RE, META_RE, english_pages, split_parts, wanted  # noqa: E402
import build as B  # noqa: E402

SITE = B.SITE
T = json.load(open(os.path.join(B.HERE, 'zh', 'strings_zh.json')))
WA_ZH = '你好 New Zen Werkz，我在你们的网站上看到信息，想咨询我的车。'
ASSETS = r'(nzw\.css|nzw\.js|favicon\.svg|favicon\.ico|apple-touch-icon\.png|site\.webmanifest)'
missing = set()


def tr(s):
    k = H.unescape(s.strip())
    if k in T:
        return T[k]
    if wanted(k):
        missing.add(k)
    return k


def tr_text(t):
    if not wanted(t):
        return t
    lead = t[:len(t) - len(t.lstrip())]
    tail = t[len(t.rstrip()):]
    return lead + H.escape(tr(t), quote=False) + tail


def ld_zh(obj, in_business=False):
    if isinstance(obj, dict):
        biz = in_business or obj.get('@type') == 'AutoRepair'
        out = {}
        for k, v in obj.items():
            if k in LD_KEYS and isinstance(v, str) and wanted(v):
                out[k] = tr(v)
            elif k == 'knowsAbout' and isinstance(v, list):
                out[k] = [tr(x) for x in v]
            else:
                out[k] = ld_zh(v, biz)
        if 'inLanguage' in out:
            out['inLanguage'] = 'zh-Hans-SG'
        return out
    if isinstance(obj, list):
        return [ld_zh(x, in_business) for x in obj]
    if isinstance(obj, str) and not in_business and obj.startswith(SITE) and '#business' not in obj \
            and not re.search(r'\.(png|jpe?g|webp|svg|ico)$', obj) and not obj.startswith(SITE + 'zh/'):
        return SITE + 'zh/' + obj[len(SITE):]
    return obj


def alternates(path):
    return ('<link rel="alternate" hreflang="en-SG" href="%s%s">\n<link rel="alternate" hreflang="zh-Hans-SG" href="%szh/%s">\n'
            '<link rel="alternate" hreflang="x-default" href="%s%s">\n') % (SITE, path, SITE, path, SITE, path)


def pill(path, depth, zh):
    """Big EN | 中文 switch in the header (Edwin, 6 Nov 2026: make it more visible)."""
    if zh:
        en, cn = '../' * (depth + 1) + path, './'
    else:
        en, cn = './', '../' * depth + 'zh/' + path
    return ('<div class="langsw" role="group" aria-label="Language / 语言">'
            '<a href="%s" hreflang="en-SG" lang="en"%s>EN</a><a href="%s" hreflang="zh-Hans-SG" lang="zh-Hans"%s>中文</a></div>') % (
        en or './', '' if zh else ' aria-current="true"', cn, ' aria-current="true"' if zh else '')


def to_zh(h, path, depth):
    out = []
    for kind, t in split_parts(h):
        if kind == 'text':
            out.append(tr_text(t))
        elif t.startswith('<script type="application/ld+json">'):
            data = json.loads(t[len('<script type="application/ld+json">'):-9].replace('<\\/', '</'))
            out.append('<script type="application/ld+json">%s</script>' % json.dumps(ld_zh(data), ensure_ascii=False).replace('</', '<\\/'))
        elif t.startswith('<script') or t.startswith('<style'):
            out.append(t)
        else:
            t = ATTR_RE.sub(lambda m: '%s="%s"' % (m.group(1), H.escape(tr(m.group(2))) if wanted(m.group(2)) else m.group(2)), t)
            t = META_RE.sub(lambda m: m.group(1) + H.escape(tr(m.group(2))) + m.group(3), t)
            out.append(t)
    z = ''.join(out)
    z = z.replace('<html lang="en-SG">', '<html lang="zh-Hans-SG">').replace('content="en_SG"', 'content="zh_SG"')
    z = re.sub(r'(href|src)="((?:\.\./)*)' + ASSETS, r'\1="../\2\3', z)
    z = z.replace('href="%s%s"' % (SITE, path), 'href="%szh/%s"' % (SITE, path), 1)          # canonical
    z = z.replace('content="%s%s"' % (SITE, path), 'content="%szh/%s"' % (SITE, path))      # og:url
    z = z.replace('text=' + quote(B.WA_MSG), 'text=' + quote(WA_ZH))
    en_link = '<a class="lang" href="%s%s" hreflang="en-SG" lang="en">English</a> · ' % ('../' * (depth + 1), path)
    z = z.replace('<span class="strip-r">', '<span class="strip-r">' + en_link, 1)
    z = re.sub(r'<div class="langsw".*?</div>', lambda m: pill(path, depth, True), z, count=1, flags=re.S)
    return z


def main():
    pages = []
    for rel in english_pages():
        if rel == '404.html':
            continue
        path = rel[:-len('index.html')]
        depth = path.count('/')
        full = os.path.join(SITE_DIR, rel)
        h = open(full).read()
        # English side: hreflang + 中文 link (idempotent)
        if 'hreflang="zh-Hans-SG"' not in h:
            h = h.replace('<link rel="preconnect"', alternates(path) + '<link rel="preconnect"', 1)
            h = h.replace('<span class="strip-r">', '<span class="strip-r"><a class="lang" href="%szh/%s" hreflang="zh-Hans-SG" lang="zh-Hans">中文</a> · ' % ('../' * depth, path), 1)
        if 'class="langsw"' not in h:
            h = h.replace('<a class="btn btn-wa hdr-call"', pill(path, depth, False) + '<a class="btn btn-wa hdr-call"', 1)
            open(full, 'w').write(h)
        # Chinese side: the zh page links back to its English twin, so drop the 中文 link and add an English one
        src = h.replace('<a class="lang" href="%szh/%s" hreflang="zh-Hans-SG" lang="zh-Hans">中文</a> · ' % ('../' * depth, path), '')
        z = to_zh(src, path, depth)
        d = os.path.join(SITE_DIR, 'zh', path)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'index.html'), 'w').write(z)
        pages.append(path)
    # sitemap: add the zh URLs
    sm = open(os.path.join(SITE_DIR, 'sitemap.xml')).read()
    if SITE + 'zh/' not in sm:
        extra = ''.join('  <url><loc>%szh/%s</loc><lastmod>%s</lastmod></url>\n' % (SITE, p, B.UPDATED) for p in B.PAGES)
        open(os.path.join(SITE_DIR, 'sitemap.xml'), 'w').write(sm.replace('</urlset>', extra + '</urlset>'))
    ll = open(os.path.join(SITE_DIR, 'llms.txt')).read()
    if '## 中文' not in ll:
        ll += '\n## 中文 (Chinese version)\n' + ''.join('- [%s](%szh/%s)\n' % (tr(B.PAGES[p]['title']).split(' | ')[0], SITE, p) for p in B.PAGES)
        open(os.path.join(SITE_DIR, 'llms.txt'), 'w').write(ll)
    print('zh pages: %d, untranslated strings: %d' % (len(pages), len(missing)))
    for m in sorted(missing)[:20]:
        print('  MISSING:', m[:100])


if __name__ == '__main__':
    main()
