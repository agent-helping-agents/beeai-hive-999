#!/bin/bash
# Scan multiple repositories for bounty opportunities

set -e

echo "🎯 BOUNTY SCANNER"
echo "================="

# Default repos to scan
REPOS=(
    "anthropics/anthropic-sdk-python"
    "langchain-ai/langchain"
    "openai/openai-python"
    "huggingface/transformers"
)

# Add custom repos from arguments
if [ $# -gt 0 ]; then
    REPOS=("$@")
fi

echo "Scanning ${#REPOS[@]} repositories..."

for repo in "${REPOS[@]}"; do
    echo ""
    echo "📂 $repo"
    python3 bounty_hunter.py --mode scan --repos "$repo"
done

echo ""
echo "✅ Scan complete!"
