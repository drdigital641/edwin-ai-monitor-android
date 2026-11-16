# Maison daily launch page run (Edwin 16 Nov 2026, PERMANENT)

Each day build exactly ONE TODO project as a full-concept page in the locked template, then re-sort the hub.
Scheduled task "Maison daily launch page (2:17pm SGT)" runs this file in a fresh session. Model: Sonnet (lead) with
Haiku helpers for checks; Opus only if a quality gate fails twice.

Files (all in /mnt/project-files/maison-interior-design/): MAISON-LAUNCH-TEMPLATE.md (the locked template + quality bar),
MAISON-LAUNCH-QUEUE.md (generated view). Source of order/status: repo branch claude/project-thread-5pg280,
`maison-launch/launch-queue.json` (+ `sort_hub.py`, `queue_md.py`). Generator: `maison-expand/gen2/` on branch
claude/project-thread-6s51oo (cf7fa7f). Work on a new branch from 6s51oo and copy maison-launch/ in, or merge both.

## Steps
0. If today's SGT date already has a "built:" line in daily-log.md (this folder), stop: one page per day.
   If yesterday's page is waiting on a guard Publish (step 6), finish that one first and build nothing new today.
1. Pick: first project in launch-queue.json with status TODO and a v4 set (`v4_set` not null). Every TODO above it
   without a set goes into the log as "waiting for images: <names>".
2. Read live through the Bridge: the project's current page, the v4 folder listing, `/nlp-expand.css`, one DONE page
   (header/footer/CSS ?v= must match live). Live wins over any repo copy.
3. Facts: only official sources (HDB project page / Layout Ideas / brochure; developer brochure or SGX/press release).
   Developer, TOP, unit mix, areas: official only, linked in Sources. Keep every existing FAQ question verbatim (add only).
4. Add the project to gen2 `data.py` (variant: BTO/HDB, condo/EC/landed, commercial; add the variant to gen2.py first if
   missing, shared parts stay in gen2). Build that one slug. Images: Base44 only, never OpenAI or stock.
5. Gate against the quality bar in MAISON-LAUNCH-TEMPLATE.md section 6 (sections, words, FAQ = JSON-LD, CTAs + data-ref,
   p1-cta.js, tracking/cta_check.py, 390px no overflow). Fail = do not deploy, log "flagged: <reason>", blocked alert.
6. Deploy: commit, Bridge sync_from_github dry run, then real sync with base_sha256 (auto-backup path goes in the log).
   A LIVE GUARD 409 (title/meta/JSON-LD change) is expected on existing pages: add a one-time GUARD_OVERRIDES entry for
   the new sha in Bridge bridgeConfig.ts following the review-before-save rule (diff under hold-resolve/<job>/, SPO review),
   save, checkpoint (create_checkpoint twice), send needs_you type "publish", and stop; the next run re-sends the identical
   sync after Edwin Publishes, then removes the override (checkpoint + publish alert). Never work around the guard.
7. Live check: page 200 on maisoninteriordesign.sg, 390 + 1280 screenshots, one ?p1test=1 WhatsApp tap shows as a
   CtaClick test row (Controller sandbox can reach the domain; this container cannot).
8. Mark DONE: set status "DONE" in launch-queue.json, run `queue_md.py` (rewrites MAISON-LAUNCH-QUEUE.md here) and
   `sort_hub.py <live hub> launch-queue.json <out>` on the live /new-launches/index.html read just now; commit, sync with
   base_sha256. The project moves into the top group automatically. sitemap.xml/IndexNow come from the Bridge auto step
   (back off on 429).
9. Log one line in daily-log.md: "<SGT date> built: <slug> | backup <path> | tap test ok | waiting for images: ...".
10. ONE Bridge needs_you alert: done (live URL, model line) or blocked (reason). Plus publish for any checkpoint.
