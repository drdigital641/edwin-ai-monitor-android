"""Refresh builder/showcase.json from Search Console data.

Usage:
    python3 builder/showcase_refresh.py CASESTUDYSTATS.json [PORTFOLIOSITE.json] [CLIENT.json]

CASESTUDYSTATS.json is a CaseStudyStats export from the SearchInsight Bridge app
(6aa2d85827b1f2c2d43b241e): either the {"entities": [...]} object that query_entities
returns or a bare list. Each record needs site_url, data_through, generated_at and
stats_json (a JSON string or an object). The newest record per site is used.

PORTFOLIOSITE.json (optional) is a PortfolioSite export from the Controller app
(6ac7f2548a9c3877449e2772); its articles_total updates each client's article count.

CLIENT.json (optional) is a Client export from the same Controller app. It sets the
"being built" count shown next to the live count (showcase.json "pipeline"): every Client
with status activating or preview whose domain or slug is not already a live showcase
site, minus the slugs in pipeline "exclude" (records that are not signed-up clients).
"as_of" becomes today's date whenever that count or the live list changes.
The exports can be given in any order; each file is recognised by its fields.

After updating showcase.json it rebuilds the site (builder/build.py) and the llms.txt sections in
pageone-site/bridge/. Exit code 0 = something changed (figures, article counts, the live list or
the being-built count: open a PR and publish), 3 = nothing changed (skip the publish).

Only numbers from these exports are written. Everything a page says is formatted from
them in builder/showcase.py, so a refresh never needs a hand edit of any figure.
"""
import datetime, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "showcase.json")
ROW_LIMIT = 5000  # gscCaseStudyStats asks Search Console for at most this many queries
QUERY_ROWS = 7    # searches shown per case study


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d.get("entities", d) if isinstance(d, dict) else d


def kind(rows):
    """Which Base44 export a file is: CaseStudyStats, PortfolioSite or Client."""
    first = rows[0] if rows else {}
    if "stats_json" in first:
        return "css"
    if "articles_total" in first:
        return "portfolio"
    if "slug" in first and "status" in first:
        return "client"
    sys.exit("Unrecognised export: expected CaseStudyStats, PortfolioSite or Client records.")


def building_count(clients, data):
    """Signed-up clients whose site is not live on its own domain yet (never named publicly, only counted)."""
    live = {c["domain"].replace("www.", "") for c in data["clients"]} | {c["key"] for c in data["clients"]}
    exclude = set(data.get("pipeline", {}).get("exclude", []))
    n = 0
    for c in clients:
        dom = (c.get("domain") or "").replace("www.", "")
        if c.get("status") in ("activating", "preview") and c.get("slug") not in exclude and dom not in live and c.get("slug") not in live:
            n += 1
    return n


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    exports = {}
    for path in sys.argv[1:]:
        rows = load(path)
        exports[kind(rows)] = rows
    if "css" not in exports:
        sys.exit("A CaseStudyStats export is required.")
    newest = {}
    for r in exports["css"]:
        s = r["site_url"]
        if s not in newest or r["generated_at"] > newest[s]["generated_at"]:
            newest[s] = r
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    snapshot = lambda: json.dumps([[c["key"], c.get("gsc"), c.get("articles")] for c in data["clients"]]
                                  + [data.get("pipeline", {}).get("building")], sort_keys=True)
    before = snapshot()

    windows = set()
    for c in data["clients"]:
        r = newest.get(c["gsc_site"])
        if not r:
            if not c.get("gsc", {}).get("record_id"):
                # A newly launched site whose Search Console property has no data yet: it stays on the page as
                # "launched, no data yet" until the Case Study Stats workflow returns a record for it.
                print(f"note: no CaseStudyStats record yet for {c['gsc_site']} ({c['name']}); shown as launched, no data yet.")
                continue
            sys.exit(f"No CaseStudyStats record for {c['gsc_site']} ({c['name']}). Add the site to Search Console or remove it.")
        st = r["stats_json"]
        st = json.loads(st) if isinstance(st, str) else st
        last, prev = st["last28"], st["prev28"]
        windows.add((r["data_through"], last["start"], last["end"], prev["start"], prev["end"]))
        skip = [q.lower() for q in c.get("skip_queries", [])]
        brand = [b.lower() for b in c.get("brand_terms", [])]
        queries = [q for q in st.get("showcase", [])
                   if q["query"].lower() not in skip and not any(b in q["query"].lower() for b in brand)]
        top3 = sorted([q for q in queries if q["position"] <= 3], key=lambda q: -q["impressions"])
        best = {"query": top3[0]["query"], "position": top3[0]["position"], "impressions": top3[0]["impressions"]} if top3 else None
        queries = sorted(sorted(queries, key=lambda q: -q["impressions"])[:QUERY_ROWS], key=lambda q: q["position"])
        c["gsc"] = {
            "record_id": r.get("id"), "first_day": st.get("first_day_with_data"),
            "clicks": last["clicks"], "impressions": last["impressions"], "position": round(last["position"], 1),
            "prev_clicks": prev["clicks"], "prev_impressions": prev["impressions"], "prev_position": round(prev["position"], 1),
            "queries": st.get("queries_28d", 0), "page_one": st.get("page_one_queries_28d", 0), "top3": st.get("top3_queries_28d", 0),
            "capped": st.get("queries_28d", 0) >= ROW_LIMIT,
            "monthly": [{"month": m["month"], "days": m["days"], "clicks": m["clicks"], "impressions": m["impressions"],
                         "position": None if m["position"] is None else round(m["position"], 1)} for m in st.get("monthly", [])],
            "best_query": best,
            "top_queries": [{"query": q["query"], "position": q["position"], "impressions": q["impressions"]} for q in queries],
        }
    if len(windows) != 1:
        sys.exit(f"Records cover different date windows: {sorted(windows)}. Re-run the Case Study Stats workflow first.")
    through, s, e, ps, pe = windows.pop()
    data["data"] = {
        "source": "Google Search Console (final data), collected by the Case Study Stats workflow into CaseStudyStats, SearchInsight Bridge app 6aa2d85827b1f2c2d43b241e",
        "generated_at": max(newest[c["gsc_site"]]["generated_at"] for c in data["clients"] if c["gsc_site"] in newest),
        "data_through": through, "window": [s, e], "prev_window": [ps, pe],
    }

    if "portfolio" in exports:
        by_domain = {}
        for p in exports["portfolio"]:
            by_domain[(p.get("domain") or "").replace("www.", "")] = p
        for c in data["clients"]:
            p = by_domain.get(c["domain"])
            if p and p.get("articles_total"):
                c["articles"] = p["articles_total"]

    if "client" in exports:
        pipe = data.setdefault("pipeline", {})
        n = building_count(exports["client"], data)
        if n != pipe.get("building"):
            pipe["building"], pipe["as_of"] = n, datetime.date.today().isoformat()
            print(f"pipeline: {n} site(s) being built (was {pipe.get('building', 'unset')}).")

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"showcase.json refreshed: {len(data['clients'])} sites, 28 days {s} to {e} (previous {ps} to {pe}).")
    site = os.path.join(HERE, "..", "site")
    subprocess.run([sys.executable, os.path.join(HERE, "build.py"), site], check=True)
    after = snapshot()
    if after == before:
        print("NO CHANGE: every figure is the same as before. Skip the PR and the publish.")
        sys.exit(3)
    print("CHANGED: commit pageone-site/, open a PR, merge, then run bridge/update_pins.mjs in the Bluehost Bridge sandbox.")


if __name__ == "__main__":
    main()
