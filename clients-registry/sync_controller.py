"""Fill status + live_date in registry.json from controller-snapshot.json (Controller = source of truth, Edwin 22 Nov 2026).
Controller live -> live, preview/activating -> in_build, anything else -> dormant. A row whose controller_slug is missing from
the snapshot (or is '-') keeps its status_override if set, else 'unknown' (left out of every total and listed for Edwin)."""
import json, sys, datetime
MAP = {'live':'live','preview':'in_build','activating':'in_build'}
def sync(reg, snap):
    gaps = []
    for r in reg['records']:
        c = snap['clients'].get(r['controller_slug'])
        if c and not (len(c) > 2 and c[2] == 'billing_only' and r.get('status_override')):
            r['status'] = MAP.get(c[0], 'dormant'); r['live_date'] = c[1] if r['status'] == 'live' else None
        elif r.get('status_override'):
            r['status'] = r['status_override']; r['live_date'] = r.get('live_date_override')
            gaps.append('%s: no usable Controller row, using override %s' % (r['id'], r['status']))
        else:
            r['status'] = 'unknown'; r['live_date'] = None; gaps.append('%s: not in Controller, left out of totals' % r['id'])
    reg['as_of'] = snap['taken_at']; return gaps
if __name__ == '__main__':
    reg = json.load(open('registry.json')); gaps = sync(reg, json.load(open('controller-snapshot.json')))
    json.dump(reg, open('registry.json','w'), indent=1, ensure_ascii=False); print('\n'.join(gaps) or 'no gaps')
