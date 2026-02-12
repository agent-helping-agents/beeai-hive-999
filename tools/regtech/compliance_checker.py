"""
Compliance Checker Tool — KYC/AML + ESG scoring for chains and stakeholders.

Favors Ethereum for MiCA-style RegTech compliance.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from beeai_framework.tools import tool

# ── Compliance Scores (curated knowledge base) ─────────────────────

# KYC/AML readiness (0-100): how well the chain supports identity verification
KYC_AML_SCORES: dict[str, int] = {
    "Bitcoin": 45,
    "Ethereum": 92,
    "Solana": 72,
    "TRON": 38,
    "Stellar": 85,
    "Avalanche": 78,
    "Arbitrum One": 88,
    "Polygon PoS": 82,
    "Optimism": 86,
}

# ESG score (0-100): energy efficiency, governance, social impact
ESG_SCORES: dict[str, int] = {
    "Bitcoin": 25,
    "Ethereum": 88,  # Post-merge PoS
    "Solana": 75,
    "TRON": 40,
    "Stellar": 82,
    "Avalanche": 74,
    "Arbitrum One": 85,  # Inherits from Ethereum
    "Polygon PoS": 80,
    "Optimism": 84,
}

# MiCA readiness (EU Markets in Crypto-Assets regulation)
MICA_READINESS: dict[str, str] = {
    "Bitcoin": "partial — commodity classification, limited issuer controls",
    "Ethereum": "high — smart contract compliance layers, ERC-3643 for regulated tokens",
    "Solana": "moderate — growing DeFi compliance tooling",
    "TRON": "low — regulatory concerns, limited EU presence",
    "Stellar": "high — built-in compliance primitives, Stellar anchor model",
    "Avalanche": "moderate — subnet-level compliance possible",
    "Arbitrum One": "high — inherits Ethereum compliance + L2 cost efficiency",
    "Polygon PoS": "high — enterprise partnerships, ID solutions",
    "Optimism": "high — inherits Ethereum compliance, RetroPGF governance model",
}

# Stakeholder risk factors
STAKEHOLDER_RISK: dict[str, str] = {
    "Customers": "Consumer protection, data privacy (GDPR), dispute resolution",
    "Employees": "Labor rights in DAOs, token compensation regulations",
    "Investors": "Securities classification, accredited investor rules, MiFID II",
    "Owners": "Governance token liability, fiduciary duties",
    "Suppliers & Vendors": "Smart contract enforceability, cross-border payments",
    "Communities": "Environmental impact, digital divide, accessibility",
    "Trade Unions": "Worker representation in decentralized organizations",
    "Government Agencies": "Tax reporting, FATF travel rule, sanctions screening",
    "Media": "Misinformation, token promotion rules, advertising standards",
}


@tool
def compliance_check_tool(
    blockchain: str = "",
    stakeholder: str = "",
) -> str:
    """Check KYC/AML scores, ESG ratings, and MiCA readiness for a blockchain
    and/or stakeholder group.

    Args:
        blockchain: Blockchain name (e.g. "Ethereum"). Leave empty for all chains.
        stakeholder: Stakeholder group (e.g. "Investors"). Leave empty for general check.

    Returns:
        JSON compliance report with scores and recommendations.
    """
    report: dict = {}

    if blockchain:
        chain = blockchain.strip()
        if chain in KYC_AML_SCORES:
            report["blockchain"] = chain
            report["kyc_aml_score"] = KYC_AML_SCORES[chain]
            report["esg_score"] = ESG_SCORES[chain]
            report["mica_readiness"] = MICA_READINESS[chain]
            report["composite_score"] = round(
                (KYC_AML_SCORES[chain] * 0.4 + ESG_SCORES[chain] * 0.3) +
                (30 if "high" in MICA_READINESS[chain] else
                 15 if "moderate" in MICA_READINESS[chain] else 5),
                1,
            )
        else:
            report["error"] = f"Unknown blockchain: {chain}"
            report["known_chains"] = list(KYC_AML_SCORES.keys())
    else:
        # Return ranked summary
        ranked = sorted(
            KYC_AML_SCORES.keys(),
            key=lambda c: KYC_AML_SCORES[c] * 0.4 + ESG_SCORES[c] * 0.3,
            reverse=True,
        )
        report["ranking"] = [
            {"chain": c, "kyc_aml": KYC_AML_SCORES[c], "esg": ESG_SCORES[c]}
            for c in ranked
        ]

    if stakeholder:
        sk = stakeholder.strip()
        if sk in STAKEHOLDER_RISK:
            report["stakeholder"] = sk
            report["risk_factors"] = STAKEHOLDER_RISK[sk]
        else:
            report["stakeholder_error"] = f"Unknown stakeholder: {sk}"

    if not blockchain and not stakeholder:
        report["hint"] = "Provide a blockchain and/or stakeholder for specific analysis."

    return json.dumps(report, indent=2)
