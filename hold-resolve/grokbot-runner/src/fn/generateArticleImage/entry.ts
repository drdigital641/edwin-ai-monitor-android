import { bridgeTool } from '../../shared/handler.ts';
import { generateArticleImage } from '../../shared/runnerImage.ts';

// GROKBOT RUNNER (18 Nov 2026): one Base44 image -> hero, card and og:image files on Bluehost (new files only).
// POST https://blue-bridge-pilot.base44.app/functions/generateArticleImage  body { site, slug, prompt, alt?, folder? }
export default bridgeTool('runner_image', (body, ctx) => generateArticleImage(body, ctx), { logs: true });
