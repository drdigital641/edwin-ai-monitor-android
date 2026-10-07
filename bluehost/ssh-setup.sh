#!/usr/bin/env bash
# Prepares ~/.ssh on a GitHub Actions runner from repository/environment secrets.
# Required env: BLUEHOST_HOST, BLUEHOST_USER, BLUEHOST_SSH_KEY
# Optional env: BLUEHOST_PORT (default 22), BLUEHOST_SSH_PASSPHRASE, BLUEHOST_KNOWN_HOSTS
set -euo pipefail

for v in BLUEHOST_HOST BLUEHOST_USER BLUEHOST_SSH_KEY; do
  if [ -z "${!v:-}" ]; then
    echo "::error::Secret $v is not set. See bluehost/README.md." >&2
    exit 1
  fi
done
PORT="${BLUEHOST_PORT:-22}"

mkdir -p ~/.ssh && chmod 700 ~/.ssh
printf '%s\n' "$BLUEHOST_SSH_KEY" | tr -d '\r' > ~/.ssh/bluehost
chmod 600 ~/.ssh/bluehost
if [ -n "${BLUEHOST_SSH_PASSPHRASE:-}" ]; then
  # Strip the passphrase on this throwaway runner copy only.
  ssh-keygen -p -q -P "$BLUEHOST_SSH_PASSPHRASE" -N "" -f ~/.ssh/bluehost >/dev/null
fi

if [ -n "${BLUEHOST_KNOWN_HOSTS:-}" ]; then
  printf '%s\n' "$BLUEHOST_KNOWN_HOSTS" > ~/.ssh/known_hosts
else
  echo "::warning::BLUEHOST_KNOWN_HOSTS is not set; trusting the host key seen now. Run 'Bluehost - Check connection' and save the printed line as that secret."
  ssh-keyscan -p "$PORT" -T 15 "$BLUEHOST_HOST" > ~/.ssh/known_hosts 2>/dev/null
fi
chmod 600 ~/.ssh/known_hosts

cat > ~/.ssh/config <<CFG
Host bluehost
  HostName $BLUEHOST_HOST
  User $BLUEHOST_USER
  Port $PORT
  IdentityFile ~/.ssh/bluehost
  IdentitiesOnly yes
  StrictHostKeyChecking yes
  ServerAliveInterval 30
  ConnectTimeout 20
CFG
chmod 600 ~/.ssh/config
