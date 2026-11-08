# Facebook carousel data (mykar.my homepage, "Latest from MyKar")

Weekly refresh: replace `fb-posts.json` and the WebPs in `../images/fb/` (same names the JSON points at),
publish `data/fb-posts.json` + `images/fb/` to the site, then rebuild and publish the EN homepage so the
server-rendered cards (the crawlable text) match. Until the homepage is rebuilt, df.js re-renders the cards from the new JSON.

## Standing caption rule (Edwin, 8 Nov 2026)
A caption with a price, RM amount, rebate, monthly payment (e.g. 月供), loan figure or the word "only"
is never shown. That card shows the photo, date and "View on Facebook" link only, like a post with no caption.
Enforced in code, not in the data: `FB_HIDE` in build.py and `HIDE` in df.js (keep the two patterns identical).
Never write, translate or edit captions. Nothing may load from facebook.com or fbcdn: images are self-hosted.

## Standing card order rule (Website Manager, 8 Nov 2026)
The order in fb-posts.json is the order on the page. The first card is always a car or showroom photo.
Close-up selfie posts and TikTok/link re-shares go last; the rest stay newest first.
The code also moves any post with "type": "link" to the end (build.py fb_section, df.js), but choosing
the lead photo and placing selfies last is done in the JSON. When the JSON changes, change its "updated"
value too, so df.js re-renders cards in browsers that still hold the old homepage.
