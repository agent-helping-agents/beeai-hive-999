#!/bin/bash
set -e
cd /home/boozelee/codex-superlab

if ! command -v stripe &> /dev/null; then
  echo "Installing Stripe CLI..."
  curl -L https://github.com/stripe/stripe-cli/releases/download/v1.19.1/stripe_1.19.1_linux_x86_64.tar.gz | tar xz
  sudo mv stripe /usr/local/bin/
fi

echo "Logging into Stripe CLI. Follow browser auth!"
stripe login

PRODUCT_ID=$(stripe products create --name "Codex SuperLab Early Access" -q id)
PRICE_ID=$(stripe prices create --unit-amount 4700 --currency usd --product $PRODUCT_ID --lookup-key codexlab_early --transfer_lookup-key)
echo "✓ Product: \$PRODUCT_ID"
echo "✓ Price: \$PRICE_ID"
echo "==> Insert this price id into payment.html: \$PRICE_ID"
