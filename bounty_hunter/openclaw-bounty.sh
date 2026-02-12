#!/usr/bin/env bash
set -e

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm use 22 >/dev/null

OPENCLAW_DIR="$HOME/openclaw"
cd "$OPENCLAW_DIR"

export OPENCLAW_PROFILE="bounty-hunter"
export OPENCLAW_DATA_DIR="$HOME/.local/share/openclaw/$OPENCLAW_PROFILE"

mkdir -p "$OPENCLAW_DATA_DIR"

echo "[*] Starting openclaw with profile: $OPENCLAW_PROFILE"
echo "    Data dir: $OPENCLAW_DATA_DIR"

pnpm run start
