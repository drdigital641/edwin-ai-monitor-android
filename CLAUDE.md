# Notes for agents

## Bluehost websites
The five Bluehost websites (sggarage, clinic, danny, alicia, site5) are published from
`sites/<site>/` by GitHub Actions over SSH. Read `bluehost/README.md` first.
- Cloud agents cannot SSH to Bluehost directly. Always go through the workflows.
- Edit files under `sites/<site>/` and push to `main` to deploy. Pushes that touch only
  `sites/**` do not rebuild the APK.
- Before a large edit, run the "Bluehost - Pull site into repo" workflow so you have the live version.
- Never add `wp-config.php`, `.env` or credentials to the repo.
- For WordPress page or post content, use the WP REST API (see README), not file edits.
