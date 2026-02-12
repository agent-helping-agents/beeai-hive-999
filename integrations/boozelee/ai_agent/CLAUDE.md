# AI AGENT AUTOMATION SYSTEM
**LangChain + GitHub Bounty Hunter + Social Automation**
*Termux Ubuntu Proot - Feb 9, 2026*

## 🚀 QUICK START COMMANDS

```bash
# Activate environment
source /root/ai_agent/bin/activate

# Run bounty hunter
python bounty_hunter.py

# Social automation
python social_automator.py

# LangChain RAG pipeline
python langchain_rag.py
```

## 🤖 LANGCHAIN FEATURES

### Available Models
- **LlamaCpp**: Local GGUF models (TinyLlama, Mistral, etc.)
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude 4.6 Opus, Claude 4.5 Sonnet/Haiku
- **Embeddings**: sentence-transformers, OpenAI embeddings

### Vector Stores
- **FAISS**: Fast similarity search
- **Chroma**: Persistent embeddings
- **In-Memory**: Quick prototyping

### Chains & Tools
- RAG (Retrieval-Augmented Generation)
- Conversational chains with memory
- Tool-calling agents
- Multi-agent systems with LangGraph

## 📋 AUTOMATION WORKFLOWS

### GitHub Bounty Hunter
- Auto-scans issues with bounty labels
- Analyzes complexity and stack requirements
- Generates implementation plans with Claude
- Auto-comments on issues with proposals
- Tracks bounty status and payments

### Social Automation
- Auto-replies to GitHub issues/PRs
- Smart commenting with context awareness
- Scheduled daily summaries
- Mentions tracking and responses
- Community engagement automation

## 🔧 GITHUB ACTIONS

All workflows are in `.github/workflows/`:
- `bounty-hunter.yml` - Hourly bounty scanning
- `social-automation.yml` - Daily social tasks
- `langchain-rag.yml` - RAG pipeline updates
- `code-review.yml` - Auto PR reviews with Claude
- `issue-triage.yml` - Auto-label and prioritize issues

## 🎯 CONVENTIONAL COMMITS

Use these prefixes:
- `feat:` - New features
- `fix:` - Bug fixes
- `perf:` - Performance improvements
- `docs:` - Documentation
- `refactor:` - Code restructuring
- `test:` - Testing
- `chore:` - Maintenance

## 🔑 REQUIRED SECRETS

Configure in GitHub Settings > Secrets:
- `ANTHROPIC_API_KEY` - Claude API access
- `OPENAI_API_KEY` - OpenAI models (optional)
- `GITHUB_TOKEN` - Auto-provided by Actions
- `GH_PAT` - Personal access token for advanced features

## 📦 INSTALLED PACKAGES

```
langchain>=1.2.9
langchain-community>=0.4.1
langchain-core>=1.2.9
faiss-cpu>=1.13.0
sentence-transformers>=5.2.0
torch>=2.10.0
anthropic>=0.79.0
openai>=2.17.0
pydantic>=2.12.0
```

## 🎮 CUSTOM COMMANDS

```bash
# Bounty hunting
./scripts/scan_bounties.sh       # Scan for new bounties
./scripts/submit_solution.sh     # Submit bounty solution
./scripts/track_earnings.sh      # Track bounty earnings

# Social automation
./scripts/engage_community.sh    # Daily community engagement
./scripts/smart_reply.sh         # Smart reply to mentions
./scripts/pr_review.sh          # Automated PR reviews

# LangChain operations
./scripts/update_rag.sh         # Update RAG knowledge base
./scripts/train_embeddings.sh   # Train custom embeddings
./scripts/agent_chat.sh         # Interactive agent chat
```

## 📊 PROJECT STRUCTURE

```
/root/ai_agent/
├── bounty_hunter.py           # Main bounty automation
├── social_automator.py        # Social engagement
├── langchain_rag.py          # RAG pipeline
├── scripts/                  # Automation scripts
│   ├── scan_bounties.sh
│   ├── smart_reply.sh
│   └── update_rag.sh
├── .github/workflows/        # GitHub Actions
│   ├── bounty-hunter.yml
│   ├── social-automation.yml
│   └── langchain-rag.yml
├── configs/                  # Configuration files
│   ├── langchain.yaml
│   ├── bounty_rules.yaml
│   └── social_rules.yaml
└── data/                    # Vector stores & cache
    ├── faiss_index/
    ├── embeddings/
    └── cache/
```

## 🌟 USAGE EXAMPLES

### LangChain RAG
```python
from langchain_rag import RAGPipeline

rag = RAGPipeline()
rag.ingest_docs("./docs/")
response = rag.query("How do I implement OAuth2?")
```

### Bounty Hunter
```python
from bounty_hunter import BountyHunter

hunter = BountyHunter()
bounties = hunter.scan_repos(["repo/name"])
hunter.auto_apply(bounties[0])
```

### Social Automation
```python
from social_automator import SocialBot

bot = SocialBot()
bot.engage_daily()
bot.smart_reply_to_mentions()
```

## 🚦 STATUS

- ✅ LangChain installed with FAISS
- ✅ Git repository initialized
- ✅ GitHub CLI configured
- ⏳ Workflows pending creation
- ⏳ Automation scripts pending creation
