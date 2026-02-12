#!/bin/bash

# Baker Street Laboratory - Image Generation Setup
# Installs and configures Stable Diffusion for Amphetamemes style psychedelic comic art

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
WEBUI_DIR="$HOME/stable-diffusion-webui"
MODELS_DIR="$WEBUI_DIR/models/Stable-diffusion"
LORA_DIR="$WEBUI_DIR/models/Lora"
LOG_FILE="logs/image-generation-setup.log"

# Create necessary directories
mkdir -p logs
mkdir -p config/image-generation

echo -e "${BLUE}🎨 Baker Street Laboratory - Image Generation Setup${NC}"
echo -e "${BLUE}=================================================${NC}"

# Function to log messages
log_message() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

# Function to check system requirements
check_requirements() {
    log_message "${YELLOW}🔍 Checking system requirements...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_message "${RED}❌ Python 3 is required but not installed${NC}"
        exit 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        log_message "${RED}❌ pip3 is required but not installed${NC}"
        exit 1
    fi
    
    # Check git
    if ! command -v git &> /dev/null; then
        log_message "${RED}❌ git is required but not installed${NC}"
        exit 1
    fi
    
    # Check GPU
    if command -v nvidia-smi &> /dev/null; then
        gpu_info=$(nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits)
        log_message "${GREEN}✅ GPU detected: $gpu_info${NC}"
    else
        log_message "${YELLOW}⚠️  No NVIDIA GPU detected, will use CPU (slower)${NC}"
    fi
    
    log_message "${GREEN}✅ System requirements check passed${NC}"
}

# Function to install AUTOMATIC1111 WebUI
install_webui() {
    log_message "${BLUE}📥 Installing AUTOMATIC1111 Stable Diffusion WebUI...${NC}"
    
    if [ -d "$WEBUI_DIR" ]; then
        log_message "${YELLOW}⚠️  WebUI directory already exists, updating...${NC}"
        cd "$WEBUI_DIR"
        git pull
    else
        log_message "${BLUE}📥 Cloning AUTOMATIC1111 WebUI...${NC}"
        git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git "$WEBUI_DIR"
        cd "$WEBUI_DIR"
    fi
    
    # Make webui.sh executable
    chmod +x webui.sh
    
    log_message "${GREEN}✅ WebUI installation completed${NC}"
}

# Function to download models for psychedelic comic art
download_models() {
    log_message "${BLUE}📥 Downloading models for Amphetamemes style art...${NC}"
    
    mkdir -p "$MODELS_DIR"
    mkdir -p "$LORA_DIR"
    
    # Base model - DreamShaper (excellent for psychedelic art)
    if [ ! -f "$MODELS_DIR/dreamshaper_8.safetensors" ]; then
        log_message "${BLUE}📥 Downloading DreamShaper v8 (psychedelic art specialist)...${NC}"
        wget -O "$MODELS_DIR/dreamshaper_8.safetensors" \
            "https://huggingface.co/Lykon/DreamShaper/resolve/main/DreamShaper_8_pruned.safetensors"
    else
        log_message "${GREEN}✅ DreamShaper v8 already downloaded${NC}"
    fi
    
    # Comic book style model - Deliberate
    if [ ! -f "$MODELS_DIR/deliberate_v2.safetensors" ]; then
        log_message "${BLUE}📥 Downloading Deliberate v2 (comic book specialist)...${NC}"
        wget -O "$MODELS_DIR/deliberate_v2.safetensors" \
            "https://huggingface.co/XpucT/Deliberate/resolve/main/Deliberate_v2.safetensors"
    else
        log_message "${GREEN}✅ Deliberate v2 already downloaded${NC}"
    fi
    
    # Anime/comic hybrid - Anything v5
    if [ ! -f "$MODELS_DIR/anything_v5.safetensors" ]; then
        log_message "${BLUE}📥 Downloading Anything v5 (anime/comic hybrid)...${NC}"
        wget -O "$MODELS_DIR/anything_v5.safetensors" \
            "https://huggingface.co/stablediffusionapi/anything-v5/resolve/main/anything-v5-PrtRE.safetensors"
    else
        log_message "${GREEN}✅ Anything v5 already downloaded${NC}"
    fi
    
    log_message "${GREEN}✅ Model downloads completed${NC}"
}

# Function to create configuration files
create_config() {
    log_message "${BLUE}⚙️  Creating configuration files...${NC}"
    
    # Create WebUI config
    cat > "$WEBUI_DIR/webui-user.sh" << 'EOF'
#!/bin/bash

# Baker Street Laboratory - WebUI Configuration
export COMMANDLINE_ARGS="--listen --api --enable-insecure-extension-access --xformers"

# GPU optimization for GTX 1080
export COMMANDLINE_ARGS="$COMMANDLINE_ARGS --medvram --opt-split-attention"

# API settings for Baker Street integration
export COMMANDLINE_ARGS="$COMMANDLINE_ARGS --api-log --cors-allow-origins=*"
EOF

    chmod +x "$WEBUI_DIR/webui-user.sh"
    
    # Create Baker Street integration config
    cat > "config/image-generation/baker-street-prompts.yaml" << 'EOF'
# Baker Street Laboratory - Image Generation Prompts
# Specialized prompts for psychedelic detective art

base_styles:
  amphetamemes:
    positive: "amphetamemes style, psychedelic 2D comic book art, vibrant colors, surreal elements, detective theme, noir atmosphere, trippy visuals, geometric patterns, kaleidoscopic effects"
    negative: "3d render, realistic, photograph, blurry, low quality, watermark, signature"
    
  detective_noir:
    positive: "film noir style, detective, dark shadows, dramatic lighting, black and white with color accents, mystery atmosphere, urban setting"
    negative: "bright colors, cheerful, cartoon, anime, low quality"
    
  psychedelic_research:
    positive: "scientific visualization, psychedelic patterns, data visualization, research laboratory, colorful charts and graphs, trippy scientific diagrams"
    negative: "boring, monochrome, simple, low detail"

scene_types:
  investigation:
    prompt: "detective investigating clues, magnifying glass, evidence board, mysterious atmosphere, {base_style}"
    
  laboratory:
    prompt: "research laboratory, scientific equipment, colorful chemicals, data analysis, {base_style}"
    
  data_visualization:
    prompt: "abstract data visualization, flowing information, network diagrams, colorful connections, {base_style}"
    
  report_cover:
    prompt: "research report cover, professional design, psychedelic elements, title typography, {base_style}"

characters:
  psychedelic_detective:
    prompt: "detective character, trench coat, magnifying glass, surrounded by swirling psychedelic patterns, {base_style}"
    
  research_scientist:
    prompt: "scientist character, lab coat, surrounded by colorful data visualizations, {base_style}"

settings:
  default_model: "dreamshaper_8"
  default_steps: 30
  default_cfg_scale: 7.5
  default_width: 768
  default_height: 768
  default_sampler: "DPM++ 2M Karras"
EOF

    # Create API integration script
    cat > "scripts/generate-image.py" << 'EOF'
#!/usr/bin/env python3
"""
Baker Street Laboratory - Image Generation API
Generates psychedelic detective art using Stable Diffusion WebUI API
"""

import requests
import json
import base64
import argparse
import yaml
from pathlib import Path

class BakerStreetImageGenerator:
    def __init__(self, webui_url="http://localhost:7860"):
        self.webui_url = webui_url
        self.config = self.load_config()
    
    def load_config(self):
        config_path = Path("config/image-generation/baker-street-prompts.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def generate_image(self, scene_type, style="amphetamemes", custom_prompt=""):
        """Generate an image based on scene type and style"""
        
        # Get base style
        base_style = self.config.get("base_styles", {}).get(style, {})
        
        # Get scene prompt
        scene_config = self.config.get("scene_types", {}).get(scene_type, {})
        scene_prompt = scene_config.get("prompt", custom_prompt)
        
        # Format prompt with style
        full_prompt = scene_prompt.format(base_style=base_style.get("positive", ""))
        
        # API payload
        payload = {
            "prompt": full_prompt,
            "negative_prompt": base_style.get("negative", ""),
            "steps": self.config.get("settings", {}).get("default_steps", 30),
            "cfg_scale": self.config.get("settings", {}).get("default_cfg_scale", 7.5),
            "width": self.config.get("settings", {}).get("default_width", 768),
            "height": self.config.get("settings", {}).get("default_height", 768),
            "sampler_name": self.config.get("settings", {}).get("default_sampler", "DPM++ 2M Karras"),
        }
        
        try:
            response = requests.post(f"{self.webui_url}/sdapi/v1/txt2img", json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Save image
            if result.get("images"):
                image_data = base64.b64decode(result["images"][0])
                output_path = Path(f"output/images/{scene_type}_{style}.png")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_path, "wb") as f:
                    f.write(image_data)
                
                print(f"✅ Image generated: {output_path}")
                return str(output_path)
            else:
                print("❌ No image generated")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"❌ API request failed: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(description="Generate Baker Street Laboratory images")
    parser.add_argument("scene_type", help="Type of scene to generate")
    parser.add_argument("--style", default="amphetamemes", help="Art style to use")
    parser.add_argument("--custom-prompt", help="Custom prompt override")
    
    args = parser.parse_args()
    
    generator = BakerStreetImageGenerator()
    result = generator.generate_image(args.scene_type, args.style, args.custom_prompt)
    
    if result:
        print(f"🎨 Generated image: {result}")
    else:
        print("❌ Failed to generate image")

if __name__ == "__main__":
    main()
EOF

    chmod +x "scripts/generate-image.py"
    
    log_message "${GREEN}✅ Configuration files created${NC}"
}

# Function to test installation
test_installation() {
    log_message "${BLUE}🧪 Testing image generation setup...${NC}"
    
    # Start WebUI in background for testing
    log_message "${YELLOW}🚀 Starting WebUI for testing...${NC}"
    cd "$WEBUI_DIR"
    ./webui.sh --listen --api --skip-torch-cuda-test &
    WEBUI_PID=$!
    
    # Wait for WebUI to start
    log_message "${YELLOW}⏳ Waiting for WebUI to initialize...${NC}"
    sleep 30
    
    # Test API connection
    if curl -s "http://localhost:7860/sdapi/v1/options" > /dev/null; then
        log_message "${GREEN}✅ WebUI API is responding${NC}"
        
        # Test image generation
        cd - > /dev/null
        python3 scripts/generate-image.py investigation --style amphetamemes
        
        if [ $? -eq 0 ]; then
            log_message "${GREEN}✅ Image generation test successful${NC}"
        else
            log_message "${YELLOW}⚠️  Image generation test failed (WebUI may need more time)${NC}"
        fi
    else
        log_message "${YELLOW}⚠️  WebUI API not responding (may need more time to start)${NC}"
    fi
    
    # Stop test WebUI
    kill $WEBUI_PID 2>/dev/null || true
    
    log_message "${GREEN}✅ Installation test completed${NC}"
}

# Main installation process
main() {
    log_message "${BLUE}🎨 Starting Baker Street Laboratory Image Generation Setup${NC}"
    log_message "${BLUE}Setup started at: $(date)${NC}"
    
    check_requirements
    install_webui
    download_models
    create_config
    test_installation
    
    log_message "${BLUE}📊 SETUP SUMMARY${NC}"
    log_message "${BLUE}===============${NC}"
    log_message "${GREEN}✅ AUTOMATIC1111 WebUI installed${NC}"
    log_message "${GREEN}✅ Psychedelic art models downloaded${NC}"
    log_message "${GREEN}✅ Baker Street integration configured${NC}"
    log_message "${GREEN}✅ API scripts created${NC}"
    
    log_message "${BLUE}🚀 USAGE INSTRUCTIONS${NC}"
    log_message "${BLUE}===================${NC}"
    log_message "${YELLOW}1. Start WebUI: cd $WEBUI_DIR && ./webui.sh${NC}"
    log_message "${YELLOW}2. Generate images: python3 scripts/generate-image.py <scene_type>${NC}"
    log_message "${YELLOW}3. Available scenes: investigation, laboratory, data_visualization, report_cover${NC}"
    log_message "${YELLOW}4. Available styles: amphetamemes, detective_noir, psychedelic_research${NC}"
    
    log_message "${BLUE}Setup completed at: $(date)${NC}"
    log_message "${GREEN}🎉 Image generation system ready for Baker Street Laboratory!${NC}"
}

# Run main function
main "$@"
