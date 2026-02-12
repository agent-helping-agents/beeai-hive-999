#!/bin/bash

# AIOS Builder Agent Launcher
# Launches the AIOS Builder Agent to build the complete AIOS system

echo "🧠 AIOS Builder Agent Launcher"
echo "================================"

# Check if we're in the right directory
if [ ! -f "aios_builder_agent.py" ]; then
    echo "❌ AIOS Builder Agent not found in current directory"
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

# Run the AIOS Builder Agent
echo "🚀 Launching AIOS Builder Agent..."
echo "This will build the complete AIOS system using our AI stack."
echo ""

python aios_builder_agent.py

# Check result
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 AIOS Builder Agent completed successfully!"
    echo "🚀 Your AIOS system is now ready for production use!"
    echo ""
    echo "Next steps:"
    echo "1. Test the system: python ~/.aios/templates/aios_productivity_workflow.py"
    echo "2. Use the desktop launcher"
    echo "3. Start building your own AI agents!"
else
    echo ""
    echo "💥 AIOS Builder Agent encountered issues."
    echo "Check the logs above for details."
fi

# Deactivate environment
deactivate
