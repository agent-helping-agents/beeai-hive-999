#!/bin/bash

# Automated Stripe Webhook Setup for Codex SuperLab
# Uses vault at ~/api-keys/stripe.env for STRIPE_SECRET_KEY
# Creates webhook for checkout.session.completed & payment_intent.succeeded
# Stores signing secret in vault and outputs for setup prompt

set -e  # Exit on error

echo "🚀 Starting Stripe webhook setup for Codex SuperLab..."

# Step 1: Check for Stripe CLI
if ! command -v stripe &>/dev/null; then
  echo "❌ Stripe CLI not found. Install it manually:"
  echo "sudo apt update && sudo apt install -y curl"
  echo "curl -L https://github.com/stripe/stripe-cli/releases/download/v1.19.1/stripe_1.19.1_linux_x86_64.tar.gz -o stripe.tar.gz"
  echo "tar -xzf stripe.tar.gz && sudo mv stripe /usr/local/bin/stripe && rm stripe.tar.gz"
  exit 1
fi
echo "✅ Stripe CLI found: $(stripe --version)"

# Step 2: Source Stripe API key from vault
if [ ! -f ~/api-keys/stripe.env ]; then
  echo "❌ Vault file ~/api-keys/stripe.env not found. Please add STRIPE_SECRET_KEY."
  exit 1
fi
source ~/api-keys/stripe.env
if [ -z "$STRIPE_SECRET_KEY" ]; then
  echo "❌ STRIPE_SECRET_KEY not found in ~/api-keys/stripe.env."
  read -p "Enter your Stripe Test API key (sk_test_... from https://dashboard.stripe.com/test/apikeys): " STRIPE_SECRET_KEY
fi
echo "✅ Using STRIPE_SECRET_KEY from vault"

# Step 3: Create webhook
WEBHOOK_URL="https://codex-superlab.netlify.app/.netlify/functions/stripe-webhook"
echo "Creating webhook at $WEBHOOK_URL for events: checkout.session.completed, payment_intent.succeeded"
CREATE_OUTPUT=$(stripe webhook_endpoints create \
  --url "$WEBHOOK_URL" \
  --enabled-event checkout.session.completed \
  --enabled-event payment_intent.succeeded \
  --api-key "$STRIPE_SECRET_KEY" 2>&1)

# Extract secret
SIGNING_SECRET=$(echo "$CREATE_OUTPUT" | grep -o 'whsec_[a-zA-Z0-9_-]*' | head -1)
if [ -z "$SIGNING_SECRET" ]; then
  echo "❌ Error creating webhook. Output: $CREATE_OUTPUT"
  exit 1
fi

# Step 4: Store secret in vault
echo "Storing signing secret in ~/api-keys/stripe.env..."
if ! grep -q "STRIPE_WEBHOOK_SECRET" ~/api-keys/stripe.env; then
  echo "STRIPE_WEBHOOK_SECRET=$SIGNING_SECRET" >> ~/api-keys/stripe.env
else
  sed -i "s/STRIPE_WEBHOOK_SECRET=.*/STRIPE_WEBHOOK_SECRET=$SIGNING_SECRET/" ~/api-keys/stripe.env
fi
chmod 600 ~/api-keys/stripe.env
echo "✅ Secret stored in vault"

# Step 5: Output for user
echo "✅ Webhook created! ID: $(echo "$CREATE_OUTPUT" | grep '"id"' | cut -d'"' -f4)"
echo "Paste this Signing Secret into your Codex SuperLab setup prompt:"
echo "$SIGNING_SECRET"
echo "Also set STRIPE_WEBHOOK_SECRET=$SIGNING_SECRET in Netlify environment variables: https://app.netlify.com/sites/codex-superlab/configuration/env"

# Step 6: Test webhook
echo "🧪 Testing webhook..."
stripe trigger checkout.session.completed --api-key "$STRIPE_SECRET_KEY"
echo "✅ Test event sent. Check Netlify logs: https://app.netlify.com/sites/codex-superlab/functions"

echo "🎉 All done! Secret: $SIGNING_SECRET"
echo "Vault updated: cat ~/api-keys/stripe.env to verify"
