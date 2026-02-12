#!/usr/bin/env python3
"""
Embed the 729 matrix nodes into ChromaDB using its default ONNX embedder.

Reads: data/matrix/matrix_729.json
Writes: data/vectors/hive_vectors/ (ChromaDB persistent storage, collection "matrix_999")
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = PROJECT_ROOT / "data" / "matrix" / "matrix_729.json"
VECTORS_DIR = PROJECT_ROOT / "data" / "vectors" / "hive_vectors"
COLLECTION_NAME = "matrix_999"
BATCH_SIZE = 100


def main() -> None:
    if not MATRIX_PATH.exists():
        print(f"❌ Matrix file not found: {MATRIX_PATH}")
        print("   Run generate_matrix.py first.")
        sys.exit(1)

    nodes = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    print(f"📦 Loaded {len(nodes)} matrix nodes")

    import chromadb

    VECTORS_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(VECTORS_DIR))

    # Delete existing collection if present
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"🗑  Deleted existing collection '{COLLECTION_NAME}'")
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    print(f"📁 Created collection '{COLLECTION_NAME}' with cosine similarity")

    # Insert in batches
    for i in range(0, len(nodes), BATCH_SIZE):
        batch = nodes[i : i + BATCH_SIZE]
        collection.add(
            ids=[n["id"] for n in batch],
            documents=[n["description"] for n in batch],
            metadatas=[
                {
                    "blockchain": n["blockchain"],
                    "stakeholder": n["stakeholder"],
                    "trend": n["trend"],
                    "digital_root": n["digital_root"],
                    "node_id": n["node_id"],
                }
                for n in batch
            ],
        )
        print(f"   Embedded {min(i + BATCH_SIZE, len(nodes))}/{len(nodes)} nodes")

    print(f"✅ All {len(nodes)} nodes embedded into '{COLLECTION_NAME}'")
    print(f"   Storage: {VECTORS_DIR}")


if __name__ == "__main__":
    main()
