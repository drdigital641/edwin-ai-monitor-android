"""Checks for AP Car article pages. build.py stops if any check fails."""
import html, json, os, re

# Words that must never appear on an AP Car page (Edwin's brief, 12 Nov 2026).
BLOCK = [r'gt\s*-?\s*hybrid', r'\b4\.3\b', r'dtc\s*off', r'\bclone', r'\bremap', r'\bRM\s?\d', r'\bRM\b', r'page\s*one', r'pageone', r'\bedwin\b',
         r'sggarage', r'singapore', r'\bwarranty\b', r'years? in business', r'since (19|20)\d\d',
         r'\bauthori[sz]ed dealer', r'official (dealer|service centre|service center)', r'\bdealer\b', r'1 ?hour', r'guarantee',
         r'autoseo', r'k tech']
SVC_DIR = None


def strip_tags(s):
    s = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s)
    return html.unescape(s)


def kw_in(kw, text):
    """Keyword match, allowing the natural 'in' / 'di' before Kuantan (EN/BM)."""
    t = text.lower()
    k = kw.lower()
    if k in t:
        return True
    for joiner in (' in ', ' di '):
        if k.replace(' kuantan', joiner + 'kuantan') in t:
            return True
    return False


def run(root, out, C, S, arts):
    errs = []
    langs = ['en', 'ms', 'zh']
    allowed_photos = set(C['photos'])
    photos = json.load(open(os.path.join(root, 'data', 'photos.json'), encoding='utf-8'))
    for art in arts:
        for l in langs:
            if l not in art:
                errs.append(f'{art["slug"]}: missing {l} (every article needs EN, BM and 中文)')
                continue
            a = art[l]
            kw = a['keyword']
            for f in ('title', 'h1', 'lead'):
                if not kw_in(kw, a[f]):
                    errs.append(f'{art["slug"]} {l}: keyword "{kw}" not in {f}')
            if len(a['description']) > 160:
                errs.append(f'{art["slug"]} {l}: description over 160 chars')
        if art['service'] not in C['services']:
            errs.append(f'{art["slug"]}: unknown service {art["service"]}')
        used = {art['hero_photo']}
        for l in langs:
            for sec in art.get(l, {}).get('sections', []):
                used |= set(sec.get('pair', [])) | ({sec['photo']} if 'photo' in sec else set())
        for p in used:
            if p not in allowed_photos or p not in photos:
                errs.append(f'{art["slug"]}: photo {p} is not an approved preview photo with captions')

    for dp, _, fs in os.walk(out):
        for f in fs:
            if not f.endswith('.html'):
                continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, out)
            s = open(p, encoding='utf-8').read()
            lang = 'ms' if rel.startswith('ms/') else 'zh' if rel.startswith('zh/') else 'en'
            pre = S[lang]['prefix']
            if C['preview'] and '<meta name="robots" content="noindex,nofollow">' not in s:
                errs.append(f'{rel}: no noindex meta')
            if s.count('<h1') != 1:
                errs.append(f'{rel}: {s.count("<h1")} H1 tags')
            if re.search(r'\{\{[a-zA-Z_]', s):
                errs.append(f'{rel}: leftover template placeholder')
            for m in re.finditer(r'<a [^>]*href="(https://wa\.me/[^"]*|tel:[^"]*|mailto:[^"]*|https://www\.google\.com/maps[^"]*)"[^>]*>', s):
                tag = m.group(0)
                if 'data-cta=' not in tag and 'class="gauge"' not in tag:
                    errs.append(f'{rel}: contact link without data-cta: {tag[:90]}')
                if m.group(1).startswith('https://wa.me/') and C['whatsapp'] not in m.group(1):
                    errs.append(f'{rel}: wrong WhatsApp number')
            for m in re.finditer(r'href="https://wa\.me/[^"?]+\?text=([^"]+)"', s):
                pass
            if f'site.css?v={C["site_asset_v"]}' not in s or f'site.js?v={C["site_asset_v"]}' not in s:
                errs.append(f'{rel}: not using the live site.css / site.js version')
            for m in re.finditer(r'href="(/preview/apcar/[^"#]*)"', s):
                h = m.group(1)
                if '/articles/' in h:
                    continue
                if lang != 'en' and not h.startswith(f'/preview/apcar/{lang}/') and '/assets/' not in h \
                        and not re.match(r'/preview/apcar/(ms/|zh/)?[^"]*$', h):
                    errs.append(f'{rel}: link to another language {h}')
            text = strip_tags(s)
            for b in BLOCK:
                m = re.search(b, text, flags=re.I)
                if m:
                    errs.append(f'{rel}: blocked word "{m.group(0)}"')
            if '/articles/' in rel.replace('\\', '/') and rel.count('/') >= (3 if pre else 2):
                # an article page: must link to its service page in the same language
                slug = rel.split('articles/')[1].split('/')[0]
                art = next(x for x in arts if x['slug'] == slug)
                svc = f'href="/preview/apcar/{pre}{C["services"][art["service"]]}"'
                if svc not in s:
                    errs.append(f'{rel}: no link to its service page in the same language')
                for x in ['en', 'ms', 'zh']:
                    if f'hreflang="{S[x]["hreflang"]}" href="{C["site_url"]}{S[x]["prefix"]}articles/{slug}/"' not in s:
                        errs.append(f'{rel}: missing hreflang {x}')
                if lang != 'en':
                    body = strip_tags(s.split('<main', 1)[1].split('</main>')[0])
                    left = [w for w in re.findall(r'\b(the|and|with|your|what|when|switched)\b', body)]
                    if len(left) > 0:
                        errs.append(f'{rel}: English words left on {lang} page: {sorted(set(left))[:6]}')
                for t in ('"@type": "Article"', '"@type": "BreadcrumbList"', '"#business"'.replace('"#', '"https://autoseo.my/preview/apcar/#')):
                    if t not in s:
                        errs.append(f'{rel}: schema missing {t}')
    for f in ('sitemap.xml', 'llms.txt', 'robots.txt'):
        if os.path.exists(os.path.join(out, f)):
            errs.append(f'{f} must not be built: articles stay out of every sitemap until Edwin says AP Car is live')
    return errs


def check_md(md_root):
    """Checks the Markdown hand-off files (articles/<slug>/en.md, ms.md, zh.md) that build.py --live reads (13 Nov 2026)."""
    errs = []
    need = ('slug', 'lang', 'url', 'date_published', 'keyword', 'title', 'description', 'h1')
    for slug in sorted(os.listdir(md_root)):
        d = os.path.join(md_root, slug)
        if not os.path.isdir(d):
            continue
        for l in ('en', 'ms', 'zh'):
            p = os.path.join(d, f'{l}.md')
            if not os.path.exists(p):
                errs.append(f'{slug}: missing {l}.md')
                continue
            text = open(p, encoding='utf-8').read()
            if not text.startswith('---\n') or '\n---\n' not in text[4:]:
                errs.append(f'{slug}/{l}.md: no front matter')
                continue
            head, body = text[4:].split('\n---\n', 1)
            fm = {}
            for line in head.splitlines():
                k, _, v = line.partition(':')
                v = v.strip()
                fm[k.strip()] = json.loads(v) if v.startswith('"') else v
            for k in need:
                if not fm.get(k):
                    errs.append(f'{slug}/{l}.md: front matter missing {k}')
            if fm.get('slug') != slug:
                errs.append(f'{slug}/{l}.md: slug in front matter is {fm.get("slug")}')
            if len(fm.get('description', '')) > 160:
                errs.append(f'{slug}/{l}.md: description over 160 chars')
            h1s = [x for x in body.splitlines() if x.startswith('# ')]
            if len(h1s) != 1:
                errs.append(f'{slug}/{l}.md: {len(h1s)} H1 lines (need exactly 1)')
            paras = [x for x in body.split('\n\n') if x.strip() and not x.lstrip().startswith(('#', '>', '-', '!', '|'))]
            kw = fm.get('keyword', '')
            for name, val in (('title', fm.get('title', '')), ('h1', h1s[0][2:] if h1s else ''), ('first paragraph', paras[0] if paras else '')):
                if kw and not kw_in(kw, val):
                    errs.append(f'{slug}/{l}.md: keyword "{kw}" not in {name}')
            if not re.search(r'^## ', body, flags=re.M):
                errs.append(f'{slug}/{l}.md: no H2 sections')
            if re.search(r'^#### ', body, flags=re.M) and not re.search(r'^### ', body, flags=re.M):
                errs.append(f'{slug}/{l}.md: H4 without H3')
            for b in BLOCK:
                m = re.search(b, text, flags=re.I)
                if m:
                    errs.append(f'{slug}/{l}.md: blocked word "{m.group(0)}"')
    return errs


if __name__ == '__main__':
    # python3 src/check.py            -> article data (data/articles/*.json) + the Markdown in articles/
    # python3 src/check.py --md DIR   -> only the Markdown folder DIR (one sub-folder per slug)
    import sys
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    args = sys.argv[1:]
    errs = []
    if '--md' in args:
        errs += check_md(args[args.index('--md') + 1])
    else:
        C = json.load(open(os.path.join(root, 'config.json'), encoding='utf-8'))
        S = {l: json.load(open(os.path.join(root, 'strings', f'{l}.json'), encoding='utf-8')) for l in ('en', 'ms', 'zh')}
        adir = os.path.join(root, 'data', 'articles')
        arts = [json.load(open(os.path.join(adir, f), encoding='utf-8')) for f in sorted(os.listdir(adir)) if f.endswith('.json')]
        errs += run(root, os.path.join(root, '_no_html_build_'), C, S, arts)
        if os.path.isdir(os.path.join(root, 'articles')):
            errs += check_md(os.path.join(root, 'articles'))
    print('\n'.join(errs) if errs else 'OK: 0 problems')
    sys.exit(1 if errs else 0)
