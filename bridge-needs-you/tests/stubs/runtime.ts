// Test stand-in for 'base44:runtime' and the SDK. Holds no real secret; cPanel is mocked in tests.
// Tests may set globalThis.__testSecrets (fake values) and globalThis.__testClient (in-memory base44 client).
export const secrets = { get: (k: string): string | undefined => {
  const t = (globalThis as any).__testSecrets;
  if (t && Object.hasOwn(t, k)) return t[k];
  return k === 'CPANEL_TOKEN' ? 'test-token-not-real' : undefined;
} };
export function createClientFromRequest(_req: Request): any {
  const c = (globalThis as any).__testClient;
  if (c) return c;
  throw new Error('not available in tests');
}
