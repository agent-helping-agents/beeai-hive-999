#!/bin/bash

# Baker Street Laboratory - Music Generation Setup
# Installs and configures music generation for psychedelic detective atmosphere

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
MUSICGEN_DIR="$HOME/musicgen"
BARK_DIR="$HOME/bark"
LOG_FILE="logs/music-generation-setup.log"

# Create necessary directories
mkdir -p logs
mkdir -p config/music-generation
mkdir -p output/audio

echo -e "${BLUE}🎵 Baker Street Laboratory - Music Generation Setup${NC}"
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
    
    # Check ffmpeg
    if ! command -v ffmpeg &> /dev/null; then
        log_message "${YELLOW}⚠️  Installing ffmpeg...${NC}"
        sudo apt-get update && sudo apt-get install -y ffmpeg
    fi
    
    log_message "${GREEN}✅ System requirements check passed${NC}"
}

# Function to install MusicGen
install_musicgen() {
    log_message "${BLUE}📥 Installing MusicGen for music generation...${NC}"
    
    # Install required packages
    pip3 install --upgrade pip
    pip3 install torch torchvision torchaudio
    pip3 install transformers
    pip3 install scipy
    pip3 install librosa
    pip3 install soundfile
    
    # Install MusicGen
    pip3 install musicgen
    
    log_message "${GREEN}✅ MusicGen installation completed${NC}"
}

# Function to install Bark for sound effects
install_bark() {
    log_message "${BLUE}📥 Installing Bark for sound effects and speech...${NC}"
    
    # Install Bark
    pip3 install git+https://github.com/suno-ai/bark.git
    
    log_message "${GREEN}✅ Bark installation completed${NC}"
}

# Function to create music generation scripts
create_music_scripts() {
    log_message "${BLUE}⚙️  Creating music generation scripts...${NC}"
    
    # Create MusicGen script
    cat > "scripts/generate-music.py" << 'EOF'
#!/usr/bin/env python3
"""
Baker Street Laboratory - Music Generation
Generates psychedelic detective atmosphere music using MusicGen
"""

import torch
from transformers import MusicgenForConditionalGeneration, AutoProcessor
import scipy.io.wavfile
import argparse
import yaml
from pathlib import Path
import numpy as np

class BakerStreetMusicGenerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.processor = None
        self.config = self.load_config()
        
    def load_config(self):
        config_path = Path("config/music-generation/baker-street-music.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}
    
    def load_model(self, model_size="medium"):
        """Load MusicGen model"""
        print(f"🎵 Loading MusicGen {model_size} model...")
        
        model_name = f"facebook/musicgen-{model_size}"
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_name)
        self.processor = AutoProcessor.from_pretrained(model_name)
        
        if self.device == "cuda":
            self.model = self.model.to(self.device)
        
        print(f"✅ Model loaded on {self.device}")
    
    def generate_music(self, prompt, duration=30, output_path=None):
        """Generate music based on text prompt"""
        
        if self.model is None:
            self.load_model()
        
        print(f"🎼 Generating music: {prompt}")
        
        # Process prompt
        inputs = self.processor(
            text=[prompt],
            padding=True,
            return_tensors="pt",
        )
        
        if self.device == "cuda":
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Generate audio
        with torch.no_grad():
            audio_values = self.model.generate(
                **inputs,
                max_new_tokens=int(duration * 50),  # Approximate tokens per second
                do_sample=True,
                guidance_scale=3.0,
            )
        
        # Convert to numpy array
        audio_array = audio_values[0, 0].cpu().numpy()
        
        # Save audio file
        if output_path is None:
            output_path = f"output/audio/generated_music_{hash(prompt) % 10000}.wav"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Normalize audio
        audio_array = audio_array / np.max(np.abs(audio_array))
        
        # Save as WAV file (32kHz sample rate)
        scipy.io.wavfile.write(str(output_path), 32000, audio_array)
        
        print(f"✅ Music saved: {output_path}")
        return str(output_path)

def main():
    parser = argparse.ArgumentParser(description="Generate Baker Street Laboratory music")
    parser.add_argument("prompt", help="Text description of the music to generate")
    parser.add_argument("--duration", type=int, default=30, help="Duration in seconds")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--model-size", default="medium", choices=["small", "medium", "large"], help="Model size")
    
    args = parser.parse_args()
    
    generator = BakerStreetMusicGenerator()
    generator.load_model(args.model_size)
    
    result = generator.generate_music(args.prompt, args.duration, args.output)
    
    if result:
        print(f"🎵 Generated music: {result}")
    else:
        print("❌ Failed to generate music")

if __name__ == "__main__":
    main()
EOF

    chmod +x "scripts/generate-music.py"
    
    # Create Bark sound effects script
    cat > "scripts/generate-sound-effects.py" << 'EOF'
#!/usr/bin/env python3
"""
Baker Street Laboratory - Sound Effects Generation
Generates sound effects and speech using Bark
"""

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import argparse
from pathlib import Path
import numpy as np

class BakerStreetSoundGenerator:
    def __init__(self):
        self.sample_rate = SAMPLE_RATE
        self.models_loaded = False
    
    def load_models(self):
        """Load Bark models"""
        if not self.models_loaded:
            print("🔊 Loading Bark models...")
            preload_models()
            self.models_loaded = True
            print("✅ Bark models loaded")
    
    def generate_speech(self, text, voice_preset="v2/en_speaker_6", output_path=None):
        """Generate speech from text"""
        
        self.load_models()
        
        print(f"🗣️  Generating speech: {text[:50]}...")
        
        # Generate audio
        audio_array = generate_audio(text, history_prompt=voice_preset)
        
        # Save audio file
        if output_path is None:
            output_path = f"output/audio/speech_{hash(text) % 10000}.wav"
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Normalize and save
        audio_array = audio_array / np.max(np.abs(audio_array))
        write_wav(str(output_path), self.sample_rate, audio_array)
        
        print(f"✅ Speech saved: {output_path}")
        return str(output_path)
    
    def generate_sound_effect(self, description, output_path=None):
        """Generate sound effect from description"""
        
        # Use special sound effect prompts
        sound_prompt = f"[sound effect: {description}]"
        
        return self.generate_speech(sound_prompt, voice_preset="v2/en_speaker_9", output_path=output_path)

def main():
    parser = argparse.ArgumentParser(description="Generate Baker Street Laboratory sound effects")
    parser.add_argument("text", help="Text to convert to speech or sound effect description")
    parser.add_argument("--type", choices=["speech", "sound"], default="speech", help="Type of audio to generate")
    parser.add_argument("--voice", default="v2/en_speaker_6", help="Voice preset for speech")
    parser.add_argument("--output", help="Output file path")
    
    args = parser.parse_args()
    
    generator = BakerStreetSoundGenerator()
    
    if args.type == "speech":
        result = generator.generate_speech(args.text, args.voice, args.output)
    else:
        result = generator.generate_sound_effect(args.text, args.output)
    
    if result:
        print(f"🔊 Generated audio: {result}")
    else:
        print("❌ Failed to generate audio")

if __name__ == "__main__":
    main()
EOF

    chmod +x "scripts/generate-sound-effects.py"
    
    log_message "${GREEN}✅ Music generation scripts created${NC}"
}

# Function to create configuration files
create_config() {
    log_message "${BLUE}⚙️  Creating music configuration...${NC}"
    
    # Create music generation config
    cat > "config/music-generation/baker-street-music.yaml" << 'EOF'
# Baker Street Laboratory - Music Generation Configuration
# Prompts and settings for psychedelic detective atmosphere

music_styles:
  psychedelic_ambient:
    prompt: "ambient psychedelic music, dreamy synthesizers, ethereal pads, mysterious atmosphere, detective investigation mood"
    duration: 60
    
  detective_noir:
    prompt: "film noir detective music, jazz saxophone, dark piano, mysterious bass, urban night atmosphere"
    duration: 45
    
  research_focus:
    prompt: "focused study music, minimal ambient, soft electronic textures, concentration enhancing, laboratory atmosphere"
    duration: 120
    
  investigation_tension:
    prompt: "suspenseful investigation music, building tension, mysterious strings, detective thriller soundtrack"
    duration: 30
    
  psychedelic_discovery:
    prompt: "psychedelic discovery music, colorful synthesizers, evolving textures, eureka moment, scientific breakthrough"
    duration: 45
    
  data_analysis:
    prompt: "data analysis background music, rhythmic patterns, digital textures, computational thinking, algorithmic beats"
    duration: 90

sound_effects:
  typing:
    description: "keyboard typing sounds, research work, data entry"
    
  page_turn:
    description: "paper pages turning, book research, document review"
    
  laboratory:
    description: "laboratory equipment sounds, beakers, scientific instruments"
    
  discovery:
    description: "eureka moment sound, discovery chime, breakthrough notification"
    
  investigation:
    description: "detective investigation sounds, magnifying glass, evidence examination"
    
  ambient_lab:
    description: "ambient laboratory sounds, quiet humming, scientific atmosphere"

voice_presets:
  detective_narrator: "v2/en_speaker_6"  # Deep, authoritative voice
  scientist: "v2/en_speaker_3"           # Clear, analytical voice
  assistant: "v2/en_speaker_1"           # Friendly, helpful voice
  mysterious: "v2/en_speaker_9"          # Mysterious, atmospheric voice

usage_scenarios:
  morning_research:
    music: "research_focus"
    duration: 120
    description: "Background music for morning research sessions"
    
  investigation_phase:
    music: "detective_noir"
    duration: 45
    description: "Music for active investigation and analysis"
    
  data_processing:
    music: "data_analysis"
    duration: 90
    description: "Rhythmic music for data processing tasks"
    
  breakthrough_moment:
    music: "psychedelic_discovery"
    duration: 30
    description: "Celebratory music for research breakthroughs"
    
  ambient_work:
    music: "psychedelic_ambient"
    duration: 60
    description: "General ambient music for focused work"

settings:
  default_model_size: "medium"
  default_duration: 60
  output_format: "wav"
  sample_rate: 32000
  normalize_audio: true
EOF

    log_message "${GREEN}✅ Configuration files created${NC}"
}

# Function to create usage examples
create_examples() {
    log_message "${BLUE}📝 Creating usage examples...${NC}"
    
    # Create example script
    cat > "scripts/baker-street-audio-examples.sh" << 'EOF'
#!/bin/bash

# Baker Street Laboratory - Audio Generation Examples
# Demonstrates various audio generation capabilities

echo "🎵 Baker Street Laboratory - Audio Examples"
echo "=========================================="

# Generate background music for different scenarios
echo "🎼 Generating background music..."

# Research session music
python3 scripts/generate-music.py \
    "ambient psychedelic music for focused research, dreamy synthesizers, laboratory atmosphere" \
    --duration 60 \
    --output "output/audio/research_session.wav"

# Investigation music
python3 scripts/generate-music.py \
    "detective noir investigation music, mysterious jazz, urban night atmosphere" \
    --duration 45 \
    --output "output/audio/investigation_theme.wav"

# Data analysis music
python3 scripts/generate-music.py \
    "rhythmic data analysis music, digital patterns, computational beats" \
    --duration 90 \
    --output "output/audio/data_analysis.wav"

# Generate sound effects
echo "🔊 Generating sound effects..."

# Laboratory sounds
python3 scripts/generate-sound-effects.py \
    "laboratory equipment humming, scientific atmosphere" \
    --type sound \
    --output "output/audio/lab_ambient.wav"

# Discovery sound
python3 scripts/generate-sound-effects.py \
    "eureka moment, breakthrough discovery chime" \
    --type sound \
    --output "output/audio/discovery.wav"

# Generate speech examples
echo "🗣️  Generating speech examples..."

# Detective narration
python3 scripts/generate-sound-effects.py \
    "The investigation reveals fascinating patterns in the data, leading us deeper into the mystery." \
    --type speech \
    --voice "v2/en_speaker_6" \
    --output "output/audio/detective_narration.wav"

# Research summary
python3 scripts/generate-sound-effects.py \
    "Analysis complete. The results show significant correlations in the psychedelic research data." \
    --type speech \
    --voice "v2/en_speaker_3" \
    --output "output/audio/research_summary.wav"

echo "✅ Audio examples generated in output/audio/"
echo "🎧 Play the files to test the Baker Street Laboratory audio system!"
EOF

    chmod +x "scripts/baker-street-audio-examples.sh"
    
    log_message "${GREEN}✅ Usage examples created${NC}"
}

# Function to test installation
test_installation() {
    log_message "${BLUE}🧪 Testing music generation setup...${NC}"
    
    # Test MusicGen
    log_message "${YELLOW}🎵 Testing MusicGen...${NC}"
    python3 -c "
import torch
from transformers import MusicgenForConditionalGeneration
print('✅ MusicGen dependencies working')
"
    
    # Test Bark
    log_message "${YELLOW}🔊 Testing Bark...${NC}"
    python3 -c "
from bark import generate_audio
print('✅ Bark dependencies working')
"
    
    log_message "${GREEN}✅ Installation test completed${NC}"
}

# Main installation process
main() {
    log_message "${BLUE}🎵 Starting Baker Street Laboratory Music Generation Setup${NC}"
    log_message "${BLUE}Setup started at: $(date)${NC}"
    
    check_requirements
    install_musicgen
    install_bark
    create_music_scripts
    create_config
    create_examples
    test_installation
    
    log_message "${BLUE}📊 SETUP SUMMARY${NC}"
    log_message "${BLUE}===============${NC}"
    log_message "${GREEN}✅ MusicGen installed for music generation${NC}"
    log_message "${GREEN}✅ Bark installed for sound effects and speech${NC}"
    log_message "${GREEN}✅ Baker Street audio scripts created${NC}"
    log_message "${GREEN}✅ Configuration and examples ready${NC}"
    
    log_message "${BLUE}🚀 USAGE INSTRUCTIONS${NC}"
    log_message "${BLUE}===================${NC}"
    log_message "${YELLOW}1. Generate music: python3 scripts/generate-music.py 'your prompt'${NC}"
    log_message "${YELLOW}2. Generate speech: python3 scripts/generate-sound-effects.py 'text' --type speech${NC}"
    log_message "${YELLOW}3. Generate sounds: python3 scripts/generate-sound-effects.py 'description' --type sound${NC}"
    log_message "${YELLOW}4. Run examples: ./scripts/baker-street-audio-examples.sh${NC}"
    
    log_message "${BLUE}Setup completed at: $(date)${NC}"
    log_message "${GREEN}🎉 Music generation system ready for Baker Street Laboratory!${NC}"
}

# Run main function
main "$@"
