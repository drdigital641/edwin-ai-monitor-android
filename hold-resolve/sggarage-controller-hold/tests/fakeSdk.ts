export const audit: any[] = []; export const cmds: any = {};
export function createClientFromRequest(_req: any) {
  return { auth: { me: async () => ({ role: 'admin', email: 'a@test' }) },
    asServiceRole: { entities: { ConnectionAudit: { create: async (r: any) => { audit.push(r); return r; } },
      WebsiteCommand: { get: async (id: string) => cmds[id], update: async (id: string, d: any) => Object.assign(cmds[id], d) } } } };
}
