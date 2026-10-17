# Page One Singapore: visitor walkthrough gaps (9 Oct 2026)

Walked the live site as a new visitor on a phone (iPhone size): homepage → menu → every page →
website checker → 12 chat questions → pricing calculator → sign-up → top-up → contact form.
No script errors on any page; homepage loads in under 2 s.

Priority: **P0** blocks revenue · **P1** loses leads or trust · **P2** polish.

| # | Pri | Area | Gap | Proposed fix | Needs Edwin? |
|---|-----|------|-----|--------------|--------------|
| 1 | P0 | Sign-up | Every sign-up and Boost top-up fails ("Online sign-up is being set up"). Stripe key not configured. | Edwin provides a test restricted key → Claude stores it, creates the webhook, runs a test-card sign-up. | **Yes: rk_test key** |
| 2 | P0 | Sign-up | When checkout fails, the visitor is lost: their name/email/business isn't saved anywhere. Also no follow-up if someone abandons Stripe checkout. | Save every sign-up attempt as a Lead *before* redirecting to Stripe; email Edwin "sign-up started"; on failure show "We've saved your details, Edwin will send you a payment link." | No |
| 3 | P1 | Sign-up | Visitor waits ~6 s before the error appears (the new auto-retry treats "not set up" as a temporary error). | Return a non-retryable status for "not configured". | No |
| 4 | P1 | Offer clarity | Nobody can tell what the S$20 pays for **every month** after the site is built. The chat improvised ("ongoing updates to your business information"), which isn't a stated promise. | Edwin defines the monthly deliverables (e.g. hosting, monthly check, X article/month, GBP post?) → add a "Every month you get" block to home, Get Found, sign-up, FAQ and chat facts. | **Yes: what's included monthly** |
| 5 | P1 | Trust | No phone number, address, UEN or company name anywhere. Our own checker flags pageonesingapore.com for "no one-tap contact". SG SMEs expect a number before paying. | Show business name + UEN in footer/terms; add a phone (call-only is fine until WhatsApp is ready). | **Yes: UEN, registered name, phone** |
| 6 | P1 | Checker | Facebook/Instagram pages are scored like websites (facebook.com/… got 48, instagram 30): misleading, and a missed sales moment. | Detect social/marketplace URLs → "That's a Facebook page, not a website. Google can't rank it like a site. Get Found builds you one for S$20/month." | No |
| 7 | P1 | Checker | Visitors with **no website** (the main target) have nothing to do: typing "my bakery" just errors. | Add "No website yet?" link under the checker → explains Get Found + sign-up / chat. | No |
| 8 | P1 | Checker | Results vanish when the visitor leaves; no lead captured. | "Email me this report" (email field) → saves Lead, emails them the report + emails Edwin. | No |
| 9 | P1 | Checker | Mobile speed test always says "busy" (Google rejects key-less requests). | Add a free Google PageSpeed API key as a Base44 secret. | **Yes: create key (5 min), or Claude walks you through** |
| 10 | P1 | Chat | Refused a Chinese question ("Please ask in English"). | Reply in the visitor's language (English, 中文, Malay). | No |
| 11 | P1 | Chat | Interested visitors can't leave details inside the chat; they're sent to /contact/ and many won't go. | Chat asks "Want Edwin to contact you?" and collects name + email/phone in the chat window → Lead + email. | No |
| 12 | P1 | Chat | Invented specifics when unsure: Google account access "connects through secure standard processes"; asked for examples, didn't link the 5 live client sites. | Add onboarding facts (what the client provides, how Google access is granted, e.g. as manager invite) and client site links to the chat facts. | **Yes: confirm onboarding steps** |
| 13 | P2 | Homepage | No "How it works / what happens after you pay" on the homepage (only on sign-up page). | Add the 3-step strip (Check → Sign up → Live in 7 days) above pricing. | No |
| 14 | P2 | Success page | /signup/success/ says "Payment received" to anyone who opens the link; doesn't confirm the payment. | Verify the Stripe session on load; show the real plan/amount, or a neutral message. | No (after #1) |
| 15 | P2 | Sample report | CTA still says "Get your free visibility check" (old wording); the sample is the fictional "Ah Seng Aircon". | Update CTA text; keep clearly labelled as a sample. | No |
| 16 | P2 | FAQ | Missing: what do I need to provide, do you need my passwords, who owns the content, what happens each month. | Add 4 FAQs once #4 and #12 are answered. | After #4/#12 |
| 17 | P2 | Articles | Only 1 article on the blog. Looks thin to visitors. | Article writer is on a 2-day cadence; consider daily for the first month. | Your call |
| 18 | P2 | Layout | Sign-up Boost picker wraps "4" onto its own line on phones; chat button overlaps the "4,290+ searches" chip on the hero. | Tighten picker to one row; nudge chip/launcher. | No |
| 19 | P2 | Admin | Leads, chats, checks and subscribers live only in Base44 entities: no simple dashboard for Edwin. | Small private dashboard page (leads, chats, checks, sign-ups this week). | Your call |
