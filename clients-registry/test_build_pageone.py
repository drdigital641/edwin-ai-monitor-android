import json, os, re, sys, unittest, datetime
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_pageone as B
from stats import stats

TODAY = datetime.date(2026, 11, 22)


class T(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = json.load(open(os.path.join(HERE, 'registry.json')))
        cls.out, cls.st, cls.counts, cls.removed = B.build(TODAY, write=False)
        cls.low = cls.out.lower()

    def test_no_white_label_leak(self):
        for rx, label in B.forbidden_terms(self.reg):
            self.assertIsNone(re.search(rx, self.low), f'leak: {label}')

    def test_fixed_forbidden(self):
        for v in ["Dongfeng", "Battery Rescue", "Klar", "MyKar", "K Tech", "ktech.my", "batteryrescue", "klardetails", "mykar.my", "hon-win"]:
            self.assertNotIn(v.lower(), self.low, v)

    def test_check_catches_leak(self):
        wl = [r for r in self.reg['records'] if r['visibility'] == 'white-label' and r.get('host')]
        for r in wl:
            with self.assertRaises(AssertionError):
                B.check(self.out + f'<img src="img/clients/{r["host"]}.webp">', self.reg)
            with self.assertRaises(AssertionError):
                B.check(self.out + ' ' + r['name'], self.reg)

    def test_misc_assertions(self):
        self.assertNotIn('aggregaterating', self.low)
        self.assertNotIn('+60', self.out)
        self.assertEqual(self.out.count('/p1-cta.js'), 1)
        self.assertEqual(self.out.count('<script src="/p1-cta.js?v='), 1)
        self.assertNotRegex(self.out, r'(?<![\d,])28 client')
        self.assertNotIn('Latest 3 launches', self.out)
        self.assertIn('/privacy/', self.out)
        self.assertIn('index, follow', self.out)

    def test_wl_block_golden(self):
        gold = open(os.path.join(HERE, 'fixtures', 'wl-stats.html'), encoding='utf-8').read()
        self.assertEqual(B.wl_stats_html(self.st), gold)
        self.assertEqual(B.wl_stats_html(self.st), B.wl_stats_html(dict(self.st)))
        self.assertIn('<!-- wl-stats:start -->' + gold + '<!-- wl-stats:end -->', self.out)

    def test_counts(self):
        st = self.st
        self.assertEqual(sum(self.counts.values()), st['po_live'])
        self.assertEqual(len(self.counts), st['po_industries'])
        self.assertIn(f'<span data-reg="po_live">{st["po_live"]}</span>', self.out)
        self.assertIn(f'"numberOfItems": {st["po_live"]}', self.out)
        self.assertIn(f'"dateModified": "{TODAY.isoformat()}"', self.out)
        self.assertEqual(self.out.count('"aggregateRating"'), 0)
        for b, n in self.counts.items():
            self.assertRegex(self.out, rf'id="{b}-h">[^<]*<span class="count-badge">{n} websites?</span>')

    def test_agencies_and_sgcaraccident(self):
        self.assertIn('For agencies &amp; dealers: white-label SEO websites', self.out)
        self.assertIn('https://wa.me/6597856612?text=Hi%20Page%20One%20Singapore%2C%20I%27d%20like%20to%20talk%20about%20white-label%20SEO%20websites%20for%20my%20agency.', self.out)
        self.assertIn('img/clients/sgcaraccident.sg.webp', self.out)
        self.assertIn('Step-by-step help after a car accident in Singapore', self.out)
        self.assertNotIn('sgcarworkshop.sg', self.low)

    def test_meta_no_28(self):
        for m in re.findall(r'<meta (?:name|property)="(?:description|og:description|twitter:description)" content="([^"]*)"', self.out):
            self.assertEqual(m, B.meta_text(self.st))
            self.assertNotIn('28', m)


if __name__ == '__main__':
    unittest.main()
