#!/bin/bash
set -e

cd ~/codex-superlab

echo "=== Setting up Complete Codex Framework ==="

# Ensure all scripts are executable
chmod +x *.sh *.py

# Install dependencies
pip3 install --user numpy sympy requests

echo "✓ Framework ready!"
echo ""
echo "To integrate into a project:"
echo "  ./integrate_codex.sh /path/to/project"
echo ""
echo "To generate research report:"
echo "  ./generate_research_report.sh"
