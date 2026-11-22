import { bridgeTool } from '../../shared/handler.ts';
import { goLiveOp } from '../../shared/goLive.ts';
import { addNeedsYou } from '../../shared/needsYou.ts';
import { clientsCardOp, pageoneClientsOp } from '../../shared/goLiveClients.ts';

// ONE-SWITCH GO-LIVE (Edwin 20 Nov 2026): Controller "Go live" control. Keys: scope golive (Controller) or Claude's signed-in session.
export default bridgeTool('golive', async (body, ctx) => {
  // 21 Nov 2026 (Edwin, PERMANENT): AutoSEO /clients/ card + launches.json after a switch-on (Controller calls it; no alert of its own).
  if (body.op === 'clients_card') return await clientsCardOp(body);
  // 22 Nov 2026 (Edwin, PERMANENT): pageonesingapore.com /clients/ totals (+ named card for a Page One public client) after every go-live.
  if (body.op === 'pageone_clients') return await pageoneClientsOp(body);
  const r = await goLiveOp(body, ctx);
  if (body.op === 'flip' && !r.refused && !r.partial && !body.no_alert) {
    try {
      await addNeedsYou(ctx.base44, { type: r.ok ? 'done' : 'blocked', thread: 'Go live ' + (r.live ? 'On' : 'Off') + ': ' + body.slug, target: String(body.domain || body.slug).slice(0, 80),
        summary: String(r.detail || '').slice(0, 380), urls: r.live ? ['https://' + body.domain + '/'] : [] }, 'bridge');
    } catch { /* an alert must never change the result */ }
  }
  return r;
}, { needsSite: false, logs: true });
