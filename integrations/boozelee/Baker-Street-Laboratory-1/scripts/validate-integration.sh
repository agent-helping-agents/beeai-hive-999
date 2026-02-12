#!/bin/bash

# Baker Street Laboratory - Integration Validation
# This script validates all GitHub integrations and features

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
    echo -e "${GREEN}[✅]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[⚠️ ]${NC} $1"
}

log_error() {
    echo -e "${RED}[❌]${NC} $1"
}

# Test URL accessibility
test_url() {
    local url=$1
    local description=$2
    
    if curl -s --head "$url" | head -n 1 | grep -q "200 OK"; then
        log_success "$description: $url"
        return 0
    else
        log_error "$description: $url (Not accessible)"
        return 1
    fi
}

# Validate repository features
validate_repository_features() {
    log_info "Validating repository features..."
    
    REPO_INFO=$(gh api repos/${REPO_FULL})
    
    # Check basic features
    if echo "$REPO_INFO" | jq -r '.has_issues' | grep -q "true"; then
        log_success "Issues enabled"
    else
        log_error "Issues not enabled"
    fi
    
    if echo "$REPO_INFO" | jq -r '.has_projects' | grep -q "true"; then
        log_success "Projects enabled"
    else
        log_error "Projects not enabled"
    fi
    
    if echo "$REPO_INFO" | jq -r '.has_wiki' | grep -q "true"; then
        log_success "Wiki enabled"
    else
        log_error "Wiki not enabled"
    fi
    
    if echo "$REPO_INFO" | jq -r '.has_discussions' | grep -q "true"; then
        log_success "Discussions enabled"
    else
        log_error "Discussions not enabled"
    fi
    
    if echo "$REPO_INFO" | jq -r '.has_pages' | grep -q "true"; then
        log_success "GitHub Pages enabled"
    else
        log_warning "GitHub Pages not enabled"
    fi
}

# Validate discussions
validate_discussions() {
    log_info "Validating discussion categories..."
    
    # Get repository ID for GraphQL query
    REPO_ID=$(gh api repos/${REPO_FULL} --jq '.node_id')
    
    # Query discussion categories
    CATEGORIES=$(gh api graphql --field query='
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        discussionCategories(first: 10) {
          nodes {
            name
            description
          }
        }
      }
    }' --field owner="$REPO_OWNER" --field name="$REPO_NAME" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        CATEGORY_COUNT=$(echo "$CATEGORIES" | jq -r '.data.repository.discussionCategories.nodes | length')
        log_success "Discussion categories found: $CATEGORY_COUNT"
        
        # List categories
        echo "$CATEGORIES" | jq -r '.data.repository.discussionCategories.nodes[] | "  - \(.name): \(.description)"'
    else
        log_warning "Could not retrieve discussion categories"
    fi
}

# Validate security features
validate_security() {
    log_info "Validating security features..."
    
    # Check vulnerability alerts
    if gh api repos/${REPO_FULL}/vulnerability-alerts >/dev/null 2>&1; then
        log_success "Vulnerability alerts enabled"
    else
        log_warning "Vulnerability alerts not enabled"
    fi
    
    # Check automated security fixes
    if gh api repos/${REPO_FULL}/automated-security-fixes >/dev/null 2>&1; then
        log_success "Automated security fixes enabled"
    else
        log_warning "Automated security fixes not enabled"
    fi
    
    # Check if SECURITY.md exists
    if gh api repos/${REPO_FULL}/contents/SECURITY.md >/dev/null 2>&1; then
        log_success "SECURITY.md file present"
    else
        log_error "SECURITY.md file missing"
    fi
}

# Validate branch protection
validate_branch_protection() {
    log_info "Validating branch protection..."
    
    PROTECTION=$(gh api repos/${REPO_FULL}/branches/main/protection 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        log_success "Branch protection enabled for main branch"
        
        # Check specific protections
        if echo "$PROTECTION" | jq -r '.enforce_admins.enabled' | grep -q "true"; then
            log_success "Admin enforcement enabled"
        else
            log_warning "Admin enforcement not enabled"
        fi
        
        if echo "$PROTECTION" | jq -r '.required_pull_request_reviews.required_approving_review_count' | grep -q "1"; then
            log_success "Pull request reviews required"
        else
            log_warning "Pull request reviews not properly configured"
        fi
    else
        log_warning "Branch protection not enabled for main branch"
    fi
}

# Validate funding configuration
validate_funding() {
    log_info "Validating funding configuration..."
    
    # Check FUNDING.yml
    if gh api repos/${REPO_FULL}/contents/.github/FUNDING.yml >/dev/null 2>&1; then
        log_success "FUNDING.yml file present"
    else
        log_error "FUNDING.yml file missing"
    fi
    
    # Check if sponsor button is visible (this requires the file to be processed)
    log_info "Sponsor button should be visible on the repository page"
}

# Validate URLs
validate_urls() {
    log_info "Validating repository URLs..."
    
    # Repository URLs
    test_url "https://github.com/${REPO_FULL}" "Repository main page"
    test_url "https://github.com/${REPO_FULL}/issues" "Issues page"
    test_url "https://github.com/${REPO_FULL}/discussions" "Discussions page"
    test_url "https://github.com/${REPO_FULL}/projects" "Projects page"
    test_url "https://github.com/${REPO_FULL}/wiki" "Wiki page"
    
    # GitHub Pages (may not be ready immediately)
    log_info "Testing GitHub Pages URL (may take time to deploy)..."
    if test_url "https://${REPO_OWNER}.github.io/${REPO_NAME}" "GitHub Pages"; then
        log_success "GitHub Pages is live"
    else
        log_warning "GitHub Pages not yet available (deployment may be in progress)"
    fi
}

# Validate GitHub Actions
validate_github_actions() {
    log_info "Validating GitHub Actions workflows..."
    
    WORKFLOWS=$(gh api repos/${REPO_FULL}/actions/workflows 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        WORKFLOW_COUNT=$(echo "$WORKFLOWS" | jq -r '.total_count')
        log_success "GitHub Actions workflows found: $WORKFLOW_COUNT"
        
        # List workflows
        echo "$WORKFLOWS" | jq -r '.workflows[] | "  - \(.name): \(.state)"'
    else
        log_warning "Could not retrieve GitHub Actions information"
    fi
}

# Generate comprehensive report
generate_report() {
    echo ""
    echo "🔬 Baker Street Laboratory - Integration Validation Report"
    echo "========================================================"
    echo ""
    
    validate_repository_features
    echo ""
    validate_discussions
    echo ""
    validate_security
    echo ""
    validate_branch_protection
    echo ""
    validate_funding
    echo ""
    validate_github_actions
    echo ""
    validate_urls
    
    echo ""
    echo "📊 Summary"
    echo "=========="
    echo "Repository: https://github.com/${REPO_FULL}"
    echo "GitHub Pages: https://${REPO_OWNER}.github.io/${REPO_NAME}"
    echo "Validation completed at: $(date)"
}

# Main execution
main() {
    generate_report
    
    echo ""
    log_success "Integration validation completed!"
    echo ""
    echo "🎯 Next Steps:"
    echo "   1. Visit your repository to verify all features are working"
    echo "   2. Test the sponsor buttons and funding links"
    echo "   3. Create your first discussion post"
    echo "   4. Set up your first project board"
    echo "   5. Wait for GitHub Pages to deploy (5-10 minutes)"
}

main "$@"
