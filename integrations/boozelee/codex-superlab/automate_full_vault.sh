#!/bin/bash
set -e

VAULT=~/api-keys
DESKTOP=~/Desktop
mkdir -p $VAULT

echo ""
echo "=== STEP 1: Gather and Backup API Credentials ==="
find ~/Downloads ~/Desktop ~ ~/* -maxdepth 1 -type f \( -name "*.json" -o -name "*.env" \) -exec cp -u {} $VAULT/ \;
ls -l $VAULT/ > $VAULT/vault_index.txt

gcloud config list account > $VAULT/gcloud_active_account.txt 2>/dev/null || echo "(gcloud not configured)" > $VAULT/gcloud_active_account.txt
gcloud services list --enabled > $VAULT/gcp_enabled_apis.txt 2>/dev/null || echo "(no gcloud services listed)" > $VAULT/gcp_enabled_apis.txt

# Custom saves for Discord/Stripe/Gmail from known locations
for f in ~/codex-superlab/discord-bot-automation/.env \
         ~/codex-superlab/netlify/functions/stripe.env \
         ~/codex-superlab/discord-bot-automation/gmail.env \
         ~/codex-superlab/netlify/functions/gmail.env; do
    [ -f "$f" ] && cp -u "$f" $VAULT/
done

chmod 700 $VAULT && chmod 600 $VAULT/*

echo ""
echo "=== STEP 2: Outdated Credential WARNING (older than 90 days) ==="
find $VAULT -type f \( -name "*.json" -o -name "*.env" -o -name "*.txt" \) -mtime +90 \
  -exec echo '⚠ Outdated (>90d):' {} \; | tee $VAULT/vault_expiry_report.txt || echo "No old files found."

echo ""
echo "=== STEP 3: Desktop Link for Easy Access ==="
if [ -d "$DESKTOP" ]; then
    ln -sf $VAULT "$DESKTOP/API Vault"
    echo "Desktop link created at ~/Desktop/API Vault"
else
    echo "No desktop detected, skipping desktop shortcut."
fi

echo ""
echo "=== STEP 4: Backup Entire Vault ==="
cd $VAULT
tar czf $VAULT/api-keys_backup_$(date +%F).tar.gz *.json *.env *.txt
chmod 600 $VAULT/api-keys_backup_*

echo ""
echo "=== STEP 5: Manual TODOs & Automation Hints ==="
echo "If you need to update/replace any old creds, they're listed in $VAULT/vault_expiry_report.txt"
echo "You can now manage all credentials in $VAULT and open with one click from your Desktop."
echo "DO NOT SYNC OR EMAIL THIS ARCHIVE UNENCRYPTED."
