"""Live-domain build mode shared by the AutoSEO client builders (Edwin, 13 Nov 2026).

    python3 autoseo-clients/<site>/src/build.py          -> site/       preview copy for autoseo.my/preview/<site>/ (noindex)
    python3 autoseo-clients/<site>/src/build.py --live   -> site-live/  live domain build: canonical/og/sitemap/llms on
                                                                         live_site_url, base path /, robots index,follow

The flag is passed to check.py through the AUTOSEO_LIVE env var, so the same checks run on the live output.
The preview build is unchanged. Nothing here deploys anything.
"""
import os
import sys

FLAG = "AUTOSEO_LIVE"


def is_live():
    if "--live" in sys.argv:
        os.environ[FLAG] = "1"
    return os.environ.get(FLAG) == "1"


def apply(cfg, root):
    """Rewrite the loaded config for a live build and return the output folder."""
    if not is_live():
        return root / "site"
    live = cfg.get("live_site_url") or ""
    if not live.startswith("https://") or not live.endswith("/") or "autoseo.my" in live:
        raise SystemExit("live build: live_site_url must be the client's own https domain ending in /")
    cfg.update(site_url=live, base_path="/", preview=False)
    return root / "site-live"
