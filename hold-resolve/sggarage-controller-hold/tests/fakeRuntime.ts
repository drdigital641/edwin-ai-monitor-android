export const secrets = { get: (k: string) => ({ FTP_HOST: 'ftp.test', FTP_USER: 'u', FTP_PASS: 'p', FTP_PORT: '21', FTP_SECURE: 'false' } as any)[k] };
