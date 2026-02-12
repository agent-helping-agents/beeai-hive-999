#!/bin/bash
set -e

VAULT=~/api-keys

echo "=== 1. List existing vault credentials ==="
grep -H "" \$VAULT/*.env || echo "No .env files found"

echo
echo "=== 2. Google Cloud login (token flow) ==="
gcloud auth login --no-launch-browser
gcloud auth application-default login

echo
echo "=== 3. Check enabled Google APIs ==="
gcloud services list --enabled > \$VAULT/gcp_enabled_apis.txt
echo "Enabled APIs:"
cat \$VAULT/gcp_enabled_apis.txt

echo
echo "=== 4. Enable missing Google APIs ==="
APIS=(
  sheets.googleapis.com
  drive.googleapis.com
  calendar-json.googleapis.com
  gmail.googleapis.com
)
for api in "\${APIS[@]}"; do
  if ! grep -q "\$api" \$VAULT/gcp_enabled_apis.txt; then
    echo "Enabling \$api..."
    gcloud services enable \$api
  else
    echo "\$api already enabled"
  fi
done

echo
echo "=== 5. Ensure Discord Bot permission scopes ==="
# Discord bot scopes are managed in the OAuth invite URL or developer portal

echo
echo "=== 6. Verify Stripe env file ==="
if grep -q "STRIPE_SECRET_KEY" \$VAULT/stripe.env; then
  echo "Stripe credentials present"
else
  echo "Stripe credentials missing! Add to \$VAULT/stripe.env"
fi

echo
echo "=== 7. Create Gumroad API env if missing ==="
if [ ! -f \$VAULT/gumroad.env ]; then
  echo "GUMROAD_API_KEY=YOUR_GUMROAD_TOKEN" > \$VAULT/gumroad.env
  chmod 600 \$VAULT/gumroad.env
  echo "Created \$VAULT/gumroad.env — fill with your Gumroad API key"
else
  echo "gumroad.env already exists"
fi

echo
echo "=== 8. Summary of missing integrations ==="
echo "- Google Sheets, Drive, Calendar, Gmail scopes enabled"
echo "- Discord bot scopes to verify in portal"
echo "- Stripe env checked"
echo "- Gumroad env created"
echo
echo "Run 'python3 retention_model.py' in ~/codex-superlab/scripts to test your retention model."
