#!/bin/bash

# Baker Street Laboratory - GitHub Pages Configuration
# This script enables and configures GitHub Pages for the repository

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Repository details
REPO_OWNER="BoozeLee"
REPO_NAME="Baker-Street-Laboratory"
REPO_FULL="${REPO_OWNER}/${REPO_NAME}"

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

# Enable GitHub Pages
enable_github_pages() {
    log_info "Enabling GitHub Pages..."
    
    # Check if Pages is already enabled
    PAGES_STATUS=$(gh api repos/${REPO_FULL}/pages 2>/dev/null || echo "not_enabled")
    
    if [[ "$PAGES_STATUS" != "not_enabled" ]]; then
        log_success "GitHub Pages already enabled"
        PAGES_URL=$(echo "$PAGES_STATUS" | jq -r '.html_url')
        log_info "Pages URL: $PAGES_URL"
        return 0
    fi
    
    # Enable Pages with main branch and root directory
    log_info "Configuring Pages to deploy from main branch..."
    
    gh api repos/${REPO_FULL}/pages --method POST --field source='{"branch":"main","path":"/"}' >/dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        log_success "GitHub Pages enabled successfully"
        log_info "Pages will be available at: https://${REPO_OWNER}.github.io/${REPO_NAME}"
        log_warning "Note: It may take a few minutes for the site to become available"
    else
        log_error "Failed to enable GitHub Pages"
        log_info "You may need to enable it manually in the repository settings"
        return 1
    fi
}

# Verify Pages deployment
verify_pages() {
    log_info "Verifying GitHub Pages configuration..."
    
    PAGES_INFO=$(gh api repos/${REPO_FULL}/pages 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "GitHub Pages Configuration:"
        echo "=========================="
        echo "Status: $(echo "$PAGES_INFO" | jq -r '.status')"
        echo "URL: $(echo "$PAGES_INFO" | jq -r '.html_url')"
        echo "Source Branch: $(echo "$PAGES_INFO" | jq -r '.source.branch')"
        echo "Source Path: $(echo "$PAGES_INFO" | jq -r '.source.path')"
        
        log_success "GitHub Pages verification completed"
    else
        log_warning "Could not retrieve Pages information"
    fi
}

# Main execution
main() {
    echo "📄 Baker Street Laboratory - GitHub Pages Configuration"
    echo "======================================================"
    
    enable_github_pages
    verify_pages
    
    echo ""
    log_success "GitHub Pages configuration completed!"
    echo ""
    echo "🌐 Your documentation will be available at:"
    echo "   https://${REPO_OWNER}.github.io/${REPO_NAME}"
    echo ""
    echo "📝 The README.md file will serve as the landing page"
    echo "⏱️  Allow 5-10 minutes for initial deployment"
}

main "$@"
