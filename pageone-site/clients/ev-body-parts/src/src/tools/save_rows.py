#!/usr/bin/env python3
"""Merge Base44 MCP query_entities output into db/*.json.
usage: python3 tools/save_rows.py EvProduct page1.json [page2.json ...]   (each file = the raw tool result {"entities":[...]} or a bare list)
Writes db/<brands|cars|products|photos>.json with only the fields build.py uses (nulls dropped). Re-run per entity; photos only for referenced groups."""
import json, sys
from pathlib import Path
DB = Path(__file__).resolve().parent.parent / "db"
NAME = {"EvBrand": "brands", "EvCar": "cars", "EvProduct": "products", "EvPhoto": "photos"}
KEEP = {"EvBrand": ["key", "name", "alias", "order", "intro", "status"], "EvCar": ["key", "b", "name", "alias", "years", "code", "photo", "status"],
        "EvProduct": ["key", "m", "p", "title", "pn", "side", "oem", "grade", "price", "stock", "photos", "desc", "note", "source", "status", "created_date", "updated_date"],
        "EvPhoto": ["group", "i", "n", "data", "product"]}
ent = sys.argv[1]; rows = []
for f in sys.argv[2:]:
    j = json.loads(Path(f).read_text()); rows += j["entities"] if isinstance(j, dict) else j
out = [{k: r[k] for k in KEEP[ent] if r.get(k) is not None} for r in rows]
if ent == "EvBrand": out.sort(key=lambda r: r.get("order", 999))
elif ent != "EvPhoto": out.sort(key=lambda r: r["key"])
(DB / (NAME[ent] + ".json")).write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(ent, len(out), "rows ->", NAME[ent] + ".json")
