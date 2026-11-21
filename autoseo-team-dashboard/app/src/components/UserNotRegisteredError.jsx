import React from 'react';
import { base44 } from '@/api/base44Client';

// Signed in with an account that was not invited to this app. Shows no client data (the server function refuses too).
const UserNotRegisteredError = () => (
  <main className="wrap" style={{ paddingTop: 48 }}>
    <h1 className="h1">This account has no access</h1>
    <p className="lede">The AutoSEO team dashboard is invite only. Sign in with the email your invite was sent to, or ask Edwin for an invite.</p>
    <button className="btn main" type="button" onClick={() => base44.auth.logout()}>Use another account</button>
  </main>
);
export default UserNotRegisteredError;
