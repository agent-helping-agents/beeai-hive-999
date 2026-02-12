#!/usr/bin/env bash
set -e

VAULT="$HOME/codex-api-vault"
PROJECT="$HOME/codex-superlab"
ENV_FILE="$PROJECT/.env"

# 1. Vault & File Validation
mkdir -p "$VAULT"
required_files=(google_service_account.json gmail_credentials.json)
for f in "\${required_files[@]}"; do
  if [[ ! -f "\$VAULT/\$f" ]]; then
    echo "❌ Missing vault file: \$f"; exit 1
  fi
done

# 2. Env Extraction (no interaction)
declare -A vault_map=(
  [DISCORD_BOT_TOKEN]=discord.env
  [DISCORD_PROGRESS_CHANNEL_ID]=discord.env
  [PROGRESS_TRACKER_SHEET_ID]=gmail.env
  [TEAM_NOTIFICATION_EMAIL]=gmail.env
  [OPENAI_API_KEY]=openai.env
  [GITHUB_TOKEN]=github.env
  [STRIPE_SECRET_KEY]=stripe.env
  [GUMROAD_API_TOKEN]=gumroad.env
)
declare -A env
for key in "\${!vault_map[@]}"; do
  file="\${vault_map[\$key]}"
  val=\$(grep \"^\$key=\" \"\$VAULT/\$file\" 2>/dev/null | cut -d= -f2-)
  if [[ -z \"\$val\" ]]; then
    echo \"❌ Missing \$key in \$file\"; exit 1
  fi
  env[\$key]=\"\$val\"
done

# 3. Generate .env
cat > "\$ENV_FILE" <<EOCONF
DISCORD_BOT_TOKEN=\${env[DISCORD_BOT_TOKEN]}
DISCORD_PROGRESS_CHANNEL_ID=\${env[DISCORD_PROGRESS_CHANNEL_ID]}

GOOGLE_SHEETS_CREDENTIALS_PATH=\$VAULT/google_service_account.json
PROGRESS_TRACKER_SHEET_ID=\${env[PROGRESS_TRACKER_SHEET_ID]}
GMAIL_CREDENTIALS_PATH=\$VAULT/gmail_credentials.json
TEAM_NOTIFICATION_EMAIL=\${env[TEAM_NOTIFICATION_EMAIL]}

OPENAI_API_KEY=\${env[OPENAI_API_KEY]}
GITHUB_TOKEN=\${env[GITHUB_TOKEN]}
VAULT_PATH=\$VAULT

STRIPE_SECRET_KEY=\${env[STRIPE_SECRET_KEY]}
GUMROAD_API_TOKEN=\${env[GUMROAD_API_TOKEN]}
EOCONF
chmod 600 "\$ENV_FILE"

# 4. Fix Syntax in Content Pipeline
sed -i "s/strftime('%Y-%m-%d')}}/strftime('%Y-%m-%d'))/g" "\$PROJECT/cat_article_content_pipeline.py"

# 5. Setup Python Venv & Install
cd "\$PROJECT"
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 6. Launch Automations
python3 discord_auto_checker_bot.py &
python3 gmail_sheets_progress_tracker.py &
python3 cat_article_content_pipeline.py &

# 7. Run Extra Scripts
for script in "\$PROJECT"/script_*.py; do
  [[ -f \$script ]] && python3 "\$script" &
done

echo "✅ Automation launched. Monitor Discord, Gmail, and Google Sheets for updates."
echo
echo "---------------- SUPER PROMPT ----------------"
echo "Next: Automate credential rotation using a Markov decision model."
echo "Implement vault integrity checks every hour via cron."
echo "Generate AI-driven anomaly detection on env drift."
echo "Enforce Principle of Minimum Exposure: rotate secrets at high frequency."
echo "Never log, print, or expose raw keys in any output."
echo "Continue building an agentic system that self-heals and secures credentials."
echo "---------------------------------------------"
