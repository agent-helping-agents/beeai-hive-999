#!/bin/bash
set -e

# System prerequisites
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3.11 python3.11-venv python3.11-dev \
    python3-pip git curl wget build-essential jq tmux htop tree

# Install uv (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh
sudo systemctl enable ollama && sudo systemctl start ollama

# Pull models
ollama pull granite3.3:8b       # Primary reasoning model
ollama pull llama3.1:8b         # General/fallback
ollama pull deepseek-r1:8b      # Deep reasoning
ollama pull nomic-embed-text    # Embedding model for RAG
