#!/bin/bash
# Live Mode Stripe Webhook Setup for Codex SuperLab
# Uses vault at ~/api-keys/stripe.env
# Creates webhook and outputs signing secret
set -e
echo "🚀 Setting up Live mode Stripe webhook..."
# Check Stripe CLI
if ! command -v stripe &>/dev/null; then
  echo "❌ Stripe CLI not found. Install it:"
  echo "sudo apt update && sudo apt install -y curl"
  echo "curl -L https://github.com/stripe/stripe-cli/releases/download/v1.19.1/stripe_1.19.1_linux_x86_64.tar.gz -o stripe.tar.gz"
  echo "tar -xzf stripe.tar.gz && sudo mv stripe /usr/local/bin/stripe && rm stripe.tar.gz"
  exit 1
fi
echo "✅ Stripe CLI: $(stripe --version)"
# Source vault
if [ ! -f ~/api-keys/stripe.env ]; then
  echo "❌ Vault file ~/api-keys/stripe.env not found."
  exit 1
fi
source ~/api-keys/stripe.env
if [ -z "$STRIPE_SECRET_KEY" ] || ! echo "$STRIPE_SECRET_KEY" | grep -q "^rk_live_\|^sk_live_"; then
  echo "❌ Invalid STRIPE_SECRET_KEY: $STRIPE_SECRET_KEY"
  exit 1
fi
echo "✅ Using STRIPE_SECRET_KEY: $(echo $STRIPE_SECRET_KEY | cut -c1-10)... (masked)"
# Create webhook
WEBHOOK_URL="https://codex-superlab.netlify.app/.netlify/functions/stripe-webhook"
echo "Creating webhook at $WEBHOOK_URL..."
CREATE_OUTPUT=$(stripe webhook_endpoints create --url "$WEBHOOK_URL" --enabled-event checkout.session.completed --enabled-event payment_intent.succeeded --api-key "$STRIPE_SECRET_KEY" --live 2>&1)
SIGNING_SECRET=$(echo "$CREATE_OUTPUT" | grep -o 'whsec_[a-zA-Z0-9_-]*' | head -1)
if [ -z "$SIGNING_SECRET" ]; then
  echo "❌ Error creating webhook: $CREATE_OUTPUT"
  exit 1
fi
# Store secret
echo "Storing signing secret in ~/api-keys/stripe.env..."
if ! grep -q "STRIPE_WEBHOOK_SECRET" ~/api-keys/stripe.env; then
  echo "STRIPE_WEBHOOK_SECRET=$SIGNING_SECRET" >> ~/api-keys/stripe.env
else
  sed -i "s/STRIPE_WEBHOOK_SECRET=.*/STRIPE_WEBHOOK_SECRET=$SIGNING_SECRET/" ~/api-keys/stripe.env
fi
chmod 600 ~/api-keys/stripe.env
echo "✅ Secret stored"
# Output
echo "✅ Webhook created! ID: $(echo "$CREATE_OUTPUT" | grep '"id"' | cut -d'"' -f4)"
echo "Paste this Signing Secret into your Codex SuperLab setup prompt:"
echo "$SIGNING_SECRET"
echo "Set STRIPE_WEBHOOK_SECRET=$SIGNING_SECRET in Netlify: https://app.netlify.com/sites/codex-superlab/configuration/env"
echo "🎉 Done! Secret: $SIGNING_SECRET"
