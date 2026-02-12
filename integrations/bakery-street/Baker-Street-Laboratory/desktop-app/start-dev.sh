#!/bin/bash
echo "🔬 Starting Baker Street Laboratory Desktop App (Development Mode)"
echo "================================================================"

# Check if API server is running
if ! curl -s -f "http://localhost:5000/api/v2/system/health" > /dev/null 2>&1; then
    echo "⚠️  API server not detected. Starting API server..."
    cd ../api && ./start_api.sh &
    API_PID=$!
    echo "API server started with PID: $API_PID"
    sleep 5
fi

# Start the desktop app in development mode
NODE_ENV=development npm run dev
