#!/bin/bash
# BeeAI Hive 999 - TUI Launcher Script
# Run THIS SCRIPT in a separate terminal to start the TUI

cd /home/boozelee/beeai-hive-999

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Check for required dependencies
python3 -c "import prompt_toolkit" 2>/dev/null || {
    echo "Installing prompt_toolkit..."
    pip install prompt-toolkit -q
}

python3 -c "import beeai_framework" 2>/dev/null || {
    echo "BeeAI Framework not found. The TUI requires it."
    echo "Install with: pip install beeai-framework"
    exit 1
}

echo "Starting BeeAI Hive 999 Enhanced TUI..."
echo "========================================"
echo ""

# Launch the enhanced TUI
python3 hive_tui_enhanced.py
