# AutoSEO team dashboard: function diffs for Security & Privacy review (21 Nov 2026)

Nothing below is saved. Base44 functions go live on save, so each item waits for SPO OK, then Website Manager OK.
Files: repo branch `claude/project-thread-e2lse6`, folder `autoseo-team-dashboard/spo-diffs/` (commit d6aff4d).

## What is already saved (no function change)
- AutoSEO Admin app (6af5e5cc9383219e49899586) checkpoint **6b00e2b41e948891ae2fe08b**: front end only (public/assets/dash.js + dash.css, src/pages/Admin.jsx, index.html, not-invited screen). New entity **AutoseoBillingPlan** (server-only RLS: no role can read/write; empty).
- The deployed `admin` function is unchanged (deployment b40222fa..., same as 13 Nov). It still only forwards me/clients/save_memo/create_client to the Controller, where the link answers 503 (no public key). So the preview shows "Not connected yet" on every page.
- Controller and AutoSEO Sales Web: no file, entity or record changed (proposals were built and tested in /tmp copies only).

## 1. AutoSEO Admin `base44/functions/admin/entry.ts` (full replacement)
File: `proposed/autoseo-admin/base44/functions/admin/entry.ts`. Type-checks (deno check).
- Gate: Base44 sign-in to this private, invite-only app; role must be admin or user. Non-invited = 401, no data.
- Forwards to the Controller ONLY `me` and `team_clients` (read only). `save_memo` and `create_client` are no longer forwarded (not in v1).
- Billing (`billing_list`, `billing_save`, `billing_handle`): AutoSEO's own records in AutoseoBillingPlan, currency fixed MYR, input checked (24-hex client id, amount 0 to 1,000,000 with 2 decimals, status enum, YYYY-MM-DD dates, end >= start). No Stripe call, no Stripe key read.
- Sales (`sales_data/add/remove/settings`): signed server-to-server call to AutoSEO Sales Web (audience `autoseo-sales`). No PIN or token anywhere.
- Same P-256 key as the Controller link (private key server-only in LinkKey; public key via admin-only `link_public_key`).
- Open point for SPO: billing and sales actions rely on the app's own invite list (Base44 login). The Controller allowlist (AutoseoAdminUser) is checked only for client data. Option: also require a passing Controller `me` before billing/sales (one extra call per action).

## 2. Controller (6ac7f2548a9c3877449e2772): `team_clients` action
File: `2-controller-autoseoLink-team_clients.diff` (3 files: functions/autoseoLink/entry.ts, shared/autoseoAdmin.ts, shared/autoseoLinkPayload.ts). Additive; existing actions untouched.
- Still needs: valid signature + nonce, active AutoseoAdminUser row for the signed email, partner account.
- Scope `teamClients()`: brand AutoSEO, not partner, not billing_only, not duplicate, not dormant, not the autoseo.my own site. Page One rows can never pass (brand filter first).
- Fields `teamRow()`: id, name, step, preview_url (Preview only), live_url (Live only), golive_domain, golive (read only), domain_check {dns_ok, https_ok, at} from the last go-live status check, health, taps {wa, call, other} 30 days, articles, billing_hint ('not_billed' for slug ktech). No phone, notes, memo, emails, owner, Stripe or Page One billing.
- Tests: new tests/teamRow.test.ts (4) + existing autoseoLink/autoseoAdmin tests = 19 passed; deno check clean.
- Optional tightening: drop save_memo/create_client from the Controller's link ACTIONS too, since the dashboard no longer sends them.

## 3. AutoSEO Sales Web (6afc5a60aa13789d675618e9): signed link path
Files: `proposed/sales-web/src/routes/api/sales-web.js` (refactor: the 4 data actions moved into one `act()` used by both paths; /sales page path unchanged), new `src/lib/link-auth.server.js`, new `src/lib/autoseo-link-key.server.js` (public key = null, so OFF, 503), new entity `LinkNonce` (admin-only RLS).
- Signed path only when X-Link-Sig is present: key check (503 if none), 2-minute window, body cap 20 KB, ECDSA verify, one-time nonce, payload `{v:1, aud:'autoseo-sales', actor, action in data|add|remove|settings}`. `login` can never be called over the link. A Controller-audience payload is refused.
- Build OK; 8 link tests pass (no key = 503, good call, replay, tampered body, stale time, wrong audience, login refused).

## Switch-on order (after OK)
1. Save #1 in AutoSEO Admin, then an admin of that app calls `link_public_key` once (signed in as Edwin) to get the PUBLIC key.
2. Save #2 in the Controller with that public key in shared/autoseoLinkKey.ts. Edwin Publishes the Controller.
3. Save #3 in Sales Web with the same public key + LinkNonce entity. Edwin Publishes Sales Web.
4. Edwin Publishes AutoSEO Admin. Staff login URL will be https://auto-seo-admin-49899586.base44.app (Base44 slug; app is not published yet, so Base44 gives no URL today).

## Stripe (Page 2)
No Stripe code is proposed. When AutoSEO's own Stripe is ready: a NEW secret named `AUTOSEO_STRIPE_READ_KEY` in the AutoSEO Admin app, restricted key, read only: Invoices, Customers, Subscriptions, Charges (+ Payment Links write only if Edwin approves link creation). Not STRIPE_LINKGEN_KEY (its purpose is unknown to this thread) and never Page One's key.
