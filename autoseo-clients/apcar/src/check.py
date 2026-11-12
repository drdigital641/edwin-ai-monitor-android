"""Checks for AP Car article pages. build.py stops if any check fails."""
import html, json, os, re

# Words that must never appear on an AP Car page (Edwin's brief, 12 Nov 2026).
BLOCK = [r'dtc\s*off', r'\bclone', r'\bremap', r'\bRM\s?\d', r'\bRM\b', r'page\s*one', r'pageone', r'\bedwin\b',
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
