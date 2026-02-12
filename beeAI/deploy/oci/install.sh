#!/bin/bash
# beeAI Installation Script for Oracle Cloud Infrastructure
# Run on: Ubuntu 22.04 LTS (OCI VM.Standard.A1.Flex recommended)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🐝 beeAI Installer for Oracle Cloud Infrastructure${NC}"
echo "=================================================="

# Check if running on OCI
if [[ ! -f /etc/oracle-release ]] && [[ ! -d /etc/cloud ]]; then
    echo -e "${YELLOW}⚠️  Warning: This script is optimized for OCI Ubuntu 22.04${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Update system
echo -e "${YELLOW}📦 Updating system packages...${NC}"
sudo apt-get update && sudo apt-get upgrade -y

# Install dependencies
echo -e "${YELLOW}🔧 Installing dependencies...${NC}"
sudo apt-get install -y \
    curl \
    wget \
    git \
    vim \
    htop \
    ufw \
    fail2ban \
    certbot \
    python3-certbot-nginx

# Install Docker
echo -e "${YELLOW}🐳 Installing Docker...${NC}"
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo -e "${GREEN}✅ Docker installed${NC}"
else
    echo -e "${GREEN}✅ Docker already installed${NC}"
fi

# Install Docker Compose
echo -e "${YELLOW}🐳 Installing Docker Compose...${NC}"
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo -e "${GREEN}✅ Docker Compose installed${NC}"
else
    echo -e "${GREEN}✅ Docker Compose already installed${NC}"
fi

# Clone beeAI repository
echo -e "${YELLOW}📥 Cloning beeAI repository...${NC}"
if [[ -d "beeAI" ]]; then
    echo -e "${YELLOW}Directory exists, pulling latest changes...${NC}"
    cd beeAI && git pull && cd ..
else
    git clone https://github.com/BoozeLee/beeAI.git || {
        echo -e "${YELLOW}⚠️  Could not clone from GitHub, using local copy...${NC}"
        mkdir -p beeAI
    }
fi

cd beeAI || exit 1

# Generate secret key
echo -e "${YELLOW}🔐 Generating secure secret key...${NC}"
if [[ -z "$T221B_SECRET_KEY" ]]; then
    export T221B_SECRET_KEY=$(openssl rand -hex 32)
    echo "export T221B_SECRET_KEY=$T221B_SECRET_KEY" >> ~/.bashrc
    echo -e "${GREEN}✅ Secret key generated and added to ~/.bashrc${NC}"
fi

# Configure firewall
echo -e "${YELLOW}🛡️  Configuring firewall...${NC}"
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 22181/tcp # beeAI API
sudo ufw --force enable

# Configure fail2ban
echo -e "${YELLOW}🛡️  Configuring fail2ban...${NC}"
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Create environment file
echo -e "${YELLOW}📝 Creating environment configuration...${NC}"
cat > .env << EOF
T221B_SECRET_KEY=$T221B_SECRET_KEY
ENV=production
LOG_LEVEL=info
RATE_LIMIT=100
EOF

echo -e "${GREEN}✅ Environment file created${NC}"

# Build and start beeAI
echo -e "${YELLOW}🚀 Building and starting beeAI...${NC}"
docker-compose -f deploy/docker/docker-compose.yml up -d --build

# Health check
echo -e "${YELLOW}🏥 Performing health check...${NC}"
sleep 5
if curl -s http://localhost:22181/health > /dev/null; then
    echo -e "${GREEN}✅ beeAI is running successfully!${NC}"
else
    echo -e "${RED}❌ Health check failed. Check logs with: docker-compose logs${NC}"
fi

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me)

echo ""
echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}🎉 Installation Complete!${NC}"
echo -e "${GREEN}==================================================${NC}"
echo ""
echo "📊 Access Information:"
echo "  • API Endpoint: http://$PUBLIC_IP:22181"
echo "  • Health Check: http://$PUBLIC_IP:22181/health"
echo ""
echo "🔐 Default Credentials (CHANGE THESE!):"
echo "  • Username: admin"
echo "  • Password: admin123"
echo ""
echo "⚙️  Next Steps:"
echo "  1. Change default passwords immediately"
echo "  2. Set up TLS/HTTPS with: sudo certbot certonly --standalone -d your-domain.com"
echo "  3. Update API URL in your client configurations"
echo ""
echo "📚 Useful Commands:"
echo "  • View logs: docker-compose -f deploy/docker/docker-compose.yml logs -f"
echo "  • Stop: docker-compose -f deploy/docker/docker-compose.yml down"
echo "  • Restart: docker-compose -f deploy/docker/docker-compose.yml restart"
echo ""
echo -e "${GREEN}==================================================${NC}"
echo -e "${GREEN}The game is afoot! 🐝🔍${NC}"
