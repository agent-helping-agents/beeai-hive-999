#!/bin/bash
# =============================================================================
# Automated Hive 999 Setup Runner
# Runs the unified secrets manager
# =============================================================================

cd /home/boozelee/beeai-hive-999

# Check if running in interactive mode
if [ -t 0 ]; then
    # Interactive - run Python script
    python3 scripts/setup_all_secrets.py
else
    # Non-interactive - show help
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║     🐝 HIVE 999 - Setup Wizard                                  ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Usage:"
    echo "  ./scripts/auto_setup.sh              # Interactive setup"
    echo "  ./scripts/ngrok_zoho_verify.sh       # Zoho verification only"
    echo "  python3 scripts/setup_all_secrets.py # Python setup wizard"
    echo ""
    echo "Quick commands:"
    echo "  ./run.sh                             # Launch Hive TUI"
    echo "  ./run.sh check                       # Check system status"
    echo ""
fi
