#!/bin/bash
# =============================================================================
# Zoho Mail Domain Verification Automation
# Uses alternative port since 8080 is occupied
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

DOMAIN="bakerstreetbandits.work.gd"
VERIFY_CODE="41845428"
VERIFY_DIR="$HOME/zohoverify"
HTTP_PORT=8888  # Alternative port since 8080 is in use

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🐝 ZOHO MAIL - Domain Verification                          ║"
echo "║     Domain: $DOMAIN"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Function to print sections
print_section() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  $1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Function to wait for user
wait_for_user() {
    echo ""
    read -p "Press Enter when ready to continue..."
}

# =============================================================================
# STEP 1: Check Prerequisites
# =============================================================================

check_prerequisites() {
    print_section "STEP 1: CHECKING PREREQUISITES"
    
    # Check verification file
    if [ ! -f "$VERIFY_DIR/verifyforzoho.html" ]; then
        echo -e "${RED}✗ Verification file not found${NC}"
        echo "Expected: $VERIFY_DIR/verifyforzoho.html"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Verification file found${NC}"
    echo "  Location: $VERIFY_DIR/verifyforzoho.html"
    echo "  Content: $(cat $VERIFY_DIR/verifyforzoho.html)"
    
    # Check ngrok
    if ! command -v ngrok &> /dev/null; then
        echo -e "${YELLOW}⚠ Ngrok not found. Installing...${NC}"
        curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
            sudo gpg --dearmor -o /usr/share/keyrings/ngrok-archive-keyring.gpg 2>/dev/null || true
        echo "deb [signed-by=/usr/share/keyrings/ngrok-archive-keyring.gpg] https://ngrok-agent.s3.amazonaws.com buster main" | \
            sudo tee /etc/apt/sources.list.d/ngrok.list > /dev/null 2>/dev/null || true
        sudo apt-get update -qq 2>/dev/null && sudo apt-get install -y ngrok 2>/dev/null || true
        
        # Try local install
        if ! command -v ngrok &> /dev/null; then
            cd /tmp
            wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz
            tar -xzf ngrok-v3-stable-linux-amd64.tgz
            chmod +x ngrok
            mv ngrok ~/.local/bin/ 2>/dev/null || mv ngrok /usr/local/bin/ 2>/dev/null || \
                mv ngrok ~/bin/ 2>/dev/null || export PATH="$PATH:/tmp"
        fi
    fi
    
    if command -v ngrok &> /dev/null; then
        echo -e "${GREEN}✓ Ngrok installed${NC}"
    else
        echo -e "${RED}✗ Ngrok installation failed${NC}"
        exit 1
    fi
    
    # Check ngrok auth
    if ! grep -q "authtoken" ~/.config/ngrok/ngrok.yml 2>/dev/null; then
        echo -e "${YELLOW}⚠ Ngrok auth token not configured${NC}"
        echo ""
        echo "Get your authtoken from: https://dashboard.ngrok.com/get-started/your-authtoken"
        read -p "Enter ngrok authtoken: " token
        
        if [ -n "$token" ]; then
            ngrok config add-authtoken "$token"
            echo -e "${GREEN}✓ Ngrok configured${NC}"
        else
            echo -e "${RED}✗ Ngrok authtoken required${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✓ Ngrok authenticated${NC}"
    fi
    
    # Check port availability
    if lsof -i :$HTTP_PORT > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠ Port $HTTP_PORT is in use, trying 8889...${NC}"
        HTTP_PORT=8889
    fi
    
    echo -e "${GREEN}✓ Will use port $HTTP_PORT${NC}"
}

# =============================================================================
# STEP 2: Start Verification Server
# =============================================================================

start_verification_server() {
    print_section "STEP 2: STARTING VERIFICATION SERVER"
    
    # Start Python HTTP server
    echo "Starting local HTTP server on port $HTTP_PORT..."
    cd "$VERIFY_DIR"
    python3 -m http.server $HTTP_PORT > /tmp/zoho_http.log 2>&1 &
    HTTP_PID=$!
    
    sleep 2
    
    # Check if server started
    if ! kill -0 $HTTP_PID 2>/dev/null; then
        echo -e "${RED}✗ Failed to start HTTP server${NC}"
        echo "Check log: /tmp/zoho_http.log"
        exit 1
    fi
    
    echo -e "${GREEN}✓ HTTP server started (PID: $HTTP_PID)${NC}"
    
    # Test local access
    if curl -s http://localhost:$HTTP_PORT/verifyforzoho.html | grep -q "$VERIFY_CODE"; then
        echo -e "${GREEN}✓ Verification file accessible locally${NC}"
    else
        echo -e "${YELLOW}⚠ Could not verify local access${NC}"
    fi
    
    # Start ngrok
    echo ""
    echo "Starting ngrok tunnel..."
    ngrok http $HTTP_PORT > /tmp/zoho_ngrok.log 2>&1 &
    NGROK_PID=$!
    
    sleep 5
    
    echo -e "${GREEN}✓ Ngrok tunnel started (PID: $NGROK_PID)${NC}"
    echo ""
    echo -e "${YELLOW}⏳ Waiting for ngrok to initialize...${NC}"
    sleep 3
    
    # Get ngrok URL
    NGROK_URL=""
    for i in {1..15}; do
        NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | head -1 | cut -d'"' -f4)
        if [ -n "$NGROK_URL" ]; then
            break
        fi
        sleep 1
    done
    
    if [ -z "$NGROK_URL" ]; then
        echo -e "${YELLOW}⚠ Could not auto-fetch ngrok URL${NC}"
        echo "Check manually at: http://localhost:4040"
        NGROK_URL="(Check http://localhost:4040/status)"
    fi
    
    export HTTP_PID NGROK_PID NGROK_URL
}

# =============================================================================
# STEP 3: Display Verification Instructions
# =============================================================================

show_verification_instructions() {
    print_section "STEP 3: DOMAIN VERIFICATION INSTRUCTIONS"
    
    echo -e "${GREEN}✓ Your verification server is running!${NC}"
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  VERIFICATION URL:"
    echo ""
    echo -e "  ${CYAN}${NGROK_URL}/verifyforzoho.html${NC}"
    echo ""
    echo "  VERIFICATION CODE: ${VERIFY_CODE}"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    echo "INSTRUCTIONS:"
    echo ""
    echo "1. Open your browser and go to:"
    echo "   https://mail.zoho.com (Zoho Mail Admin)"
    echo ""
    echo "2. Navigate to:"
    echo "   Control Panel → Domains → $DOMAIN"
    echo ""
    echo "3. Click on 'Verify Domain'"
    echo ""
    echo "4. Select 'HTML Method'"
    echo ""
    echo "5. Enter this URL:"
    echo -e "   ${CYAN}${NGROK_URL}/verifyforzoho.html${NC}"
    echo ""
    echo "6. Click 'Verify'"
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    echo -e "${YELLOW}⚠ IMPORTANT: Keep this terminal open during verification!${NC}"
    echo ""
    
    # Copy URL to clipboard if possible
    echo "$NGROK_URL/verifyforzoho.html" | xclip -selection clipboard 2>/dev/null || \
    echo "$NGROK_URL/verifyforzoho.html" | xsel --clipboard 2>/dev/null || \
    echo "$NGROK_URL/verifyforzoho.html" | pbcopy 2>/dev/null || true
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Verification URL copied to clipboard!${NC}"
    fi
    
    echo ""
    echo "Verification URL: $NGROK_URL/verifyforzoho.html"
    echo ""
}

# =============================================================================
# STEP 4: Wait for Verification
# =============================================================================

wait_for_verification() {
    print_section "STEP 4: WAITING FOR VERIFICATION"
    
    echo "The verification server is running."
    echo "Complete the verification in your browser."
    echo ""
    
    while true; do
        read -p "Have you completed the domain verification? (y/n/skip): " verified
        
        case $verified in
            y|Y)
                echo -e "${GREEN}✓ Domain verification completed!${NC}"
                return 0
                ;;
            n|N)
                echo ""
                echo "Options:"
                echo "  - Check the verification URL: $NGROK_URL/verifyforzoho.html"
                echo "  - Check ngrok status: http://localhost:4040"
                echo ""
                ;;
            s|S|skip)
                echo -e "${YELLOW}⚠ Skipping verification step${NC}"
                return 1
                ;;
        esac
    done
}

# =============================================================================
# STEP 5: Create Zoho Mail Account
# =============================================================================

create_mail_account() {
    print_section "STEP 5: CREATE EMAIL ACCOUNT"
    
    echo "After domain verification, you need to create an email account."
    echo ""
    echo "Suggested email: hive@$DOMAIN"
    echo ""
    echo "INSTRUCTIONS:"
    echo "1. In Zoho Mail Admin, go to: User Details → Add User"
    echo "2. Create user: hive"
    echo "3. Set a password"
    echo "4. Note down the email and password"
    echo ""
    
    wait_for_user
    
    read -p "Have you created the email account? (y/n): " created
    
    if [ "$created" = "y" ]; then
        echo -e "${GREEN}✓ Email account created${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ Email account not created yet${NC}"
        return 1
    fi
}

# =============================================================================
# STEP 6: Generate App Password
# =============================================================================

generate_app_password() {
    print_section "STEP 6: GENERATE APP PASSWORD"
    
    echo "You need to generate an app password for SMTP/IMAP access."
    echo ""
    echo "INSTRUCTIONS:"
    echo "1. Log in to your Zoho Mail account: hive@$DOMAIN"
    echo "2. Go to: My Account → Security → App Passwords"
    echo "   (Direct URL: https://accounts.zoho.com/home#security/app_passwords)"
    echo "3. Click 'Generate App Password'"
    echo "4. Name it: 'Hive 999 Mantis Agent'"
    echo "5. Copy the generated password"
    echo ""
    
    wait_for_user
    
    read -p "Have you generated the app password? (y/n): " generated
    
    if [ "$generated" = "y" ]; then
        echo -e "${GREEN}✓ App password generated${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠ App password not generated yet${NC}"
        return 1
    fi
}

# =============================================================================
# STEP 7: Collect Credentials
# =============================================================================

collect_credentials() {
    print_section "STEP 7: STORE CREDENTIALS"
    
    echo "Enter your Zoho Mail credentials to store them securely."
    echo ""
    
    read -p "Email address [hive@$DOMAIN]: " email
    email=${email:-hive@$DOMAIN}
    
    read -sp "App password (input hidden): " password
    echo ""
    
    if [ -n "$email" ] && [ -n "$password" ]; then
        # Store in .env
        ENV_FILE="$HOME/.env"
        
        # Remove existing entries
        if [ -f "$ENV_FILE" ]; then
            grep -v "^export MANTIS_EMAIL_" "$ENV_FILE" > "$ENV_FILE.tmp" 2>/dev/null || true
            mv "$ENV_FILE.tmp" "$ENV_FILE" 2>/dev/null || true
        fi
        
        # Add new entries
        echo "# Zoho Mail Configuration (auto-generated)" >> "$ENV_FILE"
        echo "export MANTIS_EMAIL_ADDRESS=$email" >> "$ENV_FILE"
        echo "export MANTIS_EMAIL_PASSWORD=$password" >> "$ENV_FILE"
        echo "export MANTIS_EMAIL_PROVIDER=zoho" >> "$ENV_FILE"
        
        echo ""
        echo -e "${GREEN}✓ Credentials stored in $ENV_FILE${NC}"
        echo ""
        echo "To use these credentials, run:"
        echo "  source $ENV_FILE"
        
        return 0
    else
        echo -e "${RED}✗ Email and password cannot be empty${NC}"
        return 1
    fi
}

# =============================================================================
# CLEANUP
# =============================================================================

cleanup() {
    print_section "CLEANING UP"
    
    if [ -n "$HTTP_PID" ]; then
        kill $HTTP_PID 2>/dev/null || true
        echo -e "${GREEN}✓ HTTP server stopped${NC}"
    fi
    
    if [ -n "$NGROK_PID" ]; then
        kill $NGROK_PID 2>/dev/null || true
        echo -e "${GREEN}✓ Ngrok tunnel closed${NC}"
    fi
}

# =============================================================================
# MAIN
# =============================================================================

main() {
    # Set trap to cleanup on exit
    trap cleanup EXIT
    
    # Run all steps
    check_prerequisites
    start_verification_server
    show_verification_instructions
    
    # Wait for verification
    while true; do
        if wait_for_verification; then
            break
        fi
        
        read -p "Continue waiting? (y/n): " continue_wait
        if [ "$continue_wait" != "y" ]; then
            echo "Exiting. You can complete this later."
            exit 0
        fi
    done
    
    # Continue with account setup
    create_mail_account
    generate_app_password
    collect_credentials
    
    # Final message
    print_section "SETUP COMPLETE"
    
    echo -e "${GREEN}✓ Zoho Mail domain verification complete!${NC}"
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo "NEXT STEPS:"
    echo ""
    echo "1. Load credentials:"
    echo "   source ~/.env"
    echo ""
    echo "2. Test the Mantis agent:"
    echo "   cd ~/beeai-hive-999"
    echo "   ./run.sh"
    echo ""
    echo "3. In the TUI, run:"
    echo "   :mantis"
    echo '   "Show email config"'
    echo '   "Check inbox"'
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
}

# Run main
main
