# BeeAI Hive 999

## Description
Unified multi-agent AI ecosystem with 28+ agents, Solana blockchain integration, detective-themed investigation layer, bounty hunter, and alien command center. Self-funding sovereign AI development environment.

## When to Use
- Need orchestrated multi-agent workflows
- Blockchain intelligence and investigation
- Solana transaction analysis
- Bug bounty automation
- Complex agent coordination (Queen + Workers + Drones)

## Architecture

```
Queen Bee (Orchestrator)
├── 9 Worker Bees (Task execution)
├── 9 Drones (Data collection)
├── 9 Foragers (External APIs)
└── Mantis Mail (Communications)
```

## Key Components

| Component | Purpose |
|-----------|---------|
| Hive 999 Core | Multi-agent blockchain intelligence |
| Terminal 221b | Sherlock-style Solana detective |
| Bounty Hunter | Bug bounty automation + OpenClaw |
| Alien Command | Rust execution engine + Lua scripting |

## Quick Start

```bash
git clone https://github.com/BoozeLee/beeai-hive-999
cd beeai-hive-999
docker-compose up -d

# Or run specific agent
cd agents/queen-bee
npm install && npm start
```

## Agent Communication

Agents communicate via structured messages:
```json
{
  "from": "worker-3",
  "to": "queen",
  "type": "task_complete",
  "payload": { "tx_analyzed": "5abc...", "risk": "low" }
}
```

## Links
- Repository: https://github.com/BoozeLee/beeai-hive-999
- Terminal 221b: Detective layer docs
- Bounty Hunter: OpenClaw integration
