import { bridgeTool } from '../../shared/handler.ts';
import { runnerIndexNow } from '../../shared/runner.ts';

// GROKBOT RUNNER (18 Nov 2026): IndexNow submit for URLs on the site's own domain(s). The Bridge reads the site's key
// file on the server and never returns it. POST .../functions/bridgeRunnerIndexNow  body { site, urls: [..] }
export default bridgeTool('runner_indexnow', (body) => runnerIndexNow(body));
