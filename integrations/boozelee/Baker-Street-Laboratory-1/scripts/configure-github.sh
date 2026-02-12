#!/bin/bash

# Baker Street Laboratory - Automated GitHub Repository Configuration
# This script configures GitHub web interface features using GitHub CLI and API

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Repository details
REPO_OWNER="BoozeLee"
REPO_NAME="Baker-Street-Laboratory"
REPO_FULL="${REPO_OWNER}/${REPO_NAME}"

# Logging functions
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

# Check if GitHub CLI is authenticated
check_auth() {
    log_info "Checking GitHub CLI authentication..."
    if ! gh auth status >/dev/null 2>&1; then
        log_warning "GitHub CLI not authenticated. Please run: gh auth login"
        log_info "Starting authentication process..."
        gh auth login --web
    else
        log_success "GitHub CLI is authenticated"
    fi
}

# Enable repository features
enable_repository_features() {
    log_info "Enabling repository features..."
    
    # Enable Issues (usually enabled by default)
    log_info "Ensuring Issues are enabled..."
    gh api repos/${REPO_FULL} --method PATCH --field has_issues=true >/dev/null 2>&1 || log_warning "Could not enable Issues"
    
    # Enable Projects
    log_info "Enabling Projects..."
    gh api repos/${REPO_FULL} --method PATCH --field has_projects=true >/dev/null 2>&1 || log_warning "Could not enable Projects"
    
    # Enable Wiki
    log_info "Enabling Wiki..."
    gh api repos/${REPO_FULL} --method PATCH --field has_wiki=true >/dev/null 2>&1 || log_warning "Could not enable Wiki"
    
    log_success "Repository features configuration completed"
}

# Enable GitHub Discussions
enable_discussions() {
    log_info "Enabling GitHub Discussions..."
    
    # Check if discussions are already enabled
    if gh api repos/${REPO_FULL} --jq '.has_discussions' 2>/dev/null | grep -q "true"; then
        log_success "Discussions already enabled"
    else
        # Enable discussions
        gh api repos/${REPO_FULL} --method PATCH --field has_discussions=true >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            log_success "Discussions enabled successfully"
        else
            log_error "Failed to enable Discussions"
            return 1
        fi
    fi
    
    # Wait a moment for discussions to be fully enabled
    sleep 2
    
    # Create discussion categories
    create_discussion_categories
}

# Create discussion categories
create_discussion_categories() {
    log_info "Creating discussion categories..."
    
    # Get repository ID
    REPO_ID=$(gh api repos/${REPO_FULL} --jq '.node_id')
    
    # Define categories
    declare -A categories=(
        ["General"]="DISCUSSION"
        ["Research Questions"]="Q_AND_A"
        ["Feature Requests"]="DISCUSSION"
        ["Show and Tell"]="DISCUSSION"
        ["Research Collaboration"]="DISCUSSION"
        ["Technical Support"]="Q_AND_A"
    )
    
    declare -A descriptions=(
        ["General"]="General discussions about Baker Street Laboratory"
        ["Research Questions"]="Ask questions about research methodologies and AI-augmented research"
        ["Feature Requests"]="Suggest new features and improvements"
        ["Show and Tell"]="Share your research results and success stories"
        ["Research Collaboration"]="Find collaborators and discuss joint research projects"
        ["Technical Support"]="Get help with installation, configuration, and troubleshooting"
    )
    
    for category in "${!categories[@]}"; do
        format="${categories[$category]}"
        description="${descriptions[$category]}"
        
        log_info "Creating category: $category"
        
        # Create category using GraphQL mutation
        gh api graphql --field query='
        mutation($repositoryId: ID!, $name: String!, $description: String!, $format: DiscussionCategoryFormat!) {
          createDiscussionCategory(input: {
            repositoryId: $repositoryId,
            name: $name,
            description: $description,
            format: $format
          }) {
            category {
              id
              name
            }
          }
        }' \
        --field repositoryId="$REPO_ID" \
        --field name="$category" \
        --field description="$description" \
        --field format="$format" >/dev/null 2>&1
        
        if [ $? -eq 0 ]; then
            log_success "Created category: $category"
        else
            log_warning "Category '$category' may already exist or failed to create"
        fi
    done
}

# Configure security features
configure_security() {
    log_info "Configuring security features..."
    
    # Enable vulnerability alerts
    log_info "Enabling vulnerability alerts..."
    gh api repos/${REPO_FULL}/vulnerability-alerts --method PUT >/dev/null 2>&1 || log_warning "Could not enable vulnerability alerts"
    
    # Enable automated security fixes
    log_info "Enabling automated security fixes..."
    gh api repos/${REPO_FULL}/automated-security-fixes --method PUT >/dev/null 2>&1 || log_warning "Could not enable automated security fixes"
    
    # Enable dependency graph (usually enabled by default for public repos)
    log_info "Dependency graph is automatically enabled for public repositories"
    
    log_success "Security features configuration completed"
}

# Configure branch protection
configure_branch_protection() {
    log_info "Configuring branch protection for main branch..."
    
    # Create branch protection rule
    gh api repos/${REPO_FULL}/branches/main/protection --method PUT --field required_status_checks='{"strict":true,"contexts":[]}' --field enforce_admins=true --field required_pull_request_reviews='{"required_approving_review_count":1,"dismiss_stale_reviews":true,"require_code_owner_reviews":true}' --field restrictions=null >/dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        log_success "Branch protection configured for main branch"
    else
        log_warning "Branch protection may already be configured or failed to set"
    fi
}

# Update repository metadata
update_repository_metadata() {
    log_info "Updating repository metadata..."
    
    # Update description
    gh api repos/${REPO_FULL} --method PATCH --field description="AI-Augmented Research Framework for Systematic Knowledge Discovery with Multi-Agent Pipeline" >/dev/null 2>&1
    
    # Update homepage URL (will be set to GitHub Pages URL)
    gh api repos/${REPO_FULL} --method PATCH --field homepage="https://boozelee.github.io/Baker-Street-Laboratory" >/dev/null 2>&1
    
    # Update topics
    gh api repos/${REPO_FULL}/topics --method PUT --field names='["ai-research","machine-learning","research-framework","multi-agent-system","python","automation","reproducible-research","data-science","github-actions","artificial-intelligence","research-tools","knowledge-discovery","scientific-computing","open-science","collaboration"]' >/dev/null 2>&1
    
    log_success "Repository metadata updated"
}

# Verify configuration
verify_configuration() {
    log_info "Verifying repository configuration..."
    
    # Check repository features
    REPO_INFO=$(gh api repos/${REPO_FULL})
    
    echo "Repository Configuration Status:"
    echo "================================"
    
    # Check features
    echo "Issues: $(echo "$REPO_INFO" | jq -r '.has_issues')"
    echo "Projects: $(echo "$REPO_INFO" | jq -r '.has_projects')"
    echo "Wiki: $(echo "$REPO_INFO" | jq -r '.has_wiki')"
    echo "Discussions: $(echo "$REPO_INFO" | jq -r '.has_discussions')"
    echo "Pages: $(echo "$REPO_INFO" | jq -r '.has_pages')"
    
    # Check description and homepage
    echo "Description: $(echo "$REPO_INFO" | jq -r '.description')"
    echo "Homepage: $(echo "$REPO_INFO" | jq -r '.homepage')"
    
    # Check topics
    echo "Topics: $(echo "$REPO_INFO" | jq -r '.topics | join(", ")')"
    
    log_success "Configuration verification completed"
}

# Main execution
main() {
    echo "🔬 Baker Street Laboratory - GitHub Repository Configuration"
    echo "=========================================================="
    
    check_auth
    enable_repository_features
    enable_discussions
    configure_security
    configure_branch_protection
    update_repository_metadata
    verify_configuration
    
    echo ""
    log_success "GitHub repository configuration completed!"
    echo ""
    echo "🎉 Your repository is now fully configured with:"
    echo "   ✅ GitHub Discussions with 6 categories"
    echo "   ✅ Security features enabled"
    echo "   ✅ Branch protection on main branch"
    echo "   ✅ Repository metadata and topics"
    echo "   ✅ All community features enabled"
    echo ""
    echo "🔗 Repository URL: https://github.com/${REPO_FULL}"
    echo "💬 Discussions: https://github.com/${REPO_FULL}/discussions"
    echo "🐛 Issues: https://github.com/${REPO_FULL}/issues"
    echo "📊 Projects: https://github.com/${REPO_FULL}/projects"
    echo "📚 Wiki: https://github.com/${REPO_FULL}/wiki"
}

# Run main function
main "$@"
