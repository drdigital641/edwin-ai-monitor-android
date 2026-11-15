import { bridgeTool } from '../../shared/handler.ts';
import { manageNeedsYou } from '../../shared/needsYou.ts';

// NEEDS YOU (15 Nov 2026): add an item (sends the one Grok Bot notice), mark it done after the live check, resend a notice
// that never arrived. Claude's connector (signed-in admin) or a full key only.
export default bridgeTool('needs', (body, ctx) => manageNeedsYou(ctx.base44, body, ctx.email), { needsSite: false });
