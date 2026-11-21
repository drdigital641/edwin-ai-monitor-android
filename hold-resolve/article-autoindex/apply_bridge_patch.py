# Apply the 21 Nov 2026 "article-autoindex" Bridge change to a CLEAN copy of the Bluehost Bridge repo (git a5af44b).
# Usage: python3 apply_bridge_patch.py <bridge repo root>   then: deno test --no-check -A --import-map tests/importmap.json tests/ base44/tests/
# Reviewed result: 152 passed / 0 failed (baseline a5af44b: 148 / 0). Nothing here is saved to Base44 until SPO review.
import re,sys
root=sys.argv[1]
def sub(path, old, new, count=1):
    p=root+'/'+path; s=open(p).read()
    if s.count(old)!=count: sys.exit('MISS %s: %r (found %d)'%(path,old[:80],s.count(old)))
    open(p,'w').write(s.replace(old,new))
# ---- liveGuard.ts
sub('base44/shared/liveGuard.ts', """export function autoSitemapPathOk(site: string, rel: string): boolean {
  if (site === 'pageone') {
    const m = /^preview\\/([a-z0-9-]+)\\/(sitemap\\.xml|llms\\.txt)$/.exec(rel);
    return !!m && Object.prototype.hasOwnProperty.call(AUTO_SITEMAP_CLIENT_FOLDERS, m[1]);
  }
  return AUTO_SITEMAP_ROOT_PATH.test(rel);
}""", """// LIVE CLIENT DOMAINS IN A FOLDER OF ANOTHER BRIDGE SITE (21 Nov 2026, thread "Automate article sitemap and indexing").
// An AutoSEO client that goes live with the one-switch golive template keeps its files in autoseo.my preview/<folder>/ and the
// root .htaccess host rules serve that folder as the client domain's document root. Those folders get the same auto-sitemap
// and IndexNow treatment as the Page One client folders above. Add one line on the day such a client goes live
// (autoseo-template/golive README); a folder that is not listed stays a hidden preview (never written, never pinged).
export const AUTO_SITEMAP_SITE_FOLDERS: Readonly<Record<string, Readonly<Record<string, string>>>> = Object.freeze({
  autoseo: Object.freeze({ 'hx-auto': 'hxautoservice.com.my' }),
});
const ownKey = (o: Readonly<Record<string, string>> | undefined, k: string) => !!o && Object.prototype.hasOwnProperty.call(o, k);
export function autoSitemapPathOk(site: string, rel: string): boolean {
  const m = /^preview\\/([a-z0-9-]+)\\/(sitemap\\.xml|llms\\.txt)$/.exec(rel);
  if (site === 'pageone') return !!m && ownKey(AUTO_SITEMAP_CLIENT_FOLDERS, m[1]);
  if (m) return ownKey(AUTO_SITEMAP_SITE_FOLDERS[site], m[1]);
  return AUTO_SITEMAP_ROOT_PATH.test(rel);
}""")
# ---- autoSitemapRun.ts
f='base44/shared/autoSitemapRun.ts'
sub(f,"import { AUTO_SITEMAP_CLIENT_FOLDERS } from './liveGuard.ts';","import { AUTO_SITEMAP_CLIENT_FOLDERS, AUTO_SITEMAP_SITE_FOLDERS } from './liveGuard.ts';")
sub(f,"""  if (AUTO_SITEMAP_EXCLUDE.includes(site)) return null;
  return { prefix: '', domain: SITES[site as keyof typeof SITES].domain };
}""","""  // A live client domain served from a folder of this site (AUTO_SITEMAP_SITE_FOLDERS, e.g. autoseo preview/hx-auto/).
  const folders = AUTO_SITEMAP_SITE_FOLDERS[site];
  const f = /^preview\\/([a-z0-9-]+)\\//.exec(path);
  if (f && folders && Object.prototype.hasOwnProperty.call(folders, f[1])) {
    const prefix = 'preview/' + f[1] + '/';
    return AUTO_SITEMAP_EXCLUDE.includes(site + ':' + prefix) ? null : { prefix, domain: folders[f[1]] };
  }
  if (AUTO_SITEMAP_EXCLUDE.includes(site)) return null;
  return { prefix: '', domain: SITES[site as keyof typeof SITES].domain };
}""")
sub(f,"""    return { status: res.status === 200 || res.status === 202 ? 'sent' : 'error', http: res.status, urls: urlList.length };""",
"""    // 429 = IndexNow rate limit: nothing is lost, the caller queues these URLs and resends them on its next run.
    return { status: res.status === 200 || res.status === 202 ? 'sent' : 'error', http: res.status, urls: urlList.length,
      ...(res.status === 429 ? { retry_later: true, urlList } : {}) };""")
sub(f,"""  else if (!nowUrls.length) g.indexnow = { status: 'skipped', reason: 'no URL on the site host' };
  else g.indexnow = await sendIndexNow(host, key, nowUrls);""","""  else if (!nowUrls.length) g.indexnow = { status: 'skipped', reason: 'no URL on the site host' };
  else {
    // The sitemap URL goes with the pages whenever sitemap.xml was just updated (Edwin 21 Nov 2026: ping the new article
    // plus the sitemap). Google reads the sitemap itself; the deprecated Google sitemap ping is never used.
    if (g.files['sitemap.xml'] === 'written') nowUrls.push('https://' + host + '/sitemap.xml');
    g.indexnow = await sendIndexNow(host, key, nowUrls);
  }""")
sub(f,"""    g.indexnow = key ? { status: 'would send', urls: nowUrls.slice(0, INDEXNOW_MAX_URLS) } : { status: 'skipped', reason: 'no IndexNow key file in the site folder' };""",
"""    const withMap = todo.some((t) => t.rel === 'sitemap.xml') ? [...nowUrls, 'https://' + host + '/sitemap.xml'] : nowUrls;
    g.indexnow = key ? { status: 'would send', urls: withMap.slice(0, INDEXNOW_MAX_URLS) } : { status: 'skipped', reason: 'no IndexNow key file in the site folder' };""")
# ---- runner.ts
f='base44/shared/runner.ts'
sub(f,"""  if (site !== 'pageone') return [{ prefix: '', domain: SITES[site as keyof typeof SITES].domain }];""",
"""  if (site !== 'pageone') return [{ prefix: '', domain: SITES[site as keyof typeof SITES].domain },
    ...Object.entries(AUTO_SITEMAP_SITE_FOLDERS[site] || {}).map(([f, d]) => ({ prefix: 'preview/' + f + '/', domain: d }))];""")
print('patched')
sub('base44/shared/runner.ts',"import { AUTO_SITEMAP_CLIENT_FOLDERS } from './liveGuard.ts';","import { AUTO_SITEMAP_CLIENT_FOLDERS, AUTO_SITEMAP_SITE_FOLDERS } from './liveGuard.ts';")
t='base44/tests/autoSitemap.test.ts'
sub(t,"const HOME = '/home3/sgmodde1', ROOT = HOME + '/public_html', CLEANIC = ROOT + '/cleanic', PAGEONE = ROOT + '/pageone';",
"const HOME = '/home3/sgmodde1', ROOT = HOME + '/public_html', CLEANIC = ROOT + '/cleanic', PAGEONE = ROOT + '/pageone', AUTOSEO = ROOT + '/autoseo';")
sub(t,"PAGEONE + '/preview', PAGEONE + '/preview/star-performance', ","PAGEONE + '/preview', PAGEONE + '/preview/star-performance', AUTOSEO, AUTOSEO + '/preview', AUTOSEO + '/preview/hx-auto', AUTOSEO + '/preview/carku', ")
sub(t,"{ domain: 'sofacaresg.com', documentroot: CLEANIC }]","{ domain: 'sofacaresg.com', documentroot: CLEANIC }, { domain: 'autoseo.my', documentroot: AUTOSEO }]")
s=open(root+'/'+t).read()
s+=r'''
// ---------------- 21 Nov 2026: AutoSEO client domains in autoseo.my preview/<folder>/, sitemap URL in IndexNow, 429 ----------------

import { AUTO_SITEMAP_SITE_FOLDERS } from '../shared/liveGuard.ts';
import { indexNowGroups } from '../shared/runner.ts';
const HX = 'https://hxautoservice.com.my', HXP = AUTOSEO + '/preview/hx-auto/';
const hxFiles = () => {
  resetCleanic();
  for (const k of [...files.keys()]) if (k.startsWith(AUTOSEO + '/')) files.delete(k);
  setFile(AUTOSEO + '/sitemap.xml', SM(['https://autoseo.my/'])); setFile(AUTOSEO + '/llms.txt', '# AutoSEO\n');
  setFile(HXP + 'sitemap.xml', SM([HX + '/', HX + '/articles/'])); setFile(HXP + 'llms.txt', '# HX Auto\n\n## Articles\n');
  setFile(HXP + KEY + '.txt', KEY);
  setFile(AUTOSEO + '/preview/carku/sitemap.xml', SM(['https://autoseo.my/preview/carku/']));
  return { path: 'preview/hx-auto/articles/brake-check-johor/index.html', bytes: enc(PAGE('Brake check', `<link rel="canonical" href="${HX}/articles/brake-check-johor/">`)) };
};

Deno.test('autoseo client folders: hx-auto maps to hxautoservice.com.my; other previews and the autoseo root are unchanged', async () => {
  const { autoSitemapPathOk } = await import('../shared/liveGuard.ts');
  eq(AUTO_SITEMAP_SITE_FOLDERS.autoseo['hx-auto'], 'hxautoservice.com.my', 'map');
  eq(subsiteFor('autoseo', 'preview/hx-auto/articles/x/index.html'), { prefix: 'preview/hx-auto/', domain: 'hxautoservice.com.my' }, 'hx folder');
  eq(subsiteFor('autoseo', 'articles/x/index.html'), { prefix: '', domain: 'autoseo.my' }, 'autoseo root as before');
  eq(subsiteFor('autoseo', 'preview/carku/index.html')?.prefix, '', 'hidden preview: root group (indexable() then drops the preview/ page)');
  eq(subsiteFor('ktech', 'preview/hx-auto/index.html')?.domain, 'ktech.my', 'the map is per site');
  yes(autoSitemapPathOk('autoseo', 'preview/hx-auto/sitemap.xml') && autoSitemapPathOk('autoseo', 'preview/hx-auto/llms.txt'), 'hx files allowed');
  for (const rel of ['preview/carku/sitemap.xml', 'preview/hx-auto/sitemap.txt', 'preview/hx-auto/sub/sitemap.xml', 'preview/hx-auto/robots.txt'])
    yes(!autoSitemapPathOk('autoseo', rel), 'refused: ' + rel);
  yes(!autoSitemapPathOk('ktech', 'preview/hx-auto/sitemap.xml'), 'other site refused');
  yes(autoSitemapPathOk('autoseo', 'sitemap.xml'), 'root still allowed');
  eq(indexNowGroups('autoseo'), [{ prefix: '', domain: 'autoseo.my' }, { prefix: 'preview/hx-auto/', domain: 'hxautoservice.com.my' }], 'runner IndexNow groups');
  eq(indexNowGroups('ktech'), [{ prefix: '', domain: 'ktech.my' }], 'other sites unchanged');
});

Deno.test('hook: an HX Auto article updates the hx-auto sitemap.xml + llms.txt and pings IndexNow with the page AND the sitemap', async () => {
  const page = hxFiles();
  const dry: any = await autoSitemapAfter({ site: 'autoseo', written: [page], dryRun: true });
  eq(dry.status, 'dry_run', JSON.stringify(dry)); eq(dry.groups[0].indexnow, { status: 'would send', urls: [HX + '/articles/brake-check-johor/', HX + '/sitemap.xml'] }, 'dry run plan');
  eq(posts.length, 0, 'dry run sent nothing');
  const r: any = await autoSitemapAfter({ site: 'autoseo', written: [page] });
  eq(r.status, 'ok', JSON.stringify(r)); eq(r.added, [HX + '/articles/brake-check-johor/'], 'added');
  eq(r.groups[0].files, { 'sitemap.xml': 'written', 'llms.txt': 'written' }, 'both written');
  yes(text(HXP + 'sitemap.xml').includes('<loc>' + HX + '/articles/brake-check-johor/</loc>\n    <lastmod>' + today + '</lastmod>'), 'lastmod');
  eq(text(AUTOSEO + '/sitemap.xml'), SM(['https://autoseo.my/']), 'autoseo.my root sitemap untouched');
  eq(posts.length, 1, 'one POST'); eq(posts[0].body.host, 'hxautoservice.com.my', 'host');
  eq(posts[0].body.urlList, [HX + '/articles/brake-check-johor/', HX + '/sitemap.xml'], 'page + sitemap');
  eq(posts[0].body.keyLocation, HX + '/' + KEY + '.txt', 'key on the client domain');
});

Deno.test('hook: a hidden autoseo preview page is never listed or pinged', async () => {
  hxFiles();
  const r: any = await autoSitemapAfter({ site: 'autoseo', written: [{ path: 'preview/carku/articles/x/index.html', bytes: enc(PAGE('X')) }] });
  yes(r.status !== 'ok' && r.added.length === 0, JSON.stringify(r)); eq(posts.length, 0, 'no ping');
  eq(text(AUTOSEO + '/preview/carku/sitemap.xml'), SM(['https://autoseo.my/preview/carku/']), 'untouched');
});

Deno.test('hook: IndexNow 429 is reported with retry_later and the URL list to queue; the write still succeeds', async () => {
  const page = hxFiles(); indexNowStatus = 429;
  const r: any = await autoSitemapAfter({ site: 'autoseo', written: [page] });
  eq(r.groups[0].files['sitemap.xml'], 'written', 'sitemap still written');
  eq(r.indexnow, { status: 'error', http: 429, urls: 2, retry_later: true, urlList: [HX + '/articles/brake-check-johor/', HX + '/sitemap.xml'] }, '429 result');
  indexNowStatus = 200;
});
'''
open(root+'/'+t,'w').write(s)
print('tests added')
# ---- 21 Nov fix-ups to the existing tests (sitemap URL now goes with the page in IndexNow; autoseo docroot outside public_html)
s=open(root+'/'+t).read()
for a,b in [
 ("AUTOSEO = ROOT + '/autoseo';","AUTOSEO = HOME + '/autoseo.my';"),
 ("urlList: [H + '/tips/'] } }, 'IndexNow body');","urlList: [H + '/tips/', 'https://www.sofacaresg.com/sitemap.xml'] } }, 'IndexNow body (page + sitemap, 21 Nov 2026)');"),
 ("eq(r.autoSitemap.indexnow, { status: 'sent', http: 200, urls: 1 }, 'indexnow result');","eq(r.autoSitemap.indexnow, { status: 'sent', http: 200, urls: 2 }, 'indexnow result');"),
 ("eq(posts[0].body.urlList, [H + '/tips/'], 'IndexNow for the edited page');","eq(posts[0].body.urlList, [H + '/tips/', H + '/sitemap.xml'], 'IndexNow for the edited page + sitemap');"),
 ("eq(d.autoSitemap.indexnow, { status: 'would send', urls: [H + '/tips/'] }, 'planned IndexNow');","eq(d.autoSitemap.indexnow, { status: 'would send', urls: [H + '/tips/', H + '/sitemap.xml'] }, 'planned IndexNow');"),
 ("eq(posts[0].body.urlList, [H + '/e/'], 'IndexNow');","eq(posts[0].body.urlList, [H + '/e/', H + '/sitemap.xml'], 'IndexNow');"),
 ("eq(posts.length, 1, 'IndexNow sent'); eq(posts[0].body.urlList, [J + '/articles/new-one/'], 'for the page');","eq(posts.length, 1, 'IndexNow sent'); eq(posts[0].body.urlList, [J + '/articles/new-one/', J + '/sitemap.xml'], 'for the page + sitemap');"),
]:
    assert s.count(a)==1,(a,s.count(a)); s=s.replace(a,b)
open(root+'/'+t,'w').write(s)
print('test fix-ups applied')
