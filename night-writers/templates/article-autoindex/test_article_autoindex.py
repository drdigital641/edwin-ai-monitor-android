#!/usr/bin/env python3
"""Offline tests for article_autoindex.py: a fake Bridge (no network, no live site, no IndexNow request).
Run: python3 test_article_autoindex.py"""
import json
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import article_autoindex as A  # noqa: E402

HUB = '''<!doctype html><html><head><title>Articles | Hon Win Motor</title>
<link rel="canonical" href="https://sgcarworkshop.sg/workshops/hon-win-motor/articles/"></head><body>
<nav class="hw-nav"><ul class="hw-w"><li><a href="../../../workshops/hon-win-motor/">Profile</a></li><li><a href="../../../workshops/hon-win-motor/articles/" aria-current="page">Articles</a></li></ul></nav>
<section class="hw-sec"><div class="hw-w"><ul class="hw-cards hw-arts"><li><a href="../../../workshops/hon-win-motor/articles/used-car-inspection-hougang/"><figure><img src="../../../assets/img/hw/articles/used-car-inspection-hougang.jpg" alt="Illustrative: x"></figure><h3>Used car inspection</h3><p>What we check.</p><time datetime="2026-11-21">21 November 2026</time></a></li><li><a href="../../../workshops/hon-win-motor/articles/gearbox-repair-or-replace-hougang/"><h3>Gearbox</h3></a></li></ul></div></section>
<footer><ul><li><a href="../../../workshops/hon-win-motor/articles/">Articles</a></li></ul></footer></body></html>'''
SLUG = 'brake-pads-hougang-test'
URL = 'https://sgcarworkshop.sg/workshops/hon-win-motor/articles/%s/' % SLUG
PAGE = '<!doctype html><html><head><title>Brake pads | Hon Win Motor</title><link rel="canonical" href="%s"></head><body><h1>Brake pads: when to change them</h1></body></html>' % URL
CARD = '<li><a href="../../../workshops/hon-win-motor/articles/%s/"><h3>Brake pads: when to change them</h3><p>Signs.</p><time datetime="2026-11-23">23 November 2026</time></a></li>' % SLUG
SM = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url>\n    <loc>https://sgcarworkshop.sg/workshops/hon-win-motor/articles/</loc>\n    <lastmod>2026-11-21</lastmod>\n  </url>\n</urlset>\n'


class FakeBridge:
    """Mimics the Bridge runner API, including the auto-sitemap step after write_many."""

    def __init__(self, files, indexnow_http=200, pings_sitemap=True, auto=True):
        self.files, self.http, self.pings_sitemap, self.auto = dict(files), indexnow_http, pings_sitemap, auto
        self.calls = []

    def __call__(self, fn, body):
        self.calls.append((fn, body))
        if fn == 'bridgeReadLive':
            c = self.files[body['path']]
            return 200, {'ok': True, 'content': c, 'sha256': 'sha-' + str(len(c))}
        if fn == 'bridgeWriteMany':
            base = (body.get('base_path') or '').rstrip('/')
            base = base + '/' if base else ''
            for f in body['files']:
                if 'expected_sha256' in f and f['expected_sha256'] != 'sha-' + str(len(self.files[base + f['path']])):
                    return 409, {'ok': False, 'error': 'stale'}
            urls = []
            for f in body['files']:
                m = re.search(r'rel="canonical" href="([^"]+)"', f['content'])
                urls.append(m.group(1))
                if not body['dry_run']:
                    self.files[base + f['path']] = f['content']
            if not self.auto:
                return 200, {'ok': True, 'autoSitemap': {'status': 'nothing'}}
            sm_path = base + 'sitemap.xml'
            added = [u for u in urls if u not in self.files[sm_path]]
            bumped = [u for u in urls if u not in added]
            ping = urls + (['https://sgcarworkshop.sg/sitemap.xml'] if self.pings_sitemap else [])
            if body['dry_run']:
                return 200, {'ok': True, 'autoSitemap': {'status': 'dry_run', 'added': added, 'bumped': bumped,
                                                          'indexnow': {'status': 'would send', 'urls': ping}}}
            xml = self.files[sm_path]
            for u in added:
                xml = xml.replace('</urlset>', '  <url>\n    <loc>%s</loc>\n    <lastmod>2026-11-23</lastmod>\n  </url>\n</urlset>' % u)
            self.files[sm_path] = xml
            ind = {'status': 'sent' if self.http in (200, 202) else 'error', 'http': self.http, 'urls': len(ping)}
            return 200, {'ok': True, 'autoSitemap': {'status': 'ok', 'added': added, 'bumped': bumped, 'indexnow': ind}}
        if fn == 'bridgeRunnerIndexNow':
            st = 'sent' if self.http in (200, 202) else 'error'
            return 200, {'ok': True, 'status': st, 'results': [{'host': 'sgcarworkshop.sg', 'status': st, 'http': self.http, 'urls': len(body['urls'])}]}
        if fn == 'bridgeWrite':
            self.files[body['path']] = body['content']
            return 200, {'ok': True, 'saved': True}
        if fn == 'bridgeRunnerSitemap':
            return 200, {'ok': True, 'autoSitemap': {'status': 'ok', 'added': [], 'bumped': []}}
        return 404, {'ok': False, 'error': 'unknown fn ' + fn}


def site(key='hon-win-motor'):
    return A.load_sites()[key]


class T(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.q, self.log = os.path.join(self.tmp, 'q.json'), os.path.join(self.tmp, 'log.jsonl')
        self.files = {'preview/sgcarworkshop/workshops/hon-win-motor/articles/index.html': HUB,
                      'preview/sgcarworkshop/sitemap.xml': SM}

    def run_pub(self, fb, dry=False):
        br = A.Bridge(key='', transport=fb)
        page = A.Page(path='workshops/hon-win-motor/articles/%s/index.html' % SLUG, html=PAGE, card_html=CARD)
        return A.publish(br, site(), [page], dry_run=dry, date='2026-11-23', queue_path=self.q, log_path=self.log)

    def test_hub_card_goes_first_and_nav_is_untouched(self):
        out, st = A.insert_hub_card(HUB, CARD, URL, 'hon-win-motor/articles/')
        self.assertEqual(st, 'inserted')
        cards = re.findall(r'articles/([a-z0-9-]+)/"', out.split('hw-cards')[1])
        self.assertEqual(cards[:3], [SLUG, 'used-car-inspection-hougang', 'gearbox-repair-or-replace-hougang'])
        self.assertIn('<ul class="hw-cards hw-arts">' + CARD + '<li>', out)
        self.assertEqual(out.replace(CARD, ''), HUB, 'nothing else changed')
        again, st2 = A.insert_hub_card(out, CARD, URL, 'hon-win-motor/articles/')
        self.assertEqual((again, st2), (out, 'already_listed'))

    def test_hub_without_cards_reports(self):
        self.assertEqual(A.insert_hub_card('<html><body><p>none</p></body></html>', CARD, URL, 'articles/')[1], 'no_card_list')

    def test_itemlist_json_ld(self):
        hub = HUB.replace('</head>', '<script type="application/ld+json">{"@type":"ItemList","itemListElement":[{"@type":"ListItem","position":1,"url":"https://x/a/"}]}</script></head>')
        out, _ = A.insert_hub_card(hub, CARD, URL, 'hon-win-motor/articles/', 'Brake pads')
        data = json.loads(re.search(r'ld\+json">(.*?)</script>', out).group(1))
        self.assertEqual([i['position'] for i in data['itemListElement']], [1, 2])
        self.assertEqual(data['itemListElement'][0]['url'], URL)

    def test_publish_ok_sitemap_hub_indexnow(self):
        fb = FakeBridge(self.files)
        r = self.run_pub(fb)
        self.assertTrue(r['ok'], r)
        self.assertEqual(r['hubs'], {'workshops/hon-win-motor/articles/index.html': 'inserted'})
        self.assertEqual(r['sitemap'], 'listed')
        self.assertEqual(r['sitemap_check'], {URL: '2026-11-23'})
        self.assertEqual(r['indexnow']['status'], 'sent')
        self.assertNotIn('indexnow_sitemap', r, 'the Bridge already pinged the sitemap URL')
        wm = [b for f, b in fb.calls if f == 'bridgeWriteMany'][0]
        self.assertEqual(wm['base_path'], 'preview/sgcarworkshop')
        self.assertEqual([f['path'] for f in wm['files']], ['workshops/hon-win-motor/articles/%s/index.html' % SLUG, 'workshops/hon-win-motor/articles/index.html'])
        self.assertIn('expected_sha256', wm['files'][1], 'hub replace carries the base sha (live edit rule)')
        self.assertTrue(os.path.exists(self.log))

    def test_old_bridge_gets_extra_sitemap_ping(self):
        fb = FakeBridge(self.files, pings_sitemap=False)
        r = self.run_pub(fb)
        self.assertEqual(r['indexnow_sitemap']['status'], 'sent')
        self.assertEqual([b['urls'] for f, b in fb.calls if f == 'bridgeRunnerIndexNow'], [['https://sgcarworkshop.sg/sitemap.xml']])

    def test_429_is_queued_then_resent(self):
        fb = FakeBridge(self.files, indexnow_http=429)
        r = self.run_pub(fb)
        self.assertEqual(r['indexnow']['status'], 'queued')
        q = json.load(open(self.q))
        self.assertEqual(q['items'][0]['urls'], [URL, 'https://sgcarworkshop.sg/workshops/hon-win-motor/articles/', 'https://sgcarworkshop.sg/sitemap.xml'])
        br = A.Bridge(key='', transport=fb)
        self.assertEqual(A.resend_queue(br, A.load_sites(), self.q, self.log)['still_queued'], 1, 'still 429: kept')
        fb.http = 200
        self.assertEqual(A.resend_queue(br, A.load_sites(), self.q, self.log), {'sent': 1, 'still_queued': 0, 'expired': 0})
        self.assertEqual(json.load(open(self.q))['items'], [])

    def test_dry_run_writes_nothing(self):
        fb = FakeBridge(self.files)
        r = self.run_pub(fb, dry=True)
        self.assertTrue(r['ok'], r)
        self.assertEqual(fb.files, self.files)
        self.assertEqual(r['indexnow']['bridge_plan'], [URL, 'https://sgcarworkshop.sg/workshops/hon-win-motor/articles/', 'https://sgcarworkshop.sg/sitemap.xml'])
        self.assertFalse([c for c in fb.calls if c[0] in ('bridgeRunnerIndexNow', 'bridgeWrite')])

    def test_pageone_root_manual_sitemap(self):
        files = {'articles/index.html': HUB.replace('workshops/hon-win-motor/articles/', 'articles/'),
                 'sitemap.xml': SM.replace('sgcarworkshop.sg/workshops/hon-win-motor', 'pageonesingapore.com')}
        fb = FakeBridge(files, auto=False)
        br = A.Bridge(key='', transport=fb)
        u = 'https://pageonesingapore.com/articles/new-one/'
        page = A.Page(path='articles/new-one/index.html', html=PAGE.replace(URL, u), card_html=CARD.replace('workshops/hon-win-motor/articles/' + SLUG, 'articles/new-one'))
        r = A.publish(br, A.load_sites()['pageone'], [page], date='2026-11-23', queue_path=self.q, log_path=self.log)
        self.assertTrue(r['ok'], r)
        self.assertIn('<loc>%s</loc><lastmod>2026-11-23</lastmod>' % u, fb.files['sitemap.xml'])
        self.assertIn('<loc>https://pageonesingapore.com/articles/</loc>\n    <lastmod>2026-11-23</lastmod>', fb.files['sitemap.xml'], 'hub lastmod bumped')
        self.assertEqual([b['urls'] for f, b in fb.calls if f == 'bridgeRunnerIndexNow'][0][-1], 'https://pageonesingapore.com/sitemap.xml')

    def test_blocked_site_is_skipped(self):
        fb = FakeBridge(self.files)
        r = A.publish(A.Bridge(key='', transport=fb), A.load_sites()['autotex'], [], queue_path=self.q, log_path=self.log)
        self.assertEqual(r['skipped'], 'blocked:domain-not-resolving')
        self.assertEqual(fb.calls, [])

    def test_sites_json_covers_the_roster(self):
        s = A.load_sites()
        want = ('batteryrescue.sg xado-shop.sg cleanicdetailing.com jackygearbox.com cskatrading.com theecuclinicsg.com sggarage.com '
                'maisoninteriordesign.sg ecumats.my ktech.my autoseo.my contiexpert.sg sofacaresg.com planwithben.sg pageonesingapore.com '
                'jbstaycations.com dannychuafinancial.com evbodyparts.sg aliciaongproperty.com wrapstarautostyle.com aivs.sg '
                'autotexautoparts.com.sg starperformancemotor.com klardetails.com.sg hybridworld.com.my carzyworld.com.my benzworld.my '
                'jayvenang.sg urbanecosolutions.com newzenwerkz.com.sg apcar.com.my mykar.my lilianproperties.com sgcarworkshop.sg').split()
        hosts = {x.host.replace('www.', '') for x in s.values()}
        self.assertEqual([w for w in want if w not in hosts], [])
        self.assertNotIn('commercialfitout.sg', hosts)
        for x in s.values():
            self.assertTrue(x.base == '' or x.base.endswith('/'), x.key)
            self.assertFalse(x.hub_path.startswith('/'), x.key)


if __name__ == '__main__':
    unittest.main(verbosity=1)
