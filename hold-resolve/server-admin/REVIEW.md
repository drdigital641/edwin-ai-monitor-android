# Review: Bridge cron + DNS tools (20 Nov 2026)

Edwin 20 Nov 2026 6:19pm SGT approved: add cron and DNS tools to the Bridge, narrow: cron = list/add/edit this account's own cron lines; DNS = this account's own zones on Bluehost; log every call; require a backup or before-and-after record.

Patched copy: Bridge sandbox /tmp/spo4 (base = Bridge app main). NOT saved. Tests there: serverAdmin 4/4, htaccessSafe 8, cpanelChokepoint 3, liveEdit 3, sitesView 1, needsYou all pass.

Files (new unless noted):
- base44/shared/serverAdmin.ts (logic)
- base44/functions/bridgeServerCron/entry.ts, bridgeServerDns/entry.ts (bridgeTool, sessionOnly:true, needsSite:false: every API key refused)
- base44/shared/cpanel.ts (APPEND ONLY): api2Admin + withAdminGrant. Allowed: reads Cron/listcron, ZoneEdit/fetchzone_records; changes Cron/add_line, Cron/edit_line, ZoneEdit/add_zone_record, ZoneEdit/edit_zone_record, each ONLY inside withAdminGrant(exact key) which only serverAdmin.ts opens. remove_line / remove_zone_record / every other function: refused (tests).
- base44/mcp/config.json: two tool entries server_cron, server_dns (annotations as htaccess)
- base44/entities/BridgeLog.jsonc: action enum + cron, dns
- tests/serverAdmin.test.ts

Points to review:
1. Cron command text is the dangerous part (code runs on the server). Layers: Claude signed-in session only; edit/add need expected_sha256 of the whole crontab (stale = refused); exact-line match for edit; max 40 lines; no delete; command is one line <=1000 chars, no secret-looking text, and refuses pipe-to-shell, base64 -d, eval, rm -rf, /dev/tcp, nc, chmod 777, crontab -r. This is a second layer, not a sandbox.
2. Fail-closed logging: a BridgeLog BEFORE row (full previous crontab/zone text + the change) is written first; if it fails nothing changes. AFTER row written after read-back. A cron edit that does not read back is edited back (tested).
3. DNS: domain must be main/addon/parked of this account (DomainInfo), not a subdomain; types A/AAAA/CNAME/TXT only; A may only point at 173.254.31.20; name must be the domain or under it; record type and name cannot change on edit; CNAME cannot share a name; zone base sha required; zone read back after.
4. DNS nameserver lookup = read-only public DNS-over-HTTPS (cloudflare-dns.com) for an account domain only. Only new outbound host.
5. No secret is read or returned; same CPANEL_TOKEN as the rest of the Bridge. cPanel API token must have Cron and Zone Editor rights; if not, calls fail with a clear error and nothing changes.

After PASS: copy /tmp/spo4 files over base44/ + tests/, checkpoint (call twice), needs_you publish; Edwin Publishes and reconnects the Bridge connector so server_cron, server_dns and htaccess get permission.
