import React from 'react';
import { base44 } from '@/api/base44Client';

// Signed in with a Google account that was not invited to this app (EN + 中文, 390px first).
const UserNotRegisteredError = () => (
  <main className="wrap" style={{ paddingTop: 48 }}>
    <div className="center">
      <h1 className="h1">This account is not approved<span className="zh" lang="zh-Hans">此账号未获批准</span></h1>
      <p>Log in with the email your AutoSEO invite was sent to.<span className="zh" lang="zh-Hans">请用收到 AutoSEO 邀请的电邮登录。</span></p>
      <button className="btn btn-main btn-block" style={{ minHeight: 48 }} onClick={() => base44.auth.logout()}>
        Use another account<span className="zh" lang="zh-Hans">换一个账号</span>
      </button>
    </div>
  </main>
);
export default UserNotRegisteredError;
