# Connecting ChatGPT to the Bluehost Bridge

ChatGPT connects to the **same** bridge Claude uses. Both share one set of backups,
one change log and the same safety rules. There is no second copy to keep in sync.

## 1. Add the bridge to ChatGPT

1. In ChatGPT, open **Settings → Apps** and turn on **Developer mode**.
2. Click **Create app**.
   - Name: `Bluehost Bridge`
   - MCP server URL: `https://blue-bridge-pilot.base44.app/api/mcp`
   - Authentication: **OAuth**
3. Click **Create**. A Bluehost Bridge sign-in page opens. Sign in with Edwin's
   admin account and approve. The bridge only works for admin accounts.
4. In a new chat, turn on the Bluehost Bridge app from the composer (**+ → Developer mode**,
   or the tools menu), then ask: "List my websites." You should see six sites.

If the tool list looks out of date after the bridge is updated, refresh the app in
ChatGPT's settings. ChatGPT caches the list of tools.

## 2. Paste these instructions into ChatGPT

Put this in a ChatGPT **Project's instructions**, or in **Settings → Personalization →
Custom instructions**, so ChatGPT follows the same rules as Claude:

```
I am Edwin. I own the Bluehost cPanel account sgmodde1, which hosts six websites:

- sggarage  = sggarage.com          (SG Garage)
- cleanic   = cleanicdetailing.com  (Cleanic Detailing)
- alicia    = aliciaongproperty.com (Alicia Ong Property)
- danny     = dannychuafinancial.com (Danny Chua Financial)
- sofacare  = sofacaresg.com        (SofaCare SG)
- pageone   = pageonesingapore.com  (Page One Singapore)

Every website change goes: AI -> Base44 -> Bluehost Bridge -> Bluehost server -> live site.
Use only the Bluehost Bridge app to change my websites. Changes go live immediately.

How to work with the bridge:
- Start with list_sites. Use list_files and read_file to look before changing anything.
- For small changes use edit_file (find and replace). old_text must match exactly once.
- To replace a whole file or upload an image use write_file. To overwrite an existing
  file, pass expected_sha256 from your latest read_file. If the write is refused because
  the file changed, read it again and redo the change. Never guess the sha256.
- Every change is backed up first and verified. To undo, use list_backups and
  restore_backup.
- The bridge blocks password files, .htaccess and server code (.php etc.). Do not try to
  get around this. Tell me when a change needs one of those.
- Page One Singapore gets new articles from an hourly publisher that writes articles/,
  images/articles/, sitemap and llms files. Don't hand-edit those without asking me.
- After a change, tell me which site and file changed and give me the live URL.
- If the Bluehost Bridge app isn't available in the chat, say so. Don't use any
  other way to change my live websites.
```

## Notes

- Claude and ChatGPT can both use the bridge at the same time. If both try to change the
  same file, the second change is refused because the file changed since it was read. Nothing gets
  silently overwritten.
- Every change made through ChatGPT shows up in the bridge's change log (`BridgeLog`)
  under the signed-in account.
- To cut off ChatGPT's access, delete the app in ChatGPT's Apps settings.
