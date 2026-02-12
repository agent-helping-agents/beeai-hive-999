#!/bin/bash

# Email Setup Script for Terminal 221B Automation
# Supports: Gmail (2 accounts) + Zoho Mail

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  📧 Email Setup Wizard - Terminal 221B                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

cd "$(dirname "$0")"

echo -e "${BLUE}Step 1: Choose Email Provider${NC}"
echo ""
echo "1) Gmail (kiliaanv2@gmail.com) - QUICK SETUP"
echo "2) Gmail (iamthatiamresearch@gmail.com) - QUICK SETUP"
echo "3) Zoho Mail (Business Email) - PROFESSIONAL"
echo "4) Skip for now"
echo ""
read -p "Choose (1-4): " choice

case $choice in
  1)
    echo ""
    echo -e "${YELLOW}Gmail Setup Instructions:${NC}"
    echo "1. Go to: https://myaccount.google.com/apppasswords"
    echo "2. Select app: 'Mail' and device: 'Linux'"
    echo "3. Copy the 16-character password"
    echo ""
    read -sp "Enter Gmail App Password: " pwd1
    echo ""
    
    sed -i "s|EMAIL_PASSWORD_GMAIL1=.*|EMAIL_PASSWORD_GMAIL1=$pwd1|" .env || true
    sed -i "s|ACTIVE_EMAIL_PROVIDER=.*|ACTIVE_EMAIL_PROVIDER=GMAIL1|" .env || true
    
    echo -e "${GREEN}✅ Gmail (kiliaanv2) configured!${NC}"
    ;;
    
  2)
    echo ""
    echo -e "${YELLOW}Gmail Setup Instructions:${NC}"
    echo "1. Go to: https://myaccount.google.com/apppasswords"
    echo "2. Select app: 'Mail' and device: 'Linux'"
    echo "3. Copy the 16-character password"
    echo ""
    read -sp "Enter Gmail App Password: " pwd2
    echo ""
    
    sed -i "s|EMAIL_PASSWORD_GMAIL2=.*|EMAIL_PASSWORD_GMAIL2=$pwd2|" .env || true
    sed -i "s|ACTIVE_EMAIL_PROVIDER=.*|ACTIVE_EMAIL_PROVIDER=GMAIL2|" .env || true
    
    echo -e "${GREEN}✅ Gmail (iamthatiamresearch) configured!${NC}"
    ;;
    
  3)
    echo ""
    echo -e "${YELLOW}Zoho Mail Setup Instructions:${NC}"
    echo "1. Visit: https://www.zoho.com/mail/"
    echo "2. Click 'Sign up for free'"
    echo "3. Create account: terminal221b@zoho.com"
    echo "4. Verify email"
    echo "5. Go to Settings > Connected Accounts"
    echo "6. Generate app password"
    echo "7. Copy the password"
    echo ""
    read -p "Enter Zoho Email: " zoho_email
    read -sp "Enter Zoho App Password: " zoho_pwd
    echo ""
    
    sed -i "s|EMAIL_USER_ZOHO=.*|EMAIL_USER_ZOHO=$zoho_email|" .env || true
    sed -i "s|EMAIL_PASSWORD_ZOHO=.*|EMAIL_PASSWORD_ZOHO=$zoho_pwd|" .env || true
    sed -i "s|ACTIVE_EMAIL_PROVIDER=.*|ACTIVE_EMAIL_PROVIDER=ZOHO|" .env || true
    
    echo -e "${GREEN}✅ Zoho Mail configured!${NC}"
    ;;
    
  4)
    echo "Skipping email setup..."
    exit 0
    ;;
    
  *)
    echo "Invalid choice"
    exit 1
    ;;
esac

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  ✅ Email Configuration Complete!                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}Next step:${NC} Run: npm run send-emails"
echo ""

