# 🤖 AI Agent Automation System

**LangChain RAG + GitHub Bounty Hunter + Social Automation**

*Optimized for Termux Ubuntu Proot on Android*

## 🚀 Quick Start

```bash
# Activate Python environment
source bin/activate

# Install dependencies (if needed)
pip install -r requirements.txt

# Scan for bounties
./scripts/scan_bounties.sh

# Update RAG knowledge base
./scripts/update_rag.sh

# Community engagement
./scripts/engage_community.sh
```

## 📦 Features

### 1. 🎯 Bounty Hunter
- **Auto-scan** repositories for bounty issues
- **AI analysis** of complexity and requirements
- **Smart proposals** using Claude 4.5 Sonnet
- **Auto-commenting** on bounty issues
- **Earnings tracking**

### 2. 💬 Social Automation
- **Smart replies** to mentions and questions
- **Daily engagement** with community
- **Weekly summaries** of activity
- **Sentiment analysis** of interactions
- **Auto-reviews** of pull requests

### 3. 🧠 LangChain RAG
- **FAISS vector store** for fast retrieval
- **Sentence transformers** embeddings
- **Claude-powered** Q&A
- **Persistent indexes**
- **Document ingestion** from markdown files

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- GitHub CLI (`gh`)
- Git

### Setup
```bash
# Install system dependencies (Ubuntu Proot)
apt update && apt install -y python3-pip git gh curl

# Install Python packages
pip install langchain langchain-community langchain-core
pip install faiss-cpu sentence-transformers torch
pip install anthropic openai pydantic

# Configure GitHub CLI
gh auth login --web
```

### Environment Variables
Create a `.env` file:
```bash
ANTHROPIC_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # Optional
GITHUB_TOKEN=${{ secrets.GITHUB_TOKEN }}  # In Actions
```

## 📋 Usage

### Bounty Hunter
```bash
# Scan repositories
python bounty_hunter.py --mode scan --repos owner/repo

# Analyze specific issue
python bounty_hunter.py --mode analyze --repo owner/repo --issue 123

# Generate solution proposal
python bounty_hunter.py --mode propose --repo owner/repo --issue 123 --auto-comment
```

### Social Automation
```bash
# Daily engagement
python social_automator.py --mode engage --daily

# Reply to mention
python social_automator.py --mode reply --issue-number 456

# Weekly summary
python social_automator.py --mode summary
```

### LangChain RAG
```bash
# Ingest documents
python langchain_rag.py --mode ingest --docs-dir docs

# Query knowledge base
python langchain_rag.py --mode query --question "How do I use FAISS?"

# Update index
python langchain_rag.py --mode update-index
```

## 🤖 GitHub Actions

All workflows are in `.github/workflows/`:

- **bounty-hunter.yml** - Runs every 3 hours, scans for bounties
- **social-automation.yml** - Daily engagement at 8 AM & 4 PM
- **langchain-rag.yml** - Updates RAG index on docs changes
- **code-review.yml** - Auto-reviews PRs with Claude

### Required Secrets
Configure in GitHub Settings > Secrets and variables > Actions:
- `ANTHROPIC_API_KEY` - Your Claude API key
- `OPENAI_API_KEY` - (Optional) OpenAI API key
- `GITHUB_TOKEN` - Auto-provided

## 📂 Project Structure

```
/root/ai_agent/
├── bounty_hunter.py          # Bounty scanning & analysis
├── social_automator.py       # Social engagement bot
├── langchain_rag.py          # RAG pipeline
├── CLAUDE.md                 # Claude Code instructions
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .github/workflows/        # GitHub Actions
│   ├── bounty-hunter.yml
│   ├── social-automation.yml
│   ├── langchain-rag.yml
│   └── code-review.yml
├── scripts/                  # Helper scripts
│   ├── scan_bounties.sh
│   ├── smart_reply.sh
│   ├── update_rag.sh
│   └── engage_community.sh
├── configs/                  # Configuration files
│   ├── langchain.yaml
│   ├── bounty_rules.yaml
│   └── social_rules.yaml
└── data/                    # Data & indexes
    ├── faiss_index/
    ├── embeddings/
    └── cache/
```

## 🎮 Example Workflows

### 1. Hunt for Bounties
```bash
# Scan multiple repos
./scripts/scan_bounties.sh anthropics/anthropic-sdk-python langchain-ai/langchain

# Analyze a specific issue
python bounty_hunter.py --mode analyze --repo anthropics/anthropic-sdk-python --issue 42
```

### 2. Build Knowledge Base
```bash
# Add documents to docs/
mkdir -p docs
echo "# LangChain Guide" > docs/langchain.md

# Ingest and index
./scripts/update_rag.sh

# Query it
python langchain_rag.py --mode query --question "What is LangChain?"
```

### 3. Automate Social Engagement
```bash
# Daily engagement
./scripts/engage_community.sh

# Reply to specific issue
./scripts/smart_reply.sh 123
```

## 🔧 Configuration

Edit `configs/*.yaml` files to customize:
- **bounty_rules.yaml** - Bounty detection and analysis
- **social_rules.yaml** - Social engagement behavior
- **langchain.yaml** - RAG pipeline settings

## 📊 Monitoring

Check GitHub Actions tab for:
- Workflow runs
- Automated comments
- Error logs
- Performance metrics

## 🎯 Roadmap

- [ ] Multi-repo scanning dashboard
- [ ] Earnings tracker with analytics
- [ ] Custom LLM fine-tuning for bounties
- [ ] Slack/Discord integration
- [ ] Mobile notifications
- [ ] PR auto-generation for bounties

## 🤝 Contributing

Contributions welcome! This project uses:
- **Conventional Commits** (`feat:`, `fix:`, `perf:`, etc.)
- **GitHub Actions** for CI/CD
- **Claude Code** for development

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

Built with:
- [Anthropic Claude](https://anthropic.com/) - AI reasoning
- [LangChain](https://langchain.com/) - RAG framework
- [FAISS](https://github.com/facebookresearch/faiss) - Vector search
- [GitHub CLI](https://cli.github.com/) - GitHub automation

---

*Made with ❤️ using Claude Code in Termux Ubuntu Proot*
