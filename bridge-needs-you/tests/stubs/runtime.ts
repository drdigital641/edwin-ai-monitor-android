// Test stand-in for 'base44:runtime' and the SDK. Holds no real secret; cPanel is mocked in tests.
// A test may set globalThis.__testSecrets (fake secret values, needsYou.test.ts) and globalThis.__bridgeTestClient or
// globalThis.__testClient (a fake SDK client: dropFolder.test.ts, needsYou.test.ts); otherwise nothing is available.
export const secrets = { get: (k: string): string | undefined => {
  const t = (globalThis as any).__testSecrets;
  if (t && Object.hasOwn(t, k)) return t[k];
  return k === 'CPANEL_TOKEN' ? 'test-token-not-real' : undefined;
} };
export function createClientFromRequest(_req: Request): any {
  const fake = (globalThis as any).__bridgeTestClient || (globalThis as any).__testClient;
  if (fake) return fake;
  throw new Error('not available in tests');
}
