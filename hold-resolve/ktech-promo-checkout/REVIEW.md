# K Tech promo checkout backend (22 Nov 2026)

New, isolated Base44 app **K Tech Promo Orders** (6b01d098d67ed5a4f0d997a4). Nothing else lives in it; no Page One or
Bridge code or keys. Files: entity KtechOrder (admin-only RLS), fn ktechOrder (public, Origin ktech.my only),
fn ktechStripeWebhook (Stripe-signed only).

SPO review (Sonnet, 22 Nov ~1:30am SGT): first pass FAIL (4 must-fixes: lang prototype keys, unsalted IP hash, spam
rows stored + counted, status action probing/unbound session). All fixed; second pass PASS.

Secrets (names only; values are set by Edwin/Andrew in Base44 -> app -> Settings -> Secrets, never in chat or files):
- KTECH_STRIPE_SECRET_KEY   K Tech's own Stripe secret or restricted key (Checkout Sessions write+read). Turns payment on.
- KTECH_STRIPE_WEBHOOK_SECRET  optional, whsec_ of the webhook endpoint .../functions/ktechStripeWebhook
- KTECH_STRIPE_PAYMENT_URL  alternative to the key: a Stripe Payment Link (qty 1 only unless adjustable quantity is on)
- KTECH_IP_SALT             random string for the rate-limit hash
