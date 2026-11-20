import { bridgeTool } from '../../shared/handler.ts';
import { dnsAdd, dnsEdit, dnsNameservers, dnsRead, dnsZones } from '../../shared/serverAdmin.ts';
import { BridgeError } from '../../shared/bridgeOps.ts';

// SERVER DNS (Edwin 20 Nov 2026): zones of THIS account's own domains on Bluehost only. Claude's signed-in session only; no delete.
// Every changing call stores the exact before/after zone text privately and writes a before-record and an after-record to BridgeLog (shared/serverAdmin.ts).
export default bridgeTool('dns', async (body, ctx) => {
  switch (body.op) {
    case 'zones': return await dnsZones();
    case 'nameservers': return await dnsNameservers(body.domain);
    case 'read': return await dnsRead(body.domain);
    case 'add': return await dnsAdd(body, ctx);
    case 'edit': return await dnsEdit(body, ctx);
    default: throw new BridgeError('op must be zones, nameservers, read, add or edit');
  }
}, { sessionOnly: true, needsSite: false });
