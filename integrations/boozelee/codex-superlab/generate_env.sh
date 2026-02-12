#!/usr/bin/env bash
set -e

PROJECT_DIR="$HOME/codex-superlab"
VAULT_DIR="$HOME/codex-api-vault"
ENV_FILE="$PROJECT_DIR/.env"

if [[ ! -d "$VAULT_DIR" ]]; then
  echo "Vault directory not found: $VAULT_DIR"
  exit 1
fi

echo "Generating $ENV_FILE from vault credentials…"
cat > "$ENV_FILE" <<EOF
# Discord Bot
DISCORD_BOT_TOKEN=$(grep '^DISCORD_BOT_TOKEN=' "$VAULT_DIR/discord.env" | cut -d= -f2-)
DISCORD_PROGRESS_CHANNEL_ID=$(grep '^DISCORD_PROGRESS_CHANNEL_ID=' "$VAULT_DIR/discord.env" | cut -d= -f2-)

# Google Cloud
GOOGLE_SHEETS_CREDENTIALS_PATH=$VAULT_DIR/google_service_account.json
PROGRESS_TRACKER_SHEET_ID=$(grep '^PROGRESS_TRACKER_SHEET_ID=' "$VAULT_DIR/gmail.env" | cut -d= -f2-)
GMAIL_CREDENTIALS_PATH=$VAULT_DIR/gmail_credentials.json
TEAM_NOTIFICATION_EMAIL=$(grep '^TEAM_NOTIFICATION_EMAIL=' "$VAULT_DIR/gmail.env" | cut -d= -f2-)

# OpenAI
OPENAI_API_KEY=$(grep '^OPENAI_API_KEY=' "$VAULT_DIR/openai.env" | cut -d= -f2-)

# GitHub
GITHUB_TOKEN=$(grep '^GITHUB_TOKEN=' "$VAULT_DIR/github.env" | cut -d= -f2-)
VAULT_PATH=$VAULT_DIR

# Stripe
STRIPE_SECRET_KEY=$(grep '^STRIPE_SECRET_KEY=' "$VAULT_DIR/stripe.env" | cut -d= -f2-)

# Gumroad
GUMROAD_API_TOKEN=$(grep '^GUMROAD_API_TOKEN=' "$VAULT_DIR/gumroad.env" | cut -d= -f2-)
EOF

chmod 600 "$ENV_FILE"
echo "✅ Created $ENV_FILE"
