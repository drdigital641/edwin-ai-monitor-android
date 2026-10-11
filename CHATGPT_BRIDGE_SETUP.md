# Bluehost Bridge in ChatGPT (Custom GPT)

Everything lives in Base44. The **Bluehost Bridge** app holds the rules both AIs follow,
the ChatGPT setup steps, the key generator and the link ChatGPT imports its actions from.
No Developer mode, no MCP.

## Set up ChatGPT (about 5 minutes)

Open the Bluehost Bridge app (`https://blue-bridge-pilot.base44.app`), sign in, tap
**Connect AI**, and stay on the **ChatGPT** tab. It walks you through:

1. **Generate ChatGPT key.** Copy it; it is shown only once.
2. In ChatGPT: **GPTs → Create → Configure**. Name it `Bluehost Bridge` and paste the short
   instructions from the page (copy button).
3. **Actions → Create new action → Import from URL**, paste
   `https://blue-bridge-pilot.base44.app/functions/bridgeOpenapi`, then **Import**.
4. **Authentication → API Key → Custom**, header name `X-Bridge-Key`, paste the key.
5. **Create → Only me.** Ask: "List my websites."

## Where things live

| What | Where in Base44 |
|---|---|
| Rules both AIs follow | `BridgeGuide` records (app data). Edit there; both AIs load them with `getInstructions` / `get_instructions` at the start of each conversation. |
| ChatGPT keys | Connect → ChatGPT tab. Generate, see last use, **Revoke**. Only a fingerprint of each key is stored. |
| Change log | `BridgeLog`, which shows which AI made each change |
| Handover notes / work claims | `BridgeNote` / `BridgeLock` |

The files in `chatgpt/` are copies for reference. Base44 is the source of truth.

## How Claude and ChatGPT stay in sync

They can't talk directly, so Base44 is their shared notice board:

- **Check in** (`syncStatus` / `sync_status`): what the other AI changed recently, what it
  is working on, and notes left for you.
- **Claim** (`claimWork` / `claim_work`): reserve a site or file for up to 2 hours; the
  bridge refuses the other AI's changes there until it ends.
- **Handover note** (`postNote` / `post_note`): what changed and what's left to do.

They sync by turns, not live: each picks up the other's notes when you next give it a task.

## Cutting off ChatGPT

Connect → ChatGPT tab → **Revoke** the key. It stops working at once. Claude is not affected.
