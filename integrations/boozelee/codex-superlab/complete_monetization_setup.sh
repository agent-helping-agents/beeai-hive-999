#!/bin/bash
set -e

VAULT=~/api-keys
NETLIFY_SITE="codex-superlab"

echo "🚀 Codex SuperLab - Complete Monetization Setup"
echo "================================================"

# 1. Load vault credentials
if [ -f "$VAULT/stripe.env" ]; then
  source "$VAULT/stripe.env"
  echo "✅ Loaded Stripe: $([ -n "$STRIPE_PUBLIC_KEY" ] && echo "Public key found" || echo "Missing public key")"
fi
if [ -f "$VAULT/gmail.env" ]; then
  source "$VAULT/gmail.env"
  SUPPORT_EMAIL=${GMAIL_USER:-kiliaanv2@gmail.com}
  SMTP_PASSWORD=${GMAIL_APP_PASSWORD:-$SMTP_PASSWORD}
  echo "✅ Loaded Gmail: $SUPPORT_EMAIL"
fi
if [ -f "$VAULT/discord.env" ]; then
  source "$VAULT/discord.env"
  echo "✅ Loaded Discord: $([ -n "$DISCORD_INVITE_LINK" ] && echo "Invite found" || echo "Missing invite")"
fi

# 2. Gather any missing credentials
if [ -z "$STRIPE_PUBLIC_KEY" ]; then
  echo "Go to https://dashboard.stripe.com/apikeys"
  read -p "Stripe Publishable Key (pk_test_...): " STRIPE_PUBLIC_KEY
fi
if [ -z "$STRIPE_SECRET_KEY" ]; then
  read -sp "Stripe Secret Key (sk_test_...): " STRIPE_SECRET_KEY; echo
fi
SUPPORT_EMAIL=${SUPPORT_EMAIL:-kiliaanv2@gmail.com}
if [ -z "$SMTP_PASSWORD" ]; then
  echo "Make a Gmail App Password at: https://myaccount.google.com/apppasswords"
  read -sp "Gmail App Password (16 chars): " SMTP_PASSWORD; echo
fi
if [ -z "$DISCORD_INVITE_LINK" ]; then
  echo "Create a permanent invite in your Discord server settings."
  read -p "Discord Invite Link (https://discord.gg/...): " DISCORD_INVITE_LINK
fi

# 3. Stripe webhook setup
echo "Opening Stripe webhook page..."
xdg-open "https://dashboard.stripe.com/webhooks" 2>/dev/null || echo "Visit https://dashboard.stripe.com/webhooks"
echo "Set endpoint to:"
echo "  https://$NETLIFY_SITE.netlify.app/.netlify/functions/stripe-webhook"
echo "Select: checkout.session.completed and payment_intent.succeeded"
read -p "After creating, paste Webhook Signing Secret (whsec_...): " STRIPE_WEBHOOK_SECRET

# 4. Save all credentials to vault
cat > $VAULT/stripe.env <<STRIPE
STRIPE_PUBLIC_KEY=$STRIPE_PUBLIC_KEY
STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET=$STRIPE_WEBHOOK_SECRET
SUPPORT_EMAIL=$SUPPORT_EMAIL
STRIPE

cat > $VAULT/gmail.env <<GMAIL
GMAIL_USER=$SUPPORT_EMAIL
GMAIL_APP_PASSWORD=$SMTP_PASSWORD
SMTP_PASSWORD=$SMTP_PASSWORD
GMAIL

cat > $VAULT/discord.env <<DISCORD
DISCORD_INVITE_LINK=$DISCORD_INVITE_LINK
DISCORD

chmod 600 $VAULT/*.env
echo "✅ All credentials saved to $VAULT/"

# 5. Netlify environment variables
cd ~/codex-superlab

echo "Setting Netlify environment variables..."
netlify env:set STRIPE_PUBLIC_KEY "$STRIPE_PUBLIC_KEY" --context production
netlify env:set STRIPE_SECRET_KEY "$STRIPE_SECRET_KEY" --context production
netlify env:set STRIPE_WEBHOOK_SECRET "$STRIPE_WEBHOOK_SECRET" --context production
netlify env:set SUPPORT_EMAIL "$SUPPORT_EMAIL" --context production
netlify env:set SMTP_PASSWORD "$SMTP_PASSWORD" --context production
netlify env:set DISCORD_INVITE_LINK "$DISCORD_INVITE_LINK" --context production
echo "✅ Netlify environment configured"

# 6. Update payment.html
if [ -f payment.html ]; then
  sed -i.bak "s|YOUR_STRIPE_PUBLIC_KEY|$STRIPE_PUBLIC_KEY|g" payment.html
  echo "✅ payment.html updated"
  echo "⚠️  Remember to set YOUR_PRICE_ID from your Stripe product"
else
  echo "⚠️  payment.html not found in ~/codex-superlab"
fi

# 7. Stripe webhook function
if [ -f netlify/functions/stripe-webhook.js ]; then
  echo "✅ Webhook function exists"
else
  echo "⚠️  Creating webhook function..."
  mkdir -p netlify/functions

  cat > netlify/functions/stripe-webhook.js <<'WEBHOOK'
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
const nodemailer = require('nodemailer');

exports.handler = async (event) => {
  const sig = event.headers['stripe-signature'];
  let stripeEvent;
  try {
    stripeEvent = stripe.webhooks.constructEvent(event.body, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    return { statusCode: 400, body: `Webhook Error: ${err.message}` };
  }
  if (stripeEvent.type === 'checkout.session.completed') {
    const email = stripeEvent.data.object.customer_email;
    let transporter = nodemailer.createTransport({
      service: 'gmail',
      auth: {
        user: process.env.SUPPORT_EMAIL,
        pass: process.env.SMTP_PASSWORD
      }
    });
    await transporter.sendMail({
      from: process.env.SUPPORT_EMAIL,
      to: email,
      subject: 'Welcome to Codex SuperLab!',
      html: `
        <h2>🎉 Welcome to Codex SuperLab!</h2>
        <p>Thanks for your purchase!</p>
        <p><strong>Your access:</strong></p>
        <ul>
          <li><a href="https://github.com/BoozeLee/codex-superlab">GitHub Repository</a></li>
          <li><a href="${process.env.DISCORD_INVITE_LINK}">Discord Community</a></li>
        </ul>
      `
    });
  }
  return { statusCode: 200, body: 'Success' };
};
WEBHOOK
  echo "✅ Webhook function created"
fi

echo ""
echo "=== SETUP COMPLETE! ==="
echo ""
echo "✅ Credentials saved to: $VAULT/"
echo "✅ Netlify environment configured"
echo "✅ Webhook function ready"
echo ""
echo "🎯 Next steps:"
echo "1. Deploy: netlify deploy --prod"
echo "2. Test payment with card: 4242 4242 4242 4242"
echo "3. Check webhook logs in Stripe dashboard"
echo ""
echo "📊 Your SaaS is ready to accept payments!"
