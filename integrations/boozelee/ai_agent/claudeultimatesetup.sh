#!/bin/bash
set -e

echo "🚀 CLAUDE ULTIMATE SETUP (Feb 9, 2026) - ZSH + COMMITS + WORKFLOWS"

# FULL PREREQS (auto)
sudo apt update && sudo apt install -y gh ripgrep
pipx install superclaude && superclaude install && superclaude mcp

# Claude Code
curl -fsSL https://claude.ai/install.sh | bash

# PRO Configs
git clone https://github.com/ChrisWiles/claude-code-showcase /tmp/showcase
cp -rf /tmp/showcase/.claude/* ~/.claude/ && rm -rf /tmp/showcase

# INTERACTIVE: Your repo
read -r REPO
REPO_DIR=$(mktemp -d); cd "$REPO_DIR"
git clone "https://github.com/$REPO.git" . || git init

# GitHub App (auto browser)
claude /install-github-app

# 🔥 ULTIMATE CLAUDE.md with Commit Standards
cat > CLAUDE.md << 'EOF'
# ULTIMATE LangChain Standards (Feb 9, 2026)

## COMMIT CONVENTIONS (MANDATORY)
