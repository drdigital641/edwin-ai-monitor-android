"""Refresh builder/showcase.json from Search Console data.

Usage:
    python3 builder/showcase_refresh.py CASESTUDYSTATS.json [PORTFOLIOSITE.json]

CASESTUDYSTATS.json is a CaseStudyStats export from the SearchInsight Bridge app
(6aa2d85827b1f2c2d43b241e): either the {"entities": [...]} object that query_entities
returns or a bare list. Each record needs site_url, data_through, generated_at and
stats_json (a JSON string or an object). The newest record per site is used.

PORTFOLIOSITE.json (optional) is a PortfolioSite export from the Controller app
(6ac7f2548a9c3877449e2772); its articles_total updates each client's article count.

Only numbers from these exports are written. Everything a page says is formatted from
them in builder/showcase.py, so a refresh never needs a hand edit of any figure.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "showcase.json")
ROW_LIMIT = 5000  # gscCaseStudyStats asks Search Console for at most this many queries
QUERY_ROWS = 7    # searches shown per case study


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return d.get("entities", d) if isinstance(d, dict) else d


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    records = load(sys.argv[1])
    newest = {}
    for r in records:
        s = r["site_url"]
        if s not in newest or r["generated_at"] > newest[s]["generated_at"]:
            newest[s] = r
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)

    windows = set()
    for c in data["clients"]:
        r = newest.get(c["gsc_site"])
        if not r:
            sys.exit(f"No CaseStudyStats record for {c['gsc_site']} ({c['name']}). Add the site to Search Console or remove it.")
        st = r["stats_json"]
        st = json.loads(st) if isinstance(st, str) else st
        last, prev = st["last28"], st["prev28"]
        windows.add((r["data_through"], last["start"], last["end"], prev["start"], prev["end"]))
        skip = [q.lower() for q in c.get("skip_queries", [])]
        brand = [b.lower() for b in c.get("brand_terms", [])]
        queries = [q for q in st.get("showcase", [])
                   if q["query"].lower() not in skip and not any(b in q["query"].lower() for b in brand)]
        queries = sorted(sorted(queries, key=lambda q: -q["impressions"])[:QUERY_ROWS], key=lambda q: q["position"])
        c["gsc"] = {
            "record_id": r.get("id"), "first_day": st.get("first_day_with_data"),
            "clicks": last["clicks"], "impressions": last["impressions"], "position": round(last["position"], 1),
            "prev_clicks": prev["clicks"], "prev_impressions": prev["impressions"], "prev_position": round(prev["position"], 1),
            "queries": st.get("queries_28d", 0), "page_one": st.get("page_one_queries_28d", 0), "top3": st.get("top3_queries_28d", 0),
            "capped": st.get("queries_28d", 0) >= ROW_LIMIT,
            "monthly": [{"month": m["month"], "days": m["days"], "clicks": m["clicks"], "impressions": m["impressions"],
                         "position": None if m["position"] is None else round(m["position"], 1)} for m in st.get("monthly", [])],
            "top_queries": [{"query": q["query"], "position": q["position"], "impressions": q["impressions"]} for q in queries],
        }
    if len(windows) != 1:
        sys.exit(f"Records cover different date windows: {sorted(windows)}. Re-run the Case Study Stats workflow first.")
    through, s, e, ps, pe = windows.pop()
    data["data"] = {
        "source": "Google Search Console (final data), collected by the Case Study Stats workflow into CaseStudyStats, SearchInsight Bridge app 6aa2d85827b1f2c2d43b241e",
        "generated_at": max(newest[c["gsc_site"]]["generated_at"] for c in data["clients"]),
        "data_through": through, "window": [s, e], "prev_window": [ps, pe],
    }

    if len(sys.argv) > 2:
        by_domain = {}
        for p in load(sys.argv[2]):
            by_domain[(p.get("domain") or "").replace("www.", "")] = p
        for c in data["clients"]:
            p = by_domain.get(c["domain"])
            if p and p.get("articles_total"):
                c["articles"] = p["articles_total"]

    with open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"showcase.json refreshed: {len(data['clients'])} sites, 28 days {s} to {e} (previous {ps} to {pe}).")


if __name__ == "__main__":
    main()
