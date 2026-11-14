#!/usr/bin/env python3
"""Shared head build step: add the WhatsApp/Facebook/X link-preview tags a page is missing.

Edwin's standing rule: every client page shows an image preview when its link is shared on WhatsApp.
Task "SITEMAP OVERRIDE AND INNER OG 1114-2210" (14 Nov 2026).

  python3 pageone-site/clients/og_inject.py SITE_DIR [--dims dims.tsv] [--write]

Without --write it only reports. For every .html file under SITE_DIR it ADDS, never changes, these tags
when they are missing from <head>:
  og:title, og:description, og:url, og:type, og:image, og:image:secure_url, og:image:width,
  og:image:height, twitter:card
Rules:
- og:title / og:description copy the page's own <title> / meta description exactly (already HTML-escaped there).
- og:url = the page's canonical, else the site address + the page path.
- og:image = the page's existing og:image; a page with none gets the homepage's og:image.
- og:image:secure_url = og:image (only when it is https).
- og:image:width / height = the real pixel size of that image file (repo copy, jsDelivr repo path, or a
  measured size from --dims). If the size cannot be measured the page is skipped and reported, never guessed.
- New tags go on new lines right after the last existing og:/twitter: tag (or after the meta description),
  in the page's own style. Nothing else in the file changes: title, description, H1, JSON-LD, FAQ, robots,
  review footer and body stay byte for byte.
"""
import os, re, subprocess, sys, html

NEED = ['og:title', 'og:description', 'og:url', 'og:type', 'og:image', 'og:image:secure_url',
        'og:image:width', 'og:image:height', 'twitter:card']
REPO = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True,
                      cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()


def tag_re(name):
    return re.compile(r'<meta\s+(?:property|name)=["\']' + re.escape(name) + r'["\'][^>]*>', re.I)


def content_of(head, name):
    m = tag_re(name).search(head)
    if not m:
        return None
    c = re.search(r'content=["\']([^"\']*)["\']', m.group(0))
    return c.group(1) if c else None


def img_size(data):
    from io import BytesIO
    from PIL import Image
    with Image.open(BytesIO(data)) as im:
        return im.size


def resolve_image(url, site_dir, site_origin, dims):
    """Return (w, h) for the image URL, or None if it cannot be measured."""
    if url in dims:
        return dims[url]
    raw = html.unescape(url)
    if site_origin and raw.startswith(site_origin + '/'):
        p = os.path.join(site_dir, raw[len(site_origin) + 1:].split('?')[0])
        if os.path.isfile(p):
            return img_size(open(p, 'rb').read())
        return None
    m = re.match(r'https://cdn\.jsdelivr\.net/gh/drdigital641/edwin-ai-monitor-android@([0-9a-f]{7,40})/(.+)$', raw)
    if m:
        r = subprocess.run(['git', 'show', m.group(1) + ':' + m.group(2).split('?')[0]], capture_output=True, cwd=REPO)
        if r.returncode == 0:
            return img_size(r.stdout)
    return None


def main():
    args = sys.argv[1:]
    write = '--write' in args
    dims = {}
    if '--dims' in args:
        for line in open(args[args.index('--dims') + 1], encoding='utf-8'):
            if line.strip() and not line.startswith('#'):
                u, w, h = line.rstrip('\n').split('\t')[:3]
                dims[u] = (int(w), int(h))
    site_dir = os.path.abspath(args[0])
    home = open(os.path.join(site_dir, 'index.html'), encoding='utf-8').read().split('</head>')[0]
    home_url = content_of(home, 'og:url') or ''
    origin = re.match(r'(https://[^/]+)', home_url).group(1)
    home_img = content_of(home, 'og:image')
    changed, skipped, complete = [], [], 0
    for root, _, files in os.walk(site_dir):
        for fn in sorted(files):
            if not fn.endswith('.html'):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, site_dir).replace(os.sep, '/')
            text = open(path, encoding='utf-8').read()
            hi = text.find('</head>')
            if hi < 0:
                skipped.append((rel, 'no </head>'))
                continue
            head = text[:hi]
            missing = [n for n in NEED if not tag_re(n).search(head)]
            if not missing:
                complete += 1
                continue
            if re.search(r'<meta\s+http-equiv=["\']refresh', head, re.I):
                skipped.append((rel, 'redirect stub (meta refresh), not a real page'))
                continue
            t = re.search(r'<title>(.*?)</title>', head, re.S)
            d = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']', head, re.I)
            canon = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)["\']', head, re.I)
            page_path = '/' + (rel[:-len('index.html')] if rel.endswith('index.html') else rel)
            vals = {}
            vals['og:title'] = t.group(1).strip() if t else None
            vals['og:description'] = d.group(1) if d else None
            vals['og:url'] = canon.group(1) if canon else origin + page_path
            vals['og:type'] = 'website'
            img = content_of(head, 'og:image') or home_img
            vals['og:image'] = img
            vals['og:image:secure_url'] = img if img and img.startswith('https://') else None
            size = resolve_image(img, site_dir, origin, dims) if img else None
            vals['og:image:width'] = str(size[0]) if size else None
            vals['og:image:height'] = str(size[1]) if size else None
            vals['twitter:card'] = 'summary_large_image'
            gaps = [n for n in missing if not vals.get(n)]
            if gaps:
                skipped.append((rel, 'cannot fill ' + ', '.join(gaps) + (' (image ' + img + ')' if img else '')))
                continue
            # where to insert: after the last og:/twitter: tag, else after the meta description, else after <title>
            anchors = [m.end() for n in NEED + ['og:site_name', 'og:locale', 'og:image:alt', 'og:image:type',
                       'twitter:title', 'twitter:description', 'twitter:image', 'twitter:image:alt']
                       for m in tag_re(n).finditer(head)]
            at = max(anchors) if anchors else (d.end() + head[d.end():].find('>') + 1 if d else t.end())
            if at > 0 and head[at - 1] != '>':
                at = head.index('>', at) + 1
            line_start = head.rfind('\n', 0, at) + 1
            indent = re.match(r'[ \t]*', head[line_start:]).group(0)
            attr = lambda n: 'name' if n.startswith('twitter:') else 'property'
            add = ''.join('\n' + indent + '<meta ' + attr(n) + '="' + n + '" content="' + vals[n] + '">' for n in missing)
            new = text[:at] + add + text[at:]
            changed.append((rel, missing))
            if write:
                open(path, 'w', encoding='utf-8').write(new)
    for rel, m in changed:
        print('ADD ', rel, ' '.join(m))
    for rel, why in skipped:
        print('SKIP', rel, why)
    print(f'{len(changed)} pages {"changed" if write else "to change"}, {len(skipped)} skipped, {complete} already complete')


if __name__ == '__main__':
    main()
