#!/bin/bash
set -euo pipefail

clear
echo "🚀 SUPERCLAUDE + CLAUDE CODE FULL AUTOMATION (Feb 9, 2026)"
echo "==========================================================="

# 1. System prerequisites
echo "📦 Installing system dependencies..."
sudo apt update && sudo apt install -y gh python3-pipx curl ripgrep

# GitHub CLI auth (interactive browser)
echo "🔐 Authenticating GitHub CLI..."
gh auth login --web --scopes=workflow

# 2. pipx setup
pipx ensurepath

# 3. SUPERCLAUDE FRAMEWORK (30+ commands from GitHub)
echo "⚡ Installing SuperClaude Framework..."
pipx install superclaude
superclaude install --yes
superclaude mcp --yes  # Tavily, Context7, Playwright servers

# 4. Claude Code (official)
if ! command -v claude &> /dev/null; then
    echo "🔧 Installing Claude Code..."
    curl -fsSL https://claude.ai/install.sh | bash
fi

# 5. ULTIMATE ZSH COMPLETIONS
echo "🐚 Installing permanent zsh completions..."
mkdir -p ~/.zsh/completions
curl -sL https://raw.githubusercontent.com/wbingli/zsh-claudecode-completion/main/_claude -o ~/.zsh/completions/_claude

cat >> ~/.zshrc << 'EOF'

# 🔥 SUPERCLAUDE + CLAUDE CODE ZSH (Feb 2026)
export PATH="$HOME/.local/bin:$PATH"
[[ ! -d ~/.zsh/completions ]] && mkdir -p ~/.zsh/completions
fpath=(~/.zsh/completions $fpath)
autoload -Uz compinit && compinit

# SuperClaude shortcuts
alias sc='superclaude'
alias claude-commit='claude commit --conventional --amend'
alias claude-pr='claude pr create --title "$(git diff --stat HEAD~1 | head -1)"'
EOF

# 6. Interactive repo setup
echo "📂 Enter target repo (user/repo):"
read -r REPO
REPO_DIR=$(mktemp -d)
cd "$REPO_DIR"
git clone "https://github.com/$REPO.git" . || git init "langchain-superclaude" && cd langchain-superclaude

# 7. GitHub App (auto browser popup)
echo "🔗 Auto-installing Claude GitHub App..."
claude /install-github-app

# 8. SUPERCLAUDE CLAUDE.md (LangChain/GTX 1080 optimized)
cat > CLAUDE.md << 'EOF'
# 🚀 SUPERCLAUDE + LANGCHAIN STANDARDS (Feb 9, 2026)

## SUPERCLAUDE COMMANDS (30+ Available)
