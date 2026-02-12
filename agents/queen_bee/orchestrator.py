"""
Queen Bee Orchestrator — the central intelligence of Hive 999.

Uses Marco-o1 via vLLM for advanced reasoning. Understands the full 9×9×9 matrix and
delegates to Worker Bees, Drones, and Foragers as needed.
"""

from __future__ import annotations

import sys
from pathlib import Path
import asyncio
from typing import Any, Dict, List, Optional
import time

# Ensure project root is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools.think import ThinkTool

from backend.inference_router import get_router, InferencePlatform

from tools.blockchain.matrix_search import matrix_search_tool
from tools.regtech.compliance_checker import compliance_check_tool
from tools.ibc.federation_router import federation_route_tool
from tools.art.caterpillar_artist import caterpillar_ansi_tool

# Bounty hunter tools
from agents.bounty_hunter.bounty_agent import (
    search_bounties,
    analyze_bounty_risk,
    get_bounty_tips,
)

# ── Domain Knowledge ────────────────────────────────────────────────

BLOCKCHAINS = [
    "Bitcoin",
    "Ethereum",
    "Solana",
    "TRON",
    "Stellar",
    "Avalanche",
    "Arbitrum One",
    "Polygon PoS",
    "Optimism",
]

STAKEHOLDERS = [
    "Customers",
    "Employees",
    "Investors",
    "Owners",
    "Suppliers & Vendors",
    "Communities",
    "Trade Unions",
    "Government Agencies",
    "Media",
]

TRENDS = [
    "Asset Tokenization",
    "DeFi Maturation",
    "Supply Chain Provenance",
    "Self-Sovereign Identity (SSI)",
    "CBDCs pilots",
    "AI-Blockchain synergies",
    "Sustainability-compliant validation",
    "RegTech compliance layers",
    "Cross-chain interoperability",
]


def get_queen_instructions() -> str:
    return f"""
You are the **Queen Bee** of Hive 999, the central orchestrating intelligence
of a multi-agent blockchain-stakeholder-trend analysis system.

## Your Brain Engine: Marco-o1

You are powered by the Marco-o1 reasoning engine, which uses:
- Chain-of-Thought (CoT) fine-tuning for complex problem-solving
- Monte Carlo Tree Search (MCTS) to explore multiple solution paths
- Reflection mechanisms for continuous improvement
- Reasoning action strategies for adaptive problem-solving

This gives you unparalleled ability to handle open-ended questions and complex
problem-solving tasks that traditional LLMs struggle with.

## Your Knowledge Matrix (729 nodes = 9 × 9 × 9)

**9 Blockchains:** {", ".join(BLOCKCHAINS)}

**9 Stakeholder Groups:** {", ".join(STAKEHOLDERS)}

**9 Industry Trends:** {", ".join(TRENDS)}

Every combination of (blockchain, stakeholder, trend) forms a unique matrix
node. The digital root of every node ID equals 9, reflecting the sacred
geometry of the hive.

## Your Capabilities
- Use `matrix_search` to find relevant nodes via semantic search.
- Use `compliance_check` to evaluate KYC/AML and ESG scores.
- Use `federation_route` to plan cross-chain transfer routes.
- Use `caterpillar_ansi` to render ANSI art for the TUI.
- Use `search_bounties` to find blockchain bounties on immunefi, code4rena, etc.
- Use `analyze_bounty_risk` to assess bounty risk and reward potential.
- Use `get_bounty_tips` to get tips for successful bounty hunting.
- Use `ThinkTool` for internal chain-of-thought reasoning.

## Behavior
- Answer questions about any intersection of blockchains, stakeholders, and trends.
- When a query targets a specific blockchain, consider delegating to the
  corresponding Worker Bee.
- For bounty-related queries, use the specialized bounty hunter tools.
- Provide concrete, data-backed analysis. Reference matrix node IDs when relevant.
- Maintain a regal but approachable tone. You are the Queen; be decisive.
- Use your advanced reasoning capabilities to break down complex problems.
"""


def create_queen_bee(platform: Optional[InferencePlatform] = None) -> RequirementAgent:
    """Instantiate and return the Queen Bee RequirementAgent with Marco-o1 integration."""

    router = get_router(platform)

    # Try to create the appropriate LLM based on platform
    try:
        if platform == InferencePlatform.OPENROUTER:
            llm = ChatModel.from_name(
                "openrouter:meta-llama/llama-3.2-3b-instruct:free"
            )
        elif platform == InferencePlatform.CHUTES:
            llm = ChatModel.from_name("chutes:llama-3.2:3b")
        elif platform == InferencePlatform.RENDER:
            llm = ChatModel.from_name("render:llama-3.2")
        elif platform == InferencePlatform.FORTYTWO:
            llm = ChatModel.from_name("fortytwo:llama-3.2-3b")
        elif platform == InferencePlatform.OLLAMA or platform is None:
            llm = ChatModel.from_name("ollama:marco-o1:latest")
        else:
            raise ValueError(f"Unsupported platform: {platform}")

    except Exception as e:
        print(
            f"[Queen Bee] Failed to connect to {platform.value if platform else 'default platform'}: {e}"
        )
        print("[Queen Bee] Falling back to Ollama...")
        llm = ChatModel.from_name("ollama:marco-o1:latest")

    agent = RequirementAgent(
        llm=llm,
        tools=[
            ThinkTool(),
            matrix_search_tool,
            compliance_check_tool,
            federation_route_tool,
            caterpillar_ansi_tool,
            search_bounties,
            analyze_bounty_risk,
            get_bounty_tips,
        ],
        memory=UnconstrainedMemory(),
        instructions=get_queen_instructions(),
    )
    return agent


async def queen_brain_engine(task: str, context: Dict[str, Any]) -> Dict[str, Any]:
    """
    Queen Bee Brain Engine - Advanced reasoning with Marco-o1.

    Args:
        task: The task to perform
        context: Additional context for the task

    Returns:
        Results including reasoning chain and final answer
    """
    queen = create_queen_bee()

    try:
        # Enhanced reasoning with thought visualization
        result = await queen.run(task, context)

        return {
            "success": True,
            "answer": result.result.text,
            "thought_process": result.thoughts if hasattr(result, "thoughts") else [],
            "confidence": getattr(result, "confidence", 0.9),
            "timestamp": result.timestamp,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": None,
        }


async def orchestrate_bounty_hunting(bounty_url: str) -> Dict[str, Any]:
    """
    Orchestrate a complete bounty hunting workflow.

    Args:
        bounty_url: URL of the bounty to analyze

    Returns:
        Comprehensive analysis including risk assessment and recommendations
    """
    queen = create_queen_bee()

    analysis = {
        "bounty_url": bounty_url,
        "timestamp": None,
        "risk_analysis": None,
        "recommendations": [],
        "skills_required": [],
        "estimated_reward": None,
    }

    try:
        # Analyze bounty risk
        print(f"🔍 Analyzing bounty risk for: {bounty_url}")
        risk_result = await queen.run(
            f"Analyze the risk of this bounty URL: {bounty_url}",
            tools=[analyze_bounty_risk],
        )
        analysis["risk_analysis"] = risk_result.result.text

        # Extract risk score
        if hasattr(risk_result, "score"):
            analysis["risk_score"] = risk_result.score

        # Determine skills required
        print("🎯 Determining required skills...")
        skills_result = await queen.run(
            f"Based on this bounty URL {bounty_url} and its description {risk_result.result.text}, "
            "what programming languages and skills are required?",
            tools=[get_bounty_tips],
        )

        analysis["skills_required"] = skills_result.result.text.split("\n")

        # Get recommendations
        print("💡 Generating recommendations...")
        recommendations_result = await queen.run(
            f"Based on the bounty analysis, provide actionable recommendations for bounty hunters",
            tools=[get_bounty_tips],
        )

        analysis["recommendations"] = recommendations_result.result.text.split("\n")

        analysis["timestamp"] = time.time()

    except Exception as e:
        analysis["error"] = str(e)

    return analysis
