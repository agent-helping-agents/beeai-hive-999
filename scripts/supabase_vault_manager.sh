#!/bin/bash
# =============================================================================
# Supabase Vault Manager - Interactive Credential Setup
# Uses Supabase CLI to store secrets in Vault
# =============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

HIVE_DIR="$HOME/beeai-hive-999"
ENV_FILE="$HOME/.env"

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

print_header() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║     🐝 HIVE 999 - Supabase Vault Manager                        ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# =============================================================================
# SUPABASE SETUP
# =============================================================================

check_supabase_cli() {
    if ! command -v supabase &> /dev/null; then
        print_error "Supabase CLI not found"
        print_info "Installing Supabase CLI..."
        
        # Try to install
        npm install -g supabase 2>/dev/null || \
        curl -fsSL https://github.com/supabase/cli/releases/download/v1.142.0/supabase_linux_amd64.tar.gz | \
            tar -xzf - -C /tmp && sudo mv /tmp/supabase /usr/local/bin/ 2>/dev/null || \
        curl -fsSL https://github.com/supabase/cli/releases/download/v1.142.0/supabase_linux_amd64.tar.gz | \
            tar -xzf - -C ~/.local/bin/ 2>/dev/null
        
        if ! command -v supabase &> /dev/null; then
            print_error "Failed to install Supabase CLI"
            print_info "Please install manually: npm install -g supabase"
            exit 1
        fi
    fi
    print_success "Supabase CLI found"
}

supabase_login() {
    print_info "Checking Supabase login status..."
    
    if ! supabase projects list &> /dev/null; then
        print_warning "Not logged in to Supabase"
        print_info "Please login to Supabase"
        print_info "Get your access token from: https://app.supabase.com/account/tokens"
        echo ""
        read -p "Enter Supabase access token: " token
        
        if [ -n "$token" ]; then
            echo "$token" | supabase login
            print_success "Logged in to Supabase"
        else
            print_error "Access token required"
            return 1
        fi
    else
        print_success "Already logged in to Supabase"
    fi
}

setup_supabase_project() {
    cd "$HIVE_DIR"
    
    if [ -f "supabase/config.toml" ]; then
        print_success "Supabase project already initialized"
        print_info "Project location: $HIVE_DIR/supabase"
        return 0
    fi
    
    print_info "Supabase project not initialized"
    echo ""
    echo "Options:"
    echo "  1) Create new Supabase project"
    echo "  2) Link to existing project"
    echo "  3) Skip (use local .env only)"
    echo ""
    read -p "Select option (1-3): " choice
    
    case $choice in
        1)
            print_info "Initializing new Supabase project..."
            supabase init
            print_success "Project initialized"
            print_info "Starting local Supabase..."
            supabase start || print_warning "Could not start local Supabase"
            ;;
        2)
            print_info "Available projects:"
            supabase projects list
            echo ""
            read -p "Enter project ID to link: " project_id
            if [ -n "$project_id" ]; then
                supabase init
                supabase link --project-ref "$project_id"
                print_success "Linked to project $project_id"
            fi
            ;;
        3)
            print_warning "Skipping Supabase setup"
            print_info "Secrets will be stored in ~/.env only"
            return 1
            ;;
    esac
}

# =============================================================================
# VAULT OPERATIONS
# =============================================================================

init_vault() {
    print_info "Initializing Supabase Vault..."
    
    sql="CREATE EXTENSION IF NOT EXISTS vault WITH SCHEMA vault;"
    
    if supabase db execute "$sql" 2>/dev/null; then
        print_success "Vault extension enabled"
        return 0
    else
        print_warning "Could not enable Vault via CLI"
        print_info "You may need to enable it manually in Supabase Dashboard"
        print_info "Dashboard → Database → Extensions → vault"
        return 1
    fi
}

add_secret_to_vault() {
    local name="$1"
    local value="$2"
    local description="$3"
    
    # Escape single quotes in value
    local escaped_value="${value//\'/\'\'}"
    
    sql="
    DELETE FROM vault.secrets WHERE name = '$name';
    INSERT INTO vault.secrets (name, secret, description)
    VALUES ('$name', '$escaped_value', '$description');
    "
    
    if supabase db execute "$sql" 2>/dev/null; then
        print_success "Added $name to Vault"
        return 0
    else
        return 1
    fi
}

add_secret_to_env() {
    local name="$1"
    local value="$2"
    
    # Remove existing entry
    if [ -f "$ENV_FILE" ]; then
        grep -v "^export $name=" "$ENV_FILE" > "$ENV_FILE.tmp" 2>/dev/null || true
        mv "$ENV_FILE.tmp" "$ENV_FILE" 2>/dev/null || true
    fi
    
    # Add new entry
    echo "export $name=$value" >> "$ENV_FILE"
    print_success "Added $name to ~/.env"
}

add_secret() {
    local name="$1"
    local value="$2"
    local description="$3"
    
    # Try Vault first, fall back to .env
    if [ -f "$HIVE_DIR/supabase/config.toml" ]; then
        if add_secret_to_vault "$name" "$value" "$description"; then
            # Also add to .env for local use
            add_secret_to_env "$name" "$value"
            return 0
        fi
    fi
    
    # Fall back to .env only
    add_secret_to_env "$name" "$value"
    return 0
}

list_secrets() {
    print_info "Secrets in Supabase Vault:"
    sql="SELECT name, description, created_at FROM vault.secrets ORDER BY created_at DESC;"
    supabase db execute "$sql" 2>/dev/null || print_warning "Could not list Vault secrets"
    
    echo ""
    print_info "Secrets in ~/.env:"
    if [ -f "$ENV_FILE" ]; then
        grep "^export" "$ENV_FILE" | sed 's/export //' | sed 's/=.*/=***/' || echo "  (none)"
    else
        echo "  (none)"
    fi
}

# =============================================================================
# CREDENTIAL COLLECTION
# =============================================================================

collect_ngrok_token() {
    print_info "Ngrok Setup"
    echo "Ngrok provides public URLs for local services (needed for Zoho verification)"
    echo "Get your authtoken: https://dashboard.ngrok.com/get-started/your-authtoken"
    echo ""
    read -sp "Enter Ngrok authtoken (input hidden): " token
    echo ""
    
    if [ -n "$token" ]; then
        # Configure ngrok
        ngrok config add-authtoken "$token" 2>/dev/null || true
        add_secret "NGROK_AUTHTOKEN" "$token" "Ngrok tunneling authentication token"
        print_success "Ngrok configured"
    else
        print_warning "Skipped Ngrok setup"
    fi
}

collect_langsmith() {
    print_info "LangSmith Setup"
    echo "LangSmith provides monitoring and tracing for AI agents"
    echo "Get API key: https://smith.langchain.com/settings"
    echo ""
    read -sp "Enter LangSmith API key (input hidden): " key
    echo ""
    
    if [ -n "$key" ]; then
        add_secret "LANGSMITH_API_KEY" "$key" "LangSmith API key for agent tracing"
        
        read -p "Enter project name [beeai-hive-999]: " project
        project=${project:-beeai-hive-999}
        add_secret "LANGSMITH_PROJECT" "$project" "LangSmith project name"
        add_secret "LANGSMITH_TRACING" "true" "Enable LangSmith tracing"
        print_success "LangSmith configured"
    else
        print_warning "Skipped LangSmith setup"
    fi
}

collect_openai() {
    print_info "OpenAI Setup"
    echo "OpenAI provides GPT-4 and GPT-3.5 for cloud backend"
    echo "Get API key: https://platform.openai.com/api-keys"
    echo ""
    read -sp "Enter OpenAI API key (input hidden): " key
    echo ""
    
    if [ -n "$key" ]; then
        add_secret "OPENAI_API_KEY" "$key" "OpenAI API key for GPT models"
        print_success "OpenAI configured"
    else
        print_warning "Skipped OpenAI setup"
    fi
}

collect_anthropic() {
    print_info "Anthropic Setup (Optional)"
    echo "Anthropic provides Claude-3 models for reasoning tasks"
    echo "Get API key: https://console.anthropic.com/settings/keys"
    echo ""
    read -sp "Enter Anthropic API key (input hidden, or press Enter to skip): " key
    echo ""
    
    if [ -n "$key" ]; then
        add_secret "ANTHROPIC_API_KEY" "$key" "Anthropic API key for Claude models"
        print_success "Anthropic configured"
    else
        print_warning "Skipped Anthropic setup"
    fi
}

collect_zoho() {
    print_info "Zoho Mail Setup"
    echo "Domain: bakerstreetbandits.work.gd"
    echo "Verification Code: 41845428"
    echo ""
    echo "Instructions:"
    echo "  1. Complete domain verification in Zoho Mail Admin"
    echo "  2. Create email account (e.g., hive@bakerstreetbandits.work.gd)"
    echo "  3. Generate app password in Zoho Account → Security → App Passwords"
    echo ""
    
    read -p "Enter Zoho email address: " email
    read -sp "Enter Zoho app password (input hidden): " password
    echo ""
    
    if [ -n "$email" ] && [ -n "$password" ]; then
        add_secret "MANTIS_EMAIL_ADDRESS" "$email" "Zoho Mail email address for Mantis"
        add_secret "MANTIS_EMAIL_PASSWORD" "$password" "Zoho Mail app password"
        add_secret "MANTIS_EMAIL_PROVIDER" "zoho" "Email provider type"
        print_success "Zoho Mail configured"
    else
        print_warning "Skipped Zoho setup"
    fi
}

collect_supabase_service_role() {
    print_info "Supabase Service Role Key (Optional)"
    echo "Required for advanced database operations"
    echo "Get from: Supabase Dashboard → Project Settings → API"
    echo ""
    read -sp "Enter Supabase service_role key (input hidden, or press Enter to skip): " key
    echo ""
    
    if [ -n "$key" ]; then
        add_secret "SUPABASE_SERVICE_ROLE_KEY" "$key" "Supabase service role key"
        print_success "Supabase service role configured"
    else
        print_warning "Skipped Supabase service role"
    fi
}

# =============================================================================
# MENU SYSTEM
# =============================================================================

show_main_menu() {
    print_header
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  MAIN MENU"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    echo "  1) 🚀 Complete Setup (All credentials)"
    echo "  2) 📧 Zoho Mail Only"
    echo "  3) 🌐 Ngrok Only"
    echo "  4) 🤖 LangSmith Only"
    echo "  5) 🧠 OpenAI Only"
    echo "  6) 📋 List All Secrets"
    echo "  7) 🗑️  Delete a Secret"
    echo "  8) 📤 Export .env"
    echo "  9) 🌐 Start Zoho Verification Server"
    echo "  0) ❌ Exit"
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
}

complete_setup() {
    print_header
    echo "═══════════════════════════════════════════════════════════════════"
    echo "  COMPLETE SETUP WIZARD"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    
    check_supabase_cli
    supabase_login
    setup_supabase_project
    init_vault
    
    echo ""
    echo "Now collecting credentials..."
    echo ""
    
    collect_ngrok_token
    echo ""
    collect_langsmith
    echo ""
    collect_openai
    echo ""
    collect_anthropic
    echo ""
    collect_zoho
    echo ""
    collect_supabase_service_role
    
    echo ""
    echo "═══════════════════════════════════════════════════════════════════"
    print_success "Setup complete!"
    echo "═══════════════════════════════════════════════════════════════════"
    echo ""
    echo "To use these credentials:"
    echo "  source ~/.env"
    echo ""
    echo "Or in the Hive TUI:"
    echo "  ./run.sh"
    echo "  :backend cloud"
    echo ""
}

zoho_only() {
    print_header
    collect_zoho
    
    echo ""
    read -p "Start Zoho verification server now? (y/n): " start_server
    if [ "$start_server" = "y" ]; then
        "$HIVE_DIR/scripts/ngrok_zoho_verify.sh"
    fi
}

ngrok_only() {
    print_header
    collect_ngrok_token
}

langsmith_only() {
    print_header
    collect_langsmith
}

openai_only() {
    print_header
    collect_openai
}

delete_secret() {
    print_header
    list_secrets
    echo ""
    read -p "Enter name of secret to delete: " name
    
    if [ -n "$name" ]; then
        # Try to delete from Vault
        sql="DELETE FROM vault.secrets WHERE name = '$name';"
        supabase db execute "$sql" 2>/dev/null && print_success "Deleted from Vault" || true
        
        # Delete from .env
        if [ -f "$ENV_FILE" ]; then
            grep -v "^export $name=" "$ENV_FILE" > "$ENV_FILE.tmp" && mv "$ENV_FILE.tmp" "$ENV_FILE"
            print_success "Deleted from ~/.env"
        fi
    fi
}

export_env() {
    print_header
    if [ -f "$ENV_FILE" ]; then
        print_info "Current ~/.env contents:"
        echo ""
        grep "^export" "$ENV_FILE" | sed 's/=.*/=***/' || echo "  (none)"
        echo ""
        print_info "To load these variables, run:"
        echo "  source ~/.env"
    else
        print_error "No ~/.env file found"
    fi
}

start_zoho_server() {
    print_header
    print_info "Starting Zoho verification server with Ngrok..."
    "$HIVE_DIR/scripts/ngrok_zoho_verify.sh"
}

# =============================================================================
# MAIN LOOP
# =============================================================================

main() {
    # Ensure we're in the right directory
    cd "$HIVE_DIR"
    
    while true; do
        show_main_menu
        read -p "Select option (0-9): " choice
        
        case $choice in
            1) complete_setup ;;
            2) zoho_only ;;
            3) ngrok_only ;;
            4) langsmith_only ;;
            5) openai_only ;;
            6) list_secrets ;;
            7) delete_secret ;;
            8) export_env ;;
            9) start_zoho_server ;;
            0) 
                echo ""
                print_success "Goodbye!"
                exit 0
                ;;
            *)
                print_error "Invalid option"
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
    done
}

# Run main
main
