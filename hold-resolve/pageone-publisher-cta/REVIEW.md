# Review before save: Page One publisher template keeps the CTA tap tracker (17 Nov 2026)

Bridge app 6ac6d47b4ec84148578914c7, file `base44/shared/pageoneArticles.ts` (template only; no auth, no new network calls, no secrets).
Thread "Add tap tracker to Page One site". Rule: Bridge backend diffs get SPO review BEFORE the Base44 save
(the hourly :25 publisher runs sandbox code, so a save goes live at the next run).

## Why
17 Nov 22:21-22:25 UTC: /p1-cta.js?v=eb07c660 + data-cta were added to all 79 pageonesingapore.com pages (Edwin's approval 6:07am SGT).
The 23:27 UTC publisher run (PageOnePublishRun 6afb91ae9010c13ddc863585, written 33) re-rendered the 30 article pages + /articles/
hub from this template, which has no p1-cta.js tag, no data-cta and no "Leave us a Google review" footer, so it stripped them again.
Every new or re-rendered article page now fails the CTA TAP GATE rule. Non-article pages (49) are not touched by the publisher and keep the tracker.

## Change (4 exact replacements, each occurs once)
1. line ~565 footer link
   - `<p><a class="footer-wa" href="${WA_LINK}"`
   + `<p><a data-cta="footer_whatsapp" class="footer-wa" href="${WA_LINK}"`
2. line ~597 before `<div class="wrap footer-bottom">` insert the review footer block that live pages carry (byte-identical to live /signup/success/):
   ```
   <style>
/* Google review footer button (2026-11-13) */
.p1-foot-review{margin:16px 0 0}
.p1-foot-review a{
  display:inline-flex;align-items:center;justify-content:center;box-sizing:border-box;
  min-height:44px;min-width:44px;padding:10px 18px;
  border:1.5px solid currentColor;border-radius:999px;
  text-decoration:none!important;font-weight:700;line-height:1.25;color:inherit
}
.p1-foot-review a:hover{opacity:.88}
footer.foot .p1-foot-review{margin:12px 0 8px}
</style>
<p class="p1-foot-review"><a href="/review.html?business=pageone" target="_blank" rel="noopener">Leave us a Google review</a></p>
   ```
3. line ~605 float button
   - `<a class="wa-float" id="wa-float" href="${WA_LINK}"`
   + `<a data-cta="whatsapp_link" class="wa-float" id="wa-float" href="${WA_LINK}"`
4. line ~609 scripts
   - `<script src="/main.js?v=${JS_VERSION}" defer></script>`
   + `<script src="/main.js?v=${JS_VERSION}" defer></script>` + newline + `<script src="/p1-cta.js?v=eb07c660" defer></script>`
5. line ~697 article CTA
   - `<a class="btn btn-ghost" href="${WA_LINK}"`
   + `<a data-cta="article_cta" class="btn btn-ghost" href="${WA_LINK}"`

This makes the publisher output identical to the Claude night-run renderer (night-writers/pageone/tools/render_pageone_article.mjs)
and to the 49 tracked live pages. data-cta values equal what main.js already reports, so dashboard labels do not change and
p1-cta.js leaves wa.me taps to main.js (no double count; see pageone-cta/p1-cta.js on branch claude/project-thread-0igmer).

## Effect after save
The next :25 run re-renders the 31 article/hub pages once (each gets the tag, data-cta and review footer back), then writes 0 again.
Rollback: revert the 5 replacements and save; the next run re-renders without them.
