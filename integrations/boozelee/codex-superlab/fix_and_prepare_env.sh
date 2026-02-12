#!/usr/bin/env bash
set -euo pipefail

PROJECT="$HOME/codex-superlab"
VAULT="$HOME/codex-api-vault"
ENV_FILE="$PROJECT/.env"

echo "➡️ Extracting Google credentials paths into expected vars..."
# Read existing paths
GOOGLE_PATH="\$VAULT/google_service_account.json"
GMAIL_PATH="\$VAULT/gmail_credentials.json"

# Generate .env with correct variable names
cat > "\$ENV_FILE" <<EOL
# Discord
DISCORD_BOT_TOKEN=\$(grep '^DISCORD_BOT_TOKEN=' "\$VAULT/discord.env" | cut -d= -f2-)
DISCORD_PROGRESS_CHANNEL_ID=\$(grep '^DISCORD_PROGRESS_CHANNEL_ID=' "\$VAULT/discord.env" | cut -d= -f2-)

# Google Credentials
GOOGLE_SHEETS_CREDENTIALS_PATH=\$GOOGLE_PATH
SHEETS_CREDENTIALS=\$GOOGLE_PATH
PROGRESS_TRACKER_SHEET_ID=\$(grep '^PROGRESS_TRACKER_SHEET_ID=' "\$VAULT/gmail.env" | cut -d= -f2-)
GMAIL_CREDENTIALS_PATH=\$GMAIL_PATH
GMAIL_CREDENTIALS=\$GMAIL_PATH
TEAM_NOTIFICATION_EMAIL=\$(grep '^TEAM_NOTIFICATION_EMAIL=' "\$VAULT/gmail.env" | cut -d= -f2-)

# OpenAI & GitHub
OPENAI_API_KEY=\$(grep '^OPENAI_API_KEY=' "\$VAULT/openai.env" | cut -d= -f2-)
GITHUB_TOKEN=\$(grep '^GITHUB_TOKEN=' "\$VAULT/github.env" | cut -d= -f2-)
VAULT_PATH=\$VAULT

# Stripe & Gumroad
STRIPE_SECRET_KEY=\$(grep '^STRIPE_SECRET_KEY=' "\$VAULT/stripe.env" | cut -d= -f2-)
GUMROAD_API_TOKEN=\$(grep '^GUMROAD_API_TOKEN=' "\$VAULT/gumroad.env" | cut -d= -f2-)
EOL

chmod 600 "\$ENV_FILE"
echo "✅ .env prepared with correct variable names"

echo
echo "➡️ Patching f-string syntax in content pipeline..."
sed -i "s/context.get('publish_date', datetime.now().strftime('%Y-%m-%d')}}/context.get('publish_date', datetime.now().strftime('%Y-%m-%d'))/g" "\$PROJECT/cat_article_content_pipeline.py"
echo "✅ Syntax patched"

echo
echo "➡️ Ready to launch automation suite. Run:"
echo "cd \$PROJECT && ./run_all_codex_automation.sh"
