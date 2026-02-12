#!/bin/bash
# =============================================================================
# Supabase Secrets Manager for Hive 999
# Interactively adds LangSmith and OpenAI API keys to Supabase Vault
# =============================================================================

set -e

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║     🐝 HIVE 999 - Supabase Secrets Manager                     ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if we're in a Supabase project
if [ ! -f "supabase/config.toml" ]; then
    echo -e "${YELLOW}⚠ No Supabase project found in current directory.${NC}"
    echo ""
    echo "Would you like to:"
    echo "  1) Initialize a new Supabase project"
    echo "  2) Link to an existing Supabase project"  
    echo "  3) Exit and configure manually"
    echo ""
    read -p "Select option (1-3): " choice
    
    case $choice in
        1)
            echo -e "${BLUE}Initializing Supabase project...${NC}"
            supabase init
            ;;
        2)
            echo -e "${BLUE}Linking to existing project...${NC}"
            read -p "Enter your Supabase project ID: " project_id
            supabase link --project-ref "$project_id"
            ;;
        3)
            echo "Exiting. To set up manually:"
            echo "  1. cd ~/beeai-hive-999"
            echo "  2. supabase init (or supabase link)"
            echo "  3. Run this script again"
            exit 0
            ;;
    esac
fi

echo ""
echo "Current Supabase project status:"
supabase status 2>/dev/null || echo "Status: Not running locally"
echo ""

# Function to add/update secret
add_secret() {
    local name=$1
    local description=$2
    
    echo ""
    echo -e "${BLUE}Setting up: $name${NC}"
    echo "Description: $description"
    echo ""
    
    read -sp "Enter $name (input will be hidden): " value
    echo ""
    
    if [ -z "$value" ]; then
        echo -e "${YELLOW}⚠ Skipping $name (empty value)${NC}"
        return
    fi
    
    # Using Supabase Vault via SQL
    echo "Adding secret to Supabase Vault..."
    
    # Create SQL to add secret
    sql="
    -- Enable Vault extension if not already enabled
    CREATE EXTENSION IF NOT EXISTS vault WITH SCHEMA vault;
    
    -- Delete existing secret if present
    DELETE FROM vault.secrets WHERE name = '$name';
    
    -- Insert new secret
    INSERT INTO vault.secrets (name, secret, description)
    VALUES ('$name', '$value', '$description');
    "
    
    # Execute SQL
    if supabase db execute "$sql" 2>/dev/null; then
        echo -e "${GREEN}✓ $name added successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Could not add via SQL. Trying alternative method...${NC}"
        
        # Alternative: Use local environment
        echo "export $name=$value" >> .env
        echo -e "${GREEN}✓ $name added to .env file${NC}"
    fi
}

# Menu for selecting which secrets to add
echo "Select secrets to configure:"
echo ""
echo "  1) All secrets (LangSmith + OpenAI + Anthropic)"
echo "  2) LangSmith only (for monitoring/tracing)"
echo "  3) OpenAI only (for cloud LLM backend)"
echo "  4) Custom selection"
echo "  5) View current secrets"
echo "  6) Delete a secret"
echo ""
read -p "Select option (1-6): " menu_choice

case $menu_choice in
    1)
        add_secret "LANGSMITH_API_KEY" "LangSmith API key for agent tracing and monitoring"
        add_secret "OPENAI_API_KEY" "OpenAI API key for GPT-4/GPT-3.5 cloud models"
        add_secret "ANTHROPIC_API_KEY" "Anthropic API key for Claude-3 models (optional)"
        ;;
    2)
        add_secret "LANGSMITH_API_KEY" "LangSmith API key for agent tracing and monitoring"
        ;;
    3)
        add_secret "OPENAI_API_KEY" "OpenAI API key for GPT-4/GPT-3.5 cloud models"
        ;;
    4)
        echo ""
        read -p "Enter secret name: " custom_name
        read -p "Enter description: " custom_desc
        add_secret "$custom_name" "$custom_desc"
        ;;
    5)
        echo ""
        echo "Current secrets in Supabase Vault:"
        supabase db execute "SELECT name, description, created_at FROM vault.secrets;" 2>/dev/null || \
            echo "Could not query vault. Checking .env file..."
        if [ -f .env ]; then
            echo ""
            echo "Secrets in .env file:"
            grep -E "^(LANGSMITH|OPENAI|ANTHROPIC)" .env | sed 's/=.*/=***/' || echo "  (none found)"
        fi
        ;;
    6)
        read -p "Enter name of secret to delete: " delete_name
        echo "Deleting $delete_name..."
        supabase db execute "DELETE FROM vault.secrets WHERE name = '$delete_name';" 2>/dev/null && \
            echo -e "${GREEN}✓ Deleted${NC}" || \
            echo -e "${RED}✗ Could not delete${NC}"
        ;;
esac

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "Next steps:"
echo ""
echo "  1. To use cloud backend, run:"
echo "     export HIVE_USE_CLOUD=true"
echo ""
echo "  2. Or in the TUI, use command:"
echo "     :backend cloud"
echo ""
echo "  3. To verify cloud is working:"
echo "     python backend/config_manager.py status"
echo ""
echo "═══════════════════════════════════════════════════════════════"
