#!/bin/bash
set -e

clear
echo "🔥 CLAUDE CODE FULL GITHUB + ZSH + TEAM + LANGCHAIN (Feb 9, 2026)"
echo "================================================================="

# [Previous steps 1-4 unchanged: GitHub CLI, Claude Code, SuperClaude, ChrisWiles]

# 5. INTERACTIVE: Team repo setup
echo "👥 Enter TEAM repo for workflows (user/repo):"
read -r TEAM_REPO
echo "🤖 Enter your Anthropic API key for GitHub Actions:"
read -rs ANTHROPIC_KEY

# 6. Clone team repo + LangChain template
REPO_DIR=$(mktemp -d)
cd "$REPO_DIR"
git clone "https://github.com/$TEAM_REPO.git" . || git init

# 7. LangChain → Claude Code Bridge (CLAUDE.md)
cat > CLAUDE.md << 'EOF'
# TEAM LangChain → Claude Code Standards (Feb 9, 2026)

## WORKFLOWS (Daily Use)
