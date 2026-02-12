#!/bin/bash
# Start beeAI locally for development

set -e

echo "🐝 Starting beeAI in development mode..."

# Check if running in correct directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run from beeAI root directory"
    exit 1
fi

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "📍 Python version: $python_version"

# Setup virtual environment if needed
if [ ! -d ".venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

# Set environment variables
export T221B_SECRET_KEY="${T221B_SECRET_KEY:-dev-secret-key-not-for-production}"
export ENV="development"
export LOG_LEVEL="debug"

# Start services
echo "🚀 Starting services..."
echo "   API Server: http://localhost:22181"
echo "   Health:     http://localhost:22181/health"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run the secure server
python -m src.api.secure_server_fixed
