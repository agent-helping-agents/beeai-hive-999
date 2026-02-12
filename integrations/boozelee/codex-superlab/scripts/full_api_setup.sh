#!/bin/bash
set -e

VAULT=~/api-keys
SCRIPTS=~/codex-superlab/scripts

# 1. Create retention_model.py
mkdir -p $SCRIPTS
cat <<'PYEOF' > $SCRIPTS/retention_model.py
import numpy as np

P = np.array([[0.7, 0.3],
              [0.4, 0.6]])
steady_state = np.linalg.matrix_power(P, 50)[0]
print("Expected user retention (steady state):", steady_state)
PYEOF
chmod +x $SCRIPTS/retention_model.py
echo "✓ retention_model.py created"

# 2. Audit existing vault credentials
mkdir -p $VAULT
echo
echo "=== Vault Credential Audit ==="
found_any=0
while IFS= read -r f; do
  [ -e "$f" ] || continue
  echo " - $(basename "$f") (modified: $(date -r "$f" '+%Y-%m-%d'))"
  found_any=1
done < <(find $VAULT -maxdepth 1 -type f \( -name "*.env" -o -name "*.json" -o -name "*.txt" \))
if [ "$found_any" -eq 0 ]; then
  echo "No credential files found yet."
fi

# 3. Ensure gcp_enabled_apis.txt exists
touch $VAULT/gcp_enabled_apis.txt

# 4. Google Cloud login (manual flow)
echo
echo "=== Google Cloud Authentication ==="
gcloud auth login --no-launch-browser
gcloud auth application-default login

# 5. List enabled Google APIs
echo
echo "=== Enabled Google APIs ==="
gcloud services list --enabled > $VAULT/gcp_enabled_apis.txt
cat $VAULT/gcp_enabled_apis.txt

# 6. Enable missing Google APIs
APIS=(
  sheets.googleapis.com
  drive.googleapis.com
  calendar-json.googleapis.com
  gmail.googleapis.com
)
echo
echo "=== Enabling Missing Google APIs ==="
for api in "${APIS[@]}"; do
  if ! grep -q "$api" $VAULT/gcp_enabled_apis.txt; then
    echo "Enabling $api..."
    gcloud services enable $api
  else
    echo "$api already enabled"
  fi
done

# 7. Verify other vault entries
echo
echo "=== Verify Other Vault Entries ==="
declare -A files=(
  ["Discord env"]="discord.env"
  ["Gmail env"]="gmail.env"
  ["GitHub env"]="github.env"
  ["Stripe env"]="stripe.env"
  ["Gumroad env"]="gumroad.env"
)
for name in "${!files[@]}"; do
  file=${files[$name]}
  if [ -f $VAULT/$file ]; then
    echo "✓ $name present"
  else
    echo "⚠ $name missing: creating placeholder $file"
    echo "# PLACEHOLDER for $name" > $VAULT/$file
    chmod 600 $VAULT/$file
  fi
done

# 8. Summary
echo
echo "=== Setup Complete ==="
echo "Retention model: $SCRIPTS/retention_model.py"
echo "Vault stored at: $VAULT"
echo "- Google ADC JSON: $(ls $VAULT/*.json 2>/dev/null || echo none)"
echo "- Enabled APIs logged in $VAULT/gcp_enabled_apis.txt"
echo "- Env files verified in vault:"
ls $VAULT/*.env
echo
echo "Run the retention model:"
echo "  python3 $SCRIPTS/retention_model.py"
