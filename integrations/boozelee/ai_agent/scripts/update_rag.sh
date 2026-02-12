#!/bin/bash
# Update RAG knowledge base

set -e

echo "🧠 Updating RAG Knowledge Base"
echo "=============================="

# Check if docs directory exists
if [ ! -d "docs" ]; then
    echo "📁 Creating docs directory..."
    mkdir -p docs
    echo "Add markdown files to docs/ directory"
fi

# Update FAISS index
python3 langchain_rag.py --mode update-index --docs-dir docs

echo ""
echo "✅ RAG index updated!"
