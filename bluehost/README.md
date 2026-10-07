# Bluehost publishing for all five websites

Bluehost has no MCP connector, and cloud agents can't open SSH connections
themselves (their network only allows HTTPS). So **GitHub Actions does the SSH
work for them**:

```
agent edits sites/<site>/…  →  push to main  →  "Bluehost - Deploy" runs  →  rsync over SSH  →  live site
```

* The SSH key is stored once as an encrypted GitHub secret. Agents never see it.
  Neither do chats or logs.
* Any agent with access to this repo (Claude, Base44 via GitHub, etc.) can publish.
* Every deploy backs up the live folder first (`~/deploy-backups/<site>/` on Bluehost; the last 10 are kept).
* `wp-config.php`, `.env`, uploads and other files in `excludes.txt` are never downloaded, overwritten or deleted.

## One-time setup (about 10 minutes, works from a phone browser)

### 1. Turn on SSH and create a key in Bluehost
1. Log in to Bluehost and go to **Advanced → cPanel**. The SSH settings may also be under
   **Websites → Settings → SSH Access**. Turn **SSH access on**.
2. In cPanel, open **SSH Access → Manage SSH Keys → Generate a New Key**.
   * Key name: `github-deploy`, Key type: **RSA 4096** (or Ed25519 if offered).
   * Set a passphrase you'll keep (you'll store it as a secret below).
3. Back on Manage SSH Keys, find `github-deploy` under **Public Keys** and choose **Manage → Authorize**.
4. Under **Private Keys**, choose **View/Download** for `github-deploy` and copy the whole text,
   including the `-----BEGIN` and `-----END` lines.
5. Note your **server hostname** and **cPanel username**. Both are listed in the cPanel
   "General Information" sidebar. You can also use your main domain as the hostname.

### 2. Store the secrets in GitHub
On github.com open this repository and go to **Settings → Environments → New environment**.
Name it `bluehost`. Add these **environment secrets**:

| Secret | Value |
|---|---|
| `BLUEHOST_HOST` | server hostname, or your main domain |
| `BLUEHOST_USER` | cPanel username |
| `BLUEHOST_SSH_KEY` | the private key text from step 1.4 |
| `BLUEHOST_SSH_PASSPHRASE` | the passphrase from step 1.2 (skip it if you set none) |

Optional: on the environment, add a **variable** `BLUEHOST_PORT` only if Bluehost
tells you SSH uses a port other than 22.

Optional extra safety: in the same environment, turn on **Required reviewers** and add yourself.
Each deploy then waits for you to approve it from the GitHub app on your phone.

### 3. Test and lock the connection
1. Go to **Actions → Bluehost - Check connection → Run workflow**.
2. Open the run. Copy the host key lines from the **Server host key** step into a new
   secret, `BLUEHOST_KNOWN_HOSTS`. GitHub will then refuse to connect if anyone
   impersonates your server.
3. The **Login test and website folders** step lists each site's folder. Put those folders into
   `bluehost/sites.json`, replacing each `CHANGE_ME`. An agent can do this from the run log.

### 4. Pull each site into the repo
Go to **Actions → Bluehost - Pull site into repo**, pick a site and run it. Repeat for each site.
The live files are committed under `sites/<site>/`, so agents edit what is really online.

## Day-to-day use (for people and agents)

* **Edit a site:** change files in `sites/<site>/`, then commit and push to `main`. The changed sites deploy automatically.
* **Refresh from live first**, if someone changed files directly on Bluehost: run *Bluehost - Pull site into repo*.
* **Preview a deploy:** run *Bluehost - Deploy* with `dry_run` on. The log lists every file that would change.
* **Remove files from the server:** run *Bluehost - Deploy* with `dry_run` off and `delete_removed` on.
  Excluded files stay protected.
* **Roll back:** each deploy log prints its backup path. Restore it with cPanel File Manager
  (extract the `.tgz` into the site folder). An agent can also re-deploy the previous commit with `git revert`.

## WordPress sites: read this

The Check workflow labels WordPress folders. For those sites, **pages and posts live in
the database, not in files**. File deploys only cover themes, plugins and custom code. To edit
page content, use the WordPress REST API with an **Application Password**. It runs over
HTTPS, so agents can call it directly:

1. In WordPress, go to **Users → Profile → Application Passwords**, add one named `claude-agent` and copy it.
2. Store it as an environment secret in your Claude cloud environment settings (never in chat):
   `WP_<SITE>_URL`, `WP_<SITE>_USER`, `WP_<SITE>_APP_PASSWORD`.

## Security notes
* Use a dedicated key for this purpose only. To revoke all agent access, go to cPanel →
  Manage SSH Keys → **Deauthorize** `github-deploy`. Nothing else is affected.
* Never commit `wp-config.php` or passwords. `excludes.txt` blocks them in both directions.
* GitHub masks secret values in logs, and workflows never print them.
