# BeeAI Hive 999 — Architecture

## Overview

Hive 999 is a multi-agent system built on the **BeeAI Framework** that models the intersection of **9 blockchains × 9 stakeholder groups × 9 industry trends** — producing a 729-node knowledge matrix (digital root: 9). Agents are organized in a bee-colony hierarchy, each tier running a different LLM based on task complexity.

## Agent Hierarchy

```
                    ┌─────────────┐
                    │  Queen Bee   │  granite3.3:8b — orchestrator
                    │ (Requirement │  Understands full 729 matrix
                    │   Agent)     │  Routes queries to specialists
                    └──────┬──────┘
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
   ┌──────────────┐ ┌────────────┐ ┌─────────────┐
   │ Worker Bees  │ │   Drones   │ │  Foragers   │
   │ (9 blockchain│ │(9 stake-   │ │ (9 trend    │
   │  agents)     │ │ holder     │ │  agents)    │
   │ llama3.2:3b  │ │ agents)    │ │ llama3.2:3b │
   └──────────────┘ │ llama3.2:3b│ └─────────────┘
                    └────────────┘
                           │
                    ┌──────┴──────┐
                    │ Mantis Mail │  (stub — email assistant)
                    └─────────────┘
```

| Tier | Count | Model | Role |
|------|-------|-------|------|
| **Queen Bee** | 1 | `granite3.3:8b` | Orchestrates all queries, reasons over the full matrix, delegates to specialists |
| **Worker Bees** | 9 | `llama3.2:3b` | One per blockchain (Bitcoin, Ethereum, Solana, TRON, Stellar, Avalanche, Arbitrum One, Polygon PoS, Optimism). Each owns 81 matrix nodes. |
| **Drones** | 9 | `llama3.2:3b` | One per stakeholder (Customers, Employees, Investors, Owners, Suppliers & Vendors, Communities, Trade Unions, Government Agencies, Media) |
| **Foragers** | 9 | `llama3.2:3b` | One per trend (Asset Tokenization, DeFi Maturation, Supply Chain Provenance, SSI, CBDCs pilots, AI-Blockchain synergies, Sustainability-compliant validation, RegTech compliance layers, Cross-chain interoperability) |
| **Mantis Mail** | 1 | TBD | Email drafting, GitHub summaries, weekly reports (stub) |

## Tools

| Tool | Purpose |
|------|---------|
| `matrix_search` | Semantic search over 729 matrix nodes via ChromaDB |
| `compliance_check` | KYC/AML + ESG scoring per chain/stakeholder. MiCA-aware. |
| `federation_route` | Simulates cross-chain routing with digital-root invariance |
| `caterpillar_ansi` | Loads and displays Moebius-style ANSI art |
| `ThinkTool` | BeeAI built-in chain-of-thought |

## Data Layer

- **matrix_729.json** — 729 nodes, each with `{id, blockchain, stakeholder, trend, digital_root, description}`
- **ChromaDB** (`data/vectors/hive_vectors/`, collection `matrix_999`) — ONNX-embedded vectors for semantic retrieval
- Digital root of every node ID computes to 9 (the hive number)

## TUI Layout

```
┌─────────────────────────────────────────────────────┐
│  🐝 HIVE 999 — BeeAI Multi-Agent System    [status]│
├────────────┬──────────────────────┬─────────────────┤
│ AGENTS     │                      │   ANSI ART      │
│            │   CHAT LOG           │                  │
│ [Alt+Q]    │   (scrollable)       │   (art panel)    │
│  Queen     │                      │                  │
│ [Alt+1-9]  │                      │                  │
│  Workers   │                      │                  │
│            │                      │                  │
├────────────┴──────────────────────┴─────────────────┤
│ [queen] > _                                         │
└─────────────────────────────────────────────────────┘
```

## Infrastructure

- **Runtime**: Python 3.11+, Ubuntu Linux, NVIDIA GTX 1080, CUDA 12.2
- **LLM Backend**: Ollama (local)
- **Vector Store**: ChromaDB with ONNX embeddings
- **Framework**: beeai-framework (RequirementAgent, ChatModel, tools)
- **TUI**: prompt_toolkit full-screen application
- **Service**: systemd unit for headless operation
