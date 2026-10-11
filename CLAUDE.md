# Edwin's website architecture (permanent rules)

**The master rules live in Base44** (`BridgeGuide` records in the Bluehost Bridge app) and
are shared with ChatGPT. At the start of every website conversation, call the bridge's
`get_instructions` tool and follow what it returns; it wins over this file if they differ.
This file is the fallback summary.

Owner: Edwin, who owns the Bluehost cPanel account `sgmodde1`.

## The six websites (all on `sgmodde1`)

| Bridge key | Domain                 | Name                 |
|------------|------------------------|----------------------|
| `sggarage` | sggarage.com           | SG Garage            |
| `cleanic`  | cleanicdetailing.com   | Cleanic Detailing    |
| `alicia`   | aliciaongproperty.com  | Alicia Ong Property  |
| `danny`    | dannychuafinancial.com | Danny Chua Financial |
| `sofacare` | sofacaresg.com         | SofaCare SG          |
| `pageone`  | pageonesingapore.com   | Page One Singapore   |

Page One Singapore also gets articles from an hourly publisher inside the bridge
(`publishPageOneArticles`), which writes under `articles/`, `images/articles/` and the
site's sitemap/llms files. Check its recent runs (`PageOnePublishRun`) before changing those files by hand.

## How every website change is made

Claude → Base44 → Bluehost Bridge → Bluehost server (`sgmodde1`) → live website.

- Use the **bluehost-bridge** connector (`https://blue-bridge-pilot.base44.app/api/mcp`)
  to list, read, edit, write and restore site files. Changes go live straight away.
- The bridge is the Base44 app **Bluehost Bridge** (app id `6ac6d47b4ec84148578914c7`).
  Change the bridge itself through the Base44 connector.
- Every write is backed up first and logged (`BridgeLog`). Use the restore tool to roll back.
- The bridge blocks secrets (`wp-config.php`, `.env`, keys), `.htaccess` and server-side
  code (`.php` etc.). Don't try to work around this; tell Edwin when a change needs one of those.
- If the bluehost-bridge connector isn't loaded in a session, say so. Don't switch to
  another way of changing the live sites.

## Working together with ChatGPT

ChatGPT uses the same bridge through a private Custom GPT (setup: `CHATGPT_BRIDGE_SETUP.md`).
The bridge is the shared notice board between the two AIs:

1. At the start of every website job, call `sync_status`. Tell Edwin about notes left for
   Claude, recent ChatGPT changes on the site you're about to touch, and any claims.
2. If ChatGPT has claimed the site or file, don't work around it. Tell Edwin who claimed it,
   why, and until when. The bridge also refuses the change while the claim lasts.
3. Before a bigger job (several files, a page rewrite), `claim_work` that site or file with a
   short purpose, and release it when done. Claims end on their own after at most 2 hours.
4. When you finish, `post_note` to `chatgpt` (or `anyone`): what changed, which files,
   anything left to do or check.
