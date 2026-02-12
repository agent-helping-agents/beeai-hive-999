#!/bin/bash

# Baker Street Laboratory - Complete GitHub Setup
# Master script that runs all GitHub configuration steps

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_header() {
    echo -e "${PURPLE}$1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if gh is installed
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed"
        log_info "Please install it first: https://cli.github.com/"
        exit 1
    fi
    
    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        log_warning "jq is not installed. Installing..."
        sudo apt update && sudo apt install -y jq
    fi
    
    # Check if curl is installed
    if ! command -v curl &> /dev/null; then
        log_error "curl is not installed"
        exit 1
    fi
    
    log_success "Prerequisites check completed"
}

# Main execution
main() {
    log_header "🔬 Baker Street Laboratory - Complete GitHub Setup"
    log_header "=================================================="
    echo ""
    
    check_prerequisites
    echo ""
    
    log_header "Step 1: Repository Configuration"
    log_header "================================"
    ./scripts/configure-github.sh
    echo ""
    
    log_header "Step 2: GitHub Pages Setup"
    log_header "=========================="
    ./scripts/enable-github-pages.sh
    echo ""
    
    log_header "Step 3: Integration Validation"
    log_header "=============================="
    ./scripts/validate-integration.sh
    echo ""
    
    log_header "🎉 Complete GitHub Setup Finished!"
    log_header "=================================="
    echo ""
    log_success "Your Baker Street Laboratory repository is now fully configured!"
    echo ""
    echo "🔗 Repository: https://github.com/BoozeLee/Baker-Street-Laboratory"
    echo "🌐 GitHub Pages: https://boozelee.github.io/Baker-Street-Laboratory"
    echo "💬 Discussions: https://github.com/BoozeLee/Baker-Street-Laboratory/discussions"
    echo "🐛 Issues: https://github.com/BoozeLee/Baker-Street-Laboratory/issues"
    echo "📊 Projects: https://github.com/BoozeLee/Baker-Street-Laboratory/projects"
    echo "📚 Wiki: https://github.com/BoozeLee/Baker-Street-Laboratory/wiki"
    echo ""
    echo "💖 Don't forget to:"
    echo "   - Create your first discussion post"
    echo "   - Set up project boards for research management"
    echo "   - Invite collaborators to the repository"
    echo "   - Share your research framework with the community!"
}

main "$@"
