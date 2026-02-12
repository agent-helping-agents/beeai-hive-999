#!/bin/bash

# Baker Street Laboratory - Master Installation Script
# Complete AI model ecosystem installation and integration

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
PROJECT_ROOT="$(pwd)"
LOG_FILE="logs/master-installation.log"

# Create necessary directories
mkdir -p logs
mkdir -p output/images
mkdir -p output/audio
mkdir -p output/reports

echo -e "${PURPLE}🚀 BAKER STREET LABORATORY - MASTER AI INSTALLATION${NC}"
echo -e "${PURPLE}===================================================${NC}"
echo -e "${CYAN}Complete AI model ecosystem for psychedelic detective research${NC}"
echo ""

# Function to log messages
log_message() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Function to print section header
print_section() {
    echo ""
    log_message "${BLUE}$1${NC}"
    log_message "${BLUE}$(printf '=%.0s' $(seq 1 ${#1}))${NC}"
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

# Function to wait for user confirmation
wait_for_confirmation() {
    echo ""
    read -p "Press Enter to continue with $1, or Ctrl+C to abort..."
    echo ""
}

# Main installation process
main() {
    log_message "${PURPLE}🎯 Starting Baker Street Laboratory Master Installation${NC}"
    log_message "${PURPLE}Installation started at: $(date)${NC}"
    
    # Phase 1: Core AI Models (Ollama)
    print_section "PHASE 1: CORE AI MODELS INSTALLATION"
    log_message "${YELLOW}Installing and configuring all Ollama models...${NC}"
    
    wait_for_confirmation "Ollama models installation"
    
    chmod +x scripts/install-ai-models.sh
    ./scripts/install-ai-models.sh
    check_success "Ollama models installation"
    
    # Phase 2: Image Generation Setup
    print_section "PHASE 2: IMAGE GENERATION SETUP"
    log_message "${YELLOW}Setting up Stable Diffusion for psychedelic comic art...${NC}"
    
    wait_for_confirmation "image generation setup"
    
    chmod +x scripts/setup-image-generation.sh
    ./scripts/setup-image-generation.sh
    check_success "Image generation setup"
    
    # Phase 3: Music Generation Setup
    print_section "PHASE 3: MUSIC GENERATION SETUP"
    log_message "${YELLOW}Setting up music and sound effects generation...${NC}"
    
    wait_for_confirmation "music generation setup"
    
    chmod +x scripts/setup-music-generation.sh
    ./scripts/setup-music-generation.sh
    check_success "Music generation setup"
    
    # Phase 4: Baker Street Integration
    print_section "PHASE 4: BAKER STREET LABORATORY INTEGRATION"
    log_message "${YELLOW}Creating Baker Street Laboratory integration module...${NC}"
    
    create_baker_street_integration
    check_success "Baker Street integration"
    
    # Phase 5: System Verification
    print_section "PHASE 5: SYSTEM VERIFICATION"
    log_message "${YELLOW}Testing complete AI ecosystem...${NC}"
    
    run_system_verification
    check_success "System verification"
    
    # Installation Summary
    print_section "INSTALLATION COMPLETE"
    
    log_message "${GREEN}🎉 BAKER STREET LABORATORY AI ECOSYSTEM READY!${NC}"
    log_message "${GREEN}================================================${NC}"
    
    log_message "${CYAN}📊 INSTALLED COMPONENTS:${NC}"
    log_message "${GREEN}✅ 11 AI models (vision, reasoning, creative, legal, etc.)${NC}"
    log_message "${GREEN}✅ Image generation (Stable Diffusion + psychedelic art models)${NC}"
    log_message "${GREEN}✅ Music generation (MusicGen + Bark for sound effects)${NC}"
    log_message "${GREEN}✅ Baker Street Laboratory desktop integration${NC}"
    log_message "${GREEN}✅ Complete API ecosystem with hardware optimization${NC}"
    
    log_message "${CYAN}🚀 QUICK START GUIDE:${NC}"
    log_message "${YELLOW}1. Start services: ./scripts/start-baker-street.sh${NC}"
    log_message "${YELLOW}2. Run examples: ./scripts/run-examples.sh${NC}"
    log_message "${YELLOW}3. Generate content: python3 scripts/baker-street-ai.py${NC}"
    log_message "${YELLOW}4. Open desktop app: Launch Baker Street Laboratory${NC}"
    
    log_message "${PURPLE}Installation completed at: $(date)${NC}"
    log_message "${GREEN}🔬 Ready for psychedelic detective research!${NC}"
}

# Function to create Baker Street integration
create_baker_street_integration() {
    log_message "${BLUE}🔧 Creating Baker Street Laboratory integration...${NC}"
    
    # Create main integration script
    cat > "scripts/baker-street-ai.py" << 'EOF'
#!/usr/bin/env python3
"""
Baker Street Laboratory - AI Integration Module
Complete AI ecosystem for psychedelic detective research
"""

import requests
import json
import yaml
import argparse
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

class BakerStreetAI:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.webui_url = "http://localhost:7860"
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from YAML files"""
        config = {}
        config_files = [
            "config/ollama-models.yaml",
            "config/image-generation/baker-street-prompts.yaml",
            "config/music-generation/baker-street-music.yaml"
        ]
        
        for config_file in config_files:
            if Path(config_file).exists():
                with open(config_file, 'r') as f:
                    config.update(yaml.safe_load(f))
        
        return config
    
    def query_ai(self, prompt: str, model: str = "baker-street-hermes3") -> str:
        """Query AI model with prompt"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"Error: {e}"
    
    def analyze_image(self, image_path: str, question: str = "Describe this image") -> str:
        """Analyze image using vision model"""
        try:
            with open(image_path, 'rb') as f:
                import base64
                image_data = base64.b64encode(f.read()).decode()
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "baker-street-vision",
                    "prompt": question,
                    "images": [image_data],
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json().get("response", "")
        except Exception as e:
            return f"Error: {e}"
    
    def generate_image(self, scene_type: str, style: str = "amphetamemes") -> Optional[str]:
        """Generate psychedelic detective art"""
        try:
            result = subprocess.run([
                "python3", "scripts/generate-image.py",
                scene_type, "--style", style
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Extract file path from output
                for line in result.stdout.split('\n'):
                    if 'Generated image:' in line:
                        return line.split(': ')[-1].strip()
            return None
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def generate_music(self, prompt: str, duration: int = 60) -> Optional[str]:
        """Generate background music"""
        try:
            result = subprocess.run([
                "python3", "scripts/generate-music.py",
                prompt, "--duration", str(duration)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                # Extract file path from output
                for line in result.stdout.split('\n'):
                    if 'Generated music:' in line:
                        return line.split(': ')[-1].strip()
            return None
        except Exception as e:
            print(f"Error generating music: {e}")
            return None
    
    def research_workflow(self, query: str) -> Dict[str, Any]:
        """Complete research workflow"""
        print(f"🔍 Starting research workflow for: {query}")
        
        results = {
            "query": query,
            "analysis": None,
            "visual": None,
            "audio": None,
            "report": None
        }
        
        # Step 1: AI Analysis
        print("📊 Analyzing query...")
        results["analysis"] = self.query_ai(
            f"As a psychedelic detective researcher, analyze this query and provide insights: {query}",
            "baker-street-scientific"
        )
        
        # Step 2: Generate Visual
        print("🎨 Generating visual representation...")
        results["visual"] = self.generate_image("investigation", "amphetamemes")
        
        # Step 3: Generate Background Music
        print("🎵 Generating background music...")
        results["audio"] = self.generate_music(
            "psychedelic detective investigation music, mysterious atmosphere"
        )
        
        # Step 4: Create Report
        print("📝 Creating research report...")
        results["report"] = self.query_ai(
            f"Create an engaging research report in psychedelic detective style for: {query}\n\nAnalysis: {results['analysis']}",
            "baker-street-creative"
        )
        
        return results

def main():
    parser = argparse.ArgumentParser(description="Baker Street Laboratory AI System")
    parser.add_argument("--query", help="Research query to process")
    parser.add_argument("--model", default="baker-street-hermes3", help="AI model to use")
    parser.add_argument("--workflow", action="store_true", help="Run complete research workflow")
    
    args = parser.parse_args()
    
    ai = BakerStreetAI()
    
    if args.workflow and args.query:
        results = ai.research_workflow(args.query)
        print("\n🎉 Research workflow complete!")
        print(f"📊 Analysis: {len(results['analysis'])} characters")
        print(f"🎨 Visual: {results['visual']}")
        print(f"🎵 Audio: {results['audio']}")
        print(f"📝 Report: {len(results['report'])} characters")
        
    elif args.query:
        response = ai.query_ai(args.query, args.model)
        print(f"\n🤖 {args.model} response:")
        print(response)
    
    else:
        print("🔬 Baker Street Laboratory AI System Ready!")
        print("Use --query 'your question' to ask the AI")
        print("Use --workflow --query 'research topic' for complete analysis")

if __name__ == "__main__":
    main()
EOF

    chmod +x "scripts/baker-street-ai.py"
    
    # Create service startup script
    cat > "scripts/start-baker-street.sh" << 'EOF'
#!/bin/bash

# Baker Street Laboratory - Service Startup Script
# Starts all AI services for the complete ecosystem

echo "🚀 Starting Baker Street Laboratory AI Services..."

# Start Ollama service
echo "📡 Starting Ollama service..."
sudo systemctl start ollama || ollama serve &
sleep 5

# Start Stable Diffusion WebUI (if available)
if [ -d "$HOME/stable-diffusion-webui" ]; then
    echo "🎨 Starting Stable Diffusion WebUI..."
    cd "$HOME/stable-diffusion-webui"
    ./webui.sh --listen --api &
    cd - > /dev/null
fi

echo "✅ Baker Street Laboratory services started!"
echo "🔬 Ready for psychedelic detective research!"
EOF

    chmod +x "scripts/start-baker-street.sh"
    
    # Create examples script
    cat > "scripts/run-examples.sh" << 'EOF'
#!/bin/bash

# Baker Street Laboratory - Examples Script
# Demonstrates the complete AI ecosystem capabilities

echo "🧪 Baker Street Laboratory - AI Examples"
echo "======================================="

# Example 1: Basic AI Query
echo "🤖 Example 1: Basic AI Query"
python3 scripts/baker-street-ai.py --query "What are the key principles of psychedelic research?"

# Example 2: Complete Research Workflow
echo ""
echo "🔬 Example 2: Complete Research Workflow"
python3 scripts/baker-street-ai.py --workflow --query "The relationship between psychedelics and creativity"

# Example 3: Image Generation
echo ""
echo "🎨 Example 3: Image Generation"
python3 scripts/generate-image.py investigation --style amphetamemes

# Example 4: Music Generation
echo ""
echo "🎵 Example 4: Music Generation"
python3 scripts/generate-music.py "psychedelic detective investigation music" --duration 30

echo ""
echo "✅ Examples completed! Check output/ directory for generated content."
EOF

    chmod +x "scripts/run-examples.sh"
}

# Function to run system verification
run_system_verification() {
    log_message "${BLUE}🧪 Running system verification tests...${NC}"
    
    # Test Ollama models
    log_message "${YELLOW}Testing Ollama models...${NC}"
    if ollama list > /dev/null 2>&1; then
        model_count=$(ollama list | grep -c "baker-street" || echo "0")
        log_message "${GREEN}✅ Found $model_count Baker Street models${NC}"
    else
        log_message "${RED}❌ Ollama not responding${NC}"
        return 1
    fi
    
    # Test Python dependencies
    log_message "${YELLOW}Testing Python dependencies...${NC}"
    python3 -c "import yaml, requests, torch; print('✅ Core dependencies OK')" 2>/dev/null || {
        log_message "${RED}❌ Missing Python dependencies${NC}"
        return 1
    }
    
    # Test directory structure
    log_message "${YELLOW}Testing directory structure...${NC}"
    required_dirs=("config" "scripts" "output/images" "output/audio" "logs")
    for dir in "${required_dirs[@]}"; do
        if [ -d "$dir" ]; then
            log_message "${GREEN}✅ Directory $dir exists${NC}"
        else
            log_message "${RED}❌ Missing directory $dir${NC}"
            return 1
        fi
    done
    
    log_message "${GREEN}✅ System verification passed${NC}"
    return 0
}

# Run main function
main "$@"
