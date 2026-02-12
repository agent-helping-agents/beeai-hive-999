#!/bin/bash

# Baker Street Laboratory - Installation Script
# This script sets up the complete research environment

set -e  # Exit on any error

echo "🔬 Baker Street Laboratory - Installation Script"
echo "================================================="

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

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python installation..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
        
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python 3.8+ required, found $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8 or higher."
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [ ! -d ".venv" ]; then
        $PYTHON_CMD -m venv .venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source .venv/bin/activate
    print_success "Virtual environment activated"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    # Upgrade pip first
    pip install --upgrade pip
    
    # Install requirements
    pip install -r requirements.txt
    
    print_success "Dependencies installed"
}

# Create environment file
setup_environment() {
    print_status "Setting up environment configuration..."
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        print_success "Environment file created from template"
        print_warning "Please edit .env file with your API keys and configuration"
    else
        print_warning ".env file already exists"
    fi
}

# Create necessary directories
create_directories() {
    print_status "Creating necessary directories..."
    
    # Create data directories
    mkdir -p data/vector_store
    mkdir -p data/cache
    mkdir -p data/temp
    
    # Create log directory
    mkdir -p logs
    
    print_success "Directories created"
}

# Initialize databases
init_databases() {
    print_status "Initializing databases..."

    # Run the database initialization script
    if python3 implementation/src/database/init_db.py; then
        print_success "Database initialized successfully"
    else
        print_error "Database initialization failed"
        exit 1
    fi
}

# Install optional tools
install_optional_tools() {
    print_status "Checking for optional tools..."
    
    # Check for Git
    if command -v git &> /dev/null; then
        print_success "Git found"
    else
        print_warning "Git not found - version control features will be limited"
    fi
    
    # Check for Ollama (for local LLM support)
    if command -v ollama &> /dev/null; then
        print_success "Ollama found - local LLM support available"
    else
        print_warning "Ollama not found - only API-based LLMs will be available"
        print_status "To install Ollama: curl -fsSL https://ollama.ai/install.sh | sh"
    fi
}

# Main installation process
main() {
    echo
    print_status "Starting Baker Street Laboratory installation..."
    echo
    
    check_python
    create_venv
    activate_venv
    install_dependencies
    setup_environment
    create_directories
    init_databases
    install_optional_tools
    
    echo
    print_success "Installation completed successfully!"
    echo
    echo "Next steps:"
    echo "1. Edit the .env file with your API keys"
    echo "2. Run './run.sh' to start the research pipeline"
    echo "3. Check the documentation in implementation/docs/"
    echo
    print_status "Happy researching! 🔬"
}

# Run main function
main "$@"
