#!/bin/bash

# BakerCode Startup Script
echo "🍞 Starting BakerCode Platform..."

# Set default port if not provided
export PORT=${PORT:-8000}

# Create necessary directories
mkdir -p /app/data

echo "📊 Starting Web Dashboard on port $PORT..."
cd /app/codex-superlab-recreation

# Start the web dashboard
exec gunicorn web_dashboard:app \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info