#!/usr/bin/env python3
"""
Generate matrix_729.json — all 729 nodes of the Hive 999 knowledge matrix.

Each node: 9 blockchains × 9 stakeholders × 9 trends.
Digital root of every node ID = 9.
"""

from __future__ import annotations

import json
from pathlib import Path

BLOCKCHAINS = [
    "Bitcoin", "Ethereum", "Solana", "TRON", "Stellar",
    "Avalanche", "Arbitrum One", "Polygon PoS", "Optimism",
]

STAKEHOLDERS = [
    "Customers", "Employees", "Investors", "Owners",
    "Suppliers & Vendors", "Communities", "Trade Unions",
    "Government Agencies", "Media",
]

TRENDS = [
    "Asset Tokenization", "DeFi Maturation", "Supply Chain Provenance",
    "Self-Sovereign Identity (SSI)", "CBDCs pilots",
    "AI-Blockchain synergies", "Sustainability-compliant validation",
    "RegTech compliance layers", "Cross-chain interoperability",
]

# Short descriptors per dimension for richer descriptions
CHAIN_TRAITS: dict[str, str] = {
    "Bitcoin": "the original decentralized store-of-value network",
    "Ethereum": "the leading smart-contract platform (PoS)",
    "Solana": "a high-throughput, low-latency L1",
    "TRON": "a content-focused chain with large USDT volume",
    "Stellar": "a payments-oriented network with built-in compliance anchors",
    "Avalanche": "a subnet-based platform for customizable blockchains",
    "Arbitrum One": "Ethereum's largest optimistic rollup L2",
    "Polygon PoS": "an EVM-compatible sidechain with enterprise adoption",
    "Optimism": "an Ethereum L2 with RetroPGF governance",
}

STAKEHOLDER_FOCUS: dict[str, str] = {
    "Customers": "end-user adoption, UX, and consumer protection",
    "Employees": "workforce implications, DAO labor, and token compensation",
    "Investors": "returns, risk, portfolio exposure, and securities regulation",
    "Owners": "governance, fiduciary duty, and protocol ownership",
    "Suppliers & Vendors": "supply chain integration and B2B payments",
    "Communities": "social impact, inclusion, and environmental effects",
    "Trade Unions": "collective bargaining and worker representation in DAOs",
    "Government Agencies": "regulation, taxation, FATF compliance, and CBDCs",
    "Media": "narrative shaping, advertising standards, and transparency",
}

TREND_DESC: dict[str, str] = {
    "Asset Tokenization": "converting real-world assets to on-chain tokens",
    "DeFi Maturation": "evolution of decentralized lending, DEXs, and yield",
    "Supply Chain Provenance": "tracking goods from origin to consumer on-chain",
    "Self-Sovereign Identity (SSI)": "user-controlled digital identity and credentials",
    "CBDCs pilots": "central bank digital currency experimentation",
    "AI-Blockchain synergies": "intersection of AI agents and blockchain infrastructure",
    "Sustainability-compliant validation": "green consensus and ESG-aligned validation",
    "RegTech compliance layers": "automated regulatory compliance tooling",
    "Cross-chain interoperability": "bridging assets and messages across chains",
}


def digital_root(n: int) -> int:
    """Compute digital root of a positive integer."""
    if n == 0:
        return 0
    return 1 + (n - 1) % 9


def generate_matrix() -> list[dict]:
    """Generate all 729 matrix nodes."""
    nodes: list[dict] = []
    # IDs start at 9 and increment by 9, so digital root is always 9
    node_id = 9

    for b_idx, blockchain in enumerate(BLOCKCHAINS):
        for s_idx, stakeholder in enumerate(STAKEHOLDERS):
            for t_idx, trend in enumerate(TRENDS):
                description = (
                    f"{trend} on {blockchain} ({CHAIN_TRAITS[blockchain]}) "
                    f"from the perspective of {stakeholder} — focusing on "
                    f"{STAKEHOLDER_FOCUS[stakeholder]}. "
                    f"Trend context: {TREND_DESC[trend]}."
                )
                nodes.append({
                    "id": f"H9-{node_id:04d}",
                    "node_id": node_id,
                    "blockchain": blockchain,
                    "stakeholder": stakeholder,
                    "trend": trend,
                    "blockchain_idx": b_idx,
                    "stakeholder_idx": s_idx,
                    "trend_idx": t_idx,
                    "digital_root": digital_root(node_id),
                    "description": description,
                })
                node_id += 9

    return nodes


def main() -> None:
    nodes = generate_matrix()
    assert len(nodes) == 729, f"Expected 729, got {len(nodes)}"
    assert all(n["digital_root"] == 9 for n in nodes), "Digital root invariant violated!"

    out_path = Path(__file__).parent / "matrix_729.json"
    out_path.write_text(json.dumps(nodes, indent=2), encoding="utf-8")
    print(f"✅ Generated {len(nodes)} matrix nodes → {out_path}")
    print(f"   ID range: {nodes[0]['id']} — {nodes[-1]['id']}")
    print(f"   All digital roots = 9: ✓")


if __name__ == "__main__":
    main()
