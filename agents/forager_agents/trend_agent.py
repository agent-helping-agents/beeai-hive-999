"""
Forager Agent Factory — one specialist per industry trend.

Each Forager owns 81 matrix nodes (9 blockchains × 9 stakeholders × 1 trend).
Uses llama3.2:3b for speed.
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

TRENDS: list[str] = [
    "Asset Tokenization", "DeFi Maturation", "Supply Chain Provenance",
    "Self-Sovereign Identity (SSI)", "CBDCs pilots",
    "AI-Blockchain synergies", "Sustainability-compliant validation",
    "RegTech compliance layers", "Cross-chain interoperability",
]

TREND_ALIASES: dict[str, str] = {
    "tokenization": "Asset Tokenization", "token": "Asset Tokenization",
    "defi": "DeFi Maturation",
    "supply chain": "Supply Chain Provenance", "provenance": "Supply Chain Provenance",
    "ssi": "Self-Sovereign Identity (SSI)", "identity": "Self-Sovereign Identity (SSI)",
    "cbdc": "CBDCs pilots", "cbdcs": "CBDCs pilots",
    "ai": "AI-Blockchain synergies", "ai-blockchain": "AI-Blockchain synergies",
    "sustainability": "Sustainability-compliant validation", "esg": "Sustainability-compliant validation",
    "regtech": "RegTech compliance layers", "compliance": "RegTech compliance layers",
    "crosschain": "Cross-chain interoperability", "ibc": "Cross-chain interoperability",
    "interop": "Cross-chain interoperability",
}


def _forager_instructions(trend: str) -> str:
    return f"""\
You are a **Forager Agent** specializing in the **{trend}** industry trend.
You own 81 matrix nodes covering {trend} across all 9 blockchains
and all 9 stakeholder groups.

Analyze how {trend} is evolving and its implications across the matrix.
Use `matrix_search` to find relevant nodes.
Be forward-looking and cite concrete examples.
"""


def create_forager(trend: str) -> RequirementAgent:
    """Create a Forager agent for the given trend."""
    llm = ChatModel.from_name("ollama:llama3.2:3b")
    return RequirementAgent(
        llm=llm,
        tools=[ThinkTool(), matrix_search_tool],
        memory=UnconstrainedMemory(),
        instructions=_forager_instructions(trend),
        requirements=[
            f"Focus analysis on the {trend} trend.",
            "Cite matrix node IDs in responses.",
        ],
    )


def create_all_foragers() -> dict[str, RequirementAgent]:
    """Create all 9 Forager agents. Returns {trend_name: agent}."""
    return {t: create_forager(t) for t in TRENDS}


def resolve_trend(alias: str) -> str | None:
    """Resolve a user-typed alias to a canonical trend name."""
    return TREND_ALIASES.get(alias.lower())
