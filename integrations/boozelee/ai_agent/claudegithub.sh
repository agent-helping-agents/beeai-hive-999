#!/bin/bash
set -e

clear
echo "🔧 Claude Code + GitHub Full Setup (Feb 9, 2026)"
echo "=============================================="

# 1. Update & GitHub CLI
echo "📦 Installing GitHub CLI..."
sudo apt update && sudo apt install -y gh

# Interactive GitHub auth (opens browser)
echo "🔐 Authenticate GitHub CLI..."
gh auth login --web --scopes=workflow

# 2. Install Claude Code (official)
if ! command -v claude &> /dev/null; then
    echo "⚙️ Installing Claude Code..."
    curl -fsSL https://claude.ai/install.sh | bash
fi

# 3. Zsh completions setup
echo "🐚 Setting up zsh completions..."
mkdir -p ~/.zsh/completions
curl -sL https://raw.githubusercontent.com/wbingli/zsh-claudecode-completion/main/_claude -o ~/.zsh/completions/_claude
echo '# Claude Code zsh completions' >> ~/.zshrc
echo 'fpath=(~/.zsh/completions $fpath)' >> ~/.zshrc
echo 'autoload -Uz compinit && compinit' >> ~/.zshrc
echo 'alias claude="claude --continue"' >> ~/.zshrc

# 4. Interactive repo setup
echo "📂 Enter target repo (user/repo):"
read -r REPO
REPO_DIR=$(mktemp -d)
cd "$REPO_DIR"
git clone "https://github.com/$REPO.git" . || git init "claude-langchain-demo" && cd claude-langchain-demo

# 5. GitHub App install (opens browser automatically)
echo "🔗 Installing Claude GitHub App..."
claude /install-github-app

# 6. LangChain-optimized CLAUDE.md
cat > CLAUDE.md << 'EOF'
# LangChain + Claude Code Standards (Feb 2026)

## Core Patterns
```python
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS

llm = LlamaCpp(model_path="tinyllama.gguf", n_gpu_layers=35, n_ctx=4096)
