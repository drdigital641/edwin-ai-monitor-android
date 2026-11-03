#!/usr/bin/env python3
"""Turn Controller CtaClick rows into data/taps.json (30-day WhatsApp/Call counts per workshop) for the build.

Rows come from the Controller (Base44 app 6ac7f2548a9c3877449e2772, entity CtaClick, site == 'sgcarworkshop' = live-domain taps only; the
preview's 'sgcarworkshop-test' rows are never counted). The daily run queries them and pipes the JSON list here:

    python3 taps.py rows.json            # rows.json = [{"cta_type","cta_label","session_id","created_date"}, ...]

Counting is per workshop (cta_label = slug) and per anonymous visit: one visit tapping the same button twice counts once. Nothing about a person is stored:
the output holds only slug -> {whatsapp, call} and the as_of date. build.py shows a card's WhatsApp count only from 5 (TAP_SHOW_MIN)."""
import datetime as dt, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'data', 'taps.json')


def count(rows, today=None):
    today = today or dt.datetime.now(dt.timezone.utc)
    cut = today - dt.timedelta(days=30)
    seen = {}
    for r in rows:
        k = r.get('cta_type')
        if k not in ('whatsapp', 'call') or not r.get('cta_label'):
            continue
        try:
            when = dt.datetime.fromisoformat(str(r['created_date']).replace('Z', '+00:00'))
            if when.tzinfo is None:
                when = when.replace(tzinfo=dt.timezone.utc)
        except Exception:
            continue
        if when < cut:
            continue
        seen.setdefault((r['cta_label'], k), set()).add(r.get('session_id') or id(r))
    out = {}
    for (slug, k), ids in seen.items():
        out.setdefault(slug, {'whatsapp': 0, 'call': 0})[k] = len(ids)
    return out


if __name__ == '__main__':
    rows = json.load(open(sys.argv[1])) if len(sys.argv) > 1 else []
    if isinstance(rows, dict):
        rows = rows.get('entities', [])
    res = {'as_of': dt.date.today().isoformat(), 'counts': count(rows)}
    json.dump(res, open(OUT, 'w'), indent=1, sort_keys=True)
    print('taps.json written:', len(res['counts']), 'workshops with taps')
