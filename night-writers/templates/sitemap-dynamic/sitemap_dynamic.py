#!/usr/bin/env python3
"""DYNAMIC SITEMAP TEMPLATE (Edwin, 23 Nov 2026 SGT, every live client site).

One shared step that rebuilds a live site's sitemap.xml from the pages that are really public on the server, so a
page can no longer go live without reaching the sitemap (the 22-23 Nov gaps: Danny ILP article, SofaCare dog-urine
article, Page One managed-website article, Danny trailing-slash locs).

For one site (a row of ../article-autoindex/sites.json) it:
  1. lists the site folder through the Bridge runner API (bridgeListLive, recursive, mtime per file);
  2. reads only pages that are new or whose mtime changed since the last run (cache in state/), at most
     MAX_READS per run (Bluehost load cut, 22 Nov), so a full first pass spreads over several runs;
  3. keeps a page only if it is indexable: no robots noindex, not a redirect stub (meta refresh / tiny "Moved" page),
     canonical on the site's own host. The <loc> is the page's CANONICAL, so /x/ vs /x never both appear and a
     URL that 301s is never listed (Danny fix);
  4. lastmod = the day the page's CONTENT last changed (hash of the visible body, scripts and ?v= cache-busters
     ignored), in SGT. A rebuild that rewrites identical pages does not move lastmod. First sight of a page:
     JSON-LD dateModified/datePublished if present, else the current sitemap's lastmod, else the file mtime;
  5. Rule 6 (22 Nov): a page at ms/<p> or zh/<p> gets xhtml:link hreflang alternates (en, ms, zh, x-default=en)
     ONLY when the counterpart page exists and is indexable. English-only sites get no hreflang;
  6. never drops a URL that is still live and indexable; a URL leaves only when its file is gone, noindex, a
     redirect, or canonical elsewhere. If more than DROP_GUARD of the current URLs would go, nothing is written
     and the run reports "drop_guard" (protects against a bad listing);
  7. keeps <image:image> blocks of URLs that stay (SofaCare), writes sitemap.xml ONLY (never sitemap.txt, Edwin
     16 Nov), and writes only when something changed (live edit rule: read, amend, write with expected_sha256);
  8. IndexNow: new URLs + URLs whose lastmod moved + the sitemap URL go into the SAME queue the article template
     uses (state/indexnow-queue.json); the existing daily IndexNow batch (resend_queue, 429 backoff, 7-day expiry)
     sends them. --ping-now sends at once through bridgeRunnerIndexNow and queues on 429.

Keys: the Bridge holds every IndexNow key and submits with the key file the host already publishes at its root
(bridgeRunnerIndexNow, own domain only, key never returned). This file never reads, prints or stores a key, and
nothing here goes into front-end JS. The runner key comes from BRIDGE_RUNNER_KEY.

Previews: rows whose status is not "active" are skipped, every noindex page is skipped (preview hosts send noindex),
and EXCLUDE_DIRS keeps preview/ and other client folders out of Page One's own root.

CLI (runner box):
    python3 sitemap_dynamic.py --site danny --dry-run     # report only, no write, no IndexNow
    python3 sitemap_dynamic.py --all                      # every active row; queue IndexNow for the daily batch
    python3 sitemap_dynamic.py --all --ping-now           # same, and send IndexNow now
Python 3.9+, standard library only.
"""
from __future__ import annotations

import dataclasses
import datetime as _dt
import hashlib
import json
import os
import re
import sys
from html import escape, unescape
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'article-autoindex'))
import article_autoindex as AI  # noqa: E402  (Bridge, Site, load_sites, enqueue, _ping, queue + log paths)

SGT = AI.SGT
STATE_DIR = os.environ.get('SITEMAP_STATE_DIR', AI.STATE_DIR)
MAX_READS = int(os.environ.get('SITEMAP_MAX_READS', '150'))
DROP_GUARD = 0.10
MAX_DEPTH = 4                     # bridgeListLive limit per call; deeper folders are listed again
LANGS = ('ms', 'zh')
EXCLUDE_DIRS = ('preview/', 'assets/', 'admin/', 'cgi-bin/', '.well-known/', 'wp-admin/', 'wp-includes/', 'wp-content/',
                'images/', 'media/', 'img/', 'fonts/', 'login/', 'register/', 'forgot-password/', 'reset-password/',
                'node_modules/', '_sync/', 'backups', 'dmts/')
EXCLUDE_FILES = ('404.html', 'google', 'yandex', 'BingSiteAuth')   # 404 + search-engine verification files
SITE_EXTRA_EXCLUDE = {}           # site key -> extra path prefixes, e.g. {'pageone': ('clients-admin/',)}


# ---------------------------------------------------------------- pure helpers (tested offline)

def sgt_date(iso: str) -> str:
    t = _dt.datetime.fromisoformat(iso.replace('Z', '+00:00'))
    return t.astimezone(SGT).date().isoformat()


def is_page(rel: str, site_key: str = '') -> bool:
    if not rel.endswith(('.html', '.htm')):
        return False
    if any(rel.startswith(d) or ('/' + d) in rel for d in EXCLUDE_DIRS + SITE_EXTRA_EXCLUDE.get(site_key, ())):
        return False
    name = rel.rsplit('/', 1)[-1]
    if name.startswith(EXCLUDE_FILES) or re.search(r'\.(bak|old|orig)\b|-bak-|\.bak-', rel):
        return False
    return True


def default_url(host: str, rel: str) -> str:
    return 'https://%s/%s' % (host, re.sub(r'(^|/)index\.html?$', r'\1', rel))


def robots_noindex(html: str) -> bool:
    for tag in re.findall(r'<meta\b[^>]*>', html[:20000], re.I):
        if re.search(r'name\s*=\s*["\']?(robots|googlebot)\b', tag, re.I) and re.search(r'noindex', tag, re.I):
            return True
    return False


def is_redirect_stub(html: str) -> bool:
    return bool(re.search(r'<meta\b[^>]*http-equiv\s*=\s*["\']?refresh', html[:5000], re.I)) or len(html) < 600


def doc_date(html: str) -> Optional[str]:
    for k in ('dateModified', 'datePublished'):
        m = re.search(r'"%s"\s*:\s*"(\d{4}-\d{2}-\d{2})' % k, html)
        if m:
            return m.group(1)
    m = re.search(r'<meta[^>]+property=["\']article:modified_time["\'][^>]+content=["\'](\d{4}-\d{2}-\d{2})', html, re.I)
    return m.group(1) if m else None


def content_hash(html: str) -> str:
    body = re.search(r'<body\b[\s\S]*</body>', html, re.I)
    s = body.group(0) if body else html
    s = re.sub(r'<script\b[\s\S]*?</script>', '', s, flags=re.I)
    s = re.sub(r'\?v=[\w.-]+', '', s)
    s = re.sub(r'\s+', ' ', s)
    return hashlib.sha256(s.encode('utf-8', 'ignore')).hexdigest()[:20]


def lang_of(rel: str) -> tuple[str, str]:
    """('ms', 'services/x/index.html') for 'ms/services/x/index.html'; ('en', rel) otherwise."""
    for l in LANGS:
        if rel.startswith(l + '/') or rel == l + '/index.html':
            return l, rel[len(l) + 1:]
    return 'en', rel


def parse_sitemap(xml: str) -> dict:
    """loc -> {'lastmod': str, 'extra': str (image:image blocks etc. kept verbatim)}"""
    out = {}
    for block in re.findall(r'<url\b[^>]*>[\s\S]*?</url>', xml):
        m = re.search(r'<loc>\s*([^<]*?)\s*</loc>', block)
        if not m:
            continue
        lm = re.search(r'<lastmod>\s*([^<]*?)\s*</lastmod>', block)
        extra = ''.join(re.findall(r'<image:image>[\s\S]*?</image:image>', block))
        out[unescape(m.group(1))] = {'lastmod': (lm.group(1)[:10] if lm else ''), 'extra': extra}
    return out


def render_sitemap(entries: list) -> str:
    """entries: [{'loc', 'lastmod', 'alternates': {lang: url}, 'extra'}] in a stable order."""
    has_img = any(e.get('extra') for e in entries)
    has_alt = any(e.get('alternates') for e in entries)
    ns = 'xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"'
    if has_img:
        ns += ' xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"'
    if has_alt:
        ns += ' xmlns:xhtml="http://www.w3.org/1999/xhtml"'
    rows = []
    for e in entries:
        alt = ''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (l, escape(u))
                      for l, u in sorted(e.get('alternates', {}).items()))
        if e.get('alternates'):
            alt += '<xhtml:link rel="alternate" hreflang="x-default" href="%s"/>' % escape(e['alternates']['en'])
        rows.append('<url><loc>%s</loc>%s%s%s</url>\n' % (escape(e['loc']), '<lastmod>%s</lastmod>' % e['lastmod'] if e.get('lastmod') else '',
                                                        alt, e.get('extra', '')))
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset %s>\n%s</urlset>\n' % (ns, ''.join(rows))


# ---------------------------------------------------------------- state

def _cache_path(site_key: str) -> str:
    return os.path.join(STATE_DIR, 'sitemap-cache-%s.json' % site_key)


def load_cache(site_key: str) -> dict:
    try:
        with open(_cache_path(site_key), encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'pages': {}}


def save_cache(site_key: str, cache: dict) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    tmp = _cache_path(site_key) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(cache, f, indent=0, sort_keys=True)
    os.replace(tmp, _cache_path(site_key))


# ---------------------------------------------------------------- Bridge side

def list_pages(bridge: AI.Bridge, site: AI.Site) -> dict:
    """rel path (inside site.base) -> mtime iso, for every candidate .html page."""
    base = site.base.rstrip('/')
    out, todo = {}, [base]
    while todo:
        folder = todo.pop()
        body = {'site': site.bridge_site, 'depth': MAX_DEPTH}
        if folder:
            body['path'] = folder
        d = bridge.call('bridgeListLive', body)
        start_depth = folder.count('/') + 1 if folder else 0
        for e in d.get('entries', []):
            p = e['path']
            rel = p[len(base) + 1:] if base else p
            if e.get('type') == 'folder':
                if p.count('/') + 1 - start_depth >= MAX_DEPTH and is_page(rel + '/index.html', site.key):
                    todo.append(p)
                continue
            if is_page(rel, site.key) and e.get('readable', True):
                out[rel] = e.get('mtime', '')
    return out


@dataclasses.dataclass
class Result:
    site: str
    status: str = 'ok'
    added: list = dataclasses.field(default_factory=list)
    dropped: list = dataclasses.field(default_factory=list)
    lastmod_moved: list = dataclasses.field(default_factory=list)
    reads: int = 0
    pending_reads: int = 0
    written: bool = False
    indexnow: dict = dataclasses.field(default_factory=dict)
    problems: list = dataclasses.field(default_factory=list)


def run_site(bridge: AI.Bridge, site: AI.Site, dry_run: bool = False, ping_now: bool = False,
             max_reads: int = MAX_READS, today: Optional[str] = None) -> Result:
    r = Result(site.key)
    if site.status != 'active':
        r.status = 'skipped:' + site.status
        return r
    today = today or AI.sgt_today()
    base = site.base.rstrip('/') + '/' if site.base else ''
    sm_path = base + 'sitemap.xml'
    old_xml, sha = bridge.read(site.bridge_site, sm_path)
    current = parse_sitemap(old_xml)
    files = list_pages(bridge, site)
    cache = load_cache(site.key)
    pages = cache['pages']

    # 1. read new / changed pages (capped)
    changed = [rel for rel, mt in sorted(files.items()) if pages.get(rel, {}).get('mtime') != mt]
    r.pending_reads = max(0, len(changed) - max_reads)
    for rel in changed[:max_reads]:
        html, _ = bridge.read(site.bridge_site, base + rel)
        r.reads += 1
        prev = pages.get(rel, {})
        canon = AI.canonical_of(html) or default_url(site.host, rel)
        own = re.match(r'https://(www\.)?' + re.escape(site.host.replace('www.', '')) + r'/', canon) is not None
        indexable = own and not robots_noindex(html) and not is_redirect_stub(html)
        h = content_hash(html)
        if prev.get('hash') == h and prev.get('lastmod'):
            lastmod = prev['lastmod']
        elif prev.get('hash'):
            lastmod = sgt_date(files[rel]) if files[rel] else today
        else:
            lastmod = doc_date(html) or current.get(canon, {}).get('lastmod') or (sgt_date(files[rel]) if files[rel] else today)
        pages[rel] = {'mtime': files[rel], 'hash': h, 'lastmod': lastmod, 'loc': canon, 'index': indexable}
    for rel in list(pages):
        if rel not in files:
            del pages[rel]                       # file gone from the server

    # 2. the new URL set: every known indexable page; pages not read yet keep their current sitemap entry
    by_loc, unread = {}, set(changed[max_reads:])
    for rel, p in pages.items():
        if rel in unread and rel not in cache.get('seen', {}):
            continue
        if p['index']:
            by_loc[p['loc']] = {'loc': p['loc'], 'lastmod': p['lastmod'], 'rel': rel}
    def _norm(u: str) -> str:
        return u.rstrip('/') if u.count('/') > 3 else u
    known_locs = {_norm(p['loc']) for p in pages.values()} | {_norm(default_url(site.host, rel)) for rel in pages}
    for loc, cur in current.items():             # never drop what we have not checked yet
        if loc not in by_loc and _norm(loc) not in known_locs:
            by_loc[loc] = {'loc': loc, 'lastmod': cur['lastmod'], 'rel': None}

    # 3. hreflang (Rule 6): only between pages that exist and are indexable
    rel_loc = {v['rel']: k for k, v in by_loc.items() if v['rel']}
    for loc, e in by_loc.items():
        if not e['rel']:
            continue
        lang, core = lang_of(e['rel'])
        group = {'en': rel_loc.get(core)}
        for l in LANGS:
            group[l] = rel_loc.get(l + '/' + core)
        group = {k: v for k, v in group.items() if v}
        if len(group) > 1 and 'en' in group:
            e['alternates'] = group
        e['extra'] = current.get(loc, {}).get('extra', '')

    # 4. diff + guards
    r.added = sorted(set(by_loc) - set(current))
    r.dropped = sorted(set(current) - set(by_loc))
    r.lastmod_moved = sorted(l for l in set(by_loc) & set(current) if by_loc[l]['lastmod'] and by_loc[l]['lastmod'] != current[l]['lastmod'])
    if current and len(r.dropped) > max(5, DROP_GUARD * len(current)):
        r.status = 'drop_guard'
        r.problems.append('%d of %d URLs would leave the sitemap; nothing written' % (len(r.dropped), len(current)))
        return r
    order = list(current) + [l for l in sorted(by_loc) if l not in current]
    new_xml = render_sitemap([by_loc[l] for l in order if l in by_loc])
    if parse_sitemap(new_xml) == parse_sitemap(old_xml) and 'xhtml:link' not in new_xml:
        save_cache(site.key, cache)
        r.status = 'unchanged'
        return r
    if dry_run:
        r.status = 'dry_run'
        return r

    # 5. write (live edit rule) and queue IndexNow
    try:
        bridge.write(site.bridge_site, sm_path, new_xml, sha)
        r.written = True
    except AI.BridgeError as e:
        r.status = 'write_refused'
        r.problems.append('sitemap write refused: HTTP %s %s' % (e.status, e.message[:120]) if hasattr(e, 'message') else str(e)[:160])
        return r
    save_cache(site.key, cache)
    urls = (r.added + r.lastmod_moved)[:99] + [site.sitemap_url]
    if ping_now:
        r.indexnow = AI._ping(bridge, site, urls, AI.QUEUE_PATH, AI.LOG_PATH)
    else:
        AI.enqueue(site, urls, 'pending-daily', AI.QUEUE_PATH)
        r.indexnow = {'status': 'queued_for_daily_batch', 'urls': len(urls)}
    AI.log({'event': 'sitemap_dynamic', 'site': site.key, 'added': r.added, 'dropped': r.dropped,
            'lastmod_moved': len(r.lastmod_moved), 'indexnow': r.indexnow.get('status')}, AI.LOG_PATH)
    return r


def main(argv: list) -> int:
    sites = AI.load_sites()
    keys = list(sites) if '--all' in argv else [argv[argv.index('--site') + 1]] if '--site' in argv else []
    if not keys:
        print(__doc__)
        return 0
    br = AI.Bridge()
    seen_hosts, out = set(), []
    for k in keys:
        s = sites[k]
        if (s.host, s.base) in seen_hosts:      # Hon Win rows share sgcarworkshop.sg's sitemap
            continue
        seen_hosts.add((s.host, s.base))
        try:
            res = run_site(br, s, dry_run='--dry-run' in argv, ping_now='--ping-now' in argv)
        except AI.BridgeError as e:
            res = Result(k, status='error', problems=[str(e)[:200]])
        out.append(dataclasses.asdict(res))
    print(json.dumps(out, indent=1))
    return 0 if all(o['status'] in ('ok', 'unchanged', 'dry_run') or o['status'].startswith('skipped') for o in out) else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
