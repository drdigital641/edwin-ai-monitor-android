#!/usr/bin/env python3
"""Offline tests for sitemap_dynamic.py (fake Bridge, no network). Run: python3 test_sitemap_dynamic.py"""
import os
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
_tmp = tempfile.mkdtemp()
os.environ['SITEMAP_STATE_DIR'] = _tmp
os.environ['AUTOINDEX_STATE_DIR'] = _tmp
sys.path.insert(0, HERE)
import sitemap_dynamic as S  # noqa: E402
AI = S.AI


def page(canon, robots='index, follow', body='hello', extra=''):
    return ('<!doctype html><html><head><meta name="robots" content="%s"><link rel="canonical" href="%s">%s</head>'
            '<body><main>%s</main>%s</body></html>') % (robots, canon, extra, body, 'x' * 700)


class Fake:
    def __init__(self, files, mtimes, refuse_write=False):
        self.files, self.mtimes, self.refuse = dict(files), dict(mtimes), refuse_write
        self.writes, self.pings = [], []

    def __call__(self, fn, body):
        if fn == 'bridgeListLive':
            base = body.get('path', '')
            ents = []
            for p in self.files:
                if base and not p.startswith(base + '/'):
                    continue
                ents.append({'path': p, 'type': 'file', 'mtime': self.mtimes.get(p, '2026-11-20T02:00:00Z'), 'readable': True})
            return 200, {'ok': True, 'entries': ents}
        if fn == 'bridgeReadLive':
            c = self.files[body['path']]
            return 200, {'ok': True, 'content': c, 'sha256': 'sha-%d' % len(c)}
        if fn == 'bridgeWrite':
            if self.refuse:
                return 403, {'ok': False, 'error': 'guard'}
            self.files[body['path']] = body['content']
            self.writes.append(body['path'])
            return 200, {'ok': True}
        if fn == 'bridgeRunnerIndexNow':
            self.pings.append(body['urls'])
            return 200, {'ok': True, 'results': [{'http': 429}]}
        raise AssertionError(fn)


SM_OLD = ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
          '<url><loc>https://d.com/</loc><lastmod>2026-11-01</lastmod></url>'
          '<url><loc>https://d.com/areas/</loc><lastmod>2026-11-22</lastmod></url>'
          '<url><loc>https://d.com/faq</loc></url></urlset>\n')


_N = [0]


def site(**kw):
    _N[0] += 1
    d = dict(key='t%d' % _N[0], host='d.com', bridge_site='danny', base='', hub_path='insights/index.html',
             hub_url='https://d.com/insights/', card_link='insights/')
    d.update(kw)
    return AI.Site(**d)


def files_basic():
    return {'sitemap.xml': SM_OLD,
            'index.html': page('https://d.com/'),
            'areas/index.html': page('https://d.com/areas'),
            'faq/index.html': page('https://d.com/faq'),
            'insights/new-article/index.html': page('https://d.com/insights/new-article', extra='<script type="application/ld+json">{"datePublished":"2026-11-21"}</script>'),
            'login/index.html': page('https://d.com/login'),
            'preview/x/index.html': page('https://pageonesingapore.com/preview/x/', robots='noindex'),
            'thin/index.html': page('https://d.com/thin', robots='noindex, follow'),
            '404.html': page('https://d.com/404')}


class T(unittest.TestCase):
    def run_one(self, files, mt=None, **kw):
        fb = Fake(files, mt or {})
        br = AI.Bridge(transport=fb)
        return fb, S.run_site(br, site(**kw.pop('site', {})), today='2026-11-23', **kw)

    def test_adds_missing_article_and_uses_canonical(self):
        fb, r = self.run_one(files_basic())
        xml = fb.files['sitemap.xml']
        self.assertIn('<loc>https://d.com/insights/new-article</loc><lastmod>2026-11-21</lastmod>', xml)
        self.assertIn('<loc>https://d.com/areas</loc>', xml)
        self.assertNotIn('https://d.com/areas/<', xml)          # trailing-slash loc replaced by canonical
        self.assertIn('https://d.com/insights/new-article', r.added)

    def test_skips_noindex_preview_login_404(self):
        fb, r = self.run_one(files_basic())
        xml = fb.files['sitemap.xml']
        for bad in ('/thin', '/login', '/preview/', '/404'):
            self.assertNotIn('d.com%s<' % bad, xml)
        self.assertNotIn('pageonesingapore.com', xml)

    def test_lastmod_filled_from_mtime_in_sgt(self):
        fb, r = self.run_one(files_basic(), {'faq/index.html': '2026-11-12T18:29:05Z'})
        self.assertIn('<loc>https://d.com/faq</loc><lastmod>2026-11-13</lastmod>', fb.files['sitemap.xml'])

    def test_unchanged_content_keeps_lastmod_on_rebuild(self):
        f = files_basic()
        fb = Fake(f, {})
        br = AI.Bridge(transport=fb)
        s = site(key='keep')
        S.run_site(br, s, today='2026-11-23')
        first = fb.files['sitemap.xml']
        fb.mtimes['faq/index.html'] = '2026-11-23T03:00:00Z'        # rewritten, same content
        r = S.run_site(br, s, today='2026-11-24')
        self.assertEqual(r.status, 'unchanged')
        self.assertEqual(fb.files['sitemap.xml'], first)
        fb.files['faq/index.html'] = page('https://d.com/faq', body='new answer')
        fb.mtimes['faq/index.html'] = '2026-11-24T03:00:00Z'
        r = S.run_site(br, s, today='2026-11-24')
        self.assertIn('https://d.com/faq', r.lastmod_moved)
        self.assertIn('<loc>https://d.com/faq</loc><lastmod>2026-11-24</lastmod>', fb.files['sitemap.xml'])

    def test_hreflang_only_where_translation_exists(self):
        f = {'sitemap.xml': SM_OLD.replace('https://d.com', 'https://m.my'),
             'index.html': page('https://m.my/'), 'ms/index.html': page('https://m.my/ms/'), 'zh/index.html': page('https://m.my/zh/'),
             'services/index.html': page('https://m.my/services/'), 'ms/services/index.html': page('https://m.my/ms/services/'),
             'areas/index.html': page('https://m.my/areas/'), 'faq/index.html': page('https://m.my/faq')}
        fb, r = self.run_one(f, site={'host': 'm.my', 'key': 'my'})
        xml = fb.files['sitemap.xml']
        self.assertIn('hreflang="zh" href="https://m.my/zh/"', xml)
        svc = xml.split('<loc>https://m.my/services/</loc>')[1].split('</url>')[0]
        self.assertIn('hreflang="ms"', svc)
        self.assertNotIn('hreflang="zh"', svc)                      # no zh/services page: no zh link
        self.assertIn('xmlns:xhtml=', xml)

    def test_drop_guard(self):
        f = files_basic()
        big = SM_OLD.replace('</urlset>', ''.join('<url><loc>https://d.com/gone-%d</loc></url>' % i for i in range(8)) + '</urlset>')
        f['sitemap.xml'] = big
        for i in range(8):
            f['gone-%d/index.html' % i] = page('https://d.com/gone-%d' % i, robots='noindex')
        fb, r = self.run_one(f)
        self.assertEqual(r.status, 'drop_guard')
        self.assertEqual(fb.writes, [])

    def test_keeps_image_blocks(self):
        f = files_basic()
        f['sitemap.xml'] = SM_OLD.replace('<lastmod>2026-11-01</lastmod></url>',
                                          '<lastmod>2026-11-01</lastmod><image:image><image:loc>https://d.com/a.webp</image:loc></image:image></url>')
        fb, r = self.run_one(f)
        self.assertIn('<image:image><image:loc>https://d.com/a.webp</image:loc></image:image>', fb.files['sitemap.xml'])
        self.assertIn('xmlns:image=', fb.files['sitemap.xml'])

    def test_indexnow_goes_to_daily_queue_not_sent(self):
        fb, r = self.run_one(files_basic())
        self.assertEqual(r.indexnow['status'], 'queued_for_daily_batch')
        self.assertEqual(fb.pings, [])
        q = AI._load_queue(AI.QUEUE_PATH)
        self.assertTrue(any('https://d.com/sitemap.xml' in it['urls'] for it in q['items']))

    def test_ping_now_429_is_queued(self):
        fb, r = self.run_one(files_basic(), ping_now=True, site={'key': 'pn'})
        self.assertEqual(r.indexnow['status'], 'queued')
        self.assertEqual(len(fb.pings), 1)

    def test_write_refused_reported(self):
        fb = Fake(files_basic(), {}, refuse_write=True)
        r = S.run_site(AI.Bridge(transport=fb), site(key='ref'), today='2026-11-23')
        self.assertEqual(r.status, 'write_refused')

    def test_inactive_skipped(self):
        fb, r = self.run_one(files_basic(), site={'status': 'hold:bridge-publish'})
        self.assertTrue(r.status.startswith('skipped'))

    def test_read_cap_keeps_unread_urls(self):
        fb, r = self.run_one(files_basic(), max_reads=1, site={'key': 'cap'})
        self.assertGreater(r.pending_reads, 0)
        new = fb.files['sitemap.xml']
        for u in ('https://d.com/<', 'https://d.com/faq<'):
            self.assertIn(u.replace('<', '</loc>'), new)   # unread pages keep their entry


if __name__ == '__main__':
    unittest.main(verbosity=1)
