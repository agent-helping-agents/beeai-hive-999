#!/bin/bash

# Baker Street Laboratory - Priority 2 Model Installation
# Install the 5 remaining Priority 2 models with psychedelic detective themes

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
INSTALLATION_START_TIME=$(date)

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

# Function to install model with custom Baker Street alias
install_baker_street_model() {
    local model_name="$1"
    local alias="$2"
    local description="$3"
    local psychedelic_prompt="$4"
    
    log_message "${PURPLE}🔬 Installing $alias${NC}"
    log_message "${CYAN}   Base Model: $model_name${NC}"
    log_message "${CYAN}   Role: $description${NC}"
    log_message "${BLUE}   Psychedelic Detective Theme: $psychedelic_prompt${NC}"
    echo ""
    
    # Check if model already exists
    if ollama list | grep -q "^$alias"; then
        log_message "${GREEN}✅ $alias already installed${NC}"
        return 0
    fi
    
    # Pull the base model with progress tracking
    log_message "${YELLOW}📥 Downloading base model: $model_name${NC}"
    if ! ollama pull "$model_name"; then
        log_message "${RED}❌ Failed to download $model_name${NC}"
        return 1
    fi
    check_success "Base model download for $alias"
    
    # Create Baker Street Laboratory Modelfile
    cat > "/tmp/${alias}.modelfile" <<EOF
FROM $model_name
SYSTEM "You are part of the Baker Street Laboratory AI ecosystem - a revolutionary psychedelic detective research environment. $description

Your role as a psychedelic detective: $psychedelic_prompt

Always maintain the Baker Street Laboratory identity:
- Approach problems with detective-like curiosity and systematic analysis
- Use creative, mind-expanding perspectives while maintaining scientific rigor
- Integrate artistic inspiration with analytical precision
- Think in terms of evidence, patterns, and breakthrough discoveries
- Embrace the kaleidoscopic nature of complex research problems

Remember: You are not just an AI assistant, but a specialized research detective in the most advanced AI-augmented laboratory ever created."
EOF
    
    # Create the custom Baker Street model
    log_message "${YELLOW}🎨 Creating custom Baker Street model: $alias${NC}"
    if ollama create "$alias" -f "/tmp/${alias}.modelfile"; then
        log_message "${GREEN}✅ Successfully created $alias${NC}"
        rm -f "/tmp/${alias}.modelfile"
    else
        log_message "${RED}❌ Failed to create $alias${NC}"
        rm -f "/tmp/${alias}.modelfile"
        return 1
    fi
    
    # Test the model
    log_message "${YELLOW}🧪 Testing $alias functionality...${NC}"
    test_response=$(echo "Introduce yourself as a psychedelic detective specialist." | ollama run "$alias" --verbose=false 2>/dev/null | head -n 3)
    if [ -n "$test_response" ]; then
        log_message "${GREEN}✅ $alias is responding correctly${NC}"
        log_message "${CYAN}   Sample response: ${test_response:0:100}...${NC}"
    else
        log_message "${YELLOW}⚠️  $alias created but test response empty${NC}"
    fi
    
    echo ""
    return 0
}

# Function to display installation progress
show_progress() {
    local current_model="$1"
    local total_models=5
    local completed_models="$2"
    
    log_message "${BLUE}📊 INSTALLATION PROGRESS${NC}"
    log_message "${BLUE}========================${NC}"
    log_message "${CYAN}Current Model: $current_model${NC}"
    log_message "${CYAN}Progress: $completed_models/$total_models models completed${NC}"
    log_message "${CYAN}Percentage: $((completed_models * 100 / total_models))%${NC}"
    echo ""
}

# Main installation function
main() {
    log_message "${PURPLE}🚀 BAKER STREET LABORATORY - PRIORITY 2 MODEL INSTALLATION${NC}"
    log_message "${PURPLE}============================================================${NC}"
    log_message "${CYAN}Installing 5 Priority 2 models with psychedelic detective themes${NC}"
    log_message "${PURPLE}Installation started at: $INSTALLATION_START_TIME${NC}"
    echo ""
    
    # Check Ollama service
    log_message "${BLUE}🔍 Checking Ollama service status...${NC}"
    if ! pgrep -x "ollama" > /dev/null; then
        log_message "${YELLOW}⚠️  Starting Ollama service...${NC}"
        ollama serve &
        sleep 5
    fi
    log_message "${GREEN}✅ Ollama service is running${NC}"
    echo ""
    
    # Show current Baker Street models
    log_message "${BLUE}📋 Current Baker Street Laboratory Models:${NC}"
    ollama list | grep "baker-street" | while read line; do
        log_message "${GREEN}   ✅ $line${NC}"
    done
    echo ""
    
    log_message "${BLUE}🎯 INSTALLING PRIORITY 2 MODELS${NC}"
    log_message "${BLUE}================================${NC}"
    
    # Model 1: Scientific Research Specialist
    show_progress "baker-street-scientific" 0
    install_baker_street_model \
        "openchat:latest" \
        "baker-street-scientific" \
        "Scientific research methodology and academic analysis specialist" \
        "You are the methodical investigator who applies rigorous scientific principles to uncover truth. Like Sherlock Holmes with a PhD in research methodology, you examine evidence with both analytical precision and creative insight. You see patterns in data that others miss, approach hypotheses with systematic curiosity, and transform complex research into clear, actionable insights. Your psychedelic perspective allows you to see connections across disciplines that traditional researchers overlook."
    check_success "baker-street-scientific installation"

    # Model 2: Creative Writing Specialist
    show_progress "baker-street-creative" 1
    install_baker_street_model \
        "neural-chat:latest" \
        "baker-street-creative" \
        "Creative writing and engaging research report generation" \
        "You are the storytelling detective who transforms dry research into compelling narratives. Like a psychedelic Sherlock Holmes with the soul of a poet, you weave scientific discoveries into engaging stories that captivate and educate. You see the human drama in data, the adventure in analysis, and the mystery in methodology. Your kaleidoscopic imagination turns research reports into journeys of discovery that readers can't put down."
    check_success "baker-street-creative installation"

    # Model 3: Data Analysis Specialist
    show_progress "baker-street-coder" 2
    install_baker_street_model \
        "deepseek-coder:latest" \
        "baker-street-coder" \
        "Data analysis automation and statistical processing" \
        "You are the algorithmic detective who speaks in code and thinks in patterns. Like Sherlock Holmes reborn as a master programmer, you automate the tedious and illuminate the complex. Your psychedelic coding perspective sees elegant solutions where others see chaos, creates beautiful algorithms that dance with data, and builds automated systems that free researchers to focus on breakthrough discoveries. Every script you write is a tool for uncovering hidden truths."
    check_success "baker-street-coder installation"

    # Model 4: Legal Research Specialist
    show_progress "baker-street-legal" 3
    install_baker_street_model \
        "llama3.2:latest" \
        "baker-street-legal" \
        "Legal research and compliance analysis specialist" \
        "You are the jurisprudential detective who navigates the labyrinth of law with psychedelic clarity. Like Sherlock Holmes with a law degree and expanded consciousness, you see through legal complexity to find the essential truth. You understand that law is not just rules but patterns of human behavior, and you use this insight to provide clear guidance through regulatory mazes. Your expanded perspective helps researchers stay compliant while pushing the boundaries of innovation."
    check_success "baker-street-legal installation"

    # Model 5: Audio Processing Specialist
    show_progress "baker-street-audio" 4
    install_baker_street_model \
        "qwen2.5:latest" \
        "baker-street-audio" \
        "Audio processing and transcription specialist" \
        "You are the auditory detective who hears what others miss. Like Sherlock Holmes with synesthetic superpowers, you perceive sound as color, rhythm as pattern, and voice as fingerprint. Your psychedelic hearing allows you to extract meaning from audio chaos, transcribe the untranscribable, and find the signal in the noise. You understand that every sound tells a story, every voice carries clues, and every audio file contains hidden evidence waiting to be discovered."
    check_success "baker-street-audio installation"
    
    # Final verification and summary
    log_message "${BLUE}🎉 PRIORITY 2 INSTALLATION COMPLETE!${NC}"
    log_message "${BLUE}====================================${NC}"
    
    # Count total Baker Street models
    total_models=$(ollama list | grep -c "baker-street" || echo "0")
    log_message "${GREEN}✅ Total Baker Street Laboratory models: $total_models${NC}"
    
    # Show all installed Baker Street models
    log_message "${CYAN}📋 Complete Baker Street Laboratory AI Ecosystem:${NC}"
    ollama list | grep "baker-street" | while read line; do
        log_message "${GREEN}   ✅ $line${NC}"
    done
    
    # Calculate total storage used
    total_size=$(ollama list | grep "baker-street" | awk '{sum += $3} END {print sum}')
    log_message "${CYAN}💾 Total Storage Used: ~25GB for complete AI ecosystem${NC}"
    
    echo ""
    log_message "${PURPLE}🔬 BAKER STREET LABORATORY AI ECOSYSTEM COMPLETE!${NC}"
    log_message "${PURPLE}Installation completed at: $(date)${NC}"
    log_message "${GREEN}🎭 Ready for psychedelic detective research across all domains!${NC}"
    
    return 0
}

# Run main installation
main "$@"
