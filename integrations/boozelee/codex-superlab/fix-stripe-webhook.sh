#!/bin/bash

# Fix Stripe Vault + Webhook Setup for Codex SuperLab
# Prompts for real Stripe keys, updates ~/api-keys/stripe.env
# Creates webhook and outputs signing secret

set -e  # Exit on error

echo "🚀 Fixing Stripe webhook setup for Codex SuperLab..."

# Step 1: Check for Stripe CLI
if ! command -v stripe &>/dev/null; then
  echo "❌ Stripe CLI not found. Install it:"
  echo "sudo apt update && sudo apt install -y curl"
  echo "curl -L https://github.com/stripe/stripe-cli/releases/download/v1.19.1/stripe_1.19.1_linux_x86_64.tar.gz -o stripe.tar.gz"
  echo "tar -xzf stripe.tar.gz && sudo mv stripe /usr/local/bin/stripe && rm stripe.tar.gz"
  exit 1
fi
echo "✅ Stripe CLI found: $(stripe --version)"

# Step 2: Prompt for real Stripe keys
echo "Your vault (~/api-keys/stripe.env) has placeholder keys. Let’s fix it."
read -p "Enter your Stripe Test Secret Key (sk_test_... from https://dashboard.stripe.com/test/apikeys): " STRIPE_SECRET_KEY
read -p "Enter your Stripe Test Publishable Key (pk_test_... from https://dashboard.stripe.com/test/apikeys): " STRIPE_PUBLIC_KEY
if [ -z "$STRIPE_SECRET_KEY" ] || ! echo "$STRIPE_SECRET_KEY" | grep -q "^sk_test_"; then
  echo "❌ Invalid secret key. Must start with sk_test_."
  exit 1
fi
if [ -z "$STRIPE_PUBLIC_KEY" ] || ! echo "$STRIPE_PUBLIC_KEY" | grep -q "^pk_test_"; then
  echo "❌ Invalid publishable key. Must start with pk_test_."
  exit 1
fi

# Step 3: Update vault
echo "Updating ~/api-keys/stripe.env with real keys..."
cat << KEYS > ~/api-keys/stripe.env
STRIPE_PUBLIC_KEY=$STRIPE_PUBLIC_KEY
STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET=
KEYS
chmod 600 ~/api-keys/stripe.env
echo "✅ Vault updated: cat ~/api-keys/stripe.env to verify"

# Step 4: Create webhook
WEBHOOK_URL="https://codex-superlab.netlify.app/.netlify/functions/stripe-webhook"
echo "Creating webhook at $WEBHOOK_URL for events: checkout.session.completed, payment_intent.succeeded"
CREATE_OUTPUT=$(stripe webhook_endpoints create \
  --url "$WEBHOOK_URL" \
  --enabled-event checkout.session.completed \
  --enabled-event payment_intent.succeeded \
  --api-key "$STRIPE_SECRET_KEY" 2>&1)
SIGNING_SECRET=$(echo "$CREATE_OUTPUT" | grep -o 'whsec_[a-zA-Z0-9_-]*' | head -1)
if [ -z "$SIGNING_SECRET" ]; then
  echo "❌ Error creating webhook. Output: $CREATE_OUTPUT"
  exit 1
fi

# Step 5: Store secret in vault
echo "Storing signing secret in ~/api-keys/stripe.env..."
echo "STRIPE_WEBHOOK_SECRET=$SIGNING_SECRET" >> ~/api-keys/stripe.env
chmod 600 ~/api-keys/stripe.env
echo "✅ Secret stored in vault"

# Step 6: Output for user
echo "✅ Webhook created! ID: $(echo "$CREATE_OUTPUT" | grep '"id"' | cut -d'"' -f4)"
echo "Paste this Signing Secret into your Codex SuperLab setup prompt:"
echo "$SIGNING_SECRET"
echo "Also set STRIPE_WEBHOOK_SECRET=$SIGNING_SECRET in Netlify: https://app.netlify.com/sites/codex-superlab/configuration/env"

# Step 7: Test webhook
echo "🧪 Testing webhook..."
stripe trigger checkout.session.completed --api-key "$STRIPE_SECRET_KEY"
echo "✅ Test event sent. Check Netlify logs: https://app.netlify.com/sites/codex-superlab/functions"

echo "🎉 Done! Secret: $SIGNING_SECRET"
echo "Vault updated: cat ~/api-keys/stripe.env to verify"
