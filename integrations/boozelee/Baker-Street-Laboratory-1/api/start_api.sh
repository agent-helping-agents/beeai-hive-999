#!/bin/bash

# Baker Street Laboratory - API Startup Script
# Starts the Flask API server with proper environment setup

set -e  # Exit on any error

echo "🔬 Baker Street Laboratory - API Server"
echo "======================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to project root
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    print_error "Virtual environment not found. Please run ./install.sh first."
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source .venv/bin/activate
print_success "Virtual environment activated"

# Check environment configuration
if [ ! -f ".env" ]; then
    print_error ".env file not found. Please copy .env.example to .env and configure it."
    exit 1
fi

# Load environment variables
source .env

# Check for required API keys
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    print_warning "No AI API keys found in .env file. Some features may not work."
fi

# Install API dependencies if needed
print_status "Checking API dependencies..."
pip install -q flask flask-cors flask-restx fastapi uvicorn

# Create API output directory
mkdir -p research/api_output

# Set Python path
export PYTHONPATH="$PROJECT_ROOT/implementation/src:$PYTHONPATH"

# Start the API server
print_status "Starting Baker Street Laboratory API server..."
print_status "API Documentation will be available at: http://localhost:5000/docs/"
print_status "API Base URL: http://localhost:5000/api/v1/"
print_success "Press Ctrl+C to stop the server"

echo
echo "🚀 Available Endpoints:"
echo "  GET  /                           - API information"
echo "  GET  /docs/                      - Interactive API documentation"
echo "  POST /api/v1/research/conduct    - Conduct research"
echo "  GET  /api/v1/research/status/<id> - Get research status"
echo "  GET  /api/v1/system/health       - System health check"
echo "  GET  /api/v1/system/info         - System information"
echo "  GET  /api/v1/reports/list        - List all reports"
echo "  GET  /api/v1/reports/<id>        - Get specific report"
echo

# Start the Flask server
python3 api/app.py
