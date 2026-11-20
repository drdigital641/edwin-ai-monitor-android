# server_cron / server_dns v2 (fixes for the FAIL on c5edfe2)

Base = Bridge app main. Patched copy: Bridge sandbox /tmp/spo4. NOT saved. This folder holds every changed or new file.

Files: serverAdmin.ts (new), bridgeServerCron.entry.ts + bridgeServerDns.entry.ts (new, bridgeTool sessionOnly:true needsSite:false), main-patches.diff (cpanel.ts append, bridgeOps.ts append, BridgeLog enum +cron +dns), mcp-config-entries.json (two entries appended to base44/mcp/config.json tools.functions; no existing line changed), serverAdmin.test.ts, test-output.txt.
Unchanged from main (cmp): shared/htaccess.ts, shared/handler.ts, functions/bridgeHtaccess/entry.ts. So the .htaccess tool needs only a connector reconnect.

Fix map:
1 HIGH allowlist: commandProblem(). Trailing "> /dev/null 2>&1" removed once; the rest must match [A-Za-z0-9 _./~=:,@+-] only (so no ; & | ` $ ( ) < > quotes backslash %), no "..", and must start with an approved program. Applied to the new line AND the existing line (existing lines outside the allowlist are listed read-only and refused for edit, 403). Approved programs: (a) ~/.acme.sh/acme.sh or /home*/sgmodde1/.acme.sh/acme.sh with flags --cron --home <path> --list --info --renew --deploy --deploy-hook <name> -d/--domain <domain> (every flag and value checked; --renew-hook, --pre-hook, --post-hook, --reloadcmd, --install-cert and others refused); (b) nice -n N /bin/bash /home*/sgmodde1/bin/crawler-extract.sh (the one other job path I can name from cron-extract-plan.md; EDWIN TO CONFIRM; the Bluehost :17/:29 publisher lines and the Bridge hourly job are NOT on the list because I have not seen their text: they stay read-only until Edwin confirms them from the redacted list).
2 HIGH redaction: redact() masks query strings, token/key/pass/secret/auth/cred/sig key=value, Authorization/Bearer/Basic, --token/--key style flags, hex runs >=24 and any 32+ run of base64 characters. cronList output, base_sha256 (hash of the REDACTED lines) and every BridgeLog row use it. The exact before and after text goes to ~/bluehost-bridge-private/server-admin/ (putAdminRecord in bridgeOps.ts, private zone, 0700); BridgeLog gets path + sha256 + the allowlisted (secret-free) change only. If the private record cannot be stored, nothing changes.
3 pushed here with test output.
4 MED race: edit re-reads the keyed list after the before-record and refuses (409) unless the raw line at that position still equals the line being replaced.
5 MED log size: a before-row over 7500 characters is refused (must=true); the full text lives in the private record, the log never holds it.
6 MED email: TXT refused if it starts v=spf1 / v=dmarc1 / v=dkim1 (any case), or the name starts _dmarc. / _domainkey or contains ._domainkey.; names whose first label is mail, webmail, autodiscover, autoconfig, cpanel, webdisk, whm, cpcalendars, cpcontacts refused for every type.
7 LOW AAAA dropped entirely (tool enum, validator).
8 LOW CNAME only on www.<domain> pointing at <domain>; apex CNAME refused.
9 LOW edit of an A record whose old value is not 173.254.31.20 needs expected_old_value equal to that old value (409 otherwise).
10 kept: no NS/MX/SOA edit, no delete (remove_line / remove_zone_record not in the allowlist, tested), domain limited to main/addon/parked of this account, A only to 173.254.31.20, zone base sha + read-back, fail-closed before-record, read-only DoH, session-only (every API key gets 403, tested through the real entry points).

Tests: see test-output.txt (serverAdmin 5/5 plus the existing suites). deno check --no-lock on serverAdmin.ts is clean (the entry files import the SDK package which the sandbox cannot resolve, same as every other function).

First jobs after save: acme.sh. The cron tool cannot delete, so to drop the hourly :17 deploy loop the line is edited to a harmless allowlisted no-op or Edwin removes it in cPanel > Cron Jobs (one tap). If acme.sh already stored the deploy hook per domain (it does after any successful --deploy), the existing --cron line redeploys on real renewal by itself. autotex: nameservers op first; if the zone is not on this server the tool refuses and Edwin gets the exact A record for the outside registrar.
