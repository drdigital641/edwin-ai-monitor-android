// SERVER ADMIN: CRON + DNS for this account only (Edwin 20 Nov 2026, "keep the new tools narrow, log every call, require a
// backup or before-and-after record"). Claude's signed-in session only (every API key refused by bridgeTool sessionOnly).
// Cron : list, add, edit ONE line. No delete, no other Cron function. Edit names the exact existing line and the sha256 of the
//        whole crontab it was based on; a stale base is refused. Add refuses past 40 lines.
// DNS  : zones/nameservers/read, add and edit A/AAAA/CNAME/TXT records, only in a zone of this account's own domains
//        (DomainInfo), only A records that point at this server, no delete, never NS/MX/SOA/other types. Edit names the zone's
//        sha256 base. Nameserver lookup is a read-only public DNS-over-HTTPS query for an account domain.
// Every change: (1) BridgeLog row with the BEFORE record written first (if that fails nothing changes), (2) the guarded cPanel call,
// (3) read back and compare, (4) BridgeLog row with the AFTER record. A cron edit that does not read back as asked is edited back.
import { api2Admin, checkResult, uapi, withAdminGrant } from './cpanel.ts';
import { BridgeError, sha256 } from './bridgeOps.ts';
import { secretContentReason } from './bridgeConfig.ts';

export const SERVER_IP = '173.254.31.20';
export const MAX_CRON_LINES = 40;
type Ctx = { base44?: any; email?: string | null };
const enc = (s: string) => new TextEncoder().encode(s);

// ---------- logging ----------
async function logRow(base44: any, action: 'cron' | 'dns', row: Record<string, unknown>, detail: unknown, must = false) {
  const entities = base44?.asServiceRole?.entities;
  try {
    if (!entities?.BridgeLog) throw new Error('BridgeLog not available');
    await entities.BridgeLog.create({ action, ...row, detail: JSON.stringify(detail).slice(0, 8000) });
  } catch (e) {
    if (must) throw new BridgeError('Refused: the before-record could not be written to BridgeLog (' + (e instanceof Error ? e.message : String(e)).slice(0, 120) + '). Nothing was changed.', 503);
  }
}

// ---------- cron ----------
export type CronLine = { minute: string; hour: string; day: string; month: string; weekday: string; command: string };
const FIELD = /^(\*|\d{1,2})(-\d{1,2})?(\/\d{1,2})?(,(\*|\d{1,2})(-\d{1,2})?(\/\d{1,2})?)*$/;
const FIELD_MAX: Record<string, number> = { minute: 59, hour: 23, day: 31, month: 12, weekday: 7 };
// Hard refusals for command text (a second layer, not a sandbox: only Edwin's signed-in Claude session can reach this tool).
const BAD_COMMAND = [/\|\s*(sudo\s+)?(ba|z|da)?sh\b/i, /base64\s+(-d|--decode)/i, /\beval\b/i, /\brm\s+-[a-z]*r[a-z]*f?\b/i, /\/dev\/(tcp|udp)\//i, /\bcrontab\s+-r\b/i, /\bchmod\s+(-R\s+)?[0-7]*777\b/i, /\b(nc|ncat|netcat)\b/i];

export function cronProblem(l: Partial<CronLine>): string | null {
  for (const k of Object.keys(FIELD_MAX) as (keyof CronLine)[]) {
    const v = l[k];
    if (typeof v !== 'string' || !FIELD.test(v)) return k + ' is not a valid cron field';
    for (const n of v.match(/\d+/g) || []) if (Number(n) > (FIELD_MAX[k] ?? 59) && !v.includes('/')) return k + ' value ' + n + ' is out of range';
  }
  const c = l.command;
  if (typeof c !== 'string' || !c.trim()) return 'command is required';
  if (c.length > 1000) return 'command is longer than 1000 characters';
  if (/[\0\r\n]/.test(c)) return 'command must be one line';
  if (secretContentReason(c)) return 'command looks like it carries a password, key or token';
  const bad = BAD_COMMAND.find((r) => r.test(c));
  if (bad) return 'command contains something this tool never schedules (' + String(bad).slice(0, 40) + ')';
  return null;
}
export const cronText = (l: CronLine) => [l.minute, l.hour, l.day, l.month, l.weekday, l.command].join(' ');
export async function cronBase(lines: CronLine[]) { return await sha256(enc(lines.map(cronText).join('\n'))); }

async function readCron(): Promise<CronLine[]> {
  const rows = await api2Admin('Cron', 'listcron', {});
  return rows.filter((r) => r && typeof r.command === 'string').map((r) => ({
    minute: String(r.minute), hour: String(r.hour), day: String(r.day), month: String(r.month), weekday: String(r.weekday), command: String(r.command),
  }));
}

export async function cronList() {
  const lines = await readCron();
  return { lines: lines.map((l, i) => ({ n: i + 1, ...l, text: cronText(l) })), count: lines.length, base_sha256: await cronBase(lines) };
}

function entryOf(body: any): CronLine {
  const e = { minute: body?.minute, hour: body?.hour, day: body?.day, month: body?.month, weekday: body?.weekday, command: typeof body?.command === 'string' ? body.command.trim() : body?.command };
  const bad = cronProblem(e as any);
  if (bad) throw new BridgeError('cron: ' + bad);
  return e as CronLine;
}
const params = (l: CronLine) => ({ minute: l.minute, hour: l.hour, day: l.day, month: l.month, weekday: l.weekday, command: l.command });

export async function cronAdd(body: any, ctx: Ctx) {
  const entry = entryOf(body);
  const before = await readCron();
  const baseSha = await cronBase(before);
  if (body.expected_sha256 !== baseSha) throw new BridgeError('STALE: the crontab changed since you listed it (or expected_sha256 is missing). List it again.', 409);
  if (before.length >= MAX_CRON_LINES) throw new BridgeError('The crontab already has ' + before.length + ' lines; this tool does not add past ' + MAX_CRON_LINES, 409);
  if (before.some((l) => cronText(l) === cronText(entry))) throw new BridgeError('That exact line already exists', 409);
  const at = new Date().toISOString(), actor = ctx.email || null;
  await logRow(ctx.base44, 'cron', { ok: true, actor, before_sha256: baseSha }, { kind: 'cron', op: 'add', phase: 'before', at, actor, before: before.map(cronText), new_line: cronText(entry) }, true);
  await withAdminGrant('Cron/add_line', () => api2Admin('Cron', 'add_line', params(entry)));
  const after = await readCron();
  const expected = [...before.map(cronText), cronText(entry)].sort().join('\n');
  const good = after.map(cronText).sort().join('\n') === expected;
  const afterSha = await cronBase(after);
  await logRow(ctx.base44, 'cron', { ok: good, actor, before_sha256: baseSha, after_sha256: afterSha, ...(good ? {} : { error: 'cron add did not read back as asked' }) }, { kind: 'cron', op: 'add', phase: 'after', at, actor, after: after.map(cronText) });
  if (!good) throw new BridgeError('The line was sent but the crontab does not read back as asked. Check it in cPanel > Cron Jobs. Before-record is in BridgeLog.', 502);
  return { added: cronText(entry), count: after.length, before_sha256: baseSha, base_sha256: afterSha, before: before.map(cronText) };
}

export async function cronEdit(body: any, ctx: Ctx) {
  const entry = entryOf(body);
  const existing = typeof body?.line === 'string' ? body.line.trim() : '';
  if (!existing) throw new BridgeError('line (the exact existing cron line to replace, as listed in "text") is required');
  const before = await readCron();
  const baseSha = await cronBase(before);
  if (body.expected_sha256 !== baseSha) throw new BridgeError('STALE: the crontab changed since you listed it (or expected_sha256 is missing). List it again.', 409);
  const hits = before.map((l, i) => ({ l, i })).filter((x) => cronText(x.l) === existing);
  if (hits.length !== 1) throw new BridgeError('The line must match exactly one existing cron line; matched ' + hits.length, 409);
  if (cronText(hits[0].l) === cronText(entry)) throw new BridgeError('The new line is identical to the existing one', 409);
  const at = new Date().toISOString(), actor = ctx.email || null;
  await logRow(ctx.base44, 'cron', { ok: true, actor, before_sha256: baseSha }, { kind: 'cron', op: 'edit', phase: 'before', at, actor, before: before.map(cronText), replaces: existing, with: cronText(entry) }, true);
  // cPanel numbers lines from 1 in listcron order; linekey is that line's key as listcron reports it.
  const keyed = await api2Admin('Cron', 'listcron', {});
  const rowsK = keyed.filter((r) => r && typeof r.command === 'string');
  const linekey = String(rowsK[hits[0].i]?.linekey ?? '');
  if (!linekey) throw new BridgeError('cPanel did not give a line key for that line; nothing was changed', 502);
  await withAdminGrant('Cron/edit_line', () => api2Admin('Cron', 'edit_line', { linekey, ...params(entry) }));
  const after = await readCron();
  const want = before.map((l, i) => (i === hits[0].i ? entry : l)).map(cronText);
  const good = after.map(cronText).join('\n') === want.join('\n');
  let rolledBack = false, rollbackError: string | null = null;
  if (!good) {
    try {
      const k2 = await api2Admin('Cron', 'listcron', {});
      const mine = k2.find((r) => r && typeof r.command === 'string' && cronText({ minute: String(r.minute), hour: String(r.hour), day: String(r.day), month: String(r.month), weekday: String(r.weekday), command: String(r.command) }) === cronText(entry));
      if (mine) { await withAdminGrant('Cron/edit_line', () => api2Admin('Cron', 'edit_line', { linekey: String(mine.linekey), ...params(hits[0].l) })); rolledBack = true; }
    } catch (e) { rollbackError = e instanceof Error ? e.message : String(e); }
  }
  const finalLines = good ? after : await readCron().catch(() => after);
  const afterSha = await cronBase(finalLines);
  await logRow(ctx.base44, 'cron', { ok: good, actor, before_sha256: baseSha, after_sha256: afterSha, ...(good ? {} : { error: 'cron edit did not read back as asked' }) },
    { kind: 'cron', op: 'edit', phase: 'after', at, actor, after: finalLines.map(cronText), rolledBack, rollbackError });
  if (!good) throw new BridgeError('The crontab did not read back as asked. ' + (rolledBack ? 'The old line was put back.' : 'Automatic put-back did not run or failed (' + (rollbackError || 'no match') + ').') + ' Before-record is in BridgeLog.', 502);
  return { replaced: existing, with: cronText(entry), count: after.length, before_sha256: baseSha, base_sha256: afterSha, before: before.map(cronText) };
}

// ---------- DNS ----------
export type DnsRecord = { line: number; name: string; type: string; ttl: number; value: string };
const HOST = /^(?=.{1,253}$)([a-z0-9_]([a-z0-9_-]{0,61}[a-z0-9_])?\.)+[a-z]{2,63}$/;
const IPV4 = /^(25[0-5]|2[0-4]\d|1?\d?\d)(\.(25[0-5]|2[0-4]\d|1?\d?\d)){3}$/;
const IPV6 = /^[0-9a-f:]{2,39}$/i;
const EDITABLE = new Set(['A', 'AAAA', 'CNAME', 'TXT']);
const dot = (s: string) => String(s || '').toLowerCase().replace(/\.$/, '');

export async function accountDomains(): Promise<{ domain: string; type: string }[]> {
  const data = checkResult(await uapi('DomainInfo', 'domains_data', {}), 'DomainInfo domains_data');
  const out: { domain: string; type: string }[] = [];
  const add = (d: any, type: string) => { const n = typeof d === 'string' ? d : d?.domain; if (n) out.push({ domain: dot(String(n)), type }); };
  add(data?.main_domain, 'main');
  for (const d of data?.addon_domains || []) add(d, 'addon');
  for (const d of data?.sub_domains || []) add(d, 'sub');
  for (const d of data?.parked_domains || []) add(d, 'parked');
  return out;
}
async function ownDomain(input: unknown): Promise<string> {
  const d = dot(String(input || ''));
  if (!HOST.test(d)) throw new BridgeError('domain is not a valid domain name');
  const list = await accountDomains();
  if (!list.some((x) => x.domain === d && x.type !== 'sub')) throw new BridgeError('"' + d + '" is not a main, addon or parked domain of this account; DNS tool refused', 403);
  return d;
}
export function dnsProblem(domain: string, r: { name?: unknown; type?: unknown; value?: unknown; ttl?: unknown }): string | null {
  const type = String(r.type || '').toUpperCase();
  if (!EDITABLE.has(type)) return 'type must be A, AAAA, CNAME or TXT (never NS, MX, SOA or others)';
  const name = dot(String(r.name || ''));
  if (name !== domain && !name.endsWith('.' + domain)) return 'name must be ' + domain + ' or end with .' + domain;
  if (!HOST.test(name)) return 'name is not a valid host name';
  const v = String(r.value ?? '');
  if (type === 'A') { if (!IPV4.test(v)) return 'A value must be an IPv4 address'; if (v !== SERVER_IP) return 'A records may only point at this server (' + SERVER_IP + ')'; }
  if (type === 'AAAA' && !IPV6.test(v)) return 'AAAA value must be an IPv6 address';
  if (type === 'CNAME' && !HOST.test(dot(v))) return 'CNAME value must be a host name';
  if (type === 'TXT' && (!v || v.length > 500 || /[\0\r\n]/.test(v) || secretContentReason(v))) return 'TXT value must be 1-500 plain characters with no secret';
  const ttl = Number(r.ttl ?? 14400);
  if (!Number.isInteger(ttl) || ttl < 300 || ttl > 86400) return 'ttl must be 300-86400';
  return null;
}
const recText = (r: DnsRecord) => [dot(r.name), r.ttl, r.type, r.value].join(' ');
async function readZone(domain: string): Promise<DnsRecord[]> {
  const rows = await api2Admin('ZoneEdit', 'fetchzone_records', { domain });
  return rows.filter((r) => r && (r.type || r.Type)).map((r) => ({
    line: Number(r.Line ?? r.line), name: String(r.name ?? ''), type: String(r.type ?? r.Type).toUpperCase(), ttl: Number(r.ttl ?? 0),
    value: String(r.address ?? r.record ?? r.cname ?? r.txtdata ?? r.exchange ?? '').replace(/^"|"$/g, ''),
  })).filter((r) => Number.isFinite(r.line));
}
async function zoneBase(rs: DnsRecord[]) { return await sha256(enc(rs.map(recText).sort().join('\n'))); }
const valueParam = (type: string, v: string) => (type === 'CNAME' ? { cname: dot(v) + '.' } : type === 'TXT' ? { txtdata: v } : { address: v });

export async function dnsZones() {
  const list = await accountDomains();
  return { domains: list.filter((d) => d.type !== 'sub'), server_ip: SERVER_IP };
}
export async function dnsRead(domainIn: unknown) {
  const domain = await ownDomain(domainIn);
  let records: DnsRecord[];
  try { records = await readZone(domain); } catch (e) { throw new BridgeError('No editable zone for ' + domain + ' on this server (' + (e instanceof Error ? e.message : String(e)).slice(0, 200) + '). Its DNS is probably hosted elsewhere: run op nameservers.', 404); }
  return { domain, records: records.map((r) => ({ ...r, text: recText(r) })), base_sha256: await zoneBase(records) };
}
// Read-only public DNS-over-HTTPS lookup (NS and A) for a domain of this account, to see where its DNS is hosted.
export async function dnsNameservers(domainIn: unknown) {
  const domain = await ownDomain(domainIn);
  const ask = async (type: string) => {
    const res = await fetch('https://cloudflare-dns.com/dns-query?name=' + encodeURIComponent(domain) + '&type=' + type, { headers: { accept: 'application/dns-json' }, signal: AbortSignal.timeout(10_000) });
    const j: any = await res.json();
    return { status: j?.Status, answers: (j?.Answer || []).map((a: any) => String(a.data)) , authority: (j?.Authority || []).map((a: any) => String(a.data)).slice(0, 3) };
  };
  const [ns, a] = await Promise.all([ask('NS'), ask('A')]);
  let zoneHere = false; try { zoneHere = (await readZone(domain)).length > 0; } catch { /* no zone on this server */ }
  return { domain, nameservers: ns.answers, a_records: a.answers, ns_status: ns.status, a_status: a.status, authority: ns.authority, zone_on_this_server: zoneHere, server_ip: SERVER_IP };
}

export async function dnsAdd(body: any, ctx: Ctx) {
  const domain = await ownDomain(body?.domain);
  const bad = dnsProblem(domain, body);
  if (bad) throw new BridgeError('dns: ' + bad);
  const type = String(body.type).toUpperCase(), name = dot(body.name), ttl = Number(body.ttl ?? 14400), value = String(body.value);
  const before = await readZone(domain);
  const baseSha = await zoneBase(before);
  if (body.expected_sha256 !== baseSha) throw new BridgeError('STALE: the zone changed since you read it (or expected_sha256 is missing). Read it again.', 409);
  if (before.some((r) => dot(r.name) === name && r.type === type && r.value === value)) throw new BridgeError('That exact record already exists', 409);
  if (type === 'CNAME' && before.some((r) => dot(r.name) === name)) throw new BridgeError('A CNAME cannot share a name with another record', 409);
  const at = new Date().toISOString(), actor = ctx.email || null;
  await logRow(ctx.base44, 'dns', { ok: true, actor, site: domain, before_sha256: baseSha }, { kind: 'dns', op: 'add', phase: 'before', at, actor, domain, before: before.map(recText), new_record: [name, ttl, type, value].join(' ') }, true);
  await withAdminGrant('ZoneEdit/add_zone_record', () => api2Admin('ZoneEdit', 'add_zone_record', { domain, name: name + '.', type, class: 'IN', ttl: String(ttl), ...valueParam(type, value) }));
  const after = await readZone(domain);
  const good = after.some((r) => dot(r.name) === name && r.type === type && r.value === (type === 'CNAME' ? dot(value) : value)) && after.length === before.length + 1;
  const afterSha = await zoneBase(after);
  await logRow(ctx.base44, 'dns', { ok: good, actor, site: domain, before_sha256: baseSha, after_sha256: afterSha, ...(good ? {} : { error: 'dns add did not read back as asked' }) }, { kind: 'dns', op: 'add', phase: 'after', at, actor, domain, after: after.map(recText) });
  if (!good) throw new BridgeError('The record was sent but the zone does not read back as asked. Check Zone Editor. Before-record is in BridgeLog.', 502);
  return { domain, added: [name, ttl, type, value].join(' '), records: after.length, before_sha256: baseSha, base_sha256: afterSha };
}

export async function dnsEdit(body: any, ctx: Ctx) {
  const domain = await ownDomain(body?.domain);
  const bad = dnsProblem(domain, body);
  if (bad) throw new BridgeError('dns: ' + bad);
  const line = Number(body?.line);
  const before = await readZone(domain);
  const baseSha = await zoneBase(before);
  if (body.expected_sha256 !== baseSha) throw new BridgeError('STALE: the zone changed since you read it (or expected_sha256 is missing). Read it again.', 409);
  const target = before.find((r) => r.line === line);
  if (!target) throw new BridgeError('No record on that line', 404);
  if (!EDITABLE.has(target.type) || target.type !== String(body.type).toUpperCase()) throw new BridgeError('Only an existing A, AAAA, CNAME or TXT record may be edited, and its type cannot change', 403);
  if (dot(target.name) !== dot(body.name)) throw new BridgeError('The record name cannot change; add a new record instead', 403);
  const type = target.type, name = dot(body.name), ttl = Number(body.ttl ?? target.ttl), value = String(body.value);
  const at = new Date().toISOString(), actor = ctx.email || null;
  await logRow(ctx.base44, 'dns', { ok: true, actor, site: domain, before_sha256: baseSha }, { kind: 'dns', op: 'edit', phase: 'before', at, actor, domain, before: before.map(recText), line, replaces: recText(target), with: [name, ttl, type, value].join(' ') }, true);
  await withAdminGrant('ZoneEdit/edit_zone_record', () => api2Admin('ZoneEdit', 'edit_zone_record', { domain, line: String(line), name: name + '.', type, class: 'IN', ttl: String(ttl), ...valueParam(type, value) }));
  const after = await readZone(domain);
  const good = after.length === before.length && after.some((r) => dot(r.name) === name && r.type === type && r.value === (type === 'CNAME' ? dot(value) : value));
  const afterSha = await zoneBase(after);
  await logRow(ctx.base44, 'dns', { ok: good, actor, site: domain, before_sha256: baseSha, after_sha256: afterSha, ...(good ? {} : { error: 'dns edit did not read back as asked' }) }, { kind: 'dns', op: 'edit', phase: 'after', at, actor, domain, after: after.map(recText) });
  if (!good) throw new BridgeError('The edit was sent but the zone does not read back as asked. Check Zone Editor; the old record is in the BridgeLog before-record.', 502);
  return { domain, replaced: recText(target), with: [name, ttl, type, value].join(' '), before_sha256: baseSha, base_sha256: afterSha };
}
