#!/usr/bin/env python3
"""ARTICLE AUTO-INDEX: the shared publish-side step for EVERY roster site (Edwin, 21 Nov 2026).

One template, used by the Grok Bot box runner (jobs/midnight_article.py) for every article it publishes, on every
site in sites.json. It never writes article text. For each new article it:

  1. reads the site's article hub through the Bridge (live edit rule: read, amend, write with expected_sha256) and puts
     the new card FIRST (the card markup comes from the writer; first_card() returns the hub's current first card to copy);
  2. writes the article page and the hub in ONE Bridge write_many call. The Bridge auto-sitemap step then adds the
     article to that site's sitemap.xml with today's lastmod (SGT), bumps the hub's lastmod, adds llms.txt lines and
     sends IndexNow (sitemap.xml ONLY, never sitemap.txt: Edwin 16 Nov 2026);
  3. checks the write result: the article URL must be in autoSitemap.added/bumped. If not, it calls bridgeRunnerSitemap
     once. Page One's own root is excluded from the Bridge step by design, so for it the sitemap entry is added here;
  4. IndexNow: the article URL, the hub URL and the sitemap URL. If the Bridge ping did not include the sitemap URL
     (Bridge before checkpoint "article-autoindex"), the sitemap URL is sent with bridgeRunnerIndexNow. Bing, Yandex,
     Seznam and Naver read IndexNow; Google finds the page through the updated sitemap.xml. The deprecated Google
     sitemap ping is never used;
  5. HTTP 429 (or any IndexNow failure) = the URLs go into the queue file and are resent by resend_queue() at the start
     of the next --live or --resend-indexnow run (dropped after QUEUE_MAX_DAYS, logged as expired);
  6. reads sitemap.xml back and confirms the URL is there with a lastmod; appends one JSON line to the log.

Secrets: the Bridge runner key comes from the environment (BRIDGE_RUNNER_KEY) and is never printed, logged or
written to a file. IndexNow keys never leave the Bridge. Python 3.9+, standard library only.

Use (inside the runner, after the article page HTML is final):
    from article_autoindex import Bridge, load_sites, Page, publish, resend_queue
    br = Bridge()                                   # reads BRIDGE_RUNNER_KEY
    sites = load_sites()                            # sites.json next to this file
    resend_queue(br, sites)                         # first thing in every --live / --resend-indexnow run
    report = publish(br, sites['hon-win-motor'], [Page(path='articles/<slug>/index.html', html=page_html, card_html=card)])

CLI:
    python3 article_autoindex.py --resend-indexnow           # drain the 429 queue
    python3 article_autoindex.py --check-sites               # print every site's config (no network)
"""
from __future__ import annotations

import dataclasses
import datetime as _dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from html import unescape
from typing import Any, Callable, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
BRIDGE_URL = 'https://blue-bridge-pilot.base44.app/functions/'
STATE_DIR = os.environ.get('AUTOINDEX_STATE_DIR', os.path.join(HERE, 'state'))
QUEUE_PATH = os.path.join(STATE_DIR, 'indexnow-queue.json')
LOG_PATH = os.path.join(STATE_DIR, 'article-autoindex.log.jsonl')
QUEUE_MAX_DAYS = 7
SGT = _dt.timezone(_dt.timedelta(hours=8))


def sgt_today() -> str:
    return _dt.datetime.now(SGT).date().isoformat()


def now_iso() -> str:
    return _dt.datetime.now(SGT).isoformat(timespec='seconds')


# ---------------------------------------------------------------- Bridge client

class BridgeError(RuntimeError):
    def __init__(self, fn: str, status: int, message: str):
        super().__init__(f'{fn}: HTTP {status}: {message}')
        self.fn, self.status = fn, status


class Bridge:
    """POST https://blue-bridge-pilot.base44.app/functions/<fn> with X-Bridge-Key (never logged)."""

    def __init__(self, key: Optional[str] = None, base: str = BRIDGE_URL, timeout: int = 90,
                 transport: Optional[Callable[[str, dict], tuple]] = None):
        self._key = key if key is not None else os.environ.get('BRIDGE_RUNNER_KEY', '')
        self.base, self.timeout, self._transport = base, timeout, transport
        if not self._key and transport is None:
            raise SystemExit('BRIDGE_RUNNER_KEY is not set')

    def call(self, fn: str, body: dict) -> dict:
        if self._transport:                      # tests: (fn, body) -> (status, json)
            status, data = self._transport(fn, body)
        else:
            req = urllib.request.Request(self.base + fn, data=json.dumps(body).encode(), method='POST',
                                         headers={'Content-Type': 'application/json', 'X-Bridge-Key': self._key})
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    status, data = r.status, json.loads(r.read().decode() or '{}')
            except urllib.error.HTTPError as e:
                try:
                    data = json.loads(e.read().decode() or '{}')
                except Exception:
                    data = {}
                status = e.code
        if status >= 400 or (isinstance(data, dict) and data.get('ok') is False):
            raise BridgeError(fn, status, str((data or {}).get('error', ''))[:300])
        return data.get('body', data) if isinstance(data, dict) else {}

    def read(self, site: str, path: str) -> tuple[str, str]:
        d = self.call('bridgeReadLive', {'site': site, 'path': path})
        return d['content'], d.get('sha256') or d.get('base_sha256')

    def write_many(self, site: str, base_path: str, files: list, dry_run: bool) -> dict:
        return self.call('bridgeWriteMany', {'site': site, 'base_path': base_path, 'files': files, 'dry_run': dry_run})

    def write(self, site: str, path: str, content: str, sha: str) -> dict:
        return self.call('bridgeWrite', {'site': site, 'path': path, 'content': content, 'expected_sha256': sha})

    def runner_sitemap(self, site: str, paths: list, dry_run: bool = False) -> dict:
        return self.call('bridgeRunnerSitemap', {'site': site, 'paths': paths, 'dry_run': dry_run})

    def indexnow(self, site: str, urls: list) -> dict:
        return self.call('bridgeRunnerIndexNow', {'site': site, 'urls': urls})


# ---------------------------------------------------------------- site config

@dataclasses.dataclass
class Site:
    key: str
    host: str                 # host exactly as the live sitemap uses it (www or not)
    bridge_site: str          # Bridge site key
    base: str                 # folder of the client docroot inside the Bridge site ('' = root)
    hub_path: str             # hub file, relative to base
    hub_url: str              # public hub URL
    card_link: str            # path fragment every article link on the hub contains (finds the card list)
    manual_sitemap: bool = False   # True only for Page One's own root (excluded from the Bridge auto step)
    articles_only: bool = False    # Cleanic / ContiExpert: only article pages + hub are ever written
    status: str = 'active'         # active | blocked:<reason> | hold
    note: str = ''

    @property
    def sitemap_url(self) -> str:
        return f'https://{self.host}/sitemap.xml'


def load_sites(path: Optional[str] = None) -> dict[str, Site]:
    with open(path or os.path.join(HERE, 'sites.json'), encoding='utf-8') as f:
        raw = json.load(f)
    fields = {f.name for f in dataclasses.fields(Site)}
    return {k: Site(key=k, **{a: b for a, b in v.items() if a in fields}) for k, v in raw['sites'].items()}


@dataclasses.dataclass
class Page:
    path: str                       # article file relative to the site base, e.g. articles/<slug>/index.html
    html: str
    card_html: Optional[str] = None  # card for the hub; None = the hub is not touched for this page (e.g. ms/zh copies)
    hub_path: Optional[str] = None   # default: the site's hub_path (AutoSEO ms/zh pages pass their own hub)


# ---------------------------------------------------------------- pure helpers

def canonical_of(html: str) -> Optional[str]:
    for tag in re.findall(r'<link\b[^>]*>', html, re.I):
        if re.search(r'\brel\s*=\s*["\']?canonical', tag, re.I):
            m = re.search(r'\bhref\s*=\s*"([^"]*)"|\bhref\s*=\s*\'([^\']*)\'', tag, re.I)
            if m:
                return unescape((m.group(1) or m.group(2) or '').strip())
    return None


def page_url(site: Site, page: Page) -> str:
    c = canonical_of(page.html)
    if c and re.match(r'https://(www\.)?' + re.escape(site.host.replace('www.', '')) + r'/', c):
        return c
    rel = re.sub(r'(^|/)index\.html?$', r'\1', page.path)
    return f'https://{site.host}/{rel}'


_CARD_TAGS = ('li', 'article', 'div')


def _block_end(html: str, start: int, tag: str) -> int:
    """Index just after the element that opens at `start` (balanced <tag>...</tag>), or -1."""
    depth, pos = 0, start
    pat = re.compile(r'<(/?)' + tag + r'\b[^>]*>', re.I)
    for m in pat.finditer(html, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return m.end()
        pos = m.end()
    return -1


def first_card(hub_html: str, card_link: str) -> Optional[tuple[int, int]]:
    """(start, end) of the hub's first article card: the innermost li/article/div[card] around the first link whose
    href contains card_link + something (a link to the hub itself does not count)."""
    for a in re.finditer(r'<a\b[^>]*\bhref\s*=\s*"([^"]+)"', hub_html, re.I):
        href = a.group(1)
        i = href.find(card_link)
        if i < 0 or not href[i + len(card_link):].strip('/').strip() or href[i + len(card_link):] in ('index.html',):
            continue
        best = None
        for tag in _CARD_TAGS:
            extra = r'[^>]*\bclass\s*=\s*"[^"]*(card|post|article|item)[^"]*"' if tag == 'div' else ''
            for o in re.finditer(r'<' + tag + r'\b' + extra + r'[^>]*>', hub_html[:a.start()], re.I):
                end = _block_end(hub_html, o.start(), tag)
                if end > a.start() and (best is None or o.start() > best[0]):
                    best = (o.start(), end)
        if best:
            return best
    return None


def _bump_itemlist(hub_html: str, url: str, name: str) -> str:
    """Prepend the article to a JSON-LD ItemList on the hub, if the hub has one (Page One's /articles/)."""
    def fix(m: re.Match) -> str:
        try:
            data = json.loads(m.group(2))
        except Exception:
            return m.group(0)
        nodes = data if isinstance(data, list) else data.get('@graph', [data]) if isinstance(data, dict) else []
        changed = False
        for n in nodes:
            if isinstance(n, dict) and n.get('@type') == 'ItemList' and isinstance(n.get('itemListElement'), list):
                items = n['itemListElement']
                if any(isinstance(x, dict) and (x.get('url') == url or x.get('item') == url) for x in items):
                    continue
                items.insert(0, {'@type': 'ListItem', 'position': 1, 'url': url, 'name': name})
                for i, x in enumerate(items, 1):
                    if isinstance(x, dict):
                        x['position'] = i
                n['numberOfItems'] = len(items) if 'numberOfItems' in n else n.get('numberOfItems', len(items))
                changed = True
        return m.group(1) + json.dumps(data, ensure_ascii=False) + m.group(3) if changed else m.group(0)
    return re.sub(r'(<script\b[^>]*application/ld\+json[^>]*>)([\s\S]*?)(</script>)', fix, hub_html, flags=re.I)


def title_of(html: str) -> str:
    m = re.search(r'<h1\b[^>]*>([\s\S]*?)</h1>', html, re.I) or re.search(r'<title>([\s\S]*?)</title>', html, re.I)
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', m.group(1)))).strip() if m else ''


def insert_hub_card(hub_html: str, card_html: str, article_url: str, card_link: str, title: str = '') -> tuple[str, str]:
    """New card FIRST in the hub's card list. Returns (html, status): inserted | already_listed | no_card_list."""
    path = re.sub(r'^https://[^/]+', '', article_url)
    slug = path.rstrip('/').split('/')[-1]
    for href in re.findall(r'\bhref\s*=\s*"([^"]+)"', hub_html, re.I):
        h = href.split('#')[0].split('?')[0].rstrip('/')
        if h and (h.endswith('/' + slug) or h == slug or h.endswith(path.rstrip('/'))):
            return hub_html, 'already_listed'
    at = first_card(hub_html, card_link)
    if not at:
        # 22 Nov 2026 (Edwin, "Fix AutoSEO article runner gaps"): an AutoSEO hub starts as an EMPTY list
        # (<div class="art-list" id="articles"></div>), so the first article had no card to copy and the hub kept
        # saying "will appear here". Put the first card inside that empty list instead of giving up.
        m = re.search(r'<(div|ul|ol|section)\b[^>]*\b(?:id\s*=\s*"articles"|class\s*=\s*"[^"]*\b(?:art-list|article-list|articles-list|post-list)\b[^"]*")[^>]*>', hub_html, re.I)
        if not m:
            return hub_html, 'no_card_list'
        out = hub_html[:m.end()] + '\n' + card_html.strip() + '\n' + hub_html[m.end():]
        return _bump_itemlist(out, article_url, title), 'inserted_first'
    start = at[0]
    line_start = hub_html.rfind('\n', 0, start) + 1
    indent = hub_html[line_start:start] if hub_html[line_start:start].strip() == '' else ''
    sep = ('\n' + indent) if indent else ''
    out = hub_html[:start] + card_html.strip() + sep + hub_html[start:]
    return _bump_itemlist(out, article_url, title), 'inserted'


def sitemap_lastmod(xml: str, url: str) -> Optional[str]:
    for block in re.findall(r'<url\b[^>]*>[\s\S]*?</url>', xml):
        m = re.search(r'<loc>\s*([^<]*?)\s*</loc>', block)
        if m and unescape(m.group(1)) == url:
            lm = re.search(r'<lastmod>\s*([^<]*?)\s*</lastmod>', block)
            return lm.group(1)[:10] if lm else ''
    return None


def sitemap_add(xml: str, url: str, date: str, bump: tuple = ()) -> str:
    """Page One root only: append <url> before </urlset> (never drops or reorders), bump lastmod of `bump` URLs."""
    if sitemap_lastmod(xml, url) is None:
        i = xml.rfind('</urlset>')
        if i < 0:
            raise ValueError('sitemap.xml has no </urlset>')
        xml = xml[:i] + f'  <url><loc>{url}</loc><lastmod>{date}</lastmod><priority>0.6</priority></url>\n' + xml[i:]
    for b in bump:
        xml = re.sub(r'(<loc>\s*' + re.escape(b) + r'\s*</loc>\s*<lastmod>)[^<]*(</lastmod>)', r'\g<1>' + date + r'\g<2>', xml)
    return xml


# ---------------------------------------------------------------- queue + log

def _load_queue(path: str) -> dict:
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'items': []}


def _save_queue(path: str, q: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(q, f, indent=1)
    os.replace(tmp, path)


def enqueue(site: Site, urls: list, http: Any, path: str = QUEUE_PATH) -> None:
    q = _load_queue(path)
    for it in q['items']:
        if it['site'] == site.key:
            it['urls'] = list(dict.fromkeys(it['urls'] + urls))
            it['last_http'] = http
            break
    else:
        q['items'].append({'site': site.key, 'bridge_site': site.bridge_site, 'urls': list(dict.fromkeys(urls)),
                           'first_queued': now_iso(), 'attempts': 0, 'last_http': http})
    _save_queue(path, q)


def log(entry: dict, path: str = LOG_PATH) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'at': now_iso(), **entry}, ensure_ascii=False) + '\n')


def _indexnow_results(obj: Any) -> list:
    if obj is None:
        return []
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict) and isinstance(obj.get('results'), list):
        return obj['results']
    return [obj] if isinstance(obj, dict) else []


def _ok(r: dict) -> bool:
    return r.get('status') == 'sent' or r.get('http') in (200, 202)


def resend_queue(bridge: Bridge, sites: dict[str, Site], path: str = QUEUE_PATH, log_path: str = LOG_PATH) -> dict:
    """Resend queued IndexNow URLs (429s and failures from earlier runs). Call at the start of every run."""
    q = _load_queue(path)
    keep, sent, expired = [], 0, 0
    for it in q['items']:
        first = _dt.datetime.fromisoformat(it['first_queued'])
        if _dt.datetime.now(SGT) - first > _dt.timedelta(days=QUEUE_MAX_DAYS):
            expired += 1
            log({'event': 'indexnow_expired', 'site': it['site'], 'urls': it['urls'], 'attempts': it['attempts']}, log_path)
            continue
        it['attempts'] += 1
        try:
            res = _indexnow_results(bridge.indexnow(it['bridge_site'], it['urls']))
            if res and all(_ok(r) for r in res):
                sent += 1
                log({'event': 'indexnow_resent', 'site': it['site'], 'urls': it['urls'], 'http': [r.get('http') for r in res]}, log_path)
                continue
            it['last_http'] = [r.get('http') for r in res]
        except BridgeError as e:
            it['last_http'] = e.status
        keep.append(it)
        log({'event': 'indexnow_still_queued', 'site': it['site'], 'urls': it['urls'], 'http': it['last_http']}, log_path)
    _save_queue(path, {'items': keep})
    return {'sent': sent, 'still_queued': len(keep), 'expired': expired}


# ---------------------------------------------------------------- the publish step

def _exists(bridge: 'Bridge', site: 'Site', rel: str) -> bool:
    try:
        bridge.read(site.bridge_site, site.base + rel)
        return True
    except Exception:
        return False


def drop_missing_lang_links(html: str, path: str, missing: list) -> str:
    """English article whose ms/zh copy does not exist: drop that hreflang alternate and point the language switch
    (every nav) at that language's article hub instead of a 404. path = 'articles/<slug>/index.html'."""
    art = re.sub(r'index\.html$', '', path)               # articles/<slug>/
    hub = art.split('/')[0] + '/'                          # articles/
    for lg in missing:
        codes = ('zh-Hans', 'zh-CN', 'zh') if lg == 'zh' else (lg,)
        for c in codes:
            html = re.sub(r'[ \t]*<link\b[^>]*rel="alternate"[^>]*hreflang="' + re.escape(c) + r'"[^>]*>\n?', '', html)
        html = re.sub(r'(href="[^"]*?)' + lg + '/' + re.escape(art) + '"', r'\1' + lg + '/' + hub + '"', html)
    return html


def publish(bridge: Bridge, site: Site, pages: list[Page], dry_run: bool = False, date: Optional[str] = None,
            queue_path: str = QUEUE_PATH, log_path: str = LOG_PATH) -> dict:
    """Write the article page(s) + hub card(s) and register them in sitemap.xml + IndexNow. Returns a report dict;
    report['ok'] is True only when every step checked out (or, in a dry run, would)."""
    if site.status != 'active':
        rep = {'ok': False, 'site': site.key, 'skipped': site.status}
        log({'event': 'skipped', **rep}, log_path)
        return rep
    date = date or sgt_today()
    rep: dict = {'site': site.key, 'dry_run': dry_run, 'date': date, 'pages': [], 'hubs': {}, 'problems': []}
    files, page_urls, hub_files = [], [], {}
    batch = {p.path for p in pages}
    for p in pages:
        # 22 Nov 2026: an English-only article must not link BM / 中文 copies that do not exist (they 404).
        if not re.match(r'(ms|zh)/', p.path):
            missing = [lg for lg in ('ms', 'zh') if lg + '/' + p.path not in batch and not _exists(bridge, site, lg + '/' + p.path)]
            if missing:
                p.html = drop_missing_lang_links(p.html, p.path, missing)
                rep.setdefault('lang_links', {})[p.path] = 'pointed to the ' + '/'.join(missing) + ' hub'
        url = page_url(site, p)
        page_urls.append(url)
        rep['pages'].append(url)
        files.append({'path': p.path, 'content': p.html})
        if p.card_html:
            hp = p.hub_path or site.hub_path
            if hp not in hub_files:
                html, sha = bridge.read(site.bridge_site, (site.base + hp))
                hub_files[hp] = [html, sha]
            new, st = insert_hub_card(hub_files[hp][0], p.card_html, url, site.card_link, title_of(p.html))
            hub_files[hp][0] = new
            rep['hubs'][hp] = st
            if st == 'no_card_list':
                rep['problems'].append(f'hub {hp}: no article card list found, card not added')
    for hp, (html, sha) in hub_files.items():
        if rep['hubs'].get(hp) in ('inserted', 'inserted_first'):
            files.append({'path': hp, 'content': html, 'expected_sha256': sha})

    res = bridge.write_many(site.bridge_site, site.base.rstrip('/'), files, dry_run)
    auto = res.get('autoSitemap') or {}
    rep['write'] = {'ok': res.get('ok', True), 'totals': res.get('totals'), 'auto_status': auto.get('status')}
    listed = set(auto.get('added') or []) | set(auto.get('bumped') or [])
    hub_url = site.hub_url
    want_ping = page_urls + ([hub_url] if any(v in ('inserted', 'inserted_first') for v in rep['hubs'].values()) else [])

    # ---- sitemap.xml
    if site.manual_sitemap:                       # Page One root: the Bridge step skips it by design
        xml, sha = bridge.read(site.bridge_site, site.base + 'sitemap.xml')
        new = sitemap_add(xml, page_urls[0], date, bump=(hub_url,))
        for u in page_urls[1:]:
            new = sitemap_add(new, u, date)
        rep['sitemap'] = 'would add' if dry_run else ('unchanged' if new == xml else 'written')
        if not dry_run and new != xml:
            bridge.write(site.bridge_site, site.base + 'sitemap.xml', new, sha)
        auto = {}                                 # IndexNow is sent below
    else:
        missing = [u for u in page_urls if u not in listed]
        if missing and not dry_run:
            rs = bridge.runner_sitemap(site.bridge_site, [site.base + p.path for p in pages])
            auto2 = rs.get('autoSitemap') or {}
            listed |= set(auto2.get('added') or []) | set(auto2.get('bumped') or [])
            auto = auto2 if auto2.get('indexnow') else auto
            rep['sitemap_resend'] = auto2.get('status')
        rep['sitemap'] = 'listed' if all(u in listed for u in page_urls) else 'MISSING'
        if rep['sitemap'] == 'MISSING':
            rep['problems'].append('sitemap.xml: not listed by the Bridge step: ' + ', '.join(u for u in page_urls if u not in listed))

    # ---- IndexNow (article + hub + sitemap)
    results = _indexnow_results(auto.get('indexnow'))
    sent_count = sum(int(r.get('urls') or 0) if isinstance(r.get('urls'), int) else len(r.get('urls') or []) for r in results)
    planned = [u for r in results for u in (r.get('urls') if isinstance(r.get('urls'), list) else [])]
    if dry_run:
        rep['indexnow'] = {'bridge_plan': planned or [r.get('status') for r in results],
                           'extra': [] if site.sitemap_url in planned else [site.sitemap_url] if not site.manual_sitemap else want_ping + [site.sitemap_url]}
    elif site.manual_sitemap or not results:
        urls = want_ping + [site.sitemap_url]
        rep['indexnow'] = _ping(bridge, site, urls, queue_path, log_path)
    else:
        bad = [r for r in results if not _ok(r)]
        if bad:
            urls = want_ping + [site.sitemap_url]
            http = [r.get('http') for r in bad]
            enqueue(site, urls, http, queue_path)
            rep['indexnow'] = {'status': 'queued', 'http': http, 'urls': urls}
        else:
            rep['indexnow'] = {'status': 'sent', 'http': [r.get('http') for r in results], 'urls': sent_count}
            if sent_count <= len(want_ping):      # the Bridge pinged only the pages (Bridge before the sitemap-URL fix)
                rep['indexnow_sitemap'] = _ping(bridge, site, [site.sitemap_url], queue_path, log_path)

    # ---- live check: sitemap.xml has every page with a lastmod
    if not dry_run:
        xml, _ = bridge.read(site.bridge_site, site.base + 'sitemap.xml')
        rep['sitemap_check'] = {u: sitemap_lastmod(xml, u) for u in page_urls}
        for u, lm in rep['sitemap_check'].items():
            if not lm:
                rep['problems'].append('sitemap.xml check: ' + u + (' has no lastmod' if lm == '' else ' not found'))
    rep['ok'] = not rep['problems']
    log({'event': 'dry_run' if dry_run else 'published', **rep}, log_path)
    return rep


def _ping(bridge: Bridge, site: Site, urls: list, queue_path: str, log_path: str) -> dict:
    try:
        res = _indexnow_results(bridge.indexnow(site.bridge_site, urls))
        bad = [r for r in res if not _ok(r)]
        if not res or bad:
            http = [r.get('http') for r in bad] or ['none']
            enqueue(site, urls, http, queue_path)
            return {'status': 'queued', 'http': http, 'urls': urls}
        return {'status': 'sent', 'http': [r.get('http') for r in res], 'urls': urls}
    except BridgeError as e:
        enqueue(site, urls, e.status, queue_path)
        return {'status': 'queued', 'http': e.status, 'urls': urls}


# ---------------------------------------------------------------- CLI

def main(argv: list) -> int:
    if '--check-sites' in argv:
        for k, s in load_sites().items():
            print(f'{k:24} {s.status:10} {s.bridge_site:11} {s.base or "/":38} hub={s.hub_path:28} {s.host}')
        return 0
    if '--resend-indexnow' in argv:
        print(json.dumps(resend_queue(Bridge(), load_sites())))
        return 0
    print(__doc__)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
