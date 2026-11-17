import { bridgeTool } from '../../shared/handler.ts';
import { runnerSitemap } from '../../shared/runner.ts';

// GROKBOT RUNNER (18 Nov 2026): rebuild sitemap.xml + llms.txt for pages already on the site, then IndexNow for them.
// POST https://blue-bridge-pilot.base44.app/functions/bridgeRunnerSitemap  body { site, paths: [..], dry_run? }
export default bridgeTool('runner_sitemap', (body, ctx) => runnerSitemap(body, ctx));
