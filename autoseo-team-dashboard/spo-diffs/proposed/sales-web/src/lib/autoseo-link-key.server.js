// PUBLIC key of the AutoSEO team dashboard's signed link (21 Nov 2026). Public data, safe in code; the private key never
// leaves the AutoSEO Admin app's server. null = link OFF: every signed call gets 503 (fails closed).
// Set it only in a reviewed checkpoint, with the same key that goes into the Controller (shared/autoseoLinkKey.ts).
export const AUTOSEO_ADMIN_LINK_PUBLIC_JWK = null;
