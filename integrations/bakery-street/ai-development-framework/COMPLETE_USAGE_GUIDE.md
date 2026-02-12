# 🧠 NeoSpiral AI Development Suite - Complete Usage Guide

## 🚀 Quick Access Commands

### Launch Tools

ai-menu # Interactive menu system
ai-code # OpenCode terminal AI
ai-cursor # Cursor IDE (if working)
ai-edit # Aider pair programmer

### Mathematical Demos

shannon # Shannon entropy analysis
stdp # STDP learning simulation
spiral # Spiral network topology

## 📋 Tool-by-Tool Usage Guide

### 1. OpenCode - Terminal AI Assistant
**Status**: ✅ Working (v0.5.29)
**Launch**: `ai-code` or `cd ~/ai-development && opencode`

**Basic Usage**:
- Type your coding questions directly
- Use `/edit filename.py` to edit files
- Use `/run command` to execute commands
- Type `/help` for available commands

**Example Session**:

opencode> Create a Python function to calculate factorial
opencode> /edit factorial.py
opencode> /run python factorial.py

### 2. Aider - AI Pair Programmer  
**Status**: ✅ Working (v0.86.1 after upgrade)
**Launch**: `ai-edit`

**Basic Usage**:

aider filename.py # Edit specific file
aider *.py # Edit multiple files
aider --model ollama/codellama:7b # Use local model

**Commands**:
- `/add filename.py` - Add file to session
- `/drop filename.py` - Remove file
- `/diff` - Show changes
- `/commit` - Commit changes to git
- `/help` - Show all commands

### 3. Ollama - Local LLMs
**Status**: ✅ Working (codellama:7b installed)
**Models Available**: 
- `codellama:7b` - Code generation and analysis
- Add more: `ollama pull deepseek-coder:6.7b`

**Usage**:

Interactive chat

ollama run codellama:7b
API calls

curl -X POST http://localhost:11434/api/generate
-H "Content-Type: application/json"
-d '{"model":"codellama:7b","prompt":"Explain quantum computing"}'

### 4. Mathematical Research Tools
**Status**: ✅ All working

#### Shannon Entropy Analysis

shannon # Quick demo
Or detailed usage:

cd ~/ai-development
source environments/ai-main/bin/activate
python tools/shannon_entropy.py

**Applications**:
- Analyze neuronal spike patterns
- Optimize neuromorphic systems
- Calculate information content

#### STDP Learning Simulation

stdp # Quick demo

**Features**:
- Four different STDP rules
- Weight update calculations
- Synaptic plasticity modeling

#### Spiral Network Topology

spiral # Quick demo

**Features**:
- Logarithmic spiral generation
- Hierarchical connectivity
- Network analysis metrics

## 🔧 Configuration and Customization

### OpenCode Configuration
Edit `~/.config/opencode/opencode.json`:

{
"provider": "ollama",
"model": "codellama:7b",
"providers": {
"ollama": {
"baseUrl": "http://localhost:11434"
}
},
"theme": "dark",
"permissions": {
"edit": "ask",
"bash": {
"python": "allow",
"git": "allow"
}
}
}

### Aider Configuration
Create `~/.aider.conf.yml`:

model: ollama/codellama:7b
editor-model: ollama/codellama:7b
dark-mode: true
git: true
auto-commits: false

## 🧪 Research Workflows

### Neuromorphic Computing Research

Activate neuromorphic environment

neuro-activate
Run mathematical simulations

shannon && stdp && spiral
Start research session

jupyter lab ~/ai-development/research/

### AI Development Workflow

Start development environment

ai-activate
Open project in Cursor (when fixed)

ai-cursor
Or use terminal tools

ai-code # For AI assistance
ai-edit # For direct file editing

## 🎯 Next Steps and Advanced Usage

### Add More Models

ollama pull deepseek-coder:6.7b
ollama pull mistral:7b
ollama pull phi:latest

### Cursor IDE Alternative (VS Code with AI)
Since Cursor has installation issues, use VS Code with AI extensions:


### Advanced Research
- Study Shannon entropy in neuromorphic systems
- Implement STDP learning in hardware simulators
- Develop spiral topology optimizations
- Create AI-driven security frameworks
### Support Resources
- **OpenCode**: https://opencode.ai/docs/
- **Aider**: https://aider.chat/docs/
- **Ollama**: https://ollama.ai/docs/
- **Mathematical research**: Papers in conversation links
