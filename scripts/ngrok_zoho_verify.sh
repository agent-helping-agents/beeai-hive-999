#!/bin/bash
# =============================================================================
# Automated Zoho Domain Verification with Ngrok
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
echo "║     🐝 HIVE 999 - Zoho Verification with Ngrok                 ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check ngrok
if ! command -v ngrok &> /dev/null; then
    echo -e "${RED}❌ ngrok not found${NC}"
    echo "Installing..."
    curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo gpg --dearmor -o /usr/share/keyrings/ngrok-archive-keyring.gpg 2>/dev/null || true
    echo "deb [signed-by=/usr/share/keyrings/ngrok-archive-keyring.gpg] https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list > /dev/null 2>/dev/null || true
    sudo apt-get update -qq 2>/dev/null && sudo apt-get install -y ngrok 2>/dev/null || true
fi

# Check for ngrok auth token
if ! grep -q "authtoken" ~/.config/ngrok/ngrok.yml 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Ngrok auth token not configured${NC}"
    echo ""
    echo "To get your auth token:"
    echo "  1. Go to https://dashboard.ngrok.com/get-started/your-authtoken"
    echo "  2. Copy your authtoken"
    echo "  3. Run: ngrok config add-authtoken YOUR_TOKEN"
    echo ""
    read -p "Enter your ngrok authtoken: " ngrok_token
    
    if [ -n "$ngrok_token" ]; then
        ngrok config add-authtoken "$ngrok_token"
        echo -e "${GREEN}✓ Ngrok configured${NC}"
    else
        echo -e "${RED}❌ Cannot continue without ngrok authtoken${NC}"
        exit 1
    fi
fi

# Create verification directory
mkdir -p /tmp/zohoverify
cp /home/boozelee/zohoverify/verifyforzoho.html /tmp/zohoverify/

# Start Python HTTP server in background
echo -e "${BLUE}Starting local HTTP server on port 8080...${NC}"
cd /tmp/zohoverify
python3 -m http.server 8080 > /tmp/zoho_server.log 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 2

# Start ngrok tunnel
echo -e "${BLUE}Starting ngrok tunnel...${NC}"
ngrok http 8080 > /tmp/ngrok.log 2>&1 &
NGROK_PID=$!

# Wait for ngrok to start
sleep 5

# Get ngrok URL
echo -e "${CYAN}Fetching ngrok public URL...${NC}"
sleep 3

# Try to get the URL from ngrok API
NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | grep -o '"public_url":"https://[^"]*' | head -1 | cut -d'"' -f4)

if [ -z "$NGROK_URL" ]; then
    echo -e "${YELLOW}⚠️  Could not auto-fetch ngrok URL${NC}"
    echo "Check http://localhost:4040 manually"
    NGROK_URL="(Check http://localhost:4040)"
fi

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo -e "${GREEN}✓ Zoho Verification URL Ready!${NC}"
echo ""
echo -e "${CYAN}Verification URL:${NC}"
echo "  $NGROK_URL/verifyforzoho.html"
echo ""
echo "Verification Code: 41845428"
echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo "  1. Go to Zoho Mail Admin → Domain Verification"
echo "  2. Enter this URL: $NGROK_URL/verifyforzoho.html"
echo "  3. Click 'Verify HTML File'"
echo ""
echo "Keep this terminal open during verification!"
echo ""
echo "Press Ctrl+C when verification is complete"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo -e '${GREEN}✓ Shutting down...${NC}'; kill $NGROK_PID $SERVER_PID 2>/dev/null; exit 0" INT
wait
