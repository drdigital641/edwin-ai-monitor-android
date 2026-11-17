import { bridgeTool } from '../../shared/handler.ts';
import { runnerController } from '../../shared/runner.ts';

// GROKBOT RUNNER (18 Nov 2026): Page One Controller Copy fix issues and tap counts (read only) and the article_last_*
// fields, through the Controller's signed runnerFeed. POST .../functions/bridgeRunnerController  body { op, ... }
export default bridgeTool('runner_controller', (body, ctx) => runnerController(body, ctx), { needsSite: false });
