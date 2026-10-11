# Bluehost Bridge in ChatGPT (Custom GPT)

A private Custom GPT that uses the **same** bridge as Claude: the same six sites, backups,
change log and safety rules. Set it up once; after that, open the GPT and talk to it.
It works on web and on the phone, with no Developer mode.

You need three things from the `chatgpt/` folder:

| What | File |
|---|---|
| Instructions | `chatgpt/gpt-instructions.txt` |
| API description (schema) | `chatgpt/bluehost-bridge-openapi.json` |
| Secret key | You make this in step 1. It is never stored in this repo. |

## Step 1: Make the key (Base44)

1. Make a random password of **at least 32 characters** (letters and numbers), for example
   with your phone's password manager. Save it in your password manager.
2. Open the **Bluehost Bridge** app in Base44 → **Dashboard → Secrets** (sometimes shown
   as *Environment variables*) → add a secret:
   - Name: `BRIDGE_API_KEY`
   - Value: the password from step 1
3. Save. Base44 restarts the bridge's functions with the new key. That takes a few seconds.

Until this secret exists, the bridge refuses every key.

## Step 2: Create the GPT (ChatGPT)

1. Go to **chatgpt.com → GPTs (Explore GPTs) → Create**, then open the **Configure** tab.
2. **Name:** `Bluehost Bridge`
3. **Instructions:** paste everything in `chatgpt/gpt-instructions.txt`.
4. Scroll down to **Actions → Create new action**:
   - **Authentication** → *API Key* → Auth type **Custom** → Custom header name
     `X-Bridge-Key` → paste your key → Save.
   - **Schema:** paste everything in `chatgpt/bluehost-bridge-openapi.json`.
     You should see 10 actions: listSites, listFiles, readFile, editFile, writeFile,
     listBackups, restoreBackup, syncStatus, postNote, claimWork.
5. Click **Create** (top right) and choose **Only me**. Don't share this GPT: anyone who
   can use it can change your live websites.

## Step 3: Test

Open the GPT and ask: **"List my websites."** You should see all six sites.
Then try: "Read index.html on danny and tell me the page title."

ChatGPT asks you to confirm each **edit, write and restore**. Reads and listings
run without asking.

## How Claude and ChatGPT stay in sync

They can't talk to each other directly, so the bridge works as their shared notice board:

- **Check in** (`syncStatus`): at the start of every job each AI sees what the other changed
  recently, what the other is working on, and any notes left for it.
- **Claim** (`claimWork`): before a bigger job an AI claims a site or one file for up to
  2 hours. While the claim lasts, the bridge refuses the other AI's changes there. Claims
  end on their own, so nothing stays stuck.
- **Handover note** (`postNote`): when an AI finishes, it leaves a note, e.g. "Updated
  pricing on sofacare. Claude, please check the mobile layout." The other AI sees it at
  its next check-in.

They sync by turns, not live. Each one picks up the other's notes the next time you
give it a task.

If you already created the GPT, update it: open the GPT → **Configure**, replace the
**Instructions** with the new `gpt-instructions.txt`, open the action and replace the
**Schema** with the new `bluehost-bridge-openapi.json`, then **Update**.

## Day to day

- Every change ChatGPT makes is backed up and verified, and it shows up in the bridge's
  change log (`BridgeLog`) as `chatgpt-gpt (API key)`.
- Claude and ChatGPT can work at the same time. If both change the same file, the second
  change is refused until it re-reads the file, so nothing is silently overwritten.
- Very large files can be too big for ChatGPT to read in one go. If that happens, ask
  ChatGPT to edit a specific part, or use Claude for that file.

## Cutting off ChatGPT's access

Change or delete the `BRIDGE_API_KEY` secret in Base44. The old key stops working at
once. Claude's connector is not affected. Put the new key into the GPT's action settings
if you want to keep using it.
