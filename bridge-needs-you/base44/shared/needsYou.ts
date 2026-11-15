// NEEDS YOU list (Edwin 15 Nov 2026 10:33am SGT): steps only Edwin (or a server-level helper) can do.
//   publish: a Base44 Publish (Bridge, Page One Controller, SgGarage Controller or any app) with its checkpoint id.
//   server:  a step the Bridge cannot do (.htaccess, PHP, cPanel, DNS, domain verification) with the file or setting.
// Adding a NEW item POSTs one small JSON notice to Grok Bot (secret GROKBOT_WEBHOOK_URL, sender key GROKBOT_WEBHOOK_KEY).
// Rules: a duplicate of an open item sends nothing; nothing else (progress, done, list) ever sends a notice; the URL and
// key are never logged, stored, echoed or returned (errors keep only the HTTP status). Items hold short plain text only:
// no file contents, no credentials. Marking done needs what was checked on live and the site re-check.
import { secrets } from 'base44:runtime';
import { BridgeError } from './bridgeOps.ts';
import { secretContentReason } from './bridgeConfig.ts';

const db = (base44: any) => base44.asServiceRole.entities;

export const NEEDS_TYPES = ['publish', 'server'] as const;
export type NeedsType = typeof NEEDS_TYPES[number];
export const NEEDS_LIMITS = Object.freeze({ target: 80, ref: 200, summary: 200, why: 600, check: 500, noticesPerHour: 20, timeoutMs: 10_000 });
const ROUTINE_HOST = 'api.anthropic.com';

// Base44 timestamps can lack a zone suffix; they are UTC.
function ts(value: unknown) {
  const s = String(value || '');
  return Date.parse(/[zZ]|[+-]\d\d:?\d\d$/.test(s) ? s : s + 'Z');
}

function secretValues(): string[] {
  return ['GROKBOT_WEBHOOK_URL', 'GROKBOT_WEBHOOK_KEY'].map((k) => secrets.get(k) || '').filter((v) => v.length >= 8);
}

// A 32+ character run of letters/digits that is not a plain hex hash (sha256 / git ids are fine) looks like a token.
function longToken(text: string) {
  return (text.match(/[A-Za-z0-9_+=-]{32,}/g) || []).some((t) => !/^[0-9a-f]+$/i.test(t) && /\d/.test(t) && /[A-Za-z]/.test(t));
}

// Short plain text only. Refuses file contents (markup, code, many lines) and anything that looks like a credential,
// including the webhook URL or key themselves.
export function cleanText(field: string, raw: unknown, max: number, required = true): string {
  if (raw === undefined || raw === null || raw === '') {
    if (required) throw new BridgeError(field + ' is required');
    return '';
  }
  if (typeof raw !== 'string') throw new BridgeError(field + ' must be text');
  const text = raw.replace(/\r/g, '').trim();
  if (required && !text) throw new BridgeError(field + ' is required');
  if (text.length > max) throw new BridgeError(field + ' must be at most ' + max + ' characters (a short what and why, not file contents)');
  if ((text.match(/\n/g) || []).length > 3) throw new BridgeError(field + ' must be a few lines at most (no file contents)');
  if (/<\?php|<\/?(html|head|body|script|style|div|meta)\b|```|^\s*(RewriteRule|RewriteCond|Header\s+set|<IfModule)/im.test(text)) {
    throw new BridgeError(field + ' looks like file contents. Name the file or setting and say what to change instead.');
  }
  if (secretContentReason(text) || secretValues().some((v) => text.includes(v)) || /\bsk-ant-[A-Za-z0-9_-]{10,}/.test(text) || longToken(text)) {
    throw new BridgeError(field + ' looks like it holds a key or token. Name the secret instead of its value.');
  }
  return text;
}

function cleanType(raw: unknown): NeedsType {
  if (!NEEDS_TYPES.includes(raw as NeedsType)) throw new BridgeError('type must be publish or server');
  return raw as NeedsType;
}

function cleanTarget(raw: unknown) {
  const t = cleanText('target', raw, NEEDS_LIMITS.target);
  if (!/^[A-Za-z0-9][A-Za-z0-9 ._()\/-]*$/.test(t)) throw new BridgeError('target is the site or app name, e.g. "Bluehost Bridge" or "commercialfitout.sg"');
  return t;
}

function cleanRef(type: NeedsType, raw: unknown) {
  const r = cleanText(type === 'publish' ? 'checkpoint' : 'ref', raw, NEEDS_LIMITS.ref);
  if (type === 'publish' && !/^[0-9a-f]{24}$/i.test(r)) throw new BridgeError('checkpoint must be the 24-character Base44 checkpoint id');
  return type === 'publish' ? r.toLowerCase() : r;
}

// Same step = same type + target + checkpoint/file, ignoring case and spacing.
export function dedupeKey(type: string, target: string, ref: string) {
  const n = (s: string) => s.toLowerCase().replace(/\s+/g, ' ').trim();
  return [type, n(target), n(ref)].join('|');
}

// What callers (and Grok Bot) see. Nothing secret is ever stored, so nothing secret can show here.
export function needsView(r: any) {
  return {
    id: r.id, type: r.type, target: r.target, ref: r.ref, summary: r.summary, why: r.why || null,
    status: r.status, opened_at: r.opened_at || r.created_date || null, done_at: r.done_at || null,
    live_check: r.live_check || null, site_recheck: r.site_recheck || null,
    notice: r.notice_status || null, notice_http: r.notice_http ?? null, notified_at: r.notified_at || null,
  };
}

// The one notice. Routine API trigger (api.anthropic.com/.../routines/<id>/fire, as Edwin's routine panel shows):
// Bearer token, anthropic-version + beta headers, body {"text": "<notice JSON>"}. Any other https URL: the notice JSON as the
// body with the key as a Bearer token. Exactly one request; never retried automatically (a routine fire has no idempotency
// key, so a retry would start a second session).
export function buildNotice(item: any) {
  return { event: 'needs_you', source: 'bluehost-bridge', id: item.id, type: item.type, target: item.target, ref: item.ref, summary: item.summary };
}

export function noticeRequest(urlRaw: string, key: string, notice: Record<string, unknown>): { url: string; init: RequestInit } {
  let url: URL;
  try { url = new URL(urlRaw); } catch { throw new BridgeError('GROKBOT_WEBHOOK_URL is not a valid URL', 500); }
  if (url.protocol !== 'https:') throw new BridgeError('GROKBOT_WEBHOOK_URL must be https', 500);
  const headers: Record<string, string> = { 'Content-Type': 'application/json', Authorization: 'Bearer ' + key };
  const routine = url.hostname === ROUTINE_HOST && /\/routines\/[^/]+\/fire\/?$/.test(url.pathname);
  if (routine) {
    headers['anthropic-version'] = '2023-06-01';
    headers['anthropic-beta'] = 'experimental-cc-routine-2026-04-01';
  }
  const body = routine ? JSON.stringify({ text: 'Bluehost Bridge NEEDS YOU notice (JSON): ' + JSON.stringify(notice) }) : JSON.stringify(notice);
  return { url: url.toString(), init: { method: 'POST', headers, body, redirect: 'manual' } };
}

// Sends one notice and records only the outcome: sent / failed (HTTP status) / unknown (no answer, may have arrived) /
// not_configured / rate_limited. Never throws, never returns the URL, key or response body.
async function sendNotice(base44: any, item: any) {
  const urlRaw = secrets.get('GROKBOT_WEBHOOK_URL') || '';
  const key = secrets.get('GROKBOT_WEBHOOK_KEY') || '';
  const record = async (fields: Record<string, unknown>) => {
    await db(base44).BridgeNeedsYou.update(item.id, fields).catch(() => {});
    Object.assign(item, fields);
  };
  if (!urlRaw || !key) { await record({ notice_status: 'not_configured' }); return; }
  const hourAgo = Date.now() - 3_600_000;
  const recent: any[] = await db(base44).BridgeNeedsYou.list('-created_date', 100).catch(() => []);
  const sentLastHour = recent.filter((r) => r.id !== item.id && ts(r.notified_at) >= hourAgo).length;
  if (sentLastHour >= NEEDS_LIMITS.noticesPerHour) { await record({ notice_status: 'rate_limited' }); return; }
  let req;
  try { req = noticeRequest(urlRaw, key, buildNotice(item)); } catch (e) { await record({ notice_status: 'failed', notice_error: (e as Error).message }); return; }
  await record({ notice_status: 'sending', notice_attempts: (Number(item.notice_attempts) || 0) + 1 });
  const abort = new AbortController();
  const timer = setTimeout(() => abort.abort(), NEEDS_LIMITS.timeoutMs);
  try {
    const res = await fetch(req.url, { ...req.init, signal: abort.signal });
    await res.body?.cancel().catch(() => {});
    if (res.ok) await record({ notice_status: 'sent', notice_http: res.status, notified_at: new Date().toISOString(), notice_error: null });
    else await record({ notice_status: 'failed', notice_http: res.status, notice_error: 'Grok Bot webhook answered HTTP ' + res.status });
  } catch {
    // Timeout or network error: the request may still have arrived, so it is not resent without confirm.
    await record({ notice_status: 'unknown', notice_error: 'No answer from the Grok Bot webhook (timeout or network error)' });
  } finally {
    clearTimeout(timer);
  }
}

// add: open a new item and send its one notice. An open item for the same step is returned instead (duplicate, no notice).
export async function addNeedsYou(base44: any, body: any, actor: string | null) {
  const type = cleanType(body.type);
  const target = cleanTarget(body.target);
  const ref = cleanRef(type, body.ref ?? body.checkpoint);
  const summary = cleanText('summary', body.summary, NEEDS_LIMITS.summary);
  if (summary.includes('\n')) throw new BridgeError('summary must be one line');
  const why = cleanText('why', body.why, NEEDS_LIMITS.why, false);
  const dedupe_key = dedupeKey(type, target, ref);
  const sameOpen = async () => ((await db(base44).BridgeNeedsYou.filter({ dedupe_key, status: 'open' }, 'created_date', 20)) as any[])
    .sort((a, b) => ts(a.created_date) - ts(b.created_date) || String(a.id).localeCompare(String(b.id)));
  const before = await sameOpen();
  if (before.length) return { added: false, duplicate: true, notice: 'not sent (this step is already open)', item: needsView(before[0]) };
  const row = await db(base44).BridgeNeedsYou.create({
    type, target, ref, summary, ...(why ? { why } : {}), status: 'open', dedupe_key,
    opened_at: new Date().toISOString(), opened_by: actor || 'claude', notice_status: 'pending', notice_attempts: 0,
  });
  // Two adds at the same moment: the oldest row wins, the other is removed before any notice goes out.
  const after = await sameOpen();
  if (after.length > 1 && after[0].id !== row.id) {
    await db(base44).BridgeNeedsYou.delete(row.id).catch(() => {});
    return { added: false, duplicate: true, notice: 'not sent (this step is already open)', item: needsView(after[0]) };
  }
  const item = { ...row };
  await sendNotice(base44, item);
  return { added: true, duplicate: false, notice: item.notice_status, item: needsView(item) };
}

async function getRow(base44: any, id: unknown) {
  if (typeof id !== 'string' || !/^[A-Za-z0-9]{8,40}$/.test(id)) throw new BridgeError('id is required');
  const rows: any[] = await db(base44).BridgeNeedsYou.filter({ id }, '-created_date', 1).catch(() => []);
  if (!rows[0]) throw new BridgeError('No needs-you item with that id', 404);
  return rows[0];
}

// done: only after the step was confirmed on live and the site re-checked. Sends no notice.
export async function markNeedsYouDone(base44: any, body: any, actor: string | null) {
  const row = await getRow(base44, body.id);
  if (row.status === 'done') return { done: true, already: true, item: needsView(row) };
  const live_check = cleanText('live_check', body.live_check, NEEDS_LIMITS.check);
  const site_recheck = cleanText('site_recheck', body.site_recheck, NEEDS_LIMITS.check);
  const fields = { status: 'done', done_at: new Date().toISOString(), done_by: actor || 'claude', live_check, site_recheck };
  await db(base44).BridgeNeedsYou.update(row.id, fields);
  return { done: true, item: needsView({ ...row, ...fields }) };
}

// resend: only for an open item whose notice never arrived (not_configured, rate_limited, failed with an HTTP status).
// 'unknown' (timeout) may already have arrived, so it needs confirm_resend: true.
export async function resendNeedsYou(base44: any, body: any) {
  const row = await getRow(base44, body.id);
  if (row.status !== 'open') throw new BridgeError('This item is done; nothing to send', 409);
  const st = row.notice_status;
  if (st === 'sent') throw new BridgeError('The notice for this item was already delivered; no duplicate is sent', 409);
  if (st === 'sending' || st === 'pending') throw new BridgeError('The notice for this item is being sent now', 409);
  if (st === 'unknown' && body.confirm_resend !== true) throw new BridgeError('The last send got no answer and may have arrived. Check with Grok Bot, then resend with confirm_resend: true', 409);
  const item = { ...row };
  await sendNotice(base44, item);
  return { resent: item.notice_status === 'sent', notice: item.notice_status, item: needsView(item) };
}

// Read-only: open items (or status all/done), or one item by id. No secrets, no file contents.
export async function listNeedsYou(base44: any, body: any) {
  if (body.id !== undefined) return { item: needsView(await getRow(base44, body.id)) };
  const status = body.status ?? 'open';
  if (!['open', 'done', 'all'].includes(status)) throw new BridgeError('status must be open, done or all');
  const limit = Math.min(100, Math.max(1, Math.round(Number(body.limit) || 50)));
  const rows: any[] = await db(base44).BridgeNeedsYou.filter(status === 'all' ? {} : { status }, '-created_date', limit);
  return { status, count: rows.length, items: rows.map(needsView) };
}

export async function manageNeedsYou(base44: any, body: any, actor: string | null) {
  const action = body.action ?? 'add';
  if (action === 'add') return await addNeedsYou(base44, body, actor);
  if (action === 'done') return await markNeedsYouDone(base44, body, actor);
  if (action === 'resend') return await resendNeedsYou(base44, body);
  if (action === 'list') return await listNeedsYou(base44, body);
  throw new BridgeError('action must be add, done, resend or list');
}
