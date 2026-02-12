# 🐝 BeeAI Hive 999 — Unified Multi-Agent AI Ecosystem

> A sovereign, self-funding AI development environment combining 28+ agents, blockchain intelligence, Solana integration, and a detective-themed investigation layer.

```
╔═══════════════════════════════════════════════════════════════════════╗
║  🐝 BEEAI HIVE 999 ⟡ 9×9×9 MATRIX ⟡ OFFLINE CODING ⟡ DR9       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 📋 Overview

This monorepo unifies multiple AI and blockchain projects into a single, cohesive ecosystem:

| Project | Description |
|---------|-------------|
| **Hive 999 Core** | Multi-agent blockchain intelligence — Queen Bee orchestrator, 9 Worker Bees, 9 Drones, 9 Foragers, Mantis Mail |
| **Terminal 221b** | Sherlock Holmes-inspired Solana detective investigation agents |
| **HIVE3-729 Detective Agency** | Extended detective layer with supervisor agent system, Radicle integration, HuggingFace connectors |
| **beeAI** | Unified deployment layer — cloud configs, Render/Docker/K8s manifests |
| **Bounty Hunter** | Bug bounty automation — chat TUI, todo tracker, OpenClaw integration |
| **Alien Command Center** | Rust-based experimental brain execution engine with Lua scripting |
| **Nebula Hunter** | Trend research and cosmic data hunter (scaffold) |
| **Solana Release** | Solana CLI tools, SDK, and validator toolchain |

---

## 🏗️ Architecture

```
beeai-hive-999/
├── agents/                  # Core agent definitions (Queen, Workers, Drones, Foragers)
├── art/                     # ANSI art assets
├── backend/                 # Backend API layer
├── beeAI/                   # Unified deployment & cloud configs
├── bounty_hunter/           # Bug bounty automation system
├── alien_command_center/    # Rust brain execution engine
├── config/                  # Configuration files
├── data/                    # Data stores
├── database/                # Database layer
├── docs/                    # Documentation
├── HIVE3-729-Detective-Agency/  # Extended detective layer
├── hive_core/               # Core hive logic
├── integrations/            # Third-party integrations
├── knowledge/               # Knowledge base / RAG
├── landing-page/            # Web landing page
├── models/                  # Model configurations
├── nebula_hunter/           # Trend research agent (scaffold)
├── reports/                 # Generated reports
├── scripts/                 # Utility scripts
├── solana_release/          # Solana SDK & tools
├── supabase/                # Supabase integration
├── terminal_221b/           # Terminal 221b detective system (integrated)
├── terminal221b_standalone/ # Terminal 221b standalone (monetization, email, engines)
├── tools/                   # Shared tool definitions
├── workflows/               # Workflow definitions
├── main.py                  # Main entry point
├── run.sh                   # Launch script
├── beehave.py               # Agent behavior engine
├── hive_tui_enhanced.py     # Enhanced Terminal UI
└── tui.py                   # Base Terminal UI
```

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/BoozeLee/beeai-hive-999.git
cd beeai-hive-999

# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Launch TUI
./run.sh

# Run system checks
./run.sh check

# Run tests
pytest
```

---

## 🐝 Agent System (28+)

| Type | Count | Role |
|------|-------|------|
| 👑 Queen Bee | 1 | Orchestrator — routes tasks to specialists |
| 🐝 Worker Bees | 9 | Blockchain specialists (BTC, ETH, SOL, DOT, etc.) |
| 🛸 Drone Agents | 9 | Stakeholder analysts |
| 🌸 Forager Agents | 9 | Trend researchers |
| 📬 Mantis Mail | 1 | Communication agent |
| 🕵️ Detective 221b | 1+ | Solana investigation agents |

---

## 🔗 Blockchain & Solana

- Solana Agent Kit integration
- On-chain transaction investigation (Terminal 221b)
- DeFi monetization agents (staking, arbitrage, lending, airdrops)
- Bounty hunter automation (HackerOne, Bugcrowd, OpenClaw)

---

## 🛡️ Security

- Supabase Vault for secrets management
- No API keys in code — all secrets via environment variables
- Security audit checklist in `beeAI/security/`

---

## 📄 Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — System architecture
- [COMMUNICATION_ARCHITECTURE.md](COMMUNICATION_ARCHITECTURE.md) — Agent communication protocols
- [SECURITY_IMPLEMENTATION.md](SECURITY_IMPLEMENTATION.md) — Security details
- [TERMINAL_221B_SUMMARY.md](TERMINAL_221B_SUMMARY.md) — Detective system overview
- [SETUP.md](SETUP.md) — Detailed setup instructions
- [HIVE3-729-Detective-Agency/DEPLOYMENT_GUIDE.md](HIVE3-729-Detective-Agency/DEPLOYMENT_GUIDE.md) — Deployment guide

---

## 🧪 Testing

```bash
pytest                          # All tests
pytest tests/ -v                # Verbose
pytest --cov=. tests/           # With coverage
ruff check .                    # Lint
black .                         # Format
```

---

## 📜 License

See [HIVE3-729-Detective-Agency/LICENSE.md](HIVE3-729-Detective-Agency/LICENSE.md)

---

*Built with 🐝 by the BeeAI Hive — where agents never sleep.*
