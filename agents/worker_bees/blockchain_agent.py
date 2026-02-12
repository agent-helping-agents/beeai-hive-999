"""
Worker Bee Factory — one specialist agent per blockchain.

Each Worker Bee owns 81 matrix nodes (1 blockchain × 9 stakeholders × 9 trends)
and uses llama3.2:3b for fast, focused responses.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.think import ThinkTool

from tools.blockchain.matrix_search import matrix_search_tool
from tools.regtech.compliance_checker import compliance_check_tool

BLOCKCHAINS: list[str] = [
    "Bitcoin", "Ethereum", "Solana", "TRON", "Stellar",
    "Avalanche", "Arbitrum One", "Polygon PoS", "Optimism",
]

# Short aliases for TUI commands
BLOCKCHAIN_ALIASES: dict[str, str] = {
    "btc": "Bitcoin", "bitcoin": "Bitcoin",
    "eth": "Ethereum", "ethereum": "Ethereum",
    "sol": "Solana", "solana": "Solana",
    "tron": "TRON", "trx": "TRON",
    "xlm": "Stellar", "stellar": "Stellar",
    "avax": "Avalanche", "avalanche": "Avalanche",
    "arb": "Arbitrum One", "arbitrum": "Arbitrum One",
    "matic": "Polygon PoS", "polygon": "Polygon PoS",
    "op": "Optimism", "optimism": "Optimism",
}


def _worker_instructions(chain: str) -> str:
    return f"""\
You are a **Worker Bee** specializing in the **{chain}** blockchain.
You own 81 matrix nodes covering {chain} across all 9 stakeholder groups
and all 9 industry trends.

Use `matrix_search` filtered to {chain} to answer queries.
Use `compliance_check` when regulation or ESG is relevant.

Be precise, technical, and fast. Defer cross-chain questions to the Queen.
"""


def create_worker_bee(chain: str) -> RequirementAgent:
    """Create a Worker Bee agent for the given blockchain."""
    llm = ChatModel.from_name("ollama:llama3.2:3b")
    return RequirementAgent(
        llm=llm,
        tools=[ThinkTool(), matrix_search_tool, compliance_check_tool],
        memory=UnconstrainedMemory(),
        instructions=_worker_instructions(chain),
        requirements=[
            f"Only answer questions related to {chain}.",
            "Cite matrix node IDs in responses.",
        ],
    )


def create_all_workers() -> dict[str, RequirementAgent]:
    """Create all 9 Worker Bee agents. Returns {chain_name: agent}."""
    return {chain: create_worker_bee(chain) for chain in BLOCKCHAINS}


def resolve_chain(alias: str) -> str | None:
    """Resolve a user-typed alias to a canonical blockchain name."""
    return BLOCKCHAIN_ALIASES.get(alias.lower())
