# SG Commercial Fitout: AI concept of the day (daily run, 00:00 SGT, scheduled task "SG Commercial Fitout concept of the day")

Goal: one new dated AI interior concept on the homepage hero; the previous one moves into the gallery
(/design-concepts/concept-of-the-day/). Edwin asked for this on 24 Oct 2026. Preview only until go-live.

Steps (stop and report if any step fails; never invent text that the image does not show):
1. Clone (single clone, ~10 min timeout):
   git clone --depth 1 --filter=blob:none --no-checkout --branch site-assets https://github.com/drdigital641/edwin-ai-monitor-android /home/user/edwin-ai-monitor-android
   git -C /home/user/edwin-ai-monitor-android sparse-checkout set --no-cone /site-assets/rc-design-build/ /pageone-site/clients/rc-design-build/
   git -C /home/user/edwin-ai-monitor-android checkout site-assets
   (pip install pillow if missing)
2. Today's image (Base44 MCP run_command, appId 6adc39a33be36ae8a3ed0782 "R&C Image Studio"):
   curl -s -X POST https://base44.app/api/apps/6adc39a33be36ae8a3ed0782/functions/dailyConcept -H 'Content-Type: application/json' -d '{}'
   It returns {date, space, theme, url} and makes at most one image per Singapore date (repeat calls return the same one).
   Then run_command: curl -s "<url>" | base64 -w0  -> the output is saved to a file; decode it to /tmp/daily.img.
3. Look at the image. If it shows any readable brand name, logo, trademark or copied artwork, do NOT publish: log "rejected: logo visible" and stop (Edwin rule, 24 Oct 2026: only original AI ideas and his own photos, nothing copied from other companies).
   Otherwise write the entry. Write /tmp/entry.json:
   {"date": "<date>", "space": "<space>", "title": "<5-8 words>", "summary": "<40-60 words describing only what is visible, plain Singapore English>",
    "ideas": ["4 short design ideas visible in the image"], "alt": "<what the image shows> (AI design concept)"}
   No prices, brands, claims, or "our project" wording: it is an AI design concept.
4. python3 /home/user/edwin-ai-monitor-android/pageone-site/clients/rc-design-build/tools/daily_publish.py /tmp/daily.img /tmp/entry.json
   It commits the image + rebuilt site to branch site-assets and prints SITE_SHA (skips if the date already exists).
5. Bluehost Bridge sync_from_github: {site: "pageone", ref: SITE_SHA, source_path: "pageone-site/clients/rc-design-build/site",
   base_path: "preview/rc-design-build"}. Re-run once if any file is skipped.
6. After go-live only (commercialfitout.sg serves the site): IndexNow the homepage and the gallery URL (key 7d4c2a9e1f6b8035c4e2a7d9b1f60c38).
7. Log one line to /mnt/project-files/rc-design-build/daily-log.md if the mount exists (date, title, SITE_SHA, result).

LIVE since 25 Oct 2026 on https://commercialfitout.sg (same Bluehost folder preview/rc-design-build). After the sync,
check the homepage on the domain shows today's date and IndexNow / and /design-concepts/concept-of-the-day/ from the
Base44 sandbox (key 7d4c2a9e1f6b8035c4e2a7d9b1f60c38). build.py must stay LIVE = True.
