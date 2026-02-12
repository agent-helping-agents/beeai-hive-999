#!/bin/bash
echo "🔬 Starting Baker Street Laboratory Desktop App"
echo "=============================================="

# Check if API server is running
if ! curl -s -f "http://localhost:5000/api/v2/system/health" > /dev/null 2>&1; then
    echo "⚠️  Warning: API server not detected at http://localhost:5000"
    echo "   Please start the API server first: ../api/start_api.sh"
    echo "   Or configure a different API URL in the app settings"
fi

# Start the desktop app
npm start
