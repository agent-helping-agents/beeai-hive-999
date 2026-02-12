#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────
# Hive 999 — Startup Script
# ─────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VENV_DIR="$HOME/beeai-hive-999/.venv"
MATRIX_FILE="data/matrix/matrix_729.json"
VECTORS_DIR="data/vectors/hive_vectors"

echo "🐝 Hive 999 — Starting up..."

# 0. Tailscale integration
echo "🔒 Checking Tailscale..."
if command -v tailscale &>/dev/null; then
    if tailscale status | grep -q "Connected"; then
        echo "✅ Tailscale already connected"
    else
        echo "⚠️  Tailscale not connected. Starting..."
        if sudo systemctl start tailscaled 2>/dev/null; then
            echo "✅ Tailscale daemon started"
        fi
        
        # Try to connect automatically (will prompt for authentication if needed)
        if tailscale up --hostname "beeai-hive" 2>/dev/null; then
            echo "✅ Tailscale connected"
        else
            echo "⚠️  Tailscale connection failed (will continue without Tailscale)"
        fi
    fi
else
    echo "ℹ️  Tailscale not installed"
fi

# 1. Check Ollama
echo "🔍 Checking Ollama..."
if ! command -v ollama &>/dev/null; then
    echo "❌ Ollama not found. Install from https://ollama.ai"
    exit 1
fi

if ! curl -sf http://localhost:11434/api/tags &>/dev/null; then
    echo "⚠️  Ollama not running. Starting..."
    ollama serve &
    sleep 3
fi
echo "✅ Ollama is running"

# 2. Activate venv
echo "🔍 Activating virtual environment..."
if [ -d "$VENV_DIR" ]; then
    source "$VENV_DIR/bin/activate"
    echo "✅ Venv activated: $VENV_DIR"
else
    echo "❌ Venv not found at $VENV_DIR"
    echo "   Run: python3 -m venv $VENV_DIR && source $VENV_DIR/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# 3. Check/generate matrix
if [ ! -f "$MATRIX_FILE" ]; then
    echo "📦 Generating matrix_729.json..."
    python data/matrix/generate_matrix.py
else
    echo "✅ Matrix file exists"
fi

# 4. Check/generate embeddings
if [ ! -d "$VECTORS_DIR" ] || [ -z "$(ls -A "$VECTORS_DIR" 2>/dev/null)" ]; then
    echo "📦 Embedding matrix into ChromaDB..."
    python data/embeddings/embed_matrix.py
else
    echo "✅ Vector store exists"
fi

# 5. Launch
echo ""
echo "🐝 ═══════════════════════════════════════"
echo "   HIVE 999 — Ready for launch"
echo "   ═══════════════════════════════════════"
echo ""

# Default: TUI. Pass --repl or --non-interactive as needed.
exec python main.py "$@"
