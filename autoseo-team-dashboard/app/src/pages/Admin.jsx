// AutoSEO team dashboard shell (21 Nov 2026): Overview, Billing, Sales. The screens are public/assets/dash.js (one shared
// shell: header, 3-item nav, cards, pills, money format, empty/error states). This page only hands them the signed-in
// app session: every call goes to this app's server function "admin". No key, PIN or token is put in the page.
import { useEffect } from 'react';
import { base44 } from '@/api/base44Client';
import { useAuth } from '@/lib/AuthContext';

const V = '21nov1';

export default function Admin() {
  const { isAuthenticated, navigateToLogin } = useAuth();
  useEffect(() => {
    if (!isAuthenticated) { navigateToLogin(); return; }
    window.AUTOSEO_API = (action, body) => base44.functions.invoke('admin', { ...(body || {}), action })
      .then((r) => r.data, (e) => e?.response?.data || e?.data || { ok: false, code: 'network' });
    window.AUTOSEO_SIGNOUT = () => base44.auth.logout();
    if (document.getElementById('dash-js')) return;
    const s = document.createElement('script');
    s.id = 'dash-js'; s.src = `/assets/dash.js?v=${V}`;
    document.body.appendChild(s);
  }, [isAuthenticated]);
  return (
    <>
      <header id="hdr" />
      <main className="wrap" id="app" aria-live="polite" />
    </>
  );
}
