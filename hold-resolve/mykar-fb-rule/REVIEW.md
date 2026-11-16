# SPO review: MyKar fb-posts.json standing rule (liveGuard.ts)

Verdict: PASS WITH CHANGES. Do not save until fix 1 is in. Fix 2 is recommended.

Diff sha256 32077e51...153c (copy in this folder). Tests in /tmp/mk: 121 passed, 1 failed (guardOverrides1115 fixtures, same failure as base; the 121st pass is my throwaway test, removed). /tmp/drop.json (sha 81f7aa8f...2854) passes mykarFbProblem (returns null).

## What I checked

- Scope: branch needs site === 'pageone' && rel === exact path && publisher !== true. rel is the raw string. relProblem runs first and rejects `//`, `./`, `..`, trailing `/`. Tried FB-posts.json, trailing space, `%00` suffix: all refused with "needs an override". Other site, other folder, root path, publisher route: refused (covered by the new tests). Case differences cannot match.
- Callers: bridgeOps.writeFile passes publisher only for publisher writes; bulkWrite passes none (tool route, intended). Both go through the same liveGuard call.
- Protections kept: the branch sits after relProblem, NEVER (.htaccess etc.), unknown-live refusal, absent and no-change returns. The Bridge secret checks and base-sha compare-and-swap are in writeFile and are not touched. The branch only returns null or a refusal, so it can only loosen the guard for that one file. It skips the later overrides lookup, which is fine because rel is a fixed .json.
- Live renderer (mykar.my/df.js?v=7): every field goes through esc() (& < > " ' to numeric entities) and width/height through `+`. Images and permalinks are only placed in attributes, so nothing is exploitable today. The renderer also hides captions matching its own HIDE regex (broader than the guard's).

## Findings

1. MEDIUM (fix before save): the raw-text checks run before JSON.parse, so JSON escapes bypass them. Proven: caption `<img src=x onerror=alert(1)>` returns null (accepted). It decodes to live markup text. `only RM1` is caught only because the price regex runs after parse. The renderer escapes today, so this is defense in depth, but the stated rule is "no markup" and a renderer change would make it live XSS. Same for `fbcdn` (harmless here: the image regex blocks it).
   Fix: run the markup and fbcdn tests on the decoded strings as well as the raw text. Real file has no backslashes, so it still passes.

   After the `let d` JSON.parse line, add:
   ```ts
   const strs: string[] = []; const walk = (v: unknown) => { if (typeof v === 'string') strs.push(v); else if (v && typeof v === 'object') Object.values(v).forEach(walk); }; walk(d);
   if (strs.some((s) => /fbcdn|<|>|javascript\s*:|\bon[a-z]+\s*=/i.test(s))) return 'markup, fbcdn or javascript: text is not allowed (after JSON decoding)';
   ```
   And reject escapes outright (simplest, stricter): after the raw `<|>` check add
   `if (/\\u/i.test(text)) return 'JSON \\u escapes are not allowed';`
   (Emoji and CJK are written as raw UTF-8 by the file, so this does not hurt the real file.)

2. LOW (recommended): the guard's price list is narrower than the renderer's HIDE (missing loan, pinjaman, MYR, OTR, \d+k, 万, ansuran, per month, /month, sebulan, sahaja, 分期, 贷款). The renderer hides those anyway, so no customer-facing risk, but the file could carry them. Copy the renderer list into MYKAR_FB_PRICE to keep one rule. Check the real file first: its captions contain none of them.
   Error text says caption "(must be empty)"; reword to "remove the price wording or leave the caption empty".

3. INFO: a refusal blocks the whole weekly file for one caption, so the weekly job must blank that caption and retry. "Only" as a word will be refused every time it appears (e.g. "only" in Deepavali greetings); acceptable and matches the renderer.

4. INFO: the file uses absolute /images/fb/... while the live page uses relative images/fb/.... Works on mykar.my (docroot is the folder). The guard does not check that the images exist; upload the .webp files first, or the carousel shows broken images.

5. INFO: raw regex `\bon[a-z]+\s*=` and `>` will refuse harmless captions such as "Online = easy" or "->". Fails closed; fine.

## Applied (16 Nov 2026, before save)
- Must-fix 1 applied: `if (/\\u/i.test(text)) return 'JSON \\u escapes are not allowed ...'` right after the raw markup check, plus a test.
- Recommended: added loan(s), MYR, OTR, 贷款 to MYKAR_FB_PRICE (left out \d+k and 万, which would block normal km/text captions); error text now "(price captions must be left empty)".
- mykar-fb-rule.diff in this folder is the reviewed pre-fix diff; the saved version is Bridge git 720ad63, checkpoint 6afa82f21bbc69548892b295 (base d274d09). Tests on the patched copy: 120 passed, 1 pre-existing failure (guardOverrides1115 fixtures, fails on base too). Real drop file sha 81f7aa8f passes.
