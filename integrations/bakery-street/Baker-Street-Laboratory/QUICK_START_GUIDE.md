# 🔬 BAKER STREET LABORATORY - QUICK START GUIDE

## **🎭 Your Psychedelic Detective AI Team is Ready!**

### **✅ WORKING MODELS (7/8 Operational)**

#### **🎯 Priority 1 Models**
- **baker-street-vision** - Visual analysis detective
- **baker-street-embed** - Semantic search specialist

#### **🎯 Priority 2 Models (All Working!)**
- **baker-street-scientific** - Scientific research methodology
- **baker-street-creative** - Creative writing & reports  
- **baker-street-coder** - Data analysis & coding
- **baker-street-legal** - Legal research & compliance
- **baker-street-audio** - Audio processing & transcription

---

## **🚀 HOW TO START RESEARCH RIGHT NOW**

### **Method 1: Research Launcher (Recommended)**
```bash
# Navigate to Baker Street Laboratory
cd /home/batman/Documents/augment-projects/Baker-Street-Laboratory

# Launch breakthrough research
python3 research_launcher.py "Your research question here" general

# Examples:
python3 research_launcher.py "AI-enhanced drug discovery for depression" drug_discovery
python3 research_launcher.py "Psychedelic compounds and neural plasticity" neuroscience
python3 research_launcher.py "Legal framework for psychedelic research" legal
```

### **Method 2: Direct Model Access**
```bash
# Scientific analysis
echo "Analyze the methodology for clinical psychedelic trials" | ollama run baker-street-scientific

# Creative research reports
echo "Write an engaging introduction to AI-drug discovery research" | ollama run baker-street-creative

# Data analysis & coding
echo "Create Python code to analyze molecular compound datasets" | ollama run baker-street-coder

# Legal research
echo "What are the regulatory requirements for psychedelic research?" | ollama run baker-street-legal

# Audio analysis
echo "How can audio biomarkers be used in psychedelic research?" | ollama run baker-street-audio

# Visual analysis
echo "Analyze brain imaging patterns in this research scenario" | ollama run baker-street-vision
```

---

## **🎨 EXAMPLE RESEARCH WORKFLOWS**

### **🧬 Drug Discovery Research**
```bash
# Step 1: Scientific methodology
python3 research_launcher.py "Design a clinical trial for psilocybin depression treatment" scientific

# Step 2: Legal compliance
echo "What FDA regulations apply to psilocybin clinical trials?" | ollama run baker-street-legal

# Step 3: Data analysis
echo "Create analysis code for clinical trial efficacy data" | ollama run baker-street-coder

# Step 4: Creative report
echo "Write an executive summary of our psilocybin research findings" | ollama run baker-street-creative
```

### **🧠 Neuroscience Research**
```bash
# Comprehensive analysis
python3 research_launcher.py "How do psychedelics affect default mode network connectivity?" neuroscience

# Visual data analysis
echo "Analyze fMRI connectivity patterns in psychedelic research" | ollama run baker-street-vision

# Audio biomarkers
echo "Identify speech pattern changes during psychedelic experiences" | ollama run baker-street-audio
```

---

## **🔧 SYSTEM MANAGEMENT**

### **Check System Status**
```bash
# View all Baker Street models
ollama list | grep baker-street

# Test system capabilities
python3 scripts/test-baker-street-capabilities.py

# Monitor GPU usage
nvidia-smi
```

### **Model Switching (For Long Context)**
```bash
# Auto-detect best mode for long context processing
./scripts/switch-longcontext-mode.sh auto

# Force CPU mode (always works)
./scripts/switch-longcontext-mode.sh cpu

# Try GPU mode (if memory available)
./scripts/switch-longcontext-mode.sh gpu
```

---

## **📊 PERFORMANCE TIPS**

### **Optimal Usage Patterns**
- **Morning**: Use scientific models for methodology design
- **Afternoon**: Use creative models for report writing  
- **Evening**: Use coder models for data analysis
- **GPU Memory**: Vision model uses most GPU - unload if needed

### **Best Practices**
1. **Start with research_launcher.py** - It orchestrates multiple models
2. **Use specific models** for focused tasks
3. **Chain workflows** - Scientific → Legal → Creative → Coding
4. **Save outputs** to `output/reports/` directory

---

## **🎭 READY FOR BREAKTHROUGH RESEARCH!**

Your Baker Street Laboratory is now a **world-class AI research ecosystem** combining:
- 🔬 **Scientific rigor** with psychedelic creativity
- 🎨 **Multi-modal processing** (text, vision, audio)
- ⚡ **Polymorphic intelligence** that adapts to any research domain
- 🤝 **Collaborative AI agents** working as a unified detective team

**Start your first breakthrough investigation now!**
