# 🕵️ Terminal 221b - Solana AI Detective System

A Sherlock Holmes-inspired AI agent system for Solana blockchain investigation, integrated with BeeAI Hive 999.

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  🕵️ TERMINAL 221b ⟡ SOLANA AI DETECTIVE ⟡ "The game is afoot!"           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## Overview

Terminal 221b extends the BeeAI Hive 999 architecture with specialized Solana blockchain capabilities:

- **4 Detective Personalities**: Holmes (analytical), Watson (supportive), Mycroft (strategic), Irene (adaptable)
- **Safe Transaction Simulation**: Local Solana validator for risk-free testing
- **Natural Language Blockchain Operations**: Query balances, analyze addresses, construct transactions
- **Multi-Agent Worker Pool**: Parallel investigations across multiple contexts
- **Human-in-the-Loop Safety**: Configurable approval thresholds for financial operations

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 BEEAI HIVE 999 TUI                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │  Queen  │  │ Workers │  │  Drones │  │ Foragers│    │
│  │  Bee    │  │  (9)    │  │  (9)    │  │  (9)    │    │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │
│       └─────────────┴─────────────┴─────────────┘       │
│                          │                              │
│                    ┌─────┴─────┐                        │
│                    │  Alt+D    │  ← NEW: Terminal 221b  │
│                    └─────┬─────┘                        │
│                          │                              │
│       ┌──────────────────┼──────────────────┐           │
│       ▼                  ▼                  ▼           │
│  ┌─────────┐       ┌─────────┐       ┌─────────┐       │
│  │  HOLMES │       │  WATSON │       │ IRENE   │       │
│  │Detective│       │Detective│       │Detective│       │
│  └────┬────┘       └────┬────┘       └────┬────┘       │
│       │                  │                  │            │
│       └──────────────────┼──────────────────┘            │
│                          │                              │
│                    ┌─────┴─────┐                        │
│                    │ SimServer │  ← Local validator      │
│                    │ (Port 8899)│                        │
│                    └─────┬─────┘                        │
│                          │                              │
│       ┌──────────────────┼──────────────────┐           │
│       ▼                  ▼                  ▼           │
│   ┌────────┐        ┌────────┐        ┌────────┐       │
│   │ DEVNET │        │TESTNET │        │MAINNET │       │
│   └────────┘        └────────┘        └────────┘       │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Run the Demo

```bash
cd ~/beeai-hive-999
python terminal_221b/demo.py
```

### 2. Launch in TUI

```bash
./run.sh
```

Then use:
- `:221b help` - Show all 221b commands
- `:detective holmes` - Switch to Holmes personality
- `:investigate <address>` - Start investigation
- `:simulate <transaction>` - Test transaction safely
- `Alt+D` - Quick activate detective mode

### 3. Use in Code

```python
import asyncio
from terminal_221b import AdvisorDeps, create_detective

async def main():
    # Create detective with simulation mode (safe)
    agent = await create_detective(
        deps=AdvisorDeps.from_env(),
        personality="holmes"
    )
    
    # Investigate
    result = await agent.investigate(
        "Analyze address 9x...xyz"
    )
    print(result)
    
    # Safe transfer with simulation
    result = await agent.execute_transfer(
        recipient="9x...recipient",
        amount=1.5,
        simulate_first=True  # Always simulates first!
    )
    print(result)

asyncio.run(main())
```

## Detective Personalities

### 🎩 Sherlock Holmes (holmes)
- **Style**: Analytical, deductive, pattern-seeking
- **Best for**: Complex investigations, transaction tracing, anomaly detection
- **Quote**: *"When you have eliminated the impossible, whatever remains, however improbable, must be the truth."*

### 🩺 Dr. Watson (watson)
- **Style**: Supportive, methodical, clear explanations
- **Best for**: User guidance, educational queries, documentation
- **Quote**: *"Let me explain this in terms we can both understand."*

### 🌐 Mycroft Holmes (mycroft)
- **Style**: Strategic, network-aware, politically savvy
- **Best for**: Portfolio analysis, market dynamics, governance
- **Quote**: *"I am the British Government."*

### 💋 Irene Adler (irene)
- **Style**: Adaptable, perceptive, unconventional
- **Best for**: Social engineering detection, creative solutions
- **Quote**: *"I am the woman."*

## Safety Features

### Simulation-First Architecture

All state-changing operations follow this flow:

1. **Construct** → Build transaction
2. **Simulate** → Run on local validator
3. **Validate** → Check compute units, errors
4. **Approve** → Human approval if needed
5. **Execute** → Submit to network (or report if simulation)

### Safety Levels

```python
from terminal_221b.agents.advisor_deps import SafetyLevel

# Fully autonomous (simulation only)
deps = AdvisorDeps(
    safety_level=SafetyLevel.FULLY_AUTONOMOUS,
    simulation_mode=True
)

# Moderate - approve transactions > 0.1 SOL
deps = AdvisorDeps(
    safety_level=SafetyLevel.APPROVE_MODERATE,
    auto_approve_threshold_lamports=100_000_000  # 0.1 SOL
)

# Strict - approve all transactions
deps = AdvisorDeps(
    safety_level=SafetyLevel.APPROVE_ALL
)
```

## Project Structure

```
terminal_221b/
├── __init__.py              # Main exports
├── README.md                # This file
├── demo.py                  # Demonstration script
│
├── agents/                  # Agent implementations
│   ├── advisor_deps.py      # Configuration & DI
│   ├── detective_agent.py   # Core detective agent
│   └── worker_pool.py       # Concurrent execution
│
├── blockchain/              # Solana interaction (future)
│   ├── solana_client.py
│   ├── ethereum_client.py
│   └── program_compiler.py
│
├── simulation/              # Safe testing environment
│   └── sim_server.py        # Local validator wrapper
│
└── integration/             # BeeAI Hive 999 bridge
    └── hive_bridge.py       # TUI integration
```

## Configuration

### Environment Variables

```bash
# Network environment
export TERMINAL_221B_ENV=simulation  # simulation | devnet | testnet | mainnet

# Safety settings
export TERMINAL_221B_SAFETY=moderate  # autonomous | notify | moderate | strict
export TERMINAL_221B_SIMULATION=true

# Personality
export TERMINAL_221B_PERSONALITY=holmes

# API keys (for cloud features)
export OPENAI_API_KEY="sk-..."
export LANGSMITH_API_KEY="ls-..."
```

### Programmatic Configuration

```python
from terminal_221b import AdvisorDeps, NetworkEnvironment, SafetyLevel

# Simulation config (safest)
deps = AdvisorDeps.get_simulation_config()

# Devnet config
deps = AdvisorDeps.get_devnet_config()

# Mainnet config (use with caution!)
deps = AdvisorDeps.get_mainnet_config(
    wallet_key="your_private_key",
    safety_level=SafetyLevel.APPROVE_ALL
)
```

## TUI Commands

| Command | Description |
|---------|-------------|
| `:221b status` | Show detective status |
| `:221b mode holmes` | Switch personality |
| `:221b sim start` | Start simulation server |
| `:221b sim stop` | Stop simulation server |
| `:221b env devnet` | Switch environment |
| `:detective watson` | Quick personality switch |
| `:investigate <query>` | Start investigation |
| `:simulate <tx>` | Simulate transaction |

| Keybinding | Action |
|------------|--------|
| `Alt+D` | Activate detective mode |
| `Alt+Shift+D` | Cycle personalities |

## Roadmap

### Phase 1: Foundation ✅
- [x] Core agent architecture
- [x] 4 detective personalities
- [x] Simulation server
- [x] Worker pool
- [x] TUI integration

### Phase 2: Solana Integration
- [ ] Real Solana RPC client
- [ ] Transaction construction
- [ ] SPL token operations
- [ ] Program interaction
- [ ] Wallet management

### Phase 3: Advanced Features
- [ ] Hypercube computational model
- [ ] Multi-chain (Ethereum via ethers)
- [ ] MEV-aware execution
- [ ] Jito bundle integration
- [ ] Historical analysis

### Phase 4: Production
- [ ] Security audit
- [ ] HSM integration
- [ ] Multi-signature support
- [ ] Comprehensive testing

## Integration with Existing Hive 999

Terminal 221b is designed to complement, not replace, the existing Hive architecture:

- **Queen Bee** still orchestrates high-level strategy
- **Worker-SOL** (existing) provides general Solana knowledge
- **Terminal 221b** adds deep investigative capabilities

The `:221b` command family exists alongside `:queen`, `:worker`, etc.

## Philosophy

> "When you have eliminated the impossible, whatever remains, however improbable, must be the truth." - Sherlock Holmes

Terminal 221b applies this philosophy to blockchain analysis:

1. **Observe** all available on-chain data
2. **Hypothesize** about patterns and behaviors
3. **Simulate** to test hypotheses safely
4. **Conclude** with calibrated confidence
5. **Execute** only when truth is established

## License

Part of BeeAI Hive 999 - See main project license.

---

*"The Hive remembers all chains. The Detective traces all transactions."*

**4 Personalities** | **4 Environments** | **Simulation-First** | **221B Baker Street**
