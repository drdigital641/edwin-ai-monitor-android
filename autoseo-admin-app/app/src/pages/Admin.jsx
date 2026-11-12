// AutoSEO Admin shell (13 Nov 2026). The screens are the reviewed EN + 中文 templates in public/assets/admin.js;
// this page only hands them the signed-in app session: every call goes to this app's server function "admin".
import { useEffect } from 'react';
import { base44 } from '@/api/base44Client';
import { useAuth } from '@/lib/AuthContext';

export default function Admin() {
  const { user, isAuthenticated, navigateToLogin } = useAuth();
  useEffect(() => {
    if (!isAuthenticated) { navigateToLogin(); return; }
    window.AUTOSEO_API = (action, body) => base44.functions.invoke('admin', { ...(body || {}), action })
      .then((r) => r.data, (e) => e?.response?.data || e?.data || { ok: false, code: 'network' });
    window.AUTOSEO_SIGNOUT = () => base44.auth.logout();
    window.AUTOSEO_IS_ADMIN = user?.role === 'admin';
    const add = (src) => new Promise((ok, no) => { const s = document.createElement('script'); s.src = src; s.onload = ok; s.onerror = no; document.body.appendChild(s); });
    add('/assets/strings.js?v=2').then(() => add('/assets/admin.js?v=2'));
  }, [isAuthenticated]);
  return (
    <>
      <header className="hdr" id="hdr" />
      <main className="wrap" id="app" aria-live="polite" />
    </>
  );
}
