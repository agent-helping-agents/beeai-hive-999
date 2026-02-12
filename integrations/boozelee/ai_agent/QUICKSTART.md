# 🚀 Quick Start Guide

**AI Agent Automation System - Ready to Use!**

## ✅ What's Installed

1. **LangChain RAG Pipeline** - FAISS vector store with Claude integration
2. **Bounty Hunter Bot** - Scans GitHub for bounties and generates solutions
3. **Social Automation** - Smart replies and community engagement
4. **GitHub Actions** - 4 automated workflows ready to deploy

## 🎯 Quick Actions

### 1. Find Bounties (Right Now!)

```bash
# Scan for active bounties
python3 scripts/bounty_finder.py

# Analyze a specific issue
python bounty_hunter.py --mode analyze --repo owner/repo --issue 123

# Generate solution proposal
python bounty_hunter.py --mode propose --repo owner/repo --issue 123
```

### 2. Build Knowledge Base

```bash
# Add documents to docs/
echo "# LangChain Guide" > docs/langchain.md
echo "Use LangChain for RAG pipelines..." >> docs/langchain.md

# Update index
./scripts/update_rag.sh

# Query it
python langchain_rag.py --mode query --question "What is LangChain?"
```

### 3. Social Automation

```bash
# Daily community engagement
./scripts/engage_community.sh

# Reply to specific issue
python social_automator.py --mode reply --issue-number 123
```

## 🔑 Setup API Keys

```bash
# Add to your ~/.bashrc or ~/.zshrc
export ANTHROPIC_API_KEY="your_key_here"
export OPENAI_API_KEY="your_key_here"  # Optional
```

## 📊 Deploy to GitHub

```bash
# Set repository secrets (replace YOUR_REPO)
gh secret set ANTHROPIC_API_KEY -b "your_key" --repo YOUR_REPO
gh secret set OPENAI_API_KEY -b "your_key" --repo YOUR_REPO  # Optional

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin master
```

## 🤖 GitHub Actions Will Auto-Run:

- **Bounty Hunter** - Every 3 hours
- **Social Automation** - Daily at 8 AM & 4 PM UTC
- **RAG Updates** - When docs/ changes
- **Code Reviews** - On every PR

## 📋 Today's Bounty Checklist

Since no active bounties were found, here's how to create your own:

### Create Bounty Issues in Your Repos

```bash
# Enable issues on your repos
gh repo edit BoozeLee/ai-comic-studio --enable-issues
gh repo edit BoozeLee/batman-comic-studio --enable-issues

# Create a bounty issue
gh issue create --repo BoozeLee/ai-comic-studio \
  --title "Add AI character generation feature" \
  --label "bounty,enhancement,help-wanted" \
  --body "## Bounty: \$100

Build an AI character generator using Anthropic's Claude.

**Requirements:**
- Generate comic characters with descriptions
- Use Claude API for creative text
- Support multiple art styles

**Deliverables:**
- Working Python script
- Unit tests
- Documentation"
```

### Monitor Your Codespaces

You have 2 shutdown codespaces:
- `glorious-enigma-wqr9p5jr4pwf5jq4` (rp2040-zero)
- `legendary-tribble-p5jg4wqjvv52g66` (coolify)

```bash
# List all codespaces
gh codespace list

# Start a codespace
gh codespace create --repo BoozeLee/ai-comic-studio

# Or resume existing one
gh codespace code --codespace NAME
```

## 🎮 Interactive Commands

```bash
# Scan your repos
for repo in ai-comic-studio batman-comic-studio; do
  echo "=== BoozeLee/$repo ==="
  gh repo view BoozeLee/$repo --json name,description,updatedAt
done

# Find good first issues in popular repos
gh search issues "is:open label:good-first-issue language:python" --limit 10

# Track your PRs
gh pr list --author @me --state all

# Check notifications
gh api notifications | jq '.[].repository.full_name' | sort | uniq -c
```

## 💡 Pro Tips

1. **Start Small**: Focus on "good first issue" labels before tackling bounties
2. **Build Your RAG**: Add project docs to `docs/` for AI-assisted development
3. **Automate Everything**: GitHub Actions workflows are ready - just push!
4. **Track Progress**: Use issue templates and project boards

## 🔥 Next Steps

1. **Set API Keys** (required for Claude)
2. **Push to GitHub** (activates workflows)
3. **Create bounty issues** (on your repos)
4. **Build RAG knowledge base** (add docs)
5. **Engage with community** (auto-replies)

## 📞 Need Help?

```bash
# Test your setup
python3 -c "import anthropic; print('✅ Anthropic installed')"
python3 -c "import langchain; print('✅ LangChain installed')"

# Check gh CLI
gh --version
gh auth status

# Verify git
git status
git log --oneline -5
```

---

**🎉 You're all set! Start hunting bounties and building AI agents!**
