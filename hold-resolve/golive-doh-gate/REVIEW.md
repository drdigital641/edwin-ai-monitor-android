# Go-live DNS gate: DNS-over-HTTPS (23 Nov 2026)

Requested by Edwin (approved 1:31am SGT, 23 Nov 2026) after autoseo.sg was refused:
"REFUSED: apex: resolves to 103.11.189.189, need only 173.254.31.20" while the 3 Vodien nameservers, Google and Cloudflare
all returned 173.254.31.20. Repeated taps then gave 429.

## What changed

**Bluehost Bridge** (`bridge.diff`, checkpoint `6b032af79afe9389d84188b7`, commit 2ad207b)
- `shared/goLive.ts` `domainStatus`: the A/AAAA gate now asks Google DoH (`dns.google/resolve`), then Cloudflare DoH
  (`cloudflare-dns.com/dns-query`, `accept: application/dns-json`), then the runtime's own lookup (`Deno.resolveDns`) only when
  neither DoH answered. Passes when ONE resolver gives apex only 173.254.31.20, www only 173.254.31.20 (CNAME followed) and no AAAA.
  Same rule as before; https check, addon, IndexNow key and every post-flip check are unchanged.
- `status.resolver` = resolver that passed (or the ones asked); a refusal note lists each resolver's answer.
- `shared/goLivePure.ts` `resolveGate` (pure, injected resolvers) + 6 new tests in `tests/goLive.test.ts` (20/20 pass).
- `functions/bridgeGoLive/entry.ts`: comment only, so the function redeploys with the shared change.

**Page One Controller** (`controller.diff`, checkpoint `6b032af8b841f3c30bb45bce`, commit 83131c9)
- `clientSites` checklist DNS step: same Google -> Cloudflare -> local order, resolver list in the note.
- `runGoLive`: 20 s cooldown after a "domain not ready" answer (no Bridge call, nothing written); resolver saved in golive_status.
- `set_status` Live / `golive_run` refusals now answer 200 `{ok:false, error:"Not switched ... : <reason>"}` instead of a bare 409.
- `check` returns `golive_note` (why not live yet); Clients page shows it.
- Clients page + GoLive component: errors show the function's sentence (429 -> "Too many checks in a row..."), Check now has a 20 s tap cooldown.

## Security notes
- No secrets in code. No new write paths. DoH queries carry only the client domain (already public).
- Gate is not loosened: a resolver must give a fully clean answer; mixed answers inside one resolver still refuse;
  the local lookup cannot override a DoH answer.

## Not changed
- Billing, Stripe, client records (other than the AutoSEO.sg go-live itself, which Edwin asked for).
- siteCheck / Websites Overview health checker: they fetch the site through the runtime's resolver (fetch cannot pin an IP),
  so this change does NOT fix the Rasa Sayang stale-DNS score.
