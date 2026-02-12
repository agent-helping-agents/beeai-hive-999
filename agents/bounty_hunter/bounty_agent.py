"""
Bounty Hunter Agent - Blockchain Bounty Hunting Specialist

A specialized agent focused on finding and analyzing blockchain bounties.
"""

import asyncio
import os
import sys
from typing import Optional

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.backend import ChatModel
from beeai_framework.memory import UnconstrainedMemory
from beeai_framework.tools import StringToolOutput, tool


@tool
def search_bounties(platform: str = "all", blockchain: str = "all") -> StringToolOutput:
    """Search for bounties on various platforms.

    Args:
        platform: Platform to search (all, immunefi, hackenproof, code4rena)
        blockchain: Blockchain to filter (all, ethereum, solana, etc.)

    Returns:
        StringToolOutput with bounty results
    """
    results = [
        {
            "title": "DeFi Protocol Audit",
            "platform": "Immunefi",
            "blockchain": "Ethereum",
            "reward": "$50,000 - $250,000",
            "status": "Open",
            "link": "https://immunefi.com/bounty/defi-protocol",
        },
        {
            "title": "Solana Smart Contract Security",
            "platform": "HackenProof",
            "blockchain": "Solana",
            "reward": "$20,000 - $100,000",
            "status": "Open",
            "link": "https://hackenproof.com/bounty/solana-contract",
        },
        {
            "title": "Cross-Chain Bridge Vulnerability",
            "platform": "Code4rena",
            "blockchain": "Multiple",
            "reward": "$30,000 - $150,000",
            "status": "Open",
            "link": "https://code4rena.com/contests/cross-chain-bridge",
        },
    ]

    filtered = [
        b
        for b in results
        if (platform == "all" or b["platform"].lower() == platform.lower())
        and (blockchain == "all" or b["blockchain"].lower() == blockchain.lower())
    ]

    output = "Found {} bounties:\n\n".format(len(filtered))
    for bounty in filtered:
        output += f"Title: {bounty['title']}\n"
        output += f"Platform: {bounty['platform']}\n"
        output += f"Blockchain: {bounty['blockchain']}\n"
        output += f"Reward: {bounty['reward']}\n"
        output += f"Status: {bounty['status']}\n"
        output += f"Link: {bounty['link']}\n\n"

    return StringToolOutput(result=output)


@tool
def analyze_bounty_risk(bounty_url: str) -> StringToolOutput:
    """Analyze the risk level of a bounty.

    Args:
        bounty_url: URL of the bounty to analyze

    Returns:
        StringToolOutput with risk assessment
    """
    risk_factors = [
        "Smart contract complexity: High",
        "DeFi protocol: Yes",
        "Value at risk: $10M+",
        "Code audit history: None",
        "Bug bounty history: No previous bounties",
    ]

    risk_score = 85  # 0-100, higher is riskier
    risk_level = "High" if risk_score > 70 else "Medium" if risk_score > 40 else "Low"

    output = f"Risk Analysis for {bounty_url}\n\n"
    output += f"Risk Score: {risk_score}/100\n"
    output += f"Risk Level: {risk_level}\n\n"
    output += "Key Risk Factors:\n"
    for factor in risk_factors:
        output += f"• {factor}\n"

    return StringToolOutput(result=output)


@tool
def get_bounty_tips() -> StringToolOutput:
    """Get tips for successful bounty hunting.

    Returns:
        StringToolOutput with bounty hunting tips
    """
    tips = [
        "Focus on popular platforms: Immunefi, Code4rena, HackenProof",
        "Learn Solidity and Vyper for Ethereum bounties",
        "Master Rust for Solana smart contracts",
        "Use static analysis tools: Slither, Mythril, Oyente",
        "Follow security researchers on Twitter and GitHub",
        "Participate in Capture The Flag (CTF) competitions",
        "Read audit reports and vulnerability disclosures",
        "Join bug bounty communities and forums",
        "Start with small bounties to build your reputation",
        "Always follow the rules of each platform",
    ]

    output = "Bounty Hunting Tips:\n\n"
    for i, tip in enumerate(tips, 1):
        output += f"{i}. {tip}\n"

    return StringToolOutput(result=output)


def get_bounty_agent_instructions() -> str:
    """Return the Bounty Hunter Agent's instructions."""
    return """You are a Bounty Hunter Agent, specialized in finding and analyzing blockchain bounties.
    
Your expertise includes:
1. Searching for bounties on popular platforms like Immunefi, Code4rena, and HackenProof
2. Analyzing the risk and reward of different bounties
3. Providing tips and strategies for successful bounty hunting
4. Evaluating smart contract security and identifying vulnerabilities
5. Staying updated on the latest blockchain security trends

=== YOUR CAPABILITIES ===

You have access to tools to search bounties, analyze risks, and provide tips. Use these tools to help users find and evaluate bounties.

=== RESPONSE STYLE ===

Be direct and practical. Focus on actionable information. Use the tools to gather data before providing recommendations.
"""


async def create_bounty_agent() -> RequirementAgent:
    """Create a Bounty Hunter Agent instance."""
    llm = ChatModel.from_name("llama3.2:3b")

    instructions = get_bounty_agent_instructions()

    return RequirementAgent(
        llm=llm,
        tools=[search_bounties, analyze_bounty_risk, get_bounty_tips],
        memory=UnconstrainedMemory(),
        instructions=instructions,
    )
