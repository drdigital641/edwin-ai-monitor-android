import React from 'react';
import { base44 } from '@/api/base44Client';

// Signed in with a Google account that was not invited to this app (EN + 中文, 390px first).
const UserNotRegisteredError = () => (
  <main className="wrap" style={{ paddingTop: 48 }}>
    <div className="center">
      <h1 className="h1">This account is not approved<span className="zh" lang="zh-Hans">此账号未获批准</span></h1>
      <p>Sign in with the Gmail address AutoSEO approved for you.<span className="zh" lang="zh-Hans">请用 AutoSEO 批准的 Gmail 登录。</span></p>
      <button className="btn btn-main btn-block" style={{ minHeight: 48 }} onClick={() => base44.auth.logout()}>
        Use another account<span className="zh" lang="zh-Hans">换一个账号</span>
      </button>
    </div>
  </main>
);
export default UserNotRegisteredError;
