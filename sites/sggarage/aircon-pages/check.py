"""Checks for the two SG Garage aircon pages. Exit 1 on any problem."""
import json
import os
import re
import sys
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = ["car-aircon-specialist-singapore", "car-aircon-compressor-replacement"]
ALLOWED_PRICES = {"$20", "$600", "$800", "$30"}
# Paths that exist on the live server (checked via the Bridge, 3 Nov 2026) plus the two new pages.
KNOWN = {"/", "/car-servicing-repair/", "/car-aircon-repair/", "/accident-claim-repair/", "/prices/", "/about/", "/articles/",
         "/car-aircon-specialist-singapore/", "/car-aircon-compressor-replacement/"}
ARTICLES = os.environ.get("SGG_ARTICLES", "")  # optional newline list of article file names


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.links = []
        self.summ = []
        self._in_sum = False
        self.text = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "h1":
            self.h1 += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "summary":
            self._in_sum = True
            self.summ.append("")

    def handle_endtag(self, tag):
        if tag == "summary":
            self._in_sum = False

    def handle_data(self, d):
        if self.lasttag in ("script", "style"):
            return
        if self._in_sum:
            self.summ[-1] += d
        self.text.append(d)


def main():
    errs = []
    for slug in PAGES:
        f = os.path.join(HERE, "site", slug, "index.html")
        s = open(f, encoding="utf-8").read()
        e = lambda m: errs.append(f"{slug}: {m}")
        t = re.search(r"<title>(.*?)</title>", s).group(1)
        d = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
        import html as h
        t, d = h.unescape(t), h.unescape(d)
        if len(t) > 60: e(f"title {len(t)} chars")
        if not 120 <= len(d) <= 160: e(f"description {len(d)} chars")
        if f'<link rel="canonical" href="https://www.sggarage.com/{slug}/">' not in s: e("canonical")
        if "noindex" in s: e("noindex present")
        if 'rel="icon" href="/favicon.ico"' not in s or "apple-touch-icon" not in s: e("favicon links")
        if 'property="og:image"' not in s: e("og:image")
        p = P(); p.feed(s)
        if p.h1 != 1: e(f"{p.h1} h1")
        body_text = " ".join(p.text)
        if re.search(r"walk[- ]?in", body_text, re.I): e("walk-in wording")
        prices = set(re.findall(r"\$\d+(?:,\d{3})*", body_text))
        if prices - ALLOWED_PRICES: e(f"unexpected prices {prices - ALLOWED_PRICES}")
        if re.search(r"\$\s?\d+\s?[-–]\s?\$?\d+", body_text): e("price range")
        lds = re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
        if not lds: e("no JSON-LD")
        faq = None
        for raw in lds:
            try:
                j = json.loads(raw)
            except Exception as x:
                e(f"JSON-LD parse: {x}"); continue
            if re.search(r"aggregateRating|\"Review\"", raw): e("review markup")
            for n in j.get("@graph", [j]):
                if n.get("@type") == "FAQPage":
                    faq = [q["name"] for q in n["mainEntity"]]
        if faq is None: e("no FAQPage")
        elif [x.strip() for x in p.summ] != faq: e("FAQPage != visible FAQ")
        words = len(re.findall(r"\w+", body_text))
        if words < 600: e(f"only {words} words")
        for href in p.links:
            if href.startswith("/"):
                path = href.split("#")[0]
                if path.startswith("/articles/") and path.endswith(".html"):
                    if ARTICLES and path.split("/")[-1] not in ARTICLES.split():
                        e(f"missing article {path}")
                elif path not in KNOWN:
                    e(f"unknown internal link {path}")
        print(f"{slug}: title {len(t)}, desc {len(d)}, words {words}, faq {len(faq or [])}, links {len(p.links)}")
    for x in errs:
        print("FAIL", x)
    print("OK" if not errs else f"{len(errs)} problem(s)")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
