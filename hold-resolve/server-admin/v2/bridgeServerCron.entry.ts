import { bridgeTool } from '../../shared/handler.ts';
import { cronAdd, cronEdit, cronList } from '../../shared/serverAdmin.ts';
import { BridgeError } from '../../shared/bridgeOps.ts';

// SERVER CRON (Edwin 20 Nov 2026): list, add, edit one line of this account's crontab. Claude's signed-in session only; no delete.
// Every changing call stores the exact before/after text privately and writes a before-record and an after-record to BridgeLog (shared/serverAdmin.ts).
export default bridgeTool('cron', async (body, ctx) => {
  switch (body.op) {
    case 'list': return await cronList();
    case 'add': return await cronAdd(body, ctx);
    case 'edit': return await cronEdit(body, ctx);
    default: throw new BridgeError('op must be list, add or edit');
  }
}, { sessionOnly: true, needsSite: false });
