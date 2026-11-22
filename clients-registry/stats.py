"""Computed numbers for both /clients pages. Never hard-code these on a page."""
import datetime
SGT = datetime.timezone(datetime.timedelta(hours=8))
def stats(reg, today=None):
    today = today or datetime.datetime.now(SGT).date()
    recs = [r for r in reg['records'] if r['visibility'] != 'own' and r['status'] in ('live', 'in_build')]
    wl = [r for r in recs if r['visibility'] == 'white-label']
    wl_live = [r for r in wl if r['status'] == 'live']
    inds = {}
    for r in wl_live: inds[r['industry_label']] = inds.get(r['industry_label'], 0) + 1
    cut = today - datetime.timedelta(days=30)
    recent = [r for r in wl_live if r['live_date'] and datetime.date.fromisoformat(r['live_date']) > cut]
    po_live = [r for r in recs if r['visibility'] == 'public' and r['status'] == 'live' and r['agency'] == 'pageone']
    po_build = [r for r in recs if r['visibility'] == 'public' and r['status'] == 'in_build']
    po_inds = sorted({r['industry_id'] for r in po_live})
    return dict(wl_live=len(wl_live), wl_build=sum(r['status'] == 'in_build' for r in wl),
                wl_industries=sorted(inds.items(), key=lambda x: (-x[1], x[0])), wl_last30=len(recent),
                po_live=len(po_live), po_industries=len(po_inds), po_build=len(po_build),
                updated=today.strftime('%-d %b %Y'), updated_iso=today.isoformat())
if __name__ == '__main__':
    import json; print(json.dumps(stats(json.load(open('registry.json'))), indent=1))
