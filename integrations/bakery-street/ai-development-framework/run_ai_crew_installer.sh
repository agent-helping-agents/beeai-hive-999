#!/bin/bash

# AI Crew Installer Launcher
# Launches the automated agent crew to install additional AI repositories

echo "🧠 AI Crew Installer - Automated Repository Installation"
echo "========================================================"

# Check if we're in the right directory
if [ ! -f "ai_crew_installer.py" ]; then
    echo "❌ AI Crew Installer not found in current directory"
    echo "Please run this script from /home/booze/ai-development"
    exit 1
fi

# Check if AIOS environment exists
if [ ! -d "environments/aios-env" ]; then
    echo "❌ AIOS environment not found"
    echo "Please ensure AIOS is properly installed first"
    exit 1
fi

# Activate AIOS environment
echo "🔧 Activating AIOS environment..."
source environments/aios-env/bin/activate

# Check if AIOS is working
echo "🧪 Testing AIOS import..."
python -c "import aios; print(f'✅ AIOS {aios.__version__} loaded successfully')" || {
    echo "❌ AIOS import failed. Please fix AIOS installation first."
    exit 1
}

# Check if git is available
echo "🔍 Checking git availability..."
if ! command -v git &> /dev/null; then
    echo "❌ Git not found. Installing git..."
    sudo apt update && sudo apt install -y git
fi

echo "✅ Git available"

# Run the AI Crew Installer
echo "🚀 Launching AI Crew Installer..."
echo "This will install additional repositories to complete your AI development stack."
echo ""

python ai_crew_installer.py

# Check result
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 AI Crew Installer completed successfully!"
    echo "🚀 Your AI development stack is now complete!"
    echo ""
    echo "Next steps:"
    echo "1. Test the integration: python ~/.aios/templates/aios_crew_workflow.py"
    echo "2. Start building with your complete AI stack!"
    echo "3. Use CrewAI for multi-agent orchestration"
    echo "4. Build visual workflows with Langflow/Flowise"
else
    echo ""
    echo "💥 AI Crew Installer encountered issues."
    echo "Check the logs above for details."
fi

# Deactivate environment
deactivate

echo ""
echo "🎯 AI Crew Installation Complete!"
echo "Your AI development environment is now enterprise-grade!"
