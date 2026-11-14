// SG GARAGE NEVER-WRITE block (14 Nov 2026, "SGG NEVER-WRITE 1114-1110"). PERMANENT and separate from the
// SG Garage HOLD: it applies whether the HOLD is on or off, and it has NO bypass flag. Base44 backend code is live
// as soon as it is saved, so removing it is a code change that needs security review.
// This app never creates, changes, renames, moves or deletes a server-config or server-code file:
// basename .htaccess / .htpasswd / .user.ini / php.ini, or any server-executable extension (PHP family, .cgi, .pl,
// .py, .sh, and .shtml whose server-side includes can run commands), checked case-insensitively after stripping
// trailing dots and spaces (".htaccess.", "x.PHP ", "x.cgi..."). The same extension in the middle of the name
// ("shell.php.jpg", "run.cgi.txt") is refused too, because Apache can run such files with some handler setups.
// Matches the Bluehost Bridge NEVER list (security review "SGG NEVER-WRITE ADD 1114-1125").
export class NeverWriteError extends Error {
  status = 403;
  constructor(message: string) { super(message); this.name = 'NeverWriteError'; }
}

const BLOCKED_NAMES = new Set(['.htaccess', '.htpasswd', '.user.ini', 'php.ini']);
const CODE = '(php\\d*|phtml|pht|phps|phar|cgi|pl|py|sh|shtml)';
const CODE_EXT = new RegExp('\\.' + CODE + '$');
const CODE_PART = new RegExp('\\.' + CODE + '\\.');

// Returns why a basename may never be written, or null.
export function neverWriteReason(path: unknown): string | null {
  const s = path == null ? '' : String(path);
  const raw = s.replace(/\\/g, '/').split('/').filter((x) => x !== '').pop() ?? '';
  const bare = raw.toLowerCase().replace(/[\s.]+$/u, '');  // drop trailing dots and spaces: ".htaccess." -> ".htaccess"
  if (!bare) return null;
  if (BLOCKED_NAMES.has(bare)) return 'server config file (' + raw + ')';
  if (CODE_EXT.test(bare) || CODE_PART.test(bare + '.')) return 'server code file (' + raw + ')';
  return null;
}

export function assertNotNeverWrite(what: string, path: unknown) {
  const why = neverWriteReason(path);
  if (why) throw new NeverWriteError('NEVER-WRITE: ' + what + ' ' + String(path) + ' refused: this app never writes, renames, moves or deletes a ' + why + '. Nothing was sent to the server. Change these files by hand in cPanel.');
}

export async function logNeverWrite(base44: any, source: string, error: unknown) {
  try {
    await base44.asServiceRole.entities.ConnectionAudit.create({
      checked_at: new Date().toISOString(), stage: 'never-write-refused', status: 'fail',
      detail: (source + ': ' + String((error as any)?.message || error)).slice(0, 1000),
    });
  } catch { /* logging must never hide the refusal */ }
}
