#!/bin/bash
# =============================================================================
# Zoho Mail Setup Script for Hive 999 Mantis Agent
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🐝 HIVE 999 - Zoho Mail Setup                              ║"
echo "║     Domain: bakerstreetbandits.work.gd                         ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if verifyforzoho.html exists
if [ ! -f "/home/boozelee/zohoverify/verifyforzoho.html" ]; then
    echo -e "${RED}❌ Verification file not found!${NC}"
    echo "Expected: /home/boozelee/zohoverify/verifyforzoho.html"
    echo ""
    echo "Please download the file from Zoho and place it in ~/zohoverify/"
    exit 1
fi

VERIFICATION_CODE=$(cat /home/boozelee/zohoverify/verifyforzoho.html)
echo -e "${GREEN}✓ Verification file found${NC}"
echo "  Code: $VERIFICATION_CODE"
echo ""

# Menu
echo "Select an option:"
echo ""
echo "  1) Start verification server (port 8080)"
echo "  2) Test Zoho configuration"
echo "  3) Set environment variables"
echo "  4) View current config"
echo "  5) Complete setup guide"
echo ""
read -p "Select (1-5): " choice

case $choice in
    1)
        echo ""
        echo -e "${CYAN}Starting verification server...${NC}"
        echo ""
        
        # Get IP addresses
        IP_ADDRESSES=$(hostname -I 2>/dev/null || echo "localhost")
        
        echo "Verification URLs:"
        for ip in $IP_ADDRESSES; do
            echo "  http://$ip:8080/verifyforzoho.html"
        done
        echo ""
        echo -e "${YELLOW}Note: If behind a router, you may need to:${NC}"
        echo "  1. Set up port forwarding (port 8080 → this machine)"
        echo "  2. Or use a tunnel service like ngrok"
        echo ""
        echo "Press Ctrl+C to stop the server"
        echo ""
        
        cd /home/boozelee/zohoverify
        python3 -m http.server 8080
        ;;
    
    2)
        echo ""
        echo -e "${CYAN}Testing Zoho configuration...${NC}"
        cd /home/boozelee/beeai-hive-999
        python3 agents/mantis_mail/mantis_agent.py test
        ;;
    
    3)
        echo ""
        echo -e "${CYAN}Setting environment variables...${NC}"
        echo ""
        
        read -p "Enter Zoho email address (e.g., hive@bakerstreetbandits.work.gd): " email
        read -sp "Enter Zoho app password: " password
        echo ""
        
        if [ -n "$email" ] && [ -n "$password" ]; then
            echo "export MANTIS_EMAIL_ADDRESS=$email" >> /home/boozelee/.env
            echo "export MANTIS_EMAIL_PASSWORD=$password" >> /home/boozelee/.env
            echo "export MANTIS_EMAIL_PROVIDER=zoho" >> /home/boozelee/.env
            echo ""
            echo -e "${GREEN}✓ Environment variables saved to ~/.env${NC}"
            echo "To load: source ~/.env"
        else
            echo -e "${RED}❌ Email and password cannot be empty${NC}"
        fi
        ;;
    
    4)
        echo ""
        cd /home/boozelee/beeai-hive-999
        python3 -c "from agents.mantis_mail.zoho_config import verify_setup; \
            [print(f'{k:20s}: {v}') for k,v in verify_setup().items()]"
        ;;
    
    5)
        echo ""
        cat << 'EOF'
═══════════════════════════════════════════════════════════════════
ZOHO MAIL SETUP COMPLETE GUIDE
═══════════════════════════════════════════════════════════════════

1. DOMAIN VERIFICATION
   ✓ Verification code: 41845428
   ✓ File location: ~/zohoverify/verifyforzoho.html
   
   To verify:
   a) Start the verification server:
      ./scripts/setup_zoho.sh → Option 1
   
   b) If you have a public web server:
      sudo mkdir -p /var/www/html/zohoverify
      sudo cp ~/zohoverify/verifyforzoho.html /var/www/html/zohoverify/
   
   c) Or use ngrok for temporary public URL:
      ngrok http 8080
      # Use the https URL in Zoho

2. CREATE EMAIL ACCOUNT
   After domain verification:
   - Go to Zoho Mail admin panel
   - Create user: hive@bakerstreetbandits.work.gd
   - Set password and note it down

3. GENERATE APP PASSWORD
   (Required for SMTP/IMAP access)
   - Zoho Account → Security → App Passwords
   - Generate new app password
   - Save it securely

4. CONFIGURE HIVE 999
   Set environment variables:
   
   export MANTIS_EMAIL_ADDRESS=hive@bakerstreetbandits.work.gd
   export MANTIS_EMAIL_PASSWORD=your_app_password
   export MANTIS_EMAIL_PROVIDER=zoho

5. TEST IN TUI
   Launch TUI: ./run.sh
   
   Commands:
   :mantis                    # Switch to Mantis agent
   "Show email config"        # View configuration
   "Check inbox"              # Check Zoho inbox
   "Draft email to team"      # Create draft

═══════════════════════════════════════════════════════════════════
EOF
        ;;
esac

echo ""
