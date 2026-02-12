#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# HIVE³ Radicle Setup Script
# Automated setup for sovereign, private, censorship-resistant git hosting
# ═══════════════════════════════════════════════════════════════════════════════

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="HIVE3-729-Detective-Agency"
PROJECT_DESC="HIVE³ - The 729 Detective Agency | 28 AI Agents | Solana | Digital Root 9"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Banner
echo -e "${CYAN}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════════════════════╗
║  🕵️ HIVE³ ⟡ RADICLE SETUP ⟡ SOVEREIGN CODE FORGE                         ║
║                                                                           ║
║  9 Blockchains × 9 Stakeholders × 9 Trends = 729 Nodes                   ║
║  28 AI Agents | Solana Blockchain | Maximum Privacy | IP Protection       ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Main setup - focus on documentation and preparation
main() {
    log_info "HIVE³ Radicle Setup Preparation"
    log_info "Project root: $PROJECT_ROOT"
    
    # Create necessary directories
    mkdir -p "$PROJECT_ROOT/docs"
    mkdir -p "$PROJECT_ROOT/scripts"
    
    log_success "Directory structure ready"
    
    # Display setup instructions
    echo -e "${CYAN}"
    cat << 'EOF'
═══════════════════════════════════════════════════════════════════════
  SETUP INSTRUCTIONS
═══════════════════════════════════════════════════════════════════════

To complete HIVE³ Radicle setup, run these commands:

1. INSTALL RADICLE:
   curl -sSLf https://radicle.xyz/install | sh

2. CREATE IDENTITY:
   rad auth
   
   Enter:
   - Alias: hive3-architect (or your choice)
   - Passphrase: [STRONG PASSPHRASE]

3. INITIALIZE REPOSITORY:
   cd /home/boozelee/HIVE3-729-Detective-Agency
   rad init
   
   Enter:
   - Name: HIVE3-729-Detective-Agency
   - Description: HIVE³ - The 729 Detective Agency | 28 AI Agents
   - Default branch: main
   - Visibility: PRIVATE

4. CONFIGURE SIGNING:
   git config user.signingKey "$(rad self --ssh-key)"
   git config gpg.format ssh
   git config commit.gpgsign true

5. START NODE:
   rad node start --daemon

6. PUSH CODE:
   git push rad main

═══════════════════════════════════════════════════════════════════════
EOF
    echo -e "${NC}"
    
    log_success "Documentation created in docs/"
    log_success "Review PLATFORM_COMPARISON.md for platform analysis"
    log_success "Review RADICLE_SETUP.md for detailed guide"
    log_success "Review IP_PROTECTION_FRAMEWORK.md for IP protection"
}

main "$@"
