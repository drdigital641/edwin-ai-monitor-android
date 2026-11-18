#!/usr/bin/env python3
"""Maison /new-launches/ hub: image cards on top + instant search + compact list (Edwin 18 Nov 2026).

Usage: hub_cards.py <live hub.html> <launch-queue.json> <out.html>
       (sort_hub.py calls this too, so the daily 2:17pm run keeps the layout.)

Works on the live hub in either shape (the old single card grid, or a hub this script already made), so it can be run
again every day. Card order = launch-queue.json hub_order (DONE first, then TODO by launch date, undated last).

Image card = a launch whose detail page has concept images, detected from data:
  * gen2 full-concept pages: status DONE in launch-queue.json and an entry in maison-expand/gen2/data.py
    (hero = its first render, the living room; object-position from that render's "pos"; 900w + big WebP)
  * older concept pages: listed in hub-heroes.json "legacy" (checked live 18 Nov 2026)
Everything else stays in the compact list. Every card stays in the HTML (filtering only sets hidden).
"""
import html, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GEN2 = os.path.join(HERE, "..", "maison-expand", "gen2")
HEROES = os.path.join(HERE, "hub-heroes.json")
SITE = "https://maisoninteriordesign.sg"
WA = "6593391185"
IMG = "/images/new-launches/"
EAGER = 2  # first N image cards load eagerly

KIND_WORDS = {"BTO": "hdb bto flat", "HDB": "hdb flat", "EC": "ec executive condominium",
              "Condo": "condo condominium private", "Landed": "landed house", "Commercial": "commercial office retail shop"}
KIND_LABEL = {"BTO": "HDB BTO", "HDB": "HDB", "EC": "EC", "Condo": "Condo"}

def E(s): return html.escape(s, quote=True)
def T(s): return html.escape(s, quote=False)
def U(s): return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def load_gen2():
    sys.path.insert(0, os.path.abspath(GEN2))
    import data  # noqa
    sys.path.pop(0)
    return data.P

def parse_cards(region):
    """Cards from either hub shape -> list of dicts (plain-text fields)."""
    out = []
    for m in re.finditer(r'<a class="lc[^"]*" href="/new-launches/([^/"]+)/"([^>]*)>(.*?)</a>', region, re.S):
        slug, attrs, body = m.group(1), m.group(2), m.group(3)
        a = dict(re.findall(r'data-([a-z]+)="([^"]*)"', attrs))
        if "name" in a:  # made by this script
            c = {k: html.unescape(a.get(k, "")) for k in ("kind", "tag", "name", "area", "note")}
        else:            # original hub card
            tag = re.search(r'<span class="tag">(.*?)</span>', body, re.S)
            h3 = re.search(r'<h3>(.*?)</h3>', body, re.S)
            em = re.search(r'<em>(.*?)</em>', h3.group(1), re.S) if h3 else None
            p = re.search(r'<p>(.*?)</p>', body, re.S)
            c = {"kind": a.get("kind", ""), "tag": U(tag.group(1)) if tag else "",
                 "name": U(re.sub(r"<em>.*?</em>", "", h3.group(1), flags=re.S)) if h3 else slug,
                 "area": U(em.group(1)) if em else "", "note": U(p.group(1)) if p else ""}
        c["slug"] = slug
        out.append(c)
    return out

def norm(s):
    s = html.unescape(s).lower().replace("&", " and ")
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def build(src_html, queue, gen2=None, heroes=None):
    h = src_html
    Q = queue
    P = gen2 if gen2 is not None else load_gen2()
    H = heroes if heroes is not None else json.load(open(HEROES, encoding="utf-8"))
    qp = {p["slug"]: p for p in Q["projects"]}

    # ---- locate the card region (old or new shape)
    if "<!--nlb-->" in h:
        s = h.index("<!--nlb-->"); e = h.index("<!--/nlb-->") + len("<!--/nlb-->")
        sec_open = h.rfind('<section class="sec tight', 0, s)
        pre, region, post = h[:sec_open], h[s:e], h[e:]
        post = re.sub(r'^\n', '', post)
    else:
        OPEN = '<section class="sec tight"><div class="wrap"><div class="lgrid" id="lgrid">'
        s = h.index(OPEN)
        e = h.index('<p class="nl-indep">', s)
        pre, region, post = h[:s], h[s:e], h[e:]
    # type chips move under the search box (search first on a phone screen); kept as-is so mid.js still drives them
    CH = re.compile(r'<div class="chips nlh-chips"[^>]*>.*?</div>', re.S)
    chips = CH.search(pre) or CH.search(region)
    chips = chips.group(0) if chips else ""
    pre = CH.sub("", pre)
    cards = parse_cards(region)
    assert len(cards) >= 90, f"only {len(cards)} cards parsed"
    slugs = [c["slug"] for c in cards]
    assert len(set(slugs)) == len(slugs), "duplicate cards"

    order = Q.get("hub_order") or [p["slug"] for p in Q["projects"]]
    rank = {sl: i for i, sl in enumerate(order)}
    cards.sort(key=lambda c: (rank.get(c["slug"], 10**6), slugs.index(c["slug"])))

    # ---- hero per detailed launch (from data)
    def hero(slug):
        if slug in H["legacy"]:
            x = H["legacy"][slug]
            return dict(base=f'{x["dir"]}/{x["dir"].replace("-v4", "")}-v4-{x["stem"]}', big=x["big"],
                        pos=x["pos"], alt=x["alt"], line=x["line"])
        if slug in P and qp.get(slug, {}).get("status") == "DONE":
            d = P[slug]; r = d["renders"][0]
            return dict(base=f'{d["dir"]}/{d["dir"].replace("-v4", "")}-v4-{r["stem"]}', big=d.get("big", "1920"),
                        pos=r["pos"], alt=r["alt"], line=d.get("card_line") or H["gen2_line"])
        return None

    def years(c):
        ys = set(re.findall(r"\b20[2-3]\d\b", c["note"] + " " + c["tag"]))
        ls = (qp.get(c["slug"], {}).get("launch_sort") or "")[:4]
        if re.fullmatch(r"20\d\d", ls): ys.add(ls)
        return " ".join(sorted(ys))

    def search_text(c):
        ws = norm(" ".join([c["name"], c["area"], c["tag"], KIND_WORDS.get(c["kind"], c["kind"]),
                            years(c), c["slug"].replace("-", " ")])).split()
        return " ".join(dict.fromkeys(ws))

    def common_attrs(c, ref):
        a = (f' data-kind="{E(c["kind"])}" data-cta="launch_card" data-ref="{ref}-{E(c["slug"])}"'
             f' data-s="{E(search_text(c))}"')
        if ref == "nl-img":  # image cards keep the list fields so a later run can turn them back into a list row
            a += f' data-name="{E(c["name"])}" data-area="{E(c["area"])}" data-tag="{E(c["tag"])}" data-note="{E(c["note"])}"'
        return a

    feat, rest = [], []
    for c in cards:
        hh = hero(c["slug"])
        (feat if hh else rest).append((c, hh))

    fh = []
    for i, (c, x) in enumerate(feat):
        typ = KIND_LABEL.get(c["kind"]) or c["tag"].split(" · ")[0]
        b = IMG + x["base"]
        lazy = '' if i < EAGER else ' loading="lazy"'
        fh.append(
            f'<a class="lc lk" href="/new-launches/{c["slug"]}/"{common_attrs(c, "nl-img")}>'
            f'<figure><img src="{b}-900.webp" srcset="{b}-900.webp 900w, {b}-{x["big"]}.webp {x["big"]}w"'
            f' sizes="(min-width:1240px) 390px, (min-width:1024px) 31vw, (min-width:640px) 47vw, 100vw"'
            f' width="900" height="506" alt="{E(x["alt"])}" style="object-position:{E(x["pos"])}" decoding="async"{lazy}></figure>'
            f'<span class="lk-t"><span class="lk-m"><span>{T(typ)}</span><span>{T(c["area"])}</span></span>'
            f'<h3>{T(c["name"])}</h3><span class="lk-p">{T(x["line"])}</span>'
            f'<span class="more">See the concepts</span></span></a>')
    lh = []
    for c, _ in rest:
        lh.append(f'<a class="lc" href="/new-launches/{c["slug"]}/"{common_attrs(c, "nl-list")}>'
                  f'<span class="tag">{T(c["tag"])}</span><h3>{T(c["name"])} <em>{T(c["area"])}</em></h3>'
                  f'<p>{T(c["note"])}</p><span class="more">Read the guide</span></a>')

    wa_txt = "Hi Maison, I couldn't find my project on your new launches page. Can you check it?"
    from urllib.parse import quote
    wa_href = f"https://wa.me/{WA}?text={quote(wa_txt, safe='')}"
    srch = ('<form class="nls" id="nls" role="search" action="/new-launches/" method="get">'
            '<label class="nls-l" for="nlq">Find your project</label><div class="nls-box">'
            '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="m15.5 15.5 5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>'
            '<input id="nlq" name="q" type="search" placeholder="Project, area or HDB/EC/condo" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search" maxlength="60">'
            '<button type="button" class="nls-x" id="nls-x" aria-label="Clear search" hidden><svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg></button>'
            '</div><p class="nls-n" id="nls-n" aria-live="polite"></p></form>')
    none = (f'<div class="nls-none" id="nls-none" hidden><p>No match: WhatsApp us and we\'ll check that project.</p>'
            f'<a class="btn dark-b" id="nls-wa" href="{E(wa_href)}" data-cta="whatsapp" data-ref="new-launches-search-none" target="_blank" rel="noopener">WhatsApp Maison</a></div>')
    body = ('<!--nlb-->' + srch + chips + none +
            f'<h2 class="nlh" id="nlh-f">With concept designs <span>{len(fh)}</span></h2><div class="lfeat" id="lfeat">' + "".join(fh) + '</div>'
            f'<h2 class="nlh" id="nlh-l">More new launches <span>{len(lh)}</span></h2><div class="lgrid" id="lgrid">' + "".join(lh) + '</div>'
            '<!--/nlb-->\n')
    out = pre + '<section class="sec tight nlb"><div class="wrap">' + body + post

    # ---- CSS (head) and JS (end of body), replaced on every run
    css = open(os.path.join(HERE, "hub", "nlb.css"), encoding="utf-8").read().strip()
    js = open(os.path.join(HERE, "hub", "nlb.js"), encoding="utf-8").read().strip()
    out = re.sub(r'<style id="nlb-css">.*?</style>\n', '', out, flags=re.S)
    out = re.sub(r'<script id="nlb-js">.*?</script>\n', '', out, flags=re.S)
    out = out.replace('</head>', f'<style id="nlb-css">{css}</style>\n</head>', 1)
    i = out.rindex('<script src="/mid.js')
    out = out[:i] + f'<script id="nlb-js">{js}</script>\n' + out[i:]

    # ---- WebSite SearchAction (real URL: /new-launches/?q= pre-fills the filter)
    if '"#website-nl"' not in out and f'"{SITE}/#website-nl"' not in out:
        node = {"@type": "WebSite", "@id": f"{SITE}/#website-nl", "url": f"{SITE}/", "name": "Maison Interior Design",
                "potentialAction": {"@type": "SearchAction",
                                    "target": {"@type": "EntryPoint", "urlTemplate": f"{SITE}/new-launches/?q={{search_term_string}}"},
                                    "query-input": "required name=search_term_string"}}
        k = out.index('"@graph":[') + len('"@graph":[')
        out = out[:k] + json.dumps(node, separators=(",", ":")) + "," + out[k:]

    # ---- checks
    for c in cards:
        assert out.count(f'href="/new-launches/{c["slug"]}/"') >= 1, c["slug"]
    assert out.count('id="lgrid"') == 1 and out.count('id="lfeat"') == 1 and out.count("<h1") == 1
    return out, len(fh), len(lh), [c["slug"] for c, _ in feat]

def main():
    src, qf, dst = sys.argv[1:4]
    h = open(src, encoding="utf-8").read()
    Q = json.load(open(qf, encoding="utf-8"))
    out, nf, nl, fs = build(h, Q)
    open(dst, "w", encoding="utf-8").write(out)
    print(f"{nf} image cards, {nl} list rows; image cards: {', '.join(fs)}")

if __name__ == "__main__":
    main()
