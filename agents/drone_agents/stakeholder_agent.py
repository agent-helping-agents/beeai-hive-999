"""
Drone Agent Factory — one specialist per stakeholder group.

Each Drone owns 81 matrix nodes (9 blockchains × 1 stakeholder × 9 trends).
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
from tools.regtech.compliance_checker import compliance_check_tool

STAKEHOLDERS: list[str] = [
    "Customers", "Employees", "Investors", "Owners",
    "Suppliers & Vendors", "Communities", "Trade Unions",
    "Government Agencies", "Media",
]

STAKEHOLDER_ALIASES: dict[str, str] = {
    "customers": "Customers", "cust": "Customers",
    "employees": "Employees", "emp": "Employees",
    "investors": "Investors", "inv": "Investors",
    "owners": "Owners", "own": "Owners",
    "suppliers": "Suppliers & Vendors", "vendors": "Suppliers & Vendors",
    "communities": "Communities", "comm": "Communities",
    "unions": "Trade Unions", "trade unions": "Trade Unions",
    "gov": "Government Agencies", "government": "Government Agencies",
    "media": "Media", "press": "Media",
}


def _drone_instructions(stakeholder: str) -> str:
    return f"""\
You are a **Drone Agent** specializing in the **{stakeholder}** stakeholder group.
You own 81 matrix nodes covering {stakeholder} across all 9 blockchains
and all 9 industry trends.

Analyze how blockchain technology impacts {stakeholder}.
Use `matrix_search` to find relevant nodes. Use `compliance_check` for regulatory context.
Be stakeholder-focused and empathetic to their concerns.
"""


def create_drone(stakeholder: str) -> RequirementAgent:
    """Create a Drone agent for the given stakeholder group."""
    llm = ChatModel.from_name("ollama:llama3.2:3b")
    return RequirementAgent(
        llm=llm,
        tools=[ThinkTool(), matrix_search_tool, compliance_check_tool],
        memory=UnconstrainedMemory(),
        instructions=_drone_instructions(stakeholder),
        requirements=[
            f"Focus analysis on the {stakeholder} perspective.",
            "Cite matrix node IDs in responses.",
        ],
    )


def create_all_drones() -> dict[str, RequirementAgent]:
    """Create all 9 Drone agents. Returns {stakeholder_name: agent}."""
    return {s: create_drone(s) for s in STAKEHOLDERS}


def resolve_stakeholder(alias: str) -> str | None:
    """Resolve a user-typed alias to a canonical stakeholder name."""
    return STAKEHOLDER_ALIASES.get(alias.lower())
