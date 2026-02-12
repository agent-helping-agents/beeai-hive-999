# 🐝 BeeAI Hive 999 - Enhanced Terminal UI

A production-ready, full-screen terminal UI for a hybrid multi-agent system with **100% offline coding capabilities**.

```
╔═══════════════════════════════════════════════════════════════════╗
║  🐝 BEEAI HIVE 999 ⟡ 9×9×9 MATRIX ⟡ OFFLINE CODING ⟡ DR9 ║
╚═══════════════════════════════════════════════════════════════════╝
```

## ✨ What's New (Enhanced Version)

### Core TUI Features
- ✅ **Scrollable Chat** - Navigate through message history with arrow keys
- ✅ **Visual Scrollbar** - See your position in chat history (█ thumb, │ track)
- ✅ **Message Bubbles** - Color-coded by agent type (Queen=Gold, Workers=Cyan, Drones=Green, etc.)
- ✅ **Typing Indicators** - Animated feedback when agents are "thinking"
- ✅ **Syntax Highlighting** - Code blocks detected and formatted
- ✅ **Notification System** - Success, warning, error notifications
- ✅ **Settings UI** - Configure backend, models, themes within TUI

### 100% Offline Coding
```
Recommended Models:
├── qwen2.5-coder:32b    ← Primary coding model (GPT-4o level)
├── deepseek-coder-v2:16b ← Complex algorithms & reasoning  
├── codellama:34b         ← Code generation backup
└── deepseek-coder:33b   ← Alternative
```

## 🚀 Quick Start

```bash
# Run enhanced TUI
./run.sh tui

# Setup coding models (100% offline)
./run.sh setup

# Consult the Queen Bee
./run.sh queen

# Run tests
./run.sh test
```

## 🎯 Key Features

### 28+ Agents
| Type | Count | Role |
|------|-------|------|
| Queen Bee | 1 | Central orchestrator |
| Worker Bees | 9 | Blockchain specialists |
| Drone Agents | 9 | Stakeholder analysts |
| Forager Agents | 9 | Trend researchers |
| Mantis Mail | 1 | Email communication |
| Terminal 221b | 4 | Detective specialists |

### 9×9×9 Matrix
- **9 Blockchains**: Bitcoin, Ethereum, Solana, TRON, Stellar, Avalanche, Arbitrum, Polygon, Optimism
- **9 Stakeholders**: Customers, Employees, Investors, Owners, Suppliers, Communities, Unions, Government, Media
- **9 Trends**: Tokenization, DeFi, Supply Chain, Identity, CBDC, AI, Sustainability, RegTech, Interoperability
- **Total**: 729 nodes | Digital Root: 9

### Hybrid Backend
| Backend | Models | Best For |
|---------|--------|----------|
| **Local (Ollama)** | granite3.3, qwen2.5-coder, deepseek | Privacy, offline, no API costs |
| **Cloud (LangChain)** | GPT-4, Claude-3, GPT-3.5 | Speed, scale, monitoring |

## 💻 Enhanced TUI Commands

### Navigation
| Key | Action |
|-----|--------|
| `↑/↓` | Scroll chat |
| `PgUp/PgDn` | Page scroll |
| `Home/End` | Jump to top/bottom |
| `Tab` | Toggle sidebar |

### Agent Switching
| Key | Action |
|-----|--------|
| `Alt+Q` | Queen Bee |
| `Alt+1-9` | Workers (blockchains) |
| `Alt+G` | Government Drone |
| `Alt+X` | Mantis Mail |
| `Alt+N` | Detective 221b |

### Commands
| Command | Description |
|---------|-------------|
| `:help` | Show commands |
| `:art <topic>` | Show ANSI art |
| `:settings` | Open settings |
| `:backend local` | Switch to Ollama |
| `:backend cloud` | Switch to LangChain |
| `:model <name>` | Change model |
| `:clear` | Clear chat |
| `:quit` | Exit TUI |

## 🔧 Configuration

### Environment Variables
```bash
export HIVE_BACKEND=local          # local|cloud
export HIVE_THEME=honey            # honey|dark|light|matrix
export OLLAMA_HOST=http://localhost:11434
export OPENAI_API_KEY=sk-...       # For cloud backend
export LANGSMITH_API_KEY=ls-...    # For tracing
```

### Ollama Coding Setup
```bash
# 100% offline coding - pull models
./run.sh setup

# Or manually
ollama pull qwen2.5-coder:32b      # Primary (GPT-4o level)
ollama pull deepseek-coder-v2:16b  # Reasoning
ollama pull codellama:34b          # Backup
```

## 📁 Project Structure

```
beeai-hive-999/
├── hive_tui_enhanced.py      # Enhanced TUI (scrollable, bubbles, etc)
├── tui.py                    # Original TUI
├── backend/
│   ├── llm_router.py         # Model routing (local/cloud)
│   ├── config_manager.py     # Backend config
│   ├── ollama_coder.py       # Offline coding assistant ⭐ NEW
│   └── hive_config.py        # Comprehensive config system ⭐ NEW
├── agents/
│   ├── queen_bee/
│   │   ├── orchestrator.py
│   │   └── consultation.py   # Queen Bee wisdom ⭐ NEW
│   ├── worker_bees/
│   ├── drone_agents/
│   ├── forager_agents/
│   └── mantis_mail/
├── tools/
│   ├── blockchain/matrix_search.py
│   ├── regtech/compliance_checker.py
│   ├── ibc/federation_router.py
│   └── art/caterpillar_artist.py
├── tests/
│   ├── test_hive_core.py     # Unit tests ⭐ NEW
│   └── test_integration.py   # Integration tests ⭐ NEW
├── docs/
│   ├── conf.py               # Sphinx config ⭐ NEW
│   └── index.rst            # Documentation index ⭐ NEW
├── .github/workflows/
│   └── ci.yml               # CI/CD pipeline ⭐ NEW
└── config/
    └── hive_config.py       # Comprehensive config
```

## 🧪 Testing

```bash
# Run all tests
./run.sh test

# Run linters (ruff, black, mypy)
./run.sh lint

# System checks
./run.sh check
```

## 📚 Documentation

```bash
# Generate Sphinx docs
cd docs
make html

# Consult the Queen Bee
./run.sh queen
```

### Queen Bee Consultation
```python
from agents.queen_bee.consultation import consult_queen

# Ask architecture questions
wisdom = consult_queen("How should agents be designed?")
print(wisdom.answer)

# Or use the consultant directly
from agents.queen_bee.consultation import QueenBeeConsultant
consultant = QueenBeeConsultant()
wisdom = consultant.consult("Performance optimization", domain="performance")
```

## 🎨 Color Scheme (Digital Root 9)

| Agent | Color | Hex |
|-------|-------|-----|
| Queen | Honey/Amber | `#FFAC33` |
| Workers | Cyan | `#00FFFF` |
| Drones | Green | `#32CD32` |
| Foragers | Magenta | `#FF00FF` |
| Detectives | Red | `#CD5C5C` |
| Mantis | Lime | `#32CD32` |

## 🤖 Offline Coding with OllamaCoder

```python
from backend.ollama_coder import OllamaCoder, CodingModel

coder = OllamaCoder(CodingModel.QWEN_CODER_32B)

# Code completion
suggestion = await coder.complete_code("def fibonacci(n):")

# Code explanation
explanation = await coder.explain_code(code, language="python")

# Fix code issues
fixes = await coder.fix_code(code, error="SyntaxError")

# Generate tests
tests = await coder.generate_tests(code, framework="pytest")

# Refactor code
refactored = await coder.refactor_code(code, goal="readability")
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    HiveEnhancedTUI                        │
├────────┬─────────┬──────────┬──────────┬───────────────┤
│ Agents │  Chat   │ Context  │ Scroll   │ Notifications │
│ Sidebar│ Bubbles │ Panel    │ Bar      │              │
│        │ +Scroll │          │          │              │
├────────┴─────────┴──────────┴──────────┴───────────────┤
│  [Input]                                               │
├─────────────────────────────────────────────────────────┤
│  Status: [queen] 🏠 granite3.3:8b | Ready | DR9       │
└─────────────────────────────────────────────────────────┘
```

## 📦 Installation

```bash
# Clone
git clone https://github.com/beeai-org/beeai-hive-999.git
cd beeai-hive-999

# Make executable
chmod +x run.sh

# Run with all checks
./run.sh check

# Start TUI
./run.sh tui
```

## 🔗 Resources

- **Documentation**: [docs/](docs/)
- **API Docs**: [docs/_build/html/](docs/_build/html/)
- **Queen Bee Wisdom**: `./run.sh queen`
- **CI/CD**: [`.github/workflows/ci.yml`](.github/workflows/ci.yml)

---

*"The Hive remembers all chains, serves all stakeholders, tracks all trends—and now codes 100% offline!"* 🐝

**5+ Models** | **2 Backends** | **28+ Agents** | **729 Nodes** | **Digital Root 9** | **100% Offline Coding**
