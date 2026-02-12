#!/bin/bash

# Baker Street Laboratory - Complete AI Model Installation Script
# Installs and configures all AI models for psychedelic detective research

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
OLLAMA_HOST="http://localhost:11434"
MODELS_CONFIG="config/ollama-models.yaml"
LOG_FILE="logs/model-installation.log"

# Create necessary directories
mkdir -p logs
mkdir -p models
mkdir -p config/specialized

echo -e "${BLUE}🚀 Baker Street Laboratory - AI Model Installation${NC}"
echo -e "${BLUE}=================================================${NC}"

# Function to log messages
log_message() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Function to check if Ollama is running
check_ollama() {
    log_message "${YELLOW}🔍 Checking Ollama service...${NC}"
    if ! curl -s "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; then
        log_message "${YELLOW}⚠️  Starting Ollama service...${NC}"
        sudo systemctl start ollama || ollama serve &
        sleep 5
        
        # Wait for Ollama to be ready
        for i in {1..30}; do
            if curl -s "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; then
                log_message "${GREEN}✅ Ollama service is running${NC}"
                return 0
            fi
            sleep 2
        done
        
        log_message "${RED}❌ Failed to start Ollama service${NC}"
        exit 1
    else
        log_message "${GREEN}✅ Ollama service is already running${NC}"
    fi
}

# Function to install a model
install_model() {
    local model_name="$1"
    local alias="$2"
    local description="$3"
    
    log_message "${BLUE}📥 Installing $alias ($model_name)...${NC}"
    log_message "${YELLOW}   Description: $description${NC}"
    
    if ollama list | grep -q "$model_name"; then
        log_message "${GREEN}✅ $alias already installed${NC}"
        return 0
    fi
    
    if ollama pull "$model_name"; then
        log_message "${GREEN}✅ Successfully installed $alias${NC}"
        
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
    else
        log_message "${RED}❌ Failed to install $alias${NC}"
        return 1
    fi
}

# Function to import existing model
import_existing_model() {
    local model_path="$1"
    local alias="$2"
    local description="$3"
    
    log_message "${BLUE}📂 Importing existing model $alias...${NC}"
    
    if [ ! -f "$model_path" ]; then
        log_message "${YELLOW}⚠️  Model file not found: $model_path${NC}"
        return 1
    fi
    
    if ollama list | grep -q "$alias"; then
        log_message "${GREEN}✅ $alias already imported${NC}"
        return 0
    fi
    
    # Create model from existing file
    ollama create "$alias" -f - <<EOF
FROM $model_path
SYSTEM "You are part of the Baker Street Laboratory AI ecosystem. $description"
EOF
    
    if [ $? -eq 0 ]; then
        log_message "${GREEN}✅ Successfully imported $alias${NC}"
    else
        log_message "${RED}❌ Failed to import $alias${NC}"
        return 1
    fi
}

# Function to verify model installation
verify_model() {
    local model_name="$1"
    local test_prompt="Hello, this is a test. Please respond briefly."
    
    log_message "${YELLOW}🧪 Testing $model_name...${NC}"
    
    response=$(ollama run "$model_name" "$test_prompt" 2>/dev/null | head -n 1)
    
    if [ -n "$response" ]; then
        log_message "${GREEN}✅ $model_name is working correctly${NC}"
        return 0
    else
        log_message "${RED}❌ $model_name failed verification${NC}"
        return 1
    fi
}

# Main installation process
main() {
    log_message "${BLUE}🎯 Starting Baker Street Laboratory AI Model Installation${NC}"
    log_message "${BLUE}Installation started at: $(date)${NC}"
    
    # Check Ollama service
    check_ollama
    
    # PHASE 1: PRIORITY 1 MODELS (Essential)
    log_message "${BLUE}📋 PHASE 1: Installing Priority 1 Models (Essential)${NC}"
    
    install_model "llava:7b-v1.6-mistral-q4_K_M" "baker-street-vision" "Visual analysis for research documents, charts, and diagrams"
    install_model "nomic-embed-text" "baker-street-embed" "Semantic search and content similarity analysis"
    install_model "yarn-mistral:7b-128k-q4_K_M" "baker-street-longcontext" "Process entire research papers with 128k context"
    
    # Import existing models
    log_message "${BLUE}📂 Importing existing models from external drive...${NC}"
    
    EXTERNAL_DRIVE="/media/batman/2e5c0fde-0328-49e4-8d37-dd18be027734/Desktop/boowelee/AIOSsetup/aios-models"
    
    import_existing_model "$EXTERNAL_DRIVE/hermes-3-llama-3b.gguf" "baker-street-hermes3" "Primary reasoning and research analysis model"
    import_existing_model "$EXTERNAL_DRIVE/codellama-7b-instruct.gguf" "baker-street-codellama" "Code generation and technical analysis"
    import_existing_model "$EXTERNAL_DRIVE/qwen3-1.7b.gguf" "baker-street-qwen3" "Fast responses and real-time interactions"
    
    # PHASE 2: PRIORITY 2 MODELS (Recommended)
    log_message "${BLUE}📋 PHASE 2: Installing Priority 2 Models (Recommended)${NC}"
    
    install_model "openchat:3.5-0106-q4_K_M" "baker-street-scientific" "Scientific literature analysis and research methodology"
    install_model "neural-chat:7b-v3-3-q4_K_M" "baker-street-creative" "Creative writing and engaging report generation"
    install_model "deepseek-coder:6.7b-instruct-q4_K_M" "baker-street-coder" "Statistical analysis and data processing automation"
    
    # PHASE 3: SPECIALIZED MODELS
    log_message "${BLUE}📋 PHASE 3: Installing Specialized Models${NC}"
    
    install_model "arcee-ai/arcee-agent" "baker-street-legal" "Legal research and contract analysis specialist"
    install_model "qwen2-audio:7b-instruct" "baker-street-audio" "Audio analysis and transcription capabilities"
    
    # Verify all installations
    log_message "${BLUE}🧪 VERIFICATION: Testing all installed models${NC}"
    
    models_to_verify=(
        "baker-street-vision"
        "baker-street-embed"
        "baker-street-longcontext"
        "baker-street-hermes3"
        "baker-street-codellama"
        "baker-street-qwen3"
        "baker-street-scientific"
        "baker-street-creative"
        "baker-street-coder"
        "baker-street-legal"
        "baker-street-audio"
    )
    
    failed_models=()
    
    for model in "${models_to_verify[@]}"; do
        if ! verify_model "$model"; then
            failed_models+=("$model")
        fi
    done
    
    # Installation summary
    log_message "${BLUE}📊 INSTALLATION SUMMARY${NC}"
    log_message "${BLUE}======================${NC}"
    
    total_models=${#models_to_verify[@]}
    failed_count=${#failed_models[@]}
    success_count=$((total_models - failed_count))
    
    log_message "${GREEN}✅ Successfully installed: $success_count/$total_models models${NC}"
    
    if [ $failed_count -gt 0 ]; then
        log_message "${RED}❌ Failed installations: $failed_count models${NC}"
        for model in "${failed_models[@]}"; do
            log_message "${RED}   - $model${NC}"
        done
    fi
    
    # Display model list
    log_message "${BLUE}📋 Installed Models:${NC}"
    ollama list
    
    log_message "${BLUE}Installation completed at: $(date)${NC}"
    
    if [ $failed_count -eq 0 ]; then
        log_message "${GREEN}🎉 All models installed successfully!${NC}"
        log_message "${GREEN}🚀 Baker Street Laboratory AI ecosystem is ready!${NC}"
        return 0
    else
        log_message "${YELLOW}⚠️  Installation completed with some failures${NC}"
        return 1
    fi
}

# Run main function
main "$@"
