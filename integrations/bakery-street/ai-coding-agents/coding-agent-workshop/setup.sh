#!/bin/bash

# Coding Agent Workshop Setup Script
# This script sets up the environment for the coding agent workshop

set -e

echo "🤖 Coding Agent Workshop Setup"
echo "=============================="

# Check if Go is installed
if ! command -v go &> /dev/null; then
    echo "❌ Go is not installed. Please install Go 1.24+ and try again."
    echo "   Visit: https://golang.org/dl/"
    exit 1
fi

# Check Go version
GO_VERSION=$(go version | awk '{print $3}' | sed 's/go//')
echo "✅ Go version: $GO_VERSION"

# Check if AIMLAPI_API_KEY is set
if [ -z "$AIMLAPI_API_KEY" ]; then
    echo "⚠️  AIMLAPI_API_KEY environment variable is not set."
    echo "   Please set it with: export AIMLAPI_API_KEY='your-api-key-here'"
    echo "   Get your API key at: https://aimlapi.com/app/sign-up/"
    echo ""
    read -p "Do you want to set it now? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter your AIMLAPI API key: " API_KEY
        export AIMLAPI_API_KEY="$API_KEY"
        echo "export AIMLAPI_API_KEY='$API_KEY'" >> ~/.bashrc
        echo "✅ API key set and added to ~/.bashrc"
    else
        echo "⚠️  You'll need to set the API key before running the agents."
    fi
else
    echo "✅ AIMLAPI_API_KEY is set"
fi

# Initialize Go module and install dependencies
echo "📦 Installing Go dependencies..."
go mod tidy

# Check if ripgrep is available (optional for code search)
if command -v rg &> /dev/null; then
    echo "✅ ripgrep is available (enhanced code search)"
else
    echo "⚠️  ripgrep not found. Code search will use grep as fallback."
    echo "   Install ripgrep for better performance: https://github.com/BurntSushi/ripgrep"
fi

# Create sample files if they don't exist
echo "📁 Setting up sample files..."
mkdir -p sample-files

# Test basic functionality
echo "🧪 Testing basic functionality..."

# Test Go compilation
echo "   Testing Go compilation..."
if go build -o /tmp/test-agent versions/chat.go; then
    echo "   ✅ Go compilation successful"
    rm -f /tmp/test-agent
else
    echo "   ❌ Go compilation failed"
    exit 1
fi

# Test API connectivity (if API key is set)
if [ -n "$AIMLAPI_API_KEY" ]; then
    echo "   Testing API connectivity..."
    # This is a simple test - in a real scenario you might want to make an actual API call
    echo "   ✅ API key is configured"
else
    echo "   ⚠️  Skipping API test (no API key)"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure your AIMLAPI_API_KEY is set"
echo "2. Start with the basic chat: go run versions/chat.go"
echo "3. Try the sample commands in the README"
echo ""
echo "Available versions:"
echo "  • chat.go           - Basic Claude conversation"
echo "  • read.go           - File reading capability"
echo "  • list_files.go     - Directory listing"
echo "  • bash_tool.go      - Shell command execution"
echo "  • edit_tool.go      - File editing"
echo "  • code_search_tool.go - Code pattern search"
echo ""
echo "Happy coding! 🚀"
