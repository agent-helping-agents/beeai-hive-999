#!/bin/bash

# Baker Street Laboratory - Installation Monitor
# Real-time monitoring of AI model installation progress

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
LOG_FILE="logs/master-installation.log"
OLLAMA_URL="http://localhost:11434"

# Function to print header
print_header() {
    clear
    echo -e "${PURPLE}🔬 BAKER STREET LABORATORY - INSTALLATION MONITOR${NC}"
    echo -e "${PURPLE}===================================================${NC}"
    echo -e "${CYAN}Real-time monitoring of AI model ecosystem installation${NC}"
    echo ""
    echo -e "${BLUE}Current Time: $(date)${NC}"
    echo ""
}

# Function to check Ollama status
check_ollama_status() {
    echo -e "${BLUE}📡 OLLAMA SERVICE STATUS${NC}"
    echo -e "${BLUE}========================${NC}"
    
    if curl -s "$OLLAMA_URL/api/tags" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Ollama service is running${NC}"
        
        # Get model list
        models=$(ollama list 2>/dev/null | grep -c "baker-street" || echo "0")
        echo -e "${GREEN}📊 Baker Street models installed: $models${NC}"
        
        # Show current models
        if [ "$models" -gt 0 ]; then
            echo -e "${YELLOW}📋 Installed models:${NC}"
            ollama list | grep "baker-street" | while read line; do
                echo -e "${GREEN}   ✅ $line${NC}"
            done
        fi
    else
        echo -e "${RED}❌ Ollama service not responding${NC}"
    fi
    echo ""
}

# Function to check installation progress
check_installation_progress() {
    echo -e "${BLUE}📈 INSTALLATION PROGRESS${NC}"
    echo -e "${BLUE}========================${NC}"
    
    if [ -f "$LOG_FILE" ]; then
        # Count completed installations
        completed=$(grep -c "✅.*completed successfully" "$LOG_FILE" 2>/dev/null || echo "0")
        failed=$(grep -c "❌.*failed" "$LOG_FILE" 2>/dev/null || echo "0")
        
        echo -e "${GREEN}✅ Completed installations: $completed${NC}"
        if [ "$failed" -gt 0 ]; then
            echo -e "${RED}❌ Failed installations: $failed${NC}"
        fi
        
        # Show recent activity
        echo -e "${YELLOW}📝 Recent activity:${NC}"
        tail -n 5 "$LOG_FILE" | while read line; do
            if [[ "$line" == *"✅"* ]]; then
                echo -e "${GREEN}   $line${NC}"
            elif [[ "$line" == *"❌"* ]]; then
                echo -e "${RED}   $line${NC}"
            elif [[ "$line" == *"⚠️"* ]]; then
                echo -e "${YELLOW}   $line${NC}"
            else
                echo -e "${CYAN}   $line${NC}"
            fi
        done
    else
        echo -e "${YELLOW}⚠️  Installation log not found${NC}"
    fi
    echo ""
}

# Function to check system resources
check_system_resources() {
    echo -e "${BLUE}💾 SYSTEM RESOURCES${NC}"
    echo -e "${BLUE}==================${NC}"
    
    # Memory usage
    memory_info=$(free -h | grep "Mem:")
    echo -e "${CYAN}🧠 Memory: $memory_info${NC}"
    
    # Disk usage
    disk_info=$(df -h / | tail -1)
    echo -e "${CYAN}💽 Disk: $disk_info${NC}"
    
    # GPU status (if available)
    if command -v nvidia-smi &> /dev/null; then
        gpu_info=$(nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader,nounits | head -1)
        echo -e "${CYAN}🎮 GPU: $gpu_info${NC}"
    fi
    
    # Load average
    load_avg=$(uptime | awk -F'load average:' '{print $2}')
    echo -e "${CYAN}⚡ Load Average:$load_avg${NC}"
    echo ""
}

# Function to check directory structure
check_directories() {
    echo -e "${BLUE}📁 DIRECTORY STRUCTURE${NC}"
    echo -e "${BLUE}======================${NC}"
    
    directories=("config" "scripts" "output/images" "output/audio" "logs")
    
    for dir in "${directories[@]}"; do
        if [ -d "$dir" ]; then
            file_count=$(find "$dir" -type f | wc -l)
            echo -e "${GREEN}✅ $dir ($file_count files)${NC}"
        else
            echo -e "${RED}❌ $dir (missing)${NC}"
        fi
    done
    echo ""
}

# Function to show installation phases
show_installation_phases() {
    echo -e "${BLUE}🚀 INSTALLATION PHASES${NC}"
    echo -e "${BLUE}======================${NC}"
    
    phases=(
        "PHASE 1: Core AI Models (Ollama)"
        "PHASE 2: Image Generation (Stable Diffusion)"
        "PHASE 3: Music Generation (MusicGen + Bark)"
        "PHASE 4: Baker Street Integration"
        "PHASE 5: System Verification"
    )
    
    for i in "${!phases[@]}"; do
        phase_num=$((i + 1))
        phase_name="${phases[$i]}"
        
        if [ -f "$LOG_FILE" ] && grep -q "PHASE $phase_num:" "$LOG_FILE"; then
            if grep -q "PHASE $phase_num:.*completed successfully" "$LOG_FILE"; then
                echo -e "${GREEN}✅ $phase_name${NC}"
            elif grep -q "PHASE $phase_num:" "$LOG_FILE"; then
                echo -e "${YELLOW}⏳ $phase_name (in progress)${NC}"
            else
                echo -e "${CYAN}📋 $phase_name (queued)${NC}"
            fi
        else
            echo -e "${CYAN}📋 $phase_name (queued)${NC}"
        fi
    done
    echo ""
}

# Function to show quick stats
show_quick_stats() {
    echo -e "${BLUE}📊 QUICK STATISTICS${NC}"
    echo -e "${BLUE}===================${NC}"
    
    # Installation start time
    if [ -f "$LOG_FILE" ]; then
        start_time=$(grep "Installation started at:" "$LOG_FILE" | head -1 | cut -d':' -f2- | xargs)
        if [ -n "$start_time" ]; then
            echo -e "${CYAN}🕐 Started: $start_time${NC}"
        fi
        
        # Current phase
        current_phase=$(grep "PHASE [0-9]:" "$LOG_FILE" | tail -1 | cut -d':' -f1 | xargs)
        if [ -n "$current_phase" ]; then
            echo -e "${CYAN}📍 Current: $current_phase${NC}"
        fi
        
        # Log file size
        log_size=$(du -h "$LOG_FILE" | cut -f1)
        echo -e "${CYAN}📄 Log size: $log_size${NC}"
    fi
    echo ""
}

# Main monitoring loop
main() {
    while true; do
        print_header
        show_quick_stats
        check_ollama_status
        check_installation_progress
        show_installation_phases
        check_system_resources
        check_directories
        
        echo -e "${PURPLE}Press Ctrl+C to exit monitoring${NC}"
        echo -e "${PURPLE}Refreshing in 10 seconds...${NC}"
        
        sleep 10
    done
}

# Handle Ctrl+C gracefully
trap 'echo -e "\n${GREEN}🔬 Monitoring stopped. Baker Street Laboratory installation continues in background.${NC}"; exit 0' INT

# Run main function
main
