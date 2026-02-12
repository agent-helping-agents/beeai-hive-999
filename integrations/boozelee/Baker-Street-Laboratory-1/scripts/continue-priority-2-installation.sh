#!/bin/bash

# Baker Street Laboratory - Continue Priority 2 Model Installation
# Resume installation of remaining Priority 2 models

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
LOG_FILE="logs/priority-2-installation.log"

# Function to log messages
log_message() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Function to check if command succeeded
check_success() {
    if [ $? -eq 0 ]; then
        log_message "${GREEN}✅ $1 completed successfully${NC}"
        return 0
    else
        log_message "${RED}❌ $1 failed${NC}"
        return 1
    fi
}

# Function to install model with custom alias
install_model() {
    local model_name="$1"
    local alias="$2"
    local description="$3"
    
    log_message "${YELLOW}📥 Installing $alias ($model_name)...${NC}"
    log_message "${CYAN}   Description: $description${NC}"
    
    # Check if model already exists
    if ollama list | grep -q "^$alias"; then
        log_message "${GREEN}✅ $alias already installed${NC}"
        return 0
    fi
    
    # Pull the base model
    if ! ollama pull "$model_name"; then
        log_message "${RED}❌ Failed to pull $model_name${NC}"
        return 1
    fi
    
    # Create alias if different from model name
    if [ "$model_name" != "$alias" ]; then
        # Create temporary Modelfile
        cat > "/tmp/${alias}.modelfile" <<EOF
FROM $model_name
SYSTEM "You are part of the Baker Street Laboratory AI ecosystem. $description"
EOF
        
        # Create the custom model
        if ollama create "$alias" -f "/tmp/${alias}.modelfile"; then
            log_message "${GREEN}✅ Successfully created custom model $alias${NC}"
            rm -f "/tmp/${alias}.modelfile"
        else
            log_message "${RED}❌ Failed to create custom model $alias${NC}"
            rm -f "/tmp/${alias}.modelfile"
            return 1
        fi
    fi
    
    log_message "${GREEN}✅ Successfully installed $alias${NC}"
    return 0
}

log_message "${PURPLE}🚀 BAKER STREET LABORATORY - PRIORITY 2 MODEL INSTALLATION${NC}"
log_message "${PURPLE}=========================================================${NC}"
log_message "${CYAN}Continuing with Priority 2 models for enhanced capabilities${NC}"
log_message "${PURPLE}Installation started at: $(date)${NC}"

# Check Ollama service
log_message "${BLUE}🔍 Checking Ollama service...${NC}"
if ! pgrep -x "ollama" > /dev/null; then
    log_message "${YELLOW}⚠️  Starting Ollama service...${NC}"
    ollama serve &
    sleep 5
fi
log_message "${GREEN}✅ Ollama service is running${NC}"

log_message "${BLUE}📋 PHASE 2: Installing Priority 2 Models (Recommended)${NC}"
log_message "${BLUE}====================================================${NC}"

# Priority 2 Models
install_model "openchat:3.5-0106-q4_K_M" "baker-street-scientific" "Scientific research methodology and academic analysis specialist"
check_success "OpenChat Scientific model installation"

install_model "neural-chat:7b-v3-3-q4_K_M" "baker-street-creative" "Creative writing and engaging research report generation"
check_success "Neural-Chat Creative model installation"

install_model "deepseek-coder:6.7b-instruct-q4_K_M" "baker-street-coder" "Data analysis automation and statistical processing"
check_success "DeepSeek-Coder model installation"

install_model "arcee-ai/arcee-agent" "baker-street-legal" "Legal research and compliance analysis specialist"
check_success "Arcee-Agent Legal model installation"

install_model "qwen2-audio:7b-instruct" "baker-street-audio" "Audio processing and transcription specialist"
check_success "Qwen2-Audio model installation"

# Installation Summary
log_message "${BLUE}📊 INSTALLATION SUMMARY${NC}"
log_message "${BLUE}======================${NC}"

# Count installed models
total_models=$(ollama list | grep -c "baker-street" || echo "0")
log_message "${GREEN}✅ Total Baker Street models installed: $total_models${NC}"

# Show all installed models
log_message "${CYAN}📋 Installed Baker Street models:${NC}"
ollama list | grep "baker-street" | while read line; do
    log_message "${GREEN}   ✅ $line${NC}"
done

log_message "${PURPLE}🎉 PRIORITY 2 MODEL INSTALLATION COMPLETE!${NC}"
log_message "${PURPLE}Installation completed at: $(date)${NC}"
log_message "${GREEN}🔬 Baker Street Laboratory AI ecosystem is now fully operational!${NC}"
