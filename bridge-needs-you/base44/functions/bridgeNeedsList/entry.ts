import { bridgeTool } from '../../shared/handler.ts';
import { listNeedsYou } from '../../shared/needsYou.ts';

// NEEDS YOU read tool (15 Nov 2026): Grok Bot checks an item is real and still open. Read-only: open items, or one by id.
// Works with a "needs" key (Connect page, Grok Bot key), a full key or a signed-in admin. No secrets, no file contents.
export default bridgeTool('needs_read', (body, ctx) => listNeedsYou(ctx.base44, body), { needsSite: false });
