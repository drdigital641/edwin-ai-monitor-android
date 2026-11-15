# Bridge drop folder for bot files (Edwin, 15 Nov 2026)

Bots hand files to Claude through the Bridge. Bots never upload to Bluehost and never publish. Claude reviews each drop and publishes it through the normal Bridge path.

## Where the files go
- `~/bluehost-bridge-private/drops/<drop id>/<path>` on Bluehost.
- This folder is outside `public_html`, so it is never served, never web-reachable and never indexable. The cPanel choke point already lets the Bridge write only there or through the guarded site write.
- Each drop is one site and one job, for example `maisoninteriordesign.sg` / `grand-dunman`.

## Bot routes (HTTPS POST, JSON body)
Base: `https://blue-bridge-pilot.base44.app/functions/`

| Route | What it does |
|---|---|
| `bridgeDropPut` | Store ONE file in the drop, or `"action": "ready"` to say the drop is complete |
| `bridgeDropStatus` | This key's drops: file names, sizes, sha256, who and when, state. Never returns file content |

Header on every call: `X-Bridge-Key: <bot drop key>`

### Put one file
```json
{ "site": "maisoninteriordesign.sg", "job": "grand-dunman",
  "path": "images/grand-dunman-v4-hero.webp",
  "content_base64": "<base64 of the file>",
  "sha256": "<optional: sha256 hex of the file, checked on arrival>" }
```
Text files (.json .md .txt) may send `"content": "<text>"` instead of `content_base64`.

### Mark the drop ready
```json
{ "site": "maisoninteriordesign.sg", "job": "grand-dunman", "action": "ready", "note": "v4 set complete: 1 JSON + 9 WebPs" }
```

### Example (bash, key read from a file, never typed into a chat)
```bash
KEY="$(cat ~/.pageone/bridge-drop-key)"
B64="$(base64 < hero.webp | tr -d '\n')"
curl -sS https://blue-bridge-pilot.base44.app/functions/bridgeDropPut \
  -H "X-Bridge-Key: $KEY" -H "Content-Type: application/json" \
  -d "{\"site\":\"maisoninteriordesign.sg\",\"job\":\"grand-dunman\",\"path\":\"images/hero.webp\",\"content_base64\":\"$B64\"}"
```

## Rules the Bridge enforces (self-tested)
- Types: `.json .webp .jpg .jpeg .png .md .txt` only. Everything else is refused (.htaccess, .php, .phtml, .cgi, .sh, .exe, .js, .html, .svg, .zip, .tar.gz, .7z...).
- Names: letters, digits, `-` and `_`, exactly one dot (so `a.php.jpg` is refused), at most 2 folders deep. No `../`, `./`, absolute paths, `~`, URLs, backslashes or `%`.
- Names that look secret are refused (secret, password, token, api-key, credentials, id_rsa, env, htaccess, wp-config).
- Images must really be images (file header checked) and must not contain script or PHP. Text must be valid UTF-8 with no binary bytes, no `<?php`, `<script>` or `#!/`, and nothing that looks like a password, key or token. JSON must parse.
- Size: images 1 MB each, JSON 512 KB, .md/.txt 256 KB, 40 files and 15 MB per drop, 10 open drops per key.
- Expiry: a drop expires 7 days after it opens and its files are wiped. Claude clears a drop after the page is live and checked.
- Log: every call is logged with the key's label (never the key), and every stored file records who dropped it and when.

## The bot key
- Scope `drop`: only `bridgeDropPut` and `bridgeDropStatus`. Every other Bridge tool answers 403 (no read or write of live files, no list, no sync, no restore, no key making). The Claude tools (drop_list, drop_read, drop_publish, drop_clear) refuse every API key, including the full ChatGPT key.
- Edwin makes it himself: Bridge Connect page, Site keys, pick "Bot drop folder (no site access)", label it (e.g. "Maison bot"), tap Copy, then save it on the bot's computer as below. The key is shown once and the Bridge stores only its hash.

### Putting the key on the bot's computer without any chat
Right after tapping Copy on the Connect page, on the bot's computer:
- Mac: `mkdir -p ~/.pageone && pbpaste > ~/.pageone/bridge-drop-key && chmod 600 ~/.pageone/bridge-drop-key`
- Windows PowerShell: `New-Item -ItemType Directory -Force $HOME\.pageone | Out-Null; Get-Clipboard | Set-Content -NoNewline $HOME\.pageone\bridge-drop-key`
- Linux: `mkdir -p ~/.pageone && xclip -o -selection clipboard > ~/.pageone/bridge-drop-key && chmod 600 ~/.pageone/bridge-drop-key`
Then copy something else so the key leaves the clipboard. The bot reads the file (or set an environment variable `BRIDGE_DROP_KEY` from it). If the key is ever exposed, revoke it on the Connect page and make a new one.

## Claude's side (signed-in session only)
`drop_list` -> `drop_read` (text content or image size, plus a tamper check that the stored bytes equal what was dropped) -> build the page from live files (read_live_file) -> `drop_publish` with `dry_run` first. Each file keeps its type, stays inside the drop's site folder (for Maison: pageone `preview/maison-interior-design`), and goes through writeFile: HOLD, blocked names, live guard, `expected_sha256` for every replace, private backup, byte-exact readback. Then `drop_clear`.
