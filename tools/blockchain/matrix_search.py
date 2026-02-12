"""
Matrix Search Tool — semantic search over the 729-node Hive matrix via ChromaDB.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from beeai_framework.tools import tool

# ChromaDB paths (relative to project root)
PROJECT_ROOT = Path(__file__).resolve().parents[2]
VECTORS_DIR = PROJECT_ROOT / "data" / "vectors" / "hive_vectors"
COLLECTION_NAME = "matrix_999"


def _get_collection():
    """Lazily connect to the ChromaDB collection."""
    import chromadb
    client = chromadb.PersistentClient(path=str(VECTORS_DIR))
    return client.get_collection(COLLECTION_NAME)


@tool
def matrix_search_tool(
    query: str,
    n_results: int = 5,
    blockchain_filter: str = "",
    stakeholder_filter: str = "",
    trend_filter: str = "",
) -> str:
    """Search the Hive 999 matrix (729 nodes) using semantic similarity.

    Args:
        query: Natural language search query.
        n_results: Number of results to return (default 5, max 20).
        blockchain_filter: Optional — filter to a specific blockchain.
        stakeholder_filter: Optional — filter to a specific stakeholder group.
        trend_filter: Optional — filter to a specific trend.

    Returns:
        JSON array of matching matrix nodes with id, blockchain, stakeholder,
        trend, digital_root, description, and similarity score.
    """
    n_results = min(max(1, n_results), 20)

    # Build where clause for metadata filters
    where_clauses: list[dict[str, Any]] = []
    if blockchain_filter:
        where_clauses.append({"blockchain": blockchain_filter})
    if stakeholder_filter:
        where_clauses.append({"stakeholder": stakeholder_filter})
    if trend_filter:
        where_clauses.append({"trend": trend_filter})

    where: dict[str, Any] | None = None
    if len(where_clauses) == 1:
        where = where_clauses[0]
    elif len(where_clauses) > 1:
        where = {"$and": where_clauses}

    try:
        collection = _get_collection()
        kwargs: dict[str, Any] = {
            "query_texts": [query],
            "n_results": n_results,
        }
        if where:
            kwargs["where"] = where

        results = collection.query(**kwargs)

        nodes: list[dict[str, Any]] = []
        if results and results["ids"]:
            for i, node_id in enumerate(results["ids"][0]):
                meta = results["metadatas"][0][i] if results["metadatas"] else {}
                doc = results["documents"][0][i] if results["documents"] else ""
                dist = results["distances"][0][i] if results["distances"] else None
                nodes.append({
                    "id": node_id,
                    "blockchain": meta.get("blockchain", ""),
                    "stakeholder": meta.get("stakeholder", ""),
                    "trend": meta.get("trend", ""),
                    "digital_root": meta.get("digital_root", 9),
                    "description": doc,
                    "distance": round(dist, 4) if dist is not None else None,
                })

        return json.dumps(nodes, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e), "hint": "Run embed_matrix.py first."})
