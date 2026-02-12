#!/bin/bash

echo "🚀 Setting up Wise API environment"
echo "=================================="

# Read Wise credentials from user
read -p "Enter your Wise Client ID: " WISE_CLIENT_ID
read -p "Enter your Wise Client Secret: " WISE_CLIENT_SECRET
read -p "Enter your Wise Redirect URI (e.g., http://localhost:8080/callback): " WISE_REDIRECT_URI

# Set environment variables
cat > .env << EOF
# Wise API Configuration
WISE_CLIENT_ID="$WISE_CLIENT_ID"
WISE_CLIENT_SECRET="$WISE_CLIENT_SECRET"
WISE_REDIRECT_URI="$WISE_REDIRECT_URI"

# API Base URLs
WISE_SANDBOX_URL="https://api.sandbox.transferwise.tech"
WISE_PRODUCTION_URL="https://api.transferwise.com"

# Current environment (sandbox or production)
WISE_ENVIRONMENT="sandbox"
EOF

echo "✅ Environment variables saved to .env"

# Load environment variables
set -a
source .env
set +a

echo ""
echo "📋 Your Wise Configuration:"
echo "Client ID: $WISE_CLIENT_ID"
echo "Redirect URI: $WISE_REDIRECT_URI"
echo "Environment: $WISE_ENVIRONMENT"
echo ""

echo "🎯 Next Steps:"
echo "1. Test authentication: ./treasury login"
echo "2. Complete OAuth2: ./treasury auth --code YOUR_CODE"
echo "3. View profile: ./treasury profile"
echo ""

echo "💡 Tip: Load these variables in your current session with:"
echo "  source .env"